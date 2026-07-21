# Complete Prefix Sum Guide

## What is Prefix Sum?

Prefix sum is a technique where you precompute cumulative sums to answer **range sum queries** in O(1) after O(n) preprocessing.

```
arr     = [2, 4, 1, 3, 5]
prefix  = [0, 2, 6, 7, 10, 15]
          ^  ^  ^  ^   ^   ^
          0  1  2  3   4   5
prefix[i] = sum of arr[0..i-1]
```

**When to use:**
- Multiple range sum queries on same array
- Subarray sum problems
- Difference array (inverse of prefix sum)
- 2D range queries

---

## 1. Static Prefix Sum (1D)

```python
def build_prefix(arr):
    prefix = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix

def range_sum(prefix, left, right):
    """Sum of arr[left..right] inclusive."""
    return prefix[right + 1] - prefix[left]

# Example
arr = [2, 4, 1, 3, 5]
prefix = build_prefix(arr)
# prefix = [0, 2, 6, 7, 10, 15]

# Sum of arr[1..3] = 4+1+3 = 8
print(range_sum(prefix, 1, 3))  # prefix[4] - prefix[1] = 10 - 2 = 8

# Time: Build O(n), Query O(1)
# Space: O(n)
```

---

## 2. Range Sum Query (LeetCode 303)

```python
class NumArray:
    def __init__(self, nums):
        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)
    
    def sumRange(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]
# O(1) per query after O(n) preprocessing
```

---

## 3. 2D Prefix Sum (Matrix Prefix Sum)

```python
def build_2d_prefix(matrix):
    if not matrix:
        return []
    m, n = len(matrix), len(matrix[0])
    prefix = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m):
        for j in range(n):
            prefix[i + 1][j + 1] = (
                matrix[i][j]
                + prefix[i][j + 1]
                + prefix[i + 1][j]
                - prefix[i][j]
            )
    return prefix

def range_sum_2d(prefix, r1, c1, r2, c2):
    """Sum of submatrix from (r1,c1) to (r2,c2) inclusive."""
    return (
        prefix[r2 + 1][c2 + 1]
        - prefix[r1][c2 + 1]
        - prefix[r2 + 1][c1]
        + prefix[r1][c1]
    )

# Example:
# matrix = [[1,2,3],[4,5,6],[7,8,9]]
# prefix = [[0, 0,  0,  0,  0],
#           [0, 1,  3,  6,  0],
#           [0, 5, 12, 21,  0],
#           [0,12, 27, 45,  0]]
# Time: Build O(mn), Query O(1)
```

---

## 4. Subarray Sum Equals K (LeetCode 560)

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
# Key insight: prefix[j] - prefix[i] = k means arr[i+1..j] sums to k
# So for each j, count how many i have prefix[i] = prefix[j] - k
# Time: O(n), Space: O(n)
```

---

## 5. Product of Array Except Self (LeetCode 238)

```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    
    # Left products: result[i] = product of nums[0..i-1]
    left_product = 1
    for i in range(n):
        result[i] = left_product
        left_product *= nums[i]
    
    # Right products: multiply by product of nums[i+1..n-1]
    right_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]
    
    return result
# nums =     [1, 2, 3, 4]
# left prod: [1, 1, 2, 6]
# right prod:[24,12, 4, 1]
# result:    [24,12, 8, 6]
# Time: O(n), Space: O(1) - excluding output
```

---

## 6. Find Pivot Index (LeetCode 724)

```python
def pivot_index(nums):
    total = sum(nums)
    left_sum = 0
    
    for i in range(len(nums)):
        right_sum = total - left_sum - nums[i]
        if left_sum == right_sum:
            return i
        left_sum += nums[i]
    
    return -1
# Time: O(n), Space: O(1)
```

---

## 7. Range Sum Query 2D (LeetCode 304)

```python
class NumMatrix:
    def __init__(self, matrix):
        m, n = len(matrix), len(matrix[0])
        self.prefix = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                self.prefix[i + 1][j + 1] = (
                    matrix[i][j]
                    + self.prefix[i][j + 1]
                    + self.prefix[i + 1][j]
                    - self.prefix[i][j]
                )
    
    def sumRegion(self, r1, c1, r2, c2):
        return (
            self.prefix[r2 + 1][c2 + 1]
            - self.prefix[r1][c2 + 1]
            - self.prefix[r2 + 1][c1]
            + self.prefix[r1][c1]
        )
```

---

## 8. Continuous Subarray Sum Divisible by K (LeetCode 523)

```python
def check_subarray_sum(nums, k):
    from collections import defaultdict
    remainder_map = defaultdict(int)
    remainder_map[0] = -1
    prefix_sum = 0
    
    for i, num in enumerate(nums):
        prefix_sum += num
        remainder = prefix_sum % k
        
        if remainder in remainder_map:
            if i - remainder_map[remainder] >= 2:
                return True
        else:
            remainder_map[remainder] = i
    
    return False
# Key: if prefix[i] % k == prefix[j] % k and j - i >= 2
# then nums[i+1..j] is divisible by k
# Time: O(n), Space: O(k)
```

---

## 9. Find the Longest Substring with Equal 0s and 1s

```python
def find_longest_equal_substring(s):
    """Find longest substring with equal 0s and 1s."""
    # Treat 0 as -1, 1 as +1. Find longest subarray with sum 0.
    prefix_map = {0: -1}
    prefix_sum = 0
    max_len = 0
    start = 0
    
    for i, char in enumerate(s):
        prefix_sum += 1 if char == '1' else -1
        
        if prefix_sum in prefix_map:
            length = i - prefix_map[prefix_sum]
            if length > max_len:
                max_len = length
                start = prefix_map[prefix_sum] + 1
        else:
            prefix_map[prefix_sum] = i
    
    return s[start:start + max_len]
# Time: O(n), Space: O(n)
```

---

## 10. Range Update with Difference Array

```python
def range_add(queries, n):
    """Apply multiple range additions, return final array."""
    diff = [0] * (n + 1)
    
    for left, right, val in queries:
        diff[left] += val
        diff[right + 1] -= val
    
    # Prefix sum to get final array
    result = [0] * n
    result[0] = diff[0]
    for i in range(1, n):
        result[i] = result[i - 1] + diff[i]
    
    return result
# Time: O(n + q), Space: O(n)
```

---

## Quick Reference

| Problem | Technique | Time |
|---------|-----------|------|
| Range sum query | 1D prefix sum | O(1) query |
| Matrix range sum | 2D prefix sum | O(1) query |
| Subarray sum = k | Prefix + hash map | O(n) |
| Product except self | Left/right products | O(n) |
| Pivot index | Running sum | O(n) |
| Divisible by k | Remainder + hash map | O(n) |
| Range updates | Difference array | O(n+q) |
