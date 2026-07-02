# Coin Change — Minimum Coins

**Problem**: Given an array of coin denominations and an amount, find the minimum number of coins needed to make that amount. Return -1 if impossible.

**Example**: `coins = [1, 2, 5], amount = 11` → `3` (5 + 5 + 1)

---

## Recurrence

```
dp[a] = minimum coins needed to make amount a
dp[0] = 0
dp[a] = min(dp[a - coin] + 1) for all coin ≤ a
```

**Intuition**: To make amount `a`, pick any coin `coin`. The remaining amount is `a - coin`. We need the optimal solution for `a - coin`, plus this one coin.

---

## Bottom-Up DP

```java
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1); // "infinity" — amount+1 is greater than any possible answer
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

### Trace for coins = [1, 2, 5], amount = 11

```
dp[0] = 0  (base: 0 coins to make amount 0)

dp[1] = min(dp[1], 1+dp[0]=1, 1+dp[-1]=inf, 1+dp[-4]=inf) = 1  (coin 1)
dp[2] = min(dp[2], 1+dp[1]=2, 1+dp[0]=1, 1+dp[-3]=inf) = 1  (coin 2)
dp[3] = min(dp[3], 1+dp[2]=2, 1+dp[1]=2, 1+dp[-2]=inf) = 2  (coin 1 or 2)
dp[4] = min(dp[4], 1+dp[3]=3, 1+dp[2]=2, 1+dp[-1]=inf) = 2  (coin 2)
dp[5] = min(dp[5], 1+dp[4]=3, 1+dp[3]=3, 1+dp[0]=1)    = 1  (coin 5)
...
dp[11] = min(dp[11], 1+dp[10]=3, 1+dp[9]=4, 1+dp[6]=3) = 3  (coin 1 or 5)

Answer: 3 (5+5+1 or 5+1+5 or 1+5+5 or 11*1... all give 3)
```

---

## Top-Down DP (Memoization)

```java
public int coinChange(int[] coins, int amount) {
    Integer[] memo = new Integer[amount + 1];
    return coinChange(coins, amount, memo);
}

private int coinChange(int[] coins, int amount, Integer[] memo) {
    if (amount == 0) return 0;
    if (amount < 0) return -1;
    if (memo[amount] != null) return memo[amount];

    int min = Integer.MAX_VALUE;
    for (int coin : coins) {
        int result = coinChange(coins, amount - coin, memo);
        if (result >= 0 && result < min) {
            min = 1 + result;
        }
    }

    memo[amount] = (min == Integer.MAX_VALUE) ? -1 : min;
    return memo[amount];
}
```

---

## Understanding the DP

### State Definition

`dp[a]` = minimum coins to make amount `a`

### Transition

To compute `dp[a]`, we consider the last coin used:
- If we use coin 1: need 1 + dp[a-1] coins
- If we use coin 2: need 1 + dp[a-2] coins
- If we use coin 5: need 1 + dp[a-5] coins
- Take the minimum

### Base Case

`dp[0] = 0` — zero coins to make zero amount

### Why Initialize to `amount + 1`?

The worst case is using `amount` coins of denomination 1. So `amount + 1` is effectively "infinity" (larger than any valid answer). If dp[amount] remains > amount, it's impossible.

---

## Optimizations

### Early Break (Sorted Coins)

```java
public int coinChange(int[] coins, int amount) {
    Arrays.sort(coins);
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;

    for (int a = 1; a <= amount; a++) {
        for (int coin : coins) {
            if (coin > a) break; // coins sorted ascending
            dp[a] = Math.min(dp[a], 1 + dp[a - coin]);
        }
    }

    return dp[amount] > amount ? -1 : dp[amount];
}
```

### BFS Approach (Alternative)

```java
public int coinChange(int[] coins, int amount) {
    if (amount == 0) return 0;

    Queue<Integer> queue = new LinkedList<>();
    boolean[] visited = new boolean[amount + 1];
    queue.offer(0);
    visited[0] = true;
    int level = 0;

    while (!queue.isEmpty()) {
        int size = queue.size();
        level++;
        for (int i = 0; i < size; i++) {
            int curr = queue.poll();
            for (int coin : coins) {
                int next = curr + coin;
                if (next == amount) return level;
                if (next < amount && !visited[next]) {
                    visited[next] = true;
                    queue.offer(next);
                }
            }
        }
    }

    return -1;
}
```

BFS finds the shortest path (minimum coins) by exploring reachable amounts level by level.

---

## Reconstructing the Solution

```java
public List<Integer> coinChangePath(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    int[] lastCoin = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;

    for (int a = 1; a <= amount; a++) {
        for (int coin : coins) {
            if (a >= coin && dp[a - coin] + 1 < dp[a]) {
                dp[a] = dp[a - coin] + 1;
                lastCoin[a] = coin;
            }
        }
    }

    if (dp[amount] > amount) return new ArrayList<>();

    List<Integer> path = new ArrayList<>();
    int remaining = amount;
    while (remaining > 0) {
        path.add(lastCoin[remaining]);
        remaining -= lastCoin[remaining];
    }
    return path;
}
```

---

## Complexity

| Approach | Time | Space |
|---|---|---|
| Bottom-Up DP | O(amount * coins) | O(amount) |
| Top-Down DP | O(amount * coins) | O(amount) + recursion |
| BFS | O(amount * coins) worst | O(amount) |
| Space-optimized | Same | O(amount) — array is required |

## Key Patterns

### Unbounded Knapsack Pattern

Coin change is an **unbounded knapsack** problem:
- Each coin can be used unlimited times
- We want to minimize/maximize a value
- Inner loop iterates over all items (coins)

### Why Outer Loop Over Amount, Inner Over Coins?

```java
// Correct: counts combinations (order doesn't matter)
for (int a = 1; a <= amount; a++) {
    for (int coin : coins) {
        if (a >= coin) dp[a] = Math.min(dp[a], 1 + dp[a - coin]);
    }
}

// Also correct: same result for MIN coins
// (order of loops doesn't matter for minimization)
```

For **counting** the number of ways, loop order matters:
- Outer coins, inner amount → combinations (order doesn't matter)
- Outer amount, inner coins → permutations (order matters)

But for **minimization**, both loop orders give the same answer.

## Edge Cases

```java
// No coins, or amount is 0
coins = [2], amount = 3 → -1 (impossible)
coins = [2], amount = 0 → 0 (no coins needed)
coins = [1], amount = 0 → 0
coins = [Integer.MAX_VALUE], amount = Integer.MAX_VALUE → overflow risk!
```

## Key Takeaway

> Coin Change is the classic "minimize with unlimited items" DP. The pattern is: for each amount, try every coin, take the minimum. Always use `amount + 1` as "infinity" instead of `Integer.MAX_VALUE` to avoid overflow.
