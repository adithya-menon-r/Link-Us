'''
NOTE:
your part can be integrated or incorporated with the code or replace it


Trie Structure: Added TrieNode and Trie classes to manage the usernames.
Insert Method: The insert method in the Trie class allows for adding usernames as accounts are created.
Search Method: The search method retrieves all usernames that match a given prefix, which can be used in the user search functionality.
Searching for Users: The search_users method utilizes the Trie to find users based on an input string.

THE TRIE THING, IM NOT SURE I'VE HAVE WHAT ADITHYA SAID
THE REOMMENDATION THING AND SEARCH USER THING HAS TO BE INCORPORATED BYND AASHIQ


DATA STRUCTURES USED:
NOT STACK


Deque
others are inbuilt data structures
'''
from typing import Dict, List, Set
from dataclasses import dataclass

class Vertex:
    def __init__(self, name, hobbies, description=None):
        self.name = name
        self.hobbies = set(hobbies)
        self.description = description
        self.adjacency_map = dict()
        self.inbox = []
        self.messages = []

class Edge:
    def __init__(self, vertex1, vertex2):
        self.vertex1 = vertex1
        self.vertex2 = vertex2

class Graph:
    def __init__(self):
        self.vertices = dict()

    def add_person(self, name, hobbies, description=None):
        if name not in self.vertices:
            person = Vertex(name, hobbies, description)
            self.vertices[name] = person
            return True
        return False

    def make_connections(self, name1, name2):
        person1 = self.vertices[name1]
        person2 = self.vertices[name2]
        connection = Edge(person1, person2)
        person1.adjacency_map[person2.name] = connection
        person2.adjacency_map[person1.name] = connection

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

    def common_friends(self, name1, name2):
        person1 = self.vertices[name1]
        person2 = self.vertices[name2]
        return len(set(person1.adjacency_map) & set(person2.adjacency_map))

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
        return user.messages

    def get_friend_requests(self, username):
        return self.vertices[username].inbox

def main():
    network = Graph()
    print("=== Social Network ===")
    while True:
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        option = input("Choose an option: ")
        
        if option == "1":
            name = input("Enter your name: ")
            hobbies = input("Enter hobbies (comma-separated): ").split(",")
            if network.add_person(name, hobbies):
                print("Account created successfully!")
            else:
                print("Username already exists. Please try a different one.")
        
        elif option == "2":
            username = input("Enter username: ")
            if username in network.vertices:
                print(f"\n=== Welcome, {username} ===")
                while True:
                    print("1. Recommend Friends")
                    print("2. Search Users")
                    print("3. View Users by Hobby")
                    print("4. Inbox")
                    print("5. Send Message")
                    print("6. View Messages")
                    print("7. Logout")
                    choice = input("Choose an option: ")
                    
                    if choice == "1":
                        recommendations = network.recommend_friends(username)
                        if recommendations:
                            print("Friend Recommendations:")
                            for rec in recommendations:
                                print(rec)
                        else:
                            print("No recommendations available.")
                    
                    elif choice == "2":
                        # Searching functionality can be integrated using other data structures like a Trie
                        print("This feature is not implemented yet.")
                    
                    elif choice == "3":
                        print("This feature is not implemented yet.")
                    
                    elif choice == "4":
                        friend_requests = network.get_friend_requests(username)
                        if friend_requests:
                            print("Pending friend requests:")
                            for i, requester in enumerate(friend_requests, start=1):
                                print(f"{i}. {requester}")
                            selected = input("Enter number to accept request (or 0 to skip): ")
                            if selected.isdigit() and 1 <= int(selected) <= len(friend_requests):
                                requester = friend_requests[int(selected) - 1]
                                if network.accept_friend_request(username, requester):
                                    print(f"You are now friends with {requester}!")
                                else:
                                    print("Failed to accept friend request.")
                        else:
                            print("No pending friend requests.")
                    
                    elif choice == "5":
                        to_user = input("Enter the username of the recipient: ")
                        message = input("Enter your message: ")
                        if network.send_message(username, to_user, message):
                            print("Message sent successfully!")
                        else:
                            print("Failed to send message. Check if the user is your friend.")
                    
                    elif choice == "6":
                        messages = network.get_messages(username)
                        if messages:
                            print("Your Messages:")
                            for msg in messages:
                                print(msg)
                        else:
                            print("No messages found.")
                    
                    elif choice == "7":
                        print(f"Logging out {username}.")
                        break
                    
                    else:
                        print("Invalid option. Please try again.")
            else:
                print("Login failed. Username not found.")
        
        elif option == "3":
            print("Exiting the social network.")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
