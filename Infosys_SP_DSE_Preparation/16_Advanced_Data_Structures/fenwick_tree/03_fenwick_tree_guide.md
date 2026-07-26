# Fenwick Tree (Binary Indexed Tree) Guide

> **Why Fenwick Tree?** It's a simpler, more memory-efficient alternative to Segment Tree for prefix sum problems. Uses O(n) space instead of O(4n), and the code is shorter. The "magic" is in using `idx & (-idx)` to navigate the tree.

---

## What is a Fenwick Tree? (Visual Explanation)

```
  Array: [1, 2, 3, 4, 5, 6, 7, 8]

  The BIT stores partial sums based on binary structure:

  Index:  1     2     3     4     5     6     7     8
  Binary: 001   010   011   100   101   110   111  1000
          ↓     ↓     ↓     ↓     ↓     ↓     ↓     ↓
  BIT:   [1,    3,    3,   10,    5,   11,    7,   36]
          ↓     ↓     ↓     ↓     ↓     ↓     ↓     ↓
  Covers: [1,1] [1,2] [3,3] [1,4] [5,5] [5,6] [7,7] [1,8]

  ┌──────────────────────────────────────────────────────────┐
  │  Each index i is responsible for a RANGE of elements.    │
  │  The range length = lowest set bit of i (i & -i).       │
  │                                                          │
  │  i=1 (001): covers 1 element   (1 & -1 = 1)            │
  │  i=2 (010): covers 2 elements  (2 & -2 = 2)            │
  │  i=3 (011): covers 1 element   (3 & -3 = 1)            │
  │  i=4 (100): covers 4 elements  (4 & -4 = 4)            │
  │  i=5 (101): covers 1 element   (5 & -5 = 1)            │
  │  i=6 (110): covers 2 elements  (6 & -6 = 2)            │
  │  i=7 (111): covers 1 element   (7 & -7 = 1)            │
  │  i=8 (1000): covers 8 elements (8 & -8 = 8)            │
  └──────────────────────────────────────────────────────────┘
```

### Visual: Parent-Child Relationship

```
  The tree structure (implicit):

  Index:  8
          |
      ┌───┴───┐
      4       (8)
      |
  ┌───┴───┐
  2       (6)
  |
  ┌───┴───┐
  1       (3)       (5)       (7)

  Parent of i = i + (i & -i)  [moving UP in tree]
  So: 1→2→4→8, 3→4→8, 5→6→8, 7→8

  For QUERY (prefix sum): move DOWN by removing lowest set bit
    idx & (idx - 1) removes lowest set bit

  For UPDATE: move UP by adding lowest set bit
    idx + (idx & -idx)
```

---

## When to Use Fenwick Tree vs Segment Tree

```
  ┌─────────────────┬─────────────┬──────────────────┐
  │   Operation     │ Fenwick Tree│  Segment Tree    │
  ├─────────────────┼─────────────┼──────────────────┤
  │ Point Update    │  O(log n)   │  O(log n)        │
  │ Prefix Query    │  O(log n)   │  O(log n)        │
  │ Range Query     │  O(log n)   │  O(log n)        │
  │ Range Update    │  O(log n)*  │  O(log n)        │
  │ Range+Range     │  O(log n)** │  O(log n)        │
  │ Space           │  O(n)       │  O(4n)           │
  │ Code Complexity │  Simple     │  Moderate        │
  │ Flexibility     │  Less       │  More            │
  └─────────────────┴─────────────┴──────────────────┘
  * with difference array trick
  ** with two BITs

  USE FENWICK TREE WHEN:
  ✓ Only need prefix sums + point updates
  ✓ Memory is a concern
  ✓ Simpler code is preferred
  ✓ Counting inversions / smaller elements

  USE SEGMENT TREE WHEN:
  ✓ Need arbitrary range queries (min, max, gcd)
  ✓ Need range updates + range queries
  ✓ Need more flexibility (non-commutative operations)
```

---

## 1. Build BIT

```python
class BIT:
    def __init__(self, n):
        """Initialize BIT with size n (1-indexed)"""
        self.n = n
        self.tree = [0] * (n + 1)
    
    def build(self, arr):
        """Build BIT from array (1-indexed internally)"""
        for i in range(1, self.n + 1):
            self.tree[i] += arr[i - 1]
            j = i + (i & (-i))
            if j <= self.n:
                self.tree[j] += self.tree[i]
    
    def build_v2(self, arr):
        """Alternative build method"""
        self.n = len(arr)
        self.tree = [0] * (self.n + 1)
        
        for i in range(self.n):
            self.update(i, arr[i])
    
    def build_v3(self, arr):
        """O(n) build method"""
        self.n = len(arr)
        self.tree = [0] * (self.n + 1)
        
        # First, store prefix sums
        for i in range(self.n):
            self.tree[i + 1] = arr[i]
        
        # Build tree by adding children to parents
        for i in range(1, self.n + 1):
            j = i + (i & (-i))
            if j <= self.n:
                self.tree[j] += self.tree[i]

# Test
bit = BIT(8)
arr = [1, 2, 3, 4, 5, 6, 7, 8]
bit.build_v3(arr)
print(f"BIT array: {bit.tree}")
```

**Time Complexity:** O(n log n) for build_v2, O(n) for build_v3
**Space Complexity:** O(n)

---

## 2. Update BIT

### Visual: How Update Traverses the Tree

```
  Update index 3 (0-indexed) by adding 5.
  Convert to 1-indexed: idx = 4 (binary: 100)

  idx & (-idx) for idx=4: 100 & 100 = 4

  Update path: 4 → 8 → (next would be 16, stop if > n)

  BIT before:  [_, 1, 3, 3, 10, 5, 11, 7, 36]
  Index:        0  1  2  3   4  5   6  7   8

  After updating index 4 by +5:
  ┌─────────────────────────────────────────────────┐
  │  idx=4:  tree[4] += 5  → 10+5 = 15             │
  │  idx=8:  tree[8] += 5  → 36+5 = 41             │
  │  (next: idx=16 > n=8, stop)                    │
  └─────────────────────────────────────────────────┘

  BIT after:   [_, 1, 3, 3, 15, 5, 11, 7, 41]

  WHY does this work? We update ALL nodes whose
  range includes the target index:
    tree[4] covers [1,4] → includes index 4 ✓
    tree[8] covers [1,8] → includes index 4 ✓
    tree[1] covers [1,1] → does NOT include ✗
    tree[2] covers [1,2] → does NOT include ✗
    tree[5] covers [5,5] → does NOT include ✗
```

```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, idx, delta):
        """Add delta to element at index idx (0-indexed).
        
        Algorithm: Move UP the tree by adding lowest set bit.
        Each node on the path covers a range containing idx.
        
        Time: O(log n) — at most log₂(n) nodes visited
        """
        idx += 1  # Convert to 1-indexed
        
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & (-idx)  # Move to parent (next responsible node)
    
    def point_update(self, idx, val):
        """Set element at idx to val (0-indexed)"""
        # Calculate difference and update
        # This requires storing original values
        pass

# Test
bit = BIT(8)
arr = [1, 2, 3, 4, 5, 6, 7, 8]

# Build BIT
for i, val in enumerate(arr):
    bit.update(i, val)

print(f"Before update: tree = {bit.tree}")

# Update index 3 (0-indexed) by adding 5
bit.update(3, 5)
print(f"After updating index 3 by +5: tree = {bit.tree}")
```

**Key Insight:** `idx & (-idx)` gives the lowest set bit, which determines the range that index is responsible for.

**Time Complexity:** O(log n)
**Space Complexity:** O(1)

---

## 3. Query BIT (Prefix Sum)

### Visual: How Prefix Query Traverses the Tree

```
  Query prefix sum [0, 5] (1-indexed: query(6))
  
  idx = 6 (binary: 110)

  Query path: 6 → 4 → 0 (stop when idx=0)

  ┌──────────────────────────────────────────────────────┐
  │  idx=6 (110): tree[6] covers [5,6] → add tree[6]=11 │
  │  idx=4 (100): tree[4] covers [1,4] → add tree[4]=15 │
  │  idx=0: STOP                                         │
  │                                                      │
  │  Sum = 11 + 15 = 26                                 │
  │                                                      │
  │  Verify: [1,2,3,4,5,6] = 1+2+3+4+5+6 = 21         │
  │  Wait, we updated earlier... after update:           │
  │  arr[3] became 9 (was 4, +5), so sum = 1+2+3+9+5+6 │
  │  = 26 ✓                                             │
  └──────────────────────────────────────────────────────┘

  Moving DOWN: idx -= idx & (-idx) removes lowest set bit
    110 → 100 → 000 (3 iterations for 3 set bits)

  WHY it works:
  ┌──────────────────────────────────────────────────────┐
  │  prefix_sum(6) = arr[1]+arr[2]+arr[3]+arr[4]+       │
  │                  arr[5]+arr[6]                       │
  │                                                      │
  │  tree[6] = arr[5]+arr[6]    → covers [5,6]          │
  │  tree[4] = arr[1]+arr[2]+arr[3]+arr[4] → covers [1,4]│
  │                                                      │
  │  Sum of tree[6] + tree[4] = complete prefix sum!     │
  └──────────────────────────────────────────────────────┘
```

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
        """Query prefix sum from 0 to idx (inclusive).
        
        Algorithm: Move DOWN the tree by removing lowest set bit.
        Accumulate values from nodes covering the prefix.
        
        Time: O(log n) — at most log₂(n) nodes visited
        """
        result = 0
        idx += 1  # Convert to 1-indexed
        
        while idx > 0:
            result += self.tree[idx]
            idx -= idx & (-idx)  # Move DOWN (remove lowest set bit)  # Move to parent
        
        return result
    
    def range_query(self, l, r):
        """Query sum from l to r (inclusive)"""
        if l == 0:
            return self.query(r)
        return self.query(r) - self.query(l - 1)

# Test
bit = BIT(8)
arr = [1, 2, 3, 4, 5, 6, 7, 8]

for i, val in enumerate(arr):
    bit.update(i, val)

print(f"Prefix sum [0, 3]: {bit.query(3)}")  # 1+2+3+4 = 10
print(f"Range sum [2, 5]: {bit.range_query(2, 5)}")  # 3+4+5+6 = 18
print(f"Prefix sum [0, 7]: {bit.query(7)}")  # 36
```

**Time Complexity:** O(log n) for both query and range_query
**Space Complexity:** O(1)

---

## 4. Range Update, Point Query

To support adding a value to a range and querying a single point:

**Technique:** Use difference array concept with BIT.

```python
class BITRangeUpdate:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, idx, delta):
        idx += 1
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & (-idx)
    
    def query(self, idx):
        """Query point value at idx"""
        result = 0
        idx += 1
        
        while idx > 0:
            result += self.tree[idx]
            idx -= idx & (-idx)
        
        return result
    
    def range_update(self, l, r, delta):
        """Add delta to all elements in range [l, r]"""
        self.update(l, delta)
        if r + 1 < self.n:
            self.update(r + 1, -delta)
    
    def point_query(self, idx):
        """Get value at index idx"""
        return self.query(idx)

# Test
bit = BITRangeUpdate(8)
arr = [0, 0, 0, 0, 0, 0, 0, 0]

# Add 5 to range [2, 5]
bit.range_update(2, 5, 5)
print(f"After adding 5 to [2,5]:")
for i in range(8):
    print(f"  arr[{i}] = {bit.point_query(i)}")

# Add 3 to range [4, 7]
bit.range_update(4, 7, 3)
print(f"After adding 3 to [4,7]:")
for i in range(8):
    print(f"  arr[{i}] = {bit.point_query(i)}")
```

**Time Complexity:** O(log n) for both operations
**Space Complexity:** O(n)

---

## 5. Point Update, Range Query

This is the standard BIT operation.

```python
class BITPointUpdate:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (self.n + 1)
        self.arr = arr[:]
        
        # Build BIT
        for i in range(self.n):
            self.update(i, arr[i])
    
    def update(self, idx, delta):
        """Add delta to element at idx"""
        idx += 1
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & (-idx)
    
    def query(self, idx):
        """Prefix sum from 0 to idx"""
        result = 0
        idx += 1
        while idx > 0:
            result += self.tree[idx]
            idx -= idx & (-idx)
        return result
    
    def range_query(self, l, r):
        """Sum from l to r"""
        if l == 0:
            return self.query(r)
        return self.query(r) - self.query(l - 1)
    
    def point_update(self, idx, val):
        """Set element at idx to val"""
        delta = val - self.arr[idx]
        self.arr[idx] = val
        self.update(idx, delta)

# Test
arr = [1, 2, 3, 4, 5]
bit = BITPointUpdate(arr)

print(f"Sum [0, 3]: {bit.range_query(0, 3)}")  # 10
bit.point_update(2, 10)
print(f"After update, Sum [0, 3]: {bit.range_query(0, 3)}")  # 17
```

---

## 6. Range Update, Range Query

To support both range updates and range queries, use 2 BITs.

**Mathematical Foundation:**
```
For range update [l, r] with value v:
  BIT1.update(l, v)
  BIT1.update(r+1, -v)
  BIT2.update(l, v*(l-1))
  BIT2.update(r+1, -v*r)

For prefix query [0, idx]:
  result = BIT1.query(idx) * idx - BIT2.query(idx)
```

```python
class BIT2D:
    def __init__(self, n):
        self.n = n
        self.bit1 = [0] * (n + 1)
        self.bit2 = [0] * (n + 1)
    
    def update(self, bit, idx, delta):
        while idx <= self.n:
            bit[idx] += delta
            idx += idx & (-idx)
    
    def query(self, bit, idx):
        result = 0
        while idx > 0:
            result += bit[idx]
            idx -= idx & (-idx)
        return result
    
    def range_update(self, l, r, delta):
        """Add delta to all elements in [l, r]"""
        l += 1
        r += 1
        
        self.update(self.bit1, l, delta)
        self.update(self.bit1, r + 1, -delta)
        self.update(self.bit2, l, delta * (l - 1))
        self.update(self.bit2, r + 1, -delta * r)
    
    def prefix_query(self, idx):
        """Query prefix sum from 0 to idx"""
        idx += 1
        return self.query(self.bit1, idx) * idx - self.query(self.bit2, idx)
    
    def range_query(self, l, r):
        """Query sum from l to r"""
        if l == 0:
            return self.prefix_query(r)
        return self.prefix_query(r) - self.prefix_query(l - 1)

# Test
bit2d = BIT2D(8)

# Initial array: [0, 0, 0, 0, 0, 0, 0, 0]
# Add 5 to range [2, 5]
bit2d.range_update(2, 5, 5)
print(f"After adding 5 to [2,5]:")
print(f"  Sum [0, 5]: {bit2d.range_query(0, 5)}")  # 25
print(f"  Sum [2, 5]: {bit2d.range_query(2, 5)}")  # 20

# Add 3 to range [4, 7]
bit2d.range_update(4, 7, 3)
print(f"After adding 3 to [4,7]:")
print(f"  Sum [0, 7]: {bit2d.range_query(0, 7)}")  # 37
print(f"  Sum [4, 7]: {bit2d.range_query(4, 7)}")  # 22
```

**Time Complexity:** O(log n) for all operations
**Space Complexity:** O(n)

---

## 7. Applications

### 7.1 Count Inversions

```python
def count_inversions_bit(nums):
    """Count inversions using BIT"""
    # Coordinate compression
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
    
    # Process from right to left
    for i in range(n - 1, -1, -1):
        r = rank[nums[i]]
        inv_count += query(r - 1)  # Count elements smaller than current
        update(r)
    
    return inv_count

# Test
nums = [2, 4, 1, 3, 5]
print(f"Inversions: {count_inversions_bit(nums)}")  # 3
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

---

### 7.2 Count Smaller Numbers After Self

```python
def count_smaller_after_self(nums):
    """Count smaller elements to the right of each element"""
    # Coordinate compression
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
        result = 0
        while idx > 0:
            result += bit[idx]
            idx -= idx & (-idx)
        return result
    
    # Process from right to left
    for i in range(n - 1, -1, -1):
        r = rank[nums[i]]
        result[i] = query(r - 1)
        update(r)
    
    return result

# Test
nums = [5, 2, 6, 1]
print(f"Count smaller: {count_smaller_after_self(nums)}")  # [2, 1, 1, 0]
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

---

### 7.3 Range Sum Query

```python
class RangeSumQuery:
    def __init__(self, nums):
        self.n = len(nums)
        self.bit = [0] * (self.n + 1)
        self.nums = nums[:]
        
        for i in range(self.n):
            self.update(i, nums[i])
    
    def update(self, idx, delta):
        idx += 1
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & (-idx)
    
    def query(self, idx):
        result = 0
        idx += 1
        while idx > 0:
            result += self.bit[idx]
            idx -= idx & (-idx)
        return result
    
    def sumRange(self, left, right):
        """Range sum query [left, right]"""
        if left == 0:
            return self.query(right)
        return self.query(right) - self.query(left - 1)

# Test
nums = [1, 3, 5]
rsq = RangeSumQuery(nums)
print(f"Sum [0, 2]: {rsq.sumRange(0, 2)}")  # 9
rsq.update(1, 2)
print(f"After update, Sum [0, 2]: {rsq.sumRange(0, 2)}")  # 11
```

**Time Complexity:** O(log n) for both operations
**Space Complexity:** O(n)

---

### 7.4 Frequency Count in Range

```python
def frequency_in_range(arr, queries):
    """Answer queries about frequency of elements in ranges"""
    from collections import defaultdict
    
    # Group queries by right endpoint
    indexed_queries = []
    for i, (l, r) in enumerate(queries):
        indexed_queries.append((r, l, i))
    indexed_queries.sort()
    
    # Process using BIT
    n = len(arr)
    bit = [0] * (n + 2)
    last_occurrence = {}
    result = [0] * len(queries)
    
    def update(idx, delta):
        while idx <= n:
            bit[idx] += delta
            idx += idx & (-idx)
    
    def query(idx):
        res = 0
        while idx > 0:
            res += bit[idx]
            idx -= idx & (-idx)
        return res
    
    query_idx = 0
    for r, l, q_idx in indexed_queries:
        while query_idx <= r:
            val = arr[query_idx]
            # Remove previous occurrence
            if val in last_occurrence:
                update(last_occurrence[val] + 1, -1)
            # Add current occurrence
            update(query_idx + 1, 1)
            last_occurrence[val] = query_idx
            query_idx += 1
        
        result[q_idx] = query(r + 1) - query(l)
    
    return result

# Test
arr = [1, 2, 1, 3, 2]
queries = [(0, 2), (1, 3), (0, 4)]
print(f"Frequency queries: {frequency_in_range(arr, queries)}")  # [2, 2, 3]
```

**Time Complexity:** O((n + q) log n)
**Space Complexity:** O(n)

---

### 7.5 2D BIT for Range Updates

```python
class BIT2DRangeUpdate:
    """2D BIT supporting range updates and range queries"""
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.bit = [[0] * (cols + 2) for _ in range(rows + 2)]
    
    def update(self, x, y, delta):
        i = x + 1
        while i <= self.rows + 1:
            j = y + 1
            while j <= self.cols + 1:
                self.bit[i][j] += delta
                j += j & (-j)
            i += i & (-i)
    
    def query(self, x, y):
        result = 0
        i = x + 1
        while i > 0:
            j = y + 1
            while j > 0:
                result += self.bit[i][j]
                j -= j & (-j)
            i -= i & (-i)
        return result
    
    def range_update(self, x1, y1, x2, y2, delta):
        """Add delta to rectangle [x1,y1] to [x2,y2]"""
        self.update(x1, y1, delta)
        self.update(x1, y2 + 1, -delta)
        self.update(x2 + 1, y1, -delta)
        self.update(x2 + 1, y2 + 1, delta)
    
    def range_query(self, x1, y1, x2, y2):
        """Query sum in rectangle [x1,y1] to [x2,y2]"""
        return (self.query(x2, y2) - self.query(x1 - 1, y2) -
                self.query(x2, y1 - 1) + self.query(x1 - 1, y1 - 1))

# Test
bit2d = BIT2DRangeUpdate(4, 4)
bit2d.range_update(1, 1, 3, 3, 5)
print(f"Sum of [1,1] to [3,3]: {bit2d.range_query(1, 1, 3, 3)}")  # 45
```

**Time Complexity:** O(log n * log m) for all operations
**Space Complexity:** O(n * m)

---

## 8. Advanced Applications

### 8.1 Find Kth Smallest Element

```python
class BITKthSmallest:
    def __init__(self, max_val):
        self.max_val = max_val
        self.bit = [0] * (max_val + 2)
        self.counts = [0] * (max_val + 1)
    
    def update(self, idx, delta):
        while idx <= self.max_val:
            self.bit[idx] += delta
            idx += idx & (-idx)
    
    def query(self, idx):
        result = 0
        while idx > 0:
            result += self.bit[idx]
            idx -= idx & (-idx)
        return result
    
    def add(self, num):
        if self.counts[num] == 0:
            self.update(num, 1)
        self.counts[num] += 1
    
    def remove(self, num):
        if self.counts[num] > 0:
            self.counts[num] -= 1
            if self.counts[num] == 0:
                self.update(num, -1)
    
    def kth_smallest(self, k):
        """Find kth smallest element"""
        lo, hi = 1, self.max_val
        while lo < hi:
            mid = (lo + hi) // 2
            if self.query(mid) >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo

# Test
bit_kth = BITKthSmallest(100)
bit_kth.add(5)
bit_kth.add(3)
bit_kth.add(8)
bit_kth.add(1)

print(f"1st smallest: {bit_kth.kth_smallest(1)}")  # 1
print(f"3rd smallest: {bit_kth.kth_smallest(3)}")  # 5
```

**Time Complexity:** O(log max_val) for add/remove, O(log² max_val) for kth_smallest

---

### 8.2 Dynamic Frequency Table

```python
class DynamicFrequency:
    def __init__(self, max_val):
        self.max_val = max_val
        self.bit = [0] * (max_val + 2)
        self.freq = [0] * (max_val + 1)
    
    def update(self, idx, delta):
        while idx <= self.max_val:
            self.bit[idx] += delta
            idx += idx & (-idx)
    
    def query(self, idx):
        result = 0
        while idx > 0:
            result += self.bit[idx]
            idx -= idx & (-idx)
        return result
    
    def range_query(self, l, r):
        if l > r:
            return 0
        return self.query(r) - self.query(l - 1)
    
    def add(self, num):
        self.freq[num] += 1
        self.update(num, 1)
    
    def remove(self, num):
        if self.freq[num] > 0:
            self.freq[num] -= 1
            self.update(num, -1)
    
    def count_in_range(self, l, r):
        """Count elements in range [l, r]"""
        return self.range_query(l, r)
    
    def count_less_than(self, x):
        """Count elements less than x"""
        return self.query(x - 1)
    
    def count_greater_than(self, x):
        """Count elements greater than x"""
        return self.query(self.max_val) - self.query(x)

# Test
freq = DynamicFrequency(100)
freq.add(5)
freq.add(3)
freq.add(8)
freq.add(5)
freq.add(1)

print(f"Count in [3, 8]: {freq.count_in_range(3, 8)}")  # 4
print(f"Count < 5: {freq.count_less_than(5)}")  # 2
print(f"Count > 5: {freq.count_greater_than(5)}")  # 2
```

---

## Summary

| Feature | Description |
|---------|-------------|
| Core Operations | Point Update, Prefix Query |
| Key Insight | Use `idx & (-idx)` to find parent range |
| Memory | O(n) - very efficient |
| When to Use | Prefix sums, frequency counting |
| Limitations | Only works for commutative operations |

---

## Time & Space Complexity

| Operation | Time Complexity |
|-----------|-----------------|
| Build | O(n) |
| Update | O(log n) |
| Query | O(log n) |
| Range Query | O(log n) |
| Space | O(n) |

---

## Tips for Infosys SP DSE

1. **Coordinate Compression:** When values are large but sparse, compress to rank
2. **Difference Array:** For range updates, point queries use single BIT
3. **Two BITs:** For range updates and range queries
4. **Binary Search on BIT:** For finding kth element
5. **2D BIT:** For 2D range queries
6. **Fenwick vs Segment Tree:** BIT is simpler but less flexible; use BIT for prefix sums
