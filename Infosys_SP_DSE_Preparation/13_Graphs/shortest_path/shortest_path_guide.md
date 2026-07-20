# Shortest Path Algorithms Guide

## Dijkstra's Algorithm (Min Heap)

```python
import heapq
from collections import defaultdict

def dijkstra(graph, start, n):
    """
    Dijkstra's algorithm - Single source shortest path
    Works with non-negative weights only
    Time: O((V + E) log V) | Space: O(V + E)
    
    graph: dict of {node: [(neighbor, weight), ...]}
    """
    dist = {i: float('inf') for i in range(n)}
    dist[start] = 0
    prev = {i: -1 for i in range(n)}
    
    # Min heap: (distance, node)
    heap = [(0, start)]
    
    while heap:
        d, node = heapq.heappop(heap)
        
        # Skip if we already found a shorter path
        if d > dist[node]:
            continue
        
        for neighbor, weight in graph[node]:
            new_dist = dist[node] + weight
            
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = node
                heapq.heappush(heap, (new_dist, neighbor))
    
    return dist, prev


# Reconstruct path from start to target
def reconstruct_path(prev, start, target):
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

```python
def bellman_ford(n, edges, start):
    """
    Bellman-Ford - Single source shortest path
    Works with negative weights, detects negative cycles
    Time: O(V * E) | Space: O(V)
    """
    dist = [float('inf')] * n
    dist[start] = 0
    prev = [-1] * n
    
    # Relax edges V-1 times
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                updated = True
        
        if not updated:
            break  # Early termination
    
    # Check for negative cycle
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

## Floyd-Warshall Algorithm

```python
def floyd_warshall(n, edges):
    """
    Floyd-Warshall - All pairs shortest path
    Works with negative weights, detects negative cycles
    Time: O(V³) | Space: O(V²)
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
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Check for negative cycle
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
| Algorithm | Time | Space | Negative Weights | Use Case |
|-----------|------|-------|------------------|----------|
| Dijkstra | O((V+E)logV) | O(V+E) | No | Sparse graph, single source |
| Bellman-Ford | O(VE) | O(V) | Yes | Negative weights, detect negative cycle |
| Floyd-Warshall | O(V³) | O(V²) | Yes | All pairs, dense graph |
| 0-1 BFS | O(V+E) | O(V) | No | Weights are 0 or 1 |
| DAG Shortest | O(V+E) | O(V+E) | Yes | DAG, most efficient |
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
```
