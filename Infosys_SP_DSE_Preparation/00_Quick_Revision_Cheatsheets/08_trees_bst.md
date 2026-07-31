# Trees & BST — Last-Minute Revision

Copy-paste ready, tested Python 3 templates for tree traversal, utilities, and every essential BST operation.

## TreeNode Class

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

Build a tree quickly from an array (level-order, `None` = missing node, like LeetCode):

```python
from collections import deque

def build_tree(arr):
    if not arr:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while i < len(arr):
        node = q.popleft()
        if arr[i] is not None:
            node.left = TreeNode(arr[i])
            q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            q.append(node.right)
        i += 1
    return root
```

| Utility | Time | Space |
|---|---|---|
| build_tree | O(n) | O(n) |

## Traversals — Recursive (trivial, uses call stack)

```python
def preorder(root):          # root, left, right
    res = []
    def dfs(node):
        if not node:
            return
        res.append(node.val)
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return res

def inorder(root):           # left, root, right
    res = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        res.append(node.val)
        dfs(node.right)
    dfs(root)
    return res

def postorder(root):         # left, right, root
    res = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        dfs(node.right)
        res.append(node.val)
    dfs(root)
    return res
```

## Traversals — Iterative (stack)

```python
def preorder_iter(root):     # root, left, right
    res = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node:
            res.append(node.val)
            stack.append(node.right)   # push right first so left pops first
            stack.append(node.left)
    return res

def inorder_iter(root):      # left, root, right — the stack holds "future work"
    res = []
    stack = []
    cur = root
    while cur or stack:
        while cur:                 # go as far left as possible
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()          # pop -> visit
        res.append(cur.val)
        cur = cur.right            # then go right
    return res

def postorder_iter(root):    # left, right, root = reverse of (root, right, left)
    res = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node:
            res.append(node.val)
            stack.append(node.left)    # push left first so right is processed first
            stack.append(node.right)
    return res[::-1]                  # then reverse
```

## Level Order Traversal (BFS — list of lists per level)

```python
def level_order(root):
    if not root:
        return []
    res = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):    # snapshot size: one level at a time
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(level)
    return res
```

| Template | Time | Space |
|---|---|---|
| recursive pre/in/post | O(n) | O(n) call stack (O(log n) balanced) |
| iterative pre/in/post | O(n) | O(n) stack |
| level order | O(n) | O(n) queue (widest level) |

## Tree Utilities

```python
def height(root):                    # height of the tree (edges from root to deepest leaf)
    if not root:
        return 0
    return 1 + max(height(root.left), height(root.right))

def count_nodes(root):
    if not root:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)

def max_depth(root):                 # same as height for a tree, counts nodes
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

def diameter(root):                  # longest path between any two nodes (edges)
    best = 0
    def dfs(node):
        nonlocal best
        if not node:
            return 0
        l = dfs(node.left)
        r = dfs(node.right)
        best = max(best, l + r)      # path through this node
        return 1 + max(l, r)         # height of this node
    dfs(root)
    return best

def is_same_tree(p, q):
    if not p and not q:
        return True
    if not p or not q:
        return False
    return p.val == q.val and is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)

def is_symmetric(root):
    def mirror(a, b):
        if not a and not b:
            return True
        if not a or not b:
            return False
        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)
    return mirror(root.left, root.right) if root else True
```

| Utility | Time | Space |
|---|---|---|
| height / count / depth | O(n) | O(n) |
| diameter | O(n) | O(n) |
| same tree / symmetric | O(n) | O(n) |

## BST — Insert / Search / Delete / Validate

```python
def bst_insert(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = bst_insert(root.left, val)
    else:
        root.right = bst_insert(root.right, val)
    return root

def bst_search(root, val):
    cur = root
    while cur:
        if val == cur.val:
            return cur
        cur = cur.left if val < cur.val else cur.right
    return None

def bst_delete(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = bst_delete(root.left, key)
    elif key > root.val:
        root.right = bst_delete(root.right, key)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        # two children: replace with inorder successor (smallest in right subtree)
        succ = root.right
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = bst_delete(root.right, succ.val)
    return root

def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root:
        return True
    if not (lo < root.val < hi):
        return False
    return is_valid_bst(root.left, lo, root.val) and is_valid_bst(root.right, root.val, hi)
```

BST validate — alternative via inorder (must be strictly increasing):

```python
def is_valid_bst_inorder(root):
    prev = float('-inf')
    stack = []
    cur = root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        if cur.val <= prev:
            return False
        prev = cur.val
        cur = cur.right
    return True
```

| BST op | Time (balanced) | Space |
|---|---|---|
| insert / search / delete | O(log n) avg, O(n) worst | O(log n) recursion |
| validate | O(n) | O(n) stack |

## Lowest Common Ancestor — BST version

```python
def lca_bst(root, p, q):        # p, q are TreeNode objects; both exist in tree
    cur = root
    while cur:
        if p.val < cur.val and q.val < cur.val:
            cur = cur.left
        elif p.val > cur.val and q.val > cur.val:
            cur = cur.right
        else:
            return cur          # first node that splits p and q
    return None
```

## Lowest Common Ancestor — General Binary Tree

```python
def lca(root, p, q):            # p, q exist in the tree
    if not root or root is p or root is q:
        return root
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:          # both sides contain a target -> root is LCA
        return root
    return left or right
```

| Template | Time | Space |
|---|---|---|
| lca BST | O(log n) avg, O(n) worst | O(1) |
| lca general | O(n) | O(n) |

## Path Sum Variants

```python
def has_path_sum(root, target):          # is there root->leaf path summing to target
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == target
    return has_path_sum(root.left, target - root.val) or \
           has_path_sum(root.right, target - root.val)

def path_sum_paths(root, target):        # ALL root->leaf paths summing to target
    res = []
    def dfs(node, remaining, path):
        if not node:
            return
        path.append(node.val)
        if not node.left and not node.right and remaining == node.val:
            res.append(path[:])          # copy!
        dfs(node.left, remaining - node.val, path)
        dfs(node.right, remaining - node.val, path)
        path.pop()
    dfs(root, target, [])
    return res

def max_path_sum(root):                  # max sum path between any two nodes
    best = float('-inf')
    def dfs(node):
        nonlocal best
        if not node:
            return 0
        l = max(dfs(node.left), 0)       # ignore negative contributions
        r = max(dfs(node.right), 0)
        best = max(best, l + r + node.val)
        return node.val + max(l, r)
    dfs(root)
    return best
```

| Template | Time | Space |
|---|---|---|
| has path sum | O(n) | O(n) |
| all paths | O(n) output-sensitive | O(n) |
| max path sum | O(n) | O(n) |

## Balanced BST From Sorted Array

```python
def sorted_array_to_bst(nums):           # nums is sorted ascending
    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        root = TreeNode(nums[mid])
        root.left = build(lo, mid - 1)
        root.right = build(mid + 1, hi)
        return root
    return build(0, len(nums) - 1)
```

| Template | Time | Space |
|---|---|---|
| sorted array to BST | O(n) | O(log n) recursion |

## Kth Smallest in BST — iterative inorder with stack

```python
def kth_smallest(root, k):               # 1-based k
    stack = []
    cur = root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right
    return None
```

| Template | Time | Space |
|---|---|---|
| kth smallest | O(h + k) | O(h) |

## Serialize Basics (preorder with NULL markers — the format you see in interviews)

```python
def serialize(root):                     # preorder, '#' for null
    res = []
    def dfs(node):
        if not node:
            res.append('#')
            return
        res.append(str(node.val))
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return ','.join(res)

def deserialize(data):
    it = iter(data.split(','))
    def dfs():
        v = next(it)
        if v == '#':
            return None
        node = TreeNode(int(v))
        node.left = dfs()
        node.right = dfs()
        return node
    return dfs()
```

| Template | Time | Space |
|---|---|---|
| serialize / deserialize | O(n) | O(n) |

## Quick Reference Table

| Template | Key idea | Time | Space |
|---|---|---|---|
| recursive traversals | 3 orderings | O(n) | O(n) |
| iterative traversals | explicit stack | O(n) | O(n) |
| level order | BFS + snapshot len(q) | O(n) | O(n) |
| diameter / max path | post-order accumulation | O(n) | O(n) |
| BST insert/search/delete | navigate by value | O(log n) avg | O(log n) |
| validate BST | range trick or inorder | O(n) | O(n) |
| LCA | split rule (BST) / both-sides (general) | O(log n) / O(n) | O(1) / O(n) |
| kth smallest | iterative inorder early stop | O(h+k) | O(h) |

Memory hooks:
- **Inorder of a BST is sorted** — use it for validate and kth-smallest.
- **Any tree metric that combines both children (diameter, max path sum, height) is a post-order pattern**: compute children first, combine at the parent.
- **Iterative inorder** = "go left pushing, pop and visit, go right" — memorize this one loop; preorder/postorder are one-line tweaks of it.
