# Sorting Algorithms - Complete Guide

## Table of Contents
1. [Bubble Sort](#1-bubble-sort)
2. [Selection Sort](#2-selection-sort)
3. [Insertion Sort](#3-insertion-sort)
4. [Merge Sort](#4-merge-sort)
5. [Quick Sort](#5-quick-sort)
6. [Counting Sort](#6-counting-sort)
7. [Radix Sort](#7-radix-sort)
8. [Bucket Sort](#8-bucket-sort)
9. [Python's Timsort](#9-pythons-timsort)
10. [When to Use Which](#10-when-to-use-which)
11. [Comparison Table](#11-comparison-table)

---

## 1. Bubble Sort

### Basic Version - O(n²)

```python
def bubble_sort(arr):
    """Basic bubble sort."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

### Optimized Version - O(n²) worst, O(n) best

```python
def bubble_sort_optimized(arr):
    """Optimized bubble sort - stops if no swaps in a pass."""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no swaps, array is sorted
        if not swapped:
            break
    
    return arr

# Example
arr = [64, 34, 25, 12, 22, 11, 90]
print(bubble_sort_optimized(arr))  # [11, 12, 22, 25, 34, 64, 90]
```

### Properties
- **Time Complexity**: Best O(n), Average O(n²), Worst O(n²)
- **Space Complexity**: O(1)
- **Stable**: Yes
- **In-place**: Yes
- **Adaptive**: Yes (with optimization)

---

## 2. Selection Sort

```python
def selection_sort(arr):
    """Selection sort - find minimum and swap."""
    n = len(arr)
    for i in range(n):
        # Find minimum element in unsorted portion
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Swap minimum with first unsorted element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr

# Example
arr = [64, 25, 12, 22, 11]
print(selection_sort(arr))  # [11, 12, 22, 25, 64]
```

### Properties
- **Time Complexity**: Best O(n²), Average O(n²), Worst O(n²)
- **Space Complexity**: O(1)
- **Stable**: No (can be made stable)
- **In-place**: Yes
- **Adaptive**: No

---

## 3. Insertion Sort

```python
def insertion_sort(arr):
    """Insertion sort - build sorted portion one element at a time."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Shift elements greater than key to the right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr

# Example
arr = [12, 11, 13, 5, 6]
print(insertion_sort(arr))  # [5, 6, 11, 12, 13]
```

### Properties
- **Time Complexity**: Best O(n), Average O(n²), Worst O(n²)
- **Space Complexity**: O(1)
- **Stable**: Yes
- **In-place**: Yes
- **Adaptive**: Yes
- **Best for**: Small arrays or nearly sorted arrays

---

## 4. Merge Sort

### Recursive Version - O(n log n)

```python
def merge_sort(arr):
    """Merge sort - divide and conquer."""
    if len(arr) <= 1:
        return arr
    
    # Divide
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Conquer
    return merge(left, right)

def merge(left, right):
    """Merge two sorted arrays."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Example
arr = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort(arr))  # [3, 9, 10, 27, 38, 43, 82]
```

### In-place Merge Sort

```python
def merge_sort_inplace(arr, left, right):
    """In-place merge sort using auxiliary array only for merging."""
    if left < right:
        mid = (left + right) // 2
        merge_sort_inplace(arr, left, mid)
        merge_sort_inplace(arr, mid + 1, right)
        merge_inplace(arr, left, mid, right)

def merge_inplace(arr, left, mid, right):
    """Merge two sorted subarrays in-place."""
    left_arr = arr[left:mid + 1]
    right_arr = arr[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1

# Usage
arr = [38, 27, 43, 3, 9, 82, 10]
merge_sort_inplace(arr, 0, len(arr) - 1)
print(arr)  # [3, 9, 10, 27, 38, 43, 82]
```

### Iterative Merge Sort

```python
def merge_sort_iterative(arr):
    """Iterative merge sort using bottom-up approach."""
    n = len(arr)
    width = 1
    
    while width < n:
        for i in range(0, n, 2 * width):
            left = i
            mid = min(i + width - 1, n - 1)
            right = min(i + 2 * width - 1, n - 1)
            
            if mid < right:
                merge_inplace(arr, left, mid, right)
        
        width *= 2
    
    return arr

# Example
arr = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort_iterative(arr))  # [3, 9, 10, 27, 38, 43, 82]
```

### Properties
- **Time Complexity**: Best O(n log n), Average O(n log n), Worst O(n log n)
- **Space Complexity**: O(n)
- **Stable**: Yes
- **In-place**: No (unless modified)
- **Best for**: Linked lists, external sorting

---

## 5. Quick Sort

### Lomuto Partition

```python
import random

def quicksort_lomuto(arr, low, high):
    """Quick sort using Lomuto partition."""
    if low < high:
        # Random pivot to avoid worst case
        pivot_idx = random.randint(low, high)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        
        pi = lomuto_partition(arr, low, high)
        quicksort_lomuto(arr, low, pi - 1)
        quicksort_lomuto(arr, pi + 1, high)
    
    return arr

def lomuto_partition(arr, low, high):
    """Lomuto partition scheme."""
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Usage
arr = [10, 7, 8, 9, 1, 5]
quicksort_lomuto(arr, 0, len(arr) - 1)
print(arr)  # [1, 5, 7, 8, 9, 10]
```

### Hoare Partition

```python
def quicksort_hoare(arr, low, high):
    """Quick sort using Hoare partition."""
    if low < high:
        pi = hoare_partition(arr, low, high)
        quicksort_hoare(arr, low, pi)
        quicksort_hoare(arr, pi + 1, high)
    
    return arr

def hoare_partition(arr, low, high):
    """Hoare partition scheme - more efficient than Lomuto."""
    pivot = arr[low]
    i = low - 1
    j = high + 1
    
    while True:
        # Move right pointer to element <= pivot
        j -= 1
        while arr[j] > pivot:
            j -= 1
        
        # Move left pointer to element >= pivot
        i += 1
        while arr[i] < pivot:
            i += 1
        
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
        else:
            return j

# Usage
arr = [10, 7, 8, 9, 1, 5]
quicksort_hoare(arr, 0, len(arr) - 1)
print(arr)  # [1, 5, 7, 8, 9, 10]
```

### Quick Select (Kth Smallest)

```python
import random

def quickselect(arr, k):
    """Find kth smallest element using quickselect."""
    if len(arr) == 1:
        return arr[0]
    
    pivot = random.choice(arr)
    
    lows = [x for x in arr if x < pivot]
    highs = [x for x in arr if x > pivot]
    pivots = [x for x in arr if x == pivot]
    
    if k <= len(lows):
        return quickselect(lows, k)
    elif k <= len(lows) + len(pivots):
        return pivot
    else:
        return quickselect(highs, k - len(lows) - len(pivots))

# Example
arr = [3, 2, 1, 5, 4]
k = 3
print(f"{k}rd smallest: {quickselect(arr, k)}")  # 3
```

### Properties
- **Time Complexity**: Best O(n log n), Average O(n log n), Worst O(n²)
- **Space Complexity**: O(log n) recursion stack
- **Stable**: No
- **In-place**: Yes
- **Best for**: General purpose, cache efficient

---

## 6. Counting Sort

```python
def counting_sort(arr):
    """Counting sort for non-negative integers."""
    if not arr:
        return arr
    
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val + 1
    
    # Create count array
    count = [0] * range_val
    output = [0] * len(arr)
    
    # Count occurrences
    for num in arr:
        count[num - min_val] += 1
    
    # Compute cumulative count
    for i in range(1, range_val):
        count[i] += count[i - 1]
    
    # Build output array (traverse in reverse for stability)
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
    
    return output

# Example
arr = [4, 2, 2, 8, 3, 3, 1]
print(counting_sort(arr))  # [1, 2, 2, 3, 3, 4, 8]
```

### Counting Sort with Negative Numbers

```python
def counting_sort_negative(arr):
    """Counting sort that handles negative numbers."""
    if not arr:
        return arr
    
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val + 1
    
    count = [0] * range_val
    output = [0] * len(arr)
    
    for num in arr:
        count[num - min_val] += 1
    
    for i in range(1, range_val):
        count[i] += count[i - 1]
    
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
    
    return output

# Example
arr = [-5, -1, -3, 0, 2, 4, 1]
print(counting_sort_negative(arr))  # [-5, -3, -1, 0, 1, 2, 4]
```

### Properties
- **Time Complexity**: O(n + k) where k = range of input
- **Space Complexity**: O(n + k)
- **Stable**: Yes
- **Best for**: Integer arrays with small range

---

## 7. Radix Sort

```python
def radix_sort(arr):
    """Radix sort using LSD (Least Significant Digit)."""
    if not arr:
        return arr
    
    # Handle negative numbers
    max_val = max(abs(x) for x in arr)
    
    # Separate negatives and positives
    negatives = [-x for x in arr if x < 0]
    positives = [x for x in arr if x >= 0]
    
    # Sort positives using counting sort by each digit
    if positives:
        exp = 1
        while max_val // exp > 0:
            positives = counting_sort_by_digit(positives, exp)
            exp *= 10
    
    # Sort negatives and reverse (more negative comes first)
    if negatives:
        exp = 1
        neg_max = max(negatives)
        while neg_max // exp > 0:
            negatives = counting_sort_by_digit(negatives, exp)
            exp *= 10
        negatives = [-x for x in reversed(negatives)]
    
    return negatives + positives

def counting_sort_by_digit(arr, exp):
    """Counting sort by specific digit."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    # Count occurrences
    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1
    
    # Compute cumulative count
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Build output array
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    return output

# Example
arr = [170, 45, 75, 90, 802, 24, 2, 66]
print(radix_sort(arr))  # [2, 24, 45, 66, 75, 90, 170, 802]
```

### Properties
- **Time Complexity**: O(d × (n + k)) where d = number of digits, k = base
- **Space Complexity**: O(n + k)
- **Stable**: Yes
- **Best for**: Integer arrays with many digits

---

## 8. Bucket Sort

```python
def bucket_sort(arr):
    """Bucket sort for uniformly distributed floats in [0, 1)."""
    if not arr:
        return arr
    
    n = len(arr)
    buckets = [[] for _ in range(n)]
    
    # Distribute elements into buckets
    for num in arr:
        bucket_idx = int(n * num)
        buckets[bucket_idx].append(num)
    
    # Sort individual buckets
    for i in range(n):
        buckets[i].sort()
    
    # Concatenate buckets
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result

# Example
arr = [0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51]
print(bucket_sort(arr))  # [0.23, 0.25, 0.32, 0.42, 0.47, 0.51, 0.52]
```

### Bucket Sort for Integers

```python
def bucket_sort_integers(arr, num_buckets=10):
    """Bucket sort for integers."""
    if not arr:
        return arr
    
    min_val = min(arr)
    max_val = max(arr)
    bucket_range = (max_val - min_val + 1) / num_buckets
    
    buckets = [[] for _ in range(num_buckets)]
    
    # Distribute elements
    for num in arr:
        idx = int((num - min_val) / bucket_range)
        idx = min(idx, num_buckets - 1)  # Handle edge case
        buckets[idx].append(num)
    
    # Sort individual buckets
    for i in range(num_buckets):
        buckets[i].sort()
    
    # Concatenate
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result

# Example
arr = [29, 25, 3, 49, 9, 37, 21, 43]
print(bucket_sort_integers(arr))  # [3, 9, 21, 25, 29, 37, 43, 49]
```

### Properties
- **Time Complexity**: Best O(n + k), Average O(n + k), Worst O(n²)
- **Space Complexity**: O(n + k)
- **Stable**: Yes (if using stable sort for buckets)
- **Best for**: Uniformly distributed data

---

## 9. Python's Timsort

Python's built-in `sort()` and `sorted()` use **Timsort**, a hybrid of merge sort and insertion sort.

```python
# Timsort is built into Python
arr = [5, 2, 8, 1, 9, 3]

# In-place sort
arr.sort()
print(arr)  # [1, 2, 3, 5, 8, 9]

# Returns new sorted list
arr = [5, 2, 8, 1, 9, 3]
sorted_arr = sorted(arr)
print(sorted_arr)  # [1, 2, 3, 5, 8, 9]

# Custom key function
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
students.sort(key=lambda x: x[1], reverse=True)
print(students)  # [('Bob', 92), ('Alice', 85), ('Charlie', 78)]

# Stable sort (maintains relative order of equal elements)
data = [("b", 2), ("a", 1), ("c", 2), ("d", 1)]
data.sort(key=lambda x: x[1])
print(data)  # [('a', 1), ('d', 1), ('b', 2), ('c', 2)]
```

### Properties
- **Time Complexity**: Best O(n), Average O(n log n), Worst O(n log n)
- **Space Complexity**: O(n)
- **Stable**: Yes
- **Adaptive**: Yes (efficient for partially sorted data)

---

## 10. When to Use Which

| Scenario | Recommended Sort | Why |
|----------|------------------|-----|
| Small array (n < 50) | Insertion Sort | Low overhead, simple |
| Nearly sorted | Insertion Sort / Timsort | Adaptive |
| General purpose | Quick Sort / Timsort | Fast average case |
| Need stability | Merge Sort / Timsort | Stable |
| Memory constrained | Quick Sort | In-place |
| Linked list | Merge Sort | No random access needed |
| Integers with small range | Counting Sort | O(n + k) |
| Integers with many digits | Radix Sort | O(d × (n + k)) |
| Uniformly distributed | Bucket Sort | O(n + k) average |
| External sorting | Merge Sort | Disk-friendly |

---

## 11. Comparison Table

| Sort | Best | Average | Worst | Space | Stable | In-place |
|------|------|---------|-------|-------|--------|----------|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | No | Yes |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | No |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | No | Yes |
| Counting | O(n + k) | O(n + k) | O(n + k) | O(n + k) | Yes | No |
| Radix | O(dn) | O(dn) | O(dn) | O(n + k) | Yes | No |
| Bucket | O(n + k) | O(n + k) | O(n²) | O(n + k) | Yes | No |
| Timsort | O(n) | O(n log n) | O(n log n) | O(n) | Yes | No |

---

## Key Insights

1. **Quick Sort** is fastest in practice due to cache efficiency
2. **Merge Sort** guarantees O(n log n) but uses extra space
3. **Insertion Sort** beats other sorts on small or nearly sorted data
4. **Counting/Radix/Bucket** sorts can beat comparison sorts for specific inputs
5. **Python's Timsort** is the best general-purpose sort for real-world data
