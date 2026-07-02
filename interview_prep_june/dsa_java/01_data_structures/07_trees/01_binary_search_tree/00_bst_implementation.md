# Binary Search Tree Implementation

## BST Property

For every node in a BST:
- All values in the **left subtree** are **less than** the node's value.
- All values in the **right subtree** are **greater than** the node's value.
- Both left and right subtrees are also BSTs.

```
        8
      /   \
     3     10
    / \      \
   1   6      14
      / \    /
     4   7  13
```

**Inorder traversal** of a BST gives values in **sorted ascending order**.

## TreeNode Structure

Same as binary tree node:

```java
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    
    TreeNode(int val) {
        this.val = val;
    }
}
```

## BST Class with Insert (Recursive and Iterative)

```java
import java.util.*;

public class BST {
    
    private TreeNode root;
    
    public BST() {
        this.root = null;
    }
    
    public BST(int[] values) {
        for (int val : values) {
            insert(val);
        }
    }
    
    // === INSERTION ===
    
    // Recursive insert
    public void insert(int val) {
        root = insertRec(root, val);
    }
    
    private TreeNode insertRec(TreeNode root, int val) {
        if (root == null) {
            return new TreeNode(val);
        }
        
        if (val < root.val) {
            root.left = insertRec(root.left, val);
        } else if (val > root.val) {
            root.right = insertRec(root.right, val);
        }
        // If equal, we can either ignore or handle duplicates
        // For this implementation, we ignore duplicates
        
        return root;
    }
    
    // Iterative insert
    public void insertIterative(int val) {
        TreeNode newNode = new TreeNode(val);
        
        if (root == null) {
            root = newNode;
            return;
        }
        
        TreeNode current = root;
        TreeNode parent = null;
        
        while (current != null) {
            parent = current;
            if (val < current.val) {
                current = current.left;
            } else if (val > current.val) {
                current = current.right;
            } else {
                return;  // Duplicate — ignore
            }
        }
        
        if (val < parent.val) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }
    }
    
    // === SEARCH ===
    
    // Recursive search
    public boolean search(int val) {
        return searchRec(root, val);
    }
    
    private boolean searchRec(TreeNode root, int val) {
        if (root == null) return false;
        if (root.val == val) return true;
        
        if (val < root.val) {
            return searchRec(root.left, val);
        } else {
            return searchRec(root.right, val);
        }
    }
    
    // Iterative search
    public boolean searchIterative(int val) {
        TreeNode current = root;
        
        while (current != null) {
            if (current.val == val) return true;
            if (val < current.val) {
                current = current.left;
            } else {
                current = current.right;
            }
        }
        
        return false;
    }
    
    // === TRAVERSAL ===
    
    // Inorder gives sorted order
    public List<Integer> inorder() {
        List<Integer> result = new ArrayList<>();
        inorderRec(root, result);
        return result;
    }
    
    private void inorderRec(TreeNode root, List<Integer> result) {
        if (root == null) return;
        inorderRec(root.left, result);
        result.add(root.val);
        inorderRec(root.right, result);
    }
    
    // Preorder
    public List<Integer> preorder() {
        List<Integer> result = new ArrayList<>();
        preorderRec(root, result);
        return result;
    }
    
    private void preorderRec(TreeNode root, List<Integer> result) {
        if (root == null) return;
        result.add(root.val);
        preorderRec(root.left, result);
        preorderRec(root.right, result);
    }
    
    // Postorder
    public List<Integer> postorder() {
        List<Integer> result = new ArrayList<>();
        postorderRec(root, result);
        return result;
    }
    
    private void postorderRec(TreeNode root, List<Integer> result) {
        if (root == null) return;
        postorderRec(root.left, result);
        postorderRec(root.right, result);
        result.add(root.val);
    }
    
    // Level order
    public List<Integer> levelOrder() {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            TreeNode current = queue.poll();
            result.add(current.val);
            
            if (current.left != null) queue.offer(current.left);
            if (current.right != null) queue.offer(current.right);
        }
        
        return result;
    }
    
    public TreeNode getRoot() {
        return root;
    }
    
    public static void main(String[] args) {
        BST bst = new BST();
        int[] values = {8, 3, 10, 1, 6, 14, 4, 7, 13};
        
        for (int val : values) {
            bst.insert(val);
        }
        
        System.out.println("Inorder (sorted): " + bst.inorder());
        // [1, 3, 4, 6, 7, 8, 10, 13, 14]
        
        System.out.println("Preorder: " + bst.preorder());
        // [8, 3, 1, 6, 4, 7, 10, 14, 13]
        
        System.out.println("Search 6: " + bst.search(6));     // true
        System.out.println("Search 100: " + bst.search(100)); // false
    }
}
```

## Constructing BST from Sorted Array

```java
public class BSTFromSortedArray {
    
    // Build balanced BST from sorted array
    public static TreeNode sortedArrayToBST(int[] nums) {
        return build(nums, 0, nums.length - 1);
    }
    
    private static TreeNode build(int[] nums, int left, int right) {
        if (left > right) return null;
        
        // Pick middle as root for balance
        int mid = left + (right - left) / 2;
        TreeNode root = new TreeNode(nums[mid]);
        
        root.left = build(nums, left, mid - 1);
        root.right = build(nums, mid + 1, right);
        
        return root;
    }
    
    // Convert a BST to a balanced BST
    public static TreeNode balanceBST(TreeNode root) {
        List<Integer> sorted = new ArrayList<>();
        inorderStore(root, sorted);
        
        int[] arr = sorted.stream().mapToInt(Integer::intValue).toArray();
        return sortedArrayToBST(arr);
    }
    
    private static void inorderStore(TreeNode root, List<Integer> result) {
        if (root == null) return;
        inorderStore(root.left, result);
        result.add(root.val);
        inorderStore(root.right, result);
    }
    
    public static void main(String[] args) {
        int[] sorted = {1, 3, 4, 6, 7, 8, 10, 13, 14};
        TreeNode root = sortedArrayToBST(sorted);
        
        // Verify inorder
        List<Integer> inorder = new ArrayList<>();
        BST bst = new BST();  // Need BST instance or use helper
        // Just print manually: inorder should be same array
        
        System.out.println("Balanced BST built from sorted array");
        System.out.println("Root: " + root.val);  // Should be 7 or 8
    }
}
```

## BST Insertion with Visualization

```java
public class BSTVisualization {
    
    // Insert sequence visualization
    public static void demonstrateInsertion() {
        BST bst = new BST();
        int[] values = {50, 30, 70, 20, 40, 60, 80};
        
        System.out.println("Inserting: " + Arrays.toString(values));
        System.out.println();
        
        for (int val : values) {
            bst.insert(val);
            System.out.println("After inserting " + val + ": " + bst.inorder());
        }
        
        //       50
        //      /  \
        //     30   70
        //    / \   / \
        //   20 40 60 80
        //
        // Inorder: [20, 30, 40, 50, 60, 70, 80]
        
        System.out.println("\nFinal tree inorder: " + bst.inorder());
        System.out.println("Height: " + height(bst.getRoot()));
        System.out.println("Is balanced: " + isBalanced(bst.getRoot()));
    }
    
    private static int height(TreeNode root) {
        if (root == null) return -1;
        return 1 + Math.max(height(root.left), height(root.right));
    }
    
    private static boolean isBalanced(TreeNode root) {
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
    
    public static void main(String[] args) {
        demonstrateInsertion();
    }
}
```

## BST Validation Check

```java
public class BSTValidator {
    
    // Verify BST property for a given tree
    public static boolean isValidBST(TreeNode root) {
        return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }
    
    private static boolean validate(TreeNode root, long min, long max) {
        if (root == null) return true;
        if (root.val <= min || root.val >= max) return false;
        return validate(root.left, min, root.val) &&
               validate(root.right, root.val, max);
    }
    
    // Inorder check
    public static boolean isValidBSTInorder(TreeNode root) {
        List<Integer> inorder = new ArrayList<>();
        inorderStore(root, inorder);
        
        for (int i = 1; i < inorder.size(); i++) {
            if (inorder.get(i) <= inorder.get(i - 1)) return false;
        }
        return true;
    }
    
    private static void inorderStore(TreeNode root, List<Integer> result) {
        if (root == null) return;
        inorderStore(root.left, result);
        result.add(root.val);
        inorderStore(root.right, result);
    }
    
    // Inorder with tracking previous (no extra list)
    private static TreeNode prev = null;
    
    public static boolean isValidBSTInorderOpt(TreeNode root) {
        prev = null;
        return inorderCheck(root);
    }
    
    private static boolean inorderCheck(TreeNode root) {
        if (root == null) return true;
        
        if (!inorderCheck(root.left)) return false;
        
        if (prev != null && root.val <= prev.val) return false;
        prev = root;
        
        return inorderCheck(root.right);
    }
}
```

## Utility Methods for BST

```java
public class BSTUtils {
    
    // Count nodes
    public static int countNodes(TreeNode root) {
        if (root == null) return 0;
        return 1 + countNodes(root.left) + countNodes(root.right);
    }
    
    // Height
    public static int height(TreeNode root) {
        if (root == null) return -1;
        return 1 + Math.max(height(root.left), height(root.right));
    }
    
    // Check if tree is BST
    public static boolean isBST(TreeNode root) {
        return isBSTHelper(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }
    
    private static boolean isBSTHelper(TreeNode root, long min, long max) {
        if (root == null) return true;
        if (root.val <= min || root.val >= max) return false;
        return isBSTHelper(root.left, min, root.val) &&
               isBSTHelper(root.right, root.val, max);
    }
    
    // Print tree structure
    public static void printTree(TreeNode root) {
        if (root == null) {
            System.out.println("Empty tree");
            return;
        }
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            for (int i = 0; i < levelSize; i++) {
                TreeNode current = queue.poll();
                System.out.print(current.val + " ");
                
                if (current.left != null) queue.offer(current.left);
                if (current.right != null) queue.offer(current.right);
            }
            System.out.println();
        }
    }
    
    // Deep copy
    public static TreeNode clone(TreeNode root) {
        if (root == null) return null;
        TreeNode newRoot = new TreeNode(root.val);
        newRoot.left = clone(root.left);
        newRoot.right = clone(root.right);
        return newRoot;
    }
}
```

## Test and Demo

```java
public class BSTDemo {
    public static void main(String[] args) {
        System.out.println("=== BST Implementation Demo ===\n");
        
        // Test 1: Basic insertion and traversal
        BST bst = new BST();
        int[] values = {8, 3, 10, 1, 6, 14, 4, 7, 13};
        
        for (int v : values) bst.insert(v);
        
        System.out.println("Tree built from: " + Arrays.toString(values));
        System.out.println("Inorder (sorted):   " + bst.inorder());
        System.out.println("Preorder:           " + bst.preorder());
        System.out.println("Postorder:          " + bst.postorder());
        System.out.println("Level order:        " + bst.levelOrder());
        System.out.println();
        
        // Test 2: Search
        System.out.println("Search 6:  " + bst.search(6));
        System.out.println("Search 13: " + bst.search(13));
        System.out.println("Search 99: " + bst.search(99));
        System.out.println();
        
        // Test 3: From sorted array
        int[] sorted = {1, 2, 3, 4, 5, 6, 7};
        TreeNode balanced = BSTFromSortedArray.sortedArrayToBST(sorted);
        System.out.println("Balanced BST from [1,2,3,4,5,6,7]:");
        System.out.println("Root: " + balanced.val);  // 4
        
        // Verify it's a valid BST
        System.out.println("Is valid BST: " + BSTValidator.isValidBST(balanced));
        
        // Test 4: Empty and single node
        BST empty = new BST();
        System.out.println("\nEmpty tree inorder: " + empty.inorder());
        
        BST single = new BST();
        single.insert(42);
        System.out.println("Single node inorder: " + single.inorder());
    }
}
```

## Complexity Analysis

| Operation | Average Case | Worst Case | Notes |
|-----------|-------------|------------|-------|
| Insert | O(log n) | O(n) | Skewed tree = linked list |
| Search | O(log n) | O(n) | Same as insert |
| Delete | O(log n) | O(n) | Complex for 2-child case |
| Inorder | O(n) | O(n) | Always visits all nodes |
| Space | O(n) | O(n) | Node storage |

## Practical Insights

1. **BST performance depends entirely on balance**. A skewed BST is just a linked list with O(n) operations.
2. **Inorder traversal always gives sorted order** in a BST — this is the key property used in many problems.
3. **Recursive insert** is simpler but can overflow stack for deep trees. **Iterative insert** is safer.
4. **Duplicates** in BST need a consistent policy: either left ≤ root < right, or left < root ≤ right.
5. In Java, **TreeMap** and **TreeSet** are implemented using Red-Black Trees (self-balancing BSTs).
