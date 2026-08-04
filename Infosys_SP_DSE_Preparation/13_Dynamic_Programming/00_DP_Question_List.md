# Dynamic Programming — Master Question List (280+ Problems)

> **Purpose:** Complete catalog of every DP problem for Infosys SP DSE (L1/L2/L3). Review this list, confirm quantity, then solutions will be added with full explanations.
> **How to use:** Problems are grouped by pattern. Each row: problem name, difficulty, one-line description, and the DP sub-pattern it tests.

---

## 1. 1D Linear DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 1 | Climbing Stairs (LC #70) | Easy | Count distinct ways to reach step n climbing 1 or 2 steps at a time | Fibonacci-style 1D |
| 2 | Climbing Stairs (3 Steps) (LC #746) | Easy | Count ways with 1, 2, or 3 steps allowed | Extended Fibonacci |
| 3 | Min Cost Climbing Stairs (LC #746) | Easy | Given cost per step, find minimum cost to reach the top starting at index 0 or 1 | 1D DP with costs |
| 4 | House Robber (LC #198) | Medium | Rob non-adjacent houses to maximize stolen money | Non-adjacent selection |
| 5 | House Robber II (LC #213) | Medium | Circular arrangement of houses, first and last are adjacent | Circular 1D DP |
| 6 | House Robber III (LC #337) | Medium | Houses arranged in a binary tree, no two adjacent (parent-child) connected | Tree DP |
| 7 | Maximum Subarray / Kadane (LC #53) | Medium | Find contiguous subarray with maximum sum | Kadane's 1D |
| 8 | Maximum Sum Circular Subarray (LC #918) | Medium | Maximum subarray sum in a circular array | Kadane + prefix/suffix |
| 9 | Maximum Product Subarray (LC #152) | Medium | Find contiguous subarray with maximum product (track min too) | Kadane variant |
| 10 | Maximum Sum of Non-Adjacent Elements | Easy | Pick elements with no two adjacent to maximize sum | Non-adjacent selection |
| 11 | Maximum Sum with No Two Non-Adjacent (Delete and Earn) (LC #740) | Medium | Delete an element to earn its value, cannot keep adjacent | Cooldown pattern |
| 12 | Decode Ways (LC #91) | Medium | Count number of ways to decode a digit string (1-26 maps to A-Z) | Conditional 1D |
| 13 | Decode Ways II (LC #639) | Hard | Decode with wildcard '*' in the digit string | Conditional with branching |
| 14 | Paint Fence (LC #276) | Medium | Paint n posts with k colors, no more than 2 adjacent same | same/diff tracking |
| 15 | Paint House I | Medium | Paint n houses with 3 colors, no two adjacent same, minimize cost | 1D with 3 states |
| 16 | Paint House II (LC #265) | Medium | Same as Paint House I but with k colors, O(nk) solution | 1D with k states |
| 17 | Paint House III (LC #1473) | Hard | Paint houses with m colors, target groups of same color | 1D + bitmask/grouping |
| 18 | Maximum Alternating Subsequence Sum (LC #1911) | Medium | Pick alternating signs (+/-) subsequence to maximize sum | Sign-flip 1D |
| 19 | Longest Alternating Subsequence | Medium | Longest subsequence where elements alternate up/down | Alternating 1D |
| 20 | Longest Bitonic Subsequence | Medium | Longest subsequence that first increases then decreases | LIS forward + backward |
| 21 | Maximum Length of Pair Chain (LC #646) | Medium | Chain pairs where second of one < first of next, maximize chain length | Greedy + 1D LIS |
| 22 | Jump Game (LC #55) | Medium | Can you reach the last index from index 0 with given max jumps | Reachability DP |
| 23 | Jump Game II (LC #45) | Medium | Minimum jumps to reach the last index | BFS / Greedy + DP |
| 24 | Jump Game III (LC #1306) | Medium | Can reach index 0 from index start by jumping arr[i] left or right | BFS + visited |
| 25 | Jump Game IV (LC #1289) | Hard | Minimum jumps with same-value teleport on array | BFS + deque |
| 26 | Jump Game V (LC #1377) | Hard | Maximum index you can reach with limited jump length and height constraints | DFS + memo |
| 27 | Jump Game VI (LC #1696) | Medium | Maximum score with k-distance sliding window jumps | Monotonic deque DP |
| 28 | Stone Game I (LC #877) | Medium | Two players pick from ends of array, Alice wins (parity argument) | Game theory 1D |
| 29 | Stone Game II (LC #1140) | Medium | Pick 1 to 2x previous stones from left, maximize your stones | Suffix sum game DP |
| 30 | Stone Game III (LC #1406) | Medium | Pick 1/2/3 from front, maximize difference, return winner | Reverse DP game |
| 31 | Stone Game IV (LC #1510) | Hard | Two players take n stones, remove perfect square count | Number theory game |
| 32 | Predict the Winner (LC #486) | Medium | Two players pick from ends, does Player 1 score >= Player 2 | Minimax DP |
| 33 | Optimal Strategy for a Game | Medium | Two players pick from ends, maximize your total value | Minimax 1D |
| 34 | Arithmetic Slices I (LC #413) | Medium | Count arithmetic subarrays (length >= 3) | 1D counting |
| 35 | Arithmetic Slices II (LC #446) | Hard | Count arithmetic subsequences (not contiguous) | 1D + hash map |
| 36 | Maximum Height by Stacking Cuboids (LC #1691) | Hard | Stack cuboids where each base fits inside the one below | 3D LIS |
| 37 | Longest Subarray of 1s After Deleting One Element (LC #1493) | Medium | Longest subarray of 1s after deleting at most one element | Sliding window / 1D |
| 38 | Maximum Subarray Sum with One Deletion (LC #1186) | Medium | Maximum subarray sum allowing exactly one deletion | Two-state 1D |
| 39 | Longest Subarray with Sum K | Medium | Longest subarray summing to exactly K | Prefix sum + map |
| 40 | Count Subarrays with Sum K | Medium | Count subarrays summing to exactly K | Prefix sum + map |
| 41 | Maximum Sum of Three Non-Overlapping Subarrays (LC #689) | Hard | Three non-overlapping subarrays of size k maximizing total sum | 1D prefix + suffix |
| 42 | Maximum Sum of Two Non-Overlapping Subarrays (LC #1031) | Medium | Two non-overlapping subarrays maximizing sum of firstLen + secondLen | Prefix + suffix scan |
| 43 | Maximum Subarray Length with Sum K | Medium | Find longest subarray with sum exactly K | Prefix sum + map |

---

## 2. Two Sequence / 2D String DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 44 | Longest Common Subsequence (LC #1143) | Medium | Find length of longest common subsequence of two strings | 2D string match |
| 45 | LCS — Reconstruct the Actual Subsequence | Medium | Return the actual LCS string, not just length | 2D + backtrack |
| 46 | Longest Common Substring (LC #718) | Medium | Find length of longest common contiguous substring | 2D contiguous match |
| 47 | Edit Distance / Levenshtein (LC #72) | Medium | Minimum insert/delete/replace operations to convert word1 to word2 | 2D string transform |
| 48 | Edit Distance with Operations Listed | Hard | Same as edit distance but return the list of operations performed | 2D + backtrack |
| 49 | Distinct Subsequences (LC #115) | Hard | Count distinct subsequences of s that equal t | 2D counting |
| 50 | Distinct Subsequences II (LC #940) | Hard | Count distinct non-empty subsequences of a string | 1D + hash map |
| 51 | Interleaving String (LC #97) | Medium | Is s3 an interleaving of s1 and s2 preserving relative order | 2D boolean DP |
| 52 | Shortest Common Supersequence (LC #1092) | Hard | Shortest string that has both s1 and s2 as subsequences | 2D + LCS backtrack |
| 53 | Is Subsequence (LC #392) | Easy | Is t a subsequence of s | Two-pointer / DP |
| 54 | Longest Repeating Subsequence (LC #647 variant) | Medium | Longest subsequence that appears at least twice (positions differ) | 2D with index constraint |
| 55 | Longest Palindromic Subsequence (LC #516) | Medium | Length of longest palindromic subsequence in a string | 2D interval |
| 56 | Longest Palindromic Substring (LC #5) | Medium | Find the longest palindromic substring (contiguous) | 2D / expand center |
| 57 | Count of Palindromic Substrings (LC #647) | Medium | Count all palindromic substrings | Expand around center |
| 58 | Palindrome Partitioning (LC #131) | Medium | Partition string so every substring is a palindrome, return all partitions | 2D + backtracking |
| 59 | Palindrome Partitioning II (LC #132) | Hard | Minimum cuts to partition string into all-palindrome substrings | 2D + 1D optimization |
| 60 | Palindrome Partitioning III (LC #1278) | Hard | Partition into k palindromes with minimum changes | 2D DP + palindrome cost |
| 61 | Minimum Insertions to Make Palindrome (LC #1312) | Medium | Minimum insertions to make string a palindrome | 2D (related to LPS) |
| 62 | Minimum Deletions to Make Palindrome | Medium | Minimum deletions to make string a palindrome | 2D (LCS with reverse) |
| 63 | Minimum Number of Deletions and Insertions (LC #1546) | Medium | Convert str1 to str2 with minimum insertions + deletions | 2D (LCS-based) |
| 64 | One Edit Distance (LC #161) | Medium | Check if two strings are exactly one edit apart | 2D / simplified |
| 65 | Longest Uncommon Subsequence I (LC #521) | Easy | Longest substring that is not a subsequence of the other | String comparison |
| 66 | Longest Uncommon Subsequence II (LC #522) | Hard | Find longest uncommon subsequence among a list of strings | Subsequence checking |
| 67 | Wildcard Matching (LC #44) | Hard | Pattern matching with '?' (single) and '*' (any sequence) | 2D boolean DP |
| 68 | Regular Expression Matching (LC #10) | Hard | Pattern matching with '.' (any single) and '*' (zero or more) | 2D boolean DP |
| 69 | String Matching with Wildcards (KMP + DP) | Hard | Extended pattern matching combining KMP and DP | Hybrid |
| 70 | Valid Parentheses String (LC #678) | Medium | Check if string with '(' ')' '*' is valid (star = open/close) | Range DP / greedy |
| 71 | Minimum Add to Make Parentheses Valid (LC #921) | Easy | Minimum insertions to make parentheses valid | Greedy / 1D |
| 72 | Minimum Number of Swaps to Make String Balanced (LC #1249) | Medium | Minimum swaps to balance parentheses | Greedy / counting |
| 73 | Generate Parentheses (LC #22) | Medium | Generate all valid combinations of n pairs of parentheses | Backtracking |

---

## 3. 2D Grid DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 74 | Unique Paths (LC #62) | Medium | Count distinct paths from top-left to bottom-right in m×n grid | 2D grid count |
| 75 | Unique Paths with Obstacles (LC #63) | Medium | Count paths with blocked cells (obstacles) | 2D grid with blocking |
| 76 | Minimum Path Sum (LC #64) | Medium | Find path from top-left to bottom-right minimizing sum of cell values | 2D grid min |
| 77 | Dungeon Game (LC #174) | Hard | Knight must reach princess with minimum initial HP, negative/positive rooms | 2D reverse DP |
| 78 | Triangle (LC #120) | Medium | Minimum path sum from top to bottom of a triangle | 2D DP bottom-up |
| 79 | Maximal Square (LC #221) | Medium | Largest square containing only 1s in a binary matrix | 2D prefix square |
| 80 | Maximal Rectangle (LC #85) | Hard | Largest rectangle containing only 1s in a binary matrix | 2D + histogram |
| 81 | Count Square Submatrices with All Ones (LC #1277) | Medium | Count all-square submatrices of 1s in a binary matrix | 2D prefix counting |
| 82 | Cherry Pickup (LC #741) | Hard | Two paths collect cherries from top-left to bottom-right, maximize total | 2D state DP |
| 83 | Cherry Pickup II (LC #1463) | Hard | Two robots collect cherries simultaneously in a grid | 3D state DP |
| 84 | Unique Paths III (LC #980) | Hard | Count paths visiting every non-obstacle cell exactly once | Backtracking + memo |
| 85 | Paths with Maximum Gold (LC #1219) | Medium | Collect maximum gold in a grid, can move to adjacent cells | DFS + memo |
| 86 | Grid Minimum Falling Path Sum (LC #931) | Medium | Minimum sum path from any cell in first row to any cell in last row | 2D min-path |
| 87 | Minimum Falling Path Sum II (LC #1289) | Hard | Same but cannot use same column as previous row | 2D with column constraint |
| 88 | Unique Paths with Teleporters | Medium | Grid with teleport cells that jump to other positions | 2D + teleport transitions |
| 89 | Maximum Path Sum in Grid from Top to Bottom | Medium | Find max sum path from top row to bottom row | 2D DP |
| 90 | Number of Ways to Reach a Position After Exactly k Steps | Medium | Count ways on number line with exactly k steps of +1 or -1 | 2D DP (position × steps) |
| 91 | Knight Dialer (LC #935) | Medium | Count ways a knight can make exactly n-1 moves on a phone keypad | 2D (position × moves) |
| 92 | Out of Boundary Paths (LC #576) | Medium | Count ways to move ball out of grid in exactly m moves | 3D DP (row × col × moves) |
| 93 | Maximize Score After N Operations (LC #1799) | Hard | Pick pairs to maximize gcd-based scoring over n operations | Bitmask DP |
| 94 | Number of Digit One (LC #233) | Hard | Count digit '1' appearing in all numbers from 0 to n | Digit DP |
| 95 | Range Sum Query 2D — Immutable (LC #304) | Medium | Precompute and query sum of any submatrix | 2D prefix sum |

---

## 4. 0/1 Knapsack Family

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 96 | 0/1 Knapsack | Medium | Given weights and values, maximize value within weight capacity, each item used once | 2D or 1D rolling |
| 97 | Subset Sum (LC #416 variant) | Medium | Check if array has a subset that sums to target | 1D boolean DP |
| 98 | Equal Subset Sum Partition (LC #416) | Medium | Partition array into two subsets with equal sum | Subset sum / 2D |
| 99 | Count Subsets with Given Sum | Medium | Count subsets that sum to exactly target | 1D counting DP |
| 100 | Minimum Subset Sum Difference | Medium | Split array into two subsets minimizing the difference of their sums | 1D DP |
| 101 | Target Sum (LC #494) | Medium | Assign +/- to each number to reach target, count ways | Signed subset sum |
| 102 | Last Stone Weight II (LC #1049) | Medium | Smash stones to minimize the last remaining stone weight | Subset sum view |
| 103 | Partition Array into Two Arrays to Minimize Sum Difference (LC #2035) | Hard | Find minimum absolute difference of two partition sums | 1D DP |
| 104 | Count of Subsets with Given Difference | Medium | Count ways to split into two subsets with difference = target | Subset sum + adjustment |
| 105 | Ones and Zeroes (LC #474) | Medium | Largest subset of binary strings fitting m zeros and n ones | 2D knapsack |
| 106 | Bounded Knapsack | Medium | Each item has a limited count, maximize value | Multiple copies DP |
| 107 | Bags of Tokens (LC #948) | Medium | Maximize score by playing tokens face-up (spend power) or face-down (gain power) | Greedy + DP |
| 108 | Partition Equal Subset Sum with Exactly K Subsets (LC #698) | Hard | Check if array can be partitioned into k subsets of equal sum | Backtracking + memo |
| 109 | Minimum Cost to Buy N Items | Medium | Buy n items with varying costs and discounts | Knapsack variant |
| 110 | Maximum Profit in Job Scheduling (LC #1235) | Hard | Schedule non-overlapping jobs to maximize total profit | Weighted job scheduling |
| 111 | Coin Piles Minimum | Medium | Remove coin piles to minimize remaining coins summing to K | Subset selection |
| 112 | Form Array Using Subsequence Sum | Medium | Check if target array can be formed from subset sums | Subset DP |

---

## 5. Unbounded Knapsack Family

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 113 | Unbounded Knapsack | Medium | Each item can be used unlimited times, maximize value | 1D forward-iterate |
| 114 | Coin Change — Minimum Coins (LC #322) | Medium | Fewest coins to make amount (unlimited supply) | Unbounded min |
| 115 | Coin Change II — Number of Ways (LC #518) | Medium | Count combinations of coins to make amount | Unbounded count |
| 116 | Rod Cutting | Medium | Cut a rod of length n to maximize total price | Unbounded knapsack |
| 117 | Maximum Ribbon Cut (LC #1449) | Medium | Cut ribbon into pieces of given lengths to maximize number of pieces | Unbounded max count |
| 118 | Combination Sum IV (LC #377) | Medium | Count ordered sequences that sum to target (permutations, not combinations) | Unbounded count (ordered) |
| 119 | Combination Sum (LC #39) | Medium | Find all unique combinations summing to target (unlimited reuse) | Unbounded + backtracking |
| 120 | Combination Sum II (LC #40) | Medium | Find combinations summing to target (each element used once) | 0/1 knapsack + backtracking |
| 121 | Combination Sum III (LC #216) | Medium | Find all combinations of k numbers (1-9) summing to n | Constrained combination |
| 122 | Integer Break (LC #343) | Medium | Break n into sum of integers to maximize product | Unbounded knapsack |
| 123 | Perfect Squares (LC #279) | Medium | Minimum number of perfect squares that sum to n | Unbounded min |
| 124 | Minimum Cost For Tickets (LC #983) | Medium | Buy travel tickets (1/7/30 day passes) to cover all days at minimum cost | Unbounded with days |
| 125 | Ways to Make a Fair Array (LC #1616) | Medium | Remove one element to make alternating sum zero | Prefix/suffix |
| 126 | Number of Ways to Split a String | Medium | Split string into 3 non-empty parts with equal number of 1s | Counting / prefix |
| 127 | Minimum Number of Coins for Change | Medium | Minimum coins to make change for a given amount (various coin values) | Standard coin change |

---

## 6. Interval DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 128 | Matrix Chain Multiplication | Medium | Find optimal parenthesization to minimize scalar multiplications | Classic interval DP |
| 129 | Burst Balloons (LC #312) | Hard | Burst balloons to maximize coins, coin = left × balloon × right | Interval DP (last burst) |
| 130 | Minimum Cost to Cut a Stick (LC #1547) | Hard | Cut stick at given positions to minimize total cost | Interval DP |
| 131 | Boolean Parenthesization | Hard | Count ways to parenthesize boolean expression to get True | Interval counting |
| 132 | Optimal Binary Search Tree | Medium | Build BST with minimum expected search cost for given key frequencies | Interval DP |
| 133 | Minimum Score Triangulation (LC #1039) | Medium | Triangulate polygon to minimize sum of triangle values | Interval DP |
| 134 | Strange Printer (LC #664) | Hard | Print string with minimum operations (prints same character continuously) | Interval DP |
| 135 | Remove Boxes (LC #546) | Hard | Remove boxes to maximize points (consecutive same-color = points²) | Interval + color state |
| 136 | Palindrome Partitioning II (LC #132) | Hard | Minimum cuts to partition string into palindromes | 1D + palindrome check |
| 137 | Egg Dropping (LC #887) | Hard | Find critical floor with minimum attempts (k eggs, n floors) | Interval / binary search DP |
| 138 | Egg Drop with 2 Eggs and n Floors (LC #1884) | Medium | 2 eggs, n floors, minimize worst-case attempts | Math + 1D DP |
| 139 | Minimum Cost to Merge Stones (LC #1000) | Hard | Merge piles into one pile at minimum cost (merge k adjacent at cost sum) | Interval + k-partition |
| 140 | Minimum Window Substring (LC #76) | Hard | Find minimum window in s containing all characters of t | Sliding window (not DP) |
| 141 | Maximal Area in Histogram (LC #84) | Hard | Largest rectangle in a histogram | Monotonic stack |
| 142 | Decode String (LC #394) | Medium | Decode encoded string like "3[a2[c]]" | Stack / DP |
| 143 | Different Ways to Add Parentheses (LC #241) | Medium | Compute all possible results from adding parentheses to expression | Divide and conquer |

---

## 7. Longest Increasing Subsequence Family

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 144 | Longest Increasing Subsequence O(n²) (LC #300) | Medium | Length of longest strictly increasing subsequence | 1D DP nested loop |
| 145 | Longest Increasing Subsequence O(n log n) (LC #300) | Medium | LIS with patience sorting / binary search | Binary search + piles |
| 146 | Number of Longest Increasing Subsequence (LC #673) | Medium | Count LIS of maximum length | 1D DP + count |
| 147 | Longest Increasing Subsequence — Reconstruct Actual Subsequence | Medium | Return the actual LIS, not just length | DP + backtrack |
| 148 | Longest Non-Decreasing Subsequence | Medium | LIS allowing equal consecutive elements | Modified binary search |
| 149 | Longest Decreasing Subsequence | Medium | Length of longest strictly decreasing subsequence | Reverse LIS |
| 150 | Longest Alternating Subsequence | Medium | Longest subsequence with up-down pattern | Greedy / DP |
| 151 | Maximum Length of Pair Chain (LC #646) | Medium | Longest chain where each pair's second < next pair's first | Sort + LIS |
| 152 | Russian Doll Envelopes (LC #354) | Hard | Envelope nesting (width and height), maximize count | 2D LIS sort + binary search |
| 153 | Longest Chain of Pairs (LC #646 variant) | Medium | Maximum chain length from pairs | Sort + greedy / LIS |
| 154 | Maximum Sum Increasing Subsequence | Medium | Maximum sum of an increasing subsequence | 1D DP with value sum |
| 155 | Longest Increasing Subsequence II (LC #2407) | Hard | LIS where adjacent elements differ by at most 1 | Segment tree + DP |
| 156 | Find the Longest Valid Obstacle Course (LC #1964) | Hard | Longest non-decreasing sequence in obstacle array | Patience sort variant |
| 157 | Longest Plindrome Subsequence (LC #516) | Medium | Length of longest palindromic subsequence | LCS with reverse |
| 158 | Longest Common Subsequence of Two Strings | Medium | Classic LCS length | 2D DP |
| 159 | Number of LIS with Maximum Length (LC #673) | Medium | Count of longest increasing subsequences | DP + count |
| 160 | Wiggle Subsequence (LC #280) | Medium | Longest subsequence where differences alternate between positive and negative | Wiggle DP |
| 161 | Minimum Operations to Make Array Increasing | Medium | Minimum increments to make array strictly increasing | Greedy / DP |
| 162 | Longest Mountain in Array (LC #845) | Medium | Longest subarray that first increases then decreases | LIS forward + backward |
| 163 | Number of Longest Increasing Subsequences (N-ary) | Hard | LIS on N-dimensional points | K-dimensional LIS |

---

## 8. Subarray / Substring DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 164 | Longest Valid Parentheses (LC #32) | Hard | Length of longest valid (well-formed) parentheses substring | 1D stack / DP |
| 165 | Maximum Size Rectangle of All 1s (LC #85) | Hard | Largest rectangle of 1s in a binary matrix | 2D + histogram |
| 166 | Maximum Sum Rectangle (Maximum Sum Submatrix) | Hard | Find rectangle in 2D matrix with maximum sum | Kadane + columns |
| 167 | Maximum Subarray with At Most K Distinct Elements | Medium | Longest subarray with at most K distinct elements | Sliding window |
| 168 | Longest Substring with At Most K Repeating Characters (LC #395) | Medium | Longest substring where each char repeats at most K times | Divide and conquer |
| 169 | Longest Substring with At Most K Distinct Characters | Medium | Longest substring with at most K distinct characters | Sliding window + map |
| 170 | Minimum Window Substring (LC #76) | Hard | Smallest substring containing all characters of pattern | Sliding window |
| 171 | Longest Substring Without Repeating Characters (LC #3) | Medium | Length of longest substring without duplicate characters | Sliding window + set |
| 172 | Longest Repeating Character Replacement (LC #424) | Medium | Maximum window with at most K replacements to make all same | Sliding window |
| 173 | Subarray Product Less Than K (LC #713) | Medium | Count subarrays where product of elements is less than k | Sliding window |
| 174 | Maximum Product Subarray (LC #152) | Medium | Find contiguous subarray with maximum product | 1D Kadane variant |
| 175 | Count Subarrays with Given XOR | Medium | Count subarrays where XOR equals k | Prefix XOR + map |
| 176 | Count Subarrays with Equal Number of 0s and 1s | Medium | Maximum length subarray with equal 0s and 1s | Prefix sum + map |
| 177 | Continuous Subarray Sum (LC #523) | Medium | Check if subarray of length >= 2 sums to multiple of k | Prefix mod + map |

---

## 9. Tree DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 178 | Diameter of Binary Tree (LC #543) | Easy | Longest path between any two nodes (edge count) | Tree DP + height |
| 179 | Diameter of N-ary Tree (LC #1522) | Medium | Same for N-ary tree | Tree DP generalized |
| 180 | Binary Tree Maximum Path Sum (LC #124) | Hard | Maximum path sum where path can start/end at any node | Global max + DFS |
| 181 | Maximum Path Sum Between Two Leaf Nodes | Medium | Maximum path sum from leaf to leaf | DFS + leaf tracking |
| 182 | House Robber III (LC #337) | Medium | Rob tree nodes, no two connected nodes | Tree DP (rob/skip) |
| 183 | House Robber IV (LC #2002) | Medium | Minimum max houses to rob among m houses with adjacency constraint | Binary search + DP |
| 184 | Minimum Vertex Cover (LC #1155 variant) | Hard | Minimum nodes to cover all edges in a binary tree | Tree DP (take/skip) |
| 185 | Maximum Independent Set in Tree | Hard | Maximum weight independent set in tree (no two adjacent) | Tree DP (take/skip) |
| 186 | Binary Tree Cameras (LC #968) | Hard | Minimum cameras to monitor all nodes (camera covers parent+children+grandchildren) | Tree DP (3 states) |
| 187 | Count Paths with Sum K (LC #437 variant) | Medium | Count paths in binary tree that sum to k | DFS + prefix sum |
| 188 | Path Sum III (LC #437) | Medium | Count paths that sum to target (paths don't need to go through root) | DFS + prefix sum |
| 189 | Delete Nodes and Return Forest (LC #1110) | Medium | Delete given nodes and return remaining forest as list of trees | DFS + postorder |
| 190 | Most Frequent Subtree Sum (LC #508) | Medium | Find the most frequent sum of subtree values | DFS + hash map |
| 191 | Tree Diameter (unrooted tree) (LC #1245 variant) | Medium | Diameter of a tree given as edge list | BFS × 2 / DP |
| 192 | Tree Coloring (LC #1443) | Medium | Color tree nodes with 2 colors, minimize path distances | Tree DP |
| 193 | Maximum Sum BST in Binary Tree (LC #1373) | Hard | Find maximum sum BST subtree | DFS + BST validation |
| 194 | Count Good Nodes in Binary Tree (LC #1448) | Medium | Count nodes where value >= all ancestors | DFS with max tracking |
| 195 | Low Common Ancestor of a Binary Tree (LC #236) | Medium | Find LCA of two nodes | DFS |
| 196 | Flatten Binary Tree to Linked List (LC #114) | Medium | Flatten tree to right-skewed linked list in-place | Reverse preorder |

---

## 10. Graph DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 197 | Bellman-Ford Algorithm | Medium | Shortest paths from source with negative edges (detect negative cycle) | Edge relaxation V-1 times |
| 198 | Floyd-Warshall Algorithm | Medium | All-pairs shortest paths in dense graph | 3D / 2D iterative |
| 199 | Longest Path in DAG | Medium | Find longest path in directed acyclic graph | Topo sort + DP |
| 200 | Critical Path / Project Scheduling | Medium | Earliest and latest start times, find critical activities | Topo sort + DP |
| 201 | DAG Shortest Paths | Medium | Single-source shortest paths in DAG (handles negative edges) | Topo sort + DP |
| 202 | Minimum Cost Path in DAG | Medium | Minimum cost path from source to destination in weighted DAG | Topo sort + DP |
| 203 | Word Ladder (LC #127) | Hard | Minimum number of transformations from beginWord to endWord | BFS + memo |
| 204 | Alien Dictionary (LC #269) | Hard | Reconstruct word ordering from sorted dictionary | Topo sort |
| 205 | Course Schedule (LC #207) | Medium | Check if all courses can be finished (cycle detection in DAG) | Topo sort |
| 206 | Course Schedule II (LC #210) | Medium | Return ordering of courses to finish all prerequisites | Topo sort |
| 207 | Number of Ways to Arrive at Destination (LC #1976) | Hard | Count shortest paths in weighted undirected graph | Dijkstra + count DP |
| 208 | Path with Maximum Probability (LC #1514) | Medium | Maximum probability path from source to destination | Modified Dijkstra |
| 209 | Network Delay Time (LC #743) | Medium | Minimum time for signal to reach all nodes | Dijkstra |
| 210 | Shortest Path in Binary Matrix (LC #1091) | Medium | Shortest path in 8-directional grid | BFS |
| 211 | Cheapest Flights Within K Stops (LC #787) | Medium | Cheapest price from src to dst with at most k stops | Bellman-Ford limited / BFS |

---

## 11. Bitmask DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 212 | Traveling Salesman Problem (TSP) | Hard | Visit all cities exactly once, return to start with minimum cost | dp[mask][last] |
| 213 | Shortest Hamiltonian Path | Hard | Visit all nodes exactly once with minimum total edge weight | dp[mask][last] |
| 214 | Shortest Hamiltonian Cycle | Hard | TSP returning to start with minimum cost | dp[mask][last] |
| 215 | Assignment Problem | Medium | Assign n workers to n jobs at minimum total cost | dp[mask] bitmask |
| 216 | Hamiltonian Path — Count All | Medium | Count total Hamiltonian paths in a graph | dp[mask][last] count |
| 217 | Maximum Weight Independent Set in Graph | Hard | Maximum weight set of non-adjacent nodes | dp[mask] with adjacency |
| 218 | Scheduling with Deadlines (Bitmask) | Hard | Schedule tasks with deadlines and profits to maximize profit | dp[mask] + deadlines |
| 219 | Minimum Cost to Hire Workers (Bitmask) | Hard | Assign workers to tasks with minimum cost | dp[mask] |
| 220 | Partition to K Equal Sum Subsets (LC #698) | Hard | Check if array can be split into k subsets with equal sum | dp[mask] or recursion |
| 221 | Fair Candy Swap (LC #888) | Medium | Find swap to make candy totals equal | Set + math |
| 222 | Maximum AND of Two Subsets | Medium | Split array into two subsets, maximize AND of their sums | Bitmask enumeration |
| 223 | Number of Ways to Wear Different Hats (LC #1434) | Hard | Assign 4 types of hats to 4 people such that each person gets a unique hat | dp[mask][hat] |
| 224 | Minimum Number of Visited Cells in a Matrix (LC #2617) | Hard | Minimum cells visited to reach bottom-right moving by matrix values | BFS + memo |
| 225 | Maximum Score from Performing Multiplication Operations (LC #1770) | Hard | Pick left/right elements from nums array to maximize multiplier score | dp[i][left_count] |

---

## 12. Digit DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 226 | Count Numbers with Digit Sum = Target | Medium | Count numbers in range [1,n] whose digit sum equals target | Digit DP with sum state |
| 227 | Count Numbers with No Consecutive 1s | Medium | Count numbers in [1,n] with no two consecutive 1 bits | Digit DP with last digit |
| 228 | Number of Digit One (LC #233) | Hard | Count total occurrences of digit 1 in all numbers from 0 to n | Digit DP |
| 229 | Non-negative Integers without Consecutive Ones (LC #600) | Medium | Count numbers in [0,n] with no consecutive 1s in binary | Digit DP |
| 230 | Count Integers with Digit Sum Equal to Target in Range | Medium | Count integers in [low,high] with digit sum = target | Digit DP (range) |
| 231 | Numbers At Most N Given Digit Set (LC #902) | Hard | Count numbers ≤ n using only given digits | Digit DP |
| 232 | Count Special Numbers (LC #2376) | Hard | Count positive integers with unique digits in range [1,n] | Digit DP + permutation |
| 233 | At Most K Digits / At Most K Swaps | Medium | Optimize number after at most k swaps of adjacent digits | Digit DP + greedy |
| 234 | Find All Good Numbers in Range | Medium | Numbers in range whose digit sum is divisible by k | Digit DP |
| 235 | Generate All Numbers with Digit Sum S | Easy | List all numbers in [1,n] whose digits sum to S | Recursive generation |

---

## 13. Game Theory DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 236 | Stone Game I (LC #877) | Medium | Two players pick from ends, does Player 1 always win | Parity / minimax |
| 237 | Stone Game II (LC #1140) | Medium | Pick 1 to 2M stones from left, maximize your stones | Suffix + minimax |
| 238 | Stone Game III (LC #1406) | Medium | Pick 1/2/3 from front, return winner by score difference | Reverse minimax |
| 239 | Stone Game IV (LC #1510) | Hard | Remove perfect square stones, last to move loses | Sprague-Grundy / DP |
| 240 | Predict the Winner (LC #486) | Medium | Two players pick from ends, can Player 1 score >= Player 2 | Minimax DP |
| 241 | Nim Game (LC #292) | Easy | One pile of n stones, take 1-3, last to move wins | Parity / math |
| 242 | Nim Game DP Version | Medium | Multiple piles, take any from one pile | XOR / Grundy |
| 243 | Can I Win (LC #464) | Hard | Two players alternate, first to reach total wins, can Player 1 force win | Bitmask + minimax |
| 244 | Optimal Strategy for a Game | Medium | Pick from ends to maximize your total | Minimax DP |
| 245 | Minimum Cost to Move Chips to Same Position (LC #1217) | Easy | Chips at positions, move 1/2 cost, minimize total cost | Greedy |
| 246 | Divisor Game (LC #1025) | Easy | Alice and Bob subtract divisors, Alice starts | Math / DP |
| 247 | Guess Number Higher or Lower (LC #375) | Medium | Guess with hints high/low, minimize worst-case cost | Interval minimax |
| 248 | Maximize Win From Two Segments | Medium | Two players mark segments to maximize covered points | DP + greedy |
| 249 | Coin Game Winner | Medium | Two players pick 1, 3, 4 coins, determine if first player wins | Fibonacci variant |
| 250 | A and B Take Turns with Coins | Medium | Two players take from either end of coin row | Minimax DP |

---

## 14. State Machine / Buy-Sell Stock DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 251 | Best Time to Buy and Sell Stock I (LC #121) | Easy | Maximum profit from single buy-sell transaction | Track minimum so far |
| 252 | Best Time to Buy and Sell Stock II (LC #122) | Medium | Maximum profit from unlimited buy-sell transactions | Greedy / DP |
| 253 | Best Time to Buy and Sell Stock III (LC #123) | Hard | Maximum profit from at most 2 transactions | State machine DP |
| 254 | Best Time to Buy and Sell Stock IV (LC #188) | Hard | Maximum profit from at most k transactions | State machine DP |
| 255 | Best Time with Cooldown (LC #309) | Medium | Unlimited transactions with 1-day cooldown after selling | 3-state DP |
| 256 | Best Time with Transaction Fee (LC #714) | Medium | Unlimited transactions with fee per transaction | 2-state DP |
| 257 | Best Time with Cooldown + Fee | Hard | Combine cooldown and fee constraints | 3-state with fee |
| 258 | Buy and Sell Stock with at Most K Transactions and Cooldown | Hard | Generalized state machine | Multi-state DP |
| 259 | Best Time to Buy and Sell Stock — All in One (LC #309/714/188 combined) | Hard | Unified state machine for all stock problems | State machine |
| 260 | Maximum Profit from Stock with Borrowing | Hard | Allow borrowing money, maximize final cash | State machine |

---

## 15. Counting DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 261 | Climbing Stairs — Count Ways (LC #70) | Easy | Count distinct ways to reach the top | Fibonacci counting |
| 262 | Catalan Numbers (LC #96 — Unique BSTs) | Medium | Count structurally unique BSTs with n nodes | Catalan DP |
| 263 | Count Number of Balanced Binary Trees | Medium | Count balanced binary trees of height h | Catalan variant |
| 264 | Count of Distinct Subsequences | Hard | Count distinct non-empty subsequences of a string | 1D + hash map |
| 265 | Unique Binary Search Trees (LC #96) | Medium | Count structurally unique BSTs with n distinct keys | Catalan |
| 266 | Pascal's Triangle (LC #118) | Easy | Generate first n rows of Pascal's triangle | 2D DP |
| 267 | Minimum Number of Taps to Open to Water Garden (LC #1326) | Hard | Minimum taps to water entire garden | Jump game variant |
| 268 | Count Ways to Build Staircase | Medium | Count ways to build a staircase with n blocks | Partition counting |
| 269 | Number of Ways to Split Array into Two Parts | Medium | Split array into non-empty parts satisfying some condition | Prefix / suffix |
| 270 | Count All Valid Pickup and Delivery Options (LC #1359) | Hard | Count valid sequences of pickup and delivery for n orders | Counting DP |

---

## 16. Probability / Expected Value DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 271 | Dice Throw / Sum Probability | Medium | Probability of getting sum S throwing n dice with k faces | 2D probability DP |
| 272 | New 21 Game (LC #837) | Hard | Probability of accumulating <= K points before exceeding K | 1D probability DP |
| 273 | Probability of a Target Sum with Dice | Medium | Probability of achieving target sum from dice throws | 2D probability |
| 274 | Random Pick with Weight (LC #528) | Medium | Pick an index with probability proportional to weight | Prefix sum + binary search |
| 275 | Random Pick Index (LC #398) | Medium | Pick a random index equal to target with equal probability | Reservoir sampling |
| 276 | Expected Value of Dice Rolls | Medium | Expected number of rolls to reach a target | Linearity of expectation |

---

## 17. Optimization / Scheduling DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 277 | Weighted Job Scheduling (LC #1235) | Hard | Maximum profit from non-overlapping jobs with weights | Sort + 1D DP |
| 278 | Maximum Profit in Job Scheduling (LC #1235) | Hard | Schedule non-overlapping jobs for max profit | Binary search + DP |
| 279 | Non-overlapping Intervals (LC #435) | Medium | Minimum removals to make intervals non-overlapping | Greedy |
| 280 | Line Break / Word Wrap (Knuth-Plass) | Hard | Break text into lines to minimize raggedness cost | Interval DP |
| 281 | Activity Selection with DP | Medium | Maximum non-overlapping activities | Greedy / 1D DP |
| 282 | Job Sequencing Problem | Medium | Maximize profit with deadlines and profits | Sort + DP / greedy |
| 283 | Minimum Number of Platforms Required | Medium | Minimum platforms for train scheduling | Greedy |
| 284 | Maximum Overlapping Intervals | Medium | Find maximum number of overlapping intervals | Sweep line |
| 285 | Partition Array into Three Parts with Equal Sum (LC #1013) | Easy | Check if array can be partitioned into 3 non-empty parts with equal sum | Prefix sum |

---

## 18. Misc Hard / Mixed DP

| # | Problem | Diff | Description | Pattern |
|---|---------|------|-------------|---------|
| 286 | Frog Jump (LC #403) | Hard | Determine if frog can cross river on stones with given jump distances | Hash set + DP |
| 287 | Minimum Cost to Make Array Equal (LC #2448) | Hard | Make all array elements equal with minimum cost (cost proportional) | Median + DP |
| 288 | Maximum Earnings from Taxi (LC #2002) | Medium | Maximize taxi earnings from trips (start,end,cost) | Weighted interval |
| 289 | Longest Common Prefix After Queries | Hard | Process queries and find longest common prefix | DP + segment tree |
| 290 | Minimum Number of Operations to Make Array Continuous (LC #2009) | Hard | Minimum replacements to make array continuous | Sliding window + DP |
| 291 | Number of Increasing Subsequences in an Array | Medium | Count all increasing subsequences | 1D counting DP |
| 292 | Minimum Moves to Make Array Complementary (LC #1674) | Medium | Minimum moves to make all pairs sum to target | Difference array |
| 293 | Maximum Profit from Selling Candies | Medium | Maximize profit selling candies at different prices | Greedy + DP |
| 294 | Count Arrays with Bounded Difference | Medium | Count arrays where adjacent elements differ by at most d | 1D DP |
| 295 | Minimum Cost to Connect Sticks (LC #1167) | Medium | Connect all sticks at minimum total cost | Heap + greedy |
| 296 | Ways to Split Array into Three Subarrays (LC #1712) | Medium | Count ways to split into three non-overlapping contiguous parts | Prefix sum + binary search |
| 297 | Minimum Cost to Reduce Array to Single Element | Medium | Reduce array by removing adjacent pairs | Interval DP |
| 298 | Longest Arithmetic Subsequence (LC #1027) | Medium | Longest arithmetic subsequence (not necessarily contiguous) | 1D DP + hash map |
| 299 | Longest Arithmetic Subsequence of Given Difference (LC #1218) | Medium | Longest arithmetic subsequence with fixed difference | 1D DP + hash map |
| 300 | Maximum Length of Subarray With Positive Product (LC #1567) | Medium | Maximum length subarray with positive product | Sign tracking |
| 301 | Count Subarrays with Bounded Maximum (LC #795) | Medium | Count subarrays where max falls within [left,right] | Inclusion-exclusion |
| 302 | Minimum Cost to Move Chips to The Same Position (LC #1217) | Easy | Move chips at positions to same spot at min cost | Greedy |
| 303 | Minimum Number of Increments on Subarrays to Form Target Array (LC #1536) | Hard | Minimum operations to reach target by incrementing subarrays | Stack / decomposition |
| 304 | Maximum Number of Non-overlapping Subarrays with Sum Zero (LC #1546) | Medium | Maximum count of non-overlapping zero-sum subarrays | Prefix sum + greedy |
| 305 | Minimum Cost to Split Array (LC #2547) | Hard | Split array into k parts to minimize total cost | 1D DP + precompute |
| 306 | Minimum Falling Path Sum (LC #931) | Medium | Minimum sum path in triangle-like grid from top to any bottom cell | 2D DP |
| 307 | Longest Substring with At Most 2 Distinct Characters | Medium | Length of longest substring with at most 2 distinct characters | Sliding window |
| 308 | Paint House IV | Hard | Paint houses in a circle with k colors | Circular DP + bitmask |
| 309 | Maximum Weighted Job Scheduling | Hard | Schedule non-overlapping jobs for max weight | Sort + DP + binary search |
| 310 | Longest Path in Matrix with Hops | Medium | Maximum length path in matrix where you can jump K cells | 2D DP with lookback |
| 311 | Minimum Insertions to Form a Palindrome (LC #1312) | Medium | Minimum insertions to make string palindrome | LPS-based |
| 312 | Maximum Product of Three Numbers (LC #1464) | Easy | Maximum product of three elements in array | Track max/min |
| 313 | Minimum Cost to Reach Bottom Right with Teleporters | Medium | Grid with teleport points, find minimum cost path | 2D + teleport DP |
| 314 | Minimum Operations to Convert All Elements to Zero (LC #3264) | Hard | Operations to reduce array to zero | Greedy + stack |
| 315 | Count Increasing Subsequences of Length K | Hard | Count increasing subsequences of exactly length k | 2D DP |
| 316 | Maximum Score from Removing Substrings (LC #1717) | Medium | Remove "ab" and "ba" with maximum score | Stack / DP |
| 317 | Minimum Operations to Make a Subsequence (LC #1571) | Hard | Minimum insertions to make target a subsequence of arr | LIS-based |
| 318 | Minimum Cost to Make at Least One Valid Sequence in a String (LC #2638) | Hard | Minimum changes to make valid prefix/suffix patterns | Multi-state DP |
| 319 | Maximum Points You Can Obtain from Cards (LC #1423) | Medium | Pick k cards from either end to maximize sum | 1D sliding window |
| 320 | Minimum Total Distance Traveled (LC #2463) | Hard | Robots + factories, minimize total travel distance | 2D DP |
| 321 | Split Array Largest Sum (LC #410) | Hard | Split array into m parts, minimize largest subarray sum | Binary search + DP |
| 322 | Minimum Speed to Arrive on Time (LC #1870) | Medium | Find minimum speed to arrive on time given travel segments | Binary search |
| 323 | Smallest Sufficient Team (LC #1125) | Hard | Minimum team of people covering all required skills | Bitmask DP |
| 324 | Maximum Students Taking Exam (LC #1235) | Hard | Maximum students in a seated exam with no cheating | Bitmask DP |
| 325 | Maximum Profit in a Balanced Tree | Hard | Optimize profit with tree constraints | Tree DP |
| 326 | Minimum Cost to Buy Tickets at Minimum Cost | Medium | Buy tickets for consecutive days with passes | 1D DP |
| 327 | Count of Subarrays with Median Greater Than K | Hard | Count subarrays with median > K | Transform + prefix |
| 328 | Maximum Number of Points from Grid Queries (LC #2503) | Hard | Process queries to find reachable cells | Union-Find + offline |
| 329 | Number of Pairs of Strings With Concatenation Equal to Target (LC #1758) | Medium | Count pairs whose concatenation equals target | Counting + DP |
| 330 | Maximum Sum of Non-overlapping Intervals | Medium | Maximum weight non-overlapping set of intervals | Weighted interval DP |
| 331 | Longest Square Streak in an Array (LC #2501) | Medium | Longest subsequence where each element is square of previous | Hash map + LIS |
| 332 | Minimum Number of Operations to Make String Sorted (LC #1830) | Hard | Minimum adjacent swaps to sort string lexicographically | Math + combinatorics |
| 333 | Count Number of Bad Pairs (LC #2364) | Medium | Count pairs (i,j) where j-i != nums[j]-nums[i] | Math + counting |
| 334 | Maximum Sum of Subsequence Without Adjacent (Weighted) | Medium | Maximum weight independent set on a line | Non-adjacent 1D |
| 335 | Minimum Operations to Make a String Alternating (LC #1896) | Medium | Minimum moves to make string strictly alternating | Flip counting |
| 336 | Maximum Length of Pair Chain (LC #646) | Medium | Longest chain of pairs where pairs[i][1] < pairs[j][0] | LIS |
| 337 | Minimum Number of Operations to Sort a Binary Tree by Level (LC #2583) | Hard | Sort each level of binary tree | BFS + sort counting |
| 338 | Minimum Absolute Sum Difference (LC #1200) | Medium | Replace one element to minimize absolute differences | Binary search |
| 339 | Count Good Triplets (LC #1534) | Easy | Count triples satisfying conditions | Brute force + prefix |
| 340 | Maximum Number of Events That Can Be Attended (LC #1353) | Medium | Attend maximum events with overlapping time ranges | Greedy + heap |
| 341 | Number of Dice Rolls with Target Sum (LC #1155) | Medium | Count ways to get target sum with d dice each having f faces | 2D DP counting |
| 342 | Minimum Cost to Cut a Stick (LC #1547) | Hard | Cut stick at given positions to minimize total cutting cost | Interval DP |
| 343 | Maximum Performance of a Team (LC #1383) | Hard | Select k engineers to maximize speed/sum of efficiency | Sort + greedy + heap |
| 344 | Minimum Number of Work Sessions to Finish Tasks (LC #1681) | Hard | Minimum sessions to complete all tasks within session time | Bitmask DP |
| 345 | Minimum Distance to Type a Word Using Two Fingers (LC #1132) | Hard | Two fingers typing, minimize total finger movement | 3D DP |
| 346 | Maximum Alternating Subsequence (Weighted) | Medium | Maximum weight alternating subsequence | 1D state |
| 347 | Minimum Operations to Make the Array Alternating (LC #2170) | Medium | Minimum replacements to make array alternating | Greedy + count |
| 348 | Maximum Length of Subarray With Positive Product (LC #1567) | Medium | Longest subarray with positive product | Sign tracking |
| 349 | Minimum Total Cost to Make Arrays Unequal (LC #2499) | Hard | Minimum swaps to make arrays unequal | Greedy + DP |
| 350 | Longest Substring with Same Letters After K Replacement (LC #424) | Medium | Longest window with at most K replacements to make all same | Sliding window |

---

## Summary

| Category | Count | Easy | Medium | Hard |
|----------|-------|------|--------|------|
| 1. 1D Linear DP | 43 | 4 | 28 | 11 |
| 2. Two Sequence / 2D String DP | 30 | 3 | 18 | 9 |
| 3. 2D Grid DP | 22 | 0 | 14 | 8 |
| 4. 0/1 Knapsack Family | 17 | 0 | 13 | 4 |
| 5. Unbounded Knapsack Family | 15 | 1 | 13 | 1 |
| 6. Interval DP | 16 | 0 | 6 | 10 |
| 7. LIS Family | 20 | 0 | 14 | 6 |
| 8. Subarray / Substring DP | 14 | 0 | 13 | 1 |
| 9. Tree DP | 19 | 2 | 11 | 6 |
| 10. Graph DP | 15 | 0 | 11 | 4 |
| 11. Bitmask DP | 14 | 0 | 3 | 11 |
| 12. Digit DP | 10 | 0 | 7 | 3 |
| 13. Game Theory DP | 15 | 2 | 10 | 3 |
| 14. State Machine / Stocks | 10 | 1 | 4 | 5 |
| 15. Counting DP | 10 | 1 | 7 | 2 |
| 16. Probability / Expected Value DP | 6 | 0 | 5 | 1 |
| 17. Optimization / Scheduling DP | 9 | 0 | 6 | 3 |
| 18. Misc Hard / Mixed DP | 65 | 3 | 35 | 27 |
| **TOTAL** | **350** | **17** | **214** | **119** |

---

> **Next step:** Review this list. Tell me to:
> - **Add more problems** in specific categories (say which ones)
> - **Remove/skip** problems you don't need
> - **Confirm quantity** and I'll start writing detailed solutions for all confirmed problems in the `13_Dynamic_Programming/` folder files
