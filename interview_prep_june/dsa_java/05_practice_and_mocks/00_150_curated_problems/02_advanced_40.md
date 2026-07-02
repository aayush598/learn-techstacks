# Advanced 40 — Hard Difficulty Problems

> For FAANG+ and top-tier company interviews. These require deep pattern recognition, multiple techniques combined, and careful optimization.

---

## Prerequisites

- All Beginner 30 problems done and revised
- All Intermediate 50 problems done and revised
- Strong familiarity with Java Collections, recursion, and time/space optimization
- Comfort with proofs and invariants

---

## Arrays (5 problems)

### 1. Maximum Rectangle in Binary Matrix

| Property | Value |
|---|---|
| **Pattern** | Histogram + DP + Stack |
| **Platform** | [LeetCode 85](https://leetcode.com/problems/maximal-rectangle/) |

**Description:** Given a binary matrix (0s and 1s), find the largest rectangle containing only 1s.

**Solution Approach:** Treat each row as base of histogram. Compute heights array (if cell=1, add 1 else 0). For each row, apply "largest rectangle in histogram" (monotonic stack). Track max.

**Complexity:** O(m × n) time, O(n) space.

---

### 2. First Missing Positive

| Property | Value |
|---|---|
| **Pattern** | Cycle sort / Index mapping |
| **Platform** | [LeetCode 41](https://leetcode.com/problems/first-missing-positive/) |

**Description:** Find the smallest positive integer not present in unsorted array. O(n) time, O(1) space.

**Solution Approach:** Place each number at its correct index (value i at index i-1). In-place swap: while `nums[i]` is in range [1, n] and not at correct position, swap with `nums[nums[i]-1]`. Then iterate to find first missing.

**Complexity:** O(n) time, O(1) space.

---

### 3. Merge K Sorted Arrays (Space Optimized)

| Property | Value |
|---|---|
| **Pattern** | MinHeap / Divide & Conquer |
| **Platform** | [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/) (array version) |

**Description:** Merge k sorted arrays into one sorted array.

**Solution Approach:** MinHeap of (value, arrayIndex, elementIndex). Add first element of each array. Poll smallest, add to result, push next from same array.

**Complexity:** O(n log k) time, O(k + n) space (n = total elements).

---

### 4. Sliding Window Maximum

| Property | Value |
|---|---|
| **Pattern** | Deque / Monotonic Queue |
| **Platform** | [LeetCode 239](https://leetcode.com/problems/sliding-window-maximum/) |

**Description:** Return max in each sliding window of size k.

**Solution Approach:** Maintain deque of indices where values are decreasing. Before adding new: remove indices outside window (left bound), remove smaller values from back. Front of deque is max.

**Complexity:** O(n) time, O(k) space.

---

### 5. Median of Two Sorted Arrays

| Property | Value |
|---|---|
| **Pattern** | Binary Search + Partitioning |
| **Platform** | [LeetCode 4](https://leetcode.com/problems/median-of-two-sorted-arrays/) |

**Description:** Find median of two sorted arrays. O(log(min(n,m))).

**Solution Approach:** Binary search on smaller array. Partition both arrays such that left half = right half in size. Check maxLeft ≤ minRight. Adjust partition via binary search.

**Complexity:** O(log(min(n,m))) time, O(1) space.

---

## Strings (3 problems)

### 6. Wildcard Matching

| Property | Value |
|---|---|
| **Pattern** | 2D DP / Greedy |
| **Platform** | [LeetCode 44](https://leetcode.com/problems/wildcard-matching/) |

**Description:** Wildcard matching with `?` (any char) and `*` (any sequence).

**Solution Approach (DP):** 2D DP where dp[i][j] = first i chars of s match first j chars of p. If p[j-1]=='*', dp[i][j] = dp[i][j-1] (empty) || dp[i-1][j] (match one). Handle `?` and exact match.

**Complexity:** O(m × n) time, O(n) space optimized.

---

### 7. Regular Expression Matching

| Property | Value |
|---|---|
| **Pattern** | 2D DP |
| **Platform** | [LeetCode 10](https://leetcode.com/problems/regular-expression-matching/) |

**Description:** Implement regex with `.` (any char) and `*` (zero or more of preceding).

**Solution Approach:** DP table. If next char is `*`, two possibilities: skip (treat `*` as zero) or if chars match, consume one char from s and stay. If not `*`, simple char match or `.`.

**Complexity:** O(m × n) time, O(m × n) space.

---

### 8. Distinct Subsequences

| Property | Value |
|---|---|
| **Pattern** | 2D DP |
| **Platform** | [LeetCode 115](https://leetcode.com/problems/distinct-subsequences/) |

**Description:** Count number of distinct subsequences of s that equal t.

**Solution Approach:** dp[i][j] = # ways for t[0..i-1] in s[0..j-1]. If s[j-1]==t[i-1]: dp[i][j] = dp[i-1][j-1] (use match) + dp[i][j-1] (skip). Else: dp[i][j] = dp[i][j-1].

**Complexity:** O(m × n) time, O(n) space optimized.

---

## Trees (5 problems)

### 9. Serialize and Deserialize Binary Tree

| Property | Value |
|---|---|
| **Pattern** | Preorder + Queue |
| **Platform** | [LeetCode 297](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) |

**Description:** Convert binary tree to string and back (any binary tree, not just BST).

**Solution Approach (Preorder):** Serialize: preorder with null markers ("#"). Deserialize: queue of values. Build recursively: poll front, if "#" return null, else create node and build left/right.

**Complexity:** O(n) time, O(n) space.

---

### 10. Binary Tree Maximum Path Sum

| Property | Value |
|---|---|
| **Pattern** | Postorder + max computation |
| **Platform** | [LeetCode 124](https://leetcode.com/problems/binary-tree-maximum-path-sum/) |

**Description:** Find maximum path sum (path can start and end at any node).

**Solution Approach:** Postorder traversal. For each node, compute max single-side sum = max(0, leftGain) + max(0, rightGain) + node.val. Update global max. Return node.val + max(0, leftGain, rightGain) to parent.

**Complexity:** O(n) time, O(h) space.

---

### 11. Construct Binary Tree from Inorder and Postorder

| Property | Value |
|---|---|
| **Pattern** | Divide and Conquer |
| **Platform** | [LeetCode 106](https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/) |

**Description:** Build tree from inorder and postorder arrays.

**Solution Approach:** Last element of postorder is root. Find root in inorder. Right subtree processed first (postorder reversal). Recurse with indices.

**Complexity:** O(n) time (with HashMap), O(n) space.

---

### 12. Recover Binary Search Tree

| Property | Value |
|---|---|
| **Pattern** | Morris Traversal / Inorder |
| **Platform** | [LeetCode 99](https://leetcode.com/problems/recover-binary-search-tree/) |

**Description:** Two nodes in BST are swapped. Fix in O(1) space.

**Solution Approach:** Morris inorder traversal (O(1) space). Track prev, first, second. When prev.val > curr.val, mark first (prev) and second (curr). After traversal, swap first.val and second.val.

**Complexity:** O(n) time, O(1) space.

---

### 13. Vertical Order Traversal

| Property | Value |
|---|---|
| **Pattern** | BFS + Column map + Sorting |
| **Platform** | [LeetCode 987](https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/) |

**Description:** Return vertical order traversal (top-to-bottom, left-to-right within same row/col).

**Solution Approach:** TreeMap<Integer, TreeMap<Integer, PriorityQueue>> mapping col → (row → values). BFS/DFS tracking (node, row, col). After traversal, build result from map sorted by col then row.

**Complexity:** O(n log n) time, O(n) space.

---

## Graphs (5 problems)

### 14. Alien Dictionary

| Property | Value |
|---|---|
| **Pattern** | Topological Sort |
| **Platform** | [LeetCode 269](https://leetcode.com/problems/alien-dictionary/) (locked, see LintCode 892) |

**Description:** Given sorted words in alien language, find character order.

**Solution Approach:** Build directed graph from adjacent words (find first differing char, add edge from earlier to later char). Topological sort (Kahn's). Detect cycles.

**Complexity:** O(C) time, O(1) space (26 letters).

---

### 15. Word Ladder II

| Property | Value |
|---|---|
| **Pattern** | BFS (shortest path) + Backtracking |
| **Platform** | [LeetCode 126](https://leetcode.com/problems/word-ladder-ii/) |

**Description:** Find all shortest transformation sequences from beginWord to endWord.

**Solution Approach:** BFS to find shortest distance and build neighbor graph. Then DFS/backtrack from beginWord to endWord using only edges that go to next distance level.

**Complexity:** O(m² × n) time, O(m × n) space.

---

### 16. Travelling Salesman Problem (TSP)

| Property | Value |
|---|---|
| **Pattern** | Bitmask DP |
| **Platform** | [GeeksforGeeks](https://www.geeksforgeeks.org/travelling-salesman-problem-set-1/) |

**Description:** Given a set of cities and distance matrix, find shortest route visiting each once and returning.

**Solution Approach:** dp[mask][i] = min distance to visit set `mask` ending at city i. dp[mask|1<<j][j] = min(dp[mask][i] + dist[i][j]). Base: dp[1][0] = 0.

**Complexity:** O(n² × 2ⁿ) time, O(n × 2ⁿ) space.

---

### 17. Strongly Connected Components (Kosaraju / Tarjan)

| Property | Value |
|---|---|
| **Pattern** | DFS + Stack |
| **Platform** | [GeeksforGeeks](https://www.geeksforgeeks.org/strongly-connected-components/) |

**Description:** Find all SCCs in a directed graph.

**Solution Approach (Kosaraju):** Step 1: DFS on original, push to stack on finish. Step 2: Reverse graph. Step 3: Pop from stack, DFS on reversed graph — each DFS tree is an SCC.

**Complexity:** O(V + E) time, O(V) space.

---

### 18. Minimum Height Trees

| Property | Value |
|---|---|
| **Pattern** | Topological removal (leaf peeling) |
| **Platform** | [LeetCode 310](https://leetcode.com/problems/minimum-height-trees/) |

**Description:** Find roots that minimize tree height in an undirected graph.

**Solution Approach:** Remove leaves layer by layer (BFS like Kahn's). Last one or two nodes remaining are the MHT roots.

**Complexity:** O(V + E) time, O(V + E) space.

---

## DP (5 problems)

### 19. Burst Balloons

| Property | Value |
|---|---|
| **Pattern** | Interval DP (divide & conquer) |
| **Platform** | [LeetCode 312](https://leetcode.com/problems/burst-balloons/) |

**Description:** Burst balloons to maximize coins (coin = nums[i-1]*nums[i]*nums[i+1]).

**Solution Approach:** Add 1 at both ends. dp[left][right] = max coins from bursting all balloons between left and right (exclusive). dp[l][r] = max(dp[l][r], nums[l]*nums[k]*nums[r] + dp[l][k] + dp[k][r]).

**Complexity:** O(n³) time, O(n²) space.

---

### 20. Scramble String

| Property | Value |
|---|---|
| **Pattern** | Recursion + Memoization / 3D DP |
| **Platform** | [LeetCode 87](https://leetcode.com/problems/scramble-string/) |

**Description:** Determine if s2 is a scrambled version of s1.

**Solution Approach:** DP: dp[n][i][j] = is s1[i:i+n] scramble of s2[j:j+n]. For each split k=1..n-1, check: swap case (scramble) or no-swap case.

**Complexity:** O(n⁴) time, O(n³) space.

---

### 21. Palindrome Partitioning II

| Property | Value |
|---|---|
| **Pattern** | DP + Palindrome precomputation |
| **Platform** | [LeetCode 132](https://leetcode.com/problems/palindrome-partitioning-ii/) |

**Description:** Minimum cuts needed to partition string into palindromes.

**Solution Approach:** Step 1: Precompute palindrome table (or expand centers). Step 2: DP: cut[i] = min(cut[i], cut[j-1] + 1) if s[j..i] is palindrome.

**Complexity:** O(n²) time, O(n²) space.

---

### 22. Longest Increasing Path in a Matrix

| Property | Value |
|---|---|
| **Pattern** | DFS + Memoization |
| **Platform** | [LeetCode 329](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) |

**Description:** Find longest strictly increasing path in a matrix (4-directional).

**Solution Approach:** DFS with memo. For each cell, explore all 4 neighbors that are > current. Cache max length from each cell. Result = max over all cells.

**Complexity:** O(m × n) time, O(m × n) space.

---

### 23. Frog Jump

| Property | Value |
|---|---|
| **Pattern** | HashMap + HashSet / DP |
| **Platform** | [LeetCode 403](https://leetcode.com/problems/frog-jump/) |

**Description:** Determine if frog can cross river by jumping on stones.

**Solution Approach:** HashMap<Integer, Set<Integer>> mapping stone → jump sizes that reached it. For each stone, try k-1, k, k+1 as next jump. If last stone is reached, return true.

**Complexity:** O(n²) time, O(n²) space.

---

## DP on Tree (3 problems)

### 24. House Robber III

| Property | Value |
|---|---|
| **Pattern** | Tree DP (Postorder) |
| **Platform** | [LeetCode 337](https://leetcode.com/problems/house-robber-iii/) |

**Description:** Max money from binary tree (cannot rob adjacent nodes — parent-child).

**Solution Approach:** Postorder: return int[2] where [0] = max including current, [1] = max excluding current. include = val + left[1] + right[1]. exclude = max(left[0], left[1]) + max(right[0], right[1]).

**Complexity:** O(n) time, O(h) space.

---

### 25. Binary Tree Cameras

| Property | Value |
|---|---|
| **Pattern** | Greedy + Tree DP |
| **Platform** | [LeetCode 968](https://leetcode.com/problems/binary-tree-cameras/) |

**Description:** Minimum cameras needed to monitor binary tree (camera covers node + parent + children).

**Solution Approach:** Postorder with 3 states: 0 = no camera + not covered, 1 = no camera + covered, 2 = has camera. Return final based on root state.

**Complexity:** O(n) time, O(h) space.

---

### 26. Tree Diameter

| Property | Value |
|---|---|
| **Pattern** | DFS + diameter computation |
| **Platform** | [LeetCode 543](https://leetcode.com/problems/diameter-of-binary-tree/) |

**Description:** Length of longest path between any two nodes (may not pass through root).

**Solution Approach:** Postorder: compute leftHeight, rightHeight. Update global max = max(max, leftHeight + rightHeight). Return 1 + max(leftHeight, rightHeight).

**Complexity:** O(n) time, O(h) space.

---

## Bitmask DP (3 problems)

### 27. Shortest Superstring

| Property | Value |
|---|---|
| **Pattern** | Bitmask DP + Overlap |
| **Platform** | [LeetCode 943](https://leetcode.com/problems/find-the-shortest-superstring/) |

**Description:** Find shortest string that contains each given word as substring.

**Solution Approach:** Precompute overlap[i][j] = overlap chars when word j follows word i. dp[mask][i] = min length of superstring for set `mask` ending with word i. Also store parent for reconstruction.

**Complexity:** O(n² × 2ⁿ + n² × L) time, O(n × 2ⁿ) space.

---

### 28. Partition to K Equal Sum Subsets

| Property | Value |
|---|---|
| **Pattern** | Bitmask DP / Backtracking with pruning |
| **Platform** | [LeetCode 698](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) |

**Description:** Can array be partitioned into k subsets with equal sum?

**Solution Approach (DP with mask):** dp[mask] = -1 (unreachable) or sum of current subset. For each mask, try adding unused element. If subset sum == target, start new subset. If all elements used → true.

**Complexity:** O(n × 2ⁿ) time, O(2ⁿ) space.

---

### 29. Maximum Number of Achievable Requests

| Property | Value |
|---|---|
| **Pattern** | Bitmask / Backtracking |
| **Platform** | [LeetCode 1601](https://leetcode.com/problems/maximum-number-of-achievable-transfer-requests/) |

**Description:** Max requests that can be satisfied from a set of building transfer requests.

**Solution Approach:** Evaluate all subsets via bitmask (2ⁿ). For each subset, compute net change per building. If all zero, valid. Track max count.

**Complexity:** O(n × 2ⁿ) time, O(n) space.

---

## Segment Tree / Fenwick (3 problems)

### 30. Count of Smaller Numbers After Self

| Property | Value |
|---|---|
| **Pattern** | Fenwick Tree / Segment Tree / Merge Sort |
| **Platform** | [LeetCode 315](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) |

**Description:** For each element, count numbers to its right that are smaller.

**Solution Approach (Fenwick):** Coordinate compress values. Traverse from right to left. Query Fenwick for count ≤ val-1. Update Fenwick at val's rank.

**Complexity:** O(n log n) time, O(n) space.

---

### 31. Range Sum Query 2D - Mutable

| Property | Value |
|---|---|
| **Pattern** | Fenwick Tree 2D / Segment Tree 2D |
| **Platform** | [LeetCode 308](https://leetcode.com/problems/range-sum-query-2d-mutable/) |

**Description:** 2D matrix supporting update and range sum queries.

**Solution Approach (Fenwick 2D):** 2D BIT (Fenwick tree). Update propagates along both dimensions. Sum query uses inclusion-exclusion: sum(x2,y2) - sum(x1-1,y2) - sum(x2,y1-1) + sum(x1-1,y1-1).

**Complexity:** O(log m × log n) per query, O(m × n) space.

---

### 32. Range Sum Query - Mutable (Prefix Sum with Fenwick)

| Property | Value |
|---|---|
| **Pattern** | Fenwick Tree |
| **Platform** | [LeetCode 307](https://leetcode.com/problems/range-sum-query-mutable/) |

**Description:** Array supporting point update and range sum query.

**Solution Approach:** Fenwick tree (BIT). Update: add delta to index and propagate to parent. Query: prefix sum via bit operation.

**Complexity:** O(log n) per operation, O(n) space.

---

## Tries (3 problems)

### 33. Word Search II

| Property | Value |
|---|---|
| **Pattern** | Trie + Backtracking (DFS on board) |
| **Platform** | [LeetCode 212](https://leetcode.com/problems/word-search-ii/) |

**Description:** Find all words from dictionary on the board (4-directional adjacency).

**Solution Approach:** Build Trie from words. DFS board. At each cell, if Trie node has children, explore neighbors. When wordEnd reached, collect (mark to avoid duplicates). Prune: remove leaf nodes from Trie after collection.

**Complexity:** O(m × n × 4^(L)) worst, but Trie pruning helps. O(total word chars) space.

---

### 34. Maximum XOR of Two Numbers in an Array

| Property | Value |
|---|---|
| **Pattern** | Trie (Binary) |
| **Platform** | [LeetCode 421](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/) |

**Description:** Find max XOR of any two numbers in array.

**Solution Approach:** Insert all numbers in binary Trie (31 bits). For each number, traverse Trie preferring opposite bit (1→0, 0→1) to maximize XOR. Track max.

**Complexity:** O(n × 31) time, O(n × 31) space.

---

### 35. Palindrome Pairs

| Property | Value |
|---|---|
| **Pattern** | Trie + HashMap |
| **Platform** | [LeetCode 336](https://leetcode.com/problems/palindrome-pairs/) |

**Description:** Find all pairs (i, j) such that words[i] + words[j] is palindrome.

**Solution Approach:** Insert reversed words in Trie with index. For each word, search in Trie checking all possible palindrome endings. Also handle empty string and self-palindrome cases.

**Complexity:** O(n × k²) time, O(n × k) space (k = avg word length).

---

## Design (5 problems)

### 36. LRU Cache

| Property | Value |
|---|---|
| **Pattern** | HashMap + Doubly Linked List |
| **Platform** | [LeetCode 146](https://leetcode.com/problems/lru-cache/) |

**Description:** Design cache with O(1) get and put, evicting least recently used on capacity overflow.

**Solution Approach:** HashMap<Integer, Node>. Doubly linked list with dummy head/tail. On get: move node to head. On put: if exists, update value and move to head. If new and at capacity, remove tail (LRU), add new at head.

**Complexity:** O(1) per operation, O(capacity) space.

---

### 37. LFU Cache

| Property | Value |
|---|---|
| **Pattern** | HashMap + Frequency List |
| **Platform** | [LeetCode 460](https://leetcode.com/problems/lfu-cache/) |

**Description:** Design cache evicting least frequently used (tie-break LRU).

**Solution Approach:** HashMap key→Node, HashMap freq→LinkedHashSet (ordered). Track minFreq. On get: increment freq, move between sets. On put: at capacity, evict from minFreq set (first element = LRU of LFU).

**Complexity:** O(1) per operation, O(capacity) space.

---

### 38. Design Search Autocomplete System

| Property | Value |
|---|---|
| **Pattern** | Trie + PriorityQueue / HashMap |
| **Platform** | [LeetCode 642](https://leetcode.com/problems/design-search-autocomplete-system/) |

**Description:** Autocomplete given past sentences and their hotness (frequency).

**Solution Approach:** Trie with map of sentence→hot in each node. On input: traverse Trie, collect all sentences from current node, sort by hot→lexicographical. Top 3 returned.

**Complexity:** O(n log k) per query, O(total chars) space.

---

### 39. Design In-Memory File System

| Property | Value |
|---|---|
| **Pattern** | Tree + HashMap |
| **Platform** | [LeetCode 588](https://leetcode.com/problems/design-in-memory-file-system/) |

**Description:** Design file system with mkdir, addContentToFile, readContentFromFile, ls.

**Solution Approach:** Tree of nodes (File or Dir). Each dir has HashMap<String, Node>. Ls: if file → return [name], if dir → return sorted list. Content stored in files.

**Complexity:** O(path length + n log n) for ls, O(path length) for others.

---

### 40. Design Iterator for Flattening

| Property | Value |
|---|---|
| **Pattern** | Iterator / Stack |
| **Platform** | [LeetCode 341](https://leetcode.com/problems/flatten-nested-list-iterator/) |

**Description:** Flatten nested list of integers (NestedInteger can be int or list).

**Solution Approach:** Stack of iterators (or stack of NestedInteger). hasNext: flatten until we find an integer. next: return top integer. Push/pop iterators as needed.

**Complexity:** O(n) total, O(d) space (d = nesting depth).

---

## Quick Reference Table

| # | Problem | Pattern | Time | Space |
|---|---|---|---|---|
| 1 | Max Rectangle | Histogram Stack | O(mn) | O(n) |
| 2 | First Missing Positive | Index Sort | O(n) | O(1) |
| 3 | Merge K Sorted Arrays | Heap | O(n log k) | O(n+k) |
| 4 | Sliding Window Max | Deque | O(n) | O(k) |
| 5 | Median Two Arrays | Binary Search | O(log mn) | O(1) |
| 6 | Wildcard Matching | DP | O(mn) | O(n) |
| 7 | Regex Matching | DP | O(mn) | O(mn) |
| 8 | Distinct Subsequences | DP | O(mn) | O(n) |
| 9 | Serialize/Deserialize BT | Preorder+Q | O(n) | O(n) |
| 10 | Max Path Sum | Postorder | O(n) | O(h) |
| 11 | Build from In+Post | D&C | O(n) | O(n) |
| 12 | Recover BST | Morris Inorder | O(n) | O(1) |
| 13 | Vertical Order | Map+BFS | O(n log n) | O(n) |
| 14 | Alien Dictionary | Topo Sort | O(C) | O(1) |
| 15 | Word Ladder II | BFS+BT | O(m²n) | O(mn) |
| 16 | TSP | Bitmask DP | O(n²2ⁿ) | O(n2ⁿ) |
| 17 | SCC (Kosaraju) | DFS+Rev | O(V+E) | O(V) |
| 18 | Min Height Trees | Leaf Peel | O(V+E) | O(V+E) |
| 19 | Burst Balloons | Interval DP | O(n³) | O(n²) |
| 20 | Scramble String | Memo DP | O(n⁴) | O(n³) |
| 21 | Palindrome Partition II | DP | O(n²) | O(n²) |
| 22 | Longest Inc Path | DFS+Memo | O(mn) | O(mn) |
| 23 | Frog Jump | HashMap+Set | O(n²) | O(n²) |
| 24 | House Robber III | Tree DP | O(n) | O(h) |
| 25 | BT Cameras | Greedy Tree DP | O(n) | O(h) |
| 26 | Tree Diameter | Postorder | O(n) | O(h) |
| 27 | Shortest Superstring | Bitmask DP | O(n²2ⁿ) | O(n2ⁿ) |
| 28 | Partition K Subsets | Bitmask/BT | O(n2ⁿ) | O(2ⁿ) |
| 29 | Max Requests | Bitmask | O(n2ⁿ) | O(n) |
| 30 | Count Smaller After | Fenwick | O(n log n) | O(n) |
| 31 | Range Sum 2D Mutable | Fenwick 2D | O(log²n) | O(mn) |
| 32 | Range Sum Mutable | Fenwick | O(log n) | O(n) |
| 33 | Word Search II | Trie+BT | O(mn4^L) | O(total) |
| 34 | Max XOR Pair | Binary Trie | O(31n) | O(31n) |
| 35 | Palindrome Pairs | Trie | O(nk²) | O(nk) |
| 36 | LRU Cache | DLink+Map | O(1) | O(cap) |
| 37 | LFU Cache | Freq+Map | O(1) | O(cap) |
| 38 | Autocomplete | Trie+Heap | O(n log k) | O(total) |
| 39 | File System | Tree+Map | O(path) | O(nodes) |
| 40 | Flatten Iterator | Stack | O(n) | O(d) |

---

## Tackling Hard Problems: Strategy

1. **Spend 45-60 min** before looking at solution
2. **Write out examples** — find the pattern yourself
3. **Reduce to known problem** — almost all hard problems combine 2-3 medium patterns
4. **Consider brute force first** to understand the problem bounds
5. **Check constraints** — O(n²) may be acceptable for n ≤ 10³, but not for n ≤ 10⁵
6. **Draw invariants** — especially for greedy/DP problems
7. **Debug with custom small cases** — edge cases matter most at hard level
8. **Study the solution** — even if you solve it, read the official solution for alternate approaches
9. **Re-solve without looking** — after 3 days, redo the problem from scratch
10. **Group by technique** — e.g., solve all 5 DP problems in one session, all 5 design problems in another
