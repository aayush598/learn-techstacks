# Fibonacci & Climbing Stairs

## Fibonacci Numbers

**Recurrence**: F(n) = F(n-1) + F(n-2), with F(0) = 0, F(1) = 1

### Naive Recursion (O(2^n))

```java
public int fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}
```

**Problem**: Exponential time. fib(50) would take years.

### Top-Down DP (O(n))

```java
public int fib(int n) {
    Integer[] memo = new Integer[n + 1];
    return fibMemo(n, memo);
}

private int fibMemo(int n, Integer[] memo) {
    if (n <= 1) return n;
    if (memo[n] != null) return memo[n];
    memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
    return memo[n];
}
```

### Bottom-Up DP (O(n))

```java
public int fib(int n) {
    if (n <= 1) return n;
    int[] dp = new int[n + 1];
    dp[0] = 0;
    dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}
```

### Space Optimized (O(1))

```java
public int fib(int n) {
    if (n <= 1) return n;
    int prev2 = 0, prev1 = 1;
    for (int i = 2; i <= n; i++) {
        int curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

---

## Climbing Stairs

**Problem**: You're climbing a staircase with n steps. Each time you can climb 1 or 2 steps. How many distinct ways to reach the top?

**Recurrence**: Same as Fibonacci! ways(n) = ways(n-1) + ways(n-2)

### Why?

To reach step n, you must have come from either:
- Step n-1 (then take 1 step)
- Step n-2 (then take 2 steps)

So total ways to reach n = ways to reach n-1 + ways to reach n-2

```java
public int climbStairs(int n) {
    if (n <= 2) return n;
    int[] dp = new int[n + 1];
    dp[1] = 1;
    dp[2] = 2;
    for (int i = 3; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}

// Space-optimized
public int climbStairs(int n) {
    if (n <= 2) return n;
    int prev2 = 1, prev1 = 2;
    for (int i = 3; i <= n; i++) {
        int curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

---

## Min Cost Climbing Stairs

**Problem**: Each step has a cost. You can climb 1 or 2 steps. Find minimum cost to reach the top.

```java
public int minCostClimbingStairs(int[] cost) {
    int n = cost.length;
    int[] dp = new int[n];
    dp[0] = cost[0];
    dp[1] = cost[1];

    for (int i = 2; i < n; i++) {
        dp[i] = cost[i] + Math.min(dp[i - 1], dp[i - 2]);
    }

    // Can end at last step or second-to-last step
    return Math.min(dp[n - 1], dp[n - 2]);
}

// Space-optimized
public int minCostClimbingStairs(int[] cost) {
    int prev2 = cost[0], prev1 = cost[1];
    for (int i = 2; i < cost.length; i++) {
        int curr = cost[i] + Math.min(prev1, prev2);
        prev2 = prev1;
        prev1 = curr;
    }
    return Math.min(prev1, prev2);
}
```

### With Different Starting Options

```java
public int minCostClimbingStairs(int[] cost) {
    int n = cost.length;
    // dp[i] = min cost to reach step i (before paying cost[i])
    int prev2 = 0, prev1 = 0; // start before step 0

    for (int i = 2; i <= n; i++) {
        int curr = Math.min(prev1 + cost[i - 1], prev2 + cost[i - 2]);
        prev2 = prev1;
        prev1 = curr;
    }

    return prev1;
}
```

---

## Tribonacci

**Recurrence**: T(n) = T(n-1) + T(n-2) + T(n-3)

```java
public int tribonacci(int n) {
    if (n == 0) return 0;
    if (n <= 2) return 1;

    int t0 = 0, t1 = 1, t2 = 1;
    for (int i = 3; i <= n; i++) {
        int t3 = t0 + t1 + t2;
        t0 = t1;
        t1 = t2;
        t2 = t3;
    }
    return t2;
}
```

---

## Pattern Recognition

These problems all use the same pattern:

```
dp[i] = combination of dp[i-1], dp[i-2], (dp[i-3], ...)
```

| Problem | Recurrence | Base Cases |
|---|---|---|
| Fibonacci | dp[i] = dp[i-1] + dp[i-2] | dp[0]=0, dp[1]=1 |
| Climbing Stairs | dp[i] = dp[i-1] + dp[i-2] | dp[1]=1, dp[2]=2 |
| Min Cost Stairs | dp[i] = cost[i] + min(dp[i-1], dp[i-2]) | dp[0]=cost[0], dp[1]=cost[1] |
| Tribonacci | dp[i] = dp[i-1] + dp[i-2] + dp[i-3] | dp[0]=0, dp[1]=1, dp[2]=1 |

### General Solution Template

```java
public int solve(int n) {
    // 1. Handle base cases
    if (n < baseLength) return baseValue;

    // 2. Initialize previous k values
    int[] prev = new int[k];
    for (int i = 0; i < k; i++) prev[i] = baseCase[i];

    // 3. Iterate
    for (int i = k; i <= n; i++) {
        int curr = combine(prev);  // function of prev[0..k-1]
        shift(prev, curr);         // shift window
    }

    return prev[lastIndex];
}
```

### Multi-step Climbing

If you can climb 1, 2, or 3 steps:

```java
public int climbStairs(int n) {
    if (n <= 2) return n;
    if (n == 3) return 4;

    int prev3 = 1, prev2 = 2, prev1 = 4;
    for (int i = 4; i <= n; i++) {
        int curr = prev1 + prev2 + prev3;
        prev3 = prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

If you can climb any step size from a given array `steps[]`:

```java
public int climbStairs(int n, int[] steps) {
    int[] dp = new int[n + 1];
    dp[0] = 1; // one way to be at step 0

    for (int i = 1; i <= n; i++) {
        for (int step : steps) {
            if (i >= step) {
                dp[i] += dp[i - step];
            }
        }
    }
    return dp[n];
}
```

---

## Complexity

| Algorithm | Time | Space |
|---|---|---|
| Naive recursive | O(2^n) | O(n) stack |
| Top-down DP | O(n) | O(n) |
| Bottom-up DP | O(n) | O(n) |
| Space-optimized | O(n) | O(1) |

## Key Insight

> Fibonacci-like recurrences are the simplest DP: each state depends only on the previous 1-3 states. Always optimize to O(1) space.
