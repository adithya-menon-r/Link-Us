'''
NOTE:
Trie Structure: Added TrieNode and Trie classes to manage the usernames.
Insert Method: The insert method in the Trie class allows for adding usernames as accounts are created.
Search Method: The search method retrieves all usernames that match a given prefix, which can be used in the user search functionality.
Searching for Users: The search_users method utilizes the Trie to find users based on an input string.

THE TRIE THING, IM NOT SURE I'VE HAVE WHAT ADITHYA SAID
THE REOMMENDATION THING AND SEARCH USER THING HAS TO BE INCORPORATED BY ADITHYA AND AASHIQ


DATA STRUCTURES USED:
NOT STACK


Deque
others are inbuilt data structures
'''

from typing import Dict, List, Set
from dataclasses import dataclass

class DEQUE:
    def __init__(self):
        self.items = []
    
    def append(self, item):
        self.items.append(item)
    
    def popleft(self):
        if self.items:
            return self.items.pop(0)
        raise IndexError("pop from an empty deque")
    
    def remove(self, item):
        self.items.remove(item)
    
    def __len__(self):
        return len(self.items)
    
    def __iter__(self):
        return iter(self.items)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.usernames = []  # List of usernames with this prefix

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, username: str):
        node = self.root
        for char in username:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.usernames.append(username)  # Store the username for prefix suggestions
        node.is_end_of_word = True

    def search(self, prefix: str) -> List[str]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.usernames

@dataclass
class User:
    name: str
    username: str
    hobbies: Set[str]
    friends: Set[str]
    inbox: DEQUE
    messages: DEQUE

class SocialNetwork:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.usernames_set: Set[str] = set()
        self.trie = Trie()  # Initialize the Trie for username search

    def create_account(self, name: str, username: str, hobbies: List[str]) -> bool:
        username = username.lower()
        if username in self.usernames_set:
            return False
        
        user = User(
            name=name, 
            username=username, 
            hobbies=set(hobbies), 
            friends=set(),
            inbox=DEQUE(),
            messages=DEQUE()
        )
        
        self.users[username] = user
        self.usernames_set.add(username)
        self.trie.insert(username)  # Insert the username into the Trie
        return True

    def login(self, username: str) -> bool:
        return username.lower() in self.users
    
    def recommend_friends(self, username: str, limit: int = 3) -> List[str]:
        user = self.users[username.lower()]
        recommendations = []
        
        for potential_friend in self.users:
            if potential_friend in user.friends or potential_friend == username:
                continue
            
            common_hobbies = len(user.hobbies & self.users[potential_friend].hobbies)
            if common_hobbies > 0:
                recommendations.append((common_hobbies, potential_friend))
        
        recommendations.sort(reverse=True, key=lambda x: x[0])
        return [user[1] for user in recommendations[:limit]]
    
    def send_friend_request(self, from_user: str, to_user: str) -> bool:
        from_user = from_user.lower()
        to_user = to_user.lower()
        
        if to_user not in self.users or from_user == to_user or from_user in self.users[to_user].friends:
            return False
        
        if from_user not in self.users[to_user].inbox:
            self.users[to_user].inbox.append(from_user)
            return True
        return False
    
    def get_friend_requests(self, username: str) -> List[str]:
        user = self.users[username.lower()]
        return list(user.inbox)
    
    def accept_friend_request(self, username: str, requester: str) -> bool:
        user = self.users[username.lower()]
        requester = requester.lower()
        
        if requester in user.inbox:
            user.friends.add(requester)
            self.users[requester].friends.add(username)
            user.inbox.remove(requester)
            return True
        return False

    def send_message(self, from_user: str, to_user: str, message: str) -> bool:
        from_user = from_user.lower()
        to_user = to_user.lower()
        
        if to_user in self.users and from_user in self.users[to_user].friends:
            self.users[to_user].messages.append((from_user, message))
            return True
        return False

    def get_messages(self, username: str) -> List[str]:
        user = self.users[username.lower()]
        return [f"From {msg[0]}: {msg[1]}" for msg in user.messages]

    def search_users(self, username_input: str) -> List[str]:
        suggestions = self.trie.search(username_input.lower())
        if len(suggestions) == 1:
            return suggestions
        return suggestions  


def main():
    network = SocialNetwork()
    print("=== Social Network ===")
    while True:
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        option = input("Choose an option: ")
        
        if option == "1":
            name = input("Enter your name: ")
            username = input("Enter a username: ")
            hobbies = input("Enter hobbies (comma-separated): ").split(",")
            if network.create_account(name, username, hobbies):
                print("Account created successfully!")
            else:
                print("Username already exists. Please try a different one.")
        
        elif option == "2":
            username = input("Enter username: ")
            if network.login(username):
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
                        username_input = input("Enter username to search: ")
                        suggestions = network.search_users(username_input)
                        if len(suggestions) == 1:
                            print(f"User found: {suggestions[0]}")
                        elif len(suggestions) > 1:
                            print("Users found:")
                            for i, user in enumerate(suggestions, start=1):
                                print(f"{i}. {user}")
                            selected = input("Enter the number to select a user or 0 to skip: ")
                            if selected.isdigit() and 1 <= int(selected) <= len(suggestions):
                                selected_user = suggestions[int(selected) - 1]
                                print(f"Selected User: {selected_user}")
                        else:
                            print("No users found.")
                    
                    elif choice == "3":
                        # Not implemented in the original code
                        print("This feature is not implemented yet.")
                    
                    elif choice == "4":
                        print("Pending friend requests:")
                        friend_requests = network.get_friend_requests(username)
                        if friend_requests:
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

