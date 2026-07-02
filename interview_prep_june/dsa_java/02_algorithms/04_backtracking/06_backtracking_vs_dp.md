# Backtracking vs Dynamic Programming

Both backtracking and DP solve problems by exploring subproblems. The key difference: **backtracking explores all possibilities** while **DP avoids redundant exploration**.

---

## The Core Distinction

| | Backtracking | Dynamic Programming |
|---|---|---|
| **Approach** | Try all possibilities, prune invalid | Build optimal solutions from optimal sub-solutions |
| **Overlap** | No subproblem overlap assumed | Overlapping subproblems are essential |
| **Result** | All solutions, or first valid | Optimal value/count |
| **State space** | Full exploration space | Reduced via memoization |
| **Granularity** | Decision at each step | Subproblem at each state |

### Decision Flowchart

```
Does problem need all solutions?
    ├── Yes → Use BACKTRACKING (generate all)
    └── No → Does it have optimal substructure?
                ├── Yes → Is there overlapping subproblems?
                │           ├── Yes → Use DP
                │           └── No → Use GREEDY or DIVIDE & CONQUER
                └── No → Use BACKTRACKING (brute force)
```

---

## Key Properties

### Optimal Substructure

An optimal solution contains optimal solutions to subproblems.

```
Shortest path from A to C via B:
  If A→B→C is optimal, then A→B is optimal for getting from A to B.
  And B→C is optimal for getting from B to C.

Subset sum:
  If we can make sum = 10 using {2, 3, 5}, then we can make sum = 5 (10-5) using {2, 3}.
```

### Overlapping Subproblems

The same subproblem is solved multiple times by a naive recursive algorithm.

```
Fibonacci: fib(5) calls fib(4) and fib(3)
  fib(4) calls fib(3) and fib(2)
  fib(3) is solved twice!

Binary Search: never repeats the same subproblem
```

### Both Properties → DP

```java
// Problem: Count ways to reach amount with coins
// 1. Optimal substructure: ways(amount) = sum of ways(amount - coin)
// 2. Overlapping: ways(5) might be computed many times
// → USE DP

int[] dp = new int[amount + 1];
dp[0] = 1;
for (int a = 1; a <= amount; a++) {
    for (int coin : coins) {
        if (a >= coin) dp[a] += dp[a - coin];
    }
}
```

---

## Side-by-Side Comparisons

### Problem 1: Subset Sum

```java
// BACKTRACKING: List all subsets that sum to target
void backtrack(int[] nums, int target, int start, int sum, List<Integer> current, List<List<Integer>> result) {
    if (sum == target) {
        result.add(new ArrayList<>(current));
        return;
    }
    if (sum > target) return;
    for (int i = start; i < nums.length; i++) {
        current.add(nums[i]);
        backtrack(nums, target, i + 1, sum + nums[i], current, result);
        current.remove(current.size() - 1);
    }
}

// DP: Count subsets that sum to target (or check if possible)
boolean canPartition(int[] nums) {
    int sum = Arrays.stream(nums).sum();
    if (sum % 2 != 0) return false;
    int target = sum / 2;
    boolean[] dp = new boolean[target + 1];
    dp[0] = true;
    for (int num : nums) {
        for (int w = target; w >= num; w--) {
            if (dp[w - num]) dp[w] = true;
        }
    }
    return dp[target];
}
```

### Problem 2: Longest Increasing Subsequence

```java
// BACKTRACKING: Generate all increasing subsequences
void backtrack(int[] nums, int start, List<Integer> current, List<List<Integer>> result) {
    result.add(new ArrayList<>(current));
    for (int i = start; i < nums.length; i++) {
        if (current.isEmpty() || nums[i] > current.get(current.size() - 1)) {
            current.add(nums[i]);
            backtrack(nums, i + 1, current, result);
            current.remove(current.size() - 1);
        }
    }
}

// DP: Find length of LIS
int lengthOfLIS(int[] nums) {
    int[] dp = new int[nums.length];
    int maxLen = 0;
    for (int i = 0; i < nums.length; i++) {
        dp[i] = 1;
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i]) {
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
        maxLen = Math.max(maxLen, dp[i]);
    }
    return maxLen;
}
```

### Problem 3: Coin Change

```java
// BACKTRACKING: List all combinations
void backtrack(int[] coins, int target, int start, int sum, List<Integer> current, List<List<Integer>> result) {
    if (sum == target) {
        result.add(new ArrayList<>(current));
        return;
    }
    if (sum > target) return;
    for (int i = start; i < coins.length; i++) {
        current.add(coins[i]);
        backtrack(coins, target, i, sum + coins[i], current, result);
        current.remove(current.size() - 1);
    }
}

// DP: Minimum coins needed
int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;
    for (int a = 1; a <= amount; a++) {
        for (int coin : coins) {
            if (a >= coin) {
                dp[a] = Math.min(dp[a], 1 + dp[a - coin]);
            }
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```

---

## When to Use Each: Decision Matrix

| Problem Type | Example | Best Approach |
|---|---|---|
| "Find all ways" | Generate all subsets | Backtracking |
| "Find any way" | Word Break existence | Backtracking or DP |
| "Find the minimum/maximum" | Min coins, max profit | DP |
| "Count the number of ways" | Count subsets with sum K | DP |
| "Find all optimal solutions" | All LIS sequences | Backtracking with pruning |

### Real Examples

| LeetCode Problem | Approach | Why |
|---|---|---|
| Subsets (78) | Backtracking | Need all subsets |
| Permutations (46) | Backtracking | Need all orderings |
| Combination Sum (39) | Backtracking | Need all combos |
| N-Queens (51) | Backtracking | Need all placements |
| House Robber (198) | DP | Max profit (optimal) |
| Longest Increasing Subsequence (300) | DP | Max length (optimal) |
| Coin Change (322) | DP | Min coins (optimal) |
| Partition Equal Subset Sum (416) | DP | Check if possible (boolean, has overlap) |

---

## When Backtracking is Better Than DP

1. **Need to enumerate all solutions**, not just count/find optimal
2. **No overlapping subproblems** (every path is unique)
3. **Constraints allow pruning** that eliminates most branches
4. **N is small** (n ≤ 15 for exponential, n ≤ 30 for 2^n with pruning)

## When DP is Better Than Backtracking

1. **Overlapping subproblems** (same state reached multiple ways)
2. **Only need optimal value or count**
3. **N is large** (exponential backtracking would time out)
4. **Problem has optimal substructure**

## The Borderline Case: Backtracking + Memoization

Many problems can be solved either way:

```
Backtracking + Memoization = Top-Down DP
```

```java
// This IS backtracking WITH memoization (which makes it DP)
int solve(int[] nums, int index, int param, Integer[] memo) {
    if (index == nums.length) return baseCase(param);
    if (memo[index] != null) return memo[index];

    int include = solve(nums, index + 1, param + nums[index], memo);
    int exclude = solve(nums, index + 1, param, memo);

    memo[index] = combine(include, exclude);
    return memo[index];
}
```

## Summary One-Liner

> **Need all solutions? → Backtracking. Need optimal? → DP. Need both? → Backtracking with memoization (which IS DP).**
