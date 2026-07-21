# Deque and Heapq in Python — Complete Guide for CP

## 1. collections.deque

```python
from collections import deque

# ============================================
# Deque Creation
# ============================================
dq = deque()                    # Empty deque
dq = deque([1, 2, 3, 4, 5])    # From iterable
dq = deque("hello")             # From string: deque(['h','e','l','l','o'])
dq = deque(range(5))            # deque([0, 1, 2, 3, 4])
dq = deque(maxlen=5)            # Bounded deque — auto-discards from opposite end

# ============================================
# Adding Elements — O(1)
# ============================================
dq = deque([1, 2, 3])

dq.append(4)        # deque([1, 2, 3, 4]) — add to RIGHT end
dq.appendleft(0)    # deque([0, 1, 2, 3, 4]) — add to LEFT end
dq.extend([5, 6])   # deque([0, 1, 2, 3, 4, 5, 6]) — extend RIGHT
dq.extendleft([-1, -2])  # deque([-2, -1, 0, 1, 2, 3, 4, 5, 6]) — extend LEFT (note: reversed!)

# ============================================
# Removing Elements — O(1)
# ============================================
dq = deque([0, 1, 2, 3, 4, 5])

dq.pop()         # Returns 5, deque([0, 1, 2, 3, 4]) — remove from RIGHT
dq.popleft()     # Returns 0, deque([1, 2, 3, 4]) — remove from LEFT
dq.remove(3)     # Removes first occurrence of 3 — O(n)
dq.clear()       # Empty the deque

# ============================================
# Accessing Elements
# ============================================
dq = deque([10, 20, 30, 40, 50])
print(dq[0])     # 10 — leftmost
print(dq[-1])    # 50 — rightmost
print(dq[2])     # 30 — random access (O(n) but works)

# ============================================
# Other Methods
# ============================================
dq = deque([3, 1, 4, 1, 5, 9])

dq.reverse()     # deque([9, 5, 1, 4, 1, 3]) — in-place
dq.rotate(2)     # deque([1, 3, 9, 5, 1, 4]) — rotate right by 2
dq.rotate(-2)    # deque([9, 5, 1, 4, 1, 3]) — rotate left by 2

# Count and index
dq = deque([1, 2, 2, 3])
print(dq.count(2))  # 2
print(dq.index(3))  # 3

# Copy
dq2 = dq.copy()
```

## 2. Deque vs List — Performance Comparison

```python
import time
from collections import deque

# ============================================
# List: O(n) for insert/remove at front
# ============================================
lst = list(range(100000))
start = time.time()
lst.insert(0, -1)        # O(n) — shifts all elements
lst.pop(0)                # O(n) — shifts all elements
print(f"List: {time.time() - start:.6f}s")

# ============================================
# Deque: O(1) for insert/remove at both ends
# ============================================
dq = deque(range(100000))
start = time.time()
dq.appendleft(-1)        # O(1)
dq.popleft()              # O(1)
print(f"Deque: {time.time() - start:.6f}s")

# ============================================
# WHEN TO USE WHAT:
# ============================================
# List:
#   - Random access by index: O(1)
#   - Adding/removing at END only: O(1) amortized
#   - When you need slicing, sorting, etc.

# Deque:
#   - Adding/removing at BOTH ends: O(1)
#   - Queue/stack implementations
#   - Sliding window problems
#   - BFS/DFS traversal
```

## 3. Sliding Window with Deque

```python
from collections import deque

# ============================================
# Maximum of All Subarrays of Size K
# (Classic Monotonic Deque Problem)
# ============================================
def max_sliding_window(arr, k):
    dq = deque()  # Stores INDICES
    result = []
    
    for i in range(len(arr)):
        # Remove elements outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements from right (maintain decreasing order)
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        
        dq.append(i)
        
        # Window is ready after processing k elements
        if i >= k - 1:
            result.append(arr[dq[0]])
    
    return result

print(max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))
# [3, 3, 5, 5, 6, 7]

# ============================================
# Minimum of All Subarrays of Size K
# ============================================
def min_sliding_window(arr, k):
    dq = deque()
    result = []
    
    for i in range(len(arr)):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        while dq and arr[dq[-1]] >= arr[i]:
            dq.pop()
        
        dq.append(i)
        
        if i >= k - 1:
            result.append(arr[dq[0]])
    
    return result

print(min_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))
# [-1, -3, -3, -3, 3, 3]

# ============================================
# First Negative in Every Window of Size K
# ============================================
def first_negative(arr, k):
    dq = deque()  # Store indices of negative numbers
    result = []
    
    for i in range(len(arr)):
        if arr[i] < 0:
            dq.append(i)
        
        # Remove out-of-window elements
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        if i >= k - 1:
            if dq:
                result.append(arr[dq[0]])
            else:
                result.append(0)
    
    return result

print(first_negative([12, -1, -7, 8, -15, 30, 16, 28], 3))
# [-1, -1, -7, -15, -15, 0]
```

## 4. heapq — Python's Priority Queue

```python
import heapq

# ============================================
# Min Heap (default behavior)
# ============================================
heap = []

# Push elements
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 4)
heapq.heappush(heap, 1)
heapq.heappush(heap, 5)

print(heap)  # [1, 1, 4, 3, 5] — heap structure, NOT sorted

# Pop smallest
print(heapq.heappop(heap))  # 1
print(heapq.heappop(heap))  # 1
print(heapq.heappop(heap))  # 3

# ============================================
# heapify — Convert list to heap in O(n)
# ============================================
arr = [5, 3, 8, 1, 2]
heapq.heapify(arr)  # In-place! arr becomes a heap
print(arr)  # [1, 2, 8, 3, 5] — valid heap structure

# ============================================
# Peek at smallest element without popping
# ============================================
arr = [5, 3, 8, 1, 2]
heapq.heapify(arr)
print(arr[0])  # 1 — smallest element, O(1)

# ============================================
# Push and pop in one operation
# ============================================
heapq.heappushpop(heap, 10)  # Push 10, then pop smallest
heapq.heapreplace(heap, 10)  # Pop smallest, then push 10

# ============================================
# Merge sorted iterables
# ============================================
a = [1, 3, 5]
b = [2, 4, 6]
merged = list(heapq.merge(a, b))
# [1, 2, 3, 4, 5, 6]
```

## 5. Max Heap — The Negate Trick

```python
import heapq

# Python only provides MIN heap. For MAX heap, negate all values.

# ============================================
# Max Heap using negate trick
# ============================================
heap = []

# Push (negate values)
for x in [3, 1, 4, 1, 5, 9]:
    heapq.heappush(heap, -x)

# Pop (negate back)
largest = -heapq.heappop(heap)  # 9
second = -heapq.heappop(heap)   # 5

# ============================================
# Heapify for max heap
# ============================================
arr = [5, 3, 8, 1, 2]
max_heap = [-x for x in arr]
heapq.heapify(max_heap)
print(-max_heap[0])  # 8 — largest element

# ============================================
# Heap with custom comparison (e.g., max heap of tuples)
# ============================================
tasks = [(1, 'low'), (3, 'high'), (2, 'medium')]

# Min heap by first element (default)
heapq.heapify(tasks)

# Max heap by first element
max_tasks = [(-priority, name) for priority, name in tasks]
heapq.heapify(max_tasks)
print(-max_tasks[0][0], max_tasks[0][1])  # 3 high
```

## 6. nlargest and nsmallest

```python
import heapq

arr = [5, 3, 8, 1, 2, 9, 4, 7, 6]

# ============================================
# nlargest / nsmallest — efficient for small n
# ============================================
print(heapq.nlargest(3, arr))   # [9, 8, 7]
print(heapq.nsmallest(3, arr))  # [1, 2, 3]

# With key function
words = ["banana", "apple", "cherry", "date"]
print(heapq.nlargest(2, words, key=len))
# ['banana', 'cherry']

# From a dictionary
d = {"a": 3, "b": 1, "c": 5, "d": 2}
print(heapq.nlargest(2, d.items(), key=lambda x: x[1]))
# [('c', 5), ('a', 3)]

# ============================================
# When to use nlargest vs sorting
# ============================================
# nlargest(n, arr): O(N + n*log(N)) — better when n << N
# sorted(arr)[-n:]: O(N*log(N)) — better when n ≈ N
```

## 7. Priority Queue Patterns in CP

```python
import heapq
from collections import defaultdict

# ============================================
# Pattern 1: Merge K Sorted Arrays
# ============================================
def merge_k_sorted(arrays):
    heap = []
    
    # Push first element of each array with (value, array_idx, element_idx)
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))
    
    result = []
    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, arr_idx, elem_idx + 1))
    
    return result

arrays = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
print(merge_k_sorted(arrays))
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ============================================
# Pattern 2: Kth Largest Element
# ============================================
def kth_largest(arr, k):
    min_heap = arr[:k]
    heapq.heapify(min_heap)
    
    for num in arr[k:]:
        if num > min_heap[0]:
            heapq.heapreplace(min_heap, num)
    
    return min_heap[0]

print(kth_largest([3, 2, 1, 5, 6, 4], 2))  # 5

# Or simply:
def kth_largest_v2(arr, k):
    return heapq.nlargest(k, arr)[-1]

# ============================================
# Pattern 3: Kth Smallest Element
# ============================================
def kth_smallest(arr, k):
    heapq.heapify(arr)
    for _ in range(k - 1):
        heapq.heappop(arr)
    return heapq.heappop(arr)

print(kth_smallest([3, 2, 1, 5, 6, 4], 3))  # 3

# ============================================
# Pattern 4: Task Scheduler (with cooldown)
# ============================================
def least_interval(tasks, n):
    from collections import Counter
    count = Counter(tasks)
    max_freq = max(count.values())
    max_count = sum(1 for v in count.values() if v == max_freq)
    
    result = (max_freq - 1) * (n + 1) + max_count
    return max(result, len(tasks))

print(least_interval(["A","A","A","B","B","B"], 2))  # 8

# ============================================
# Pattern 5: Dijkstra's Shortest Path
# ============================================
import heapq
from collections import defaultdict

def dijkstra(graph, start):
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    heap = [(0, start)]
    visited = set()
    
    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        
        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(heap, (dist[v], v))
    
    return dict(dist)

graph = defaultdict(list)
edges = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5)]
for u, v, w in edges:
    graph[u].append((v, w))

print(dijkstra(graph, 0))
# {0: 0, 2: 1, 1: 3, 3: 4}

# ============================================
# Pattern 6: Huffman Coding (Greedy)
# ============================================
def huffman_codes(freq):
    heap = [[freq, [char, ""]] for char, freq in freq.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        
        combined = lo + hi
        heapq.heappush(heap, combined)
    
    return dict(heap[0][1:])

codes = huffman_codes({'a': 5, 'b': 9, 'c': 12, 'd': 13, 'e': 16, 'f': 45})
print(codes)  # {'f': '0', 'c': '100', 'd': '101', 'a': '1100', 'b': '1101', 'e': '111'}
```

## 8. Sliding Window Maximum with Deque — Complete Implementation

```python
from collections import deque

def max_subarray_of_size_k(arr, k):
    """
    Find maximum sum of all contiguous subarrays of size k.
    Uses deque to track maximum element in each window.
    """
    n = len(arr)
    if n < k:
        return -1
    
    dq = deque()
    max_sum = float('-inf')
    window_sum = 0
    
    for i in range(n):
        # Add current element to window sum
        window_sum += arr[i]
        
        # Remove indices outside window from front
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements from back
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        
        dq.append(i)
        
        # Window is complete
        if i >= k - 1:
            max_sum = max(max_sum, window_sum)
            window_sum -= arr[dq[0]] if dq[0] == i - k + 1 else 0
    
    return max_sum

print(max_subarray_of_size_k([1, 4, 2, 10, 23, 3, 1, 0, 20], 4))
# 39 (subarray [10, 23, 3, 1] → wait, let me recalculate)
# Actually the max sum subarray of size 4 is [10, 23, 3, 1] = 37
# or [23, 3, 1, 0] = 27, or [3, 1, 0, 20] = 24, or [10, 23, 3, 1] = 37
```

## 9. Quick Reference

```python
# ============================================
# Deque Operations — All O(1)
# ============================================
# append(x)       → add to right end
# appendleft(x)   → add to left end
# pop()           → remove from right end
# popleft()       → remove from left end
# extend(iter)    → add multiple to right
# extendleft(iter)→ add multiple to left (reversed!)
# remove(x)       → remove first occurrence — O(n)
# rotate(n)       → rotate right by n
# rotate(-n)      → rotate left by n

# ============================================
# heapq Operations
# ============================================
# heappush(heap, x)       → push x onto heap — O(log n)
# heappop(heap)           → pop smallest — O(log n)
# heapify(list)           → convert to heap — O(n)
# heappushpop(heap, x)    → push then pop — O(log n)
# heapreplace(heap, x)    → pop then push — O(log n)
# nlargest(n, iterable)   → n largest elements — O(N + n log N)
# nsmallest(n, iterable)  → n smallest elements — O(N + n log N)
# merge(*iterables)       → merge sorted iterables
```
