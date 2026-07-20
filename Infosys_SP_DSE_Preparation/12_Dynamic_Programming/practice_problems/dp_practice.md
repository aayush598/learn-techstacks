# DP Practice Problems for Infosys SP DSE

25 carefully curated problems in order of difficulty.

---

## EASY

### 1. Climbing Stairs

Problem: n steps, climb 1 or 2 steps at a time. Count ways to reach top.

DP Approach: dp[n] = dp[n-1] + dp[n-2] (Fibonacci)

def climb_stairs(n):
    if n <= 1: return 1
    a, b = 1, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b

# Time: O(n), Space: O(1)

def climb_stairs_memo(n, memo=None):
    if memo is None: memo = {}
    if n <= 1: return 1
    if n in memo: return memo[n]
    memo[n] = climb_stairs_memo(n-1, memo) + climb_stairs_memo(n-2, memo)
    return memo[n]

---

### 2. House Robber

Problem: Adjacent houses cannot be robbed together. Maximize sum.

def rob(nums):
    prev2 = prev1 = 0
    for num in nums:
        curr = max(prev1, prev2 + num)
        prev2, prev1 = prev1, curr
    return prev1

# Time: O(n), Space: O(1)

---

### 3. Min Cost Climbing Stairs

Problem: cost[i] to step on stair i. Start at 0 or 1. Find min cost to reach top.

def min_cost_climbing(cost):
    a, b = cost[0], cost[1]
    for i in range(2, len(cost)):
        a, b = b, cost[i] + min(a, b)
    return min(a, b)

# Time: O(n), Space: O(1)

---

## MEDIUM

### 4. Longest Increasing Subsequence

Problem: Find length of LIS.

def length_of_lis(nums):
    import bisect
    piles = []
    for num in nums:
        i = bisect.bisect_left(piles, num)
        if i == len(piles):
            piles.append(num)
        else:
            piles[i] = num
    return len(piles)

# Time: O(n log n), Space: O(n)

def length_of_lis_n2(nums):
    if not nums: return 0
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

---

### 5. Coin Change

Problem: Minimum coins to make amount. Unlimited supply.

def coin_change(coins, amount):
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a-coin] + 1)
    return dp[amount] if dp[amount] != float("inf") else -1

# Time: O(n*amount), Space: O(amount)

def coin_change_memo(coins, amount, memo=None):
    if memo is None: memo = {}
    if amount == 0: return 0
    if amount < 0: return float("inf")
    if amount in memo: return memo[amount]
    best = float("inf")
    for coin in coins:
        res = coin_change_memo(coins, amount-coin, memo)
        if res != float("inf"):
            best = min(best, 1 + res)
    memo[amount] = best
    return best

---

### 6. Word Break

Problem: Can s be segmented using words from dictionary?

def word_break(s, word_dict):
    words = set(word_dict)
    n = len(s)
    dp = [False]*(n+1)
    dp[0] = True
    for i in range(1, n+1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[n]

# Time: O(n^2), Space: O(n)

---

### 7. Unique Paths

Problem: m x n grid. Move right/down. Count paths to bottom-right.

def unique_paths(m, n):
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    return dp[-1]

# Time: O(m*n), Space: O(n)

def unique_paths_memo(m, n, i=0, j=0, memo=None):
    if memo is None: memo = {}
    if i == m-1 and j == n-1: return 1
    if i >= m or j >= n: return 0
    key = (i, j)
    if key in memo: return memo[key]
    memo[key] = unique_paths_memo(m, n, i+1, j, memo) + unique_paths_memo(m, n, i, j+1, memo)
    return memo[key]

---

### 8. Longest Common Subsequence

Problem: Given two strings, find LCS length.

def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# Time: O(m*n), Space: O(m*n)

def longest_common_subsequence_optimized(text1, text2):
    if len(text1) < len(text2): text1, text2 = text2, text1
    m, n = len(text1), len(text2)
    prev = [0]*(n+1)
    for i in range(1, m+1):
        curr = [0]*(n+1)
        for j in range(1, n+1):
            if text1[i-1] == text2[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(prev[j], curr[j-1])
        prev = curr
    return prev[n]

# Time: O(m*n), Space: O(min(m,n))

---

## HARD

### 9. Burst Balloons

Problem: Burst balloon i, get nums[i-1]*nums[i]*nums[i+1]. Max coins.

def max_coins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0]*n for _ in range(n)]
    for length in range(2, n):
        for i in range(n-length):
            j = i + length
            for k in range(i+1, j):
                dp[i][j] = max(dp[i][j],
                    nums[i]*nums[k]*nums[j] + dp[i][k] + dp[k][j])
    return dp[0][n-1]

# Time: O(n^3), Space: O(n^2)

def max_coins_memo(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    memo = {}
    def solve(l, r):
        if l >= r-1: return 0
        key = (l, r)
        if key in memo: return memo[key]
        best = 0
        for k in range(l+1, r):
            coins = nums[l]*nums[k]*nums[r] + solve(l, k) + solve(k, r)
            best = max(best, coins)
        memo[key] = best
        return best
    return solve(0, n-1)

---

### 10. Edit Distance

Problem: Min ops (insert, delete, replace) to convert word1 to word2.

def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    prev = list(range(n+1))
    for i in range(1, m+1):
        curr = [0]*(n+1)
        curr[0] = i
        for j in range(1, n+1):
            if word1[i-1] == word2[j-1]:
                curr[j] = prev[j-1]
            else:
                curr[j] = 1 + min(prev[j], curr[j-1], prev[j-1])
        prev = curr
    return prev[n]

# Time: O(m*n), Space: O(n)

---

### 11. Regular Expression Matching

Problem: Implement "." and "*" regex matching.

def is_match(s, p):
    m, n = len(s), len(p)
    dp = [[False]*(n+1) for _ in range(m+1)]
    dp[0][0] = True
    for j in range(2, n+1):
        if p[j-1] == "*":
            dp[0][j] = dp[0][j-2]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if p[j-1] == s[i-1] or p[j-1] == ".":
                dp[i][j] = dp[i-1][j-1]
            elif p[j-1] == "*":
                dp[i][j] = dp[i][j-2]
                if p[j-2] == s[i-1] or p[j-2] == ".":
                    dp[i][j] = dp[i][j] or dp[i-1][j]
    return dp[m][n]

---

### 12. Longest Palindromic Subsequence

Problem: Find length of longest palindromic subsequence.

def longest_palindrome_subseq(s):
    n = len(s)
    dp = [[0]*n for _ in range(n)]
    for i in range(n-1, -1, -1):
        dp[i][i] = 1
        for j in range(i+1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i+1][j-1] + 2
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j-1])
    return dp[0][n-1]

# Time: O(n^2), Space: O(n^2)

---

### 13. Maximal Rectangle

Problem: Find largest rectangle of 1s in binary matrix.

def maximal_rectangle(matrix):
    if not matrix: return 0
    n = len(matrix[0])
    heights = [0]*n
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

---

### 14. Dungeon Game

Problem: Min initial health needed for knight to reach princess.

def calculate_minimum_hp(dungeon):
    m, n = len(dungeon), len(dungeon[0])
    dp = [[float("inf")]*(n+1) for _ in range(m+1)]
    dp[m][n-1] = dp[m-1][n] = 1
    for i in range(m-1, -1, -1):
        for j in range(n-1, -1, -1):
            need = min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j]
            dp[i][j] = max(1, need)
    return dp[0][0]

# Time: O(m*n), Space: O(m*n)

---

### 15. Stone Game III

Problem: Alice and Bob take 1-3 stones from front. Maximize Alice score.

def stone_game_iii(values):
    n = len(values)
    dp = [float("-inf")]*(n+1)
    dp[n] = 0
    suffix = [0]*(n+1)
    for i in range(n-1, -1, -1):
        suffix[i] = suffix[i+1] + values[i]
    for i in range(n-1, -1, -1):
        for take in range(1, 4):
            if i + take <= n:
                dp[i] = max(dp[i], suffix[i] - dp[i+take])
    a, b = dp[0], suffix[0] - dp[0]
    return "Alice" if a > b else ("Bob" if b > a else "Tie")

# Time: O(n), Space: O(n)

---

## SP L3 LEVEL

### 16. TSP (Bitmask DP)

Problem: Shortest tour visiting all cities and returning.

def tsp(cost):
    n = len(cost)
    INF = 10**9
    dp = [[INF]*n for _ in range(1<<n)]
    dp[1][0] = 0
    for mask in range(1<<n):
        for last in range(n):
            if not (mask>>last & 1): continue
            if dp[mask][last] == INF: continue
            for nxt in range(n):
                if (mask>>nxt) & 1: continue
                dp[mask|(1<<nxt)][nxt] = min(dp[mask|(1<<nxt)][nxt], dp[mask][last] + cost[last][nxt])
    full = (1<<n)-1
    ans = INF
    for i in range(1, n):
        if cost[i][0]:
            ans = min(ans, dp[full][i] + cost[i][0])
    return ans

# Time: O(2^n * n^2), Space: O(2^n * n)

---

### 17. Tree DP - Max Independent Set

Problem: In a tree, find max weight set of non-adjacent nodes.

def max_independent_set_tree(root):
    def dfs(node):
        if not node: return (0, 0)
        left = dfs(node.left)
        right = dfs(node.right)
        take = node.val + left[1] + right[1]
        skip = max(left) + max(right)
        return (take, skip)
    return max(dfs(root))

# Time: O(n), Space: O(h)

---

### 18. Interval DP - Matrix Chain

Problem: Min scalar multiplications for matrix chain.

def matrix_chain(p):
    n = len(p) - 1
    dp = [[0]*n for _ in range(n)]
    for length in range(2, n+1):
        for i in range(n-length+1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                q = dp[i][k] + dp[k+1][j] + p[i]*p[k+1]*p[j+1]
                dp[i][j] = min(dp[i][j], q)
    return dp[0][n-1]

# Time: O(n^3), Space: O(n^2)

---

### 19. Palindrome Partitioning II

Problem: Min cuts to partition string into palindromes.

def min_cut(s):
    n = len(s)
    if n <= 1: return 0
    pal = [[False]*n for _ in range(n)]
    for i in range(n-1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j-i <= 2 or pal[i+1][j-1]):
                pal[i][j] = True
    dp = [float("inf")]*n
    for i in range(n):
        if pal[0][i]:
            dp[i] = 0
        else:
            for j in range(i):
                if pal[j+1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)
    return dp[n-1]

# Time: O(n^2), Space: O(n^2)

---

### 20. Minimum Cost to Cut Stick

Problem: Cut stick at given positions. Cost is current stick length. Min total cost.

def min_cost(n, cuts):
    cuts = [0] + sorted(cuts) + [n]
    m = len(cuts)
    dp = [[0]*m for _ in range(m)]
    for length in range(2, m):
        for i in range(m-length):
            j = i + length
            dp[i][j] = float("inf")
            for k in range(i+1, j):
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cuts[j] - cuts[i])
    return dp[0][m-1]

# Time: O(m^3), Space: O(m^2)

---

### 21. Longest Valid Parentheses

Problem: Find length of longest valid (well-formed) parentheses substring.

def longest_valid_parentheses(s):
    dp = [0]*len(s)
    max_len = 0
    for i in range(1, len(s)):
        if s[i] == ")":
            if s[i-1] == "(":
                dp[i] = (dp[i-2] if i>=2 else 0) + 2
            elif i-dp[i-1]-1 >= 0 and s[i-dp[i-1]-1] == "(":
                dp[i] = dp[i-1] + 2 + (dp[i-dp[i-1]-2] if i-dp[i-1]-2 >= 0 else 0)
            max_len = max(max_len, dp[i])
    return max_len

# Time: O(n), Space: O(n)

---

### 22. Count Different Palindromic Subsequences

Problem: Count distinct palindromic subsequences (not necessarily contiguous).

def count_palindromic_subsequences(s):
    mod = 10**9 + 7
    n = len(s)
    dp = [[0]*n for _ in range(n)]
    for i in range(n): dp[i][i] = 1
    for length in range(2, n+1):
        for i in range(n-length+1):
            j = i + length - 1
            if s[i] == s[j]:
                low, high = i+1, j-1
                while low <= high and s[low] != s[i]: low += 1
                while low <= high and s[high] != s[j]: high -= 1
                if low > high:
                    dp[i][j] = 2*dp[i+1][j-1] + 2
                elif low == high:
                    dp[i][j] = 2*dp[i+1][j-1] + 1
                else:
                    dp[i][j] = 2*dp[i+1][j-1] - dp[low+1][high-1]
            else:
                dp[i][j] = dp[i+1][j] + dp[i][j-1] - dp[i+1][j-1]
            dp[i][j] = (dp[i][j] + mod) % mod
    return dp[0][n-1]

# Time: O(n^2), Space: O(n^2)

---

### 23. Maximum Sum of 3 Non-Overlapping Subarrays

Problem: Find 3 non-overlapping subarrays of length k with max sum.

def max_sum_of_three_subarrays(nums, k):
    n = len(nums)
    sums = [0]*(n-k+1)
    curr = sum(nums[:k])
    sums[0] = curr
    for i in range(1, len(sums)):
        curr += nums[i+k-1] - nums[i-1]
        sums[i] = curr
    left = [0]*len(sums)
    best = 0
    for i in range(len(sums)):
        if sums[i] > sums[best]:
            best = i
        left[i] = best
    right = [0]*len(sums)
    best = len(sums)-1
    for i in range(len(sums)-1, -1, -1):
        if sums[i] > sums[best]:
            best = i
        right[i] = best
    max_sum = 0
    ans = [-1, -1, -1]
    for mid in range(k, len(sums)-k):
        l, r = left[mid-k], right[mid+k]
        total = sums[l] + sums[mid] + sums[r]
        if total > max_sum:
            max_sum = total
            ans = [l, mid, r]
    return ans

# Time: O(n), Space: O(n)

---

### 24. Egg Dropping (SP L3 Version)

Problem: k eggs, n floors. Min drops in worst case.

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
            mid = (lo+hi)//2
            broken = dp(e-1, mid-1)
            intact = dp(e, f-mid)
            if broken > intact:
                hi = mid-1
            else:
                lo = mid+1
            best = min(best, 1 + max(broken, intact))
        memo[key] = best
        return best
    return dp(k, n)

# Time: O(k*n*log n), Space: O(k*n)

---

### 25. Count Vowels Permutation

Problem: Count strings of length n with vowel ordering constraints.

def count_vowel_permutation(n):
    mod = 10**9 + 7
    a = e = i = o = u = 1
    for _ in range(n-1):
        a, e, i, o, u = (e+i+u) % mod, (a+i) % mod, (e+o) % mod, i % mod, (i+o) % mod
    return (a+e+i+o+u) % mod

# Time: O(n), Space: O(1)

---

## Summary

| Difficulty | Problems | Key Technique |
|------------|----------|---------------|
| Easy | 1-3 | 1D DP, Fibonacci style |
| Medium | 4-8 | 2D DP, LIS, strings |
| Hard | 9-15 | Interval DP, minimax, game theory |
| SP L3 | 16-25 | Bitmask, tree DP, advanced interval |
