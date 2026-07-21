# 40-Day Study Plan — Infosys SP/DSE Preparation (Python)

## Overview

| Detail | Info |
|--------|------|
| **Duration** | 40 Days |
| **Daily Commitment** | 4–6 hours |
| **Language** | Python 3 |
| **Target** | SP L2/L3 (₹16–21 LPA) |
| **Primary Resource** | LeetCode |
| **Supplementary** | NeetCode 150, Striver's SDE Sheet |

---

## Weekly Breakdown

```
Week 1-2 (Day 1-14):   Arrays, Strings, Hashing         → EASY LEVEL
Week 3-4 (Day 15-28):  Linked Lists, Stacks, Trees, BST  → MEDIUM LEVEL
Week 5   (Day 29-35):  Sorting, Searching, Greedy, Recursion → MEDIUM LEVEL
Week 6-7 (Day 36-49):  Dynamic Programming 1D & 2D       → HARD LEVEL
Week 8   (Day 42-49):  DP on Trees, Graphs, Bitmask DP   → HARD + COMPLEX
```

> Adjust as needed — the key is covering all topics, not hitting exact day numbers.

---

## Week 1–2: Arrays, Strings, Hashing (Easy Level)

### Day 1: Array Basics & Two Pointer

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Two Sum | LC 1 | HashMap lookup |
| 2 | Best Time to Buy and Sell Stock | LC 121 | Single pass tracking |
| 3 | Contains Duplicate | LC 217 | HashSet |
| 4 | Max Subarray | LC 53 | Kadane's algorithm |
| 5 | Merge Sorted Array | LC 88 | Two pointer from end |

**Day Target:** Solve all 5. Time yourself — aim for <20 min per Easy problem.

### Day 2: Arrays — Prefix Sum & Sliding Window

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Running Sum of 1d Array | LC 1480 | Prefix sum |
| 2 | Subarray Sum Equals K | LC 560 | Prefix sum + HashMap |
| 3 | Maximum Average Subarray I | LC 643 | Sliding window |
| 4 | Minimum Size Subarray Sum | LC 209 | Variable window |
| 5 | Longest Substring Without Repeating | LC 3 | Sliding window + HashMap |

**Day Target:** Master sliding window pattern — it appears in 30%+ of Array problems.

### Day 3: Strings — Basics & Manipulation

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Valid Anagram | LC 242 | Frequency count |
| 2 | Valid Palindrome | LC 125 | Two pointer |
| 3 | Reverse String | LC 344 | Two pointer swap |
| 4 | First Unique Character | LC 387 | HashMap count |
| 5 | Ransom Note | LC 383 | Character frequency |

### Day 4: Strings — Advanced Patterns

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Longest Palindromic Substring | LC 5 | Expand around center |
| 2 | String to Integer (atoi) | LC 8 | Edge case handling |
| 3 | Group Anagrams | LC 49 | Sorted string as key |
| 4 | Valid Parentheses | LC 20 | Stack-based string |
| 5 | Minimum Window Substring | LC 76 | Sliding window hard |

### Day 5: Hashing — Fundamentals

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Intersection of Two Arrays | LC 349 | HashSet |
| 2 | Happy Number | LC 202 | HashSet cycle detection |
| 3 | Single Number | LC 136 | XOR / HashMap |
| 4 | Two Sum II | LC 167 | Sorted array + two pointer |
| 5 | Subarray Sum Equals K | LC 560 | Prefix sum + HashMap |

### Day 6: Arrays — Harder Easy Problems

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Product of Array Except Self | LC 238 | Prefix/suffix product |
| 2 | Maximum Product Subarray | LC 152 | Kadane's variant |
| 3 | 3Sum | LC 15 | Two pointer + sorting |
| 4 | Container With Most Water | LC 11 | Two pointer |
| 5 | Move Zeroes | LC 283 | Two pointer |

### Day 7: Week 1 Revision + Mock Test

```
Morning (2 hours):
- Revise all problems solved this week
- Write down patterns in a notebook/Notion
- Focus on patterns you found difficult

Afternoon (2 hours):
- Take 1 Easy mock test (3 problems, 90 minutes)
- Time yourself strictly
- Review mistakes

Evening (1 hour):
- Re-solve any problems you couldn't solve in time
- Update pattern notes
```

### Day 8-9: Hashing — Advanced

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Longest Consecutive Sequence | LC 128 | HashSet O(n) |
| 2 | Top K Frequent Elements | LC 347 | HashMap + bucket sort |
| 3 | Sort Characters By Frequency | LC 451 | HashMap + sorting |
| 4 | Find All Anagrams in a String | LC 438 | Sliding window + HashMap |
| 5 | Minimum Window Substring | LC 76 | Sliding window |
| 6 | Subarray Product Less Than K | LC 713 | Sliding window |
| 7 | Continuous Subarray Sum | LC 523 | Prefix sum + HashMap |
| 8 | Find Duplicate Number | LC 287 | Floyd's cycle |

### Day 10: Arrays — Contest-Style Problems

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Rotate Array | LC 189 | Reversal algorithm |
| 2 | Spiral Matrix | LC 54 | Boundary simulation |
| 3 | Set Matrix Zeroes | LC 73 | In-place marking |
| 4 | Next Permutation | LC 31 | Pattern recognition |
| 5 | Sort Colors | LC 75 | Dutch national flag |

### Day 11-14: Mixed Easy Practice

- Solve 3-4 Easy problems daily from mixed topics
- Focus on speed — under 15 min per problem
- Start doing virtual contests (LeetCode Weekly/Biweekly)

**Suggested Problems:**

| Day | Problems | Focus |
|-----|----------|-------|
| Day 11 | LC 26, 27, 80, 169 | Array manipulation |
| Day 12 | LC 346, 622, 876, 141 | Linked list intro |
| Day 13 | LC 206, 21, 141, 160 | Linked list patterns |
| Day 14 | REVISION DAY — Redo all Week 1-2 problems you found hard |

---

## Week 3–4: Linked Lists, Stacks, Queues, Trees, BST (Medium Level)

### Day 15: Linked List — Reversal & Traversal

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Reverse Linked List | LC 206 | Iterative reversal |
| 2 | Reverse Linked List II | LC 92 | Partial reversal |
| 3 | Merge Two Sorted Lists | LC 21 | Dummy node technique |
| 4 | Add Two Numbers | LC 2 | Carry propagation |
| 5 | Remove Nth Node From End | LC 19 | Two pointer gap |

### Day 16: Linked List — Fast & Slow Pointer

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Linked List Cycle | LC 141 | Floyd's detection |
| 2 | Linked List Cycle II | LC 142 | Cycle start detection |
| 3 | Middle of Linked List | LC 876 | Fast/slow pointer |
| 4 | Palindrome Linked List | LC 234 | Reverse + compare |
| 5 | Reorder List | LC 143 | Middle + reverse + merge |

### Day 17: Linked List — Advanced

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | LRU Cache | LC 146 | HashMap + Doubly LL |
| 2 | Copy List with Random Pointer | LC 138 | Interleaving technique |
| 3 | Flatten a Multilevel Doubly Linked List | LC 430 | DFS/Stack |
| 4 | Rotate List | LC 61 | Circular list |
| 5 | Swap Nodes in Pairs | LC 24 | Recursive swap |

### Day 18: Stacks — Fundamentals

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Valid Parentheses | LC 20 | Basic stack |
| 2 | Min Stack | LC 155 | Auxiliary stack |
| 3 | Implement Queue using Stacks | LC 232 | Amortized O(1) |
| 4 | Implement Stack using Queues | LC 225 | Queue simulation |
| 5 | Evaluate Reverse Polish Notation | LC 150 | Stack evaluation |

### Day 19: Stacks — Next Greater Element Patterns

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Next Greater Element I | LC 496 | Monotonic stack |
| 2 | Next Greater Element II | LC 503 | Circular array |
| 3 | Daily Temperatures | LC 739 | Monotonic stack |
| 4 | Largest Rectangle in Histogram | LC 84 | Monotonic stack |
| 5 | Trapping Rain Water | LC 42 | Stack / Two pointer |

### Day 20: Queues & Deque

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Sliding Window Maximum | LC 239 | Monotonic deque |
| 2 | First Unique Character in Queue | — | Deque simulation |
| 3 | Rotting Oranges | LC 994 | BFS with queue |
| 4 | Number of Islands | LC 200 | BFS |
| 5 | Course Schedule | LC 207 | Topological sort |

### Day 21: Week 3 Revision

```
Morning (2 hours):
- Revise Linked List patterns (reversal, fast/slow, dummy node)
- Revise Stack patterns (monotonic stack, evaluation)
- Write pattern cheat sheet

Afternoon (2 hours):
- Medium mock test (3 problems, 120 minutes)
- Pick 1 LL + 1 Stack + 1 mixed

Evening (1 hour):
- Review and re-solve weak problems
```

### Day 22: Binary Trees — Traversals

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Maximum Depth of Binary Tree | LC 104 | DFS |
| 2 | Same Tree | LC 100 | Recursive comparison |
| 3 | Invert Binary Tree | LC 226 | Recursive swap |
| 4 | Binary Tree Inorder Traversal | LC 94 | Inorder + stack |
| 5 | Binary Tree Level Order Traversal | LC 102 | BFS |

### Day 23: Binary Trees — Path Problems

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Path Sum | LC 112 | DFS with sum |
| 2 | Binary Tree Maximum Path Sum | LC 124 | Global max tracking |
| 3 | Diameter of Binary Tree | LC 543 | Height calculation |
| 4 | Lowest Common Ancestor | LC 236 | Recursive LCA |
| 5 | Serialize and Deserialize Binary Tree | LC 297 | BFS/DFS encoding |

### Day 24: BST — Basics

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Validate BST | LC 98 | Range check |
| 2 | Search in BST | LC 700 | Binary search |
| 3 | Insert into BST | LC 701 | Recursive insert |
| 4 | Kth Smallest Element in BST | LC 230 | Inorder traversal |
| 5 | Convert Sorted Array to BST | LC 108 | Recursive build |

### Day 25: BST — Advanced

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Lowest Common Ancestor of BST | LC 235 | BST property |
| 2 | Binary Search Tree Iterator | LC 173 | Stack simulation |
| 3 | Kth Largest Element in BST | LC 230 | Reverse inorder |
| 4 | Recover BST | LC 99 | Two swapped nodes |
| 5 | Trim a BST | LC 669 | Recursive trim |

### Day 26: Trees — Mixed Practice

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Construct Binary Tree from Preorder and Inorder | LC 105 | Recursive build |
| 2 | Populating Next Right Pointers | LC 116 | Level order |
| 3 | Binary Tree Right Side View | LC 199 | BFS/DFS |
| 4 | Count Good Nodes in Binary Tree | LC 1448 | DFS with max |
| 5 | Vertical Order Traversal | LC 987 | BFS + sorting |

### Day 27: Medium Difficulty Mixed

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Longest Palindromic Substring | LC 5 | Expand around center |
| 2 | Coin Change | LC 322 | 1D DP intro |
| 3 | Clone Graph | LC 133 | DFS/BFS + HashMap |
| 4 | Number of Provinces | LC 547 | Union-Find |
| 5 | Word Search | LC 79 | Backtracking |

### Day 28: Week 4 Revision

```
Full Revision Day:
- Go through ALL problems from Week 3-4
- Time yourself on 3 random Medium problems
- Identify weak patterns
- Update pattern cheat sheet
- REST in the evening (important for Week 5)
```

---

## Week 5: Sorting, Searching, Greedy, Recursion (Medium Level)

### Day 29: Binary Search

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Binary Search | LC 704 | Standard template |
| 2 | Search Insert Position | LC 35 | Lower bound |
| 3 | Find Minimum in Rotated Sorted Array | LC 153 | Modified binary search |
| 4 | Search in Rotated Sorted Array | LC 33 | Two-phase binary search |
| 5 | Find Peak Element | LC 162 | Binary search on answer |

### Day 30: Binary Search — Advanced

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Koko Eating Bananas | LC 875 | Binary search on answer |
| 2 | Magnetic Force Between Two Balls | LC 1552 | Binary search on answer |
| 3 | Median of Two Sorted Arrays | LC 4 | Hard binary search |
| 4 | Find First and Last Position | LC 34 | Leftmost + rightmost |
| 5 | Time Based Key-Value Store | LC 981 | Binary search on values |

### Day 31: Sorting Algorithms (Implementation + Problems)

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Merge Sort implementation | — | Divide & conquer |
| 2 | Quick Sort implementation | — | Partition |
| 3 | Merge Intervals | LC 56 | Sort + merge |
| 4 | Non-overlapping Intervals | LC 435 | Greedy + sort |
| 5 | Meeting Rooms II | LC 253 | Sort + heap |

### Day 32: Greedy — Fundamentals

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Maximum Subarray | LC 53 | Greedy Kadane's |
| 2 | Jump Game | LC 55 | Greedy reach |
| 3 | Jump Game II | LC 45 | Greedy BFS |
| 4 | Gas Station | LC 134 | Greedy tracking |
| 5 | Hand of Straights | LC 846 | Greedy + map |

### Day 33: Greedy — Advanced

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Task Scheduler | LC 621 | Greedy + count |
| 2 | Partition Labels | LC 763 | Greedy + last occurrence |
| 3 | Minimum Number of Arrows | LC 452 | Interval scheduling |
| 4 | Valid Triangle Number | LC 611 | Sort + binary search |
| 5 | Queue Reconstruction by Height | LC 406 | Greedy insert |

### Day 34: Recursion — Fundamentals

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Power of Two | LC 231 | Simple recursion |
| 2 | Fibonacci Number | LC 509 | Recursion + memo |
| 3 | Subsets | LC 78 | Include/exclude |
| 4 | Subsets II | LC 90 | Subsets with duplicates |
| 5 | Permutations | LC 46 | Backtracking |

### Day 35: Backtracking

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Permutations II | LC 47 | Backtracking + pruning |
| 2 | Combination Sum | LC 39 | Backtracking + reuse |
| 3 | Combination Sum II | LC 40 | Backtracking no reuse |
| 4 | Letter Combinations of Phone | LC 17 | Backtracking |
| 5 | Word Search | LC 79 | Grid backtracking |
| 6 | N-Queens | LC 51 | Classic backtracking |

---

## Week 6–7: Dynamic Programming (Hard Level)

### Day 36: DP — 1D Basics

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Climbing Stairs | LC 70 | Fibonacci pattern |
| 2 | Min Cost Climbing Stairs | LC 746 | 1D DP |
| 3 | House Robber | LC 198 | 1D DP |
| 4 | House Robber II | LC 213 | Circular DP |
| 5 | Longest Increasing Subsequence | LC 300 | LIS pattern |

### Day 37: DP — 1D Advanced

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Word Break | LC 139 | DP + dictionary |
| 2 | Coin Change | LC 322 | Unbounded knapsack |
| 3 | Maximum Product Subarray | LC 152 | Track min and max |
| 4 | Decode Ways | LC 91 | 1D DP |
| 5 | Partition Equal Subset Sum | LC 416 | 0/1 Knapsack |

### Day 38: DP — 2D Basics

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Unique Paths | LC 62 | 2D grid DP |
| 2 | Minimum Path Sum | LC 64 | 2D grid DP |
| 3 | Unique Paths II | LC 63 | Grid with obstacles |
| 4 | Longest Common Subsequence | LC 1143 | Classic LCS |
| 5 | Edit Distance | LC 72 | Classic DP |

### Day 39: DP — 2D Advanced

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Longest Palindromic Subsequence | LC 516 | LCS variant |
| 2 | Target Sum | LC 494 | 2D DP |
| 3 | Interleaving String | LC 97 | 2D DP |
| 4 | Distinct Subsequences | LC 115 | 2D DP |
| 5 | Burst Balloons | LC 312 | Interval DP |

### Day 40: DP — Knapsack Variants

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | 0/1 Knapsack (template) | — | Classic knapsack |
| 2 | Subset Sum | LC 416 | Knapsack variant |
| 3 | Combination Sum IV | LC 377 | Unbounded knapsack |
| 4 | Ones and Zeroes | LC 474 | Multi-dimensional knapsack |
| 5 | Last Stone Weight II | LC 1049 | Knapsack |

### Day 41: DP on Strings

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Longest Common Substring | — | LCS variant |
| 2 | Shortest Common Supersequence | LC 1092 | LCS + reconstruction |
| 3 | Distinct Subsequences | LC 115 | 2D string DP |
| 4 | Is Subsequence | LC 392 | Two pointer / DP |
| 5 | Minimum ASCII Delete Sum | LC 712 | LCS variant |

### Day 42: DP — Harder Problems

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Maximal Rectangle | LC 85 | Histogram + DP |
| 2 | Regular Expression Matching | LC 10 | 2D DP |
| 3 | Wildcard Matching | LC 44 | 2D DP |
| 4 | Dungeon Game | LC 174 | Reverse DP |
| 5 | Paint House II | LC 265 | Multi-choice DP |

### Day 43: Week 6 Revision

```
CRITICAL REVISION DAY

Morning (3 hours):
- Revise ALL 1D DP patterns (LIS, Knapsack, House Robber variants)
- Write transition formulas on paper for each

Afternoon (3 hours):
- Revise ALL 2D DP patterns (LCS, Edit Distance, Grid DP)
- Practice writing code from memory for 3 hard DP problems

Evening (2 hours):
- Take a full mock test: 3 problems, 180 minutes
- Include at least 1 Hard DP problem
```

### Day 44-45: Advanced DP Patterns

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Longest Increasing Subsequence (Binary Search O(n log n)) | LC 300 | LIS optimization |
| 2 | Maximum Length of Pair Chain | LC 646 | LIS variant |
| 3 | Russian Doll Envelopes | LC 354 | 2D LIS |
| 4 | Best Time to Buy and Sell Stock with Cooldown | LC 309 | State machine DP |
| 5 | Best Time to Buy and Sell Stock with Transaction Fee | LC 714 | State machine DP |

### Day 46-47: Interval DP & Range DP

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Stone Game | LC 877 | Interval DP |
| 2 | Predict the Winner | LC 486 | Minimax DP |
| 3 | Decode Ways II | LC 639 | 1D DP hard |
| 4 | Unique Binary Search Trees | LC 96 | Catalan number |
| 5 | Minimum Cost Tree From Leaf Values | LC 1130 | Greedy / stack |

### Day 48-49: DP Mixed Hard Practice

Solve 2-3 Hard DP problems daily. Focus on:
- Recognizing which DP pattern applies
- Writing clean transition equations
- Handling base cases correctly
- Space optimization (rolling array)

**Recommended Hard Problems:**

| Problem | LeetCode | Why Important |
|---------|----------|---------------|
| Word Break II | LC 140 | DFS + DP |
| Palindrome Partitioning II | LC 132 | Hard 1D DP |
| Maximal Rectangle | LC 85 | Multi-concept |
| Stone Game III | LC 1406 | Game theory DP |
| Minimum Cost to Cut a Rod | — | Interval DP |

---

## Week 8: DP on Trees, Graphs, Bitmask DP (Hard + Complex)

### Day 50: Graph Basics — BFS & DFS

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Number of Islands | LC 200 | BFS/DFS on grid |
| 2 | Clone Graph | LC 133 | DFS + HashMap |
| 3 | Pacific Atlantic Water Flow | LC 417 | Multi-source BFS |
| 4 | Rotting Oranges | LC 994 | Multi-source BFS |
| 5 | Surrounded Regions | LC 130 | Boundary DFS |

### Day 51: Graph — Topological Sort & DAG

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Course Schedule | LC 207 | Cycle detection |
| 2 | Course Schedule II | LC 210 | Topological sort |
| 3 | Alien Dictionary | LC 269 | Topological sort |
| 4 | Minimum Height Trees | LC 310 | Topological pruning |
| 5 | Sequence Reconstruction | LC 444 | Topological unique |

### Day 52: Graph — Shortest Path & MST

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Network Delay Time | LC 743 | Dijkstra's |
| 2 | Cheapest Flights Within K Stops | LC 787 | Modified Dijkstra |
| 3 | Min Cost to Connect All Points | LC 1584 | Prim's MST |
| 4 | Is Graph Bipartite? | LC 785 | BFS/DFS coloring |
| 5 | Accounts Merge | LC 721 | Union-Find |

### Day 53: Graph — Advanced

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Word Ladder | LC 127 | BFS |
| 2 | Word Ladder II | LC 126 | BFS + DFS |
| 3 | Critical Connections | LC 1192 | Tarjan's bridge |
| 4 | Number of Islands II | LC 305 | Dynamic connectivity |
| 5 | Swim in Rising Water | LC 778 | Binary search + BFS |

### Day 54: DP on Trees

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | House Robber III | LC 337 | Tree DP |
| 2 | Binary Tree Cameras | LC 968 | Tree DP + states |
| 3 | Diameter of Binary Tree | LC 543 | Tree DP |
| 4 | Path Sum III | LC 437 | Prefix sum on tree |
| 5 | Maximum Path Sum | LC 124 | Tree DP |

### Day 55: Bitmask DP

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Single Number | LC 136 | XOR basics |
| 2 | Single Number III | LC 260 | XOR + mask |
| 3 | Bitwise AND of Numbers Range | LC 201 | Bit manipulation |
| 4 | Counting Bits | LC 338 | DP + bits |
| 5 | Minimum XOR Sum of Two Arrays | LC 1879 | Bitmask DP |

### Day 56: Bitmask DP — Advanced

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Shortest Path Visiting All Nodes | LC 847 | Bitmask BFS |
| 2 | Optimal Account Balancing | — | Bitmask subset |
| 3 | Maximum Students Taking Exam | LC 1349 | Bitmask DP |
| 4 | Dota2 Senate | LC 649 | Greedy + simulation |
| 5 | Find the Shortest Superstring | LC 943 | Bitmask DP (TSP) |

### Day 57: Union-Find

| # | Problem | LeetCode | Concept |
|---|---------|----------|---------|
| 1 | Redundant Connection | LC 684 | Basic Union-Find |
| 2 | Number of Provinces | LC 547 | Union-Find |
| 3 | Accounts Merge | LC 721 | Union-Find |
| 4 | Smallest String With Swaps | LC 1202 | Union-Find |
| 5 | Number of Islands II | LC 305 | Dynamic Union-Find |

### Day 58-59: Complex Level Practice

Solve 2-3 Complex-level problems daily:

| Problem | LeetCode | Concept |
|---------|----------|---------|
| Alien Dictionary | LC 269 | Topo sort |
| Word Ladder II | LC 126 | BFS + DFS |
| Minimum Cost to Make Array Equal | LC 2448 | Math + Binary search |
| Find Median from Data Stream | LC 295 | Two heaps |
| Serialize and Deserialize Binary Tree | LC 297 | BFS/DFS |

### Day 60: Final Revision

```
FINAL DAY — FULL MOCK

Morning (3 hours):
- Full mock test (3-4 problems, 180 minutes)
- Simulate exact exam conditions
- No phone, no breaks

Afternoon (2 hours):
- Review all mistakes
- Go through pattern cheat sheet
- Review template code

Evening (1 hour):
- Light revision only
- Prepare exam environment
- Sleep early
```

---

## Mock Test Schedule

| Day | Mock Type | Duration | Problems |
|-----|-----------|----------|----------|
| Day 7 | Easy mock | 90 min | 3 Easy problems |
| Day 14 | Easy + Medium mock | 120 min | 2 Easy + 1 Medium |
| Day 21 | Medium mock | 120 min | 3 Medium problems |
| Day 28 | Medium + Hard mock | 180 min | 1 Medium + 2 Hard |
| Day 35 | Mixed mock | 180 min | 1 Easy + 1 Medium + 1 Hard |
| Day 43 | Full mock | 180 min | All difficulty levels |
| Day 50 | Full mock | 180 min | All difficulty levels |
| Day 55 | Full mock | 180 min | All difficulty levels |
| Day 60 | Final mock | 180 min | Simulate real exam |

---

## Revision Strategy

### Weekly Revision (Every Sunday)

```
1. Go through ALL problems solved that week
2. For each problem, write:
   - Pattern name
   - Time complexity
   - Space complexity
   - Key insight / trick
3. Re-solve any problem that took > 30 min
4. Update pattern cheat sheet
```

### Pattern Cheat Sheet (Maintain Throughout)

```
ARRAYS:
- Two pointer: sorted array pair problems
- Sliding window: subarray/substring problems
- Prefix sum: range queries
- Kadane's: max subarray

STRINGS:
- Sliding window: substring problems
- Two pointer: palindrome, anagram
- HashMap: character frequency

LINKED LISTS:
- Fast/slow: cycle detection, middle
- Dummy node: simplifies edge cases
- Reversal: in-place reversal pattern

STACKS:
- Monotonic stack: next greater/smaller
- Balanced parentheses: matching
- Expression evaluation: RPN

TREES:
- Recursive DFS: most tree problems
- BFS level order: level-based problems
- BST property: left < root < right

GRAPHS:
- BFS: shortest path unweighted
- DFS: connected components
- Topological sort: ordering problems
- Union-Find: dynamic connectivity

DP:
- 1D: LIS, Knapsack, House Robber
- 2D: LCS, Edit Distance, Grid
- State machine: stock problems
- Interval: range-based DP
```

---

## Daily Schedule Template

```
┌──────────────────────────────────────────────┐
│           DAILY STUDY SCHEDULE               │
├──────────────────────────────────────────────┤
│                                              │
│  Morning (2-3 hours):                        │
│  - Solve 3-5 problems from today's topic     │
│  - Focus on understanding, not just solving  │
│                                              │
│  Afternoon (1-2 hours):                      │
│  - Revise yesterday's problems               │
│  - Update pattern notes                      │
│                                              │
│  Evening (1-2 hours):                        │
│  - Solve 1-2 additional problems             │
│  - OR take mock test (on mock days)          │
│                                              │
│  Before bed (15 min):                        │
│  - Quick review of today's patterns          │
│  - Note down what was hard                   │
│                                              │
└──────────────────────────────────────────────┘
```

---

## Resources

| Resource | Link | Purpose |
|----------|------|---------|
| LeetCode | leetcode.com | Primary problem source |
| NeetCode 150 | neetcode.io | Curated problem list |
| Striver's SDE Sheet | takeuforward.org | Structured preparation |
| CP-Algorithms | cp-algorithms.com | Algorithm reference |
| Python Docs | docs.python.org | Language reference |

---

## Final Tips

1. **Consistency > Intensity** — 4 hours daily for 40 days beats 12 hours for 5 days
2. **Pattern recognition is key** — Don't just solve, understand the pattern
3. **Time yourself** — Always track how long each problem takes
4. **Mock tests are non-negotiable** — Take at least 5 full mock tests before exam
5. **Python is slower** — Always aim for optimal complexity, not just "working" code
6. **Partial scoring saves you** — Always submit brute force if optimal isn't ready
7. **Sleep is part of preparation** — 7+ hours sleep improves problem-solving significantly

> **Good luck. Follow this plan, and SP L3 is within reach.**
