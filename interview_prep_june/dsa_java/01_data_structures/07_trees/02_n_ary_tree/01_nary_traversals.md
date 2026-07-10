# N-ary Tree Traversals

## The Three Core Traversals

In an N-ary tree, traversals extend naturally from binary trees. The key difference: instead of visiting left then right, we iterate through **all children** in order.

## Preorder Traversal (Root → Children)

Visit the root first, then recursively visit each child from left to right.

```
Tree:
        1
      / | \
     3  2  4
    / \
   5   6

Preorder: 1 → 3 → 5 → 6 → 2 → 4
```

```java
import java.util.*;

class NAryNode {
    int val;
    List<NAryNode> children;

    NAryNode(int val) {
        this.val = val;
        this.children = new ArrayList<>();
    }

    NAryNode(int val, List<NAryNode> children) {
        this.val = val;
        this.children = children;
    }
}

class NaryPreorder {

    // Recursive preorder
    public static List<Integer> preorderRecursive(NAryNode root) {
        List<Integer> result = new ArrayList<>();
        preorderHelper(root, result);
        return result;
    }

    private static void preorderHelper(NAryNode node, List<Integer> result) {
        if (node == null) return;

        result.add(node.val); // Process root FIRST

        for (NAryNode child : node.children) {
            preorderHelper(child, result);
        }
    }

    // Iterative preorder using stack
    // Trick: push children in REVERSE order so leftmost is processed first
    public static List<Integer> preorderIterative(NAryNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        Deque<NAryNode> stack = new ArrayDeque<>();
        stack.push(root);

        while (!stack.isEmpty()) {
            NAryNode current = stack.pop();
            result.add(current.val);

            // Push children in reverse order
            // So that the first child is on top of stack
            for (int i = current.children.size() - 1; i >= 0; i--) {
                stack.push(current.children.get(i));
            }
        }

        return result;
    }
}
```

## Postorder Traversal (Children → Root)

Visit all children first, then process the root.

```
Postorder: 5 → 6 → 3 → 2 → 4 → 1
```

```java
class NaryPostorder {

    // Recursive postorder
    public static List<Integer> postorderRecursive(NAryNode root) {
        List<Integer> result = new ArrayList<>();
        postorderHelper(root, result);
        return result;
    }

    private static void postorderHelper(NAryNode node, List<Integer> result) {
        if (node == null) return;

        for (NAryNode child : node.children) {
            postorderHelper(child, result);
        }

        result.add(node.val); // Process root LAST
    }

    // Iterative postorder using two stacks
    // Stack 1: process nodes, Stack 2: reverse the order
    public static List<Integer> postorderIterative(NAryNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        Deque<NAryNode> stack1 = new ArrayDeque<>();
        Deque<NAryNode> stack2 = new ArrayDeque<>();

        stack1.push(root);

        while (!stack1.isEmpty()) {
            NAryNode current = stack1.pop();
            stack2.push(current);

            // Push children in normal order to stack1
            // (they'll be popped in reverse, which is fine
            //  since stack2 reverses everything again)
            for (NAryNode child : current.children) {
                stack1.push(child);
            }
        }

        while (!stack2.isEmpty()) {
            result.add(stack2.pop().val);
        }

        return result;
    }
}
```

## Level Order Traversal (BFS)

Process nodes level by level using a queue.

```
Level order: [1], [3, 2, 4], [5, 6]
```

```java
class NaryLevelOrder {

    // Standard level order — returns flat list
    public static List<Integer> levelOrder(NAryNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        Queue<NAryNode> queue = new LinkedList<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            NAryNode current = queue.poll();
            result.add(current.val);

            for (NAryNode child : current.children) {
                queue.offer(child);
            }
        }

        return result;
    }

    // Level order grouped by level — returns List<List<Integer>>
    public static List<List<Integer>> levelOrderGrouped(NAryNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;

        Queue<NAryNode> queue = new LinkedList<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            int size = queue.size(); // nodes at current level
            List<Integer> currentLevel = new ArrayList<>();

            for (int i = 0; i < size; i++) {
                NAryNode current = queue.poll();
                currentLevel.add(current.val);

                for (NAryNode child : current.children) {
                    queue.offer(child);
                }
            }

            result.add(currentLevel);
        }

        return result;
    }

    // Reverse level order (bottom-up)
    public static List<List<Integer>> reverseLevelOrder(NAryNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;

        Queue<NAryNode> queue = new LinkedList<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> currentLevel = new ArrayList<>();

            for (int i = 0; i < size; i++) {
                NAryNode current = queue.poll();
                currentLevel.add(current.val);

                for (NAryNode child : current.children) {
                    queue.offer(child);
                }
            }

            result.add(0, currentLevel); // add to front
        }

        return result;
    }
}
```

## Maximum Depth of N-ary Tree

Classic LeetCode problem — elegant recursive solution:

```java
class MaxDepth {

    // Recursive approach
    public int maxDepth(NAryNode root) {
        if (root == null) return 0;
        if (root.children.isEmpty()) return 1;

        int maxChildDepth = 0;
        for (NAryNode child : root.children) {
            maxChildDepth = Math.max(maxChildDepth, maxDepth(child));
        }
        return 1 + maxChildDepth;
    }

    // BFS approach — count levels
    public int maxDepthBFS(NAryNode root) {
        if (root == null) return 0;

        Queue<NAryNode> queue = new LinkedList<>();
        queue.offer(root);
        int depth = 0;

        while (!queue.isEmpty()) {
            int size = queue.size();
            depth++;

            for (int i = 0; i < size; i++) {
                NAryNode current = queue.poll();
                for (NAryNode child : current.children) {
                    queue.offer(child);
                }
            }
        }

        return depth;
    }
}
```

## Serialize and Deserialize N-ary Tree

```java
class NAryCodec {

    // Serialization: use preorder with child count
    // Format: "val(numChildren)(children...)"
    // Example: "1(3(2)(5)(6))(4)"

    // Encodes a tree to a single string
    public String serialize(NAryNode root) {
        if (root == null) return "";

        StringBuilder sb = new StringBuilder();
        serializeHelper(root, sb);
        return sb.toString();
    }

    private void serializeHelper(NAryNode node, StringBuilder sb) {
        sb.append(node.val);
        sb.append("(");
        sb.append(node.children.size());

        for (NAryNode child : node.children) {
            sb.append("(");
            serializeHelper(child, sb);
            sb.append(")");
        }

        sb.append(")");
    }

    // Decodes your encoded data to tree
    public NAryNode deserialize(String data) {
        if (data == null || data.isEmpty()) return null;

        int[] index = {0}; // use array to pass by reference
        return deserializeHelper(data, index);
    }

    private NAryNode deserializeHelper(String data, int[] index) {
        // Parse value
        int val = 0;
        boolean negative = false;

        if (data.charAt(index[0]) == '-') {
            negative = true;
            index[0]++;
        }

        while (index[0] < data.length() &&
               Character.isDigit(data.charAt(index[0]))) {
            val = val * 10 + (data.charAt(index[0]) - '0');
            index[0]++;
        }

        NAryNode node = new NAryNode(negative ? -val : val);

        // Parse child count
        index[0]++; // skip '('
        int childCount = 0;
        while (index[0] < data.length() &&
               Character.isDigit(data.charAt(index[0]))) {
            childCount = childCount * 10 + (data.charAt(index[0]) - '0');
            index[0]++;
        }
        index[0]++; // skip ')'

        // Parse children
        for (int i = 0; i < childCount; i++) {
            index[0]++; // skip '('
            node.children.add(deserializeHelper(data, index));
            index[0]++; // skip ')'
        }

        return node;
    }
}
```

## Alternative: Level-order Serialization

```java
class NAryLevelCodec {

    // Serialize using level order with null separators
    public String serialize(NAryNode root) {
        if (root == null) return "";

        StringBuilder sb = new StringBuilder();
        Queue<NAryNode> queue = new LinkedList<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            NAryNode current = queue.poll();

            if (current == null) {
                sb.append("null,");
                continue;
            }

            sb.append(current.val).append(",");

            // Add children (including null markers for separation)
            for (NAryNode child : current.children) {
                queue.offer(child);
            }
            queue.offer(null); // separator between node groups
        }

        // Remove trailing separator
        if (sb.length() > 0) {
            sb.setLength(sb.length() - 1);
        }

        return sb.toString();
    }
}
```

## Traversal Summary

| Traversal | Order | Use Case |
|-----------|-------|----------|
| Preorder | Root → Children | Copy tree, prefix expressions, serialization |
| Postorder | Children → Root | Delete tree, calculate directory size |
| Level order | Level by level | BFS, shortest path in unweighted tree |

## Common Pitfalls

1. **Forgetting to handle null** — always check root != null at the start
2. **Stack overflow** — very deep N-ary trees may need iterative solutions
3. **Children order** — in iterative preorder, push children in reverse order
4. **Serialization format** — know which format the problem expects (LeetCode uses specific formats)

## Practice: Count Nodes with Given Degree

```java
class CountNodesWithDegree {

    // Count nodes that have exactly k children
    public int countNodes(NAryNode root, int k) {
        if (root == null) return 0;

        int count = (root.children.size() == k) ? 1 : 0;

        for (NAryNode child : root.children) {
            count += countNodes(child, k);
        }

        return count;
    }
}
```
