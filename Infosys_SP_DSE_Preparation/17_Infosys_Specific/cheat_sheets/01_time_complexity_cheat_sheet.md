# Time Complexity Cheat Sheet

> Quick reference for all algorithm complexities and decision guide.

---

## Common Algorithms

### Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | O(n) | O(n^2) | O(n^2) | O(1) | Yes |
| Selection Sort | O(n^2) | O(n^2) | O(n^2) | O(1) | No |
| Insertion Sort | O(n) | O(n^2) | O(n^2) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n^2) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Tim Sort | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| Counting Sort | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes |
| Radix Sort | O(nk) | O(nk) | O(nk) | O(n + k) | Yes |
| Bucket Sort | O(n + k) | O(n + k) | O(n^2) | O(n + k) | Yes |

### Searching Algorithms

| Algorithm | Time | Space | When to Use |
|-----------|------|-------|-------------|
| Linear Search | O(n) | O(1) | Unsorted array |
| Binary Search | O(log n) | O(1) | Sorted array |
| Ternary Search | O(log n) | O(1) | Unimodal function |
| Interpolation Search | O(log log n) avg | O(1) | Uniform distribution |

### Graph Algorithms

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| BFS | O(V + E) | O(V) | Shortest path (unweighted) |
| DFS | O(V + E) | O(V) | Path finding, cycles |
| Dijkstra | O((V + E) log V) | O(V) | Shortest path (weighted) |
| Bellman-Ford | O(VE) | O(V) | Negative weights |
| Floyd-Warshall | O(V^3) | O(V^2) | All pairs shortest path |
| Kruskal | O(E log E) | O(V) | MST |
| Prim | O(E log V) | O(V) | MST |
| Topological Sort | O(V + E) | O(V) | DAG ordering |
| Tarjan's | O(V + E) | O(V) | SCC |
| Kosaraju's | O(V + E) | O(V) | SCC |

### Tree Algorithms

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| Inorder/Preorder/Postorder | O(n) | O(h) | Traversal |
| Level Order | O(n) | O(w) | Level-wise traversal |
| BST Operations | O(log n) avg | O(h) | Search, Insert, Delete |
| LCA (Binary Lifting) | O(n log n) | O(n log n) | Lowest Common Ancestor |
| Diameter | O(n) | O(h) | Longest path |

### Dynamic Programming

| Problem | Time | Space | Pattern |
|---------|------|-------|---------|
| Fibonacci | O(n) | O(1) | 1D DP |
| 0/1 Knapsack | O(nW) | O(nW) | 2D DP |
| Subset Sum | O(nW) | O(nW) | 2D DP |
| LCS | O(mn) | O(mn) | 2D DP |
| LIS | O(n log n) | O(n) | DP + Binary Search |
| Edit Distance | O(mn) | O(mn) | 2D DP |
| Matrix Chain | O(n^3) | O(n^2) | Interval DP |
| Coin Change | O(n * amount) | O(amount) | 1D DP |
| Palindrome | O(n^2) | O(n^2) | Interval DP |
| Burst Balloons | O(n^3) | O(n^2) | Interval DP |

---

## Space Complexity of Data Structures

| Structure | Access | Search | Insert | Delete | Space |
|-----------|--------|--------|--------|--------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1) | O(1) | O(n) |
| Stack | O(n) | O(n) | O(1) | O(1) | O(n) |
| Queue | O(n) | O(n) | O(1) | O(1) | O(n) |
| Hash Table | N/A | O(1) avg | O(1) avg | O(1) avg | O(n) |
| BST | O(log n) avg | O(log n) avg | O(log n) avg | O(log n) avg | O(n) |
| Heap | O(1) | O(n) | O(log n) | O(log n) | O(n) |
| Trie | O(m) | O(m) | O(m) | O(m) | O(n*m) |

---

## Python Specific Complexities

### List Operations
```python
# O(1) operations
lst.append(x)      # Add to end
lst.pop()          # Remove from end
lst[-1]            # Access last element
len(lst)           # Get length

# O(n) operations
lst.insert(0, x)   # Add to beginning
lst.pop(0)         # Remove from beginning
x in lst           # Search
lst.remove(x)      # Remove first occurrence
lst.index(x)       # Find index
lst.count(x)       # Count occurrences
```

### Dict Operations
```python
# O(1) average operations
d[key]             # Access
d[key] = value     # Insert/Update
key in d           # Search
d.get(key)         # Safe access
d.pop(key)         # Remove
d.keys()           # Get keys
d.values()         # Get values
d.items()          # Get items

# O(n) operations
dict(d)            # Copy
d.update(other)    # Merge
```

### Set Operations
```python
# O(1) average operations
s.add(x)           # Insert
s.remove(x)        # Remove
x in s             # Search
s.discard(x)       # Safe remove
s.pop()            # Remove arbitrary

# O(n) operations
s1 | s2            # Union
s1 & s2            # Intersection
s1 - s2            # Difference
s1 ^ s2            # Symmetric difference
```

### String Operations
```python
# O(n) operations
s + t               # Concatenation
s * n               # Repeat
s.find(t)           # Search
s.replace(a, b)     # Replace
s.split()           # Split
s.strip()           # Trim
s.upper()           # Convert case
s.startswith(t)     # Check prefix
s.endswith(t)       # Check suffix
```

---

## Decision Tree: What Algorithm to Use

### Based on Constraints

```
N ≤ 10:           Brute Force, Backtracking, Permutations
N ≤ 20:           Bitmask DP, Backtracking with Pruning
N ≤ 500:          O(N^3) algorithms (Floyd-Warshall, Matrix Chain)
N ≤ 5000:         O(N^2) algorithms (DP, Two Pointer variants)
N ≤ 10^6:         O(N log N) algorithms (Sorting, Binary Search, DP)
N ≤ 10^8:         O(N) algorithms (Linear scan, Hash Map)
N ≤ 10^18:        O(log N) algorithms (Binary Search, Matrix Exponentiation)
```

### Based on Problem Type

```
Find minimum/maximum:
├── Sorted array → Binary Search
├── Unsorted array → Linear Scan
├── With constraints → DP
└── In graph → Dijkstra/BFS

Find pair/triplet:
├── Sum equals target → Two Pointer or Hash Map
├── Product equals target → Hash Map
├── Minimum difference → Sorting + Two Pointer
└── Count pairs → Hash Map

Find subarray:
├── Fixed size → Sliding Window
├── Variable size → Sliding Window + Two Pointer
├── Maximum sum → Kadane's
├── Sum equals K → Prefix Sum + Hash Map
└── All subarrays → O(N^2) brute force

Find subsequence:
├── LIS → DP + Binary Search
├── LCS → 2D DP
├── Palindrome → DP or Expand Around Center
└── Subset → Backtracking or DP

Graph problems:
├── Shortest path → BFS (unweighted) / Dijkstra (weighted)
├── Connectivity → Union-Find or DFS
├── Cycle detection → DFS (directed/undirected)
├── Topological order → BFS/DFS
└── MST → Kruskal or Prim
```

### When O(N^2) is Acceptable

```python
# N ≤ 5000: O(N^2) is fine
# Examples:
# - Two pointer on array
# - DP on 2D states
# - Nested loops with small N
# - Brute force with pruning

# Example: O(N^2) solution
def find_pairs(arr, target):
    result = []
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == target:
                result.append((arr[i], arr[j]))
    return result
```

### When You Need O(N log N) or Better

```python
# N > 5000: Need better than O(N^2)
# Examples:
# - Sorting + Binary Search
# - Divide and Conquer
# - Efficient DP
# - Segment Trees

# Example: O(N log N) solution
import bisect

def count_pairs(arr, target):
    arr.sort()
    count = 0
    for i in range(len(arr)):
        idx = bisect.bisect_right(arr, target - arr[i], i + 1)
        count += idx - (i + 1)
    return count
```

### When You Need O(N) or Better

```python
# N > 10^6: Need linear time
# Examples:
# - Hash Map operations
# - Two Pointer / Sliding Window
# - Kadane's Algorithm
# - BFS/DFS on graph

# Example: O(N) solution
def two_sum(arr, target):
    seen = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

---

## Complexity Cheat Sheet Table

| N | Max Operations | Algorithm Type |
|---|----------------|----------------|
| 10 | 100 | O(N^2) Brute Force |
| 20 | 1M | Bitmask DP |
| 50 | 12.5M | O(N^3) |
| 100 | 100M | O(N^3) with optimization |
| 500 | 250M | O(N^2 log N) |
| 1,000 | 1B | O(N^2) |
| 5,000 | 25M | O(N^2) |
| 10,000 | 100M | O(N^2) borderline |
| 100,000 | 10B | O(N log N) |
| 1,000,000 | 100B | O(N) |
| 10,000,000 | 1T | O(N) with optimization |
| 100,000,000 | 100T | O(log N) |

---

## Python Optimization Tips

### Use Built-in Functions
```python
# Instead of manual loop
total = 0
for x in arr:
    total += x

# Use built-in
total = sum(arr)

# Use list comprehension instead of loop
squares = [x**2 for x in range(10)]

# Use enumerate instead of manual index
for i, x in enumerate(arr):
    pass
```

### Use Efficient Data Structures
```python
# For frequency counting
from collections import Counter
freq = Counter(arr)  # O(n) instead of O(n^2)

# For default values
from collections import defaultdict
d = defaultdict(int)  # No KeyError

# For queue operations
from collections import deque
dq = deque()  # O(1) for append/popleft vs O(n) for list
```

### Avoid Unnecessary Operations
```python
# Bad: O(n^2)
result = []
for x in arr:
    if x not in result:  # O(n) search
        result.append(x)

# Good: O(n)
seen = set()
result = []
for x in arr:
    if x not in seen:  # O(1) search
        seen.add(x)
        result.append(x)
```

### Use Generators for Large Data
```python
# Memory efficient
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Process without storing
for x in fibonacci():
    if x > 1000:
        break
    print(x)
```

---

## Quick Decision Reference

```
Problem asks for:
├── "Find if possible" → BFS/DFS, DP boolean
├── "Find minimum/maximum" → DP, Greedy, Binary Search
├── "Count ways" → DP, Combinatorics
├── "Find all" → Backtracking, DFS
├── "Check if exists" → Hash Map, Binary Search
├── "Longest/Shortest" → DP, BFS, Sliding Window
├── "Sort" → Use efficient sort
└── "Search" → Binary Search (sorted), Hash Map (unsorted)
```

> **Key Rule:** Always check constraints first. They determine which algorithms are feasible. A brute force solution that passes is better than an optimal solution that's wrong.
