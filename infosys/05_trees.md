# Trees

## Problem 1: Binary Tree Traversals (Inorder, Preorder, Postorder)
**Difficulty: Easy | Marks: 20**

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder(root):
    return inorder(root.left) + [root.val] + inorder(root.right) if root else []

def preorder(root):
    return [root.val] + preorder(root.left) + preorder(root.right) if root else []

def postorder(root):
    return postorder(root.left) + postorder(root.right) + [root.val] if root else []

# Iterative inorder
def inorder_iterative(root):
    result, stack = [], []
    curr = root
    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result
```

---

## Problem 2: Maximum Depth of Binary Tree
**Difficulty: Easy | Marks: 20**

```python
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

---

## Problem 3: Diameter of Binary Tree
**Difficulty: Easy-Medium | Marks: 20**

```python
def diameter_of_binary_tree(root):
    diameter = 0
    def height(node):
        nonlocal diameter
        if not node:
            return 0
        left = height(node.left)
        right = height(node.right)
        diameter = max(diameter, left + right)
        return 1 + max(left, right)
    height(root)
    return diameter
```

---

## Problem 4: Validate Binary Search Tree
**Difficulty: Medium | Marks: 30**

```python
def is_valid_bst(root):
    def validate(node, low, high):
        if not node:
            return True
        if node.val <= low or node.val >= high:
            return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)
    return validate(root, float('-inf'), float('inf'))
```

---

## Problem 5: Lowest Common Ancestor of BST
**Difficulty: Easy-Medium | Marks: 20-30**

```python
def lowest_common_ancestor_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
```

---

## Problem 6: Lowest Common Ancestor of Binary Tree
**Difficulty: Medium | Marks: 30**

```python
def lowest_common_ancestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right
```

---

## Problem 7: Binary Tree Level Order Traversal
**Difficulty: Medium | Marks: 30**

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
```

---

## Problem 8: Zigzag Level Order Traversal
**Difficulty: Medium | Marks: 30**

```python
from collections import deque

def zigzag_level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    left_to_right = True
    while queue:
        level = deque()
        for _ in range(len(queue)):
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

---

## Problem 9: Path Sum
**Difficulty: Easy | Marks: 20**

```python
def has_path_sum(root, target_sum):
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == target_sum
    return has_path_sum(root.left, target_sum - root.val) or \
           has_path_sum(root.right, target_sum - root.val)
```

---

## Problem 10: Path Sum II (All Paths)
**Difficulty: Medium | Marks: 30**

```python
def path_sum(root, target_sum):
    result = []
    def dfs(node, remaining, path):
        if not node:
            return
        if not node.left and not node.right:
            if remaining == node.val:
                result.append(path + [node.val])
            return
        dfs(node.left, remaining - node.val, path + [node.val])
        dfs(node.right, remaining - node.val, path + [node.val])
    dfs(root, target_sum, [])
    return result
```

---

## Problem 11: Path Sum III (Any direction, not necessarily root-leaf)
**Difficulty: Medium | Marks: 30**

```python
def path_sum_iii(root, target_sum):
    prefix = {0: 1}
    def dfs(node, curr_sum):
        if not node:
            return 0
        curr_sum += node.val
        count = prefix.get(curr_sum - target_sum, 0)
        prefix[curr_sum] = prefix.get(curr_sum, 0) + 1
        count += dfs(node.left, curr_sum) + dfs(node.right, curr_sum)
        prefix[curr_sum] -= 1
        return count
    return dfs(root, 0)
```

---

## Problem 12: Construct Binary Tree from Inorder and Preorder
**Difficulty: Medium | Marks: 30**

```python
def build_tree(preorder, inorder):
    if not inorder:
        return None
    root_val = preorder.pop(0)
    root = TreeNode(root_val)
    idx = inorder.index(root_val)
    root.left = build_tree(preorder, inorder[:idx])
    root.right = build_tree(preorder, inorder[idx + 1:])
    return root
```

---

## Problem 13: Binary Tree Right Side View
**Difficulty: Medium | Marks: 30**

```python
from collections import deque

def right_side_view(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_len = len(queue)
        for i in range(level_len):
            node = queue.popleft()
            if i == level_len - 1:
                result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return result
```

---

## Problem 14: Serialize and Deserialize Binary Tree
**Difficulty: Hard | Marks: 50**

```python
def serialize(root):
    def helper(node):
        if not node:
            vals.append('#')
            return
        vals.append(str(node.val))
        helper(node.left)
        helper(node.right)
    vals = []
    helper(root)
    return ','.join(vals)

def deserialize(data):
    def helper():
        val = next(vals)
        if val == '#':
            return None
        node = TreeNode(int(val))
        node.left = helper()
        node.right = helper()
        return node
    vals = iter(data.split(','))
    return helper()
```

---

## Problem 15: Kth Smallest Element in BST
**Difficulty: Medium | Marks: 30**

```python
def kth_smallest(root, k):
    stack = []
    curr = root
    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        k -= 1
        if k == 0:
            return curr.val
        curr = curr.right
    return -1
```

---

## Problem 16: Flatten Binary Tree to Linked List
**Difficulty: Medium | Marks: 30**

```python
def flatten(root):
    if not root:
        return
    flatten(root.left)
    flatten(root.right)
    temp = root.right
    root.right = root.left
    root.left = None
    while root.right:
        root = root.right
    root.right = temp
```

---

## Problem 17: Maximum Path Sum (Any Node to Any Node)
**Difficulty: Hard | Marks: 50**

```python
def max_path_sum(root):
    max_sum = float('-inf')
    def gain(node):
        nonlocal max_sum
        if not node:
            return 0
        left_gain = max(gain(node.left), 0)
        right_gain = max(gain(node.right), 0)
        max_sum = max(max_sum, node.val + left_gain + right_gain)
        return node.val + max(left_gain, right_gain)
    gain(root)
    return max_sum
```

---

## Problem 18: Populating Next Right Pointers in Each Node
**Difficulty: Medium | Marks: 30**

```python
from collections import deque

def connect(root):
    if not root:
        return None
    queue = deque([root])
    while queue:
        level_len = len(queue)
        for i in range(level_len):
            node = queue.popleft()
            if i < level_len - 1:
                node.next = queue[0]
            if node.left:
                queue.append(node.left)
                queue.append(node.right)
    return root
```

---

## Problem 19: Count Complete Tree Nodes
**Difficulty: Medium | Marks: 30**

```python
def count_nodes(root):
    if not root:
        return 0
    def left_depth(node):
        d = 0
        while node:
            node = node.left
            d += 1
        return d
    def right_depth(node):
        d = 0
        while node:
            node = node.right
            d += 1
        return d
    left_d = left_depth(root)
    right_d = right_depth(root)
    if left_d == right_d:
        return (1 << left_d) - 1
    return 1 + count_nodes(root.left) + count_nodes(root.right)
```

---

## Problem 20: Binary Tree Cameras
**Difficulty: Hard | Marks: 50**

```python
def min_camera_cover(root):
    cameras = 0
    def dfs(node):
        nonlocal cameras
        if not node:
            return 2
        left = dfs(node.left)
        right = dfs(node.right)
        if left == 0 or right == 0:
            cameras += 1
            return 1
        if left == 1 or right == 1:
            return 2
        return 0
    return cameras + (1 if dfs(root) == 0 else 0)
```
