# Morris Traversal — O(1) Space Tree Traversal

## Concept

Morris traversal uses **threaded binary tree** concept to achieve inorder and preorder traversal in **O(1) extra space** (besides the output list) while maintaining O(n) time complexity.

### Key Insight
Instead of using a stack or recursion to backtrack, Morris traversal temporarily modifies the tree by creating **threads** (pointers from the rightmost node of left subtree back to the current node).

## Threaded Binary Tree Concept

A threaded binary tree has **threads** (pointers) that point from a node to its inorder predecessor or successor, eliminating the need for recursion/stack.

In Morris traversal:
- Before moving to left subtree, we find the **predecessor** (rightmost node in left subtree).
- We create a **temporary thread** from predecessor to current node.
- When we revisit the node (via thread), we **remove the thread** to restore the tree.

## Morris Inorder Traversal

```java
import java.util.*;

public class MorrisInorder {
    
    public static List<Integer> morrisInorder(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        TreeNode current = root;
        
        while (current != null) {
            if (current.left == null) {
                // No left subtree, visit current and go right
                result.add(current.val);
                current = current.right;
            } else {
                // Find inorder predecessor of current
                TreeNode predecessor = current.left;
                while (predecessor.right != null && predecessor.right != current) {
                    predecessor = predecessor.right;
                }
                
                // If no thread yet, create one and go left
                if (predecessor.right == null) {
                    predecessor.right = current;  // Create thread
                    current = current.left;
                } 
                // Thread exists, remove it and visit current
                else {
                    predecessor.right = null;  // Remove thread
                    result.add(current.val);
                    current = current.right;
                }
            }
        }
        
        return result;
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
        
        System.out.println("Morris Inorder: " + morrisInorder(root));
        // Output: [4, 2, 5, 1, 3]
        
        // Tree is restored to original after traversal
    }
}
```

## Morris Preorder Traversal

```java
public class MorrisPreorder {
    
    public static List<Integer> morrisPreorder(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        TreeNode current = root;
        
        while (current != null) {
            if (current.left == null) {
                // No left subtree, visit current and go right
                result.add(current.val);
                current = current.right;
            } else {
                // Find inorder predecessor
                TreeNode predecessor = current.left;
                while (predecessor.right != null && predecessor.right != current) {
                    predecessor = predecessor.right;
                }
                
                // If no thread yet, visit current, create thread, go left
                if (predecessor.right == null) {
                    result.add(current.val);  // Visit in preorder
                    predecessor.right = current;
                    current = current.left;
                }
                // Thread exists, remove it and go right
                else {
                    predecessor.right = null;
                    current = current.right;
                }
            }
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        
        System.out.println("Morris Preorder: " + morrisPreorder(root));
        // Output: [1, 2, 4, 5, 3]
    }
}
```

## Detailed Step-by-Step Example

For the tree:
```
    4
   / \
  2   6
 / \ / \
1  3 5 7
```

### Morris Inorder Steps:

1. `current = 4`, has left child → find predecessor of 4 = 3
   - `predecessor.right == null` → create thread 3.right = 4, move left to 2

2. `current = 2`, has left child → find predecessor of 2 = 1
   - `predecessor.right == null` → create thread 1.right = 2, move left to 1

3. `current = 1`, no left child → **visit 1**, move to right = 2 (via thread)

4. `current = 2`, has left child → predecessor.right = current (thread exists)
   - Remove thread (1.right = null), **visit 2**, move right to 3

5. `current = 3`, no left child → **visit 3**, move to right = 4 (via thread)

6. `current = 4`, has left child → predecessor.right = current (thread exists)
   - Remove thread (3.right = null), **visit 4**, move right to 6

7. `current = 6`, has left child → predecessor of 6 = 5
   - Create thread 5.right = 6, move left to 5

8. `current = 5`, no left child → **visit 5**, move right to 6 (via thread)

9. `current = 6`, has left child → predecessor.right = current (thread exists)
   - Remove thread, **visit 6**, move right to 7

10. `current = 7`, no left child → **visit 7**, move right (null) → traversal ends

Result: **1, 2, 3, 4, 5, 6, 7**

## Unified Morris Traversal

```java
public class MorrisTraversal {
    
    public enum TraversalType {
        INORDER, PREORDER
    }
    
    public static List<Integer> morrisTraversal(TreeNode root, TraversalType type) {
        List<Integer> result = new ArrayList<>();
        TreeNode current = root;
        
        while (current != null) {
            if (current.left == null) {
                result.add(current.val);
                current = current.right;
            } else {
                TreeNode predecessor = current.left;
                while (predecessor.right != null && predecessor.right != current) {
                    predecessor = predecessor.right;
                }
                
                if (predecessor.right == null) {
                    predecessor.right = current;
                    if (type == TraversalType.PREORDER) {
                        result.add(current.val);
                    }
                    current = current.left;
                } else {
                    predecessor.right = null;
                    if (type == TraversalType.INORDER) {
                        result.add(current.val);
                    }
                    current = current.right;
                }
            }
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        
        System.out.println("Morris Inorder:  " + 
            morrisTraversal(root, TraversalType.INORDER));
        System.out.println("Morris Preorder: " + 
            morrisTraversal(root, TraversalType.PREORDER));
    }
}
```

## Complexity Analysis

| Metric | Value |
|--------|-------|
| Time | **O(n)** — each edge traversed at most 3 times |
| Space | **O(1)** — no stack/recursion, only pointers |
| Tree modification | **Temporary** — tree restored after traversal |

### Why is it O(n)?
- Each node is visited at most twice (once to create thread, once to remove)
- Finding predecessor: total work is O(n) because each edge in left subtree is traversed at most twice (once down to find predecessor, once up via thread)

## When to Use Morris Traversal

1. **When O(1) space is required** (e.g., embedded systems, interview constraints)
2. **When tree is read-only** is NOT a constraint (tree is temporarily modified)
3. **Postorder** cannot be done with Morris (or is very complex)
4. Use when recursion stack overflow is a concern

## Comparison: Recursive vs Iterative vs Morris

| Aspect | Recursive | Iterative (Stack) | Morris |
|--------|-----------|-------------------|--------|
| Space | O(h) | O(h) | O(1) |
| Time | O(n) | O(n) | O(n) |
| Simplicity | High | Medium | Low |
| Modifies tree | No | No | Yes (temporary) |
| Stack overflow risk | Yes (deep trees) | No | No |
| Postorder | Easy | Complex | Very hard |

## Practical Insights

1. Morris traversal is **rarely asked** in interviews, but knowing it demonstrates deep understanding of tree structure.

2. The **key trick** is finding the predecessor and using it for backtracking — this same idea appears in other tree algorithms.

3. Always **restore the tree** (remove threads) — otherwise subsequent operations will have infinite loops.

4. For **production code**, prefer iterative stack-based traversal unless memory is extremely constrained.
