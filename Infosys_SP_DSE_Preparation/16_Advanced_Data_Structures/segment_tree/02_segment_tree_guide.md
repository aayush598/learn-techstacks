# Segment Tree Guide

## What is Segment Tree?

A Segment Tree is a binary tree data structure used for storing information about intervals/segments. It supports:
1. **Range queries** (sum, min, max, gcd, etc.) in O(log n)
2. **Point updates** in O(log n)
3. **Range updates** with lazy propagation in O(log n)

**When to use:**
- Multiple range queries on static/dynamic array
- Need to update values and query ranges efficiently
- Problems involving intervals

**Comparison with other structures:**
| Operation | Array | Prefix Sum | Segment Tree |
|-----------|-------|------------|--------------|
| Point Update | O(1) | O(n) | O(log n) |
| Range Query | O(n) | O(1) | O(log n) |
| Range Update | O(n) | O(n) | O(log n) |

---

## 1. Build Segment Tree

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

```python
class SegmentTreeSum:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.build(data, 0, 0, self.n - 1)
    
    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self.build(data, 2 * node + 1, start, mid)
            self.build(data, 2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
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
