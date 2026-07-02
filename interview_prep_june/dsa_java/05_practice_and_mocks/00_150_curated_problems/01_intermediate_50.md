# Intermediate 50 — Medium Difficulty Problems

> Core interview-level problems. Master these for most top-tier company interviews.

---

## Prerequisites

Before attempting these, you should be comfortable with:
- All Beginner 30 problems (file `00_beginner_30.md`)
- Core data structure implementations in Java
- Big O analysis
- Basic recursion and iteration patterns

---

## Arrays (10 problems)

### 1. Subarray Sum Equals K

| Property | Value |
|---|---|
| **Pattern** | Prefix Sum + HashMap |
| **Platform** | [LeetCode 560](https://leetcode.com/problems/subarray-sum-equals-k/) |

**Description:** Find the total number of subarrays whose sum equals k.

**Solution Approach:** Compute running prefix sum. Use a HashMap to store frequency of each prefix sum seen so far. For each `prefixSum`, check if `prefixSum - k` exists in map — count of that key is the number of subarrays ending at current index with sum k.

**Complexity:** O(n) time, O(n) space.

---

### 2. Product of Array Except Self

| Property | Value |
|---|---|
| **Pattern** | Prefix/Suffix product |
| **Platform** | [LeetCode 238](https://leetcode.com/problems/product-of-array-except-self/) |

**Description:** Return an array `answer` where `answer[i]` = product of all elements except `nums[i]`. Must be O(n) and without division.

**Solution Approach:** First pass compute prefix products into result array. Second pass traverse backwards with a running suffix product, multiplying into result.

**Complexity:** O(n) time, O(1) extra (output array not counted).

---

### 3. Spiral Matrix

| Property | Value |
|---|---|
| **Pattern** | Layer-by-layer simulation |
| **Platform** | [LeetCode 54](https://leetcode.com/problems/spiral-matrix/) |

**Description:** Given an m×n matrix, return all elements in spiral order.

**Solution Approach:** Use four boundaries: `top, bottom, left, right`. Traverse top row left→right, increment top. Traverse right column top→bottom, decrement right. Continue until boundaries cross.

**Complexity:** O(m×n) time, O(1) space (excluding output).

---

### 4. 3Sum

| Property | Value |
|---|---|
| **Pattern** | Sorting + Two Pointer |
| **Platform** | [LeetCode 15](https://leetcode.com/problems/3sum/) |

**Description:** Find all triplets that sum to zero (no duplicates).

**Solution Approach:** Sort array. Fix `nums[i]`, then use two pointers (left=i+1, right=n-1) to find pairs that sum to `-nums[i]`. Skip duplicates.

**Complexity:** O(n²) time, O(1) or O(n) for sorting.

---

### 5. Sort Colors (Dutch National Flag)

| Property | Value |
|---|---|
| **Pattern** | Partitioning |
| **Platform** | [LeetCode 75](https://leetcode.com/problems/sort-colors/) |

**Description:** Sort array of 0s, 1s, 2s in-place (no sorting library).

**Solution Approach:** Three pointers: `low, mid, high`. If `nums[mid]==0` swap with low. If `==1` mid++. If `==2` swap with high--.

**Complexity:** O(n) time, O(1) space.

---

### 6. Set Matrix Zeroes

| Property | Value |
|---|---|
| **Pattern** | In-place marker |
| **Platform** | [LeetCode 73](https://leetcode.com/problems/set-matrix-zeroes/) |

**Description:** If an element is 0, set its entire row and column to 0. Do it in-place.

**Solution Approach:** Use first row and first column as markers. First check if first row/col should be zeroed. Then iterate rest, marking rows/cols. In second pass, zero marked cells. Finally handle first row/col.

**Complexity:** O(m×n) time, O(1) space.

---

### 7. Rotate Image

| Property | Value |
|---|---|
| **Pattern** | Matrix transpose + reverse |
| **Platform** | [LeetCode 48](https://leetcode.com/problems/rotate-image/) |

**Description:** Rotate n×n matrix 90 degrees clockwise in-place.

**Solution Approach:** Transpose (swap across diagonal), then reverse each row.

**Complexity:** O(n²) time, O(1) space.

---

### 8. Merge Intervals

| Property | Value |
|---|---|
| **Pattern** | Sorting + merging |
| **Platform** | [LeetCode 56](https://leetcode.com/problems/merge-intervals/) |

**Description:** Merge overlapping intervals.

**Solution Approach:** Sort by start time. Iterate: if current interval overlaps with last in result (`curr.start <= last.end`), merge by setting `last.end = max(last.end, curr.end)`. Else add as new.

**Complexity:** O(n log n) time, O(n) space.

---

### 9. Find the Duplicate Number

| Property | Value |
|---|---|
| **Pattern** | Floyd's Cycle (Linked List in Array) |
| **Platform** | [LeetCode 287](https://leetcode.com/problems/find-the-duplicate-number/) |

**Description:** Find the repeated number in an array of size n+1 with values 1..n. Cannot modify array, O(1) space.

**Solution Approach:** Treat array values as "pointers" to indices (linked list). Use Floyd's cycle detection to find entry point of cycle — that's the duplicate.

**Complexity:** O(n) time, O(1) space.

---

### 10. Container With Most Water

| Property | Value |
|---|---|
| **Pattern** | Two Pointer |
| **Platform** | [LeetCode 11](https://leetcode.com/problems/container-with-most-water/) |

**Description:** Find two lines that form the maximum water container.

**Solution Approach:** Two pointers: `left=0, right=n-1`. Compute area = `min(h[l], h[r]) * (r-l)`. Move the smaller pointer inward.

**Complexity:** O(n) time, O(1) space.

---

## Strings (8 problems)

### 11. Longest Substring Without Repeating Characters

| Property | Value |
|---|---|
| **Pattern** | Sliding Window + HashMap |
| **Platform** | [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/) |

**Description:** Find length of longest substring without repeating characters.

**Solution Approach:** Sliding window with HashMap of char→lastIndex. Expand right. If duplicate found inside window, move left to max(left, lastSeen[char]+1).

**Complexity:** O(n) time, O(min(m, n)) space where m = charset size.

---

### 12. Group Anagrams

| Property | Value |
|---|---|
| **Pattern** | HashMap with sorted key |
| **Platform** | [LeetCode 49](https://leetcode.com/problems/group-anagrams/) |

**Description:** Group anagrams together from an array of strings.

**Solution Approach:** For each string, sort characters and use as key in HashMap<String, List<String>>. Alternatively, use char count array as key.

**Complexity:** O(n × k log k) time (sorting), O(n × k) space.

---

### 13. Longest Palindromic Substring

| Property | Value |
|---|---|
| **Pattern** | Expand around center |
| **Platform** | [LeetCode 5](https://leetcode.com/problems/longest-palindromic-substring/) |

**Description:** Find the longest palindromic substring.

**Solution Approach:** For each position (and between positions), expand outward as long as palindrome condition holds. Track max length.

**Complexity:** O(n²) time, O(1) space.

---

### 14. String to Integer (atoi)

| Property | Value |
|---|---|
| **Pattern** | State machine / parsing |
| **Platform** | [LeetCode 8](https://leetcode.com/problems/string-to-integer-atoi/) |

**Description:** Implement `atoi` — parse string to integer handling whitespace, sign, overflow.

**Solution Approach:** Skip leading whitespace. Handle sign. Read digits while building result. Check overflow before multiplication by comparing with Integer.MAX_VALUE/10.

**Complexity:** O(n) time, O(1) space.

---

### 15. KMP Algorithm: Find Pattern in String

| Property | Value |
|---|---|
| **Pattern** | LPS array + matching |
| **Platform** | [LeetCode 28](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) (strStr) |

**Description:** Find first occurrence of needle in haystack.

**Solution Approach (KMP):** Build LPS (longest prefix suffix) array. Use LPS to skip characters during matching. When mismatch, reuse earlier matches.

**Complexity:** O(n + m) time, O(m) space for LPS.

---

### 16. Zigzag Conversion

| Property | Value |
|---|---|
| **Pattern** | Row simulation |
| **Platform** | [LeetCode 6](https://leetcode.com/problems/zigzag-conversion/) |

**Description:** Convert string to zigzag on `numRows` rows and read row-wise.

**Solution Approach:** Use StringBuilder array for each row. Traverse s, append to current row, toggle direction at boundaries.

**Complexity:** O(n) time, O(n) space.

---

### 17. Compare Version Numbers

| Property | Value |
|---|---|
| **Pattern** | String splitting + parsing |
| **Platform** | [LeetCode 165](https://leetcode.com/problems/compare-version-numbers/) |

**Description:** Compare two version strings (e.g., "1.01" vs "1.001").

**Solution Approach:** Split by dots. Iterate max(parts1, parts2), parse each revision as int. Compare values.

**Complexity:** O(n + m) time, O(n + m) space.

---

### 18. Simplify Path

| Property | Value |
|---|---|
| **Pattern** | Stack + string parsing |
| **Platform** | [LeetCode 71](https://leetcode.com/problems/simplify-path/) |

**Description:** Simplify an absolute Unix-style path.

**Solution Approach:** Split by `/`. Use deque/stack. If `..` → pop. If `.` or empty → skip. Else push. Build result with `/` joining.

**Complexity:** O(n) time, O(n) space.

---

## Linked List (6 problems)

### 19. Remove Nth Node From End of List

| Property | Value |
|---|---|
| **Pattern** | Two pointer (fast/slow with gap) |
| **Platform** | [LeetCode 19](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) |

**Description:** Remove the nth node from the end.

**Solution Approach:** Dummy node, fast pointer moves n steps ahead. Then move both until fast reaches null. Remove slow.next.

**Complexity:** O(n) time, O(1) space.

---

### 20. Add Two Numbers

| Property | Value |
|---|---|
| **Pattern** | Dummy head + carry |
| **Platform** | [LeetCode 2](https://leetcode.com/problems/add-two-numbers/) |

**Description:** Add two numbers represented as reversed linked lists.

**Solution Approach:** Dummy node, carry variable. While l1 or l2 or carry, compute sum = carry + val1 + val2. Carry = sum/10. Node = sum%10.

**Complexity:** O(max(n, m)) time, O(1) space.

---

### 21. Reverse Linked List II

| Property | Value |
|---|---|
| **Pattern** | Partial reversal |
| **Platform** | [LeetCode 92](https://leetcode.com/problems/reverse-linked-list-ii/) |

**Description:** Reverse a linked list from position left to right.

**Solution Approach:** Traverse to node before left. Then reverse sublist (standard reversal) between left and right. Reconnect.

**Complexity:** O(n) time, O(1) space.

---

### 22. Odd Even Linked List

| Property | Value |
|---|---|
| **Pattern** | Node rearrangement |
| **Platform** | [LeetCode 328](https://leetcode.com/problems/odd-even-linked-list/) |

**Description:** Group all odd-indexed nodes together, then even-indexed.

**Solution Approach:** Maintain odd and even pointers. Connect odd.next = odd.next.next, even.next = even.next.next. At end, oddTail.next = evenHead.

**Complexity:** O(n) time, O(1) space.

---

### 23. Intersection of Two Linked Lists

| Property | Value |
|---|---|
| **Pattern** | Two-pointer alignment |
| **Platform** | [LeetCode 160](https://leetcode.com/problems/intersection-of-two-linked-lists/) |

**Description:** Find node where two LLs intersect.

**Solution Approach:** Two pointers. When one reaches null, redirect to other list's head. After second pass they meet at intersection. Or: compute lengths and advance longer.

**Complexity:** O(n + m) time, O(1) space.

---

### 24. Palindrome Linked List

| Property | Value |
|---|---|
| **Pattern** | Midpoint + reverse |
| **Platform** | [LeetCode 234](https://leetcode.com/problems/palindrome-linked-list/) |

**Description:** Check if linked list is palindrome.

**Solution Approach:** Find middle (slow/fast). Reverse second half. Compare first half with reversed second half. Restore if needed.

**Complexity:** O(n) time, O(1) space.

---

## Stack/Queue (4 problems)

### 25. Largest Rectangle in Histogram

| Property | Value |
|---|---|
| **Pattern** | Monotonic stack |
| **Platform** | [LeetCode 84](https://leetcode.com/problems/largest-rectangle-in-histogram/) |

**Description:** Find largest rectangle that can be formed in a histogram.

**Solution Approach:** Maintain monotonic increasing stack of indices. When a shorter bar arrives, pop taller bars, compute area with popped bar as shortest.

**Complexity:** O(n) time, O(n) space.

---

### 26. Daily Temperatures

| Property | Value |
|---|---|
| **Pattern** | Monotonic stack |
| **Platform** | [LeetCode 739](https://leetcode.com/problems/daily-temperatures/) |

**Description:** For each day, find days until warmer temperature.

**Solution Approach:** Monotonic decreasing stack. Pop when warmer found. Distance = current index - popped index.

**Complexity:** O(n) time, O(n) space.

---

### 27. Min Stack

| Property | Value |
|---|---|
| **Pattern** | Design with auxiliary stack |
| **Platform** | [LeetCode 155](https://leetcode.com/problems/min-stack/) |

**Description:** Stack supporting push, pop, top, getMin in O(1).

**Solution Approach:** Two stacks: main + minStack. Push: push value. Push min(value, minStack.peek()) onto minStack.

**Complexity:** O(1) per operation, O(n) space.

---

### 28. Implement Stack using Queues

| Property | Value |
|---|---|
| **Pattern** | Design |
| **Platform** | [LeetCode 225](https://leetcode.com/problems/implement-stack-using-queues/) |

**Description:** Implement LIFO stack using only queues.

**Solution Approach:** (Single queue) After pushing, rotate queue size-1 times so new element is at front. Or use two queues.

**Complexity:** O(n) push, O(1) pop, O(n) space.

---

## Trees (8 problems)

### 29. Binary Tree Inorder Traversal (Iterative)

| Property | Value |
|---|---|
| **Pattern** | Stack-based traversal |
| **Platform** | [LeetCode 94](https://leetcode.com/problems/binary-tree-inorder-traversal/) |

**Description:** Return inorder traversal without recursion.

**Solution Approach:** Stack. While curr != null or stack not empty: push left, pop → visit, go right.

**Complexity:** O(n) time, O(n) space.

---

### 30. Lowest Common Ancestor of BST

| Property | Value |
|---|---|
| **Pattern** | BST property |
| **Platform** | [LeetCode 235](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) |

**Description:** Find LCA of two nodes in a BST.

**Solution Approach:** If both values < root, go left. If both > root, go right. Else root is LCA.

**Complexity:** O(log n) / O(h) time, O(1) space.

---

### 31. Binary Tree Level Order Traversal

| Property | Value |
|---|---|
| **Pattern** | BFS with queue |
| **Platform** | [LeetCode 102](https://leetcode.com/problems/binary-tree-level-order-traversal/) |

**Description:** Return level-by-level traversal of binary tree.

**Solution Approach:** Queue. Process level by level using size variable. Add children for each node.

**Complexity:** O(n) time, O(n) space.

---

### 32. Validate Binary Search Tree

| Property | Value |
|---|---|
| **Pattern** | Range validation |
| **Platform** | [LeetCode 98](https://leetcode.com/problems/validate-binary-search-tree/) |

**Description:** Determine if a binary tree is a valid BST.

**Solution Approach:** Inorder traversal (must be strictly increasing). Or: recursive range check with min/max bounds.

**Complexity:** O(n) time, O(h) space.

---

### 33. Construct Binary Tree from Preorder and Inorder

| Property | Value |
|---|---|
| **Pattern** | Divide and conquer |
| **Platform** | [LeetCode 105](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) |

**Description:** Build tree from preorder and inorder arrays.

**Solution Approach:** First element of preorder is root. Find root's index in inorder. Left subtree = inorder[left:rootIdx], right = inorder[rootIdx+1:]. Recurse.

**Complexity:** O(n) time (with HashMap), O(n) space.

---

### 34. Binary Tree Zigzag Level Order

| Property | Value |
|---|---|
| **Pattern** | BFS + toggle direction |
| **Platform** | [LeetCode 103](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) |

**Description:** Return zigzag level order (alternating L→R, R→L).

**Solution Approach:** BFS with deque. Use a flag `leftToRight`. If true, add to end (normal). If false, add to front.

**Complexity:** O(n) time, O(n) space.

---

### 35. Kth Smallest Element in BST

| Property | Value |
|---|---|
| **Pattern** | Inorder (iterative) |
| **Platform** | [LeetCode 230](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) |

**Description:** Find the kth smallest element in a BST.

**Solution Approach:** Iterative inorder traversal. Stack-based. Decrement k at each visit. When k == 0, return current node value.

**Complexity:** O(h + k) time, O(h) space.

---

### 36. Serialize and Deserialize BST

| Property | Value |
|---|---|
| **Pattern** | Preorder + Queue |
| **Platform** | [LeetCode 449](https://leetcode.com/problems/serialize-and-deserialize-bst/) |

**Description:** Serialize BST to string and deserialize back.

**Solution Approach:** Preorder traversal with a marker (e.g., "#") for nulls. Deserialize: use queue of split values. Recursively build using bounds.

**Complexity:** O(n) time, O(n) space.

---

## Heaps (4 problems)

### 37. Merge k Sorted Lists

| Property | Value |
|---|---|
| **Pattern** | MinHeap |
| **Platform** | [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/) |

**Description:** Merge k sorted linked lists into one.

**Solution Approach:** MinHeap of ListNode (by value). Add all heads. Poll smallest, add its next. Continue until heap empty.

**Complexity:** O(n log k) time, O(k) space.

---

### 38. Find Median from Data Stream

| Property | Value |
|---|---|
| **Pattern** | Two Heaps |
| **Platform** | [LeetCode 295](https://leetcode.com/problems/find-median-from-data-stream/) |

**Description:** Continuously find median as numbers are added.

**Solution Approach:** MaxHeap for left half, MinHeap for right half. Maintain size balance (maxHeap has 0 or 1 more). If sizes differ by 2, rebalance.

**Complexity:** O(log n) per add, O(1) for median. O(n) space.

---

### 39. Top K Frequent Elements

| Property | Value |
|---|---|
| **Pattern** | Frequency map + Heap |
| **Platform** | [LeetCode 347](https://leetcode.com/problems/top-k-frequent-elements/) |

**Description:** Return k most frequent elements.

**Solution Approach:** Frequency map. MinHeap of size k (by frequency). If heap size < k, add. Else if freq > heap peek's freq, poll and add.

**Complexity:** O(n log k) time, O(n + k) space.

---

### 40. Kth Largest Element in an Array

| Property | Value |
|---|---|
| **Pattern** | QuickSelect / MinHeap |
| **Platform** | [LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/) |

**Description:** Find kth largest element in unsorted array.

**Solution Approach:** MinHeap of size k. Add elements. If heap size > k and new > peek, poll and add. Top is kth largest.

**Complexity:** O(n log k) time, O(k) space.

---

## Graphs (5 problems)

### 41. Clone Graph

| Property | Value |
|---|---|
| **Pattern** | DFS/BFS + HashMap |
| **Platform** | [LeetCode 133](https://leetcode.com/problems/clone-graph/) |

**Description:** Deep copy of an undirected connected graph.

**Solution Approach:** HashMap<Node, Node> for visited/cloned. DFS: clone node, recursively clone neighbors. Return from map if already cloned.

**Complexity:** O(V + E) time, O(V) space.

---

### 42. Course Schedule (Topological Sort)

| Property | Value |
|---|---|
| **Pattern** | Kahn's algorithm (BFS) / DFS |
| **Platform** | [LeetCode 207](https://leetcode.com/problems/course-schedule/) |

**Description:** Determine if all courses can be finished given prerequisites.

**Solution Approach:** Build adjacency list and indegree array. Kahn's: queue nodes with indegree 0. Decrement indegrees of neighbors. Count processed.

**Complexity:** O(V + E) time, O(V + E) space.

---

### 43. Number of Islands

| Property | Value |
|---|---|
| **Pattern** | DFS/BFS on grid |
| **Platform** | [LeetCode 200](https://leetcode.com/problems/number-of-islands/) |

**Description:** Count islands in a 2D grid (1 = land, 0 = water).

**Solution Approach:** Iterate grid. When '1' found, increment count, DFS to sink all connected '1's.

**Complexity:** O(m × n) time, O(m × n) space (call stack / queue).

---

### 44. Word Ladder

| Property | Value |
|---|---|
| **Pattern** | BFS (shortest path) |
| **Platform** | [LeetCode 127](https://leetcode.com/problems/word-ladder/) |

**Description:** Find shortest transformation sequence from beginWord to endWord.

**Solution Approach:** BFS. For each word, generate all possible next words by changing one letter. Use HashSet for word list. Track level/distance.

**Complexity:** O(m² × n) time, O(m × n) space (m = word length, n = word count).

---

### 45. Pacific Atlantic Water Flow

| Property | Value |
|---|---|
| **Pattern** | DFS from boundaries |
| **Platform** | [LeetCode 417](https://leetcode.com/problems/pacific-atlantic-water-flow/) |

**Description:** Find cells that can flow to both Pacific and Atlantic oceans.

**Solution Approach:** Two boolean grids. DFS from Pacific borders and Atlantic borders. Cells reachable from both are result.

**Complexity:** O(m × n) time, O(m × n) space.

---

## Backtracking (4 problems)

### 46. Subsets

| Property | Value |
|---|---|
| **Pattern** | Backtracking / Recursion |
| **Platform** | [LeetCode 78](https://leetcode.com/problems/subsets/) |

**Description:** Return all possible subsets (power set).

**Solution Approach:** Backtracking: at each index, either include or exclude element. Add current list to result at each step.

**Complexity:** O(n × 2ⁿ) time, O(n × 2ⁿ) space.

---

### 47. Permutations

| Property | Value |
|---|---|
| **Pattern** | Backtracking with swap |
| **Platform** | [LeetCode 46](https://leetcode.com/problems/permutations/) |

**Description:** Return all permutations of distinct integers.

**Solution Approach:** Swap-based backtracking: at each position, swap with each later index. Recurse, then swap back.

**Complexity:** O(n × n!) time, O(n) space excluding output.

---

### 48. Combination Sum

| Property | Value |
|---|---|
| **Pattern** | Backtracking with target |
| **Platform** | [LeetCode 39](https://leetcode.com/problems/combination-sum/) |

**Description:** Find all combinations that sum to target (unlimited use of same element).

**Solution Approach:** Backtracking: sort first. At each step, try current element, recurse with same index, subtract from target. Backtrack when target < 0 or == 0.

**Complexity:** O(2^(t/m)) time, O(t/m) space.

---

### 49. N-Queens

| Property | Value |
|---|---|
| **Pattern** | Backtracking with pruning |
| **Platform** | [LeetCode 51](https://leetcode.com/problems/n-queens/) |

**Description:** Place N queens on N×N board such that none attack each other.

**Solution Approach:** Place row by row. Track occupied columns and diagonals (two diagonals: row-col, row+col). Backtrack when conflict.

**Complexity:** O(n!) time, O(n) space.

---

## DP (5 problems)

### 50. Coin Change

| Property | Value |
|---|---|
| **Pattern** | Unbounded knapSack (DP) |
| **Platform** | [LeetCode 322](https://leetcode.com/problems/coin-change/) |

**Description:** Find fewest number of coins to make a given amount.

**Solution Approach:** DP array of size amount+1, initialized to amount+1. DP[0] = 0. For each amount, for each coin: dp[i] = min(dp[i], dp[i-coin] + 1).

**Complexity:** O(amount × n) time, O(amount) space.

---

### 51. Longest Increasing Subsequence

| Property | Value |
|---|---|
| **Pattern** | DP + Binary Search |
| **Platform** | [LeetCode 300](https://leetcode.com/problems/longest-increasing-subsequence/) |

**Description:** Find length of LIS.

**Solution Approach (O(n log n)):** Maintain list `tails` where tails[i] = smallest ending value for subsequence of length i+1. Binary search to place each num.

**Complexity:** O(n log n) time, O(n) space.

---

### 52. Edit Distance

| Property | Value |
|---|---|
| **Pattern** | 2D DP |
| **Platform** | [LeetCode 72](https://leetcode.com/problems/edit-distance/) |

**Description:** Minimum number of operations (insert, delete, replace) to convert word1 to word2.

**Solution Approach:** 2D DP table. dp[i][j] = min operations for word1[0..i-1] → word2[0..j-1]. If chars equal, copy diagonal. Else 1 + min of insert/delete/replace.

**Complexity:** O(m × n) time, O(m × n) space (can be optimized to O(min(m,n))).

---

### 53. 0/1 KnapSack

| Property | Value |
|---|---|
| **Pattern** | 2D DP |
| **Platform** | [GeeksforGeeks](https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/) |

**Description:** Maximize value with weight constraint — each item used once.

**Solution Approach:** 2D DP: dp[i][w] = max value using first i items with weight ≤ w. dp[i][w] = max(dp[i-1][w], val[i-1] + dp[i-1][w - wt[i-1]]).

**Complexity:** O(n × W) time, O(n × W) space (can be 1D).

---

### 54. House Robber

| Property | Value |
|---|---|
| **Pattern** | 1D DP |
| **Platform** | [LeetCode 198](https://leetcode.com/problems/house-robber/) |

**Description:** Max money you can rob without robbing adjacent houses.

**Solution Approach:** dp[i] = max(dp[i-1], dp[i-2] + nums[i]). Optimize to O(1) space with two variables.

**Complexity:** O(n) time, O(1) space.

---

## Quick Reference Table

| # | Problem | Pattern | Time | Space |
|---|---|---|---|---|
| 1 | Subarray Sum K | Prefix+HashMap | O(n) | O(n) |
| 2 | Product Except Self | Prefix/Suffix | O(n) | O(1) |
| 3 | Spiral Matrix | Layer sim | O(mn) | O(1) |
| 4 | 3Sum | Sort+2ptr | O(n²) | O(1) |
| 5 | Sort Colors | 3 ptr | O(n) | O(1) |
| 6 | Set Matrix Zeroes | Markers | O(mn) | O(1) |
| 7 | Rotate Image | Transpose+Rev | O(n²) | O(1) |
| 8 | Merge Intervals | Sort | O(n log n) | O(n) |
| 9 | Find Duplicate | Floyd | O(n) | O(1) |
| 10 | Container Water | 2 ptr | O(n) | O(1) |
| 11 | Longest Substr w/o Repeat | Sliding Window | O(n) | O(m) |
| 12 | Group Anagrams | HashMap | O(nk log k) | O(nk) |
| 13 | Longest Palindromic | Expand center | O(n²) | O(1) |
| 14 | atoi | Parse | O(n) | O(1) |
| 15 | KMP | LPS array | O(n+m) | O(m) |
| 16 | Zigzag Conversion | Row sim | O(n) | O(n) |
| 17 | Compare Versions | Split + parse | O(n+m) | O(n+m) |
| 18 | Simplify Path | Stack | O(n) | O(n) |
| 19 | Remove Nth Node | Fast/Slow gap | O(n) | O(1) |
| 20 | Add Two Numbers | Math | O(n+m) | O(1) |
| 21 | Reverse LL II | Partial rev | O(n) | O(1) |
| 22 | Odd Even LL | Rearrange | O(n) | O(1) |
| 23 | Intersection LL | 2 ptr | O(n+m) | O(1) |
| 24 | Palindrome LL | Mid+Rev | O(n) | O(1) |
| 25 | Largest Rectangle | Monotonic Stack | O(n) | O(n) |
| 26 | Daily Temperatures | Monotonic Stack | O(n) | O(n) |
| 27 | Min Stack | Design | O(1) | O(n) |
| 28 | Stack w/ Queues | Design | O(n) push | O(n) |
| 29 | Inorder Iterative | Stack | O(n) | O(n) |
| 30 | LCA BST | BST property | O(h) | O(1) |
| 31 | Level Order | BFS | O(n) | O(n) |
| 32 | Validate BST | Range | O(n) | O(h) |
| 33 | Build Tree Pre+In | D&C | O(n) | O(n) |
| 34 | Zigzag Level | BFS | O(n) | O(n) |
| 35 | Kth Smallest | Inorder | O(h+k) | O(h) |
| 36 | Serialize BST | Preorder | O(n) | O(n) |
| 37 | Merge K Sorted | MinHeap | O(n log k) | O(k) |
| 38 | Median Stream | 2 Heaps | O(log n) | O(n) |
| 39 | Top K Frequent | Heap | O(n log k) | O(n+k) |
| 40 | Kth Largest | QuickSelect/Heap | O(n log k) | O(k) |
| 41 | Clone Graph | DFS+Map | O(V+E) | O(V) |
| 42 | Course Schedule | Kahn's | O(V+E) | O(V+E) |
| 43 | Number of Islands | DFS grid | O(mn) | O(mn) |
| 44 | Word Ladder | BFS | O(m²n) | O(mn) |
| 45 | Water Flow | Boundary DFS | O(mn) | O(mn) |
| 46 | Subsets | Backtrack | O(n2ⁿ) | O(n2ⁿ) |
| 47 | Permutations | Swap BT | O(n!) | O(n) |
| 48 | Combination Sum | BT | O(2^(t/m)) | O(t/m) |
| 49 | N-Queens | BT+prune | O(n!) | O(n) |
| 50 | Coin Change | DP | O(amount×n) | O(amount) |
| 51 | LIS | DP+BS | O(n log n) | O(n) |
| 52 | Edit Distance | 2D DP | O(mn) | O(mn) |
| 53 | 0/1 KnapSack | 2D DP | O(nW) | O(nW) |
| 54 | House Robber | 1D DP | O(n) | O(1) |

---

## Study Strategy for Intermediate Problems

1. **Attempt each problem for 30-45 min** before looking at solution
2. **Identify the pattern** first — this decides the approach
3. **Code the brute force** before optimal
4. **Dry run** with examples and edge cases
5. **Compare your solution** with the official one on LeetCode
6. **Re-solve** after 3 days and again after 7 days (spaced repetition)
7. **Group by pattern** — solve multiple problems with same pattern in a row
8. **Track time taken** — if >45 min consistently, you need more pattern review
9. **Explain out loud** — simulate interview conditions
10. **Focus on patterns, not problems** — the pattern transfers across problems
