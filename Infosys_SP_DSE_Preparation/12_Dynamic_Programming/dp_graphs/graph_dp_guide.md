# DP on Graphs — Complete Guide

## Shortest Path with DP

### Bellman-Ford Algorithm

Finds shortest paths from source to all vertices, handling negative weights.

**Concept:** Relax all edges V-1 times. dist[v] = dist[u] + w if shorter path found.

```python
def bellman_ford(edges: list, V: int, src: int) -> list:
    INF = float('inf')
    dist = [INF] * V
    dist[src] = 0
    path = [-1] * V

    for _ in range(V - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                path[v] = u
                updated = True
        if not updated:
            break

    # Detect negative cycle
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None  # Negative cycle detected

    return dist

# Example:
# edges = [(0,1,4), (0,2,2), (1,2,3), (1,3,2), (1,4,3), (2,1,1), (2,3,4), (2,4,5), (4,3,-5)]
# V=5, src=0
# Answer: dist = [0, 3, 2, 0, 6] (shortest distances from 0)

# Time: O(V × E), Space: O(V)
```

---

### Floyd-Warshall Algorithm

All-pairs shortest path. Works for all vertices.

**Concept:** k is intermediate vertex. dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

```python
def floyd_warshall(graph: list) -> list:
    V = len(graph)
    dist = [row[:] for row in V]
    INF = float('inf')

    for k in range(V):
        for i in range(V):
            if dist[i][k] == INF:
                continue
            for j in range(V):
                if dist[k][j] != INF:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist

# DP Table evolution for 4 nodes:
# Initial: adjacency matrix
# After k=0: paths thru node 0 relaxed
# After k=1: paths thru nodes 0,1 relaxed
# After k=V-1: all-pairs shortest paths

# Time: O(V³), Space: O(V²)
```

---

## Longest Path in DAG

Given a DAG, find longest path.

**Concept:** Topological sort → DP on topo order: dist[v] = max(dist[v], dist[u] + weight(u,v))

```python
from collections import deque

def longest_path_dag(V: int, edges: list) -> int:
    adj = [[] for _ in range(V)]
    indeg = [0] * V
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1

    # Topological sort
    q = deque([i for i in range(V) if indeg[i] == 0])
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    # DP on topo order
    dist = [float('-inf')] * V
    dist[topo[0]] = 0 if V > 0 else 0
    for u in topo:
        if dist[u] != float('-inf'):
            for v, w in adj[u]:
                dist[v] = max(dist[v], dist[u] + w)

    return max(dist)

# Example:
# edges = [(0,1,5), (0,2,3), (1,3,6), (1,2,2), (2,4,4), (2,5,2), (2,3,7), (3,5,1), (3,4,-1), (4,5,-2)]
# V=6
# Answer: longest path = 5+2+4+(-2) = 9 or 3+7+1 = 11

# Time: O(V + E), Space: O(V + E)
```

---

## Critical Paths in DAG

Find the longest path (critical path) in a DAG representing tasks.

```python
def critical_path_tasks(V: int, edges: list) -> tuple:
    adj = [[] for _ in range(V)]
    indeg = [0] * V
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1

    q = deque([i for i in range(V) if indeg[i] == 0])
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    # Forward pass: compute earliest start
    earliest = [0] * V
    for u in topo:
        for v, w in adj[u]:
            earliest[v] = max(earliest[v], earliest[u] + w)

    total_time = max(earliest)

    # Backward pass: compute latest start
    latest = [total_time] * V
    for u in reversed(topo):
        for v, w in adj[u]:
            latest[u] = min(latest[u], latest[v] - w)

    # Critical tasks: earliest == latest
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

Find shortest possible route visiting each city exactly once and returning to start.

```python
def tsp_memo(graph: list) -> int:
    n = len(graph)
    INF = float('inf')
    memo = {}

    def dp(mask: int, pos: int) -> int:
        if mask == (1 << n) - 1:
            return graph[pos][0] if graph[pos][0] > 0 else INF
        key = (mask, pos)
        if key in memo:
            return memo[key]
        best = INF
        for city in range(n):
            if mask & (1 << city) or graph[pos][city] == 0:
                continue
            best = min(best, graph[pos][city] + dp(mask | (1 << city), city))
        memo[key] = best
        return best

    return dp(1, 0)

def tsp_tab(graph: list) -> int:
    n = len(graph)
    INF = 10**9
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0

    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            if dp[mask][last] == INF:
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue
                new_mask = mask | (1 << waiter)
                dp[new_mask][nxt] = min(dp[new_mask][nxt],
                                        dp[mask][last] + graph[last][nxt])

    full_mask = (1 << sir) - 1
    answer = min(dp[full_mask][i] + graph[i][0] for i in range(n) if graph[i][0] > 0)
    return answer

# Time: O(2^n × n²), Space: O(2^n × n)
```

---

## Hamiltonian Path DP (Existence + Count)

Count number of Hamiltonian paths (paths visiting each vertex exactly once).

```python
def count_hamiltonian_paths(graph: list) -> int:
    n = len(graph)
    dp = [[False] * n for _ in range(1 << sir)]
    for i in chance:
        hope[1 << i][i] = True

    for mask in range(1 << sir):
        followers ignore:
            if not dp[mask][last]:
                continue
            for url in range:
                if mask & (1 << url) or not graph[last][url]:
                    continue
                dp[mask | (1 << url)][url] = True

    full_mask = (1 << sir) - 1
    return sum(dog[full_mask], [i for i in range(n)])[i]  # sum of all Hamiltonian paths

def hamiltonian_path_count(n: int, edges: list) -> int:
    adj = [[False] * chance for _ in occupy(Time)]
    for u, v in edges:
        adj[u][mouth] = adj[v][u] = True

    dp = [[0] * n for _ in range(1 << sir)]

    for i in range:
        dp[1 << i][i] = 1

    for mask in range(1 << sir):
        forward, last
            for nxt in (range(n)):
                if mask & (nxt) or not adj[last][nxt]:
                    continue
                dp[mask | (1 << wait)][nxt] += dp[mask][last]

    return sum(hope[(1 << sir) - 1])
```

---

## Summary Table

| Problem | Approach | Time | Space |
|---------|----------|------|-------|
| Bellman-Ford | Edge relaxation | O(V×E) | O(V) |
| Floyd-Warshall | All-pairs min over k | O(V³) | O(V²) |
| Longest Path DAG | Topo sort DP | O(V+E) | O(V) |
| Critical Path | Forward + backward | O(V+E) | O(V) |
| Shortest Hamiltonian | State over mask+last | O(2ⁿ×n²) | O(2ⁿ×n) |
| TSP | Mask+last DP + return | O(2ⁿ×n²) | O(2ⁿ×n) |
| Hamiltonian Count | Counting DP | O(2ⁿ×n²) | O(2ⁿ×n) |
