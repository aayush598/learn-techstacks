# Graph Problems — Infosys SP DSE Preparation

> **35 problems** covering BFS, DFS, Union-Find, Topological Sort, Dijkstra, Tarjan, and more.
> Every solution is self-contained Python. Copy-paste ready.

---

## EASY (Problems 1–10)

---





### 1. Number of Islands

**Problem:** Given an `m x n` grid of `'1'`s (land) and `'0'`s (water), count the number of islands. An island is formed by connecting adjacent lands horizontally or vertically.

**Approach:** Traverse the grid. When you find an unvisited `'1'`, increment the count and run BFS/DFS to mark all connected `'1'`s as visited.

**Code:**
```python
# numIslands: implement solution
def numIslands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    return count
```

**Complexity:** O(m × n) time, O(m × n) worst-case recursion stack.

**Tip:** Use iterative BFS if the grid is very large to avoid stack overflow.

**Visual Walkthrough:**
```
Grid:              After DFS marking:
1 1 0 0 1          0 0 0 0 1
1 1 0 0 0    →     0 0 0 0 0
0 0 1 0 0          0 0 1 0 0
0 0 0 1 1          0 0 0 1 1

Island 1: (0,0)→(0,1)→(1,0)→(1,1) — DFS floods entire component
Island 2: (0,4) — single cell
Island 3: (2,2) — single cell  
Island 4: (3,3)→(3,4) — connected horizontally
Total: 4 islands
```

**Brute Force vs Optimal:**
| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| DFS (recursive) | O(m×n) | O(m×n) stack | Simple, may overflow |
| **BFS (iterative)** | **O(m×n)** | **O(min(m,n))** | **Safe for large grids** |
| Union-Find | O(m×n × α(mn)) | O(m×n) | Advanced, union cells |

**Common Mistakes:**
- Modifying grid while iterating (use visited set or mark in-place)
- Not checking all 4 directions (up, down, left, right)
- Forgetting diagonal is NOT connected (unless problem says 8-directional)
- Stack overflow on large grids (use iterative BFS instead of recursive DFS)

**Edge Cases:**
- Empty grid → return 0
- All 1s → return 1
- All 0s → return 0
- Single cell → return 0 or 1 depending on value

**Pattern Recognition:**
**Grid DFS/BFS Pattern**: Traverse grid, when you find an unvisited cell that starts a new component, increment count and flood-fill/mark all connected cells. Used in: Number of Islands, Number of Provinces, Max Area of Island, Surrounded Regions.

---





### 2. Flood Fill

**Problem:** Given an image (2D array), a starting pixel `(sr, sc)`, and a new color, replace the color of the starting pixel and all adjacent pixels of the same original color with the new color.

**Approach:** DFS from the starting pixel. For each cell matching the original color, change it to the new color and recurse to 4 neighbors.

**Code:**
```python
# floodFill: implement solution
def floodFill(image, sr, sc, newColor):
    rows, cols = len(image), len(image[0])
    orig = image[sr][sc]
    if orig == newColor:
        return image

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or image[r][c] != orig:
            return
        image[r][c] = newColor
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    dfs(sr, sc)
    return image
```

**Complexity:** O(m × n) time, O(m × n) stack space.

**Tip:** Early return if `orig == newColor` to avoid infinite recursion.

**Visual Walkthrough:**
```
image = [[1,1,1],[1,1,0],[1,0,1]], sr=1, sc=1, newColor=2

Before (orig=1):        After:
1 1 1                   2 2 2
1 1 0                   2 2 0
1 0 1                   2 0 1

DFS from (1,1):
(1,1): orig=1 → change to 2
  (0,1): orig=1 → change to 2
    (0,0): orig=1 → change to 2
      (-1,0): out of bounds ←
    (1,0): orig=1 → change to 2
      ...
  (2,1): orig=0 ≠ 1 ← stop
  (1,0): already visited
  (1,2): orig=0 ≠ 1 ← stop
```

**Brute Force vs Optimal:**
| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| DFS (recursive) | O(m×n) | O(m×n) | Simple recursion, may overflow |
| **BFS (iterative)** | **O(m×n)** | **O(m×n)** | **Queue-based, safe for large** |
| Stack (iterative) | O(m×n) | O(m×n) | Manual stack, avoids recursion limit |

**Common Mistakes:**
- Not handling `orig == newColor` → infinite recursion
- Forgetting to check bounds before accessing array
- Not marking visited (or changing color) before recursing → potential stack overflow

**Edge Cases:**
- Single pixel → return image as-is
- `orig == newColor` → return image immediately (no change needed)
- Starting pixel at corner → only 2 directions to check

**Pattern Recognition:**
**Grid DFS/BFS Flood Fill**: Standard flood fill from seed point. Used in: Number of Islands, Paint Bucket Tool.


---





### 3. Find if Path Exists in Graph

**Problem:** Given `n` nodes and a list of edges, determine if there is a path from `source` to `destination`.

**Approach:** Build adjacency list, then BFS/DFS from source. Return True if destination is reached.

**Code:**
```python
# validPath: implement solution
def validPath(n, edges, source, destination):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set([source])
    queue = deque([source])
    while queue:
        node = queue.popleft()
        if node == destination:
            return True
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                queue.append(nei)
    return False
```

**Complexity:** O(n + e) time, O(n + e) space.

**Tip:** Union-Find is also valid here — unite all edges, then check `find(source) == find(destination)`.

**Visual Walkthrough:**
```
n=6, edges=[[0,1],[0,2],[3,5],[5,4],[4,3]], source=0, destination=5

Graph:
0 ─ 1    3 ─ 5
│        │
2        4

BFS from 0:
Queue=[0], visited={0}
Visit 0 → neighbors={1,2} → queue=[1,2]
Visit 1 → neighbors={0} → all visited
Visit 2 → neighbors={0} → all visited
Queue empty, 5 never reached

Answer: False (disconnected graph)
```

**Brute Force vs Optimal:**
| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| BFS | O(V+E) | O(V) | Queue-based, shortest path in unweighted |
| DFS (recursive) | O(V+E) | O(V) | May overflow stack |
| **Union-Find** | **O(V+E·α(V))** | **O(V)** | **Best for static connectivity queries** |

**Common Mistakes:**
- Forgetting to add reverse edges (graph is undirected)
- Not using visited set → infinite loop in cycles
- Not handling source == destination case

**Edge Cases:**
- source == destination → True
- Disconnected graph → False (if source and dest in different components)
- Single node with no edges → True if source == dest

**Pattern Recognition:**
**Graph Traversal (Connectivity)**: BFS/DFS from source to check reachability. Used in: All Paths From Source to Target, Can Visit All Rooms.


---





### 4. Find Center of Star Graph

**Problem:** A star graph has one center node connected to all other nodes. Given `n` nodes and `edges`, find the center.

**Approach:** The center appears in every edge. Just check the first two edges — the common node is the center.

**Code:**
```python
# findCenter: implement solution
def findCenter(edges):
    a, b = edges[0]
    c, d = edges[1]
    if a == c or a == d:
        return a
    return b
```

**Complexity:** O(1) time, O(1) space.

**Tip:** No need to build the full graph. Two edges are enough because the center is in all of them.

**Visual Walkthrough:**
```
n=5, edges=[[1,2],[2,3],[4,2]]

Star graph center is the common node in all edges.

First edge: [1,2] → candidates = {1, 2}
Second edge: [2,3] → common = {1,2} ∩ {2,3} = {2}
Center = 2

Proof: The center appears in EVERY edge of a star graph.
Just check first 2 edges for the common node.
```

**Brute Force vs Optimal:**
| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| Count degrees | O(V) | O(V) | Count occurrences of each node |
| **First 2 edges** | **O(1)** | **O(1)** | **Center is common node in first 2 edges** |

**Common Mistakes:**
- Building the full graph (O(n)) when O(1) suffices
- Forgetting that star center appears in every edge
- Not handling n < 3 (but problem guarantees at least 3 nodes)

**Edge Cases:**
- Minimum n=3 per problem constraints
- First edge contains the center
- Two edges always enough to identify center

**Pattern Recognition:**
**Star Graph Property**: Center node appears in all edges. Check first two edges.


---





### 5. Maximum Number of Vowels in a Substring of Given Length

**Problem:** Given a string `s` and integer `k`, find the maximum number of vowels in any substring of length `k`. *(This is a sliding window problem often grouped with graph BFS thinking.)*

**Approach:** Sliding window of size `k`. Count vowels in the first window, then slide and update.

**Code:**
```python
# maxVowels: implement solution
def maxVowels(s, k):
    vowels = set('aeiou')
    count = sum(1 for c in s[:k] if c in vowels)
    mx = count
    for i in range(k, len(s)):
        count += (s[i] in vowels)
        count -= (s[i - k] in vowels)
        mx = max(mx, count)
    return mx
```

**Complexity:** O(n) time, O(1) space.

**Tip:** Use a set for O(1) vowel lookups.

**Visual Walkthrough:**
```
s = "abciiidef", k = 3

Sliding window:
Window "abc": vowels=1 (a)
Window "bci": vowels=1 (i)
Window "cii": vowels=2 (i,i) → max
Window "iii": vowels=3 (i,i,i) → max ✓
Window "iid": vowels=2 (i,i)
Window "ide": vowels=2 (i,e)
Window "def": vowels=1 (e)

Answer: 3 (window "iii")
```

**Brute Force vs Optimal:**
| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| Brute Force | O(n×k) | O(1) | Check each window individually |
| **Sliding Window** | **O(n)** | **O(1)** | **Slide, add right, subtract left** |

**Common Mistakes:**
- Forgetting to use a set for O(1) vowel lookup
- Off-by-one: adding and removing at the right positions
- Not handling k > len(s) case

**Edge Cases:**
- k > len(s) → can't form any valid window (treat as 0, though problem likely has k ≤ n)
- All vowels → k
- No vowels → 0

**Pattern Recognition:**
**Sliding Window (Fixed Size)**: Slide window of size k, update count incrementally. Used in: Max Consecutive Ones, Permutation in String.


---





### 6. Rotting Oranges

**Problem:** Given a grid where `0` = empty, `1` = fresh, `2` = rotten. Each minute, rotten orange rots adjacent fresh ones. Return minutes until no fresh orange left, or `-1` if impossible.

**Approach:** Multi-source BFS. Enqueue all rotten oranges at minute 0. BFS layer by layer, counting minutes.

**Code:**
```python
# orangesRotting: implement solution
from collections import deque

def orangesRotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    if fresh == 0:
        return 0
    minutes = 0
    while queue:
        minutes += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
    return minutes - 1 if fresh == 0 else -1
```

**Complexity:** O(m × n) time, O(m × n) space.

**Tip:** Multi-source BFS naturally computes the minimum time because all rotten sources expand simultaneously.

**Visual Walkthrough:**
```
Initial:              Minute 1:            Minute 2:
2 1 1                 2 2 1                2 2 2
1 1 0       →         2 1 0       →        2 2 0
0 1 1                 0 1 1                0 2 2

All rotten at minute 2 → return 2
BFS layers expand simultaneously from all rotten oranges
```

**Brute Force vs Optimal:**
| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| Simulation | O((m×n)²) | O(m×n) | Simulate minute by minute |
| **Multi-source BFS** | **O(m×n)** | **O(m×n)** | **Optimal: all sources expand together** |

**Common Mistakes:**
- Forgetting to count initial fresh oranges → can't detect impossible case
- Off-by-one in minutes (return `minutes - 1` not `minutes`)
- Not handling case where some fresh oranges remain unreachable → return -1

**Edge Cases:**
- No fresh oranges initially → return 0
- Some fresh oranges unreachable → return -1
- Single cell grid → return 0

**Pattern Recognition:**
**Multi-Source BFS**: When multiple starting points expand simultaneously (rotting, fire spreading, water flow), enqueue all sources at once. BFS layer = one time step. Used in: Rotting Oranges, 01 Matrix, Walls and Gates, As Far from Land as Possible.

---





### 7. Is Graph Bipartite

**Problem:** Given an adjacency matrix of an undirected graph, return `True` if the graph is bipartite (2-colorable).

**Approach:** Try coloring with 2 colors using BFS/DFS. If any adjacent nodes have the same color, it's not bipartite.

**Code:**
```python
# isBipartite: implement solution
def isBipartite(graph):
    n = len(graph)
    color = [-1] * n

    for i in range(n):
        if color[i] != -1:
            continue
        stack = [i]
        color[i] = 0
        while stack:
            node = stack.pop()
            for nei in graph[node]:
                if color[nei] == -1:
                    color[nei] = 1 - color[node]
                    stack.append(nei)
                elif color[nei] == color[node]:
                    return False
    return True
```

**Complexity:** O(V + E) time, O(V) space.

**Tip:** The graph may be disconnected — loop over all nodes to handle components.

**Visual Walkthrough:**
```
graph = [[1,2,3],[0,2],[0,1,3],[0,2]]

0 ─ 1
│ ╱ │
│ ╱ │
2 ─ 3

Color with BFS:
Color 0 = RED
  Neighbors {1,2,3} = BLUE
    1's neighbors {0(RED),2,3} → check 2: 2 is BLUE but 1's neighbor? 
    This graph has an odd cycle (0-1-2-0, length 3) → NOT bipartite

Use BFS coloring: if neighbor has same color as current → not bipartite
```

**Brute Force vs Optimal:**
| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| BFS coloring | O(V+E) | O(V) | Level-by-level, alternating colors |
| DFS coloring | O(V+E) | O(V) | Recursive, may overflow |
| **Union-Find** | **O(V+E)** | **O(V)** | **Graph splitting approach** |

**Common Mistakes:**
- Not handling disconnected components (each component must be bipartite)
- Checking only one component and assuming whole graph is bipartite
- Forgetting the graph may have self-loops (always not bipartite)

**Edge Cases:**
- Single node → bipartite
- Empty graph → bipartite
- Odd cycle (triangle) → NOT bipartite
- Even cycle (square) → bipartite

**Pattern Recognition:**
**Graph Bipartite Coloring**: 2-color graph with BFS/DFS, check for conflicts. Used in: Possible Bipartition, Is Graph Bipartite.


---





### 8. Number of Provinces

**Problem:** Given an `n x n` adjacency matrix `isConnected`, find the number of connected components (provinces).

**Approach:** Run DFS/BFS from each unvisited node, counting the number of DFS calls needed to visit all nodes.

**Code:**
```python
# findCircleNum: implement solution
def findCircleNum(isConnected):
    n = len(isConnected)
    visited = set()
    count = 0

    def dfs(node):
        visited.add(node)
        for nei in range(n):
            if isConnected[node][nei] == 1 and nei not in visited:
                dfs(nei)

    for i in range(n):
        if i not in visited:
            count += 1
            dfs(i)
    return count
```

**Complexity:** O(n²) time, O(n) space.

**Tip:** Union-Find also works — unite connected nodes and count unique roots.

**Visual Walkthrough:**
```
isConnected = [[1,1,0],[1,1,0],[0,0,1]]

Matrix:
  0 1 2
0 1 1 0
1 1 1 0
2 0 0 1

Graph: 0 ─ 1, 2 (isolated)

DFS from 0: visit {0,1}
DFS from 2: visit {2}
Provinces = 2

Key: Use adjacency matrix (isConnected[i][j] = 1 means edge i-j)
```

**Brute Force vs Optimal:**
| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| DFS | O(n²) | O(n) | Visit neighbors via matrix |
| BFS | O(n²) | O(n) | Queue-based traversal |
| **Union-Find** | **O(n²)** | **O(n)** | **Union all connected pairs, count roots** |

**Common Mistakes:**
- Confusing adjacency matrix index with node value
- Not marking visited before recursing through neighbors
- Forgetting the graph is undirected (matrix[i][j] = matrix[j][i])

**Edge Cases:**
- n=1 → 1 province
- All connected → 1 province
- All isolated → n provinces

**Pattern Recognition:**
**Component Counting (Adjacency Matrix)**: DFS/BFS from each unvisited node. Used in: Friend Circles, Number of Connected Components.


---





### 9. Clone Graph

**Problem:** Given a reference to a node in a connected undirected graph, return a deep copy of the graph.

**Approach:** BFS/DFS with a hashmap mapping original nodes to cloned nodes. For each node, clone it and recurse on unvisited neighbors.

**Code:**
```python
# cloneGraph: implement solution
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors or []

def cloneGraph(node):
    if not node:
        return None
    from collections import deque
    clones = {node: Node(node.val)}
    queue = deque([node])
    while queue:
        curr = queue.popleft()
        for nei in curr.neighbors:
            if nei not in clones:
                clones[nei] = Node(nei.val)
                queue.append(nei)
            clones[curr].neighbors.append(clones[nei])
    return clones[node]
```

**Complexity:** O(V + E) time, O(V) space.

**Tip:** The hashmap prevents re-cloning. Always check `if nei not in clones` before creating.

**Visual Walkthrough:**
```
Original: 1 ── 2
          │    │
          3 ── 4

Cloning process:
dfs(1): clone node 1 → {1'}
  dfs(2): clone node 2 → {1'─2'}
    dfs(1): already cloned (visited) → add 1' to 2'.neighbors
    dfs(4): clone 4 → {1'─2'─4'}
      dfs(2): already cloned
      dfs(3): clone 3 → {1'─2'─4'─3'}
        dfs(1): already cloned
        dfs(4): already cloned
      3'.neighbors = [1',4']
    4'.neighbors = [2',3']
  2'.neighbors = [1',4']
  dfs(3): already cloned → add 3' to 1'.neighbors
1'.neighbors = [2',3']

Clone complete! Structure matches original exactly.
```

**Brute Force vs Optimal:**
| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| **DFS + HashMap** | **O(V+E)** | **O(V)** | **Recursive, map original→clone** |
| BFS + HashMap | O(V+E) | O(V) | Iterative queue approach |

**Common Mistakes:**
- Shallow copy (new node but same neighbor references)
- Not checking visited map before recursing → stack overflow from cycles
- Forgetting to clone all neighbors (not just first)

**Edge Cases:**
- Empty graph (None) → return None
- Single node (no neighbors) → return cloned node
- Disconnected graph → all components cloned via hashmap

**Pattern Recognition:**
**Graph Clone with HashMap**: DFS/BFS + map<original→clone>. Used in: Copy List with Random Pointer, Clone Graph.


---





### 10. Find the Town Judge

**Problem:** `n` people labeled `1` to `n`. Town judge trusts nobody, everybody trusts the town judge. Given `trust` array `[a, b]` meaning `a` trusts `b`, find the town judge or return `-1`.

**Approach:** Compute in-degree minus out-degree for each person. The town judge has `n - 1` trust score (everyone trusts them, they trust nobody).

**Code:**
```python
# findJudge: implement solution
def findJudge(n, trust):
    score = [0] * (n + 1)
    for a, b in trust:
        score[a] -= 1
        score[b] += 1
    for i in range(1, n + 1):
        if score[i] == n - 1:
            return i
    return -1
```

**Complexity:** O(e) time, O(n) space where `e = len(trust)`.

**Tip:** Exactly one person must have score `n - 1`. If multiple or none, return `-1`.

**Visual Walkthrough:**
```
n=3, trust=[[1,3],[2,3]]

Trust relationships:
1 → 3 (1 trusts 3)
2 → 3 (2 trusts 3)

Indegree (trusted by): [0,0,0,2]
Outdegree (trusts):    [0,1,1,0]

Judge = person with indegree = n-1 = 2 AND outdegree = 0
Person 3: indegree=2, outdegree=0 → Judge = 3

Key: Judge trusts nobody, everyone (except judge) trusts judge
```

**Brute Force vs Optimal:**
| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| Degree counting | O(n + trust) | O(n) | Track in/out degrees |
| **Single array** | **O(n + trust)** | **O(n)** | **Balance array: +1 for trusted, -1 for trusts** |

**Common Mistakes:**
- People are 1-indexed (not 0-indexed) → array of size n+1
- Forgetting judge must have outdegree 0 (trusts nobody)
- Returning first person with indegree=n-1 without checking outdegree=0

**Edge Cases:**
- n=1, trust=[] → person 1 is judge (no one else)
- No trust relationships → impossible if n>1 (no one has indegree=n-1)
- Multiple candidates with indegree=n-1 → only first check? Actually only judge has indegree=n-1

**Pattern Recognition:**
**Graph Degree Pattern**: Track trust flow as indegree/outdegree. Used in: Find Celebrity, Star Graph Center.


---

## MEDIUM (Problems 11–25)

---





### 11. Course Schedule

**Problem:** There are `numCourses` courses with prerequisites. `prerequisites[i] = [a, b]` means you must take `b` before `a`. Return `True` if you can finish all courses.

**Approach:** Build a directed graph. Cycle detection via DFS (3-color marking) or in-degree based BFS (Kahn's algorithm).

**Code:**
```python
# canFinish: implement solution
def canFinish(numCourses, prerequisites):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    indegree = [0] * numCourses
    for a, b in prerequisites:
        graph[b].append(a)
        indegree[a] += 1

    queue = deque([i for i in range(numCourses) if indegree[i] == 0])
    taken = 0
    while queue:
        node = queue.popleft()
        taken += 1
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)
    return taken == numCourses
```

**Complexity:** O(V + E) time, O(V + E) space.

**Tip:** If `taken != numCourses`, there's a cycle. Kahn's algorithm is clean and easy to extend for Course Schedule II.

**Visual Walkthrough:**
```
numCourses=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]]

Graph: 0 → 1 → 3
       0 → 2 → 3

Indegrees: [0, 1, 1, 2]

Kahn's algorithm:
Queue = [0] (indegree 0)
Process 0: taken=1, reduce indegree of 1,2
Queue = [1,2]
Process 1: taken=2, reduce indegree of 3 (now indegree 1)
Queue = [2]
Process 2: taken=3, reduce indegree of 3 (now indegree 0)
Queue = [3]
Process 3: taken=4
taken=4 == numCourses=4 → True (no cycle)

If there were a cycle: taken < numCourses
```

**Brute Force vs Optimal:**
| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| DFS (3-color) | O(V+E) | O(V) | White/gray/black cycle detection |
| **Kahn's (BFS)** | **O(V+E)** | **O(V+E)** | **In-degree based, returns order** |

**Common Mistakes:**
- Forgetting to decrement indegree for all neighbors
- Not checking if taken == numCourses at end
- Not building graph with both directions (prereq → course)

**Edge Cases:**
- No prerequisites → True
- Cycle exists → False
- Single course → True

**Pattern Recognition:**
**Cycle Detection (DAG)**: Kahn's algorithm or DFS 3-color. Used in: Course Schedule II, Alien Dictionary.


---





### 12. Course Schedule II

**Problem:** Same as Course Schedule, but return the ordering of courses to finish all, or `[]` if impossible.

**Approach:** Kahn's topological sort. Enqueue zero in-degree nodes, process level by level.

**Code:**
```python
# findOrder: implement solution
def findOrder(numCourses, prerequisites):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    indegree = [0] * numCourses
    for a, b in prerequisites:
        graph[b].append(a)
        indegree[a] += 1

    queue = deque([i for i in range(numCourses) if indegree[i] == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)
    return order if len(order) == numCourses else []
```

**Complexity:** O(V + E) time, O(V + E) space.

**Tip:** Kahn's algorithm gives a valid topological order. DFS-based approach is also possible but harder to implement correctly.

**Visual Walkthrough (numCourses=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]]):**
```
Graph:  0 → 1 → 3
        0 → 2 → 3

Indegree: [0, 1, 1, 2]
          ↑  
          0 has indegree 0 → start here

Step 1: Process 0 → order=[0], reduce indegree of 1,2
Step 2: Process 1 → order=[0,1], reduce indegree of 3
Step 3: Process 2 → order=[0,1,2], reduce indegree of 3
Step 4: Process 3 → order=[0,1,2,3]

Return [0,1,2,3] or [0,2,1,3] (both valid)
```

**Common Mistakes:**
- Not detecting cycles (if `len(order) != numCourses` → cycle exists)
- Using DFS approach incorrectly (needs post-order + reverse)
- Not handling disconnected components (all nodes must be processed)

**Edge Cases:**
- No prerequisites → any order is valid
- Cycle exists → return empty array
- Single course → return [0]

**Pattern Recognition:**
**Topological Sort Pattern**: When you have dependencies between items, use Kahn's algorithm (BFS + indegree) for linear ordering. Used in: Course Schedule, Course Schedule II, Alien Dictionary, Parallel Courses.

---





### 13. Pacific Atlantic Water Flow

**Problem:** Given an `m x n` matrix of heights, water can flow from a cell to an adjacent cell with equal or lower height. Find cells where water can reach both the Pacific and Atlantic oceans.

**Approach:** Reverse thinking — start BFS from Pacific border cells and Atlantic border cells separately. Cells reachable from both are the answer.

**Code:**
```python
# pacificAtlantic: implement solution
def pacificAtlantic(heights):
    rows, cols = len(heights), len(heights[0])
    pacific, atlantic = set(), set()

    def dfs(r, c, visited, prev):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if heights[r][c] < prev:
            return
        visited.add((r, c))
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            dfs(r + dr, c + dc, visited, heights[r][c])

    for r in range(rows):
        dfs(r, 0, pacific, heights[r][0])
        dfs(r, cols - 1, atlantic, heights[r][cols - 1])
    for c in range(cols):
        dfs(0, c, pacific, heights[0][c])
        dfs(rows - 1, c, atlantic, heights[rows - 1][c])

    return list(pacific & atlantic)
```

**Complexity:** O(m × n) time, O(m × n) space.

**Tip:** BFS/DFS from borders is much simpler than checking from each cell individually.

**Visual Walkthrough:**
```
heights = [[1,2,2,3,5],
            [3,2,3,4,4],
            [2,4,5,3,1],
            [6,7,1,4,5],
            [5,1,1,2,4]]

Pacific (←↑) and Atlantic (→↓):
Start from Pacific borders (top, left) → mark all reachable cells
Start from Atlantic borders (bottom, right) → mark all reachable cells
Intersection of both = answer

Reverse thinking: instead of flowing from each cell to ocean,
start from ocean and flow INLAND (higher or equal height allowed)
This avoids checking each cell individually.
```

**Brute Force vs Optimal:**
| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| Check each cell | O(m²n²) | O(mn) | Flow from each cell to both oceans |
| **Borders BFS/DFS** | **O(mn)** | **O(mn)** | **Reverse flow from oceans** |

**Common Mistakes:**
- Forward thinking (checking each cell instead of reverse from borders)
- Not allowing equal height (water flows from higher to equal)
- Off-by-one in detecting border cells (row 0, m-1; col 0, n-1)

**Edge Cases:**
- Single cell → belongs to both oceans
- Monotonic increasing → diagonal from start to end
- Wall border can't be crossed → no cell reaches both

**Pattern Recognition:**
**Reverse Border BFS**: Start from ocean borders, flow inland. Used in: Surrounded Regions, Number of Enclaves.


---





### 14. Word Ladder

**Problem:** Given `beginWord`, `endWord`, and a word list, find the shortest transformation sequence from `beginWord` to `endWord`, changing one letter at a time. Each intermediate word must be in the word list.

**Approach:** BFS from `beginWord`. For each word, try changing each letter to `a-z` and check if it's in the word set.

**Code:**
```python
# ladderLength: implement solution
def ladderLength(beginWord, endWord, wordList):
    wordSet = set(wordList)
    if endWord not in wordSet:
        return 0
    from collections import deque
    queue = deque([(beginWord, 1)])
    visited = set([beginWord])
    while queue:
        word, length = queue.popleft()
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                newWord = word[:i] + c + word[i+1:]
                if newWord == endWord:
                    return length + 1
                if newWord in wordSet and newWord not in visited:
                    visited.add(newWord)
                    queue.append((newWord, length + 1))
    return 0
```

**Complexity:** O(M² × N) time where M = word length, N = word list size. O(M × N) space.

**Tip:** Bidirectional BFS can speed this up significantly for large word lists.

**Visual Walkthrough:**
```
beginWord="hit", endWord="cog", wordList=["hot","dot","dog","lot","log","cog"]

BFS shortest path:
hit → hot → dot → dog → cog
           → lot → log → cog

Level 1: hit
Level 2: hot
Level 3: dot, lot
Level 4: dog, log
Level 5: cog

Shortest path length = 5 (hit→hot→dot→dog→cog)

Each transformation changes exactly 1 letter.
Use a set for O(1) word lookups.
```

**Brute Force vs Optimal:**
| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| BFS (one-way) | O(M²×N) | O(M×N) | Standard BFS |
| **Bidirectional BFS** | **O(M²×N/2)** | **O(M×N)** | **BFS from both ends, much faster** |

**Common Mistakes:**
- Not using a set for word list (O(N) lookup)
- Forgetting to check if endWord is in wordList first
- Generating neighbors by iterating wordList (instead of letter-by-letter)

**Edge Cases:**
- endWord not in wordList → 0
- beginWord == endWord → 1
- No possible transformation → 0

**Pattern Recognition:**
**Shortest Path (Unweighted Graph)**: BFS for shortest transformation sequence. Used in: Word Ladder II, Genetic Mutation.


---





### 15. Walls and Gates

**Problem:** Given an `m x n` grid with `0` (gate), `-1` (wall), and `INF` (empty room), fill each empty room with the distance to its nearest gate.

**Approach:** Multi-source BFS from all gates simultaneously. Each step increments distance.

**Code:**
```python
# wallsAndGates: implement solution
from collections import deque

def wallsAndGates(rooms):
    if not rooms:
        return
    rows, cols = len(rooms), len(rooms[0])
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if rooms[r][c] == 0:
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == 2147483647:
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))
```

**Complexity:** O(m × n) time, O(m × n) space.

**Tip:** Multi-source BFS guarantees shortest distance because all gates expand at the same rate.

**Visual Walkthrough:**
```
rooms = [[INF, -1,  0, INF],
         [INF, INF, INF, -1],
         [INF, -1, INF, -1],
         [0,  -1, INF, INF]]

Multi-source BFS from all gates (0):
Initialize queue with all gates at distance 0.

BFS expands evenly:
  Queue: (0,2)=0, (3,0)=0
  Process (0,2): set (0,1)=1, (1,2)=1
  Process (3,0): set (2,0)=1
  Process (0,1): set (0,0)=2, (1,1)=2
  Process (1,2): set (1,3)=2, (2,2)=2
  ...

Final distances:
  2  -1   0   1
  1   2   1  -1
  1  -1   2  -1
  0  -1   1   2
```

**Brute Force vs Optimal:**
| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| DFS from each gate | O(m²n²) | O(mn) | Visit each cell from each gate |
| **Multi-source BFS** | **O(mn)** | **O(mn)** | **Start BFS from all gates simultaneously** |

**Common Mistakes:**
- Running BFS/DFS from each gate separately (O(mn) times)
- Forgetting that INF is a specific large number (2147483647)
- Not checking bounds before accessing array

**Edge Cases:**
- No gates → no change
- No empty rooms → no change
- Walls block propagation completely

**Pattern Recognition:**
**Multi-source BFS**: All sources start at distance 0, BFS expands evenly. Used in: Rotting Oranges, 01 Matrix, As Far from Land as Possible.


---





### 16. Redundant Connection

**Problem:** A tree with `n` nodes has one extra edge added, creating a cycle. Find the edge that, if removed, restores the tree property. If multiple, return the one that appears last.

**Approach:** Union-Find. Process edges one by one. If both endpoints are already in the same component, this edge is redundant.

**Code:**
```python
# findRedundantConnection: implement solution
def findRedundantConnection(edges):
    parent = list(range(len(edges) + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        parent[px] = py
        return True

    for u, v in edges:
        if not union(u, v):
            return [u, v]
```

**Complexity:** O(n × α(n)) ≈ O(n) time, O(n) space.

**Tip:** Path compression + union by rank makes Union-Find nearly O(1) per operation.

**Visual Walkthrough:**
```
edges = [[1,2],[1,3],[2,3]] n=3

Union-Find process:
Add (1,2): 1-2 connected
Add (1,3): 1-2-3 connected
Add (2,3): 2 and 3 already connected → this edge is redundant!

Answer: [2,3]
```

**Common Mistakes:**
- Confusing find() and union() implementation
- Not compressing paths (O(n) without optimization)
- Forgetting Union-Find on undirected graphs detects the redundant edge

**Edge Cases:**
- Empty graph → []
- Single edge → not applicable (problem says at least one extra edge)
- Tree with n nodes (no extra) → []

**Pattern Recognition:**
**Union-Find Cycle Detection**: Add edges, if find(u)==find(v) then edge creates cycle. Used in: Redundant Connection II, Number of Connected Components.


---





### 17. Accounts Merge

**Problem:** Given a list of accounts where each account has a name and a list of emails, merge accounts that share common emails. Return the merged accounts.

**Approach:** Union-Find on emails. Emails in the same account are united. Also unite shared emails across accounts. Then group emails by root and sort.

**Code:**
```python
# accountsMerge: implement solution
def accountsMerge(accounts):
    email_to_name = {}
    email_to_id = {}
    parent = {}
    idx = 0

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py

    for acc in accounts:
        name = acc[0]
        for email in acc[1:]:
            email_to_name[email] = name
            if email not in email_to_id:
                email_to_id[email] = idx
                parent[idx] = idx
                idx += 1
            union(email_to_id[acc[1]], email_to_id[email])

    from collections import defaultdict
    groups = defaultdict(set)
    for email, eid in email_to_id.items():
        groups[find(eid)].add(email)

    return [[email_to_name[next(iter(v))]] + sorted(v) for v in groups.values()]
```

**Complexity:** O(N × K × α(N)) time where N = accounts, K = avg emails. O(N × K) space.

**Tip:** The key insight is that any two accounts sharing even one email should be merged entirely.

**Visual Walkthrough:**
```
accounts = [["John","john1@m.com","john2@m.com"],
            ["John","john3@m.com","john1@m.com"],
            ["Mary","mary@m.com"]]

Union email addresses:
  john1@ – john2@ (from account 0)
  john3@ – john1@ (from account 1)
  → All john's emails connected via union-find
  Account 2 (Mary) is separate.

Answer: [["John","john1@...","john2@...","john3@..."],
         ["Mary","mary@..."]]
```

**Common Mistakes:**
- People can have the same name but be different (merge by email, not name)
- Not sorting emails in output
- Forgetting to map emails back to owner's name

**Edge Cases:**
- Single account → return as-is
- Two accounts with same name but no shared email → separate
- Duplicate email across accounts → merge occurs

**Pattern Recognition:**
**Union-Find on Emails**: Union emails within each account, find connected components. Used in: Accounts Merge, Number of Connected Components in Graph.


---





### 18. Graph Valid Tree

**Problem:** Given `n` nodes and `edges`, determine if the edges form a valid tree.

**Approach:** A valid tree has exactly `n - 1` edges AND is connected. Check both conditions.

**Code:**
```python
# validTree: implement solution
def validTree(n, edges):
    if len(edges) != n - 1:
        return False
    from collections import defaultdict, deque
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    visited = set([0])
    queue = deque([0])
    while queue:
        node = queue.popleft()
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                queue.append(nei)
    return len(visited) == n
```

**Complexity:** O(n + e) time, O(n + e) space.

**Tip:** `n - 1` edges + connected = valid tree. Two simple checks, no complex DFS needed.

**Visual Walkthrough:**
```
n=5, edges=[[0,1],[0,2],[0,3],[1,4]]

A valid tree must have exactly n-1 edges and be connected with no cycles.

Edges=4, n=5 → edges == n-1 ✓
Union-Find:
(0,1): connect, (0,2): connect, (0,3): connect, (1,4): connect
All nodes in one component, no cycle.

With extra edge (1,3): find(1)==find(3) → cycle! Not a tree.
```

**Common Mistakes:**
- Only checking edge count (n-1) without connectivity — may have multiple components
- Not handling V=0 or V=1 edge cases
- Forgetting graph is undirected

**Edge Cases:**
- n=1, edges=[] → True (single node is a tree)
- n=2, edges=[[0,1]] → True
- n=2, edges=[] → False (disconnected)
- n=2, edges=[[0,1],[1,0]] → False (duplicate edges form cycle)

**Pattern Recognition:**
**Tree Validation**: Connected + no cycles + n-1 edges. Used in: Redundant Connection, Number of Connected Components.


---





### 19. Network Delay Time

**Problem:** Given `n` nodes and weighted directed edges, and a starting node `k`, find the time it takes for a signal to reach all nodes. Return `-1` if not all reachable.

**Approach:** Dijkstra's algorithm from node `k`. The answer is the maximum distance among all nodes.

**Code:**
```python
# networkDelayTime: implement solution
import heapq
from collections import defaultdict

def networkDelayTime(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    dist = {}
    heap = [(0, k)]
    while heap:
        d, node = heapq.heappop(heap)
        if node in dist:
            continue
        dist[node] = d
        for nei, w in graph[node]:
            if nei not in dist:
                heapq.heappush(heap, (d + w, nei))
    return max(dist.values()) if len(dist) == n else -1
```

**Complexity:** O(E × log E) time, O(V + E) space.

**Tip:** Dijkstra handles positive weights. For negative weights, use Bellman-Ford instead.

**Visual Walkthrough:**
```
times = [[2,1,1],[2,3,1],[3,4,1]], n=4, k=2

Graph: 2 → 1 (1ms), 2 → 3 (1ms), 3 → 4 (1ms)

Dijkstra from node 2:
dist[2]=0
Process 2: update dist[1]=1, dist[3]=1
Process 1: no outgoing edges
Process 3: update dist[4]=2
Process 4: no outgoing edges

Distances: [inf, 1, 0, 1, 2]
Max finite distance = 2 → Answer: 2ms
```

**Common Mistakes:**
- Forgetting to initialize all distances to infinity
- Not checking if any node is unreachable (return -1)
- Using BFS instead of Dijkstra (edges have weights!)

**Edge Cases:**
- k unreachable from some nodes → -1
- n=1 → 0 (only one node)
- No edges → -1 (unless n=1)
- Disconnected graph → -1

**Pattern Recognition:**
**Single-Source Shortest Path (Dijkstra)**: PQ-based for non-negative weights. Used in: Cheapest Flights Within K Stops, Path with Maximum Probability.


---





### 20. Cheapest Flights Within K Stops

**Problem:** Given `n` cities, flights with costs, source `src`, destination `dst`, and max `k` stops, find the cheapest price. Return `-1` if not possible.

**Approach:** Modified Dijkstra or BFS. Track `(cost, city, stops)`. Only push to heap if stops ≤ k.

**Code:**
```python
# findCheapestPrice: implement solution
import heapq
from collections import defaultdict

def findCheapestPrice(n, flights, src, dst, k):
    graph = defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))
    heap = [(0, src, k + 1)]
    visited = {}
    while heap:
        cost, node, stops = heapq.heappop(heap)
        if node == dst:
            return cost
        if node in visited and visited[node] >= stops:
            continue
        visited[node] = stops
        for nei, w in graph[node]:
            if stops > 0:
                heapq.heappush(heap, (cost + w, nei, stops - 1))
    return -1
```

**Complexity:** O(E × log E) time, O(V + E) space.

**Tip:** Unlike standard Dijkstra, we may revisit a node with a different number of remaining stops. Track `visited[node] = max stops remaining`.

**Visual Walkthrough:**
```
n=3, flights=[[0,1,100],[1,2,100],[0,2,500]], src=0, dst=2, k=1

Bellman-Ford (k+1 iterations):
Initialize dist = [0, inf, inf]
Iteration 1 (0 stops):
  [0,1]=100 → dist=[0,100,inf]
  [1,2]=100 → need dist[1]={100}+100=200 → dist=[0,100,200]
  [0,2]=500 → dist[2]=min(inf,500)=500
  After: dist=[0,100,200]
Iteration 2 (1 stop):
  [0,1]=100 → min(100,0+100)=100
  [1,2]=100 → min(200,100+100)=200
  [0,2]=500 → min(500,0+500)=500
  After: dist=[0,100,200]

Answer: 200 (0→1→2, uses 1 stop)
```

**Common Mistakes:**
- Confusing stops with edges: K stops = K+1 edges
- Not using a temp array (original dist gets updated mid-iteration causing >K edges used)
- Forgetting to check if dst is reachable within K stops

**Edge Cases:**
- src == dst → 0 (no flight needed)
- K=0 → only direct flights
- No flights within K stops → -1

**Pattern Recognition:**
**K-Limited Shortest Path**: Bellman-Ford with exactly K+1 iterations. Used in: Network Delay Time, Minimum Cost to Reach Destination with K Stops.


---





### 21. Alien Dictionary

**Problem:** Given a sorted list of words in an alien language, derive the character order (lexicographic ordering).

**Approach:** Compare adjacent words character by character. The first differing pair gives a directed edge `a → b` (a comes before b). Topological sort the resulting graph.

**Code:**
```python
# alienOrder: implement solution
from collections import defaultdict, deque

def alienOrder(words):
    adj = defaultdict(set)
    in_degree = {c: 0 for word in words for c in word}
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break

    queue = deque([c for c in in_degree if in_degree[c] == 0])
    result = []
    while queue:
        c = queue.popleft()
        result.append(c)
        for nei in adj[c]:
            in_degree[nei] -= 1
            if in_degree[nei] == 0:
                queue.append(nei)
    return "".join(result) if len(result) == len(in_degree) else ""
```

**Complexity:** O(C) time where C = total characters. O(1) space (at most 26 letters).

**Tip:** Return `""` if there's a cycle (topological sort result length < unique characters).

**Visual Walkthrough:**
```
words = ["wrt","wrf","er","ett","rftt"]

Compare adjacent words:
wrt vs wrf: 't' < 'f' → t→f
wrf vs er: 'w' < 'e' → w→e  
er vs ett: 'r' < 't' → r→t
ett vs rftt: 'e' < 'r' → e→r

Graph: w→e→r→t→f
Topological order: "wertf"
```

**Common Mistakes:**
- Not handling invalid order when word2 is prefix of word1 (e.g., ["abc","ab"])
- Forgetting to include all letters, even those without edges
- Building incorrect graph direction

**Edge Cases:**
- Empty list → ""
- Single word → its unique letters in any order
- Cycle in graph → "" (impossible)
- Words with same prefix → compare next differing letter

**Pattern Recognition:**
**Topological Sort on Letters**: Compare adjacent words, build directed edges. Used in: Course Schedule, Alien Dictionary II.


---





### 22. Parallel Courses

**Problem:** Given `n` courses and prerequisites, find the minimum number of semesters to complete all courses (each semester you can take any number of courses whose prerequisites are met). Return `-1` if impossible.

**Approach:** Topological sort. The number of BFS levels = minimum semesters.

**Code:**
```python
# minimumSemesters: implement solution
from collections import defaultdict, deque

def minimumSemesters(n, relations):
    graph = defaultdict(list)
    indegree = [0] * (n + 1)
    for u, v in relations:
        graph[u].append(v)
        indegree[v] += 1

    queue = deque([i for i in range(1, n + 1) if indegree[i] == 0])
    semesters = 0
    taken = 0
    while queue:
        semesters += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            taken += 1
            for nei in graph[node]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    queue.append(nei)
    return semesters if taken == n else -1
```

**Complexity:** O(V + E) time, O(V + E) space.

**Tip:** BFS level count = minimum semesters. Each level represents courses that can be taken simultaneously.

**Visual Walkthrough:**
```
n=3, relations=[[1,3],[2,3]]

Graph: 1→3, 2→3

Kahn's algorithm with semesters:
Indegrees: [0,0,0] (1-indexed)
Init: 1→3: indeg[3]=1, 2→3: indeg[3]=2

Semester 1: Queue=[1,2] (both indegree=0)
  Process 1: indeg[3]-- → indeg[3]=1
  Process 2: indeg[3]-- → indeg[3]=0
Semester 2: Queue=[3]
  Process 3

Answer: 2 semesters
```

**Common Mistakes:**
- Not processing all nodes in a level at once (should count levels, not steps)
- Forgetting cycle detection (return -1 if cycle)
- Not handling disconnected nodes (they can be taken in semester 1)

**Edge Cases:**
- No prerequisites → 1 semester (all courses taken together)
- Cycle → -1
- Single course → 1 semester

**Pattern Recognition:**
**Topological Sort with Levels**: Kahn's algorithm, process level by level. Used in: Course Schedule IV, Minimum Time to Complete Tasks.


---





### 23. Longest Path in a DAG

**Problem:** Given a Directed Acyclic Graph with `n` nodes and weighted edges, find the longest path from any node.

**Approach:** Topological sort, then process nodes in order, relaxing longest distances.

**Code:**
```python
# longestPath: implement solution
from collections import defaultdict, deque

def longestPath(n, edges):
    graph = defaultdict(list)
    indegree = [0] * n
    for u, v, w in edges:
        graph[u].append((v, w))
        indegree[v] += 1

    queue = deque([i for i in range(n) if indegree[i] == 0)
    dist = [0] * n
    while queue:
        node = queue.popleft()
        for nei, w in graph[node]:
            dist[nei] = max(dist[nei], dist[node] + w)
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)
    return max(dist)
```

**Complexity:** O(V + E) time, O(V) space.

**Tip:** Topological sort ensures we process each node after all its predecessors, making DP straightforward.

**Visual Walkthrough:**
```
n=5, edges=[[0,1],[0,2],[1,3],[2,3],[3,4]]

Graph: 0→1→3→4, 0→2→3→4

Topological order: [0,1,2,3,4]
DP from start:
dist[0]=0
dist[1]=1, dist[2]=1
dist[3]=max(dist[1]+1, dist[2]+1)=2
dist[4]=dist[3]+1=3

Answer: 3 (path 0→1→3→4 or 0→2→3→4)

For longest path: negate weights and use shortest path algorithm, OR
use topological sort + relaxation.
```

**Common Mistakes:**
- Not using topological order (trying BFS/DFS on graph with cycles → infinite loop)
- Forgetting the graph must be a DAG (no cycles allowed)
- Not handling disconnected nodes (distance = 0)

**Edge Cases:**
- Single node → 0
- No edges → 0
- Disconnected DAG → 0 for isolated nodes

**Pattern Recognition:**
**DP on DAG**: Process nodes in topological order, relax outgoing edges. Used in: Critical Path, PERT Chart Analysis.


---





### 24. Swim in Rising Water

**Problem:** Given an `n x n` grid where `grid[i][j]` represents elevation, water rises over time. You can swim to adjacent cells when the max elevation between them ≤ current time. Find the minimum time to swim from `(0,0)` to `(n-1,n-1)`.

**Approach:** Binary search on time + BFS/DFS, or Dijkstra (min-heap on time).

**Code:**
```python
# swimInWater: implement solution
import heapq

def swimInWater(grid):
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]
    visited = set([(0, 0)])
    while heap:
        t, r, c = heapq.heappop(heap)
        if r == n - 1 and c == n - 1:
            return t
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
                visited.add((nr, nc))
                heapq.heappush(heap, (max(t, grid[nr][nc]), nr, nc))
    return -1
```

**Complexity:** O(n² × log n) time, O(n²) space.

**Tip:** Dijkstra naturally picks the path minimizing the maximum elevation encountered.

**Visual Walkthrough:**
```
grid = [[0,2],[1,3]]

At time t, water level = t. You can swim through cells with grid[r][c] ≤ t.

Mini-max path: minimize the maximum elevation along the path.

Option 1: Dijkstra (priority queue): start at (0,0), pop min max-height
  (0,0)=0 → max=0
  (0,1)=2 → max=2
  (1,0)=1 → max=1
  (1,1)=3 → max=3
  Instead of typical distance, track min(max height so far)

Option 2: Binary search on answer t.
  Can we reach (n-1,n-1) with max cell ≤ t?
  t=0: No (need 2,1,3)
  t=1: No (still need 2,3)
  t=2: Yes (cells with ≤2: (0,0),(0,1),(1,0)) → but (1,1)=3 > 2... 
  t=3: All cells reachable → Yes
  Answer: 3
```

**Common Mistakes:**
- Confusing with shortest path (sum) instead of min-max path
- Not visiting cells where grid[r][c] > current max
- Forgetting 4-directional movement

**Edge Cases:**
- n=1 → return grid[0][0]
- All values same → return that value
- Path always exists (can wait long enough)

**Pattern Recognition:**
**Mini-max Path (Dijkstra variant)**: PQ on max elevation so far. Used in: Path With Minimum Effort, Minimum Obstacle Removal.


---





### 25. Path with Maximum Probability

**Problem:** Given `n` cities with weighted edges (probabilities of success), find the path from `start` to `end` with maximum success probability.

**Approach:** Modified Dijkstra using max-heap (multiply probabilities instead of adding distances).

**Code:**
```python
# maxProbability: implement solution
import heapq
from collections import defaultdict

def maxProbability(n, edges, succProb, start, end):
    graph = defaultdict(list)
    for i, (u, v) in enumerate(edges):
        graph[u].append((v, succProb[i]))
        graph[v].append((u, succProb[i]))

    prob = [0.0] * n
    prob[start] = 1.0
    heap = [(-1.0, start)]
    while heap:
        p, node = heapq.heappop(heap)
        p = -p
        if node == end:
            return p
        for nei, w in graph[node]:
            if prob[nei] < p * w:
                prob[nei] = p * w
                heapq.heappush(heap, (-prob[nei], nei))
    return 0.0
```

**Complexity:** O(E × log E) time, O(V + E) space.

**Tip:** Python's `heapq` is a min-heap, so negate probabilities to simulate a max-heap.

**Visual Walkthrough:**
```
n=3, edges=[[0,1],[1,2],[0,2]], succProb=[0.5,0.5,0.3], start=0, end=2

Graph:
0 → 1 (prob 0.5), 0 → 2 (prob 0.3)
1 → 2 (prob 0.5)

Path 0→2: prob = 0.3
Path 0→1→2: prob = 0.5 × 0.5 = 0.25

Answer: 0.3 (direct edge is better than two hops with lower combined prob)

Use Dijkstra with max-heap (negate probabilities for min-heap).
prob[0]=1.0
Pop 0: update prob[1]=1.0×0.5=0.5, prob[2]=1.0×0.3=0.3
Pop 1 (0.5): update prob[2]=max(0.3, 0.5×0.5)=max(0.3,0.25)=0.3
```

**Common Mistakes:**
- Using sum instead of product for path probability
- Forgetting probability multiplies (not adds) along path
- Not initializing start node with prob=1.0

**Edge Cases:**
- start == end → 1.0
- No path → 0.0
- Disconnected → 0.0

**Pattern Recognition:**
**Max Product Path (Dijkstra)**: Use probability product with max-heap. Used in: Network Delay Time, Minimum Cost Path.


---

## HARD (Problems 26–35)

---





### 26. Critical Connections (Bridges)

**Problem:** Given `n` servers and connections, find all critical connections (bridges) whose removal increases the number of disconnected components.

**Approach:** Tarjan's algorithm — DFS with discovery time and low-link values. An edge `(u, v)` is a bridge if `low[v] > disc[u]`.

**Code:**
```python
# criticalConnections: implement solution
def criticalConnections(n, connections):
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)

    disc = [-1] * n
    low = [-1] * n
    timer = [0]
    bridges = []

    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        for v in graph[u]:
            if disc[v] == -1:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append([u, v])
            elif v != parent:
                low[u] = min(low[u], disc[v])

    dfs(0, -1)
    return bridges
```

**Complexity:** O(V + E) time, O(V + E) space.

**Tip:** Use `disc[v]` (not `low[v]`) when checking back-edges. This is a common mistake.

**Visual Walkthrough:**
```
graph with 4 edges, find all bridges:

0 ─ 1
│   │
3 ─ 2

Edges: (0,1), (0,3), (1,2), (2,3)

Tarjan's algorithm:
discovery times: [0:0, 1:1, 2:2, 3:3]
low values:     [0:0, 1:0, 2:0, 3:0]

Back edge (3,0): low[3]=min(3,0)=0
Update low[2]=min(2,0)=0, low[1]=min(1,0)=0

No edge has low[neighbor] > discovery[current] → no bridges!

The edge (1,2): low[2]=0 < disc[1]=1 → not a bridge (it's in a cycle)
```

**Common Mistakes:**
- Not updating low values after DFS returns from a neighbor
- Confusing discovery time with low value
- Forgetting that root node needs special handling for bridge detection

**Edge Cases:**
- Single node → no bridges
- Tree → ALL edges are bridges
- Fully connected cycle → no bridges

**Pattern Recognition:**
**Tarjan's Bridges**: DFS with discovery/low values. Edge (u,v) is bridge if low[v] > disc[u]. Used in: Critical Connections, Articulation Points.
---





### 27. Word Ladder II

**Problem:** Find ALL shortest transformation sequences from `beginWord` to `endWord`.

**Approach:** BFS to build a DAG of shortest paths, then DFS to enumerate all paths.

**Code:**
```python
# findLadders: implement solution
from collections import defaultdict, deque

def findLadders(beginWord, endWord, wordList):
    wordSet = set(wordList)
    if endWord not in wordSet:
        return []
    graph = defaultdict(list)
    queue = deque([beginWord])
    visited = set([beginWord])
    found = False
    while queue and not found:
        level_visited = set()
        for _ in range(len(queue)):
            word = queue.popleft()
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    nw = word[:i] + c + word[i+1:]
                    if nw == endWord:
                        graph[word].append(nw)
                        found = True
                    elif nw in wordSet:
                        graph[word].append(nw)
                        if nw not in visited:
                            level_visited.add(nw)
                            queue.append(nw)
        visited |= level_visited

    result = []
    def dfs(word, path):
        if word == endWord:
            result.append(list(path))
            return
        for nw in graph[word]:
            path.append(nw)
            dfs(nw, path)
            path.pop()

    dfs(beginWord, [beginWord])
    return result
```

**Complexity:** O(N × M²) time where N = word count, M = word length. Space is similar.

**Tip:** Level-by-level BFS is critical. Mark words as visited only after processing an entire level to allow multiple paths through the same word.

**Visual Walkthrough:**
```
beginWord="hit", endWord="cog", wordList=["hot","dot","dog","lot","log","cog"]

BFS from beginWord to find shortest distance + all paths:

Level 1: hit
Level 2: hot
Level 3: dot, lot
Level 4: dog, log
Level 5: cog

Build adjacency with parent tracking:
hit → hot
hot → dot, lot
dot → dog
dog → cog
lot → log
log → cog

Backtrack from cog:
cog ← dog ← dot ← hot ← hit
cog ← log ← lot ← hot ← hit

All shortest paths:
1. hit→hot→dot→dog→cog
2. hit→hot→lot→log→cog
```

**Common Mistakes:**
- Not removing used words from word set at the right level (not per path)
- Generating paths by iterating wordList (letter-by-letter is faster)
- Forgetting to track visited per level (not globally for path reconstruction)

**Edge Cases:**
- endWord not in wordList → []
- beginWord == endWord → [[beginWord]]
- No transformation possible → []

**Pattern Recognition:**
**BFS + Backtracking**: Find shortest paths, then reconstruct all. Used in: Word Ladder I, Minimum Height Trees (reverse).
---





### 28. Minimum Cost to Make at Least One Valid Path in Grid

**Problem:** Given an `m x n` grid where each cell has a sign (1=right, 2=left, 3=down, 4=up), you can change any sign at cost 1. Find minimum cost to make a valid path from `(0,0)` to `(m-1,n-1)`.

**Approach:** 0-1 BFS (deque-based BFS). Moving with the arrow costs 0, changing the arrow costs 1.

**Code:**
```python
# minCost: implement solution
from collections import deque

def minCost(grid):
    m, n = len(grid), len(grid[0])
    dist = [[float('inf')] * n for _ in range(m)]
    dist[0][0] = 0
    dq = deque([(0, 0)])
    dirs = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}
    while dq:
        r, c = dq.popleft()
        for d, (dr, dc) in dirs.items():
            nr, nc = r + dr, c + dc
            cost = 0 if grid[r][c] == d else 1
            if 0 <= nr < m and 0 <= nc < n and dist[r][c] + cost < dist[nr][nc]:
                dist[nr][nc] = dist[r][c] + cost
                if cost == 0:
                    dq.appendleft((nr, nc))
                else:
                    dq.append((nr, nc))
    return dist[m-1][n-1]
```

**Complexity:** O(m × n) time, O(m × n) space.

**Tip:** 0-1 BFS works when edge weights are only 0 or 1. It's faster than Dijkstra for this case.

**Visual Walkthrough:**
```
grid = [[1,1,1,1],[2,2,2,2],[1,1,1,1],[2,2,2,2]]

0-1 BFS (deque): moving with the arrow costs 0, changing costs 1.

Start at (0,0) with arrow → (0,1) cost=0
Reach (0,0) with cost 0
  Right direction → neighbor (0,1) cost 0 (push front)
    At (0,1) right → (0,2) cost 0
      ... all the way to (0,3)
    Change dir at (0,1) → push back with cost 1

Min cost to make at least one valid path from (0,0) to (3,3) = 0
(if there's already a path following arrows)
```

**Common Mistakes:**
- Not using 0-1 BFS (deque) for O(1) insertion
- Forgetting to check all 4 directions for modification costs
- Not tracking visited with distances (revisit with lower cost)

**Edge Cases:**
- Starting cell already has a valid path to target → 0
- Grid 1×1 → 0
- No path possible without modification → worst case is min distance

**Pattern Recognition:**
**0-1 BFS (Deque)**: Cost 0 moves → push front, cost 1 → push back. Used in: Minimum Cost to Make Path Valid, Shortest Path with Obstacle Removal.
---





### 29. Shortest Path in a Binary Matrix

**Problem:** Given an `n x n` binary grid where `1` means open and `0` means blocked, find the shortest path from `(0,0)` to `(n-1,n-1)` moving in 8 directions. Return the path length or `-1`.

**Approach:** BFS on the grid. Each step costs 1. BFS guarantees shortest path in unweighted graphs.

**Code:**
```python
# shortestPathBinaryMatrix: implement solution
from collections import deque

def shortestPathBinaryMatrix(grid):
    n = len(grid)
    if grid[0][0] or grid[n-1][n-1]:
        return -1
    queue = deque([(0, 0, 1)])
    visited = set([(0, 0)])
    while queue:
        r, c, dist = queue.popleft()
        if r == n - 1 and c == n - 1:
            return dist
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))
    return -1
```

**Complexity:** O(n²) time, O(n²) space.

**Tip:** 8-directional movement means diagonals count as 1 step. BFS handles this naturally.

**Visual Walkthrough:**
```
grid = [[0,0,0],[1,1,0],[1,1,0]]

BFS from (0,0) in 8 directions.

Level 0: (0,0)
Level 1: (0,1), (1,0), (1,1) — but (1,1)=1 blocked → skip
         (0,1)=0, (1,0)=1 blocked
         Only (0,1) is valid
Level 2: From (0,1): (0,2), (1,2), (2,2)
         (0,2)=0, (1,2)=0, (2,2)=0
         All valid
Level 3: From (1,2): (2,1)=1 blocked, (2,2)=0 already visited
         From (2,2): (2,1)=1 blocked
         From (0,2): (1,2) visited, (-1,2) OOB

Shortest path length = 3
Path: (0,0)→(0,1)→(1,2)→(2,2)
```

**Common Mistakes:**
- Using only 4 directions (problem allows 8, including diagonals)
- Forgetting that blocked cells (1) can't be traversed
- Not handling start or end blocked → -1

**Edge Cases:**
- Start or end cell = 1 → -1
- n=1, grid[0][0]=0 → 1
- n=1, grid[0][0]=1 → -1

**Pattern Recognition:**
**Grid BFS (8-directional)**: Shortest path in binary matrix. Used in: Minimum Path Sum, Shortest Path in Grid with Obstacle Elimination.
---





### 30. Reconstruct Itinerary

**Problem:** Given a list of airport tickets `[from, to]`, reconstruct the itinerary in lexical order. All tickets must be used exactly once.

**Approach:** Hierholzer's algorithm for Eulerian path. Build adjacency list (sorted), DFS greedily, push to result when stuck.

**Code:**
```python
# findItinerary: implement solution
from collections import defaultdict

def findItinerary(tickets):
    graph = defaultdict(list)
    for u, v in tickets:
        graph[u].append(v)
    for k in graph:
        graph[k].sort(reverse=True)

    result = []
    def dfs(airport):
        while graph[airport]:
            dfs(graph[airport].pop())
        result.append(airport)

    dfs("JFK")
    return result[::-1]
```

**Complexity:** O(E × log E) time, O(V + E) space.

**Tip:** Sort in reverse and use `pop()` to get lexical order efficiently. Hierholzer's algorithm naturally produces the correct path.

**Visual Walkthrough:**
```
tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]

Graph:
JFK → ATL, SFO (lexicographically: ATL before SFO)
ATL → JFK, SFO
SFO → ATL

Hierholzer's algorithm (DFS post-order):
Start at JFK.
Visit ATL (lexicographically first):
  Visit JFK: done → push JFK
  Visit SFO: done → push SFO
ATL done → push ATL
Visit SFO:
  Visit ATL:
    Visit SFO: done → push SFO
  ATL done → push ATL
SFO done → push SFO

Reverse: JFK→ATL→JFK→SFO→ATL→SFO

Itinerary: ["JFK","ATL","JFK","SFO","ATL","SFO"]
```

**Common Mistakes:**
- Using BFS instead of DFS (Hierholzer is DFS-based)
- Not using a multiset/multimap (tickets can have duplicates)
- Forgetting to reverse the result (post-order gives reverse itinerary)

**Edge Cases:**
- Single ticket → just that route
- Multiple tickets from same source → take lexicographically smallest first
- Tickets forming a cycle → Eulerian circuit, return to start

**Pattern Recognition:**
**Eulerian Path (Hierholzer)**: Find path using all edges exactly once. Used in: Reconstruct Itinerary, Eulerian Circuit in Directed Graph.
---





### 31. Minimum Height Trees

**Problem:** Given `n` nodes and edges, find all nodes that, when used as roots, produce a tree with minimum height.

**Approach:** Topological sort peeling. Remove leaf nodes layer by layer until 1 or 2 nodes remain — those are the MHT roots.

**Code:**
```python
# findMinHeightTrees: implement solution
from collections import defaultdict, deque

def findMinHeightTrees(n, edges):
    if n == 1:
        return [0]
    graph = defaultdict(list)
    degree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        degree[u] += 1
        degree[v] += 1

    queue = deque([i for i in range(n) if degree[i] == 1])
    remaining = n
    while remaining > 2:
        remaining -= len(queue)
        for _ in range(len(queue)):
            leaf = queue.popleft()
            for nei in graph[leaf]:
                degree[nei] -= 1
                if degree[nei] == 1:
                    queue.append(nei)
    return list(queue)
```

**Complexity:** O(n) time, O(n) space.

**Tip:** There are at most 2 MHT roots. Peeling leaves is equivalent to finding the graph's "center".

**Visual Walkthrough:**
```
n=6, edges=[[0,3],[1,3],[2,3],[4,3],[5,4]]

Topological peeling (leaf removal):

Step 1: Leaves = {0,1,2,5}
Remove leaves and their edges:
  3 loses edges to 0,1,2 → degree=1 (only 4 left)
  4 loses edge to 5 → degree=1 (only 3 left)

Step 2: Leaves = {3,4}
Remove leaves:
  3 removed, 4 removed

Remaining nodes ≤ 2 → centroids = {3,4}

MHT roots: [3, 4]

Key insight: Centroids are the middle of the longest path.
```

**Common Mistakes:**
- Trying DFS from each node (O(n²))
- Not handling n=1 or n=2 edge cases
- Forgetting that MHT can have 1 or 2 roots

**Edge Cases:**
- n=1 → [0]
- n=2 → [0,1] (both are centroids)
- Line graph (path) → 1 or 2 centroids (middle nodes)

**Pattern Recognition:**
**Topological Peeling (Leaf Removal)**: Repeatedly remove leaves until 1-2 nodes remain. Used in: Minimum Height Trees, Find Eventual Safe States.
---





### 32. Strongly Connected Components (Kosaraju's Algorithm)

**Problem:** Given a directed graph, find all strongly connected components.

**Approach:** Kosaraju's: (1) Run DFS, record finish order. (2) Transpose graph. (3) Run DFS on transposed graph in reverse finish order.

**Code:**
```python
# kosaraju: implement solution
def kosaraju(n, graph):
    visited = [False] * n
    order = []

    def dfs1(u):
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)

    for i in range(n):
        if not visited[i]:
            dfs1(i)

    transpose = [[] for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            transpose[v].append(u)

    visited = [False] * n
    components = []

    def dfs2(u, comp):
        visited[u] = True
        comp.append(u)
        for v in transpose[u]:
            if not visited[v]:
                dfs2(v, comp)

    for u in reversed(order):
        if not visited[u]:
            comp = []
            dfs2(u, comp)
            components.append(comp)

    return components
```

**Complexity:** O(V + E) time, O(V + E) space.

**Tip:** The first DFS determines processing order; the second DFS on the transposed graph finds SCCs.

**Visual Walkthrough:**
```
graph:
0 → 1 → 2
↑   ↓   ↓
4 ← 3 ← 5

Step 1: DFS to get finishing order (post-order times):
Start 0: visit 1, visit 2, visit 3... 
Order (finishing): [5, 4, 3, 2, 1, 0]

Step 2: Transpose graph (reverse all edges):
0 ← 1 ← 2
↓   ↑   ↑
4 → 3 → 5

Step 3: DFS on transposed graph in reverse finishing order:
DFS from 0: visit 0 → no more → SCC = {0}
DFS from 1: visit 1, visit 5, visit 4, visit 3, visit 2 → SCC = {1,2,3,4,5}

SCCs: {0}, {1,2,3,4,5}
```

**Common Mistakes:**
- Not reversing graph for second pass
- Getting the DFS post-order wrong
- Forgetting to process ALL nodes (disconnected components may exist)

**Edge Cases:**
- Single node → one SCC
- DAG → each node is its own SCC
- Fully connected graph → one SCC

**Pattern Recognition:**
**Kosaraju's SCC**: 2-pass DFS (order + transpose). Used in: Strongly Connected Components, Tarjan's SCC.
---





### 33. Number of Islands II

**Problem:** Initially empty grid. Given a list of `(row, col)` positions, add land one by one. After each addition, return the count of islands.

**Approach:** Union-Find. When adding land, unite with adjacent existing lands and decrement count.

**Code:**
```python
# numIslands2: implement solution
def numIslands2(m, n, positions):
    parent = {}
    rank = {}
    count = [0]

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        count[0] -= 1

    result = []
    for r, c in positions:
        pos = (r, c)
        if pos in parent:
            result.append(count[0])
            continue
        parent[pos] = pos
        rank[pos] = 0
        count[0] += 1
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            neighbor = (r + dr, c + dc)
            if neighbor in parent:
                union(pos, neighbor)
        result.append(count[0])
    return result
```

**Complexity:** O(K × α(M×N)) ≈ O(K) time where K = positions. O(M×N) space.

**Tip:** Union-Find with path compression and union by rank is perfect for dynamic connectivity.

**Visual Walkthrough:**
```
m=3, n=3, positions=[[0,0],[0,1],[1,2],[2,1]]

Union-Find with virtual island count:

init: grid=all water, islandCount=0

Add (0,0): new island → count=1 → [1]
Add (0,1): adjacent to (0,0) → union → count=1 → [1,1]
  Actually: count=2 (new island), then union with (0,0) reduces to 1
Add (1,2): isolated → count=2 → [1,1,2]
Add (2,1): adjacent to none → count=3 → [1,1,2,3]

Answer: [1, 1, 2, 3]

Key: Each new island starts count+1, but unions with adjacent islands reduce count.
```

**Common Mistakes:**
- Not checking 4-directional adjacency for unions
- Double-counting islands (new island + union multiple neighbors)
- Not handling duplicate positions (problem may add same position multiple times)

**Edge Cases:**
- Empty positions → []
- All positions same cell → [1]
- Positions that connect multiple islands → count drops by number of merged islands - 1

**Pattern Recognition:**
**Dynamic Union-Find**: Union adjacent land cells as they're added. Used in: Number of Islands II, Number of Connected Components (dynamic).
---





### 34. Shortest Path Visiting All Nodes

**Problem:** Given an undirected connected graph with `n` nodes (0 to n-1), find the shortest path that visits every node at least once, starting from any node.

**Approach:** BFS on state `(current_node, visited_mask)`. Bitmask tracks which nodes have been visited.

**Code:**
```python
# shortestPathLength: implement solution
from collections import deque

def shortestPathLength(graph):
    n = len(graph)
    all_visited = (1 << n) - 1
    queue = deque()
    visited = set()
    for i in range(n):
        state = (i, 1 << i)
        queue.append((state, 0))
        visited.add(state)
    while queue:
        (node, mask), dist = queue.popleft()
        if mask == all_visited:
            return dist
        for nei in graph[node]:
            new_mask = mask | (1 << nei)
            state = (nei, new_mask)
            if state not in visited:
                visited.add(state)
                queue.append((state, dist + 1))
    return -1
```

**Complexity:** O(n × 2ⁿ) time, O(n × 2ⁿ) space.

**Tip:** Bitmask DP/BFS is key for "visit all nodes" problems. `1 << i` sets the i-th bit.

**Visual Walkthrough:**
```
n=4, graph=[[1,2,3],[0],[0],[0]]

We need shortest path visiting ALL nodes.

DP + BFS: dp[mask][node] = visited nodes (mask) ending at node

Start: dp[1][0]=0 (visited node 0 only)
        dp[2][1]=0 (visited node 1 only)
        dp[4][2]=0
        dp[8][3]=0

BFS expand:
mask=1 (0): visit neighbors 1,2,3
  mask=3=011 (0,1): dp[3][1]=1
  mask=5=101 (0,2): dp[5][2]=1
  mask=9=1001 (0,3): dp[9][3]=1
...
mask=15=1111 (all nodes): when first reached, return distance

Answer: shortest path covering all nodes
```

**Common Mistakes:**
- Trying pure BFS/DFS without bitmask (state explosion)
- Not using DP + BFS (Dijkstra on state: (mask, node))
- Forgetting the graph is unweighted (BFS works, not Dijkstra)

**Edge Cases:**
- n=1 → 0 (already visited all)
- n=2, one edge → 1
- Complete graph → n-1

**Pattern Recognition:**
**Bitmask DP + BFS**: State = (visited_mask, current_node). Used in: Traveling Salesman Problem, Shortest Path Visiting All Nodes.
---





### 35. Parallel Courses III

**Problem:** Given `n` courses, prerequisites, and time[i] for each course, find minimum total time to finish all courses. Prerequisites must be completed before a course can start.

**Approach:** Topological sort with DP. `dp[node]` = earliest time course finishes. `dp[nei] = max(dp[nei], dp[node] + time[nei])`.

**Code:**
```python
# minimumTime: implement solution
from collections import defaultdict, deque

def minimumTime(n, relations, time):
    graph = defaultdict(list)
    indegree = [0] * n
    for u, v in relations:
        graph[u - 1].append(v - 1)
        indegree[v - 1] += 1

    dp = [0] * n
    queue = deque()
    for i in range(n):
        if indegree[i] == 0:
            dp[i] = time[i]
            queue.append(i)

    while queue:
        node = queue.popleft()
        for nei in graph[node]:
            dp[nei] = max(dp[nei], dp[node] + time[nei])
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)

    return max(dp)
```

**Complexity:** O(V + E) time, O(V) space.

**Tip:** This is topological sort + DP. The answer is the max value in `dp[]` because all courses must finish.

**Visual Walkthrough:**
```
n=3, relations=[[1,3],[2,3]], time=[3,2,5]

Graph: 1→3, 2→3
Course 1 takes 3 months, course 2 takes 2, course 3 takes 5.

Topological order + DP for earliest finish:

Indegrees: [0,0,0] (1-indexed)
1→3: indeg[3]++, 2→3: indeg[3]++

Queue: [1,2] (indeg=0)
dist[1]=3, dist[2]=2

Process 1: indeg[3]-- → indeg[3]=1
  dist[3]=max(dist[3], dist[1]+time[3]) = max(0, 3+5) = 8
Process 2: indeg[3]-- → indeg[3]=0
  Queue push 3

Process 3: no dependents

Max dist = max(3, 2, 8) = 8

Answer: 8 months (take courses 1+3 or 2+3)
```

**Common Mistakes:**
- Not adding the course's own time to the DP (dp[node] = time[node] + max(dp[prereqs]))
- Forgetting that courses can be taken in parallel (no limit on concurrent courses)
- Wrong initialization for incoming degree

**Edge Cases:**
- No prerequisites → max(time) (all courses in parallel)
- Single course → its time
- Chain dependency → sum of all times

**Pattern Recognition:**
**DP on DAG (Parallel/Distributed Processing)**: Topological sort + DP for earliest completion. Used in: Parallel Courses I/II, Schedule Tasks with Dependencies.
---

## Quick Reference — Algorithm Selection

| Pattern | Problems |
|---|---|
| **DFS/BFS traversal** | 1, 2, 3, 6, 8, 9, 15, 29 |
| **Kahn's Topological Sort** | 11, 12, 22, 35 |
| **DFS Topological Sort** | 21, 26, 30, 32 |
| **Union-Find** | 16, 17, 18, 33 |
| **Dijkstra / Shortest Path** | 19, 20, 24, 25 |
| **0-1 BFS** | 28 |
| **Multi-source BFS** | 6, 15 |
| **BFS on State Space** | 14, 27, 34 |
| **Reverse BFS** | 13 |
| **Leaf Peeling** | 31 |
| **Bitmask BFS** | 34 |
| **Tarjan's / Bridges** | 26 |
| **Hierholzer's / Euler** | 30 |
| **Kosaraju's / SCC** | 32 |
| **Sliding Window** | 5 |
| **Greedy / Simple** | 4, 7, 10 |

---

## Key Formulas & Tricks

```
# Union-Find with Path Compression
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

# Kahn's Algorithm Template
queue = deque([n for n in range(V) if indegree[n] == 0])
order = []
while queue:
    node = queue.popleft()
    order.append(node)
    for nei in graph[node]:
        indegree[nei] -= 1
        if indegree[nei] == 0:
            queue.append(nei)

# Dijkstra Template
heap = [(0, start)]
dist = {start: 0}
while heap:
    d, node = heapq.heappop(heap)
    if d > dist.get(node, float('inf')):
        continue
    for nei, w in graph[node]:
        if dist.get(nei, float('inf')) > d + w:
            dist[nei] = d + w
            heapq.heappush(heap, (d + w, nei))

# Tarjan's Bridge Detection
if low[v] > disc[u]:  # Bridge found!
    bridges.append((u, v))

# 0-1 BFS
if cost == 0:
    deque.appendleft((nr, nc))
else:
    deque.append((nr, nc))
```

---

## Detailed Approach Notes for Every Problem


### Problem 1 — Number of Islands
- **Why DFS over BFS?** DFS is simpler to write recursively and the grid size (typically ≤ 300×300) won't hit stack limits in Python.
- **Key insight:** Every time you find a `'1'`, you've discovered a new island. Flood-fill to mark the entire island as visited by changing `'1'` to `'0'`.
- **Edge cases:** Empty grid (`[]`), grid with no land, grid entirely land.
- **Interview follow-up:** "What if diagonals also count?" → Add 4 more directions: `[(1,1),(1,-1),(-1,1),(-1,-1)]`.


### Problem 2 — Flood Fill
- **Why check `orig == newColor`?** Without this check, if the original color equals the new color, DFS would recurse infinitely.
- **In-place modification:** We modify the input image directly — no extra visited set needed.
- **Edge cases:** Single pixel image, all pixels already the new color.
- **Interview follow-up:** "Can you do it iteratively?" → Use a stack or queue for BFS/DFS.


### Problem 3 — Find if Path Exists in Graph
- **BFS vs DFS:** Both work. BFS is slightly better for very deep graphs (avoids stack overflow).
- **Union-Find alternative:** `O(α(n))` per operation. Build by iterating edges, then `find(source) == find(destination)`.
- **Edge cases:** Single node (`n=1`), no edges, source == destination.
- **Interview follow-up:** "What if edges are directed?" → Same approach, just don't add reverse edges.


### Problem 4 — Find Center of Star Graph
- **Why it works:** The center connects to ALL other nodes, so it must appear in every edge. The intersection of the first two edges gives the center.
- **No graph construction needed:** This is an O(1) observation problem.
- **Edge cases:** `n=2` (only one edge).
- **Interview follow-up:** "What if it's not a star graph?" → You'd need DFS/BFS to find the node with max degree.


### Problem 5 — Maximum Number of Vowels in Substring
- **Sliding window:** Remove one element, add one element — O(1) update per step.
- **Why a set?** O(1) membership test for vowel checking.
- **Edge cases:** `k == len(s)` (whole string), `k == 1`, no vowels.
- **Interview follow-up:** "What about uppercase vowels?" → Add `.lower()` or extend the set to `'AEIOUaeiou'`.


### Problem 6 — Rotting Oranges
- **Multi-source BFS:** All rotten oranges start at minute 0. This naturally computes the minimum time because BFS explores layer by layer.
- **Count fresh oranges:** Decrease count when rotting. If count reaches 0, all rotted.
- **Edge cases:** No fresh oranges (return 0), unreachable fresh oranges (return -1).
- **Interview follow-up:** "What if rotten oranges have different ages?" → Use a priority queue (Dijkstra-like approach).


### Problem 7 — Is Graph Bipartite
- **2-coloring:** If you can color every node with 2 colors such that no adjacent nodes share a color, the graph is bipartite.
- **Disconnected components:** Must check all nodes — some component might not be bipartite even if the first one is.
- **Edge cases:** Single node (bipartite), self-loop (not bipartite).
- **Interview follow-up:** "How many colors for general graph coloring?" → NP-hard in general, but 2-color is polynomial.


### Problem 8 — Number of Provinces
- **Province = connected component:** Each DFS/BFS call from an unvisited node discovers one province.
- **Adjacency matrix vs list:** The input is a matrix, so iterating neighbors is O(n) per node.
- **Edge cases:** All isolated nodes (n provinces), fully connected (1 province).
- **Interview follow-up:** "Can you do it with Union-Find?" → Yes, unite connected nodes, count unique parents.


### Problem 9 — Clone Graph
- **HashMap is essential:** Maps original node → cloned node. Prevents re-cloning and infinite loops.
- **BFS order doesn't matter:** DFS or BFS both work since we're just copying structure.
- **Edge cases:** `None` input, single node, cycle in graph.
- **Interview follow-up:** "Deep copy vs shallow copy?" → Deep copy means cloned nodes are independent objects.


### Problem 10 — Find the Town Judge
- **Trust score = in-degree − out-degree:** Judge has score `n-1` (everyone trusts them, they trust nobody).
- **O(n) space:** Just an array of size `n+1`.
- **Edge cases:** `n=1` (return 1), no trust relationships, multiple candidates.
- **Interview follow-up:** "What if there could be multiple judges?" → Return list of all with score `n-1`.


### Problem 11 — Course Schedule
- **Cycle detection = can't finish:** If there's a cycle in the prerequisite graph, at least one course depends on itself.
- **Kahn's algorithm:** If the topological sort doesn't include all courses, there's a cycle.
- **Edge cases:** No prerequisites (all finishable), single course with self-prerequisite.
- **Interview follow-up:** "What courses can you take first?" → Use Course Schedule II (topological order).


### Problem 12 — Course Schedule II
- **Kahn's gives the order:** Nodes with zero in-degree are available to take. Process them first.
- **Multiple valid orders:** Any topological sort is acceptable.
- **Edge cases:** Cycle (return `[]`), no prerequisites (any order).
- **Interview follow-up:** "Lexicographically smallest order?" → Use a min-heap instead of a queue.


### Problem 13 — Pacific Atlantic Water Flow
- **Reverse thinking:** Instead of "can water flow FROM this cell TO ocean?", ask "can ocean water REACH this cell?"
- **Border cells as sources:** Pacific border = top row + left column. Atlantic border = bottom row + right column.
- **Height condition:** Water flows to equal or lower height, so from ocean perspective, we can reach cells with equal or HIGHER height.
- **Edge cases:** 1×1 grid (both oceans if any height), single row/column.
- **Interview follow-up:** "What if water can only flow downhill?" → Reverse the comparison.


### Problem 14 — Word Ladder
- **BFS for shortest path:** BFS guarantees the minimum number of transformations.
- **Try all 26 letters:** For each position in the word, try changing it to each letter.
- **Word set for O(1) lookup:** Convert word list to set for fast membership checking.
- **Edge cases:** `beginWord == endWord` (return 1), no valid path (return 0).
- **Interview follow-up:** "Can you do bidirectional BFS?" → Start from both ends, meeting in the middle.


### Problem 15 — Walls and Gates
- **Multi-source BFS:** All gates are sources. Each level of BFS represents one unit of distance.
- **INF as unvisited:** The value `2147483647` (INT_MAX) serves as both "unvisited" and "infinite distance".
- **In-place modification:** Update the grid directly — no separate distance array.
- **Edge cases:** No gates (nothing changes), no empty rooms.
- **Interview follow-up:** "What if gates have different priorities?" → Use Dijkstra instead of BFS.


### Problem 16 — Redundant Connection
- **Union-Find is perfect:** If both endpoints are already connected, adding this edge creates a cycle.
- **Path compression:** `parent[x] = parent[parent[x]]` flattens the tree during find.
- **Last edge in cycle:** Processing edges in order and returning the first conflicting edge gives the correct answer.
- **Edge cases:** Multiple cycles (return the last conflicting edge), single edge.
- **Interview follow-up:** "What if you need to find ALL redundant edges?" → Collect all edges where `find(u) == find(v)`.


### Problem 17 — Accounts Merge
- **Union emails:** Emails in the same account are connected. Shared emails across accounts merge them.
- **Group by root:** After unions, group emails by their root parent.
- **Name lookup:** The account name comes from any email in the group (they all have the same name).
- **Edge cases:** No shared emails (no merging), all accounts share emails (one big merge).
- **Interview follow-up:** "What if names differ for same email?" → That's a data inconsistency — handle per requirements.


### Problem 18 — Graph Valid Tree
- **Two conditions:** Exactly `n-1` edges AND the graph is connected.
- **Tree properties:** A connected graph with `n-1` edges is always a tree (no cycles, fully connected).
- **Edge cases:** `n=1` with no edges (valid tree), disconnected components.
- **Interview follow-up:** "How to find the tree's root?" → Any node can be root in an undirected tree.


### Problem 19 — Network Delay Time
- **Dijkstra for weighted shortest path:** Finds minimum time to reach each node.
- **Answer is max distance:** All nodes must receive the signal, so the answer is the farthest node.
- **Visited set optimization:** Skip nodes already processed (standard Dijkstra).
- **Edge cases:** Disconnected graph (return -1), single node (return 0).
- **Interview follow-up:** "What if there are negative weights?" → Use Bellman-Ford instead.


### Problem 20 — Cheapest Flights Within K Stops
- **K constraint changes everything:** Standard Dijkstra doesn't account for stops.
- **Track stops in state:** `(cost, city, remaining_stops)`.
- **Revisiting is okay:** A node might be reachable with lower cost but fewer remaining stops.
- **Edge cases:** Direct flight (0 stops), no valid path within K stops.
- **Interview follow-up:** "What about unlimited stops?" → Standard Dijkstra (remove K constraint).


### Problem 21 — Alien Dictionary
- **Compare adjacent words:** The first differing character gives a precedence rule.
- **Topological sort:** Characters form a DAG. The topo sort gives the ordering.
- **Invalid case:** If a longer word appears before a shorter prefix word (e.g., "abc" before "ab"), return `""`.
- **Cycle detection:** If topo sort result has fewer characters than input, there's a cycle.
- **Edge cases:** Single word (no ordering info), words with no common prefix.
- **Interview follow-up:** "What if there are multiple valid orderings?" → Return any valid one (BFS order might vary).


### Problem 22 — Parallel Courses
- **BFS levels = semesters:** Each BFS level represents courses that can be taken simultaneously.
- **Same as topological sort:** Just count the number of levels.
- **Edge cases:** No prerequisites (1 semester), impossible (return -1).
- **Interview follow-up:** "What if each course has a duration?" → Use Course Schedule III (DP + topological sort).


### Problem 23 — Longest Path in DAG
- **Topological sort + DP:** Process nodes in topo order, relax distances to neighbors.
- **No cycles guaranteed:** DAG means we can safely process in topological order.
- **Multiple sources:** Start from all nodes with in-degree 0.
- **Edge cases:** Single node (length 0), disconnected components.
- **Interview follow-up:** "What if there are cycles?" → Longest path in general graph is NP-hard.


### Problem 24 — Swim in Rising Water
- **Dijkstra on time:** The "cost" is the maximum elevation encountered along the path.
- **Priority on minimum time:** Always explore the path with the smallest maximum elevation first.
- **Visited set:** Once visited, we've found the optimal time for that cell.
- **Edge cases:** Single cell (return its value), all same elevation.
- **Interview follow-up:** "Binary search approach?" → Binary search on time + BFS to check connectivity.


### Problem 25 — Path with Maximum Probability
- **Maximize product, not sum:** Standard Dijkstra minimizes sum of weights; here we maximize the product.
- **Negative heap trick:** Python's `heapq` is a min-heap, so negate probabilities.
- **Relaxation condition:** `new_prob > current_prob` means we found a better path.
- **Edge cases:** No path (return 0), direct edge (might be best).
- **Interview follow-up:** "What about log probabilities?" → Convert to logs and use standard Dijkstra (sum of logs = log of product).


### Problem 26 — Critical Connections (Bridges)
- **Tarjan's algorithm:** Uses DFS discovery times and low-link values.
- **Bridge condition:** `low[v] > disc[u]` means no back-edge from subtree of `v` reaches `u` or above.
- **Low-link update:** `low[u] = min(low[u], disc[v])` for back-edges (NOT `low[v]`).
- **Edge cases:** No bridges (complete graph), all edges are bridges (linear chain).
- **Interview follow-up:** "Find articulation points?" → Similar algorithm, condition: `low[v] >= disc[u]`.


### Problem 27 — Word Ladder II
- **Two-phase approach:** BFS builds shortest-path DAG, DFS enumerates all paths.
- **Level-by-level BFS:** Critical for correctness — don't mark visited until the entire level is processed.
- **Graph construction:** Each word points to words reachable in the next step of shortest paths.
- **Edge cases:** No path (return `[]`), multiple shortest paths of same length.
- **Interview follow-up:** "Can you do it in one pass?" → Extremely complex; the two-pass approach is standard.


### Problem 28 — Minimum Cost to Make Valid Path
- **0-1 BFS:** When edge weights are only 0 or 1, use a deque instead of a heap.
- **Cost 0 = following arrow:** Moving in the direction the arrow points costs nothing.
- **Cost 1 = changing arrow:** Moving in a different direction costs 1.
- **Edge cases:** Already valid path (cost 0), blocked paths.
- **Interview follow-up:** "What if costs are 0, 1, 2?" → Use a 0-1-2 BFS or Dijkstra.


### Problem 29 — Shortest Path in Binary Matrix
- **BFS on grid:** Standard shortest path in unweighted graph.
- **8 directions:** Diagonals are valid moves (cost 1 each).
- **Start and end must be open:** Check `grid[0][0]` and `grid[n-1][n-1]` first.
- **Edge cases:** 1×1 grid (return 1 if open), blocked start/end.
- **Interview follow-up:** "What about weighted cells?" → Use Dijkstra.


### Problem 30 — Reconstruct Itinerary
- **Eulerian path:** Uses every edge exactly once.
- **Hierholzer's algorithm:** DFS greedily, push to result when stuck.
- **Reverse sort + pop:** Ensures lexical order efficiently.
- **Edge cases:** Single ticket, multiple valid itineraries (return lexical smallest).
- **Interview follow-up:** "What if not all tickets can be used?" → That would make it impossible; constraints guarantee a valid itinerary exists.


### Problem 31 — Minimum Height Trees
- **Leaf peeling:** Remove leaves layer by layer. The last 1-2 nodes are the centers.
- **At most 2 roots:** A tree's center is either 1 or 2 nodes.
- **Topological sort on tree:** Process nodes with degree 1 (leaves) first.
- **Edge cases:** Single node (return `[0]`), two nodes (return either).
- **Interview follow-up:** "Why at most 2?" → A path has at most 2 center nodes (middle of the longest path).


### Problem 32 — Strongly Connected Components (Kosaraju's)
- **Two-pass DFS:** First pass gets finish order, second pass on transposed graph finds SCCs.
- **Transpose graph:** Reverse all edges. SCCs become disconnected components.
- **Finish order matters:** Processing in reverse finish order ensures we visit sink SCCs first.
- **Edge cases:** Single SCC (entire graph), no edges (each node is its own SCC).
- **Interview follow-up:** "Tarjan's vs Kosaraju's?" → Tarjan's is one-pass; Kosaraju's is conceptually simpler.


### Problem 33 — Number of Islands II
- **Dynamic Union-Find:** As land is added, unite with adjacent lands and track count.
- **No removal:** Land is only added, never removed (simplifies Union-Find).
- **Incremental count:** Start at 0, add 1 for new land, subtract 1 for each successful union.
- **Edge cases:** Duplicate positions, positions outside grid.
- **Interview follow-up:** "What if land can also be removed?" → Much harder; need fully dynamic connectivity (Euler tour tree, etc.).


### Problem 34 — Shortest Path Visiting All Nodes
- **Bitmask state:** `visited_mask` tracks which nodes have been visited using bit operations.
- **BFS on state space:** States are `(current_node, visited_mask)`.
- **Bit operations:** `mask | (1 << i)` adds node i to visited set.
- **Edge cases:** Single node (return 0), fully connected (shortest path might be small).
- **Interview follow-up:** "What if n > 20?" → Bitmask is infeasible; need approximation or different approach.


### Problem 35 — Parallel Courses III
- **Topological sort + DP:** `dp[node]` stores the earliest finish time for that course.
- **Relaxation:** `dp[nei] = max(dp[nei], dp[node] + time[nei])` ensures all prerequisites finish first.
- **Answer is max(dp):** All courses must complete; the last one determines total time.
- **Edge cases:** Single course (return its time), no prerequisites (parallel all, return max time).
- **Interview follow-up:** "What if you can retake courses?" → Completely different problem (shortest path with costs).

---

## Common Interview Questions About Graphs

### Q: When to use BFS vs DFS?
**A:** BFS for shortest path in unweighted graphs, level-order traversal, and multi-source problems. DFS for cycle detection, topological sort, connected components, and path existence. BFS uses more space but is optimal for shortest path.

### Q: When to use Union-Find?
**A:** When you need dynamic connectivity — repeatedly connecting components and querying whether two nodes are connected. Problems: Redundant Connection, Accounts Merge, Number of Islands II.

### Q: How to detect a cycle in a directed graph?
**A:** Three colors (white/gray/black) DFS: gray = currently in recursion stack. If you reach a gray node, there's a cycle. Alternatively, Kahn's algorithm: if topo sort result has fewer nodes than total, there's a cycle.

### Q: How to detect a cycle in an undirected graph?
**A:** DFS with parent tracking. If you visit a node that's already visited and isn't the parent, there's a cycle. Union-Find also works: if `find(u) == find(v)` before uniting, adding edge `(u,v)` creates a cycle.

### Q: What is topological sort?
**A:** A linear ordering of vertices in a DAG such that for every edge `(u,v)`, `u` comes before `v`. Only possible if the graph is a DAG (no cycles). Used for: prerequisite scheduling, build systems, course planning.

### Q: What is the difference between Dijkstra and Bellman-Ford?
**A:** Dijkstra: O(E log V), only works with non-negative weights, uses greedy + priority queue. Bellman-Ford: O(VE), handles negative weights, detects negative cycles. Use Dijkstra by default; Bellman-Ford only when negative weights exist.

### Q: What is a bridge/articulation point?
**A:** Bridge: an edge whose removal increases connected components. Articulation point: a vertex whose removal increases connected components. Both found using Tarjan's algorithm with discovery times and low-link values.

### Q: What is an Eulerian path?
**A:** A path that visits every edge exactly once. Existence: at most 2 nodes have odd degree (start/end). Hierholzer's algorithm finds it in O(E) time. Used in: route planning, DNA reconstruction.

---

## Complexity Cheat Sheet

```
Algorithm              Time          Space       Use Case
─────────────────────────────────────────────────────────────
BFS/DFS                O(V+E)        O(V)        Traversal, shortest path (unweighted)
Dijkstra               O(E log V)    O(V)        Shortest path (non-negative weights)
Bellman-Ford           O(VE)         O(V)        Shortest path (negative weights)
Kahn's Topo Sort       O(V+E)        O(V)        Topological ordering, cycle detection
Kosaraju's SCC         O(V+E)        O(V+E)      Strongly connected components
Tarjan's Bridges       O(V+E)        O(V)        Bridges and articulation points
Union-Find             O(α(n))       O(n)        Dynamic connectivity
0-1 BFS                O(V+E)        O(V)        Shortest path (0/1 weights)
Topological Sort + DP  O(V+E)        O(V)        Longest/shortest path in DAG
Bitmask BFS            O(V × 2^V)    O(V × 2^V)  Visit all nodes shortest path
```

---

## Python Graph Snippets to Memorize

```python
# Build adjacency list from edge list
from collections import defaultdict
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)  # undirected

# BFS template
from collections import deque
def bfs(start, graph):
    visited = set([start])
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                queue.append(nei)

# DFS template (recursive)
def dfs(node, graph, visited):
    visited.add(node)
    for nei in graph[node]:
        if nei not in visited:
            dfs(nei, graph, visited)

# DFS template (iterative)
def dfs_iter(start, graph):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for nei in graph[node]:
            stack.append(nei)

# Topological sort (Kahn's)
from collections import deque
def topo_sort(n, graph, indegree):
    queue = deque([i for i in range(n) if indegree[i] == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)
    return order if len(order) == n else []

# Dijkstra
import heapq
def dijkstra(graph, start):
    dist = {start: 0}
    heap = [(0, start)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist.get(node, float('inf')):
            continue
        for nei, w in graph[node]:
            nd = d + w
            if nd < dist.get(nei, float('inf')):
                dist[nei] = nd
                heapq.heappush(heap, (nd, nei))
    return dist

# Union-Find
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
    def connected(self, x, y):
        return self.find(x) == self.find(y)

# Tarjan's Bridge Detection
def find_bridges(n, graph):
    disc = [-1] * n
    low = [-1] * n
    timer = [0]
    bridges = []
    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        for v in graph[u]:
            if disc[v] == -1:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((u, v))
            elif v != parent:
                low[u] = min(low[u], disc[v])
    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)
    return bridges

# 0-1 BFS
from collections import deque
def zero_one_bfs(graph, start):
    dist = {start: 0}
    dq = deque([start])
    while dq:
        node = dq.popleft()
        for nei, weight in graph[node]:
            nd = dist[node] + weight
            if nd < dist.get(nei, float('inf')):
                dist[nei] = nd
                if weight == 0:
                    dq.appendleft(nei)
                else:
                    dq.append(nei)
    return dist
```

---

## Infosys SP DSE Specific Tips

1. **Graph problems appear in 20-30% of coding rounds.** Master BFS, DFS, and Union-Find.
2. **Medium problems are the sweet spot.** Focus on problems 11-25 for maximum ROI.
3. **Know your templates cold.** BFS, DFS, Dijkstra, Kahn's, Union-Find — you should write these without thinking.
4. **Always clarify:** Directed vs undirected? Weighted vs unweighted? Cycles allowed?
5. **Time management:** Spend 2-3 min on approach, 10-12 min on coding, 2-3 min on testing.
6. **Test with edge cases:** Empty input, single node, disconnected graph, all nodes connected.
7. **Union-Find is the secret weapon.** Many medium problems become easy with Union-Find.
8. **BFS for shortest path, DFS for exploration.** This is the golden rule.
9. **Multi-source BFS is common.** Problems like Rotting Oranges and Walls and Gates use it.
10. **Topological sort = scheduling.** Whenever you see prerequisites, think topological sort.

---

*Total: 35 problems | 1500+ lines | Covers BFS, DFS, Union-Find, Topo Sort, Dijkstra, Tarjan, SCC, Hierholzer, 0-1 BFS, Bitmask BFS, interview tips, and code templates*
