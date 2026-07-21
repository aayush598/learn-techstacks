# Binary Tree Construction

## Table of Contents
1. [Construct Tree from Inorder and Preorder](#1-construct-tree-from-inorder-and-preorder)
2. [Construct Tree from Inorder and Postorder](#2-construct-tree-from-inorder-and-postorder)
3. [Serialize and Deserialize Binary Tree](#3-serialize-and-deserialize-binary-tree)
4. [Construct BST from Preorder Traversal](#4-construct-bst-from-preorder-traversal)
5. [Construct Binary Tree from String](#5-construct-binary-tree-from-string)

---

## 1. Construct Tree from Inorder and Preorder

**Key Insight:** Preorder gives root first, inorder splits into left/right subtrees.

```
Preorder: [3, 9, 20, 15, 7]   → Root = 3 first
Inorder:  [9, 3, 15, 20, 7]   → 9 is left subtree, [15,20,7] is right subtree
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

```python
def build_tree_optimized(preorder, inorder):
    """O(n) solution using hashmap for O(1) index lookup."""
    inorder_map = {val: idx for idx, val in enumerate(inorder)}
    pre_idx = [0]  # Mutable index to track current root in preorder
    
    def helper(in_start, in_end):
        if in_start > in_end:
            return None
        
        root_val = preorder[pre_idx[0]]
        pre_idx[0] += 1
        
        root = TreeNode(root_val)
        mid = inorder_map[root_val]
        
        # Build left subtree first (preorder: root, left, right)
        root.left = helper(in_start, mid - 1)
        root.right = helper(mid + 1, in_end)
        
        return root
    
    return helper(0, len(inorder) - 1)

# Time: O(n), Space: O(n) for hashmap + O(h) for recursion
```

---

## 2. Construct Tree from Inorder and Postorder

**Key Insight:** Postorder gives root last, so traverse in reverse.

```
Postorder: [9, 15, 7, 20, 3]   → Root = 3 (last element)
Inorder:   [9, 3, 15, 20, 7]   → Split around 3
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

**Interview Tips:**
- For construction problems, always clarify: are there duplicate values?
- Inorder + one other traversal uniquely defines a tree (no duplicates)
- Preorder + Postorder alone is NOT sufficient (multiple trees possible)
- BST from preorder: exploit BST property (bounds approach is cleanest)
- Serialization: mention trade-offs between preorder vs level-order
