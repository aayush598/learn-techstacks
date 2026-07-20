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

## 1. Path Sum I

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

**Interview Tips:**
- Path Sum III prefix sum trick is the same as subarray sum = k
- Max Path Sum: every node is a potential "peak" — calculate contribution at each node
- Diameter: same pattern as max path sum but simpler
- Path via LCA: two-step — find LCA, then find paths from LCA to each node
- Always clarify: can paths go through any node or only root-to-leaf?
