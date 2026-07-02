# Iterative DFS Traversals

## Why Iterative?

- Avoids **StackOverflowError** for deep trees (common in production)
- More control over the traversal process
- Space complexity is still O(h) but stack is on heap (larger limit)
- Useful when recursion is not allowed

## Iterative Inorder Traversal

Uses a stack to simulate recursion: go left as far as possible, visit, then go right.

```java
import java.util.*;

public class IterativeInorder {
    
    public static List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        Stack<TreeNode> stack = new Stack<>();
        TreeNode current = root;
        
        while (current != null || !stack.isEmpty()) {
            // Reach the leftmost node of current subtree
            while (current != null) {
                stack.push(current);
                current = current.left;
            }
            
            // Current is null at this point, pop from stack
            current = stack.pop();
            result.add(current.val);
            
            // Now visit the right subtree
            current = current.right;
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        
        System.out.println("Iterative Inorder: " + inorderTraversal(root));
        // [4, 2, 5, 1, 3]
    }
}
```

## Iterative Preorder Traversal

### Method 1: Using Stack (push right first, then left)

```java
public class IterativePreorder {
    
    public static List<Integer> preorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Stack<TreeNode> stack = new Stack<>();
        stack.push(root);
        
        while (!stack.isEmpty()) {
            TreeNode current = stack.pop();
            result.add(current.val);
            
            // Push right first so left is processed first
            if (current.right != null) {
                stack.push(current.right);
            }
            if (current.left != null) {
                stack.push(current.left);
            }
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        
        System.out.println("Iterative Preorder: " + preorderTraversal(root));
        // [1, 2, 4, 5, 3]
    }
}
```

### Method 2: Simulating Recursion Stack (less common)

```java
public static List<Integer> preorderSimulated(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    Stack<TreeNode> stack = new Stack<>();
    TreeNode current = root;
    
    while (current != null || !stack.isEmpty()) {
        while (current != null) {
            result.add(current.val);  // Visit before going left
            stack.push(current);
            current = current.left;
        }
        current = stack.pop();
        current = current.right;
    }
    
    return result;
}
```

## Iterative Postorder Traversal

### Method 1: Two Stacks

```java
public class IterativePostorder {
    
    // Two stacks approach
    public static List<Integer> postorderTwoStacks(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Stack<TreeNode> stack1 = new Stack<>();
        Stack<TreeNode> stack2 = new Stack<>();
        stack1.push(root);
        
        // stack1: root → left → right (preorder-like, but push left first)
        // stack2: reverse of postorder
        while (!stack1.isEmpty()) {
            TreeNode current = stack1.pop();
            stack2.push(current);
            
            // Push left first, then right (opposite of preorder)
            if (current.left != null) {
                stack1.push(current.left);
            }
            if (current.right != null) {
                stack1.push(current.right);
            }
        }
        
        // stack2 has nodes in postorder (root at bottom)
        while (!stack2.isEmpty()) {
            result.add(stack2.pop().val);
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        
        System.out.println("Postorder (2 stacks): " + postorderTwoStacks(root));
        // [4, 5, 2, 3, 1]
    }
}
```

### Method 2: One Stack with Visited Marker

```java
public class IterativePostorderOneStack {
    
    static class Pair {
        TreeNode node;
        boolean visited;
        
        Pair(TreeNode node, boolean visited) {
            this.node = node;
            this.visited = visited;
        }
    }
    
    public static List<Integer> postorderOneStack(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Stack<Pair> stack = new Stack<>();
        stack.push(new Pair(root, false));
        
        while (!stack.isEmpty()) {
            Pair pair = stack.pop();
            TreeNode node = pair.node;
            boolean visited = pair.visited;
            
            if (visited) {
                result.add(node.val);
            } else {
                stack.push(new Pair(node, true));
                if (node.right != null) {
                    stack.push(new Pair(node.right, false));
                }
                if (node.left != null) {
                    stack.push(new Pair(node.left, false));
                }
            }
        }
        
        return result;
    }
    
    // Alternative approach using a Set for visited tracking
    public static List<Integer> postorderWithSet(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Stack<TreeNode> stack = new Stack<>();
        Set<TreeNode> visited = new HashSet<>();
        stack.push(root);
        
        while (!stack.isEmpty()) {
            TreeNode current = stack.peek();
            
            // If leaf or children processed, visit node
            if ((current.left == null && current.right == null) ||
                visited.contains(current)) {
                result.add(stack.pop().val);
                continue;
            }
            
            // Push right then left (stack = LIFO, so left processed first)
            if (current.right != null) {
                stack.push(current.right);
            }
            if (current.left != null) {
                stack.push(current.left);
            }
            
            // Mark current as visited (children already in stack)
            visited.add(current);
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        
        System.out.println("Postorder (1 stack): " + postorderOneStack(root));
        System.out.println("Postorder (set):     " + postorderWithSet(root));
    }
}
```

## Complete Iterative Traversal Utility

```java
public class IterativeTraversalUtils {
    
    public static List<Integer> inorder(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        Stack<TreeNode> stack = new Stack<>();
        TreeNode current = root;
        
        while (current != null || !stack.isEmpty()) {
            while (current != null) {
                stack.push(current);
                current = current.left;
            }
            current = stack.pop();
            result.add(current.val);
            current = current.right;
        }
        return result;
    }
    
    public static List<Integer> preorder(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Stack<TreeNode> stack = new Stack<>();
        stack.push(root);
        
        while (!stack.isEmpty()) {
            TreeNode current = stack.pop();
            result.add(current.val);
            if (current.right != null) stack.push(current.right);
            if (current.left != null) stack.push(current.left);
        }
        return result;
    }
    
    public static List<Integer> postorder(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Stack<TreeNode> stack1 = new Stack<>();
        Stack<TreeNode> stack2 = new Stack<>();
        stack1.push(root);
        
        while (!stack1.isEmpty()) {
            TreeNode current = stack1.pop();
            stack2.push(current);
            if (current.left != null) stack1.push(current.left);
            if (current.right != null) stack1.push(current.right);
        }
        
        while (!stack2.isEmpty()) {
            result.add(stack2.pop().val);
        }
        return result;
    }
    
    public static void printAllIterative(TreeNode root) {
        System.out.println("Inorder (iterative):   " + inorder(root));
        System.out.println("Preorder (iterative):  " + preorder(root));
        System.out.println("Postorder (iterative): " + postorder(root));
    }
}
```

## Comparison: Recursive vs Iterative

| Aspect | Recursive | Iterative (Stack) |
|--------|-----------|-------------------|
| Code clarity | Very clean, mirrors definition | More verbose |
| Stack space | Call stack (limited, ~8KB per frame) | Heap (virtually unlimited) |
| Overflow risk | High for deep trees | Low |
| Postorder | Trivial (3 lines) | Complex (2 stacks) |
| Performance | Function call overhead | Faster (no function calls) |
| Debugging | Harder (implicit stack) | Easier (explicit state) |

### Stack Depth Limits

- Java default stack size: ~1MB (varies by JVM/config)
- Each recursive call: ~8-16 bytes plus frame overhead
- Typical limit: **~10,000 to 30,000 calls** before StackOverflowError
- For a skewed tree with 100K nodes, recursion will **always fail**
- Use `-Xss` flag to increase stack size, but iterative is safer

## Practical Insights

1. **Inorder iterative** is the most common interview question among the three.

2. **Postorder with 2 stacks** is easier to remember and explain than the 1-stack approach.

3. The **pattern** for iterative traversal:
   - Inorder: go left all the way, process, go right
   - Preorder: stack (push right first), process on push
   - Postorder: 2 stacks or visited marker

4. For **competitive programming**, recursive is usually fine (n is small). For **production**, prefer iterative or Morris.

5. **Key difference from recursion**: Iterative manages the stack explicitly, giving you control over what gets pushed and when.
