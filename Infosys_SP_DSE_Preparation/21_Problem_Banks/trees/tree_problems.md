# 🌲 TREE PROBLEMS - COMPLETE PROBLEM BANK

## Infosys SP DSE Preparation | 35 Problems with Solutions

---

## TreeNode Class Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

---

# EASY PROBLEMS (1-10)

---

## Problem 1: Maximum Depth of Binary Tree

**Problem Statement:**
Given the root of a binary tree, return its maximum depth. A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

**Example:**
```
Input: [3,9,20,null,null,15,7]
Output: 3
```

**Approach:**
Use recursive DFS. The depth of a tree is 1 + max(depth of left subtree, depth of right subtree). Base case: if node is None, return 0.

```python
class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        left = self.maxDepth(root.left)
        right = self.maxDepth(root.right)
        return 1 + max(left, right)
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack, h = height of tree

**Trick/Tip:** This is the foundation of tree recursion. Every tree problem starts here. Remember: `1 + max(left, right)`.

---

## Problem 2: Same Tree

**Problem Statement:**
Given the roots of two binary trees p and q, write a function to check if they are the same or not. Two binary trees are considered the same if they are structurally identical and the nodes have the same values.

**Example:**
```
Input: p = [1,2,3], q = [1,2,3]
Output: True

Input: p = [1,2], q = [1,null,2]
Output: False
```

**Approach:**
Compare both trees simultaneously using DFS. Both None → True. One None → False. Values differ → False. Recurse on left and right children.

```python
class Solution:
    def isSameTree(self, p: TreeNode, q: TreeNode) -> bool:
        if not p and not q:
            return True
        if not p or not q:
            return False
        if p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** Handle three cases: both None, one None, values different. Order matters — check both None first.

---

## Problem 3: Invert/Flip Binary Tree

**Problem Statement:**
Given the root of a binary tree, invert the tree, and return its root. Inverting means swapping left and right children of every node.

**Example:**
```
Input:     4          Output:     4
           / \                   / \
          2   7                 7   2
         / \ / \               / \ / \
        1  3 6  9             9  6 3  1
```

**Approach:**
Use recursive DFS. For each node, swap left and right children. Recurse on both children. Base case: if node is None, return None.

```python
class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:
        if not root:
            return None
        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** Python's tuple swap `a, b = b, a` makes this elegant. Can also be done iteratively with a queue (BFS).

---

## Problem 4: Subtree of Another Tree

**Problem Statement:**
Given the roots of two binary trees root and subRoot, return true if there is a subtree of root with the same structure and node values as subRoot. A subtree is a tree consisting of a node in root and all of its descendants.

**Example:**
```
Input: root = [3,4,5,1,2], subRoot = [4,1,2]
Output: True
```

**Approach:**
For each node in root, check if the subtree starting at that node is identical to subRoot using the "Same Tree" check from Problem 2.

```python
class Solution:
    def isSubtree(self, root: TreeNode, subRoot: TreeNode) -> bool:
        if not root:
            return False
        if self.isSameTree(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
    
    def isSameTree(self, p: TreeNode, q: TreeNode) -> bool:
        if not p and not q:
            return True
        if not p or not q:
            return False
        if p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
```

**Complexity:**
- Time: O(m * n) - for each node in root, we check up to n nodes in subRoot
- Space: O(h) - recursion stack

**Trick/Tip:** Decompose into two problems: (1) find matching root, (2) check if trees are identical.

---

## Problem 5: Diameter of Binary Tree

**Problem Statement:**
Given the root of a binary tree, return the length of the diameter of the tree. The diameter is the length of the longest path between any two nodes. This path may or may not pass through the root.

**Example:**
```
Input: [1,2,3,4,5]
Output: 3 (path: 4 -> 2 -> 1 -> 3)
```

**Approach:**
At each node, the longest path passing through it = height of left subtree + height of right subtree. Track the maximum across all nodes. Use a global variable or pass by reference.

```python
class Solution:
    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        self.diameter = 0
        
        def height(node):
            if not node:
                return 0
            left = height(node.left)
            right = height(node.right)
            self.diameter = max(self.diameter, left + right)
            return 1 + max(left, right)
        
        height(root)
        return self.diameter
```

**Complexity:**
- Time: O(n) - single pass computing heights
- Space: O(h) - recursion stack

**Trick/Tip:** Diameter at any node = left_height + right_height. Update global max during height computation. Don't confuse diameter (edges) with depth (nodes).

---

## Problem 6: Balanced Binary Tree

**Problem Statement:**
Given a binary tree, determine if it is height-balanced. A height-balanced tree is one where the depth of the two subtrees of every node never differs by more than one.

**Example:**
```
Input: [1,2,2,3,3,null,null,4,4]
Output: False
```

**Approach:**
Use a recursive approach that returns the height, but returns -1 if the subtree is unbalanced. This avoids recalculating heights multiple times.

```python
class Solution:
    def isBalanced(self, root: TreeNode) -> bool:
        def check(node):
            if not node:
                return 0
            left = check(node.left)
            if left == -1:
                return -1
            right = check(node.right)
            if right == -1:
                return -1
            if abs(left - right) > 1:
                return -1
            return 1 + max(left, right)
        
        return check(root) != -1
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** Return -1 as a sentinel for "unbalanced". This makes the solution O(n) instead of O(n²) because we don't recalculate heights.

---

## Problem 7: Minimum Depth of Binary Tree

**Problem Statement:**
Given a binary tree, find its minimum depth. The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

**Example:**
```
Input: [3,9,20,null,null,15,7]
Output: 2
```

**Approach:**
Use BFS (level order traversal). The first leaf node we encounter gives us the minimum depth. BFS guarantees shortest path.

```python
from collections import deque

class Solution:
    def minDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        queue = deque([(root, 1)])
        while queue:
            node, depth = queue.popleft()
            if not node.left and not node.right:
                return depth
            if node.left:
                queue.append((node.left, depth + 1))
            if node.right:
                queue.append((node.right, depth + 1))
        return 0
```

**Complexity:**
- Time: O(n) - worst case visit all nodes
- Space: O(w) - w = max width of tree

**Trick/Tip:** Don't use DFS for minimum depth — it doesn't guarantee shortest path. BFS finds the nearest leaf first.

---

## Problem 8: Path Sum

**Problem Statement:**
Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.

**Example:**
```
Input: root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
Output: True (5 -> 4 -> 11 -> 2 = 22)
```

**Approach:**
Use DFS. At each node, subtract the node's value from the remaining sum. When we reach a leaf, check if the remaining sum is 0.

```python
class Solution:
    def hasPathSum(self, root: TreeNode, targetSum: int) -> bool:
        if not root:
            return False
        if not root.left and not root.right:
            return root.val == targetSum
        remaining = targetSum - root.val
        return self.hasPathSum(root.left, remaining) or self.hasPathSum(root.right, remaining)
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** Only check at leaf nodes (both children None). The path must be root-to-leaf, not root-to-any node.

---

## Problem 9: Merge Two Binary Trees

**Problem Statement:**
Given two binary trees, merge them into a new binary tree. If two nodes overlap, sum their values. Otherwise, use the non-null node.

**Example:**
```
Tree 1:     1          Tree 2:     2
           / \                   / \
          3   2                 1   3
         /                       \   \
        5                         4   7

Merged:     3
           / \
          4   5
         / \   \
        5   4   7
```

**Approach:**
Recursive DFS. If both trees have nodes, create a merged node with sum of values. Otherwise, use whichever node is non-null.

```python
class Solution:
    def mergeTrees(self, root1: TreeNode, root2: TreeNode) -> TreeNode:
        if not root1 and not root2:
            return None
        if not root1:
            return root2
        if not root2:
            return root1
        merged = TreeNode(root1.val + root2.val)
        merged.left = self.mergeTrees(root1.left, root2.left)
        merged.right = self.mergeTrees(root1.right, root2.right)
        return merged
```

**Complexity:**
- Time: O(min(m, n)) - visit nodes up to the smaller tree size
- Space: O(min(m, n)) - recursion stack

**Trick/Tip:** Handle three cases: both None, one None, both exist. The order of checks matters.

---

## Problem 10: Convert Sorted Array to Binary Search Tree

**Problem Statement:**
Given an integer array nums where the elements are sorted in ascending order, convert it to a height-balanced BST.

**Example:**
```
Input: [-10,-3,0,5,9]
Output: [0,-3,9,-10,null,5]
```

**Approach:**
Pick the middle element as root to ensure balance. Recursively build left subtree from left half and right subtree from right half.

```python
class Solution:
    def sortedArrayToBST(self, nums: list) -> TreeNode:
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

**Complexity:**
- Time: O(n) - visit each element once
- Space: O(log n) - height of balanced tree for recursion stack

**Trick/Tip:** Always pick the middle element for root. This guarantees height-balanced property. Use index-based recursion to avoid array slicing.

---

# MEDIUM PROBLEMS (11-25)

---

## Problem 11: Validate Binary Search Tree

**Problem Statement:**
Given the root of a binary tree, determine if it is a valid binary search tree (BST). A valid BST has left subtree values < node < right subtree values for every node.

**Example:**
```
Input: [2,1,3]
Output: True

Input: [5,1,4,null,null,3,6]
Output: False (4 is in the right subtree but < 5)
```

**Approach:**
Use DFS with bounds. Each node must be within a valid range. For left child, the upper bound becomes parent's value. For right child, the lower bound becomes parent's value.

```python
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        def validate(node, low=float('-inf'), high=float('inf')):
            if not node:
                return True
            if node.val <= low or node.val >= high:
                return False
            return validate(node.left, low, node.val) and validate(node.right, node.val, high)
        
        return validate(root)
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** Don't just check left.val < node < right.val. You need to propagate bounds from all ancestors. Use float('-inf') and float('inf') as initial bounds.

---

## Problem 12: Kth Smallest Element in BST

**Problem Statement:**
Given the root of a BST and an integer k, return the kth smallest value (1-indexed) of all the node values in the tree.

**Example:**
```
Input: root = [3,1,4,null,2], k = 1
Output: 1
```

**Approach:**
Use inorder traversal (left → root → right) which gives sorted order in BST. Stop at the kth element.

```python
class Solution:
    def kthSmallest(self, root: TreeNode, k: int) -> int:
        self.count = 0
        self.result = 0
        
        def inorder(node):
            if not node or self.count >= k:
                return
            inorder(node.left)
            self.count += 1
            if self.count == k:
                self.result = node.val
                return
            inorder(node.right)
        
        inorder(root)
        return self.result
```

**Complexity:**
- Time: O(k) - we stop after k elements in worst case O(n)
- Space: O(h) - recursion stack

**Trick/Tip:** Inorder traversal of BST gives sorted order. Use a counter and stop early when count == k. No need to traverse the entire tree.

---

## Problem 13: Binary Tree Level Order Traversal

**Problem Statement:**
Given the root of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).

**Example:**
```
Input: [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]
```

**Approach:**
Use BFS with a queue. Process all nodes at current level before moving to next level. Track level size to separate levels.

```python
from collections import deque

class Solution:
    def levelOrder(self, root: TreeNode) -> list:
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

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(n) - queue can hold up to n/2 nodes at last level

**Trick/Tip:** Use `for _ in range(level_size)` to process one level at a time. This is the template for all level-order variations.

---

## Problem 14: Binary Tree Right Side View

**Problem Statement:**
Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see from top to bottom.

**Example:**
```
Input: [1,2,3,null,5,null,4]
Output: [1,3,4]
```

**Approach:**
Use BFS level order traversal. For each level, the last node (rightmost) is what we see from the right side.

```python
from collections import deque

class Solution:
    def rightSideView(self, root: TreeNode) -> list:
        if not root:
            return []
        result = []
        queue = deque([root])
        while queue:
            level_size = len(queue)
            for i in range(level_size):
                node = queue.popleft()
                if i == level_size - 1:
                    result.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return result
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(n) - queue size

**Trick/Tip:** Take the last node at each level. Can also be done with DFS by visiting right subtree first and tracking depth.

---

## Problem 15: Lowest Common Ancestor of Binary Tree

**Problem Statement:**
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes p and q. The LCA is the deepest node that has both p and q as descendants.

**Example:**
```
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
Output: 3
```

**Approach:**
Use recursive DFS. If current node is None, p, or q, return it. Recurse left and right. If both return non-null, current node is LCA. If only one side returns non-null, that side contains both nodes.

```python
class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        if not root or root == p or root == q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root
        return left if left else right
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** This is one of the most important tree problems. The key insight: if p and q are in different subtrees, current node is LCA. If both are in same subtree, LCA is in that subtree.

---

## Problem 16: Lowest Common Ancestor of BST

**Problem Statement:**
Given a BST, find the lowest common ancestor of two nodes p and q. The BST property makes this simpler than the general tree version.

**Example:**
```
Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
Output: 6
```

**Approach:**
Exploit BST property: if both p and q are smaller than root, LCA is in left subtree. If both are larger, LCA is in right subtree. Otherwise, current root is LCA.

```python
class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        while root:
            if p.val < root.val and q.val < root.val:
                root = root.left
            elif p.val > root.val and q.val > root.val:
                root = root.right
            else:
                return root
```

**Complexity:**
- Time: O(h) - height of BST
- Space: O(1) - iterative, no extra space

**Trick/Tip:** Much simpler than Problem 15 because we can use BST property to eliminate half the tree at each step. Can be done iteratively.

---

## Problem 17: Serialize and Deserialize Binary Tree

**Problem Statement:**
Design an algorithm to serialize and deserialize a binary tree. Serialization is converting a tree to a string, and deserialization is reconstructing the tree from that string.

**Example:**
```
Input: [1,2,3,null,null,4,5]
Serialized: "1,2,#,#,3,4,#,#,5,#,#"
```

**Approach:**
Use preorder traversal. For serialization, write node values with a marker for null. For deserialization, read values in the same order, recreating the tree structure.

```python
class Codec:
    def serialize(self, root):
        if not root:
            return "null"
        return str(root.val) + "," + self.serialize(root.left) + "," + self.serialize(root.right)
    
    def deserialize(self, data):
        def helper(nodes):
            val = next(nodes)
            if val == "null":
                return None
            node = TreeNode(int(val))
            node.left = helper(nodes)
            node.right = helper(nodes)
            return node
        
        nodes = iter(data.split(","))
        return helper(nodes)
```

**Complexity:**
- Time: O(n) for both operations
- Space: O(n) for the string and recursion stack

**Trick/Tip:** Use `iter()` with `next()` for clean deserialization. The order of operations in serialize and deserialize must match exactly. Preorder is natural here.

---

## Problem 18: Binary Tree Maximum Path Sum

**Problem Statement:**
A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge. The path sum is the sum of node values. Find the maximum path sum. The path can start and end at any node.

**Example:**
```
Input: [1,2,3]
Output: 6 (2 -> 1 -> 3)
```

**Approach:**
At each node, calculate the max path sum that passes through it. Track the global maximum. For each node, the path sum = node.val + left_gain + right_gain. But for returning to parent, we can only take one branch.

```python
class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        self.max_sum = float('-inf')
        
        def gain(node):
            if not node:
                return 0
            left = max(gain(node.left), 0)
            right = max(gain(node.right), 0)
            self.max_sum = max(self.max_sum, node.val + left + right)
            return node.val + max(left, right)
        
        gain(root)
        return self.max_sum
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** Use `max(gain, 0)` to ignore negative paths. Update global max at each node with `node.val + left + right`, but only return `node.val + max(left, right)` to parent (can only go one way).

---

## Problem 19: Path Sum II

**Problem Statement:**
Given the root of a binary tree and an integer targetSum, return all root-to-leaf paths where the sum equals targetSum.

**Example:**
```
Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
Output: [[5,4,11,2],[5,8,4,5]]
```

**Approach:**
Use DFS with backtracking. Maintain a current path list and remaining sum. When reaching a leaf with remaining sum == 0, add the current path to result.

```python
class Solution:
    def pathSum(self, root: TreeNode, targetSum: int) -> list:
        result = []
        
        def dfs(node, remaining, path):
            if not node:
                return
            path.append(node.val)
            if not node.left and not node.right and remaining == node.val:
                result.append(list(path))
            else:
                dfs(node.left, remaining - node.val, path)
                dfs(node.right, remaining - node.val, path)
            path.pop()
        
        dfs(root, targetSum, [])
        return result
```

**Complexity:**
- Time: O(n²) - in worst case, we copy paths of length n for n leaves
- Space: O(n) - path storage and recursion stack

**Trick/Tip:** Use `path.pop()` for backtracking. Always make a copy of path with `list(path)` when adding to result. Don't modify the path after returning.

---

## Problem 20: Binary Tree Zigzag Level Order Traversal

**Problem Statement:**
Return the zigzag level order traversal of a binary tree's nodes' values (i.e., from left to right, then right to left for the next level, and so on).

**Example:**
```
Input: [3,9,20,null,null,15,7]
Output: [[3],[20,9],[15,7]]
```

**Approach:**
Use BFS level order traversal with a flag to track direction. Alternate between left-to-right and right-to-left for each level.

```python
from collections import deque

class Solution:
    def zigzagLevelOrder(self, root: TreeNode) -> list:
        if not root:
            return []
        result = []
        queue = deque([root])
        left_to_right = True
        while queue:
            level_size = len(queue)
            level = deque()
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
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(n) - queue and deque size

**Trick/Tip:** Use a deque for each level and alternate between `append` (left-to-right) and `appendleft` (right-to-left). Flip the flag after each level.

---

## Problem 21: Construct Binary Tree from Preorder and Inorder

**Problem Statement:**
Given two integer arrays preorder and inorder where preorder is the preorder traversal and inorder is the inorder traversal of a binary tree, construct and return the binary tree.

**Example:**
```
Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
Output: [3,9,20,null,null,15,7]
```

**Approach:**
First element of preorder is always the root. Find that element in inorder to split into left and right subtrees. Recurse on both halves.

```python
class Solution:
    def buildTree(self, preorder: list, inorder: list) -> TreeNode:
        if not preorder or not inorder:
            return None
        
        root = TreeNode(preorder[0])
        mid = inorder.index(preorder[0])
        root.left = self.buildTree(preorder[1:mid+1], inorder[:mid])
        root.right = self.buildTree(preorder[mid+1:], inorder[mid+1:])
        return root
```

**Complexity:**
- Time: O(n²) - worst case with index() call, can be O(n) with hashmap
- Space: O(n) - recursion stack and hashmap

**Trick/Tip:** Optimize by using a hashmap to store inorder values and their indices for O(1) lookup. Preorder gives root, inorder gives left/right subtree sizes.

---

## Problem 22: Construct Binary Tree from Inorder and Postorder

**Problem Statement:**
Given two integer arrays inorder and postorder where inorder is the inorder traversal and postorder is the postorder traversal of a binary tree, construct and return the binary tree.

**Example:**
```
Input: inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
Output: [3,9,20,null,null,15,7]
```

**Approach:**
Last element of postorder is always the root. Find that element in inorder to split into left and right subtrees. Recurse right subtree first (since postorder is left-right-root).

```python
class Solution:
    def buildTree(self, inorder: list, postorder: list) -> TreeNode:
        if not inorder or not postorder:
            return None
        
        root = TreeNode(postorder[-1])
        mid = inorder.index(postorder[-1])
        root.left = self.buildTree(inorder[:mid], postorder[:mid])
        root.right = self.buildTree(inorder[mid+1:], postorder[mid:-1])
        return root
```

**Complexity:**
- Time: O(n²) - worst case with index() call
- Space: O(n) - recursion stack

**Trick/Tip:** In postorder (left-right-root), the last element is root. The size of left subtree is determined by inorder split. Recurse right before left to match postorder order.

---

## Problem 23: Populating Next Right Pointers in Each Node

**Problem Statement:**
You are given a perfect binary tree. Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to NULL.

**Approach:**
Use BFS level order traversal. Connect each node to the next node in the queue at the same level.

```python
from collections import deque

class Solution:
    def connect(self, root: TreeNode) -> TreeNode:
        if not root:
            return None
        queue = deque([root])
        while queue:
            level_size = len(queue)
            prev = None
            for _ in range(level_size):
                node = queue.popleft()
                if prev:
                    prev.next = node
                prev = node
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return root
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(n) - queue size

**Trick/Tip:** Can also be done in O(1) space by using the already-established next pointers to traverse. Connect children using parent's next pointer chain.

---

## Problem 24: Binary Search Tree Iterator

**Problem Statement:**
Implement an iterator over a BST. The iterator initializes with the root of the BST and has next() and hasNext() methods that return the next smallest number.

**Approach:**
Flatten the BST into a sorted list using inorder traversal. Use an index to track current position.

```python
class BSTIterator:
    def __init__(self, root: TreeNode):
        self.stack = []
        self._push_left(root)
    
    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left
    
    def next(self) -> int:
        node = self.stack.pop()
        if node.right:
            self._push_left(node.right)
        return node.val
    
    def hasNext(self) -> bool:
        return len(self.stack) > 0
```

**Complexity:**
- Time: O(h) for next(), O(1) amortized
- Space: O(h) - stack size

**Trick/Tip:** Use an explicit stack instead of flattening. Push all left nodes. When popping, push all left nodes of the right child. This is the standard approach for BST iterators.

---

## Problem 25: Flatten Binary Tree to Linked List

**Problem Statement:**
Given the root of a binary tree, flatten the tree into a linked list in-place. The "linked list" should use the same TreeNode class, where the right child points to the next node and the left child is always NULL.

**Example:**
```
Input:     1         Output: 1
           / \                \
          2   5                2
         / \   \              \
        3   4   6              3
                                \
                                 4
                                  \
                                   5
                                    \
                                     6
```

**Approach:**
Use reverse preorder (right → left → root). Process nodes in reverse and link them. Or use Morris-like traversal to rewire nodes.

```python
class Solution:
    def flatten(self, root: TreeNode) -> None:
        curr = root
        while curr:
            if curr.left:
                rightmost = curr.left
                while rightmost.right:
                    rightmost = rightmost.right
                rightmost.right = curr.right
                curr.right = curr.left
                curr.left = None
            curr = curr.right
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(1) - no extra space

**Trick/Tip:** For each node with a left child, find the rightmost node in left subtree and connect it to the right child. Then move left subtree to right. This is an elegant O(1) space solution.

---

# HARD PROBLEMS (26-35)

---

## Problem 26: Binary Tree Cameras

**Problem Statement:**
You are given the root of a binary tree. We install cameras on the tree nodes. Each camera at a node can monitor its parent, itself, and its immediate children. Return the minimum number of cameras needed to monitor all nodes.

**Example:**
```
Input: [0,0,null,0,0]
Output: 1
```

**Approach:**
Use post-order traversal with states: 0 = not covered, 1 = has camera, 2 = covered (no camera). A camera is needed when a child is not covered. Place camera at uncovered node's parent.

```python
class Solution:
    def minCameraCover(self, root: TreeNode) -> int:
        self.cameras = 0
        
        def dfs(node):
            if not node:
                return 2
            left = dfs(node.left)
            right = dfs(node.right)
            if left == 0 or right == 0:
                self.cameras += 1
                return 1
            if left == 1 or right == 1:
                return 2
            return 0
        
        if dfs(root) == 0:
            self.cameras += 1
        return self.cameras
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** States: 0 = uncovered, 1 = has camera, 2 = covered. Post-order ensures children are processed before parent. Place cameras as late as possible (at parent) for optimal placement.

---

## Problem 27: House Robber III

**Problem Statement:**
The thief has found a new place to rob with a binary tree structure. Each node has a certain amount of money. If two directly-linked nodes are both robbed, the alarm goes off. Find the maximum amount the thief can rob without alerting the police.

**Example:**
```
Input: [3,2,3,null,3,null,1]
Output: 7 (rob 3 + 3 + 1 = 7)
```

**Approach:**
For each node, return a tuple: (max money if we rob this node, max money if we don't rob this node). If we rob this node, we can't rob children. If we don't, we take max from children.

```python
class Solution:
    def rob(self, root: TreeNode) -> int:
        def dfs(node):
            if not node:
                return (0, 0)
            left = dfs(node.left)
            right = dfs(node.right)
            rob_this = node.val + left[1] + right[1]
            skip_this = max(left) + max(right)
            return (rob_this, skip_this)
        
        return max(dfs(root))
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** Tree DP with two states per node: rob or skip. Return both values and let parent decide. This pattern works for many tree optimization problems.

---

## Problem 28: Vertical Order Traversal of Binary Tree

**Problem Statement:**
Given the root of a binary tree, calculate the vertical order traversal. For each vertical column, nodes should be listed from top to bottom, and within the same row and column, nodes should be sorted by value.

**Example:**
```
Input: [3,9,20,null,null,15,7]
Output: [[9],[3,15],[20],[7]]
```

**Approach:**
Use BFS or DFS to track column, row, and value for each node. Group by column, then sort by row and value within each column.

```python
from collections import defaultdict, deque

class Solution:
    def verticalTraversal(self, root: TreeNode) -> list:
        nodes = []
        queue = deque([(root, 0, 0)])
        while queue:
            node, row, col = queue.popleft()
            if node:
                nodes.append((col, row, node.val))
                queue.append((node.left, row + 1, col - 1))
                queue.append((node.right, row + 1, col + 1))
        
        nodes.sort()
        result = []
        prev_col = None
        for col, row, val in nodes:
            if col != prev_col:
                result.append([])
                prev_col = col
            result[-1].append(val)
        return result
```

**Complexity:**
- Time: O(n log n) - sorting nodes
- Space: O(n) - storing all nodes

**Trick/Tip:** Use tuple (col, row, val) for sorting. Python's tuple comparison sorts by first element, then second, etc. This automatically handles the required ordering.

---

## Problem 29: Morris Traversal (Inorder, O(1) Space)

**Problem Statement:**
Implement inorder traversal of a binary tree using O(1) extra space (no recursion, no stack). This is called Morris Traversal.

**Approach:**
Use threaded binary tree concept. For each node, find its inorder predecessor and create a temporary link from predecessor to current node. This allows us to return to the parent without a stack.

```python
class Solution:
    def morrisInorder(self, root: TreeNode) -> list:
        result = []
        curr = root
        while curr:
            if not curr.left:
                result.append(curr.val)
                curr = curr.right
            else:
                predecessor = curr.left
                while predecessor.right and predecessor.right != curr:
                    predecessor = predecessor.right
                if not predecessor.right:
                    predecessor.right = curr
                    curr = curr.left
                else:
                    predecessor.right = None
                    result.append(curr.val)
                    curr = curr.right
        return result
```

**Complexity:**
- Time: O(n) - each node visited at most twice
- Space: O(1) - no extra space

**Trick/Tip:** When moving to left subtree, create a thread from inorder predecessor back to current node. When we return via the thread, we know we've visited the left subtree and can process current node. Remove thread after use.

---

## Problem 30: Count Nodes Equal to Average of Subtree

**Problem Statement:**
Given the root of a binary tree, return the number of nodes where the value of the node equals the average of the values in its subtree. The average is the sum divided by count, rounded down.

**Example:**
```
Input: [4,8,5,0,1,null,6]
Output: 5
```

**Approach:**
Use post-order traversal. At each node, calculate sum and count of its subtree. Compare node's value with average. Return (sum, count) to parent.

```python
class Solution:
    def averageOfSubtree(self, root: TreeNode) -> int:
        self.count = 0
        
        def dfs(node):
            if not node:
                return (0, 0)
            left_sum, left_count = dfs(node.left)
            right_sum, right_count = dfs(node.right)
            total_sum = left_sum + right_sum + node.val
            total_count = left_count + right_count + 1
            if node.val == total_sum // total_count:
                self.count += 1
            return (total_sum, total_count)
        
        dfs(root)
        return self.count
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** Return both sum and count from each subtree to avoid recalculation. Post-order ensures children are processed before parent.

---

## Problem 31: Maximum Width of Binary Tree

**Problem Statement:**
Given the root of a binary tree, return the maximum width of the tree. Width is the number of nodes between the leftmost and rightmost non-null nodes (including null nodes in between) at the same level.

**Example:**
```
Input: [1,3,2,5,3,null,9]
Output: 4 (level 2 has nodes at positions 1,2,3,4)
```

**Approach:**
Use BFS with position numbering. Root is at position 0. Left child at 2*pos, right child at 2*pos+1. Width at each level = max_pos - min_pos + 1.

```python
from collections import deque

class Solution:
    def widthOfBinaryTree(self, root: TreeNode) -> int:
        if not root:
            return 0
        max_width = 0
        queue = deque([(root, 0)])
        while queue:
            level_size = len(queue)
            min_pos = queue[0][1]
            max_pos = queue[-1][1]
            max_width = max(max_width, max_pos - min_pos + 1)
            for _ in range(level_size):
                node, pos = queue.popleft()
                if node.left:
                    queue.append((node.left, 2 * pos))
                if node.right:
                    queue.append((node.right, 2 * pos + 1))
        return max_width
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(n) - queue size

**Trick/Tip:** Normalize positions at each level by subtracting the minimum position to avoid overflow. This handles skewed trees where positions can become very large.

---

## Problem 32: All Nodes Distance K in Binary Tree

**Problem Statement:**
Given the root of a binary tree, a target node, and an integer k, return a list of all nodes that are exactly k distance from the target node.

**Example:**
```
Input: root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2
Output: [7,4,1]
```

**Approach:**
First, build a parent map using BFS/DFS. Then from target, do BFS in all directions (left, right, parent) for k steps. Use a visited set to avoid revisiting nodes.

```python
from collections import deque

class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> list:
        parent = {}
        
        def build_parent(node, par=None):
            if node:
                parent[node] = par
                build_parent(node.left, node)
                build_parent(node.right, node)
        
        build_parent(root)
        
        queue = deque([(target, 0)])
        visited = {target}
        result = []
        
        while queue:
            node, dist = queue.popleft()
            if dist == k:
                result.append(node.val)
            elif dist < k:
                for neighbor in [node.left, node.right, parent[node]]:
                    if neighbor and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, dist + 1))
        
        return result
```

**Complexity:**
- Time: O(n) - build parent map and BFS
- Space: O(n) - parent map, queue, visited set

**Trick/Tip:** Convert tree to graph by adding parent pointers. Then use BFS from target. This technique works for many "distance in tree" problems.

---

## Problem 33: Burn the Tree

**Problem Statement:**
Given a binary tree and a target node, find the minimum time required to burn the entire tree. Burning starts from the target node and spreads to adjacent nodes (parent, left, right) each second.

**Example:**
```
Input:     1
          / \
         2   3
        /   / \
       4   5   6
      /
     7
Target: 4, Output: 5 seconds
```

**Approach:**
Build parent map and convert tree to graph. BFS from target, tracking time. The last node reached gives the minimum burn time.

```python
from collections import deque

class Solution:
    def burnTree(self, root: TreeNode, target: TreeNode) -> int:
        parent = {}
        
        def build_parent(node, par=None):
            if node:
                parent[node] = par
                build_parent(node.left, node)
                build_parent(node.right, node)
        
        build_parent(root)
        
        queue = deque([(target, 0)])
        visited = {target}
        max_time = 0
        
        while queue:
            node, time = queue.popleft()
            max_time = max(max_time, time)
            for neighbor in [node.left, node.right, parent[node]]:
                if neighbor and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, time + 1))
        
        return max_time
```

**Complexity:**
- Time: O(n) - build parent map and BFS
- Space: O(n) - parent map, queue, visited set

**Trick/Tip:** Same as Problem 32 but we take max time instead of collecting nodes at distance k. Tree-to-graph conversion is key.

---

## Problem 34: Find Duplicate Subtrees

**Problem Statement:**
Given the root of a binary tree, return all duplicate subtrees. Two trees are duplicate if they have the same structure and node values. Return the root node of each duplicate subtree.

**Example:**
```
Input: [1,2,3,4,null,2,4,null,null,4]
Output: [[2,4],[4]]
```

**Approach:**
Serialize each subtree. Use a hashmap to count occurrences. If a serialization appears more than once, it's a duplicate.

```python
from collections import defaultdict

class Solution:
    def findDuplicateSubtrees(self, root: TreeNode) -> list:
        serial_count = defaultdict(int)
        result = []
        
        def serialize(node):
            if not node:
                return "#"
            serial = str(node.val) + "," + serialize(node.left) + "," + serialize(node.right)
            serial_count[serial] += 1
            if serial_count[serial] == 2:
                result.append(node)
            return serial
        
        serialize(root)
        return result
```

**Complexity:**
- Time: O(n²) - serialization takes O(n) per node
- Space: O(n²) - storing serializations

**Trick/Tip:** Serialization is the key to comparing subtrees. Use a delimiter (comma) to avoid ambiguity. Only add to result when count == 2 to avoid duplicates in result.

---

## Problem 35: Sum of Distances in Tree

**Problem Statement:**
Given an undirected tree with n nodes (0 to n-1) and n-1 edges, return an array answer where answer[i] is the sum of distances between node i and all other nodes.

**Example:**
```
Input: n = 6, edges = [[0,1],[0,2],[2,3],[2,4],[2,5]]
Output: [8,6,4,5,5,5]
```

**Approach:**
Use two-pass DFS. First, compute answer[0] (root) and count of nodes in each subtree. Then, reroot the tree: when moving root from parent to child, answer[child] = answer[parent] - count[child] + (n - count[child]).

```python
from collections import defaultdict

class Solution:
    def sumOfDistancesInTree(self, n: int, edges: list) -> list:
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        
        count = [1] * n
        answer = [0] * n
        
        def dfs1(node, parent):
            for neighbor in graph[node]:
                if neighbor != parent:
                    dfs1(neighbor, node)
                    count[node] += count[neighbor]
                    answer[node] += answer[neighbor] + count[neighbor]
        
        def dfs2(node, parent):
            for neighbor in graph[node]:
                if neighbor != parent:
                    answer[neighbor] = answer[node] - count[neighbor] + (n - count[neighbor])
                    dfs2(neighbor, node)
        
        dfs1(0, -1)
        dfs2(0, -1)
        return answer
```

**Complexity:**
- Time: O(n) - two passes of DFS
- Space: O(n) - count and answer arrays

**Trick/Tip:** The rerooting formula is key: when moving root from parent to child, distances to nodes in child's subtree decrease by 1, distances to all other nodes increase by 1. This gives: answer[child] = answer[parent] - count[child] + (n - count[child]).

---

# 📚 QUICK REFERENCE

## Common Patterns

| Pattern | Problems |
|---------|----------|
| DFS Recursion | 1, 2, 3, 4, 5, 6, 8, 9, 11, 15, 18, 19, 25, 26, 27, 30 |
| BFS Level Order | 7, 13, 14, 20, 23, 28, 31, 32, 33 |
| BST Properties | 12, 16, 24 |
| Tree Serialization | 17, 34 |
| Tree-to-Graph | 32, 33, 35 |
| Post-order Traversal | 22, 26, 27, 30 |
| Pre-order Traversal | 21, 25 |
| Inorder Traversal | 12, 24, 29 |

## Complexity Summary

| Complexity | Problems |
|------------|----------|
| O(n) Time | 1-10, 11, 13-16, 18, 20-23, 26-30, 32, 33, 35 |
| O(n log n) Time | 28 |
| O(n²) Time | 4, 21, 22, 34 |
| O(1) Space | 16, 25, 29 |
| O(n) Space | 13, 14, 20, 23, 28, 31 |

## Key Insights

1. **Tree Recursion**: Most tree problems can be solved with simple recursion. Master the pattern first.
2. **BFS vs DFS**: Use BFS for level-by-level problems, DFS for path/subtree problems.
3. **Global Variables**: Use self.var or nonlocal to track results across recursive calls.
4. **Backtracking**: Use path.pop() after recursive call to restore state.
5. **Threaded Trees**: Morris traversal shows how to traverse without stack by creating temporary links.

---

*Total Problems: 35 | Easy: 10 | Medium: 15 | Hard: 10*
