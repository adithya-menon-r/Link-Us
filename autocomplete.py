class TrieNode():
    def __init__(self):
        self.children = [None] * 128
        self.end_of_name = False

class Trie():
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, name):
        name = name.lower()
        curnode = self.root
        for char in name:
            char_index = ord(char)
            if not curnode.children[char_index]:
                curnode.children[char_index] = TrieNode()
            curnode = curnode.children[char_index]
        curnode.end_of_name = True

    def search(self, name):
        name = name.lower()
        curnode = self.root
        for char in name:
            char_index = ord(char)
            if not curnode.children[char_index]:
                return False
            curnode = curnode.children[char_index]
        return curnode.end_of_name and curnode
    
    def get_suggestions(self, prefix):
        prefix = prefix.lower()
        curnode = self.root
        for char in prefix:
            char_index = ord(char)
            if not curnode.children[char_index]:
                return []
            curnode = curnode.children[char_index]
        suggestions = []
        self.dfs(curnode, prefix, suggestions)
        return suggestions

    def dfs(self, node, path, suggestions):
        if node.end_of_name:
            suggestions.append(path)
        for i in range(128):
            if node.children[i] is not None:
                self.dfs(node.children[i], path + chr(i), suggestions)

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
