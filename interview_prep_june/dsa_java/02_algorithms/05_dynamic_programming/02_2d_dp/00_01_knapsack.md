# 0/1 Knapsack

**Problem**: Given N items, each with weight `wt[i]` and value `val[i]`, and a knapsack with capacity W, maximize the total value. Each item can be taken or left (0 or 1).

---

## Recurrence

```
dp[i][w] = maximum value using first i items with capacity w

dp[i][w] = max(
    dp[i-1][w],              // skip item i-1
    dp[i-1][w-wt[i-1]] + val[i-1]  // take item i-1 (if w >= wt[i-1])
)

Base: dp[0][w] = 0 for all w (no items → no value)
      dp[i][0] = 0 for all i (no capacity → no value)
```

---

## 2D DP Table

```java
public int knapsack(int[] values, int[] weights, int capacity) {
    int n = values.length;
    int[][] dp = new int[n + 1][capacity + 1];

    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= capacity; w++) {
            if (weights[i - 1] <= w) {
                // Either skip or take item i-1
                dp[i][w] = Math.max(dp[i - 1][w],
                                   dp[i - 1][w - weights[i - 1]] + values[i - 1]);
            } else {
                // Item too heavy, must skip
                dp[i][w] = dp[i - 1][w];
            }
        }
    }

    return dp[n][capacity];
}
```

### Trace for val = [60, 100, 120], wt = [10, 20, 30], W = 50

```
     capacity:  0   10   20   30   40   50
item 0 (none):  0    0    0    0    0    0
item 1 (w=10):  0   60   60   60   60   60
item 2 (w=20):  0   60  100  160  160  160
item 3 (w=30):  0   60  100  160  180  220
```

**Cell by cell**:
- `dp[1][10]`: item 0 (weight 10). Can take: max(0, 0+60) = 60
- `dp[2][20]`: items 0,1 (weights 10,20). Skip 2nd: 60. Take 2nd: 0+100 = 100. Max = 100
- `dp[2][30]`: skip: 60. Take 2nd: dp[1][10]+100 = 60+100 = 160. Max = 160
- `dp[3][50]`: skip: 160. Take 3rd: dp[2][20]+120 = 100+120 = 220. Max = 220

Answer: 220 (items 1 and 3: 60+120=180? No, items 2 and 3: 100+120=220 ✓)

---

## Space-Optimized 1D DP

Since `dp[i][w]` only depends on `dp[i-1][*]`, we can use a 1D array.

**Critical**: Iterate capacity **backwards** to prevent reusing the same item.

```java
public int knapsack(int[] values, int[] weights, int capacity) {
    int[] dp = new int[capacity + 1];

    for (int i = 0; i < values.length; i++) {
        // Iterate backwards to avoid using the same item multiple times
        for (int w = capacity; w >= weights[i]; w--) {
            dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }

    return dp[capacity];
}
```

### Why Iterate Backwards?

Forward iteration would use the **same item multiple times** (unbounded knapsack behavior).

```
Forward (WRONG for 0/1):
  dp[10] = max(dp[10], dp[0] + 60) = 60
  dp[20] = max(dp[20], dp[10] + 60) = 120  ← used item 0 twice!

Backward (CORRECT for 0/1):
  dp[20] = max(dp[20], dp[10] + 60) = 60   ← dp[10] is from previous iteration
  dp[10] = max(dp[10], dp[0] + 60) = 60
```

---

## Reconstructing Chosen Items

```java
public List<Integer> knapsackItems(int[] values, int[] weights, int capacity) {
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

    // Backtrack to find which items were taken
    List<Integer> taken = new ArrayList<>();
    int w = capacity;
    for (int i = n; i > 0; i--) {
        if (dp[i][w] != dp[i - 1][w]) {
            taken.add(0, i - 1); // item was taken
            w -= weights[i - 1];
        }
    }

    return taken;
}
```

---

## Applications

### Subset Sum

**Problem**: Given an array and a target sum, can we achieve exactly the target using any subset?

```java
public boolean canPartition(int[] nums) {
    int sum = 0;
    for (int num : nums) sum += num;
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

### Partition Equal Subset Sum

**Problem**: Can the array be partitioned into two subsets with equal sum?

```java
public boolean canPartition(int[] nums) {
    int total = 0;
    for (int num : nums) total += num;
    if (total % 2 != 0) return false;

    int target = total / 2;
    boolean[] dp = new boolean[target + 1];
    dp[0] = true;

    for (int num : nums) {
        for (int w = target; w >= num; w--) {
            dp[w] = dp[w] || dp[w - num];
        }
    }

    return dp[target];
}
```

### Count of Subset Sum

**Problem**: Count number of subsets that sum to target.

```java
public int countSubsets(int[] nums, int target) {
    int[] dp = new int[target + 1];
    dp[0] = 1;

    for (int num : nums) {
        for (int w = target; w >= num; w--) {
            dp[w] += dp[w - num];
        }
    }

    return dp[target];
}
```

### Ones and Zeroes

**Problem**: Given strings of 0s and 1s, find max subset with at most m 0s and n 1s.

```java
public int findMaxForm(String[] strs, int m, int n) {
    int[][] dp = new int[m + 1][n + 1];

    for (String s : strs) {
        int zeros = 0, ones = 0;
        for (char c : s.toCharArray()) {
            if (c == '0') zeros++;
            else ones++;
        }

        for (int i = m; i >= zeros; i--) {
            for (int j = n; j >= ones; j--) {
                dp[i][j] = Math.max(dp[i][j], dp[i - zeros][j - ones] + 1);
            }
        }
    }

    return dp[m][n];
}
```

---

## Complexity

| Version | Time | Space |
|---|---|---|
| 2D DP | O(N * W) | O(N * W) |
| 1D DP | O(N * W) | O(W) |

W is the capacity. If W is very large and N is small, this becomes inefficient.

---

## Key Patterns

### 0/1 Knapsack Identification

Look for:
- "Choose items with limited capacity"
- "Each item can be used at most once"
- "Maximize value / minimize cost"
- Binary decision (take or leave)

### Template

```java
// 0/1 Knapsack DP template
int solve(int[] values, int[] weights, int capacity) {
    // 1D DP, iterate capacity backwards
    int[] dp = new int[capacity + 1];

    for (int i = 0; i < values.length; i++) {
        for (int w = capacity; w >= weights[i]; w--) {
            dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }

    return dp[capacity];
}
```

### Derivative Problems

| Problem | Variation |
|---|---|
| Subset Sum | dp[w] = dp[w] \|\| dp[w - num] (boolean) |
| Partition Equal | Subset sum with target = total/2 |
| Count Subset Sum | dp[w] += dp[w - num] |
| Target Sum | Count subsets with + or - |
| Ones and Zeroes | 2D capacity (m zeros, n ones) |

## Common Mistakes

1. **Forward iteration**: Using `for (int w = 0; w <= capacity; w++)` in 1D DP turns 0/1 into unbounded
2. **Indexing**: confusing item index i with weight array index
3. **Initialization**: For maximization: dp[0] = 0. For boolean: dp[0] = true. For min: dp[0] = 0, others = INF
4. **Integer overflow**: Use long for large values
