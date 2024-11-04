from datetime import datetime
from typing import List, Tuple, Optional

from hash_map import ChainHashMap
from max_heap import MaxHeap
from post_system import Post

class Deque:
    def __init__(self):
        self.items = []
    
    def append(self, item):
        self.items.append(item)

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)

    def __iter__(self):
        return iter(self.items)

    def __repr__(self):
        return repr(self.items)

class Vertex:
    def __init__(self, name, username, hobbies, description=None):
        self.name = name
        self.hobbies = set(hobbies)
        self.description = description
        self.username = username
        self.adjacency_map = dict()
        self.inbox = Deque()
        self.messages = Deque()

class Edge:
    def __init__(self, vertex1, vertex2):
        self.vertex1 = vertex1
        self.vertex2 = vertex2

class SocialNetwork:
    def __init__(self):
        self.vertices = dict()
        # Initialize hashmaps for posts
        self.posts = ChainHashMap()  # Maps post_id to Post objects
        self.user_posts = ChainHashMap()  # Maps username to list of post IDs
        self.post_counter = 0  # For generating unique post IDs
        self.interaction_history = {}  # Track user interactions

    def add_person(self, name, username, hobbies, description=None):
        person = Vertex(name, username, hobbies, description)
        self.vertices[username] = person
        return True

    def make_connections(self, username1, username2):
        person1 = self.vertices[username1]
        person2 = self.vertices[username2]
        connection = Edge(person1, person2)
        person1.adjacency_map[person2] = connection
        person2.adjacency_map[person1] = connection

    def recommend_friends(self, name, limit=3):
        recommendations = []
        person = self.vertices[name]
        
        for potential_friend_name, potential_friend in self.vertices.items():
            if potential_friend_name == name or potential_friend in person.adjacency_map:
                continue
            
            common_hobbies = len(person.hobbies & potential_friend.hobbies)
            if common_hobbies > 0:
                recommendations.append((common_hobbies, potential_friend_name))
        
        recommendations.sort(reverse=True, key=lambda x: x[0])
        return [user[1] for user in recommendations[:limit]]

    def common_friends(self, username1, username2):
        count = 0
        person1 = self.vertices[username1]
        person2 = self.vertices[username2]
        if len(person1.adjacency_map) < len(person2.adjacency_map):
            for friend in person1.adjacency_map:
                if friend in person2.adjacency_map:
                    count += 1
        else:
            for friend in person2.adjacency_map:
                if friend in person1.adjacency_map:
                    count += 1
        return count

    """
    (method) def send_friend_request(
        self: Self@SocialNetwork,
        from_user: Any,
        to_user: Any
    ) -> bool
    """
    def send_friend_request(self, from_user, to_user):
        """
        Sends a friend request from one user to another.

        Time Complexity: O(1) - Direct dictionary access and append operation are constant time
        """
        if to_user in self.vertices and from_user not in self.vertices[to_user].inbox:
            self.vertices[to_user].inbox.append(from_user)
            return True
        return False

    """
    (method) def accept_friend_request(
        self: Self@SocialNetwork,
        username: Any,
        requester: Any
    ) -> bool
    """
    def accept_friend_request(self, username, requester):
        """
        Accepts a friend request from a requester to the specified user.

        Time Complexity: O(1) - Dictionary lookup, remove from list, and make_connections are all constant time operations
        """
        user = self.vertices[username]
        if requester in user.inbox:
            self.make_connections(username, requester)
            user.inbox.remove(requester)
            return True
        return False

    """
    (method) def send_message(
        self: Self@SocialNetwork,
        from_user: Any,
        to_user: Any,
        message: Any
    ) -> bool
    """
    def send_message(self, from_user, to_user, message):
        """
        Sends a message from one user to another if they are friends.

        Time Complexity: O(1) - Dictionary lookups and append operation are constant time
        """
        if to_user not in self.vertices or from_user not in self.vertices:
            return False
        to_vertex = self.vertices[to_user]
        from_vertex = self.vertices[from_user]
        if from_vertex in to_vertex.adjacency_map:
            to_vertex.messages.append(f"From {from_user}: {message}")
            return True
        return False

    """
    (method) def get_messages(
        self: Self@SocialNetwork,
        username: Any
    ) -> list
    """
    def get_messages(self, username):
        """
        Retrieves all messages received by a specified user.

        Time Complexity: O(n) where n is the number of messages - Creating a new list copies all messages
        """
        return list(self.vertices[username].messages)

    """
    (method) def get_friend_requests(
        self: Self@SocialNetwork,
        username: Any
    ) -> list
    """
    def get_friend_requests(self, username):
        """
        Retrieves all pending friend requests for a specified user.

        Time Complexity: O(n) where n is the number of friend requests - Creating a new list copies all requests
        """
        return list(self.vertices[username].inbox)
    
    def record_interaction(self, user1: str, user2: str):
        """Records interactions to boost affinity scores between users."""
        self.interaction_history[user1] = self.interaction_history.get(user1, {})
        self.interaction_history[user1][user2] = self.interaction_history[user1].get(user2, 0) + 1

    # New methods for post functionality
    def create_post(self, username: str, content: str) -> str:
        """Create a new post and return its ID"""
        post_id = str(self.post_counter)
        self.post_counter += 1
        
        # Create and store the post
        post = Post(content, username)
        self.posts.put(post_id, post)
        
        # Add to user's posts
        user_posts = self.user_posts.get(username) or []
        user_posts.append(post_id)
        self.user_posts.put(username, user_posts)
        
        return post_id

    def like_post(self, post_id: str, username: str) -> bool:
        """Like a post and return success status"""
        post = self.posts.get(post_id)
        if post and username in self.vertices:
            post.add_like(username)
            self.posts.put(post_id, post)
            return True
        return False

    def unlike_post(self, post_id: str, username: str) -> bool:
        """Remove like from a post and return success status"""
        post = self.posts.get(post_id)
        if post and username in post.likes:
            post.remove_like(username)
            self.posts.put(post_id, post)
            return True
        return False

    def comment_on_post(self, post_id: str, username: str, comment: str) -> bool:
        """Add a comment to a post and return success status"""
        post = self.posts.get(post_id)
        if post and username in self.vertices:
            post.add_comment(username, comment)
            self.posts.put(post_id, post)
            return True
        return False

    def get_user_posts(self, username: str) -> List[Tuple[str, Post]]:
        """Get all posts by a user"""
        post_ids = self.user_posts.get(username) or []
        return [(pid, self.posts.get(pid)) for pid in post_ids if self.posts.get(pid) is not None]

    def get_friend_posts(self, username: str) -> List[Tuple[str, Post]]:
        """Get all posts from user's friends"""
        if username not in self.vertices:
            return []
            
        user = self.vertices[username]
        friend_posts = []
        
        # Get posts from all friends
        for friend in user.adjacency_map:
            friend_post_ids = self.user_posts.get(friend.username) or []
            for pid in friend_post_ids:
                post = self.posts.get(pid)
                if post is not None:
                    friend_posts.append((pid, post))
        
        # Sort by timestamp, newest first
        friend_posts.sort(key=lambda x: x[1].timestamp, reverse=True)
        return friend_posts
    
    """
    (method) def get_personalized_feed(
        self: Self@SocialNetwork,
        username: str
    ) -> List[Post]
    """
    def get_personalized_feed(self, username):
        """
        Generates a personalized feed using a priority queue for ranking.

        Time Explanation: Processes all friend posts, calculates scores based on recency/engagement/interactions, uses heap for top 10
        Time Complexity: O(F * P * log(F*P)) where F is number of friends and P is posts per friend - due to heap operations on all friend posts
        
        Ranking factors (in order of importance):
        1. Post recency (40% weight)
        2. Engagement metrics - likes and comments (40% weight)
        3. User interaction frequency (20% weight)
        
        """
        if username not in self.vertices:
            return []

        posts_heap = MaxHeap()
        user = self.vertices[username]
        current_time = datetime.now()
    
        max_time_diff = 60 * 60 * 24 * 7 
        max_engagement = 0
        max_interaction = 0
        
        friend_posts = []
        for friend_vertex in user.adjacency_map.keys():
            friend_username = friend_vertex.username
            friend_post_ids = self.user_posts.get(friend_username) or []
            
            interaction_count = (self.interaction_history.get(username, {})
                            .get(friend_username, 0))
            max_interaction = max(max_interaction, interaction_count)
            
            for pid in friend_post_ids:
                post = self.posts.get(pid)
                if post:
                    engagement = len(post.likes) * 2 + len(post.comments) * 3
                    max_engagement = max(max_engagement, engagement)
                    friend_posts.append((post, interaction_count))
        
        max_engagement = max(max_engagement, 1)
        max_interaction = max(max_interaction, 1)
        
        for post, interaction_count in friend_posts:
            # 1. Recency Score (40% weight)
            time_diff = (current_time - post.timestamp).total_seconds()
            recency_score = 1 - min(time_diff / max_time_diff, 1)
            
            # 2. Engagement Score (40% weight)
            engagement = len(post.likes) * 2 + len(post.comments) * 3
            engagement_score = engagement / max_engagement
            
            # 3. User Interaction Score (20% weight)
            interaction_score = interaction_count / max_interaction
            
            final_score = (
                recency_score * 0.4 +
                engagement_score * 0.4 +
                interaction_score * 0.2
            )
            posts_heap.insert((-final_score, post))

        feed = []
        while len(feed) < 10 and not posts_heap.is_empty():
            score, post = posts_heap.extract_max()
            feed.append(post)
        return feed


    def get_post(self, post_id: str) -> Optional[Post]:
        """Get a specific post by ID"""
        return self.posts.get(post_id)
