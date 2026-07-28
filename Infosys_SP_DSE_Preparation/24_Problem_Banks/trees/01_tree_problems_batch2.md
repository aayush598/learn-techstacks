# Tree Problems Batch 2 - Infosys SP DSE Preparation

> **40 More Tree Problems** | Complete Python Solutions | Easy -> Hard
> Companion to `tree_problems_batch1.md`

---

## TreeNode Class Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Node:
    """N-ary Tree Node"""
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children else []
```

---

---

# EASY PROBLEMS (1-12)

---

## Problem 1: Sum of Left Leaves

**Statement:** Given a binary tree, return the sum of all left leaves. A left leaf is a leaf node that is the left child of its parent.

**Problem Explanation in Simple Words:**
Walk through the tree. Whenever you find a node that is a LEFT child of its parent AND has no children of its own (a leaf), add its value to the total. Right leaves don't count. Non-leaf left children don't count (only leaves).

**Example:**
```
Input Tree:
     3
    / \
   9  20
      /  \
     15   7

Left leaves: 9 (left child of 3, no children)
             15 (left child of 20, no children)
Sum = 9 + 15 = 24
```

**Detailed Approach with Algorithm Steps:**
1. **Base Case:** If root is None, return 0.
2. **Check Left Child:** If left child exists:
   - If it's a leaf (no left/right children), add its value.
   - Otherwise, recursively process the left subtree.
3. **Process Right:** Recursively process the right subtree (right child could have left leaves deeper down).
4. **Return:** Total sum accumulated.

**Visual Tree Diagram:**
```
        3
       / \
     [9] 20    ← 9 is a left leaf (sum += 9)
         /  \
       [15] 7  ← 15 is a left leaf (sum += 15)

Labels:
  [ ] = left leaf (counted)
  ( ) = not counted
```

**Step-by-Step Trace with Input `[3,9,20,null,null,15,7]`:**
```
sumOfLeftLeaves(3):
  root.left=9: is leaf? yes → total+=9
  root.right=20: not left child → skip direct check
  sumOfLeftLeaves(20):
    root.left=15: is leaf? yes → total+=15
    root.right=7: not left child → skip
    sumOfLeftLeaves(15): left=none, right=none → return 0
    sumOfLeftLeaves(7): left=none, right=none → return 0
    return 15
  sumOfLeftLeaves(9): left=none, right=none → return 0
  return 9 + 0 + 15 = 24 ✅
```

**Well-Commented Code:**
```python
def sumOfLeftLeaves(root):
    # Base case: empty tree
    if not root:
        return 0

    total = 0

    # Check if left child exists
    if root.left:
        # If left child is a leaf, add its value
        if not root.left.left and not root.left.right:
            total += root.left.val
        else:
            # Otherwise, recursively explore left subtree
            total += sumOfLeftLeaves(root.left)

    # Recursively explore right subtree (may contain left leaves deeper down)
    total += sumOfLeftLeaves(root.right)

    return total
```

**Complexity Analysis:**
- **Time:** O(n) — visit every node exactly once
- **Space:** O(h) — recursion stack, h = height of tree

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[]` | 0 | Empty tree |
| `[1]` | 0 | Single node has no left leaves |
| `[1,2]` | 2 | 2 is left leaf |
| `[1,null,3]` | 0 | Right child is not counted |
| `[1,2,3,4]` | 4 | 4 is left leaf of 2 |

**Common Mistakes:**
- ❌ Counting right leaves — only left leaves count
- ❌ Counting non-leaf left children — only leaves count
- ❌ Not checking that the left child is actually a leaf
- ❌ Forgetting to recurse on the right subtree (might contain left leaves deeper)

**Pattern Recognition Hints:**
- **Conditional Leaf Detection:** Checks both position (left child) AND type (leaf)
- **Two-level Check:** Need to check grandchild (node.left.left) from grandparent level
- **Recursive Summation:** Accumulate results from left and right subtrees

---

## Problem 2: Two Sum IV - BST

**Statement:** Given the root of a BST and an integer k, return true if there exist two nodes such that their values sum to k.

**Problem Explanation in Simple Words:**
This is the "Two Sum" problem on a BST. Find any two different nodes whose values add up to k. The tree is a BST, but we mainly just need to visit all nodes and check if we've seen the complement before.

**Example:**
```
BST:        k = 9
    5
   / \
  3   6
 / \   \
2   4   7

2 + 7 = 9 → True ✅
3 + 6 = 9 → True ✅
4 + 5 = 9 → True ✅
```

**Detailed Approach with Algorithm Steps:**
1. **Initialize:** Create an empty hash set `seen`.
2. **DFS Traversal:** Recursively traverse the BST:
   - If node is None, return False.
   - Compute `complement = k - node.val`.
   - If complement is already in the set → found a pair → return True.
   - Add current node's value to the set.
   - Recursively check left and right subtrees.
3. **Return:** True if any pair found, False otherwise.

**Visual Tree Diagram:**
```
Set contents during traversal (DFS order: 5→3→2→4→6→7):

Step 1: visit 5, complement=4, seen={}, 4∉seen → seen={5}
Step 2: visit 3, complement=6, seen={5}, 6∉seen → seen={5,3}
Step 3: visit 2, complement=7, seen={5,3}, 7∉seen → seen={5,3,2}
Step 4: visit 4, complement=5, seen={5,3,2}, 5∈seen! → True ✅
```

**Step-by-Step Trace with Input `[5,3,6,2,4,null,7], k=9`:**
```
findTarget(5, 9):
  complement = 4, not in seen → add 5, seen={5}
  dfs(3):
    complement = 6, not in seen → add 3, seen={5,3}
    dfs(2):
      complement = 7, not in seen → add 2, seen={5,3,2}
      dfs(None) → False
      dfs(None) → False
      return False
    dfs(4):
      complement = 5, IN seen! → True ✅
      return True
    return True
  return True ✅
```

**Well-Commented Code:**
```python
def findTarget(root, k):
    seen = set()  # Store values we've visited

    def dfs(node):
        if not node:
            return False

        # Check if complement exists among previously visited nodes
        complement = k - node.val
        if complement in seen:
            return True  # Found a pair that sums to k

        # Add current value for future lookups
        seen.add(node.val)

        # Continue searching in left and right subtrees
        return dfs(node.left) or dfs(node.right)

    return dfs(root)
```

**Complexity Analysis:**
- **Time:** O(n) — visit each node once
- **Space:** O(n) — set may store up to n values

**Edge Cases with Examples:**
| Input | k | Output | Reason |
|-------|---|--------|--------|
| `[1]` | 2 | False | Only one node, need two |
| `[2,1,3]` | 4 | True | 1+3=4 |
| `[1,2]` | 3 | True | 1+2=3 |
| Empty | any | False | No nodes to sum |
| All values > k/2 | small k | Depends | May not find complement |

**Common Mistakes:**
- ❌ Using two-pointer on inorder array (works but O(n) extra space for array)
- ❌ Counting the same node twice — the set ensures we only match with previously visited nodes
- ❌ Not adding current node to set before recursing — needed for future complement checks
- ❌ Forgetting that the pair must be two DIFFERENT nodes

**Pattern Recognition Hints:**
- **Hash Set Pattern:** Classic "Two Sum" adapted for trees — trade space for time
- **BST Alternative:** Inorder + two-pointer gives O(n) time, O(h) space
- **DFS with State:** Passing context (seen set) through recursive traversal
- **Any-order Traversal:** The approach works with ANY traversal order, not just DFS

---

## Problem 3: Find Mode in BST

**Statement:** Given a BST with duplicates, return all modes (most frequently occurring values) in any order.

**Problem Explanation in Simple Words:**
Find which value(s) appear most frequently in the BST. Since this is a BST with possible duplicates, inorder traversal gives us sorted order, making duplicates adjacent. Track the count of each value and collect the ones with max frequency.

**Example:**
```
BST:
    1
     \
      2
     / \
    2   3

Inorder: [1, 2, 2, 3]
Frequencies: 1→1, 2→2, 3→1
Mode(s): [2] (appears twice)
```

**Detailed Approach with Algorithm Steps:**
1. **Initialize:** result list, prev_val=None, curr_count=0, max_count=0.
2. **Inorder Traversal:**
   - If node is None, return.
   - Recursively traverse left subtree.
   - If current value equals previous: increment curr_count.
   - Otherwise: reset curr_count=1, update prev_val.
   - If curr_count > max_count: new mode found → clear result, add current value, update max_count.
   - If curr_count == max_count: add current value to result.
   - Recursively traverse right subtree.
3. **Return result.**

**Visual Tree Diagram:**
```
BST:
       1
     /   \
    2     2
   / \   / \
  2   3 3   4

Inorder: [2, 2, 2, 3, 1, 3, 2, 4]
                                      (wait, this isn't a valid BST)
Proper BST with duplicates (values duplicated across positions):
    2
   / \
  1   3
     / \
    2   4

Inorder: [1, 2, 2, 3, 4]
Frequencies: 1→1, 2→2, 3→1, 4→1
Mode: [2]
```

**Step-by-Step Trace with Input `[1,null,2,2]`:**
```
Initialize: result=[], prev=None, curr=0, max=0

inorder(1):
  inorder(None): return
  node.val=1: prev=None → curr=1, prev=1
    curr=1 > max=0 → max=1, result=[1]
  inorder(2):
    inorder(2):
      inorder(None): return
      node.val=2: prev=1 → curr=1, prev=2
        curr=1 == max=1 → result=[1,2]
      inorder(None): return
    node.val=2: prev=2 → curr=2, prev=2
      curr=2 > max=1 → max=2, result=[2]
    inorder(None): return

Result: [2] ✅ (2 appears twice, 1 appears once)
```

**Well-Commented Code:**
```python
def findMode(root):
    result = []
    prev_val = None   # Previously visited value
    curr_count = 0    # Count of current value
    max_count = 0     # Maximum frequency seen so far

    def inorder(node):
        nonlocal prev_val, curr_count, max_count
        if not node:
            return

        inorder(node.left)

        # Count occurrences of current value
        if node.val == prev_val:
            curr_count += 1      # Same value continues
        else:
            curr_count = 1        # New value starts
            prev_val = node.val

        # Update result based on frequency
        if curr_count > max_count:
            max_count = curr_count
            result.clear()        # Previous modes are no longer modes
            result.append(node.val)
        elif curr_count == max_count:
            result.append(node.val)  # Another value with max frequency

        inorder(node.right)

    inorder(root)
    return result
```

**Complexity Analysis:**
- **Time:** O(n) — single inorder traversal visits all nodes
- **Space:** O(h) — recursion stack; O(n) worst case for result if all values are modes

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[1]` | `[1]` | Single node is the mode |
| `[1,null,2]` | `[1,2]` | Both appear once |
| `[1,1,2]` | `[1]` | 1 appears twice |
| Empty | `[]` | No nodes, no mode |
| All same value | `[val]` | All nodes are same value |

**Common Mistakes:**
- ❌ Using a hashmap (extra O(n) space) instead of the BST property for O(1) extra space
- ❌ Forgetting to clear the result list when a new higher frequency is found
- ❌ Not resetting count when the value changes
- ❌ Only collecting one mode when multiple values have the same max frequency

**Pattern Recognition Hints:**
- **BST + Inorder = Sorted:** The sorted property means duplicates are adjacent — reduces space
- **Online Mode Tracking:** Find mode in a single pass without storing all frequencies
- **Non-BST Alternative:** Use hashmap to count frequencies, then find max

---

## Problem 4: Increasing BST

**Statement:** Given a BST, rearrange it in-place so that the leftmost node becomes the root, each node has no left child, and each node has only one right child (increasing order).

**Problem Explanation in Simple Words:**
Straighten the BST into a "right-leaning" chain where nodes are in sorted order (increasing). The smallest element becomes the new root, and every node has only a right child (no left child). It's like flattening into a linked list following inorder order.

**Example:**
```
Input:
    5
   / \
  3   6
 / \   \
2   4   8
       / \
      7   9

Output:
 2
  \
   3
    \
     4
      \
       5
        \
         6
          \
           7
            \
             8
              \
               9
```

**Detailed Approach with Algorithm Steps:**
1. **Dummy Node:** Create a dummy root (value 0) to simplify linking — its right child will be the new root.
2. **Inorder Traversal:**
   - Recursively traverse left subtree.
   - Set current node's left child to None.
   - Attach current node as right child of the previous node.
   - Move the pointer to current node.
   - Recursively traverse right subtree.
3. **Return:** dummy.right — the new root (smallest element).

**Visual Tree Diagram:**
```
Building the increasing tree:

Dummy → ... (building chain)

After inorder(2):
dummy.right = 2, curr = 2
  2

After inorder(3):
2.right = 3, curr = 3
  2
   \
    3

After inorder(4):
3.right = 4, curr = 4
  2
   \
    3
     \
      4

... continues building chain in order
```

**Step-by-Step Trace with Input `[5,3,6,2,4,null,8]`:**
```
Initialize: dummy=0, curr=dummy

inorder(5):
  inorder(3):
    inorder(2):
      inorder(None): return
      node=2: left=None, curr.right=2, curr=2
      inorder(None): return
    node=3: left=None, curr.right=3, curr=3
    inorder(4):
      node=4: left=None, curr.right=4, curr=4
      return
  node=5: left=None, curr.right=5, curr=5
  inorder(6):
    inorder(None): return
    node=6: left=None, curr.right=6, curr=6
    inorder(8):
      inorder(7):
        node=7: left=None, curr.right=7, curr=7
        return
      node=8: left=None, curr.right=8, curr=8
      inorder(9):
        node=9: left=None, curr.right=9, curr=9
        return

Return dummy.right → 2→3→4→5→6→7→8→9
```

**Well-Commented Code:**
```python
def increasingBST(root):
    # Dummy node simplifies edge case of attaching the first node
    dummy = TreeNode(0)
    curr = dummy  # Pointer to the last node in the chain

    def inorder(node):
        nonlocal curr
        if not node:
            return

        # Process left subtree (smaller elements)
        inorder(node.left)

        # Disconnect left child and attach to chain
        node.left = None
        curr.right = node  # Previous node points to current
        curr = node        # Move pointer forward

        # Process right subtree (larger elements)
        inorder(node.right)

    inorder(root)
    return dummy.right  # New root (smallest element)
```

**Complexity Analysis:**
- **Time:** O(n) — visit each node once during inorder traversal
- **Space:** O(h) — recursion stack

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[]` | `[]` | Empty tree |
| `[1]` | `[1]` | Single node, already in order |
| `[2,1,3]` | `[1,null,2,null,3]` | Simple BST |
| `[1,null,2,null,3]` | Same | Already increasing |

**Common Mistakes:**
- ❌ Forgetting to set `node.left = None` — left children must be cleaned up
- ❌ Modifying the tree while traversing without the dummy node — first node attachment is tricky
- ❌ Not using `nonlocal curr` — Python requires this for modifying closure variables
- ❌ Reversing order (building decreasing instead of increasing chain)

**Pattern Recognition Hints:**
- **Dummy Node Pattern:** Simplifies linked list building — avoids special case for first node
- **Inorder Building:** Process in sorted order and link nodes as they are visited
- **In-place Transformation:** Modifies existing nodes rather than creating new ones
- **Related to Flatten:** Problem 25 from Batch 1 also flattens but in preorder, not inorder

---

## Problem 5: Range Sum of BST

**Statement:** Given a BST root and two integers low and high, return the sum of all node values in the range [low, high].

**Problem Explanation in Simple Words:**
Add up all the node values that fall within the given range [low, high]. Since it's a BST, we can skip entire subtrees that are guaranteed to be out of range. If a node is smaller than low, its entire left subtree is also smaller → skip it. If a node is larger than high, its entire right subtree is also larger → skip it.

**Example:**
```
BST:        low=7, high=15
      10
     /  \
    5    15
   / \     \
  3   7     18

Values in [7,15]: 10, 7, 15
Sum = 10 + 7 + 15 = 32
```

**Detailed Approach with Algorithm Steps:**
1. **Base Case:** If node is None, return 0.
2. **Out of Range (low):** If node.val < low, everything in left subtree is also < low → skip left, only recurse right.
3. **Out of Range (high):** If node.val > high, everything in right subtree is also > high → skip right, only recurse left.
4. **In Range:** If low <= node.val <= high, add node.val and recurse both sides.

**Visual Tree Diagram:**
```
BST pruning with low=7, high=15:
      10 ← in range (7≤10≤15)
     /  \
    5 ← too small   15 ← in range
   / \     \
  3   7 ← in range  18 ← too big
     (right subtree
      only for 5)

Path: 10 → add 10, check left(5) and right(15)
  5: 5<7 → skip left(3), check right(7)
    7: 7≥7 → add 7, recurse children (None)
  15: 15≤15 → add 15, check left(None), right(18)
    18: 18>15 → skip right, check left(None)

Sum = 10 + 7 + 15 = 32 ✅
```

**Step-by-Step Trace with Input `[10,5,15,3,7,null,18], low=7, high=15`:**
```
rangeSumBST(10, 7, 15): 7≤10≤15 → sum += 10
  rangeSumBST(5, 7, 15): 5<7 → skip left
    rangeSumBST(7, 7, 15): 7≥7 → sum += 7
      rangeSumBST(None): 0
      rangeSumBST(None): 0
      return 7
    return 7
  rangeSumBST(15, 7, 15): 15≤15 → sum += 15
    rangeSumBST(None): 0
    rangeSumBST(18, 7, 15): 18>15 → skip right
      rangeSumBST(None): 0
      return 0
    return 15
  return 10 + 7 + 15 = 32 ✅
```

**Well-Commented Code:**
```python
def rangeSumBST(root, low, high):
    # Base case: empty node
    if not root:
        return 0

    # Node value is below range — left subtree is even smaller
    if root.val < low:
        return rangeSumBST(root.right, low, high)

    # Node value is above range — right subtree is even larger
    if root.val > high:
        return rangeSumBST(root.left, low, high)

    # Node is within range: add its value and check both subtrees
    return (root.val +
            rangeSumBST(root.left, low, high) +
            rangeSumBST(root.right, low, high))
```

**Complexity Analysis:**
- **Time:** O(n) worst case (all nodes in range), O(h) best case (range is narrow)
- **Space:** O(h) — recursion stack

**Edge Cases with Examples:**
| Input | Range | Output | Reason |
|-------|-------|--------|--------|
| `[]` | any | 0 | Empty tree |
| `[1]` | [1,1] | 1 | Single node in range |
| `[5,3,7]` | [6,10] | 7 | Only 7 is in range |
| All nodes out of range | any | 0 | Quick exit via BST property |

**Common Mistakes:**
- ❌ Visiting all nodes even when BST property allows pruning — resulting in O(n) unnecessarily
- ❌ Using `<=` or `>=` incorrectly for range boundaries
- ❌ Forgetting that if node.val < low, we should NOT recurse left at all
- ❌ Not understanding that the BST property guarantees all left values < node < right values

**Pattern Recognition Hints:**
- **Pruning/Bounding:** Skip subtrees that can't possibly contain valid values — key BST optimization
- **Range Query:** Processing nodes within a range is a fundamental BST operation
- **Conditional Recursion:** Choose which subtree(s) to explore based on current node's value

---

## Problem 6: Minimum Absolute Difference in BST

**Statement:** Given a BST, return the minimum absolute difference between values of any two different nodes.

**Problem Explanation in Simple Words:**
Find the two nodes in the BST that are closest in value (smallest difference). Since inorder traversal of a BST gives sorted order, the minimum difference will always be between two adjacent values in the sorted list. Like finding the smallest gap between consecutive numbers in a sorted array.

**Example:**
```
BST:
    4
   / \
  2   6
 / \
1   3

Inorder: [1, 2, 3, 4, 6]
Differences: |2-1|=1, |3-2|=1, |4-3|=1, |6-4|=2
Minimum = 1 ✅
```

**Detailed Approach with Algorithm Steps:**
1. **Initialize:** min_diff = infinity, prev = None.
2. **Inorder Traversal:**
   - Traverse left subtree.
   - If prev is not None: compute node.val - prev (positive since inorder is sorted).
   - Update min_diff with the smaller value.
   - Set prev = node.val.
   - Traverse right subtree.
3. **Return:** min_diff.

**Visual Tree Diagram:**
```
Inorder traversal tracking differences:

    4 ← first visited? No, go left first
   / \
  2   6
 / \
1   3

Traversal order:
  visit 1: prev=None, just set prev=1
  visit 2: diff=|2-1|=1, min_diff=1, prev=2
  visit 3: diff=|3-2|=1, min_diff=1, prev=3
  visit 4: diff=|4-3|=1, min_diff=1, prev=4
  visit 6: diff=|6-4|=2, min_diff stays 1

Return 1 ✅
```

**Step-by-Step Trace with Input `[4,2,6,1,3]`:**
```
Initialize: min_diff=∞, prev=None

inorder(4):
  inorder(2):
    inorder(1):
      inorder(None): return
      prev=None → skip diff check, prev=1
      inorder(None): return
    prev=1 → diff=2-1=1, min_diff=1, prev=2
    inorder(3):
      inorder(None): return
      prev=2 → diff=3-2=1, min_diff=1, prev=3
      inorder(None): return
  prev=3 → diff=4-3=1, min_diff=1, prev=4
  inorder(6):
    inorder(None): return
    prev=4 → diff=6-4=2, min_diff stays 1, prev=6
    inorder(None): return

Return 1 ✅
```

**Well-Commented Code:**
```python
def getMinimumDifference(root):
    min_diff = float('inf')  # Initialize to largest possible
    prev = None              # Previous node value in inorder

    def inorder(node):
        nonlocal min_diff, prev
        if not node:
            return

        inorder(node.left)

        # Compute difference with previous (adjacent in sorted order)
        if prev is not None:
            min_diff = min(min_diff, node.val - prev)
        prev = node.val

        inorder(node.right)

    inorder(root)
    return min_diff
```

**Complexity Analysis:**
- **Time:** O(n) — single inorder traversal
- **Space:** O(h) — recursion stack

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[1]` | ∞ | Only one node — no pair to compare |
| `[2,1,3]` | 1 | |2-1|=1, |3-2|=1 |
| `[5,3,8]` | 2 | |5-3|=2, |8-5|=3 |
| Large BST | smallest gap | Always between adjacent inorder values |

**Common Mistakes:**
- ❌ Computing absolute differences between all pairs (O(n²)) instead of just adjacent nodes
- ❌ Not initializing prev correctly (should be None, not 0)
- ❌ Forgetting to check prev is None before computing difference
- ❌ Using nonlocal incorrectly — Python requires it for modifying closure variables

**Pattern Recognition Hints:**
- **Inorder = Sorted:** The key insight is that inorder traversal of BST is sorted
- **Adjacent Differences:** Minimum difference is always between adjacent elements
- **Single Pass:** Track previous element during traversal for O(n) time, O(1) extra space

---

## Problem 7: Check if Tree is Symmetric

**Statement:** Given a binary tree, check whether it is a mirror of itself (symmetric around its center).

**Problem Explanation in Simple Words:**
The tree should look the same when reflected across its center. For each node, the left subtree should be a mirror image of the right subtree. Imagine folding the tree in half vertically — the two halves should match.

**Example:**
```
Symmetric:                     Not symmetric:
    1                             1
   / \                           / \
  2   2                         2   2
 / \ / \                         \   \
3  4 4  3                         3   3

Left mirror = Right               Left mirror ≠ Right
✅                                ❌
```

**Detailed Approach with Algorithm Steps:**
1. **Base:** If root is None, return True (empty tree is symmetric).
2. **Mirror Check Helper:** Create isMirror(left, right):
   - Both None → True (both empty, symmetric here).
   - One None → False (structure differs).
   - Values differ → False.
   - Check: left.left mirrors right.right AND left.right mirrors right.left.
3. **Return:** isMirror(root.left, root.right).

**Visual Tree Diagram:**
```
Mirror relationship:
        1
       / \
     [2] [2]    ← Compare left subtree(2) with right subtree(2)
     / \   / \
   (3)(4)(4)(3) ← Compare (3↔3), (4↔4) crosswise
   ↑       ↑
   |       |
   left.left mirrors right.right
   left.right mirrors right.left
```

**Step-by-Step Trace with Input `[1,2,2,3,4,4,3]`:**
```
isSymmetric(1):
  isMirror(2, 2):
    2==2, continue
    isMirror(3, 3): 3==3 → both children None → True
    isMirror(4, 4): 4==4 → both children None → True
    True AND True = True ✅
  return True ✅
```

**Well-Commented Code:**
```python
def isSymmetric(root):
    # Empty tree is symmetric
    if not root:
        return True

    def isMirror(left, right):
        # Both nodes None — symmetric at this point
        if not left and not right:
            return True

        # One is None, other isn't — not symmetric
        if not left or not right:
            return False

        # Values must match, and subtrees must mirror each other
        return (left.val == right.val and
                isMirror(left.left, right.right) and   # Outer comparison
                isMirror(left.right, right.left))       # Inner comparison

    return isMirror(root.left, root.right)
```

**Complexity Analysis:**
- **Time:** O(n) — visit each node once
- **Space:** O(h) — recursion stack, h = height

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[]` | True | Empty tree |
| `[1]` | True | Single node |
| `[1,2,2,3,null,null,3]` | True | Mirror structure |
| `[1,2,2,null,3,null,3]` | False | Values at different positions |
| `[1,2,3]` | False | Values don't match (2≠3) |

**Common Mistakes:**
- ❌ Checking root.left == root.right (direct equality) instead of structural/value comparison
- ❌ Comparing left.left with right.left (same side) instead of left.left with right.right (opposite sides)
- ❌ Forgetting that both children could be None (valid symmetric case)
- ❌ Using iterative queue approach but not comparing the right pairs

**Pattern Recognition Hints:**
- **Mirror Comparison:** Cross-compare outer with outer, inner with inner
- **Same Tree Variant:** Compare two trees, but with opposite children
- **Iterative Alternative:** Use a queue with paired nodes, process two at a time
- **Recursive Elegance:** Very clean recursive solution with a helper that takes two nodes

---

## Problem 8: Univalued Binary Tree

**Statement:** A binary tree is univalued if every node has the same value. Given the root of a binary tree, return true if it is univalued.

**Problem Explanation in Simple Words:**
Check if ALL nodes in the tree have the same value. The root sets the expected value. As soon as you find a single node with a different value, the tree is not univalued.

**Example:**
```
Univalued:                    Not univalued:
    2                              2
   / \                            / \
  2   2                          2   3
 / \   \                        / \   \
2   2   2                      2   2   2

All values = 2 ✅               Found 3 ≠ 2 ❌
```

**Detailed Approach with Algorithm Steps:**
1. **Base:** If root is None, return True (empty tree is trivially univalued).
2. **Store Root Value:** Record root.val as the expected value.
3. **DFS:** Recursively traverse:
   - If node is None, return True.
   - If node.val != expected value, return False.
   - Return True only if BOTH left and right subtrees are also univalued.
4. **Return:** Result of DFS from root.

**Well-Commented Code:**
```python
def isUnivalTree(root):
    # Empty tree is considered univalued
    if not root:
        return True

    val = root.val  # Expected value for all nodes

    def dfs(node):
        if not node:
            return True
        # Mismatch found — not univalued
        if node.val != val:
            return False
        # Both subtrees must also match
        return dfs(node.left) and dfs(node.right)

    return dfs(root)
```

**Complexity Analysis:**
- **Time:** O(n) — visit every node in worst case
- **Space:** O(h) — recursion stack

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[]` | True | Empty tree |
| `[1]` | True | Single node |
| `[1,1,1,1,1]` | True | All same |
| `[1,1,1,null,2]` | False | 2 differs from 1 |
| Large tree all same | True | Traverse all nodes, no mismatch |

**Common Mistakes:**
- ❌ Checking if all values are equal to the root but forgetting root itself could be None
- ❌ Using root.val without checking if root exists first
- ❌ Only checking immediate children instead of all nodes
- ❌ Returning True when a mismatch is found (should return False)

**Pattern Recognition Hints:**
- **Early Termination:** Return False as soon as a mismatch is found — no need to continue
- **Value Propagation:** Expected value is determined once at root and passed down
- **Consistency Check:** Verify a property holds for ALL nodes

---

## Problem 9: Count Good Nodes in Binary Tree

**Statement:** A node is "good" if in the path from root to that node, there are no nodes with a value greater than it. Return the number of good nodes.

**Problem Explanation in Simple Words:**
A node is "good" if it's greater than or equal to ALL nodes on the path from root to itself. In other words, if you walk from root to a node and that node has the maximum value seen so far, it's good. Count all such nodes.

**Example:**
```
    3  ← good (max so far = 3)
   / \
  1  4  ← good (max so far along this path = 4)
 /   / \
3   1  5  ← good (max so far along this path = 5)

Path to leftmost 3: 3→1→3, max=3, 3≥3 → good
Path to 1: 3→1, max=3, 1<3 → NOT good
Path to 4: 3→4, max=4, 4≥4 → good
Path to 1 (right subtree): 3→4→1, max=4, 1<4 → NOT good
Path to 5: 3→4→5, max=5, 5≥5 → good

Total good: 3 (3, 4, 5)
```

**Detailed Approach with Algorithm Steps:**
1. **Initialize:** count = [0] (list for mutability in recursion).
2. **DFS:** Pass current node and max value seen on path so far.
   - If node is None, return.
   - If node.val >= max_so_far: increment count (this node is "good").
   - Update max_so_far = max(max_so_far, node.val).
   - Recurse left and right with the new max.
3. **Call:** dfs(root, float('-inf')) — start with negative infinity.
4. **Return:** count[0].

**Well-Commented Code:**
```python
def goodNodes(root):
    # Use list for mutability across recursive calls (avoids nonlocal)
    count = [0]

    def dfs(node, max_so_far):
        if not node:
            return

        # Node is "good" if it's >= all nodes on the path
        if node.val >= max_so_far:
            count[0] += 1

        # Update max for children
        new_max = max(max_so_far, node.val)
        dfs(node.left, new_max)
        dfs(node.right, new_max)

    # Start with -inf since root is always good
    dfs(root, float('-inf'))
    return count[0]
```

**Complexity Analysis:**
- **Time:** O(n) — visit every node once
- **Space:** O(h) — recursion stack

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[]` | 0 | Empty tree |
| `[1]` | 1 | Root is always good |
| `[3,1,4,3,null,1,5]` | 4 | 3, 4, 3(left), 5 are good |
| `[2,null,4,null,6]` | 3 | All nodes are good (strictly increasing) |
| All decreasing | 1 | Only root is good |

**Common Mistakes:**
- ❌ Comparing against parent only — must compare against ALL ancestors
- ❌ Not updating max_so_far before recursing to children
- ❌ Using nonlocal keyword incorrectly — list trick avoids this
- ❌ Counting nodes that are NOT the maximum on their path

**Pattern Recognition Hints:**
- **Path State Propagation:** Pass information (max) down the path from root
- **Prefix Maximum:** Classic pattern — track the maximum seen so far in a sequence
- **Context Carrying:** Recursion carries context from parent to children
- **Tree + Array Analogy:** Like counting "record-breaking" elements in an array

---

## Problem 10: Leaf-Similar Trees

**Statement:** Two binary trees are leaf-similar if their leaf sequences (left to right) are the same. Return True if two trees are leaf-similar.

**Problem Explanation in Simple Words:**
Collect the leaf values from both trees in left-to-right order. If the two sequences are identical, the trees are leaf-similar. It doesn't matter what the internal nodes look like — only the leaves matter.

**Example:**
```
Tree 1:             Tree 2:
    3                   3
   / \                 / \
  5   1               5   1
 / \                 /   /
6   2               6   2
Leaves: [6, 2, 1]   Leaves: [6, 2, 1]
Both sequences match → True ✅
```

**Detailed Approach with Algorithm Steps:**
1. **Helper Function:** get_leaves(node, leaves):
   - If node is None, return.
   - If node is a leaf (no left/right children), append its value.
   - Recurse left, then right.
2. **Collect:** Get leaves of both trees into separate lists.
3. **Compare:** Return leaves1 == leaves2.

**Well-Commented Code:**
```python
def leafSimilar(root1, root2):
    def get_leaves(node, leaves):
        """Collect leaf values in left-to-right order."""
        if not node:
            return
        # Leaf node: no children
        if not node.left and not node.right:
            leaves.append(node.val)
            return
        # Non-leaf: continue traversal (left first, then right)
        get_leaves(node.left, leaves)
        get_leaves(node.right, leaves)

    leaves1, leaves2 = [], []
    get_leaves(root1, leaves1)
    get_leaves(root2, leaves2)

    # Direct list comparison
    return leaves1 == leaves2
```

**Complexity Analysis:**
- **Time:** O(n1 + n2) — traverse both trees
- **Space:** O(n1 + n2) — storing leaf sequences (worst case O(n) if all are leaves)

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[]`, `[]` | True | Both empty, no leaves |
| `[1]`, `[1]` | True | Both have same leaf |
| `[1,2]`, `[1,null,2]` | True | Leaves: [2] and [2] |
| `[1,2,3]`, `[1,2,3]` | False? | Leaves: [2,3] vs [2,3] → actually True |
| `[1]`, `[2]` | False | Different leaf values |

**Common Mistakes:**
- ❌ Comparing the entire tree structures instead of just leaf sequences
- ❌ Collecting leaves in wrong order (right before left)
- ❌ Forgetting to handle the case where a leaf is also the root
- ❌ Using string concatenation for leaf sequence instead of list (works but less clean)

**Pattern Recognition Hints:**
- **Leaf Collection:** Only nodes with no children are of interest
- **Sequence Comparison:** Two independent traversals compared at the end
- **DFS Order:** Left-to-right traversal ensures consistent ordering
- **Optimization:** Could use generators/yield to avoid storing all leaves in memory

---

## Problem 11: Maximum Depth of N-ary Tree

**Statement:** Given an N-ary tree, find its maximum depth. The depth is the number of nodes along the longest path from the root to the farthest leaf.

**Problem Explanation in Simple Words:**
Same as binary tree max depth, but each node can have any number of children (not just 2). Find the longest path from root to a leaf by checking all children and taking the maximum depth among them.

**Example:**
```
N-ary Tree:
        1
      / | \
     2  3  4
    /      / \
   5      6   7
  /
 8

Longest path: 1→2→5→8 (4 nodes)
Max depth = 4
```

**Detailed Approach with Algorithm Steps:**
1. **Base Case:** If root is None, return 0.
2. **No Children:** If root has no children, return 1 (just the node itself).
3. **Recurse:** Return 1 + max depth among all children.
4. **Return:** Computed max depth.

**Visual Tree Diagram:**
```
        1
      / | \
     2  3  4
    /      / \
   5      6   7
  /
 8

Depth calculation:
  leaf(8): depth=1
  node(5): depth=1+max(depth(8))=2
  node(2): depth=1+max(depth(5))=3
  leaf(3): depth=1
  leaf(6): depth=1
  leaf(7): depth=1
  node(4): depth=1+max(depth(6),depth(7))=2
  root(1): depth=1+max(depth(2),depth(3),depth(4))=1+max(3,1,2)=4 ✅
```

**Well-Commented Code:**
```python
def maxDepth(root):
    if not root:
        return 0
    # Leaf node (no children)
    if not root.children:
        return 1
    # Find max depth among all children
    return 1 + max(maxDepth(child) for child in root.children)
```

**Complexity Analysis:**
- **Time:** O(n) — visit every node
- **Space:** O(d) — recursion depth = maximum depth of tree

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[]` | 0 | Empty tree |
| `[1]` | 1 | Single node with no children |
| Star-shaped (root + n children) | 2 | Root + one level of children |
| Linear chain (each node has one child) | n | Degenerate N-ary tree |

**Common Mistakes:**
- ❌ Forgetting the case where children list is empty (leaf node)
- ❌ Using binary tree logic (left/right) instead of iterating over children
- ❌ Not handling None nodes in the children list
- ❌ Confusing depth (node count) with height (edge count)

**Pattern Recognition Hints:**
- **N-ary Generalization:** Same pattern as binary tree, but iterate over children
- **Recursive Depth:** 1 + max(depth of children) is the universal pattern
- **Tree Agnostic:** The recursive depth algorithm works for any tree structure

---

## Problem 12: N-ary Tree Level Order Traversal

**Statement:** Given an N-ary tree, return the level order traversal of its nodes' values (left to right, level by level).

**Problem Explanation in Simple Words:**
Traverse the tree level by level from top to bottom. Within each level, process nodes from left to right. Same as binary tree level order, but each node has a list of children instead of just left/right.

**Example:**
```
N-ary Tree:
        1
      / | \
     3  2  4
    / \
   5   6

Output: [[1], [3,2,4], [5,6]]

Level 0: [1]
Level 1: [3, 2, 4]
Level 2: [5, 6]
```

**Detailed Approach with Algorithm Steps:**
1. **Initialize:** If root is None, return []. Create queue with root.
2. **BFS:** While queue is not empty:
   - Record current level size.
   - Create level list.
   - For each node at this level: pop, add val to level, enqueue all children.
   - Append level to result.
3. **Return result.**

**Well-Commented Code:**
```python
from collections import deque

def levelOrder(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level = []
        # Process all nodes at the current level
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            # Enqueue all children for the next level
            for child in node.children:
                queue.append(child)
        result.append(level)

    return result
```

**Complexity Analysis:**
- **Time:** O(n) — visit each node once
- **Space:** O(n) — queue can hold up to the widest level

**Edge Cases with Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `[]` | `[]` | Empty tree |
| `[1]` | `[[1]]` | Single node |
| Root with many children | `[[1], [c1,c2,...,cn]]` | Two levels only |

**Common Mistakes:**
- ❌ Using recursion (DFS) instead of BFS — doesn't naturally group by level
- ❌ Not iterating over all children of N-ary nodes (only checking left/right)
- ❌ Forgetting to check for None children in the children list
- ❌ Not recording `len(queue)` before processing — level size changes as children are added

**Pattern Recognition Hints:**
- **BFS Template:** For any tree structure, level order uses queue + level_size pattern
- **N-ary vs Binary:** Only difference is iterating over children list vs checking left/right
- **Level Tracking:** The inner `for _ in range(len(queue))` loop is the standard technique

---

---

# MEDIUM PROBLEMS (13-30)

---

## Problem 13: Binary Tree Level Order Traversal II

**Statement:** Given a binary tree, return the bottom-up level order traversal (first the deepest level, then the level above, up to the root).

**Approach:** Perform standard BFS level order traversal. After collecting all levels in top-down order, reverse the result list to get bottom-up order.

```python
from collections import deque

def levelOrderBottom(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result[::-1]
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(n) - storing all levels

---

## Problem 14: Binary Tree Tilt

**Statement:** The tilt of a node is the absolute difference between the sum of all left subtree values and right subtree values. The tilt of the whole tree is the sum of all node tilts.

**Approach:** Post-order DFS. For each node, compute its subtree sum (left_sum + right_sum + node.val). The tilt contribution is abs(left_sum - right_sum). Accumulate total tilt globally. Return the subtree sum for parent computation.

```python
def findTilt(root):
    total_tilt = [0]

    def subtree_sum(node):
        if not node:
            return 0
        left = subtree_sum(node.left)
        right = subtree_sum(node.right)
        total_tilt[0] += abs(left - right)
        return left + right + node.val

    subtree_sum(root)
    return total_tilt[0]
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 15: Find Bottom Left Tree Value

**Statement:** Given a binary tree, find the leftmost value in the last row of the tree.

**Approach:** BFS level order traversal. The first node visited at each level is the leftmost. Track the first node's value at each level; by the end, the answer is the first node of the last level.

```python
from collections import deque

def findBottomLeftValue(root):
    queue = deque([root])
    result = root.val
    while queue:
        for i in range(len(queue)):
            node = queue.popleft()
            if i == 0:
                result = node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return result
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(w) - max width of tree

---

## Problem 16: Largest Value in Each Tree Row

**Statement:** Given a binary tree, return a list of the largest value in each row (level).

**Approach:** BFS level order traversal. For each level, track the maximum value. Append that maximum to the result after processing all nodes in the level.

```python
from collections import deque

def largestValues(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_max = float('-inf')
        for _ in range(len(queue)):
            node = queue.popleft()
            level_max = max(level_max, node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level_max)
    return result
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(w) - max width of tree

---

## Problem 17: Closest Value in BST

**Statement:** Given a BST and a target value, find the value in the BST that is closest to the target.

**Approach:** Start from root. At each node, update the closest value if the current node is closer. If target < node.val, go left; if target > node.val, go right; if equal, return immediately.

```python
def closestValue(root, target):
    closest = root.val
    while root:
        if abs(root.val - target) < abs(closest - target):
            closest = root.val
        if target < root.val:
            root = root.left
        elif target > root.val:
            root = root.right
        else:
            return root.val
    return closest
```

**Time Complexity:** O(h) - height of BST, worst O(n)
**Space Complexity:** O(1) - iterative approach

---

## Problem 18: Inorder Successor in BST

**Statement:** Given a BST node p, find the in-order successor (the node with the smallest key greater than p.val). Return None if it does not exist.

**Approach:** Starting from root, track potential successor. If node.val > p.val, it could be the successor -- record it and go left. If node.val <= p.val, go right. By the end, the last recorded value is the successor.

```python
def inorderSuccessor(root, p):
    successor = None
    while root:
        if root.val > p.val:
            successor = root
            root = root.left
        else:
            root = root.right
    return successor
```

**Time Complexity:** O(h) - height of BST
**Space Complexity:** O(1) - iterative

---

## Problem 19: Delete Node in BST

**Statement:** Given a BST root and a key, delete the node with the given key and return the root of the updated BST.

**Approach:** Find the node to delete. Three cases: (1) No left child -- replace with right subtree. (2) No right child -- replace with left subtree. (3) Both children exist -- find the inorder successor (smallest in right subtree), copy its value, then delete that successor from the right subtree.

```python
def deleteNode(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = deleteNode(root.left, key)
    elif key > root.val:
        root.right = deleteNode(root.right, key)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        successor = root.right
        while successor.left:
            successor = successor.left
        root.val = successor.val
        root.right = deleteNode(root.right, successor.val)
    return root
```

**Time Complexity:** O(h) - find and delete in BST
**Space Complexity:** O(h) - recursion stack

---

## Problem 20: Construct BST from Preorder Traversal

**Statement:** Given an array of unique values representing the preorder traversal of a BST, construct the tree and return its root.

**Approach:** Use a recursive helper with bounds. The first element is the root. All values less than root go to the left subtree, rest to the right. Use an index pointer that advances as nodes are consumed.

```python
def bstFromPreorder(preorder):
    idx = [0]

    def build(lower, upper):
        if idx[0] >= len(preorder):
            return None
        val = preorder[idx[0]]
        if val < lower or val > upper:
            return None
        node = TreeNode(val)
        idx[0] += 1
        node.left = build(lower, val)
        node.right = build(val, upper)
        return node

    return build(float('-inf'), float('inf'))
```

**Time Complexity:** O(n) - each node visited once
**Space Complexity:** O(h) - recursion stack

---

## Problem 21: Convert BST to Greater Tree

**Statement:** Given a BST, transform it into a Greater Tree where every node's value is replaced by the original value plus the sum of all values greater than it in the BST.

**Approach:** Reverse inorder traversal (right -> node -> left). Maintain a running sum. At each node, update its value to be the running sum, then update the running sum to include the current node's original value.

```python
def convertBST(root):
    running_sum = [0]

    def reverse_inorder(node):
        if not node:
            return
        reverse_inorder(node.right)
        running_sum[0] += node.val
        node.val = running_sum[0]
        reverse_inorder(node.left)

    reverse_inorder(root)
    return root
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 22: Diameter of N-ary Tree

**Statement:** Given an N-ary tree, find the diameter -- the longest path between any two nodes (measured in edges).

**Approach:** For each node, find the two longest paths going down through different children. Diameter = max(diameter, longest + second_longest). Return the max diameter seen.

```python
def diameter(root):
    max_diam = [0]

    def height(node):
        if not node:
            return 0
        first, second = 0, 0
        for child in node.children:
            h = height(child)
            if h > first:
                second = first
                first = h
            elif h > second:
                second = h
        max_diam[0] = max(max_diam[0], first + second)
        return 1 + first

    height(root)
    return max_diam[0]
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 23: Step-By-Step Directions from One Node to Another

**Statement:** Given a binary tree with two node values (start and dest), return a string of directions ('L', 'R', 'U') to go from start to destination. Minimize the length.

**Approach:** Find the lowest common ancestor (LCA) of the two nodes. From LCA to destination: record path using 'L'/'R'. From LCA to start: record path using 'L'/'R', then reverse and convert to 'U'. Concatenate the 'U' path with the destination path.

```python
def getDirections(root, startValue, destValue):
    def find_path(node, target, path):
        if not node:
            return False
        if node.val == target:
            return True
        path.append('L')
        if find_path(node.left, target, path):
            return True
        path.pop()
        path.append('R')
        if find_path(node.right, target, path):
            return True
        path.pop()
        return False

    def lca(node, v1, v2):
        if not node or node.val == v1 or node.val == v2:
            return node
        left = lca(node.left, v1, v2)
        right = lca(node.right, v1, v2)
        if left and right:
            return node
        return left if left else right

    ancestor = lca(root, startValue, destValue)
    path_to_start = []
    find_path(ancestor, startValue, path_to_start)
    path_to_dest = []
    find_path(ancestor, destValue, path_to_dest)
    return 'U' * len(path_to_start) + ''.join(path_to_dest)
```

**Time Complexity:** O(n) - finding LCA and paths
**Space Complexity:** O(h) - recursion stack

---

## Problem 24: Binary Tree Right Side View

**Statement:** Given a binary tree, return the values of nodes you can see from the right side (last node at each level).

**Approach:** BFS level order traversal. For each level, the last node processed is the rightmost. Record the last node at each level.

```python
from collections import deque

def rightSideView(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:
                result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return result
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(w) - max width of tree

---

## Problem 25: Even Odd Tree

**Statement:** A binary tree is Even-Odd if: at every even-indexed level (0, 2, 4, ...), all values are odd and strictly increasing; at every odd-indexed level (1, 3, 5, ...), all values are even and strictly decreasing.

**Approach:** BFS level order. Track the level. For each level, check parity constraints and order constraints. If any violation is found, return False.

```python
from collections import deque

def isEvenOddTree(root):
    queue = deque([root])
    level = 0
    while queue:
        prev = None
        for _ in range(len(queue)):
            node = queue.popleft()
            if level % 2 == 0:
                if node.val % 2 == 0:
                    return False
                if prev is not None and node.val <= prev:
                    return False
            else:
                if node.val % 2 == 1:
                    return False
                if prev is not None and node.val >= prev:
                    return False
            prev = node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        level += 1
    return True
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(w) - max width of tree

---

## Problem 26: Maximum Level Sum of Binary Tree

**Statement:** Given a binary tree, return the level (1-indexed) with the maximum sum of node values. If there is a tie, return the smallest level number.

**Approach:** BFS level order traversal. Sum values at each level. Track the maximum sum and the level at which it occurs. Return the level number (1-indexed).

```python
from collections import deque

def maxLevelSum(root):
    max_sum = float('-inf')
    result_level = 0
    level = 1
    queue = deque([root])
    while queue:
        level_sum = 0
        for _ in range(len(queue)):
            node = queue.popleft()
            level_sum += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        if level_sum > max_sum:
            max_sum = level_sum
            result_level = level
        level += 1
    return result_level
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(w) - max width of tree

---

## Problem 27: Deepest Leaves Sum

**Statement:** Given a binary tree, return the sum of the values of its deepest leaves (the leaves at the deepest level).

**Approach:** BFS level order traversal. The last level processed contains the deepest leaves. Sum all values at that level.

```python
from collections import deque

def deepestLeavesSum(root):
    queue = deque([root])
    while queue:
        level_sum = 0
        for _ in range(len(queue)):
            node = queue.popleft()
            level_sum += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return level_sum
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(w) - max width of tree

---

## Problem 28: Check Completeness of a Binary Tree

**Statement:** Given a binary tree, check if it is a complete binary tree. A complete tree has all levels fully filled except possibly the last, which is filled left to right.

**Approach:** BFS traversal. Once a null node is encountered, no more non-null nodes should appear after it. Use a flag to track if we have seen a null. If a non-null node appears after a null, the tree is not complete.

```python
from collections import deque

def isCompleteTree(root):
    if not root:
        return True
    queue = deque([root])
    seen_null = False
    while queue:
        node = queue.popleft()
        if not node:
            seen_null = True
        else:
            if seen_null:
                return False
            queue.append(node.left)
            queue.append(node.right)
    return True
```

**Time Complexity:** O(n) - visit every node
**Space Complexity:** O(w) - max width of tree

---

## Problem 29: Trim a Binary Search Tree

**Statement:** Given a BST root and two values low and high, trim the tree so all values fall within [low, high]. The relative structure of remaining nodes should be preserved.

**Approach:** Recursive: if node.val < low, the entire left subtree is out of range -- return trimmed right subtree. If node.val > high, return trimmed left subtree. Otherwise, recurse on both children and return the node.

```python
def trimBST(root, low, high):
    if not root:
        return None
    if root.val < low:
        return trimBST(root.right, low, high)
    if root.val > high:
        return trimBST(root.left, low, high)
    root.left = trimBST(root.left, low, high)
    root.right = trimBST(root.right, low, high)
    return root
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 30: Flatten Binary Tree to Linked List

**Statement:** Given a binary tree, flatten it to a linked list in-place. The "linked list" should use the right child pointers, and the left child pointers should be null. The order should be pre-order traversal.

**Approach:** Recursive approach: recursively flatten left and right subtrees. Save the right subtree, attach the flattened left subtree to the current node's right, then find the tail of the flattened left subtree and attach the saved right subtree to it.

```python
def flatten(root):
    def helper(node):
        if not node:
            return None
        left_tail = helper(node.left)
        right_tail = helper(node.right)
        if left_tail:
            left_tail.right = node.right
            node.right = node.left
            node.left = None
        return right_tail if right_tail else (left_tail if left_tail else node)

    helper(root)
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

---

# HARD PROBLEMS (31-40)

---

## Problem 31: Binary Tree Cameras

**Statement:** You are given the root of a binary tree. We install cameras on tree nodes. Each camera at a node can monitor its parent, itself, and its immediate children. Return the minimum number of cameras needed to monitor all nodes.

**Approach:** Post-order DFS with states: 0 = not covered, 1 = has camera, 2 = covered (no camera). If a child is not covered, place a camera at current node (state 1, count++). If a child has a camera, current node is covered (state 2). If both children are covered and no camera needed, return state 0 (not covered) so parent places camera. After DFS, if root state is 0, add one more camera.

```python
def minCameraCover(root):
    count = [0]

    def dfs(node):
        if not node:
            return 2  # null nodes are considered covered
        left = dfs(node.left)
        right = dfs(node.right)
        if left == 0 or right == 0:
            # child not covered -> place camera here
            count[0] += 1
            return 1  # has camera
        if left == 1 or right == 1:
            # child has camera -> this node is covered
            return 2
        # both children covered, no camera needed
        return 0

    if dfs(root) == 0:
        count[0] += 1
    return count[0]
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 32: Find Duplicate Subtrees

**Statement:** Given a binary tree, find all duplicate subtrees. Return the root nodes of each duplicate subtree. Two trees are duplicates if they have the same structure and node values.

**Approach:** Serialize each subtree as a string. Use a dictionary to count occurrences. When a serialization appears for the second time, add the node to the result.

```python
def findDuplicateSubtrees(root):
    from collections import defaultdict
    serial_count = defaultdict(int)
    result = []

    def serialize(node):
        if not node:
            return "#"
        serial = f"{node.val},{serialize(node.left)},{serialize(node.right)}"
        serial_count[serial] += 1
        if serial_count[serial] == 2:
            result.append(node)
        return serial

    serialize(root)
    return result
```

**Time Complexity:** O(n^2) in worst case due to string operations; O(n) average
**Space Complexity:** O(n) - storing serializations

---

## Problem 33: Serialize and Deserialize N-ary Tree

**Statement:** Design an algorithm to serialize and deserialize an N-ary tree to/from a string.

**Approach:** Serialize: DFS preorder. For each node, write its value followed by the count of children, then recurse on each child. Deserialize: Read value, read child count, recursively deserialize children, return the node.

```python
class Codec:
    def serialize(self, root):
        if not root:
            return ""
        result = []

        def dfs(node):
            result.append(str(node.val))
            result.append(str(len(node.children)))
            for child in node.children:
                dfs(child)

        dfs(root)
        return ','.join(result)

    def deserialize(self, data):
        if not data:
            return None
        tokens = data.split(',')
        idx = [0]

        def dfs():
            val = int(tokens[idx[0]])
            idx[0] += 1
            num_children = int(tokens[idx[0]])
            idx[0] += 1
            node = Node(val)
            for _ in range(num_children):
                node.children.append(dfs())
            return node

        return dfs()
```

**Time Complexity:** O(n) - serialize and deserialize each visit node once
**Space Complexity:** O(n) - storing the serialized string and recursion stack

---

## Problem 34: Critical Connections in a Network

**Statement:** There are n servers connected by undirected edges. A critical connection is an edge that, if removed, makes some servers unreachable from others. Find all critical connections (Tarjan's bridge-finding algorithm).

**Approach:** Use DFS with discovery time and low values. For each edge (u, v), if low[v] > disc[u], then the edge is a bridge (critical connection). The low value of a node is the minimum discovery time reachable from its subtree.

```python
def criticalConnections(n, connections):
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)

    disc = [-1] * n
    low = [-1] * n
    timer = [0]
    result = []

    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        for v in graph[u]:
            if v == parent:
                continue
            if disc[v] == -1:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    result.append([u, v])
            else:
                low[u] = min(low[u], disc[v])

    dfs(0, -1)
    return result
```

**Time Complexity:** O(V + E) - DFS traversal
**Space Complexity:** O(V + E) - graph storage and recursion stack

---

## Problem 35: Binary Search Tree Iterator II

**Statement:** Implement a BST iterator that supports: hasNext(), next(), hasPrev(), and prev(). The iterator works like a sorted array traversal but uses the BST structure.

**Approach:** Use a stack to simulate inorder traversal. hasNext/next work as standard BST iterator (push left nodes). prev() needs a secondary stack to track previously visited nodes.

```python
class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self.back_stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def hasNext(self):
        return bool(self.stack or self.back_stack)

    def next(self):
        if self.back_stack:
            node = self.back_stack.pop()
        else:
            node = self.stack.pop()
            if node.right:
                self._push_left(node.right)
        return node.val

    def hasPrev(self):
        return bool(self.back_stack)

    def prev(self):
        if self.back_stack:
            node = self.back_stack.pop()
        else:
            node = self.stack.pop()
            if node.left:
                self._push_left(node.left)
        return node.val
```

**Time Complexity:** O(h) per next/prev operation
**Space Complexity:** O(n) - for stacks holding nodes

---

## Problem 36: Maximum Binary Tree II

**Statement:** A maximum binary tree is built from an array: pick the max, left subtree from left subarray, right subtree from right subarray. Given the root of a max binary tree and an integer val, insert val into the tree and return the root.

**Approach:** Traverse down the rightmost path. Find the first node where val > node.val. The current node becomes the left child of a new node with val. The new node becomes the right child of the parent. If no such node exists, val becomes the new root.

```python
def insertIntoMaxTree(root, val):
    parent = None
    node = root
    while node:
        if val > node.val:
            parent = node
            node = node.right
        else:
            node = node.right

    new_node = TreeNode(val)
    if not parent:
        new_node.left = root
        return new_node

    new_node.left = parent.right
    parent.right = new_node
    return root
```

**Time Complexity:** O(h) - traverse rightmost path
**Space Complexity:** O(1) - iterative

---

## Problem 37: Vertical Order Traversal II

**Statement:** Given a binary tree, return the vertical order traversal of its nodes' values. For each column, nodes should be sorted by row (top to bottom), and within the same row, by value (left to right).

**Approach:** BFS with (node, row, col) tuples. Store (row, val) for each column in a dictionary. After BFS, sort each column by row, then by value for same row. Build result by iterating columns from left to right.

```python
from collections import defaultdict, deque

def verticalTraversal(root):
    if not root:
        return []
    col_map = defaultdict(list)
    queue = deque([(root, 0, 0)])

    while queue:
        for _ in range(len(queue)):
            node, row, col = queue.popleft()
            col_map[col].append((row, node.val))
            if node.left:
                queue.append((node.left, row + 1, col - 1))
            if node.right:
                queue.append((node.right, row + 1, col + 1))

    result = []
    for col in sorted(col_map.keys()):
        col_map[col].sort()
        result.append([val for _, val in col_map[col]])
    return result
```

**Time Complexity:** O(n log n) - sorting within each column
**Space Complexity:** O(n) - storing all nodes in the dictionary

---

## Problem 38: Longest Univalue Path

**Statement:** Given a binary tree, find the length of the longest path where each node in the path has the same value. The path length is measured in edges.

**Approach:** Post-order DFS. For each node, recursively get the longest univalue path from left and right children. If the child's value matches the current node's value, extend that path. Update the global maximum with left + right (path through current node). Return the longer of the two single-side paths for parent use.

```python
def longestUnivaluePath(root):
    max_path = [0]

    def dfs(node):
        if not node:
            return 0
        left_len = dfs(node.left)
        right_len = dfs(node.right)
        left_arrow = left_len + 1 if node.left and node.left.val == node.val else 0
        right_arrow = right_len + 1 if node.right and node.right.val == node.val else 0
        max_path[0] = max(max_path[0], left_arrow + right_arrow)
        return max(left_arrow, right_arrow)

    dfs(root)
    return max_path[0]
```

**Time Complexity:** O(n) - visit each node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 39: Sum of Nodes with Even Valued Grandparent

**Statement:** Given a binary tree, return the sum of values of nodes whose grandparent has an even value. If a node does not have a grandparent, it is not included.

**Approach:** DFS passing parent and grandparent values. If grandparent's value is even, add the current node's value. Recurse on children, passing current node as parent and parent as grandparent.

```python
def sumEvenGrandparent(root):
    total = [0]

    def dfs(node, parent_val, grandparent_val):
        if not node:
            return
        if grandparent_val % 2 == 0:
            total[0] += node.val
        dfs(node.left, node.val, parent_val)
        dfs(node.right, node.val, parent_val)

    dfs(root, 1, 1)  # dummy non-even values for root's non-existent parents
    return total[0]
```

**Time Complexity:** O(n) - visit every node once
**Space Complexity:** O(h) - recursion stack

---

## Problem 40: All Elements in Two Binary Search Trees

**Statement:** Given two BSTs root1 and root2, return a list containing all integers from both trees sorted in ascending order.

**Approach:** Inorder traverse both BSTs to get two sorted lists. Merge the two sorted lists into one sorted list using two-pointer technique.

```python
def getAllElements(root1, root2):
    def inorder(node, result):
        if not node:
            return
        inorder(node.left, result)
        result.append(node.val)
        inorder(node.right, result)

    list1, list2 = [], []
    inorder(root1, list1)
    inorder(root2, list2)

    merged = []
    i, j = 0, 0
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1
    while i < len(list1):
        merged.append(list1[i])
        i += 1
    while j < len(list2):
        merged.append(list2[j])
        j += 1
    return merged
```

**Time Complexity:** O(n1 + n2) - traverse both trees and merge
**Space Complexity:** O(n1 + n2) - storing the two sorted lists

---

# Summary Table

| #  | Problem                                    | Difficulty | Time       | Space |
|----|--------------------------------------------|------------|------------|-------|
| 1  | Sum of Left Leaves                         | Easy       | O(n)       | O(h)  |
| 2  | Two Sum IV - BST                           | Easy       | O(n)       | O(n)  |
| 3  | Find Mode in BST                           | Easy       | O(n)       | O(h)  |
| 4  | Increasing BST                             | Easy       | O(n)       | O(h)  |
| 5  | Range Sum of BST                           | Easy       | O(n)       | O(h)  |
| 6  | Minimum Absolute Difference in BST         | Easy       | O(n)       | O(h)  |
| 7  | Check if Tree is Symmetric                 | Easy       | O(n)       | O(h)  |
| 8  | Univalued Binary Tree                      | Easy       | O(n)       | O(h)  |
| 9  | Count Good Nodes                           | Easy       | O(n)       | O(h)  |
| 10 | Leaf-Similar Trees                         | Easy       | O(n1+n2)   | O(n)  |
| 11 | Maximum Depth of N-ary Tree                | Easy       | O(n)       | O(h)  |
| 12 | N-ary Tree Level Order Traversal           | Easy       | O(n)       | O(n)  |
| 13 | Level Order Traversal II (Bottom-Up)       | Medium     | O(n)       | O(n)  |
| 14 | Binary Tree Tilt                           | Medium     | O(n)       | O(h)  |
| 15 | Find Bottom Left Tree Value                | Medium     | O(n)       | O(w)  |
| 16 | Largest Value in Each Tree Row             | Medium     | O(n)       | O(w)  |
| 17 | Closest Value in BST                       | Medium     | O(h)       | O(1)  |
| 18 | Inorder Successor in BST                   | Medium     | O(h)       | O(1)  |
| 19 | Delete Node in BST                         | Medium     | O(h)       | O(h)  |
| 20 | Construct BST from Preorder                | Medium     | O(n)       | O(h)  |
| 21 | Convert BST to Greater Tree                | Medium     | O(n)       | O(h)  |
| 22 | Diameter of N-ary Tree                     | Medium     | O(n)       | O(h)  |
| 23 | Step-By-Step Directions                    | Medium     | O(n)       | O(h)  |
| 24 | Binary Tree Right Side View                | Medium     | O(n)       | O(w)  |
| 25 | Even Odd Tree                              | Medium     | O(n)       | O(w)  |
| 26 | Maximum Level Sum                          | Medium     | O(n)       | O(w)  |
| 27 | Deepest Leaves Sum                         | Medium     | O(n)       | O(w)  |
| 28 | Check Completeness of Binary Tree          | Medium     | O(n)       | O(w)  |
| 29 | Trim a Binary Search Tree                  | Medium     | O(n)       | O(h)  |
| 30 | Flatten Binary Tree to Linked List         | Medium     | O(n)       | O(h)  |
| 31 | Binary Tree Cameras                        | Hard       | O(n)       | O(h)  |
| 32 | Find Duplicate Subtrees                    | Hard       | O(n^2)     | O(n)  |
| 33 | Serialize/Deserialize N-ary Tree           | Hard       | O(n)       | O(n)  |
| 34 | Critical Connections (Tarjan's)            | Hard       | O(V+E)     | O(V)  |
| 35 | Binary Search Tree Iterator II             | Hard       | O(h)       | O(n)  |
| 36 | Maximum Binary Tree II                     | Hard       | O(h)       | O(1)  |
| 37 | Vertical Order Traversal II                | Hard       | O(n log n) | O(n)  |
| 38 | Longest Univalue Path                      | Hard       | O(n)       | O(h)  |
| 39 | Sum of Nodes with Even Grandparent         | Hard       | O(n)       | O(h)  |
| 40 | All Elements in Two BSTs                   | Hard       | O(n1+n2)   | O(n)  |

---

> **Total: 40 problems | 12 Easy + 18 Medium + 10 Hard**
> **Pair with `tree_problems_batch1.md` for complete tree mastery!**

---

# Quick Reference: Key Tree Patterns

## Pattern 1: Recursive DFS (Most Common)

Used in: Problems 1, 2, 5, 7, 8, 9, 10, 11, 14, 21, 22, 29, 30, 31, 32, 38, 39

```python
def dfs(node):
    if not node:
        return base_case
    left = dfs(node.left)
    right = dfs(node.right)
    # process current node
    return result
```

**When to use:** When you need to process children before parent (post-order), or when you need information from subtrees.

---

## Pattern 2: BFS Level Order (Very Common)

Used in: Problems 12, 13, 15, 16, 24, 25, 26, 27, 28, 37

```python
from collections import deque

def bfs(root):
    queue = deque([root])
    while queue:
        for _ in range(len(queue)):
            node = queue.popleft()
            # process node
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
```

**When to use:** When you need level-by-level processing, finding level properties, or level order traversal.

---

## Pattern 3: BST Property Exploitation

Used in: Problems 3, 4, 5, 6, 17, 18, 19, 20, 21, 29, 35

```python
def bst_operation(root, target):
    if not root:
        return None
    if target < root.val:
        return bst_operation(root.left, target)
    elif target > root.val:
        return bst_operation(root.right, target)
    else:
        # found target
```

**When to use:** When the problem specifically involves a BST and you can leverage the ordering property to prune the search space.

---

## Pattern 4: Inorder Traversal (BST -> Sorted)

Used in: Problems 3, 4, 6, 21, 35, 40

```python
def inorder(node):
    if not node:
        return
    inorder(node.left)
    # process node (nodes are in sorted order for BST)
    inorder(node.right)
```

**When to use:** When you need sorted order from a BST, or when comparing adjacent elements in sorted order.

---

## Pattern 5: Serialization / Hashing

Used in: Problems 32, 33

```python
def serialize(node):
    if not node:
        return "#"
    return f"{node.val},{serialize(node.left)},{serialize(node.right)}"
```

**When to use:** When you need to compare subtrees, or when you need to flatten a tree into a string representation.

---

## Pattern 6: Post-order with State

Used in: Problems 14, 21, 22, 31, 38

```python
def postorder(node):
    if not node:
        return state  # null state
    left_state = postorder(node.left)
    right_state = postorder(node.right)
    # compute current state from children
    return current_state
```

**When to use:** When the decision at a node depends on information from its children (e.g., cameras, diameter, path problems).

---

## Pattern 7: Two-Pointer Merge

Used in: Problem 40

```python
def merge_sorted(l1, l2):
    result = []
    i, j = 0, 0
    while i < len(l1) and j < len(l2):
        if l1[i] <= l2[j]:
            result.append(l1[i])
            i += 1
        else:
            result.append(l2[j])
            j += 1
    result.extend(l1[i:])
    result.extend(l2[j:])
    return result
```

**When to use:** When you need to combine two sorted sequences from separate tree traversals.

---

# Edge Cases Checklist for Tree Problems

| Edge Case                        | How to Handle                                    |
|----------------------------------|--------------------------------------------------|
| Empty tree (root = None)         | Return 0, None, False, or [] as appropriate      |
| Single node                     | Handle as both root and leaf                      |
| Skewed tree (all left/right)    | Height = n, width = 1                            |
| Complete binary tree            | Width at level i = 2^i                           |
| All nodes same value            | Check for univalued tree problems                |
| Negative values                 | Use float('-inf') or float('inf') carefully      |
| BST with duplicates             | Account for duplicates in comparisons             |
| Very deep tree                  | Watch for recursion depth (use iterative)        |
| Very wide tree                  | Watch for queue size in BFS                      |

---

# Complexity Quick Reference

| Operation                        | Time     | Space    |
|----------------------------------|----------|----------|
| DFS (any order)                  | O(n)     | O(h)     |
| BFS (level order)                | O(n)     | O(w)     |
| BST Search/Insert/Delete         | O(h)     | O(h)     |
| Inorder Traversal                | O(n)     | O(h)     |
| Serialize/Deserialize            | O(n)     | O(n)     |
| Find LCA                         | O(n)     | O(h)     |
| Diameter of Tree                 | O(n)     | O(h)     |
| Level Order Traversal            | O(n)     | O(n)     |

Where: n = number of nodes, h = height of tree, w = maximum width of tree

For balanced BST: h = log(n)
For skewed BST: h = n
For complete binary tree: w = n/2

---

# Tips for Infosys SP DSE Tree Problems

1. **Always start with the base case** -- what happens when the node is None?

2. **Choose the right traversal:**
   - Pre-order: when you need to process parent before children
   - In-order: when you need sorted order from BST
   - Post-order: when you need children's info before parent
   - Level-order: when you need level-by-level processing

3. **BST problems can often be solved in O(h) time** by exploiting the ordering property.

4. **For "find all" problems**, use a hash map / dictionary for counting or grouping.

5. **For path problems**, consider both DFS (path from root) and finding LCA.

6. **For optimization problems on trees**, think about:
   - What information do I need from my children?
   - What information do I need to pass to my parent?
   - Can I maintain a global/running answer?

7. **Iterative vs Recursive:**
   - Recursive is simpler and preferred for interviews
   - Use iterative if recursion depth is a concern (very deep trees)
   - For iterative DFS, use an explicit stack
   - For iterative BFS, use a deque

8. **Common mistakes to avoid:**
   - Forgetting to handle the empty tree case
   - Modifying the tree while traversing without saving references
   - Off-by-one errors in level tracking
   - Not resetting state between recursive calls
   - Using global variables incorrectly in recursion

---

# Interview Simulation Questions

These are the kinds of follow-up questions interviewers might ask:

**After Problem 31 (Binary Tree Cameras):**
- Can you do it iteratively?
- What if a camera can monitor nodes 2 hops away instead of 1?

**After Problem 34 (Critical Connections):**
- Can you explain why Tarjan's algorithm works?
- How would you find articulation points (nodes whose removal disconnects the graph)?

**After Problem 19 (Delete Node in BST):**
- What if we need to delete multiple nodes?
- How would you handle duplicate values in the BST?

**After Problem 30 (Flatten to Linked List):**
- Can you do it without recursion (iterative)?
- Can you do it using O(1) extra space (Morris traversal)?

**After Problem 32 (Duplicate Subtrees):**
- How would you optimize the serialization to avoid O(n) string operations per node?
- Can you find duplicate subtrees of at least size k?
