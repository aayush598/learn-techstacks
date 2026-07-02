# Maximal Square

**Problem**: Given an m×n binary matrix filled with 0s and 1s, find the largest square containing only 1s and return its area.

---

## Recurrence

```
dp[i][j] = side length of largest square ending at (i, j)

dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1   if matrix[i][j] == '1'
         = 0                                               if matrix[i][j] == '0'

Base: First row/col: dp[i][j] = matrix[i][j] - '0'
```

---

## Bottom-Up DP

```java
public int maximalSquare(char[][] matrix) {
    if (matrix.length == 0) return 0;
    int m = matrix.length, n = matrix[0].length;
    int[][] dp = new int[m][n];
    int maxSide = 0;

    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (matrix[i][j] == '1') {
                if (i == 0 || j == 0) {
                    dp[i][j] = 1;
                } else {
                    dp[i][j] = Math.min(dp[i - 1][j],
                               Math.min(dp[i][j - 1], dp[i - 1][j - 1])) + 1;
                }
                maxSide = Math.max(maxSide, dp[i][j]);
            }
        }
    }

    return maxSide * maxSide;
}
```

### Why Min of Three?

For a square of side k ending at (i,j), we need:
- A square of side k-1 above: dp[i-1][j] ≥ k-1
- A square of side k-1 to the left: dp[i][j-1] ≥ k-1
- A square of side k-1 diagonally: dp[i-1][j-1] ≥ k-1

The side length is limited by the smallest of these three.

### Space-Optimized

```java
public int maximalSquare(char[][] matrix) {
    if (matrix.length == 0) return 0;
    int m = matrix.length, n = matrix[0].length;
    int[] dp = new int[n + 1];
    int maxSide = 0, prev = 0;

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            int temp = dp[j];
            if (matrix[i - 1][j - 1] == '1') {
                dp[j] = Math.min(dp[j], Math.min(dp[j - 1], prev)) + 1;
                maxSide = Math.max(maxSide, dp[j]);
            } else {
                dp[j] = 0;
            }
            prev = temp;
        }
    }

    return maxSide * maxSide;
}
```

---

## Complexity

| Version | Time | Space |
|---|---|---|
| Full DP | O(m*n) | O(m*n) |
| 1D DP | O(m*n) | O(n) |

## Key Takeaways

1. **Min of (top, left, diagonal) + 1** — the core insight
2. **Answer is area = maxSide²**, not maxSide
3. **Initialization**: first row/col cells = 1 if they contain '1'
4. **Space optimization**: need `prev` variable for dp[i-1][j-1]
