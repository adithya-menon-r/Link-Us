import re
from social_network import SocialNetwork
from hobby_network import HobbyNetwork
from friendRecommendation import FriendRecommender
from auto_complete import Trie

network = SocialNetwork()
hobby_network = HobbyNetwork()
recommender = FriendRecommender(network, hobby_network)
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
        
def show_post_menu(network, username):
    while True:
        print("\n==== Post Menu ====")
        print("1. Create New Post")
        print("2. View My Posts")
        print("3. View Friend Posts")
        print("4. Like/Unlike Post")
        print("5. Comment on Post")
        print("6. Back to Main Menu")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            content = input("Enter your post content: ")
            post_id = network.create_post(username, content)
            print("Post created successfully!")
            
        elif choice == "2":
            posts = network.get_user_posts(username)
            if posts:
                print("\nYour Posts:")
                for pid, post in posts:
                    print(f"\nPost ID: {pid}")
                    print(post)
                    print("Liked by:", ", ".join(post.likes) if post.likes else "No likes yet")
                    if post.comments:
                        print("\nComments:")
                        for commenter, comment, timestamp in post.comments:
                            print(f"  {commenter} ({timestamp.strftime('%Y-%m-%d %H:%M')}): {comment}")
            else:
                print("No posts yet!")
                
        elif choice == "3":
            posts = network.get_friend_posts(username)
            if posts:
                print("\nFriend Posts:")
                for pid, post in posts:
                    print(f"\nPost ID: {pid}")
                    print(post)
                    print("Liked by:", ", ".join(post.likes) if post.likes else "No likes yet")
                    if post.comments:
                        print("\nComments:")
                        for commenter, comment, timestamp in post.comments:
                            print(f"  {commenter} ({timestamp.strftime('%Y-%m-%d %H:%M')}): {comment}")
            else:
                print("No friend posts to show!")
                
        elif choice == "4":
            post_id = input("Enter Post ID: ")
            post = network.get_post(post_id)
            if post:
                print(post)
                if username in post.likes:
                    if network.unlike_post(post_id, username):
                        print("Post unliked!")
                else:
                    if network.like_post(post_id, username):
                        print("Post liked!")
            else:
                print("Post not found!")
                
        elif choice == "5":
            post_id = input("Enter Post ID: ")
            post = network.get_post(post_id)
            if post:
                print(post)
                comment = input("Enter your comment: ")
                if network.comment_on_post(post_id, username, comment):
                    print("Comment added!")
                else:
                    print("Failed to add comment!")
            else:
                print("Post not found!")
                
        elif choice == "6":
            break
        
        else:
            print("Invalid option!")

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
                print("7. Posts")
                print("8. logout")
                choice = input("Choose an option: ")
                
                if choice == "1":
                    print("\n==== Friend Recommendations ====")
                    recommendations = recommender.get_recommendations(username)
                    
                    if not recommendations:
                        print("No recommendations available at this time!")
                        print("Try adding more information to your profile or connecting with more people.")
                        continue
                        
                    print("\nHere are some people you might know:")
                    for i, (recommended_user, score) in enumerate(recommendations, 1):
                        person = network.vertices[recommended_user]
                        # Calculate common friends for display
                        common_friends = network.common_friends(username, recommended_user)
                        
                        # Format the score as a percentage
                        match_percentage = int(score * 100)
                        
                        print(f"\n{i}. {recommended_user}")
                        print(f"   Name: {person.name}")
                        print(f"   Hobbies: {', '.join(person.hobbies)}")
                        print(f"   Common Friends: {common_friends}")
                        print(f"   Match Score: {match_percentage}%")
                        
                    print("\nOptions:")
                    print("1. Send Friend Request")
                    print("2. Back to Menu")
                    
                    while True:
                        try:
                            option = input("\nChoose an option (or enter user number to send request): ")
                            
                            if option == "2":
                                break
                                
                            if option == "1":
                                user_num = input("Enter the number of the user you want to connect with: ")
                                if user_num.isdigit() and 1 <= int(user_num) <= len(recommendations):
                                    recommended_user = recommendations[int(user_num) - 1][0]
                                    if network.send_friend_request(username, recommended_user):
                                        print(f"\nFriend request sent to {recommended_user}!")
                                    else:
                                        print("\nCouldn't send friend request. They might have already received a request from you.")
                                    break
                                else:
                                    print("Invalid user number. Please try again!")
                            
                            elif option.isdigit() and 1 <= int(option) <= len(recommendations):
                                recommended_user = recommendations[int(option) - 1][0]
                                if network.send_friend_request(username, recommended_user):
                                    print(f"\nFriend request sent to {recommended_user}!")
                                else:
                                    print("\nCouldn't send friend request. They might have already received a request from you.")
                                break
                            
                            else:
                                print("Invalid option. Please try again!")
                                
                        except ValueError:
                            print("Invalid input. Please enter a number!")
                    
                elif choice == "2":
                    search_username = get_username("Enter Username to Search: ")
                    if search_username in network.vertices:
                        person = network.vertices[search_username]
                        print(f"\n==== User Profile: {search_username} ====")
                        print(f"Name: {person.name}")
                        print(f"Hobbies: {', '.join(person.hobbies)}")
                        if person.description:
                            print(f"Description: {person.description}")
                        
                        # Show connection status
                        is_friend = person in network.vertices[username].adjacency_map
                        has_pending_request = search_username in network.vertices[username].inbox
                        received_request = username in person.inbox
                        
                        if is_friend:
                            print("\nStatus: Friend ✓")
                            common_friends_count = network.common_friends(username, search_username)
                            print(f"Common Friends: {common_friends_count}")
                        else:
                            print("\nStatus: Not Connected")
                            
                        while True:
                            print("\nOptions:")
                            if is_friend:
                                print("1. View Posts")
                                print("2. Send Message")
                                print("3. Back")
                            elif received_request:
                                print("1. Accept Friend Request")
                                print("2. Back")
                            elif has_pending_request:
                                print("1. Friend Request Pending")
                                print("2. Back")
                            else:
                                print("1. Send Friend Request")
                                print("2. Back")
                            
                            sub_choice = input("Choose an option: ")
                            
                            if is_friend:
                                if sub_choice == "1":
                                    posts = network.get_user_posts(search_username)
                                    if posts:
                                        print("\nUser Posts:")
                                        for pid, post in posts:
                                            print(f"\nPost ID: {pid}")
                                            print(post)
                                            print("Liked by:", ", ".join(post.likes) if post.likes else "No likes yet")
                                            if post.comments:
                                                print("\nComments:")
                                                for commenter, comment, timestamp in post.comments:
                                                    print(f"  {commenter} ({timestamp.strftime('%Y-%m-%d %H:%M')}): {comment}")
                                    else:
                                        print("No posts to show!")
                                elif sub_choice == "2":
                                    message = input("Enter your message: ")
                                    if network.send_message(username, search_username, message):
                                        print("Message sent successfully!")
                                    else:
                                        print("Failed to send message.")
                                elif sub_choice == "3":
                                    break
                            elif received_request:
                                if sub_choice == "1":
                                    if network.accept_friend_request(username, search_username):
                                        print(f"Yay! You are now friends with {search_username}!")
                                        break
                                    else:
                                        print("Failed to accept friend request.")
                                elif sub_choice == "2":
                                    break
                            elif has_pending_request:
                                if sub_choice in {"1", "2"}:
                                    break
                            else:
                                if sub_choice == "1":
                                    if network.send_friend_request(username, search_username):
                                        print("Friend request sent successfully!")
                                        break
                                    else:
                                        print("Failed to send friend request.")
                                elif sub_choice == "2":
                                    break
                            
                            if sub_choice not in {"1", "2", "3"}:
                                print("Invalid option! Please try again.")
                    else:
                        print("User not found!")
                    
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

                elif choice=="7":
                    show_post_menu(network, username)
                
                elif choice == "8":
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
