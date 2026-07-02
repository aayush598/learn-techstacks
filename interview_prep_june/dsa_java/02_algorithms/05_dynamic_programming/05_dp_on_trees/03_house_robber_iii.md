# House Robber III — Tree Version

**Problem**: A thief can rob houses arranged as a binary tree. If a parent is robbed, its children cannot be robbed. Find the maximum money the thief can steal.

**Example**:
```
    3
   / \
  2   3
   \    \
    3    1
```
Max: 3 + 3 + 1 = 7 (rob root=3, grandchild=3, grandchild=1)

---

## State Definition

For each node, we return two values:
- `[0]` = max value if we rob THIS node (cannot rob children)
- `[1]` = max value if we do NOT rob this node (can rob children optimally)

```java
public int rob(TreeNode root) {
    int[] result = robOrNot(root);
    return Math.max(result[0], result[1]);
}

// Returns [robThisNode, notRobThisNode]
private int[] robOrNot(TreeNode node) {
    if (node == null) return new int[]{0, 0};

    int[] left = robOrNot(node.left);
    int[] right = robOrNot(node.right);

    // If we rob this node, we must skip children
    int robThis = node.val + left[1] + right[1];

    // If we don't rob this node, we can rob or skip children optimally
    int notRobThis = Math.max(left[0], left[1]) + Math.max(right[0], right[1]);

    return new int[]{robThis, notRobThis};
}
```

### Trace for [3, 2, 3, null, 3, null, 1]

```
    3
   / \
  2   3
   \    \
    3    1

Leaf 3: [3, 0]   (rob=3+0+0=3, notRob=max(3,0)=3... wait)

Let me trace carefully.

null children: [0, 0]

Node(3) [left=null, right=null]:
  left = [0, 0], right = [0, 0]
  robThis = 3 + 0 + 0 = 3
  notRobThis = max(0,0) + max(0,0) = 0
  → [3, 0]

Node(1) [left=null, right=null]:
  → [1, 0]

Node(2) [left=null, right=Node(3)]:
  left = [0, 0], right = [3, 0]
  robThis = 2 + 0 + 0 = 2
  notRobThis = max(0,0) + max(3,0) = 3
  → [2, 3]

Node(3-right) [left=null, right=Node(1)]:
  left = [0, 0], right = [1, 0]
  robThis = 3 + 0 + 0 = 3
  notRobThis = max(0,0) + max(1,0) = 1
  → [3, 1]

Root(3) [left=Node(2), right=Node(3-right)]:
  left = [2, 3], right = [3, 1]
  robThis = 3 + 3 + 1 = 7
  notRobThis = max(2,3) + max(3,1) = 3 + 3 = 6
  → [7, 6]

Answer: max(7, 6) = 7 ✓
```

---

## Why the Two Values Pattern Works

The state space for a tree node is:
1. **Rob this node** → children must be not-robbed
2. **Don't rob this node** → children can be either (we choose max)

This is a direct application of the constraint: "parent and child cannot both be robbed."

---

## Complexity

| Time | Space |
|---|---|
| O(n) | O(h) |

## Key Takeaways

1. **Two-value DP**: `[rob, notRob]` at each node
2. **rob = node.val + left.notRob + right.notRob**
3. **notRob = max(left.rob, left.notRob) + max(right.rob, right.notRob)**
4. **Postorder traversal**: children before parent
5. **Base case**: null node → [0, 0]
6. **Final answer**: max(root.rob, root.notRob)
