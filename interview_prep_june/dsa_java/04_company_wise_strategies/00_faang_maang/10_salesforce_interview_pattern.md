# Salesforce Interview Pattern

## Table of Contents
1. Interview Format
2. Most Asked Topics
3. Salesforce Culture
4. Types of Problems
5. Example Problems
6. Preparation Strategy

---

## 1. Interview Format

### Recruiter Screen (30 min)
- Background review and role discussion
- Focus on product-oriented engineering
- Discussion of past projects and impact

### Technical Phone Screen (45-60 min)
- 1-2 coding problems (Medium difficulty)
- Often includes OOP design discussion
- May ask about databases and SQL
- Focus on clean, correct code

### On-site (4-5 rounds, 45-60 min each)
- **Coding / Algorithms** (2): DSA problems, medium difficulty
- **System Design** (1): Multi-tenant system design
- **OOP Design** (1): Design patterns, SOLID principles
- **Hiring Manager / Behavioral** (1): Team fit, product thinking

### Key Differences from Other FAANG
- **Moderate difficulty** — They don't ask LeetCode Hards
- **Product-focused** — Think about user impact
- **OOP design** is heavily weighted
- **Multi-tenancy** concepts sometimes appear
- **Clean code** matters more than clever solutions
- **SQL knowledge** is a plus for backend roles

---

## 2. Most Asked Topics

### Priority Matrix

| Priority | Topic | Frequency | Notes |
|----------|-------|-----------|-------|
| 1 | Arrays | 80% | Medium difficulty, sliding window |
| 2 | Strings | 75% | Manipulation, parsing |
| 3 | Trees | 70% | BST, binary tree basics |
| 4 | HashMaps | 70% | Frequency, grouping |
| 5 | OOP Design | 65% | Design patterns, SOLID |
| 6 | SQL / Databases | 50% | Queries, normalization |
| 7 | DP Basics | 40% | 1D DP, simple patterns |

### Topic Frequency Graph
```
Arrays:     ██████████████████
Strings:    █████████████████
Trees:      ██████████████
HashMaps:   ██████████████
OOP:        █████████████
SQL:        ██████████
DP:         ████████
```

### What Makes Salesforce Different
- **Moderate difficulty** — They value correctness over optimization
- **OOP design** is more important than at most companies
- **Product thinking** — How does your code affect users?
- **Multi-tenancy** — Understanding shared infrastructure
- **Clean code** — Salesforce has massive codebases; readability matters

---

## 3. Salesforce Culture

### Core Values

| Value | Meaning | Interview Impact |
|-------|---------|-----------------|
| **Trust** | Customer trust is paramount | Reliable, secure code |
| **Customer Success** | Help customers succeed | User-centric thinking |
| **Innovation** | Continuous improvement | Creative solutions |
| **Equality** | Inclusive environment | Respectful communication |
| **Sustainability** | Long-term thinking | Maintainable code |

### What Salesforce Looks For
1. Clean, maintainable code
2. OOP design principles
3. Product-oriented thinking
4. Database knowledge (SQL basics)
5. Understanding of multi-tenant architecture

### Behavioral Questions
- "Tell me about a time you built a feature that users loved"
- "How do you approach writing maintainable code?"
- "Describe a time you had to design a system for multiple customers"
- "How do you handle technical debt?"

---

## 4. Types of Problems

### Array/String Problems
- Two sum and variants
- Sliding window problems
- String manipulation
- Anagram detection
- Subarray problems

### Tree Problems
- BST validation and search
- Level-order traversal
- Lowest Common Ancestor
- Tree height and diameter
- Path sum problems

### HashMap Problems
- Frequency counting
- Group anagrams
- Two sum variants
- Subarray sum equals k

### OOP Design
- Design a CRM module
- Design a reporting system
- Design a notification service
- Design a multi-tenant data model

### Database Problems
- SQL query optimization
- Database normalization
- Index design
- Multi-tenant data isolation

---

## 5. Example Problems

### Problem 1: Two Sum
**Problem:** Find two numbers that add up to a target.

**Approach:** HashMap — store seen numbers, check complement for each new number.

```java
import java.util.*;

public class TwoSum {

    // APPROACH: One-pass HashMap
    // For each number, check if complement exists in map
    // If yes, return both indices
    // If no, add current number to map
    
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

    // VARIANT: Return all pairs (not just first)
    public static List<int[]> twoSumAllPairs(int[] nums, int target) {
        List<int[]> result = new ArrayList<>();
        Map<Integer, List<Integer>> map = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            
            if (map.containsKey(complement)) {
                for (int j : map.get(complement)) {
                    result.add(new int[]{j, i});
                }
            }
            
            map.computeIfAbsent(nums[i], k -> new ArrayList<>()).add(i);
        }
        
        return result;
    }

    public static void main(String[] args) {
        int[] nums = {2, 7, 11, 15};
        int[] result = twoSum(nums, 9);
        System.out.println("Indices: " + result[0] + ", " + result[1]); // 0, 1
        
        int[] nums2 = {3, 3, 3, 3};
        List<int[]> allPairs = twoSumAllPairs(nums2, 6);
        System.out.println("All pairs: " + allPairs.size()); // 3 pairs
    }
}
```

**Time:** O(n) | **Space:** O(n)

---

### Problem 2: Binary Tree Level Order Traversal
**Problem:** Return level-order traversal of a binary tree.

**Approach:** BFS using a queue — process all nodes at current level before moving to next.

```java
import java.util.*;

public class LevelOrderTraversal {

    static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    // APPROACH: BFS with queue
    // Process all nodes at current level
    // Add children to queue for next level
    
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

    // VARIANT: Zigzag level order
    public static List<List<Integer>> zigzagLevelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        boolean leftToRight = true;
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            LinkedList<Integer> currentLevel = new LinkedList<>();
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.poll();
                
                if (leftToRight) {
                    currentLevel.addLast(node.val);
                } else {
                    currentLevel.addFirst(node.val);
                }
                
                if (node.left != null) queue.offer(node.left);
                if (node.right != null) queue.offer(node.right);
            }
            
            result.add(currentLevel);
            leftToRight = !leftToRight;
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
        
        System.out.println(zigzagLevelOrder(root));
        // [[3], [20, 9], [15, 7]]
    }
}
```

**Time:** O(n) | **Space:** O(n)

---

### Problem 3: Valid Parentheses
**Problem:** Determine if input string has valid parentheses.

**Approach:** Stack — push opening brackets, pop and match when closing bracket found.

```java
import java.util.*;

public class ValidParentheses {

    // APPROACH: Stack
    // Push opening brackets onto stack
    // When closing bracket found, check if top of stack matches
    // Valid if stack is empty at the end
    
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
        System.out.println(isValid("([)]"));     // false
        System.out.println(isValid("{[]}"));     // true
    }
}
```

**Time:** O(n) | **Space:** O(n)

---

### Problem 4: Product of Array Except Self
**Problem:** Return array where each element is product of all other elements.

**Approach:** Two passes — left products and right products.

```java
import java.util.Arrays;

public class ProductExceptSelf {

    // APPROACH: Two passes
    // Pass 1: leftProducts[i] = product of all elements to the left of i
    // Pass 2: rightProducts[i] = product of all elements to the right of i
    // result[i] = leftProducts[i] * rightProducts[i]
    
    public static int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        
        // Left pass: result[i] = product of all elements to the left
        result[0] = 1;
        for (int i = 1; i < n; i++) {
            result[i] = result[i - 1] * nums[i - 1];
        }
        
        // Right pass: multiply by product of all elements to the right
        int rightProduct = 1;
        for (int i = n - 1; i >= 0; i--) {
            result[i] *= rightProduct;
            rightProduct *= nums[i];
        }
        
        return result;
    }

    public static void main(String[] args) {
        int[] nums1 = {1, 2, 3, 4};
        System.out.println(Arrays.toString(productExceptSelf(nums1)));
        // [24, 12, 8, 6]
        
        int[] nums2 = {-1, 1, 0, -3, 3};
        System.out.println(Arrays.toString(productExceptSelf(nums2)));
        // [0, 0, 9, 0, 0]
    }
}
```

**Time:** O(n) | **Space:** O(1) (excluding output)

---

### Problem 5: Climbing Stairs
**Problem:** How many distinct ways can you climb to the top (1 or 2 steps at a time)?

**Approach:** DP — dp[i] = dp[i-1] + dp[i-2] (Fibonacci pattern).

```java
public class ClimbingStairs {

    // APPROACH: 1D DP (Fibonacci pattern)
    // dp[i] = number of ways to reach step i
    // dp[i] = dp[i-1] (came from 1 step below) + dp[i-2] (came from 2 steps below)
    
    public static int climbStairs(int n) {
        if (n <= 2) return n;
        
        int prev2 = 1; // dp[i-2]
        int prev1 = 2; // dp[i-1]
        
        for (int i = 3; i <= n; i++) {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        
        return prev1;
    }

    // VARIANT: With different step sizes (1, 2, 3)
    public static int climbStairsVariants(int n) {
        if (n == 0) return 1;
        if (n == 1) return 1;
        if (n == 2) return 2;
        
        int[] dp = new int[n + 1];
        dp[0] = 1;
        dp[1] = 1;
        dp[2] = 2;
        
        for (int i = 3; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3];
        }
        
        return dp[n];
    }

    public static void main(String[] args) {
        System.out.println(climbStairs(2));  // 2
        System.out.println(climbStairs(3));  // 3
        System.out.println(climbStairs(10)); // 89
        
        System.out.println(climbStairsVariants(3)); // 4
        System.out.println(climbStairsVariants(4)); // 7
    }
}
```

**Time:** O(n) | **Space:** O(1) for optimized, O(n) for variant

---

## 6. Preparation Strategy

### Focus Areas (4-Week Plan)

#### Week 1: Arrays and Strings
- [ ] Two sum variants (10 problems)
- [ ] Sliding window (10 problems)
- [ ] String manipulation (10 problems)
- [ ] Prefix sums (5 problems)
- [ ] Practice: 25 problems

#### Week 2: Trees and HashMaps
- [ ] BST operations (10 problems)
- [ ] Binary tree traversals (10 problems)
- [ ] HashMap patterns (10 problems)
- [ ] LCA and path problems (5 problems)
- [ ] Practice: 25 problems

#### Week 3: OOP Design and SQL
- [ ] Design patterns (Singleton, Factory, Observer)
- [ ] SOLID principles
- [ ] SQL basics (SELECT, JOIN, GROUP BY)
- [ ] Multi-tenancy concepts
- [ ] Practice: 10 problems + design exercises

#### Week 4: DP Basics and Mocks
- [ ] 1D DP patterns (10 problems)
- [ ] Knapsack basics (5 problems)
- [ ] Mock interviews (3-5 sessions)
- [ ] Review weak areas

### Salesforce-Specific Tips
1. **Focus on correctness** — They value correct code over clever solutions
2. **OOP design is key** — Practice design patterns and SOLID principles
3. **Clean code matters** — Readability and maintainability
4. **Know SQL basics** — Especially JOINs and GROUP BY
5. **Multi-tenancy** — Understand shared infrastructure concepts
6. **Medium problems are enough** — Don't waste time on LeetCode Hards
7. **Product thinking** — How does your code affect users?
8. **Practice OOP design** — Design a CRM module, reporting system

### Common Follow-up Questions
- "How would you make this code more maintainable?"
- "What design pattern would you use here?"
- "How would this work in a multi-tenant system?"
- "How would you handle concurrent access?"
- "What if the input is very large?"

### Resources
- LeetCode Medium problems (arrays, strings, trees)
- "Head First Design Patterns" for OOP
- SQL basics tutorial
- Multi-tenancy architecture articles

---

> **Remember:** Salesforce values clean, maintainable code and product thinking. They don't ask the hardest algorithm problems, but they expect you to write production-quality code with good OOP design.
