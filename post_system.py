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
        
    def __repr__(self) -> str:
        likes_count = len(self.likes)
        comments_count = len(self.comments)
        return f"""
[Post by {self.author} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]
{self.content}

❤️   {likes_count} {'like' if likes_count == 1 else 'likes'} | 💬 {comments_count} {'comment' if comments_count == 1 else 'comments'}
"""
