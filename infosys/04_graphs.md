# Graphs

## Problem 1: BFS - Shortest Path in Unweighted Graph
**Difficulty: Easy-Medium | Marks: 20-30**

```python
from collections import deque

def bfs_shortest_path(graph, start, goal):
    visited = {start}
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return []

graph = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 5],
    3: [1],
    4: [1, 5],
    5: [2, 4]
}
print(bfs_shortest_path(graph, 0, 5))
```

---

## Problem 2: DFS - Detect Cycle in Directed Graph
**Difficulty: Medium | Marks: 30**

```python
def has_cycle_directed(graph, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    def dfs(node):
        color[node] = GRAY
        for neighbor in graph.get(node, []):
            if color[neighbor] == GRAY:
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

graph = {0: [1], 1: [2], 2: [0]}
print(has_cycle_directed(graph, 3))
```

---

## Problem 3: Detect Cycle in Undirected Graph (Union-Find)
**Difficulty: Medium | Marks: 30**

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        return True

def has_cycle_undirected(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):
            return True
    return False

n = 5
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
print(has_cycle_undirected(n, edges))
```

---

## Problem 4: Dijkstra's Algorithm - Shortest Path
**Difficulty: Medium | Marks: 30**

```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    heap = [(0, start)]
    while heap:
        curr_dist, node = heapq.heappop(heap)
        if curr_dist > distances[node]:
            continue
        for neighbor, weight in graph[node]:
            dist = curr_dist + weight
            if dist < distances[neighbor]:
                distances[neighbor] = dist
                heapq.heappush(heap, (dist, neighbor))
    return distances

graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 1), ('D', 5)],
    'C': [('D', 8), ('E', 10)],
    'D': [('E', 2)],
    'E': []
}
print(dijkstra(graph, 'A'))
```

---

## Problem 5: Topological Sort
**Difficulty: Medium | Marks: 30**

```python
from collections import defaultdict, deque

def topological_sort(n, prerequisites):
    graph = defaultdict(list)
    indegree = [0] * n
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    queue = deque([i for i in range(n) if indegree[i] == 0])
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return result if len(result) == n else []

n = 4
prereqs = [(1, 0), (2, 0), (3, 1), (3, 2)]
print(topological_sort(n, prereqs))
```

---

## Problem 6: Number of Islands
**Difficulty: Medium | Marks: 30**

```python
def num_islands(grid):
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])
    count = 0
    def dfs(i, j):
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == '0':
            return
        grid[i][j] = '0'
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                count += 1
                dfs(i, j)
    return count

grid = [
    ['1', '1', '0', '0', '0'],
    ['1', '1', '0', '0', '0'],
    ['0', '0', '1', '0', '0'],
    ['0', '0', '0', '1', '1']
]
print(num_islands(grid))
```

---

## Problem 7: Max Area of Island
**Difficulty: Medium | Marks: 30**

```python
def max_area_of_island(grid):
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])
    def dfs(i, j):
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == 0:
            return 0
        grid[i][j] = 0
        return 1 + dfs(i + 1, j) + dfs(i - 1, j) + dfs(i, j + 1) + dfs(i, j - 1)
    max_area = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                max_area = max(max_area, dfs(i, j))
    return max_area

grid = [
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
]
print(max_area_of_island(grid))
```

---

## Problem 8: Rotting Oranges
**Difficulty: Medium | Marks: 30**

```python
from collections import deque

def oranges_rotting(grid):
    m, n = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 2:
                queue.append((i, j, 0))
            elif grid[i][j] == 1:
                fresh += 1
    if fresh == 0:
        return 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    minutes = 0
    while queue:
        i, j, mins = queue.popleft()
        minutes = max(minutes, mins)
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                grid[ni][nj] = 2
                fresh -= 1
                queue.append((ni, nj, mins + 1))
    return minutes if fresh == 0 else -1

grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
print(oranges_rotting(grid))
```

---

## Problem 9: Clone Graph
**Difficulty: Medium | Marks: 30**

```python
def clone_graph(node):
    if not node:
        return None
    cloned = {}
    def dfs(original):
        if original in cloned:
            return cloned[original]
        copy = Node(original.val)
        cloned[original] = copy
        for neighbor in original.neighbors:
            copy.neighbors.append(dfs(neighbor))
        return copy
    return dfs(node)

# Node class for reference
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
```

---

## Problem 10: Course Schedule (Cycle Detection)
**Difficulty: Medium | Marks: 30**

```python
from collections import defaultdict, deque

def can_finish(num_courses, prerequisites):
    graph = defaultdict(list)
    indegree = [0] * num_courses
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    queue = deque([i for i in range(num_courses) if indegree[i] == 0])
    count = 0
    while queue:
        node = queue.popleft()
        count += 1
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return count == num_courses

num = 2
prereqs = [[1, 0]]
print(can_finish(num, prereqs))
```

---

## Problem 11: Word Ladder
**Difficulty: Hard | Marks: 50**

```python
from collections import deque

def ladder_length(begin_word, end_word, word_list):
    word_set = set(word_list)
    if end_word not in word_set:
        return 0
    queue = deque([(begin_word, 1)])
    visited = {begin_word}
    while queue:
        word, length = queue.popleft()
        if word == end_word:
            return length
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i + 1:]
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, length + 1))
    return 0

begin = "hit"
end = "cog"
words = ["hot", "dot", "dog", "lot", "log", "cog"]
print(ladder_length(begin, end, words))
```

---

## Problem 12: Pacific Atlantic Water Flow
**Difficulty: Medium | Marks: 30**

```python
def pacific_atlantic(heights):
    if not heights:
        return []
    m, n = len(heights), len(heights[0])
    pacific = [[False] * n for _ in range(m)]
    atlantic = [[False] * n for _ in range(m)]

    def dfs(i, j, ocean):
        ocean[i][j] = True
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and not ocean[ni][nj] and heights[ni][nj] >= heights[i][j]:
                dfs(ni, nj, ocean)

    for i in range(m):
        dfs(i, 0, pacific)
        dfs(i, n - 1, atlantic)
    for j in range(n):
        dfs(0, j, pacific)
        dfs(m - 1, j, atlantic)

    result = []
    for i in range(m):
        for j in range(n):
            if pacific[i][j] and atlantic[i][j]:
                result.append([i, j])
    return result

heights = [
    [1, 2, 2, 3, 5],
    [3, 2, 3, 4, 4],
    [2, 4, 5, 3, 1],
    [6, 7, 1, 4, 5],
    [5, 1, 1, 2, 4]
]
print(pacific_atlantic(heights))
```

---

## Problem 13: Alien Dictionary
**Difficulty: Hard | Marks: 50**

```python
from collections import defaultdict, deque

def alien_order(words):
    graph = defaultdict(set)
    indegree = {c: 0 for word in words for c in word}
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        if len(w1) > len(w2) and w1[:len(w2)] == w2:
            return ""
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if c2 not in graph[c1]:
                    graph[c1].add(c2)
                    indegree[c2] += 1
                break
    queue = deque([c for c in indegree if indegree[c] == 0])
    result = []
    while queue:
        c = queue.popleft()
        result.append(c)
        for neighbor in graph[c]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return ''.join(result) if len(result) == len(indegree) else ""

words = ["wrt", "wrf", "er", "ett", "rftt"]
print(alien_order(words))
```

---

## Problem 14: Minimum Spanning Tree (Kruskal's)
**Difficulty: Medium | Marks: 30**

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        return True

def kruskal_mst(n, edges):
    edges.sort(key=lambda x: x[2])
    uf = UnionFind(n)
    mst_weight = 0
    mst_edges = []
    for u, v, w in edges:
        if uf.union(u, v):
            mst_weight += w
            mst_edges.append((u, v, w))
    return mst_weight, mst_edges

n = 4
edges = [(0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4)]
print(kruskal_mst(n, edges))
```

---

## Problem 15: Cheapest Flights Within K Stops
**Difficulty: Medium | Marks: 30**

```python
import heapq
from collections import defaultdict

def find_cheapest_price(n, flights, src, dst, k):
    graph = defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))
    heap = [(0, src, 0)]
    best = {}
    while heap:
        cost, city, stops = heapq.heappop(heap)
        if city == dst:
            return cost
        if stops > k:
            continue
        key = (city, stops)
        if key in best and best[key] <= cost:
            continue
        best[key] = cost
        for neighbor, price in graph[city]:
            heapq.heappush(heap, (cost + price, neighbor, stops + 1))
    return -1

n = 4
flights = [[0, 1, 100], [1, 2, 100], [2, 3, 100], [0, 2, 500]]
src, dst, k = 0, 3, 1
print(find_cheapest_price(n, flights, src, dst, k))
```

---

## Problem 16: Minimum Knight Moves
**Difficulty: Medium | Marks: 30**

```python
from collections import deque

def min_knight_moves(x, y):
    x, y = abs(x), abs(y)
    if x == 0 and y == 0:
        return 0
    directions = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                  (-2, -1), (-1, -2), (1, -2), (2, -1)]
    queue = deque([(0, 0, 0)])
    visited = {(0, 0)}
    while queue:
        cx, cy, steps = queue.popleft()
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if nx == x and ny == y:
                return steps + 1
            if (nx, ny) not in visited and nx >= -2 and ny >= -2:
                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1))
    return -1

print(min_knight_moves(2, 1))
print(min_knight_moves(5, 5))
```
