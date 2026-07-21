# Shortest Path Problems

## Network Delay Time

```python
import heapq
from collections import defaultdict

def network_delay_time(times, n, k):
    """
    LeetCode 743 - Time for all nodes to receive signal
    Find max distance in shortest path tree from k
    Time: O(E log V) | Space: O(V + E)
    """
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


# Example
times = [[2,1,1],[2,3,1],[3,4,1]]
print(network_delay_time(times, 4, 2))  # 2
```

## Cheapest Flights Within K Stops

```python
import heapq
from collections import defaultdict

def find_cheapest_price(n, flights, src, dst, k):
    """
    LeetCode 787 - Cheapest price with at most K stops
    Modified Dijkstra / Bellman-Ford
    Time: O(E * K) | Space: O(N)
    """
    # Bellman-Ford approach
    prices = [float('inf')] * n
    prices[src] = 0
    
    for _ in range(k + 1):
        temp = prices[:]
        for u, v, cost in flights:
            if prices[u] + cost < temp[v]:
                temp[v] = prices[u] + cost
        prices = temp
    
    return prices[dst] if prices[dst] != float('inf') else -1


# Dijkstra with stops tracking
def find_cheapest_price_dijkstra(n, flights, src, dst, k):
    graph = defaultdict(list)
    for u, v, cost in flights:
        graph[u].append((v, cost))
    
    # (cost, node, stops)
    heap = [(0, src, 0)]
    visited = {}  # node -> min stops to reach
    
    while heap:
        cost, node, stops = heapq.heappop(heap)
        
        if node == dst:
            return cost
        
        if node in visited and visited[node] <= stops:
            continue
        
        visited[node] = stops
        
        if stops <= k:
            for neighbor, price in graph[node]:
                heapq.heappush(heap, (cost + price, neighbor, stops + 1))
    
    return -1


# Example
flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
print(find_cheapest_price(4, flights, 0, 3, 1))  # 700
print(find_cheapest_price_dijkstra(4, flights, 0, 3, 1))  # 700
```

## Swim in Rising Water

```python
import heapq

def swim_in_rising_water(grid):
    """
    LeetCode 778 - Find min time to reach bottom-right
    Time: O(N² log N) | Space: O(N²)
    """
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]
    visited = set([(0, 0)])
    max_time = 0
    
    while heap:
        time, r, c = heapq.heappop(heap)
        max_time = max(max_time, time)
        
        if r == n - 1 and c == n - 1:
            return max_time
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < n and 0 <= nc < n and 
                (nr, nc) not in visited):
                visited.add((nr, nc))
                heapq.heappush(heap, (grid[nr][nc], nr, nc))
    
    return -1


# Binary search + BFS approach
def swim_in_rising_water_bfs(grid):
    n = len(grid)
    
    def can_reach(time):
        if grid[0][0] > time:
            return False
        visited = set([(0, 0)])
        queue = [(0, 0)]
        
        for r, c in queue:
            if r == n - 1 and c == n - 1:
                return True
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < n and 0 <= nc < n and
                    (nr, nc) not in visited and grid[nr][nc] <= time):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        
        return False
    
    lo, hi = 0, n * n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if can_reach(mid):
            hi = mid
        else:
            lo = mid + 1
    
    return lo


# Example
grid = [[0,2],[1,3]]
print(swim_in_rising_water(grid))  # 3
```

## Path with Maximum Probability

```python
import heapq
from collections import defaultdict

def max_probability(n, edges, succProb, start, end):
    """
    LeetCode 1514 - Path with maximum probability
    Modified Dijkstra (maximize instead of minimize)
    Time: O(E log V) | Space: O(V + E)
    """
    graph = defaultdict(list)
    for i, (u, v) in enumerate(edges):
        graph[u].append((v, succProb[i]))
        graph[v].append((u, succProb[i]))
    
    # Max heap (negate probability for min heap)
    heap = [(-1, start)]
    visited = set()
    
    while heap:
        prob, node = heapq.heappop(heap)
        prob = -prob
        
        if node == end:
            return prob
        
        if node in visited:
            continue
        visited.add(node)
        
        for neighbor, p in graph[node]:
            if neighbor not in visited:
                heapq.heappush(heap, (-(prob * p), neighbor))
    
    return 0.0


# Example
n = 3
edges = [[0,1],[1,2],[0,2]]
succProb = [0.5, 0.5, 0.2]
print(max_probability(n, edges, succProb, 0, 2))  # 0.25
```

## Shortest Path in Binary Matrix

```python
from collections import deque

def shortest_path_binary_matrix(grid):
    """
    LeetCode 1091 - Shortest path in binary matrix
    BFS with 8-directional movement
    Time: O(N²) | Space: O(N²)
    """
    if grid[0][0] == 1 or grid[-1][-1] == 1:
        return -1
    
    n = len(grid)
    queue = deque([(0, 0, 1)])
    visited = set([(0, 0)])
    
    while queue:
        r, c, dist = queue.popleft()
        
        if r == n - 1 and c == n - 1:
            return dist
        
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if (0 <= nr < n and 0 <= nc < n and
                    grid[nr][nc] == 0 and (nr, nc) not in visited):
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))
    
    return -1


# Example
grid = [[0,0,0],[1,1,0],[1,1,0]]
print(shortest_path_binary_matrix(grid))  # 4
```

## Path with Minimum Effort

```python
import heapq

def minimum_effort_path(heights):
    """
    LeetCode 1631 - Minimize max absolute difference along path
    Dijkstra where edge weight = max effort so far
    Time: O(M * N * log(M * N)) | Space: O(M * N)
    """
    rows, cols = len(heights), len(heights[0])
    
    # (effort, row, col)
    heap = [(0, 0, 0)]
    visited = set()
    max_effort = [[float('inf')] * cols for _ in range(rows)]
    max_effort[0][0] = 0
    
    while heap:
        effort, r, c = heapq.heappop(heap)
        
        if r == rows - 1 and c == cols - 1:
            return effort
        
        if (r, c) in visited:
            continue
        visited.add((r, c))
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_effort = max(effort, abs(heights[nr][nc] - heights[r][c]))
                if new_effort < max_effort[nr][nc]:
                    max_effort[nr][nc] = new_effort
                    heapq.heappush(heap, (new_effort, nr, nc))
    
    return -1


# Binary search + BFS approach
def minimum_effort_path_binary_search(heights):
    rows, cols = len(heights), len(heights[0])
    
    def can_reach(max_effort):
        visited = set([(0, 0)])
        queue = [(0, 0)]
        
        for r, c in queue:
            if r == rows - 1 and c == cols - 1:
                return True
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and
                    (nr, nc) not in visited and
                    abs(heights[nr][nc] - heights[r][c]) <= max_effort):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        
        return False
    
    lo, hi = 0, 10**6
    while lo < hi:
        mid = (lo + hi) // 2
        if can_reach(mid):
            hi = mid
        else:
            lo = mid + 1
    
    return lo


# Example
heights = [[1,2,2],[3,8,2],[5,3,5]]
print(minimum_effort_path(heights))  # 2
```

## Key Patterns

```
1. Grid shortest path with uniform weights → BFS
2. Grid shortest path with varying weights → Dijkstra on grid
3. Single source, non-negative weights → Dijkstra
4. Need to find min/max along path → Modified Dijkstra
5. Constraints on path (K stops) → Modified Dijkstra or Bellman-Ford
6. Binary search on answer → Check feasibility with BFS/DFS
7. Swim in Rising Water → Dijkstra or Binary Search + BFS
8. Min effort → Dijkstra maximizing the minimum edge
```
