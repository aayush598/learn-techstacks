# Knuth Optimization

**Reduces O(n³) interval DP to O(n²)** when the optimal partition point is monotonic.

## Condition

For dp[i][j] = min(dp[i][k-1] + dp[k][j] + C[i][j]), if:
- opt[i][j-1] ≤ opt[i][j] ≤ opt[i+1][j] (monotonicity)

Then we only need to check k from opt[i][j-1] to opt[i+1][j].

```java
int[][] dp = new int[n][n];
int[][] opt = new int[n][n]; // optimal k for each interval

for (int i = 0; i < n; i++) {
    dp[i][i] = 0;
    opt[i][i] = i;
}

for (int len = 2; len <= n; len++) {
    for (int i = 0; i + len - 1 < n; i++) {
        int j = i + len - 1;
        dp[i][j] = INF;
        for (int k = opt[i][j-1]; k <= Math.min(j-1, opt[i+1][j]); k++) {
            int val = dp[i][k] + dp[k+1][j] + cost(i, k, j);
            if (val < dp[i][j]) {
                dp[i][j] = val;
                opt[i][j] = k;
            }
        }
    }
}
```

## Key Insight

> The monotonicity condition means: as the interval grows, the optimal split point moves right (or stays). This drastically reduces the search space.
