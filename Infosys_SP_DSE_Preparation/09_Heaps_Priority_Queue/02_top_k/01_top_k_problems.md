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

### Key Insight

```
Two approaches:
1. Min-heap of size k  → O(n log k)  — good for any input
2. Bucket sort        → O(n)         — best when values are bounded integers

The min-heap approach:
  - Count frequencies first (O(n))
  - For each element, push (freq, num) to a min-heap of size k
  - If heap exceeds k, pop the smallest frequency (least frequent)
  - At the end, heap contains the k most frequent elements
```

### Method 1: Min Heap - O(n log k)

```python
import heapq
from collections import Counter

def top_k_frequent(nums, k):
    """Find k most frequent elements using a min-heap of size k.
    
    Why min-heap? We want to keep the k LARGEST frequencies.
    A min-heap lets us efficiently evict the SMALLEST frequency
    when we have more than k elements.
    """
    # Count frequencies: O(n)
    count = Counter(nums)
    
    # Min-heap of size k, storing (frequency, number)
    min_heap = []
    for num, freq in count.items():
        heapq.heappush(min_heap, (freq, num))
        if len(min_heap) > k:
            heapq.heappop(min_heap)  # Evict least frequent
    
    return [num for freq, num in min_heap]

# Example
nums = [1, 1, 1, 2, 2, 3]
k = 2
print(top_k_frequent(nums, k))  # [1, 2]
```

### Visual: Step-by-Step Walkthrough

```
Input: nums = [1, 1, 1, 2, 2, 3],  k = 2

Step 1: Count frequencies
  Counter: {1: 3, 2: 2, 3: 1}

Step 2: Process each (freq, num) pair

  Push (3, 1): heap = [(3, 1)]
  Size 1 ≤ k=2 → no pop
  
  3
  (1 appears 3 times)

  Push (2, 2): heap = [(2, 2), (3, 1)]
  Size 2 ≤ k=2 → no pop
  
  (2,2)
     \
     (3,1)
  
  Push (1, 3): heap = [(1, 3), (3, 1), (2, 2)]
  Size 3 > k=2 → pop smallest! Pop (1, 3)
  heap = [(2, 2), (3, 1)]
  
  (2,2)          ← This is now the root (smallest freq in heap)
     \
     (3,1)

Final heap: [(2, 2), (3, 1)]
  → nums with freq 2 and 3 → [2, 1] (or [1, 2])
  
Result: [1, 2]  ✓ (1 appears 3 times, 2 appears 2 times — top 2)
```

### Method 2: Bucket Sort - O(n)

```python
from collections import Counter

def top_k_frequent_bucket(nums, k):
    """Find k most frequent elements using bucket sort.
    
    Key insight: frequency can range from 1 to n (at most n occurrences).
    Create n+1 buckets where bucket[i] = list of elements with frequency i.
    Then scan from highest frequency down to collect top k.
    """
    count = Counter(nums)
    
    # Create buckets: index = frequency, value = list of numbers with that freq
    # If n=6, max possible frequency is 6, so we need buckets[0..6]
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)
    
    # Collect top k from highest frequency bucket downward
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

### Visual: Bucket Sort Approach

```
Input: nums = [1, 1, 1, 2, 2, 3],  n = 6

Step 1: Count frequencies → {1:3, 2:2, 3:1}

Step 2: Create buckets (index = frequency)
  Bucket:    0     1      2      3      4      5      6
  Contents: []   [3]    [2]    [1]     []     []     []
                        ↑      ↑
                      freq=2  freq=3

Step 3: Scan from highest bucket (index 6) down to 1
  
  Bucket 6: empty
  Bucket 5: empty
  Bucket 4: empty
  Bucket 3: [1] → add 1. result = [1]
  Bucket 2: [2] → add 2. result = [1, 2]. len=2=k, STOP!

Result: [1, 2]  ✓

Time complexity: O(n) — counting is O(n), bucket creation is O(n),
scanning is O(n). Everything is linear!
Space: O(n) for buckets and counter.
```

---

## 2. Kth Largest Element in Array

**Problem**: Find the kth largest element in an unsorted array.

### Key Insight

```
The "Kth Largest" trick:
  To find the kth LARGEST, maintain a min-heap of size k.
  The root of this heap IS the kth largest element!
  
  Why? The heap always contains the k largest elements seen so far.
  Since it's a min-heap, the root is the smallest among those k largest
  = the kth largest overall.

  Example: k=2, array = [3, 2, 1, 5, 6, 4]
  
  After processing all elements, heap = [5, 6]
  Root = 5 = 2nd largest ✓
```

### Method 1: Min Heap of size k - O(n log k)

```python
import heapq

def find_kth_largest(nums, k):
    """Find kth largest element using a min-heap of size k.
    
    Algorithm:
    1. Build a min-heap from the first k elements
    2. For each remaining element, if it's larger than the root,
       replace the root (the current kth largest candidate)
    3. The root at the end is the answer
    """
    # Build min-heap from first k elements: O(k)
    min_heap = nums[:k]
    heapq.heapify(min_heap)
    
    # Process remaining elements
    for num in nums[k:]:
        if num > min_heap[0]:  # num is larger than current kth largest
            heapq.heapreplace(min_heap, num)  # Evict root, insert num
    
    # Root is the kth largest
    return min_heap[0]

# Example
nums = [3, 2, 1, 5, 6, 4]
k = 2
print(find_kth_largest(nums, k))  # 5
```

### Visual: Step-by-Step Walkthrough

```
Input: nums = [3, 2, 1, 5, 6, 4],  k = 2

Step 1: Build min-heap from first k=2 elements
  heap = [3, 2]  → heapify → [2, 3]
  
    2      ← root = 2nd largest so far
    |
    3

Step 2: Process nums[2:] = [1, 5, 6, 4]

  num=1: 1 > heap[0]=2? NO → skip.   heap = [2, 3]
  
  num=5: 5 > heap[0]=2? YES → replace!
    heap = [5, 3]  (3 moves to root, 5 sifts up)
    
    3      ← new root = 3 (2nd largest so far)
    |
    5

  num=6: 6 > heap[0]=3? YES → replace!
    heap = [6, 5]  (5 moves to root, 6 sifts up)
    
    5      ← new root = 5 (2nd largest so far)
    |
    6

  num=4: 4 > heap[0]=5? NO → skip.   heap = [5, 6]

Final heap = [5, 6]
  Root = 5 = 2nd largest element ✓
  
Sorted check: [1, 2, 3, 4, 5, 6] → 2nd largest = 5 ✓
```

### Method 2: Max Heap - O(n log n)

```python
import heapq

def find_kth_largest_max_heap(nums, k):
    """Find kth largest using max-heap (negation trick).
    
    Strategy: negate all values, build max-heap, pop k-1 times.
    The kth pop gives the kth largest.
    """
    # Negate all values for max-heap behavior
    max_heap = [-num for num in nums]
    heapq.heapify(max_heap)  # O(n)
    
    # Pop k-1 times to remove the (k-1) largest elements
    for _ in range(k - 1):
        heapq.heappop(max_heap)  # O(log n) each
    
    # The next element is the kth largest
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
    """Find kth largest using quickselect (average O(n)).
    
    Quickselect is like quicksort but only recurses into ONE partition.
    Convert "kth largest" to "kth smallest" via index math:
      kth largest in array of size n = (n - k)th smallest
    
    Time: O(n) average, O(n²) worst case (randomized pivot avoids this)
    Space: O(1) in-place
    """
    target = len(nums) - k  # Convert to kth smallest
    
    def quickselect(left, right):
        if left == right:
            return nums[left]
        
        # Random pivot to avoid worst case O(n²)
        pivot_idx = random.randint(left, right)
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        pivot = nums[right]
        
        # Partition: all elements < pivot go to the left
        store_idx = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[store_idx], nums[i] = nums[i], nums[store_idx]
                store_idx += 1
        nums[store_idx], nums[right] = nums[right], nums[store_idx]
        
        # Check if pivot is at the target position
        if store_idx == target:
            return nums[store_idx]
        elif store_idx < target:
            return quickselect(store_idx + 1, right)  # Search right
        else:
            return quickselect(left, store_idx - 1)    # Search left
    
    return quickselect(0, len(nums) - 1)

# Example
nums = [3, 2, 1, 5, 6, 4]
k = 2
print(find_kth_largest_quickselect(nums, k))  # 5
```

### Visual: Quickselect Walkthrough

```
Input: nums = [3, 2, 1, 5, 6, 4],  k = 2
Target index: n - k = 6 - 2 = 4  (4th smallest = 2nd largest)

Partition around pivot=4 (moved to end):
  [3, 2, 1, 5, 6, |4]
  
  After partition: [3, 2, 1, 4, 6, 5]
                    store_idx=4 (pivot at index 3)
  
  Wait — let me re-trace. Elements < 4: 3, 2, 1.
  store_idx starts at 0.
  3 < 4: swap nums[0]↔nums[0], store=1  → [3, 2, 1, 5, 6, 4]
  2 < 4: swap nums[1]↔nums[1], store=2  → [3, 2, 1, 5, 6, 4]
  1 < 4: swap nums[2]↔nums[2], store=3  → [3, 2, 1, 5, 6, 4]
  5 < 4: NO
  6 < 4: NO
  
  Final: swap pivot (4) with store_idx (3):
  [3, 2, 1, 4, 6, 5]  → pivot at index 3
  
  store_idx=3 < target=4 → search RIGHT: quickselect(4, 5)

Next partition: nums[4:6] = [6, 5], target=4
  Pivot = 5 (or 6, randomized). Let's say pivot=5:
  [6, 5] → 6 < 5? NO → pivot stays at index 5
  store_idx=4, swap pivot(5) with store_idx(4): [5, 6]
  store_idx=4 == target=4 → return 5 ✓

Answer: 5 = 2nd largest ✓
```

---

## 3. Kth Smallest Element in Sorted Matrix

**Problem**: Given an `n x n` matrix where each row and column is sorted, find the kth smallest element.

### Key Insight

```
The matrix is sorted both row-wise and column-wise:

  1   5   9
  10  11  13
  12  13  15

This means:
  - Each row is sorted left to right
  - Each column is sorted top to bottom
  - The smallest is always at top-left (matrix[0][0])
  - The largest is always at bottom-right (matrix[n-1][n-1])

Two approaches:
  1. Min-heap: Push first element of each row, pop k times → O(k log n)
  2. Binary search: Search for the answer in value space → O(n log(max-min))
```

### Method 1: Min Heap - O(k log n)

```python
import heapq

def kth_smallest_matrix(matrix, k):
    """Find kth smallest in sorted matrix using min-heap.
    
    Strategy: Push the first element of each row into the heap.
    Each pop gives the next smallest, and we push the next element
    from that row. This is like merging n sorted arrays!
    """
    n = len(matrix)
    # Push (value, row, col) for first element of each row
    min_heap = [(matrix[i][0], i, 0) for i in range(min(n, k))]
    heapq.heapify(min_heap)
    
    # Pop k times to get the kth smallest
    for _ in range(k):
        val, row, col = heapq.heappop(min_heap)
        # Push next element in the same row (if exists)
        if col + 1 < n:
            heapq.heappush(min_heap, (matrix[row][col + 1], row, col + 1))
    
    return val  # The kth popped value

# Example
matrix = [
    [1,  5,  9],
    [10, 11, 13],
    [12, 13, 15]
]
k = 8
print(kth_smallest_matrix(matrix, k))  # 13
```

### Visual: Step-by-Step Heap Walkthrough

```
Matrix:
  1   5   9
  10  11  13
  12  13  15

k = 8 (find 8th smallest)

Initial heap: push first element of each row
  [(1,0,0), (10,1,0), (12,2,0)]
  
    (1, row=0)        ← smallest
    /       \
  (10,r=1)  (12,r=2)

Pop 1st: (1,0,0) → output 1. Push (5,0,1) from row 0.
  [(5,0,1), (10,1,0), (12,2,0)]
  
Pop 2nd: (5,0,1) → output 5. Push (9,0,2) from row 0.
  [(9,0,2), (10,1,0), (12,2,0)]

Pop 3rd: (9,0,2) → output 9. No more in row 0.
  [(10,1,0), (12,2,0)]

Pop 4th: (10,1,0) → output 10. Push (11,1,1) from row 1.
  [(11,1,1), (12,2,0)]

Pop 5th: (11,1,1) → output 11. Push (13,1,2) from row 1.
  [(12,2,0), (13,1,2)]

Pop 6th: (12,2,0) → output 12. Push (13,2,1) from row 2.
  [(13,2,1), (13,1,2)]   ← two 13s from different rows!

Pop 7th: (13,2,1) → output 13. Push (15,2,2) from row 2.
  [(13,1,2), (15,2,2)]

Pop 8th: (13,1,2) → output 13. ← THIS IS THE ANSWER!

8th smallest = 13 ✓

Sorted order: 1, 5, 9, 10, 11, 12, 13, [13], 15
                                   7th   8th
```

### Method 2: Binary Search - O(n log(max-min))

```python
def kth_smallest_matrix_binary(matrix, k):
    """Find kth smallest using binary search on VALUE space.
    
    Instead of searching the array, search the possible answer values.
    For a candidate mid, count how many elements are <= mid.
    If count < k, the answer is larger than mid.
    If count >= k, the answer is <= mid.
    """
    n = len(matrix)
    
    def count_less_equal(mid):
        """Count elements <= mid in the matrix. O(n) time.
        
        Start from bottom-left corner:
        - If current element <= mid, all elements above are too → count += row+1
        - Move right to find larger elements
        - If current element > mid, move up to find smaller elements
        """
        count = 0
        row, col = n - 1, 0  # Start bottom-left
        
        while row >= 0 and col < n:
            if matrix[row][col] <= mid:
                # Everything above this cell in this column is also <= mid
                count += row + 1
                col += 1  # Move right
            else:
                row -= 1  # Move up
        
        return count
    
    # Binary search on value space
    lo, hi = matrix[0][0], matrix[-1][-1]
    
    while lo < hi:
        mid = (lo + hi) // 2
        if count_less_equal(mid) < k:
            lo = mid + 1   # Need larger values
        else:
            hi = mid       # Answer could be mid or smaller
    
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

### Visual: Binary Search Count Walkthrough

```
Matrix:
  1   5   9
  10  11  13
  12  13  15

Binary search: lo=1, hi=15, k=8

mid = 8: count elements <= 8
  Start bottom-left (12): 12 > 8 → move up (10)
  10 > 8 → move up (1)
  1 <= 8 → count += 1 (row+1 = 0+1 = 1), move right (5)
  5 <= 8 → count += 1, move right (9)
  9 > 8 → move up (out of bounds)
  count = 2 < 8 → lo = 9

mid = 12: count elements <= 12
  (12,0): 12 <= 12 → count += 1 (row+1 = 3), move right (col=1)
  (13,1): 13 > 12 → move up (11)
  (11,1): 11 <= 12 → count += 2 (row+1 = 1+1 = 2), move right (col=2)
  (13,2): 13 > 12 → move up (9)
  (9,2): 9 <= 12 → count += 1, move right (out)
  count = 3+2+1 = 6 < 8 → lo = 13

mid = 13: count elements <= 13
  (12,0): 13 <= 13 → count += 3, move right
  (13,1): 13 <= 13 → count += 2, move right
  (15,2): 15 > 13 → move up (13)
  (13,2): 13 <= 13 → count += 1
  count = 3+2+1+1 = 7 < 8 → lo = 14

mid = 14: count elements <= 14
  Same as <= 13: count = 7 < 8 → lo = 15

lo = 15, hi = 15 → return 15? That seems wrong...

Let me recount for mid=13:
  Start (2,0)=12: 12<=13, count += 3 (all of col 0: 1,10,12), col=1
  (2,1)=13: 13<=13, count += 3 (all of col 1: 5,11,13), col=2
  (2,2)=15: 15>13, row=1
  (1,2)=13: 13<=13, count += 2 (rows 0-1 of col 2: 9,13), col=3 (exit)
  count = 3+3+2 = 8 >= 8 → hi = 13

mid = 12: count = 6 (shown above) < 8 → lo = 13

lo = hi = 13 → return 13 ✓
```

---

## 4. K Closest Points to Origin

**Problem**: Find the k closest points to the origin (0, 0).

### Key Insight

```
Distance from origin: sqrt(x² + y²)
We only need to compare distances, so we can use x² + y² (skip sqrt).

Strategy: Use a min-heap OR a max-heap of size k.

Max-heap approach (more efficient for k << n):
  - Maintain a max-heap of size k storing (-distance, x, y)
  - For each new point, if closer than the farthest in heap, replace it
  - Negate distance because heapq is min-heap (negation = max-heap)
```

```python
import heapq
import math

def k_closest_points(points, k):
    """Find k closest points to origin using a max-heap of size k.
    
    The max-heap stores the k closest points seen so far.
    The root is the FARTHEST of the k closest — if a new point
    is closer, we replace the root.
    """
    # Max-heap storing (-distance, x, y)
    max_heap = []
    
    for x, y in points:
        dist = x**2 + y**2  # Skip sqrt — only comparing, not measuring
        heapq.heappush(max_heap, (-dist, x, y))
        if len(max_heap) > k:
            heapq.heappop(max_heap)  # Remove farthest
    
    return [(x, y) for _, x, y in max_heap]

# Or more Pythonic version using nlargest/nsmallest
def k_closest_pythonic(points, k):
    """Find k closest points to origin using nlargest."""
    return heapq.nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2)

# Example
points = [[3, 3], [5, -1], [-2, 4], [1, 1]]
k = 2
print(k_closest_pythonic(points, k))  # [[1, 1], [3, 3]]
```

### Visual: Step-by-Step Walkthrough

```
Points: [(3,3), (5,-1), (-2,4), (1,1)],  k = 2

Distances: (3,3)→18, (5,-1)→26, (-2,4)→20, (1,1)→2

Process (3,3): dist=18
  heap = [(-18, 3, 3)]
  
  Point (3,3)       Farthest: (3,3) dist=18

Process (5,-1): dist=26
  heap = [(-26, 5,-1), (-18, 3, 3)]
  Size 2 = k → no pop
  
  Point (3,3)  Point (5,-1)
               Farthest: (5,-1) dist=26

Process (-2,4): dist=20
  20 > 26 (farthest)? NO, 20 < 26. Push and pop:
  Actually: -20 > -26? YES → push (-20, -2, 4), pop (-26, 5, -1)
  heap = [(-20, -2, 4), (-18, 3, 3)]
  
  Point (3,3)  Point (-2,4)
               Farthest: (-2,4) dist=20

Process (1,1): dist=2
  2 > 20 (farthest)? NO, 2 < 20. Push and pop:
  -2 > -20? YES → push (-2, 1, 1), pop (-20, -2, 4)
  heap = [(-18, 3, 3), (-2, 1, 1)]
  
  Point (3,3)  Point (1,1)
               Farthest: (3,3) dist=18

Final: [(3,3), (1,1)] → the 2 closest points ✓
Distances: 18 and 2 (both closer than removed 20 and 26)
```

---

## 5. Kth Largest in Stream

**Problem**: Design a class to find the kth largest element in a stream.

### Key Insight

```
Same as "Kth Largest in Array" but adapted for streaming data.

Maintain a min-heap of size k:
  - Heap always contains the k largest elements seen so far
  - Root = kth largest overall
  - New element arrives: if larger than root, replace root
  - Return root as the answer

This is the STANDARD pattern for "kth largest in stream" problems.
```

```python
import heapq

class KthLargest:
    """Find kth largest element in a stream.
    
    Maintain a min-heap of size k. The root is the kth largest.
    When a new value arrives:
      - If heap has room: push it
      - If value > root: replace root (evict the old kth largest)
      - Return root
    """
    
    def __init__(self, k, nums):
        """
        :type k: int — the k in "kth largest"
        :type nums: List[int] — initial numbers in the stream
        """
        self.k = k
        # Build min-heap from first k elements
        self.min_heap = nums[:k]
        heapq.heapify(self.min_heap)
        
        # Process remaining elements
        for num in nums[k:]:
            if num > self.min_heap[0]:
                heapq.heapreplace(self.min_heap, num)
    
    def add(self, val):
        """
        Add val to stream and return kth largest.
        :type val: int
        :rtype: int — the kth largest element after adding val
        Time: O(log k)
        """
        if len(self.min_heap) < self.k:
            # Heap not full yet, just push
            heapq.heappush(self.min_heap, val)
        elif val > self.min_heap[0]:
            # New val is larger than current kth largest — replace
            heapq.heapreplace(self.min_heap, val)
        
        # Root is always the kth largest
        return self.min_heap[0]

# Example
k = 3
nums = [4, 5, 8, 2]
kth_largest = KthLargest(k, nums)

print(kth_largest.add(3))   # 4  — heap: [4, 5, 8], 4 is 3rd largest
print(kth_largest.add(5))   # 5  — heap: [5, 5, 8], 5 replaces 4
print(kth_largest.add(10))  # 5  — heap: [5, 8, 10], 10 replaces 5
print(kth_largest.add(9))   # 8  — heap: [8, 9, 10], 9 replaces 5, 8 is root
print(kth_largest.add(4))   # 8  — heap unchanged (4 < 8)
```

### Visual: Stream Processing Walkthrough

```
k = 3, initial nums = [4, 5, 8, 2]

After init: heap = [4, 5, 8] (3 largest: 8, 5, 4)
  4       ← root = 4 = 3rd largest
 / \
5   8

add(3): 3 > 4? NO → heap unchanged → return 4
  heap = [4, 5, 8]
  Stream so far: [4, 5, 8, 2, 3]
  3 largest: 8, 5, 4 → 3rd largest = 4 ✓

add(5): 5 > 4? YES → replace 4 with 5 → heap = [5, 5, 8]
  5       ← root = 5 = 3rd largest
 / \
5   8
  Stream so far: [4, 5, 8, 2, 3, 5]
  3 largest: 8, 5, 5 → 3rd largest = 5 ✓

add(10): 10 > 5? YES → replace 5 with 10 → heap = [5, 8, 10]
  5       ← root = 5
 / \
8   10
  3 largest: 10, 8, 5 → 3rd largest = 5 ✓

add(9): 9 > 5? YES → replace 5 with 9 → heap = [8, 9, 10]
  8       ← root = 8
 / \
9   10
  3 largest: 10, 9, 8 → 3rd largest = 8 ✓

add(4): 4 > 8? NO → heap unchanged → return 8
  3 largest: 10, 9, 8 → 3rd largest = 8 ✓
```

---

## 6. Sort Array by Frequency

**Problem**: Sort an array by frequency of elements. If two elements have the same frequency, sort them by value (descending).

### Key Insight

```
We need: highest frequency first, then highest value for ties.

Approach: Max-heap with tuple (-frequency, -value).
  - Negate frequency so most frequent pops first
  - Negate value so larger value breaks ties first
```

```python
import heapq
from collections import Counter

def frequency_sort(nums):
    """Sort array by frequency using a max-heap.
    
    Heap entry: (-frequency, -value)
    - Most frequent pops first (most negative frequency = highest)
    - Same frequency → higher value pops first (more negative value)
    """
    count = Counter(nums)
    
    # Max-heap: (-frequency, -value)
    max_heap = [(-freq, -num) for num, freq in count.items()]
    heapq.heapify(max_heap)
    
    result = []
    while max_heap:
        freq, num = heapq.heappop(max_heap)
        result.extend([-num] * -freq)  # Repeat num freq times
    
    return result

# Alternative: Using sorted() — simpler but O(n log n)
def frequency_sort_v2(nums):
    count = Counter(nums)
    # Sort by (-frequency, -value) — same ordering as heap
    return sorted(nums, key=lambda x: (-count[x], -x))

# Example
nums = [2, 3, 5, 3, 7, 9, 5, 3, 7]
print(frequency_sort(nums))  # [3, 3, 3, 7, 7, 5, 5, 2, 9]
```

### Visual: Walkthrough

```
Input: [2, 3, 5, 3, 7, 9, 5, 3, 7]

Counter: {2:1, 3:3, 5:2, 7:2, 9:1}

Heap entries: [(-3,-3), (-2,-5), (-2,-7), (-1,-2), (-1,-9)]
              freq=3     freq=2     freq=2     freq=1     freq=1
              val=3      val=5      val=7      val=2      val=9

Pop order:
  1. (-3, -3) → 3 appears 3 times → [3, 3, 3]
  2. (-2, -7) → 7 appears 2 times → [3, 3, 3, 7, 7]
  3. (-2, -5) → 5 appears 2 times → [3, 3, 3, 7, 7, 5, 5]
  4. (-1, -9) → 9 appears 1 time  → [3, 3, 3, 7, 7, 5, 5, 9]
  5. (-1, -2) → 2 appears 1 time  → [3, 3, 3, 7, 7, 5, 5, 9, 2]

Wait — tie-breaking: (-1, -9) vs (-1, -2). 
(-1, -9) < (-1, -2)? Yes, because -9 < -2. So 9 pops before 2.
But the expected output was [3, 3, 3, 7, 7, 5, 5, 2, 9].

Hmm — the problem says "same frequency, sort by value". If descending:
  Same freq=1: 9 should come before 2 (larger first)
  So output: [3, 3, 3, 7, 7, 5, 5, 9, 2] ← correct with our ordering!

But the original output showed [3, 3, 3, 7, 7, 5, 5, 2, 9].
That would be ascending value for ties. Adjust the tuple to (-freq, num)
if ascending tie-break is desired.

Either way, the HEAP PATTERN is the key takeaway.
```

---

## 7. Reorganize String

**Problem**: Rearrange string so that no two adjacent characters are the same. Return empty string if not possible.

### Key Insight

```
Greedy approach: Always place the MOST FREQUENT remaining character
that is NOT the previously placed character.

If impossible: any character appears more than (n+1)//2 times.

Why (n+1)//2? For n characters, you can place at most ceil(n/2) of
one type by alternating: a_x_a_x_a (for n=5, max 3 of one type).
```

```python
import heapq
from collections import Counter

def reorganize_string(s):
    """Reorganize string so no adjacent chars are same.
    
    Algorithm:
    1. Check if possible (max freq <= (n+1)//2)
    2. Use max-heap to always pick the most frequent remaining char
    3. Hold the previously used char aside (can't reuse immediately)
    4. After placing a char, push the previous char back if it still has count
    """
    count = Counter(s)
    max_count = max(count.values())
    n = len(s)
    
    # If any character appears more than (n+1)//2 times, impossible
    if max_count > (n + 1) // 2:
        return ""
    
    # Max-heap: (-frequency, char)
    max_heap = [(-freq, char) for char, freq in count.items()]
    heapq.heapify(max_heap)
    
    result = []
    prev = None  # The character we just used (can't reuse immediately)
    
    while max_heap:
        freq, char = heapq.heappop(max_heap)
        result.append(char)
        
        # Push back the previous character (it's available again now)
        if prev:
            heapq.heappush(max_heap, prev)
            prev = None
        
        # If this character still has remaining count, hold it aside
        if freq + 1 < 0:  # freq is negative, so +1 means one less occurrence
            prev = (freq + 1, char)
    
    return ''.join(result)

# Example
print(reorganize_string("aab"))   # "aba"
print(reorganize_string("aaab"))  # "" (impossible: 'a' appears 3 times > (4+1)//2=2)
```

### Visual: Step-by-Step Walkthrough

```
Input: s = "aab"

Counter: {'a': 2, 'b': 1}
Check: max_count=2 <= (3+1)//2=2 → possible ✓

Initial heap: [(-2, 'a'), (-1, 'b')]

Step 1: Pop (-2, 'a') → result = ['a'], prev = None
  'a' has remaining: -2+1=-1 < 0 → hold prev = (-1, 'a')
  result = "a"
  prev = ('a')

Step 2: Pop (-1, 'b') → result = ['a','b'], prev = ('a')
  Push back prev ('a'): heap = [(-1, 'a')]
  'b' remaining: -1+1=0 → not held (no more 'b')
  result = "ab"
  prev = None

Step 3: Pop (-1, 'a') → result = ['a','b','a'], prev = None
  Push back prev (None): skip
  'a' remaining: -1+1=0 → not held
  result = "aba"
  prev = None

Final: "aba" ✓ — no adjacent characters are the same!

Input: s = "aaab"

Counter: {'a': 3, 'b': 1}
Check: max_count=3 > (4+1)//2=2 → IMPOSSIBLE → return ""

Why impossible? You'd need to arrange as: a _ a _ a
But that requires 3 'a' and 2 separators — we only have 1 'b'.
```

### Visual: Why (n+1)//2 is the Limit

```
For n=6 characters:
  Maximum of one type: (6+1)//2 = 3
  Valid arrangement: a x a x a _  (3 a's, need at least 2 others)
  
  Impossible with 4 a's: a x a x a x → needs 3 others, but a _ a _ a _ a
  needs 4 others for 4 a's. With only 2 others, we get: a b a b a a → adjacent a's!
  
  Visual test:
  3 a's: a b a c a _  ✓ (interleaved)
  4 a's: a b a c a a  ✗ (last two a's adjacent)
```

---

## 8. Task Scheduler

**Problem**: Given tasks with cooldown period, find minimum intervals to finish all tasks.

### Key Insight

```
This is a GREEDY problem:
  - Always execute the task with the HIGHEST remaining frequency
  - If same task was just executed, wait for cooldown (insert idle)
  - Use a max-heap for frequencies + a cooldown queue

The mathematical formula (when no idle needed):
  result = max(len(tasks), (max_freq - 1) * (n + 1) + count_of_max_freq)
```

```python
import heapq
from collections import Counter

def least_interval(tasks, n):
    """
    Find minimum intervals to complete all tasks.
    
    :param tasks: list of characters representing tasks
    :param n: cooldown period between same tasks
    
    Algorithm:
    1. Count frequencies
    2. Max-heap for frequencies
    3. Execute most frequent task, put it in cooldown
    4. When cooldown expires, push back to heap
    5. Count intervals including idle slots
    """
    count = Counter(tasks)
    
    # Max-heap of frequencies (negate for max-heap)
    max_heap = [-freq for freq in count.values()]
    heapq.heapify(max_heap)
    
    time = 0
    cooldown_queue = []  # (remaining_count, available_time)
    
    while max_heap or cooldown_queue:
        time += 1
        
        if max_heap:
            # Execute most frequent task
            freq = heapq.heappop(max_heap)
            if freq + 1 < 0:  # Still has remaining occurrences
                cooldown_queue.append((freq + 1, time + n))
        
        # Check if any task has finished its cooldown
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

### Visual: Step-by-Step Walkthrough

```
tasks = ["A", "A", "A", "B", "B", "B"],  n = 2

Counter: {'A': 3, 'B': 3}
Heap: [-3, -3]  (both have freq 3)

Time | Action           | Heap After    | Cooldown Queue | Output
-----|------------------|---------------|----------------|--------
  1  | Pop A (freq-3→-2)| [-3, -2]      | [(-2, 1+2=3)] | A
  2  | Pop B (freq-3→-2)| [-2, -2]      | [(-2,3),(-2,4)]| B
  3  | Idle (A still in | [-2, -2]      | [(-2,4)]       | idle
     | cooldown)        |               |                |
  4  | A ready! Push -2 | [-2, -2]      | []             |
     | Pop A (freq-2→-1)| [-2, -1]      | [(-1, 4+2=6)] | A
  5  | Pop B (freq-2→-1)| [-1, -1]      | [(-1,6),(-1,7)]| B
  6  | Idle (both in    | [-1, -1]      | [(-1,7)]       | idle
     | cooldown)        |               |                |
  7  | A ready! Push -1 | [-1, -1]      | []             |
     | Pop A (freq-1→ 0)| [-1]          | []             | A
  8  | Pop B (freq-1→ 0)| []            | []             | B

Total: 8 intervals ✓

Timeline visualization:
  Slot:   1   2   3   4   5   6   7   8
  Task:   A   B   _   A   B   _   A   B
                 ↑           ↑
              idle        idle
  
  A can't run at slot 3 because n=2 means 2 slots between A's.
  B can't run at slot 6 for same reason.
```

### Alternative Mathematical Approach - O(n)

```python
from collections import Counter

def least_interval_math(tasks, n):
    """Mathematical approach for task scheduler — O(n) time, O(1) space.
    
    Key formula: (max_freq - 1) * (n + 1) + count_of_max_freq
    
    Why? The most frequent task creates a framework:
    
      A _ _ A _ _ A
      |  n  |  n  |
      
    With max_freq=3, n=2: framework = (3-1)*(2+1) = 6 slots
    Then add count of max-freq tasks at the end: + max_count
    
    But we might not need all the framework slots if there are
    enough other tasks to fill them. So take max with len(tasks).
    """
    count = Counter(tasks)
    max_freq = max(count.values())
    
    # Count how many tasks share the maximum frequency
    max_count = sum(1 for freq in count.values() if freq == max_freq)
    
    # Framework: (max_freq - 1) full cooldown rounds + max_count tasks at end
    result = (max_freq - 1) * (n + 1) + max_count
    
    # If there are enough tasks to fill every slot without idle, use len(tasks)
    return max(result, len(tasks))

# Example
tasks = ["A", "A", "A", "B", "B", "B"]
n = 2
print(least_interval_math(tasks, n))  # 8
```

### Visual: Mathematical Formula Explained

```
tasks = ["A","A","A","B","B","B"], n = 2

Most frequent task: A with freq=3, count_of_max=2 (both A and B)

Framework:
  A _ _ A _ _ A
  ├───┤ ├───┤
    n     n
  
  Slots used: (3-1) × (2+1) = 6
  
  Then add max_count=2 at the end:
  A _ _ A _ _ A B B  → but that's 9 slots...
  
  Actually: framework = 6 slots, then max_count tasks appended
  A _ _ | A _ _ | A B → framework slots + max_count
  = 6 + 2 = 8

  B can fill some idle slots: A B _ | A B _ | A B → still 8
  
  Result: max(8, len(tasks)=6) = 8 ✓

When formula equals len(tasks):
  tasks = ["A","A","B","C"], n=1
  max_freq=2, max_count=1
  framework = (2-1)*(1+1)+1 = 3
  max(3, 4) = 4 = len(tasks) — no idle needed!
  Arrangement: A B A C ✓
```

---

## Quick Reference: Top K Patterns

| Pattern               | Approach                     | Time           | Space | When to Use                        |
|-----------------------|------------------------------|----------------|-------|------------------------------------|
| Top K Frequent        | Min heap of size K           | O(n log k)     | O(n)  | k << n, any data type              |
| Top K Frequent        | Bucket sort                  | O(n)           | O(n)  | Values are bounded integers        |
| Kth Largest           | Min heap of size K           | O(n log k)     | O(k)  | Simple, reliable, any input        |
| Kth Largest           | Quickselect                  | O(n) avg       | O(1)  | Need O(n), worst case OK           |
| K Closest Points      | Max-heap of size K           | O(n log k)     | O(k)  | Distance metric available          |
| Kth in Sorted Matrix  | Min heap (merge rows)        | O(k log n)     | O(n)  | k is small                         |
| Kth in Sorted Matrix  | Binary search + count        | O(n log(max-min))| O(1)| k is large or n is small           |
| Stream Processing     | Maintain heap of size K      | O(log k) add   | O(k)  | Online/streaming data              |
| Sort by Frequency     | Max-heap with Counter        | O(n log n)     | O(n)  | Custom sort ordering needed        |
| Reorganize String     | Max-heap + hold-previous     | O(n log n)     | O(n)  | No adjacent same chars             |
| Task Scheduler        | Max-heap + cooldown queue    | O(n log n)     | O(n)  | Cooldown/constraint scheduling     |

---

## Tips

1. **Min-heap for "K largest"**: Keep k largest, evict smallest
2. **Max-heap for "K smallest"**: Keep k smallest, evict largest
3. **Bucket sort**: When values are bounded integers — O(n) beats O(n log k)
4. **Quickselect**: Average O(n), but O(n²) worst case — randomized pivot helps
5. **Binary search on answer**: When answer space is monotonic and you can count efficiently
6. **Negation trick**: Always negate for max-heap in Python: `heapq.heappush(h, -val)`
7. **Tuple ordering**: `(freq, val)` sorts by freq first, then val — use negation for reverse
8. **Heap invariant**: heap[0] is always the min (or max if negated). Never trust heap[1:]

### Decision Flowchart: Which Pattern to Use?

```
Problem asks for Kth something?
├── Kth largest/smallest in array?
│   ├── Need O(n)? → Quickselect
│   ├── Need O(log k) per operation? → Min-heap of size k
│   └── Simple solution? → Min-heap of size k
│
├── Top K most frequent?
│   ├── Values bounded? → Bucket sort O(n)
│   └── Any values? → Min-heap of size k
│
├── K closest by distance?
│   └── Max-heap of size k (negate distance)
│
├── Kth in sorted matrix?
│   ├── k small? → Min-heap (merge k rows)
│   └── k large? → Binary search on value
│
├── Stream of data?
│   └── Maintain heap of size k (KthLargest class pattern)
│
└── Rearrange/reorganize?
    ├── No adjacent same? → Max-heap + hold-previous
    └── With cooldown? → Max-heap + cooldown queue
```
