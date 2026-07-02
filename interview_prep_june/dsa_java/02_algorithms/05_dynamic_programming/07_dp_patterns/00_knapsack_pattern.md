# Knapsack Pattern

## When to Use

Look for:
- "Choose items from a set"
- "Maximum/minimum value with limited capacity"
- "Each item can be used once" (0/1) or "unlimited" (unbounded)
- Binary decision per item

## Derivative Problems

| Problem | Type | Variation |
|---|---|---|
| Subset Sum | Boolean 0/1 | dp[w] = dp[w] \|\| dp[w-num] |
| Partition Equal | Boolean 0/1 | Target = total/2 |
| Count Subset Sum | Count 0/1 | dp[w] += dp[w-num] |
| Target Sum | Count 0/1 | Transform to subset sum |
| Ones and Zeroes | 0/1 2D | dp[m][n] for m zeros, n ones |
| Last Stone Weight II | 0/1 minimize | Partition into two sets |
| Coin Change II | Unbounded count | Outer item, inner forward |
| Coin Change (min) | Unbounded min | dp[a] = min(dp[a], dp[a-coin]+1) |

## Template

```java
// 0/1 Knapsack — Outer items, inner backward
for (int item : items) {
    for (int w = capacity; w >= item; w--) {
        dp[w] = combine(dp[w], dp[w - item]);
    }
}

// Unbounded Knapsack — Outer items, inner forward
for (int item : items) {
    for (int w = item; w <= capacity; w++) {
        dp[w] = combine(dp[w], dp[w - item]);
    }
}
```

## Key Insight

> The forward/backward loop direction determines whether items can be reused. Backward = 0/1, forward = unbounded.
