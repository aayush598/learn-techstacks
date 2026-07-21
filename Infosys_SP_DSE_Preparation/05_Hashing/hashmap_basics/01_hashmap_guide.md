# Hash Map Guide - Python

## 1. Python Dict as Hash Map

```python
# Basic dictionary operations
hash_map = {}

# Insert
hash_map["key1"] = "value1"
hash_map["key2"] = "value2"
hash_map[123] = "integer key"

# Access
value = hash_map["key1"]  # Raises KeyError if not found
value = hash_map.get("key1")  # Returns None if not found
value = hash_map.get("key1", "default")  # Returns "default" if not found

# Check existence
if "key1" in hash_map:
    print("Key exists")

# Delete
del hash_map["key1"]
value = hash_map.pop("key2")  # Remove and return
value = hash_map.pop("key3", None)  # Safe pop with default

# Length
print(len(hash_map))

# Get all keys, values, items
keys = hash_map.keys()
values = hash_map.values()
items = hash_map.items()

# Update
hash_map.update({"key3": "value3", "key4": "value4"})

# Set default (get or set)
hash_map.setdefault("key5", "default_value")

# Clear
hash_map.clear()
```

## 2. defaultdict(int) for Counting

```python
from collections import defaultdict

# Count character frequency
def char_frequency(s):
    count = defaultdict(int)
    for c in s:
        count[c] += 1
    return dict(count)

# Count word frequency
def word_frequency(sentence):
    words = sentence.lower().split()
    count = defaultdict(int)
    for word in words:
        count[word] += 1
    return dict(count)

# Count occurrences in array
def count_occurrences(arr):
    count = defaultdict(int)
    for num in arr:
        count[num] += 1
    return dict(count)

# Example
print(char_frequency("hello"))  # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
print(word_frequency("the cat and the dog"))  # {'the': 2, 'cat': 1, 'and': 1, 'dog': 1}
```

## 3. defaultdict(list) for Grouping

```python
from collections import defaultdict

# Group strings by first letter
def group_by_first_letter(words):
    groups = defaultdict(list)
    for word in words:
        groups[word[0]].append(word)
    return dict(groups)

# Group numbers by even/odd
def group_by_parity(nums):
    groups = defaultdict(list)
    for num in nums:
        groups["even" if num % 2 == 0 else "odd"].append(num)
    return dict(groups)

# Group anagrams
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        groups[key].append(s)
    return list(groups.values())

# Group by custom key
def group_by_length(words):
    groups = defaultdict(list)
    for word in words:
        groups[len(word)].append(word)
    return dict(groups)

# Example
print(group_by_first_letter(["apple", "banana", "avocado", "blueberry"]))
# {'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry']}

print(group_by_parity([1, 2, 3, 4, 5, 6]))
# {'odd': [1, 3, 5], 'even': [2, 4, 6]}
```

## 4. Counter for Frequency

```python
from collections import Counter

# Basic Counter
counter = Counter("hello")
print(counter)  # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})

# Counter from list
counter = Counter([1, 2, 2, 3, 3, 3])
print(counter)  # Counter({3: 3, 2: 2, 1: 1})

# Most common
print(counter.most_common(2))  # [(3, 3), (2, 2)]

# Counter operations
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)

# Addition
print(c1 + c2)  # Counter({'a': 4, 'b': 3})

# Subtraction
print(c1 - c2)  # Counter({'a': 2})

# Intersection
print(c1 & c2)  # Counter({'a': 1, 'b': 1})

# Update
c1.update(c2)
print(c1)

# Subtract
c1.subtract(c2)
print(c1)

# Practical examples
def most_frequent_char(s):
    return Counter(s).most_common(1)[0][0]

def top_k_frequent(nums, k):
    return [num for num, _ in Counter(nums).most_common(k)]

def character_replacement(s, k):
    """Find longest substring with at most k character replacements"""
    count = Counter()
    max_count = 0
    left = 0
    result = 0
    
    for right in range(len(s)):
        count[s[right]] += 1
        max_count = max(max_count, count[s[right]])
        
        while (right - left + 1) - max_count > k:
            count[s[left]] -= 1
            left += 1
        
        result = max(result, right - left + 1)
    
    return result

# Test
print(most_frequent_char("aab"))  # 'a'
print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))  # [1, 2]
print(character_replacement("AABABBA", 1))  # 4
```

## 5. When to Use Hash Map vs Array

```python
"""
WHEN TO USE HASH MAP:
1. Key range is large or unknown
2. Need O(1) average lookup/insert/delete
3. Keys are strings or complex objects
4. Need to count frequencies
5. Need to group elements
6. Two sum type problems

WHEN TO USE ARRAY:
1. Key range is small and known (e.g., 0-25 for letters)
2. Need cache-friendly access
3. Memory is constrained
4. Keys are consecutive integers
5. Need O(1) worst case access

EXAMPLES:
- Character frequency: Use array[26] for lowercase letters
- Word frequency: Use hash map (strings as keys)
- Counting sort: Use array when range is known
- Two sum: Use hash map for O(n) solution
"""

# Array for character counting
def count_chars_array(s):
    count = [0] * 26
    for c in s:
        count[ord(c) - ord('a')] += 1
    return count

# Hash map for character counting
def count_chars_map(s):
    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1
    return count

# Example
print(count_chars_array("hello"))  # [0, 0, 0, ..., 1, 1, 2, ...]
print(count_chars_map("hello"))     # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

## 6. Collision Handling Concepts

```python
"""
HASH COLLISION HANDLING:

1. CHAINING (Open Hashing):
   - Each bucket contains a linked list
   - Collisions appended to list
   - Simple but can degrade to O(n)

2. OPEN ADDRESSING (Closed Hashing):
   - Linear Probing: Check next slot
   - Quadratic Probing: Check i^2 slots away
   - Double Hashing: Use second hash function

3. PYTHON'S APPROACH:
   - Uses open addressing with perturbation
   - Combines hash with random bits
   - Resizes when 2/3 full

PYTHON DICT INTERNALS:
- Initial size: 8 slots
- Load factor threshold: 2/3
- Resizing: Doubles size
- Hash: hash() function with salt
"""

# Simple hash table implementation
class SimpleHashTable:
    def __init__(self, size=16):
        self.size = size
        self.count = 0
        self.buckets = [[] for _ in range(size)]
    
    def _hash(self, key):
        return hash(key) % self.size
    
    def put(self, key, value):
        if self.count >= self.size * 2 // 3:
            self._resize()
        
        idx = self._hash(key)
        bucket = self.buckets[idx]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        bucket.append((key, value))
        self.count += 1
    
    def get(self, key):
        idx = self._hash(key)
        bucket = self.buckets[idx]
        
        for k, v in bucket:
            if k == key:
                return v
        
        raise KeyError(key)
    
    def _resize(self):
        old_buckets = self.buckets
        self.size *= 2
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0
        
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)

# Test
ht = SimpleHashTable()
ht.put("name", "Alice")
ht.put("age", 25)
print(ht.get("name"))  # Alice
print(ht.get("age"))   # 25
```

## 7. Common Hash Map Operations

```python
from collections import defaultdict, Counter

"""
TIME COMPLEXITIES:

Average Case:
- Insert: O(1)
- Lookup: O(1)
- Delete: O(1)
- Search: O(1)

Worst Case (rare):
- All operations: O(n) when all keys collide

Space Complexity: O(n)
"""

# Common patterns

# 1. Two Sum Pattern
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# 2. Frequency Counting
def frequency_count(arr):
    freq = Counter(arr)
    return freq

# 3. Grouping
def group_elements(arr, key_func):
    groups = defaultdict(list)
    for item in arr:
        groups[key_func(item)].append(item)
    return dict(groups)

# 4. Anagram Checking
def are_anagrams(s1, s2):
    return Counter(s1) == Counter(s2)

# 5. Subarray Sum
def subarray_sum(nums, k):
    count = 0
    prefix_sum = 0
    seen = {0: 1}
    
    for num in nums:
        prefix_sum += num
        if prefix_sum - k in seen:
            count += seen[prefix_sum - k]
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1
    
    return count

# Test
print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
print(frequency_count([1, 1, 2, 3, 3, 3]))  # Counter({3: 3, 1: 2, 2: 1})
print(group_elements([1, 2, 3, 4, 5], lambda x: "even" if x % 2 == 0 else "odd"))
print(are_anagrams("listen", "silent"))  # True
print(subarray_sum([1, 1, 1], 2))  # 2
```

## 8. Hash Map vs Hash Set

```python
"""
HASH MAP vs HASH SET:

HASH MAP (dict):
- Stores key-value pairs
- Keys must be hashable
- Use when you need to map keys to values
- Example: {name: age, ...}

HASH SET (set):
- Stores unique elements only
- Elements must be hashable
- Use for membership testing
- Example: {1, 2, 3}

WHEN TO USE WHICH:
- Need to count/use values → HashMap
- Need to track seen/visited → HashSet
- Need to check membership → HashSet
- Need to store associations → HashMap
"""

# Hash Map example
student_grades = {
    "Alice": 95,
    "Bob": 87,
    "Charlie": 92
}

# Hash Set example
visited = set()
visited.add(1)
visited.add(2)
visited.add(1)  # Already exists, no change
print(visited)  # {1, 2}

# Set operations
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

print(set1 | set2)  # Union: {1, 2, 3, 4, 5, 6}
print(set1 & set2)  # Intersection: {3, 4}
print(set1 - set2)  # Difference: {1, 2}
print(set1 ^ set2)  # Symmetric difference: {1, 2, 5, 6}
```

## 9. Advanced Hash Map Patterns

```python
from collections import defaultdict

# 1. Two Sum with multiple solutions
def two_sum_all(nums, target):
    seen = {}
    result = []
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            for j in seen[complement]:
                result.append([j, i])
        seen[num] = seen.get(num, [])
        seen[num].append(i)
    return result

# 2. Subarray with equal 0s and 1s
def max_len_subarray_equal_01(arr):
    """Find longest subarray with equal number of 0s and 1s"""
    # Replace 0 with -1
    for i in range(len(arr)):
        if arr[i] == 0:
            arr[i] = -1
    
    # Now find longest subarray with sum 0
    prefix_sum = 0
    seen = {0: -1}
    max_len = 0
    start, end = 0, 0
    
    for i in range(len(arr)):
        prefix_sum += arr[i]
        
        if prefix_sum in seen:
            length = i - seen[prefix_sum]
            if length > max_len:
                max_len = length
                start = seen[prefix_sum] + 1
                end = i
        else:
            seen[prefix_sum] = i
    
    return max_len, arr[start:end + 1]

# 3. Continuous Subarray Sum (divisible by k)
def check_subarray_sum(nums, k):
    """Check if there's a subarray with sum divisible by k"""
    seen = {0: -1}
    prefix_sum = 0
    
    for i, num in enumerate(nums):
        prefix_sum += num
        remainder = prefix_sum % k
        
        if remainder in seen:
            if i - seen[remainder] >= 2:
                return True
        else:
            seen[remainder] = i
    
    return False

# 4. Find all duplicates
def find_duplicates(nums):
    """Find all elements that appear twice"""
    count = Counter(nums)
    return [num for num, freq in count.items() if freq == 2]

# Test
print(two_sum_all([1, 1, 1], 2))  # [[0, 1], [0, 2], [1, 2]]
print(max_len_subarray_equal_01([0, 1, 0, 1, 0]))  # (5, [-1, 1, -1, 1, -1])
print(check_subarray_sum([23, 2, 4, 6, 7], 6))  # True
print(find_duplicates([4, 3, 2, 7, 8, 2, 3, 1]))  # [2, 3]
```
