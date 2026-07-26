# Sorting Tricks for Competitive Programming

> **Why this matters:** In CP, sorting is rarely the final answer — it's a *tool* that simplifies
> harder problems. The trick is knowing *what to sort by* and *what pattern to apply after sorting*.

---

## 1. Custom Comparator Using functools.cmp_to_key

### What is a Comparator?

```
A comparator is a function that tells the sort HOW to compare two elements.

  Python's default:    a < b  →  sorts ascending
  Custom comparator:   returns negative (a before b), positive (b before a), or 0

  ┌──────────────────────────────────────────────────────────┐
  │  cmp(a, b) < 0  →  a comes before b                     │
  │  cmp(a, b) = 0  →  a and b keep relative order (stable) │
  │  cmp(a, b) > 0  →  b comes before a                     │
  └──────────────────────────────────────────────────────────┘
```

### Example: Sort by Absolute Value

```python
from functools import cmp_to_key

arr = [-3, 1, -4, 1, 5]

# Compare by absolute value: |a| vs |b|
arr.sort(key=cmp_to_key(lambda a, b: abs(a) - abs(b)))
# Result: [-3, 1, 1, -4, 5]  (sorted by |x|: 1,1,3,4,5)

# Step-by-step trace:
#   Compare -3 and 1:  |−3| − |1| = 3−1 = 2 > 0 → 1 before -3
#   Compare -3 and -4: |−3| − |−4| = 3−4 = −1 < 0 → -3 before -4
#   Compare 1 and 5:   |1| − |5| = 1−5 = −4 < 0 → 1 before 5
```

### Example: Sort Even Before Odd, Then by Value

```python
arr = [3, 2, 5, 1, 4]
arr.sort(key=cmp_to_key(lambda a, b: (a % 2) - (b % 2) or a - b))
# Result: [2, 4, 1, 3, 5]

# How it works:
#   (a % 2) - (b % 2)  →  0 if both same parity, +1 if a is odd & b even, -1 otherwise
#   "or a - b"          →  if parity is same, sort by value
#
#   Visual:
#     Evens: [2, 4]    → sorted by value
#     Odds:  [1, 3, 5] → sorted by value
#     Combined: [2, 4, 1, 3, 5]
```

### Example: Sort Strings by Length, Then Alphabetically

```python
words = ["banana", "hi", "apple", "ok"]
words.sort(key=cmp_to_key(lambda a, b: len(a) - len(b) or (a > b) - (a < b)))
# Result: ['hi', 'ok', 'apple', 'banana']

# Step-by-step:
#   "hi" (2) vs "ok" (2):       same length → alphabetical: "hi" < "ok"
#   "hi" (2) vs "apple" (5):    2 < 5 → "hi" first
#   "apple" (5) vs "banana" (6): 5 < 6 → "apple" first
```

---

## 2. Sort Strings by Length, by Frequency

### By Length

```python
words = ["apple", "hi", "banana", "ok"]
words.sort(key=len)
# Result: ['hi', 'ok', 'apple', 'banana']
#         (2)    (2)    (5)     (6)
```

### By Character Frequency (LeetCode 451)

```python
from collections import Counter

s = "tree"
freq = Counter(s)    # {'t': 1, 'r': 1, 'e': 2}
result = sorted(s, key=lambda x: (-freq[x], x))
# Result: ['e', 'e', 'r', 't']  → "eert"

# Visual walkthrough:
#   Character: t  r  e  e
#   Freq:      1  1  2  2
#   Sort key: (-1, 't')  (-1, 'r')  (-2, 'e')  (-2, 'e')
#
#   Sorting by (-freq, char):
#     (-2, 'e') comes first (highest freq)
#     (-2, 'e') next (same freq, 'e' < 't' and 'e' < 'r')
#     (-1, 'r') next (freq 1, 'r' < 't')
#     (-1, 't') last
#
#   Result: "eert"
```

### Frequency Sort Function (Reusable)

```python
def frequency_sort(s):
    """Sort characters by frequency (most frequent first), then by character."""
    freq = Counter(s)
    return ''.join(sorted(s, key=lambda x: (-freq[x], x)))

# Example:
#   frequency_sort("cccaaa") → "aaaccc" or "cccaaa"
#   frequency_sort("tree")   → "eert"
```

---

## 3. Interval Scheduling (Sort by End Time)

### The Greedy Strategy

```
Problem: Given intervals, select the MAXIMUM number of non-overlapping intervals.

Key Insight: Sort by END TIME, always pick the one that finishes earliest!

Why? Because the interval that ends earliest leaves the most room for future intervals.

  Analogy: You have meetings all day. To attend the MOST meetings,
           always pick the meeting that ends earliest next!
```

### Visual Walkthrough

```
Input: [[1,2], [2,3], [1,3], [3,4]]

Timeline:
  1   2   3   4
  ├───┤           [1,2]
      ├───┤       [2,3]
  ├───────┤       [1,3]
          ├───┤   [3,4]

Step 1: Sort by end time → [[1,2], [2,3], [1,3], [3,4]]

Step 2: Greedily pick non-overlapping:
  Pick [1,2]   → last_end = 2
  Pick [2,3]   → start(2) >= last_end(2) ✓  → last_end = 3
  Skip [1,3]   → start(1) < last_end(3) ✗   → OVERLAPS!
  Pick [3,4]   → start(3) >= last_end(3) ✓  → last_end = 4

Result: 3 intervals selected: [1,2], [2,3], [3,4]
```

### Annotated Code

```python
def max_non_overlapping_intervals(intervals):
    """Select maximum number of non-overlapping intervals."""
    # Step 1: Sort by end time (greedy choice)
    intervals.sort(key=lambda x: x[1])

    count = 0                             # Number of selected intervals
    last_end = float('-inf')              # End of last selected interval

    for start, end in intervals:
        if start >= last_end:             # No overlap with last selected
            count += 1                    # Select this interval
            last_end = end                # Update the boundary

    return count

# Time: O(n log n) for sorting + O(n) for scan = O(n log n)
# Space: O(1) — only tracking count and last_end
```

---

## 4. Meeting Rooms Problem (LeetCode 252 & 253)

### Meeting Rooms I — Can you attend all meetings?

```
Problem: Given meeting intervals, determine if you can attend ALL meetings
         (no overlaps).

Strategy: Sort by start time, check if any consecutive pair overlaps.

  Input: [[0,30],[5,10],[15,20]]

  Timeline:
    0    5    10   15   20   30
    ├─────────────────────────┤ [0,30]
         ├────┤                [5,10]  ← OVERLAPS with [0,30]!
                   ├──┤       [15,20]  ← OVERLAPS with [0,30]!

  Result: False (can't attend all)
```

```python
def can_attend_meetings(intervals):
    """Return True if you can attend all meetings (no overlaps)."""
    intervals.sort(key=lambda x: x[0])    # Sort by start time

    for i in range(1, len(intervals)):
        # If current meeting starts before previous one ends → overlap
        if intervals[i][0] < intervals[i - 1][1]:
            return False                  # Can't attend both

    return True
# Time: O(n log n), Space: O(1)
```

### Meeting Rooms II — Minimum rooms needed (LeetCode 253)

```
Problem: Find the MINIMUM number of conference rooms required.
         (How many meetings happen simultaneously at peak?)

Strategy: Sort by start time, use a min-heap to track end times.
          The heap size = number of concurrent meetings = rooms needed.

  Input: [[0,30],[5,10],[15,20],[25,30]]

  Timeline:
    0    5    10   15   20   25   30
    ├─────────────────────────────┤  [0,30]       Room 1
         ├────┤                   [5,10]          Room 2 (overlap at 5-10)
                   ├──┤          [15,20]          Room 3 (overlap at 15-20)
                              ├────┤              [25,30] Room 2 (room freed at 10)

  Peak concurrent meetings: 3 (at time 15-20)
  Answer: 3 rooms needed
```

```python
import heapq

def min_meeting_rooms(intervals):
    """Find minimum number of meeting rooms required."""
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])    # Sort by start time
    heap = []  # Min-heap of end times (rooms in use)

    for start, end in intervals:
        # If the earliest-ending meeting has ended, reuse that room
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)  # Pop old end, push new end
        else:
            heapq.heappush(heap, end)     # Need a new room

    return len(heap)  # Heap size = number of rooms in use at peak

# Visual trace with heap:
#   Meeting [0,30]:  heap = [30]           → 1 room
#   Meeting [5,10]:  heap[0]=30 > 5        → heap = [10, 30]   → 2 rooms
#   Meeting [15,20]: heap[0]=10 ≤ 15       → heap = [20, 30]   → 2 rooms (reuse room 10)
#   Meeting [25,30]: heap[0]=20 ≤ 25       → heap = [30, 30]   → 2 rooms (reuse room 20)

# Time: O(n log n) for sorting + O(n log n) for heap ops = O(n log n)
# Space: O(n) for the heap
```

---

## 5. Sort Colors Without Sorting (Dutch National Flag — LeetCode 75)

### The Problem

```
Given an array with only 0s, 1s, and 2s, sort it IN-PLACE in a single pass.

  Input:  [2, 0, 2, 1, 1, 0]
  Output: [0, 0, 1, 1, 2, 2]

  Constraint: Must be O(n) time, O(1) space, ONE pass!
```

### Visual Walkthrough — The Three-Way Partition

```
The idea: Maintain 3 regions by moving pointers:

  ┌─────────┬──────────────┬─────────────┬──────────────┐
  │ 0s      │  1s          │  unvisited  │  2s          │
  └─────────┴──────────────┴─────────────┴──────────────┘
  0       low            mid            high            n

  - Elements before `low` are all 0
  - Elements between `low` and `mid` are all 1
  - Elements between `mid` and `high` are unvisited
  - Elements after `high` are all 2

Step-by-step with [2, 0, 2, 1, 1, 0]:

  Start: [2, 0, 2, 1, 1, 0]   low=0, mid=0, high=5
          ↑  ↑              ↑
         low mid           high

  mid=0, nums[mid]=2:
    Swap nums[mid] and nums[high]: [0, 0, 2, 1, 1, 2]
    high-- → high=4
    (Don't increment mid — we haven't checked the swapped element!)

  mid=0, nums[mid]=0:
    Swap nums[low] and nums[mid]: [0, 0, 2, 1, 1, 2]  (no change)
    low++ → low=1, mid++ → mid=1

  mid=1, nums[mid]=0:
    Swap nums[low] and nums[mid]: [0, 0, 2, 1, 1, 2]  (no change)
    low++ → low=2, mid++ → mid=2

  mid=2, nums[mid]=2:
    Swap nums[mid] and nums[high]: [0, 0, 1, 1, 2, 2]
    high-- → high=3

  mid=2, nums[mid]=1:
    Just mid++ → mid=3

  mid=3 > high=3 → STOP!

  Result: [0, 0, 1, 1, 2, 2] ✓
```

### Annotated Code

```python
def sort_colors(nums):
    """Sort array of 0s, 1s, and 2s in-place in one pass."""
    low, mid, high = 0, 0, len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            # 0 belongs in the left region → swap with low boundary
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1                         # Expand 0s region
            mid += 1                         # Move past the swapped element
        elif nums[mid] == 1:
            # 1 is already in the middle region → just advance
            mid += 1                         # Expand 1s region
        else:
            # 2 belongs in the right region → swap with high boundary
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1                        # Expand 2s region
            # DON'T increment mid! The swapped element might be a 0 or 1

# Time: O(n) — single pass
# Space: O(1) — in-place
# Stable: No (relative order of 0s and 2s may change)

# ┌──────────────────────────────────────────────────────────┐
# │ Key insight: mid is NOT incremented when swapping with  │
# │ high, because the element swapped from high might be a  │
# │ 0 or 1 that needs to be processed.                      │
# └──────────────────────────────────────────────────────────┘
```

---

## 6. Merge Intervals (LeetCode 56)

### The Problem

```
Given a collection of intervals, merge all overlapping intervals.

  Input:  [[1,3],[2,6],[8,10],[15,18]]
  Output: [[1,6],[8,10],[15,18]]
```

### Visual Walkthrough

```
Step 1: Sort by start time → [[1,3],[2,6],[8,10],[15,18]]

  Timeline:
    1    2    3    4    5    6    7    8    9   10   15   18
    ├────────┤                       [1,3]
         ├──────────────────┤        [2,6]       ← OVERLAPS with [1,3]!
                                  ├──────┤       [8,10]
                                                  ├──────┤  [15,18]

Step 2: Merge overlapping intervals

  Start with merged = [[1,3]]
  Process [2,6]:  2 <= 3 (overlaps!) → merge: [1, max(3,6)] = [1,6]
  Process [8,10]: 8 > 6 (no overlap) → add [8,10]
  Process [15,18]: 15 > 10 (no overlap) → add [15,18]

  Result: [[1,6],[8,10],[15,18]] ✓
```

### Annotated Code

```python
def merge_intervals(intervals):
    """Merge all overlapping intervals."""
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])    # Sort by start time
    merged = [intervals[0]]               # Start with first interval

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:         # Overlaps with last merged interval
            # Extend the last interval's end to cover the overlap
            merged[-1][1] = max(merged[-1][1], end)
        else:
            # No overlap → add as new interval
            merged.append([start, end])

    return merged

# Time: O(n log n) for sorting + O(n) for merging = O(n log n)
# Space: O(1) excluding the output array
```

---

## 7. Insert Interval (LeetCode 57)

### The Problem

```
Given a sorted list of non-overlapping intervals and a new interval,
insert the new interval and merge if necessary.

  Input:  intervals = [[1,3],[6,9]], newInterval = [2,5]
  Output: [[1,5],[6,9]]
```

### Visual Walkthrough

```
Three phases:

  intervals: [1,3] [6,9]
  new:             [2,5]

  Phase 1: Add intervals BEFORE the new interval (no overlap possible)
    [1,3]: end(3) >= start(2) → STOP, move to Phase 2

  Phase 2: Merge overlapping intervals
    [1,3]: start(1) <= end(5) → OVERLAP! Merge: [min(2,1), max(5,3)] = [1,5]
    [6,9]: start(6) <= end(5)? NO → STOP, move to Phase 3

  Phase 3: Add remaining intervals
    [6,9] → add as-is

  Result: [[1,5],[6,9]] ✓

Another example:
  intervals: [[1,2],[3,5],[6,7],[8,10],[12,16]]
  new:                     [4,8]

  Phase 1: [1,2] end=2 < start=4 → add [1,2]
  Phase 2: [3,5] overlap → merge [3,8]
           [6,7] overlap → merge [3,8]
           [8,10] overlap → merge [3,10]
  Phase 3: [12,16] → add as-is

  Result: [[1,2],[3,10],[12,16]]
```

### Annotated Code

```python
def insert_interval(intervals, new_interval):
    """Insert a new interval into sorted non-overlapping intervals and merge."""
    result = []
    i = 0
    n = len(intervals)

    # Phase 1: Add all intervals that end before new_interval starts
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])       # No overlap possible
        i += 1

    # Phase 2: Merge all overlapping intervals with new_interval
    while i < n and intervals[i][0] <= new_interval[1]:
        # Expand new_interval to cover the overlap
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)            # Add the merged interval

    # Phase 3: Add all remaining intervals (no overlap possible)
    while i < n:
        result.append(intervals[i])
        i += 1

    return result

# Time: O(n) — single pass through intervals
# Space: O(n) — for the result array
```

---

## 8. Non-overlapping Intervals (LeetCode 435)

### The Problem

```
Given a collection of intervals, find the MINIMUM number of intervals
you need to remove to make the rest non-overlapping.

  Input:  [[1,2],[2,3],[1,3],[3,4]]
  Output: 1 (remove [1,3])
```

### Visual Walkthrough

```
This is the REVERSE of "Maximum Non-overlapping Intervals" (Section 3):

  Max non-overlapping = 3: [1,2], [2,3], [3,4]
  Total intervals = 4
  Min removals = 4 - 3 = 1

Strategy: Same greedy (sort by end time), but COUNT overlaps instead of selections.

  Sorted by end: [[1,2],[2,3],[1,3],[3,4]]

  Timeline:
    1    2    3    4
    ├───┤              [1,2]  → select (last_end = 2)
        ├───┤          [2,3]  → select (start=2 >= last_end=2) ✓
    ├───────┤          [1,3]  → REMOVE! (start=1 < last_end=2) ✗
            ├───┤      [3,4]  → select (start=3 >= last_end=3) ✓

  Removals = 1
```

### Annotated Code

```python
def erase_overlap_intervals(intervals):
    """Minimize removals to make all intervals non-overlapping."""
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])    # Sort by END time (greedy)

    count = 0                              # Number of intervals to remove
    last_end = intervals[0][1]             # End of last kept interval

    for i in range(1, len(intervals)):
        if intervals[i][0] < last_end:    # Overlaps with last kept
            count += 1                     # Must remove this one
        else:
            last_end = intervals[i][1]    # Keep it, update boundary

    return count

# Time: O(n log n), Space: O(1)
# Key insight: count = total - max_non_overlapping
```

---

## 9. Minimum Number of Arrows to Burst Balloons (LeetCode 452)

### The Problem

```
Each balloon is represented as a horizontal interval [start, end].
An arrow shot at position x bursts all balloons where start ≤ x ≤ end.
Find the MINIMUM number of arrows needed to burst ALL balloons.

  Input:  [[10,16],[2,8],[1,6],[7,12]]
  Output: 2
```

### Visual Walkthrough

```
This is IDENTICAL to "Maximum Non-overlapping Intervals"!

Why? Each arrow can burst a set of overlapping balloons (one group).
Min arrows = min groups = max non-overlapping intervals.

  Timeline:
    1    2    6    7    8   10   12   16
    ├───┬──┬────┤        [1,6]
       ├────────────────┤      [2,8]     ← OVERLAPS with [1,6]
                         ├─────┬──┤      [7,12]  ← OVERLAPS with [2,8]
                                  ├──────┤ [10,16] ← OVERLAPS with [7,12]

  Sort by end: [[1,6],[2,8],[7,12],[10,16]]

  Arrow 1: burst [1,6] → last_end = 6
           [2,8]: start=2 < 6 → overlaps, same arrow
           [7,12]: start=7 >= 6 → NEW arrow → last_end = 12
           [10,16]: start=10 < 12 → overlaps, same arrow

  Answer: 2 arrows ✓
```

### Annotated Code

```python
def find_min_arrows(points):
    """Find minimum arrows to burst all balloons."""
    if not points:
        return 0

    points.sort(key=lambda x: x[1])       # Sort by END time
    arrows = 1                             # Need at least 1 arrow
    last_end = points[0][1]                # End of first balloon group

    for start, end in points[1:]:
        if start > last_end:               # New group needs new arrow
            arrows += 1
            last_end = end

    return arrows

# Time: O(n log n), Space: O(1)
# This is the same algorithm as max_non_overlapping_intervals!
```

---

## 10. Sort by Custom Tuple Key

### Multi-Level Sorting

```
Problem: Sort by multiple criteria at once.

Strategy: Use a tuple as the sort key. Python sorts tuples element-by-element.

  key = (primary_sort, secondary_sort, tertiary_sort, ...)
```

### Example: Students by Score, Then Name

```python
students = [("Alice", 90), ("Bob", 85), ("Charlie", 90)]

# Sort by score DESC, then name ASC (for ties)
students.sort(key=lambda x: (-x[1], x[0]))
# Result: [('Alice', 90), ('Charlie', 90), ('Bob', 85)]

# Visual walkthrough:
#   Alice:   (-90, 'Alice')
#   Bob:     (-85, 'Bob')
#   Charlie: (-90, 'Charlie')
#
#   Compare (-90, 'Alice') vs (-90, 'Charlie'):
#     First element same (-90) → compare second: 'Alice' < 'Charlie'
#     → Alice before Charlie ✓
#
#   Compare (-90, 'Alice') vs (-85, 'Bob'):
#     -90 < -85 → Alice before Bob ✓
```

### Example: Sort Matrix Rows by Sum

```python
matrix = [[3, 1, 2], [1, 1, 1], [2, 2, 3]]
matrix.sort(key=sum)
# Result: [[1,1,1], [3,1,2], [2,2,3]]
#         (sum=3)   (sum=6)  (sum=7)
```

### Example: Sort by Last Element

```python
arr = [(1, 3), (2, 1), (3, 2)]
arr.sort(key=lambda x: x[-1])
# Result: [(2,1), (3,2), (1,3)]
#         (last=1) (last=2) (last=3)
```

### Tuple Key Cheat Sheet

```
┌─────────────────────────────────────┬──────────────────────────────┐
│ Goal                                │ Sort Key                      │
├─────────────────────────────────────┼──────────────────────────────┤
│ Ascending                           │ key=lambda x: x              │
│ Descending                          │ key=lambda x: -x             │
│ By absolute value                   │ key=lambda x: abs(x)         │
│ By frequency (most common first)    │ key=lambda x: -freq[x]       │
│ By length (shortest first)          │ key=len                      │
│ Multi-level: primary asc, second asc│ key=lambda x: (x[0], x[1])  │
│ Multi-level: primary asc, second dsc│ key=lambda x: (x[0], -x[1]) │
│ Even before odd, then by value      │ key=lambda x: (x%2, x)      │
│ Case-insensitive string sort        │ key=str.lower                │
└─────────────────────────────────────┴──────────────────────────────┘
```

---

## Summary — Pattern Recognition Guide

| Pattern | Key Insight | Time | Problems |
|---------|-------------|------|----------|
| **Sort by end time** | Greedy: pick earliest-ending intervals | O(n log n) | Max non-overlapping, min arrows, non-overlapping removal |
| **Sort by start time** | Process intervals left-to-right | O(n log n) | Merge intervals, insert interval, meeting rooms I |
| **cmp_to_key** | Complex comparisons as a function | O(n log n) | Custom ordering, parity-based sort |
| **Tuple key** | Multi-level sorting in one line | O(n log n) | Score+name, primary+secondary criteria |
| **Dutch National Flag** | 3-way partition in O(n) | O(n) | Sort 0s/1s/2s, 3-color problems |
| **Heap + sort** | Track concurrent events | O(n log n) | Meeting rooms II, overlapping events |

---

## Quick Reference: When to Use Each Trick

```
  ┌──────────────────────────────────────────────────┐
  │  Problem mentions "intervals" or "meetings"?     │
  │  → Sort by start or end time                      │
  │                                                   │
  │  Need to find "max non-overlapping"?              │
  │  → Sort by END time, greedy selection             │
  │                                                   │
  │  Need to "merge overlapping intervals"?           │
  │  → Sort by START time, merge greedily             │
  │                                                   │
  │  Need to count "how many overlap at once"?        │
  │  → Sort by start time + min-heap on end times     │
  │                                                   │
  │  Array has only 3 distinct values?                │
  │  → Dutch National Flag (3-way partition)          │
  │                                                   │
  │  Need complex sorting criteria?                   │
  │  → Tuple key or cmp_to_key                        │
  └──────────────────────────────────────────────────┘
```
