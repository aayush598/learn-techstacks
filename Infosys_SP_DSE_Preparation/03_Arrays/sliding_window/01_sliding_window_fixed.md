# Fixed Size Sliding Window - Complete Guide

## What is Sliding Window?

Sliding window is a technique where you maintain a **window** (subarray) and slide it across the array.

**When to use:**
- Find subarray/substring of fixed size k
- Find longest/shortest subarray with condition
- Character frequency problems
- Maximum/minimum in subarrays

---

## Template for Fixed Window

```python
def fixed_window(arr, k):
    # Step 1: Compute first window
    window_sum = sum(arr[:k])
    result = window_sum  # or max/min
    
    # Step 2: Slide the window
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]  # Add new, remove old
        result = max(result, window_sum)    # Update result
    
    return result
# Time: O(n), Space: O(1)
```

### Visual: Sliding Window of Size 3

```
Array: [2, 1, 5, 1, 3, 2]

Window 1: [2, 1, 5]   → sum = 8
           ─────
           
Window 2:    [1, 5, 1] → sum = 7
              ─────
              
Window 3:       [5, 1, 3] → sum = 9 ← MAX!
                 ─────
                 
Window 4:          [1, 3, 2] → sum = 6
                    ─────
```

**Key Insight:** When sliding, we only add ONE new element and remove ONE old element!

---

## Problem 1: Maximum Sum Subarray of Size K

**Statement:** Find maximum sum of any subarray of size k.

**Input:** arr = [2, 1, 5, 1, 3, 2], k = 3

### Step-by-Step Walkthrough:

```
Step 1: Compute first window [2, 1, 5]
        window_sum = 2 + 1 + 5 = 8
        max_sum = 8
        
        [2, 1, 5] | 1, 3, 2
         ─────
         window

Step 2: Slide window → add 1, remove 2
        window_sum = 8 + 1 - 2 = 7
        max_sum = max(8, 7) = 8
        
        2, [1, 5, 1] | 3, 2
           ─────

Step 3: Slide window → add 3, remove 1
        window_sum = 7 + 3 - 1 = 9
        max_sum = max(8, 9) = 9
        
        2, 1, [5, 1, 3] | 2
             ─────
             NEW MAX!

Step 4: Slide window → add 2, remove 5
        window_sum = 9 + 2 - 5 = 6
        max_sum = max(9, 6) = 9
        
        2, 1, 5, [1, 3, 2]
                  ─────

Result: 9 ✓
```

### The Code:
```python
def max_sum_subarray_k(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]  # Add new, remove old
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

**Time:** O(n) | **Space:** O(1)

---

## Problem 2: Max of All Subarrays of Size K (Monotonic Deque)

**Statement:** Find maximum in every window of size k.

**Input:** nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

### Why Use Deque?

**Naive approach:** Check all elements in each window → O(n×k)
**Better approach:** Use deque to track maximum → O(n)

### Visual Walkthrough:

```
nums = [1, 3, -1, -3, 5, 3, 6, 7], k=3

i=0: nums[0]=1
     deque: [0]  (indices)
     vals:  [1]
     
i=1: nums[1]=3
     3 > 1, so remove index 0
     deque: [1]
     vals:  [3]
     
i=2: nums[2]=-1
     -1 < 3, keep both
     deque: [1, 2]
     vals:  [3, -1]
     
     Window complete! Max = nums[deque[0]] = 3
     
i=3: nums[3]=-3
     First, remove index 1 if outside window (1 < 3-3+1=1? No)
     -3 < -1, keep both
     deque: [1, 2, 3]
     vals:  [3, -1, -3]
     
     Window complete! Max = 3

i=4: nums[4]=5
     Remove index 1 if outside window (1 < 4-3+1=2? Yes!)
     Remove index 1
     5 > -3, remove index 3
     5 > -1, remove index 2
     deque: [4]
     vals:  [5]
     
     Window complete! Max = 5

i=5: nums[5]=3
     3 < 5, keep both
     deque: [4, 5]
     vals:  [5, 3]
     
     Window complete! Max = 5

i=6: nums[6]=6
     Remove index 4 if outside window (4 < 6-3+1=4? No)
     6 > 3, remove index 5
     6 > 5, remove index 4
     deque: [6]
     vals:  [6]
     
     Window complete! Max = 6

i=7: nums[7]=7
     7 > 6, remove index 6
     deque: [7]
     vals:  [7]
     
     Window complete! Max = 7

Result: [3, 3, 5, 5, 6, 7]
```

### The Code:
```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()  # Stores indices, front = max of window
    result = []
    
    for i in range(len(nums)):
        # Remove indices outside current window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements from back (they're useless!)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        dq.append(i)
        
        # Window is complete after processing k-1 elements
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result
```

**Key Insight:** Deque maintains **decreasing order**. Front is always the maximum!

**Time:** O(n) | **Space:** O(k)

---

## Problem 3: Permutation in String

**Statement:** Check if s2 contains a permutation of s1.

**Input:** s1 = "ab", s2 = "eidbaooo"

### Visual Walkthrough:

```
s1 = "ab", s2 = "eidbaooo"
Target: {a:1, b:1}
Window size: 2

Window 1: "ei"
          {e:1, i:1} ≠ {a:1, b:1}

Window 2: "id"
          {i:1, d:1} ≠ {a:1, b:1}

Window 3: "db"
          {d:1, b:1} ≠ {a:1, b:1}

Window 4: "ba"
          {b:1, a:1} = {a:1, b:1} ✓ FOUND!

Return True
```

### The Code:
```python
def check_inclusion(s1, s2):
    if len(s1) > len(s2):
        return False
    
    from collections import Counter
    s1_count = Counter(s1)
    window_count = Counter()
    
    for i in range(len(s2)):
        # Add new character to window
        window_count[s2[i]] += 1
        
        # Remove old character if window is full
        if i >= len(s1):
            old = s2[i - len(s1)]
            window_count[old] -= 1
            if window_count[old] == 0:
                del window_count[old]
        
        # Check if window matches
        if window_count == s1_count:
            return True
    
    return False
```

**Time:** O(n) | **Space:** O(1) - 26 letters only

---

## Problem 4: Minimum Window Substring

**Statement:** Find minimum window in s containing all characters of t.

**Input:** s = "ADOBECODEBANC", t = "ABC"

### Visual Walkthrough:

```
s = "ADOBECODEBANC", t = "ABC"
Need: {A:1, B:1, C:1}

Expand right until we have all characters:
A D O B E C
↑           ↑
l           r
Window: "ADOBEC" (contains ABC!)
Now shrink from left to minimize:
 D O B E C → still has BC, but no A → stop

Continue expanding:
 D O B E C O D E B A N C
 ↑                     ↑
 l                   r
Window: "CODEBANC" (contains ABC!)
Shrink from left:
  O D E B A N C → no O needed, remove
  O → "DEBANC" → no D needed
  D → "EBANC" → no E needed
  E → "BANC" → has ABC!
  
Can we shrink more?
   "ANC" → no B → stop
  
Minimum window: "BANC" (length 4)
```

### The Code:
```python
def min_window(s, t):
    from collections import Counter
    
    if not t or not s:
        return ""
    
    t_count = Counter(t)
    required = len(t_count)  # Number of unique chars needed
    formed = 0               # Number of unique chars with required count
    
    window_counts = {}
    l, r = 0, 0
    ans = float('inf'), None, None  # (window_len, left, right)
    
    while r < len(s):
        # Add character at right to window
        char = s[r]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        # Check if this char's count matches requirement
        if char in t_count and window_counts[char] == t_count[char]:
            formed += 1
        
        # Try to shrink window from left
        while formed == required:
            # Update answer if smaller window found
            if r - l + 1 < ans[0]:
                ans = (r - l + 1, l, r)
            
            # Remove character at left from window
            left_char = s[l]
            window_counts[left_char] -= 1
            if left_char in t_count and window_counts[left_char] < t_count[left_char]:
                formed -= 1
            l += 1
        
        r += 1
    
    return "" if ans[0] == float('inf') else s[ans[1]:ans[2] + 1]
```

**Time:** O(|s| + |t|) | **Space:** O(|s| + |t|)

---

## Problem 5: Longest Substring Without Repeating Characters

**Statement:** Find length of longest substring without repeating characters.

**Input:** s = "abcabcbb"

### Visual Walkthrough:

```
s = "abcabcbb"

left=0, right=0: 'a'
  Window: "a", len=1, max_len=1
  
left=0, right=1: 'b'
  Window: "ab", len=2, max_len=2
  
left=0, right=2: 'c'
  Window: "abc", len=3, max_len=3
  
left=0, right=3: 'a' (repeat!)
  Remove 'a', left=1
  Window: "bca", len=3, max_len=3
  
left=1, right=4: 'b' (repeat!)
  Remove 'b', left=2
  Window: "cab", len=3, max_len=3
  
left=2, right=5: 'c' (repeat!)
  Remove 'c', left=3
  Window: "abc", len=3, max_len=3
  
left=3, right=6: 'b' (repeat!)
  Remove 'b', left=4
  Window: "cb", len=2, max_len=3
  
left=4, right=7: 'b' (repeat!)
  Remove 'c', left=5
  Remove 'b', left=6
  Window: "b", len=1, max_len=3

Result: 3 ✓
```

### The Code:
```python
def length_of_longest_substring(s):
    char_set = set()
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        # Shrink window until no duplicate
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current character
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

**Time:** O(n) | **Space:** O(min(n, charset))

---

## Problem 6: Longest Substring with At Most K Distinct Characters

**Input:** s = "eceba", k = 2

### Visual Walkthrough:

```
s = "eceba", k = 2

left=0, right=0: 'e'
  Window: {e:1}, distinct=1 ≤ 2 ✓
  len=1, max_len=1

left=0, right=1: 'c'
  Window: {e:1, c:1}, distinct=2 ≤ 2 ✓
  len=2, max_len=2

left=0, right=2: 'e'
  Window: {e:2, c:1}, distinct=2 ≤ 2 ✓
  len=3, max_len=3

left=0, right=3: 'b'
  Window: {e:2, c:1, b:1}, distinct=3 > 2 ✗
  Remove s[left]='e', left=1
  Window: {e:1, c:1, b:1}, distinct=3 > 2 ✗
  Remove s[left]='c', left=2
  Window: {e:1, b:1}, distinct=2 ≤ 2 ✓
  len=2, max_len=3

left=2, right=4: 'a'
  Window: {e:1, b:1, a:1}, distinct=3 > 2 ✗
  Remove s[left]='e', left=3
  Window: {b:1, a:1}, distinct=2 ≤ 2 ✓
  len=2, max_len=3

Result: 3 ✓ (substring "ece")
```

### The Code:
```python
def longest_substring_k_distinct(s, k):
    if k == 0:
        return 0
    
    from collections import Counter
    window = Counter()
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        window[s[right]] += 1
        
        # Shrink if too many distinct characters
        while len(window) > k:
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

**Time:** O(n) | **Space:** O(k)

---

## Problem 7: Subarrays with K Different Integers

**Statement:** Count subarrays with exactly k distinct integers.

**Key Insight:** exactly(k) = at_most(k) - at_most(k-1)

### The Code:
```python
def subarrays_with_k_distinct(nums, k):
    def at_most(k):
        from collections import Counter
        count = Counter()
        left = 0
        result = 0
        
        for right in range(len(nums)):
            count[nums[right]] += 1
            
            while len(count) > k:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]
                left += 1
            
            # All subarrays ending at right with at most k distinct
            result += right - left + 1
        
        return result
    
    return at_most(k) - at_most(k - 1)
```

### Why This Works:

```
at_most(3) = count of subarrays with ≤ 3 distinct
at_most(2) = count of subarrays with ≤ 2 distinct

exactly(3) = at_most(3) - at_most(2)
           = (≤3) - (≤2)
           = exactly 3
```

**Time:** O(n) | **Space:** O(k)

---

## Summary: Fixed Window Checklist

1. **Identify window size** `k`
2. **Compute first window** manually or with loop
3. **Slide window**: add `arr[i]`, remove `arr[i-k]`
4. **Track result**: max, min, count, or pattern match
5. **For min/max per window**: use monotonic deque
6. **For character counting**: use `Counter` or array of size 26

## Quick Reference

| Problem | Technique | Time | Space |
|---------|-----------|------|-------|
| Max sum subarray | Window sum | O(n) | O(1) |
| Max of each window | Monotonic deque | O(n) | O(k) |
| Permutation in string | Character count | O(n) | O(1) |
| Min window substring | Expand + Shrink | O(n) | O(n) |
| Longest no repeat | Set + Shrink | O(n) | O(n) |
| K distinct chars | Counter + Shrink | O(n) | O(k) |
| Exactly k distinct | at_most(k) - at_most(k-1) | O(n) | O(k) |

## When to Use Fixed vs Variable Window

**Fixed Window:**
- Window size is given (k)
- "Subarray of size k"
- "Every window of length k"

**Variable Window:**
- Window size changes
- "Longest/shortest subarray where..."
- "Find subarray with sum = target"
