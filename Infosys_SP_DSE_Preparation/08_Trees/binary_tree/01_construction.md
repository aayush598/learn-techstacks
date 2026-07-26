# Binary Tree Construction

## Table of Contents
1. [Construct Tree from Inorder and Preorder](#1-construct-tree-from-inorder-and-preorder)
2. [Construct Tree from Inorder and Postorder](#2-construct-tree-from-inorder-and-postorder)
3. [Serialize and Deserialize Binary Tree](#3-serialize-and-deserialize-binary-tree)
4. [Construct BST from Preorder Traversal](#4-construct-bst-from-preorder-traversal)
5. [Construct Binary Tree from String](#5-construct-binary-tree-from-string)

---

## Why Tree Construction Matters

Tree construction problems test your understanding of **traversal properties**.
Before diving in, understand what each traversal tells you:

```
        3
       / \
      9   20
         /  \
        15   7

Preorder  (Root-Left-Right):  [3, 9, 20, 15, 7]  ← Root is ALWAYS first
Inorder   (Left-Root-Right):  [9, 3, 15, 20, 7]  ← Root splits left/right
Postorder (Left-Right-Root):  [9, 15, 7, 20, 3]  ← Root is ALWAYS last
Level-order (BFS):           [3, 9, 20, 15, 7]  ← Level by level
```

**Golden Rules for Construction:**
```
╔══════════════════════════════════════════════════════════════════╗
║  ✦ Inorder + Preorder   → UNIQUE tree (most common)            ║
║  ✦ Inorder + Postorder  → UNIQUE tree                          ║
║  ✦ Preorder + Postorder → NOT unique (multiple trees possible)  ║
║  ✦ Inorder alone         → Could be BST (sorted = inorder)     ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 1. Construct Tree from Inorder and Preorder

### Concept Walkthrough

**Key Insight:** Preorder gives root first, inorder splits into left/right subtrees.

```
Preorder: [3, 9, 20, 15, 7]   → Root = 3 (first element)
Inorder:  [9, 3, 15, 20, 7]   → 9 is LEFT subtree, [15,20,7] is RIGHT subtree
```

### Step-by-Step Visualization

Let's trace through the algorithm visually:

```
Step 1: Preorder[0] = 3 → This is the ROOT

    Inorder:  [9, 3, 15, 20, 7]
                   ^
                 root

    Split around root:
    LEFT inorder:  [9]        (elements before 3)
    RIGHT inorder: [15, 20, 7] (elements after 3)

         3              ← root
        / \
       ?   ?            ← need to figure out children

Step 2: Preorder[1] = 9 → This is root of LEFT subtree
    LEFT preorder: [9]
    LEFT inorder:  [9]

    9 has no left/right children (single element)

         3
        / \
       9   ?

Step 3: Preorder[2] = 20 → This is root of RIGHT subtree
    RIGHT preorder: [20, 15, 7]
    RIGHT inorder:  [15, 20, 7]

    Inorder split around 20:
    LEFT:  [15]
    RIGHT: [7]

         3
        / \
       9   20
          /  \
         15   7

Step 4: Preorder[3] = 15 → leaf (no children in inorder)
Step 5: Preorder[4] = 7  → leaf

FINAL TREE:
         3
        / \
       9   20
          /  \
         15   7
```

### The Index Mapping Pattern

```
Preorder: [root | left_subtree | right_subtree]
           ^       ^              ^
           0     1 to mid    mid+1 to end

Inorder:  [left_subtree | root | right_subtree]
                    ^      ^       ^
                0 to mid-1  mid  mid+1 to end

If inorder has `mid` elements in left subtree:
  → Preorder[1 ... mid] = left subtree
  → Preorder[mid+1 ... end] = right subtree
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree_preorder_inorder(preorder, inorder):
    """Construct binary tree from preorder and inorder traversals.
    
    preorder[0] is always the root.
    In inorder, everything left of root index is left subtree,
    everything right is right subtree.
    """
    if not preorder or not inorder:
        return None
    
    root_val = preorder[0]
    root = TreeNode(root_val)
    
    # Find root in inorder to split
    mid = inorder.index(root_val)
    
    # Preorder: [root] [left_subtree] [right_subtree]
    # Inorder:  [left_subtree] [root] [right_subtree]
    root.left = build_tree_preorder_inorder(
        preorder[1:mid+1],      # Left subtree in preorder
        inorder[:mid]            # Left subtree in inorder
    )
    root.right = build_tree_preorder_inorder(
        preorder[mid+1:],        # Right subtree in preorder
        inorder[mid+1:]          # Right subtree in inorder
    )
    
    return root

# Example
preorder = [3, 9, 20, 15, 7]
inorder = [9, 3, 15, 20, 7]
root = build_tree_preorder_inorder(preorder, inorder)

# Time: O(n^2) worst case due to index() and slicing
# Space: O(n) for recursion + new arrays
```

### Optimized Version with HashMap (O(n))

**Why the naive version is slow:** `inorder.index(root_val)` is O(n) per call,
making the total O(n²). Using a hashmap reduces this to O(1) per lookup.

```python
def build_tree_optimized(preorder, inorder):
    """O(n) solution using hashmap for O(1) index lookup.
    
    Key idea:
    - Build a hashmap: value → index in inorder array
    - Use a pointer (pre_idx) to track current root in preorder
    - At each call, determine subtree boundaries using inorder indices
    """
    inorder_map = {val: idx for idx, val in enumerate(inorder)}
    pre_idx = [0]  # Mutable index to track current root in preorder
    
    def helper(in_start, in_end):
        # Base case: no elements to construct
        if in_start > in_end:
            return None
        
        # Current root from preorder (pre_idx advances left to right)
        root_val = preorder[pre_idx[0]]
        pre_idx[0] += 1
        
        root = TreeNode(root_val)
        
        # Find root position in inorder to determine subtree boundaries
        mid = inorder_map[root_val]
        
        # IMPORTANT: Build left subtree FIRST (preorder goes root → left → right)
        root.left = helper(in_start, mid - 1)    # Left subtree boundaries
        root.right = helper(mid + 1, in_end)      # Right subtree boundaries
        
        return root
    
    return helper(0, len(inorder) - 1)

# Time: O(n) — each node processed exactly once
# Space: O(n) for hashmap + O(h) for recursion stack (h = height)
```

### Walkthrough with HashMap Version

```
preorder = [3, 9, 20, 15, 7]
inorder  = [9, 3, 15, 20, 7]

inorder_map = {9:0, 3:1, 15:2, 20:3, 7:4}

Call 1: helper(0, 4)
  pre_idx=0, root_val=3, pre_idx→1
  mid = inorder_map[3] = 1
  Left:  helper(0, 0)  ← inorder indices [0..0]
  Right: helper(2, 4)  ← inorder indices [2..4]

Call 2: helper(0, 0)
  pre_idx=1, root_val=9, pre_idx→2
  mid = inorder_map[9] = 0
  Left:  helper(0, -1) → None
  Right: helper(1, 0) → None
  Returns: node(9)

Call 3: helper(2, 4)
  pre_idx=2, root_val=20, pre_idx→3
  mid = inorder_map[20] = 3
  Left:  helper(2, 2)  ← [15]
  Right: helper(4, 4)  ← [7]

Call 4: helper(2, 2)
  pre_idx=3, root_val=15, pre_idx→4
  Returns: node(15)

Call 5: helper(4, 4)
  pre_idx=4, root_val=7, pre_idx→5
  Returns: node(7)

Result:
     3
    / \
   9   20
      /  \
     15   7
```

---

## 2. Construct Tree from Inorder and Postorder

### Concept Walkthrough

**Key Insight:** Postorder gives root LAST, so we traverse in REVERSE.

```
Postorder: [9, 15, 7, 20, 3]   → Root = 3 (LAST element)
Inorder:   [9, 3, 15, 20, 7]   → Split around 3
```

### Step-by-Step Visualization

```
Step 1: Postorder[-1] = 3 → ROOT

    Inorder split around 3:
    LEFT:  [9]
    RIGHT: [15, 20, 7]

Step 2: Traverse postorder in REVERSE: 3, 20, 7, 15, 9
        (root → right → left order)

    Next in reverse postorder: 20 → RIGHT subtree root
    Inorder split around 20:
    LEFT:  [15]
    RIGHT: [7]

Step 3: Next: 7 → right child of 20
Step 4: Next: 15 → left child of 20
Step 5: Next: 9 → left child of 3

FINAL TREE:
         3
        / \
       9   20
          /  \
         15   7
```

### Reverse Postorder Ordering

```
Normal Postorder:  [9, 15, 7, 20, 3]  (left, right, root)
Reversed:          [3, 20, 7, 15, 9]  (root, right, left)

This means we process nodes as:
  root → right subtree → left subtree

So in the recursive helper, we must build RIGHT child FIRST:
    node.right = helper(mid + 1, in_end)    ← RIGHT first!
    node.left  = helper(in_start, mid - 1)  ← LEFT second
```

```python
def build_tree_inorder_postorder(inorder, postorder):
    """Construct binary tree from inorder and postorder.
    
    postorder[-1] is always the root.
    Traverse postorder from right to left.
    """
    if not inorder or not postorder:
        return None
    
    inorder_map = {val: idx for idx, val in enumerate(inorder)}
    post_idx = [len(postorder) - 1]  # Start from end
    
    def helper(in_start, in_end):
        if in_start > in_end:
            return None
        
        root_val = postorder[post_idx[0]]
        post_idx[0] -= 1
        
        root = TreeNode(root_val)
        mid = inorder_map[root_val]
        
        # Build RIGHT subtree first (reversed postorder hits right first)
        root.right = helper(mid + 1, in_end)
        root.left = helper(in_start, mid - 1)
        
        return root
    
    return helper(0, len(inorder) - 1)

# Example
inorder = [9, 3, 15, 20, 7]
postorder = [9, 15, 7, 20, 3]
root = build_tree_inorder_postorder(inorder, postorder)

# Time: O(n), Space: O(n)
```

**Common Mistake:** Building left subtree before right in postorder version. Since we traverse postorder in reverse (root → right → left), we must build right subtree FIRST.

---

## 3. Serialize and Deserialize Binary Tree

### Concept Walkthrough

Serialization = converting a tree to a string (for storage/transmission).
Deserialization = converting a string back to a tree.

```
Tree:
         1
        / \
       2   3
          / \
         4   5

Preorder with null markers:
  Visit 1 → Visit 2 → 2 has no left → "N"
                    → 2 has no right → "N"
              Visit 3 → Visit 4 → 4 has no left → "N"
                                 → 4 has no right → "N"
                           Visit 5 → 5 has no left → "N"
                                    → 5 has no right → "N"

Serialized: "1,2,N,N,3,4,N,N,5,N,N"
```

### Why Null Markers Are Necessary

```
Consider these two different trees:

Tree A:          Tree B:
    1                1
   /                  \
  2                    2

Without null markers, both serialize to: "1,2"
We can't tell which tree it is!

WITH null markers:
Tree A: "1,2,N,N"   (2 has no children, but is left child of 1)
Tree B: "1,N,2,N,N" (2 has no children, but is right child of 1)

Now they're distinguishable!
```

### Deserialization Walkthrough

```
Serialized: "1,2,N,N,3,4,N,N,5,N,N"
Token iterator: 1 → 2 → N → N → 3 → 4 → N → N → 5 → N → N

Step 1: Read "1" → create node(1)
  - Build left:  Read "2" → create node(2)
    - Build left:  Read "N" → None
    - Build right: Read "N" → None
    - Return node(2)
  - Build right: Read "3" → create node(3)
    - Build left:  Read "4" → create node(4)
      - Build left:  Read "N" → None
      - Build right: Read "N" → None
      - Return node(4)
    - Build right: Read "5" → create node(5)
      - Build left:  Read "N" → None
      - Build right: Read "N" → None
      - Return node(5)
    - Return node(3)
  - Return node(1)

Result:
     1
    / \
   2   3
      / \
     4   5  ✓
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:
    """Convert tree to string and back.
    
    Uses preorder with 'N' for null nodes.
    Example: [1, 2, 3, None, None, 4, 5]
    Serialized: "1,2,N,N,3,4,N,N,5,N,N"
    """
    
    def serialize(self, root):
        """Encodes a tree to a single string."""
        result = []
        
        def dfs(node):
            if not node:
                result.append("N")
                return
            result.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        
        dfs(root)
        return ",".join(result)
    
    def deserialize(self, data):
        """Decodes a string back to a tree."""
        tokens = iter(data.split(","))
        
        def dfs():
            val = next(tokens)
            if val == "N":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node
        
        return dfs()

# Usage
codec = Codec()
root = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
serialized = codec.serialize(root)
# "1,2,N,N,3,4,N,N,5,N,N"
deserialized = codec.deserialize(serialized)

# Time: O(n) for both serialize and deserialize
# Space: O(n) for the string and recursion stack
```

### Level-Order Serialization

```python
from collections import deque

class LevelOrderCodec:
    """Level-order serialization matching LeetCode format."""
    
    def serialize(self, root):
        """BFS serialization."""
        if not root:
            return ""
        
        result = []
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("N")
        
        # Remove trailing Nones
        while result and result[-1] == "N":
            result.pop()
        
        return ",".join(result)
    
    def deserialize(self, data):
        """BFS deserialization."""
        if not data:
            return None
        
        tokens = data.split(",")
        root = TreeNode(int(tokens[0]))
        queue = deque([root])
        i = 1
        
        while queue and i < len(tokens):
            node = queue.popleft()
            
            if i < len(tokens) and tokens[i] != "N":
                node.left = TreeNode(int(tokens[i]))
                queue.append(node.left)
            i += 1
            
            if i < len(tokens) and tokens[i] != "N":
                node.right = TreeNode(int(tokens[i]))
                queue.append(node.right)
            i += 1
        
        return root

# Time: O(n), Space: O(n)
```

---

## 4. Construct BST from Preorder Traversal

### Concept Walkthrough

**Key Insight:** BST property lets us use bounds instead of inorder array.

```
BST Property:  left < root < right  (for ALL nodes)

preorder = [10, 5, 1, 7, 40, 50]

Step-by-step with bounds:
─────────────────────────────────────────────
Process 10: bounds = (-∞, +∞) → 10 fits → create node
  Process 5:  bounds = (-∞, 10) → 5 fits → create node
    Process 1:  bounds = (-∞, 5)  → 1 fits → create node
    Process 7:  bounds = (5, 10)  → 7 fits → create node
  Process 40: bounds = (10, +∞) → 40 fits → create node
    Process 50: bounds = (40, +∞) → 50 fits → create node
─────────────────────────────────────────────

Result:
        10
       /  \
      5    40
     / \     \
    1   7     50
```

### Visual Trace of Bounds

```
preorder = [10, 5, 1, 7, 40, 50]

idx=0: val=10, bounds=(-∞, +∞) ✓
                    10
                   /  \

idx=1: val=5,  bounds=(-∞, 10) ✓  ← must be < 10
                    10
                   /
                  5

idx=2: val=1,  bounds=(-∞, 5)  ✓  ← must be < 5
                    10
                   /
                  5
                 /
                1

idx=3: val=7,  bounds=(5, 10)   ✓  ← must be > 5 AND < 10
                    10
                   /
                  5
                 / \
                1   7

idx=4: val=40, bounds=(10, +∞) ✓  ← must be > 10
                    10
                   /  \
                  5    40

idx=5: val=50, bounds=(40, +∞) ✓  ← must be > 40
                    10
                   /  \
                  5    40
                        \
                         50

DONE! ✓
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def bst_from_preorder(preorder):
    """Construct BST from preorder traversal.
    
    BST property: left < root < right.
    First element of preorder is always the root.
    Use bounds to decide placement.
    
    preorder = [10, 5, 1, 7, 40, 50]
    Output:
          10
         /  \
        5    40
       / \     \
      1   7     50
    """
    idx = [0]
    
    def helper(lower, upper):
        if idx[0] >= len(preorder):
            return None
        
        val = preorder[idx[0]]
        if val < lower or val > upper:
            return None
        
        node = TreeNode(val)
        idx[0] += 1
        
        # Left subtree: all values must be < val
        node.left = helper(lower, val)
        # Right subtree: all values must be > val
        node.right = helper(val, upper)
        
        return node
    
    return helper(float('-inf'), float('inf'))

# Time: O(n), Space: O(h)
```

### Alternative: Using Inorder + Preorder (with BST property)

```python
def bst_from_preorder_inorder(preorder):
    """Use BST property: inorder of BST is sorted.
    So we can derive inorder from preorder by sorting.
    """
    inorder = sorted(preorder)
    
    inorder_map = {val: idx for idx, val in enumerate(inorder)}
    pre_idx = [0]
    
    def helper(in_start, in_end):
        if in_start > in_end:
            return None
        
        val = preorder[pre_idx[0]]
        pre_idx[0] += 1
        
        node = TreeNode(val)
        mid = inorder_map[val]
        
        node.left = helper(in_start, mid - 1)
        node.right = helper(mid + 1, in_end)
        
        return node
    
    return helper(0, len(inorder) - 1)

# Time: O(n log n) for sorting, Space: O(n)
```

---

## 5. Construct Binary Tree from String

### Concept Walkthrough

**String Format:** `root(left_subtree)(right_subtree)`
Numbers can be negative: `-4(2)(1)`

```
String: "4(2(3)(1))(6(5))"

Parse tree:
"4" → root node with value 4
"(2(3)(1))" → left subtree string
"(6(5))" → right subtree string

Left subtree: "2(3)(1)"
  "2" → root = 2
  "(3)" → left child = 3
  "(1)" → right child = 1

Right subtree: "6(5)"
  "6" → root = 6
  "(5)" → left child = 5

Result:
        4
       / \
      2   6
     / \ /
    3  1 5
```

### Parsing Strategy

```
String: "4(2(3)(1))(6(5))"

Key observations:
1. A number is always followed by optional '(' for children
2. Each '(' starts a child, matched by ')'
3. After one child's ')', another '(' means second child

Parsing state machine:
  ┌─────────────┐
  │ Parse Number │ ← Always start here
  └──────┬──────┘
         │
    ┌────▼────┐     No '('    ┌────────┐
    │ '(' ?   │──────────────►│ Return │
    └────┬────┘               │  Node  │
         │ Yes                 └────────┘
    ┌────▼──────────┐
    │ Parse Left     │ ← Recurse inside '(' ... ')'
    │ Child          │
    └────┬──────────┘
         │
    ┌────▼────┐     No '('    ┌────────┐
    │ '(' ?   │──────────────►│ Return │
    └────┬────┘               │  Node  │
         │ Yes                 └────────┘
    ┌────▼──────────┐
    │ Parse Right    │ ← Recurse inside '(' ... ')'
    │ Child          │
    └───────────────┘
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def str2tree(s):
    """Convert string like "4(2(3)(1))(6(5))" to binary tree.
    
    Format: root(left_subtree)(right_subtree)
    Numbers can be negative: "-4(2)(1)"
    """
    if not s:
        return None
    
    idx = [0]
    
    def parse_number():
        """Parse a possibly negative number."""
        negative = False
        if s[idx[0]] == '-':
            negative = True
            idx[0] += 1
        
        num = 0
        while idx[0] < len(s) and s[idx[0]].isdigit():
            num = num * 10 + int(s[idx[0]])
            idx[0] += 1
        
        return -num if negative else num
    
    def parse():
        if idx[0] >= len(s) or s[idx[0]] == ')':
            return None
        
        val = parse_number()
        node = TreeNode(val)
        
        # Check for left child
        if idx[0] < len(s) and s[idx[0]] == '(':
            idx[0] += 1  # skip '('
            node.left = parse()
            idx[0] += 1  # skip ')'
        
        # Check for right child
        if idx[0] < len(s) and s[idx[0]] == '(':
            idx[0] += 1  # skip '('
            node.right = parse()
            idx[0] += 1  # skip ')'
        
        return node
    
    return parse()

# Examples
root1 = str2tree("4(2(3)(1))(6(5))")
root2 = str2tree("-4(2(3)(1))(6(5))")
root3 = str2tree("10(5(3)(7))(15)")

# Time: O(n), Space: O(h)
```

### Using Stack Approach

```python
def str2tree_stack(s):
    """Stack-based approach for parsing tree string."""
    if not s:
        return None
    
    stack = []
    i = 0
    
    while i < len(s):
        if s[i].isdigit() or s[i] == '-':
            # Parse number
            j = i
            if s[i] == '-':
                i += 1
            while i < len(s) and s[i].isdigit():
                i += 1
            num = int(s[j:i])
            node = TreeNode(num)
            
            if stack:
                parent = stack[-1]
                if not parent.left:
                    parent.left = node
                else:
                    parent.right = node
            
            stack.append(node)
        
        elif s[i] == ')':
            stack.pop()
        
        i += 1
    
    return stack[0] if stack else None

# Time: O(n), Space: O(n)
```

---

## Quick Reference

| Problem | Key Idea | Time | Space |
|---------|----------|------|-------|
| Inorder + Preorder | Preorder[0] = root, split inorder | O(n) | O(n) |
| Inorder + Postorder | Postorder[-1] = root, reverse traverse | O(n) | O(n) |
| Serialize/Deserialize | Preorder with null markers | O(n) | O(n) |
| BST from Preorder | Use bounds to place nodes | O(n) | O(h) |
| String to Tree | Recursive parsing with parentheses | O(n) | O(h) |

### When to Use Each Construction Method

```
╔══════════════════════════════════════════════════════════════════════╗
║  Given Preorder + Inorder?     → Standard recursive split         ║
║  Given Postorder + Inorder?    → Reverse postorder traversal       ║
║  Given Preorder only (BST)?    → Bounds-based approach             ║
║  Need to transmit/store tree?  → Serialize with null markers       ║
║  String with parentheses?      → Recursive parser or stack         ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Common Pitfalls

1. **Postorder: build RIGHT first** — reversing postorder gives root→right→left
2. **Forgetting null markers** — without them, different trees serialize the same
3. **Slicing arrays** — creates copies, leading to O(n²) time; use indices instead
4. **BST from preorder** — don't sort to get inorder; use bounds approach for O(n)
5. **Empty subtrees** — always handle `None` inputs at the start of recursion

### Interview Tips
- For construction problems, always clarify: are there duplicate values?
- Inorder + one other traversal uniquely defines a tree (no duplicates)
- Preorder + Postorder alone is NOT sufficient (multiple trees possible)
- BST from preorder: exploit BST property (bounds approach is cleanest)
- Serialization: mention trade-offs between preorder vs level-order
