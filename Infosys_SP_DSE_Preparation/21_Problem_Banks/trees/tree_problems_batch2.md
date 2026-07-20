# Tree Problems Batch 2 - Infosys SP DSE Preparation

> **40 More Tree Problems** | Complete Python Solutions | Easy -> Hard
> Companion to `tree_problems_batch1.md`

---

## TreeNode Class Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Node:
    """N-ary Tree Node"""
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children else []
```

---

---

# EASY PROBLEMS (1-12)

---

## Problem 1: Sum of Left Leaves

**Statement:** Given a binary tree, return the sum of all left leaves. A left leaf is a leaf node that is the left child of its parent.

**Approach:** Traverse the tree. When at a node, check if its left child exists and is a leaf (no left or right children). If so, add its value. Recurse on left and right children.

```python
def sumOfLeftLeaves(root):
    if not root:
        return 0
    total = 0
    if root.left:
        if not root.left.left and not root.left.right:
            total += root.left.val
        else:
            total += sumOfLeftLeaves(root.left)
    total += sumOfLeftLeaves(root.right)
    return total
```

**Time Complexity:** O(n) - visit every node once
**Space Complexity:** O(h) - recursion stack, h = height of tree

---

## Problem 2: Two Sum IV - BST

**Statement:** Given the root of a BST and an integer k, return true if there exist two nodes such that their values sum to k.

**Approach:** Use a set to store seen values. Traverse the BST. For each node, check if (k - node.val) exists in the set. If yes, return True. Otherwise, add the node's value to the set.

```python
def findTarget(root, k):
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
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(n) - set stores up to n values

---

## Problem 3: Find Mode in BST

**Statement:** Given a BST with duplicates, return all modes (most frequently occurring values) in any order.

**Approach:** Inorder traversal of BST gives sorted order, so duplicates are adjacent. Track current value, current count, and max count. Reset count when value changes. Collect results when count equals max count.

```python
def findMode(root):
    result = []
    prev_val = None
    curr_count = 0
    max_count = 0

    def inorder(node):
        nonlocal prev_val, curr_count, max_count
        if not node:
            return
        inorder(node.left)
        if node.val == prev_val:
            curr_count += 1
        else:
            curr_count = 1
            prev_val = node.val
        if curr_count > max_count:
            max_count = curr_count
            result.clear()
            result.append(node.val)
        elif curr_count == max_count:
            result.append(node.val)
        inorder(node.right)

    inorder(root)
    return result
```

**Time Complexity:** O(n) - inorder traversal visits all nodes
**Space Complexity:** O(h) - recursion stack

---

## Problem 4: Increasing BST

**Statement:** Given a BST, rearrange it in-place so that the leftmost node becomes the root, each node has no left child, and each node has only one right child (increasing order).

**Approach:** Perform inorder traversal. For each node, disconnect its left child and attach it as the right child of the previous node in the inorder sequence. Use a dummy node to simplify linking.

```python
def increasingBST(root):
    dummy = TreeNode(0)
    curr = dummy

    def inorder(node):
        nonlocal curr
        if not node:
            return
        inorder(node.left)
        node.left = None
        curr.right = node
        curr = node
        inorder(node.right)

    inorder(root)
    return dummy.right
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 5: Range Sum of BST

**Statement:** Given a BST root and two integers low and high, return the sum of all node values in the range [low, high].

**Approach:** DFS on the BST. If node.val < low, only go right (all left values are smaller). If node.val > high, only go left (all right values are larger). If within range, add the value and recurse both ways.

```python
def rangeSumBST(root, low, high):
    if not root:
        return 0
    if root.val < low:
        return rangeSumBST(root.right, low, high)
    if root.val > high:
        return rangeSumBST(root.left, low, high)
    return (root.val +
            rangeSumBST(root.left, low, high) +
            rangeSumBST(root.right, low, high))
```

**Time Complexity:** O(n) - worst case visit all nodes
**Space Complexity:** O(h) - recursion stack

---

## Problem 6: Minimum Absolute Difference in BST

**Statement:** Given a BST, return the minimum absolute difference between values of any two different nodes.

**Approach:** Inorder traversal gives sorted order. The minimum absolute difference must be between adjacent nodes in sorted order. Track previous value during inorder traversal and compute the difference.

```python
def getMinimumDifference(root):
    min_diff = float('inf')
    prev = None

    def inorder(node):
        nonlocal min_diff, prev
        if not node:
            return
        inorder(node.left)
        if prev is not None:
            min_diff = min(min_diff, node.val - prev)
        prev = node.val
        inorder(node.right)

    inorder(root)
    return min_diff
```

**Time Complexity:** O(n) - inorder traversal
**Space Complexity:** O(h) - recursion stack

---

## Problem 7: Check if Tree is Symmetric

**Statement:** Given a binary tree, check whether it is a mirror of itself (symmetric around its center).

**Approach:** Use a helper function that checks if two trees are mirrors of each other. Two trees are mirrors if: both roots have the same value, the left subtree of one mirrors the right subtree of the other, and vice versa.

```python
def isSymmetric(root):
    if not root:
        return True

    def isMirror(left, right):
        if not left and not right:
            return True
        if not left or not right:
            return False
        return (left.val == right.val and
                isMirror(left.left, right.right) and
                isMirror(left.right, right.left))

    return isMirror(root.left, root.right)
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack (worst O(n/2) for skewed tree)

---

## Problem 8: Univalued Binary Tree

**Statement:** A binary tree is univalued if every node has the same value. Given the root of a binary tree, return true if it is univalued.

**Approach:** Store the root's value. Traverse the entire tree. If any node has a different value, return False. If traversal completes without mismatch, return True.

```python
def isUnivalTree(root):
    if not root:
        return True
    val = root.val

    def dfs(node):
        if not node:
            return True
        if node.val != val:
            return False
        return dfs(node.left) and dfs(node.right)

    return dfs(root)
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(h) - recursion stack

---

## Problem 9: Count Good Nodes in Binary Tree

**Statement:** A node is "good" if in the path from root to that node, there are no nodes with a value greater than it. Return the number of good nodes.

**Approach:** DFS, passing down the maximum value seen so far on the path. If current node's value >= max so far, it is a good node (increment count). Update max and recurse on children.

```python
def goodNodes(root):
    count = [0]

    def dfs(node, max_so_far):
        if not node:
            return
        if node.val >= max_so_far:
            count[0] += 1
        new_max = max(max_so_far, node.val)
        dfs(node.left, new_max)
        dfs(node.right, new_max)

    dfs(root, float('-inf'))
    return count[0]
```

**Time Complexity:** O(n) - visit every node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 10: Leaf-Similar Trees

**Statement:** Two binary trees are leaf-similar if their leaf sequences (left to right) are the same. Return True if two trees are leaf-similar.

**Approach:** For each tree, collect all leaf values in order via DFS. Compare the two resulting lists for equality.

```python
def leafSimilar(root1, root2):
    def get_leaves(node, leaves):
        if not node:
            return
        if not node.left and not node.right:
            leaves.append(node.val)
        get_leaves(node.left, leaves)
        get_leaves(node.right, leaves)

    leaves1, leaves2 = [], []
    get_leaves(root1, leaves1)
    get_leaves(root2, leaves2)
    return leaves1 == leaves2
```

**Time Complexity:** O(n1 + n2) - traverse both trees
**Space Complexity:** O(n1 + n2) - storing leaf sequences

---

## Problem 11: Maximum Depth of N-ary Tree

**Statement:** Given an N-ary tree, find its maximum depth. The depth is the number of nodes along the longest path from the root to the farthest leaf.

**Approach:** DFS: if node is None, return 0. Otherwise, return 1 + max(depth of each child). Handle the base case where children list is empty.

```python
def maxDepth(root):
    if not root:
        return 0
    if not root.children:
        return 1
    return 1 + max(maxDepth(child) for child in root.children)
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(m) where m is max width - worst O(n) for degenerate tree

---

## Problem 12: N-ary Tree Level Order Traversal

**Statement:** Given an N-ary tree, return the level order traversal of its nodes' values (left to right, level by level).

**Approach:** BFS using a queue. Start with root. For each level, record the size of the queue, dequeue that many nodes, record their values, and enqueue all their children.

```python
from collections import deque

def levelOrder(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            for child in node.children:
                queue.append(child)
        result.append(level)
    return result
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(n) - queue can hold up to n/2 nodes at widest level

---

---

# MEDIUM PROBLEMS (13-30)

---

## Problem 13: Binary Tree Level Order Traversal II

**Statement:** Given a binary tree, return the bottom-up level order traversal (first the deepest level, then the level above, up to the root).

**Approach:** Perform standard BFS level order traversal. After collecting all levels in top-down order, reverse the result list to get bottom-up order.

```python
from collections import deque

def levelOrderBottom(root):
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
    return result[::-1]
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(n) - storing all levels

---

## Problem 14: Binary Tree Tilt

**Statement:** The tilt of a node is the absolute difference between the sum of all left subtree values and right subtree values. The tilt of the whole tree is the sum of all node tilts.

**Approach:** Post-order DFS. For each node, compute its subtree sum (left_sum + right_sum + node.val). The tilt contribution is abs(left_sum - right_sum). Accumulate total tilt globally. Return the subtree sum for parent computation.

```python
def findTilt(root):
    total_tilt = [0]

    def subtree_sum(node):
        if not node:
            return 0
        left = subtree_sum(node.left)
        right = subtree_sum(node.right)
        total_tilt[0] += abs(left - right)
        return left + right + node.val

    subtree_sum(root)
    return total_tilt[0]
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 15: Find Bottom Left Tree Value

**Statement:** Given a binary tree, find the leftmost value in the last row of the tree.

**Approach:** BFS level order traversal. The first node visited at each level is the leftmost. Track the first node's value at each level; by the end, the answer is the first node of the last level.

```python
from collections import deque

def findBottomLeftValue(root):
    queue = deque([root])
    result = root.val
    while queue:
        for i in range(len(queue)):
            node = queue.popleft()
            if i == 0:
                result = node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return result
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(w) - max width of tree

---

## Problem 16: Largest Value in Each Tree Row

**Statement:** Given a binary tree, return a list of the largest value in each row (level).

**Approach:** BFS level order traversal. For each level, track the maximum value. Append that maximum to the result after processing all nodes in the level.

```python
from collections import deque

def largestValues(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_max = float('-inf')
        for _ in range(len(queue)):
            node = queue.popleft()
            level_max = max(level_max, node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level_max)
    return result
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(w) - max width of tree

---

## Problem 17: Closest Value in BST

**Statement:** Given a BST and a target value, find the value in the BST that is closest to the target.

**Approach:** Start from root. At each node, update the closest value if the current node is closer. If target < node.val, go left; if target > node.val, go right; if equal, return immediately.

```python
def closestValue(root, target):
    closest = root.val
    while root:
        if abs(root.val - target) < abs(closest - target):
            closest = root.val
        if target < root.val:
            root = root.left
        elif target > root.val:
            root = root.right
        else:
            return root.val
    return closest
```

**Time Complexity:** O(h) - height of BST, worst O(n)
**Space Complexity:** O(1) - iterative approach

---

## Problem 18: Inorder Successor in BST

**Statement:** Given a BST node p, find the in-order successor (the node with the smallest key greater than p.val). Return None if it does not exist.

**Approach:** Starting from root, track potential successor. If node.val > p.val, it could be the successor -- record it and go left. If node.val <= p.val, go right. By the end, the last recorded value is the successor.

```python
def inorderSuccessor(root, p):
    successor = None
    while root:
        if root.val > p.val:
            successor = root
            root = root.left
        else:
            root = root.right
    return successor
```

**Time Complexity:** O(h) - height of BST
**Space Complexity:** O(1) - iterative

---

## Problem 19: Delete Node in BST

**Statement:** Given a BST root and a key, delete the node with the given key and return the root of the updated BST.

**Approach:** Find the node to delete. Three cases: (1) No left child -- replace with right subtree. (2) No right child -- replace with left subtree. (3) Both children exist -- find the inorder successor (smallest in right subtree), copy its value, then delete that successor from the right subtree.

```python
def deleteNode(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = deleteNode(root.left, key)
    elif key > root.val:
        root.right = deleteNode(root.right, key)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        successor = root.right
        while successor.left:
            successor = successor.left
        root.val = successor.val
        root.right = deleteNode(root.right, successor.val)
    return root
```

**Time Complexity:** O(h) - find and delete in BST
**Space Complexity:** O(h) - recursion stack

---

## Problem 20: Construct BST from Preorder Traversal

**Statement:** Given an array of unique values representing the preorder traversal of a BST, construct the tree and return its root.

**Approach:** Use a recursive helper with bounds. The first element is the root. All values less than root go to the left subtree, rest to the right. Use an index pointer that advances as nodes are consumed.

```python
def bstFromPreorder(preorder):
    idx = [0]

    def build(lower, upper):
        if idx[0] >= len(preorder):
            return None
        val = preorder[idx[0]]
        if val < lower or val > upper:
            return None
        node = TreeNode(val)
        idx[0] += 1
        node.left = build(lower, val)
        node.right = build(val, upper)
        return node

    return build(float('-inf'), float('inf'))
```

**Time Complexity:** O(n) - each node visited once
**Space Complexity:** O(h) - recursion stack

---

## Problem 21: Convert BST to Greater Tree

**Statement:** Given a BST, transform it into a Greater Tree where every node's value is replaced by the original value plus the sum of all values greater than it in the BST.

**Approach:** Reverse inorder traversal (right -> node -> left). Maintain a running sum. At each node, update its value to be the running sum, then update the running sum to include the current node's original value.

```python
def convertBST(root):
    running_sum = [0]

    def reverse_inorder(node):
        if not node:
            return
        reverse_inorder(node.right)
        running_sum[0] += node.val
        node.val = running_sum[0]
        reverse_inorder(node.left)

    reverse_inorder(root)
    return root
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 22: Diameter of N-ary Tree

**Statement:** Given an N-ary tree, find the diameter -- the longest path between any two nodes (measured in edges).

**Approach:** For each node, find the two longest paths going down through different children. Diameter = max(diameter, longest + second_longest). Return the max diameter seen.

```python
def diameter(root):
    max_diam = [0]

    def height(node):
        if not node:
            return 0
        first, second = 0, 0
        for child in node.children:
            h = height(child)
            if h > first:
                second = first
                first = h
            elif h > second:
                second = h
        max_diam[0] = max(max_diam[0], first + second)
        return 1 + first

    height(root)
    return max_diam[0]
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 23: Step-By-Step Directions from One Node to Another

**Statement:** Given a binary tree with two node values (start and dest), return a string of directions ('L', 'R', 'U') to go from start to destination. Minimize the length.

**Approach:** Find the lowest common ancestor (LCA) of the two nodes. From LCA to destination: record path using 'L'/'R'. From LCA to start: record path using 'L'/'R', then reverse and convert to 'U'. Concatenate the 'U' path with the destination path.

```python
def getDirections(root, startValue, destValue):
    def find_path(node, target, path):
        if not node:
            return False
        if node.val == target:
            return True
        path.append('L')
        if find_path(node.left, target, path):
            return True
        path.pop()
        path.append('R')
        if find_path(node.right, target, path):
            return True
        path.pop()
        return False

    def lca(node, v1, v2):
        if not node or node.val == v1 or node.val == v2:
            return node
        left = lca(node.left, v1, v2)
        right = lca(node.right, v1, v2)
        if left and right:
            return node
        return left if left else right

    ancestor = lca(root, startValue, destValue)
    path_to_start = []
    find_path(ancestor, startValue, path_to_start)
    path_to_dest = []
    find_path(ancestor, destValue, path_to_dest)
    return 'U' * len(path_to_start) + ''.join(path_to_dest)
```

**Time Complexity:** O(n) - finding LCA and paths
**Space Complexity:** O(h) - recursion stack

---

## Problem 24: Binary Tree Right Side View

**Statement:** Given a binary tree, return the values of nodes you can see from the right side (last node at each level).

**Approach:** BFS level order traversal. For each level, the last node processed is the rightmost. Record the last node at each level.

```python
from collections import deque

def rightSideView(root):
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

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(w) - max width of tree

---

## Problem 25: Even Odd Tree

**Statement:** A binary tree is Even-Odd if: at every even-indexed level (0, 2, 4, ...), all values are odd and strictly increasing; at every odd-indexed level (1, 3, 5, ...), all values are even and strictly decreasing.

**Approach:** BFS level order. Track the level. For each level, check parity constraints and order constraints. If any violation is found, return False.

```python
from collections import deque

def isEvenOddTree(root):
    queue = deque([root])
    level = 0
    while queue:
        prev = None
        for _ in range(len(queue)):
            node = queue.popleft()
            if level % 2 == 0:
                if node.val % 2 == 0:
                    return False
                if prev is not None and node.val <= prev:
                    return False
            else:
                if node.val % 2 == 1:
                    return False
                if prev is not None and node.val >= prev:
                    return False
            prev = node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        level += 1
    return True
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(w) - max width of tree

---

## Problem 26: Maximum Level Sum of Binary Tree

**Statement:** Given a binary tree, return the level (1-indexed) with the maximum sum of node values. If there is a tie, return the smallest level number.

**Approach:** BFS level order traversal. Sum values at each level. Track the maximum sum and the level at which it occurs. Return the level number (1-indexed).

```python
from collections import deque

def maxLevelSum(root):
    max_sum = float('-inf')
    result_level = 0
    level = 1
    queue = deque([root])
    while queue:
        level_sum = 0
        for _ in range(len(queue)):
            node = queue.popleft()
            level_sum += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        if level_sum > max_sum:
            max_sum = level_sum
            result_level = level
        level += 1
    return result_level
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(w) - max width of tree

---

## Problem 27: Deepest Leaves Sum

**Statement:** Given a binary tree, return the sum of the values of its deepest leaves (the leaves at the deepest level).

**Approach:** BFS level order traversal. The last level processed contains the deepest leaves. Sum all values at that level.

```python
from collections import deque

def deepestLeavesSum(root):
    queue = deque([root])
    while queue:
        level_sum = 0
        for _ in range(len(queue)):
            node = queue.popleft()
            level_sum += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return level_sum
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(w) - max width of tree

---

## Problem 28: Check Completeness of a Binary Tree

**Statement:** Given a binary tree, check if it is a complete binary tree. A complete tree has all levels fully filled except possibly the last, which is filled left to right.

**Approach:** BFS traversal. Once a null node is encountered, no more non-null nodes should appear after it. Use a flag to track if we have seen a null. If a non-null node appears after a null, the tree is not complete.

```python
from collections import deque

def isCompleteTree(root):
    if not root:
        return True
    queue = deque([root])
    seen_null = False
    while queue:
        node = queue.popleft()
        if not node:
            seen_null = True
        else:
            if seen_null:
                return False
            queue.append(node.left)
            queue.append(node.right)
    return True
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(w) - max width of tree

---

## Problem 29: Trim a Binary Search Tree

**Statement:** Given a BST root and two values low and high, trim the tree so all values fall within [low, high]. The relative structure of remaining nodes should be preserved.

**Approach:** Recursive: if node.val < low, the entire left subtree is out of range -- return trimmed right subtree. If node.val > high, return trimmed left subtree. Otherwise, recurse on both children and return the node.

```python
def trimBST(root, low, high):
    if not root:
        return None
    if root.val < low:
        return trimBST(root.right, low, high)
    if root.val > high:
        return trimBST(root.left, low, high)
    root.left = trimBST(root.left, low, high)
    root.right = trimBST(root.right, low, high)
    return root
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 30: Flatten Binary Tree to Linked List

**Statement:** Given a binary tree, flatten it to a linked list in-place. The "linked list" should use the right child pointers, and the left child pointers should be null. The order should be pre-order traversal.

**Approach:** Recursive approach: recursively flatten left and right subtrees. Save the right subtree, attach the flattened left subtree to the current node's right, then find the tail of the flattened left subtree and attach the saved right subtree to it.

```python
def flatten(root):
    def helper(node):
        if not node:
            return None
        left_tail = helper(node.left)
        right_tail = helper(node.right)
        if left_tail:
            left_tail.right = node.right
            node.right = node.left
            node.left = None
        return right_tail if right_tail else (left_tail if left_tail else node)

    helper(root)
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

---

# HARD PROBLEMS (31-40)

---

## Problem 31: Binary Tree Cameras

**Statement:** You are given the root of a binary tree. We install cameras on tree nodes. Each camera at a node can monitor its parent, itself, and its immediate children. Return the minimum number of cameras needed to monitor all nodes.

**Approach:** Post-order DFS with states: 0 = not covered, 1 = has camera, 2 = covered (no camera). If a child is not covered, place a camera at current node (state 1, count++). If a child has a camera, current node is covered (state 2). If both children are covered and no camera needed, return state 0 (not covered) so parent places camera. After DFS, if root state is 0, add one more camera.

```python
def minCameraCover(root):
    count = [0]

    def dfs(node):
        if not node:
            return 2  # null nodes are considered covered
        left = dfs(node.left)
        right = dfs(node.right)
        if left == 0 or right == 0:
            # child not covered -> place camera here
            count[0] += 1
            return 1  # has camera
        if left == 1 or right == 1:
            # child has camera -> this node is covered
            return 2
        # both children covered, no camera needed
        return 0

    if dfs(root) == 0:
        count[0] += 1
    return count[0]
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 32: Find Duplicate Subtrees

**Statement:** Given a binary tree, find all duplicate subtrees. Return the root nodes of each duplicate subtree. Two trees are duplicates if they have the same structure and node values.

**Approach:** Serialize each subtree as a string. Use a dictionary to count occurrences. When a serialization appears for the second time, add the node to the result.

```python
def findDuplicateSubtrees(root):
    from collections import defaultdict
    serial_count = defaultdict(int)
    result = []

    def serialize(node):
        if not node:
            return "#"
        serial = f"{node.val},{serialize(node.left)},{serialize(node.right)}"
        serial_count[serial] += 1
        if serial_count[serial] == 2:
            result.append(node)
        return serial

    serialize(root)
    return result
```

**Time Complexity:** O(n^2) in worst case due to string operations; O(n) average
**Space Complexity:** O(n) - storing serializations

---

## Problem 33: Serialize and Deserialize N-ary Tree

**Statement:** Design an algorithm to serialize and deserialize an N-ary tree to/from a string.

**Approach:** Serialize: DFS preorder. For each node, write its value followed by the count of children, then recurse on each child. Deserialize: Read value, read child count, recursively deserialize children, return the node.

```python
class Codec:
    def serialize(self, root):
        if not root:
            return ""
        result = []

        def dfs(node):
            result.append(str(node.val))
            result.append(str(len(node.children)))
            for child in node.children:
                dfs(child)

        dfs(root)
        return ','.join(result)

    def deserialize(self, data):
        if not data:
            return None
        tokens = data.split(',')
        idx = [0]

        def dfs():
            val = int(tokens[idx[0]])
            idx[0] += 1
            num_children = int(tokens[idx[0]])
            idx[0] += 1
            node = Node(val)
            for _ in range(num_children):
                node.children.append(dfs())
            return node

        return dfs()
```

**Time Complexity:** O(n) - serialize and deserialize each visit node once
**Space Complexity:** O(n) - storing the serialized string and recursion stack

---

## Problem 34: Critical Connections in a Network

**Statement:** There are n servers connected by undirected edges. A critical connection is an edge that, if removed, makes some servers unreachable from others. Find all critical connections (Tarjan's bridge-finding algorithm).

**Approach:** Use DFS with discovery time and low values. For each edge (u, v), if low[v] > disc[u], then the edge is a bridge (critical connection). The low value of a node is the minimum discovery time reachable from its subtree.

```python
def criticalConnections(n, connections):
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)

    disc = [-1] * n
    low = [-1] * n
    timer = [0]
    result = []

    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        for v in graph[u]:
            if v == parent:
                continue
            if disc[v] == -1:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    result.append([u, v])
            else:
                low[u] = min(low[u], disc[v])

    dfs(0, -1)
    return result
```

**Time Complexity:** O(V + E) - DFS traversal
**Space Complexity:** O(V + E) - graph storage and recursion stack

---

## Problem 35: Binary Search Tree Iterator II

**Statement:** Implement a BST iterator that supports: hasNext(), next(), hasPrev(), and prev(). The iterator works like a sorted array traversal but uses the BST structure.

**Approach:** Use a stack to simulate inorder traversal. hasNext/next work as standard BST iterator (push left nodes). prev() needs a secondary stack to track previously visited nodes.

```python
class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self.back_stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def hasNext(self):
        return bool(self.stack or self.back_stack)

    def next(self):
        if self.back_stack:
            node = self.back_stack.pop()
        else:
            node = self.stack.pop()
            if node.right:
                self._push_left(node.right)
        return node.val

    def hasPrev(self):
        return bool(self.back_stack)

    def prev(self):
        if self.back_stack:
            node = self.back_stack.pop()
        else:
            node = self.stack.pop()
            if node.left:
                self._push_left(node.left)
        return node.val
```

**Time Complexity:** O(h) per next/prev operation
**Space Complexity:** O(n) - for stacks holding nodes

---

## Problem 36: Maximum Binary Tree II

**Statement:** A maximum binary tree is built from an array: pick the max, left subtree from left subarray, right subtree from right subarray. Given the root of a max binary tree and an integer val, insert val into the tree and return the root.

**Approach:** Traverse down the rightmost path. Find the first node where val > node.val. The current node becomes the left child of a new node with val. The new node becomes the right child of the parent. If no such node exists, val becomes the new root.

```python
def insertIntoMaxTree(root, val):
    parent = None
    node = root
    while node:
        if val > node.val:
            parent = node
            node = node.right
        else:
            node = node.right

    new_node = TreeNode(val)
    if not parent:
        new_node.left = root
        return new_node

    new_node.left = parent.right
    parent.right = new_node
    return root
```

**Time Complexity:** O(h) - traverse rightmost path
**Space Complexity:** O(1) - iterative

---

## Problem 37: Vertical Order Traversal II

**Statement:** Given a binary tree, return the vertical order traversal of its nodes' values. For each column, nodes should be sorted by row (top to bottom), and within the same row, by value (left to right).

**Approach:** BFS with (node, row, col) tuples. Store (row, val) for each column in a dictionary. After BFS, sort each column by row, then by value for same row. Build result by iterating columns from left to right.

```python
from collections import defaultdict, deque

def verticalTraversal(root):
    if not root:
        return []
    col_map = defaultdict(list)
    queue = deque([(root, 0, 0)])

    while queue:
        for _ in range(len(queue)):
            node, row, col = queue.popleft()
            col_map[col].append((row, node.val))
            if node.left:
                queue.append((node.left, row + 1, col - 1))
            if node.right:
                queue.append((node.right, row + 1, col + 1))

    result = []
    for col in sorted(col_map.keys()):
        col_map[col].sort()
        result.append([val for _, val in col_map[col]])
    return result
```

**Time Complexity:** O(n log n) - sorting within each column
**Space Complexity:** O(n) - storing all nodes in the dictionary

---

## Problem 38: Longest Univalue Path

**Statement:** Given a binary tree, find the length of the longest path where each node in the path has the same value. The path length is measured in edges.

**Approach:** Post-order DFS. For each node, recursively get the longest univalue path from left and right children. If the child's value matches the current node's value, extend that path. Update the global maximum with left + right (path through current node). Return the longer of the two single-side paths for parent use.

```python
def longestUnivaluePath(root):
    max_path = [0]

    def dfs(node):
        if not node:
            return 0
        left_len = dfs(node.left)
        right_len = dfs(node.right)
        left_arrow = left_len + 1 if node.left and node.left.val == node.val else 0
        right_arrow = right_len + 1 if node.right and node.right.val == node.val else 0
        max_path[0] = max(max_path[0], left_arrow + right_arrow)
        return max(left_arrow, right_arrow)

    dfs(root)
    return max_path[0]
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 39: Sum of Nodes with Even Valued Grandparent

**Statement:** Given a binary tree, return the sum of values of nodes whose grandparent has an even value. If a node does not have a grandparent, it is not included.

**Approach:** DFS passing parent and grandparent values. If grandparent's value is even, add the current node's value. Recurse on children, passing current node as parent and parent as grandparent.

```python
def sumEvenGrandparent(root):
    total = [0]

    def dfs(node, parent_val, grandparent_val):
        if not node:
            return
        if grandparent_val % 2 == 0:
            total[0] += node.val
        dfs(node.left, node.val, parent_val)
        dfs(node.right, node.val, parent_val)

    dfs(root, 1, 1)  # dummy non-even values for root's non-existent parents
    return total[0]
```

**Time Complexity:** O(n) - visit every node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 40: All Elements in Two Binary Search Trees

**Statement:** Given two BSTs root1 and root2, return a list containing all integers from both trees sorted in ascending order.

**Approach:** Inorder traverse both BSTs to get two sorted lists. Merge the two sorted lists into one sorted list using two-pointer technique.

```python
def getAllElements(root1, root2):
    def inorder(node, result):
        if not node:
            return
        inorder(node.left, result)
        result.append(node.val)
        inorder(node.right, result)

    list1, list2 = [], []
    inorder(root1, list1)
    inorder(root2, list2)

    merged = []
    i, j = 0, 0
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1
    while i < len(list1):
        merged.append(list1[i])
        i += 1
    while j < len(list2):
        merged.append(list2[j])
        j += 1
    return merged
```

**Time Complexity:** O(n1 + n2) - traverse both trees and merge
**Space Complexity:** O(n1 + n2) - storing the two sorted lists

---

# Summary Table

| #  | Problem                                    | Difficulty | Time       | Space |
|----|--------------------------------------------|------------|------------|-------|
| 1  | Sum of Left Leaves                         | Easy       | O(n)       | O(h)  |
| 2  | Two Sum IV - BST                           | Easy       | O(n)       | O(n)  |
| 3  | Find Mode in BST                           | Easy       | O(n)       | O(h)  |
| 4  | Increasing BST                             | Easy       | O(n)       | O(h)  |
| 5  | Range Sum of BST                           | Easy       | O(n)       | O(h)  |
| 6  | Minimum Absolute Difference in BST         | Easy       | O(n)       | O(h)  |
| 7  | Check if Tree is Symmetric                 | Easy       | O(n)       | O(h)  |
| 8  | Univalued Binary Tree                      | Easy       | O(n)       | O(h)  |
| 9  | Count Good Nodes                           | Easy       | O(n)       | O(h)  |
| 10 | Leaf-Similar Trees                         | Easy       | O(n1+n2)   | O(n)  |
| 11 | Maximum Depth of N-ary Tree                | Easy       | O(n)       | O(h)  |
| 12 | N-ary Tree Level Order Traversal           | Easy       | O(n)       | O(n)  |
| 13 | Level Order Traversal II (Bottom-Up)       | Medium     | O(n)       | O(n)  |
| 14 | Binary Tree Tilt                           | Medium     | O(n)       | O(h)  |
| 15 | Find Bottom Left Tree Value                | Medium     | O(n)       | O(w)  |
| 16 | Largest Value in Each Tree Row             | Medium     | O(n)       | O(w)  |
| 17 | Closest Value in BST                       | Medium     | O(h)       | O(1)  |
| 18 | Inorder Successor in BST                   | Medium     | O(h)       | O(1)  |
| 19 | Delete Node in BST                         | Medium     | O(h)       | O(h)  |
| 20 | Construct BST from Preorder                | Medium     | O(n)       | O(h)  |
| 21 | Convert BST to Greater Tree                | Medium     | O(n)       | O(h)  |
| 22 | Diameter of N-ary Tree                     | Medium     | O(n)       | O(h)  |
| 23 | Step-By-Step Directions                    | Medium     | O(n)       | O(h)  |
| 24 | Binary Tree Right Side View                | Medium     | O(n)       | O(w)  |
| 25 | Even Odd Tree                              | Medium     | O(n)       | O(w)  |
| 26 | Maximum Level Sum                          | Medium     | O(n)       | O(w)  |
| 27 | Deepest Leaves Sum                         | Medium     | O(n)       | O(w)  |
| 28 | Check Completeness of Binary Tree          | Medium     | O(n)       | O(w)  |
| 29 | Trim a Binary Search Tree                  | Medium     | O(n)       | O(h)  |
| 30 | Flatten Binary Tree to Linked List         | Medium     | O(n)       | O(h)  |
| 31 | Binary Tree Cameras                        | Hard       | O(n)       | O(h)  |
| 32 | Find Duplicate Subtrees                    | Hard       | O(n^2)     | O(n)  |
| 33 | Serialize/Deserialize N-ary Tree           | Hard       | O(n)       | O(n)  |
| 34 | Critical Connections (Tarjan's)            | Hard       | O(V+E)     | O(V)  |
| 35 | Binary Search Tree Iterator II             | Hard       | O(h)       | O(n)  |
| 36 | Maximum Binary Tree II                     | Hard       | O(h)       | O(1)  |
| 37 | Vertical Order Traversal II                | Hard       | O(n log n) | O(n)  |
| 38 | Longest Univalue Path                      | Hard       | O(n)       | O(h)  |
| 39 | Sum of Nodes with Even Grandparent         | Hard       | O(n)       | O(h)  |
| 40 | All Elements in Two BSTs                   | Hard       | O(n1+n2)   | O(n)  |

---

> **Total: 40 problems | 12 Easy + 18 Medium + 10 Hard**
> **Pair with `tree_problems_batch1.md` for complete tree mastery!**

---

# Quick Reference: Key Tree Patterns

## Pattern 1: Recursive DFS (Most Common)

Used in: Problems 1, 2, 5, 7, 8, 9, 10, 11, 14, 21, 22, 29, 30, 31, 32, 38, 39

```python
def dfs(node):
    if not node:
        return base_case
    left = dfs(node.left)
    right = dfs(node.right)
    # process current node
    return result
```

**When to use:** When you need to process children before parent (post-order), or when you need information from subtrees.

---

## Pattern 2: BFS Level Order (Very Common)

Used in: Problems 12, 13, 15, 16, 24, 25, 26, 27, 28, 37

```python
from collections import deque

def bfs(root):
    queue = deque([root])
    while queue:
        for _ in range(len(queue)):
            node = queue.popleft()
            # process node
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
```

**When to use:** When you need level-by-level processing, finding level properties, or level order traversal.

---

## Pattern 3: BST Property Exploitation

Used in: Problems 3, 4, 5, 6, 17, 18, 19, 20, 21, 29, 35

```python
def bst_operation(root, target):
    if not root:
        return None
    if target < root.val:
        return bst_operation(root.left, target)
    elif target > root.val:
        return bst_operation(root.right, target)
    else:
        # found target
```

**When to use:** When the problem specifically involves a BST and you can leverage the ordering property to prune the search space.

---

## Pattern 4: Inorder Traversal (BST -> Sorted)

Used in: Problems 3, 4, 6, 21, 35, 40

```python
def inorder(node):
    if not node:
        return
    inorder(node.left)
    # process node (nodes are in sorted order for BST)
    inorder(node.right)
```

**When to use:** When you need sorted order from a BST, or when comparing adjacent elements in sorted order.

---

## Pattern 5: Serialization / Hashing

Used in: Problems 32, 33

```python
def serialize(node):
    if not node:
        return "#"
    return f"{node.val},{serialize(node.left)},{serialize(node.right)}"
```

**When to use:** When you need to compare subtrees, or when you need to flatten a tree into a string representation.

---

## Pattern 6: Post-order with State

Used in: Problems 14, 21, 22, 31, 38

```python
def postorder(node):
    if not node:
        return state  # null state
    left_state = postorder(node.left)
    right_state = postorder(node.right)
    # compute current state from children
    return current_state
```

**When to use:** When the decision at a node depends on information from its children (e.g., cameras, diameter, path problems).

---

## Pattern 7: Two-Pointer Merge

Used in: Problem 40

```python
def merge_sorted(l1, l2):
    result = []
    i, j = 0, 0
    while i < len(l1) and j < len(l2):
        if l1[i] <= l2[j]:
            result.append(l1[i])
            i += 1
        else:
            result.append(l2[j])
            j += 1
    result.extend(l1[i:])
    result.extend(l2[j:])
    return result
```

**When to use:** When you need to combine two sorted sequences from separate tree traversals.

---

# Edge Cases Checklist for Tree Problems

| Edge Case                        | How to Handle                                    |
|----------------------------------|--------------------------------------------------|
| Empty tree (root = None)         | Return 0, None, False, or [] as appropriate      |
| Single node                     | Handle as both root and leaf                      |
| Skewed tree (all left/right)    | Height = n, width = 1                            |
| Complete binary tree            | Width at level i = 2^i                           |
| All nodes same value            | Check for univalued tree problems                |
| Negative values                 | Use float('-inf') or float('inf') carefully      |
| BST with duplicates             | Account for duplicates in comparisons             |
| Very deep tree                  | Watch for recursion depth (use iterative)        |
| Very wide tree                  | Watch for queue size in BFS                      |

---

# Complexity Quick Reference

| Operation                        | Time     | Space    |
|----------------------------------|----------|----------|
| DFS (any order)                  | O(n)     | O(h)     |
| BFS (level order)                | O(n)     | O(w)     |
| BST Search/Insert/Delete         | O(h)     | O(h)     |
| Inorder Traversal                | O(n)     | O(h)     |
| Serialize/Deserialize            | O(n)     | O(n)     |
| Find LCA                         | O(n)     | O(h)     |
| Diameter of Tree                 | O(n)     | O(h)     |
| Level Order Traversal            | O(n)     | O(n)     |

Where: n = number of nodes, h = height of tree, w = maximum width of tree

For balanced BST: h = log(n)
For skewed BST: h = n
For complete binary tree: w = n/2

---

# Tips for Infosys SP DSE Tree Problems

1. **Always start with the base case** -- what happens when the node is None?

2. **Choose the right traversal:**
   - Pre-order: when you need to process parent before children
   - In-order: when you need sorted order from BST
   - Post-order: when you need children's info before parent
   - Level-order: when you need level-by-level processing

3. **BST problems can often be solved in O(h) time** by exploiting the ordering property.

4. **For "find all" problems**, use a hash map / dictionary for counting or grouping.

5. **For path problems**, consider both DFS (path from root) and finding LCA.

6. **For optimization problems on trees**, think about:
   - What information do I need from my children?
   - What information do I need to pass to my parent?
   - Can I maintain a global/running answer?

7. **Iterative vs Recursive:**
   - Recursive is simpler and preferred for interviews
   - Use iterative if recursion depth is a concern (very deep trees)
   - For iterative DFS, use an explicit stack
   - For iterative BFS, use a deque

8. **Common mistakes to avoid:**
   - Forgetting to handle the empty tree case
   - Modifying the tree while traversing without saving references
   - Off-by-one errors in level tracking
   - Not resetting state between recursive calls
   - Using global variables incorrectly in recursion

---

# Interview Simulation Questions

These are the kinds of follow-up questions interviewers might ask:

**After Problem 31 (Binary Tree Cameras):**
- Can you do it iteratively?
- What if a camera can monitor nodes 2 hops away instead of 1?

**After Problem 34 (Critical Connections):**
- Can you explain why Tarjan's algorithm works?
- How would you find articulation points (nodes whose removal disconnects the graph)?

**After Problem 19 (Delete Node in BST):**
- What if we need to delete multiple nodes?
- How would you handle duplicate values in the BST?

**After Problem 30 (Flatten to Linked List):**
- Can you do it without recursion (iterative)?
- Can you do it using O(1) extra space (Morris traversal)?

**After Problem 32 (Duplicate Subtrees):**
- How would you optimize the serialization to avoid O(n) string operations per node?
- Can you find duplicate subtrees of at least size k?
