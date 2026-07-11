# Knuth Optimization

**Reduces O(n³) interval DP to O(n²)** when the optimal partition point is monotonic.

## When Knuth Optimization Works

For DP of the form:

```
dp[i][j] = min { dp[i][k] + dp[k+1][j] + cost(i, j) }    for i ≤ k < j
     i<k<j
```

The naive approach checks all k from i to j-1, leading to O(n³).

Knuth optimization applies when **two conditions** hold:

1. **Quadrangle Inequality (QI)**: cost(i, j) is quadrangle-inequality-convex
   - cost(a, c) + cost(b, d) ≤ cost(a, d) + cost(b, c) for a ≤ b ≤ c ≤ d
   - i.e., cost doesn't increase faster for wider intervals

2. **Monotonicity of opt**: The optimal split point `opt[i][j]` is monotonic:
   - `opt[i][j-1] ≤ opt[i][j] ≤ opt[i+1][j]`
   - As interval widens, the optimal split moves right (or stays)

When these hold, we only need to check k from `opt[i][j-1]` to `opt[i+1][j]`, which amortizes to O(1) per state — total O(n²).

## Generic Template

```java
public class KnuthOptimization {

    public static int solve(int n, int[][] cost) {
        int[][] dp = new int[n][n];
        int[][] opt = new int[n][n];

        // Initialize single-element intervals
        for (int i = 0; i < n; i++) {
            dp[i][i] = 0;          // base cost
            opt[i][i] = i;          // only possible split
        }

        // Build intervals by increasing length
        for (int len = 2; len <= n; len++) {
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;
                dp[i][j] = Integer.MAX_VALUE;

                // Only check narrowed range
                int startK = opt[i][j - 1];
                int endK = Math.min(j - 1, opt[i + 1][j]);

                for (int k = startK; k <= endK; k++) {
                    int val = dp[i][k] + dp[k + 1][j] + cost[i][j];
                    if (val < dp[i][j]) {
                        dp[i][j] = val;
                        opt[i][j] = k;
                    }
                }
            }
        }
        return dp[0][n - 1];
    }
}
```

### Why the narrowed loop works

The monotonicity `opt[i][j-1] ≤ opt[i][j] ≤ opt[i+1][j]` means:
- When computing dp[i][j], we already know opt[i][j-1] (from smaller interval ending at j-1)
- And opt[i+1][j] (from smaller interval starting at i+1)
- The optimal k for dp[i][j] must lie between these two values

Each k is checked in O(1) intervals on average, so total work is O(n²).

## Classic Example: Optimal BST

Given n keys with frequencies `freq[i]`, build a BST that minimizes expected search cost.

```
dp[i][j] = min cost of BST containing keys i..j
cost(i,j) = sum of frequencies of keys i..j (each node adds depth 1)
```

```java
public class OptimalBST {

    public static int optimalBST(int[] freq) {
        int n = freq.length;
        int[][] dp = new int[n][n];
        int[][] opt = new int[n][n];
        int[][] prefix = new int[n + 1][n + 1]; // precomputed costs

        // Precompute cost(i,j) = sum of freq[i..j]
        int[] prefSum = new int[n + 1];
        for (int i = 0; i < n; i++) {
            prefSum[i + 1] = prefSum[i] + freq[i];
        }

        for (int i = 0; i < n; i++) {
            dp[i][i] = freq[i];
            opt[i][i] = i;
        }

        for (int len = 2; len <= n; len++) {
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;
                int sum = prefSum[j + 1] - prefSum[i];
                dp[i][j] = Integer.MAX_VALUE;

                int startK = opt[i][j - 1];
                int endK = Math.min(j - 1, opt[i + 1][j]);

                for (int k = startK; k <= endK; k++) {
                    int leftCost = (k > i) ? dp[i][k - 1] : 0;
                    int rightCost = (k < j) ? dp[k + 1][j] : 0;
                    int val = leftCost + rightCost + sum;
                    if (val < dp[i][j]) {
                        dp[i][j] = val;
                        opt[i][j] = k;
                    }
                }
            }
        }
        return dp[0][n - 1];
    }

    public static void main(String[] args) {
        int[] freq = {4, 2, 6, 3};
        // Keys with frequencies: k1(4), k2(2), k3(6), k4(3)
        System.out.println(optimalBST(freq));  // Minimum search cost
    }
}
```

### Walkthrough for freq = [4, 2, 6, 3]

| Interval | Length | Candidates | opt[i][j] |
|----------|--------|------------|-----------|
| [0,0] | 1 | — | 0 |
| [1,1] | 1 | — | 1 |
| [2,2] | 1 | — | 2 |
| [3,3] | 1 | — | 3 |
| [0,1] | 2 | k=0: 4+0+6=10, k=1: 0+2+6=8 | 1 |
| [1,2] | 2 | k=1: 2+0+8=10, k=2: 0+6+8=14 | 1 |
| [2,3] | 2 | k=2: 6+0+9=15, k=3: 0+3+9=12 | 3 |
| [0,2] | 3 | k from opt[0][1]=1 to opt[1][2]=1: only k=1: dp[0][0]+dp[2][2]+12=4+6+12=22 | 1 |
| [1,3] | 3 | k from opt[1][2]=1 to opt[2][3]=3: k=1: 2+dp[2][3]=2+12=14+11=25, k=2: dp[1][1]+dp[3][3]=2+3=5+11=16, k=3: dp[1][2]+0=10+11=21 | 2 |
| [0,3] | 4 | k from opt[0][2]=1 to opt[1][3]=2: k=1: 4+dp[2][3]+15=4+12+15=31, k=2: dp[0][1]+3+15=8+3+15=26 | 2 |

Without optimization: 14 candidate checks. With optimization: 8. For n=100, it's ~3300 vs ~166,000.

## Comparison with Divide and Conquer Optimization

| Aspect | Knuth Optimization | Divide & Conquer Optimization |
|--------|-------------------|-------------------------------|
| DP form | dp[i][j] = min(dp[i][k] + dp[k+1][j] + C(i,j)) | dp[i][j] = min(dp[i-1][k] + C(k+1,j)) |
| Dimension | 2D intervals | 2D (layers) |
| Monotonicity | opt[i][j-1] ≤ opt[i][j] ≤ opt[i+1][j] | opt[i][j] ≤ opt[i][j+1] |
| Complexity reduction | O(n³) → O(n²) | O(k·n²) → O(k·n log n) |
| Typical problem | Optimal BST, matrix chain | DP with convex hull trick |

## When NOT to Use Knuth Optimization

1. **Cost is not QI-convex**: If cost doesn't satisfy quadrangle inequality, the monotonicity condition may not hold.
2. **DP form doesn't match**: Knuth requires dp[i][j] = min(dp[i][k] + dp[k+1][j] + cost(i,j)). If the recurrence has extra terms or is not an interval DP, it won't work.
3. **opt is not monotonic**: Always verify with brute-force for small n before relying on Knuth.

### Counterexample: Non-monotonic opt

Consider `cost(i,j) = (j - i)²` instead of a prefix-sum-based cost. The cost grows quadratically, and QI may be violated:

```
cost(0,3) + cost(1,2) = 9 + 1 = 10
cost(0,2) + cost(1,3) = 4 + 4 = 8
```

Since 10 > 8, QI is violated (needs ≤). The monotonicity of opt breaks, and Knuth optimization would give the wrong answer.

## Key Insight

> The monotonicity condition means: as the interval grows, the optimal split point moves right (or stays). This drastically reduces the search space. Combined with quadrangle inequality on the cost function, it guarantees O(n²) total runtime — each opt[i][j] is evaluated in amortized O(1) time.

## Verification Checklist

```java
public class VerifyMonotonicity {

    // Brute force to check if Knuth applies
    public static boolean checkMonotonicity(int n, int[][] cost) {
        int[][] opt = bruteForceOpt(n, cost);
        for (int i = 0; i < n; i++) {
            for (int j = i + 2; j < n; j++) {
                if (opt[i][j - 1] > opt[i][j]) return false;
                if (opt[i][j] > opt[i + 1][j]) return false;
            }
        }
        return true;
    }

    private static int[][] bruteForceOpt(int n, int[][] cost) {
        int[][] dp = new int[n][n];
        int[][] opt = new int[n][n];
        for (int i = 0; i < n; i++) {
            dp[i][i] = 0; opt[i][i] = i;
        }
        for (int len = 2; len <= n; len++) {
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;
                dp[i][j] = Integer.MAX_VALUE;
                for (int k = i; k < j; k++) {
                    int val = dp[i][k] + dp[k + 1][j] + cost[i][j];
                    if (val < dp[i][j]) {
                        dp[i][j] = val;
                        opt[i][j] = k;
                    }
                }
            }
        }
        return opt;
    }
}
```
