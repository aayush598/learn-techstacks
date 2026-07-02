# LCA in BST

## Problem Statement
Given a BST and two nodes p and q, find their Lowest Common Ancestor.

## Why LCA in BST is Simpler

In a BST, node ordering tells you which subtree to search:
- If both values are **less** than root → LCA is in **left subtree**
- If both values are **greater** than root → LCA is in **right subtree**
- Otherwise (one less, one greater, or one equals root) → **current root is LCA**

## Recursive Approach

```java
public class LCAInBST {
    
    // Recursive: O(h) time, O(h) space
    public static TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null) return null;
        
        // Both in left subtree
        if (p.val < root.val && q.val < root.val) {
            return lowestCommonAncestor(root.left, p, q);
        }
        // Both in right subtree
        if (p.val > root.val && q.val > root.val) {
            return lowestCommonAncestor(root.right, p, q);
        }
        // Current node is the LCA
        return root;
    }
    
    public static void main(String[] args) {
        //       6
        //      / \
        //     2   8
        //    / \ / \
        //   0  4 7 9
        //     / \
        //    3   5
        TreeNode root = new TreeNode(6);
        root.left = new TreeNode(2);
        root.right = new TreeNode(8);
        root.left.left = new TreeNode(0);
        root.left.right = new TreeNode(4);
        root.right.left = new TreeNode(7);
        root.right.right = new TreeNode(9);
        root.left.right.left = new TreeNode(3);
        root.left.right.right = new TreeNode(5);
        
        System.out.println("LCA of 2 and 8: " + 
            lowestCommonAncestor(root, root.left, root.right).val);                    // 6
        System.out.println("LCA of 0 and 5: " + 
            lowestCommonAncestor(root, root.left.left, root.left.right.right).val);    // 2
        System.out.println("LCA of 2 and 4: " + 
            lowestCommonAncestor(root, root.left, root.left.right).val);              // 2
        System.out.println("LCA of 3 and 5: " + 
            lowestCommonAncestor(root, root.left.right.left, root.left.right.right).val); // 4
    }
}
```

## Iterative Approach (Optimal)

```java
public class LCAInBSTIterative {
    
    // Iterative: O(h) time, O(1) space
    public static TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        TreeNode current = root;
        
        while (current != null) {
            if (p.val < current.val && q.val < current.val) {
                current = current.left;
            } else if (p.val > current.val && q.val > current.val) {
                current = current.right;
            } else {
                return current;
            }
        }
        
        return null;
    }
    
    // Generic version (works even if p or q don't exist in tree)
    public static TreeNode lowestCommonAncestorSafe(TreeNode root, TreeNode p, TreeNode q) {
        if (!exists(root, p) || !exists(root, q)) return null;
        
        TreeNode current = root;
        while (current != null) {
            if (p.val < current.val && q.val < current.val) {
                current = current.left;
            } else if (p.val > current.val && q.val > current.val) {
                current = current.right;
            } else {
                return current;
            }
        }
        return null;
    }
    
    private static boolean exists(TreeNode root, TreeNode target) {
        if (root == null) return false;
        if (root == target) return true;
        if (target.val < root.val) return exists(root.left, target);
        return exists(root.right, target);
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(6);
        root.left = new TreeNode(2);
        root.right = new TreeNode(8);
        root.left.left = new TreeNode(0);
        root.left.right = new TreeNode(4);
        
        TreeNode p = root.left;     // 2
        TreeNode q = root.left.right; // 4
        
        System.out.println("LCA of 2 and 4: " + lowestCommonAncestor(root, p, q).val);  // 2
    }
}
```

## LCA in BST with Values Only (No Node References)

```java
public class LCAWithValues {
    
    // Find LCA by values only (nodes might not exist)
    public static int lowestCommonAncestor(TreeNode root, int p, int q) {
        TreeNode current = root;
        
        while (current != null) {
            if (p < current.val && q < current.val) {
                current = current.left;
            } else if (p > current.val && q > current.val) {
                current = current.right;
            } else {
                return current.val;
            }
        }
        
        return -1;  // Not found
    }
    
    // Alternative: find LCA and also check if both values exist
    public static int lowestCommonAncestorSafe(TreeNode root, int p, int q) {
        if (!search(root, p) || !search(root, q)) return -1;
        return lowestCommonAncestor(root, p, q);
    }
    
    private static boolean search(TreeNode root, int val) {
        TreeNode current = root;
        while (current != null) {
            if (current.val == val) return true;
            if (val < current.val) current = current.left;
            else current = current.right;
        }
        return false;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(6);
        root.left = new TreeNode(2);
        root.right = new TreeNode(8);
        root.left.left = new TreeNode(0);
        root.left.right = new TreeNode(4);
        
        System.out.println("LCA of 2 and 8: " + lowestCommonAncestor(root, 2, 8));  // 6
        System.out.println("LCA of 0 and 4: " + lowestCommonAncestor(root, 0, 4));  // 2
        System.out.println("LCA of 2 and 4: " + lowestCommonAncestor(root, 2, 4));  // 2
        System.out.println("LCA of 5 and 8: " + lowestCommonAncestor(root, 5, 8));  // 6 (5 not in tree)
    }
}
```

## LCA in BST with Distance

```java
public class LCADistanceBST {
    
    // Find distance between two nodes in BST
    public static int distance(TreeNode root, int p, int q) {
        TreeNode lca = lowestCommonAncestor(root, p, q);
        if (lca == null) return -1;
        return distFromNode(lca, p) + distFromNode(lca, q);
    }
    
    private static TreeNode lowestCommonAncestor(TreeNode root, int p, int q) {
        TreeNode current = root;
        while (current != null) {
            if (p < current.val && q < current.val) current = current.left;
            else if (p > current.val && q > current.val) current = current.right;
            else return current;
        }
        return null;
    }
    
    private static int distFromNode(TreeNode root, int target) {
        int dist = 0;
        TreeNode current = root;
        
        while (current != null) {
            if (current.val == target) return dist;
            if (target < current.val) current = current.left;
            else current = current.right;
            dist++;
        }
        
        return -1;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(6);
        root.left = new TreeNode(2);
        root.right = new TreeNode(8);
        root.left.left = new TreeNode(0);
        root.left.right = new TreeNode(4);
        root.left.right.left = new TreeNode(3);
        root.left.right.right = new TreeNode(5);
        
        System.out.println("Distance between 0 and 5: " + distance(root, 0, 5));  // 4 (0-2-4-5)
        System.out.println("Distance between 2 and 8: " + distance(root, 2, 8));  // 3 (2-6-8)
    }
}
```

## LCA in BST — Edge Cases

```java
public class LCAEdgeCases {
    
    public static void testCases() {
        // Test 1: Normal BST
        TreeNode root = new TreeNode(6);
        root.left = new TreeNode(2);
        root.right = new TreeNode(8);
        root.left.left = new TreeNode(0);
        root.left.right = new TreeNode(4);
        
        // Test 2: p and q on same side
        System.out.println("Both left: " + lowestCommonAncestor(root, 0, 4).val);  // 2
        
        // Test 3: One is ancestor of the other
        System.out.println("p is ancestor: " + lowestCommonAncestor(root, 2, 4).val);  // 2
        
        // Test 4: p equals q
        System.out.println("p == q: " + lowestCommonAncestor(root, 4, 4).val);  // 4
        
        // Test 5: Root is LCA
        System.out.println("Root is LCA: " + lowestCommonAncestor(root, 2, 8).val);  // 6
        
        // Test 6: Skewed tree
        TreeNode skewed = new TreeNode(1);
        skewed.right = new TreeNode(2);
        skewed.right.right = new TreeNode(3);
        skewed.right.right.right = new TreeNode(4);
        
        System.out.println("Skewed LCA (2, 4): " + 
            lowestCommonAncestor(skewed, skewed.right, skewed.right.right.right).val);  // 2
    }
    
    public static TreeNode lowestCommonAncestor(TreeNode root, int p, int q) {
        TreeNode current = root;
        while (current != null) {
            if (p < current.val && q < current.val) current = current.left;
            else if (p > current.val && q > current.val) current = current.right;
            else return current;
        }
        return null;
    }
    
    public static void main(String[] args) {
        testCases();
    }
}
```

## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Recursive | O(h) | O(h) | Simpler, function call overhead |
| Iterative | O(h) | O(1) | Optimal for BST |
| With value search | O(h) | O(1) | Safe version |

## Comparison: Binary Tree LCA vs BST LCA

| Aspect | Binary Tree LCA | BST LCA |
|--------|----------------|---------|
| Time | O(n) | O(h) |
| Space | O(h) | O(1) |
| Logic | Recursively check left/right for nodes | Compare values with root |
| Complexity | More complex | Trivially simple |
| Key insight | LCA is where left and right both return non-null | LCA is where values split around root |

## Practical Insights

1. **BST LCA is one of the simplest tree problems** — if you understand BST property, the solution is immediate.
2. The **iterative solution** is O(1) space and is the best answer in interviews.
3. The same idea extends: once you know the values, you can find LCA without even having node references (just values).
4. For **distance between nodes** in BST, find LCA first, then sum distances from LCA to each node.
5. Be careful with **non-existent nodes** — verify that nodes exist before computing LCA.
