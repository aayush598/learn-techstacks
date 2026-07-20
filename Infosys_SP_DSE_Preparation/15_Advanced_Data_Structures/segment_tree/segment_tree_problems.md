# Segment Tree Problems

## Problem 1: Kth Number in Stream

**Problem:** Given a stream of numbers, find the kth smallest number at any point.

**Approach:** Use a segment tree to count frequencies and binary search for kth element.

```python
class KthNumberStream:
    def __init__(self, max_val):
        self.max_val = max_val
        self.tree = [0] * (4 * max_val)
        self.counts = [0] * (max_val + 1)
    
    def update(self, node, start, end, idx, delta):
        if start == end:
            self.tree[node] += delta
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node + 1, start, mid, idx, delta)
            else:
                self.update(2 * node + 2, mid + 1, end, idx, delta)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def query_kth(self, node, start, end, k):
        """Find kth smallest element"""
        if start == end:
            return start
        
        mid = (start + end) // 2
        left_count = self.tree[2 * node + 1]
        
        if k <= left_count:
            return self.query_kth(2 * node + 1, start, mid, k)
        else:
            return self.query_kth(2 * node + 2, mid + 1, end, k - left_count)
    
    def add_number(self, num):
        self.update(0, 0, self.max_val, num, 1)
        self.counts[num] += 1
    
    def remove_number(self, num):
        if self.counts[num] > 0:
            self.update(0, 0, self.max_val, num, -1)
            self.counts[num] -= 1
    
    def get_kth_smallest(self, k):
        if k > self.tree[0]:
            return -1
        return self.query_kth(0, 0, self.max_val, k)

# Test
stream = KthNumberStream(100)
stream.add_number(5)
stream.add_number(3)
stream.add_number(8)
stream.add_number(1)
stream.add_number(4)

print(f"1st smallest: {stream.get_kth_smallest(1)}")  # 1
print(f"3rd smallest: {stream.get_kth_smallest(3)}")  # 4
print(f"5th smallest: {stream.get_kth_smallest(5)}")  # 8
```

**Time Complexity:** O(log max_val) for add/remove, O(log max_val) for query
**Space Complexity:** O(max_val)

---

## Problem 2: Number of Elements Greater Than X in Range

**Problem:** Given an array, answer queries: count elements greater than X in range [l, r].

**Approach:** Use persistent segment tree or merge sort tree.

```python
class MergeSortTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [[] for _ in range(4 * self.n)]
        self.build(data, 0, 0, self.n - 1)
    
    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = [data[start]]
        else:
            mid = (start + end) // 2
            self.build(data, 2 * node + 1, start, mid)
            self.build(data, 2 * node + 2, mid + 1, end)
            
            # Merge sorted lists
            left = self.tree[2 * node + 1]
            right = self.tree[2 * node + 2]
            self.tree[node] = self.merge(left, right)
    
    def merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def count_greater(self, node, start, end, l, r, x):
        """Count elements greater than x in range [l, r]"""
        if r < start or end < l:
            return 0
        
        if l <= start and end <= r:
            # Binary search for first element greater than x
            arr = self.tree[node]
            lo, hi = 0, len(arr)
            while lo < hi:
                mid = (lo + hi) // 2
                if arr[mid] <= x:
                    lo = mid + 1
                else:
                    hi = mid
            return len(arr) - lo
        
        mid = (start + end) // 2
        left_count = self.count_greater(2 * node + 1, start, mid, l, r, x)
        right_count = self.count_greater(2 * node + 2, mid + 1, end, l, r, x)
        
        return left_count + right_count
    
    def query(self, l, r, x):
        return self.count_greater(0, 0, self.n - 1, l, r, x)

# Alternative: Using offline queries with BIT
def count_greater_offline(nums, queries):
    """Count elements > x in [l, r] using offline processing"""
    from bisect import bisect_right
    
    n = len(nums)
    
    # Create sorted copy for coordinate compression
    sorted_nums = sorted(set(nums))
    compressed = {v: i + 1 for i, v in enumerate(sorted_nums)}
    
    # Sort queries by x in descending order
    indexed_queries = [(x, l, r, i) for i, (l, r, x) in enumerate(queries)]
    indexed_queries.sort(reverse=True)
    
    # Use BIT to mark elements
    bit = [0] * (n + 2)
    
    def update(idx, delta):
        while idx <= n:
            bit[idx] += delta
            idx += idx & (-idx)
    
    def query(idx):
        result = 0
        while idx > 0:
            result += bit[idx]
            idx -= idx & (-idx)
        return result
    
    def range_query(l, r):
        return query(r) - query(l - 1)
    
    # Process elements in descending order
    element_index = [(nums[i], i) for i in range(n)]
    element_index.sort(reverse=True)
    
    results = [0] * len(queries)
    elem_ptr = 0
    
    for x, l, r, idx in indexed_queries:
        # Add all elements > x
        while elem_ptr < len(element_index) and element_index[elem_ptr][0] > x:
            pos = element_index[elem_ptr][1]
            update(pos + 1, 1)
            elem_ptr += 1
        
        results[idx] = range_query(l + 1, r + 1)
    
    return results

# Test MergeSortTree
data = [1, 5, 3, 7, 9, 2, 6]
mst = MergeSortTree(data)

print(f"Elements > 4 in [0, 3]: {mst.query(0, 3, 4)}")  # 2 (5, 7)
print(f"Elements > 3 in [0, 6]: {mst.query(0, 6, 3)}")  # 4 (5, 7, 9, 6)

# Test offline approach
nums = [1, 5, 3, 7, 9, 2, 6]
queries = [(0, 3, 4), (0, 6, 3)]
print(f"Offline results: {count_greater_offline(nums, queries)}")  # [2, 4]
```

**Time Complexity:** O(n log n) build, O(log^2 n) query for MergeSortTree
**Time Complexity:** O((n + q) log n) for offline approach

---

## Problem 3: Merge Sort with Segment Tree (Count Inversions)

**Problem:** Count number of inversions in an array.

**Approach:** Use merge sort technique - count inversions during merge phase.

```python
def count_inversions_merge_sort(nums):
    """Count inversions using merge sort"""
    temp = [0] * len(nums)
    return merge_sort_count(nums, temp, 0, len(nums) - 1)

def merge_sort_count(arr, temp, left, right):
    inv_count = 0
    if left < right:
        mid = (left + right) // 2
        inv_count += merge_sort_count(arr, temp, left, mid)
        inv_count += merge_sort_count(arr, temp, mid + 1, right)
        inv_count += merge_count(arr, temp, left, mid, right)
    return inv_count

def merge_count(arr, temp, left, mid, right):
    i = left
    j = mid + 1
    k = left
    inv_count = 0
    
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            # All remaining elements in left subarray are > arr[j]
            inv_count += (mid - i + 1)
            temp[k] = arr[j]
            j += 1
        k += 1
    
    while i <= mid:
        temp[k] = arr[i]
        i += 1
        k += 1
    
    while j <= right:
        temp[k] = arr[j]
        j += 1
        k += 1
    
    for i in range(left, right + 1):
        arr[i] = temp[i]
    
    return inv_count

# Alternative: Using BIT
def count_inversions_bit(nums):
    """Count inversions using BIT"""
    # Coordinate compression
    sorted_nums = sorted(set(nums))
    rank = {v: i + 1 for i, v in enumerate(sorted_nums)}
    
    n = len(nums)
    bit = [0] * (n + 2)
    
    def update(idx, delta):
        while idx <= n:
            bit[idx] += delta
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
        update(r, 1)
    
    return inv_count

# Test
nums = [2, 4, 1, 3, 5]
print(f"Inversions (merge sort): {count_inversions_merge_sort(nums[:])}")  # 3
print(f"Inversions (BIT): {count_inversions_bit(nums)}")  # 3

nums2 = [5, 4, 3, 2, 1]
print(f"Inversions (worst case): {count_inversions_merge_sort(nums2[:])}")  # 10
```

**Time Complexity:** O(n log n) for both methods
**Space Complexity:** O(n)

---

## Problem 4: Reverse Pairs Using Segment Tree

**Problem:** Count pairs (i, j) where i < j and nums[i] > 2 * nums[j].

**Approach:** Use BIT or merge sort to count elements > 2*nums[j] in prefix.

```python
def reverse_pairs_merge_sort(nums):
    """Count reverse pairs using merge sort"""
    return merge_sort_reverse_pairs(nums[:], 0, len(nums) - 1)

def merge_sort_reverse_pairs(arr, left, right):
    if left >= right:
        return 0
    
    mid = (left + right) // 2
    count = 0
    count += merge_sort_reverse_pairs(arr, left, mid)
    count += merge_sort_reverse_pairs(arr, mid + 1, right)
    count += count_cross_pairs(arr, left, mid, right)
    merge(arr, left, mid, right)
    
    return count

def count_cross_pairs(arr, left, mid, right):
    """Count pairs where i in [left, mid] and j in [mid+1, right]"""
    count = 0
    j = mid + 1
    
    for i in range(left, mid + 1):
        while j <= right and arr[i] > 2 * arr[j]:
            j += 1
        count += j - (mid + 1)
    
    return count

def merge(arr, left, mid, right):
    temp = []
    i, j = left, mid + 1
    
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1
    
    temp.extend(arr[i:mid + 1])
    temp.extend(arr[j:right + 1])
    
    for i in range(len(temp)):
        arr[left + i] = temp[i]

def reverse_pairs_bit(nums):
    """Count reverse pairs using BIT"""
    # For each j, count i < j where nums[i] > 2*nums[j]
    # Or equivalently, for each i, count j > i where nums[j] < nums[i]/2
    
    sorted_vals = sorted(set(nums))
    rank = {v: i + 1 for i, v in enumerate(sorted_vals)}
    
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
    
    count = 0
    
    # Process from right to left
    for i in range(n - 1, -1, -1):
        # Find elements < nums[i] / 2
        target = nums[i] / 2
        # Find rank of first element >= target
        lo, hi = 0, len(sorted_vals) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if sorted_vals[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        
        # Count elements with rank <= hi + 1
        if hi >= 0:
            count += query(hi + 1)
        
        update(rank[nums[i]])
    
    return count

# Test
nums = [1, 3, 2, 3, 1]
print(f"Reverse pairs (merge sort): {reverse_pairs_merge_sort(nums)}")  # 2
print(f"Reverse pairs (BIT): {reverse_pairs_bit(nums)}")  # 2

nums2 = [2, 4, 3, 5, 1]
print(f"Reverse pairs: {reverse_pairs_merge_sort(nums2)}")  # 3
```

**Time Complexity:** O(n log n) for both methods
**Space Complexity:** O(n)

---

## Problem 5: Maximum in Range with Updates

**Problem:** Find maximum element in range [l, r] with point updates.

```python
class MaxSegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [float('-inf')] * (4 * self.n)
        self.build(0, 0, self.n - 1, data)
    
    def build(self, node, start, end, data):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self.build(2 * node + 1, start, mid, data)
            self.build(2 * node + 2, mid + 1, end, data)
            self.tree[node] = max(self.tree[2 * node + 1], 
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
            self.tree[node] = max(self.tree[2 * node + 1], 
                                  self.tree[2 * node + 2])
    
    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return float('-inf')
        
        if l <= start and end <= r:
            return self.tree[node]
        
        mid = (start + end) // 2
        return max(self.query(2 * node + 1, start, mid, l, r),
                   self.query(2 * node + 2, mid + 1, end, l, r))
    
    def point_update(self, idx, val):
        self.update(0, 0, self.n - 1, idx, val)
    
    def range_max(self, l, r):
        return self.query(0, 0, self.n - 1, l, r)

# Test
data = [1, 3, 5, 7, 9, 11]
seg = MaxSegmentTree(data)

print(f"Max in [1, 4]: {seg.range_max(1, 4)}")  # 9
seg.point_update(2, 15)
print(f"After update, Max in [0, 3]: {seg.range_max(0, 3)}")  # 15

# Sliding Window Maximum using Segment Tree
def sliding_window_max(nums, k):
    """Find maximum in each sliding window of size k"""
    if not nums or k <= 0:
        return []
    
    seg = MaxSegmentTree(nums)
    result = []
    
    for i in range(len(nums) - k + 1):
        result.append(seg.range_max(i, i + k - 1))
    
    return result

print(f"Sliding window max [1,3,-1,-3,5,3,6,7], k=3: {sliding_window_max([1,3,-1,-3,5,3,6,7], 3)}")
# Output: [3, 3, 5, 5, 6, 7]
```

**Time Complexity:** O(n) build, O(log n) query/update
**Space Complexity:** O(n)

---

## Problem 6: Subarray Sum Divisible by K (Segment Tree Variant)

```python
def subarrays_divisible_by_k(nums, k):
    """Count subarrays with sum divisible by k"""
    # Use prefix sum + frequency counting
    prefix_mod = [0] * (k + 1)
    prefix_mod[0] = 1  # Empty prefix
    
    current_sum = 0
    count = 0
    
    for num in nums:
        current_sum += num
        mod = current_sum % k
        
        count += prefix_mod[mod]
        prefix_mod[mod] += 1
    
    return count

# Alternative: Using segment tree to count frequencies
def subarrays_divisible_by_k_segtree(nums, k):
    """Using segment tree for range frequency queries"""
    # This is more complex but demonstrates segment tree usage
    # Coordinate compress and use segment tree
    
    # For this problem, the simpler approach is O(n)
    return subarrays_divisible_by_k(nums, k)

print(subarrays_divisible_by_k([4, 5, 0, -2, -3, 1], 5))  # 7
```

---

## Problem 7: Range Frequency Query

```python
class RangeFreqQuery:
    def __init__(self, arr):
        from collections import defaultdict
        
        self.n = len(arr)
        # For each value, store sorted list of indices
        self.positions = defaultdict(list)
        
        for i, num in enumerate(arr):
            self.positions[num].append(i)
    
    def query(self, left, right, value):
        """Count occurrences of value in [left, right]"""
        if value not in self.positions:
            return 0
        
        positions = self.positions[value]
        
        # Binary search for first position >= left
        lo, hi = 0, len(positions)
        while lo < hi:
            mid = (lo + hi) // 2
            if positions[mid] < left:
                lo = mid + 1
            else:
                hi = mid
        
        start = lo
        
        # Binary search for first position > right
        lo, hi = 0, len(positions)
        while lo < hi:
            mid = (lo + hi) // 2
            if positions[mid] <= right:
                lo = mid + 1
            else:
                hi = mid
        
        end = lo
        
        return end - start

# Test
arr = [1, 1, 2, 2, 2, 3]
rq = RangeFreqQuery(arr)
print(rq.query(0, 5, 2))  # 3
print(rq.query(0, 2, 1))  # 2
```

**Time Complexity:** O(n) build, O(log n) query
**Space Complexity:** O(n)

---

## Problem 8: Count Smaller Numbers After Self

```python
def count_smaller_after_self(nums):
    """Count smaller elements after self using segment tree"""
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
    
    result = []
    
    # Process from right to left
    for i in range(n - 1, -1, -1):
        r = rank[nums[i]]
        result.append(query(r - 1))
        update(r)
    
    return result[::-1]

# Alternative: Using merge sort
def count_smaller_merge_sort(nums):
    """Count smaller using merge sort"""
    indices = list(range(len(nums)))
    result = [0] * len(nums)
    
    def merge_sort(arr, left, right):
        if left >= right:
            return
        
        mid = (left + right) // 2
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        merge(arr, left, mid, right)
    
    def merge(arr, left, mid, right):
        temp = []
        i, j = left, mid + 1
        right_count = 0
        
        while i <= mid and j <= right:
            if nums[arr[j]] < nums[arr[i]]:
                temp.append(arr[j])
                right_count += 1
                j += 1
            else:
                result[arr[i]] += right_count
                temp.append(arr[i])
                i += 1
        
        while i <= mid:
            result[arr[i]] += right_count
            temp.append(arr[i])
            i += 1
        
        while j <= right:
            temp.append(arr[j])
            j += 1
        
        for i in range(len(temp)):
            arr[left + i] = temp[i]
    
    merge_sort(indices, 0, len(indices) - 1)
    return result

# Test
nums = [5, 2, 6, 1]
print(f"Count smaller (BIT): {count_smaller_after_self(nums)}")  # [2, 1, 1, 0]
print(f"Count smaller (merge sort): {count_smaller_merge_sort(nums)}")  # [2, 1, 1, 0]
```

**Time Complexity:** O(n log n) for both methods
**Space Complexity:** O(n)

---

## Problem 9: Range Sum Query with Updates

```python
class RangeSumQuery:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
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

# Test
nums = [1, 2, 3, 4, 5]
rsq = RangeSumQuery(nums)

print(f"Sum [0, 4]: {rsq.range_sum(0, 4)}")  # 15
rsq.range_update(1, 3, 2)
print(f"After update, Sum [0, 4]: {rsq.range_sum(0, 4)}")  # 21
print(f"Sum [1, 3]: {rsq.range_sum(1, 3)}")  # 15
```

---

## Problem 10: Find Median from Data Stream

```python
class MedianFinder:
    def __init__(self):
        self.nums = []
        self.sorted_nums = []
    
    def addNum(self, num: int) -> None:
        # Insert in sorted order using binary search
        from bisect import bisect_left
        idx = bisect_left(self.sorted_nums, num)
        self.sorted_nums.insert(idx, num)
    
    def findMedian(self) -> float:
        n = len(self.sorted_nums)
        if n % 2 == 1:
            return self.sorted_nums[n // 2]
        else:
            return (self.sorted_nums[n // 2 - 1] + self.sorted_nums[n // 2]) / 2

# Alternative: Using two heaps (more efficient)
import heapq

class MedianFinderHeap:
    def __init__(self):
        self.max_heap = []  # Lower half (stores negative values)
        self.min_heap = []  # Upper half
    
    def addNum(self, num: int) -> None:
        heapq.heappush(self.max_heap, -num)
        heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        
        if len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))
    
    def findMedian(self) -> float:
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        return (-self.max_heap[0] + self.min_heap[0]) / 2

# Test
mf = MedianFinder()
mf.addNum(1)
mf.addNum(2)
print(f"Median: {mf.findMedian()}")  # 1.5
mf.addNum(3)
print(f"Median: {mf.findMedian()}")  # 2

mf_heap = MedianFinderHeap()
mf_heap.addNum(1)
mf_heap.addNum(2)
print(f"Heap Median: {mf_heap.findMedian()}")  # 1.5
mf_heap.addNum(3)
print(f"Heap Median: {mf_heap.findMedian()}")  # 2
```

---

## Summary of Techniques

| Problem | Optimal Approach | Time |
|---------|-----------------|------|
| Kth Number in Stream | Segment Tree + Binary Search | O(log max) |
| Greater Than X in Range | Merge Sort Tree | O(log² n) |
| Count Inversions | Merge Sort / BIT | O(n log n) |
| Reverse Pairs | Merge Sort / BIT | O(n log n) |
| Maximum in Range | Segment Tree | O(log n) |
| Range Frequency Query | Position Lists + Binary Search | O(log n) |
| Count Smaller After Self | BIT / Merge Sort | O(n log n) |

---

## Tips for Infosys SP DSE

1. **Merge Sort Tree:** For range queries involving order statistics
2. **Offline Processing:** When queries can be reordered
3. **BIT:** When only prefix queries are needed
4. **Lazy Propagation:** For range updates with range queries
5. **Coordinate Compression:** When values are large but sparse
