# Advanced Data Structures Practice Problems

## Segment Tree Problems

### Problem 1: Range Sum Query Mutable (LC 307)

**Problem:** Design a data structure to answer range sum queries and support point updates.

**Approach:** Use segment tree for O(log n) updates and queries.

```python
class NumArray:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)
        self.nums = nums[:]
        self.build(0, 0, self.n - 1)
    
    def build(self, node, start, end):
        if start == end:
            self.tree[node] = self.nums[start]
        else:
            mid = (start + end) // 2
            self.build(2 * node + 1, start, mid)
            self.build(2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def update(self, node, start, end, idx, val):
        if start == end:
            self.nums[idx] = val
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node + 1, start, mid, idx, val)
            else:
                self.update(2 * node + 2, mid + 1, end, idx, val)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def sumRange(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return self.sumRange(2 * node + 1, start, mid, l, r) + \
               self.sumRange(2 * node + 2, mid + 1, end, l, r)

# Usage
arr = NumArray([1, 3, 5, 7, 9])
print(arr.sumRange(0, 0, 4, 1, 3))  # 15
arr.update(0, 0, 4, 2, 6)
print(arr.sumRange(0, 0, 4, 1, 3))  # 16
```

**Time Complexity:** O(n) build, O(log n) query/update
**Space Complexity:** O(n)

---

### Problem 2: Range Minimum Query (LC 315)

**Problem:** Find minimum element in a range with point updates.

**Approach:** Use segment tree storing minimum values.

```python
class RMQ:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [float('inf')] * (4 * self.n)
        self.build(0, 0, self.n - 1, nums)
    
    def build(self, node, start, end, nums):
        if start == end:
            self.tree[node] = nums[start]
        else:
            mid = (start + end) // 2
            self.build(2 * node + 1, start, mid, nums)
            self.build(2 * node + 2, mid + 1, end, nums)
            self.tree[node] = min(self.tree[2 * node + 1], 
                                  self.tree[2 * node + 2])
    
    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node + 1, start, mid, idx, val)
            else:
                self.update(2 * node + 2, mid + 1, end, idx, val)
            self.tree[node] = min(self.tree[2 * node + 1], 
                                  self.tree[2 * node + 2])
    
    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return float('inf')
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return min(self.query(2 * node + 1, start, mid, l, r),
                   self.query(2 * node + 2, mid + 1, end, l, r))

# Usage
rmq = RMQ([2, 1, 5, 3, 4])
print(rmq.query(0, 0, 4, 1, 3))  # 1
rmq.update(0, 0, 4, 2, 0)
print(rmq.query(0, 0, 4, 1, 3))  # 0
```

**Time Complexity:** O(n) build, O(log n) query/update
**Space Complexity:** O(n)

---

### Problem 3: Count of Range Sum (LC 327)

**Problem:** Count range sums in [lower, upper].

**Approach:** Use merge sort to count prefix sum pairs.

```python
def countRangeSum(nums, lower, upper):
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)
    
    def merge_sort_count(arr):
        if len(arr) <= 1:
            return arr, 0
        
        mid = len(arr) // 2
        left, left_count = merge_sort_count(arr[:mid])
        right, right_count = merge_sort_count(arr[mid:])
        
        # Count cross pairs
        j = k = 0
        cross_count = 0
        for i in range(len(left)):
            while j < len(right) and left[i] + lower > right[j]:
                j += 1
            while k < len(right) and left[i] + upper >= right[k]:
                k += 1
            cross_count += k - j
        
        # Merge
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        
        return merged, left_count + right_count + cross_count
    
    _, result = merge_sort_count(prefix)
    return result

# Test
print(countRangeSum([-2, 5, -1], -2, 2))  # 3
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

---

## Fenwick Tree Problems

### Problem 4: Count Inversions (LC 315)

**Problem:** Count number of inversions in array.

**Approach:** Use BIT to count elements smaller than current from right.

```python
def count_inversions(nums):
    sorted_nums = sorted(set(nums))
    rank = {v: i + 1 for i, v in enumerate(sorted_nums)}
    
    n = len(nums)
    bit = [0] * (n + 2)
    
    def update(idx):
        while idx <= n:
            bit[idx] += 1
            idx += idx & (-idx)
    
    def query(idx):
        result = 0
        while idx > 0:
            result += bit[idx]
            idx -= idx & (-idx)
        return result
    
    inv_count = 0
    
    for i in range(n - 1, -1, -1):
        r = rank[nums[i]]
        inv_count += query(r - 1)
        update(r)
    
    return inv_count

# Test
print(count_inversions([2, 4, 1, 3, 5]))  # 3
print(count_inversions([5, 4, 3, 2, 1]))  # 10
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

---

### Problem 5: Count Smaller Numbers After Self (LC 315)

**Problem:** For each element, count smaller elements to its right.

**Approach:** Use BIT processing from right to left.

```python
def count_smaller(nums):
    sorted_nums = sorted(set(nums))
    rank = {v: i + 1 for i, v in enumerate(sorted_nums)}
    
    n = len(nums)
    bit = [0] * (n + 2)
    result = [0] * n
    
    def update(idx):
        while idx <= n:
            bit[idx] += 1
            idx += idx & (-idx)
    
    def query(idx):
        res = 0
        while idx > 0:
            res += bit[idx]
            idx -= idx & (-idx)
        return res
    
    for i in range(n - 1, -1, -1):
        r = rank[nums[i]]
        result[i] = query(r - 1)
        update(r)
    
    return result

# Test
print(count_smaller([5, 2, 6, 1]))  # [2, 1, 1, 0]
print(count_smaller([-1]))  # [0]
print(count_smaller([-1, -1]))  # [0, 0]
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

---

### Problem 6: Range Update and Point Query

**Problem:** Support range updates (add value) and point queries.

**Approach:** Use BIT with difference array concept.

```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, idx, delta):
        idx += 1
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & (-idx)
    
    def query(self, idx):
        result = 0
        idx += 1
        while idx > 0:
            result += self.tree[idx]
            idx -= idx & (-idx)
        return result
    
    def range_update(self, l, r, delta):
        self.update(l, delta)
        if r + 1 < self.n:
            self.update(r + 1, -delta)

# Test
bit = BIT(8)
bit.range_update(2, 5, 5)
print(f"arr[3] = {bit.query(3)}")  # 5
print(f"arr[1] = {bit.query(1)}")  # 0
```

**Time Complexity:** O(log n) for both operations
**Space Complexity:** O(n)

---

## Trie Problems

### Problem 7: Implement Trie (LC 208)

**Problem:** Implement trie with insert, search, and startsWith.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def startsWith(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

# Test
trie = Trie()
trie.insert("apple")
print(trie.search("apple"))   # True
print(trie.search("app"))     # False
print(trie.startsWith("app")) # True
trie.insert("app")
print(trie.search("app"))     # True
```

**Time Complexity:** O(m) for all operations, m = word length
**Space Complexity:** O(m) per word

---

### Problem 8: Word Search II (LC 212)

**Problem:** Find all words from dictionary that can be formed in board.

**Approach:** Build trie, then DFS on board with backtracking.

```python
def find_words(board, words):
    trie = {}
    for word in words:
        node = trie
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['#'] = word
    
    rows, cols = len(board), len(board[0])
    result = []
    
    def dfs(i, j, parent):
        char = board[i][j]
        if char not in parent:
            return
        
        node = parent[char]
        
        if '#' in node:
            result.append(node['#'])
            del node['#']
        
        board[i][j] = '#'
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = i + dx, j + dy
            if 0 <= ni < rows and 0 <= nj < cols and board[ni][nj] != '#':
                dfs(ni, nj, node)
        
        board[i][j] = char
        
        if not node:
            del parent[char]
    
    for i in range(rows):
        for j in range(cols):
            dfs(i, j, trie)
    
    return result

# Test
board = [
    ['o', 'a', 'a', 'n'],
    ['e', 't', 'a', 'e'],
    ['i', 'h', 'k', 'r'],
    ['i', 'f', 'l', 'v']
]
words = ["oath", "pea", "eat", "rain"]
print(find_words(board, words))  # ["oath", "eat"]
```

**Time Complexity:** O(M * N * 4^L) where L = max word length
**Space Complexity:** O(W * L) for trie

---

### Problem 9: Maximum XOR of Two Numbers (LC 421)

**Problem:** Find maximum XOR of two numbers in array.

**Approach:** Use binary trie for bit-by-bit matching.

```python
class TrieNode:
    def __init__(self):
        self.children = {}

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, num):
        node = self.root
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            if bit not in node.children:
                node.children[bit] = TrieNode()
            node = node.children[bit]
    
    def query(self, num):
        node = self.root
        result = 0
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            desired = 1 - bit
            
            if desired in node.children:
                result |= (1 << i)
                node = node.children[desired]
            else:
                node = node.children[bit]
        return result

def find_maximum_xor(nums):
    trie = Trie()
    max_xor = 0
    
    for num in nums:
        trie.insert(num)
        max_xor = max(max_xor, trie.query(num))
    
    return max_xor

# Test
print(find_maximum_xor([3, 10, 5, 25, 2, 8]))  # 28
print(find_maximum_xor([0]))  # 0
print(find_maximum_xor([2, 3]))  # 3
```

**Time Complexity:** O(31n) = O(n)
**Space Complexity:** O(31n)

---

### Problem 10: Replace Words (LC 648)

**Problem:** Replace roots in sentence with shortest root.

**Approach:** Build trie, find shortest root for each word.

```python
def replace_words(dictionary, sentence):
    trie = {}
    for root in dictionary:
        node = trie
        for char in root:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['#'] = root
    
    def find_shortest_root(word):
        node = trie
        for i, char in enumerate(word):
            if '#' in node:
                return node['#']
            if char not in node:
                return word
            node = node[char]
        return word
    
    return ' '.join(find_shortest_root(word) for word in sentence.split())

# Test
dictionary = ["cat", "bat", "rat"]
sentence = "the cattle was rattled by the battery"
print(replace_words(dictionary, sentence))
# "the cat was rat by the bat"
```

**Time Complexity:** O(D * L + S) where D = dictionary size, L = avg root length
**Space Complexity:** O(D * L)

---

## DSU Problems

### Problem 11: Number of Provinces (LC 547)

**Problem:** Find number of connected components in friendship matrix.

**Approach:** Use DSU to merge friends.

```python
def find_circle_num(isConnected):
    n = len(isConnected)
    parent = list(range(n))
    rank = [0] * n
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x == root_y:
            return
        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_y] = root_x
            rank[root_x] += 1
    
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j]:
                union(i, j)
    
    return len(set(find(i) for i in range(n)))

# Test
isConnected = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
print(find_circle_num(isConnected))  # 2
```

**Time Complexity:** O(n²)
**Space Complexity:** O(n)

---

### Problem 12: Redundant Connection (LC 684)

**Problem:** Find edge that creates a cycle.

**Approach:** DSU - if union returns False, edge creates cycle.

```python
def findRedundantConnection(edges):
    parent = list(range(len(edges) + 1))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x == root_y:
            return False
        parent[root_y] = root_x
        return True
    
    for u, v in edges:
        if not union(u, v):
            return [u, v]
    
    return []

# Test
print(findRedundantConnection([[1, 2], [1, 3], [2, 3]]))  # [2, 3]
print(findRedundantConnection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]))  # [1, 4]
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

---

### Problem 13: Accounts Merge (LC 721)

**Problem:** Merge accounts that share common emails.

**Approach:** Map emails to account indices, union accounts with common emails.

```python
def accountsMerge(accounts):
    from collections import defaultdict
    
    parent = list(range(len(accounts)))
    rank = [0] * len(accounts)
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x == root_y:
            return
        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_y] = root_x
            rank[root_x] += 1
    
    email_to_id = {}
    
    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in email_to_id:
                union(i, email_to_id[email])
            email_to_id[email] = i
    
    groups = defaultdict(list)
    for email, idx in email_to_id.items():
        root = find(idx)
        groups[root].append(email)
    
    result = []
    for root, emails in groups.items():
        name = accounts[root][0]
        result.append([name] + sorted(set(emails)))
    
    return result

# Test
accounts = [
    ["John", "john@example.com", "john@example.net"],
    ["John", "john@example.com", "john_work@example.com"],
    ["Mary", "mary@example.com"]
]
print(accountsMerge(accounts))
# [["John", "john@example.com", "john@example.net", "john_work@example.com"],
#  ["Mary", "mary@example.com"]]
```

**Time Complexity:** O(n * k * α(n))
**Space Complexity:** O(n * k)

---

### Problem 14: Number of Islands II (LC 305)

**Problem:** Dynamic number of islands with add land operations.

**Approach:** DSU with 2D grid mapped to 1D.

```python
def numIslands2(m, n, positions):
    parent = list(range(m * n))
    rank = [0] * (m * n)
    grid = [0] * (m * n)
    count = 0
    result = []
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x == root_y:
            return False
        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_y] = root_x
            rank[root_x] += 1
        return True
    
    def id(r, c):
        return r * n + c
    
    for r, c in positions:
        if grid[id(r, c)]:
            result.append(count)
            continue
        
        grid[id(r, c)] = 1
        count += 1
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[id(nr, nc)]:
                if union(id(r, c), id(nr, nc)):
                    count -= 1
        
        result.append(count)
    
    return result

# Test
print(numIslands2(3, 3, [(0, 0), (0, 1), (1, 2), (2, 1)]))  # [1, 1, 2, 3]
```

**Time Complexity:** O(k * α(m*n))
**Space Complexity:** O(m*n)

---

### Problem 15: Graph Valid Tree (LC 261)

**Problem:** Check if graph is a valid tree.

**Approach:** Tree has n-1 edges and is connected.

```python
def validTree(n, edges):
    if len(edges) != n - 1:
        return False
    
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x == root_y:
            return False
        parent[root_y] = root_x
        return True
    
    for u, v in edges:
        if not union(u, v):
            return False
    
    return True

# Test
print(validTree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]))  # True
print(validTree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]))  # False
```

**Time Complexity:** O(n + E)
**Space Complexity:** O(n)

---

## Summary Table

| # | Problem | Data Structure | Time Complexity |
|---|---------|---------------|-----------------|
| 1 | Range Sum Query Mutable | Segment Tree | O(n + q log n) |
| 2 | Range Minimum Query | Segment Tree | O(n + q log n) |
| 3 | Count of Range Sum | Merge Sort | O(n log n) |
| 4 | Count Inversions | BIT | O(n log n) |
| 5 | Count Smaller After Self | BIT | O(n log n) |
| 6 | Range Update Point Query | BIT | O(q log n) |
| 7 | Implement Trie | Trie | O(q * m) |
| 8 | Word Search II | Trie + DFS | O(M * N * 4^L) |
| 9 | Maximum XOR Pair | Trie | O(31n) |
| 10 | Replace Words | Trie | O(D * L + S) |
| 11 | Number of Provinces | DSU | O(n²) |
| 12 | Redundant Connection | DSU | O(n) |
| 13 | Accounts Merge | DSU | O(n * k * α(n)) |
| 14 | Number of Islands II | DSU | O(k * α(m*n)) |
| 15 | Graph Valid Tree | DSU | O(n + E) |

---

## Tips for Infosys SP DSE

1. **Segment Tree:** Use for range queries with updates
2. **Fenwick Tree:** Simpler for prefix sums and frequency counting
3. **Trie:** Use for string matching and prefix problems
4. **DSU:** Use for connected components and cycle detection
5. **Combine techniques:** Many problems combine these structures
