# Graph Practice Problems (20 Problems)

## Easy Problems

### 1. Number of Islands
```python
def num_islands(grid):
    """LeetCode 200 - Count connected components of '1's"""
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] != '1'):
            return
        grid[r][c] = '0'
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

# Time: O(M * N) | Space: O(M * N) - recursion stack
# Approach: DFS/BFS to mark visited cells, count components
```

### 2. Flood Fill
```python
def flood_fill(image, sr, sc, newColor):
    """LeetCode 733 - Fill connected region with new color"""
    rows, cols = len(image), len(image[0])
    oldColor = image[sr][sc]
    
    if oldColor == newColor:
        return image
    
    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            image[r][c] != oldColor):
            return
        
        image[r][c] = newColor
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    dfs(sr, sc)
    return image

# Time: O(M * N) | Space: O(M * N)
# Approach: DFS from seed pixel, change matching neighbors
```

### 3. Valid Tree
```python
def valid_tree(n, edges):
    """LeetCode 261 - Check if graph is a valid tree"""
    if len(edges) != n - 1:
        return False
    
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        parent[px] = py
        return True
    
    for u, v in edges:
        if not union(u, v):
            return False
    
    return True

# Time: O(V + E * α(V)) | Space: O(V)
# Approach: Tree has V-1 edges and no cycles
```

### 4. Find Center of Star Graph
```python
def findCenter(edges):
    """LeetCode 1791 - Find center node of star graph"""
    return edges[0][0] if edges[0][0] in edges[1] else edges[0][1]

# Time: O(1) | Space: O(1)
# Approach: Center appears in all edges
```

## Medium Problems

### 5. Course Schedule
```python
def can_finish(numCourses, prerequisites):
    """LeetCode 207 - Check if all courses can be finished"""
    from collections import defaultdict, deque
    
    graph = defaultdict(list)
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    count = 0
    
    while queue:
        node = queue.popleft()
        count += 1
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return count == numCourses

# Time: O(V + E) | Space: O(V + E)
# Approach: Kahn's algorithm, check if all nodes processed
```

### 6. Pacific Atlantic Water Flow
```python
def pacific_atlantic(heights):
    """LeetCode 417 - Find cells reachable by both oceans"""
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
    
    for r in range(rows):
        dfs(r, 0, pacific, 0)
        dfs(r, cols - 1, atlantic, 0)
    for c in range(cols):
        dfs(0, c, pacific, 0)
        dfs(rows - 1, c, atlantic, 0)
    
    return list(pacific & atlantic)

# Time: O(M * N) | Space: O(M * N)
# Approach: DFS from ocean borders, find intersection
```

### 7. Rotting Oranges
```python
from collections import deque

def oranges_rotting(grid):
    """LeetCode 994 - Find minutes to rot all oranges"""
    if not grid or not grid[0]:
        return 0
    
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
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        minutes += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and 
                    grid[nr][nc] == 1):
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        
        if fresh == 0:
            return minutes
    
    return -1

# Time: O(M * N) | Space: O(M * N)
# Approach: Multi-source BFS from all rotten oranges
```

### 8. Clone Graph
```python
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors else []

def cloneGraph(node):
    """LeetCode 133 - Deep copy of graph"""
    if not node:
        return None
    
    cloned = {node: Node(node.val)}
    stack = [node]
    
    while stack:
        curr = stack.pop()
        for neighbor in curr.neighbors:
            if neighbor not in cloned:
                cloned[neighbor] = Node(neighbor.val)
                stack.append(neighbor)
            cloned[curr].neighbors.append(cloned[neighbor])
    
    return cloned[node]

# Time: O(V + E) | Space: O(V)
# Approach: BFS/DFS with hash map for cloned nodes
```

### 9. Word Ladder
```python
from collections import deque

def ladder_length(beginWord, endWord, wordList):
    """LeetCode 127 - Shortest transformation sequence"""
    word_set = set(wordList)
    if endWord not in word_set:
        return 0
    
    queue = deque([(beginWord, 1)])
    visited = set([beginWord])
    
    while queue:
        word, length = queue.popleft()
        
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]
                
                if new_word == endWord:
                    return length + 1
                
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, length + 1))
    
    return 0

# Time: O(M² * N) | Space: O(M² * N)
# Approach: BFS on implicit word graph
```

### 10. Graph Valid Tree
```python
def valid_tree(n, edges):
    """LeetCode 261 - Check if graph is a valid tree (duplicate)"""
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
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return len(visited) == n

# Time: O(V + E) | Space: O(V + E)
# Approach: V-1 edges + connected = valid tree
```

### 11. Number of Provinces
```python
def findCircleNum(isConnected):
    """LeetCode 547 - Count connected components"""
    n = len(isConnected)
    visited = set()
    count = 0
    
    def dfs(node):
        visited.add(node)
        for neighbor in range(n):
            if isConnected[node][neighbor] == 1 and neighbor not in visited:
                dfs(neighbor)
    
    for i in range(n):
        if i not in visited:
            dfs(i)
            count += 1
    
    return count

# Time: O(n²) | Space: O(n)
# Approach: DFS on adjacency matrix
```

### 12. Redundant Connection
```python
def findRedundantConnection(edges):
    """LeetCode 684 - Find edge that creates cycle"""
    n = len(edges)
    parent = list(range(n + 1))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        parent[px] = py
        return True
    
    for u, v in edges:
        if not union(u, v):
            return [u, v]
    
    return []

# Time: O(E * α(V)) | Space: O(V)
# Approach: Union-Find, detect cycle edge
```

### 13. Max Area of Island
```python
def maxAreaOfIsland(grid):
    """LeetCode 695 - Find largest island area"""
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    max_area = 0
    
    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] != 1):
            return 0
        grid[r][c] = 0
        return 1 + dfs(r+1, c) + dfs(r-1, c) + dfs(r, c+1) + dfs(r, c-1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                max_area = max(max_area, dfs(r, c))
    
    return max_area

# Time: O(M * N) | Space: O(M * N)
# Approach: DFS, return area of each component
```

### 14. Surrounded Regions
```python
def solve(board):
    """LeetCode 130 - Flip surrounded 'O's to 'X's"""
    if not board or not board[0]:
        return
    
    rows, cols = len(board), len(board[0])
    
    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            board[r][c] != 'O'):
            return
        board[r][c] = 'S'
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)
    
    for r in range(rows):
        dfs(r, 0)
        dfs(r, cols - 1)
    for c in range(cols):
        dfs(0, c)
        dfs(rows - 1, c)
    
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == 'S':
                board[r][c] = 'O'

# Time: O(M * N) | Space: O(M * N)
# Approach: DFS from borders, mark safe, flip rest
```

## Hard Problems

### 15. Network Delay Time
```python
import heapq
from collections import defaultdict

def networkDelayTime(times, n, k):
    """LeetCode 743 - Find time for all nodes to receive signal"""
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    
    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[k] = 0
    heap = [(0, k)]
    
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for neighbor, weight in graph[node]:
            new_dist = dist[node] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    
    max_dist = max(dist.values())
    return max_dist if max_dist < float('inf') else -1

# Time: O(E log V) | Space: O(V + E)
# Approach: Dijkstra from source, return max distance
```

### 16. Alien Dictionary
```python
def alienDictionary(words):
    """LeetCode 269 - Find character ordering"""
    from collections import defaultdict, deque
    
    graph = defaultdict(set)
    in_degree = {c: 0 for word in words for c in word}
    
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
        
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in graph[w1[j]]:
                    graph[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break
    
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

# Time: O(C) | Space: O(1)
# Approach: Build graph from word comparisons, Kahn's sort
```

### 17. Longest Path in DAG
```python
from collections import defaultdict, deque

def longestPath(n, edges):
    """Find longest path length in DAG"""
    graph = defaultdict(list)
    in_degree = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    dist = [0] * n
    for node in topo_order:
        for neighbor in graph[node]:
            dist[neighbor] = max(dist[neighbor], dist[node] + 1)
    
    return max(dist)

# Time: O(V + E) | Space: O(V + E)
# Approach: Topological sort + DP
```

### 18. Swim in Rising Water
```python
import heapq

def swimInRisingWater(grid):
    """LeetCode 778 - Min time to reach bottom-right"""
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]
    visited = set([(0, 0)])
    
    while heap:
        time, r, c = heapq.heappop(heap)
        
        if r == n - 1 and c == n - 1:
            return time
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < n and 0 <= nc < n and 
                (nr, nc) not in visited):
                visited.add((nr, nc))
                heapq.heappush(heap, (grid[nr][nc], nr, nc))
    
    return -1

# Time: O(N² log N) | Space: O(N²)
# Approach: Dijkstra on grid
```

### 19. Critical Connections
```python
from collections import defaultdict

def criticalConnections(n, connections):
    """LeetCode 1192 - Find all bridges in graph"""
    graph = defaultdict(list)
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)
    
    disc = [0] * n
    low = [0] * n
    parent = [-1] * n
    bridges = []
    timer = [0]
    
    def dfs(node):
        disc[node] = low[node] = timer[0]
        timer[0] += 1
        
        for neighbor in graph[node]:
            if disc[neighbor] == 0:
                parent[neighbor] = node
                dfs(neighbor)
                low[node] = min(low[node], low[neighbor])
                if low[neighbor] > disc[node]:
                    bridges.append([node, neighbor])
            elif neighbor != parent[node]:
                low[node] = min(low[node], disc[neighbor])
    
    dfs(0)
    return bridges

# Time: O(V + E) | Space: O(V + E)
# Approach: DFS to find bridges using disc/low values
```

### 20. Accounts Merge
```python
from collections import defaultdict

def accountsMerge(accounts):
    """LeetCode 721 - Merge accounts with common emails"""
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
    
    parent = list(range(id_counter))
    rank = [0] * id_counter
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
    
    for account in accounts:
        first_id = email_to_id[account[1]]
        for email in account[2:]:
            union(first_id, email_to_id[email])
    
    groups = defaultdict(list)
    for email, eid in email_to_id.items():
        root = find(eid)
        groups[root].append(email)
    
    result = []
    for emails in groups.values():
        name = email_to_name[emails[0]]
        result.append([name] + sorted(emails))
    
    return result

# Time: O(N * K * α(N*K)) | Space: O(N * K)
# Approach: Union-Find on email IDs, group by root
```

## Problem Categories Summary

```
EASY (4):
1. Number of Islands - DFS/BFS on grid
2. Flood Fill - DFS/BFS coloring
3. Valid Tree - Union-Find
4. Find Center - Star graph property

MEDIUM (10):
5. Course Schedule - Topological sort
6. Pacific Atlantic - DFS from borders
7. Rotting Oranges - Multi-source BFS
8. Clone Graph - BFS/DFS with map
9. Word Ladder - BFS on word graph
10. Graph Valid Tree - Union-Find
11. Number of Provinces - DFS
12. Redundant Connection - Union-Find
13. Max Area of Island - DFS returning area
14. Surrounded Regions - DFS from borders

HARD (6):
15. Network Delay Time - Dijkstra
16. Alien Dictionary - Topological sort
17. Longest Path in DAG - Topo sort + DP
18. Swim in Rising Water - Dijkstra on grid
19. Critical Connections - Bridge finding
20. Accounts Merge - Union-Find
```
