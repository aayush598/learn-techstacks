# Union-Find & MST Complete Guide

## Union-Find (Disjoint Set Union)

### Visual: How Union-Find Works

```
Union-Find tracks which "group" (component) each node belongs to.
Two operations:
  FIND(x) → Which group is x in? (find the root/representative)
  UNION(x, y) → Merge the groups containing x and y

INITIAL STATE: Each node is its own group
  Parent: [0, 1, 2, 3, 4]  (parent[i] = i means i is a root)
  Visual:
    0    1    2    3    4    (5 separate components)

UNION(0, 1): Merge groups of 0 and 1
  Parent: [0, 0, 2, 3, 4]
  Visual:
    0    2    3    4
    |              (4 components: {0,1}, {2}, {3}, {4})
    1

UNION(2, 3): Merge groups of 2 and 3
  Parent: [0, 0, 2, 2, 4]
  Visual:
    0    2    4
    |    |         (3 components: {0,1}, {2,3}, {4})
    1    3

UNION(1, 3): Merge groups of 1 and 3
  Parent: [0, 0, 0, 2, 4]  ← find(1)=0, find(3)=2, set parent[2]=0
  Visual:
    0         4
    |              (2 components: {0,1,2,3}, {4})
    1
    |
    2
    |
    3

FIND(3): Follow parent chain to root
  parent[3]=2 → parent[2]=0 → parent[0]=0 (root!)
  Returns 0

FIND(4): Follow parent chain
  parent[4]=4 (root!)
  Returns 4

Result: find(0) == find(3) → True (same component!)
        find(0) == find(4) → False (different components!)
```

### Path Compression — Making Find Fast

```
WITHOUT path compression:
  find(5): 5→4→3→2→1→0  (6 steps!)

WITH path compression:
  find(5): 5→4→3→2→1→0, then SET all to point directly to 0
  After:   5→0, 4→0, 3→0, 2→0, 1→0
  Next find(5): 5→0  (1 step!)

Path compression in code:
  def find(x):
      if parent[x] != x:
          parent[x] = find(parent[x])  ← THIS LINE compresses!
      return parent[x]

  Before:        After path compression:
  0              0
  |             /|\ \
  1            1 2 3 4 5
  |
  2
  |
  3
  |
  4
  |
  5
```

```python
class UnionFind:
    """
    Union-Find with path compression and union by rank
    Time: O(α(n)) per operation ≈ O(1) amortized
    Space: O(n)

    α(n) is the inverse Ackermann function — it's effectively
    constant for all practical values of n (< 10^800).
    """
    def __init__(self, n):
        self.parent = list(range(n))  # Each node is its own parent
        self.rank = [0] * n           # Tree depth (for union by rank)
        self.count = n  # Number of connected components

    def find(self, x):
        """Find root with PATH COMPRESSION"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Compress!
        return self.parent[x]

    def union(self, x, y):
        """
        Union by RANK. Attaches shorter tree under taller tree.
        Returns True if merged, False if already same set.
        """
        px, py = self.find(x), self.find(y)

        if px == py:
            return False  # Already in same set (would create cycle!)

        # Attach shorter tree under taller tree
        if self.rank[px] < self.rank[py]:
            px, py = py, px   # Ensure px is the taller one
        self.parent[py] = px

        # Only increase rank if trees were same height
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

        self.count -= 1
        return True

    def connected(self, x, y):
        """Check if x and y are in same set"""
        return self.find(x) == self.find(y)

    def components(self):
        """Return number of connected components"""
        return self.count


# Simple Union-Find (without rank, simpler to remember)
class UnionFindSimple:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            self.parent[px] = py
            return True
        return False

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

## Find Connected Components

```python
def count_components(n, edges):
    """
    Count connected components using Union-Find
    Time: O(V + E * α(V)) | Space: O(V)
    """
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.components()


# List all components
def find_components(n, edges):
    """Return list of components"""
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    
    from collections import defaultdict
    components = defaultdict(list)
    for i in range(n):
        components[uf.find(i)].append(i)
    
    return list(components.values())


# Example
edges = [[0, 1], [2, 3], [4, 5]]
print(count_components(6, edges))  # 3
print(find_components(6, edges))  # [[0, 1], [2, 3], [4, 5]]
```

## Number of Provinces

```python
def find_circle_num(isConnected):
    """
    LeetCode 547 - Count connected components in adjacency matrix
    Time: O(n²) | Space: O(n)
    """
    n = len(isConnected)
    uf = UnionFind(n)
    
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                uf.union(i, j)
    
    return uf.components()


# DFS approach
def find_circle_num_dfs(isConnected):
    n = len(isConnected)
    visited = set()
    count = 0
    
    def dfs(node):
        visited.add(node)
        for neighbor in range(n):
            if isConnected[node][neighbor] == 1 and neighbor not in visited:
                dfs(neighbor)
    
    for i in range(n):
        if i not in visited:
            dfs(i)
            count += 1
    
    return count


# Example
isConnected = [[1,1,0],[1,1,0],[0,0,1]]
print(find_circle_num(isConnected))  # 2
```

## Redundant Connection

```python
def find_redundant_connection(edges):
    """
    LeetCode 684 - Find edge that creates cycle
    Time: O(E * α(V)) | Space: O(V)
    """
    n = len(edges)
    uf = UnionFind(n)
    
    for u, v in edges:
        if not uf.union(u - 1, v - 1):
            return [u, v]
    
    return []


# Example
edges = [[1,2],[1,3],[2,3]]
print(find_redundant_connection(edges))  # [2, 3]


def find_redundant_connection_directed(edges):
    """
    LeetCode 685 - Redundant connection II (directed)
    """
    n = len(edges)
    parent = list(range(n + 1))
    rank = [0] * (n + 1)
    indegree = [0] * (n + 1)
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True
    
    # Check for two types of redundancy
    for u, v in edges:
        indegree[v] += 1
    
    # Case 1: Node has two parents
    candidates = []
    for i in range(n):
        if indegree[edges[i][1]] == 2:
            candidates.append(i)
    
    if candidates:
        # Try removing second candidate first
        for i in reversed(candidates):
            temp_edges = edges[:i] + edges[i+1:]
            uf = UnionFind(n + 1)
            valid = True
            for u, v in temp_edges:
                if not uf.union(u, v):
                    valid = False
                    break
            if valid:
                return edges[i]
    
    # Case 2: Cycle without two-parent issue
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]
    
    return []
```

## Accounts Merge

```python
def accounts_merge(accounts):
    """
    LeetCode 721 - Merge accounts with common emails
    Time: O(N * K * α(N*K)) | Space: O(N * K)
    """
    from collections import defaultdict
    
    email_to_id = {}
    email_to_name = {}
    id_counter = 0
    
    # Assign unique ID to each email
    for account in accounts:
        name = account[0]
        for email in account[1:]:
            email_to_name[email] = name
            if email not in email_to_id:
                email_to_id[email] = id_counter
                id_counter += 1
    
    # Union emails in same account
    uf = UnionFind(id_counter)
    for account in accounts:
        first_email = account[1]
        for email in account[2:]:
            uf.union(email_to_id[first_email], email_to_id[email])
    
    # Group emails by root
    groups = defaultdict(list)
    for email, eid in email_to_id.items():
        root = uf.find(eid)
        groups[root].append(email)
    
    # Build result
    result = []
    for root, emails in groups.items():
        name = email_to_name[emails[0]]
        result.append([name] + sorted(emails))
    
    return result


# Example
accounts = [
    ["John", "johnsmith@mail.com", "john00@mail.com"],
    ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
    ["Mary", "mary@mail.com"],
    ["John", "johnnybravo@mail.com"]
]
print(accounts_merge(accounts))
# [["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
#  ["Mary", "mary@mail.com"],
#  ["John", "johnnybravo@mail.com"]]
```

## Minimum Spanning Tree: Kruskal's Algorithm

### Visual: Kruskal's Step-by-Step

```
Kruskal's = Greedy: Sort edges by weight, add if no cycle.

Graph:                    Sorted edges:
  0 --4-- 1               1. (0,2) weight 1
  |  \ /  |               2. (2,3) weight 1
  1   2   3               3. (1,2) weight 2
  |   |   |               4. (1,3) weight 3
  v   v   v               5. (0,1) weight 4
  2   3   1               6. (0,3) weight 5
      |
      1

Step │ Edge    │ Weight │ Action          │ MST so far     │ Total
─────│─────────│────────│─────────────────│────────────────│──────
  1  │ (0,2)   │   1    │ Add (no cycle)  │ {(0,2)}        │  1
  2  │ (2,3)   │   1    │ Add (no cycle)  │ {(0,2),(2,3)}  │  2
  3  │ (1,2)   │   2    │ Add (no cycle)  │ {(0,2),(2,3),  │  4
     │         │        │                 │  (1,2)}        │
  4  │ (1,3)   │   3    │ SKIP! Creates   │ (already have  │  4
     │         │        │ cycle 1-2-3-1   │  path 1→2→3)   │
  5  │ (0,1)   │   4    │ SKIP! Creates   │ (already have  │  4
     │         │        │ cycle 0-2-1-0   │  path 0→2→1)   │
  6  │ (0,3)   │   5    │ SKIP! Creates   │ (already have  │  4
     │         │        │ cycle 0-2-3-0   │  path 0→2→3)   │
  DONE: MST has 3 edges (V-1), total weight = 4

Final MST:
  0 --1-- 2 --1-- 3
         |
         1
         |
         1 (wait, that's wrong)
  Let me draw it correctly:
  0 --1-- 2 --1-- 3
         |
         1
         |
  (This is a tree: 3 edges for 4 nodes)

  Wait, (1,2) connects 1 to 2 with weight 2:
  0 --1-- 2 --2-- 1
         |
         1
         |
         3
  
  Actually: edges are (0,2,1), (2,3,1), (1,2,2)
  0 --1-- 2 --2-- 1
         |
         1
         |
         3
  
  MST weight = 1 + 1 + 2 = 4 ✓
```

```python
def kruskal_mst(n, edges):
    """
    Kruskal's MST - Greedy approach using Union-Find
    Time: O(E log E) for sorting + O(E × α(V)) for unions = O(E log E)
    Space: O(V)

    ALGORITHM:
    1. Sort all edges by weight (ascending)
    2. For each edge (in sorted order):
       - If it doesn't create a cycle → add to MST
       - If it creates a cycle → skip it
    3. Stop when MST has V-1 edges

    WHY IT WORKS:
    Kruskal's is greedy — always pick the cheapest available edge.
    If adding an edge creates a cycle, we skip it because all nodes
    in the cycle are already connected (we can reach them cheaper).
    """
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])

    uf = UnionFind(n)
    mst = []
    total_weight = 0

    for u, v, w in edges:
        if uf.union(u, v):    # True = no cycle, edge added
            mst.append((u, v, w))
            total_weight += w

            # MST has exactly V-1 edges
            if len(mst) == n - 1:
                break

    return mst, total_weight


# Example
edges = [
    (0, 1, 4), (0, 2, 1), (0, 3, 5),
    (1, 2, 2), (1, 3, 3), (2, 3, 1)
]

mst, total = kruskal_mst(4, edges)
print(mst)    # [(0, 2, 1), (2, 3, 1), (1, 2, 2)]
print(total)  # 4
```

## Minimum Spanning Tree: Prim's Algorithm

### Visual: Prim's Step-by-Step

```
Prim's = Grow from one node: Always add the cheapest edge
that connects a visited node to an unvisited node.

Graph:
  0 --4-- 1
  |  \ /  |
  1   2   3
  |   |   |
  v   v   v
  2   3   1
      |
      1

Starting from node 0:

Step │ Visited       │ Heap (candidates)     │ Pop    │ MST
─────│───────────────│───────────────────────│────────│──────────
  1  │ {0}           │ (1,0→2), (4,0→1),     │ (1,0→2)│ {(0,2)}
     │               │ (5,0→3)               │        │
  2  │ {0, 2}        │ (4,0→1), (5,0→3),     │ (1,2→3)│ {(0,2),
     │               │ (1,2→3), (2,2→1)      │        │ (2,3)}
  3  │ {0, 2, 3}     │ (4,0→1), (2,2→1),     │ (2,2→1)│ {(0,2),
     │               │ (3,3→1)               │        │ (2,3),(2,1)}
  4  │ {0,1,2,3}     │ (4,0→1) — skip, 1     │ done!  │ MST done
     │               │ already visited        │        │
  DONE: MST has 3 edges, total = 1+1+2 = 4

PRIM'S vs KRUSKAL'S:
  Kruskal's: Picks globally cheapest edge (may not connect to tree yet)
  Prim's: Picks cheapest edge FROM the current tree (always connected)

Both give the SAME total weight, but may pick different edges!
```

```python
import heapq
from collections import defaultdict

def prim_mst(n, edges):
    """
    Prim's MST - Start from any node, greedily add cheapest edge
    Time: O(E log V) | Space: O(V + E)

    ALGORITHM:
    1. Start from node 0 (or any node)
    2. Add all edges from visited → unvisited to min-heap
    3. Pop cheapest edge; if destination is unvisited, add it
    4. Repeat until V-1 edges added

    BEST FOR: Dense graphs (fewer nodes, many edges)
    """
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    visited = set([0])
    mst = []
    total_weight = 0

    # Min heap: (weight, from_node, to_node)
    heap = [(w, 0, v) for v, w in graph[0]]
    heapq.heapify(heap)

    while heap and len(mst) < n - 1:
        w, u, v = heapq.heappop(heap)

        if v in visited:
            continue   # Skip — we already reached this node

        visited.add(v)
        mst.append((u, v, w))
        total_weight += w

        # Add edges from newly visited node to unvisited neighbors
        for neighbor, weight in graph[v]:
            if neighbor not in visited:
                heapq.heappush(heap, (weight, v, neighbor))

    return mst, total_weight


# Example
edges = [
    (0, 1, 4), (0, 2, 1), (0, 3, 5),
    (1, 2, 2), (1, 3, 3), (2, 3, 1)
]

mst, total = prim_mst(4, edges)
print(mst)    # [(0, 2, 1), (2, 1, 2), (2, 3, 1)] or similar
print(total)  # 4


# Prim's starting from specific node
def prim_mst_from_node(n, edges, start):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    visited = set([start])
    mst = []
    total_weight = 0

    heap = [(w, start, v) for v, w in graph[start]]
    heapq.heapify(heap)

    while heap and len(mst) < n - 1:
        w, u, v = heapq.heappop(heap)

        if v in visited:
            continue

        visited.add(v)
        mst.append((u, v, w))
        total_weight += w

        for neighbor, weight in graph[v]:
            if neighbor not in visited:
                heapq.heappush(heap, (weight, v, neighbor))

    return mst, total_weight
```

## Kruskal vs Prim Comparison

```
| Feature           | Kruskal's                | Prim's                    |
|-------------------|--------------------------|---------------------------|
| Approach          | Edge-based (greedy)      | Vertex-based (greedy)     |
| Data Structure    | Union-Find               | Min Heap                  |
| Time              | O(E log E)               | O(E log V)                |
| Space             | O(V)                     | O(V + E)                  |
| Best For          | Sparse graphs            | Dense graphs              |
| Edge List         | Yes (natural input)      | Needs adjacency list      |
| Adjacency List    | Yes                      | Yes                       |

DECISION GUIDE:
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  Sparse graph (E << V²)?                                 │
│  └── YES → Kruskal's (simpler, uses edge list)          │
│                                                          │
│  Dense graph (E ≈ V²)?                                   │
│  └── YES → Prim's (fewer heap operations)               │
│                                                          │
│  Already have edge list?                                 │
│  └── YES → Kruskal's (no need to build graph)           │
│                                                          │
│  Need MST from specific node?                            │
│  └── YES → Prim's (natural starting point)              │
│                                                          │
│  Need to detect if graph is connected?                   │
│  └── EITHER: If MST has V-1 edges, it's connected       │
│                                                          │
└──────────────────────────────────────────────────────────┘

WHY BOTH WORK:
  Both are greedy algorithms that exploit the "cut property":
  For any cut of the graph, the minimum weight edge crossing
  the cut MUST be in some MST.
  Kruskal's: Considers edges globally (cheapest first)
  Prim's: Considers edges locally (from current tree)
```

## Key Takeaways

```
UNION-FIND:
1. Path compression + union by rank → O(α(n)) ≈ O(1) per operation
2. Use for: connected components, cycle detection, grouping
3. Pattern: Create UF, union edges, check find(x) == find(y)

CRITICAL: Without path compression, find() can be O(n) in worst case!
  With path compression, the tree stays flat → O(1) amortized.

  No compression:         With compression:
  0                       0
  |                      /|\ \
  1                     1 2 3 4
  |
  2
  |
  3
  |     find(4)=O(4)      find(4)=O(1)
  4

KRUSKAL'S MST:
1. Sort edges by weight (O(E log E))
2. Add edges if they don't create cycle (Union-Find checks)
3. Stop when V-1 edges added
4. Best for sparse graphs

PRIM'S MST:
1. Start from any node
2. Greedily add cheapest edge to unvisited node (min-heap)
3. Use min heap for efficiency
4. Best for dense graphs

WHEN TO USE:
- Connected components → Union-Find (O(E × α(V)))
- Cycle detection (undirected) → Union-Find
- MST → Kruskal's (sparse) or Prim's (dense)
- Group merging → Union-Find
- Accounts merge → Union-Find
- Redundant connection → Union-Find

COMMON MISTAKES:
┌──────────────────────────────────────────────────────────┐
│ ✗ Forgetting path compression (find becomes O(n))        │
│ ✗ Union by rank: forgetting to update rank when equal    │
│ ✗ Kruskal's: forgetting to sort edges first!             │
│ ✗ Prim's: not checking if destination already visited    │
│ ✗ Prim's: using wrong heap format (must be (w, u, v))   │
│ ✗ Confusing union(x,y) return value:                     │
│   → Returns False when already same set (CYCLE!)         │
│   → Returns True when merged successfully                │
└──────────────────────────────────────────────────────────┘
```
