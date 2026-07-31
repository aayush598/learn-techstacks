# Shortest Path Algorithms Guide

## Algorithm Selection Guide

```
WHICH SHORTEST PATH ALGORITHM SHOULD I USE?

                    ┌──────────────────┐
                    │ Need shortest    │
                    │ path?            │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ All edges have   │
                    │ weight ≥ 0?      │
                    └───┬──────────┬───┘
                    YES │          │ NO
                ┌───────▼───┐  ┌──▼──────────┐
                │ Single    │  │ Negative    │
                │ source?   │  │ weights?    │
                └──┬─────┬──┘  └──┬───────┬──┘
               YES │  NO │     YES│    NO │
            ┌──────▼┐  ┌─▼──┐  ┌─▼────┐  │
            │Dijkst-│  │All │  │Bellm-│  └──┐
            │ra     │  │pair│  │an-   │     │
            │       │  │    │  │Ford  │  ┌──▼────────┐
            └───────┘  └────┘  └──────┘  │Floyd-War  │
                                         │shall      │
Special cases:                           └───────────┘
  • Weights are 0 or 1 → 0-1 BFS (faster than Dijkstra)
  • Graph is a DAG → Topological sort + DP (O(V+E)!)
  • Unweighted graph → BFS (simplest!)
```

## Dijkstra's Algorithm (Min Heap)

### Visual: Dijkstra's Step-by-Step

```
Graph (directed, weighted):
  0 --4--> 1
  |        |
  1        1
  |        v
  v   2    3
  2 ------> 
     5

Edges: (0→1, 4), (0→2, 1), (1→3, 1), (2→1, 2), (2→3, 5)

Dijkstra's from node 0:

Step │ Heap (min)           │ Pop │ Distances          │ Updated
─────│──────────────────────│─────│────────────────────│──────────
  1  │ [(0, 0)]             │  0  │ [0, ∞, ∞, ∞]      │ 0=0
  2  │ [(1, 2), (4, 1)]     │  2  │ [0, ∞, 1, ∞]      │ 2=1
  3  │ [(3, 1), (4, 1)]     │  1  │ [0, 3, 1, ∞]      │ 1=3
  4  │ [(3, 1), (3, 6)]     │  3  │ [0, 3, 1, 4]      │ 3=4
  5  │ [(3, 6)]             │  -  │ Already have 4<6   │ skip
  DONE: dist = [0, 3, 1, 4]

Final Shortest Paths:
  0 → 0: distance 0 (direct)
  0 → 1: distance 3 (0→2→1, cost 1+2=3)  ← NOT 0→1 (cost 4)!
  0 → 2: distance 1 (0→2, cost 1)
  0 → 3: distance 4 (0→2→1→3, cost 1+2+1=4)

WHY Dijkstra's works:
┌───────────────────────────────────────────────────────────┐
│  Greedy property: When we pop a node from the min-heap,  │
│  we've GUARANTEED found the shortest path to it.         │
│  Why? Because all remaining paths in heap are ≥ current. │
│  With non-negative weights, no future path can be shorter│
└───────────────────────────────────────────────────────────┘
```

```python
import heapq
from collections import defaultdict

def dijkstra(graph, start, n):
    """
    Dijkstra's algorithm - Single source shortest path
    Works with NON-NEGATIVE weights only
    Time: O((V + E) log V) | Space: O(V + E)

    graph: dict of {node: [(neighbor, weight), ...]}
    n: number of vertices

    ALGORITHM:
    1. Initialize distances to infinity, start = 0
    2. Push (0, start) to min-heap
    3. While heap not empty:
       a. Pop node with smallest distance
       b. Skip if we already found a shorter path
       c. For each neighbor, try to improve distance
    """
    dist = {i: float('inf') for i in range(n)}
    dist[start] = 0
    prev = {i: -1 for i in range(n)}

    # Min heap: (distance, node)
    heap = [(0, start)]

    while heap:
        d, node = heapq.heappop(heap)

        # KEY OPTIMIZATION: Skip if outdated entry
        if d > dist[node]:
            continue

        for neighbor, weight in graph[node]:
            new_dist = dist[node] + weight

            # Relaxation: found a shorter path?
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = node
                heapq.heappush(heap, (new_dist, neighbor))

    return dist, prev


# Reconstruct path from start to target
def reconstruct_path(prev, start, target):
    """Follow prev pointers backward to build path"""
    path = []
    curr = target
    while curr != -1:
        path.append(curr)
        curr = prev[curr]
    return path[::-1] if path[-1] == start else []


# Example
graph = defaultdict(list)
edges = [(0, 1, 4), (0, 2, 1), (1, 3, 1), (2, 1, 2), (2, 3, 5)]
for u, v, w in edges:
    graph[u].append((v, w))

dist, prev = dijkstra(graph, 0, 4)
print(dist)  # {0: 0, 1: 3, 2: 1, 3: 4}
print(reconstruct_path(prev, 0, 3))  # [0, 2, 1, 3]
```

## Dijkstra's on Grid

```python
import heapq

def dijkstra_grid(grid, start, end):
    """
    Dijkstra's on grid where grid values are weights
    Time: O(M * N * log(M * N)) | Space: O(M * N)
    """
    if not grid or not grid[0]:
        return -1
    
    rows, cols = len(grid), len(grid[0])
    
    # dist[r][c] = min distance to reach (r, c)
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[start[0]][start[1]] = grid[start[0]][start[1]]
    
    # Min heap: (distance, row, col)
    heap = [(grid[start[0]][start[1]], start[0], start[1])]
    
    while heap:
        d, r, c = heapq.heappop(heap)
        
        if (r, c) == end:
            return d
        
        if d > dist[r][c]:
            continue
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < rows and 0 <= nc < cols:
                new_dist = d + grid[nr][nc]
                if new_dist < dist[nr][nc]:
                    dist[nr][nc] = new_dist
                    heapq.heappush(heap, (new_dist, nr, nc))
    
    return -1


# Example
grid = [
    [1, 3, 1],
    [1, 5, 1],
    [4, 2, 1]
]
print(dijkstra_grid(grid, (0, 0), (2, 2)))  # 7 (1→1→1→1→3)
```

## Bellman-Ford Algorithm

### Visual: Bellman-Ford Step-by-Step

```
WHEN to use Bellman-Ford (not Dijkstra):
  ✓ Graph has NEGATIVE edge weights
  ✓ Need to detect NEGATIVE CYCLES
  ✓ Simpler to implement than Dijkstra

Graph with negative edges:
  0 --(-1)--> 1 --(-1)--> 4
  |           |
  4          -1
  |           v
  v    3      3
  2 ------->
     2
  Edges: (0,1,-1), (0,2,4), (1,2,3), (1,3,2), (1,4,-1), (2,3,5), (3,4,3)

Bellman-Ford from node 0 (V=5, so relax V-1=4 times):

Iteration │ dist[0] │ dist[1] │ dist[2] │ dist[3] │ dist[4]
──────────│─────────│─────────│─────────│─────────│────────
Init      │    0    │    ∞    │    ∞    │    ∞    │    ∞
After 1   │    0    │   -1    │    4    │    1    │    0
After 2   │    0    │   -1    │    2    │    1    │    0
After 3   │    0    │   -1    │    2    │    1    │    0
After 4   │    0    │   -1    │    2    │    1    │    0
                              (no changes → converged!)

Final: dist = [0, -1, 2, 1, 0]

To detect negative cycle: Run one more iteration (V-th)
  If any distance STILL decreases → negative cycle exists!
  (A negative cycle can make path arbitrarily short)
```

```python
def bellman_ford(n, edges, start):
    """
    Bellman-Ford - Single source shortest path
    Works with NEGATIVE weights, detects negative cycles
    Time: O(V * E) | Space: O(V)

    ALGORITHM:
    1. Initialize distances: start=0, all others=infinity
    2. Repeat V-1 times: try to relax every edge
    3. After V-1 iterations, shortest paths are guaranteed
    4. Check one more time: if still improving → negative cycle!

    WHY V-1 iterations?
    The longest possible shortest path (without cycles) has V-1 edges.
    Each iteration guarantees finding paths with at most k edges.
    After V-1 iterations, we've found paths with up to V-1 edges.
    """
    dist = [float('inf')] * n
    dist[start] = 0
    prev = [-1] * n

    # Relax edges V-1 times
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w   # Relaxation!
                prev[v] = u
                updated = True

        if not updated:
            break  # Early termination: no more improvements

    # Check for negative cycle (V-th iteration)
    has_negative_cycle = False
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break

    return dist, prev, has_negative_cycle


# Example with negative weights
n = 5
edges = [
    (0, 1, -1), (0, 2, 4),
    (1, 2, 3), (1, 3, 2), (1, 4, -1),
    (2, 3, 5),
    (3, 4, 3)
]

dist, prev, neg_cycle = bellman_ford(n, edges, 0)
print(dist)  # [0, -1, 2, 1, 0]
print(neg_cycle)  # False
```

### Why Bellman-Ford Detects Negative Cycles

```
A negative cycle makes paths infinitely short:

  0 --> 1 --> 2
  |     ↑     |
  +--(-5)-----+

Cycle: 1→2→1 has total weight = -5 + 3 = -2
Going around this cycle makes distance decrease forever!

  dist[1] = -1 (after round 1)
  dist[1] = -3 (after round 2, went around cycle again)
  dist[1] = -5 (after round 3)
  ... keeps decreasing!

After V-1 rounds, shortest paths should be found.
If distances STILL decrease in round V → negative cycle!
```

## Floyd-Warshall Algorithm

### Visual: Floyd-Warshall All-Pairs Shortest Path

```
Floyd-Warshall finds shortest paths between ALL pairs of nodes.
Uses a 2D distance matrix and tries every node as intermediate.

Graph:           Initial dist[][]:
  0 --3--> 1     0   1   2   3
  |   8    |   ┌──────────────────┐
  2        2   0 │ 0 │ 3 │ 8 │ ∞ │
  |        v   ├──────────────────┤
  v   2    2   1 │ ∞ │ 0 │ 2 │ ∞ │
  2 ------->    ├──────────────────┤
     1          2 │ ∞ │ ∞ │ 0 │ 1 │
                  ├──────────────────┤
                3 │ ∞ │ ∞ │ ∞ │ 0 │
                  └──────────────────┘

After k=0 (via node 0):
  Can go 1→0→2: dist[1][2] = min(2, dist[1][0]+dist[0][2]) = 2 (no change)
  (no 0 paths improve things)

After k=1 (via node 1):
  Can go 0→1→3: dist[0][3] = min(∞, 3+2) = 5 ✓
  Can go 2→1→3: dist[2][3] = min(1, ∞+2) = 1 (no change)

After k=2 (via node 2):
  Can go 0→2→3: dist[0][3] = min(5, 8+1) = 5 (no change)
  Can go 1→2→3: dist[1][3] = min(∞, 2+1) = 3 ✓
  Can go 3→2→1: dist[3][1] = min(∞, ∞+∞) = ∞

After k=3 (via node 3):
  (minor improvements possible)

Final dist[][]:
  0   1   2   3
┌──────────────────┐
│ 0 │ 3 │ 5 │ 6 │   dist[0][3] = 6 (0→1→2→3: 3+2+1=6)
├──────────────────┤
│ 7 │ 0 │ 2 │ 3 │   dist[1][3] = 3 (1→2→3: 2+1=3)
├──────────────────┤
│ 5 │ 8 │ 0 │ 1 │
├──────────────────┤
│ 4 │ 7 │ 9 │ 0 │
└──────────────────┘
```

```python
def floyd_warshall(n, edges):
    """
    Floyd-Warshall - All pairs shortest path
    Works with NEGATIVE weights, detects negative cycles
    Time: O(V³) | Space: O(V²)

    ALGORITHM (3 nested loops):
    For each intermediate node k:
      For each pair (i, j):
        Is path i→k→j shorter than current i→j?
        If yes, update!

    KEY INSIGHT: dist[i][j] = min over all intermediate nodes k
    of (dist[i][k] + dist[k][j])
    """
    # Initialize distance matrix
    dist = [[float('inf')] * n for _ in range(n)]

    # Distance from node to itself is 0
    for i in range(n):
        dist[i][i] = 0

    # Set direct edges
    for u, v, w in edges:
        dist[u][v] = w

    # DP: Try all intermediate nodes
    for k in range(n):           # intermediate node
        for i in range(n):       # source
            for j in range(n):   # destination
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # Check for negative cycle (diagonal < 0 means negative cycle)
    has_negative_cycle = False
    for i in range(n):
        if dist[i][i] < 0:
            has_negative_cycle = True
            break

    return dist, has_negative_cycle


# Example
n = 4
edges = [
    (0, 1, 3), (0, 2, 8), (1, 2, 2),
    (2, 3, 1), (3, 0, 4)
]

dist, neg_cycle = floyd_warshall(n, edges)
for row in dist:
    print(row)
# [0, 3, 5, 6]
# [7, 0, 2, 3]
# [5, 8, 0, 1]
# [4, 7, 9, 0]
```

### Floyd-Warshall Code Pattern

```
The triple nested loop is ALWAYS:
  for k in range(n):        # intermediate
      for i in range(n):    # from
          for j in range(n): # to
              dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

MEMORY OPTIMIZATION:
  If you only need distances (not paths), use a 1D rolling array.
  But for the standard version, keep the full 2D matrix.
```

## 0-1 BFS (Using Deque)

```python
from collections import deque

def zero_one_bfs(graph, start, n):
    """
    0-1 BFS - Shortest path when edge weights are 0 or 1
    Time: O(V + E) | Space: O(V)
    """
    dist = [float('inf')] * n
    dist[start] = 0
    deque_ = deque([start])
    
    while deque_:
        node = deque_.popleft()
        
        for neighbor, weight in graph[node]:
            if dist[node] + weight < dist[neighbor]:
                dist[neighbor] = dist[node] + weight
                if weight == 0:
                    deque_.appendleft(neighbor)
                else:
                    deque_.append(neighbor)
    
    return dist


# Example
from collections import defaultdict
graph = defaultdict(list)
# (neighbor, weight) where weight is 0 or 1
edges = [(0, 1, 0), (0, 2, 1), (1, 3, 1), (2, 3, 0)]
for u, v, w in edges:
    graph[u].append((v, w))

print(zero_one_bfs(graph, 0, 4))  # [0, 0, 1, 0]


# 0-1 BFS on grid
def shortest_path_binary_matrix(grid):
    """
    LeetCode 1091 - Shortest path in binary matrix
    All moves have cost 1, use BFS
    """
    if grid[0][0] == 1 or grid[-1][-1] == 1:
        return -1
    
    n = len(grid)
    queue = deque([(0, 0, 1)])
    visited = set([(0, 0)])
    
    while queue:
        r, c, dist = queue.popleft()
        
        if r == n - 1 and c == n - 1:
            return dist
        
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if (0 <= nr < n and 0 <= nc < n and
                    grid[nr][nc] == 0 and (nr, nc) not in visited):
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))
    
    return -1
```

## Shortest Path in Weighted DAG

```python
from collections import defaultdict

def shortest_path_dag(n, edges, start):
    """
    Shortest path in weighted DAG using topological sort
    Time: O(V + E) | Space: O(V + E)
    More efficient than Dijkstra for DAGs
    """
    graph = defaultdict(list)
    in_degree = [0] * n
    
    for u, v, w in edges:
        graph[u].append((v, w))
        in_degree[v] += 1
    
    # Topological sort using Kahn's
    from collections import deque
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor, _ in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Process vertices in topological order
    dist = [float('inf')] * n
    dist[start] = 0
    
    for node in topo_order:
        if dist[node] != float('inf'):
            for neighbor, weight in graph[node]:
                if dist[node] + weight < dist[neighbor]:
                    dist[neighbor] = dist[node] + weight
    
    return dist


# Example
edges = [(0, 1, 5), (0, 2, 3), (1, 3, 6), (1, 2, 2), (2, 4, 4), (2, 5, 2), (3, 5, 1), (4, 5, 3)]
print(shortest_path_dag(6, edges, 0))  # [0, 5, 3, 11, 7, 8]
```

## Comparison Table

```
| Algorithm          | Time        | Space    | Negative Wt | Neg Cycle | Use Case                    |
|--------------------|-------------|----------|-------------|-----------|-----------------------------|
| Dijkstra           | O((V+E)logV)| O(V+E)  | No          | No        | Sparse, single source       |
| Bellman-Ford       | O(VE)       | O(V)     | Yes         | Yes       | Negative weights            |
| Floyd-Warshall     | O(V³)       | O(V²)    | Yes         | Yes       | All pairs, dense graph      |
| 0-1 BFS            | O(V+E)      | O(V)     | No (0/1)    | No        | Weights are 0 or 1          |
| DAG Shortest       | O(V+E)      | O(V+E)   | Yes         | No        | DAG, most efficient         |

DECISION FLOWCHART:

  Which algorithm?
  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │  Single source, non-negative weights?                   │
  │  └── YES → Dijkstra's (O((V+E)logV))                   │
  │                                                         │
  │  Single source, negative weights possible?              │
  │  └── YES → Bellman-Ford (O(VE))                         │
  │                                                         │
  │  All pairs shortest path?                               │
  │  └── YES → Floyd-Warshall (O(V³))                       │
  │                                                         │
  │  Edge weights only 0 or 1?                              │
  │  └── YES → 0-1 BFS (O(V+E)) — faster than Dijkstra!    │
  │                                                         │
  │  Graph is a DAG (no cycles)?                            │
  │  └── YES → Topological sort + DP (O(V+E)) — fastest!   │
  │                                                         │
  │  Unweighted graph (all edges weight 1)?                 │
  │  └── YES → BFS (O(V+E)) — simplest!                    │
  │                                                         │
  └─────────────────────────────────────────────────────────┘
```

## When to Use What

```
Single source, non-negative weights → Dijkstra
Single source, negative weights → Bellman-Ford
All pairs shortest path → Floyd-Warshall
Weights are only 0 or 1 → 0-1 BFS
Graph is a DAG → Topological sort approach
Need to detect negative cycle → Bellman-Ford or Floyd-Warshall
Grid with uniform weights → BFS
Grid with varying weights → Dijkstra on grid

COMMON MISTAKES TO AVOID:
┌──────────────────────────────────────────────────────────┐
│ ✗ Using Dijkstra with negative weights                   │
│   → Dijkstra is GREEDY, negative edges break it!        │
│                                                         │
│ ✗ Forgetting the "if d > dist[node]: continue" check    │
│   → Without this, you get TLE (duplicate heap entries)  │
│                                                         │
│ ✗ Running Floyd-Warshall when V > 500                    │
│   → O(V³) is too slow for large graphs                  │
│                                                         │
│ ✗ Not using early termination in Bellman-Ford            │
│   → Add "if not updated: break" to save time            │
│                                                         │
│ ✗ Confusing 0-1 BFS with regular BFS                    │
│   → 0-1 BFS uses deque: 0-weight → appendleft           │
│   →                             1-weight → append       │
└──────────────────────────────────────────────────────────┘
```
