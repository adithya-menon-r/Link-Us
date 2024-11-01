class TrieNode:
    def __init__(self):
        self.children = {}  # Stores node for each char/child (more space efficient than fixed array implementation)
        self.end_of_name = False  # Denotes whether the char is the last char in the stored name

class Trie:
    def __init__(self):
        self.root = TrieNode()  # Trie is always initialised with an empty root node
    
    """
    (method) def insert(
        self: Self@Trie,
        name: str
    ) -> None
    """
    def insert(self, name):
        """
        Inserts a name into the Trie

        Time Complexity - O(L) where L is the length of the name
        Justification - Method iterates through and processes each char once in the name to be inserted
        """ 
        name = name.lower()  # Makes insertion case-insensitive
        current = self.root
        for char in name:  # Iterating and processing each char in the name
            # If the char isn't stored as a child, then the char and a TrieNode are inserted into the dict
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.end_of_name = True  # end_of_name flag is set to True to know when we reach the end of a name

    """
    (method) def search(
        self: Self@Trie,
        name: str
    ) -> bool
    """
    def search(self, name):
        """
        Searches for a name and returns if the name exists in the Trie

        Time Complexity - O(L) where L is the length of the name
        Justification - Method iterates through and processes each char once in the name to be searched
        """
        name = name.lower()  # Since all insertions are in lowercase, the search string must be converted to lowercase
        current = self.root
        for char in name:
            # Returns False if there is char isn't in the dict (is not a child) - name doesn't exist
            if char not in current.children:
                return False
            current = current.children[char]
        # Returns True if the char with end_of_name True is reached, indicating a complete match
        return current.end_of_name
    
    """
    (method) def get_suggestions(
        self: Self@Trie,
        prefix: str
    ) -> list
    """
    def get_suggestions(self, prefix):
        """
        Gets a list of names (suggestions) that start with the given prefix

        Time Complexity - O(L + m) where L is the number of characters in the prefix and m is the number of nodes in the subtree
        Justification - Method iterates through each char of the prefix to check if the prefix exists and performs DFS from the last char to get suggestions
        """
        prefix = prefix.lower()  # Since all insertions are in lowercase, the search string must be converted to lowercase
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []  # Returns an empty list when we encounter a char that isn't a child (when no such prefix stored)
            current = current.children[char]
        # Perform a DFS from the end of the prefix to collect all possible name matches (suggestions)
        suggestions = []
        self.depth_first_search(current, prefix, suggestions)
        return suggestions

    """
    (method) def depth_first_search(
        self: Self@Trie,
        node: TrieNode,
        result: str,
        suggestions: list
    ) -> None
    """
    def depth_first_search(self, node, result, suggestions):
        """
        Performs a depth-first search from the given node to find all names with the current prefix

        Time complexity - O(m) where m is the number of nodes in the subtree rooted at the given node
        Justification - We are traversing through all the nodes of the subtree one by one, to find all stored names with that prefix
        """
        # Adds the name to suggestion when we reach a node denoting end of the name
        if node.end_of_name:
            suggestions.append(result) 
        for char, child_node in node.children.items():
            # Recursively calls the method for every child stored in dict
            self.depth_first_search(child_node, result + char, suggestions) 

def main():
    trie = Trie()

    names = ["NARAIN", "Adithya", "Aditi", "Karthik", "Karthikeya", "Karthikeyan", "ADITHYA", "Aashiq", "Aashiqi", "Anurup", "Varun Hirthik", "Varun_Raj"]
    print("Inserting names...")
    for name in names:
        if not trie.search(name):
            trie.insert(name)
            print(f"{name} Added")
        else:
            print(f"{name} already Exists!")

    print("\nSearching for names...")
    search_names = ["Adithya", "NARAIN", "Karthik", "Varun", "Karthikeya", "Ishaan"]
    for name in search_names:
        exists = trie.search(name)
        print(f"Search '{name}': {'Found' if exists else 'Not Found'}")
    
    print("\nGetting suggestions...")
    prefixes = ["Karthi", "Varun", "A", "Nar", "XYZ"]
    for prefix in prefixes:
        suggestions = trie.get_suggestions(prefix)
        print(f"Suggestions for '{prefix}': {suggestions if suggestions else 'No Suggestions'}")

if __name__ == "__main__":
    main()
