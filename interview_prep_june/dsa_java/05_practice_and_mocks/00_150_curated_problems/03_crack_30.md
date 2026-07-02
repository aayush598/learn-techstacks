# Crack 30 — Make-or-Break Interview Problems

> These are the problems that appear in **every** serious interview loop. If you can solve all 30 cold (without looking up solutions), you are interview-ready for DSA at any company.

---

## How to Use This List

1. **Solve one per day** for 30 days (timed, 30-45 min max)
2. **Don't look at solutions** until you've exhausted your own ideas
3. **After solving**: read the official LeetCode solution + top 3 discuss posts
4. **Revise**: re-solve at 1 day, 7 days, 30 days
5. **Group by pattern** — many of these share the same underlying pattern
6. **Company mapping**: these problems cover Google, Meta, Amazon, Microsoft, Apple, Netflix

---

## 1. Two Sum

| Detail | Value |
|---|---|
| **Pattern** | HashMap (complementation) |
| **Difficulty** | Easy |
| **Companies** | Amazon, Google, Meta, Microsoft |
| **LeetCode** | [1](https://leetcode.com/problems/two-sum/) |

**Approach:** Iterate storing `nums[i] → i` in HashMap. For each element, check if `target - nums[i]` exists.

**Why it's a crack problem:** It's the most asked LeetCode problem of all time. Tests HashMap intuition and edge-of-seat thinking.

**Time:** O(n) | **Space:** O(n)

---

## 2. Longest Substring Without Repeating Characters

| Detail | Value |
|---|---|
| **Pattern** | Sliding Window + HashMap |
| **Difficulty** | Medium |
| **Companies** | Amazon, Google, Meta |
| **LeetCode** | [3](https://leetcode.com/problems/longest-substring-without-repeating-characters/) |

**Approach:** Sliding window with HashMap tracking last index of each character. When duplicate found, move left bound past the previous occurrence.

**Why it's a crack problem:** Tests sliding window mastery — the foundation for many string problems.

**Time:** O(n) | **Space:** O(min(m, n))

---

## 3. Median of Two Sorted Arrays

| Detail | Value |
|---|---|
| **Pattern** | Binary Search (partitioning) |
| **Difficulty** | Hard |
| **Companies** | Google, Amazon, Meta |
| **LeetCode** | [4](https://leetcode.com/problems/median-of-two-sorted-arrays/) |

**Approach:** Binary search on smaller array to find correct partition. Ensure `maxLeftA ≤ minRightB && maxLeftB ≤ minRightA`.

**Why it's a crack problem:** Tests deep understanding of binary search and invariants. The O(log(m+n)) requirement forces elegant thinking.

**Time:** O(log(min(n,m))) | **Space:** O(1)

---

## 4. Merge K Sorted Lists

| Detail | Value |
|---|---|
| **Pattern** | MinHeap / Divide & Conquer |
| **Difficulty** | Hard |
| **Companies** | Amazon, Google, Meta, Microsoft |
| **LeetCode** | [23](https://leetcode.com/problems/merge-k-sorted-lists/) |

**Approach:** MinHeap of list heads. Poll smallest, push its next. Repeat until heap empty.

**Why it's a crack problem:** Tests heap usage for merging — a pattern used in external sorting, log merging, etc.

**Time:** O(n log k) | **Space:** O(k)

---

## 5. Reverse Nodes in K-Group

| Detail | Value |
|---|---|
| **Pattern** | Linked List reversal |
| **Difficulty** | Hard |
| **Companies** | Amazon, Microsoft, Google |
| **LeetCode** | [25](https://leetcode.com/problems/reverse-nodes-in-k-group/) |

**Approach:** Recursion: reverse first k nodes, then recursively call on rest. Iterative: count k nodes, reverse sublist, connect.

**Why it's a crack problem:** Tests pointer manipulation skills under pressure.

**Time:** O(n) | **Space:** O(n/k) recursion or O(1) iterative

---

## 6. Trapping Rain Water

| Detail | Value |
|---|---|
| **Pattern** | Two Pointer |
| **Difficulty** | Hard |
| **Companies** | Amazon, Google, Meta |
| **LeetCode** | [42](https://leetcode.com/problems/trapping-rain-water/) |

**Approach:** Two pointers: left and right. Track leftMax and rightMax. At each step, process the smaller of the two boundaries. Water = max(0, boundary - height).

**Why it's a crack problem:** Elegant two-pointer solution that requires understanding the invariant.

**Time:** O(n) | **Space:** O(1)

---

## 7. Word Ladder II

| Detail | Value |
|---|---|
| **Pattern** | BFS + Backtracking |
| **Difficulty** | Hard |
| **Companies** | Amazon, Google |
| **LeetCode** | [126](https://leetcode.com/problems/word-ladder-ii/) |

**Approach:** BFS to find shortest distances and build neighbor graph, then DFS/backtrack to enumerate all paths.

**Why it's a crack problem:** Combines two major techniques (BFS + backtracking) end-to-end.

**Time:** O(m² × n) | **Space:** O(m × n)

---

## 8. LRU Cache

| Detail | Value |
|---|---|
| **Pattern** | Doubly Linked List + HashMap |
| **Difficulty** | Medium |
| **Companies** | Amazon, Google, Meta, Microsoft, Apple |
| **LeetCode** | [146](https://leetcode.com/problems/lru-cache/) |

**Approach:** HashMap for O(1) access. Doubly linked list for O(1) add/remove. Move to head on access. Remove from tail on eviction.

**Why it's a crack problem:** Classic system design + OOP problem that tests Java's data structure composition skills.

**Time:** O(1) per operation | **Space:** O(capacity)

---

## 9. Serialize and Deserialize Binary Tree

| Detail | Value |
|---|---|
| **Pattern** | Preorder + Queue |
| **Difficulty** | Hard |
| **Companies** | Amazon, Google, Meta, Microsoft |
| **LeetCode** | [297](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) |

**Approach:** Preorder with null markers. Deserialize by rebuilding recursively from a queue of values.

**Why it's a crack problem:** Tests recursive thinking and tree construction.

**Time:** O(n) | **Space:** O(n)

---

## 10. Longest Palindromic Substring

| Detail | Value |
|---|---|
| **Pattern** | Expand Around Center / DP |
| **Difficulty** | Medium |
| **Companies** | Amazon, Google, Meta |
| **LeetCode** | [5](https://leetcode.com/problems/longest-palindromic-substring/) |

**Approach:** For each of 2n-1 centers, expand outward while palindrome holds. Track max.

**Why it's a crack problem:** Tests palindrome understanding and O(n²) optimization.

**Time:** O(n²) | **Space:** O(1)

---

## 11. Next Permutation

| Detail | Value |
|---|---|
| **Pattern** | Array manipulation |
| **Difficulty** | Medium |
| **Companies** | Amazon, Google, Meta |
| **LeetCode** | [31](https://leetcode.com/problems/next-permutation/) |

**Approach:** Find first decreasing element from right. Find next larger element to its right. Swap. Reverse suffix.

**Why it's a crack problem:** Lexicographic ordering logic appears in many combinatorics problems.

**Time:** O(n) | **Space:** O(1)

---

## 12. Minimum Window Substring

| Detail | Value |
|---|---|
| **Pattern** | Sliding Window + HashMap |
| **Difficulty** | Hard |
| **Companies** | Amazon, Google, Meta, Microsoft |
| **LeetCode** | [76](https://leetcode.com/problems/minimum-window-substring/) |

**Approach:** Two pointers for window. HashMap for char counts of t. Expand right until window contains t. Then shrink left while still valid. Track min length.

**Why it's a crack problem:** Tests advanced sliding window with frequency tracking—very common pattern.

**Time:** O(n) | **Space:** O(m)

---

## 13. Maximal Rectangle

| Detail | Value |
|---|---|
| **Pattern** | Histogram + Stack |
| **Difficulty** | Hard |
| **Companies** | Google, Amazon |
| **LeetCode** | [85](https://leetcode.com/problems/maximal-rectangle/) |

**Approach:** Build heights per row. Apply Largest Rectangle in Histogram (monotonic stack) for each row.

**Why it's a crack problem:** Combines two techniques (prefix sums concept + stack) into one.

**Time:** O(m × n) | **Space:** O(n)

---

## 14. Number of Islands

| Detail | Value |
|---|---|
| **Pattern** | DFS / BFS on Grid |
| **Difficulty** | Medium |
| **Companies** | Amazon, Google, Meta, Microsoft |
| **LeetCode** | [200](https://leetcode.com/problems/number-of-islands/) |

**Approach:** Iterate grid. When '1' found, increment count and DFS to sink all connected '1's.

**Why it's a crack problem:** The canonical grid traversal problem. Foundation for all island/graph-on-grid problems.

**Time:** O(m × n) | **Space:** O(m × n)

---

## 15. Course Schedule II

| Detail | Value |
|---|---|
| **Pattern** | Topological Sort (Kahn's) |
| **Difficulty** | Medium |
| **Companies** | Google, Amazon, Meta |
| **LeetCode** | [210](https://leetcode.com/problems/course-schedule-ii/) |

**Approach:** Build adjacency list and indegree array. Queue nodes with indegree 0. Process, decrement indegree of neighbors.

**Why it's a crack problem:** Tests graph dependency resolution — used in build systems, task scheduling.

**Time:** O(V + E) | **Space:** O(V + E)

---

## 16. Copy List with Random Pointer

| Detail | Value |
|---|---|
| **Pattern** | Interleaving / HashMap |
| **Difficulty** | Medium |
| **Companies** | Amazon, Microsoft, Google |
| **LeetCode** | [138](https://leetcode.com/problems/copy-list-with-random-pointer/) |

**Approach:** Interleave original and copy: create copy, insert between original and original.next. Set random pointers. Separate lists.

**Why it's a crack problem:** Tests creative O(1) space pointer manipulation.

**Time:** O(n) | **Space:** O(1)

---

## 17. Find Median from Data Stream

| Detail | Value |
|---|---|
| **Pattern** | Two Heaps |
| **Difficulty** | Hard |
| **Companies** | Amazon, Google, Meta |
| **LeetCode** | [295](https://leetcode.com/problems/find-median-from-data-stream/) |

**Approach:** MaxHeap for left half, MinHeap for right half. Balance sizes. Median = top of larger heap or average of tops.

**Why it's a crack problem:** Real-time data processing pattern. Tests heap balancing.

**Time:** O(log n) per add, O(1) for median | **Space:** O(n)

---

## 18. Word Break II

| Detail | Value |
|---|---|
| **Pattern** | DP + Backtracking / Memoization |
| **Difficulty** | Hard |
| **Companies** | Amazon, Google |
| **LeetCode** | [140](https://leetcode.com/problems/word-break-ii/) |

**Approach:** Memoization: for each index i, compute all sentences from i to end. Combine word + each sentence from remaining part.

**Why it's a crack problem:** Tests DP with result construction, not just counting.

**Time:** O(2ⁿ) worst (but much better with memo) | **Space:** O(n × 2ⁿ)

---

## 19. Basic Calculator

| Detail | Value |
|---|---|
| **Pattern** | Stack + Parsing |
| **Difficulty** | Hard |
| **Companies** | Google, Amazon, Meta |
| **LeetCode** | [224](https://leetcode.com/problems/basic-calculator/) |

**Approach:** Stack for results/signs. Track current number and sign. When '(' encountered, push current result and sign. When ')' encountered, compute.

**Why it's a crack problem:** Tests expression parsing with state management.

**Time:** O(n) | **Space:** O(n)

---

## 20. Best Time to Buy and Sell Stock IV

| Detail | Value |
|---|---|
| **Pattern** | DP (transaction state) |
| **Difficulty** | Hard |
| **Companies** | Amazon, Google |
| **LeetCode** | [188](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/) |

**Approach:** dp[k][i] = max profit with at most k transactions up to day i. Optimize: track maxDiff = dp[k-1][i-1] - prices[i-1].

**Why it's a crack problem:** State machine DP pattern — foundational for scheduling problems.

**Time:** O(k × n) | **Space:** O(k × n) or O(n) with optimization

---

## 21. Valid Number

| Detail | Value |
|---|---|
| **Pattern** | State machine / Deterministic parsing |
| **Difficulty** | Hard |
| **Companies** | Google, Meta |
| **LeetCode** | [65](https://leetcode.com/problems/valid-number/) |

**Approach:** Track flags: seenDigit, seenDot, seenE, seenSignAfterE. Iterate characters with state transitions.

**Why it's a crack problem:** Tests rigorous specification parsing and edge case handling.

**Time:** O(n) | **Space:** O(1)

---

## 22. Longest Increasing Path in a Matrix

| Detail | Value |
|---|---|
| **Pattern** | DFS + Memoization |
| **Difficulty** | Hard |
| **Companies** | Google, Amazon |
| **LeetCode** | [329](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) |

**Approach:** DFS from each cell with memoization. Cache longest path starting from each cell. Only move to cells with greater value.

**Why it's a crack problem:** Top-down DP on grid — classic combination of DFS and DP.

**Time:** O(m × n) | **Space:** O(m × n)

---

## 23. Alien Dictionary

| Detail | Value |
|---|---|
| **Pattern** | Topological Sort |
| **Difficulty** | Hard |
| **Companies** | Google, Amazon, Meta |
| **LeetCode** | [269](https://leetcode.com/problems/alien-dictionary/) |

**Approach:** Compare adjacent words to find ordering rules. Build directed graph. Topological sort (Kahn's). Detect cycles.

**Why it's a crack problem:** Tests unknown-problem mapping to known techniques (graph).

**Time:** O(C) where C = total characters | **Space:** O(1)

---

## 24. Shortest Subarray with Sum at Least K

| Detail | Value |
|---|---|
| **Pattern** | Deque + Prefix Sum |
| **Difficulty** | Hard |
| **Companies** | Google, Amazon |
| **LeetCode** | [862](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/) |

**Approach:** Maintain prefix sums in monotonic increasing deque. For each prefix sum, remove from front those satisfying sum ≥ K. Before adding, remove from back larger sums.

**Why it's a crack problem:** Tests deque optimization beyond basic sliding window.

**Time:** O(n) | **Space:** O(n)

---

## 25. Count of Smaller Numbers After Self

| Detail | Value |
|---|---|
| **Pattern** | Fenwick Tree / Merge Sort |
| **Difficulty** | Hard |
| **Companies** | Google, Amazon |
| **LeetCode** | [315](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) |

**Approach (BIT):** Coordinate compress. Traverse right to left. Query BIT for count ≤ value-1. Update BIT with +1 at this value.

**Why it's a crack problem:** Fenwick tree application that tests advanced data structure thinking.

**Time:** O(n log n) | **Space:** O(n)

---

## 26. Frog Jump

| Detail | Value |
|---|---|
| **Pattern** | HashMap + Set / DP |
| **Difficulty** | Hard |
| **Companies** | Google, Amazon |
| **LeetCode** | [403](https://leetcode.com/problems/frog-jump/) |

**Approach:** HashMap<Integer, Set<Integer>> mapping stone → reachable jump sizes. For each stone, try adding k-1, k, k+1.

**Why it's a crack problem:** Non-standard DP that requires choosing the right state representation.

**Time:** O(n²) | **Space:** O(n²)

---

## 27. Palindrome Pairs

| Detail | Value |
|---|---|
| **Pattern** | Trie + HashMap |
| **Difficulty** | Hard |
| **Companies** | Google, Meta |
| **LeetCode** | [336](https://leetcode.com/problems/palindrome-pairs/) |

**Approach:** Insert all words reversed in Trie. For each word, search in Trie checking both full match and partial match (where remaining chars form palindrome).

**Why it's a crack problem:** Tests creative combinations of data structures.

**Time:** O(n × k²) | **Space:** O(n × k)

---

## 28. Sliding Window Maximum

| Detail | Value |
|---|---|
| **Pattern** | Deque (Monotonic Queue) |
| **Difficulty** | Hard |
| **Companies** | Amazon, Google, Meta |
| **LeetCode** | [239](https://leetcode.com/problems/sliding-window-maximum/) |

**Approach:** Maintain deque of indices with decreasing values. Before adding new: remove out-of-window indices from front, remove smaller values from back. Front = max.

**Why it's a crack problem:** Monotonic queue pattern — tests understanding of optimization beyond brute force.

**Time:** O(n) | **Space:** O(k)

---

## 29. Longest Valid Parentheses

| Detail | Value |
|---|---|
| **Pattern** | Stack / DP |
| **Difficulty** | Hard |
| **Companies** | Google, Amazon, Meta |
| **LeetCode** | [32](https://leetcode.com/problems/longest-valid-parentheses/) |

**Approach (Stack):** Stack with indices. Push -1 as base. When '(' push index. When ')' pop, if stack empty push current index (new base), else compute length = i - stack.peek().

**Why it's a crack problem:** Tests understanding of stack beyond simple matching — tracking positions.

**Time:** O(n) | **Space:** O(n)

---

## 30. Sudoku Solver

| Detail | Value |
|---|---|
| **Pattern** | Backtracking |
| **Difficulty** | Hard |
| **Companies** | Amazon, Google, Microsoft |
| **LeetCode** | [37](https://leetcode.com/problems/sudoku-solver/) |

**Approach:** Find empty cell. For each valid digit 1-9, place it and recursively solve. If fails, backtrack. Use arrays for row/col/box validation.

**Why it's a crack problem:** Classic constraint satisfaction — tests backtracking implementation proficiency.

**Time:** O(9!(n²)) worst | **Space:** O(n²)

---

## Prioritization Matrix

| Problem | Difficulty | Pattern | Importance | Frequency |
|---|---|---|---|---|
| Two Sum | Easy | HashMap | ★★★★★ | Extremely High |
| Longest Substring | Medium | Sliding Window | ★★★★★ | Extremely High |
| Median of Two Arrays | Hard | Binary Search | ★★★★☆ | High |
| Merge K Sorted | Hard | Heap | ★★★★★ | Extremely High |
| Reverse K-Group | Hard | LL Reverse | ★★★★☆ | High |
| Trapping Rain Water | Hard | Two Pointer | ★★★★★ | Extremely High |
| Word Ladder II | Hard | BFS+BT | ★★★★☆ | Medium |
| LRU Cache | Medium | Design | ★★★★★ | Extremely High |
| Serialize/Deserialize | Hard | Tree | ★★★★★ | High |
| Longest Palindromic | Medium | Expand | ★★★★★ | High |
| Next Permutation | Medium | Array | ★★★★☆ | High |
| Min Window Substr | Hard | Sliding Window | ★★★★★ | High |
| Maximal Rectangle | Hard | Stack | ★★★★☆ | Medium |
| Number of Islands | Medium | DFS | ★★★★★ | Extremely High |
| Course Schedule II | Medium | Topo Sort | ★★★★★ | High |
| Copy Random Pointer | Medium | LL | ★★★★☆ | High |
| Median from Stream | Hard | Two Heaps | ★★★★★ | High |
| Word Break II | Hard | DP+BT | ★★★★☆ | Medium |
| Basic Calculator | Hard | Stack | ★★★★☆ | High |
| Buy&Sell Stock IV | Hard | DP | ★★★★☆ | Medium |
| Valid Number | Hard | Parse | ★★★☆☆ | Medium |
| Longest Inc Path | Hard | DFS+Memo | ★★★★★ | High |
| Alien Dictionary | Hard | Topo Sort | ★★★★☆ | Medium |
| Shortest Subarray K | Hard | Deque | ★★★★☆ | Medium |
| Count Smaller After | Hard | Fenwick | ★★★★☆ | Medium |
| Frog Jump | Hard | DP | ★★★☆☆ | Medium |
| Palindrome Pairs | Hard | Trie | ★★★★☆ | Medium |
| Sliding Window Max | Hard | Deque | ★★★★★ | High |
| Longest Valid Parens | Hard | Stack/DP | ★★★★☆ | High |
| Sudoku Solver | Hard | Backtrack | ★★★★☆ | Medium |

---

## 30-Day Drill Schedule

| Day | Problems |
|---|---|
| 1-5 | 1-6 (Two Sum, Longest Substr, Median, Merge K, Reverse K, Rain Water) |
| 6-10 | 7-12 (Word Ladder II, LRU Cache, Serialize, Longest Pal, Next Perm, Min Window) |
| 11-15 | 13-18 (Max Rect, Islands, Course Schedule II, Copy Random, Median Stream, Word Break II) |
| 16-20 | 19-24 (Basic Calc, Stock IV, Valid Number, Longest Inc Path, Alien Dict, Shortest Sub K) |
| 21-25 | 25-30 (Count Smaller, Frog Jump, Palindrome Pairs, Sliding Max, Longest Parens, Sudoku) |
| 26-28 | Full-mix timed mock (3 problems, 90 min) |
| 29-30 | Weak problem review + re-solve |

---

## Final Tips

- Solve these **without any hints** before looking at solutions
- For each problem, **write Java code** that compiles and passes LeetCode
- **Time yourself** — 30 min for Medium, 45 min for Hard
- **Explain out loud** as you code (or record yourself)
- **Revise** — these problems need 3+ passes for full retention
- **Cover all companies** — this list covers Google, Amazon, Meta, Microsoft, Apple patterns
- **Mock interviews** — after finishing, run full 45-min mocks with these problems
