# Red-Black Tree — Overview

A self-balancing BST with less strict balancing than AVL, requiring at most 2 rotations per insert and at most 3 per delete.

---

## The Five Rules

1. **Every node is either RED or BLACK**
2. **The root is BLACK**
3. **Every leaf (NIL/null) is BLACK**
4. **If a node is RED, both its children are BLACK** (no two adjacent reds)
5. **All paths from a node to its descendant leaves have the same number of BLACK nodes** (black-height property)

**Result:** The longest path is at most **2× the shortest path**. Height ≤ 2 × log₂(n + 1).

---

## Why Java Uses Red-Black Trees

Java's `TreeMap`, `TreeSet`, and `HashMap` (when buckets get large enough, JDK 8+) use Red-Black Trees.

**Why RB over AVL?**
- RB trees need **at most 2 rotations on insert** (vs potentially O(log n) for AVL)
- RB trees need **at most 3 rotations on delete** (vs O(log n) for AVL)
- For map/set operations, inserts and deletes are common → RB's faster mutations matter
- AVL's tighter balance gives faster lookups, but the difference is small in practice

---

## Insert Cases

When inserting a new node, color it **RED** (rule 5 is automatically satisfied, only rule 4 might be violated).

**Key:** The **uncle** (parent's sibling) determines the action:

### Case 1: Uncle is RED → Recolor

```
Uncle is RED:
  - Recolor parent and uncle to BLACK
  - Recolor grandparent to RED
  - Move problem up to grandparent (may need further fixes)

      G(b)                G(r)
     / \                 / \
    P(r) U(r)   →      P(b) U(b)
   /                  /
  N(r)               N(r)
```

### Case 2: Uncle is BLACK → Rotate + Recolor

**Case 2a: Left-Left** (parent is left child, node is left child)
```
Right rotation at grandparent, then recolor:
  - Parent becomes black
  - Grandparent becomes red
```

**Case 2b: Left-Right** (parent is left child, node is right child)
```
Left rotation at parent first (reduces to Case 2a)
Then right rotation at grandparent, recolor
```

**Case 2c: Right-Right** (mirror of 2a)
```
Left rotation at grandparent, recolor
```

**Case 2d: Right-Left** (mirror of 2b)
```
Right rotation at parent first (reduces to Case 2c)
Then left rotation at grandparent, recolor
```

---

## Conceptual Insert Algorithm

```java
// Conceptual — not full implementation
void insert(int key) {
    // Step 1: Standard BST insert, color new node RED
    TreeNode newNode = bstInsert(root, key);
    newNode.color = RED;

    // Step 2: Fix violations
    fixInsert(newNode);
}

void fixInsert(TreeNode node) {
    while (node != root && node.parent.color == RED) {
        TreeNode uncle = getUncle(node);

        if (uncle != null && uncle.color == RED) {
            // Case 1: Uncle is RED → recolor
            node.parent.color = BLACK;
            uncle.color = BLACK;
            node.parent.parent.color = RED;
            node = node.parent.parent; // move up
        } else {
            // Cases 2-4: Uncle is BLACK → rotate + recolor
            // (details depend on LL, LR, RR, RL cases)
            if (isLeftChild(node.parent) && isLeftChild(node)) {
                // LL: right rotate grandparent
            } else if (isLeftChild(node.parent) && isRightChild(node)) {
                // LR: left rotate parent, then right rotate grandparent
            } else if (isRightChild(node.parent) && isRightChild(node)) {
                // RR: left rotate grandparent
            } else {
                // RL: right rotate parent, then left rotate grandparent
            }
            break; // after rotation, at most 1 fix needed
        }
    }
    root.color = BLACK; // rule 2: root is always black
}
```

---

## Delete Overview

RB tree deletion is the most complex part:

1. **Standard BST delete** (find successor, replace, etc.)
2. If deleted node was **RED** → no fix needed (rules preserved)
3. If deleted node was **BLACK** → black-height disrupted → fix needed

**Fix cases for deletion (conceptual):**
- Sibling is RED → rotate, recolor
- Sibling is BLACK, both children BLACK → recolor sibling RED, move problem up
- Sibling is BLACK, far child RED → rotate, recolor (fixes immediately)
- Sibling is BLACK, near child RED, far child BLACK → rotate sibling inward, reduces to previous case

**At most 3 rotations** needed for deletion fix.

---

## AVL vs Red-Black Tree: Side by Side

| Feature | AVL Tree | Red-Black Tree |
|---------|----------|----------------|
| Balance factor | {-1, 0, 1} strictly | Black-height equality |
| Max rotations (insert) | O(log n) | 2 |
| Max rotations (delete) | O(log n) | 3 |
| Height | ≤ 1.44 log₂(n) | ≤ 2 log₂(n+1) |
| Lookup speed | Slightly faster | Slightly slower |
| Insert/Delete speed | Slower | Faster |
| Memory per node | Height field + pointers | Color bit + pointers |
| Use case | Read-heavy, databases | General-purpose maps/sets |
| Implementation complexity | Moderate | High |

---

## Java Implementation Notes

You won't implement RB tree from scratch in interviews, but understand these aspects:

```java
// Java TreeMap uses Red-Black Tree internally
TreeMap<Integer, String> map = new TreeMap<>();
// put() → RB insert → O(log n)
// get() → RB search → O(log n)
// remove() → RB delete → O(log n)

// HashMap in JDK 8+ uses RB tree for buckets with ≥ 64 entries
// Converts linked list → RB tree when bucket is large enough
// This improves worst-case get() from O(n) to O(log n)
```

---

## When to Mention RB Tree in Interviews

1. **"What data structure does Java use for sorted maps?"** → Red-Black Tree (TreeMap)
2. **"HashMap worst case?"** → O(n) for linked list, but JDK 8+ converts to RB tree → O(log n)
3. **"Why not AVL for TreeMap?"** → RB has faster inserts/deletes (fewer rotations), which matters for map operations
4. **"When would you use AVL instead?"** → Read-heavy workloads where lookup speed is paramount

---

## Interview Tips

- **Don't implement from scratch** — focus on conceptual understanding.
- **Know the rules** — be able to list all 5 rules from memory.
- **Know the trade-off** — AVL = faster reads, RB = faster writes.
- **Connect to Java** — TreeMap, TreeSet, HashMap (JDK 8+) all use RB trees.
- **If asked to implement** — clarify: "Do you want a full implementation, or should I focus on the key operations and rebalancing logic?"
