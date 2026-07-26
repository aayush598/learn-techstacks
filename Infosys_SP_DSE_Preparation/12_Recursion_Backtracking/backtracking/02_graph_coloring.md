# Graph Coloring, Hamiltonian Path/Cycle, Maze & Knight Problems

## Table of Contents
1. [Graph Coloring Problem](#graph-coloring)
2. [M-Coloring Problem](#m-coloring)
3. [Hamiltonian Path](#hamiltonian-path)
4. [Hamiltonian Cycle](#hamiltonian-cycle)
5. [Rat in a Maze](#rat-in-a-maze)
6. [Knight's Tour](#knights-tour)

---

## Graph Coloring

### Problem
Assign colors to vertices of a graph such that no two adjacent vertices share the same color.

### Visual: What is Graph Coloring?

```
  GRAPH COLORING PROBLEM:
  ═══════════════════════

  Given a graph and m colors, color each vertex so
  no two ADJACENT (connected) vertices share a color.

  Example Graph:                 VALID 3-COLORING:
  (4 vertices, edges shown)      (R=Red, G=Green, B=Blue)

      0                           0 (R)
     /|\                          /|\
    / | \                        / | \
   1──┼──2                       1 (G)  2 (B)
   \  |  /                       \  |  /
    \ | /                        \ | /
      3                            3 (G)

  Edges: 0-1, 0-2, 0-3, 1-2, 2-3    0(R)≠1(G) ✓ 0(R)≠2(B) ✓
                                           0(R)≠3(G) ✓ 1(G)≠2(B) ✓
                                           2(B)≠3(G) ✓  ALL VALID!

  INVALID COLORING:
  0 (R)
  /|\
 1 (R) ← SAME COLOR as 0! ❌ INVALID
```

```python
def graph_coloring(graph, m):
    """
    graph: adjacency list, e.g. {0: [1,2], 1: [0,2], 2: [0,1]}
    m: number of colors available (indexed 0 to m-1)
    Returns: color assignment dict {vertex: color} or None
    """
    V = len(graph)
    colors = [-1] * V

    def is_safe(v, c):
        for neighbor in graph[v]:
            if colors[neighbor] == c:
                return False
        return True

    def backtrack(v):
        if v == V:
            return True  # all vertices colored

        for c in range(m):
            if not is_safe(v, c):
                continue
            colors[v] = c
            if backtrack(v + 1):
                return True
            colors[v] = -1  # undo

        return False

    if backtrack(0):
        return {i: colors[i] for i in range(V)}
    return None


# Example: 4-color theorem
graph = {
    0: [1, 2, 3],
    1: [0, 2],
    2: [0, 1, 3],
    3: [0, 2]
}
print(graph_coloring(graph, 3))
# {0: 0, 1: 1, 2: 2, 3: 1}
```

### Step-by-Step Walkthrough: Coloring the Example Graph

```
  Graph: 0-1, 0-2, 0-3, 1-2, 2-3    (4 vertices, 3 colors: R, G, B)
  ═══════════════════════════════════════════════════════════════════

  STEP 1: Color vertex 0
  ┌──────────┬──────────────────────────────────────────────┐
  │ Vertex 0 │ Try R → OK (no neighbors colored yet)       │
  │          │ colors = [R, _, _, _]                        │
  └──────────┴──────────────────────────────────────────────┘

  STEP 2: Color vertex 1 (neighbors: 0)
  ┌──────────┬──────────────────────────────────────────────┐
  │ Vertex 1 │ Try R → ❌ (0 is R, adjacent!)              │
  │          │ Try G → OK (only 0 is colored, 0=R≠G)       │
  │          │ colors = [R, G, _, _]                        │
  └──────────┴──────────────────────────────────────────────┘

  STEP 3: Color vertex 2 (neighbors: 0, 1)
  ┌──────────┬──────────────────────────────────────────────┐
  │ Vertex 2 │ Try R → ❌ (0 is R)                         │
  │          │ Try G → ❌ (1 is G)                          │
  │          │ Try B → OK (0=R, 1=G, neither is B)         │
  │          │ colors = [R, G, B, _]                        │
  └──────────┴──────────────────────────────────────────────┘

  STEP 4: Color vertex 3 (neighbors: 0, 2)
  ┌──────────┬──────────────────────────────────────────────┐
  │ Vertex 3 │ Try R → ❌ (0 is R)                         │
  │          │ Try G → OK (0=R, 2=B, neither is G)         │
  │          │ colors = [R, G, B, G]  ✓ ALL VERTICES DONE! │
  └──────────┴──────────────────────────────────────────────┘

  DECISION TREE:
  ══════════════
                          [ ]
                           │
                      ┌────┼────┐
                    col=0  col=1  col=2
                    [R]    [G]    [B]
                     │
               ┌─────┼─────┐
             col=0  col=1   col=2
             [R,R]  [R,G]   [R,B] ❌ (1 adj to 0)
              ❌      │       │
                 ┌────┼──┐   ┌──┼──┐
               col=0  col=1 col=0 col=1
              [R,G,R] [R,G,B] [R,B,R] [R,B,G] ❌
                 ❌      │       ❌      │
                    ┌────┼──┐        ┌───┼───┐
                  col=0  col=1     col=0  col=1
                 [R,G,B,R] [R,G,B,G] [R,B,G,R] [R,B,G,G]
                    ❌       ✓        ❌          ✓

  SOLUTIONS FOUND: [R,G,B,G] and [R,B,G,G]
  (and equivalents with different color labels)
```

**Complexity**: O(m^V) time (try all color assignments), O(V) space.

---

## M-Coloring Problem

### Problem
Determine if a graph can be colored with at most m colors such that no adjacent vertices share the same color. Count the number of valid colorings.

```python
def m_coloring_count(graph, m):
    """
    Returns the number of ways to color the graph with at most m colors.
    """
    V = len(graph)
    colors = [-1] * V
    count = 0

    def is_safe(v, c):
        for neighbor in graph[v]:
            if colors[neighbor] == c:
                return False
        return True

    def backtrack(v):
        nonlocal count
        if v == V:
            count += 1
            return

        for c in range(m):
            if not is_safe(v, c):
                continue
            colors[v] = c
            backtrack(v + 1)
            colors[v] = -1

    backtrack(0)
    return count


# Example
graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1, 3],
    3: [2]
}
print(m_coloring_count(graph, 3))  # 6 ways with 3 colors
print(m_coloring_count(graph, 4))  # 18 ways with 4 colors
```

### Optimized with constraint propagation

```python
def m_coloring_optimized(graph, m):
    V = len(graph)
    colors = [-1] * V
    # domain[v] = set of colors still available for vertex v
    domains = [set(range(m)) for _ in range(V)]
    count = [0]

    def is_safe(v, c):
        for neighbor in graph[v]:
            if colors[neighbor] == c:
                return False
        return True

    def propagate(v, c, removed):
        """Remove c from neighbors' domains. Track what was removed for undo."""
        for neighbor in graph[v]:
            if colors[neighbor] == -1 and c in domains[neighbor]:
                domains[neighbor].remove(c)
                removed.append((neighbor, c))

    def undo_propagate(removed):
        for v, c in removed:
            domains[v].add(c)

    def backtrack():
        # MRV (Minimum Remaining Values): pick uncolored vertex with smallest domain
        # This heuristic picks the most constrained variable first → fails faster
        uncolored = [v for v in range(V) if colors[v] == -1]
        if not uncolored:
            count[0] += 1
            return

        v = min(uncolored, key=lambda x: len(domains[x]))

        if not domains[v]:
            return  # dead end: no colors available for this vertex

        for c in list(domains[v]):
            if not is_safe(v, c):
                continue
            colors[v] = c
            removed = []
            propagate(v, c, removed)      # reduce neighbors' domains
            backtrack()                    # recurse
            undo_propagate(removed)        # restore neighbors' domains
            colors[v] = -1                 # undo coloring

    backtrack()
    return count[0]
```

### Visual: Constraint Propagation in Action

```
  GRAPH: 0-1, 0-2, 1-2, 2-3    (3 colors: R, G, B)
  ═══════════════════════════════════════════════════

  INITIAL STATE:
  ┌────────┬──────────────────────┬──────────┐
  │ Vertex │ Available Colors     │ MRV      │
  ├────────┼──────────────────────┼──────────┤
  │   0    │ {R, G, B}            │ 3        │
  │   1    │ {R, G, B}            │ 3        │
  │   2    │ {R, G, B}            │ 3        │
  │   3    │ {R, G, B}            │ 3        │
  └────────┴──────────────────────┴──────────┘

  STEP 1: Color vertex 2 with R (MRV picks any, let's say 2)
  ┌────────┬──────────────────────┬──────────┐
  │   0    │ {G, B}  (R removed)  │ 2 ← MRV │
  │   1    │ {G, B}  (R removed)  │ 2 ← MRV │
  │   2    │ [R] colored          │ -        │
  │   3    │ {G, B}  (R removed)  │ 2 ← MRV │
  └────────┴──────────────────────┴──────────┘

  STEP 2: Color vertex 0 with G (MRV picks from {G,B}, say G)
  ┌────────┬──────────────────────┬──────────┐
  │   0    │ [G] colored          │ -        │
  │   1    │ {B}  (G removed too) │ 1 ← MRV │
  │   2    │ [R] colored          │ -        │
  │   3    │ {G, B}               │ 2        │
  └────────┴──────────────────────┴──────────┘

  STEP 3: Color vertex 1 with B (only choice!)
  ┌────────┬──────────────────────┬──────────┐
  │   0    │ [G] colored          │ -        │
  │   1    │ [B] colored          │ -        │
  │   2    │ [R] colored          │ -        │
  │   3    │ {G}  (B removed too) │ 1 ← MRV │
  └────────┴──────────────────────┴──────────┘

  STEP 4: Color vertex 3 with G (only choice!)
  ALL VERTICES COLORED! ✓

  MRV HEURISTIC picks the most constrained vertex first,
  which often leads to earlier pruning and faster solutions.
```

---

## Hamiltonian Path

### Problem
Find a path in a graph that visits every vertex exactly once.

### Visual: Hamiltonian Path vs Cycle

```
  HAMILTONIAN PATH: Visit EVERY vertex exactly ONCE
  ═══════════════════════════════════════════════════

  Example Graph:
      0 ──── 1
      │╲     │
      │  ╲   │
      │   ╲  │
      2 ──── 3

  Valid Hamiltonian Paths:
  ┌──────────────────────────────────────────────────────┐
  │  0 → 1 → 2 → 3   (visits all 4 vertices once)       │
  │  0 → 1 → 3 → 2   ✓ valid                             │
  │  0 → 2 → 1 → 3   ✓ valid                             │
  │  0 → 2 → 3 → 1   ✓ valid                             │
  │  0 → 3 → 1 → 2   ✓ valid                             │
  │  0 → 3 → 2 → 1   ✓ valid                             │
  └──────────────────────────────────────────────────────┘

  NOT a Hamiltonian Path:
  0 → 1 → 2 → 0 → 3  ❌ (visits 0 twice!)

  HAMILTONIAN CYCLE: Path that returns to start
  ═══════════════════════════════════════════════
  0 → 1 → 3 → 2 → 0   ✓ visits all + returns to 0
  0 → 2 → 3 → 1 → 0   ✓ visits all + returns to 0

  NOT a Hamiltonian Cycle:
  0 → 1 → 2 → 3 → 0   ❌ (3→0 not connected in our graph)
```

```python
def hamiltonian_path(graph):
    """
    graph: adjacency list {0: [1, 2], 1: [0, 3], ...}
    Returns: list of vertices in Hamiltonian path order, or None
    """
    V = len(graph)
    visited = [False] * V
    path = []

    def backtrack(v):
        visited[v] = True
        path.append(v)

        if len(path) == V:
            return True  # all vertices visited

        for neighbor in graph[v]:
            if not visited[neighbor]:
                if backtrack(neighbor):
                    return True

        # Backtrack
        path.pop()
        visited[v] = False
        return False

    # Try starting from each vertex
    for start in range(V):
        if backtrack(start):
            return path
    return None


# Example
graph = {
    0: [1, 2],
    1: [0, 2, 3],
    2: [0, 1, 3],
    3: [1, 2]
}
print(hamiltonian_path(graph))
# [0, 1, 2, 3] or [0, 2, 1, 3] etc.
```

### Find ALL Hamiltonian Paths

```python
def all_hamiltonian_paths(graph):
    V = len(graph)
    result = []

    def backtrack(path, visited):
        if len(path) == V:
            result.append(path[:])
            return

        current = path[-1]
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                backtrack(path, visited)
                path.pop()
                visited.remove(neighbor)

    for start in range(V):
        backtrack([start], {start})

    return result


# Example
graph = {
    0: [1, 2],
    1: [0, 2, 3],
    2: [0, 1, 3],
    3: [1, 2]
}
paths = all_hamiltonian_paths(graph)
for p in paths:
    print(p)
# [0, 1, 2, 3], [0, 2, 1, 3], [1, 0, 2, 3], ...
```

**Complexity**: O(V!) time (try all orderings), O(V) space.

---

## Hamiltonian Cycle

### Problem
Find a cycle that visits every vertex exactly once and returns to the starting vertex.

```python
def hamiltonian_cycle(graph):
    V = len(graph)
    path = [0]  # start from vertex 0
    visited = {0}

    def backtrack():
        if len(path) == V:
            # Check if last vertex connects back to start
            if 0 in graph[path[-1]]:
                return True
            return False

        current = path[-1]
        for neighbor in graph[current]:
            if neighbor in visited:
                continue
            visited.add(neighbor)
            path.append(neighbor)
            if backtrack():
                return True
            path.pop()
            visited.remove(neighbor)

        return False

    if backtrack():
        return path + [0]  # close the cycle
    return None


# Example
graph = {
    0: [1, 2, 3],
    1: [0, 2],
    2: [0, 1, 3],
    3: [0, 2]
}
print(hamiltonian_cycle(graph))
# [0, 1, 2, 3, 0]
```

### Optimized: Reduce candidates using degree property

```python
def hamiltonian_cycle_optimized(graph):
    V = len(graph)

    # A vertex with degree < 2 cannot be in a Hamiltonian cycle
    for v in graph:
        if len(graph[v]) < 2:
            return None

    path = [0]
    visited = {0}

    def get_candidates(current):
        """Only try neighbors that could lead to a valid cycle."""
        candidates = []
        for neighbor in graph[current]:
            if neighbor in visited:
                continue
            # If we've visited all but 1 vertex, neighbor must connect to start
            if len(visited) == V - 1 and 0 not in graph[neighbor]:
                continue
            candidates.append(neighbor)
        return candidates

    def backtrack():
        if len(path) == V:
            return 0 in graph[path[-1]]

        current = path[-1]
        for neighbor in get_candidates(current):
            visited.add(neighbor)
            path.append(neighbor)
            if backtrack():
                return True
            path.pop()
            visited.remove(neighbor)
        return False

    if backtrack():
        return path + [0]
    return None


# Example
graph = {
    0: [1, 2, 3],
    1: [0, 2],
    2: [0, 1, 3],
    3: [0, 2]
}
print(hamiltonian_cycle_optimized(graph))
# [0, 1, 2, 3, 0]
```

**Complexity**: O(V!) time, O(V) space. The optimization prunes many branches.

---

## Rat in a Maze

### Problem
A rat starts at (0,0) in an N x N maze. Find a path to (N-1, N-1). 1 = open cell, 0 = wall. The rat can move right or down.

### Visual: Maze and Solution

```
  MAZE (1=open, 0=wall):           SOLUTION PATH:
  ═══════════════════════           ══════════════

  ┌───┬───┬───┬───┐                ┌───┬───┬───┬───┐
  │ 1 │ 0 │ 0 │ 0 │                │ R→│   │   │   │
  ├───┼───┼───┼───┤                ├───┼───┼───┼───┤
  │ 1 │ 1 │ 0 │ 1 │                │ R │ R→│   │   │
  ├───┼───┼───┼───┤                ├───┼───┼───┼───┤
  │ 0 │ 1 │ 0 │ 0 │                │   │ R │   │   │
  ├───┼───┼───┼───┤                ├───┼───┼───┼───┤
  │ 1 │ 1 │ 1 │ 1 │                │   │ R │ R→│ R │
  └───┴───┴───┴───┘                └───┴───┴───┴───┘
                                      R = path
  Start: (0,0)  End: (3,3)
  Path: (0,0)→(1,0)→(1,1)→(2,1)→(3,1)→(3,2)→(3,3)

  STEP-BY-STEP EXPLORATION:
  ═════════════════════════
  (0,0): Try RIGHT → (0,1) ❌ WALL!
         Try DOWN  → (1,0) ✓
  (1,0): Try RIGHT → (1,1) ✓
  (1,1): Try RIGHT → (1,2) ❌ WALL!
         Try DOWN  → (2,1) ✓
  (2,1): Try RIGHT → (2,2) ❌ WALL!
         Try DOWN  → (3,1) ✓
  (3,1): Try RIGHT → (3,2) ✓
  (3,2): Try RIGHT → (3,3) ✓ REACHED END!
```

### Basic version: Right and Down only

```python
def rat_in_maze(maze):
    N = len(maze)
    if maze[0][0] == 0 or maze[N-1][N-1] == 0:
        return []

    solution = [[0] * N for _ in range(N)]

    def backtrack(r, c):
        if r == N - 1 and c == N - 1:
            solution[r][c] = 1
            return True

        # Check bounds and validity
        if r < 0 or r >= N or c < 0 or c >= N:
            return False
        if maze[r][c] == 0 or solution[r][c] == 1:
            return False

        solution[r][c] = 1  # mark as part of path

        # Try moving right
        if backtrack(r, c + 1):
            return True
        # Try moving down
        if backtrack(r + 1, c):
            return True

        solution[r][c] = 0  # backtrack
        return False

    if backtrack(0, 0):
        return solution
    return []


# Example
maze = [
    [1, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 1, 0, 0],
    [1, 1, 1, 1]
]
result = rat_in_maze(maze)
for row in result:
    print(row)
# [1, 0, 0, 0]
# [1, 1, 0, 0]
# [0, 1, 0, 0]
# [0, 1, 1, 1]
```

### Extended version: All 4 directions

```python
def rat_in_maze_all_directions(maze):
    N = len(maze)
    if maze[0][0] == 0 or maze[N-1][N-1] == 0:
        return []

    solution = [[0] * N for _ in range(N)]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # R, D, L, U

    def backtrack(r, c):
        if r == N - 1 and c == N - 1:
            solution[r][c] = 1
            return True

        if r < 0 or r >= N or c < 0 or c >= N:
            return False
        if maze[r][c] == 0 or solution[r][c] == 1:
            return False

        solution[r][c] = 1

        for dr, dc in directions:
            if backtrack(r + dr, c + dc):
                return True

        solution[r][c] = 0
        return False

    if backtrack(0, 0):
        return solution
    return []
```

### Find ALL paths

```python
def all_paths_maze(maze):
    N = len(maze)
    result = []

    def backtrack(r, c, path):
        if r == N - 1 and c == N - 1:
            result.append(path[:()])
            return

        if r < 0 or r >= N or c < 0 or c >= N:
            return
        if maze[r][c] == 0:
            return

        maze[r][c] = 0  # mark visited

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            path.append((r + dr, c + dc))
            backtrack(r + dr, c + dc, path)
            path.pop()

        maze[r][c] = 1  # restore

    path = [(0, 0)]
    backtrack(0, 0, path)
    return result


# Example
maze = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]
paths = all_paths_maze(maze)
for p in paths:
    print(p)
```

**Complexity**: O(4^(N^2)) time worst case (4 directions, N^2 cells), O(N^2) space.

---

## Knight's Tour

### Problem
Find a sequence of moves for a knight on an N x N chessboard such that it visits every square exactly once.

### Visual: Knight Movement and Tour

```
  KNIGHT'S MOVES (L-shape: 2+1):
  ════════════════════════════════

  ┌───┬───┬───┬───┬───┐
  │   │ 1 │   │ 2 │   │    From center (2,2), knight can move to
  ├───┼───┼───┼───┼───┤    any cell marked with a number:
  │ 8 │   │   │   │ 3 │
  ├───┼───┼───┼───┼───┤    All 8 possible moves:
  │   │   │ K │   │   │    (±2, ±1) and (±1, ±2)
  ├───┼───┼───┼───┼───┤
  │ 7 │   │   │   │ 4 │    8 possible next positions
  ├───┼───┼───┼───┼───┤    from any interior square.
  │   │ 6 │   │ 5 │   │
  └───┴───┴───┴───┴───┘

  COMPLETE KNIGHT'S TOUR (5x5):
  ════════════════════════════════

  ┌────┬────┬────┬────┬────┐
  │  0 │ 17 │ 14 │  5 │  6 │
  ├────┼────┼────┼────┼────┤
  │ 13 │  4 │  7 │ 16 │ 15 │
  ├────┼────┼────┼────┼────┤
  │ 18 │ 12 │ 19 │  8 │  2 │
  ├────┼────┼────┼────┼────┤
  │  3 │ 20 │  9 │ 22 │ 11 │
  ├────┼────┼────┼────┼────┤
  │ 24 │ 23 │ 10 │ 21 │ 24 │
  └────┴────┴────┴────┴────┘

  Path traced: 0→17→14→5→6→15→...→24
  Each step is a valid L-shaped knight move!

  WARNSDORFF'S HEURISTIC:
  ════════════════════════
  At each step, move to the neighbor with the FEWEST onward moves.

  ┌──────────────────────────────────────────────────────┐
  │  Step 1: At (0,0)                                   │
  │  Possible moves: (1,2) and (2,1)                    │
  │  (1,2) has 6 onward moves, (2,1) has 6 onward moves │
  │  → Tie, pick either (say (2,1))                     │
  │                                                      │
  │  Step 2: At (2,1)                                   │
  │  Possible moves: (0,0)✗visited, (0,2), (1,3),       │
  │                   (3,3), (4,0), (4,2)               │
  │  (4,0) has 2 onward moves → FEWEST → pick (4,0)    │
  │                                                      │
  │  KEY INSIGHT: Greedy approach finds solution faster  │
  │  but doesn't guarantee one for all board sizes.     │
  └──────────────────────────────────────────────────────┘
```

### Backtracking Solution

```python
def knights_tour(n):
    board = [[-1] * n for _ in range(n)]
    # All 8 possible moves for a knight
    moves = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]

    def is_valid(r, c):
        return 0 <= r < n and 0 <= c < n and board[r][c] == -1

    def backtrack(r, c, count):
        board[r][c] = count

        if count == n * n - 1:
            return True  # all squares visited

        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc):
                if backtrack(nr, nc, count + 1):
                    return True

        board[r][c] = -1  # backtrack
        return False

    board[0][0] = 0
    if backtrack(0, 0, 1):
        return board
    return None


# Example for 5x5
result = knights_tour(5)
if result:
    for row in result:
        print(row)
```

### Warnsdorff's Heuristic (much faster)

```python
def knights_tour_warnsdorff(n):
    board = [[-1] * n for _ in range(n)]
    moves = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]

    def get_degree(r, c):
        """Count valid next moves from (r, c)."""
        count = 0
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and board[nr][nc] == -1:
                count += 1
        return count

    def backtrack(r, c, count):
        board[r][c] = count

        if count == n * n - 1:
            return True

        # Warnsdorff: try moves with fewest onward moves first
        candidates = []
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and board[nr][nc] == -1:
                degree = get_degree(nr, nc)
                candidates.append((degree, nr, nc))

        candidates.sort()  # sort by degree (ascending)

        for _, nr, nc in candidates:
            if backtrack(nr, nc, count + 1):
                return True

        board[r][c] = -1
        return False

    board[0][0] = 0
    if backtrack(0, 0, 1):
        return board
    return None


# Example
result = knights_tour_warnsdorff(6)
if result:
    for row in result:
        print(row)
```

### Iterative with Warnsdorff (fastest for large boards)

```python
def knights_tour_iterative(n):
    board = [[-1] * n for _ in range(n)]
    moves = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]

    def get_neighbors(r, c):
        result = []
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and board[nr][nc] == -1:
                result.append((nr, nc))
        return result

    r, c = 0, 0
    board[r][c] = 0

    for step in range(1, n * n):
        neighbors = get_neighbors(r, c)
        if not neighbors:
            return None  # stuck!

        # Warnsdorff: pick neighbor with fewest onward moves
        r, c = min(neighbors, key=lambda pos: len(get_neighbors(*pos)))
        board[r][c] = step

    return board


# Example
result = knights_tour_iterative(6)
if result:
    for row in result:
        print(' '.join(f'{x:2d}' for x in row))
```

**Complexity**:
- Brute force: O(8^(N^2)) — infeasible for N > 5
- Warnsdorff: O(N^2) — near-linear in practice
- The heuristic works well but doesn't guarantee a solution for all board sizes

---

## Summary Table

| Problem | State | Choices | Constraint | Time Complexity |
|---------|-------|---------|------------|----------------|
| Graph Coloring | vertex index | m colors | no adjacent same | O(m^V) |
| M-Coloring Count | vertex index | m colors | no adjacent same | O(m^V) |
| Hamiltonian Path | current vertex | unvisited neighbors | visit all once | O(V!) |
| Hamiltonian Cycle | current vertex | unvisited neighbors | visit all + return | O(V!) |
| Rat in Maze | position (r,c) | directions | valid cells only | O(4^(N^2)) |
| Knight's Tour | position (r,c) | 8 knight moves | visit all once | O(8^(N^2)) or O(N^2) w/ Warnsdorff |

### Quick-Reference: Problem → Technique Mapping

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │  GRAPH PROBLEMS THAT USE BACKTRACKING                               │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │  COLORING PROBLEMS                                                  │
  │  ├── Graph m-coloring: assign colors to vertices                   │
  │  ├── Map coloring: real-world maps (4-color theorem)               │
  │  └── Scheduling: no conflicts between connected tasks              │
  │                                                                     │
  │  PATH/CYCLE PROBLEMS                                                │
  │  ├── Hamiltonian Path: visit all vertices once                     │
  │  ├── Hamiltonian Cycle: visit all + return to start                │
  │  ├── Euler Path: traverse all EDGES once (different problem!)      │
  │  └── TSP: shortest path visiting all cities (optimization)         │
  │                                                                     │
  │  GRID/BOARD PROBLEMS                                                │
  │  ├── Rat in a Maze: find path through obstacles                    │
  │  ├── Knight's Tour: visit all squares with L-moves                 │
  │  ├── N-Queens: place queens without attacks                        │
  │  └── Sudoku: fill grid with constraint satisfaction                 │
  │                                                                     │
  │  COMMON OPTIMIZATIONS:                                              │
  │  • Use sets for O(1) constraint checks                              │
  │  • Check validity BEFORE recursing (not after)                      │
  │  • Return early when finding ONE solution                           │
  │  • Sort candidates and break early on bounds                        │
  │  • Use heuristics (MRV, Warnsdorff) for better pruning              │
  └─────────────────────────────────────────────────────────────────────┘
```

## Key Backtracking Patterns for These Problems

1. **Always check validity before recursing** — saves unnecessary stack frames
2. **Use sets for O(1) visited checks** — faster than arrays for sparse graphs
3. **Pruning**: 
   - Color: don't try colors already used by neighbors
   - Hamiltonian: only go to unvisited vertices
   - Maze: only move to open, unvisited cells
   - Knight: Warnsdorff's rule (most constrained first)
4. **Return early** when finding one solution vs counting all solutions
5. **Undo changes** before returning (backtrack step)
