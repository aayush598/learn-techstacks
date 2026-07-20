# Binary Tree Basics

## Table of Contents
1. [TreeNode Class Definition](#1-treenode-class-definition)
2. [Building a Tree from Array](#2-building-a-tree-from-array)
3. [Tree Traversals - Recursive](#3-tree-traversals---recursive)
4. [Tree Traversals - Iterative](#4-tree-traversals---iterative)
5. [Level Order Traversal (BFS)](#5-level-order-traversal-bfs)
6. [Zigzag Level Order Traversal](#6-zigzag-level-order-traversal)
7. [Maximum Depth of Binary Tree](#7-maximum-depth-of-binary-tree)
8. [Minimum Depth of Binary Tree](#8-minimum-depth-of-binary-tree)
9. [Same Tree / Identical Tree](#9-same-tree--identical-tree)
10. [Invert/Flip Binary Tree](#10-invertflip-binary-tree)
11. [Subtree of Another Tree](#11-subtree-of-another-tree)

---

## 1. TreeNode Class Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

**Key Points:**
- Each node has a value, a left child pointer, and a right child pointer
- `None` represents absence of a child
- A tree with only root node: `TreeNode(1)`
- Time to create a node: O(1)
- Space for one node: O(1)

---

## 2. Building a Tree from Array

Given a level-order array where `None` represents missing nodes:

```python
from collections import deque

def build_tree_from_array(arr):
    """Build binary tree from level-order array.
    
    Example: [1, 2, 3, None, 4, 5, None] creates:
            1
           / \
          2   3
           \ / 
            4 5
    """
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


def tree_to_array(root):
    """Convert tree back to level-order array for verification."""
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    
    # Remove trailing Nones
    while result and result[-1] is None:
        result.pop()
    
    return result


# Usage
arr = [1, 2, 3, None, 4, 5]
root = build_tree_from_array(arr)
print(tree_to_array(root))  # [1, 2, 3, None, 4, 5]
```

**Complexity:**
- Time: O(n) — visit each element once
- Space: O(n) — queue can hold up to n/2 nodes

---

## 3. Tree Traversals — Recursive

### Inorder (Left → Root → Right)

```python
def inorder_traversal(root):
    """Inorder traversal: Left, Root, Right.
    For BST, gives sorted order.
    """
    result = []
    
    def dfs(node):
        if not node:
            return
        dfs(node.left)       # Left
        result.append(node.val)  # Root
        dfs(node.right)      # Right
    
    dfs(root)
    return result

# Example:     1
#            /   \
#           2     3
#          / \   / \
#         4   5 6   7
# Inorder: [4, 2, 5, 1, 6, 3, 7]
```

### Preorder (Root → Left → Right)

```python
def preorder_traversal(root):
    """Preorder traversal: Root, Left, Right.
    Used to copy/serialize tree structure.
    """
    result = []
    
    def dfs(node):
        if not node:
            return
        result.append(node.val)  # Root
        dfs(node.left)       # Left
        dfs(node.right)      # Right
    
    dfs(root)
    return result

# Preorder: [1, 2, 4, 5, 3, 6, 7]
```

### Postorder (Left → Right → Root)

```python
def postorder_traversal(root):
    """Postorder traversal: Left, Right, Root.
    Used for deletion, expression evaluation.
    """
    result = []
    
    def dfs(node):
        if not node:
            return
        dfs(node.left)       # Left
        dfs(node.right)      # Right
        result.append(node.val)  # Root
    
    dfs(root)
    return result

# Postorder: [4, 5, 2, 6, 7, 3, 1]
```

**Complexity for all recursive traversals:**
- Time: O(n) — visit each node exactly once
- Space: O(h) — recursion stack, h = height of tree (O(log n) balanced, O(n) skewed)

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

# Time: O(n), Space: O(h)
```

### Iterative Preorder

```python
def preorder_iterative(root):
    """Iterative preorder using stack."""
    if not root:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        
        # Push right first so left is processed first (LIFO)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return result

# Time: O(n), Space: O(h)
```

### Iterative Postorder (Two Stack Method)

```python
def postorder_iterative(root):
    """Iterative postorder using two stacks."""
    if not root:
        return []
    
    stack1 = [root]
    stack2 = []
    
    while stack1:
        node = stack1.pop()
        stack2.append(node.val)
        
        if node.left:
            stack1.append(node.left)
        if node.right:
            stack1.append(node.right)
    
    return stack2[::-1]

# Time: O(n), Space: O(n)
```

### Iterative Postorder (One Stack Method)

```python
def postorder_one_stack(root):
    """Iterative postorder using single stack with tracking."""
    result = []
    stack = []
    current = root
    last_visited = None
    
    while current or stack:
        # Go as far left as possible
        while current:
            stack.append(current)
            current = current.left
        
        peek = stack[-1]
        
        # If right child exists and hasn't been visited yet
        if peek.right and peek.right != last_visited:
            current = peek.right
        else:
            result.append(peek.val)
            last_visited = stack.pop()
    
    return result

# Time: O(n), Space: O(h)
```

---

## 5. Level Order Traversal (BFS)

```python
from collections import deque

def level_order_traversal(root):
    """BFS level order traversal.
    
    Example:     3
                / \
               9  20
                  /  \
                 15   7
    Output: [[3], [9, 20], [15, 7]]
    """
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

# Time: O(n), Space: O(n)
```

### Level Order Traversal — Return as Single List

```python
def level_order_flat(root):
    """Return all values in level order as a flat list."""
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        result.append(node.val)
        
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return result

# [3, 9, 20, 15, 7]
```

---

## 6. Zigzag Level Order Traversal

```python
from collections import deque

def zigzag_level_order(root):
    """Zigzag (alternating left-to-right, right-to-left).
    
    Example:     3
                / \
               9  20
                  /  \
                 15   7
    Output: [[3], [20, 9], [15, 7]]
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    left_to_right = True
    
    while queue:
        level_size = len(queue)
        level = deque()  # Use deque for O(1) appendleft
        
        for _ in range(level_size):
            node = queue.popleft()
            
            if left_to_right:
                level.append(node.val)
            else:
                level.appendleft(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(list(level))
        left_to_right = not left_to_right
    
    return result

# Time: O(n), Space: O(n)
```

---

## 7. Maximum Depth of Binary Tree

```python
def max_depth_recursive(root):
    """Maximum depth using recursion.
    Depth = number of nodes on longest path from root to leaf.
    """
    if not root:
        return 0
    
    left_depth = max_depth_recursive(root.left)
    right_depth = max_depth_recursive(root.right)
    
    return 1 + max(left_depth, right_depth)

# Time: O(n), Space: O(h)
```

```python
from collections import deque

def max_depth_bfs(root):
    """Maximum depth using BFS level order."""
    if not root:
        return 0
    
    depth = 0
    queue = deque([root])
    
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return depth

# Time: O(n), Space: O(n)
```

---

## 8. Minimum Depth of Binary Tree

```python
def min_depth(root):
    """Minimum depth = shortest path from root to a leaf node.
    
    Note: A leaf node has NO children.
    If tree is [2, None, 3], min depth is 2 (2->3), not 1.
    """
    if not root:
        return 0
    
    # Leaf node
    if not root.left and not root.right:
        return 1
    
    # If only right child exists, go right
    if not root.left:
        return 1 + min_depth(root.right)
    
    # If only left child exists, go left
    if not root.right:
        return 1 + min_depth(root.left)
    
    # Both children exist
    return 1 + min(min_depth(root.left), min_depth(root.right))

# Time: O(n), Space: O(h)
```

### BFS Approach (Faster — Stops at First Leaf)

```python
from collections import deque

def min_depth_bfs(root):
    """BFS stops at the first leaf found (shallowest)."""
    if not root:
        return 0
    
    queue = deque([(root, 1)])
    
    while queue:
        node, depth = queue.popleft()
        
        # First leaf we encounter is at minimum depth
        if not node.left and not node.right:
            return depth
        
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    
    return 0

# Time: O(n) worst case, Space: O(n)
```

---

## 9. Same Tree / Identical Tree

```python
def is_same_tree(p, q):
    """Check if two binary trees are structurally identical with same values."""
    
    # Both empty
    if not p and not q:
        return True
    
    # One empty, one not
    if not p or not q:
        return False
    
    # Both non-empty: check value and recurse
    return (p.val == q.val and
            is_same_tree(p.left, q.left) and
            is_same_tree(p.right, q.right))

# Time: O(n), Space: O(h)
```

### Iterative Approach

```python
from collections import deque

def is_same_tree_iterative(p, q):
    """BFS/iterative approach using queue."""
    queue = deque([(p, q)])
    
    while queue:
        node1, node2 = queue.popleft()
        
        if not node1 and not node2:
            continue
        if not node1 or not node2:
            return False
        if node1.val != node2.val:
            return False
        
        queue.append((node1.left, node2.left))
        queue.append((node1.right, node2.right))
    
    return True

# Time: O(n), Space: O(n)
```

---

## 10. Invert/Flip Binary Tree

```python
def invert_tree(root):
    """Mirror the tree: swap left and right children at every node.
    
    Input:      4              Output:      4
               / \                        / \
              2   7                      7   2
             / \ / \                    / \ / \
            1  3 6  9                  9  6 3  1
    """
    if not root:
        return None
    
    # Swap
    root.left, root.right = root.right, root.left
    
    # Recurse
    invert_tree(root.left)
    invert_tree(root.right)
    
    return root

# Time: O(n), Space: O(h)
```

### Iterative Approach (BFS)

```python
from collections import deque

def invert_tree_bfs(root):
    """BFS approach: swap at each level."""
    if not root:
        return None
    
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        node.left, node.right = node.right, node.left
        
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return root

# Time: O(n), Space: O(n)
```

---

## 11. Subtree of Another Tree

```python
def is_subtree(root, subRoot):
    """Check if subRoot is a subtree of root.
    
    A subtree must be a complete downward tree, not just a fragment.
    """
    
    def is_same(p, q):
        if not p and not q:
            return True
        if not p or not q:
            return False
        return (p.val == q.val and
                is_same(p.left, q.left) and
                is_same(p.right, q.right))
    
    if not root:
        return False
    
    if is_same(root, subRoot):
        return True
    
    return is_subtree(root.left, subRoot) or is_subtree(root.right, subRoot)

# Time: O(m * n) where m = root nodes, n = subRoot nodes
# Space: O(h) for recursion stack
```

### Optimized with Hashing (O(m + n))

```python
def is_subtree_optimized(root, subRoot):
    """Optimized using tree hashing."""
    
    def hash_tree(node, hash_map):
        if not node:
            return "#"
        
        left = hash_tree(node.left, hash_map)
        right = hash_tree(node.right, hash_map)
        
        tree_hash = f"({node.val},{left},{right})"
        hash_map.add(tree_hash)
        return tree_hash
    
    root_hashes = set()
    hash_tree(root, root_hashes)
    
    sub_hash = hash_tree(subRoot, set())
    
    return sub_hash in root_hashes

# Time: O(m + n), Space: O(m + n)
```

---

## Quick Reference Table

| Operation | Time | Space | Method |
|-----------|------|-------|--------|
| Create node | O(1) | O(1) | — |
| Build from array | O(n) | O(n) | BFS with queue |
| Inorder (recursive) | O(n) | O(h) | DFS |
| Preorder (recursive) | O(n) | O(h) | DFS |
| Postorder (recursive) | O(n) | O(h) | DFS |
| Inorder (iterative) | O(n) | O(h) | Stack |
| Level order | O(n) | O(n) | BFS with queue |
| Max depth | O(n) | O(h) | DFS or BFS |
| Min depth | O(n) | O(h) | DFS or BFS |
| Same tree | O(n) | O(h) | DFS |
| Invert tree | O(n) | O(h) | DFS |
| Subtree check | O(m*n) | O(h) | DFS |

> **h** = height of tree (O(log n) balanced, O(n) worst case skewed)
