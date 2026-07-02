# Level Order Traversal (BFS)

## Basic Level Order Traversal

Uses a **Queue** (FIFO) to process nodes level by level.

```java
import java.util.*;

public class LevelOrderTraversal {
    
    // Basic level order: print each level on separate line
    public static void levelOrder(TreeNode root) {
        if (root == null) return;
        
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
            System.out.println();  // New line per level
        }
    }
    
    // Level order returning list of levels
    public static List<List<Integer>> levelOrderList(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            List<Integer> currentLevel = new ArrayList<>();
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode current = queue.poll();
                currentLevel.add(current.val);
                
                if (current.left != null) queue.offer(current.left);
                if (current.right != null) queue.offer(current.right);
            }
            
            result.add(currentLevel);
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        //       1
        //      / \
        //     2   3
        //    / \   \
        //   4   5   6
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        root.right.right = new TreeNode(6);
        
        System.out.println("Level Order:");
        levelOrder(root);
        // 1
        // 2 3
        // 4 5 6
        
        System.out.println("Level Order List: " + levelOrderList(root));
        // [[1], [2, 3], [4, 5, 6]]
    }
}
```

## Zigzag / Spiral Level Order

Alternating direction: left→right, then right→left, then left→right, etc.

```java
public class ZigzagTraversal {
    
    // Method 1: Using deque and direction flag
    public static List<List<Integer>> zigzagLevelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        
        Deque<TreeNode> deque = new LinkedList<>();
        deque.offer(root);
        boolean leftToRight = true;
        
        while (!deque.isEmpty()) {
            int levelSize = deque.size();
            List<Integer> currentLevel = new ArrayList<>();
            
            for (int i = 0; i < levelSize; i++) {
                if (leftToRight) {
                    // Remove from front, add children to back (left then right)
                    TreeNode current = deque.pollFirst();
                    currentLevel.add(current.val);
                    
                    if (current.left != null) deque.offerLast(current.left);
                    if (current.right != null) deque.offerLast(current.right);
                } else {
                    // Remove from back, add children to front (right then left)
                    TreeNode current = deque.pollLast();
                    currentLevel.add(current.val);
                    
                    if (current.right != null) deque.offerFirst(current.right);
                    if (current.left != null) deque.offerFirst(current.left);
                }
            }
            
            result.add(currentLevel);
            leftToRight = !leftToRight;
        }
        
        return result;
    }
    
    // Method 2: Using queue and Collections.reverse
    public static List<List<Integer>> zigzagWithReverse(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        boolean reverse = false;
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            List<Integer> currentLevel = new ArrayList<>();
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode current = queue.poll();
                currentLevel.add(current.val);
                
                if (current.left != null) queue.offer(current.left);
                if (current.right != null) queue.offer(current.right);
            }
            
            if (reverse) {
                Collections.reverse(currentLevel);
            }
            result.add(currentLevel);
            reverse = !reverse;
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        root.right.left = new TreeNode(6);
        root.right.right = new TreeNode(7);
        
        System.out.println("Zigzag: " + zigzagLevelOrder(root));
        // [[1], [3, 2], [4, 5, 6, 7]]
    }
}
```

## Average of Levels

```java
public class AverageOfLevels {
    
    public static List<Double> averageOfLevels(TreeNode root) {
        List<Double> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            double levelSum = 0;
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode current = queue.poll();
                levelSum += current.val;
                
                if (current.left != null) queue.offer(current.left);
                if (current.right != null) queue.offer(current.right);
            }
            
            result.add(levelSum / levelSize);
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(9);
        root.right = new TreeNode(20);
        root.right.left = new TreeNode(15);
        root.right.right = new TreeNode(7);
        
        System.out.println("Averages: " + averageOfLevels(root));
        // [3.0, 14.5, 11.0]
    }
}
```

## Right Side View

Shows the rightmost node at each level.

```java
public class RightSideView {
    
    // BFS approach: last node of each level
    public static List<Integer> rightSideView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode current = queue.poll();
                
                // Last node of this level → visible from right side
                if (i == levelSize - 1) {
                    result.add(current.val);
                }
                
                if (current.left != null) queue.offer(current.left);
                if (current.right != null) queue.offer(current.right);
            }
        }
        
        return result;
    }
    
    // DFS approach: track depth, first time at depth = rightmost
    public static List<Integer> rightSideViewDFS(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        rightViewDFS(root, 0, result);
        return result;
    }
    
    private static void rightViewDFS(TreeNode root, int depth, List<Integer> result) {
        if (root == null) return;
        
        // First time at this depth from the right side
        if (depth == result.size()) {
            result.add(root.val);
        }
        
        // Go right first! (ensures rightmost node is seen first)
        rightViewDFS(root.right, depth + 1, result);
        rightViewDFS(root.left, depth + 1, result);
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.right = new TreeNode(5);
        root.right.right = new TreeNode(4);
        
        System.out.println("Right Side View: " + rightSideView(root));
        // [1, 3, 4]
    }
}
```

## Left Side View

```java
public class LeftSideView {
    
    // BFS: first node of each level
    public static List<Integer> leftSideView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode current = queue.poll();
                
                // First node of this level → visible from left side
                if (i == 0) {
                    result.add(current.val);
                }
                
                if (current.left != null) queue.offer(current.left);
                if (current.right != null) queue.offer(current.right);
            }
        }
        
        return result;
    }
    
    // DFS: track depth
    public static List<Integer> leftSideViewDFS(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        leftViewDFS(root, 0, result);
        return result;
    }
    
    private static void leftViewDFS(TreeNode root, int depth, List<Integer> result) {
        if (root == null) return;
        
        if (depth == result.size()) {
            result.add(root.val);
        }
        
        leftViewDFS(root.left, depth + 1, result);
        leftViewDFS(root.right, depth + 1, result);
    }
}
```

## Cousins in Binary Tree

Two nodes are cousins if they are at the same level but have different parents.

```java
public class CousinsInBinaryTree {
    
    public static boolean areCousins(TreeNode root, int x, int y) {
        if (root == null) return false;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            boolean foundX = false;
            boolean foundY = false;
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode current = queue.poll();
                
                // Check if current node is one of the targets
                if (current.val == x) foundX = true;
                if (current.val == y) foundY = true;
                
                // Check if they share the same parent
                if (current.left != null && current.right != null) {
                    if ((current.left.val == x && current.right.val == y) ||
                        (current.left.val == y && current.right.val == x)) {
                        return false;  // Siblings, not cousins
                    }
                }
                
                if (current.left != null) queue.offer(current.left);
                if (current.right != null) queue.offer(current.right);
            }
            
            // Both found at same level → cousins
            if (foundX && foundY) return true;
            // Only one found → not cousins
            if (foundX || foundY) return false;
        }
        
        return false;
    }
    
    // Alternative: find parent and depth for both, compare
    public static boolean areCousinsAlt(TreeNode root, int x, int y) {
        int[] depthX = new int[1];
        int[] depthY = new int[1];
        TreeNode parentX = findParentAndDepth(root, x, -1, depthX, 0);
        TreeNode parentY = findParentAndDepth(root, y, -1, depthY, 0);
        
        return depthX[0] == depthY[0] && parentX != parentY;
    }
    
    private static TreeNode findParentAndDepth(TreeNode root, int val, int parentVal,
                                                int[] depth, int currentDepth) {
        if (root == null) return null;
        
        if (root.val == val) {
            depth[0] = currentDepth;
            return new TreeNode(parentVal);  // Return parent as dummy node
        }
        
        TreeNode left = findParentAndDepth(root.left, val, root.val, depth, currentDepth + 1);
        if (left != null) return left;
        return findParentAndDepth(root.right, val, root.val, depth, currentDepth + 1);
    }
    
    public static void main(String[] args) {
        //       1
        //      / \
        //     2   3
        //    /   / \
        //   4   5   6
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.right.left = new TreeNode(5);
        root.right.right = new TreeNode(6);
        
        System.out.println("Are 4 and 5 cousins? " + areCousins(root, 4, 5));  // true
        System.out.println("Are 4 and 6 cousins? " + areCousins(root, 4, 6));  // true
        System.out.println("Are 4 and 2 cousins? " + areCousins(root, 4, 2));  // false
        System.out.println("Are 2 and 3 cousins? " + areCousins(root, 2, 3));  // false
    }
}
```

## BFS Utility Methods

```java
public class BFSUtils {
    
    // Get maximum width of tree (max nodes at any level)
    public static int maxWidth(TreeNode root) {
        if (root == null) return 0;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        int maxWidth = 0;
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            maxWidth = Math.max(maxWidth, levelSize);
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode current = queue.poll();
                if (current.left != null) queue.offer(current.left);
                if (current.right != null) queue.offer(current.right);
            }
        }
        
        return maxWidth;
    }
    
    // Check if value exists at a level
    public static boolean existsAtLevel(TreeNode root, int target, int level) {
        if (root == null) return false;
        if (level == 0) return root.val == target;
        
        return existsAtLevel(root.left, target, level - 1) ||
               existsAtLevel(root.right, target, level - 1);
    }
    
    // Print all nodes at level k
    public static List<Integer> nodesAtLevel(TreeNode root, int k) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        int currentLevel = 0;
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            
            if (currentLevel == k) {
                for (int i = 0; i < levelSize; i++) {
                    result.add(queue.poll().val);
                }
                return result;
            }
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode current = queue.poll();
                if (current.left != null) queue.offer(current.left);
                if (current.right != null) queue.offer(current.right);
            }
            currentLevel++;
        }
        
        return result;  // Level doesn't exist
    }
    
    // Level order as single array
    public static List<Integer> levelOrderArray(TreeNode root) {
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
}
```

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Level order traversal | O(n) | O(w) where w = max width |
| Zigzag traversal | O(n) | O(w) |
| Right/Left side view | O(n) | O(w) or O(h) for DFS |
| Cousins check | O(n) | O(w) |
| Average of levels | O(n) | O(w) |
| Max width | O(n) | O(w) |

Worst case space: O(n/2) ≈ O(n) for a complete tree's last level.

## Practical Insights

1. **Queue is the natural data structure** for BFS — use LinkedList or ArrayDeque.
2. The **inner loop** (`for i in 0..levelSize`) is the key pattern for level-by-level processing.
3. For **zigzag**, the deque approach is more elegant and slightly faster than reversing.
4. **Right side view** from BFS uses `i == levelSize - 1`; from DFS, go right first.
5. **Cousins** problem tests understanding of BFS: same level + different parent = cousins.
