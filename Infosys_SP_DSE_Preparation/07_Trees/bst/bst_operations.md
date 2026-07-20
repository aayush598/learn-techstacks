# Binary Search Tree (BST) Operations

## Table of Contents
1. [BST Search](#1-bst-search)
2. [BST Insert](#2-bst-insert)
3. [BST Delete](#3-bst-delete)
4. [Validate BST](#4-validate-bst)
5. [Lowest Common Ancestor in BST](#5-lowest-common-ancestor-in-bst)
6. [Kth Smallest Element in BST](#6-kth-smallest-element-in-bst)
7. [Kth Largest Element in BST](#7-kth-largest-element-in-bst)
8. [Inorder Successor and Predecessor](#8-inorder-successor-and-predecessor)
9. [Convert Sorted Array to BST](#9-convert-sorted-array-to-bst)
10. [Two Sum in BST](#10-two-sum-in-bst)
11. [BST Iterator](#11-bst-iterator)

---

## BST Property

```
For every node:
  - All values in LEFT subtree < node.val
  - All values in RIGHT subtree > node.val
  - Inorder traversal gives SORTED order
```

---

## 1. BST Search

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def search_bst(root, val):
    """Search for a value in BST.
    
    At each node:
      - val == node.val → found
      - val < node.val  → go left
      - val > node.val  → go right
    """
    if not root or root.val == val:
        return root
    
    if val < root.val:
        return search_bst(root.left, val)
    else:
        return search_bst(root.right, val)

# Iterative version
def search_bst_iterative(root, val):
    """Iterative BST search — preferred (no recursion overhead)."""
    while root and root.val != val:
        root = root.left if val < root.val else root.right
    return root

# Time: O(h) — O(log n) balanced, O(n) skewed
# Space: O(h) recursive, O(1) iterative
```

---

## 2. BST Insert

```python
def insert_into_bst(root, val):
    """Insert a value into BST.
    
    If root is None, create new node.
    Otherwise, recurse to correct position.
    """
    if not root:
        return TreeNode(val)
    
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    elif val > root.val:
        root.right = insert_into_bst(root.right, val)
    
    return root

# Iterative version
def insert_bst_iterative(root, val):
    """Iterative insertion."""
    new_node = TreeNode(val)
    
    if not root:
        return new_node
    
    current = root
    while True:
        if val < current.val:
            if not current.left:
                current.left = new_node
                break
            current = current.left
        else:
            if not current.right:
                current.right = new_node
                break
            current = current.right
    
    return root

# Time: O(h), Space: O(h) recursive / O(1) iterative
```

---

## 3. BST Delete

```python
def delete_node(root, key):
    """Delete a node from BST.
    
    Three cases:
    1. Node is a leaf → simply remove it
    2. Node has one child → replace with child
    3. Node has two children → replace with inorder successor
       (smallest in right subtree), then delete successor
    """
    if not root:
        return None
    
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        # Found the node to delete
        
        # Case 1 & 2: No child or one child
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        
        # Case 3: Two children
        # Find inorder successor (smallest in right subtree)
        successor = find_min(root.right)
        root.val = successor.val
        root.right = delete_node(root.right, successor.val)
    
    return root


def find_min(node):
    """Find the minimum value node (leftmost)."""
    while node.left:
        node = node.left
    return node

# Time: O(h), Space: O(h)
```

### Iterative Delete

```python
def delete_node_iterative(root, key):
    """Iterative BST delete."""
    parent = None
    current = root
    
    # Find the node
    while current and current.val != key:
        parent = current
        current = current.left if key < current.val else current.right
    
    if not current:
        return root  # Key not found
    
    # Node has two children
    if current.left and current.right:
        # Find inorder successor
        successor_parent = current
        successor = current.right
        while successor.left:
            successor_parent = successor
            successor = successor.left
        
        # Replace current with successor
        current.val = successor.val
        # Delete successor (it has at most one right child)
        current = successor
        parent = successor_parent
    
    # Node has at most one child
    child = current.left if current.left else current.right
    
    if not parent:
        # Deleting root
        return child
    
    if parent.left == current:
        parent.left = child
    else:
        parent.right = child
    
    return root

# Time: O(h), Space: O(1)
```

---

## 4. Validate BST

```python
def is_valid_bst(root):
    """Check if tree is a valid BST.
    
    WRONG approach: just check node.left < node < node.right
    Correct: every node must be within (min, max) bounds.
    """
    
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))

# Time: O(n), Space: O(h)
```

### Inorder Approach

```python
def is_valid_bst_inorder(root):
    """Valid BST has strictly increasing inorder traversal."""
    stack = []
    current = root
    prev = float('-inf')
    
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        
        current = stack.pop()
        
        # Inorder should be strictly increasing
        if current.val <= prev:
            return False
        prev = current.val
        
        current = current.right
    
    return True

# Time: O(n), Space: O(h)
```

---

## 5. Lowest Common Ancestor in BST

```python
def lca_bst(root, p, q):
    """LCA in BST using BST property.
    
    If both p, q < root → LCA is in left subtree
    If both p, q > root → LCA is in right subtree
    Otherwise, root is the LCA (split point)
    """
    current = root
    
    while current:
        if p.val < current.val and q.val < current.val:
            current = current.left
        elif p.val > current.val and q.val > current.val:
            current = current.right
        else:
            # Split point — this is the LCA
            return current
    
    return None

# Time: O(h), Space: O(1)
```

---

## 6. Kth Smallest Element in BST

```python
def kth_smallest(root, k):
    """Kth smallest = kth element in inorder traversal.
    
    Inorder of BST is sorted in ascending order.
    """
    stack = []
    current = root
    
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        
        current = stack.pop()
        k -= 1
        
        if k == 0:
            return current.val
        
        current = current.right
    
    return -1  # Should not reach here if k is valid

# Time: O(k + h), Space: O(h)
```

### Recursive Approach

```python
def kth_smallest_recursive(root, k):
    """Recursive inorder with early termination."""
    result = None
    count = [0]
    
    def inorder(node):
        nonlocal result
        if not node or result is not None:
            return
        
        inorder(node.left)
        count[0] += 1
        if count[0] == k:
            result = node.val
            return
        inorder(node.right)
    
    inorder(root)
    return result

# Time: O(k + h), Space: O(h)
```

---

## 7. Kth Largest Element in BST

```python
def kth_largest(root, k):
    """Kth largest = (n - k + 1)th smallest.
    
    OR use reverse inorder (Right → Root → Left).
    """
    stack = []
    current = root
    
    while current or stack:
        while current:
            stack.append(current)
            current = current.right  # Go right first for descending
        
        current = stack.pop()
        k -= 1
        
        if k == 0:
            return current.val
        
        current = current.left
    
    return -1

# Time: O(k + h), Space: O(h)
```

### Using Count

```python
def kth_largest_count(root, k):
    """Count nodes, then find (count - k + 1)th smallest."""
    def count_nodes(node):
        if not node:
            return 0
        return 1 + count_nodes(node.left) + count_nodes(node.right)
    
    total = count_nodes(node)
    return kth_smallest(root, total - k + 1)

# Time: O(n + k + h), Space: O(h)
```

---

## 8. Inorder Successor and Predecessor

```python
def inorder_successor(root, p):
    """Find the node with smallest value greater than p.val.
    
    Two cases:
    1. p has right subtree → successor is leftmost in right subtree
    2. p has no right subtree → successor is the deepest ancestor
       where we went left
    """
    successor = None
    current = root
    
    while current:
        if p.val < current.val:
            successor = current
            current = current.left
        else:
            current = current.right
    
    return successor

# Time: O(h), Space: O(1)
```

```python
def inorder_predecessor(root, p):
    """Find the node with largest value smaller than p.val.
    
    Two cases:
    1. p has left subtree → predecessor is rightmost in left subtree
    2. p has no left subtree → predecessor is the deepest ancestor
       where we went right
    """
    predecessor = None
    current = root
    
    while current:
        if p.val > current.val:
            predecessor = current
            current = current.right
        else:
            current = current.left
    
    return predecessor

# Time: O(h), Space: O(1)
```

---

## 9. Convert Sorted Array to BST

```python
def sorted_array_to_bst(nums):
    """Convert sorted array to height-balanced BST.
    
    Height-balanced: depth of two subtrees of every node differs by at most 1.
    
    nums = [-10, -3, 0, 5, 9]
    Output:      0
                / \
              -3   5
              /     \
            -10      9
    """
    if not nums:
        return None
    
    def helper(left, right):
        if left > right:
            return None
        
        mid = (left + right) // 2
        node = TreeNode(nums[mid])
        
        node.left = helper(left, mid - 1)
        node.right = helper(mid + 1, right)
        
        return node
    
    return helper(0, len(nums) - 1)

# Time: O(n), Space: O(log n) for recursion (balanced tree)
```

### Convert Sorted Linked List to BST

```python
def sorted_list_to_bst(head):
    """Convert sorted linked list to height-balanced BST.
    Uses fast-slow pointer to find middle.
    """
    if not head:
        return None
    if not head.next:
        return TreeNode(head.val)
    
    # Find middle using slow-fast pointers
    prev = None
    slow = head
    fast = head
    
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next
    
    # Disconnect left half
    if prev:
        prev.next = None
    
    root = TreeNode(slow.val)
    root.left = sorted_list_to_bst(head)
    root.right = sorted_list_to_bst(slow.next)
    
    return root

# Time: O(n log n), Space: O(log n)
```

---

## 10. Two Sum in BST

```python
def two_sum_bst(root, k):
    """Check if there exist two nodes whose values sum to k.
    
    Approach 1: Use BST Iterator (two pointers from both ends)
    Approach 2: Inorder + Two Sum (sorted array approach)
    """
    
    # Approach 1: Inorder into sorted list
    def inorder(node, result):
        if not node:
            return
        inorder(node.left, result)
        result.append(node.val)
        inorder(node.right, result)
    
    nums = []
    inorder(root, nums)
    
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == k:
            return True
        elif current_sum < k:
            left += 1
        else:
            right -= 1
    
    return False

# Time: O(n), Space: O(n)
```

### Optimized with HashSet (One Pass)

```python
def two_sum_bst_hashset(root, k):
    """Using HashSet for O(n) time, O(n) space."""
    seen = set()
    
    def dfs(node):
        if not node:
            return False
        
        complement = k - node.val
        if complement in seen:
            return True
        
        seen.add(node.val)
        
        return dfs(node.left) or dfs(node.right)
    
    return dfs(root)

# Time: O(n), Space: O(n)
```

---

## 11. BST Iterator

```python
class BSTIterator:
    """Iterator that returns next smallest element in BST.
    
    Uses stack to simulate inorder traversal.
    Next() and HasNext() should run in O(1) amortized time.
    Space: O(h).
    """
    
    def __init__(self, root):
        self.stack = []
        self._push_left(root)
    
    def _push_left(self, node):
        """Push all left children onto stack."""
        while node:
            self.stack.append(node)
            node = node.left
    
    def next(self) -> int:
        """Return next smallest element."""
        node = self.stack.pop()
        # If right child exists, push all its left children
        if node.right:
            self._push_left(node.right)
        return node.val
    
    def has_next(self) -> bool:
        """Check if there are more elements."""
        return len(self.stack) > 0

# Usage
# iter = BSTIterator(root)
# while iter.has_next():
#     print(iter.next())

# Time: O(1) amortized per next(), O(h) space
```

### Iterator with O(1) Space (Morris-like)

```python
class BSTIteratorFlattened:
    """Flatten BST to right-skewed tree during init.
    O(n) init, O(1) next, O(1) space (modifying tree)."""
    
    def __init__(self, root):
        self.curr = None
        self._reverse_inorder(root)  # Process in reverse
        # This approach modifies the tree
        # Not recommended if tree must be preserved
```

---

## Quick Reference Table

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Search | O(h) | O(1) iterative | Use BST property |
| Insert | O(h) | O(1) iterative | Find position, attach |
| Delete | O(h) | O(h) recursive | 3 cases: leaf, 1 child, 2 children |
| Validate BST | O(n) | O(h) | Use bounds or inorder |
| LCA in BST | O(h) | O(1) | Split point where paths diverge |
| Kth smallest | O(k+h) | O(h) | Inorder traversal |
| Kth largest | O(k+h) | O(h) | Reverse inorder |
| Successor | O(h) | O(1) | Leftmost in right or ancestor |
| Predecessor | O(h) | O(1) | Rightmost in left or ancestor |
| Sorted array → BST | O(n) | O(log n) | Middle element as root |
| Two Sum in BST | O(n) | O(n) | HashSet or sorted array |
| BST Iterator | O(1) amortized | O(h) | Stack-based inorder |

> **h** = height: O(log n) for balanced BST, O(n) for skewed BST

**Interview Tips:**
- BST inorder traversal gives sorted order — this is the most powerful property
- For Kth element problems, think inorder traversal
- For LCA in BST, use BST property to avoid scanning entire tree
- Validate BST: always use range bounds, never just compare with immediate children
- BST Iterator is a common design problem — understand the amortized O(1) approach
