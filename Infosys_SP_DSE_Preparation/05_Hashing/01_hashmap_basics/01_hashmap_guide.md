# Hash Map Guide - Python

## What is a Hash Map?

A Hash Map (Dictionary in Python) stores **key-value pairs** and provides
**O(1) average** time for insert, lookup, and delete operations.

### How Hashing Works (Visual)

```
  KEY          HASH FUNCTION         BUCKET INDEX       VALUE
 ┌──────┐      ┌──────────┐        ┌──────────┐      ┌───────┐
 │ "age" │ ──► │ hash("age") % 8 │ ──► │    3     │ ──► │  25   │
 └──────┘      └──────────┘        └──────────┘      └───────┘

 INTERNAL HASH TABLE STRUCTURE (size = 8 slots):

 ┌────────┬─────────────────────────────────┐
 │ Index  │  Contents                       │
 ├────────┼─────────────────────────────────┤
 │   0    │  (empty)                        │
 │   1    │  (empty)                        │
 │   2    │  "city" ──► "Mumbai"            │
 │   3    │  "age"  ──► 25                  │
 │   4    │  (empty)                        │
 │   5    │  "name" ──► "Alice"             │
 │   6    │  (empty)                        │
 │   7    │  (empty)                        │
 └────────┴─────────────────────────────────┘

 When a collision occurs, Python chains entries:
 ┌────────┬─────────────────────────────────────────────┐
 │   2    │  "city" ──► "Mumbai" ──► "grade" ──► "A"   │
 └────────┴─────────────────────────────────────────────┘
```

### Python Dict Internals

```
 INITIAL STATE (8 slots, empty):
 ┌───┬───┬───┬───┬───┬───┬───┬───┐
 │   │   │   │   │   │   │   │   │
 └───┴───┴───┴───┴───┴───┴───┴───┘

 AFTER INSERTING 5 ELEMENTS (load factor = 5/8 = 0.625):
 ┌───┬───┬───┬───┬───┬───┬───┬───┐
 │   │ K │   │ V │   │ K │   │ V │   5/8 = 62.5% full
 └───┴───┴───┴───┴───┴───┴───┴───┘

 AFTER INSERTING 6 ELEMENTS (load factor = 6/8 = 0.75 > 2/3):
 ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 │   │ K │   │ V │   │ K │ V │   │   │   │   │   │   │   │   │   │
 └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
                                  ▲
                          RESIZE: 8 → 16 slots (doubled)
```

## 1. Python Dict as Hash Map

```python
# ============================================================
# BASIC DICTIONARY OPERATIONS
# ============================================================
# Python dict = built-in hash map implementation
# Keys must be HASHABLE (immutable: str, int, tuple, frozenset)
# Values can be ANY type

hash_map = {}

# INSERT: O(1) average — assigns value to key
hash_map["key1"] = "value1"      # String key
hash_map["key2"] = "value2"
hash_map[123] = "integer key"    # Integer key
hash_map[(1, 2)] = "tuple key"   # Tuple key (mutable list NOT allowed)

# ACCESS: O(1) average — two ways
value = hash_map["key1"]          # ⚠ Raises KeyError if key missing!
value = hash_map.get("key1")      # ✅ Returns None if key missing
value = hash_map.get("key1", "default")  # ✅ Returns "default" if missing

# CHECK EXISTENCE: O(1) average
if "key1" in hash_map:            # 'in' checks KEYS only, not values
    print("Key exists")

# DELETE: O(1) average — three ways
del hash_map["key1"]              # ⚠ Raises KeyError if missing
value = hash_map.pop("key2")      # Remove & return, ⚠ KeyError if missing
value = hash_map.pop("key3", None)  # ✅ Safe: returns None if missing

# LENGTH
print(len(hash_map))              # Number of key-value pairs

# ITERATE
keys = hash_map.keys()            # dict_keys view object
values = hash_map.values()        # dict_values view object
items = hash_map.items()          # dict_items view: [(k1,v1), (k2,v2)]

# UPDATE: Merge multiple key-value pairs at once
hash_map.update({"key3": "value3", "key4": "value4"})

# SET DEFAULT: Get value if exists, otherwise set & return default
hash_map.setdefault("key5", "default_value")

# CLEAR: Remove all entries
hash_map.clear()
```

## Quick Reference: Hash Map Operations

```
┌─────────────────────┬──────────────┬──────────────┐
│ Operation           │ Average      │ Worst Case   │
├─────────────────────┼──────────────┼──────────────┤
│ Insert (set)        │ O(1)         │ O(n)         │
│ Lookup (get)        │ O(1)         │ O(n)         │
│ Delete (pop/del)    │ O(1)         │ O(n)         │
│ Search (in)         │ O(1)         │ O(n)         │
│ Iteration           │ O(n)         │ O(n)         │
│ Space               │ O(n)         │ O(n)         │
└─────────────────────┴──────────────┴──────────────┘
 Worst case happens when ALL keys collide (extremely rare in practice)
```

## 2. defaultdict(int) for Counting

### Visual: How defaultdict(int) Auto-Initializes

```
 BEFORE (plain dict — KeyError!):
 ┌──────────────────────────────────┐
 │ count["h"] = count["h"] + 1     │  ← count["h"] doesn't exist → ERROR
 └──────────────────────────────────┘

 AFTER (defaultdict(int) — auto-creates missing keys with value 0):
 ┌──────────────────────────────────┐
 │ count["h"] += 1                  │  ← count["h"] is auto-created as 0
 │                                  │     then incremented to 1
 │ STEP-BY-STEP for "hello":        │
 │   count["h"] += 1  → {h: 1}     │
 │   count["e"] += 1  → {h:1, e:1} │
 │   count["l"] += 1  → {h:1, e:1, l:1}       │
 │   count["l"] += 1  → {h:1, e:1, l:2}       │
 │   count["o"] += 1  → {h:1, e:1, l:2, o:1}  │
 └──────────────────────────────────┘
```

```python
from collections import defaultdict

# defaultdict(int) creates a dict where missing keys start at 0
# This avoids the "KeyError" problem with plain dicts

# PATTERN 1: Count character frequency
def char_frequency(s):
    count = defaultdict(int)       # Missing keys auto-default to 0
    for c in s:
        count[c] += 1              # No KeyError — works on first occurrence!
    return dict(count)

# STEP-BY-STEP WALKTHROUGH for char_frequency("hello"):
# ┌──────┬─────────────┬──────────────────────────────────┐
# │ Step │ char (c)    │ count state after += 1           │
# ├──────┼─────────────┼──────────────────────────────────┤
# │  1   │ 'h'         │ {'h': 1}                         │
# │  2   │ 'e'         │ {'h': 1, 'e': 1}                │
# │  3   │ 'l'         │ {'h': 1, 'e': 1, 'l': 1}       │
# │  4   │ 'l'         │ {'h': 1, 'e': 1, 'l': 2}       │
# │  5   │ 'o'         │ {'h': 1, 'e': 1, 'l': 2, 'o': 1}│
# └──────┴─────────────┴──────────────────────────────────┘

# PATTERN 2: Count word frequency
def word_frequency(sentence):
    words = sentence.lower().split()
    count = defaultdict(int)
    for word in words:
        count[word] += 1
    return dict(count)

# PATTERN 3: Count occurrences in array
def count_occurrences(arr):
    count = defaultdict(int)
    for num in arr:
        count[num] += 1
    return dict(count)

# Test
print(char_frequency("hello"))  # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
print(word_frequency("the cat and the dog"))  # {'the': 2, 'cat': 1, 'and': 1, 'dog': 1}
```

## 3. defaultdict(list) for Grouping

### Visual: How Grouping Works

```
 INPUT: ["apple", "banana", "avocado", "blueberry"]

 STEP-BY-STEP (group by first letter):
 ┌──────┬────────────┬─────────────────────────────────┐
 │ Step │ word       │ groups state                    │
 ├──────┼────────────┼─────────────────────────────────┤
 │  1   │ "apple"    │ {'a': ['apple']}                │
 │  2   │ "banana"   │ {'a': ['apple'], 'b': ['banana']}  │
 │  3   │ "avocado"  │ {'a': ['apple','avocado'], 'b': ['banana']}  │
 │  4   │ "blueberry"│ {'a': ['apple','avocado'], 'b': ['banana','blueberry']}  │
 └──────┴────────────┴─────────────────────────────────┘

 FINAL: {'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry']}
```

```python
from collections import defaultdict

# defaultdict(list) creates a dict where missing keys start as empty list []
# Perfect for GROUPING elements by a common key

# PATTERN 1: Group strings by first letter
def group_by_first_letter(words):
    groups = defaultdict(list)     # Missing keys auto-default to []
    for word in words:
        groups[word[0]].append(word)  # No KeyError — list is auto-created
    return dict(groups)

# PATTERN 2: Group numbers by even/odd
def group_by_parity(nums):
    groups = defaultdict(list)
    for num in nums:
        groups["even" if num % 2 == 0 else "odd"].append(num)
    return dict(groups)

# PATTERN 3: Group anagrams
# KEY INSIGHT: Sorted version of anagram = same string → use as grouping key
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))   # "eat" → "aet", "tea" → "aet"
        groups[key].append(s)
    return list(groups.values())

# PATTERN 4: Group by custom key (length, modulo, etc.)
def group_by_length(words):
    groups = defaultdict(list)
    for word in words:
        groups[len(word)].append(word)
    return dict(groups)

# Test
print(group_by_first_letter(["apple", "banana", "avocado", "blueberry"]))
# {'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry']}

print(group_by_parity([1, 2, 3, 4, 5, 6]))
# {'odd': [1, 3, 5], 'even': [2, 4, 6]}
```

## 4. Counter for Frequency

### Visual: Counter Operations

```
 Counter("hello"):
 ┌─────────────────────────────────────────┐
 │  Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})  │
 │  Sorted by count (descending)            │
 └─────────────────────────────────────────┘

 Counter ARITHMETIC:
 c1 = Counter(a=3, b=1)     c2 = Counter(a=1, b=2)

 c1 + c2  = Counter(a=4, b=3)      ← ADD counts
 c1 - c2  = Counter(a=2)            ← SUBTRACT (negative removed)
 c1 & c2  = Counter(a=1, b=1)      ← MIN of each count
 c1 | c2  = Counter(a=3, b=2)      ← MAX of each count

 most_common(k): Returns top k elements by count
 ┌────────────────────────────────────────────────────┐
 │ Counter([1,1,1,2,2,3]).most_common(2)              │
 │ → [(1, 3), (2, 2)]    # (element, count) pairs    │
 └────────────────────────────────────────────────────┘
```

```python
from collections import Counter

# Counter is a dict subclass specialized for counting hashable objects
# It automatically counts occurrences and sorts by frequency

# BASIC USAGE
counter = Counter("hello")
print(counter)  # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})

# From a list
counter = Counter([1, 2, 2, 3, 3, 3])
print(counter)  # Counter({3: 3, 2: 2, 1: 1})

# TOP K FREQUENT — most_common(k) returns [(elem, count), ...]
print(counter.most_common(2))  # [(3, 3), (2, 2)]

# COUNTER ARITHMETIC — powerful for comparing frequencies
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)

print(c1 + c2)  # Counter({'a': 4, 'b': 3})   — combined counts
print(c1 - c2)  # Counter({'a': 2})            — subtract (non-positive removed)
print(c1 & c2)  # Counter({'a': 1, 'b': 1})   — minimum of each
print(c1 | c2)  # Counter({'a': 3, 'b': 2})   — maximum of each

# UPDATE vs SUBTRACT
c1.update(c2)      # Adds c2 counts to c1
c1.subtract(c2)    # Subtracts c2 counts from c1

# ============================================================
# PRACTICAL EXAMPLES
# ============================================================

# 1. Most frequent character
def most_frequent_char(s):
    return Counter(s).most_common(1)[0][0]  # (char, count) → char

# 2. Top K frequent elements (LeetCode 347)
def top_k_frequent(nums, k):
    return [num for num, _ in Counter(nums).most_common(k)]

# 3. Longest substring with k replacements (LeetCode 424)
def character_replacement(s, k):
    """Find longest substring where at most k chars can be replaced
    to make all characters the same.

    VISUAL WALKTHROUGH for s="AABABBA", k=1:
    ┌───────┬───────┬─────────────────────┬──────────┐
    │ right │ char  │ count               │ window   │
    ├───────┼───────┼─────────────────────┼──────────┤
    │   0   │  'A'  │ {A:1}               │ "A"  len=1│
    │   1   │  'A'  │ {A:2}               │ "AA" len=2│
    │   2   │  'B'  │ {A:2, B:1}          │ "AAB" len=3│
    │   3   │  'A'  │ {A:3, B:1}          │ "AABA" len=4│
    │   4   │  'B'  │ {A:3, B:2} → shrink │ "ABAB" len=4│
    └───────┴───────┴─────────────────────┴──────────┘
    """
    count = Counter()
    max_count = 0      # Most frequent char count in current window
    left = 0
    result = 0

    for right in range(len(s)):
        count[s[right]] += 1
        max_count = max(max_count, count[s[right]])

        # If chars to replace > k, shrink window from left
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

### Decision Guide

```
                    ┌─────────────────────────────┐
                    │  Need key-value lookups?      │
                    └──────────────┬──────────────┘
                          YES     │     NO
                    ┌─────────────▼─────────────┐
                    │ Key range is small & known?│
                    └──────────────┬────────────┘
                     YES (0-25)    │    NO (strings, large)
               ┌───────────────────▼───────────────────┐
               │         USE ARRAY                     │
               │ • count = [0] * 26  (for a-z)        │
               │ • Cache-friendly                      │
               │ • O(1) worst-case                     │
               │ • Memory efficient                    │
               └──────────────────────────────────────┘
                                    │
               ┌────────────────────▼───────────────────┐
               │         USE HASH MAP                   │
               │ • Keys are strings or complex objects  │
               │ • Key range unknown/large              │
               │ • Need O(1) average lookup             │
               │ • Need flexible grouping               │
               └───────────────────────────────────────┘

 COMPARISON TABLE:
 ┌────────────────────┬───────────────┬───────────────┐
 │ Feature            │ Array[26]     │ Hash Map      │
 ├────────────────────┼───────────────┼───────────────┤
 │ Lookup             │ O(1) worst    │ O(1) avg      │
 │ Insert             │ O(1)          │ O(1) avg      │
 │ Memory             │ Fixed (26)    │ Dynamic       │
 │ Key flexibility    │ Integers only │ Any hashable  │
 │ Cache performance  │ Excellent     │ Good          │
 │ Suitable for       │ 'a'-'z' only │ Any keys      │
 └────────────────────┴───────────────┴───────────────┘
```

```python
# ============================================================
# WHEN TO USE HASH MAP:
# 1. Key range is large or unknown (e.g., strings as keys)
# 2. Need O(1) average lookup/insert/delete
# 3. Keys are strings or complex objects
# 4. Need to count frequencies
# 5. Need to group elements by a key
# 6. Two-sum type problems (complement lookup)
#
# WHEN TO USE ARRAY:
# 1. Key range is small and known (e.g., 0-25 for letters)
# 2. Need cache-friendly access
# 3. Memory is constrained
# 4. Keys are consecutive integers
# 5. Need O(1) worst-case access (not just average)
# ============================================================

# ARRAY approach for character counting (when input is lowercase letters only)
def count_chars_array(s):
    count = [0] * 26                          # Fixed size: one slot per letter
    for c in s:
        count[ord(c) - ord('a')] += 1          # Map 'a'→0, 'b'→1, ... 'z'→25
    return count

# HASH MAP approach for character counting (works for ANY characters)
def count_chars_map(s):
    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1        # Works for unicode, mixed case, etc.
    return count

# Example
print(count_chars_array("hello"))  # [0, 0, 0, ..., 1, 1, 2, ...] (26 elements)
print(count_chars_map("hello"))     # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

## 6. Collision Handling Concepts

### Visual: How Collisions Happen

```
 Two different keys can hash to the SAME bucket index:

 hash("age") % 8 = 3     ──┐
                             ├──► COLLISION at index 3!
 hash("cat") % 8 = 3     ──┘

 METHOD 1: CHAINING (Open Hashing) — Each bucket = linked list
 ┌────────┬──────────────────────────────────────────────┐
 │ Index  │  Contents                                    │
 ├────────┼──────────────────────────────────────────────┤
 │   0    │  (empty)                                     │
 │   1    │  (empty)                                     │
 │   2    │  "city" → "Mumbai"                           │
 │   3    │  "age" → 25 ──► "cat" → "meow"  ← CHAIN!   │
 │   4    │  (empty)                                     │
 │   5    │  "name" → "Alice"                            │
 │   6    │  (empty)                                     │
 │   7    │  (empty)                                     │
 └────────┴──────────────────────────────────────────────┘

 METHOD 2: OPEN ADDRESSING (Closed Hashing) — Linear Probing
 ┌────────┬──────────────────────────────────────────────┐
 │ Index  │  Contents                                    │
 ├────────┼──────────────────────────────────────────────┤
 │   0    │  (empty)                                     │
 │   1    │  (empty)                                     │
 │   2    │  "city" → "Mumbai"                           │
 │   3    │  "age" → 25         ← First key hashes here  │
 │   4    │  "cat" → "meow"     ← Collision! Probe next  │
 │   5    │  "name" → "Alice"                            │
 │   6    │  (empty)                                     │
 │   7    │  (empty)                                     │
 └────────┴──────────────────────────────────────────────┘

 PYTHON'S APPROACH: Uses open addressing with perturbation
   - Perturbation mixes hash bits to reduce clustering
   - Resizes (doubles) when 2/3 full
   - Initial size: 8 slots
```

```python
"""
HASH COLLISION HANDLING — Three Main Strategies:

1. CHAINING (Open Hashing):
   ┌──────┬───┐   ┌──────┬───┐   ┌──────┬───┐
   │  A   │ ●─┼──►│  B   │ ●─┼──►│ NULL │   │
   └──────┴───┘   └──────┴───┘   └──────┴───┘
   - Each bucket holds a linked list
   - Collisions appended to end of list
   - Simple but can degrade to O(n) with bad hash

2. OPEN ADDRESSING (Closed Hashing):
   - Linear Probing:   Check slot (hash+1), (hash+2), ...
   - Quadratic Probing: Check slot (hash+1²), (hash+2²), ...
   - Double Hashing:   Use second hash function for step size
   - All slots stored in the array itself

3. PYTHON'S APPROACH:
   - Open addressing with perturbation (randomized probing)
   - Combines hash with random bits to avoid clustering
   - Resizes when 2/3 full to keep collision rate low
"""

# ============================================================
# SIMPLE HASH TABLE IMPLEMENTATION (Chaining)
# ============================================================
class SimpleHashTable:
    def __init__(self, size=16):
        self.size = size
        self.count = 0
        self.buckets = [[] for _ in range(size)]  # Array of empty lists

    def _hash(self, key):
        """Hash function: maps any key to bucket index [0, size)"""
        return hash(key) % self.size

    def put(self, key, value):
        """Insert or update a key-value pair — O(1) average"""
        # Resize if load factor > 2/3
        if self.count >= self.size * 2 // 3:
            self._resize()

        idx = self._hash(key)
        bucket = self.buckets[idx]

        # Check if key already exists (UPDATE)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # Key doesn't exist → APPEND new pair
        bucket.append((key, value))
        self.count += 1

    def get(self, key):
        """Lookup a key — O(1) average"""
        idx = self._hash(key)
        bucket = self.buckets[idx]

        # Scan the chain (linked list) at this bucket
        for k, v in bucket:
            if k == key:
                return v

        raise KeyError(key)

    def _resize(self):
        """Double the table size and rehash all entries — O(n)"""
        old_buckets = self.buckets
        self.size *= 2
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0

        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)  # Rehash into new table

# Test
ht = SimpleHashTable()
ht.put("name", "Alice")
ht.put("age", 25)
print(ht.get("name"))  # Alice
print(ht.get("age"))   # 25
```

## 7. Common Hash Map Operations

### Master Cheat Sheet

```
 ┌─────────────────────────────────────────────────────────────────────┐
 │              HASH MAP — KEY PATTERNS CHEAT SHEET                    │
 ├─────────────────────┬───────────────────────────────────────────────┤
 │ Pattern             │ When to Use                                  │
 ├─────────────────────┼───────────────────────────────────────────────┤
 │ Two Sum             │ Find pair that sums to target                │
 │ Frequency Count     │ Count occurrences of elements                │
 │ Grouping            │ Group items by a common key                  │
 │ Anagram Check       │ Compare character frequencies                │
 │ Subarray Sum        │ Prefix sum + hash map for sum=k              │
 │ Prefix Sum          │ Convert range queries to point queries       │
 │ Anagram Grouping    │ Sort chars as key, group originals           │
 └─────────────────────┴───────────────────────────────────────────────┘

 TIME COMPLEXITIES:
 ┌────────────┬──────────────┬──────────────┐
 │ Operation  │ Average      │ Worst Case   │
 ├────────────┼──────────────┼──────────────┤
 │ Insert     │ O(1)         │ O(n)         │
 │ Lookup     │ O(1)         │ O(n)         │
 │ Delete     │ O(1)         │ O(n)         │
 │ Space      │ O(n)         │ O(n)         │
 └────────────┴──────────────┴──────────────┘
```

```python
from collections import defaultdict, Counter

# ============================================================
# PATTERN 1: Two Sum — Store complements as you iterate
# ============================================================
# VISUAL WALKTHROUGH for nums=[2,7,11,15], target=9:
# ┌──────┬───────┬────────────┬──────────┬──────────────────┐
# │  i   │ num   │ complement │  seen    │ found?           │
# ├──────┼───────┼────────────┼──────────┼──────────────────┤
# │  0   │   2   │  9-2 = 7   │  {2: 0}  │ No               │
# │  1   │   7   │  9-7 = 2   │  {2: 0}  │ YES! 2 in seen  │
# └──────┴───────┴────────────┴──────────┴──────────────────┘
def two_sum(nums, target):
    seen = {}                              # key=num, value=index
    for i, num in enumerate(nums):
        complement = target - num          # What number would complete the pair?
        if complement in seen:             # O(1) lookup!
            return [seen[complement], i]
        seen[num] = i                      # Store for future lookups
    return []

# ============================================================
# PATTERN 2: Frequency Count — Count occurrences
# ============================================================
def frequency_count(arr):
    freq = Counter(arr)
    return freq

# ============================================================
# PATTERN 3: Grouping — Group by arbitrary key function
# ============================================================
def group_elements(arr, key_func):
    groups = defaultdict(list)
    for item in arr:
        groups[key_func(item)].append(item)
    return dict(groups)

# ============================================================
# PATTERN 4: Anagram Checking — Compare sorted or counted chars
# ============================================================
def are_anagrams(s1, s2):
    return Counter(s1) == Counter(s2)      # O(n) — compare frequencies

# ============================================================
# PATTERN 5: Subarray Sum — Prefix sum + hash map
# ============================================================
# KEY INSIGHT: If prefix_sum[j] - prefix_sum[i] = k,
#   then subarray [i+1..j] sums to k
def subarray_sum(nums, k):
    count = 0
    prefix_sum = 0
    seen = {0: 1}                          # Empty prefix has sum 0

    for num in nums:
        prefix_sum += num
        if prefix_sum - k in seen:         # Any earlier prefix with this difference?
            count += seen[prefix_sum - k]  # Multiple starts possible
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

### Visual Comparison

```
 HASH MAP (dict):                    HASH SET (set):
 ┌─────────────────────────┐         ┌─────────────────────────┐
 │  "Alice" ──► 95         │         │  "Alice"                │
 │  "Bob"   ──► 87         │         │  "Bob"                  │
 │  "Charlie" ► 92         │         │  "Charlie"              │
 └─────────────────────────┘         └─────────────────────────┘
  Stores KEY → VALUE pairs           Stores unique KEYS only

 WHEN TO USE WHICH:
 ┌─────────────────────────┬─────────────────────────────────┐
 │ Use HashMap when:       │ Use HashSet when:               │
 ├─────────────────────────┼─────────────────────────────────┤
 │ Need key → value lookup │ Need O(1) membership check      │
 │ Count occurrences       │ Track visited/seen elements     │
 │ Store associations      │ Remove duplicates               │
 │ e.g., student → grade   │ e.g., "have I visited node X?"  │
 └─────────────────────────┴─────────────────────────────────┘
```

```python
# ============================================================
# HASH MAP (dict): key-value associations
# ============================================================
student_grades = {
    "Alice": 95,
    "Bob": 87,
    "Charlie": 92
}
print(student_grades["Alice"])  # 95 — lookup by key

# ============================================================
# HASH SET (set): unique elements, membership testing
# ============================================================
visited = set()
visited.add(1)
visited.add(2)
visited.add(1)     # Already exists, no change — sets enforce uniqueness
print(visited)      # {1, 2}

print(1 in visited) # O(1) — "Have I seen 1 before?"

# ============================================================
# SET OPERATIONS — Useful for comparing collections
# ============================================================
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

print(set1 | set2)  # Union:              {1, 2, 3, 4, 5, 6}
print(set1 & set2)  # Intersection:       {3, 4}
print(set1 - set2)  # Difference:         {1, 2}
print(set1 ^ set2)  # Symmetric Diff:     {1, 2, 5, 6}
```

## 9. Advanced Hash Map Patterns

### Visual: Prefix Sum Pattern

```
 ARRAY:     [1,  2,  3,  4,  5]
 PREFIX: [0, 1,  3,  6, 10, 15]
              ▲        ▲
              │        │
              └── i=1  └── j=3

 prefix[j] - prefix[i] = 10 - 1 = 9
 → subarray [i+1 .. j] = [2, 3, 4] sums to 9 ✓

 HASH MAP stores: {prefix_sum: first_index}
 When we see the same prefix_sum again → subarray between them sums to 0!
```

```python
from collections import defaultdict

# ============================================================
# PATTERN 1: Two Sum with ALL solutions (not just one)
# ============================================================
# Same key can have MULTIPLE indices → store list of indices
def two_sum_all(nums, target):
    seen = {}                                # key=num → list of indices
    result = []
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            for j in seen[complement]:       # Pair with EACH previous occurrence
                result.append([j, i])
        seen[num] = seen.get(num, [])
        seen[num].append(i)
    return result

# ============================================================
# PATTERN 2: Longest subarray with equal 0s and 1s
# ============================================================
# TRICK: Replace 0→-1, then find longest subarray with sum = 0
# Uses prefix sum: if prefix_sum[j] == prefix_sum[i], subarray sums to 0
def max_len_subarray_equal_01(arr):
    """Find longest subarray with equal number of 0s and 1s"""
    # Replace 0 with -1 so equal counts → sum = 0
    for i in range(len(arr)):
        if arr[i] == 0:
            arr[i] = -1

    prefix_sum = 0
    seen = {0: -1}                          # Empty prefix sum = 0 at index -1
    max_len = 0
    start, end = 0, 0

    for i in range(len(arr)):
        prefix_sum += arr[i]

        if prefix_sum in seen:
            length = i - seen[prefix_sum]   # Subarray from seen[prefix_sum]+1 to i
            if length > max_len:
                max_len = length
                start = seen[prefix_sum] + 1
                end = i
        else:
            seen[prefix_sum] = i            # First occurrence of this sum

    return max_len, arr[start:end + 1]

# ============================================================
# PATTERN 3: Subarray sum divisible by k
# ============================================================
# KEY INSIGHT: If prefix_sum[j] % k == prefix_sum[i] % k,
#   then subarray [i+1..j] has sum divisible by k
def check_subarray_sum(nums, k):
    """Check if there's a subarray with sum divisible by k"""
    seen = {0: -1}                          # Remainder 0 at index -1
    prefix_sum = 0

    for i, num in enumerate(nums):
        prefix_sum += num
        remainder = prefix_sum % k

        if remainder in seen:
            if i - seen[remainder] >= 2:    # Need subarray length >= 2
                return True
        else:
            seen[remainder] = i             # First time seeing this remainder

    return False

# ============================================================
# PATTERN 4: Find all duplicates
# ============================================================
def find_duplicates(nums):
    """Find all elements that appear exactly twice"""
    count = Counter(nums)
    return [num for num, freq in count.items() if freq == 2]

# Test
print(two_sum_all([1, 1, 1], 2))  # [[0, 1], [0, 2], [1, 2]]
print(max_len_subarray_equal_01([0, 1, 0, 1, 0]))  # (5, [-1, 1, -1, 1, -1])
print(check_subarray_sum([23, 2, 4, 6, 7], 6))  # True
print(find_duplicates([4, 3, 2, 7, 8, 2, 3, 1]))  # [2, 3]
```
