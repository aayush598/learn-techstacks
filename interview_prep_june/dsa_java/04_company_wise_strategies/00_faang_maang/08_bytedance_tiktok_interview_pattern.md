# ByteDance / TikTok Interview Pattern

## Table of Contents
1. Interview Format
2. Most Asked Topics
3. ByteDance Culture
4. Types of Problems
5. Example Problems
6. Preparation Strategy

---

## 1. Interview Format

### Recruiter Screen (30 min)
- Background review and role discussion
- Focus on algorithmic problem-solving experience
- Discussion of past projects and technical depth

### Technical Phone Screen (45-60 min)
- 1-2 coding problems (Medium to Hard difficulty)
- ByteDance is known for asking **harder problems** than average
- Focus on optimal solutions, not just correct ones
- Strict time pressure — they want fast, correct implementations

### On-site (4-5 rounds, 45-60 min each)
- **Coding / Algorithms** (3): Heavy DSA, often Hard problems
- **System Design** (1): Scalable systems (for mid-senior)
- **Behavioral / Culture** (1): Fast-paced culture fit

### Key Differences from Other FAANG
- ByteDance asks **harder algorithm problems** on average
- They expect **optimal solutions** — O(n²) when O(n log n) exists may not pass
- Speed matters — they want you to code fast and correctly
- **Edge cases** are heavily tested
- TikTok-specific: recommendation system problems are common
- Known for asking problems that require creative optimization

---

## 2. Most Asked Topics

### Priority Matrix

| Priority | Topic | Frequency | Notes |
|----------|-------|-----------|-------|
| 1 | Arrays | 90% | Advanced: sliding window, two pointers |
| 2 | Strings | 85% | Pattern matching, substring problems |
| 3 | Dynamic Programming | 85% | Hard DP, optimization variants |
| 4 | Graphs | 75% | BFS, DFS, shortest path |
| 5 | Backtracking | 70% | Permutations, combinations, constraints |
| 6 | Trees | 65% | Advanced tree problems |
| 7 | HashMaps | 60% | Frequency, grouping, sliding window |

### Topic Frequency Graph
```
Arrays:     ████████████████████
Strings:    ███████████████████
DP:         ███████████████████
Graphs:     █████████████████
Backtrack:  ██████████████
Trees:      █████████████
HashMaps:   ████████████
```

### What Makes ByteDance Different
- **Hard problems** are the norm, not the exception
- Optimization is not optional — they expect the best solution
- Creative approaches to standard problems
- Heavy emphasis on **edge case handling**
- Speed of implementation matters (they time you)
- Known for problems that combine multiple techniques

---

## 3. ByteDance Culture

### Core Values

| Value | Meaning | Interview Impact |
|-------|---------|-----------------|
| **Always Day 1** | Startup mentality, fast growth | Show adaptability, speed |
| **Default to Action** | Bias for action, not overthinking | Quick problem-solving |
| **Be Deep** | Deep expertise in your area | Technical depth |
| **Be Candid** | Honest, direct communication | Clear thought process |
| **Be Creative** | Innovation and creativity | Creative solutions |

### What ByteDance Looks For
1. **Speed** — Quick problem-solving, fast coding
2. **Optimization** — Always find the best solution
3. **Edge cases** — Handle all boundary conditions
4. **Technical depth** — Deep understanding of algorithms
5. **Adaptability** — Learn new things quickly

### Behavioral Questions
- "Tell me about a time you had to deliver under tight deadlines"
- "How do you approach optimizing code for performance?"
- "Describe a time you found an innovative solution"
- "How do you handle ambiguity in requirements?"

---

## 4. Types of Problems

### Hard Array/String Problems
- Sliding window maximum/minimum
- Subarray with given sum (variants)
- Longest substring with constraints
- String matching with wildcards
- Minimum window substring

### Hard DP Problems
- Stock trading with multiple transactions
- Burst balloons
- Regular expression matching
- Edit distance with constraints
- Longest increasing subsequence variants

### Graph Problems
- Word ladder (shortest transformation sequence)
- Alien dictionary (topological sort)
- Cheapest flights within K stops
- Graph with edge weights and constraints

### Backtracking
- N-Queens variants
- Sudoku solver
- Word search in grid
- Combination sum with constraints

### Optimization Problems
- Merge K sorted arrays
- Find median from data stream
- Sliding window median
- Randomized data structures

---

## 5. Example Problems

### Problem 1: Longest Substring Without Repeating Characters
**Problem:** Find the length of the longest substring without repeating characters.

**Approach:** Sliding window with HashSet to track characters in current window.

```java
import java.util.*;

public class LongestSubstring {

    // APPROACH: Sliding window with HashSet
    // Expand right pointer, shrink left when duplicate found
    
    public static int lengthOfLongestSubstring(String s) {
        Set<Character> window = new HashSet<>();
        int left = 0, maxLen = 0;
        
        for (int right = 0; right < s.length(); right++) {
            // Shrink window until no duplicate
            while (window.contains(s.charAt(right))) {
                window.remove(s.charAt(left));
                left++;
            }
            window.add(s.charAt(right));
            maxLen = Math.max(maxLen, right - left + 1);
        }
        
        return maxLen;
    }
    
    // OPTIMIZED: HashMap with last seen index
    // Skip left pointer directly to last occurrence + 1
    public static int lengthOfLongestSubstringOptimized(String s) {
        Map<Character, Integer> lastSeen = new HashMap<>();
        int left = 0, maxLen = 0;
        
        for (int right = 0; right < s.length(); right++) {
            if (lastSeen.containsKey(s.charAt(right))) {
                // Jump left pointer past the last occurrence
                left = Math.max(left, lastSeen.get(s.charAt(right)) + 1);
            }
            lastSeen.put(s.charAt(right), right);
            maxLen = Math.max(maxLen, right - left + 1);
        }
        
        return maxLen;
    }

    public static void main(String[] args) {
        System.out.println(lengthOfLongestSubstring("abcabcbb")); // 3
        System.out.println(lengthOfLongestSubstring("bbbbb"));    // 1
        System.out.println(lengthOfLongestSubstring("pwwkew"));   // 3
        System.out.println(lengthOfLongestSubstring(""));          // 0
    }
}
```

**Time:** O(n) | **Space:** O(min(n, charset size))

---

### Problem 2: Minimum Window Substring
**Problem:** Find the minimum window in s that contains all characters of t.

**Approach:** Sliding window with character frequency tracking.

```java
import java.util.*;

public class MinWindowSubstring {

    // APPROACH: Sliding window
    // 1. Expand right until all chars of t are included
    // 2. Contract left to find minimum window
    // 3. Track when we have all required characters
    
    public static String minWindow(String s, String t) {
        if (s.length() < t.length()) return "";
        
        Map<Character, Integer> need = new HashMap<>();
        Map<Character, Integer> have = new HashMap<>();
        
        // Count characters needed from t
        for (char c : t.toCharArray()) {
            need.put(c, need.getOrDefault(c, 0) + 1);
        }
        
        int required = need.size(); // Number of unique chars needed
        int formed = 0;             // Number of unique chars with required count
        int left = 0;
        int minLen = Integer.MAX_VALUE;
        int minStart = 0;
        
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            have.put(c, have.getOrDefault(c, 0) + 1);
            
            // Check if this char's count matches required
            if (have.get(c).intValue() == need.getOrDefault(c, 0).intValue()) {
                formed++;
            }
            
            // Try to contract window
            while (formed == required) {
                if (right - left + 1 < minLen) {
                    minLen = right - left + 1;
                    minStart = left;
                }
                
                char leftChar = s.charAt(left);
                have.put(leftChar, have.get(leftChar) - 1);
                if (have.get(leftChar) < need.getOrDefault(leftChar, 0)) {
                    formed--;
                }
                left++;
            }
        }
        
        return minLen == Integer.MAX_VALUE ? "" 
               : s.substring(minStart, minStart + minLen);
    }

    public static void main(String[] args) {
        System.out.println(minWindow("ADOBECODEBANC", "ABC")); // "BANC"
        System.out.println(minWindow("a", "a"));               // "a"
        System.out.println(minWindow("a", "aa"));              // ""
    }
}
```

**Time:** O(|s| + |t|) | **Space:** O(|s| + |t|)

---

### Problem 3: Word Ladder
**Problem:** Find the shortest transformation sequence from beginWord to endWord.

**Approach:** BFS on word graph — each word is a node, edges connect words differing by one letter.

```java
import java.util.*;

public class WordLadder {

    // APPROACH: BFS (shortest path in unweighted graph)
    // Each level of BFS = one letter change
    // Stop when we reach endWord
    
    public static int ladderLength(String beginWord, String endWord, 
                                    List<String> wordList) {
        Set<String> wordSet = new HashSet<>(wordList);
        if (!wordSet.contains(endWord)) return 0;
        
        Queue<String> queue = new LinkedList<>();
        queue.offer(beginWord);
        int level = 1;
        
        while (!queue.isEmpty()) {
            int size = queue.size();
            
            for (int i = 0; i < size; i++) {
                String current = queue.poll();
                char[] chars = current.toCharArray();
                
                // Try changing each character
                for (int j = 0; j < chars.length; j++) {
                    char original = chars[j];
                    
                    for (char c = 'a'; c <= 'z'; c++) {
                        if (c == original) continue;
                        
                        chars[j] = c;
                        String newWord = new String(chars);
                        
                        if (newWord.equals(endWord)) return level + 1;
                        
                        if (wordSet.contains(newWord)) {
                            queue.offer(newWord);
                            wordSet.remove(newWord); // Mark as visited
                        }
                    }
                    
                    chars[j] = original; // Restore
                }
            }
            
            level++;
        }
        
        return 0;
    }

    public static void main(String[] args) {
        List<String> wordList1 = Arrays.asList("hot", "dot", "dog", 
            "lot", "log", "cog");
        System.out.println(ladderLength("hit", "cog", wordList1)); // 5
        
        List<String> wordList2 = Arrays.asList("hot", "dot", "dog", 
            "lot", "log");
        System.out.println(ladderLength("hit", "cog", wordList2)); // 0
    }
}
```

**Time:** O(M² × N) where M = word length, N = word list size | **Space:** O(M × N)

---

### Problem 4: Coin Change (Hard Variant)
**Problem:** Given coins and amount, return number of ways to make change.

**Approach:** Bottom-up DP — dp[i] = number of ways to make amount i.

```java
public class CoinChangeWays {

    // APPROACH: Bottom-up DP
    // dp[i] = sum of dp[i - coin] for each coin
    // Order of coins doesn't matter (combination, not permutation)
    
    public static int change(int amount, int[] coins) {
        int[] dp = new int[amount + 1];
        dp[0] = 1; // One way to make amount 0: use no coins
        
        // Iterate coins first to avoid counting permutations
        for (int coin : coins) {
            for (int i = coin; i <= amount; i++) {
                dp[i] += dp[i - coin];
            }
        }
        
        return dp[amount];
    }

    // VARIANT: Return all combinations
    public static List<List<Integer>> changeCombinations(int amount, int[] coins) {
        List<List<Integer>> result = new ArrayList<>();
        Arrays.sort(coins);
        backtrack(coins, amount, 0, new ArrayList<>(), result);
        return result;
    }
    
    private static void backtrack(int[] coins, int remaining, int start,
                                   List<Integer> path, List<List<Integer>> result) {
        if (remaining == 0) {
            result.add(new ArrayList<>(path));
            return;
        }
        
        for (int i = start; i < coins.length; i++) {
            if (coins[i] > remaining) break;
            path.add(coins[i]);
            backtrack(coins, remaining - coins[i], i, path, result);
            path.remove(path.size() - 1);
        }
    }

    public static void main(String[] args) {
        int[] coins1 = {1, 5, 10, 25};
        System.out.println(change(30, coins1)); // 18 ways
        
        int[] coins2 = {2};
        System.out.println(change(3, coins2)); // 0 ways
        
        System.out.println(changeCombinations(5, new int[]{1, 2, 5}));
        // [[1,1,1,1,1], [1,1,1,2], [1,2,2], [5]]
    }
}
```

**Time:** O(amount × coins) | **Space:** O(amount)

---

### Problem 5: Merge K Sorted Lists
**Problem:** Merge k sorted linked lists into one sorted list.

**Approach:** Min-heap of size k — always pick the smallest head from all lists.

```java
import java.util.*;

public class MergeKSortedLists {

    static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    // APPROACH: Min-Heap (PriorityQueue)
    // Add head of each list to heap
    // Always extract min, add its next to heap
    // O(N log k) where N = total nodes, k = number of lists
    
    public static ListNode mergeKLists(ListNode[] lists) {
        PriorityQueue<ListNode> pq = new PriorityQueue<>(
            (a, b) -> a.val - b.val
        );
        
        // Add head of each non-empty list
        for (ListNode list : lists) {
            if (list != null) pq.offer(list);
        }
        
        ListNode dummy = new ListNode(0);
        ListNode current = dummy;
        
        while (!pq.isEmpty()) {
            ListNode min = pq.poll();
            current.next = min;
            current = current.next;
            
            if (min.next != null) {
                pq.offer(min.next);
            }
        }
        
        return dummy.next;
    }

    public static void main(String[] args) {
        ListNode l1 = new ListNode(1);
        l1.next = new ListNode(4);
        l1.next.next = new ListNode(5);
        
        ListNode l2 = new ListNode(1);
        l2.next = new ListNode(3);
        l2.next.next = new ListNode(4);
        
        ListNode l3 = new ListNode(2);
        l3.next = new ListNode(6);
        
        ListNode[] lists = {l1, l2, l3};
        ListNode merged = mergeKLists(lists);
        
        while (merged != null) {
            System.out.print(merged.val + " -> ");
            merged = merged.next;
        }
        // 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6
    }
}
```

**Time:** O(N log k) | **Space:** O(k)

---

## 6. Preparation Strategy

### Focus Areas (5-Week Plan — ByteDance needs extra prep)

#### Week 1: Array Hard Problems
- [ ] Sliding window maximum (10 problems)
- [ ] Two pointer advanced (10 problems)
- [ ] Prefix sum variations (5 problems)
- [ ] Practice: 20 problems (Medium + Hard)

#### Week 2: String Hard Problems
- [ ] Pattern matching (KMP, Rabin-Karp)
- [ ] Substring problems (10 problems)
- [ ] String DP (10 problems)
- [ ] Practice: 20 problems

#### Week 3: Dynamic Programming
- [ ] 1D DP hard variants (10 problems)
- [ ] 2D DP problems (10 problems)
- [ ] Knapsack and subset sum (5 problems)
- [ ] Interval DP (5 problems)
- [ ] Practice: 20 problems

#### Week 4: Graphs and Backtracking
- [ ] BFS/DFS on graphs (10 problems)
- [ ] Topological sort (5 problems)
- [ ] Shortest path (5 problems)
- [ ] Backtracking (10 problems)
- [ ] Practice: 20 problems

#### Week 5: Optimization and Mocks
- [ ] Hard problems from LeetCode
- [ ] Mock interviews (5+ sessions)
- [ ] Time yourself — aim for 20 min per Medium, 30 min per Hard
- [ ] Review and consolidate

### ByteDance-Specific Tips
1. **Practice Hard problems** — ByteDance is known for difficulty
2. **Optimize everything** — Don't settle for the first working solution
3. **Handle edge cases** — Empty inputs, single elements, large inputs
4. **Code fast** — They time your implementation speed
5. **Know time/space complexity** — Be ready to prove it
6. **Practice optimization** — "Can you do better?" is a common follow-up
7. **Be creative** — Standard approaches may not be optimal enough
8. **Study hard problems** — LeetCode Hard problems are their baseline

### Common Follow-up Questions
- "Can you optimize the time complexity?"
- "Can you do it in O(1) space?"
- "What if the input is 10^9 elements?"
- "Can you handle concurrent access?"
- "What's the best theoretical complexity?"

### Resources
- LeetCode Hard problems (focus on top 100)
- ByteDance tagged problems on LeetCode
- Algorithm competition problems (Codeforces, AtCoder)
- "Algorithm Design Manual" for optimization techniques

---

> **Remember:** ByteDance values speed and optimization above all else. They expect you to not just solve the problem, but solve it in the most efficient way possible. Practice Hard problems and always think about optimization.
