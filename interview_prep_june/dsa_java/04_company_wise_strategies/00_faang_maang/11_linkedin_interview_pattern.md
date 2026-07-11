# LinkedIn Interview Pattern

## Table of Contents
1. Interview Format
2. Most Asked Topics
3. LinkedIn Culture
4. Types of Problems
5. Example Problems
6. Preparation Strategy

---

## 1. Interview Format

### Recruiter Screen (30 min)
- Background review and role discussion
- Focus on social graph and data problems
- Discussion of past projects and impact

### Technical Phone Screen (45-60 min)
- 1-2 coding problems (Medium to Hard difficulty)
- Often includes system design discussion
- Focus on scalable, data-driven solutions
- Well-structured and fair interviews

### On-site (4-5 rounds, 45-60 min each)
- **Coding / Algorithms** (2-3): DSA problems with data focus
- **System Design** (1): Scalable data systems (feed, search, recommendations)
- **Hiring Manager / Behavioral** (1): Team fit, product thinking

### Key Differences from Other FAANG
- Part of Microsoft but has **distinct engineering culture**
- Known for **fair and well-structured** interviews
- **Data-driven problems** are common (feed ranking, search)
- **Social graph** problems appear frequently
- Emphasis on **product thinking** and user impact
- Good work-life balance reflected in interview pace

---

## 2. Most Asked Topics

### Priority Matrix

| Priority | Topic | Frequency | Notes |
|----------|-------|-----------|-------|
| 1 | Arrays | 85% | Advanced problems, optimization |
| 2 | Strings | 80% | Pattern matching, parsing |
| 3 | Trees | 75% | BST, binary tree, trie |
| 4 | System Design | 70% | Feed, search, recommendations |
| 5 | Graphs | 60% | Social graph, connectivity |
| 6 | DP | 55% | Medium difficulty |
| 7 | HashMaps | 55% | Frequency, grouping |

### Topic Frequency Graph
```
Arrays:     ████████████████████
Strings:    ██████████████████
Trees:      █████████████████
Sys Design: ██████████████
Graphs:     ████████████
DP:         ███████████
HashMaps:   ███████████
```

### What Makes LinkedIn Different
- **Social graph problems** — connections, recommendations, feed
- **Data-driven** — ranking, search, recommendation systems
- **Fair interviews** — Well-structured, reasonable difficulty
- **Product thinking** — How does this feature affect users?
- **System design** is important — especially for mid-senior roles
- **Search problems** — LinkedIn is a search/discovery platform

---

## 3. LinkedIn Culture

### Core Values

| Value | Meaning | Interview Impact |
|-------|---------|-----------------|
| **Members First** | User-centric decisions | Think about user impact |
| **Be Open, Honest, Constructive** | Direct communication | Clear thought process |
| **Be Your Best Self** | Personal growth | Show learning mindset |
| **Play as a Team** | Collaboration | Team-oriented solutions |
| **Trust** | Build trust with members | Reliable, secure code |

### What LinkedIn Looks For
1. **Product thinking** — How does your code affect users?
2. **Data-driven solutions** — Use data to drive decisions
3. **Scalability** — Handle millions of users
4. **Clean code** — Maintainable, readable solutions
5. **Social graph understanding** — Connections, networks, communities

### Behavioral Questions
- "Tell me about a time you built a feature that impacted millions of users"
- "How do you approach building a recommendation system?"
- "Describe a time you had to optimize for user experience"
- "How do you handle disagreements about technical decisions?"

---

## 4. Types of Problems

### Social Graph Problems
- Find connections between users
- Degree of separation (BFS)
- Friend recommendation algorithms
- Community detection
- Influence analysis

### Search/Discovery Problems
- Relevance ranking
- Autocomplete implementation
- Content recommendation
- Feed ranking
- Job matching algorithms

### Array/String Problems
- Sliding window variants
- Two pointer techniques
- String parsing and manipulation
- Subarray problems
- Sorting and searching

### Tree Problems
- BST operations
- Trie for autocomplete
- Tree serialization
- Path problems
- Level-order traversal

### System Design
- Design LinkedIn feed
- Design job matching system
- Design messaging system
- Design recommendation engine
- Design search/autocomplete

---

## 5. Example Problems

### Problem 1: Find Duplicate Number
**Problem:** Given an array of n+1 integers where each is between 1 and n, find one duplicate.

**Approach:** Floyd's cycle detection — treat array as linked list where value = next pointer.

```java
public class FindDuplicate {

    // APPROACH: Floyd's Cycle Detection
    // Treat array as linked list: index → value → next index
    // If duplicate exists, there's a cycle
    // Find entry point of cycle = duplicate number
    
    public static int findDuplicate(int[] nums) {
        // Phase 1: Find intersection point
        int slow = nums[0];
        int fast = nums[0];
        
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        
        // Phase 2: Find entrance of cycle
        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        
        return slow;
    }

    // BINARY SEARCH APPROACH: Count elements ≤ mid
    public static int findDuplicateBinarySearch(int[] nums) {
        int low = 1, high = nums.length - 1;
        
        while (low < high) {
            int mid = low + (high - low) / 2;
            int count = 0;
            
            for (int num : nums) {
                if (num <= mid) count++;
            }
            
            if (count > mid) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }
        
        return low;
    }

    public static void main(String[] args) {
        int[] nums1 = {1, 3, 4, 2, 2};
        System.out.println(findDuplicate(nums1)); // 2
        
        int[] nums2 = {3, 1, 3, 4, 2};
        System.out.println(findDuplicate(nums2)); // 3
        
        int[] nums3 = {1, 1};
        System.out.println(findDuplicate(nums3)); // 1
    }
}
```

**Time:** O(n) for Floyd's, O(n log n) for binary search | **Space:** O(1)

---

### Problem 2: Lowest Common Ancestor of a Binary Tree
**Problem:** Find the lowest common ancestor of two nodes in a binary tree.

**Approach:** Recursive — if current node is one of the targets, return it. Otherwise, search left and right subtrees.

```java
public class LowestCommonAncestor {

    static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    // APPROACH: Recursive DFS
    // If current node is null, p, or q → return current node
    // Recurse left and right
    // If both return non-null → current node is LCA
    // If only one returns non-null → that's the LCA
    
    public static TreeNode lowestCommonAncestor(TreeNode root, 
                                                  TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) return root;
        
        TreeNode left = lowestCommonAncestor(root.left, p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);
        
        if (left != null && right != null) return root;
        
        return left != null ? left : right;
    }

    // VARIANT: For BST (can use BST property)
    public static TreeNode lowestCommonAncestorBST(TreeNode root, 
                                                    TreeNode p, TreeNode q) {
        if (root.val > p.val && root.val > q.val) {
            return lowestCommonAncestorBST(root.left, p, q);
        }
        if (root.val < p.val && root.val < q.val) {
            return lowestCommonAncestorBST(root.right, p, q);
        }
        return root;
    }

    public static void main(String[] args) {
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(5);
        root.right = new TreeNode(1);
        root.left.left = new TreeNode(6);
        root.left.right = new TreeNode(2);
        root.right.left = new TreeNode(0);
        root.right.right = new TreeNode(8);
        
        TreeNode lca = lowestCommonAncestor(root, root.left, root.right);
        System.out.println("LCA of 5 and 1: " + lca.val); // 3
        
        TreeNode lca2 = lowestCommonAncestor(root, root.left, root.left.right);
        System.out.println("LCA of 5 and 2: " + lca2.val); // 5
    }
}
```

**Time:** O(n) | **Space:** O(h) for recursion stack

---

### Problem 3: Binary Search
**Problem:** Implement binary search on a sorted array.

**Approach:** Divide and conquer — compare target with mid, eliminate half.

```java
public class BinarySearch {

    // APPROACH: Standard binary search
    // Compare target with mid element
    // If equal, return mid
    // If target < mid, search left half
    // If target > mid, search right half
    
    public static int binarySearch(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (nums[mid] == target) {
                return mid;
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1;
    }
    
    // VARIANT: Find first occurrence
    public static int findFirst(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        int result = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (nums[mid] == target) {
                result = mid;
                right = mid - 1; // Continue searching left
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }
    
    // VARIANT: Find last occurrence
    public static int findLast(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        int result = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (nums[mid] == target) {
                result = mid;
                left = mid + 1; // Continue searching right
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }

    public static void main(String[] args) {
        int[] nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        System.out.println(binarySearch(nums, 5));  // 4
        System.out.println(binarySearch(nums, 11)); // -1
        
        int[] nums2 = {1, 2, 2, 2, 3, 4, 5};
        System.out.println(findFirst(nums2, 2)); // 1
        System.out.println(findLast(nums2, 2));  // 3
    }
}
```

**Time:** O(log n) | **Space:** O(1)

---

### Problem 4: Subarray Sum Equals K
**Problem:** Find the number of subarrays whose sum equals k.

**Approach:** Prefix sum with HashMap — count prefix sums.

```java
import java.util.*;

public class SubarraySumK {

    // APPROACH: Prefix sum + HashMap
    // If prefixSum[j] - prefixSum[i] = k, then subarray(i+1..j) sums to k
    // Count how many times each prefixSum appears
    
    public static int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> prefixCount = new HashMap<>();
        prefixCount.put(0, 1); // Empty prefix has sum 0
        
        int prefixSum = 0;
        int count = 0;
        
        for (int num : nums) {
            prefixSum += num;
            
            // If (prefixSum - k) exists, there's a subarray summing to k
            if (prefixCount.containsKey(prefixSum - k)) {
                count += prefixCount.get(prefixSum - k);
            }
            
            prefixCount.merge(prefixSum, 1, Integer::sum);
        }
        
        return count;
    }

    public static void main(String[] args) {
        int[] nums1 = {1, 1, 1};
        System.out.println(subarraySum(nums1, 2)); // 2
        
        int[] nums2 = {1, 2, 3};
        System.out.println(subarraySum(nums2, 3)); // 2
    }
}
```

**Time:** O(n) | **Space:** O(n)

---

### Problem 5: Maximum Depth of Binary Tree
**Problem:** Find the maximum depth of a binary tree.

**Approach:** Recursive DFS — depth = 1 + max(depth of left, depth of right).

```java
public class MaxDepth {

    static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    // APPROACH: Recursive DFS
    // Base case: null node has depth 0
    // Recursive: depth = 1 + max(left depth, right depth)
    
    public static int maxDepth(TreeNode root) {
        if (root == null) return 0;
        
        int leftDepth = maxDepth(root.left);
        int rightDepth = maxDepth(root.right);
        
        return 1 + Math.max(leftDepth, rightDepth);
    }
    
    // ITERATIVE APPROACH: BFS (level order)
    public static int maxDepthIterative(TreeNode root) {
        if (root == null) return 0;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        int depth = 0;
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            depth++;
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.poll();
                if (node.left != null) queue.offer(node.left);
                if (node.right != null) queue.offer(node.right);
            }
        }
        
        return depth;
    }

    public static void main(String[] args) {
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(9);
        root.right = new TreeNode(20);
        root.right.left = new TreeNode(15);
        root.right.right = new TreeNode(7);
        
        System.out.println(maxDepth(root)); // 3
        System.out.println(maxDepthIterative(root)); // 3
    }
}
```

**Time:** O(n) | **Space:** O(h) for recursive, O(n) for iterative

---

## 6. Preparation Strategy

### Focus Areas (4-Week Plan)

#### Week 1: Arrays and Strings
- [ ] Sliding window problems (10 problems)
- [ ] Two pointer technique (10 problems)
- [ ] Prefix sum problems (5 problems)
- [ ] String manipulation (10 problems)
- [ ] Practice: 25 problems

#### Week 2: Trees and HashMaps
- [ ] BST operations (10 problems)
- [ ] Binary tree traversals (10 problems)
- [ ] LCA and path problems (5 problems)
- [ ] HashMap patterns (10 problems)
- [ ] Practice: 25 problems

#### Week 3: Graphs and DP
- [ ] BFS/DFS on graphs (10 problems)
- [ ] Social graph problems (5 problems)
- [ ] 1D DP patterns (10 problems)
- [ ] 2D DP patterns (5 problems)
- [ ] Practice: 20 problems

#### Week 4: System Design and Mocks
- [ ] LinkedIn feed design
- [ ] Recommendation system design
- [ ] Search/autocomplete design
- [ ] Mock interviews (3-5 sessions)
- [ ] Review weak areas

### LinkedIn-Specific Tips
1. **Social graph problems** — Practice BFS/DFS on graphs
2. **Product thinking** — How does this feature affect users?
3. **System design** — Feed, search, recommendation systems
4. **Clean code** — LinkedIn values maintainable solutions
5. **Data-driven** — Use data to drive your decisions
6. **Fair interviews** — They're well-structured; don't panic
7. **Medium-Hard problems** — They're moderate difficulty
8. **Search problems** — LinkedIn is a discovery platform

### Common Follow-up Questions
- "How would this work for 100M+ users?"
- "How would you handle real-time updates?"
- "What if the graph doesn't fit in memory?"
- "How would you test this recommendation system?"
- "What's the latency requirement?"

### Resources
- LeetCode Graph and Tree problems
- "System Design Interview" by Alex Xu
- LinkedIn engineering blog
- Social network analysis concepts

---

> **Remember:** LinkedIn values fair, well-structured solutions. They want you to think about product impact and user experience. Show that you can build scalable, data-driven systems that millions of people use daily.
