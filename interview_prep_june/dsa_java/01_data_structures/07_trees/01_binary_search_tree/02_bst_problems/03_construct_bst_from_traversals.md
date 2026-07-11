# Construct BST from Traversals

Given a traversal sequence, reconstruct the original BST. The BST property (left < root < right) provides strong constraints that make reconstruction possible even from a single traversal.

## TreeNode Definition

```java
public class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int val) { this.val = val; }
}
```

---

## 1. Construct BST from Preorder

Preorder: `[root, left-subtree, right-subtree]`

The first element is always the root. Each subsequent element belongs to left or right based on BST bound.

### Example

```
preorder = [8, 5, 1, 7, 10, 12]

       8
      / \
     5   10
    / \    \
   1   7    12
```

### Approach 1: Value Range (Recursive)

Maintain a global index. For each node, bound it within (min, max). If value is outside range, return null (belongs to parent's other subtree).

```java
public class BSTFromPreorder {

    private int idx = 0;

    public TreeNode bstFromPreorder(int[] preorder) {
        idx = 0;
        return build(preorder, Integer.MIN_VALUE, Integer.MAX_VALUE);
    }

    private TreeNode build(int[] preorder, int min, int max) {
        if (idx >= preorder.length) return null;

        int val = preorder[idx];
        if (val < min || val > max) return null;

        idx++;
        TreeNode node = new TreeNode(val);
        node.left = build(preorder, min, val);
        node.right = build(preorder, val, max);
        return node;
    }
}
```

**Walkthrough** for `preorder = [8, 5, 1, 7, 10, 12]`:
| Call | idx | val | range | Action |
|------|-----|-----|-------|--------|
| build(-∞,∞) | 0 | 8 | in range | root=8, idx→1 |
| build(-∞,8) | 1 | 5 | in range | left=5, idx→2 |
| build(-∞,5) | 2 | 1 | in range | left=1, idx→3 |
| build(-∞,1) | 3 | 7 | out of range | null |
| build(1,5) | 3 | 7 | out of range | null |
| build(5,8) | 3 | 7 | in range | right=7, idx→4 |
| build(5,7) | 4 | 10 | out of range | null |
| build(7,8) | 4 | 10 | out of range | null |
| build(8,∞) | 4 | 10 | in range | right=10, idx→5 |
| build(8,10) | 5 | 12 | out of range | null |
| build(10,∞) | 5 | 12 | in range | right=12, idx→6 |

### Approach 2: Iterative with Stack

Use a stack to track ancestors. The next element becomes left child of the last node if smaller; otherwise, find the parent whose right child to attach to.

```java
public class BSTFromPreorderIterative {

    public TreeNode bstFromPreorder(int[] preorder) {
        if (preorder == null || preorder.length == 0) return null;

        TreeNode root = new TreeNode(preorder[0]);
        Stack<TreeNode> stack = new Stack<>();
        stack.push(root);

        for (int i = 1; i < preorder.length; i++) {
            TreeNode node = new TreeNode(preorder[i]);

            if (preorder[i] < stack.peek().val) {
                stack.peek().left = node;
            } else {
                TreeNode parent = null;
                while (!stack.isEmpty() && stack.peek().val < preorder[i]) {
                    parent = stack.pop();
                }
                parent.right = node;
            }
            stack.push(node);
        }

        return root;
    }
}
```

### Complexity
| Approach | Time | Space |
|----------|------|-------|
| Recursive range | O(n) | O(h) |
| Iterative stack | O(n) | O(h) |

---

## 2. Construct BST from Postorder

Postorder: `[left-subtree, right-subtree, root]`

The last element is the root. Process from right to left — it's the mirror of preorder.

```java
public class BSTFromPostorder {

    private int idx;

    public TreeNode bstFromPostorder(int[] postorder) {
        idx = postorder.length - 1;
        return build(postorder, Integer.MIN_VALUE, Integer.MAX_VALUE);
    }

    private TreeNode build(int[] postorder, int min, int max) {
        if (idx < 0) return null;

        int val = postorder[idx];
        if (val < min || val > max) return null;

        idx--;
        // Build right first (right-to-left reading)
        TreeNode node = new TreeNode(val);
        node.right = build(postorder, val, max);
        node.left = build(postorder, min, val);
        return node;
    }
}
```

### Example

```
postorder = [1, 7, 5, 12, 10, 8]

Read from right: 8(root) → 10(right) → 12(right of 10) → 5(left) → 7(right of 5) → 1(left of 5)
```

Key difference from preorder: **build right subtree first** since we read the array in reverse.

---

## 3. Construct BST from Preorder and Inorder

Preorder gives root; inorder tells what's left and right of root.

For BST specifically, **inorder is just the sorted order** of unique elements. So we can derive it:

```java
public class BSTFromPreorderInorder {

    private int preIdx;
    private Map<Integer, Integer> inorderMap;

    public TreeNode buildTree(int[] preorder, int[] inorder) {
        preIdx = 0;
        inorderMap = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) {
            inorderMap.put(inorder[i], i);
        }
        return build(preorder, 0, inorder.length - 1);
    }

    private TreeNode build(int[] preorder, int left, int right) {
        if (left > right) return null;

        int rootVal = preorder[preIdx++];
        TreeNode root = new TreeNode(rootVal);
        int mid = inorderMap.get(rootVal);

        root.left = build(preorder, left, mid - 1);
        root.right = build(preorder, mid + 1, right);
        return root;
    }
}
```

### For BST Only — Derive Inorder

Since inorder of BST = sorted order of elements, we can skip passing inorder:

```java
public class BSTFromPreorderOnly {

    public TreeNode bstFromPreorder(int[] preorder) {
        int[] inorder = preorder.clone();
        Arrays.sort(inorder);
        return new BSTFromPreorderInorder().buildTree(preorder, inorder);
    }
}
```

### Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Build with given inorder | O(n) | O(n) |
| Derive inorder + build | O(n log n) | O(n) |

---

## 4. Construct BST from Level Order

Level order (BFS) processes nodes level by level. Use a queue with min/max bounds per node.

```java
import java.util.*;

public class BSTFromLevelOrder {

    static class NodeBound {
        TreeNode node;
        int min;
        int max;
        NodeBound(TreeNode node, int min, int max) {
            this.node = node;
            this.min = min;
            this.max = max;
        }
    }

    public TreeNode bstFromLevelOrder(int[] levelOrder) {
        if (levelOrder == null || levelOrder.length == 0) return null;

        TreeNode root = new TreeNode(levelOrder[0]);
        Queue<NodeBound> queue = new LinkedList<>();
        queue.offer(new NodeBound(root, Integer.MIN_VALUE, Integer.MAX_VALUE));

        int i = 1;
        while (!queue.isEmpty() && i < levelOrder.length) {
            NodeBound cur = queue.poll();

            // Try to add left child
            if (i < levelOrder.length && levelOrder[i] > cur.min && levelOrder[i] < cur.node.val) {
                TreeNode left = new TreeNode(levelOrder[i++]);
                cur.node.left = left;
                queue.offer(new NodeBound(left, cur.min, cur.node.val));
            }

            // Try to add right child
            if (i < levelOrder.length && levelOrder[i] > cur.node.val && levelOrder[i] < cur.max) {
                TreeNode right = new TreeNode(levelOrder[i++]);
                cur.node.right = right;
                queue.offer(new NodeBound(right, cur.node.val, cur.max));
            }
        }

        return root;
    }
}
```

### Example

```
levelOrder = [8, 5, 10, 1, 7, 12]
Queue: [(8, -∞, ∞)]

Process (8, -∞, ∞):
  i=1: 5 ∈ (-∞, 8) → left child of 8
  i=2: 10 ∈ (8, ∞) → right child of 8
Queue: [(5, -∞, 8), (10, 8, ∞)]

Process (5, -∞, 8):
  i=3: 1 ∈ (-∞, 5) → left child of 5
  i=4: 7 ∈ (5, 8) → right child of 5
Queue: [(10, 8, ∞), (1, -∞, 5), (7, 5, 8)]

Process (10, 8, ∞):
  i=5: 12 ∈ (10, ∞) → right child of 10
Result: correct BST constructed
```

### Complexity

| Aspect | Value |
|--------|-------|
| Time | O(n) |
| Space | O(n) for queue |

---

## 5. Sorted Array to Balanced BST

Pick middle element as root, recursively build left and right halves. This guarantees O(log n) height.

```java
public class SortedArrayToBST {

    public TreeNode sortedArrayToBST(int[] nums) {
        return build(nums, 0, nums.length - 1);
    }

    private TreeNode build(int[] nums, int left, int right) {
        if (left > right) return null;

        int mid = left + (right - left) / 2;
        TreeNode root = new TreeNode(nums[mid]);

        root.left = build(nums, left, mid - 1);
        root.right = build(nums, mid + 1, right);

        return root;
    }
}
```

### Example

```
nums = [1, 2, 3, 4, 5, 6, 7]

     4
   /   \
  2     6
 / \   / \
1   3 5   7
```

**Walkthrough**:
- mid=3 (index 3, value 4) → root
- Left subarray [1,2,3]: mid=1 (value 2) → root.left
  - Left subarray [1]: mid=0 (value 1) → 2.left
  - Right subarray [3]: mid=2 (value 3) → 2.right
- Right subarray [5,6,7]: mid=5 (value 6) → root.right
  - Left subarray [5]: mid=4 (value 5) → 6.left
  - Right subarray [7]: mid=6 (value 7) → 6.right

### Complexity

| Aspect | Value |
|--------|-------|
| Time | O(n) |
| Space | O(log n) recursion stack |

### Alternative: Sorted Linked List to BST

If input is a sorted linked list (O(n) random access not available):

```java
public class SortedListToBST {

    private ListNode head;

    public TreeNode sortedListToBST(ListNode head) {
        this.head = head;
        int size = 0;
        ListNode curr = head;
        while (curr != null) {
            size++;
            curr = curr.next;
        }
        return build(0, size - 1);
    }

    private TreeNode build(int left, int right) {
        if (left > right) return null;

        int mid = left + (right - left) / 2;

        // Build left subtree first (inorder simulation)
        TreeNode leftChild = build(left, mid - 1);

        TreeNode root = new TreeNode(head.val);
        root.left = leftChild;
        head = head.next;

        root.right = build(mid + 1, right);
        return root;
    }
}
```

This uses inorder simulation: a BST built from inorder is just consuming the list in order, which is what the algorithm above does — it constructs left, then root (consumes list), then right.

---

## Summary Table

| Problem | Input | Method | Time | Key Trick |
|---------|-------|--------|------|-----------|
| Preorder only | pre[] | Value range, recursive | O(n) | Global idx, min/max bounds |
| Preorder only | pre[] | Iterative stack | O(n) | Pop when val > stack.peek |
| Postorder only | post[] | Value range, reversed | O(n) | Read right-to-left, build right first |
| Preorder + Inorder | pre[], in[] | HashMap for indices | O(n) | Pre gives root, in gives split |
| Preorder only (BST) | pre[] | Sort to get inorder | O(n log n) | BST inorder = sorted |
| Level order | level[] | Queue with bounds | O(n) | Each node carries min/max |
| Sorted array | arr[] | Recursive mid | O(n) | Mid as root, divide halves |
| Sorted list | list | Inorder simulation | O(n) | Build left → root → right |

## Edge Cases

```java
public class EdgeCases {
    public static void main(String[] args) {
        // Empty array
        BSTFromPreorder builder = new BSTFromPreorder();
        System.out.println(builder.bstFromPreorder(new int[]{})); // null

        // Single element
        TreeNode single = builder.bstFromPreorder(new int[]{5});
        // Just root(5)

        // Skewed tree (preorder same as path)
        // preorder = [1, 2, 3]  (all right children)
        TreeNode skewed = builder.bstFromPreorder(new int[]{1, 2, 3});
        // 1 -> right(2) -> right(3)

        // Reverse skewed (all left children)
        // preorder = [3, 2, 1]
        TreeNode revSkewed = builder.bstFromPreorder(new int[]{3, 2, 1});
        // 3 -> left(2) -> left(1)

        // Negative values
        TreeNode neg = builder.bstFromPreorder(new int[]{0, -5, -10, 5});
        //    0
        //   / \
        // -5   5
        // /
        // -10

        // Balanced from sorted array
        SortedArrayToBST bst = new SortedArrayToBST();
        TreeNode balanced = bst.sortedArrayToBST(new int[]{1, 2, 3, 4, 5});
        //      3
        //     / \
        //    1   4
        //     \   \
        //      2   5
        // (multiple valid balanced BSTs exist)
    }
}
```

## Complexity Comparison

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Preorder (range) | O(n) | O(h) | Most elegant |
| Preorder (stack) | O(n) | O(h) | Iterative, no recursion depth concern |
| Postorder (range) | O(n) | O(h) | Mirror of preorder |
| Pre+Inorder | O(n) | O(n) | General binary tree approach |
| Level order | O(n) | O(n) | BFS-based |
| Sorted array | O(n) | O(log n) | Guarantees balanced height |

## Interview Tips

1. **Preorder BST construction** is the most commonly asked BST construction problem.
2. Always start with the **value range approach** — it's clean and intuitive.
3. Mention that **for BST, inorder is just sorted order**, so you don't need an inorder array.
4. For **sorted array to BST**, emphasize that choosing middle ensures balance — there are O(n) valid outputs but this gives a height-balanced one.
5. For **linked list to BST**, the inorder simulation trick avoids O(n log n) complexity from finding middle repeatedly.
