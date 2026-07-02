# Height, Diameter, Depth Problems

## Height / Depth of Tree

```java
import java.util.*;

public class TreeHeightDepth {
    
    // Height (number of edges on longest path from root to leaf)
    public static int height(TreeNode root) {
        if (root == null) return -1;  // -1 for edge count
        return 1 + Math.max(height(root.left), height(root.right));
    }
    
    // Height counting nodes (root at height 1)
    public static int heightNodes(TreeNode root) {
        if (root == null) return 0;
        return 1 + Math.max(heightNodes(root.left), heightNodes(root.right));
    }
    
    // Depth of a specific node
    public static int depth(TreeNode root, int target, int currentDepth) {
        if (root == null) return -1;
        if (root.val == target) return currentDepth;
        
        int left = depth(root.left, target, currentDepth + 1);
        if (left != -1) return left;
        return depth(root.right, target, currentDepth + 1);
    }
    
    // Iterative depth finder
    public static int depthIterative(TreeNode root, int target) {
        if (root == null) return -1;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        int depth = 0;
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode current = queue.poll();
                if (current.val == target) return depth;
                
                if (current.left != null) queue.offer(current.left);
                if (current.right != null) queue.offer(current.right);
            }
            depth++;
        }
        
        return -1;
    }
    
    // Is node a leaf?
    public static boolean isLeaf(TreeNode node) {
        return node != null && node.left == null && node.right == null;
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
        
        System.out.println("Height (edges): " + height(root));  // 2
        System.out.println("Height (nodes): " + heightNodes(root));  // 3
        System.out.println("Depth of 4: " + depth(root, 4, 0));  // 2
        System.out.println("Depth of 1: " + depth(root, 1, 0));  // 0
        System.out.println("Depth of 3: " + depth(root, 3, 0));  // 1
    }
}
```

## Diameter of Binary Tree

The **diameter** (or width) of a binary tree is the length of the longest path between any two nodes. This path may or may not pass through the root.

```java
public class TreeDiameter {
    
    // O(n²) approach — compute height for each node
    public static int diameterNaive(TreeNode root) {
        if (root == null) return 0;
        
        // Path passes through root
        int throughRoot = height(root.left) + height(root.right) + 2;
        // Path is entirely in left or right subtree
        int leftDiameter = diameterNaive(root.left);
        int rightDiameter = diameterNaive(root.right);
        
        return Math.max(throughRoot, Math.max(leftDiameter, rightDiameter));
    }
    
    private static int height(TreeNode root) {
        if (root == null) return -1;
        return 1 + Math.max(height(root.left), height(root.right));
    }
    
    // O(n) approach — compute height and diameter simultaneously
    static class DiaResult {
        int diameter = 0;
    }
    
    public static int diameterOptimized(TreeNode root) {
        DiaResult result = new DiaResult();
        calculateHeight(root, result);
        return result.diameter;
    }
    
    private static int calculateHeight(TreeNode root, DiaResult result) {
        if (root == null) return -1;
        
        int leftHeight = calculateHeight(root.left, result);
        int rightHeight = calculateHeight(root.right, result);
        
        // Update diameter: path through this node
        int currentDiameter = leftHeight + rightHeight + 2;
        result.diameter = Math.max(result.diameter, currentDiameter);
        
        // Return height of this node
        return 1 + Math.max(leftHeight, rightHeight);
    }
    
    // Alternative: using a global variable
    private static int diameter = 0;
    
    public static int diameterGlobal(TreeNode root) {
        diameter = 0;
        heightForDiameter(root);
        return diameter;
    }
    
    private static int heightForDiameter(TreeNode root) {
        if (root == null) return -1;
        
        int leftHeight = heightForDiameter(root.left);
        int rightHeight = heightForDiameter(root.right);
        
        diameter = Math.max(diameter, leftHeight + rightHeight + 2);
        
        return 1 + Math.max(leftHeight, rightHeight);
    }
    
    // Diameter counting nodes (instead of edges)
    public static int diameterNodeCount(TreeNode root) {
        if (root == null) return 0;
        
        int[] result = new int[1];
        heightNodeCount(root, result);
        return result[0];
    }
    
    private static int heightNodeCount(TreeNode root, int[] result) {
        if (root == null) return 0;
        
        int left = heightNodeCount(root.left, result);
        int right = heightNodeCount(root.right, result);
        
        result[0] = Math.max(result[0], left + right + 1);
        
        return 1 + Math.max(left, right);
    }
    
    public static void main(String[] args) {
        //       1
        //      / \
        //     2   3
        //    / \
        //   4   5
        //  /
        // 6
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        root.left.left.left = new TreeNode(6);
        
        System.out.println("Diameter (naive):    " + diameterNaive(root));    // 4 (6→4→2→5)
        System.out.println("Diameter (opt):      " + diameterOptimized(root)); // 4
        System.out.println("Diameter (global):   " + diameterGlobal(root));    // 4
        System.out.println("Diameter (nodes):    " + diameterNodeCount(root)); // 5
    }
}
```

## Balanced Tree Check

A tree is height-balanced if for every node, the height difference between left and right subtrees is at most 1.

```java
public class BalancedTreeCheck {
    
    // O(n²) approach
    public static boolean isBalancedNaive(TreeNode root) {
        if (root == null) return true;
        
        int leftHeight = height(root.left);
        int rightHeight = height(root.right);
        
        return Math.abs(leftHeight - rightHeight) <= 1 &&
               isBalancedNaive(root.left) &&
               isBalancedNaive(root.right);
    }
    
    private static int height(TreeNode root) {
        if (root == null) return -1;
        return 1 + Math.max(height(root.left), height(root.right));
    }
    
    // O(n) approach — return -1 if unbalanced, else return height
    public static boolean isBalanced(TreeNode root) {
        return checkHeight(root) != -1;
    }
    
    private static int checkHeight(TreeNode root) {
        if (root == null) return -1;
        
        int leftHeight = checkHeight(root.left);
        if (leftHeight == -1) return -1;  // Left unbalanced
        
        int rightHeight = checkHeight(root.right);
        if (rightHeight == -1) return -1;  // Right unbalanced
        
        if (Math.abs(leftHeight - rightHeight) > 1) return -1;  // Current unbalanced
        
        return 1 + Math.max(leftHeight, rightHeight);
    }
    
    // Alternative: using a class to track balance + height
    static class BalanceInfo {
        boolean balanced;
        int height;
        
        BalanceInfo(boolean balanced, int height) {
            this.balanced = balanced;
            this.height = height;
        }
    }
    
    public static boolean isBalancedClass(TreeNode root) {
        return checkBalanced(root).balanced;
    }
    
    private static BalanceInfo checkBalanced(TreeNode root) {
        if (root == null) return new BalanceInfo(true, -1);
        
        BalanceInfo left = checkBalanced(root.left);
        if (!left.balanced) return new BalanceInfo(false, 0);
        
        BalanceInfo right = checkBalanced(root.right);
        if (!right.balanced) return new BalanceInfo(false, 0);
        
        boolean balanced = Math.abs(left.height - right.height) <= 1;
        int height = 1 + Math.max(left.height, right.height);
        
        return new BalanceInfo(balanced, height);
    }
    
    public static void main(String[] args) {
        // Balanced tree
        TreeNode balanced = new TreeNode(1);
        balanced.left = new TreeNode(2);
        balanced.right = new TreeNode(3);
        balanced.left.left = new TreeNode(4);
        balanced.left.right = new TreeNode(5);
        
        System.out.println("Balanced: " + isBalanced(balanced));  // true
        
        // Unbalanced tree
        TreeNode unbalanced = new TreeNode(1);
        unbalanced.left = new TreeNode(2);
        unbalanced.left.left = new TreeNode(3);
        unbalanced.left.left.left = new TreeNode(4);
        
        System.out.println("Unbalanced: " + isBalanced(unbalanced));  // false
    }
}
```

## Minimum Depth of Binary Tree

The minimum depth is the number of nodes along the shortest path from root to the nearest leaf.

```java
public class MinDepth {
    
    // Recursive
    public static int minDepth(TreeNode root) {
        if (root == null) return 0;
        
        // Leaf node
        if (root.left == null && root.right == null) return 1;
        
        // If one child is null, we must go through the other
        if (root.left == null) return 1 + minDepth(root.right);
        if (root.right == null) return 1 + minDepth(root.left);
        
        // Both children exist
        return 1 + Math.min(minDepth(root.left), minDepth(root.right));
    }
    
    // BFS — more efficient for minimum depth (short-circuits early)
    public static int minDepthBFS(TreeNode root) {
        if (root == null) return 0;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        int depth = 1;
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode current = queue.poll();
                
                // First leaf found = minimum depth
                if (current.left == null && current.right == null) {
                    return depth;
                }
                
                if (current.left != null) queue.offer(current.left);
                if (current.right != null) queue.offer(current.right);
            }
            
            depth++;
        }
        
        return depth;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(9);
        root.right = new TreeNode(20);
        root.right.left = new TreeNode(15);
        root.right.right = new TreeNode(7);
        
        System.out.println("Min Depth: " + minDepth(root));      // 2
        System.out.println("Min Depth BFS: " + minDepthBFS(root)); // 2
        
        // Skewed tree
        TreeNode skewed = new TreeNode(1);
        skewed.left = new TreeNode(2);
        skewed.left.right = new TreeNode(3);
        
        System.out.println("Min Depth (skewed): " + minDepth(skewed));  // 3 (must go to leaf)
    }
}
```

## Maximum Depth of Binary Tree

```java
public class MaxDepth {
    
    // Recursive
    public static int maxDepth(TreeNode root) {
        if (root == null) return 0;
        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
    }
    
    // BFS
    public static int maxDepthBFS(TreeNode root) {
        if (root == null) return 0;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        int depth = 0;
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            for (int i = 0; i < levelSize; i++) {
                TreeNode current = queue.poll();
                if (current.left != null) queue.offer(current.left);
                if (current.right != null) queue.offer(current.right);
            }
            depth++;
        }
        
        return depth;
    }
    
    // Iterative DFS (preorder)
    public static int maxDepthDFS(TreeNode root) {
        if (root == null) return 0;
        
        Stack<TreeNode> nodeStack = new Stack<>();
        Stack<Integer> depthStack = new Stack<>();
        nodeStack.push(root);
        depthStack.push(1);
        int maxDepth = 0;
        
        while (!nodeStack.isEmpty()) {
            TreeNode node = nodeStack.pop();
            int depth = depthStack.pop();
            maxDepth = Math.max(maxDepth, depth);
            
            if (node.right != null) {
                nodeStack.push(node.right);
                depthStack.push(depth + 1);
            }
            if (node.left != null) {
                nodeStack.push(node.left);
                depthStack.push(depth + 1);
            }
        }
        
        return maxDepth;
    }
}
```

## Complete Test Class

```java
public class HeightDiameterDepthDemo {
    public static void main(String[] args) {
        //       1
        //      / \
        //     2   3
        //    / \   \
        //   4   5   6
        //  /
        // 7
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        root.right.right = new TreeNode(6);
        root.left.left.left = new TreeNode(7);
        
        System.out.println("=== Height, Diameter, Depth ===");
        System.out.println("Height (edges): " + TreeHeightDepth.height(root));       // 3
        System.out.println("Height (nodes): " + TreeHeightDepth.heightNodes(root));  // 4
        System.out.println("Min Depth: " + MinDepth.minDepth(root));                 // 3
        System.out.println("Max Depth: " + MaxDepth.maxDepth(root));                 // 4
        
        System.out.println("\nDiameter: " + TreeDiameter.diameterOptimized(root));   // 5 (7→4→2→5 or 7→4→2→1→3→6)
        System.out.println("Is Balanced: " + BalancedTreeCheck.isBalanced(root));    // true
        
        // Check specific node depths
        System.out.println("\nDepth of 5: " + TreeHeightDepth.depth(root, 5, 0));   // 2
        System.out.println("Depth of 7: " + TreeHeightDepth.depth(root, 7, 0));     // 3
        System.out.println("Depth of 1: " + TreeHeightDepth.depth(root, 1, 0));     // 0
    }
}
```

## Complexity Analysis

| Problem | Naive Time | Optimized Time | Space |
|---------|-----------|----------------|-------|
| Height | O(n) | O(n) | O(h) |
| Diameter | O(n²) | O(n) | O(h) |
| Balanced Check | O(n²) | O(n) | O(h) |
| Min Depth (recursive) | O(n) | O(n) | O(h) |
| Min Depth (BFS) | O(n) | O(n) | O(w) |
| Max Depth | O(n) | O(n) | O(h) |

## Practical Insights

1. **Diameter** is a classic postorder problem: compute heights bottom-up, update diameter along the way.
2. **Balanced check** returning `-1` for unbalanced is an elegant optimization that short-circuits early.
3. **Min depth** with BFS is more efficient than recursion because you stop at the first leaf.
4. The **difference between height and depth**: height goes up from leaf, depth goes down from root.
5. All these problems follow the **postorder pattern**: compute for children first, then combine at root.
