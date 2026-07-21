# Advanced Hashing Techniques

## 1. Custom Hashing Techniques

```python
from collections import defaultdict

class CustomHash:
    """Custom hash function for specific use cases"""
    
    @staticmethod
    def hash_tuple(pair):
        """Hash a pair/tuple for graph problems"""
        return hash((pair[0], pair[1]))
    
    @staticmethod
    def hash_point(point):
        """Hash a 2D point"""
        return hash((point[0], point[1]))
    
    @staticmethod
    def hash_interval(interval):
        """Hash an interval [start, end]"""
        return hash((interval[0], interval[1]))

# Example: Custom hash for pairs
def count_pairs_with_sum(arr, target):
    """Count pairs that sum to target using custom hash"""
    count = 0
    seen = set()
    
    for num in arr:
        complement = target - num
        if complement in seen:
            count += 1
        seen.add(num)
    
    return count

# Test
print(count_pairs_with_sum([1, 5, 7, -1, 5], 6))  # 3
```

## 2. Pair Hashing for Graph Problems

```python
class PairHash:
    """Hash pairs efficiently for graph operations"""
    
    def __init__(self):
        self.pairs = defaultdict(set)
    
    def add_edge(self, u, v):
        """Add undirected edge"""
        self.pairs[u].add(v)
        self.pairs[v].add(u)
    
    def has_edge(self, u, v):
        """Check if edge exists"""
        return v in self.pairs[u]
    
    def get_neighbors(self, u):
        """Get all neighbors"""
        return self.pairs[u]
    
    def remove_edge(self, u, v):
        """Remove edge"""
        self.pairs[u].discard(v)
        self.pairs[v].discard(u)

# Example: Build graph and check connectivity
graph = PairHash()
edges = [(1, 2), (2, 3), (3, 4), (4, 5)]

for u, v in edges:
    graph.add_edge(u, v)

print(f"Neighbors of 3: {graph.get_neighbors(3)}")  # {2, 4}
print(f"Has edge (1, 2): {graph.has_edge(1, 2)}")  # True
print(f"Has edge (1, 5): {graph.has_edge(1, 5)}")  # False
```

## 3. Coordinate Compression

```python
def coordinate_compression(arr):
    """
    Compress coordinates to smaller range
    Useful when coordinates are sparse but large
    Time: O(n log n), Space: O(n)
    """
    # Get sorted unique values
    sorted_vals = sorted(set(arr))
    
    # Create mapping
    compression = {val: idx for idx, val in enumerate(sorted_vals)}
    
    # Apply compression
    compressed = [compression[val] for val in arr]
    
    return compressed, compression, sorted_vals

def compress_2d_points(points):
    """Compress 2D coordinates"""
    x_coords = sorted(set(p[0] for p in points))
    y_coords = sorted(set(p[1] for p in points))
    
    x_map = {x: i for i, x in enumerate(x_coords)}
    y_map = {y: i for i, y in enumerate(y_coords)}
    
    compressed = [(x_map[p[0]], y_map[p[1]]) for p in points]
    
    return compressed, x_map, y_map

# Test
arr = [100, 200, 100, 300, 200, 100]
compressed, mapping, original = coordinate_compression(arr)
print(f"Original: {arr}")
print(f"Compressed: {compressed}")
print(f"Mapping: {mapping}")

points = [(100, 200), (100, 300), (200, 200), (100, 200)]
compressed, x_map, y_map = compress_2d_points(points)
print(f"Compressed points: {compressed}")
```

## 4. Hash Set for Visited Nodes

```python
class Graph:
    """Graph with hash set for visited tracking"""
    
    def __init__(self):
        self.adj_list = defaultdict(list)
    
    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)
    
    def bfs(self, start):
        """BFS using hash set for visited"""
        visited = set()
        queue = [start]
        visited.add(start)
        result = []
        
        while queue:
            node = queue.pop(0)
            result.append(node)
            
            for neighbor in self.adj_list[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def dfs(self, start):
        """DFS using hash set for visited"""
        visited = set()
        result = []
        
        def dfs_helper(node):
            visited.add(node)
            result.append(node)
            
            for neighbor in self.adj_list[node]:
                if neighbor not in visited:
                    dfs_helper(neighbor)
        
        dfs_helper(start)
        return result
    
    def has_cycle(self):
        """Detect cycle using hash set"""
        visited = set()
        
        def dfs(node, parent):
            visited.add(node)
            
            for neighbor in self.adj_list[node]:
                if neighbor not in visited:
                    if dfs(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True
            
            return False
        
        for node in self.adj_list:
            if node not in visited:
                if dfs(node, -1):
                    return True
        
        return False

# Test
g = Graph()
edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]
for u, v in edges:
    g.add_edge(u, v)

print(f"BFS from 1: {g.bfs(1)}")  # [1, 2, 5, 3, 4]
print(f"DFS from 1: {g.dfs(1)}")  # [1, 2, 3, 4, 5]
print(f"Has cycle: {g.has_cycle()}")  # True
```

## 5. Rolling Hash for Strings

```python
class RollingHashString:
    """Rolling hash for efficient string operations"""
    
    def __init__(self, string, base=31, mod=10**9 + 7):
        self.string = string
        self.base = base
        self.mod = mod
        self.n = len(string)
        
        # Precompute hashes
        self.hash = [0] * (self.n + 1)
        self.power = [1] * (self.n + 1)
        
        for i in range(self.n):
            self.hash[i + 1] = (self.hash[i] * base + ord(string[i])) % mod
            self.power[i + 1] = (self.power[i] * base) % mod
    
    def get_hash(self, l, r):
        """Get hash of substring [l, r)"""
        return (self.hash[r] - self.hash[l] * self.power[r - l]) % self.mod
    
    def find_pattern(self, pattern):
        """Find all occurrences of pattern"""
        m = len(pattern)
        pattern_hash = 0
        for c in pattern:
            pattern_hash = (pattern_hash * self.base + ord(c)) % self.mod
        
        result = []
        for i in range(self.n - m + 1):
            if self.get_hash(i, i + m) == pattern_hash:
                if self.string[i:i + m] == pattern:
                    result.append(i)
        
        return result

# Test
rs = RollingHashString("abcabcabc")
print(f"Hash of 'abc' (0:3): {rs.get_hash(0, 3)}")
print(f"Hash of 'abc' (3:6): {rs.get_hash(3, 6)}")
print(f"Find 'abc': {rs.find_pattern('abc')}")  # [0, 3, 6]
```

## 6. Double Hashing

```python
class DoubleHash:
    """Double hashing for collision resistance"""
    
    def __init__(self, string, base1=31, base2=37, 
                 mod1=10**9 + 7, mod2=10**9 + 9):
        self.string = string
        self.base1, self.base2 = base1, base2
        self.mod1, self.mod2 = mod1, mod2
        self.n = len(string)
        
        # First hash
        self.hash1 = [0] * (self.n + 1)
        self.power1 = [1] * (self.n + 1)
        
        # Second hash
        self.hash2 = [0] * (self.n + 1)
        self.power2 = [1] * (self.n + 1)
        
        for i in range(self.n):
            self.hash1[i + 1] = (self.hash1[i] * base1 + ord(string[i])) % mod1
            self.power1[i + 1] = (self.power1[i] * base1) % mod1
            self.hash2[i + 1] = (self.hash2[i] * base2 + ord(string[i])) % mod2
            self.power2[i + 1] = (self.power2[i] * base2) % mod2
    
    def get_hash(self, l, r):
        """Get double hash of substring [l, r)"""
        h1 = (self.hash1[r] - self.hash1[l] * self.power1[r - l]) % self.mod1
        h2 = (self.hash2[r] - self.hash2[l] * self.power2[r - l]) % self.mod2
        return (h1, h2)
    
    def find_pattern(self, pattern):
        """Find pattern using double hash"""
        m = len(pattern)
        
        h1 = 0
        h2 = 0
        for c in pattern:
            h1 = (h1 * self.base1 + ord(c)) % self.mod1
            h2 = (h2 * self.base2 + ord(c)) % self.mod2
        
        pattern_hash = (h1, h2)
        
        result = []
        for i in range(self.n - m + 1):
            if self.get_hash(i, i + m) == pattern_hash:
                if self.string[i:i + m] == pattern:
                    result.append(i)
        
        return result

# Test
dh = DoubleHash("abcabcabc")
print(f"Double hash of 'abc' (0:3): {dh.get_hash(0, 3)}")
print(f"Double hash of 'abc' (3:6): {dh.get_hash(3, 6)}")
print(f"Find 'abc': {dh.find_pattern('abc')}")  # [0, 3, 6]
```

## 7. Hash Map for Memoization

```python
from functools import lru_cache

def fibonacci_memo(n):
    """Fibonacci with hash map memoization"""
    memo = {}
    
    def fib(n):
        if n <= 1:
            return n
        
        if n in memo:
            return memo[n]
        
        memo[n] = fib(n - 1) + fib(n - 2)
        return memo[n]
    
    return fib(n)

def fibonacci_lru(n):
    """Fibonacci with lru_cache"""
    @lru_cache(maxsize=None)
    def fib(n):
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)
    
    return fib(n)

def climb_stairs(n):
    """Climb stairs problem with memoization"""
    memo = {}
    
    def helper(n):
        if n <= 1:
            return 1
        
        if n in memo:
            return memo[n]
        
        memo[n] = helper(n - 1) + helper(n - 2)
        return memo[n]
    
    return helper(n)

# Test
print(fibonacci_memo(50))  # 12586269025
print(fibonacci_lru(50))   # 12586269025
print(climb_stairs(10))    # 89
```

## 8. Consistent Hashing Concept

```python
import hashlib
from bisect import bisect_right

class ConsistentHash:
    """
    Consistent hashing for distributed systems
    Minimizes rehashing when nodes are added/removed
    """
    
    def __init__(self, nodes=None, virtual_nodes=100):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_keys = []
        self.nodes = set()
        
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def _hash(self, key):
        """Hash function"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_node(self, node):
        """Add a node to the ring"""
        self.nodes.add(node)
        
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:v{i}"
            h = self._hash(virtual_key)
            self.ring[h] = node
            self.sorted_keys.append(h)
        
        self.sorted_keys.sort()
    
    def remove_node(self, node):
        """Remove a node from the ring"""
        self.nodes.discard(node)
        
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:v{i}"
            h = self._hash(virtual_key)
            if h in self.ring:
                del self.ring[h]
                self.sorted_keys.remove(h)
    
    def get_node(self, key):
        """Get the node responsible for the key"""
        if not self.ring:
            return None
        
        h = self._hash(key)
        idx = bisect_right(self.sorted_keys, h) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]
    
    def get_distribution(self, keys):
        """Get distribution of keys across nodes"""
        distribution = {node: 0 for node in self.nodes}
        
        for key in keys:
            node = self.get_node(key)
            if node:
                distribution[node] += 1
        
        return distribution

# Test
ch = ConsistentHash(["Node1", "Node2", "Node3"])
keys = [f"key{i}" for i in range(100)]

print("Distribution before removal:")
print(ch.get_distribution(keys))

ch.remove_node("Node2")
print("\nDistribution after removing Node2:")
print(ch.get_distribution(keys))
```

## 9. Advanced Hashing Applications

```python
from collections import defaultdict

# Problem: Find All Anagrams in a String
def find_anagrams(s, p):
    """Find all anagram occurrences using hashing"""
    from collections import Counter
    
    n, m = len(s), len(p)
    if m > n:
        return []
    
    p_count = Counter(p)
    window_count = Counter()
    
    result = []
    
    for i in range(n):
        window_count[s[i]] += 1
        
        if i >= m:
            window_count[s[i - m]] -= 1
            if window_count[s[i - m]] == 0:
                del window_count[s[i - m]]
        
        if window_count == p_count:
            result.append(i - m + 1)
    
    return result

# Problem: Group Shifted Strings
def group_shifted_strings(strings):
    """Group strings that are shifts of each other"""
    groups = defaultdict(list)
    
    for s in strings:
        # Create normalized key by shifting to start with 'a'
        if not s:
            groups[""].append(s)
            continue
        
        shift = ord(s[0])
        key = tuple((ord(c) - shift) % 26 for c in s)
        groups[key].append(s)
    
    return list(groups.values())

# Problem: Find Longest Substring with At Most K Distinct Characters
def longest_substring_k_distinct(s, k):
    """Find longest substring with at most k distinct characters"""
    from collections import defaultdict
    
    freq = defaultdict(int)
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        freq[s[right]] += 1
        
        while len(freq) > k:
            freq[s[left]] -= 1
            if freq[s[left]] == 0:
                del freq[s[left]]
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len

# Test
print(find_anagrams("cbaebabacd", "abc"))  # [0, 6]
print(group_shifted_strings(["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"]))
print(longest_substring_k_distinct("eceba", 2))  # 3
```
