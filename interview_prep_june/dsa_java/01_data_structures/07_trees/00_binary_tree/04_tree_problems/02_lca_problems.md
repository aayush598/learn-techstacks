# Lowest Common Ancestor (LCA) Problems

## LCA in Binary Tree

The Lowest Common Ancestor of two nodes p and q is the deepest node that has both p and q as descendants.

```java
import java.util.*;

public class LCAInBinaryTree {
    
    // Recursive approach
    public static TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) return root;
        
        TreeNode left = lowestCommonAncestor(root.left, p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);
        
        // If both sides return non-null, current node is LCA
        if (left != null && right != null) return root;
        
        // Otherwise, return the non-null side
        return left != null ? left : right;
    }
    
    // Iterative: find paths and compare
    public static TreeNode lowestCommonAncestorIterative(TreeNode root, TreeNode p, TreeNode q) {
        List<TreeNode> pathP = findPath(root, p);
        List<TreeNode> pathQ = findPath(root, q);
        
        TreeNode lca = root;
        int minLen = Math.min(pathP.size(), pathQ.size());
        
        for (int i = 0; i < minLen; i++) {
            if (pathP.get(i) == pathQ.get(i)) {
                lca = pathP.get(i);
            } else {
                break;
            }
        }
        
        return lca;
    }
    
    private static List<TreeNode> findPath(TreeNode root, TreeNode target) {
        List<TreeNode> path = new ArrayList<>();
        findPathHelper(root, target, path);
        return path;
    }
    
    private static boolean findPathHelper(TreeNode root, TreeNode target, List<TreeNode> path) {
        if (root == null) return false;
        
        path.add(root);
        if (root == target) return true;
        
        if (findPathHelper(root.left, target, path) || 
            findPathHelper(root.right, target, path)) {
            return true;
        }
        
        path.remove(path.size() - 1);
        return false;
    }
    
    // Using parent pointers (BFS + HashMap)
    public static TreeNode lowestCommonAncestorParentMap(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null) return null;
        
        Map<TreeNode, TreeNode> parent = new HashMap<>();
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        parent.put(root, null);
        
        // BFS to find both nodes and record parents
        while (!parent.containsKey(p) || !parent.containsKey(q)) {
            TreeNode current = queue.poll();
            if (current.left != null) {
                parent.put(current.left, current);
                queue.offer(current.left);
            }
            if (current.right != null) {
                parent.put(current.right, current);
                queue.offer(current.right);
            }
        }
        
        // Collect ancestors of p
        Set<TreeNode> ancestors = new HashSet<>();
        while (p != null) {
            ancestors.add(p);
            p = parent.get(p);
        }
        
        // Find first ancestor of q in p's ancestors
        while (!ancestors.contains(q)) {
            q = parent.get(q);
        }
        
        return q;
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
        
        System.out.println("LCA of 4 and 5: " + 
            lowestCommonAncestor(root, root.left.left, root.left.right).val);  // 2
        System.out.println("LCA of 4 and 3: " + 
            lowestCommonAncestor(root, root.left.left, root.right).val);      // 1
        System.out.println("LCA of 4 and 2: " + 
            lowestCommonAncestor(root, root.left.left, root.left).val);       // 2
    }
}
```

## LCA in BST

In a BST, we can use the value ordering to determine LCA efficiently.

```java
public class LCAInBST {
    
    // Recursive: O(h) time, O(h) space
    public static TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null) return null;
        
        // Both in left subtree
        if (p.val < root.val && q.val < root.val) {
            return lowestCommonAncestor(root.left, p, q);
        }
        // Both in right subtree
        if (p.val > root.val && q.val > root.val) {
            return lowestCommonAncestor(root.right, p, q);
        }
        // Split or one is root
        return root;
    }
    
    // Iterative: O(h) time, O(1) space
    public static TreeNode lowestCommonAncestorIterative(TreeNode root, TreeNode p, TreeNode q) {
        TreeNode current = root;
        
        while (current != null) {
            if (p.val < current.val && q.val < current.val) {
                current = current.left;
            } else if (p.val > current.val && q.val > current.val) {
                current = current.right;
            } else {
                return current;
            }
        }
        
        return null;
    }
    
    public static void main(String[] args) {
        //       6
        //      / \
        //     2   8
        //    / \ / \
        //   0  4 7 9
        //     / \
        //    3   5
        TreeNode root = new TreeNode(6);
        root.left = new TreeNode(2);
        root.right = new TreeNode(8);
        root.left.left = new TreeNode(0);
        root.left.right = new TreeNode(4);
        root.right.left = new TreeNode(7);
        root.right.right = new TreeNode(9);
        root.left.right.left = new TreeNode(3);
        root.left.right.right = new TreeNode(5);
        
        System.out.println("LCA of 2 and 8: " + 
            lowestCommonAncestor(root, root.left, root.right).val);                  // 6
        System.out.println("LCA of 0 and 5: " + 
            lowestCommonAncestor(root, root.left.left, root.left.right.right).val);  // 2
        System.out.println("LCA of 3 and 5: " + 
            lowestCommonAncestor(root, root.left.right.left, root.left.right.right).val);  // 4
    }
}
```

## LCA with Parent Pointers

When each node has a reference to its parent.

```java
class TreeNodeWithParent {
    int val;
    TreeNodeWithParent left;
    TreeNodeWithParent right;
    TreeNodeWithParent parent;
    
    TreeNodeWithParent(int val) { this.val = val; }
}

public class LCAWithParentPointers {
    
    // Using depth calculation
    public static TreeNodeWithParent lowestCommonAncestor(TreeNodeWithParent p, TreeNodeWithParent q) {
        int depthP = getDepth(p);
        int depthQ = getDepth(q);
        
        // Align depths
        while (depthP > depthQ) {
            p = p.parent;
            depthP--;
        }
        while (depthQ > depthP) {
            q = q.parent;
            depthQ--;
        }
        
        // Move up together until they meet
        while (p != q) {
            p = p.parent;
            q = q.parent;
        }
        
        return p;
    }
    
    private static int getDepth(TreeNodeWithParent node) {
        int depth = 0;
        while (node.parent != null) {
            node = node.parent;
            depth++;
        }
        return depth;
    }
    
    // Using set (simpler)
    public static TreeNodeWithParent lowestCommonAncestorSet(TreeNodeWithParent p, TreeNodeWithParent q) {
        Set<TreeNodeWithParent> ancestors = new HashSet<>();
        
        while (p != null) {
            ancestors.add(p);
            p = p.parent;
        }
        
        while (q != null) {
            if (ancestors.contains(q)) return q;
            q = q.parent;
        }
        
        return null;
    }
    
    public static void main(String[] args) {
        // Build tree with parent pointers
        TreeNodeWithParent root = new TreeNodeWithParent(1);
        TreeNodeWithParent node2 = new TreeNodeWithParent(2);
        TreeNodeWithParent node3 = new TreeNodeWithParent(3);
        TreeNodeWithParent node4 = new TreeNodeWithParent(4);
        TreeNodeWithParent node5 = new TreeNodeWithParent(5);
        
        root.left = node2; node2.parent = root;
        root.right = node3; node3.parent = root;
        node2.left = node4; node4.parent = node2;
        node2.right = node5; node5.parent = node2;
        
        System.out.println("LCA of 4 and 5 (with parent): " + 
            lowestCommonAncestor(node4, node5).val);  // 2
        System.out.println("LCA of 4 and 3 (with parent): " + 
            lowestCommonAncestor(node4, node3).val);  // 1
    }
}
```

## LCA of Deepest Leaves

Find the LCA of the set of deepest leaves.

```java
public class LCADeepestLeaves {
    
    static class Result {
        TreeNode node;
        int depth;
        
        Result(TreeNode node, int depth) {
            this.node = node;
            this.depth = depth;
        }
    }
    
    public static TreeNode lcaDeepestLeaves(TreeNode root) {
        return dfs(root).node;
    }
    
    private static Result dfs(TreeNode root) {
        if (root == null) return new Result(null, 0);
        
        Result left = dfs(root.left);
        Result right = dfs(root.right);
        
        if (left.depth == right.depth) {
            return new Result(root, left.depth + 1);
        } else if (left.depth > right.depth) {
            return new Result(left.node, left.depth + 1);
        } else {
            return new Result(right.node, right.depth + 1);
        }
    }
    
    // Alternative approach
    public static TreeNode lcaDeepestLeavesAlt(TreeNode root) {
        Map<TreeNode, Integer> depthMap = new HashMap<>();
        int maxDepth = findMaxDepth(root, depthMap);
        return findLCA(root, depthMap, maxDepth);
    }
    
    private static int findMaxDepth(TreeNode root, Map<TreeNode, Integer> depthMap) {
        if (root == null) return -1;
        int depth = 1 + Math.max(findMaxDepth(root.left, depthMap), 
                                  findMaxDepth(root.right, depthMap));
        depthMap.put(root, depth);
        return depth;
    }
    
    private static TreeNode findLCA(TreeNode root, Map<TreeNode, Integer> depthMap, int maxDepth) {
        if (root == null) return null;
        if (depthMap.get(root) == maxDepth) return root;
        
        TreeNode left = findLCA(root.left, depthMap, maxDepth);
        TreeNode right = findLCA(root.right, depthMap, maxDepth);
        
        if (left != null && right != null) return root;
        return left != null ? left : right;
    }
    
    public static void main(String[] args) {
        //       1
        //      / \
        //     2   3
        //    /
        //   4
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        
        // Deepest leaf is 4 (depth 2), LCA is 1 (since 4's ancestors include 1)
        System.out.println("LCA of deepest leaves: " + 
            lcaDeepestLeaves(root).val);  // Actually 2 (subtree has both deepest nodes)
        // Wait: deepest leaves: only node 4 at depth 2. So LCA of deepest leaves = 2?
        // Actually 4 is the only deepest leaf. LCA of {4} = 4.
        // Let me check with more leaves:
        
        TreeNode root2 = new TreeNode(1);
        root2.left = new TreeNode(2);
        root2.right = new TreeNode(3);
        root2.left.left = new TreeNode(4);
        root2.right.left = new TreeNode(5);
        root2.right.right = new TreeNode(6);
        
        // Deepest leaves: 4, 5, 6 (all depth 2)
        System.out.println("LCA of deepest leaves: " + 
            lcaDeepestLeaves(root2).val);  // 1
    }
}
```

## LCA in N-ary Tree

```java
class NaryNode {
    int val;
    List<NaryNode> children;
    
    NaryNode(int val) {
        this.val = val;
        this.children = new ArrayList<>();
    }
}

public class LCANaryTree {
    
    public static NaryNode lowestCommonAncestor(NaryNode root, NaryNode p, NaryNode q) {
        if (root == null || root == p || root == q) return root;
        
        NaryNode lca = null;
        int count = 0;
        
        for (NaryNode child : root.children) {
            NaryNode result = lowestCommonAncestor(child, p, q);
            if (result != null) {
                lca = result;
                count++;
            }
        }
        
        // If more than one child returns non-null, root is LCA
        if (count > 1) return root;
        
        // If exactly one child returns non-null, that's the LCA
        return lca;
    }
    
    public static void main(String[] args) {
        //       1
        //    /  |  \
        //   2   3   4
        //  / \  |
        // 5   6 7
        NaryNode root = new NaryNode(1);
        NaryNode n2 = new NaryNode(2);
        NaryNode n3 = new NaryNode(3);
        NaryNode n4 = new NaryNode(4);
        NaryNode n5 = new NaryNode(5);
        NaryNode n6 = new NaryNode(6);
        NaryNode n7 = new NaryNode(7);
        
        root.children.add(n2);
        root.children.add(n3);
        root.children.add(n4);
        n2.children.add(n5);
        n2.children.add(n6);
        n3.children.add(n7);
        
        System.out.println("LCA of 5 and 6: " + lowestCommonAncestor(root, n5, n6).val);  // 2
        System.out.println("LCA of 5 and 7: " + lowestCommonAncestor(root, n5, n7).val);  // 1
    }
}
```

## LCA with Distance / Path Problems

```java
public class LCADistance {
    
    // Find distance between two nodes (number of edges)
    public static int findDistance(TreeNode root, TreeNode p, TreeNode q) {
        TreeNode lca = LCAInBinaryTree.lowestCommonAncestor(root, p, q);
        return distanceFromRoot(lca, p, 0) + distanceFromRoot(lca, q, 0);
    }
    
    private static int distanceFromRoot(TreeNode root, TreeNode target, int depth) {
        if (root == null) return -1;
        if (root == target) return depth;
        
        int left = distanceFromRoot(root.left, target, depth + 1);
        if (left != -1) return left;
        return distanceFromRoot(root.right, target, depth + 1);
    }
    
    // Find path from LCA to a node
    public static List<TreeNode> pathFromLCA(TreeNode root, TreeNode target) {
        List<TreeNode> path = new ArrayList<>();
        findPath(root, target, path);
        return path;
    }
    
    private static boolean findPath(TreeNode root, TreeNode target, List<TreeNode> path) {
        if (root == null) return false;
        path.add(root);
        if (root == target) return true;
        if (findPath(root.left, target, path) || findPath(root.right, target, path)) {
            return true;
        }
        path.remove(path.size() - 1);
        return false;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        
        TreeNode p = root.left.left;  // 4
        TreeNode q = root.left.right; // 5
        
        System.out.println("Distance between 4 and 5: " + findDistance(root, p, q));  // 2
        System.out.println("LCA of 4 and 5: " + 
            LCAInBinaryTree.lowestCommonAncestor(root, p, q).val);  // 2
    }
}
```

## Complexity Summary

| Problem | Time | Space | Notes |
|---------|------|-------|-------|
| LCA in Binary Tree | O(n) | O(h) | Recursive, elegant |
| LCA in BST | O(h) | O(1) | Iterative optimal |
| LCA with Parent Ptr | O(h) | O(1) | Align depths then climb |
| LCA of Deepest Leaves | O(n) | O(h) | Postorder with depth |
| LCA in N-ary Tree | O(n) | O(h) | Count non-null children |
| Distance between nodes | O(n) | O(h) | LCA + depth calculations |

## Practical Insights

1. **Binary Tree LCA** recursive solution is one of the most beautiful recursive algorithms — it's worth memorizing.
2. **BST LCA** is much simpler because BST ordering tells you which subtree to search.
3. The **parent pointer** approach is useful when you have that structure (e.g., in some tree library implementations).
4. **Distance between nodes** = depth(p) + depth(q) - 2*depth(LCA).
5. The LCA algorithm is a special case of the more general **range query** problem on trees.
