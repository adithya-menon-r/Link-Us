from collections import deque
from datetime import datetime, timedelta
from typing import List, Set, Tuple, Dict
from max_heap import MaxHeap  # MaxHeap used for prioritizing top counts
from hash_map import ChainHashMap  # ChainHashMap chosen for efficient key-value mapping

class HobbyVertex:
    """Node representing a hobby in the hobby graph"""
    def __init__(self, hobby_name: str):
        self.hobby_name = hobby_name
        self.users = set()  # Set of usernames
        self.connections = ChainHashMap()  # Map to store related hobbies and their weights
        self.trend_data = deque(maxlen=100)  # Limited to last 100 entries
        self.update_trend_data()  # Logs the current trend data

    def update_trend_data(self) -> None:
        """
        Add current timestamp and user count to trend data
        Time Complexity: O(1) - appending to the deque is constant time.
        """
        self.trend_data.append((datetime.now(), len(self.users)))

    def add_connection(self, other_hobby: str) -> None:
        """
        Increment connection weight with another hobby
        Time Complexity: O(1) - ChainHashMap provides average O(1) access and update time
        """
        current_weight = self.connections.get(other_hobby) or 0
        self.connections.put(other_hobby, current_weight + 1)

class UserVertex:
    """Node representing a user in the hobby graph"""
    def __init__(self, username: str):
        self.username = username # Initialize a user vertex with the username
        self.hobbies = set()  # Set of hobby names

class HobbyNetwork:
    """Graph-based implementation of hobby relationships"""
    def __init__(self):
        # Dictionary mappings for hobby vertices and user vertices
        self.hobby_vertices: Dict[str, HobbyVertex] = {}
        self.user_vertices: Dict[str, UserVertex] = {}

    def _normalize_hobby(self, hobby: str) -> str:
        """Normalize hobby name for consistent storage"""
        return hobby.lower().strip()

    def add_hobby(self, hobby_name: str) -> HobbyVertex:
        """
        Add a new hobby or return existing one
        Time Complexity: O(n) - where n is the length of the string (strip and lower)
        """
        hobby = self._normalize_hobby(hobby_name)
        if not hobby:
            raise ValueError("Hobby name cannot be empty")
            
        if hobby not in self.hobby_vertices:
            self.hobby_vertices[hobby] = HobbyVertex(hobby)
            
        return self.hobby_vertices[hobby]

    def add_user(self, username: str) -> UserVertex:
        """
        Add a new user or return existing one
        Time Complexity: O(1) on average, dictionary lookup and insertion are O(1).
        """
        if not username:
            raise ValueError("Username cannot be empty")
            
        if username not in self.user_vertices:
            self.user_vertices[username] = UserVertex(username)
            
        return self.user_vertices[username]

    def add_user_hobby(self, username: str, hobby_name: str) -> None:
        """
        Connect a user to a hobby and update relationships
        Time Complexity: O(k) for each user hobby, where k is the number of user's hobbies.
        """
        if not username or not hobby_name:
            raise ValueError("Username and hobby name must not be empty")

        hobby = self._normalize_hobby(hobby_name)
        
        # Get or create vertices
        hobby_vertex = self.add_hobby(hobby)
        user_vertex = self.add_user(username)

        # Skip if connection already exists
        if hobby in user_vertex.hobbies:
            return

        # Create new connections
        hobby_vertex.users.add(username)
        user_vertex.hobbies.add(hobby)
        
        # Update trend data
        hobby_vertex.update_trend_data()

        # Update hobby connections
        for existing_hobby in user_vertex.hobbies:
            if existing_hobby != hobby:
                self.hobby_vertices[hobby].add_connection(existing_hobby)
                self.hobby_vertices[existing_hobby].add_connection(hobby)

    def add_user_hobbies(self, username: str, hobbies: List[str]) -> None:
        """
        Add multiple hobbies for a user
        Time Complexity: O(m*k) where m is the number of hobbies and k is time per hobby addition.
        """
        if not username:
            raise ValueError("Username cannot be empty")
        
        for hobby in hobbies:
            if hobby:  # Skip empty hobby names
                self.add_user_hobby(username, hobby)

    def get_hobby_counts(self) -> Dict[str, int]:
        """
        Get all hobbies and their user counts
        Time Complexity: O(h) where h is the number of hobbies.
        """
        return {
            hobby: len(vertex.users)
            for hobby, vertex in self.hobby_vertices.items()
        }

    def get_top_hobbies(self, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Get most popular hobbies
        Time Complexity: O(h*log(l)), with h as hobbies count, l as limit.
        """
        heap = MaxHeap()
        for hobby, vertex in self.hobby_vertices.items():
            heap.insert((len(vertex.users), hobby))

        result = []
        while len(result) < limit and not heap.is_empty():
            count, hobby = heap.extract_max()
            result.append((hobby, count))

        return result

    def get_users_with_most_hobbies(self, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Get users with the most hobbies
        Time Complexity: O(h*log(l)), where h is users count and l is limit.
        """
        heap = MaxHeap()
        for username, vertex in self.user_vertices.items():
            heap.insert((len(vertex.hobbies), username))

        result = []
        while len(result) < limit and not heap.is_empty():
            count, username = heap.extract_max()
            result.append((username, count))

        return result

    def get_hobby_trends(self, days: int = 30) -> Dict[str, List[Tuple[datetime, int]]]:
        """
        Get trend data for all hobbies
        Time Complexity: O(h*t) where h is the number of hobbies, t is trend data length.
        """
        cutoff = datetime.now() - timedelta(days=days)
        return {
            hobby: [(t, c) for t, c in vertex.trend_data if t >= cutoff]
            for hobby, vertex in self.hobby_vertices.items()
        }

    def get_users_by_hobby(self, hobby: str) -> Set[str]:
        """
        Get all users who have a specific hobby
        Time Complexity: O(1) average, dictionary access and set copy.
        """
        hobby = self._normalize_hobby(hobby)
        vertex = self.hobby_vertices.get(hobby)
        return vertex.users.copy() if vertex else set()
