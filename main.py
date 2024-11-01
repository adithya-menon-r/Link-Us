import re
from social_network import SocialNetwork
from auto_complete import Trie

network = SocialNetwork()
trie = Trie()

def validate_username(username):
    return re.match(r'^[A-Za-z0-9_.]+$', username)

def confirm_username(username, suggestions):
    if len(suggestions) == 1:
        if suggestions[0] != username.lower():
            confirmation = input(f"Similar username found. Did you mean {suggestions[0]}? (yes/no): ")
            if confirmation.lower() in {"y", "yes"}:
                return suggestions[0]
        return suggestions[0]
    else:
        print("Similar usernames found:")
        for i, suggestion in enumerate(suggestions, start=1):
            print(f"{i}. {suggestion}")
        print("0. Retry")
        while True:
            try:
                confirmation = int(input("Select intended username >> "))
                if confirmation == 0:
                    break
                elif 1 <= confirmation <= len(suggestions):
                    return suggestions[confirmation - 1]
                else:
                    print("Invalid option. Please try again!")
            except ValueError:
                print("Invalid option. Please enter a number!")
    return None

def get_username(input_msg):
    while True:
        username = input(input_msg)
        suggestions = trie.get_suggestions(username)
        if not suggestions:
            print("No such username found! Please try again.")
            continue
        confirmed_username = confirm_username(username, suggestions)
        if confirmed_username:
            return confirmed_username

def main():
    while True:
        print("======== LinkUs ========")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        option = input("Choose an option >> ")
        
        if option == "1":
            name = input("Enter your name: ")
            while True:
                username = input("Enter a username: ")
                if not validate_username(username):
                    print("Invalid username! Try again with only letters, numbers, underscore and period")
                    continue
                if trie.search(username):
                    print("Username already exists! Please try again.")
                    continue
                trie.insert(username)
                break
            hobbies = input("Enter hobbies (comma-separated): ").split(",")
            description = input("Enter a personal description: ")
            network.add_person(name, username, hobbies, description)
            print(f"Account for {username.lower()} created successfully!\n")
        
        elif option == "2":
            username = get_username("Enter the Username: ")
            print(f"\n==== Welcome, {username} ====")
            while True:
                print("1. Get Friend Recommendations")
                print("2. Search Users")
                print("3. View Users by Hobby")
                print("4. Inbox")
                print("5. Send Message")
                print("6. View Messages")
                print("7. Logout")
                choice = input("Choose an option: ")
                
                if choice == "1":
                    ... # TODO: To be implemented by Aashiq & Narain
                    
                elif choice == "2":
                    username = get_username("Enter Username to Search: ")
                    ... # TODO: Rest to be implemented by Karthikeyan
                
                elif choice == "3":
                    ... # TODO: To be implemented by Anurup
                    
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
                                print(f"Yay! You are now friends with {requester}!")
                            else:
                                print("Failed to Accept Friend Request.")
                    else:
                        print("No pending Friend Requests.")
                
                elif choice == "5":
                    to_user = get_username("Enter the Username of the recipient: ")
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
                    print(f"\nLogging out {username}...")
                    break
                
                else:
                    print("Invalid option. Please try again!")
        
        elif option == "3":
            print("\nThanks for using LinkUs....")
            break
        
        else:
            print("Invalid option. Please try again!")

if __name__ == "__main__":
    main()
