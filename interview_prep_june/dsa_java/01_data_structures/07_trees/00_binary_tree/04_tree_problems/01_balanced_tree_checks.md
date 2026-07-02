# Balanced Tree Checks & Structural Comparisons

## Height-Balanced Binary Tree

A tree is height-balanced if for every node, the height difference between its left and right subtrees is at most 1.

Covered in detail in `00_height_diameter_depth.md`. Quick recap:

```java
public class HeightBalanced {
    
    // O(n) — returns -1 if unbalanced
    public static boolean isBalanced(TreeNode root) {
        return checkHeight(root) != -1;
    }
    
    private static int checkHeight(TreeNode root) {
        if (root == null) return 0;
        
        int left = checkHeight(root.left);
        if (left == -1) return -1;
        
        int right = checkHeight(root.right);
        if (right == -1) return -1;
        
        if (Math.abs(left - right) > 1) return -1;
        
        return 1 + Math.max(left, right);
    }
}
```

## Symmetric Tree (Mirror Check)

Check if a tree is a mirror of itself.

```java
public class SymmetricTree {
    
    public static boolean isSymmetric(TreeNode root) {
        if (root == null) return true;
        return isMirror(root.left, root.right);
    }
    
    private static boolean isMirror(TreeNode left, TreeNode right) {
        if (left == null && right == null) return true;
        if (left == null || right == null) return false;
        
        return (left.val == right.val) &&
               isMirror(left.left, right.right) &&
               isMirror(left.right, right.left);
    }
    
    // Iterative using queue
    public static boolean isSymmetricIterative(TreeNode root) {
        if (root == null) return true;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root.left);
        queue.offer(root.right);
        
        while (!queue.isEmpty()) {
            TreeNode left = queue.poll();
            TreeNode right = queue.poll();
            
            if (left == null && right == null) continue;
            if (left == null || right == null) return false;
            if (left.val != right.val) return false;
            
            queue.offer(left.left);
            queue.offer(right.right);
            queue.offer(left.right);
            queue.offer(right.left);
        }
        
        return true;
    }
    
    public static void main(String[] args) {
        // Symmetric tree
        //       1
        //      / \
        //     2   2
        //    / \ / \
        //   3  4 4  3
        TreeNode symmetric = new TreeNode(1);
        symmetric.left = new TreeNode(2);
        symmetric.right = new TreeNode(2);
        symmetric.left.left = new TreeNode(3);
        symmetric.left.right = new TreeNode(4);
        symmetric.right.left = new TreeNode(4);
        symmetric.right.right = new TreeNode(3);
        
        System.out.println("Symmetric: " + isSymmetric(symmetric));  // true
        
        // Asymmetric tree
        TreeNode asymmetric = new TreeNode(1);
        asymmetric.left = new TreeNode(2);
        asymmetric.right = new TreeNode(2);
        asymmetric.left.right = new TreeNode(3);
        asymmetric.right.right = new TreeNode(3);
        
        System.out.println("Asymmetric: " + isSymmetric(asymmetric));  // false
    }
}
```

## Same Tree (Structural Check)

Check if two trees are structurally identical.

```java
public class SameTree {
    
    public static boolean isSameTree(TreeNode p, TreeNode q) {
        if (p == null && q == null) return true;
        if (p == null || q == null) return false;
        if (p.val != q.val) return false;
        
        return isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
    }
    
    // Iterative using stack
    public static boolean isSameTreeIterative(TreeNode p, TreeNode q) {
        Stack<TreeNode> stack = new Stack<>();
        stack.push(p);
        stack.push(q);
        
        while (!stack.isEmpty()) {
            TreeNode first = stack.pop();
            TreeNode second = stack.pop();
            
            if (first == null && second == null) continue;
            if (first == null || second == null) return false;
            if (first.val != second.val) return false;
            
            stack.push(first.left);
            stack.push(second.left);
            stack.push(first.right);
            stack.push(second.right);
        }
        
        return true;
    }
    
    // Level order comparison
    public static boolean isSameTreeBFS(TreeNode p, TreeNode q) {
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(p);
        queue.offer(q);
        
        while (!queue.isEmpty()) {
            TreeNode first = queue.poll();
            TreeNode second = queue.poll();
            
            if (first == null && second == null) continue;
            if (first == null || second == null) return false;
            if (first.val != second.val) return false;
            
            queue.offer(first.left);
            queue.offer(second.left);
            queue.offer(first.right);
            queue.offer(second.right);
        }
        
        return true;
    }
    
    public static void main(String[] args) {
        TreeNode t1 = new TreeNode(1);
        t1.left = new TreeNode(2);
        t1.right = new TreeNode(3);
        
        TreeNode t2 = new TreeNode(1);
        t2.left = new TreeNode(2);
        t2.right = new TreeNode(3);
        
        TreeNode t3 = new TreeNode(1);
        t3.left = new TreeNode(2);
        t3.right = new TreeNode(4);
        
        System.out.println("Same: " + isSameTree(t1, t2));  // true
        System.out.println("Different: " + isSameTree(t1, t3));  // false
    }
}
```

## Subtree of Another Tree

Check if tree t is a subtree of tree s (i.e., exists a node in s whose subtree matches t).

```java
public class SubtreeCheck {
    
    public static boolean isSubtree(TreeNode s, TreeNode t) {
        if (s == null) return false;
        if (isSameTree(s, t)) return true;
        return isSubtree(s.left, t) || isSubtree(s.right, t);
    }
    
    private static boolean isSameTree(TreeNode s, TreeNode t) {
        if (s == null && t == null) return true;
        if (s == null || t == null) return false;
        if (s.val != t.val) return false;
        return isSameTree(s.left, t.left) && isSameTree(s.right, t.right);
    }
    
    // Optimized: serialize tree and use string matching
    public static boolean isSubtreeSerialization(TreeNode s, TreeNode t) {
        String sSerial = serialize(s);
        String tSerial = serialize(t);
        return sSerial.contains(tSerial);
    }
    
    private static String serialize(TreeNode root) {
        StringBuilder sb = new StringBuilder();
        serializeHelper(root, sb);
        return sb.toString();
    }
    
    private static void serializeHelper(TreeNode root, StringBuilder sb) {
        if (root == null) {
            sb.append(",#");  // Marker for null
            return;
        }
        sb.append(",").append(root.val);
        serializeHelper(root.left, sb);
        serializeHelper(root.right, sb);
    }
    
    public static void main(String[] args) {
        // Tree s:        Tree t:
        //    3             4
        //   / \           / \
        //  4   5         1   2
        // / \
        //1   2
        TreeNode s = new TreeNode(3);
        s.left = new TreeNode(4);
        s.right = new TreeNode(5);
        s.left.left = new TreeNode(1);
        s.left.right = new TreeNode(2);
        
        TreeNode t = new TreeNode(4);
        t.left = new TreeNode(1);
        t.right = new TreeNode(2);
        
        System.out.println("Is Subtree: " + isSubtree(s, t));  // true
        System.out.println("Is Subtree (serial): " + isSubtreeSerialization(s, t));  // true
    }
}
```

## Sum Tree

A SumTree is where for every node (except leaves), the node's value equals the sum of its left and right subtrees' values.

```java
public class SumTreeCheck {
    
    // Check if tree is a Sum Tree
    public static boolean isSumTree(TreeNode root) {
        if (root == null || isLeaf(root)) return true;
        
        int leftSum = sum(root.left);
        int rightSum = sum(root.right);
        
        return (root.val == leftSum + rightSum) &&
               isSumTree(root.left) &&
               isSumTree(root.right);
    }
    
    private static boolean isLeaf(TreeNode node) {
        return node != null && node.left == null && node.right == null;
    }
    
    private static int sum(TreeNode root) {
        if (root == null) return 0;
        return root.val + sum(root.left) + sum(root.right);
    }
    
    // Optimized O(n) approach
    public static boolean isSumTreeOptimized(TreeNode root) {
        return checkSumTree(root).isSum;
    }
    
    static class SumResult {
        boolean isSum;
        int sum;
        
        SumResult(boolean isSum, int sum) {
            this.isSum = isSum;
            this.sum = sum;
        }
    }
    
    private static SumResult checkSumTree(TreeNode root) {
        if (root == null) return new SumResult(true, 0);
        if (isLeaf(root)) return new SumResult(true, root.val);
        
        SumResult left = checkSumTree(root.left);
        SumResult right = checkSumTree(root.right);
        
        if (!left.isSum || !right.isSum) {
            return new SumResult(false, 0);
        }
        
        boolean isValid = (root.val == left.sum + right.sum);
        return new SumResult(isValid, root.val + left.sum + right.sum);
    }
    
    public static void main(String[] args) {
        // Valid Sum Tree:
        //      26
        //     /  \
        //    10   3
        //   / \   \
        //  4   6   3
        TreeNode sumTree = new TreeNode(26);
        sumTree.left = new TreeNode(10);
        sumTree.right = new TreeNode(3);
        sumTree.left.left = new TreeNode(4);
        sumTree.left.right = new TreeNode(6);
        sumTree.right.right = new TreeNode(3);
        
        System.out.println("Is Sum Tree: " + isSumTree(sumTree));           // true
        System.out.println("Is Sum Tree (opt): " + isSumTreeOptimized(sumTree)); // true
        
        // Invalid Sum Tree
        TreeNode invalid = new TreeNode(10);
        invalid.left = new TreeNode(5);
        invalid.right = new TreeNode(3);
        
        System.out.println("Invalid: " + isSumTree(invalid));  // false (10 != 5+3)
    }
}
```

## Flip Equivalent Binary Trees

Two trees are flip equivalent if one can be obtained by flipping left and right children of some nodes.

```java
public class FlipEquivalent {
    
    public static boolean flipEquiv(TreeNode root1, TreeNode root2) {
        if (root1 == null && root2 == null) return true;
        if (root1 == null || root2 == null) return false;
        if (root1.val != root2.val) return false;
        
        // Either not flipped (same order) or flipped
        return (flipEquiv(root1.left, root2.left) && flipEquiv(root1.right, root2.right)) ||
               (flipEquiv(root1.left, root2.right) && flipEquiv(root1.right, root2.left));
    }
    
    public static void main(String[] args) {
        TreeNode t1 = new TreeNode(1);
        t1.left = new TreeNode(2);
        t1.right = new TreeNode(3);
        t1.left.left = new TreeNode(4);
        t1.left.right = new TreeNode(5);
        
        TreeNode t2 = new TreeNode(1);
        t2.left = new TreeNode(3);
        t2.right = new TreeNode(2);
        t2.right.left = new TreeNode(5);
        t2.right.right = new TreeNode(4);
        
        System.out.println("Flip Equivalent: " + flipEquiv(t1, t2));  // true
    }
}
```

## Complete Tree Check

Verify if a binary tree is a complete binary tree.

```java
public class CompleteTreeCheck {
    
    public static boolean isCompleteTree(TreeNode root) {
        if (root == null) return true;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        boolean seenNull = false;
        
        while (!queue.isEmpty()) {
            TreeNode current = queue.poll();
            
            if (current == null) {
                seenNull = true;
            } else {
                if (seenNull) return false;  // Non-null after null → not complete
                queue.offer(current.left);
                queue.offer(current.right);
            }
        }
        
        return true;
    }
    
    // Alternative: index-based check
    public static boolean isCompleteTreeIndex(TreeNode root) {
        int totalNodes = countNodes(root);
        return checkComplete(root, 0, totalNodes);
    }
    
    private static boolean checkComplete(TreeNode root, int index, int totalNodes) {
        if (root == null) return true;
        if (index >= totalNodes) return false;
        return checkComplete(root.left, 2 * index + 1, totalNodes) &&
               checkComplete(root.right, 2 * index + 2, totalNodes);
    }
    
    private static int countNodes(TreeNode root) {
        if (root == null) return 0;
        return 1 + countNodes(root.left) + countNodes(root.right);
    }
    
    public static void main(String[] args) {
        // Complete:     Not complete:
        //    1             1
        //   / \           / \
        //  2   3         2   3
        // /             /    \
        //4             4     5
        TreeNode complete = new TreeNode(1);
        complete.left = new TreeNode(2);
        complete.right = new TreeNode(3);
        complete.left.left = new TreeNode(4);
        
        TreeNode incomplete = new TreeNode(1);
        incomplete.left = new TreeNode(2);
        incomplete.right = new TreeNode(3);
        incomplete.left.left = new TreeNode(4);
        incomplete.right.right = new TreeNode(5);
        
        System.out.println("Complete: " + isCompleteTree(complete));  // true
        System.out.println("Complete 2: " + isCompleteTree(incomplete));  // false
    }
}
```

## Full Tree Check

Check if every node has either 0 or 2 children (no node has exactly 1 child).

```java
public class FullTreeCheck {
    
    public static boolean isFullTree(TreeNode root) {
        if (root == null) return true;
        
        // Leaf
        if (root.left == null && root.right == null) return true;
        
        // Has both children
        if (root.left != null && root.right != null) {
            return isFullTree(root.left) && isFullTree(root.right);
        }
        
        // Has exactly one child
        return false;
    }
    
    public static void main(String[] args) {
        TreeNode full = new TreeNode(1);
        full.left = new TreeNode(2);
        full.right = new TreeNode(3);
        full.left.left = new TreeNode(4);
        full.left.right = new TreeNode(5);
        
        TreeNode notFull = new TreeNode(1);
        notFull.left = new TreeNode(2);
        notFull.right = new TreeNode(3);
        notFull.left.left = new TreeNode(4);  // Node 2 has only 1 child
        
        System.out.println("Full: " + isFullTree(full));  // true
        System.out.println("Not full: " + isFullTree(notFull));  // false
    }
}
```

## Complexity Summary

| Problem | Time | Space | Approach |
|---------|------|-------|---------|
| Height-Balanced | O(n) | O(h) | Postorder (return -1) |
| Symmetric Tree | O(n) | O(h) | Recursive mirror check |
| Same Tree | O(n) | O(h) | Recursive structural check |
| Subtree | O(m·n) / O(m+n) | O(h) | Recursive / Serialization |
| Sum Tree | O(n) | O(h) | Postorder with sum return |
| Flip Equivalent | O(n) | O(h) | Recursive with/without flip |
| Complete Tree | O(n) | O(w) | BFS or index check |
| Full Tree | O(n) | O(h) | Check both children |

## Practical Insights

1. **Same Tree** is the foundation for many tree comparison problems (subtree, symmetric, etc.).
2. **Serialization + string matching** can optimize subtree check to O(m+n) but may have false positives with certain serialization formats.
3. **Postorder traversal** is the natural fit for tree property checks that depend on children's properties.
4. For **complete tree** check, the null-tracking BFS approach is simpler than the index approach.
5. Many of these problems follow the pattern: **recurse on children, combine results at parent**.
