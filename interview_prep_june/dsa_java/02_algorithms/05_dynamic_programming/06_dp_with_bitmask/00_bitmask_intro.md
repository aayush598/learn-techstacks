# DP with Bitmask Introduction

Bitmask DP is used when the state space is a subset of items (n ≤ 20). We represent subsets as bitmasks: a 32-bit integer where bit i = 1 means item i is included.

---

## Core Concept

```
Mask:  binary    decimal    subsets of {a,b,c}
      000         0         {}
      001         1         {c}
      010         2         {b}
      011         3         {b,c}
      100         4         {a}
      101         5         {a,c}
      110         6         {a,b}
      111         7         {a,b,c}
```

**dp[mask]** = optimal value for this subset

---

## Template

```java
int n = items.length;
int[] dp = new int[1 << n];
Arrays.fill(dp, INF); // or some initialization
dp[0] = 0; // empty set

for (int mask = 0; mask < (1 << n); mask++) {
    for (int i = 0; i < n; i++) {
        if ((mask & (1 << i)) == 0) { // item i not yet used
            int newMask = mask | (1 << i);
            dp[newMask] = min(dp[newMask], dp[mask] + cost);
        }
    }
}

return dp[(1 << n) - 1]; // all items used
```

---

## Key Operations

```java
int n = 5;
int allUsed = (1 << n) - 1; // 11111

// Check if item i is used
boolean used = (mask & (1 << i)) != 0;

// Add item i
int newMask = mask | (1 << i);

// Remove item i
int newMask = mask ^ (1 << i); // (if item is present)

// Count items in mask
int count = Integer.bitCount(mask);

// Iterate over unused items
for (int i = 0; i < n; i++) {
    if ((mask & (1 << i)) == 0) {
        // use item i
    }
}

// Iterate over submasks of a mask
for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {
    // sub is a non-empty subset of mask
}
```

---

## When to Use Bitmask DP

| Condition | Detail |
|---|---|
| **n ≤ 20** | 2^n states, each O(n) → ~20 million operations max |
| **Subset of items** | State is which items are used/assigned |
| **Order matters** | Need to know which items used and which is last |
| **Small constraint** | Famous problems: TSP (n ≤ 20), Assignment (n ≤ 15) |

---

## Example: Subset Sum (Find if any subset sums to target)

```java
// n ≤ 20, target any value
// O(n * 2^n) time, O(2^n) space
public boolean subsetSum(int[] nums, int target) {
    int n = nums.length;
    int[] sum = new int[1 << n];

    for (int mask = 0; mask < (1 << n); mask++) {
        if (sum[mask] == target) return true;
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) == 0) {
                int newMask = mask | (1 << i);
                sum[newMask] = sum[mask] + nums[i];
            }
        }
    }

    return false;
}
```

## Complexity

| Operation | Time | Space |
|---|---|---|
| Standard DP | O(n * 2^n) | O(2^n) |
| n = 15 | 491,520 states | 32 KB |
| n = 20 | 20,971,520 states | 4 MB |
| n = 25 | 838,860,800 states | 128 MB (too much) |

## Key Takeaways

1. **Bitmask DP is for n ≤ 20** — exponential state space
2. **Two common patterns**: dp[mask] (subset only) and dp[mask][last] (TSP style)
3. **State transition**: add one item at a time
4. **Always iterate masks in increasing order** — ensures subproblems are solved before larger sets
