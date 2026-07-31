# 12. Graphs Cheatsheet

Graph representations, BFS/DFS traversals, grid BFS/DFS, cycle detection, topological sort, shortest paths (Dijkstra, Bellman-Ford, Floyd-Warshall), MST (Prim, Kruskal), bipartite check, SCC (Kosaraju), bridges/articulation points. All code verified on Python 3.

## Graph Representations

### Adjacency List (defaultdict) — THE standard

```python
from collections import defaultdict

def build_adj(edges, n, undirected=True):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        if undirected:
            adj[v].append(u)
    return adj
```

### Adjacency List (plain dict, all keys present)

```python
def build_adj_dict(edges, n):
    adj = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)      # undirected: add BOTH ways
    return adj
```

### Adjacency Matrix (dense, small n)

```python
def build_matrix(edges, n):
    mat = [[0] * n for _ in range(n)]
    for u, v in edges:
        mat[u][v] = 1
        mat[v][u] = 1
    return mat   # check neighbor v of u: mat[u][v] != 0; O(n) per node
```

### Edge List (for Bellman-Ford, Kruskal)

```python
edges = [(0, 1, 4), (1, 2, 2), (2, 0, 1)]   # triplets (u, v, w)
```

| Representation | Build time | Check edge u→v | Iterate neighbors | Use for |
|---|---|---|---|---|
| Adjacency list | O(E) | O(deg(u)) | O(deg(u)) | BFS/DFS, Dijkstra, topo |
| Adjacency matrix | O(n²) | O(1) | O(n) | Floyd-Warshall, dense graphs |
| Edge list | O(E) | O(E) | — | Bellman-Ford, Kruskal |

**Directed graph rule:** drop the `adj[v].append(u)` line. **Weighted graph rule:** store `(v, w)` tuples.

## Traversals

### Iterative BFS with deque + distance

```python
from collections import deque

def bfs(start, adj):
    dist = {start: 0}
    q = deque([start])
    order = []
    while q:
        u = q.popleft()          # FIFO = level order
        order.append(u)
        for v in adj[u]:
            if v not in dist:    # visited check on ENQUEUE
                dist[v] = dist[u] + 1
                q.append(v)
    return order, dist

# order, dist = bfs(0, adj)
# order = BFS order, dist[v] = shortest path length from start (unweighted)
```

- **Visited set:** a dict/set guarding *enqueue* (not dequeue) — this guarantees each node is enqueued once and the first time a node is reached is its shortest path.
- **Complexity:** O(V + E) time, O(V) space.

### BFS with level-by-level separation (islands, 0-1 BFS variants)

```python
from collections import deque

def bfs_levels(start, adj):
    visited = {start}
    q = deque([start])
    level = 0
    while q:
        for _ in range(len(q)):   # process one full level at a time
            u = q.popleft()
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    q.append(v)
        level += 1
    return visited
```

### Iterative DFS with stack

```python
def dfs_iter(start, adj):
    visited = set()
    stack = [start]
    order = []
    while stack:
        u = stack.pop()           # LIFO
        if u in visited:          # recheck: node may be pushed twice
            continue
        visited.add(u)
        order.append(u)
        for v in reversed(adj[u]):   # reversed to mimic recursive order
            if v not in visited:
                stack.append(v)
    return order
```

**Complexity:** O(V + E) time, O(V) space.

### Recursive DFS (simplest; watch recursion depth)

```python
def dfs_rec(u, adj, visited=None, order=None):
    if visited is None:
        visited, order = set(), []
    visited.add(u)
    order.append(u)
    for v in adj[u]:
        if v not in visited:
            dfs_rec(v, adj, visited, order)
    return order
```

### Recursive DFS on grids with on-path set (backtracking)

```python
def dfs_grid(grid, r, c, target, on_path):
    rows, cols = len(grid), len(grid[0])
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]   # or reuse dirs_4 below
    if not (0 <= r < rows and 0 <= c < cols):
        return False
    if grid[r][c] != target or (r, c) in on_path:
        return False
    on_path.add((r, c))
    for dr, dc in dirs:
        if dfs_grid(grid, r + dr, c + dc, target, on_path):
            return True
    on_path.remove((r, c))
    return False
```

`on_path` marks the current recursion chain so a path cannot reuse cells — use it when the path must be simple (word search, knight tours). For reachability ("flood fill") use a plain visited set or mark cells in-place.

## Grid Utility Constants

```python
dirs_4 = [(0, 1), (0, -1), (1, 0), (-1, 0)]          # 4-directional
dirs_8 = [(0, 1), (0, -1), (1, 0), (-1, 0),
          (1, 1), (1, -1), (-1, 1), (-1, -1)]        # 8-directional (incl. diagonals)
```

**Complexity note for all grid DFS/BFS:** O(rows × cols) since each cell is visited once.

## Grid BFS

### Number of Islands (grid BFS)

```python
from collections import deque

def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def bfs(r, c):
        q = deque([(r, c)])
        grid[r][c] = "0"          # mark visited by flooding in-place
        while q:
            r, c = q.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                    grid[nr][nc] = "0"
                    q.append((nr, nc))

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                bfs(r, c)
    return count
```

Counting: each flood-erase of an island increments once. Same shape works for "largest island" (track max size per BFS). **Complexity:** O(rows·cols), O(rows·cols) queue.

### Shortest Path in Grid with 0/1 Weights (BFS levels)

```python
from collections import deque

def shortest_path_binary(grid):   # each cell weight 0 or 1; 8-dir variant shown
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[rows - 1][cols - 1] == 1:
        return -1
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)]
    q = deque([(0, 0, 1)])
    grid[0][0] = 1                # visited
    while q:
        r, c, d = q.popleft()
        if (r, c) == (rows - 1, cols - 1):
            return d
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                grid[nr][nc] = 1
                q.append((nr, nc, d + 1))
    return -1
```

**0-1 BFS pattern:** if all edges are 0 or 1 weight, use a deque — push `0`-weight edges to the **front** (`appendleft`), `1`-weight edges to the **back** (`append`); dist array replaces the level counter. **Complexity:** O(rows·cols).

### Rotten Oranges (multi-source BFS)

```python
from collections import deque

def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c, 0))       # all rotten oranges are sources
            elif grid[r][c] == 1:
                fresh += 1
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    minutes = 0
    while q:
        r, c, t = q.popleft()
        minutes = max(minutes, t)
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                q.append((nr, nc, t + 1))
    return -1 if fresh else minutes

assert oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
```

**Multi-source trick:** enqueue ALL source cells with distance 0 before the BFS loop. **Complexity:** O(rows·cols).

## Grid DFS

### Number of Islands (DFS flood-fill variant)

```python
def num_islands_dfs(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1":
            return
        grid[r][c] = "0"            # sink the island
        for dr, dc in dirs:
            dfs(r + dr, c + dc)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)
    return count
```

**Complexity:** O(rows·cols) time, O(rows·cols) recursion stack worst case (chain of 1s). Use BFS/iterative when the grid is huge.

### Surrounded Regions (mark border, then flip)

```python
def solve(board):
    if not board:
        return
    rows, cols = len(board), len(board[0])
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != "O":
            return
        board[r][c] = "#"           # temporarily mark border-connected
        for dr, dc in dirs:
            dfs(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if r in (0, rows - 1) or c in (0, cols - 1):
                if board[r][c] == "O":
                    dfs(r, c)

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "O":
                board[r][c] = "X"   # enclosed -> capture
            elif board[r][c] == "#":
                board[r][c] = "O"   # restore border-connected
```

**Strategy:** any O touching the border survives; flood from all border O's, then flip everything still O to X. **Complexity:** O(rows·cols).

## Cycle Detection

### Directed — 3-color state (WHITE/GRAY/BLACK)

```python
from collections import defaultdict

def has_cycle_directed(n, edges):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n

    def dfs(u):
        color[u] = GRAY          # on current path
        for v in adj[u]:
            if color[v] == GRAY:     # back edge to an ancestor on path -> cycle
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK         # fully explored
        return False

    return any(color[u] == WHITE and dfs(u) for u in range(n))

assert has_cycle_directed(4, [(0, 1), (1, 2), (2, 0)])          # True
assert not has_cycle_directed(4, [(0, 1), (1, 2), (2, 3)])      # False
```

GRAY = currently on the DFS stack (an ancestor); BLACK = fully processed. A `GRAY` neighbor = back edge = directed cycle. **Complexity:** O(V + E).

### Undirected — parent pointer

```python
from collections import defaultdict

def has_cycle_undirected(n, edges):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    visited = [False] * n

    def dfs(u, parent):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                if dfs(v, u):
                    return True
            elif v != parent:       # visited neighbor that is NOT parent -> cycle
                return True
        return False

    return any(not visited[u] and dfs(u, -1) for u in range(n))
```

In undirected graphs the only visited neighbor that is NOT a cycle is the parent — every other visited neighbor is a back edge. **Complexity:** O(V + E).

## Topological Sort

### Kahn's Algorithm (BFS + in-degree) — DAG only

```python
from collections import defaultdict, deque

def topo_kahn(n, edges):
    adj = defaultdict(list)
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque([u for u in range(n) if indeg[u] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []   # [] means graph has a cycle
```

- **If `len(order) != n`** → a cycle exists (nodes with never-zero in-degree remain) — this doubles as cycle detection.
- **Complexity:** O(V + E) time, O(V) space.

### DFS-based (postorder, then reverse)

```python
from collections import defaultdict

def topo_dfs(n, edges):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
    visited = [False] * n
    order = []

    def dfs(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs(v)
        order.append(u)              # postorder

    for u in range(n):
        if not visited[u]:
            dfs(u)
    return order[::-1]               # reverse postorder = topo order

assert topo_dfs(4, [(0, 1), (1, 2), (2, 3)]) == [0, 1, 2, 3]
```

**Why reverse postorder?** DFS finishing order lists nodes with all descendants first; reversing gives "dependencies before dependents". **Complexity:** O(V + E).

## Shortest Paths

### Dijkstra (non-negative weights, heap)

```python
from collections import defaultdict
import heapq

def dijkstra(n, edges, src):
    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [float("inf")] * n
    dist[src] = 0
    pq = [(0, src)]                       # (distance, node) tuples
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:                   # stale entry -> skip
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:              # relax
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

assert dijkstra(5, [(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5),(3,4,3)], 0) == [0, 3, 1, 4, 7]
```

- Heap holds `(dist, node)` — the dist goes FIRST so the heap sorts by distance.
- **Stale-entry skip** (`if d > dist[u]: continue`) is mandatory for correctness/performance; it makes the visited-set check unnecessary.
- **Complexity:** O((V + E) log V). Fails on negative weights — use Bellman-Ford.

### Bellman-Ford (negative weights; relax V-1 times)

```python
def bellman_ford(n, edges, src):
    dist = [float("inf")] * n
    dist[src] = 0
    for _ in range(n - 1):                # relax ALL edges V-1 times
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    # one more pass detects negative-weight cycles
    for u, v, w in edges:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            return None                   # negative cycle present
    return dist
```

**Why V-1 passes?** The longest simple path in V nodes uses ≤ V-1 edges; relaxing all edges once per pass guarantees shortest paths propagate fully. **Complexity:** O(V·E).

### Floyd-Warshall (all-pairs; k outer)

```python
def floyd_warshall(n, edges):
    INF = float("inf")
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)   # handle duplicate edges
    for k in range(n):                    # k OUTER: intermediate node
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist

assert floyd_warshall(5, [(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5),(3,4,3)])[0] == [0, 3, 1, 4, 7]
```

**k MUST be the outermost loop** — otherwise you'd use a not-yet-final intermediate. Negative cycle ⇔ `dist[i][i] < 0` after the loop. **Complexity:** O(V³) time, O(V²) space.

## Minimum Spanning Tree

### Prim's Algorithm (heap)

```python
from collections import defaultdict
import heapq

def prim_mst(n, edges):
    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    visited = [False] * n
    pq = [(0, 0)]                        # (weight, node), start at 0
    total = 0
    count = 0
    while pq and count < n:
        w, u = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        total += w
        count += 1
        for v, w2 in adj[u]:
            if not visited[v]:
                heapq.heappush(pq, (w2, v))
    return total if count == n else None  # None = disconnected

assert prim_mst(5, [(0,1,2),(0,3,6),(1,2,3),(1,3,8),(1,4,5),(2,4,7),(3,4,9)]) == 16
```

Greedily grow one tree by always taking the cheapest edge from the tree to an unvisited node. **Complexity:** O((V + E) log V).

### Kruskal's Algorithm (union-find) — requires DSU

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):                     # path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):                 # union by rank
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.components -= 1
        return True

def kruskal_mst(n, edges):
    dsu = DSU(n)
    total = 0
    for w, u, v in sorted((w, u, v) for u, v, w in edges):   # sort edges by weight
        if dsu.union(u, v):                # union returns False if already connected
            total += w
    return total if dsu.components == 1 else None

assert kruskal_mst(5, [(0,1,2),(0,3,6),(1,2,3),(1,3,8),(1,4,5),(2,4,7),(3,4,9)]) == 16
```

**Complexity:** O(E log E) for sorting + near-O(1) amortized per DSU op (α ≈ 1). The DSU class above is the complete union-find template (path compression + union by rank) — reuse it verbatim for any connectivity/counting problem.

## Bipartite Check (BFS 2-coloring)

```python
from collections import defaultdict, deque

def is_bipartite(n, edges):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    color = [-1] * n                        # -1 uncolored, else 0 or 1
    for start in range(n):                  # handle disconnected graph
        if color[start] != -1:
            continue
        color[start] = 0
        q = deque([start])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]      # opposite color
                    q.append(v)
                elif color[v] == color[u]:       # same color -> conflict
                    return False
    return True

assert is_bipartite(4, [(0, 1), (1, 2), (2, 3)])        # True (path = 2-colorable)
assert not is_bipartite(3, [(0, 1), (1, 2), (2, 0)])    # False (odd cycle)
```

A graph is bipartite ⇔ 2-colorable ⇔ has **no odd-length cycle**. Coloring also partitions nodes into the two sides (useful for "split groups" problems). **Complexity:** O(V + E).

## Strongly Connected Components (Kosaraju, outline)

```python
from collections import defaultdict

def kosaraju(n, edges):
    adj = defaultdict(list)
    radj = defaultdict(list)               # reversed graph
    for u, v in edges:
        adj[u].append(v)
        radj[v].append(u)

    # Pass 1: DFS on G, record finish order
    visited = [False] * n
    order = []

    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)                    # postorder

    for u in range(n):
        if not visited[u]:
            dfs1(u)

    # Pass 2: DFS on reversed graph in reverse finish order
    comp = [-1] * n

    def dfs2(u, cid):
        comp[u] = cid
        for v in radj[u]:
            if comp[v] == -1:
                dfs2(v, cid)

    cid = 0
    for u in reversed(order):
        if comp[u] == -1:
            dfs2(u, cid)
            cid += 1
    return cid                              # number of SCCs

assert kosaraju(5, [(1, 0), (0, 2), (2, 1), (0, 3), (3, 4)]) == 3
```

**Intuition:** In a DAG of SCCs, processing vertices by decreasing finish time and searching the *reversed* graph visits exactly one SCC at a time. (Tarjan does it in one pass with a low-link array — same O(V+E).) **Complexity:** O(V + E) time, O(V) space.

## Bridges & Articulation Points (Tarjan, outline)

```python
from collections import defaultdict

def find_bridges(n, edges):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    tin = [-1] * n                          # discovery time
    low = [0] * n                           # lowest tin reachable via back edges
    timer = [0]
    bridges = []

    def dfs(u, parent):
        tin[u] = low[u] = timer[0]
        timer[0] += 1
        for v in adj[u]:
            if v == parent:
                continue
            if tin[v] != -1:                # back edge
                low[u] = min(low[u], tin[v])
            else:                           # tree edge
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:         # bridge condition
                    bridges.append((u, v))

    for u in range(n):
        if tin[u] == -1:
            dfs(u, -1)
    return bridges
```

- **Bridge (u,v):** `low[v] > tin[u]` — no back edge from v's subtree reaches u or above.
- **Articulation point u:** root → more than one child in DFS tree; non-root → exists child v with `low[v] >= tin[u]`.
- **Complexity:** O(V + E) time, O(V) space.

## Complexity Reference Table

| Algorithm | Time | Space |
|---|---|---|
| BFS / DFS (list) | O(V + E) | O(V) |
| BFS / DFS (grid) | O(rows·cols) | O(rows·cols) |
| Cycle detection (directed / undirected) | O(V + E) | O(V) |
| Topological sort (Kahn / DFS) | O(V + E) | O(V) |
| Dijkstra (heap) | O((V + E) log V) | O(V + E) |
| Bellman-Ford | O(V·E) | O(V) |
| Floyd-Warshall | O(V³) | O(V²) |
| Prim (heap) | O((V + E) log V) | O(V + E) |
| Kruskal (union-find) | O(E log E) | O(V) |
| Bipartite check (BFS) | O(V + E) | O(V) |
| Kosaraju / Tarjan SCC | O(V + E) | O(V) |
| Bridges / articulation | O(V + E) | O(V) |
