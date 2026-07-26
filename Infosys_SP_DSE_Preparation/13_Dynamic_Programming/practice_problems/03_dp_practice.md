# DP Practice Problems for Infosys SP DSE

25 carefully curated problems in order of difficulty.

## Quick Pattern Reference for Practice

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Problem # → Pattern                                                   │
├──────────────────────────────────────────────────────────────────────────┤
│  1-3 (Easy)  → 1D DP, Fibonacci-style (build up from base cases)      │
│  4-8 (Medium)→ 2D DP, LIS, LCS, string comparison                     │
│  9-15 (Hard) → Interval DP, minimax, game theory, reverse DP           │
│  16-25 (SP L3)→ Bitmask DP, tree DP, advanced interval/string DP      │
└──────────────────────────────────────────────────────────────────────────┘

Before solving: ask yourself
  1. Is the problem asking for count, max/min, or yes/no?
  2. Are there choices at each step?
  3. Can I break the problem into overlapping subproblems?
  4. What state captures the necessary context?
```

---

## EASY

### 1. Climbing Stairs

Problem: n steps, climb 1 or 2 steps at a time. Count ways to reach top.

**Pattern:** Fibonacci — each step depends on previous two.

```
dp[i] = dp[i-1] + dp[i-2]
Base: dp[1]=1, dp[2]=2

Example: n=5
dp = [_, 1, 2, 3, 5, 8]
              └──┴──┘
          dp[3]=dp[2]+dp[1]
Answer: 8
```

```python
def climb_stairs(n):
    if n <= 1: return 1
    a, b = 1, 1  # dp[1], dp[2] base
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Time: O(n), Space: O(1)

def climb_stairs_memo(n, memo=None):
    if memo is None: memo = {}
    if n <= 1: return 1
    if n in memo: return memo[n]
    memo[n] = climb_stairs_memo(n - 1, memo) + climb_stairs_memo(n - 2, memo)
    return memo[n]
```

---

### 2. House Robber

Problem: Adjacent houses cannot be robbed together. Maximize sum.

**Pattern:** 1D DP — at each house, choose to rob (add to prev-skip) or skip (take prev-best).

```
At house i:
  rob   = prev_skip + nums[i]   # Can only rob if previous was skipped
  skip  = max(prev_rob, prev_skip)  # Free to choose best so far

Example: nums = [2, 7, 9, 3, 1]
  i=0: rob=2,  skip=0  → best=2
  i=1: rob=7,  skip=2  → best=7
  i=2: rob=11, skip=7  → best=11
  i=3: rob=10, skip=11 → best=11
  i=4: rob=12, skip=11 → best=12
Answer: 12 (rob houses 0, 2, 4)
```

```python
def rob(nums):
    prev2 = prev1 = 0
    for num in nums:
        curr = max(prev1, prev2 + num)  # skip or rob
        prev2, prev1 = prev1, curr
    return prev1

# Time: O(n), Space: O(1)
```

---

### 3. Min Cost Climbing Stairs

Problem: cost[i] to step on stair i. Start at 0 or 1. Find min cost to reach top.

```python
def min_cost_climbing(cost):
    a, b = cost[0], cost[1]
    for i in range(2, len(cost)):
        a, b = b, cost[i] + min(a, b)  # Pay cost[i] + min of reaching from 1 or 2 steps back
    return min(a, b)

# Time: O(n), Space: O(1)
```

---

## MEDIUM

### 4. Longest Increasing Subsequence

Problem: Find length of LIS.

**Pattern:** Two approaches: O(n²) DP or O(n log n) patience sorting.

```
Approach 1 — O(n²) DP:
  dp[i] = length of LIS ending at index i
  dp[i] = 1 + max(dp[j]) for all j < i where nums[j] < nums[i]

Approach 2 — O(n log n) Patience Sorting:
  Maintain "piles" where each pile's top is the smallest ending element
  of an increasing subsequence of that length.
  
  nums = [10, 9, 2, 5, 3, 7, 101, 18]
  
  piles: [10] → [9] → [2] → [2,5] → [2,3] → [2,3,7] → [2,3,7,101]
                                           7<101 → append
  Answer: 4 piles = LIS length 4 (subsequence: 2,3,7,101 or 2,3,7,18)
```

```python
def length_of_lis(nums):
    import bisect
    piles = []
    for num in nums:
        i = bisect.bisect_left(piles, num)  # Find first pile top >= num
        if i == len(piles):
            piles.append(num)   # Extend longest subsequence
        else:
            piles[i] = num      # Replace pile top (smaller ending = more options)
    return len(piles)

# Time: O(n log n), Space: O(n)
```

---

### 5. Coin Change

Problem: Minimum coins to make amount. Unlimited supply.

**Pattern:** Unbounded Knapsack — loop coins first, capacity left-to-right.

```
coins = [1, 2, 5], amount = 11
dp = [0, ∞, ∞, ..., ∞]  (length 12)
After coin=1: dp = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
After coin=2: dp = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5,  6]
After coin=5: dp = [0, 1, 1, 2, 2, 1, 2, 2, 3, 3, 2,  3]
Answer: 3 (5+5+1)
```

```python
def coin_change(coins, amount):
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for a in range(coin, amount + 1):  # Left-to-right (unbounded!)
            dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != float("inf") else -1

# Time: O(n*amount), Space: O(amount)
```

---

### 6. Word Break

Problem: Can s be segmented using words from dictionary?

**Pattern:** 1D DP — dp[i] = True if s[0:i] can be segmented.

```python
def word_break(s, word_dict):
    words = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[n]

# Time: O(n^2), Space: O(n)
```

---

### 7. Unique Paths

Problem: m x n grid. Move right/down. Count paths to bottom-right.

**Pattern:** 2D Grid DP — dp[i][j] = ways to reach cell (i,j).

```
For a 3×4 grid:
dp = [[1, 1, 1, 1],
      [1, 2, 3, 4],
      [1, 3, 6, 10]]
Answer: 10
```

```python
def unique_paths(m, n):
    dp = [1] * n  # First row is all 1s
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]  # From above + from left
    return dp[-1]

# Time: O(m*n), Space: O(n)
```

---

### 8. Longest Common Subsequence

Problem: Given two strings, find LCS length.

**Pattern:** 2D String DP — match → diagonal+1, no match → max(above, left).

```
a="abcde", b="ace" → LCS = "ace", length = 3

     "" a c e
  ""  0 0 0 0
  a   0 1 1 1
  b   0 1 1 1
  c   0 1 2 2
  d   0 1 2 2
  e   0 1 2 3  ← answer
```

```python
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1   # Match → extend diagonal
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])  # No match → best so far
    return dp[m][n]

# Time: O(m*n), Space: O(m*n)
```

---

## HARD

### 9. Burst Balloons

Problem: Burst balloon i, get nums[i-1]*nums[i]*nums[i+1]. Max coins.

**Pattern:** Interval DP — "which balloon is LAST to burst in range [l..r]?"

```
nums = [3,1,5,8] → add sentinels [1,3,1,5,8,1]
dp[i][j] = max coins from bursting all balloons between sentinels i and j

dp[0][5] = 167 (burst order: 1→5→3→8)
```

```python
def max_coins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):        # Range length
        for i in range(n - length):   # Left boundary
            j = i + length            # Right boundary
            for k in range(i + 1, j): # Last balloon to burst
                dp[i][j] = max(dp[i][j],
                    nums[i] * nums[k] * nums[j] + dp[i][k] + dp[k][j])
    return dp[0][n - 1]

# Time: O(n^3), Space: O(n^2)
```

---

### 10. Edit Distance

Problem: Min ops (insert, delete, replace) to convert word1 to word2.

**Pattern:** 2D String DP — match → diagonal, no match → 1 + min(delete, insert, replace).

```python
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    prev = list(range(n + 1))   # Base: dp[0][j] = j inserts
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        curr[0] = i              # Base: dp[i][0] = i deletes
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]      # Match, no operation
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev = curr
    return prev[n]

# Time: O(m*n), Space: O(n)
```

---

### 11. Regular Expression Matching

Problem: Implement "." and "*" regex matching.

**Pattern:** 2D String DP — handle '*', '.' as special transitions.

```python
def is_match(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(2, n + 1):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]  # a*, b* can match empty
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == s[i - 1] or p[j - 1] == ".":
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j - 1] == "*":
                dp[i][j] = dp[i][j - 2]              # Zero occurrences
                if p[j - 2] == s[i - 1] or p[j - 2] == ".":
                    dp[i][j] = dp[i][j] or dp[i - 1][j]  # 1+ occurrences
    return dp[m][n]

# Time: O(m*n), Space: O(m*n)
```

---

### 12. Longest Palindromic Subsequence

Problem: Find length of longest palindromic subsequence.

**Pattern:** Interval DP — dp[i][j] on substring s[i..j].

```python
def longest_palindrome_subseq(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]

# Time: O(n^2), Space: O(n^2)
```

---

### 13. Maximal Rectangle

Problem: Find largest rectangle of 1s in binary matrix.

**Pattern:** Row-by-row histogram + monotone stack.

```python
def maximal_rectangle(matrix):
    if not matrix: return 0
    n = len(matrix[0])
    heights = [0] * n
    max_area = 0
    for row in matrix:
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == "1" else 0
        max_area = max(max_area, largest_rectangle_area(heights))
    return max_area

def largest_rectangle_area(heights):
    stack = []
    max_area = 0
    heights.append(0)
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    heights.pop()
    return max_area

# Time: O(m*n), Space: O(n)
```

---

### 14. Dungeon Game

Problem: Min initial health needed for knight to reach princess.

**Pattern:** Reverse DP — work backwards from princess to knight. Minimum health ≥ 1.

```python
def calculate_minimum_hp(dungeon):
    m, n = len(dungeon), len(dungeon[0])
    dp = [[float("inf")] * (n + 1) for _ in range(m + 1)]
    dp[m][n - 1] = dp[m - 1][n] = 1  # After reaching princess, need 1 HP
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            need = min(dp[i + 1][j], dp[i][j + 1]) - dungeon[i][j]
            dp[i][j] = max(1, need)  # Health can never drop below 1
    return dp[0][0]

# Time: O(m*n), Space: O(m*n)
```

---

### 15. Stone Game III

Problem: Alice and Bob take 1-3 stones from front. Maximize Alice score.

**Pattern:** Game DP — dp[i] = best score difference from position i.

```python
def stone_game_iii(values):
    n = len(values)
    dp = [float("-inf")] * (n + 1)
    dp[n] = 0
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + values[i]
    for i in range(n - 1, -1, -1):
        for take in range(1, 4):
            if i + take <= n:
                dp[i] = max(dp[i], suffix[i] - dp[i + take])
    a, b = dp[0], suffix[0] - dp[0]
    return "Alice" if a > b else ("Bob" if b > a else "Tie")

# Time: O(n), Space: O(n)
```

---

## SP L3 LEVEL

### 16. TSP (Bitmask DP)

Problem: Shortest tour visiting all cities and returning.

**Pattern:** Bitmask DP — dp[mask][last] = min cost with visited set and current city.

```
mask = bitmask of visited cities (e.g., 1011 = cities 0,1,3 visited)
dp[1][0] = 0  (only city 0 visited, cost 0)
Answer: min(dp[full][i] + cost[i][0]) for all i

n=4 cities: 2^4 = 16 masks × 4 cities = 64 states
```

```python
def tsp(cost):
    n = len(cost)
    INF = 10**9
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Start at city 0
    for mask in range(1 << n):
        for last in range(n):
            if not (mask >> last & 1): continue
            if dp[mask][last] == INF: continue
            for nxt in range(n):
                if (mask >> nxt) & 1: continue  # Already visited
                new_mask = mask | (1 << nxt)
                dp[new_mask][nxt] = min(dp[new_mask][nxt],
                    dp[mask][last] + cost[last][nxt])
    full = (1 << n) - 1
    ans = min(dp[full][i] + cost[i][0] for i in range(1, n) if cost[i][0])
    return ans

# Time: O(2^n * n^2), Space: O(2^n * n)
```

---

### 17. Tree DP - Max Independent Set

Problem: In a tree, find max weight set of non-adjacent nodes.

**Pattern:** 2-state Tree DP — (take, skip) at each node.

```python
def max_independent_set_tree(root):
    def dfs(node):
        if not node: return (0, 0)  # (take, skip)
        left = dfs(node.left)
        right = dfs(node.right)
        take = node.val + left[1] + right[1]      # Take node → must skip children
        skip = max(left) + max(right)              # Skip node → children are free
        return (take, skip)
    return max(dfs(root))

# Time: O(n), Space: O(h)
```

---

### 18. Interval DP - Matrix Chain

Problem: Min scalar multiplications for matrix chain.

**Pattern:** Interval DP — try all split points for each interval.

```
p = [10, 30, 5, 60]  (3 matrices: 10×30, 30×5, 5×60)
dp[0][2] = 4500  (parenthesis: (A₁×A₂)×A₃)
```

```python
def matrix_chain(p):
    n = len(p) - 1
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                q = dp[i][k] + dp[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                dp[i][j] = min(dp[i][j], q)
    return dp[0][n - 1]

# Time: O(n^3), Space: O(n^2)
```

---

### 19. Palindrome Partitioning II

Problem: Min cuts to partition string into palindromes.

**Pattern:** Precompute palindromes + 1D DP for min cuts.

```
s = "aab"
palindrome check: "aa"=T, "aab"=F, "ab"=F, "b"=T
dp[0]=0 ("a" is palindrome), dp[1]=0 ("aa" is palindrome), dp[2]=1 ("b" needs 1 cut)
Answer: 1 ("aa" | "b")
```

```python
def min_cut(s):
    n = len(s)
    if n <= 1: return 0
    # Precompute palindrome table
    pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or pal[i + 1][j - 1]):
                pal[i][j] = True
    # dp[i] = min cuts for s[0..i]
    dp = [float("inf")] * n
    for i in range(n):
        if pal[0][i]:
            dp[i] = 0           # Entire prefix is palindrome, no cuts needed
        else:
            for j in range(i):
                if pal[j + 1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)  # Cut after j, s[j+1..i] is palindrome
    return dp[n - 1]

# Time: O(n^2), Space: O(n^2)
```

---

### 20. Minimum Cost to Cut Stick

Problem: Cut stick at given positions. Cost is current stick length. Min total cost.

**Pattern:** Interval DP — try each cut as the "first cut" in the interval.

```
stick length=7, cuts=[1,3,4,5]
cuts with boundaries: [0,1,3,4,5,7]
First cut at position 3: cost=7, then solve [0,3] and [3,7] independently
```

```python
def min_cost(n, cuts):
    cuts = [0] + sorted(cuts) + [n]
    m = len(cuts)
    dp = [[0] * m for _ in range(m)]
    for length in range(2, m):
        for i in range(m - length):
            j = i + length
            dp[i][j] = float("inf")
            for k in range(i + 1, j):  # First cut position
                dp[i][j] = min(dp[i][j],
                    dp[i][k] + dp[k][j] + cuts[j] - cuts[i])
    return dp[0][m - 1]

# Time: O(m^3), Space: O(m^2)
```

---

### 21. Longest Valid Parentheses

Problem: Find length of longest valid (well-formed) parentheses substring.

**Pattern:** 1D DP — dp[i] = longest valid ending at position i.

```python
def longest_valid_parentheses(s):
    dp = [0] * len(s)
    max_len = 0
    for i in range(1, len(s)):
        if s[i] == ")":
            if s[i - 1] == "(":
                dp[i] = (dp[i - 2] if i >= 2 else 0) + 2  # ...() pattern
            elif i - dp[i - 1] - 1 >= 0 and s[i - dp[i - 1] - 1] == "(":
                # ...((...)) pattern: match with char before the valid substring
                dp[i] = dp[i - 1] + 2 + (dp[i - dp[i - 1] - 2] if i - dp[i - 1] - 2 >= 0 else 0)
            max_len = max(max_len, dp[i])
    return max_len

# Time: O(n), Space: O(n)
```

---

### 22. Count Different Palindromic Subsequences

Problem: Count distinct palindromic subsequences (not necessarily contiguous).

**Pattern:** Interval DP with deduplication using next/prev occurrence tracking.

```python
def count_palindromic_subsequences(s):
    mod = 10**9 + 7
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n): dp[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                low, high = i + 1, j - 1
                while low <= high and s[low] != s[i]: low += 1
                while low <= high and s[high] != s[j]: high -= 1
                if low > high:
                    dp[i][j] = 2 * dp[i + 1][j - 1] + 2
                elif low == high:
                    dp[i][j] = 2 * dp[i + 1][j - 1] + 1
                else:
                    dp[i][j] = 2 * dp[i + 1][j - 1] - dp[low + 1][high - 1]
            else:
                dp[i][j] = dp[i + 1][j] + dp[i][j - 1] - dp[i + 1][j - 1]
            dp[i][j] = (dp[i][j] + mod) % mod
    return dp[0][n - 1]

# Time: O(n^2), Space: O(n^2)
```

---

### 23. Maximum Sum of 3 Non-Overlapping Subarrays

Problem: Find 3 non-overlapping subarrays of length k with max sum.

**Pattern:** Precompute left-best and right-best, then try all middle positions.

```python
def max_sum_of_three_subarrays(nums, k):
    n = len(nums)
    sums = [0] * (n - k + 1)
    curr = sum(nums[:k])
    sums[0] = curr
    for i in range(1, len(sums)):
        curr += nums[i + k - 1] - nums[i - 1]
        sums[i] = curr
    # left[i] = index of best subarray in sums[0..i]
    left = [0] * len(sums)
    best = 0
    for i in range(len(sums)):
        if sums[i] > sums[best]:
            best = i
        left[i] = best
    # right[i] = index of best subarray in sums[i..end]
    right = [0] * len(sums)
    best = len(sums) - 1
    for i in range(len(sums) - 1, -1, -1):
        if sums[i] > sums[best]:
            best = i
        right[i] = best
    max_sum = 0
    ans = [-1, -1, -1]
    for mid in range(k, len(sums) - k):
        l, r = left[mid - k], right[mid + k]
        total = sums[l] + sums[mid] + sums[r]
        if total > max_sum:
            max_sum = total
            ans = [l, mid, r]
    return ans

# Time: O(n), Space: O(n)
```

---

### 24. Egg Dropping (SP L3 Version)

Problem: k eggs, n floors. Min drops in worst case.

**Pattern:** 2D DP with binary search optimization — minimax on floor choice.

```python
def super_egg_drop(k, n):
    if k == 1 or n <= 1: return n
    memo = {}
    def dp(e, f):
        if e == 1 or f <= 1: return f
        key = (e, f)
        if key in memo: return memo[key]
        lo, hi = 1, f
        best = float("inf")
        while lo <= hi:
            mid = (lo + hi) // 2
            broken = dp(e - 1, mid - 1)     # Egg breaks → search below
            intact = dp(e, f - mid)           # Egg survives → search above
            if broken > intact:
                hi = mid - 1
            else:
                lo = mid + 1
            best = min(best, 1 + max(broken, intact))
        memo[key] = best
        return best
    return dp(k, n)

# Time: O(k*n*log n), Space: O(k*n)
```

---

### 25. Count Vowels Permutation

Problem: Count strings of length n with vowel ordering constraints.

**Pattern:** State machine DP — 5 states (a,e,i,o,u) with transition rules.

```
Constraints: a→e, e→a or i, i→a/e/o/u, o→i, u→i
dp[a] = (e+i+u) from prev  (only e,i,u can precede a)
dp[e] = (a+i)               (only a,i can precede e)
dp[i] = (e+o)               (only e,o can precede i)
dp[o] = i                    (only i can precede o)
dp[u] = (i+o)               (only i,o can precede u)
```

```python
def count_vowel_permutation(n):
    mod = 10**9 + 7
    a = e = i = o = u = 1  # Base: length 1, each vowel = 1 string
    for _ in range(n - 1):
        # Apply transition rules simultaneously
        a, e, i, o, u = (e + i + u) % mod, (a + i) % mod, (e + o) % mod, i % mod, (i + o) % mod
    return (a + e + i + o + u) % mod

# Time: O(n), Space: O(1)
```

---

## Summary & Study Plan

```
┌────────────┬─────────┬─────────────────────────────────────────────────────────┐
│ Difficulty │ Problems│ Key Techniques to Master                                │
├────────────┼─────────┼─────────────────────────────────────────────────────────┤
│ Easy       │ 1-3     │ 1D DP, Fibonacci recurrence, two-variable state       │
│            │         │ → Practice: climbing stairs, house robber, min cost    │
├────────────┼─────────┼─────────────────────────────────────────────────────────┤
│ Medium     │ 4-8     │ 2D DP tables, LIS (patience sort), LCS, string DP     │
│            │         │ → Practice: fill tables manually, understand transitions│
├────────────┼─────────┼─────────────────────────────────────────────────────────┤
│ Hard       │ 9-15    │ Interval DP, minimax game theory, reverse DP           │
│            │         │ → Practice: burst balloons, dungeon game, stone games  │
├────────────┼─────────┼─────────────────────────────────────────────────────────┤
│ SP L3      │ 16-25   │ Bitmask DP, tree DP, advanced interval, state machine  │
│            │         │ → Practice: TSP, matrix chain, egg drop, vowel perm    │
└────────────┴─────────┴─────────────────────────────────────────────────────────┘

Recommended study order:
  Week 1: Easy (1-3) + Medium (4-8) — master the basics
  Week 2: Hard (9-15) — interval DP and game theory
  Week 3: SP L3 (16-25) — advanced patterns
  Week 4: Mix all — solve under timed conditions (30 min each)
```

### Pattern Summary Table

```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│  Pattern         │ Problems    │ Template                                           │
├───────────────────┼─────────────┼───────────────────────────────────────────────────┤
│  Fibonacci/1D     │ 1, 2, 3     │ dp[i] = f(dp[i-1], dp[i-2])                      │
│  LIS              │ 4           │ Patience sort O(n log n) or O(n²) DP             │
│  Unbounded Knapsack│ 5, 6, 7    │ Coin change, word break (loop L→R for reuse)     │
│  LCS/Edit Distance│ 8, 10       │ 2D match/no-match transition                     │
│  Interval DP      │ 9, 12, 18, 19, 20 │ dp[i][j] on subarrays, fill by length    │
│  Reverse DP       │ 14          │ Work backwards (dungeon game)                     │
│  Game/Minimax     │ 15          │ dp[i] = best when opponent plays optimally       │
│  Bitmask DP       │ 16          │ dp[mask][last] for visiting subsets of cities    │
│  Tree DP          │ 17          │ Post-order DFS, (take, skip) tuple return        │
│  State Machine    │ 25          │ 5 vowel states with transition rules             │
│  Precompute+DP    │ 22, 23      │ Build palindrome table, then 1D DP on top       │
│  Binary Search DP │ 24          │ Minimax with BS on optimal floor choice          │
└───────────────────┴─────────────┴───────────────────────────────────────────────────┘
```
