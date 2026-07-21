# Python Competitive Programming Templates - Infosys SP DSE

Ready-to-use templates. Copy-paste during the exam.

---

## 1. Fast I/O Template

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    # solution here
    print(result)

# For multiple test cases
def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        # solution here
        print(result)

solve()
```

---

## 2. BFS Template

```python
from collections import deque

def bfs(start, graph):
    """BFS traversal. Returns dict of {node: distance from start}."""
    queue = deque([start])
    visited = {start: 0}
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited[neighbor] = visited[node] + 1
                queue.append(neighbor)
    return visited

def bfs_shortest_path(start, end, graph):
    """Returns shortest path (list) from start to end."""
    if start == end:
        return [start]
    
    queue = deque([start])
    visited = {start: None}
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited[neighbor] = node
                if neighbor == end:
                    # Reconstruct path
                    path = []
                    curr = end
                    while curr is not None:
                        path.append(curr)
                        curr = visited[curr]
                    return path[::-1]
                queue.append(neighbor)
    return []  # no path

def bfs_grid(start, grid, rows, cols):
    """BFS on a grid. start = (r, c). Returns distances."""
    queue = deque([start])
    dist = {start: 0}
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in dist:
                if grid[nr][nc] != '#':  # not a wall
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    queue.append((nr, nc))
    return dist
```

---

## 3. DFS Template

```python
def dfs(node, graph, visited):
    """Iterative DFS using a stack."""
    stack = [node]
    while stack:
        curr = stack.pop()
        if curr in visited:
            continue
        visited.add(curr)
        for neighbor in graph[curr]:
            if neighbor not in visited:
                stack.append(neighbor)

def dfs_recursive(node, graph, visited):
    """Recursive DFS."""
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(neighbor, graph, visited)

def dfs_topological(node, graph, visited, order):
    """DFS for topological sorting."""
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_topological(neighbor, graph, visited, order)
    order.append(node)

def dfs_connected_components(n, graph):
    """Find all connected components."""
    visited = set()
    components = []
    
    for i in range(n):
        if i not in visited:
            component = []
            stack = [i]
            while stack:
                node = stack.pop()
                if node in visited:
                    continue
                visited.add(node)
                component.append(node)
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
            components.append(sorted(component))
    
    return components
```

---

## 4. Dijkstra Template

```python
import heapq

def dijkstra(start, graph, n):
    """Shortest path from start to all nodes.
    graph: adjacency list where graph[u] = [(v, weight), ...]
    Returns: list of distances
    """
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]
    
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for neighbor, weight in graph[node]:
            if dist[node] + weight < dist[neighbor]:
                dist[neighbor] = dist[node] + weight
                heapq.heappush(heap, (dist[neighbor], neighbor))
    
    return dist

def dijkstra_with_path(start, end, graph, n):
    """Shortest path from start to end with path reconstruction."""
    dist = [float('inf')] * n
    prev = [-1] * n
    dist[start] = 0
    heap = [(0, start)]
    
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        if node == end:
            break
        for neighbor, weight in graph[node]:
            if dist[node] + weight < dist[neighbor]:
                dist[neighbor] = dist[node] + weight
                prev[neighbor] = node
                heapq.heappush(heap, (dist[neighbor], neighbor))
    
    # Reconstruct path
    if dist[end] == float('inf'):
        return float('inf'), []
    
    path = []
    curr = end
    while curr != -1:
        path.append(curr)
        curr = prev[curr]
    return dist[end], path[::-1]
```

---

## 5. Union-Find Template

```python
class UnionFind:
    """Disjoint Set Union with path compression and union by rank."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n  # number of connected components
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # already in same set
        
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        
        self.components -= 1
        return True
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)

class UnionFindWithSize:
    """DSU with component size tracking."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        
        if self.size[px] < self.size[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        self.components -= 1
        return True
    
    def get_size(self, x):
        return self.size[self.find(x)]
```

---

## 6. Segment Tree Template

```python
class SegmentTree:
    """Segment tree for range sum queries with point updates."""
    
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.build(data, 1, 0, self.n - 1)
    
    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        self.build(data, 2 * node, start, mid)
        self.build(data, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def update(self, idx, val):
        """Update element at index idx to val."""
        self._update(1, 0, self.n - 1, idx, val)
    
    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self._update(2 * node, start, mid, idx, val)
        else:
            self._update(2 * node + 1, mid + 1, end, idx, val)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def query(self, l, r):
        """Query sum of elements in range [l, r]."""
        return self._query(1, 0, self.n - 1, l, r)
    
    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return self._query(2 * node, start, mid, l, r) + \
               self._query(2 * node + 1, mid + 1, end, l, r)

class SegmentTreeMinMax:
    """Segment tree for range min/max queries."""
    
    def __init__(self, data, func=min):
        self.n = len(data)
        self.func = func
        self.default = float('inf') if func == min else float('-inf')
        self.tree = [self.default] * (4 * self.n)
        self.build(data, 1, 0, self.n - 1)
    
    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        self.build(data, 2 * node, start, mid)
        self.build(data, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.func(self.tree[2 * node], self.tree[2 * node + 1])
    
    def query(self, l, r):
        return self._query(1, 0, self.n - 1, l, r)
    
    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return self.default
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return self.func(self._query(2 * node, start, mid, l, r),
                         self._query(2 * node + 1, mid + 1, end, l, r))
```

---

## 7. Trie Template

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0  # number of words with this prefix

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.count += 1
        node.is_end = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    
    def count_words_with_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.count
    
    def delete(self, word):
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                return len(node.children) == 0
            
            char = word[depth]
            if char not in node.children:
                return False
            
            should_delete = _delete(node.children[char], word, depth + 1)
            if should_delete:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end
            return False
        
        _delete(self.root, word, 0)

# Usage example
trie = Trie()
trie.insert("apple")
trie.insert("app")
trie.insert("application")
print(trie.search("apple"))      # True
print(trie.starts_with("app"))   # True
print(trie.count_words_with_prefix("app"))  # 3
```

---

## 8. Monotonic Stack Template

```python
def next_greater_element(arr):
    """Find the next greater element for each element in the array.
    Returns list where result[i] = next element > arr[i], or -1 if none.
    """
    n = len(arr)
    result = [-1] * n
    stack = []  # stores indices
    
    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            result[stack.pop()] = arr[i]
        stack.append(i)
    return result

def next_smaller_element(arr):
    """Find the next smaller element for each element."""
    n = len(arr)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        while stack and arr[stack[-1]] > arr[i]:
            result[stack.pop()] = arr[i]
        stack.append(i)
    return result

def previous_greater_element(arr):
    """Find the previous greater element for each element."""
    n = len(arr)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        if stack:
            result[i] = arr[stack[-1]]
        stack.append(i)
    return result

def largest_rectangle_histogram(heights):
    """Largest rectangle in histogram."""
    n = len(heights)
    stack = []
    max_area = 0
    
    for i in range(n + 1):
        while stack and (i == n or heights[stack[-1]] > heights[i]):
            h = heights[stack.pop()]
            w = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, h * w)
        stack.append(i)
    
    return max_area

def trapping_rain_water(height):
    """Trapping rain water problem."""
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n
    
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])
    
    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])
    
    water = 0
    for i in range(n):
        water += min(left_max[i], right_max[i]) - height[i]
    return water
```

---

## 9. Backtracking Template

```python
def permutations(nums):
    """Generate all permutations of nums."""
    result = []
    
    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        for i, num in enumerate(remaining):
            path.append(num)
            backtrack(path, remaining[:i] + remaining[i + 1:])
            path.pop()
    
    backtrack([], nums)
    return result

def combinations(n, k):
    """Generate all combinations of k numbers from 1 to n."""
    result = []
    
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(1, [])
    return result

def subsets(nums):
    """Generate all subsets of nums."""
    result = []
    
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(0, [])
    return result

def subsets_with_duplicates(nums):
    """Generate all unique subsets (nums may contain duplicates)."""
    result = []
    nums.sort()
    
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(0, [])
    return result

def n_queens(n):
    """Solve N-Queens problem. Returns all valid board configurations."""
    result = []
    
    def backtrack(row, cols, diag1, diag2, board):
        if row == n:
            result.append(["".join(r) for r in board])
            return
        
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            backtrack(row + 1, cols, diag1, diag2, board)
            
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    
    board = [['.' for _ in range(n)] for _ in range(n)]
    backtrack(0, set(), set(), set(), board)
    return result
```

---

## 10. Modular Arithmetic Template

```python
MOD = 10**9 + 7

def power(base, exp, mod=MOD):
    """Fast exponentiation: base^exp % mod. Time: O(log exp)"""
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result

def mod_inverse(a, mod=MOD):
    """Modular inverse using Fermat's little theorem. a^(-1) = a^(mod-2) % mod"""
    return power(a, mod - 2, mod)

def mod_add(a, b, mod=MOD):
    return (a + b) % mod

def mod_sub(a, b, mod=MOD):
    return (a - b + mod) % mod

def mod_mul(a, b, mod=MOD):
    return (a * b) % mod

def mod_div(a, b, mod=MOD):
    return mod_mul(a, mod_inverse(b, mod))

# Precompute factorials
def precompute_factorials(n, mod=MOD):
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    return fact

# nCr % MOD
def nCr(n, r, fact, mod=MOD):
    if r < 0 or r > n:
        return 0
    return fact[n] * mod_inverse(fact[r] * fact[n - r] % mod, mod) % mod

# nPr % MOD
def nPr(n, r, fact, mod=MOD):
    if r < 0 or r > n:
        return 0
    return fact[n] * mod_inverse(fact[n - r], mod) % mod
```

---

## 11. Binary Search on Answer Template

```python
def binary_search_minimize(lo, hi, check):
    """Find minimum value in [lo, hi] where check(mid) is True.
    Assumes: if check(mid) is True, check(mid+1) is also True.
    """
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

def binary_search_maximize(lo, hi, check):
    """Find maximum value in [lo, hi] where check(mid) is True.
    Assumes: if check(mid) is True, check(mid-1) is also True.
    """
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if check(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo

# Example: Split array into m subarrays such that max sum is minimized
def split_array(nums, m):
    def can_split(max_sum):
        count = 1
        current = 0
        for num in nums:
            if current + num > max_sum:
                count += 1
                current = num
            else:
                current += num
        return count <= m
    
    lo = max(nums)
    hi = sum(nums)
    return binary_search_minimize(lo, hi, can_split)
```

---

## 12. Sliding Window Template

```python
from collections import Counter

def sliding_window_fixed(s, k):
    """Fixed-size sliding window of size k."""
    window = Counter()
    result = []
    
    for right in range(len(s)):
        window[s[right]] += 1
        
        if right >= k:
            left = right - k
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
        
        if right >= k - 1:
            # Process window
            result.append(dict(window))
    
    return result

def sliding_window_variable(s, condition):
    """Variable-size sliding window with a condition."""
    window = Counter()
    left = 0
    result = 0
    
    for right in range(len(s)):
        window[s[right]] += 1
        
        while not condition(window):
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        
        # Update result (e.g., max length, count, etc.)
        result = max(result, right - left + 1)
    
    return result

# Example: Longest substring without repeating characters
def length_of_longest_substring(s):
    char_set = set()
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)
    
    return max_len

# Example: Minimum window substring
def min_window(s, t):
    from collections import Counter
    
    if not t or not s:
        return ""
    
    t_count = Counter(t)
    required = len(t_count)
    formed = 0
    window_counts = {}
    
    left = 0
    min_len = float('inf')
    min_left = 0
    
    for right in range(len(s)):
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        if char in t_count and window_counts[char] == t_count[char]:
            formed += 1
        
        while formed == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left
            
            left_char = s[left]
            window_counts[left_char] -= 1
            if left_char in t_count and window_counts[left_char] < t_count[left_char]:
                formed -= 1
            left += 1
    
    return "" if min_len == float('inf') else s[min_left:min_left + min_len]
```

---

## 13. Kadane's Algorithm Template

```python
def kadane(arr):
    """Maximum subarray sum (can be all negative)."""
    max_sum = curr_sum = arr[0]
    for num in arr[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)
    return max_sum

def kadane_with_indices(arr):
    """Maximum subarray sum with start and end indices."""
    max_sum = curr_sum = arr[0]
    start = end = temp_start = 0
    
    for i in range(1, len(arr)):
        if arr[i] > curr_sum + arr[i]:
            curr_sum = arr[i]
            temp_start = i
        else:
            curr_sum += arr[i]
        
        if curr_sum > max_sum:
            max_sum = curr_sum
            start = temp_start
            end = i
    
    return max_sum, start, end

def kadane_circular(arr):
    """Maximum circular subarray sum."""
    # Case 1: Normal Kadane's (max subarray not wrapping around)
    normal_max = kadane(arr)
    
    # Case 2: Circular (min subarray in the middle, sum - min = max wrapping)
    total_sum = sum(arr)
    min_sum = float('inf')
    curr_min = 0
    for num in arr:
        curr_min = min(num, curr_min + num)
        min_sum = min(min_sum, curr_min)
    
    circular_max = total_sum - min_sum
    
    # If all elements are negative, circular_max will be 0 (empty subarray)
    # which is invalid, so return normal_max
    if circular_max == 0:
        return normal_max
    
    return max(normal_max, circular_max)
```

---

## 14. Topological Sort (Kahn's) Template

```python
from collections import deque

def topological_sort_kahn(n, edges):
    """Kahn's BFS-based topological sort.
    n: number of nodes (0 to n-1)
    edges: list of [u, v] meaning u -> v
    Returns: topological order, or [] if cycle exists
    """
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    
    queue = deque([i for i in range(n) if indegree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    return result if len(result) == n else []  # [] means cycle

def topological_sort_dfs(n, edges):
    """DFS-based topological sort."""
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
    
    visited = set()
    order = []
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        order.append(node)
    
    for i in range(n):
        if i not in visited:
            dfs(i)
    
    return order[::-1]

def course_schedule(n, prerequisites):
    """Can finish all courses? (Cycle detection via topological sort)"""
    return len(topological_sort_kahn(n, prerequisites)) == n
```

---

## 15. Fenwick Tree (Binary Indexed Tree) Template

```python
class FenwickTree:
    """Binary Indexed Tree for prefix sum queries and point updates.
    1-indexed internally.
    """
    
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, i, delta):
        """Add delta to element at index i (0-indexed)."""
        i += 1  # convert to 1-indexed
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)
    
    def query(self, i):
        """Prefix sum from index 0 to i (0-indexed)."""
        i += 1
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s
    
    def range_query(self, l, r):
        """Sum of elements from index l to r (0-indexed)."""
        return self.query(r) - (self.query(l - 1) if l > 0 else 0)

class FenwickTree2D:
    """2D Fenwick Tree for 2D prefix sum queries."""
    
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.tree = [[0] * (n + 1) for _ in range(m + 1)]
    
    def update(self, x, y, delta):
        x += 1
        y += 1
        while x <= self.m:
            j = y
            while j <= self.n:
                self.tree[x][j] += delta
                j += j & (-j)
            x += x & (-x)
    
    def query(self, x, y):
        x += 1
        y += 1
        s = 0
        while x > 0:
            j = y
            while j > 0:
                s += self.tree[x][j]
                j -= j & (-j)
            x -= x & (-x)
        return s
    
    def range_query(self, x1, y1, x2, y2):
        """Sum of rectangle from (x1,y1) to (x2,y2) inclusive."""
        return (self.query(x2, y2) 
                - self.query(x1 - 1, y2) 
                - self.query(x2, y1 - 1) 
                + self.query(x1 - 1, y1 - 1))
```

---

## 16. Disjoint Set Union (with Size + Rollback) Template

```python
class DSU:
    """DSU with union by size, path compression, and component count."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n
    
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.size[px] < self.size[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        self.components -= 1
        return True
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)

class DSURollback:
    """DSU with rollback capability (for offline queries)."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n
        self.history = []  # stack of changes for rollback
    
    def find(self, x):
        while self.parent[x] != x:
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.size[px] < self.size[py]:
            px, py = py, px
        self.history.append((py, self.parent[py], px, self.size[px], self.components))
        self.parent[py] = px
        self.size[px] += self.size[py]
        self.components -= 1
        return True
    
    def rollback(self):
        if not self.history:
            return
        py, old_parent, px, old_size, old_components = self.history.pop()
        self.parent[py] = old_parent
        self.size[px] = old_size
        self.components = old_components
```

---

## 17. LCA (Binary Lifting) Template

```python
import sys
sys.setrecursionlimit(10**6)

class LCA:
    """Lowest Common Ancestor using binary lifting.
    Preprocess: O(n log n), Query: O(log n)
    """
    
    def __init__(self, n, root, graph):
        self.n = n
        self.LOG = 20  # enough for n <= 10^6
        self.depth = [0] * n
        self.parent = [[-1] * self.LOG for _ in range(n)]
        self.graph = graph
        
        self._dfs(root, -1, 0)
        self._preprocess()
    
    def _dfs(self, node, par, d):
        self.depth[node] = d
        self.parent[node][0] = par
        for neighbor in self.graph[node]:
            if neighbor != par:
                self._dfs(neighbor, node, d + 1)
    
    def _preprocess(self):
        for j in range(1, self.LOG):
            for i in range(self.n):
                if self.parent[i][j - 1] != -1:
                    self.parent[i][j] = self.parent[self.parent[i][j - 1]][j - 1]
    
    def lca(self, u, v):
        """Find LCA of u and v."""
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        
        # Lift u to same depth as v
        diff = self.depth[u] - self.depth[v]
        for j in range(self.LOG):
            if diff & (1 << j):
                u = self.parent[u][j]
        
        if u == v:
            return u
        
        # Binary lift both
        for j in range(self.LOG - 1, -1, -1):
            if self.parent[u][j] != self.parent[v][j]:
                u = self.parent[u][j]
                v = self.parent[v][j]
        
        return self.parent[u][0]
    
    def distance(self, u, v):
        """Distance between u and v."""
        w = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[w]

# Usage:
# graph = {0: [1, 2], 1: [0, 3, 4], 2: [0], 3: [1], 4: [1]}
# lca = LCA(5, 0, graph)
# print(lca.lca(3, 4))  # 1
```

---

## 18. KMP Algorithm Template

```python
def kmp_build_lps(pattern):
    """Build the Longest Proper Prefix which is also Suffix array.
    lps[i] = length of longest proper prefix of pattern[0..i]
             which is also a suffix of pattern[0..i]
    """
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps

def kmp_search(text, pattern):
    """KMP string matching. Returns list of all starting indices where
    pattern is found in text. Time: O(n + m)
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return []
    
    lps = kmp_build_lps(pattern)
    result = []
    i = j = 0  # i for text, j for pattern
    
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        
        if j == m:
            result.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return result

# Example
text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
print(kmp_search(text, pattern))  # [9]
```

---

## 19. Rabin-Karp Algorithm Template

```python
def rabin_karp(text, pattern):
    """Rabin-Karp string matching using rolling hash.
    Returns list of starting indices where pattern is found in text.
    Time: O(n + m) average, O(n*m) worst case (with hash verification)
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    base = 256
    mod = 10**9 + 7
    
    # Precompute base^(m-1) % mod
    base_pow = pow(base, m - 1, mod)
    
    # Compute hash of pattern and first window of text
    pattern_hash = 0
    text_hash = 0
    
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        text_hash = (text_hash * base + ord(text[i])) % mod
    
    result = []
    
    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            # Verify character by character (to avoid hash collision)
            if text[i:i + m] == pattern:
                result.append(i)
        
        # Rolling hash: remove leading char, add trailing char
        if i < n - m:
            text_hash = (text_hash - ord(text[i]) * base_pow) % mod
            text_hash = (text_hash * base + ord(text[i + m])) % mod
            text_hash %= mod  # ensure non-negative
    
    return result

# Example
text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
print(rabin_karp(text, pattern))  # [9]
```

---

## 20. Fast Exponentiation + Combinatorics Template

```python
MOD = 10**9 + 7

# Matrix exponentiation for linear recurrences
def mat_mult(A, B, mod=MOD):
    """Multiply two matrices A and B."""
    n = len(A)
    m = len(B[0])
    k = len(B)
    C = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for l in range(k):
                C[i][j] = (C[i][j] + A[i][l] * B[l][j]) % mod
    return C

def mat_pow(matrix, power, mod=MOD):
    """Matrix exponentiation. Raises matrix to given power."""
    n = len(matrix)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    while power > 0:
        if power % 2 == 1:
            result = mat_mult(result, matrix, mod)
        matrix = mat_mult(matrix, matrix, mod)
        power //= 2
    
    return result

def fibonacci_matrix(n):
    """Find nth Fibonacci number using matrix exponentiation.
    F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)
    [1 1]^n   [F(n+1) F(n)  ]
    [1 1]   = [F(n)   F(n-1)]
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    base = [[1, 1], [1, 0]]
    result = mat_pow(base, n)
    return result[0][1]

# Example
for i in range(10):
    print(f"F({i}) = {fibonacci_matrix(i)}")
# F(0)=0, F(1)=1, F(2)=1, F(3)=2, F(4)=3, F(5)=5, ...
```

---

## Template Quick Reference

| # | Template | When to Use |
|---|----------|-------------|
| 1 | Fast I/O | Always in competitive programming |
| 2 | BFS | Shortest path in unweighted graph/grid |
| 3 | DFS | Connected components, cycle detection, path finding |
| 4 | Dijkstra | Shortest path in weighted graph |
| 5 | Union-Find | Dynamic connectivity, cycle detection in undirected graph |
| 6 | Segment Tree | Range queries + point updates |
| 7 | Trie | String prefix matching, autocomplete |
| 8 | Monotonic Stack | Next greater/smaller element, largest rectangle |
| 9 | Backtracking | Permutations, combinations, N-Queens, Sudoku |
| 10 | Modular Arithmetic | nCr, power, inverse (always with MOD) |
| 11 | Binary Search on Answer | Minimize maximum, maximize minimum |
| 12 | Sliding Window | Subarray/substring problems |
| 13 | Kadane's | Maximum subarray sum |
| 14 | Topological Sort | Task scheduling, course prerequisites |
| 15 | Fenwick Tree | Prefix sums with updates |
| 16 | DSU | Graph connectivity, Kruskal's MST |
| 17 | LCA (Binary Lifting) | Distance between nodes in tree |
| 18 | KMP | Pattern matching in strings |
| 19 | Rabin-Karp | Pattern matching with rolling hash |
| 20 | Matrix Exponentiation | Fast Fibonacci, linear recurrences |
