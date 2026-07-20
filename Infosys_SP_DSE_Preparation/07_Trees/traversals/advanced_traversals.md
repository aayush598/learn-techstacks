# Advanced Tree Traversals

## Table of Contents
1. [Morris Traversal (O(1) Space)](#1-morris-traversal-o1-space)
2. [Boundary Traversal](#2-boundary-traversal)
3. [Vertical Order Traversal](#3-vertical-order-traversal)
4. [Tree Views](#4-tree-views)
5. [Diagonal Traversal](#5-diagonal-traversal)
6. [Spiral Level Order Traversal](#6-spiral-level-order-traversal)

---

## 1. Morris Traversal (O(1) Space)

**Key Insight:** Use threaded binary tree concept — temporary links from rightmost node of left subtree back to current node.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def morris_inorder(root):
    """Inorder traversal with O(1) space, O(n) time.
    
    How it works:
    1. If left child doesn't exist → visit current, go right
    2. If left child exists → find inorder predecessor
       a. If predecessor's right is None → create thread, go left
       b. If predecessor's right points to current → 
          remove thread, visit current, go right
    """
    result = []
    current = root
    
    while current:
        if not current.left:
            # No left subtree — visit and go right
            result.append(current.val)
            current = current.right
        else:
            # Find inorder predecessor (rightmost in left subtree)
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                predecessor = predecessor.right
            
            if not predecessor.right:
                # Create thread: predecessor → current
                predecessor.right = current
                current = current.left
            else:
                # Thread exists → left subtree fully visited
                predecessor.right = None  # Remove thread
                result.append(current.val)
                current = current.right
    
    return result

# Time: O(n), Space: O(1) — truly constant space!
# Note: Temporarily modifies tree structure but restores it
```

### Morris Preorder

```python
def morris_preorder(root):
    """Preorder traversal with O(1) space.
    Same as inorder, but visit node when creating thread.
    """
    result = []
    current = root
    
    while current:
        if not current.left:
            result.append(current.val)
            current = current.right
        else:
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                predecessor = predecessor.right
            
            if not predecessor.right:
                result.append(current.val)  # Visit BEFORE going left
                predecessor.right = current
                current = current.left
            else:
                predecessor.right = None
                current = current.right
    
    return result

# Time: O(n), Space: O(1)
```

**When to Use:**
- When O(1) space is a strict requirement
- When modifying tree temporarily is acceptable
- Common in interviews to demonstrate deep knowledge

---

## 2. Boundary Traversal

**Definition:** Traverse the boundary of the tree in anti-clockwise direction.

```
        1
       / \
      2   3
     / \ / \
    4  5 6  7
    
Boundary: 1, 2, 4, 5, 6, 7, 3
```

```python
def boundary_traversal(root):
    """Boundary traversal: left boundary + leaves + right boundary.
    
    Steps:
    1. Root (if not a leaf)
    2. Left boundary (top-down, excluding leaves)
    3. All leaf nodes (left to right)
    4. Right boundary (bottom-up, excluding leaves)
    """
    if not root:
        return []
    
    result = [root.val]
    
    def left_boundary(node):
        """Add left boundary nodes (top-down, no leaves)."""
        while node:
            if node.left or node.right:  # Not a leaf
                result.append(node.val)
            if node.left:
                node = node.left
            else:
                node = node.right
    
    def right_boundary(node):
        """Add right boundary nodes (bottom-up, no leaves)."""
        stack = []
        while node:
            if node.left or node.right:  # Not a leaf
                stack.append(node.val)
            if node.right:
                node = node.right
            else:
                node = node.left
        result.extend(reversed(stack))
    
    def leaves(node):
        """Add all leaf nodes left to right."""
        if not node:
            return
        if not node.left and not node.right:
            result.append(node.val)
            return
        leaves(node.left)
        leaves(node.right)
    
    # Left boundary (excluding root and leaves)
    left_boundary(root.left)
    # Leaves
    leaves(root)
    # Right boundary (excluding root and leaves)
    right_boundary(root.right)
    
    return result

# Time: O(n), Space: O(h)
```

---

## 3. Vertical Order Traversal

```python
from collections import defaultdict, deque

def vertical_order(root):
    """Group nodes by horizontal distance (column).
    
            1
           / \
          2   3
         / \ / \
        4  5 6  7
        
    Column -2: [4]
    Column -1: [2]
    Column  0: [1, 5, 6]
    Column  1: [3]
    Column  2: [7]
    
    Output: [[4], [2], [1, 5, 6], [3], [7]]
    """
    if not root:
        return []
    
    # column → list of (row, val) pairs
    col_map = defaultdict(list)
    queue = deque([(root, 0, 0)])  # (node, column, row)
    min_col = max_col = 0
    
    while queue:
        node, col, row = queue.popleft()
        col_map[col].append((row, node.val))
        min_col = min(min_col, col)
        max_col = max(max_col, col)
        
        if node.left:
            queue.append((node.left, col - 1, row + 1))
        if node.right:
            queue.append((node.right, col + 1, row + 1))
    
    result = []
    for col in range(min_col, max_col + 1):
        # Sort by row, then by value for same row
        col_map[col].sort()
        result.append([val for _, val in col_map[col]])
    
    return result

# Time: O(n log n) due to sorting, Space: O(n)
```

### Strict Vertical Order (LeetCode 987)

```python
def vertical_order_strict(root):
    """When nodes at same column AND row are sorted by value."""
    entries = []  # (col, row, val)
    queue = deque([(root, 0, 0)])
    
    while queue:
        node, col, row = queue.popleft()
        entries.append((col, row, node.val))
        
        if node.left:
            queue.append((node.left, col - 1, row + 1))
        if node.right:
            queue.append((node.right, col + 1, row + 1))
    
    # Sort by column, then row, then value
    entries.sort()
    
    result = []
    prev_col = None
    for col, row, val in entries:
        if col != prev_col:
            result.append([])
            prev_col = col
        result[-1].append(val)
    
    return result

# Time: O(n log n), Space: O(n)
```

---

## 4. Tree Views

### Top View

```python
from collections import deque

def top_view(root):
    """Top view: first node at each horizontal distance.
    Imagine looking from the top — you see only the first node per column.
    
            1
           / \
          2   3
         / \
        4   5
    
    Top view: [2, 1, 3]
    """
    if not root:
        return []
    
    col_map = {}
    queue = deque([(root, 0)])
    
    while queue:
        node, col = queue.popleft()
        
        # First node at this column → top view
        if col not in col_map:
            col_map[col] = node.val
        
        if node.left:
            queue.append((node.left, col - 1))
        if node.right:
            queue.append((node.right, col + 1))
    
    return [col_map[c] for c in sorted(col_map.keys())]

# Time: O(n), Space: O(n)
```

### Bottom View

```python
def bottom_view(root):
    """Bottom view: LAST node at each horizontal distance.
    Look from bottom — see only the last node per column.
    """
    if not root:
        return []
    
    col_map = {}
    queue = deque([(root, 0)])
    
    while queue:
        node, col = queue.popleft()
        col_map[col] = node.val  # Always overwrite → last node wins
        
        if node.left:
            queue.append((node.left, col - 1))
        if node.right:
            queue.append((node.right, col + 1))
    
    return [col_map[c] for c in sorted(col_map.keys())]

# Time: O(n), Space: O(n)
```

### Left View

```python
def left_view(root):
    """Left view: first node at each level.
    Imagine looking from the left side.
    
            1
           / \
          2   3
         / \ / \
        4  5 6  7
    
    Left view: [1, 2, 4]
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        
        for i in range(level_size):
            node = queue.popleft()
            
            # First node at each level
            if i == 0:
                result.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return result

# Time: O(n), Space: O(n)
```

### Right View

```python
def right_view(root):
    """Right view: last node at each level.
    Imagine looking from the right side.
    
            1
           / \
          2   3
         / \ / \
        4  5 6  7
    
    Right view: [1, 3, 7]
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        
        for i in range(level_size):
            node = queue.popleft()
            
            # Last node at each level
            if i == level_size - 1:
                result.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return result

# Time: O(n), Space: O(n)
```

### Recursive Left View

```python
def left_view_recursive(root):
    """Left view using recursive DFS."""
    result = []
    
    def dfs(node, level):
        if not node:
            return
        
        # First node at this level
        if level == len(result):
            result.append(node.val)
        
        # Visit left first
        dfs(node.left, level + 1)
        dfs(node.right, level + 1)
    
    dfs(root, 0)
    return result
```

---

## 5. Diagonal Traversal

```python
from collections import deque

def diagonal_traversal(root):
    """Traverse tree diagonally (right child same diagonal, left child next).
    
            8
           / \
          3   10
         /     \
        1       14
         \     /
          6   13
    
    Diagonal 0: [8, 10, 14]
    Diagonal 1: [3, 1, 6, 13]
    Diagonal 2: [1 (if exists)]
    
    Key: left child moves to next diagonal
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        size = len(queue)
        level = []
        
        for _ in range(size):
            node = queue.popleft()
            
            # Traverse current diagonal
            while node:
                level.append(node.val)
                
                # Left child starts new diagonal
                if node.left:
                    queue.append(node.left)
                
                node = node.right  # Right child same diagonal
        
        result.append(level)
    
    return result

# Time: O(n), Space: O(n)
```

### Diagonal Traversal Using Map

```python
def diagonal_traversal_map(root):
    """Using dictionary to group by diagonal distance.
    Right child: same diagonal (d)
    Left child: next diagonal (d + 1)
    """
    diag_map = {}
    
    def dfs(node, d):
        if not node:
            return
        
        if d not in diag_map:
            diag_map[d] = []
        diag_map[d].append(node.val)
        
        dfs(node.left, d + 1)
        dfs(node.right, d)
    
    dfs(root, 0)
    
    return [diag_map[d] for d in sorted(diag_map.keys())]

# Time: O(n), Space: O(n)
```

---

## 6. Spiral Level Order Traversal

```python
from collections import deque

def spiral_level_order(root):
    """Zigzag traversal: alternate left→right and right→left per level.
    
    Also called: zigzag level order or snake pattern.
    
            1
           / \
          2   3
         / \ / \
        4  5 6  7
    
    Output: [[1], [3, 2], [4, 5, 6, 7]]
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    left_to_right = True
    
    while queue:
        size = len(queue)
        level = deque()
        
        for _ in range(size):
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

### Spiral Using Two Stacks

```python
def spiral_two_stacks(root):
    """Zigzag using two stacks."""
    if not root:
        return []
    
    result = []
    current_level = [root]
    next_level = []
    left_to_right = True
    
    while current_level:
        level = []
        
        while current_level:
            node = current_level.pop()
            level.append(node.val)
            
            if left_to_right:
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)
            else:
                if node.right:
                    next_level.append(node.right)
                if node.left:
                    next_level.append(node.left)
        
        result.append(level)
        current_level = next_level
        next_level = []
        left_to_right = not left_to_right
    
    return result

# Time: O(n), Space: O(n)
```

---

## Quick Reference Table

| Traversal | Time | Space | Key Idea |
|-----------|------|-------|----------|
| Morris Inorder | O(n) | O(1) | Thread temporary links |
| Morris Preorder | O(n) | O(1) | Visit when creating thread |
| Boundary | O(n) | O(h) | Left boundary + leaves + right boundary |
| Vertical Order | O(n log n) | O(n) | Group by column, sort by row |
| Top View | O(n) | O(n) | First node per column |
| Bottom View | O(n) | O(n) | Last node per column |
| Left View | O(n) | O(n) | First node per level |
| Right View | O(n) | O(n) | Last node per level |
| Diagonal | O(n) | O(n) | Right = same diag, left = next diag |
| Spiral/Zigzag | O(n) | O(n) | Alternate L→R and R→L per level |

**Interview Tips:**
- Morris Traversal is a great way to impress — O(1) space inorder is powerful
- Vertical Order: clarify tie-breaking rules (by row? by value?)
- Top/Bottom view: bottom view is just overwriting the map (last wins)
- Left/Right view: first/last element at each BFS level
- Diagonal: think of it as right = same group, left = new group
- Spiral: use deque for O(1) appendleft, or use two stacks
