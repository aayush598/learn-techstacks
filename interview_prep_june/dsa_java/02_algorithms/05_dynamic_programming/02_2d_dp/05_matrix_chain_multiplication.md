# Matrix Chain Multiplication (MCM)

**Problem**: Given dimensions of matrices A1×A2×...×An, find the minimum number of scalar multiplications to compute the product A1×A2×...×An by optimal parenthesization.

**Example**: `dims = [10, 30, 5, 60]` → matrices: 10×30, 30×5, 5×60
- ((A1×A2)×A3): 10×30×5 + 10×5×60 = 1,500 + 3,000 = 4,500
- (A1×(A2×A3)): 30×5×60 + 10×30×60 = 9,000 + 18,000 = 27,000
- Optimal: 4,500

---

## Recurrence

```
dp[i][j] = minimum multiplications to compute Ai × ... × Aj

dp[i][j] = min(dp[i][k] + dp[k+1][j] + dims[i-1]*dims[k]*dims[j])
            for k in [i, j-1]

Base: dp[i][i] = 0 (single matrix, no multiplication)
```

---

## Bottom-Up DP (Interval DP)

```java
public int matrixChainOrder(int[] dims) {
    int n = dims.length - 1; // number of matrices
    int[][] dp = new int[n + 1][n + 1];

    // dp[i][j] = 0 for i == j (single matrix)

    // len = length of chain (2 to n)
    for (int len = 2; len <= n; len++) {
        for (int i = 1; i <= n - len + 1; i++) {
            int j = i + len - 1;
            dp[i][j] = Integer.MAX_VALUE;

            for (int k = i; k < j; k++) {
                int cost = dp[i][k] + dp[k + 1][j]
                         + dims[i - 1] * dims[k] * dims[j];
                dp[i][j] = Math.min(dp[i][j], cost);
            }
        }
    }

    return dp[1][n];
}
```

### Trace for dims = [10, 30, 5, 60]

```
n = 3 matrices: A1(10×30), A2(30×5), A3(5×60)

len = 2:
  i=1,j=2: only k=1 → dp[1][2] = dp[1][1]+dp[2][2]+10*30*5 = 1500
  i=2,j=3: only k=2 → dp[2][3] = dp[2][2]+dp[3][3]+30*5*60 = 9000

len = 3:
  i=1,j=3:
    k=1: dp[1][1]+dp[2][3]+10*30*60 = 0+9000+18000 = 27000
    k=2: dp[1][2]+dp[3][3]+10*5*60 = 1500+0+3000 = 4500
    dp[1][3] = min(27000, 4500) = 4500

Answer: 4500
```

---

## Print Optimal Parenthesization

```java
public String matrixChainOrder(int[] dims) {
    int n = dims.length - 1;
    int[][] dp = new int[n + 1][n + 1];
    int[][] split = new int[n + 1][n + 1]; // stores optimal k

    for (int len = 2; len <= n; len++) {
        for (int i = 1; i <= n - len + 1; i++) {
            int j = i + len - 1;
            dp[i][j] = Integer.MAX_VALUE;

            for (int k = i; k < j; k++) {
                int cost = dp[i][k] + dp[k + 1][j]
                         + dims[i - 1] * dims[k] * dims[j];
                if (cost < dp[i][j]) {
                    dp[i][j] = cost;
                    split[i][j] = k;
                }
            }
        }
    }

    // Reconstruct
    return printParenthesization(split, 1, n);
}

private String printParenthesization(int[][] split, int i, int j) {
    if (i == j) return "A" + i;
    return "(" + printParenthesization(split, i, split[i][j])
           + " × " + printParenthesization(split, split[i][j] + 1, j) + ")";
}
```

---

## The Interval DP Pattern

MCM is the classic example of **interval DP**:

```
for length = 2 to n:
    for i = 0 to n-length:
        j = i + length - 1
        for k = i to j-1:
            dp[i][j] = min(dp[i][j], merge(dp[i][k], dp[k+1][j]))
```

This pattern applies to many problems where the answer for a range depends on splitting it optimally.

---

## Applications

### Burst Balloons

**Problem**: Burst balloons to maximize coins. Each balloon i has value nums[i]. When balloon i bursts, you get nums[i-1]*nums[i]*nums[i+1].

```java
public int maxCoins(int[] nums) {
    int n = nums.length;
    int[] balloons = new int[n + 2];
    balloons[0] = balloons[n + 1] = 1;
    for (int i = 0; i < n; i++) balloons[i + 1] = nums[i];

    int[][] dp = new int[n + 2][n + 2];

    for (int len = 1; len <= n; len++) {
        for (int i = 1; i <= n - len + 1; i++) {
            int j = i + len - 1;
            for (int k = i; k <= j; k++) {
                dp[i][j] = Math.max(dp[i][j],
                    dp[i][k - 1] + dp[k + 1][j]
                    + balloons[i - 1] * balloons[k] * balloons[j + 1]);
            }
        }
    }

    return dp[1][n];
}
```

### Minimum Cost to Merge Stones

**Problem**: Merge N piles of stones into one. Can only merge K consecutive piles. Cost of merging = sum of stones in the merged pile.

### Boolean Parenthesization

**Problem**: Given boolean expression with &, |, ^, count number of ways to parenthesize to get true.

```java
public int countEval(String s, int result) {
    int n = s.length();
    // dp[i][j][0] = ways to evaluate s[i..j] as false
    // dp[i][j][1] = ways to evaluate s[i..j] as true
    int[][][] dp = new int[n][n][2];

    for (int i = 0; i < n; i += 2) {
        dp[i][i][s.charAt(i) == 'T' ? 1 : 0] = 1;
    }

    for (int len = 2; len < n; len += 2) {
        for (int i = 0; i + len < n; i += 2) {
            int j = i + len;
            for (int k = i + 1; k < j; k += 2) {
                char op = s.charAt(k);
                // Combine dp[i][k-1] and dp[k+1][j] based on op
                for (int a = 0; a <= 1; a++) {
                    for (int b = 0; b <= 1; b++) {
                        int val = apply(a, b, op);
                        dp[i][j][val] += dp[i][k-1][a] * dp[k+1][j][b];
                    }
                }
            }
        }
    }

    return dp[0][n-1][result];
}
```

### Minimum Score Triangulation of Polygon

```java
public int minScoreTriangulation(int[] values) {
    int n = values.length;
    int[][] dp = new int[n][n];

    for (int len = 3; len <= n; len++) {
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            dp[i][j] = Integer.MAX_VALUE;
            for (int k = i + 1; k < j; k++) {
                dp[i][j] = Math.min(dp[i][j],
                    dp[i][k] + dp[k][j] + values[i]*values[k]*values[j]);
            }
        }
    }

    return dp[0][n - 1];
}
```

---

## Complexity

| Problem | Time | Space |
|---|---|---|
| MCM | O(n³) | O(n²) |
| Burst Balloons | O(n³) | O(n²) |
| Boolean Parenthesization | O(n³) | O(n²) |

## Key Takeaways

1. **Interval DP = process substrings/subarrays by increasing length**
2. **Outer loop is always over length** — ensures subproblems are solved before larger ones
3. **The partition point k splits the interval into two parts**
4. **MCM recurrence template**:
   ```
   dp[i][j] = optimize over k of (dp[i][k] + dp[k+1][j] + cost(i,k,j))
   ```
5. **O(n³) time, O(n²) space** — standard for interval DP
6. **Base case**: dp[i][i] = 0 (single element, no operation needed)
7. **Knuth optimization** can reduce O(n³) to O(n²) for some interval DP problems (when monotonicity holds)
