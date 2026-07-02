# Binary Tree Implementation in Java

## TreeNode Class

```java
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    
    TreeNode() {}
    
    TreeNode(int val) {
        this.val = val;
    }
    
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
```

## Building a Tree Manually (Hardcoded for Testing)

```java
public class BinaryTreeBuilder {
    
    // Build this tree:
    //       1
    //      / \
    //     2   3
    //    / \
    //   4   5
    public static TreeNode buildSampleTree() {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        return root;
    }
    
    // Build this tree:
    //       10
    //      /  \
    //     5    15
    //    / \   / \
    //   2   8 12 20
    public static TreeNode buildBST() {
        TreeNode root = new TreeNode(10);
        root.left = new TreeNode(5);
        root.right = new TreeNode(15);
        root.left.left = new TreeNode(2);
        root.left.right = new TreeNode(8);
        root.right.left = new TreeNode(12);
        root.right.right = new TreeNode(20);
        return root;
    }
    
    // Build a skewed tree
    public static TreeNode buildSkewedTree() {
        TreeNode root = new TreeNode(1);
        root.right = new TreeNode(2);
        root.right.right = new TreeNode(3);
        root.right.right.right = new TreeNode(4);
        return root;
    }
    
    // Build a single node tree
    public static TreeNode buildSingleNode() {
        return new TreeNode(1);
    }
    
    // Build empty tree
    public static TreeNode buildEmptyTree() {
        return null;
    }
}
```

## Building Tree from Array Representation

Using level-order representation where `null` means no node.

```java
import java.util.*;

public class TreeFromArray {
    
    // Input: [1, 2, 3, null, 5, null, null]
    // Tree:
    //       1
    //      / \
    //     2   3
    //      \
    //       5
    public static TreeNode buildFromArray(Integer[] arr) {
        if (arr == null || arr.length == 0 || arr[0] == null) {
            return null;
        }
        
        TreeNode root = new TreeNode(arr[0]);
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        int i = 1;
        while (!queue.isEmpty() && i < arr.length) {
            TreeNode current = queue.poll();
            
            // Add left child
            if (i < arr.length && arr[i] != null) {
                current.left = new TreeNode(arr[i]);
                queue.offer(current.left);
            }
            i++;
            
            // Add right child
            if (i < arr.length && arr[i] != null) {
                current.right = new TreeNode(arr[i]);
                queue.offer(current.right);
            }
            i++;
        }
        
        return root;
    }
    
    // Convert tree back to array representation
    public static List<Integer> treeToArray(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            TreeNode node = queue.poll();
            if (node == null) {
                result.add(null);
            } else {
                result.add(node.val);
                queue.offer(node.left);
                queue.offer(node.right);
            }
        }
        
        // Remove trailing nulls
        int lastIndex = result.size() - 1;
        while (lastIndex >= 0 && result.get(lastIndex) == null) {
            lastIndex--;
        }
        return result.subList(0, lastIndex + 1);
    }
}
```

## Building Tree from Level Order Input

```java
import java.util.*;

public class LevelOrderInput {
    
    // Read tree from Scanner input
    public static TreeNode readFromScanner(Scanner sc) {
        System.out.println("Enter tree elements in level order (use -1 for null):");
        String[] tokens = sc.nextLine().split(" ");
        
        if (tokens.length == 0 || tokens[0].equals("-1")) {
            return null;
        }
        
        Integer[] arr = new Integer[tokens.length];
        for (int i = 0; i < tokens.length; i++) {
            int val = Integer.parseInt(tokens[i]);
            arr[i] = (val == -1) ? null : val;
        }
        
        return TreeFromArray.buildFromArray(arr);
    }
    
    // Create tree from list of values
    public static TreeNode createTree(List<Integer> values) {
        Integer[] arr = values.toArray(new Integer[0]);
        return TreeFromArray.buildFromArray(arr);
    }
}
```

## Utility Methods

### Count Nodes

```java
public class TreeUtils {
    
    // Count total nodes in tree
    public static int countNodes(TreeNode root) {
        if (root == null) return 0;
        return 1 + countNodes(root.left) + countNodes(root.right);
    }
    
    // Count leaf nodes
    public static int countLeaves(TreeNode root) {
        if (root == null) return 0;
        if (root.left == null && root.right == null) return 1;
        return countLeaves(root.left) + countLeaves(root.right);
    }
    
    // Count internal nodes
    public static int countInternalNodes(TreeNode root) {
        if (root == null || (root.left == null && root.right == null)) {
            return 0;
        }
        return 1 + countInternalNodes(root.left) + countInternalNodes(root.right);
    }
    
    // Count nodes at given level
    public static int countNodesAtLevel(TreeNode root, int level) {
        if (root == null) return 0;
        if (level == 0) return 1;
        return countNodesAtLevel(root.left, level - 1) +
               countNodesAtLevel(root.right, level - 1);
    }
    
    // Count nodes with exactly one child
    public static int countNodesWithOneChild(TreeNode root) {
        if (root == null) return 0;
        int hasOneChild = 0;
        if ((root.left == null && root.right != null) ||
            (root.left != null && root.right == null)) {
            hasOneChild = 1;
        }
        return hasOneChild + countNodesWithOneChild(root.left) +
               countNodesWithOneChild(root.right);
    }
    
    // Count full nodes (nodes with 2 children)
    public static int countFullNodes(TreeNode root) {
        if (root == null) return 0;
        int isFull = (root.left != null && root.right != null) ? 1 : 0;
        return isFull + countFullNodes(root.left) + countFullNodes(root.right);
    }
}
```

### Height and Depth

```java
// Height of tree (number of edges on longest path from root to leaf)
public static int height(TreeNode root) {
    if (root == null) return -1;  // by edges convention
    // if (root == null) return 0; // by nodes convention
    return 1 + Math.max(height(root.left), height(root.right));
}

// Height of a specific node
public static int nodeHeight(TreeNode root, int target, int depth) {
    if (root == null) return -1;
    if (root.val == target) return height(root);
    int left = nodeHeight(root.left, target, depth + 1);
    if (left != -1) return left;
    return nodeHeight(root.right, target, depth + 1);
}

// Depth of a node from root
public static int depth(TreeNode root, int target, int currentDepth) {
    if (root == null) return -1;
    if (root.val == target) return currentDepth;
    int left = depth(root.left, target, currentDepth + 1);
    if (left != -1) return left;
    return depth(root.right, target, currentDepth + 1);
}

// Level of a node (depth + 1)
public static int level(TreeNode root, int target) {
    int d = depth(root, target, 0);
    return d == -1 ? -1 : d + 1;
}
```

### Size, Max, Min

```java
// Size of tree (total nodes)
public static int size(TreeNode root) {
    if (root == null) return 0;
    return size(root.left) + 1 + size(root.right);
}

// Maximum value in tree
public static int findMax(TreeNode root) {
    if (root == null) return Integer.MIN_VALUE;
    int leftMax = findMax(root.left);
    int rightMax = findMax(root.right);
    return Math.max(root.val, Math.max(leftMax, rightMax));
}

// Minimum value in tree
public static int findMin(TreeNode root) {
    if (root == null) return Integer.MAX_VALUE;
    int leftMin = findMin(root.left);
    int rightMin = findMin(root.right);
    return Math.min(root.val, Math.min(leftMin, rightMin));
}

// Search for a value
public static boolean contains(TreeNode root, int target) {
    if (root == null) return false;
    if (root.val == target) return true;
    return contains(root.left, target) || contains(root.right, target);
}
```

### Helper Methods

```java
// Print tree in formatted way (for debugging)
public static void printTree(TreeNode root) {
    if (root == null) {
        System.out.println("Tree is empty");
        return;
    }
    
    int h = height(root);
    int width = (int) Math.pow(2, h + 1);
    List<List<String>> levels = new ArrayList<>();
    
    for (int i = 0; i <= h; i++) {
        levels.add(new ArrayList<>(Collections.nCopies(width, " ")));
    }
    
    fillLevels(root, 0, 0, width - 1, levels);
    
    for (List<String> level : levels) {
        for (String s : level) {
            System.out.print(s);
        }
        System.out.println();
    }
}

private static void fillLevels(TreeNode node, int level, int left, int right,
                                List<List<String>> levels) {
    if (node == null) return;
    
    int mid = left + (right - left) / 2;
    levels.get(level).set(mid, String.valueOf(node.val));
    
    fillLevels(node.left, level + 1, left, mid - 1, levels);
    fillLevels(node.right, level + 1, mid + 1, right, levels);
}

// Check if tree is empty
public static boolean isEmpty(TreeNode root) {
    return root == null;
}

// Deep clone a tree
public static TreeNode clone(TreeNode root) {
    if (root == null) return null;
    TreeNode newNode = new TreeNode(root.val);
    newNode.left = clone(root.left);
    newNode.right = clone(root.right);
    return newNode;
}
```

## Main Test Class

```java
public class Main {
    public static void main(String[] args) {
        // Build from Array
        Integer[] arr = {1, 2, 3, null, 5, null, null};
        TreeNode root = TreeFromArray.buildFromArray(arr);
        
        System.out.println("Tree built from array:");
        System.out.println("Size: " + TreeUtils.countNodes(root));
        System.out.println("Height: " + TreeUtils.height(root));
        System.out.println("Max value: " + TreeUtils.findMax(root));
        System.out.println("Min value: " + TreeUtils.findMin(root));
        System.out.println("Leaves: " + TreeUtils.countLeaves(root));
        System.out.println("Internal nodes: " + TreeUtils.countInternalNodes(root));
        
        // Build from hardcoded
        TreeNode sample = BinaryTreeBuilder.buildSampleTree();
        System.out.println("\nSample tree size: " + TreeUtils.size(sample));
        
        // Convert back to array
        List<Integer> arrBack = TreeFromArray.treeToArray(root);
        System.out.println("\nTree as array: " + arrBack);
        
        // Array: [1, 2, 3, null, 5]
    }
}
```
