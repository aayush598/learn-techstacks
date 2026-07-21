# Dynamic Programming on Trees

## Table of Contents
1. [DP on Trees Concept](#1-dp-on-trees-concept)
2. [House Robber III](#2-house-robber-iii)
3. [Diameter Using Tree DP](#3-diameter-using-tree-dp)
4. [Maximum Independent Set](#4-maximum-independent-set)
5. [Tree Coloring Problem](#5-tree-coloring-problem)
6. [House with Colors Constraint](#6-house-with-colors-constraint)
7. [House Robber with Tree Structure](#7-house-robber-with-tree-structure)
8. [Each Node's Contribution Concept](#8-each-nodes-contribution-concept)

---

## 1. DP on Trees Concept

**Core Idea:** Process nodes in post-order (bottom-up). For each node, compute DP values based on children's DP values.

```
General Pattern:
1. Do DFS (post-order: process children BEFORE parent)
2. For each node, compute dp values from children
3. Return the dp values to parent
4. Global answer is updated at each node
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def tree_dp_template(root):
    """Template for DP on trees."""
    
    def dfs(node):
        # Base case
        if not node:
            return 0  # or appropriate base value
        
        # Recursive case: get children's dp values FIRST
        left_val = dfs(node.left)
        right_val = dfs(node.right)
        
        # Compute current node's dp value
        # ... (depends on problem)
        
        return result  # Return to parent
    
    return dfs(root)
```

**Why Post-Order?**
- Children's values must be known before parent can make decisions
- This is naturally done by post-order DFS (left → right → root)

**Two Approaches:**
1. **Return value from DFS** — simpler, good when each node returns one value
2. **Return tuple/array** — when each node needs to return multiple states

---

## 2. House Robber III

```python
def rob(root):
    """Houses arranged as binary tree. Rob houses such that no two
    adjacent houses (connected by an edge) are robbed.
    
    Maximize total robbed value.
    
            3
           / \
          2   3
           \   \
            3   1
    
    Rob 3 + 3 = 6 (root + left child's right child)
    """
    
    def dfs(node):
        """Returns (max_rob, max_not_rob) for subtree rooted at node.
        
        max_rob: max money if we rob this node
        max_not_rob: max money if we don't rob this node
        """
        if not node:
            return (0, 0)
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        # If we rob this node → can't rob children
        rob_this = node.val + left[1] + right[1]
        
        # If we don't rob this node → take best from children
        not_rob_this = max(left) + max(right)
        
        return (rob_this, not_rob_this)
    
    return max(dfs(root))

# Time: O(n), Space: O(h)
```

### Iterative DP with Memoization

```python
def rob_memo(root):
    """Same problem with explicit memoization."""
    memo = {}
    
    def dfs(node):
        if not node:
            return 0
        
        if id(node) in memo:
            return memo[id(node)]
        
        # Option 1: Rob this node
        rob_this = node.val
        if node.left:
            rob_this += dfs(node.left.left) + dfs(node.left.right)
        if node.right:
            rob_this += dfs(node.right.left) + dfs(node.right.right)
        
        # Option 2: Don't rob this node
        not_rob_this = dfs(node.left) + dfs(node.right)
        
        memo[id(node)] = max(rob_this, not_rob_this)
        return memo[id(node)]
    
    return dfs(root)

# Time: O(n), Space: O(h + n) for memo
```

---

## 3. Diameter Using Tree DP

```python
def diameter_of_binary_tree(root):
    """Diameter = longest path between any two nodes (in edges).
    
    Tree DP approach: for each node, compute:
    - longest path through this node (left_depth + right_depth)
    - return max depth to parent
    """
    result = [0]
    
    def depth(node):
        if not node:
            return 0
        
        left = depth(node.left)
        right = depth(node.right)
        
        # Update diameter: path through this node
        result[0] = max(result[0], left + right)
        
        # Return depth to parent
        return 1 + max(left, right)
    
    depth(root)
    return result[0]

# Time: O(n), Space: O(h)
```

### Returning Both Depth and Diameter

```python
def diameter_return_pair(root):
    """Return (depth, diameter) from each node.
    
    This avoids using global variable.
    """
    
    def dfs(node):
        """Returns (depth, diameter) for subtree."""
        if not node:
            return (0, 0)
        
        left_depth, left_diam = dfs(node.left)
        right_depth, right_diam = dfs(node.right)
        
        # Depth of this subtree
        depth = 1 + max(left_depth, right_depth)
        
        # Diameter: either through this node or in a child's subtree
        through_node = left_depth + right_depth
        diameter = max(through_node, left_diam, right_diam)
        
        return (depth, diameter)
    
    return dfs(root)[1]

# Time: O(n), Space: O(h)
```

---

## 4. Maximum Independent Set

```python
def max_independent_set(root):
    """Maximum weight independent set in a tree.
    
    Independent set: no two selected nodes are adjacent.
    Maximize sum of selected node values.
    
    Generalization of House Robber III (node values can be negative).
    
            1
           / \
          2   3
         / \   \
        4   5   6
    
    Weights = [1, 2, 3, 4, 5, 6]
    Max independent set = {4, 5, 3, 6} = 18 or {1, 4, 5, 6} = 16
    Actually: {2, 3} → sum = 5, {4, 5, 6} → sum = 15, {1, 4, 5, 6} → sum = 16
    Correct: {4, 5, 3, 6} = 18 ✓
    """
    
    def dfs(node):
        """Returns (include, exclude) for subtree rooted at node.
        
        include: max sum if node is included
        exclude: max sum if node is excluded
        """
        if not node:
            return (0, 0)
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        # Include this node → can't include children
        include = node.val + left[1] + right[1]
        
        # Exclude this node → take best from children
        exclude = max(left) + max(right)
        
        return (include, exclude)
    
    return max(dfs(root))

# Time: O(n), Space: O(h)
```

---

## 5. Tree Coloring Problem

```python
def min_coloring(root):
    """Color tree nodes such that no two adjacent nodes have same color.
    Each color has a cost. Find minimum total cost.
    
    Classic 3-color problem:
    costs = [1, 2, 3]  # cost of red, green, blue
    
            1
           / \
          2   3
    
    Node 1 colored red (cost 1), nodes 2,3 colored green,blue (costs 2+3=5)
    Total = 6
    """
    
    def dfs(node):
        """Returns minimum cost for subtree at each node.
        Returns (cost_red, cost_green, cost_blue)."""
        if not node:
            return (0, 0, 0)
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        # Cost if current node is RED (can't be red for children)
        red = 1 + min(left[1], left[2]) + min(right[1], right[2])
        
        # Cost if current node is GREEN
        green = 2 + min(left[0], left[2]) + min(right[0], right[2])
        
        # Cost if current node is BLUE
        blue = 3 + min(left[0], left[1]) + min(right[0], right[1])
        
        return (red, green, blue)
    
    return min(dfs(root))

# Time: O(n), Space: O(h)
```

### General K-Coloring

```python
def min_k_coloring(root, costs):
    """General k-coloring with given costs.
    
    costs[i] = cost of using color i
    """
    
    def dfs(node):
        if not node:
            return [0] * len(costs)
        
        child_costs = dfs(node.left) if node.left else [0] * len(costs)
        right_costs = dfs(node.right) if node.right else [0] * len(costs)
        
        my_costs = [0] * len(costs)
        
        for c in range(len(costs)):
            # Cost if I use color c
            min_left = min(child_costs[j] for j in range(len(costs)) if j != c)
            min_right = min(right_costs[j] for j in range(len(costs)) if j != c)
            my_costs[c] = costs[c] + min_left + min_right
        
        return my_costs
    
    return min(dfs(root))

# Time: O(n * k^2), Space: O(h * k)
```

---

## 6. House with Colors Constraint

```python
def min_cost_paint(root, costs):
    """Paint houses (tree nodes) such that no adjacent nodes have same color.
    
    costs[node][color] = cost of painting node with color.
    
    Generalization of coloring problem with custom costs per node.
    
    costs = [[1, 5, 3],   # node 0: red=1, green=5, blue=3
             [2, 7, 4],   # node 1: red=2, green=7, blue=4
             [3, 3, 1]]   # node 2: red=3, green=3, blue=1
    
    Tree: 0 → [1, 2]
    """
    num_colors = len(costs[0])
    
    def dfs(node):
        """Returns list of min costs for each color at this node."""
        if not node:
            return [0] * num_colors
        
        left = dfs(node.left) if node.left else [0] * num_colors
        right = dfs(node.right) if node.right else [0] * num_colors
        
        result = [0] * num_colors
        
        for c in range(num_colors):
            # Min cost from left child not using color c
            min_left = min(left[j] for j in range(num_colors) if j != c)
            min_right = min(right[j] for j in range(num_colors) if j != c)
            result[c] = costs[node.val][c] + min_left + min_right
        
        return result
    
    return min(dfs(root))

# Time: O(n * k^2), Space: O(h)
```

---

## 7. House Robber with Tree Structure

```python
def rob_optimized(root):
    """House Robber III — optimized without tuple return.
    
    Uses post-order DFS with (rob, skip) pair.
    """
    
    def dfs(node):
        """Returns (max_if_robbed, max_if_skipped)."""
        if not node:
            return (0, 0)
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        # Rob this node: skip children
        rob = node.val + left[1] + right[1]
        
        # Skip this node: take max from each child
        skip = max(left) + max(right)
        
        return (rob, skip)
    
    return max(dfs(root))

# Time: O(n), Space: O(h)
```

### With Path Reconstruction

```python
def rob_with_path(root):
    """Return max money and which nodes to rob."""
    
    def dfs(node):
        if not node:
            return (0, [])
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        # Rob this node
        rob_val = node.val + left[1] + right[1]
        rob_path = [node.val] + left[1] + right[1] if isinstance(left[1], list) else [node.val]
        
        # Skip this node
        skip_val = max(left[0], 0) + max(right[0], 0)
        
        # Actually, let's simplify:
        left_rob, left_skip = dfs(node.left) if node.left else (0, 0)
        right_rob, right_skip = dfs(node.right) if node.right else (0, 0)
        
        rob = node.val + left_skip + right_skip
        skip = max(left_rob, left_skip) + max(right_rob, right_skip)
        
        return (rob, skip)
    
    return max(dfs(root))

# Time: O(n), Space: O(h)
```

---

## 8. Each Node's Contribution Concept

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_path_sum(root):
    """Each node's contribution = its value + max(left_contribution, 0) + max(right_contribution, 0).
    
    This is the fundamental pattern for tree DP problems:
    "What is this node's best answer considering only its subtree?"
    
    The global answer is updated at each node.
    """
    max_sum = float('-inf')
    
    def contribution(node):
        """Return max sum of path going DOWN from this node.
        (This node + best left path + best right path, each >= 0)."""
        nonlocal max_sum
        
        if not node:
            return 0
        
        # Get contributions from children (ignore negative)
        left = max(contribution(node.left), 0)
        right = max(contribution(node.right), 0)
        
        # Path through this node (for global answer)
        path_through = node.val + left + right
        max_sum = max(max_sum, path_through)
        
        # Return contribution to parent (single path downward)
        return node.val + max(left, right)
    
    contribution(root)
    return max_sum

# Time: O(n), Space: O(h)
```

### Pattern: Count of Specific Structures

```python
def count_paths_with_sum(root, target):
    """Count paths where sum equals target (using contribution pattern)."""
    prefix = {0: 1}
    
    def dfs(node, curr_sum):
        if not node:
            return 0
        
        curr_sum += node.val
        count = prefix.get(curr_sum - target, 0)
        
        prefix[curr_sum] = prefix.get(curr_sum, 0) + 1
        
        count += dfs(node.left, curr_sum)
        count += dfs(node.right, curr_sum)
        
        prefix[curr_sum] -= 1
        if prefix[curr_sum] == 0:
            del prefix[curr_sum]
        
        return count
    
    return dfs(root, 0)
```

### Pattern: Ancestor DP

```python
def count_good_nodes(root):
    """Count "good" nodes: node is good if no ancestor has greater value.
    
    Pass max-so-far DOWN the tree (not returning from children).
    """
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

# Time: O(n), Space: O(h)
```

### Pattern: Merge Children Results

```python
def max_width(root):
    """Maximum width of binary tree.
    
    Width = max number of nodes at any level.
    Uses BFS but demonstrates "merge children" pattern.
    """
    if not root:
        return 0
    
    from collections import deque
    
    queue = deque([(root, 0)])
    max_width = 0
    
    while queue:
        level_size = len(queue)
        _, first_idx = queue[0]
        
        for _ in range(level_size):
            node, idx = queue.popleft()
            
            if node.left:
                queue.append((node.left, 2 * idx))
            if node.right:
                queue.append((node.right, 2 * idx + 1))
        
        max_width = max(max_width, level_size)
    
    return max_width
```

---

## Summary: Tree DP Patterns

| Pattern | What to Return | When to Use |
|---------|---------------|-------------|
| **Single value** | `dp[node]` | Simple problems (depth, diameter) |
| **Include/Exclude** | `(include, exclude)` | Independent set, house robber |
| **Multi-color** | `(cost_c1, cost_c2, ...)` | Coloring, painting problems |
| **Contribution** | `max_downward_path` | Path sum, max path problems |
| **Ancestor info** | Value passed DOWN | Good nodes, range queries |

**Decision Framework:**
1. What decisions does each node make? → determines return tuple size
2. What info from children is needed? → determines DFS structure
3. Is answer at node or global? → determines if we return or use nonlocal
4. Can path go up through parent? → determines if we use contribution pattern

**Time/Space for all tree DP:**
- Time: O(n) — visit each node once
- Space: O(h) — recursion stack (h = height)
