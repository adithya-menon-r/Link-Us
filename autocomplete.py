class TrieNode:
    def __init__(self):
        # Each TrieNode has an array of 128 children, a child for every Standard ASCII character (0-127)
        self.children = [None] * 128 
        self.end_of_name = False # Denotes whether the char is the last char in the stored name

class Trie:
    def __init__(self):
        self.root = TrieNode() # Trie is always initialised with an empty root node
    
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
        name = name.lower() # Makes insertion case-insensitive
        current = self.root
        for char in name: # Iterating and processing each char in the name
            char_index = ord(char) # Using ASCII value of the char as index - makes storing an O(1) operation
            # If there is no node at that char_index, then a TrieNode is created
            if not current.children[char_index]: 
                current.children[char_index] = TrieNode()
            current = current.children[char_index]
        current.end_of_name = True # end_of_name flag is set to True to know when we reach the end of a name

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
        name = name.lower() # Since all insertions are in lowercase, the search string must be converted to lowercase
        current = self.root
        for char in name:
            char_index = ord(char) # Using ASCII value of the char as index - makes searching an O(1) operation
            # returns False if there is no node at one of char indices - name doesn't exist
            if not current.children[char_index]:
                return False
            current = current.children[char_index]
        # Returns True if the end of name is reached and the current is not None, indicating a complete match
        return current.end_of_name and current 
    
    """
    (method) def get_suggestions(
        self: Self@Trie,
        prefix: str
    ) -> list
    """
    def get_suggestions(self, prefix):
        """
        Gets a list of names (suggestions) that start with the given prefix

        Time Complexity - O(L + m) where L is the number of characters in ths prefix and m is the number of nodes in the subtree
        Justification - Method iterates through each char of the prefix to check if the prefix exists and performs DFS to get sugegstions
        """
        prefix = prefix.lower() # Since all insertions are in lowercase, the search string must be converted to lowercase
        current = self.root
        for char in prefix:
            char_index = ord(char)
            if not current.children[char_index]:
                return [] # Returns an empty list when we encounter a char with no node (no such prefix)
            current = current.children[char_index]
        # Perform a DFS from the end of the prefix to collect all possible name matches (suggestions)
        suggestions = []
        self._depth_first_search(current, prefix, suggestions)
        return suggestions

    """
    (method) def depth_first_search(
        self: Self@Trie,
        node: TrieNode,
        result: str,
        suggestions: list
    ) -> None
    """
    def _depth_first_search(self, node, result, suggestions):
        """
        Performs a depth-first search from the given node to find all names with the current prefix

        Time complexity - O(m) where m is the number of nodes in the subtree rooted at the given node
        Justification - We are traversing through all the nodes of the subtree, to find all stored names with that prefix
        """
        # Adds the name to suggestion when we reach the node denoting end of the name
        if node.end_of_name:
            suggestions.append(result) 
        for i in range(128):
            if node.children[i] is not None:
                # Recursively calls the method for every non-null child
                self.depth_first_search(node.children[i], result + chr(i), suggestions) 

def main():
    trie = Trie()
    names = ["NARAIN", "Adithya", "Aditi", "Karthik", "Karthikeya", "Karthikeyan", "ADITHYA", "Aashiq", "Aashiqi", "Anurup", "Varun_Hirthik", "Varun_Raj"]
    for name in names:
        if not trie.search(name):
            trie.insert(name)
            print(f"{name} Added")
        else:
            print(f"{name} Exists")
    suggestions = trie.get_suggestions("Varun")
    if suggestions:
        print(f"Suggestions - {suggestions}")
    else:
        print("No Suggestions")
    
if __name__ == "__main__":
    main()
