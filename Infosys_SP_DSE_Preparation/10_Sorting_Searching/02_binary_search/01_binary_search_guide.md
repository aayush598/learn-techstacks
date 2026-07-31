# Binary Search - Complete Guide

## Table of Contents
1. [Basic Binary Search](#1-basic-binary-search)
2. [Binary Search on Sorted Array](#2-binary-search-on-sorted-array)
3. [Binary Search on Answer Space](#3-binary-search-on-answer-space)
4. [First and Last Occurrence](#4-first-and-last-occurrence)
5. [Search in Rotated Sorted Array](#5-search-in-rotated-sorted-array)
6. [Search in Rotated Sorted Array II](#6-search-in-rotated-sorted-array-ii)
7. [Find Minimum in Rotated Sorted Array](#7-find-minimum-in-rotated-sorted-array)
8. [Median of Two Sorted Arrays](#8-median-of-two-sorted-arrays)

---

## 1. Basic Binary Search

### How Binary Search Works - Visual Walkthrough

Binary search works by repeatedly dividing the search interval in half.

```
Problem: Find target = 10 in sorted array

Array:  [2, 3, 4, 10, 40]
Index:   0  1  2   3   4
         L        M      R

Step 1: L=0, R=4, M=2
        arr[2] = 4 < 10  →  target is in RIGHT half
        L moves to mid+1 = 3

Array:  [2, 3, 4, 10, 40]
Index:   0  1  2   3   4
               L   M   R

Step 2: L=3, R=4, M=3
        arr[3] = 10 == 10  →  FOUND at index 3!

Result: 3

Total comparisons: 2 (instead of 4 with linear search)
```

### Why Binary Search is Fast

```
Array size    Linear Search (worst)    Binary Search (worst)
-----------   ----------------------   ---------------------
10            10 comparisons           ~3 comparisons
100           100 comparisons          ~7 comparisons
1,000         1,000 comparisons        ~10 comparisons
1,000,000     1,000,000 comparisons    ~20 comparisons
1,000,000,000 1 billion comparisons    ~30 comparisons

Each step ELIMINATES HALF of remaining elements!
```

### Iterative Version

```python
def binary_search(arr, target):
    """Basic iterative binary search."""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2  # Avoids overflow
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Target not found

# Example
arr = [2, 3, 4, 10, 40]
target = 10
print(binary_search(arr, target))  # 3
```

### Recursive Version

```python
def binary_search_recursive(arr, target, left, right):
    """Recursive binary search."""
    # Base case: search space is empty
    if left > right:
        return -1

    mid = left + (right - left) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        # Target is in the right half - recurse on right
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        # Target is in the left half - recurse on left
        return binary_search_recursive(arr, target, left, mid - 1)

# Example
arr = [2, 3, 4, 10, 40]
target = 10
print(binary_search_recursive(arr, target, 0, len(arr) - 1))  # 3
```

### Recursion Tree for Target=10

```
binary_search([2,3,4,10,40], 10, L=0, R=4)
│   mid=2, arr[2]=4 < 10 → go RIGHT
│
├── binary_search([2,3,4,10,40], 10, L=3, R=4)
│   │   mid=3, arr[3]=10 == 10 → FOUND!
│   │
│   └── return 3

Call depth: 2 (log₂(5) ≈ 2.3)
```

### Key Points

```
COMMON PITFALL: Integer Overflow
─────────────────────────────────
WRONG:  mid = (left + right) // 2
        If left=1,000,000,000 and right=1,000,000,000
        then left + right = 2,000,000,000 → OVERFLOW in some languages!

CORRECT: mid = left + (right - left) // 2
         = left + (right - left) // 2
         = 1,000,000,000 + 0 = 1,000,000,000 → SAFE

In Python, integers are arbitrary precision, so overflow doesn't happen.
But it's still a good habit to write it the safe way!
```

```python
# Template 1: left <= right  (SEARCH complete range)
# Use when: You want to FIND an element and return its index
#           or confirm it doesn't exist.

def bs_template_1(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid        # Found it!
        elif arr[mid] < target:
            left = mid + 1    # Search right half
        else:
            right = mid - 1   # Search left half
    return -1                 # Not found

# Template 2: left < right  (SEARCH for boundary)
# Use when: You want to find the LEFTMOST position where
#           a condition becomes true (first/last occurrence,
#           minimum valid answer, etc.)

def bs_template_2(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:         # Note: < not <=
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1      # Boundary is to the right
        else:
            right = mid         # Boundary is at mid or left
    return left                 # left == right, the answer
```

### When to Use Which Template - Visual Guide

```
Template 1 (left <= right):           Template 2 (left < right):
─────────────────────────             ─────────────────────────
Find EXACT element                    Find BOUNDARY / POSITION

    L   M   R                            L   R
    ↓   ↓   ↓                            ↓   ↓
[   2   3   4   10   40  ]         [   2   3   4   10   40  ]

When arr[mid] == target → RETURN     When condition met → right = mid
When L > R → NOT FOUND              When L == R → RETURN L

Use for:                             Use for:
• Finding exact element              • First occurrence of target
• Search in rotated array            • Insert position
• Count occurrences                  • Binary search on answer
```

---

## 2. Binary Search on Sorted Array

### Find Element - Step by Step

```
arr = [1, 3, 5, 7, 9, 11]     target = 7

Step 1: L=0, R=5, M=2
Index:  0  1  2  3  4  5
        1  3  5  7  9  11
        L     M        R
        arr[2]=5 < 7 → go RIGHT

Step 2: L=3, R=5, M=4
Index:  0  1  2  3  4  5
        1  3  5  7  9  11
              L  M     R
        arr[4]=9 > 7 → go LEFT

Step 3: L=3, R=3, M=3
Index:  0  1  2  3  4  5
        1  3  5  7  9  11
                 LM   R
                 (all converge)
        arr[3]=7 == 7 → FOUND at index 3!
```

### Find Insert Position - Visual

```
arr = [1, 3, 5, 6]     target = 2

Question: Where should 2 be inserted to keep the array sorted?

Index:  0  1  2  3
        1  3  5  6

Step 1: L=0, R=4, M=2
        arr[2]=5 > 2 → right = 2

Step 2: L=0, R=2, M=1
        arr[1]=3 > 2 → right = 1

Step 3: L=0, R=1, M=0
        arr[0]=1 < 2 → left = 1

L == R → return 1

Result: Insert at index 1
        [1, (2), 3, 5, 6]
             ↑ insert here
```

### Find Element

```python
def search_sorted(arr, target):
    """Search in sorted array."""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Example
arr = [1, 3, 5, 7, 9, 11]
print(search_sorted(arr, 7))  # 3
print(search_sorted(arr, 6))  # -1
```

### Find Insert Position

```python
def search_insert(arr, target):
    """Find index where target should be inserted."""
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left

# Example
arr = [1, 3, 5, 6]
print(search_insert(arr, 5))  # 2
print(search_insert(arr, 2))  # 1
print(search_insert(arr, 7))  # 4
```

---

## 3. Binary Search on Answer Space

The key insight: we're NOT searching an array. We're searching for the BEST ANSWER
in a range of possible answers, where there's a clear YES/NO predicate.

```
ANSWER SPACE VISUALIZATION:
─────────────────────────────

For Sqrt(x): Find integer square root of 8

Answer Space:  [0, 1, 2, 3, 4, 5, 6, 7, 8]
                ↓                 ↓
              (impossible)    (possible)

Predicate: mid * mid <= x?
           0*0=0  ≤ 8 ✓
           1*1=1  ≤ 8 ✓
           2*2=4  ≤ 8 ✓     ← answer space transitions here
           3*3=9  > 8 ✗
           4*4=16 > 8 ✗

We want the LARGEST mid where predicate is TRUE
→ Binary search for the boundary!
```

### Sqrt(x) - Find Integer Square Root

```python
def my_sqrt(x):
    """Find integer square root of x."""
    if x < 2:
        return x

    # Search space: [1, x//2]
    # Why x//2? Because sqrt(x) is never more than x/2 for x >= 4
    left, right = 1, x // 2

    while left <= right:
        mid = left + (right - left) // 2
        square = mid * mid

        if square == x:
            return mid           # Perfect square found!
        elif square < x:
            left = mid + 1       # Try larger
        else:
            right = mid - 1      # Try smaller

    return right  # right is the largest mid where mid*mid <= x

# Example
print(my_sqrt(8))   # 2 (since 2²=4 ≤ 8 < 9=3²)
print(my_sqrt(16))  # 4
```

```
Walkthrough for my_sqrt(8):

Search space: [1, 4]
Step 1: L=1, R=4, M=2
        2*2=4 ≤ 8 ✓ → L=3

        [3, 4]
Step 2: L=3, R=4, M=3
        3*3=9 > 8 ✗ → R=2

L > R → return R=2

Answer: 2 ✓ (since 2²=4 ≤ 8 < 9=3²)
```

### Painters Partition / Split Array

```
PROBLEM: Allocate books to k students, minimize the maximum pages
         any single student has to read.

arr = [12, 34, 67, 90]    k = 2 students

ANSWER SPACE:
            min possible        max possible
            (one book each      (one student gets
             = max of single)    everything)
                ↓                    ↓
                90 ←————————→ 203 (12+34+67+90)

We binary search for the minimum value of "max pages per student"
such that we can allocate all books to k students.
```

```python
def min_pages(arr, k):
    """Find minimum maximum pages allocatable to k students."""
    def can_allocate(max_pages):
        """Check if we can allocate with given max pages."""
        students = 1
        current_sum = 0
        
        for pages in arr:
            if current_sum + pages > max_pages:
                students += 1
                current_sum = pages
                if students > k:
                    return False
            else:
                current_sum += pages
        
        return True
    
    # Search space: [max(arr), sum(arr)]
    left, right = max(arr), sum(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if can_allocate(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

# Example
arr = [12, 34, 67, 90]
k = 2
print(min_pages(arr, k))  # 113
```

---

## 4. First and Last Occurrence

When there are duplicates, standard binary search finds "some" occurrence.
To find the FIRST or LAST, we keep searching even after finding the target.

### First Occurrence - Visual Walkthrough

```
arr = [1, 2, 2, 2, 3, 4, 5]     target = 2
Index: 0  1  2  3  4  5  6

The first occurrence of 2 is at index 1.

Step 1: L=0, R=6, M=3
        arr[3]=2 == target!
        But is it the FIRST? We dont know -> save and go LEFT
        result=3, R=2

Step 2: L=0, R=2, M=1
        arr[1]=2 == target!
        result=1, R=0

Step 3: L=0, R=0, M=0
        arr[0]=1 < target -> L=1

L > R -> return result=1

KEY INSIGHT: When we find the target, instead of returning immediately,
we RECORD the position and KEEP GOING LEFT to find an earlier one.
```

### Last Occurrence - Visual Walkthrough

```
arr = [1, 2, 2, 2, 3, 4, 5]     target = 2
Index: 0  1  2  3  4  5  6

The last occurrence of 2 is at index 3.

Step 1: L=0, R=6, M=3
        arr[3]=2 == target!
        But is it the LAST? We dont know -> save and go RIGHT
        result=3, L=4

Step 2: L=4, R=6, M=5
        arr[5]=4 > target -> R=4

Step 3: L=4, R=4, M=4
        arr[4]=3 > target -> R=3

L > R -> return result=3

KEY INSIGHT: When we find the target, we RECORD the position
and KEEP GOING RIGHT to find a later one.
```

### First vs Last - Side by Side

```
FIRST OCCURRENCE:                    LAST OCCURRENCE:
When arr[mid] == target:             When arr[mid] == target:
  result = mid                        result = mid
  right = mid - 1  (GO LEFT)          left = mid + 1   (GO RIGHT)

Think of it as:                       Think of it as:
"I found one, but there might         "I found one, but there might
 be one EARLIER to my left"            be one LATER to my right"
```

### First Occurrence

```python
def first_occurrence(arr, target):
    """Find first occurrence of target."""
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            result = mid
            right = mid - 1  # Continue searching LEFT for earlier occurrence
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result

# Example
arr = [1, 2, 2, 2, 3, 4, 5]
print(first_occurrence(arr, 2))  # 1
```

### Last Occurrence

```python
def last_occurrence(arr, target):
    """Find last occurrence of target."""
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            result = mid
            left = mid + 1  # Continue searching RIGHT for later occurrence
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result

# Example
arr = [1, 2, 2, 2, 3, 4, 5]
print(last_occurrence(arr, 2))  # 3
```

### Count Occurrences

```python
def count_occurrences(arr, target):
    """Count occurrences of target."""
    first = first_occurrence(arr, target)
    if first == -1:
        return 0
    last = last_occurrence(arr, target)
    return last - first + 1

# Example
arr = [1, 2, 2, 2, 3, 4, 5]
print(count_occurrences(arr, 2))  # 3
```

### Find in Rotated Array (First Occurrence Approach)

```python
def search_rotated(arr, target):
    """Search in rotated sorted array."""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        
        # Left half is sorted
        if arr[left] <= arr[mid]:
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1

# Example
arr = [4, 5, 6, 7, 0, 1, 2]
print(search_rotated(arr, 0))  # 4
```

---

## 5. Search in Rotated Sorted Array

A rotated sorted array is a sorted array that has been rotated at some pivot.

```
Original sorted:  [1, 2, 3, 4, 5, 6, 7]
Rotated at pivot: [4, 5, 6, 7, 0, 1, 2]
                   ─────────  ─────────
                   sorted       sorted

The key insight: At least ONE half (left or right) is ALWAYS sorted.
We can use this property to decide which half to search.
```

### Visual Walkthrough - Searching for target=0

```
arr = [4, 5, 6, 7, 0, 1, 2]     target = 0
Index: 0  1  2  3  4  5  6

Step 1: L=0, R=6, M=3
        arr = [4, 5, 6, 7, 0, 1, 2]
              L        M        R
        arr[L]=4 <= arr[M]=7 → LEFT half is sorted
        Is target in left sorted range [4, 7)?
        arr[L]=4 <= target=0 < arr[M]=7?  NO!
        So target must be in RIGHT half -> L=4

Step 2: L=4, R=6, M=5
        arr = [4, 5, 6, 7, 0, 1, 2]
                          L  M  R
        arr[L]=0 <= arr[M]=1 → LEFT half is sorted
        Is target in left sorted range [0, 1)?
        arr[L]=0 <= target=0 < arr[M]=1?  YES!
        So target is in LEFT half -> R=4

Step 3: L=4, R=4, M=4
        arr[M]=0 == target -> FOUND at index 4!
```

### Decision Flowchart

```
At each step:
                    ┌─────────────────┐
                    │ arr[L] <= arr[M]? │
                    └────────┬────────┘
                   YES /     │     \ NO
                          ┌──┴──┐
                          ▼     ▼
               ┌──────────┐  ┌──────────┐
               │LEFT half  │  │RIGHT half│
               │is sorted  │  │is sorted  │
               └─────┬─────┘  └─────┬─────┘
                     │              │
                     ▼              ▼
              ┌────────────┐ ┌────────────┐
              │Is target in│ │Is target in│
              │[arr[L],    │ │(arr[M],    │
              │ arr[M])?   │ │ arr[R]]?   │
              └─────┬──────┘ └─────┬──────┘
               YES/   \NO     YES/   \NO
                    ┌──┴──┐      ┌──┴──┐
                    ▼     ▼      ▼     ▼
                 GO    GO     GO     GO
                LEFT  RIGHT  LEFT  RIGHT
```

---

## 6. Search in Rotated Sorted Array II

```python
def search_rotated_ii(arr, target):
    """Search in rotated sorted array with duplicates."""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return True
        
        # Handle duplicates
        if arr[left] == arr[mid] == arr[right]:
            left += 1
            right -= 1
            continue
        
        # Left part is sorted
        if arr[left] <= arr[mid]:
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right part is sorted
        else:
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return False

# Example
arr = [2, 5, 6, 0, 0, 1, 2]
print(search_rotated_ii(arr, 0))  # True
print(search_rotated_ii(arr, 3))  # False
```

---

## 7. Find Minimum in Rotated Sorted Array

The minimum element is at the "rotation point" - where the array dips.

```
arr = [4, 5, 6, 7, 0, 1, 2]

Visual representation:
Value
  7 |        *
  6 |      *
  5 |    *
  4 |  *
  2 |                  *
  1 |                *
  0 |              *
    └──────────────────────
      0  1  2  3  4  5  6  Index

The minimum (0) is at the "rotation point" where values drop.
If arr[mid] > arr[right], the minimum MUST be to the RIGHT of mid.
If arr[mid] <= arr[right], the minimum is at mid or to the LEFT.
```

### Walkthrough

```
arr = [4, 5, 6, 7, 0, 1, 2]

Step 1: L=0, R=6, M=3
        [4, 5, 6, 7, 0, 1, 2]
         L        M        R
        arr[M]=7 > arr[R]=2
        Minimum is in RIGHT half -> L=4

Step 2: L=4, R=6, M=5
        [4, 5, 6, 7, 0, 1, 2]
                     L  M  R
        arr[M]=1 <= arr[R]=2
        Minimum is at M or LEFT -> R=5

Step 3: L=4, R=5, M=4
        [4, 5, 6, 7, 0, 1, 2]
                     LM     R
        arr[M]=0 <= arr[R]=2
        Minimum is at M or LEFT -> R=4

L == R -> return arr[4] = 0

Answer: 0 (the rotation point)
```

### Find Minimum Index

```python
def find_min_index_rotated(arr):
    """Find index of minimum element."""
    left, right = 0, len(arr) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if arr[mid] > arr[right]:
            left = mid + 1
        else:
            right = mid
    
    return left

# Example
arr = [4, 5, 6, 7, 0, 1, 2]
print(find_min_index_rotated(arr))  # 4
```

---

## 8. Median of Two Sorted Arrays

**Problem**: Find median of two sorted arrays in O(log(min(n,m))) time.

### Visual Concept

```
nums1 = [1, 3]       nums2 = [2, 4]
Length: m=2          Length: n=2

Combined sorted: [1, 2, 3, 4]
Median = (2 + 3) / 2 = 2.5

The trick: We PARTITION both arrays such that:
  - Left half has exactly (m+n+1)//2 = 2 elements
  - All elements in left half <= all elements in right half

Partition A:  [1 | 3]       Partition B:  [2 | 4]
              L    R                       L    R
              └──┘ └──┘                    └─┘ └──┘
              Left  Right                  Left Right

Left half = {1, 2}   Right half = {3, 4}
max_left = max(1,2)=2   min_right = min(3,4)=3
2 <= 3 ✓  → Valid partition!
Median = (2 + 3) / 2 = 2.5
```

```python
def find_median_sorted_arrays(nums1, nums2):
    """Find median of two sorted arrays."""
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    
    while left <= right:
        partition_x = (left + right) // 2
        partition_y = (m + n + 1) // 2 - partition_x
        
        # Edge cases: if partition is at boundary
        max_left_x = float('-inf') if partition_x == 0 else nums1[partition_x - 1]
        min_right_x = float('inf') if partition_x == m else nums1[partition_x]
        
        max_left_y = float('-inf') if partition_y == 0 else nums2[partition_y - 1]
        min_right_y = float('inf') if partition_y == n else nums2[partition_y]
        
        # Check if we found the correct partition
        if max_left_x <= min_right_y and max_left_y <= min_right_x:
            # Found correct partition
            if (m + n) % 2 == 1:
                return max(max_left_x, max_left_y)
            else:
                return (max(max_left_x, max_left_y) + min(min_right_x, min_right_y)) / 2
        elif max_left_x > min_right_y:
            # Move partition left
            right = partition_x - 1
        else:
            # Move partition right
            left = partition_x + 1
    
    raise ValueError("Input arrays are not sorted")

# Example 1
nums1 = [1, 3]
nums2 = [2]
print(find_median_sorted_arrays(nums1, nums2))  # 2.0

# Example 2
nums1 = [1, 2]
nums2 = [3, 4]
print(find_median_sorted_arrays(nums1, nums2))  # 2.5
```

---

## Templates Summary

### Template 1: Standard Binary Search (left <= right)

```python
def binary_search_standard(arr, target):
    """When you need to find exact target."""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

### Template 2: Boundary Binary Search (left < right)

```python
def binary_search_boundary(arr, target):
    """When you need to find leftmost/rightmost position."""
    left, right = 0, len(arr) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left
```

### Template 3: Binary Search on Answer

```python
def binary_search_answer(arr):
    """When answer space is monotonic."""
    left, right = min_possible, max_possible
    
    while left < right:
        mid = left + (right - left) // 2
        
        if is_valid(mid):
            right = mid  # Try smaller
        else:
            left = mid + 1  # Need larger
    
    return left
```

---

## Quick Reference

| Problem | Template | Time |
|---------|----------|------|
| Find element | Template 1 | O(log n) |
| First/Last occurrence | Template 1 | O(log n) |
| Search rotated array | Template 1 | O(log n) |
| Find minimum rotated | Template 2 | O(log n) |
| Median two arrays | Binary search on partition | O(log(min(n,m))) |
| Answer space search | Template 3 | O(log(answer space)) |
