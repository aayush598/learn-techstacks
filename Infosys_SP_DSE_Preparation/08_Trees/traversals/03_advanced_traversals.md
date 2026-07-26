# Advanced Tree Traversals

## Table of Contents
1. [Morris Traversal (O(1) Space)](#1-morris-traversal-o1-space)
2. [Boundary Traversal](#2-boundary-traversal)
3. [Vertical Order Traversal](#3-vertical-order-traversal)
4. [Tree Views](#4-tree-views)
5. [Diagonal Traversal](#5-diagonal-traversal)
6. [Spiral Level Order Traversal](#6-spiral-level-order-traversal)

---

## When to Use Which Traversal

```
╔════════════════════════════════════════════════════════════════════════╗
║  Need O(1) space?           → Morris Traversal                      ║
║  Need border nodes?         → Boundary Traversal                     ║
║  Group by column?           → Vertical Order                         ║
║  What's visible from side?  → Left/Right/Top/Bottom View             ║
║  Group by diagonal?         → Diagonal Traversal                     ║
║  Alternate direction/level? → Spiral/Zigzag Traversal                ║
╚════════════════════════════════════════════════════════════════════════╝
```

---

## 1. Morris Traversal (O(1) Space)

### The Big Idea

**Key Insight:** Use threaded binary tree concept — temporary links from rightmost node of left subtree back to current node.

```
Normal tree:              Threaded concept:
     4                         4
    / \                       / \
   2   5                     2   5
  / \                       / \
 1   3                     1   3
                             ↺ ← Thread: node 3's right points back to 2
                                 (temporarily, to find way back)
```

### Step-by-Step Walkthrough

```
Tree:
       4
      / \
     2   5
    / \
   1   3

Inorder result should be: [1, 2, 3, 4, 5]

═══════════════════════════════════════════════════════
Step 1: current = 4, has left child (2)
  → Find predecessor: go to 2, then right to 3
  → predecessor = 3, 3.right is None
  → CREATE THREAD: 3.right = 4
  → Move left: current = 2

  Tree now:  4 ←── 3 (thread)
            /       \
           2         5
          /
         1

Step 2: current = 2, has left child (1)
  → Find predecessor: go to 1, 1.right is None
  → CREATE THREAD: 1.right = 2
  → Move left: current = 1

  Tree now:  4 ←── 3
            /       \
           2 ←── 1   5
                 (thread)

Step 3: current = 1, NO left child
  → VISIT 1, result = [1]
  → Move right: current = 1.right = 2 (via thread!)

Step 4: current = 2, has left child (1)
  → Find predecessor: 1.right = 2 (thread exists!)
  → REMOVE THREAD: 1.right = None
  → VISIT 2, result = [1, 2]
  → Move right: current = 2.right = 3

Step 5: current = 3, NO left child
  → VISIT 3, result = [1, 2, 3]
  → Move right: current = 3.right = 4 (via thread!)

Step 6: current = 4, has left child (2)
  → Find predecessor: 2.right = 3, 3.right = 4 (thread exists!)
  → REMOVE THREAD: 3.right = None
  → VISIT 4, result = [1, 2, 3, 4]
  → Move right: current = 4.right = 5

Step 7: current = 5, NO left child
  → VISIT 5, result = [1, 2, 3, 4, 5]
  → Move right: current = None

DONE! result = [1, 2, 3, 4, 5] ✓
═══════════════════════════════════════════════════════
```

### Decision Flowchart

```
                ┌──────────────┐
                │  current = ? │
                └──────┬───────┘
                       │
              ┌────────▼────────┐
              │ current is None?│──Yes──► DONE
              └────────┬────────┘
                       │ No
              ┌────────▼────────┐
              │ Has left child? │──No──► VISIT node, go RIGHT
              └────────┬────────┘
                       │ Yes
              ┌────────▼────────┐
              │ Find predecessor│
              │ (rightmost in   │
              │  left subtree)  │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │ predecessor     │──Yes──► Thread exists!
              │ .right == None? │        REMOVE thread,
              └────────┬────────┘        VISIT node, go RIGHT
                       │ No
                       ▼
              Thread doesn't exist!
              CREATE thread (pred.right = current)
              Go LEFT
```

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
        1             Boundary nodes highlighted:
       / \            1 (root)
      2   3           2 (left boundary)
     / \ / \          4 (left boundary, leaf)
    4  5 6  7         5 (leaf)
                      6 (leaf)
Boundary: 1, 2, 4, 5, 6, 7, 3
                      7 (leaf)
                      3 (right boundary)
```

### Breaking Down the Boundary

```
The boundary consists of THREE parts:

Part 1: LEFT BOUNDARY (top-down, excluding leaves)
  Start from root.left, always go left if possible, else go right
  Path: 1 → 2 → 4 (stops at leaf)

Part 2: ALL LEAF NODES (left to right)
  Leaves: 4, 5, 6, 7

Part 3: RIGHT BOUNDARY (bottom-up, excluding leaves)
  Start from root.right, always go right if possible, else go left
  Path: 3 (bottom-up: just 3, since 3 is a leaf)

Combined: [1] + [2] + [4,5,6,7] + [3] = [1,2,4,5,6,7,3]
```

### Visual Walkthrough

```
Tree:           Boundary path (anti-clockwise):
        1              1
       / \            / \
      2   3     →    2   3
     / \ / \        /     \
    4  5 6  7      4       7
                     ↘   ↙
                      5 6
                      (leaves)

Step 1: Add root (1)
Step 2: Left boundary (top-down, skip leaves):
  1.left = 2, not leaf → add 2
  2.left = 4, IS leaf → stop
Step 3: Leaves (left to right DFS):
  4 (leaf) → add
  5 (leaf) → add
  6 (leaf) → add
  7 (leaf) → add
Step 4: Right boundary (bottom-up, skip leaves):
  1.right = 3, IS leaf → skip (or add if non-leaf only)

Result: [1, 2, 4, 5, 6, 7]
Note: 3 is excluded because it's a leaf AND right boundary,
      but the code handles this based on the specific definition.
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

### Concept

Group nodes by their **horizontal distance (column)** from the root.

```
            1              Horizontal distances:
           / \
          2   3            col -2: [4]
         / \ / \           col -1: [2]
        4  5 6  7          col  0: [1, 5, 6]
                           col  1: [3]
Column assignment:         col  2: [7]
  root = column 0
  left child = parent - 1
  right child = parent + 1

Output: [[4], [2], [1, 5, 6], [3], [7]]
```

### BFS Walkthrough

```
Tree:
            1            col=0
           / \
          2   3          col=-1, col=+1
         / \ / \
        4  5 6  7        col=-2, col=0, col=0, col=+2

BFS Queue Processing:
─────────────────────────────────────
Process (1, col=0, row=0):
  col_map[0] = [(0, 1)]
  Queue: [(2, -1, 1), (3, +1, 1)]

Process (2, col=-1, row=1):
  col_map[-1] = [(1, 2)]
  Queue: [(3, +1, 1), (4, -2, 2), (5, 0, 2)]

Process (3, col=+1, row=1):
  col_map[+1] = [(1, 3)]
  Queue: [(4, -2, 2), (5, 0, 2), (6, 0, 2), (7, +2, 2)]

Process (4, col=-2, row=2):
  col_map[-2] = [(2, 4)]

Process (5, col=0, row=2):
  col_map[0] = [(0, 1), (2, 5)]   ← same column, different row

Process (6, col=0, row=2):
  col_map[0] = [(0, 1), (2, 5), (2, 6)]  ← same column AND row!

Process (7, col=+2, row=2):
  col_map[+2] = [(2, 7)]

Final: sort each column by (row, val):
  col -2: [(2,4)]        → [4]
  col -1: [(1,2)]        → [2]
  col  0: [(0,1),(2,5),(2,6)] → [1, 5, 6]  (5 and 6 sorted by value)
  col +1: [(1,3)]        → [3]
  col +2: [(2,7)]        → [7]
─────────────────────────────────────
```

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

### Visual Comparison of All 4 Views

```
            1
           / \
          2   3
         / \ / \
        4  5 6  7

TOP VIEW (looking from above):
  → First node at each horizontal distance
  → Imagine dropping a vertical line from each column, take the topmost

        4 [2] [1] [3] [7]
             ↑   ↑   ↑
         col -1  0  +1
  Result: [4, 2, 1, 3, 7]

BOTTOM VIEW (looking from below):
  → LAST node at each horizontal distance
  → Same columns, but take the bottommost

        [4] [2] [1] [3] [7]
             ↑   ↑   ↑
  Since no nodes overlap in columns for this tree:
  Result: [4, 2, 1, 3, 7]

LEFT VIEW (looking from the left):
  → First node at each LEVEL

            1  ←── Level 0: first = 1
           / \
          2   3  ←── Level 1: first = 2
         / \ / \
        4  5 6  7  ←── Level 2: first = 4
  Result: [1, 2, 4]

RIGHT VIEW (looking from the right):
  → LAST node at each LEVEL

            1  ←── Level 0: last = 1
           / \
          2   3  ←── Level 1: last = 3
         / \ / \
        4  5 6  7  ←── Level 2: last = 7
  Result: [1, 3, 7]
```

### Key Difference: Top/Bottom vs Left/Right

```
Top/Bottom View: grouped by COLUMN (horizontal distance)
  → Uses BFS with column tracking
  → Top: first node per column (don't overwrite map)
  → Bottom: last node per column (overwrite map)

Left/Right View: grouped by LEVEL (depth)
  → Uses BFS with level tracking
  → Left: first node per level (index 0)
  → Right: last node per level (index -1)
```

### Top View

```python
from collections import deque

def top_view(root):
    """Top view: first node at each horizontal distance."""
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

### Concept

Diagonal traversal groups nodes by "diagonal lines" going from top-left to bottom-right.

```
            8
           / \
          3   10
         /     \
        1       14
         \     /
          6   13

Diagonal assignment:
  Diag 0:  8 → 10 → 14         (follow right children from root)
  Diag 1:  3 → 1 → 6 → 13      (left children start new diagonals)
  Diag 2:  (empty for this tree)

Rule:
  → RIGHT child = SAME diagonal (stay on the line)
  → LEFT child  = NEXT diagonal (move to next line)

Visual:
  Diag 0: 8 ──── 10 ──── 14
  Diag 1:   3 ──── 1 ──── 6 ──── 13
  Diag 2:      (left child of 1 would go here)
```

### BFS Walkthrough

```
Queue: [8]
──────────────────────────────────────
Round 1 (diag 0):
  Process 8: level=[8], enqueue left child 3
    → go right: 10: level=[8,10], enqueue left child None
    → go right: 14: level=[8,10,14], enqueue left child 13
    → go right: None → stop
  result = [[8, 10, 14]]
  Queue: [3, 13]

Round 2 (diag 1):
  Process 3: level=[3], enqueue left child 1
    → go right: None → stop
  Process 13: level=[3, 13], enqueue left child None
    → go right: None → stop
  result = [[8, 10, 14], [3, 13]]
  Queue: [1]

  Wait — let me re-trace. The tree is:
            8
           / \
          3   10
         /     \
        1       14
         \     /
          6   13

  Actually, 1 has right child 6, and 14 has left child 13.
  
  Queue after round 1: [3, 13] (left children of 8 and 14... but 14.left=13)

  Actually the BFS diagonal approach:
  - Process each diagonal level
  - For each node in current diagonal, add left child to next level queue

  Let me re-do:
  Queue: [8]
  
  Round 1 (diag 0):
    Dequeue 8, go right: 8→10→14
    For each, enqueue their left children: 3 (from 8), None (from 10), 13 (from 14)
    Diag 0: [8, 10, 14]
    Queue for next diag: [3, 13]
  
  Round 2 (diag 1):
    Dequeue 3, go right: 3→None (3 has no right)
    For 3, enqueue left child: 1
    Dequeue 13, go right: 13→None
    For 13, enqueue left child: None
    Diag 1: [3, 13]
    Queue for next diag: [1]
  
  Round 3 (diag 2):
    Dequeue 1, go right: 1→6
    For 1, enqueue left child: None
    For 6, enqueue left child: None
    Diag 2: [1, 6]
    Queue: []
  
  Result: [[8, 10, 14], [3, 13], [1, 6]]
```

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

### Concept

Also called **zigzag** traversal — alternate left→right and right→left per level.

```
            1
           / \
          2   3
         / \ / \
        4  5 6  7

Level 0 (L→R): [1]
Level 1 (R→L): [3, 2]     ← reversed!
Level 2 (L→R): [4, 5, 6, 7]

Output: [[1], [3, 2], [4, 5, 6, 7]]

Visual snake pattern:
  Level 0:  ──────────►   1
  Level 1:  ◄──────────   3, 2
  Level 2:  ──────────►   4, 5, 6, 7
```

### Key Implementation Detail

```
The trick is using a DEQUE (double-ended queue):
  → L→R level:  append to RIGHT  of deque (normal order)
  → R→L level:  append to LEFT   of deque (reverse order)

OR use two stacks approach:
  Stack 1: processes current level
  Stack 2: builds next level (in reverse order)
```

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

### Pattern Recognition Guide

```
╔══════════════════════════════════════════════════════════════════════════╗
║  "O(1) space"           → Morris Traversal                             ║
║  "boundary" / "perimeter" → Boundary Traversal                         ║
║  "vertical" / "column"   → Vertical Order + column tracking            ║
║  "top view" / "bottom"   → BFS + column map (first/last per column)   ║
║  "left view" / "right"   → BFS + level tracking (first/last per level) ║
║  "diagonal"              → BFS/DFS + diagonal grouping                 ║
║  "zigzag" / "spiral"     → BFS + alternate direction per level         ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Common Mistakes

1. **Morris:** Forgetting to remove threads (must restore tree structure)
2. **Boundary:** Including leaves in left/right boundary, or including root twice
3. **Vertical Order:** Not handling tie-breaking (same row → sort by value)
4. **Top vs Bottom:** Top = first write wins, Bottom = last write (overwrite)
5. **Left vs Right:** Left = first node per level (i==0), Right = last (i==last)
6. **Spiral:** Using regular list instead of deque for O(1) appendleft

**Interview Tips:**
- Morris Traversal is a great way to impress — O(1) space inorder is powerful
- Vertical Order: clarify tie-breaking rules (by row? by value?)
- Top/Bottom view: bottom view is just overwriting the map (last wins)
- Left/Right view: first/last element at each BFS level
- Diagonal: think of it as right = same group, left = new group
- Spiral: use deque for O(1) appendleft, or use two stacks
