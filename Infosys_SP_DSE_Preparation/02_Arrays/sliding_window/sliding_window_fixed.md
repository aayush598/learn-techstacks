# Fixed Size Sliding Window

## Template

```python
def fixed_window(arr, k):
    # Compute first window
    window_sum = sum(arr[:k])
    result = window_sum  # or max/min
    
    # Slide the window
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]  # Add new, remove old
        result = max(result, window_sum)    # or min, or collect
    
    return result
# Time: O(n), Space: O(1)
```

---

## 1. Maximum Sum Subarray of Size K

```python
def max_sum_subarray_k(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum

# Example: arr=[2,1,5,1,3,2], k=3
# Window 1: [2,1,5] = 8
# Window 2: [1,5,1] = 7
# Window 3: [5,1,3] = 9  <-- max
# Window 4: [1,3,2] = 6
# Time: O(n), Space: O(1)
```

---

## 2. Max/Min of All Subarrays of Size K (Using Deque)

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()  # Stores indices, front = max of window
    result = []
    
    for i in range(len(nums)):
        # Remove indices outside current window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements from back (they're useless)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        dq.append(i)
        
        # Window is complete after processing k-1 elements
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

# Example: nums=[1,3,-1,-3,5,3,6,7], k=3
# i=0: dq=[0] (val=1)
# i=1: dq=[1] (val=3, popped 0 since 1<3)
# i=2: dq=[1,2] (val=-1), window complete -> result=[3]
# i=3: dq=[1,2,3], remove dq[0] if < 1 -> dq=[2,3], remove <-3 < -3? no
#        window complete -> result=[3,3]
# ... and so on
# Time: O(n), Space: O(k)

# For minimum, just reverse the comparison:
def min_sliding_window(nums, k):
    dq = deque()
    result = []
    for i in range(len(nums)):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] > nums[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

---

## 3. Count Anagrams (LeetCode 438 - Permutation in String)

```python
from collections import Counter

def count_anagrams(s, pattern):
    p_count = Counter(pattern)
    k = len(pattern)
    result = []
    
    # Build first window
    window_count = Counter(s[:k])
    if window_count == p_count:
        result.append(0)
    
    # Slide window
    for i in range(k, len(s)):
        # Add new character
        window_count[s[i]] += 1
        # Remove old character
        old_char = s[i - k]
        window_count[old_char] -= 1
        if window_count[old_char] == 0:
            del window_count[old_char]
        
        if window_count == p_count:
            result.append(i - k + 1)
    
    return len(result)

# Time: O(n * 26) = O(n), Space: O(1) - alphabet is constant
```

---

## 4. Permutation in String (LeetCode 567)

```python
def check_inclusion(s1, s2):
    if len(s1) > len(s2):
        return False
    
    from collections import Counter
    s1_count = Counter(s1)
    window_count = Counter()
    
    for i in range(len(s2)):
        window_count[s2[i]] += 1
        
        if i >= len(s1):
            old = s2[i - len(s1)]
            window_count[old] -= 1
            if window_count[old] == 0:
                del window_count[old]
        
        if window_count == s1_count:
            return True
    return False
# Time: O(n), Space: O(1) - 26 letters
```

---

## 5. Minimum Window Substring (LeetCode 76)

```python
def min_window(s, t):
    from collections import Counter
    
    if not t or not s:
        return ""
    
    t_count = Counter(t)
    required = len(t_count)
    formed = 0
    
    window_counts = {}
    l, r = 0, 0
    ans = float('inf'), None, None  # (window_len, left, right)
    
    while r < len(s):
        char = s[r]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        if char in t_count and window_counts[char] == t_count[char]:
            formed += 1
        
        # Try to shrink from left
        while formed == required:
            if r - l + 1 < ans[0]:
                ans = (r - l + 1, l, r)
            
            left_char = s[l]
            window_counts[left_char] -= 1
            if left_char in t_count and window_counts[left_char] < t_count[left_char]:
                formed -= 1
            l += 1
        
        r += 1
    
    return "" if ans[0] == float('inf') else s[ans[1]:ans[2] + 1]
# Time: O(|s| + |t|), Space: O(|s| + |t|)
```

---

## 6. Longest Substring Without Repeating Characters (LeetCode 3)

```python
def length_of_longest_substring(s):
    char_index = {}  # char -> last seen index
    max_len = 0
    left = 0
    
    for right in range(len(s)):
        if s[right] in char_index and char_index[s[right]] >= left:
            left = char_index[s[right]] + 1
        char_index[s[right]] = right
        max_len = max(max_len, right - left + 1)
    
    return max_len

# Example: s = "abcabcbb"
# r=0: a, max=1
# r=1: b, max=2
# r=2: c, max=3
# r=3: a (seen at 0 >= left=0), left=1, max=3
# r=4: b (seen at 1 >= left=1), left=2, max=3
# ...
# Time: O(n), Space: O(min(n, charset))

# Variant with sliding window (easier to understand):
def length_of_longest_substring_v2(s):
    char_set = set()
    left = 0
    max_len = 0
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)
    return max_len
```

---

## 7. Longest Substring with At Most K Distinct Characters

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
        
        while len(window) > k:
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
# Time: O(n), Space: O(k)
```

---

## 8. Subarrays with K Different Integers (LeetCode 992)

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
            result += right - left + 1
        return result
    
    return at_most(k) - at_most(k - 1)
# Time: O(n), Space: O(k)
# Key insight: exactly(k) = at_most(k) - at_most(k-1)
```

---

## Fixed Window Template with Deque

```python
from collections import deque

def fixed_window_deque(arr, k):
    dq = deque()
    result = []
    
    for i in range(len(arr)):
        # Remove out-of-window elements from front
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Process current element (add/remove based on problem)
        while dq and arr[dq[-1]] < arr[i]:
            dq.pop()
        dq.append(i)
        
        # Record result when window is complete
        if i >= k - 1:
            result.append(arr[dq[0]])
    
    return result

# When to use deque with fixed window:
# - Need min/max of each window (monotonic deque)
# - Need to maintain order of elements
# - Need to quickly remove expired elements
```

---

## Summary: Fixed Window Checklist

1. **Identify window size** `k`
2. **Compute first window** (manually or with loop)
3. **Slide window**: add `arr[i]`, remove `arr[i-k]`
4. **Track result**: max, min, count, or pattern match
5. **For min/max per window**: use monotonic deque
6. **For character counting**: use `Counter` or array of size 26
