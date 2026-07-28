# 🌲 TREE PROBLEMS - COMPLETE PROBLEM BANK

## Infosys SP DSE Preparation | 35 Problems with Solutions

---

## TreeNode Class Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

---

# EASY PROBLEMS (1-10)

---

## Problem 1: Maximum Depth of Binary Tree

**Problem Statement:**
Given the root of a binary tree, return its maximum depth. A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

**Example:**
```
Input: [3,9,20,null,null,15,7]
Output: 3
```

**Approach:**
Use recursive DFS. The depth of a tree is 1 + max(depth of left subtree, depth of right subtree). Base case: if node is None, return 0.

```python
class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        left = self.maxDepth(root.left)
        right = self.maxDepth(root.right)
        return 1 + max(left, right)
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack, h = height of tree

**Trick/Tip:** This is the foundation of tree recursion. Every tree problem starts here. Remember: `1 + max(left, right)`.

**Visual Walkthrough:**
```
        3           depth(3) = 1 + max(depth(9), depth(20))
       / \          depth(9) = 1 + max(0, 0) = 1
      9  20         depth(20) = 1 + max(depth(15), depth(7))
        /  \        depth(15) = 1 + max(0, 0) = 1
       15   7       depth(7) = 1 + max(0, 0) = 1

Backtrack: depth(20) = 1 + max(1, 1) = 2
           depth(3) = 1 + max(1, 2) = 3 ✓
```

**Common Mistakes:**
- Forgetting base case (node is None → return 0)
- Off-by-one: depth is number of nodes, not edges
- Using `+1` for each level correctly

**Edge Cases:**
- Empty tree → return 0
- Single node → return 1
- Skewed tree (all left or all right) → return n

**Pattern Recognition:**
**Tree DFS Pattern**: Recursive post-order traversal. Process left subtree, process right subtree, combine results at current node. This is the template for most tree height/depth problems.

---

## Problem 2: Same Tree

**Problem Statement:**
Given the roots of two binary trees p and q, write a function to check if they are the same or not. Two binary trees are considered the same if they are structurally identical and the nodes have the same values.

**Problem Explanation in Simple Words:**
You have two trees. Are they exactly identical? They must have the same shape (structure) AND every corresponding node must have the same value. Think of taking a photograph of each tree and overlaying them — every branch and every leaf must match perfectly.

**Example Walkthrough:**
```
Tree 1:         Tree 2:
    1              1
   / \            / \
  2   3          2   3
```
Both structurally same and values match → True ✅

```
Tree 1:         Tree 2:
    1              1
   /                \
  2                  2
```
Structure differs (left vs right child) → False ❌

**Detailed Approach with Algorithm Steps:**
1. **Base Case 1 — Both Empty:** If both p and q are None, they are identical → return True.
2. **Base Case 2 — One Empty:** If exactly one of them is None (not both), structure differs → return False.
3. **Value Check:** If both are non-None but their values differ → return False.
4. **Recursive Check:** Recurse on left children AND right children. Both must return True.
5. **Return:** Combine results with AND — both left and right subtrees must match.

**Visual Tree Comparison:**
```
Tree p:            Tree q:
     1                 1
    / \               / \
   2   3             2   3
  /                 /
 4                 4

compare(1, 1) → val match → compare(2,2) AND compare(3,3)
  compare(2,2) → val match → compare(4,4) AND compare(None,None)
    compare(4,4) → val match → compare(None,None) AND compare(None,None) → True
    compare(None,None) → True ✅
  compare(3,3) → val match → compare(None,None) AND compare(None,None) → True ✅
Result: True ✅
```

**Step-by-Step Trace with Input `p=[1,2,3], q=[1,2,3]`:**
```
Step 1: isSameTree(p=1, q=1) → both non-None, val(1)==val(1) ✓
  Step 2: isSameTree(p=2, q=2) → both non-None, val(2)==val(2) ✓
    Step 3: isSameTree(None, None) → both None → True ✅
    Step 4: isSameTree(None, None) → both None → True ✅
  Step 5: isSameTree(p=3, q=3) → both non-None, val(3)==val(3) ✓
    Step 6: isSameTree(None, None) → both None → True ✅
    Step 7: isSameTree(None, None) → both None → True ✅
Final: True AND True = True ✅
```

**Well-Commented Code:**
```python
class Solution:
    def isSameTree(self, p: TreeNode, q: TreeNode) -> bool:
        # Case 1: Both nodes are None -> structurally identical here
        if not p and not q:
            return True

        # Case 2: One is None, other isn't -> structure mismatch
        if not p or not q:
            return False

        # Case 3: Both exist but values differ
        if p.val != q.val:
            return False

        # Case 4: Recurse on left and right, both must match
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
```

**Complexity Analysis:**
- **Time:** O(n) — we visit each node in both trees exactly once
- **Space:** O(h) — recursion stack can grow up to the height of the tree

**Edge Cases with Examples:**
| Input | Expected | Reason |
|-------|----------|--------|
| `p=[], q=[]` | True | Both empty trees |
| `p=[1], q=[]` | False | One empty, one not |
| `p=[1,2], q=[1,null,2]` | False | Structure differs (left vs right) |
| `p=[1,2,1], q=[1,1,2]` | False | Values in different positions |

**Common Mistakes:**
- ❌ Checking `p.val == q.val` without first checking that both p and q are non-None
- ❌ Using `or` instead of `and` when combining recursive calls
- ❌ Forgetting to check one-None case separately
- ❌ Not recursing on both left and right children

**Pattern Recognition Hints:**
- **Mirror Problem:** This same logic is used in "Subtree of Another Tree" (Problem 4)
- **Recursive Checks Pattern:** Any problem requiring structural comparison uses this pattern
- **Short-circuit Evaluation:** Python's `and` will stop evaluating as soon as one side returns False

---

## Problem 3: Invert/Flip Binary Tree

**Problem Statement:**
Given the root of a binary tree, invert the tree, and return its root. Inverting means swapping left and right children of every node.

**Problem Explanation in Simple Words:**
Take a mirror image of the tree. Every node's left child becomes its right child, and vice versa. If you were looking at the tree in a mirror, this is what you'd see. The entire tree is flipped horizontally.

**Example Walkthrough:**
```
Original:
     4
   /   \
  2     7
 / \   / \
1   3 6   9

Inverted:
     4
   /   \
  7     2
 / \   / \
9   6 3   1
```
Every node's children are swapped — the tree is mirrored.

**Detailed Approach with Algorithm Steps:**
1. **Base Case:** If the current node is None, return None (nothing to invert).
2. **Swap:** Exchange the left and right child pointers of the current node.
3. **Recurse Left:** Recursively invert the left subtree (which was originally the right subtree).
4. **Recurse Right:** Recursively invert the right subtree (which was originally the left subtree).
5. **Return:** Return the current node (which now has inverted children).

**Visual Tree Diagram:**
```
Before inversion:
       4
     /   \
    2     7
   / \   / \
  1   3 6   9

After swapping children at each node:
       4
     /   \
    7     2
   / \   / \
  9   6 3   1

Step-by-step at root(4):
  original left=2, right=7
  swap → left=7, right=2
  recurse on left(7): swap 6↔9
  recurse on right(2): swap 1↔3
```

**Step-by-Step Trace with Input `[4,2,7,1,3,6,9]`:**
```
Step 1: invertTree(4) → swap left(2)↔right(7)
  Step 2: invertTree(7) → swap left(6)↔right(9)
    Step 3: invertTree(9) → no children, return 9
    Step 4: invertTree(6) → no children, return 6
  Step 5: invertTree(2) → swap left(1)↔right(3)
    Step 6: invertTree(3) → no children, return 3
    Step 7: invertTree(1) → no children, return 1
  Return 4 (fully inverted)
```

**Well-Commented Code:**
```python
class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:
        # Base case: empty node has nothing to invert
        if not root:
            return None

        # Swap left and right children using Python's tuple swap
        root.left, root.right = root.right, root.left

        # Recursively invert the left and right subtrees
        self.invertTree(root.left)
        self.invertTree(root.right)

        # Return the current node with inverted subtree
        return root
```

**Complexity Analysis:**
- **Time:** O(n) — every node is visited exactly once
- **Space:** O(h) — recursion stack depth equals tree height

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[]` | `[]` | Empty tree returns None |
| `[1]` | `[1]` | Single node has no children to swap |
| `[1,2]` | `[1,null,2]` | Single child moves from left to right |
| `[1,null,2]` | `[1,2]` | Single child moves from right to left |

**Common Mistakes:**
- ❌ Reversing value arrays instead of swapping children — children are node references, not values
- ❌ Using a temporary variable incorrectly: `temp = root.left; root.left = root.right; root.right = temp` — works but tuple swap is cleaner
- ❌ Forgetting to return the root after inversion
- ❌ Only swapping one level instead of recursing through the entire tree

**Pattern Recognition Hints:**
- **Symmetry Pattern:** Inverting a tree is the first step in checking if a tree is symmetric (Problem 7 in Batch 2)
- **Post-order Variant:** You could also swap after processing children — same result!
- **BFS Alternative:** Use a queue, swap each node's children as you pop it from the queue

---

## Problem 4: Subtree of Another Tree

**Problem Statement:**
Given the roots of two binary trees root and subRoot, return true if there is a subtree of root with the same structure and node values as subRoot. A subtree is a tree consisting of a node in root and all of its descendants.

**Problem Explanation in Simple Words:**
Imagine you have a big tree (root) and a small tree (subRoot). Does the big tree contain the small tree as a complete branch somewhere? The small tree must match exactly — same shape AND same values — starting from some node in the big tree down to the leaves.

**Example Walkthrough:**
```
root = [3,4,5,1,2]          subRoot = [4,1,2]
    3
   / \
  4   5
 / \
1   2

Does root contain [4,1,2] as a subtree?
  → Yes! Node 4 has left=1, right=2, matching subRoot exactly ✅
```

**Detailed Approach with Algorithm Steps:**
1. **Base Case:** If root is None, we've exhausted the big tree → return False.
2. **Check Current Node:** Use `isSameTree()` to check if the tree rooted at current node matches subRoot exactly.
3. **Recurse Left:** If no match at current node, check the left subtree.
4. **Recurse Right:** If no match in left, check the right subtree.
5. **Helper — isSameTree(p, q):**
   - If both None → True (both empty)
   - If one None → False (structural mismatch)
   - If values differ → False
   - Recurse on left+right children

**Visual Tree Diagram:**
```
Big Tree (root):
     3
   /   \
  4     5
 / \
1   2

Subtree to find (subRoot):
  4
 / \
1   2

Check at root=3: isSameTree(3, 4)? → False (3≠4)
Check left: isSameTree(4, 4)? → True (4=4) → Check children
  isSameTree(1,1)? → True
  isSameTree(2,2)? → True
  → Match found! Return True ✅
```

**Step-by-Step Trace:**
```
Input: root=[3,4,5,1,2], subRoot=[4,1,2]

isSubtree(root=3, subRoot=4):
  isSameTree(3, 4)? 3≠4 → False
  isSubtree(root=4, subRoot=4):
    isSameTree(4, 4)? 4=4 → check children
      isSameTree(1, 1)? 1=1 → check children
        isSameTree(None, None)? True
        isSameTree(None, None)? True
      isSameTree(2, 2)? 2=2 → check children
        isSameTree(None, None)? True
        isSameTree(None, None)? True
      → True ✅
    → True ✅
  → True ✅
```

**Well-Commented Code:**
```python
class Solution:
    def isSubtree(self, root: TreeNode, subRoot: TreeNode) -> bool:
        # Base case: we've reached a leaf's child without finding a match
        if not root:
            return False

        # Check if tree starting at this node matches subRoot
        if self.isSameTree(root, subRoot):
            return True

        # No match here — check left and right subtrees
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)

    def isSameTree(self, p: TreeNode, q: TreeNode) -> bool:
        # Both empty — structurally identical at this point
        if not p and not q:
            return True

        # One empty, one not — structure mismatch
        if not p or not q:
            return False

        # Values must match
        if p.val != q.val:
            return False

        # Recurse on children — both must match
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
```

**Complexity Analysis:**
- **Time:** O(m × n) — worst case, for each of m nodes in root, we call isSameTree which visits n nodes in subRoot
- **Space:** O(h) — recursion stack for both functions

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `root=[], subRoot=[]` | True | Empty tree is subtree of empty tree |
| `root=[1], subRoot=[]` | True | Empty tree is subtree of any tree |
| `root=[1], subRoot=[2]` | False | Value mismatch |
| `root=[3,4,5,1,2], subRoot=[4,1]` | False | Partial match — 4→1→null vs 4→1→2 structure mismatch |
| `root=[1,1], subRoot=[1]` | True | Root itself matches, but also left child might match |

**Common Mistakes:**
- ❌ Not handling the case where subRoot is None (empty subtree is always present)
- ❌ Checking only the root node and not recursing through the entire tree
- ❌ Using `isSameTree(root.left, subRoot.left)` instead of `isSubtree(root.left, subRoot)`
- ❌ Confusing subtree with subarray — subtree must include ALL descendants of a node

**Pattern Recognition Hints:**
- **Problem Decomposition:** Break into "find candidate root" + "verify identical trees"
- **Optimization:** Can be optimized to O(m+n) using tree serialization (Problem 17)
- **Hash-based:** Serialize both trees and use string matching (KMP) for O(m+n)
- **Recursive Traversal Pattern:** Used whenever you need to "check condition on every node"

---

## Problem 5: Diameter of Binary Tree

**Problem Statement:**
Given the root of a binary tree, return the length of the diameter of the tree. The diameter is the length of the longest path between any two nodes. This path may or may not pass through the root.

**Example:**
```
Input: [1,2,3,4,5]
Output: 3 (path: 4 -> 2 -> 1 -> 3)
```

**Approach:**
At each node, the longest path passing through it = height of left subtree + height of right subtree. Track the maximum across all nodes. Use a global variable or pass by reference.

```python
class Solution:
    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        self.diameter = 0
        
        def height(node):
            if not node:
                return 0
            left = height(node.left)
            right = height(node.right)
            self.diameter = max(self.diameter, left + right)
            return 1 + max(left, right)
        
        height(root)
        return self.diameter
```

**Complexity:**
- Time: O(n) - single pass computing heights
- Space: O(h) - recursion stack

**Trick/Tip:** Diameter at any node = left_height + right_height. Update global max during height computation. Don't confuse diameter (edges) with depth (nodes).

---

## Problem 6: Balanced Binary Tree

**Problem Statement:**
Given a binary tree, determine if it is height-balanced. A height-balanced tree is one where the depth of the two subtrees of every node never differs by more than one.

**Example:**
```
Input: [1,2,2,3,3,null,null,4,4]
Output: False
```

**Approach:**
Use a recursive approach that returns the height, but returns -1 if the subtree is unbalanced. This avoids recalculating heights multiple times.

```python
class Solution:
    def isBalanced(self, root: TreeNode) -> bool:
        def check(node):
            if not node:
                return 0
            left = check(node.left)
            if left == -1:
                return -1
            right = check(node.right)
            if right == -1:
                return -1
            if abs(left - right) > 1:
                return -1
            return 1 + max(left, right)
        
        return check(root) != -1
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** Return -1 as a sentinel for "unbalanced". This makes the solution O(n) instead of O(n²) because we don't recalculate heights.

---

## Problem 7: Minimum Depth of Binary Tree

**Problem Statement:**
Given a binary tree, find its minimum depth. The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

**Example:**
```
Input: [3,9,20,null,null,15,7]
Output: 2
```

**Approach:**
Use BFS (level order traversal). The first leaf node we encounter gives us the minimum depth. BFS guarantees shortest path.

```python
from collections import deque

class Solution:
    def minDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        queue = deque([(root, 1)])
        while queue:
            node, depth = queue.popleft()
            if not node.left and not node.right:
                return depth
            if node.left:
                queue.append((node.left, depth + 1))
            if node.right:
                queue.append((node.right, depth + 1))
        return 0
```

**Complexity:**
- Time: O(n) - worst case visit all nodes
- Space: O(w) - w = max width of tree

**Trick/Tip:** Don't use DFS for minimum depth — it doesn't guarantee shortest path. BFS finds the nearest leaf first.

---

## Problem 8: Path Sum

**Problem Statement:**
Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.

**Example:**
```
Input: root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
Output: True (5 -> 4 -> 11 -> 2 = 22)
```

**Approach:**
Use DFS. At each node, subtract the node's value from the remaining sum. When we reach a leaf, check if the remaining sum is 0.

```python
class Solution:
    def hasPathSum(self, root: TreeNode, targetSum: int) -> bool:
        if not root:
            return False
        if not root.left and not root.right:
            return root.val == targetSum
        remaining = targetSum - root.val
        return self.hasPathSum(root.left, remaining) or self.hasPathSum(root.right, remaining)
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** Only check at leaf nodes (both children None). The path must be root-to-leaf, not root-to-any node.

---

## Problem 9: Merge Two Binary Trees

**Problem Statement:**
Given two binary trees, merge them into a new binary tree. If two nodes overlap, sum their values. Otherwise, use the non-null node.

**Problem Explanation in Simple Words:**
You have two trees placed on top of each other. Where they overlap (both have a node at the same position), add the values together to get the new node's value. Where only one tree has a node, just use that node directly. The result is a completely new merged tree.

**Example Walkthrough:**
```
Tree 1:        Tree 2:        Merged:
     1           2              3
    / \         / \            / \
   3   2       1   3          4   5
  /             \   \        / \   \
 5               4   7      5   4   7

Node-by-node merge:
  - root: 1 + 2 = 3
  - left: 3 + 1 = 4
  - right: 2 + 3 = 5
  - left-left: 5 + None = 5
  - left-right: None + 4 = 4
  - right-right: None + 7 = 7
```

**Detailed Approach with Algorithm Steps:**
1. **Base Case — Both None:** If both root1 and root2 are None, return None.
2. **Base Case — One None:** If root1 is None, return root2 (take whatever tree2 has). If root2 is None, return root1.
3. **Both Exist:** Create a new TreeNode with value = root1.val + root2.val.
4. **Recurse Left:** Merge the left children of both trees.
5. **Recurse Right:** Merge the right children of both trees.
6. **Return:** The newly created merged node.

**Visual Tree Diagram:**
```
Position mapping during merge:
          (1+2)=3
         /       \
   (3+1)=4     (2+3)=5
    /     \        \
(5+None) (None+4) (None+7)
 =5        =4        =7
```

**Step-by-Step Trace:**
```
Input: root1=[1,3,2,5], root2=[2,1,3,null,null,null,4,null,7]

mergeTrees(1, 2): both exist → merged=3
  mergeTrees(3, 1): both exist → merged=4
    mergeTrees(5, None): root2 None → return 5
    mergeTrees(None, 4): root1 None → return 4
  mergeTrees(2, 3): both exist → merged=5
    mergeTrees(None, None): both None → return None
    mergeTrees(None, 7): root1 None → return 7

Result: [3,4,5,5,4,null,7]
```

**Well-Commented Code:**
```python
class Solution:
    def mergeTrees(self, root1: TreeNode, root2: TreeNode) -> TreeNode:
        # Case 1: Both nodes are None
        if not root1 and not root2:
            return None

        # Case 2: One node is None — use the other node
        if not root1:
            return root2
        if not root2:
            return root1

        # Case 3: Both nodes exist — sum values and merge children
        merged = TreeNode(root1.val + root2.val)
        merged.left = self.mergeTrees(root1.left, root2.left)
        merged.right = self.mergeTrees(root1.right, root2.right)

        return merged
```

**Complexity Analysis:**
- **Time:** O(min(m, n)) — we only visit nodes where at least one tree has a node, up to the size of the smaller tree
- **Space:** O(min(m, n)) — recursion stack depth equals the minimum tree height

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[1], [2]` | `[3]` | Simple sum at root |
| `[1], []` | `[1]` | One tree empty → return the other |
| `[], []` | `[]` | Both empty → None |
| `[1,2], [1,null,2]` | `[2,2,2]` | Merged with different structures |
| One is very deep, other is shallow | Merged tree shape follows the deeper tree | Non-null nodes from deeper tree fill in gaps |

**Common Mistakes:**
- ❌ Modifying the original trees instead of creating new nodes
- ❌ Not handling all three cases (both None, one None, both exist)
- ❌ Swapping the order of checks — check both None first, then one None, then both exist
- ❌ Forgetting that when one node is None, you can just return the other (no need to recurse deeper)

**Pattern Recognition Hints:**
- **Simultaneous Traversal Pattern:** Traverse two trees side-by-side — used in "Same Tree" (Problem 2) as well
- **Overlay Pattern:** Any problem where two trees are combined at corresponding positions
- **Short-circuit Returns:** When one is None, return the other — avoids unnecessary recursion

---

## Problem 10: Convert Sorted Array to Binary Search Tree

**Problem Statement:**
Given an integer array nums where the elements are sorted in ascending order, convert it to a height-balanced BST.

**Problem Explanation in Simple Words:**
You have a sorted list of numbers. Build a binary search tree where:
1. It's a BST (left < root < right for all nodes)
2. It's height-balanced (left and right subtrees differ in height by at most 1)

This is like building a phonebook from sorted names — pick the middle entry as the root, then recursively do the same for the left and right halves.

**Example Walkthrough:**
```
Input: [-10, -3, 0, 5, 9]

Pick middle (0) as root:
    0
   / \
[-10,-3] [5,9]

Left half [-10,-3]: pick -3 as root:
    0
   / \
 -3    ...
 /
-10

Right half [5,9]: pick 5 as root (actually 5, since floor of mid):
    0
   / \
 -3   5
 /     \
-10     9

Wait — let's use proper index math: mid = (0+4)//2 = 2, nums[2] = 0
Left: indices [0,1] → mid=0 → nums[0]=-10
  Right: indices [1,1] → nums[1]=-3
Right: indices [3,4] → mid=3 → nums[3]=5
  Right: indices [4,4] → nums[4]=9
```

**Detailed Approach with Algorithm Steps:**
1. **Base Case:** If the array is empty (left > right), return None.
2. **Find Midpoint:** Calculate mid = (left + right) // 2 to get the middle index.
3. **Create Root:** Create a TreeNode with the value at the middle index.
4. **Build Left Subtree:** Recursively build the left subtree from left half [left, mid-1].
5. **Build Right Subtree:** Recursively build the right subtree from right half [mid+1, right].
6. **Return:** Return the root. The tree is guaranteed to be height-balanced.

**Visual Tree Diagram:**
```
Input: [-10, -3, 0, 5, 9]
Indices: 0    1  2  3  4

Step 1: nums[2]=0 is root
          0
       /     \
  [-10,-3]  [5,9]
  idx 0-1   idx 3-4

Step 2: nums[0]=-10 (left subtree root)
        0
      /   \
    -10    5
      \     \
      -3     9
(After recursive processing)
```

**Step-by-Step Trace:**
```
nums = [-10, -3, 0, 5, 9]
helper(left=0, right=4):
  mid = (0+4)//2 = 2, node = TreeNode(0)
  left = helper(0, 1):
    mid = (0+1)//2 = 0, node = TreeNode(-10)
    left = helper(0, -1) → None
    right = helper(1, 1):
      mid = (1+1)//2 = 1, node = TreeNode(-3)
      left = helper(1, 0) → None
      right = helper(2, 1) → None
      return -3
    return -10
  right = helper(3, 4):
    mid = (3+4)//2 = 3, node = TreeNode(5)
    left = helper(3, 2) → None
    right = helper(4, 4):
      mid = (4+4)//2 = 4, node = TreeNode(9)
      left = helper(4, 3) → None
      right = helper(5, 4) → None
      return 9
    return 5
  return 0

Result BST:
      0
     / \
   -10  5
     \   \
     -3   9
```

**Well-Commented Code:**
```python
class Solution:
    def sortedArrayToBST(self, nums: list) -> TreeNode:
        # Edge case: empty array
        if not nums:
            return None

        def helper(left: int, right: int) -> TreeNode:
            # Base case: no elements in this range
            if left > right:
                return None

            # Pick the middle element to maintain balance
            mid = (left + right) // 2

            # Create root node with middle element
            node = TreeNode(nums[mid])

            # Recursively build left and right subtrees
            node.left = helper(left, mid - 1)
            node.right = helper(mid + 1, right)

            return node

        return helper(0, len(nums) - 1)
```

**Complexity Analysis:**
- **Time:** O(n) — each element is visited exactly once to create a node
- **Space:** O(log n) — recursion stack for a balanced tree (height = log n)

**Edge Cases with Examples:**
| Input | Output (BST) | Reason |
|-------|--------------|--------|
| `[]` | `None` | Empty array → empty tree |
| `[1]` | `[1]` | Single element → single node |
| `[1,2,3]` | `[2,1,3]` | Three elements, 2 is middle |
| `[1,2,3,4,5,6,7]` | `[4,2,6,1,3,5,7]` | Perfectly balanced full tree |

**Common Mistakes:**
- ❌ Using array slicing (`nums[:mid]`, `nums[mid+1:]`) instead of index-based recursion — O(n²) due to copying
- ❌ Picking the wrong middle position for even-length arrays
- ❌ Forgetting that the tree must be height-balanced, not just any BST
- ❌ Not handling the empty array edge case
- ❌ Off-by-one errors: `helper(left, mid-1)` not `helper(left, mid)`

**Pattern Recognition Hints:**
- **Divide and Conquer:** Split array in half, solve each half independently — classic D&C pattern
- **Binary Search Analogous:** Same logic as binary search on a sorted array
- **Recursive Tree Construction:** Used whenever you need to build a tree from a linear structure
- **Importance of Balance:** Picking the middle guarantees O(log n) search time in the resulting BST

---

# MEDIUM PROBLEMS (11-25)

---

## Problem 11: Validate Binary Search Tree

**Problem Statement:**
Given the root of a binary tree, determine if it is a valid binary search tree (BST). A valid BST has left subtree values < node < right subtree values for every node.

**Example:**
```
Input: [2,1,3]
Output: True

Input: [5,1,4,null,null,3,6]
Output: False (4 is in the right subtree but < 5)
```

**Approach:**
Use DFS with bounds. Each node must be within a valid range. For left child, the upper bound becomes parent's value. For right child, the lower bound becomes parent's value.

```python
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        def validate(node, low=float('-inf'), high=float('inf')):
            if not node:
                return True
            if node.val <= low or node.val >= high:
                return False
            return validate(node.left, low, node.val) and validate(node.right, node.val, high)
        
        return validate(root)
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** Don't just check left.val < node < right.val. You need to propagate bounds from all ancestors. Use float('-inf') and float('inf') as initial bounds.

---

## Problem 12: Kth Smallest Element in BST

**Problem Statement:**
Given the root of a BST and an integer k, return the kth smallest value (1-indexed) of all the node values in the tree.

**Problem Explanation in Simple Words:**
You have a BST. You want to find the kth smallest number in it. Think of this as: if you sorted all the values in the tree, what would be the kth value? Since BST inorder traversal gives sorted order, we can stop early once we've visited k nodes.

**Example Walkthrough:**
```
Input:
    3
   / \
  1   4
   \
    2
k = 1 (want the 1st smallest)

Inorder traversal: [1, 2, 3, 4]
1st smallest = 1 ✅
```

**Detailed Approach with Algorithm Steps:**
1. **Initialize:** Set `count = 0` and `result = 0` as instance variables.
2. **Inorder Traversal:** Recursively traverse: left → process → right.
3. **Early Termination:** Stop when `count >= k` (we've found our element).
4. **Count:** Increment count when visiting a node.
5. **Capture:** When `count == k`, save the node's value and return.
6. **Return:** The saved result after traversal completes.

**Visual Tree Diagram:**
```
Finding k=3 in this BST:

        5
      /   \
     3     7
    / \   / \
   2   4 6   8
  /
 1

Inorder (sorted): [1, 2, 3, 4, 5, 6, 7, 8]
k=3 → 3rd smallest = 3

Traversal sequence:
  1. visit left subtree of 5 → left subtree of 3 → left subtree of 2 → 1 (count=1)
  2. 2 (count=2)
  3. 3 (count=3) → k reached! Answer = 3
```

**Step-by-Step Trace:**
```
root=[3,1,4,null,2], k=1

inorder(3):
  inorder(1):
    inorder(None): return
    count=1, count==k → result=1, return
  (remaining traversal is skipped due to count >= k)

Return: 1 ✅
```

**Well-Commented Code:**
```python
class Solution:
    def kthSmallest(self, root: TreeNode, k: int) -> int:
        # Instance variables to track state across recursive calls
        self.count = 0   # how many nodes visited so far
        self.result = 0  # stores the kth smallest value

        def inorder(node):
            # Base case or early termination
            if not node or self.count >= k:
                return

            # Process left subtree (smaller elements)
            inorder(node.left)

            # Process current node (this is the (count+1)th smallest)
            self.count += 1
            if self.count == k:
                self.result = node.val
                return  # can stop early

            # Process right subtree (larger elements)
            inorder(node.right)

        inorder(root)
        return self.result
```

**Complexity Analysis:**
- **Time:** O(k) — we stop as soon as we find the kth element; worst case O(n)
- **Space:** O(h) — recursion stack, h = height = O(log n) for balanced, O(n) for skewed

**Edge Cases with Examples:**
| Input | k | Output | Reason |
|-------|---|--------|--------|
| `[1]` | 1 | 1 | Only one node |
| `[2,1,3]` | 3 | 3 | k equals total nodes |
| `[5,3,6,2,4,null,null,1]` | 6 | 6 | Last element in inorder |
| k = n | largest | Largest element in BST |

**Common Mistakes:**
- ❌ Not stopping early — traversing the entire tree even after finding kth element
- ❌ Forgetting that k is 1-indexed, not 0-indexed
- ❌ Using global variables incorrectly in recursion (use `self.` or `nonlocal`)
- ❌ Confusing "kth smallest" with "kth largest" — they are different traversals

**Pattern Recognition Hints:**
- **Inorder on BST = Sorted Order:** This is the most important BST property
- **Early Termination Pattern:** Stop traversal when condition is met
- **Follow-up — Kth Largest:** Use reverse inorder (right-node-left) for kth largest
- **Iterative Version:** Use explicit stack for O(h) space and O(k) time

---

## Problem 13: Binary Tree Level Order Traversal

**Problem Statement:**
Given the root of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).

**Problem Explanation in Simple Words:**
Traverse the tree level by level, from top to bottom. Within each level, go left to right. Think of reading the tree like a book — you read the first row (root), then the second row, then the third, etc.

**Example Walkthrough:**
```
Input:
       3
      / \
     9   20
        /  \
       15   7

Output: [[3], [9, 20], [15, 7]]

Level 0: [3]
Level 1: [9, 20]
Level 2: [15, 7]
```

**Detailed Approach with Algorithm Steps:**
1. **Initialize:** Create a queue and add the root node. Create an empty result list.
2. **Process Levels:** While the queue is not empty:
   a. Record the current queue size (number of nodes at current level).
   b. Create an empty `level` list.
   c. For each node at this level (loop `level_size` times):
      - Dequeue the front node.
      - Add its value to the level list.
      - Enqueue its left child (if exists).
      - Enqueue its right child (if exists).
   d. Append the level list to the result.
3. **Return:** The result list containing levels from top to bottom.

**Visual Tree Diagram:**
```
Queue processing visualization:

Step 0: queue = [3], level_size = 1
  Pop 3, level=[3], push 9, 20
  → result = [[3]]

Step 1: queue = [9, 20], level_size = 2
  Pop 9, level=[9]
  Pop 20, level=[9,20], push 15, 7
  → result = [[3], [9,20]]

Step 2: queue = [15, 7], level_size = 2
  Pop 15, level=[15]
  Pop 7, level=[15,7]
  → result = [[3], [9,20], [15,7]]
```

**Step-by-Step Trace:**
```
Input: [3,9,20,null,null,15,7]

Initialize: queue = deque([3]), result = []

Iteration 1: level_size = 1
  Pop 3 → level = [3]
  Push 9 (left of 3), Push 20 (right of 3)
  result = [[3]], queue = [9, 20]

Iteration 2: level_size = 2
  Pop 9 → level = [9] (no children to push)
  Pop 20 → level = [9, 20]
  Push 15 (left of 20), Push 7 (right of 20)
  result = [[3], [9, 20]], queue = [15, 7]

Iteration 3: level_size = 2
  Pop 15 → level = [15]
  Pop 7 → level = [15, 7]
  result = [[3], [9, 20], [15, 7]], queue = []

Return [[3], [9, 20], [15, 7]] ✅
```

**Well-Commented Code:**
```python
from collections import deque

class Solution:
    def levelOrder(self, root: TreeNode) -> list:
        # Edge case: empty tree
        if not root:
            return []

        result = []
        queue = deque([root])  # Initialize queue with root

        while queue:
            # Number of nodes at the current level
            level_size = len(queue)
            level = []  # Stores values for this level

            # Process all nodes at this level
            for _ in range(level_size):
                node = queue.popleft()  # Dequeue front node
                level.append(node.val)

                # Add children for the next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(level)  # Add this level to result

        return result
```

**Complexity Analysis:**
- **Time:** O(n) — each node is visited exactly once
- **Space:** O(n) — queue can hold up to n/2 nodes at the widest level

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[]` | `[]` | Empty tree |
| `[1]` | `[[1]]` | Single node |
| `[1,2]` | `[[1],[2]]` | Two levels |
| `[1,null,2]` | `[[1],[2]]` | Skewed tree — each level has one node |
| Full tree with 7 nodes | `[[root],[2 nodes],[4 nodes]]` | Each level doubles |

**Common Mistakes:**
- ❌ Not separating levels — mixing all nodes into a single list
- ❌ Modifying queue size during iteration — must capture `len(queue)` before the inner loop
- ❌ Not checking if children exist before enqueuing
- ❌ Using recursion instead of BFS (DFS doesn't process level-by-level naturally)

**Pattern Recognition Hints:**
- **Template Pattern:** This is the template for all level-order problems
- **Variations:** Right Side View (Problem 14), Zigzag (Problem 20), Average of Levels, etc.
- **BFS for Shortest Path:** BFS guarantees shortest path because it explores level by level
- **Level Tracking:** The inner loop `for _ in range(level_size)` is the key technique

---

## Problem 14: Binary Tree Right Side View

**Problem Statement:**
Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see from top to bottom.

**Problem Explanation in Simple Words:**
You're standing to the right of the tree, looking at it. At each level, you can only see the rightmost node (nodes to its left are hidden behind it). Return what you see, from top to bottom.

**Example Walkthrough:**
```
Input:        Output from right side:
    1←              [1, 3, 4]
   / \
  2   3←
   \   \
    5   4←

Level 0: Rightmost = 1
Level 1: Rightmost = 3 (2 is hidden behind 3)
Level 2: Rightmost = 4 (5 is hidden behind 4)
```

**Detailed Approach with Algorithm Steps:**
1. **Initialize:** Create a queue with the root. Create an empty result list.
2. **BFS:** While queue is not empty:
   a. Record the current level size.
   b. Iterate through all nodes at this level.
   c. If current node is the LAST node in this level (i == level_size-1), add its value to result.
   d. Enqueue left and right children (if they exist).
3. **Return:** The result list containing the rightmost node at each level.

**Visual Tree Diagram:**
```
Right side visibility:
          [1] ← Visible (root)
         / \
      [2]  [3] ← Visible (rightmost at level 1)
        \    \
       [5]  [4] ← Visible (rightmost at level 2)

Hidden nodes: 2 (behind 3), 5 (behind 4)
```

**Step-by-Step Trace:**
```
Input: [1,2,3,null,5,null,4]

Initialize: queue = [1], result = []

Level 0: level_size = 1
  Pop 1, i=0 == level_size-1=0 → result=[1]
  Push 2, Push 3

Level 1: level_size = 2
  Pop 2, i=0 != 1 → skip, Push 5
  Pop 3, i=1 == 1 → result=[1,3], Push 4

Level 2: level_size = 2
  Pop 5, i=0 != 1 → skip
  Pop 4, i=1 == 1 → result=[1,3,4]

Return [1,3,4] ✅
```

**Well-Commented Code:**
```python
from collections import deque

class Solution:
    def rightSideView(self, root: TreeNode) -> list:
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)

            # Process all nodes at current level
            for i in range(level_size):
                node = queue.popleft()

                # The last node at each level is visible from the right
                if i == level_size - 1:
                    result.append(node.val)

                # Enqueue children for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return result
```

**Complexity Analysis:**
- **Time:** O(n) — each node is visited exactly once
- **Space:** O(n) — queue can hold up to n/2 nodes at the widest level

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[]` | `[]` | Empty tree |
| `[1]` | `[1]` | Only one node |
| `[1,2]` | `[1,2]` | Two levels, both rightmost |
| `[1,2,3,4]` | `[1,3,4]` | 2 hidden behind 3 at level 1 |

**Common Mistakes:**
- ❌ Taking the right child of every node instead of the rightmost at each level
- ❌ Not considering that left nodes can be visible if no right node exists at that level
- ❌ Forgetting to check for empty tree
- ❌ Using DFS without tracking depth (need to override earlier values)

**Pattern Recognition Hints:**
- **Level-order Variant:** Any "side view" or "corner view" uses this pattern
- **Left Side View:** Same but take the FIRST node at each level (i == 0)
- **DFS Alternative:** Preorder traversal visiting right child first, tracking depth
- **Real-world:** This is essentially computing the "silhouette" of a tree

---

## Problem 15: Lowest Common Ancestor of Binary Tree

**Problem Statement:**
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes p and q. The LCA is the deepest node that has both p and q as descendants.

**Example:**
```
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
Output: 3
```

**Approach:**
Use recursive DFS. If current node is None, p, or q, return it. Recurse left and right. If both return non-null, current node is LCA. If only one side returns non-null, that side contains both nodes.

```python
class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        if not root or root == p or root == q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root
        return left if left else right
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** This is one of the most important tree problems. The key insight: if p and q are in different subtrees, current node is LCA. If both are in same subtree, LCA is in that subtree.

---

## Problem 16: Lowest Common Ancestor of BST

**Problem Statement:**
Given a BST, find the lowest common ancestor of two nodes p and q. The BST property makes this simpler than the general tree version.

**Problem Explanation in Simple Words:**
Find the deepest (lowest) node in the BST that is an ancestor of BOTH p and q. Since this is a BST, we can use the ordering property: all left values < root < all right values. This lets us decide at each node whether p and q are both on the left, both on the right, or split.

**Example Walkthrough:**
```
BST:
        6       p=2, q=8
       / \
      2   8     Path to 2: 6→2
     / \ / \    Path to 8: 6→8
    0  4 7 9      Common ancestor: 6
      / \
     3   5      LCA = 6 ✅

If p=2, q=4:
  6→2, 6→2→4   Common ancestor: 2
  LCA = 2 ✅
```

**Detailed Approach with Algorithm Steps:**
1. **Start at Root:** Begin traversal from the root.
2. **Both on Left:** If both p.val < root.val and q.val < root.val, LCA must be in the left subtree → move root to root.left.
3. **Both on Right:** If both p.val > root.val and q.val > root.val, LCA must be in the right subtree → move root to root.right.
4. **Split Found:** Otherwise (one is on left, one is on right, or one equals root), the current node is the LCA → return root.

**Visual Tree Diagram:**
```
Finding LCA of 2 and 8:
        [6] ← start here (2<6, 8>6 → split, LCA=6)
       /   \
      2     8
     / \   / \
    0   4 7   9

Finding LCA of 2 and 4:
        [6] ← (2<6, 4<6 → go left)
       /   \
     [2] ← start here (2<2? No, 4>2 → split, LCA=2)
     / \
    0   4

Finding LCA of 0 and 5:
        [6] ← (0<6, 5<6 → go left)
       /   \
     [2] ← (0<2, 5>2 → split, LCA=2)
     / \
    0   4
       / \
      3   5
```

**Step-by-Step Trace:**
```
Input: root=[6,2,8,0,4,7,9,null,null,3,5], p=2, q=8

Iteration 1: root=6
  p.val=2 < 6 AND q.val=8 > 6 → NOT both left, NOT both right
  → SPLIT: return 6 ✅

Input: root=[6,2,8,0,4,7,9,null,null,3,5], p=2, q=4

Iteration 1: root=6
  p.val=2 < 6 AND q.val=4 < 6 → both left → root = root.left = 2

Iteration 2: root=2
  p.val=2 == 2 (one equals root) → SPLIT: return 2 ✅
```

**Well-Commented Code:**
```python
class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        # Iterative traversal using BST property
        while root:
            # Both nodes are in the left subtree
            if p.val < root.val and q.val < root.val:
                root = root.left

            # Both nodes are in the right subtree
            elif p.val > root.val and q.val > root.val:
                root = root.right

            # Split: one on left, one on right, or one equals root
            else:
                return root

        # Should never reach here for valid input
        return None
```

**Complexity Analysis:**
- **Time:** O(h) — at each step we go down one level, h = height of BST
- **Space:** O(1) — iterative, no extra space

**Edge Cases with Examples:**
| Input | p | q | Output | Reason |
|-------|---|---|--------|--------|
| Root = [2,1] | 2 | 1 | 2 | Root is LCA when one node IS the root |
| Skewed BST [1,2,3,4] | 3 | 4 | 3 | LCA can be one of the nodes itself |
| Normal BST | same node | same node | that node | LCA of a node with itself is the node |

**Common Mistakes:**
- ❌ Using a general binary tree LCA algorithm (O(n) time, O(h) space) instead of the simpler BST version
- ❌ Not using iterative approach — recursion adds unnecessary O(h) space
- ❌ Forgetting that if p or q equals the root, the root is the LCA
- ❌ Using `<=` instead of `<` when comparing values — careful with BST property

**Pattern Recognition Hints:**
- **BST Property Exploitation:** BST problems often have simpler O(h) solutions vs O(n) for general trees
- **Divide and Conquer:** Eliminate half the tree at each step — like binary search!
- **LCA in BST vs Binary Tree:** Compare with Problem 15 — BST property saves you from exploring both subtrees
- **Iterative is Better:** For BST problems, iterative solutions are often simpler and use O(1) space

---

## Problem 17: Serialize and Deserialize Binary Tree

**Problem Statement:**
Design an algorithm to serialize and deserialize a binary tree. Serialization is converting a tree to a string, and deserialization is reconstructing the tree from that string.

**Problem Explanation in Simple Words:**
How do you save a tree to a file and load it back? Serialization converts the tree structure into a string (like writing it to a file). Deserialization takes that string and rebuilds the exact same tree in memory. Think of it as "pickling" and "unpickling" the tree.

**Example Walkthrough:**
```
Tree:
     1
    / \
   2   3
      / \
     4   5

Serialized: "1,2,null,null,3,4,null,null,5,null,null"

How to read it: Preorder traversal
  1 → left=2 → left=null → right=null → return to 1
  → right=3 → left=4 → left=null → right=null → return to 3
  → right=5 → left=null → right=null → done
```

**Detailed Approach with Algorithm Steps:**
**Serialization:**
1. **Base Case:** If node is None, return "null".
2. **Preorder:** Write current node's value as a string.
3. **Recurse Left:** Append comma + serialized left subtree.
4. **Recurse Right:** Append comma + serialized right subtree.
5. **Return:** The complete string.

**Deserialization:**
1. **Split:** Split the string by comma to get a list of tokens.
2. **Iterator:** Create an iterator over the tokens.
3. **Helper:** Read next token:
   - If "null", return None.
   - Otherwise, create a TreeNode with the integer value.
   - Recursively build left and right subtrees.
4. **Return:** The constructed tree root.

**Visual Tree Diagram:**
```
Serialization process (preorder):
       1
      / \
     2   3
        / \
       4   5

Order of writing: 1 → 2 → null → null → 3 → 4 → null → null → 5 → null → null
String: "1,2,null,null,3,4,null,null,5,null,null"

Deserialization reads the same sequence backwards:
  read "1" → create node(1)
  read "2" → create node(2), attach as left of 1
  read "null" → no left child for 2
  read "null" → no right child for 2
  read "3" → create node(3), attach as right of 1
  ... and so on
```

**Step-by-Step Trace:**
```
Serialize [1,2,3,null,null,4,5]:
  serialize(1):
    "1" + "," + serialize(2):
      "2" + "," + serialize(null) = "null" + "," + serialize(null) = "null"
      → "2,null,null"
    + "," + serialize(3):
      "3" + "," + serialize(4):
        "4" + "," + serialize(null) = "null" + "," + serialize(null) = "null"
        → "4,null,null"
      + "," + serialize(5):
        "5" + "," + serialize(null) = "null" + "," + serialize(null) = "null"
        → "5,null,null"
      → "3,4,null,null,5,null,null"
    → "1,2,null,null,3,4,null,null,5,null,null"

Deserialize "1,2,null,null,3,4,null,null,5,null,null":
  helper("1"): node=1
    helper("2"): node=2
      helper("null"): None (left of 2)
      helper("null"): None (right of 2)
    helper("3"): node=3
      helper("4"): node=4
        helper("null"): None
        helper("null"): None
      helper("5"): node=5
        helper("null"): None
        helper("null"): None
  → Tree reconstructed! ✅
```

**Well-Commented Code:**
```python
class Codec:
    def serialize(self, root: TreeNode) -> str:
        """Convert tree to string using preorder traversal."""
        # Base case: null node marker
        if not root:
            return "null"

        # Preorder: root → left → right
        return str(root.val) + "," + self.serialize(root.left) + "," + self.serialize(root.right)

    def deserialize(self, data: str) -> TreeNode:
        """Convert string back to tree."""
        def helper(nodes):
            """Recursive helper that consumes tokens from the iterator."""
            # Read next token
            val = next(nodes)
            # Null marker → no node here
            if val == "null":
                return None

            # Create node and recursively build children
            node = TreeNode(int(val))
            node.left = helper(nodes)   # Build left subtree
            node.right = helper(nodes)  # Build right subtree
            return node

        # Split string and create iterator
        nodes = iter(data.split(","))
        return helper(nodes)
```

**Complexity Analysis:**
- **Time:** O(n) for both operations — visit each node exactly once
- **Space:** O(n) — the serialized string is O(n), recursion stack is O(h)

**Edge Cases with Examples:**
| Input | Serialized | Deserialized | Reason |
|-------|-----------|-------------|--------|
| `[]` | `"null"` | `[]` | Empty tree |
| `[1]` | `"1,null,null"` | `[1]` | Single node with null children |
| `[1,2]` | `"1,2,null,null,null"` | `[1,2]` | Only left child |
| `[1,null,2]` | `"1,null,2,null,null"` | `[1,null,2]` | Only right child |

**Common Mistakes:**
- ❌ Not handling null nodes — the tree structure is impossible to reconstruct without null markers
- ❌ Mismatched order between serialize and deserialize (e.g., preorder vs inorder)
- ❌ Not using a delimiter (comma) — ambiguous without it for multi-digit numbers
- ❌ Using string concatenation in a loop (O(n²)) instead of recursive building
- ❌ Forgetting to convert string values back to integers during deserialization

**Pattern Recognition Hints:**
- **Tree Serialization is Fundamental:** Used in "Find Duplicate Subtrees" (Problem 34)
- **Preorder + Null Markers:** The simplest and most common serialization format
- **Format Variations:** Level-order (BFS) serialization is also common (LeetCode format)
- **Iterator Pattern:** `iter()` + `next()` makes deserialization elegant and efficient
- **Reversible Traversal:** The key insight is that any traversal can be used as long as null markers are included

---

## Problem 18: Binary Tree Maximum Path Sum

**Problem Statement:**
A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge. The path sum is the sum of node values. Find the maximum path sum. The path can start and end at any node.

**Example:**
```
Input: [1,2,3]
Output: 6 (2 -> 1 -> 3)
```

**Approach:**
At each node, calculate the max path sum that passes through it. Track the global maximum. For each node, the path sum = node.val + left_gain + right_gain. But for returning to parent, we can only take one branch.

```python
class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        self.max_sum = float('-inf')
        
        def gain(node):
            if not node:
                return 0
            left = max(gain(node.left), 0)
            right = max(gain(node.right), 0)
            self.max_sum = max(self.max_sum, node.val + left + right)
            return node.val + max(left, right)
        
        gain(root)
        return self.max_sum
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** Use `max(gain, 0)` to ignore negative paths. Update global max at each node with `node.val + left + right`, but only return `node.val + max(left, right)` to parent (can only go one way).

---

## Problem 19: Path Sum II

**Problem Statement:**
Given the root of a binary tree and an integer targetSum, return all root-to-leaf paths where the sum equals targetSum.

**Example:**
```
Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
Output: [[5,4,11,2],[5,8,4,5]]
```

**Approach:**
Use DFS with backtracking. Maintain a current path list and remaining sum. When reaching a leaf with remaining sum == 0, add the current path to result.

```python
class Solution:
    def pathSum(self, root: TreeNode, targetSum: int) -> list:
        result = []
        
        def dfs(node, remaining, path):
            if not node:
                return
            path.append(node.val)
            if not node.left and not node.right and remaining == node.val:
                result.append(list(path))
            else:
                dfs(node.left, remaining - node.val, path)
                dfs(node.right, remaining - node.val, path)
            path.pop()
        
        dfs(root, targetSum, [])
        return result
```

**Complexity:**
- Time: O(n²) - in worst case, we copy paths of length n for n leaves
- Space: O(n) - path storage and recursion stack

**Trick/Tip:** Use `path.pop()` for backtracking. Always make a copy of path with `list(path)` when adding to result. Don't modify the path after returning.

---

## Problem 20: Binary Tree Zigzag Level Order Traversal

**Problem Statement:**
Return the zigzag level order traversal of a binary tree's nodes' values (i.e., from left to right, then right to left for the next level, and so on).

**Problem Explanation in Simple Words:**
Traverse the tree level by level, but alternate direction each level. First level: left to right. Second level: right to left. Third level: left to right, and so on. It's a "zigzag" pattern.

**Example Walkthrough:**
```
Input:
        3
       / \
      9   20
         /  \
        15   7

Level 0 (L→R): [3]
Level 1 (R→L): [20, 9]   ← reversed!
Level 2 (L→R): [15, 7]

Output: [[3], [20, 9], [15, 7]]
```

**Detailed Approach with Algorithm Steps:**
1. **Initialize:** Queue with root, direction flag `left_to_right = True`.
2. **Process Levels:** While queue is not empty:
   a. Record current level size.
   b. Create a deque for this level's values.
   c. For each node at this level:
      - If left_to_right: append value to the END of the deque.
      - If right_to_left: append value to the FRONT of the deque (prepend).
      - Enqueue children (left then right, always).
   d. Convert deque to list and append to result.
   e. Flip the direction flag.
3. **Return result.**

**Visual Tree Diagram:**
```
Zigzag pattern visualization:

Level 0 → [3]       (left to right)
              ──►

Level 1 → [20, 9]   (right to left — reversed)
              ◄──

Level 2 → [15, 7]   (left to right)
              ──►

Queue processing:
  Step 0: queue=[3], L→R, level=[3]
  Step 1: queue=[9,20], R→L → pop 9 → prepend, pop 20 → prepend → level=[20,9]
  Step 2: queue=[15,7], L→R → level=[15,7]
```

**Step-by-Step Trace:**
```
Input: [3,9,20,null,null,15,7]

Initialize: queue = [3], left_to_right = True

Level 0 (L→R): level_size=1
  Pop 3 → append 3 → level_deque = [3]
  Push 9 (left), Push 20 (right)
  result = [[3]], flip flag → L→R = False

Level 1 (R→L): level_size=2
  Pop 9 → appendleft 9 → level_deque = [9]
  Pop 20 → appendleft 20 → level_deque = [20, 9]
  Push 15 (left of 20), Push 7 (right of 20)
  result = [[3], [20, 9]], flip flag → L→R = True

Level 2 (L→R): level_size=2
  Pop 15 → append 15 → level_deque = [15]
  Pop 7 → append 7 → level_deque = [15, 7]
  result = [[3], [20, 9], [15, 7]]

Return [[3], [20, 9], [15, 7]] ✅
```

**Well-Commented Code:**
```python
from collections import deque

class Solution:
    def zigzagLevelOrder(self, root: TreeNode) -> list:
        if not root:
            return []

        result = []
        queue = deque([root])
        left_to_right = True  # Direction flag for current level

        while queue:
            level_size = len(queue)
            level = deque()  # Use deque for O(1) append at either end

            for _ in range(level_size):
                node = queue.popleft()

                # Add to deque based on current direction
                if left_to_right:
                    level.append(node.val)      # Add to end
                else:
                    level.appendleft(node.val)  # Add to front

                # Always enqueue children left-to-right
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(list(level))  # Convert deque to list
            left_to_right = not left_to_right  # Flip direction

        return result
```

**Complexity Analysis:**
- **Time:** O(n) — each node visited exactly once
- **Space:** O(n) — queue holds up to n/2 nodes, deque holds one level

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[]` | `[]` | Empty tree |
| `[1]` | `[[1]]` | Single level, always L→R |
| `[1,2,3]` | `[[1],[3,2]]` | Level 1 reversed |
| `[1,2,3,4,5,6,7]` | `[[1],[3,2],[4,5,6,7]]` | Full tree zigzag |
| One-sided tree | Each level has one element | Single element unaffected by reversal |

**Common Mistakes:**
- ❌ Reversing the children enqueue order instead of the values — always enqueue left then right
- ❌ Using a regular list and reversing for R→L levels — O(n) per level vs O(1) with deque
- ❌ Forgetting to flip the flag after processing each level
- ❌ Modifying the queue while iterating over `range(level_size)` — safe here since level_size was captured

**Pattern Recognition Hints:**
- **Level-order Variant:** Minor modification to the standard BFS template
- **Deque for Two-sided Operations:** `append` vs `appendleft` gives O(1) for both directions
- **Alternating Logic:** A boolean flag toggled each level is a common pattern
- **Relation to Right Side View:** Both process level-by-level but collect different nodes

---

## Problem 21: Construct Binary Tree from Preorder and Inorder

**Problem Statement:**
Given two integer arrays preorder and inorder where preorder is the preorder traversal and inorder is the inorder traversal of a binary tree, construct and return the binary tree.

**Problem Explanation in Simple Words:**
You have two clues about a tree: its preorder traversal (root → left → right) and its inorder traversal (left → root → right). Using these two traversals together, you can uniquely reconstruct the tree. The first element in preorder is always the root. The root's position in inorder tells you which elements are in the left subtree vs the right subtree.

**Example Walkthrough:**
```
preorder = [3, 9, 20, 15, 7]   Format: [root, left_subtree..., right_subtree...]
inorder  = [9, 3, 15, 20, 7]   Format: [left_subtree..., root, right_subtree...]

Step 1: preorder[0] = 3 → root is 3
Find 3 in inorder: inorder[1] = 3
  Left subtree inorder = [9]     (elements before 3)
  Right subtree inorder = [15, 20, 7]  (elements after 3)
  Left subtree preorder = [9]    (next 1 element from preorder)
  Right subtree preorder = [20, 15, 7]  (remaining elements)

Step 2 (left subtree): preorder=[9], inorder=[9]
  root = 9, left=None, right=None

Step 3 (right subtree): preorder=[20,15,7], inorder=[15,20,7]
  root = 20, find 20 in inorder at index 1
  Left: preorder=[15], inorder=[15] → node 15
  Right: preorder=[7], inorder=[7] → node 7

Result tree:
      3
     / \
    9   20
       /  \
      15   7
```

**Detailed Approach with Algorithm Steps:**
1. **Base Case:** If arrays are empty, return None.
2. **Identify Root:** The first element of preorder is the root.
3. **Find Split Point:** Locate root's value in inorder array using index lookup.
   - Elements to the left of root in inorder form the left subtree.
   - Elements to the right form the right subtree.
4. **Calculate Sizes:** The number of elements in left inorder = the split index = mid.
   - Left subtree preorder: preorder[1:mid+1] (next `mid` elements)
   - Right subtree preorder: preorder[mid+1:] (rest)
   - Left subtree inorder: inorder[:mid]
   - Right subtree inorder: inorder[mid+1:]
5. **Recurse:** Build left and right subtrees recursively.
6. **Return:** The constructed tree root.

**Visual Tree Diagram:**
```
Relating preorder and inorder:

preorder: [3,   9,    20, 15, 7]
           ↑    ↑     ↑
         root  left   right
               1 elem 3 elems

inorder:  [9,   3,    15, 20, 7]
           ↑    ↑     ↑
         left  root   right
         1 ele        3 elems

Numbers match: left subtree has 1 node, right has 3 nodes!
```

**Step-by-Step Trace:**
```
preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]

buildTree(preorder, inorder):
  root = TreeNode(3)
  mid = inorder.index(3) = 1

  # Left subtree: 1 element
  root.left = buildTree([9], [9]):
    root = TreeNode(9)
    mid = inorder.index(9) = 0
    root.left = buildTree([], []) → None
    root.right = buildTree([], []) → None
    return 9

  # Right subtree: 3 elements
  root.right = buildTree([20,15,7], [15,20,7]):
    root = TreeNode(20)
    mid = inorder.index(20) = 1
    root.left = buildTree([15], [15]):
      root = TreeNode(15)
      mid = 0
      root.left = root.right = None
      return 15
    root.right = buildTree([7], [7]):
      root = TreeNode(7)
      mid = 0
      root.left = root.right = None
      return 7
    return 20

  return 3

Result: [3,9,20,null,null,15,7] ✅
```

**Well-Commented Code (Optimized with Hashmap):**
```python
class Solution:
    def buildTree(self, preorder: list, inorder: list) -> TreeNode:
        # Build hashmap for O(1) inorder lookup
        # Maps value → index in inorder array
        inorder_map = {val: idx for idx, val in enumerate(inorder)}

        def helper(pre_start, pre_end, in_start, in_end):
            """Build subtree from preorder[pre_start:pre_end] and inorder[in_start:in_end]"""
            # Base case: no elements in this range
            if pre_start > pre_end or in_start > in_end:
                return None

            # Root is the first element in preorder range
            root_val = preorder[pre_start]
            root = TreeNode(root_val)

            # Find root's position in inorder to split left/right
            mid = inorder_map[root_val]

            # Calculate how many nodes are in the left subtree
            left_size = mid - in_start

            # Recursively build left and right subtrees
            root.left = helper(pre_start + 1, pre_start + left_size, in_start, mid - 1)
            root.right = helper(pre_start + left_size + 1, pre_end, mid + 1, in_end)

            return root

        return helper(0, len(preorder) - 1, 0, len(inorder) - 1)
```

**Complexity Analysis:**
- **Time:** O(n) with hashmap optimization (O(n²) without — due to `inorder.index()` each call)
- **Space:** O(n) — hashmap and recursion stack

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `pre=[1], in=[1]` | `[1]` | Single node |
| `pre=[], in=[]` | `[]` | Empty |
| `pre=[1,2,3], in=[3,2,1]` | Skewed left tree | All elements on left side |
| `pre=[1,2,3], in=[1,2,3]` | Skewed right tree | All elements on right side |

**Common Mistakes:**
- ❌ Using array slicing (O(n²) copying) instead of index ranges (O(n))
- ❌ Confusing left_size calculation — it's `mid - in_start`, not just `mid`
- ❌ Forgetting that preorder and inorder have different structures for the same tree
- ❌ Incorrectly mapping preorder ranges — the number of left subtree elements is the same in both arrays

**Pattern Recognition Hints:**
- **Unique Tree Construction:** A binary tree can be uniquely reconstructed from:
  - Preorder + Inorder (this problem)
  - Inorder + Postorder (Problem 22)
  - Preorder + Postorder (NOT unique for full binary trees)
- **Hashmap for Lookup:** Always use a hashmap to avoid O(n) `index()` calls in recursive solutions
- **Divide and Conquer:** The inorder split gives you the exact count of left/right subtree nodes

---

## Problem 22: Construct Binary Tree from Inorder and Postorder

**Problem Statement:**
Given two integer arrays inorder and postorder where inorder is the inorder traversal and postorder is the postorder traversal of a binary tree, construct and return the binary tree.

**Problem Explanation in Simple Words:**
Just like Problem 21, but now you have postorder (left → right → root) instead of preorder. The last element in postorder is the root. Use inorder to determine left and right subtree sizes. Same concept, different traversal.

**Example Walkthrough:**
```
inorder   = [9, 3, 15, 20, 7]   Format: [left..., root, right...]
postorder = [9, 15, 7, 20, 3]   Format: [left..., right..., root]

Step 1: postorder[-1] = 3 → root is 3
Find 3 in inorder: index 1
  Left subtree inorder = [9]
  Right subtree inorder = [15, 20, 7]
  Left subtree postorder = [9]          (first mid=1 elements)
  Right subtree postorder = [15, 7, 20]  (remaining except last)

Step 2 (left): inorder=[9], postorder=[9] → node 9
Step 3 (right): inorder=[15,20,7], postorder=[15,7,20]
  root = 20, find 20 at index 1
  Left: [15], [15] → node 15
  Right: [7], [7] → node 7

Result:
      3
     / \
    9   20
       /  \
      15   7
```

**Detailed Approach with Algorithm Steps:**
1. **Base Case:** If arrays are empty, return None.
2. **Identify Root:** The LAST element of postorder is the root.
3. **Find Split:** Locate root's value in inorder using a hashmap.
   - Left inorder: inorder[:mid]
   - Right inorder: inorder[mid+1:]
4. **Split Postorder:**
   - Left postorder: postorder[:mid] (same number of elements as left inorder)
   - Right postorder: postorder[mid:-1] (remaining except last element which is root)
5. **Recurse Right First (optional):** Unlike preorder, the recursion order doesn't matter here since postorder already separates left and right.
6. **Return root.**

**Visual Tree Diagram:**
```
Relating postorder and inorder:

postorder: [9,    15, 7, 20,    3]
            ↑     ↑             ↑
          left   right        root
          1 ele  3 ele

inorder: [9,      3,    15, 20, 7]
          ↑       ↑     ↑
         left   root   right
         1 ele          3 ele

The key insight: number of LEFT elements is the same in both arrays.
```

**Step-by-Step Trace:**
```
inorder=[9,3,15,20,7], postorder=[9,15,7,20,3]

buildTree(inorder, postorder):
  root_val = postorder[-1] = 3
  mid = inorder.index(3) = 1

  # Left subtree: mid=1 elements
  root.left = buildTree([9], [9]):
    root_val = 9, mid = 0
    root.left = buildTree([], []) → None
    root.right = buildTree([], []) → None
    return 9

  # Right subtree: remaining elements
  root.right = buildTree([15,20,7], [15,7,20]):
    root_val = 20, mid = 1
    root.left = buildTree([15], [15]):
      return 15
    root.right = buildTree([7], [7]):
      return 7
    return 20

  return 3
```

**Well-Commented Code (Optimized with Hashmap):**
```python
class Solution:
    def buildTree(self, inorder: list, postorder: list) -> TreeNode:
        # Hashmap for O(1) inorder lookup
        inorder_map = {val: idx for idx, val in enumerate(inorder)}

        def helper(in_start, in_end, post_start, post_end):
            """Build subtree from inorder[in_start:in_end+1] and postorder[post_start:post_end+1]"""
            if in_start > in_end or post_start > post_end:
                return None

            # Last element in postorder range is the root
            root_val = postorder[post_end]
            root = TreeNode(root_val)

            # Find root position in inorder
            mid = inorder_map[root_val]

            # Number of nodes in left subtree
            left_size = mid - in_start

            # Build left and right subtrees
            root.left = helper(in_start, mid - 1, post_start, post_start + left_size - 1)
            root.right = helper(mid + 1, in_end, post_start + left_size, post_end - 1)

            return root

        return helper(0, len(inorder) - 1, 0, len(postorder) - 1)
```

**Complexity Analysis:**
- **Time:** O(n) with hashmap; O(n²) without
- **Space:** O(n) — hashmap and recursion stack

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `in=[1], post=[1]` | `[1]` | Single node |
| `in=[2,1], post=[2,1]` | `[1,2]` | Skewed left tree |
| `in=[1,2], post=[2,1]` | `[1,null,2]` | Skewed right tree |

**Common Mistakes:**
- ❌ Taking the first element of postorder (it's the last element!)
- ❌ Incorrect slicing for postorder — remember the last element is the root
- ❌ Confusing with preorder version — the recursion structure is different
- ❌ Not accounting for the root removal in postorder when splitting

**Pattern Recognition Hints:**
- **Symmetric to Problem 21:** Same idea, different end of the array
- **Postorder = Left-Right-Root:** The last element is always the root
- **Inorder = Left-Root-Right:** The root splits left and right subtrees
- **Combined:** These two constructions show how traversal pairs uniquely determine a tree

---

## Problem 23: Populating Next Right Pointers in Each Node

**Problem Statement:**
You are given a perfect binary tree. Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to NULL.

**Problem Explanation in Simple Words:**
You have a perfect binary tree (all levels are completely filled). Each node has an extra pointer `next`. Set each node's `next` to point to the node immediately to its right at the same level. The rightmost node at each level should have `next = None`. Think of connecting nodes horizontally across the tree.

**Example Walkthrough:**
```
Input: Perfect binary tree
        1
       / \
      2   3
     / \ / \
    4  5 6  7

Output with next pointers:
        1 → None
       / \
      2 → 3 → None
     / \ / \
    4→5→6→7 → None
```

**Detailed Approach with Algorithm Steps:**
1. **Initialize:** Queue with root. Handle empty tree edge case.
2. **Process Levels:** While queue is not empty:
   a. Record level_size.
   b. Set `prev = None` — tracks the previous node at this level.
   c. For each node at this level:
      - Dequeue node.
      - If prev exists, set `prev.next = node` (connect previous to current).
      - Update `prev = node` for next iteration.
      - Enqueue left and right children.
3. **Return:** The root with all next pointers populated.

**Visual Tree Diagram:**
```
Perfect binary tree with next pointers:

Level 0:      1 ───────────→ None
Level 1:     2 ───────→ 3 → None
Level 2:   4 → 5 → 6 → 7 → None

Queue-based connection at level 2:
  queue initially: [4, 5, 6, 7]
  Pop 4: prev=None, prev=4
  Pop 5: 4.next=5, prev=5
  Pop 6: 5.next=6, prev=6
  Pop 7: 6.next=7, prev=7
  (end of level, 7.next stays None)
```

**Step-by-Step Trace:**
```
Input: [1,2,3,4,5,6,7]

Initialize: queue=[1]

Level 0 (size=1): prev=None
  Pop 1: prev=None→skip, prev=1. Push 2, 3
  Result: 1.next = None (default)

Level 1 (size=2): prev=None
  Pop 2: prev=None→skip, prev=2. Push 4, 5
  Pop 3: prev=2→2.next=3, prev=3. Push 6, 7
  Result: 2.next = 3, 3.next = None

Level 2 (size=4): prev=None
  Pop 4: prev=None→skip, prev=4
  Pop 5: 4.next=5, prev=5
  Pop 6: 5.next=6, prev=6
  Pop 7: 6.next=7, prev=7 (end, 7.next=None)
  Result: 4→5→6→7→None

Return root ✅
```

**Well-Commented Code (BFS Approach):**
```python
from collections import deque

class Solution:
    def connect(self, root: TreeNode) -> TreeNode:
        if not root:
            return None

        queue = deque([root])

        while queue:
            level_size = len(queue)
            prev = None  # Previous node at current level

            for _ in range(level_size):
                node = queue.popleft()

                # Connect previous node to current node
                if prev:
                    prev.next = node

                prev = node  # Update previous for next iteration

                # Add children for processing next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return root
```

**Well-Commented Code (O(1) Space — Optimal):**
```python
class Solution:
    def connect(self, root: TreeNode) -> TreeNode:
        if not root:
            return None

        # Start with the root (leftmost of level 0)
        leftmost = root

        while leftmost.left:  # While there's a next level
            # Traverse current level using next pointers
            head = leftmost
            while head:
                # Connection 1: left child → right child
                head.left.next = head.right

                # Connection 2: right child → next node's left child
                if head.next:
                    head.right.next = head.next.left

                head = head.next  # Move right on current level

            leftmost = leftmost.left  # Move to next level

        return root
```

**Complexity Analysis:**
- BFS: **Time** O(n), **Space** O(n)
- Optimal: **Time** O(n), **Space** O(1)

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[]` | `[]` | Empty tree |
| `[1]` | `[1]` | Single node, next=None |
| Perfect tree of height 3 | All next pointers connected | All levels fully populated |

**Common Mistakes:**
- ❌ Setting `node.next` to the next node in the queue without level separation — might cross levels
- ❌ Forgetting that the rightmost node at each level should have `next = None`
- ❌ Using DFS instead of BFS — DFS doesn't naturally give horizontal connections
- ❌ Only applicable to perfect binary trees (Problem 23 in some variants works on any binary tree)

**Pattern Recognition Hints:**
- **Level-order with Previous Pointer:** Track `prev` at each level for connecting adjacent nodes
- **O(1) Space Alternative:** Use the next pointers themselves to traverse levels — very elegant
- **Perfect Tree Property:** The tree must be perfect for the O(1) space solution to work
- **General Tree Version:** For non-perfect trees, use BFS with O(n) space

---

## Problem 24: Binary Search Tree Iterator

**Problem Statement:**
Implement an iterator over a BST. The iterator initializes with the root of the BST and has next() and hasNext() methods that return the next smallest number.

**Problem Explanation in Simple Words:**
Create an iterator that visits BST nodes in ascending order (like inorder traversal) but one at a time. Think of it as flattening the BST into a sorted list and then iterating through it, but done efficiently without actually creating the list.

**Example Walkthrough:**
```
BST:
      7
     / \
    3   15
       /  \
      9    20

Iterator usage:
  BSTIterator it = BSTIterator(root)
  it.next()     → 3     (smallest)
  it.next()     → 7     (next smallest)
  it.next()     → 9     (next)
  it.hasNext()  → True
  it.next()     → 15
  it.next()     → 20
  it.hasNext()  → False
```

**Detailed Approach with Algorithm Steps:**
1. **Initialization:** Create an empty stack. Push all nodes along the leftmost path from root to the stack (this gives us the smallest element at the top).
2. **_push_left(node):** Helper that pushes a node and all its left descendants onto the stack.
3. **next():**
   - Pop the top node from the stack (which is the current smallest unvisited node).
   - If this node has a right child, call _push_left on it (to prepare the next inorder successor).
   - Return the popped node's value.
4. **hasNext():** Return True if stack is non-empty (there are more nodes to visit).

**Visual Tree Diagram:**
```
Stack states during iteration:

BST:
      7
     / \
    3   15
       /  \
      9    20

Initial: stack = [7, 3] (pushed 7, then leftmost path 7→3)
         top = 3 (smallest element)

next(): pop 3 → return 3
  Stack: [7]
  3 has no right child → nothing to push

next(): pop 7 → return 7
  Stack: []
  7 has right=15 → push 15 and its left chain: push 15, push 9
  Stack: [15, 9]

next(): pop 9 → return 9
  Stack: [15]
  9 has no right child → nothing to push

next(): pop 15 → return 15
  Stack: []
  15 has right=20 → push 20 (no left children)
  Stack: [20]

next(): pop 20 → return 20
  Stack: [] → empty
  hasNext() → False
```

**Step-by-Step Trace:**
```
BST: [7, 3, 15, null, null, 9, 20]

BSTIterator(root):
  _push_left(7):
    push 7, push 3 (left of 7)
  stack = [7, 3]

hasNext(): len(stack)=2 > 0 → True

next():
  pop → 3, stack = [7]
  3.right = None → nothing to push
  return 3

next():
  pop → 7, stack = []
  7.right = 15 → _push_left(15): push 15, push 9
  stack = [15, 9]
  return 7

next():
  pop → 9, stack = [15]
  9.right = None
  return 9

next():
  pop → 15, stack = []
  15.right = 20 → _push_left(20): push 20
  stack = [20]
  return 15

next():
  pop → 20, stack = []
  20.right = None
  return 20

hasNext(): stack = [] → False ✅
```

**Well-Commented Code:**
```python
class BSTIterator:
    def __init__(self, root: TreeNode):
        """Initialize the iterator with the BST root."""
        self.stack = []
        self._push_left(root)  # Push leftmost path onto stack

    def _push_left(self, node: TreeNode):
        """Push a node and all its left descendants onto the stack."""
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        """Return the next smallest element in the BST."""
        # Pop the current smallest unvisited node
        node = self.stack.pop()

        # If the node has a right child, push its leftmost path
        # This is the next subtree to explore
        if node.right:
            self._push_left(node.right)

        return node.val

    def hasNext(self) -> bool:
        """Return True if there are more elements to iterate."""
        return len(self.stack) > 0
```

**Complexity Analysis:**
- **Time:** O(1) amortized for next(), O(1) for hasNext()
  - Each node is pushed and popped exactly once across the entire iteration
  - Individual next() calls are O(h) worst-case (when pushing left chain of right child)
- **Space:** O(h) — stack holds at most h nodes at any time

**Edge Cases with Examples:**
| Input | Sequence | Reason |
|-------|----------|--------|
| `[1]` | `[1]` | Single node |
| `[2,1,3]` | `[1,2,3]` | Normal 3-node BST |
| `[]` | `[]` | Empty tree, hasNext()=False |
| Skewed left `[3,2,1]` | `[1,2,3]` | Stack will contain all nodes initially |

**Common Mistakes:**
- ❌ Flattening the entire BST into a list (uses O(n) space instead of O(h))
- ❌ Not pushing the left chain when a right child exists — breaks the inorder sequence
- ❌ Popping without handling the right child's left subtree
- ❌ Forgetting that the iterator should work one step at a time

**Pattern Recognition Hints:**
- **Inorder Without Recursion:** The stack-based approach simulates recursive inorder traversal
- **Controlled Recursion:** This is a pattern for building iterators over tree data structures
- **Amortized Analysis:** O(1) amortized means expensive operations are rare enough that the average is O(1)
- **Follow-up Question:** "Implement hasPrev() and prev()" — see Problem 35 in Batch 2

---

## Problem 25: Flatten Binary Tree to Linked List

**Problem Statement:**
Given the root of a binary tree, flatten the tree into a linked list in-place. The "linked list" should use the same TreeNode class, where the right child points to the next node and the left child is always NULL.

**Problem Explanation in Simple Words:**
Turn the tree into a linked list that follows the order of preorder traversal. All left children become None, and the right pointers form a chain. It must be done in-place (modify the original tree, not create a new one).

**Example Walkthrough:**
```
Input Tree:
     1
    / \
   2   5
  / \   \
 3   4   6

Preorder: [1, 2, 3, 4, 5, 6]

Output (flattened):
 1 → 2 → 3 → 4 → 5 → 6 → None
     ↘   ↘   ↘   ↘   ↘
     (every left child is None)
```

**Detailed Approach with Algorithm Steps:**
1. Start with `curr = root`.
2. While `curr` is not None:
   a. If `curr` has a left child:
      - Find the rightmost node in the left subtree (predecessor).
      - Connect predecessor's right to `curr.right` (rewire: left subtree's tail → right subtree).
      - Move `curr.left` to `curr.right` (move left subtree to right).
      - Set `curr.left = None`.
   b. Move `curr` to `curr.right` (continue down the chain).
3. The tree is now flattened in-place.

**Visual Tree Diagram:**
```
Step-by-step flattening:

Initial:
      1
     / \
    2   5
   / \   \
  3   4   6

Step 1 (curr=1): has left=2
  Find rightmost in left subtree: 4
  4.right = 1.right (5's subtree)
  1.right = 1.left (2's subtree)
  1.left = None
      1
       \
        2
       / \
      3   4
           \
            5
             \
              6

Step 2 (curr=2): has left=3
  Find rightmost in left: 3
  3.right = 2.right (4's subtree)
  2.right = 2.left (3)
  2.left = None
      1
       \
        2
         \
          3
           \
            4
             \
              5
               \
                6

Step 3 (curr=3): no left, curr=3.right=4
Step 4 (curr=4): no left, curr=4.right=5
...
Done! All left children are None ✅
```

**Step-by-Step Trace:**
```
Input: [1,2,5,3,4,null,6]

curr = 1:
  left exists (2) → find rightmost: 4
  4.right = 5 (the right subtree)
  1.right = 2 (move left to right)
  1.left = None
curr = 2:
  left exists (3) → find rightmost: 3
  3.right = 4 (the right subtree, which now includes 5,6)
  2.right = 3 (move left to right)
  2.left = None
curr = 3:
  no left → curr = 4
curr = 4:
  no left → curr = 5
curr = 5:
  no left → curr = 6
curr = 6:
  no left → curr = None → done

Result: 1→2→3→4→5→6
```

**Well-Commented Code:**
```python
class Solution:
    def flatten(self, root: TreeNode) -> None:
        """Flatten tree to linked list in-place using Morris-like traversal."""
        curr = root

        while curr:
            # If current node has a left child, we need to rewire
            if curr.left:
                # Step 1: Find the rightmost node in the left subtree
                # This will be the predecessor in preorder
                rightmost = curr.left
                while rightmost.right:
                    rightmost = rightmost.right

                # Step 2: Connect predecessor to current's right subtree
                rightmost.right = curr.right

                # Step 3: Move left subtree to the right side
                curr.right = curr.left

                # Step 4: Set left child to None
                curr.left = None

            # Move to the next node (always go right now)
            curr = curr.right
```

**Complexity Analysis:**
- **Time:** O(n) — each node visited at most twice (once in main loop, once finding rightmost)
- **Space:** O(1) — iterative, no extra space (besides the input tree modifications)

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[]` | `[]` | Empty tree |
| `[1]` | `[1]` | Single node, already flattened |
| `[1,2]` | `[1,null,2]` | Simple left child |
| `[1,null,2]` | `[1,null,2]` | Already flattened (no left children) |
| `[1,2,3]` | `[1,null,2,null,3]` | Chain flattened in order |

**Common Mistakes:**
- ❌ Creating a new tree instead of modifying in-place
- ❌ Forgetting to set `left = None` after moving it to the right
- ❌ Not finding the actual rightmost node — traversing past None and losing the connection
- ❌ Using recursion (O(h) space) instead of the O(1) space iterative approach
- ❌ Confusing with "increasing BST" (Problem 4, Batch 2) which uses inorder instead of preorder

**Pattern Recognition Hints:**
- **Morris-like Traversal:** Uses threaded tree concepts without extra space
- **Preorder Chain:** The flattened order is exactly preorder traversal
- **Reverse Post-order Alternative:** Process right-left-root and link as you go (also works)
- **In-place Transformation:** A common theme in tree problems — modify existing structure instead of building new

---

# HARD PROBLEMS (26-35)

---

## Problem 26: Binary Tree Cameras

**Problem Statement:**
You are given the root of a binary tree. We install cameras on the tree nodes. Each camera at a node can monitor its parent, itself, and its immediate children. Return the minimum number of cameras needed to monitor all nodes.

**Example:**
```
Input: [0,0,null,0,0]
Output: 1
```

**Approach:**
Use post-order traversal with states: 0 = not covered, 1 = has camera, 2 = covered (no camera). A camera is needed when a child is not covered. Place camera at uncovered node's parent.

```python
class Solution:
    def minCameraCover(self, root: TreeNode) -> int:
        self.cameras = 0
        
        def dfs(node):
            if not node:
                return 2
            left = dfs(node.left)
            right = dfs(node.right)
            if left == 0 or right == 0:
                self.cameras += 1
                return 1
            if left == 1 or right == 1:
                return 2
            return 0
        
        if dfs(root) == 0:
            self.cameras += 1
        return self.cameras
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** States: 0 = uncovered, 1 = has camera, 2 = covered. Post-order ensures children are processed before parent. Place cameras as late as possible (at parent) for optimal placement.

---

## Problem 27: House Robber III

**Problem Statement:**
The thief has found a new place to rob with a binary tree structure. Each node has a certain amount of money. If two directly-linked nodes are both robbed, the alarm goes off. Find the maximum amount the thief can rob without alerting the police.

**Example:**
```
Input: [3,2,3,null,3,null,1]
Output: 7 (rob 3 + 3 + 1 = 7)
```

**Approach:**
For each node, return a tuple: (max money if we rob this node, max money if we don't rob this node). If we rob this node, we can't rob children. If we don't, we take max from children.

```python
class Solution:
    def rob(self, root: TreeNode) -> int:
        def dfs(node):
            if not node:
                return (0, 0)
            left = dfs(node.left)
            right = dfs(node.right)
            rob_this = node.val + left[1] + right[1]
            skip_this = max(left) + max(right)
            return (rob_this, skip_this)
        
        return max(dfs(root))
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** Tree DP with two states per node: rob or skip. Return both values and let parent decide. This pattern works for many tree optimization problems.

---

## Problem 28: Vertical Order Traversal of Binary Tree

**Problem Statement:**
Given the root of a binary tree, calculate the vertical order traversal. For each vertical column, nodes should be listed from top to bottom, and within the same row and column, nodes should be sorted by value.

**Example:**
```
Input: [3,9,20,null,null,15,7]
Output: [[9],[3,15],[20],[7]]
```

**Approach:**
Use BFS or DFS to track column, row, and value for each node. Group by column, then sort by row and value within each column.

```python
from collections import defaultdict, deque

class Solution:
    def verticalTraversal(self, root: TreeNode) -> list:
        nodes = []
        queue = deque([(root, 0, 0)])
        while queue:
            node, row, col = queue.popleft()
            if node:
                nodes.append((col, row, node.val))
                queue.append((node.left, row + 1, col - 1))
                queue.append((node.right, row + 1, col + 1))
        
        nodes.sort()
        result = []
        prev_col = None
        for col, row, val in nodes:
            if col != prev_col:
                result.append([])
                prev_col = col
            result[-1].append(val)
        return result
```

**Complexity:**
- Time: O(n log n) - sorting nodes
- Space: O(n) - storing all nodes

**Trick/Tip:** Use tuple (col, row, val) for sorting. Python's tuple comparison sorts by first element, then second, etc. This automatically handles the required ordering.

---

## Problem 29: Morris Traversal (Inorder, O(1) Space)

**Problem Statement:**
Implement inorder traversal of a binary tree using O(1) extra space (no recursion, no stack). This is called Morris Traversal.

**Approach:**
Use threaded binary tree concept. For each node, find its inorder predecessor and create a temporary link from predecessor to current node. This allows us to return to the parent without a stack.

```python
class Solution:
    def morrisInorder(self, root: TreeNode) -> list:
        result = []
        curr = root
        while curr:
            if not curr.left:
                result.append(curr.val)
                curr = curr.right
            else:
                predecessor = curr.left
                while predecessor.right and predecessor.right != curr:
                    predecessor = predecessor.right
                if not predecessor.right:
                    predecessor.right = curr
                    curr = curr.left
                else:
                    predecessor.right = None
                    result.append(curr.val)
                    curr = curr.right
        return result
```

**Complexity:**
- Time: O(n) - each node visited at most twice
- Space: O(1) - no extra space

**Trick/Tip:** When moving to left subtree, create a thread from inorder predecessor back to current node. When we return via the thread, we know we've visited the left subtree and can process current node. Remove thread after use.

---

## Problem 30: Count Nodes Equal to Average of Subtree

**Problem Statement:**
Given the root of a binary tree, return the number of nodes where the value of the node equals the average of the values in its subtree. The average is the sum divided by count, rounded down.

**Example:**
```
Input: [4,8,5,0,1,null,6]
Output: 5
```

**Approach:**
Use post-order traversal. At each node, calculate sum and count of its subtree. Compare node's value with average. Return (sum, count) to parent.

```python
class Solution:
    def averageOfSubtree(self, root: TreeNode) -> int:
        self.count = 0
        
        def dfs(node):
            if not node:
                return (0, 0)
            left_sum, left_count = dfs(node.left)
            right_sum, right_count = dfs(node.right)
            total_sum = left_sum + right_sum + node.val
            total_count = left_count + right_count + 1
            if node.val == total_sum // total_count:
                self.count += 1
            return (total_sum, total_count)
        
        dfs(root)
        return self.count
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(h) - recursion stack

**Trick/Tip:** Return both sum and count from each subtree to avoid recalculation. Post-order ensures children are processed before parent.

---

## Problem 31: Maximum Width of Binary Tree

**Problem Statement:**
Given the root of a binary tree, return the maximum width of the tree. Width is the number of nodes between the leftmost and rightmost non-null nodes (including null nodes in between) at the same level.

**Example:**
```
Input: [1,3,2,5,3,null,9]
Output: 4 (level 2 has nodes at positions 1,2,3,4)
```

**Approach:**
Use BFS with position numbering. Root is at position 0. Left child at 2*pos, right child at 2*pos+1. Width at each level = max_pos - min_pos + 1.

```python
from collections import deque

class Solution:
    def widthOfBinaryTree(self, root: TreeNode) -> int:
        if not root:
            return 0
        max_width = 0
        queue = deque([(root, 0)])
        while queue:
            level_size = len(queue)
            min_pos = queue[0][1]
            max_pos = queue[-1][1]
            max_width = max(max_width, max_pos - min_pos + 1)
            for _ in range(level_size):
                node, pos = queue.popleft()
                if node.left:
                    queue.append((node.left, 2 * pos))
                if node.right:
                    queue.append((node.right, 2 * pos + 1))
        return max_width
```

**Complexity:**
- Time: O(n) - visit each node once
- Space: O(n) - queue size

**Trick/Tip:** Normalize positions at each level by subtracting the minimum position to avoid overflow. This handles skewed trees where positions can become very large.

---

## Problem 32: All Nodes Distance K in Binary Tree

**Problem Statement:**
Given the root of a binary tree, a target node, and an integer k, return a list of all nodes that are exactly k distance from the target node.

**Example:**
```
Input: root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2
Output: [7,4,1]
```

**Approach:**
First, build a parent map using BFS/DFS. Then from target, do BFS in all directions (left, right, parent) for k steps. Use a visited set to avoid revisiting nodes.

```python
from collections import deque

class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> list:
        parent = {}
        
        def build_parent(node, par=None):
            if node:
                parent[node] = par
                build_parent(node.left, node)
                build_parent(node.right, node)
        
        build_parent(root)
        
        queue = deque([(target, 0)])
        visited = {target}
        result = []
        
        while queue:
            node, dist = queue.popleft()
            if dist == k:
                result.append(node.val)
            elif dist < k:
                for neighbor in [node.left, node.right, parent[node]]:
                    if neighbor and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, dist + 1))
        
        return result
```

**Complexity:**
- Time: O(n) - build parent map and BFS
- Space: O(n) - parent map, queue, visited set

**Trick/Tip:** Convert tree to graph by adding parent pointers. Then use BFS from target. This technique works for many "distance in tree" problems.

---

## Problem 33: Burn the Tree

**Problem Statement:**
Given a binary tree and a target node, find the minimum time required to burn the entire tree. Burning starts from the target node and spreads to adjacent nodes (parent, left, right) each second.

**Example:**
```
Input:     1
          / \
         2   3
        /   / \
       4   5   6
      /
     7
Target: 4, Output: 5 seconds
```

**Approach:**
Build parent map and convert tree to graph. BFS from target, tracking time. The last node reached gives the minimum burn time.

```python
from collections import deque

class Solution:
    def burnTree(self, root: TreeNode, target: TreeNode) -> int:
        parent = {}
        
        def build_parent(node, par=None):
            if node:
                parent[node] = par
                build_parent(node.left, node)
                build_parent(node.right, node)
        
        build_parent(root)
        
        queue = deque([(target, 0)])
        visited = {target}
        max_time = 0
        
        while queue:
            node, time = queue.popleft()
            max_time = max(max_time, time)
            for neighbor in [node.left, node.right, parent[node]]:
                if neighbor and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, time + 1))
        
        return max_time
```

**Complexity:**
- Time: O(n) - build parent map and BFS
- Space: O(n) - parent map, queue, visited set

**Trick/Tip:** Same as Problem 32 but we take max time instead of collecting nodes at distance k. Tree-to-graph conversion is key.

---

## Problem 34: Find Duplicate Subtrees

**Problem Statement:**
Given the root of a binary tree, return all duplicate subtrees. Two trees are duplicate if they have the same structure and node values. Return the root node of each duplicate subtree.

**Example:**
```
Input: [1,2,3,4,null,2,4,null,null,4]
Output: [[2,4],[4]]
```

**Approach:**
Serialize each subtree. Use a hashmap to count occurrences. If a serialization appears more than once, it's a duplicate.

```python
from collections import defaultdict

class Solution:
    def findDuplicateSubtrees(self, root: TreeNode) -> list:
        serial_count = defaultdict(int)
        result = []
        
        def serialize(node):
            if not node:
                return "#"
            serial = str(node.val) + "," + serialize(node.left) + "," + serialize(node.right)
            serial_count[serial] += 1
            if serial_count[serial] == 2:
                result.append(node)
            return serial
        
        serialize(root)
        return result
```

**Complexity:**
- Time: O(n²) - serialization takes O(n) per node
- Space: O(n²) - storing serializations

**Trick/Tip:** Serialization is the key to comparing subtrees. Use a delimiter (comma) to avoid ambiguity. Only add to result when count == 2 to avoid duplicates in result.

---

## Problem 35: Sum of Distances in Tree

**Problem Statement:**
Given an undirected tree with n nodes (0 to n-1) and n-1 edges, return an array answer where answer[i] is the sum of distances between node i and all other nodes.

**Example:**
```
Input: n = 6, edges = [[0,1],[0,2],[2,3],[2,4],[2,5]]
Output: [8,6,4,5,5,5]
```

**Approach:**
Use two-pass DFS. First, compute answer[0] (root) and count of nodes in each subtree. Then, reroot the tree: when moving root from parent to child, answer[child] = answer[parent] - count[child] + (n - count[child]).

```python
from collections import defaultdict

class Solution:
    def sumOfDistancesInTree(self, n: int, edges: list) -> list:
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        
        count = [1] * n
        answer = [0] * n
        
        def dfs1(node, parent):
            for neighbor in graph[node]:
                if neighbor != parent:
                    dfs1(neighbor, node)
                    count[node] += count[neighbor]
                    answer[node] += answer[neighbor] + count[neighbor]
        
        def dfs2(node, parent):
            for neighbor in graph[node]:
                if neighbor != parent:
                    answer[neighbor] = answer[node] - count[neighbor] + (n - count[neighbor])
                    dfs2(neighbor, node)
        
        dfs1(0, -1)
        dfs2(0, -1)
        return answer
```

**Complexity:**
- Time: O(n) - two passes of DFS
- Space: O(n) - count and answer arrays

**Trick/Tip:** The rerooting formula is key: when moving root from parent to child, distances to nodes in child's subtree decrease by 1, distances to all other nodes increase by 1. This gives: answer[child] = answer[parent] - count[child] + (n - count[child]).

---

# 📚 QUICK REFERENCE

## Common Patterns

| Pattern | Problems |
|---------|----------|
| DFS Recursion | 1, 2, 3, 4, 5, 6, 8, 9, 11, 15, 18, 19, 25, 26, 27, 30 |
| BFS Level Order | 7, 13, 14, 20, 23, 28, 31, 32, 33 |
| BST Properties | 12, 16, 24 |
| Tree Serialization | 17, 34 |
| Tree-to-Graph | 32, 33, 35 |
| Post-order Traversal | 22, 26, 27, 30 |
| Pre-order Traversal | 21, 25 |
| Inorder Traversal | 12, 24, 29 |

## Complexity Summary

| Complexity | Problems |
|------------|----------|
| O(n) Time | 1-10, 11, 13-16, 18, 20-23, 26-30, 32, 33, 35 |
| O(n log n) Time | 28 |
| O(n²) Time | 4, 21, 22, 34 |
| O(1) Space | 16, 25, 29 |
| O(n) Space | 13, 14, 20, 23, 28, 31 |

## Key Insights

1. **Tree Recursion**: Most tree problems can be solved with simple recursion. Master the pattern first.
2. **BFS vs DFS**: Use BFS for level-by-level problems, DFS for path/subtree problems.
3. **Global Variables**: Use self.var or nonlocal to track results across recursive calls.
4. **Backtracking**: Use path.pop() after recursive call to restore state.
5. **Threaded Trees**: Morris traversal shows how to traverse without stack by creating temporary links.

---

*Total Problems: 35 | Easy: 10 | Medium: 15 | Hard: 10*
