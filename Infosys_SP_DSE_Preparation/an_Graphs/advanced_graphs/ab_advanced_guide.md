# Advanced Graph Concepts

## Bipartite Graph Checking

```python
def is_bipartite(graph):
    """
    LeetCode 785 - Check if graph is bipartite
    Can be colored with 2 colors such that no adjacent nodes have same color
    Time: O(V + E) | Space: O(V)
    """
    n = len(graph)
    color = [-1] * n
    
    def dfs(node, c):
        color[node] = c
        for neighbor in graph[node]:
            if color[neighbor] == c:
                return False
            if color[neighbor] == -1:
                if not dfs(neighbor, 1 - c):
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
                    color[neighbor] = 1 - color[node]
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
                color[node] = -1
        
        return False
    
    return graph_coloring(0)


# Example
graph = [[1, 3], [0, 2], [1, 3], [0, 2]]  # Bipartite: {0,2} and {1,3}
print(is_bipartite(graph))  # True

graph = [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]  # Not bipartite
print(is_bipartite(graph))  # False
```

## Strongly Connected Components (Kosaraju's Algorithm)

```python
from collections import defaultdict

def kosaraju_scc(n, edges):
    """
    Find all Strongly Connected Components using Kosaraju's algorithm
    Time: O(V + E) | Space: O(V + E)
    """
    # Step 1: Build original graph and reverse graph
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)
    
    for u, v in edges:
        graph[u].append(v)
        reverse_graph[v].append(u)
    
    # Step 2: Get finish order using DFS on original graph
    visited = [False] * n
    order = []
    
    def dfs1(node):
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs1(neighbor)
        order.append(node)
    
    for i in range(n):
        if not visited[i]:
            dfs1(i)
    
    # Step 3: DFS on reverse graph in reverse finish order
    visited = [False] * n
    sccs = []
    
    def dfs2(node, component):
        visited[node] = True
        component.append(node)
        for neighbor in reverse_graph[node]:
            if not visited[neighbor]:
                dfs2(neighbor, component)
    
    for node in reversed(order):
        if not visited[node]:
            component = []
            dfs2(node, component)
            sccs.append(component)
    
    return sccs


# Tarjan's SCC (one pass)
def tarjan_scc(n, edges):
    """
    Find SCCs using Tarjan's algorithm (single DFS)
    Time: O(V + E) | Space: O(V)
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

```python
from collections import defaultdict

def find_articulation_points(n, edges):
    """
    Find all articulation points (cut vertices)
    Removing them disconnects the graph
    Time: O(V + E) | Space: O(V)
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = [False] * n
    disc = [0] * n  # Discovery time
    low = [0] * n   # Lowest reachable ancestor
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

```python
from collections import defaultdict

def find_bridges(n, edges):
    """
    Find all bridges (cut edges)
    Removing them disconnects the graph
    Time: O(V + E) | Space: O(V)
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
                if low[neighbor] > disc[node]:
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
Bipartite Graph:
- 2-colorable graph
- Check using DFS/BFS coloring
- Application: Matching problems, scheduling

SCC (Strongly Connected Components):
- Kosaraju's: 2 DFS passes (order + reverse graph)
- Tarjan's: 1 DFS pass with lowlink values
- Condensation graph of SCCs is always a DAG

Articulation Points:
- Vertices whose removal disconnects graph
- DFS with disc/low values
- Condition: low[neighbor] >= disc[node]

Bridges:
- Edges whose removal disconnects graph
- Similar DFS to articulation points
- Condition: low[neighbor] > disc[node]

Euler Path/Circuit:
- Euler Path: visits every edge exactly once
- Euler Circuit: Euler path that starts and ends at same vertex
- All even degrees → Circuit
- Exactly 2 odd degrees → Path
- Hierholzer's algorithm to find the path
```
