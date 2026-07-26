# Segment Tree Guide

> **What is it?** A binary tree that stores information about array intervals/segments. It enables both range queries AND point/range updates in O(log n) — something neither prefix sums nor raw arrays can do alone.

---

## Visual: What a Segment Tree Looks Like

```
  Array: [1, 3, 5, 7, 9, 11]

  Segment Tree (sum queries):
                      [36]             ← sum of [0..5]
                    /      \
                [9]          [27]      ← sum of [0..2] and [3..5]
               /    \       /    \
            [4]    [5]   [16]   [11]   ← sum of [0..1],[2..2],[3..4],[5..5]
           /  \    |    /  \     |
         [1]  [3] [5] [7]  [9] [11]   ← leaf nodes = array elements

  Each internal node stores the SUM of its children.
  To query sum[l..r], we decompose [l..r] into O(log n) segments.

  ┌──────────────────────────────────────────────────────┐
  │  KEY INSIGHT: The tree has height O(log n)           │
  │  So query/update only touch O(log n) nodes!          │
  │                                                      │
  │  Array size: n = 6                                   │
  │  Tree size: 4n = 24 nodes (allocated)                │
  │  Leaf nodes: n = 6                                   │
  │  Internal nodes: n - 1 = 5                           │
  └──────────────────────────────────────────────────────┘
```

### Array Representation of Segment Tree

```
  We store the tree in an array using indices:
  
  For node at index i:
    Left child  = 2*i + 1
    Right child = 2*i + 2
    Parent      = (i - 1) / 2

  Index:  0    1    2    3    4    5    6    7    8    9   10   11
  Value: [36,   9,  27,   4,   5,  16,  11,   1,   3,   5,   7,   9]
          ↑
       root (index 0)

  Mapping:
  ┌───────┬──────────────┬──────────────┬────────────┐
  │ Index │  Left Child  │ Right Child  │   Range    │
  ├───────┼──────────────┼──────────────┼────────────┤
  │   0   │      1       │      2       │   [0,5]    │
  │   1   │      3       │      4       │   [0,2]    │
  │   2   │      5       │      6       │   [3,5]    │
  │   3   │      7       │      8       │   [0,1]    │
  │   4   │      -       │      -       │   [2,2]    │
  │   5   │      9       │     10       │   [3,4]    │
  │   6   │      -       │      -       │   [5,5]    │
  └───────┴──────────────┴──────────────┴────────────┘
  (indices 7-11 are leaves)
```

---

## When to Use Segment Tree vs Alternatives

```
  ┌─────────────────┬──────────┬─────────────┬──────────────┐
  │   Operation     │  Array   │ Prefix Sum  │ Segment Tree │
  ├─────────────────┼──────────┼─────────────┼──────────────┤
  │ Point Update    │  O(1)    │  O(n)       │  O(log n)    │
  │ Range Query     │  O(n)    │  O(1)       │  O(log n)    │
  │ Range Update    │  O(n)    │  O(n)       │  O(log n)*   │
  │ Space           │  O(n)    │  O(n)       │  O(4n)       │
  └─────────────────┴──────────┴─────────────┴──────────────┘
  * with lazy propagation

  USE SEGMENT TREE WHEN:
  ✓ Need BOTH range queries AND point updates
  ✓ Need range updates (with lazy propagation)
  ✓ Query/update happen frequently (q >> n)
  ✓ Need min/max AND updates (prefix sums can't do this)

  USE PREFIX SUM WHEN:
  ✓ Array is STATIC (no updates)
  ✓ Only need range sum queries
```

---

## 1. Build Segment Tree

### Visual: How Building Works (Recursive)

```
  Array: [1, 3, 5, 7, 9, 11]

  Build function is called recursively:

  build(data, node=0, start=0, end=5)
  │
  ├── start != end, so split:
  │   mid = (0+5)//2 = 2
  │
  ├── build(data, node=1, start=0, end=2)    ← left subtree
  │   │
  │   ├── build(data, node=3, start=0, end=1)
  │   │   ├── build(data, node=7, start=0, end=0) → tree[7] = 1
  │   │   └── build(data, node=8, start=1, end=1) → tree[8] = 3
  │   │   tree[3] = 1 + 3 = 4
  │   │
  │   └── build(data, node=4, start=2, end=2) → tree[4] = 5
  │   tree[1] = 4 + 5 = 9
  │
  └── build(data, node=2, start=3, end=5)    ← right subtree
      │
      ├── build(data, node=5, start=3, end=4)
      │   ├── build(data, node=9, start=3, end=3) → tree[9] = 7
      │   └── build(data, node=10, start=4, end=4) → tree[10] = 9
      │   tree[5] = 7 + 9 = 16
      │
      └── build(data, node=6, start=5, end=5) → tree[6] = 11
      tree[2] = 16 + 11 = 27

  tree[0] = 9 + 27 = 36  ← root = total sum
```

```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.build(data, 0, 0, self.n - 1)
    
    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            
            self.build(data, left_child, start, mid)
            self.build(data, right_child, mid + 1, end)
            
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

# Test
data = [1, 3, 5, 7, 9, 11]
seg_tree = SegmentTree(data)
print(f"Tree array: {seg_tree.tree}")
```

**Time Complexity:** O(n) for building
**Space Complexity:** O(4n) for the tree array

---

## 2. Range Query (Sum)

### Visual: How Range Query Works

```
  Query: sum[1, 3] (sum of elements at indices 1, 2, 3)

  Starting at root [0,5]:

                     [36]              query(0,5, l=1,r=3)
                    /      \
               [9]          [27]
              /    \       /    \
           [4]    [5]   [16]   [11]
          /  \    |    /  \     |
        [1] [3] [5] [7] [9] [11]

  Step 1: Root covers [0,5], query is [1,3]
          PARTIAL OVERLAP → recurse both children

  Step 2: Left child [0,2] vs query [1,3]
          PARTIAL OVERLAP → recurse both children
          ├── Left child [0,1] vs [1,3]: PARTIAL
          │   ├── [0,0]: NO OVERLAP → return 0
          │   └── [1,1]: COMPLETE OVERLAP → return 3
          └── Right child [2,2] vs [1,3]: COMPLETE → return 5

  Step 3: Right child [3,5] vs query [1,3]
          PARTIAL OVERLAP → recurse
          ├── Left child [3,4] vs [1,3]: PARTIAL
          │   ├── [3,3]: COMPLETE OVERLAP → return 7
          │   └── [4,4]: NO OVERLAP → return 0
          └── Right child [5,5]: NO OVERLAP → return 0

  Final: 0 + 3 + 5 + 7 + 0 = 15 ✓

  ┌──────────────────────────────────────────────────────┐
  │  Three cases in query:                               │
  │                                                      │
  │  1. NO OVERLAP (r < start or end < l)                │
  │     → Return identity (0 for sum, INF for min)       │
  │                                                      │
  │  2. COMPLETE OVERLAP (l ≤ start and end ≤ r)         │
  │     → Return tree[node] (already computed!)          │
  │                                                      │
  │  3. PARTIAL OVERLAP                                   │
  │     → Recurse to both children, combine results      │
  └──────────────────────────────────────────────────────┘
```

```python
    def query(self, node, start, end, l, r):
        """Query sum in range [l, r]"""
        # No overlap
        if r < start or end < l:
            return 0
        
        # Complete overlap
        if l <= start and end <= r:
            return self.tree[node]
        
        # Partial overlap
        mid = (start + end) // 2
        left_sum = self.query(2 * node + 1, start, mid, l, r)
        right_sum = self.query(2 * node + 2, mid + 1, end, l, r)
        
        return left_sum + right_sum
    
    def range_query(self, l, r):
        """Public method for range query"""
        return self.query(0, 0, self.n - 1, l, r)
    
    def update(self, node, start, end, idx, val):
        """Update value at index idx"""
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node + 1, start, mid, idx, val)
            else:
                self.update(2 * node + 2, mid + 1, end, idx, val)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def point_update(self, idx, val):
        """Public method for point update"""
        self.update(0, 0, self.n - 1, idx, val)

# Test
data = [1, 3, 5, 7, 9, 11]
seg = SegmentTreeSum(data)

print(f"Sum of [1, 3]: {seg.range_query(1, 3)}")  # 3 + 5 + 7 = 15
print(f"Sum of [0, 5]: {seg.range_query(0, 5)}")  # 36

seg.point_update(2, 10)  # Update index 2 from 5 to 10
print(f"After update, sum of [1, 3]: {seg.range_query(1, 3)}")  # 3 + 10 + 7 = 20
```

**Time Complexity:** O(log n) for query and update
**Space Complexity:** O(4n)

---

## 3. Range Query (Minimum)

```python
class SegmentTreeMin:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [float('inf')] * (4 * self.n)
        self.build(data, 0, 0, self.n - 1)
    
    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self.build(data, 2 * node + 1, start, mid)
            self.build(data, 2 * node + 2, mid + 1, end)
            self.tree[node] = min(self.tree[2 * node + 1], self.tree[2 * node + 2])
    
    def query(self, node, start, end, l, r):
        """Query minimum in range [l, r]"""
        if r < start or end < l:
            return float('inf')
        
        if l <= start and end <= r:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_min = self.query(2 * node + 1, start, mid, l, r)
        right_min = self.query(2 * node + 2, mid + 1, end, l, r)
        
        return min(left_min, right_min)
    
    def range_query(self, l, r):
        return self.query(0, 0, self.n - 1, l, r)
    
    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node + 1, start, mid, idx, val)
            else:
                self.update(2 * node + 2, mid + 1, end, idx, val)
            self.tree[node] = min(self.tree[2 * node + 1], self.tree[2 * node + 2])
    
    def point_update(self, idx, val):
        self.update(0, 0, self.n - 1, idx, val)

# Test
data = [5, 3, 7, 9, 1, 4]
seg_min = SegmentTreeMin(data)

print(f"Min in [1, 4]: {seg_min.range_query(1, 4)}")  # min(3,7,9,1) = 1
print(f"Min in [0, 2]: {seg_min.range_query(0, 2)}")  # min(5,3,7) = 3
```

---

## 4. Range Query (Maximum)

```python
class SegmentTreeMax:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [float('-inf')] * (4 * self.n)
        self.build(data, 0, 0, self.n - 1)
    
    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self.build(data, 2 * node + 1, start, mid)
            self.build(data, 2 * node + 2, mid + 1, end)
            self.tree[node] = max(self.tree[2 * node + 1], self.tree[2 * node + 2])
    
    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return float('-inf')
        
        if l <= start and end <= r:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_max = self.query(2 * node + 1, start, mid, l, r)
        right_max = self.query(2 * node + 2, mid + 1, end, l, r)
        
        return max(left_max, right_max)
    
    def range_query(self, l, r):
        return self.query(0, 0, self.n - 1, l, r)
    
    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node + 1, start, mid, idx, val)
            else:
                self.update(2 * node + 2, mid + 1, end, idx, val)
            self.tree[node] = max(self.tree[2 * node + 1], self.tree[2 * node + 2])
    
    def point_update(self, idx, val):
        self.update(0, 0, self.n - 1, idx, val)

# Test
data = [5, 3, 7, 9, 1, 4]
seg_max = SegmentTreeMax(data)

print(f"Max in [1, 4]: {seg_max.range_query(1, 4)}")  # max(3,7,9,1) = 9
print(f"Max in [3, 5]: {seg_max.range_query(3, 5)}")  # max(9,1,4) = 9
```

---

## 5. Range Update with Lazy Propagation

When you need to update a range of elements efficiently.

### Visual: How Lazy Propagation Works

```
  Array: [1, 2, 3, 4, 5]
  Operation: Add 2 to range [1, 3]

  ┌──────────────────────────────────────────────────────────┐
  │  WITHOUT lazy propagation:                               │
  │  Update [1,3] → recurse to each leaf → O(n) time!       │
  │                                                          │
  │  WITH lazy propagation:                                  │
  │  Mark root's children as "needs update later"            │
  │  Don't recurse further → O(log n) time!                  │
  └──────────────────────────────────────────────────────────┘

  Step 1: Add 2 to [1,3]
          Root covers [0,4], partial overlap → recurse

  Step 2: Left child covers [0,2], partial overlap
          ├── [0,1]: NO overlap with [1,3] → skip
          │   Wait, [1,1] overlaps! But [0,0] doesn't.
          │   Recurse to [0,0]: no overlap → skip
          │   Recurse to [1,1]: complete overlap!
          │   → LAZY[1,1] += 2, tree[1,1] += 2×1 = 2
          └── [2,2]: complete overlap
              → LAZY[2,2] += 2, tree[2,2] += 2×1 = 2

  Step 3: Right child covers [3,4], partial overlap
          ├── [3,3]: complete overlap → LAZY += 2
          └── [4,4]: no overlap → skip

  Step 4: Update parent sums up the tree
          tree[0] = tree[1] + tree[2] after updating

  ┌──────────────────────────────────────────────────────────┐
  │  The lazy array stores PENDING updates:                  │
  │                                                          │
  │  lazy[node] = value to ADD to all elements in node's     │
  │               range (but haven't been pushed yet)        │
  │                                                          │
  │  When do we PUSH?                                        │
  │  - Before querying a node                               │
  │  - Before updating children of a node                   │
  │                                                          │
  │  push(node, start, end):                                │
  │    if lazy[node] != 0:                                  │
  │      tree[node] += lazy[node] × (end - start + 1)       │
  │      if not leaf:                                       │
  │        lazy[left_child]  += lazy[node]                  │
  │        lazy[right_child] += lazy[node]                  │
  │      lazy[node] = 0                                     │
  └──────────────────────────────────────────────────────────┘
```

```python
class SegmentTreeLazy:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.build(data, 0, 0, self.n - 1)
    
    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self.build(data, 2 * node + 1, start, mid)
            self.build(data, 2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def push(self, node, start, end):
        """Push lazy value to children"""
        if self.lazy[node] != 0:
            # Apply pending update
            self.tree[node] += self.lazy[node] * (end - start + 1)
            
            if start != end:
                # Push to children
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
            
            self.lazy[node] = 0
    
    def update_range(self, node, start, end, l, r, val):
        """Add val to all elements in range [l, r]"""
        self.push(node, start, end)
        
        # No overlap
        if r < start or end < l:
            return
        
        # Complete overlap
        if l <= start and end <= r:
            self.lazy[node] += val
            self.push(node, start, end)
            return
        
        # Partial overlap
        mid = (start + end) // 2
        self.update_range(2 * node + 1, start, mid, l, r, val)
        self.update_range(2 * node + 2, mid + 1, end, l, r, val)
        
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def range_update(self, l, r, val):
        self.update_range(0, 0, self.n - 1, l, r, val)
    
    def query(self, node, start, end, l, r):
        """Query sum in range [l, r]"""
        self.push(node, start, end)
        
        if r < start or end < l:
            return 0
        
        if l <= start and end <= r:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_sum = self.query(2 * node + 1, start, mid, l, r)
        right_sum = self.query(2 * node + 2, mid + 1, end, l, r)
        
        return left_sum + right_sum
    
    def range_query(self, l, r):
        return self.query(0, 0, self.n - 1, l, r)

# Test
data = [1, 2, 3, 4, 5]
seg = SegmentTreeLazy(data)

print(f"Initial sum [0, 4]: {seg.range_query(0, 4)}")  # 15

seg.range_update(1, 3, 2)  # Add 2 to indices 1, 2, 3
print(f"After update [0, 4]: {seg.range_query(0, 4)}")  # 21
print(f"After update [1, 3]: {seg.range_query(1, 3)}")  # 15 (3+4+5 + 2*3)

seg.range_update(0, 2, 3)  # Add 3 to indices 0, 1, 2
print(f"After second update [0, 4]: {seg.range_query(0, 4)}")  # 30
```

**Time Complexity:** O(log n) for both update and query
**Space Complexity:** O(4n)

---

## 6. Segment Tree for Range Minimum Query

Complete implementation with all operations:

```python
class RMQSegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [float('inf')] * (4 * self.n)
        self.data = data[:]
        self.build(0, 0, self.n - 1)
    
    def build(self, node, start, end):
        if start == end:
            self.tree[node] = self.data[start]
        else:
            mid = (start + end) // 2
            self.build(2 * node + 1, start, mid)
            self.build(2 * node + 2, mid + 1, end)
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
    
    def update(self, node, start, end, idx, val):
        if start == end:
            self.data[idx] = val
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node + 1, start, mid, idx, val)
            else:
                self.update(2 * node + 2, mid + 1, end, idx, val)
            self.tree[node] = min(self.tree[2 * node + 1], 
                                  self.tree[2 * node + 2])
    
    def find_min_index(self, node, start, end, l, r):
        """Find index of minimum element in range [l, r]"""
        if r < start or end < l:
            return -1
        
        if start == end:
            return start
        
        mid = (start + end) // 2
        left_idx = self.find_min_index(2 * node + 1, start, mid, l, r)
        right_idx = self.find_min_index(2 * node + 2, mid + 1, end, l, r)
        
        if left_idx == -1:
            return right_idx
        if right_idx == -1:
            return left_idx
        
        if self.data[left_idx] <= self.data[right_idx]:
            return left_idx
        return right_idx
    
    def range_query(self, l, r):
        return self.query(0, 0, self.n - 1, l, r)
    
    def point_update(self, idx, val):
        self.update(0, 0, self.n - 1, idx, val)
    
    def find_min(self, l, r):
        """Return (min_value, min_index)"""
        min_idx = self.find_min_index(0, 0, self.n - 1, l, r)
        return self.data[min_idx], min_idx

# Test
data = [4, 2, 8, 1, 6, 3, 7]
rmq = RMQSegmentTree(data)

print(f"Min in [1, 5]: {rmq.range_query(1, 5)}")  # 1
print(f"Min element: {rmq.find_min(0, 6)}")  # (1, 3)

rmq.point_update(3, 10)
print(f"After update, min in [0, 3]: {rmq.range_query(0, 3)}")  # 2
```

---

## 7. Segment Tree for Range Sum Query

Complete implementation with lazy propagation:

```python
class SumSegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.data = data[:]
        self.build(0, 0, self.n - 1)
    
    def build(self, node, start, end):
        if start == end:
            self.tree[node] = self.data[start]
        else:
            mid = (start + end) // 2
            self.build(2 * node + 1, start, mid)
            self.build(2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def push(self, node, start, end):
        if self.lazy[node] != 0:
            self.tree[node] += self.lazy[node] * (end - start + 1)
            if start != end:
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
            self.lazy[node] = 0
    
    def update_range(self, node, start, end, l, r, val):
        self.push(node, start, end)
        
        if r < start or end < l:
            return
        
        if l <= start and end <= r:
            self.lazy[node] += val
            self.push(node, start, end)
            return
        
        mid = (start + end) // 2
        self.update_range(2 * node + 1, start, mid, l, r, val)
        self.update_range(2 * node + 2, mid + 1, end, l, r, val)
        
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def query(self, node, start, end, l, r):
        self.push(node, start, end)
        
        if r < start or end < l:
            return 0
        
        if l <= start and end <= r:
            return self.tree[node]
        
        mid = (start + end) // 2
        return self.query(2 * node + 1, start, mid, l, r) + \
               self.query(2 * node + 2, mid + 1, end, l, r)
    
    def range_sum(self, l, r):
        return self.query(0, 0, self.n - 1, l, r)
    
    def range_update(self, l, r, val):
        self.update_range(0, 0, self.n - 1, l, r, val)
    
    def point_update(self, idx, val):
        self.range_update(idx, idx, val - self.data[idx])
        self.data[idx] = val

# Test
data = [1, 3, 5, 7, 9, 11]
seg = SumSegmentTree(data)

print(f"Sum [1, 3]: {seg.range_sum(1, 3)}")  # 15
seg.range_update(1, 3, 2)
print(f"After update, sum [1, 3]: {seg.range_sum(1, 3)}")  # 21
print(f"Sum [0, 5]: {seg.range_sum(0, 5)}")  # 42
```

---

## Practice Problems

### 1. Range Sum Query Mutable (LC 307)

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
arr.update(0, 0, 4, 2, 6)  # Update index 2 to 6
print(arr.sumRange(0, 0, 4, 1, 3))  # 16
```

### 2. Range Minimum Query (LC 315)

```python
class RMQ:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [float('inf')] * (4 * self.n)
        self.nums = nums[:]
        self.build(0, 0, self.n - 1)
    
    def build(self, node, start, end):
        if start == end:
            self.tree[node] = self.nums[start]
        else:
            mid = (start + end) // 2
            self.build(2 * node + 1, start, mid)
            self.build(2 * node + 2, mid + 1, end)
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
```

### 3. Count of Range Sum (LC 327)

```python
def countRangeSum(nums, lower, upper):
    """Count range sums in [lower, upper]"""
    # Use merge sort with prefix sums
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

---

## Key Patterns for Infosys SP DSE

1. **Static Range Queries:** Use basic segment tree (sum/min/max)
2. **Dynamic Updates:** Add point update functionality
3. **Range Updates:** Use lazy propagation
4. **Complex Queries:** Combine with other techniques (binary search, etc.)

## Time & Space Complexity Summary

| Operation | Time | Space |
|-----------|------|-------|
| Build | O(n) | O(4n) |
| Query | O(log n) | O(log n) stack |
| Point Update | O(log n) | O(log n) stack |
| Range Update (Lazy) | O(log n) | O(log n) stack |

---

## Tips for Interview

1. Start with the base case (leaf nodes)
2. Explain the tree structure (complete binary tree)
3. Draw the tree for small examples
4. Handle edge cases: empty range, single element
5. For lazy propagation, explain the concept clearly
