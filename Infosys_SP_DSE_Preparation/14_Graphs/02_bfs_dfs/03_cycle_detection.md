# Cycle Detection Complete Guide

## Cycle in Undirected Graph (DFS)

### Visual: Cycle Detection Using Parent Tracking

```
Key Idea: In an undirected graph, if we visit a node that is
ALREADY visited and is NOT our parent, we found a cycle!

Cycle:                        No Cycle (Tree):
  0 --- 1                       0 --- 1
  |   / |                       |   /
  |  /  |                       |  /
  | /   |                       | /
  2 --- 3                       2

DFS from 0:                   DFS from 0:
  Visit 0 (parent=-1)          Visit 0 (parent=-1)
  Visit 1 (parent=0)           Visit 1 (parent=0)
  Visit 2 (parent=1)           Visit 2 (parent=1)
  Visit 3 (parent=2)           3 is leaf → backtrack
  Look at neighbor 1:          Backtrack to 0
  1 is VISITED and ≠ parent(3) No more unvisited neighbors
  → CYCLE FOUND!               → NO CYCLE

WHY does parent tracking work?
┌───────────────────────────────────────────────────────┐
│ In undirected graph, edge A↔B means:                  │
│   When we visit B from A, the edge A→B is "used"     │
│   The "back" edge B→A is just the reverse             │
│                                                       │
│   If we find a visited neighbor that is NOT parent:   │
│   → We found an edge NOT in our DFS tree              │
│   → That edge creates a cycle!                        │
└───────────────────────────────────────────────────────┘
```

```python
def has_cycle_undirected_dfs(n, edges):
    """
    Detect cycle in undirected graph using DFS
    Time: O(V + E) | Space: O(V + E)

    KEY INSIGHT: Track parent of each node.
    If we reach a visited node that is NOT the parent → cycle!
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
                # Recurse with current node as parent
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                # Visited neighbor that is NOT parent = CYCLE!
                return True

        return False

    # Check all components (graph might be disconnected)
    for i in range(n):
        if i not in visited:
            if dfs(i, -1):   # -1 means no parent (root)
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

### Visual: 3-Color Marking System

```
WHY we need 3 colors for DIRECTED graphs:
─────────────────────────────────────────
In undirected graphs, parent tracking works.
In directed graphs, edges are ONE-WAY, so we need to detect
"back edges" — edges that go back to a node currently on
the recursion stack.

The 3-Color System:
┌─────────────────────────────────────────────────────────┐
│  WHITE (0) = Not visited yet                           │
│  GRAY  (1) = Currently being explored (ON the stack)   │
│  BLACK (2) = Fully processed (DONE with this node)     │
│                                                         │
│  When we see a GRAY neighbor → BACK EDGE → CYCLE!      │
│  When we see a BLACK neighbor → Already done, skip      │
│  When we see a WHITE neighbor → Keep exploring          │
└─────────────────────────────────────────────────────────┘

Example with cycle: 0 → 1 → 2 → 0

Step │ Current │ Colors        │ Action
─────│─────────│───────────────│───────────────────────────
  1  │ dfs(0)  │ 0:GRAY        │ Start exploring 0
  2  │ dfs(1)  │ 0:GRAY,1:GRAY │ 0→1, explore 1
  3  │ dfs(2)  │ 0:GRAY,1:GRAY │ 1→2, explore 2
     │         │ 2:GRAY        │
  4  │ check 0 │ 0:GRAY        │ 2→0, 0 is GRAY = CYCLE!

Without cycle: 0 → 1 → 2 → 3

Step │ Current │ Colors          │ Action
─────│─────────│─────────────────│─────────────────────────
  1  │ dfs(0)  │ 0:GRAY          │ Start exploring 0
  2  │ dfs(1)  │ 0:GRAY,1:GRAY   │ 0→1, explore 1
  3  │ dfs(2)  │ 0:GRAY,1:GRAY   │ 1→2, explore 2
     │         │ 2:GRAY          │
  4  │ dfs(3)  │ ..., 2:GRAY     │ 2→3, explore 3
     │         │ 3:GRAY          │
  5  │ done(3) │ ..., 3:BLACK    │ No neighbors → mark BLACK
  6  │ done(2) │ ..., 2:BLACK    │ Done → mark BLACK
  7  │ done(1) │ ..., 1:BLACK    │ Done → mark BLACK
  8  │ done(0) │ 0:BLACK         │ Done → mark BLACK
     │         │                 │ NO GRAY neighbor found → NO CYCLE
```

```python
def has_cycle_directed_dfs(n, edges):
    """
    Detect cycle in directed graph using DFS with 3 colors
    WHITE = 0: Not visited
    GRAY = 1: In current DFS path (on stack)
    BLACK = 2: Fully processed
    Time: O(V + E) | Space: O(V + E)

    WHY IT WORKS:
    - GRAY nodes are ancestors in the DFS tree
    - If we reach a GRAY node, we found a back edge → cycle
    - BLACK nodes are completely done — no need to revisit
    """
    from collections import defaultdict

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n

    def dfs(node):
        color[node] = GRAY   # Mark as "currently exploring"

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                # Back edge found = CYCLE!
                return True
            if color[neighbor] == WHITE and dfs(neighbor):
                return True

        color[node] = BLACK  # Mark as "fully processed"
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
                # Reconstruct cycle by following parent pointers
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
UNDIRECTED GRAPH — Cycle Detection:
────────────────────────────────────
Method 1: DFS with parent tracking
  → If visited neighbor ≠ parent → CYCLE
  → O(V + E) time, O(V) space

Method 2: BFS with parent tracking
  → Same logic, using queue instead of recursion
  → O(V + E) time, O(V) space

Method 3: Union-Find
  → If both nodes already in same set → CYCLE
  → O(E × α(V)) time ≈ O(E), O(V) space

DIRECTED GRAPH — Cycle Detection:
──────────────────────────────────
Method 1: DFS with 3-color marking
  → WHITE → GRAY → BLACK
  → GRAY → GRAY edge = back edge = CYCLE
  → O(V + E) time, O(V) space

Method 2: Kahn's Algorithm (BFS)
  → Topological sort
  → If sorted order has < V nodes → CYCLE
  → O(V + E) time, O(V) space

DECISION GUIDE:
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  Undirected graph?                                       │
│  ├─ YES → Use Union-Find (simplest) OR DFS with parent  │
│  │        Union-Find is best for online/edge-by-edge     │
│  │        DFS is best for one-shot analysis              │
│  │                                                       │
│  └─ NO (Directed)?                                       │
│      ├─ Need cycle path? → DFS with 3-color + parent    │
│      ├─ Need topological order too? → Kahn's            │
│      └─ Just need YES/NO? → Either works                │
│                                                          │
└──────────────────────────────────────────────────────────┘

Complexity Comparison:
┌─────────────────────┬──────────────┬──────────────┐
│ Algorithm           │ Time         │ Space        │
├─────────────────────┼──────────────┼──────────────┤
│ DFS (undirected)    │ O(V + E)     │ O(V)         │
│ BFS (undirected)    │ O(V + E)     │ O(V)         │
│ Union-Find          │ O(E × α(V))  │ O(V)         │
│ DFS (directed)      │ O(V + E)     │ O(V)         │
│ Kahn's (directed)   │ O(V + E)     │ O(V)         │
└─────────────────────┴──────────────┴──────────────┘

When to use what:
- Undirected graph cycle → Union-Find or DFS with parent
- Directed graph cycle → DFS with colors
- Topological ordering → Kahn's (BFS) or DFS
- Check if DAG → Either method
```
