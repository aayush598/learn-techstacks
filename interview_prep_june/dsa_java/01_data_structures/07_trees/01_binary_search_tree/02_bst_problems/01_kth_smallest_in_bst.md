# Kth Smallest / Largest in BST

## Kth Smallest Element in BST

### Approach 1: Inorder Traversal (Stop at K)

Inorder of BST gives sorted order. Traverse until we reach the Kth element.

```java
import java.util.*;

public class KthSmallest {
    
    // Recursive inorder with counter
    public static int kthSmallest(TreeNode root, int k) {
        int[] count = {0};
        int[] result = {0};
        inorder(root, k, count, result);
        return result[0];
    }
    
    private static void inorder(TreeNode root, int k, int[] count, int[] result) {
        if (root == null || count[0] >= k) return;
        
        inorder(root.left, k, count, result);
        
        count[0]++;
        if (count[0] == k) {
            result[0] = root.val;
            return;
        }
        
        inorder(root.right, k, count, result);
    }
    
    // Iterative inorder
    public static int kthSmallestIterative(TreeNode root, int k) {
        Stack<TreeNode> stack = new Stack<>();
        TreeNode current = root;
        int count = 0;
        
        while (current != null || !stack.isEmpty()) {
            while (current != null) {
                stack.push(current);
                current = current.left;
            }
            
            current = stack.pop();
            count++;
            
            if (count == k) {
                return current.val;
            }
            
            current = current.right;
        }
        
        return -1;  // k is larger than number of nodes
    }
    
    public static void main(String[] args) {
        //       5
        //      / \
        //     3   6
        //    / \
        //   2   4
        //  /
        // 1
        TreeNode root = new TreeNode(5);
        root.left = new TreeNode(3);
        root.right = new TreeNode(6);
        root.left.left = new TreeNode(2);
        root.left.right = new TreeNode(4);
        root.left.left.left = new TreeNode(1);
        
        System.out.println("1st smallest: " + kthSmallest(root, 1));  // 1
        System.out.println("3rd smallest: " + kthSmallest(root, 3));  // 3
        System.out.println("5th smallest: " + kthSmallest(root, 5));  // 5
        System.out.println("6th smallest: " + kthSmallest(root, 6));  // 6
    }
}
```

### Approach 2: Augmented BST (Store Left Subtree Size)

Maintain count of nodes in left subtree for O(h) kth smallest queries.

```java
class AugmentedTreeNode {
    int val;
    int leftSize;  // Number of nodes in left subtree
    AugmentedTreeNode left;
    AugmentedTreeNode right;
    
    AugmentedTreeNode(int val) {
        this.val = val;
        this.leftSize = 0;
    }
}

public class KthSmallestAugmented {
    
    // Insert and update leftSize
    public static AugmentedTreeNode insert(AugmentedTreeNode root, int val) {
        if (root == null) return new AugmentedTreeNode(val);
        
        if (val < root.val) {
            root.left = insert(root.left, val);
            root.leftSize++;  // Increment left subtree size
        } else {
            root.right = insert(root.right, val);
        }
        
        return root;
    }
    
    // Find kth smallest using leftSize (1-indexed)
    public static int kthSmallest(AugmentedTreeNode root, int k) {
        if (root == null) return -1;
        
        int leftCount = root.leftSize;
        
        if (k <= leftCount) {
            return kthSmallest(root.left, k);
        } else if (k == leftCount + 1) {
            return root.val;
        } else {
            return kthSmallest(root.right, k - leftCount - 1);
        }
    }
    
    // Build from array
    public static AugmentedTreeNode buildTree(int[] values) {
        AugmentedTreeNode root = null;
        for (int val : values) {
            root = insert(root, val);
        }
        return root;
    }
    
    public static void main(String[] args) {
        int[] values = {5, 3, 6, 2, 4, 1};
        AugmentedTreeNode root = buildTree(values);
        
        System.out.println("1st smallest: " + kthSmallest(root, 1));  // 1
        System.out.println("3rd smallest: " + kthSmallest(root, 3));  // 3
        System.out.println("6th smallest: " + kthSmallest(root, 6));  // 6
    }
}
```

## Kth Largest Element in BST

```java
public class KthLargest {
    
    // Method 1: Reverse inorder (right → root → left)
    public static int kthLargest(TreeNode root, int k) {
        int[] count = {0};
        int[] result = {0};
        reverseInorder(root, k, count, result);
        return result[0];
    }
    
    private static void reverseInorder(TreeNode root, int k, int[] count, int[] result) {
        if (root == null || count[0] >= k) return;
        
        reverseInorder(root.right, k, count, result);
        
        count[0]++;
        if (count[0] == k) {
            result[0] = root.val;
            return;
        }
        
        reverseInorder(root.left, k, count, result);
    }
    
    // Method 2: Total nodes - K + 1 = (N-K+1)th smallest
    public static int kthLargestAlt(TreeNode root, int k) {
        int totalNodes = countNodes(root);
        return kthSmallestInorder(root, totalNodes - k + 1);
    }
    
    private static int countNodes(TreeNode root) {
        if (root == null) return 0;
        return 1 + countNodes(root.left) + countNodes(root.right);
    }
    
    private static int kthSmallestInorder(TreeNode root, int k) {
        List<Integer> inorder = new ArrayList<>();
        inorderCollect(root, inorder);
        return inorder.get(k - 1);
    }
    
    private static void inorderCollect(TreeNode root, List<Integer> result) {
        if (root == null) return;
        inorderCollect(root.left, result);
        result.add(root.val);
        inorderCollect(root.right, result);
    }
    
    // Method 3: Iterative reverse inorder
    public static int kthLargestIterative(TreeNode root, int k) {
        Stack<TreeNode> stack = new Stack<>();
        TreeNode current = root;
        int count = 0;
        
        while (current != null || !stack.isEmpty()) {
            while (current != null) {
                stack.push(current);
                current = current.right;  // Go right first
            }
            
            current = stack.pop();
            count++;
            
            if (count == k) {
                return current.val;
            }
            
            current = current.left;
        }
        
        return -1;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(5);
        root.left = new TreeNode(3);
        root.right = new TreeNode(6);
        root.left.left = new TreeNode(2);
        root.left.right = new TreeNode(4);
        root.left.left.left = new TreeNode(1);
        
        System.out.println("1st largest: " + kthLargest(root, 1));   // 6
        System.out.println("2nd largest: " + kthLargest(root, 2));   // 5
        System.out.println("3rd largest: " + kthLargest(root, 3));   // 4
        System.out.println("6th largest: " + kthLargest(root, 6));   // 1
    }
}
```

## Kth Smallest with Frequency (Duplicate Handling)

```java
public class KthSmallestWithDuplicates {
    
    static class TreeNodeFreq {
        int val;
        int freq;  // Count of this value
        int leftCount;  // Total nodes in left subtree
        TreeNodeFreq left;
        TreeNodeFreq right;
        
        TreeNodeFreq(int val) {
            this.val = val;
            this.freq = 1;
        }
    }
    
    public static TreeNodeFreq insert(TreeNodeFreq root, int val) {
        if (root == null) return new TreeNodeFreq(val);
        
        if (val == root.val) {
            root.freq++;
        } else if (val < root.val) {
            root.left = insert(root.left, val);
            root.leftCount += 1;  // Add 1 for the node, not frequency
        } else {
            root.right = insert(root.right, val);
        }
        
        return root;
    }
    
    public static int kthSmallest(TreeNodeFreq root, int k) {
        if (root == null) return -1;
        
        if (k <= root.leftCount) {
            return kthSmallest(root.left, k);
        } else if (k <= root.leftCount + root.freq) {
            return root.val;
        } else {
            return kthSmallest(root.right, k - root.leftCount - root.freq);
        }
    }
    
    public static void main(String[] args) {
        TreeNodeFreq root = null;
        int[] values = {2, 2, 3, 1, 1, 4};
        for (int v : values) root = insert(root, v);
        
        System.out.println("1st smallest: " + kthSmallest(root, 1));  // 1
        System.out.println("2nd smallest: " + kthSmallest(root, 2));  // 1
        System.out.println("3rd smallest: " + kthSmallest(root, 3));  // 2
        System.out.println("4th smallest: " + kthSmallest(root, 4));  // 2
        System.out.println("5th smallest: " + kthSmallest(root, 5));  // 3
    }
}
```

## Order-Statistic Tree (Full Implementation)

An order-statistic tree supports:
- Insert, Delete
- kthSmallest(k)
- Rank(x): how many elements ≤ x

```java
public class OrderStatisticTree {
    
    private AugmentedTreeNode root;
    
    public void insert(int val) {
        root = insert(root, val);
    }
    
    private AugmentedTreeNode insert(AugmentedTreeNode node, int val) {
        if (node == null) return new AugmentedTreeNode(val);
        
        if (val < node.val) {
            node.left = insert(node.left, val);
            node.leftSize++;
        } else if (val > node.val) {
            node.right = insert(node.right, val);
        }
        // Ignore duplicates
        
        return node;
    }
    
    public int kthSmallest(int k) {
        if (root == null || k <= 0) return -1;
        return kthSmallest(root, k);
    }
    
    private int kthSmallest(AugmentedTreeNode node, int k) {
        if (node == null) return -1;
        
        int leftCount = node.leftSize;
        
        if (k <= leftCount) {
            return kthSmallest(node.left, k);
        } else if (k == leftCount + 1) {
            return node.val;
        } else {
            return kthSmallest(node.right, k - leftCount - 1);
        }
    }
    
    // Rank: number of elements ≤ val (1-indexed)
    public int rank(int val) {
        return rank(root, val);
    }
    
    private int rank(AugmentedTreeNode node, int val) {
        if (node == null) return 0;
        
        if (val < node.val) {
            return rank(node.left, val);
        } else if (val == node.val) {
            return node.leftSize + 1;
        } else {
            return node.leftSize + 1 + rank(node.right, val);
        }
    }
    
    public static void main(String[] args) {
        OrderStatisticTree ost = new OrderStatisticTree();
        int[] values = {5, 3, 6, 2, 4, 1, 7};
        for (int v : values) ost.insert(v);
        
        System.out.println("3rd smallest: " + ost.kthSmallest(3));  // 3
        System.out.println("5th smallest: " + ost.kthSmallest(5));  // 5
        System.out.println("Rank of 4: " + ost.rank(4));  // 4 (1,2,3,4)
        System.out.println("Rank of 6: " + ost.rank(6));  // 6
    }
}
```

## Complexity Analysis

| Approach | Query Time | Update Time | Space | Notes |
|----------|-----------|-------------|-------|-------|
| Inorder traversal | O(n) | N/A | O(h) | One-time query |
| Augmented BST | O(h) | O(h) | O(n) | Maintain leftSize |
| Inorder + List | O(n) | N/A | O(n) | Simple but wasteful |
| Order-Statistic Tree | O(log n) avg | O(log n) avg | O(n) | Full-featured |

## Practical Insights

1. For a **single query**, inorder traversal with early stopping (O(k)) is the simplest and most efficient.
2. For **frequent queries** or **dynamic BST** (frequent insert/delete), use the augmented BST with left subtree size.
3. The **augmented BST** approach is the foundation for **Order-Statistic Trees** (like `std::set` with `order_of_key` in C++'s GNU PBDS).
4. **Kth largest** = `(n - k + 1)`th smallest.
5. The **reverse inorder** (right → root → left) gives sorted descending order directly.
