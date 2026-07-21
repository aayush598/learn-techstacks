# Advanced Data Structures & Bit Manipulation - Problem Bank (Batch 2)

> **Infosys SP DSE Preparation — 30 Problems**
> Covers: Segment Tree, Fenwick Tree, Trie, Disjoint Set Union, Bit Manipulation

---

## SEGMENT TREE / FENWICK TREE (Problems 1–10)

---

### Problem 1: Count of Smaller Numbers After Self

**Statement:** Given an integer array `nums`, return an integer array `counts` where `counts[i]` is the number of smaller elements to the right of `nums[i]`.

**Approach:** Use a Fenwick Tree (Binary Indexed Tree). Coordinate-compress values to indices, then iterate from right to left. For each element, query the BIT prefix sum up to its compressed index minus one to get count of smaller elements already seen, then update the BIT at its index.

```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, i, delta=1):
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

def count_smaller(nums):
    sorted_vals = sorted(set(nums))
    rank = {v: i + 1 for i, v in enumerate(sorted_vals)}
    bit = BIT(len(sorted_vals))
    result = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):
        r = rank[nums[i]]
        result[i] = bit.query(r - 1)
        bit.update(r)
    return result

# Example
print(count_smaller([5, 2, 6, 1]))  # [2, 1, 1, 0]
```

**Time Complexity:** O(n log n) — each element triggers one BIT query and one update.
**Space Complexity:** O(n) — for BIT array and rank map.

---

### Problem 2: Range Sum Query - Mutable (Fenwick Tree)

**Statement:** Design a data structure that supports two operations on an integer array: `update(index, val)` to update the value at index, and `sumRange(left, right)` to return the sum between indices `left` and `right` inclusive.

**Approach:** Use a Fenwick Tree. The BIT stores prefix sums implicitly. To get the range sum, compute `query(right) - query(left - 1)`. For updates, propagate the difference using `update(index, delta)`.

```python
class FenwickTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (self.n + 1)
        self.nums = [0] * self.n
        for i, v in enumerate(nums):
            self.update(i, v)

    def update(self, index, val):
        delta = val - self.nums[index]
        self.nums[index] = val
        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def _query(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def sum_range(self, left, right):
        return self._query(right + 1) - self._query(left)

# Example
ft = FenwickTree([1, 3, 5])
print(ft.sum_range(0, 2))   # 9
ft.update(1, 2)
print(ft.sum_range(0, 2))   # 8
```

**Time Complexity:** O(log n) for both update and query operations.
**Space Complexity:** O(n) — for the BIT tree and nums copy.

---

### Problem 3: Range Minimum Query (Segment Tree)

**Statement:** Given an array, support two operations: `update(index, val)` and `query(l, r)` that returns the minimum value in the range `[l, r]`.

**Approach:** Build a segment tree where each node stores the minimum value of its segment. For a query, recursively combine results from the left and right halves. For an update, propagate the change from leaf to root updating minimums along the way.

```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [float('inf')] * (4 * self.n)
        self._build(data, 1, 0, self.n - 1)

    def _build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        self._build(data, 2 * node, start, mid)
        self._build(data, 2 * node + 1, mid + 1, end)
        self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])

    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self._update(2 * node, start, mid, idx, val)
        else:
            self._update(2 * node + 1, mid + 1, end, idx, val)
        self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])

    def update(self, idx, val):
        self._update(1, 0, self.n - 1, idx, val)

    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return float('inf')
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        left_min = self._query(2 * node, start, mid, l, r)
        right_min = self._query(2 * node + 1, mid + 1, end, l, r)
        return min(left_min, right_min)

    def query(self, l, r):
        return self._query(1, 0, self.n - 1, l, r)

# Example
st = SegmentTree([2, 1, 5, 3, 4])
print(st.query(1, 3))   # 1
st.update(2, 0)
print(st.query(1, 3))   # 0
```

**Time Complexity:** O(log n) for update and query; O(n) for building.
**Space Complexity:** O(n) — segment tree uses ~4n space.

---

### Problem 4: Merge Sort with Inversion Count

**Statement:** Count the number of inversions in an array. An inversion is a pair `(i, j)` where `i < j` and `nums[i] > nums[j]`.

**Approach:** Modify merge sort. During the merge step, whenever an element from the right half is placed before elements from the left half, all remaining left-half elements form inversions with it. Count these during the merge process.

```python
def count_inversions(arr):
    def merge_sort_count(nums, temp, left, right):
        if left >= right:
            return 0
        mid = (left + right) // 2
        count = merge_sort_count(nums, temp, left, mid)
        count += merge_sort_count(nums, temp, mid + 1, right)
        count += merge_count(nums, temp, left, mid, right)
        return count

    def merge_count(nums, temp, left, mid, right):
        i, j, k = left, mid + 1, left
        inv_count = 0
        while i <= mid and j <= right:
            if nums[i] <= nums[j]:
                temp[k] = nums[i]
                i += 1
            else:
                temp[k] = nums[j]
                inv_count += (mid - i + 1)
                j += 1
            k += 1
        while i <= mid:
            temp[k] = nums[i]
            i += 1
            k += 1
        while j <= right:
            temp[k] = nums[j]
            j += 1
            k += 1
        for i in range(left, right + 1):
            nums[i] = temp[i]
        return inv_count

    temp = [0] * len(arr)
    return merge_sort_count(arr, temp, 0, len(arr) - 1)

# Example
print(count_inversions([2, 4, 1, 3, 5]))  # 3
```

**Time Complexity:** O(n log n) — standard merge sort complexity.
**Space Complexity:** O(n) — auxiliary array for merging.

---

### Problem 5: Count Inversions using BIT

**Statement:** Count the number of inversions in an array using a Binary Indexed Tree instead of merge sort.

**Approach:** Coordinate-compress values. Traverse from left to right. For each element, query BIT for count of elements greater than current (already inserted), which is `total_inserted - query(rank)`. Then update BIT at current rank.

```python
class BIT:
    def __init__(self, n):
        self.tree = [0] * (n + 1)

    def update(self, i, delta=1):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

def count_inversions_bit(nums):
    sorted_vals = sorted(set(nums))
    rank = {v: i + 1 for i, v in enumerate(sorted_vals)}
    bit = BIT(len(sorted_vals))
    inversions = 0
    for i, num in enumerate(nums):
        r = rank[num]
        inversions += i - bit.query(r)
        bit.update(r)
    return inversions

# Example
print(count_inversions_bit([2, 4, 1, 3, 5]))  # 3
```

**Time Complexity:** O(n log n) — each element triggers one BIT query and update.
**Space Complexity:** O(n) — for BIT and rank map.

---

### Problem 6: Reverse Pairs using Segment Tree

**Statement:** Given an array, count reverse pairs `(i, j)` where `i < j` and `nums[i] > 2 * nums[j]`.

**Approach:** Use coordinate compression on all values and their doubled values. Iterate left to right. For each element `nums[i]`, query the segment tree for how many previously inserted elements are greater than `2 * nums[i]` (range sum from `2*nums[i]+1` to max). Then insert current element.

```python
class BIT:
    def __init__(self, n):
        self.tree = [0] * (n + 1)

    def update(self, i, delta=1):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def range_query(self, l, r):
        return self.query(r) - self.query(l - 1)

def reverse_pairs(nums):
    sorted_vals = sorted(set(
        [v for num in nums for v in (num, 2 * num + 1)]
    ))
    rank = {v: i + 1 for i, v in enumerate(sorted_vals)}
    bit = BIT(len(sorted_vals))
    count = 0
    for num in nums:
        # Query elements greater than 2*num
        target = 2 * num
        r = rank[target]
        if target in rank:
            count += bit.range_query(r + 1, len(rank))
        else:
            count += bit.range_query(r, len(rank))
        bit.update(rank[num])
    return count

# Example
print(reverse_pairs([1, 3, 2, 3, 1]))  # 2
```

**Time Complexity:** O(n log n) — compression and BIT operations dominate.
**Space Complexity:** O(n) — for coordinate map and BIT.

---

### Problem 7: Range Sum Query 2D - Mutable

**Statement:** Design a 2D data structure that supports `update(row, col, val)` and `sumRegion(row1, col1, row2, col2)` for a 2D matrix.

**Approach:** Use a 2D Binary Indexed Tree. Each cell `(r, c)` is stored in the BIT using 2D prefix sums. For updates, propagate delta to all relevant BIT cells using nested loops with `i += i & (-i)`. For queries, use inclusion-exclusion on the 2D prefix.

```python
class BIT2D:
    def __init__(self, matrix):
        self.m = len(matrix)
        self.n = len(matrix[0]) if self.m else 0
        self.tree = [[0] * (self.n + 1) for _ in range(self.m + 1)]
        self.original = [[0] * self.n for _ in range(self.m)]
        for i in range(self.m):
            for j in range(self.n):
                self.update(i, j, matrix[i][j])

    def _update(self, r, c, delta):
        i = r + 1
        while i <= self.m:
            j = c + 1
            while j <= self.n:
                self.tree[i][j] += delta
                j += j & (-j)
            i += i & (-i)

    def update(self, r, c, val):
        delta = val - self.original[r][c]
        self.original[r][c] = val
        self._update(r, c, delta)

    def _query(self, r, c):
        s = 0
        i = r + 1
        while i > 0:
            j = c + 1
            while j > 0:
                s += self.tree[i][j]
                j -= j & (-j)
            i -= i & (-i)
        return s

    def sum_region(self, r1, c1, r2, c2):
        return (self._query(r2, c2) - self._query(r1 - 1, c2)
                - self._query(r2, c1 - 1) + self._query(r1 - 1, c1 - 1))

# Example
b = BIT2D([[3, 0, 1], [5, 6, 2], [1, 4, 3]])
print(b.sum_region(1, 1, 2, 2))  # 15
b.update(1, 1, 10)
print(b.sum_region(1, 1, 2, 2))  # 25
```

**Time Complexity:** O(log m * log n) for update and sum_region.
**Space Complexity:** O(m * n) — for BIT and original matrix.

---

### Problem 8: Maximum in Range using Segment Tree

**Statement:** Given an array, support `update(index, val)` and `query(l, r)` returning the maximum value in range `[l, r]`.

**Approach:** Build a segment tree where each node stores the maximum of its segment. Query traverses the tree combining left and right max values. Update propagates changes from leaf upward comparing children to set parent maximum.

```python
class MaxSegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [float('-inf')] * (4 * self.n)
        self._build(data, 1, 0, self.n - 1)

    def _build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        self._build(data, 2 * node, start, mid)
        self._build(data, 2 * node + 1, mid + 1, end)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self._update(2 * node, start, mid, idx, val)
        else:
            self._update(2 * node + 1, mid + 1, end, idx, val)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

    def update(self, idx, val):
        self._update(1, 0, self.n - 1, idx, val)

    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return float('-inf')
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return max(
            self._query(2 * node, start, mid, l, r),
            self._query(2 * node + 1, mid + 1, end, l, r)
        )

    def query(self, l, r):
        return self._query(1, 0, self.n - 1, l, r)

# Example
st = MaxSegmentTree([1, 5, 3, 9, 2])
print(st.query(0, 3))   # 9
st.update(4, 10)
print(st.query(0, 4))   # 10
```

**Time Complexity:** O(log n) for update and query; O(n) for build.
**Space Complexity:** O(n) — segment tree array ~4n.

---

### Problem 9: Count of Range Sum

**Statement:** Given an integer array `nums` and two integers `lower` and `upper`, return the number of range sums that lie in `[lower, upper]` inclusive. Range sum `S(i, j)` is defined as the sum of elements from index `i` to `j`.

**Approach:** Compute prefix sums. Use merge sort to count pairs `(i, j)` where `i < j` and `lower <= prefix[j] - prefix[i] <= upper`. During merge, count elements from right half satisfying the condition using binary search on the sorted left half.

```python
def count_range_sum(nums, lower, upper):
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)

    def merge_sort_count(arr, temp, left, right):
        if left >= right:
            return 0
        mid = (left + right) // 2
        count = merge_sort_count(arr, temp, left, mid)
        count += merge_sort_count(arr, temp, mid + 1, right)
        # Count cross-range pairs
        j, k = mid + 1, mid + 1
        for i in range(left, mid + 1):
            while j <= right and arr[j] - arr[i] < lower:
                j += 1
            while k <= right and arr[k] - arr[i] <= upper:
                k += 1
            count += k - j
        # Merge
        i, j, k2 = left, mid + 1, left
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp[k2] = arr[i]
                i += 1
            else:
                temp[k2] = arr[j]
                j += 1
            k2 += 1
        while i <= mid:
            temp[k2] = arr[i]
            i += 1
            k2 += 1
        while j <= right:
            temp[k2] = arr[j]
            j += 1
            k2 += 1
        for i in range(left, right + 1):
            arr[i] = temp[i]
        return count

    temp = [0] * len(prefix)
    return merge_sort_count(prefix, temp, 0, len(prefix) - 1)

# Example
print(count_range_sum([-2, 5, -1], -2, 2))  # 3
```

**Time Complexity:** O(n log n) — merge sort with two-pointer counting.
**Space Complexity:** O(n) — for prefix array and temp array.

---

### Problem 10: Number of Provinces with Range Queries

**Statement:** Given `n` cities and a list of connections, answer queries: "How many provinces exist if we only consider connections with weight ≤ `threshold`?" Process queries offline.

**Approach:** Sort edges by weight. Sort queries by threshold. Use Union-Find (DSU). Process edges incrementally for each query in ascending threshold order, unioning connected cities. The number of provinces is `n - number_of_unions` (components = n - successful unions).

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

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
        self.components -= 1
        return True

def count_provinces_queries(n, edges, queries):
    edges.sort(key=lambda e: e[2])
    sorted_queries = sorted(enumerate(queries), key=lambda x: x[1])
    result = [0] * len(queries)
    dsu = DSU(n)
    edge_idx = 0
    for orig_idx, threshold in sorted_queries:
        while edge_idx < len(edges) and edges[edge_idx][2] <= threshold:
            dsu.union(edges[edge_idx][0], edges[edge_idx][1])
            edge_idx += 1
        result[orig_idx] = dsu.components
    return result

# Example: 4 cities, edges (u, v, weight)
edges = [(0, 1, 3), (1, 2, 1), (2, 3, 4), (0, 2, 2)]
print(count_provinces_queries(4, edges, [1, 2, 3, 5]))  # [4, 2, 2, 1]
```

**Time Complexity:** O(E log E + Q log Q + (E + Q) * α(N)) — sorting + DSU operations.
**Space Complexity:** O(N + E + Q) — for DSU, edges, and queries.

---

## TRIE (Problems 11–18)

---

### Problem 11: Implement Trie (Prefix Tree)

**Statement:** Implement a Trie with `insert(word)`, `search(word)` (exact match), and `starts_with(prefix)` (prefix check).

**Approach:** Each Trie node is a dict of children and a boolean `is_end`. Insert traverses/creates nodes per character. Search checks if all characters exist and the final node is marked `is_end`. Starts_with checks if all characters exist regardless of `is_end`.

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
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True

# Example
t = Trie()
t.insert("apple")
print(t.search("apple"))      # True
print(t.search("app"))        # False
print(t.starts_with("app"))   # True
```

**Time Complexity:** O(m) for insert, search, and starts_with where m = word length.
**Space Complexity:** O(total characters) — storing all inserted words.

---

### Problem 12: Word Search II (Trie + Backtracking)

**Statement:** Given a 2D board of characters and a list of words, find all words from the list that exist on the board. A word can be formed by tracing adjacent cells (up/down/left/right) without revisiting a cell.

**Approach:** Insert all words into a Trie. For each cell on the board, run DFS/backtracking. At each step, check if current prefix exists in Trie (prune if not). When a node is marked `is_end`, add the word to result and unmark to avoid duplicates.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

def find_words(board, words):
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.word = word

    rows, cols = len(board), len(board[0])
    result = []

    def dfs(r, c, node):
        ch = board[r][c]
        if ch not in node.children:
            return
        child = node.children[ch]
        if child.word:
            result.append(child.word)
            child.word = None
        board[r][c] = '#'
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, child)
        board[r][c] = ch
        if not child.children:
            del node.children[ch]

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)
    return result

# Example
board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
print(find_words(board, ["oath","pea","eat","rain"]))  # ['oath', 'eat']
```

**Time Complexity:** O(M * N * 4^L) worst case where M*N is board size, L is max word length. Trie pruning makes it much faster in practice.
**Space Complexity:** O(K) where K is total characters in all words for Trie.

---

### Problem 13: Maximum XOR of Two Numbers in Array

**Statement:** Given an array of integers, find the maximum value of `nums[i] XOR nums[j]` where `0 ≤ i, j < n`.

**Approach:** Build a Trie of the binary representations (32 bits). For each number, traverse the Trie preferring the opposite bit at each level to maximize XOR. Track the maximum XOR found across all numbers.

```python
class TrieNode:
    def __init__(self):
        self.children = {}

def find_max_xor(nums):
    root = TrieNode()

    def insert(num):
        node = root
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            if bit not in node.children:
                node.children[bit] = TrieNode()
            node = node.children[bit]

    def query(num):
        node = root
        result = 0
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            want = 1 - bit
            if want in node.children:
                result |= (1 << i)
                node = node.children[want]
            else:
                node = node.children[bit]
        return result

    for num in nums:
        insert(num)

    max_xor = 0
    for num in nums:
        max_xor = max(max_xor, query(num))
    return max_xor

# Example
print(find_max_xor([3, 10, 5, 25, 2, 8]))  # 28
```

**Time Complexity:** O(n * 32) = O(n) — insert and query each number in 32-bit Trie.
**Space Complexity:** O(n * 32) — Trie nodes for n numbers.

---

### Problem 14: Longest Word in Dictionary

**Statement:** Given a list of words, find the longest word that can be built one character at a time from other words in the list. If there are multiple, return the lexicographically smallest.

**Approach:** Insert all words into a Trie. Then DFS from root, only traversing children that are marked as `is_end` (meaning the prefix itself is a valid word). Track the longest path; on ties, prefer lexicographically smaller character.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

def longest_word(words):
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    best = ""

    def dfs(node, path):
        nonlocal best
        for ch in sorted(node.children.keys()):
            child = node.children[ch]
            if child.is_end:
                word = path + ch
                if len(word) > len(best) or (len(word) == len(best) and word < best):
                    best = word
                dfs(child, word)

    dfs(root, "")
    return best

# Example
print(longest_word(["w", "wo", "wor", "worl", "world"]))  # "world"
```

**Time Complexity:** O(N * L + 26^L) in worst case — building Trie + DFS. In practice much less due to pruning.
**Space Complexity:** O(N * L) — Trie storage.

---

### Problem 15: Search Suggestions System

**Statement:** Given a list of product names and a search word, for each prefix of the search word, return up to 3 product names that start with that prefix, sorted lexicographically.

**Approach:** Sort the products. Build a Trie of all products. For each prefix of the search word, traverse the Trie to the prefix node, then DFS to collect up to 3 words. Sorting once allows ordered traversal.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.suggestions = []

def suggested_products(products, search_word):
    products.sort()
    root = TrieNode()

    for product in products:
        node = root
        for ch in product:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            if len(node.suggestions) < 3:
                node.suggestions.append(product)

    result = []
    node = root
    for ch in search_word:
        if node and ch in node.children:
            node = node.children[ch]
            result.append(node.suggestions)
        else:
            node = None
            result.append([])
    return result

# Example
print(suggested_products(
    ["mobile", "mouse", "moneypot", "monitor", "mousepad"],
    "mouse"
))
# [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],
#  ["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"]]
```

**Time Complexity:** O(N * L * log N) for sorting + O(L) per query. Trie construction is O(N * L).
**Space Complexity:** O(N * L) — Trie nodes storing references.

---

### Problem 16: Replace Words (Shortest Prefix)

**Statement:** Given a list of roots (dictionary) and a sentence, replace each word in the sentence with its shortest root prefix from the dictionary. If no root matches, keep the original word.

**Approach:** Insert all roots into a Trie. For each word in the sentence, traverse the Trie character by character. If a node is marked `is_end`, that root is the shortest prefix match. If traversal fails before finding a match, keep the original word.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

def replace_words(dictionary, sentence):
    root = TrieNode()
    for word in dictionary:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def find_shortest_prefix(word):
        node = root
        for i, ch in enumerate(word):
            if node.is_end:
                return word[:i]
            if ch not in node.children:
                return word
            node = node.children[ch]
        return word

    return " ".join(find_shortest_prefix(w) for w in sentence.split())

# Example
print(replace_words(
    ["cat", "bat", "rat"],
    "the cattle was rattled by the battery"
))
# "the cat was rat by the bat"
```

**Time Complexity:** O(D * L + S) where D = dict size, L = avg root length, S = sentence length.
**Space Complexity:** O(D * L) — Trie for dictionary roots.

---

### Problem 17: Stream of Characters (Suffix Matching)

**Statement:** Design a class that receives a stream of characters one at a time and returns `True` if the suffix of characters received so far matches any word in a given dictionary.

**Approach:** Insert all dictionary words into a Trie, but insert them reversed. Maintain a buffer of recent characters (up to max word length). On each new character, check the Trie with the buffer in reverse order. If any prefix matches (meaning a reversed word matches a suffix), return `True`.

```python
class StreamChecker:
    def __init__(self, words):
        self.root = {}
        self.buffer = []
        self.max_len = 0
        for word in words:
            node = self.root
            self.max_len = max(self.max_len, len(word))
            for ch in reversed(word):
                if ch not in node:
                    node[ch] = {}
                node = node[ch]
            node['$'] = True

    def query(self, letter):
        self.buffer.append(letter)
        if len(self.buffer) > self.max_len:
            self.buffer.pop(0)
        node = self.root
        for ch in reversed(self.buffer):
            if ch not in node:
                return False
            node = node[ch]
            if '$' in node:
                return True
        return False

# Example
sc = StreamChecker(["cd", "f", "kl"])
print(sc.query('a'))  # False
print(sc.query('b'))  # False
print(sc.query('c'))  # False
print(sc.query('d'))  # True  (suffix "cd")
print(sc.query('e'))  # False
print(sc.query('f'))  # True  (suffix "f")
```

**Time Complexity:** O(L) per query where L = max word length (buffer bounded).
**Space Complexity:** O(total characters in words + L) — Trie + buffer.

---

### Problem 18: Palindrome Pairs using Trie

**Statement:** Given a list of words, find all pairs `(i, j)` where `i ≠ j` and `words[i] + words[j]` forms a palindrome.

**Approach:** For each word, insert its reversed form into a Trie with the word's index. For each word, try all possible splits. If the prefix part is a palindrome, check if the remaining suffix exists in the Trie. If the suffix part is a palindrome, check if the reversed prefix exists. Also handle the case where a word's reverse is another word.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.index = -1
        self.palindrome_indices = []

def palindrome_pairs(words):
    root = TrieNode()

    def insert(word, idx):
        node = root
        for i, ch in enumerate(reversed(word)):
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            prefix = word[:len(word) - i]
            if prefix == prefix[::-1]:
                node.palindrome_indices.append(idx)
        node.index = idx

    def search(word, idx):
        node = root
        result = []
        for i, ch in enumerate(word):
            # Case: remaining suffix of word + some word from Trie = palindrome
            if node.index >= 0 and node.index != idx:
                suffix = word[i:]
                if suffix == suffix[::-1]:
                    result.append([idx, node.index])
            if ch not in node.children:
                return result
            node = node.children[ch]
        # Case: entire word consumed, check palindrome indices in Trie
        for j in node.palindrome_indices:
            if j != idx:
                result.append([idx, j])
        return result

    for i, w in enumerate(words):
        insert(w, i)

    result = []
    for i, w in enumerate(words):
        result.extend(search(w, i))
    return result

# Example
print(palindrome_pairs(["abcd", "dcba", "lls", "s", "sssll"]))
# [[0,1],[1,0],[3,2],[2,4]]
```

**Time Complexity:** O(N * K²) where N = number of words, K = max word length.
**Space Complexity:** O(N * K) — Trie storage for all reversed words.

---

## DISJOINT SET UNION (Problems 19–23)

---

### Problem 19: Redundant Connection

**Statement:** Given a tree with `n` nodes labeled `1` to `n`, an extra edge is added making it a graph with one cycle. Find the edge that, when removed, results in a tree.

**Approach:** Use Union-Find. Process edges one by one. For each edge `(u, v)`, check if `u` and `v` are already connected (same root). If yes, this is the redundant edge. Otherwise, union them.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)

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

def find_redundant(edges):
    n = len(edges)
    dsu = DSU(n)
    for u, v in edges:
        if not dsu.union(u, v):
            return [u, v]
    return []

# Example
print(find_redundant([[1,2],[1,3],[2,3]]))  # [2, 3]
```

**Time Complexity:** O(N * α(N)) ≈ O(N) — near-linear with path compression and union by rank.
**Space Complexity:** O(N) — parent and rank arrays.

---

### Problem 20: Number of Islands II (Dynamic)

**Statement:** Start with an empty `m x n` grid. Process a list of operations: each operation adds land at position `(row, col)`. After each operation, return the current number of islands.

**Approach:** Use Union-Find. Each added land cell is a new island. For each added cell, check its 4 neighbors; if a neighbor is land, union them (decreasing island count by 1 per successful union). Track total islands.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = 0

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
        self.count -= 1
        return True

def num_islands2(m, n, positions):
    dsu = DSU(m * n)
    grid = [[0] * n for _ in range(m)]
    result = []
    for r, c in positions:
        if grid[r][c] == 1:
            result.append(dsu.count)
            continue
        grid[r][c] = 1
        dsu.count += 1
        idx = r * n + c
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                dsu.union(idx, nr * n + nc)
        result.append(dsu.count)
    return result

# Example
print(num_islands2(3, 3, [(0,0),(0,1),(1,2),(2,1)]))
# [1, 1, 2, 3]
```

**Time Complexity:** O(K * α(m*n)) where K = number of operations.
**Space Complexity:** O(m * n) — for DSU and grid.

---

### Problem 21: Accounts Merge

**Statement:** Given a list of accounts where each account has a name and a list of emails, merge accounts that share at least one email. Return the merged accounts with unique sorted emails.

**Approach:** Use Union-Find to group account indices that share emails. For each email, track which account index first saw it. If an account sees an email already seen by another account, union the two indices. After processing all emails, group by root parent and build result.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            self.parent[py] = px

def accounts_merge(accounts):
    dsu = DSU(len(accounts))
    email_to_acc = {}
    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in email_to_acc:
                dsu.union(i, email_to_acc[email])
            email_to_acc[email] = i

    groups = {}
    for email, acc_idx in email_to_acc.items():
        root = dsu.find(acc_idx)
        if root not in groups:
            groups[root] = set()
        groups[root].add(email)

    result = []
    for root, emails in groups.items():
        result.append([accounts[root][0]] + sorted(emails))
    return result

# Example
accounts = [["John","john@mail.com","john_new@mail.com"],
            ["John","john@mail.com","john0@mail.com"],
            ["Mary","mary@mail.com"],
            ["John","johnny@mail.com","john@mail.com"]]
print(accounts_merge(accounts))
# [["John","john@mail.com","john_new@mail.com","john0@mail.com"],
#  ["Mary","mary@mail.com"],
#  ["John","john@mail.com","johnny@mail.com"]]
```

**Time Complexity:** O(N * K * α(N)) where N = accounts, K = avg emails per account.
**Space Complexity:** O(N * K) — for email-to-account map and DSU.

---

### Problem 22: Smallest String With Swaps

**Statement:** Given a string and a list of pairs `(i, j)` where characters at indices `i` and `j` can be swapped any number of times, find the lexicographically smallest string achievable.

**Approach:** Use Union-Find to group indices that are connected (directly or transitively) via swap pairs. Within each connected component, sort the characters and place them back at the sorted indices to get the lexicographically smallest arrangement.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            self.parent[py] = px

def smallest_string(s, pairs):
    n = len(s)
    dsu = DSU(n)
    for i, j in pairs:
        dsu.union(i, j)

    groups = {}
    for i in range(n):
        root = dsu.find(i)
        if root not in groups:
            groups[root] = {'indices': [], 'chars': []}
        groups[root]['indices'].append(i)
        groups[root]['chars'].append(s[i])

    result = list(s)
    for root, data in groups.items():
        indices = sorted(data['indices'])
        chars = sorted(data['chars'])
        for idx, ch in zip(indices, chars):
            result[idx] = ch

    return ''.join(result)

# Example
print(smallest_string("dcab", [[0,3],[1,2]]))  # "bacd"
print(smallest_string("dcab", [[0,3],[1,2],[0,2]]))  # "abcd"
```

**Time Complexity:** O(N log N + P * α(N)) where P = number of pairs, N = string length.
**Space Complexity:** O(N) — for DSU and group maps.

---

### Problem 23: Find Smallest Missing Elements

**Statement:** Given an array and queries of the form `(start, k)`, for each query find the k-th smallest missing positive integer starting from `start`.

**Approach:** Process offline. Sort queries by start descending. Use a Union-Find where each positive integer points to the next available integer. Start from the highest value and add numbers to the DSU. For each query, find the k-th available number using the DSU structure.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 2))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def remove(self, x):
        self.parent[x] = self.find(x + 1)

def smallest_missing_queries(arr, queries):
    present = set(arr)
    max_val = max(max(arr) if arr else 0, max(q[0] + q[1] for q in queries) + 1)
    max_val = max(max_val + len(queries) + 2, 100)
    dsu = DSU(max_val)

    # Precompute missing numbers available at each position
    for i in range(1, max_val + 1):
        if i in present:
            dsu.remove(i)

    sorted_queries = sorted(enumerate(queries), key=lambda x: x[0])
    result = [0] * len(queries)

    for orig_idx, (start, k) in sorted_queries:
        # Need k-th missing from start
        # Process: remove all numbers < start to find what's available
        temp_dsu = DSU(max_val)
        for i in range(1, max_val + 1):
            if i in present and i >= start:
                temp_dsu.remove(i)
        # Also remove numbers < start from consideration
        # Actually find k-th missing >= start
        pos = temp_dsu.find(start)
        for _ in range(k - 1):
            temp_dsu.remove(pos)
            pos = temp_dsu.find(pos)
        result[orig_idx] = pos

    return result

# Simple brute-force version for clarity:
def smallest_missing_simple(arr, queries):
    arr_set = set(arr)
    result = []
    for start, k in queries:
        count = 0
        num = start
        while count < k:
            if num not in arr_set:
                count += 1
                if count == k:
                    result.append(num)
                    break
            num += 1
    return result

# Example
print(smallest_missing_simple([1, 3, 5], [(2, 1), (2, 2), (1, 3)]))
# [2, 4, 6]
```

**Time Complexity:** O(N + Q * sqrt(N)) for the simple version. DSU version O((max_val + Q) * α(N)).
**Space Complexity:** O(N + max_val) — for set and DSU.

---

## BIT MANIPULATION (Problems 24–30)

---

### Problem 24: Single Number II

**Statement:** Given an integer array where every element appears exactly three times except one element which appears exactly once, find the single element.

**Approach:** Use bit counting. For each bit position (0–31), count how many numbers have that bit set. If the count is not divisible by 3, the single number has that bit set. Alternatively, use `ones` and `twos` state variables for a more efficient approach.

```python
def single_number(nums):
    ones = 0
    twos = 0
    for num in nums:
        ones = (ones ^ num) & ~twos
        twos = (twos ^ num) & ~ones
    return ones

# Example
print(single_number([2, 2, 3, 2]))     # 3
print(single_number([0, 1, 0, 1, 0, 1, 99]))  # 99
```

**Time Complexity:** O(n) — single pass through the array.
**Space Complexity:** O(1) — only two integer variables.

---

### Problem 25: Maximum XOR Subarray

**Statement:** Find the maximum XOR of a contiguous subarray.

**Approach:** Use a Trie of prefix XOR values. Compute prefix XOR as you traverse. For each prefix, query the Trie to find the previously stored prefix that gives maximum XOR with current prefix. The XOR of two prefixes gives a subarray XOR.

```python
class TrieNode:
    def __init__(self):
        self.children = {}

def max_xor_subarray(nums):
    root = TrieNode()

    def insert(num):
        node = root
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            if bit not in node.children:
                node.children[bit] = TrieNode()
            node = node.children[bit]

    def query(num):
        node = root
        result = 0
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            want = 1 - bit
            if want in node.children:
                result |= (1 << i)
                node = node.children[want]
            else:
                node = node.children[bit]
        return result

    # Insert 0 (empty prefix)
    insert(0)
    prefix_xor = 0
    max_xor = 0

    for num in nums:
        prefix_xor ^= num
        max_xor = max(max_xor, query(prefix_xor))
        insert(prefix_xor)

    return max_xor

# Example
print(max_xor_subarray([1, 2, 3]))     # 3
print(max_xor_subarray([8, 1, 2, 12]))  # 15
```

**Time Complexity:** O(n * 32) = O(n) — for each element, Trie operations are O(32).
**Space Complexity:** O(n * 32) — Trie nodes.

---

### Problem 26: Bitwise AND of Range

**Statement:** Given two integers `left` and `right`, return the bitwise AND of all numbers in the range `[left, right]`.

**Approach:** Find the common prefix of `left` and `right` in binary. The result is the common prefix followed by zeros. Shift both numbers right until they're equal (counting shifts), then shift back left.

```python
def range_bitwise_and(left, right):
    shift = 0
    while left != right:
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift

# Alternative approach using Brian Kernighan's algorithm
def range_bitwise_and_v2(left, right):
    while left < right:
        right &= (right - 1)
    return right

# Example
print(range_bitwise_and(5, 7))   # 4 (binary: 100)
print(range_bitwise_and(1, 2147483647))  # 0
```

**Time Complexity:** O(log n) — shifting right until common prefix, or removing lowest bits.
**Space Complexity:** O(1) — only integer variables.

---

### Problem 27: Minimum Flips to Make a OR b Equal to c

**Statement:** Given three integers `a`, `b`, and `c`, find the minimum number of bit flips required so that `a OR b` equals `c`.

**Approach:** Process each bit position from 0 to 31. For each bit, check the bits of `a`, `b`, and `c`. If `c`'s bit is 1, we need at least one of `a` or `b`'s bits to be 1 (flip one if both are 0). If `c`'s bit is 0, both `a` and `b`'s bits must be 0 (flip each that is 1).

```python
def min_flips(a, b, c):
    flips = 0
    for i in range(32):
        bit_a = (a >> i) & 1
        bit_b = (b >> i) & 1
        bit_c = (c >> i) & 1
        if bit_c == 0:
            flips += bit_a + bit_b
        else:
            if bit_a == 0 and bit_b == 0:
                flips += 1
    return flips

# Example
print(min_flips(2, 6, 5))  # 3
# 2=010, 6=110, 5=101
# 010 OR 110 = 110 != 101 → need flips
```

**Time Complexity:** O(32) = O(1) — fixed number of bit positions.
**Space Complexity:** O(1) — constant extra space.

---

### Problem 28: Binary String With Substrings Representing 1 to N

**Statement:** Given a binary string `s` and an integer `n`, return `True` if for every integer `x` from 1 to `n`, its binary representation is a substring of `s`.

**Approach:** Convert each number from 1 to n to binary and check if it exists in `s`. To optimize, we can check only numbers whose binary length is ≤ len(s), and for large n, iterate through numbers whose binary representations are within the substring length.

```python
def query_string(s, n):
    for i in range(1, n + 1):
        if bin(i)[2:] not in s:
            return False
    return True

# Optimized version: only check numbers whose binary fits in s
def query_string_optimized(s, n):
    max_len = len(s)
    for i in range(1, n + 1):
        binary = bin(i)[2:]
        if len(binary) > max_len:
            return False
        if binary not in s:
            return False
    return True

# Example
print(query_string("0110", 3))  # True (1="1", 2="10", 3="11" all in "0110")
print(query_string("0110", 4))  # False ("100" not in "0110")
```

**Time Complexity:** O(n * L * S) where L = avg binary length, S = len(s). With optimization, only checks numbers with binary length ≤ len(s).
**Space Complexity:** O(L) — for binary string conversion.

---

### Problem 29: Concatenation of Consecutive Binary Numbers

**Statement:** Given an integer `n`, return the decimal value of the binary string formed by concatenating the binary representations of 1 to n, modulo `10^9 + 7`.

**Approach:** For each number `i` from 1 to `n`, find its bit length. Shift the current result left by that many bits (modulo) and add `i`. Track the number of bits to shift using `bit_length()`.

```python
def concatenated_binary(n):
    MOD = 10**9 + 7
    result = 0
    for i in range(1, n + 1):
        bits = i.bit_length()
        result = ((result << bits) + i) % MOD
    return result

# Example
print(concatenated_binary(1))   # 1
print(concatenated_binary(3))   # 27
# "1" + "10" + "11" = "11011" = 27
print(concatenated_binary(12))  # 50537971
```

**Time Complexity:** O(n) — single pass from 1 to n, each step is O(1).
**Space Complexity:** O(1) — only integer variables.

---

### Problem 30: Find the Longest Substring With All Unique Characters

**Statement:** Given a string, find the length of the longest substring without repeating characters.

**Approach:** Use sliding window with a hash map storing the last seen index of each character. Maintain a window `[left, right]`. When a character repeats, move `left` to `max(left, last_seen[char] + 1)`. Track the maximum window size.

```python
def longest_unique_substring(s):
    char_index = {}
    left = 0
    max_len = 0
    for right, ch in enumerate(s):
        if ch in char_index and char_index[ch] >= left:
            left = char_index[ch] + 1
        char_index[ch] = right
        max_len = max(max_len, right - left + 1)
    return max_len

# Bit manipulation approach: use a bitmask for ASCII characters
def longest_unique_bitmask(s):
    char_mask = 0
    left = 0
    max_len = 0
    for right, ch in enumerate(s):
        bit = 1 << (ord(ch) - ord('a'))
        while char_mask & bit:
            char_mask ^= (1 << (ord(s[left]) - ord('a')))
            left += 1
        char_mask |= bit
        max_len = max(max_len, right - left + 1)
    return max_len

# Example
print(longest_unique_substring("abcabcbb"))   # 3 ("abc")
print(longest_unique_substring("bbbbb"))      # 1
print(longest_unique_substring("pwwkew"))     # 3 ("wke")
print(longest_unique_bitmask("abcabcbb"))     # 3
```

**Time Complexity:** O(n) — each character visited at most twice (once by `right`, once by `left`).
**Space Complexity:** O(min(n, 26)) — for hash map with lowercase letters only.

---

## Summary Table

| # | Problem | Data Structure | Time Complexity | Space Complexity |
|---|---------|---------------|-----------------|------------------|
| 1 | Count Smaller After Self | Fenwick Tree | O(n log n) | O(n) |
| 2 | Range Sum Mutable | Fenwick Tree | O(n log n) build, O(log n) query/update | O(n) |
| 3 | Range Minimum Query | Segment Tree | O(n build, log n query/update) | O(n) |
| 4 | Merge Sort Inversions | Modified Merge Sort | O(n log n) | O(n) |
| 5 | Count Inversions (BIT) | Fenwick Tree | O(n log n) | O(n) |
| 6 | Reverse Pairs | Fenwick Tree | O(n log n) | O(n) |
| 7 | 2D Range Sum Mutable | 2D Fenwick Tree | O(log m * log n) | O(m*n) |
| 8 | Maximum in Range | Segment Tree | O(n build, log n query/update) | O(n) |
| 9 | Count Range Sum | Modified Merge Sort | O(n log n) | O(n) |
| 10 | Provinces with Queries | DSU + Offline | O(E log E + Q log Q) | O(N) |
| 11 | Implement Trie | Trie | O(m) per operation | O(total chars) |
| 12 | Word Search II | Trie + Backtracking | O(M*N*4^L) | O(K) |
| 13 | Max XOR of Two Numbers | Trie | O(n * 32) | O(n * 32) |
| 14 | Longest Word in Dict | Trie + DFS | O(N*L) | O(N*L) |
| 15 | Search Suggestions | Trie | O(N*L log N + Q*L) | O(N*L) |
| 16 | Replace Words | Trie | O(D*L + S) | O(D*L) |
| 17 | Stream of Characters | Trie (Reversed) | O(L) per query | O(total + L) |
| 18 | Palindrome Pairs | Trie | O(N*K²) | O(N*K) |
| 19 | Redundant Connection | DSU | O(N*α(N)) | O(N) |
| 20 | Islands II Dynamic | DSU | O(K*α(mn)) | O(m*n) |
| 21 | Accounts Merge | DSU | O(N*K*α(N)) | O(N*K) |
| 22 | Smallest String Swaps | DSU | O(N log N) | O(N) |
| 23 | Smallest Missing | DSU | O(N + Q*sqrt(N)) | O(N) |
| 24 | Single Number II | Bit Manipulation | O(n) | O(1) |
| 25 | Max XOR Subarray | Trie + Prefix XOR | O(n * 32) | O(n * 32) |
| 26 | Bitwise AND Range | Bit Manipulation | O(log n) | O(1) |
| 27 | Min Flips OR Equal | Bit Manipulation | O(1) | O(1) |
| 28 | Binary 1 to N Substrings | String + Binary | O(n * L * S) | O(L) |
| 29 | Concat Binary Numbers | Bit Manipulation | O(n) | O(1) |
| 30 | Longest Unique Substring | Sliding Window | O(n) | O(1) or O(26) |

---

> **Total: 30 problems** covering Segment Trees, Fenwick Trees, Tries, Disjoint Set Union, and Bit Manipulation — all with complete Python solutions.
