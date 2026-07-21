# Medium Practice Problems - Arrays

## Problem 1: 3Sum (LeetCode 15)

**Problem:** Find all unique triplets that sum to zero.

**Constraints:**
- Return unique triplets (no duplicates in result)
- Cannot use same element twice

**Approach:**
1. Sort the array
2. Fix one element, use two pointer for remaining two
3. Skip duplicates for all three pointers

```python
def three_sum(nums):
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    
    return result

# Example
print(three_sum([-1, 0, 1, 2, -1, -4]))
# [[-1, -1, 2], [-1, 0, 1]]
```

**Time:** O(n²) | **Space:** O(1) excluding output

**Similar Problems:**
- 3Sum Closest
- 4Sum
- 3Sum Smaller

---

## Problem 2: Container With Most Water (LeetCode 11)

**Problem:** Find two lines that together with x-axis form a container holding the most water.

**Constraints:**
- n >= 2
- Height is non-negative

**Approach:**
1. Start with widest container (left=0, right=n-1)
2. Move the pointer with smaller height inward
3. Area is limited by shorter line, so moving taller line can't help

```python
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        water = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, water)
        
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water

# Example
print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # 49
```

**Time:** O(n) | **Space:** O(1)

**Similar Problems:**
- Trapping Rain Water
- Largest Rectangle in Histogram

---

## Problem 3: Product of Array Except Self (LeetCode 238)

**Problem:** Return array where each element is product of all other elements.

**Constraints:**
- Cannot use division
- O(n) time, O(1) extra space (excluding output)

**Approach:**
1. First pass: result[i] = product of all elements to the left of i
2. Second pass: multiply by product of all elements to the right of i

```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    
    # Left products
    left_product = 1
    for i in range(n):
        result[i] = left_product
        left_product *= nums[i]
    
    # Right products (multiply in)
    right_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]
    
    return result

# Example
print(product_except_self([1, 2, 3, 4]))  # [24, 12, 8, 6]
print(product_except_self([0, 0]))          # [0, 0]
```

**Time:** O(n) | **Space:** O(1) excluding output

**Similar Problems:**
- Divide Two Integers
- Factorial Trailing Zeroes

---

## Problem 4: Subarray Sum Equals K (LeetCode 560)

**Problem:** Find number of continuous subarrays whose sum equals k.

**Constraints:**
- Can have negative numbers
- Array length 1 to 10^5

**Approach:**
1. Use prefix sum with hash map
2. If prefix_sum - k exists in map, we found a subarray
3. Store count of each prefix sum

```python
from collections import defaultdict

def subarray_sum(nums, k):
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

# Example
print(subarray_sum([1, 1, 1], 2))  # 2
print(subarray_sum([1, 2, 3], 3))   # 2 ([1,2] and [3])
```

**Time:** O(n) | **Space:** O(n)

**Similar Problems:**
- Subarray Product Less Than K
- Continuous Subarray Sum (divisible by k)
- Binary Subarrays with Sum

---

## Problem 5: Set Matrix Zeroes (LeetCode 73)

**Problem:** If an element is 0, set its entire row and column to 0.

**Constraints:**
- Try to do it in O(mn) time, O(1) extra space

**Approach (O(1) space):**
1. Use first row and first column as markers
2. Mark zeros in first row/col separately
3. Use markers to set inner cells to zero
4. Handle first row/col last

```python
def set_zeroes(matrix):
    if not matrix:
        return
    
    m, n = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_zero = any(matrix[i][0] == 0 for i in range(m))
    
    # Use first row/col as markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    
    # Set zeros based on markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    
    # Handle first row/col
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0
    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0

# Example
matrix = [[1,1,1],[1,0,1],[1,1,1]]
set_zeroes(matrix)
print(matrix)  # [[1,0,1],[0,0,0],[1,0,1]]
```

**Time:** O(mn) | **Space:** O(1)

**Similar Problems:**
- Search a 2D Matrix
- Rotate Image
- Spiral Matrix

---

## Tips for Medium Problems

1. **Sort first** when order doesn't matter (often reduces complexity)
2. **Hash map** for O(1) lookups and prefix sums
3. **Two pointer** after sorting for pair/triplet problems
4. **In-place** modifications: use first row/col as markers, swap technique
5. **Prefix sum** for subarray sum problems (especially with negatives)
6. Always think about **edge cases**: empty, single element, all zeros
