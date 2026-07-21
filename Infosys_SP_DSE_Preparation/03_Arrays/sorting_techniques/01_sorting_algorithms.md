# Sorting Algorithms for Competitive Programming

## 1. Bubble Sort

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:  # Early termination
            break
    return arr
# Time: O(n²) worst, O(n) best (already sorted)
# Space: O(1)
# Stable: Yes
# Use: Nearly sorted data, educational purposes
```

---

## 2. Selection Sort

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
# Time: O(n²) always
# Space: O(1)
# Stable: No (can be made stable)
# Use: When memory writes are expensive (minimizes swaps)
```

---

## 3. Insertion Sort

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
# Time: O(n²) worst, O(n) best
# Space: O(1)
# Stable: Yes
# Use: Small arrays (n < 50), nearly sorted data, online sorting
```

---

## 4. Merge Sort

### Recursive

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
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
# Time: O(n log n) always
# Space: O(n)
# Stable: Yes
# Use: Guaranteed O(n log n), linked lists, external sorting
```

### In-Place Merge Sort (for CP)

```python
def merge_sort_inplace(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort_inplace(arr, left, mid)
        merge_sort_inplace(arr, mid + 1, right)
        merge_arr(arr, left, mid, right)

def merge_arr(arr, left, mid, right):
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

# Usage: merge_sort_inplace(arr, 0, len(arr) - 1)
```

---

## 5. Quick Sort

### Lomuto Partition

```python
def quicksort_lomuto(arr, low, high):
    if low < high:
        pivot_idx = partition_lomuto(arr, low, high)
        quicksort_lomuto(arr, low, pivot_idx - 1)
        quicksort_lomuto(arr, pivot_idx + 1, high)

def partition_lomuto(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

### Hoare Partition (Fewer Swaps)

```python
def quicksort_hoare(arr, low, high):
    if low < high:
        p = partition_hoare(arr, low, high)
        quicksort_hoare(arr, low, p)
        quicksort_hoare(arr, p + 1, high)

def partition_hoare(arr, low, high):
    pivot = arr[low]
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        j -= 1
        while arr[j] > pivot:
            j -= 1
        if i >= j:
            return j
        arr[i], arr[j] = arr[j], arr[i]
    return j

# Quick Sort: O(n²) worst, O(n log n) average
# Space: O(log n) average (recursion stack)
# Stable: No
# Use: General purpose, fastest in practice
# For CP: Use random pivot to avoid worst case

def quicksort_random(arr, low, high):
    import random
    if low < high:
        pivot_idx = random.randint(low, high)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        p = partition_lomuto(arr, low, high)
        quicksort_random(arr, low, p - 1)
        quicksort_random(arr, p + 1, high)
```

---

## 6. Counting Sort

```python
def counting_sort(arr):
    if not arr:
        return arr
    min_val, max_val = min(arr), max(arr)
    range_val = max_val - min_val + 1
    
    count = [0] * range_val
    for num in arr:
        count[num - min_val] += 1
    
    # Cumulative count
    for i in range(1, range_val):
        count[i] += count[i - 1]
    
    # Build result (traverse backwards for stability)
    result = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        count[arr[i] - min_val] -= 1
        result[count[arr[i] - min_val]] = arr[i]
    
    return result
# Time: O(n + k) where k = range of values
# Space: O(n + k)
# Stable: Yes
# Use: Small range of integer values
```

---

## 7. Radix Sort

```python
def radix_sort(arr):
    if not arr:
        return arr
    max_val = max(arr)
    exp = 1
    
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10
    
    return arr

def counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for num in arr:
        idx = (num // exp) % 10
        count[idx] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for i in range(n - 1, -1, -1):
        idx = (arr[i] // exp) % 10
        count[idx] -= 1
        output[count[idx]] = arr[i]
    
    for i in range(n):
        arr[i] = output[i]

# Time: O(d * (n + k)) where d = digits, k = 10
# Space: O(n + k)
# Stable: Yes
# Use: When range is large but number of digits is small
```

---

## 8. Bucket Sort

```python
def bucket_sort(arr, num_buckets=10):
    if not arr:
        return arr
    
    min_val, max_val = min(arr), max(arr)
    bucket_range = (max_val - min_val) / num_buckets + 1
    
    buckets = [[] for _ in range(num_buckets)]
    
    for num in arr:
        idx = int((num - min_val) / bucket_range)
        buckets[idx].append(num)
    
    result = []
    for bucket in buckets:
        bucket.sort()  # Use insertion sort or any sort
        result.extend(bucket)
    
    return result
# Time: O(n + k) average, O(n²) worst
# Space: O(n + k)
# Stable: Depends on inner sort
# Use: Uniformly distributed data
```

---

## 9. Tim Sort (Python's Built-in)

```python
# Python's sorted() and list.sort() use Tim Sort
# It's a hybrid of Merge Sort and Insertion Sort

arr = [5, 2, 8, 1, 9]
arr.sort()           # In-place
result = sorted(arr) # Returns new list

# Custom key
arr.sort(key=lambda x: -x)  # Descending
arr.sort(key=lambda x: (x % 10, x))  # Sort by last digit, then value

# Custom comparator (Python 3)
from functools import cmp_to_key
arr.sort(key=cmp_to_key(lambda a, b: a - b))  # Ascending
arr.sort(key=cmp_to_key(lambda a, b: b - a))  # Descending

# Sorting tuples
pairs = [(1, 'b'), (2, 'a'), (1, 'a')]
pairs.sort(key=lambda x: (x[0], x[1]))  # Sort by first, then second
# Time: O(n log n) guaranteed
# Space: O(n)
# Stable: Yes
```

---

## Sorting with Custom Key

```python
# Sort by absolute value
arr = [-3, 1, -4, 1, 5]
arr.sort(key=lambda x: abs(x))
# [-3, 1, 1, -4, 5] -> [-3, 1, 1, -4, 5] by abs

# Sort by frequency
from collections import Counter
freq = Counter([3, 1, 4, 1, 5, 9, 2, 6, 5])
arr = [3, 1, 4, 1, 5, 9, 2, 6, 5]
arr.sort(key=lambda x: (freq[x], -x))
# Sort by frequency ascending, then by value descending

# Sort strings by length
words = ["apple", "hi", "banana", "ok"]
words.sort(key=len)
# ['hi', 'ok', 'apple', 'banana']

# Sort with operator.itemgetter
from operator import itemgetter
data = [(1, 'c'), (2, 'a'), (1, 'b')]
data.sort(key=itemgetter(0, 1))  # Sort by index 0, then index 1
```

---

## Sorting Tricks for CP

```python
# 1. Sort only part of array
arr = [5, 3, 8, 1, 9, 2]
arr[1:4] = sorted(arr[1:4])  # Sort only indices 1 to 3
# [5, 1, 3, 8, 9, 2]

# 2. Stable sort preserves order of equal elements
# Use for multi-level sorting without tuples

# 3. argsort - get indices that would sort array
import numpy as np  # (or implement manually)
arr = [3, 1, 4, 1, 5]
indices = sorted(range(len(arr)), key=lambda i: arr[i])
# [1, 3, 0, 2, 4]

# 4. Sort and deduplicate
arr = [3, 1, 4, 1, 5, 3, 4]
unique_sorted = sorted(set(arr))
# [1, 3, 4, 5]

# 5. Find kth smallest without full sort
import heapq
kth = heapq.nsmallest(k, arr)[-1]  # O(n log k)

# 6. Partial sort for top k
top_k = heapq.nlargest(k, arr)  # O(n log k)
```

---

## Comparison Table

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Counting | O(n+k) | O(n+k) | O(n+k) | O(n+k) | Yes |
| Radix | O(dn) | O(dn) | O(dn) | O(n+k) | Yes |
| Bucket | O(n+k) | O(n+k) | O(n²) | O(n+k) | Depends |
| Tim Sort | O(n) | O(n log n) | O(n log n) | O(n) | Yes |

**For CP:** Use Python's built-in `sort()` (Tim Sort) unless specifically asked to implement another.
