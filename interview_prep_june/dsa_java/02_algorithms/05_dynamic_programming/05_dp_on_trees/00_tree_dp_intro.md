# Tree DP Introduction

Tree DP uses **postorder traversal** to compute values for a node based on its children's values. The DFS returns the DP value(s) for the subtree rooted at that node.

---

## Core Pattern

```java
// Tree DP template
Result dfs(TreeNode node) {
    if (node == null) return baseCase;

    Result left = dfs(node.left);
    Result right = dfs(node.right);

    // Combine children's results with current node
    Result current = combine(node, left, right);

    return current;
}
```

**Key insight**: Process children first (postorder), then compute parent's value.

---

## Why Postorder?

In a tree, a node's optimal solution depends on its children's optimal solutions. Postorder traversal ensures children are processed before parents.

```
Preorder:   node → left → right  (parent before children)
Inorder:    left → node → right  (used for BST)
Postorder:  left → right → node  (children before parent) ← DP
```

---

## State Definition for Tree DP

Unlike array DP (where state is `dp[i]` for position i), tree DP state is more nuanced:

**Common state types:**

1. **Single value**: `int dfs(node)` returns the result for the subtree
2. **Two values**: `int[] dfs(node)` returns a pair (e.g., [include, exclude])
3. **Global variable**: Update a global during traversal (e.g., diameter)

### Single Value Pattern

```java
// Returns the optimal value for the subtree
int dfs(TreeNode node) {
    if (node == null) return 0;
    int left = dfs(node.left);
    int right = dfs(node.right);
    return compute(node.val, left, right);
}
```

Used for: max path sum (that goes through node in one direction), height, etc.

### Multiple Values Pattern

```java
// Returns multiple DP values for the subtree
int[] dfs(TreeNode node) {
    if (node == null) return new int[]{0, 0};
    int[] left = dfs(node.left);
    int[] right = dfs(node.right);
    int include = node.val + left[1] + right[1];
    int exclude = max(left) + max(right);
    return new int[]{include, exclude};
}
```

Used for: House Robber III, tree coloring, tree matching.

### Global Variable Pattern

```java
int globalMax = 0;

int dfs(TreeNode node) {
    if (node == null) return 0;
    int left = dfs(node.left);
    int right = dfs(node.right);
    globalMax = Math.max(globalMax, left + right + node.val);
    return node.val + Math.max(left, right);
}
```

Used for: diameter, maximum path sum (any node to any node).

---

## Common Tree DP Problems

| Problem | Return Type | Global Var? |
|---|---|---|
| Height/Depth | int | No |
| Diameter | int (height) | Yes (update diameter) |
| Max Path Sum | int (max one-sided) | Yes (update max) |
| House Robber III | int[2] {rob, notRob} | No |
| Balanced Binary Tree | boolean (or int) | No |
| Largest BST Subtree | int[4] {size,min,max,isBST} | Yes |

---

## Template Examples

### Single Value: Height

```java
public int height(TreeNode root) {
    if (root == null) return 0;
    int left = height(root.left);
    int right = height(root.right);
    return Math.max(left, right) + 1;
}
```

### Two Values: House Robber III

```java
public int rob(TreeNode root) {
    int[] result = dfs(root);
    return Math.max(result[0], result[1]);
}

private int[] dfs(TreeNode node) {
    if (node == null) return new int[]{0, 0};
    int[] left = dfs(node.left);
    int[] right = dfs(node.right);
    int rob = node.val + left[1] + right[1];
    int notRob = Math.max(left[0], left[1]) + Math.max(right[0], right[1]);
    return new int[]{rob, notRob};
}
```

### Global Variable: Diameter

```java
int diameter = 0;

public int diameterOfBinaryTree(TreeNode root) {
    height(root);
    return diameter;
}

private int height(TreeNode node) {
    if (node == null) return 0;
    int left = height(node.left);
    int right = height(node.right);
    diameter = Math.max(diameter, left + right);
    return Math.max(left, right) + 1;
}
```

---

## Complexity

| Aspect | Value |
|---|---|
| Time | O(n) — visit each node once |
| Space | O(h) — recursion stack, h = height of tree |

## Key Takeaways

1. **Always process children first** (postorder traversal)
2. **Define clear return values** — what does your DFS represent for a subtree?
3. **Use global variables** for values that span across nodes (diameter, max sum)
4. **Use arrays/tuples** when a node has multiple DP states (rob/not-rob, include/exclude)
5. **Base case is always null → identity value** (0, min, max, etc.)
6. **Tree DP is O(n) time** — visit each node exactly once
