# Complete Prefix Sum Guide - Detailed Version

## What is Prefix Sum?

Prefix sum is a technique where you precompute cumulative sums to answer **range sum queries** in O(1) after O(n) preprocessing.

### Visual: How Prefix Sum Works

```
Original Array:  arr = [2, 4, 1, 3, 5]
Index:             0   1  2  3  4

Prefix Sum:     prefix = [0, 2, 6, 7, 10, 15]
Index:              0  1  2  3   4   5

prefix[0] = 0 (empty prefix)
prefix[1] = 2 (sum of arr[0])
prefix[2] = 2+4 = 6 (sum of arr[0..1])
prefix[3] = 2+4+1 = 7 (sum of arr[0..2])
prefix[4] = 2+4+1+3 = 10 (sum of arr[0..3])
prefix[5] = 2+4+1+3+5 = 15 (sum of arr[0..4])
```

### Key Formula:

```
Sum of arr[left..right] = prefix[right+1] - prefix[left]

Example: Sum of arr[1..3] = 4+1+3 = 8
         prefix[4] - prefix[1] = 10 - 2 = 8 ✓
```

**Why it works:**
- `prefix[right+1]` = sum of all elements from start to right
- `prefix[left]` = sum of all elements before left
- Subtracting gives sum from left to right!

---

## 1. Static Prefix Sum (1D)

### The Code:
```python
def build_prefix(arr):
    """Build prefix sum array from original array."""
    n = len(arr)
    prefix = [0] * (n + 1)  # One extra element for prefix[0]
    
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    return prefix

def range_sum(prefix, left, right):
    """Get sum of arr[left..right] in O(1)."""
    return prefix[right + 1] - prefix[left]
```

### Visual Walkthrough: Build Prefix for [2, 4, 1, 3, 5]

```
Step 0: prefix = [0, 0, 0, 0, 0, 0]

Step 1: i=0, arr[0]=2
        prefix[1] = prefix[0] + 2 = 0 + 2 = 2
        prefix = [0, 2, 0, 0, 0, 0]

Step 2: i=1, arr[1]=4
        prefix[2] = prefix[1] + 4 = 2 + 4 = 6
        prefix = [0, 2, 6, 0, 0, 0]

Step 3: i=2, arr[2]=1
        prefix[3] = prefix[2] + 1 = 6 + 1 = 7
        prefix = [0, 2, 6, 7, 0, 0]

Step 4: i=3, arr[3]=3
        prefix[4] = prefix[3] + 3 = 7 + 3 = 10
        prefix = [0, 2, 6, 7, 10, 0]

Step 5: i=4, arr[4]=5
        prefix[5] = prefix[4] + 5 = 10 + 5 = 15
        prefix = [0, 2, 6, 7, 10, 15]

Final: prefix = [0, 2, 6, 7, 10, 15]
```

### Example Queries:

```
Query: Sum of arr[1..3] = 4+1+3 = 8
       prefix[4] - prefix[1] = 10 - 2 = 8 ✓

Query: Sum of arr[0..2] = 2+4+1 = 7
       prefix[3] - prefix[0] = 7 - 0 = 7 ✓

Query: Sum of arr[2..4] = 1+3+5 = 9
       prefix[5] - prefix[2] = 15 - 6 = 9 ✓
```

**Time:** Build O(n), Query O(1) | **Space:** O(n)

---

## 2. Range Sum Query (LeetCode 303)

**Statement:** Given an array, answer multiple queries about sum of elements between indices left and right.

**Example:**
```
nums = [-2, 0, 3, -5, 2, -1]
sumRange(0, 2) → 1 (=-2+0+3)
sumRange(2, 5) → -1 (=3-5+2-1)
sumRange(0, 5) → -3 (=-2+0+3-5+2-1)
```

### The Code:
```python
class NumArray:
    def __init__(self, nums):
        """Build prefix sum array."""
        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)
    
    def sumRange(self, left, right):
        """Return sum of nums[left..right]."""
        return self.prefix[right + 1] - self.prefix[left]

# Usage:
# arr = NumArray([-2, 0, 3, -5, 2, -1])
# arr.sumRange(0, 2)  # Returns 1
```

### Visual:

```
nums = [-2, 0, 3, -5, 2, -1]

Prefix: [0, -2, -2, 1, -4, -2, -3]
         0   1   2  3   4   5   6

sumRange(0, 2): prefix[3] - prefix[0] = 1 - 0 = 1
sumRange(2, 5): prefix[6] - prefix[2] = -3 - (-2) = -1
```

**Time:** Build O(n), Query O(1) | **Space:** O(n)

---

## 3. 2D Prefix Sum (Matrix Prefix Sum)

**Statement:** Given a matrix, answer multiple queries about sum of submatrix.

### Visual: 2D Prefix Sum

```
Original Matrix:        Prefix Sum Matrix:
[1, 2, 3]              [0,  0,  0,  0]
[4, 5, 6]              [0,  1,  3,  6]
[7, 8, 9]              [0,  5, 12, 21]
                        [0, 12, 27, 45]

prefix[i][j] = sum of all elements in rectangle (0,0) to (i-1,j-1)
```

### Formula:

```
Sum of submatrix (r1,c1) to (r2,c2):

        ┌─────────────────────┐
        │                     │
        │    ┌───────────┐    │
        │    │  TARGET   │    │
        │    │  (r1,c1)  │    │
        │    │     to    │    │
        │    │  (r2,c2)  │    │
        │    └───────────┘    │
        │                     │
        └─────────────────────┘

Sum = prefix[r2+1][c2+1]      (entire rectangle)
    - prefix[r1][c2+1]        (subtract top part)
    - prefix[r2+1][c1]        (subtract left part)
    + prefix[r1][c1]          (add back overlapping corner)
```

### The Code:
```python
def build_2d_prefix(matrix):
    """Build 2D prefix sum matrix."""
    if not matrix:
        return []
    m, n = len(matrix), len(matrix[0])
    prefix = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m):
        for j in range(n):
            prefix[i + 1][j + 1] = (
                matrix[i][j]
                + prefix[i][j + 1]      # top
                + prefix[i + 1][j]      # left
                - prefix[i][j]          # top-left (counted twice)
            )
    return prefix

def range_sum_2d(prefix, r1, c1, r2, c2):
    """Get sum of submatrix from (r1,c1) to (r2,c2)."""
    return (
        prefix[r2 + 1][c2 + 1]
        - prefix[r1][c2 + 1]
        - prefix[r2 + 1][c1]
        + prefix[r1][c1]
    )
```

### Visual Walkthrough: Sum of submatrix (1,1) to (2,2)

```
Matrix:
[1, 2, 3]
[4, 5, 6]  ← rows 1-2, cols 1-2
[7, 8, 9]  → target is [5,6,8,9]

Target sum = 5+6+8+9 = 28

Using formula:
prefix[3][3] = 45 (entire matrix)
prefix[1][3] = 6  (first row)
prefix[3][1] = 12 (first column)
prefix[1][1] = 1  (top-left corner)

Sum = 45 - 6 - 12 + 1 = 28 ✓
```

**Time:** Build O(m×n), Query O(1) | **Space:** O(m×n)

---

## 4. Subarray Sum Equals K (LeetCode 560)

**Statement:** Count number of subarrays with sum equal to k.

**Input:** nums = [1, 1, 1], k = 2
**Output:** 2 (subarrays [1,1] at indices 0-1 and [1,1] at indices 1-2)

### Key Insight:

```
If prefix[j] - prefix[i] = k
Then subarray nums[i+1..j] has sum k!

So for each j, count how many i's have prefix[i] = prefix[j] - k
```

### Visual Walkthrough:

```
nums = [1, 1, 1], k = 2

prefix_count = {0: 1}  # Start with prefix sum 0 seen once

Processing num=1:
  current_sum = 1
  Need: 1 - 2 = -1 in prefix_count? No
  Update: prefix_count = {0: 1, 1: 1}

Processing num=1:
  current_sum = 2
  Need: 2 - 2 = 0 in prefix_count? Yes! (count=1)
  count += 1
  Update: prefix_count = {0: 1, 1: 1, 2: 1}

Processing num=1:
  current_sum = 3
  Need: 3 - 2 = 1 in prefix_count? Yes! (count=1)
  count += 1
  Update: prefix_count = {0: 1, 1: 1, 2: 1, 3: 1}

Total count: 2 ✓
```

### The Code:
```python
def subarray_sum(nums, k):
    from collections import defaultdict
    prefix_count = defaultdict(int)
    prefix_count[0] = 1  # Empty prefix has sum 0
    current_sum = 0
    count = 0
    
    for num in nums:
        current_sum += num
        
        # Check if (current_sum - k) was seen before
        if current_sum - k in prefix_count:
            count += prefix_count[current_sum - k]
        
        # Record current prefix sum
        prefix_count[current_sum] += 1
    
    return count
```

**Time:** O(n) | **Space:** O(n)

---

## 5. Product of Array Except Self (LeetCode 238)

**Statement:** Return array where each element is product of all other elements (no division).

**Input:** nums = [1, 2, 3, 4]
**Output:** [24, 12, 8, 6]

### Visual Walkthrough:

```
nums = [1, 2, 3, 4]

Step 1: Calculate LEFT products
        result[i] = product of all elements to the LEFT of i
        
        i=0: no left elements → result[0] = 1
        i=1: left = [1] → result[1] = 1
        i=2: left = [1,2] → result[2] = 2
        i=3: left = [1,2,3] → result[3] = 6
        
        result = [1, 1, 2, 6]

Step 2: Calculate RIGHT products and multiply
        result[i] *= product of all elements to the RIGHT of i
        
        i=3: no right elements → result[3] = 6 × 1 = 6
        i=2: right = [4] → result[2] = 2 × 4 = 8
        i=1: right = [3,4] → result[1] = 1 × 12 = 12
        i=0: right = [2,3,4] → result[0] = 1 × 24 = 24
        
        result = [24, 12, 8, 6] ✓

Verification:
  result[0] = 2×3×4 = 24 ✓
  result[1] = 1×3×4 = 12 ✓
  result[2] = 1×2×4 = 8 ✓
  result[3] = 1×2×3 = 6 ✓
```

### The Code:
```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    
    # Step 1: Left products
    left_product = 1
    for i in range(n):
        result[i] = left_product
        left_product *= nums[i]
    
    # Step 2: Right products (multiply in-place)
    right_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]
    
    return result
```

**Time:** O(n) | **Space:** O(1) excluding output

---

## 6. Find Pivot Index (LeetCode 724)

**Statement:** Find index where sum of left elements equals sum of right elements.

**Input:** nums = [1, 7, 3, 6, 5, 6]
**Output:** 3 (index of value 6)

### Visual Walkthrough:

```
nums = [1, 7, 3, 6, 5, 6]
total = 28

i=0: left_sum=0, right_sum=28-0-1=27 → 0≠27
i=1: left_sum=1, right_sum=28-1-7=20 → 1≠20
i=2: left_sum=8, right_sum=28-8-3=17 → 8≠17
i=3: left_sum=11, right_sum=28-11-6=11 → 11=11 ✓ FOUND!

Pivot index = 3
Left: [1,7,3] = 11
Right: [5,6] = 11
```

### The Code:
```python
def pivot_index(nums):
    total = sum(nums)
    left_sum = 0
    
    for i in range(len(nums)):
        right_sum = total - left_sum - nums[i]
        
        if left_sum == right_sum:
            return i
        
        left_sum += nums[i]
    
    return -1  # No pivot found
```

**Time:** O(n) | **Space:** O(1)

---

## 7. Continuous Subarray Sum Divisible by K (LeetCode 523)

**Statement:** Check if array has a continuous subarray of length ≥ 2 that sums to a multiple of k.

**Input:** nums = [23, 2, 4, 6, 7], k = 6
**Output:** True (subarray [2,4] sums to 6)

### Key Insight:

```
If prefix[i] % k == prefix[j] % k
Then subarray nums[i+1..j] is divisible by k!

Because: (prefix[j] - prefix[i]) % k = 0
```

### Visual Walkthrough:

```
nums = [23, 2, 4, 6, 7], k = 6

remainder_map = {0: -1}

i=0, num=23: prefix_sum=23, remainder=23%6=5
             5 not in map → store {0:-1, 5:0}

i=1, num=2: prefix_sum=25, remainder=25%6=1
            1 not in map → store {0:-1, 5:0, 1:1}

i=2, num=4: prefix_sum=29, remainder=29%6=5
            5 in map! (index 0)
            Check length: 2 - 0 = 2 ≥ 2 ✓
            Return True!

Subarray: nums[1..2] = [2,4], sum = 6, divisible by 6 ✓
```

### The Code:
```python
def check_subarray_sum(nums, k):
    from collections import defaultdict
    remainder_map = defaultdict(int)
    remainder_map[0] = -1  # Handle case where prefix itself is divisible
    prefix_sum = 0
    
    for i, num in enumerate(nums):
        prefix_sum += num
        remainder = prefix_sum % k
        
        if remainder in remainder_map:
            # Check if subarray length ≥ 2
            if i - remainder_map[remainder] >= 2:
                return True
        else:
            remainder_map[remainder] = i
    
    return False
```

**Time:** O(n) | **Space:** O(k)

---

## 8. Difference Array (Range Updates)

**Statement:** Apply multiple range additions efficiently.

**Example:**
```
Array: [0, 0, 0, 0, 0] (size 5)
Queries: [(1,3,2), (2,4,1)]

After (1,3,2): add 2 to indices 1,2,3 → [0,2,2,2,0]
After (2,4,1): add 1 to indices 2,3,4 → [0,2,3,3,1]
```

### Visual Walkthrough:

```
Initial: arr = [0, 0, 0, 0, 0]
         diff = [0, 0, 0, 0, 0, 0]

Query (1,3,2): Add 2 to indices 1..3
  diff[1] += 2 → diff = [0, 2, 0, 0, 0, 0]
  diff[4] -= 2 → diff = [0, 2, 0, 0, -2, 0]

Query (2,4,1): Add 1 to indices 2..4
  diff[2] += 1 → diff = [0, 2, 1, 0, -2, 0]
  diff[5] -= 1 → diff = [0, 2, 1, 0, -2, -1]

Build result from diff:
  result[0] = diff[0] = 0
  result[1] = result[0] + diff[1] = 0 + 2 = 2
  result[2] = result[1] + diff[2] = 2 + 1 = 3
  result[3] = result[2] + diff[3] = 3 + 0 = 3
  result[4] = result[3] + diff[4] = 3 + (-2) = 1

Final: [0, 2, 3, 3, 1] ✓
```

### The Code:
```python
def range_add(queries, n):
    """Apply multiple range additions, return final array."""
    diff = [0] * (n + 1)
    
    # Mark range boundaries
    for left, right, val in queries:
        diff[left] += val        # Start of range
        diff[right + 1] -= val  # End of range + 1
    
    # Build result using prefix sum
    result = [0] * n
    result[0] = diff[0]
    for i in range(1, n):
        result[i] = result[i - 1] + diff[i]
    
    return result
```

**Why it works:**
- `diff[left] += val` starts the increment
- `diff[right+1] -= val` ends the increment
- Prefix sum propagates the values correctly!

**Time:** O(n + q) | **Space:** O(n)

---

## Quick Reference

| Problem | Technique | Time | Space |
|---------|-----------|------|-------|
| Range sum query | 1D prefix sum | Build O(n), Query O(1) | O(n) |
| Matrix range sum | 2D prefix sum | Build O(mn), Query O(1) | O(mn) |
| Subarray sum = k | Prefix + hash map | O(n) | O(n) |
| Product except self | Left/right products | O(n) | O(1) |
| Pivot index | Running sum | O(n) | O(1) |
| Divisible by k | Remainder + hash map | O(n) | O(k) |
| Range updates | Difference array | O(n+q) | O(n) |

## When to Use Prefix Sum

1. **Multiple range queries** - precompute once, answer many
2. **Subarray sum problems** - convert to prefix difference
3. **Range updates** - use difference array
4. **2D problems** - use 2D prefix sum
5. **Divisibility problems** - use remainder pattern
