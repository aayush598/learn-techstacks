# Hashing Practice Problems

## Difficulty & Topic Map

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                    PRACTICE PROBLEMS MAP                                 │
 ├─────────────────────────────────────────────────────────────────────────┤
 │  EASY (1-5):                                                            │
 │    1. Valid Anagram (242)         — Counter comparison                 │
 │    2. Isomorphic Strings (205)    — Bi-directional mapping             │
 │    3. Jewels and Stones (771)     — Set membership                     │
 │    4. Intersection of Arrays(349) — Set operations                     │
 │    5. Happy Number (202)          — Cycle detection with set           │
 │                                                                         │
 │  MEDIUM (6-10):                                                          │
 │    6. Group Anagrams (49)         — defaultdict(list) grouping          │
 │    7. Longest Substring No Repeat (3) — Sliding window + set           │
 │    8. Min Window Substring (76)   — Sliding window + Counter           │
 │    9. Subarray Sum = K (560)      — Prefix sum + hash map              │
 │   10. Encode/Decode Strings (271) — String delimiter trick             │
 │                                                                         │
 │  HARD (11-15):                                                           │
 │   11. Sliding Window Max (239)    — Monotonic deque                     │
 │   12. Count Smaller After Self(315)— Merge sort + counting             │
 │   13. Max Points on Line (149)    — Slope hash map                     │
 │   14. Word Ladder (127)           — BFS + hash set                     │
 │   15. Longest Duplicate Sub(1044) — Binary search + rolling hash       │
 │                                                                         │
 │  BONUS (16-20):                                                          │
 │   16. Group Shifted Strings (249) — Normalization + grouping           │
 │   17. Continuous Subarray Sum(523)— Remainder pattern                  │
 │   18. Find Duplicate (287)        — Floyd's cycle detection            │
 │   19. Subarray Product < K (713)  — Sliding window + product           │
 │   20. Unique Email Addresses(929) — String processing + set            │
 └─────────────────────────────────────────────────────────────────────────┘
```

## Easy Problems

### 1. Valid Anagram (LeetCode 242)

### Visual Walkthrough

```
 INPUT: s = "anagram", t = "nagaram"

 METHOD 1: CHARACTER COUNTING
 ┌─────────────────────────────────────────────────────────────┐
 │ Step through s: count each char                             │
 │   count = {a:3, n:1, g:1, r:1, m:1}                        │
 │                                                             │
 │ Step through t: decrement each char                         │
 │   'n': count[n]=1→0    'a': count[a]=3→2                   │
 │   'g': count[g]=1→0    'a': count[a]=2→1                   │
 │   'r': count[r]=1→0    'a': count[a]=1→0                   │
 │   'm': count[m]=1→0                                        │
 │                                                             │
 │ All counts are 0 → ANAGRAM ✓                               │
 └─────────────────────────────────────────────────────────────┘

 METHOD 2: SORTING
   sorted("anagram") = ['a','a','a','g','m','n','r']
   sorted("nagaram") = ['a','a','a','g','m','n','r']
   Same? → ANAGRAM ✓

 COMPARISON:
 ┌──────────────────┬──────────┬──────────┐
 │ Method           │ Time     │ Space    │
 ├──────────────────┼──────────┼──────────┤
 │ Counter/Counting │ O(n)     │ O(1)*    │
 │ Sorting          │ O(n log n)│ O(n)    │
 └──────────────────┴──────────┴──────────┘
 * O(1) because at most 26 lowercase letters
```

```python
from collections import Counter

def is_anagram(s, t):
    """
    Check if t is an anagram of s.

    APPROACH: Count characters in s, decrement for t
    If all counts reach 0 → anagram

    Time: O(n) — two passes through strings
    Space: O(1) — at most 26 character counts
    """
    if len(s) != len(t):       # Quick check: different lengths → not anagram
        return False

    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1       # Count up for s
    for c in t:
        count[c] = count.get(c, 0) - 1       # Count down for t
        if count[c] < 0:                      # More of c in t than s → not anagram
            return False
    return True

# Test
print(is_anagram("anagram", "nagaram"))  # True
print(is_anagram("rat", "car"))          # False
```

### 2. Isomorphic Strings (LeetCode 205)

### Visual Walkthrough

```
 INPUT: s = "egg", t = "add"

 TWO-WAY MAPPING (must be bijection):
 ┌───────────────────────────────────────────────────────┐
 │ s → t mapping:          t → s mapping:               │
 │   e → a                   a → e                      │
 │   g → d                   d → g                      │
 │   g → d (consistent!)     d → g (consistent!)        │
 └───────────────────────────────────────────────────────┘

 INPUT: s = "foo", t = "bar"
   s → t:  f→b, o→a, o→r  ← CONFLICT! o can't map to both a and r
   → NOT isomorphic ✗

 WHY TWO MAPS ARE NEEDED:
   s = "ab", t = "aa"
   s→t: a→a, b→a  (OK for s→t)
   t→s: a→a, a→b  ← CONFLICT! a can't map to both a and b
   → NOT isomorphic ✗

 ┌───────────────────────────────────────────────────────┐
 │ BOTH directions must be consistent for isomorphism!   │
 └───────────────────────────────────────────────────────┘
```

```python
def is_isomorphic(s, t):
    """
    Check if s and t are isomorphic (one-to-one character mapping).

    KEY: Need BIJECTION — both s→t and t→s must be consistent
    - "egg" → "add": e↔a, g↔d (one-to-one) ✓
    - "foo" → "bar": o→a AND o→r (NOT one-to-one) ✗

    Time: O(n) — single pass
    Space: O(k) — k = character set size (at most 26)
    """
    if len(s) != len(t):
        return False

    s_to_t = {}    # Map: char in s → char in t
    t_to_s = {}    # Map: char in t → char in s (reverse!)

    for c1, c2 in zip(s, t):
        # Check s → t mapping
        if c1 in s_to_t:
            if s_to_t[c1] != c2:
                return False        # Same s-char maps to different t-char
        else:
            s_to_t[c1] = c2

        # Check t → s mapping (reverse)
        if c2 in t_to_s:
            if t_to_s[c2] != c1:
                return False        # Same t-char maps to different s-char
        else:
            t_to_s[c2] = c1

    return True

# Test
print(is_isomorphic("egg", "add"))    # True
print(is_isomorphic("foo", "bar"))    # False
print(is_isomorphic("paper", "title"))  # True
```

### 3. Jewels and Stones (LeetCode 771)

```python
def num_jewels_in_stones(jewels, stones):
    """
    Count stones that are jewels
    Time: O(n + m), Space: O(m)
    """
    jewel_set = set(jewels)
    return sum(1 for stone in stones if stone in jewel_set)

# Test
print(num_jewels_in_stones("aA", "aAAbbbb"))  # 3
print(num_jewels_in_stones("z", "ZZ"))        # 0
```

### 4. Intersection of Two Arrays (LeetCode 349)

### Visual Walkthrough

```
 INPUT: nums1 = [1, 2, 2, 1], nums2 = [2, 2]

 METHOD: Set Intersection
   set1 = {1, 2}
   set2 = {2}
   set1 & set2 = {2}  ← Only common element

 OUTPUT: [2]

 FOR DUPLICATES (LeetCode 350):
   Counter({1:2, 2:2}) ∩ Counter({2:2})
   min counts: {2:2} → [2, 2]
```

```python
def intersection(nums1, nums2):
    """
    Find intersection of two arrays (unique elements only).
    Time: O(n + m), Space: O(min(n, m))
    """
    return list(set(nums1) & set(nums2))  # Set intersection = common elements

def intersection_ii(nums1, nums2):
    """Find intersection WITH duplicates (each element appears min(count1, count2))"""
    from collections import Counter
    count1 = Counter(nums1)
    result = []

    for num in nums2:
        if count1[num] > 0:
            result.append(num)
            count1[num] -= 1    # Don't use this element again

    return result

# Test
print(intersection([1, 2, 2, 1], [2, 2]))      # [2]
print(intersection_ii([1, 2, 2, 1], [2, 2]))    # [2, 2]
```

### 5. Happy Number (LeetCode 202)

### Visual Walkthrough

```
 INPUT: n = 19

 STEP-BY-STEP:
 ┌──────┬───────┬────────────────────────────┬──────────────────┐
 │ Step │   n   │ Process                    │ Seen             │
 ├──────┼───────┼────────────────────────────┼──────────────────┤
 │  1   │  19   │ 1²+9² = 1+81 = 82         │ {19}             │
 │  2   │  82   │ 8²+2² = 64+4 = 68         │ {19, 82}         │
 │  3   │  68   │ 6²+8² = 36+64 = 100       │ {19,82,68}       │
 │  4   │ 100   │ 1²+0²+0² = 1              │ {19,82,68,100}   │
 │  5   │   1   │ HAPPY! Reached 1 ✓         │                  │
 └──────┴───────┴────────────────────────────┴──────────────────┘

 INPUT: n = 2
   2 → 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 → ...
   CYCLE DETECTED! (4 appears again) → NOT happy ✗

 KEY INSIGHT: Either reaches 1 (happy) or enters a cycle (not happy)
 Use a SET to detect cycles — if we see a number again → cycle!
```

```python
def is_happy(n):
    """
    Check if n is a happy number.
    A happy number eventually reaches 1 when replaced by sum of squares.

    APPROACH: Simulate the process, use set to detect cycles
    - If we reach 1 → happy
    - If we see a number again → cycle → not happy

    Time: O(log n) — number of digits decreases each step
    Space: O(log n) — set stores seen numbers
    """
    def get_next(num):
        """Replace number with sum of squares of its digits"""
        total = 0
        while num > 0:
            digit = num % 10
            total += digit * digit
            num //= 10
        return total

    seen = set()

    while n != 1 and n not in seen:
        seen.add(n)
        n = get_next(n)

    return n == 1   # True if reached 1, False if cycle

# Test
print(is_happy(19))  # True
print(is_happy(2))   # False
```

## Medium Problems

### 6. Group Anagrams (LeetCode 49)

### Visual Walkthrough

```
 INPUT: ["eat", "tea", "tan", "ate", "nat", "bat"]

 STEP 1: For each string, sort its characters → use as grouping key
 ┌───────────┬────────────────┬───────────────────────────────────────┐
 │ String    │ Sorted Key     │ Group (defaultdict(list))             │
 ├───────────┼────────────────┼───────────────────────────────────────┤
 │ "eat"     │ "aet"          │ {'aet': ['eat']}                      │
 │ "tea"     │ "aet"          │ {'aet': ['eat', 'tea']}              │
 │ "tan"     │ "ant"          │ {'aet': ['eat','tea'], 'ant': ['tan']}│
 │ "ate"     │ "aet"          │ {'aet': ['eat','tea','ate'], ...}    │
 │ "nat"     │ "ant"          │ {'aet': [...], 'ant': ['tan','nat']} │
 │ "bat"     │ "abt"          │ {..., 'abt': ['bat']}                 │
 └───────────┴────────────────┴───────────────────────────────────────┘

 STEP 2: Return values of the dict
 OUTPUT: [['eat','tea','ate'], ['tan','nat'], ['bat']]

 WHY SORTED STRING AS KEY:
   Anagrams have identical characters → sorting produces same string
   "eat" → sorted → "aet"
   "tea" → sorted → "aet"  ← Same key!
```

```python
from collections import defaultdict

def group_anagrams(strs):
    """
    Group strings that are anagrams of each other.

    APPROACH: Sort each string → use sorted version as dict key
    Anagrams produce the same sorted string, so they group together.

    Time: O(n * k log k) — n strings, each sorted in O(k log k)
    Space: O(n * k) — storing all strings in groups
    """
    anagram_map = defaultdict(list)

    for s in strs:
        key = ''.join(sorted(s))       # "eat" → "aet", "tea" → "aet"
        anagram_map[key].append(s)

    return list(anagram_map.values())

# Test
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

### 7. Longest Substring Without Repeating Characters (LeetCode 3)

### Visual Walkthrough

```
 INPUT: s = "abcabcbb"

 SLIDING WINDOW with hash map tracking last index of each char:

 ┌──────┬───────┬──────────────────────┬───────────────────┬─────────┐
 │ right│ char  │ char_index map       │ left              │ max_len │
 ├──────┼───────┼──────────────────────┼───────────────────┼─────────┤
 │  0   │ 'a'   │ {a:0}                │ 0                 │ 1       │
 │  1   │ 'b'   │ {a:0, b:1}           │ 0                 │ 2       │
 │  2   │ 'c'   │ {a:0, b:1, c:2}      │ 0                 │ 3       │
 │  3   │ 'a'   │ {a:3, b:1, c:2}      │ 1 (skip to a+1)  │ 3       │
 │  4   │ 'b'   │ {a:3, b:4, c:2}      │ 3 (skip to b+1)  │ 3       │
 │  5   │ 'c'   │ {a:3, b:4, c:5}      │ 4 (skip to c+1)  │ 3       │
 │  6   │ 'b'   │ {a:3, b:6, c:5}      │ 5 (skip to b+1)  │ 3       │
 │  7   │ 'b'   │ {a:3, b:7, c:5}      │ 6 (skip to b+1)  │ 3       │
 └──────┴───────┴──────────────────────┴───────────────────┴─────────┘

 OUTPUT: 3 (substring "abc")

 KEY INSIGHT: When we see a repeated character, jump 'left' to
   max(left, last_index[char] + 1) — no need to shrink one by one!
```

```python
def length_of_longest_substring(s):
    """
    Find length of longest substring without repeating characters.

    APPROACH: Sliding window + hash map
    - char_index stores the LAST SEEN index of each character
    - When we see a repeated char, jump left past its last occurrence
    - Update max_len at each step

    Time: O(n) — each character visited once
    Space: O(min(n, m)) — m = character set size
    """
    char_index = {}    # char → last seen index
    max_len = 0
    left = 0

    for right, c in enumerate(s):
        # If c was seen and its index is within current window
        if c in char_index and char_index[c] >= left:
            left = char_index[c] + 1    # Jump left past the duplicate

        char_index[c] = right           # Update last seen index
        max_len = max(max_len, right - left + 1)

    return max_len

# Test
print(length_of_longest_substring("abcabcbb"))  # 3
print(length_of_longest_substring("bbbbb"))      # 1
print(length_of_longest_substring("pwwkew"))     # 3
```

### 8. Minimum Window Substring (LeetCode 76)

### Visual Walkthrough

```
 INPUT: s = "ADOBECODEBANC", t = "ABC"

 GOAL: Find smallest window in s containing all chars of t

 ┌─────────────────────────────────────────────────────────────┐
 │ t needs: {A:1, B:1, C:1}                                   │
 │                                                             │
 │ Windows found (containing all 3 chars):                    │
 │   "ADOBEC"       length 6                                   │
 │   "CODEBANC"     length 8                                   │
 │   "BANC"         length 4  ← SHORTEST!                     │
 └─────────────────────────────────────────────────────────────┘

 OUTPUT: "BANC"

 APPROACH: Sliding window + Counter
 - Expand right until window contains all chars of t
 - Shrink left while still valid, tracking minimum
 - Use 'formed' counter to track how many chars meet required count
```

```python
from collections import Counter

def min_window(s, t):
    """
    Find minimum window in s containing all characters of t.

    APPROACH: Sliding window + two Counters
    1. Expand right to include more characters
    2. When window is valid (has all t chars), shrink from left
    3. Track minimum valid window

    Time: O(n) — each character processed at most twice
    Space: O(m) — m = length of t
    """
    if not s or not t:
        return ""

    dict_t = Counter(t)          # Characters we need
    required = len(dict_t)       # How many distinct chars needed

    # Filter s to only relevant characters (optimization)
    filtered = [(c, i) for i, c in enumerate(s) if c in dict_t]
    l, r = 0, 0
    formed = 0                   # How many chars have required count
    window = {}

    ans = (float("inf"), 0, 0)  # (window_length, start, end)

    while r < len(filtered):
        char = filtered[r][0]
        window[char] = window.get(char, 0) + 1

        # Check if this char now has required count
        if window[char] == dict_t[char]:
            formed += 1

        # Try to shrink window while it's still valid
        while l <= r and formed == required:
            char = filtered[l][0]
            end = filtered[r][1]
            start = filtered[l][1]

            # Update best answer
            if end - start + 1 < ans[0]:
                ans = (end - start + 1, start, end)

            # Shrink from left
            window[char] -= 1
            if window[char] < dict_t[char]:
                formed -= 1
            l += 1

        r += 1

    return "" if ans[0] == float("inf") else s[ans[1]:ans[2] + 1]

# Test
print(min_window("ADOBECODEBANC", "ABC"))  # "BANC"
print(min_window("a", "a"))                # "a"
```

### 9. Subarray Sum Equals K (LeetCode 560)

```python
def subarray_sum(nums, k):
    """
    Count subarrays with sum k
    Time: O(n), Space: O(n)
    """
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
print(subarray_sum([1, 1, 1], 2))        # 2
print(subarray_sum([1, 2, 3], 3))        # 2
```

### 10. Encode and Decode Strings (LeetCode 271)

```python
class Codec:
    """Encode and decode strings to/from single string"""
    
    def encode(self, strs):
        """Encode list of strings to single string"""
        return '|'.join(s.replace('|', '||') for s in strs)
    
    def decode(self, s):
        """Decode single string to list of strings"""
        return [part.replace('||', '|') for part in s.split('|')]

# Test
codec = Codec()
encoded = codec.encode(["lint", "code", "love", "you"])
print(f"Encoded: {encoded}")
decoded = codec.decode(encoded)
print(f"Decoded: {decoded}")
```

## Hard Problems

### 11. Sliding Window Maximum (LeetCode 239)

### Visual: Monotonic Deque Approach

```
 INPUT: nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

 MONOTONIC DEQUE: stores INDICES, front = max in current window

 ┌───────┬──────────────┬──────────────────────┬────────────┐
 │ right │ Window       │ Deque (indices)      │ Output     │
 ├───────┼──────────────┼──────────────────────┼────────────┤
 │   0   │ [1]          │ [0]                  │            │
 │   1   │ [1,3]        │ [1] (3>1, pop 0)    │            │
 │   2   │ [1,3,-1]     │ [1,2]                │ 3          │
 │   3   │ [3,-1,-3]    │ [1,2,3]              │ 3          │
 │   4   │ [-1,-3,5]    │ [4] (5>-1,-3, pop all)│ 5        │
 │   5   │ [-3,5,3]     │ [4,5]                │ 5          │
 │   6   │ [5,3,6]      │ [6] (6>5,3, pop all) │ 6          │
 │   7   │ [3,6,7]      │ [7] (7>3,6, pop all) │ 7          │
 └───────┴──────────────┴──────────────────────┴────────────┘

 OUTPUT: [3, 3, 5, 5, 6, 7]

 KEY INSIGHT: Deque stores indices in DECREASING order of values
   - Front of deque = index of current maximum
   - Remove indices outside window from front
   - Remove smaller elements from back (they'll never be max)
```

```python
from collections import deque

def max_sliding_window(nums, k):
    """
    Find max in each sliding window of size k.

    APPROACH: Monotonic deque (decreasing)
    - Deque stores indices, values in decreasing order
    - Front = current window's maximum
    - Remove expired indices from front
    - Remove smaller values from back (they're useless)

    Time: O(n) — each element pushed/popped at most once
    Space: O(k) — deque size at most k
    """
    result = []
    dq = deque()    # Stores indices, values decreasing from front to back

    for i in range(len(nums)):
        # Remove indices outside current window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements from back (they'll never be max)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        dq.append(i)

        # Start recording results once window is full
        if i >= k - 1:
            result.append(nums[dq[0]])    # Front = max

    return result

# Test
print(max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))  # [3, 3, 5, 5, 6, 7]
```

### 12. Count of Smaller Numbers After Self (LeetCode 315)

```python
def count_smaller(nums):
    """
    Count smaller elements after each element
    Time: O(n log n), Space: O(n)
    """
    def merge_sort(enum):
        half = len(enum) // 2
        if half > 1:
            left = merge_sort(enum[:half])
            right = merge_sort(enum[half:])
            merge(left, right, enum)
        return enum
    
    def merge(left, right, enum):
        i = j = 0
        while i < len(left) or j < len(right):
            if j == len(right) or (i < len(left) and left[i][1] <= right[j][1]):
                enum[i + j] = left[i]
                count[left[i][0]] += j
                i += 1
            else:
                enum[i + j] = right[j]
                j += 1
    
    count = [0] * len(nums)
    merge_sort(list(enumerate(nums)))
    return count

# Test
print(count_smaller([5, 2, 6, 1]))  # [2, 1, 1, 0]
print(count_smaller([-1]))           # [0]
```

### 13. Max Points on a Line (LeetCode 149)

```python
from collections import defaultdict
from math import gcd

def max_points(points):
    """
    Find maximum number of points on same line
    Time: O(n^2), Space: O(n)
    """
    if len(points) <= 2:
        return len(points)
    
    def slope_key(p1, p2):
        """Get normalized slope as key"""
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        
        if dx == 0:
            return (0, 1)
        if dy == 0:
            return (1, 0)
        
        g = gcd(dx, dy)
        dx //= g
        dy //= g
        
        if dx < 0:
            dx, dy = -dx, -dy
        
        return (dx, dy)
    
    result = 1
    
    for i in range(len(points)):
        slopes = defaultdict(int)
        
        for j in range(i + 1, len(points)):
            slope = slope_key(points[i], points[j])
            slopes[slope] += 1
        
        if slopes:
            result = max(result, max(slopes.values()) + 1)
    
    return result

# Test
print(max_points([[1,1],[2,2],[3,3]]))  # 3
print(max_points([[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]))  # 4
```

### 14. Word Ladder (LeetCode 127)

### Visual: BFS Level by Level

```
 INPUT: begin = "hit", end = "cog", wordList = ["hot","dot","dog","lot","log","cog"]

 BFS GRAPH (edges = one character change):
 ┌─────────────────────────────────────────────────────────┐
 │                                                         │
 │   hit → hot → dot → dog → cog                           │
 │          │     │      │                                 │
 │          │     └→ lot → log → cog                       │
 │          │                                              │
 │   Shortest path: hit → hot → dot → dog → cog (5 steps) │
 └─────────────────────────────────────────────────────────┘

 BFS LEVEL BY LEVEL:
   Queue: [(hit, 1)]
   Visit hot (1 char change) → [(hot, 2)]
   Visit dot, lot (1 char change from hot) → [(dot,3), (lot,3)]
   Visit dog (from dot), log (from lot) → [(dog,4), (log,4)]
   Visit cog (from dog) → return 5!

 WHY BFS: BFS guarantees SHORTEST path in unweighted graph
   Hash set for wordList enables O(1) membership check
```

```python
from collections import deque

def ladder_length(begin_word, end_word, word_list):
    """
    Find shortest transformation sequence from begin_word to end_word,
    changing one character at a time, using words from word_list.

    APPROACH: BFS (breadth-first search)
    - Each word is a node, edges connect words differing by 1 char
    - BFS guarantees shortest path

    Time: O(n * m²) — n words, m word length, for each position try 26 chars
    Space: O(n * m) — queue and visited set
    """
    word_set = set(word_list)       # O(1) membership check

    if end_word not in word_set:
        return 0                    # End word not in dictionary

    queue = deque([(begin_word, 1)])  # (word, steps so far)
    visited = {begin_word}

    while queue:
        word, steps = queue.popleft()

        # Try changing each character position
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i + 1:]

                if new_word == end_word:
                    return steps + 1

                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, steps + 1))

    return 0    # No path found

# Test
print(ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]))  # 5
print(ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"]))  # 0
```

### 15. Longest Duplicate Substring (LeetCode 1044)

```python
def longest_dup_substring(s):
    """
    Find longest substring that appears at least twice
    Time: O(n log n), Space: O(n)
    """
    def check(length):
        if length == 0:
            return ""
        
        base, mod = 31, 10**9 + 7
        
        hash_count = {}
        current_hash = 0
        power = pow(base, length - 1, mod)
        
        for i in range(length):
            current_hash = (current_hash * base + ord(s[i])) % mod
        
        hash_count[current_hash] = [0]
        
        for i in range(1, len(s) - length + 1):
            current_hash = (current_hash - ord(s[i - 1]) * power) % mod
            current_hash = (current_hash * base + ord(s[i + length - 1])) % mod
            current_hash = (current_hash + mod) % mod
            
            if current_hash in hash_count:
                for pos in hash_count[current_hash]:
                    if s[pos:pos + length] == s[i:i + length]:
                        return s[i:i + length]
                hash_count[current_hash].append(i)
            else:
                hash_count[current_hash] = [i]
        
        return ""
    
    left, right = 0, len(s) - 1
    result = ""
    
    while left <= right:
        mid = (left + right) // 2
        found = check(mid)
        if found:
            result = found
            left = mid + 1
        else:
            right = mid - 1
    
    return result

# Test
print(longest_dup_substring("abcabc"))    # "abc"
print(longest_dup_substring("abcdabcd"))  # "abcd"
```

## Bonus Problems

### 16. Group Shifted Strings (LeetCode 249)

```python
from collections import defaultdict

def group_strings(strings):
    """Group strings that are shifts of each other"""
    groups = defaultdict(list)
    
    for s in strings:
        if not s:
            groups[""].append(s)
            continue
        
        # Normalize by shifting first char to 'a'
        shift = ord(s[0]) - ord('a')
        key = tuple((ord(c) - ord('a') - shift) % 26 for c in s)
        groups[key].append(s)
    
    return list(groups.values())

# Test
print(group_strings(["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"]))
```

### 17. Continuous Subarray Sum (LeetCode 523)

```python
def check_subarray_sum(nums, k):
    """
    Check if subarray sum is divisible by k
    Time: O(n), Space: O(k)
    """
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

# Test
print(check_subarray_sum([23, 2, 4, 6, 7], 6))  # True
print(check_subarray_sum([23, 2, 6, 4, 7], 6))  # True
```

### 18. Find Duplicate Number (LeetCode 287)

### Visual: Floyd's Cycle Detection (Tortoise & Hare)

```
 INPUT: nums = [1, 3, 4, 2, 2]

 Treat array as linked list: index → value → next index
   Index:  0  1  2  3  4
   Value:  1  3  4  2  2

 GRAPH:
   0 → 1 → 3 → 2 → 4
               ↑   │
               └───┘   (cycle! 2→4→2)

 FLOYD'S ALGORITHM:
 ┌─────────────────────────────────────────────────────────┐
 │ PHASE 1: Detect cycle (find meeting point)              │
 │   slow = 1 step at a time    slow: 1→3→2→4→2→4→...     │
 │   fast = 2 steps at a time   fast: 1→2→4→2→4→...       │
 │   They meet inside the cycle!                           │
 │                                                         │
 │ PHASE 2: Find entrance to cycle (= the duplicate)      │
 │   Reset slow to 0, keep fast at meeting point           │
 │   Move both 1 step at a time                            │
 │   They meet at cycle entrance = DUPLICATE               │
 │   slow: 0→1→3→2  ← meets at 2!                         │
 │   fast: 2→4→2                                              │
 │                                                         │
 │ OUTPUT: 2 (the duplicate number = cycle entrance)       │
 └─────────────────────────────────────────────────────────┘

 WHY IT WORKS:
   Array values define a linked list: nums[i] = next node
   Duplicate = two indices pointing to same node = cycle entrance
   Floyd's algorithm finds cycle entrance in O(n) time, O(1) space!
```

```python
def find_duplicate(nums):
    """
    Find duplicate number in array (appears at least twice).

    APPROACH: Floyd's Cycle Detection (Tortoise and Hare)
    - Treat array as linked list: nums[i] = next node
    - Duplicate creates a cycle
    - Phase 1: Find meeting point inside cycle
    - Phase 2: Find cycle entrance = duplicate number

    Time: O(n) — two passes
    Space: O(1) — no extra data structures!
    """
    # PHASE 1: Find intersection point in cycle
    slow = fast = nums[0]

    while True:
        slow = nums[slow]           # 1 step
        fast = nums[nums[fast]]     # 2 steps
        if slow == fast:
            break

    # PHASE 2: Find entrance to cycle (the duplicate)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]           # Both move 1 step
        fast = nums[fast]

    return slow    # Entrance to cycle = duplicate number

# Test
print(find_duplicate([1, 3, 4, 2, 2]))  # 2
print(find_duplicate([3, 1, 3, 4, 2]))  # 3
```

### 19. Subarray Product Less Than K (LeetCode 713)

```python
def num_subarray_product_less_than_k(nums, k):
    """
    Count subarrays with product less than k
    Time: O(n), Space: O(1)
    """
    if k <= 1:
        return 0
    
    count = 0
    product = 1
    left = 0
    
    for right in range(len(nums)):
        product *= nums[right]
        
        while product >= k:
            product //= nums[left]
            left += 1
        
        count += right - left + 1
    
    return count

# Test
print(num_subarray_product_less_than_k([10, 5, 2, 6], 100))  # 8
```

### 20. Unique Email Addresses (LeetCode 929)

```python
def num_unique_emails(emails):
    """
    Count unique email addresses
    Time: O(n * m), Space: O(n * m)
    """
    unique = set()
    
    for email in emails:
        local, domain = email.split('@')
        
        # Process local name
        if '+' in local:
            local = local[:local.index('+')]
        
        local = local.replace('.', '')
        
        unique.add(f"{local}@{domain}")
    
    return len(unique)

# Test
print(num_unique_emails([
    "test.email+alex@leetcode.com",
    "test.e.mail+bob@leetcode.com",
    "testemail+david@leetcode.com"
]))  # 2
```

## Complexity Quick Reference

```
 ┌─────────────────────────────────────────┬────────────┬──────────┐
 │ Problem                                 │ Time       │ Space    │
 ├─────────────────────────────────────────┼────────────┼──────────┤
 │ 1.  Valid Anagram (242)                 │ O(n)       │ O(1)     │
 │ 2.  Isomorphic Strings (205)            │ O(n)       │ O(k)     │
 │ 3.  Jewels and Stones (771)             │ O(n+m)     │ O(m)     │
 │ 4.  Intersection of Arrays (349)        │ O(n+m)     │ O(min)   │
 │ 5.  Happy Number (202)                  │ O(log n)   │ O(log n) │
 │ 6.  Group Anagrams (49)                 │ O(nk log k)│ O(nk)    │
 │ 7.  Longest Substring No Repeat (3)     │ O(n)       │ O(min)   │
 │ 8.  Min Window Substring (76)           │ O(n)       │ O(m)     │
 │ 9.  Subarray Sum = K (560)              │ O(n)       │ O(n)     │
 │ 10. Encode/Decode Strings (271)         │ O(n)       │ O(1)     │
 │ 11. Sliding Window Max (239)            │ O(n)       │ O(k)     │
 │ 12. Count Smaller After Self (315)      │ O(n log n) │ O(n)     │
 │ 13. Max Points on Line (149)            │ O(n²)     │ O(n)     │
 │ 14. Word Ladder (127)                   │ O(nm²)    │ O(nm)    │
 │ 15. Longest Duplicate Sub (1044)        │ O(n log n) │ O(n)     │
 │ 16. Group Shifted Strings (249)         │ O(nm)      │ O(nm)    │
 │ 17. Continuous Subarray Sum (523)       │ O(n)       │ O(k)     │
 │ 18. Find Duplicate (287)                │ O(n)       │ O(1)     │
 │ 19. Subarray Product < K (713)          │ O(n)       │ O(1)     │
 │ 20. Unique Email Addresses (929)        │ O(nm)      │ O(nm)    │
 └─────────────────────────────────────────┴────────────┴──────────┘
```

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                 HASHING PROBLEM PATTERNS                                │
 ├──────────────────────┬──────────────────────────────────────────────────┤
 │ Pattern              │ Template & When to Use                          │
 ├──────────────────────┼──────────────────────────────────────────────────┤
 │                      │ seen = {}                                        │
 │ TWO SUM              │ for num in nums:                                │
 │                      │     complement = target - num                   │
 │                      │     if complement in seen: return pair          │
 │                      │     seen[num] = i                               │
 │ USE WHEN: Finding pairs with specific sum                              │
 ├──────────────────────┼──────────────────────────────────────────────────┤
 │                      │ freq = Counter(arr)                             │
 │ FREQUENCY COUNT      │ OR freq = {}; for x: freq[x] = freq.get(x,0)+1│
 │ USE WHEN: Count duplicates, find mode, group by count                  │
 ├──────────────────────┼──────────────────────────────────────────────────┤
 │                      │ groups = defaultdict(list)                      │
 │ GROUPING             │ for item in items:                              │
 │                      │     groups[key(item)].append(item)              │
 │ USE WHEN: Group by sorted string, frequency, custom key                │
 ├──────────────────────┼──────────────────────────────────────────────────┤
 │                      │ freq = Counter(window)                          │
 │ SLIDING WINDOW       │ for right in range(n):                          │
 │   + HASH             │     freq[s[right]] += 1                         │
 │                      │     while invalid: freq[s[left]]-=1; left+=1   │
 │ USE WHEN: Substring/subarray with character constraints                │
 ├──────────────────────┼──────────────────────────────────────────────────┤
 │                      │ prefix_sum = 0                                  │
 │ PREFIX SUM + HASH    │ seen = {0: 1}                                   │
 │                      │ for num in nums:                                │
 │                      │     prefix_sum += num                           │
 │                      │     if prefix_sum - k in seen: found!          │
 │ USE WHEN: Subarray sum equals k, divisible by k                        │
 ├──────────────────────┼──────────────────────────────────────────────────┤
 │                      │ char_index = {}                                 │
 │ LAST SEEN INDEX      │ for right, c in enumerate(s):                  │
 │                      │     if c in char_index: left = max(left, ...)  │
 │                      │     char_index[c] = right                       │
 │ USE WHEN: Longest substring without repeats                            │
 ├──────────────────────┼──────────────────────────────────────────────────┤
 │                      │ sorted_key = tuple(sorted(s))                  │
 │ ANAGRAM KEY          │ groups[sorted_key].append(s)                   │
 │ USE WHEN: Group/check anagrams                                         │
 ├──────────────────────┼──────────────────────────────────────────────────┤
 │                      │ visited = set()                                 │
 │ CYCLE DETECTION      │ Use Floyd's (slow/fast) for O(1) space         │
 │ USE WHEN: Find duplicates, detect cycles in linked structures          │
 ├──────────────────────┼──────────────────────────────────────────────────┤
 │                      │ hash_count = {}                                 │
 │ ROLLING HASH         │ current = (current * base + ord(c)) % mod      │
 │ USE WHEN: String pattern matching, longest duplicate substring         │
 └──────────────────────┴──────────────────────────────────────────────────┘
```
