# Diameter of Binary Tree

**Problem**: Given a binary tree, find the length of the longest path between any two nodes (measured by number of edges).

**Example**:
```
    1
   / \
  2   3
 / \
4   5
```
Diameter = 3 (path: 4→2→1→3, edges=3)

---

## Approach: Height + Global Max

For each node, the diameter passing through it is `leftHeight + rightHeight`. The global diameter is the maximum of all such values.

```java
class Solution {
    private int diameter = 0;

    public int diameterOfBinaryTree(TreeNode root) {
        height(root);
        return diameter;
    }

    private int height(TreeNode node) {
        if (node == null) return 0;

        int left = height(node.left);
        int right = height(node.right);

        // Update diameter: path through this node
        diameter = Math.max(diameter, left + right);

        // Return height of this subtree
        return Math.max(left, right) + 1;
    }
}
```

### Trace

```
    1
   / \
  2   3
 / \
4   5

height(4): left=0, right=0, diam=0, return 1
height(5): left=0, right=0, diam=0, return 1
height(2): left=1, right=1, diam=max(0,2)=2, return 2
height(3): left=0, right=0, diam=2, return 1
height(1): left=2, right=1, diam=max(2,3)=3, return 3

diameter = 3
```

---

## Complexity

| Time | Space |
|---|---|
| O(n) | O(h) where h = height of tree |

## Key Takeaways

1. **Diameter = max over all nodes of (leftHeight + rightHeight)**
2. **Height function is reused** — returns subtree height, updates global diameter
3. **The diameter doesn't have to pass through root** — that's why we use a global variable
4. **O(n) time** — each node visited once
5. **O(h) space** — recursion stack
