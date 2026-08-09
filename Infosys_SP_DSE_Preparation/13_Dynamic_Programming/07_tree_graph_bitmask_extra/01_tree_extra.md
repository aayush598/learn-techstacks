# Tree DP — Extra Problems

Additional tree DP problems covering N-ary trees, BST properties, tree
coloring, LCA, and tree transformations. Problems already covered in the
main guide (Diameter of Binary Tree, Max Path Sum, House Robber III,
Vertex Cover, Independent Set, Path Sum III, Delete Nodes, Most Frequent
Subtree Sum, Binary Tree Cameras) are skipped here.

---

## 1. Diameter of N-ary Tree (LC #1522) — Medium

**🔗 Practice Link:** [1. Diameter of N-ary Tree](https://www.geeksforgeeks.org/diameter-n-ary-tree)

### Problem Explanation
Given an n-ary tree (each node can have any number of children), find the
diameter: the longest path between any two nodes in edges. Unlike a binary
tree where we compare left vs right, here we scan ALL children and keep the
top two heights.

### State Definition
`height(node)` = longest downward path (in edges) from `node` to a leaf.
Global `diameter` = max path bent at any node = `max1 + max2` (two tallest
child heights at that node).

### Recurrence Relation
```
height(node) = 0                                        (leaf)
             = 1 + max(height(child) for child in children)  (otherwise)
diameter     = max(diameter, max1 + max2)
```

### Base Cases
- Leaf returns `0`.
- Single-node tree: diameter = `0`.

### Intuition (Why This Works)
Post-order DFS computes children heights first. A path bending at a node
splits into exactly two branches, so only the top two child heights matter.
This generalizes binary-tree diameter to any arity.

### Step-by-Step Procedure
1. Initialize `diameter = 0`.
2. DFS post-order: for each child, get `ch = dfs(child) + 1`.
3. Maintain `max1` and `max2` (two largest `ch` values seen).
4. Update `diameter = max(diameter, max1 + max2)`.
5. Return `max1` to parent.

### Worked Example (Dry Run)
```
N-ary Tree:
        1
      / | \
     2  3  4
    /   |   \
   5    6    7
  /
 8

DFS (post-order):
  Node 8: leaf → h=0
  Node 5: child 8→h=1  max1=1,max2=0 → diam=1, return 1
  Node 2: child 5→h=2  max1=2,max2=0 → diam=2, return 2
  Node 6: leaf → h=0   Node 3: h=1     Node 7: leaf   Node 4: h=1
  Node 1: children give h=2,1,1 → max1=2,max2=1
          diameter = max(2, 2+1) = 3, return 2

Answer: 3  (path: 8→5→2→1→3→6, 3 edges)
```

### Code
```python
class Solution:
    def diameter(self, root: 'Node') -> int:
        self.diam = 0
        def height(node):
            if not node.children:
                return 0
            max1 = max2 = 0
            for child in node.children:
                ch = height(child) + 1
                if ch > max1:
                    max2, max1 = max1, ch
                elif ch > max2:
                    max2 = ch
            self.diam = max(self.diam, max1 + max2)
            return max1
        height(root)
        return self.diam
# Time: O(n), Space: O(h)
```

### Complexity
- Time: O(n), Space: O(h) recursion stack.

### Common Mistakes & Edge Cases
- Only checking first two children instead of scanning all for max1/max2.
- Forgetting `+1` when comparing child heights at parent.
- Single-node tree must return `0`.

---

## 2. Maximum Path Sum Between Two Leaf Nodes — Medium

**🔗 Practice Link:** [2. Maximum Path Sum Between Two Leaf Nodes — Medium](https://www.geeksforgeeks.org/find-maximum-path-sum-two-leaves-binary-tree)

### Problem Explanation
Given a binary tree with possibly negative values, find the maximum sum
path that MUST start and end at leaf nodes. If no leaf-to-leaf path exists
(single node), return root's value.

### State Definition
`leaf_path(node)` = max sum from `node` down to a leaf (return `-inf` if
no leaf below). Global `max_sum` updated at nodes with two valid paths.

### Recurrence Relation
```
leaf_path(node) = node.val                                      (leaf)
                = node.val + max(leaf_path(left), leaf_path(right))
max_sum = max(max_sum, left + node.val + right)
          only when BOTH children != -inf
```

### Base Cases
- `None` returns `-inf`. Leaf returns `node.val`.
- If `max_sum` stays `-inf`, return `root.val`.

### Intuition (Why This Works)
`-inf` for `None` prevents fake leaf paths from single-child nodes. Only
nodes where both subtrees contain leaves can form valid leaf-to-leaf paths.

### Step-by-Step Procedure
1. Init `max_sum = float('-inf')`.
2. DFS: if `None` return `-inf`; if leaf return `node.val`.
3. Get `left` and `right` from children.
4. If both valid, update `max_sum = max(max_sum, left+val+right)`.
5. Return `val + max(left, right)`.
6. After DFS return `max_sum` or `root.val` if unchanged.

### Worked Example (Dry Run)
```
Tree:      -10
          /   \
         9    20
             /  \
            15   7

  Node 9: leaf → 9    Node 15: →15    Node 7: →7
  Node 20: left=15,right=7 both valid
           max_sum=15+20+7=42, return 35
  Node -10: left=9,right=35 both valid
            max_sum=max(42,9-10+35)=42, return 25

Answer: 42 (path 15→20→7)
```

### Code
```python
class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        self.max_sum = float('-inf')
        def dfs(node):
            if not node:
                return float('-inf')
            if not node.left and not node.right:
                return node.val
            left, right = dfs(node.left), dfs(node.right)
            if left > float('-inf') and right > float('-inf'):
                self.max_sum = max(self.max_sum, left + node.val + right)
            return node.val + max(left, right)
        dfs(root)
        return self.max_sum if self.max_sum != float('-inf') else root.val
# Time: O(n), Space: O(h)
```

### Complexity
- Time: O(n), Space: O(h).

### Common Mistakes & Edge Cases
- Using `0` instead of `-inf` creates fake leaf paths.
- Updating max_sum with only one valid child.
- Single-node tree falls back to `root.val`.

---

## 3. House Robber IV (LC #2002) — Medium

**🔗 Practice Link:** [3. House Robber IV](https://leetcode.com/problems/house-robber-iv/)

### Problem Explanation
Houses in a CIRCLE. Cannot rob two adjacent houses. Since house 0 and
house n-1 are adjacent, we cannot rob both. Split into two linear
subproblems: `[0..n-2]` and `[1..n-1]`, take the max.

### State Definition
`dp[i]` = max money robbed from houses `0..i` in a linear arrangement.
Recurrence: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`.

### Recurrence Relation
```
dp[i] = max(dp[i-1], dp[i-2] + nums[i])
```
Linear robber applied twice with different ranges.

### Base Cases
- `n == 1`: return `nums[0]`. `n == 2`: return `max(nums)`.
- Linear base: `prev2=0, prev1=0`.

### Intuition (Why This Works)
The circular edge is the ONLY difference from linear House Robber. By
excluding one endpoint in each subproblem, we guarantee the circular
constraint. Both subproblems are independent.

### Step-by-Step Procedure
1. Handle `n<=2` directly.
2. Define `linear_rob(arr)` with O(1) space.
3. `opt1 = linear_rob(nums[:-1])` (exclude last).
4. `opt2 = linear_rob(nums[1:])` (exclude first).
5. Return `max(opt1, opt2)`.

### Worked Example (Dry Run)
```
nums = [2,3,2]  (circular: 0 adj to 2)
  opt1: linear_rob([2,3]) → max(2,3)=3
  opt2: linear_rob([3,2]) → max(3,2)=3
  Answer: 3

nums = [1,2,3,1]
  opt1: linear_rob([1,2,3]) → dp:1,2,4 → 4
  opt2: linear_rob([2,3,1]) → dp:2,3,4 → 4
  Answer: 4 (rob houses 1 and 3)
```

### Code
```python
class Solution:
    def rob(self, nums: list) -> int:
        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums)
        def linear_rob(arr):
            prev2, prev1 = 0, 0
            for val in arr:
                prev2, prev1 = prev1, max(prev1, prev2 + val)
            return prev1
        return max(linear_rob(nums[:-1]), linear_rob(nums[1:]))
# Time: O(n), Space: O(1)
```

### Complexity
- Time: O(n), Space: O(1).

### Common Mistakes & Edge Cases
- Forgetting circular constraint and running linear robber on full array.
- Not handling `n == 1` or `n == 2`.
- All zeros: answer is `0`.

---

## 4. Minimum Vertex Cover — Weighted (LC #1155 variant) — Hard

**🔗 Practice Link:** [4. Minimum Vertex Cover — Weighted](https://www.geeksforgeeks.org/vertex-cover-problem-set-2-dynamic-programming-solution-tree)

### Problem Explanation
Binary tree where each node has a cost. Find minimum total cost set of
nodes such that every edge has at least one endpoint selected. Unlike the
unweighted version (count nodes), here each node has a different cost.

### State Definition
`dfs(node)` returns `(cost_cover, cost_skip)`:
- `cost_cover` = min cost covering subtree when node IS selected.
- `cost_skip` = min cost when node is NOT selected.

### Recurrence Relation
```
cost_cover = node.val + min(left) + min(right)
cost_skip  = left[0] + right[0]
```
Skipped node forces children into cover state (they must cover the edge).

### Base Cases
- `None` returns `(0, 0)`.
- Leaf: cover=`val`, skip=`0`.

### Intuition (Why This Works)
Weighted variant: same structural logic as unweighted but with costs.
The forced-choice at skipped nodes (children MUST cover) is unchanged.

### Step-by-Step Procedure
1. DFS returns `(0,0)` for `None`.
2. Recurse left/right.
3. `cover = val + min(left) + min(right)`.
4. `skip = left[0] + right[0]`.
5. Return `(cover, skip)`. Answer = `min(dfs(root))`.

### Worked Example (Dry Run)
```
Tree:       3
          /   \
         1     2
        / \     \
       4   5     3

  Node 4:(4,0)  Node 5:(5,0)
  Node 1:cover=1+0+0=1; skip=4+5=9 → (1,9)
  Node 3:(3,0)
  Node 2:cover=2+0=2; skip=3 → (2,3)
  Root: cover=3+1+2=6; skip=9+3=12 → (6,12)

Answer: 6 (select nodes 3,1,2; cost 6)
```

### Code
```python
class Solution:
    def minVertexCover(self, root: TreeNode) -> int:
        def dfs(node):
            if not node:
                return (0, 0)
            left = dfs(node.left)
            right = dfs(node.right)
            cover = node.val + min(left) + min(right)
            skip = left[0] + right[0]
            return (cover, skip)
        return min(dfs(root)) if root else 0
# Time: O(n), Space: O(h)
```

### Complexity
- Time: O(n), Space: O(h).

### Common Mistakes & Edge Cases
- Mixing up forced index: skip forces `left[0]`, not `left[1]`.
- Single node with no edges: cost `0` (no edges to cover).
- All costs `1` reduces to unweighted vertex cover.

---

## 5. Maximum Weight Independent Set in Tree — Hard

**🔗 Practice Link:** [5. Maximum Weight Independent Set in Tree — Hard](https://www.geeksforgeeks.org/maximum-sum-nodes-binary-tree-no-two-adjacent)

### Problem Explanation
Binary tree with weighted nodes. Find max weight set of non-adjacent
nodes (no parent-child pair both selected). Weighted version of counting
max independent set size.

### State Definition
`dfs(node)` returns `(take, skip)`:
- `take` = max weight when node IS in the set.
- `skip` = max weight when node is NOT in the set.

### Recurrence Relation
```
take = node.val + skip_left + skip_right
skip = max(left) + max(right)
```

### Base Cases
- `None` returns `(0, 0)`.
- Leaf returns `(val, 0)`.

### Intuition (Why This Works)
Taking a node forces children out (adjacency). Skipping lets children
choose freely. The two-state tuple carries exactly the info parents need.

### Step-by-Step Procedure
1. DFS returns `(0,0)` for `None`.
2. Recurse left/right.
3. `take = val + left[1] + right[1]`.
4. `skip = max(left) + max(right)`.
5. Return `(take, skip)`. Answer = `max(dfs(root))`.

### Worked Example (Dry Run)
```
Tree:       10
          /    \
         5      15
        / \       \
       3   7       8

  Node 3:(3,0)  Node 7:(7,0)
  Node 5:take=5+0+0=5; skip=max(3,0)+max(7,0)=10 → (5,10)
  Node 8:(8,0)
  Node 15:take=15; skip=0 → (15,0)
  Root 10:take=10+10+0=20; skip=max(5,10)+max(15,0)=25 → (20,25)

Answer: max(20,25) = 25 (set {5,7,15})
```

### Code
```python
class Solution:
    def maxWeightIndependentSet(self, root: TreeNode) -> int:
        def dfs(node):
            if not node:
                return (0, 0)
            left = dfs(node.left)
            right = dfs(node.right)
            take = node.val + left[1] + right[1]
            skip = max(left) + max(right)
            return (take, skip)
        return max(dfs(root)) if root else 0
# Time: O(n), Space: O(h)
```

### Complexity
- Time: O(n), Space: O(h).

### Common Mistakes & Edge Cases
- Confusing take/skip with vertex cover (mirrored logic).
- Single node returns its weight, not `0`.
- All negative: answer `0` if empty set allowed.

---

## 6. Tree Coloring (LC #1443) — Medium

**🔗 Practice Link:** [6. Tree Coloring](https://www.geeksforgeeks.org/m-coloring-problem-backtracking-5)

### Problem Explanation
Given a binary tree with `n` nodes and `m` colors, color every node such
that no parent and child share the same color. Count the total number of
valid colorings modulo 10^9+7. For the root, all `m` colors are available;
for each other node, `m-1` colors are available (different from parent).

### State Definition
`countWays(node, parent_color)` = number of valid colorings of the subtree
rooted at `node` given the parent's color. Equivalently, for each node the
answer depends only on whether the parent uses one of the `m` colors.

### Recurrence Relation
```
countWays(node) = (m-1) * product(countWays(child) for each child)
```
Each child independently picks any color except the parent's. The root has
`m` choices, and each other node has `m-1` choices (regardless of which
specific parent color, since only exclusion matters).

### Base Cases
- Leaf: returns `1` (one valid coloring for a leaf).
- `None` node: returns `1`.

### Intuition (Why This Works)
The constraint "parent != child" means each child independently excludes
exactly one color. The specific parent color doesn't matter — only the
count `m-1` of available colors matters. So the total is:
`m * (m-1)^(n-1)` for a tree (since every non-root node has exactly one
parent constraint).

### Step-by-Step Procedure
1. If `root` is `None`, return `0`.
2. Use DFS to count nodes (or apply formula directly).
3. Answer = `m * pow(m-1, n-1, MOD) % MOD`.
4. Alternatively, DFS multiplying `(m-1)` per edge.

### Worked Example (Dry Run)
```
Tree:     1
        /   \
       2     3

n=3 nodes, m=3 colors.
Root: 3 choices. Node 2: 2 choices (≠parent). Node 3: 2 choices (≠parent).
Answer = 3 * 2 * 2 = 12 mod (10^9+7) = 12

Verification: root=color0, node2∈{1,2}, node3∈{1,2} → 1*2*2=4 per root color.
3 root colors × 4 = 12.
```

### Code
```python
class Solution:
    def numberOfWays(self, root: TreeNode, m: int) -> int:
        MOD = 10**9 + 7
        # For a tree: m choices for root, (m-1) for each of n-1 other nodes.
        # Formula: m * (m-1)^(n-1)
        def count_nodes(node):
            if not node:
                return 0
            return 1 + count_nodes(node.left) + count_nodes(node.right)
        n = count_nodes(root)
        if n == 0:
            return 0
        return m * pow(m - 1, n - 1, MOD) % MOD
# Time: O(n), Space: O(h)
```

### Complexity
- Time: O(n), Space: O(h).

### Common Mistakes & Edge Cases
- Forgetting modular exponentiation for large trees.
- `n == 0`: return `0`, not `1`.
- `m == 1` and `n > 1`: impossible, return `0`.

---

## 7. Maximum Sum BST in Binary Tree (LC #1373) — Hard

**🔗 Practice Link:** [7. Maximum Sum BST in Binary Tree](https://leetcode.com/problems/maximum-sum-bst-in-binary-tree/)

### Problem Explanation
Given a binary tree, find the maximum sum of all nodes in a subtree that
is also a valid BST (Binary Search Tree). An empty tree is a valid BST
with sum `0`. Return the max sum.

### State Definition
`dfs(node)` returns `(is_bst, subtree_sum, min_val, max_val)`:
- `is_bst` = whether the subtree rooted at `node` is a valid BST.
- `subtree_sum` = sum of all values in the subtree.
- `min_val` / `max_val` = min and max values in the subtree.

### Recurrence Relation
```
Left subtree must be BST, right subtree must be BST.
Left max < node.val < Right min.
subtree_sum = left_sum + right_sum + node.val
```
If all conditions met, this subtree is a BST and we update global max.

### Base Cases
- `None` returns `(True, 0, inf, -inf)` — empty tree is a valid BST.

### Intuition (Why This Works)
Post-order DFS computes children's BST status and range first. We check
the BST property (left max < node < right min) at each node. If valid,
the subtree sum is a candidate for the global answer.

### Step-by-Step Procedure
1. Init `max_sum = 0`.
2. DFS returns `(is_bst, sum, min_val, max_val)`.
3. For `None`: return `(True, 0, inf, -inf)`.
4. Get left and right results.
5. If `left.is_bst and right.is_bst and left.max < node.val < right.min`:
   update `max_sum = max(max_sum, left.sum + right.sum + val)`.
   Return `(True, sum, left.min, right.max)`.
6. Otherwise return `(False, 0, 0, 0)`.

### Worked Example (Dry Run)
```
Tree:       1
          /   \
         4     3
        / \   / \
       2   4 2   5

DFS post-order:
  Node 2 (left-left): BST, sum=2, min=2, max=2
  Node 4 (left-right leaf): BST, sum=4, min=4, max=4
  Node 4 (left): left.max(2) < 4 < right.min(4)? No (4<4 false).
    NOT BST.
  Node 2 (right-left): BST, sum=2, min=2, max=2
  Node 5: BST, sum=5, min=5, max=5
  Node 3: left.max(2) < 3 < right.min(5)? Yes.
    BST, sum=2+5+3=10, max_sum=10
  Root 1: left.is_bst=False → NOT BST.

Answer: 10 (subtree rooted at 3: nodes 2,3,5)
```

### Code
```python
class Solution:
    def maxSumBST(self, root: TreeNode) -> int:
        self.max_sum = 0
        def dfs(node):
            if not node:
                return (True, 0, float('inf'), float('-inf'))
            lb, ls, lmin, lmax = dfs(node.left)
            rb, rs, rmin, rmax = dfs(node.right)
            if lb and rb and lmax < node.val < rmin:
                total = ls + rs + node.val
                self.max_sum = max(self.max_sum, total)
                return (True, total, min(lmin, node.val), max(rmax, node.val))
            return (False, 0, 0, 0)
        dfs(root)
        return self.max_sum
# Time: O(n), Space: O(h)
```

### Complexity
- Time: O(n), Space: O(h).

### Common Mistakes & Edge Cases
- Off-by-one in BST check: use strict `<` not `<=`.
- All negative values: answer is `0` (empty BST).
- Single node: always a BST with sum = `node.val`.

---

## 8. Count Good Nodes in Binary Tree (LC #1448) — Medium

**🔗 Practice Link:** [8. Count Good Nodes in Binary Tree](https://leetcode.com/problems/count-good-nodes-in-binary-tree/)

### Problem Explanation
A node is "good" if no node on the path from the root to it has a value
greater than or equal to it. Count the number of good nodes.

### State Definition
`dfs(node, max_so_far)` = count of good nodes in `node`'s subtree given
that the maximum value on the path from root to `node`'s parent is
`max_so_far`.

### Recurrence Relation
```
is_good = (node.val >= max_so_far)
new_max = max(max_so_far, node.val)
count = is_good + dfs(left, new_max) + dfs(right, new_max)
```

### Base Cases
- `None` returns `0`.
- Root: `dfs(root, -inf)` (no ancestor to beat).

### Intuition (Why This Works)
We pass down the running maximum. At each node, if the node's value meets
or exceeds the running max, it is good. Then we update the running max for
children and recurse.

### Step-by-Step Procedure
1. Define `dfs(node, max_so_far)`.
2. If `None`, return `0`.
3. Check `good = 1 if node.val >= max_so_far else 0`.
4. `new_max = max(max_so_far, node.val)`.
5. Return `good + dfs(left, new_max) + dfs(right, new_max)`.
6. Call `dfs(root, float('-inf'))`.

### Worked Example (Dry Run)
```
Tree:       3
          /   \
         1     4
        /     / \
       3     1   5

  dfs(3, -inf): good=1, max=3 → 1+dfs(1,3)+dfs(4,3)
  dfs(1, 3): good=0, max=3 → 0+dfs(3,3)+0
  dfs(3, 3): good=1, max=3 → 1+0+0 = 1
  dfs(4, 3): good=1, max=4 → 1+dfs(1,4)+dfs(5,4)
  dfs(1, 4): good=0 → 0    dfs(5, 4): good=1 → 1
  Root: 1 + (0+1) + (1+0+1) = 1+1+2 = 4

Answer: 4 (nodes 3, 3, 4, 5 are good)
```

### Code
```python
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node, max_so_far):
            if not node:
                return 0
            good = 1 if node.val >= max_so_far else 0
            new_max = max(max_so_far, node.val)
            return good + dfs(node.left, new_max) + dfs(node.right, new_max)
        return dfs(root, float('-inf'))
# Time: O(n), Space: O(h)
```

### Complexity
- Time: O(n), Space: O(h).

### Common Mistakes & Edge Cases
- Using `>` instead of `>=` for good node check.
- Root is always good (max_so_far starts at `-inf`).
- All equal values: every node is good.

---

## 9. Lowest Common Ancestor of a Binary Tree (LC #236) — Medium

**🔗 Practice Link:** [9. Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)

### Problem Explanation
Given a binary tree and two nodes `p` and `q`, find their lowest common
ancestor (LCA): the deepest node that is an ancestor of both `p` and `q`.
A node can be an ancestor of itself.

### State Definition
`dfs(node)` returns the LCA subtree result: if `node` is `p` or `q`,
return `node`. Otherwise, recurse left and right. If both sides return
non-null, `node` is the LCA. If only one side returns non-null, propagate
it up.

### Recurrence Relation
```
if node is None, p, or q: return node
left  = dfs(left)
right = dfs(right)
if left and right: return node    (split point: p and q in different subtrees)
return left or right              (propagate whichever is non-null)
```

### Base Cases
- `None` returns `None`.
- Node equals `p` or `q`: return `node`.

### Intuition (Why This Works)
Post-order DFS ensures children are processed first. The first node where
both left and right subtrees return non-null is exactly the LCA — it is
the deepest point where the paths to `p` and `q` diverge.

### Step-by-Step Procedure
1. DFS post-order.
2. If `node` is `None`, `p`, or `q`, return `node`.
3. Recurse left and right.
4. If both return non-null, `node` is LCA — return it.
5. Return whichever side is non-null (or `None`).

### Worked Example (Dry Run)
```
Tree:       3
          /   \
         5     1
        / \   / \
       6   2 0   8
          / \
         7   4

p=5, q=1:
  DFS(6): not p/q → left=None,right=None → None
  DFS(7): not p/q → None
  DFS(4): not p/q → None
  DFS(2): not p/q → left=7→None, right=4→None → None
  DFS(5): IS p → return 5
  DFS(0): None
  DFS(8): None
  DFS(1): IS q → return 1
  DFS(3): left=5, right=1 → both non-null → return 3 (LCA)

Answer: 3
```

### Code
```python
class Solution:
    def lowestCommonAncestor(self, root, p, q):
        # Returns the LCA of nodes p and q in the binary tree.
        if not root or root == p or root == q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root               # p and q split here: this is the LCA
        return left or right          # propagate whichever side found something
# Time: O(n), Space: O(h)
```

### Complexity
- Time: O(n), Space: O(h).

### Common Mistakes & Edge Cases
- `p` is ancestor of `q` (or vice versa): LCA is `p` (or `q`).
- `p == q`: LCA is `p` itself.
- Forgetting to check `root == p or root == q` before recursing.

---

## 10. Flatten Binary Tree to Linked List (LC #114) — Medium

**🔗 Practice Link:** [10. Flatten Binary Tree to Linked List](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/)

### Problem Explanation
Given a binary tree, flatten it to a right-skewed linked list in-place.
The preorder traversal order must be preserved: for every node, its left
child is `None` and its right child is the next node in preorder.

### State Definition
`dfs(node)` processes the tree in reverse preorder (right, left, node).
We maintain a global `prev` pointer to track the last node visited. Each
node's right is set to `prev` and left is set to `None`.

### Recurrence Relation
```
dfs(node.right)
dfs(node.left)
node.right = prev
node.left  = None
prev = node
```

### Base Cases
- `None` node: return.
- After full traversal, `prev` points to the last node in preorder.

### Intuition (Why This Works)
Reverse preorder (right-left-node) processes nodes from last to first.
Setting each node's right to the previously processed node builds the
linked list from tail to head. The in-place modification is safe because
we traverse right before left.

### Step-by-Step Procedure
1. Init `prev = None`.
2. Define `dfs(node)`: if `None`, return.
3. Recurse `dfs(node.right)`, then `dfs(node.left)`.
4. `node.right = prev`, `node.left = None`.
5. `prev = node`.

### Worked Example (Dry Run)
```
Tree:       1
          /   \
         2     5
        / \     \
       3   4     6

Reverse preorder: 6, 5, 4, 3, 2, 1

  dfs(1): → dfs(5) → dfs(6)
    dfs(6): right=None,left=None → node.right=None,prev=6
    dfs(5): right=6→already done → dfs(None) →
            node.right=6,node.left=None,prev=5
  dfs(1): → dfs(2) → dfs(4)
    dfs(4): node.right=5,node.left=None,prev=4
    dfs(3): node.right=4,node.left=None,prev=3
    dfs(2): node.right=3,node.left=None,prev=2
  dfs(1): node.right=2,node.left=None,prev=1

Result: 1→2→3→4→5→6 (right-linked list)
```

### Code
```python
class Solution:
    def flatten(self, root: TreeNode) -> None:
        # Flatten in-place to right-skewed linked list (preorder).
        self.prev = None
        def dfs(node):
            if not node:
                return
            dfs(node.right)            # process right first (reversed preorder)
            dfs(node.left)
            node.right = self.prev     # link to previously processed node
            node.left = None           # clear left child
            self.prev = node           # this node becomes the new "previous"
        dfs(root)
# Time: O(n), Space: O(h)
```

### Complexity
- Time: O(n), Space: O(h).

### Common Mistakes & Edge Cases
- Forgetting to set `node.left = None` — creates cycles.
- Processing left before right (gives reverse-preorder instead of preorder).
- Already flat tree: no changes needed.
- Single node: already flat.
