# What is Dynamic Programming?

Dynamic Programming is a method for solving complex problems by breaking them into simpler subproblems, solving each subproblem once, and storing their results.

**DP = Recursion + Memoization (Top-Down)**
**DP = Iterative Tabulation (Bottom-Up)**

---

## The Two Essential Properties

### 1. Optimal Substructure

A problem has optimal substructure if an optimal solution can be constructed from optimal solutions of its subproblems.

```
Example: Shortest Path
- Shortest path from A to C via B = shortest path from A to B + shortest path from B to C
- The optimal solution to A→C contains optimal solutions to A→B and B→C

Non-example: Longest Simple Path
- Longest path between two nodes may not contain longest paths between intermediate nodes
```

### 2. Overlapping Subproblems

The same subproblems are solved multiple times when using a naive recursive approach.

```
Example: Fibonacci
- fib(5) = fib(4) + fib(3)
- fib(4) = fib(3) + fib(2)
  → fib(3) is computed twice

Non-example: Binary Search
- Binary search in [0, n] → search in [0, mid] or [mid, n] — never both
- No overlap
```

### Both Properties Together

```
Optimal substructure → problem can be solved via subproblems
Overlapping subproblems → solving subproblems once saves time
Both → DP is applicable and efficient
```

---

## Identifying DP Problems

### Common Keywords

| Phrase | Likely DP |
|---|---|
| "Count the number of ways..." | ✅ DP |
| "Minimum/maximum..." | ✅ DP (or greedy) |
| "Find the longest/shortest..." | ✅ DP |
| "Is it possible to..." | ✅ DP (boolean) |
| "Number of ways to reach..." | ✅ DP |
| "Find all..." | ❌ Backtracking |

### The DP Checklist

```
1. Can the problem be broken into overlapping subproblems?
2. Can you define a recurrence relation?
3. Does the problem ask for optimal value or count?
4. Is brute force exponential?

If yes to 3+ of these → use DP
```

---

## State Definition

**State**: What does dp[i] (or dp[i][j]) represent?

This is the most important step. A good state definition makes DP easy; a bad one makes it impossible.

### Examples

```java
// Fibonacci: what is the i-th Fibonacci number?
int fib(int n) {
    // dp[i] = i-th Fibonacci number
    int[] dp = new int[n + 1];
    dp[0] = 0; dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}

// Climbing Stairs: how many ways to reach step i?
int climbStairs(int n) {
    // dp[i] = number of ways to reach step i
    int[] dp = new int[n + 1];
    dp[0] = 1; dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}

// 0/1 Knapsack: max value using first i items with weight w
int knapsack(int[] values, int[] weights, int capacity) {
    // dp[i][w] = max value using first i items with capacity w
    int n = values.length;
    int[][] dp = new int[n + 1][capacity + 1];
    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= capacity; w++) {
            if (weights[i - 1] <= w) {
                dp[i][w] = Math.max(dp[i - 1][w],
                                   dp[i - 1][w - weights[i - 1]] + values[i - 1]);
            } else {
                dp[i][w] = dp[i - 1][w];
            }
        }
    }
    return dp[n][capacity];
}
```

### Good State Definitions

A good state:
1. **Completely describes the subproblem** — no missing information
2. **Has clear base cases** — dp[0], dp[i][0], dp[0][j], etc.
3. **Has a recurrence** — can compute dp[i] from earlier states
4. **Captures the answer** — dp[n] or dp[n][m] or max(dp[...])

---

## Transition: The Recurrence Relation

The transition tells us how to compute dp[i] from smaller states.

```
General form:
  dp[i] = combine(dp[prev1], dp[prev2], ...)

Examples:
  Fibonacci:      dp[i] = dp[i-1] + dp[i-2]
  House Robber:   dp[i] = max(dp[i-1], dp[i-2] + nums[i])
  LIS:            dp[i] = 1 + max(dp[j]) for all j < i with arr[j] < arr[i]
  LCS:            dp[i][j] = (match ? dp[i-1][j-1]+1 : max(dp[i-1][j], dp[i][j-1]))
```

### Finding the Right Transition

```
Step 1: Define the state
  "dp[i] = answer for input of size i"

Step 2: Think about the last decision
  "If I know the answer for smaller sizes, how does the last element change things?"

Step 3: Write the recurrence
  dp[i] = function of dp[smaller values]
```

---

## Top-Down (Memoization) vs Bottom-Up (Tabulation)

| Aspect | Top-Down | Bottom-Up |
|---|---|---|
| Approach | Recursive + cache | Iterative, fill table |
| Thinking | Start from problem, go down to base | Start from base, build up |
| Code | More intuitive | More efficient |
| Speed | Slightly slower (recursion overhead) | Faster (no recursion) |
| Space | O(n) recursion stack + O(n) cache | O(n) table (can optimize) |
| Debugging | Easier | Can be tricky |
| When to use | Complex recurrences, need only some states | Simple recurrences, need all states |

### Top-Down Example

```java
int fib(int n, int[] memo) {
    if (n <= 1) return n;
    if (memo[n] != 0) return memo[n];
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo);
    return memo[n];
}
```

### Bottom-Up Example

```java
int fib(int n) {
    if (n <= 1) return n;
    int[] dp = new int[n + 1];
    dp[0] = 0; dp[1] = 1;
    for (int i = 2; i <= n; i++)
        dp[i] = dp[i - 1] + dp[i - 2];
    return dp[n];
}
```

---

## The DP Framework

When solving any DP problem, follow these steps:

```
1. Define the STATE
   - What does dp[...] represent?

2. Identify BASE CASES
   - What are the simplest inputs?

3. Write the TRANSITION / RECURRENCE
   - How does dp[i] relate to earlier values?

4. Determine the ANSWER
   - Where is the final answer in the DP table?

5. OPTIMIZE (optional)
   - Can space be reduced? Can order be changed?
```

### Example: Min Cost Climbing Stairs

```java
// Problem: Each step has a cost, you can climb 1 or 2 steps.
// Find min cost to reach the top.

// Step 1: STATE
// dp[i] = minimum cost to reach step i

// Step 2: BASE CASES
// dp[0] = cost[0] (first step)
// dp[1] = cost[1] (second step)

// Step 3: TRANSITION
// dp[i] = cost[i] + min(dp[i-1], dp[i-2])
// (pay cost at step i, then add min of arriving from i-1 or i-2)

// Step 4: ANSWER
// min(dp[n-1], dp[n-2]) — can end at either of the last two steps

public int minCostClimbingStairs(int[] cost) {
    int n = cost.length;
    int[] dp = new int[n];
    dp[0] = cost[0];
    dp[1] = cost[1];
    for (int i = 2; i < n; i++) {
        dp[i] = cost[i] + Math.min(dp[i - 1], dp[i - 2]);
    }
    return Math.min(dp[n - 1], dp[n - 2]);
}
```

---

## Common DP Categories

| Category | State | Example |
|---|---|---|
| 1D DP | dp[i] | Fibonacci, House Robber |
| 2D DP | dp[i][j] | LCS, Knapsack, Edit Distance |
| Grid DP | dp[i][j] | Unique Paths, Min Path Sum |
| Tree DP | dfs returns value | Diameter, Max Path Sum |
| Bitmask DP | dp[mask] | TSP, Assignment |
| Interval DP | dp[i][j] for i..j | MCM, Burst Balloons |
| Digit DP | dp[pos][tight][state] | Count numbers with property |

## Key Takeaway

> DP is about recognizing that the same subproblems appear repeatedly and caching their results. The art is in defining states and transitions that capture the problem's structure.
