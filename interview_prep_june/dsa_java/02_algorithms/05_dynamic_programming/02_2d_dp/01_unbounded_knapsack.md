# Unbounded Knapsack

**Problem**: Given items with weight and value, each item can be used **unlimited times**. Maximize total value without exceeding capacity.

---

## Key Difference: 0/1 vs Unbounded

```
0/1 Knapsack:
  dp[i][w] = max(dp[i-1][w], dp[i-1][w-wi] + vi)
              ↑skip item     ↑take item (from prev row, not using item again)

Unbounded Knapsack:
  dp[i][w] = max(dp[i-1][w], dp[i][w-wi] + vi)
              ↑skip item     ↑take item (from CURRENT row, can reuse item)
```

**Critical difference**: In 0/1, we use `dp[i-1][w-wi]` (can't reuse). In unbounded, we use `dp[i][w-wi]` (can reuse).

---

## 2D DP Solution

```java
public int unboundedKnapsack(int[] values, int[] weights, int capacity) {
    int n = values.length;
    int[][] dp = new int[n + 1][capacity + 1];

    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= capacity; w++) {
            if (weights[i - 1] <= w) {
                // Note: dp[i][w-wi] instead of dp[i-1][w-wi]
                dp[i][w] = Math.max(dp[i - 1][w],
                                   dp[i][w - weights[i - 1]] + values[i - 1]);
            } else {
                dp[i][w] = dp[i - 1][w];
            }
        }
    }

    return dp[n][capacity];
}
```

---

## 1D DP Solution (Forward Iteration)

For unbounded knapsack, iterate capacity **forward**:

```java
public int unboundedKnapsack(int[] values, int[] weights, int capacity) {
    int[] dp = new int[capacity + 1];

    for (int i = 0; i < values.length; i++) {
        for (int w = weights[i]; w <= capacity; w++) {  // forward!
            dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }

    return dp[capacity];
}
```

### Why Forward?

Forward iteration allows using the same item multiple times:

```
Forward (CORRECT for unbounded):
  dp[10] = max(dp[10], dp[0] + 60) = 60    (take item once)
  dp[20] = max(dp[20], dp[10] + 60) = 120  (take item AGAIN!)
  dp[30] = max(dp[30], dp[20] + 60) = 180  (take item again!)
```

---

## Applications

### Coin Change II (Number of Ways)

**Problem**: Count the number of ways to make amount using unlimited coins.

```java
public int change(int amount, int[] coins) {
    int[] dp = new int[amount + 1];
    dp[0] = 1;

    for (int coin : coins) {
        for (int a = coin; a <= amount; a++) {
            dp[a] += dp[a - coin];
        }
    }

    return dp[amount];
}
```

**Critical**: Outer loop over coins (not amount) to count combinations, not permutations:
- Outer coins, inner amount → combinations (order doesn't matter) → Coin Change II
- Outer amount, inner coins → permutations (order matters) → Combination Sum IV

### Rod Cutting

```java
public int cutRod(int[] price, int n) {
    int[] dp = new int[n + 1];
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            dp[i] = Math.max(dp[i], dp[i - j] + price[j - 1]);
        }
    }
    return dp[n];
}
```

### Minimum Coins (Unbounded Minimization)

```java
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;

    for (int coin : coins) {
        for (int a = coin; a <= amount; a++) {
            dp[a] = Math.min(dp[a], dp[a - coin] + 1);
        }
    }

    return dp[amount] > amount ? -1 : dp[amount];
}
```

---

## Loop Order Matters for Counting

For minimization/maximization, loop order doesn't matter. For counting, it does:

```java
// COMBINATIONS: {1,2} and {2,1} are the same
// Outer loop over items/coins
int combinations = 0;
for (int coin : coins) {
    for (int a = coin; a <= amount; a++) {
        dp[a] += dp[a - coin];
    }
}
// dp[3] with coins=[1,2]: {1,1,1}, {1,2} → 2 ways

// PERMUTATIONS: {1,2} and {2,1} are different
// Outer loop over amount
int permutations = 0;
for (int a = 1; a <= amount; a++) {
    for (int coin : coins) {
        if (a >= coin) dp[a] += dp[a - coin];
    }
}
// dp[3] with coins=[1,2]: {1,1,1}, {1,2}, {2,1} → 3 ways
```

---

## Comparison Table

| | 0/1 Knapsack | Unbounded Knapsack |
|---|---|---|
| Item usage | Once | Unlimited |
| 1D loop direction | Backward (w--) | Forward (w++) |
| Recurrence | dp[w-wi] from prev row | dp[w-wi] from current row |
| 2D recurrence | dp[i-1][w-wi] | dp[i][w-wi] |
| Count loops | Outer item, inner backward | Outer item, inner forward |

## Template

```java
// Unbounded Knapsack template (maximization)
int unbounded(int[] values, int[] weights, int capacity) {
    int[] dp = new int[capacity + 1];
    for (int i = 0; i < values.length; i++) {
        for (int w = weights[i]; w <= capacity; w++) { // forward!
            dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }
    return dp[capacity];
}
```
