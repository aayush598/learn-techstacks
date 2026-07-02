# Validate Binary Search Tree

## Problem Statement
Given the root of a binary tree, determine if it is a valid BST.

## The Common Mistake

```java
// WRONG APPROACH: Only checking immediate children
public boolean isValidBST_WRONG(TreeNode root) {
    if (root == null) return true;
    
    if (root.left != null && root.left.val >= root.val) return false;
    if (root.right != null && root.right.val <= root.val) return false;
    
    return isValidBST_WRONG(root.left) && isValidBST_WRONG(root.right);
}
```

**Why this is wrong**: A BST requires that ALL values in the left subtree are less than root, not just the immediate left child.

Counterexample:
```
    5
   / \
  1   6
     / \
    4   7
```
This tree is NOT a valid BST (4 is in the right subtree of 5 but 4 < 5). The wrong approach would return `true`.

## Approach 1: Range-Based Recursive Check (Optimal)

Each node must be within a valid range [min, max].

```java
public class ValidateBST {
    
    public static boolean isValidBST(TreeNode root) {
        return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }
    
    private static boolean validate(TreeNode root, long min, long max) {
        if (root == null) return true;
        
        // Current node must be within range
        if (root.val <= min || root.val >= max) {
            return false;
        }
        
        // Left subtree: values must be < root.val (max = root.val)
        // Right subtree: values must be > root.val (min = root.val)
        return validate(root.left, min, root.val) &&
               validate(root.right, root.val, max);
    }
    
    public static void main(String[] args) {
        // Valid BST
        TreeNode valid = new TreeNode(5);
        valid.left = new TreeNode(3);
        valid.right = new TreeNode(7);
        valid.left.left = new TreeNode(2);
        valid.left.right = new TreeNode(4);
        valid.right.right = new TreeNode(8);
        
        System.out.println("Valid BST: " + isValidBST(valid));  // true
        
        // Invalid BST (4 is in wrong position)
        TreeNode invalid = new TreeNode(5);
        invalid.left = new TreeNode(3);
        invalid.right = new TreeNode(7);
        invalid.left.left = new TreeNode(2);
        invalid.left.right = new TreeNode(6);  // 6 > 5, but in left subtree!
        invalid.right.right = new TreeNode(8);
        
        System.out.println("Invalid BST: " + isValidBST(invalid));  // false
    }
}
```

## Approach 2: Inorder Traversal + Check Sorted

Inorder of a BST must be strictly increasing.

```java
public class ValidateBSTInorder {
    
    // Method 1: Collect inorder in list, check sorted
    public static boolean isValidBSTList(TreeNode root) {
        List<Integer> inorder = new ArrayList<>();
        inorderCollect(root, inorder);
        
        for (int i = 1; i < inorder.size(); i++) {
            if (inorder.get(i) <= inorder.get(i - 1)) {
                return false;
            }
        }
        return true;
    }
    
    private static void inorderCollect(TreeNode root, List<Integer> result) {
        if (root == null) return;
        inorderCollect(root.left, result);
        result.add(root.val);
        inorderCollect(root.right, result);
    }
    
    // Method 2: Track previous node (more efficient, no extra list)
    private static TreeNode prev = null;
    
    public static boolean isValidBSTInorder(TreeNode root) {
        prev = null;
        return inorderCheck(root);
    }
    
    private static boolean inorderCheck(TreeNode root) {
        if (root == null) return true;
        
        if (!inorderCheck(root.left)) return false;
        
        // Check current against previous
        if (prev != null && root.val <= prev.val) {
            return false;
        }
        prev = root;
        
        return inorderCheck(root.right);
    }
    
    // Method 3: Iterative inorder with prev tracking
    public static boolean isValidBSTIterative(TreeNode root) {
        if (root == null) return true;
        
        Stack<TreeNode> stack = new Stack<>();
        TreeNode current = root;
        TreeNode prev = null;
        
        while (current != null || !stack.isEmpty()) {
            while (current != null) {
                stack.push(current);
                current = current.left;
            }
            
            current = stack.pop();
            
            if (prev != null && current.val <= prev.val) {
                return false;
            }
            prev = current;
            
            current = current.right;
        }
        
        return true;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(5);
        root.left = new TreeNode(3);
        root.right = new TreeNode(7);
        root.left.left = new TreeNode(2);
        root.left.right = new TreeNode(4);
        root.right.right = new TreeNode(8);
        
        System.out.println("List approach: " + isValidBSTList(root));      // true
        System.out.println("Inorder approach: " + isValidBSTInorder(root)); // true
        System.out.println("Iterative: " + isValidBSTIterative(root));     // true
    }
}
```

## Handling Duplicates

Different BST conventions handle duplicates differently:

1. **Left ≤ Root < Right**: duplicates go to left subtree
2. **Left < Root ≤ Right**: duplicates go to right subtree
3. **No duplicates allowed**: strict BST

```java
public class ValidateBSTWithDuplicates {
    
    // Variation: left <= root < right
    public static boolean isValidBSTLeftLeq(TreeNode root) {
        return validateLeftLeq(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }
    
    private static boolean validateLeftLeq(TreeNode root, long min, long max) {
        if (root == null) return true;
        // Left can be equal to root (use <= for min check)
        if (root.val < min || root.val >= max) return false;
        return validateLeftLeq(root.left, min, root.val) &&
               validateLeftLeq(root.right, root.val, max);
    }
    
    // Variation: left < root <= right
    public static boolean isValidBSTRightLeq(TreeNode root) {
        return validateRightLeq(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }
    
    private static boolean validateRightLeq(TreeNode root, long min, long max) {
        if (root == null) return true;
        if (root.val <= min || root.val > max) return false;
        return validateRightLeq(root.left, min, root.val) &&
               validateRightLeq(root.right, root.val, max);
    }
}
```

## Edge Cases to Consider

```java
public class BSTEdgeCases {
    
    public static void testEdgeCases() {
        // Empty tree
        System.out.println("Empty: " + ValidateBST.isValidBST(null));  // true
        
        // Single node
        TreeNode single = new TreeNode(0);
        System.out.println("Single: " + ValidateBST.isValidBST(single));  // true
        
        // Root with both children
        TreeNode root = new TreeNode(0);
        root.left = new TreeNode(-1);
        root.right = new TreeNode(1);
        System.out.println("Root with children: " + ValidateBST.isValidBST(root));  // true
        
        // Integer overflow cases
        TreeNode overflow = new TreeNode(Integer.MAX_VALUE);
        overflow.left = new TreeNode(Integer.MIN_VALUE);
        overflow.right = new TreeNode(Integer.MAX_VALUE);  // Duplicate
        System.out.println("Overflow case: " + ValidateBST.isValidBST(overflow));  // false
        
        // Chain: 1 -> 2 -> 3 -> 4 (skewed, but valid)
        TreeNode skewed = new TreeNode(1);
        skewed.right = new TreeNode(2);
        skewed.right.right = new TreeNode(3);
        skewed.right.right.right = new TreeNode(4);
        System.out.println("Skewed valid: " + ValidateBST.isValidBST(skewed));  // true
    }
}
```

## Complete Validation with All Approaches

```java
public class BSTValidatorComplete {
    
    public static boolean isValidBST(TreeNode root) {
        return rangeCheck(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }
    
    private static boolean rangeCheck(TreeNode root, long min, long max) {
        if (root == null) return true;
        if (root.val <= min || root.val >= max) return false;
        return rangeCheck(root.left, min, root.val) && 
               rangeCheck(root.right, root.val, max);
    }
    
    public static boolean isValidBSTInorder(TreeNode root) {
        if (root == null) return true;
        
        Stack<TreeNode> stack = new Stack<>();
        TreeNode current = root;
        TreeNode prev = null;
        
        while (current != null || !stack.isEmpty()) {
            while (current != null) {
                stack.push(current);
                current = current.left;
            }
            
            current = stack.pop();
            
            if (prev != null && current.val <= prev.val) {
                return false;
            }
            prev = current;
            
            current = current.right;
        }
        
        return true;
    }
    
    // Min/Max tracking approach (alternative to Long)
    public static boolean isValidBSTWithNull(TreeNode root) {
        return validateWithNull(root, null, null);
    }
    
    private static boolean validateWithNull(TreeNode root, Integer min, Integer max) {
        if (root == null) return true;
        
        if ((min != null && root.val <= min) || (max != null && root.val >= max)) {
            return false;
        }
        
        return validateWithNull(root.left, min, root.val) &&
               validateWithNull(root.right, root.val, max);
    }
    
    // Test all approaches
    public static void main(String[] args) {
        TreeNode root = new TreeNode(10);
        root.left = new TreeNode(5);
        root.right = new TreeNode(15);
        root.left.left = new TreeNode(3);
        root.left.right = new TreeNode(7);
        root.right.right = new TreeNode(20);
        
        System.out.println("Range check: " + isValidBST(root));       // true
        System.out.println("Inorder: " + isValidBSTInorder(root));    // true
        System.out.println("Null bounds: " + isValidBSTWithNull(root)); // true
        
        // Edge case with Integer values
        TreeNode tricky = new TreeNode(Integer.MAX_VALUE);
        System.out.println("Integer.MAX_VALUE: " + isValidBST(tricky));  // true
        // With Long bounds, Integer.MAX_VALUE < Long.MAX_VALUE, no overflow
    }
}
```

## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Range Recursive | O(n) | O(h) | Best overall |
| Inorder + List | O(n) | O(n) | Extra list space |
| Inorder + Prev | O(n) | O(h) | No extra list |
| Iterative Inorder | O(n) | O(h) | Avoids recursion |

## Practical Insights

1. **Use `long` for bounds**, not `int`. This handles Integer.MIN_VALUE and Integer.MAX_VALUE edge cases.
2. The **range approach** is the most intuitive and most commonly expected in interviews.
3. The **inorder approach** is useful when you also need to verify sorted order for other properties.
4. **Common mistake**: only checking immediate children instead of the full subtree.
5. **Interview tip**: mention both approaches and explain the tradeoffs. Start with range recursive, mention inorder alternative.
