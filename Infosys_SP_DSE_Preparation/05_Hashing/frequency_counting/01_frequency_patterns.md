# Frequency Counting Patterns

## Overview: When to Use Frequency Counting

```
 ┌─────────────────────────────────────────────────────────────────┐
 │           FREQUENCY COUNTING — WHEN TO USE                      │
 ├─────────────────────┬───────────────────────────────────────────┤
 │ Problem Type        │ Pattern                                  │
 ├─────────────────────┼───────────────────────────────────────────┤
 │ Count duplicates    │ Counter(arr) → filter count == 2         │
 │ Group by count      │ Counter → group elements by freq         │
 │ Sort by frequency   │ Counter → sort items by -count           │
 │ Anagram grouping    │ Counter(sorted_str) as grouping key      │
 │ Top-K frequent      │ Counter.most_common(k) or heap           │
 │ Sliding window      │ Counter for window state + expand/shrink │
 │ Stream processing   │ Counter + queue for first non-repeating  │
 └─────────────────────┴───────────────────────────────────────────┘
```

## 1. Frequency Counting with Counter

### Visual Walkthrough

```
 INPUT: [1, 2, 2, 3, 3, 3]

 STEP-BY-STEP:
 ┌──────┬───────┬───────────────────────────────────┐
 │ Step │ item  │ Counter state                     │
 ├──────┼───────┼───────────────────────────────────┤
 │  1   │   1   │ Counter({1: 1})                   │
 │  2   │   2   │ Counter({1: 1, 2: 1})             │
 │  3   │   2   │ Counter({1: 1, 2: 2})             │
 │  4   │   3   │ Counter({2: 2, 1: 1, 3: 1})      │
 │  5   │   3   │ Counter({3: 2, 2: 2, 1: 1})      │
 │  6   │   3   │ Counter({3: 3, 2: 2, 1: 1})      │
 └──────┴───────┴───────────────────────────────────┘

 OUTPUT: Counter({3: 3, 2: 2, 1: 1})
         Sorted by frequency (descending) automatically!
```

```python
from collections import Counter, defaultdict

# ============================================================
# FREQUENCY COUNTING — Two Main Approaches
# ============================================================

# APPROACH 1: Using Counter (Pythonic, one-liner)
def count_frequency(arr):
    """Count frequency of each element — O(n)"""
    return Counter(arr)

# APPROACH 2: Using plain dict (interview-friendly, shows understanding)
def count_frequency_dict(arr):
    """Count frequency using plain dict — O(n)"""
    freq = {}
    for item in arr:
        freq[item] = freq.get(item, 0) + 1  # get returns 0 if key missing
    return freq

# CHARACTER FREQUENCY — Useful for anagram problems
def char_frequency(s):
    return Counter(s)  # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})

# WORD FREQUENCY — Useful for text analysis problems
def word_frequency(text):
    words = text.lower().split()
    return Counter(words)

# Test
print(count_frequency([1, 2, 2, 3, 3, 3]))  # Counter({3: 3, 2: 2, 1: 1})
print(char_frequency("hello"))  # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})
print(word_frequency("the cat and the dog"))  # Counter({'the': 2, 'cat': 1, ...})
```

## 2. Group Elements by Frequency

### Visual Walkthrough: sort_by_frequency

```
 INPUT: [2, 3, 5, 3, 7, 9, 5, 3]

 STEP 1: Count frequencies
 ┌─────────────────────────────────────────────┐
 │ Counter({3: 3, 5: 2, 2: 1, 7: 1, 9: 1})   │
 └─────────────────────────────────────────────┘

 STEP 2: Sort by (-frequency, value)
 ┌──────┬───────┬──────────┬───────────────────┐
 │ num  │ freq  │ sort key │ position          │
 ├──────┼───────┼──────────┼───────────────────┤
 │  3   │   3   │ (-3, 3)  │ 1st (highest)     │
 │  3   │   3   │ (-3, 3)  │ 2nd               │
 │  3   │   3   │ (-3, 3)  │ 3rd               │
 │  5   │   2   │ (-2, 5)  │ 4th               │
 │  5   │   2   │ (-2, 5)  │ 5th               │
 │  2   │   1   │ (-1, 2)  │ 6th               │
 │  7   │   1   │ (-1, 7)  │ 7th               │
 │  9   │   1   │ (-1, 9)  │ 8th               │
 └──────┴───────┴──────────┴───────────────────┘

 OUTPUT: [3, 3, 3, 5, 5, 2, 7, 9]
```

```python
from collections import Counter, defaultdict

def group_by_frequency(arr):
    """Group elements by their frequency"""
    freq = Counter(arr)
    groups = defaultdict(list)
    
    for num, count in freq.items():
        groups[count].append(num)
    
    return dict(groups)

def sort_by_frequency(arr):
    """Sort elements by frequency (descending)"""
    freq = Counter(arr)
    return sorted(arr, key=lambda x: (-freq[x], x))

def frequency_sort(s):
    """Sort characters by frequency (LeetCode 451)"""
    freq = Counter(s)
    result = []
    
    for char, count in sorted(freq.items(), key=lambda x: -x[1]):
        result.append(char * count)
    
    return ''.join(result)

# Test
print(group_by_frequency([1, 1, 2, 2, 2, 3]))  # {2: [1, 2], 1: [3]}
print(sort_by_frequency([2, 3, 5, 3, 7, 9, 5, 3]))  # [3, 3, 3, 5, 5, 2, 7, 9]
print(frequency_sort("tree"))  # "eert"
```

## 3. Top K Frequent Elements (LeetCode 347)

### Visual Walkthrough: Bucket Sort Approach

```
 INPUT: nums = [1, 1, 1, 2, 2, 3], k = 2

 STEP 1: Count frequencies
 Counter({1: 3, 2: 2, 3: 1})

 STEP 2: Create buckets (index = frequency)
 ┌─────────────────────────────────────────────────────┐
 │ Buckets (index = frequency, value = list of nums):  │
 │                                                     │
 │ Bucket 0: []           (nothing has freq 0)         │
 │ Bucket 1: [3]          (3 appears once)             │
 │ Bucket 2: [2]          (2 appears twice)            │
 │ Bucket 3: [1]          (1 appears thrice)           │
 │ ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑  │
 │ Scan from RIGHT to LEFT (highest freq first)        │
 └─────────────────────────────────────────────────────┘

 STEP 3: Collect top k from rightmost buckets
   freq=3: [1] → result=[1]
   freq=2: [2] → result=[1, 2]  ← k=2, done!

 OUTPUT: [1, 2]

 WHY BUCKET SORT IS O(n):
   - Counting: O(n)
   - Creating buckets: O(n)
   - Scanning buckets: O(n) (at most n buckets)
   - TOTAL: O(n) — better than O(n log n) heap approach!
```

```python
from collections import Counter
import heapq

# ============================================================
# APPROACH 1: Counter.most_common(k) — Simplest, O(n log k)
# ============================================================
def top_k_frequent(nums, k):
    """Find k most frequent elements"""
    count = Counter(nums)
    return [num for num, _ in count.most_common(k)]

# ============================================================
# APPROACH 2: Min-Heap — O(n log k), good for large n
# ============================================================
# Keep only k elements in heap → log k per insert
def top_k_frequent_heap(nums, k):
    """Using heap — efficient when k << n"""
    count = Counter(nums)

    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:               # Keep only k smallest frequencies
            heapq.heappop(heap)          # Remove lowest frequency

    return [num for freq, num in heap]

# ============================================================
# APPROACH 3: Bucket Sort — O(n), optimal!
# ============================================================
def top_k_frequent_bucket(nums, k):
    """Using bucket sort — O(n) time, O(n) space"""
    count = Counter(nums)
    max_freq = max(count.values())

    # Bucket[i] = list of numbers that appear i times
    buckets = [[] for _ in range(max_freq + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)

    # Collect from highest frequency bucket down
    result = []
    for freq in range(max_freq, 0, -1):
        result.extend(buckets[freq])
        if len(result) >= k:
            break

    return result[:k]

# Test
print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))  # [1, 2]
print(top_k_frequent_heap([1, 1, 1, 2, 2, 3], 2))  # [1, 2]
print(top_k_frequent_bucket([1, 1, 1, 2, 2, 3], 2))  # [1, 2]
```

### Complexity Comparison

```
 ┌─────────────────────┬────────────┬──────────┬───────────────────────┐
 │ Approach            │ Time       │ Space    │ Best When             │
 ├─────────────────────┼────────────┼──────────┼───────────────────────┤
 │ Counter.most_common │ O(n log n) │ O(n)     │ Simple, small input   │
 │ Min-Heap            │ O(n log k) │ O(n+k)   │ k << n                │
 │ Bucket Sort         │ O(n)       │ O(n)     │ Always optimal!       │
 └─────────────────────┴────────────┴──────────┴───────────────────────┘
```

## 4. Sort Characters by Frequency

### Visual: How Frequency Sorting Works

```
 INPUT: "tree"

 STEP 1: Count characters
 Counter({'e': 2, 't': 1, 'r': 1})

 STEP 2: Sort by frequency (descending)
 ┌───────────┬───────┬───────────────────────┐
 │ Character │ Freq  │ Repeated String        │
 ├───────────┼───────┼───────────────────────┤
 │   'e'     │   2   │ "ee"                  │
 │   'r'     │   1   │ "r"                   │
 │   't'     │   1   │ "t"                   │
 └───────────┴───────┴───────────────────────┘

 STEP 3: Concatenate
 OUTPUT: "eert"

 ALTERNATIVE OUTPUT: "eetr" (also valid, depends on tie-breaking)
```

```python
from collections import Counter

def sort_chars_by_frequency(s):
    """Sort characters by frequency in descending order"""
    freq = Counter(s)
    
    # Sort by frequency, then by character for stability
    sorted_chars = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    
    result = []
    for char, count in sorted_chars:
        result.append(char * count)
    
    return ''.join(result)

def sort_string_by_frequency(s):
    """Alternative implementation"""
    freq = Counter(s)
    max_freq = max(freq.values()) if freq else 0
    
    result = []
    for f in range(max_freq, 0, -1):
        for char in sorted(freq.keys()):
            if freq[char] == f:
                result.append(char * f)
    
    return ''.join(result)

# Test
print(sort_chars_by_frequency("tree"))  # "eert"
print(sort_chars_by_frequency("cccaaa"))  # "aaaccc"
print(sort_string_by_frequency("Aabb"))  # "bbAa"
```

## 5. Maximum Frequency Character

### Visual: Single-Pass Max Tracking

```
 INPUT: "hello"

 STEP-BY-STEP (tracking max as we go):
 ┌──────┬───────┬─────────────────────┬───────────┬──────────┐
 │ Step │ char  │ freq map            │ max_count │ max_char │
 ├──────┼───────┼─────────────────────┼───────────┼──────────┤
 │  1   │ 'h'   │ {h:1}               │    1      │   'h'    │
 │  2   │ 'e'   │ {h:1, e:1}          │    1      │   'h'    │
 │  3   │ 'l'   │ {h:1, e:1, l:1}     │    1      │   'h'    │
 │  4   │ 'l'   │ {h:1, e:1, l:2}     │    2      │   'l'    │ ← NEW MAX!
 │  5   │ 'o'   │ {h:1, e:1, l:2, o:1}│    2      │   'l'    │
 └──────┴───────┴─────────────────────┴───────────┴──────────┘

 OUTPUT: 'l' (appears 2 times)
```

```python
from collections import Counter

def max_freq_char(s):
    """Find character with maximum frequency"""
    if not s:
        return None
    
    freq = Counter(s)
    return freq.most_common(1)[0][0]

def max_freq_char_dict(s):
    """Using plain dict"""
    if not s:
        return None
    
    freq = {}
    max_count = 0
    max_char = s[0]
    
    for c in s:
        freq[c] = freq.get(c, 0) + 1
        if freq[c] > max_count:
            max_count = freq[c]
            max_char = c
    
    return max_char

def max_freq_substring(s, k):
    """Find length of longest substring with at most k distinct characters"""
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
print(max_freq_char("hello"))  # 'l'
print(max_freq_char_dict("hello"))  # 'l'
print(max_freq_substring("eceba", 2))  # 3
```

## 6. Subarray with Given Frequency Pattern

```python
from collections import defaultdict

def subarray_with_frequency(arr, target_freq):
    """Find subarray where most frequent element appears target_freq times"""
    freq = defaultdict(int)
    left = 0
    result = []
    
    for right in range(len(arr)):
        freq[arr[right]] += 1
        
        # Check if any element appears target_freq times
        while any(f >= target_freq for f in freq.values()):
            if freq[arr[left]] >= target_freq:
                result.append(arr[left:right + 1])
            freq[arr[left]] -= 1
            left += 1
    
    return result

def k_most_frequent_subarray(arr, k):
    """Find subarray with at most k distinct elements"""
    freq = defaultdict(int)
    left = 0
    result = []
    
    for right in range(len(arr)):
        freq[arr[right]] += 1
        
        while len(freq) > k:
            freq[arr[left]] -= 1
            if freq[arr[left]] == 0:
                del freq[arr[left]]
            left += 1
        
        result.append(arr[left:right + 1])
    
    return result

# Test
print(subarray_with_frequency([1, 2, 2, 3, 3, 3, 2], 3))
print(k_most_frequent_subarray([1, 2, 3, 1, 2, 3], 2))
```

## 7. Count Distinct Elements in Every Window

### Visual Walkthrough

```
 INPUT: arr = [1, 2, 1, 3, 4, 2, 3], k = 4

 STEP-BY-STEP SLIDING WINDOW:
 ┌──────────┬──────────────────┬────────────────────┬─────────────┐
 │ Position │ Window           │ freq map           │ # Distinct  │
 ├──────────┼──────────────────┼────────────────────┼─────────────┤
 │ 0..3     │ [1, 2, 1, 3]     │ {1:2, 2:1, 3:1}   │ 3           │
 │ 1..4     │ [2, 1, 3, 4]     │ {2:1, 1:1, 3:1, 4:1}│ 4         │
 │ 2..5     │ [1, 3, 4, 2]     │ {1:1, 3:1, 4:1, 2:1}│ 4         │
 │ 3..6     │ [3, 4, 2, 3]     │ {3:2, 4:1, 2:1}   │ 3           │
 └──────────┴──────────────────┴────────────────────┴─────────────┘

 OUTPUT: [3, 4, 4, 3]

 KEY OPERATION: When window slides right by 1:
   1. ADD new element (right side): freq[new] += 1
   2. REMOVE old element (left side): freq[old] -= 1
      → If freq[old] == 0, delete it (reduces distinct count)
```

```python
from collections import defaultdict

def count_distinct_in_windows(arr, k):
    """Count distinct elements in every window of size k"""
    n = len(arr)
    if n < k:
        return []
    
    freq = defaultdict(int)
    result = []
    
    # First window
    for i in range(k):
        freq[arr[i]] += 1
    result.append(len(freq))
    
    # Remaining windows
    for i in range(k, n):
        # Add new element
        freq[arr[i]] += 1
        
        # Remove old element
        freq[arr[i - k]] -= 1
        if freq[arr[i - k]] == 0:
            del freq[arr[i - k]]
        
        result.append(len(freq))
    
    return result

def distinct_elements_sliding(arr, k):
    """Optimized version using set"""
    n = len(arr)
    if n < k:
        return []
    
    from collections import Counter
    window = Counter(arr[:k])
    result = [len(window)]
    
    for i in range(k, n):
        # Remove leftmost
        window[arr[i - k]] -= 1
        if window[arr[i - k]] == 0:
            del window[arr[i - k]]
        
        # Add rightmost
        window[arr[i]] += 1
        
        result.append(len(window))
    
    return result

# Test
print(count_distinct_in_windows([1, 2, 1, 3, 4, 2, 3], 4))  # [3, 4, 4, 3]
print(distinct_elements_sliding([1, 2, 1, 3, 4, 2, 3], 4))  # [3, 4, 4, 3]
```

## 8. First Non-Repeating Character in Stream (LeetCode 387)

### Visual Walkthrough

```
 INPUT: s = "aababc"

 ┌───────┬───────┬───────────────────┬───────────────┬──────────────────┐
 │ Step  │ char  │ count map         │ queue (order) │ first non-repeat │
 ├───────┼───────┼───────────────────┼───────────────┼──────────────────┤
 │   1   │ 'a'   │ {a:1}             │ [a]           │ 'a'              │
 │   2   │ 'a'   │ {a:2}             │ []            │ '#' (none)       │
 │   3   │ 'b'   │ {a:2, b:1}        │ [b]           │ 'b'              │
 │   4   │ 'a'   │ {a:3, b:1}        │ [b]           │ 'b'              │
 │   5   │ 'b'   │ {a:3, b:2}        │ []            │ '#' (none)       │
 │   6   │ 'c'   │ {a:3, b:2, c:1}   │ [c]           │ 'c'              │
 └───────┴───────┴───────────────────┴───────────────┴──────────────────┘

 OUTPUT: ['a', '#', 'b', '#', '#', 'c']

 KEY INSIGHT: Use a QUEUE to maintain order of first occurrences
   - Add char to queue when count becomes 1
   - Remove from front of queue while count > 1
   - Front of queue = first non-repeating character
```

```python
from collections import OrderedDict

def first_non_repeating_stream(s):
    """Find first non-repeating character at each point in stream"""
    freq = OrderedDict()
    result = []
    
    for c in s:
        freq[c] = freq.get(c, 0) + 1
        
        # Find first character with frequency 1
        found = '#'
        for char, count in freq.items():
            if count == 1:
                found = char
                break
        
        result.append(found)
    
    return result

from collections import Counter

def first_non_repeating_efficient(s):
    """More efficient approach using Counter"""
    count = Counter()
    queue = []
    result = []
    
    for c in s:
        count[c] += 1
        
        # Add to queue if first occurrence
        if count[c] == 1:
            queue.append(c)
        
        # Remove from front if repeating
        while queue and count[queue[0]] > 1:
            queue.pop(0)
        
        result.append(queue[0] if queue else '#')
    
    return result

# Test
print(first_non_repeating_stream("aababc"))  # ['a', '#', 'b', '#', '#', 'c']
print(first_non_repeating_efficient("aababc"))  # ['a', '#', 'b', '#', '#', 'c']
```

## 9. Check if Two Strings Are Anagrams

```python
from collections import Counter

def are_anagrams(s1, s2):
    """Check if two strings are anagrams"""
    return Counter(s1) == Counter(s2)

def are_anagrams_sorted(s1, s2):
    """Using sorting"""
    return sorted(s1) == sorted(s2)

def are_anagrams_array(s1, s2):
    """Using fixed-size array (for lowercase letters)"""
    if len(s1) != len(s2):
        return False
    
    count = [0] * 26
    for c in s1:
        count[ord(c) - ord('a')] += 1
    for c in s2:
        count[ord(c) - ord('a')] -= 1
        if count[ord(c) - ord('a')] < 0:
            return False
    return True

def are_anagrams_dict(s1, s2):
    """Using plain dict"""
    if len(s1) != len(s2):
        return False
    
    freq = {}
    for c in s1:
        freq[c] = freq.get(c, 0) + 1
    for c in s2:
        if c not in freq:
            return False
        freq[c] -= 1
        if freq[c] < 0:
            return False
    return True

# Test
print(are_anagrams("listen", "silent"))  # True
print(are_anagrams_sorted("hello", "olleh"))  # True
print(are_anagrams_array("anagram", "nagaram"))  # True
print(are_anagrams_dict("rat", "car"))  # False
```

## 10. Find All Duplicates in Array (LeetCode 442)

### Visual: Negative Marking Technique (O(n) time, O(1) space!)

```
 INPUT: [4, 3, 2, 7, 8, 2, 3, 1]
 Values are 1..n, find elements appearing twice.

 IDEA: Use array INDEX as hash key!
   - Value v maps to index (v-1)
   - If we've seen v before, nums[v-1] is already negative

 STEP-BY-STEP:
 ┌──────┬────────────────────────┬───────────────────────────┬──────────┐
 │ Step │ Current num            │ Array state               │ result   │
 ├──────┼────────────────────────┼───────────────────────────┼──────────┤
 │  1   │ nums[0]=4, idx=3       │ [4,3,2,-7,8,2,3,1]       │ []       │
 │      │ nums[3]=7>0 → negate   │                           │          │
 │  2   │ nums[1]=3, idx=2       │ [4,3,-2,-7,8,2,3,1]      │ []       │
 │      │ nums[2]=2>0 → negate   │                           │          │
 │  3   │ nums[2]=-2, idx=1      │ [4,3,-2,-7,8,2,3,1]      │ []       │
 │      │ abs=2, nums[1]=3>0→neg  │ [4,-3,-2,-7,8,2,3,1]     │          │
 │  4   │ nums[3]=-7, idx=6      │ [4,-3,-2,-7,8,2,-3,1]    │ []       │
 │      │ abs=7, nums[6]=3>0→neg  │                           │          │
 │  5   │ nums[4]=8, idx=7       │ [4,-3,-2,-7,8,2,-3,-1]   │ []       │
 │      │ nums[7]=1>0 → negate   │                           │          │
 │  6   │ nums[5]=2, idx=1       │ [4,-3,-2,-7,8,2,-3,-1]   │ [2] ★    │
 │      │ nums[1]=-3 < 0 → DUP!  │ Already negative!         │          │
 │  7   │ nums[6]=-3, idx=2      │ [4,-3,-2,-7,8,2,-3,-1]   │ [2,3] ★  │
 │      │ abs=3, nums[2]=-2 < 0  │ Already negative!         │          │
 │  8   │ nums[7]=-1, idx=0      │ [4,-3,-2,-7,8,2,-3,-1]   │ [2,3]    │
 │      │ abs=1, nums[0]=4>0→neg  │ [-4,-3,-2,-7,8,2,-3,-1]  │          │
 └──────┴────────────────────────┴───────────────────────────┴──────────┘

 OUTPUT: [2, 3]

 WHY IT WORKS:
   - Each value v "marks" index (v-1) by making it negative
   - If we visit v again and find nums[v-1] already negative → duplicate!
   - Time: O(n), Space: O(1) — modifies input array
```

```python
def find_duplicates(nums):
    """Find all elements that appear twice"""
    freq = Counter(nums)
    return [num for num, count in freq.items() if count == 2]

def find_duplicates_optimal(nums):
    """Using negative marking - O(n) time, O(1) space"""
    result = []
    
    for num in nums:
        idx = abs(num) - 1
        if nums[idx] < 0:
            result.append(abs(num))
        else:
            nums[idx] = -nums[idx]
    
    return result

def find_duplicates_set(nums):
    """Using set"""
    seen = set()
    duplicates = set()
    
    for num in nums:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    
    return list(duplicates)

# Test
print(find_duplicates([4, 3, 2, 7, 8, 2, 3, 1]))  # [2, 3]
print(find_duplicates_optimal([4, 3, 2, 7, 8, 2, 3, 1]))  # [2, 3]
print(find_duplicates_set([1, 2, 3, 1, 4, 5]))  # [1]
```

## 11. Additional Frequency Problems

### Visual: Longest Substring with K Distinct Characters

```
 INPUT: s = "eceba", k = 2

 SLIDING WINDOW:
 ┌──────────┬──────────────────┬────────────────────┬─────────────┐
 │ Window   │ chars in window  │ distinct count     │ max_len     │
 ├──────────┼──────────────────┼────────────────────┼─────────────┤
 │ "e"      │ {e:1}            │ 1 ≤ 2 ✓           │ 1           │
 │ "ec"     │ {e:1, c:1}       │ 2 ≤ 2 ✓           │ 2           │
 │ "ece"    │ {e:2, c:1}       │ 2 ≤ 2 ✓           │ 3           │
 │ "eceb"   │ {e:2, c:1, b:1}  │ 3 > 2 ✗ → shrink  │ 3           │
 │ "ceb"    │ {c:1, e:1, b:1}  │ 3 > 2 ✗ → shrink  │ 3           │
 │ "eb"     │ {e:1, b:1}       │ 2 ≤ 2 ✓           │ 3           │
 │ "eba"    │ {e:1, b:1, a:1}  │ 3 > 2 ✗ → shrink  │ 3           │
 └──────────┴──────────────────┴────────────────────┴─────────────┘

 OUTPUT: 3 (substring "ece")
```

### Complexity Summary

```
 ┌─────────────────────────────────────────┬────────────┬──────────┐
 │ Problem                                 │ Time       │ Space    │
 ├─────────────────────────────────────────┼────────────┼──────────┤
 │ Frequency Count                         │ O(n)       │ O(n)     │
 │ Group by Frequency                      │ O(n)       │ O(n)     │
 │ Sort by Frequency                       │ O(n log n) │ O(n)     │
 │ Top K Frequent (heap)                   │ O(n log k) │ O(n)     │
 │ Top K Frequent (bucket)                 │ O(n)       │ O(n)     │
 │ Max Frequency Char                      │ O(n)       │ O(k)     │
 │ Distinct in Windows                     │ O(n)       │ O(k)     │
 │ First Non-Repeating (stream)            │ O(n)       │ O(k)     │
 │ Find Duplicates (neg marking)           │ O(n)       │ O(1)     │
 │ Longest Substring K Distinct            │ O(n)       │ O(k)     │
 └─────────────────────────────────────────┴────────────┴──────────┘
```

```python
from collections import Counter, defaultdict

# Problem: Frequency of Most Frequent Element (LeetCode 1838)
def max_frequency(nums, k):
    """Find max frequency of any element after at most k operations"""
    nums.sort()
    left = 0
    total = 0
    result = 0
    
    for right in range(len(nums)):
        total += nums[right]
        
        while (right - left + 1) * nums[right] - total > k:
            total -= nums[left]
            left += 1
        
        result = max(result, right - left + 1)
    
    return result

# Problem: Kth Most Frequent Character
def kth_most_frequent(s, k):
    """Find kth most frequent character"""
    freq = Counter(s)
    sorted_chars = sorted(freq.items(), key=lambda x: -x[1])
    
    if k <= len(sorted_chars):
        return sorted_chars[k - 1][0]
    return None

# Problem: Longest Substring with At Most K Distinct Characters
def longest_substring_k_distinct(s, k):
    """Find longest substring with at most k distinct characters"""
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
print(max_frequency([1, 2, 4], 5))  # 3
print(kth_most_frequent("abracadabra", 2))  # 'a' or 'b' (depends on tie-breaking)
print(longest_substring_k_distinct("eceba", 2))  # 3
```
