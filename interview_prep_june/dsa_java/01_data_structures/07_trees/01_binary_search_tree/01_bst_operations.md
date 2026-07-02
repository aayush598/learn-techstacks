# BST Operations: Min, Max, Floor, Ceiling, Delete, Successor, Predecessor

## Find Min and Max

```java
import java.util.*;

public class BSTMinMax {
    
    // Find minimum (leftmost node)
    public static int findMin(TreeNode root) {
        if (root == null) throw new NoSuchElementException("Empty tree");
        
        TreeNode current = root;
        while (current.left != null) {
            current = current.left;
        }
        return current.val;
    }
    
    // Find minimum recursively
    public static TreeNode findMinNode(TreeNode root) {
        if (root == null || root.left == null) return root;
        return findMinNode(root.left);
    }
    
    // Find maximum (rightmost node)
    public static int findMax(TreeNode root) {
        if (root == null) throw new NoSuchElementException("Empty tree");
        
        TreeNode current = root;
        while (current.right != null) {
            current = current.right;
        }
        return current.val;
    }
    
    // Find maximum recursively
    public static TreeNode findMaxNode(TreeNode root) {
        if (root == null || root.right == null) return root;
        return findMaxNode(root.right);
    }
    
    public static void main(String[] args) {
        //       8
        //      / \
        //     3   10
        //    / \    \
        //   1   6   14
        TreeNode root = new TreeNode(8);
        root.left = new TreeNode(3);
        root.right = new TreeNode(10);
        root.left.left = new TreeNode(1);
        root.left.right = new TreeNode(6);
        root.right.right = new TreeNode(14);
        
        System.out.println("Min: " + findMin(root));  // 1
        System.out.println("Max: " + findMax(root));  // 14
    }
}
```

## Floor and Ceiling

**Floor**: largest value in BST ≤ target
**Ceiling**: smallest value in BST ≥ target

```java
public class FloorCeiling {
    
    // Floor: largest value <= target
    public static int floor(TreeNode root, int target) {
        int result = Integer.MIN_VALUE;
        
        while (root != null) {
            if (root.val == target) return target;
            
            if (root.val < target) {
                result = root.val;  // This could be the floor
                root = root.right;  // Look for a larger but still <= target
            } else {
                root = root.left;   // Look for smaller values
            }
        }
        
        return result;
    }
    
    // Ceiling: smallest value >= target
    public static int ceiling(TreeNode root, int target) {
        int result = Integer.MAX_VALUE;
        
        while (root != null) {
            if (root.val == target) return target;
            
            if (root.val > target) {
                result = root.val;  // This could be the ceiling
                root = root.left;   // Look for a smaller but still >= target
            } else {
                root = root.right;  // Look for larger values
            }
        }
        
        return result;
    }
    
    // Floor recursively
    public static TreeNode floorNode(TreeNode root, int target) {
        if (root == null) return null;
        if (root.val == target) return root;
        
        if (root.val > target) return floorNode(root.left, target);
        
        // root.val < target, this could be floor, but check right subtree
        TreeNode rightResult = floorNode(root.right, target);
        return rightResult != null ? rightResult : root;
    }
    
    // Ceiling recursively
    public static TreeNode ceilingNode(TreeNode root, int target) {
        if (root == null) return null;
        if (root.val == target) return root;
        
        if (root.val < target) return ceilingNode(root.right, target);
        
        TreeNode leftResult = ceilingNode(root.left, target);
        return leftResult != null ? leftResult : root;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(8);
        root.left = new TreeNode(3);
        root.right = new TreeNode(10);
        root.left.left = new TreeNode(1);
        root.left.right = new TreeNode(6);
        root.right.right = new TreeNode(14);
        
        System.out.println("Floor of 5: " + floor(root, 5));      // 3
        System.out.println("Floor of 7: " + floor(root, 7));      // 6
        System.out.println("Floor of 17: " + floor(root, 17));    // 14
        System.out.println("Floor of 1: " + floor(root, 1));      // 1
        System.out.println("Floor of -1: " + floor(root, -1));    // MIN_VALUE (no floor)
        
        System.out.println("Ceiling of 5: " + ceiling(root, 5));  // 6
        System.out.println("Ceiling of 7: " + ceiling(root, 7));  // 8
        System.out.println("Ceiling of 17: " + ceiling(root, 17)); // MAX_VALUE (no ceiling)
    }
}
```

## Delete a Node in BST

Three cases:
- **0 children (leaf)**: just remove
- **1 child**: replace node with its child
- **2 children**: find inorder successor (or predecessor), replace value, delete successor

```java
public class BSTDelete {
    
    public static TreeNode deleteNode(TreeNode root, int val) {
        if (root == null) return null;
        
        // Search for the node to delete
        if (val < root.val) {
            root.left = deleteNode(root.left, val);
        } else if (val > root.val) {
            root.right = deleteNode(root.right, val);
        } else {
            // Node to delete found
            
            // Case 1: Leaf (0 children)
            if (root.left == null && root.right == null) {
                return null;
            }
            
            // Case 2: 1 child
            if (root.left == null) {
                return root.right;
            }
            if (root.right == null) {
                return root.left;
            }
            
            // Case 3: 2 children
            // Find inorder successor (smallest in right subtree)
            TreeNode successor = findMin(root.right);
            root.val = successor.val;  // Replace with successor value
            root.right = deleteNode(root.right, successor.val);  // Delete successor
        }
        
        return root;
    }
    
    // Alternative: use inorder predecessor (largest in left subtree)
    public static TreeNode deleteNodeWithPredecessor(TreeNode root, int val) {
        if (root == null) return null;
        
        if (val < root.val) {
            root.left = deleteNodeWithPredecessor(root.left, val);
        } else if (val > root.val) {
            root.right = deleteNodeWithPredecessor(root.right, val);
        } else {
            if (root.left == null && root.right == null) return null;
            if (root.left == null) return root.right;
            if (root.right == null) return root.left;
            
            // Use inorder predecessor (largest in left subtree)
            TreeNode predecessor = findMax(root.left);
            root.val = predecessor.val;
            root.left = deleteNodeWithPredecessor(root.left, predecessor.val);
        }
        
        return root;
    }
    
    private static TreeNode findMin(TreeNode root) {
        while (root.left != null) root = root.left;
        return root;
    }
    
    private static TreeNode findMax(TreeNode root) {
        while (root.right != null) root = root.right;
        return root;
    }
    
    // Iterative delete
    public static TreeNode deleteNodeIterative(TreeNode root, int val) {
        if (root == null) return null;
        
        TreeNode parent = null;
        TreeNode current = root;
        
        // Find node to delete and its parent
        while (current != null && current.val != val) {
            parent = current;
            if (val < current.val) {
                current = current.left;
            } else {
                current = current.right;
            }
        }
        
        if (current == null) return root;  // Not found
        
        // Case 1 & 2: 0 or 1 child
        if (current.left == null || current.right == null) {
            TreeNode newChild = (current.left != null) ? current.left : current.right;
            
            if (parent == null) {
                return newChild;  // Deleting root
            }
            if (parent.left == current) {
                parent.left = newChild;
            } else {
                parent.right = newChild;
            }
        } else {
            // Case 3: 2 children
            TreeNode successorParent = current;
            TreeNode successor = current.right;
            
            while (successor.left != null) {
                successorParent = successor;
                successor = successor.left;
            }
            
            current.val = successor.val;
            
            if (successorParent.left == successor) {
                successorParent.left = successor.right;
            } else {
                successorParent.right = successor.right;
            }
        }
        
        return root;
    }
    
    public static void main(String[] args) {
        //       8
        //      / \
        //     3   10
        //    / \    \
        //   1   6   14
        //      / \
        //     4   7
        TreeNode root = new TreeNode(8);
        root.left = new TreeNode(3);
        root.right = new TreeNode(10);
        root.left.left = new TreeNode(1);
        root.left.right = new TreeNode(6);
        root.right.right = new TreeNode(14);
        root.left.right.left = new TreeNode(4);
        root.left.right.right = new TreeNode(7);
        
        System.out.println("Original inorder: " + inorderList(root));
        
        root = deleteNode(root, 3);  // Node with 2 children
        System.out.println("After delete 3: " + inorderList(root));
        // [1, 4, 6, 7, 8, 10, 14]
        
        root = deleteNode(root, 14);  // Leaf
        System.out.println("After delete 14: " + inorderList(root));
        // [1, 4, 6, 7, 8, 10]
        
        root = deleteNode(root, 10);  // Node with 1 child
        System.out.println("After delete 10: " + inorderList(root));
        // [1, 4, 6, 7, 8]
    }
    
    private static List<Integer> inorderList(TreeNode root) {
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

## Predecessor and Successor

**Predecessor**: largest node with value < given value
**Successor**: smallest node with value > given value

```java
public class PredecessorSuccessor {
    
    // Inorder predecessor
    public static TreeNode predecessor(TreeNode root, int val) {
        TreeNode pred = null;
        
        while (root != null) {
            if (root.val >= val) {
                root = root.left;
            } else {
                pred = root;
                root = root.right;
            }
        }
        
        return pred;
    }
    
    // Inorder successor
    public static TreeNode successor(TreeNode root, int val) {
        TreeNode succ = null;
        
        while (root != null) {
            if (root.val <= val) {
                root = root.right;
            } else {
                succ = root;
                root = root.left;
            }
        }
        
        return succ;
    }
    
    // Predecessor recursively
    public static TreeNode predecessorRec(TreeNode root, int val) {
        if (root == null) return null;
        
        if (root.val >= val) {
            return predecessorRec(root.left, val);
        }
        
        TreeNode right = predecessorRec(root.right, val);
        return right != null ? right : root;
    }
    
    // Successor recursively
    public static TreeNode successorRec(TreeNode root, int val) {
        if (root == null) return null;
        
        if (root.val <= val) {
            return successorRec(root.right, val);
        }
        
        TreeNode left = successorRec(root.left, val);
        return left != null ? left : root;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(8);
        root.left = new TreeNode(3);
        root.right = new TreeNode(10);
        root.left.left = new TreeNode(1);
        root.left.right = new TreeNode(6);
        root.right.right = new TreeNode(14);
        root.left.right.left = new TreeNode(4);
        root.left.right.right = new TreeNode(7);
        
        System.out.println("Predecessor of 8: " + predecessor(root, 8).val);   // 7
        System.out.println("Successor of 8: " + successor(root, 8).val);       // 10
        System.out.println("Predecessor of 6: " + predecessor(root, 6).val);   // 4
        System.out.println("Successor of 6: " + successor(root, 6).val);       // 7
        System.out.println("Predecessor of 1: " + predecessor(root, 1));       // null
        System.out.println("Successor of 14: " + successor(root, 14));         // null
        System.out.println("Predecessor of 5: " + predecessor(root, 5).val);   // 4
        System.out.println("Successor of 5: " + successor(root, 5).val);       // 6
    }
}
```

## Range Sum in BST

```java
public class RangeSumBST {
    
    // Sum of values between L and R inclusive
    public static int rangeSumBST(TreeNode root, int L, int R) {
        if (root == null) return 0;
        
        if (root.val < L) {
            return rangeSumBST(root.right, L, R);
        }
        if (root.val > R) {
            return rangeSumBST(root.left, L, R);
        }
        
        return root.val + rangeSumBST(root.left, L, R) + rangeSumBST(root.right, L, R);
    }
    
    // Iterative using stack
    public static int rangeSumBSTIterative(TreeNode root, int L, int R) {
        int sum = 0;
        if (root == null) return sum;
        
        Stack<TreeNode> stack = new Stack<>();
        stack.push(root);
        
        while (!stack.isEmpty()) {
            TreeNode current = stack.pop();
            
            if (current == null) continue;
            
            if (current.val >= L && current.val <= R) {
                sum += current.val;
            }
            
            if (current.val > L) {
                stack.push(current.left);
            }
            if (current.val < R) {
                stack.push(current.right);
            }
        }
        
        return sum;
    }
    
    // BFS
    public static int rangeSumBSTBFS(TreeNode root, int L, int R) {
        int sum = 0;
        if (root == null) return sum;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            TreeNode current = queue.poll();
            
            if (current.val >= L && current.val <= R) {
                sum += current.val;
            }
            
            if (current.left != null && current.val > L) {
                queue.offer(current.left);
            }
            if (current.right != null && current.val < R) {
                queue.offer(current.right);
            }
        }
        
        return sum;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(10);
        root.left = new TreeNode(5);
        root.right = new TreeNode(15);
        root.left.left = new TreeNode(3);
        root.left.right = new TreeNode(7);
        root.right.right = new TreeNode(18);
        
        System.out.println("Range sum [7, 15]: " + rangeSumBST(root, 7, 15));  // 10+7+15=32
        System.out.println("Range sum [5, 18]: " + rangeSumBST(root, 5, 18));  // 5+7+10+15+18=55
    }
}
```

## Inorder Successor in BST (with parent pointers)

```java
public class InorderSuccessorWithParent {
    
    // If node has right subtree → successor is min of right subtree
    // Else → climb up until node is left child of its parent
    
    public static TreeNode inorderSuccessor(TreeNode node) {
        if (node == null) return null;
        
        // Case 1: Has right subtree
        if (node.right != null) {
            TreeNode current = node.right;
            while (current.left != null) {
                current = current.left;
            }
            return current;
        }
        
        // Case 2: No right subtree, climb up
        TreeNode parent = node.parent;  // Assuming node has parent field
        while (parent != null && parent.right == node) {
            node = parent;
            parent = parent.parent;
        }
        return parent;
    }
    
    // Find successor in BST given root (without parent)
    public static TreeNode inorderSuccessor(TreeNode root, TreeNode target) {
        TreeNode successor = null;
        
        while (root != null) {
            if (target.val < root.val) {
                successor = root;
                root = root.left;
            } else {
                root = root.right;
            }
        }
        
        return successor;
    }
}
```

## Complexity Summary

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Min/Max | O(h) | O(1) | Traverse left/right only |
| Floor/Ceiling | O(h) | O(1) | Iterative traversal |
| Delete | O(h) | O(h) | Recursive; O(1) iterative |
| Predecessor/Successor | O(h) | O(1) | Two-step algorithm |
| Range Sum | O(n) | O(h) | BST pruning optimization |
| Inorder Successor | O(h) | O(1) | With or without parent |

## Practical Insights

1. **Delete is the most complex** BST operation. The 2-child case requires finding the successor (or predecessor).
2. **Inorder successor** is a classic interview problem. Key insight: if right subtree exists, it's the minimum of right subtree; otherwise, climb up.
3. **Floor/Ceiling** operations are generalizations of search — they don't require exact matches.
4. **Range sum** can be optimized using BST pruning: skip entire subtrees that fall outside the range.
5. The **predecessor/successor** concept extends to order-statistic operations (Kth smallest, etc.).
