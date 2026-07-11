# Bitmask DP — Complete Reference

Bitmask DP is used when you need to track which items from a small set (n ≤ 20)
have been used/visited. Each state is a bitmask where bit i = 1 means item i
has been processed. With n ≤ 20, there are at most 2^20 ≈ 1M states.

---

## 1. When to Use Bitmask DP

Use bitmask DP when:
- n ≤ 20 (2^n states are feasible)
- You need to track a **subset** of items as part of the state
- The problem involves permutations, assignments, or covering all elements
- You need to know "which items have been used so far"

**Key operations:**
```java
int all = (1 << n) - 1;           // mask with all n bits set
boolean allUsed = (mask == all);   // check if all items used
boolean used = (mask & (1 << i)) != 0;  // check if item i is used
int newMask = mask | (1 << i);     // mark item i as used
int newMask = mask & ~(1 << i);    // mark item i as unused
```

---

## 2. Travelling Salesman Problem (TSP)

**Problem:** Visit all cities exactly once starting from city 0, returning to
city 0. Find the minimum cost tour.

**State:** `dp[mask][last]` = minimum cost to visit all cities in `mask`,
ending at city `last`.

**Transition:** `dp[mask | (1 << k)][k] = min(dp[mask][last] + dist[last][k])`
for all k not in mask.

**Base case:** `dp[1][0] = 0` (start at city 0, only city 0 visited).

```java
public int tsp(int[][] dist) {
    int n = dist.length;
    int ALL = (1 << n) - 1;
    int[][] dp = new int[1 << n][n];

    // Initialize with infinity
    for (int[] row : dp) Arrays.fill(row, Integer.MAX_VALUE / 2);
    dp[1][0] = 0;  // mask=001 (only city 0), at city 0, cost=0

    for (int mask = 1; mask <= ALL; mask++) {
        for (int last = 0; last < n; last++) {
            if ((mask & (1 << last)) == 0) continue;  // last not in mask
            if (dp[mask][last] == Integer.MAX_VALUE / 2) continue;

            for (int next = 0; next < n; next++) {
                if ((mask & (1 << next)) != 0) continue;  // already visited
                int newMask = mask | (1 << next);
                dp[newMask][next] = Math.min(
                    dp[newMask][next],
                    dp[mask][last] + dist[last][next]
                );
            }
        }
    }

    // Find minimum cost to return to city 0
    int minCost = Integer.MAX_VALUE;
    for (int last = 1; last < n; last++) {
        minCost = Math.min(minCost, dp[ALL][last] + dist[last][0]);
    }
    return minCost;
}
```

**Walkthrough with 4 cities:**
```
n=4, ALL=1111 (15)

States: dp[mask][last]
mask=0001 (only city 0):
  dp[0001][0] = 0  (start)

Expand from dp[0001][0]:
  → dp[0011][1] = dp[0001][0] + dist[0][1]
  → dp[0101][2] = dp[0001][0] + dist[0][2]
  → dp[1001][3] = dp[0001][0] + dist[0][3]

... continue expanding until mask=1111...

Answer: min over last of dp[1111][last] + dist[last][0]
```

**Time: O(2^n * n^2), Space: O(2^n * n)**
For n=20: ~400M operations (tight but feasible with optimizations).

---

## 3. Assignment Problem

**Problem:** Assign n workers to n tasks, each worker-task pair has a cost.
Minimize total cost. (This is the Hungarian problem, solvable in O(n^3), but
bitmask DP works for small n.)

**State:** `dp[mask]` = minimum cost to assign workers for the bits set in mask.
The number of set bits = number of workers assigned so far.

**Transition:** `dp[mask | (1 << k)] = min(dp[mask] + cost[popcount(mask)][k])`

```java
public int minAssignmentCost(int[][] cost) {
    int n = cost.length;
    int ALL = (1 << n) - 1;
    int[] dp = new int[1 << n];
    Arrays.fill(dp, Integer.MAX_VALUE / 2);
    dp[0] = 0;

    for (int mask = 0; mask < ALL; mask++) {
        int worker = Integer.bitCount(mask);  // next worker to assign
        for (int task = 0; task < n; task++) {
            if ((mask & (1 << task)) != 0) continue;  // task already assigned
            int newMask = mask | (1 << task);
            dp[newMask] = Math.min(dp[newMask], dp[mask] + cost[worker][task]);
        }
    }

    return dp[ALL];
}
```

**Walkthrough with 3 workers, 3 tasks:**
```
cost = [[1, 2, 3],
        [3, 1, 2],
        [2, 3, 1]]

mask=000: dp[000]=0, worker=0
  assign task 0: dp[001] = 0 + 1 = 1
  assign task 1: dp[010] = 0 + 2 = 2
  assign task 2: dp[100] = 0 + 3 = 3

mask=001: dp[001]=1, worker=1
  assign task 1: dp[011] = 1 + 1 = 2
  assign task 2: dp[101] = 1 + 2 = 3

mask=010: dp[010]=2, worker=1
  assign task 0: dp[011] = min(2, 2 + 3) = 2  (already 2)
  assign task 2: dp[110] = 2 + 2 = 4

mask=011: dp[011]=2, worker=2
  assign task 2: dp[111] = 2 + 1 = 3

mask=100: dp[100]=3, worker=1
  assign task 0: dp[101] = min(3, 3+3) = 3
  assign task 1: dp[110] = min(4, 3+1) = 4

... continuing to mask=111...

dp[111] = 3 → minimum cost = 3
(optimal: worker 0→task 0, worker 1→task 1, worker 2→task 2: 1+1+1=3) ✓
```

**Time: O(2^n * n), Space: O(2^n)**

---

## 4. Partition into K Subsets with Equal Sum (LeetCode 698)

**Problem:** Can the array be partitioned into K subsets with equal sum?

**State:** `dp[mask]` = sum of the current subset being built (modulo target).
When dp[mask] reaches target, start a new subset.

```java
public boolean canPartitionKSubsets(int[] nums, int k) {
    int total = 0;
    for (int x : nums) total += x;
    if (total % k != 0) return false;
    int target = total / k;

    int n = nums.length;
    int ALL = (1 << n) - 1;
    int[] dp = new int[1 << n];  // dp[mask] = sum of current subset mod target
    dp[0] = 0;

    for (int mask = 0; mask < ALL; mask++) {
        if (dp[mask] == -1) continue;
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) continue;
            int newMask = mask | (1 << i);
            int newSum = dp[mask] + nums[i];
            if (newSum <= target) {
                dp[newMask] = newSum % target;  // 0 means subset complete
            } else {
                dp[newMask] = -1;  // invalid state
            }
        }
    }

    return dp[ALL] == 0;
}
```

**Alternative approach — count subsets:**
```java
public boolean canPartitionKSubsets(int[] nums, int k) {
    int total = 0;
    for (int x : nums) total += x;
    if (total % k != 0) return false;
    int target = total / k;

    int n = nums.length;
    int ALL = (1 << n) - 1;
    int[] dp = new int[1 << n];
    // dp[mask] = number of complete subsets we can form, and remaining sum

    // Use bitmask DP: dp[mask] = remaining sum in current incomplete subset
    Arrays.fill(dp, -1);
    dp[0] = 0;

    for (int mask = 0; mask <= ALL; mask++) {
        if (dp[mask] == -1) continue;
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) continue;
            if (dp[mask] + nums[i] <= target) {
                int newMask = mask | (1 << i);
                dp[newMask] = (dp[mask] + nums[i]) % target;
            }
        }
    }

    return dp[ALL] == 0;
}
```

---

## 5. Count Hamiltonian Paths

**Problem:** Count the number of Hamiltonian paths (paths visiting every vertex
exactly once) in a directed graph.

**State:** `dp[mask][last]` = number of ways to visit all vertices in `mask`,
ending at vertex `last`.

```java
public long countHamiltonianPaths(int[][] adj) {
    int n = adj.length;
    int ALL = (1 << n) - 1;
    long[][] dp = new long[1 << n][n];

    // Base case: each vertex can be a starting point
    for (int i = 0; i < n; i++) {
        dp[1 << i][i] = 1;
    }

    for (int mask = 1; mask <= ALL; mask++) {
        for (int last = 0; last < n; last++) {
            if ((mask & (1 << last)) == 0) continue;
            if (dp[mask][last] == 0) continue;

            for (int next = 0; next < n; next++) {
                if ((mask & (1 << next)) != 0) continue;
                if (adj[last][next] == 0) continue;  // no edge
                int newMask = mask | (1 << next);
                dp[newMask][next] += dp[mask][last];
            }
        }
    }

    long count = 0;
    for (int last = 0; last < n; last++) {
        count += dp[ALL][last];
    }
    return count;
}
```

**Walkthrough with 3 vertices (complete graph):**
```
n=3, ALL=111

dp[001][0] = 1  (start at 0)
dp[010][1] = 1  (start at 1)
dp[100][2] = 1  (start at 2)

Expand dp[001][0]:
  → dp[011][1] += 1  (0→1)
  → dp[101][2] += 1  (0→2)

Expand dp[010][1]:
  → dp[011][0] += 1  (1→0)
  → dp[110][2] += 1  (1→2)

Expand dp[100][2]:
  → dp[101][0] += 1  (2→0)
  → dp[110][1] += 1  (2→1)

Expand dp[011][1]:
  → dp[111][2] += 1  (0→1→2)

Expand dp[101][2]:
  → dp[111][1] += 1  (0→2→1)

Expand dp[011][0]:
  → dp[111][2] += 1  (1→0→2)

Expand dp[110][2]:
  → dp[111][0] += 1  (1→2→0)

Expand dp[101][0]:
  → dp[111][1] += 1  (2→0→1)

Expand dp[110][1]:
  → dp[111][0] += 1  (2→1→0)

Total = dp[111][0] + dp[111][1] + dp[111][2] = 2 + 2 + 2 = 6 = 3! ✓
(all permutations of 3 vertices)
```

---

## 6. Minimum Cost to Visit All Nodes (TSP Variant)

Same as TSP but without returning to start:

```java
public int shortestHamiltonianPath(int[][] dist) {
    int n = dist.length;
    int ALL = (1 << n) - 1;
    int[][] dp = new int[1 << n][n];

    for (int[] row : dp) Arrays.fill(row, Integer.MAX_VALUE / 2);
    for (int i = 0; i < n; i++) dp[1 << i][i] = 0;

    for (int mask = 1; mask <= ALL; mask++) {
        for (int last = 0; last < n; last++) {
            if ((mask & (1 << last)) == 0) continue;
            for (int next = 0; next < n; next++) {
                if ((mask & (1 << next)) != 0) continue;
                int newMask = mask | (1 << next);
                dp[newMask][next] = Math.min(
                    dp[newMask][next],
                    dp[mask][last] + dist[last][next]
                );
            }
        }
    }

    int minCost = Integer.MAX_VALUE;
    for (int last = 0; last < n; last++) {
        minCost = Math.min(minCost, dp[ALL][last]);
    }
    return minCost;
}
```

---

## 7. Bitmask DP with SOS (Sum Over Subsets) Optimization

For problems where `dp[mask]` depends on all submasks of mask, SOS DP
computes this in O(n * 2^n) instead of O(3^n):

```java
// dp[mask] = sum of f[submask] for all submask ⊆ mask
int[] dp = new int[1 << n];
for (int i = 0; i < n; i++) {
    for (int mask = 0; mask < (1 << n); mask++) {
        if ((mask & (1 << i)) != 0) {
            dp[mask] += dp[mask ^ (1 << i)];
        }
    }
}
```

---

## 8. Summary Table

| Problem                        | State              | Time         | Space      |
|--------------------------------|--------------------|--------------|------------|
| TSP                            | dp[mask][last]     | O(2^n * n^2) | O(2^n * n) |
| Assignment Problem             | dp[mask]           | O(2^n * n)   | O(2^n)     |
| K Equal-Sum Partitions         | dp[mask]           | O(2^n * n)   | O(2^n)     |
| Hamiltonian Paths Count        | dp[mask][last]     | O(2^n * n^2) | O(2^n * n) |
| Shortest Hamiltonian Path      | dp[mask][last]     | O(2^n * n^2) | O(2^n * n) |
| SOS (Sum Over Subsets)         | dp[mask]           | O(n * 2^n)   | O(2^n)     |

**Practical limits:** n ≤ 20 for O(2^n * n^2), n ≤ 23 for O(2^n * n).
