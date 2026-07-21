# Top K Problems - Complete Guide

## Table of Contents
1. [Top K Frequent Elements](#1-top-k-frequent-elements)
2. [Kth Largest Element in Array](#2-kth-largest-element-in-array)
3. [Kth Smallest Element in Sorted Matrix](#3-kth-smallest-element-in-sorted-matrix)
4. [K Closest Points to Origin](#4-k-closest-points-to-origin)
5. [Kth Largest in Stream](#5-kth-largest-in-stream)
6. [Sort Array by K Frequency](#6-sort-array-by-frequency)
7. [Reorganize String](#7-reorganize-string)
8. [Task Scheduler](#8-task-scheduler)

---

## 1. Top K Frequent Elements

**Problem**: Given an integer array `nums` and an integer `k`, return the `k` most frequent elements.

**Approach**: Use a min-heap of size k, or bucket sort.

### Method 1: Min Heap - O(n log k)

```python
import heapq
from collections import Counter

def top_k_frequent(nums, k):
    """Find k most frequent elements using min-heap."""
    # Count frequencies
    count = Counter(nums)
    
    # Min-heap of size k
    min_heap = []
    for num, freq in count.items():
        heapq.heappush(min_heap, (freq, num))
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    
    return [num for freq, num in min_heap]

# Example
nums = [1, 1, 1, 2, 2, 3]
k = 2
print(top_k_frequent(nums, k))  # [1, 2]
```

### Method 2: Bucket Sort - O(n)

```python
from collections import Counter

def top_k_frequent_bucket(nums, k):
    """Find k most frequent elements using bucket sort."""
    count = Counter(nums)
    
    # Create buckets: index = frequency
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)
    
    # Collect top k from highest frequency bucket
    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result
    
    return result

# Example
nums = [1, 1, 1, 2, 2, 3]
k = 2
print(top_k_frequent_bucket(nums, k))  # [1, 2]
```

---

## 2. Kth Largest Element in Array

**Problem**: Find the kth largest element in an unsorted array.

### Method 1: Min Heap of size k - O(n log k)

```python
import heapq

def find_kth_largest(nums, k):
    """Find kth largest element using min-heap."""
    min_heap = nums[:k]
    heapq.heapify(min_heap)
    
    for num in nums[k:]:
        if num > min_heap[0]:
            heapq.heapreplace(min_heap, num)
    
    return min_heap[0]

# Example
nums = [3, 2, 1, 5, 6, 4]
k = 2
print(find_kth_largest(nums, k))  # 5
```

### Method 2: Max Heap - O(n log n)

```python
import heapq

def find_kth_largest_max_heap(nums, k):
    """Find kth largest using max-heap (negation trick)."""
    max_heap = [-num for num in nums]
    heapq.heapify(max_heap)
    
    for _ in range(k - 1):
        heapq.heappop(max_heap)
    
    return -max_heap[0]

# Example
nums = [3, 2, 1, 5, 6, 4]
k = 2
print(find_kth_largest_max_heap(nums, k))  # 5
```

### Method 3: Quickselect - Average O(n)

```python
import random

def find_kth_largest_quickselect(nums, k):
    """Find kth largest using quickselect."""
    target = len(nums) - k  # Convert to kth smallest
    
    def quickselect(left, right):
        if left == right:
            return nums[left]
        
        # Random pivot to avoid worst case
        pivot_idx = random.randint(left, right)
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        pivot = nums[right]
        
        # Partition
        store_idx = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[store_idx], nums[i] = nums[i], nums[store_idx]
                store_idx += 1
        nums[store_idx], nums[right] = nums[right], nums[store_idx]
        
        if store_idx == target:
            return nums[store_idx]
        elif store_idx < target:
            return quickselect(store_idx + 1, right)
        else:
            return quickselect(left, store_idx - 1)
    
    return quickselect(0, len(nums) - 1)

# Example
nums = [3, 2, 1, 5, 6, 4]
k = 2
print(find_kth_largest_quickselect(nums, k))  # 5
```

---

## 3. Kth Smallest Element in Sorted Matrix

**Problem**: Given an `n x n` matrix where each row and column is sorted, find the kth smallest element.

### Method 1: Min Heap - O(k log n)

```python
import heapq

def kth_smallest_matrix(matrix, k):
    """Find kth smallest in sorted matrix using min-heap."""
    n = len(matrix)
    min_heap = [(matrix[i][0], i, 0) for i in range(min(n, k))]
    heapq.heapify(min_heap)
    
    for _ in range(k):
        val, row, col = heapq.heappop(min_heap)
        if col + 1 < n:
            heapq.heappush(min_heap, (matrix[row][col + 1], row, col + 1))
    
    return val

# Example
matrix = [
    [1,  5,  9],
    [10, 11, 13],
    [12, 13, 15]
]
k = 8
print(kth_smallest_matrix(matrix, k))  # 13
```

### Method 2: Binary Search - O(n log(max-min))

```python
def kth_smallest_matrix_binary(matrix, k):
    """Find kth smallest using binary search."""
    n = len(matrix)
    
    def count_less_equal(mid):
        """Count elements <= mid in the matrix."""
        count = 0
        row, col = n - 1, 0  # Start from bottom-left
        
        while row >= 0 and col < n:
            if matrix[row][col] <= mid:
                count += row + 1
                col += 1
            else:
                row -= 1
        
        return count
    
    lo, hi = matrix[0][0], matrix[-1][-1]
    
    while lo < hi:
        mid = (lo + hi) // 2
        if count_less_equal(mid) < k:
            lo = mid + 1
        else:
            hi = mid
    
    return lo

# Example
matrix = [
    [1,  5,  9],
    [10, 11, 13],
    [12, 13, 15]
]
k = 8
print(kth_smallest_matrix_binary(matrix, k))  # 13
```

---

## 4. K Closest Points to Origin

**Problem**: Find the k closest points to the origin (0, 0).

```python
import heapq
import math

def k_closest_points(points, k):
    """Find k closest points to origin using max-heap."""
    # Max-heap storing (-distance, x, y)
    max_heap = []
    
    for x, y in points:
        dist = math.sqrt(x**2 + y**2)
        heapq.heappush(max_heap, (-dist, x, y))
        if len(max_heap) > k:
            heapq.heappop(max_heap)
    
    return [(x, y) for _, x, y in max_heap]

# Or more Pythonic version
def k_closest_pythonic(points, k):
    """Find k closest points to origin."""
    return heapq.nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2)

# Example
points = [[3, 3], [5, -1], [-2, 4], [1, 1]]
k = 2
print(k_closest_pythonic(points, k))  # [[1, 1], [3, 3]]
```

---

## 5. Kth Largest in Stream

**Problem**: Design a class to find the kth largest element in a stream.

```python
import heapq

class KthLargest:
    """Find kth largest element in a stream."""
    
    def __init__(self, k, nums):
        """
        :type k: int
        :type nums: List[int]
        """
        self.k = k
        self.min_heap = nums[:k]
        heapq.heapify(self.min_heap)
        
        for num in nums[k:]:
            if num > self.min_heap[0]:
                heapq.heapreplace(self.min_heap, num)
    
    def add(self, val):
        """
        Add val to stream and return kth largest.
        :type val: int
        :rtype: int
        """
        if len(self.min_heap) < self.k:
            heapq.heappush(self.min_heap, val)
        elif val > self.min_heap[0]:
            heapq.heapreplace(self.min_heap, val)
        
        return self.min_heap[0]

# Example
k = 3
nums = [4, 5, 8, 2]
kth_largest = KthLargest(k, nums)

print(kth_largest.add(3))   # 4
print(kth_largest.add(5))   # 5
print(kth_largest.add(10))  # 5
print(kth_largest.add(9))   # 8
print(kth_largest.add(4))   # 8
```

---

## 6. Sort Array by Frequency

**Problem**: Sort an array by frequency of elements. If two elements have the same frequency, sort them by value.

```python
import heapq
from collections import Counter

def frequency_sort(nums):
    """Sort array by frequency."""
    count = Counter(nums)
    
    # Max-heap: (-frequency, -value) for descending order
    max_heap = [(-freq, -num) for num, freq in count.items()]
    heapq.heapify(max_heap)
    
    result = []
    while max_heap:
        freq, num = heapq.heappop(max_heap)
        result.extend([-num] * -freq)
    
    return result

# Alternative: using sorted()
def frequency_sort_v2(nums):
    count = Counter(nums)
    return sorted(nums, key=lambda x: (-count[x], -x))

# Example
nums = [2, 3, 5, 3, 7, 9, 5, 3, 7]
print(frequency_sort(nums))  # [3, 3, 3, 7, 7, 5, 5, 2, 9]
```

---

## 7. Reorganize String

**Problem**: Rearrange string so that no two adjacent characters are the same. Return empty string if not possible.

```python
import heapq
from collections import Counter

def reorganize_string(s):
    """Reorganize string so no adjacent chars are same."""
    count = Counter(s)
    max_count = max(count.values())
    
    # If any character appears more than (n+1)//2 times, impossible
    if max_count > (len(s) + 1) // 2:
        return ""
    
    # Max-heap: (-frequency, char)
    max_heap = [(-freq, char) for char, freq in count.items()]
    heapq.heapify(max_heap)
    
    result = []
    prev = None
    
    while max_heap:
        freq, char = heapq.heappop(max_heap)
        result.append(char)
        
        # Push back previous character if it still has count
        if prev:
            heapq.heappush(max_heap, prev)
            prev = None
        
        # Update frequency
        if freq + 1 < 0:
            prev = (freq + 1, char)
    
    return ''.join(result)

# Example
print(reorganize_string("aab"))   # "aba"
print(reorganize_string("aaab"))  # "" (impossible)
```

---

## 8. Task Scheduler

**Problem**: Given tasks with cooldown period, find minimum intervals to finish all tasks.

```python
import heapq
from collections import Counter

def least_interval(tasks, n):
    """
    Find minimum intervals to complete all tasks.
    tasks: list of characters representing tasks
    n: cooldown period between same tasks
    """
    # Count task frequencies
    count = Counter(tasks)
    
    # Max-heap of frequencies
    max_heap = [-freq for freq in count.values()]
    heapq.heapify(max_heap)
    
    time = 0
    cooldown_queue = []  # (remaining_count, available_time)
    
    while max_heap or cooldown_queue:
        time += 1
        
        if max_heap:
            # Execute most frequent task
            freq = heapq.heappop(max_heap)
            if freq + 1 < 0:  # Still has remaining
                cooldown_queue.append((freq + 1, time + n))
        
        # Check if any task is ready from cooldown
        if cooldown_queue and cooldown_queue[0][1] <= time:
            freq, _ = cooldown_queue.pop(0)
            heapq.heappush(max_heap, freq)
    
    return time

# Example
tasks = ["A", "A", "A", "B", "B", "B"]
n = 2
print(least_interval(tasks, n))  # 8
# Schedule: A -> B -> idle -> A -> B -> idle -> A -> B
```

### Alternative Mathematical Approach - O(n)

```python
from collections import Counter

def least_interval_math(tasks, n):
    """Mathematical approach for task scheduler."""
    count = Counter(tasks)
    max_freq = max(count.values())
    
    # Count how many tasks have max frequency
    max_count = sum(1 for freq in count.values() if freq == max_freq)
    
    # Formula: (max_freq - 1) * (n + 1) + max_count
    result = (max_freq - 1) * (n + 1) + max_count
    
    # Result is at least len(tasks)
    return max(result, len(tasks))

# Example
tasks = ["A", "A", "A", "B", "B", "B"]
n = 2
print(least_interval_math(tasks, n))  # 8
```

---

## Quick Reference: Top K Patterns

| Pattern | Approach | Time | Space |
|---------|----------|------|-------|
| Top K Frequent | Min heap of size K | O(n log k) | O(n) |
| Kth Largest | Min heap of size K | O(n log k) | O(k) |
| K Closest | Min/Max heap | O(n log k) | O(k) |
| Kth in Sorted Matrix | Binary search + count | O(n log(max-min)) | O(1) |
| Stream Processing | Maintain heap of size K | O(log k) per add | O(k) |

---

## Tips

1. **Min-heap for "K largest"**: Keep k largest, evict smallest
2. **Max-heap for "K smallest"**: Keep k smallest, evict largest
3. **Bucket sort**: When values are bounded integers
4. **Quickselect**: Average O(n), but O(n²) worst case
5. **Binary search on answer**: When answer space is monotonic
