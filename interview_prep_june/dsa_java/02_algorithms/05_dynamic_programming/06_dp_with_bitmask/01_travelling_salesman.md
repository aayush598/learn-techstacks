# Travelling Salesman Problem (TSP)

**Problem**: Given a set of cities and distance between each pair, find the shortest tour visiting each city exactly once and returning to the start.

---

## State Definition

```
dp[mask][last] = minimum distance to reach state where:
  - mask represents visited cities (bit i = 1 means visited)
  - last is the current city
```

**Base**: `dp[1 << 0][0] = 0` (start at city 0)

**Transition**:
```
dp[mask | (1 << next)][next] = min(dp[mask | (1 << next)][next],
                                    dp[mask][last] + dist[last][next])
```

**Answer**: `min(dp[(1 << n) - 1][last] + dist[last][0])` for all last ≠ 0

---

## Implementation

```java
public int tsp(int[][] dist) {
    int n = dist.length;
    int[][] dp = new int[1 << n][n];

    // Initialize with large value
    for (int[] row : dp) Arrays.fill(row, Integer.MAX_VALUE / 2);
    dp[1 << 0][0] = 0; // start at city 0

    for (int mask = 0; mask < (1 << n); mask++) {
        for (int last = 0; last < n; last++) {
            if ((mask & (1 << last)) == 0) continue; // last not in mask
            if (dp[mask][last] == Integer.MAX_VALUE / 2) continue;

            for (int next = 0; next < n; next++) {
                if ((mask & (1 << next)) != 0) continue; // already visited

                int newMask = mask | (1 << next);
                dp[newMask][next] = Math.min(dp[newMask][next],
                                            dp[mask][last] + dist[last][next]);
            }
        }
    }

    // Return to start
    int allVisited = (1 << n) - 1;
    int minCost = Integer.MAX_VALUE;
    for (int last = 1; last < n; last++) {
        minCost = Math.min(minCost, dp[allVisited][last] + dist[last][0]);
    }

    return minCost;
}
```

### Trace for n=4 cities

```
dist matrix:
  [0, 10, 15, 20]
  [10, 0, 35, 25]
  [15, 35, 0, 30]
  [20, 25, 30, 0]

dp table (showing non-INF values):

mask=0001 (visited {0}):
  dp[0001][0] = 0

mask=0011 (visited {0,1}):
  dp[0011][1] = dp[0001][0] + dist[0][1] = 0 + 10 = 10

mask=0101 (visited {0,2}):
  dp[0101][2] = dp[0001][0] + dist[0][2] = 0 + 15 = 15

mask=1001 (visited {0,3}):
  dp[1001][3] = dp[0001][0] + dist[0][3] = 0 + 20 = 20

mask=0111 (visited {0,1,2}):
  dp[0111][2] = min(dp[0011][1] + dist[1][2], ...)
              = 10 + 35 = 45
  dp[0111][1] = dp[0101][2] + dist[2][1] = 15 + 35 = 50

mask=1011 (visited {0,1,3}):
  dp[1011][1] = dp[1001][3] + dist[3][1] = 20 + 25 = 45
  dp[1011][3] = dp[0011][1] + dist[1][3] = 10 + 25 = 35

mask=1101 (visited {0,2,3}):
  dp[1101][2] = dp[1001][3] + dist[3][2] = 20 + 30 = 50
  dp[1101][3] = dp[0101][2] + dist[2][3] = 15 + 30 = 45

mask=1111 (visited {0,1,2,3}):
  dp[1111][1] = dp[0111][2] + dist[2][1] = 45 + 35 = 80
  dp[1111][2] = dp[1011][1] + dist[1][2] = 45 + 35 = 80
  dp[1111][3] = min(dp[0111][1] + dist[1][3], dp[1101][2] + dist[2][3])
              = min(50 + 25, 50 + 30) = 75

Return to start:
  from 1: 80 + dist[1][0] = 80 + 10 = 90
  from 2: 80 + dist[2][0] = 80 + 15 = 95
  from 3: 75 + dist[3][0] = 75 + 20 = 95

Answer: 80 (0→1→3→2→0? No, that would be... let me check: 0→1=10, 1→3=25, 3→2=30, 2→0=15 → total=80 ✓)
```

---

## Complexity

| Version | Time | Space |
|---|---|---|
| Standard DP | O(n² * 2^n) | O(n * 2^n) |

n ≤ 15: 7 million operations, 480 KB
n ≤ 20: 419 million operations, 20 MB (borderline)

---

## Space-Optimized

```java
public int tsp(int[][] dist) {
    int n = dist.length;
    int[][] dp = new int[1 << n][n];
    for (int[] row : dp) Arrays.fill(row, Integer.MAX_VALUE / 2);
    dp[1][0] = 0;

    for (int mask = 1; mask < (1 << n); mask += 2) { // only masks with city 0
        for (int last = 0; last < n; last++) {
            if ((mask & (1 << last)) == 0) continue;
            if (dp[mask][last] == Integer.MAX_VALUE / 2) continue;

            for (int next = 0; next < n; next++) {
                if ((mask & (1 << next)) != 0) continue;
                int newMask = mask | (1 << next);
                dp[newMask][next] = Math.min(dp[newMask][next],
                                            dp[mask][last] + dist[last][next]);
            }
        }
    }

    int all = (1 << n) - 1;
    int min = Integer.MAX_VALUE;
    for (int i = 1; i < n; i++) {
        min = Math.min(min, dp[all][i] + dist[i][0]);
    }
    return min;
}
```

**Optimization**: only iterate masks that include city 0 (odd numbers).

---

## Key Takeaways

1. **dp[mask][last]**: the minimum cost to visit the set `mask` ending at `last`
2. **Base**: dp[1][0] = 0 (start at city 0)
3. **Answer**: min over last of dp[all][last] + dist[last][0]
4. **O(n² * 2^n) time** — feasible for n ≤ 20
5. **Always include city 0** — mask is always odd (bit 0 = 1)
