from typing import List, Tuple, Dict
from collections import defaultdict

# Import from provided files
from max_heap import MaxHeap
from social_network import SocialNetwork
from hobby_network import HobbyNetwork

class FriendRecommender:
    def __init__(self, social_network: SocialNetwork, hobby_network: HobbyNetwork):
        # Initialize with instances of SocialNetwork and HobbyNetwork
        self.social_network = social_network
        self.hobby_network = hobby_network
        self.popularity_cache = {}   # Cache to store calculated popularity scores for faster access

    """
        (method) def calculate_popularity_score(
            self: Self@FriendRecommender,
            username: str
        ) -> float
    """ 
    def calculate_popularity_score(self, username: str) -> float: 
        """
            Calculate a user's popularity score based on friend count and engagement

            Time Complexity: O(P) where P is the number of posts by the user
            Justification: Must process each post exactly once to calculate engagement scores, with constant-time operations per post.
        """
        if username in self.popularity_cache:
            return self.popularity_cache[username] # Return cached score if it exists
            
        user = self.social_network.vertices.get(username)
        if not user:
            return 0.0 # Return 0 if the user doesn't exist
            
        # Get user's posts
        posts = self.social_network.get_user_posts(username)  # List[(pid, post obj)]
        total_engagement = 0
        
        for _, post in posts:
            total_engagement += len(post.likes) * 2  # Weighted score for likes
            total_engagement += len(post.comments) * 3  # Weighted score for Comments
            
        # Combine friend count and engagement
        friend_count = len(user.adjacency_map)
        popularity = (friend_count * 0.6) + (total_engagement * 0.4)
        
        # Cache the result
        self.popularity_cache[username] = popularity
        return popularity
        
    """
        (method) def get_friends_of_friends(
            self: Self@FriendRecommender,
            username: str
        ) -> Dict[str, int]
    """
    def get_friends_of_friends(self, username: str) -> Dict[str, int]:
        """
            Get friends of friends and their frequency

            Time Complexity:  O(F * F') where F is number of friends of the user and F' is average number of friends per friend
            Justification: Must examine every friend (F) and then every friend of each friend (F') to build complete 
                           friends-of-friends list.
        """
        user = self.social_network.vertices.get(username) # Get the user object corresponding to the username
        if not user:
            return {}
            
        fof_count = defaultdict(int)
        # Iterate through each friend and get their friends (friends of friends)
        for friend in user.adjacency_map:
            for friend_of_friend in friend.adjacency_map:
                # Count only if they’re not the user and are not a direct friend
                if friend_of_friend.username != username and friend_of_friend not in user.adjacency_map:
                    fof_count[friend_of_friend.username] += 1
                    
        return fof_count
        
    """
        (method) def calculate_hobby_similarity(
            self: Self@FriendRecommender,
            user1_hobbies: set,
            user2_hobbies: set
        ) -> float
    """
    def calculate_hobby_similarity(self, user1_hobbies: set, user2_hobbies: set) -> float:
        """
            Calculate hobby similarity using Jaccard similarity

            Time Complexity: O(min(H1, H2)) where H1 and H2 are sizes of hobby sets
            Justification: Set intersection/union operations only need to process elements from the smaller set once.    
        """
        if not user1_hobbies or not user2_hobbies:
            return 0.0
            
        intersection = len(user1_hobbies & user2_hobbies)
        union = len(user1_hobbies | user2_hobbies)
        return intersection / union if union > 0 else 0 # JS(A, B) = |A ∩ B| / |A ∪ B|
        
    """
        (method) def get_recommendations(
            self: Self@FriendRecommender,
            username: str,
            limit: int = 5
        ) -> List[Tuple[str, float]]
    """
    def get_recommendations(self, username: str, limit: int = 5) -> List[Tuple[str, float]]:
        """
            Get friend recommendations with scores

            Time Complexity: O(N * (F*F' + P + H)) where N is no. of users in the network, F is no. of friends per user,
                                F' is average no. of friends of friends, P is average no. of posts per user and 
                                H is average no. of hobbies per user.
            Justification: Must calculate comprehensive scores for every user in the network (N), with each score 
                           calculation requiring friends-of-friends lookup, post analysis, and hobby comparison.
        """
        user = self.social_network.vertices.get(username)
        if not user:
            return []
            
        # Initialize scoring components
        candidates = {}
        fof_counts = self.get_friends_of_friends(username)
        
        # Calculate scores for each candidate
        for candidate_username, candidate in self.social_network.vertices.items():
            # Skip if candidate is the user themselves or already a friend
            if candidate_username == username or candidate in user.adjacency_map:
                continue
                
            # Initialize base score
            score = 0.0
            
            # 1. Friends of friends score (30% weight)
            fof_score = fof_counts[candidate_username] * 0.3
            
            # 2. Mutual friends score (25% weight)
            mutual_friends = self.social_network.common_friends(username, candidate_username)
            mutual_score = (mutual_friends / max(len(candidate.adjacency_map), 1)) * 0.25
            
            # 3. Hobby similarity score (25% weight)
            hobby_score = self.calculate_hobby_similarity(user.hobbies, candidate.hobbies) * 0.25
            
            # 4. Popularity score (20% weight)
            popularity = self.calculate_popularity_score(candidate_username)
            max_popularity = max(self.calculate_popularity_score(u) for u in self.social_network.vertices.keys())
            popularity_score = (popularity / max_popularity if max_popularity > 0 else 0) * 0.20
            
            # Combine all scores
            total_score = fof_score + mutual_score + hobby_score + popularity_score
            candidates[candidate_username] = total_score
        
        # Use MaxHeap for getting top recommendations
        recommendation_heap = MaxHeap()
        for username, score in candidates.items():
            recommendation_heap.insert((score, username))
        
        # Extract recommendations in descending order
        recommendations = []
        for _ in range(min(limit, len(candidates))):
            if recommendation_heap.is_empty():
                break
            score, username = recommendation_heap.extract_max()
            recommendations.append((username, score))
            
        return recommendations
