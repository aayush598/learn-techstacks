# AVL Tree

A self-balancing BST where the heights of the two child subtrees of any node differ by at most 1.

---

## Definition & Properties

- **Balance Factor** = height(left) - height(right)
- Valid balance factors: **{-1, 0, 1}**
- If balance factor goes outside this range, a **rotation** is needed
- All operations guaranteed **O(log n)**
- Stricter balance than Red-Black Tree → faster lookups, slower inserts

---

## The Four Rotations

### Case 1: Left-Left (LL) → Right Rotation

```
    z (bf = +2)           y
   / \                   / \
  y   T4    →          x    z
 / \                  / \  / \
x   T3               T1 T2 T3 T4
/ \
T1  T2
```

```java
private TreeNode rotateRight(TreeNode z) {
    TreeNode y = z.left;
    TreeNode T3 = y.right;

    y.right = z;
    z.left = T3;

    z.height = Math.max(height(z.left), height(z.right)) + 1;
    y.height = Math.max(height(y.left), height(y.right)) + 1;

    return y; // y is new root of this subtree
}
```

### Case 2: Right-Right (RR) → Left Rotation

```
  z (bf = -2)              y
 / \                      / \
T1   y       →          z    x
    / \                 / \  / \
   T2  x              T1 T2 T3 T4
      / \
     T3  T4
```

```java
private TreeNode rotateLeft(TreeNode z) {
    TreeNode y = z.right;
    TreeNode T2 = y.left;

    y.left = z;
    z.right = T2;

    z.height = Math.max(height(z.left), height(z.right)) + 1;
    y.height = Math.max(height(y.left), height(y.right)) + 1;

    return y;
}
```

### Case 3: Left-Right (LR) → Left Rotation then Right Rotation

```
    z (bf = +2)
   / \
  y   T4
 / \
T1   x        →   LR Case: rotateLeft(y) then rotateRight(z)
    / \
   T2  T3
```

### Case 4: Right-Left (RL) → Right Rotation then Left Rotation

```
  z (bf = -2)
 / \
T1   y              →   RL Case: rotateRight(y) then rotateLeft(z)
    / \
   x   T4
  / \
 T2  T3
```

---

## Full Java Implementation

```java
public class AVLTree {

    private static class TreeNode {
        int key;
        int height;
        TreeNode left, right;

        TreeNode(int key) {
            this.key = key;
            this.height = 1; // new node is leaf
        }
    }

    private TreeNode root;

    private int height(TreeNode node) {
        return node == null ? 0 : node.height;
    }

    private int getBalance(TreeNode node) {
        return node == null ? 0 : height(node.left) - height(node.right);
    }

    private void updateHeight(TreeNode node) {
        node.height = 1 + Math.max(height(node.left), height(node.right));
    }

    // --- Rotations ---

    private TreeNode rotateRight(TreeNode z) {
        TreeNode y = z.left;
        TreeNode T3 = y.right;

        y.right = z;
        z.left = T3;

        updateHeight(z);
        updateHeight(y);
        return y;
    }

    private TreeNode rotateLeft(TreeNode z) {
        TreeNode y = z.right;
        TreeNode T2 = y.left;

        y.left = z;
        z.right = T2;

        updateHeight(z);
        updateHeight(y);
        return y;
    }

    // --- Rebalance ---

    private TreeNode rebalance(TreeNode node) {
        updateHeight(node);
        int balance = getBalance(node);

        // Left heavy
        if (balance > 1) {
            if (getBalance(node.left) < 0) {
                // Left-Right case
                node.left = rotateLeft(node.left);
            }
            // Left-Left case
            return rotateRight(node);
        }

        // Right heavy
        if (balance < -1) {
            if (getBalance(node.right) > 0) {
                // Right-Left case
                node.right = rotateRight(node.right);
            }
            // Right-Right case
            return rotateLeft(node);
        }

        return node; // balanced
    }

    // --- Insert ---

    public void insert(int key) {
        root = insert(root, key);
    }

    private TreeNode insert(TreeNode node, int key) {
        if (node == null) return new TreeNode(key);

        if (key < node.key) {
            node.left = insert(node.left, key);
        } else if (key > node.key) {
            node.right = insert(node.right, key);
        } else {
            return node; // duplicate keys not allowed
        }

        return rebalance(node);
    }

    // --- Delete ---

    public void delete(int key) {
        root = delete(root, key);
    }

    private TreeNode delete(TreeNode node, int key) {
        if (node == null) return null;

        if (key < node.key) {
            node.left = delete(node.left, key);
        } else if (key > node.key) {
            node.right = delete(node.right, key);
        } else {
            // Found node to delete
            if (node.left == null) return node.right;
            if (node.right == null) return node.left;

            // Two children: get in-order successor
            TreeNode successor = findMin(node.right);
            node.key = successor.key;
            node.right = delete(node.right, successor.key);
        }

        return rebalance(node);
    }

    private TreeNode findMin(TreeNode node) {
        while (node.left != null) node = node.left;
        return node;
    }

    // --- Search ---

    public boolean search(int key) {
        return search(root, key);
    }

    private boolean search(TreeNode node, int key) {
        if (node == null) return false;
        if (key == node.key) return true;
        if (key < node.key) return search(node.left, key);
        return search(node.right, key);
    }

    // --- In-order traversal (sorted output) ---

    public void inorder() {
        inorder(root);
        System.out.println();
    }

    private void inorder(TreeNode node) {
        if (node == null) return;
        inorder(node.left);
        System.out.print(node.key + " ");
        inorder(node.right);
    }
}
```

---

## Insert Walkthrough: Inserting 1, 2, 3

```
Insert 1:
  1 (bf=0) ✓

Insert 2:
  1 (bf=-1)
   \
    2 (bf=0) ✓

Insert 3:
  1 (bf=-2) ← unbalanced!
   \
    2 (bf=-1)
     \
      3 (bf=0)

  Node 1: balance = -2, right child (2) balance = -1
  → Right-Right case → Left rotate at 1

       2 (bf=0)
      / \
     1   3   ✓ Balanced!
```

---

## Delete Walkthrough: Delete 3 from {1, 2, 3}

```
Tree:
    2 (bf=0)
   / \
  1   3

Delete 3:
  2 (bf=1)
 / \
1   null

  Node 2: balance = 1 (within range) ✓
  
Result:
  2 (bf=1)
 /
1   ✓ Still valid AVL (balance in [-1, 1])
```

---

## Complexity Analysis

| Operation | Time    | Space (stack) |
|-----------|---------|---------------|
| Search    | O(log n)| O(log n)      |
| Insert    | O(log n)| O(log n)      |
| Delete    | O(log n)| O(log n)      |

**Why O(log n):** Height of AVL tree is at most ~1.44 × log₂(n). Each operation does at most O(1) rotations per level.

---

## AVL Tree vs Red-Black Tree

| Property | AVL Tree | Red-Black Tree |
|----------|----------|----------------|
| Balance | Strictly balanced | Approximately balanced |
| Height | ~1.44 log n | ~2 log n |
| Lookup | Faster (shorter tree) | Slightly slower |
| Insert | Slower (may need rotations) | Faster (fewer rotations) |
| Delete | Slower (may cascade) | Faster |
| Used in | Databases, read-heavy | Java TreeMap, C++ map |

---

## Interview Tips

- **Know when to rebalance:** After insert or delete, check balance factor from the modified node up to root.
- **Always update height** before checking balance factor.
- **LR/RL cases:** Always reduce to LL/RR with a rotation first, then apply the standard rotation.
- **For interviews:** Most interviewers don't ask you to implement a full AVL tree. Focus on understanding rotations and when they're needed.
- **Java TreeMap** uses Red-Black Tree, not AVL — mention this if asked about Java's built-in implementations.
