# Tree Traversal Patterns

## Table of Contents
1. Tree Traversal Fundamentals
2. Inorder Traversal (BST Sorted Order)
3. Preorder Traversal (Serialize, Copy Tree)
4. Postorder Traversal (Compute from Children, Delete)
5. Level Order Traversal (Shortest Path, Views)
6. DFS vs BFS on Trees
7. Recursive vs Iterative Traversal
8. Morris Traversal (O(1) Space Inorder)

---

## 1. Tree Traversal Fundamentals

### Binary Tree Node
```java
public class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
```

### The Three Orders
```
       1
      / \
     2   3
    / \   \
   4   5   6

Inorder  (Left-Root-Right):   4 2 5 1 3 6
Preorder (Root-Left-Right):   1 2 4 5 3 6
Postorder(Left-Right-Root):   4 5 2 6 3 1
Levelorder:                   1 2 3 4 5 6
```

### Complexity Comparison
| Traversal | Time | Space (balanced) | Space (skewed) | Use Case |
|-----------|------|------------------|----------------|----------|
| Inorder (rec) | O(n) | O(h) | O(n) | BST sort |
| Preorder (rec) | O(n) | O(h) | O(n) | Serialize |
| Postorder (rec) | O(n) | O(h) | O(n) | Delete tree |
| Level order | O(n) | O(n) | O(n) | Shortest path |
| Morris inorder | O(n) | O(1) | O(1) | O(1) space |

---

## 2. Inorder Traversal — BST Sorted Order

**When to use:**
- BST → get elements in sorted order
- Validate BST (compare current with previous)
- Find Kth smallest/largest in BST
- Convert BST to balanced BST / sorted array
- Find inorder successor/predecessor

**Recursive:**
```java
public List<Integer> inorderTraversal(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    inorder(root, result);
    return result;
}
private void inorder(TreeNode node, List<Integer> result) {
    if (node == null) return;
    inorder(node.left, result);
    result.add(node.val);
    inorder(node.right, result);
}
```

**Iterative:**
```java
public List<Integer> inorderTraversal(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    Stack<TreeNode> stack = new Stack<>();
    TreeNode curr = root;
    while (curr != null || !stack.isEmpty()) {
        while (curr != null) {
            stack.push(curr);
            curr = curr.left;
        }
        curr = stack.pop();
        result.add(curr.val);
        curr = curr.right;
    }
    return result;
}
```

**Validate BST:**
```java
public boolean isValidBST(TreeNode root) {
    Stack<TreeNode> stack = new Stack<>();
    TreeNode curr = root, prev = null;
    while (curr != null || !stack.isEmpty()) {
        while (curr != null) {
            stack.push(curr);
            curr = curr.left;
        }
        curr = stack.pop();
        if (prev != null && prev.val >= curr.val) return false;
        prev = curr;
        curr = curr.right;
    }
    return true;
}
```

**Kth Smallest in BST:**
```java
public int kthSmallest(TreeNode root, int k) {
    Stack<TreeNode> stack = new Stack<>();
    TreeNode curr = root;
    while (curr != null || !stack.isEmpty()) {
        while (curr != null) {
            stack.push(curr);
            curr = curr.left;
        }
        curr = stack.pop();
        if (--k == 0) return curr.val;
        curr = curr.right;
    }
    return -1;
}
```

---

## 3. Preorder Traversal — Serialize, Copy Tree

**When to use:**
- Serialize/deserialize a tree (root first, easy to reconstruct)
- Copy/clone a tree
- Create a prefix expression (Polish notation)
- Print tree structure (root → children → grandchildren)

**Recursive:**
```java
public List<Integer> preorderTraversal(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    preorder(root, result);
    return result;
}
private void preorder(TreeNode node, List<Integer> result) {
    if (node == null) return;
    result.add(node.val);
    preorder(node.left, result);
    preorder(node.right, result);
}
```

**Iterative:**
```java
public List<Integer> preorderTraversal(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    if (root == null) return result;
    Stack<TreeNode> stack = new Stack<>();
    stack.push(root);
    while (!stack.isEmpty()) {
        TreeNode node = stack.pop();
        result.add(node.val);
        if (node.right != null) stack.push(node.right);
        if (node.left != null) stack.push(node.left);
    }
    return result;
}
```

**Serialize and Deserialize:**
```java
// Serialize
public String serialize(TreeNode root) {
    StringBuilder sb = new StringBuilder();
    serialize(root, sb);
    return sb.toString();
}
private void serialize(TreeNode node, StringBuilder sb) {
    if (node == null) {
        sb.append("null,");
        return;
    }
    sb.append(node.val).append(",");
    serialize(node.left, sb);
    serialize(node.right, sb);
}

// Deserialize
public TreeNode deserialize(String data) {
    Queue<String> queue = new LinkedList<>(Arrays.asList(data.split(",")));
    return deserialize(queue);
}
private TreeNode deserialize(Queue<String> queue) {
    String val = queue.poll();
    if (val.equals("null")) return null;
    TreeNode node = new TreeNode(Integer.parseInt(val));
    node.left = deserialize(queue);
    node.right = deserialize(queue);
    return node;
}
```

**Clone a tree:**
```java
public TreeNode cloneTree(TreeNode root) {
    if (root == null) return null;
    TreeNode newNode = new TreeNode(root.val);
    newNode.left = cloneTree(root.left);
    newNode.right = cloneTree(root.right);
    return newNode;
}
```

---

## 4. Postorder Traversal — Compute from Children, Delete

**When to use:**
- Compute something that requires child results first (height, diameter, balanced)
- Delete a tree (delete children before parent)
- Evaluate expression tree (postfix notation)
- Bottom-up DP on trees

**Recursive:**
```java
public List<Integer> postorderTraversal(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    postorder(root, result);
    return result;
}
private void postorder(TreeNode node, List<Integer> result) {
    if (node == null) return;
    postorder(node.left, result);
    postorder(node.right, result);
    result.add(node.val);
}
```

**Iterative (Two-Stack method):**
```java
public List<Integer> postorderTraversal(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    if (root == null) return result;
    Stack<TreeNode> stack1 = new Stack<>();
    Stack<TreeNode> stack2 = new Stack<>();
    stack1.push(root);
    while (!stack1.isEmpty()) {
        TreeNode node = stack1.pop();
        stack2.push(node);
        if (node.left != null) stack1.push(node.left);
        if (node.right != null) stack1.push(node.right);
    }
    while (!stack2.isEmpty()) {
        result.add(stack2.pop().val);
    }
    return result;
}
```

**Postorder Applications:**

**Height of tree:**
```java
public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}
```

**Balanced binary tree check:**
```java
public boolean isBalanced(TreeNode root) {
    return checkHeight(root) != -1;
}
private int checkHeight(TreeNode node) {
    if (node == null) return 0;
    int left = checkHeight(node.left);
    if (left == -1) return -1;
    int right = checkHeight(node.right);
    if (right == -1) return -1;
    if (Math.abs(left - right) > 1) return -1;
    return 1 + Math.max(left, right);
}
```

**Diameter of tree:**
```java
int diameter = 0;
public int diameterOfBinaryTree(TreeNode root) {
    height(root);
    return diameter;
}
private int height(TreeNode node) {
    if (node == null) return 0;
    int left = height(node.left);
    int right = height(node.right);
    diameter = Math.max(diameter, left + right);
    return 1 + Math.max(left, right);
}
```

---

## 5. Level Order Traversal (BFS)

**When to use:**
- Level-by-level processing
- Shortest path in unweighted tree (min depth, find closest leaf)
- All views of tree (right side, left side, top, bottom)
- Connect level order siblings
- Zigzag/spiral traversal

**Template:**
```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    while (!queue.isEmpty()) {
        int size = queue.size();
        List<Integer> level = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            level.add(node.val);
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        result.add(level);
    }
    return result;
}
```

**Right side view:**
```java
public List<Integer> rightSideView(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    while (!queue.isEmpty()) {
        int size = queue.size();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            if (i == size - 1) result.add(node.val); // last on level
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
    }
    return result;
}
```

**Min depth:**
```java
public int minDepth(TreeNode root) {
    if (root == null) return 0;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    int depth = 1;
    while (!queue.isEmpty()) {
        int size = queue.size();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            if (node.left == null && node.right == null) return depth;
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        depth++;
    }
    return depth;
}
```

---

## 6. DFS vs BFS on Trees

### When to Choose DFS

| Use Case | DFS Traversal |
|---------|--------------|
| Need to process all nodes | Any traversal |
| Need sorted order (BST) | Inorder DFS |
| Need to reconstruct tree | Preorder DFS |
| Need child results to compute parent | Postorder DFS |
| Finding path from root to leaf | Preorder with path tracking |
| Checking if tree is valid BST | Inorder DFS |
| Tree DP (max path sum, camera, robbing) | Postorder DFS |

### When to Choose BFS

| Use Case | Why BFS |
|---------|---------|
| Level-by-level processing | BFS naturally processes levels |
| Shortest path (min depth, closest) | BFS finds shortest first |
| View problems (right side, top) | BFS gives last/first on each level |
| Connect level order siblings | Process level → connect same level |
| Zigzag/spiral order | BFS with level direction toggle |
| Serialize level order | More compact, complete tree |

### Decision Framework
```
Need to traverse tree:
├── Need shortest path / min depth?
│   ├── YES → BFS (Level order)
│   └── NO → ↓
├── Need level-by-level processing?
│   ├── YES → BFS
│   └── NO → ↓
├── Need results from children to compute parent?
│   ├── YES → DFS Postorder
│   └── NO → ↓
├── Need sorted order (BST)?
│   ├── YES → DFS Inorder
│   └── NO → ↓
├── Need to reconstruct or serialize?
│   ├── YES → DFS Preorder
│   └── NO → Any DFS works
```

---

## 7. Recursive vs Iterative Traversal

### Recursive
**Pros:**
- Simple, clean, matches mathematical definition
- Natural for divide-and-conquer

**Cons:**
- O(h) call stack space (could overflow for skewed tree, h = n)
- Not suitable for production with very deep trees

### Iterative
**Pros:**
- No call stack overflow
- More control (can pause/resume)
- O(1) extra space with Morris traversal

**Cons:**
- More complex code
- Easy to make mistakes with stack management

### When to Choose Which
- **Interview:** Start with recursive (faster to write), mention iterative for deep trees
- **Production:** Iterative for safety, recursive for simple tree operations
- **Deep trees (n > 10,000):** Always iterative to avoid stack overflow

---

## 8. Morris Traversal (O(1) Space Inorder)

**Key insight:** Create temporary links from rightmost node of left subtree to current node, then traverse back.

**Inorder Morris:**
```java
public List<Integer> inorderTraversal(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    TreeNode curr = root;
    while (curr != null) {
        if (curr.left == null) {
            result.add(curr.val);
            curr = curr.right;
        } else {
            TreeNode predecessor = curr.left;
            while (predecessor.right != null && predecessor.right != curr) {
                predecessor = predecessor.right;
            }
            if (predecessor.right == null) {
                predecessor.right = curr; // create thread
                curr = curr.left;
            } else {
                predecessor.right = null; // remove thread
                result.add(curr.val);
                curr = curr.right;
            }
        }
    }
    return result;
}
```

**Preorder Morris:**
```java
public List<Integer> preorderTraversal(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    TreeNode curr = root;
    while (curr != null) {
        if (curr.left == null) {
            result.add(curr.val);
            curr = curr.right;
        } else {
            TreeNode predecessor = curr.left;
            while (predecessor.right != null && predecessor.right != curr) {
                predecessor = predecessor.right;
            }
            if (predecessor.right == null) {
                predecessor.right = curr;
                result.add(curr.val); // Visit before going left
                curr = curr.left;
            } else {
                predecessor.right = null;
                curr = curr.right;
            }
        }
    }
    return result;
}
```

---

## Quick Reference: Problem → Traversal

| Problem | Best Traversal | Why |
|---------|---------------|-----|
| Validate BST | Inorder | Checks sorted order |
| Kth smallest in BST | Inorder | Stops early at Kth element |
| Serialize tree | Preorder | Root-first reconstruction |
| Clone tree | Preorder | Create node then clone children |
| Max depth | Postorder | Need child depths |
| Balanced tree | Postorder | Need child heights |
| Diameter | Postorder | Combine child heights at each node |
| LCA | Postorder | Both children must be checked |
| Right side view | Level order | Last node on each level |
| Min depth | Level order | First leaf found = min depth |
| Zigzag order | Level order | Toggle direction per level |
| Path sum (any root-leaf) | Preorder (DFS) | Track path sum from root |
| Max path sum (any node) | Postorder | Combine left+right paths |
| Level order connect | Level order | Same level processing |
| Flatten to linked list | Preorder | Root then left then right order |
| Invert tree | Preorder (or postorder) | Swap children at each node |
| Count good nodes | Preorder | Pass maxSoFar from root |
| BST iterator | Inorder iterative | Controlled traversal |
