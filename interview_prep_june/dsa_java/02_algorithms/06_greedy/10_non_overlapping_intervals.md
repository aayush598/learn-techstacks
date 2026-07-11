# Non-Overlapping Intervals / Interval Scheduling Maximization

## Problem

Given a collection of intervals `[start, end]`, find the **maximum number of non-overlapping intervals** you can select. Equivalently, find the **minimum number of intervals to remove** so that the remaining intervals don't overlap.

This is the classic **Interval Scheduling Maximization Problem (ISMP)** — one of the most elegant greedy problems.

---

## Greedy Strategy

**Sort intervals by end time.** Always pick the interval that finishes earliest. This leaves the maximum room for future intervals.

### Why not sort by start time?

Sorting by start time is tempting but fails. Consider:

```
Intervals: [1,10], [2,3], [4,5]
Sorted by start: [1,10], [2,3], [4,5]
- Pick [1,10] → blocks everything → result = 1
Sorted by end:   [2,3], [4,5], [1,10]
- Pick [2,3] then [4,5] → result = 2 ✓
```

The earliest-start greedy picks the interval that "reaches farthest into the future," starving subsequent choices.

---

## Proof by Exchange Argument

**Claim**: The greedy algorithm (sort by end, pick earliest finishing) produces an optimal solution.

**Proof**:

Let `G = {g₁, g₂, ..., gₖ}` be the greedy solution (intervals picked in order).
Let `O = {o₁, o₂, ..., oₘ}` be an optimal solution, also sorted by end time.
We want to show `k = m`.

**Step 1 — Base case of induction**: Compare `g₁` and `o₁`.

`g₁` is the interval with the earliest end time in the entire set. So `end(g₁) ≤ end(o₁)`.

**Step 2 — Exchange argument**: Suppose the first `i-1` intervals of `G` and `O` are the same (or can be exchanged). Consider interval `i`.

We have `end(gᵢ) ≤ end(oᵢ)` because:
- The greedy always picks the earliest-ending interval that doesn't conflict.
- `oᵢ` doesn't conflict with `oᵢ₋₁`, so it's a candidate.
- `gᵢ` is the earliest-ending candidate, so it finishes no later.

**Step 3 — Exchange**: Replace `oᵢ` with `gᵢ` in `O`. The new set `O'` is still valid (since `end(gᵢ) ≤ end(oᵢ)`, the next interval `oᵢ₊₁` won't conflict).

**Step 4 — Conclusion**: By induction, every optimal solution can be transformed into the greedy solution without losing any intervals. So `k = m`, and the greedy is optimal.

```
Exchange visualization:

Optimal:  |--o1--|    |---o2---|    |--o3--|
                ↑         ↑
Greedy:   |--g1--|--g2--|      |--g3--|

After exchange: |--g1--|--g2--|--o3--|  (still valid, still m intervals)
```

---

## Variants and Related Problems

### Variant 1: Minimum Removals to Make Non-Overlapping

**LeetCode 435 — Erase Overlap Intervals**

If you want to remove the minimum number of intervals to eliminate all overlaps:

```
minRemovals = totalIntervals - maxNonOverlappingIntervals
```

This follows directly from ISMP.

### Variant 2: Maximum Number of Meetings in One Room

Identical to ISMP. Each meeting is an interval `[start, end]`. Sort by end time, greedily pick. The room can hold one meeting at a time — non-overlapping constraint.

### Variant 3: Meeting Rooms I (LeetCode 252)

**Problem**: Given an array of intervals, determine if a person can attend **all** meetings (i.e., no overlaps at all).

**Approach**: Sort by start time. Check if any interval starts before the previous ends.

```java
boolean canAttendAll(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
    for (int i = 1; i < intervals.length; i++) {
        if (intervals[i][0] < intervals[i - 1][1]) return false;
    }
    return true;
}
```

### Variant 4: Meeting Rooms II (LeetCode 253)

**Problem**: Find the **minimum number of rooms** needed to hold all meetings.

This is a different problem — we need ALL intervals covered, not a maximum subset.

**Approach**: Sort both arrivals and departures, use two pointers. Or use a min-heap of end times.

```java
int minRooms(int[][] intervals) {
    int[] starts = new int[intervals.length];
    int[] ends = new int[intervals.length];
    for (int i = 0; i < intervals.length; i++) {
        starts[i] = intervals[i][0];
        ends[i] = intervals[i][1];
    }
    Arrays.sort(starts);
    Arrays.sort(ends);

    int rooms = 0, endIdx = 0;
    for (int start : starts) {
        if (start >= ends[endIdx]) endIdx++;  // reuse room
        else rooms++;                          // need new room
    }
    return rooms;
}
```

### Variant 5: Insert Interval to Make Non-Overlapping (LeetCode 57)

Given sorted non-overlapping intervals and a new interval, insert it and merge if necessary. (Covers insertion + merging logic.)

---

## Complete Java Implementation

```java
import java.util.*;

public class NonOverlappingIntervals {

    // Core: max number of non-overlapping intervals
    public int eraseOverlapIntervals(int[][] intervals) {
        if (intervals.length == 0) return 0;

        // Sort by end time
        Arrays.sort(intervals, (a, b) -> Integer.compare(a[1], b[1]));

        int count = 1;                // first interval always picked
        int lastEnd = intervals[0][1];

        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] >= lastEnd) {
                // No overlap — pick this interval
                count++;
                lastEnd = intervals[i][1];
            }
            // else: overlap — skip (equivalent to erasing this interval)
        }

        return count;
    }

    // Min removals = total - max non-overlapping
    public int minRemovals(int[][] intervals) {
        return intervals.length - eraseOverlapIntervals(intervals);
    }

    // Meeting Rooms I: can attend all?
    public boolean canAttendAll(int[][] intervals) {
        if (intervals.length <= 1) return true;

        Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] < intervals[i - 1][1]) return false;
        }
        return true;
    }

    // Meeting Rooms II: min rooms needed
    public int minRooms(int[][] intervals) {
        if (intervals.length == 0) return 0;

        int[] starts = new int[intervals.length];
        int[] ends = new int[intervals.length];
        for (int i = 0; i < intervals.length; i++) {
            starts[i] = intervals[i][0];
            ends[i] = intervals[i][1];
        }
        Arrays.sort(starts);
        Arrays.sort(ends);

        int rooms = 0, endPtr = 0;
        for (int start : starts) {
            if (start >= ends[endPtr]) {
                endPtr++;
            } else {
                rooms++;
            }
        }
        return rooms;
    }

    // K rooms: partition into k non-overlapping groups
    // Returns true if intervals can be colored with k colors
    // such that no two overlapping intervals share a color
    public boolean canScheduleInKRooms(int[][] intervals, int k) {
        return minRooms(intervals) <= k;
    }
}
```

---

## Complexity

| Aspect       | Value               |
|-------------|---------------------|
| **Time**    | O(n log n) — sorting dominates |
| **Space**   | O(1) extra (sorting in-place) or O(n) if not counting sort space |

---

## Step-by-Step Walkthrough

```
Input: [[1,2], [2,3], [3,4], [1,3]]

Step 1 — Sort by end time:
  [1,2], [1,3], [2,3], [3,4]
   ↑end=2   ↑end=3   ↑end=3  ↑end=4

Step 2 — Greedy selection:
  Pick [1,2] → lastEnd=2, count=1
  [1,3] → start=1 < lastEnd=2 → OVERLAP → skip
  [2,3] → start=2 >= lastEnd=2 → PICK → lastEnd=3, count=2
  [3,4] → start=3 >= lastEnd=3 → PICK → lastEnd=4, count=3

Result: max non-overlapping = 3
Min removals = 4 - 3 = 1 (remove [1,3])
```

---

## Edge Cases

| Case | Input | Output | Notes |
|------|-------|--------|-------|
| Empty | `[]` | 0 | No intervals |
| Single | `[[1,2]]` | 1 | Always pick |
| All overlap | `[[1,4],[2,3],[3,4]]` | 1 | Only shortest fits |
| No overlap | `[[1,2],[3,4],[5,6]]` | 3 | All fit |
| Equal end times | `[[1,3],[2,3],[3,3]]` | 1 | All end at 3, only one picks |
| Nested | `[[1,10],[2,5],[3,6]]` | 1 | [2,5] or [3,6] picked, blocks [1,10] |
| Contiguous | `[[1,2],[2,3],[3,4]]` | 3 | `[2,3]` touches — `>=` allows it |

---

## Common Pitfalls

1. **Using `<` instead of `>=`**: `start >= lastEnd` means intervals touching at endpoints are non-overlapping. Check the problem statement — some define `[1,2]` and `[2,3]` as overlapping.

2. **Forgetting to sort**: Without sorting by end time, the greedy fails completely.

3. **Confusing with Meeting Rooms II**: ISMP finds a maximum subset; Meeting Rooms II finds how many intervals overlap at any point.

4. **Starting count at 0**: First interval is always picked, so start `count = 1`.
