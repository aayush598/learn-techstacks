# DFS Complete Guide

## DFS Recursive Template

```python
def dfs_recursive(graph, node, visited=None):
    """
    Standard DFS recursive template
    Time: O(V + E) | Space: O(V) - recursion stack
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
    """Returns True if target found"""
    if visited is None:
        visited = set()
    
    if node == target:
        return True
    
    visited.add(node)
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            if dfs_search(graph, neighbor, target, visited):
                return True
    
    return False


# DFS with path tracking
def dfs_path(graph, start, end, visited=None):
    """Returns path from start to end"""
    if visited is None:
        visited = set()
    
    if start == end:
        return [start]
    
    visited.add(start)
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            path = dfs_path(graph, neighbor, end, visited)
            if path:
                return [start] + path
    
    return None
```

## DFS Iterative (Using Stack)

```python
def dfs_iterative(graph, start):
    """
    Iterative DFS using explicit stack
    Time: O(V + E) | Space: O(V)
    """
    visited = set([start])
    stack = [start]
    result = []
    
    while stack:
        node = stack.pop()
        result.append(node)
        
        # Add neighbors in reverse for consistent order with recursive
        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    
    return result


# DFS without visited set (for backtracking)
def dfs_backtracking(graph, node, visited):
    """DFS that modifies visited in-place"""
    visited.add(node)
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_backtracking(graph, neighbor, visited)
    
    return visited
```

## DFS on Grid/Matrix

```python
def dfs_grid(grid, row, col, visited):
    """
    DFS on a 2D grid
    Time: O(M * N) | Space: O(M * N)
    """
    rows, cols = len(grid), len(grid[0])
    
    # Boundary and condition check
    if (row < 0 or row >= rows or col < 0 or col >= cols or
        (row, col) in visited or grid[row][col] == 0):
        return
    
    visited.add((row, col))
    
    # 4-directional movement
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        dfs_grid(grid, row + dr, col + dc, visited)


def dfs_grid_iterative(grid, start_row, start_col):
    """Iterative DFS on grid"""
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
| Feature | BFS | DFS |
|---------|-----|-----|
| Data Structure | Queue | Stack/Recursion |
| Shortest Path | Yes (unweighted) | No (but finds any path) |
| Memory | O(V) | O(V) worst case |
| Level Order | Yes | No |
| Cycle Detection | Yes | Yes (with colors) |
| Topological Sort | Yes (Kahn's) | Yes (reverse finish) |
| Connected Components | Yes | Yes |
| Grid Traversal | Yes | Yes |
| Bidirectional | Easy | Hard |
```

## Key Takeaways for DFS

```
1. DFS uses STACK (LIFO) or recursion - goes deep first
2. DFS is NATURAL for backtracking problems
3. DFS uses less memory than BFS in wide graphs
4. For grid problems, DFS is simpler to write (recursive)
5. For shortest path in UNWEIGHTED graph, use BFS
6. For checking if path EXISTS, use either
7. Pattern: check boundary BEFORE recursive call
8. Time: O(V + E) for graphs, O(M * N) for grids
9. Space: O(V) for visited + recursion stack
10. Use iterative DFS if recursion depth > 10^5
```
