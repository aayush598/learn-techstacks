# Indian Startups — Meesho, Zerodha, Unacademy, Lenskart, Nykaa

> "Indian startups test practical problem-solving with medium difficulty. They focus on clean engineering, product thinking, and broad LeetCode coverage. Less emphasis on hard algorithms, more on real-world coding."

---

## 1. Company Overview

### Meesho
- **Package:** ₹12-25 LPA (freshers)
- **Focus:** E-commerce, social commerce
- **Known for:** Fast growth, practical engineering

### Zerodha
- **Package:** ₹15-30 LPA (freshers)
- **Focus:** Stock trading platform
- **Known for:** Clean code, performance-critical systems

### Unacademy
- **Package:** ₹10-22 LPA (freshers)
- **Focus:** EdTech platform
- **Known for:** Product-driven engineering

### Lenskart
- **Package:** ₹10-20 LPA (freshers)
- **Focus:** E-commerce, AR/VR features
- **Known for:** Tech innovation, product focus

### Nykaa
- **Package:** ₹10-20 LPA (freshers)
- **Focus:** E-commerce, beauty/fashion
- **Known for:** Product engineering, clean code

### Common Pattern
- **Rounds:** Online Test → Technical (2 rounds) → HR
- **Focus:** DSA (medium), System Design, Product Thinking
- **Difficulty:** Easy-Medium (broad coverage over depth)
- **Culture:** Fast-paced, product-driven, clean engineering

---

## 2. Most Asked Topics

### Topic Priority

| Priority | Topic | Frequency | Notes |
|----------|-------|-----------|-------|
| 1 | Arrays | 85% | Easy-medium, broad coverage |
| 2 | Strings | 75% | Manipulation, parsing |
| 3 | Trees | 70% | BST basics, traversals |
| 4 | DP Basics | 60% | 1D DP, simple patterns |
| 5 | HashMaps | 60% | Frequency, grouping |
| 6 | System Design | 50% | Scalable systems |
| 7 | OOP Design | 40% | Design patterns |

### Topic Frequency Graph
```
Arrays:     ████████████████████
Strings:    █████████████████
Trees:      ██████████████
DP Basics:  ████████████
HashMaps:   ████████████
Sys Design: ██████████
OOP:        ████████
```

### What Makes Startups Different
- **Medium difficulty** — They don't ask LeetCode Hards
- **Broad coverage** — They want you to know many topics
- **Product thinking** — How does this feature serve users?
- **Clean engineering** — Maintainable, readable code
- **Practical problems** — Real-world scenarios
- **Fast-paced** — Quick problem-solving expected

---

## 3. Company-Specific Focus

### Meesho
- **E-commerce problems** — Product search, recommendations
- **Graph problems** — Social connections, referral networks
- **System design** — Scalable marketplace architecture
- **DP** — Optimization for pricing, recommendations

### Zerodha
- **Performance-critical** — Low-latency trading systems
- **Concurrency** — Thread-safe order processing
- **Mathematical** — Financial calculations, statistics
- **Clean code** — Trading systems must be reliable

### Unacademy
- **Product-focused** — Learning platform features
- **Content delivery** — Video streaming, progress tracking
- **System design** — Scalable education platform
- **Moderate DSA** — Medium difficulty problems

### Lenskart
- **E-commerce** — Product catalog, search
- **AR/VR features** — Face detection, try-on
- **System design** — Scalable retail platform
- **Clean engineering** — Maintainable codebase

### Nykaa
- **E-commerce** — Product search, recommendations
- **Content management** — Reviews, ratings
- **System design** — Scalable beauty platform
- **Product thinking** — User experience focus

---

## 4. Example Problems

### Problem 1: Two Sum
**Why startups ask this:** Foundational problem; tests HashMap understanding.

```java
import java.util.*;

public class TwoSum {

    public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            
            map.put(nums[i], i);
        }
        
        return new int[]{-1, -1};
    }

    public static void main(String[] args) {
        int[] nums = {2, 7, 11, 15};
        int[] result = twoSum(nums, 9);
        System.out.println("Indices: " + result[0] + ", " + result[1]); // 0, 1
    }
}
```

**Time:** O(n) | **Space:** O(n)

---

### Problem 2: Binary Tree Level Order Traversal
**Why startups ask this:** Tree traversal is fundamental; tests BFS understanding.

```java
import java.util.*;

public class LevelOrderTraversal {

    static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    public static List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            List<Integer> currentLevel = new ArrayList<>();
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.poll();
                currentLevel.add(node.val);
                
                if (node.left != null) queue.offer(node.left);
                if (node.right != null) queue.offer(node.right);
            }
            
            result.add(currentLevel);
        }
        
        return result;
    }

    public static void main(String[] args) {
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(9);
        root.right = new TreeNode(20);
        root.right.left = new TreeNode(15);
        root.right.right = new TreeNode(7);
        
        System.out.println(levelOrder(root));
        // [[3], [9, 20], [15, 7]]
    }
}
```

**Time:** O(n) | **Space:** O(n)

---

### Problem 3: Climbing Stairs (DP Basics)
**Why startups ask this:** Simple DP; tests understanding of recursion to DP conversion.

```java
public class ClimbingStairs {

    // APPROACH: Fibonacci pattern
    // dp[i] = dp[i-1] + dp[i-2]
    
    public static int climbStairs(int n) {
        if (n <= 2) return n;
        
        int prev2 = 1;
        int prev1 = 2;
        
        for (int i = 3; i <= n; i++) {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        
        return prev1;
    }

    public static void main(String[] args) {
        System.out.println(climbStairs(2));  // 2
        System.out.println(climbStairs(3));  // 3
        System.out.println(climbStairs(10)); // 89
    }
}
```

**Time:** O(n) | **Space:** O(1)

---

### Problem 4: Maximum Subarray (Kadane's)
```java
public class MaxSubarray {

    public static int maxSubarraySum(int[] nums) {
        int maxSum = nums[0];
        int currentSum = nums[0];
        
        for (int i = 1; i < nums.length; i++) {
            currentSum = Math.max(nums[i], currentSum + nums[i]);
            maxSum = Math.max(maxSum, currentSum);
        }
        
        return maxSum;
    }

    public static void main(String[] args) {
        int[] nums = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        System.out.println(maxSubarraySum(nums)); // 6
    }
}
```

**Time:** O(n) | **Space:** O(1)

---

### Problem 5: Valid Parentheses
```java
import java.util.*;

public class ValidParentheses {

    public static boolean isValid(String s) {
        Deque<Character> stack = new LinkedList<>();
        
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '[' || c == '{') {
                stack.push(c);
            } else {
                if (stack.isEmpty()) return false;
                
                char top = stack.pop();
                if ((c == ')' && top != '(') ||
                    (c == ']' && top != '[') ||
                    (c == '}' && top != '{')) {
                    return false;
                }
            }
        }
        
        return stack.isEmpty();
    }

    public static void main(String[] args) {
        System.out.println(isValid("()"));       // true
        System.out.println(isValid("()[]{}"));   // true
        System.out.println(isValid("(]"));       // false
    }
}
```

**Time:** O(n) | **Space:** O(n)

---

## 5. Preparation Strategy

### Focus Areas (3-Week Plan)

#### Week 1: Arrays, Strings, HashMaps
- [ ] Two sum variants (10 problems)
- [ ] Sliding window (10 problems)
- [ ] String manipulation (10 problems)
- [ ] HashMap patterns (10 problems)
- [ ] Practice: 30 problems

#### Week 2: Trees and DP Basics
- [ ] BST operations (10 problems)
- [ ] Binary tree traversals (10 problems)
- [ ] 1D DP (climbing stairs, house robber) (10 problems)
- [ ] Simple knapsack (5 problems)
- [ ] Practice: 25 problems

#### Week 3: Design and Mocks
- [ ] OOP design patterns
- [ ] System design basics
- [ ] Product thinking exercises
- [ ] Mock interviews (3-5 sessions)
- [ ] Review and consolidate

### Startup-Specific Tips
1. **Medium problems are enough** — Don't waste time on LeetCode Hards
2. **Broad coverage** — Know many topics at medium level
3. **Product thinking** — How does this feature serve users?
4. **Clean code** — Readable, maintainable solutions
5. **Fast problem-solving** — They expect quick implementation
6. **Practical context** — Frame problems in e-commerce/product context
7. **System design basics** — Scalable systems for millions of users
8. **OOP design** — Design patterns in product context

### Common Follow-up Questions
- "How would this work for 10M users?"
- "Can you make this more efficient?"
- "How would you handle edge cases?"
- "What if the input is very large?"
- "How would you test this feature?"

### Resources
- LeetCode Easy-Medium problems (top 100)
- System design basics
- Product thinking articles
- Clean code principles

---

> **Remember:** Indian startups value practical, clean engineering over algorithmic complexity. They want you to solve medium problems quickly and correctly. Focus on broad coverage and product thinking.
