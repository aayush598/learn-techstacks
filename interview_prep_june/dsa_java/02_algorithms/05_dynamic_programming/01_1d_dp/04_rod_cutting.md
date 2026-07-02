# Rod Cutting

**Problem**: Given a rod of length n, and a price array `price[i]` for a rod of length i+1 (1-indexed), find the maximum profit by cutting the rod into pieces and selling them.

**Example**: `price = [1, 5, 8, 9, 10, 17, 17, 20]`, `n = 8` → max profit = 22 (cut into 2+6: 5+17)

---

## Recurrence

```
dp[i] = maximum profit for rod of length i
dp[0] = 0 (no rod, no profit)
dp[i] = max(price[j-1] + dp[i - j]) for all j = 1 to i
```

**Intuition**: For a rod of length i, try cutting a piece of length j (1 ≤ j ≤ i) and sell it, then optimally cut the remaining rod of length i-j.

---

## Bottom-Up DP

```java
public int cutRod(int[] price, int n) {
    int[] dp = new int[n + 1];
    dp[0] = 0;

    for (int i = 1; i <= n; i++) {
        int maxProfit = Integer.MIN_VALUE;
        for (int j = 1; j <= i; j++) {
            // cut off piece of length j, sell it, recurse on i-j
            maxProfit = Math.max(maxProfit, price[j - 1] + dp[i - j]);
        }
        dp[i] = maxProfit;
    }

    return dp[n];
}
```

### Trace for price = [1, 5, 8, 9, 10, 17, 17, 20], n = 8

```
dp[0] = 0

dp[1] = max(price[0]+dp[0]=1) = 1

dp[2] = max(price[0]+dp[1]=1+1=2, price[1]+dp[0]=5+0=5) = 5

dp[3] = max(price[0]+dp[2]=1+5=6, price[1]+dp[1]=5+1=6, price[2]+dp[0]=8+0=8) = 8

dp[4] = max(1+8=9, 5+5=10, 8+1=9, 9+0=9) = 10

dp[5] = max(1+10=11, 5+8=13, 8+5=13, 9+1=10, 10+0=10) = 13

dp[6] = max(1+13=14, 5+10=15, 8+8=16, 9+5=14, 10+1=11, 17+0=17) = 17

dp[7] = max(1+17=18, 5+13=18, 8+10=18, 9+8=17, 10+5=15, 17+1=18, 17+0=17) = 18

dp[8] = max(1+18=19, 5+17=22, 8+13=21, 9+10=19, 10+8=18, 17+5=22, 17+1=18, 20+0=20) = 22
```

Answer: 22 (cut into pieces of length 2 and 6)

---

## Reconstructing the Cuts

```java
public List<Integer> cutRodPath(int[] price, int n) {
    int[] dp = new int[n + 1];
    int[] cut = new int[n + 1]; // stores the length of first cut

    dp[0] = 0;
    for (int i = 1; i <= n; i++) {
        int maxProfit = Integer.MIN_VALUE;
        for (int j = 1; j <= i; j++) {
            if (price[j - 1] + dp[i - j] > maxProfit) {
                maxProfit = price[j - 1] + dp[i - j];
                cut[i] = j; // first cut of length j
            }
        }
        dp[i] = maxProfit;
    }

    // Reconstruct
    List<Integer> cuts = new ArrayList<>();
    int remaining = n;
    while (remaining > 0) {
        cuts.add(cut[remaining]);
        remaining -= cut[remaining];
    }
    return cuts;
}
```

---

## Relationship to Unbounded Knapsack

Rod cutting is identical to unbounded knapsack:

```
Unbounded Knapsack:
  - "Items" with weight = length and value = price
  - "Capacity" = rod length n
  - Each item can be used unlimited times
  - Maximize value

Rod Cutting:
  - dp[i] = max profit for rod length i
  - dp[i] = max(dp[i], dp[i-j] + price[j-1]) for each possible cut length j
```

```java
// Unbounded knapsack formulation
public int cutRod(int[] price, int n) {
    int[] dp = new int[n + 1];

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            if (j <= i) {
                dp[i] = Math.max(dp[i], dp[i - j] + price[j - 1]);
            }
        }
    }

    return dp[n];
}
```

---

## Comparison: Rod Cutting vs Coin Change

| Aspect | Rod Cutting | Coin Change (Min Coins) |
|---|---|---|
| Item usage | Unlimited | Unlimited |
| Goal | Maximize profit | Minimize coins |
| DP direction | dp[i] = max(dp[i-j] + price[j-1]) | dp[i] = min(dp[i-coin] + 1) |
| Initialization | dp[0] = 0 | dp[0] = 0, dp[i] = INF |
| Loop order | Outer: length, Inner: cut size | Outer: amount, Inner: coin |

---

## Cost of Cutting

If each cut has a cost `C`:

```java
public int cutRodWithCost(int[] price, int n, int cutCost) {
    int[] dp = new int[n + 1];

    for (int i = 1; i <= n; i++) {
        // Option 1: sell as whole piece
        dp[i] = price[i - 1];
        // Option 2: cut at some position
        for (int j = 1; j < i; j++) {
            dp[i] = Math.max(dp[i], price[j - 1] + dp[i - j] - cutCost);
        }
    }

    return dp[n];
}
```

---

## Alternative: Top-Down

```java
public int cutRod(int[] price, int n) {
    Integer[] memo = new Integer[n + 1];
    return cutRodMemo(price, n, memo);
}

private int cutRodMemo(int[] price, int n, Integer[] memo) {
    if (n == 0) return 0;
    if (memo[n] != null) return memo[n];

    int maxProfit = Integer.MIN_VALUE;
    for (int j = 1; j <= n; j++) {
        maxProfit = Math.max(maxProfit, price[j - 1] + cutRodMemo(price, n - j, memo));
    }

    memo[n] = maxProfit;
    return maxProfit;
}
```

---

## Complexity

| Approach | Time | Space |
|---|---|---|
| Bottom-up | O(n²) | O(n) |
| Top-down | O(n²) | O(n) + recursion |

## Key Takeaways

1. **Rod cutting = Unbounded Knapsack** — both allow unlimited use of items
2. **The recurrence checks every possible first cut** — for length i, try cut of every size j from 1 to i
3. **Reconstruction** uses a separate array to track which cut was optimal
4. **Cost of cutting** can be added by subtracting from profit
5. **Initialization** for maximization: `dp[0] = 0` (minimum value)
