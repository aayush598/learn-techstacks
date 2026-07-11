# Oracle India Interview

> "Oracle India tests moderate-hard DSA problems with emphasis on trees, strings, and SQL. Known for structured multi-round interviews and strong CS fundamentals requirements."

---

## 1. Company Overview

- **Package:** ₹10-25 LPA (freshers), higher for experienced
- **Hiring:** Campus + Off-campus + Referrals
- **Rounds:** Online Test → Technical (2-3 rounds) → HR
- **Focus:** DSA, SQL, CS Fundamentals, OOP
- **Key Differentiator:** **SQL questions** alongside DSA for backend roles

---

## 2. Interview Process

### Online Test (HackerRank)
- 3-4 coding problems (Easy to Medium-Hard)
- Time limit: 90-120 minutes
- Topics: Arrays, Strings, Trees, SQL
- Sometimes includes multiple-choice CS fundamentals

### Technical Rounds (2-3 rounds, 45-60 min each)

| Round | Focus | Difficulty |
|-------|-------|------------|
| Round 1 | DSA Coding (Trees/Strings) | Medium |
| Round 2 | DSA Coding (DP/Arrays) | Medium-Hard |
| Round 3 | SQL + CS Fundamentals | Medium |

### HR Round (30 min)
- Basic behavioral questions
- Salary and location discussion

### What Makes Oracle Different
- **SQL questions** are common for backend roles
- **CS fundamentals** — OS, DBMS, networking
- **Structured process** — Well-defined rounds
- **Moderate difficulty** — Not as hard as FAANG, but solid
- **Enterprise mindset** — They value production-ready code

---

## 3. Most Asked Topics

### Topic Priority

| Priority | Topic | Frequency | Example Problems |
|----------|-------|-----------|-----------------|
| 1 | Arrays | 85% | Subarray problems, sorting |
| 2 | Strings | 80% | Palindrome, substring, matching |
| 3 | Trees | 75% | BST, LCA, traversals |
| 4 | DP | 65% | Medium DP, knapsack |
| 5 | SQL | 60% | JOINs, GROUP BY, subqueries |
| 6 | HashMaps | 55% | Frequency, two sum |
| 7 | CS Fundamentals | 50% | OS, DBMS basics |

### Topic Frequency Graph
```
Arrays:     ████████████████████
Strings:    ██████████████████
Trees:      █████████████████
DP:         █████████████
SQL:        ████████████
HashMaps:   ███████████
CS Fund:    ██████████
```

---

## 4. Common Problems (Top 20)

### Arrays
1. Two Sum
3. Maximum Subarray (Kadane's)
4. Merge Intervals
5. Product of Array Except Self

### Strings
6. Valid Palindrome
7. Longest Substring Without Repeating Characters
8. Group Anagrams
9. Longest Common Subsequence

### Trees
10. Validate BST
11. Lowest Common Ancestor
12. Binary Tree Level Order Traversal
13. Maximum Depth of Binary Tree
14. Inorder Successor in BST

### DP
15. Climbing Stairs
16. Coin Change
17. Longest Increasing Subsequence
18. Edit Distance

### SQL
19. Second Highest Salary
20. Department Top Three Salaries

---

## 5. Example Problems with Approaches

### Problem 1: Valid Palindrome
**Why Oracle asks this:** String manipulation is fundamental; tests attention to detail.

```java
public class ValidPalindrome {

    // APPROACH: Two pointers from both ends
    // Skip non-alphanumeric characters
    // Compare characters (case-insensitive)
    
    public static boolean isPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        
        while (left < right) {
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) {
                left++;
            }
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) {
                right--;
            }
            
            if (Character.toLowerCase(s.charAt(left)) != 
                Character.toLowerCase(s.charAt(right))) {
                return false;
            }
            
            left++;
            right--;
        }
        
        return true;
    }

    public static void main(String[] args) {
        System.out.println(isPalindrome("A man, a plan, a canal: Panama")); // true
        System.out.println(isPalindrome("race a car")); // false
        System.out.println(isPalindrome(" ")); // true
    }
}
```

**Time:** O(n) | **Space:** O(1)

---

### Problem 2: Binary Tree Level Order Traversal
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

### Problem 3: Inorder Successor in BST
**Why Oracle asks this:** BST operations are common; tests tree traversal understanding.

```java
public class InorderSuccessor {

    static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    // APPROACH: If node has right child → leftmost in right subtree
    // If no right child → go up until we find ancestor where we're in left subtree
    
    public static TreeNode inorderSuccessor(TreeNode root, TreeNode p) {
        TreeNode successor = null;
        
        while (root != null) {
            if (p.val < root.val) {
                successor = root;
                root = root.left;
            } else {
                root = root.right;
            }
        }
        
        return successor;
    }

    public static void main(String[] args) {
        TreeNode root = new TreeNode(2);
        root.left = new TreeNode(1);
        root.right = new TreeNode(3);
        
        TreeNode successor = inorderSuccessor(root, root.left);
        System.out.println(successor.val); // 2
    }
}
```

**Time:** O(h) | **Space:** O(1)

---

### Problem 4: Coin Change
```java
import java.util.Arrays;

public class CoinChange {
    public static int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        
        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (coin <= i) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
        }
        
        return dp[amount] > amount ? -1 : dp[amount];
    }
    
    public static void main(String[] args) {
        int[] coins = {1, 5, 10, 25};
        System.out.println(coinChange(coins, 30)); // 2
    }
}
```

---

### Problem 5: SQL - Second Highest Salary
**Why Oracle asks this:** SQL knowledge is essential for database-focused roles.

```sql
-- APPROACH 1: Subquery
SELECT MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);

-- APPROACH 2: LIMIT/OFFSET
SELECT DISTINCT salary AS SecondHighestSalary
FROM Employee
ORDER BY salary DESC
LIMIT 1 OFFSET 1;

-- APPROACH 3: Using DENSE_RANK
SELECT salary AS SecondHighestSalary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rank
    FROM Employee
) ranked
WHERE rank = 2;

-- HARDER: Find Nth highest salary
SELECT salary AS NthHighestSalary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rank
    FROM Employee
) ranked
WHERE rank = N;
```

---

## 6. Preparation Strategy

### Focus Areas (4-Week Plan)

#### Week 1: Arrays and Strings
- [ ] Two sum variants (10 problems)
- [ ] Kadane's algorithm (5 problems)
- [ ] String manipulation (10 problems)
- [ ] Palindrome problems (5 problems)
- [ ] Practice: 20 problems

#### Week 2: Trees and HashMaps
- [ ] BST operations (10 problems)
- [ ] Binary tree traversals (10 problems)
- [ ] LCA and path problems (5 problems)
- [ ] HashMap patterns (5 problems)
- [ ] Practice: 20 problems

#### Week 3: DP and SQL
- [ ] 1D DP (10 problems)
- [ ] 2D DP (5 problems)
- [ ] SQL basics (5 queries)
- [ ] SQL JOINs and GROUP BY (5 queries)
- [ ] Practice: 15 problems + 10 SQL queries

#### Week 4: CS Fundamentals and Mocks
- [ ] OS basics (processes, threads, memory)
- [ ] DBMS basics (normalization, ACID, transactions)
- [ ] Networking basics (TCP/IP, HTTP)
- [ ] Mock interviews (3-5 sessions)
- [ ] Review and consolidate

### Oracle-Specific Tips
1. **SQL knowledge** — Practice JOINs, GROUP BY, subqueries
2. **CS fundamentals** — OS, DBMS, networking basics
3. **Moderate difficulty** — Focus on easy-medium problems
4. **Clean code** — Enterprise-grade readability
5. **BST problems** — Common in Oracle interviews
6. **String manipulation** — Practice parsing and transformation
7. **Edge cases** — Empty inputs, null values
8. **Communication** — Explain your approach clearly

### Common Follow-up Questions
- "Can you write the SQL query for this?"
- "What's the time complexity?"
- "How would this work with large datasets?"
- "Can you optimize for memory?"
- "What if the input is null?"

### Resources
- LeetCode Easy-Medium problems
- SQL practice on LeetCode/HackerRank
- OS and DBMS basics
- "Introduction to Algorithms" for DSA fundamentals

---

> **Remember:** Oracle values well-rounded engineers who know DSA, SQL, and CS fundamentals. Practice SQL queries alongside coding problems. Moderate difficulty is fine — focus on correctness and clean code.
