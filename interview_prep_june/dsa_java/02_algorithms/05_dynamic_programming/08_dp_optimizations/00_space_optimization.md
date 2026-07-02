# Space Optimization in DP

## 1. 1D from 2D: When dp[i] depends on dp[i-1]

```java
// 2D version
int[][] dp = new int[n + 1][m + 1];
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m; j++) {
        dp[i][j] = f(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]);
    }
}

// 1D version
int[] dp = new int[m + 1];
for (int i = 1; i <= n; i++) {
    int prev = dp[0]; // dp[i-1][j-1]
    for (int j = 1; j <= m; j++) {
        int temp = dp[j]; // dp[i-1][j]
        dp[j] = f(temp, dp[j-1], prev);
        prev = temp;
    }
}
```

## 2. Rolling Array (dp[i%2])

```java
int[][] dp = new int[2][m + 1];
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m; j++) {
        dp[i % 2][j] = f(dp[(i-1) % 2][j], dp[i % 2][j-1]);
    }
}
return dp[n % 2][m];
```

## 3. Single Variable (Fibonacci-like)

```java
// O(n) space → O(1)
int prev2 = 0, prev1 = 1;
for (int i = 2; i <= n; i++) {
    int curr = prev1 + prev2;
    prev2 = prev1;
    prev1 = curr;
}
return prev1;
```

## Common Optimizations

| Problem | Original Space | Optimized |
|---|---|---|
| LCS | O(m*n) | O(min(m,n)) |
| Knapsack | O(N*W) | O(W) |
| Min Path Sum | O(m*n) | O(n) |
| Unique Paths | O(m*n) | O(n) |

## Key Insight

> If dp[i] depends only on dp[i-1] (or a few previous rows), we can compress to 1D or rolling array. The direction of iteration (forward/backward) matters.
