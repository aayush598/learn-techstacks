# Minimum Path Sum

**Problem**: Given an m×n grid filled with non-negative numbers, find a path from top-left to bottom-right that minimizes the sum of numbers along the path. You can only move right or down.

---

## Recurrence

```
dp[i][j] = minimum sum to reach cell (i, j)
dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])

Base: dp[0][0] = grid[0][0]
      dp[i][0] = grid[i][0] + dp[i-1][0]  (first column)
      dp[0][j] = grid[0][j] + dp[0][j-1]  (first row)
```

---

## Bottom-Up DP

```java
public int minPathSum(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    int[][] dp = new int[m][n];

    dp[0][0] = grid[0][0];

    // Initialize first row
    for (int j = 1; j < n; j++) {
        dp[0][j] = dp[0][j - 1] + grid[0][j];
    }

    // Initialize first column
    for (int i = 1; i < m; i++) {
        dp[i][0] = dp[i - 1][0] + grid[i][0];
    }

    // Fill rest
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[i][j] = grid[i][j] + Math.min(dp[i - 1][j], dp[i][j - 1]);
        }
    }

    return dp[m - 1][n - 1];
}
```

### Space-Optimized (1D)

```java
public int minPathSum(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    int[] dp = new int[n];

    // First row
    dp[0] = grid[0][0];
    for (int j = 1; j < n; j++) {
        dp[j] = dp[j - 1] + grid[0][j];
    }

    // Remaining rows
    for (int i = 1; i < m; i++) {
        dp[0] += grid[i][0]; // first column
        for (int j = 1; j < n; j++) {
            dp[j] = grid[i][j] + Math.min(dp[j], dp[j - 1]);
        }
    }

    return dp[n - 1];
}
```

### In-place (Modifying Input)

```java
public int minPathSum(int[][] grid) {
    int m = grid.length, n = grid[0].length;

    for (int i = 2; i < n; i++) grid[0][i] += grid[0][i - 1];
    for (int i = 2; i < m; i++) grid[i][0] += grid[i - 1][0];

    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            grid[i][j] += Math.min(grid[i - 1][j], grid[i][j - 1]);
        }
    }

    return grid[m - 1][n - 1];
}
```

---

## Triangular Grid

**Problem**: Given a triangle of numbers, find minimum path sum from top to bottom moving to adjacent numbers on the row below.

```java
public int minimumTotal(List<List<Integer>> triangle) {
    int n = triangle.size();
    // Start from bottom and go up
    int[] dp = new int[n];

    // Initialize with last row
    List<Integer> lastRow = triangle.get(n - 1);
    for (int i = 0; i < n; i++) {
        dp[i] = lastRow.get(i);
    }

    // Bottom-up
    for (int i = n - 2; i >= 0; i--) {
        List<Integer> row = triangle.get(i);
        for (int j = 0; j < row.size(); j++) {
            dp[j] = row.get(j) + Math.min(dp[j], dp[j + 1]);
        }
    }

    return dp[0];
}
```

---

## Complexity

| Version | Time | Space |
|---|---|---|
| Full DP | O(m*n) | O(m*n) |
| 1D DP | O(m*n) | O(n) |
| In-place | O(m*n) | O(1) |

## Key Takeaways

1. **Classic grid DP**: dp[i][j] depends on dp[i-1][j] (top) and dp[i][j-1] (left)
2. **Initialize first row and first column** before main loop
3. **Space optimization**: 1D array + single variable
4. **Bottom-up from triangle**: simpler to compute from bottom to top
