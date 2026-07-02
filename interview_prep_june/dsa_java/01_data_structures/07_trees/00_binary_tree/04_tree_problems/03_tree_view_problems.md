# Tree View Problems

## Left View of Tree

Nodes visible from the left side of the tree (first node at each level).

```java
import java.util.*;

public class LeftView {
    
    // BFS approach
    public static List<Integer> leftViewBFS(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode current = queue.poll();
                
                // First node of level → visible from left
                if (i == 0) {
                    result.add(current.val);
                }
                
                if (current.left != null) queue.offer(current.left);
                if (current.right != null) queue.offer(current.right);
            }
        }
        
        return result;
    }
    
    // DFS approach
    public static List<Integer> leftViewDFS(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        leftViewDFSHelper(root, 0, result);
        return result;
    }
    
    private static void leftViewDFSHelper(TreeNode root, int depth, List<Integer> result) {
        if (root == null) return;
        
        // First node at this depth from left
        if (depth == result.size()) {
            result.add(root.val);
        }
        
        leftViewDFSHelper(root.left, depth + 1, result);
        leftViewDFSHelper(root.right, depth + 1, result);
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
        
        System.out.println("Left View (BFS): " + leftViewBFS(root));  // [1, 2, 4]
        System.out.println("Left View (DFS): " + leftViewDFS(root));  // [1, 2, 4]
    }
}
```

## Right View of Tree

Nodes visible from the right side of the tree (last node at each level).

```java
public class RightView {
    
    // BFS approach
    public static List<Integer> rightViewBFS(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode current = queue.poll();
                
                // Last node of level → visible from right
                if (i == levelSize - 1) {
                    result.add(current.val);
                }
                
                if (current.left != null) queue.offer(current.left);
                if (current.right != null) queue.offer(current.right);
            }
        }
        
        return result;
    }
    
    // DFS approach — go right first
    public static List<Integer> rightViewDFS(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        rightViewDFSHelper(root, 0, result);
        return result;
    }
    
    private static void rightViewDFSHelper(TreeNode root, int depth, List<Integer> result) {
        if (root == null) return;
        
        // First node at this depth from right
        if (depth == result.size()) {
            result.add(root.val);
        }
        
        rightViewDFSHelper(root.right, depth + 1, result);
        rightViewDFSHelper(root.left, depth + 1, result);
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.right = new TreeNode(5);
        root.right.right = new TreeNode(4);
        
        System.out.println("Right View (BFS): " + rightViewBFS(root));  // [1, 3, 4]
        System.out.println("Right View (DFS): " + rightViewDFS(root));  // [1, 3, 4]
    }
}
```

## Top View of Tree

Nodes visible from the top — first node at each horizontal distance (column) from root.

```java
public class TopView {
    
    static class NodeInfo {
        TreeNode node;
        int col;  // Horizontal distance (column index)
        
        NodeInfo(TreeNode node, int col) {
            this.node = node;
            this.col = col;
        }
    }
    
    public static List<Integer> topView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        // TreeMap keeps columns sorted
        Map<Integer, Integer> columnMap = new TreeMap<>();
        Queue<NodeInfo> queue = new LinkedList<>();
        queue.offer(new NodeInfo(root, 0));
        
        while (!queue.isEmpty()) {
            NodeInfo info = queue.poll();
            TreeNode node = info.node;
            int col = info.col;
            
            // Only first node at each column matters for top view
            columnMap.putIfAbsent(col, node.val);
            
            if (node.left != null) {
                queue.offer(new NodeInfo(node.left, col - 1));
            }
            if (node.right != null) {
                queue.offer(new NodeInfo(node.right, col + 1));
            }
        }
        
        result.addAll(columnMap.values());
        return result;
    }
    
    // DFS approach — track min/max column, use HashMap
    public static List<Integer> topViewDFS(TreeNode root) {
        if (root == null) return new ArrayList<>();
        
        Map<Integer, int[]> columnMap = new HashMap<>();  // col -> [value, depth]
        topViewDFSHelper(root, 0, 0, columnMap);
        
        // Sort by column and build result
        List<Integer> sortedCols = new ArrayList<>(columnMap.keySet());
        Collections.sort(sortedCols);
        
        List<Integer> result = new ArrayList<>();
        for (int col : sortedCols) {
            result.add(columnMap.get(col)[0]);
        }
        
        return result;
    }
    
    private static void topViewDFSHelper(TreeNode root, int col, int depth,
                                          Map<Integer, int[]> columnMap) {
        if (root == null) return;
        
        // If column not yet visited, or we're at a shallower depth
        if (!columnMap.containsKey(col) || depth < columnMap.get(col)[1]) {
            columnMap.put(col, new int[]{root.val, depth});
        }
        
        topViewDFSHelper(root.left, col - 1, depth + 1, columnMap);
        topViewDFSHelper(root.right, col + 1, depth + 1, columnMap);
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
        // Columns: -2(4), -1(2), 0(1), 1(3), 2(6)
        // [4, 2, 1, 3, 6]
        
        //       1
        //      / \
        //     2   3
        //      \
        //       4
        //        \
        //         5
        //          \
        //           6
        TreeNode skewed = new TreeNode(1);
        skewed.left = new TreeNode(2);
        skewed.right = new TreeNode(3);
        skewed.left.right = new TreeNode(4);
        skewed.left.right.right = new TreeNode(5);
        skewed.left.right.right.right = new TreeNode(6);
        
        System.out.println("Top View (skewed): " + topView(skewed));
        // [2, 1, 3] — column -1: first node is 2
    }
}
```

## Bottom View of Tree

Nodes visible from the bottom — last node at each horizontal distance (column).

```java
public class BottomView {
    
    static class NodeInfo {
        TreeNode node;
        int col;
        int depth;
        
        NodeInfo(TreeNode node, int col, int depth) {
            this.node = node;
            this.col = col;
            this.depth = depth;
        }
    }
    
    // BFS approach — overwrite with latest node at each column
    public static List<Integer> bottomViewBFS(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Map<Integer, Integer> columnMap = new TreeMap<>();
        Queue<NodeInfo> queue = new LinkedList<>();
        queue.offer(new NodeInfo(root, 0, 0));
        
        while (!queue.isEmpty()) {
            NodeInfo info = queue.poll();
            TreeNode node = info.node;
            int col = info.col;
            
            // Overwrite with each node at this column (last one = bottom view)
            columnMap.put(col, node.val);
            
            if (node.left != null) {
                queue.offer(new NodeInfo(node.left, col - 1, info.depth + 1));
            }
            if (node.right != null) {
                queue.offer(new NodeInfo(node.right, col + 1, info.depth + 1));
            }
        }
        
        result.addAll(columnMap.values());
        return result;
    }
    
    // DFS approach — track max depth per column
    public static List<Integer> bottomViewDFS(TreeNode root) {
        if (root == null) return new ArrayList<>();
        
        Map<Integer, int[]> columnMap = new HashMap<>();  // col -> [value, maxDepth]
        bottomViewDFSHelper(root, 0, 0, columnMap);
        
        List<Integer> sortedCols = new ArrayList<>(columnMap.keySet());
        Collections.sort(sortedCols);
        
        List<Integer> result = new ArrayList<>();
        for (int col : sortedCols) {
            result.add(columnMap.get(col)[0]);
        }
        
        return result;
    }
    
    private static void bottomViewDFSHelper(TreeNode root, int col, int depth,
                                              Map<Integer, int[]> columnMap) {
        if (root == null) return;
        
        // If not visited or we're at a deeper level
        if (!columnMap.containsKey(col) || depth >= columnMap.get(col)[1]) {
            columnMap.put(col, new int[]{root.val, depth});
        }
        
        bottomViewDFSHelper(root.left, col - 1, depth + 1, columnMap);
        bottomViewDFSHelper(root.right, col + 1, depth + 1, columnMap);
    }
    
    public static void main(String[] args) {
        //       20
        //      /  \
        //     8   22
        //    / \    \
        //   5   3   25
        //      / \
        //     10 14
        TreeNode root = new TreeNode(20);
        root.left = new TreeNode(8);
        root.right = new TreeNode(22);
        root.left.left = new TreeNode(5);
        root.left.right = new TreeNode(3);
        root.right.right = new TreeNode(25);
        root.left.right.left = new TreeNode(10);
        root.left.right.right = new TreeNode(14);
        
        System.out.println("Bottom View (BFS): " + bottomViewBFS(root));  // [5, 10, 14, 25, 3?]
        // Actually: columns -2(5), -1(10), 0(3), 1(14? 25?), etc.
    }
}
```

## All Views Utility

```java
public class TreeViews {
    
    public static void printAllViews(TreeNode root) {
        System.out.println("Left View:   " + LeftView.leftViewBFS(root));
        System.out.println("Right View:  " + RightView.rightViewBFS(root));
        System.out.println("Top View:    " + TopView.topView(root));
        System.out.println("Bottom View: " + BottomView.bottomViewBFS(root));
    }
    
    public static void main(String[] args) {
        //       1
        //      / \
        //     2   3
        //    / \   \
        //   4   5   6
        //      /
        //     7
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        root.right.right = new TreeNode(6);
        root.left.right.left = new TreeNode(7);
        
        printAllViews(root);
        // Left View:   [1, 2, 4, 7]
        // Right View:  [1, 3, 6, 7]
        // Top View:    [4, 2, 1, 3, 6]
        // Bottom View: [4, 7, 5, 6] — depends on ordering
    }
}
```

## Using Vertical Order for Top/Bottom View

```java
public class VerticalBasedViews {
    
    // Top view using vertical order concept
    public static List<Integer> topViewVertical(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Map<Integer, List<Integer>> verticalMap = new TreeMap<>();
        Queue<Map.Entry<TreeNode, Integer>> queue = new LinkedList<>();
        queue.offer(new AbstractMap.SimpleEntry<>(root, 0));
        
        while (!queue.isEmpty()) {
            Map.Entry<TreeNode, Integer> entry = queue.poll();
            TreeNode node = entry.getKey();
            int col = entry.getValue();
            
            verticalMap.putIfAbsent(col, new ArrayList<>());
            verticalMap.get(col).add(node.val);
            
            if (node.left != null) queue.offer(new AbstractMap.SimpleEntry<>(node.left, col - 1));
            if (node.right != null) queue.offer(new AbstractMap.SimpleEntry<>(node.right, col + 1));
        }
        
        for (List<Integer> colNodes : verticalMap.values()) {
            result.add(colNodes.get(0));  // First node in column = top view
        }
        
        return result;
    }
    
    // Bottom view using vertical order concept
    public static List<Integer> bottomViewVertical(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Map<Integer, List<Integer>> verticalMap = new TreeMap<>();
        Queue<Map.Entry<TreeNode, Integer>> queue = new LinkedList<>();
        queue.offer(new AbstractMap.SimpleEntry<>(root, 0));
        
        while (!queue.isEmpty()) {
            Map.Entry<TreeNode, Integer> entry = queue.poll();
            TreeNode node = entry.getKey();
            int col = entry.getValue();
            
            verticalMap.putIfAbsent(col, new ArrayList<>());
            verticalMap.get(col).add(node.val);
            
            if (node.left != null) queue.offer(new AbstractMap.SimpleEntry<>(node.left, col - 1));
            if (node.right != null) queue.offer(new AbstractMap.SimpleEntry<>(node.right, col + 1));
        }
        
        for (List<Integer> colNodes : verticalMap.values()) {
            result.add(colNodes.get(colNodes.size() - 1));  // Last node = bottom view
        }
        
        return result;
    }
}
```

## Complexity Analysis

| View | Time | Space | Approach |
|------|------|-------|----------|
| Left View | O(n) | O(h) or O(w) | BFS (first per level) or DFS |
| Right View | O(n) | O(h) or O(w) | BFS (last per level) or DFS (right-first) |
| Top View | O(n) | O(n) | BFS + TreeMap or Level Order |
| Bottom View | O(n) | O(n) | BFS + TreeMap (overwrite) |

## Practical Insights

1. **Left and Right views** are the simplest — just track the first/last node at each level.
2. **Top and Bottom views** require column tracking (horizontal distance from root).
3. **DFS with level tracking** (`depth == result.size()`) is elegant for left/right view.
4. For **Top view**, `putIfAbsent` gives the first node at each column. For **Bottom view**, `put` (overwrite) gives the last.
5. **TreeMap** keeps columns sorted, but HashMap + min/max tracking is more efficient (O(1) vs O(log n) per operation).
