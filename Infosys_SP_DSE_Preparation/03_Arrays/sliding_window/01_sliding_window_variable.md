# Variable Size Sliding Window - Complete Guide

## What is Variable Window?

Unlike fixed window (size k given), variable window **changes size** based on a condition.

**When to use:**
- "Longest subarray where..."
- "Shortest subarray with sum >= target"
- "At most k distinct characters"
- Window size is NOT given

---

## Template

```python
def variable_window(arr, condition):
    left = 0
    result = 0
    window_state = ...  # sum, count, frequency map, etc.
    
    for right in range(len(arr)):
        # EXPAND: add arr[right] to window
        window_state += arr[right]
        
        # SHRINK: while window violates condition
        while window_invalid(window_state):
            window_state -= arr[left]
            left += 1
        
        # UPDATE: record result from valid window
        result = max(result, right - left + 1)
    
    return result
```

### Visual: Variable Window in Action

```
arr = [1, 2, 3, 1, 1, 1], k = 3 (sum constraint)

Window expands until sum > k, then shrinks:

[1, 2, 3, 1, 1, 1]
 ↑
 l, r=0: sum=1 ≤ 3, len=1

[1, 2, 3, 1, 1, 1]
 ↑  ↑
 l  r=1: sum=3 ≤ 3, len=2

[1, 2, 3, 1, 1, 1]
 ↑     ↑
 l  r=2: sum=6 > 3, SHRINK!

   [2, 3, 1, 1, 1]
    ↑     ↑
    l  r=2: sum=6 > 3, SHRINK!
   
      [3, 1, 1, 1]
       ↑     ↑
       l  r=2: sum=4 > 3, SHRINK!
   
         [1, 1, 1]
          ↑     ↑
          l  r=2: sum=3 ≤ 3, len=1

... and so on
```

---

## When to Expand vs When to Shrink

| Situation | Expand | Shrink |
|-----------|--------|--------|
| Looking for longest | `right` moves right | `while` condition violated |
| Looking for shortest | `right` moves right | `while` condition met |
| Sum < target | Always expand | Never shrink |
| Sum > target | Still expand | Shrink from left |
| Distinct chars > k | Still expand | Shrink until ≤ k |

**Key rule:** Expand with `for right`, shrink with `while left < right`.

---

## Problem 1: Minimum Size Subarray Sum

**Statement:** Find minimal length of subarray with sum ≥ target.

**Input:** target = 7, nums = [2, 3, 1, 2, 4, 3]

### Step-by-Step Walkthrough:

```
target = 7, nums = [2, 3, 1, 2, 4, 3]

right=0: add 2, sum=2 < 7
         [2] 3 1 2 4 3
          ↑
          l,r

right=1: add 3, sum=5 < 7
         [2 3] 1 2 4 3
          ↑  ↑
          l  r

right=2: add 1, sum=6 < 7
         [2 3 1] 2 4 3
          ↑     ↑
          l     r

right=3: add 2, sum=8 ≥ 7 ✓
         [2 3 1 2] 4 3
          ↑        ↑
          l        r
         min_len = 4
         
         SHRINK: remove 2, sum=6 < 7
            [3 1 2] 4 3
             ↑     ↑
             l     r

right=4: add 4, sum=10 ≥ 7 ✓
            [3 1 2 4] 3
             ↑        ↑
             l        r
            min_len = min(4, 4) = 4
            
            SHRINK: remove 3, sum=7 ≥ 7 ✓
               [1 2 4] 3
                ↑     ↑
                l     r
               min_len = min(4, 3) = 3
               
               SHRINK: remove 1, sum=6 < 7
                  [2 4] 3
                   ↑  ↑
                   l  r

right=5: add 3, sum=9 ≥ 7 ✓
                  [2 4 3]
                   ↑     ↑
                   l     r
                  min_len = min(3, 3) = 3
                  
                  SHRINK: remove 2, sum=7 ≥ 7 ✓
                     [4 3]
                      ↑ ↑
                      l r
                     min_len = min(3, 2) = 2
                     
                     SHRINK: remove 4, sum=3 < 7
                        [3]
                         ↑
                        l,r

Result: 2 ✓ (subarray [4, 3])
```

### The Code:
```python
def min_sub_array_len(target, nums):
    left = 0
    current_sum = 0
    min_len = float('inf')
    
    for right in range(len(nums)):
        current_sum += nums[right]
        
        # Shrink while condition met (sum >= target)
        while current_sum >= target:
            min_len = min(min_len, right - left + 1)
            current_sum -= nums[left]
            left += 1
    
    return min_len if min_len != float('inf') else 0
```

**Time:** O(n) | **Space:** O(1)

---

## Problem 2: Longest Substring with At Most K Distinct Characters

**Statement:** Find length of longest substring with at most k distinct characters.

**Input:** s = "eceba", k = 2

### Step-by-Step Walkthrough:

```
s = "eceba", k = 2

right=0: 'e', window={e:1}, distinct=1 ≤ 2 ✓
         [e] c e b a
          ↑
          l,r
         max_len = 1

right=1: 'c', window={e:1,c:1}, distinct=2 ≤ 2 ✓
         [e c] e b a
          ↑ ↑
          l r
         max_len = 2

right=2: 'e', window={e:2,c:1}, distinct=2 ≤ 2 ✓
         [e c e] b a
          ↑   ↑
          l   r
         max_len = 3

right=3: 'b', window={e:2,c:1,b:1}, distinct=3 > 2 ✗
         SHRINK!
         [e c e b] a → remove 'e', left=1
          [c e b] a → distinct=3 > 2, remove 'c', left=2
           [e b] a → distinct=2 ≤ 2 ✓
            ↑  ↑
            l  r
         max_len = max(3, 2) = 3

right=4: 'a', window={e:1,b:1,a:1}, distinct=3 > 2 ✗
         SHRINK!
         [e b a] → remove 'e', left=3
          [b a] → distinct=2 ≤ 2 ✓
           ↑ ↑
           l r
         max_len = max(3, 2) = 3

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

## Problem 3: Subarray Product Less Than K

**Statement:** Count subarrays where product of all elements is less than k.

**Input:** nums = [10, 5, 2, 6], k = 100

### Step-by-Step Walkthrough:

```
nums = [10, 5, 2, 6], k = 100

right=0: product=10 < 100 ✓
         [10] 5 2 6
          ↑
          l,r
         count += 1 (subarray [10])

right=1: product=50 < 100 ✓
         [10 5] 2 6
          ↑  ↑
          l  r
         count += 2 (subarrays [5], [10,5])

right=2: product=100 ≥ 100 ✗
         SHRINK!
         [10 5 2] → remove 10, left=1
          [5 2] → product=10 < 100 ✓
           ↑ ↑
           l r
         count += 1 (subarray [2])

right=3: product=60 < 100 ✓
         [5 2 6]
          ↑   ↑
          l   r
         count += 2 (subarrays [6], [2,6])

Total count: 1 + 2 + 1 + 2 = 6
```

### Why count += right - left + 1?

```
For window [left..right], all subarrays ending at right are valid:
[left..right], [left+1..right], ..., [right..right]

Number of such subarrays = right - left + 1
```

### The Code:
```python
def num_subarray_product_less_than_k(nums, k):
    if k <= 1:
        return 0
    
    left = 0
    product = 1
    count = 0
    
    for right in range(len(nums)):
        product *= nums[right]
        
        while product >= k:
            product //= nums[left]
            left += 1
        
        count += right - left + 1
    
    return count
```

**Time:** O(n) | **Space:** O(1)

---

## Problem 4: Subarray Sum Equals K

**Statement:** Find number of subarrays with sum equal to k.

**Input:** nums = [1, 1, 1], k = 2

### Key Insight: Prefix Sum + Hash Map

```
If prefix_sum[j] - prefix_sum[i] = k
Then subarray [i+1..j] has sum k!

So for each j, count how many i's have prefix_sum[i] = prefix_sum[j] - k
```

### Step-by-Step Walkthrough:

```
nums = [1, 1, 1], k = 2

prefix_count = {0: 1}

num=1: current_sum = 1
       Check: 1 - 2 = -1 in prefix_count? No
       prefix_count = {0: 1, 1: 1}

num=1: current_sum = 2
       Check: 2 - 2 = 0 in prefix_count? Yes! (count=1)
       count += 1
       prefix_count = {0: 1, 1: 1, 2: 1}

num=1: current_sum = 3
       Check: 3 - 2 = 1 in prefix_count? Yes! (count=1)
       count += 1
       prefix_count = {0: 1, 1: 1, 2: 1, 3: 1}

Total count: 2 ✓ (subarrays [1,1] at indices 0-1 and [1,1] at indices 1-2)
```

### The Code:
```python
def subarray_sum(nums, k):
    from collections import defaultdict
    prefix_count = defaultdict(int)
    prefix_count[0] = 1
    current_sum = 0
    count = 0
    
    for num in nums:
        current_sum += num
        if current_sum - k in prefix_count:
            count += prefix_count[current_sum - k]
        prefix_count[current_sum] += 1
    
    return count
```

**Time:** O(n) | **Space:** O(n)

---

## Problem 5: Max Consecutive Ones III

**Statement:** Find max consecutive 1s if you can flip at most k zeros.

**Input:** nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2

### Step-by-Step Walkthrough:

```
nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2

right=0: 1, zeros=0 ≤ 2 ✓
         [1] 1 1 0 0 0 1 1 1 1 0
          ↑
          l,r
         max_len = 1

right=1: 1, zeros=0 ≤ 2 ✓
         [1 1] 1 0 0 0 1 1 1 1 0
          ↑  ↑
          l  r
         max_len = 2

right=2: 1, zeros=0 ≤ 2 ✓
         [1 1 1] 0 0 0 1 1 1 1 0
          ↑     ↑
          l     r
         max_len = 3

right=3: 0, zeros=1 ≤ 2 ✓
         [1 1 1 0] 0 0 1 1 1 1 0
          ↑        ↑
          l        r
         max_len = 4

right=4: 0, zeros=2 ≤ 2 ✓
         [1 1 1 0 0] 0 1 1 1 1 0
          ↑           ↑
          l           r
         max_len = 5

right=5: 0, zeros=3 > 2 ✗
         SHRINK!
         [1 1 1 0 0 0] → remove 1, left=1
          [1 1 0 0 0] → zeros=3 > 2, remove 1, left=2
           [1 0 0 0] → zeros=3 > 2, remove 1, left=3
            [0 0 0] → zeros=3 > 2, remove 0, left=4
             [0 0] → zeros=2 ≤ 2 ✓
              ↑ ↑
              l r
         max_len = max(5, 2) = 5

... continuing this process...

Maximum window with ≤ 2 zeros has length 6
```

### The Code:
```python
def longest_ones(nums, k):
    left = 0
    max_len = 0
    zeros = 0
    
    for right in range(len(nums)):
        if nums[right] == 0:
            zeros += 1
        
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

**Time:** O(n) | **Space:** O(1)

---

## Problem 6: Longest Substring with Same Letters After Replacement

**Statement:** Find longest substring where you can replace at most k characters to make all same.

**Input:** s = "AABABBA", k = 1

### Key Insight:

```
Window is valid if: window_size - max_freq ≤ k

Where max_freq = most frequent character in window
```

### Step-by-Step Walkthrough:

```
s = "AABABBA", k = 1

right=0: 'A', window={A:1}, max_freq=1
         [A] A B A B B A
          ↑
          l,r
         size=1, need_replace = 1-1 = 0 ≤ 1 ✓
         max_len = 1

right=1: 'A', window={A:2}, max_freq=2
         [A A] B A B B A
          ↑  ↑
          l  r
         size=2, need_replace = 2-2 = 0 ≤ 1 ✓
         max_len = 2

right=2: 'B', window={A:2,B:1}, max_freq=2
         [A A B] A B B A
          ↑     ↑
          l     r
         size=3, need_replace = 3-2 = 1 ≤ 1 ✓
         max_len = 3

right=3: 'A', window={A:3,B:1}, max_freq=3
         [A A B A] B B A
          ↑        ↑
          l        r
         size=4, need_replace = 4-3 = 1 ≤ 1 ✓
         max_len = 4

right=4: 'B', window={A:3,B:2}, max_freq=3
         [A A B A B] B A
          ↑           ↑
          l           r
         size=5, need_replace = 5-3 = 2 > 1 ✗
         SHRINK!
         remove A, left=1, window={A:2,B:2}
         size=4, need_replace = 4-2 = 2 > 1 ✗
         SHRINK!
         remove A, left=2, window={A:1,B:2}, max_freq=2
         size=3, need_replace = 3-2 = 1 ≤ 1 ✓
         max_len = max(4, 3) = 4

... and so on

Result: 4 ✓
```

### The Code:
```python
def character_replacement(s, k):
    from collections import Counter
    count = Counter()
    left = 0
    max_freq = 0
    max_len = 0
    
    for right in range(len(s)):
        count[s[right]] += 1
        max_freq = max(max_freq, count[s[right]])
        
        # Window size - max_freq = chars to replace
        while (right - left + 1) - max_freq > k:
            count[s[left]] -= 1
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

**Time:** O(n) | **Space:** O(1) - 26 letters only

---

## Summary: Variable Window Checklist

1. **Initialize**: left=0, window_state, result
2. **Expand**: Add `arr[right]` to state (for loop)
3. **Shrink**: `while` condition violated, remove `arr[left]`, left++
4. **Record**: Update result after each valid window

## Quick Reference

| Problem | Window State | Shrink When | Time |
|---------|--------------|-------------|------|
| Min size sum ≥ k | current_sum | sum ≥ target | O(n) |
| K distinct chars | Counter | len(counter) > k | O(n) |
| Product < k | product | product ≥ k | O(n) |
| Subarray sum = k | prefix_sum | (use hash map) | O(n) |
| Max consecutive ones | zeros count | zeros > k | O(n) |
| Same letters after replacement | max_freq | size - max_freq > k | O(n) |

## Fixed vs Variable Window

| Aspect | Fixed Window | Variable Window |
|--------|--------------|-----------------|
| Window size | Given (k) | Changes |
| Template | Sum first k, then slide | Expand with for, shrink with while |
| Example | "Max sum subarray of size k" | "Longest with sum ≤ k" |
| Negative numbers | Works | Works |
| Time | O(n) | O(n) |
