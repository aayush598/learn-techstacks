# BFS Complete Guide

## What is BFS? — Visual Intuition

```
BFS = Breadth-First Search
Explores ALL neighbors at current depth BEFORE moving to next level.

Think of it as: Ripples spreading from a stone dropped in water.

         START at 0
            │
    ┌───────┼───────┐
    ▼       ▼       ▼
    1       2       3        ← Level 1: all direct neighbors
    │       │    ┌──┤
    ▼       ▼    ▼  ▼
    4       5    6  7        ← Level 2: neighbors of neighbors

BFS processes: 0 → 1,2,3 → 4,5,6,7

KEY INSIGHT: BFS guarantees SHORTEST PATH in unweighted graphs!
  Distance from 0 to 5 = 2 (0→2→5) — BFS finds this first!
```

## BFS Template

### Step-by-Step Walkthrough

```
Graph:
    0 -- 1
    |    |
    2 -- 3 -- 4

Adjacency list: {0:[1,2], 1:[0,3], 2:[0,3], 3:[1,2,4], 4:[3]}

BFS from node 0:

Step │ Queue    │ Pop │ Visited Set     │ Result
─────│──────────│─────│─────────────────│──────────
  1  │ [0]      │ --  │ {0}             │ []
  2  │ []       │  0  │ {0}             │ [0]
  3  │ [1, 2]   │ --  │ {0, 1, 2}      │ [0]
  4  │ [2]      │  1  │ {0, 1, 2}      │ [0, 1]
  5  │ [3]      │  2  │ {0, 1, 2, 3}   │ [0, 1, 2]
  6  │ [4]      │  3  │ {0, 1, 2, 3}   │ [0, 1, 2, 3]
  7  │ []       │  4  │ {0, 1, 2, 3, 4}│ [0, 1, 2, 3, 4]
  8  │ DONE     │ --  │ {0, 1, 2, 3, 4}│ [0, 1, 2, 3, 4]

Visual of the queue at each step:
  Step 1: | 0 |             ← Start: enqueue source
  Step 3: | 1 | 2 |         ← After popping 0, enqueue its neighbors
  Step 4: | 2 |             ← After popping 1, enqueue its unvisited neighbor (3)
  Step 5: | 3 |             ← After popping 2, enqueue its unvisited neighbor (3 already added)
  Step 6: | 4 |             ← After popping 3, enqueue its unvisited neighbor (4)
  Step 7: |                 ← After popping 4, no unvisited neighbors
```

```python
from collections import deque

def bfs_template(graph, start):
    """
    Standard BFS template for graph traversal
    Time: O(V + E) | Space: O(V)

    ALGORITHM:
    1. Add start node to queue and visited set
    2. While queue is not empty:
       a. Dequeue a node
       b. Process it
       c. Enqueue all unvisited neighbors (mark visited BEFORE enqueuing!)
    """
    visited = set([start])
    queue = deque([start])
    result = []

    while queue:
        node = queue.popleft()         # FIFO: process oldest first
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)  # Mark BEFORE adding to queue!
                queue.append(neighbor)

    return result


# BFS with distance tracking
def bfs_distance(graph, start):
    """
    Returns shortest distance from start to all reachable nodes
    Time: O(V + E) | Space: O(V)

    KEY INSIGHT: When we first visit a node, we've found the
    shortest path to it (because BFS explores level by level).
    """
    visited = {start: 0}   # node → distance from start
    queue = deque([start])

    while queue:
        node = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited[neighbor] = visited[node] + 1  # distance = parent's dist + 1
                queue.append(neighbor)

    return visited


# BFS with path reconstruction
def bfs_shortest_path(graph, start, end):
    """
    Returns shortest path from start to end
    Time: O(V + E) | Space: O(V)

    We store the PATH alongside each node in the queue.
    When we find the end, we return the path immediately.
    """
    if start == end:
        return [start]

    visited = {start}
    queue = deque([(start, [start])])  # (node, path_so_far)

    while queue:
        node, path = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in visited:
                new_path = path + [neighbor]
                if neighbor == end:
                    return new_path       # Found shortest path!
                visited.add(neighbor)
                queue.append((neighbor, new_path))

    return []  # No path found

## BFS on Grid/Matrix

### Visual: Grid BFS Step-by-Step

```
Grid BFS: Starting from (0,0) in this grid (1=walkable, 0=wall)

  Grid:              BFS Progress (distance from start):
  ┌───┬───┬───┬───┐  ┌───┬───┬───┬───┐
  │ 1 │ 1 │ 1 │ 0 │  │ 0 │ 1 │ 2 │ · │  ← Level 0: (0,0)
  ├───┼───┼───┼───┤  ├───┼───┼───┼───┤  ← Level 1: (0,1),(1,0)
  │ 1 │ 0 │ 1 │ 1 │  │ 1 │ · │ 3 │ 4 │  ← Level 2: (0,2),(2,0)
  ├───┼───┼───┼───┤  ├───┼───┼───┼───┤  ← Level 3: (1,2),(2,1)
  │ 1 │ 1 │ 1 │ 1 │  │ 2 │ 3 │ 4 │ 5 │  ← Level 4: (1,3),(2,2)
  └───┴───┴───┴───┘  └───┴───┴───┴───┘  ← Level 5: (2,3)

  4-directional moves from (r, c):
  ┌─────────────────────────────┐
  │  (r-1, c)  ← UP            │
  │  (r+1, c)  ← DOWN          │
  │  (r, c-1)  ← LEFT          │
  │  (r, c+1)  ← RIGHT         │
  └─────────────────────────────┘

  Directions array: [(-1,0), (1,0), (0,-1), (0,1)]
```

```python
from collections import deque

def bfs_grid(grid, start_row, start_col):
    """
    BFS on a 2D grid
    Time: O(M * N) | Space: O(M * N)

    STEP-BY-STEP:
    1. Initialize queue with start cell
    2. For each cell, try all 4 directions
    3. Check bounds, visited, and walkable before enqueuing
    """
    if not grid or not grid[0]:
        return []

    rows, cols = len(grid), len(grid[0])
    visited = set([(start_row, start_col)])
    queue = deque([(start_row, start_col)])
    result = []

    while queue:
        r, c = queue.popleft()
        result.append((r, c))

        # 4-directional movement: up, down, left, right
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check: in bounds? Not visited? Walkable?
            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in visited and grid[nr][nc] == 1):
                visited.add((nr, nc))
                queue.append((nr, nc))

    return result


# 8-directional movement (includes diagonals)
def bfs_grid_8(grid, start_row, start_col):
    """
    BFS with 8-directional movement
    Useful for: "number of islands" variants where diagonals connect
    """
    rows, cols = len(grid), len(grid[0])
    visited = set([(start_row, start_col)])
    queue = deque([(start_row, start_col)])

    while queue:
        r, c = queue.popleft()

        # 8 directions: all combinations of -1, 0, 1 (except 0,0)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip (0,0) — that's the current cell
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and
                    (nr, nc) not in visited):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
```

## Level Order Traversal

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_order(root):
    """
    Level order traversal of binary tree
    Time: O(N) | Space: O(N)
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)
    
    return result


# Zigzag level order
def zigzag_level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    left_to_right = True
    
    while queue:
        level_size = len(queue)
        level = deque()
        
        for _ in range(level_size):
            node = queue.popleft()
            
            if left_to_right:
                level.append(node.val)
            else:
                level.appendleft(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(list(level))
        left_to_right = not left_to_right
    
    return result
```

## Shortest Path in Unweighted Graph

```python
from collections import deque

def shortest_path_unweighted(graph, start, end):
    """
    BFS finds shortest path in unweighted graph
    Time: O(V + E) | Space: O(V)
    """
    if start == end:
        return [start]
    
    visited = {start}
    queue = deque([(start, [start])])
    
    while queue:
        node, path = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                new_path = path + [neighbor]
                if neighbor == end:
                    return new_path
                visited.add(neighbor)
                queue.append((neighbor, new_path))
    
    return []


# Return distance only
def shortest_distance(graph, start, end):
    if start == end:
        return 0
    
    visited = {start: 0}
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited[neighbor] = visited[node] + 1
                if neighbor == end:
                    return visited[neighbor]
                queue.append(neighbor)
    
    return -1


# Example
graph = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 5],
    3: [1],
    4: [1, 5],
    5: [2, 4]
}

print(shortest_distance(graph, 0, 5))  # 2 (0 -> 2 -> 5)
print(shortest_path_unweighted(graph, 0, 5))  # [0, 2, 5]
```

## Rotting Oranges (Multi-Source BFS)

### Visual: Multi-Source BFS

```
MULTI-SOURCE BFS = Start from MULTIPLE nodes simultaneously!
Instead of 1 source, add ALL sources to queue initially.

  Rotting Oranges (LeetCode 994):
  0 = empty, 1 = fresh orange, 2 = rotten

  Minute 0:           Minute 1:           Minute 2:
  ┌───┬───┬───┐       ┌───┬───┬───┐       ┌───┬───┬───┐
  │ 2 │ 1 │ 0 │       │ 2 │ 2 │ 0 │       │ 2 │ 2 │ 0 │
  ├───┼───┼───┤       ├───┼───┼───┤       ├───┼───┼───┤
  │ 0 │ 1 │ 1 │  ──►  │ 0 │ 2 │ 1 │  ──►  │ 0 │ 2 │ 2 │
  ├───┼───┼───┤       ├───┼───┼───┤       ├───┼───┼───┤
  │ 1 │ 0 │ 1 │       │ 1 │ 0 │ 1 │       │ 2 │ 0 │ 2 │
  └───┴───┴───┘       └───┴───┴───┘       └───┴───┴───┘

  Queue starts with ALL rotten oranges: [(0,0)]
  After minute 1: queue has [(0,1), (1,1)]
  After minute 2: queue has [(1,2), (2,0), (2,2)]
  All fresh → return 2 minutes

  KEY PATTERN:
  ┌──────────────────────────────────────────────────────────┐
  │ for _ in range(len(queue)):  ← process ONE level = 1 min│
  │     r, c = queue.popleft()                               │
  │     for each neighbor:                                   │
  │         if fresh: rot it, add to queue                   │
  └──────────────────────────────────────────────────────────┘
```

```python
from collections import deque

def oranges_rotting(grid):
    """
    LeetCode 994 - Find minutes until all oranges rot
    Multi-source BFS: start from all rotten oranges simultaneously
    Time: O(M * N) | Space: O(M * N)
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0

    # Initialize: find ALL rotten oranges (multi-source!)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))   # Add all rotten to queue
            elif grid[r][c] == 1:
                fresh += 1             # Count fresh oranges

    if fresh == 0:
        return 0   # Nothing to rot

    minutes = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        minutes += 1
        # Process ALL currently rotten oranges (one minute's worth)
        for _ in range(len(queue)):
            r, c = queue.popleft()

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and
                    grid[nr][nc] == 1):
                    grid[nr][nc] = 2       # Rot it
                    fresh -= 1
                    queue.append((nr, nc))  # It can now rot neighbors

        if fresh == 0:
            return minutes

    return -1  # Some oranges remain fresh (impossible)
```

## Walls and Gates

```python
from collections import deque

def walls_and_gates(rooms):
    """
    LeetCode 286 - Fill each empty room with distance to nearest gate
    Multi-source BFS starting from all gates
    Time: O(M * N) | Space: O(M * N)
    """
    if not rooms or not rooms[0]:
        return
    
    rows, cols = len(rooms), len(rooms[0])
    queue = deque()
    INF = 2147483647
    
    # Start from all gates
    for r in range(rows):
        for c in range(cols):
            if rooms[r][c] == 0:
                queue.append((r, c))
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        r, c = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols and 
                rooms[nr][nc] == INF):
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))
    
    return rooms


# Example
rooms = [
    [2147483647, -1, 0, 2147483647],
    [2147483647, 2147483647, 2147483647, -1],
    [2147483647, -1, 2147483647, -1],
    [0, -1, 2147483647, 2147483647]
]
print(walls_and_gates(rooms))
# [[3, -1, 0, 1], [2, 2, 1, -1], [1, -1, 2, -1], [0, -1, 3, 4]]
```

## Word Ladder

```python
from collections import deque

def word_ladder(begin_word, end_word, word_list):
    """
    LeetCode 127 - Shortest transformation sequence
    BFS on word graph
    Time: O(M² * N) where M = word length, N = word list size
    Space: O(M² * N)
    """
    word_set = set(word_list)
    if end_word not in word_set:
        return 0
    
    queue = deque([(begin_word, 1)])
    visited = set([begin_word])
    
    while queue:
        word, length = queue.popleft()
        
        # Try changing each character
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]
                
                if new_word == end_word:
                    return length + 1
                
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, length + 1))
    
    return 0


# Alternative: Bi-directional BFS (faster)
def word_ladder_bidirectional(begin_word, end_word, word_list):
    if end_word not in word_list:
        return 0
    
    word_set = set(word_list)
    front = {begin_word}
    back = {end_word}
    length = 1
    
    while front and back:
        # Always expand smaller set
        if len(front) > len(back):
            front, back = back, front
        
        next_front = set()
        for word in front:
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    new_word = word[:i] + c + word[i+1:]
                    
                    if new_word in back:
                        return length + 1
                    
                    if new_word in word_set:
                        next_front.add(new_word)
                        word_set.remove(new_word)
        
        front = next_front
        length += 1
    
    return 0
```

## Clone Graph

```python
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph_bfs(node):
    """
    LeetCode 133 - Deep copy of graph using BFS
    Time: O(V + E) | Space: O(V)
    """
    if not node:
        return None
    
    cloned = {node: Node(node.val)}
    queue = deque([node])
    
    while queue:
        curr = queue.popleft()
        
        for neighbor in curr.neighbors:
            if neighbor not in cloned:
                cloned[neighbor] = Node(neighbor.val)
                queue.append(neighbor)
            cloned[curr].neighbors.append(cloned[neighbor])
    
    return cloned[node]
```

## Number of Islands (BFS)

```python
from collections import deque

def num_islands(grid):
    """
    LeetCode 200 - Count islands using BFS
    Time: O(M * N) | Space: O(M * N)
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def bfs(r, c):
        queue = deque([(r, c)])
        grid[r][c] = '0'  # Mark visited
        
        while queue:
            row, col = queue.popleft()
            
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < rows and 0 <= nc < cols and 
                    grid[nr][nc] == '1'):
                    grid[nr][nc] = '0'
                    queue.append((nr, nc))
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                bfs(r, c)
                count += 1
    
    return count
```

## BFS Template for Grid Problems

```python
from collections import deque

def bfs_grid_template(grid, start, end=None):
    """
    Universal BFS template for grid problems
    Customize the condition check and movement
    """
    if not grid or not grid[0]:
        return -1
    
    rows, cols = len(grid), len(grid[0])
    visited = set([start])
    queue = deque([start])
    distance = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            
            # Check if reached destination
            if end and (r, c) == end:
                return distance
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                # Customize this condition based on problem
                if (0 <= nr < rows and 0 <= nc < cols and 
                    (nr, nc) not in visited and 
                    grid[nr][nc] != 'X'):  # Not blocked
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        
        distance += 1
    
    return -1
```

## Key Takeaways for BFS

```
1. BFS uses QUEUE (FIFO) - process nodes level by level
2. BFS finds SHORTEST PATH in unweighted graphs
3. Multi-source BFS: Initialize queue with multiple starting points
4. Grid BFS: 4 directions (up/down/left/right) for most problems
5. Time: O(V + E) for graphs, O(M * N) for grids
6. Space: O(V) for visited set + queue
7. Use BFS when:
   - Finding shortest path in unweighted graph
   - Level-order traversal
   - Multi-source propagation (rotting oranges)
   - Checking if graph is bipartite
8. Pattern: visited check BEFORE adding to queue, not after

CRITICAL MISTAKE TO AVOID:
┌─────────────────────────────────────────────────────────┐
│  WRONG: Check visited AFTER popping from queue          │
│  → Node gets added to queue multiple times!             │
│  → Wastes memory and time                               │
│                                                         │
│  RIGHT: Check visited BEFORE adding to queue            │
│  → Each node enters queue exactly once                  │
│  → Guarantees O(V + E) time complexity                  │
└─────────────────────────────────────────────────────────┘

Complexity Analysis:
┌────────────────────┬──────────────┬──────────────┐
│ Operation          │ Graph BFS    │ Grid BFS     │
├────────────────────┼──────────────┼──────────────┤
│ Time Complexity    │ O(V + E)     │ O(M × N)     │
│ Space Complexity   │ O(V)         │ O(M × N)     │
│ Queue Max Size     │ O(V)         │ O(M × N)     │
│ Visited Set Size   │ O(V)         │ O(M × N)     │
└────────────────────┴──────────────┴──────────────┘

Common Patterns:
┌─────────────────────────┬───────────────────────────────┐
│ Problem Type            │ BFS Variant                   │
├─────────────────────────┼───────────────────────────────┤
│ Shortest path (unwt.)   │ Standard BFS with distance    │
│ Level order (tree)      │ BFS with level size tracking  │
│ Multi-source spread     │ BFS with multiple start nodes │
│ Bipartite check         │ BFS with 2-coloring           │
│ Word transformation     │ BFS on implicit word graph    │
│ Clone graph             │ BFS with hash map             │
└─────────────────────────┴───────────────────────────────┘
```
