# Cycle Detection Complete Guide

## Cycle in Undirected Graph (DFS)

```python
def has_cycle_undirected_dfs(n, edges):
    """
    Detect cycle in undirected graph using DFS
    Time: O(V + E) | Space: O(V + E)
    """
    from collections import defaultdict
    
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                # Visited neighbor that is not parent = cycle
                return True
        
        return False
    
    for i in range(n):
        if i not in visited:
            if dfs(i, -1):
                return True
    
    return False


# Example
edges = [[0, 1], [1, 2], [2, 0]]  # Triangle = cycle
print(has_cycle_undirected_dfs(3, edges))  # True

edges = [[0, 1], [1, 2], [2, 3]]  # Line = no cycle
print(has_cycle_undirected_dfs(4, edges))  # False
```

## Cycle in Undirected Graph (BFS)

```python
from collections import defaultdict, deque

def has_cycle_undirected_bfs(n, edges):
    """
    Detect cycle in undirected graph using BFS
    Time: O(V + E) | Space: O(V + E)
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = set()
    
    for start in range(n):
        if start in visited:
            continue
        
        queue = deque([(start, -1)])
        visited.add(start)
        
        while queue:
            node, parent = queue.popleft()
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, node))
                elif neighbor != parent:
                    return True
    
    return False
```

## Cycle in Directed Graph (DFS with Color Marking)

```python
def has_cycle_directed_dfs(n, edges):
    """
    Detect cycle in directed graph using DFS with 3 colors
    WHITE = 0: Not visited
    GRAY = 1: In current DFS path (on stack)
    BLACK = 2: Fully processed
    Time: O(V + E) | Space: O(V + E)
    """
    from collections import defaultdict
    
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    
    def dfs(node):
        color[node] = GRAY
        
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                # Back edge found = cycle
                return True
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        
        color[node] = BLACK
        return False
    
    for i in range(n):
        if color[i] == WHITE:
            if dfs(i):
                return True
    
    return False


# Example with path tracking
def find_cycle_directed(n, edges):
    """Returns the cycle path if found, else []"""
    from collections import defaultdict
    
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    parent = [-1] * n
    
    def dfs(node):
        color[node] = GRAY
        
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                # Reconstruct cycle
                cycle = [neighbor]
                curr = node
                while curr != neighbor:
                    cycle.append(curr)
                    curr = parent[curr]
                cycle.append(neighbor)
                return cycle[::-1]
            
            if color[neighbor] == WHITE:
                parent[neighbor] = node
                result = dfs(neighbor)
                if result:
                    return result
        
        color[node] = BLACK
        return None
    
    for i in range(n):
        if color[i] == WHITE:
            result = dfs(i)
            if result:
                return result
    
    return []


# Example
edges = [[0, 1], [1, 2], [2, 0]]  # 0→1→2→0 cycle
print(has_cycle_directed_dfs(3, edges))  # True
print(find_cycle_directed(3, edges))  # [0, 1, 2, 0]
```

## Topological Sort Using DFS

```python
def topological_sort_dfs(n, edges):
    """
    Topological sort using DFS (reverse post-order)
    Time: O(V + E) | Space: O(V + E)
    Only works on DAGs (Directed Acyclic Graphs)
    """
    from collections import defaultdict
    
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    
    visited = set()
    order = []
    
    def dfs(node):
        visited.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        
        # Add to front after all children processed
        order.append(node)
    
    for i in range(n):
        if i not in visited:
            dfs(i)
    
    return order[::-1]


# Course Schedule II using DFS
def find_order_dfs(num_courses, prerequisites):
    from collections import defaultdict
    
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * num_courses
    order = []
    
    def dfs(node):
        color[node] = GRAY
        
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return False  # Cycle detected
            if color[neighbor] == WHITE:
                if not dfs(neighbor):
                    return False
        
        color[node] = BLACK
        order.append(node)
        return True
    
    for i in range(num_courses):
        if color[i] == WHITE:
            if not dfs(i):
                return []
    
    return order[::-1]


# Example
edges = [[5, 0], [5, 2], [4, 0], [4, 1], [2, 3], [3, 1]]
print(topological_sort_dfs(6, edges))  # [5, 4, 2, 3, 1, 0] or similar
```

## Topological Sort Using BFS (Kahn's Algorithm)

```python
from collections import defaultdict, deque

def topological_sort_bfs(n, edges):
    """
    Kahn's Algorithm - BFS-based topological sort
    Time: O(V + E) | Space: O(V + E)
    Process nodes with in-degree 0 first
    """
    graph = defaultdict(list)
    in_degree = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    
    # Start with all nodes having in-degree 0
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If order doesn't contain all nodes, there's a cycle
    return order if len(order) == n else []


# Course Schedule II using Kahn's
def find_order_kahn(num_courses, prerequisites):
    graph = defaultdict(list)
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return order if len(order) == num_courses else []


# Example
edges = [[5, 0], [5, 2], [4, 0], [4, 1], [2, 3], [3, 1]]
print(topological_sort_bfs(6, edges))  # [0, 1, 2, 3, 4, 5] or similar
```

## Alien Dictionary

```python
def alien_dictionary(words):
    """
    LeetCode 269 - Find character ordering from sorted words
    Time: O(C) where C = total characters | Space: O(1) - 26 letters max
    """
    from collections import defaultdict, deque
    
    # Build graph: for each adjacent pair of words, find first diff
    graph = defaultdict(set)
    in_degree = {c: 0 for word in words for c in word}
    
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        min_len = min(len(word1), len(word2))
        
        # Invalid case: longer word before shorter
        if len(word1) > len(word2) and word1[:min_len] == word2[:min_len]:
            return ""
        
        for j in range(min_len):
            if word1[j] != word2[j]:
                if word2[j] not in graph[word1[j]]:
                    graph[word1[j]].add(word2[j])
                    in_degree[word2[j]] += 1
                break
    
    # Kahn's algorithm
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    order = []
    
    while queue:
        c = queue.popleft()
        order.append(c)
        
        for neighbor in graph[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all characters are included
    if len(order) != len(in_degree):
        return ""
    
    return "".join(order)


# Example
words = ["wrt", "wrf", "er", "ett", "rftt"]
print(alien_dictionary(words))  # "wertf"
```

## Detect Cycle Using Union-Find (Undirected)

```python
def has_cycle_union_find(n, edges):
    """
    Detect cycle in undirected graph using Union-Find
    Time: O(E * α(n)) ≈ O(E) | Space: O(V)
    """
    parent = list(range(n))
    rank = [0] * n
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return True  # Already connected = cycle
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return False
    
    for u, v in edges:
        if union(u, v):
            return True
    
    return False


# Example
edges = [[0, 1], [1, 2], [2, 0]]
print(has_cycle_union_find(3, edges))  # True

edges = [[0, 1], [1, 2], [2, 3]]
print(has_cycle_union_find(4, edges))  # False
```

## Parallel Courses (Longest Path in DAG)

```python
from collections import defaultdict, deque

def minimum_semesters(n, relations):
    """
    LeetCode 1136 - Find minimum semesters to complete all courses
    Equivalent to longest path in DAG
    Time: O(V + E) | Space: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = [0] * n
    
    for u, v in relations:
        graph[u - 1].append(v - 1)
        in_degree[v - 1] += 1
    
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    semesters = 0
    completed = 0
    
    while queue:
        semesters += 1
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            completed += 1
            
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
    
    return semesters if completed == n else -1


# Example
print(minimum_semesters(3, [[1, 3], [2, 3]]))  # 2
```

## Graph Coloring Check (Bipartite)

```python
def is_bipartite(graph):
    """
    LeetCode 785 - Check if graph is bipartite
    Time: O(V + E) | Space: O(V)
    """
    n = len(graph)
    color = [-1] * n
    
    def dfs(node, c):
        color[node] = c
        
        for neighbor in graph[node]:
            if color[neighbor] == c:
                return False  # Same color = not bipartite
            if color[neighbor] == -1:
                if not dfs(neighbor, 1 - c):
                    return False
        
        return True
    
    # Check all components
    for i in range(n):
        if color[i] == -1:
            if not dfs(i, 0):
                return False
    
    return True


# BFS approach
def is_bipartite_bfs(graph):
    n = len(graph)
    color = [-1] * n
    
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
```

## Key Takeaways for Cycle Detection

```
Undirected Graph:
- DFS: Track parent, if visited neighbor ≠ parent → cycle
- BFS: Same logic as DFS but with queue
- Union-Find: If both nodes already in same set → cycle
- All: O(V + E) time

Directed Graph:
- DFS: 3-color marking (WHITE/GRAY/BLACK)
  - GRAY → GRAY edge = back edge = cycle
- Kahn's: If topological order size < V → cycle
- Both: O(V + E) time

Topological Sort:
- Only works on DAGs (no cycles)
- DFS: Reverse post-order traversal
- BFS: Process nodes with in-degree 0 (Kahn's)
- Both: O(V + E) time

When to use what:
- Undirected graph cycle → Union-Find or DFS with parent
- Directed graph cycle → DFS with colors
- Topological ordering → Kahn's (BFS) or DFS
- Check if DAG → Either method
```
