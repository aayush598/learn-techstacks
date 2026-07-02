# DP Pattern Identification

## Table of Contents
1. How to Identify DP Problems
2. "Choose with Capacity" → Knapsack DP
3. "Sequence Comparison" → LCS (Longest Common Subsequence)
4. "Increasing Subsequence" → LIS (Longest Increasing Subsequence)
5. "Range/Interval" → Interval DP (MCM)
6. "Grid Path" → Grid DP
7. "Tree Traversal" → Tree DP
8. "Subset of Items" → Bitmask DP
9. "Digit Constraints" → Digit DP
10. "String Matching" → String DP
11. DP Pattern Decision Tree

---

## 1. How to Identify DP Problems

**Three questions to ask:**
1. Does the problem ask for optimal value (max/min) or count of ways?
2. Can the problem be broken into overlapping subproblems?
3. Does the current decision depend on previous decisions?

**Optimal substructure:** Optimal solution of the problem can be obtained by using optimal solutions of its subproblems.
**Overlapping subproblems:** The same subproblems are solved multiple times.

**Keywords that suggest DP:**
- "Maximum/minimum" (path sum, profit, length)
- "Number of ways" (count paths, ways to make change)
- "Can we achieve" (subset sum, partition)
- "Longest/shortest" (subsequence, path)
- "Optimal" (schedule, allocation)

**When NOT to use DP:**
- Greedy works (locally optimal = globally optimal)
- Problem doesn't have overlapping subproblems (use divide & conquer)
- Input constraints allow brute force (n ≤ 20)

---

## 2. "Choose with Capacity" → Knapsack DP

**Keywords:** Capacity, weight, value, maximize, subset sum, partition, can we make exactly target

### 0/1 Knapsack
- Each item can be taken at most once
- `dp[i][w] = max value using first i items, capacity w`

```java
// State: dp[w] = max value achievable with exact capacity w
int knapsack01(int[] weights, int[] values, int capacity) {
    int n = weights.length;
    int[] dp = new int[capacity + 1];
    for (int i = 0; i < n; i++) {
        for (int w = capacity; w >= weights[i]; w--) {
            dp[w] = Math.max(dp[w], values[i] + dp[w - weights[i]]);
        }
    }
    return dp[capacity];
}
```

### Unbounded Knapsack (Coin Change)
- Each item can be taken unlimited times
- Iterate w forward for unbounded

```java
int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;
    for (int coin : coins) {
        for (int w = coin; w <= amount; w++) {
            dp[w] = Math.min(dp[w], 1 + dp[w - coin]);
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```

### Problems that Map to Knapsack
| Problem | What is "capacity"? | What is "value"? | Knapsack type |
|---------|-------------------|-------------------|---------------|
| Partition equal subset sum | target = sum/2 | sum of subset | 0/1 (can we achieve) |
| Target sum (+/- assignment) | target | count of ways | 0/1 (count ways) |
| Ones and zeroes | m ones, n zeroes | size of subset | 2D 0/1 |
| Last stone weight II | sum/2 | max achievable ≤ sum/2 | 0/1 |
| Coin change II | amount | number of combos | Unbounded |
| Combination sum IV | target | number of permutations | Unbounded (order matters) |
| Perfect squares | n | min count | Unbounded |
| Word break | string length | can segment | Unbounded (on string) |

---

## 3. "Sequence Comparison" → LCS

**Keywords:** Longest common, edit distance, alignment, similarity between two strings/sequences

**Template:**
```java
int lcs(String text1, String text2) {
    int m = text1.length(), n = text2.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                dp[i][j] = 1 + dp[i - 1][j - 1];
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    return dp[m][n];
}
```

**Problems that map to LCS:**
| Problem | Insight | Variation |
|---------|---------|-----------|
| Longest common subsequence | Classic LCS | Base |
| Longest common substring | Match consecutively, reset on mismatch | Diagonal tracking |
| Shortest common supersequence | m + n - LCS | Build string |
| Edit distance (Levenshtein) | Insert/delete/replace costs | min of 3 operations |
| Delete operation for two strings | m + n - 2*LCS | Deletions only |
| Minimum ASCII delete sum | Sum of ASCII of deleted chars | Weighted edit |
| Longest palindromic subsequence | LCS(s, reverse(s)) | Reduce to LCS |
| Distinct subsequences | Count ways, not length | DP with sum |

### Edit Distance Variant
```java
int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], // replace
                                Math.min(dp[i - 1][j],     // delete
                                         dp[i][j - 1]));  // insert
            }
        }
    }
    return dp[m][n];
}
```

---

## 4. "Increasing Subsequence" → LIS

**Keywords:** Longest increasing, longest chain, longest sequence

**Template (O(n²) DP):**
```java
int lengthOfLIS(int[] nums) {
    int n = nums.length;
    int[] dp = new int[n];
    Arrays.fill(dp, 1);
    int maxLen = 1;
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i]) {
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
        maxLen = Math.max(maxLen, dp[i]);
    }
    return maxLen;
}
```

**Template (O(n log n) Patience Sorting):**
```java
int lengthOfLIS(int[] nums) {
    int[] tails = new int[nums.length];
    int size = 0;
    for (int num : nums) {
        int i = Arrays.binarySearch(tails, 0, size, num);
        if (i < 0) i = -(i + 1);
        tails[i] = num;
        if (i == size) size++;
    }
    return size;
}
```

**Problems that map to LIS:**
| Problem | Insight |
|---------|---------|
| Longest increasing subsequence | Classic |
| Number of LIS | Track count along with length |
| Russian doll envelopes | Sort by width asc, height desc → LIS on height |
| Longest chain of pairs | Sort by first, LIS on second |
| Longest bitonic subsequence | LIS(left) + LIS(right) - 1 |
| Minimum deletions to make sorted | n - LIS |
| Maximum height by stacking cubes | Sort + LIS on multiple dimensions |
| Widest vertical area → not LIS | Actually greedy, but can mislead |

---

## 5. "Range/Interval" → Interval DP (MCM)

**Keywords:** Matrix chain, burst balloons, polygon, palindrome partitioning

**Key pattern:** Solve for all intervals [i, j], use results of smaller intervals [i, k] and [k+1, j].

**Template:**
```java
// Matrix Chain Multiplication
int matrixMultiplication(int[] arr) {
    int n = arr.length;
    int[][] dp = new int[n][n];
    // dp[i][j] = min cost to multiply matrices i..j

    for (int len = 2; len < n; len++) {
        for (int i = 1; i < n - len + 1; i++) {
            int j = i + len - 1;
            dp[i][j] = Integer.MAX_VALUE;
            for (int k = i; k < j; k++) {
                int cost = dp[i][k] + dp[k + 1][j]
                         + arr[i - 1] * arr[k] * arr[j];
                dp[i][j] = Math.min(dp[i][j], cost);
            }
        }
    }
    return dp[1][n - 1];
}
```

**Template: Palindrome Partitioning**
```java
int minCut(String s) {
    int n = s.length();
    boolean[][] isPal = new boolean[n][n];
    int[] dp = new int[n]; // dp[i] = min cuts for s[0..i]

    for (int i = 0; i < n; i++) {
        dp[i] = i; // max cuts = i (cut every char)
        for (int j = 0; j <= i; j++) {
            if (s.charAt(j) == s.charAt(i) && (i - j <= 2 || isPal[j+1][i-1])) {
                isPal[j][i] = true;
                dp[i] = (j == 0) ? 0 : Math.min(dp[i], dp[j - 1] + 1);
            }
        }
    }
    return dp[n - 1];
}
```

**Problems that map to Interval DP:**
| Problem | Base case | Transition |
|---------|-----------|------------|
| Matrix chain multiplication | len = 1 cost = 0 | dp[i][k] + dp[k+1][j] + cost |
| Burst balloons | Add 1 at ends | dp[i][k-1] + dp[k+1][j] + burst(k) last |
| Longest palindromic subsequence | dp[i][i] = 1 | match: 2+dp[i+1][j-1], else max |
| Minimum cost to cut a stick | Sort cuts, add ends | dp[i][k] + dp[k][j] + len |
| Stone game | dp[i][i] = piles[i] | max(piles[i]-dp[i+1][j], piles[j]-dp[i][j-1]) |
| Remove boxes | Complex state | Need 3D DP for color grouping |
| Strange printer | dp[i][i] = 1 | match: dp[i][k-1] + dp[k+1][j] |

---

## 6. "Grid Path" → Grid DP

**Keywords:** Robot in grid, path with obstacles, min path sum, max gold, dungeon game

**Template: Min Path Sum**
```java
public int minPathSum(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    int[][] dp = new int[m][n];
    dp[0][0] = grid[0][0];
    for (int i = 1; i < m; i++) dp[i][0] = dp[i-1][0] + grid[i][0];
    for (int j = 1; j < n; j++) dp[0][j] = dp[0][j-1] + grid[0][j];
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[i][j] = grid[i][j] + Math.min(dp[i-1][j], dp[i][j-1]);
        }
    }
    return dp[m-1][n-1];
}
```

**Problems that map to Grid DP:**
| Problem | Variation |
|---------|-----------|
| Unique paths | Count ways to reach bottom-right |
| Unique paths II | Same with obstacles |
| Minimum path sum | Min sum path |
| Maximum path sum (triangle) | From top to bottom |
| Dungeon game | Work backwards from end |
| Cherry pickup | 2 passes = 4D DP |
| Gold mine | Max gold from any starting cell |
| Out of boundary paths | Count ways to leave grid in k steps |

---

## 7. "Tree Traversal" → Tree DP

**Keywords:** Tree, subtree, maximum path sum in tree, diameter, binary tree camera

**Key insight:** For each node, compute answer using children's results (post-order traversal).

**Template: Tree Diameter**
```java
int diameter = 0;
int diameterOfBinaryTree(TreeNode root) {
    height(root);
    return diameter;
}
int height(TreeNode node) {
    if (node == null) return 0;
    int left = height(node.left);
    int right = height(node.right);
    diameter = Math.max(diameter, left + right); // path through node
    return 1 + Math.max(left, right); // height of node
}
```

**Template: House Robber III**
```java
public int rob(TreeNode root) {
    int[] result = robHelper(root);
    return Math.max(result[0], result[1]);
}
// returns [max with node, max without node]
int[] robHelper(TreeNode node) {
    if (node == null) return new int[]{0, 0};
    int[] left = robHelper(node.left);
    int[] right = robHelper(node.right);
    int withNode = node.val + left[1] + right[1]; // can't rob children
    int withoutNode = Math.max(left[0], left[1]) + Math.max(right[0], right[1]);
    return new int[]{withNode, withoutNode};
}
```

**Problems that map to Tree DP:**
| Problem | State at node |
|---------|--------------|
| Max path sum (any node to any) | max single path, max through node |
| Binary tree cameras | 3 states: covered/no camera, has camera, needs coverage |
| Longest univalue path | Extend from matching children |
| Smallest subtree with deepest nodes | Return deepest depth, return node when equal |
| Max sum BST in binary tree | Track isBST, sum, min, max |
| Distribute coins in tree | Excess coins passed to parent |

---

## 8. "Subset of Items" → Bitmask DP

**Keywords:** Small n (≤ 20), assign to groups, subset covering, traveling salesman

**Key idea:** Use bitmask (integer whose bits represent which items are used) as DP state.

**Template: Traveling Salesman**
```java
int tsp(int[][] dist, int n) {
    int[][] dp = new int[1 << n][n];
    for (int[] row : dp) Arrays.fill(row, Integer.MAX_VALUE / 2);
    dp[1][0] = 0; // start at city 0, mask 1 = only city 0 visited

    for (int mask = 1; mask < (1 << n); mask++) {
        for (int last = 0; last < n; last++) {
            if ((mask & (1 << last)) == 0) continue; // last not in mask
            for (int next = 0; next < n; next++) {
                if ((mask & (1 << next)) != 0) continue; // already visited
                int newMask = mask | (1 << next);
                dp[newMask][next] = Math.min(dp[newMask][next],
                    dp[mask][last] + dist[last][next]);
            }
        }
    }
    int fullMask = (1 << n) - 1;
    int minDist = Integer.MAX_VALUE;
    for (int last = 1; last < n; last++) {
        minDist = Math.min(minDist, dp[fullMask][last] + dist[last][0]);
    }
    return minDist;
}
```

**Template: Partition to K Equal Sum Subsets**
```java
public boolean canPartitionKSubsets(int[] nums, int k) {
    int sum = 0;
    for (int num : nums) sum += num;
    if (sum % k != 0) return false;
    int target = sum / k;
    int n = nums.length;
    Boolean[] dp = new Boolean[1 << n];
    dp[0] = true;
    int[] sumMask = new int[1 << n];

    for (int mask = 0; mask < (1 << n); mask++) {
        if (dp[mask] == null || !dp[mask]) continue;
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) continue;
            int newMask = mask | (1 << i);
            int newSum = (sumMask[mask] + nums[i]) % target;
            if (sumMask[mask] + nums[i] <= target) {
                sumMask[newMask] = newSum;
                dp[newMask] = true;
            }
        }
    }
    return dp[(1 << n) - 1];
}
```

**Problems:**
- Partition to k equal sum subsets
- Matchsticks to square (subset of 4)
- Traveling salesman problem
- Maximum students taking exam (seating constraints with masks)
- Beautiful arrangement (count permutations with constraints)
- Number of ways to wear hats (person → hat assignment)

---

## 9. "Digit Constraints" → Digit DP

**Keywords:** Count numbers in range [L, R] with property, digit constraints

**Key insight:** Process digits from most significant to least, tracking tight flag.

**Template: Count numbers with sum of digits ≤ S**
```java
public int countNumbers(int limit, int maxSum) {
    String s = String.valueOf(limit);
    int n = s.length();
    int[][][] dp = new int[n + 1][2][maxSum + 1];
    dp[0][1][0] = 1; // starts tight

    for (int pos = 0; pos < n; pos++) {
        int digit = s.charAt(pos) - '0';
        for (int tight = 0; tight <= 1; tight++) {
            for (int sum = 0; sum <= maxSum; sum++) {
                int ways = dp[pos][tight][sum];
                if (ways == 0) continue;
                int maxDigit = tight == 1 ? digit : 9;
                for (int d = 0; d <= maxDigit; d++) {
                    if (sum + d <= maxSum) {
                        dp[pos + 1][tight == 1 && d == maxDigit ? 1 : 0][sum + d] += ways;
                    }
                }
            }
        }
    }
    int total = 0;
    for (int tight = 0; tight <= 1; tight++) {
        for (int sum = 0; sum <= maxSum; sum++) {
            total += dp[n][tight][sum];
        }
    }
    return total;
}
```

**Problems:**
- Count numbers with digit sum = S in range
- Numbers with repeated digits
- Numbers with non-decreasing digits
- Count of integers with digit difference
- Count special numbers (divisible by digits)
- Number of digit one (count 1s in all numbers)

---

## 10. "String Matching" → String DP

**Keywords:** Wildcard matching, regex, pattern match, interleaving strings

**Template: Wildcard Matching**
```java
public boolean isMatch(String s, String p) {
    int m = s.length(), n = p.length();
    boolean[][] dp = new boolean[m + 1][n + 1];
    dp[0][0] = true;
    for (int j = 1; j <= n; j++) {
        if (p.charAt(j - 1) == '*') dp[0][j] = dp[0][j - 1];
    }
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            char sc = s.charAt(i - 1), pc = p.charAt(j - 1);
            if (pc == '*') {
                dp[i][j] = dp[i][j - 1] || dp[i - 1][j];
            } else if (pc == '?' || sc == pc) {
                dp[i][j] = dp[i - 1][j - 1];
            }
        }
    }
    return dp[m][n];
}
```

**Problems:**
- Wildcard matching (* matches any sequence, ? matches single char)
- Regular expression matching (* matches preceding element zero or more, . matches any char)
- Interleaving string (is s3 interleaving of s1 and s2)
- Distinct subsequences (count of s2 as subsequence of s1)

---

## 11. DP Pattern Decision Tree

```
Identify the problem:
├── Is it on a tree/graph?
│   ├── Tree → Tree DP (post-order traversal)
│   └── Graph with small N (≤20) → Bitmask DP
│
├── Is it comparing two sequences?
│   ├── Find common/longest → LCS
│   ├── Edit/match → String DP
│   └── Increasing within one → LIS
│
├── Is it about ranges/intervals?
│   ├── Matrix chain multiplication style → Interval DP
│   └── Palindrome partitioning → Interval DP
│
├── Is it choosing items with constraints?
│   ├── Items used once → 0/1 Knapsack
│   ├── Items unlimited → Unbounded Knapsack
│   └── Subset sum / partition → Knapsack (boolean)
│
├── Is it about paths in grid?
│   └── Robot moving right/down → Grid DP
│
├── Is it counting numbers in range?
│   └── Digit constraints → Digit DP
│
├── Is it about subarrays?
│   ├── Kadane (max subarray sum) → Greedy/DP
│   └── Contiguous → Sliding window (not DP)
│
└── None of the above?
    └── Is it a subsequence problem?
        ├── Single array → LIS/other 1D DP
        └── Two arrays → LCS
```
