from datetime import datetime
import heapq
import math
from hashmap import ChainHashMap
from typing import List, Set, Tuple, Optional

class Post:
    """Represents a social network post with content, likes, and comments"""
    def __init__(self, content: str, author: str, timestamp: datetime = None):
        self.content = content
        self.author = author
        self.timestamp = timestamp or datetime.now()
        self.likes: Set[str] = set()  # Set of usernames who liked the post
        self.comments: List[Tuple[str, str, datetime]] = []  # List of (username, comment, timestamp)
        
    def add_like(self, username: str) -> None:
        """Add a like to the post"""
        self.likes.add(username)
        
    def remove_like(self, username: str) -> None:
        """Remove a like from the post"""
        self.likes.discard(username)
        
    def add_comment(self, username: str, comment: str) -> None:
        """Add a comment to the post"""
        self.comments.append((username, comment, datetime.now()))

    def priority_score(self, viewer_username: str, interaction_history: dict) -> float:
        """Calculates a priority score for ranking in personalized feeds."""
        # Time decay factor: newer posts get higher scores
        time_diff = (datetime.now() - self.timestamp).total_seconds()
        time_decay = math.exp(-time_diff / (60 * 60 * 24))  # Half-life of one day
        
        # Engagement factor: likes and comments add to score
        engagement_score = len(self.likes) * 2 + len(self.comments) * 3

        # User affinity: based on interaction frequency
        affinity_score = interaction_history.get(self.author, 0) * 1.5
        
        # Final score combines factors with weights
        return time_decay * 0.4 + engagement_score * 0.4 + affinity_score * 0.2
        
    def __repr__(self) -> str:
        likes_count = len(self.likes)
        comments_count = len(self.comments)
        return f"""
[Post by {self.author} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]
{self.content}

❤️ {likes_count} {'like' if likes_count == 1 else 'likes'} | 💬 {comments_count} {'comment' if comments_count == 1 else 'comments'}
"""

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

    def send_friend_request(self, from_user, to_user):
        if to_user in self.vertices and from_user not in self.vertices[to_user].inbox:
            self.vertices[to_user].inbox.append(from_user)
            return True
        return False

    def accept_friend_request(self, username, requester):
        user = self.vertices[username]
        if requester in user.inbox:
            self.make_connections(username, requester)
            user.inbox.remove(requester)
            return True
        return False

    def send_message(self, from_user, to_user, message):
        if to_user in self.vertices and from_user in self.vertices[to_user].adjacency_map:
            self.vertices[to_user].messages.append(f"From {from_user}: {message}")
            return True
        return False

    def get_messages(self, username):
        return list(self.vertices[username].messages)

    def get_friend_requests(self, username):
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
    
    def get_personalized_feed(self, username: str) -> List[Post]:
        """Generates a personalized feed using a priority queue for ranking."""
        if username not in self.vertices:
            return []

        # Get friend posts and calculate priority scores
        posts_heap = []
        user = self.vertices[username]
        
        for friend in user.adjacency_map:
            friend_post_ids = self.user_posts.get(friend.username) or []
            for pid in friend_post_ids:
                post = self.posts.get(pid)
                if post:
                    # Calculate priority score and push to heap
                    score = post.priority_score(username, self.interaction_history.get(username, {}))
                    heapq.heappush(posts_heap, (-score, post))  # Use negative for max-heap behavior

        # Retrieve top-ranked posts
        feed = []
        while posts_heap and len(feed) < 10:
            _, post = heapq.heappop(posts_heap)
            feed.append(post)
        
        return feed

    def get_post(self, post_id: str) -> Optional[Post]:
        """Get a specific post by ID"""
        return self.posts.get(post_id)
