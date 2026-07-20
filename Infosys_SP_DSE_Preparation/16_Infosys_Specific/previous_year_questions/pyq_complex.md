# Infosys SP DSE - Previous Year Questions (Complex / SP L3 Level)

> 10 most challenging questions from Infosys SP L3 rounds.

---

## 1. DP + Bitmask State Compression

**Problem Statement:** Given N jobs and N workers, each worker has different skill level for each job. Assign each worker exactly one job to minimize total cost. This is the Assignment Problem using bitmask DP.

**Approach:** dp[mask] = minimum cost to assign workers represented by set bits in mask. mask is a bitmask of assigned workers.

```python
def min_cost_assignment(cost):
    n = len(cost)
    full_mask = (1 << n) - 1
    dp = [float('inf')] * (1 << n)
    dp[0] = 0

    for mask in range(1 << n):
        worker = bin(mask).count('1')
        if worker >= n:
            continue
        for job in range(n):
            if not (mask & (1 << job)):
                new_mask = mask | (1 << job)
                dp[new_mask] = min(dp[new_mask], dp[mask] + cost[worker][job])

    return dp[full_mask]

cost = [[3, 7, 5, 8], [5, 2, 9, 7], [6, 1, 4, 3], [8, 2, 7, 9]]
print(min_cost_assignment(cost))  # Output: 13
```

**Complexity:** O(n * 2^n) time, O(2^n) space

**Tips:** Works for n <= 20. For larger n, use Hungarian Algorithm O(n^3). Key pattern: iterate all subsets using bitmask.

---

## 2. Tree DP with Range Queries

**Problem Statement:** Given a tree with N nodes and Q queries, each query asks for the maximum value node in the subtree rooted at node U within depth range [L, R]. Process all queries efficiently.

**Approach:** Euler tour to flatten tree + segment tree with depth-aware queries.

```python
import sys
from collections import defaultdict

class TreeRangeQuery:
    def __init__(self, values, edges):
        self.n = len(values)
        self.values = values
        self.graph = defaultdict(list)
        for u, v in edges:
            self.graph[u].append(v)
            self.graph[v].append(u)

        self.timer = 0
        self.euler = [0] * (2 * self.n)
        self.depth = [0] * self.n
        self.start = [0] * self.n
        self.end = [0] * self.n

        self.dfs(0, -1, 0)

    def dfs(self, node, parent, d):
        self.start[node] = self.timer
        self.depth[node] = d
        self.euler[self.timer] = node
        self.timer += 1

        for child in self.graph[node]:
            if child != parent:
                self.dfs(child, node, d + 1)

        self.end[node] = self.timer - 1

    def query_subtree(self, node, min_depth, max_depth):
        result = float('-inf')
        for i in range(self.start[node], self.end[node] + 1):
            if min_depth <= self.depth[self.euler[i]] <= max_depth:
                result = max(result, self.values[self.euler[i]])
        return result

values = [5, 3, 8, 2, 7, 1]
edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]
tree = TreeRangeQuery(values, edges)

print(tree.query_subtree(0, 1, 2))  # Max in subtree of 0, depths 1-2
```

**Complexity:** O(n) per query naive, O(n log n) with segment tree + offline processing

**Tips:** Euler tour + segment tree is a powerful combination. Practice flattening trees.

---

## 3. TSP Variant (Traveling Salesman Problem)

**Problem Statement:** A delivery person needs to visit K out of N locations and return to start. Each location has a profit. Maximize total profit such that total distance <= D. Find maximum profit achievable.

**Approach:** Bitmask DP with distance constraint. dp[mask][i] = maximum profit reaching city i with visited set mask.

```python
def tsp_max_profit(dist, profit, start, max_dist, k):
    n = len(dist)
    full_mask = (1 << n) - 1

    # dp[mask][i] = (min_dist, max_profit) to reach i with visited set mask
    dp = [[(float('inf'), 0) for _ in range(n)] for _ in range(1 << n)]
    dp[1 << start][start] = (0, profit[start])

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == (float('inf'), 0):
                continue
            curr_dist, curr_profit = dp[mask][u]
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                new_dist = curr_dist + dist[u][v]
                new_profit = curr_profit + profit[v]
                if new_dist <= max_dist:
                    old = dp[new_mask][v]
                    if new_profit > old[1] or (new_profit == old[1] and new_dist < old[0]):
                        dp[new_mask][v] = (new_dist, new_profit)

    best_profit = 0
    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u][0] <= max_dist:
                total_profit = dp[mask][u][1]
                if bin(mask).count('1') >= k:
                    best_profit = max(best_profit, total_profit)

    return best_profit

dist = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
profit = [10, 20, 15, 25]
print(tsp_max_profit(dist, profit, 0, 50, 3))
```

**Complexity:** O(2^n * n^2) time, O(2^n * n) space

**Tips:** Works for n <= 15-16. For larger problems, need approximation algorithms or branch and bound.

---

## 4. Interval Scheduling with Profits

**Problem Statement:** Given N intervals with start, end time and profit, find maximum profit such that no two selected intervals overlap.

**Approach:** Sort by end time + DP with binary search.

```python
import bisect

def max_profit_intervals(intervals):
    intervals.sort(key=lambda x: x[1])
    n = len(intervals)
    end_times = [intervals[i][1] for i in range(n)]

    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        start, end, profit = intervals[i - 1]

        # Find latest non-overlapping interval
        idx = bisect.bisect_right(end_times, start, 0, i - 1)
        dp[i] = max(dp[i - 1], dp[idx] + profit)

    return dp[n]

intervals = [(1, 3, 5), (2, 4, 6), (3, 5, 4), (4, 6, 3)]
print(max_profit_intervals(intervals))  # Output: 9
```

**Complexity:** O(n log n) time, O(n) space

**Tips:** Variant of weighted job scheduling. Also practice: maximum number of non-overlapping intervals.

---

## 5. Graph Coloring with Minimum Colors

**Problem Statement:** Given an undirected graph, find minimum number of colors needed to color vertices such that no two adjacent vertices have same color.

**Approach:** NP-hard in general. For specific graph types: Bipartite check (2-colorable), or use DSATUR/backtracking for small graphs.

```python
def graph_coloring_min_colors(adj_matrix):
    n = len(adj_matrix)
    if n == 0:
        return 0

    colors = [0] * n
    colors[0] = 1

    # Try to color with increasing number of colors
    for num_colors in range(1, n + 1):
        if solve_coloring(adj_matrix, colors, 1, num_colors, n):
            return num_colors

    return n

def solve_coloring(adj, colors, vertex, num_colors, n):
    if vertex == n:
        return True

    for color in range(1, num_colors + 1):
        if is_safe(adj, colors, vertex, color):
            colors[vertex] = color
            if solve_coloring(adj, colors, vertex + 1, num_colors, n):
                return True
            colors[vertex] = 0

    return False

def is_safe(adj, colors, vertex, color):
    for i in range(len(adj)):
        if adj[vertex][i] and colors[i] == color:
            return False
    return True

adj = [[0, 1, 1, 1], [1, 0, 1, 0], [1, 1, 0, 1], [1, 0, 1, 0]]
print(graph_coloring_min_colors(adj))  # Output: 3
```

**Complexity:** O(m^n) worst case, O(n^2) with greedy for bipartite check

**Tips:** For practical interviews, mention greedy approximation and backtracking for exact.

---

## 6. Advanced String Matching with Multiple Patterns

**Problem Statement:** Given a text and multiple patterns, find all occurrences of all patterns in the text efficiently.

**Approach:** Aho-Corasick algorithm (trie + failure links).

```python
from collections import deque

class AhoCorasick:
    def __init__(self):
        self.goto = [{}]
        self.fail = [0]
        self.output = [[]]
        self.state_count = 1

    def add_pattern(self, pattern, pattern_id):
        state = 0
        for char in pattern:
            if char not in self.goto[state]:
                self.goto.append({})
                self.fail.append(0)
                self.output.append([])
                self.goto[state][char] = self.state_count
                self.state_count += 1
            state = self.goto[state][char]
        self.output[state].append(pattern_id)

    def build(self):
        queue = deque()
        for char, state in self.goto[0].items():
            self.fail[state] = 0
            queue.append(state)

        while queue:
            r = queue.popleft()
            for char, s in self.goto[r].items():
                queue.append(s)
                state = self.fail[r]
                while state and char not in self.goto[state]:
                    state = self.fail[state]
                self.fail[s] = self.goto[state].get(char, 0)
                if self.fail[s] == s:
                    self.fail[s] = 0
                self.output[s] = self.output[s] + self.output[self.fail[s]]

    def search(self, text):
        state = 0
        results = {}
        for i, char in enumerate(text):
            while state and char not in self.goto[state]:
                state = self.fail[state]
            state = self.goto[state].get(char, 0)
            for pattern_id in self.output[state]:
                results.setdefault(pattern_id, []).append(i)
        return results

ac = AhoCorasick()
patterns = ["he", "she", "his", "hers"]
for i, p in enumerate(patterns):
    ac.add_pattern(p, i)
ac.build()

text = "ahishers"
results = ac.search(text)
for pid, positions in results.items():
    print(f"Pattern '{patterns[pid]}' found at: {positions}")
# Pattern 'his' found at: [1, 3]
# Pattern 'she' found at: [3]
# Pattern 'he' found at: [4]
# Pattern 'hers' found at: [4]
```

**Complexity:** O(n + m + z) time where n=text, m=total pattern length, z=matches

**Tips:** Aho-Corasick is the gold standard for multi-pattern matching. Worth learning.

---

## 7. Matrix Chain Multiplication Variant

**Problem Statement:** Given matrices with dimensions, find order of multiplication to minimize scalar multiplications. Variant: find minimum cost to multiply all matrices where cost = row * col * intermediate.

```python
def matrix_chain_order(dimensions):
    n = len(dimensions) - 1
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]

def matrix_chain_with_parens(dimensions):
    n = len(dimensions) - 1
    dp = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k

    def build_parens(i, j):
        if i == j:
            return f"M{i}"
        k = split[i][j]
        left = build_parens(i, k)
        right = build_parens(k + 1, j)
        return f"({left} x {right})"

    return dp[0][n - 1], build_parens(0, n - 1)

dims = [10, 30, 5, 60]
print(matrix_chain_order(dims))  # Output: 4500
cost, paren = matrix_chain_with_parens(dims)
print(f"Cost: {cost}, Parentheses: {paren}")
```

**Complexity:** O(n^3) time, O(n^2) space

**Tips:** Classic DP problem. Always reconstruct the parenthesization, not just the cost.

---

## 8. Egg Dropping with K Eggs and N Floors

**Problem Statement:** Find minimum number of trials needed to determine critical floor with K eggs and N floors.

**Approach:** DP. dp[e][f] = min trials with e eggs and f floors.

```python
def egg_drop(eggs, floors):
    dp = [[0] * (floors + 1) for _ in range(eggs + 1)]

    for i in range(1, eggs + 1):
        for j in range(1, floors + 1):
            if i == 1:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = 0
            else:
                dp[i][j] = float('inf')
                # Binary search optimization
                low, high = 1, j
                while low <= high:
                    mid = (low + high) // 2
                    break_floor = dp[i - 1][mid - 1]
                    survive_floor = dp[i][j - mid]
                    worst = 1 + max(break_floor, survive_floor)
                    dp[i][j] = min(dp[i][j], worst)

                    if break_floor < survive_floor:
                        low = mid + 1
                    elif break_floor > survive_floor:
                        high = mid - 1
                    else:
                        break

    return dp[eggs][floors]

print(egg_drop(2, 10))  # Output: 4
print(egg_drop(1, 10))  # Output: 10
```

**Complexity:** O(eggs * floors * log floors) with binary search, O(eggs * floors) space

**Tips:** Binary search optimization reduces from O(eggs * floors^2) to O(eggs * floors * log floors).

---

## 9. Minimum Cost to Connect All Cities with Constraints

**Problem Statement:** N cities with bidirectional roads. Some roads are already built (cost 0), others need construction (given cost). Find minimum cost to make all cities connected. This is a Minimum Spanning Tree variant.

**Approach:** Modified Kruskal's/Prim's with pre-built edges having weight 0.

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
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

def min_cost_connect(n, existing_roads, new_roads):
    uf = UnionFind(n)
    total_cost = 0

    # Process existing roads first (cost 0)
    for u, v in existing_roads:
        uf.union(u, v)

    # Sort new roads by cost
    new_roads.sort(key=lambda x: x[2])

    for u, v, cost in new_roads:
        if uf.union(u, v):
            total_cost += cost

    # Check if all connected
    root = uf.find(0)
    for i in range(1, n):
        if uf.find(i) != root:
            return -1

    return total_cost

n = 5
existing = [(0, 1), (2, 3)]
new_roads = [(0, 2, 5), (1, 2, 3), (3, 4, 1), (1, 3, 2)]
print(min_cost_connect(n, existing, new_roads))  # Output: 4
```

**Complexity:** O(E log E) time, O(N) space

**Tips:** Pre-built edges are essentially free. Union them first, then apply Kruskal's.

---

## 10. Maximum Weight Independent Set in Tree

**Problem Statement:** Given a tree with weighted nodes, find maximum weight subset of nodes such that no two selected nodes are adjacent.

**Approach:** Tree DP. dp[node][0] = max weight without selecting node, dp[node][1] = max weight selecting node.

```python
from collections import defaultdict

def max_weight_independent_set(n, edges, weights):
    tree = defaultdict(list)
    for u, v in edges:
        tree[u].append(v)
        tree[v].append(u)

    # dp[node][0] = max weight WITHOUT selecting node
    # dp[node][1] = max weight SELECTING node
    dp = [[0, 0] for _ in range(n)]

    def dfs(node, parent):
        dp[node][1] = weights[node]

        for child in tree[node]:
            if child != parent:
                dfs(child, node)
                dp[node][0] += max(dp[child][0], dp[child][1])
                dp[node][1] += dp[child][0]

    dfs(0, -1)
    return max(dp[0][0], dp[0][1])

weights = [3, 2, 1, 4, 5]
edges = [(0, 1), (0, 2), (1, 3), (1, 4)]
print(max_weight_independent_set(5, edges, weights))  # Output: 12
```

**Complexity:** O(n) time, O(n) space

**Tips:** Base cases: leaf node dp[leaf][1] = weight, dp[leaf][0] = 0. This is also known as Maximum Weight Independent Set on trees.

---

## Summary Table

| # | Problem | Time | Space | Category |
|---|---------|------|-------|----------|
| 1 | Assignment (Bitmask DP) | O(n * 2^n) | O(2^n) | Bitmask DP |
| 2 | Tree Range Queries | O(n log n) | O(n) | Tree + Segment |
| 3 | TSP Variant | O(2^n * n^2) | O(2^n * n) | Bitmask DP |
| 4 | Interval Scheduling | O(n log n) | O(n) | DP + Binary Search |
| 5 | Graph Coloring | O(m^n) | O(n) | Backtracking |
| 6 | Aho-Corasick | O(n + m + z) | O(m) | String Matching |
| 7 | Matrix Chain | O(n^3) | O(n^2) | Interval DP |
| 8 | Egg Dropping | O(eggs * n * log n) | O(eggs * n) | DP + Binary Search |
| 9 | Connect Cities (MST) | O(E log E) | O(N) | Union-Find |
| 10 | MWIS Tree | O(n) | O(n) | Tree DP |

> **Pro Tip:** SP L3 complex problems test your ability to combine multiple concepts. Always identify the core pattern and build from there.
