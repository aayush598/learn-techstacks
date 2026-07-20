# Array Fundamentals for Competitive Programming

## Array vs List in Python

Python lists ARE dynamic arrays. There is no separate array type.

```python
# Python list (dynamic array)
arr = [1, 2, 3, 4, 5]

# Array module (fixed-type, more memory efficient)
import array
arr = array.array('i', [1, 2, 3, 4, 5])  # 'i' = signed int

# NumPy array (for heavy computation)
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
```

| Feature | Python List | array module | NumPy |
|---------|------------|--------------|-------|
| Type restriction | None | Single type | Single type |
| Memory | More | Less | Least |
| Speed | Slow | Medium | Fast |
| Resize | Auto | Manual | Fixed |

**For CP/Interviews: Always use Python lists.**

---

## Static vs Dynamic Arrays

```python
# Dynamic (Python lists auto-resize)
arr = []
for i in range(10):
    arr.append(i)  # Grows automatically

# Simulating static array behavior
size = 5
arr = [None] * size  # Fixed size, fill with None
arr[0] = 10  # Works
# arr[5] = 60  # IndexError - full
```

---

## 1D Array Operations

```python
# Initialization
arr = [0] * 5              # [0, 0, 0, 0, 0]
arr = list(range(1, 6))    # [1, 2, 3, 4, 5]
arr = [i**2 for i in range(5)]  # [0, 1, 4, 9, 16]

# Access
print(arr[0])    # First element
print(arr[-1])   # Last element
print(arr[1:4])  # Slice [1, 2, 3]

# Update
arr[2] = 99

# Delete
arr.pop()        # Remove last
arr.pop(0)       # Remove first (O(n) - shifts all)
del arr[1]       # Remove by index
arr.remove(99)   # Remove by value
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
matrix[0][0]  # 1
matrix[1][2]  # 6

# Create m x n matrix (CAUTION with mutable defaults)
# WRONG: matrix = [[0] * n] * m  (all rows reference same list!)
matrix = [[0] * n for _ in range(m)]  # Correct way

# Transpose
transposed = list(zip(*matrix))

# Flatten 2D to 1D
flat = [x for row in matrix for x in row]

# Spiral traversal
def spiral_order(matrix):
    result = []
    if not matrix:
        return result
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        top += 1
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        if top <= bottom:
            for i in range(right, left - 1, -1):
                result.append(matrix[bottom][i])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    return result
```

---

## Array Traversal Patterns

```python
# Forward traversal
for i in range(len(arr)):
    print(arr[i])

# Backward traversal
for i in range(len(arr) - 1, -1, -1):
    print(arr[i])

# With index and value
for i, val in enumerate(arr):
    print(f"Index {i}: {val}")

# Skip by 2
for i in range(0, len(arr), 2):
    print(arr[i])

# Two pointers (start and end)
left, right = 0, len(arr) - 1
while left < right:
    # Process arr[left] and arr[right]
    left += 1
    right -= 1
```

---

## Reverse an Array (3 Ways)

```python
# Method 1: Two pointer (MOST IMPORTANT for interviews)
def reverse_array(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr
# Time: O(n), Space: O(1) - In-place

# Method 2: Python slicing
def reverse_array_slice(arr):
    return arr[::-1]
# Time: O(n), Space: O(n) - Creates new array

# Method 3: Built-in reverse
def reverse_array_builtin(arr):
    arr.reverse()  # In-place
    return arr
# Time: O(n), Space: O(1) - In-place

# Method 4: Recursion (for interview knowledge)
def reverse_recursive(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left >= right:
        return arr
    arr[left], arr[right] = arr[right], arr[left]
    return reverse_recursive(arr, left + 1, right - 1)
```

---

## Rotate Array by k Positions

```python
# LEFT rotation by k: [1,2,3,4,5] k=2 -> [3,4,5,1,2]
# RIGHT rotation by k: [1,2,3,4,5] k=2 -> [4,5,1,2,3]

# ---- Method 1: Slicing (Simple) ----
def rotate_left(arr, k):
    k %= len(arr)
    return arr[k:] + arr[:k]

def rotate_right(arr, k):
    k %= len(arr)
    return arr[-k:] + arr[:-k]
# Time: O(n), Space: O(n)

# ---- Method 2: Reversal Algorithm (BEST for interviews) ----
def rotate_right_inplace(arr, k):
    n = len(arr)
    k %= n
    arr.reverse()
    arr[:k] = reversed(arr[:k])
    arr[k:] = reversed(arr[k:])
    return arr
# [1,2,3,4,5] k=2
# Step 1: Reverse all      -> [5,4,3,2,1]
# Step 2: Reverse first k   -> [4,5,3,2,1]
# Step 3: Reverse rest      -> [4,5,1,2,3]
# Time: O(n), Space: O(1) - In-place!

# ---- Method 3: Cyclic Replacements ----
def rotate_cyclic(arr, k):
    n = len(arr)
    k %= n
    count = 0
    start = 0
    while count < n:
        current = start
        prev = arr[start]
        while True:
            next_idx = (current + k) % n
            arr[next_idx], prev = prev, arr[next_idx]
            current = next_idx
            count += 1
            if current == start:
                break
        start += 1
    return arr
# Time: O(n), Space: O(1)
```

---

## Find Max/Min, Second Largest

```python
# ---- Max/Min ----
arr = [3, 1, 4, 1, 5, 9, 2, 6]
max_val = max(arr)  # Built-in
min_val = min(arr)

# Manual (interview)
def find_max(arr):
    result = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > result:
            result = arr[i]
    return result
# Time: O(n), Space: O(1)

# ---- Second Largest (ONE PASS) ----
def second_largest(arr):
    if len(arr) < 2:
        return None
    first = second = float('-inf')
    for num in arr:
        if num > first:
            second = first
            first = num
        elif num > second and num != first:
            second = num
    return second if second != float('-inf') else None

# Example: [10, 5, 20, 8, 15]
# first=20, second=15

# ---- Second Largest using set ----
def second_largest_set(arr):
    unique = list(set(arr))
    unique.sort()
    return unique[-2] if len(unique) >= 2 else None
# Time: O(n log n) due to sort
```

---

## Remove Duplicates from Sorted Array

```python
# LeetCode 26 - Return new length
def remove_duplicates(nums):
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1

# nums = [1,1,2,3,3,4]
# slow=0, fast=1: nums[1]==nums[0], skip
# slow=0, fast=2: nums[2]!=nums[0], slow=1, nums[1]=2
# slow=1, fast=3: nums[3]!=nums[1], slow=2, nums[2]=3
# Result: [1,2,3,4,_], return 4
# Time: O(n), Space: O(1)

# Remove duplicates allowing at most 2 occurrences
def remove_duplicates_ii(nums):
    if len(nums) <= 2:
        return len(nums)
    slow = 2
    for fast in range(2, len(nums)):
        if nums[fast] != nums[slow - 2]:
            nums[slow] = nums[fast]
            slow += 1
    return slow
```

---

## Merge Two Sorted Arrays

```python
# Method 1: Extra space
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
    result.extend(a[i:])
    result.extend(b[j:])
    return result
# Time: O(n+m), Space: O(n+m)

# Method 2: Merge in-place (LeetCode 88)
# nums1 has enough space to hold nums2
def merge_inplace(nums1, m, nums2, n):
    p1 = m - 1
    p2 = n - 1
    p = m + n - 1
    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1
    nums1[:p2 + 1] = nums2[:p2 + 1]
# Time: O(n+m), Space: O(1)
```

---

## Move Zeros to End

```python
# LeetCode 283
def move_zeroes(nums):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
# [0,1,0,3,12]
# fast=0: nums[0]=0, skip
# fast=1: nums[1]=1, swap(0,1) -> [1,0,0,3,12], slow=1
# fast=2: nums[2]=0, skip
# fast=3: nums[3]=3, swap(1,3) -> [1,3,0,0,12], slow=2
# fast=4: nums[4]=12, swap(2,4) -> [1,3,12,0,0]
# Time: O(n), Space: O(1)
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
        digits[i] = 0
    # If all were 9s: [9,9,9] -> [1,0,0,0]
    return [1] + digits
# Time: O(n), Space: O(1) (or O(n) if new array needed)
```

---

## Contains Duplicate (LeetCode 217)

```python
# Method 1: Set
def contains_duplicate(nums):
    return len(nums) != len(set(nums))
# Time: O(n), Space: O(n)

# Method 2: Sort + Check adjacent
def contains_duplicate_sort(nums):
    nums.sort()
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            return True
    return False
# Time: O(n log n), Space: O(1)

# Method 3: Hash set (early exit)
def contains_duplicate_set(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
# Time: O(n), Space: O(n)
```

---

## Quick Reference: When to Use What

| Problem | Best Approach | Time |
|---------|--------------|------|
| Find max/min | Single pass | O(n) |
| Second largest | Track two vars | O(n) |
| Reverse array | Two pointer | O(n) |
| Rotate array | Reversal algorithm | O(n) |
| Remove duplicates sorted | Two pointer | O(n) |
| Merge sorted | Merge technique | O(n+m) |
| Move zeros | Two pointer | O(n) |
| Contains duplicate | Hash set | O(n) |
