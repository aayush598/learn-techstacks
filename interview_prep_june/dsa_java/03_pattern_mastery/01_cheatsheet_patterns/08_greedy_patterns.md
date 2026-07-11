# Greedy Patterns Cheatsheet

---

## When Greedy Works

Greedy algorithms build solutions piece by piece, always choosing the **locally optimal** choice, hoping to find the **globally optimal** solution.

**Two properties must hold:**
1. **Greedy Choice Property:** A globally optimal solution can be reached by making locally optimal choices.
2. **Optimal Substructure:** An optimal solution contains optimal solutions to subproblems.

---

## Proof Technique: Exchange Argument

1. Assume an optimal solution that differs from the greedy choice.
2. Show you can "exchange" one element of the optimal solution with the greedy choice.
3. Prove the exchange doesn't make the solution worse.
4. This contradicts the assumption, proving greedy is optimal.

---

## Pattern 1: Sort + Greedy (Activity Selection)

**Template:** Sort by end time, pick activities that don't overlap.

```java
// Activity Selection / Meeting Rooms II (min rooms)
public int minMeetingRooms(int[][] intervals) {
    if (intervals.length == 0) return 0;

    Arrays.sort(intervals, (a, b) -> Integer.compare(a[1], b[1]));

    PriorityQueue<Integer> endTimes = new PriorityQueue<>();
    endTimes.offer(intervals[0][1]);

    for (int i = 1; i < intervals.length; i++) {
        if (intervals[i][0] >= endTimes.peek()) {
            endTimes.poll(); // reuse room
        }
        endTimes.offer(intervals[i][1]);
    }
    return endTimes.size();
}
```

**Problems:** Meeting Rooms II, Non-overlapping Intervals, Minimum Number of Arrows

---

## Pattern 2: Sort by Start, Merge

```java
// Merge Intervals
public int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
    List<int[]> merged = new ArrayList<>();

    for (int[] interval : intervals) {
        if (merged.isEmpty() || merged.get(merged.size() - 1)[1] < interval[0]) {
            merged.add(interval);
        } else {
            merged.get(merged.size() - 1)[1] =
                Math.max(merged.get(merged.size() - 1)[1], interval[1]);
        }
    }
    return merged.toArray(new int[0][]);
}
```

---

## Pattern 3: Jump Game (Choose Locally Optimal)

```java
// Jump Game — can you reach the end?
public boolean canJump(int[] nums) {
    int maxReach = 0;
    for (int i = 0; i < nums.length; i++) {
        if (i > maxReach) return false;
        maxReach = Math.max(maxReach, i + nums[i]);
    }
    return true;
}

// Jump Game II — minimum jumps
public int jump(int[] nums) {
    int jumps = 0, currentEnd = 0, farthest = 0;
    for (int i = 0; i < nums.length - 1; i++) {
        farthest = Math.max(farthest, i + nums[i]);
        if (i == currentEnd) {
            jumps++;
            currentEnd = farthest;
        }
    }
    return jumps;
}
```

---

## Pattern 4: Gas Station (Circular Greedy)

```java
public int canCompleteCircuit(int[] gas, int[] cost) {
    int totalTank = 0, currentTank = 0, start = 0;

    for (int i = 0; i < gas.length; i++) {
        int diff = gas[i] - cost[i];
        totalTank += diff;
        currentTank += diff;

        if (currentTank < 0) {
            start = i + 1;
            currentTank = 0;
        }
    }

    return totalTank >= 0 ? start : -1;
}
```

**Why greedy works:** If total gas ≥ total cost, a solution exists. Starting from the first deficit point guarantees enough fuel from previous stations.

---

## Pattern 5: Huffman-like (Combine Smallest Repeatedly)

```java
// Minimum Cost to Connect Sticks
public int connectSticks(int[] sticks) {
    PriorityQueue<Integer> pq = new PriorityQueue<>();
    for (int stick : sticks) pq.offer(stick);

    int cost = 0;
    while (pq.size() > 1) {
        int a = pq.poll(), b = pq.poll();
        cost += a + b;
        pq.offer(a + b);
    }
    return cost;
}
```

**Problems:** Reorganize String, Task Scheduler, Minimum Cost to Connect Sticks

---

## Pattern 6: Process from Both Ends

```java
// Candy Distribution
public int candy(int[] ratings) {
    int n = ratings.length;
    int[] candies = new int[n];
    Arrays.fill(candies, 1);

    // Left to right
    for (int i = 1; i < n; i++) {
        if (ratings[i] > ratings[i - 1]) {
            candies[i] = candies[i - 1] + 1;
        }
    }

    // Right to left (and take max)
    for (int i = n - 2; i >= 0; i--) {
        if (ratings[i] > ratings[i + 1]) {
            candies[i] = Math.max(candies[i], candies[i + 1] + 1);
        }
    }

    return Arrays.stream(candies).sum();
}
```

---

## Pattern 7: Greedy with Priority Queue

```java
// Task Scheduler — least intervals to complete all tasks
public int leastInterval(char[] tasks, int n) {
    int[] freq = new int[26];
    for (char c : tasks) freq[c - 'A']++;

    PriorityQueue<Integer> pq = new PriorityQueue<>(Collections.reverseOrder());
    for (int f : freq) if (f > 0) pq.offer(f);

    int intervals = 0;
    while (!pq.isEmpty()) {
        List<Integer> temp = new ArrayList<>();
        for (int i = 0; i <= n; i++) {
            if (!pq.isEmpty()) {
                temp.add(pq.poll() - 1);
            }
        }
        for (int f : temp) if (f > 0) pq.offer(f);

        intervals += pq.isEmpty() ? temp.size() : n + 1;
    }
    return intervals;
}
```

---

## Greedy vs DP Decision Tree

```
Need to make choices affecting future?
├── Yes → Can you prove greedy choice property?
│   ├── Yes → GREEDY (sort + pick, or iterate + choose)
│   └── No → DYNAMIC PROGRAMMING
└── No → Simple iteration/brute force
```

| Scenario | Approach | Why |
|----------|----------|-----|
| Activity selection (by end time) | Greedy | Exchange argument works |
| Knapsack (0/1) | DP | Greedy fails (value/weight ratio) |
| Jump Game | Greedy | Local reachability is optimal |
| Coin change | DP | Greedy fails for arbitrary denominations |
| Interval scheduling | Greedy | Sort by end, pick non-overlapping |
| Longest increasing subsequence | DP | No local choice leads to global |

---

## 10+ Greedy Problem Templates

| # | Problem | Greedy Strategy |
|---|---------|----------------|
| 1 | Activity Selection | Sort by end time, pick greedily |
| 2 | Jump Game | Track max reachable index |
| 3 | Gas Station | Track deficit, restart from deficit+1 |
| 4 | Task Scheduler | Most frequent first, fill cooldowns |
| 5 | Merge Intervals | Sort by start, merge overlaps |
| 6 | Non-overlapping Intervals | Sort by end, remove conflicts |
| 7 | Candy | Two-pass: left→right, right→left |
| 8 | Hand of Straights | Sort + greedy grouping |
| 9 | Minimum Arrows | Sort by end, count non-overlapping |
| 10 | Partition Labels | Track last occurrence, cut at boundary |
| 11 | Valid Parenthesis String | Track min/max possible open count |
| 12 | Reconstruct Queue | Sort by height desc, insert by k |
