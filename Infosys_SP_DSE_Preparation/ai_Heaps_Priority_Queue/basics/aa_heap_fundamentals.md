# Heap Fundamentals - Complete Guide

## Table of Contents
1. [Heap Concept](#1-heap-concept)
2. [Python heapq Module](#2-python-heapq-module)
3. [Basic Operations](#3-basic-operations)
4. [Max Heap Using Negation Trick](#4-max-heap-using-negation-trick)
5. [nlargest and nsmallest](#5-nlargest-and-nsmallest)
6. [Custom Comparison with Heaps](#6-custom-comparison-with-heaps)
7. [Merge K Sorted Arrays](#7-merge-k-sorted-arrays)
8. [Find Median from Data Stream](#8-find-median-from-data-stream)

---

## 1. Heap Concept

A **heap** is a complete binary tree that satisfies the **heap property**:
- **Min Heap**: Parent ≤ Children (smallest element at root)
- **Max Heap**: Parent ≥ Children (largest element at root)

```
Min Heap:          Max Heap:
      1                  9
     / \                / \
    3   2              7   8
   / \                / \
  5   4              3   6
```

**Array Representation** (0-indexed):
- Parent of node at index `i`: `(i - 1) // 2`
- Left child of node at index `i`: `2 * i + 1`
- Right child of node at index `i`: `2 * i + 2`

**Time Complexities**:
| Operation | Time Complexity |
|-----------|----------------|
| Insert    | O(log n)       |
| Extract Min/Max | O(log n) |
| Peek      | O(1)           |
| Build Heap | O(n)          |
| Heapify   | O(log n)       |

---

## 2. Python heapq Module

Python's `heapq` module provides a **min-heap** implementation as a list.

```python
import heapq

# Initialize a heap
heap = []

# Push elements
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 4)
heapq.heappush(heap, 1)
heapq.heappush(heap, 5)

print(heap)  # [1, 1, 4, 3, 5] - min heap property maintained

# Pop minimum element
min_val = heapq.heappop(heap)
print(min_val)  # 1
print(heap)     # [1, 4, 3, 5]
```

---

## 3. Basic Operations

### heapify - Convert list to heap in O(n)

```python
import heapq

# Convert a list to a heap in-place
arr = [5, 3, 8, 1, 2]
heapq.heapify(arr)
print(arr)  # [1, 2, 8, 3, 5] - min heap

# Peek at minimum element
print(arr[0])  # 1

# Get sorted version (heap sort)
sorted_arr = [heapq.heappop(arr) for _ in range(len(arr))]
print(sorted_arr)  # [1, 2, 3, 5, 8]
```

### heappush and heappop

```python
import heapq

def demonstrate_operations():
    heap = []
    elements = [15, 10, 20, 8, 12, 25, 5]
    
    # Build heap by pushing elements one by one
    for elem in elements:
        heapq.heappush(heap, elem)
        print(f"After pushing {elem}: {heap}")
    
    # Extract elements in sorted order
    result = []
    while heap:
        result.append(heapq.heappop(heap))
    
    print(f"Sorted extraction: {result}")

demonstrate_operations()
# Output: [5, 8, 10, 12, 15, 20, 25]
```

### heappushpop and heapreplace

```python
import heapq

# heappushpop: push then pop (more efficient)
heap = [1, 3, 5, 7, 9]
result = heapq.heappushpop(heap, 2)
print(result)  # 1 (popped min)
print(heap)    # [2, 3, 5, 7, 9]

# heapreplace: pop then push (must have at least one element)
result = heapq.heapreplace(heap, 0)
print(result)  # 2 (popped min)
print(heap)    # [0, 3, 5, 7, 9]
```

---

## 4. Max Heap Using Negation Trick

Python's `heapq` only provides min-heap. For max-heap, negate all values:

```python
import heapq

# Max heap using negation trick
max_heap = []
elements = [15, 10, 20, 8, 12, 25, 5]

# Push negated values
for elem in elements:
    heapq.heappush(max_heap, -elem)

# Pop maximum (negate back)
result = []
while max_heap:
    result.append(-heapq.heappop(max_heap))

print(result)  # [25, 20, 15, 12, 10, 8, 5]

# Helper class for max heap
class MaxHeap:
    def __init__(self):
        self.heap = []
    
    def push(self, val):
        heapq.heappush(self.heap, -val)
    
    def pop(self):
        return -heapq.heappop(self.heap)
    
    def peek(self):
        return -self.heap[0]
    
    def size(self):
        return len(self.heap)
    
    def is_empty(self):
        return len(self.heap) == 0

# Usage
max_h = MaxHeap()
for val in [1, 5, 3, 7, 2]:
    max_h.push(val)

print(max_h.pop())  # 7
print(max_h.pop())  # 5
```

---

## 5. nlargest and nsmallest

```python
import heapq

arr = [4, 1, 7, 3, 8, 2, 6, 5]

# Find k largest elements
k = 3
largest = heapq.nlargest(k, arr)
print(f"{k} largest: {largest}")  # [8, 7, 6]

# Find k smallest elements
smallest = heapq.nsmallest(k, arr)
print(f"{k} smallest: {smallest}")  # [1, 2, 3]

# With custom key function
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78), ("Diana", 95)]

# Top 2 students by score
top_students = heapq.nlargest(2, students, key=lambda x: x[1])
print(top_students)  # [('Diana', 95), ('Bob', 92)]

# Bottom 2 students by score
bottom_students = heapq.nsmallest(2, students, key=lambda x: x[1])
print(bottom_students)  # [('Charlie', 78), ('Alice', 85)]
```

---

## 6. Custom Comparison with Heaps

```python
import heapq

# Custom object with comparison
class Task:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority
    
    # For min-heap based on priority
    def __lt__(self, other):
        return self.priority < other.priority
    
    def __repr__(self):
        return f"Task({self.name}, {self.priority})"

# Priority queue
task_queue = []
heapq.heappush(task_queue, Task("Low priority task", 5))
heapq.heappush(task_queue, Task("High priority task", 1))
heapq.heappush(task_queue, Task("Medium priority task", 3))

# Process tasks in priority order
while task_queue:
    task = heapq.heappop(task_queue)
    print(f"Processing: {task}")
# Processing: Task(High priority task, 1)
# Processing: Task(Medium priority task, 3)
# Processing: Task(Low priority task, 5)

# Custom comparison for tuples
# Sort by first element, then by second
pairs = [(3, 'c'), (1, 'a'), (1, 'b'), (2, 'a')]
heapq.heapify(pairs)
print(pairs)  # [(1, 'a'), (1, 'b'), (3, 'c'), (2, 'a')]
```

---

## 7. Merge K Sorted Arrays

### Method 1: Using Min Heap - O(N log k)

```python
import heapq

def merge_k_sorted_arrays(arrays):
    """Merge k sorted arrays into one sorted array."""
    result = []
    min_heap = []
    
    # Push first element of each array with array index and element index
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(min_heap, (arr[0], i, 0))
    
    while min_heap:
        val, arr_idx, elem_idx = heapq.heappop(min_heap)
        result.append(val)
        
        # Push next element from the same array
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(min_heap, (next_val, arr_idx, elem_idx + 1))
    
    return result

# Example
arrays = [
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9]
]
print(merge_k_sorted_arrays(arrays))
# Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Method 2: Using Divide and Conquer - O(N log k)

```python
import heapq

def merge_two_sorted(arr1, arr2):
    """Merge two sorted arrays."""
    result = []
    i = j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result

def merge_k_sorted_dc(arrays):
    """Merge k sorted arrays using divide and conquer."""
    if not arrays:
        return []
    
    while len(arrays) > 1:
        merged = []
        for i in range(0, len(arrays), 2):
            if i + 1 < len(arrays):
                merged.append(merge_two_sorted(arrays[i], arrays[i + 1]))
            else:
                merged.append(arrays[i])
        arrays = merged
    
    return arrays[0]

# Example
arrays = [
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9]
]
print(merge_k_sorted_dc(arrays))
# Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

## 8. Find Median from Data Stream

### Using Two Heaps

```python
import heapq

class MedianFinder:
    """Find median from a data stream using two heaps."""
    
    def __init__(self):
        # Max heap for lower half (negate values)
        self.lower = []  # max heap
        # Min heap for upper half
        self.upper = []  # min heap
    
    def add_number(self, num):
        """Add a number to the data structure."""
        # Push to max heap (negate for max heap behavior)
        heapq.heappush(self.lower, -num)
        
        # Ensure max of lower <= min of upper
        if self.upper and -self.lower[0] > self.upper[0]:
            val = -heapq.heappop(self.lower)
            heapq.heappush(self.upper, val)
        
        # Balance sizes: lower can have at most 1 more than upper
        if len(self.lower) > len(self.upper) + 1:
            val = -heapq.heappop(self.lower)
            heapq.heappush(self.upper, val)
        elif len(self.upper) > len(self.lower):
            val = heapq.heappop(self.upper)
            heapq.heappush(self.lower, -val)
    
    def find_median(self):
        """Find the current median."""
        if len(self.lower) == len(self.upper):
            return (-self.lower[0] + self.upper[0]) / 2.0
        else:
            return float(-self.lower[0])

# Example usage
mf = MedianFinder()
numbers = [5, 15, 1, 3, 8, 7, 9]

for num in numbers:
    mf.add_number(num)
    print(f"Added {num}, median = {mf.find_median()}")

# Output:
# Added 5, median = 5
# Added 15, median = 10.0
# Added 1, median = 5
# Added 3, median = 4.0
# Added 8, median = 5
# Added 7, median = 6.0
# Added 9, median = 7
```

### Alternative: Using SortedList (O(log n) insert, O(1) median)

```python
from sortedcontainers import SortedList

class MedianFinderSorted:
    def __init__(self):
        self.data = SortedList()
    
    def add_number(self, num):
        self.data.add(num)
    
    def find_median(self):
        n = len(self.data)
        if n % 2 == 1:
            return self.data[n // 2]
        else:
            return (self.data[n // 2 - 1] + self.data[n // 2]) / 2.0
```

---

## Quick Reference: Heap Patterns

| Problem Pattern | Approach |
|----------------|----------|
| Top K elements | Min heap of size K |
| Kth smallest/largest | Min/Max heap |
| Merge K sorted | Min heap with K pointers |
| Running median | Two heaps (min + max) |
| Sliding window max | Deque (monotonic) |
| Task scheduling | Max heap + frequency |

---

## Common Pitfalls

1. **Forgetting negation**: `heapq` is min-heap only; negate for max-heap
2. **Off-by-one in index math**: Left child = `2*i+1`, Right = `2*i+2`
3. **heapify is O(n)**, not O(n log n) - don't push one by one when building
4. **heappushpop** is faster than push + pop separately
5. **heapreplace** requires at least one element in heap
