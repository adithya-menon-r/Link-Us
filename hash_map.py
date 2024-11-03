from random import randrange

class Entry:
    """A key-value pair entry for the hash map"""
    __slots__ = '_key', '_value'
    
    def __init__(self, k, v):
        self._key = k
        self._value = v
    
    def __eq__(self, other):
        if isinstance(other, Entry):
            return self._key == other._key
        return False
    
    def __hash__(self):
        return hash(self._key)

class UnsortedTableMap:
    """Map implementation using an unordered list."""
    
    def __init__(self):
        self._table = []
        
    def get(self, k):
        for item in self._table:
            if k == item._key:
                return item._value
        raise KeyError('Key Error: ' + repr(k))
        
    def put(self, k, v):
        for item in self._table:
            if k == item._key:
                item._value = v
                return
        self._table.append(Entry(k, v))
        
    def remove(self, k):
        for j in range(len(self._table)):
            if k == self._table[j]._key:
                return self._table.pop(j)._value
        raise KeyError('Key Error: ' + repr(k))
    
    def __contains__(self, k):
        try:
            self.get(k)
            return True
        except KeyError:
            return False
        
    def __len__(self):
        return len(self._table)
        
    def items(self):
        return [(item._key, item._value) for item in self._table]
    
    def keys(self):
        return [item._key for item in self._table]
    
    def values(self):
        return [item._value for item in self._table]

class ChainHashMap:
    """Hash map implemented with separate chaining for collision resolution."""
    
    def __init__(self, cap=11, p=109345121):
        self._table = cap * [None]  # bucket array
        self._n = 0                 # number of entries
        self._prime = p             # prime for MAD compression
        self._scale = 1 + randrange(p-1)
        self._shift = randrange(p)
        self._load_factor_threshold = 0.5
        
    def _hash_function(self, k):
        return (hash(k) * self._scale + self._shift) % self._prime % len(self._table)
        
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
    
    def update(self, key, update_func):
        """Update a value using a function that takes the old value and returns a new one"""
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
                
    def remove(self, key):
        """Remove item associated with key"""
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
            
    def _resize(self, c):
        """Resize bucket array to capacity c"""
        old = []
        for bucket in self._table:
            if bucket is not None:
                old.extend(bucket.items())
        self._table = c * [None]
        self._n = 0
        for (k, v) in old:
            self.put(k, v)
    
    def __contains__(self, key):
        """Support for 'in' operator"""
        j = self._hash_function(key)
        bucket = self._table[j]
        return bucket is not None and key in bucket
    
    def items(self):
        """Return a list of all (key, value) pairs in the map"""
        result = []
        for bucket in self._table:
            if bucket is not None:
                result.extend(bucket.items())
        return result
    
    def keys(self):
        """Return a list of all keys in the map"""
        result = []
        for bucket in self._table:
            if bucket is not None:
                result.extend(bucket.keys())
        return result
    
    def values(self):
        """Return a list of all values in the map"""
        result = []
        for bucket in self._table:
            if bucket is not None:
                result.extend(bucket.values())
        return result
            
    def __len__(self):
        return self._n
    
    def clear(self):
        """Remove all items from the map"""
        self._table = len(self._table) * [None]
        self._n = 0
