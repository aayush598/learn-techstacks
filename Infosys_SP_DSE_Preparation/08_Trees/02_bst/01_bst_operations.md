# Binary Search Tree (BST) Operations - Complete Guide

## What is a BST?

A Binary Search Tree is a binary tree with a special property:
- **Left subtree** contains only values **less than** node's value
- **Right subtree** contains only values **greater than** node's value

### Visual: BST Property

```
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13

For node 8:
  Left subtree: {1, 3, 4, 6, 7} — ALL < 8 ✓
  Right subtree: {10, 13, 14} — ALL > 8 ✓

For node 3:
  Left subtree: {1} — ALL < 3 ✓
  Right subtree: {4, 6, 7} — ALL > 3 ✓
```

### Key Property: Inorder Traversal is SORTED!

```
Inorder traversal of BST:
1 → 3 → 4 → 6 → 7 → 8 → 10 → 13 → 14

This is SORTED order! ✓
```

---

## 1. BST Search

**Problem:** Find if a value exists in BST.

**Approach:** Use BST property to eliminate half the tree at each step.

### Visual: Search for 6

```
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13

Step 1: Compare 6 with 8
        6 < 8 → go LEFT
        
        8
       /
      3
     / \
    1   6
       / \
      4   7

Step 2: Compare 6 with 3
        6 > 3 → go RIGHT
        
        3
         \
          6
         / \
        4   7

Step 3: Compare 6 with 6
        6 == 6 → FOUND! ✓
```

### The Code:
```python
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

# Iterative version (preferred)
def search_bst_iterative(root, val):
    """Iterative BST search — no recursion overhead."""
    while root and root.val != val:
        root = root.left if val < root.val else root.right
    return root
```

**Time:** O(h) — O(log n) balanced, O(n) skewed | **Space:** O(1) iterative

---

## 2. BST Insert

**Problem:** Insert a value into BST.

**Approach:** Find correct position (like search), then attach new node.

### Visual: Insert 5 into BST

```
Before:
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13

Insert 5:
Step 1: Compare with 8 → 5 < 8 → go left
Step 2: Compare with 3 → 5 > 3 → go right
Step 3: Compare with 6 → 5 < 6 → go left
Step 4: 6.left is None → insert here!

After:
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13
     /
    5  ← NEW NODE!
```

### The Code:
```python
def insert_into_bst(root, val):
    """Insert a value into BST."""
    if not root:
        return TreeNode(val)
    
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    elif val > root.val:
        root.right = insert_into_bst(root.right, val)
    
    return root
```

**Time:** O(h) | **Space:** O(h) recursive / O(1) iterative

---

## 3. BST Delete

**Problem:** Delete a node from BST.

**Three Cases:**
1. **Leaf node** → Simply remove it
2. **One child** → Replace with child
3. **Two children** → Replace with inorder successor (smallest in right subtree)

### Visual: Delete 3 (Two Children Case)

```
Before:
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13

Delete 3:
Step 1: Find node 3 (has two children)
Step 2: Find inorder successor = 4 (smallest in right subtree)
Step 3: Replace 3 with 4
Step 4: Delete 4 from right subtree

After:
        8
       / \
      4   10
     / \    \
    1   6    14
       / \   /
      5   7 13
```

### Visual: Delete 10 (One Child Case)

```
Before:
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13

Delete 10:
Step 1: Find node 10 (has one child: 14)
Step 2: Replace 10 with 14

After:
        8
       / \
      3   14
     / \   /
    1   6 13
       / \
      4   7
```

### The Code:
```python
def delete_node(root, key):
    """Delete a node from BST."""
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
```

**Time:** O(h) | **Space:** O(h)

---

## 4. Validate BST

**Problem:** Check if tree is a valid BST.

**Wrong Approach:** Just check `node.left < node < node.right`

**Correct Approach:** Every node must be within (min, max) bounds!

### Visual: Why Bounds Matter

```
Invalid BST:
        5
       / \
      1   6
         / \
        3   7
        
Node 3 is in right subtree of 5, but 3 < 5!
This violates BST property!

Using bounds:
- Node 5: (-inf, inf) ✓
- Node 1: (-inf, 5) ✓
- Node 6: (5, inf) ✓
- Node 3: (5, 6) ✗ — 3 is NOT > 5!
```

### The Code:
```python
def is_valid_bst(root):
    """Check if tree is a valid BST using bounds."""
    
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))
```

**Time:** O(n) | **Space:** O(h)

---

## 5. Lowest Common Ancestor in BST

**Problem:** Find LCA of two nodes in BST.

**Key Insight:** Use BST property! If both nodes are on same side, go that way. Otherwise, current node is LCA.

### Visual: LCA of 4 and 14

```
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13

LCA(4, 14):
Step 1: Compare with 8
        4 < 8 and 14 > 8 → SPLIT!
        LCA is 8 ✓

LCA(4, 7):
Step 1: Compare with 8
        4 < 8 and 7 < 8 → go LEFT
        
Step 2: Compare with 3
        4 > 3 and 7 > 3 → go RIGHT
        
Step 3: Compare with 6
        4 < 6 and 7 > 6 → SPLIT!
        LCA is 6 ✓
```

### The Code:
```python
def lca_bst(root, p, q):
    """LCA in BST using BST property."""
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
```

**Time:** O(h) | **Space:** O(1)

---

## 6. Kth Smallest Element in BST

**Problem:** Find kth smallest element.

**Key Insight:** Inorder traversal of BST gives sorted order!

### Visual: 3rd Smallest

```
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13

Inorder: 1, 3, 4, 6, 7, 8, 10, 13, 14
         1  2  3  4  5  6   7   8   9
                ↑
           3rd smallest = 4
```

### The Code:
```python
def kth_smallest(root, k):
    """Kth smallest = kth element in inorder traversal."""
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
    
    return -1
```

**Time:** O(k + h) | **Space:** O(h)

---

## 7. Convert Sorted Array to BST

**Problem:** Convert sorted array to height-balanced BST.

**Approach:** Pick middle element as root, recursively build left and right subtrees.

### Visual: Convert [-10, -3, 0, 5, 9]

```
Step 1: Pick middle (0) as root
        [-10, -3, 0, 5, 9]
                     ↑
                    root

Step 2: Left subarray [-10, -3]
        Pick middle (-3) as left child
        
              0
             /
           -3

Step 3: Right subarray [5, 9]
        Pick middle (5) as right child
        
              0
             / \
           -3   5

Step 4: Left of -3: [-10]
        Pick -10 as left child of -3
        
              0
             / \
           -3   5
           /
         -10

Step 5: Right of 5: [9]
        Pick 9 as right child of 5
        
              0
             / \
           -3   5
           /     \
         -10      9

Final BST is height-balanced! ✓
```

### The Code:
```python
def sorted_array_to_bst(nums):
    """Convert sorted array to height-balanced BST."""
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
```

**Time:** O(n) | **Space:** O(log n) for recursion

---

## 8. Two Sum in BST

**Problem:** Find two nodes that sum to target.

**Approach:** Inorder traversal gives sorted array, then use two pointers!

### Visual: Two Sum = 9

```
        8
       / \
      3   10
     / \    \
    1   6    14

Inorder: [1, 3, 6, 8, 10, 14]

Two pointers:
  left=0 (1), right=5 (14): 1+14=15 > 9 → right--
  left=0 (1), right=4 (10): 1+10=11 > 9 → right--
  left=0 (1), right=3 (8): 1+8=9 ✓ FOUND!
  
Return True (nodes 1 and 8)
```

### The Code:
```python
def two_sum_bst(root, k):
    """Check if two nodes sum to k."""
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
```

**Time:** O(n) | **Space:** O(n)

---

## Quick Reference

| Operation | Time | Space | Key Insight |
|-----------|------|-------|-------------|
| Search | O(h) | O(1) | Use BST property |
| Insert | O(h) | O(1) | Find position, attach |
| Delete | O(h) | O(h) | 3 cases: leaf, 1 child, 2 children |
| Validate | O(n) | O(h) | Use bounds |
| LCA | O(h) | O(1) | Split point |
| Kth smallest | O(k+h) | O(h) | Inorder traversal |
| Convert array | O(n) | O(log n) | Middle as root |
| Two Sum | O(n) | O(n) | Inorder + two pointers |

> **h** = height: O(log n) balanced, O(n) skewed

## Key Insights

1. **Inorder traversal gives sorted order** — most powerful property!
2. **Kth element problems** → think inorder traversal
3. **LCA in BST** → use BST property to avoid scanning entire tree
4. **Validate BST** → always use range bounds, not just compare with children
5. **BST Iterator** → stack-based inorder simulation
