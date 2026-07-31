# DP on Trees — Complete Guide

## What is Tree DP?

Tree DP applies dynamic programming to hierarchical (tree) data using a bottom-up
(post-order) approach. Because every node's answer depends only on its children's
answers, a single depth-first traversal that solves children first and then combines
their results gives a full DP solution without any explicit memoization table.

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

The recursion stack replaces the usual dp array: each recursive call is one
"cell" of the table, filled the moment its children are done.

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

### Helper: The TreeNode Class

Most binary-tree DP functions below take a `root` parameter whose nodes have
`val`, `left`, and `right`. Here is the class used in every code block:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

To build the example trees from level-order lists (as shown in the dry runs),
you can use:

```python
def build_tree(vals):
    """Build a binary tree from a level-order list; None means a missing child."""
    if not vals:
        return None
    nodes = [TreeNode(v) if v is not None else None for v in vals]
    for i, n in enumerate(nodes):
        if n is None:
            continue
        li, ri = 2 * i + 1, 2 * i + 2
        if li < len(nodes):
            n.left = nodes[li]
        if ri < len(nodes):
            n.right = nodes[ri]
    return nodes[0]
```

---

## Path-Based Problems on Trees

Problems in this topic ask for the best path through a tree. The unifying trick:
a path that bends at some node H is the sum of two downward paths leaving H,
so each node only needs to report its best single downward branch.

### Diameter of a Tree

**Problem Explanation:**
Given a tree (a connected, acyclic, undirected graph) with n nodes, find the
diameter: the length of the longest path between any two nodes, measured in
number of edges. The input is an adjacency list, `graph[i]` = list of neighbors
of node `i`, with nodes numbered `0..n-1`. The return value is the edge count of
the longest path.

**State Definition:**
`height(node)` = the length (in edges) of the longest *downward* path from
`node` to a leaf inside its subtree. The global answer `diameter` = the length
of the longest path anywhere, updated at every node. A path is "bent" at its
highest node (closest to the root), and below that node it splits into two
downward branches, so we need the top two heights per node.

**Recurrence Relation:**
```
height(node) = 0                                    (if node is a leaf)
             = 1 + max(height(child))               (otherwise)
diameter     = max(diameter, max1 + max2)           (max1, max2 = two largest child heights)
```
Plain-English reason: every longest path is composed of two downward branches
meeting at its highest node, so its length is exactly the sum of the two longest
child-subtree heights of that node.

**Base Cases:**
- A leaf has `max1 = max2 = 0` and returns `0`.
- A single-node tree returns diameter `0`.

**Intuition (Why This Works):**
Post-order DFS visits all children before the parent, so when we compute the
parent's top two heights, both are already final — this is DP in disguise, with
the recursion stack acting as the table. The choice being made at each node is
which two child branches to join into a candidate path; the best candidate over
all nodes is the diameter, and it does not necessarily pass through the root.
A visited array (or passing the parent) stops the traversal from walking back
up the tree.

**Step-by-Step Procedure:**
1. Build the adjacency list `graph` where `graph[i]` lists every neighbor of `i`.
2. Initialize `visited = [False] * n` and `diameter = 0`.
3. Define `height(node)`: mark `node` visited; set `max1 = max2 = 0`.
4. For each unvisited neighbor `nei`, recursively get `child_h = height(nei) + 1`.
5. Keep the two largest values: shift `max1` down to `max2` when a new maximum
   appears, otherwise try to replace `max2`.
6. Update `diameter = max(diameter, max1 + max2)` — the best path bent at this node.
7. Return `max1` (the single best branch) to the caller.
8. Call `height(0)` and print `diameter`.

**Worked Example (Dry Run):**
```
Tree (adjacency list):
       0
     /   \
    1     2
   / \     \
  3   4     5

DFS trace (post-order):
  Node 3: max1=0, max2=0 → height=0 (leaf)
  Node 4: max1=0, max2=0 → height=0 (leaf)
  Node 1: children 3,4 both give height 0+1=1
           max1=1, max2=1 → diameter candidate = 1+1 = 2
           returns height = 1
  Node 5: max1=0, max2=0 → height=0 (leaf)
  Node 2: child 5 gives height 0+1=1 → max1=1, max2=0
           diameter candidate = 1+0 = 1
           returns height = 1
  Node 0: child 1 gives height 1+1=2, child 2 gives height 1+1=2
           max1=2, max2=2 → diameter candidate = 2+2 = 4  ← MAX!
           returns height = 2

Answer: 4  (path: 3 → 1 → 0 → 2 → 5, which uses 4 edges)
```

**Code:**

```python
def tree_diameter(graph: list) -> int:
    """Return the diameter (longest path in edges) of a tree given as adjacency list."""
    n = len(graph)
    visited = [False] * n
    diameter = 0

    def height(node: int) -> int:
        # post-order: solve all children first, then combine into this node's height
        nonlocal diameter
        visited[node] = True          # this node is being processed
        max1 = max2 = 0               # two longest child heights seen so far
        for nei in graph[node]:
            if not visited[nei]:      # don't walk back to the parent
                child_h = height(nei) + 1   # longest downward path through this child
                if child_h > max1:          # new best: demote old best to second place
                    max2, max1 = max1, child_h
                elif child_h > max2:        # not best, but still better than second
                    max2 = child_h
        diameter = max(diameter, max1 + max2)  # best path BENT at this node
        return max1                           # return only the single best branch

    height(0)
    return diameter

# Time: O(n), Space: O(n)
```

**Complexity:**
- Time: O(n) — every node and every edge is touched once.
- Space: O(n) — the visited array plus up to O(n) recursion stack depth on a chain.

**Common Mistakes & Edge Cases:**
- Forgetting to prevent walking back to the parent, which turns the tree into a
  cycle and breaks the recursion. (A visited array or an explicit `parent`
  argument fixes this.)
- Tracking only the single longest child height — the diameter needs the TWO
  longest, because a path bends through a node.
- Assuming the diameter passes through the root. It may lie entirely inside one
  subtree, which is why the global `diameter` is updated at every node.
- Single-node tree: answer is `0`, not `1`.
- A straight chain of n nodes has diameter `n - 1`; make sure a chain-shaped
  graph doesn't blow the recursion stack (an iterative version avoids this).

---

### Maximum Path Sum in a Binary Tree

**Problem Explanation:**
Given a binary tree where every node holds an integer value (possibly negative),
find the maximum sum of any path. Here a "path" is any sequence of nodes joined
by parent–child edges; it may start and end anywhere (it does not have to pass
through the root or end at leaves). Return the integer maximum path sum.

**State Definition:**
`best_down(node)` = the maximum sum of a path that starts at `node` and moves
only downward through one branch of its subtree (either just `node` itself, or
`node` plus the best downward path of one child). Separately, the global
`max_sum` = the best sum of any path, updated at each node by joining the best
left branch, the node, and the best right branch.

**Recurrence Relation:**
```
best_down(node) = node.val + max(0, best_down(left), best_down(right))
max_sum         = max(max_sum, max(0, best_down(left)) + node.val + max(0, best_down(right)))
```
Plain-English reason: any path whose highest point is `node` is the sum of one
downward branch in each child subtree plus the node itself; a child branch with
negative sum is discarded (max with 0), because skipping it can only improve the
total.

**Base Cases:**
- `None` node: `best_down = 0` (an empty branch contributes nothing).
- Initial value of `max_sum` must be `float('-inf')` so the first node always
  updates it (important when all values are negative).

**Intuition (Why This Works):**
Post-order traversal computes each child's `best_down` before the parent, so the
parent can read final values from both children — the recursion itself is the
DP table. The key choice is whether to include each child branch or throw it
away (the `max(..., 0)`); two distinct results are produced at each node: the
candidate path *through* the node (goes into the global answer) and the best
single branch *starting* at the node (is returned upward so an ancestor can use
it). This is why the function returns `node.val + max(left, right)` while the
global answer uses `left + right + node.val`.

**Step-by-Step Procedure:**
1. Initialize `max_sum = float('-inf')` outside the DFS.
2. Define `dfs(node)`; if `node` is `None`, return `0`.
3. Recurse into both children, then clamp each result: `left = max(dfs(node.left), 0)`,
   `right = max(dfs(node.right), 0)` — negative branches are dropped.
4. Update `max_sum = max(max_sum, left + right + node.val)` — the path bent
   through this node.
5. Return `node.val + max(left, right)` — the best single downward branch for
   the parent.
6. After `dfs(root)`, return `max_sum`.

**Worked Example (Dry Run):**
```
Tree:      -10
          /   \
         9    20
             /  \
            15   7

DFS trace (post-order):
  Node 9:  left=0, right=0 → path_through = 9.     Return 9+0 = 9
  Node 15: left=0, right=0 → path_through = 15.    Return 15
  Node 7:  left=0, right=0 → path_through = 7.     Return 7
  Node 20: left=15, right=7
            path_through = 15 + 20 + 7 = 42  ← global max!
            Return 20 + max(15,7) = 35
  Node -10: left=9, right=35
             path_through = 9 + (-10) + 35 = 34
             Return -10 + max(9,35) = 25

Global max = 42  (path: 15 → 20 → 7)
```

**Code:**

```python
def max_path_sum(root) -> int:
    """Return the maximum path sum in a binary tree (path can start and end anywhere)."""
    max_sum = float('-inf')          # global answer; -inf so negative trees still work

    def dfs(node):
        nonlocal max_sum
        if not node:
            return 0                 # empty subtree contributes 0 to any path
        # Best downward path from each child, clamping negatives to 0:
        # a negative branch is worse than skipping it entirely.
        left = max(dfs(node.left), 0)
        right = max(dfs(node.right), 0)
        # Candidate path that BENDS through this node: best-left + node + best-right.
        max_sum = max(max_sum, left + right + node.val)
        # Return the best SINGLE downward branch so an ancestor can extend it.
        return node.val + max(left, right)

    dfs(root)
    return max_sum

# Time: O(n), Space: O(h) — h = height of tree (recursion stack)
```

**Complexity:**
- Time: O(n) — each node is visited once.
- Space: O(h) — recursion stack, where h is the tree height; O(n) worst case on a
  skewed (chain-like) tree.

**Common Mistakes & Edge Cases:**
- Forgetting the `max(..., 0)` clamp on child results — this is what allows
  paths to avoid negative subtrees and is the whole difference between "path
  through node" and "any path".
- Initializing `max_sum` to `0` instead of `float('-inf')`: a tree of all
  negative values would then incorrectly return `0` instead of the largest
  single node value.
- Confusing the returned value (`best_down`, a single branch) with the global
  answer (a bent path) — the function returns one thing but updates another.
- Empty tree: the function would return `-inf`; guard `if not root: return 0`
  if your test cases include it.

---

### Maximum Path Sum Between Leaves

**Problem Explanation:**
This is the previous problem with a strict rule: the path MUST start at one leaf
and end at another leaf, where a leaf is a node with no children. Given the
binary tree, return the maximum leaf-to-leaf path sum. If no leaf-to-leaf path
exists (e.g., a tree with a single node), return the single node's value.

**State Definition:**
`leaf_path(node)` = the maximum sum of a path that starts at `node` and descends
to a leaf within its subtree (used only for nodes that can reach a leaf). The
global `max_sum` = the best sum of a path joining a leaf in the left subtree,
the node, and a leaf in the right subtree — only valid at nodes that have two
children both containing leaves.

**Recurrence Relation:**
```
leaf_path(node) = node.val                                       (if node is a leaf)
                = node.val + max(leaf_path(left), leaf_path(right))   (has a child)
max_sum = max(max_sum, leaf_path(left) + node.val + leaf_path(right))
                (only when BOTH children return a valid leaf path)
```
Plain-English reason: a leaf-to-leaf path is an upward branch from one leaf to a
joining node, plus a downward branch to another leaf, so at every node that has
two leaf-bearing children we try joining them and remember the best join.

**Base Cases:**
- `None` node returns `float('-inf')` — meaning "no leaf exists in this empty
  direction", which prevents invalid joins.
- A leaf returns `node.val`.
- Fallback: if no node ever had two leaf-bearing children (`max_sum` still
  `-inf`), the tree has at most one leaf; return `root.val`.

**Intuition (Why This Works):**
The structure is identical to maximum path sum, but now we must not fake a "leaf
path" from an empty child: empty children return `-inf` instead of `0` so they
are never joined. Only nodes whose left AND right subtrees both contain a leaf
can form a leaf-to-leaf path. Post-order DFS again supplies children's final
answers before the parent needs them; the choice is which leaf-bearing branch to
send upward (the max of the two) versus which join to record globally.

**Step-by-Step Procedure:**
1. Initialize `max_sum = float('-inf')`.
2. Define `dfs(node)`; if `None`, return `-inf` (no leaf below).
3. If `node` is a leaf (no children), return `node.val`.
4. Recurse into left and right to get their best leaf-paths.
5. If both children returned valid values (not `-inf`), update
   `max_sum = max(max_sum, left + right + node.val)`.
6. Return `node.val + max(left, right)` — the best leaf-path through this node.
7. After the DFS, return `max_sum` if it was updated, otherwise `root.val`.

**Worked Example (Dry Run):**
```
Tree:      -10
          /   \
         9    20
             /  \
            15   7

Leaves are 9, 15 and 7. Possible leaf-to-leaf paths:
  9 → -10 → 20 → 15   = 34
  9 → -10 → 20 → 7    = 26
  15 → 20 → 7         = 42  ← best

DFS trace (post-order):
  Node 9:  leaf → returns 9
  Node 15: leaf → returns 15
  Node 7:  leaf → returns 7
  Node 20: left=15, right=7, both valid → max_sum = 15+20+7 = 42
           returns 20 + max(15,7) = 35
  Node -10: left=9, right=35, both valid → max_sum = max(42, 9+(-10)+35) = 42
            returns -10 + max(9,35) = 25

Answer: 42
```

**Code:**

```python
def max_path_sum_leaves(root) -> int:
    """Return the max path sum where the path MUST start and end at leaves."""
    max_sum = float('-inf')          # global best leaf-to-leaf sum

    def dfs(node):
        nonlocal max_sum
        if not node:
            # No leaf can live in an empty subtree. -inf marks 'invalid path',
            # so we never join an empty branch into a leaf-to-leaf path.
            return float('-inf')
        if not node.left and not node.right:
            return node.val          # this node IS a leaf
        left = dfs(node.left)
        right = dfs(node.right)
        # Only update when BOTH children supply a valid path to a leaf.
        if left != float('-inf') and right != float('-inf'):
            max_sum = max(max_sum, left + right + node.val)
        # Send the best single leaf-path upward; -inf propagates from empty sides.
        return node.val + max(left, right)

    dfs(root)
    # If no two leaves were ever joinable, the tree has at most one leaf: use it.
    return max_sum if max_sum != float('-inf') else root.val

# Time: O(n), Space: O(h)
```

**Complexity:**
- Time: O(n) — every node is visited once.
- Space: O(h) — recursion stack, O(n) worst case on a skewed tree.

**Common Mistakes & Edge Cases:**
- Using `0` instead of `-inf` for empty subtrees — that would silently create
  fake "leaf paths" at nodes with only one child.
- Updating `max_sum` even when only one child is valid — a leaf-to-leaf path
  needs a leaf in BOTH directions.
- A single-node tree: no pair of leaves exists, so the fallback `root.val`
  handles it.
- A tree that is a straight chain has only one leaf (one end), so no leaf-to-leaf
  path exists; the fallback returns `root.val`, not the sum of the chain.

---

## Selection Problems on Trees (Two-State Take/Skip DP)

These problems share one shape: at each node you choose between two states, and
the choice's feasibility at the parent depends on which state the children are
in. The DFS returns a `(stateA, stateB)` tuple and the parent combines both.

### House Robber III

**Problem Explanation:**
The houses of a neighborhood form a binary tree, and each house holds a fixed
amount of money in `node.val`. You may not rob two directly linked houses (a
parent and its child) on the same night. Maximize the total amount you can rob
from the whole tree. Input is the root `TreeNode`; return the maximum integer
sum.

**State Definition:**
`dfs(node)` returns a two-tuple `(rob_this, skip_this)` where:
- `rob_this` = max money obtainable from `node`'s subtree **given that `node`
  itself is robbed**;
- `skip_this` = max money obtainable from `node`'s subtree **given that `node`
  is NOT robbed**.
The answer is `max(dfs(root))`.

**Recurrence Relation:**
```
rob_this  = node.val + skip_left + skip_right
skip_this = max(left) + max(right)         # left is (rob_this, skip_this), so max(left) chooses the better state
```
Plain-English reason: if you rob the node, both children are forbidden, so you
must take their "skip" values; if you skip the node, each child is free to make
its own best choice, so you take each child's maximum.

**Base Cases:**
- `None` node returns `(0, 0)` — an empty subtree earns nothing either way.
- A leaf returns `(node.val, 0)`.

**Intuition (Why This Works):**
The parent's decision depends on which state each child ended in, so each child
must report both states — this is exactly why the DFS returns a tuple instead of
a single number. Post-order traversal fills the "table" from the leaves up; the
choice at each node is forced (rob → children skip, skip → children free), so no
guessing is needed, only correct aggregation. Because every combination is
covered by the two states, the final `max` at the root is globally optimal.

**Step-by-Step Procedure:**
1. Define `dfs(node)`; if `node` is `None`, return `(0, 0)`.
2. Recurse: `left = dfs(node.left)`, `right = dfs(node.right)`.
3. Compute `rob_this = node.val + left[1] + right[1]` (children must skip).
4. Compute `skip_this = max(left) + max(right)` (children choose their best).
5. Return the tuple `(rob_this, skip_this)`.
6. At the top level, return `max(dfs(root))`.

**Worked Example (Dry Run):**
```
Tree:     3
        /   \
       2     3
        \     \
         3     1

DFS trace (post-order):
  Node 3 (leaf, left-right): returns (3, 0)
  Node 2: left=(0,0), right=(3,0)
    rob  = 2 + 0 + 0 = 2
    skip = max(0,0) + max(3,0) = 3
    returns (2, 3)
  Node 1 (leaf, right-right): returns (1, 0)
  Node 3 (right): left=(0,0), right=(1,0)
    rob  = 3 + 0 + 0 = 3
    skip = max(0,0) + max(1,0) = 1
    returns (3, 1)
  Root 3: left=(2,3), right=(3,1)
    rob  = 3 + 3 + 1 = 7   ← rob root + skip children's best-skip states
    skip = max(2,3) + max(3,1) = 3 + 3 = 6

Answer: max(7, 6) = 7   (rob root 3, plus left-leaf 3, plus right-leaf 1)
```

**Code:**

```python
def rob_tree(root) -> int:
    """Max money with the rule: two directly-linked houses cannot both be robbed."""

    def dfs(node):
        if not node:
            return (0, 0)              # (rob_this, skip_this) for an empty subtree

        left = dfs(node.left)          # left = (rob_left, skip_left)
        right = dfs(node.right)        # right = (rob_right, skip_right)

        # If we rob THIS node, its children MUST be skipped (they are adjacent).
        rob_this = node.val + left[1] + right[1]
        # If we skip THIS node, each child is free to pick its better state.
        not_rob_this = max(left) + max(right)

        return (rob_this, not_rob_this)

    return max(dfs(root))              # root can be robbed or skipped; take the best

# Time: O(n), Space: O(h)
```

**Complexity:**
- Time: O(n) — each node visited once.
- Space: O(h) — recursion stack, O(n) worst case on a skewed tree.

**Common Mistakes & Edge Cases:**
- Indexing the tuple wrongly: `rob_this` needs the children's **skip** values
  (`[1]`), while `skip_this` uses `max(...)` over the whole tuples.
- Forgetting that each child may independently choose to rob or skip — children
  do not share a single global decision.
- Empty tree: `max(dfs(None)) = 0`, fine — but callers with `root = None` should
  handle it gracefully.
- All-positive and all-negative node values both work because the recurrence
  always sums the better states.

---

### Minimum Vertex Cover

**Problem Explanation:**
Given a binary tree, select a set of vertices such that every edge has at least
one of its two endpoints selected. A set with this property is called a
*vertex cover*. Find the minimum size of such a set and return that integer.
For example, in a tree with edges (1,2) and (1,3), selecting `{1}` covers both
edges.

**State Definition:**
`dfs(node)` returns `(cover_this, skip_this)` where:
- `cover_this` = minimum cover size in `node`'s subtree given that `node` IS
  selected;
- `skip_this` = minimum cover size in `node`'s subtree given that `node` is NOT
  selected.
The answer is `min(dfs(root))` (and `0` for an empty tree).

**Recurrence Relation:**
```
skip_this  = cover_left + cover_right
cover_this = 1 + min(left) + min(right)
```
Plain-English reason: if `node` is skipped, the edges from `node` to its children
must be covered by the children, so both children are forced into the "cover"
state; if `node` is covered, each child is free to take whichever of its two
states is smaller.

**Base Cases:**
- `None` node returns `(0, 0)`.
- Empty tree returns `0`.

**Intuition (Why This Works):**
Each edge is a constraint connecting exactly one parent-child pair, so deciding
the parent's state fully determines what the children are allowed to do — the
two-state tuple carries exactly the information the parent needs. Post-order
traversal guarantees children's optimal covers exist before the parent sums
them; the forced choices (child must be covered when parent is skipped) make the
greedy per-node aggregation provably optimal.

**Step-by-Step Procedure:**
1. If `root` is `None`, return `0`.
2. Define `dfs(node)`; if `None`, return `(0, 0)`.
3. Recurse into `left` and `right`.
4. Compute `not_cover = left[0] + right[0]` — children must cover their edges.
5. Compute `cover = 1 + min(left) + min(right)` — node selected, children free.
6. Return `(cover, not_cover)`.
7. Return `min(dfs(root))`.

**Worked Example (Dry Run):**
```
Tree:     3
        /   \
       2     3
        \     \
         3     1

Edges: (3,2), (3,3), (2,3'), (3,1)   [3' = left child of 2]

DFS trace (post-order):
  Node 3 (left-right leaf): (cover=1, skip=0)
  Node 2: left=(0,0), right=(1,0)
    skip = left[0] + right[0] = 0 + 1 = 1
    cover = 1 + min(0,0) + min(1,0) = 1
    returns (1, 1)
  Node 1 (right-right leaf): (cover=1, skip=0)
  Node 3 (right): left=(0,0), right=(1,0)
    skip = 0 + 1 = 1, cover = 1 + 0 + 0 = 1
    returns (1, 1)
  Root 3: left=(1,1), right=(1,1)
    skip = 1 + 1 = 2     ← skip root, cover both children
    cover = 1 + 1 + 1 = 3
    returns (3, 2)

Answer: min(3, 2) = 2   (select nodes 2 and 3-right; every edge is covered)
```

**Code:**

```python
def vertex_cover(root) -> int:
    """Minimum number of vertices such that every edge touches a selected vertex."""

    def dfs(node):
        if not node:
            return (0, 0)              # (cover_this, skip_this) for an empty subtree
        left = dfs(node.left)
        right = dfs(node.right)
        # Node NOT selected: the edges node-child must be covered by the children,
        # so both children are FORCED into the covered state.
        not_cover = left[0] + right[0]
        # Node selected: covers its own edges; each child may pick its cheaper state.
        cover = 1 + min(left) + min(right)
        return (cover, not_cover)

    if not root:
        return 0
    return min(dfs(root))              # root may be selected or not; take the smaller

# Time: O(n), Space: O(h)
```

**Complexity:**
- Time: O(n) — each node visited once.
- Space: O(h) — recursion stack, O(n) worst case.

**Common Mistakes & Edge Cases:**
- Empty tree returns `0` (there are no edges to cover).
- A single-node tree has no edges, so the minimum cover is `0`, not `1`.
- Forgetting that a skipped node FORCES its children into the cover state — this
  is the opposite of the House Robber rule and is the most common bug.
- Reading the tuple backwards: `skip_this` uses `left[0] + right[0]`, not
  `left[1] + right[1]`.

---

### Maximum Independent Set in a Tree

**Problem Explanation:**
Given a binary tree, find the largest set of nodes such that no two nodes in the
set are adjacent (directly connected by an edge). Such a set is an *independent
set*. Return the maximum possible size. It is the "counting" mirror of the
vertex cover: for any graph, `max independent set = n - min vertex cover`, and
the two DPs have symmetric recurrences.

**State Definition:**
`dfs(node)` returns `(take_node, skip_node)` where:
- `take_node` = maximum independent-set size in `node`'s subtree given that
  `node` IS in the set;
- `skip_node` = maximum size given that `node` is NOT in the set.
The answer is `max(dfs(root))`.

**Recurrence Relation:**
```
take_node = 1 + skip_left + skip_right
skip_node = max(left) + max(right)
```
Plain-English reason: if `node` is in the set, its children cannot be (they are
adjacent), so we take both children's "skip" values; if `node` is skipped, each
child may independently be in or out of the set, whichever is larger.

**Base Cases:**
- `None` node returns `(0, 0)`.
- A leaf returns `(1, 0)`.

**Intuition (Why This Works):**
This is literally the same recurrence as House Robber III, reframed: "money in a
house" becomes "a node counted as 1", and the adjacency rule is identical. The
two-state tuple resolves the only conflict — whether children are available —
before the parent's decision is made. Post-order DFS guarantees optimal
subtree values are final when combined.

**Step-by-Step Procedure:**
1. Define `dfs(node)`; if `None`, return `(0, 0)`.
2. Recurse into both children.
3. Compute `take_node = 1 + left[1] + right[1]` (children forced out of the set).
4. Compute `skip_node = max(left) + max(right)` (children free to choose).
5. Return `(take_node, skip_node)`.
6. Return `max(dfs(root))`.

**Worked Example (Dry Run):**
```
Tree:     3
        /   \
       2     3
        \     \
         3     1

DFS trace (post-order):
  Node 3 (left-right): returns (take=1, skip=0)
  Node 2: left=(0,0), right=(1,0)
    take = 1 + 0 + 0 = 1
    skip = max(0,0) + max(1,0) = 1
    returns (1, 1)
  Node 1 (right-right): returns (1, 0)
  Node 3 (right): left=(0,0), right=(1,0)
    take = 1 + 0 + 0 = 1
    skip = 0 + max(1,0) = 1
    returns (1, 1)
  Root 3: left=(1,1), right=(1,1)
    take = 1 + 1 + 1 = 3   ← take root, skip children's subtrees
    skip = max(1,1) + max(1,1) = 2

Answer: max(3, 2) = 3   (set = {root 3, left-right 3, right-right 1}; none are adjacent)
```

**Code:**

```python
def max_independent_set(root) -> int:
    """Largest set of nodes with no two adjacent (no parent-child pairs)."""

    def dfs(node):
        if not node:
            return (0, 0)              # (take_node, skip_node) for an empty subtree
        left = dfs(node.left)
        right = dfs(node.right)
        # Node taken: it is adjacent to its children, so they must be skipped.
        take_node = 1 + left[1] + right[1]
        # Node skipped: children are free to be taken or skipped, pick the best.
        skip_node = max(left) + max(right)
        return (take_node, skip_node)

    return max(dfs(root))              # root may be taken or skipped; take the larger

# Time: O(n), Space: O(h)
```

**Complexity:**
- Time: O(n) — each node visited once.
- Space: O(h) — recursion stack, O(n) worst case.

**Common Mistakes & Edge Cases:**
- Confusing this with the vertex cover: the recurrences are mirror images —
  here the taken node is worth `+1` and children are skipped; there the skipped
  node forces children to be covered.
- A single-node tree has an independent set of size `1`.
- Empty tree returns `0` (`max((0,0))`).
- All nodes have the same value: answer is the maximum number of non-adjacent
  nodes, which depends only on the shape.

---

## Counting and Monitoring Problems on Trees

These problems keep extra bookkeeping during a single traversal: a running sum
with a hashmap, a three-state label, or a forest root flag.

### Count Paths with Sum K

**Problem Explanation:**
Given a binary tree and an integer `target_sum`, count how many downward paths
sum to `target_sum`. A downward path starts at any node and moves only through
child links (it may be a single node). Return the integer count. Nodes can hold
negative values, which is why this needs prefix-sum counting rather than simple
subtree sums.

**State Definition:**
There is no per-node numeric DP state. Instead the algorithm threads one
variable — the running sum from the root down to the current node — and one
hashmap `prefix`, where `prefix[s]` = how many times the running sum has equaled
`s` on the current root-to-node path *before* reaching the current node.

**Recurrence Relation:**
```
For the current node with running sum curr:
  count += 1 if curr == target_sum                 # path starting at the root
  count += prefix[curr - target_sum]               # paths ending here that start deeper
  prefix[curr] += 1, then recurse left and right, then prefix[curr] -= 1
```
Plain-English reason: a downward path ending at the current node has sum
`target_sum` exactly when the running sum before that path equals
`curr - target_sum`, and `prefix` stores how many times each such running sum
occurred on the current branch.

**Base Cases:**
- `None` node: return immediately (no node to count).
- Empty `prefix` map at the start of the DFS.

**Intuition (Why This Works):**
This is the two-sum idea carried along a DFS: the current running sum lets us
look up "how many earlier points on this root-to-node path are exactly
`curr - target_sum` behind me", which counts every valid downward path ending
here in O(1). The `prefix[curr] -= 1` after visiting both children is
*backtracking*: each branch of the tree has its own prefix history, so a sum
from a finished sibling must not leak into another branch. Because every path
is counted exactly once, at the node where it ends, the total is correct.

**Step-by-Step Procedure:**
1. Initialize `count = 0` and `prefix = {}`.
2. Define `dfs(node, curr_sum)`; if `node` is `None`, return.
3. Add the node's value: `curr_sum += node.val`.
4. If `curr_sum == target_sum`, a root-starting path is found: `count += 1`.
5. Add the number of earlier prefixes equal to `curr_sum - target_sum`:
   `count += prefix.get(curr_sum - target_sum, 0)`.
6. Record the current prefix: `prefix[curr_sum] += 1`.
7. Recurse into `node.left` and `node.right` with `curr_sum`.
8. Backtrack: `prefix[curr_sum] -= 1` (remove this sum from the active branch).
9. Return `count`.

**Worked Example (Dry Run):**
```
Tree:      10
         /    \
        5     -3
       / \      \
      3   2     11
     / \   \
    3  -2   1
    target_sum = 8

DFS trace (showing count updates):
  Node 10:  curr=10, no prefix match          count=0,  prefix={10:1}
  Node 5:   curr=15, prefix[7]=0              count=0,  prefix={10:1,15:1}
  Node 3:   curr=18, prefix[10]=1 → count=1   (path 5+3=8)   prefix adds 18
  Node 3:   curr=21, prefix[13]=0             count=1        prefix adds 21
  Node -2:  curr=16, prefix[8]=0              count=1        prefix adds 16
  Node 2:   curr=17, prefix[9]=0              count=1        prefix adds 17
  Node 1:   curr=18, prefix[10]=1 → count=2   (path 5+2+1=8) prefix adds 18
  Node -3:  curr=7,  prefix[-1]=0             count=2        prefix adds 7
  Node 11:  curr=18, prefix[10]=1 → count=3   (path -3+11=8)

Answer: 3
```

**Code:**

```python
def path_sum_count(root, target_sum: int) -> int:
    """Count downward paths in a binary tree whose node values sum to target_sum."""
    count = 0
    prefix = {}                     # prefix[s] = how many times running sum 's'
                                    # has appeared on the CURRENT root-to-node path

    def dfs(node, curr_sum):
        nonlocal count
        if not node:
            return                  # nothing to count below an empty subtree
        curr_sum += node.val        # extend the running sum with this node

        # Case 1: the path that starts at the root and ends here.
        if curr_sum == target_sum:
            count += 1
        # Case 2: paths that start below the root. Any earlier prefix sum equal
        # to (curr_sum - target_sum) means the segment between then and now sums
        # to exactly target_sum. prefix.get(..., 0) is safe when key is absent.
        count += prefix.get(curr_sum - target_sum, 0)

        # Register the current running sum as a possible start point for the
        # paths found in the subtrees below, then explore children...
        prefix[curr_sum] = prefix.get(curr_sum, 0) + 1
        dfs(node.left, curr_sum)
        dfs(node.right, curr_sum)

        # Backtrack: remove this sum so sibling branches don't see it.
        prefix[curr_sum] -= 1

    dfs(root, 0)
    return count

# Time: O(n), Space: O(h)
```

**Complexity:**
- Time: O(n) — each node is visited once, and each hashmap lookup is O(1).
- Space: O(h) — the prefix map holds at most one entry per depth level, plus the
  recursion stack.

**Common Mistakes & Edge Cases:**
- Forgetting the backtracking `prefix[curr_sum] -= 1` — without it, a sum from
  one branch is wrongly visible to another branch and paths get double-counted.
- Looking up `curr_sum - target_sum` BEFORE adding the current sum to the map —
  the current node must not be its own prefix (that would allow empty paths).
- A `target_sum` of 0 still works, but paths must contain at least one node; the
  ordering above ensures no empty path is counted.
- Negative node values are fine; they only make the prefix sums non-monotonic,
  which the hashmap handles.
- Using `prefix[curr_sum] = prefix.get(curr_sum, 0) + 1` (get-or-create) is
  required since sums can repeat.

---

### Binary Tree Cameras

**Problem Explanation:**
You have a binary tree and you may install a camera on any node. One camera
monitors its own node, its parent, and its direct children. Find the minimum
number of cameras needed so that every node in the tree is monitored. Return
that integer.

**State Definition:**
`dfs(node)` returns a three-state label describing whether `node` is already
monitored, where the label is decided from the children's states:
- `0` = node is NOT monitored by anyone below it yet;
- `1` = node is monitored (covered by a camera placed in one of its children);
- `2` = a camera is installed ON this node.
A global counter `cameras` counts every camera placed.

**Recurrence Relation:**
(Greedy decision rules — given the children's states `left` and `right`:)
```
left, right = dfs(node.left), dfs(node.right)
if left == 0 or right == 0:   cameras += 1; return 2   # uncovered child → put camera here
elif left == 2 or right == 2: return 1                 # covered by a child's camera
else:                         return 0                 # children covered by grandchildren → I'm uncovered
At the root: if root returns 0, cameras += 1.
```
Plain-English reason: process children bottom-up, and whenever a child reports
it is uncovered, the cheapest fix is a camera on the current node because that
camera covers the child, the parent side, and the node itself — covering upward
greedily is optimal since a camera can never cover anything below its own
subtree.

**Base Cases:**
- `None` node returns `1` (an empty child must be treated as "covered", never as
  "uncovered", so it never forces a camera).
- After the root's DFS, if the root returned `0`, one extra camera is added for
  the root itself (nothing above can cover it).

**Intuition (Why This Works):**
The state must remember more than "selected or not" — it has to remember who
covered the node — so we need three states instead of two. Post-order traversal
resolves every child before its parent, so the decision rules never look ahead;
the choice "place a camera only when forced" is optimal because a camera placed
at a parent strictly covers more upward territory than one placed at the child,
so delaying camera placement to the highest possible node is always best.

**Step-by-Step Procedure:**
1. Initialize `cameras = 0`.
2. Define `dfs(node)`; if `None`, return `1` (empty subtree counts as covered).
3. Recurse: `left = dfs(node.left)`, `right = dfs(node.right)`.
4. If either child is uncovered (`0`): place a camera here, `cameras += 1`,
   return `2`.
5. Else if either child has a camera (`2`): this node is covered, return `1`.
6. Else (both children are `1`, covered by their own children): this node is not
   yet covered, return `0`.
7. Run `root_state = dfs(root)`.
8. Return `cameras + (1 if root_state == 0 else 0)`.

**Worked Example (Dry Run):**
```
Tree:         0
             /
            0
           /
          0
  (a straight chain of 3 nodes)

DFS trace (post-order):
  Bottom node 0: no children → returns 1 (covered)
  Middle node 0: left = 1 (no uncovered child, no camera child)
                 → returns 0 (not covered yet)
  Root node 0:   left = 0 (uncovered!) → place camera here, cameras = 1, returns 2
  root_state = 2, no extra camera needed.

Answer: 1   (one camera at the middle node monitors all three nodes)

Another example:
          0
         / \
        0   0
       / \
      0   0

  Both leaf pairs return 0 from their parents; the left child has uncovered
  children → camera at left child (cameras=1, returns 2); the right child is
  uncovered (returns 0); the root sees an uncovered child → camera at root
  (cameras=2). Answer: 2.
```

**Code:**

```python
def min_camera_cover(root) -> int:
    """Minimum cameras so every node is monitored by itself, a parent, or a child."""
    cameras = 0

    def dfs(node):
        nonlocal cameras
        if not node:
            # Empty children are treated as 'covered' so they never force a camera.
            return 1
        left = dfs(node.left)
        right = dfs(node.right)
        # If any child reports uncovered (0), the cheapest fix is a camera HERE:
        # it covers the child, this node, and this node's parent.
        if left == 0 or right == 0:
            cameras += 1
            return 2                       # 2 = this node has a camera
        # No uncovered child, but a child has a camera -> this node is covered.
        if left == 2 or right == 2:
            return 1                       # 1 = covered by a child
        # Both children were covered by their own children -> this node is NOT
        # covered yet; report 0 so the PARENT decides whether to place a camera.
        return 0

    root_state = dfs(root)
    # If the root itself is still uncovered, nothing above can cover it:
    # place one final camera on the root.
    return cameras + (1 if root_state == 0 else 0)

# Time: O(n), Space: O(h)
```

**Complexity:**
- Time: O(n) — each node visited once.
- Space: O(h) — recursion stack, O(n) worst case.

**Common Mistakes & Edge Cases:**
- Returning `0` for `None` children instead of `1` — an empty child would then
  count as "uncovered" and force cameras on every leaf's parent.
- Forgetting the final `+1` when the root reports `0`; nothing above the root
  can ever cover it.
- Confusing the three states: `0` means *not yet covered*, `1` means *covered by
  a child*, `2` means *has a camera*; both `1` and `2` satisfy "monitored".
- A single-node tree needs exactly `1` camera.
- A chain tree of any length: a camera every two nodes (e.g., 3-node chain → 1).

---

### Delete Nodes and Return Forest

**Problem Explanation:**
Given a binary tree and a list of node values to delete, deleting those nodes
splits the tree into several disconnected subtrees. Return a list containing the
roots of all the remaining trees (a *forest*). The order of the returned list
does not matter. The returned subtrees may be the original mutated nodes (the
deleted nodes are removed from the tree).

**State Definition:**
`dfs(node, is_root)` returns the (possibly modified) subtree headed by `node`,
or `None` if `node` was deleted. `is_root` is a boolean saying whether `node`
would be the root of a new forest tree if it survives — this is exactly the
information that decides whether to add `node` to the output list.

**Recurrence Relation:**
```
node_deleted = node.val in to_delete
if is_root and not node_deleted: forest.append(node)     # a surviving root goes in the answer
node.left  = dfs(node.left,  node_deleted)               # deleted parent → child becomes a root
node.right = dfs(node.right, node_deleted)
return None if node_deleted else node
```
Plain-English reason: a node is the root of a forest tree exactly when it was
not deleted and its parent was deleted (or it is the original root), so passing
`node_deleted` down as the next `is_root` makes every surviving node reach the
append decision once.

**Base Cases:**
- `None` node returns `None`.

**Intuition (Why This Works):**
The key insight is that a node becomes a "new root" precisely at the moment its
parent is deleted — so the single boolean `is_root` threaded through the
recursion captures all the structural information, and no post-processing is
needed. Post-order DFS rebuilds the tree's links bottom-up, and mutating
`node.left` / `node.right` to the results of the children's DFS is what
physically detaches deleted subtrees. Deleting happens "on the way down" (we
know the value immediately), while forest building is finished on the way up.

**Step-by-Step Procedure:**
1. Convert `to_delete` into a set for O(1) membership tests.
2. Initialize `forest = []`.
3. Define `dfs(node, is_root)`; if `None`, return `None`.
4. Record `node_deleted = node.val in to_delete`.
5. If `is_root` and not deleted, append `node` to `forest` (it is a surviving tree root).
6. Recurse: `node.left = dfs(node.left, node_deleted)` and
   `node.right = dfs(node.right, node_deleted)` — a deleted parent marks its
   children as roots.
7. Return `None` if the node was deleted, otherwise the (mutated) node.
8. Call `dfs(root, True)` and return `forest`.

**Worked Example (Dry Run):**
```
Tree:          1
             /   \
            2     3
           / \   / \
          4   5 6   7     to_delete = [3, 5]

DFS trace (post-order, showing is_root decisions):
  Node 4: survives, parent 2 kept → is_root=False → not added.
  Node 5: DELETED, children None → returns None.
  Node 2: survives (is_root from root 1 was False), its right child is now None.
  Node 6, 7: survive, parent 3 deleted → is_root=True → added to forest.
  Node 3: DELETED → returns None; root 1's right link becomes None.
  Root 1: survives, is_root=True → added to forest.

Answer: forest = [1 (with children 2, 4), 6, 7]
```

**Code:**

```python
def del_nodes(root: TreeNode, to_delete: list) -> list:
    """Return the roots of the trees remaining after deleting the given values."""
    to_delete = set(to_delete)          # O(1) membership checks
    forest = []                          # roots of the surviving trees

    def dfs(node, is_root):
        if not node:
            return None
        node_deleted = node.val in to_delete
        # A surviving node whose parent was deleted (or the original root)
        # starts a new tree in the forest.
        if is_root and not node_deleted:
            forest.append(node)
        # Children inherit "am I a root?" from whether THIS node was deleted:
        # if the parent is gone, each kept child becomes a root.
        node.left = dfs(node.left, node_deleted)
        node.right = dfs(node.right, node_deleted)
        return None if node_deleted else node   # delete the node by un-linking it

    dfs(root, True)
    return forest

# Time: O(n), Space: O(h)
```

**Complexity:**
- Time: O(n) — every node visited once; set lookups are O(1).
- Space: O(h) — recursion stack (plus O(n) output storage for the forest).

**Common Mistakes & Edge Cases:**
- Deleting nothing: the forest is `[root]`.
- Deleting every node: the forest is `[]`.
- Using a list instead of a set for `to_delete` turns each lookup into O(n),
  making the whole algorithm O(n²).
- Forgetting that `node.left` / `node.right` must be reassigned to the DFS
  results — otherwise deleted subtrees are still reachable through old links.
- Passing `node_deleted` as the children's `is_root` (not the original
  `is_root`) — this is the whole mechanism for finding new roots.

---

### Most Frequent Subtree Sum

**Problem Explanation:**
For each node of a binary tree, its *subtree sum* is the sum of the node's value
and all values in its subtree (every descendant). Compute every node's subtree
sum, then find which value(s) occur most frequently. Return a list of the
subtree sums that tie for the maximum frequency (the order does not matter).

**State Definition:**
`subtree_sum(node)` = the sum of all node values in `node`'s subtree. A global
hashmap `freq` counts how many nodes produced each sum, and `max_freq` tracks
the largest count seen so far.

**Recurrence Relation:**
```
subtree_sum(node) = node.val + subtree_sum(left) + subtree_sum(right)
freq[subtree_sum(node)] += 1
max_freq = max(max_freq, freq[subtree_sum(node)])
```
Plain-English reason: a subtree sum is just the node's own value plus the
already-computed sums of its children's subtrees — a perfect post-order
accumulation, and every time a sum is computed we record it in the frequency
table.

**Base Cases:**
- `None` node returns `0` (an empty subtree contributes nothing).

**Intuition (Why This Works):**
The subtree sums have an immediate bottom-up dependency — each one is built from
its children's sums — so post-order DFS computes every sum in one pass with no
memoization. The DP-like accumulation and the frequency counting happen in the
same traversal; afterwards a single scan of the hashmap returns all values
tied at `max_freq`.

**Step-by-Step Procedure:**
1. Initialize `freq = {}` and `max_freq = 0`.
2. Define `subtree_sum(node)`; if `None`, return `0`.
3. Compute `total = node.val + subtree_sum(left) + subtree_sum(right)`.
4. Update `freq[total] += 1` (get-or-create with `.get`).
5. Update `max_freq = max(max_freq, freq[total])`.
6. Return `total` so the parent can accumulate it.
7. After the root call, return every sum `s` where `freq[s] == max_freq`.

**Worked Example (Dry Run):**
```
Tree:        5
           /   \
          2    -5

DFS trace (post-order):
  Node 2:  total = 2 + 0 + 0 = 2       freq={2:1},  max_freq=1
  Node -5: total = -5 + 0 + 0 = -5     freq={2:1, -5:1}, max_freq=1
  Root 5:  total = 5 + 2 + (-5) = 2    freq={2:2, -5:1}, max_freq=2

Answer: [2]   (subtree sum 2 occurs twice: node 2 and the whole tree)
```

**Code:**

```python
def most_frequent_subtree_sum(root) -> list:
    """Return all subtree sums that occur with the maximum frequency."""
    freq = {}                           # subtree sum -> how many nodes have it
    max_freq = 0

    def subtree_sum(node):
        nonlocal max_freq
        if not node:
            return 0                    # empty subtree contributes nothing
        # Post-order accumulation: sum = own value + both children's sums.
        total = node.val + subtree_sum(node.left) + subtree_sum(node.right)
        freq[total] = freq.get(total, 0) + 1   # count this node's subtree sum
        max_freq = max(max_freq, freq[total])
        return total                    # hand the sum up to the parent

    subtree_sum(root)
    # Collect every sum that reached the maximum frequency.
    return [s for s, f in freq.items() if f == max_freq]

# Time: O(n), Space: O(n)
```

**Complexity:**
- Time: O(n) — one traversal plus a final scan of the hashmap.
- Space: O(n) — the hashmap can hold up to n distinct sums, plus the recursion
  stack O(h).

**Common Mistakes & Edge Cases:**
- Empty tree: the function returns `[]` (there are no subtree sums); guard the
  root if you prefer `0` or `[0]`.
- Negative values are fine and often create ties (as in the example) — make sure
  the tie-breaking scan compares by frequency, not by value.
- Forgetting `freq.get(total, 0)` — a KeyError on the first occurrence.
- Single-node tree: answer is `[node.val]`.
- Very large sums can overflow 32-bit integers in other languages; in Python,
  arbitrary-precision ints handle them.

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
