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
    if left > right:
        return -1
    
    mid = left + (right - left) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)

# Example
arr = [2, 3, 4, 10, 40]
target = 10
print(binary_search_recursive(arr, target, 0, len(arr) - 1))  # 3
```

### Key Points

```python
# Common pitfalls and solutions

# 1. Overflow prevention: Use left + (right - left) // 2 instead of (left + right) // 2

# 2. Template for left <= right (search complete range)
def bs_template_1(arr, target):
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

# 3. Template for left < right (search for boundary)
def bs_template_2(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left
```

---

## 2. Binary Search on Sorted Array

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

### Sqrt(x) - Find Integer Square Root

```python
def my_sqrt(x):
    """Find integer square root of x."""
    if x < 2:
        return x
    
    left, right = 1, x // 2
    
    while left <= right:
        mid = left + (right - left) // 2
        square = mid * mid
        
        if square == x:
            return mid
        elif square < x:
            left = mid + 1
        else:
            right = mid - 1
    
    return right  # Return right when not exact match

# Example
print(my_sqrt(8))   # 2 (since 2² = 4 ≤ 8 < 9 = 3²)
print(my_sqrt(16))  # 4
```

### Painters Partition / Split Array

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
            right = mid - 1  # Continue searching left
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
            left = mid + 1  # Continue searching right
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

```python
def search_rotated(arr, target):
    """Search in rotated sorted array (no duplicates)."""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        
        # Left part is sorted
        if arr[left] <= arr[mid]:
            # Target is in left sorted part
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right part is sorted
        else:
            # Target is in right sorted part
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1

# Example
arr = [4, 5, 6, 7, 0, 1, 2]
print(search_rotated(arr, 0))  # 4
print(search_rotated(arr, 3))  # -1
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

```python
def find_min_rotated(arr):
    """Find minimum element in rotated sorted array."""
    left, right = 0, len(arr) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if arr[mid] > arr[right]:
            # Minimum is in right half
            left = mid + 1
        else:
            # Minimum is in left half (including mid)
            right = mid
    
    return arr[left]

# Example
arr = [4, 5, 6, 7, 0, 1, 2]
print(find_min_rotated(arr))  # 0
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
