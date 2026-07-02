# Interval DP Pattern

## When to Use

Look for:
- "Problem involves subarrays/substrings"
- "Combine adjacent elements"
- "Parenthesization", "Merge stones"
- DP on intervals [i, j] where result depends on splitting the interval

## Template

```java
int n = arr.length;
int[][] dp = new int[n][n];

// Initialize base cases (length = 1)
for (int i = 0; i < n; i++) dp[i][i] = base;

// Length increasing order
for (int len = 2; len <= n; len++) {
    for (int i = 0; i + len - 1 < n; i++) {
        int j = i + len - 1;
        dp[i][j] = INF;
        for (int k = i; k < j; k++) {
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j] + cost(i, k, j));
        }
    }
}
```

## Derivative Problems

| Problem | Cost Function |
|---|---|
| MCM | dims[i]*dims[k]*dims[j] |
| Burst Balloons | nums[i-1]*nums[k]*nums[j+1] |
| Min Score Triangulation | values[i]*values[k]*values[j] |
| Boolean Parenthesization | Ways to evaluate to true/false |
| Min Cost to Merge Stones | Sum of stones in range |

## Key Insight

> Interval DP processes subarrays by length. The partition point k divides the interval into two independent subproblems. All are O(n³) time, O(n²) space.
