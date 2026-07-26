# Array Fundamentals for Competitive Programming - Complete Guide

## What is an Array?

An array is a collection of elements stored at **contiguous memory locations**.

### Visual: How Arrays Work in Memory

```
Index:    0      1      2      3      4
Value:  [ 10 ] [ 20 ] [ 30 ] [ 40 ] [ 50 ]
Memory: 0x100  0x104  0x108  0x10C  0x110

Each element takes 4 bytes (for int)
Element at index i is at address: base + i × 4
```

**Why contiguous matters:**
- Random access in O(1) - can jump directly to any index
- Cache friendly - elements are next to each other in memory

---

## Python List vs Array vs NumPy

**For interviews/CP: ALWAYS use Python lists!**

```python
# Python list (dynamic array) - USE THIS
arr = [1, 2, 3, 4, 5]

# Array module (fixed-type, rarely used)
import array
arr = array.array('i', [1, 2, 3, 4, 5])

# NumPy (for heavy computation, not needed for CP)
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
```

---

## Creating Arrays

```python
# Method 1: Direct
arr = [1, 2, 3, 4, 5]

# Method 2: Zeros
arr = [0] * 5           # [0, 0, 0, 0, 0]

# Method 3: Range
arr = list(range(1, 6))  # [1, 2, 3, 4, 5]

# Method 4: List comprehension
arr = [i**2 for i in range(5)]  # [0, 1, 4, 9, 16]

# Method 5: Repeat
arr = [1] * 10  # [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
```

### Visual: Creating [0, 1, 4, 9, 16]

```
i=0: 0² = 0  → arr[0] = 0
i=1: 1² = 1  → arr[1] = 1
i=2: 2² = 4  → arr[2] = 4
i=3: 3² = 9  → arr[3] = 9
i=4: 4² = 16 → arr[4] = 16

Result: [0, 1, 4, 9, 16]
```

---

## Accessing Elements

```python
arr = [10, 20, 30, 40, 50]

# Index from 0
print(arr[0])    # 10 (first)
print(arr[2])    # 30 (third)
print(arr[-1])   # 50 (last)
print(arr[-2])   # 40 (second last)

# Slicing: arr[start:end:step]
print(arr[1:4])   # [20, 30, 40]
print(arr[::2])   # [10, 30, 50] (every 2nd)
print(arr[::-1])  # [50, 40, 30, 20, 10] (reversed)
```

### Visual: Slicing arr[1:4]

```
Index:    0      1      2      3      4
Value:  [ 10 ] [ 20 ] [ 30 ] [ 40 ] [ 50 ]
                ↑                    ↑
              start                end (exclusive)
              
Result: [20, 30, 40]
```

**Key Rule:** Slicing includes start, excludes end!

---

## Time Complexity of Array Operations

| Operation | Time | Why |
|-----------|------|-----|
| Access arr[i] | O(1) | Direct memory calculation |
| Search (unsorted) | O(n) | Must check each element |
| Search (sorted) | O(log n) | Binary search possible |
| Insert at end | O(1)* | *Amortized (see below) |
| Insert at beginning | O(n) | Must shift all elements |
| Delete at end | O(1) | Just remove last |
| Delete at beginning | O(n) | Must shift all elements |

### Why Insert at End is O(1)?

```
When array is full:
[10][20][30][40][50]  ← full!

New array (2x size):
[10][20][30][40][50][ ][ ][ ][ ][ ]  ← room to grow!

Copy operations: n
But over n inserts, total copies = n + n/2 + n/4 + ... ≈ 2n
So average = 2n/n = O(1) per insert!
```

---

## 1D Array Operations

### Reverse an Array (3 Ways)

```python
arr = [1, 2, 3, 4, 5]

# Method 1: Two pointer (BEST for interviews)
def reverse_array(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr

# Method 2: Python slicing
arr = arr[::-1]

# Method 3: Built-in
arr.reverse()
```

### Visual: Two Pointer Reverse

```
Initial: [1, 2, 3, 4, 5]
          ↑           ↑
         left       right

Step 1: Swap 1 and 5
        [5, 2, 3, 4, 1]
              ↑     ↑
            left  right

Step 2: Swap 2 and 4
        [5, 4, 3, 2, 1]
                ↑
             left=right (STOP!)

Result: [5, 4, 3, 2, 1]
```

**Time:** O(n) | **Space:** O(1) - In-place!

---

### Rotate Array by k Positions

```python
# LEFT rotation: [1,2,3,4,5] k=2 → [3,4,5,1,2]
# RIGHT rotation: [1,2,3,4,5] k=2 → [4,5,1,2,3]

# Reversal Algorithm (BEST for interviews)
def rotate_right(arr, k):
    n = len(arr)
    k %= n  # Handle k > n
    
    # Step 1: Reverse entire array
    arr.reverse()
    # [1,2,3,4,5] → [5,4,3,2,1]
    
    # Step 2: Reverse first k elements
    arr[:k] = reversed(arr[:k])
    # k=2: [4,5,3,2,1]
    
    # Step 3: Reverse remaining elements
    arr[k:] = reversed(arr[k:])
    # [4,5,1,2,3]
    
    return arr
```

### Visual: Right Rotate [1,2,3,4,5] by 2

```
Step 1: Reverse ALL
        [1,2,3,4,5] → [5,4,3,2,1]

Step 2: Reverse FIRST k=2
        [5,4,3,2,1] → [4,5,3,2,1]
         ↑───↑

Step 3: Reverse REST (from index 2)
        [4,5,3,2,1] → [4,5,1,2,3]
              ↑───────↑

Final: [4,5,1,2,3] ✓
```

**Time:** O(n) | **Space:** O(1) - In-place!

---

### Find Second Largest (One Pass)

```python
def second_largest(arr):
    if len(arr) < 2:
        return None
    
    first = second = float('-inf')
    
    for num in arr:
        if num > first:
            second = first  # Old first becomes second
            first = num     # Update first
        elif num > second and num != first:
            second = num    # Update second
    
    return second if second != float('-inf') else None
```

### Visual: Find Second Largest in [10, 5, 20, 8, 15]

```
num=10: first=10, second=-inf
num=5:  first=10, second=5
num=20: first=20, second=10 (old first)
num=8:  first=20, second=10 (8 < 10, skip)
num=15: first=20, second=15 (15 > 10)

Result: 15 ✓
```

---

### Remove Duplicates from Sorted Array

**Problem:** Remove duplicates in-place, return new length.

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    
    slow = 0  # Points to last unique element
    
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    
    return slow + 1  # Length of unique elements
```

### Visual: Remove Duplicates from [1, 1, 2, 3, 3, 4]

```
Initial: slow=0, fast=1
[1, 1, 2, 3, 3, 4]
 ↑  ↑
slow fast

fast=1: nums[1]==nums[0] (both 1), skip

fast=2: nums[2]!=nums[0] (2≠1)
        slow=1, nums[1]=2
        [1, 2, 2, 3, 3, 4]
           ↑     ↑
         slow   fast

fast=3: nums[3]!=nums[1] (3≠2)
        slow=2, nums[2]=3
        [1, 2, 3, 3, 3, 4]
              ↑        ↑
            slow      fast

fast=4: nums[4]==nums[2] (both 3), skip

fast=5: nums[5]!=nums[2] (4≠3)
        slow=3, nums[3]=4
        [1, 2, 3, 4, 3, 4]
              ↑           ↑
            slow         fast

Result: [1, 2, 3, 4, _, _], return 4
```

**Time:** O(n) | **Space:** O(1)

---

### Move Zeros to End

```python
def move_zeroes(nums):
    slow = 0
    
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
```

### Visual: Move Zeros in [0, 1, 0, 3, 12]

```
fast=0: nums[0]=0, skip
        [0, 1, 0, 3, 12]

fast=1: nums[1]=1≠0, swap(0,1)
        [1, 0, 0, 3, 12], slow=1

fast=2: nums[2]=0, skip
        [1, 0, 0, 3, 12]

fast=3: nums[3]=3≠0, swap(1,3)
        [1, 3, 0, 0, 12], slow=2

fast=4: nums[4]=12≠0, swap(2,4)
        [1, 3, 12, 0, 0], slow=3

Result: [1, 3, 12, 0, 0] ✓
```

---

## 2D Arrays (Matrix)

```python
# Creating a 3x3 matrix
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Access
matrix[0][0]  # 1 (row 0, col 0)
matrix[1][2]  # 6 (row 1, col 2)

# CAUTION: Don't do this!
# matrix = [[0] * n] * m  ← All rows reference same list!

# Correct way
matrix = [[0] * n for _ in range(m)]
```

### Visual: 2D Array in Memory

```
Indexing: matrix[row][col]

     Col0 Col1 Col2
Row0 [ 1 ] [ 2 ] [ 3 ]
Row1 [ 4 ] [ 5 ] [ 6 ]
Row2 [ 7 ] [ 8 ] [ 9 ]

matrix[1][2] = 6  (Row 1, Col 2)
```

### Spiral Traversal

```
Given matrix:
[ 1 ] [ 2 ] [ 3 ]
[ 4 ] [ 5 ] [ 6 ]
[ 7 ] [ 8 ] [ 9 ]

Spiral order: 1 → 2 → 3 → 6 → 9 → 8 → 7 → 4 → 5

Visual path:
1 → 2 → 3
          ↓
4   5   6
↑       ↓
7 ← 8 ← 9
```

### The Code:
```python
def spiral_order(matrix):
    result = []
    if not matrix:
        return result
    
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # Traverse right
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        top += 1
        
        # Traverse down
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        
        # Traverse left
        if top <= bottom:
            for i in range(right, left - 1, -1):
                result.append(matrix[bottom][i])
            bottom -= 1
        
        # Traverse up
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    
    return result
```

---

## Merge Two Sorted Arrays

```python
def merge_sorted(a, b):
    result = []
    i = j = 0
    
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    
    # Add remaining elements
    result.extend(a[i:])
    result.extend(b[j:])
    
    return result
```

### Visual: Merge [1, 3, 5] and [2, 4, 6]

```
a: [1, 3, 5]    b: [2, 4, 6]
    ↑                ↑
   i=0              j=0

Compare 1 vs 2: 1<2, add 1
result: [1]

Compare 3 vs 2: 3>2, add 2
result: [1, 2]

Compare 3 vs 4: 3<4, add 3
result: [1, 2, 3]

Compare 5 vs 4: 5>4, add 4
result: [1, 2, 3, 4]

Compare 5 vs 6: 5<6, add 5
result: [1, 2, 3, 4, 5]

a exhausted, add remaining b: [6]
result: [1, 2, 3, 4, 5, 6]
```

---

## Contains Duplicate

```python
# Method 1: Set (fastest)
def contains_duplicate(nums):
    return len(nums) != len(set(nums))

# Method 2: Hash set (early exit)
def contains_duplicate_set(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

# Method 3: Sort + check adjacent
def contains_duplicate_sort(nums):
    nums.sort()
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            return True
    return False
```

---

## Plus One (LeetCode 66)

```python
def plus_one(digits):
    n = len(digits)
    
    for i in range(n - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0  # Carry over
    
    # All digits were 9
    return [1] + digits
```

### Visual: Plus One [1, 2, 9]

```
Start from rightmost digit:

digits[2] = 9, set to 0, carry
digits[1] = 2, add 1 = 3, return

Result: [1, 3, 0]

Example 2: [9, 9, 9]

digits[2] = 9, set to 0
digits[1] = 9, set to 0
digits[0] = 9, set to 0

All were 9s!
Return [1] + [0, 0, 0] = [1, 0, 0, 0]
```

---

## Array Traversal Patterns

```python
# Forward
for i in range(len(arr)):
    print(arr[i])

# Backward
for i in range(len(arr) - 1, -1, -1):
    print(arr[i])

# With index and value
for i, val in enumerate(arr):
    print(f"Index {i}: {val}")

# Two pointers
left, right = 0, len(arr) - 1
while left < right:
    # Process arr[left] and arr[right]
    left += 1
    right -= 1
```

---

## Quick Reference

| Problem | Best Approach | Time | Space |
|---------|--------------|------|-------|
| Find max/min | Single pass | O(n) | O(1) |
| Second largest | Track two vars | O(n) | O(1) |
| Reverse array | Two pointer | O(n) | O(1) |
| Rotate array | Reversal algorithm | O(n) | O(1) |
| Remove duplicates sorted | Two pointer | O(n) | O(1) |
| Merge sorted | Merge technique | O(n+m) | O(n+m) |
| Move zeros | Two pointer | O(n) | O(1) |
| Contains duplicate | Hash set | O(n) | O(n) |
| Spiral traversal | Boundary tracking | O(m×n) | O(1) |

## Key Interview Tips

1. **Clarify** if array is sorted - changes the approach!
2. **Two pointer** is the most common technique
3. **Edge cases:** empty array, single element, all same elements
4. **In-place** operations preferred (O(1) space)
5. **Python slicing** creates new arrays (O(n) space)
