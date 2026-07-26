# DP on Trees — Complete Guide

## What is Tree DP?

Tree DP applies DP to hierarchical (tree) data using a bottom-up (post-order) approach.

### Core Pattern

```
          Root
         / | \
        A  B  C       Post-order: visit ALL children first, then compute parent.
       / \   |        This guarantees children's results are ready when we process parent.
      D   E   F

  Traversal order: D, E, A, F, C, B, Root

Template:
  def dfs(node, parent):
      for child in node.children:
          if child != parent:        # Avoid going back up
              dfs(child, node)       # Solve children first (post-order)
              # Now combine child's results into node's answer

  State: dp[node][state] or return a tuple (e.g., (take, skip))
  Root answer: result computed at the root after DFS completes
```

### Tree DP vs Linear DP

```
┌──────────────────────┬───────────────────────┬─────────────────────────┐
│                      │ Linear DP             │ Tree DP                 │
├──────────────────────┼───────────────────────┼─────────────────────────┤
│ State dimension      │ dp[i] or dp[i][j]     │ dp[node] or dp[node][s] │
│ Dependency           │ dp[i] ← dp[i-1]       │ dp[node] ← dp[children] │
│ Fill order           │ Left to right         │ Post-order (bottom-up)  │
│ Space                │ O(n) or O(n²)         │ O(n) implicit via recursion│
│ Recurrence           │ From previous states  │ From children's answers │
└──────────────────────┴───────────────────────┴─────────────────────────┘
```

### Common Tree DP State Patterns

```
Two-State Pattern (most common):
  dp[node][0] = best when node is NOT selected
  dp[node][1] = best when node IS selected

  Transition:
    dp[node][1] = value(node) + Σ dp[child][0]  # children must be skipped
    dp[node][0] = Σ max(dp[child][0], dp[child][1])  # children free to choose

  Used for: Vertex Cover, Independent Set, House Robber III
```

---

## Diameter of Tree

Given a tree, find the longest path (diameter) between any two nodes.

### Visual Walkthrough

```
Tree:
       0
     /   \
    1     2
   / \     \
  3   4     5

At each node, track the TWO longest paths through children.
Diameter = max(longest1 + longest2) across all nodes.

DFS trace (post-order):
  Node 3: max1=0, max2=0 → height=0 (leaf)
  Node 4: max1=0, max2=0 → height=0 (leaf)
  Node 1: children 3,4 both height 0+1=1
           max1=1, max2=1 → diameter candidate = 1+1 = 2
           returns height=1
  Node 5: height=0 (leaf)
  Node 2: children 5 height 0+1=1 → max1=1, max2=0
           diameter candidate = 1+0 = 1
           returns height=1
  Node 0: children 1(height=1+1=2), 2(height=1+1=2)
           max1=2, max2=2 → diameter candidate = 2+2 = 4  ← MAX!
           returns height=2

  Answer: 4 (path 3→1→0→2→5)

Alternative: Two BFS approach
  1. BFS from any node → find farthest node A
  2. BFS from A → find farthest node B
  3. Distance(A, B) = diameter

  BFS from 0: farthest = 3 or 5 (distance 2)
  BFS from 3: farthest = 5 (distance 4)
  Diameter = 4 ✓
```

```python
def tree_diameter(graph: list) -> int:
    n = len(graph)
    visited = [False] * n
    diameter = 0

    def height(node: int) -> int:
        nonlocal diameter
        visited[node] = True
        max1 = max2 = 0  # Two longest child heights
        for nei in graph[node]:
            if not visited[nei]:
                child_h = height(nei) + 1
                if child_h > max1:
                    max2, max1 = max1, child_h   # Update two longest
                elif child_h > max2:
                    max2 = child_h
        diameter = max(diameter, max1 + max2)  # Best path through this node
        return max1  # Return longest path to parent

    height(0)
    return diameter

# Time: O(n), Space: O(n)
```

---

## Maximum Path Sum (Binary Tree)

Given a binary tree, find maximum path sum. Path can start and end anywhere.

### Visual Walkthrough

```
Tree:      -10
          /   \
         9    20
             /  \
            15   7

At each node, consider: path THROUGH this node = left + node + right

DFS trace (post-order):
  Node 9:  left=0, right=0 → path_through = 9.  Return max(9,0)=9 to parent
  Node 15: left=0, right=0 → path_through = 15. Return 15 to parent
  Node 7:  left=0, right=0 → path_through = 7.  Return 7 to parent
  Node 20: left=15, right=7
            path_through = 15 + 20 + 7 = 42  ← global max!
            Return 20 + max(15,7) = 35 to parent
  Node -10: left=9, right=35 (from node 20)
             path_through = 9 + (-10) + 35 = 34
             Return -10 + max(9,35) = 25 to parent

  Global max = 42 (path: 15→20→7)

Key: We take max(dfs, 0) for left/right to handle negative nodes.
     Negative paths are skipped (better to not include them).
```

```python
def max_path_sum(root) -> int:
    max_sum = float('-inf')

    def dfs(node):
        nonlocal max_sum
        if not node:
            return 0
        # Get max path sum from each child, skip if negative
        left = max(dfs(node.left), 0)
        right = max(dfs(node.right), 0)
        # Path THROUGH this node (can be the global answer)
        max_sum = max(max_sum, left + right + node.val)
        # Return the best single branch to parent
        return node.val + max(left, right)

    dfs(root)
    return max_sum

# Time: O(n), Space: O(h) — h = height of tree (recursion stack)
```

### Binary Tree Maximum Path Sum Between Leaves

Max path sum that MUST start and end at leaves.

```python
def max_path_sum_leaves(root) -> int:
    max_sum = float('-inf')

    def dfs(node):
        nonlocal max_sum
        if not node:
            return float('-inf')  # Indicates no leaf path exists
        if not node.left and not node.right:
            return node.val  # Leaf node
        left = dfs(node.left)
        right = dfs(node.right)
        # Only update if BOTH children provide valid leaf paths
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

### Visual Walkthrough

```
Tree:     3
        /   \
       2     3
        \     \
         3     1

Two-state DP at each node:
  rob_this  = value of robbing this node + skip both children
  skip_this = best from children (each child can be robbed or skipped)

DFS trace (post-order):
  Node 2 (child): rob=2+0=2, skip=0 → (2, 0)
  Node 3 (right child): rob=3+0=3, skip=0 → (3, 0)
  Node 3 (right leaf 1): rob=1+0=1, skip=0 → (1, 0)
  Node 3 (right non-leaf 3): rob=3+0=3, skip=max(1,0)=1 → (3, 1)

  Root node 3:
    left = (2, 0)   → rob_left=2, skip_left=0
    right = (3, 1)  → rob_right=3, skip_right=1
    rob_this = 3 + skip_left + skip_right = 3+0+1 = 4
    skip_this = max(left) + max(right) = max(2,0) + max(3,1) = 2+3 = 5

  Answer: max(4, 5) = 7 (skip root, rob 2 and 3 and 1)

Wait, let me recalculate... rob_this=3+0+1=4, skip_this=2+3=5, max=5
But 2+3+1=6 or 3+3+1=7... Let me re-examine.

Actually: Node 3 (right side, value=3, child 1):
  rob=3, skip=0 → returns (3, 0)  [rob this = 3, skip = max(3,0)=3]

Root: left=(2,0), right=(3,0)
  rob_this = 3 + 0 + 0 = 3
  skip_this = max(2,0) + max(3,0) = 2+3 = 5
  But wait... right subtree node 3 has child 3 (value 3):
  
Let me redo properly:
  Leaf 3 (left-right): returns (3, 0)
  Node 2: left=(0,0), right=(3,0)
    rob = 2 + 0 + 0 = 2
    skip = 0 + max(3,0) = 3
    returns (2, 3)
  
  Leaf 1 (right-right): returns (1, 0)
  Node 3 (right): left=(0,0), right=(1,0)
    rob = 3 + 0 + 0 = 3
    skip = 0 + max(1,0) = 1
    returns (3, 1)
  
  Root 3: left=(2,3), right=(3,1)
    rob = 3 + 3 + 1 = 7  ← rob root + skip left children + skip right children
    skip = max(2,3) + max(3,1) = 3 + 3 = 6
  
  Answer: max(7, 6) = 7 ✓ (rob root + rob left-right(3) + rob right-left... no)

Actually: rob_root = root.val + left[1] + right[1] = 3 + 3 + 1 = 7
This means: rob root(3), skip left subtree but its best non-rob is 3, 
            skip right subtree but its best non-rob is 1.
Total = 7: 3(root) + 3(left's best-skip = the leaf 3) + 1(right's leaf 1) = 7 ✓
```

```python
def rob_tree(root) -> int:
    def dfs(node):
        if not node:
            return (0, 0)  # (rob_this, not_rob_this)

        left = dfs(node.left)
        right = dfs(node.right)

        # If we rob this node, children MUST be skipped
        rob_this = node.val + left[1] + right[1]
        # If we skip this node, children are free to choose
        not_rob_this = max(left) + max(right)

        return (rob_this, not_rob_this)

    return max(dfs(root))

# Time: O(n), Space: O(h)
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

## Summary Table & Quick Reference

```
┌──────────────────────────┬──────────────────────┬──────────┬───────────────────────────────────────────┐
│ Problem                  │ States               │ Time     │ Key Insight                               │
├──────────────────────────┼──────────────────────┼──────────┼───────────────────────────────────────────┤
│ Diameter                 │ heights              │ O(n)     │ Track top-2 child heights at each node    │
│ Max Path Sum             │ path_through         │ O(n)     │ max(left,0) + node + max(right,0)         │
│ Max Leaf Path Sum        │ leaf_path            │ O(n)     │ Only count paths with both leaf children  │
│ House Robber III         │ take/skip            │ O(n)     │ Take→children skipped; Skip→children free │
│ Vertex Cover             │ cover/skip           │ O(n)     │ cover=1+min(children); skip=sum(covered)  │
│ Max Independent Set      │ take/skip            │ O(n)     │ take=1+skip_children; skip=max(children)  │
│ Path Sum Count           │ prefix sums          │ O(n)     │ Hashmap + backtrack                       │
│ Binary Tree Cameras      │ 0/1/2 (3 states)     │ O(n)     │ Uncovered→place camera; camera→covered    │
│ Delete and Return Forest │ root/non-root        │ O(n)     │ Track if parent was deleted               │
│ Most Frequent Subtree    │ hash + DFS           │ O(n)     │ Sum subtree, count frequencies            │
└──────────────────────────┴──────────────────────┴──────────┴───────────────────────────────────────────┘
```

### The Universal Tree DP Template

```python
# For ANY tree DP problem, follow this skeleton:
def tree_dp(root):
    def dfs(node, parent):
        # Base case: leaf node
        # Initialize states
        
        for child in node.children:
            if child != parent:
                dfs(child, node)           # Post-order: solve children first
                # Combine child's result into current node's states
        
        # Compute this node's dp values from children's results
    
    dfs(root, None)
    return extract_answer(root)
```

### When to Use 2-State vs 3-State

```
2-State (take/skip) covers:
  - Maximum Independent Set
  - House Robber III
  - Vertex Cover (min vertices to cover all edges)

3-State needed when:
  - Binary Tree Cameras (uncovered=0, covered-by-child=1, has-camera=2)
  - Some tree coloring problems
  - State must track MORE than just selection status
```
