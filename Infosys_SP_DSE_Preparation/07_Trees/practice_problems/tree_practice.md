# Trees Practice Problems — Infosys SP DSE

## 20 Problems Organized by Difficulty

---

## EASY (5 Problems)

### 1. Maximum Depth of Binary Tree

**Problem:** Given a binary tree, find its maximum depth. Maximum depth is the number of nodes along the longest path from root to the farthest leaf node.

**Example:**
```
Input:     3
          / \
         9  20
            /  \
           15   7
Output: 3
```

**Approach:** Recursively find depth of left and right subtrees, return 1 + max.

```python
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# Time: O(n), Space: O(h) where h is height
```

---

### 2. Same Tree

**Problem:** Given two binary trees, check if they are identical (same structure and same node values).

**Example:**
```
Tree 1:     1         Tree 2:     1
           / \                   / \
          2   3                 2   3
Output: True
```

**Approach:** Recursively compare both trees — both None → True, one None → False, values differ → False, otherwise recurse on children.

```python
def is_same_tree(p, q):
    if not p and not q:
        return True
    if not p or not q:
        return False
    return (p.val == q.val and
            is_same_tree(p.left, q.left) and
            is_same_tree(p.right, q.right))

# Time: O(n), Space: O(h)
```

---

### 3. Invert Binary Tree

**Problem:** Invert (mirror) a binary tree — swap left and right children of every node.

**Example:**
```
Input:      4             Output:      4
           / \                        / \
          2   7                      7   2
         / \ / \                    / \ / \
        1  3 6  9                  9  6 3  1
```

**Approach:** Post-order DFS — recurse to children first, then swap. Or swap first, then recurse.

```python
def invert_tree(root):
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

---

### 4. Subtree of Another Tree

**Problem:** Given two binary trees `root` and `subRoot`, check if `subRoot` is a subtree of `root`. A subtree must be a complete downward tree.

**Example:**
```
root:      3          subRoot:   4
          / \                   / \
         4   5                 1   2
        / \
       1   2
Output: True (subRoot is subtree of root's left child)
```

**Approach:** For each node in root, check if the subtree rooted there is identical to subRoot.

```python
def is_subtree(root, subRoot):
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

# Time: O(m * n), Space: O(h)
```

---

### 5. Diameter of Binary Tree

**Problem:** Find the length of the longest path between any two nodes (number of edges). Path may or may not pass through root.

**Example:**
```
Input:     1
          / \
         2   3
        / \
       4   5
Output: 3 (path: 4 → 2 → 1 → 3)
```

**Approach:** At each node, diameter = left_depth + right_depth. Track global max.

```python
def diameter_of_binary_tree(root):
    max_diameter = [0]
    
    def depth(node):
        if not node:
            return 0
        left = depth(node.left)
        right = depth(node.right)
        max_diameter[0] = max(max_diameter[0], left + right)
        return 1 + max(left, right)
    
    depth(root)
    return max_diameter[0]

# Time: O(n), Space: O(h)
```

---

## MEDIUM (5 Problems)

### 6. Validate Binary Search Tree

**Problem:** Determine if a binary tree is a valid BST.

**Example:**
```
Input:     2
          / \
         1   3
Output: True

Input:     5
          / \
         1   4
            / \
           3   6
Output: False (4 is between 2 and 5 but in wrong subtree)
```

**Approach:** Use bounds — each node must be within (min, max) range.

```python
def is_valid_bst(root):
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

---

### 7. Kth Smallest Element in BST

**Problem:** Find the kth smallest element in a BST.

**Example:**
```
Input: BST with inorder [1, 2, 3, 4, 5], k = 3
Output: 3
```

**Approach:** Inorder traversal of BST is sorted. Use iterative inorder to stop at kth element.

```python
def kth_smallest(root, k):
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

# Time: O(k + h), Space: O(h)
```

---

### 8. Binary Tree Level Order Traversal

**Problem:** Return level order traversal as list of lists (BFS).

**Example:**
```
Input:     3
          / \
         9  20
            /  \
           15   7
Output: [[3], [9, 20], [15, 7]]
```

**Approach:** BFS with queue. Track level size to separate levels.

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level = []
        for _ in range(len(queue)):
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

---

### 9. Path Sum II

**Problem:** Find all root-to-leaf paths where the sum equals targetSum.

**Example:**
```
Input:     5
          / \
         4   8
        /   / \
       11  13  4
      / \       \
     7   2       1
Target: 22
Output: [[5, 4, 11, 2]]
```

**Approach:** DFS with backtracking. Track current path, add to result when leaf and sum matches.

```python
def path_sum(root, target_sum):
    result = []
    
    def dfs(node, remaining, path):
        if not node:
            return
        
        path.append(node.val)
        
        if not node.left and not node.right:
            if remaining == node.val:
                result.append(path[:])
        else:
            dfs(node.left, remaining - node.val, path)
            dfs(node.right, remaining - node.val, path)
        
        path.pop()
    
    dfs(root, target_sum, [])
    return result

# Time: O(n^2), Space: O(n)
```

---

### 10. Lowest Common Ancestor of Binary Tree

**Problem:** Find LCA of nodes p and q in a binary tree.

**Example:**
```
Input:     3
          / \
         5   1
        / \ / \
       6  2 0  8
         / \
        7   4
LCA(5, 1) = 3
LCA(5, 4) = 5
```

**Approach:** If current node is p or q, return it. If left and right both return non-null, current is LCA.

```python
def lowest_common_ancestor(root, p, q):
    if not root:
        return None
    if root == p or root == q:
        return root
    
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    
    if left and right:
        return root
    return left if left else right

# Time: O(n), Space: O(h)
```

---

## HARD (5 Problems)

### 11. Serialize and Deserialize Binary Tree

**Problem:** Design an algorithm to serialize a binary tree to a string and deserialize it back.

**Example:**
```
Input:     1
          / \
         2   3
            / \
           4   5
Serialized: "1,2,N,N,3,4,N,N,5,N,N"
```

**Approach:** Use preorder traversal with "N" markers for null nodes.

```python
class Codec:
    def serialize(self, root):
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

# Time: O(n) for both, Space: O(n)
```

---

### 12. Binary Tree Maximum Path Sum

**Problem:** Find the maximum path sum where path can start and end at any node.

**Example:**
```
Input:     -10
          /   \
         9    20
             /  \
            15   7
Output: 42 (path: 15 → 20 → 7)
```

**Approach:** At each node, compute path through it = node + max(left,0) + max(right,0). Return max downward contribution to parent.

```python
def max_path_sum(root):
    max_sum = float('-inf')
    
    def max_gain(node):
        nonlocal max_sum
        if not node:
            return 0
        
        left_gain = max(max_gain(node.left), 0)
        right_gain = max(max_gain(node.right), 0)
        
        path_through = node.val + left_gain + right_gain
        max_sum = max(max_sum, path_through)
        
        return node.val + max(left_gain, right_gain)
    
    max_gain(root)
    return max_sum

# Time: O(n), Space: O(h)
```

---

### 13. Vertical Order Traversal of Binary Tree

**Problem:** Return vertical order traversal sorted by column, then row, then value.

**Example:**
```
Input:     3
          / \
         9  20
            /  \
           15   7
Output: [[9], [3, 15], [20], [7]]
```

**Approach:** BFS with column tracking. Store (col, row, val) and sort.

```python
from collections import deque

def vertical_traversal(root):
    entries = []
    queue = deque([(root, 0, 0)])
    
    while queue:
        node, col, row = queue.popleft()
        entries.append((col, row, node.val))
        if node.left:
            queue.append((node.left, col - 1, row + 1))
        if node.right:
            queue.append((node.right, col + 1, row + 1))
    
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

### 14. Morris Traversal

**Problem:** Implement inorder traversal with O(1) space complexity.

**Example:**
```
Input:     1
          / \
         2   3
        / \
       4   5
Output: [4, 2, 5, 1, 3] using O(1) space
```

**Approach:** Threaded binary tree — create temporary links from inorder predecessor back to current node.

```python
def morris_inorder(root):
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
                predecessor.right = current
                current = current.left
            else:
                predecessor.right = None
                result.append(current.val)
                current = current.right
    
    return result

# Time: O(n), Space: O(1)
```

---

### 15. House Robber III

**Problem:** Houses arranged as a binary tree. Rob houses such that no two adjacent (connected by edge) houses are robbed. Maximize total value.

**Example:**
```
Input:     3
          / \
         2   3
          \   \
           3   1
Output: 7 (rob nodes 3 + 3 + 1 = root + left-right + right-right)
```

**Approach:** For each node, return (max_rob, max_not_rob). If rob → can't rob children. If not rob → take max from children.

```python
def rob(root):
    def dfs(node):
        if not node:
            return (0, 0)
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        rob_this = node.val + left[1] + right[1]
        not_rob_this = max(left) + max(right)
        
        return (rob_this, not_rob_this)
    
    return max(dfs(root))

# Time: O(n), Space: O(h)
```

---

## ADDITIONAL 5 MEDIUM-HARD Problems (16-20)

### 16. Path Sum III

**Problem:** Count number of paths (any start, any end downward) that sum to target.

```python
def path_sum_iii(root, target_sum):
    prefix = {0: 1}
    
    def dfs(node, curr_sum):
        if not node:
            return 0
        
        curr_sum += node.val
        count = prefix.get(curr_sum - target_sum, 0)
        
        prefix[curr_sum] = prefix.get(curr_sum, 0) + 1
        count += dfs(node.left, curr_sum)
        count += dfs(node.right, curr_sum)
        prefix[curr_sum] -= 1
        if prefix[curr_sum] == 0:
            del prefix[curr_sum]
        
        return count
    
    return dfs(root, 0)

# Time: O(n), Space: O(n)
```

---

### 17. Construct Binary Tree from Preorder and Inorder

```python
def build_tree(preorder, inorder):
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

# Time: O(n), Space: O(n)
```

---

### 18. Binary Search Tree Iterator

```python
class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)
    
    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left
    
    def next(self):
        node = self.stack.pop()
        if node.right:
            self._push_left(node.right)
        return node.val
    
    def has_next(self):
        return len(self.stack) > 0

# Time: O(1) amortized next(), O(h) space
```

---

### 19. Convert Sorted Array to BST

```python
def sorted_array_to_bst(nums):
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

# Time: O(n), Space: O(log n)
```

---

### 20. Minimum Depth of Binary Tree

```python
def min_depth(root):
    if not root:
        return 0
    if not root.left:
        return 1 + min_depth(root.right)
    if not root.right:
        return 1 + min_depth(root.left)
    return 1 + min(min_depth(root.left), min_depth(root.right))

# Time: O(n), Space: O(h)
```

---

## Complexity Summary

| # | Problem | Difficulty | Time | Space |
|---|---------|------------|------|-------|
| 1 | Maximum Depth | Easy | O(n) | O(h) |
| 2 | Same Tree | Easy | O(n) | O(h) |
| 3 | Invert Binary Tree | Easy | O(n) | O(h) |
| 4 | Subtree of Another Tree | Easy | O(mn) | O(h) |
| 5 | Diameter | Easy | O(n) | O(h) |
| 6 | Validate BST | Medium | O(n) | O(h) |
| 7 | Kth Smallest in BST | Medium | O(k+h) | O(h) |
| 8 | Level Order Traversal | Medium | O(n) | O(n) |
| 9 | Path Sum II | Medium | O(n²) | O(n) |
| 10 | LCA of Binary Tree | Medium | O(n) | O(h) |
| 11 | Serialize/Deserialize | Hard | O(n) | O(n) |
| 12 | Max Path Sum | Hard | O(n) | O(h) |
| 13 | Vertical Order | Hard | O(n log n) | O(n) |
| 14 | Morris Traversal | Hard | O(n) | O(1) |
| 15 | House Robber III | Hard | O(n) | O(h) |
| 16 | Path Sum III | Medium | O(n) | O(n) |
| 17 | Build from Pre+Inorder | Medium | O(n) | O(n) |
| 18 | BST Iterator | Medium | O(1)* | O(h) |
| 19 | Sorted Array to BST | Medium | O(n) | O(log n) |
| 20 | Minimum Depth | Easy | O(n) | O(h) |

> **h** = height (O(log n) balanced, O(n) skewed), *amortized

---

## Key Patterns to Remember

1. **DFS + return value:** Maximum depth, minimum depth, diameter, path sum
2. **DFS + global variable:** Max path sum, diameter, tree DP problems
3. **BFS + queue:** Level order, zigzag, views, vertical order
4. **Backtracking:** Path Sum II, all root-to-leaf paths
5. **BST property:** Validate BST, Kth smallest, LCA in BST
6. **Post-order DP:** House Robber III, max independent set, tree coloring
7. **Threaded tree:** Morris traversal for O(1) space
8. **Prefix sum:** Path Sum III (subarray sum technique on trees)
9. **Graph conversion:** Burning tree, distance K (convert tree to undirected graph)
10. **Construction:** Use preorder/root + inorder split, or bounds for BST
