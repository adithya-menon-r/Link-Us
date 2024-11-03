from datetime import datetime, timedelta
from collections import deque
from typing import List, Set, Tuple, Optional

class HobbyVertex:
    """Node representing a hobby in the hobby graph"""
    def __init__(self, hobby_name: str):
        self.hobby_name = hobby_name
        self.users = set()  # Set of users with this hobby
        self.connections = {}  # Map to other hobbies and their weights (shared users)
        self.trend_data = deque()  # Efficient handling of timestamped data with deque

    def update_trend_data(self):
        """Add a timestamp entry and maintain only recent data points (last 100)"""
        timestamp = datetime.now()
        self.trend_data.append((timestamp, len(self.users)))
        if len(self.trend_data) > 100:
            self.trend_data.popleft()


class UserVertex:
    """Node representing a user in the hobby graph"""
    def __init__(self, username: str):
        self.username = username
        self.hobbies = set()  # Set of hobbies this user has


class HobbyNetwork:
    """
    Graph-based implementation of the hobby network using adjacency lists
    and custom data structures for optimal performance
    """
    def __init__(self):
        self.hobby_vertices = {}  # Maps hobby_name -> HobbyVertex
        self.user_vertices = {}   # Maps username -> UserVertex
        self.top_hobbies_cache = None
        self.user_with_most_hobbies_cache = None

    def add_hobby(self, hobby_name: str) -> HobbyVertex:
        hobby = hobby_name.lower().strip()
        if not hobby or hobby in self.hobby_vertices:
            return self.hobby_vertices.get(hobby)
        
        self.hobby_vertices[hobby] = HobbyVertex(hobby)
        self.top_hobbies_cache = None  # Invalidate cache
        return self.hobby_vertices[hobby]

    def add_user(self, username: str) -> UserVertex:
        if not username or username in self.user_vertices:
            return self.user_vertices.get(username)

        self.user_vertices[username] = UserVertex(username)
        self.user_with_most_hobbies_cache = None  # Invalidate cache
        return self.user_vertices[username]

    def add_user_hobby(self, username: str, hobby_name: str) -> None:
        hobby = hobby_name.lower().strip()
        
        # Get or create vertices
        hobby_vertex = self.add_hobby(hobby)
        user_vertex = self.add_user(username)
        
        # Avoid duplicate connections
        if hobby in user_vertex.hobbies:
            return

        # Create bidirectional connections
        hobby_vertex.users.add(username)
        user_vertex.hobbies.add(hobby)
        
        hobby_vertex.update_trend_data()  # Update trend data using deque

        # Update hobby connections for recommendations
        for other_hobby in user_vertex.hobbies:
            if other_hobby != hobby:
                self.hobby_vertices[hobby].connections[other_hobby] = \
                    self.hobby_vertices[hobby].connections.get(other_hobby, 0) + 1
                self.hobby_vertices[other_hobby].connections[hobby] = \
                    self.hobby_vertices[other_hobby].connections.get(hobby, 0) + 1

    def add_user_hobbies(self, username: str, hobbies: List[str]) -> None:
        """Add multiple hobbies for a user"""
        for hobby in hobbies:
            self.add_user_hobby(username, hobby)

    def get_all_hobbies(self) -> List[str]:
        """Return sorted list of all hobbies"""
        return sorted(self.hobby_vertices.keys())

    def get_users_by_hobby(self, hobby: str) -> Set[str]:
        """Get all users who have a specific hobby"""
        hobby_vertex = self.hobby_vertices.get(hobby.lower().strip())
        return hobby_vertex.users if hobby_vertex else set()

    def get_top_hobbies(self, limit: int = 10) -> List[Tuple[str, int]]:
        if self.top_hobbies_cache:
            return self.top_hobbies_cache[:limit]

        heap = MaxHeap()
        for hobby, vertex in self.hobby_vertices.items():
            heap.insert((len(vertex.users), hobby))
        
        result = []
        for _ in range(min(limit, len(self.hobby_vertices))):
            if not heap.is_empty():
                count, hobby = heap.extract_max()
                result.append((hobby, count))

        self.top_hobbies_cache = result  # Cache result
        return result

    def get_user_with_most_hobbies(self) -> Tuple[str, int]:
        if self.user_with_most_hobbies_cache:
            return self.user_with_most_hobbies_cache

        max_user = None
        max_count = 0
        
        for username, vertex in self.user_vertices.items():
            hobby_count = len(vertex.hobbies)
            if hobby_count > max_count:
                max_count = hobby_count
                max_user = username
                
        self.user_with_most_hobbies_cache = (max_user, max_count)  # Cache result
        return max_user, max_count

    def get_hobby_trend(self, hobby: str, days: int = 30) -> List[Tuple[datetime, int]]:
        """Get trend data for a specific hobby"""
        hobby_vertex = self.hobby_vertices.get(hobby.lower().strip())
        if not hobby_vertex:
            return []
            
        cutoff = datetime.now() - timedelta(days=days)
        return [(t, c) for t, c in hobby_vertex.trend_data if t >= cutoff]
