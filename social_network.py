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
            if potential_friend_name == name or potential_friend_name in person.adjacency_map:
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
        user = self.vertices[username]
        return list(user.messages)

    def get_friend_requests(self, username):
        return list(self.vertices[username].inbox)
