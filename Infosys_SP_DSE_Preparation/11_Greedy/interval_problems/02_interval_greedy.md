# Interval Problems - Complete Guide

## Table of Contents
1. [Merge Intervals](#1-merge-intervals)
2. [Insert Interval](#2-insert-interval)
3. [Non-overlapping Intervals](#3-non-overlapping-intervals)
4. [Minimum Arrows to Burst Balloons](#4-minimum-arrows-to-burst-balloons)
5. [Meeting Rooms I and II](#5-meeting-rooms-i-and-ii)
6. [Interval Partitioning](#6-interval-partitioning)

---

## 1. Merge Intervals

**Problem**: Given a collection of intervals, merge all overlapping intervals.

### Visual Walkthrough

```
  INPUT: [[1, 3], [2, 6], [8, 10], [15, 18]]
  
  STEP 1: Sort by start time → already sorted
  
  TIMELINE VISUALIZATION:
  Time:  0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18
         │  ├──[1──3]──┤           │           │                    │
         │     ├──[2──────6]──┤    │           │                    │
         │                              ├──[8──10]──┤               │
         │                                                           ├──[15─18]──┤
  
  STEP 2: Process each interval:
  ┌──────────────────────────────────────────────────────────────────┐
  │ Start with merged = [[1, 3]]                                    │
  │                                                                  │
  │ Check [2, 6]:  2 <= 3 (overlaps with last) → merge to [1, 6]   │
  │   merged = [[1, 6]]                                             │
  │                                                                  │
  │ Check [8, 10]: 8 > 6 (no overlap) → add new                    │
  │   merged = [[1, 6], [8, 10]]                                    │
  │                                                                  │
  │ Check [15, 18]: 15 > 10 (no overlap) → add new                 │
  │   merged = [[1, 6], [8, 10], [15, 18]]                         │
  └──────────────────────────────────────────────────────────────────┘
  
  OUTPUT: [[1, 6], [8, 10], [15, 18]]
```

```python
def merge_intervals(intervals):
    """Merge all overlapping intervals."""
    if not intervals:
        return []
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last = merged[-1]
        
        # If current interval overlaps with last merged
        if current[0] <= last[1]:
            # Merge them
            merged[-1] = [last[0], max(last[1], current[1])]
        else:
            # No overlap, add current
            merged.append(current)
    
    return merged

# Example
intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
print(merge_intervals(intervals))
# Output: [[1, 6], [8, 10], [15, 18]]

intervals = [[1, 4], [4, 5]]
print(merge_intervals(intervals))
# Output: [[1, 5]]
```

### Detailed Version

```python
def merge_intervals_detailed(intervals):
    """Merge intervals with detailed steps."""
    if not intervals:
        return []
    
    # Sort by start time
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged = [sorted_intervals[0]]
    merge_steps = []
    
    for i in range(1, len(sorted_intervals)):
        current = sorted_intervals[i]
        last = merged[-1]
        
        if current[0] <= last[1]:
            # Merge
            new_interval = [last[0], max(last[1], current[1])]
            merged[-1] = new_interval
            merge_steps.append(f"Merged {last} and {current} -> {new_interval}")
        else:
            merged.append(current)
            merge_steps.append(f"No overlap: added {current}")
    
    print("Merge steps:")
    for step in merge_steps:
        print(f"  {step}")
    
    return merged

# Example
intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
print(merge_intervals_detailed(intervals))
```

---

## 2. Insert Interval

**Problem**: Insert a new interval into a list of non-overlapping intervals and merge if necessary.

### Visual Walkthrough

```
  INPUT: intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]
         new_interval = [4, 8]
  
  THREE-PHASE APPROACH:
  ┌────────────────────────────────────────────────────────────────────┐
  │                                                                    │
  │  Phase 1: Add intervals BEFORE new_interval (end < 4)             │
  │  ─────────────────────────────────────────────────────────         │
  │  [1, 2]: end=2 < 4 → ADD ✓                                        │
  │  result = [[1, 2]]                                                │
  │                                                                    │
  │  Phase 2: Merge overlapping intervals (start <= 8)                │
  │  ─────────────────────────────────────────────────────────         │
  │  [3, 5]:  3 <= 8 → merge → new = [min(4,3), max(8,5)] = [3, 8]  │
  │  [6, 7]:  6 <= 8 → merge → new = [min(3,6), max(8,7)] = [3, 8]  │
  │  [8, 10]: 8 <= 8 → merge → new = [min(3,8), max(8,10)] = [3, 10] │
  │  result = [[1, 2], [3, 10]]                                       │
  │                                                                    │
  │  Phase 3: Add remaining intervals (start > 8)                     │
  │  ─────────────────────────────────────────────────────────         │
  │  [12, 16]: ADD ✓                                                   │
  │  result = [[1, 2], [3, 10], [12, 16]]                             │
  │                                                                    │
  └────────────────────────────────────────────────────────────────────┘
  
  OUTPUT: [[1, 2], [3, 10], [12, 16]]
```

```python
def insert_interval(intervals, new_interval):
    """Insert new interval and merge if necessary."""
    result = []
    i = 0
    n = len(intervals)
    
    # Add all intervals that end before new interval starts
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

# Example
intervals = [[1, 3], [6, 9]]
new_interval = [2, 5]
print(insert_interval(intervals, new_interval))
# Output: [[1, 5], [6, 9]]

intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]
new_interval = [4, 8]
print(insert_interval(intervals, new_interval))
# Output: [[1, 2], [3, 10], [12, 16]]
```

---

## 3. Non-overlapping Intervals

**Problem**: Find minimum number of intervals to remove to make the rest non-overlapping.

### Visual Walkthrough

```
  INPUT: [[1, 2], [2, 3], [3, 4], [1, 3]]
  
  SORT BY END TIME:
  ┌──────┬───────┬────────┐
  │ Sort │ Start │  End   │
  ├──────┼───────┼────────┤
  │  1   │   1   │    2   │ ◄── keep (earliest finish)
  │  2   │   2   │    3   │     start 2 >= end 2 → KEEP
  │  3   │   3   │    4   │     start 3 >= end 3 → KEEP
  │  4   │   1   │    3   │     start 1 < end 2  → REMOVE
  └──────┴───────┴────────┘
  
  TIMELINE:
  Time:  0  1  2  3  4
         │  [1─2]        ← KEEP
         │     [2─3]     ← KEEP
         │        [3─4]  ← KEEP
         │  [1───3]      ← REMOVE (overlaps with [1-2])
  
  Minimum removals: 1
  
  GREEDY STRATEGY: Keep intervals that end EARLIEST.
  This maximizes remaining time for other intervals.
```

```python
def erase_overlap_intervals(intervals):
    """Find minimum intervals to remove for non-overlapping."""
    if not intervals:
        return 0
    
    # Sort by end time (greedy: keep intervals that end earliest)
    intervals.sort(key=lambda x: x[1])
    
    count = 0
    last_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] >= last_end:
            # No overlap, keep this interval
            last_end = intervals[i][1]
        else:
            # Overlap, remove this interval
            count += 1
    
    return count

# Example
intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]
print(erase_overlap_intervals(intervals))  # 1

intervals = [[1, 2], [1, 2], [1, 3]]
print(erase_overlap_intervals(intervals))  # 2
```

### With Details of Removed Intervals

```python
def erase_overlap_intervals_detailed(intervals):
    """Find minimum intervals to remove with details."""
    if not intervals:
        return 0, []
    
    # Sort by end time
    sorted_intervals = sorted(enumerate(intervals), key=lambda x: x[1][1])
    
    kept = [sorted_intervals[0]]
    removed = []
    last_end = sorted_intervals[0][1][1]
    
    for i in range(1, len(sorted_intervals)):
        idx, interval = sorted_intervals[i]
        
        if interval[0] >= last_end:
            kept.append(sorted_intervals[i])
            last_end = interval[1]
        else:
            removed.append((idx, interval))
    
    print(f"Kept intervals: {[interval for _, interval in kept]}")
    print(f"Removed intervals: {[interval for _, interval in removed]}")
    print(f"Minimum removals: {len(removed)}")
    
    return len(removed), removed

# Example
intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]
erase_overlap_intervals_detailed(intervals)
```

---

## 4. Minimum Arrows to Burst Balloons

**Problem**: Find minimum arrows to burst all balloons (balloon = interval on x-axis).

### Visual Walkthrough

```
  INPUT: [[10, 16], [2, 8], [1, 6], [7, 12]]
  
  SORT BY END POSITION: [[1, 6], [2, 8], [7, 12], [10, 16]]
  
  X-AXIS VISUALIZATION:
  
  Arrow 1 at x=6:
  Position:  0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
             │  ├────[1──────6]──┤  │  │                    │
             │     ├────[2────────8]──┤  │                    │
  
  Balloons [1,6] and [2,8] are burst by arrow at x=6 ✓
  
  Arrow 2 at x=12:
  Position:  7  8  9  10 11 12 13 14 15 16
             ├──[7────────12]──┤  │  │
             │        ├────[10─────────16]──┤
  
  Balloons [7,12] and [10,16] are burst by arrow at x=12 ✓
  
  RESULT: 2 arrows needed
  
  GREEDY STRATEGY:
  ┌─────────────────────────────────────────────────────┐
  │ 1. Sort balloons by END position                    │
  │ 2. Place arrow at end of first balloon              │
  │ 3. Skip all balloons that this arrow bursts         │
  │ 4. Place next arrow at end of next unburst balloon  │
  │ 5. Repeat until all balloons are burst              │
  └─────────────────────────────────────────────────────┘
  
  SAME AS: Non-overlapping Intervals problem!
  Each arrow = one non-overlapping interval.
  Minimum arrows = maximum non-overlapping intervals.
```

```python
def find_min_arrows(points):
    """Find minimum arrows to burst all balloons."""
    if not points:
        return 0
    
    # Sort by end position
    points.sort(key=lambda x: x[1])
    
    arrows = 1
    last_end = points[0][1]
    
    for i in range(1, len(points)):
        if points[i][0] > last_end:
            # Need new arrow
            arrows += 1
            last_end = points[i][1]
    
    return arrows

# Example
points = [[10, 16], [2, 8], [1, 6], [7, 12]]
print(find_min_arrows(points))  # 2

points = [[1, 2], [3, 4], [5, 6], [7, 8]]
print(find_min_arrows(points))  # 4

points = [[1, 2], [2, 3], [3, 4], [4, 5]]
print(find_min_arrows(points))  # 2
```

### Visualization

```python
def find_min_arrows_visual(points):
    """Find minimum arrows with visualization."""
    if not points:
        return 0
    
    # Sort by end position
    sorted_points = sorted(points, key=lambda x: x[1])
    
    arrows = []
    last_end = float('-inf')
    
    for point in sorted_points:
        if point[0] > last_end:
            # Need new arrow at end of this balloon
            arrows.append(point[1])
            last_end = point[1]
    
    print("Balloons (sorted by end):")
    for i, (start, end) in enumerate(sorted_points):
        print(f"  Balloon {i}: [{start}, {'.' * (end - start - 1)}{end}]")
    
    print(f"\nArrows at positions: {arrows}")
    print(f"Minimum arrows needed: {len(arrows)}")
    
    return len(arrows)

# Example
points = [[10, 16], [2, 8], [1, 6], [7, 12]]
find_min_arrows_visual(points)
```

---

## 5. Meeting Rooms I and II

### Meeting Rooms I

**Problem**: Determine if a person can attend all meetings.

### Visual Explanation

```
  INPUT: [[0, 30], [5, 10], [15, 20]]
  
  SORT BY START TIME:
  Time:  0  5  10  15  20  25  30
         ├──[0──────────────30]──┤
              ├──[5──10]──┤
                     ├──[15──20]──┤
  
  Check overlaps:
  [0,30] and [5,10]: 5 < 30 → OVERLAP! → return False
  
  INPUT: [[7, 10], [2, 4]]
  
  SORT BY START TIME:
  Time:  0  2  4  5  6  7  8  9  10
              [2─4]           [7─10]
  
  Check overlaps:
  [2,4] and [7,10]: 7 >= 4 → NO OVERLAP → return True
```

### Meeting Rooms II

**Problem**: Find minimum number of conference rooms required.

### Visual Walkthrough (Min-Heap Approach)

```
  INPUT: [[0, 30], [5, 10], [15, 20]]
  
  SORT BY START TIME, then use min-heap:
  
  Time:  0     5     10    15    20    30
         │     │     │     │     │     │
         ▼     ▼     ▼     ▼     ▼     ▼
  ┌──────────────────────────────────────────────┐
  │ t=0: Start [0,30]                            │
  │   heap = [30]          rooms needed = 1      │
  │                                               │
  │ t=5: Start [5,10]                            │
  │   heap[0]=30 > 5 → can't reuse room          │
  │   heap = [10, 30]    rooms needed = 2        │
  │                                               │
  │ t=10: Start [15,20]  (after [5,10] ends)     │
  │   heap[0]=10 <= 15 → reuse room!             │
  │   heap = [20, 30]    rooms still = 2         │
  │                                               │
  │ t=30: All done                                │
  │   heap = [20, 30]    max rooms = 2           │
  └──────────────────────────────────────────────┘
  
  RESULT: 2 rooms needed
  
  ALTERNATIVE: Line Sweep
  ┌──────────────────────────────────────────────┐
  │ Events:                                      │
  │   (0, +1)  (5, +1)  (10, -1)  (15, +1)     │
  │   (20, -1)  (30, -1)                         │
  │                                               │
  │ Sorted: (0,+1)(5,+1)(10,-1)(15,+1)(20,-1)(30,-1) │
  │                                               │
  │ Count: 0→1→2→1→2→1→0                         │
  │ Max concurrent = 2                            │
  └──────────────────────────────────────────────┘
```

```python
def can_attend_meetings(intervals):
    """Check if person can attend all meetings."""
    if not intervals:
        return True
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    # Check for overlaps
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    
    return True

# Example
intervals = [[0, 30], [5, 10], [15, 20]]
print(can_attend_meetings(intervals))  # False

intervals = [[7, 10], [2, 4]]
print(can_attend_meetings(intervals))  # True
```

### Meeting Rooms II

**Problem**: Find minimum number of conference rooms required.

```python
import heapq

def min_meeting_rooms(intervals):
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
print(min_meeting_rooms(intervals))  # 2

intervals = [[7, 10], [2, 4]]
print(min_meeting_rooms(intervals))  # 1
```

### Alternative: Line Sweep

```python
def min_meeting_rooms_sweep(intervals):
    """Find minimum rooms using line sweep."""
    events = []
    
    for start, end in intervals:
        events.append((start, 1))   # Meeting starts
        events.append((end, -1))    # Meeting ends
    
    # Sort events: by time, then by type (end before start)
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

---

## 6. Interval Partitioning

**Problem**: Partition intervals into minimum number of groups such that no two intervals in the same group overlap.

### Visual Walkthrough

```
  INPUT: [[1, 3], [2, 4], [5, 6], [7, 8], [7, 9]]
  
  SORT BY START TIME:
  Time:  1  2  3  4  5  6  7  8  9
         ├──[1──3]──┤
            ├──[2──4]──┤
                     ├──[5─6]──┤
                           ├──[7─8]──┤
                           ├────[7──9]──┤
  
  ASSIGNMENT PROCESS (using min-heap of end times):
  ┌──────────────────────────────────────────────────────────┐
  │ [1,3]: No group available → create Group 1              │
  │   heap = [(3, G1)]                                       │
  │                                                          │
  │ [2,4]: heap[0]=(3,G1), 2 < 3 → create Group 2          │
  │   heap = [(3,G1), (4,G2)]                               │
  │                                                          │
  │ [5,6]: heap[0]=(3,G1), 5 >= 3 → REUSE Group 1           │
  │   heap = [(4,G2), (6,G1)]                               │
  │                                                          │
  │ [7,8]: heap[0]=(4,G2), 7 >= 4 → REUSE Group 2           │
  │   heap = [(6,G1), (8,G2)]                               │
  │                                                          │
  │ [7,9]: heap[0]=(6,G1), 7 >= 6 → REUSE Group 1           │
  │   heap = [(8,G2), (9,G1)]                               │
  └──────────────────────────────────────────────────────────┘
  
  RESULT:
  Group 1: [[1, 3], [5, 6], [7, 8]]
  Group 2: [[2, 4], [7, 9]]
  Minimum groups needed: 2
  
  KEY INSIGHT: This is equivalent to finding the maximum
  number of overlapping intervals at any point (Meeting Rooms II).
```

```python
import heapq

def interval_partitioning(intervals):
    """Partition intervals into minimum groups."""
    if not intervals:
        return 0, []
    
    # Sort by start time
    sorted_intervals = sorted(enumerate(intervals), key=lambda x: x[1][0])
    
    # Min-heap: (end_time, group_id)
    groups = []
    group_assignment = [0] * len(intervals)
    group_count = 0
    
    for idx, (start, end) in sorted_intervals:
        # Check if any group is available
        if groups and groups[0][0] <= start:
            # Reuse group
            _, group_id = heapq.heappop(groups)
            group_assignment[idx] = group_id
            heapq.heappush(groups, (end, group_id))
        else:
            # Create new group
            group_count += 1
            group_assignment[idx] = group_count
            heapq.heappush(groups, (end, group_count))
    
    print(f"Minimum groups needed: {group_count}")
    print(f"Group assignments: {group_assignment}")
    
    # Show groups
    group_contents = {}
    for idx, group_id in enumerate(group_assignment):
        if group_id not in group_contents:
            group_contents[group_id] = []
        group_contents[group_id].append(intervals[idx])
    
    for group_id, interval_list in sorted(group_contents.items()):
        print(f"  Group {group_id}: {interval_list}")
    
    return group_count, group_assignment

# Example
intervals = [[1, 3], [2, 4], [5, 6], [7, 8], [7, 9]]
interval_partitioning(intervals)
# Output:
# Minimum groups needed: 2
# Group 1: [[1, 3], [5, 6], [7, 8]]
# Group 2: [[2, 4], [7, 9]]
```

### Alternative: Using SortedList

```python
from sortedcontainers import SortedList

def interval_partitioning_sorted(intervals):
    """Interval partitioning using SortedList."""
    sorted_intervals = sorted(enumerate(intervals), key=lambda x: x[1][0])
    
    # SortedList of end times
    end_times = SortedList()
    group_assignment = [0] * len(intervals)
    group_count = 0
    
    for idx, (start, end) in enumerate(sorted_intervals):
        # Find group with earliest end time <= start
        pos = end_times.bisect_right(start) - 1
        
        if pos >= 0:
            # Reuse group
            group_count = max(group_count, len(end_times))
        else:
            # Need new group
            group_count += 1
        
        end_times.add(end)
    
    return group_count

# Example
intervals = [[1, 3], [2, 4], [5, 6], [7, 8], [7, 9]]
print(interval_partitioning_sorted(intervals))  # 2
```

---

## Quick Reference: Interval Patterns

| Problem | Key Insight | Approach |
|---------|-------------|----------|
| Merge Intervals | Overlapping intervals merge | Sort by start, merge |
| Insert Interval | Insert and merge if needed | Three-phase approach |
| Non-overlapping | Keep intervals that end early | Sort by end, count |
| Burst Balloons | Same as non-overlapping | Sort by end, count |
| Meeting Rooms I | No overlaps possible | Sort by start, check |
| Meeting Rooms II | Track concurrent meetings | Min-heap of end times |
| Partitioning | Min groups for non-overlapping | Sort by start, assign |

---

## Complexity Analysis

| Problem | Time | Space |
|---------|------|-------|
| Merge Intervals | O(n log n) | O(n) |
| Insert Interval | O(n) | O(n) |
| Non-overlapping | O(n log n) | O(1) |
| Burst Balloons | O(n log n) | O(1) |
| Meeting Rooms I | O(n log n) | O(1) |
| Meeting Rooms II | O(n log n) | O(n) |
| Partitioning | O(n log n) | O(n) |

---

## Key Insights

1. **Sort by start** for problems about merging/inserting
2. **Sort by end** for problems about keeping maximum non-overlapping
3. **Min-heap** tracks concurrent intervals/meetings
4. **Line sweep** is powerful for event-based problems
5. Always check if **end time** comparison is strict or non-strict

### Interval Problem Decision Guide

```
  ┌──────────────────────────────────────────────────────────────────┐
  │           INTERVAL PROBLEM PATTERN MATCHER                       │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                  │
  │  "Merge overlapping intervals?"                                  │
  │    → Sort by START, iterate and merge                            │
  │                                                                  │
  │  "Insert a new interval?"                                        │
  │    → Three-phase: before, merge, after                           │
  │                                                                  │
  │  "Remove min intervals to make non-overlapping?"                 │
  │    → Sort by END, greedily keep earliest finishers               │
  │                                                                  │
  │  "Min arrows to burst balloons?"                                 │
  │    → Same as non-overlapping (sort by END)                       │
  │                                                                  │
  │  "Can attend all meetings?"                                      │
  │    → Sort by START, check consecutive overlaps                   │
  │                                                                  │
  │  "Min conference rooms?"                                         │
  │    → Sort by START + min-heap of END times                       │
  │    → OR line sweep (+1 for start, -1 for end)                    │
  │                                                                  │
  │  "Partition into min non-overlapping groups?"                    │
  │    → Sort by START + min-heap (same as Meeting Rooms II)         │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
```

### Sort Key Cheat Sheet

```
  ┌─────────────────────┬────────────────────────────────────────┐
  │ When to sort by...  │ Problems                               │
  ├─────────────────────┼────────────────────────────────────────┤
  │ START time          │ Merge intervals, Insert interval,      │
  │                     │ Meeting Rooms I/II, Interval partition  │
  ├─────────────────────┼────────────────────────────────────────┤
  │ END time            │ Non-overlapping intervals,              │
  │                     │ Burst balloons, Activity selection      │
  ├─────────────────────┼────────────────────────────────────────┤
  │ Both (events)       │ Line sweep approach for Meeting Rooms   │
  └─────────────────────┴────────────────────────────────────────┘
```
