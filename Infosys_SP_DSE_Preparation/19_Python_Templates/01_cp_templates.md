# Python Competitive Programming Templates - Infosys SP DSE

Ready-to-use templates. Copy-paste during the exam.

> **Exam Tip:** Memorize the template numbers below. During the exam, identify the
> problem type, jump to the matching template, and adapt it to the problem.

---

## Quick Reference - Decision Flowchart

```
                    START HERE
                        |
               What does the problem ask?
                        |
        +---------------+----------------+------------------+
        |               |                |                  |
   PATH in graph?   RANGE query?    PATTERN in string?  NUMBER theory?
        |               |                |                  |
   +----+----+     +---+----+      +----+----+        +----+----+
   |         |     |        |      |         |        |         |
 Weighted?  No   Update?  Just   Exact?   Hash?    nCr/pow?  Matrix?
   |        |     |       sum?     |         |        |         |
 Dijkstra  BFS  SegTree Fenwick  KMP    RabinKarp   ModArith  MatExp
                Fenwick Tree
                        |
            +-----------+-----------+
            |           |           |
        Subarray?   Connect?   Order tasks?
            |           |           |
         Kadane    Union-Find   TopoSort
            |           |
        Sliding     Cycle in
         Window     undirected?
                        |
                    Union-Find
```

## Template Cheat Sheet

| #  | Template              | Time           | Space  | One-Liner When to Use                     |
|----|-----------------------|----------------|--------|-------------------------------------------|
| 1  | Fast I/O              | -              | -      | **Always** in CP                          |
| 2  | BFS                   | O(V + E)       | O(V)   | Shortest path unweighted grid/graph       |
| 3  | DFS                   | O(V + E)       | O(V)   | Components, cycles, reachability          |
| 4  | Dijkstra              | O((V+E) log V) | O(V)   | Shortest path weighted graph              |
| 5  | Union-Find            | O(alpha(n))    | O(n)   | Dynamic connectivity, merge sets          |
| 6  | Segment Tree          | O(n log n)     | O(n)   | Range query + point update                |
| 7  | Trie                  | O(L)           | O(N*L) | Prefix matching, autocomplete             |
| 8  | Monotonic Stack       | O(n)           | O(n)   | Next greater/smaller, histogram           |
| 9  | Backtracking          | O(2^n) / n!    | O(n)   | Generate all combos/permutations          |
| 10 | Modular Arithmetic    | O(log n)       | O(n)   | nCr, power, inverse mod MOD               |
| 11 | Binary Search Answer  | O(log R * f()) | O(1)   | Minimize max / maximize min               |
| 12 | Sliding Window        | O(n)           | O(k)   | Contiguous subarray/substring             |
| 13 | Kadane's              | O(n)           | O(1)   | Maximum subarray sum                      |
| 14 | Topological Sort      | O(V + E)       | O(V)   | Task ordering, detect cycle in DAG        |
| 15 | Fenwick Tree          | O(n log n)     | O(n)   | Prefix sum + point update (simpler than ST)|
| 16 | DSU + Rollback        | O(n alpha(n))  | O(n)   | Offline connectivity queries              |
| 17 | LCA (Binary Lifting)  | O(n log n)     | O(n log n)| Distance between tree nodes            |
| 18 | KMP                   | O(n + m)       | O(m)   | Exact pattern matching                    |
| 19 | Rabin-Karp            | O(n + m) avg   | O(1)   | Multiple pattern matching, rolling hash   |
| 20 | Matrix Exponentiation | O(k^3 log n)   | O(k^2) | Fast Fibonacci, linear recurrences        |

**Legend:** V = vertices, E = edges, n = input size, L = string length, k = matrix size, R = binary search range

---

## 1. Fast I/O Template

### Why This Matters

Python's default `input()` is **slow** — it strips whitespace, decodes bytes,
and does extra processing. When a problem reads 10^5 lines, this overhead adds
up. `sys.stdin.readline` is **~5-10x faster** and is the single most important
optimization in Python CP.

### When to Use

```
Problem input size?
  |
  +-- >= 10^4 lines  -->  MUST use this template
  +-- < 10^4 lines   -->  input() works, but this is always safe
  +-- Multiple test cases  -->  Use the loop variant
```

### How It Works - Step by Step

```
  input = sys.stdin.readline
         |
         v
  Built-in input():     "  42  \n"  ->  "42"        (strips + decodes)
  sys.stdin.readline(): "  42  \n"  ->  "  42  \n"   (raw, use .strip())


  Reading a line of numbers: "5 3 7 1 9\n"
         |
         v
  input().split()   ->  ['5', '3', '7', '1', '9']     (split by whitespace)
         |
         v
  map(int, ...)     ->  5, 3, 7, 1, 9                  (convert each to int)
         |
         v
  list(...)         ->  [5, 3, 7, 1, 9]                 (make it a list)
```

### Complexity

- **Time:** O(n) per line (unavoidable), but constant factor ~5x smaller than default
- **Space:** O(1) extra overhead

### Key Pattern: Multiple Test Cases

```
  Standard input layout:
  ┌─────────────────┐
  │  t               │  <-- number of test cases
  │  n               │  <-- size of array for test case 1
  │  a1 a2 ... an    │  <-- array elements
  │  n               │  <-- size for test case 2
  │  a1 a2 ... an    │
  │  ...             │
  └─────────────────┘
```

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    # solution here
    print(result)

# For multiple test cases
def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        # solution here
        print(result)

solve()
```

---

## 2. BFS Template

### Why This Matters

BFS explores nodes **level by level** (all neighbors first, then their neighbors).
This guarantees the **shortest path** in unweighted graphs/grids.

### When to Use

```
Problem keyword?  -->
  |
  +-- "shortest path" + unweighted grid/graph  -->  USE BFS
  +-- "minimum steps" to reach target           -->  USE BFS
  +-- "level order traversal"                   -->  USE BFS
  +-- "nearest" in a grid with obstacles         -->  USE BFS
  +-- "01 BFS" or weighted edges                 -->  USE Dijkstra instead (Template 4)
```

### Visual: How BFS Explores

```
  Start at node 0. Explore all neighbors, then their neighbors...

      Graph:              BFS Level-by-Level Exploration:

        0                  Level 0:  [0]
       / \                 Level 1:  [1, 2]
      1   2                Level 2:  [3, 4]
     / \   \               Level 3:  [5]
    3   4   5

  Queue progression:
  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐
  │ [0] │[1,2]│[2,3]│[3,4]│[4,5]│ [5] │ [ ] │
  └─────┴─────┴─────┴─────┴─────┴─────┴─────┘
   pop 0  pop 1  pop 2  pop 3  pop 4  pop 5  done!
```

### Step-by-Step Walkthrough (Grid BFS)

```
  Grid (3x4), S = start, T = target, # = wall:

      S . . .
      . # # .
      . . . T

  Step 1: Queue = [(0,0)], Dist = {(0,0): 0}
  Step 2: Pop (0,0) -> check neighbors:
          (0,1): empty, add, dist=1
          (1,0): empty, add, dist=1
  Step 3: Pop (0,1) -> check neighbors:
          (0,2): empty, add, dist=2
          (1,1): '#', skip
  ...continues until (2,3) is reached with dist=4
```

### Complexity

- **Time:** O(V + E) for graph, O(rows × cols) for grid
- **Space:** O(V) for visited set + queue

```python
from collections import deque

def bfs(start, graph):
    """BFS traversal. Returns dict of {node: distance from start}."""
    queue = deque([start])
    visited = {start: 0}
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited[neighbor] = visited[node] + 1
                queue.append(neighbor)
    return visited

def bfs_shortest_path(start, end, graph):
    """Returns shortest path (list) from start to end."""
    if start == end:
        return [start]
    
    queue = deque([start])
    visited = {start: None}
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited[neighbor] = node
                if neighbor == end:
                    # Reconstruct path
                    path = []
                    curr = end
                    while curr is not None:
                        path.append(curr)
                        curr = visited[curr]
                    return path[::-1]
                queue.append(neighbor)
    return []  # no path

def bfs_grid(start, grid, rows, cols):
    """BFS on a grid. start = (r, c). Returns distances."""
    queue = deque([start])
    dist = {start: 0}
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in dist:
                if grid[nr][nc] != '#':  # not a wall
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    queue.append((nr, nc))
    return dist
```

---

## 3. DFS Template

### Why This Matters

DFS explores **as deep as possible** before backtracking. It's the Swiss Army
knife of graph algorithms — used for connectivity, cycle detection, path finding,
and topological sort.

### When to Use

```
Problem keyword?  -->
  |
  +-- "connected components"       -->  DFS (or BFS)
  +-- "cycle detection"            -->  DFS with coloring
  +-- "is there a path?"           -->  DFS
  +-- "topological ordering"       -->  DFS (Template 14 for Kahn's BFS variant)
  +-- "generate all paths"         -->  DFS + backtracking
  +-- "maze solving"               -->  DFS
  +-- needs shortest path?         -->  Use BFS instead (Template 2)
```

### Visual: DFS vs BFS

```
  Same graph, different traversal order:

       A              DFS goes DEEP first:
      / \             A -> B -> D -> (backtrack) -> E -> (backtrack)
     B   C            -> C -> F
    / \   \
   D   E   F

  BFS: A, B, C, D, E, F   (level by level)
  DFS: A, B, D, E, C, F   (depth first, then backtrack)
```

### Iterative vs Recursive DFS

```
  Recursive:                    Iterative:
  + Clean code                  + No stack overflow risk
  + Natural for tree problems   + Same time complexity
  - Risk of stack overflow      + Slightly more code
    for deep graphs (10^5+)
```

### Key Concept: Topological Sort via DFS

```
  Post-order DFS on DAG gives reverse topological order:

      0 --> 1 --> 3
      |         ^
      v         |
      2 --------+

  DFS post-order:  3, 1, 2, 0
  Topo order:      0, 2, 1, 3  (reversed)
```

### Complexity

- **Time:** O(V + E) — each node and edge visited once
- **Space:** O(V) — visited set + recursion stack / explicit stack

```python
def dfs(node, graph, visited):
    """Iterative DFS using a stack."""
    stack = [node]
    while stack:
        curr = stack.pop()
        if curr in visited:
            continue
        visited.add(curr)
        for neighbor in graph[curr]:
            if neighbor not in visited:
                stack.append(neighbor)

def dfs_recursive(node, graph, visited):
    """Recursive DFS."""
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(neighbor, graph, visited)

def dfs_topological(node, graph, visited, order):
    """DFS for topological sorting."""
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_topological(neighbor, graph, visited, order)
    order.append(node)

def dfs_connected_components(n, graph):
    """Find all connected components."""
    visited = set()
    components = []
    
    for i in range(n):
        if i not in visited:
            component = []
            stack = [i]
            while stack:
                node = stack.pop()
                if node in visited:
                    continue
                visited.add(node)
                component.append(node)
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
            components.append(sorted(component))
    
    return components
```

---

## 4. Dijkstra Template

### Why This Matters

BFS only works for **unweighted** graphs. When edges have weights (costs, distances),
Dijkstra finds the shortest path using a **priority queue** (min-heap).

### When to Use

```
Problem has weighted edges?  -->
  |
  +-- All weights >= 0?       -->  USE Dijkstra
  +-- Some weights negative?  -->  USE Bellman-Ford (not in this template set)
  +-- Need path itself?       -->  Use dijkstra_with_path variant
  +-- Just need distances?    -->  Use dijkstra variant
```

### Visual: How Dijkstra Works

```
  Graph with weights:
        1
   0 ------- 1
   |         |
   4         2
   |         |
   2 ------- 3
        3

  Step-by-step (start=0):

  ┌──────┬──────────┬─────────────────────────────────┐
  │ Step │ Heap     │ dist[]                           │
  ├──────┼──────────┼─────────────────────────────────┤
  │  0   │ [(0,0)]  │ [0, inf, inf, inf]              │
  │  1   │ [(1,1),  │ [0, 1, 4, inf]  -- pop 0, relax │
  │      │  (4,2)]  │   neighbors                     │
  │  2   │ [(2,3),  │ [0, 1, 3, inf]  -- pop 1, relax │
  │      │  (4,2)]  │   1 -> 3 (cost 2)               │
  │  3   │ [(3,3),  │ [0, 1, 3, 5]   -- pop 2, relax  │
  │      │  (3,3)]  │   2 -> 3 (cost 3)               │
  │  4   │ [(3,3)]  │ [0, 1, 3, 5]   -- pop 3, done   │
  └──────┴──────────┴─────────────────────────────────┘

  Key insight: Once a node is popped from heap, its distance is FINAL
  (because all edge weights >= 0).
```

### Complexity

- **Time:** O((V + E) log V) — each edge processed once, heap operations log V
- **Space:** O(V) — distance array + heap

```python
import heapq

def dijkstra(start, graph, n):
    """Shortest path from start to all nodes.
    graph: adjacency list where graph[u] = [(v, weight), ...]
    Returns: list of distances
    """
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]
    
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for neighbor, weight in graph[node]:
            if dist[node] + weight < dist[neighbor]:
                dist[neighbor] = dist[node] + weight
                heapq.heappush(heap, (dist[neighbor], neighbor))
    
    return dist

def dijkstra_with_path(start, end, graph, n):
    """Shortest path from start to end with path reconstruction."""
    dist = [float('inf')] * n
    prev = [-1] * n
    dist[start] = 0
    heap = [(0, start)]
    
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        if node == end:
            break
        for neighbor, weight in graph[node]:
            if dist[node] + weight < dist[neighbor]:
                dist[neighbor] = dist[node] + weight
                prev[neighbor] = node
                heapq.heappush(heap, (dist[neighbor], neighbor))
    
    # Reconstruct path
    if dist[end] == float('inf'):
        return float('inf'), []
    
    path = []
    curr = end
    while curr != -1:
        path.append(curr)
        curr = prev[curr]
    return dist[end], path[::-1]
```

---

## 5. Union-Find Template

### Why This Matters

Union-Find (Disjoint Set Union / DSU) efficiently tracks which elements belong
to the same group. It supports two operations: **find** (which group?) and
**union** (merge two groups) in nearly O(1) amortized time.

### When to Use

```
Problem keyword?  -->
  |
  +-- "are these two nodes connected?"    -->  Union-Find
  +-- "how many connected components?"    -->  Union-Find
  +-- "merge two groups/sets"             -->  Union-Find
  +-- "detect cycle in undirected graph"  -->  Union-Find
  +-- "Kruskal's MST"                     -->  Union-Find
  +-- dynamic connectivity queries        -->  Union-Find
```

### Visual: How Union-Find Works

```
  Initially: Each element is its own set.

  [0] [1] [2] [3] [4]    <-- 5 separate components

  union(0, 1):           union(2, 3):
  [0]──[1] [2] [3] [4]   [0]──[1] [2]──[3] [4]
   └──────┘              parent[1] = 0     parent[3] = 2

  union(0, 2):
  [0]──[1]               [0]──[1]
   \                      /
    [2]──[3]    --->    [2]──[3]     All in one tree!
                    parent[2] = 0

  Path Compression (find(3)):
  Before:  0              After find(3):
          / \             0
         1   2            /|\
             |           1 2 3    <-- 3 now points directly to root!
             3

  Union by Rank (attach smaller tree under larger):
  Always make the shorter tree a child of the taller one.
  This keeps trees balanced = fast finds.
```

### Complexity

- **Time:** O(alpha(n)) amortized per operation — alpha is inverse Ackermann,
  effectively O(1) for all practical inputs (n <= 10^6)
- **Space:** O(n) — parent and rank/size arrays

```python
class UnionFind:
    """Disjoint Set Union with path compression and union by rank."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n  # number of connected components
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # already in same set
        
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        
        self.components -= 1
        return True
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)

class UnionFindWithSize:
    """DSU with component size tracking."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        
        if self.size[px] < self.size[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        self.components -= 1
        return True
    
    def get_size(self, x):
        return self.size[self.find(x)]
```

---

## 6. Segment Tree Template

### Why This Matters

Naive range sum: O(n) per query. With updates, that's O(n²) for q queries.
Segment Tree does **both** range queries and point updates in **O(log n)**.

### When to Use

```
Problem has?  -->
  |
  +-- Range query (sum/min/max) + Point update  -->  Segment Tree
  +-- Range query + Range update (lazy)          -->  Segment Tree + Lazy Propagation
  +-- Just prefix sums, no updates?              -->  Use simple prefix array
  +-- Just prefix sums + point updates?          -->  Fenwick Tree (simpler, Template 15)
  +-- Need median / order statistics?            -->  Segment Tree with counts
```

### Visual: Segment Tree Structure

```
  Array: [1, 3, 5, 7, 9, 11]

  Segment Tree (stores sums):

                    [36]              Range [0,5]
                   /    \
              [9]          [27]        [0,2]     [3,5]
             /   \        /    \
         [4]     [5]  [16]    [11]    [0,1] [2,2] [3,4] [5,5]
        /   \          /  \          /  \
      [1]   [3]      [7]  [9]     [1]  [3]  [5]  [7]  [9]  [11]
       ^     ^                              Leaf nodes = original array

  Query: sum(1, 4) = ?
  Path:  [36] -> [9] (covers 0-2, partially) -> [5] (covers 1-2, YES)
                         -> [27] (covers 3-5, partially) -> [16] (covers 3-4, YES)
  Result: 5 + 16 = 21  (which is 3+5+7+9 = 24... wait let me recalc)
  Actually: sum of index 1..4 = 3+5+7+9 = 24
  Tree query: node [5] covers [1,2]=5+7... 
```

### Step-by-Step: Query Range [1, 4]

```
  query(node=1, start=0, end=5, l=1, r=4)

  Step 1: node=1 covers [0,5], not fully in [1,4]
          -> go to children

  Step 2: node=2 covers [0,2], partially overlaps [1,4]
          -> go to children
      Step 2a: node=4 covers [0,1], partially overlaps [1,4]
               -> go to children
          Step 2a-i:  node=8 covers [0,0], NOT in [1,4] -> return 0
          Step 2a-ii: node=9 covers [1,1], IN [1,4] -> return 3 ✓

      Step 2b: node=5 covers [2,2], IN [1,4] -> return 5 ✓

  Step 3: node=3 covers [3,5], partially overlaps [1,4]
          -> go to children
      Step 3a: node=6 covers [3,4], IN [1,4] -> return 16 ✓
      Step 3b: node=7 covers [5,5], NOT in [1,4] -> return 0

  Result: 3 + 5 + 16 = 24  ✓
```

### Complexity

- **Build:** O(n)
- **Query:** O(log n)
- **Update:** O(log n)
- **Space:** O(4n) — array of size 4n for safety

```python
class SegmentTree:
    """Segment tree for range sum queries with point updates."""
    
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.build(data, 1, 0, self.n - 1)
    
    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        self.build(data, 2 * node, start, mid)
        self.build(data, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def update(self, idx, val):
        """Update element at index idx to val."""
        self._update(1, 0, self.n - 1, idx, val)
    
    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self._update(2 * node, start, mid, idx, val)
        else:
            self._update(2 * node + 1, mid + 1, end, idx, val)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def query(self, l, r):
        """Query sum of elements in range [l, r]."""
        return self._query(1, 0, self.n - 1, l, r)
    
    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return self._query(2 * node, start, mid, l, r) + \
               self._query(2 * node + 1, mid + 1, end, l, r)

class SegmentTreeMinMax:
    """Segment tree for range min/max queries."""
    
    def __init__(self, data, func=min):
        self.n = len(data)
        self.func = func
        self.default = float('inf') if func == min else float('-inf')
        self.tree = [self.default] * (4 * self.n)
        self.build(data, 1, 0, self.n - 1)
    
    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        self.build(data, 2 * node, start, mid)
        self.build(data, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.func(self.tree[2 * node], self.tree[2 * node + 1])
    
    def query(self, l, r):
        return self._query(1, 0, self.n - 1, l, r)
    
    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return self.default
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return self.func(self._query(2 * node, start, mid, l, r),
                         self._query(2 * node + 1, mid + 1, end, l, r))
```

---

## 7. Trie Template

### Why This Matters

A Trie (prefix tree) stores strings character-by-character in a tree. It enables
**O(L)** prefix matching, search, and autocomplete — where L is the word length,
independent of how many words are stored.

### When to Use

```
Problem keyword?  -->
  |
  +-- "prefix matching" / "starts with"   -->  Trie
  +-- "autocomplete" / "word search"      -->  Trie
  +-- "count words with prefix"           -->  Trie (with count field)
  +-- "XOR maximum" with numbers          -->  Binary Trie variant
  +-- "spell check" / "dictionary"        -->  Trie
  +-- just substring search?              -->  Use KMP (Template 18) instead
```

### Visual: Trie Structure

```
  Insert: "app", "apple", "application", "bat", "ball"

                  root
                /      \
              a          b
              |          |
              p          a
             / \        / \
            p   p*     t*  l
            |   |          |
           l*  i           l*
           |   |
           e*  c
               |
               a
               |
               t
               |
               i
               |
               o
               |
               n*

  * = is_end of a word (complete word ends here)

  Search "apple":  root -> a -> p -> p -> l -> e*   FOUND
  Search "app":    root -> a -> p -> p*              FOUND
  Search "ap":     root -> a -> p (not is_end)       NOT FOUND
  Starts "app":    root -> a -> p -> p               EXISTS
  Count "app":     Follow path to second p, return node.count = 3
                   (app, apple, application all have prefix "app")
```

### Complexity

- **Insert:** O(L) where L = word length
- **Search:** O(L)
- **Space:** O(N × L × alphabet_size) worst case, but shared prefixes save memory
  (N = number of words)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0  # number of words with this prefix

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.count += 1
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
    
    def count_words_with_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.count
    
    def delete(self, word):
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                return len(node.children) == 0
            
            char = word[depth]
            if char not in node.children:
                return False
            
            should_delete = _delete(node.children[char], word, depth + 1)
            if should_delete:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end
            return False
        
        _delete(self.root, word, 0)

# Usage example
trie = Trie()
trie.insert("apple")
trie.insert("app")
trie.insert("application")
print(trie.search("apple"))      # True
print(trie.starts_with("app"))   # True
print(trie.count_words_with_prefix("app"))  # 3
```

---

## 8. Monotonic Stack Template

### Why This Matters

Monotonic stack solves "next greater/smaller element" problems in **O(n)**.
The stack maintains elements in sorted order, allowing you to find relationships
between elements in a single pass.

### When to Use

```
Problem keyword?  -->
  |
  +-- "next greater element"               -->  Monotonic decreasing stack
  +-- "next smaller element"               -->  Monotonic increasing stack
  +-- "largest rectangle in histogram"     -->  Monotonic stack
  +-- "trapping rain water"                -->  Monotonic stack (or prefix arrays)
  +-- "daily temperatures"                 -->  Monotonic stack
  +-- "stock span problem"                 -->  Monotonic stack
```

### Visual: Next Greater Element

```
  Array:  [2, 1, 2, 4, 3]

  Scan left to right, maintain decreasing stack:

  i=0: stack=[], push 0(val=2)     stack=[0]
  i=1: arr[1]=1 < arr[0]=2        stack=[0,1]
  i=2: arr[2]=2 > arr[1]=1        pop 1 -> result[1]=2
       arr[2]=2 == arr[0]=2       stack=[0,2]
  i=3: arr[3]=4 > arr[2]=2        pop 2 -> result[2]=4
       arr[3]=4 > arr[0]=2        pop 0 -> result[0]=4
       push 3                      stack=[3]
  i=4: arr[4]=3 < arr[3]=4        stack=[3,4]

  result = [4, 2, 4, -1, -1]

  Visual:
  [2] [1] [2] [4] [3]
   ^   ^   ^   ^   ^
   |   |   |   |   no next element -> -1
   |   |   |   no greater element -> -1
   |   |   |
   |   |   next greater is 4
   |   next greater is 2
   next greater is 4
```

### Visual: Largest Rectangle in Histogram

```
  Heights: [2, 1, 5, 6, 2, 3]

     ██
     ██ ██
     ██ ██
  ██ ██ ██
  ██ ██ ██ ██
  ██ ██ ██ ██    ██
  ─────────────────
  0  1  2  3  4  5

  For each bar, find how far it extends left and right
  (while maintaining height >= current bar).

  Bar 2 (h=5): extends from index 2 to 3 -> area = 5 * 2 = 10
  Bar 3 (h=6): extends from index 3 to 3 -> area = 6 * 1 = 6
  Best: Bar 2 -> area = 10
```

### Complexity

- **Time:** O(n) — each element pushed and popped at most once
- **Space:** O(n) — stack stores indices

```python
def next_greater_element(arr):
    """Find the next greater element for each element in the array.
    Returns list where result[i] = next element > arr[i], or -1 if none.
    """
    n = len(arr)
    result = [-1] * n
    stack = []  # stores indices
    
    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            result[stack.pop()] = arr[i]
        stack.append(i)
    return result

def next_smaller_element(arr):
    """Find the next smaller element for each element."""
    n = len(arr)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        while stack and arr[stack[-1]] > arr[i]:
            result[stack.pop()] = arr[i]
        stack.append(i)
    return result

def previous_greater_element(arr):
    """Find the previous greater element for each element."""
    n = len(arr)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        if stack:
            result[i] = arr[stack[-1]]
        stack.append(i)
    return result

def largest_rectangle_histogram(heights):
    """Largest rectangle in histogram."""
    n = len(heights)
    stack = []
    max_area = 0
    
    for i in range(n + 1):
        while stack and (i == n or heights[stack[-1]] > heights[i]):
            h = heights[stack.pop()]
            w = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, h * w)
        stack.append(i)
    
    return max_area

def trapping_rain_water(height):
    """Trapping rain water problem."""
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n
    
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])
    
    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])
    
    water = 0
    for i in range(n):
        water += min(left_max[i], right_max[i]) - height[i]
    return water
```

---

## 9. Backtracking Template

### Why This Matters

Backtracking systematically explores all possible solutions by **building choices
incrementally** and **undoing** bad decisions. It's the go-to for generating all
permutations, combinations, subsets, and constraint-satisfaction problems.

### When to Use

```
Problem keyword?  -->
  |
  +-- "generate all permutations"          -->  Backtracking
  +-- "generate all combinations"          -->  Backtracking
  +-- "generate all subsets"               -->  Backtracking
  +-- "N-Queens" / "Sudoku"                -->  Backtracking with constraints
  +-- "word search" in grid                -->  DFS + backtracking
  +-- "partition into k subsets"           -->  Backtracking
  +-- Problem asks for "all possible"       -->  Backtracking
```

### Visual: How Backtracking Works (Subsets of [1, 2, 3])

```
  Decision tree:

                          []
                  /         |         \
               [1]        [2]        [3]
              /   \        |          |
          [1,2]  [1,3]  [2,3]       |
            |      |       |         |
        [1,2,3] [1,2,3] [1,2,3] [1,2,3]

  All subsets: [], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]

  Key: At each step, pick one element from remaining, add to path,
  recurse, then REMOVE (backtrack) before trying next choice.
```

### The Backtracking Pattern

```
  def backtrack(path, choices):
      if goal_reached:
          result.append(path[:])    # IMPORTANT: copy the path!
          return

      for choice in choices:
          path.append(choice)       # 1. CHOOSE
          backtrack(path, new_choices)  # 2. EXPLORE
          path.pop()                # 3. UN-CHOOSE (backtrack!)
```

### Complexity

- **Permutations:** O(n! × n) — n! permutations, each of length n
- **Combinations:** O(C(n,k) × k) — C(n,k) combinations
- **Subsets:** O(2^n × n) — 2^n subsets
- **N-Queens:** O(n!) — prune early when queen placement conflicts

```python
def permutations(nums):
    """Generate all permutations of nums."""
    result = []
    
    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        for i, num in enumerate(remaining):
            path.append(num)
            backtrack(path, remaining[:i] + remaining[i + 1:])
            path.pop()
    
    backtrack([], nums)
    return result

def combinations(n, k):
    """Generate all combinations of k numbers from 1 to n."""
    result = []
    
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(1, [])
    return result

def subsets(nums):
    """Generate all subsets of nums."""
    result = []
    
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(0, [])
    return result

def subsets_with_duplicates(nums):
    """Generate all unique subsets (nums may contain duplicates)."""
    result = []
    nums.sort()
    
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(0, [])
    return result

def n_queens(n):
    """Solve N-Queens problem. Returns all valid board configurations."""
    result = []
    
    def backtrack(row, cols, diag1, diag2, board):
        if row == n:
            result.append(["".join(r) for r in board])
            return
        
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            backtrack(row + 1, cols, diag1, diag2, board)
            
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    
    board = [['.' for _ in range(n)] for _ in range(n)]
    backtrack(0, set(), set(), set(), board)
    return result
```

---

## 10. Modular Arithmetic Template

### Why This Matters

CP problems often ask for answers **modulo 10^9 + 7** because numbers get huge
(e.g., 100! has 158 digits). Modular arithmetic keeps numbers manageable while
preserving mathematical properties.

### When to Use

```
Problem says "answer modulo 10^9+7"?  -->
  |
  +-- Need nCr (combinations)?    -->  precompute_factorials() + nCr()
  +-- Need nPr (permutations)?    -->  precompute_factorials() + nPr()
  +-- Need a^b % MOD?             -->  power() (fast exponentiation)
  +-- Need a/b % MOD?             -->  mod_div() (Fermat's little theorem)
  +-- Need a*b % MOD?             -->  mod_mul()
```

### Key Concepts

```
  MOD = 10^9 + 7 (a prime number)

  Why prime? Because Fermat's Little Theorem applies:
    a^(p-1) ≡ 1 (mod p)  when p is prime and a is not divisible by p
    Therefore: a^(-1) ≡ a^(p-2) (mod p)

  This lets us do modular DIVISION:
    a / b  (mod p)  =  a * b^(p-2)  (mod p)
```

### Visual: Fast Exponentiation (Binary Exponentiation)

```
  Compute 3^13 % 7:

  13 in binary: 1101

  Step:    base    exp     result
  Init:      3     1101     1
  exp & 1?   3      yes    1 * 3 = 3
  square:    3^2=9  110     3
  exp & 1?   9      yes    3 * 9 = 27 ≡ 6 (mod 7)
  square:    9^2=81 11      6
  exp & 1?   81     yes    6 * 81 = 486 ≡ 3 (mod 7)
  square:    ...    1       3
  exp & 1?   ...    yes    3 * ... ≡ 5 (mod 7)

  Result: 3^13 % 7 = 5

  Time: O(log exp) instead of O(exp)!
```

### Visual: Factorial Precomputation

```
  fact[0] = 1
  fact[1] = 1 * 1 = 1
  fact[2] = 1 * 2 = 2
  fact[3] = 2 * 3 = 6
  ...
  fact[n] = fact[n-1] * n % MOD

  Then nCr = fact[n] * inv(fact[r]) * inv(fact[n-r]) % MOD
```

### Complexity

- **Fast power:** O(log exp)
- **Precompute factorials:** O(n)
- **nCr query:** O(log MOD) after precomputation

```python
MOD = 10**9 + 7

def power(base, exp, mod=MOD):
    """Fast exponentiation: base^exp % mod. Time: O(log exp)"""
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result

def mod_inverse(a, mod=MOD):
    """Modular inverse using Fermat's little theorem. a^(-1) = a^(mod-2) % mod"""
    return power(a, mod - 2, mod)

def mod_add(a, b, mod=MOD):
    return (a + b) % mod

def mod_sub(a, b, mod=MOD):
    return (a - b + mod) % mod

def mod_mul(a, b, mod=MOD):
    return (a * b) % mod

def mod_div(a, b, mod=MOD):
    return mod_mul(a, mod_inverse(b, mod))

# Precompute factorials
def precompute_factorials(n, mod=MOD):
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    return fact

# nCr % MOD
def nCr(n, r, fact, mod=MOD):
    if r < 0 or r > n:
        return 0
    return fact[n] * mod_inverse(fact[r] * fact[n - r] % mod, mod) % mod

# nPr % MOD
def nPr(n, r, fact, mod=MOD):
    if r < 0 or r > n:
        return 0
    return fact[n] * mod_inverse(fact[n - r], mod) % mod
```

---

## 11. Binary Search on Answer Template

### Why This Matters

Instead of binary searching on an array, you binary search on the **answer space**.
The idea: if you can check whether a candidate answer works in O(f(n)), you can
find the optimal answer in O(log(R) × f(n)), where R is the range of possible answers.

### When to Use

```
Problem has these properties?  -->
  |
  +-- Answer is a number (not a path/structure)     -->  Yes
  +-- You can CHECK if a candidate works in O(n)    -->  Yes
  +-- Binary monotonicity:                          -->  Yes
     "if X works, does X+1 work?"                    -->  Minimize: YES
     "if X works, does X-1 work?"                    -->  Maximize: YES
  +-- Then USE THIS TEMPLATE
```

### Visual: Binary Search on Answer

```
  Problem: Split array into m subarrays, minimize the maximum subarray sum.

  Answer space: [max(nums), sum(nums)]

  Example: nums = [7, 2, 5, 10, 8], m = 2
  Answer space: [10, 32]

  Binary search:
  ┌─────┬──────────────────────────────────────────────┐
  │ lo  │ 10  (minimum possible = max element)         │
  │ hi  │ 32  (maximum possible = sum of all)          │
  │ mid │ 21  -> can we split into <= 2 groups         │
  │     │     with max sum 21? YES (7+2+5=14, 10+8=18) │
  │     │     -> try smaller: hi = 21                  │
  │ mid │ 15  -> can we split? NO                      │
  │     │     -> try bigger: lo = 16                   │
  │ mid │ 18  -> can we split? YES (7+2+5=14, 10+8=18) │
  │     │     -> try smaller: hi = 18                  │
  │ ... │ converges to 18                              │
  └─────┴──────────────────────────────────────────────┘
```

### The Two Variants

```
  Minimize maximum (e.g., split array):
    check(mid) = True  ->  hi = mid      (try smaller)
    check(mid) = False ->  lo = mid + 1  (must go bigger)
    mid = (lo + hi) // 2

  Maximize minimum (e.g., allocate flowers):
    check(mid) = True  ->  lo = mid      (try bigger)
    check(mid) = False ->  hi = mid - 1  (must go smaller)
    mid = (lo + hi + 1) // 2    <-- NOTE: +1 to avoid infinite loop!
```

### Complexity

- **Time:** O(log(R) × f(n)) where R = answer range, f(n) = check function time
- **Space:** O(1) or O(n) depending on check function

```python
def binary_search_minimize(lo, hi, check):
    """Find minimum value in [lo, hi] where check(mid) is True.
    Assumes: if check(mid) is True, check(mid+1) is also True.
    """
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

def binary_search_maximize(lo, hi, check):
    """Find maximum value in [lo, hi] where check(mid) is True.
    Assumes: if check(mid) is True, check(mid-1) is also True.
    """
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if check(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo

# Example: Split array into m subarrays such that max sum is minimized
def split_array(nums, m):
    def can_split(max_sum):
        count = 1
        current = 0
        for num in nums:
            if current + num > max_sum:
                count += 1
                current = num
            else:
                current += num
        return count <= m
    
    lo = max(nums)
    hi = sum(nums)
    return binary_search_minimize(lo, hi, can_split)
```

---

## 12. Sliding Window Template

### Why This Matters

Sliding window processes **contiguous subarrays/substrings** in O(n) instead
of O(n²). The window expands right and contracts left, maintaining a valid
window throughout.

### When to Use

```
Problem has these properties?  -->
  |
  +-- Contiguous subarray/substring required   -->  Yes
  +-- Fixed size window?                       -->  Use sliding_window_fixed
  +-- Variable size with constraint?           -->  Use sliding_window_variable
  +-- "Longest subarray where..."              -->  Sliding window
  +-- "Smallest subarray containing..."        -->  Sliding window
  +-- "Maximum/minimum sum of k elements"      -->  Sliding window fixed
```

### Visual: Fixed-Size Window (k=3)

```
  Array: [1, 2, 3, 4, 5, 6, 7]

  Window slides right by 1 each step:

  Step 1: [1, 2, 3] 4, 5, 6, 7    sum = 6
  Step 2:  1 [2, 3, 4] 5, 6, 7    sum = 9   (+4, -1)
  Step 3:  1, 2 [3, 4, 5] 6, 7    sum = 12  (+5, -2)
  Step 4:  1, 2, 3 [4, 5, 6] 7    sum = 15  (+6, -3)
  Step 5:  1, 2, 3, 4 [5, 6, 7]   sum = 18  (+7, -4)

  Key: Remove left element, add right element -> O(1) update!
```

### Visual: Variable-Size Window

```
  Problem: Longest substring without repeating characters.
  String: "abcabcbb"

  left  right  window    valid?
  0     0      "a"       yes     max_len = 1
  0     1      "ab"      yes     max_len = 2
  0     2      "abc"     yes     max_len = 3
  0     3      "abca"    NO! 'a' repeats -> shrink left
  1     3      "bca"     yes     max_len = 3
  1     4      "bcab"    NO! 'b' repeats -> shrink left
  2     4      "cab"     yes     max_len = 3
  ...
  Result: 3 ("abc")
```

### Complexity

- **Time:** O(n) — each element added and removed at most once
- **Space:** O(k) where k = window size or alphabet size

```python
from collections import Counter

def sliding_window_fixed(s, k):
    """Fixed-size sliding window of size k."""
    window = Counter()
    result = []
    
    for right in range(len(s)):
        window[s[right]] += 1
        
        if right >= k:
            left = right - k
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
        
        if right >= k - 1:
            # Process window
            result.append(dict(window))
    
    return result

def sliding_window_variable(s, condition):
    """Variable-size sliding window with a condition."""
    window = Counter()
    left = 0
    result = 0
    
    for right in range(len(s)):
        window[s[right]] += 1
        
        while not condition(window):
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        
        # Update result (e.g., max length, count, etc.)
        result = max(result, right - left + 1)
    
    return result

# Example: Longest substring without repeating characters
def length_of_longest_substring(s):
    char_set = set()
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)
    
    return max_len

# Example: Minimum window substring
def min_window(s, t):
    from collections import Counter
    
    if not t or not s:
        return ""
    
    t_count = Counter(t)
    required = len(t_count)
    formed = 0
    window_counts = {}
    
    left = 0
    min_len = float('inf')
    min_left = 0
    
    for right in range(len(s)):
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        if char in t_count and window_counts[char] == t_count[char]:
            formed += 1
        
        while formed == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left
            
            left_char = s[left]
            window_counts[left_char] -= 1
            if left_char in t_count and window_counts[left_char] < t_count[left_char]:
                formed -= 1
            left += 1
    
    return "" if min_len == float('inf') else s[min_left:min_left + min_len]
```

---

## 13. Kadane's Algorithm Template

### Why This Matters

Finding the maximum subarray sum naively is O(n²). Kadane's algorithm does it
in **O(n)** using the key insight: at each position, either extend the current
subarray or start a new one.

### When to Use

```
Problem keyword?  -->
  |
  +-- "maximum subarray sum"               -->  Kadane's
  +-- "maximum sum contiguous subarray"    -->  Kadane's
  +-- "largest sum subarray"               -->  Kadane's
  +-- "circular array max subarray sum"    -->  Kadane's circular variant
  +-- "maximum product subarray"           -->  Modified Kadane (track min too)
```

### Visual: How Kadane's Works

```
  Array: [-2, 1, -3, 4, -1, 2, 1, -5, 4]

  i:       0    1    2    3    4    5    6    7    8
  arr[i]: -2    1   -3    4   -1    2    1   -5    4
  curr:   -2    1   -2    4    3    5    6    1    5
  max:    -2    1    1    4    4    5    6    6    6

  Key decisions:
  i=1: max(1, -2+1) = 1    -> Start new (1 > -1)
  i=2: max(-3, 1-3) = -2   -> Extend (not starting from -3)
  i=3: max(4, -2+4) = 4    -> Start new (4 > 2)
  ...
  i=6: max(1, 5+1) = 6     -> Extend!

  Best subarray: [4, -1, 2, 1] with sum = 6
  Visual:
  [-2] [1] [-3] [4, -1, 2, 1] [-5] [4]
                      ^^^^^^^^
                   maximum sum = 6
```

### Circular Variant

```
  For circular arrays, the max subarray might WRAP AROUND:

  [5, -3, 5] -> max normal = 5, max circular = 5+5 = 10 (wraps!)

  Trick: max_circular = total_sum - min_subarray_sum
  (If we remove the minimum subarray, what's left wraps around)

  Final answer = max(normal_max, circular_max)
  Special case: if all negative, circular_max = 0 (invalid), use normal_max
```

### Complexity

- **Time:** O(n) — single pass through array
- **Space:** O(1) — just a few variables

```python
def kadane(arr):
    """Maximum subarray sum (can be all negative)."""
    max_sum = curr_sum = arr[0]
    for num in arr[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)
    return max_sum

def kadane_with_indices(arr):
    """Maximum subarray sum with start and end indices."""
    max_sum = curr_sum = arr[0]
    start = end = temp_start = 0
    
    for i in range(1, len(arr)):
        if arr[i] > curr_sum + arr[i]:
            curr_sum = arr[i]
            temp_start = i
        else:
            curr_sum += arr[i]
        
        if curr_sum > max_sum:
            max_sum = curr_sum
            start = temp_start
            end = i
    
    return max_sum, start, end

def kadane_circular(arr):
    """Maximum circular subarray sum."""
    # Case 1: Normal Kadane's (max subarray not wrapping around)
    normal_max = kadane(arr)
    
    # Case 2: Circular (min subarray in the middle, sum - min = max wrapping)
    total_sum = sum(arr)
    min_sum = float('inf')
    curr_min = 0
    for num in arr:
        curr_min = min(num, curr_min + num)
        min_sum = min(min_sum, curr_min)
    
    circular_max = total_sum - min_sum
    
    # If all elements are negative, circular_max will be 0 (empty subarray)
    # which is invalid, so return normal_max
    if circular_max == 0:
        return normal_max
    
    return max(normal_max, circular_max)
```

---

## 14. Topological Sort (Kahn's) Template

### Why This Matters

Topological sort orders vertices in a **Directed Acyclic Graph (DAG)** so that
every edge goes from earlier to later. It's essential for task scheduling,
dependency resolution, and cycle detection.

### When to Use

```
Problem keyword?  -->
  |
  +-- "order of tasks" / "prerequisites"    -->  Topological sort
  +-- "can finish all courses?"             -->  Topological sort (check for cycle)
  +-- "dependency resolution"               -->  Topological sort
  +-- "compile order" / "build order"       -->  Topological sort
  +-- undirected graph?                     -->  Use Union-Find (Template 5) instead
```

### Visual: Kahn's Algorithm (BFS-based)

```
  Graph (task dependencies):
  0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3, 3 -> 4

  Step 1: Compute indegrees:
  Node:    0   1   2   3   4
  Indeg:   0   1   1   2   1

  Step 2: Start BFS with indegree=0 nodes: [0]
  ┌──────┬───────┬──────────┬────────────────────────┐
  │ Step │ Queue │ Popped   │ Update indegrees       │
  ├──────┼───────┼──────────┼────────────────────────┤
  │  1   │ [0]   │ 0        │ 1->0, 2->0            │
  │  2   │ [1,2] │ 1        │ 3->1                  │
  │  3   │ [2,3] │ 2        │ 3->0                  │
  │  4   │ [3]   │ 3        │ 4->0                  │
  │  5   │ [4]   │ 4        │ done!                 │
  └──────┴───────┴──────────┴────────────────────────┘

  Result: [0, 1, 2, 3, 4] (valid topological order)

  CYCLE DETECTION: If result has fewer nodes than graph, cycle exists!
  (Some nodes never reach indegree=0 because of circular dependency)
```

### Complexity

- **Time:** O(V + E) — each node and edge processed once
- **Space:** O(V) — indegree array + queue + result

```python
from collections import deque

def topological_sort_kahn(n, edges):
    """Kahn's BFS-based topological sort.
    n: number of nodes (0 to n-1)
    edges: list of [u, v] meaning u -> v
    Returns: topological order, or [] if cycle exists
    """
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    
    queue = deque([i for i in range(n) if indegree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    return result if len(result) == n else []  # [] means cycle

def topological_sort_dfs(n, edges):
    """DFS-based topological sort."""
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
    
    visited = set()
    order = []
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        order.append(node)
    
    for i in range(n):
        if i not in visited:
            dfs(i)
    
    return order[::-1]

def course_schedule(n, prerequisites):
    """Can finish all courses? (Cycle detection via topological sort)"""
    return len(topological_sort_kahn(n, prerequisites)) == n
```

---

## 15. Fenwick Tree (Binary Indexed Tree) Template

### Why This Matters

Fenwick Tree does **prefix sums + point updates** in O(log n) — same as Segment
Tree but with **much simpler code** and smaller constant factor. If you only need
prefix sums (not arbitrary range queries), prefer this over Segment Tree.

### When to Use

```
Problem has?  -->
  |
  +-- Prefix sum queries + point updates          -->  Fenwick Tree (simplest!)
  +-- Range sum queries + point updates           -->  Fenwick Tree (with subtraction)
  +-- Range sum + range updates                   -->  Segment Tree (Fenwick can't do this)
  +-- Range min/max + updates                     -->  Segment Tree
  +-- 2D prefix sum + point updates               -->  FenwickTree2D
  +-- Just prefix sums, no updates?               -->  Simple prefix array O(1)
```

### Visual: How Fenwick Tree Uses Binary Indexing

```
  Index:    1    2    3    4    5    6    7    8
  Binary:  001  010  011  100  101  110  111  1000
                          ^
  The lowest set bit determines what range each node covers:

  Node 1 (001): covers [1]           (1 element)
  Node 2 (010): covers [1,2]         (2 elements)
  Node 3 (011): covers [3]           (1 element)
  Node 4 (100): covers [1,2,3,4]     (4 elements)
  Node 5 (101): covers [5]           (1 element)
  Node 6 (110): covers [5,6]         (2 elements)
  Node 7 (111): covers [7]           (1 element)
  Node 8 (1000):covers [1..8]        (8 elements)

  prefix_sum(7) = tree[7] + tree[6] + tree[4]
                  covers [7] + [5,6] + [1,2,3,4]
                  = all of [1..7] ✓

  Key operation: i & (-i) gives the lowest set bit!
    6 & (-6) = 110 & 010 = 010 = 2  (covers 2 elements)
```

### Complexity

- **Build:** O(n)
- **Update:** O(log n)
- **Query:** O(log n)
- **Space:** O(n)

```python
class FenwickTree:
    """Binary Indexed Tree for prefix sum queries and point updates.
    1-indexed internally.
    """
    
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, i, delta):
        """Add delta to element at index i (0-indexed)."""
        i += 1  # convert to 1-indexed
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)
    
    def query(self, i):
        """Prefix sum from index 0 to i (0-indexed)."""
        i += 1
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s
    
    def range_query(self, l, r):
        """Sum of elements from index l to r (0-indexed)."""
        return self.query(r) - (self.query(l - 1) if l > 0 else 0)

class FenwickTree2D:
    """2D Fenwick Tree for 2D prefix sum queries."""
    
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.tree = [[0] * (n + 1) for _ in range(m + 1)]
    
    def update(self, x, y, delta):
        x += 1
        y += 1
        while x <= self.m:
            j = y
            while j <= self.n:
                self.tree[x][j] += delta
                j += j & (-j)
            x += x & (-x)
    
    def query(self, x, y):
        x += 1
        y += 1
        s = 0
        while x > 0:
            j = y
            while j > 0:
                s += self.tree[x][j]
                j -= j & (-j)
            x -= x & (-x)
        return s
    
    def range_query(self, x1, y1, x2, y2):
        """Sum of rectangle from (x1,y1) to (x2,y2) inclusive."""
        return (self.query(x2, y2) 
                - self.query(x1 - 1, y2) 
                - self.query(x2, y1 - 1) 
                + self.query(x1 - 1, y1 - 1))
```

---

## 16. Disjoint Set Union (with Size + Rollback) Template

### Why This Matters

This is an **advanced DSU** with two extra features:
1. **Size tracking** — know how big each component is
2. **Rollback** — undo previous unions (for offline/parallel algorithms)

### When to Use

```
Problem has?  -->
  |
  +-- Basic connectivity?                     -->  DSU (Template 5)
  +-- Need component sizes?                   -->  UnionFindWithSize (Template 5)
  +-- Need to UNDO unions (rollback)?         -->  DSURollback (this template)
  +-- Offline connectivity + queries?          -->  DSURollback
  +-- Dynamic connectivity over time?         -->  DSURollback + divide & conquer
  +-- Kruskal's MST + need to check?          -->  DSU (Template 5)
```

### Visual: Rollback DSU

```
  Operations:
  union(0,1) -> union(1,2) -> rollback -> rollback

  History stack:
  ┌────┬──────────────────────────┐
  │ #  │ Changes made             │
  ├────┼──────────────────────────┤
  │  1 │ parent[1]=0, size[0]=2  │  union(0,1)
  │  2 │ parent[2]=0, size[0]=3  │  union(1,2)
  └────┴──────────────────────────┘

  After rollback #2: parent[2]=2, size[0]=2  (undo union(1,2))
  After rollback #1: parent[1]=1, size[0]=1  (undo union(0,1))
  Back to initial state!

  Note: NO path compression in rollback DSU (would break rollback).
  Only union by size/rank.
```

### Complexity

- **Time:** O(log n) per operation (no path compression, only union by size)
- **Space:** O(n + number of unions)

```python
class DSU:
    """DSU with union by size, path compression, and component count."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n
    
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.size[px] < self.size[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        self.components -= 1
        return True
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)

class DSURollback:
    """DSU with rollback capability (for offline queries)."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n
        self.history = []  # stack of changes for rollback
    
    def find(self, x):
        while self.parent[x] != x:
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.size[px] < self.size[py]:
            px, py = py, px
        self.history.append((py, self.parent[py], px, self.size[px], self.components))
        self.parent[py] = px
        self.size[px] += self.size[py]
        self.components -= 1
        return True
    
    def rollback(self):
        if not self.history:
            return
        py, old_parent, px, old_size, old_components = self.history.pop()
        self.parent[py] = old_parent
        self.size[px] = old_size
        self.components = old_components
```

---

## 17. LCA (Binary Lifting) Template

### Why This Matters

Lowest Common Ancestor (LCA) of two nodes u and v is the deepest node that is
an ancestor of both. Binary Lifting preprocesses the tree so each LCA query
answers in **O(log n)**.

### When to Use

```
Problem keyword?  -->
  |
  +-- "distance between two nodes in tree"    -->  LCA (distance = depth[u]+depth[v]-2*depth[lca])
  +-- "lowest common ancestor"                -->  LCA
  +-- "path between two nodes"                -->  LCA + path reconstruction
  +-- "k-th ancestor of node"                 -->  Binary lifting (same preprocessing)
  +-- just parent queries?                    -->  Simple DFS is enough
```

### Visual: Binary Lifting Concept

```
  Tree:
         0
        / \
       1   2
      / \   \
     3   4   5
    /       / \
   6       7   8

  parent[node][j] = 2^j-th ancestor of node

  j=0 (2^0=1st ancestor):     j=1 (2^1=2nd ancestor):
  parent[0][0] = -1            parent[0][1] = -1
  parent[1][0] = 0             parent[1][1] = -1
  parent[2][0] = 0             parent[2][1] = -1
  parent[3][0] = 1             parent[3][1] = 0    (1's parent)
  parent[4][0] = 1             parent[4][1] = 0
  parent[5][0] = 2             parent[5][1] = 0
  parent[6][0] = 3             parent[6][1] = 1    (3's parent)
  parent[7][0] = 5             parent[7][1] = 2    (5's parent)
  parent[8][0] = 5             parent[8][1] = 2

  To find LCA(6, 8):
  Step 1: Equalize depths. depth[6]=3, depth[8]=3 -> same depth.
  Step 2: Check if ancestors are different going up in powers of 2:
          j=1: parent[6][1]=1, parent[8][1]=2 -> different, move both up
          j=0: parent[6][0]=3, parent[8][0]=5 -> different, move both up
          Now parent[6][0]=1, parent[8][0]=2 -> different, move up
          ... eventually they meet at node 0.
          LCA(6, 8) = 0 ✓
```

### Complexity

- **Preprocessing:** O(n log n)
- **Query:** O(log n)
- **Space:** O(n log n)

```python
import sys
sys.setrecursionlimit(10**6)

class LCA:
    """Lowest Common Ancestor using binary lifting.
    Preprocess: O(n log n), Query: O(log n)
    """
    
    def __init__(self, n, root, graph):
        self.n = n
        self.LOG = 20  # enough for n <= 10^6
        self.depth = [0] * n
        self.parent = [[-1] * self.LOG for _ in range(n)]
        self.graph = graph
        
        self._dfs(root, -1, 0)
        self._preprocess()
    
    def _dfs(self, node, par, d):
        self.depth[node] = d
        self.parent[node][0] = par
        for neighbor in self.graph[node]:
            if neighbor != par:
                self._dfs(neighbor, node, d + 1)
    
    def _preprocess(self):
        for j in range(1, self.LOG):
            for i in range(self.n):
                if self.parent[i][j - 1] != -1:
                    self.parent[i][j] = self.parent[self.parent[i][j - 1]][j - 1]
    
    def lca(self, u, v):
        """Find LCA of u and v."""
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        
        # Lift u to same depth as v
        diff = self.depth[u] - self.depth[v]
        for j in range(self.LOG):
            if diff & (1 << j):
                u = self.parent[u][j]
        
        if u == v:
            return u
        
        # Binary lift both
        for j in range(self.LOG - 1, -1, -1):
            if self.parent[u][j] != self.parent[v][j]:
                u = self.parent[u][j]
                v = self.parent[v][j]
        
        return self.parent[u][0]
    
    def distance(self, u, v):
        """Distance between u and v."""
        w = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[w]

# Usage:
# graph = {0: [1, 2], 1: [0, 3, 4], 2: [0], 3: [1], 4: [1]}
# lca = LCA(5, 0, graph)
# print(lca.lca(3, 4))  # 1
```

---

## 18. KMP Algorithm Template

### Why This Matters

Naive string matching is O(n×m). KMP achieves **O(n+m)** by using the LPS
(Longest Proper Prefix which is also Suffix) array to avoid redundant comparisons.

### When to Use

```
Problem keyword?  -->
  |
  +-- "find pattern in text"                  -->  KMP or Rabin-Karp
  +-- "all occurrences of pattern"            -->  KMP
  +-- "string contains substring"             -->  KMP
  +-- "periodic string" / "repeated pattern"  -->  KMP (LPS array gives period)
  +-- multiple patterns to search?            -->  Aho-Corasick (advanced)
  +-- just need existence?                    -->  Python 'in' operator is fine
```

### Visual: How LPS Array Works

```
  Pattern: "ABABCABAB"

  LPS[i] = length of longest proper prefix of pattern[0..i]
           that is also a suffix of pattern[0..i]

  Index:  0   1   2   3   4   5   6   7   8
  Char:   A   B   A   B   C   A   B   A   B
  LPS:    0   0   1   2   0   1   2   3   4

  LPS[8] = 4 because:
  "ABABCABAB"
   ^^^^   ^^^^
   prefix "ABAB" == suffix "ABAB"

  Why does this help? When mismatch at position j:
  Instead of restarting from pattern[0], jump to LPS[j-1].
  We know the suffix already matches the prefix!
```

### Visual: KMP Search

```
  Text:    "ABABDABACDABABCABAB"
  Pattern: "ABABCABAB"

  i=0:  ABABDABACDABABCABAB     Match ABAB, mismatch at D/C
        ABABCABAB
        ^^^^
        LPS says: skip first 2 chars, try from "AB..."

  i=2:  ABABDABACDABABCABAB     Match ABABC...
        ..ABABCABAB
            ^

  (continues until full match at position 9)

  Key: The text pointer i NEVER goes backward!
  This is what makes KMP O(n+m).
```

### Complexity

- **Build LPS:** O(m)
- **Search:** O(n)
- **Total:** O(n + m)
- **Space:** O(m) for LPS array

```python
def kmp_build_lps(pattern):
    """Build the Longest Proper Prefix which is also Suffix array.
    lps[i] = length of longest proper prefix of pattern[0..i]
             which is also a suffix of pattern[0..i]
    """
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps

def kmp_search(text, pattern):
    """KMP string matching. Returns list of all starting indices where
    pattern is found in text. Time: O(n + m)
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return []
    
    lps = kmp_build_lps(pattern)
    result = []
    i = j = 0  # i for text, j for pattern
    
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        
        if j == m:
            result.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return result

# Example
text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
print(kmp_search(text, pattern))  # [9]
```

---

## 19. Rabin-Karp Algorithm Template

### Why This Matters

Rabin-Karp uses **rolling hash** to compare strings in O(1) instead of O(m).
This makes it great for searching **multiple patterns simultaneously** or for
problems requiring hash-based string comparison.

### When to Use

```
Problem keyword?  -->
  |
  +-- "find pattern in text"              -->  Rabin-Karp or KMP
  +-- "count distinct substrings"         -->  Rabin-Karp (with HashSet)
  +-- "longest repeated substring"        -->  Rabin-Karp + binary search
  +-- "anagram substrings"                -->  Rabin-Karp with hash
  +-- "find all rotations"                -->  Rabin-Karp
  +-- need guaranteed O(n+m)?             -->  Use KMP instead (no hash collisions)
```

### Visual: Rolling Hash Concept

```
  Text:    "ABABDABAC"
  Pattern: "ABAB"  (m=4)

  base = 256, mod = 10^9+7

  hash("ABAB") = A*256^3 + B*256^2 + A*256^1 + B*256^0

  Rolling hash: slide window by 1 character:

  hash("ABAB") = h1
  hash("BABA") = (h1 - A*256^3) * 256 + A    <-- remove leading, add trailing
                = (h1 - A*256^3) * 256 + new_char

  This is O(1) per shift! Instead of recomputing entire hash.

  ┌───┬───┬───┬───┐
  │ A │ B │ A │ B │ D │ A │ B │ A │ C │
  └───┴───┴───┴───┘
    h1 (hash of "ABAB")
         └───┴───┴───┬───┘
           h2 = rolling(h1, remove 'A', add 'D')
```

### Visual: Collision Handling

```
  Problem: Two different strings could have the same hash!

  Solution: When hash matches, ALWAYS verify character by character.

  hash(text[i:i+m]) == hash(pattern)?
    |
    +-- NO   ->  definitely not a match, skip
    +-- YES  ->  verify: text[i:i+m] == pattern?
                   |
                   +-- YES ->  confirmed match!
                   +-- NO  ->  hash collision, skip (rare)
```

### Complexity

- **Average case:** O(n + m)
- **Worst case:** O(n × m) with hash collisions (rare with good mod)
- **Space:** O(1)

```python
def rabin_karp(text, pattern):
    """Rabin-Karp string matching using rolling hash.
    Returns list of starting indices where pattern is found in text.
    Time: O(n + m) average, O(n*m) worst case (with hash verification)
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    base = 256
    mod = 10**9 + 7
    
    # Precompute base^(m-1) % mod
    base_pow = pow(base, m - 1, mod)
    
    # Compute hash of pattern and first window of text
    pattern_hash = 0
    text_hash = 0
    
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        text_hash = (text_hash * base + ord(text[i])) % mod
    
    result = []
    
    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            # Verify character by character (to avoid hash collision)
            if text[i:i + m] == pattern:
                result.append(i)
        
        # Rolling hash: remove leading char, add trailing char
        if i < n - m:
            text_hash = (text_hash - ord(text[i]) * base_pow) % mod
            text_hash = (text_hash * base + ord(text[i + m])) % mod
            text_hash %= mod  # ensure non-negative
    
    return result

# Example
text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
print(rabin_karp(text, pattern))  # [9]
```

---

## 20. Fast Exponentiation + Combinatorics Template

### Why This Matters

Matrix exponentiation computes **linear recurrences** (like Fibonacci) in
**O(k^3 log n)** where k is the matrix size. This turns O(n) DP into O(log n).

### When to Use

```
Problem has linear recurrence?  -->
  |
  +-- Fibonacci: F(n) = F(n-1) + F(n-2)           -->  2x2 matrix
  +-- Any F(n) = a*F(n-1) + b*F(n-2) + c          -->  3x3 matrix
  +-- System of linear equations evolving in steps  -->  Matrix exponentiation
  +-- "nth term of recurrence in O(log n)"         -->  Matrix exponentiation
  +-- just Fibonacci?                               -->  Could also use fast doubling
```

### Visual: Matrix Exponentiation for Fibonacci

```
  Fibonacci: F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)

  Can be written as matrix multiplication:

  [F(n+1)]   [1  1]^n   [F(1)]   [1  1]^n   [1]
  [F(n)  ] = [1  0]   * [F(0)] = [1  0]   * [0]

  So: compute [1 1; 1 0]^n using binary exponentiation!

  [1 1]^n
  [1 0]

  n=5 (binary: 101):

  Start: result = I = [1 0; 0 1]

  bit=1 (odd):  result = I * M = [1 1; 1 0]
  square:       M = M^2 = [2 1; 1 1]
  bit=0 (even): result unchanged
  square:       M = M^4 = [5 3; 3 2]
  bit=1 (odd):  result = [1 1; 1 0] * [5 3; 3 2] = [8 5; 5 3]

  F(5) = result[0][1] = 5 ✓
```

### Visual: Binary Exponentiation of Matrix

```
  Compute M^13 (13 = 1101 in binary):

  ┌──────┬──────────┬────────────────────────┐
  │ Step │ exp bit  │ Action                 │
  ├──────┼──────────┼────────────────────────┤
  │ init │ 1101     │ result = I            │
  │  1   │    1     │ result *= M^1         │
  │  2   │   10     │ M squared -> M^2      │
  │  3   │  100     │ result unchanged      │
  │      │          │ M squared -> M^4      │
  │  4   │ 1000     │ result *= M^4         │
  │      │          │ M squared -> M^8      │
  └──────┴──────────┴────────────────────────┘
  result = M^1 * M^4 * M^8 = M^13  ✓
```

### Complexity

- **Matrix multiplication:** O(k^3) where k = matrix dimension
- **Matrix exponentiation:** O(k^3 × log n)
- **Space:** O(k^2)

```python
MOD = 10**9 + 7

# Matrix exponentiation for linear recurrences
def mat_mult(A, B, mod=MOD):
    """Multiply two matrices A and B."""
    n = len(A)
    m = len(B[0])
    k = len(B)
    C = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for l in range(k):
                C[i][j] = (C[i][j] + A[i][l] * B[l][j]) % mod
    return C

def mat_pow(matrix, power, mod=MOD):
    """Matrix exponentiation. Raises matrix to given power."""
    n = len(matrix)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    while power > 0:
        if power % 2 == 1:
            result = mat_mult(result, matrix, mod)
        matrix = mat_mult(matrix, matrix, mod)
        power //= 2
    
    return result

def fibonacci_matrix(n):
    """Find nth Fibonacci number using matrix exponentiation.
    F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)
    [1 1]^n   [F(n+1) F(n)  ]
    [1 1]   = [F(n)   F(n-1)]
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    base = [[1, 1], [1, 0]]
    result = mat_pow(base, n)
    return result[0][1]

# Example
for i in range(10):
    print(f"F({i}) = {fibonacci_matrix(i)}")
# F(0)=0, F(1)=1, F(2)=1, F(3)=2, F(4)=3, F(5)=5, ...
```

---

## Template Quick Reference (Detailed)

### Problem Type -> Template Mapping

```
  GRAPH PROBLEMS
  ┌─────────────────────────────────────┬──────────────────────────┐
  │ Problem Type                        │ Template to Use          │
  ├─────────────────────────────────────┼──────────────────────────┤
  │ Shortest path (unweighted)          │ #2 BFS                   │
  │ Shortest path (weighted, no neg)    │ #4 Dijkstra              │
  │ Detect cycle in undirected graph    │ #5 Union-Find            │
  │ Connected components                │ #3 DFS or #5 Union-Find  │
  │ Topological ordering                │ #14 TopoSort             │
  │ Task scheduling / prerequisites     │ #14 TopoSort             │
  │ MST (Kruskal's)                     │ #5 Union-Find            │
  │ LCA / tree distance                 │ #17 LCA                  │
  │ All paths in graph                  │ #3 DFS + #9 Backtracking │
  └─────────────────────────────────────┴──────────────────────────┘

  ARRAY / STRING PROBLEMS
  ┌─────────────────────────────────────┬──────────────────────────┐
  │ Problem Type                        │ Template to Use          │
  ├─────────────────────────────────────┼──────────────────────────┤
  │ Maximum subarray sum                │ #13 Kadane's             │
  │ Next greater/smaller element        │ #8 Monotonic Stack       │
  │ Range sum + point updates           │ #15 Fenwick or #6 SegTree│
  │ Range min/max + updates             │ #6 Segment Tree          │
  │ Subarray with condition             │ #12 Sliding Window       │
  │ Find pattern in string              │ #18 KMP or #19 RabinKarp │
  │ Prefix matching                     │ #7 Trie                  │
  │ Largest rectangle in histogram      │ #8 Monotonic Stack       │
  │ Trapping rain water                 │ #8 Monotonic Stack       │
  └─────────────────────────────────────┴──────────────────────────┘

  MATH / NUMBER THEORY
  ┌─────────────────────────────────────┬──────────────────────────┐
  │ Problem Type                        │ Template to Use          │
  ├─────────────────────────────────────┼──────────────────────────┤
  │ nCr or nPr mod 10^9+7               │ #10 Modular Arithmetic   │
  │ Fast power (a^b mod p)              │ #10 Modular Arithmetic   │
  │ Fibonacci (large n)                 │ #20 Matrix Exponentiation│
  │ General linear recurrence           │ #20 Matrix Exponentiation│
  └─────────────────────────────────────┴──────────────────────────┘

  OPTIMIZATION
  ┌─────────────────────────────────────┬──────────────────────────┐
  │ Problem Type                        │ Template to Use          │
  ├─────────────────────────────────────┼──────────────────────────┤
  │ Minimize the maximum value          │ #11 Binary Search Answer │
  │ Maximize the minimum value          │ #11 Binary Search Answer │
  │ All permutations/combinations       │ #9 Backtracking          │
  │ N-Queens / Sudoku / constraint      │ #9 Backtracking          │
  └─────────────────────────────────────┴──────────────────────────┘
```

### Complete Quick Reference Table

| #  | Template              | Time           | Space  | When to Use                                  |
|----|-----------------------|----------------|--------|----------------------------------------------|
| 1  | Fast I/O              | -              | -      | **Always** in CP                             |
| 2  | BFS                   | O(V + E)       | O(V)   | Shortest path unweighted grid/graph          |
| 3  | DFS                   | O(V + E)       | O(V)   | Components, cycles, reachability             |
| 4  | Dijkstra              | O((V+E) log V) | O(V)   | Shortest path weighted graph                 |
| 5  | Union-Find            | O(alpha(n))    | O(n)   | Dynamic connectivity, merge sets             |
| 6  | Segment Tree          | O(n log n)     | O(n)   | Range query + point update                   |
| 7  | Trie                  | O(L)           | O(N*L) | Prefix matching, autocomplete                |
| 8  | Monotonic Stack       | O(n)           | O(n)   | Next greater/smaller, histogram              |
| 9  | Backtracking          | O(2^n) / n!    | O(n)   | Generate all combos/permutations             |
| 10 | Modular Arithmetic    | O(log n)       | O(n)   | nCr, power, inverse mod MOD                  |
| 11 | Binary Search Answer  | O(log R * f()) | O(1)   | Minimize max / maximize min                  |
| 12 | Sliding Window        | O(n)           | O(k)   | Contiguous subarray/substring                |
| 13 | Kadane's              | O(n)           | O(1)   | Maximum subarray sum                         |
| 14 | Topological Sort      | O(V + E)       | O(V)   | Task ordering, detect cycle in DAG           |
| 15 | Fenwick Tree          | O(n log n)     | O(n)   | Prefix sum + point update (simpler than ST)  |
| 16 | DSU + Rollback        | O(n alpha(n))  | O(n)   | Offline connectivity queries                 |
| 17 | LCA (Binary Lifting)  | O(n log n)     | O(n log n) | Distance between tree nodes              |
| 18 | KMP                   | O(n + m)       | O(m)   | Exact pattern matching                       |
| 19 | Rabin-Karp            | O(n + m) avg   | O(1)   | Multiple pattern matching, rolling hash      |
| 20 | Matrix Exponentiation | O(k^3 log n)   | O(k^2) | Fast Fibonacci, linear recurrences           |

**Legend:** V = vertices, E = edges, n = input size, L = string length, k = matrix size, R = binary search range, alpha = inverse Ackermann (nearly 1)

### Exam Day Checklist

```
  Before coding:
  □  Add Fast I/O template (Template 1) — always
  □  Check if answer needs MOD 10^9+7 -> use Template 10 helpers
  □  Identify the problem type -> jump to matching template
  □  Copy template, rename functions, adapt to problem
  □  Test with given examples before submitting

  Common pitfalls:
  ⚠  Forgetting to use sys.setrecursionlimit(10**6) for DFS
  ⚠  Off-by-one in segment tree / fenwick tree (0-indexed vs 1-indexed)
  ⚠  Using BFS for weighted graphs (use Dijkstra instead)
  ⚠  Not handling edge cases (n=0, n=1, negative numbers)
  ⚠  Integer overflow in C++ — not an issue in Python, but watch for TLE
```
