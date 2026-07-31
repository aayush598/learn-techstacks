# Lowest Common Ancestor and Distances

## Table of Contents
1. [LCA of Binary Tree](#1-lowest-common-ancestor-of-binary-tree)
2. [LCA of BST](#2-lowest-common-ancestor-of-bst)
3. [Distance Between Two Nodes](#3-distance-between-two-nodes)
4. [Distance from Root to Node](#4-distance-from-root-to-node)
5. [Burning Tree Problem](#5-burning-tree-problem)
6. [All Nodes at Distance K](#6-all-nodes-at-distance-k)

---

## When to Use LCA Patterns

```
╔══════════════════════════════════════════════════════════════════════════╗
║  "distance between two nodes"  → Find LCA, then distance from LCA    ║
║  "common ancestor" / "LCA"     → Recursive DFS (post-order)          ║
║  "LCA in BST"                  → BST property (O(h), no full scan)   ║
║  "burn tree" / "fire spreads"  → Build parent pointers + BFS          ║
║  "nodes at distance K"         → Graph BFS or recursive DFS           ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 1. Lowest Common Ancestor of Binary Tree

### What is LCA?

```
LCA = Lowest (deepest) Common Ancestor of two nodes

            3
           / \
          5   1
         / \ / \
        6  2 0  8
          / \
         7   4

LCA(5, 1) = 3    ← Both are in different subtrees of 3
LCA(5, 4) = 5    ← 5 is ancestor of 4 (a node can be its own ancestor)
LCA(6, 4) = 5    ← Both are in left subtree of 5
LCA(7, 8) = 3    ← 7 is in left subtree, 8 is in right subtree of 3
```

### The Elegant Recursive Insight

```
At each node, we ask: "Are p or q in my left subtree? Right subtree?"

Three cases:
┌─────────────────────────────────────────────────────────────────┐
│ Case 1: p is in LEFT, q is in RIGHT (or vice versa)           │
│   → CURRENT node is the LCA!                                   │
│                                                                 │
│ Case 2: Both p and q are in LEFT subtree                       │
│   → LCA is in the left subtree (keep searching left)           │
│                                                                 │
│ Case 3: Both p and q are in RIGHT subtree                      │
│   → LCA is in the right subtree (keep searching right)         │
│                                                                 │
│ Case 4: Neither p nor q found                                  │
│   → Return None                                                 │
│                                                                 │
│ Special: If current node IS p or q, it might be the LCA        │
│   → Return itself (p or q found in this subtree)               │
└─────────────────────────────────────────────────────────────────┘
```

### Visual Walkthrough: LCA(6, 4)

```
            3
           / \
          5   1
         / \ / \
        6  2 0  8
          / \
         7   4

Step 1: dfs(3)
  → dfs(5)
    → dfs(6): found 6! return node(6)
    → dfs(2)
      → dfs(7): not found, return None
      → dfs(4): found 4! return node(4)
    → left=6, right=4 → BOTH non-null → return node(5) as LCA!
  → left=node(5), right=None (nothing found in right subtree)
  → return node(5)

Answer: LCA(6, 4) = 5 ✓
```

### Visual Walkthrough: LCA(6, 7)

```
            3
           / \
          5   1
         / \ / \
        6  2 0  8
          / \
         7   4

Step 1: dfs(3)
  → dfs(5)
    → dfs(6): found 6! return node(6)
    → dfs(2)
      → dfs(7): found 7! return node(7)
      → dfs(4): not found, return None
    → left=6, right=7 → BOTH non-null → return node(5) as LCA!
  → left=node(5), right=None
  → return node(5)

Answer: LCA(6, 7) = 5 ✓
Note: LCA is 5, not 2, because 2 is NOT an ancestor of 6.
      LCA must be a TRUE ancestor of both nodes.
```

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

### Why BST LCA is Faster

```
BST Property:  left < root < right  (for ALL nodes)

This means we can use VALUE COMPARISON instead of searching the whole tree!

            6
           / \
          2   8
         / \ / \
        0  4 7  9
          / \
         3   5

LCA(2, 4) in BST:
  Start at 6:  Both 2 and 4 < 6 → go LEFT
  Start at 2:  2 == 2 (match!) and 4 > 2 → SPLIT POINT!
  Answer: 2

LCA(0, 7) in BST:
  Start at 6:  0 < 6 and 7 > 6 → SPLIT POINT!
  Answer: 6

Key insight: We go LEFT only if BOTH values are smaller.
            We go RIGHT only if BOTH values are larger.
            Otherwise, we've found the LCA!
```

### Decision Flow

```
              ┌────────────────┐
              │  Start at root │
              └───────┬────────┘
                      │
         ┌────────────▼────────────┐
         │  p < root AND q < root?  │──Yes──► Go LEFT
         └────────────┬────────────┘
                      │ No
         ┌────────────▼────────────┐
         │  p > root AND q > root?  │──Yes──► Go RIGHT
         └────────────┬────────────┘
                      │ No
                      ▼
              root is the LCA!
        (p and q split here)
```

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

### Key Formula

```
Distance(p, q) = Distance(LCA, p) + Distance(LCA, q)

Example:
            3
           / \
          5   1
         / \ / \
        6  2 0  8
          / \
         7   4

Distance(6, 4):
  Step 1: Find LCA(6, 4) = 5
  Step 2: Distance(5, 6) = 1  (5 → 6)
  Step 3: Distance(5, 4) = 2  (5 → 2 → 4)
  Answer: 1 + 2 = 3

Visual path: 6 ← 5 → 2 → 4
             (1 edge) + (2 edges) = 3 edges
```

### Step-by-Step Walkthrough

```
Tree:
            3
           / \
          5   1
         / \ / \
        6  2 0  8
          / \
         7   4

Finding Distance(6, 7):

Step 1: Find LCA(6, 7)
  dfs(3) → dfs(5) → dfs(6)=found, dfs(2)→dfs(7)=found
  Both left(6) and right(7) found → LCA = 5

Step 2: Distance(5, 6)
  Start at 5, target=6
  5 → 6: found! distance = 1

Step 3: Distance(5, 7)
  Start at 5, target=7
  5 → 2 → 7: found! distance = 2

Answer: 1 + 2 = 3
Path: 6 → 5 → 2 → 7 (3 edges)
```

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

### Concept

Fire starts at a target node and spreads to adjacent nodes every second. Find the minimum time to burn the entire tree.

```
Tree (as undirected graph for fire spreading):

        1
       / \
      2   3
     /   / \
    4   5   6
       /
      7

Target = 5, Time = 0

Second 1: Fire spreads to neighbors of 5 → {3, 7}
  Burned: {5, 3, 7}

Second 2: Fire spreads to neighbors of {3, 7}
  From 3: {1, 6}
  From 7: {2}
  Burned: {5, 3, 7, 1, 6, 2}

Second 3: Fire spreads to neighbors of {1, 6, 2}
  From 1: {already burned}
  From 6: {already burned}
  From 2: {4}
  Burned: {5, 3, 7, 1, 6, 2, 4}

Total time = 3 seconds
```

### The Key Trick: Convert Tree to Graph

```
A tree is normally directed (parent → child), but fire spreads
in ALL directions (up to parent too). So we convert to undirected graph:

Original tree:          Undirected graph:
      1                     1
     / \                   / \
    2   3                 2───3
   /   / \               /   / \
  4   5   6             4   5───6
     /                   \ /
    7                     7

Step 1: Build parent pointers (creates upward edges)
Step 2: BFS from target (fire spreads in all directions)
Step 3: Count BFS levels until all nodes burned
```

### BFS Walkthrough

```
Building parent map:
  parent[2] = 1, parent[3] = 1
  parent[4] = 2, parent[5] = 3, parent[6] = 3
  parent[7] = 5

BFS from target=5:
  Queue: [5], visited={5}
  
  Level 1 (time=1):
    Dequeue 5, check neighbors: left=None, right=7, parent=3
    → 7 not visited, enqueue. 3 not visited, enqueue.
    Queue: [7, 3], visited={5, 7, 3}
  
  Level 2 (time=2):
    Dequeue 7, check neighbors: parent=5 (visited)
    Dequeue 3, check neighbors: left=5(visited), right=6, parent=1
    → 6 not visited, enqueue. 1 not visited, enqueue.
    Queue: [6, 1], visited={5, 7, 3, 6, 1}
  
  Level 3 (time=3):
    Dequeue 6, check neighbors: all visited
    Dequeue 1, check neighbors: left=2, right=3(visited)
    → 2 not visited, enqueue.
    Queue: [2], visited={5, 7, 3, 6, 1, 2}
  
  Level 4 (time=4):
    Dequeue 2, check neighbors: left=4, parent=1(visited)
    → 4 not visited, enqueue.
    Queue: [4], visited={5, 7, 3, 6, 1, 2, 4}
  
  Level 5: Queue empty.
  
  Total time = 4 seconds
```

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

### Concept

Find all nodes exactly K edges away from a target node.

```
            3
           / \
          5   1
         / \ / \
        6  2 0  8
          / \
         7   4

Target = 5, K = 2

Distance from 5:
  Distance 0: {5}        (the target itself)
  Distance 1: {6, 2}     (direct children)
  Distance 2: {7, 4, 1}  ← ANSWER
                ↑  ↑  ↑
                |  |  └── via parent (5→3→1)
                |  └───── via 2 (5→2→4)
                └──────── via 2 (5→2→7)

Answer: [7, 4, 1]
```

### Two Approaches

```
Approach 1: Graph BFS (straightforward)
  1. Build undirected graph (add parent edges)
  2. BFS from target for exactly K levels
  3. Return all nodes at level K

Approach 2: Recursive DFS (elegant)
  1. Find target in tree
  2. If target in left subtree:
     - Nodes at distance K going DOWN from target
     - Nodes at distance (K - dist - 2) going DOWN from right sibling
     - If K == dist + 1, the current node is at distance K
  3. Similar logic for right subtree
```

### Visual: Recursive DFS Approach

```
            3
           / \
          5   1
         / \ / \
        6  2 0  8
          / \
         7   4

Target = 5, K = 2

Step 1: dfs(3)
  → dfs(5): TARGET FOUND! (distance 0)
    → Find nodes at distance 2 going DOWN from 5:
      5 → 6 (dist 1) → no children → stop
      5 → 2 (dist 1) → 7 (dist 2) ✓, 4 (dist 2) ✓
    → Return distance 0 to parent (3)

Step 2: Back at node 3:
  → Target is in left subtree at distance 1 from 3
  → Check: 1 + 1 == K? → 1 + 1 == 2 → YES! → node 3 is at distance K! 
  
  Wait, 3 is at distance 1 from 5, not 2.
  Actually: dist=0 (at 5), so dist_to_3 = 1.
  K - dist_to_3 - 1 = 2 - 0 - 1 = 1
  → Search right subtree of 3 (node 1) for nodes at distance 1:
    1 → 0 (dist 1) ✓, 1 → 8 (dist 1) ✓
  
  Result: [7, 4, 0, 8] ... hmm let me re-check
  
  Actually the recursive formula:
  If target found in left subtree at distance d:
    - Nodes at distance K from target going downward: found by add_nodes_at_distance
    - Current node is at distance d+1 from target
    - If d+1 == K → current node is in answer
    - Else → search RIGHT subtree for nodes at distance K-d-2

  For node 3, target in left subtree at distance 0:
    d = 0, current node at distance 0+1 = 1 from target
    1 != 2 → search right subtree for distance 2-0-1 = 1
    Right subtree (1): nodes at distance 1 → [0, 8]
  
  Final answer: [7, 4, 0, 8]
  But earlier I said [7, 4, 1]... let me recheck.
  
  Distance from 5 to 1: 5 → 3 → 1 = 2 edges ✓
  Distance from 5 to 0: 5 → 3 → 1 → 0 = 3 edges ✗
  
  So the answer should be [7, 4, 1] for K=2.
  
  The recursive formula: K - d - 2 where d is distance from node to target.
  At node 3: d = 1 (distance from 3 to target 5)
  Search right subtree (1) for distance: K - d - 2 = 2 - 1 - 2 = -1 → skip
  
  And node 3 itself: d + 1 = 1 + 1 = 2 = K → node 3 IS in answer!
  
  Hmm but that gives [7, 4, 3] not [7, 4, 1].
  
  Let me just clarify the algorithm properly...
  
  Actually, the standard recursive approach:
  
  dfs(node) returns distance from node to target, or -1 if not found.
  
  When target is found at some node:
    1. Call add_nodes_at_distance(target, K) — finds K nodes going downward
    2. Return 0 to parent
  
  When parent receives distance d from child:
    If d != -1:
      - Remaining distance to search: K - d - 1
      - If K - d - 1 == 0 → parent is at distance K → add to result
      - Else → search OTHER subtree for K - d - 2 nodes going down
  
  At node 3:
    left child (5) returns d=0
    K - d - 1 = 2 - 0 - 1 = 1
    1 != 0 → search right subtree (1) for distance 1 going down
    From 1: nodes at distance 1 = [0, 8]
    
    But we also need to check if 3 itself is at distance K:
    K - d - 1 = 1 ≠ 0, so 3 is NOT at distance K (it's at distance 1)
  
  At node 1 (searched for distance 1):
    1 → 0 (dist 1) ✓
    1 → 8 (dist 1) ✓
  
  Wait, but 0 and 8 are at distance 3 from target 5:
    5 → 3 → 1 → 0 = 3 edges
    5 → 3 → 1 → 8 = 3 edges
  
  So the answer for K=2 should be: [7, 4, 1]
    5 → 2 → 7 = 2 edges ✓
    5 → 2 → 4 = 2 edges ✓
    5 → 3 → 1 = 2 edges ✓
  
  The issue is: at node 3, we search right subtree for distance K-d-1 = 1.
  But the distance from 3 to 1 is 1 edge, so 1 is at distance d+1+1 = 0+1+1 = 2 ✓!
  
  Actually, the recursive approach works differently:
  - dfs returns distance from current node to target
  - If target is in left subtree at distance d from left child:
    - Left child returned d
    - Current node is at distance d+1 from target
    - If d+1+1 == K → search right subtree of right child? No...
    
  OK this is getting complex. Let me just present the graph BFS approach cleanly
  and the recursive approach with correct formulas.
```

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

### Problem-to-Pattern Mapping

```
╔══════════════════════════════════════════════════════════════════════════╗
║  "lowest common ancestor"     → Recursive DFS (return non-null)      ║
║  "LCA in BST"                 → Value comparison (O(h) time)          ║
║  "distance between nodes"     → LCA + distance from LCA               ║
║  "burn tree / fire spread"    → Parent pointers + BFS                 ║
║  "nodes at distance K"        → Graph BFS (build adj list)           ║
║  "distance from root"         → Simple DFS with depth counter        ║
╚══════════════════════════════════════════════════════════════════════════╝
```

**Interview Tips:**
- LCA binary tree: the recursive solution is elegant — if left and right both return non-null, current node is LCA
- LCA BST: always check if you can use BST property — saves time
- Burning tree: always build parent pointers first, then BFS
- Distance K: graph approach is straightforward; recursive approach is more elegant
- For distance problems, LCA is usually the key first step
