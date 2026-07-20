# Disjoint Set Union (Union-Find) Guide

## What is Disjoint Set Union?

DSU (also called Union-Find) is a data structure that tracks a set of elements partitioned into disjoint (non-overlapping) subsets. It supports two main operations:
1. **Find:** Determine which set an element belongs to
2. **Union:** Merge two sets into one

**When to use:**
- Tracking connected components in a graph
- Detecting cycles in undirected graphs
- Kruskal's Minimum Spanning Tree
- Dynamic connectivity problems
- Accounts merge problems

**Key Properties:**
- Each set is represented by a representative element (root)
- Elements point to their parent until they reach the root
- Path compression and union by rank optimize operations

**Comparison with DFS/BFS:**
| Feature | DSU | DFS/BFS |
|---------|-----|---------|
| Find connected components | O(α(n)) amortized | O(V + E) |
| Dynamic connectivity | O(α(n)) | O(V + E) |
| Space | O(V) | O(V + E) |
| Implementation complexity | Simple | Moderate |

Where α is the inverse Ackermann function (practically constant)

---

## 1. Basic DSU Implementation

```python
class DSU:
    def __init__(self, n):
        """Initialize n elements, each in its own set"""
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
    
    def find(self, x):
        """Find representative of set containing x"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        """Union sets containing x and y"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same set
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return True
    
    def connected(self, x, y):
        """Check if x and y are in same set"""
        return self.find(x) == self.find(y)
    
    def get_components(self):
        """Get all connected components"""
        components = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in components:
                components[root] = []
            components[root].append(i)
        return list(components.values())
    
    def count_components(self):
        """Count number of connected components"""
        return len(set(self.find(i) for i in range(len(self.parent))))

# Test
dsu = DSU(7)
dsu.union(0, 1)
dsu.union(1, 2)
dsu.union(3, 4)
dsu.union(5, 6)
dsu.union(4, 5)

print(f"Components: {dsu.get_components()}")  # [[0, 1, 2], [3, 4, 5, 6]]
print(f"Count: {dsu.count_components()}")  # 2
print(f"0 and 2 connected: {dsu.connected(0, 2)}")  # True
print(f"0 and 3 connected: {dsu.connected(0, 3)}")  # False
```

**Time Complexity:** O(α(n)) amortized for find and union
**Space Complexity:** O(n)

---

## 2. Union by Size (Alternative to Rank)

```python
class DSUBySize:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        # Union by size: attach smaller tree to larger tree
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        
        return True
    
    def get_size(self, x):
        """Get size of set containing x"""
        return self.size[self.find(x)]

# Test
dsu = DSUBySize(6)
dsu.union(0, 1)
dsu.union(2, 3)
dsu.union(4, 5)
dsu.union(1, 3)

print(f"Size of set containing 0: {dsu.get_size(0)}")  # 4
print(f"Components: {dsu.count_components()}")

def count_components(self):
    return len(set(self.find(i) for i in range(len(self.parent))))
```

---

## 3. Applications

### 3.1 Number of Provinces (LC 547)

```python
def find_circle_num(isConnected):
    """Find number of provinces (connected components)"""
    n = len(isConnected)
    dsu = DSU(n)
    
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j]:
                dsu.union(i, j)
    
    return dsu.count_components()

# Alternative using DFS
def find_circle_num_dfs(isConnected):
    n = len(isConnected)
    visited = [False] * n
    
    def dfs(i):
        visited[i] = True
        for j in range(n):
            if isConnected[i][j] and not visited[j]:
                dfs(j)
    
    count = 0
    for i in range(n):
        if not visited[i]:
            dfs(i)
            count += 1
    
    return count

# Test
isConnected = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
print(f"Provinces (DSU): {find_circle_num(isConnected)}")  # 2
print(f"Provinces (DFS): {find_circle_num_dfs(isConnected)}")  # 2
```

**Time Complexity:** O(n²)
**Space Complexity:** O(n)

---

### 3.2 Redundant Connection (LC 684)

```python
def find_redundant_connection(edges):
    """Find edge that creates a cycle"""
    n = len(edges)
    dsu = DSU(n + 1)  # 1-indexed
    
    for u, v in edges:
        if not dsu.union(u, v):
            return [u, v]
    
    return []

# Alternative: Track when components merge
def find_redundant_connection_v2(edges):
    n = len(edges)
    parent = list(range(n + 1))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    for u, v in edges:
        root_u = find(u)
        root_v = find(v)
        if root_u == root_v:
            return [u, v]
        parent[root_v] = root_u
    
    return []

# Test
edges = [[1, 2], [1, 3], [2, 3]]
print(f"Redundant edge: {find_redundant_connection(edges)}")  # [2, 3]

edges2 = [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]
print(f"Redundant edge: {find_redundant_connection(edges2)}")  # [1, 4]
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

---

### 3.3 Accounts Merge (LC 721)

```python
def accounts_merge(accounts):
    """Merge accounts that have common emails"""
    from collections import defaultdict
    
    n = len(accounts)
    dsu = DSU(n)
    
    # Map email to account index
    email_to_id = {}
    
    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in email_to_id:
                dsu.union(i, email_to_id[email])
            email_to_id[email] = i
    
    # Group emails by root
    groups = defaultdict(set)
    for email, idx in email_to_id.items():
        root = dsu.find(idx)
        groups[root].add(email)
    
    # Build result
    result = []
    for root, emails in groups.items():
        name = accounts[root][0]
        result.append([name] + sorted(emails))
    
    return result

# Test
accounts = [
    ["John", "john@example.com", "john@example.net"],
    ["John", "john@example.com", "john_work@example.com"],
    ["Mary", "mary@example.com"],
    ["John", "john_work@example.com", "john@example.com"]
]
print(f"Merged accounts: {accounts_merge(accounts)}")
# [["John", "john@example.com", "john@example.net", "john_work@example.com"],
#  ["Mary", "mary@example.com"]]
```

**Time Complexity:** O(n * k * α(n)) where k = average emails per account
**Space Complexity:** O(n * k)

---

### 3.4 Number of Connected Components

```python
def count_components(n, edges):
    """Count number of connected components in graph"""
    dsu = DSU(n)
    
    for u, v in edges:
        dsu.union(u, v)
    
    return dsu.count_components()

def get_all_components(n, edges):
    """Get all connected components"""
    dsu = DSU(n)
    
    for u, v in edges:
        dsu.union(u, v)
    
    return dsu.get_components()

# Test
n = 5
edges = [[0, 1], [1, 2], [3, 4]]
print(f"Components: {count_components(n, edges)}")  # 2
print(f"All components: {get_all_components(n, edges)}")  # [[0, 1, 2], [3, 4]]
```

**Time Complexity:** O(n + E * α(n))
**Space Complexity:** O(n)

---

### 3.5 Detect Cycle in Undirected Graph

```python
def has_cycle(n, edges):
    """Detect if undirected graph has a cycle using DSU"""
    dsu = DSU(n)
    
    for u, v in edges:
        if not dsu.union(u, v):
            return True  # Cycle detected
    
    return False

# Alternative using DFS
def has_cycle_dfs(n, edges):
    """Detect cycle using DFS"""
    from collections import defaultdict
    
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = [False] * n
    
    def dfs(node, parent):
        visited[node] = True
        
        for neighbor in graph[node]:
            if not visited[neighbor]:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        
        return False
    
    for i in range(n):
        if not visited[i]:
            if dfs(i, -1):
                return True
    
    return False

# Test
n = 4
edges1 = [[0, 1], [1, 2], [2, 3]]
print(f"Has cycle: {has_cycle(n, edges1)}")  # False

edges2 = [[0, 1], [1, 2], [2, 0]]
print(f"Has cycle: {has_cycle(n, edges2)}")  # True
```

**Time Complexity:** O(n + E)
**Space Complexity:** O(n)

---

### 3.6 Kruskal's Minimum Spanning Tree

```python
def kruskal_mst(n, edges):
    """Find MST weight using Kruskal's algorithm"""
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    
    dsu = DSU(n)
    mst_weight = 0
    edges_used = 0
    
    for u, v, weight in edges:
        if dsu.union(u, v):
            mst_weight += weight
            edges_used += 1
            
            if edges_used == n - 1:
                break
    
    return mst_weight if edges_used == n - 1 else -1

def kruskal_mst_edges(n, edges):
    """Find MST edges using Kruskal's algorithm"""
    edges.sort(key=lambda x: x[2])
    
    dsu = DSU(n)
    mst_edges = []
    
    for u, v, weight in edges:
        if dsu.union(u, v):
            mst_edges.append([u, v, weight])
            
            if len(mst_edges) == n - 1:
                break
    
    return mst_edges

# Test
n = 4
edges = [[0, 1, 10], [0, 2, 6], [0, 3, 5], [1, 3, 15], [2, 3, 4]]
print(f"MST weight: {kruskal_mst(n, edges)}")  # 19
print(f"MST edges: {kruskal_mst_edges(n, edges)}")  # [[2,3,4],[0,3,5],[0,1,10]]
```

**Time Complexity:** O(E log E) for sorting + O(E * α(V))
**Space Complexity:** O(V)

---

### 3.7 Accounts Merge II (With Emails)

```python
def accounts_merge_v2(accounts):
    """Merge accounts with detailed email handling"""
    from collections import defaultdict
    
    email_to_name = {}
    email_to_id = {}
    n = len(accounts)
    
    dsu = DSU(n)
    
    for i, account in enumerate(accounts):
        name = account[0]
        for email in account[1:]:
            email_to_name[email] = name
            
            if email in email_to_id:
                dsu.union(i, email_to_id[email])
            else:
                email_to_id[email] = i
    
    # Group emails by root
    groups = defaultdict(list)
    for email in email_to_name:
        root = dsu.find(email_to_id[email])
        groups[root].append(email)
    
    # Build result
    result = []
    for root, emails in groups.items():
        name = accounts[root][0]
        result.append([name] + sorted(set(emails)))
    
    return result

# Test
accounts = [
    ["Alex", "alex@mail.com", "alex2@mail.com"],
    ["Bob", "bob@mail.com"],
    ["Alex", "alex3@mail.com", "alex@mail.com"],
    ["Bob", "bob2@mail.com", "bob@mail.com"]
]
print(f"Merged: {accounts_merge_v2(accounts)}")
```

---

### 3.8 Number of Islands II (LC 305)

```python
def num_islands_ii(m, n, positions):
    """Dynamic number of islands with add land operations"""
    dsu = DSU(m * n)
    grid = [[0] * n for _ in range(m)]
    result = []
    count = 0
    
    def id(r, c):
        return r * n + c
    
    for r, c in positions:
        if grid[r][c] == 1:
            result.append(count)
            continue
        
        grid[r][c] = 1
        count += 1
        
        # Check all 4 directions
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                if dsu.union(id(r, c), id(nr, nc)):
                    count -= 1
        
        result.append(count)
    
    return result

# Test
m, n = 3, 3
positions = [(0, 0), (0, 1), (1, 2), (2, 1)]
print(f"Islands: {num_islands_ii(m, n, positions)}")  # [1, 1, 2, 3]
```

**Time Complexity:** O(k * α(m*n)) where k = number of operations
**Space Complexity:** O(m*n)

---

### 3.9 Graph Valid Tree (LC 261)

```python
def valid_tree(n, edges):
    """Check if graph is a valid tree"""
    # A tree has exactly n-1 edges and is connected
    if len(edges) != n - 1:
        return False
    
    dsu = DSU(n)
    
    for u, v in edges:
        if not dsu.union(u, v):
            return False  # Cycle detected
    
    return dsu.count_components() == 1

# Alternative using DFS
def valid_tree_dfs(n, edges):
    """Check if graph is a valid tree using DFS"""
    from collections import defaultdict
    
    if len(edges) != n - 1:
        return False
    
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = [False] * n
    
    def dfs(node, parent):
        visited[node] = True
        
        for neighbor in graph[node]:
            if not visited[neighbor]:
                if not dfs(neighbor, node):
                    return False
            elif neighbor != parent:
                return False
        
        return True
    
    return dfs(0, -1) and all(visited)

# Test
n = 5
edges1 = [[0, 1], [0, 2], [0, 3], [1, 4]]
print(f"Valid tree: {valid_tree(n, edges1)}")  # True

edges2 = [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]
print(f"Valid tree: {valid_tree(n, edges2)}")  # False
```

**Time Complexity:** O(n + E)
**Space Complexity:** O(n)

---

## 4. Advanced Applications

### 4.1 Friend Circles (LC 547)

```python
def find_circle_num_v2(isConnected):
    """Number of friend circles using DSU"""
    n = len(isConnected)
    dsu = DSU(n)
    
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j]:
                dsu.union(i, j)
    
    return dsu.count_components()

# Test
isConnected = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
print(f"Friend circles: {find_circle_num_v2(isConnected)}")  # 2
```

### 4.2 Satisfiability of Equality Equations (LC 990)

```python
def equationsPossible(equations):
    """Check if equations can be satisfied"""
    dsu = DSU(26)  # 26 lowercase letters
    
    # Process equalities first
    for eq in equations:
        if eq[1] == '=':
            x, y = ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a')
            dsu.union(x, y)
    
    # Check inequalities
    for eq in equations:
        if eq[1] == '!':
            x, y = ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a')
            if dsu.connected(x, y):
                return False
    
    return True

# Test
equations = ["a==b", "b!=a", "b==c", "a==c"]
print(f"Equations possible: {equationsPossible(equations)}")  # False
```

### 4.3 Regions Cut By Slashes (LC 959)

```python
def regions_by_slashes(grid):
    """Count regions in grid with slashes"""
    n = len(grid)
    dsu = DSU(4 * n * n)
    
    def id(r, c, k):
        return 4 * (r * n + c) + k
    
    for r in range(n):
        for c in range(n):
            char = grid[r][c]
            
            if char == '/':
                dsu.union(id(r, c, 0), id(r, c, 1))
                dsu.union(id(r, c, 2), id(r, c, 3))
            elif char == '\\':
                dsu.union(id(r, c, 0), id(r, c, 3))
                dsu.union(id(r, c, 1), id(r, c, 2))
            else:
                dsu.union(id(r, c, 0), id(r, c, 1))
                dsu.union(id(r, c, 1), id(r, c, 2))
                dsu.union(id(r, c, 2), id(r, c, 3))
            
            # Connect to neighbors
            if r + 1 < n:
                dsu.union(id(r, c, 2), id(r + 1, c, 0))
            if c + 1 < n:
                dsu.union(id(r, c, 1), id(r, c + 1, 3))
    
    return dsu.count_components()

# Test
grid = ["/\\", "\\/"]
print(f"Regions: {regions_by_slashes(grid)}")  # 5
```

---

## 5. Weighted DSU

```python
class WeightedDSU:
    """DSU with weights for problems requiring distance tracking"""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.weight = [0] * n  # Weight from node to parent
    
    def find(self, x):
        if self.parent[x] != x:
            root = self.find(self.parent[x])
            self.weight[x] += self.weight[self.parent[x]]
            self.parent[x] = root
        return self.parent[x]
    
    def union(self, x, y, w):
        """Union with weight: weight(y) - weight(x) = w"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            # Check consistency
            return self.weight[y] - self.weight[x] == w
        
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.weight[root_x] = self.weight[y] - self.weight[x] - w
        else:
            self.parent[root_y] = root_x
            self.weight[root_y] = self.weight[x] - self.weight[y] + w
        
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
        
        return True
    
    def diff(self, x, y):
        """Get weight difference: weight(y) - weight(x)"""
        if self.find(x) != self.find(y):
            return None
        return self.weight[y] - self.weight[x]

# Test
dsu = WeightedDSU(4)
dsu.union(0, 1, 5)  # weight(1) - weight(0) = 5
dsu.union(1, 2, 3)  # weight(2) - weight(1) = 3
print(f"weight(2) - weight(0) = {dsu.diff(0, 2)}")  # 8
```

---

## Summary

| Operation | Time Complexity |
|-----------|-----------------|
| Find | O(α(n)) amortized |
| Union | O(α(n)) amortized |
| Connected | O(α(n)) amortized |
| Count Components | O(n * α(n)) |

Where α is the inverse Ackermann function (practically ≤ 4 for all practical inputs)

---

## Key Patterns for Infosys SP DSE

1. **Connected Components:** DSU for dynamic connectivity
2. **Cycle Detection:** If union returns False, cycle exists
3. **MST:** Kruskal's algorithm with DSU
4. **Accounts Merge:** Map emails to indices, union accounts
5. **Dynamic Graphs:** When edges are added over time
6. **Grid Problems:** Convert 2D to 1D for DSU

---

## Tips for Interview

1. **Always optimize:** Use path compression + union by rank/size
2. **0-indexed vs 1-indexed:** Be careful with indexing
3. **Union returns bool:** Use for cycle detection
4. **Weighted DSU:** For problems requiring distance tracking
5. **Coordinate compression:** When nodes have non-contiguous values
