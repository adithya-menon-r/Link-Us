from random import randrange

"""
Preamble:
    This Class represents an entry(key-value pair) in a hash map.
    The Entry class provides basic functionality for comparing and hashing
    entries based on their keys.
    
    Class Signature:
    class Entry(k: Any, v: Any)
    
    Parameters:
    -> k: Key of any hashable type
    -> v: Value of any type
    
    Methods:
    1) def __eq__(self, other) -> bool
    Compares two entries for equality based on their keys.
    
    2) def __hash__(self) -> int
    Returns hash value of the entry's key.
"""
class Entry:

    #Constructor initialises Entry with key k and value v.
    def __init__(self, k, v):
        self._key = k
        self._value = v
    
    """ 
    Compares two entries based on their keys.
    This func is called when the '==' operator is encountered.
    Time Complexity: O(1)
    """
    def __eq__(self, other):
        if isinstance(other, Entry):
            #"self" is the instance on left side
            #"other" is the instance on right side 
            return self._key == other._key
        return False
    
    """ 
    This function returns hash value of an entry.
    Time Complexity: O(1)
    """
    def __hash__(self):
        return hash(self._key)

"""
Preamble:
    This Class implements a hashmap using an unordered list.
    It contains basic hashmap operations with linear time complexity.
    
    Class Signature:
    class UnsortedTableMap()
    
    Methods:
    1) def get(self, k) -> Any
    Returns value associated with key k.
    
    2) def put(self, k, v) -> None
    Inserts or updates entry with key k and value v.
    
    3) def remove(self, k) -> Any
    Removes and returns value associated with key k.

    4) def __contains__(self, key) -> bool
    This method checks if a given key exists in the hashmap.
    
    5) def __len__(self) -> int
    This method returns number of entries in the hashmap.

    6) def items()/keys()/values() -> list
    Returns list of all items/keys/values in the hashmap.
"""
class UnsortedTableMap:

    #Constructor initialises an empty hashmap 
    def __init__(self):
        self._table = []
        
    """ 
    This function returns value for given key.
    Time Comeplexity: O(n)
    """   
    def get(self, k):
        for item in self._table:
            if k == item._key:
                return item._value
        raise KeyError('Key Error: ' + repr(k))
        
    """ 
    This function inserts or updates key-value pair (k:v).
    Time Complexity: O(n)
    """
    def put(self, k, v):
        for item in self._table:
            if k == item._key:
                item._value = v
                return
        self._table.append(Entry(k, v))
    
    """ 
    This function removes an entry for a given key and returns its value.
    Time Complexity: O(n)
    """
    def remove(self, k):
        for j in range(len(self._table)):
            if k == self._table[j]._key:
                return self._table.pop(j)._value
        raise KeyError('Key Error: ' + repr(k))
    
    """
    This function checks if a given key exists in hashmap.
    Time Complexity: O(n)
    """
    def __contains__(self, k):
        try:
            self.get(k)
            return True
        except KeyError:
            return False
    
    """
    Function to get number of entries in map .
    Time Complexity: O(1)
    """
    def __len__(self):
        return len(self._table)
        
    """ 
    Function to get list of all key-value pairs.
    Time Complexity: O(n)
    """       
    def items(self):
        return [(item._key, item._value) for item in self._table]
    
    """
    Function to get list of all keys.
    Time Complexity: O(n)
    """
    def keys(self):
        return [item._key for item in self._table]
    
    """ 
    Function to get list of all values.
    Time Complexity: O(n)
    """
    def values(self):
        return [item._value for item in self._table]

"""
Preamble:
    This Class implements a hashmap using separate chaining for collision resolution,
    using MAD (Multiply-Add-Divide) compression for hash function and to dynamically
    resize when load factor exceeds threshold.
    
    Class Signature:
    class ChainHashMap(cap: int = 11, p: int = 109345121)
    
    Parameters:
    -> cap: Initial capacity of the hash table
    -> p: Prime number for MAD compression
    
    Methods:
    1) def _hash_function(self, k) -> int
    This method computes hash value using MAD compression.
    
    2) def get(self, key) -> Any
    This method retrieves value associated with given key.

    3) def put(self, key) -> None
    This method inserts or updates key-value pair.
    
    4) def remove(self, key) -> Any
    This method removes and returns value associated with the given key.
    
    5) def update(self, key, update_func) -> bool
    This method updates value of given key using provided function(update_func).
    
    6) def _resize(self, c) -> None
    This method resizes the bucket array to capacity c

    7) def __contains__(self, key) -> bool
    This method checks if a given key exists in the hashmap.

    8) def items()/keys()/values() -> list
    Returns list of all items/keys/values in the hashmap.

    9) def __len__(self) -> int
    This method returns number of entries in the hashmap.

    10) def clear(self) -> None
    This method removes all entries from the hashmap.
    """
class ChainHashMap:
    
    #Constructor initialises an empty hashmap with given capacity
    def __init__(self, cap=11, p=109345121):
        self._table = cap * [None]  # empty bucket array
        self._n = 0                 # number of entries
        self._prime = p             # prime no for MAD compression
        self._scale = 1 + randrange(p-1)    # scale factor
        self._shift = randrange(p)          # shift factor       
        self._load_factor_threshold = 0.5   # load factor threshold
    
    """ 
    This function returns the hash value of a key using MAD compression method.
    Time Complexity: O(1)
    """
    def _hash_function(self, k):
        return (hash(k) * self._scale + self._shift) % self._prime % len(self._table)
    
    """ 
    This function returns value for given key.
    Time Complexity: O(1)
    """
    def get(self, key):
        """Retrieve value associated with key"""
        j = self._hash_function(key)
        bucket = self._table[j]
        if bucket is None:
            return None
        try:
            return bucket.get(key)
        except KeyError:
            return None

    """ This function inserts or updates key-value pair
        and increases overall map size if load factor exceeds threshold 
        and resizes the bucket array if it exceeds capacity.
        Time Complexity: O(1)"""
    def put(self, key, value):
        """Insert or update key-value pair"""
        j = self._hash_function(key)
        if self._table[j] is None:
            self._table[j] = UnsortedTableMap()
        
        oldsize = len(self._table[j])
        self._table[j].put(key, value)
        
        if len(self._table[j]) > oldsize:  # key was new
            self._n += 1  # increase overall map size
            # resize if load factor exceeds threshold
            if self._n > len(self._table) * self._load_factor_threshold:
                self._resize(2 * len(self._table) - 1)
    
    """Updates a value using a function that takes the old value and returns a new one.
        Time Complexity: O(1)"""
    def update(self, key, update_func):
        j = self._hash_function(key)
        bucket = self._table[j]
        if bucket is not None:
            try:
                old_value = bucket.get(key)
                new_value = update_func(old_value)
                bucket.put(key, new_value)
                return True
            except KeyError:
                return False
        return False

    """Remove item associated with key.
    Time Complexity: O(1)"""             
    def remove(self, key):
        j = self._hash_function(key)
        bucket = self._table[j]
        if bucket is None:
            return None
        try:
            value = bucket.remove(key)
            self._n -= 1
            return value
        except KeyError:
            return None

    """Resize bucket array to capacity c.
    Time Complexity: O(n)"""        
    def _resize(self, c):
        old = []
        for bucket in self._table:
            if bucket is not None:
                old.extend(bucket.items())
        self._table = c * [None]
        self._n = 0
        for (k, v) in old:
            self.put(k, v)
    
    """Support for the 'in' operator.
    Time Complexity: O(1)"""
    def __contains__(self, key):
        j = self._hash_function(key)
        bucket = self._table[j]
        return bucket is not None and key in bucket
    
    """Return a list of all (key, value) pairs in the map.
    Time Complexity: O(n)"""
    def items(self):
        result = []
        for bucket in self._table:
            if bucket is not None:
                result.extend(bucket.items())
        return result
    
    """Return a list of all keys in the map.
    Time Complexity: O(n)"""
    def keys(self):
        result = []
        for bucket in self._table:
            if bucket is not None:
                result.extend(bucket.keys())
        return result
    
    """Return a list of all values in the map.
    Time Complexity: O(n)"""
    def values(self):
        result = []
        for bucket in self._table:
            if bucket is not None:
                result.extend(bucket.values())
        return result

    """ 
    This function returns number of entries in the map.
    Time Complexity: O(1)
    """        
    def __len__(self):
        return self._n
    
    """
    This function clears the map. It resets it to initial empty state.
    Time Complexity: O(n)
    """
    def clear(self):
        self._table = len(self._table) * [None]
        self._n = 0
