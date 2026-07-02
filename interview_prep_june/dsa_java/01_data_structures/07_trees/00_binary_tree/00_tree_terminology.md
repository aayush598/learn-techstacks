# Tree Terminology & Binary Tree Basics

## Tree Terminology

### Basic Terms
- **Root**: The topmost node of a tree. Only one root per tree.
- **Parent**: A node that has one or more child nodes directly connected below it.
- **Child**: A node directly connected to a parent node from below.
- **Sibling**: Nodes that share the same parent.
- **Leaf** (External node): A node with no children.
- **Internal node**: A node with at least one child.
- **Ancestor**: Parent, grandparent, great-grandparent, etc. (all nodes on path from root to node)
- **Descendant**: Child, grandchild, etc. (all nodes in the subtree rooted at the node)
- **Subtree**: A tree formed by a node and all its descendants.
- **Edge**: Connection between two nodes.
- **Path**: Sequence of nodes and edges connecting a node to another.
- **Height of node**: Number of edges on the longest path from that node to a leaf.
- **Depth of node**: Number of edges from the root to that node.
- **Level of node**: Depth + 1 (or sometimes depth; both conventions used).
- **Size of tree**: Total number of nodes.

```
         A          ← Root (depth 0, level 1)
       /   \
      B     C       ← B and C are children of A, siblings of each other
     / \   / \
    D   E F   G     ← D, E, F, G are leaves (depth 2, level 3)
```

- Height of A = 2 (A→B→D or A→C→F, etc.)
- Depth of D = 2, Depth of B = 1
- Height of B = 1 (B→D), Height of D = 0

## Binary Tree

A **binary tree** is a tree where each node has **at most 2 children** (left child and right child).

```java
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int val) { this.val = val; }
}
```

## Types of Binary Trees

### Full Binary Tree (Strict Binary Tree)
Every node has either 0 or 2 children. No node has exactly 1 child.

```
    1
   / \
  2   3
 / \
4   5
```

### Complete Binary Tree
All levels except possibly the last are completely filled, and nodes in the last level are as far left as possible.

```
    1
   / \
  2   3
 / \  /
4  5 6
```

Used in heap data structure.

### Perfect Binary Tree
All internal nodes have 2 children, and all leaves are at the same level.

```
    1
   / \
  2   3
 / \ / \
4  5 6 7
```

### Balanced Binary Tree
For every node, the height difference between left and right subtrees is at most 1.

```
    1
   / \
  2   3
 / \
4   5
```

AVL trees are height-balanced.

### Skewed Binary Tree
Every node has exactly one child (like a linked list).

```
1
 \
  2
   \
    3
     \
      4
```

## Properties

### Maximum Nodes at Level h
- Level h (1-indexed, root at level 1): maximum nodes = **2^(h-1)**
- Level h (0-indexed, root at level 0): maximum nodes = **2^h**

### Maximum Nodes in a Tree of Height h
- Height h (0-indexed, single node has height 0):
  - Maximum nodes = **2^(h+1) - 1** (perfect binary tree)
  - Minimum nodes = **h + 1** (skewed tree)

### Height of a Tree with n nodes
- Best case (balanced): **⌈log₂(n+1)⌉ - 1 ≈ log₂n**
- Worst case (skewed): **n - 1**

### Number of Edges
- A tree with n nodes has exactly **n-1** edges.

### Leaf Nodes in Full Binary Tree
- If a full binary tree has I internal nodes, it has **I + 1** leaf nodes.

### Relation between Height and Nodes
- Complete binary tree with n nodes has height **⌊log₂n⌋**

## Height vs Depth vs Level

| Term | Definition | Direction of Measurement |
|------|-----------|------------------------|
| **Height** | Longest path from node to a leaf (edges) | Bottom-up (from leaf) |
| **Depth** | Path from root to node (edges) | Top-down (from root) |
| **Level** | Depth + 1 (in 1-indexed convention) | Top-down |

```
        A (height=2, depth=0)
       / \
      B   C (B: height=1, depth=1)
     / \
    D   E (D: height=0, depth=2)
```

## Tree Traversals Overview

### Depth-First Search (DFS)
1. **Preorder**: Root → Left → Right
2. **Inorder**: Left → Root → Right
3. **Postorder**: Left → Right → Root

For the tree:
```
    1
   / \
  2   3
 / \
4   5
```

- Preorder:  1 → 2 → 4 → 5 → 3
- Inorder:   4 → 2 → 5 → 1 → 3
- Postorder: 4 → 5 → 2 → 3 → 1

### Breadth-First Search (BFS)
4. **Level Order**: Process level by level, left to right
   - 1 → 2 → 3 → 4 → 5

## Time & Space Complexity Summary

| Traversal | Time | Space (Recursive) | Space (Iterative) |
|-----------|------|-------------------|-------------------|
| DFS (any) | O(n) | O(h) recursion stack | O(h) explicit stack |
| BFS       | O(n) | N/A               | O(w) queue (w = max width, worst O(n)) |
| Morris    | O(n) | O(1)              | O(1) |

Where h is tree height (n in worst case, log n in best case).

## Practical Insights

- **Inorder** traversal of a BST gives **sorted order**.
- **Preorder** is used for **serialization** and **tree copying**.
- **Postorder** is used for **deleting a tree** (process children before parent).
- **Level order** is used for **shortest path** in unweighted trees.
- Balanced trees give O(log n) operations, skewed trees degrade to O(n).
- In interviews, always consider the **worst-case height** for space complexity of recursive solutions.
- When recursion depth could exceed stack limit (thousands of nodes), prefer **iterative** approaches.
