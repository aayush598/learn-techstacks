# Activity Selection Problems - Complete Guide

## Table of Contents
1. [Activity Selection - Maximize Activities](#1-activity-selection--maximize-activities)
2. [Job Sequencing Problem](#2-job-sequencing-problem)
3. [Job Sequencing with Deadlines](#3-job-sequencing-with-deadlines)
4. [Weighted Job Scheduling](#4-weighted-job-scheduling)
5. [Platform Allocation Problem](#5-platform-allocation-problem)

---

## 1. Activity Selection - Maximize Activities

**Problem**: Select maximum number of non-overlapping activities.

### Visual Walkthrough

```
  INPUT: [(1,4), (3,5), (0,6), (5,7), (3,9), (5,9), (6,10), (8,11), (8,12), (2,14), (12,16)]
  
  STEP 1: Sort by finish time:
  ┌─────┬───────┬────────┐
  │ Act │ Start │ Finish │
  ├─────┼───────┼────────┤
  │  1  │   1   │    4   │
  │  2  │   3   │    5   │
  │  3  │   0   │    6   │
  │  4  │   5   │    7   │
  │  5  │   3   │    9   │
  │  6  │   5   │    9   │
  │  7  │   6   │   10   │
  │  8  │   8   │   11   │
  │  9  │   8   │   12   │
  │ 10  │   2   │   14   │
  │ 11  │  12   │   16   │
  └─────┴───────┴────────┘
  
  STEP 2: Greedy selection:
  ┌──────────────────────────────────────────────────────────┐
  │ Pick Act 1 (1,4): last_finish=4                         │
  │   Act 2 (3,5): 3 < 4 → SKIP                             │
  │   Act 3 (0,6): 0 < 4 → SKIP                             │
  │   Act 4 (5,7): 5 >= 4 → PICK ✓  last_finish=7          │
  │   Act 5 (3,9): 3 < 7 → SKIP                             │
  │   Act 6 (5,9): 5 < 7 → SKIP                             │
  │   Act 7 (6,10): 6 < 7 → SKIP                            │
  │   Act 8 (8,11): 8 >= 7 → PICK ✓  last_finish=11        │
  │   Act 9 (8,12): 8 < 11 → SKIP                           │
  │   Act 10 (2,14): 2 < 11 → SKIP                          │
  │   Act 11 (12,16): 12 >= 11 → PICK ✓  last_finish=16    │
  └──────────────────────────────────────────────────────────┘
  
  SELECTED: [(1,4), (5,7), (8,11), (12,16)] → 4 activities
  
  WHY SORT BY FINISH TIME?
  Picking the activity that finishes earliest leaves
  MAXIMUM remaining time for other activities.
```

```python
def activity_selection(activities):
    """
    Select maximum non-overlapping activities.
    activities: list of (start, finish) tuples
    """
    # Sort by finish time (greedy choice)
    activities.sort(key=lambda x: x[1])
    
    selected = [activities[0]]
    last_finish = activities[0][1]
    
    for i in range(1, len(activities)):
        start, finish = activities[i]
        
        # If activity starts after last selected finishes
        if start >= last_finish:
            selected.append(activities[i])
            last_finish = finish
    
    return selected

# Example
activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
selected = activity_selection(activities)
print(f"Selected activities: {selected}")
print(f"Maximum activities: {len(selected)}")
# Output: Selected activities: [(1, 4), (5, 7), (8, 11), (12, 16)]
# Maximum activities: 4
```

### Alternative: Sort by Start Time

```python
def activity_selection_by_start(activities):
    """Activity selection sorted by start time."""
    # Sort by start time
    activities.sort(key=lambda x: x[0])
    
    selected = [activities[0]]
    last_finish = activities[0][1]
    
    for i in range(1, len(activities)):
        start, finish = activities[i]
        
        if start >= last_finish:
            selected.append(activities[i])
            last_finish = finish
    
    return selected

# Example
activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
selected = activity_selection_by_start(activities)
print(f"Selected: {selected}")
print(f"Count: {len(selected)}")
```

### Proof of Correctness

```python
def activity_selection_proof(activities):
    """Activity selection with proof of optimality."""
    # Sort by finish time
    sorted_acts = sorted(activities, key=lambda x: x[1])
    
    selected = [sorted_acts[0]]
    last_finish = sorted_acts[0][1]
    
    for i in range(1, len(sorted_acts)):
        start, finish = sorted_acts[i]
        
        if start >= last_finish:
            selected.append(sorted_acts[i])
            last_finish = finish
    
    print("Proof of optimality:")
    print("1. Greedy choice: Always pick activity with earliest finish time")
    print("   This leaves maximum time for remaining activities")
    print("2. Optimal substructure: After picking activity i,")
    print("   the remaining problem is to select from activities starting after i finishes")
    print("3. Therefore, greedy choice leads to optimal solution")
    
    return selected
```

---

## 2. Job Sequencing Problem

**Problem**: Given jobs with deadlines and profits, maximize profit by scheduling at most one job per unit time.

### Visual Walkthrough

```
  INPUT: [(1, 2, 100), (2, 1, 19), (3, 2, 27), (4, 1, 25), (5, 3, 15)]
  
  STEP 1: Sort by PROFIT descending:
  ┌───────┬──────────┬──────────┬────────┐
  │  Job  │ Deadline │  Profit  │ Order  │
  ├───────┼──────────┼──────────┼────────┤
  │   1   │    2     │   100    │   1st  │
  │   3   │    2     │    27    │   2nd  │
  │   4   │    1     │    25    │   3rd  │
  │   2   │    1     │    19    │   4th  │
  │   5   │    3     │    15    │   5th  │
  └───────┴──────────┴──────────┴────────┘
  
  STEP 2: Schedule jobs (find latest available slot):
  ┌──────────────────────────────────────────────────────┐
  │ Time Slots: [_, _, _]  (indices 1, 2, 3)            │
  │                                                       │
  │ Job 1 (deadline=2):                                  │
  │   Slot 2 is free → schedule at slot 2 ✓              │
  │   Slots: [_, J1, _]                                  │
  │                                                       │
  │ Job 3 (deadline=2):                                  │
  │   Slot 2 taken, slot 1 free → schedule at slot 1 ✓   │
  │   Slots: [J3, J1, _]                                 │
  │                                                       │
  │ Job 4 (deadline=1):                                  │
  │   Slot 1 taken → NO SLOT AVAILABLE ✗                 │
  │                                                       │
  │ Job 2 (deadline=1):                                  │
  │   Slot 1 taken → NO SLOT AVAILABLE ✗                 │
  │                                                       │
  │ Job 5 (deadline=3):                                  │
  │   Slot 3 free → schedule at slot 3 ✓                 │
  │   Slots: [J3, J1, J5]                                │
  └──────────────────────────────────────────────────────┘
  
  RESULT:
  Time Slot 1: Job 3 (profit 27)
  Time Slot 2: Job 1 (profit 100)
  Time Slot 3: Job 5 (profit 15)
  Total Profit: 142
  
  KEY INSIGHT: Always try to place high-profit jobs in
  the LATEST possible slot before their deadline.
  This preserves earlier slots for jobs with tighter deadlines.
```

```python
def job_sequencing(jobs):
    """
    Maximize profit from jobs with deadlines.
    jobs: list of (job_id, deadline, profit)
    """
    # Sort jobs by profit in descending order
    jobs.sort(key=lambda x: x[2], reverse=True)
    
    # Find maximum deadline
    max_deadline = max(job[1] for job in jobs)
    
    # Schedule array: time slot -> job_id
    schedule = [-1] * (max_deadline + 1)
    total_profit = 0
    scheduled_jobs = []
    
    for job_id, deadline, profit in jobs:
        # Find latest available slot before deadline
        for t in range(deadline, 0, -1):
            if schedule[t] == -1:
                schedule[t] = job_id
                total_profit += profit
                scheduled_jobs.append((job_id, t, profit))
                break
    
    return total_profit, scheduled_jobs

# Example
jobs = [(1, 2, 100), (2, 1, 19), (3, 2, 27), (4, 1, 25), (5, 3, 15)]
total_profit, scheduled = job_sequencing(jobs)
print(f"Total profit: {total_profit}")
print(f"Scheduled jobs: {scheduled}")
# Output:
# Total profit: 142
# Scheduled jobs: [(1, 2, 100), (3, 1, 27), (5, 3, 15)]
```

### Detailed Version

```python
def job_sequencing_detailed(jobs):
    """Job sequencing with detailed output."""
    # Sort by profit descending
    sorted_jobs = sorted(jobs, key=lambda x: x[2], reverse=True)
    
    max_deadline = max(job[1] for job in sorted_jobs)
    schedule = [None] * (max_deadline + 1)
    
    total_profit = 0
    scheduled = []
    rejected = []
    
    for job_id, deadline, profit in sorted_jobs:
        # Find available slot
        scheduled_flag = False
        for t in range(min(deadline, max_deadline), 0, -1):
            if schedule[t] is None:
                schedule[t] = (job_id, profit)
                total_profit += profit
                scheduled.append((job_id, deadline, profit, t))
                scheduled_flag = True
                break
        
        if not scheduled_flag:
            rejected.append((job_id, deadline, profit))
    
    print("Job Sequencing Result:")
    print("-" * 40)
    print(f"{'Time Slot':<12} {'Job ID':<10} {'Profit':<10}")
    print("-" * 40)
    
    for t in range(1, max_deadline + 1):
        if schedule[t]:
            job_id, profit = schedule[t]
            print(f"{t:<12} {job_id:<10} {profit:<10}")
        else:
            print(f"{t:<12} {'Idle':<10} {'-':<10}")
    
    print("-" * 40)
    print(f"Total Profit: {total_profit}")
    print(f"Scheduled: {len(scheduled)} jobs")
    print(f"Rejected: {len(rejected)} jobs")
    
    return total_profit, scheduled

# Example
jobs = [(1, 2, 100), (2, 1, 19), (3, 2, 27), (4, 1, 25), (5, 3, 15)]
job_sequencing_detailed(jobs)
```

---

## 3. Job Sequencing with Deadlines

**Problem**: Schedule jobs to maximize profit, each job takes 1 unit of time.

```python
def job_sequencing_deadlines(jobs):
    """
    Job sequencing with deadlines.
    jobs: list of (job_id, deadline, profit)
    Returns maximum profit and scheduled jobs.
    """
    # Sort by profit descending
    jobs.sort(key=lambda x: x[2], reverse=True)
    
    max_deadline = max(job[1] for job in jobs)
    
    # Find parent for union-find
    parent = list(range(max_deadline + 1))
    
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    
    def union(x, y):
        parent[find(x)] = find(y)
    
    total_profit = 0
    scheduled = []
    
    for job_id, deadline, profit in jobs:
        # Find available slot using union-find
        slot = find(min(deadline, max_deadline))
        
        if slot > 0:
            scheduled.append((job_id, slot, profit))
            total_profit += profit
            # Mark slot as used
            union(slot, slot - 1)
    
    return total_profit, scheduled

# Example
jobs = [(1, 2, 100), (2, 1, 19), (3, 2, 27), (4, 1, 25), (5, 3, 15)]
total_profit, scheduled = job_sequencing_deadlines(jobs)
print(f"Total profit: {total_profit}")
print(f"Scheduled jobs: {scheduled}")
```

### Alternative: Using Disjoint Set

```python
def job_sequencing_disjoint_set(jobs):
    """Job sequencing using Disjoint Set for O(n log n) complexity."""
    # Sort by profit descending
    jobs.sort(key=lambda x: x[2], reverse=True)
    
    max_deadline = max(job[1] for job in jobs)
    
    # Disjoint Set for finding available slots
    ds = DisjointSet(max_deadline + 1)
    
    total_profit = 0
    scheduled = []
    
    for job_id, deadline, profit in jobs:
        # Find available slot
        slot = ds.find(min(deadline, max_deadline))
        
        if slot > 0:
            scheduled.append((job_id, slot, profit))
            total_profit += profit
            # Mark this slot as used
            ds.union(slot, slot - 1)
    
    return total_profit, scheduled

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

# Example
jobs = [(1, 2, 100), (2, 1, 19), (3, 2, 27), (4, 1, 25), (5, 3, 15)]
total_profit, scheduled = job_sequencing_disjoint_set(jobs)
print(f"Total profit: {total_profit}")
print(f"Scheduled: {scheduled}")
```

---

## 4. Weighted Job Scheduling

**Problem**: Given jobs with start time, finish time, and profit, find maximum profit subset of non-overlapping jobs.

### Visual Walkthrough

```
  INPUT: [(1, 3, 50), (2, 5, 20), (4, 6, 70), (6, 7, 60), (5, 8, 30), (7, 9, 40)]
  
  STEP 1: Sort by finish time:
  ┌───────┬───────┬────────┬────────┐
  │  Job  │ Start │ Finish │ Profit │
  ├───────┼───────┼────────┼────────┤
  │  J1   │   1   │    3   │   50   │
  │  J2   │   2   │    5   │   20   │
  │  J3   │   4   │    6   │   70   │
  │  J4   │   6   │    7   │   60   │
  │  J5   │   5   │    8   │   30   │
  │  J6   │   7   │    9   │   40   │
  └───────┴───────┴────────┴────────┘
  
  STEP 2: DP with binary search:
  ┌──────────────────────────────────────────────────────────────┐
  │ dp[i] = max profit using first i jobs                        │
  │                                                              │
  │ dp[0] = 0                                                   │
  │ dp[1] = 50  (include J1: 50, or skip: 0) → 50              │
  │ dp[2] = 50  (include J2: 20+dp[0]=20, or skip: 50) → 50    │
  │ dp[3] = 120 (include J3: 70+dp[1]=120, or skip: 50) → 120  │
  │ dp[4] = 130 (include J4: 60+dp[3]=130, or skip: 120) → 130 │
  │ dp[5] = 130 (include J5: 30+dp[2]=80, or skip: 130) → 130  │
  │ dp[6] = 170 (include J6: 40+dp[4]=170, or skip: 130) → 170 │
  └──────────────────────────────────────────────────────────────┘
  
  BINARY SEARCH for "latest non-overlapping job":
  For J3 (start=4): find rightmost job with finish <= 4
  Finish times: [3, 5, 6, 7, 8, 9]
  Binary search: 3 <= 4 ✓, 5 > 4 → J1 is the latest
  
  RESULT: Maximum profit = 170
  Selected jobs: J3 (profit 70) + J4 (profit 60) + J6 (profit 40)
  
  VISUAL OF SELECTED JOBS:
  Time: 1  2  3  4  5  6  7  8  9
         [J1──3]
                  [J3──6][J4─7]  [J6─9]
  
  NOTE: This is NOT a pure greedy problem — it needs DP!
  Greedy doesn't work because high-profit jobs might block
  combinations of medium-profit jobs that sum to more.
```

```python
def weighted_job_scheduling(jobs):
    """
    Find maximum profit from non-overlapping jobs.
    jobs: list of (start, finish, profit)
    """
    from bisect import bisect_right
    
    n = len(jobs)
    
    # Sort by finish time
    jobs.sort(key=lambda x: x[1])
    
    # Extract finish times
    finish_times = [job[1] for job in jobs]
    
    # dp[i] = maximum profit using jobs[0..i-1]
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1):
        start, finish, profit = jobs[i - 1]
        
        # Find latest non-overlapping job
        # bisect_right finds first element > start
        j = bisect_right(finish_times, start, 0, i - 1)
        
        # Include current job
        dp[i] = max(dp[i - 1], dp[j] + profit)
    
    return dp[n]

# Example
jobs = [(1, 3, 50), (2, 5, 20), (4, 6, 70), (6, 7, 60), (5, 8, 30), (7, 9, 40)]
print(weighted_job_scheduling(jobs))  # 120 (jobs 1 and 4: 50 + 70)
```

### With Job Selection Details

```python
from bisect import bisect_right

def weighted_job_scheduling_detailed(jobs):
    """Weighted job scheduling with job selection details."""
    n = len(jobs)
    
    # Add original indices
    indexed_jobs = [(i, start, finish, profit) for i, (start, finish, profit) in enumerate(jobs)]
    
    # Sort by finish time
    indexed_jobs.sort(key=lambda x: x[2])
    
    finish_times = [job[2] for job in indexed_jobs]
    
    # dp[i] = max profit using jobs[0..i-1]
    dp = [0] * (n + 1)
    
    # parent[i] = index of job that led to dp[i]
    parent = [-1] * (n + 1)
    
    for i in range(1, n + 1):
        orig_idx, start, finish, profit = indexed_jobs[i - 1]
        
        # Find latest non-overlapping job
        j = bisect_right(finish_times, start, 0, i - 1)
        
        if dp[j] + profit > dp[i - 1]:
            dp[i] = dp[j] + profit
            parent[i] = j
        else:
            dp[i] = dp[i - 1]
            parent[i] = i - 1
    
    # Backtrack to find selected jobs
    selected = []
    i = n
    while i > 0:
        if parent[i] != i - 1:
            orig_idx, start, finish, profit = indexed_jobs[i - 1]
            selected.append((orig_idx, start, finish, profit))
            i = parent[i]
        else:
            i -= 1
    
    selected.reverse()
    
    print(f"Maximum profit: {dp[n]}")
    print(f"Selected jobs:")
    for orig_idx, start, finish, profit in selected:
        print(f"  Job {orig_idx}: [{start}, {finish}] profit={profit}")
    
    return dp[n], selected

# Example
jobs = [(1, 3, 50), (2, 5, 20), (4, 6, 70), (6, 7, 60), (5, 8, 30), (7, 9, 40)]
weighted_job_scheduling_detailed(jobs)
```

### Alternative: Using Binary Search with DP

```python
from bisect import bisect_right

def weighted_job_scheduling_optimized(jobs):
    """Optimized weighted job scheduling."""
    if not jobs:
        return 0
    
    # Sort by finish time
    jobs.sort(key=lambda x: x[1])
    n = len(jobs)
    
    # dp[i] = max profit considering jobs[0..i]
    dp = [0] * n
    dp[0] = jobs[0][2]
    
    for i in range(1, n):
        # Option 1: Include current job
        include_profit = jobs[i][2]
        
        # Find latest non-overlapping job using binary search
        j = binary_search(jobs, i)
        if j != -1:
            include_profit += dp[j]
        
        # Option 2: Exclude current job
        exclude_profit = dp[i - 1]
        
        dp[i] = max(include_profit, exclude_profit)
    
    return dp[n - 1]

def binary_search(jobs, i):
    """Find latest non-overlapping job before i."""
    lo, hi = 0, i - 1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        if jobs[mid][1] <= jobs[i][0]:
            if jobs[mid + 1][1] <= jobs[i][0]:
                lo = mid + 1
            else:
                return mid
        else:
            hi = mid - 1
    
    return -1

# Example
jobs = [(1, 3, 50), (2, 5, 20), (4, 6, 70), (6, 7, 60), (5, 8, 30), (7, 9, 40)]
print(weighted_job_scheduling_optimized(jobs))  # 120
```

---

## 5. Platform Allocation Problem

**Problem**: Given train arrival and departure times, find minimum platforms needed at any time.

### Visual Walkthrough

```
  INPUT:
  Arrivals:    [900, 940, 950, 1100, 1500, 1800]
  Departures:  [910, 1200, 1120, 1130, 1900, 2000]
  
  TRAIN SCHEDULE:
  Time:  900  910  940  950  1100 1120 1130 1200 1500 1800 1900 2000
         T1   T1   T2   T3   T4        T4   T2   T5   T6   T5   T6
         ARR  DEP  ARR  ARR  ARR  T3   DEP  DEP  ARR  ARR  DEP  DEP
                             T3   DEP               T6   T5
                             DEP
  
  LINE SWEEP APPROACH:
  ┌────────────────────────────────────────────────────────────────┐
  │ Events sorted by time (arrivals=+1, departures=-1):           │
  │                                                                │
  │ Time  │ Event │ Count │ Platforms                            │
  │───────┼───────┼───────┼──────────────────────────────────────│
  │  900  │  +1   │   1   │ █                                    │
  │  910  │  -1   │   0   │                                      │
  │  940  │  +1   │   1   │ █                                    │
  │  950  │  +1   │   2   │ ██                                   │
  │ 1100  │  +1   │   3   │ ███  ◄── MAXIMUM                    │
  │ 1120  │  -1   │   2   │ ██                                   │
  │ 1130  │  -1   │   1   │ █                                    │
  │ 1200  │  -1   │   0   │                                      │
  │ 1500  │  +1   │   1   │ █                                    │
  │ 1800  │  +1   │   2   │ ██                                   │
  │ 1900  │  -1   │   1   │ █                                    │
  │ 2000  │  -1   │   0   │                                      │
  └────────────────────────────────────────────────────────────────┘
  
  RESULT: 3 platforms needed (at time 1100)
  
  KEY INSIGHT: This is the same as Meeting Rooms II!
  Maximum concurrent intervals = minimum resources needed.
```

```python
def min_platforms(arrivals, departures):
    """
    Find minimum platforms required.
    arrivals: list of arrival times
    departures: list of departure times
    """
    # Combine and sort events
    events = []
    for time in arrivals:
        events.append((time, 1))   # Train arrives
    for time in departures:
        events.append((time, -1))  # Train departs
    
    # Sort events: by time, then arrivals before departures
    events.sort(key=lambda x: (x[0], -x[1]))
    
    current_platforms = 0
    max_platforms = 0
    
    for time, event_type in events:
        current_platforms += event_type
        max_platforms = max(max_platforms, current_platforms)
    
    return max_platforms

# Example
arrivals = [900, 940, 950, 1100, 1500, 1800]
departures = [910, 1200, 1120, 1130, 1900, 2000]
print(min_platforms(arrivals, departures))  # 3
```

### With Platform Assignment

```python
import heapq

def min_platforms_detailed(arrivals, departures):
    """Find minimum platforms with detailed assignment."""
    # Pair trains with their times
    trains = list(zip(arrivals, departures))
    
    # Sort by arrival time
    trains.sort(key=lambda x: x[0])
    
    # Min-heap: (departure_time, platform_id)
    platforms = []
    platform_count = 0
    
    assignments = []
    
    for i, (arr, dep) in enumerate(trains):
        # Check if any platform is available
        if platforms and platforms[0][0] <= arr:
            # Reuse platform
            _, platform_id = heapq.heappop(platforms)
            assignments.append((i, platform_id, arr, dep))
            heapq.heappush(platforms, (dep, platform_id))
        else:
            # Allocate new platform
            platform_count += 1
            assignments.append((i, platform_count, arr, dep))
            heapq.heappush(platforms, (dep, platform_count))
    
    print(f"Minimum platforms needed: {platform_count}")
    print("\nPlatform assignments:")
    for train_id, platform_id, arr, dep in sorted(assignments, key=lambda x: x[0]):
        print(f"  Train {train_id + 1}: Platform {platform_id} ({arr:04d}-{dep:04d})")
    
    return platform_count, assignments

# Example
arrivals = [900, 940, 950, 1100, 1500, 1800]
departures = [910, 1200, 1120, 1130, 1900, 2000]
min_platforms_detailed(arrivals, departures)
```

### Alternative: Using SortedList

```python
from sortedcontainers import SortedList

def min_platforms_sorted(arrivals, departures):
    """Find minimum platforms using SortedList."""
    events = []
    
    for time in arrivals:
        events.append((time, 'A'))
    for time in departures:
        events.append((time, 'D'))
    
    # Sort: by time, departures before arrivals (to free platform first)
    events.sort(key=lambda x: (x[0], 0 if x[1] == 'D' else 1))
    
    current = 0
    max_platforms = 0
    
    for time, event_type in events:
        if event_type == 'A':
            current += 1
            max_platforms = max(max_platforms, current)
        else:
            current -= 1
    
    return max_platforms

# Example
arrivals = [900, 940, 950, 1100, 1500, 1800]
departures = [910, 1200, 1120, 1130, 1900, 2000]
print(min_platforms_sorted(arrivals, departures))  # 3
```

---

## Quick Reference: Activity Selection Patterns

| Pattern | Key Idea | Approach |
|---------|----------|---------|
| Max Activities | Keep shortest finish | Sort by finish |
| Max Profit Jobs | Prioritize high profit | Sort by profit |
| Weighted Jobs | DP + binary search | Sort by finish |
| Platform Allocation | Track concurrent events | Line sweep or heap |

---

## Complexity Analysis

| Problem | Time | Space |
|---------|------|-------|
| Activity Selection | O(n log n) | O(n) |
| Job Sequencing | O(n²) or O(n log n) | O(n) |
| Weighted Job Scheduling | O(n log n) | O(n) |
| Platform Allocation | O(n log n) | O(n) |

---

## Key Insights

1. **Sort by finish time** for maximum non-overlapping activities
2. **Sort by profit** for job sequencing
3. **Binary search** optimizes finding non-overlapping jobs
4. **Union-Find** can optimize job scheduling
5. **Line sweep** is powerful for platform/resource allocation

### Activity Selection vs Job Scheduling Comparison

```
  ┌──────────────────────────────────────────────────────────────────┐
  │              PROBLEM COMPARISON CHEAT SHEET                       │
  ├────────────────────────────┬─────────────────────────────────────┤
  │ Activity Selection         │ Job Sequencing                      │
  ├────────────────────────────┼─────────────────────────────────────┤
  │ Goal: Max COUNT of jobs    │ Goal: Max PROFIT of jobs            │
  │ Weight: All jobs = 1       │ Weight: Each job has profit         │
  │ Approach: Pure greedy      │ Approach: Greedy + Union-Find       │
  │ Sort by: Finish time       │ Sort by: Profit (descending)        │
  │ Time: O(n log n)           │ Time: O(n²) or O(n log n) with DS  │
  ├────────────────────────────┼─────────────────────────────────────┤
  │ Activity Selection         │ Weighted Job Scheduling             │
  ├────────────────────────────┼─────────────────────────────────────┤
  │ Goal: Max COUNT of jobs    │ Goal: Max PROFIT of non-overlapping │
  │ Approach: Pure greedy      │ Approach: DP + Binary Search        │
  │ Time: O(n log n)           │ Time: O(n log n)                    │
  │ Sort by: Finish time       │ Sort by: Finish time + binary search│
  └────────────────────────────┴─────────────────────────────────────┘
```

### Problem Pattern Quick Reference

```
  ┌──────────────────────────────────────────────────────────────┐
  │  "Max number of non-overlapping activities?"                 │
  │    → Sort by finish, greedy selection                        │
  │                                                              │
  │  "Max profit from jobs with deadlines?"                      │
  │    → Sort by profit desc, place in latest available slot     │
  │                                                              │
  │  "Max profit from weighted non-overlapping jobs?"            │
  │    → Sort by finish, DP + binary search                      │
  │                                                              │
  │  "Min platforms / rooms for concurrent events?"              │
  │    → Line sweep or min-heap of end times                     │
  │                                                              │
  │  "Partition into min non-overlapping groups?"                │
  │    → Same as min platforms (Meeting Rooms II pattern)        │
  └──────────────────────────────────────────────────────────────┘
```
