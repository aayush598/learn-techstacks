# Median Problems - Complete Guide

## Table of Contents
1. [Find Median from Data Stream](#1-find-median-from-data-stream)
2. [Sliding Window Median](#2-sliding-window-median)
3. [IPO - Select K Projects](#3-ipo-select-k-projects)
4. [Meeting Rooms II](#4-meeting-rooms-ii)

---

## 1. Find Median from Data Stream

**Problem**: Design a data structure that supports adding integers and finding the median of all elements.

### Solution: Two Heaps

```python
import heapq

class MedianFinder:
    """Find median from data stream using two heaps."""
    
    def __init__(self):
        # Max-heap for lower half (store negatives)
        self.lower = []
        # Min-heap for upper half
        self.upper = []
    
    def add_num(self, num):
        """Add number to data structure - O(log n)."""
        # Always add to max-heap first
        heapq.heappush(self.lower, -num)
        
        # Ensure max(lower) <= min(upper)
        if self.upper and -self.lower[0] > self.upper[0]:
            val = -heapq.heappop(self.lower)
            heapq.heappush(self.upper, val)
        
        # Balance sizes: lower can have at most 1 more than upper
        if len(self.lower) > len(self.upper) + 1:
            val = -heapq.heappop(self.lower)
            heapq.heappush(self.upper, val)
        elif len(self.upper) > len(self.lower):
            val = heapq.heappop(self.upper)
            heapq.heappush(self.lower, -val)
    
    def find_median(self):
        """Find current median - O(1)."""
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        elif len(self.upper) > len(self.lower):
            return float(self.upper[0])
        else:
            return (-self.lower[0] + self.upper[0]) / 2.0

# Example usage
mf = MedianFinder()
test_cases = [5, 15, 1, 3, 8, 7, 9, 2, 6]

for num in test_cases:
    mf.add_num(num)
    print(f"Added {num:2d}, median = {mf.find_median()}")

# Output:
# Added  5, median = 5
# Added 15, median = 10.0
# Added  1, median = 5
# Added  3, median = 4.0
# Added  8, median = 5
# Added  7, median = 6.0
# Added  9, median = 7
# Added  2, median = 5.5
# Added  6, median = 6
```

### Alternative: Using SortedList

```python
from sortedcontainers import SortedList

class MedianFinderSortedList:
    """Find median using SortedList - O(log n) add, O(1) find."""
    
    def __init__(self):
        self.data = SortedList()
    
    def add_num(self, num):
        self.data.add(num)
    
    def find_median(self):
        n = len(self.data)
        if n % 2 == 1:
            return self.data[n // 2]
        else:
            return (self.data[n // 2 - 1] + self.data[n // 2]) / 2.0
```

---

## 2. Sliding Window Median

**Problem**: Find the median of all elements in a sliding window of size k.

### Solution: Two Heaps with Lazy Deletion

```python
import heapq
from collections import defaultdict

class SlidingWindowMedian:
    """Find median in sliding window using two heaps."""
    
    def __init__(self):
        self.lower = []  # max-heap (negate values)
        self.upper = []  # min-heap
        self.lazy_deletes = defaultdict(int)
        self.lower_size = 0
        self.upper_size = 0
    
    def _prune_lower(self):
        """Remove deleted elements from lower heap."""
        while self.lower and self.lazy_deletes[-self.lower[0]] > 0:
            self.lazy_deletes[-self.lower[0]] -= 1
            heapq.heappop(self.lower)
    
    def _prune_upper(self):
        """Remove deleted elements from upper heap."""
        while self.upper and self.lazy_deletes[self.upper[0]] > 0:
            self.lazy_deletes[self.upper[0]] -= 1
            heapq.heappop(self.upper)
    
    def _rebalance(self):
        """Ensure heaps are balanced."""
        # Lower can have at most 1 more than upper
        if self.lower_size > self.upper_size + 1:
            self._prune_lower()
            val = -heapq.heappop(self.lower)
            self.lower_size -= 1
            heapq.heappush(self.upper, val)
            self.upper_size += 1
            self._prune_upper()
        elif self.upper_size > self.lower_size:
            self._prune_upper()
            val = heapq.heappop(self.upper)
            self.upper_size -= 1
            heapq.heappush(self.lower, -val)
            self.lower_size += 1
            self._prune_lower()
    
    def add(self, num):
        """Add number to heaps."""
        if not self.lower or num <= -self.lower[0]:
            heapq.heappush(self.lower, -num)
            self.lower_size += 1
        else:
            heapq.heappush(self.upper, num)
            self.upper_size += 1
        self._rebalance()
    
    def remove(self, num):
        """Mark number for lazy deletion."""
        self.lazy_deletes[num] += 1
        if num <= -self.lower[0]:
            self.lower_size -= 1
        else:
            self.upper_size -= 1
        self._rebalance()
    
    def get_median(self):
        """Get current median."""
        self._prune_lower()
        self._prune_upper()
        
        if self.lower_size > self.upper_size:
            return float(-self.lower[0])
        elif self.upper_size > self.lower_size:
            return float(self.upper[0])
        else:
            return (-self.lower[0] + self.upper[0]) / 2.0
    
    def median_sliding_window(self, nums, k):
        """Find medians of all sliding windows."""
        if not nums or k == 0:
            return []
        
        result = []
        swm = SlidingWindowMedian()
        
        for i in range(len(nums)):
            swm.add(nums[i])
            
            if i >= k:
                swm.remove(nums[i - k])
            
            if i >= k - 1:
                result.append(swm.get_median())
        
        return result

# Example
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
swm = SlidingWindowMedian()
print(swm.median_sliding_window(nums, k))
# Output: [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
```

### Simpler Alternative: Using SortedList

```python
from sortedcontainers import SortedList

def median_sliding_window_sorted(nums, k):
    """Find medians using SortedList."""
    window = SortedList()
    result = []
    
    for i, num in enumerate(nums):
        window.add(num)
        
        if len(window) > k:
            window.remove(nums[i - k])
        
        if len(window) == k:
            if k % 2 == 1:
                result.append(window[k // 2])
            else:
                result.append((window[k // 2 - 1] + window[k // 2]) / 2.0)
    
    return result

# Example
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(median_sliding_window_sorted(nums, k))
# Output: [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
```

---

## 3. IPO - Select K Projects

**Problem**: You have `k` projects to fund. Each project gives profit `profits[i]` and requires capital `capital[i]`. Find maximum final capital.

```python
import heapq

def find_maximized_capital(k, w, profits, capital):
    """
    Find maximized capital after completing at most k projects.
    :param k: number of projects to complete
    :param w: initial capital
    :param profits: list of profits
    :param capital: list of required capitals
    :return: maximum final capital
    """
    # Pair projects by capital requirement
    projects = sorted(zip(capital, profits))
    
    # Max-heap for available profits
    max_heap = []
    project_idx = 0
    current_capital = w
    
    for _ in range(k):
        # Add all affordable projects to max-heap
        while project_idx < len(projects) and projects[project_idx][0] <= current_capital:
            heapq.heappush(max_heap, -projects[project_idx][1])
            project_idx += 1
        
        # If no project available, break
        if not max_heap:
            break
        
        # Take the most profitable project
        current_capital += -heapq.heappop(max_heap)
    
    return current_capital

# Example 1
k = 2
w = 0
profits = [1, 2, 3]
capital = [0, 1, 1]
print(find_maximized_capital(k, w, profits, capital))
# Output: 4
# Take project with profit 1 (capital 0), then project with profit 3 (capital 1)

# Example 2
k = 3
w = 0
profits = [1, 2, 3, 4, 5]
capital = [0, 1, 2, 3, 4]
print(find_maximized_capital(k, w, profits, capital))
# Output: 8
```

### Step-by-step Visualization

```python
def find_maximized_capital_verbose(k, w, profits, capital):
    """Verbose version to show the process."""
    projects = sorted(zip(capital, profits))
    print(f"Sorted projects (capital, profit): {projects}")
    
    max_heap = []
    project_idx = 0
    current_capital = w
    
    for round_num in range(k):
        # Add affordable projects
        while project_idx < len(projects) and projects[project_idx][0] <= current_capital:
            heapq.heappush(max_heap, -projects[project_idx][1])
            print(f"  Added project (cap={projects[project_idx][0]}, prof={projects[project_idx][1]}) to heap")
            project_idx += 1
        
        print(f"Round {round_num + 1}: Available projects in heap: {[-p for p in max_heap]}")
        
        if not max_heap:
            print("  No affordable projects available!")
            break
        
        profit = -heapq.heappop(max_heap)
        current_capital += profit
        print(f"  Took project with profit {profit}, new capital = {current_capital}")
    
    print(f"Final capital: {current_capital}")
    return current_capital

# Example
k = 2
w = 0
profits = [1, 2, 3]
capital = [0, 1, 1]
find_maximized_capital_verbose(k, w, profits, capital)
```

---

## 4. Meeting Rooms II

**Problem**: Given an array of meeting time intervals, find the minimum number of conference rooms required.

### Solution 1: Min Heap - O(n log n)

```python
import heapq

def min_meeting_rooms_heap(intervals):
    """Find minimum meeting rooms using min-heap."""
    if not intervals:
        return 0
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    # Min-heap to track end times of active meetings
    heap = []
    
    for start, end in intervals:
        # If earliest ending meeting has ended, remove it
        if heap and heap[0] <= start:
            heapq.heappop(heap)
        
        # Add current meeting's end time
        heapq.heappush(heap, end)
    
    return len(heap)

# Example
intervals = [[0, 30], [5, 10], [15, 20]]
print(min_meeting_rooms_heap(intervals))  # 2
# Meeting room 1: [0, 30]
# Meeting room 2: [5, 10] then [15, 20]
```

### Solution 2: Chronological Ordering - O(n log n)

```python
def min_meeting_rooms_chronological(intervals):
    """Find minimum meeting rooms using start/end arrays."""
    if not intervals:
        return 0
    
    # Separate and sort start and end times
    starts = sorted([i[0] for i in intervals])
    ends = sorted([i[1] for i in intervals])
    
    rooms = 0
    max_rooms = 0
    end_ptr = 0
    
    for start in starts:
        # If meeting starts after earliest meeting ends, reuse room
        if start >= ends[end_ptr]:
            end_ptr += 1
        else:
            rooms += 1
        
        max_rooms = max(max_rooms, rooms)
    
    return max_rooms

# Example
intervals = [[0, 30], [5, 10], [15, 20]]
print(min_meeting_rooms_chronological(intervals))  # 2
```

### Solution 3: Line Sweep - O(n log n)

```python
def min_meeting_rooms_sweep(intervals):
    """Find minimum meeting rooms using line sweep."""
    events = []
    
    for start, end in intervals:
        events.append((start, 1))   # Meeting starts
        events.append((end, -1))    # Meeting ends
    
    # Sort events: by time, then by type (end before start for same time)
    events.sort(key=lambda x: (x[0], x[1]))
    
    current_rooms = 0
    max_rooms = 0
    
    for time, event_type in events:
        current_rooms += event_type
        max_rooms = max(max_rooms, current_rooms)
    
    return max_rooms

# Example
intervals = [[0, 30], [5, 10], [15, 20]]
print(min_meeting_rooms_sweep(intervals))  # 2
```

### Extended: Meeting Rooms with Resource Allocation

```python
import heapq

def allocate_meeting_rooms(intervals, rooms):
    """
    Allocate meetings to rooms and return allocation.
    Returns list of (room_id, start, end) for each meeting.
    """
    if not intervals:
        return []
    
    # Sort by start time
    sorted_meetings = sorted(enumerate(intervals), key=lambda x: x[1][0])
    
    # Min-heap: (end_time, room_id)
    available_rooms = list(range(rooms))
    heapq.heapify(available_rooms)
    
    occupied_rooms = []  # (end_time, room_id)
    allocation = []
    
    for idx, (start, end) in sorted_meetings:
        # Free up rooms that have ended
        while occupied_rooms and occupied_rooms[0][0] <= start:
            _, room_id = heapq.heappop(occupied_rooms)
            heapq.heappush(available_rooms, room_id)
        
        if available_rooms:
            room_id = heapq.heappop(available_rooms)
            heapq.heappush(occupied_rooms, (end, room_id))
            allocation.append((idx, room_id, start, end))
        else:
            # No room available, meeting cannot be scheduled
            allocation.append((idx, -1, start, end))
    
    return allocation

# Example
intervals = [[0, 30], [5, 10], [15, 20]]
rooms = 2
allocation = allocate_meeting_rooms(intervals, rooms)
print("Allocations:")
for idx, room, start, end in allocation:
    status = f"Room {room}" if room != -1 else "REJECTED"
    print(f"  Meeting {idx} [{start}, {end}] -> {status}")
```

---

## Quick Reference: Median Patterns

| Problem | Key Insight | Approach |
|---------|-------------|----------|
| Running Median | Two heaps balance | Max-heap + Min-heap |
| Sliding Window Median | Lazy deletion | Two heaps + hash map |
| IPO | Greedy + heap | Max-heap for profits |
| Meeting Rooms | Line sweep or heap | Min-heap for end times |

---

## Complexity Analysis

| Problem | Time | Space |
|---------|------|-------|
| Find Median from Data Stream | O(log n) add, O(1) find | O(n) |
| Sliding Window Median | O(n log k) | O(k) |
| IPO | O(n log n + k log n) | O(n) |
| Meeting Rooms II | O(n log n) | O(n) |
