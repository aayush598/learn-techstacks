# Hashing and Frequency

Tested hashmap/set patterns for DSA. Everything here is O(1)-average-lookup motivated.

## Core hashmap patterns

```python
from collections import Counter, defaultdict

# Sample data
arr = [1, 2, 2, 3]
s = "aab"
x, k = 2, 1
key, val, v = "k", 1, 5
i, j, w = 0, 0, "abc"

# 1. Build a frequency Counter — O(n)
cnt = Counter(arr)                     # Counter({2: 2, 1: 1, 3: 1})
cnt = Counter(s)                       # works on strings/iterables
cnt[x]                                 # count of x, 0 if absent (never KeyError)
cnt.most_common(k)                     # top-k (value, count) pairs, O(n log k)

# 2. Manual count with dict.get — the universal pattern
freq = {}
for x in arr:
    freq[x] = freq.get(x, 0) + 1

# 3. setdefault for building dict-of-lists
d = {}
d.setdefault(key, []).append(val)      # creates [] only if key missing

# 4. defaultdict factories
freq = defaultdict(int)                # missing -> 0
groups = defaultdict(list)             # missing -> []
index = defaultdict(set)               # missing -> set()
# WARNING: reading d[k] AUTO-CREATES the key in a defaultdict.
# Use d.get(k, default) if you must not insert.

# 5. Lookup optimization / memoization (cache)
memo = {}
def fib(n):
    if n in memo:
        return memo[n]
    if n < 2:
        return n
    memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]

# 6. Hashable keys
d[(i, j)] = v                          # tuple for 2D coordinates
d[frozenset({1, 2})] = v               # frozenset for unordered pairs
d["".join(sorted(w))] = v              # string (canonical form)
# Lists and dicts are UNhashable -> convert to tuple before using as a key.
```

## Templates

### Two-sum returning indices (LeetCode 1)
```python
def two_sum(nums, target):
    d = {}
    for i, x in enumerate(nums):
        if target - x in d:            # complement already seen
            return [d[target - x], i]
        d[x] = i                       # store value -> index
    return []
```
Complexity: O(n) time, O(n) space.
Modify: return the values (store nothing but check membership in a set); find all pairs (collect instead of return).

### First non-repeating character (LeetCode 387)
```python
def first_uniq(s):
    cnt = Counter(s)
    for i, ch in enumerate(s):
        if cnt[ch] == 1:
            return i
    return -1
```
Complexity: O(n) time, O(1) space (bounded alphabet).

### Longest consecutive sequence (LeetCode 128) — set-based O(n)
```python
def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for x in s:                        # only start at a sequence head
        if x - 1 not in s:             # x is the smallest in its run
            cur = x
            length = 1
            while cur + 1 in s:        # stretch the run
                cur += 1
                length += 1
            best = max(best, length)
    return best
```
Complexity: O(n) time (each element visited at most twice), O(n) space.
Key trick: the `x - 1 not in s` guard means we only begin counting from run starts, keeping total work linear.

### Majority element (LeetCode 169) — Boyer-Moore
```python
def majority(nums):                    # guaranteed to exist in the classic problem
    cand = None
    count = 0
    for x in nums:
        if count == 0:
            cand = x
        count += 1 if x == cand else -1
    return cand                        # optional: verify count(cand) > n//2
```
Complexity: O(n) time, O(1) space. No hashmap needed.
If majority is NOT guaranteed, verify: `Counter(nums)[cand] > len(nums) // 2`.

### Subarray sum equals k (LeetCode 560) — prefix sum dict
```python
def subarray_sum(nums, k):
    pref = {0: 1}                      # prefix sum -> how many times seen
    total = ans = 0
    for x in nums:
        total += x
        ans += pref.get(total - k, 0)  # count starts where sum == k
        pref[total] = pref.get(total, 0) + 1
    return ans
```
Complexity: O(n) time, O(n) space.
The `{0: 1}` sentinel counts subarrays equal to the entire prefix (starting at index 0).

### Group by key — dict of lists
```python
def group_by(pairs):                   # pairs = [(key, value), ...]
    groups = defaultdict(list)
    for k, v in pairs:
        groups[k].append(v)
    return dict(groups)
# group_by([("a",1),("b",2),("a",3)]) -> {"a": [1, 3], "b": [2]}
```

### Frequency counting on strings — [0]*26 array
```python
def all_unique_lowercase(s):
    seen = [0] * 26
    for c in s:
        idx = ord(c) - 97              # 97 = ord('a')
        if seen[idx]:
            return False
        seen[idx] = 1
    return True
# Fast anagram check with two 26-arrays, or with Counter:
# Counter(s1) == Counter(s2)
```

## Problem-to-pattern map

| Problem | Pattern | Complexity |
|---|---|---|
| Two sum | dict value->index while scanning | O(n), O(n) |
| First non-repeating char | Counter + one pass | O(n), O(1) |
| Longest consecutive sequence | set + head-start counting | O(n), O(n) |
| Majority element | Boyer-Moore counter | O(n), O(1) |
| Subarray sum = k | prefix dict, count occurrences | O(n), O(n) |
| Anagrams | sorted-string / count-tuple key | O(n·k), O(n·k) |
| Most frequent element | Counter.most_common(1) | O(n), O(n) |
| Contains duplicate | set membership | O(n), O(n) |
| Pair with target | set of seen values | O(n), O(n) |
| # pairs equal k (with freq) | Counter + freq math | O(n), O(n) |
| Group anagrams / by key | defaultdict(list) | O(n·k), O(n·k) |
| Ransom note (can build?) | Counter subtraction | O(n), O(n) |
