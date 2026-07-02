# Memoization vs Tabulation

Two ways to implement DP: top-down (memoization) and bottom-up (tabulation).

---

## Top-Down (Memoization)

Recursive approach with caching. Start from the problem and recurse down to base cases.

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

### Structure

```java
Result solve(State state, Cache cache) {
    // 1. Base case
    if (isBaseCase(state)) return baseValue;

    // 2. Check cache
    if (cache.contains(state)) return cache.get(state);

    // 3. Compute result using subproblems
    Result result = combine(solve(subState1), solve(subState2), ...);

    // 4. Cache and return
    cache.put(state, result);
    return result;
}
```

### Cache Types

```java
// 1D: array
Integer[] memo = new Integer[n + 1];

// 2D: 2D array
int[][] memo = new int[m + 1][n + 1];
for (int[] row : memo) Arrays.fill(row, -1);

// Sparse: HashMap
Map<String, Integer> memo = new HashMap<>();
// Key encoding: "i,j,sum"

// Multi-dimensional: nested maps (rare)
Map<Integer, Map<Integer, Integer>> memo = new HashMap<>();
```

### When to Use Top-Down

1. **Complex recurrence** — easier to write recursively
2. **Not all states needed** — memoization only computes reachable states
3. **Natural recursive formulation** — the problem is easier to think about recursively
4. **Quick prototyping** — fastest way to convert brute force to DP

---

## Bottom-Up (Tabulation)

Iterative approach. Start from base cases and fill the table in order.

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

### Structure

```java
Result solve(Input input) {
    // 1. Initialize DP table with base cases
    dp[baseState] = baseValue;

    // 2. Iterate over all states in order
    for (State state : states) {
        // 3. Compute from already-computed smaller states
        dp[state] = combine(dp[prev1], dp[prev2], ...);
    }

    // 4. Return answer
    return dp[finalState];
}
```

### When to Use Bottom-Up

1. **Simple recurrence** — easy iterative formula
2. **All states needed** — DP table is fully filled anyway
3. **Space optimization needed** — easier to optimize space iteratively
4. **Performance critical** — no recursion overhead

---

## Converting Top-Down to Bottom-Up

### Step-by-Step Process

```java
// TOP-DOWN
int solve(int n) {
    Integer[] memo = new Integer[n + 1];
    return dp(n, memo);
}
int dp(int i, Integer[] memo) {
    if (i == 0) return 0;  // base case
    if (i == 1) return 1;  // base case
    if (memo[i] != null) return memo[i];
    memo[i] = dp(i - 1, memo) + dp(i - 2, memo);
    return memo[i];
}

// BOTTOM-UP
int solve(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    int[] dp = new int[n + 1];
    dp[0] = 0;  // base case
    dp[1] = 1;  // base case
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2]; // same recurrence
    }
    return dp[n];
}
```

### Rules for Conversion

| Top-Down | Bottom-Up |
|---|---|
| Base case `if (i == 0) return X` | `dp[0] = X` |
| Recursive call `dp(i-1)` | Previous row/iteration `dp[i-1]` |
| Return value at `i=n` | Answer at `dp[n]` |
| Memo check `if (memo[i] != null)` | No check needed (already computed) |

### Complex Example: LCS

```java
// TOP-DOWN
int lcs(String s1, String s2, int i, int j, int[][] memo) {
    if (i == 0 || j == 0) return 0;
    if (memo[i][j] != -1) return memo[i][j];

    if (s1.charAt(i-1) == s2.charAt(j-1)) {
        memo[i][j] = 1 + lcs(s1, s2, i-1, j-1, memo);
    } else {
        memo[i][j] = Math.max(lcs(s1, s2, i-1, j, memo),
                              lcs(s1, s2, i, j-1, memo));
    }
    return memo[i][j];
}

// BOTTOM-UP
int lcs(String s1, String s2) {
    int m = s1.length(), n = s2.length();
    int[][] dp = new int[m+1][n+1];

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1.charAt(i-1) == s2.charAt(j-1)) {
                dp[i][j] = 1 + dp[i-1][j-1];
            } else {
                dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
            }
        }
    }
    return dp[m][n];
}
```

---

## Performance Comparison

### Fibonacci with Top-Down

```
fib(5) → fib(4) + fib(3)
       → fib(3) + fib(2) + fib(2) + fib(1)
       → ...
Calls: fib(5), fib(4), fib(3), fib(2), fib(1) = 5 unique calls
Memoization avoids recomputing the same values.
```

### Fibonacci with Bottom-Up

```
dp[0]=0, dp[1]=1
dp[2]=dp[1]+dp[0]=1
dp[3]=dp[2]+dp[1]=2
dp[4]=dp[3]+dp[2]=3
dp[5]=dp[4]+dp[3]=5
// Fills array sequentially, no recursion overhead
```

### Actual Performance

| n | Top-Down (calls) | Bottom-Up (iterations) |
|---|---|---|
| 10 | 19 | 9 |
| 20 | 39 | 19 |
| 30 | 59 | 29 |
| 100 | 199 | 99 |

Top-down makes ~2n calls, bottom-up does n iterations. Both O(n). Bottom-up has lower constant factor.

---

## Comparison Table

| Aspect | Top-Down (Memoization) | Bottom-Up (Tabulation) |
|---|---|---|
| **Direction** | Large → Small (recursive) | Small → Large (iterative) |
| **Coding** | Natural for recursive thinkers | Natural for iterative thinkers |
| **Cache** | Explicit (memo array/map) | Implicit (DP table) |
| **Stack overflow** | Risk for deep recursion | No risk |
| **Processing** | Only computes needed states | Computes all states |
| **Space** | O(recursion depth + cache) | O(table size) |
| **Space optimization** | Harder | Easier (rolling arrays) |
| **Debugging** | Harder (recursive calls) | Easier (linear iteration) |
| **When all states are needed** | Slightly slower | Slightly faster |
| **When few states are needed** | Much faster | Might overcompute |

### Choosing Between Them

```java
// USE TOP-DOWN when:
// 1. The recurrence is complex or non-standard ordering
// 2. Not all states are needed (sparse DP)
// 3. You're converting a backtracking solution
// 4. The problem has many unreachable states

// USE BOTTOM-UP when:
// 1. Simple, standard recurrence
// 2. All states are needed
// 3. Space optimization is important
// 4. Maximum performance is required
```

## Practical Advice

In an interview:
1. **Start with top-down** if you're more comfortable with recursion
2. **Then suggest bottom-up** for optimization
3. **Mention space optimization** possibilities

The most important thing is to get a working DP solution. Optimization can come later.
