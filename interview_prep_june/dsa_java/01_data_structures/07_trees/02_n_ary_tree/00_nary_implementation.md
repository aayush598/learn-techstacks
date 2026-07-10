# N-ary Tree Implementation

## What is an N-ary Tree?

An N-ary tree is a tree where each node can have **at most N children**. Unlike binary trees (max 2 children), N-ary trees generalize to any branching factor. Think of a file system — a folder can contain any number of subfolders and files.

## When to Use N-ary Trees?

- **File systems**: Directories contain multiple files/subdirectories
- **Organization charts**: A manager has multiple reports
- **DOM tree**: HTML elements contain multiple child elements
- **Parse trees**: Arithmetic expressions, compiler ASTs
- **Trie (prefix tree)**: Each node has up to 26 children (one per letter)

## N-ary Tree Node

```java
import java.util.ArrayList;
import java.util.List;

class NAryNode {
    int val;
    List<NAryNode> children;

    NAryNode(int val) {
        this.val = val;
        this.children = new ArrayList<>();
    }

    NAryNode(int val, List<NAryNode> children) {
        this.val = val;
        this.children = children;
    }
}
```

### Key Observations

- Each node stores a **list of children** instead of left/right pointers
- Children list can be empty (leaf node) or contain up to N nodes
- No need to distinguish between "left" and "right" — children are ordered in the list

## Building an N-ary Tree from a Children List

Given a level-order serialization (like LeetCode's format), build the tree:

```
Input: [1, null, 3, 2, 4, null, 5, 6]
Output tree:
        1
      / | \
     3  2  4
    / \
   5   6
```

```java
import java.util.*;

class NAryTreeBuilder {

    // Build from level-order serialization
    // Null markers separate parent groups
    public static NAryNode buildFromLevelOrder(Integer[] values) {
        if (values == null || values.length == 0 || values[0] == null) {
            return null;
        }

        NAryNode root = new NAryNode(values[0]);
        Queue<NAryNode> queue = new LinkedList<>();
        queue.offer(root);

        int i = 1; // index in values array

        while (!queue.isEmpty() && i < values.length) {
            NAryNode current = queue.poll();

            // Collect all children for current node
            while (i < values.length && values[i] != null) {
                NAryNode child = new NAryNode(values[i]);
                current.children.add(child);
                queue.offer(child);
                i++;
            }

            // Skip the null separator
            if (i < values.length) {
                i++;
            }
        }

        return root;
    }

    // Build manually by specifying children
    public static NAryNode buildManually() {
        NAryNode node5 = new NAryNode(5);
        NAryNode node6 = new NAryNode(6);

        NAryNode node3 = new NAryNode(3, Arrays.asList(node5, node6));
        NAryNode node2 = new NAryNode(2);
        NAryNode node4 = new NAryNode(4);

        NAryNode root = new NAryNode(1, Arrays.asList(node3, node2, node4));
        return root;
    }
}
```

## Counting Nodes

```java
class NAryTreeOperations {

    // Count total nodes — recursive
    public static int countNodes(NAryNode root) {
        if (root == null) return 0;

        int count = 1; // count this node
        for (NAryNode child : root.children) {
            count += countNodes(child);
        }
        return count;
    }

    // Count nodes iteratively using BFS
    public static int countNodesBFS(NAryNode root) {
        if (root == null) return 0;

        Queue<NAryNode> queue = new LinkedList<>();
        queue.offer(root);
        int count = 0;

        while (!queue.isEmpty()) {
            NAryNode current = queue.poll();
            count++;
            for (NAryNode child : current.children) {
                queue.offer(child);
            }
        }
        return count;
    }

    // Count leaf nodes
    public static int countLeaves(NAryNode root) {
        if (root == null) return 0;
        if (root.children.isEmpty()) return 1;

        int leaves = 0;
        for (NAryNode child : root.children) {
            leaves += countLeaves(child);
        }
        return leaves;
    }

    // Count internal nodes (non-leaf, non-null)
    public static int countInternalNodes(NAryNode root) {
        if (root == null || root.children.isEmpty()) return 0;

        int count = 1;
        for (NAryNode child : root.children) {
            count += countInternalNodes(child);
        }
        return count;
    }
}
```

## Finding Height

```java
class NAryTreeHeight {

    // Height = longest path from root to leaf
    // Single node tree has height 0 (edges) or 1 (nodes)
    // We'll use edge-based height here

    public static int height(NAryNode root) {
        if (root == null) return -1; // edge-based: empty tree is -1
        if (root.children.isEmpty()) return 0;

        int maxHeight = 0;
        for (NAryNode child : root.children) {
            maxHeight = Math.max(maxHeight, height(child));
        }
        return 1 + maxHeight;
    }

    // Height using BFS (level counting)
    public static int heightBFS(NAryNode root) {
        if (root == null) return -1;

        Queue<NAryNode> queue = new LinkedList<>();
        queue.offer(root);
        int levels = -1;

        while (!queue.isEmpty()) {
            int size = queue.size();
            levels++;

            for (int i = 0; i < size; i++) {
                NAryNode current = queue.poll();
                for (NAryNode child : current.children) {
                    queue.offer(child);
                }
            }
        }
        return levels;
    }

    // Depth of a specific node
    public static int depth(NAryNode root, int target) {
        if (root == null) return -1;
        if (root.val == target) return 0;

        for (NAryNode child : root.children) {
            int d = depth(child, target);
            if (d != -1) return 1 + d;
        }
        return -1;
    }
}
```

## Printing the Tree

```java
class NAryTreePrinter {

    // Print tree with indentation (visual representation)
    public static void printTree(NAryNode root) {
        printTreeHelper(root, "", true);
    }

    private static void printTreeHelper(NAryNode node, String prefix, boolean isLast) {
        if (node == null) return;

        System.out.println(prefix + (isLast ? "└── " : "├── ") + node.val);

        String childPrefix = prefix + (isLast ? "    " : "│   ");

        for (int i = 0; i < node.children.size(); i++) {
            printTreeHelper(node.children.get(i), childPrefix,
                          i == node.children.size() - 1);
        }
    }
}
```

## Practice Problem: Max Degree of an N-ary Tree

```java
class MaxDegree {

    // The degree = number of children a node has
    public static int maxDegree(NAryNode root) {
        if (root == null) return 0;

        int max = root.children.size();
        for (NAryNode child : root.children) {
            max = Math.max(max, maxDegree(child));
        }
        return max;
    }
}
```

## Key Takeaways

1. **N-ary trees generalize binary trees** — same traversal logic, just loop over children instead of left/right
2. **ArrayList for children** gives O(1) amortized append, O(1) access by index
3. **BFS is great for level-by-level processing**, recursion is natural for depth-based questions
4. **Serialization format matters** — understand whether nulls are used as separators or not
5. **Edge-based vs node-based height** — clarify which one the problem expects (0 vs 1 for single node)
