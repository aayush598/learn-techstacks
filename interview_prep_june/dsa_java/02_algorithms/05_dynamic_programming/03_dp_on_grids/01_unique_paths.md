# Unique Paths

**Problem**: A robot is at top-left corner of an m×n grid. It can only move right or down. How many unique paths to the bottom-right corner?

---

## Recurrence

```
dp[i][j] = number of paths to reach cell (i, j)
dp[i][j] = dp[i-1][j] + dp[i][j-1]

Base: dp[0][j] = 1 (only one way: all rights)
      dp[i][0] = 1 (only one way: all downs)
```

---

## Bottom-Up DP

```java
public int uniquePaths(int m, int n) {
    int[][] dp = new int[m][n];

    for (int i = 0; i < m; i++) dp[i][0] = 1;
    for (int j = 0; j < n; j++) dp[0][j] = 1;

    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        }
    }

    return dp[m - 1][n - 1];
}

// Space-optimized
public int uniquePaths(int m, int n) {
    int[] dp = new int[n];
    Arrays.fill(dp, 1);

    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[j] += dp[j - 1];
        }
    }

    return dp[n - 1];
}
```

### Combinatorics Solution

From (0,0) to (m-1,n-1), we need (m-1) downs and (n-1) rights, total (m+n-2) moves. Choose which (m-1) moves are downs:

```java
public int uniquePaths(int m, int n) {
    // C(m+n-2, m-1)
    long result = 1;
    int total = m + n - 2;
    int k = Math.min(m - 1, n - 1); // use smaller for fewer iterations

    for (int i = 1; i <= k; i++) {
        result = result * (total - k + i) / i;
    }

    return (int) result;
}
```

---

## With Obstacles

**Problem**: Same grid, but some cells have obstacles (value 1). Robot cannot pass through obstacles.

```java
public int uniquePathsWithObstacles(int[][] obstacleGrid) {
    int m = obstacleGrid.length, n = obstacleGrid[0].length;

    if (obstacleGrid[0][0] == 1) return 0;

    int[][] dp = new int[m][n];
    dp[0][0] = 1;

    // First column
    for (int i = 1; i < m; i++) {
        dp[i][0] = (obstacleGrid[i][0] == 0 && dp[i - 1][0] == 1) ? 1 : 0;
    }

    // First row
    for (int j = 1; j < n; j++) {
        dp[0][j] = (obstacleGrid[0][j] == 0 && dp[0][j - 1] == 1) ? 1 : 0;
    }

    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            if (obstacleGrid[i][j] == 1) {
                dp[i][j] = 0;
            } else {
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
            }
        }
    }

    return dp[m - 1][n - 1];
}
```

---

## Complexity

| Version | Time | Space |
|---|---|---|
| DP | O(m*n) | O(m*n) |
| 1D DP | O(m*n) | O(n) |
| Combinatorics | O(min(m,n)) | O(1) |

## Key Takeaways

1. **Same as min path sum** but with addition instead of min
2. **Combinatorics O(1) space** — use C(m+n-2, m-1)
3. **Obstacles**: set dp[i][j] = 0 for blocked cells
4. **Overflow warning**: combinatorics involves large numbers — use long and careful division
