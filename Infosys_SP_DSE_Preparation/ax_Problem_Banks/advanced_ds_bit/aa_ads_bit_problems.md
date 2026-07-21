# Advanced Data Structures & Bit Manipulation — Infosys SP DSE Problem Bank

> 40 curated problems across Segment Trees, Fenwick Trees, Tries, DSU, and Bit Manipulation.
> Each problem includes: statement, approach, complete Python solution, complexity, and trick.

---

## Table of Contents

### Segment Tree / Fenwick Tree (Problems 1–10)
### Trie (Problems 11–18)
### Disjoint Set Union (Problems 19–25)
### Bit Manipulation — Easy (Problems 26–30)
### Bit Manipulation — Medium (Problems 31–37)
### Bit Manipulation — Hard (Problems 38–40)

---

# SEGMENT TREE / FENWICK TREE PROBLEMS

---

## Problem 1: Range Sum Query — Mutable (Fenwick Tree / Binary Indexed Tree)

**Statement:**  
Given an integer array `nums`, handle two types of queries:
1. `update(index, val)` — Set `nums[index] = val`.
2. `sumRange(left, right)` — Return the sum of elements between indices `left` and `right` (inclusive).

Implement the `NumArray` class with these two methods.

**Approach:**  
Use a Binary Indexed Tree (Fenwick Tree). BIT supports point updates and prefix sum queries in O(log n). To get range sum `[l, r]`, compute `prefixSum(r) - prefixSum(l-1)`. The key insight is that BIT stores partial sums in a tree structure where each node `i` is responsible for range `[i - lowbit(i) + 1, i]`. Building the BIT from an array takes O(n), and both update and query are O(log n).

**Solution:**
```python
class NumArray:
    def __init__(self, nums):
        self.n = len(nums)
        self.nums = nums[:]
        self.bit = [0] * (self.n + 1)
        for i, v in enumerate(nums):
            self._add(i + 1, v)

    def _add(self, i, delta):
        while i <= self.n:
            self.bit[i] += delta
            i += i & (-i)

    def _prefix_sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & (-i)
        return s

    def update(self, index, val):
        diff = val - self.nums[index]
        self.nums[index] = val
        self._add(index + 1, diff)

    def sumRange(self, left, right):
        return self._prefix_sum(right + 1) - self._prefix_sum(left)
```

**Complexity:** Build O(n), Update O(log n), Query O(log n), Space O(n)

**Trick:** `i & (-i)` isolates the lowest set bit — this is the core of BIT. Think of BIT as a forest of trees where each node stores a partial sum.

---

## Problem 2: Range Minimum Query (Segment Tree)

**Statement:**  
Given an array `nums` of integers, perform:
1. `update(index, val)` — Update value at index.
2. `query(l, r)` — Return the minimum value in range `[l, r]`.

Implement a class supporting both operations.

**Approach:**  
Build a segment tree where each node stores the minimum of its segment. The tree is built recursively: `tree[node] = min(tree[2*node], tree[2*node+1])`. For update, propagate the change up from the leaf. For query, recursively combine results from overlapping segments. Segment tree is a complete binary tree stored as an array of size 4n.

**Solution:**
```python
class MinSegmentTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [float('inf')] * (4 * self.n)
        self._build(nums, 1, 0, self.n - 1)

    def _build(self, nums, node, start, end):
        if start == end:
            self.tree[node] = nums[start]
            return
        mid = (start + end) // 2
        self._build(nums, 2 * node, start, mid)
        self._build(nums, 2 * node + 1, mid + 1, end)
        self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])

    def update(self, index, val, node=1, start=0, end=None):
        if end is None: end = self.n - 1
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if index <= mid:
            self.update(index, val, 2 * node, start, mid)
        else:
            self.update(index, val, 2 * node + 1, mid + 1, end)
        self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, l, r, node=1, start=0, end=None):
        if end is None: end = self.n - 1
        if r < start or end < l:
            return float('inf')
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return min(
            self.query(l, r, 2 * node, start, mid),
            self.query(l, r, 2 * node + 1, mid + 1, end)
        )
```

**Complexity:** Build O(n), Update O(log n), Query O(log n), Space O(4n)

**Trick:** Allocate 4n space for the tree to avoid index overflow. Segment tree root at index 1 makes child calculations cleaner (left = 2*i, right = 2*i+1).

---

## Problem 3: Count of Range Sum

**Statement:**  
Given an integer array `nums` and two integers `lower` and `upper`, return the number of range sums that lie in `[lower, upper]` inclusive. Range sum `S(i, j)` is defined as the sum of the elements in `nums` between indices `i` and `j` (inclusive), where `i <= j`.

**Approach:**  
Compute prefix sums. The problem becomes: count pairs `(i, j)` where `i < j` and `lower <= prefix[j] - prefix[i] <= upper`. This is equivalent to counting, for each `j`, how many `i < j` satisfy `prefix[j] - upper <= prefix[i] <= prefix[j] - lower`. Use a Fenwick tree after coordinate-compressing all prefix sums. Process prefix sums left to right, querying the BIT for the count of prefix sums in the required range.

**Solution:**
```python
class Solution:
    def countRangeSum(self, nums, lower, upper):
        n = len(nums)
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]

        vals = sorted(set(prefix))
        rank = {v: i + 1 for i, v in enumerate(vals)}
        m = len(vals)
        bit = [0] * (m + 2)

        def add(i):
            while i <= m:
                bit[i] += 1
                i += i & (-i)

        def query(i):
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & (-i)
            return s

        def range_query(lo, hi):
            if lo > hi: return 0
            return query(hi) - query(lo - 1)

        from bisect import bisect_left, bisect_right
        count = 0
        # Process prefix sums; we want pairs (i, j) with i < j
        # Before processing prefix[j], insert prefix[i] for all i < j
        # Then query how many prefix[i] fall in [prefix[j] - upper, prefix[j] - lower]
        # We need to handle this carefully:
        # Insert prefix[0] first (represents sum of empty prefix)
        add(rank[prefix[0]])
        for j in range(1, n + 1):
            target_lo = prefix[j] - upper
            target_hi = prefix[j] - lower
            # Binary search in vals for the range [target_lo, target_hi]
            lo_idx = bisect_left(vals, target_lo) + 1  # 1-indexed for BIT
            hi_idx = bisect_right(vals, target_hi)     # bisect_right is already 1-indexed
            count += range_query(lo_idx, hi_idx)
            add(rank[prefix[j]])

        return count
```

**Complexity:** O(n log n) for sorting + O(n log n) for BIT operations = O(n log n), Space O(n)

**Trick:** Convert the range sum problem into a counting problem on prefix sums. Coordinate compression is essential because prefix sums can be very large but the number of distinct values is at most n+1.

---

## Problem 4: Count Inversions (Fenwick Tree)

**Statement:**  
Given an array `nums`, count the number of pairs `(i, j)` such that `i < j` and `nums[i] > nums[j]`. These are called inversions.

**Approach:**  
Use a Fenwick tree after coordinate compression. Traverse the array from left to right. For each element `nums[j]`, query the BIT to count how many elements already seen are greater than `nums[j]` (i.e., total elements seen minus elements <= nums[j]). Then add `nums[j]` to the BIT. This counts inversions in O(n log n).

**Solution:**
```python
class Solution:
    def countInversions(self, nums):
        if not nums: return 0
        # Coordinate compression
        sorted_vals = sorted(set(nums))
        rank = {v: i + 1 for i, v in enumerate(sorted_vals)}
        m = len(sorted_vals)
        bit = [0] * (m + 2)

        def add(i):
            while i <= m:
                bit[i] += 1
                i += i & (-i)

        def query(i):
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & (-i)
            return s

        inversions = 0
        seen = 0
        for v in nums:
            r = rank[v]
            # Count elements greater than v already seen
            inversions += seen - query(r)
            add(r)
            seen += 1

        return inversions
```

**Complexity:** O(n log n) time, O(n) space

**Trick:** `seen - query(r)` gives elements greater than `v` because `query(r)` counts elements <= `v`. Coordinate compression maps values to ranks 1..m making BIT indexing clean.

---

## Problem 5: Count Smaller Numbers After Self

**Statement:**  
Given an integer array `nums`, return an integer array `counts` where `counts[i]` is the number of smaller elements to the right of `nums[i]`.

**Approach:**  
Traverse from right to left. For each element, query the BIT to count how many elements already inserted are strictly smaller. Then insert the current element. Process right-to-left because we want "after self" — elements to the right are the ones we've already inserted.

**Solution:**
```python
class Solution:
    def countSmaller(self, nums):
        if not nums: return []
        sorted_vals = sorted(set(nums))
        rank = {v: i + 1 for i, v in enumerate(sorted_vals)}
        m = len(sorted_vals)
        bit = [0] * (m + 2)

        def add(i):
            while i <= m:
                bit[i] += 1
                i += i & (-i)

        def query(i):
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & (-i)
            return s

        result = [0] * len(nums)
        for i in range(len(nums) - 1, -1, -1):
            r = rank[nums[i]]
            result[i] = query(r - 1)  # strictly smaller means query(r - 1)
            add(r)

        return result
```

**Complexity:** O(n log n) time, O(n) space

**Trick:** `query(r - 1)` counts strictly smaller elements. Process right-to-left so the BIT only contains elements to the right of current index.

---

## Problem 6: Maximum in Range (Segment Tree)

**Statement:**  
Given an array `nums`, support:
1. `update(index, val)` — Update value at index.
2. `query(l, r)` — Return the maximum value in range `[l, r]`.

Implement both operations efficiently.

**Approach:**  
Identical structure to Problem 2 but storing max instead of min at each node. Each segment tree node stores the maximum of its range. Update propagates upward taking max of children.

**Solution:**
```python
class MaxSegmentTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [float('-inf')] * (4 * self.n)
        self._build(nums, 1, 0, self.n - 1)

    def _build(self, nums, node, start, end):
        if start == end:
            self.tree[node] = nums[start]
            return
        mid = (start + end) // 2
        self._build(nums, 2 * node, start, mid)
        self._build(nums, 2 * node + 1, mid + 1, end)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

    def update(self, index, val, node=1, start=0, end=None):
        if end is None: end = self.n - 1
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if index <= mid:
            self.update(index, val, 2 * node, start, mid)
        else:
            self.update(index, val, 2 * node + 1, mid + 1, end)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, l, r, node=1, start=0, end=None):
        if end is None: end = self.n - 1
        if r < start or end < l:
            return float('-inf')
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return max(
            self.query(l, r, 2 * node, start, mid),
            self.query(l, r, 2 * node + 1, mid + 1, end)
        )
```

**Complexity:** Build O(n), Update O(log n), Query O(log n), Space O(4n)

**Trick:** The segment tree template is the same for min, max, sum — just change the merge operation. This is the power of the segment tree abstraction.

---

## Problem 7: Range Update and Point Query (Fenwick Tree)

**Statement:**  
Given an array of zeros of size `n`, handle two types of queries:
1. `updateRange(l, r, val)` — Add `val` to all elements in range `[l, r]`.
2. `queryPoint(index)` — Return the value at `index`.

**Approach:**  
Use a BIT with a clever trick: to add `val` to range `[l, r]`, do `add(l, val)` and `add(r+1, -val)`. Then `queryPoint(i)` is simply `prefixSum(i)`. This works because the prefix sum at `i` accumulates all the additions whose range covers `i`, and the `-val` at `r+1` stops the accumulation beyond `r`.

**Solution:**
```python
class BITRangeUpdate:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 2)

    def _add(self, i, delta):
        while i <= self.n:
            self.bit[i] += delta
            i += i & (-i)

    def update_range(self, l, r, val):
        self._add(l + 1, val)
        self._add(r + 2, -val)

    def query_point(self, index):
        i = index + 1
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & (-i)
        return s

    def build_from_array(self, nums):
        # Build initial array using range updates (alternative to direct build)
        for i, v in enumerate(nums):
            self.update_range(i, i, v)
```

**Complexity:** Update O(log n), Query O(log n), Space O(n)

**Trick:** The `add(l, val); add(r+1, -val)` trick converts range update + point query into two point updates and a prefix sum query. This is the standard lazy BIT pattern.

---

## Problem 8: Merge Sort with Inversion Count

**Statement:**  
Given an array `nums`, count the number of inversions (pairs where `i < j` but `nums[i] > nums[j]`) using a modified merge sort.

**Approach:**  
During merge sort's merge step, when an element from the right half is placed before elements from the left half, all remaining left-half elements form inversions with it. Count these during merge. This is the classic divide-and-conquer approach to counting inversions.

**Solution:**
```python
class Solution:
    def countInversions(self, nums):
        def merge_sort(arr):
            if len(arr) <= 1:
                return arr, 0
            mid = len(arr) // 2
            left, left_inv = merge_sort(arr[:mid])
            right, right_inv = merge_sort(arr[mid:])
            merged = []
            inversions = left_inv + right_inv
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    # All remaining elements in left are greater than right[j]
                    inversions += len(left) - i
                    j += 1
            merged.extend(left[i:])
            merged.extend(right[j:])
            return merged, inversions

        _, count = merge_sort(nums)
        return count
```

**Complexity:** O(n log n) time, O(n) space

**Trick:** The key insight is that merge sort naturally identifies inversions — whenever we pick from the right array before the left array, all remaining left elements form inversions. This gives O(n log n) which beats the O(n²) brute force.

---

## Problem 9: Reverse Pairs

**Statement:**  
Given an array `nums`, return the number of pairs `(i, j)` where `i < j` and `nums[i] > 2 * nums[j]`.

**Approach:**  
Modify merge sort. During the merge step, before merging, count pairs where left element > 2 * right element using two pointers. Since both halves are sorted, for each left element, find how many right elements satisfy the condition. Then merge as usual.

**Solution:**
```python
class Solution:
    def reversePairs(self, nums):
        def merge_sort(arr):
            if len(arr) <= 1:
                return arr, 0
            mid = len(arr) // 2
            left, lc = merge_sort(arr[:mid])
            right, rc = merge_sort(arr[mid:])
            count = lc + rc

            # Count reverse pairs: left[i] > 2 * right[j]
            j = 0
            for i in range(len(left)):
                while j < len(right) and left[i] > 2 * right[j]:
                    j += 1
                count += j

            # Merge
            merged = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i]); i += 1
                else:
                    merged.append(right[j]); j += 1
            merged.extend(left[i:])
            merged.extend(right[j:])
            return merged, count

        _, result = merge_sort(nums)
        return result
```

**Complexity:** O(n log n) time, O(n) space

**Trick:** Two-pointer counting during merge avoids O(n²). Since both halves are sorted, the `j` pointer only moves forward — total work across all merge steps is O(n log n). The condition `left[i] > 2 * right[j]` must use `2 * right[j]` to handle overflow — use `left[i] > 2 * right[j]` with Python's arbitrary precision integers.

---

## Problem 10: Kth Number in a Stream

**Statement:**  
Design a data structure that receives a stream of integers and at any point can return the k-th smallest number seen so far.

Implement the `KthLargest` class:
- `KthLargest(k, nums)` — Initializes with `k` and initial stream `nums`.
- `add(val)` — Adds `val` to the stream and returns the k-th largest element.

**Approach:**  
Use a min-heap of size `k`. The heap always contains the `k` largest elements seen so far. The root (minimum of the heap) is the k-th largest. When a new element arrives, if the heap has fewer than `k` elements or the new element is larger than the heap's minimum, push it and pop the minimum if size exceeds `k`.

**Solution:**
```python
import heapq

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = []
        for num in nums:
            self._add_to_heap(num)

    def _add_to_heap(self, val):
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, val)
        elif val > self.heap[0]:
            heapq.heapreplace(self.heap, val)

    def add(self, val):
        self._add_to_heap(val)
        return self.heap[0]

# Alternative: Fenwick Tree approach for multiple kth queries on static stream
class KthInStreamBIT:
    def __init__(self, nums):
        self.nums = sorted(set(nums))
        self.bit = [0] * (len(self.nums) + 2)
        self.counts = {}
        for v in nums:
            self._insert(v)

    def _rank(self, v):
        from bisect import bisect_left
        return bisect_left(self.nums, v) + 1

    def _add(self, i, delta):
        while i < len(self.bit):
            self.bit[i] += delta
            i += i & (-i)

    def _query(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & (-i)
        return s

    def _insert(self, v):
        self.counts[v] = self.counts.get(v, 0) + 1
        self._add(self._rank(v), 1)

    def kth_smallest(self, k):
        lo, hi = 0, len(self.nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            cnt = self._query(mid + 1)
            if cnt >= k:
                hi = mid - 1
            else:
                lo = mid + 1
        return self.nums[lo]
```

**Complexity:** Heap approach: Init O(n log k), Add O(log k). BIT approach: Insert O(log n), Kth query O(log² n). Space O(k) for heap, O(n) for BIT.

**Trick:** The heap approach is simple and O(log k) per addition. The BIT approach uses binary search on prefix sums to find the k-th element — this generalizes to the "kth element in stream" problem.

---

# TRIE PROBLEMS

---

## Problem 11: Implement Trie (Prefix Tree)

**Statement:**  
Implement a trie with:
1. `insert(word)` — Inserts a word.
2. `search(word)` — Returns True if the word is in the trie.
3. `startsWith(prefix)` — Returns True if any word in the trie has the given prefix.

**Approach:**  
Each node is a dictionary of children plus a boolean `is_end`. `search` traverses character by character and checks `is_end` at the last node. `startsWith` is identical but doesn't check `is_end`.

**Solution:**
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

    def startsWith(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
```

**Complexity:** Insert/Search/StartsWith all O(m) where m = word length. Space O(N*M) total for N words of average length M.

**Trick:** `search` checks `is_end` while `startsWith` does not — this is the only difference. Trie enables O(m) prefix operations instead of O(n*m) linear scan.

---

## Problem 12: Search Suggestions System

**Statement:**  
Given a list of products (strings) and a search word, design a system that returns at most 3 product names after each character of the search word is typed. Suggestions should be lexicographically smallest.

**Approach:**  
Sort the products. Build a trie from sorted products. For each prefix of the search word (after typing each character), traverse the trie and do a DFS to collect up to 3 lexicographically smallest completions. Since products are sorted, the DFS naturally visits them in order.

**Solution:**
```python
class Solution:
    def suggestedProducts(self, products, searchWord):
        products.sort()
        root = {}
        for prod in products:
            node = root
            for ch in prod:
                if ch not in node:
                    node[ch] = {}
                node = node[ch]
            node['$'] = prod  # mark end with the word itself

        result = []
        node = root
        prefix = ""
        found = True
        for ch in searchWord:
            prefix += ch
            if found and ch in node:
                node = node[ch]
                # DFS to collect up to 3 words
                suggestions = []
                stack = [node]
                while stack and len(suggestions) < 3:
                    curr = stack.pop()
                    if '$' in curr:
                        suggestions.append(curr['$'])
                    # Pop children in reverse alphabetical order
                    for c in sorted(curr.keys(), reverse=True):
                        if c != '$':
                            stack.append(curr[c])
                result.append(suggestions)
            else:
                found = False
                result.append([])

        return result
```

**Complexity:** O(n * m * log m) to build trie (sort dominates), O(L * 3 * m) per query where L = searchWord length. Space O(n * m).

**Trick:** Storing the full word at the end node (`$`) makes DFS collection trivial. Sort products first so DFS gives lexicographic order naturally. The `found` flag avoids re-traversing failed prefixes.

---

## Problem 13: Word Search II (Trie + Backtracking)

**Statement:**  
Given an `m x n` board of characters and a list of words, return all words from the list that can be found on the board. A word can be formed by tracing adjacent cells (horizontally or vertically), and each cell may only be used once per word.

**Approach:**  
Build a trie from all words. For each cell on the board, start DFS. At each step, check if the current path exists in the trie — if not, prune. If we reach a trie node that marks the end of a word, add it to results. After exploring, backtrack by restoring the cell's character. This avoids checking every word independently.

**Solution:**
```python
class Solution:
    def findWords(self, board, words):
        trie = {}
        for word in words:
            node = trie
            for ch in word:
                if ch not in node:
                    node[ch] = {}
                node = node[ch]
            node['#'] = word

        result = []
        rows, cols = len(board), len(board[0])

        def dfs(r, c, node):
            ch = board[r][c]
            if ch not in node:
                return
            node = node[ch]
            if '#' in node:
                result.append(node['#'])
                del node['#']  # avoid duplicates

            board[r][c] = '.'  # mark visited
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '.':
                    dfs(nr, nc, node)
            board[r][c] = ch  # restore

        for r in range(rows):
            for c in range(cols):
                dfs(r, c, trie)

        return result
```

**Complexity:** O(M * N * 4^L) worst case per cell where L = max word length, but trie pruning makes it much faster in practice. Space O(W * L) for trie.

**Trick:** Delete the `#` key after finding a word to avoid duplicate results. Marking visited cells with `'.'` avoids O(n) visited set overhead. The trie prunes entire branches — if no word starts with the current path, we stop immediately.

---

## Problem 14: Maximum XOR of Two Numbers in an Array

**Statement:**  
Given an array `nums`, find the maximum `nums[i] XOR nums[j]` where `0 <= i, j < n`.

**Approach:**  
Build a trie of all numbers as 31-bit binary strings (MSB first). For each number, greedily traverse the trie trying to take the opposite bit at each position — this maximizes XOR. If the opposite bit exists in the trie, go that way; otherwise go the same bit way. Track the maximum XOR found.

**Solution:**
```python
class Solution:
    def findMaximumXOR(self, nums):
        # Build trie
        trie = {}
        for num in nums:
            node = trie
            for i in range(31, -1, -1):
                bit = (num >> i) & 1
                if bit not in node:
                    node[bit] = {}
                node = node[bit]

        # For each number, find max XOR using trie
        max_xor = 0
        for num in nums:
            node = trie
            curr_xor = 0
            for i in range(31, -1, -1):
                bit = (num >> i) & 1
                want = 1 - bit  # greedy: try opposite bit
                if want in node:
                    curr_xor |= (1 << i)
                    node = node[want]
                else:
                    node = node[bit]
            max_xor = max(max_xor, curr_xor)

        return max_xor
```

**Complexity:** O(32 * n) = O(n) time, O(32 * n) space

**Trick:** Greedy bit-by-bit from MSB works because if we can set bit `i` in the XOR, it's always better regardless of lower bits. The trie enables O(1) per bit lookup instead of checking all pairs.

---

## Problem 15: Map Sum Pairs

**Statement:**  
Implement a map that stores key-value pairs and supports:
1. `insert(key, val)` — Insert or update a key-value pair.
2. `sum(prefix)` — Return the sum of all values whose keys start with the given prefix.

**Approach:**  
Use a trie where each node stores the cumulative sum of all values in its subtree. When inserting, traverse/create nodes and update sums along the path. For `sum(prefix)`, traverse to the prefix node and return its stored sum.

**Solution:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.sum = 0

class MapSum:
    def __init__(self):
        self.root = TrieNode()
        self.map = {}  # track existing keys for updates

    def insert(self, key, val):
        diff = val - self.map.get(key, 0)
        self.map[key] = val
        node = self.root
        for ch in key:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.sum += diff

    def sum(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return 0
            node = node.children[ch]
        return node.sum
```

**Complexity:** Insert O(m), Sum O(m) where m = key length. Space O(total characters in all keys).

**Trick:** Store the old value and compute the `diff` when updating — this avoids needing to remove the old value's contribution from the trie. The `map` dictionary tracks current values for quick diff computation.

---

## Problem 16: Replace Words (Shortest Prefix)

**Statement:**  
Given a list of root words (dictionary) and a sentence (space-separated words), replace each word in the sentence with its shortest root — the root that is a prefix of the word. If no root exists, keep the original word.

**Approach:**  
Build a trie from all root words. For each word in the sentence, traverse the trie character by character. The first time we encounter a node marked as end-of-root, that's the shortest prefix. If we exhaust the word without finding a root, keep the original.

**Solution:**
```python
class Solution:
    def replaceWords(self, dictionary, sentence):
        trie = {}
        for root in dictionary:
            node = trie
            for ch in root:
                if ch not in node:
                    node[ch] = {}
                node = node[ch]
            node['#'] = True  # mark end of root

        def find_shortest_root(word):
            node = trie
            for i, ch in enumerate(word):
                if '#' in node:
                    return word[:i]  # shortest root found
                if ch not in node:
                    return word  # no root exists
                node = node[ch]
            return word

        return ' '.join(find_shortest_root(w) for w in sentence.split())

# Alternative using Trie class
class Solution2:
    def replaceWords(self, dictionary, sentence):
        roots = set(dictionary)
        words = sentence.split()
        result = []
        for word in words:
            replaced = word
            for i in range(1, len(word)):
                if word[:i] in roots:
                    replaced = word[:i]
                    break
            result.append(replaced)
        return ' '.join(result)
```

**Complexity:** Trie approach: O(D * R + S * W) where D = dictionary size, R = avg root length, S = sentence words, W = max word length. Set approach: O(S * W²). Space O(D * R).

**Trick:** The set-based approach works because we only need prefix matching — for each word, try all possible prefixes and check if it's in the set. It's simpler and fast enough for most cases. Trie is more elegant.

---

## Problem 17: Longest Word in Dictionary

**Statement:**  
Given a list of words, find the longest word that can be built one character at a time from other words in the list. Return the lexicographically smallest if there are ties.

**Approach:**  
Sort words by length, then lexicographically. Use a set of buildable words, starting with all single-letter words. For each word, if its prefix (all but last character) is buildable, then the word itself is buildable. Track the longest buildable word.

**Solution:**
```python
class Solution:
    def longestWord(self, words):
        words.sort()
        buildable = set()
        result = ""

        for word in words:
            if len(word) == 1 or word[:-1] in buildable:
                buildable.add(word)
                if len(word) > len(result):
                    result = word

        return result

# Trie-based approach
class Solution2:
    def longestWord(self, words):
        trie = {}
        for word in words:
            node = trie
            for ch in word:
                if ch not in node:
                    node[ch] = {}
                node = node[ch]
            node['#'] = word

        def dfs(node):
            best = node.get('#', '')
            for c in sorted(node.keys()):
                if c == '#': continue
                child_word = dfs(node[c])
                if child_word and len(child_word) + 1 > len(best):
                    best = node[c].get('#', '') + child_word
                elif child_word and len(child_word) + 1 == len(best):
                    candidate = node[c].get('#', '') + child_word
                    best = min(best, candidate)
            return best

        # Simplified: track words buildable one char at a time
        result = ""
        for word in sorted(words, key=lambda w: (len(w), w)):
            if len(word) == 1 or word[:-1] in buildable_set:
                buildable_set.add(word)
                result = word
        return result

# Cleanest approach
class Solution3:
    def longestWord(self, words):
        words.sort(key=lambda w: (len(w), w))
        valid = set([""])
        result = ""
        for word in words:
            if word[:-1] in valid:
                valid.add(word)
                result = word
        return result
```

**Complexity:** O(n * L * log n) for sorting + O(n * L) for checking. Space O(n * L).

**Trick:** Sort by length then lex order. The empty string `""` is always buildable. `word[:-1] in valid` checks if the prefix was buildable — if yes, this word extends the chain. The last word assigned to `result` is the answer since sorting ensures longest + smallest.

---

## Problem 18: Stream of Characters

**Statement:**  
Design a stream that receives characters one at a time and returns True whenever the suffix of the stream (from some point to end) forms a word from a given dictionary.

**Approach:**  
Build a trie from the dictionary words in reverse. For each incoming character, append it to a buffer and search the trie from the most recent character backward. If we find a complete word in the trie while traversing backward through the buffer, return True. This avoids checking every possible suffix.

**Solution:**
```python
class StreamChecker:
    def __init__(self, words):
        self.trie = {}
        self.buffer = []
        max_len = 0
        for word in words:
            max_len = max(max_len, len(word))
            node = self.trie
            for ch in reversed(word):
                if ch not in node:
                    node[ch] = {}
                node = node[ch]
            node['#'] = True  # end marker
        self.max_len = max_len

    def query(self, letter):
        self.buffer.append(letter)
        # Keep buffer bounded
        if len(self.buffer) > self.max_len:
            self.buffer.pop(0)
        # Search from most recent character backward
        node = self.trie
        for ch in reversed(self.buffer):
            if ch not in node:
                return False
            node = node[ch]
            if '#' in node:
                return True
        return False
```

**Complexity:** Build O(W * L), Query O(min(buffer_size, max_word_len)) per character. Space O(W * L + max_word_len).

**Trick:** Reverse words in trie and search from newest to oldest character — this turns suffix matching into prefix matching. The bounded buffer (`max_len`) prevents memory growth. This is a clever reversal that avoids exponential suffix checking.

---

# DISJOINT SET UNION PROBLEMS

---

## Problem 19: Number of Provinces

**Statement:**  
Given an `n x n` adjacency matrix `isConnected` where `isConnected[i][j] = 1` means cities `i` and `j` are directly connected, return the number of provinces (connected components).

**Approach:**  
Use Union-Find. Initialize each city as its own parent. For each pair `(i, j)` where `isConnected[i][j] = 1`, union them. The number of distinct roots is the number of provinces. Path compression and union by rank keep operations nearly O(1).

**Solution:**
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
        if px == py: return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True

class Solution:
    def findCircleNum(self, isConnected):
        n = len(isConnected)
        dsu = DSU(n)
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j] == 1:
                    dsu.union(i, j)
        return dsu.components
```

**Complexity:** O(n² * α(n)) ≈ O(n²) time, O(n) space where α is the inverse Ackermann function.

**Trick:** Only iterate `j > i` since the matrix is symmetric. `dsu.components` tracks the count without needing a separate pass. Union-Find with path compression + rank gives near-constant amortized time per operation.

---

## Problem 20: Redundant Connection

**Statement:**  
Given a tree (connected graph with n nodes and n-1 edges) with one extra edge added, find the edge that can be removed so the graph remains a tree. If multiple edges qualify, return the one that appears last in the input.

**Approach:**  
Use Union-Find. Process edges in order. For each edge, if both endpoints are already connected (same root), this edge is redundant — it's our answer. Otherwise, union them. The last redundant edge found is the answer.

**Solution:**
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

class Solution:
    def findRedundantConnection(self, edges):
        dsu = DSU(len(edges))
        for u, v in edges:
            if not dsu.union(u, v):
                return [u, v]
```

**Complexity:** O(n * α(n)) ≈ O(n) time, O(n) space

**Trick:** The redundant edge is the one where both endpoints are already in the same component when we try to add it. Since we process edges in order and the graph was originally a tree, exactly one edge will fail the union.

---

## Problem 21: Accounts Merge

**Statement:**  
Given a list of accounts where each account has a name and a list of emails, merge accounts that share at least one email. Return the merged accounts with the name and sorted unique emails.

**Approach:**  
Map each email to an account index. Use Union-Find to merge accounts that share emails. After processing all emails, group emails by their root parent. Build result by getting the name from the root account and sorting the emails.

**Solution:**
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

class Solution:
    def accountsMerge(self, accounts):
        dsu = DSU(len(accounts))
        email_to_id = {}
        for i, account in enumerate(accounts):
            for email in account[1:]:
                if email in email_to_id:
                    dsu.union(i, email_to_id[email])
                email_to_id[email] = i

        from collections import defaultdict
        groups = defaultdict(set)
        for email, i in email_to_id.items():
            groups[dsu.find(i)].add(email)

        result = []
        for i, emails in groups.items():
            result.append([accounts[i][0]] + sorted(emails))
        return result
```

**Complexity:** O(N * K * α(N)) where N = accounts, K = max emails per account. Space O(N * K).

**Trick:** `email_to_id` maps each email to its account index. When we see an email belonging to two accounts, we union those accounts. After all unions, `dsu.find(i)` gives the canonical account for account `i`.

---

## Problem 22: Number of Connected Components in an Undirected Graph

**Statement:**  
Given `n` nodes labeled from 0 to n-1 and a list of undirected edges, return the number of connected components.

**Approach:**  
Use Union-Find. Initialize each node as its own component. For each edge, union the two endpoints and decrement component count. Return the final count.

**Solution:**
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.count -= 1
        return True

class Solution:
    def countComponents(self, n, edges):
        dsu = DSU(n)
        for u, v in edges:
            dsu.union(u, v)
        return dsu.count
```

**Complexity:** O(E * α(N)) ≈ O(E) time, O(N) space

**Trick:** Maintaining `count` during union avoids a final pass over all nodes. Each successful union reduces the component count by exactly 1.

---

## Problem 23: Graph Valid Tree

**Statement:**  
Given `n` nodes labeled 0 to n-1 and a list of edges, determine if the graph forms a valid tree. A valid tree is connected and has no cycles.

**Approach:**  
A graph is a valid tree if and only if:
1. It has exactly `n - 1` edges (otherwise it's either disconnected or has a cycle).
2. All nodes are connected (one component).

Use Union-Find. If any edge connects two already-connected nodes, there's a cycle. If we process all edges without finding a cycle and the component count is 1, it's a valid tree.

**Solution:**
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

class Solution:
    def validTree(self, n, edges):
        if len(edges) != n - 1:
            return False
        dsu = DSU(n)
        for u, v in edges:
            if not dsu.union(u, v):
                return False
        return True
```

**Complexity:** O(E * α(N)) ≈ O(E) time, O(N) space

**Trick:** `len(edges) != n - 1` is a quick rejection — a tree with n nodes must have exactly n-1 edges. If it passes, just check for cycles using DSU.

---

## Problem 24: Number of Islands II (Dynamic)

**Statement:**  
Given an `m x n` 2D grid initially full of water, and a list of positions to add land one at a time, return the number of islands after each addition. An island is formed by connecting adjacent land cells (4-directionally).

**Approach:**  
Use Union-Find. Initially, all cells are water (no components). When adding land at `(r, c)`:
1. Create a new component (increment count).
2. Check all 4 neighbors — if a neighbor is land, union them and decrement count for each successful union.

This dynamically tracks connected components as land is added.

**Solution:**
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

class Solution:
    def numIslands2(self, m, n, positions):
        dsu = DSU(m * n)
        land = set()
        count = 0
        result = []

        for r, c in positions:
            pos = r * n + c
            if pos in land:
                result.append(count)
                continue
            land.add(pos)
            count += 1
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc
                neighbor = nr * n + nc
                if 0 <= nr < m and 0 <= nc < n and neighbor in land:
                    if dsu.union(pos, neighbor):
                        count -= 1
            result.append(count)

        return result
```

**Complexity:** O(K * α(M*N)) where K = number of positions. Space O(M*N).

**Trick:** Map 2D coordinates to 1D: `pos = r * n + c`. Only union with existing land cells (check `land` set). The `land` set tracks which positions have been added, preventing duplicate processing.

---

## Problem 25: Smallest String With Swaps

**Statement:**  
Given a string `s` and a list of pairs `[i, j]` where you can swap characters at positions `i` and `j` any number of times, return the lexicographically smallest string you can obtain.

**Approach:**  
Use Union-Find to group all positions that are connected through swaps. Within each group, the characters can be rearranged freely. To get the lexicographically smallest result, sort the characters in each group and place them back in the sorted order of positions within that group.

**Solution:**
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

class Solution:
    def smallestStringWithSwaps(self, s, pairs):
        n = len(s)
        dsu = DSU(n)
        for i, j in pairs:
            dsu.union(i, j)

        from collections import defaultdict
        groups = defaultdict(list)
        for i in range(n):
            groups[dsu.find(i)].append(i)

        result = list(s)
        for indices in groups.values():
            chars = sorted(result[i] for i in indices)
            for idx, ch in zip(sorted(indices), chars):
                result[idx] = ch

        return ''.join(result)
```

**Complexity:** O(n log n + K * α(n)) where K = pairs. Space O(n).

**Trick:** Within a connected component, all permutations of characters are achievable. Sort characters and sort positions, then place the i-th smallest character at the i-th smallest position — this gives the lexicographically smallest arrangement.

---

# BIT MANIPULATION — EASY PROBLEMS

---

## Problem 26: Single Number

**Statement:**  
Given a non-empty array where every element appears twice except one, find the single number. Your solution should have O(n) time and O(1) space.

**Approach:**  
XOR all elements. Since `a ^ a = 0` and `a ^ 0 = a`, all pairs cancel out and the remaining value is the single number. XOR is commutative and associative, so order doesn't matter.

**Solution:**
```python
class Solution:
    def singleNumber(self, nums):
        result = 0
        for num in nums:
            result ^= num
        return result

# One-liner
# return functools.reduce(lambda a, b: a ^ b, nums)
```

**Complexity:** O(n) time, O(1) space

**Trick:** XOR is the "parity" operation — it flips a bit an odd number of times. Paired elements cancel (even flips = 0), single element survives (odd flips = itself).

---

## Problem 27: Number of 1 Bits (Hamming Weight)

**Statement:**  
Write a function that takes an unsigned integer and returns the number of '1' bits it has (also known as the Hamming weight).

**Approach:**  
Use Brian Kernighan's algorithm: `n & (n - 1)` clears the lowest set bit. Count how many times we can do this before n becomes 0. This is faster than checking each bit individually because it skips zeros.

**Solution:**
```python
class Solution:
    def hammingWeight(self, n):
        count = 0
        while n:
            n &= (n - 1)  # clear lowest set bit
            count += 1
        return count

# Alternative: check each bit
class Solution2:
    def hammingWeight(self, n):
        return bin(n).count('1')

# Alternative: bit by bit
class Solution3:
    def hammingWeight(self, n):
        count = 0
        while n:
            count += n & 1
            n >>= 1
        return count
```

**Complexity:** O(k) where k = number of set bits (Brian Kernighan's), O(32) = O(1) for bit-by-bit. Space O(1).

**Trick:** `n & (n-1)` is a classic bit trick that removes the lowest set bit. For example: `1100 & 1011 = 1000`. The loop runs exactly as many times as there are set bits, which is faster than iterating all 32 bits when the number is sparse.

---

## Problem 28: Counting Bits

**Statement:**  
Given an integer `n`, return an array `ans` of length `n + 1` where `ans[i]` is the number of 1s in the binary representation of `i`.

**Approach:**  
Use dynamic programming: `ans[i] = ans[i >> 1] + (i & 1)`. The number of 1 bits in `i` equals the number of 1 bits in `i/2` (right shift) plus the last bit. Alternatively, `ans[i] = ans[i & (i-1)] + 1` — the count for `i` equals the count for `i` with its lowest set bit cleared, plus 1.

**Solution:**
```python
class Solution:
    def countBits(self, n):
        ans = [0] * (n + 1)
        for i in range(1, n + 1):
            ans[i] = ans[i >> 1] + (i & 1)
        return ans

# Alternative using Brian Kernighan's trick
class Solution2:
    def countBits(self, n):
        ans = [0] * (n + 1)
        for i in range(1, n + 1):
            ans[i] = ans[i & (i - 1)] + 1
        return ans
```

**Complexity:** O(n) time, O(n) space

**Trick:** `ans[i & (i-1)] + 1` is elegant — `i & (i-1)` removes the lowest set bit, and we know the popcount of that value from DP. This builds on previously computed results with no wasted work.

---

## Problem 29: Reverse Bits

**Statement:**  
Reverse the bits of a given 32-bit unsigned integer.

**Approach:**  
Process bits from LSB to MSB. For each bit in the input, shift the result left (making room) and add the current bit. After processing all 32 bits, the result has the reversed bits.

**Solution:**
```python
class Solution:
    def reverseBits(self, n):
        result = 0
        for _ in range(32):
            result = (result << 1) | (n & 1)
            n >>= 1
        return result

# Bit manipulation in chunks (divide and conquer)
class Solution2:
    def reverseBits(self, n):
        n = ((n & 0x55555555) << 1)  | ((n >> 1) & 0x55555555)
        n = ((n & 0x33333333) << 2)  | ((n >> 2) & 0x33333333)
        n = ((n & 0x0F0F0F0F) << 4)  | ((n >> 4) & 0x0F0F0F0F)
        n = ((n & 0x00FF00FF) << 8)  | ((n >> 8) & 0x00FF00FF)
        n = ((n & 0x0000FFFF) << 16) | ((n >> 16) & 0x0000FFFF)
        return n
```

**Complexity:** O(1) — always 32 iterations. Space O(1).

**Trick:** The chunk approach swaps halves at each power-of-2 level. 0x55555555 = alternating 10 pattern (swap adjacent bits), 0x33333333 = 0011 pattern (swap pairs), etc. This is O(log 32) = O(1) with constant factors.

---

## Problem 30: Power of Two

**Statement:**  
Given an integer `n`, return True if it is a power of two (i.e., n = 2^k for some integer k).

**Approach:**  
A power of two in binary has exactly one set bit: 1, 10, 100, 1000, etc. So `n > 0` and `n & (n - 1) == 0` means it's a power of two. `n & (n-1)` clears the lowest set bit — if nothing remains, there was exactly one set bit.

**Solution:**
```python
class Solution:
    def isPowerOfTwo(self, n):
        return n > 0 and (n & (n - 1)) == 0

# Alternative: count bits
class Solution2:
    def isPowerOfTwo(self, n):
        return n > 0 and bin(n).count('1') == 1

# Alternative: using log
import math
class Solution3:
    def isPowerOfTwo(self, n):
        if n <= 0: return False
        log = math.log2(n)
        return log == int(log)
```

**Complexity:** O(1) time, O(1) space

**Trick:** `n & (n-1) == 0` is the canonical one-liner for power-of-two check. The `n > 0` check is essential because `(-n) & (-n-1)` doesn't work as expected for negative numbers.

---

# BIT MANIPULATION — MEDIUM PROBLEMS

---

## Problem 31: Single Number II

**Statement:**  
Given an integer array where every element appears exactly three times except one element which appears exactly once, find the single element. Solve without using extra memory in linear time.

**Approach:**  
Count the number of set bits at each position across all numbers. If a bit position has a total count divisible by 3, the single number has a 0 there; otherwise, it has a 1. Use two variables `ones` and `twos` to track bits appearing once and twice respectively.

**Solution:**
```python
class Solution:
    def singleNumber(self, nums):
        ones = twos = 0
        for num in nums:
            ones = (ones ^ num) & ~twos
            twos = (twos ^ num) & ~ones
        return ones

# Alternative: count bits at each position
class Solution2:
    def singleNumber(self, nums):
        result = 0
        for i in range(32):
            bit_count = sum((num >> i) & 1 for num in nums)
            if bit_count % 3 != 0:
                result |= (1 << i)
        # Handle negative numbers
        return result if result < (1 << 31) else result - (1 << 32)
```

**Complexity:** O(n) time, O(1) space

**Trick:** The `ones/twos` state machine: a bit goes through states 0 → 1 → 2 → 0 as it appears. `ones` tracks bits seen once, `twos` tracks bits seen twice. The `& ~twos` in the `ones` update prevents bits in `twos` from being counted again. This generalizes to "every element appears k times" using k state variables.

---

## Problem 32: Maximum Product of Word Lengths

**Statement:**  
Given a list of words, return the maximum value of `len(word[i]) * len(word[j])` where the two words share no common letters.

**Approach:**  
Represent each word as a 26-bit mask where bit `i` is set if the word contains the i-th letter. Two words share no letters if `(mask[i] & mask[j]) == 0`. Check all pairs and track the maximum product.

**Solution:**
```python
class Solution:
    def maxProduct(self, words):
        n = len(words)
        masks = [0] * n
        for i, word in enumerate(words):
            for ch in word:
                masks[i] |= 1 << (ord(ch) - ord('a'))

        max_prod = 0
        for i in range(n):
            for j in range(i + 1, n):
                if masks[i] & masks[j] == 0:
                    max_prod = max(max_prod, len(words[i]) * len(words[j]))
        return max_prod
```

**Complexity:** O(n² + n*L) where L = avg word length. Space O(n).

**Trick:** Bit masks reduce "do these words share a letter?" to a single AND operation. Building masks is O(n*L) and pair checking is O(n²) — much faster than checking character intersections for each pair.

---

## Problem 33: Bitwise AND of Numbers Range

**Statement:**  
Given two integers `left` and `right`, return the bitwise AND of all numbers in the range `[left, right]` (inclusive).

**Approach:**  
Find the common prefix of `left` and `right` in binary. Any bit that differs between `left` and `right` will be 0 in the final AND (because for any differing bit, there exist numbers in the range with both 0 and 1 at that position). Shift both numbers right until they're equal — count the shifts, then shift back left.

**Solution:**
```python
class Solution:
    def rangeBitwiseAnd(self, left, right):
        shift = 0
        while left != right:
            left >>= 1
            right >>= 1
            shift += 1
        return left << shift

# Alternative: clear rightmost bit of right
class Solution2:
    def rangeBitwiseAnd(self, left, right):
        while right > left:
            right &= (right - 1)  # clear lowest set bit
        return right
```

**Complexity:** O(log n) time, O(1) space

**Trick:** `right &= (right - 1)` clears the lowest set bit of `right`. Repeat until `right <= left`. This works because any bit that "turns over" (goes from 1 to 0 with carries) in the range `[left, right]` contributes 0 to the AND. The common prefix bits survive.

---

## Problem 34: UTF-8 Validation

**Statement:**  
Given an integer array representing bytes of a UTF-8 encoded string, determine if it is valid.

**Approach:**  
UTF-8 encoding rules:
- 1-byte: `0xxxxxxx`
- 2-byte: `110xxxxx 10xxxxxx`
- 3-byte: `1110xxxx 10xxxxxx 10xxxxxx`
- 4-byte: `11110xxx 10xxxxxx 10xxxxxx 10xxxxxx`

Count the leading 1-bits to determine the number of bytes. Then verify that the correct number of continuation bytes (starting with `10`) follow.

**Solution:**
```python
class Solution:
    def validUtf8(self, data):
        count = 0
        for byte in data:
            if count == 0:
                if byte >> 7 == 0:
                    count = 0
                elif byte >> 5 == 0b110:
                    count = 1
                elif byte >> 4 == 0b1110:
                    count = 2
                elif byte >> 3 == 0b11110:
                    count = 3
                else:
                    return False
            else:
                if byte >> 6 != 0b10:
                    return False
                count -= 1
        return count == 0
```

**Complexity:** O(n) time, O(1) space

**Trick:** Use right-shift + comparison instead of masking: `byte >> 5 == 0b110` checks if the top 3 bits are `110`. The `count` variable tracks remaining continuation bytes. After processing all bytes, `count` must be 0 (no incomplete sequence).

---

## Problem 35: Bitwise XOR of All Pairings

**Statement:**  
Given two integer arrays `nums1` and `nums2`, return the XOR of all possible pairings `(nums1[i], nums2[j])`. A pairing consists of taking one element from each array.

**Approach:**  
The XOR of all pairings equals `(XOR of nums1) repeated len(nums2) times XOR'd with (XOR of nums2) repeated len(nums1) times`. If an element appears an even number of times in the pairing XOR, it cancels out. So the result is `(xor1 if len(nums2) % 2 else 0) ^ (xor2 if len(nums1) % 2 else 0)`.

**Solution:**
```python
class Solution:
    def xorAllNums(self, nums1, nums2):
        xor1 = 0
        for x in nums1:
            xor1 ^= x
        xor2 = 0
        for x in nums2:
            xor2 ^= x
        # Each nums1 element appears len(nums2) times, each nums2 element appears len(nums1) times
        return (xor1 if len(nums2) % 2 else 0) ^ (xor2 if len(nums1) % 2 else 0)
```

**Complexity:** O(n + m) time, O(1) space

**Trick:** This is a pure math insight — you don't need to enumerate pairs. Each element from `nums1` participates in `len(nums2)` pairs, and each element from `nums2` participates in `len(nums1)` pairs. Since `x ^ x = 0`, odd occurrences contribute the value and even occurrences cancel out.

---

## Problem 36: Minimum One Bit Operations to Make Integers Zero

**Statement:**  
Given an integer `n`, return the minimum number of operations to reduce it to 0. In one operation, you can flip any bit at position `k` if all lower bits (0 to k-1) are 0.

**Approach:**  
This follows the Gray code sequence. The answer for `n` is the sum of `C(n)` where the operation follows: convert `n` to Gray code, then the answer is the value of that Gray code interpreted as a regular number. Alternatively, the recurrence is: `f(n) = f(n - 2^k) + (2^(k+1) - 1)` where `2^k` is the highest set bit of `n`.

**Solution:**
```python
class Solution:
    def minimumOneBitOperations(self, n):
        # Convert to Gray code, then sum the bit values
        result = 0
        while n:
            result ^= n
            n >>= 1
        return result

# Alternative: explicit recurrence
class Solution2:
    def minimumOneBitOperations(self, n):
        # f(n) = 2*f(n - highest_bit(n)) + (highest_bit(n) - 1)... 
        # Actually, the Gray code approach is simpler and proven correct
        result = 0
        mask = n
        while mask:
            result ^= mask
            mask >>= 1
        return result
```

**Complexity:** O(log n) time, O(1) space

**Trick:** The answer is `n ^ (n >> 1) ^ (n >> 2) ^ ... ^ 1`, which equals `n ^ (n >> 1) ^ (n >> 2) ^ ...`. This is the "Gray code sum" — it appears in the HackerRank problem and the sequence is A006068 in OEIS. The loop `result ^= n; n >>= 1` computes this elegantly.

---

## Problem 37: Find the Difference

**Statement:**  
Given two strings `s` and `t` where `t` is generated by randomly shuffling `s` and adding one extra character, find the added character.

**Approach:**  
XOR all characters of `s` and `t` together. All paired characters cancel out (`a ^ a = 0`), and the remaining value is the extra character. This works because XOR is commutative and associative.

**Solution:**
```python
class Solution:
    def findTheDifference(self, s, t):
        result = 0
        for ch in s + t:
            result ^= ord(ch)
        return chr(result)

# Alternative: sum approach
class Solution2:
    def findTheDifference(self, s, t):
        return chr(sum(ord(c) for c in t) - sum(ord(c) for c in s))

# Alternative: collections.Counter
from collections import Counter
class Solution3:
    def findTheDifference(self, s, t):
        diff = Counter(t) - Counter(s)
        return list(diff.keys())[0]
```

**Complexity:** O(n) time, O(1) space (XOR approach)

**Trick:** XOR is the cleanest solution — no overflow risk (unlike sum), no extra space (unlike Counter). `result ^= ord(ch)` for all characters leaves only the extra character's ASCII value.

---

# BIT MANIPULATION — HARD PROBLEMS

---

## Problem 38: Minimum Flips to Make a OR b Equal to c

**Statement:**  
Given 3 integers `a`, `b`, and `c`, return the minimum number of flips required on bits of `a` and `b` such that `(a | b) == c`. A flip changes a bit from 0 to 1 or 1 to 0.

**Approach:**  
Process each bit position independently. For each bit position:
- If `c`'s bit is 0: both `a` and `b` must be 0. If either is 1, flip it (cost = number of 1-bits in `a | b` at this position).
- If `c`'s bit is 1: at least one of `a` or `b` must be 1. If both are 0, flip one (cost = 1). Otherwise, no flip needed.

**Solution:**
```python
class Solution:
    def minFlips(self, a, b, c):
        flips = 0
        for i in range(32):
            abit = (a >> i) & 1
            bbit = (b >> i) & 1
            cbit = (c >> i) & 1
            if cbit == 0:
                flips += abit + bbit  # both must be 0
            else:
                if abit == 0 and bbit == 0:
                    flips += 1  # flip one to 1
        return flips

# Alternative: vectorized
class Solution2:
    def minFlips(self, a, b, c):
        or_ab = a | b
        # Bits where c=1 but or_ab=0 need 1 flip
        need_one = (~or_ab) & c
        # Bits where c=0 but or_ab=1 need flips for each set bit
        need_zero = or_ab & (~c)
        return bin(need_one).count('1') + bin(need_zero).count('1')
```

**Complexity:** O(1) — always 32 iterations. Space O(1).

**Trick:** The vectorized approach is elegant: `need_one` identifies positions where neither a nor b is 1 but c requires 1 (need exactly 1 flip). `need_zero` identifies positions where at least one of a/b is 1 but c requires 0 (need to flip every set bit). Sum the popcounts.

---

## Problem 39: Concatenation of Consecutive Binary Numbers

**Statement:**  
Given an integer `n`, return the decimal value of the binary string formed by concatenating the binary representations of 1 to n, modulo 10^9 + 7.

**Approach:**  
Build the result incrementally. When appending the binary representation of `i`, shift the current result left by `bit_length(i)` positions and add `i`. Track the bit length to know how many positions to shift.

**Solution:**
```python
class Solution:
    def concatenatedBinary(self, n):
        MOD = 10**9 + 7
        result = 0
        for i in range(1, n + 1):
            length = i.bit_length()
            result = ((result << length) | i) % MOD
        return result

# Alternative: using bit_length
class Solution2:
    def concatenatedBinary(self, n):
        MOD = 10**9 + 7
        result = 0
        for i in range(1, n + 1):
            result = ((result << i.bit_length()) + i) % MOD
        return result
```

**Complexity:** O(n * log n) since bit_length is O(log n). Space O(1).

**Trick:** `i.bit_length()` gives the number of bits needed to represent `i`. Shifting `result` left by this amount makes room for `i`'s bits. Modular arithmetic keeps numbers manageable. The `% MOD` after each step prevents overflow in languages with fixed-width integers (Python handles big ints but it's good practice).

---

## Problem 40: Maximum XOR with an Element from Array

**Statement:**  
You are given an array `nums` and a list of queries. Each query is `[x, m]` where you need to find the maximum `nums[i] XOR x` where `nums[i] <= m`. Return the results for all queries.

**Approach:**  
Sort `nums` and sort queries by `m`. Use an offline approach: process queries in increasing order of `m`, inserting nums into a binary trie as they become eligible (nums[i] <= m). For each query, find the max XOR with the current trie using the greedy approach.

**Solution:**
```python
class Solution:
    def maximizeXor(self, nums, queries):
        nums.sort()
        # queries: [x, m, original_index]
        sorted_queries = sorted([(q[1], q[0], i) for i, q in enumerate(queries)])
        result = [0] * len(queries)

        trie = {}
        idx = 0  # pointer into sorted nums

        for m, x, qi in sorted_queries:
            # Insert all nums <= m into trie
            while idx < len(nums) and nums[idx] <= m:
                node = trie
                for b in range(31, -1, -1):
                    bit = (nums[idx] >> b) & 1
                    if bit not in node:
                        node[bit] = {}
                    node = node[bit]
                idx += 1

            if not trie:
                result[qi] = -1
                continue

            # Find max XOR with x
            node = trie
            max_xor = 0
            for b in range(31, -1, -1):
                bit = (x >> b) & 1
                want = 1 - bit
                if want in node:
                    max_xor |= (1 << b)
                    node = node[want]
                else:
                    node = node[bit]
            result[qi] = max_xor

        return result
```

**Complexity:** O((n + q) * 32) for trie operations + O(n log n + q log q) for sorting. Space O(n * 32 + q).

**Trick:** The offline approach (sort queries by `m`) is key — it lets us incrementally insert nums into the trie in sorted order. This avoids rebuilding the trie for each query. The greedy max XOR on the trie is the same as Problem 14 but applied to a dynamic subset.

---

# Quick Reference: Complexity Cheat Sheet

| Problem | DS Used | Time | Space |
|---------|---------|------|-------|
| 1. Range Sum Query - Mutable | BIT | O(n log n) | O(n) |
| 2. Range Minimum Query | Seg Tree | O(n log n) | O(n) |
| 3. Count of Range Sum | BIT + Compress | O(n log n) | O(n) |
| 4. Count Inversions (BIT) | BIT | O(n log n) | O(n) |
| 5. Count Smaller After Self | BIT | O(n log n) | O(n) |
| 6. Maximum in Range | Seg Tree | O(n log n) | O(n) |
| 7. Range Update Point Query | BIT | O(n log n) | O(n) |
| 8. Merge Sort Inversions | Merge Sort | O(n log n) | O(n) |
| 9. Reverse Pairs | Merge Sort | O(n log n) | O(n) |
| 10. Kth in Stream | Heap/BIT | O(n log k) | O(k) |
| 11. Implement Trie | Trie | O(m) per op | O(NM) |
| 12. Search Suggestions | Trie | O(P + S) | O(NM) |
| 13. Word Search II | Trie + DFS | O(MN * 4^L) | O(WL) |
| 14. Max XOR Two Numbers | Trie | O(32n) | O(32n) |
| 15. Map Sum Pairs | Trie | O(m) per op | O(total chars) |
| 16. Replace Words | Trie/Set | O(D*R + S*W) | O(D*R) |
| 17. Longest Word Dict | Sort + Set | O(n log n) | O(nL) |
| 18. Stream of Characters | Reversed Trie | O(W*L + Q*maxL) | O(WL) |
| 19. Number of Provinces | DSU | O(n² * α(n)) | O(n) |
| 20. Redundant Connection | DSU | O(n * α(n)) | O(n) |
| 21. Accounts Merge | DSU | O(NK * α(N)) | O(NK) |
| 22. Connected Components | DSU | O(E * α(N)) | O(N) |
| 23. Graph Valid Tree | DSU | O(E * α(N)) | O(N) |
| 24. Number of Islands II | DSU | O(K * α(MN)) | O(MN) |
| 25. Smallest String Swaps | DSU | O(n log n) | O(n) |
| 26. Single Number | XOR | O(n) | O(1) |
| 27. Number of 1 Bits | Kernighan | O(k) | O(1) |
| 28. Counting Bits | DP + Bit | O(n) | O(n) |
| 29. Reverse Bits | Shift | O(1) | O(1) |
| 30. Power of Two | Bit Trick | O(1) | O(1) |
| 31. Single Number II | State Machine | O(n) | O(1) |
| 32. Max Product Word Length | Bit Mask | O(n² + nL) | O(n) |
| 33. AND of Range | Common Prefix | O(log n) | O(1) |
| 34. UTF-8 Validation | Bit Check | O(n) | O(1) |
| 35. XOR of All Pairings | Parity | O(n+m) | O(1) |
| 36. Min One Bit Ops | Gray Code | O(log n) | O(1) |
| 37. Find the Difference | XOR | O(n) | O(1) |
| 38. Min Flips OR Equal | Bit Check | O(1) | O(1) |
| 39. Concat Binary Numbers | Shift + Mod | O(n log n) | O(1) |
| 40. Max XOR with Element | Trie + Offline | O((n+q)*32) | O(n*32) |

---

# Key Patterns to Remember

## Segment Tree / BIT Patterns
1. **BIT for prefix sums** — `add(i, delta)` + `prefixSum(i)` → range sum = `prefixSum(r) - prefixSum(l-1)`
2. **BIT for range update point query** — `add(l, val); add(r+1, -val)` then `prefixSum(i)` = value at i
3. **Segment tree template** — same code for min/max/sum, just change the merge operation
4. **Coordinate compression** — essential when values are large but count is small
5. **Merge sort for counting** — count inversions/pairs during the merge step

## Trie Patterns
1. **Standard trie** — insert/search/startsWith in O(m)
2. **Bitwise trie** — traverse bits from MSB for max/min XOR queries
3. **Reversed trie** — reverse words to convert suffix matching to prefix matching
4. **Trie + DFS** — for word search, use trie for pruning branches

## DSU Patterns
1. **Basic DSU** — path compression + union by rank = near-constant per operation
2. **Component counting** — maintain a counter, decrement on each successful union
3. **Dynamic connectivity** — add edges and track components in real time
4. **Grouping by equivalence** — emails, swaps, accounts — all use DSU to find connected groups

## Bit Manipulation Patterns
1. **XOR all** — find single element, find difference, cancel pairs
2. **`n & (n-1)`** — clear lowest set bit (power of two check, popcount)
3. **Bit masks** — represent sets of characters/flags in a single integer
4. **Greedy bit traversal** — for max XOR, always try to set the current bit to 1
5. **Bit-by-bit processing** — count set bits at each position, handle each bit independently
