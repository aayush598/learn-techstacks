# Assignment Problems (Bitmask DP)

**Problem**: Given N tasks and N workers, assign each worker one task. Each worker i has cost c[i][j] to do task j. Minimize total cost.

---

## State Definition

```dp[mask]``` = minimum cost to assign tasks in `mask` to workers 0...k-1 (where k = popcount(mask))

**Key**: Worker k = number of assigned tasks so far = `Integer.bitCount(mask)`

---

## Implementation

```java
public int assign(int[][] cost) {
    int n = cost.length; // number of workers = number of tasks
    int[] dp = new int[1 << n];
    Arrays.fill(dp, Integer.MAX_VALUE / 2);
    dp[0] = 0; // no tasks assigned

    for (int mask = 0; mask < (1 << n); mask++) {
        int worker = Integer.bitCount(mask); // next worker to assign

        if (worker >= n) continue; // all workers assigned

        for (int task = 0; task < n; task++) {
            if ((mask & (1 << task)) != 0) continue; // task already assigned

            int newMask = mask | (1 << task);
            dp[newMask] = Math.min(dp[newMask], dp[mask] + cost[worker][task]);
        }
    }

    return dp[(1 << n) - 1];
}
```

### Trace for cost = [[9,2,7],[6,4,3],[5,8,1]]

```
Workers: 0, 1, 2
Tasks: 0, 1, 2

dp[000] = 0 (no assignments)

mask=000 (worker=0):
  task 0 → dp[001] = min(INF, 0+9) = 9
  task 1 → dp[010] = min(INF, 0+2) = 2
  task 2 → dp[100] = min(INF, 0+7) = 7

mask=001 (worker=1):
  task 1 → dp[011] = min(INF, 9+4) = 13
  task 2 → dp[101] = min(INF, 9+3) = 12

mask=010 (worker=1):
  task 0 → dp[011] = min(13, 2+6) = 8
  task 2 → dp[110] = min(INF, 2+3) = 5

mask=100 (worker=1):
  task 0 → dp[101] = min(12, 7+6) = 12
  task 1 → dp[110] = min(5, 7+4) = 5

mask=011 (worker=2):
  task 2 → dp[111] = min(INF, 8+3) = 11

mask=101 (worker=2):
  task 1 → dp[111] = min(11, 12+8) = 11

mask=110 (worker=2):
  task 0 → dp[111] = min(11, 5+5) = 10

Answer: dp[111] = 10
Assignment: worker 0 → task 1 (cost 2), worker 1 → task 2 (cost 3), worker 2 → task 0 (cost 5)
Total: 2 + 3 + 5 = 10
```

---

## Reconstruct Assignment

```java
public int[] assignWithTrace(int[][] cost) {
    int n = cost.length;
    int[] dp = new int[1 << n];
    int[] parent = new int[1 << n]; // which task was added
    Arrays.fill(dp, Integer.MAX_VALUE / 2);
    dp[0] = 0;

    for (int mask = 0; mask < (1 << n); mask++) {
        int worker = Integer.bitCount(mask);
        if (worker >= n) continue;

        for (int task = 0; task < n; task++) {
            if ((mask & (1 << task)) != 0) continue;
            int newMask = mask | (1 << task);
            int newCost = dp[mask] + cost[worker][task];
            if (newCost < dp[newMask]) {
                dp[newMask] = newCost;
                parent[newMask] = task;
            }
        }
    }

    // Reconstruct
    int[] assignment = new int[n];
    int mask = (1 << n) - 1;
    while (mask > 0) {
        int task = parent[mask];
        int worker = Integer.bitCount(mask) - 1;
        assignment[worker] = task;
        mask ^= (1 << task); // remove this task
    }

    return assignment; // assignment[w] = task assigned to worker w
}
```

---

## Variations

### Maximization (Profit)

```java
public int maximizeProfit(int[][] profit) {
    int n = profit.length;
    int[] dp = new int[1 << n];
    Arrays.fill(dp, Integer.MIN_VALUE / 2);
    dp[0] = 0;

    for (int mask = 0; mask < (1 << n); mask++) {
        int worker = Integer.bitCount(mask);
        if (worker >= n) continue;
        for (int task = 0; task < n; task++) {
            if ((mask & (1 << task)) != 0) continue;
            int newMask = mask | (1 << task);
            dp[newMask] = Math.max(dp[newMask], dp[mask] + profit[worker][task]);
        }
    }

    return dp[(1 << n) - 1];
}
```

### Minimum Makespan (Load Balancing)

```java
public int minMakespan(int[] tasks, int k) {
    // Assign tasks to k workers, minimize max load
    int n = tasks.length;
    int[] dp = new int[1 << n];
    Arrays.fill(dp, Integer.MAX_VALUE);
    dp[0] = 0;

    // Precompute sum of each subset
    int[] sum = new int[1 << n];
    for (int mask = 0; mask < (1 << n); mask++) {
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) {
                sum[mask] = sum[mask ^ (1 << i)] + tasks[i];
                break;
            }
        }
    }

    // dp[mask] = min makespan for this set of tasks
    for (int mask = 0; mask < (1 << n); mask++) {
        if (Integer.bitCount(mask) <= k) {
            dp[mask] = sum[mask]; // one worker does all
        }
        // Try splitting
        for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {
            int remaining = mask ^ sub;
            dp[mask] = Math.min(dp[mask], Math.max(sum[sub], dp[remaining]));
        }
    }

    return dp[(1 << n) - 1];
}
```

---

## Complexity

| Problem | Time | Space |
|---|---|---|
| Standard Assignment | O(n * 2^n) | O(2^n) |
| TSP | O(n² * 2^n) | O(n * 2^n) |
| Makespan | O(3^n) worst | O(2^n) |

## Key Takeaways

1. **dp[mask]**: cost for first k workers doing tasks in `mask`, where k = popcount(mask)
2. **Worker index = popcount(mask)** — implicit, no need for separate dimension
3. **Small n ≤ 15-20** — exponential states
4. **Reconstruction**: track parent (which task was added)
5. **Same pattern** for any problem where N things are assigned to N entities
