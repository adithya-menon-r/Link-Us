# LinkUs

## About
LinkUs is a Python-based Social Networking System that enables users to connect based on shared hobbies and mutual connections. 
It offers functionalities such as user registration, hobby management and friend recommendations based on different criteria.
It also features a post and messaging system to facilitate interaction among users.

LinkUs was created as a project for the **23CSE203 (Data Structures & Algorithms)** course.

## Installation
1. Download the `Source Code` or Clone the repository:

   ```bash
   git clone https://github.com/adithya-menon-r/Link-Us.git
   cd Link-Us
   ```

2. Ensure you are using `Python 3.x` and have all the custom modules in the same directory
   
3. To start the program, run the following command:

    ```bash
    python main.py
    ```

## Project Structure
```
Link-Us/
 |── main.py                     # Main entry point to the program
 |── social_network.py           # Social Network Graph implementation
 ├── hobby_network.py            # Hobby Network Graph implementation
 ├── friend_recommendation.py    # Friend recommendation algorithm
 |── auto_complete.py            # Trie implementation for username suggestions
 └── post_system.py              # Post Class storing all post data
```
`max_heap.py` and `hash_map.py` are custom implementations of the Max Heap and Hash Map data structures, used to optimize operations like friend recommendations and fast lookups in the program.

## Core Features 
### User Management & Social Network
- The program enables users to create accounts and connect with others, forming a dynamic social network. During account creation, users can input their name, username, hobbies and description. Users can connect with others through friend requests. Each user has an inbox, implemented using a deque, to manage and store pending requests. Other key features include a messaging system for communication between friends and the ability to create and interact with posts.

### Autocomplete & User Suggestions
- This key feature leverages the Trie data structure and enhances user experience during tasks like searching for friends or creating a new account. It provides prefix-based autocomplete suggestions, enabling users to quickly find usernames by typing only a partial match. The feature supports case-insensitive username matching. Additionally, when creating new accounts, it helps prevent the duplication of usernames.

### Friend Recommendation System
- The Friend Recommendation System generates friend recommendations by assigning scores based on multiple factors: popularity, friends of friends (FoF), mutual friends, and hobby similarity. Popularity is derived from a user's friend count and post engagement, while FoF counts mutual connections, and hobby similarity is calculated using the Jaccard index.
- These factors are weighted (FoF: 30%, mutual friends: 25%, hobby similarity: 25%, popularity: 20%) and combined into a final score. The recommendations are ranked using a Priority Queue (Max Heap), ensuring the best matches are selected. The system also caches popularity scores for efficiency.

### Hobby Network
- A graph-based system connecting users and hobbies is implemented. It efficiently manages relationships, tracks hobby trends, and prioritizes popular hobbies using a MaxHeap. The feature caches trend data using a deque, creates hobby connections dynamically, and uses a ChainHashMap for efficient hobby mapping, ensuring fast lookups and updates.

### Post System
- The post system allows users to share posts and engage with content within their connected network. Users can interact with their friends' posts by liking them and adding comments. 

### Messaging Services
- The messaging service allows users to send messages to friends, enhancing interaction within the social network. Messages sent and received are stored in a Deque, allowing efficient management of message order, within each user's messages collection. Messages can only be sent if the users are connected as friends in the network.

## Non-Linear Data Structures Used
### Graph
- The Graph data structure is used in `social_network.py` and `hobby_network.py`. In the Social Network, the graph models user connections, where each user is represented as a node, and friendships between users are represented as edges. This structure allows for efficient traversal of user connections. 
- In the Hobby Network, the graph is used to represent hobbies as nodes. Each user is connected to the hobby nodes they are interested in, making it easy to track and manage user hobbies. 

### Trie
- The Trie data structure is employed in `auto_complete.py` to efficiently store and retrieve usernames. Its primary purpose is to enable prefix-based search functionality for autocomplete. It also generates username suggestions by performing a Depth First Search (DFS) from the last character of the prefix to get potential matches. When creating new accounts, username duplication is prevented by checking if the username is already stored in the Trie. 

### Priority Queue (Max Heap)
- A Priority Queue implemented as a Max Heap is used in both `friend_recommendation.py` and `hobby_network.py`. In the Friend Recommendation System, the Max Heap ranks friends based on various factors like mutual friends, popularity, and hobby similarity, ensuring that the best potential friends are recommended first. 
- In the Hobby Network, the Max Heap helps prioritize the most popular hobbies, ensuring that the trending hobbies are always easily accessible. 

### Hash Map
- The Hash Map is used in both `social_network.py`(For Posts) and `hobby_network.py`. In the Post System, it is used to store and retrieve post details efficiently, mapping each post object to a post ID and each username to a list of post IDs (posts created by that user). This allows for quick access to posts when users interact with content. 
- In the Hobby Network, the Hash Map is used to map hobbies to users, enabling fast lookups and updates for managing hobby relationships and tracking hobby trends within the system.

## Conclusion
The Link-Us project effectively utilizes non-linear data structures like graphs, tries, priority queues (Max Heap), and hash maps to build a dynamic social network. These data structures enable features such as friend recommendations, hobby tracking, and user interactions through posts and messages. The project showcases how well-applied data structures can enhance the functionality and performance of a social platform.

## License
This project is licensed under the [MIT LICENSE](LICENSE).

## Team behind LinkUs
- [Adithya Menon R](https://www.linkedin.com/in/adithya-menon-r)
- [PG Karthikeyan](https://www.linkedin.com/in/karthikeyan-pg-95a5b6291)
- [Varun Raj V](https://www.linkedin.com/in/varunraj2005)
- [Anurup R Krishnan](https://www.linkedin.com/in/anurup-r-krishnan-9877b1289)
- [Edavalapati Aashiq](https://www.linkedin.com/in/aashiq-edavalapati-77b346289)
- [Narain BK](https://www.linkedin.com/in/narain-bk)
