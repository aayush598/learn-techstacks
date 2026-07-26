# Binary Tree Basics - Complete Guide

## What is a Binary Tree?

A binary tree is a hierarchical data structure where each node has at most TWO children (left and right).

### Visual:

```
        1          ← Root node (no parent)
       / \
      2   3        ← Children of 1
     / \ / \
    4  5 6  7      ← Leaf nodes (no children)

Properties:
- Root: 1 (top node)
- Parent: 1 is parent of 2 and 3
- Child: 2 and 3 are children of 1
- Leaf: 4, 5, 6, 7 (no children)
- Height: 3 (longest path from root to leaf)
- Depth of node 5: 2 (distance from root)
```

---

## 1. TreeNode Class Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val      # The value stored in node
        self.left = left    # Pointer to left child
        self.right = right  # Pointer to right child
```

### Visual: Creating Nodes

```python
# Create leaf nodes
node4 = TreeNode(4)    # 4 (no children)
node5 = TreeNode(5)    # 5 (no children)

# Create internal node
node2 = TreeNode(2)    # 2
node2.left = node4     # 2 → left = 4
node2.right = node5    # 2 → right = 5

# Create root
root = TreeNode(1)     # 1
root.left = node2      # 1 → left = 2
```

```
Result:
    1
   / \
  2   None
 / \
4   5
```

---

## 2. Building a Tree from Array

Given level-order array where `None` represents missing nodes:

```python
arr = [1, 2, 3, None, 4, 5, None]
```

### Visual: Building from Array

```
Array: [1, 2, 3, None, 4, 5, None]

Level 0: 1
Level 1: 2, 3
Level 2: None, 4, 5, None

Tree:
        1
       / \
      2   3
       \ /
       4 5
```

### Step-by-Step Build:

```
Step 1: Create root = TreeNode(1)
        Queue: [1]

Step 2: Process 1, add children 2, 3
        Queue: [2, 3]

Step 3: Process 2, add children None, 4
        Queue: [3, 4]

Step 4: Process 3, add children 5, None
        Queue: [4, 5]

Step 5: Process 4, add children None, None
        Queue: [5]

Step 6: Process 5, add children None, None
        Queue: []

Result:
        1
       / \
      2   3
       \ /
       4 5
```

### The Code:
```python
from collections import deque

def build_tree_from_array(arr):
    """Build binary tree from level-order array."""
    if not arr or arr[0] is None:
        return None
    
    root = TreeNode(arr[0])
    queue = deque([root])
    i = 1
    
    while queue and i < len(arr):
        node = queue.popleft()
        
        # Left child
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        
        # Right child
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1
    
    return root
```

**Time:** O(n) | **Space:** O(n)

---

## 3. Tree Traversals — Recursive

### Inorder (Left → Root → Right)

**Use case:** For BST, gives sorted order!

```
Tree:
        1
       / \
      2   3
     / \ / \
    4  5 6  7

Inorder traversal:
1. Go left from 1 → reach 2
2. Go left from 2 → reach 4
3. 4 has no left, visit 4
4. Back to 2, visit 2
5. Go right from 2 → reach 5
6. 5 has no left, visit 5
7. Back to 1, visit 1
8. Go right from 1 → reach 3
9. Go left from 3 → reach 6
10. 6 has no left, visit 6
11. Back to 3, visit 3
12. Go right from 3 → reach 7
13. 7 has no left, visit 7

Result: [4, 2, 5, 1, 6, 3, 7]
```

### Visual:

```
        1
       / \
      2   3
     / \ / \
    4  5 6  7

Visit order: 4 → 2 → 5 → 1 → 6 → 3 → 7

       (1)
      /   \
    (2)   (3)
    / \   / \
  (4)(5)(6)(7)
  
Path: 4→2→5→1→6→3→7
      ↑     ↑     ↑
     Left  Root  Right
```

### The Code:
```python
def inorder_traversal(root):
    """Inorder: Left, Root, Right"""
    result = []
    
    def dfs(node):
        if not node:
            return
        dfs(node.left)       # Left
        result.append(node.val)  # Root
        dfs(node.right)      # Right
    
    dfs(root)
    return result

# For BST [2,1,3]: inorder gives [1,2,3] (sorted!)
```

---

### Preorder (Root → Left → Right)

**Use case:** Copy/serialize tree structure!

```
Tree:
        1
       / \
      2   3
     / \ / \
    4  5 6  7

Preorder traversal:
1. Visit root 1
2. Go left to 2, visit 2
3. Go left to 4, visit 4
4. Back to 2, go right to 5, visit 5
5. Back to 1, go right to 3, visit 3
6. Go left to 6, visit 6
7. Back to 3, go right to 7, visit 7

Result: [1, 2, 4, 5, 3, 6, 7]
```

### Visual:

```
        (1)        ← Visit 1st
       /   \
     (2)   (3)     ← Visit 2nd, 5th
     / \   / \
   (4)(5)(6)(7)    ← Visit 3rd, 4th, 6th, 7th

Path: 1→2→4→5→3→6→7
      ↑           ↑
     Root      Left→Right
```

### The Code:
```python
def preorder_traversal(root):
    """Preorder: Root, Left, Right"""
    result = []
    
    def dfs(node):
        if not node:
            return
        result.append(node.val)  # Root (first!)
        dfs(node.left)       # Left
        dfs(node.right)      # Right
    
    dfs(root)
    return result
```

---

### Postorder (Left → Right → Root)

**Use case:** Delete tree, evaluate expressions!

```
Tree:
        1
       / \
      2   3
     / \ / \
    4  5 6  7

Postorder traversal:
1. Go left to 2, then left to 4
2. 4 has no children, visit 4
3. Back to 2, go right to 5
4. 5 has no children, visit 5
5. Back to 2, both children done, visit 2
6. Back to 1, go right to 3
7. Go left to 6, visit 6
8. Back to 3, go right to 7, visit 7
9. Back to 3, both children done, visit 3
10. Back to 1, both children done, visit 1

Result: [4, 5, 2, 6, 7, 3, 1]
```

### Visual:

```
        (1)        ← Visit 7th (last)
       /   \
     (2)   (3)     ← Visit 3rd, 6th
     / \   / \
   (4)(5)(6)(7)    ← Visit 1st, 2nd, 4th, 5th

Path: 4→5→2→6→7→3→1
      ↑     ↑     ↑
    Left  Right  Root
```

### The Code:
```python
def postorder_traversal(root):
    """Postorder: Left, Right, Root"""
    result = []
    
    def dfs(node):
        if not node:
            return
        dfs(node.left)       # Left
        dfs(node.right)      # Right
        result.append(node.val)  # Root (last!)
    
    dfs(root)
    return result
```

---

## 4. Tree Traversals — Iterative

### Iterative Inorder

```python
def inorder_iterative(root):
    """Iterative inorder using explicit stack."""
    result = []
    stack = []
    current = root
    
    while current or stack:
        # Go as far left as possible
        while current:
            stack.append(current)
            current = current.left
        
        # Process node
        current = stack.pop()
        result.append(current.val)
        
        # Move to right subtree
        current = current.right
    
    return result
```

### Visual: Iterative Inorder

```
Tree:
        1
       / \
      2   3
     / \
    4   5

Step 1: Push 1, go left to 2
        Stack: [1, 2]

Step 2: Push 2, go left to 4
        Stack: [1, 2, 4]

Step 3: 4 has no left, pop 4
        Stack: [1, 2]
        Result: [4]

Step 4: 4 has no right, pop 2
        Stack: [1]
        Result: [4, 2]

Step 5: 2 has right (5), go to 5
        Stack: [1]

Step 6: 5 has no left, pop 5
        Stack: [1]
        Result: [4, 2, 5]

Step 7: 5 has no right, pop 1
        Stack: []
        Result: [4, 2, 5, 1]

Step 8: 1 has right (3), go to 3
        Stack: []

Step 9: 3 has no left, pop 3
        Stack: []
        Result: [4, 2, 5, 1, 3]

Final: [4, 2, 5, 1, 3] ✓
```

---

## 5. Level Order Traversal (BFS)

**Visit nodes level by level, left to right.**

```
Tree:
        3
       / \
      9  20
        /  \
       15   7

Level 0: [3]
Level 1: [9, 20]
Level 2: [15, 7]

Output: [[3], [9, 20], [15, 7]]
```

### Step-by-Step BFS:

```
Step 1: Queue: [3]
        Visit 3, add children 9, 20
        Queue: [9, 20]
        Level 0: [3]

Step 2: Queue: [9, 20]
        Visit 9 (no children)
        Visit 20, add children 15, 7
        Queue: [15, 7]
        Level 1: [9, 20]

Step 3: Queue: [15, 7]
        Visit 15 (no children)
        Visit 7 (no children)
        Queue: []
        Level 2: [15, 7]

Result: [[3], [9, 20], [15, 7]]
```

### The Code:
```python
from collections import deque

def level_order_traversal(root):
    """BFS level order traversal."""
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result
```

**Time:** O(n) | **Space:** O(n)

---

## 6. Maximum Depth of Binary Tree

**Depth = number of nodes on longest path from root to leaf.**

```
Tree:
        1
       / \
      2   3
     / \
    4   5

Path 1→2→4: length 3
Path 1→2→5: length 3
Path 1→3: length 2

Maximum depth = 3
```

### Recursive Approach:

```python
def max_depth_recursive(root):
    """Maximum depth using recursion."""
    if not root:
        return 0
    
    left_depth = max_depth_recursive(root.left)
    right_depth = max_depth_recursive(root.right)
    
    return 1 + max(left_depth, right_depth)
```

### Visual: Recursive Call Stack

```
max_depth(1)
├── max_depth(2)
│   ├── max_depth(4)
│   │   └── return 0 (no children)
│   │   → return 1 + max(0, 0) = 1
│   └── max_depth(5)
│       └── return 0 (no children)
│       → return 1 + max(0, 0) = 1
│   → return 1 + max(1, 1) = 2
└── max_depth(3)
    └── return 0 (no children)
    → return 1 + max(0, 0) = 1
→ return 1 + max(2, 1) = 3

Result: 3 ✓
```

---

## 7. Minimum Depth of Binary Tree

**Minimum depth = shortest path from root to a LEAF node.**

```
Tree:
        2
         \
          3
         /
        4

Minimum depth = 3 (path 2→3→4)
NOT 2! (3 is not a leaf, it has child 4)
```

### The Code:
```python
def min_depth(root):
    """Minimum depth = shortest path to a leaf."""
    if not root:
        return 0
    
    # Leaf node
    if not root.left and not root.right:
        return 1
    
    # If only right child exists
    if not root.left:
        return 1 + min_depth(root.right)
    
    # If only left child exists
    if not root.right:
        return 1 + min_depth(root.left)
    
    # Both children exist
    return 1 + min(min_depth(root.left), min_depth(root.right))
```

---

## 8. Invert/Flip Binary Tree

**Swap left and right children at every node (mirror the tree).**

```
Input:          4              Output:      4
               / \                        / \
              2   7                      7   2
             / \ / \                    / \ / \
            1  3 6  9                  9  6 3  1
```

### The Code:
```python
def invert_tree(root):
    """Mirror the tree: swap left and right at every node."""
    if not root:
        return None
    
    # Swap left and right
    root.left, root.right = root.right, root.left
    
    # Recurse on children
    invert_tree(root.left)
    invert_tree(root.right)
    
    return root
```

### Visual: Step-by-Step

```
Step 1: Start at root (4)
        Swap 2 and 7
        
        4          →        4
       / \                 / \
      2   7               7   2
     / \ / \             / \ / \
    1  3 6  9           1  3 6  9

Step 2: Go to 7 (new left)
        Swap 1 and 3
        
        4                 4
       / \               / \
      7   2             7   2
     / \ / \           / \ / \
    1  3 6  9         3  1 6  9

Step 3: Go to 2 (new right)
        Swap 6 and 9
        
        4                 4
       / \               / \
      7   2             7   2
     / \ / \           / \ / \
    3  1 6  9         3  1 9  6

Done! Tree is mirrored ✓
```

---

## Quick Reference

| Operation | Time | Space | When to Use |
|-----------|------|-------|-------------|
| Inorder | O(n) | O(h) | BST sorted order |
| Preorder | O(n) | O(h) | Copy/serialize tree |
| Postorder | O(n) | O(h) | Delete tree, expressions |
| Level order | O(n) | O(n) | Level-by-level processing |
| Max depth | O(n) | O(h) | Height-related problems |
| Min depth | O(n) | O(h) | Shortest path to leaf |
| Invert tree | O(n) | O(h) | Mirror tree |
| Subtree check | O(m×n) | O(h) | Tree comparison |

> **h** = height of tree (O(log n) balanced, O(n) worst case skewed)

## Key Insights

1. **Inorder on BST** gives sorted order!
2. **Preorder** is great for serialization (reconstruct tree from preorder)
3. **Postorder** processes children before parent (useful for deletion)
4. **Level order** uses BFS (queue), others use DFS (stack/recursion)
5. **Recursive solutions** are elegant but may cause stack overflow for deep trees
6. **Iterative solutions** use explicit stack/queue, safer for large trees
