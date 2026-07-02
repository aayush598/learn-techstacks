# Maximum Path Sum (Binary Tree)

**Problem**: Given a binary tree, find the maximum path sum. A path can start and end at any node. Each node can be used at most once.

**Example**:
```
   -10
   / \
  9  20
    /  \
   15   7
```
Max path sum = 42 (15→20→7)

---

## Approach: One-Sided Max + Global Max

The key insight: for each node, we compute the maximum "one-sided" sum that can extend upward. The global maximum path might not go through the node's parent (it could stop at the node or go through both children).

```java
class Solution {
    private int maxSum = Integer.MIN_VALUE;

    public int maxPathSum(TreeNode root) {
        maxGain(root);
        return maxSum;
    }

    // Returns maximum gain from this node going in ONE direction (left OR right)
    private int maxGain(TreeNode node) {
        if (node == null) return 0;

        // Max gain from left/right subtrees (only take positive gains)
        int leftGain = Math.max(maxGain(node.left), 0);
        int rightGain = Math.max(maxGain(node.right), 0);

        // Path through this node (left + node + right)
        int pathThrough = node.val + leftGain + rightGain;
        maxSum = Math.max(maxSum, pathThrough);

        // Return max one-sided gain for parent to use
        return node.val + Math.max(leftGain, rightGain);
    }
}
```

### Trace for [-10, 9, 20, null, null, 15, 7]

```
     -10
     / \
    9   20
       /  \
      15   7

maxGain(9): leftGain=0, rightGain=0, pathThrough=9, maxSum=9, return 9
maxGain(15): leftGain=0, rightGain=0, pathThrough=15, maxSum=15, return 15
maxGain(7): leftGain=0, rightGain=0, pathThrough=7, maxSum=15, return 7
maxGain(20): leftGain=15, rightGain=7, pathThrough=20+15+7=42, maxSum=42, return 20+15=35
maxGain(-10): leftGain=9, rightGain=35, pathThrough=-10+9+35=34, maxSum=42, return -10+35=25

Answer: 42
```

### Why Take Math.max(gain, 0)?

Negative contributions only reduce the sum. By taking max(gain, 0), we effectively prune branches that hurt the total.

```
   -10
   / \
  9  20
    /  \
   15   -7

Without max(gain, 0):
  maxGain(-7) = -7 (no way to get positive)
  maxGain(20): pathThrough = 20 + 15 + (-7) = 28 (still correct)
  
  But what about this tree:
    -5
   / \
  2  -3

Without max: maxGain(-3) = -3
maxGain(-5): leftGain=2, rightGain=-3, pathThrough=-5+2-3=-6
But max path sum should be 2 (just the node 2), not -6.

With max(..., 0): rightGain = max(-3, 0) = 0
maxGain(-5): pathThrough = -5 + 2 + 0 = -3, global max = max(-3, 2) = 2 ✓
```

---

## Key Differences from Diameter

| | Diameter | Max Path Sum |
|---|---|---|
| Metric | Number of edges | Sum of node values |
| Negative values | Not applicable (edges) | Need to handle |
| Pruning | No pruning needed | Prune negative gains (max with 0) |
| Formula | leftHeight + rightHeight | node.val + leftGain + rightGain |

---

## Complexity

| Time | Space |
|---|---|
| O(n) | O(h) |

## Edge Cases

```java
// All negative values
TreeNode root = new TreeNode(-3);
// maxGain(-3): max(0,0)=0, pathThrough=-3, maxSum=-3, return max(-3,0... wait)

// Actually:
// leftGain = max(maxGain(null), 0) = max(0, 0) = 0
// rightGain = same = 0
// pathThrough = -3 + 0 + 0 = -3
// maxSum = max(INT_MIN, -3) = -3
// return -3 + 0 = -3
// Answer: -3 (the single node)

// Single node tree
TreeNode root = new TreeNode(1);
// leftGain = 0, rightGain = 0
// pathThrough = 1 + 0 + 0 = 1
// maxSum = 1
// return 1
// Answer: 1
```

## Key Takeaways

1. **Two values per node**: one-sided max gain (returned) and global max path (global variable)
2. **Prune negative gains** with `Math.max(gain, 0)`
3. **Path can start and end anywhere** — always update global max with left+node+right
4. **Return one-sided max** for parent to chain through
5. **O(n) time, O(h) space**
