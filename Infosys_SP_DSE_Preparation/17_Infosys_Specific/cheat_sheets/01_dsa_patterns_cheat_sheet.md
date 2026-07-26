# DSA Patterns Cheat Sheet - Quick Reference

> Python code templates for all major DSA patterns. Copy-paste ready.

## Pattern Recognition Speed Chart

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PATTERN RECOGNITION CHEAT SHEET                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  INPUT特征 (Input Features)     ──►  PATTERN (模式)                 │
│  ─────────────────────────────────────────────────────────────────  │
│  Sorted array + pair sum       ──►  Two Pointer                    │
│  Subarray/substring + window   ──►  Sliding Window                 │
│  Sorted + search target        ──►  Binary Search                  │
│  Graph/Tree + shortest path    ──►  BFS (unweighted)               │
│  Graph/Tree + explore all      ──►  DFS                            │
│  Weighted graph + shortest     ──►  Dijkstra                       │
│  Dynamic connectivity          ──►  Union-Find                     │
│  Task ordering/deps            ──►  Topological Sort               │
│  Generate all combinations     ──►  Backtracking                   │
│  Optimal substructure          ──►  Dynamic Programming            │
│  Prefix/suffix + range query   ──►  Segment Tree                   │
│  Prefix matching/autocomplete  ──►  Trie                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Complexity Quick Reference

```
┌────────────────┬──────────┬──────────────────────────────────┐
│ Pattern        │ Time     │ Space                            │
├────────────────┼──────────┼──────────────────────────────────┤
│ Two Pointer    │ O(n)     │ O(1)                             │
│ Sliding Window │ O(n)     │ O(k) where k = window size       │
│ Binary Search  │ O(log n) │ O(1)                             │
│ BFS / DFS      │ O(V+E)   │ O(V)                             │
│ Dijkstra       │ O(ElogV) │ O(V)                             │
│ Union-Find     │ O(α(n))  │ O(n)                             │
│ Topo Sort      │ O(V+E)   │ O(V)                             │
│ Backtracking   │ O(2^n)   │ O(n)                             │
│ DP (1D)        │ O(n)     │ O(n) or O(1) optimized           │
│ DP (2D)        │ O(m*n)   │ O(m*n) or O(n) optimized         │
│ Segment Tree   │ O(log n) │ O(n)                             │
│ Trie           │ O(m)     │ O(ALPHABET * n * m)               │
└────────────────┴──────────┴──────────────────────────────────┘
  α(n) = inverse Ackermann function (nearly constant)
  m = string length / alphabet size as applicable
```

---

## 1. Two Pointer Template

```python
def two_pointer(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        if condition_met(arr, left, right):
            # Process
            left += 1
            right -= 1
        elif need_increase(arr, left, right):
            left += 1
        else:
            right -= 1
```

**When to use:**
- Sorted array problems
- Pair/triplet problems
- Palindrome checking
- Container problems

### Visual Walkthrough: Two Pointer on Sorted Array

```
Array:  [1, 2, 4, 6, 8, 10]    Target = 12
         ^                    ^
         L                    R    sum = 1+10 = 11 < 12 → move L →

Array:  [1, 2, 4, 6, 8, 10]
              ^              ^
              L              R    sum = 2+10 = 12 = 12 ✓ FOUND!

Two Pointer Movement Pattern:
┌──────────────────────────────────────────────────┐
│  Sum too small  →  Move L right (increase sum)   │
│  Sum too large →  Move R left  (decrease sum)    │
│  Sum matches   →  Return result                  │
│  L meets R     →  No solution                    │
└──────────────────────────────────────────────────┘
```

**Example: Two Sum Sorted**
```python
def two_sum_sorted(arr, target):
    # Step 1: Initialize pointers at both ends
    left, right = 0, len(arr) - 1
    
    # Step 2: Move pointers inward based on comparison
    while left < right:
        curr_sum = arr[left] + arr[right]
        if curr_sum == target:       # Found the pair
            return [left, right]
        elif curr_sum < target:      # Need larger sum → move left pointer right
            left += 1
        else:                        # Need smaller sum → move right pointer left
            right -= 1
    return []  # No pair found
```

### Common Mistakes
```
❌ Forgetting to handle duplicates: [1,1,3,4,5] target=6
   → Should return only one pair (1,5), not duplicate (1,5)

❌ Not checking left < right condition
   → Can process same element twice

✅ Always add: while left < right (not while left <= right)
```

---

## 2. Sliding Window Template

```python
def sliding_window(s, k):
    window = {}
    result = 0
    left = 0

    for right in range(len(s)):
        # Add right element to window
        window[s[right]] = window.get(s[right], 0) + 1

        # Shrink window if needed
        while window_needs_shrink:
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1

        # Update result
        result = max(result, right - left + 1)

    return result
```

**When to use:**
- Subarray/substring problems
- Fixed size window problems
- Minimum/maximum window problems
- Characters/anagram problems

### Visual Walkthrough: Sliding Window

```
Array:  [2, 1, 5, 1, 3, 2]    Window Size K = 3

Step 1: Initial Window
┌───┬───┬───┬───┬───┬───┐
│ 2 │ 1 │ 5 │ 1 │ 3 │ 2 │
└───┴───┴───┴───┴───┴───┘
  [===]  Sum = 2+1+5 = 8

Step 2: Slide window right by removing left, adding right
┌───┬───┬───┬───┬───┬───┐
│ 2 │ 1 │ 5 │ 1 │ 3 │ 2 │
└───┴───┴───┴───┴───┴───┘
      [===]  Sum = 8 - 2 + 1 = 7

Step 3: Slide again
┌───┬───┬───┬───┬───┬───┐
│ 2 │ 1 │ 5 │ 1 │ 3 │ 2 │
└───┴───┴───┴───┴───┴───┘
          [===]  Sum = 7 - 1 + 5 = 11  ← MAX!

Step 4: Continue sliding...
┌───┬───┬───┬───┬───┬───┐
│ 2 │ 1 │ 5 │ 1 │ 3 │ 2 │
└───┴───┴───┴───┴───┴───┘
              [===]  Sum = 11 - 5 + 1 = 7

Sliding Window Formula:
┌───────────────────────────────────────────────────────┐
│  new_sum = old_sum - arr[left] + arr[right + 1]       │
│                                                       │
│  Think of it as:                                      │
│  "Remove the leftmost, add the next rightmost"        │
└───────────────────────────────────────────────────────┘
```

**Example: Max Sum Subarray of Size K**
```python
def max_sum_k(arr, k):
    # Step 1: Calculate initial window sum
    window_sum = sum(arr[:k])    # First window
    max_sum = window_sum
    
    # Step 2: Slide the window - remove left, add right
    for i in range(k, len(arr)):
        # Slide: remove element going out, add new element coming in
        window_sum += arr[i] - arr[i - k]  # O(1) update!
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

### Fixed vs Variable Window

```
FIXED SIZE WINDOW (K fixed):
  Use when: "Find max sum of K elements"
  Pattern:  sum += arr[right] - arr[left]
  
VARIABLE SIZE WINDOW (expand/shrink):
  Use when: "Find longest substring with at most K distinct"
  Pattern:  expand right until condition broken, then shrink left
  
┌─────────────────────────────────────────────────┐
│  Fixed:     right always moves, left follows    │
│  Variable:  right expands, left shrinks         │
└─────────────────────────────────────────────────┘
```

---

## 3. Binary Search Template

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1  # Not found

# Binary search on answer
def binary_search_answer(arr):
    left, right = min_possible, max_possible

    while left < right:
        mid = left + (right - left) // 2

        if can_solve(mid):
            right = mid  # Try smaller
        else:
            left = mid + 1  # Try larger

    return left
```

**When to use:**
- Sorted array searching
- Finding minimum/maximum value
- Optimization problems
- "Find first/last occurrence"

### Visual Walkthrough: Binary Search

```
Array:  [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]    Target = 23

Step 1: left=0, right=9, mid=4
[2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
 L              M                    R
 arr[mid]=16 < 23 → search RIGHT half

Step 2: left=5, right=9, mid=7
[2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
                  L        M        R
 arr[mid]=56 > 23 → search LEFT half

Step 3: left=5, right=6, mid=5
[2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
                  L  M     R
 arr[mid]=23 = 23 → FOUND at index 5!

Binary Search Decision Tree:
┌────────────────────────────────────────────────┐
│  arr[mid] == target  →  Return mid             │
│  arr[mid] < target   →  Search right: L = mid+1│
│  arr[mid] > target   →  Search left:  R = mid-1│
└────────────────────────────────────────────────┘

CRITICAL BUG PREVENTION:
  mid = left + (right - left) // 2   ← SAFE ✅
  mid = (left + right) // 2          ← Can overflow ❌
```

**Example: Find First and Last Position**
```python
def find_first_last(arr, target):
    def find_first():
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] < target:
                left = mid + 1
            elif arr[mid] > target:
                right = mid - 1
            else:
                if mid == 0 or arr[mid - 1] != target:
                    return mid
                right = mid - 1
        return -1

    def find_last():
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] < target:
                left = mid + 1
            elif arr[mid] > target:
                right = mid - 1
            else:
                if mid == len(arr) - 1 or arr[mid + 1] != target:
                    return mid
                left = mid + 1
        return -1

    return [find_first(), find_last()]
```

---

## 4. BFS Template

```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    level = 0

    while queue:
        level_size = len(queue)

        for _ in range(level_size):
            node = queue.popleft()

            # Process node
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        level += 1

    return level
```

**When to use:**
- Shortest path in unweighted graph
- Level-order traversal
- Connected components
- Bipartite checking

### Visual Walkthrough: BFS Level-by-Level

```
Graph:
        A
       / \
      B   C
     / \   \
    D   E   F

BFS Exploration Order (Level by Level):
┌─────────────────────────────────────────────┐
│  Level 0:  [A]         → queue: [A]        │
│  Level 1:  [B, C]      → queue: [B, C]    │
│  Level 2:  [D, E, F]   → queue: [D, E, F] │
└─────────────────────────────────────────────┘

Queue Visualization:
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  A  │  B  │  C  │  D  │  E  │  F  │
└─────┴─────┴─────┴─────┴─────┴─────┘
  ↑ dequeue from front, enqueue to back
  
BFS = "Explore neighbor first, then neighbor's neighbor"
     = "Layer by layer, like ripples in water"
```

**Example: Level Order Traversal**
```python
from collections import deque

def level_order(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result
```

---

## 5. DFS Template

```python
# Recursive DFS
def dfs_recursive(graph, node, visited):
    if node in visited:
        return
    visited.add(node)

    # Process node
    for neighbor in graph[node]:
        dfs_recursive(graph, neighbor, visited)

# Iterative DFS
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
```

**When to use:**
- Path finding
- Cycle detection
- Topological sort
- Connected components
- Tree traversals

### Visual Walkthrough: DFS (Depth First)

```
Graph:
        A
       / \
      B   C
     / \   \
    D   E   F

DFS Exploration Order (Go deep first):
┌─────────────────────────────────────────────────────┐
│  Step 1: Visit A → stack: [A]                       │
│  Step 2: Visit B → stack: [A, B]                    │
│  Step 3: Visit D → stack: [A, B, D]                 │
│  Step 4: Dead end → backtrack → stack: [A, B, E]    │
│  Step 5: Visit E → stack: [A, C]                    │
│  Step 6: Visit C → stack: [A, C, F]                 │
│  Step 7: Visit F → done!                            │
└─────────────────────────────────────────────────────┘

DFS = "Go as deep as possible, then backtrack"
     = "Like exploring a maze, marking visited paths"

Recursive vs Iterative DFS:
┌────────────────────────────────────────────────┐
│  Recursive:  Uses call stack (simpler code)   │
│  Iterative:  Uses explicit stack (no overflow)│
│                                                │
│  For large graphs (10^5+ nodes), use iterative│
└────────────────────────────────────────────────┘
```

**Example: Detect Cycle in Directed Graph**
```python
def has_cycle(graph, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n

    def dfs(node):
        color[node] = GRAY
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        color[node] = BLACK
        return False

    for i in range(n):
        if color[i] == WHITE and dfs(i):
            return True
    return False
```

---

## 6. Dijkstra Template

```python
import heapq

def dijkstra(graph, start, n):
    dist = [float('inf')] * n
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:
            continue

        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    return dist

# Usage
graph = defaultdict(list)
graph[0].append((1, 4))
graph[0].append((2, 1))
graph[1].append((3, 1))
graph[2].append((1, 2))
graph[2].append((3, 5))

distances = dijkstra(graph, 0, 4)
```

**When to use:**
- Shortest path in weighted graph
- Non-negative edge weights only
- Single source shortest path

---

## 7. Union-Find Template

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False

        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)

# Usage
uf = UnionFind(5)
uf.union(0, 1)
uf.union(2, 3)
print(uf.connected(0, 1))  # True
print(uf.connected(0, 2))  # False
```

**When to use:**
- Dynamic connectivity
- Cycle detection in undirected graph
- Kruskal's MST
- Connected components

### Visual Walkthrough: Union-Find

```
Initial State (each node is its own parent):
  0   1   2   3   4
  │   │   │   │   │
 [0] [1] [2] [3] [4]

After union(0,1):
  0   1   2   3   4
  │  /
 [0]
 └──── 0 and 1 are now in same set

After union(2,3):
  0   1   2   3   4
  │  / │  /
 [0]  [2]
 └────   └──── 0-1 connected, 2-3 connected

After union(0,2):
  0   1   2   3   4
  │  / │  /
 [0]  [2]
  └────┘   └──── All 0,1,2,3 connected

Path Compression Visualization:
  Before:  3 → 2 → 1 → 0   (find(3) follows chain)
  After:   3 → 0             (path compressed directly)
           2 → 0
           1 → 0
```

---

## 8. Topological Sort Template

```python
from collections import deque, defaultdict

def topological_sort(n, edges):
    graph = defaultdict(list)
    in_degree = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)

    result = []
    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != n:
        return []  # Cycle exists
    return result
```

**When to use:**
- Task scheduling
- Course prerequisites
- Build systems
- Dependency resolution

---

## 9. Backtracking Template

```python
def backtrack(path, choices):
    if need_to_record_result(path):
        result.append(path[:])
        return

    for choice in choices:
        if is_valid(choice):
            path.append(choice)       # Choose
            backtrack(path, new_choices)  # Explore
            path.pop()                # Un-choose
```

**When to use:**
- Permutations/Combinations
- Subset problems
- Constraint satisfaction
- Maze solving

### Visual Walkthrough: Backtracking Decision Tree

```
Generate Permutations of [1, 2, 3]:

                         []
                    /    |    \
                  [1]   [2]   [3]
                 / \    / \    / \
              [1,2][1,3][2,1][2,3][3,1][3,2]
                |    |    |    |    |    |
            [1,2,3][1,3,2][2,1,3][2,3,1][3,1,2][3,2,1]

The three steps:
┌─────────────────────────────────────────────────────────┐
│  1. CHOOSE:    path.append(choice)                      │
│  2. EXPLORE:   backtrack(path, new_choices)              │
│  3. UNCHOOSE:  path.pop()  ← CRITICAL for correctness   │
└─────────────────────────────────────────────────────────┘

Without step 3 (pop), the path would keep growing incorrectly!
```

**Example: Generate Permutations**
```python
def permute(nums):
    result = []

    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return

        for i in range(len(remaining)):
            path.append(remaining[i])
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()

    backtrack([], nums)
    return result
```

---

## 10. DP Template (1D)

### Visual: DP State Transition

```
Climbing Stairs Example:
  Stairs: 1  2  3  4  5
  Ways:   1  2  3  5  8

dp[i] = dp[i-1] + dp[i-2]
        ↑ step 1   ↑ step 2

  dp[1] = 1 (only one way: step 1)
  dp[2] = 2 (two ways: 1+1 or 2)
  dp[3] = dp[2] + dp[1] = 2 + 1 = 3
  dp[4] = dp[3] + dp[2] = 3 + 2 = 5
  
Space Optimization: Only need last 2 values!
  Instead of dp[] array, just track: prev1, prev2
```

```python
def dp_1d(arr):
    n = len(arr)
    dp = [0] * (n + 1)

    # Base case
    dp[0] = base_value

    # Fill dp array
    for i in range(1, n + 1):
        dp[i] = min/max(dp[i-1] + cost, dp[i-2] + cost)

    return dp[n]

# Space optimized
def dp_1d_optimized(arr):
    n = len(arr)
    prev2 = base1
    prev1 = base2

    for i in range(2, n + 1):
        curr = min/max(prev1 + cost, prev2 + cost)
        prev2 = prev1
        prev1 = curr

    return prev1
```

**Example: Climbing Stairs**
```python
def climb_stairs(n):
    if n <= 2:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2

    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]

    return dp[n]
```

---

## 11. DP Template (2D)

### Visual: 2D DP Table for LCS

```
LCS("ABC", "AC"):
        ""  A  C
    ""   0  0  0
     A   0  1  1
     B   0  1  1
     C   0  1  2  ← LCS length = 2

Fill order: Row by row, left to right
Each cell depends on: top, left, top-left diagonals
```

```python
def dp_2d(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = 0
    for j in range(n + 1):
        dp[0][j] = 0

    # Fill dp array
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]
```

**Example: LCS**
```python
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]
```

---

## 12. Segment Tree Template

### Visual: Segment Tree for Range Sum Queries

```
Array: [1, 3, 5, 7, 9, 11]

Segment Tree Structure:
                        [36]                       ← root = total sum
                    /          \
                [9]              [27]
              /     \          /      \
           [4]      [5]     [16]     [11]
          /   \    /   \   /    \   /    \
        [1]  [3] [5]  [7] [9]  [11]
        
Query: sum(1,3) → 3+5+7 = 15
  Traverse tree: skip [1], take [3]+[5]+[7] = 15
  
Update: index 2 = 5 → 10
  Only update path from leaf to root: [5]→[10], then recalculate parents
```

```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.build(data, 0, 0, self.n - 1)

    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self.build(data, 2 * node + 1, start, mid)
            self.build(data, 2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node + 1, start, mid, idx, val)
            else:
                self.update(2 * node + 2, mid + 1, end, idx, val)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        left_sum = self.query(2 * node + 1, start, mid, l, r)
        right_sum = self.query(2 * node + 2, mid + 1, end, l, r)
        return left_sum + right_sum

# Usage
data = [1, 3, 5, 7, 9, 11]
st = SegmentTree(data)
print(st.query(0, 0, len(data) - 1, 1, 3))  # Sum of [3, 5, 7] = 15
st.update(0, 0, len(data) - 1, 1, 10)  # Update index 1 to 10
```

**When to use:**
- Range queries (sum, min, max)
- Range updates
- Online queries

---

## 13. Trie Template

### Visual: Trie Structure

```
Insert words: "apple", "app", "bat", "ball"

          root
       /    |    \
      a     b     
      |     |  \
      p     a   a
      |     |    \
      p     t     l
      |           |
      l           l
      |           |
      e*          e*
      
  * = is_end of word marker
  
Lookup "app": root→a→p→p (is_end=True) → FOUND ✅
Lookup "ap":  root→a→p (is_end=False) → NOT a word ❌
Lookup "bat": root→b→a→t (is_end=True) → FOUND ✅

Trie vs HashMap for prefix operations:
┌──────────────────────────────────────────────────┐
│  Task          │ HashMap  │ Trie     │           │
│  Insert word   │ O(k)     │ O(k)     │           │
│  Search word   │ O(k)     │ O(k)     │ Same!     │
│  Search prefix │ O(n*k)   │ O(k)     │ Trie wins │
│  Autocomplete  │ O(n*k)   │ O(k+out) │ Trie wins │
└──────────────────────────────────────────────────┘
  k = word length, n = number of words
```

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

# Usage
trie = Trie()
trie.insert("apple")
trie.insert("app")
print(trie.search("apple"))     # True
print(trie.search("app"))       # True
print(trie.search("appl"))      # False
print(trie.starts_with("app"))  # True
```

**When to use:**
- Prefix matching
- Autocomplete
- Word games
- String dictionary operations

---

## Pattern Decision Tree

```
Start Here
    |
    ├── Sorted Array? → Two Pointer
    |
    ├── Subarray/Substring? → Sliding Window
    |
    ├── Search in Sorted? → Binary Search
    |
    ├── Graph/Tree?
    |   ├── Shortest Path? → BFS (unweighted) / Dijkstra (weighted)
    |   ├── Traversal? → DFS
    |   ├── Connected Components? → Union-Find or DFS
    |   ├── Dependencies? → Topological Sort
    |   └── MST? → Kruskal (Union-Find) or Prim
    |
    ├── Subsequence/Subset? → Backtracking or DP
    |
    ├── Optimization? → DP or Binary Search on Answer
    |
    ├── String Matching? → Trie or Aho-Corasick
    |
    └── Range Queries? → Segment Tree or Fenwick Tree
```

> **Tip:** Recognize the pattern quickly, apply the template, and customize for the specific problem. Practice until templates become muscle memory.
