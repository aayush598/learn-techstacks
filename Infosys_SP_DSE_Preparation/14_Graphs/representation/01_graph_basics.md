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

## Types of Graphs — Visual Guide

### Undirected vs Directed Graphs

```
  UNDIRECTED GRAPH              DIRECTED GRAPH (Digraph)
  (edges go both ways)          (edges have arrows)

      A --- B                       A --> B
      |   / |                       ^   / |
      |  /  |                       |  /  v
      C --- D                       C <-- D

  Edge (A,B) means               Edge A-->B means
  A can reach B AND              A can reach B
  B can reach A                  BUT B cannot reach A
```

### Weighted vs Unweighted Graphs

```
  UNWEIGHTED GRAPH              WEIGHTED GRAPH
  (all edges equal)             (each edge has a cost)

      A --- B                       A --5-- B
      |   / |                       |      /|
      |  /  |                       3    2/ |4
      C --- D                       |  /    |
                                    C --1-- D

  Just connectivity matters      Cost of path matters
  BFS gives shortest path        Need Dijkstra's/Bellman-Ford
```

### Cyclic vs Acyclic Graphs

```
  CYCLIC GRAPH                  ACYCLIC GRAPH (DAG)
  (has at least one cycle)      (Directed Acyclic Graph)

      A --> B                        A --> B
      ^     |                        |     |
      |     v                        v     v
      C <-- D                        C --> D

  A → B → D → C → A             No path leads back
  is a CYCLE!                    to where it started
```

### Connected vs Disconnected Graphs

```
  CONNECTED GRAPH               DISCONNECTED GRAPH
  (one piece)                   (multiple components)

      A --- B                     A --- B
      |   / |                     |
      |  /  |                     |
      C --- D                     C --- D

  You can get from              You CANNOT get from
  ANY node to ANY other         A to C or D
  node                           Components: {A,B}, {C,D}
```

## Types of Graphs — Summary Table

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

### Special Graph Types

```
TREE (special DAG)               COMPLETE GRAPH (K_n)
  Every pair connected,            Every node connected
  exactly V-1 edges,               to every other node
  no cycles                        E = V*(V-1)/2 edges

       1                               1
      / \                            / | \
     2   3                          2--+--3
    / \   \                         | / \| 
   4   5   6                        4--+--5

V=6, E=5 (V-1)                  V=5, E=10 (5*4/2)
```

## Adjacency Matrix

### Visual: How an Adjacency Matrix Works

```
Graph:           Adjacency Matrix (matrix[i][j] = weight or 1):

  0 --- 1           0   1   2   3   4
  |   / |       ┌───────────────────────┐
  |  /  |     0 │ 0 │ 1 │ 0 │ 0 │ 1 │  ← Node 0 connects to 1 and 4
  | /   |       ├───────────────────────┤
  2 --- 3     1 │ 1 │ 0 │ 1 │ 1 │ 0 │  ← Node 1 connects to 0, 2, 3
      |         ├───────────────────────┤
      4       2 │ 0 │ 1 │ 0 │ 1 │ 0 │  ← Node 2 connects to 1, 3
                ├───────────────────────┤
              3 │ 0 │ 1 │ 1 │ 0 │ 1 │  ← Node 3 connects to 1, 2, 4
                ├───────────────────────┤
              4 │ 1 │ 0 │ 0 │ 1 │ 0 │  ← Node 4 connects to 0, 3
                └───────────────────────┘
                  ↑
            For undirected graphs, matrix is SYMMETRIC
            matrix[i][j] == matrix[j][i] (mirror along diagonal)
```

### Reading the Matrix

```
To check if edge exists between node i and j:
  → Just look at matrix[i][j] — O(1)!

To find all neighbors of node i:
  → Scan entire row matrix[i] — O(V)

Example: Is there an edge from node 1 to node 3?
  → matrix[1][3] = 1 → YES!

Example: What are all neighbors of node 2?
  → Row 2: [0, 1, 0, 1, 0]
  → Neighbors: nodes 1 and 3
```

### Weighted Directed Graph Matrix

```
Graph with weights:       Weighted Matrix:

  0 --4--> 1              0   1   2   3
  |        |          ┌──────────────────┐
  1        1        0 │ 0 │ 4 │ 1 │ 0 │
  |        v          ├──────────────────┤
  v   +2   3        1 │ 0 │ 0 │ 0 │ 1 │
  2 ------>          ├──────────────────┤
     5               2 │ 0 │ 2 │ 0 │ 5 │
                       ├──────────────────┤
                     3 │ 0 │ 0 │ 0 │ 0 │
                       └──────────────────┘
  matrix[0][1] = 4 (edge 0→1 has weight 4)
  matrix[2][1] = 2 (edge 2→1 has weight 2)
  matrix[1][0] = 0 (NO edge from 1→0)
```

```python
def create_adjacency_matrix(n, edges, directed=False):
    """
    n = number of vertices (0 to n-1)
    edges = list of [u, v] or [u, v, weight]

    HOW IT WORKS:
    1. Create an n×n matrix filled with zeros
    2. For each edge (u, v), set matrix[u][v] = weight
    3. If undirected, also set matrix[v][u] = weight (symmetric)
    """
    # Step 1: Initialize n×n matrix with zeros
    matrix = [[0] * n for _ in range(n)]

    # Step 2: Fill in the edges
    for edge in edges:
        u, v = edge[0], edge[1]
        w = edge[2] if len(edge) > 2 else 1

        matrix[u][v] = w        # Always set u→v
        if not directed:
            matrix[v][u] = w    # Also set v→u for undirected

    return matrix


# Example: Undirected graph
n = 5
edges = [[0, 1], [0, 4], [1, 2], [1, 3], [2, 3], [3, 4]]

matrix = create_adjacency_matrix(n, edges, directed=False)
for row in matrix:
    print(row)

# Output:
# [0, 1, 0, 0, 1]   ← row 0: node 0 → neighbors 1, 4
# [1, 0, 1, 1, 0]   ← row 1: node 1 → neighbors 0, 2, 3
# [0, 1, 0, 1, 0]   ← row 2: node 2 → neighbors 1, 3
# [0, 1, 1, 0, 1]   ← row 3: node 3 → neighbors 1, 2, 4
# [1, 0, 0, 1, 0]   ← row 4: node 4 → neighbors 0, 3


# Example: Weighted directed graph
weighted_edges = [[0, 1, 4], [0, 2, 1], [1, 3, 1], [2, 1, 2], [2, 3, 5]]
matrix_w = create_adjacency_matrix(4, weighted_edges, directed=True)
for row in matrix_w:
    print(row)

# Output:
# [0, 4, 1, 0]   ← 0→1 (weight 4), 0→2 (weight 1)
# [0, 0, 0, 1]   ← 1→3 (weight 1)
# [0, 2, 0, 5]   ← 2→1 (weight 2), 2→3 (weight 5)
# [0, 0, 0, 0]   ← 3 has no outgoing edges
```

## Adjacency List (Most Common)

### Visual: How an Adjacency List Works

```
Same Graph:                Adjacency List (array of lists):

  0 --- 1                 Index │ Neighbors
  |   / |                 ──────┼──────────────────
  |  /  |                   0   │ [1, 4]
  | /   |                   1   │ [0, 2, 3]
  2 --- 3                   2   │ [1, 3]
      |                     3   │ [1, 2, 4]
      4                     4   │ [0, 3]

For weighted graphs, store tuples:
  Index │ Neighbors (with weights)
  ──────┼─────────────────────────
    0   │ [(1, w01), (4, w04)]
    1   │ [(0, w01), (2, w12), (3, w13)]
    ...
```

### Why Adjacency List is Preferred

```
ADJACENCY LIST vs MATRIX — Memory comparison:

  Graph with V=5, E=6 (sparse):
  ┌─────────────────────────────────────────┐
  │ Adjacency Matrix: V² = 25 cells         │
  │   Many zeros (wasted space)             │
  │                                         │
  │ Adjacency List: V+E = 11 entries        │
  │   Only stores existing edges            │
  └─────────────────────────────────────────┘

  Rule: If E << V², use adjacency list!
  (Most LeetCode problems have sparse graphs)
```

```python
from collections import defaultdict

# Method 1: defaultdict(list) - Most Pythonic
def create_adj_list_defaultdict(n, edges, directed=False):
    """
    Uses defaultdict so we never get KeyError.
    Each key maps to a list of (neighbor, weight) tuples.
    """
    graph = defaultdict(list)

    for u, v, *w in edges:
        weight = w[0] if w else 1
        graph[u].append((v, weight))
        if not directed:
            graph[v].append((u, weight))

    return graph


# Method 2: Simple dict of lists
def create_adj_list_dict(n, edges, directed=False):
    """
    Explicitly initialize all n nodes (safer for iteration).
    Use this when you need to iterate ALL nodes, not just those with edges.
    """
    graph = {i: [] for i in range(n)}

    for u, v, *w in edges:
        weight = w[0] if w else 1
        graph[u].append((v, weight))
        if not directed:
            graph[v].append((u, weight))

    return graph


# Method 3: List of lists (for integer vertices 0 to n-1)
def create_adj_list_list(n, edges, directed=False):
    """
    Fastest option when vertices are integers 0..n-1.
    No hashing overhead, direct index access.
    """
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

### Traversal Comparison

```
BFS (Queue) — Level by Level:       DFS (Stack) — Go Deep First:

        0                                 0
       / \                               / \
      1   2                             1   2
     / \   \                           / \   \
    3   4   5                         3   4   5

  Visit order:                      Visit order:
  Level 0:  [0]                     Go deep: 0→1→3→back→4→back→back→2→5
  Level 1:  [1, 2]
  Level 2:  [3, 4, 5]
  Result:   [0, 1, 2, 3, 4, 5]     Result:   [0, 1, 3, 4, 2, 5]
```

## Edge List

### Visual: Edge List Representation

```
Graph:                      Edge List (just store edges):

  0 --4--> 1               [[0, 1, 4],    ← from, to, weight
  |        |                [1, 2, 3],
  1        1                [2, 3, 1],
  |        v                [3, 0, 2]]
  v   +2   3
  2 ------>              Simplest representation!
                          Just a list of all edges.
                          Perfect for Kruskal's MST!
```

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

### Visual: Understanding Degree

```
UNDIRECTED GRAPH:              DIRECTED GRAPH:
Degree = # edges                In-degree = # incoming edges
connected to node               Out-degree = # outgoing edges

      0 --- 1                       0 --> 1
      |   / |                       ^    /
      |  /  |                       |   /
      | /   |                       |  v
      2 --- 3                       2 --> 3

  degree[0] = 2 (edges to 1,2)   Node │ In │ Out
  degree[1] = 3 (edges to 0,2,3) ─────┼────┼─────
  degree[2] = 3 (edges to 0,1,3)   0   │  0 │  1  (no in, 1 out)
  degree[3] = 2 (edges to 1,2)     1   │  1 │  1  (1 in, 1 out)
                                      2   │  1 │  1  (1 in, 1 out)
Sum of degrees = 2 * E              3   │  1 │  0  (1 in, no out)
(The Handshaking Lemma)
```

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

### Visual: Conversion Map

```
                    ┌──────────────────────┐
                    │     EDGE LIST        │
                    │ (simplest, just      │
                    │  [u, v, w] tuples)   │
                    └──────────┬───────────┘
                               │
               ┌───────────────┼───────────────┐
               │               │               │
               ▼               ▼               │
     ┌─────────────────┐  ┌──────────────┐    │
     │ ADJACENCY LIST  │  │  ADJACENCY   │    │
     │ (most common)   │◄─┤   MATRIX     │    │
     │ defaultdict     │──►│  (V×V array) │    │
     │ {node: [nbrs]}  │  └──────────────┘    │
     └─────────────────┘        ▲              │
               │                │              │
               └────────────────┼──────────────┘
                                │
                    Best for:   │
                    - BFS/DFS   │
                    - Sparse    │
                    - Default   │
```

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
Decision Flowchart — Which representation should I use?

         START
           │
           ▼
    ┌──────────────┐     YES    ┌──────────────────────┐
    │ E << V² ?    ├───────────►│ Use ADJACENCY LIST   │
    │ (sparse?)    │            │ (default choice)     │
    └──────┬───────┘            └──────────────────────┘
           │ NO
           ▼
    ┌──────────────┐     YES    ┌──────────────────────┐
    │ Need O(1)    ├───────────►│ Use ADJACENCY MATRIX │
    │ edge check?  │            │                      │
    └──────┬───────┘            └──────────────────────┘
           │ NO
           ▼
    ┌──────────────┐     YES    ┌──────────────────────┐
    │ Kruskal's    ├───────────►│ Use EDGE LIST        │
    │ MST?         │            │ (sort by weight)     │
    └──────┬───────┘            └──────────────────────┘
           │ NO
           ▼
    ┌──────────────────────────────────────────────┐
    │ Default: Use ADJACENCY LIST (defaultdict)   │
    │ Works for 95% of LeetCode graph problems     │
    └──────────────────────────────────────────────┘

Rule of thumb:
- Sparse graphs (E << V²) → Adjacency List
- Dense graphs (E ≈ V²) → Adjacency Matrix
- Need to check edge existence frequently → Adjacency Matrix
- Need to iterate neighbors → Adjacency List
- Kruskal's MST → Edge List
- Almost all LeetCode graph problems → Adjacency List (defaultdict)
```

## Graph Traversal Order

### Visual: BFS vs DFS Step-by-Step

```
Graph (sorted neighbors):
    0 → [1, 2]
    1 → [0, 3, 4]
    2 → [0, 4]
    3 → [1, 5]
    4 → [1, 2]
    5 → [3]

            0
           / \
          1   2
         / \   \
        3   4---+
        |
        5

BFS from 0 (level by level using QUEUE):
═══════════════════════════════════════════════════════
Step │ Queue       │ Pop  │ Visit         │ Result
═════│═════════════│══════│═══════════════│══════════
  1  │ [0]         │  0   │ {0}           │ [0]
  2  │ [1, 2]      │  1   │ {0,1}         │ [0, 1]
  3  │ [2, 3, 4]   │  2   │ {0,1,2}       │ [0, 1, 2]
  4  │ [3, 4, 4]   │  3   │ {0,1,2,3}     │ [0, 1, 2, 3]
  5  │ [4, 4, 5]   │  4   │ {0,1,2,3,4}   │ [0, 1, 2, 3, 4]
  6  │ [4, 5]      │  5   │ {0,1,2,3,4,5} │ [0, 1, 2, 3, 4, 5]

BFS Order: [0, 1, 2, 3, 4, 5]
  Level 0: 0
  Level 1: 1, 2
  Level 2: 3, 4, 5

DFS from 0 (go deep using STACK/recursion):
═══════════════════════════════════════════════════════
Step │ Stack       │ Pop  │ Visit         │ Result
═════│═════════════│══════│═══════════════│══════════
  1  │ [0]         │  0   │ {0}           │ [0]
  2  │ [2, 1]      │  1   │ {0,1}         │ [0, 1]
  3  │ [2, 4, 3]   │  3   │ {0,1,3}       │ [0, 1, 3]
  4  │ [2, 4, 5]   │  5   │ {0,1,3,5}     │ [0, 1, 3, 5]
  5  │ [2, 4]      │  4   │ {0,1,3,5,4}   │ [0, 1, 3, 5, 4]
  6  │ [2]         │  2   │ {all}         │ [0, 1, 3, 5, 4, 2]

DFS Order: [0, 1, 3, 5, 4, 2]
  Goes deep: 0 → 1 → 3 → 5 (dead end, backtrack)
  Then: → 4 (dead end, backtrack) → 2
```

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
        node = queue.popleft()         # O(1) from left of deque
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

### Grid Representation — Converting 2D Grid to Graph

```
Grid problems = graph problems in disguise!
Each cell (r, c) is a NODE. Neighbors are adjacent cells.

  Grid:                        Graph:
  ┌───┬───┬───┬───┐           (0,0)──(0,1)──(0,2)──(0,3)
  │ 0 │ 1 │ 2 │ 3 │           │      │      │      │
  ├───┼───┼───┼───┤           (1,0)──(1,1)──(1,2)──(1,3)
  │ 4 │ 5 │ 6 │ 7 │           │      │      │      │
  ├───┼───┼───┼───┤           (2,0)──(2,1)──(2,2)──(2,3)
  │ 8 │ 9 │10 │11 │
  └───┴───┴───┴───┘

  Cell (1,1) has neighbors: (0,1), (2,1), (1,0), (1,2)
  Use directions: [(-1,0),(1,0),(0,-1),(0,1)]

  4-directional:          8-directional (includes diagonals):
       ↑                        ↖ ↑ ↗
    ←  ·  →                   ←  ·  →
       ↓                        ↙ ↓ ↘
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
