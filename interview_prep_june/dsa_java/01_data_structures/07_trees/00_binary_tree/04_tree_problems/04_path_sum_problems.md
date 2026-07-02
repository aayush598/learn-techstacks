# Path Sum Problems

## Path Sum (Root to Leaf)

Check if there exists a root-to-leaf path with sum equal to target.

```java
import java.util.*;

public class PathSum {
    
    public static boolean hasPathSum(TreeNode root, int targetSum) {
        if (root == null) return false;
        
        // Leaf node: check if remaining sum equals node value
        if (root.left == null && root.right == null) {
            return targetSum == root.val;
        }
        
        return hasPathSum(root.left, targetSum - root.val) ||
               hasPathSum(root.right, targetSum - root.val);
    }
    
    // Iterative DFS with stack
    public static boolean hasPathSumIterative(TreeNode root, int targetSum) {
        if (root == null) return false;
        
        Stack<TreeNode> nodeStack = new Stack<>();
        Stack<Integer> sumStack = new Stack<>();
        nodeStack.push(root);
        sumStack.push(targetSum - root.val);
        
        while (!nodeStack.isEmpty()) {
            TreeNode node = nodeStack.pop();
            int remainingSum = sumStack.pop();
            
            if (node.left == null && node.right == null && remainingSum == 0) {
                return true;
            }
            
            if (node.right != null) {
                nodeStack.push(node.right);
                sumStack.push(remainingSum - node.right.val);
            }
            if (node.left != null) {
                nodeStack.push(node.left);
                sumStack.push(remainingSum - node.left.val);
            }
        }
        
        return false;
    }
    
    public static void main(String[] args) {
        //       5
        //      / \
        //     4   8
        //    /   / \
        //   11  13  4
        //  /  \      \
        // 7    2      1
        TreeNode root = new TreeNode(5);
        root.left = new TreeNode(4);
        root.right = new TreeNode(8);
        root.left.left = new TreeNode(11);
        root.right.left = new TreeNode(13);
        root.right.right = new TreeNode(4);
        root.left.left.left = new TreeNode(7);
        root.left.left.right = new TreeNode(2);
        root.right.right.right = new TreeNode(1);
        
        System.out.println("Has sum 22: " + hasPathSum(root, 22));  // true (5→4→11→2)
        System.out.println("Has sum 26: " + hasPathSum(root, 26));  // true (5→8→13)
    }
}
```

## Path Sum II (All Root-to-Leaf Paths)

Find all root-to-leaf paths with sum equal to target.

```java
public class PathSumII {
    
    public static List<List<Integer>> pathSum(TreeNode root, int targetSum) {
        List<List<Integer>> result = new ArrayList<>();
        List<Integer> currentPath = new ArrayList<>();
        findPaths(root, targetSum, currentPath, result);
        return result;
    }
    
    private static void findPaths(TreeNode root, int remainingSum,
                                   List<Integer> currentPath, List<List<Integer>> result) {
        if (root == null) return;
        
        currentPath.add(root.val);
        
        if (root.left == null && root.right == null && remainingSum == root.val) {
            result.add(new ArrayList<>(currentPath));  // Deep copy
        } else {
            findPaths(root.left, remainingSum - root.val, currentPath, result);
            findPaths(root.right, remainingSum - root.val, currentPath, result);
        }
        
        currentPath.remove(currentPath.size() - 1);  // Backtrack
    }
    
    // Iterative DFS
    public static List<List<Integer>> pathSumIterative(TreeNode root, int targetSum) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        
        Stack<TreeNode> nodeStack = new Stack<>();
        Stack<List<Integer>> pathStack = new Stack<>();
        Stack<Integer> sumStack = new Stack<>();
        
        nodeStack.push(root);
        pathStack.push(new ArrayList<>(Arrays.asList(root.val)));
        sumStack.push(root.val);
        
        while (!nodeStack.isEmpty()) {
            TreeNode node = nodeStack.pop();
            List<Integer> path = pathStack.pop();
            int currentSum = sumStack.pop();
            
            if (node.left == null && node.right == null && currentSum == targetSum) {
                result.add(path);
            }
            
            if (node.right != null) {
                nodeStack.push(node.right);
                List<Integer> newPath = new ArrayList<>(path);
                newPath.add(node.right.val);
                pathStack.push(newPath);
                sumStack.push(currentSum + node.right.val);
            }
            if (node.left != null) {
                nodeStack.push(node.left);
                List<Integer> newPath = new ArrayList<>(path);
                newPath.add(node.left.val);
                pathStack.push(newPath);
                sumStack.push(currentSum + node.left.val);
            }
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(5);
        root.left = new TreeNode(4);
        root.right = new TreeNode(8);
        root.left.left = new TreeNode(11);
        root.right.left = new TreeNode(13);
        root.right.right = new TreeNode(4);
        root.left.left.left = new TreeNode(7);
        root.left.left.right = new TreeNode(2);
        root.right.right.left = new TreeNode(5);
        root.right.right.right = new TreeNode(1);
        
        System.out.println("Paths with sum 22: " + pathSum(root, 22));
        // [[5, 4, 11, 2], [5, 8, 4, 5]]
    }
}
```

## Path Sum III (Any Path, Not Necessarily Root/Leaf)

Count paths that sum to target where paths can start and end anywhere but must go downwards.

```java
public class PathSumIII {
    
    // O(n²) approach — DFS from each node
    public static int pathSumNaive(TreeNode root, int targetSum) {
        if (root == null) return 0;
        
        int fromRoot = countPathsFromNode(root, targetSum, 0);
        int left = pathSumNaive(root.left, targetSum);
        int right = pathSumNaive(root.right, targetSum);
        
        return fromRoot + left + right;
    }
    
    private static int countPathsFromNode(TreeNode root, int targetSum, long currentSum) {
        if (root == null) return 0;
        
        currentSum += root.val;
        int count = (currentSum == targetSum) ? 1 : 0;
        
        count += countPathsFromNode(root.left, targetSum, currentSum);
        count += countPathsFromNode(root.right, targetSum, currentSum);
        
        return count;
    }
    
    // O(n) approach — prefix sum + HashMap
    public static int pathSum(TreeNode root, int targetSum) {
        Map<Long, Integer> prefixSumCount = new HashMap<>();
        prefixSumCount.put(0L, 1);  // Base case: empty path
        return countPaths(root, 0, targetSum, prefixSumCount);
    }
    
    private static int countPaths(TreeNode root, long currentSum, int targetSum,
                                   Map<Long, Integer> prefixSumCount) {
        if (root == null) return 0;
        
        currentSum += root.val;
        
        // Number of paths ending at current node that sum to target
        int count = prefixSumCount.getOrDefault(currentSum - targetSum, 0);
        
        // Add current sum to map
        prefixSumCount.put(currentSum, prefixSumCount.getOrDefault(currentSum, 0) + 1);
        
        // Recurse
        count += countPaths(root.left, currentSum, targetSum, prefixSumCount);
        count += countPaths(root.right, currentSum, targetSum, prefixSumCount);
        
        // Backtrack — remove current sum for sibling subtrees
        prefixSumCount.put(currentSum, prefixSumCount.get(currentSum) - 1);
        
        return count;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(10);
        root.left = new TreeNode(5);
        root.right = new TreeNode(-3);
        root.left.left = new TreeNode(3);
        root.left.right = new TreeNode(2);
        root.right.right = new TreeNode(11);
        root.left.left.left = new TreeNode(3);
        root.left.left.right = new TreeNode(-2);
        root.left.right.right = new TreeNode(1);
        
        System.out.println("Paths with sum 8: " + pathSum(root, 8));
        // 3 paths: 5→3, 5→2→1, -3→11
    }
}
```

## Maximum Path Sum (Any Node to Any Node)

Find the maximum path sum where path can start and end at any node.

```java
public class MaxPathSum {
    
    private static int maxSum = Integer.MIN_VALUE;
    
    public static int maxPathSum(TreeNode root) {
        maxSum = Integer.MIN_VALUE;
        calculateMaxGain(root);
        return maxSum;
    }
    
    // Returns maximum sum of a path starting at this node going downward
    private static int calculateMaxGain(TreeNode root) {
        if (root == null) return 0;
        
        // Max sum of path going left (only take positive contributions)
        int leftGain = Math.max(calculateMaxGain(root.left), 0);
        // Max sum of path going right
        int rightGain = Math.max(calculateMaxGain(root.right), 0);
        
        // Path that goes through this node (left + node + right)
        int currentMaxPath = root.val + leftGain + rightGain;
        
        // Update global maximum
        maxSum = Math.max(maxSum, currentMaxPath);
        
        // Return max gain from this node going down (can only take one branch)
        return root.val + Math.max(leftGain, rightGain);
    }
    
    // Using a result class
    static class Result {
        int maxSum;
        
        Result() {
            maxSum = Integer.MIN_VALUE;
        }
    }
    
    public static int maxPathSumAlt(TreeNode root) {
        Result result = new Result();
        calculateMaxGainAlt(root, result);
        return result.maxSum;
    }
    
    private static int calculateMaxGainAlt(TreeNode root, Result result) {
        if (root == null) return 0;
        
        int left = Math.max(calculateMaxGainAlt(root.left, result), 0);
        int right = Math.max(calculateMaxGainAlt(root.right, result), 0);
        
        result.maxSum = Math.max(result.maxSum, root.val + left + right);
        
        return root.val + Math.max(left, right);
    }
    
    public static void main(String[] args) {
        //      -10
        //      /  \
        //     9    20
        //         /  \
        //        15   7
        TreeNode root = new TreeNode(-10);
        root.left = new TreeNode(9);
        root.right = new TreeNode(20);
        root.right.left = new TreeNode(15);
        root.right.right = new TreeNode(7);
        
        System.out.println("Max Path Sum: " + maxPathSum(root));  // 42 (15→20→7)
        
        // All negative
        TreeNode allNeg = new TreeNode(-3);
        allNeg.left = new TreeNode(-5);
        allNeg.right = new TreeNode(-2);
        
        System.out.println("Max Path Sum (negatives): " + maxPathSum(allNeg));  // -2 (single node)
    }
}
```

## Root to Leaf Path with Target Sum

Return the path (or just check existence).

```java
public class RootToLeafPath {
    
    public static List<Integer> getPath(TreeNode root, int targetSum) {
        List<Integer> path = new ArrayList<>();
        if (findPath(root, targetSum, path)) {
            return path;
        }
        return new ArrayList<>();  // No path found
    }
    
    private static boolean findPath(TreeNode root, int remainingSum, List<Integer> path) {
        if (root == null) return false;
        
        path.add(root.val);
        
        if (root.left == null && root.right == null && remainingSum == root.val) {
            return true;
        }
        
        if (findPath(root.left, remainingSum - root.val, path) ||
            findPath(root.right, remainingSum - root.val, path)) {
            return true;
        }
        
        path.remove(path.size() - 1);
        return false;
    }
    
    // Find path with maximum sum (root to leaf)
    public static List<Integer> maxSumPath(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        List<Integer> currentPath = new ArrayList<>();
        int[] maxSum = {Integer.MIN_VALUE};
        findMaxSumPath(root, 0, currentPath, maxSum, result);
        return result;
    }
    
    private static void findMaxSumPath(TreeNode root, int currentSum,
                                        List<Integer> currentPath, int[] maxSum,
                                        List<Integer> result) {
        if (root == null) return;
        
        currentPath.add(root.val);
        currentSum += root.val;
        
        if (root.left == null && root.right == null) {
            if (currentSum > maxSum[0]) {
                maxSum[0] = currentSum;
                result.clear();
                result.addAll(currentPath);
            }
        } else {
            findMaxSumPath(root.left, currentSum, currentPath, maxSum, result);
            findMaxSumPath(root.right, currentSum, currentPath, maxSum, result);
        }
        
        currentPath.remove(currentPath.size() - 1);
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(5);
        root.left = new TreeNode(4);
        root.right = new TreeNode(8);
        root.left.left = new TreeNode(11);
        root.right.left = new TreeNode(13);
        root.right.right = new TreeNode(4);
        root.left.left.left = new TreeNode(7);
        root.left.left.right = new TreeNode(2);
        
        System.out.println("Path to sum 22: " + getPath(root, 22));   // [5, 4, 11, 2]
        System.out.println("Max sum path: " + maxSumPath(root));      // [5, 8, 13] sum=26
    }
}
```

## Root to Leaf Numbers (Sum of All Numbers)

Each root-to-leaf path forms a number. Return sum of all such numbers.

```java
public class SumRootToLeaf {
    
    public static int sumNumbers(TreeNode root) {
        return calculateSum(root, 0);
    }
    
    private static int calculateSum(TreeNode root, int currentNumber) {
        if (root == null) return 0;
        
        currentNumber = currentNumber * 10 + root.val;
        
        if (root.left == null && root.right == null) {
            return currentNumber;
        }
        
        return calculateSum(root.left, currentNumber) +
               calculateSum(root.right, currentNumber);
    }
    
    // Iterative
    public static int sumNumbersIterative(TreeNode root) {
        if (root == null) return 0;
        
        Stack<TreeNode> nodeStack = new Stack<>();
        Stack<Integer> numStack = new Stack<>();
        nodeStack.push(root);
        numStack.push(root.val);
        int totalSum = 0;
        
        while (!nodeStack.isEmpty()) {
            TreeNode node = nodeStack.pop();
            int currentNum = numStack.pop();
            
            if (node.left == null && node.right == null) {
                totalSum += currentNum;
            }
            
            if (node.right != null) {
                nodeStack.push(node.right);
                numStack.push(currentNum * 10 + node.right.val);
            }
            if (node.left != null) {
                nodeStack.push(node.left);
                numStack.push(currentNum * 10 + node.left.val);
            }
        }
        
        return totalSum;
    }
    
    public static void main(String[] args) {
        //    1
        //   / \
        //  2   3
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        
        System.out.println("Sum of root-to-leaf numbers: " + sumNumbers(root));  // 12 + 13 = 25
    }
}
```

## Binary Tree Maximum Path Sum Between Leaves

```java
public class MaxPathSumLeaves {
    
    private static int maxLeafToLeaf = Integer.MIN_VALUE;
    
    public static int maxPathSumLeaves(TreeNode root) {
        maxLeafToLeaf = Integer.MIN_VALUE;
        calculateLeafToLeaf(root);
        return maxLeafToLeaf;
    }
    
    private static int calculateLeafToLeaf(TreeNode root) {
        if (root == null) return Integer.MIN_VALUE;
        
        // Leaf node
        if (root.left == null && root.right == null) {
            return root.val;
        }
        
        int left = calculateLeafToLeaf(root.left);
        int right = calculateLeafToLeaf(root.right);
        
        // If both children exist, consider path through root
        if (root.left != null && root.right != null) {
            maxLeafToLeaf = Math.max(maxLeafToLeaf, left + right + root.val);
        }
        
        // Return max path from this node to a leaf
        if (root.left == null) return right + root.val;
        if (root.right == null) return left + root.val;
        return Math.max(left, right) + root.val;
    }
    
    public static void main(String[] args) {
        //      -15
        //      /  \
        //     5    6
        //    / \  / \
        //  -8  1 3  9
        //  / \
        // 2   6
        TreeNode root = new TreeNode(-15);
        root.left = new TreeNode(5);
        root.right = new TreeNode(6);
        root.left.left = new TreeNode(-8);
        root.left.right = new TreeNode(1);
        root.right.left = new TreeNode(3);
        root.right.right = new TreeNode(9);
        root.left.left.left = new TreeNode(2);
        root.left.left.right = new TreeNode(6);
        
        System.out.println("Max leaf-to-leaf path sum: " + maxPathSumLeaves(root));
        // 2→(-8)→5→6→3 = 8? or 6→(-8)→5→6→9 = 18
    }
}
```

## Complexity Summary

| Problem | Time | Space | Notes |
|---------|------|-------|-------|
| Path Sum (root to leaf) | O(n) | O(h) | Simple recursion |
| Path Sum II (all paths) | O(n²) | O(h) | Copy path at leaf |
| Path Sum III (any path) | O(n) | O(n) | Prefix sum + HashMap |
| Max Path Sum (any node) | O(n) | O(h) | Postorder, global var |
| Root to Leaf Numbers | O(n) | O(h) | DFS with number building |

## Practical Insights

1. **Path Sum III** is the hardest — the prefix sum technique is a common pattern in subarray sum problems applied to trees.
2. **Maximum Path Sum** uses the "max gain" concept: at each node, take only positive contributions from children.
3. **Backtracking** is essential for Path Sum II — remove the last element when returning from recursion.
4. The **prefix sum HashMap** in Path Sum III must be backtracked (decrement count) when leaving a subtree.
5. For **maximum path sum between leaves**, the tree must have at least two leaves for a valid path.
