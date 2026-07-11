# Adobe India Interview

> "Adobe India is one of the best product companies in India. They test deep algorithmic thinking, clean code, and computer science fundamentals. Known for BST problems, DP, and LRU cache variants."

---

## 1. Company Overview

- **Package:** ₹15-45 LPA (freshers, varies by role and college)
- **Hiring:** Campus + Off-campus + Referrals
- **Rounds:** Online Test → Phone Screen → Onsite (4 rounds)
- **Focus:** DSA, OOP, System Design, CS Fundamentals
- **Key Differentiator:** **Clean code** and **optimal solutions** with strong CS fundamentals

---

## 2. Interview Process

### Online Test (HackerRank/CodeSignal)
- 3-4 coding problems (Easy to Medium-Hard)
- Time limit: 90-120 minutes
- Topics: Arrays, Strings, Trees, DP
- Cutoff is usually high — aim for all test cases

### Phone Screen (45-60 min)
- 1-2 coding problems (Medium difficulty)
- May include OOP design discussion
- Focus on clean, readable code
- Strong communication expected

### On-site (4 rounds, 45-60 min each)

| Round | Focus | Difficulty |
|-------|-------|------------|
| Round 1 | DSA Coding (Trees/Strings) | Medium-Hard |
| Round 2 | DSA Coding (DP/Arrays) | Medium-Hard |
| Round 3 | System Design / OOP | Medium |
| Round 4 | Hiring Manager + Behavioral | Culture fit |

### What Makes Adobe India Different
- **BST problems** are extremely common (almost every interview)
- **LRU Cache** is a frequent question
- **Clean code** is heavily weighted — they review code quality
- **CS fundamentals** — OS, DBMS, networking basics may be asked
- **Product thinking** — How does this feature serve users?

---

## 3. Most Asked Topics

### Topic Priority

| Priority | Topic | Frequency | Example Problems |
|----------|-------|-----------|-----------------|
| 1 | Trees (BST) | 90% | Validate BST, LCA, Kth smallest, BST from sorted array |
| 2 | DP | 80% | LIS, knapsack, coin change, edit distance |
| 3 | HashMaps | 75% | LRU cache, two sum, group anagrams |
| 4 | Arrays | 70% | Sliding window, Kadane's, merge intervals |
| 5 | Strings | 65% | Palindrome, string parsing, pattern matching |
| 6 | System Design | 50% | Document editor, layer management |
| 7 | OOP Design | 45% | Design patterns, SOLID principles |

### Topic Frequency Graph
```
BST:        ████████████████████
DP:         ██████████████████
HashMaps:   █████████████████
Arrays:     ██████████████
Strings:    █████████████
Sys Design: ██████████
OOP:        █████████
```

---

## 4. Common Problems (Top 20)

### Trees / BST
1. Validate Binary Search Tree
2. Lowest Common Ancestor
3. Kth Smallest Element in BST
4. Binary Tree Right Side View
5. Construct BST from Preorder Traversal
6. Inorder Successor in BST
7. Flatten Binary Tree to Linked List

### Dynamic Programming
8. Longest Increasing Subsequence
9. 0/1 Knapsack
10. Coin Change (minimum coins)
11. Edit Distance
12. Longest Common Subsequence
13. Maximum Product Subarray

### HashMap / Design
14. LRU Cache (frequently asked!)
15. Two Sum
16. Group Anagrams
17. Subarray Sum Equals K

### Arrays / Strings
18. Merge Intervals
19. Maximum Subarray (Kadane's)
20. Longest Palindromic Substring

---

## 5. Example Problems with Approaches

### Problem 1: LRU Cache
**Why Adobe asks this:** Cache management is core to document editing (keeping recently used files/pages in memory).

```java
import java.util.*;

public class LRUCache {

    private class Node {
        int key, value;
        Node prev, next;
        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }
    
    private int capacity;
    private Map<Integer, Node> map;
    private Node head, tail;
    
    public LRUCache(int capacity) {
        this.capacity = capacity;
        map = new HashMap<>();
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head.next = tail;
        tail.prev = head;
    }
    
    private void addToFront(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
    
    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    private void moveToHead(Node node) {
        removeNode(node);
        addToFront(node);
    }
    
    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        moveToHead(node);
        return node.value;
    }
    
    public void put(int key, int value) {
        if (map.containsKey(key)) {
            Node node = map.get(key);
            node.value = value;
            moveToHead(node);
        } else {
            Node newNode = new Node(key, value);
            map.put(key, newNode);
            addToFront(newNode);
            
            if (map.size() > capacity) {
                Node lru = tail.prev;
                removeNode(lru);
                map.remove(lru.key);
            }
        }
    }
    
    public static void main(String[] args) {
        LRUCache cache = new LRUCache(2);
        cache.put(1, 1);
        cache.put(2, 2);
        System.out.println(cache.get(1)); // 1
        cache.put(3, 3); // Evicts key 2
        System.out.println(cache.get(2)); // -1
        cache.put(4, 4); // Evicts key 1
        System.out.println(cache.get(1)); // -1
        System.out.println(cache.get(3)); // 3
        System.out.println(cache.get(4)); // 4
    }
}
```

**Time:** O(1) for get/put | **Space:** O(capacity)

---

### Problem 2: Validate BST
**Why Adobe asks this:** Tree structures are used in document hierarchies (pages → sections → paragraphs).

```java
public class ValidateBST {

    static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }
    
    // APPROACH: Recursion with bounds
    public boolean isValidBST(TreeNode root) {
        return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }
    
    private boolean validate(TreeNode node, long min, long max) {
        if (node == null) return true;
        if (node.val <= min || node.val >= max) return false;
        
        return validate(node.left, min, node.val) 
            && validate(node.right, node.val, max);
    }
    
    // INORDER APPROACH: iterative
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
            
            if (prev != null && current.val <= prev.val) return false;
            prev = current;
            current = current.right;
        }
        return true;
    }
}
```

**Time:** O(n) | **Space:** O(h)

---

### Problem 3: Longest Increasing Subsequence
**Why Adobe asks this:** Optimization problems related to document layout and content organization.

```java
import java.util.*;

public class LIS {

    // O(n²) DP approach
    public static int lengthOfLIS(int[] nums) {
        int n = nums.length;
        int[] dp = new int[n];
        Arrays.fill(dp, 1);
        
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[j] < nums[i]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
        }
        
        int max = 0;
        for (int val : dp) max = Math.max(max, val);
        return max;
    }
    
    // O(n log n) Binary Search approach
    public static int lengthOfLISBinarySearch(int[] nums) {
        List<Integer> tails = new ArrayList<>();
        
        for (int num : nums) {
            int pos = Collections.binarySearch(tails, num);
            if (pos < 0) pos = -(pos + 1);
            
            if (pos == tails.size()) {
                tails.add(num);
            } else {
                tails.set(pos, num);
            }
        }
        
        return tails.size();
    }

    public static void main(String[] args) {
        int[] nums = {10, 9, 2, 5, 3, 7, 101, 18};
        System.out.println(lengthOfLIS(nums)); // 4
        System.out.println(lengthOfLISBinarySearch(nums)); // 4
    }
}
```

**Time:** O(n²) for DP, O(n log n) for binary search | **Space:** O(n)

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

### Problem 5: Merge Intervals
```java
import java.util.*;

public class MergeIntervals {
    public static int[][] merge(int[][] intervals) {
        if (intervals.length <= 1) return intervals;
        
        Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
        List<int[]> merged = new ArrayList<>();
        merged.add(intervals[0]);
        
        for (int i = 1; i < intervals.length; i++) {
            int[] last = merged.get(merged.size() - 1);
            if (intervals[i][0] <= last[1]) {
                last[1] = Math.max(last[1], intervals[i][1]);
            } else {
                merged.add(intervals[i]);
            }
        }
        
        return merged.toArray(new int[0][]);
    }
    
    public static void main(String[] args) {
        int[][] intervals = {{1,3},{2,6},{8,10},{15,18}};
        int[][] result = merge(intervals);
        for (int[] interval : result) {
            System.out.print(Arrays.toString(interval) + " ");
        }
        // [[1,6], [8,10], [15,18]]
    }
}
```

---

## 6. Preparation Strategy

### Focus Areas (4-Week Plan)

#### Week 1: BST Mastery
- [ ] BST operations: insert, delete, search, validate
- [ ] BST from sorted array / preorder / inorder
- [ ] Kth smallest/largest in BST
- [ ] Inorder successor/predecessor
- [ ] LCA in BST
- [ ] Practice: 15 BST problems

#### Week 2: DP Fundamentals
- [ ] 1D DP: LIS, coin change, house robber
- [ ] 2D DP: edit distance, LCS
- [ ] Knapsack variants (0/1, unbounded)
- [ ] String DP: palindrome, subsequence
- [ ] Practice: 15 DP problems

#### Week 3: Arrays, Strings, HashMaps
- [ ] Sliding window problems
- [ ] Two pointer technique
- [ ] Prefix sums
- [ ] HashMap patterns (two sum, group anagrams)
- [ ] LRU Cache (must know!)
- [ ] Practice: 15 problems

#### Week 4: Design + CS Fundamentals + Mocks
- [ ] OOP design patterns
- [ ] System design basics (document editor)
- [ ] OS basics (processes, threads, deadlocks)
- [ ] DBMS basics (normalization, transactions)
- [ ] Mock interviews (3-5 sessions)

### Adobe India-Specific Tips
1. **Master BST** — Almost every interview has a BST problem
2. **LRU Cache is a must** — Practice it until you can write it in 5 minutes
3. **Clean code** — Use meaningful names, proper indentation
4. **CS fundamentals** — OS, DBMS, networking basics may be asked
5. **Product thinking** — Frame problems in document/media context
6. **Optimal solutions** — O(n²) may not pass; aim for O(n log n)
7. **Edge cases** — Empty tree, single node, duplicate values
8. **Communication** — Explain your approach before coding

### Common Follow-up Questions
- "Can you optimize the time complexity?"
- "What if the tree has millions of nodes?"
- "Can you do it without extra space?"
- "How would this work in a multi-threaded environment?"
- "What's the space complexity?"

---

> **Remember:** Adobe India values clean code and strong CS fundamentals. BST problems are their signature — master them. LRU Cache appears in almost every batch. Focus on optimal solutions with clear communication.
