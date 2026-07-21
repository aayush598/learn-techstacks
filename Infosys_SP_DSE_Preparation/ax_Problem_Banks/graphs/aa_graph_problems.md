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

---

### 2. Flood Fill

**Problem:** Given an image (2D array), a starting pixel `(sr, sc)`, and a new color, replace the color of the starting pixel and all adjacent pixels of the same original color with the new color.

**Approach:** DFS from the starting pixel. For each cell matching the original color, change it to the new color and recurse to 4 neighbors.

**Code:**
```python
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

---

### 3. Find if Path Exists in Graph

**Problem:** Given `n` nodes and a list of edges, determine if there is a path from `source` to `destination`.

**Approach:** Build adjacency list, then BFS/DFS from source. Return True if destination is reached.

**Code:**
```python
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

---

### 4. Find Center of Star Graph

**Problem:** A star graph has one center node connected to all other nodes. Given `n` nodes and `edges`, find the center.

**Approach:** The center appears in every edge. Just check the first two edges — the common node is the center.

**Code:**
```python
def findCenter(edges):
    a, b = edges[0]
    c, d = edges[1]
    if a == c or a == d:
        return a
    return b
```

**Complexity:** O(1) time, O(1) space.

**Tip:** No need to build the full graph. Two edges are enough because the center is in all of them.

---

### 5. Maximum Number of Vowels in a Substring of Given Length

**Problem:** Given a string `s` and integer `k`, find the maximum number of vowels in any substring of length `k`. *(This is a sliding window problem often grouped with graph BFS thinking.)*

**Approach:** Sliding window of size `k`. Count vowels in the first window, then slide and update.

**Code:**
```python
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

---

### 6. Rotting Oranges

**Problem:** Given a grid where `0` = empty, `1` = fresh, `2` = rotten. Each minute, rotten orange rots adjacent fresh ones. Return minutes until no fresh orange left, or `-1` if impossible.

**Approach:** Multi-source BFS. Enqueue all rotten oranges at minute 0. BFS layer by layer, counting minutes.

**Code:**
```python
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

---

### 7. Is Graph Bipartite

**Problem:** Given an adjacency matrix of an undirected graph, return `True` if the graph is bipartite (2-colorable).

**Approach:** Try coloring with 2 colors using BFS/DFS. If any adjacent nodes have the same color, it's not bipartite.

**Code:**
```python
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

---

### 8. Number of Provinces

**Problem:** Given an `n x n` adjacency matrix `isConnected`, find the number of connected components (provinces).

**Approach:** Run DFS/BFS from each unvisited node, counting the number of DFS calls needed to visit all nodes.

**Code:**
```python
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

---

### 9. Clone Graph

**Problem:** Given a reference to a node in a connected undirected graph, return a deep copy of the graph.

**Approach:** BFS/DFS with a hashmap mapping original nodes to cloned nodes. For each node, clone it and recurse on unvisited neighbors.

**Code:**
```python
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

---

### 10. Find the Town Judge

**Problem:** `n` people labeled `1` to `n`. Town judge trusts nobody, everybody trusts the town judge. Given `trust` array `[a, b]` meaning `a` trusts `b`, find the town judge or return `-1`.

**Approach:** Compute in-degree minus out-degree for each person. The town judge has `n - 1` trust score (everyone trusts them, they trust nobody).

**Code:**
```python
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

---

## MEDIUM (Problems 11–25)

---

### 11. Course Schedule

**Problem:** There are `numCourses` courses with prerequisites. `prerequisites[i] = [a, b]` means you must take `b` before `a`. Return `True` if you can finish all courses.

**Approach:** Build a directed graph. Cycle detection via DFS (3-color marking) or in-degree based BFS (Kahn's algorithm).

**Code:**
```python
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

---

### 12. Course Schedule II

**Problem:** Same as Course Schedule, but return the ordering of courses to finish all, or `[]` if impossible.

**Approach:** Kahn's topological sort. Enqueue zero in-degree nodes, process level by level.

**Code:**
```python
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

---

### 13. Pacific Atlantic Water Flow

**Problem:** Given an `m x n` matrix of heights, water can flow from a cell to an adjacent cell with equal or lower height. Find cells where water can reach both the Pacific and Atlantic oceans.

**Approach:** Reverse thinking — start BFS from Pacific border cells and Atlantic border cells separately. Cells reachable from both are the answer.

**Code:**
```python
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

---

### 14. Word Ladder

**Problem:** Given `beginWord`, `endWord`, and a word list, find the shortest transformation sequence from `beginWord` to `endWord`, changing one letter at a time. Each intermediate word must be in the word list.

**Approach:** BFS from `beginWord`. For each word, try changing each letter to `a-z` and check if it's in the word set.

**Code:**
```python
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

---

### 15. Walls and Gates

**Problem:** Given an `m x n` grid with `0` (gate), `-1` (wall), and `INF` (empty room), fill each empty room with the distance to its nearest gate.

**Approach:** Multi-source BFS from all gates simultaneously. Each step increments distance.

**Code:**
```python
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

---

### 16. Redundant Connection

**Problem:** A tree with `n` nodes has one extra edge added, creating a cycle. Find the edge that, if removed, restores the tree property. If multiple, return the one that appears last.

**Approach:** Union-Find. Process edges one by one. If both endpoints are already in the same component, this edge is redundant.

**Code:**
```python
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

---

### 17. Accounts Merge

**Problem:** Given a list of accounts where each account has a name and a list of emails, merge accounts that share common emails. Return the merged accounts.

**Approach:** Union-Find on emails. Emails in the same account are united. Also unite shared emails across accounts. Then group emails by root and sort.

**Code:**
```python
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

---

### 18. Graph Valid Tree

**Problem:** Given `n` nodes and `edges`, determine if the edges form a valid tree.

**Approach:** A valid tree has exactly `n - 1` edges AND is connected. Check both conditions.

**Code:**
```python
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

---

### 19. Network Delay Time

**Problem:** Given `n` nodes and weighted directed edges, and a starting node `k`, find the time it takes for a signal to reach all nodes. Return `-1` if not all reachable.

**Approach:** Dijkstra's algorithm from node `k`. The answer is the maximum distance among all nodes.

**Code:**
```python
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

---

### 20. Cheapest Flights Within K Stops

**Problem:** Given `n` cities, flights with costs, source `src`, destination `dst`, and max `k` stops, find the cheapest price. Return `-1` if not possible.

**Approach:** Modified Dijkstra or BFS. Track `(cost, city, stops)`. Only push to heap if stops ≤ k.

**Code:**
```python
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

---

### 21. Alien Dictionary

**Problem:** Given a sorted list of words in an alien language, derive the character order (lexicographic ordering).

**Approach:** Compare adjacent words character by character. The first differing pair gives a directed edge `a → b` (a comes before b). Topological sort the resulting graph.

**Code:**
```python
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

---

### 22. Parallel Courses

**Problem:** Given `n` courses and prerequisites, find the minimum number of semesters to complete all courses (each semester you can take any number of courses whose prerequisites are met). Return `-1` if impossible.

**Approach:** Topological sort. The number of BFS levels = minimum semesters.

**Code:**
```python
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

---

### 23. Longest Path in a DAG

**Problem:** Given a Directed Acyclic Graph with `n` nodes and weighted edges, find the longest path from any node.

**Approach:** Topological sort, then process nodes in order, relaxing longest distances.

**Code:**
```python
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

---

### 24. Swim in Rising Water

**Problem:** Given an `n x n` grid where `grid[i][j]` represents elevation, water rises over time. You can swim to adjacent cells when the max elevation between them ≤ current time. Find the minimum time to swim from `(0,0)` to `(n-1,n-1)`.

**Approach:** Binary search on time + BFS/DFS, or Dijkstra (min-heap on time).

**Code:**
```python
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

---

### 25. Path with Maximum Probability

**Problem:** Given `n` cities with weighted edges (probabilities of success), find the path from `start` to `end` with maximum success probability.

**Approach:** Modified Dijkstra using max-heap (multiply probabilities instead of adding distances).

**Code:**
```python
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

---

## HARD (Problems 26–35)

---

### 26. Critical Connections (Bridges)

**Problem:** Given `n` servers and connections, find all critical connections (bridges) whose removal increases the number of disconnected components.

**Approach:** Tarjan's algorithm — DFS with discovery time and low-link values. An edge `(u, v)` is a bridge if `low[v] > disc[u]`.

**Code:**
```python
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

---

### 27. Word Ladder II

**Problem:** Find ALL shortest transformation sequences from `beginWord` to `endWord`.

**Approach:** BFS to build a DAG of shortest paths, then DFS to enumerate all paths.

**Code:**
```python
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

---

### 28. Minimum Cost to Make at Least One Valid Path in Grid

**Problem:** Given an `m x n` grid where each cell has a sign (1=right, 2=left, 3=down, 4=up), you can change any sign at cost 1. Find minimum cost to make a valid path from `(0,0)` to `(m-1,n-1)`.

**Approach:** 0-1 BFS (deque-based BFS). Moving with the arrow costs 0, changing the arrow costs 1.

**Code:**
```python
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

---

### 29. Shortest Path in a Binary Matrix

**Problem:** Given an `n x n` binary grid where `1` means open and `0` means blocked, find the shortest path from `(0,0)` to `(n-1,n-1)` moving in 8 directions. Return the path length or `-1`.

**Approach:** BFS on the grid. Each step costs 1. BFS guarantees shortest path in unweighted graphs.

**Code:**
```python
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

---

### 30. Reconstruct Itinerary

**Problem:** Given a list of airport tickets `[from, to]`, reconstruct the itinerary in lexical order. All tickets must be used exactly once.

**Approach:** Hierholzer's algorithm for Eulerian path. Build adjacency list (sorted), DFS greedily, push to result when stuck.

**Code:**
```python
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

---

### 31. Minimum Height Trees

**Problem:** Given `n` nodes and edges, find all nodes that, when used as roots, produce a tree with minimum height.

**Approach:** Topological sort peeling. Remove leaf nodes layer by layer until 1 or 2 nodes remain — those are the MHT roots.

**Code:**
```python
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

---

### 32. Strongly Connected Components (Kosaraju's Algorithm)

**Problem:** Given a directed graph, find all strongly connected components.

**Approach:** Kosaraju's: (1) Run DFS, record finish order. (2) Transpose graph. (3) Run DFS on transposed graph in reverse finish order.

**Code:**
```python
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

---

### 33. Number of Islands II

**Problem:** Initially empty grid. Given a list of `(row, col)` positions, add land one by one. After each addition, return the count of islands.

**Approach:** Union-Find. When adding land, unite with adjacent existing lands and decrement count.

**Code:**
```python
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

---

### 34. Shortest Path Visiting All Nodes

**Problem:** Given an undirected connected graph with `n` nodes (0 to n-1), find the shortest path that visits every node at least once, starting from any node.

**Approach:** BFS on state `(current_node, visited_mask)`. Bitmask tracks which nodes have been visited.

**Code:**
```python
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

---

### 35. Parallel Courses III

**Problem:** Given `n` courses, prerequisites, and time[i] for each course, find minimum total time to finish all courses. Prerequisites must be completed before a course can start.

**Approach:** Topological sort with DP. `dp[node]` = earliest time course finishes. `dp[nei] = max(dp[nei], dp[node] + time[nei])`.

**Code:**
```python
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
