# DFS Complete Guide

## What is DFS? — Visual Intuition

```
DFS = Depth-First Search
Goes as deep as possible before backtracking.

Think of it as: A mouse exploring a maze — it runs down
one path until it hits a dead end, then backtracks.

        0
       / \
      1   2          DFS from 0:
     / \   \         0 → 1 → 3 → 5 (dead end)
    3   4   5        backtrack → 4 (dead end)
                     backtrack → 2
  DFS Order: [0, 1, 3, 5, 4, 2]

  BFS Order: [0, 1, 2, 3, 4, 5]  (for comparison)

DFS uses a STACK (LIFO):
  Push 0:  [0]
  Pop 0:   []     → process 0, push children [2, 1]
  Pop 1:   [2]    → process 1, push children [2, 4, 3]
  Pop 3:   [2, 4] → process 3, push children [2, 4, 5]
  Pop 5:   [2, 4] → process 5, no children
  Pop 4:   [2]    → process 4, no new children
  Pop 2:   []     → process 2, no new children
  Done!

BFS vs DFS:
  BFS: "Visit all neighbors first" → LEVEL by level
  DFS: "Visit one neighbor deeply" → BRANCH by branch
```

## DFS Recursive Template

### Step-by-Step: Recursive DFS Walkthrough

```
Graph:
    0 → [1, 2]
    1 → [0, 3, 4]
    2 → [0, 4]
    3 → [1, 5]
    4 → [1, 2]
    5 → [3]

DFS(0) call stack visualization:

  dfs(0)                    ← Enter node 0
  ├─ visited = {0}
  ├─ neighbor 1 not visited
  │   └─ dfs(1)             ← Go deep into node 1
  │       ├─ visited = {0, 1}
  │       ├─ neighbor 0 already visited, skip
  │       ├─ neighbor 3 not visited
  │       │   └─ dfs(3)     ← Go deep into node 3
  │       │       ├─ visited = {0, 1, 3}
  │       │       ├─ neighbor 1 already visited
  │       │       ├─ neighbor 5 not visited
  │       │       │   └─ dfs(5)
  │       │       │       ├─ visited = {0, 1, 3, 5}
  │       │       │       ├─ neighbor 3 already visited
  │       │       │       └─ return [5]        ← Dead end!
  │       │       └─ return [3, 5]
  │       ├─ neighbor 4 not visited
  │       │   └─ dfs(4)     ← Go deep into node 4
  │       │       ├─ visited = {0, 1, 3, 5, 4}
  │       │       ├─ neighbor 1 already visited
  │       │       ├─ neighbor 2 not visited... BUT wait
  │       │       │   Actually let's check: visited = {0,1,3,5,4}
  │       │       │   2 is NOT in visited, so:
  │       │       │   └─ dfs(2)
  │       │       │       ├─ visited = {0, 1, 3, 5, 4, 2}
  │       │       │       ├─ neighbor 0 already visited
  │       │       │       ├─ neighbor 4 already visited
  │       │       │       └─ return [2]
  │       │       └─ return [4, 2]
  │       └─ return [1, 3, 5, 4, 2]
  ├─ neighbor 2 already visited (added by dfs(4))
  └─ return [0, 1, 3, 5, 4, 2]

FINAL DFS ORDER: [0, 1, 3, 5, 4, 2]
```

```python
def dfs_recursive(graph, node, visited=None):
    """
    Standard DFS recursive template
    Time: O(V + E) | Space: O(V) - recursion stack

    ALGORITHM:
    1. Mark current node as visited
    2. For each unvisited neighbor, recursively call DFS
    3. Return the list of visited nodes
    """
    if visited is None:
        visited = set()

    visited.add(node)
    result = [node]

    for neighbor in graph[node]:
        if neighbor not in visited:
            result.extend(dfs_recursive(graph, neighbor, visited))

    return result


# DFS with return value (for searching)
def dfs_search(graph, node, target, visited=None):
    """Returns True if target found in the graph"""
    if visited is None:
        visited = set()

    if node == target:
        return True

    visited.add(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            if dfs_search(graph, neighbor, target, visited):
                return True   # Found in subtree!

    return False  # Not found anywhere


# DFS with path tracking
def dfs_path(graph, start, end, visited=None):
    """Returns the FIRST path found from start to end"""
    if visited is None:
        visited = set()

    if start == end:
        return [start]   # Base case: found the destination

    visited.add(start)

    for neighbor in graph[start]:
        if neighbor not in visited:
            path = dfs_path(graph, neighbor, end, visited)
            if path:                    # If a path was found in subtree
                return [start] + path   # Prepend current node

    return None   # No path from this node
```

## DFS Iterative (Using Stack)

### Visual: Iterative DFS Walkthrough

```
Graph: 0 → [1, 2], 1 → [0, 3], 2 → [0, 4]

Iterative DFS from 0 (push in REVERSE order for consistent order):

Step │ Stack   │ Pop │ Visited     │ Result
─────│─────────│─────│─────────────│──────────
  1  │ [0]     │ --  │ {0}         │ []
  2  │ [2, 1]  │  0  │ {0}         │ [0]
  3  │ [2, 4, 3]│ 1  │ {0, 1}      │ [0, 1]
  4  │ [2, 4]  │  3  │ {0, 1, 3}   │ [0, 1, 3]
  5  │ [2]     │  4  │ {0,1,3,4}   │ [0, 1, 3, 4]
  6  │ []      │  2  │ {all}       │ [0, 1, 3, 4, 2]
  7  │ DONE    │ --  │ {all}       │ [0, 1, 3, 4, 2]

WHY push in reverse? 
  Graph[0] = [1, 2]
  If we push 1 then 2, stack pops 2 first (LIFO)
  Pushing [2, 1] makes stack pop 1 first → matches recursive order
```

```python
def dfs_iterative(graph, start):
    """
    Iterative DFS using explicit stack
    Time: O(V + E) | Space: O(V)

    WHY ITERATIVE?
    - Python recursion limit is ~1000
    - For graphs with V > 1000, recursive DFS will crash!
    - Use iterative DFS for large graphs
    """
    visited = set([start])
    stack = [start]
    result = []

    while stack:
        node = stack.pop()           # LIFO: process most recently added
        result.append(node)

        # Add neighbors in REVERSE for consistent order with recursive
        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return result


# DFS without visited set (for backtracking)
def dfs_backtracking(graph, node, visited):
    """DFS that modifies visited in-place — useful for backtracking"""
    visited.add(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_backtracking(graph, neighbor, visited)

    return visited
```

### Recursion Limit Warning

```
⚠️  IMPORTANT: Python default recursion limit is ~1000

For graphs with > 1000 nodes, recursive DFS WILL CRASH:
  → RecursionError: maximum recursion depth exceeded

SOLUTION 1: Use iterative DFS (explicit stack)
SOLUTION 2: Increase limit: sys.setrecursionlimit(10**6)

When to use which:
┌───────────────────────┬─────────────────────────────┐
│ Recursive DFS         │ Iterative DFS               │
├───────────────────────┼─────────────────────────────┤
│ Cleaner code          │ No recursion limit          │
│ V < 1000              │ V can be any size           │
│ Natural for backtracking│ Slightly more complex     │
│ Easier to reason about│ Better for production code  │
└───────────────────────┴─────────────────────────────┘
```

## DFS on Grid/Matrix

### Visual: Grid DFS — Recursive vs BFS

```
Grid DFS from (0,0) — Goes deep in ONE direction first:

  Grid:                DFS Path:
  ┌───┬───┬───┐       ┌───┬───┬───┐
  │ S │ 1 │ 1 │       │ 1→│ 2→│ 3 │   S = Start (0,0)
  ├───┼───┼───┤       ├───┼───┼───┤   Numbers = visit order
  │ 1 │ 1 │ 1 │  ──►  │ 8 │ 9→│ 4 │   Goes RIGHT until blocked
  ├───┼───┼───┤       ├───┼───┼───┤   then DOWN, then LEFT...
  │ 1 │ 1 │ E │       │ 7←│ 6←│ 5 │   E = End
  └───┴───┴───┘       └───┴───┴───┘

  DFS: 1→2→3→4→5→6→7→8→9 (winds through entire region)
  BFS: 1→2→8→3→9→4→7→6→5 (level by level, different order!)

DFS advantage: Uses less memory (only one branch in stack)
BFS advantage: Finds shortest path first
```

```python
def dfs_grid(grid, row, col, visited):
    """
    DFS on a 2D grid
    Time: O(M * N) | Space: O(M * N)
    """
    rows, cols = len(grid), len(grid[0])

    # Boundary and condition check — ALWAYS check BEFORE recursing!
    if (row < 0 or row >= rows or col < 0 or col >= cols or
        (row, col) in visited or grid[row][col] == 0):
        return

    visited.add((row, col))

    # 4-directional movement
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        dfs_grid(grid, row + dr, col + dc, visited)


def dfs_grid_iterative(grid, start_row, start_col):
    """Iterative DFS on grid — no recursion limit issues"""
    rows, cols = len(grid), len(grid[0])
    visited = set([(start_row, start_col)])
    stack = [(start_row, start_col)]

    while stack:
        r, c = stack.pop()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in visited and grid[nr][nc] == 1):
                visited.add((nr, nc))
                stack.append((nr, nc))

    return visited
```

## Number of Islands (DFS)

```python
def num_islands_dfs(grid):
    """
    LeetCode 200 - Count connected components
    Time: O(M * N) | Space: O(M * N)
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] != '1'):
            return
        
        grid[r][c] = '0'  # Mark visited
        
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    
    return count
```

## Surrounded Regions

```python
def solve(board):
    """
    LeetCode 130 - Flip 'O' to 'X' if surrounded by 'X'
    Time: O(M * N) | Space: O(M * N)
    Strategy: DFS from border 'O's, mark safe, flip rest
    """
    if not board or not board[0]:
        return
    
    rows, cols = len(board), len(board[0])
    
    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            board[r][c] != 'O'):
            return
        
        board[r][c] = 'S'  # Mark as safe (connected to border)
        
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    # Mark all 'O's connected to border as safe
    for r in range(rows):
        dfs(r, 0)
        dfs(r, cols - 1)
    for c in range(cols):
        dfs(0, c)
        dfs(rows - 1, c)
    
    # Flip remaining 'O's to 'X' and 'S' back to 'O'
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == 'S':
                board[r][c] = 'O'
    
    return board


# Example
board = [
    ['X', 'X', 'X', 'X'],
    ['X', 'O', 'O', 'X'],
    ['X', 'X', 'O', 'X'],
    ['X', 'O', 'X', 'X']
]
print(solve(board))
# [['X', 'X', 'X', 'X'], ['X', 'X', 'X', 'X'], ['X', 'X', 'X', 'X'], ['X', 'O', 'X', 'X']]
```

## Max Area of Island

```python
def max_area_of_island(grid):
    """
    LeetCode 695 - Find largest connected component
    Time: O(M * N) | Space: O(M * N)
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    max_area = 0
    
    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] != 1):
            return 0
        
        grid[r][c] = 0  # Mark visited
        
        area = 1
        area += dfs(r + 1, c)
        area += dfs(r - 1, c)
        area += dfs(r, c + 1)
        area += dfs(r, c - 1)
        
        return area
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                max_area = max(max_area, dfs(r, c))
    
    return max_area
```

## Pacific Atlantic Water Flow

```python
def pacific_atlantic(heights):
    """
    LeetCode 417 - Find cells that can flow to both oceans
    Time: O(M * N) | Space: O(M * N)
    Strategy: DFS from ocean borders inward
    """
    if not heights or not heights[0]:
        return []
    
    rows, cols = len(heights), len(heights[0])
    pacific = set()
    atlantic = set()
    
    def dfs(r, c, visited, prev_height):
        if ((r, c) in visited or
            r < 0 or r >= rows or c < 0 or c >= cols or
            heights[r][c] < prev_height):
            return
        
        visited.add((r, c))
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, visited, heights[r][c])
    
    # DFS from Pacific (top and left borders)
    for r in range(rows):
        dfs(r, 0, pacific, 0)
        dfs(r, cols - 1, atlantic, 0)
    for c in range(cols):
        dfs(0, c, pacific, 0)
        dfs(rows - 1, c, atlantic, 0)
    
    # Intersection of both reachable cells
    return list(pacific & atlantic)
```

## Course Schedule (Cycle Detection in Directed Graph)

```python
def can_finish(num_courses, prerequisites):
    """
    LeetCode 207 - Detect cycle in directed graph
    Time: O(V + E) | Space: O(V + E)
    """
    from collections import defaultdict
    
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[course].append(prereq)
    
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {i: WHITE for i in range(num_courses)}
    
    def has_cycle(node):
        color[node] = GRAY
        
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True
            if color[neighbor] == WHITE and has_cycle(neighbor):
                return True
        
        color[node] = BLACK
        return False
    
    for i in range(num_courses):
        if color[i] == WHITE and has_cycle(i):
            return False
    
    return True


# Course Schedule II - Return topological order
def find_order(num_courses, prerequisites):
    """LeetCode 210 - Return course order or [] if impossible"""
    from collections import defaultdict, deque
    
    graph = defaultdict(list)
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    # BFS - Kahn's algorithm
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
print(can_finish(2, [[1, 0]]))  # True
print(find_order(4, [[1, 0], [2, 1], [3, 2]]))  # [0, 1, 2, 3]
```

## Path Exists in Graph

```python
def valid_path(n, edges, source, destination):
    """
    LeetCode 1971 - Check if path exists between source and destination
    Time: O(V + E) | Space: O(V + E)
    """
    from collections import defaultdict
    
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = set([source])
    stack = [source]
    
    while stack:
        node = stack.pop()
        
        if node == destination:
            return True
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    
    return False


# Union-Find approach (more efficient for single query)
def valid_path_union_find(n, edges, source, destination):
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        parent[find(x)] = find(y)
    
    for u, v in edges:
        union(u, v)
    
    return find(source) == find(destination)
```

## DFS Backtracking Template

```python
def dfs_backtracking_template(graph, start, target, path=None, visited=None):
    """
    Backtracking DFS - explores all paths
    Useful for: finding all paths, permutations, combinations
    """
    if path is None:
        path = []
    if visited is None:
        visited = set()
    
    path.append(start)
    visited.add(start)
    
    if start == target:
        result = path.copy()
        path.pop()
        visited.remove(start)
        return [result]
    
    all_paths = []
    for neighbor in graph[start]:
        if neighbor not in visited:
            paths = dfs_backtracking_template(graph, neighbor, target, path, visited)
            all_paths.extend(paths)
    
    path.pop()
    visited.remove(start)
    
    return all_paths


# Example
graph = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 4],
    3: [1, 5],
    4: [1, 2],
    5: [3]
}

print(dfs_backtracking_template(graph, 0, 5))
# [[0, 1, 3, 5], [0, 2, 4, 1, 3, 5]]
```

## DFS Template for Grid Problems

```python
def dfs_grid_template(grid, start_row, start_col):
    """
    Universal DFS template for grid problems
    """
    rows, cols = len(grid), len(grid[0])
    visited = set()
    
    def dfs(r, c):
        # Boundary check
        if (r < 0 or r >= rows or c < 0 or c >= cols):
            return
        
        # Condition check (customize per problem)
        if (r, c) in visited or grid[r][c] == 0:
            return
        
        visited.add((r, c))
        
        # 4-directional (or 8-directional)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc)
    
    dfs(start_row, start_col)
    return visited


# Variant: count regions
def count_regions(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0
    
    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            (r, c) in visited or grid[r][c] == 0):
            return
        
        visited.add((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in visited:
                dfs(r, c)
                count += 1
    
    return count
```

## BFS vs DFS Comparison

```
| Feature           | BFS                    | DFS                    |
|-------------------|------------------------|------------------------|
| Data Structure    | Queue (FIFO)           | Stack/Recursion (LIFO) |
| Shortest Path     | Yes (unweighted)       | No (but finds any path)|
| Memory            | O(V) — wide graphs     | O(V) — deep graphs     |
| Level Order       | Yes                    | No                     |
| Cycle Detection   | Yes                    | Yes (with colors)      |
| Topological Sort  | Yes (Kahn's)           | Yes (reverse finish)   |
| Connected Comp.   | Yes                    | Yes                    |
| Grid Traversal    | Yes                    | Yes                    |
| Bidirectional     | Easy                   | Hard                   |

WHEN TO CHOOSE BFS vs DFS:

┌─────────────────────────────────────────────────────────────┐
│                    USE BFS WHEN:                             │
│                                                             │
│  ✓ Shortest path in UNWEIGHTED graph                        │
│  ✓ Level-by-level processing (tree level order)             │
│  ✓ Multi-source propagation (rotting oranges)               │
│  ✓ Bipartite checking                                       │
│  ✓ Minimum moves/steps in a puzzle                          │
│                                                             │
│                    USE DFS WHEN:                             │
│                                                             │
│  ✓ Finding ALL paths between two nodes                      │
│  ✓ Backtracking problems (permutations, combinations)       │
│  ✓ Topological sort (reverse post-order)                    │
│  ✓ Cycle detection in directed graphs                       │
│  ✓ Connected components (simpler code)                      │
│  ✓ Detecting bridges/articulation points                     │
│  ✓ Grid problems (recursive DFS is shorter to write)        │
│                                                             │
│                    USE EITHER:                               │
│                                                             │
│  ✓ Checking if a path exists                                │
│  ✓ Counting connected components                            │
│  ✓ Flood fill / region problems                             │
└─────────────────────────────────────────────────────────────┘
```

## Key Takeaways for DFS

```
1. DFS uses STACK (LIFO) or recursion — goes deep first
2. DFS is NATURAL for backtracking problems
3. DFS uses less memory than BFS in wide graphs
4. For grid problems, DFS is simpler to write (recursive)
5. For shortest path in UNWEIGHTED graph, use BFS
6. For checking if path EXISTS, use either
7. Pattern: check boundary BEFORE recursive call
8. Time: O(V + E) for graphs, O(M * N) for grids
9. Space: O(V) for visited + recursion stack
10. Use iterative DFS if recursion depth > 10^5

CRITICAL: Boundary Check Pattern for Grid DFS
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  def dfs(grid, r, c, visited):                          │
│      # Step 1: Check BOUNDS first (before anything else!)│
│      if r < 0 or r >= rows or c < 0 or c >= cols:      │
│          return                                          │
│                                                          │
│      # Step 2: Check VISITED and CONDITION               │
│      if (r, c) in visited or grid[r][c] != target:      │
│          return                                          │
│                                                          │
│      # Step 3: MARK as visited                           │
│      visited.add((r, c))                                 │
│                                                          │
│      # Step 4: RECURSE in all directions                 │
│      for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:        │
│          dfs(grid, r+dr, c+dc, visited)                  │
│                                                          │
│  WHY this order?                                         │
│  - Bounds check prevents IndexOutOfBounds errors         │
│  - Visited check prevents infinite recursion             │
│  - Mark visited BEFORE recursing (prevents duplicates)   │
└──────────────────────────────────────────────────────────┘

Complexity Analysis:
┌────────────────────┬──────────────┬──────────────┐
│ Operation          │ Graph DFS    │ Grid DFS     │
├────────────────────┼──────────────┼──────────────┤
│ Time Complexity    │ O(V + E)     │ O(M × N)     │
│ Space (recursive)  │ O(V) stack   │ O(M × N)     │
│ Space (iterative)  │ O(V) stack   │ O(M × N)     │
│ Max recursion depth│ O(V)         │ O(M × N)     │
└────────────────────┴──────────────┴──────────────┘

Common DFS Patterns:
┌─────────────────────────┬───────────────────────────────────┐
│ Pattern                 │ Example Problems                  │
├─────────────────────────┼───────────────────────────────────┤
│ Count components        │ Number of Islands                 │
│ Find largest component  │ Max Area of Island                │
│ Mark visited & explore  │ Flood Fill                        │
│ DFS from borders        │ Surrounded Regions                │
│ DFS with coloring       │ Graph Coloring / Bipartite        │
│ DFS with 3-color        │ Cycle Detection (directed)        │
│ DFS + backtracking      │ Find all paths                    │
│ DFS + disc/low          │ Bridges & Articulation Points     │
└─────────────────────────┴───────────────────────────────────┘
```
