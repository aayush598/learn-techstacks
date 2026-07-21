# Graph Problems - Batch 2 (Additional 40 Problems)

---

## Problem 1: Find the Town Judge

**Statement:** In a town of n people, person 1 to n. Trust[i] = [a,b] means a trusts b. Town judge trusts nobody, everybody trusts town judge. Find the judge.

**Approach:** Use an array to track trust balance. +1 for being trusted, -1 for trusting. Judge has balance = n-1.

```python
def findTownJudge(n, trust):
    balance = [0] * (n + 1)
    for a, b in trust:
        balance[a] -= 1
        balance[b] += 1
    for i in range(1, n + 1):
        if balance[i] == n - 1:
            return i
    return -1
```
**Time:** O(n) | **Space:** O(n)

---

## Problem 2: Find Center of Star Graph

**Statement:** Find the center node of a star graph (all edges connect to center).

**Approach:** The center appears in every edge. Just check first two edges - common node is center.

```python
def findCenter(edges):
    if edges[0][0] == edges[1][0] or edges[0][0] == edges[1][1]:
        return edges[0][0]
    return edges[0][1]
```
**Time:** O(1) | **Space:** O(1)

---

## Problem 3: Find if Path Exists in Graph

**Statement:** Given n nodes, edges, source, destination. Check if path exists.

**Approach:** Simple BFS/DFS from source to see if we reach destination.

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
**Time:** O(n+e) | **Space:** O(n+e)

---

## Problem 4: Number of Connected Components

**Statement:** Count connected components in undirected graph.

**Approach:** DFS/BFS from each unvisited node, increment count.

```python
def countComponents(n, edges):
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    visited = set()
    count = 0
    def dfs(node):
        visited.add(node)
        for nei in graph[node]:
            if nei not in visited:
                dfs(nei)
    for i in range(n):
        if i not in visited:
            dfs(i)
            count += 1
    return count
```
**Time:** O(n+e) | **Space:** O(n+e)

---

## Problem 5: Is Graph Bipartite

**Statement:** Check if graph can be colored with 2 colors such that no adjacent nodes have same color.

**Approach:** BFS/DFS coloring. If we find a node with same color as current, not bipartite.

```python
def isBipartite(graph):
    n = len(graph)
    color = [-1] * n
    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        stack = [start]
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
**Time:** O(n+e) | **Space:** O(n)

---

## Problem 6: Number of Nodes in Sub-Tree With Same Label

**Statement:** For each node, find number of nodes in its subtree with the same label.

**Approach:** DFS returning frequency map of labels in subtree. Merge children's maps.

```python
def countSubTrees(n, edges, labels):
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    result = [0] * n
    def dfs(node, parent):
        count = {labels[node]: 1}
        for nei in graph[node]:
            if nei != parent:
                child_count = dfs(nei, node)
                for k, v in child_count.items():
                    count[k] = count.get(k, 0) + v
        result[node] = count[labels[node]]
        return count
    dfs(0, -1)
    return result
```
**Time:** O(n) | **Space:** O(n)

---

## Problem 7: Maximum Number of Edges to Make Graph Fully Connected

**Statement:** Given n nodes and edges, find max edges to add to make graph fully connected.

**Approach:** Count connected components using Union-Find. Need (components-1) more edges.

```python
def maxNumEdgesToRemove(n, edges):
    class UnionFind:
        def __init__(self, n):
            self.p = list(range(n+1))
            self.r = [0]*(n+1)
            self.components = n
        def find(self, x):
            if self.p[x] != x: self.p[x] = self.find(self.p[x])
            return self.p[x]
        def union(self, x, y):
            px, py = self.find(x), self.find(y)
            if px == py: return False
            if self.r[px] < self.r[py]: px, py = py, px
            self.p[py] = px
            if self.r[px] == self.r[py]: self.r[px] += 1
            self.components -= 1
            return True
    alice, bob = UnionFind(n), UnionFind(n)
    edges_used = 0
    for t, u, v in sorted(edges, reverse=True):
        if t == 3:
            if alice.union(u, v):
                bob.union(u, v)
                edges_used += 1
        elif t == 1:
            if alice.union(u, v):
                edges_used += 1
        else:
            if bob.union(u, v):
                edges_used += 1
    if alice.components == 1 and bob.components == 1:
        return len(edges) - edges_used
    return -1
```
**Time:** O(e*α(n)) | **Space:** O(n)

---

## Problem 8: Is Graph Bipartite (DFS)

**Statement:** Same as Problem 5 but using DFS approach.

```python
def isBipartite(graph):
    n = len(graph)
    color = [-1] * n
    def dfs(node, c):
        color[node] = c
        for nei in graph[node]:
            if color[nei] == -1:
                if not dfs(nei, 1 - c):
                    return False
            elif color[nei] == c:
                return False
        return True
    for i in range(n):
        if color[i] == -1:
            if not dfs(i, 0):
                return False
    return True
```
**Time:** O(n+e) | **Space:** O(n)

---

## Problem 9: All Paths from Source to Target

**Statement:** Find all paths from node 0 to node n-1 in DAG.

**Approach:** Simple DFS, add path when reaching target.

```python
def allPathsSourceTarget(graph):
    n = len(graph)
    result = []
    def dfs(node, path):
        if node == n - 1:
            result.append(path[:])
            return
        for nei in graph[node]:
            path.append(nei)
            dfs(nei, path)
            path.pop()
    dfs(0, [0])
    return result
```
**Time:** O(2^n) | **Space:** O(n)

---

## Problem 10: Keys and Rooms

**Statement:** You have n rooms. Room 0 is unlocked. Each room has keys to other rooms. Can you visit all rooms?

**Approach:** DFS/BFS from room 0, count visited rooms.

```python
def canVisitAllRooms(rooms):
    visited = set([0])
    stack = [0]
    while stack:
        room = stack.pop()
        for key in rooms[room]:
            if key not in visited:
                visited.add(key)
                stack.append(key)
    return len(visited) == len(rooms)
```
**Time:** O(n+e) | **Space:** O(n)

---

## Problem 11: Number of Provinces

**Statement:** Given adjacency matrix of connections, find number of provinces (connected components).

**Approach:** DFS on adjacency matrix.

```python
def findCircleNum(isConnected):
    n = len(isConnected)
    visited = set()
    def dfs(node):
        visited.add(node)
        for j in range(n):
            if isConnected[node][j] == 1 and j not in visited:
                dfs(j)
    count = 0
    for i in range(n):
        if i not in visited:
            dfs(i)
            count += 1
    return count
```
**Time:** O(n^2) | **Space:** O(n)

---

## Problem 12: Possible Bipartition

**Statement:** Divide people into two groups such that no two people in same group dislike each other.

**Approach:** Build graph, check bipartite using BFS coloring.

```python
def possibleBipartition(n, dislikes):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    for u, v in dislikes:
        graph[u].append(v)
        graph[v].append(u)
    color = [-1] * (n + 1)
    for start in range(1, n + 1):
        if color[start] != -1:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nei in graph[node]:
                if color[nei] == -1:
                    color[nei] = 1 - color[node]
                    queue.append(nei)
                elif color[nei] == color[node]:
                    return False
    return True
```
**Time:** O(n+e) | **Space:** O(n+e)

---

## Problem 13: As Far from Land as Possible

**Statement:** Grid with 1s (land) and 0s (water). Find max distance from water to nearest land. Return -1 if no water or no land.

**Approach:** Multi-source BFS from all land cells simultaneously.

```python
def maxDistance(grid):
    from collections import deque
    n = len(grid)
    queue = deque()
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                queue.append((i, j))
    if not queue or len(queue) == n*n:
        return -1
    dist = -1
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    while queue:
        dist += 1
        for _ in range(len(queue)):
            x, y = queue.popleft()
            for dx, dy in dirs:
                nx, ny = x+dx, y+dy
                if 0<=nx<n and 0<=ny<n and grid[nx][ny] == 0:
                    grid[nx][ny] = 1
                    queue.append((nx, ny))
    return dist
```
**Time:** O(n^2) | **Space:** O(n^2)

---

## Problem 14: Surrounded Regions

**Statement:** Capture all 'O' regions completely surrounded by 'X'. Border 'O's are not captured.

**Approach:** DFS from border 'O's, mark safe. Then flip remaining 'O's to 'X'.

```python
def solve(board):
    if not board: return
    m, n = len(board), len(board[0])
    def dfs(i, j):
        if i<0 or i>=m or j<0 or j>=n or board[i][j]!='O': return
        board[i][j] = 'S'
        dfs(i+1,j); dfs(i-1,j); dfs(i,j+1); dfs(i,j-1)
    for i in range(m):
        dfs(i, 0); dfs(i, n-1)
    for j in range(n):
        dfs(0, j); dfs(m-1, j)
    for i in range(m):
        for j in range(n):
            if board[i][j]=='O': board[i][j]='X'
            elif board[i][j]=='S': board[i][j]='O'
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Problem 15: Number of Enclaves

**Statement:** Count 1s (land) that cannot reach boundary of grid.

**Approach:** DFS from boundary 1s, mark reachable. Count remaining 1s.

```python
def numEnclaves(grid):
    m, n = len(grid), len(grid[0])
    def dfs(i, j):
        if i<0 or i>=m or j<0 or j>=n or grid[i][j]!=1: return
        grid[i][j] = 0
        dfs(i+1,j); dfs(i-1,j); dfs(i,j+1); dfs(i,j-1)
    for i in range(m):
        dfs(i,0); dfs(i,n-1)
    for j in range(n):
        dfs(0,j); dfs(m-1,j)
    return sum(grid[i][j] for i in range(m) for j in range(n))
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Problem 16: Clone Graph

**Statement:** Deep copy of undirected graph.

**Approach:** DFS + HashMap to map original nodes to copies.

```python
def cloneGraph(node):
    if not node: return None
    visited = {}
    def dfs(n):
        if n in visited: return visited[n]
        copy = Node(n.val)
        visited[n] = copy
        for nei in n.neighbors:
            copy.neighbors.append(dfs(nei))
        return copy
    return dfs(node)
```
**Time:** O(n+e) | **Space:** O(n)

---

## Problem 17: Number of Operations to Make Network Connected

**Statement:** Given n computers and cables, find min operations to connect all. One operation = remove a cable and connect to another.

**Approach:** Need (components-1) cables to connect. Count extra cables and components.

```python
def makeConnected(n, connections):
    if len(connections) < n - 1: return -1
    class UF:
        def __init__(self,n): self.p=list(range(n)); self.r=[0]*n; self.c=n
        def find(self,x):
            if self.p[x]!=x: self.p[x]=self.find(self.p[x])
            return self.p[x]
        def union(self,x,y):
            px,py=self.find(x),self.find(y)
            if px==py: return False
            if self.r[px]<self.r[py]: px,py=py,px
            self.p[py]=px
            if self.r[px]==self.r[py]: self.r[px]+=1
            self.c-=1
            return True
    uf = UF(n)
    for u,v in connections:
        uf.union(u,v)
    return uf.c - 1
```
**Time:** O(e*α(n)) | **Space:** O(n)

---

## Problem 18: Find the City With Smallest Number of Neighbors

**Statement:** Find city with smallest number of cities reachable within threshold distance. Tie-break: larger city number.

**Approach:** Floyd-Warshall or Dijkstra from each city.

```python
def findTheCity(n, edges, distanceThreshold):
    dist = [[float('inf')]*n for _ in range(n)]
    for i in range(n): dist[i][i] = 0
    for u,v,w in edges:
        dist[u][v] = dist[v][u] = w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k]+dist[k][j])
    min_reachable = n
    result = -1
    for i in range(n):
        count = sum(1 for j in range(n) if dist[i][j] <= distanceThreshold)
        if count <= min_reachable:
            min_reachable = count
            result = i
    return result
```
**Time:** O(n^3) | **Space:** O(n^2)

---

## Problem 19: Keys and Rooms (BFS)

```python
def canVisitAllRooms(rooms):
    from collections import deque
    visited = {0}
    queue = deque([0])
    while queue:
        room = queue.popleft()
        for key in rooms[room]:
            if key not in visited:
                visited.add(key)
                queue.append(key)
    return len(visited) == len(rooms)
```
**Time:** O(n+e) | **Space:** O(n)

---

## Problem 20: Shortest Path in Binary Matrix

**Statement:** Find shortest path from top-left to bottom-right in binary grid (8 directions). Return length or -1.

**Approach:** BFS on grid (unweighted, BFS gives shortest path).

```python
def shortestPathBinaryMatrix(grid):
    from collections import deque
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1: return -1
    queue = deque([(0, 0, 1)])
    grid[0][0] = 1
    dirs = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    while queue:
        x, y, d = queue.popleft()
        if x == n-1 and y == n-1: return d
        for dx,dy in dirs:
            nx,ny = x+dx, y+dy
            if 0<=nx<n and 0<=ny<n and grid[nx][ny]==0:
                grid[nx][ny] = 1
                queue.append((nx,ny,d+1))
    return -1
```
**Time:** O(n^2) | **Space:** O(n^2)

---

## Problem 21: Number of Islands

**Statement:** Count islands in 2D grid ('1' land, '0' water).

**Approach:** DFS/BFS to mark connected land.

```python
def numIslands(grid):
    if not grid: return 0
    count = 0
    m, n = len(grid), len(grid[0])
    def dfs(i, j):
        if i<0 or i>=m or j<0 or j>=n or grid[i][j]!='1': return
        grid[i][j] = '0'
        dfs(i+1,j); dfs(i-1,j); dfs(i,j+1); dfs(i,j-1)
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                dfs(i, j)
                count += 1
    return count
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Problem 22: Flood Fill

**Statement:** Replace all connected pixels of same color with new color.

**Approach:** DFS from starting pixel.

```python
def floodFill(image, sr, sc, newColor):
    m, n = len(image), len(image[0])
    old = image[sr][sc]
    if old == newColor: return image
    def dfs(i, j):
        if i<0 or i>=m or j<0 or j>=n or image[i][j]!=old: return
        image[i][j] = newColor
        dfs(i+1,j); dfs(i-1,j); dfs(i,j+1); dfs(i,j-1)
    dfs(sr, sc)
    return image
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Problem 23: Rotting Oranges

**Statement:** Find minutes until all fresh oranges rot. Each minute, adjacent fresh oranges rot.

**Approach:** Multi-source BFS from all rotten oranges.

```python
def orangesRotting(grid):
    from collections import deque
    m, n = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 2: queue.append((i,j))
            elif grid[i][j] == 1: fresh += 1
    if fresh == 0: return 0
    minutes = 0
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    while queue:
        minutes += 1
        for _ in range(len(queue)):
            x,y = queue.popleft()
            for dx,dy in dirs:
                nx,ny = x+dx, y+dy
                if 0<=nx<m and 0<=ny<n and grid[nx][ny]==1:
                    grid[nx][ny] = 2
                    fresh -= 1
                    queue.append((nx,ny))
    return minutes-1 if fresh==0 else -1
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Problem 24: Pacific Atlantic Water Flow

**Statement:** Find cells where water can flow to both Pacific (top/left) and Atlantic (bottom/right) oceans.

**Approach:** Reverse DFS from both oceans, find intersection.

```python
def pacificAtlantic(grid):
    if not grid: return []
    m, n = len(grid), len(grid[0])
    pacific = set()
    atlantic = set()
    def dfs(i, j, prev, visited):
        if i<0 or i>=m or j<0 or j>=n or (i,j) in visited or grid[i][j]<prev: return
        visited.add((i,j))
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            dfs(i+dx,j+dy,grid[i][j],visited)
    for i in range(m):
        dfs(i,0,0,pacific); dfs(i,n-1,0,atlantic)
    for j in range(n):
        dfs(0,j,0,pacific); dfs(m-1,j,0,atlantic)
    return list(pacific & atlantic)
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Problem 25: Walls and Gates

**Statement:** Fill each empty room with distance to nearest gate. Empty = INF, Gate = 0, Wall = -1.

**Approach:** Multi-source BFS from all gates.

```python
def wallsAndGates(rooms):
    from collections import deque
    m, n = len(rooms), len(rooms[0])
    queue = deque()
    for i in range(m):
        for j in range(n):
            if rooms[i][j] == 0: queue.append((i,j))
    while queue:
        x,y = queue.popleft()
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx,ny = x+dx, y+dy
            if 0<=nx<m and 0<=ny<n and rooms[nx][ny]==2147483647:
                rooms[nx][ny] = rooms[x][y]+1
                queue.append((nx,ny))
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Problem 26: Redundant Connection

**Statement:** Find edge that creates cycle when added to tree.

**Approach:** Union-Find. Edge where both nodes already connected is the answer.

```python
def findRedundantConnection(edges):
    class UF:
        def __init__(self,n): self.p=list(range(n+1))
        def find(self,x):
            if self.p[x]!=x: self.p[x]=self.find(self.p[x])
            return self.p[x]
        def union(self,x,y):
            px,py=self.find(x),self.find(y)
            if px==py: return False
            self.p[py]=px; return True
    uf = UF(len(edges))
    for u,v in edges:
        if not uf.union(u,v):
            return [u,v]
```
**Time:** O(e*α(n)) | **Space:** O(n)

---

## Problem 27: Accounts Merge

**Statement:** Merge accounts that share common emails.

**Approach:** Union-Find on email indices. Group emails by owner.

```python
def accountsMerge(accounts):
    from collections import defaultdict
    email_to_id = {}
    email_to_name = {}
    id_counter = 0
    for account in accounts:
        name = account[0]
        for email in account[1:]:
            email_to_name[email] = name
            if email not in email_to_id:
                email_to_id[email] = id_counter
                id_counter += 1
    class UF:
        def __init__(self,n): self.p=list(range(n))
        def find(self,x):
            if self.p[x]!=x: self.p[x]=self.find(self.p[x])
            return self.p[x]
        def union(self,x,y):
            px,py=self.find(x),self.find(y)
            if px!=py: self.p[py]=px
    uf = UF(id_counter)
    for account in accounts:
        first = email_to_id[account[1]]
        for email in account[2:]:
            uf.union(first, email_to_id[email])
    groups = defaultdict(set)
    for email, eid in email_to_id.items():
        groups[uf.find(eid)].add(email)
    return [[email_to_name[next(iter(emails))]] + sorted(emails) for emails in groups.values()]
```
**Time:** O(n*k*log(n*k)) | **Space:** O(n*k)

---

## Problem 28: Course Schedule

**Statement:** Can you finish all courses? (Cycle detection in directed graph)

**Approach:** DFS with state array (0=unvisited, 1=visiting, 2=visited).

```python
def canFinish(numCourses, prerequisites):
    from collections import defaultdict
    graph = defaultdict(list)
    for u,v in prerequisites: graph[v].append(u)
    state = [0] * numCourses
    def dfs(node):
        state[node] = 1
        for nei in graph[node]:
            if state[nei] == 1: return False
            if state[nei] == 0 and not dfs(nei): return False
        state[node] = 2
        return True
    return all(dfs(i) for i in range(numCourses) if state[i]==0)
```
**Time:** O(n+e) | **Space:** O(n+e)

---

## Problem 29: Course Schedule II

**Statement:** Return ordering to finish all courses. Return empty if impossible.

**Approach:** Topological sort using DFS or Kahn's.

```python
def findOrder(numCourses, prerequisites):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    indeg = [0]*numCourses
    for u,v in prerequisites:
        graph[v].append(u); indeg[u]+=1
    queue = deque([i for i in range(numCourses) if indeg[i]==0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nei in graph[node]:
            indeg[nei]-=1
            if indeg[nei]==0: queue.append(nei)
    return order if len(order)==numCourses else []
```
**Time:** O(n+e) | **Space:** O(n+e)

---

## Problem 30: Network Delay Time

**Statement:** Time for signal from source to reach all nodes.

**Approach:** Dijkstra's shortest path, return max distance.

```python
def networkDelayTime(times, n, k):
    import heapq
    from collections import defaultdict
    graph = defaultdict(list)
    for u,v,w in times: graph[u].append((v,w))
    dist = {k: 0}
    heap = [(0, k)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist.get(node, float('inf')): continue
        for nei, w in graph[node]:
            nd = d + w
            if nd < dist.get(nei, float('inf')):
                dist[nei] = nd
                heapq.heappush(heap, (nd, nei))
    return max(dist.values()) if len(dist)==n else -1
```
**Time:** O(e*log(e)) | **Space:** O(n+e)

---

## Problem 31: Cheapest Flights Within K Stops

**Statement:** Find cheapest price from src to dst with at most k stops.

**Approach:** Bellman-Ford variant or BFS with stops tracking.

```python
def findCheapestPrice(n, flights, src, dst, k):
    prices = [float('inf')] * n
    prices[src] = 0
    for _ in range(k + 1):
        temp = prices[:]
        for u, v, w in flights:
            if prices[u] + w < temp[v]:
                temp[v] = prices[u] + w
        prices = temp
    return prices[dst] if prices[dst] != float('inf') else -1
```
**Time:** O(k*e) | **Space:** O(n)

---

## Problem 32: Alien Dictionary

**Statement:** Derive character order from sorted list of words.

**Approach:** Build graph from adjacent character comparisons, topological sort.

```python
def alienOrder(words):
    from collections import defaultdict, deque
    graph = defaultdict(set)
    indeg = {c:0 for word in words for c in word}
    for i in range(len(words)-1):
        w1, w2 = words[i], words[i+1]
        if len(w1) > len(w2) and w1.startswith(w2):
            return ""
        for c1, c2 in zip(w1, w2):
            if c1 != c2 and c2 not in graph[c1]:
                graph[c1].add(c2)
                indeg[c2] += 1
    queue = deque([c for c in indeg if indeg[c]==0])
    result = []
    while queue:
        c = queue.popleft()
        result.append(c)
        for nei in graph[c]:
            indeg[nei] -= 1
            if indeg[nei] == 0:
                queue.append(nei)
    return "".join(result) if len(result)==len(indeg) else ""
```
**Time:** O(n*m) | **Space:** O(1) limited by alphabet

---

## Problem 33: Swim in Rising Water

**Statement:** Find minimum time to swim from (0,0) to (n-1,n-1). Grid[i][j] = elevation, time = max elevation along path.

**Approach:** Binary search + BFS/DFS, or Dijkstra.

```python
def swimInWater(grid):
    import heapq
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]
    visited = {(0,0)}
    while heap:
        t, x, y = heapq.heappop(heap)
        if x==n-1 and y==n-1: return t
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx,ny = x+dx, y+dy
            if 0<=nx<n and 0<=ny<n and (nx,ny) not in visited:
                visited.add((nx,ny))
                heapq.heappush(heap, (max(t,grid[nx][ny]),nx,ny))
    return -1
```
**Time:** O(n^2*log(n^2)) | **Space:** O(n^2)

---

## Problem 34: Path with Maximum Probability

**Statement:** Find path from start to end with maximum success probability.

**Approach:** Modified Dijkstra (maximize instead of minimize).

```python
def maxProbability(n, edges, succProb, start, end):
    import heapq
    from collections import defaultdict
    graph = defaultdict(list)
    for i in range(len(edges)):
        u,v = edges[i]
        graph[u].append((v,succProb[i]))
        graph[v].append((u,succProb[i]))
    dist = {start: 1.0}
    heap = [(-1.0, start)]
    while heap:
        d, node = heapq.heappop(heap)
        d = -d
        if node == end: return d
        if d < dist.get(node, 0): continue
        for nei, prob in graph[node]:
            nd = d * prob
            if nd > dist.get(nei, 0):
                dist[nei] = nd
                heapq.heappush(heap, (-nd, nei))
    return 0.0
```
**Time:** O(e*log(n)) | **Space:** O(n+e)

---

## Problem 35: Parallel Courses III

**Statement:** Find minimum time to complete all courses with prerequisites and durations.

**Approach:** Topological sort + DP (max time to reach each course).

```python
def minimumTime(n, relations, time):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    indeg = [0]*n
    for u,v in relations:
        graph[u-1].append(v-1); indeg[v-1]+=1
    dp = [0]*n
    queue = deque()
    for i in range(n):
        if indeg[i]==0:
            queue.append(i)
            dp[i] = time[i]
    while queue:
        node = queue.popleft()
        for nei in graph[node]:
            dp[nei] = max(dp[nei], dp[node]+time[nei])
            indeg[nei]-=1
            if indeg[nei]==0: queue.append(nei)
    return max(dp)
```
**Time:** O(n+e) | **Space:** O(n+e)

---

## Problem 36: Longest Path in DAG

**Statement:** Find longest path in directed acyclic graph.

**Approach:** Topological sort + DP.

```python
def longestPath(n, edges):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    indeg = [0]*n
    for u,v in edges:
        graph[u].append(v); indeg[v]+=1
    dp = [0]*n
    queue = deque([i for i in range(n) if indeg[i]==0])
    while queue:
        node = queue.popleft()
        for nei in graph[node]:
            dp[nei] = max(dp[nei], dp[node]+1)
            indeg[nei]-=1
            if indeg[nei]==0: queue.append(nei)
    return max(dp)
```
**Time:** O(n+e) | **Space:** O(n+e)

---

## Problem 37: Minimum Height Trees

**Statement:** Find root nodes that give minimum height tree.

**Approach:** Strip leaves iteratively until 1-2 nodes remain.

```python
def findMinHeightTrees(n, edges):
    if n == 1: return [0]
    from collections import defaultdict, deque
    graph = defaultdict(set)
    for u,v in edges:
        graph[u].add(v); graph[v].add(u)
    leaves = [i for i in range(n) if len(graph[i])==1]
    remaining = n
    while remaining > 2:
        remaining -= len(leaves)
        new_leaves = []
        for leaf in leaves:
            nei = graph[leaf].pop()
            graph[nei].discard(leaf)
            if len(graph[nei])==1: new_leaves.append(nei)
        leaves = new_leaves
    return leaves
```
**Time:** O(n) | **Space:** O(n)

---

## Problem 38: Find the Safest Path in a Grid

**Statement:** Find safest path where minimum distance to thief is maximized.

**Approach:** Multi-source BFS for distances, then binary search + BFS.

```python
def maximumSafenessFactor(grid):
    from collections import deque
    n = len(grid)
    if grid[0][0]==1 or grid[n-1][n-1]==1: return 0
    dist = [[-1]*n for _ in range(n)]
    queue = deque()
    for i in range(n):
        for j in range(n):
            if grid[i][j]==1: queue.append((i,j)); dist[i][j]=0
    while queue:
        x,y = queue.popleft()
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx,ny=x+dx,y+dy
            if 0<=nx<n and 0<=ny<n and dist[nx][ny]==-1:
                dist[nx][ny]=dist[x][y]+1
                queue.append((nx,ny))
    import heapq
    heap = [(-dist[0][0],0,0)]
    visited = {(0,0)}
    while heap:
        d,x,y = heapq.heappop(heap)
        if x==n-1 and y==n-1: return -d
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx,ny=x+dx,y+dy
            if 0<=nx<n and 0<=ny<n and (nx,ny) not in visited:
                visited.add((nx,ny))
                heapq.heappush(heap, (min(d,-dist[nx][ny]),nx,ny))
    return 0
```
**Time:** O(n^2*log(n^2)) | **Space:** O(n^2)

---

## Problem 39: All Paths from Source to Target (BFS)

```python
def allPathsSourceTarget(graph):
    from collections import deque
    n = len(graph)
    result = []
    queue = deque([(0, [0])])
    while queue:
        node, path = queue.popleft()
        if node == n-1:
            result.append(path)
            continue
        for nei in graph[node]:
            queue.append((nei, path+[nei]))
    return result
```
**Time:** O(2^n) | **Space:** O(2^n)

---

## Problem 40: Reconstruct Itinerary

**Statement:** Given tickets, find itinerary starting from JFK (smallest lexical order).

**Approach:** DFS with stack, remove edges as used.

```python
def findItinerary(tickets):
    from collections import defaultdict
    graph = defaultdict(list)
    for u,v in sorted(tickets, reverse=True):
        graph[u].append(v)
    result = []
    def dfs(airport):
        while graph[airport]:
            dfs(graph[airport].pop())
        result.append(airport)
    dfs("JFK")
    return result[::-1]
```
**Time:** O(e*log(e)) | **Space:** O(n+e)

---

