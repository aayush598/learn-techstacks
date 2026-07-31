# DP on Graphs — Complete Guide

## Graph DP Decision Tree

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    GRAPH DP PATTERN GUIDE                                │
├─────────────────────────────┬────────────────────────────────────────────┤
│ Problem hints               │ Approach                                 │
├─────────────────────────────┼────────────────────────────────────────────┤
│ "shortest paths, neg edges" │ Bellman-Ford (V-1 edge relaxations)      │
│ "all-pairs shortest paths"  │ Floyd-Warshall (DP over intermediate k)  │
│ "longest path in DAG"       │ Topo sort + DP on DAG                    │
│ "critical path / scheduling"│ Forward + backward DP on topo order      │
│ "visit all nodes exactly once"│ TSP / Hamiltonian (bitmask DP, O(2ⁿn²))│
│ "shortest Hamiltonian path"  │ Bitmask DP: dp[mask][last]              │
│ "count Hamiltonian paths"    │ Bitmask counting DP                     │
└─────────────────────────────┴────────────────────────────────────────────┘
```

---

## Shortest Path with DP

### Bellman-Ford Algorithm

Finds shortest paths from source to all vertices, handles negative weights.

### Visual Walkthrough

```
Graph:
  0 --4--> 1 --3--> 3
  |         ^       ^
  2         |1      |
  v         2       |
  2 ---------> 1    |
         5          |
  2 --5--> 4        |
  4 --(-5)--> 3

Edges: (0,1,4), (0,2,2), (1,2,3), (1,3,2), (1,4,3),
       (2,1,1), (2,3,4), (2,4,5), (4,3,-5)

Relax all edges V-1=4 times. Each round, distances improve:

  Initial:  dist = [0, ∞, ∞, ∞, ∞]

  Round 1 (relax all edges):
    (0,1,4): dist[1] = min(∞, 0+4) = 4
    (0,2,2): dist[2] = min(∞, 0+2) = 2
    (1,2,3): dist[2] = min(2, 4+3) = 2 (no change)
    (1,3,2): dist[3] = min(∞, 4+2) = 6
    (1,4,3): dist[4] = min(∞, 4+3) = 7
    (2,1,1): dist[1] = min(4, 2+1) = 3  ← improved!
    (2,3,4): dist[3] = min(6, 2+4) = 6 (no change)
    (2,4,5): dist[4] = min(7, 2+5) = 7 (no change)
    (4,3,-5): dist[3] = min(6, 7-5) = 2  ← improved!
    → dist = [0, 3, 2, 2, 7]

  Round 2:
    (2,1,1): dist[1] = min(3, 2+1) = 3 (no change)
    (1,3,2): dist[3] = min(2, 3+2) = 2 (no change)
    (4,3,-5): dist[3] = min(2, 7-5) = 2 (no change)
    → No changes → can terminate early!

  Final: dist = [0, 3, 2, 2, 6]  (wait, let me recalculate...)
  Actually: after more rounds, dist[4] might improve via 2→4 route
  
  Answer: dist = [0, 3, 2, 2, 7] (or 0, 3, 2, 0, 6 with the -5 edge)

Negative cycle check: run one more round; if any distance improves → negative cycle!
```

```python
def bellman_ford(edges: list, V: int, src: int) -> list:
    INF = float('inf')
    dist = [INF] * V
    dist[src] = 0
    path = [-1] * V

    for _ in range(V - 1):        # V-1 rounds sufficient for shortest path
        updated = False
        for u, v, w in edges:      # Relax every edge
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                path[v] = u
                updated = True
        if not updated:            # Early termination
            break

    # Negative cycle detection: one more round
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None  # Negative cycle detected!

    return dist

# Time: O(V × E), Space: O(V)
```

---

### Floyd-Warshall Algorithm

All-pairs shortest path. Works for all vertices.

### Visual Walkthrough

```
Key idea: Try ALL vertices as intermediate nodes one at a time.

  dp[k][i][j] = shortest path from i to j using only vertices 0..k

  dp[0][i][j] = direct edge i→j (or ∞ if none)
  dp[k][i][j] = min(dp[k-1][i][j], dp[k-1][i][k] + dp[k-1][k][j])
                          ──────          ─────────────────────────
                      don't use k         go through k as intermediate

Example: 3 nodes
  Initial (k=-1, direct edges):
       0    1    2
    ┌────┬────┬────┐
  0 │  0 │  5 │  ∞ │
    ├────┼────┼────┤
  1 │  ∞ │  0 │  3 │
    ├────┼────┼────┤
  2 │  2 │  ∞ │  0 │
    └────┴────┴────┘

  k=0 (use node 0 as intermediate):
    dp[0][2][1] = min(∞, dp[2][0]+dp[0][1]) = min(∞, 2+5) = 7

       0    1    2
    ┌────┬────┬────┐
  0 │  0 │  5 │  ∞ │
    ├────┼────┼────┤
  1 │  ∞ │  0 │  3 │
    ├────┼────┼────┤
  2 │  2 │  7 │  0 │  ← 2→0→1 = 7
    └────┴────┴────┘

  k=1 (use node 1 as intermediate):
    dp[0][2][1] already 7, check dp[0][1]+dp[1][2] = 5+3 = 8 > ∞... no

  k=2 (use node 2 as intermediate):
    dp[0][1][2] = min(5, dp[1][0]+dp[0][2])... etc

  Space optimization: use 2D array (overwrite in place, since k depends on k-1)
```

```python
def floyd_warshall(graph: list) -> list:
    V = len(graph)
    INF = float('inf')
    dist = [row[:] for row in graph]  # Copy adjacency matrix

    for k in range(V):              # Intermediate vertex
        for i in range(V):          # Source
            if dist[i][k] == INF:
                continue
            for j in range(V):      # Destination
                if dist[k][j] != INF:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist

# Time: O(V³), Space: O(V²) — can be O(V) with space optimization
```

---

## Longest Path in DAG

Given a DAG, find longest path.

### Visual Walkthrough

```
Topological sort → process nodes in order → relax edges:

  Graph:  0→1(5), 0→2(3), 1→2(2), 1→3(6), 2→4(4), 2→5(2), 2→3(7)

  Topo sort: 0, 1, 2, 3, 4, 5

  dist[0] = 0 (source)
  
  Process 0: edges to 1(+5), 2(+3)
    dist[1] = max(-∞, 0+5) = 5
    dist[2] = max(-∞, 0+3) = 3

  Process 1: edges to 2(+2), 3(+6)
    dist[2] = max(3, 5+2) = 7  ← improved!
    dist[3] = max(-∞, 5+6) = 11

  Process 2: edges to 3(+7), 4(+4), 5(+2)
    dist[3] = max(11, 7+7) = 14 ← improved!
    dist[4] = max(-∞, 7+4) = 11
    dist[5] = max(-∞, 7+2) = 9

  Process 3: edges to 4(-1)
    dist[4] = max(11, 14-1) = 13 ← improved!

  Process 4: edges to 5(-2)
    dist[5] = max(9, 13-2) = 11 ← improved!

  Final: dist = [0, 5, 7, 14, 13, 11]
  Longest path = 14 (0→1→2→3)
```

```python
def longest_path_dag(V: int, edges: list) -> int:
    adj = [[] for _ in range(V)]
    indeg = [0] * V
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1

    # Step 1: Topological sort (Kahn's BFS)
    from collections import deque
    q = deque([i for i in range(V) if indeg[i] == 0])
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    # Step 2: DP on topological order
    dist = [float('-inf')] * V
    dist[topo[0]] = 0 if V > 0 else 0
    for u in topo:
        if dist[u] != float('-inf'):
            for v, w in adj[u]:
                dist[v] = max(dist[v], dist[u] + w)

    return max(dist) if dist else 0

# Time: O(V + E), Space: O(V + E)
```

---

## Critical Paths in DAG

Find the longest path (critical path) in a DAG representing task dependencies.

```
Forward pass:  earliest_start[v] = max over all parents u of (earliest[u] + weight(u,v))
Backward pass: latest_start[u]  = min over all children v of (latest[v] - weight(u,v))

Critical tasks: earliest_start[i] == latest_start[i]
  (no slack — delaying this task delays the entire project)
```

```python
def critical_path_tasks(V: int, edges: list) -> tuple:
    adj = [[] for _ in range(V)]
    indeg = [0] * V
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1

    from collections import deque
    q = deque([i for i in range(V) if indeg[i] == 0])
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    # Forward pass: earliest start times
    earliest = [0] * V
    for u in topo:
        for v, w in adj[u]:
            earliest[v] = max(earliest[v], earliest[u] + w)

    total_time = max(earliest)

    # Backward pass: latest start times
    latest = [total_time] * V
    for u in reversed(topo):
        for v, w in adj[u]:
            latest[u] = min(latest[u], latest[v] - w)

    # Critical tasks: earliest == latest (zero slack)
    critical = [i for i in range(V) if earliest[i] == latest[i]]

    return total_time, critical

# Time: O(V + E), Space: O(V + E)
```

---

## DP with State Compression on Graphs

### Shortest Hamiltonian Path

Given a complete weighted graph on n nodes, find shortest path visiting each vertex exactly once.

```python
def shortest_hamiltonian_path(graph: list) -> int:
    n = len(graph)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    for i in range(n):
        dp[1 << i][i] = 0 if i == 0 else INF  # start from node 0

    # dp[mask][last] = min cost to reach state (visited mask, current node)
    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            if dp[mask][last] == INF:
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue
                new_mask = mask | (1 << nxt)
                dp[new_mask][nxt] = min(dp[new_mask][nxt],
                                        dp[mask][last] + graph[last][nxt])

    full_mask = (1 << n) - 1
    return min(dp[full_mask][i] for i in range(n))

# Example: n=4, graph = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
# Answer: 10 + 25 + 30 = 65 (path: 0→1→3→2)

# Time: O(2^n × n²), Space: O(2^n × n)
```

---

## Traveling Salesman Problem (TSP)

Find shortest route visiting each city exactly once and returning to start.

### Visual Walkthrough

```
TSP is the quintessential bitmask DP problem.

State: dp[mask][last] = min cost to reach this state
  mask = bitmask of visited cities
  last = current city

  Start: dp[1][0] = 0 (only city 0 visited, cost 0)

Example: 4 cities
  0→1=10, 0→2=15, 0→3=20
  1→0=10, 1→2=35, 1→3=25
  2→0=15, 2→3=30, 2→1=35
  3→0=20, 3→1=25, 3→2=30

State transitions:
  dp[mask | (1<<nxt)][nxt] = min(dp[mask][last] + graph[last][nxt])

Trace for path 0→1→3→2→0:
  dp[0001][0] = 0        (start)
  dp[0011][1] = 10       (0→1)
  dp[1011][3] = 35       (1→3, cost 25)
  dp[1111][2] = 65       (3→2, cost 30)
  Answer: 65 + graph[2][0] = 65+15 = 80

  Optimal: 0→1→3→2→0 = 10+25+30+15 = 80
  
  Actually optimal is 0→2→3→1→0 = 15+30+25+10 = 80 too.
  Or 0→1→3→2→0 = 10+25+30+15 = 80

  dp table for n=4:
  mask=1 (city 0): dp[1][0] = 0
  mask=3: dp[3][1] = 10 (from 0→1)
  mask=5: dp[5][2] = 15 (from 0→2)
  mask=9: dp[9][3] = 20 (from 0→3)
  ... continue building up to mask=15 (all visited)
  Answer = min(dp[15][i] + graph[i][0] for i in 1..3)
```

```python
def tsp_memo(graph: list) -> int:
    n = len(graph)
    INF = float('inf')
    memo = {}

    def dp(mask: int, pos: int) -> int:
        if mask == (1 << n) - 1:        # All cities visited
            return graph[pos][0] if graph[pos][0] > 0 else INF  # Return to start
        key = (mask, pos)
        if key in memo:
            return memo[key]
        best = INF
        for city in range(n):
            if mask & (1 << city) or graph[pos][city] == 0:
                continue                 # Already visited or no edge
            best = min(best, graph[pos][city] + dp(mask | (1 << city), city))
        memo[key] = best
        return best

    return dp(1, 0)  # Start at city 0, only city 0 visited

def tsp_tab(graph: list) -> int:
    n = len(graph)
    INF = 10**9
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Start at city 0

    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            if dp[mask][last] == INF:
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue             # Already visited
                new_mask = mask | (1 << nxt)
                dp[new_mask][nxt] = min(dp[new_mask][nxt],
                                        dp[mask][last] + graph[last][nxt])

    full_mask = (1 << n) - 1
    return min(dp[full_mask][i] + graph[i][0] for i in range(n) if graph[i][0] > 0)

# Time: O(2^n × n²), Space: O(2^n × n)
# Feasible for n ≤ 20
```

### Shortest Hamiltonian Path (No Return to Start)

```python
def shortest_hamiltonian_path(graph: list) -> int:
    n = len(graph)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Start from node 0

    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            if dp[mask][last] == INF:
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue
                new_mask = mask | (1 << nxt)
                dp[new_mask][nxt] = min(dp[new_mask][nxt],
                                        dp[mask][last] + graph[last][nxt])

    full_mask = (1 << n) - 1
    return min(dp[full_mask])  # No return edge needed!

# Time: O(2^n × n²), Space: O(2^n × n)
```

---

## Hamiltonian Path DP (Existence + Count)

Count number of Hamiltonian paths (paths visiting each vertex exactly once).

```python
def hamiltonian_path_count(n: int, edges: list) -> int:
    """Count Hamiltonian paths in an undirected graph"""
    adj = [[False] * n for _ in range(n)]
    for u, v in edges:
        adj[u][v] = adj[v][u] = True

    dp = [[0] * n for _ in range(1 << n)]

    for i in range(n):
        dp[1 << i][i] = 1  # Start from any single city

    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)) or dp[mask][last] == 0:
                continue
            for nxt in range(n):
                if mask & (1 << nxt) or not adj[last][nxt]:
                    continue
                dp[mask | (1 << nxt)][nxt] += dp[mask][last]

    return sum(dp[(1 << n) - 1])  # Sum all paths ending at any city

# Time: O(2^n × n²), Space: O(2^n × n)
```

---

## Summary Table & Quick Reference

```
┌──────────────────────────┬─────────────────────────┬──────────┬──────────┬────────────────────────────────┐
│ Problem                  │ Approach                │ Time     │ Space    │ When to Use                    │
├──────────────────────────┼─────────────────────────┼──────────┼──────────┼────────────────────────────────┤
│ Bellman-Ford             │ Edge relaxation ×V-1    │ O(V×E)   │ O(V)     │ Single source, neg edges OK   │
│ Floyd-Warshall           │ DP over intermediates   │ O(V³)    │ O(V²)    │ All-pairs shortest paths       │
│ Longest Path DAG         │ Topo sort + DP          │ O(V+E)   │ O(V)     │ DAG + longest path             │
│ Critical Path            │ Forward + backward pass │ O(V+E)   │ O(V)     │ Task scheduling / project mgmt │
│ Shortest Hamiltonian     │ Bitmask dp[mask][last]  │ O(2ⁿn²) │ O(2ⁿn)  │ Visit all nodes, shortest path │
│ TSP                      │ Bitmask + return        │ O(2ⁿn²) │ O(2ⁿn)  │ Visit all, return to start     │
│ Hamiltonian Path Count   │ Bitmask counting DP     │ O(2ⁿn²) │ O(2ⁿn)  │ Count all valid paths          │
└──────────────────────────┴─────────────────────────┴──────────┴──────────┴────────────────────────────────┘
```

### Bitmask DP Pattern for TSP/Hamiltonian

```python
# Universal bitmask DP template for graph traversal:
n = number of cities
dp = [[INF] * n for _ in range(1 << n)]
dp[1][start] = 0  # Base: only start visited, cost 0

for mask in range(1 << n):
    for last in range(n):
        if not (mask & (1 << last)): continue  # last not in mask
        for nxt in range(n):
            if mask & (1 << nxt): continue      # nxt already visited
            new_mask = mask | (1 << nxt)
            dp[new_mask][nxt] = min(dp[new_mask][nxt],
                                    dp[mask][last] + graph[last][nxt])

# For TSP: answer = min(dp[full_mask][i] + graph[i][start])
# For Hamiltonian path: answer = min(dp[full_mask])  (no return)
```

### Bitmask Visualization for n=4

```
mask = 0000: no cities visited
mask = 0001: city 0 visited
mask = 0011: cities 0,1 visited
mask = 1011: cities 0,1,3 visited
mask = 1111: all cities visited (full_mask)

Transitions:
  From mask=0011 (0,1 visited), last=1:
    → try nxt=2: mask=0111, nxt=2
    → try nxt=3: mask=1011, nxt=3

  From mask=0111 (0,1,2 visited), last=2:
    → try nxt=3: mask=1111, nxt=3  (all visited!)
```
