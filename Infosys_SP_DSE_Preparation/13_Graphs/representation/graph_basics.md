# Graph Basics & Representations

## Graph Terminology

```
Graph G = (V, E)
V = set of vertices (nodes)
E = set of edges (connections)

Example:
    A --- B
    |   / |
    |  /  |
    C --- D

V = {A, B, C, D}
E = {(A,B), (A,C), (B,C), (B,D), (C,D)}
```

## Types of Graphs

| Type | Description | Example |
|------|-------------|---------|
| Undirected | Edges have no direction | A-B means A↔B |
| Directed | Edges have direction | A→B means only A to B |
| Weighted | Edges have weights/costs | A-B (weight=5) |
| Unweighted | All edges equal | A-B (no weight) |
| Cyclic | Contains at least one cycle | A→B→C→A |
| Acyclic | No cycles | Tree is a DAG |
| Connected | Path exists between every pair | Single component |
| Disconnected | Some pairs unreachable | Multiple components |

## Adjacency Matrix

```python
def create_adjacency_matrix(n, edges, directed=False):
    """
    n = number of vertices (0 to n-1)
    edges = list of [u, v] or [u, v, weight]
    """
    matrix = [[0] * n for _ in range(n)]
    
    for edge in edges:
        u, v = edge[0], edge[1]
        w = edge[2] if len(edge) > 2 else 1
        
        matrix[u][v] = w
        if not directed:
            matrix[v][u] = w
    
    return matrix


# Example usage
n = 5
edges = [[0, 1], [0, 4], [1, 2], [1, 3], [2, 3], [3, 4]]

# Undirected graph
matrix = create_adjacency_matrix(n, edges, directed=False)
for row in matrix:
    print(row)

# Output:
# [0, 1, 0, 0, 1]
# [1, 0, 1, 1, 0]
# [0, 1, 0, 1, 0]
# [0, 1, 1, 0, 1]
# [1, 0, 0, 1, 0]


# Weighted graph
weighted_edges = [[0, 1, 4], [0, 2, 1], [1, 3, 1], [2, 1, 2], [2, 3, 5]]
matrix_w = create_adjacency_matrix(4, weighted_edges, directed=True)
for row in matrix_w:
    print(row)

# Output:
# [0, 4, 1, 0]
# [0, 0, 0, 1]
# [0, 2, 0, 5]
# [0, 0, 0, 0]
```

## Adjacency List (Most Common)

```python
from collections import defaultdict

# Method 1: defaultdict(list) - Most Pythonic
def create_adj_list_defaultdict(n, edges, directed=False):
    graph = defaultdict(list)
    
    for u, v, *w in edges:
        weight = w[0] if w else 1
        graph[u].append((v, weight))
        if not directed:
            graph[v].append((u, weight))
    
    return graph


# Method 2: Simple dict of lists
def create_adj_list_dict(n, edges, directed=False):
    graph = {i: [] for i in range(n)}
    
    for u, v, *w in edges:
        weight = w[0] if w else 1
        graph[u].append((v, weight))
        if not directed:
            graph[v].append((u, weight))
    
    return graph


# Method 3: List of lists (for integer vertices 0 to n-1)
def create_adj_list_list(n, edges, directed=False):
    graph = [[] for _ in range(n)]
    
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    
    return graph


# Example usage
edges = [[0, 1], [0, 4], [1, 2], [1, 3], [2, 3], [3, 4]]

graph = create_adj_list_defaultdict(5, edges, directed=False)
print(dict(graph))
# {0: [1, 4], 1: [0, 2, 3], 2: [1, 3], 3: [1, 2, 4], 4: [0, 3]}

# For character vertices
edges_char = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]
graph_char = defaultdict(list)
for u, v in edges_char:
    graph_char[u].append(v)
    graph_char[v].append(u)

print(dict(graph_char))
# {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A', 'D'], 'D': ['B', 'C']}
```

## Edge List

```python
# Simplest representation - just store edges
def create_edge_list(edges):
    return edges


# Example
edges = [[0, 1, 4], [1, 2, 3], [2, 3, 1], [3, 0, 2]]
# Each element: [from, to, weight]

# Useful for Kruskal's MST algorithm
# Sort edges by weight
edges_sorted = sorted(edges, key=lambda x: x[2])
print(edges_sorted)
# [[2, 3, 1], [3, 0, 2], [1, 2, 3], [0, 1, 4]]
```

## Degree of Node

```python
# Degree = number of edges connected to a node
def find_degrees(n, edges, directed=False):
    if directed:
        in_deg = [0] * n
        out_deg = [0] * n
        for u, v in edges:
            out_deg[u] += 1
            in_deg[v] += 1
        return in_deg, out_deg
    else:
        degree = [0] * n
        for u, v in edges:
            degree[u] += 1
            degree[v] += 1
        return degree


# Undirected graph
edges = [[0, 1], [0, 4], [1, 2], [1, 3], [2, 3], [3, 4]]
degrees = find_degrees(5, edges, directed=False)
print(degrees)  # [2, 3, 2, 3, 2]

# Directed graph
edges_dir = [[0, 1], [0, 2], [1, 2], [2, 3]]
in_d, out_d = find_degrees(4, edges_dir, directed=True)
print(f"In-degree:  {in_d}")   # [0, 1, 2, 1]
print(f"Out-degree: {out_d}")  # [2, 1, 1, 0]
```

## Converting Between Representations

```python
from collections import defaultdict

# Edge List → Adjacency List
def edge_list_to_adj_list(edges, directed=False):
    graph = defaultdict(list)
    for u, v, *w in edges:
        weight = w[0] if w else 1
        graph[u].append((v, weight))
        if not directed:
            graph[v].append((u, weight))
    return graph


# Adjacency List → Edge List
def adj_list_to_edge_list(graph):
    edges = []
    visited = set()
    for u in graph:
        for v, w in graph[u]:
            edge = tuple(sorted([u, v]))
            if edge not in visited:
                visited.add(edge)
                edges.append([u, v, w])
    return edges


# Adjacency Matrix → Adjacency List
def adj_matrix_to_list(matrix, directed=False):
    graph = defaultdict(list)
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                graph[i].append((j, matrix[i][j]))
                if not directed and i != j:
                    graph[j].append((i, matrix[i][j]))
    return graph


# Adjacency List → Adjacency Matrix
def adj_list_to_matrix(graph, n):
    matrix = [[0] * n for _ in range(n)]
    for u in graph:
        for v, w in graph[u]:
            matrix[u][v] = w
    return matrix


# Example conversion
edges = [[0, 1, 5], [0, 2, 3], [1, 2, 1], [2, 3, 7]]

adj_list = edge_list_to_adj_list(edges, directed=False)
print(dict(adj_list))
# {0: [(1, 5), (2, 3)], 1: [(0, 5), (2, 1)], 2: [(0, 3), (1, 1), (3, 7)], 3: [(2, 7)]}

matrix = adj_list_to_matrix(adj_list, 4)
for row in matrix:
    print(row)
# [0, 5, 3, 0]
# [5, 0, 1, 0]
# [3, 1, 0, 7]
# [0, 0, 7, 0]
```

## When to Use Which Representation

| Representation | Space | Add Edge | Check Edge | Iterate Neighbors | Best For |
|---------------|-------|----------|------------|-------------------|----------|
| Adjacency Matrix | O(V²) | O(1) | O(1) | O(V) | Dense graphs, check if edge exists |
| Adjacency List | O(V+E) | O(1) | O(degree) | O(degree) | Sparse graphs, BFS/DFS |
| Edge List | O(E) | O(1) | O(E) | O(E) | Kruskal's MST |

```
Rule of thumb:
- Sparse graphs (E << V²) → Adjacency List
- Dense graphs (E ≈ V²) → Adjacency Matrix
- Need to check edge existence frequently → Adjacency Matrix
- Need to iterate neighbors → Adjacency List
- Kruskal's MST → Edge List
- Almost all LeetCode graph problems → Adjacency List (defaultdict)
```

## Graph Traversal Order

```python
from collections import defaultdict, deque

# Building graph from edges
edges = [[0, 1], [0, 2], [1, 3], [2, 4], [3, 5]]
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)

# Always sort neighbors for consistent traversal order
for node in graph:
    graph[node].sort()


# BFS - Level by level
def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


# DFS - Goes deep first
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    order = [node]
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            order.extend(dfs(graph, neighbor, visited))
    return order


print("BFS:", bfs(graph, 0))  # [0, 1, 2, 3, 4, 5]
print("DFS:", dfs(graph, 0))  # [0, 1, 3, 5, 2, 4]
```

## Key Takeaways for Infosys SP DSE

```
1. Default to adjacency list using defaultdict(list)
2. For grid problems, treat cell (i,j) as node with edges to neighbors
3. For weighted graphs, store (neighbor, weight) tuples
4. For directed graphs, only add edge u→v, not v→u
5. Always track visited to avoid infinite loops
6. Edge list is useful for sorting edges (Kruskal's MST)
7. Adjacency matrix useful for Floyd-Warshall (all-pairs shortest path)
```
