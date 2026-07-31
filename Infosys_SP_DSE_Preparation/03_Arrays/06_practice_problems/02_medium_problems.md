# Medium Practice Problems - Arrays - Detailed Guide

## Problem 1: 3Sum (LeetCode 15)

**Problem Statement:** Find all unique triplets in the array that give the sum of zero.

**Constraints:**
- Return unique triplets (no duplicates in result)
- Cannot use same element twice

**Example:**
```
Input: nums = [-1, 0, 1, 2, -1, -4]
Output: [[-1, -1, 2], [-1, 0, 1]]
Explanation: 
  -1 + 0 + 1 = 0
  -1 + -1 + 2 = 0
```

### Approach: Sort + Fix One + Two Pointer

**Key Insight:** After sorting, fix one element and use two pointer for remaining two.

### Step-by-Step Walkthrough:

```
nums = [-1, 0, 1, 2, -1, -4]
After sort: [-4, -1, -1, 0, 1, 2]

i=0 (nums[i]=-4):
  left=1 (-1), right=5 (2)
  sum = -4 + -1 + 2 = -3 < 0 → left++
  
  left=2 (-1), right=5 (2)
  sum = -4 + -1 + 2 = -3 < 0 → left++
  
  left=3 (0), right=5 (2)
  sum = -4 + 0 + 2 = -2 < 0 → left++
  
  left=4 (1), right=5 (2)
  sum = -4 + 1 + 2 = -1 < 0 → left++
  
  left=5, STOP

i=1 (nums[i]=-1):
  left=2 (-1), right=5 (2)
  sum = -1 + -1 + 2 = 0 ✓ FOUND!
  Add [-1, -1, 2]
  
  Skip duplicates: left=3, right=4
  
  left=3 (0), right=4 (1)
  sum = -1 + 0 + 1 = 0 ✓ FOUND!
  Add [-1, 0, 1]
  
  left=4, right=3, STOP

i=2 (nums[i]=-1): Skip (same as i=1)

Result: [[-1, -1, 2], [-1, 0, 1]]
```

### Visual:

```
Sorted: [-4, -1, -1, 0, 1, 2]
          ↑   ↑           ↑
         i   left       right

i=0: Try -4 with all pairs
     -4 + (-1) + 2 = -3 (too small)
     -4 + (-1) + 2 = -3 (too small)
     -4 + 0 + 2 = -2 (too small)
     -4 + 1 + 2 = -1 (too small)
     No triplet with -4

i=1: Try -1 with all pairs
     -1 + (-1) + 2 = 0 ✓ FOUND!
     -1 + 0 + 1 = 0 ✓ FOUND!
     
i=2: Skip (duplicate of i=1)
```

### The Code:
```python
def three_sum(nums):
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicate first elements
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicate second elements
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicate third elements
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif total < 0:
                left += 1  # Need bigger sum
            else:
                right -= 1  # Need smaller sum
    
    return result

# Example usage:
print(three_sum([-1, 0, 1, 2, -1, -4]))  # [[-1, -1, 2], [-1, 0, 1]]
```

**Time:** O(n²) | **Space:** O(1) excluding output

---

## Problem 2: Container With Most Water (LeetCode 11)

**Problem Statement:** Find two lines that together with x-axis form a container holding the most water.

**Constraints:**
- n >= 2
- Height is non-negative

**Example:**
```
Input: height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
Output: 49
Explanation: Lines at index 1 (height=8) and index 8 (height=7)
             Area = min(8, 7) × (8-1) = 7 × 7 = 49
```

### Approach: Two Pointer

**Key Insight:** Area is limited by shorter line. Moving taller line can't help.

### Step-by-Step Walkthrough:

```
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]

left=0 (height=1), right=8 (height=7)
Area = min(1, 7) × 8 = 8
Move left (1 < 7)

left=1 (height=8), right=8 (height=7)
Area = min(8, 7) × 7 = 49 ← NEW MAX!
Move right (8 > 7)

left=1 (height=8), right=7 (height=3)
Area = min(8, 3) × 6 = 18
Move right (8 > 3)

left=1 (height=8), right=6 (height=8)
Area = min(8, 8) × 5 = 40
Move right (8 = 8, either works)

... continuing...

Maximum area found: 49
```

### Visual:

```
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]

    8 |     █           █
    7 |     █           █   █
    6 |     █   █       █   █
    5 |     █   █   █   █   █
    4 |     █   █   █   █   █
    3 |     █   █   █   █   █ █
    2 |     █   █ █ █   █   █ █
    1 | █   █   █ █ █   █   █ █
    0 +---+---+---+---+---+---+---+---+--
        0   1   2   3   4   5   6   7   8

Container with max area:
     █─────────────────────█
     ↑                     ↑
   left=1               right=8
   height=8             height=7
   
Area = min(8,7) × (8-1) = 7 × 7 = 49
```

### The Code:
```python
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        # Calculate current area
        water = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, water)
        
        # Move the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water

# Example usage:
print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # 49
```

**Time:** O(n) | **Space:** O(1)

---

## Problem 3: Product of Array Except Self (LeetCode 238)

**Problem Statement:** Return array where each element is product of all other elements (no division).

**Constraints:**
- Cannot use division
- O(n) time, O(1) extra space (excluding output)

**Example:**
```
Input: nums = [1, 2, 3, 4]
Output: [24, 12, 8, 6]
Explanation: 
  result[0] = 2×3×4 = 24
  result[1] = 1×3×4 = 12
  result[2] = 1×2×4 = 8
  result[3] = 1×2×3 = 6
```

### Approach: Left Products × Right Products

### Step-by-Step Walkthrough:

```
nums = [1, 2, 3, 4]

Step 1: Calculate LEFT products
        result[i] = product of all elements to LEFT of i
        
        i=0: no left → result[0] = 1
        i=1: left=[1] → result[1] = 1
        i=2: left=[1,2] → result[2] = 2
        i=3: left=[1,2,3] → result[3] = 6
        
        result = [1, 1, 2, 6]

Step 2: Calculate RIGHT products and multiply
        result[i] *= product of all elements to RIGHT of i
        
        i=3: no right → result[3] = 6 × 1 = 6
        i=2: right=[4] → result[2] = 2 × 4 = 8
        i=1: right=[3,4] → result[1] = 1 × 12 = 12
        i=0: right=[2,3,4] → result[0] = 1 × 24 = 24
        
        result = [24, 12, 8, 6] ✓
```

### Visual:

```
nums = [1, 2, 3, 4]

LEFT products:
[1] 2 3 4  → result[0] = 1
 1 [1] 3 4  → result[1] = 1
 1  2 [2] 4  → result[2] = 2
 1  2  3 [6]  → result[3] = 6

RIGHT products:
[24] 2 3 4  → result[0] = 1 × 24 = 24
 1 [12] 3 4  → result[1] = 1 × 12 = 12
 1  2 [8] 4  → result[2] = 2 × 4 = 8
 1  2  3 [6]  → result[3] = 6 × 1 = 6

Final: [24, 12, 8, 6]
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

# Example usage:
print(product_except_self([1, 2, 3, 4]))  # [24, 12, 8, 6]
```

**Time:** O(n) | **Space:** O(1) excluding output

---

## Problem 4: Subarray Sum Equals K (LeetCode 560)

**Problem Statement:** Find number of continuous subarrays whose sum equals k.

**Constraints:**
- Can have negative numbers
- Array length 1 to 10^5

**Example:**
```
Input: nums = [1, 1, 1], k = 2
Output: 2
Explanation: Subarrays [1,1] at indices 0-1 and [1,1] at indices 1-2
```

### Approach: Prefix Sum + Hash Map

**Key Insight:** If prefix[j] - prefix[i] = k, then subarray nums[i+1..j] has sum k.

### Step-by-Step Walkthrough:

```
nums = [1, 1, 1], k = 2

prefix_count = {0: 1}

num=1: current_sum = 1
       Need: 1 - 2 = -1 in prefix_count? No
       Update: prefix_count = {0: 1, 1: 1}

num=1: current_sum = 2
       Need: 2 - 2 = 0 in prefix_count? Yes! (count=1)
       count += 1
       Update: prefix_count = {0: 1, 1: 1, 2: 1}

num=1: current_sum = 3
       Need: 3 - 2 = 1 in prefix_count? Yes! (count=1)
       count += 1
       Update: prefix_count = {0: 1, 1: 1, 2: 1, 3: 1}

Total count: 2 ✓
```

### Visual:

```
nums = [1, 1, 1], k = 2

Prefix sums:
prefix[0] = 0
prefix[1] = 1
prefix[2] = 2
prefix[3] = 3

Subarray sum = prefix[j] - prefix[i]

For k=2, we need prefix[j] - prefix[i] = 2

j=2: prefix[2]=2, need prefix[i]=0
     i=0: prefix[0]=0 ✓
     Subarray: nums[1..2] = [1,1]

j=3: prefix[3]=3, need prefix[i]=1
     i=1: prefix[1]=1 ✓
     Subarray: nums[2..3] = [1,1]

Total: 2 subarrays ✓
```

### The Code:
```python
from collections import defaultdict

def subarray_sum(nums, k):
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

# Example usage:
print(subarray_sum([1, 1, 1], 2))  # 2
print(subarray_sum([1, 2, 3], 3))  # 2 ([1,2] and [3])
```

**Time:** O(n) | **Space:** O(n)

---

## Problem 5: Set Matrix Zeroes (LeetCode 73)

**Problem Statement:** If an element is 0, set its entire row and column to 0.

**Constraints:**
- Try to do it in O(mn) time, O(1) extra space

**Example:**
```
Input: matrix = [[1,1,1],[1,0,1],[1,1,1]]
Output: [[1,0,1],[0,0,0],[1,0,1]]
```

### Approach: Use First Row/Col as Markers

### Step-by-Step Walkthrough:

```
matrix = [[1,1,1],[1,0,1],[1,1,1]]

Step 1: Check if first row/col has zeros
        first_row_zero = False (no zeros in first row)
        first_col_zero = False (no zeros in first column)

Step 2: Mark zeros in first row/col
        matrix[1][1] = 0
        Mark: matrix[1][0] = 0 (row marker)
              matrix[0][1] = 0 (col marker)
        
        matrix = [[1,0,1],[0,0,1],[1,1,1]]

Step 3: Set inner cells to zero based on markers
        For i=1, j=1: matrix[1][0]=0 or matrix[0][1]=0 → matrix[1][1]=0
        For i=1, j=2: matrix[1][0]=0 → matrix[1][2]=0
        For i=2, j=1: matrix[0][1]=0 → matrix[2][1]=0
        
        matrix = [[1,0,1],[0,0,0],[1,0,1]]

Step 4: Handle first row/col
        first_row_zero = False → no change
        first_col_zero = False → no change

Final: [[1,0,1],[0,0,0],[1,0,1]] ✓
```

### Visual:

```
Original:
[1, 1, 1]
[1, 0, 1]  ← zero at (1,1)
[1, 1, 1]

Step 1: Mark first row/col
[1, 0, 1]  ← marked
[0, 0, 1]
[1, 1, 1]

Step 2: Set zeros based on markers
[1, 0, 1]
[0, 0, 0]  ← entire row becomes 0
[1, 0, 1]  ← entire column becomes 0
```

### The Code:
```python
def set_zeroes(matrix):
    if not matrix:
        return
    
    m, n = len(matrix), len(matrix[0])
    
    # Check if first row/col has zeros
    first_row_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_zero = any(matrix[i][0] == 0 for i in range(m))
    
    # Use first row/col as markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0  # Mark row
                matrix[0][j] = 0  # Mark column
    
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

# Example usage:
matrix = [[1,1,1],[1,0,1],[1,1,1]]
set_zeroes(matrix)
print(matrix)  # [[1,0,1],[0,0,0],[1,0,1]]
```

**Time:** O(mn) | **Space:** O(1)

---

## Summary Table

| # | Problem | Key Technique | Time | Space |
|---|---------|---------------|------|-------|
| 1 | 3Sum | Sort + Two Pointer | O(n²) | O(1) |
| 2 | Container With Most Water | Two Pointer | O(n) | O(1) |
| 3 | Product Except Self | Left/Right Products | O(n) | O(1) |
| 4 | Subarray Sum = K | Prefix Sum + Hash Map | O(n) | O(n) |
| 5 | Set Matrix Zeroes | Markers | O(mn) | O(1) |

## Common Mistakes & Edge Cases (All Medium Problems)

### 3Sum
- **Mistake:** Forgetting to skip duplicate elements → results in duplicate triplets.
  - `if i > 0 and nums[i] == nums[i-1]: continue` skips duplicate `i`.
  - After finding a triplet, skip duplicate `left` and `right` values.
- **Mistake:** Using the original array instead of sorting first.
  - Sorting is essential for the two-pointer approach to work.
- **Edge case:** `[-1, -1, -1, 2]` → only one valid triplet `[-1, -1, 2]`.
- **Edge case:** All zeros `[0, 0, 0]` → result is `[[0, 0, 0]]`.

### Container With Most Water
- **Mistake:** Moving the taller pointer instead of the shorter one.
  - Moving the taller pointer can only decrease width without improving height.
  - Always move the SHORTER pointer.
- **Edge case:** Two elements → area = min(h1, h2) * 1.
- **Edge case:** All same heights → area = height * (n-1).

### Product of Array Except Self
- **Mistake:** Using division (problem says "no division").
  - Division fails with zeros anyway.
- **Mistake:** Overwriting the result array before reading it.
  - Use `result[i] = left_product` then multiply by `right_product` in a separate loop.
- **Edge case:** Contains zero → result at zero's index should be product of all others.
- **Edge case:** `[1, 1]` → `[1, 1]` (product of all others is 1).

### Subarray Sum Equals K
- **Mistake:** Forgetting `prefix_count[0] = 1` (the empty prefix).
  - Without it, subarrays starting from index 0 won't be counted.
- **Mistake:** Updating the hash map BEFORE checking for complement.
  - You must check first, then update (or you'll count the current element as a subarray of length 0).
- **Edge case:** `k = 0` with `[0, 0, 0]` → multiple subarrays sum to 0.

### Set Matrix Zeroes
- **Mistake:** Modifying markers before using them.
  - If you zero out a cell, then use it as a marker for other cells, you lose the information.
  - Solution: First pass MARKS only, second pass SETS zeros.
- **Edge case:** Zero in first row AND first column → both must be handled separately.
- **Edge case:** Matrix with no zeros → no changes needed.

---

## Brute Force vs Optimal Comparison

```
┌─────────────────────────┬──────────────────────┬──────────────────────┐
│ Problem                 │ Brute Force          │ Optimal              │
├─────────────────────────┼──────────────────────┼──────────────────────┤
│ 3Sum                    │ O(n³) three nested   │ O(n²) sort +         │
│                         │ loops                │ two pointer          │
├─────────────────────────┼──────────────────────┼──────────────────────┤
│ Container Most Water    │ O(n²) try all pairs  │ O(n) two pointer     │
├─────────────────────────┼──────────────────────┼──────────────────────┤
│ Product Except Self     │ O(n²) for each       │ O(n) left/right      │
│                         │ element, multiply    │ products in-place    │
│                         │ all others           │                      │
├─────────────────────────┼──────────────────────┼──────────────────────┤
│ Subarray Sum = K        │ O(n²) check all      │ O(n) prefix sum +    │
│                         │ subarrays            │ hash map             │
├─────────────────────────┼──────────────────────┼──────────────────────┤
│ Set Matrix Zeroes       │ O(mn) extra O(mn)    │ O(mn) time O(1)      │
│                         │ space for markers    │ space using 1st row  │
└─────────────────────────┴──────────────────────┴──────────────────────┘
```

---

## Intuition Behind Key Techniques

### Why "Sort + Two Pointer" works for 3Sum

```
After sorting: [-4, -1, -1, 0, 1, 2]

Key insight: For a FIXED element nums[i], we need nums[left] + nums[right] = -nums[i]
             Since array is sorted, if sum is too small → move left pointer right (bigger)
             If sum is too big → move right pointer left (smaller)
             
This eliminates one dimension of searching → O(n) per fixed element → O(n²) total.

Without sorting: You cannot decide which pointer to move → must try all pairs.
```

### Why "Move shorter pointer" works for Container

```
Why not move the taller pointer?
┌─────────────────────────────────────────────────┐
│ If height[left] < height[right]:                │
│   - Area = height[left] × (right - left)        │
│   - Moving right left: width decreases,         │
│     height can only stay same or increase       │
│     BUT area = min(new_height, left) × new_w    │
│     Since left is the bottleneck, area CAN only │
│     decrease or stay same.                      │
│   - Moving left right: width decreases,         │
│     height might increase (no guarantee)        │
│     BUT we might find a taller left that makes  │
│     area bigger despite smaller width.          │
│                                                 │
│ So: Only moving the shorter pointer has a CHANCE │
│     of finding a bigger area.                   │
└─────────────────────────────────────────────────┘
```

---

## Tips for Medium Problems

1. **Sort first** when order doesn't matter (often reduces complexity)
2. **Hash map** for O(1) lookups and prefix sums
3. **Two pointer** after sorting for pair/triplet problems
4. **In-place** modifications: use first row/col as markers, swap technique
5. **Prefix sum** for subarray sum problems (especially with negatives)
6. **Pattern recognition:** "Subarray sum = k" → always think prefix sum + hash map
7. **Pattern recognition:** "Matrix zero" → think about using existing space as markers
8. **Dry run everything:** Medium problems are tricky — always trace through with the example before coding
