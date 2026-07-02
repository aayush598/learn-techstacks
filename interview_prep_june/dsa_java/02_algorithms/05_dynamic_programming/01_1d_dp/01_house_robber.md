# House Robber I, II, III

---

## House Robber I — Linear Array

**Problem**: Given an array of money in houses, rob houses such that no two adjacent houses are robbed. Maximize total money.

**Recurrence**: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`

**Explanation**: At house i, either:
- Skip it: profit = dp[i-1] (best up to previous house)
- Rob it: profit = dp[i-2] + nums[i] (must skip previous house)

```java
public int rob(int[] nums) {
    if (nums.length == 0) return 0;
    if (nums.length == 1) return nums[0];

    int[] dp = new int[nums.length];
    dp[0] = nums[0];
    dp[1] = Math.max(nums[0], nums[1]);

    for (int i = 2; i < nums.length; i++) {
        dp[i] = Math.max(dp[i - 1], dp[i - 2] + nums[i]);
    }

    return dp[nums.length - 1];
}

// Space-optimized O(1)
public int rob(int[] nums) {
    int prev2 = 0, prev1 = 0;

    for (int num : nums) {
        int curr = Math.max(prev1, prev2 + num);
        prev2 = prev1;
        prev1 = curr;
    }

    return prev1;
}
```

### Trace for [2, 7, 9, 3, 1]

```
i=0: prev2=0, prev1=0, curr = max(0, 0+2)=2 → prev2=0, prev1=2
i=1: curr = max(2, 0+7)=7 → prev2=2, prev1=7
i=2: curr = max(7, 2+9)=11 → prev2=7, prev1=11
i=3: curr = max(11, 7+3)=11 → prev2=11, prev1=11
i=4: curr = max(11, 11+1)=12 → prev2=11, prev1=12

Answer: 12 (rob houses 0, 2, 4: 2+9+1=12)
```

### Why This Works

At each house, we make a binary decision: rob or skip. The optimal substructure is:

```
best[up to i] = max(best[up to i-1],   // skip house i
                     best[up to i-2] + nums[i])  // rob house i
```

---

## House Robber II — Circular Array

**Problem**: Houses are arranged in a circle (first and last are adjacent).

**Approach**: Solve two linear cases:
1. Rob houses [0, n-2] (exclude last)
2. Rob houses [1, n-1] (exclude first)
3. Take the maximum

```java
public int rob(int[] nums) {
    if (nums.length == 0) return 0;
    if (nums.length == 1) return nums[0];

    return Math.max(robLinear(nums, 0, nums.length - 2),
                    robLinear(nums, 1, nums.length - 1));
}

private int robLinear(int[] nums, int start, int end) {
    int prev2 = 0, prev1 = 0;

    for (int i = start; i <= end; i++) {
        int curr = Math.max(prev1, prev2 + nums[i]);
        prev2 = prev1;
        prev1 = curr;
    }

    return prev1;
}
```

### Trace for [2, 3, 2]

```
Case 1: rob [0,1] = [2,3]
  i=0: curr = max(0, 0+2)=2 → p2=0, p1=2
  i=1: curr = max(2, 0+3)=3 → p2=2, p1=3
  Result: 3

Case 2: rob [1,2] = [3,2]
  i=1: curr = max(0, 0+3)=3 → p2=0, p1=3
  i=2: curr = max(3, 0+2)=3 → p2=3, p1=3
  Result: 3

Answer: max(3, 3) = 3
```

### Why Two Cases?

If houses are in a circle, house 0 and house n-1 are adjacent. So:
- Either house 0 is not robbed → we can rob houses [1, n-1]
- Or house n-1 is not robbed → we can rob houses [0, n-2]

These two cases cover all possibilities without circular constraint violation.

---

## House Robber III — Binary Tree

**Problem**: Houses arranged as a binary tree. Cannot rob parent and child directly connected. Root of tree is given.

**Approach**: DFS returns two values for each node:
- `[robThis, notRobThis]`
  - `robThis` = value if we rob this node (cannot rob children)
  - `notRobThis` = value if we skip this node (can rob children optimally)

```java
public int rob(TreeNode root) {
    int[] result = dfs(root);
    return Math.max(result[0], result[1]);
}

// Returns [robThis, notRobThis]
private int[] dfs(TreeNode node) {
    if (node == null) return new int[]{0, 0};

    int[] left = dfs(node.left);
    int[] right = dfs(node.right);

    // Rob this node: must skip children
    int robThis = node.val + left[1] + right[1];

    // Don't rob this node: can rob or skip children optimally
    int notRobThis = Math.max(left[0], left[1]) + Math.max(right[0], right[1]);

    return new int[]{robThis, notRobThis};
}
```

### Trace

```
    3
   / \
  2   3
   \    \
    3    1

dfs(leaf=3): [3, 0]   (rob=3+0+0, not=0+0)
dfs(leaf=1): [1, 0]
dfs(node=2):
  left = [0, 0], right = [3, 0]
  robThis = 2 + 0 + 0 = 2
  notRobThis = max(0,0) + max(3,0) = 3
  → [2, 3]
dfs(node=3):
  left = [0, 0], right = [1, 0]
  robThis = 3 + 0 + 0 = 3
  notRobThis = max(0,0) + max(1,0) = 1
  → [3, 1]
dfs(root=3):
  left = [2, 3], right = [3, 1]
  robThis = 3 + 3 + 1 = 7  (3 + left[notRob]=3 + right[notRob]=1)
  notRobThis = max(2,3) + max(3,1) = 3 + 3 = 6
  → [7, 6]
Answer: max(7, 6) = 7
```

### Key Insight for Tree DP

```
For any node, the optimal solution is:
  either: rob node + best from grandchildren
  or:     skip node + best from children

We encode this by returning both values from DFS:
  [0] = best when THIS node IS robbed
  [1] = best when THIS node is NOT robbed
```

---

## Comparison

| Version | Structure | Approach | Time | Space |
|---|---|---|---|---|
| House Robber I | Linear array | DP, dp[i] depends on dp[i-1], dp[i-2] | O(n) | O(1) |
| House Robber II | Circular array | Two linear cases | O(n) | O(1) |
| House Robber III | Binary tree | Tree DP (postorder) | O(n) | O(h) |

## Common Variations

### House Robber with Constraint (K-apart)

```java
// Rob houses at least K apart
public int rob(int[] nums, int k) {
    int n = nums.length;
    if (n == 0) return 0;
    int[] dp = new int[n];
    for (int i = 0; i < n; i++) {
        dp[i] = nums[i];
        for (int j = 0; j <= i - k; j++) {
            dp[i] = Math.max(dp[i], dp[j] + nums[i]);
        }
        if (i > 0) dp[i] = Math.max(dp[i], dp[i - 1]);
    }
    return dp[n - 1];
}
```

### Maximum Sum of Non-Adjacent Elements

```java
// Same as House Robber I — just different problem name
public int maxNonAdjacentSum(int[] nums) {
    return rob(nums);
}
```

### With Alternating Constraints

```java
// Cannot rob 3 adjacent houses (at most 2 consecutive)
// State needs to track how many consecutive houses robbed
public int rob(int[] nums) {
    int n = nums.length;
    // dp[i][j] = max for first i houses, with j consecutive robbed ending at i
    if (n == 0) return 0;
    int[][] dp = new int[n][3];

    dp[0][0] = 0;        // didn't rob house 0
    dp[0][1] = nums[0];  // robbed house 0 (1 consecutive)
    dp[0][2] = nums[0];  // robbed house 0 (2 consecutive — same as 1 for first)

    for (int i = 1; i < n; i++) {
        dp[i][0] = Math.max(dp[i-1][0], Math.max(dp[i-1][1], dp[i-1][2]));
        dp[i][1] = dp[i-1][0] + nums[i];
        dp[i][2] = dp[i-1][1] + nums[i];
    }

    return Math.max(dp[n-1][0], Math.max(dp[n-1][1], dp[n-1][2]));
}
```

## Key Pattern

> House Robber is the quintessential "decision DP" problem. At each step, you make a choice that affects what you can do next. The state captures the consequences of the choice. For linear problems, only the previous 1-2 states matter.
