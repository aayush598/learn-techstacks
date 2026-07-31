# Dictionaries and Sets in Python — Complete Guide for CP

## 1. Dictionary Creation

```python
# ============================================
# Creating Dictionaries
# ============================================
# Empty dict
d = {}
d = dict()

# From key-value pairs
d = {"a": 1, "b": 2, "c": 3}

# From list of tuples
d = dict([("name", "Alice"), ("age", 25)])

# From zip
keys = ["a", "b", "c"]
values = [1, 2, 3]
d = dict(zip(keys, values))

# Dict comprehension
d = {x: x**2 for x in range(1, 6)}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# From list with frequency count
arr = [1, 2, 2, 3, 3, 3]
d = {}
for x in arr:
    d[x] = d.get(x, 0) + 1
# {1: 1, 2: 2, 3: 3}
```

## 2. Dictionary Access and Methods

```python
d = {"name": "Alice", "age": 25, "city": "NYC"}

# ============================================
# Accessing Values
# ============================================
print(d["name"])        # "Alice" — raises KeyError if missing
print(d.get("name"))    # "Alice" — returns None if missing
print(d.get("salary", 0))  # 0 — default value if key missing

# Check if key exists
print("name" in d)      # True
print("salary" in d)    # False

# ============================================
# Modifying
# ============================================
d["age"] = 26           # Update
d["email"] = "a@b.com"  # Add new key

# setdefault — set if not exists
d.setdefault("country", "US")  # Sets "country" to "US" only if not present
d.setdefault("name", "Bob")    # "name" already exists, stays "Alice"

# update — merge another dict
d.update({"age": 30, "phone": "123"})

# ============================================
# Removing
# ============================================
del d["email"]           # Remove key (KeyError if missing)
phone = d.pop("phone")   # Remove and return value
phone = d.pop("phone", None)  # Remove and return, or default if missing
d.clear()                # Empty the dict

# ============================================
# Iterating
# ============================================
d = {"a": 1, "b": 2, "c": 3}

for key in d:
    print(key, d[key])

for key, value in d.items():
    print(f"{key}: {value}")

for key in d.keys():
    print(key)

for value in d.values():
    print(value)

# ============================================
# Other Useful Methods
# ============================================
d = {"a": 1, "b": 2, "c": 3}

keys = list(d.keys())      # ["a", "b", "c"]
values = list(d.values())  # [1, 2, 3]
items = list(d.items())    # [("a", 1), ("b", 2), ("c", 3)]

# Copy
d2 = d.copy()

# Merge (Python 3.9+)
d3 = d | {"d": 4}  # {"a": 1, "b": 2, "c": 3, "d": 4}
```

## 3. defaultdict

```python
from collections import defaultdict

# ============================================
# defaultdict — no KeyError on missing keys
# ============================================

# Default value: 0
d = defaultdict(int)
d["a"] += 1   # d["a"] = 0 + 1 = 1
d["b"] += 5   # d["b"] = 0 + 5 = 5
print(d)      # defaultdict(<class 'int'>, {'a': 1, 'b': 5})

# Default value: empty list
d = defaultdict(list)
d["fruits"].append("apple")
d["fruits"].append("banana")
d["veggies"].append("carrot")
print(d)  # {'fruits': ['apple', 'banana'], 'veggies': ['carrot']}

# Default value: empty set
d = defaultdict(set)
d["group1"].add(1)
d["group1"].add(2)
d["group2"].add(3)

# ============================================
# CP Usage: Building adjacency list
# ============================================
edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
adj = defaultdict(list)
for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)
# {0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2]}

# ============================================
# CP Usage: Grouping elements
# ============================================
words = ["apple", "bat", "bar", "atom", "book"]
by_length = defaultdict(list)
for w in words:
    by_length[len(w)].append(w)
# {5: ['apple'], 3: ['bat', 'bar', 'atom', 'book']}
```

## 4. Counter

```python
from collections import Counter

# ============================================
# Counter Creation
# ============================================
# From list
arr = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
c = Counter(arr)
print(c)  # Counter({4: 4, 3: 3, 2: 2, 1: 1})

# From string
c = Counter("mississippi")
# Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})

# From dictionary
c = Counter({"a": 3, "b": 1, "c": 2})

# From keyword arguments
c = Counter(a=3, b=1, c=2)

# ============================================
# Counter Methods
# ============================================
c = Counter("abracadabra")

print(c["a"])       # 5 — count of 'a'
print(c["z"])       # 0 — returns 0 for missing keys (no KeyError)
print(c.most_common(3))  # [('a', 5), ('b', 2), ('r', 2)]
print(c.most_common())   # All elements sorted by count

# Elements (iterator of elements repeated by count)
list(c.elements())  # ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'r', 'r', 'c', 'd']

# Arithmetic operations
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)  # Counter({'a': 4, 'b': 3})
print(c1 - c2)  # Counter({'a': 2}) — keeps only positive
print(c1 & c2)  # Counter({'a': 1, 'b': 1}) — minimum
print(c1 | c2)  # Counter({'a': 3, 'b': 2}) — maximum

# ============================================
# CP Usage: Frequency counting
# ============================================
# Find most frequent element
arr = [1, 2, 2, 3, 3, 3, 3]
c = Counter(arr)
most_common = c.most_common(1)[0]  # (3, 4)

# Check if all elements appear same number of times
def is_balanced(arr):
    c = Counter(arr)
    counts = list(c.values())
    return len(set(counts)) == 1

# Check if can be rearranged to alternate characters
from collections import Counter
def can_rearrange(s):
    c = Counter(s)
    max_freq = max(c.values())
    return max_freq <= (len(s) + 1) // 2
```

## 5. Set Operations

```python
# ============================================
# Set Creation
# ============================================
s = {1, 2, 3, 4, 5}
s = set([1, 2, 2, 3, 3])  # {1, 2, 3} — removes duplicates
s = set("hello")           # {'h', 'e', 'l', 'o'}
s = set()                  # Empty set (NOT {} which is empty dict)

# Set comprehension
s = {x**2 for x in range(1, 6)}  # {1, 4, 9, 16, 25}

# ============================================
# Set Methods
# ============================================
s = {1, 2, 3}

# Adding
s.add(4)             # {1, 2, 3, 4}
s.update([5, 6])     # {1, 2, 3, 4, 5, 6}

# Removing
s.remove(3)          # KeyError if not found
s.discard(3)         # No error if not found
popped = s.pop()     # Remove and return arbitrary element
s.clear()            # Empty set

# ============================================
# Set Operations
# ============================================
A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7, 8}

# Union — all elements from both sets
print(A | B)         # {1, 2, 3, 4, 5, 6, 7, 8}
print(A.union(B))    # Same

# Intersection — elements in both sets
print(A & B)         # {4, 5}
print(A.intersection(B))

# Difference — elements in A but not in B
print(A - B)         # {1, 2, 3}
print(A.difference(B))

# Symmetric difference — elements in either set but not both
print(A ^ B)         # {1, 2, 3, 6, 7, 8}
print(A.symmetric_difference(B))

# ============================================
# Set Comparisons
# ============================================
A = {1, 2, 3}
B = {1, 2, 3, 4, 5}
C = {1, 2, 3}

print(A.issubset(B))      # True — A is subset of B
print(A <= B)              # True — same as issubset
print(B.issuperset(A))    # True — B is superset of A
print(B >= A)              # True — same as issuperset
print(A.isdisjoint({4, 5}))  # True — no common elements
print(A.isdisjoint({2, 3}))  # False — has common elements

# ============================================
# Set Membership — O(1) average lookup
# ============================================
s = set(range(1000000))
print(999999 in s)   # True — O(1)
# vs
lst = list(range(1000000))
print(999999 in lst)  # True — O(n)!
```

## 6. frozenset

```python
# ============================================
# frozenset — immutable set
# ============================================
fs = frozenset([1, 2, 3, 4, 5])

# Can be used as dictionary key or set element
d = {frozenset([1, 2]): "pair", frozenset([3, 4, 5]): "triplet"}

# Can be used in sets
s = {frozenset([1, 2]), frozenset([3, 4])}

# Operations still work (return new frozensets)
fs2 = frozenset([4, 5, 6])
print(fs | fs2)   # frozenset({1, 2, 3, 4, 5, 6})
print(fs & fs2)   # frozenset({4, 5})
print(fs - fs2)   # frozenset({1, 2, 3})

# Cannot modify
# fs.add(6)  # AttributeError!

# ============================================
# When to use frozenset in CP
# ============================================
# When you need immutable sets as dictionary keys
# or as elements of another set
state = frozenset([1, 3, 5])
visited = set()
visited.add(state)
```

## 7. Dict vs Set — When to Use What

```python
# ============================================
# USE DICTIONARY when:
# ============================================
# 1. Mapping keys to values
prices = {"apple": 1.5, "banana": 0.5}

# 2. Frequency counting
freq = {}
for x in arr:
    freq[x] = freq.get(x, 0) + 1

# 3. Caching / memoization
memo = {}
def fib(n):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n-1) + fib(n-2)
    return memo[n]

# 4. Graph representation (adjacency list)
graph = {0: [1, 2], 1: [2], 2: [3]}

# ============================================
# USE SET when:
# ============================================
# 1. Fast membership testing
if x in seen_set:  # O(1) vs O(n) for list

# 2. Removing duplicates
unique = set(arr)

# 3. Set operations (union, intersection, etc.)
common = set(arr1) & set(arr2)

# 4. Tracking visited elements
visited = set()
visited.add(node)
```

## 8. Common CP Patterns with Dict/Set

```python
# ============================================
# Pattern 1: Two Sum
# ============================================
def two_sum(arr, target):
    seen = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

print(two_sum([2, 7, 11, 15], 9))  # [0, 1]

# ============================================
# Pattern 2: Subarray Sum Equals K
# ============================================
def subarray_sum(arr, k):
    prefix_sum = 0
    count = 0
    seen = {0: 1}
    
    for num in arr:
        prefix_sum += num
        if prefix_sum - k in seen:
            count += seen[prefix_sum - k]
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1
    
    return count

print(subarray_sum([1, 1, 1], 2))  # 2

# ============================================
# Pattern 3: Group Anagrams
# ============================================
from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)
    for word in words:
        key = tuple(sorted(word))
        groups[key].append(word)
    return list(groups.values())

print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

# ============================================
# Pattern 4: LRU Cache (simplified)
# ============================================
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# ============================================
# Pattern 5: Longest Consecutive Sequence
# ============================================
def longest_consecutive(nums):
    num_set = set(nums)
    longest = 0
    
    for num in num_set:
        if num - 1 not in num_set:  # Start of sequence
            current = num
            streak = 1
            while current + 1 in num_set:
                current += 1
                streak += 1
            longest = max(longest, streak)
    
    return longest

print(longest_consecutive([100, 4, 200, 1, 3, 2]))  # 4

# ============================================
# Pattern 6: Check if two strings are anagrams
# ============================================
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)

print(is_anagram("listen", "silent"))  # True

# ============================================
# Pattern 7: First non-repeating character
# ============================================
def first_unique_char(s):
    count = Counter(s)
    for i, ch in enumerate(s):
        if count[ch] == 1:
            return i
    return -1

print(first_unique_char("leetcode"))  # 0

# ============================================
# Pattern 8: Intersection of two arrays
# ============================================
def intersection(arr1, arr2):
    return list(set(arr1) & set(arr2))

# With duplicates (each element appears min count)
def intersection_with_dup(arr1, arr2):
    c1 = Counter(arr1)
    c2 = Counter(arr2)
    result = []
    for key in c1:
        if key in c2:
            result.extend([key] * min(c1[key], c2[key]))
    return result
```

## 9. Performance Tips

```python
# ============================================
# Dict vs List for lookups
# ============================================
import time

# List lookup — O(n)
large_list = list(range(1000000))
start = time.time()
999999 in large_list
print(f"List: {time.time() - start:.4f}s")  # ~0.01s

# Dict lookup — O(1) average
large_dict = {i: True for i in range(1000000)}
start = time.time()
999999 in large_dict
print(f"Dict: {time.time() - start:.4f}s")  # ~0.000001s

# Set lookup — O(1) average
large_set = set(range(1000000))
start = time.time()
999999 in large_set
print(f"Set:  {time.time() - start:.4f}s")  # ~0.000001s

# ============================================
# Dict as default value — use defaultdict
# ============================================
# SLOW:
d = {}
for x in arr:
    if x not in d:
        d[x] = 0
    d[x] += 1

# FAST:
from collections import defaultdict
d = defaultdict(int)
for x in arr:
    d[x] += 1

# FAST:
from collections import Counter
d = Counter(arr)
```
