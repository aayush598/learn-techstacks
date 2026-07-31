# Advanced Graph Concepts

## Bipartite Graph Checking

### Visual: What is a Bipartite Graph?

```
BIPARTITE GRAPH: Can be colored with 2 colors such that
NO two adjacent nodes have the same color.

Equivalently: Can split all nodes into two groups where
every edge goes BETWEEN groups (never within a group).

  BIPARTITE ✓               NOT BIPARTITE ✗
  (2-colorable)             (has odd cycle)

  Color A: {0, 2}           0 --- 1
  Color B: {1, 3}           |   / |

  0 --- 1                   This is a triangle (odd cycle)
  |   / |                   You CANNOT 2-color a triangle:
  |  /  |                   If 0=R, 1=B, then 2 needs to be
  2 --- 3                   both R (for edge 0-2) and B
                            (for edge 1-2) — IMPOSSIBLE!

  0(R) -- 1(B)              THEOREM: A graph is bipartite
       \  /                 IFF it has no odd-length cycles.
        2(R) -- 3(B)

Key Insight:
  BFS/DFS coloring: Start with color 0, alternate 0↔1.
  If you ever try to color a node with the same color
  as an already-colored neighbor → NOT bipartite!
```

```python
def is_bipartite(graph):
    """
    LeetCode 785 - Check if graph is bipartite
    Can be colored with 2 colors such that no adjacent nodes have same color
    Time: O(V + E) | Space: O(V)

    ALGORITHM:
    1. Try to 2-color the graph using DFS
    2. Start each component with color 0
    3. Color all neighbors with alternate color (1 - c)
    4. If conflict found → not bipartite
    """
    n = len(graph)
    color = [-1] * n   # -1 = uncolored, 0 = color A, 1 = color B

    def dfs(node, c):
        color[node] = c
        for neighbor in graph[node]:
            if color[neighbor] == c:
                return False   # Same color as neighbor = NOT bipartite
            if color[neighbor] == -1:
                if not dfs(neighbor, 1 - c):   # Alternate color
                    return False
        return True

    for i in range(n):
        if color[i] == -1:
            if not dfs(i, 0):
                return False
    return True


# BFS approach
def is_bipartite_bfs(graph):
    n = len(graph)
    color = [-1] * n
    from collections import deque

    for i in range(n):
        if color[i] != -1:
            continue

        queue = deque([i])
        color[i] = 0

        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if color[neighbor] == color[node]:
                    return False
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]   # Flip color
                    queue.append(neighbor)
    return True


# Check if graph can be colored with k colors
def is_k_colorable(graph, k):
    """Returns True if graph is k-colorable"""
    n = len(graph)
    color = [-1] * n

    def is_safe(node, c):
        for neighbor in graph[node]:
            if color[neighbor] == c:
                return False
        return True

    def graph_coloring(node):
        if node == n:
            return True

        for c in range(k):
            if is_safe(node, c):
                color[node] = c
                if graph_coloring(node + 1):
                    return True
                color[node] = -1   # Backtrack

        return False

    return graph_coloring(0)


# Example
graph = [[1, 3], [0, 2], [1, 3], [0, 2]]  # Bipartite: {0,2} and {1,3}
print(is_bipartite(graph))  # True

graph = [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]  # Not bipartite
print(is_bipartite(graph))  # False
```

## Strongly Connected Components (Kosaraju's Algorithm)

### Visual: What are SCCs?

```
STRONGLY CONNECTED COMPONENT (SCC):
  A maximal set of nodes where EVERY node can reach EVERY other node
  (via directed edges).

  Example:
  ┌──────────┐     ┌──────────┐
  │  0 → 1   │────►│  3 → 4   │
  │  ↑   ↓   │     │  ↑   ↓   │
  │  2 → 0   │     │  5 → 3   │
  └──────────┘     └──────────┘
     SCC 1             SCC 2

  In SCC1: 0 can reach 1,2 and 1 can reach 0,2 etc.
  But NO node in SCC1 can reach SCC2... wait, there IS an edge 1→3.
  And SCC2 can't reach SCC1. So SCC1 and SCC2 are separate SCCs.

KOSARAJU'S ALGORITHM (2 DFS passes):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pass 1: DFS on ORIGINAL graph → get finish order
Pass 2: DFS on REVERSE graph in REVERSE finish order → get SCCs

WHY IT WORKS:
  - Pass 1: Nodes that finish LAST are in the "source" SCC
    (the one with no incoming edges from other SCCs)
  - Reverse graph + reverse order = start from sink SCC
  - DFS on reverse graph from sink = find all nodes in that SCC
  - Each DFS in pass 2 finds exactly ONE SCC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```python
from collections import defaultdict

def kosaraju_scc(n, edges):
    """
    Find all Strongly Connected Components using Kosaraju's algorithm
    Time: O(V + E) | Space: O(V + E)

    TWO-PASS ALGORITHM:
    Pass 1: DFS on original graph → nodes added to "order" after all
            descendants are processed (like topo sort)
    Pass 2: DFS on reversed graph, processing nodes in reverse of
            "order" → each DFS tree in pass 2 = one SCC
    """
    # Step 1: Build original graph and reverse graph
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)

    for u, v in edges:
        graph[u].append(v)
        reverse_graph[v].append(u)   # Reversed!

    # Step 2: Get finish order using DFS on original graph
    visited = [False] * n
    order = []

    def dfs1(node):
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs1(neighbor)
        order.append(node)   # Add AFTER all descendants

    for i in range(n):
        if not visited[i]:
            dfs1(i)

    # Step 3: DFS on reverse graph in REVERSE finish order
    visited = [False] * n
    sccs = []

    def dfs2(node, component):
        visited[node] = True
        component.append(node)
        for neighbor in reverse_graph[node]:
            if not visited[neighbor]:
                dfs2(neighbor, component)

    for node in reversed(order):   # Process in reverse finish order
        if not visited[node]:
            component = []
            dfs2(node, component)
            sccs.append(component)

    return sccs


# Tarjan's SCC (one pass — more efficient)
def tarjan_scc(n, edges):
    """
    Find SCCs using Tarjan's algorithm (single DFS)
    Time: O(V + E) | Space: O(V)

    Uses "lowlink" values to detect SCCs in one pass.
    lowlink[v] = smallest index reachable from v in DFS tree
    If lowlink[v] == index[v], v is the root of an SCC
    """
    from collections import defaultdict

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    on_stack = {}
    sccs = []

    def strongconnect(node):
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        on_stack[node] = True

        for neighbor in graph[node]:
            if neighbor not in index:
                strongconnect(neighbor)
                lowlink[node] = min(lowlink[node], lowlink[neighbor])
            elif on_stack.get(neighbor, False):
                lowlink[node] = min(lowlink[node], index[neighbor])

        # If node is root of an SCC
        if lowlink[node] == index[node]:
            component = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                component.append(w)
                if w == node:
                    break
            sccs.append(component)

    for i in range(n):
        if i not in index:
            strongconnect(i)

    return sccs


# Example
edges = [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 5], [5, 3]]
print(kosaraju_scc(6, edges))  # [[0, 1, 2], [3, 4, 5]]
print(tarjan_scc(6, edges))    # [[5, 4, 3], [2, 1, 0]] or similar
```

## Articulation Points

### Visual: What are Articulation Points?

```
ARTICULATION POINT (Cut Vertex):
  A node whose removal DISCONNECTS the graph.

  Graph:                    Remove node 2:
  0 --- 1 --- 2 --- 3       0 --- 1     3 --- 4
        |           |               ↑           ↑
        +--- 4 -----+               +-----------+
        
  Node 2 is an articulation point!
  Without it, {0,1,4} and {3,4} become separate.

HOW TO FIND THEM (DFS with disc/low):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  disc[u] = discovery time of u (when DFS first visits u)
  low[u]  = earliest discovered node reachable from u
            via back edges in DFS subtree

  A node u is an articulation point if:
  1. u is ROOT of DFS tree and has > 1 child
     (removing root disconnects its children)
  2. u is NOT root and has a child v where
     low[v] >= disc[u]
     (v's subtree has NO back edge to an ancestor of u,
      so removing u disconnects v's subtree)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```python
from collections import defaultdict

def find_articulation_points(n, edges):
    """
    Find all articulation points (cut vertices)
    Removing them disconnects the graph
    Time: O(V + E) | Space: O(V)

    disc[u] = when DFS first visits u
    low[u]  = min(disc[u], min disc of nodes reachable via back edges)

    Two conditions for articulation point:
    1. Root with > 1 child
    2. Non-root where low[child] >= disc[parent]
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n
    disc = [0] * n   # Discovery time
    low = [0] * n    # Lowest reachable ancestor
    parent = [-1] * n
    ap = set()
    timer = [0]

    def dfs(node):
        visited[node] = True
        disc[node] = low[node] = timer[0]
        timer[0] += 1
        children = 0

        for neighbor in graph[node]:
            if not visited[neighbor]:
                children += 1
                parent[neighbor] = node
                dfs(neighbor)

                low[node] = min(low[node], low[neighbor])

                # Condition 1: Root with more than 1 child
                if parent[node] == -1 and children > 1:
                    ap.add(node)

                # Condition 2: Non-root where low[neighbor] >= disc[node]
                if parent[node] != -1 and low[neighbor] >= disc[node]:
                    ap.add(node)

            elif neighbor != parent[node]:
                # Back edge to ancestor
                low[node] = min(low[node], disc[neighbor])

    for i in range(n):
        if not visited[i]:
            dfs(i)

    return sorted(list(ap))


# Example
edges = [[0, 1], [0, 2], [1, 2], [2, 3]]
print(find_articulation_points(4, edges))  # [2]
```

## Bridges in Graph

### Visual: What are Bridges?

```
BRIDGE (Cut Edge):
  An edge whose removal DISCONNECTS the graph.

  Graph:                    Remove edge (1,3):
  0 --- 1 --- 3 --- 4       0 --- 1   3 --- 4
        |           |              ↑   ↑
        +--- 2 -----+              +---+

  Edge (1,3) is a bridge!
  Removing it disconnects {0,1,2} from {3,4}.

  Note: Edge (0,1) is NOT a bridge because even after
  removing it, 0 can still reach 1 via 0→2→1.

HOW TO FIND BRIDGES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Same DFS as articulation points, but different condition:

  Edge (u, v) is a bridge if:
    low[v] > disc[u]

  Meaning: v's subtree has NO back edge to u or any
  ancestor of u. So removing edge (u,v) disconnects them.

  NOTE THE DIFFERENCE:
  Articulation point: low[v] >= disc[u]  (>=)
  Bridge:             low[v] > disc[u]   (strict >)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```python
from collections import defaultdict

def find_bridges(n, edges):
    """
    Find all bridges (cut edges)
    Removing them disconnects the graph
    Time: O(V + E) | Space: O(V)

    Bridge condition: low[v] > disc[u]
    (strictly greater than — no back edge from v's subtree to u)
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n
    disc = [0] * n
    low = [0] * n
    parent = [-1] * n
    bridges = []
    timer = [0]

    def dfs(node):
        visited[node] = True
        disc[node] = low[node] = timer[0]
        timer[0] += 1

        for neighbor in graph[node]:
            if not visited[neighbor]:
                parent[neighbor] = node
                dfs(neighbor)

                low[node] = min(low[node], low[neighbor])

                # Bridge condition: no back edge from subtree
                if low[neighbor] > disc[node]:   # STRICTLY greater!
                    bridges.append([node, neighbor])

            elif neighbor != parent[node]:
                low[node] = min(low[node], disc[neighbor])

    for i in range(n):
        if not visited[i]:
            dfs(i)

    return bridges


# Example
edges = [[0, 1], [1, 2], [2, 0], [1, 3]]
print(find_bridges(4, edges))  # [[1, 3]]
```

## Euler Path and Circuit

```python
from collections import defaultdict

def has_euler_path(n, edges):
    """
    Check if graph has Euler path or circuit
    Time: O(V + E) | Space: O(V)
    """
    graph = defaultdict(list)
    degree = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        degree[u] += 1
        degree[v] += 1
    
    # Count odd degree vertices
    odd_count = sum(1 for d in degree if d % 2 == 1)
    
    # Check connectivity
    visited = set()
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
    
    # Find first vertex with non-zero degree
    start = -1
    for i in range(n):
        if degree[i] > 0:
            start = i
            break
    
    if start != -1:
        dfs(start)
        # Check all edges are reachable
        for i in range(n):
            if degree[i] > 0 and i not in visited:
                return False, False  # Not connected
    
    # Euler circuit: all even degrees
    # Euler path: exactly 0 or 2 odd degrees
    if odd_count == 0:
        return True, True   # Has Euler circuit
    elif odd_count == 2:
        return True, False  # Has Euler path
    else:
        return False, False


# Hierholzer's Algorithm - Find Euler Path/Circuit
def hierholzer(n, edges):
    """
    Find Euler path or circuit using Hierholzer's algorithm
    Time: O(E) | Space: O(E)
    """
    graph = defaultdict(list)
    degree = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        degree[u] += 1
        degree[v] += 1
    
    # Find start vertex
    start = 0
    for i in range(n):
        if degree[i] % 2 == 1:
            start = i
            break
    
    # Hierholzer's algorithm
    stack = [start]
    path = []
    
    while stack:
        node = stack[-1]
        
        if graph[node]:
            neighbor = graph[node].pop()
            # Remove reverse edge
            graph[neighbor].remove(node)
            stack.append(neighbor)
        else:
            path.append(stack.pop())
    
    # Check if all edges were used
    total_edges = sum(len(v) for v in graph.values())
    
    if total_edges == 0:
        return path[::-1]  # Reverse to get correct order
    else:
        return []  # Not all edges visited


# Example
edges = [[0, 1], [1, 2], [2, 0], [0, 3], [3, 4], [4, 0]]
has_path, has_circuit = has_euler_path(5, edges)
print(f"Euler Path: {has_path}, Euler Circuit: {has_circuit}")
# Euler Path: True, Euler Circuit: True

path = hierholzer(5, edges)
print(path)  # [0, 1, 2, 0, 3, 4, 0] or similar
```

## Key Takeaways

```
BIPARTITE GRAPH:
- 2-colorable graph (no odd-length cycles)
- Check using DFS/BFS coloring (alternate 0↔1)
- If conflict found → not bipartite
- Application: Matching problems, scheduling

SCC (Strongly Connected Components):
- Kosaraju's: 2 DFS passes (order + reverse graph) → O(V+E)
- Tarjan's: 1 DFS pass with lowlink values → O(V+E)
- Condensation graph of SCCs is always a DAG

ARTICULATION POINTS:
- Vertices whose removal disconnects graph
- DFS with disc/low values
- Condition: low[neighbor] >= disc[node]
- Root special case: must have > 1 child

BRIDGES:
- Edges whose removal disconnects graph
- Same DFS as articulation points
- Condition: low[neighbor] > disc[node] (strictly greater!)

EULER PATH/CIRCUIT:
- Euler Path: visits every edge exactly once
- Euler Circuit: Euler path that starts and ends at same vertex
- All even degrees → Circuit exists
- Exactly 2 odd degrees → Path exists
- Hierholzer's algorithm to find the path

COMPARISON TABLE:
┌────────────────────┬──────────────────┬──────────────────────┐
│ Concept            │ Key Condition    │ Algorithm            │
├────────────────────┼──────────────────┼──────────────────────┤
│ Bipartite          │ No odd cycles    │ 2-coloring DFS/BFS   │
│ SCC                │ Every pair       │ Kosaraju's/Tarjan's  │
│                    │ reachable        │                      │
│ Articulation Point │ low[v] >= disc[u]│ DFS with disc/low    │
│ Bridge             │ low[v] > disc[u] │ DFS with disc/low    │
│ Euler Path         │ 0 or 2 odd deg.  │ Hierholzer's         │
└────────────────────┴──────────────────┴──────────────────────┘

WHEN TO USE:
- "2-colorable" / "alternating groups" → Bipartite check
- "Minimum edges to make strongly connected" → SCC condensation
- "Critical points / single points of failure" → Articulation points
- "Critical connections" → Bridges
- "Visit every road exactly once" → Euler path
```
