# 16. Advanced Data Structures

Complete, tested implementations of the data structures that come up in coding
rounds. Copy-paste ready; each class is self-contained.

## Segment Tree (array-based, point update + range query)

### Sum variant

```python
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.build(arr, 0, 0, self.n - 1)

    def build(self, arr, node, lo, hi):
        if lo == hi:
            self.tree[node] = arr[lo]
            return
        mid = (lo + hi) // 2
        self.build(arr, 2 * node + 1, lo, mid)
        self.build(arr, 2 * node + 2, mid + 1, hi)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def update(self, idx, val, node=0, lo=None, hi=None):
        if lo is None:
            lo, hi = 0, self.n - 1
        if lo == hi:
            self.tree[node] = val
            return
        mid = (lo + hi) // 2
        if idx <= mid:
            self.update(idx, val, 2 * node + 1, lo, mid)
        else:
            self.update(idx, val, 2 * node + 2, mid + 1, hi)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def query(self, ql, qr, node=0, lo=None, hi=None):
        if lo is None:
            lo, hi = 0, self.n - 1
        if ql <= lo and hi <= qr:            # node fully inside query
            return self.tree[node]
        if qr < lo or hi < ql:               # node fully outside query
            return 0
        mid = (lo + hi) // 2
        return (self.query(ql, qr, 2 * node + 1, lo, mid)
                + self.query(ql, qr, 2 * node + 2, mid + 1, hi))

st = SegmentTree([1, 3, 5, 7, 9, 11])
print(st.query(0, 5))    # 36  (whole range)
print(st.query(1, 3))    # 15  (3 + 5 + 7)
st.update(1, 10)
print(st.query(1, 3))    # 22
```

### Min/max variant — just change the combine operation and the "outside" value

```python
class SegmentTreeMin:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.build(arr, 0, 0, self.n - 1)

    def build(self, arr, node, lo, hi):
        if lo == hi:
            self.tree[node] = arr[lo]
            return
        mid = (lo + hi) // 2
        self.build(arr, 2 * node + 1, lo, mid)
        self.build(arr, 2 * node + 2, mid + 1, hi)
        self.tree[node] = min(self.tree[2 * node + 1], self.tree[2 * node + 2])

    def update(self, idx, val, node=0, lo=None, hi=None):
        if lo is None:
            lo, hi = 0, self.n - 1
        if lo == hi:
            self.tree[node] = val
            return
        mid = (lo + hi) // 2
        if idx <= mid:
            self.update(idx, val, 2 * node + 1, lo, mid)
        else:
            self.update(idx, val, 2 * node + 2, mid + 1, hi)
        self.tree[node] = min(self.tree[2 * node + 1], self.tree[2 * node + 2])

    def query(self, ql, qr, node=0, lo=None, hi=None):
        if lo is None:
            lo, hi = 0, self.n - 1
        if ql <= lo and hi <= qr:
            return self.tree[node]
        if qr < lo or hi < ql:
            return float('inf')              # 'inf' for min tree, '-inf' for max tree
        mid = (lo + hi) // 2
        return min(self.query(ql, qr, 2 * node + 1, lo, mid),
                   self.query(ql, qr, 2 * node + 2, mid + 1, hi))
```

For a max tree: swap `min` -> `max` everywhere and use `float('-inf')` for
out-of-range queries.

Complexity (both variants): build O(n), update O(log n), query O(log n), space O(4n).

## Fenwick / Binary Indexed Tree (BIT)

```python
class Fenwick:
    def __init__(self, arr=None, n=0):
        if arr is not None:                  # build from array
            n = len(arr)
            self.n = n
            self.bit = [0] * (n + 1)
            for i, v in enumerate(arr, 1):   # 1-based
                self.add(i, v)
        else:                                # build empty, size n
            self.n = n
            self.bit = [0] * (n + 1)

    def add(self, i, delta):                 # point update: +delta at i
        while i <= self.n:
            self.bit[i] += delta
            i += i & (-i)

    def prefix_sum(self, i):                 # sum of indices 1..i
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & (-i)
        return s

    def range_sum(self, l, r):               # inclusive
        return self.prefix_sum(r) - self.prefix_sum(l - 1)

    def point_query(self, i):                # value at index i (range-update mode)
        return self.prefix_sum(i) - self.prefix_sum(i - 1)

fw = Fenwick([1, 3, 5])
print(fw.prefix_sum(3))     # 9
print(fw.range_sum(1, 3))   # 9
print(fw.range_sum(2, 3))   # 8
fw.add(2, 5)
print(fw.range_sum(1, 3))   # 14
```

Complexity: build O(n log n) (or O(n) with a linear build trick), each
add/prefix/range query O(log n), space O(n). Note indices are 1-based — use
`i + 1` when mapping from a 0-based array.

## Trie (dict-based nodes)

```python
class TrieNode:
    __slots__ = ('children', 'is_end', 'count')

    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0            # number of words passing through this node


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1
        node.is_end = True

    def search(self, word):          # exact word present
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix):   # any word has this prefix
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True

    def count_prefix(self, prefix):  # how many words have this prefix
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return 0
            node = node.children[ch]
        return node.count

    def count_words(self):           # total number of words stored
        def dfs(node):
            total = 1 if node.is_end else 0
            for child in node.children.values():
                total += dfs(child)
            return total
        return dfs(self.root)

    def longest_common_prefix(self): # LCP of all words in the trie
        node = self.root
        prefix = []
        while len(node.children) == 1 and not node.is_end:
            (ch, node), = node.children.items()
            prefix.append(ch)
        return ''.join(prefix)

t = Trie()
t.insert('apple')
t.insert('app')
print(t.search('apple'))            # True
print(t.search('app'))              # True
print(t.starts_with('app'))         # True
print(t.count_prefix('app'))        # 2
print(t.count_words())              # 2

t2 = Trie()
for w in ('flower', 'flow', 'flight'):
    t2.insert(w)
print(t2.longest_common_prefix())   # 'fl'
```

Complexity: insert/search/starts_with O(L) (L = word length), count_words
O(total characters), space O(total characters). No collisions, but heavier
than a dict-keyed hash approach.

## Disjoint Set Union / Union-Find (DSU)

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    # iterative path compression (fastest — use this)
    def find_iterative(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != x:         # compress path
            nxt = self.parent[x]
            self.parent[x] = root
            x = nxt
        return root

    # recursive path compression (shorter to write)
    def find_recursive(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find_recursive(self.parent[x])
        return self.parent[x]

    def union(self, a, b):                 # union by rank
        ra = self.find_iterative(a)
        rb = self.find_iterative(b)
        if ra == rb:
            return False                   # already connected
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.components -= 1
        return True

    def connected(self, a, b):
        return self.find_iterative(a) == self.find_iterative(b)

dsu = DSU(5)
dsu.union(0, 1)
dsu.union(2, 3)
dsu.union(0, 2)
print(dsu.components)            # 2
print(dsu.connected(1, 3))       # True
print(dsu.connected(0, 4))       # False
```

Complexity: near-constant amortized O(alpha(n)) (inverse Ackermann) per
operation; space O(n). `components` tracks number of connected components.

## sortedcontainers — NOT allowed in interviews

`sortedcontainers.SortedList` is a third-party library. Coding platforms
(LeetCode, HackerRank, Infosys SP DSE) do not provide it. Do not reach for it.

Use instead, depending on the need:

| Need | Replacement |
|---|---|
| sorted order + kth/lower_bound queries | `bisect` on a list (maintain sorted order) |
| always-min/max element | `heapq` |
| ordered dict by key/insertion | `dict` is insertion-ordered; sort keys as needed |
| balanced BST-style (order statistics) | Fenwick over compressed indices / segment tree |

```python
# keep a list sorted with bisect.insort
import bisect
s = []
bisect.insort(s, 5)
bisect.insort(s, 1)
bisect.insort(s, 3)
print(s)                       # [1, 3, 5]
print(bisect.bisect_left(s, 3))   # 1  (first index of 3)
print(bisect.bisect_right(s, 3))  # 2  (index after last 3)
```
