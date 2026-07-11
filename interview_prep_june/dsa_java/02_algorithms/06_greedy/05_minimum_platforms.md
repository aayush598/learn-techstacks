# Minimum Platforms (Railway Station)

**Problem**: Given arrival and departure times of trains, find minimum number of platforms needed at a station to avoid waiting time.

**Greedy**: Sort arrivals and departures separately. Use two pointers to track concurrent trains.

```java
public int findPlatform(int[] arr, int[] dep) {
    int n = arr.length;
    Arrays.sort(arr);
    Arrays.sort(dep);

    int platforms = 0, maxPlatforms = 0;
    int i = 0, j = 0;

    while (i < n && j < n) {
        if (arr[i] <= dep[j]) {
            platforms++; // train arrives
            maxPlatforms = Math.max(maxPlatforms, platforms);
            i++;
        } else {
            platforms--; // train departs
            j++;
        }
    }

    return maxPlatforms;
}
```

## Key Insight

> Sort both arrays. When a train arrives before the earliest departure, we need another platform. Otherwise, a platform frees up. This is O(n log n) and much simpler than interval overlap checking.

---

## Detailed Walkthrough

Let's trace through a concrete example:

```
Trains:  1    2    3    4    5    6
arr[]: [900, 940, 950, 1100, 1500, 1800]
dep[]: [910, 1200, 1120, 1130, 1900, 2000]
```

### Step-by-Step Two-Pointer Trace

| Step | i | j | arr[i] | dep[j] | Action | Platforms | Max |
|------|---|---|--------|--------|--------|-----------|-----|
| 1 | 0 | 0 | 900 | 910 | 900 ≤ 910 → arrive | 1 | 1 |
| 2 | 1 | 0 | 940 | 910 | 940 > 910 → depart | 0 | 1 |
| 3 | 1 | 1 | 940 | 1200 | 940 ≤ 1200 → arrive | 1 | 1 |
| 4 | 2 | 1 | 950 | 1200 | 950 ≤ 1200 → arrive | 2 | 2 |
| 5 | 3 | 1 | 1100 | 1200 | 1100 ≤ 1200 → arrive | 3 | 3 |
| 6 | 4 | 1 | 1500 | 1200 | 1500 > 1200 → depart | 2 | 3 |
| 7 | 4 | 2 | 1500 | 1120 | 1500 > 1120 → depart | 1 | 3 |
| 8 | 4 | 3 | 1500 | 1130 | 1500 > 1130 → depart | 0 | 3 |
| 9 | 4 | 4 | 1500 | 1900 | 1500 ≤ 1900 → arrive | 1 | 3 |
| 10 | 5 | 4 | 1800 | 1900 | 1800 ≤ 1900 → arrive | 2 | 3 |
| 11 | 5 | 5 | 1800 | 2000 | ... done | | |
| 12 | 6 | 5 | done | 2000 | depart remaining | ... | 3 |

**Answer: 3 platforms needed** (peak at step 5 when trains 2, 3, 4 are all present).

---

## Approach 2: Sweep Line (Event-Based)

This approach treats each arrival as `+1` and each departure as `-1` on a timeline, then finds the maximum prefix sum.

```java
public int findPlatformSweepLine(int[] arr, int[] dep) {
    int n = arr.length;

    // Collect all events: (time, type) where type = +1 (arrive) or -1 (depart)
    TreeMap<Integer, Integer> events = new TreeMap<>();

    for (int i = 0; i < n; i++) {
        events.merge(arr[i], 1, Integer::sum);   // arrival
        events.merge(dep[i], -1, Integer::sum);   // departure
    }

    int platforms = 0, maxPlatforms = 0;
    for (int delta : events.values()) {
        platforms += delta;
        maxPlatforms = Math.max(maxPlatforms, platforms);
    }

    return maxPlatforms;
}
```

**Walkthrough with the same example**:

```
Events sorted by time:
  900:  +1  (train 1 arrives)
  910:  -1  (train 1 departs)    + net 0 → platforms: 1, max: 1
  940:  +1  (train 2 arrives)     → platforms: 1, max: 1
  950:  +1  (train 3 arrives)     → platforms: 2, max: 2
 1100:  +1  (train 4 arrives)     → platforms: 3, max: 3
 1120:  -1  (train 2 departs)    → platforms: 2
 1130:  -1  (train 3 departs)    → platforms: 1
 1200:  -1  (train 4 departs)    → platforms: 0
 1500:  +1  (train 5 arrives)     → platforms: 1
 1800:  +1  (train 6 arrives)     → platforms: 2
 1900:  -1  (train 5 departs)    → platforms: 1
 2000:  -1  (train 6 departs)    → platforms: 0

Answer: 3
```

**Note**: If multiple events happen at the same time, process departures before arrivals (or vice versa depending on problem constraint). The two-pointer approach handles this naturally with `<=`.

---

## Approach Comparison

| Aspect | Two-Pointer | Sweep Line |
|--------|-------------|------------|
| Time | O(n log n) | O(n log n) |
| Space | O(1) extra | O(n) for TreeMap |
| Simplicity | ★★★ | ★★☆ |
| Handles ties | Natural (`<=` → arrive first) | Must order events explicitly |
| Best for | Interviews | Event-based problems, coordinate compression |

---

## Edge Cases

| Case | Input | Output | Notes |
|------|-------|--------|-------|
| Empty | `arr=[], dep=[]` | 0 | No trains |
| Single train | `arr=[900], dep=[910]` | 1 | Always at least 1 |
| All overlap | `arr=[900,900,900], dep=[910,910,910]` | 3 | All trains simultaneous |
| No overlap | `arr=[900,1000,1100], dep=[910,1010,1110]` | 1 | Sequential, one platform suffices |
| Equal arr/dep | `arr=[900], dep=[900]` | 1 | Same time arrival/departure — use `<=` for arrive-first |
| Out-of-order arrays | `arr=[1800,900,940], dep=[2000,910,1200]` | 3 | Sorting handles this |
| Back-to-back | `arr=[900,910], dep=[910,920]` | 1 | `910 <= 910` → arrive before depart |

---

## Variant: K Platforms / Bus Station

**Problem**: Given `K` platforms, determine the maximum number of trains that can be scheduled without conflict, or find the minimum number of platforms to schedule all trains without waiting.

This generalizes to the **interval scheduling** family:
- **1 platform**: Maximum non-overlapping intervals (greedy by end time)
- **K platforms**: Each interval must be assigned to one of K platforms with no overlap
- **All trains**: Minimum platforms = peak concurrent trains (this problem)

For K platforms, if you need to schedule more trains than a single platform allows:
- Sort by arrival time
- Use a min-heap of size K tracking the end time of the last task on each platform
- Assign each train to the platform that finishes earliest (or a new one if all are busy)

```java
public int minPlatformsForAll(int[] arr, int[] dep) {
    Arrays.sort(arr);
    Arrays.sort(dep);
    // Standard two-pointer — this gives the minimum platforms needed
    int platforms = 0, maxPlatforms = 0;
    int i = 0, j = 0;
    while (i < arr.length) {
        if (arr[i] <= dep[j]) {
            platforms++;
            maxPlatforms = Math.max(maxPlatforms, platforms);
            i++;
        } else {
            platforms--;
            j++;
        }
    }
    return maxPlatforms;
}
```

---

## Common Pitfalls

1. **Not sorting both arrays independently**: The arrival and departure arrays must be sorted separately — don't sort interval pairs together.

2. **Using `<` instead of `<=`**: When arrival equals departure, the arriving train needs the platform before the departing one frees it. Use `<=` for "arrive first."

3. **Off-by-one with remaining departures**: After the while loop, remaining departures reduce platforms but don't increase max — no extra processing needed.
