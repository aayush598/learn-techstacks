# Sorting Tricks for Competitive Programming

## 1. Custom Comparator Using functools.cmp_to_key

```python
from functools import cmp_to_key

# Sort by absolute value
arr = [-3, 1, -4, 1, 5]
arr.sort(key=cmp_to_key(lambda a, b: abs(a) - abs(b)))
# [-3, 1, 1, -4, 5] or [1, -3, 1, -4, 5] (stable)

# Sort even numbers before odd, then by value
arr = [3, 2, 5, 1, 4]
arr.sort(key=cmp_to_key(lambda a, b: (a % 2) - (b % 2) or a - b))
# [2, 4, 1, 3, 5]

# Sort strings by length, then alphabetically
words = ["banana", "hi", "apple", "ok"]
words.sort(key=cmp_to_key(lambda a, b: len(a) - len(b) or (a > b) - (a < b)))
# ['hi', 'ok', 'apple', 'banana']
```

---

## 2. Sort Strings by Length, by Frequency

```python
# By length
words = ["apple", "hi", "banana", "ok"]
words.sort(key=len)
# ['hi', 'ok', 'apple', 'banana']

# By frequency (most frequent first)
from collections import Counter
s = "tree"
freq = Counter(s)
result = sorted(s, key=lambda x: (-freq[x], x))
# 'eert' or 'eetr' (both valid, sorted by freq desc, then char)

# Sort characters by frequency in string
def frequency_sort(s):
    freq = Counter(s)
    return ''.join(sorted(s, key=lambda x: (-freq[x], x)))
```

---

## 3. Interval Scheduling (Sort by End Time)

```python
def max_non_overlapping_intervals(intervals):
    """Select maximum number of non-overlapping intervals."""
    intervals.sort(key=lambda x: x[1])  # Sort by end time
    count = 0
    last_end = float('-inf')
    
    for start, end in intervals:
        if start >= last_end:
            count += 1
            last_end = end
    
    return count

# Example: intervals=[[1,2],[2,3],[1,3],[3,4]]
# Sorted by end: [[1,2],[2,3],[1,3],[3,4]]
# Select [1,2] -> [2,3] -> [3,4] = 3 intervals
# Time: O(n log n), Space: O(1)
```

---

## 4. Meeting Rooms Problem (LeetCode 252)

```python
def can_attend_meetings(intervals):
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True

# Meeting Rooms II (LeetCode 253) - min rooms needed
import heapq
def min_meeting_rooms(intervals):
    intervals.sort(key=lambda x: x[0])
    heap = []  # End times of ongoing meetings
    
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)
        else:
            heapq.heappush(heap, end)
    
    return len(heap)
```

---

## 5. Sort Colors Without Sorting (Dutch National Flag - LeetCode 75)

```python
def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1

# Three-way partition
# All 0s before low, all 1s between low and high, all 2s after high
# Time: O(n), Space: O(1), One pass
```

---

## 6. Merge Intervals (LeetCode 56)

```python
def merge_intervals(intervals):
    if not intervals:
        return []
    
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:  # Overlapping
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    
    return merged

# Example: [[1,3],[2,6],[8,10],[15,18]]
# Sorted: [[1,3],[2,6],[8,10],[15,18]]
# Merge [1,3] and [2,6] -> [1,6]
# [8,10] no overlap -> keep
# [15,18] no overlap -> keep
# Result: [[1,6],[8,10],[15,18]]
# Time: O(n log n), Space: O(1) excluding output
```

---

## 7. Insert Interval (LeetCode 57)

```python
def insert_interval(intervals, new_interval):
    result = []
    i = 0
    n = len(intervals)
    
    # Add all intervals before new_interval
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1
    
    # Merge overlapping intervals
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)
    
    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1
    
    return result
```

---

## 8. Non-overlapping Intervals (LeetCode 435)

```python
def erase_overlap_intervals(intervals):
    """Minimize removals to make all intervals non-overlapping."""
    if not intervals:
        return 0
    
    intervals.sort(key=lambda x: x[1])  # Sort by end time
    count = 0
    last_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < last_end:
            count += 1  # Must remove this interval
        else:
            last_end = intervals[i][1]
    
    return count
# Time: O(n log n), Space: O(1)
```

---

## 9. Minimum Number of Arrows to Burst Balloons (LeetCode 452)

```python
def find_min_arrows(points):
    """Find min arrows to burst all balloons (each balloon is [start, end])."""
    if not points:
        return 0
    
    points.sort(key=lambda x: x[1])  # Sort by end
    arrows = 1
    last_end = points[0][1]
    
    for start, end in points[1:]:
        if start > last_end:  # New arrow needed
            arrows += 1
            last_end = end
    
    return arrows
# Time: O(n log n), Space: O(1)
```

---

## 10. Sort by Custom Tuple Key

```python
# Multi-level sorting
students = [("Alice", 90), ("Bob", 85), ("Charlie", 90)]
students.sort(key=lambda x: (-x[1], x[0]))  # Score desc, then name asc
# [('Alice', 90), ('Charlie', 90), ('Bob', 85)]

# Sort matrix rows by sum
matrix = [[3, 1, 2], [1, 1, 1], [2, 2, 3]]
matrix.sort(key=sum)
# [[1,1,1], [3,1,2], [2,2,3]]

# Sort by last element
arr = [(1, 3), (2, 1), (3, 2)]
arr.sort(key=lambda x: x[-1])
# [(2,1), (3,2), (1,3)]
```

---

## Summary

| Trick | When to Use |
|-------|------------|
| Sort by end time | Interval scheduling, max non-overlapping |
| Sort by start time | Merge intervals, insert interval |
| cmp_to_key | Complex comparisons |
| Tuple key | Multi-level sorting |
| Dutch flag | 3-element sorting in O(n) |
| Heap + sort | Meeting rooms II |
