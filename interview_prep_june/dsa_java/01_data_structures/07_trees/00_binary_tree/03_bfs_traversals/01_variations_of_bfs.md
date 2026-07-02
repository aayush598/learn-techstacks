# Variations of BFS

## Level Order Bottom (Reverse Level Order)

Process from bottom level to top level.

```java
import java.util.*;

public class LevelOrderBottom {
    
    // Method 1: BFS + stack (reverse)
    public static List<List<Integer>> levelOrderBottom(TreeNode root) {
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
        
        Collections.reverse(result);
        return result;
    }
    
    // Method 2: Using stack during BFS
    public static List<List<Integer>> levelOrderBottomStack(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        Stack<List<Integer>> stack = new Stack<>();
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
            
            stack.push(currentLevel);
        }
        
        while (!stack.isEmpty()) {
            result.add(stack.pop());
        }
        
        return result;
    }
    
    // Method 3: DFS with level tracking (then reverse)
    public static List<List<Integer>> levelOrderBottomDFS(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        dfs(root, 0, result);
        Collections.reverse(result);
        return result;
    }
    
    private static void dfs(TreeNode root, int level, List<List<Integer>> result) {
        if (root == null) return;
        
        if (level == result.size()) {
            result.add(new ArrayList<>());
        }
        
        result.get(level).add(root.val);
        dfs(root.left, level + 1, result);
        dfs(root.right, level + 1, result);
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(9);
        root.right = new TreeNode(20);
        root.right.left = new TreeNode(15);
        root.right.right = new TreeNode(7);
        
        System.out.println("Level Order Bottom: " + levelOrderBottom(root));
        // [[15, 7], [9, 20], [3]]
    }
}
```

## Diagonal Traversal

Traverse the tree diagonally (along lines of slope -1).

```java
public class DiagonalTraversal {
    
    // Using HashMap: key = diagonal level
    public static List<Integer> diagonalTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Map<Integer, List<Integer>> diagonalMap = new HashMap<>();
        diagonalDFS(root, 0, diagonalMap);
        
        // Collect in order of diagonal index
        int diag = 0;
        while (diagonalMap.containsKey(diag)) {
            result.addAll(diagonalMap.get(diag));
            diag++;
        }
        
        return result;
    }
    
    private static void diagonalDFS(TreeNode root, int diagonal, 
                                     Map<Integer, List<Integer>> map) {
        if (root == null) return;
        
        map.putIfAbsent(diagonal, new ArrayList<>());
        map.get(diagonal).add(root.val);
        
        // Left child goes to next diagonal
        diagonalDFS(root.left, diagonal + 1, map);
        // Right child stays on same diagonal
        diagonalDFS(root.right, diagonal, map);
    }
    
    // Iterative diagonal traversal
    public static List<Integer> diagonalTraversalIterative(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            TreeNode current = queue.poll();
            
            // Process all nodes on this diagonal (going right)
            while (current != null) {
                result.add(current.val);
                
                // Left child goes to queue (next diagonal)
                if (current.left != null) {
                    queue.offer(current.left);
                }
                
                // Move right along same diagonal
                current = current.right;
            }
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        //       1
        //      / \
        //     2   3
        //    / \   \
        //   4   5   6
        //      / \
        //     7   8
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        root.right.right = new TreeNode(6);
        root.left.right.left = new TreeNode(7);
        root.left.right.right = new TreeNode(8);
        
        System.out.println("Diagonal: " + diagonalTraversal(root));
        // Diag 0: [1, 3, 6]
        // Diag 1: [2, 5, 8]
        // Diag 2: [4, 7]
        // Output: [1, 3, 6, 2, 5, 8, 4, 7]
    }
}
```

## Vertical Order Traversal

Nodes are grouped by their horizontal distance from root (column index).

```java
public class VerticalOrderTraversal {
    
    static class NodeInfo {
        TreeNode node;
        int col;  // Column index (horizontal distance)
        
        NodeInfo(TreeNode node, int col) {
            this.node = node;
            this.col = col;
        }
    }
    
    // BFS-based vertical order
    public static List<List<Integer>> verticalOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        
        Map<Integer, List<Integer>> columnMap = new HashMap<>();
        Queue<NodeInfo> queue = new LinkedList<>();
        queue.offer(new NodeInfo(root, 0));
        
        int minCol = 0;
        int maxCol = 0;
        
        while (!queue.isEmpty()) {
            NodeInfo info = queue.poll();
            TreeNode node = info.node;
            int col = info.col;
            
            minCol = Math.min(minCol, col);
            maxCol = Math.max(maxCol, col);
            
            columnMap.putIfAbsent(col, new ArrayList<>());
            columnMap.get(col).add(node.val);
            
            if (node.left != null) {
                queue.offer(new NodeInfo(node.left, col - 1));
            }
            if (node.right != null) {
                queue.offer(new NodeInfo(node.right, col + 1));
            }
        }
        
        // Build result from minCol to maxCol
        for (int i = minCol; i <= maxCol; i++) {
            result.add(columnMap.get(i));
        }
        
        return result;
    }
    
    // Vertical order with sorting for same row/same column nodes
    // (LeetCode 987: Vertical Order Traversal of a Binary Tree)
    static class NodePosition {
        TreeNode node;
        int row;
        int col;
        
        NodePosition(TreeNode node, int row, int col) {
            this.node = node;
            this.row = row;
            this.col = col;
        }
    }
    
    public static List<List<Integer>> verticalOrderSorted(TreeNode root) {
        Map<Integer, List<int[]>> map = new HashMap<>();  // col -> list of [row, val]
        Queue<NodePosition> queue = new LinkedList<>();
        queue.offer(new NodePosition(root, 0, 0));
        
        int minCol = 0, maxCol = 0;
        
        while (!queue.isEmpty()) {
            NodePosition pos = queue.poll();
            int col = pos.col;
            int row = pos.row;
            
            minCol = Math.min(minCol, col);
            maxCol = Math.max(maxCol, col);
            
            map.putIfAbsent(col, new ArrayList<>());
            map.get(col).add(new int[]{row, pos.node.val});
            
            if (pos.node.left != null) {
                queue.offer(new NodePosition(pos.node.left, row + 1, col - 1));
            }
            if (pos.node.right != null) {
                queue.offer(new NodePosition(pos.node.right, row + 1, col + 1));
            }
        }
        
        List<List<Integer>> result = new ArrayList<>();
        for (int i = minCol; i <= maxCol; i++) {
            List<int[]> nodes = map.get(i);
            // Sort by row first, then by value
            nodes.sort((a, b) -> a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]);
            
            List<Integer> colVals = new ArrayList<>();
            for (int[] node : nodes) {
                colVals.add(node[1]);
            }
            result.add(colVals);
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(9);
        root.right = new TreeNode(20);
        root.right.left = new TreeNode(15);
        root.right.right = new TreeNode(7);
        
        System.out.println("Vertical Order: " + verticalOrder(root));
        // [[9], [3, 15], [20], [7]]
    }
}
```

## Top View and Bottom View

### Top View
First node at each horizontal distance when viewed from the top.

```java
public class TopView {
    
    public static List<Integer> topView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        // TreeMap to maintain order by column (key = column)
        Map<Integer, Integer> topMap = new TreeMap<>();
        Queue<NodeInfo> queue = new LinkedList<>();
        queue.offer(new NodeInfo(root, 0));
        
        while (!queue.isEmpty()) {
            NodeInfo info = queue.poll();
            TreeNode node = info.node;
            int col = info.col;
            
            // Only first node at each column from top
            topMap.putIfAbsent(col, node.val);
            
            if (node.left != null) {
                queue.offer(new NodeInfo(node.left, col - 1));
            }
            if (node.right != null) {
                queue.offer(new NodeInfo(node.right, col + 1));
            }
        }
        
        result.addAll(topMap.values());
        return result;
    }
    
    static class NodeInfo {
        TreeNode node;
        int col;
        
        NodeInfo(TreeNode node, int col) {
            this.node = node;
            this.col = col;
        }
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
        
        System.out.println("Top View: " + topView(root));
        // [4, 2, 1, 3, 6]
    }
}
```

### Bottom View
Last node at each horizontal distance when viewed from the bottom.

```java
public class BottomView {
    
    public static List<Integer> bottomView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Map<Integer, Integer> bottomMap = new TreeMap<>();  // col -> value
        Queue<NodeInfo> queue = new LinkedList<>();
        queue.offer(new NodeInfo(root, 0));
        
        while (!queue.isEmpty()) {
            NodeInfo info = queue.poll();
            TreeNode node = info.node;
            int col = info.col;
            
            // Overwrite with latest (bottom-most) node at this column
            bottomMap.put(col, node.val);
            
            if (node.left != null) {
                queue.offer(new NodeInfo(node.left, col - 1));
            }
            if (node.right != null) {
                queue.offer(new NodeInfo(node.right, col + 1));
            }
        }
        
        result.addAll(bottomMap.values());
        return result;
    }
    
    static class NodeInfo {
        TreeNode node;
        int col;
        
        NodeInfo(TreeNode node, int col) {
            this.node = node;
            this.col = col;
        }
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(20);
        root.left = new TreeNode(8);
        root.right = new TreeNode(22);
        root.left.left = new TreeNode(5);
        root.left.right = new TreeNode(3);
        root.right.right = new TreeNode(25);
        root.left.right.left = new TreeNode(10);
        root.left.right.right = new TreeNode(14);
        
        System.out.println("Bottom View: " + bottomView(root));
        // [5, 10, 3, 14, 25]
    }
}
```

## Boundary Traversal

Traverse the boundary of a binary tree in anti-clockwise order:
1. Left boundary (excluding leaf)
2. Leaves (left to right)
3. Right boundary (excluding leaf, reversed)

```java
public class BoundaryTraversal {
    
    public static List<Integer> boundaryOfBinaryTree(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        result.add(root.val);
        
        // Left boundary (excluding root and leaf)
        addLeftBoundary(root.left, result);
        
        // Leaves
        addLeaves(root.left, result);
        addLeaves(root.right, result);
        
        // Right boundary (excluding root and leaf, reversed)
        addRightBoundary(root.right, result);
        
        return result;
    }
    
    private static void addLeftBoundary(TreeNode root, List<Integer> result) {
        if (root == null || (root.left == null && root.right == null)) {
            return;  // Skip leaf nodes
        }
        
        result.add(root.val);
        
        if (root.left != null) {
            addLeftBoundary(root.left, result);
        } else {
            addLeftBoundary(root.right, result);
        }
    }
    
    private static void addLeaves(TreeNode root, List<Integer> result) {
        if (root == null) return;
        
        if (root.left == null && root.right == null) {
            result.add(root.val);
            return;
        }
        
        addLeaves(root.left, result);
        addLeaves(root.right, result);
    }
    
    private static void addRightBoundary(TreeNode root, List<Integer> result) {
        if (root == null || (root.left == null && root.right == null)) {
            return;  // Skip leaf nodes
        }
        
        if (root.right != null) {
            addRightBoundary(root.right, result);
        } else {
            addRightBoundary(root.left, result);
        }
        
        result.add(root.val);  // Add after recursion (reverse order)
    }
    
    // Iterative boundary traversal
    public static List<Integer> boundaryIterative(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        result.add(root.val);
        
        // Left boundary
        if (root.left != null) {
            TreeNode curr = root.left;
            while (!(curr.left == null && curr.right == null)) {
                result.add(curr.val);
                if (curr.left != null) curr = curr.left;
                else curr = curr.right;
            }
        }
        
        // Leaves (level order, check leaf)
        addLeavesIterative(root, result);
        
        // Right boundary (use stack for reverse)
        if (root.right != null) {
            Stack<Integer> stack = new Stack<>();
            TreeNode curr = root.right;
            while (!(curr.left == null && curr.right == null)) {
                stack.push(curr.val);
                if (curr.right != null) curr = curr.right;
                else curr = curr.left;
            }
            while (!stack.isEmpty()) {
                result.add(stack.pop());
            }
        }
        
        return result;
    }
    
    private static void addLeavesIterative(TreeNode root, List<Integer> result) {
        if (root == null) return;
        
        Stack<TreeNode> stack = new Stack<>();
        stack.push(root);
        
        while (!stack.isEmpty()) {
            TreeNode current = stack.pop();
            
            if (current.left == null && current.right == null) {
                if (current != root) {  // Skip root (already added)
                    result.add(current.val);
                }
            }
            
            if (current.right != null) stack.push(current.right);
            if (current.left != null) stack.push(current.left);
        }
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        root.right.left = new TreeNode(6);
        root.right.right = new TreeNode(7);
        root.left.right.left = new TreeNode(8);
        root.left.right.right = new TreeNode(9);
        
        System.out.println("Boundary: " + boundaryOfBinaryTree(root));
        // [1, 2, 4, 8, 9, 6, 7, 3]
    }
}
```

## Complexity Summary

| Traversal | Time | Space | Data Structure |
|-----------|------|-------|---------------|
| Level Order Bottom | O(n) | O(n) | Queue + Stack/Reverse |
| Diagonal | O(n) | O(n) | Queue or HashMap |
| Vertical Order | O(n) | O(n) | Queue + HashMap |
| Vertical (sorted) | O(n log n) | O(n) | Queue + HashMap + Sort |
| Top View | O(n) | O(n) | Queue + TreeMap |
| Bottom View | O(n) | O(n) | Queue + TreeMap |
| Boundary | O(n) | O(n) | Recursion or Stack |

## Practical Insights

1. **Vertical order** is a popular interview topic. The key is tracking column index (root = 0, left = -1, right = +1).
2. **Top view** uses `putIfAbsent` (first node per column), **bottom view** uses `put` (last node per column).
3. **Boundary traversal** is tricky with recursion because the right boundary needs to be reversed.
4. **TreeMap** is useful for column-based traversals (maintains sorted keys). HashMap + min/max tracking is more efficient (O(n) vs O(n log n)).
5. **Diagonal traversal** tests understanding of the geometric interpretation of tree structure. Left moves to next diagonal, right stays on current.
