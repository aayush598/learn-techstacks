# Inorder, Preorder, Postorder Traversals (Recursive)

## Overview

Depth-First Search (DFS) traversals explore the tree by going as deep as possible before backtracking. The three main types differ in the order of visiting the root relative to its children.

## Inorder Traversal (Left → Root → Right)

```java
public class InorderTraversal {
    
    // Recursive inorder
    public static void inorderRecursive(TreeNode root) {
        if (root == null) return;
        inorderRecursive(root.left);
        System.out.print(root.val + " ");
        inorderRecursive(root.right);
    }
    
    // Inorder with result list
    public static List<Integer> inorderList(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        inorderHelper(root, result);
        return result;
    }
    
    private static void inorderHelper(TreeNode root, List<Integer> result) {
        if (root == null) return;
        inorderHelper(root.left, result);
        result.add(root.val);
        inorderHelper(root.right, result);
    }
}
```

### Properties of Inorder
- In a **BST**, inorder gives nodes in **ascending order**.
- For the tree below, inorder = **4, 2, 5, 1, 3**
- Time: O(n), Space: O(h) for recursion stack

```
    1
   / \
  2   3
 / \
4   5
```

## Preorder Traversal (Root → Left → Right)

```java
public class PreorderTraversal {
    
    // Recursive preorder
    public static void preorderRecursive(TreeNode root) {
        if (root == null) return;
        System.out.print(root.val + " ");
        preorderRecursive(root.left);
        preorderRecursive(root.right);
    }
    
    // Preorder with result list
    public static List<Integer> preorderList(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        preorderHelper(root, result);
        return result;
    }
    
    private static void preorderHelper(TreeNode root, List<Integer> result) {
        if (root == null) return;
        result.add(root.val);
        preorderHelper(root.left, result);
        preorderHelper(root.right, result);
    }
}
```

### Properties of Preorder
- Root is visited **first** before any subtree.
- Used to **serialize** a tree (reconstruct from preorder + inorder).
- Used to **copy/clone** a tree (create root first, then children).
- For the sample tree: **1, 2, 4, 5, 3**

## Postorder Traversal (Left → Right → Root)

```java
public class PostorderTraversal {
    
    // Recursive postorder
    public static void postorderRecursive(TreeNode root) {
        if (root == null) return;
        postorderRecursive(root.left);
        postorderRecursive(root.right);
        System.out.print(root.val + " ");
    }
    
    // Postorder with result list
    public static List<Integer> postorderList(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        postorderHelper(root, result);
        return result;
    }
    
    private static void postorderHelper(TreeNode root, List<Integer> result) {
        if (root == null) return;
        postorderHelper(root.left, result);
        postorderHelper(root.right, result);
        result.add(root.val);
    }
}
```

### Properties of Postorder
- Root is visited **last** after both subtrees.
- Used to **delete a tree** (delete children before parent).
- Used in **bottom-up DP** calculations (e.g., tree diameter).
- For the sample tree: **4, 5, 2, 3, 1**

## All Three Traversals in One Class

```java
public class AllTraversals {
    
    public static void traverse(TreeNode root) {
        System.out.print("Inorder: ");
        inorder(root);
        System.out.println();
        
        System.out.print("Preorder: ");
        preorder(root);
        System.out.println();
        
        System.out.print("Postorder: ");
        postorder(root);
        System.out.println();
    }
    
    private static void inorder(TreeNode root) {
        if (root == null) return;
        inorder(root.left);
        System.out.print(root.val + " ");
        inorder(root.right);
    }
    
    private static void preorder(TreeNode root) {
        if (root == null) return;
        System.out.print(root.val + " ");
        preorder(root.left);
        preorder(root.right);
    }
    
    private static void postorder(TreeNode root) {
        if (root == null) return;
        postorder(root.left);
        postorder(root.right);
        System.out.print(root.val + " ");
    }
    
    public static void main(String[] args) {
        //       1
        //      / \
        //     2   3
        //    / \
        //   4   5
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        
        traverse(root);
        // Inorder:   4 2 5 1 3
        // Preorder:  1 2 4 5 3
        // Postorder: 4 5 2 3 1
    }
}
```

## Multi-Method Traversal

```java
import java.util.*;

public class TraversalDemo {
    
    public static List<Integer> inorder(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        inorderHelper(root, res);
        return res;
    }
    
    private static void inorderHelper(TreeNode root, List<Integer> res) {
        if (root == null) return;
        inorderHelper(root.left, res);
        res.add(root.val);
        inorderHelper(root.right, res);
    }
    
    public static List<Integer> preorder(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        preorderHelper(root, res);
        return res;
    }
    
    private static void preorderHelper(TreeNode root, List<Integer> res) {
        if (root == null) return;
        res.add(root.val);
        preorderHelper(root.left, res);
        preorderHelper(root.right, res);
    }
    
    public static List<Integer> postorder(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        postorderHelper(root, res);
        return res;
    }
    
    private static void postorderHelper(TreeNode root, List<Integer> res) {
        if (root == null) return;
        postorderHelper(root.left, res);
        postorderHelper(root.right, res);
        res.add(root.val);
    }
    
    public static void printAll(TreeNode root) {
        System.out.println("Inorder:    " + inorder(root));
        System.out.println("Preorder:   " + preorder(root));
        System.out.println("Postorder:  " + postorder(root));
    }
}
```

## Usage Scenarios

| Traversal | Use Case |
|-----------|---------|
| **Inorder** | BST gives sorted order, expression trees (infix notation) |
| **Preorder** | Tree serialization, cloning, prefix expression, copying |
| **Postorder** | Tree deletion, postfix expression, bottom-up DP, calculating tree properties (height, diameter) |

### Example: BST Inorder Gives Sorted Order

```java
// For BST:    10
//            /  \
//           5    15
//          / \   / \
//         2   8 12 20
// Inorder: 2, 5, 8, 10, 12, 15, 20
// 
// This property is used to verify if a tree is a BST
// (inorder traversal should be strictly increasing)
```

## Time & Space Complexity

| Aspect | Complexity |
|--------|-----------|
| Time | **O(n)** — each node visited exactly once |
| Space (recursion stack) | **O(h)** where h = height of tree |
| Best case space (balanced) | O(log n) |
| Worst case space (skewed) | O(n) |

## Practical Insights

1. **Recursion is elegant** but can cause **StackOverflowError** for very deep trees (10K+ nodes). Use iterative approaches for production code with unknown depth.

2. **Morris traversal** achieves O(1) space by using threaded connections, at the cost of modifying the tree temporarily.

3. The **order of recursive calls** directly corresponds to:
   - Preorder: process before recursive calls
   - Inorder: process between recursive calls
   - Postorder: process after recursive calls

4. The three traversals can be remembered as:
   - **Pre** = before children (root first)
   - **In** = between children (root in middle)
   - **Post** = after children (root last)
