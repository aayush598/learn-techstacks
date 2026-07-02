# 30-Day DSA Pattern Challenge

## Overview
A structured 30-day plan to master DSA patterns. Each day covers one pattern with 3-5 problems of increasing difficulty. Spend 2-3 hours daily: 30 min learning the pattern, 90 min solving, 30 min reviewing.

---

## Week 1: Array Patterns (Days 1-5)

### Day 1: Prefix Sum
**Pattern:** Precompute cumulative sums to answer range sum queries in O(1).

**Key problems:**
1. **Range Sum Query - Immutable** — Build prefix sum array, query sum[left..right] = prefix[right+1] - prefix[left]
2. **Subarray Sum Equals K** — Use HashMap of prefix sum → count; O(n) time
3. **Continuous Subarray Sum** — Prefix sum modulo k; if same mod seen, subarray sum is multiple of k
4. **Product of Array Except Self** — Left products + right products arrays; O(n) time, O(1) space
5. **Minimum Value to Get Positive Step by Step Sum** — Find min prefix sum, answer = 1 - minPrefix

**Java Template:**
```java
class PrefixSum {
    int[] prefix;
    public PrefixSum(int[] nums) {
        prefix = new int[nums.length + 1];
        for (int i = 0; i < nums.length; i++)
            prefix[i+1] = prefix[i] + nums[i];
    }
    public int rangeSum(int left, int right) {
        return prefix[right+1] - prefix[left];
    }
}
```

### Day 2: Kadane's Algorithm
**Pattern:** Maximum subarray sum. Track current sum, reset if negative.

**Key problems:**
1. **Maximum Subarray** — Classic Kadane; O(n)
2. **Maximum Sum Circular Subarray** — Max subarray OR total - min subarray
3. **Maximum Product Subarray** — Track both max and min (negative × negative = positive)
4. **Maximum Absolute Sum of Any Subarray** — Kadane for positive + Kadane for negative
5. **Largest Sum of Contiguous Subarray with At Most K** — Sliding window + Kadane

**Template:**
```java
public int maxSubArray(int[] nums) {
    int maxEndingHere = nums[0], maxSoFar = nums[0];
    for (int i = 1; i < nums.length; i++) {
        maxEndingHere = Math.max(nums[i], maxEndingHere + nums[i]);
        maxSoFar = Math.max(maxSoFar, maxEndingHere);
    }
    return maxSoFar;
}
```

### Day 3: Two Pointers
**Pattern:** Two pointers moving toward each other or in same direction.

**Key problems:**
1. **Two Sum II (Sorted)** — Opposite ends, adjust based on sum vs target
2. **3Sum** — Fix i, two pointers for remaining; skip duplicates
3. **Container With Most Water** — Move shorter line inward
4. **Trapping Rain Water** — Two pointers with leftMax/rightMax
5. **Remove Duplicates from Sorted Array** — Slow/fast pointers

### Day 4: Sliding Window
**Pattern:** Expand window, contract when needed, track optimal window.

**Key problems:**
1. **Maximum Average Subarray I** — Fixed size k window
2. **Longest Substring Without Repeating Characters** — Variable window with freq array
3. **Minimum Window Substring** — Expand to satisfy, contract to minimize
4. **Max Consecutive Ones III** — Flip at most k zeroes → window with zero count
5. **Sliding Window Maximum** — Deque (monotonic queue) for O(n)

### Day 5: Dutch Flag / Partitioning
**Pattern:** Partition array into 2 or 3 categories.

**Key problems:**
1. **Sort Colors** — Three pointers (0s, 1s, 2s)
2. **Move Zeroes** — Two pointers, swap non-zero to front
3. **Partition Labels** — Last index map, greedy partition
4. **Sort Array by Parity** — Even numbers first
5. **Segregate 0s and 1s** — Two pointers

---

## Week 2: String & LinkedList Patterns (Days 6-10)

### Day 6: KMP & String Matching
**Pattern:** Pattern matching in O(n+m) using LPS array.

**Key problems:**
1. **Implement strStr() / Find the Index of the First Occurrence** — KMP
2. **Shortest Palindrome** — KMP on s + '#' + reverse(s)
3. **Repeated Substring Pattern** — KMP LPS analysis
4. **Longest Happy Prefix** — KMP LPS table
5. **String Matching in an Array** — Substring check with KMP

### Day 7: Palindrome Problems
**Pattern:** Two pointers expand from center, or DP for palindromic substrings.

**Key problems:**
1. **Valid Palindrome** — Two pointers, skip non-alphanumeric
2. **Longest Palindromic Substring** — Expand around center O(n²) or Manacher O(n)
3. **Palindromic Substrings** — Count all palindromic substrings
4. **Longest Palindromic Subsequence** — DP: LCS(s, rev(s))
5. **Palindrome Partitioning** — Backtracking + DP for palindrome check

### Day 8: Anagram Problems
**Pattern:** Character frequency counting, sliding window for substring anagrams.

**Key problems:**
1. **Valid Anagram** — Frequency array of size 26
2. **Find All Anagrams in a String** — Sliding window + freq array
3. **Group Anagrams** — HashMap with sorted char string as key
4. **Minimum Number of Steps to Make Two Strings Anagram** — Count differences
5. **Find Resultant Array After Removing Anagrams** — Compare adjacent

### Day 9: Linked List Reversal & Manipulation
**Pattern:** In-place reversal, slow/fast pointers.

**Key problems:**
1. **Reverse Linked List** — Iterative (prev, curr, next) or recursive
2. **Reverse Linked List II** — Reverse between positions
3. **Reverse Nodes in k-Group** — Recursively reverse k at a time
4. **Palindrome Linked List** — Find middle, reverse second half, compare
5. **Reorder List** — Middle + reverse + merge

### Day 10: Linked List Cycle & Merge
**Pattern:** Floyd's cycle detection, merging sorted lists.

**Key problems:**
1. **Linked List Cycle** — Fast & slow pointers
2. **Detect Cycle Start** — Floyd's cycle detection phase 2
3. **Intersection of Two Linked Lists** — Two pointers, reset when null
4. **Merge Two Sorted Lists** — Dummy node, compare
5. **Merge K Sorted Lists** — PriorityQueue (K-way merge)

---

## Week 3: Stack, Queue, Heap, hashing (Days 11-14)

### Day 11: Stack Patterns
**Pattern:** LIFO for matching, monotonic stack for next greater/smaller.

**Key problems:**
1. **Valid Parentheses** — Stack for matching
2. **Min Stack** — Two stacks or single stack with pairs
3. **Next Greater Element** — Monotonic decreasing stack
4. **Largest Rectangle in Histogram** — Monotonic increasing stack
5. **Daily Temperatures** — Monotonic stack, store indices

### Day 12: Queue & Monotonic Queue
**Pattern:** Queue for BFS, Deque for sliding window min/max.

**Key problems:**
1. **Sliding Window Maximum** — Deque with indices
2. **Implement Stack Using Queues** — Two queues or single queue
3. **Design Circular Queue** — Array with front/back pointers
4. **Task Scheduler** — Max heap + queue for cooldown
5. **Longest Continuous Subarray With Absolute Diff ≤ Limit** — Two deques (min + max)

### Day 13: Hashing Patterns
**Pattern:** HashMap for O(1) lookup, frequency counting.

**Key problems:**
1. **Two Sum** — HashMap of value → index
2. **Longest Consecutive Sequence** — HashSet, check previous existence
3. **Subarray Sum Equals K** — Prefix sum HashMap
4. **Minimum Window Substring** — HashMap for character counts
5. **Encode and Decode TinyURL** — HashMap for long↔short

### Day 14: Advanced Hashing & Design
**Pattern:** Custom hashing, object as key, multi-map.

**Key problems:**
1. **Group Anagrams** — Sorted string as key
2. **Find Duplicate Subtrees** — Serialize subtree as key
3. **Contains Duplicate II** — HashMap of value → last index
4. **Top K Frequent Elements** — HashMap + bucket sort or heap
5. **Design HashMap** — Array of LinkedList for collision

---

## Week 4: Trees & Heaps (Days 15-18)

### Day 15: Tree DFS (Pre/In/Post-order)
**Pattern:** Recursive tree traversal.

**Key problems:**
1. **Binary Tree Inorder Traversal** — Recursive + iterative
2. **Maximum Depth of Binary Tree** — Post-order (height)
3. **Validate Binary Search Tree** — Inorder or min/max range
4. **Path Sum** — Pre-order with target subtraction
5. **Lowest Common Ancestor** — Post-order, check both sides

### Day 16: Tree BFS & Views
**Pattern:** Level order traversal using queue.

**Key problems:**
1. **Binary Tree Level Order Traversal** — BFS with level size
2. **Right Side View** — Last node on each level
3. **Average of Levels in Binary Tree** — Level sum / count
4. **Binary Tree Zigzag Level Order** — Toggle add order
5. **Populating Next Right Pointers** — Level order or constant space

### Day 17: Heap Patterns
**Pattern:** Top K, K-way merge, median finding.

**Key problems:**
1. **Top K Frequent Elements** — Min-heap of size k
2. **Kth Largest Element in an Array** — QuickSelect or min-heap of size k
3. **Find Median from Data Stream** — Two heaps (max + min)
4. **K Closest Points to Origin** — Max-heap of size k
5. **Merge K Sorted Lists** — Min-heap for K-way merge

### Day 18: Two Heaps / Sliding Window Median
**Pattern:** Balancing two heaps for order statistics.

**Key problems:**
1. **Find Median from Data Stream** — Classic two heaps
2. **Sliding Window Median** — Two heaps + lazy deletion
3. **IPO** — Capital + profit, two heaps for available projects
4. **Schedule Tasks** — Max heap + queue for idle
5. **Minimum Cost to Hire K Workers** — Sort by ratio, max heap for quality

---

## Week 5: Graph & Backtracking (Days 19-22)

### Day 19: Graph BFS & Shortest Path
**Pattern:** BFS for unweighted shortest path, level order traversal.

**Key problems:**
1. **Number of Islands** — BFS on grid
2. **Shortest Path in Binary Matrix** — BFS with 8 directions
3. **Word Ladder** — BFS with word transformation
4. **01 Matrix** — BFS from all zeroes
5. **Rotten Oranges** — Multi-source BFS

### Day 20: Graph DFS & Topological Sort
**Pattern:** DFS for connectivity, Kahn's algorithm for topo.

**Key problems:**
1. **Number of Provinces** — DFS on adjacency matrix
2. **Course Schedule I (Cycle Detection)** — DFS with state[3]
3. **Course Schedule II (Topological Order)** — Kahn's algorithm
4. **Alien Dictionary** — Compare adjacent words, build graph
5. **Clone Graph** — DFS with HashMap

### Day 21: Backtracking (Permutations & Subsets)
**Pattern:** Explore all possibilities, backtrack on dead end.

**Key problems:**
1. **Permutations** — Used array or swapping
2. **Subsets** — Include/exclude pattern
3. **Combination Sum** — Can reuse elements
4. **Generate Parentheses** — Track open/close count
5. **Letter Combinations of a Phone Number** — Recursion on digits

### Day 22: Backtracking (Constraint Satisfaction)
**Pattern:** Constraint checking before placement.

**Key problems:**
1. **N-Queens** — Check column and diagonals
2. **Sudoku Solver** — Row, col, box validation
3. **Word Search** — DFS on grid with visited
4. **Palindrome Partitioning** — Check palindrome before recursion
5. **Restore IP Addresses** — Valid segment check

---

## Week 6: DP Patterns (Days 23-27)

### Day 23: Knapsack DP (0/1 & Unbounded)
**Pattern:** Choosing items with capacity constraint.

**Key problems:**
1. **0/1 Knapsack** — dp[w] = max value
2. **Subset Sum** — dp[w] = can achieve
3. **Partition Equal Subset Sum** — target = sum/2
4. **Coin Change (Min Coins)** — Unbounded, minimize count
5. **Coin Change II (Combinations)** — Unbounded, count ways

### Day 24: Longest Common Subsequence (LCS)
**Pattern:** Two-sequence comparison.

**Key problems:**
1. **Longest Common Subsequence** — Classic DP
2. **Longest Common Substring** — Track max with diagonal reset
3. **Edit Distance** — Insert/delete/replace
4. **Shortest Common Supersequence** — m + n - LCS
5. **Longest Palindromic Subsequence** — LCS(s, rev(s))

### Day 25: Longest Increasing Subsequence (LIS)
**Pattern:** Find longest sequence where elements increase.

**Key problems:**
1. **Longest Increasing Subsequence** — O(n log n) using tails array
2. **Russian Doll Envelopes** — Sort + LIS on heights
3. **Maximum Length of Pair Chain** — Sort by second, greedy or LIS
4. **Longest Bitonic Subsequence** — LIS from left + LIS from right
5. **Number of LIS** — DP with count tracking

### Day 26: Interval DP
**Pattern:** Solving for all intervals [i,j].

**Key problems:**
1. **Matrix Chain Multiplication** — Classic interval DP
2. **Burst Balloons** — Burst last, add 1 at ends
3. **Longest Palindromic Substring** — DP for palindrome checking
4. **Palindrome Partitioning II** — Min cuts for palindrome partitioning
5. **Minimum Cost to Cut a Stick** — Sort cuts, add ends

### Day 27: Grid DP
**Pattern:** Robot moving right/down in grid.

**Key problems:**
1. **Unique Paths** — Count ways
2. **Unique Paths with Obstacles** — Set dp=0 at obstacles
3. **Minimum Path Sum** — Min sum path
4. **Triangle (Min Path Sum to Bottom)** — Bottom-up DP
5. **Dungeon Game** — Work backwards from princess

---

## Week 7: Greedy, Bit Manip, Review (Days 28-30)

### Day 28: Greedy Patterns
**Pattern:** Local optimal → global optimal.

**Key problems:**
1. **Activity Selection / N Meetings in One Room** — Sort by end time
2. **Jump Game** — Track furthest reachable
3. **Jump Game II** — Jump to maximize reach
4. **Non-overlapping Intervals** — Sort by end, count overlapping
5. **Gas Station** — If total gas ≥ total cost, find start

### Day 29: Bit Manipulation
**Pattern:** XOR, bit counting, bit masking.

**Key problems:**
1. **Single Number** — XOR all elements
2. **Number of 1 Bits** — n & (n-1) trick
3. **Counting Bits** — DP: count[i] = count[i >> 1] + (i & 1)
4. **Reverse Bits** — Bit by bit construction
5. **Power of Two** — n > 0 && (n & (n-1)) == 0

### Day 30: Mixed Review
Solve problems that combine multiple patterns:

1. **Serialize and Deserialize Binary Tree** — BFS/DFS + string manipulation
2. **LRU Cache** — HashMap + DoublyLinkedList (OOP + data structures)
3. **Merge Intervals** — Sorting + interval merging
4. **Meeting Rooms II** — Interval + heap
5. **Top K Frequent Words** — HashMap + heap + sorting

**Final review checklist:**
- [ ] Can I identify sliding window vs two pointers vs prefix sum?
- [ ] Can I write BFS and DFS on trees and graphs from memory?
- [ ] Can I implement all 5 backtracking templates?
- [ ] Can I map problems to the correct DP pattern?
- [ ] Can I apply binary search on answer for optimization?
- [ ] Can I identify which data structure fits each problem?

---

## Quick Reference: Day → Pattern → Key Technique

| Day | Pattern | Key Technique | Example Problem |
|-----|---------|---------------|-----------------|
| 1 | Prefix Sum | Precompute sums | Subarray Sum = K |
| 2 | Kadane | Track current max | Max Subarray Sum |
| 3 | Two Pointers | Opposite/same direction | 3Sum |
| 4 | Sliding Window | Expand/contract | Longest Substr w/o Repeat |
| 5 | Partitioning | 3-way partition | Sort Colors |
| 6 | KMP | LPS array | strStr() |
| 7 | Palindrome | Center expansion | Longest Palindromic Substr |
| 8 | Anagram | Freq array | Group Anagrams |
| 9 | LL Reversal | prev/curr/next | Reverse List |
| 10 | LL Cycle | Floyd's algorithm | Detect Cycle |
| 11 | Stack | Monotonic stack | Next Greater Element |
| 12 | Queue/Deque | Deque for window max | Sliding Window Max |
| 13 | Hashing | HashMap O(1) lookup | Two Sum |
| 14 | Advanced Hash | Object as key | Group Anagrams |
| 15 | Tree DFS | Recursive traversal | Validate BST |
| 16 | Tree BFS | Level order | Right Side View |
| 17 | Heap | Top K / K-way merge | Top K Frequent |
| 18 | Two Heaps | Balance heaps | Median from Stream |
| 19 | Graph BFS | Level order / shortest | Word Ladder |
| 20 | Graph DFS | Topo sort / SCC | Course Schedule |
| 21 | Backtracking I | Subsets/Perms | Combinations |
| 22 | Backtracking II | CSP | N-Queens |
| 23 | Knapsack DP | 0/1 + unbounded | Subset Sum |
| 24 | LCS | 2-sequence DP | Edit Distance |
| 25 | LIS | Patience sorting | Russian Doll |
| 26 | Interval DP | Range [i,j] | MCM |
| 27 | Grid DP | Robot path | Min Path Sum |
| 28 | Greedy | Local optimal | Activity Selection |
| 29 | Bit Manipulation | XOR, bit count | Single Number |
| 30 | Mixed Review | Combine patterns | LRU Cache |
