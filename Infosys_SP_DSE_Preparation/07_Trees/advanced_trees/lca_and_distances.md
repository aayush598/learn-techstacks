# Lowest Common Ancestor and Distances

## Table of Contents
1. [LCA of Binary Tree](#1-lowest-common-ancestor-of-binary-tree)
2. [LCA of BST](#2-lowest-common-ancestor-of-bst)
3. [Distance Between Two Nodes](#3-distance-between-two-nodes)
4. [Distance from Root to Node](#4-distance-from-root-to-node)
5. [Burning Tree Problem](#5-burning-tree-problem)
6. [All Nodes at Distance K](#6-all-nodes-at-distance-k)

---

## 1. Lowest Common Ancestor of Binary Tree

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def lowest_common_ancestor(root, p, q):
    """Find LCA of nodes p and q in a binary tree.
    
    LCA = deepest node that has both p and q as descendants
    (a node can be a descendant of itself).
    
            3
           / \
          5   1
         / \ / \
        6  2 0  8
          / \
         7   4
    
    LCA(5, 1) = 3
    LCA(5, 4) = 5
    LCA(6, 4) = 5
    """
    if not root:
        return None
    
    # If root is one of p or q, root is the LCA
    if root == p or root == q:
        return root
    
    # Search in left and right subtrees
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    
    # If both sides return non-null, current root is LCA
    if left and right:
        return root
    
    # Otherwise, return whichever side found something
    return left if left else right

# Time: O(n), Space: O(h)
```

### LCA with Parent Pointers

```python
def lca_with_parent(p, q):
    """LCA when each node has a parent pointer.
    
    Approach: Get depth of both nodes, move deeper one up
    until same level, then move both up until they meet.
    """
    def get_depth(node):
        depth = 0
        while node:
            node = node.parent
            depth += 1
        return depth
    
    depth_p = get_depth(p)
    depth_q = get_depth(q)
    
    # Move deeper node up
    while depth_p > depth_q:
        p = p.parent
        depth_p -= 1
    while depth_q > depth_p:
        q = q.parent
        depth_q -= 1
    
    # Move both up until they meet
    while p != q:
        p = p.parent
        q = q.parent
    
    return p

# Time: O(h), Space: O(1)
```

---

## 2. LCA of BST

```python
def lca_bst(root, p, q):
    """LCA using BST property — O(h) without scanning entire tree.
    
    If both p, q < root → LCA is in left subtree
    If both p, q > root → LCA is in right subtree
    Otherwise → root is the LCA (split point)
    """
    current = root
    
    while current:
        if p.val < current.val and q.val < current.val:
            current = current.left
        elif p.val > current.val and q.val > current.val:
            current = current.right
        else:
            return current
    
    return None

# Time: O(h), Space: O(1)
```

### LCA of BST (Recursive)

```python
def lca_bst_recursive(root, p, q):
    """Recursive BST LCA."""
    if p.val < root.val and q.val < root.val:
        return lca_bst_recursive(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lca_bst_recursive(root.right, p, q)
    return root

# Time: O(h), Space: O(h)
```

---

## 3. Distance Between Two Nodes

```python
def distance_between_nodes(root, p, q):
    """Distance = number of edges on path between p and q.
    
    Distance = dist(LCA, p) + dist(LCA, q)
    
    Step 1: Find LCA
    Step 2: Find distance from LCA to p
    Step 3: Find distance from LCA to q
    Step 4: Add them
    """
    
    def find_lca(node, p, q):
        if not node or node == p or node == q:
            return node
        
        left = find_lca(node.left, p, q)
        right = find_lca(node.right, p, q)
        
        if left and right:
            return node
        return left if left else right
    
    def find_distance(node, target, dist):
        """Find distance from node to target."""
        if not node:
            return -1
        
        if node == target:
            return dist
        
        left = find_distance(node.left, target, dist + 1)
        if left != -1:
            return left
        
        return find_distance(node.right, target, dist + 1)
    
    lca = find_lca(root, p, q)
    
    dist_p = find_distance(lca, p, 0)
    dist_q = find_distance(lca, q, 0)
    
    return dist_p + dist_q

# Time: O(n), Space: O(h)
```

### Cleaner One-Pass Distance

```python
def distance_one_pass(root, p, q):
    """Find distance in one pass by computing LCA and depths."""
    
    def dfs(node):
        """Returns (lca, dist_to_p, dist_to_q) or None if neither found."""
        if not node:
            return None, -1, -1
        
        if node == p:
            return node, 0, -1
        if node == q:
            return node, -1, 0
        
        left_lca, left_p, left_q = dfs(node.left)
        if left_lca:
            return left_lca, left_p + 1, left_q + 1
        
        right_lca, right_p, right_q = dfs(node.right)
        if right_lca:
            return right_lca, right_p + 1, right_q + 1
        
        # Both children found something
        if left_p != -1 and right_q != -1:
            return node, left_p + 1, right_q + 1
        if right_p != -1 and left_q != -1:
            return node, right_p + 1, left_q + 1
        
        # Only one child found something
        if left_p != -1:
            return None, left_p + 1, -1
        if left_q != -1:
            return None, -1, left_q + 1
        if right_p != -1:
            return None, right_p + 1, -1
        if right_q != -1:
            return None, -1, right_q + 1
        
        return None, -1, -1
    
    lca, dist_p, dist_q = dfs(root)
    return dist_p + dist_q

# Time: O(n), Space: O(h)
```

---

## 4. Distance from Root to Node

```python
def distance_root_to_node(root, target):
    """Find distance (number of edges) from root to target node."""
    
    def dfs(node, target, dist):
        if not node:
            return -1
        
        if node == target:
            return dist
        
        left = dfs(node.left, target, dist + 1)
        if left != -1:
            return left
        
        return dfs(node.right, target, dist + 1)
    
    return dfs(root, target, 0)

# Time: O(n), Space: O(h)
```

### Finding All Paths from Root

```python
def all_paths_from_root(root, target):
    """Find all paths from root to target nodes."""
    result = []
    
    def dfs(node, path):
        if not node:
            return
        
        path.append(node.val)
        
        if node == target:
            result.append(list(path))
        else:
            dfs(node.left, path)
            dfs(node.right, path)
        
        path.pop()
    
    dfs(root, [])
    return result
```

---

## 5. Burning Tree Problem

```python
from collections import deque, defaultdict

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def time_to_burn_tree(root, target):
    """Given a binary tree and a target node, fire starts at target.
    Fire spreads to adjacent nodes every second.
    Find minimum time to burn the entire tree.
    
    Key Idea:
    1. Create parent pointers (undirected graph)
    2. BFS from target node
    3. Count levels until all nodes burned
    """
    if not root:
        return 0
    
    # Step 1: Build parent map and find target node
    parent = {}
    target_node = None
    node_map = {}  # val → node
    
    def build_graph(node, par=None):
        nonlocal target_node
        if not node:
            return
        
        node_map[node.val] = node
        parent[node.val] = par
        
        if node.val == target:
            target_node = node
        
        build_graph(node.left, node)
        build_graph(node.right, node)
    
    build_graph(root)
    
    # Step 2: BFS from target
    visited = set()
    queue = deque([target_node])
    visited.add(target_node.val)
    time = 0
    
    while queue:
        level_size = len(queue)
        burned_any = False
        
        for _ in range(level_size):
            node = queue.popleft()
            
            # Check all neighbors: left, right, parent
            for neighbor in [node.left, node.right, parent.get(node.val)]:
                if neighbor and neighbor.val not in visited:
                    visited.add(neighbor.val)
                    queue.append(neighbor)
                    burned_any = True
        
        if burned_any:
            time += 1
    
    return time

# Time: O(n), Space: O(n)
```

### Burning Tree — Return Minute-by-Minute

```python
def burning_tree_minutes(root, target):
    """Return list of node values burned at each minute."""
    parent = {}
    target_node = None
    node_map = {}
    
    def build(node, par=None):
        nonlocal target_node
        if not node:
            return
        node_map[node.val] = node
        parent[node.val] = par
        if node.val == target:
            target_node = node
        build(node.left, node)
        build(node.right, node)
    
    build(root)
    
    visited = set()
    queue = deque([target_node])
    visited.add(target_node.val)
    result = []
    
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            
            for neighbor in [node.left, node.right, parent.get(node.val)]:
                if neighbor and neighbor.val not in visited:
                    visited.add(neighbor.val)
                    queue.append(neighbor)
        
        if level:
            result.append(level)
    
    return result

# Time: O(n), Space: O(n)
```

---

## 6. All Nodes at Distance K

```python
from collections import deque, defaultdict

def distance_k(root, target, k):
    """Find all nodes at distance K from target node.
    
            3
           / \
          5   1
         / \ / \
        6  2 0  8
          / \
         7   4
    
    target = 5, K = 2
    Output: [7, 4, 1] (all nodes at distance 2 from node 5)
    """
    if not root:
        return []
    
    # Step 1: Build adjacency list (undirected)
    graph = defaultdict(list)
    
    def build_graph(node, parent=None):
        if not node:
            return
        if parent:
            graph[node.val].append(parent.val)
            graph[parent.val].append(node.val)
        build_graph(node.left, node)
        build_graph(node.right, node)
    
    build_graph(root)
    
    # Step 2: BFS from target
    visited = {target.val}
    queue = deque([target.val])
    
    for _ in range(k):
        next_level = []
        for _ in range(len(queue)):
            node_val = queue.popleft()
            for neighbor in graph[node_val]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
    
    return list(queue)

# Time: O(n), Space: O(n)
```

### Without Building Graph (Recursive)

```python
def distance_k_recursive(root, target, k):
    """Find nodes at distance K without building explicit graph."""
    result = []
    
    def dfs(node):
        """Returns distance from node to target, or -1 if target not in subtree."""
        if not node:
            return -1
        
        if node == target:
            # Target found, now find all nodes at distance k downward
            add_nodes_at_distance(node, k, result)
            return 0
        
        left = dfs(node.left)
        if left != -1:
            # Target is in left subtree at distance left
            if left + 1 == k:
                result.append(node.val)
            else:
                # Search right subtree for (k - left - 2) distance
                add_nodes_at_distance(node.right, k - left - 2, result)
            return left + 1
        
        right = dfs(node.right)
        if right != -1:
            if right + 1 == k:
                result.append(node.val)
            else:
                add_nodes_at_distance(node.left, k - right - 2, result)
            return right + 1
        
        return -1
    
    def add_nodes_at_distance(node, dist, result):
        """Add all nodes at exact distance from node going downward."""
        if not node or dist < 0:
            return
        if dist == 0:
            result.append(node.val)
            return
        add_nodes_at_distance(node.left, dist - 1, result)
        add_nodes_at_distance(node.right, dist - 1, result)
    
    dfs(root)
    return result

# Time: O(n), Space: O(h)
```

---

## Quick Reference Table

| Problem | Approach | Time | Space |
|---------|----------|------|-------|
| LCA (Binary Tree) | Post-order DFS | O(n) | O(h) |
| LCA (BST) | BST property (no scanning) | O(h) | O(1) |
| Distance between nodes | LCA + two BFS | O(n) | O(h) |
| Root to node distance | DFS | O(n) | O(h) |
| Burning tree | Build graph + BFS from target | O(n) | O(n) |
| Nodes at distance K | Graph BFS or recursive DFS | O(n) | O(n) |

**Interview Tips:**
- LCA binary tree: the recursive solution is elegant — if left and right both return non-null, current node is LCA
- LCA BST: always check if you can use BST property — saves time
- Burning tree: always build parent pointers first, then BFS
- Distance K: graph approach is straightforward; recursive approach is more elegant
- For distance problems, LCA is usually the key first step
