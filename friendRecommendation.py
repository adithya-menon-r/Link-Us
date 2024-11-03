# Import from provided files
from social_network import SocialNetwork
from hobby_network import HobbyNetwork
from max_heap import MaxHeap
from typing import List, Tuple, Dict
from collections import defaultdict

class FriendRecommender:
    def __init__(self, social_network: SocialNetwork, hobby_network: HobbyNetwork):
        self.social_network = social_network
        self.hobby_network = hobby_network
        self.popularity_cache = {}  # Cache for user popularity scores
        
    def calculate_popularity_score(self, username: str) -> float:
        """Calculate popularity score based on friend count and engagement"""
        if username in self.popularity_cache:
            return self.popularity_cache[username]
            
        user = self.social_network.vertices.get(username)
        if not user:
            return 0.0
            
        # Get user's posts and their engagement
        posts = self.social_network.get_user_posts(username)
        total_engagement = 0
        
        for _, post in posts:
            total_engagement += len(post.likes) * 2  # Likes weight
            total_engagement += len(post.comments) * 3  # Comments weight
            
        # Combine friend count and engagement
        friend_count = len(user.adjacency_map)
        popularity = (friend_count * 0.6) + (total_engagement * 0.4)
        
        # Cache the result
        self.popularity_cache[username] = popularity
        return popularity
        
    def get_friends_of_friends(self, username: str) -> Dict[str, int]:
        """Get friends of friends and their frequency"""
        user = self.social_network.vertices.get(username)
        if not user:
            return {}
            
        fof_count = defaultdict(int)
        # For each friend
        for friend in user.adjacency_map:
            # Look at their friends
            for friend_of_friend in friend.adjacency_map:
                if friend_of_friend.username != username and friend_of_friend not in user.adjacency_map:
                    fof_count[friend_of_friend.username] += 1
                    
        return fof_count
        
    def calculate_hobby_similarity(self, user1_hobbies: set, user2_hobbies: set) -> float:
        """Calculate hobby similarity using Jaccard similarity"""
        if not user1_hobbies or not user2_hobbies:
            return 0.0
            
        intersection = len(user1_hobbies & user2_hobbies)
        union = len(user1_hobbies | user2_hobbies)
        return intersection / union if union > 0 else 0
        
    def get_recommendations(self, username: str, limit: int = 10) -> List[Tuple[str, float]]:
        """Get friend recommendations with scores"""
        user = self.social_network.vertices.get(username)
        if not user:
            return []
            
        # Initialize scoring components
        candidates = {}
        fof_counts = self.get_friends_of_friends(username)
        
        # Calculate scores for each candidate
        for candidate_username, candidate in self.social_network.vertices.items():
            # Skip if already friends or self
            if candidate_username == username or candidate in user.adjacency_map:
                continue
                
            # Initialize base score
            score = 0.0
            
            # 1. Friends of friends score (30%)
            fof_score = fof_counts.get(candidate_username, 0) * 0.3
            
            # 2. Mutual friends score (25%)
            mutual_friends = self.social_network.common_friends(username, candidate_username)
            mutual_score = (mutual_friends / max(len(candidate.adjacency_map), 1)) * 0.25
            
            # 3. Hobby similarity score (25%)
            hobby_score = self.calculate_hobby_similarity(user.hobbies, candidate.hobbies) * 0.25
            
            # 4. Popularity score (20%)
            popularity = self.calculate_popularity_score(candidate_username)
            max_popularity = max(self.calculate_popularity_score(u) for u in self.social_network.vertices.keys())
            popularity_score = (popularity / max_popularity if max_popularity > 0 else 0) * 0.20
            
            # Combine all scores
            total_score = fof_score + mutual_score + hobby_score + popularity_score
            candidates[candidate_username] = total_score
        
        # Use the provided MaxHeap class for getting top recommendations
        recommendation_heap = MaxHeap()
        for username, score in candidates.items():
            recommendation_heap.insert((score, username))
        
        # Extract recommendations in descending order
        recommendations = []
        for _ in range(min(limit, len(candidates))):
            if recommendation_heap.is_empty():  # Using sz to check if heap is empty
                break
            score, username = recommendation_heap.extract_max()
            recommendations.append((username, score))
            
        return recommendations