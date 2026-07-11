# Adobe Interview Pattern

## Table of Contents
1. Interview Format
2. Most Asked Topics
3. Adobe Values and Culture
4. Types of Problems
5. Example Problems
6. Preparation Strategy

---

## 1. Interview Format

### Recruiter Screen (30 min)
- Background review and role discussion
- Salary expectations and team fit
- Typical questions about past projects

### Technical Phone Screen (45-60 min)
- 1-2 coding problems (medium difficulty)
- Usually one data structure + one string/tree problem
- Focus on clean, readable code
- May include a short system design discussion for senior roles

### On-site (4-5 rounds, 45-60 min each)
- **Coding / Algorithms** (2-3): DSA problems with emphasis on clean implementation
- **System Design** (1): For mid-senior roles (design an editor feature, document system)
- **Hiring Manager / Behavioral** (1): Team fit, project discussion
- **Culture Fit** (1): Adobe values alignment

### Key Differences from Other FAANG
- Adobe values **attention to detail** more than raw algorithmic speed
- Clean, maintainable code is heavily weighted
- OOP design principles are important (they make creative software)
- Problems tend to be medium difficulty rather than hard
- Strong focus on **strings** and **text processing** (PDF, Photoshop heritage)

---

## 2. Most Asked Topics

### Priority Matrix

| Priority | Topic | Frequency | Notes |
|----------|-------|-----------|-------|
| 1 | Trees (BST) | 85% | BST problems, LCA, traversals |
| 2 | Strings | 80% | Parsing, manipulation, pattern matching |
| 3 | Dynamic Programming | 70% | Medium-difficulty DP, not hard |
| 4 | Arrays | 70% | Sliding window, two pointers |
| 5 | HashMaps | 60% | Frequency count, caching |
| 6 | System Design | 50% | Document systems, collaboration |
| 7 | OOP Design | 40% | Design patterns, SOLID principles |

### Topic Frequency Graph
```
Trees:      ████████████████████
Strings:    ██████████████████
DP:         ██████████████
Arrays:     ██████████████
HashMaps:   ████████████
Sys Design: ██████████
OOP:        ████████
```

### What Makes Adobe Different
- Heavy emphasis on **string parsing** problems (Adobe is a document/media company)
- Tree problems often involve **hierarchical data** (layers, pages, components)
- DP problems are usually medium-level with clean state transitions
- OOP design is more important here than at most companies

---

## 3. Adobe Values and Culture

### Core Values

| Value | Meaning | Interview Impact |
|-------|---------|-----------------|
| **Creativity** | Innovation in products | Show creative problem-solving |
| **Diversity** | Inclusive environment | Respectful communication |
| **Integrity** | Ethical behavior | Honest about trade-offs |
| **Involvement** | Collaborative culture | Team-oriented thinking |
| **Excellence** | High standards | Attention to detail in code |

### Behavioral Questions
- "Tell me about a project where you had to pay extreme attention to detail"
- "Describe a time you improved an existing system's performance"
- "How do you approach debugging complex issues?"
- "Tell me about a time you mentored someone"
- "What creative solution have you designed recently?"

### What Adobe Looks For
1. Clean, well-structured code (not just correct)
2. Clear communication of thought process
3. Attention to edge cases
4. Understanding of OOP principles
5. Passion for creative tools and products

---

## 4. Types of Problems

### String Parsing (Adobe Specialty)
- Parse custom formats (CSV, JSON-like, config files)
- String transformation and encoding problems
- Pattern matching and search
- Substring problems with constraints
- Text justification and wrapping

### Tree Manipulation
- BST validation and construction
- Lowest Common Ancestor variants
- Tree serialization/deserialization
- Path sum problems
- Level-order and zigzag traversals

### Range / Interval Problems
- Range query problems (prefix sums)
- Interval scheduling and merging
- Segment tree basics (senior roles)
- Matrix range sum queries

### DP (Medium Focus)
- 1D DP (climbing stairs, house robber)
- 2D DP (unique paths, minimum path sum)
- Knapsack variants
- String DP (edit distance, LCS)
- Memoization vs tabulation discussion

### Design Problems
- Design a text editor
- Design a layer management system
- Design a document collaboration feature
- Design a photo filter pipeline

---

## 5. Example Problems

### Problem 1: Validate BST
**Problem:** Determine if a binary tree is a valid Binary Search Tree.

**Approach:** Use recursion with min/max bounds. Each node must be within a valid range defined by its ancestors.

```java
class TreeNode {
    int val;
    TreeNode left, right;
    TreeNode(int val) { this.val = val; }
}

public class ValidateBST {

    // APPROACH: Inorder traversal should be strictly increasing
    // Alternative: pass min/max bounds down the recursion
    
    public boolean isValidBST(TreeNode root) {
        return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }
    
    private boolean validate(TreeNode node, long min, long max) {
        if (node == null) return true;
        
        // Current node must be within bounds
        if (node.val <= min || node.val >= max) return false;
        
        // Left subtree: max becomes current node's value
        // Right subtree: min becomes current node's value
        return validate(node.left, min, node.val) 
            && validate(node.right, node.val, max);
    }

    // INORDER APPROACH: iterative with stack
    public boolean isValidBSTInorder(TreeNode root) {
        Deque<TreeNode> stack = new LinkedList<>();
        TreeNode current = root;
        TreeNode prev = null;
        
        while (current != null || !stack.isEmpty()) {
            while (current != null) {
                stack.push(current);
                current = current.left;
            }
            current = stack.pop();
            
            // In inorder, current should be > previous
            if (prev != null && current.val <= prev.val) {
                return false;
            }
            prev = current;
            current = current.right;
        }
        return true;
    }

    public static void main(String[] args) {
        TreeNode root = new TreeNode(2);
        root.left = new TreeNode(1);
        root.right = new TreeNode(3);
        
        ValidateBST sol = new ValidateBST();
        System.out.println(sol.isValidBST(root)); // true
        
        TreeNode invalid = new TreeNode(5);
        invalid.left = new TreeNode(1);
        invalid.right = new TreeNode(4);
        invalid.right.left = new TreeNode(3);
        invalid.right.right = new TreeNode(6);
        System.out.println(sol.isValidBST(invalid)); // false
    }
}
```

**Time:** O(n) | **Space:** O(h) where h is tree height

---

### Problem 2: Longest Palindromic Substring
**Problem:** Find the longest palindromic substring in a given string.

**Approach:** Expand around center. Every palindrome has a center — try all possible centers (2n-1 of them).

```java
public class LongestPalindrome {

    // APPROACH: Expand around each possible center
    // Centers: each character (odd length) + between characters (even length)
    
    public static String longestPalindrome(String s) {
        if (s == null || s.length() < 2) return s;
        
        String longest = "";
        
        for (int i = 0; i < s.length(); i++) {
            // Odd length palindrome (center = single character)
            String odd = expandAroundCenter(s, i, i);
            // Even length palindrome (center = between characters)
            String even = expandAroundCenter(s, i, i + 1);
            
            if (odd.length() > longest.length()) longest = odd;
            if (even.length() > longest.length()) longest = even;
        }
        
        return longest;
    }
    
    private static String expandAroundCenter(String s, int left, int right) {
        while (left >= 0 && right < s.length() 
               && s.charAt(left) == s.charAt(right)) {
            left--;
            right++;
        }
        // When loop ends, left and right are one step beyond valid palindrome
        return s.substring(left + 1, right);
    }

    public static void main(String[] args) {
        System.out.println(longestPalindrome("babad")); // "bab" or "aba"
        System.out.println(longestPalindrome("cbbd"));  // "bb"
        System.out.println(longestPalindrome("a"));      // "a"
        System.out.println(longestPalindrome("racecar")); // "racecar"
    }
}
```

**Time:** O(n²) | **Space:** O(1)

---

### Problem 3: Maximum Subarray Sum (Kadane's Algorithm)
**Problem:** Find the contiguous subarray with the largest sum.

**Approach:** Kadane's algorithm — track current sum, reset when it goes negative.

```java
public class MaxSubarraySum {

    // APPROACH: Kadane's Algorithm
    // At each position, decide: extend current subarray or start new one
    // If current sum < 0, starting fresh is always better
    
    public static int maxSubarraySum(int[] nums) {
        int maxSum = nums[0];
        int currentSum = nums[0];
        
        for (int i = 1; i < nums.length; i++) {
            // Either extend previous subarray or start fresh
            currentSum = Math.max(nums[i], currentSum + nums[i]);
            maxSum = Math.max(maxSum, currentSum);
        }
        
        return maxSum;
    }
    
    // VARIANT: Return the subarray indices as well
    public static int[] maxSubarrayWithIndices(int[] nums) {
        int maxSum = nums[0];
        int currentSum = nums[0];
        int start = 0, end = 0, tempStart = 0;
        
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] > currentSum + nums[i]) {
                currentSum = nums[i];
                tempStart = i;
            } else {
                currentSum += nums[i];
            }
            
            if (currentSum > maxSum) {
                maxSum = currentSum;
                start = tempStart;
                end = i;
            }
        }
        
        return new int[]{start, end, maxSum};
    }

    public static void main(String[] args) {
        int[] nums = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        System.out.println("Max sum: " + maxSubarraySum(nums)); // 6
        
        int[] result = maxSubarrayWithIndices(nums);
        System.out.println("Indices: " + result[0] + " to " + result[1] 
                         + ", Sum: " + result[2]);
    }
}
```

**Time:** O(n) | **Space:** O(1)

---

### Problem 4: Group Anagrams
**Problem:** Group strings that are anagrams of each other.

**Approach:** Use sorted string as key in HashMap. All anagrams share the same sorted form.

```java
import java.util.*;

public class GroupAnagrams {

    // APPROACH: Sort each string → use as HashMap key
    // "eat" → "aet", "tea" → "aet", "ate" → "aet" → same group
    
    public static List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        
        for (String s : strs) {
            char[] chars = s.toCharArray();
            Arrays.sort(chars);
            String sorted = new String(chars);
            
            map.computeIfAbsent(sorted, k -> new ArrayList<>()).add(s);
        }
        
        return new ArrayList<>(map.values());
    }

    // OPTIMIZED: Use character count as key instead of sorting
    public static List<List<String>> groupAnagramsOptimized(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        
        for (String s : strs) {
            int[] count = new int[26];
            for (char c : s.toCharArray()) {
                count[c - 'a']++;
            }
            
            StringBuilder sb = new StringBuilder();
            for (int c : count) {
                sb.append('#').append(c);
            }
            String key = sb.toString();
            
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
        }
        
        return new ArrayList<>(map.values());
    }

    public static void main(String[] args) {
        String[] strs = {"eat", "tea", "tan", "ate", "nat", "bat"};
        List<List<String>> groups = groupAnagrams(strs);
        System.out.println(groups);
        // [[eat, tea, ate], [tan, nat], [bat]]
    }
}
```

**Time:** O(n × k log k) for sorting approach, O(n × k) for count approach | **Space:** O(n × k)

---

### Problem 5: Coin Change
**Problem:** Find minimum number of coins to make a given amount.

**Approach:** Bottom-up DP. dp[i] = min coins needed to make amount i.

```java
import java.util.Arrays;

public class CoinChange {

    // APPROACH: Bottom-up DP
    // dp[i] = minimum coins needed for amount i
    // dp[0] = 0 (base case: 0 coins for amount 0)
    // dp[i] = min(dp[i - coin] + 1) for each coin
    
    public static int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1); // Use amount+1 as "infinity"
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

    // VARIANT: Return the actual coins used
    public static List<Integer> coinChangeWithCoins(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        int[] parent = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        parent[0] = -1;
        
        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (coin <= i && dp[i - coin] + 1 < dp[i]) {
                    dp[i] = dp[i - coin] + 1;
                    parent[i] = coin;
                }
            }
        }
        
        if (dp[amount] > amount) return new ArrayList<>();
        
        List<Integer> result = new ArrayList<>();
        int current = amount;
        while (current > 0) {
            result.add(parent[current]);
            current -= parent[current];
        }
        return result;
    }

    public static void main(String[] args) {
        int[] coins1 = {1, 5, 10, 25};
        System.out.println(coinChange(coins1, 30)); // 2 (25 + 5)
        
        int[] coins2 = {2};
        System.out.println(coinChange(coins2, 3)); // -1 (impossible)
        
        System.out.println(coinChangeWithCoins(coins1, 30)); // [5, 25]
    }
}
```

**Time:** O(amount × coins) | **Space:** O(amount)

---

## 6. Preparation Strategy

### Focus Areas (4-Week Plan)

#### Week 1: Strings and Trees
- [ ] String parsing problems (20 problems)
- [ ] BST operations: insert, delete, search, validate
- [ ] Tree traversals: inorder, preorder, postorder, level-order
- [ ] LCA, path sum, diameter problems
- [ ] Practice: 20 problems

#### Week 2: Arrays and HashMaps
- [ ] Sliding window problems (15 problems)
- [ ] Two pointer technique
- [ ] Prefix sum and range queries
- [ ] HashMap pattern problems
- [ ] Practice: 20 problems

#### Week 3: Dynamic Programming
- [ ] 1D DP patterns (10 problems)
- [ ] 2D DP patterns (10 problems)
- [ ] String DP (edit distance, LCS, palindrome)
- [ ] Knapsack variants
- [ ] Practice: 15 problems

#### Week 4: Design and Mock Interviews
- [ ] OOP design patterns (Singleton, Factory, Observer)
- [ ] SOLID principles
- [ ] Design a text editor / document system
- [ ] Mock interviews (3-5 sessions)
- [ ] Review and weak areas

### Adobe-Specific Tips
1. **Write clean code** — Adobe values readability over clever one-liners
2. **Use meaningful variable names** — `maxLength` not `ml`
3. **Handle edge cases explicitly** — null checks, empty inputs, single elements
4. **Explain your thought process** — Adobe interviewers want to see how you think
5. **Practice string problems** — Adobe's heritage is in document/media processing
6. **Know OOP well** — They make creative software; design patterns matter
7. **Don't over-optimize** — Medium solutions are fine; correctness first
8. **Prepare for follow-ups** — "Can you optimize?" "What if input is very large?"

### Common Follow-up Questions
- "What is the time and space complexity?"
- "Can you do it without extra space?"
- "What if the input has millions of elements?"
- "How would you handle concurrent access?"
- "Can you make the code more readable?"

### Resources
- LeetCode Medium problems (focus on strings and trees)
- "Cracking the Coding Interview" — OOP design chapters
- Practice explaining code out loud
- Adobe's engineering blog for product insights

---

> **Remember:** Adobe looks for engineers who write clean, maintainable code. They don't need you to solve LeetCode Hards — they need you to solve Medium problems perfectly with excellent code quality and clear communication.
