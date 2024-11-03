import math
from datetime import datetime
from typing import List, Set, Tuple

class Post:
    """Represents a social network post with content, likes, and comments"""
    current_post_id = 0
    def __init__(self, content: str, author: str, timestamp: datetime = None):
        self.pid = Post.current_post_id
        Post.current_post_id += 1
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
        # Time delay factor: newer posts get higher scores
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

❤️   {likes_count} {'like' if likes_count == 1 else 'likes'} | 💬 {comments_count} {'comment' if comments_count == 1 else 'comments'}
"""
