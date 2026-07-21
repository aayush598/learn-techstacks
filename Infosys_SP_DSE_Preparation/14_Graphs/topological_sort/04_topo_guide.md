# Topological Sort Complete Guide

## What is Topological Sort?

```
Topological Sort: Linear ordering of vertices in a DAG such that
for every directed edge (u, v), vertex u comes before vertex v.

Only possible for Directed Acyclic Graphs (DAGs).

Example:
    5 → 0 → 4
    5 → 2 → 3 → 1
    
    Valid topological orders:
    [5, 0, 4, 2, 3, 1]
    [5, 2, 0, 3, 4, 1]
    [5, 2, 3, 0, 4, 1]
    
    Invalid: [0, 5, ...] because 5 must come before 0
```

## DFS-Based Topological Sort

```python
from collections import defaultdict

def topological_sort_dfs(n, edges):
    """
    Reverse post-order DFS
    Time: O(V + E) | Space: O(V + E)
    """
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
        order.append(node)
    
    for i in range(n):
        if i not in visited:
            dfs(i)
    
    return order[::-1]


# With cycle detection
def topological_sort_with_cycle_check(n, edges):
    """Returns topological order or [] if cycle exists"""
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    order = []
    
    def dfs(node):
        color[node] = GRAY
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return False  # Back edge = cycle
            if color[neighbor] == WHITE:
                if not dfs(neighbor):
                    return False
        color[node] = BLACK
        order.append(node)
        return True
    
    for i in range(n):
        if color[i] == WHITE:
            if not dfs(i):
                return []
    
    return order[::-1]


# Example
edges = [[5, 0], [5, 2], [4, 0], [4, 1], [2, 3], [3, 1]]
print(topological_sort_dfs(6, edges))  # [5, 4, 2, 3, 1, 0] or similar
```

## BFS-Based Topological Sort (Kahn's Algorithm)

```python
from collections import defaultdict, deque

def topological_sort_bfs(n, edges):
    """
    Kahn's Algorithm
    Time: O(V + E) | Space: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return order if len(order) == n else []


# With level tracking (parallel execution)
def topological_sort_levels(n, edges):
    """Returns topological order grouped by levels"""
    graph = defaultdict(list)
    in_degree = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    levels = []
    
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node)
            
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        levels.append(level)
    
    return levels if sum(len(l) for l in levels) == n else []


# Example
edges = [[5, 0], [5, 2], [4, 0], [4, 1], [2, 3], [3, 1]]
print(topological_sort_bfs(6, edges))  # [0, 1, 2, 3, 4, 5] or similar
print(topological_sort_levels(6, edges))  # [[5, 4], [0, 2], [3], [1]]
```

## Course Schedule I

```python
def can_finish(num_courses, prerequisites):
    """
    LeetCode 207 - Can all courses be finished?
    Check if topological order exists (no cycles)
    Time: O(V + E) | Space: O(V + E)
    """
    from collections import defaultdict, deque
    
    graph = defaultdict(list)
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    count = 0
    
    while queue:
        node = queue.popleft()
        count += 1
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return count == num_courses


# Example
print(can_finish(2, [[1, 0]]))  # True
print(can_finish(2, [[1, 0], [0, 1]]))  # False
```

## Course Schedule II

```python
def find_order(num_courses, prerequisites):
    """
    LeetCode 210 - Return course order
    Time: O(V + E) | Space: O(V + E)
    """
    from collections import defaultdict, deque
    
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
print(find_order(4, [[1, 0], [2, 1], [3, 2]]))  # [0, 1, 2, 3]
```

## Alien Dictionary

```python
def alien_dictionary(words):
    """
    LeetCode 269 - Find character ordering
    Time: O(C) | Space: O(1) - max 26 characters
    """
    from collections import defaultdict, deque
    
    # Build graph from adjacent word comparisons
    graph = defaultdict(set)
    in_degree = {c: 0 for word in words for c in word}
    
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        min_len = min(len(word1), len(word2))
        
        # Invalid: longer word comes before shorter (prefix case)
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
    
    return "".join(order) if len(order) == len(in_degree) else ""


# Example
words = ["wrt", "wrf", "er", "ett", "rftt"]
print(alien_dictionary(words))  # "wertf"
```

## Parallel Courses

```python
from collections import defaultdict, deque

def minimum_semesters(n, relations):
    """
    LeetCode 1136 - Minimum semesters to complete all courses
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

## Longest Path in DAG

```python
from collections import defaultdict, deque

def longest_path(n, edges):
    """
    Find longest path in DAG
    Time: O(V + E) | Space: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    
    # Topological sort
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Longest path using DP
    dist = [0] * n
    
    for node in topo_order:
        for neighbor in graph[node]:
            dist[neighbor] = max(dist[neighbor], dist[node] + 1)
    
    return max(dist)


# Longest path from specific source
def longest_path_from_source(n, edges, source):
    graph = defaultdict(list)
    in_degree = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    
    # Topological sort
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # DP from source
    dist = [-float('inf')] * n
    dist[source] = 0
    
    for node in topo_order:
        if dist[node] != -float('inf'):
            for neighbor in graph[node]:
                dist[neighbor] = max(dist[neighbor], dist[node] + 1)
    
    return dist


# Example
edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
print(longest_path(4, edges))  # 2 (0 → 1 → 3 or 0 → 2 → 3)
```

## Key Takeaways

```
1. Topological sort only works on DAGs
2. DFS: Reverse post-order traversal
3. BFS: Process nodes with in-degree 0 (Kahn's)
4. Cycle detection: If order size < V → cycle exists
5. Level-based: Track which nodes are processed together
6. Applications:
   - Course scheduling
   - Build systems (make)
   - Task scheduling with dependencies
   - Compilation order
   - Alien dictionary
   - Parallel execution planning
7. When to use:
   - "Order of tasks" → Topological sort
   - "Can finish all tasks" → Check for cycles
   - "Minimum time with parallelism" → Level-based topo sort
   - "All possible orders" → DFS with backtracking
```
