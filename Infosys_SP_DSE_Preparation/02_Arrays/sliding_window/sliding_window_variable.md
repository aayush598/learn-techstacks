# Variable Size Sliding Window

## Template

```python
def variable_window(arr, condition):
    left = 0
    result = 0
    window_state = ...  # sum, count, frequency map, etc.
    
    for right in range(len(arr)):
        # EXPAND: add arr[right] to window
        window_state += arr[right]  # or update map
        
        # SHRINK: while window violates condition
        while window_invalid(window_state):
            window_state -= arr[left]  # or update map
            left += 1
        
        # UPDATE: record result from valid window
        result = max(result, right - left + 1)
    
    return result
```

---

## When to Expand vs When to Shrink

| Situation | Expand | Shrink |
|-----------|--------|--------|
| Looking for longest | `right` moves right | `while` condition violated |
| Looking for shortest | `right` moves right | `while` condition met |
| Sum < target | Always expand | Never shrink |
| Sum > target | Still expand | Shrink from left |
| Distinct chars > k | Still expand | Shrink until <= k |

**Key rule:** Expand with `for right`, shrink with `while left < right`.

---

## 1. Minimum Size Subarray Sum (LeetCode 209)

**Problem:** Find minimal length of subarray with sum >= target (positive integers).

```python
def min_sub_array_len(target, nums):
    left = 0
    current_sum = 0
    min_len = float('inf')
    
    for right in range(len(nums)):
        current_sum += nums[right]
        
        while current_sum >= target:
            min_len = min(min_len, right - left + 1)
            current_sum -= nums[left]
            left += 1
    
    return min_len if min_len != float('inf') else 0

# Example: target=7, nums=[2,3,1,2,4,3]
# r=0: sum=2 < 7
# r=1: sum=5 < 7
# r=2: sum=6 < 7
# r=3: sum=8 >= 7, min_len=4, shrink: sum=6 < 7
# r=4: sum=10 >= 7, min_len=4, shrink: sum=6 < 7
# r=5: sum=9 >= 7, min_len=3, shrink: sum=5 < 7
# Result: 3 ([4,3].. wait [2,4,3])
# Time: O(n), Space: O(1)
```

---

## 2. Longest Substring with At Most K Distinct Characters

```python
def longest_substring_k(s, k):
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

## 3. Maximum Length Subarray with Sum <= K (positive numbers)

```python
def max_length_subarray_sum(arr, k):
    left = 0
    current_sum = 0
    max_len = 0
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum > k:
            current_sum -= arr[left]
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
# Time: O(n), Space: O(1)
# Only works with positive numbers
```

---

## 4. Subarray Product Less Than K (LeetCode 713)

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
        
        # All subarrays ending at 'right' with start from left to right
        # are valid: [left..right], [left+1..right], ..., [right..right]
        count += right - left + 1
    
    return count
# Example: nums=[10,5,2,6], k=100
# r=0: prod=10, count+=1 (subarray [10])
# r=1: prod=50, count+=2 ([5], [10,5])
# r=2: prod=100 >= 100, shrink: prod=10, left=2, count+=1 ([2])
# r=3: prod=60, count+=2 ([6], [2,6])
# Total: 6
# Time: O(n), Space: O(1)
```

---

## 5. Subarray Sum Equals K (LeetCode 560)

```python
def subarray_sum(nums, k):
    from collections import defaultdict
    prefix_count = defaultdict(int)
    prefix_count[0] = 1
    current_sum = 0
    count = 0
    
    for num in nums:
        current_sum += num
        # If (current_sum - k) was seen before, those subarrays sum to k
        if current_sum - k in prefix_count:
            count += prefix_count[current_sum - k]
        prefix_count[current_sum] += 1
    
    return count
# This uses prefix sum + hash map, not pure sliding window
# (sliding window only works for positive numbers)
# Time: O(n), Space: O(n)
```

---

## 6. Max Consecutive Ones III (LeetCode 1004)

**Problem:** Find max consecutive 1s if you can flip at most k zeros.

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
# Example: nums=[1,1,1,0,0,0,1,1,1,1,0], k=2
# Window expands until 3rd zero, then shrinks
# Max window with <= 2 zeros = 6
# Time: O(n), Space: O(1)
```

---

## 7. Binary Subarrays with Sum (LeetCode 930)

**Problem:** Number of subarrays with sum equal to target (binary array).

```python
def num_subarrays_with_sum(nums, goal):
    from collections import defaultdict
    
    prefix_count = defaultdict(int)
    prefix_count[0] = 1
    current_sum = 0
    count = 0
    
    for num in nums:
        current_sum += num
        if current_sum - goal in prefix_count:
            count += prefix_count[current_sum - goal]
        prefix_count[current_sum] += 1
    
    return count
# Time: O(n), Space: O(n)
```

---

## 8. Count Subarrays with Exactly K Different Elements (LeetCode 992)

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
# exactly(k) = at_most(k) - at_most(k-1)
# Time: O(n), Space: O(k)
```

---

## 9. Longest Substring with Same Letters After Replacement (LeetCode 424)

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
        
        # Window size - max_freq = number of chars to replace
        while (right - left + 1) - max_freq > k:
            count[s[left]] -= 1
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
# Example: s="AABABBA", k=1
# Window "AABAB" has max_freq=3, size=5, need replace=2 > k=1, shrink
# Time: O(n), Space: O(1) - 26 letters
```

---

## Variable Window Template (Complete)

```python
def variable_window_template(arr, condition_fn, result_fn):
    """
    condition_fn(window_state) -> True if window is valid
    result_fn(window_state, window_size) -> value to track
    """
    left = 0
    window_state = init_state()
    result = init_result()
    
    for right in range(len(arr)):
        # Expand
        add_to_state(arr[right])
        
        # Shrink while invalid
        while not condition_fn(window_state):
            remove_from_state(arr[left])
            left += 1
        
        # Update result
        result = result_fn(result, window_state, right - left + 1)
    
    return result

# Concrete example: longest subarray with sum <= k
def longest_subarray_sum_at_most_k(arr, k):
    left = 0
    current_sum = 0
    max_len = 0
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum > k:  # Shrink while invalid
            current_sum -= arr[left]
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

---

## Summary: Variable Window Checklist

1. **Initialize**: left=0, window_state, result
2. **Expand**: Add `arr[right]` to state (for loop)
3. **Shrink**: `while` condition violated, remove `arr[left]`, left++
4. **Record**: Update result after each valid window
5. **Positive numbers only?** Can shrink when sum > target
6. **Negative numbers?** Use prefix sum + hash map instead
7. **Exactly K?** = at_most(K) - at_most(K-1)
