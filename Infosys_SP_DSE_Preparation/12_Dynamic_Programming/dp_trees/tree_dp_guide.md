# DP on Trees — Complete Guide

## What is Tree DP?

Tree DP applies DP to hierarchical (tree) data:
- **Post-order traversal**: solve children first, compute parent
- **Two-state DP**: for each node, maintain dp[node][state1], dp[node][state2], etc.
- **In-Out DP**: dfs_in (going down) + dfs_out (coming up) for rerooting

Core pattern:
```python
def dfs(node, parent):
    for child in node.children:
        if child != parent:
            dfs(child, node)
            # combine child results into node
```

---

## Diameter of Tree

Given a tree, find the longest path (diameter) between any two nodes.

**Concept:** For each node as LCA of endpoints:
- diameter = max(child1_height + child2_height + 2) across all pairs of children

```python
def tree_diameter(graph: list) -> int:
    n = len(graph)
    visited = [False] * n
    diameter = 0

    def height(node: int) -> int:
        nonlocal diameter
        visited[node] = True
        max1 = max2 = 0
        for nei in graph[node]:
            if not visited[nei]:
                child_h = height(nei) + 1
                if child_h > max1:
                    max2, max1 = max1, child_h
                elif child_h > max2:
                    max2 = child_h
        diameter = max(diameter, max1 + max2)
        return max1

    height(0)
    return diameter

# Alternative: Two BFS approach (easier)
from collections import deque

def tree_diameter_bfs(graph: list) -> int:
    def bfs(start: int):
        dist = [-1] * len(graph)
        dist[start] = 0
        q = deque([start])
        farthest_node = start
        while q:
            node = q.popleft()
            for nei in graph[node]:
                if dist[nei] == -1:
                    dist[nei] = dist[node] + 1
                    q.append(nei)
                    if dist[nei] > dist[farthest_node]:
                        farthest_node = nei
        return farthest_node, dist[farthest_node]

    node_a, _ = bfs(0)
    node_b, dist = bfs(node_a)
    return dist

# Example:
#       0
#     /   \
#    1     2
#   / \     \
#  3   4     5
# Answer: 4 (3-1-0-2-5 or 4-1-0-2-5)

# Time: O(n), Space: O(n)
```

---

## Maximum Path Sum (Binary Tree)

Given a binary tree, find maximum path sum. Path can start and end anywhere.

```python
def max_path_sum(root) -> int:
    max_sum = float('-inf')

    def dfs(node):
        nonlocal max_sum
        if not node:
            return 0
        left = max(dfs(node.left), 0)
        right = max(dfs(node.right), 0)
        max_sum = max(max_sum, left + right + node.val)
        return node.val + max(left, right)

    dfs(root)
    return max_sum

# Example:
# Tree:   -10
#        /   \
#       9    20
#           /  \
#          15   7
# Answer: 42 (15 + 20 + 7)

# Time: O(n), Space: O(h)
```

---

## Binary Tree Maximum Path Sum Between Leaves

Max path sum that MUST start and end at leaves.

```python
def max_path_sum_leaves(root) -> int:
    max_sum = float('-inf')

    def dfs(node):
        nonlocal max_sum
        if not node:
            return float('-inf')
        if not node.left and not node.right:
            return node.val
        left = dfs(node.left)
        right = dfs(node.right)
        if left != float('-inf') and right != float('-inf'):
            max_sum = max(max_sum, left + right + node.val)
        return node.val + max(left, right)

    dfs(root)
    return max_sum if max_sum != float('-inf') else root.val

# Time: O(n), Space: O(h)
```

---

## House Robber III

The houses form a binary tree. Two directly linked houses cannot be robbed on same night. Maximize sum.

**Concept:** dp[node][0] = not robbing node, dp[node][1] = robbing node

```python
def rob_tree(root) -> int:
    def dfs(node):
        if not node:
            return (0, 0)  # (rob_this, not_rob_this)

        left = dfs(node.left)
        right = dfs(node.right)

        rob_this = node.val + left[1] + right[1]
        not_rob_this = max(left) + max(right)

        return (rob_this, not_rob_this)

    return max(dfs(root))

# Example:
# Tree:     3
#         /   \
#        2     3
#         \     \
#          3     1
# Answer: 7 (3 + 3 + 1 = 7; rob 3 (root) + 3 (right child) + 1 (right grandchild))

# Time O(n), Space: O(h)
```

---

## Tree Coloring / Vertex Cover

Given a tree, find minimum vertices to select such that every edge has at least one endpoint selected.

```python
def vertex_cover(root) -> int:
    def dfs(node):
        if not node:
            return (0, 0)  # (covered, not_covered)
        left = dfs(node.left)
        right = dfs(node.right)
        not_cover = left[0] + right[0]
        cover = 1 + min(left) + min(right)
        return (cover, not_cover)

    if not root:
        return 0
    return min(dfs(root))

# Time: O(n), Space: O(h)
```

---

## Maximum Independent Set in Tree

Find max size of a set of nodes where no two are adjacent.

```python
def max_independent_set(root) -> int:
    def dfs(node):
        if not node:
            return (0, 0)  # (take_node, skip_node)
        left = dfs(node.left)
        right = dfs(node.right)
        take_node = 1 + left[1] + right[1]
        skip_node = max(left) + max(right)
        return (take_node, skip_node)

    return max(dfs(root))

# Time: O(n), Space: O(h)
```

---

## Count Paths with Sum K (Binary Tree)

Count paths that sum to a given value. Path can start anywhere and go downwards.

```python
def path_sum_count(root, target_sum: int) -> int:
    count = 0
    prefix = {}

    def dfs(node, curr_sum):
        nonlocal count
        if not node:
            return
        curr_sum += node.val
        if curr_sum == target_sum:
            count += 1
        count += prefix.get(curr_sum - target_sum, 0)
        prefix[curr_sum] = prefix.get(curr_sum, 0) + 1
        dfs(node.left, curr_sum)
        dfs(node.right, curr_sum)
        prefix[curr_sum] -= 1

    dfs(root, 0)
    return count

# Example:
# Tree:     10
#         /    \
#        5     -3
#       / \      \
#      3   2     11
#     / \   \
#    3  -2   1
# targetSum = 8, Answer: 3 (5+3, 5+2+1, -3+11)

# Time: O(n), Space: O(h)
```

---

## Binary Tree Cameras

Given a binary tree, install cameras on nodes. Each camera monitors its node, parent, and immediate children. Find min cameras needed.

**Concept:** Three states: 0=not monitored, 1=monitored by child, 2=has camera

```python
def min_camera_cover(root) -> int:
    cameras = 0

    def dfs(node):
        nonlocal cameras
        if not node:
            return 1  # Null nodes are covered
        left = dfs(node.left)
        right = dfs(node.right)
        # If any child is uncovered, place camera here
        if left == 0 or right == 0:
            cameras += 1
            return 2
        # If any child has a camera, this node is covered
        if left == 2 or right == 2:
            return 1
        # Children are covered but this node is not yet
        return 0

    root_state = dfs(root)
    return cameras + (1 if root_state == 0 else 0)

# Example:
# Tree:     0
#         /
#        0
#       / \
#      0   1 (already has camera -> not possible, just illustration)
# Simplified:        0
#                  /
#                 0
#                /
#               0
# Answer: 1 (camera at middle node)

# Time: O(n), Space: O(h)
```

---

## Delete Nodes and Return Forest

Given a binary tree root and array of nodes to delete, return forest of remaining trees.

```python
def del_nodes(root: TreeNode, to_delete: list) -> list:
    to_delete = set(to_delete)
    forest = []

    def dfs(node, is_root):
        if not node:
            return None
        node_deleted = node.val in to_delete
        if is_root and not node_deleted:
            forest.append(node)
        node.left = dfs(node.left, node_deleted)
        node.right = dfs(node.right, node_deleted)
        return None if node_deleted else node

    dfs(root, True)
    return forest

# Time: O(n), Space: O(h)
```

---

## Most Frequent Subtree Sum

Given a binary tree, find the most frequent subtree sum (sum of all node values in subtree).

```python
def most_frequent_subtree_sum(root) -> list:
    freq = {}
    max_freq = 0

    def subtree_sum(node):
        nonlocal max_freq
        if not node:
            return 0
        total = node.val + subtree_sum(node.left) + subtree_sum(node.right)
        freq[total] = freq.get(total, 0) + 1
        max_freq = max(max_freq, freq[total])
        return total

    subtree_sum(root)
    return [s for s, f in freq.items() if f == max_freq]

# Time: O(n), Space: O(n)
```

---

## Summary Table

| Problem | States | Transitions | Time |
|---------|--------|-------------|------|
| Diameter | heights | max of two largest child heights | O(n) |
| Max Path Sum | path sum | left + right + node.val | O(n) |
| House Robber III | take/skip | 2-state DP per node | O(n) |
| Vertex Cover | cover/skip | cover=1+min(children) | O(n) |
| Max Independent Set | take/skip | take=1+skip_children | O(n) |
| Path Sum Count | prefix sums | hashmap + backtrack | O(n) |
| Binary Tree Cameras | 3 states | 0/1/2 for coverage | O(n) |
