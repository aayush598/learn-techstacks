# Tree Path Problems

## Table of Contents
1. [Path Sum I](#1-path-sum-i)
2. [Path Sum II](#2-path-sum-ii)
3. [Path Sum III](#3-path-sum-iii)
4. [Binary Tree Maximum Path Sum](#4-binary-tree-maximum-path-sum)
5. [Diameter of Binary Tree](#5-diameter-of-binary-tree)
6. [Root to Leaf Paths](#6-root-to-leaf-paths)
7. [Path from Node to Node via LCA](#7-path-from-node-to-node-via-lca)
8. [Longest Consecutive Sequence](#8-longest-consecutive-sequence)

---

## Path Problem Taxonomy

```
Not all path problems are the same! Understand the constraints:

╔══════════════════════════════════════════════════════════════════════════╗
║  Path type          │ Constraint                                       ║
║ ────────────────────┼────────────────────────────────────────────────── ║
║  Root-to-leaf       │ Must start at root, end at leaf                  ║
║  Any-to-any         │ Can start and end at any node                   ║
║  Downward only      │ Must go parent → child (no going up)            ║
║  Through any node   │ Can pass through any node (like a road)         ║
╚══════════════════════════════════════════════════════════════════════════╝

Quick identification:
  "root to leaf sum"     → Path Sum I/II (DFS with remaining sum)
  "any path sum"         → Path Sum III (prefix sum trick)
  "max path sum"         → Max Path Sum (contribution pattern)
  "longest path"         → Diameter (depth of left + right)
  "consecutive"          → Longest Consecutive (DFS with parent tracking)
```

---

## 1. Path Sum I

### Concept Walkthrough

**Does any root-to-leaf path sum equal targetSum?**

```
            5
           / \
          4   8
         /   / \
        11  13  4
       / \       \
      7   2       1

targetSum = 22

Path 1: 5 → 4 → 11 → 7 = 27 ✗
Path 2: 5 → 4 → 11 → 2 = 22 ✓ ← FOUND!
Path 3: 5 → 8 → 13 = 26 ✗
Path 4: 5 → 8 → 4 → 1 = 18 ✗
```

### DFS with Remaining Sum

```
At each node, subtract node value from remaining sum.
At leaf, check if remaining sum equals leaf value.

Start: remaining = 22

5: remaining = 22 - 5 = 17
  4: remaining = 17 - 4 = 13
    11: remaining = 13 - 11 = 2
      7: leaf! 7 == 2? No ✗
      2: leaf! 2 == 2? Yes ✓ → return True

Answer: True
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def has_path_sum(root, target_sum):
    """Does any root-to-leaf path sum equal targetSum?
    
    Path must go from root to a LEAF (no intermediate nodes).
    
            5
           / \
          4   8
         /   / \
        11  13  4
       / \       \
      7   2       1
    
    targetSum = 22 → True (5→4→11→2 = 22)
    """
    if not root:
        return False
    
    # Leaf node — check if remaining sum equals leaf value
    if not root.left and not root.right:
        return root.val == target_sum
    
    remaining = target_sum - root.val
    return (has_path_sum(root.left, remaining) or
            has_path_sum(root.right, remaining))

# Time: O(n), Space: O(h)
```

---

## 2. Path Sum II

```python
def path_sum_ii(root, target_sum):
    """Find ALL root-to-leaf paths that sum to targetSum.
    
    Return list of paths, each path is a list of node values.
    
            5
           / \
          4   8
         /   / \
        11  13  4
       / \       \
      7   2       1
    
    targetSum = 22 → [[5, 4, 11, 2]]
    """
    result = []
    
    def dfs(node, remaining, path):
        if not node:
            return
        
        path.append(node.val)
        
        # Leaf node — check sum
        if not node.left and not node.right:
            if remaining == node.val:
                result.append(path[:])  # Copy the path
            path.pop()
            return
        
        dfs(node.left, remaining - node.val, path)
        dfs(node.right, remaining - node.val, path)
        
        path.pop()  # Backtrack
    
    dfs(root, target_sum, [])
    return result

# Time: O(n^2) worst case — copying paths
# Space: O(n) for path + O(h) for recursion
```

---

## 3. Path Sum III

### Concept: The Prefix Sum Trick

**Paths can start and end at ANY node (not just root/leaf). Must go downward.**

```
This is the same as "Subarray Sum Equals K" but on a tree!

Array version:  [1, 2, 3] → prefix_sum[i] - prefix_sum[j] = target
Tree version:   root-to-node sum - some ancestor sum = target

prefix_sum = running sum from root to current node
If (prefix_sum - target) was seen before, we found a valid path!
```

### Visual Walkthrough

```
            10
           /  \
          5   -3
         / \    \
        3   2   11
       / \   \
      3  -2   1

targetSum = 8

DFS traversal with prefix sums:
─────────────────────────────────────────────────
Node 10: prefix = 10
  needed = 10 - 8 = 2 → not in prefix_sums → count = 0
  prefix_sums = {0:1, 10:1}

Node 5: prefix = 10+5 = 15
  needed = 15 - 8 = 7 → not in prefix_sums → count = 0
  prefix_sums = {0:1, 10:1, 15:1}

Node 3: prefix = 15+3 = 18
  needed = 18 - 8 = 10 → 10 is in prefix_sums! count = 1
  (Path: 5 → 3, sum = 8) ✓
  prefix_sums = {0:1, 10:1, 15:1, 18:1}

Node 3: prefix = 18+3 = 21
  needed = 21 - 8 = 13 → not found → count = 0
  prefix_sums = {0:1, 10:1, 15:1, 18:1, 21:1}
  Backtrack: remove 21

Node -2: prefix = 18+(-2) = 16
  needed = 16 - 8 = 8 → not found → count = 0
  Backtrack: remove 16

Node 2: prefix = 15+2 = 17
  needed = 17 - 8 = 9 → not found → count = 0

Node 1: prefix = 17+1 = 18
  needed = 18 - 8 = 10 → 10 is in prefix_sums! count = 1
  (Path: 5 → 2 → 1, sum = 8) ✓

Node -3: prefix = 10+(-3) = 7
  needed = 7 - 8 = -1 → not found → count = 0

Node 11: prefix = 7+11 = 18
  needed = 18 - 8 = 10 → 10 is in prefix_sums! count = 1
  (Path: -3 → 11, sum = 8) ✓

Total count = 3 paths: [5,3], [5,2,1], [-3,11]
─────────────────────────────────────────────────
```

### Why Backtracking Is Essential

```
Without backtracking: prefix_sums keeps ALL ancestors' sums
With backtracking: only sums from root-to-current path

Without backtracking (WRONG):
  After visiting left subtree of 10, prefix_sums has sums from left.
  When visiting right subtree, those left subtree sums are still there.
  This would count paths through the left subtree from the right subtree,
  which is NOT valid (paths must go downward).

With backtracking (CORRECT):
  When we return from a subtree, we remove its prefix sums.
  This ensures only ancestor sums remain in the map.
```

```python
def path_sum_iii(root, target_sum):
    """Count paths (any start, any end) that sum to targetSum.
    
    Paths can start and end at ANY node (not just root/leaf).
    Paths must go downward (parent to child).
    
            10
           /  \
          5   -3
         / \    \
        3   2   11
       / \   \
      3  -2   1
    
    targetSum = 8 → 3 paths: [5,3], [5,2,1], [-3,11]
    """
    def dfs(node, target):
        """Count paths starting from this node going downward."""
        if not node:
            return 0
        
        count = 0
        if node.val == target:
            count += 1
        
        count += dfs(node.left, target - node.val)
        count += dfs(node.right, target - node.val)
        
        return count
    
    if not root:
        return 0
    
    # Paths starting from root + paths in left subtree + paths in right subtree
    return (dfs(root, target_sum) +
            path_sum_iii(root.left, target_sum) +
            path_sum_iii(root.right, target_sum))

# Time: O(n^2) worst case, Space: O(h)
```

### Optimized with Prefix Sum (O(n))

```python
def path_sum_iii_optimized(root, target_sum):
    """Prefix sum approach — like subarray sum equals k.
    
    prefix_sum: running sum from root to current node
    needed: prefix_sum - target_sum
    
    If needed exists in prefix_sums, we found a valid path.
    """
    prefix_sums = {0: 1}  # {prefix_sum: count}
    
    def dfs(node, curr_sum):
        if not node:
            return 0
        
        curr_sum += node.val
        needed = curr_sum - target_sum
        
        count = prefix_sums.get(needed, 0)
        
        # Add current prefix sum
        prefix_sums[curr_sum] = prefix_sums.get(curr_sum, 0) + 1
        
        # Recurse
        count += dfs(node.left, curr_sum)
        count += dfs(node.right, curr_sum)
        
        # Backtrack: remove current prefix sum
        prefix_sums[curr_sum] -= 1
        if prefix_sums[curr_sum] == 0:
            del prefix_sums[curr_sum]
        
        return count
    
    return dfs(root, 0)

# Time: O(n), Space: O(h) for recursion + O(n) for hashmap
```

---

## 4. Binary Tree Maximum Path Sum

### The Two Calculations Pattern

**Each node calculates TWO different things:**

```
            1
           / \
          2   3

At node 2:
  1. Path THROUGH this node (can go both left and right):
     2 + 0 + 0 = 2  (no children contribute positively)
     → This is a CANDIDATE for global max

  2. Max gain going DOWNWARD (for parent's use):
     2 + max(0, 0) = 2
     → Parent can only extend ONE direction

At node 1:
  1. Path through 1: 1 + max(2,0) + max(3,0) = 1 + 2 + 3 = 6
     → global_max = 6 ✓

  2. Max gain going downward: 1 + max(2, 3) = 4
     → Not used (root has no parent)
```

### Visual Walkthrough

```
         -10
         /  \
        9   20
           /  \
          15   7

Node 9:  left_gain=0, right_gain=0
  path_through = 9 + 0 + 0 = 9
  max_sum = 9
  return 9 (contribution to parent)

Node 15: left_gain=0, right_gain=0
  path_through = 15 + 0 + 0 = 15
  max_sum = 15
  return 15

Node 7: left_gain=0, right_gain=0
  path_through = 7 + 0 + 0 = 7
  max_sum = 15 (unchanged)
  return 7

Node 20: left_gain=15, right_gain=7
  path_through = 20 + 15 + 7 = 42
  max_sum = 42 ✓ ← THE ANSWER!
  return 20 + max(15, 7) = 35

Node -10: left_gain=9, right_gain=35
  path_through = -10 + 9 + 35 = 34
  max_sum = 42 (unchanged)
  return -10 + max(9, 35) = 25

Final answer: 42 (path: 15 → 20 → 7)
```

**Key Insight:** Each node calculates two things:
1. **Path through this node** (for global answer): `node + left_gain + right_gain`
2. **Max gain downward** (for parent): `node + max(left, right)`

```python
def max_path_sum(root):
    """Maximum path sum where path can start and end at ANY node.
    
    Path can go through any node (not necessarily root or leaf).
    
            1
           / \
          2   3
    
    Max path sum = 6 (2 → 1 → 3)
    
            -10
            /  \
           9   20
              /  \
             15   7
    
    Max path sum = 42 (15 → 20 → 7)
    """
    max_sum = [float('-inf')]
    
    def max_gain(node):
        """Return max gain from this node going DOWNWARD.
        Also update global max_sum for paths through this node."""
        if not node:
            return 0
        
        # Max gain from left and right (ignore negative contributions)
        left_gain = max(max_gain(node.left), 0)
        right_gain = max(max_gain(node.right), 0)
        
        # Path through this node as the "peak"
        path_through_node = node.val + left_gain + right_gain
        max_sum[0] = max(max_sum[0], path_through_node)
        
        # Return max gain going downward (for parent's calculation)
        return node.val + max(left_gain, right_gain)
    
    max_gain(root)
    return max_sum[0]

# Time: O(n), Space: O(h)
```

**Key Insight:** Each node calculates two things:
1. **Path through this node** (for global answer): `node + left_gain + right_gain`
2. **Max gain downward** (for parent): `node + max(left, right)`

---

## 5. Diameter of Binary Tree

### Concept

**Longest path between any two nodes (number of edges).**

```
            1
           / \
          2   3
         / \
        4   5

Possible paths:
  4 → 2 → 1 → 3  (3 edges) ← LONGEST
  5 → 2 → 1 → 3  (3 edges) ← also longest
  4 → 2 → 5      (2 edges)
  1 → 2 → 4      (2 edges)

Diameter = 3
```

### Same Pattern as Max Path Sum

```
At each node:
  diameter_through_node = left_depth + right_depth

At node 2:
  left_depth = 1 (node 4)
  right_depth = 1 (node 5)
  diameter = 1 + 1 = 2

At node 1:
  left_depth = 2 (2→4 or 2→5)
  right_depth = 1 (node 3)
  diameter = 2 + 1 = 3 ← ANSWER!

The diameter may or may not pass through root!
We track the GLOBAL max at every node.
```

```python
def diameter_of_binary_tree(root):
    """Longest path between any two nodes (number of edges).
    
    The longest path may or may not pass through the root.
    
            1
           / \
          2   3
         / \
        4   5
    
    Diameter = 3 (path: 4 → 2 → 1 → 3, or 5 → 2 → 1 → 3)
    """
    max_diameter = [0]
    
    def depth(node):
        """Return depth of tree rooted at node.
        Update max_diameter as a side effect."""
        if not node:
            return 0
        
        left_depth = depth(node.left)
        right_depth = depth(node.right)
        
        # Diameter through this node
        max_diameter[0] = max(max_diameter[0], left_depth + right_depth)
        
        return 1 + max(left_depth, right_depth)
    
    depth(root)
    return max_diameter[0]

# Time: O(n), Space: O(h)
```

### Variant: Diameter of N-ary Tree

```python
def diameter_nary_tree(root):
    """Diameter of N-ary tree — longest path through any node."""
    max_diameter = [0]
    
    def depth(node):
        if not node:
            return 0
        
        # Get depths of all children
        depths = []
        for child in node.children:
            depths.append(depth(child))
        
        # Top two deepest children
        depths.sort(reverse=True)
        
        if len(depths) >= 2:
            max_diameter[0] = max(max_diameter[0], depths[0] + depths[1])
        
        return 1 + (depths[0] if depths else 0)
    
    depth(root)
    return max_diameter[0]
```

---

## 6. Root to Leaf Paths

```python
def binary_tree_paths(root):
    """Return all root-to-leaf paths as strings.
    
            1
           / \
          2   3
         \
          5
    
    Output: ["1->2->5", "1->3"]
    """
    result = []
    
    def dfs(node, path):
        if not node:
            return
        
        path.append(str(node.val))
        
        if not node.left and not node.right:
            result.append("->".join(path))
        else:
            dfs(node.left, path)
            dfs(node.right, path)
        
        path.pop()
    
    dfs(root, [])
    return result

# Time: O(n^2) — building strings, Space: O(n)
```

### Root to Leaf Paths as Lists

```python
def all_root_to_leaf_paths(root):
    """Return all root-to-leaf paths as lists."""
    result = []
    
    def dfs(node, path):
        if not node:
            return
        
        path.append(node.val)
        
        if not node.left and not node.right:
            result.append(list(path))
        else:
            dfs(node.left, path)
            dfs(node.right, path)
        
        path.pop()
    
    dfs(root, [])
    return result
```

---

## 7. Path from Node to Node via LCA

```python
def path_between_nodes(root, p, q):
    """Find path between two nodes using LCA.
    
    Step 1: Find LCA
    Step 2: Find path from LCA to p
    Step 3: Find path from LCA to q
    Step 4: Combine: reverse(p_path) + q_path[1:]
    """
    
    def find_lca(node, p, q):
        if not node or node == p or node == q:
            return node
        
        left = find_lca(node.left, p, q)
        right = find_lca(node.right, p, q)
        
        if left and right:
            return node
        return left if left else right
    
    def find_path(node, target, path):
        if not node:
            return False
        
        path.append(node.val)
        
        if node == target:
            return True
        
        if find_path(node.left, target, path) or find_path(node.right, target, path):
            return True
        
        path.pop()
        return False
    
    lca = find_lca(root, p, q)
    
    path_to_p = []
    path_to_q = []
    
    find_path(lca, p, path_to_p)
    find_path(lca, q, path_to_q)
    
    # Combine paths: reverse path_to_p + path_to_q (skip LCA in one)
    return path_to_p[::-1] + path_to_q[1:]

# Time: O(n), Space: O(h)
```

---

## 8. Longest Consecutive Sequence

```python
def longest_consecutive(root):
    """Find longest consecutive sequence in binary tree.
    
    Sequence must follow parent → child relationship with diff = 1.
    
            1
             \
              3
             / \
            2   4
             \
              5
    
    Longest consecutive sequence: 2 → 3 → 4 (length 3)
    """
    max_length = [0]
    
    def dfs(node, parent_val, current_length):
        if not node:
            return
        
        if parent_val is not None and node.val == parent_val + 1:
            current_length += 1
        else:
            current_length = 1
        
        max_length[0] = max(max_length[0], current_length)
        
        dfs(node.left, node.val, current_length)
        dfs(node.right, node.val, current_length)
    
    dfs(root, None, 0)
    return max_length[0]

# Time: O(n), Space: O(h)
```

### Variant: Longest Consecutive Sequence (Any Direction)

```python
def longest_consecutive_v2(root):
    """Consecutive sequence can go up or down (diff = ±1).
    
    For each node, track both increasing and decreasing paths.
    """
    max_length = [0]
    
    def dfs(node):
        """Returns (inc_length, dec_length) from this node."""
        if not node:
            return (0, 0)
        
        left_inc, left_dec = dfs(node.left)
        right_inc, right_dec = dfs(node.right)
        
        # Increasing path (node is smallest)
        inc = 1
        if node.left and node.val + 1 == node.left.val:
            inc = max(inc, 1 + left_inc)
        if node.right and node.val + 1 == node.right.val:
            inc = max(inc, 1 + right_inc)
        
        # Decreasing path (node is largest)
        dec = 1
        if node.left and node.val - 1 == node.left.val:
            dec = max(dec, 1 + left_dec)
        if node.right and node.val - 1 == node.right.val:
            dec = max(dec, 1 + right_dec)
        
        max_length[0] = max(max_length[0], inc, dec)
        
        return (inc, dec)
    
    dfs(root)
    return max_length[0]

# Time: O(n), Space: O(h)
```

---

## Quick Reference Table

| Problem | Key Idea | Time | Space |
|---------|----------|------|-------|
| Path Sum I | DFS with remaining sum | O(n) | O(h) |
| Path Sum II | DFS + backtrack | O(n^2) | O(n) |
| Path Sum III | Prefix sum / hashmap | O(n) | O(n) |
| Max Path Sum | Node contribution + global max | O(n) | O(h) |
| Diameter | Depth of left + right at each node | O(n) | O(h) |
| Root to Leaf Paths | DFS + backtrack | O(n^2) | O(n) |
| Path via LCA | Find LCA + find paths | O(n) | O(h) |
| Longest Consecutive | DFS with parent tracking | O(n) | O(h) |

### Problem Identification Guide

```
╔══════════════════════════════════════════════════════════════════════════╗
║  "root to leaf" + "sum"     → Path Sum I/II (DFS with subtraction)    ║
║  "any path" + "sum"         → Path Sum III (prefix sum)               ║
║  "max path sum"             → Max Path Sum (contribution pattern)     ║
║  "longest path" / "diameter"→ Diameter (depth of left + right)        ║
║  "all root-to-leaf paths"   → DFS + backtracking                      ║
║  "path between two nodes"   → LCA + find paths from LCA               ║
║  "consecutive sequence"     → DFS with parent value tracking          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Common Patterns

1. **Subtract from target** — Path Sum I/II: pass remaining sum down
2. **Prefix sum** — Path Sum III: same as subarray sum = k on arrays
3. **Two calculations** — Max Path Sum: path-through-node AND downward-gain
4. **Backtracking** — Path Sum II/Root-to-Leaf: build path, pop on return
5. **Global variable** — Diameter/Max Path Sum: update max at each node

**Interview Tips:**
- Path Sum III prefix sum trick is the same as subarray sum = k
- Max Path Sum: every node is a potential "peak" — calculate contribution at each node
- Diameter: same pattern as max path sum but simpler
- Path via LCA: two-step — find LCA, then find paths from LCA to each node
- Always clarify: can paths go through any node or only root-to-leaf?
