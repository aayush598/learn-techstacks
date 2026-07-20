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
