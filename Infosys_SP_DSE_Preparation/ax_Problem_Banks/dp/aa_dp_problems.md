# Dynamic Programming - Complete Problem Bank (55 Problems)

> **THE MOST CRITICAL TOPIC** - Hard/Complex problems in Infosys SP DSE are ALWAYS DP.
> Master every pattern here. DP is not about memorizing - it's about recognizing states and transitions.

---

## Table of Contents

| Section | Problems | Difficulty |
|---------|----------|------------|
| [Easy (1-10)](#easy-problems) | Climbing Stairs, Min Cost, House Robber, Fibonacci, Kadane's, etc. | Easy |
| [Medium (11-35)](#medium-problems) | LIS, Coin Change, LCS, Subset Sum, Grid DP, etc. | Medium |
| [Hard (36-55)](#hard-problems) | Edit Distance, Burst Balloons, Egg Drop, Pattern Matching, etc. | Hard |

---

# Easy Problems

---

## Problem 1: Climbing Stairs

### Problem Statement
You are climbing a staircase with `n` steps. Each time you can climb 1 or 2 steps. In how many distinct ways can you reach the top?

### Approach
- **State**: `dp[i]` = number of ways to reach step `i`
- **Recurrence**: `dp[i] = dp[i-1] + dp[i-2]` (came from step i-1 taking 1 step, or i-2 taking 2 steps)
- **Base Cases**: `dp[0] = 1` (one way to stay at ground), `dp[1] = 1`
- **Note**: This is essentially Fibonacci with different base cases.

### Python Code (Tabulation + Space Optimized)

```python
def climbStairs(n: int) -> int:
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for i in range(3, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1
```

### Complexity
- **Time**: O(n)
- **Space**: O(1)

### Trick/Tip
This is the gateway DP problem. If you can't solve this, you need to revisit fundamentals. The pattern `dp[i] = dp[i-1] + dp[i-2]` appears everywhere.

---

## Problem 2: Min Cost Climbing Stairs

### Problem Statement
You are given an integer array `cost` where `cost[i]` is the cost of the `i-th` step. Once you pay the cost, you can climb 1 or 2 steps. You can start from step 0 or step 1. Find the minimum cost to reach the top.

### Approach
- **State**: `dp[i]` = minimum cost to reach step `i`
- **Recurrence**: `dp[i] = cost[i] + min(dp[i-1], dp[i-2])`
- **Base Cases**: `dp[0] = cost[0]`, `dp[1] = cost[1]`
- **Answer**: `min(dp[n-1], dp[n-2])` (can reach top from either last or second-to-last step)

### Python Code (Tabulation + Space Optimized)

```python
def minCostClimbingStairs(cost: list[int]) -> int:
    n = len(cost)
    if n == 2:
        return min(cost[0], cost[1])
    prev2, prev1 = cost[0], cost[1]
    for i in range(2, n):
        curr = cost[i] + min(prev1, prev2)
        prev2 = prev1
        prev1 = curr
    return min(prev1, prev2)
```

### Complexity
- **Time**: O(n)
- **Space**: O(1)

### Trick/Tip
The key insight is the answer is `min(dp[n-1], dp[n-2])` not just `dp[n-1]` because you can step off from either of the last two positions.

---

## Problem 3: House Robber

### Problem Statement
You are a robber planning to rob houses along a street. Each house has a certain amount of money. The only constraint is that you cannot rob two adjacent houses (they have connected security systems). Given an array `nums` representing money in each house, return the maximum amount you can rob.

### Approach
- **State**: `dp[i]` = maximum money you can rob from houses `0..i`
- **Recurrence**: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`
  - Either skip house `i` (take `dp[i-1]`) or rob house `i` (add `nums[i]` to `dp[i-2]`)
- **Base Cases**: `dp[0] = nums[0]`, `dp[1] = max(nums[0], nums[1])`

### Python Code (Tabulation + Space Optimized)

```python
def rob(nums: list[int]) -> int:
    n = len(nums)
    if n == 1:
        return nums[0]
    if n == 2:
        return max(nums[0], nums[1])
    prev2, prev1 = nums[0], max(nums[0], nums[1])
    for i in range(2, n):
        curr = max(prev1, prev2 + nums[i])
        prev2 = prev1
        prev1 = curr
    return prev1
```

### Complexity
- **Time**: O(n)
- **Space**: O(1)

### Trick/Tip
This is the classic "skip or take" pattern. The recurrence `max(take, skip)` appears in many DP problems including stock problems, knapsack variants, etc.

---

## Problem 4: Fibonacci Number

### Problem Statement
Given `n`, calculate `F(n)` where `F(0) = 0`, `F(1) = 1`, and `F(n) = F(n-1) + F(n-2)` for `n > 1`.

### Approach
- **State**: `dp[i]` = `i-th` Fibonacci number
- **Recurrence**: `dp[i] = dp[i-1] + dp[i-2]`
- **Base Cases**: `dp[0] = 0`, `dp[1] = 1`

### Python Code (Space Optimized)

```python
def fib(n: int) -> int:
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1
```

### Python Code (Memoization)

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_memo(n: int) -> int:
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)
```

### Complexity
- **Time**: O(n) for iterative, O(n) for memoization
- **Space**: O(1) for iterative, O(n) for memoization

### Trick/Tip
Every DP problem is essentially a generalized Fibonacci. If you understand this, you understand the core idea of DP: overlapping subproblems + optimal substructure.

---

## Problem 5: Maximum Subarray (Kadane's Algorithm)

### Problem Statement
Given an integer array `nums`, find the subarray with the largest sum and return its sum. A subarray is a contiguous non-empty sequence of elements.

### Approach
- **State**: `dp[i]` = maximum sum of subarray ending at index `i`
- **Recurrence**: `dp[i] = max(nums[i], dp[i-1] + nums[i])`
  - Either start fresh at `i` or extend the previous subarray
- **Base Case**: `dp[0] = nums[0]`
- **Answer**: `max(dp)` — maximum over all ending positions

### Python Code (Space Optimized - O(1))

```python
def maxSubArray(nums: list[int]) -> int:
    max_sum = curr_sum = nums[0]
    for i in range(1, len(nums)):
        curr_sum = max(nums[i], curr_sum + nums[i])
        max_sum = max(max_sum, curr_sum)
    return max_sum
```

### Python Code (Full DP with Index Tracking)

```python
def maxSubArrayWithIndices(nums: list[int]) -> tuple[int, int, int]:
    max_sum = curr_sum = nums[0]
    start = end = temp_start = 0
    for i in range(1, len(nums)):
        if nums[i] > curr_sum + nums[i]:
            curr_sum = nums[i]
            temp_start = i
        else:
            curr_sum += nums[i]
        if curr_sum > max_sum:
            max_sum = curr_sum
            start = temp_start
            end = i
    return max_sum, start, end
```

### Complexity
- **Time**: O(n)
- **Space**: O(1)

### Trick/Tip
Kadane's algorithm is greedy-DP hybrid. The key insight: if the running sum becomes negative, it's never beneficial to carry it forward. This is THE most frequently asked easy DP.

---

## Problem 6: Maximum Product Subarray

### Problem Statement
Given an integer array `nums`, find the subarray with the largest product and return the product.

### Approach
- **State**: `dp_max[i]` = max product of subarray ending at `i`, `dp_min[i]` = min product (because negative × negative = positive)
- **Recurrence**:
  - `dp_max[i] = max(nums[i], dp_max[i-1] * nums[i], dp_min[i-1] * nums[i])`
  - `dp_min[i] = min(nums[i], dp_max[i-1] * nums[i], dp_min[i-1] * nums[i])`
- **Base Cases**: `dp_max[0] = dp_min[0] = nums[0]`

### Python Code (Space Optimized)

```python
def maxProduct(nums: list[int]) -> int:
    result = max_val = min_val = nums[0]
    for i in range(1, len(nums)):
        num = nums[i]
        if num < 0:
            max_val, min_val = min_val, max_val
        max_val = max(num, max_val * num)
        min_val = min(num, min_val * num)
        result = max(result, max_val)
    return result
```

### Complexity
- **Time**: O(n)
- **Space**: O(1)

### Trick/Tip
The trick is tracking BOTH min and max because a large negative can become the largest when multiplied by another negative. When current number is negative, swap max and min.

---

## Problem 7: Decode Ways

### Problem Statement
A message consisting of letters A-Z is encoded using numerical mapping: A→1, B→2, ..., Z→26. Given a string `s` of digits, return the total number of ways to decode it.

### Approach
- **State**: `dp[i]` = number of ways to decode substring `s[0:i]`
- **Recurrence**:
  - If `s[i-1] != '0'`: `dp[i] += dp[i-1]` (single digit decode)
  - If `s[i-2:i]` forms valid 10-26: `dp[i] += dp[i-2]` (two digit decode)
- **Base Cases**: `dp[0] = 1` (empty string has one way), `dp[1] = 1 if s[0] != '0' else 0`

### Python Code (Space Optimized)

```python
def numDecodings(s: str) -> int:
    if not s or s[0] == '0':
        return 0
    prev2, prev1 = 1, 1
    for i in range(1, len(s)):
        curr = 0
        if s[i] != '0':
            curr += prev1
        two_digit = int(s[i-1:i+1])
        if 10 <= two_digit <= 26:
            curr += prev2
        prev2, prev1 = prev1, curr
    return prev1
```

### Complexity
- **Time**: O(n)
- **Space**: O(1)

### Trick/Tip
Watch out for leading zeros and numbers > 26. The string "27" cannot be decoded as a two-digit number. Always check the two-digit window is in range [10, 26].

---

## Problem 8: Best Time to Buy and Sell Stock

### Problem Statement
Given an array `prices` where `prices[i]` is the price of a stock on the `i-th` day, find the maximum profit from one buy and one sell. You must buy before selling. Return 0 if no profit possible.

### Approach
- **State**: Track the minimum price seen so far
- **Logic**: At each day, calculate profit if we sell today (`prices[i] - min_price`), update max profit
- **No formal DP array needed** — this is greedy-DP

### Python Code

```python
def maxProfit(prices: list[int]) -> int:
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit
```

### Complexity
- **Time**: O(n)
- **Space**: O(1)

### Trick/Tip
This is the simplest stock problem. The key insight: track the minimum price seen so far, and at each step calculate the profit if you sold today.

---

## Problem 9: Best Time to Buy and Sell Stock with Cooldown

### Problem Statement
After selling your stock, you must wait one day before buying again (cooldown period). Find the maximum profit.

### Approach
- **States**: `hold[i]` = max profit on day `i` if holding stock, `sold[i]` = max profit on day `i` if just sold, `rest[i]` = max profit on day `i` if resting
- **Recurrence**:
  - `hold[i] = max(hold[i-1], rest[i-1] - prices[i])` (keep holding or buy after cooldown)
  - `sold[i] = hold[i-1] + prices[i]` (sell today)
  - `rest[i] = max(rest[i-1], sold[i-1])` (keep resting or just finished cooldown)

### Python Code (Space Optimized)

```python
def maxProfit(prices: list[int]) -> int:
    if len(prices) <= 1:
        return 0
    hold = -prices[0]
    sold = 0
    rest = 0
    for i in range(1, len(prices)):
        prev_hold = hold
        hold = max(hold, rest - prices[i])
        rest = max(rest, sold)
        sold = prev_hold + prices[i]
    return max(sold, rest)
```

### Complexity
- **Time**: O(n)
- **Space**: O(1)

### Trick/Tip
Stock problems are state machine DP. Define states (hold/sold/rest) and transitions between them. Cooldown adds a delay between sell and next buy.

---

## Problem 10: Paint Fence

### Problem Statement
Given `n` fence posts and `k` colors, paint each post one color such that no more than two adjacent posts have the same color. Return the number of ways.

### Approach
- **State**: `same[i]` = ways to paint `i` posts where post `i` same color as `i-1`, `diff[i]` = ways where different
- **Recurrence**:
  - `same[i] = diff[i-1]` (must change from different to make same)
  - `diff[i] = (same[i-1] + diff[i-1]) * (k-1)` (from either state, pick any of k-1 different colors)
- **Base Cases**: `same[2] = k`, `diff[2] = k * (k-1)`
- **Answer**: `same[n] + diff[n]`

### Python Code (Space Optimized)

```python
def numWays(n: int, k: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return k
    if n == 2:
        return k * k
    same, diff = k, k * (k - 1)
    for i in range(3, n + 1):
        same, diff = diff, (same + diff) * (k - 1)
    return same + diff
```

### Complexity
- **Time**: O(n)
- **Space**: O(1)

### Trick/Tip
The constraint "no more than 2 adjacent same" means you CAN have exactly 2 adjacent same but NOT 3. Split into same/different states to handle this cleanly.

---

# Medium Problems

---

## Problem 11: House Robber II

### Problem Statement
Houses are arranged in a circle. If you rob house 0, you cannot rob house `n-1` (and vice versa). Find the maximum money you can rob.

### Approach
- **Key Insight**: If houses are circular, either you don't rob house 0 OR you don't rob house `n-1`. So solve House Robber twice:
  1. On houses `0..n-2` (exclude last)
  2. On houses `1..n-1` (exclude first)
- Answer is `max(both)`

### Python Code

```python
def rob(nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]
    if len(nums) == 2:
        return max(nums[0], nums[1])

    def rob_linear(houses: list[int]) -> int:
        prev2, prev1 = 0, 0
        for h in houses:
            prev2, prev1 = prev1, max(prev1, prev2 + h)
        return prev1

    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

### Complexity
- **Time**: O(n)
- **Space**: O(1)

### Trick/Tip
Circular constraint → break into two linear subproblems. This trick appears in many circular arrangement problems. Don't try to handle the circularity directly.

---

## Problem 12: Longest Increasing Subsequence (O(n²))

### Problem Statement
Given an integer array `nums`, return the length of the longest strictly increasing subsequence.

### Approach
- **State**: `dp[i]` = length of LIS ending at index `i`
- **Recurrence**: `dp[i] = 1 + max(dp[j])` for all `j < i` where `nums[j] < nums[i]`
- **Base Case**: `dp[i] = 1` (every element is a subsequence of length 1)
- **Answer**: `max(dp)`

### Python Code (Tabulation)

```python
def lengthOfLIS(nums: list[int]) -> int:
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

### Python Code (Memoization)

```python
def lengthOfLIS_memo(nums: list[int]) -> int:
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dfs(i: int) -> int:
        best = 1
        for j in range(i):
            if nums[j] < nums[i]:
                best = max(best, dfs(j) + 1)
        return best

    return max(dfs(i) for i in range(len(nums)))
```

### Complexity
- **Time**: O(n²)
- **Space**: O(n)

### Trick/Tip
The O(n²) solution is the standard approach. For each element, look back at all previous elements. If you need O(n log n), see Problem 13.

---

## Problem 13: Longest Increasing Subsequence (O(n log n))

### Problem Statement
Same as Problem 12, but with optimal time complexity.

### Approach
- **Idea**: Maintain a `tails` array where `tails[i]` is the smallest possible tail element for an increasing subsequence of length `i+1`
- For each number, use binary search to find its position in `tails`:
  - If larger than all tails → append
  - Otherwise → replace the first tail that is >= num
- The length of `tails` at the end is the LIS length

### Python Code

```python
import bisect

def lengthOfLIS(nums: list[int]) -> int:
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)
```

### Complexity
- **Time**: O(n log n)
- **Space**: O(n)

### Trick/Tip
The `tails` array is NOT the actual LIS — it's a structure that helps us determine the length efficiently. To reconstruct the actual LIS, you need parent pointers. The binary search replaces linear scan.

---

## Problem 14: Coin Change

### Problem Statement
Given an integer array `coins` and an integer `amount`, return the fewest number of coins needed to make up `amount`. If not possible, return -1.

### Approach
- **State**: `dp[i]` = minimum coins to make amount `i`
- **Recurrence**: `dp[i] = min(dp[i - coin] + 1)` for each coin where `i - coin >= 0`
- **Base Case**: `dp[0] = 0` (0 coins needed for amount 0)
- **Initialization**: All values to `amount + 1` (infinity)

### Python Code (Tabulation)

```python
def coinChange(coins: list[int], amount: int) -> int:
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != amount + 1 else -1
```

### Python Code (Memoization)

```python
def coinChange_memo(coins: list[int], amount: int) -> int:
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dfs(remaining: int) -> int:
        if remaining == 0:
            return 0
        if remaining < 0:
            return float('inf')
        best = float('inf')
        for coin in coins:
            best = min(best, dfs(remaining - coin) + 1)
        return best

    result = dfs(amount)
    return result if result != float('inf') else -1
```

### Complexity
- **Time**: O(amount × len(coins))
- **Space**: O(amount)

### Trick/Tip
This is the classic unbounded knapsack variant. The order of loops matters: outer loop over amounts ensures each coin is counted once per subproblem. Initialize with `amount + 1` as infinity sentinel.

---

## Problem 15: Coin Change II

### Problem Statement
Given `coins` and `amount`, return the number of combinations that make up the amount. Each coin can be used unlimited times.

### Approach
- **State**: `dp[i]` = number of ways to make amount `i`
- **Recurrence**: `dp[i] += dp[i - coin]` for each coin
- **Base Case**: `dp[0] = 1` (one way to make amount 0: use no coins)
- **Loop Order**: Amount outer, coins inner (avoids counting permutations as different combinations)

### Python Code

```python
def change(amount: int, coins: list[int]) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    return dp[amount]
```

### Complexity
- **Time**: O(amount × len(coins))
- **Space**: O(amount)

### Trick/Tip
**Critical**: The loop order determines combinations vs permutations. Coins outer + amounts inner → combinations. Amounts outer + coins inner → permutations (Problem 25). This is the #1 mistake people make.

---

## Problem 16: Word Break

### Problem Statement
Given a string `s` and a dictionary of words `wordDict`, return `True` if `s` can be segmented into a space-separated sequence of dictionary words.

### Approach
- **State**: `dp[i]` = can `s[0:i]` be segmented
- **Recurrence**: `dp[i] = True` if there exists `j < i` such that `dp[j] = True` AND `s[j:i]` in `wordDict`
- **Base Case**: `dp[0] = True` (empty string can always be segmented)

### Python Code (Tabulation)

```python
def wordBreak(s: str, wordDict: list[str]) -> bool:
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]
```

### Python Code (Memoization)

```python
def wordBreak_memo(s: str, wordDict: list[str]) -> bool:
    word_set = set(wordDict)
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dfs(start: int) -> bool:
        if start == len(s):
            return True
        for end in range(start + 1, len(s) + 1):
            if s[start:end] in word_set and dfs(end):
                return True
        return False

    return dfs(0)
```

### Complexity
- **Time**: O(n² × k) where k is average word length for substring comparison
- **Space**: O(n)

### Trick/Tip
Convert `wordDict` to a set for O(1) lookup. The order of checking matters: for each position `i`, check all possible previous breakpoints `j`.

---

## Problem 17: Unique Paths

### Problem Statement
Given an `m x n` grid, find the number of unique paths from the top-left corner to the bottom-right corner, moving only right or down at each step.

### Approach
- **State**: `dp[i][j]` = number of unique paths to reach cell `(i, j)`
- **Recurrence**: `dp[i][j] = dp[i-1][j] + dp[i][j-1]`
- **Base Cases**: `dp[0][j] = 1` for all `j`, `dp[i][0] = 1` for all `i`

### Python Code (Space Optimized)

```python
def uniquePaths(m: int, n: int) -> int:
    dp = [1] * n
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    return dp[n - 1]
```

### Complexity
- **Time**: O(m × n)
- **Space**: O(n)

### Trick/Tip
This is combinatorics: answer = C(m+n-2, m-1). But DP is the general approach when obstacles/costs are added. The 1D space optimization works because each row only depends on the row above.

---

## Problem 18: Unique Paths with Obstacles

### Problem Statement
Given an `m x n` grid with obstacles (1 = obstacle, 0 = empty), find unique paths from top-left to bottom-right. You cannot step on obstacles.

### Approach
- **State**: `dp[i][j]` = number of unique paths to `(i, j)` avoiding obstacles
- **Recurrence**: `dp[i][j] = dp[i-1][j] + dp[i][j-1]` if `grid[i][j] = 0`, else `dp[i][j] = 0`
- **Base Case**: If `grid[0][0] = 1`, return 0

### Python Code

```python
def uniquePathsWithObstacles(obstacleGrid: list[list[int]]) -> int:
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    if obstacleGrid[0][0] == 1 or obstacleGrid[m-1][n-1] == 1:
        return 0
    dp = [0] * n
    dp[0] = 1
    for i in range(m):
        for j in range(n):
            if obstacleGrid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j - 1]
    return dp[n - 1]
```

### Complexity
- **Time**: O(m × n)
- **Space**: O(n)

### Trick/Tip
When you hit an obstacle, set dp[j] = 0 because no paths can go through that cell. The space-optimized version needs to handle the first column carefully.

---

## Problem 19: Minimum Path Sum

### Problem Statement
Given an `m x n` grid filled with non-negative numbers, find a path from top-left to bottom-right that minimizes the sum of numbers along the path (moving only right or down).

### Approach
- **State**: `dp[i][j]` = minimum sum to reach `(i, j)`
- **Recurrence**: `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`
- **Base Cases**: First row and first column are cumulative sums

### Python Code (Space Optimized)

```python
def minPathSum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [0] * n
    dp[0] = grid[0][0]
    for j in range(1, n):
        dp[j] = dp[j-1] + grid[0][j]
    for i in range(1, m):
        dp[0] += grid[i][0]
        for j in range(1, n):
            dp[j] = grid[i][j] + min(dp[j], dp[j-1])
    return dp[n - 1]
```

### Complexity
- **Time**: O(m × n)
- **Space**: O(n)

### Trick/Tip
For the first row/column, there's only one way to reach (only right or only down), so accumulate the grid values directly.

---

## Problem 20: Longest Common Subsequence

### Problem Statement
Given two strings `text1` and `text2`, return the length of their longest common subsequence (not necessarily contiguous).

### Approach
- **State**: `dp[i][j]` = LCS length of `text1[0:i]` and `text2[0:j]`
- **Recurrence**:
  - If `text1[i-1] == text2[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`
  - Else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`
- **Base Cases**: `dp[0][j] = 0`, `dp[i][0] = 0`

### Python Code (Space Optimized)

```python
def longestCommonSubsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    if m < n:
        text1, text2, m, n = text2, text1, n, m
    dp = [0] * (n + 1)
    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if text1[i-1] == text2[j-1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            prev = temp
    return dp[n]
```

### Complexity
- **Time**: O(m × n)
- **Space**: O(min(m, n))

### Trick/Tip
LCS is the foundation of many string DP problems (Edit Distance, Shortest Common Supersequence). The space optimization requires careful handling of the diagonal value (prev).

---

## Problem 21: Longest Common Substring

### Problem Statement
Given two strings, find the length of the longest common substring (contiguous).

### Approach
- **State**: `dp[i][j]` = length of longest common substring ending at `text1[i-1]` and `text2[j-1]`
- **Recurrence**:
  - If `text1[i-1] == text2[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`
  - Else: `dp[i][j] = 0` (substring must be contiguous)
- **Answer**: Maximum value in entire dp table

### Python Code (Space Optimized)

```python
def longestCommonSubstring(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [0] * (n + 1)
    max_len = 0
    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if text1[i-1] == text2[j-1]:
                dp[j] = prev + 1
                max_len = max(max_len, dp[j])
            else:
                dp[j] = 0
            prev = temp
    return max_len
```

### Complexity
- **Time**: O(m × n)
- **Space**: O(min(m, n))

### Trick/Tip
Unlike LCS, when characters don't match we reset to 0 (not max) because substring requires contiguity. Track max during computation since answer isn't necessarily at dp[m][n].

---

## Problem 22: Subset Sum Problem

### Problem Statement
Given an array of non-negative integers and a target sum, determine if there exists a subset with the given sum.

### Approach
- **State**: `dp[i][sum]` = can we achieve `sum` using first `i` elements
- **Recurrence**:
  - `dp[i][sum] = dp[i-1][sum]` (don't take element i)
  - OR `dp[i][sum] = dp[i-1][sum - nums[i-1]]` (take element i, if `sum >= nums[i-1]`)
- **Base Cases**: `dp[i][0] = True` (empty subset sums to 0), `dp[0][j] = False` for j > 0

### Python Code (Space Optimized)

```python
def subsetSum(nums: list[int], target: int) -> bool:
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for s in range(target, num - 1, -1):
            dp[s] = dp[s] or dp[s - num]
    return dp[target]
```

### Complexity
- **Time**: O(n × target)
- **Space**: O(target)

### Trick/Tip
When optimizing to 1D, iterate backwards to avoid using the same element twice. This is the 0/1 knapsack pattern. If you iterate forward, it becomes unbounded knapsack.

---

## Problem 23: Partition Equal Subset Sum

### Problem Statement
Given a non-negative array, determine if it can be partitioned into two subsets with equal sum.

### Approach
- **Key Insight**: Find subset with sum = `total_sum / 2`. If `total_sum` is odd, return False.
- This reduces to Subset Sum Problem (Problem 22) with target = `total_sum / 2`.

### Python Code

```python
def canPartition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2 != 0:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for s in range(target, num - 1, -1):
            dp[s] = dp[s] or dp[s - num]
    return dp[target]
```

### Complexity
- **Time**: O(n × target)
- **Space**: O(target)

### Trick/Tip
Always check if total sum is odd first — immediate return False. This saves time and is the most common edge case.

---

## Problem 24: Target Sum

### Problem Statement
Given an array `nums` and an integer `target`, assign `+` or `-` to each element to make their sum equal to `target`. Return the number of ways.

### Approach
- **Key Insight**: Let P = sum of elements with +, N = sum of elements with -. Then P - N = target, P + N = sum. So P = (sum + target) / 2.
- Reduces to Count Subsets with Sum = `(sum + target) / 2`
- **State**: `dp[i]` = number of ways to get sum `i`
- **Recurrence**: `dp[i] += dp[i - num]`

### Python Code

```python
def findTargetSumWays(nums: list[int], target: int) -> int:
    total = sum(nums)
    if (total + target) % 2 != 0 or abs(target) > total:
        return 0
    s = (total + target) // 2
    dp = [0] * (s + 1)
    dp[0] = 1
    for num in nums:
        for i in range(s, num - 1, -1):
            dp[i] += dp[i - num]
    return dp[s]
```

### Complexity
- **Time**: O(n × s) where s = (sum + target) / 2
- **Space**: O(s)

### Trick/Tip
The mathematical transformation from +/- assignment to subset sum is the key trick. Always check: can (sum + target) be evenly divided? If not, 0 ways.

---

## Problem 25: Combination Sum IV

### Problem Statement
Given an array of distinct positive integers `nums` and a target integer `target`, return the number of combinations that sum to `target`. Each number can be used unlimited times.

### Approach
- **State**: `dp[i]` = number of combinations that sum to `i`
- **Recurrence**: `dp[i] += dp[i - num]` for each `num` in `nums` where `i - num >= 0`
- **Base Case**: `dp[0] = 1`
- **Loop Order**: Target outer, nums inner (counts permutations, which is what problem asks)

### Python Code

```python
def combinationSum4(nums: list[int], target: int) -> int:
    dp = [0] * (target + 1)
    dp[0] = 1
    for i in range(1, target + 1):
        for num in nums:
            if num <= i:
                dp[i] += dp[i - num]
    return dp[target]
```

### Complexity
- **Time**: O(target × len(nums))
- - **Space**: O(target)

### Trick/Tip
**CRITICAL DISTINCTION from Coin Change II**: Loop order determines permutations vs combinations. Here target is outer → permutations (e.g., [1,2] and [2,1] are different). In Coin Change II, coins is outer → combinations.

---

## Problem 26: Maximum Length of Subarray With Product ≤ K

### Problem Statement
Given an array of positive integers `nums` and an integer `k`, find the length of the longest subarray where the product of all elements is less than or equal to `k`.

### Approach
- **Idea**: Sliding window with product tracking
- Expand window right; when product exceeds k, shrink from left
- This is sliding window, but included here because it relates to DP thinking about subarray constraints

### Python Code

```python
def numSubarrayProductLessThanK(nums: list[int], k: int) -> int:
    if k <= 1:
        return 0
    count = 0
    product = 1
    left = 0
    for right in range(len(nums)):
        product *= nums[right]
        while product >= k:
            product //= nums[left]
            left += 1
        count += right - left + 1
    return count
```

### Complexity
- **Time**: O(n)
- **Space**: O(1)

### Trick/Tip
For each valid right pointer, all subarrays ending at right are valid (since product decreases as we shrink). The count of subarrays ending at right = `right - left + 1`.

---

## Problem 27: Maximal Square

### Problem Statement
Given a binary matrix filled with 0s and 1s, find the largest square containing only 1s and return its area.

### Approach
- **State**: `dp[i][j]` = side length of largest square with bottom-right corner at `(i, j)`
- **Recurrence**: If `matrix[i][j] = 1`:
  `dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1`
- **Base Cases**: First row and first column copy from matrix
- **Answer**: `max(dp)²`

### Python Code (Space Optimized)

```python
def maximalSquare(matrix: list[list[str]]) -> int:
    m, n = len(matrix), len(matrix[0])
    dp = [0] * (n + 1)
    max_side = 0
    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if matrix[i-1][j-1] == '1':
                dp[j] = min(dp[j], dp[j-1], prev) + 1
                max_side = max(max_side, dp[j])
            else:
                dp[j] = 0
            prev = temp
    return max_side * max_side
```

### Complexity
- **Time**: O(m × n)
- **Space**: O(n)

### Trick/Tip
The min of three neighbors (top, left, top-left) ensures all four corners of the square are 1s. This pattern extends to Problem 41 (Maximal Rectangle).

---

## Problem 28: Maximum Product of a Splitted Binary Tree

### Problem Statement
Given a binary tree with `n` nodes, remove one edge to split into two subtrees. The product of their sums should be maximized. Return the result modulo 10^9 + 7.

### Approach
- **Step 1**: Calculate total sum of tree (DFS)
- **Step 2**: For each subtree, calculate its sum and track product `(subtree_sum) * (total - subtree_sum)`
- Use DFS to compute subtree sums

### Python Code

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxProduct(root: TreeNode) -> int:
    MOD = 10**9 + 7
    total = [0]

    def get_total(node):
        if not node:
            return 0
        total_val = node.val + get_total(node.left) + get_total(node.right)
        return total_val

    total[0] = get_total(root)
    result = [0]

    def dfs(node):
        if not node:
            return 0
        subtree_sum = node.val + dfs(node.left) + dfs(node.right)
        result[0] = max(result[0], subtree_sum * (total[0] - subtree_sum))
        return subtree_sum

    dfs(root)
    return result[0] % MOD
```

### Complexity
- **Time**: O(n)
- **Space**: O(h) where h is tree height

### Trick/Tip
Two-pass DFS: first to get total, second to compute subtree sums and maximize product. Modulo operation at the end only.

---

## Problem 29: Stone Game

### Problem Statement
Alex and Lee take turns picking stones from either end of a row. The player with the maximum total stones wins. Both play optimally. Return True if Alex wins.

### Approach
- **State**: `dp[i][j]` = maximum stones Alex can get from stones[i:j+1]
- **Recurrence**: `dp[i][j] = max(stones[i] + min(dp[i+2][j], dp[i+1][j-1]), stones[j] + min(dp[i+1][j-1], dp[i][j-2]))`
  - Alex picks either end, then Lee picks optimally (minimizing Alex's next move)
- **Base Case**: `dp[i][i] = stones[i]`

### Python Code

```python
def stoneGame(piles: list[int]) -> bool:
    # With optimal play, first player always wins with even number of piles
    return True
```

### Python Code (General DP Solution)

```python
def stoneGameDP(piles: list[int]) -> bool:
    n = len(piles)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = piles[i]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(
                piles[i] + min(dp[i+2][j] if i+2 <= j else 0,
                               dp[i+1][j-1] if i+1 <= j-1 else 0),
                piles[j] + min(dp[i+1][j-1] if i+1 <= j-1 else 0,
                               dp[i][j-2] if i <= j-2 else 0)
            )
    return dp[0][n-1] > sum(piles) // 2
```

### Complexity
- **Time**: O(n²)
- **Space**: O(n²)

### Trick/Tip
Fun fact: Alex always wins this game with even piles (mathematical proof exists). The DP solution is important for the general case and for understanding minimax DP patterns.

---

## Problem 30: Longest Palindromic Subsequence

### Problem Statement
Given a string `s`, find the length of the longest palindromic subsequence.

### Approach
- **Key Insight**: LPS(s) = LCS(s, reverse(s))
- **Alternative DP**: `dp[i][j]` = LPS length in `s[i:j+1]`
- **Recurrence**:
  - If `s[i] == s[j]`: `dp[i][j] = dp[i+1][j-1] + 2`
  - Else: `dp[i][j] = max(dp[i+1][j], dp[i][j-1])`

### Python Code (LCS Approach)

```python
def longestPalindromeSubseq(s: str) -> int:
    t = s[::-1]
    m = len(s)
    dp = [0] * (m + 1)
    for i in range(1, m + 1):
        prev = 0
        for j in range(1, m + 1):
            temp = dp[j]
            if s[i-1] == t[j-1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            prev = temp
    return dp[m]
```

### Python Code (Direct DP)

```python
def longestPalindromeSubseq_direct(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i+1][j-1] + 2
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j-1])
    return dp[0][n-1]
```

### Complexity
- **Time**: O(n²)
- **Space**: O(n)

### Trick/Tip
LPS = LCS with reverse is the elegant one-liner approach. The direct DP is also important to know for interval DP problems.

---

## Problem 31: Palindrome Partitioning - Min Cuts

### Problem Statement
Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return the minimum number of cuts needed.

### Approach
- **State**: `dp[i]` = minimum cuts for `s[0:i]`
- **Recurrence**: `dp[i] = min(dp[j] + 1)` for all `j < i` where `s[j:i]` is palindrome
- **Base Case**: `dp[0] = -1` (no cuts for empty string)
- **Pre-computation**: Palindrome table `is_pal[i][j]` for O(1) lookup

### Python Code

```python
def minCut(s: str) -> int:
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                is_pal[i][j] = length == 2 or is_pal[i+1][j-1]

    dp = [0] * n
    for i in range(n):
        if is_pal[0][i]:
            dp[i] = 0
        else:
            dp[i] = i
            for j in range(1, i + 1):
                if is_pal[j][i]:
                    dp[i] = min(dp[i], dp[j-1] + 1)
    return dp[n-1]
```

### Complexity
- **Time**: O(n²)
- **Space**: O(n²)

### Trick/Tip
Pre-compute palindrome table first. Then the DP is a straightforward minimum cuts calculation. The base case `dp[0] = -1` is important to avoid off-by-one errors.

---

## Problem 32: Interleaving String

### Problem Statement
Given strings `s1`, `s2`, and `s3`, determine if `s3` is formed by interleaving `s1` and `s2`. An interleaving uses all characters from both strings in their original order.

### Approach
- **State**: `dp[i][j]` = is `s3[0:i+j]` an interleaving of `s1[0:i]` and `s2[0:j]`
- **Recurrence**:
  - `dp[i][j] = dp[i-1][j] AND s1[i-1] == s3[i+j-1]` (take from s1)
  - OR `dp[i][j] = dp[i][j-1] AND s2[j-1] == s3[i+j-1]` (take from s2)
- **Base Case**: `dp[0][0] = True`

### Python Code (Space Optimized)

```python
def isInterleave(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False
    dp = [False] * (n + 1)
    dp[0] = True
    for j in range(1, n + 1):
        dp[j] = dp[j-1] and s2[j-1] == s3[j-1]
    for i in range(1, m + 1):
        dp[0] = dp[0] and s1[i-1] == s3[i-1]
        for j in range(1, n + 1):
            dp[j] = (dp[j] and s1[i-1] == s3[i+j-1]) or \
                     (dp[j-1] and s2[j-1] == s3[i+j-1])
    return dp[n]
```

### Complexity
- **Time**: O(m × n)
- **Space**: O(n)

### Trick/Tip
Check length first: if `len(s1) + len(s2) != len(s3)`, immediately False. The 2D DP tracks whether we can form s3 prefix using some combination of s1 and s2 prefixes.

---

## Problem 33: Unique Binary Search Trees

### Problem Statement
Given `n`, return the number of structurally unique BSTs that store values 1..n.

### Approach
- **State**: `dp[i]` = number of unique BSTs with `i` nodes
- **Recurrence**: `dp[i] = sum(dp[j-1] * dp[i-j])` for `j = 1..i` (j is root)
  - Left subtree has `j-1` nodes, right subtree has `i-j` nodes
- **Base Case**: `dp[0] = 1` (empty tree), `dp[1] = 1`

### Python Code

```python
def numTrees(n: int) -> int:
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for nodes in range(2, n + 1):
        for root in range(1, nodes + 1):
            dp[nodes] += dp[root - 1] * dp[nodes - root]
    return dp[n]
```

### Complexity
- **Time**: O(n²)
- **Space**: O(n)

### Trick/Tip
This is the Catalan number: `C(n) = C(2n,n) / (n+1)`. The DP is the standard way to compute it. The insight: each root splits remaining nodes into left/right subtrees, and BST count is multiplicative.

---

## Problem 34: Dungeon Game

### Problem Statement
The knight starts at `dungeon[0][0]` and must reach `dungeon[m-1][n-1]`. Each cell has an integer (positive = health gained, negative = damage). The knight must always have at least 1 HP. Find the minimum initial HP to reach the princess.

### Approach
- **State**: `dp[i][j]` = minimum HP needed to enter cell `(i, j)` and reach the end
- **Recurrence**: `dp[i][j] = min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j]`
  - If result <= 0, set to 1 (must have at least 1 HP)
- **Direction**: Bottom-right to top-left
- **Base Case**: `dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])`

### Python Code

```python
def calculateMinimumHP(dungeon: list[list[int]]) -> int:
    m, n = len(dungeon), len(dungeon[0])
    dp = [[0] * n for _ in range(m)]
    dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])
    for i in range(m - 2, -1, -1):
        dp[i][n-1] = max(1, dp[i+1][n-1] - dungeon[i][n-1])
    for j in range(n - 2, -1, -1):
        dp[m-1][j] = max(1, dp[m-1][j+1] - dungeon[m-1][j])
    for i in range(m - 2, -1, -1):
        for j in range(n - 2, -1, -1):
            min_needed = min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j]
            dp[i][j] = max(1, min_needed)
    return dp[0][0]
```

### Complexity
- **Time**: O(m × n)
- **Space**: O(m × n)

### Trick/Tip
This problem MUST be solved bottom-up (reverse DP). If you go top-down, you don't know future requirements. The key insight: you need to know what happens ahead to decide current HP.

---

## Problem 35: Ones and Zeroes

### Problem Statement
Given an array of binary strings `strs` and two integers `m` and `n`, find the size of the largest subset of `strs` such that there are at most `m` 0s and `n` 1s in the subset.

### Approach
- **State**: `dp[i][j]` = max strings using at most `i` zeros and `j` ones
- **Recurrence**: For each string with `zeros, ones` count:
  - `dp[i][j] = max(dp[i][j], dp[i-zeros][j-ones] + 1)` (0/1 knapsack)
- **Base Case**: `dp[0][0] = 0`

### Python Code

```python
def findMaxForm(strs: list[str], m: int, n: int) -> int:
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        zeros = s.count('0')
        ones = s.count('1')
        for i in range(m, zeros - 1, -1):
            for j in range(n, ones - 1, -1):
                dp[i][j] = max(dp[i][j], dp[i-zeros][j-ones] + 1)
    return dp[m][n]
```

### Complexity
- **Time**: O(k × m × n) where k = number of strings
- **Space**: O(m × n)

### Trick/Tip
This is 2D 0/1 knapsack. Two constraints (m zeros, n ones) make it 2D. Iterate backwards in both dimensions to avoid using same string twice.

---

# Hard Problems

---

## Problem 36: Edit Distance

### Problem Statement
Given two strings `word1` and `word2`, return the minimum number of operations (insert, delete, replace) to convert `word1` to `word2`.

### Approach
- **State**: `dp[i][j]` = min operations to convert `word1[0:i]` to `word2[0:j]`
- **Recurrence**:
  - If `word1[i-1] == word2[j-1]`: `dp[i][j] = dp[i-1][j-1]`
  - Else: `dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`
    - `dp[i-1][j]` = delete from word1
    - `dp[i][j-1]` = insert into word1
    - `dp[i-1][j-1]` = replace in word1
- **Base Cases**: `dp[i][0] = i` (delete all), `dp[0][j] = j` (insert all)

### Python Code (Space Optimized)

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    if m < n:
        word1, word2, m, n = word2, word1, n, m
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if word1[i-1] == word2[j-1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j-1])
            prev = temp
    return dp[n]
```

### Complexity
- **Time**: O(m × n)
- **Space**: O(min(m, n))

### Trick/Tip
Edit Distance is the king of string DP. The three operations map to three directions in the DP table: diagonal (replace), up (delete), left (insert).

---

## Problem 37: Burst Balloons

### Problem Statement
Given `n` balloons indexed 0 to n-1, each with a number `nums[i]`. Burst balloon `i` to gain `nums[i-1] * nums[i] * nums[i+1]` coins. Burst all balloons to maximize coins. (Treat 0 for out-of-bounds indices)

### Approach
- **State**: `dp[i][j]` = max coins from bursting balloons in range `[i, j]`
- **Recurrence**: For each `k` in `[i, j]` (last balloon to burst in this range):
  `dp[i][j] = max(dp[i][j], dp[i][k-1] + dp[k+1][j] + nums[i-1] * nums[k] * nums[j+1])`
- **Base Cases**: `dp[i][i] = nums[i-1] * nums[i] * nums[i+1]` (with 0 padding)
- **Direction**: Increasing range length

### Python Code

```python
def maxCoins(nums: list[int]) -> int:
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for length in range(1, n - 1):
        for i in range(1, n - length):
            j = i + length - 1
            for k in range(i, j + 1):
                dp[i][j] = max(dp[i][j],
                    dp[i][k-1] + dp[k+1][j] + nums[i-1] * nums[k] * nums[j+1])
    return dp[1][n-2]
```

### Complexity
- **Time**: O(n³)
- **Space**: O(n²)

### Trick/Tip
The key insight: think about which balloon is burst LAST in a range, not first. Adding 1s at boundaries handles edge cases cleanly. This is interval DP.

---

## Problem 38: Regular Expression Matching

### Problem Statement
Implement regular expression matching with support for `.` (any single character) and `*` (zero or more of the preceding element). The matching covers the entire input string.

### Approach
- **State**: `dp[i][j]` = does `s[0:i]` match `p[0:j]`
- **Recurrence**:
  - If `p[j-1] != '*'`: `dp[i][j] = dp[i-1][j-1] AND (s[i-1] == p[j-1] OR p[j-1] == '.')`
  - If `p[j-1] == '*'`:
    - Zero occurrences: `dp[i][j] = dp[i][j-2]`
    - One or more: `dp[i][j] = dp[i-1][j] AND (s[i-1] == p[j-2] OR p[j-2] == '.')`
- **Base Case**: `dp[0][0] = True`, `dp[0][j]` handles `a*b*c*` patterns

### Python Code

```python
def isMatch(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(2, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                dp[i][j] = dp[i][j-2]
                if p[j-2] == '.' or p[j-2] == s[i-1]:
                    dp[i][j] = dp[i][j] or dp[i-1][j]
            else:
                if p[j-1] == '.' or p[j-1] == s[i-1]:
                    dp[i][j] = dp[i-1][j-1]
    return dp[m][n]
```

### Complexity
- **Time**: O(m × n)
- **Space**: O(m × n)

### Trick/Tip
When you see `*`, always consider two cases: zero occurrences (look two chars back in pattern) or one+ occurrences (look at current position in pattern with previous char in string). Handle empty string patterns carefully.

---

## Problem 39: Wildcard Pattern Matching

### Problem Statement
Given a string `s` and a pattern `p` with `?` (any single character) and `*` (any sequence of characters including empty), implement pattern matching.

### Approach
- **State**: `dp[i][j]` = does `s[0:i]` match `p[0:j]`
- **Recurrence**:
  - If `p[j-1] == '*'`: `dp[i][j] = dp[i][j-1] OR dp[i-1][j]`
    - `dp[i][j-1]`: `*` matches empty
    - `dp[i-1][j]`: `*` extends to include `s[i-1]`
  - If `p[j-1] == '?' OR p[j-1] == s[i-1]`: `dp[i][j] = dp[i-1][j-1]`
- **Base Case**: `dp[0][0] = True`, handle `*` in pattern for empty string

### Python Code

```python
def isMatch(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(1, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-1]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                dp[i][j] = dp[i][j-1] or dp[i-1][j]
            elif p[j-1] == '?' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]
    return dp[m][n]
```

### Complexity
- **Time**: O(m × n)
- **Space**: O(m × n)

### Trick/Tip
Wildcard `*` is easier than regex `*` because it can match any sequence, not just repetitions of one character. The recurrence for `*` has a self-reference `dp[i][j] = dp[i-1][j]` which handles multiple character matching.

---

## Problem 40: Shortest Common Supersequence

### Problem Statement
Given two strings `str1` and `str2`, return the shortest string that has both as subsequences. If there are multiple, return any.

### Approach
- **Key Insight**: SCS length = `len(str1) + len(str2) - LCS(str1, str2)`
- **Reconstruction**: Build LCS table, then merge strings by following the path
- **Step 1**: Compute LCS DP table
- **Step 2**: Walk backwards through table to build result

### Python Code

```python
def shortestCommonSupersequence(str1: str, str2: str) -> str:
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if str1[i-1] == str2[j-1]:
            result.append(str1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            result.append(str1[i-1])
            i -= 1
        else:
            result.append(str2[j-1])
            j -= 1
    while i > 0:
        result.append(str1[i-1])
        i -= 1
    while j > 0:
        result.append(str2[j-1])
        j -= 1
    return ''.join(reversed(result))
```

### Complexity
- **Time**: O(m × n)
- **Space**: O(m × n)

### Trick/Tip
SCS = LCS + remaining characters. The reconstruction is similar to LCS but you add non-matching characters to the result. Always append and reverse at the end.

---

## Problem 41: Maximal Rectangle

### Problem Statement
Given a `m x n` binary matrix filled with 0s and 1s, find the largest rectangle containing only 1s and return its area.

### Approach
- **Key Insight**: For each row, compute "height" of consecutive 1s above (including current row). Then apply Largest Rectangle in Histogram for each row.
- **Step 1**: Build heights array row by row
- **Step 2**: For each row, use stack-based histogram algorithm

### Python Code

```python
def maximalRectangle(matrix: list[list[str]]) -> int:
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    heights = [0] * n
    max_area = 0

    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '1':
                heights[j] += 1
            else:
                heights[j] = 0

        stack = [-1]
        for j in range(n + 1):
            h = heights[j] if j < n else 0
            while stack[-1] != -1 and heights[stack[-1]] > h:
                height = heights[stack.pop()]
                width = j - stack[-1] - 1
                max_area = max(max_area, height * width)
            stack.append(j)

    return max_area
```

### Complexity
- **Time**: O(m × n)
- **Space**: O(n)

### Trick/Tip
This combines two problems: building height histogram + largest rectangle in histogram. The stack-based histogram algorithm runs in O(n) and is essential to know.

---

## Problem 42: Egg Dropping

### Problem Statement
You have `k` eggs and a building with `n` floors. Find the minimum number of trials needed to determine the critical floor (the floor from which an egg breaks when dropped).

### Approach
- **State**: `dp[k][n]` = min trials with `k` eggs and `n` floors
- **Recurrence**: For each floor `x` (1 to n):
  - Egg breaks: `dp[k-1][x-1]`
  - Egg doesn't break: `dp[k][n-x]`
  - `dp[k][n] = 1 + min over all x of max(dp[k-1][x-1], dp[k][n-x])`
- **Base Cases**: `dp[1][n] = n`, `dp[k][0] = 0`, `dp[0][n] = infinity`

### Python Code

```python
def superEggDrop(k: int, n: int) -> int:
    dp = [[0] * (n + 1) for _ in range(k + 1)]
    for j in range(1, n + 1):
        dp[1][j] = j
    for i in range(2, k + 1):
        for j in range(1, n + 1):
            dp[i][j] = j
            lo, hi = 1, j
            while lo <= hi:
                mid = (lo + hi) // 2
                breaks = dp[i-1][mid-1]
                survives = dp[i][j-mid]
                if breaks < survives:
                    lo = mid + 1
                elif breaks > survives:
                    hi = mid - 1
                else:
                    lo = hi = mid
            x = lo
            dp[i][j] = 1 + max(dp[i-1][x-1], dp[i][j-x])
    return dp[k][n]
```

### Complexity
- **Time**: O(k × n × log n) with binary search optimization
- **Space**: O(k × n)

### Trick/Tip
The key optimization: binary search for the optimal floor `x` where `dp[k-1][x-1] ≈ dp[k][n-x]`. Without binary search, it's O(k × n²). There's also an O(k × log n) solution using different state definition.

---

## Problem 43: Paint House II

### Problem Statement
There are `n` houses and `k` colors. `cost[i][j]` = cost to paint house `i` with color `j`. No two adjacent houses can have the same color. Find minimum cost.

### Approach
- **State**: `dp[i][j]` = min cost to paint first `i` houses where house `i` is color `j`
- **Recurrence**: `dp[i][j] = cost[i][j] + min(dp[i-1][*])` excluding `j`
- **Optimization**: Track min and second min of previous row to avoid O(k) per cell

### Python Code (Optimized O(n×k))

```python
def minCostII(costs: list[list[int]]) -> int:
    if not costs:
        return 0
    n, k = len(costs), len(costs[0])
    if k == 1:
        return costs[0][0] if n == 1 else float('inf')

    prev_min = prev_second_min = 0
    prev_min_color = -1

    for i in range(n):
        curr_min = curr_second_min = float('inf')
        curr_min_color = -1
        for j in range(k):
            if j == prev_min_color:
                cost = costs[i][j] + prev_second_min
            else:
                cost = costs[i][j] + prev_min
            if cost < curr_min:
                curr_second_min = curr_min
                curr_min = cost
                curr_min_color = j
            elif cost < curr_second_min:
                curr_second_min = cost
        prev_min, prev_second_min, prev_min_color = curr_min, curr_second_min, curr_min_color

    return prev_min
```

### Complexity
- **Time**: O(n × k)
- **Space**: O(1) extra

### Trick/Tip
The min/second-min optimization reduces O(n × k²) to O(n × k). If the current color matches the previous min color, use second min; otherwise use min. This is a crucial optimization pattern.

---

## Problem 44: Minimum Cost to Cut Stick

### Problem Statement
Given a stick of length `n` and array of cuts, find the minimum total cost to cut the stick at all specified positions. Cost of a cut = length of the stick being cut.

### Approach
- **State**: `dp[i][j]` = min cost to cut stick between cuts `i` and `j`
- **Recurrence**: For each possible cut `k` between `i` and `j`:
  `dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cuts[j] - cuts[i])`
- **Setup**: Add 0 and n to cuts array, sort it
- **Base Case**: `dp[i][i+1] = 0` (no cuts between adjacent cuts)

### Python Code

```python
def minCost(n: int, cuts: list[int]) -> int:
    cuts = sorted([0] + cuts + [n])
    m = len(cuts)
    dp = [[0] * m for _ in range(m)]
    for length in range(2, m):
        for i in range(m - length):
            j = i + length
            dp[i][j] = float('inf')
            for k in range(i + 1, j):
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cuts[j] - cuts[i])
    return dp[0][m-1]
```

### Complexity
- **Time**: O(m³) where m = number of cuts + 2
- **Space**: O(m²)

### Trick/Tip
This is interval DP. Adding 0 and n to cuts and sorting gives natural boundaries. The outer loop must iterate over increasing interval lengths.

---

## Problem 45: Number of Digit One

### Problem Statement
Given an integer `n`, count the total number of digit 1 appearing in all non-negative integers less than or equal to `n`.

### Approach
- **State**: Analyze each digit position separately
- For each position (ones, tens, hundreds, etc.), calculate how many times 1 appears
- At position `d` with digit `curr`:
  - If `curr == 0`: count += higher × factor
  - If `curr == 1`: count += higher × factor + lower + 1
  - If `curr > 1`: count += (higher + 1) × factor

### Python Code

```python
def countDigitOne(n: int) -> int:
    count = 0
    factor = 1
    while factor <= n:
        lower = n % factor
        curr = (n // factor) % 10
        higher = n // (factor * 10)
        if curr == 0:
            count += higher * factor
        elif curr == 1:
            count += higher * factor + lower + 1
        else:
            count += (higher + 1) * factor
        factor *= 10
    return count
```

### Complexity
- **Time**: O(log n)
- **Space**: O(1)

### Trick/Tip
This is digit DP without the actual DP table. Analyze each digit position independently. The three cases (0, 1, >1) handle the boundary conditions.

---

## Problem 46: Strange Printer

### Problem Statement
The printer can only print a sequence of the same character in each turn. Each turn, it can print new characters over existing ones. Given a string `s`, return the minimum number of turns to print `s`.

### Approach
- **State**: `dp[i][j]` = min turns to print `s[i:j+1]`
- **Recurrence**:
  - `dp[i][j] = dp[i+1][j] + 1` (print `s[i]` separately first)
  - For each `k` in `[i+1, j]` where `s[i] == s[k]`:
    `dp[i][j] = min(dp[i][j], dp[i+1][k-1] + dp[k][j])`
    (combine printing of `s[i]` and `s[k]` in one turn)
- **Base Case**: `dp[i][i] = 1`

### Python Code

```python
def strangePrinter(s: str) -> int:
    if not s:
        return 0
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = dp[i+1][j] + 1
            for k in range(i + 1, j + 1):
                if s[k] == s[i]:
                    dp[i][j] = min(dp[i][j], dp[i+1][k-1] + dp[k][j])
    return dp[0][n-1]
```

### Complexity
- **Time**: O(n³)
- **Space**: O(n²)

### Trick/Tip
The key insight: if `s[i] == s[k]`, we can print both in one turn by printing `s[i]` over the entire range first, then filling in middle. Handle `k == i+1` carefully (empty subproblem).

---

## Problem 47: Stone Game III

### Problem Statement
Alice and Bob take turns picking stones from a row. Each player can pick 1, 2, or 3 stones. The player with the maximum score wins. Return "Alice", "Bob", or "Tie".

### Approach
- **State**: `dp[i]` = max score difference (current player - opponent) from stones `i` onward
- **Recurrence**: `dp[i] = max(stones[i] - dp[i+1], stones[i] + stones[i+1] - dp[i+2], stones[i] + stones[i+1] + stones[i+2] - dp[i+3])`
- **Base Cases**: `dp[n] = 0`, compute from right to left
- **Answer**: If `dp[0] > 0` → Alice, `< 0` → Bob, `== 0` → Tie

### Python Code

```python
def stoneGameIII(stoneValue: list[int]) -> str:
    n = len(stoneValue)
    dp = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        dp[i] = stoneValue[i] - dp[i + 1]
        if i + 1 < n:
            dp[i] = max(dp[i], stoneValue[i] + stoneValue[i+1] - dp[i + 2])
        if i + 2 < n:
            dp[i] = max(dp[i], stoneValue[i] + stoneValue[i+1] + stoneValue[i+2] - dp[i + 3])
    if dp[0] > 0:
        return "Alice"
    elif dp[0] < 0:
        return "Bob"
    return "Tie"
```

### Complexity
- **Time**: O(n)
- **Space**: O(n) (can be O(1) with rolling window)

### Trick/Tip
Score difference DP: instead of tracking both scores, track the difference. If current player takes stones `s`, opponent gets `dp[i+k]`, so current player net = `s - dp[i+k]`.

---

## Problem 48: Predict the Winner

### Problem Statement
Two players take turns picking from either end of an array. Player 1 goes first. Return True if Player 1 can win (score >= Player 2).

### Approach
- **State**: `dp[i][j]` = max score difference (current player - opponent) for `nums[i:j+1]`
- **Recurrence**: `dp[i][j] = max(nums[i] - dp[i+1][j], nums[j] - dp[i][j-1])`
- **Base Case**: `dp[i][i] = nums[i]`
- **Answer**: `dp[0][n-1] >= 0`

### Python Code

```python
def PredictTheWinner(nums: list[int]) -> bool:
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = nums[i]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(nums[i] - dp[i+1][j], nums[j] - dp[i][j-1])
    return dp[0][n-1] >= 0
```

### Complexity
- **Time**: O(n²)
- **Space**: O(n²)

### Trick/Tip
Same score difference pattern as Stone Game III. The insight: if I take `nums[i]`, my opponent will play optimally to maximize THEIR score difference from `nums[i+1:j+1]`, so my net advantage is `nums[i] - opponent's advantage`.

---

## Problem 49: Minimum Cost Tree From Leaf Values

### Problem Statement
Given an array `arr`, build a binary tree where each leaf node has value `arr[i]` (in order), and each non-leaf node has value = product of largest leaf values in its left and right subtrees. Return minimum total cost.

### Approach
- **State**: `dp[i][j]` = min cost of tree built from `arr[i:j+1]`
- **Recurrence**: For each root `k` in `[i, j]`:
  `dp[i][j] = min(dp[i][k] + dp[k+1][j] + max(arr[i:k+1]) * max(arr[k+1:j+1]))`
- **Base Case**: `dp[i][i] = 0` (single leaf, no cost)

### Python Code (Stack-based O(n))

```python
def mctFromLeafValues(arr: list[int]) -> int:
    result = 0
    stack = [float('inf')]
    for a in arr:
        while stack[-1] <= a:
            mid = stack.pop()
            result += mid * min(stack[-1], a)
        stack.append(a)
    while len(stack) > 2:
        result += stack.pop() * stack[-1]
    return result
```

### Python Code (DP O(n³))

```python
def mctFromLeafValuesDP(arr: list[int]) -> int:
    n = len(arr)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                root_val = max(arr[i:k+1]) * max(arr[k+1:j+1])
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j] + root_val)
    return dp[0][n-1]
```

### Complexity
- **Time**: O(n) for stack, O(n³) for DP
- **Space**: O(n)

### Trick/Tip
The stack solution is elegant: for each element, pair it with the smaller of its neighbors. This greedy works because removing the smallest interior node minimizes the product cost.

---

## Problem 50: Longest String Chain

### Problem Statement
Given a list of words, a word chain is a sequence where each word differs from the previous by exactly one character (insert/delete). Find the longest word chain.

### Approach
- **State**: `dp[word]` = longest chain ending at this word
- **Recurrence**: `dp[word] = max(dp[prev] + 1)` for all `prev` that is one character less and differs by one insertion
- **Process**: Sort words by length, check all possible predecessors

### Python Code

```python
def longestStrChain(words: list[str]) -> int:
    word_set = set(words)
    dp = {}
    result = 0
    for word in sorted(words, key=len):
        dp[word] = 1
        for i in range(len(word)):
            prev = word[:i] + word[i+1:]
            if prev in dp:
                dp[word] = max(dp[word], dp[prev] + 1)
        result = max(result, dp[word])
    return result
```

### Complexity
- **Time**: O(n × L) where n = number of words, L = max word length
- **Space**: O(n)

### Trick/Tip
Process words in order of length. For each word, try removing one character at a time to find predecessors. Using a dict for dp allows O(1) lookup by word.

---

## Problem 51: Number of Ways to Rearrange Sticks

### Problem Statement
Given `n` sticks of lengths 1 to n, count the number of ways to arrange them such that exactly `k` sticks are visible from the left. A stick is visible if it's longer than all sticks to its left. Return modulo 10^9+7.

### Approach
- **State**: `dp[i][j]` = number of ways to arrange `i` sticks with `j` visible
- **Recurrence**: Place the longest stick (length `i`):
  - If placed at the leftmost: `dp[i-1][j-1]` (one more visible)
  - If placed somewhere else (not leftmost): `(i-1) * dp[i-1][j]` (doesn't add visible, but can go in any of `i-1` non-first positions)
- **Base Case**: `dp[0][0] = 1`

### Python Code

```python
def rearrangeSticks(n: int, k: int) -> int:
    MOD = 10**9 + 7
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            dp[i][j] = (dp[i-1][j-1] + (i - 1) * dp[i-1][j]) % MOD
    return dp[n][k]
```

### Complexity
- **Time**: O(n × k)
- **Space**: O(n × k)

### Trick/Tip
Adding elements one by one and tracking visible count. The key insight: the longest stick determines visibility — if it's first, it's visible; otherwise, it doesn't affect the visible count of shorter sticks.

---

## Problem 52: Count All Valid Pickup and Delivery Options

### Problem Statement
Given `n` orders, each order has a pickup and delivery. Count all valid sequences where every pickup comes before its delivery. Return modulo 10^9+7.

### Approach
- **State**: `dp[i]` = number of valid sequences for `i` orders
- **Recurrence**: When adding order `i`, there are `2*i - 1` positions to place the pickup, and `2*i - 1 - (pickup_position)` positions for delivery (after pickup).
  - Total ways to add one order = `(2*i - 1) * (2*i - 2) / 2 = (2*i - 1) * (i - 1)`
- **Base Case**: `dp[0] = 1`
- **Recurrence**: `dp[i] = dp[i-1] * (2*i - 1) * (i - 1)`

### Python Code

```python
def countOrders(n: int) -> int:
    MOD = 10**9 + 7
    dp = 1
    for i in range(2, n + 1):
        dp = dp * (2 * i - 1) * (i - 1) % MOD
    return dp
```

### Complexity
- **Time**: O(n)
- - **Space**: O(1)

### Trick/Tip
The combinatorial insight: when adding the i-th order (2 new positions), there are `2i-1` choices for pickup, and once pickup is placed, exactly `(2i-1) - (pickup_index)` valid positions for delivery. The sum simplifies to the formula.

---

## Problem 53: Profitable Schemes

### Problem Statement
Given `n` members, `minProfit` profit goal, and group/profit arrays where `group[i]` is members needed and `profit[i]` is profit for crime `i`, count the number of schemes where profit >= minProfit. Return modulo 10^9+7.

### Approach
- **State**: `dp[i][j][p]` = ways considering first `i` crimes with `j` members and profit `p`
- **Recurrence**:
  - Skip crime: `dp[i][j][p] += dp[i-1][j][p]`
  - Take crime (if j >= group[i]): `dp[i][j][p] += dp[i-1][j-group[i]][min(minProfit, p-profit[i])]`
- **Optimization**: Cap profit at minProfit (any profit >= minProfit is equivalent)
- **Space optimization**: 2D array, iterate crimes outer

### Python Code

```python
def profitableSchemes(n: int, minProfit: int, group: list[int], profit: list[int]) -> int:
    MOD = 10**9 + 7
    m = len(group)
    dp = [[0] * (minProfit + 1) for _ in range(n + 1)]
    dp[0][0] = 1

    for i in range(m):
        new_dp = [row[:] for row in dp]
        for j in range(n + 1):
            for p in range(minProfit + 1):
                if dp[j][p] == 0:
                    continue
                nj = j + group[i]
                if nj <= n:
                    np = min(minProfit, p + profit[i])
                    new_dp[nj][np] = (new_dp[nj][np] + dp[j][p]) % MOD
        dp = new_dp

    result = 0
    for j in range(n + 1):
        result = (result + dp[j][minProfit]) % MOD
    return result
```

### Complexity
- **Time**: O(m × n × minProfit)
- **Space**: O(n × minProfit)

### Trick/Tip
Cap profit at minProfit — any profit above minProfit is treated the same. This optimization keeps the DP table bounded. Use a new_dp to avoid counting same crime twice.

---

## Problem 54: Sum of Subarray Minimums

### Problem Statement
Given an array `arr`, find the sum of minimum values of all subarrays. Return modulo 10^9+7.

### Approach
- **Key Insight**: For each element `arr[i]`, find how many subarrays have `arr[i]` as the minimum
- **Monotonic Stack**: Find `left[i]` (distance to previous smaller) and `right[i]` (distance to next smaller or equal)
- Contribution of `arr[i]` = `arr[i] * left[i] * right[i]`

### Python Code

```python
def sumSubarrayMins(arr: list[int]) -> int:
    MOD = 10**9 + 7
    n = len(arr)
    stack = []
    left = [0] * n
    right = [0] * n

    for i in range(n):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)

    stack.clear()
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)

    result = 0
    for i in range(n):
        result = (result + arr[i] * left[i] * right[i]) % MOD
    return result
```

### Complexity
- **Time**: O(n)
- **Space**: O(n)

### Trick/Tip
Use strict inequality on one side and non-strict on the other to avoid double-counting equal elements. `left` uses `>` (strict), `right` uses `>=` (non-strict).

---

## Problem 55: Filling Bookcase Shelves

### Problem Statement
Given an array `books` where `books[i] = [thickness, height]` and an integer `shelfWidth`, place books on shelves. Each shelf has width `shelfWidth`. The total height is the max height of books on each shelf. Minimize total height.

### Approach
- **State**: `dp[i]` = minimum height to place first `i` books
- **Recurrence**: For each book `i`, try placing books `j..i` on the last shelf:
  - If total thickness of `j..i` <= shelfWidth:
  `dp[i] = min(dp[i], dp[j-1] + max(height of books j..i))`
- **Base Case**: `dp[0] = 0`

### Python Code

```python
def minHeightShelves(books: list[list[int]], shelfWidth: int) -> int:
    n = len(books)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    for i in range(1, n + 1):
        width = 0
        height = 0
        for j in range(i, 0, -1):
            width += books[j-1][0]
            if width > shelfWidth:
                break
            height = max(height, books[j-1][1])
            dp[i] = min(dp[i], dp[j-1] + height)
    return dp[n]
```

### Complexity
- **Time**: O(n²)
- **Space**: O(n)

### Trick/Tip
Iterate backwards from current book to find valid shelf configurations. As we add more books to the shelf, track max height and check width constraint. Break early when width exceeded.

---

# Summary of DP Patterns

| Pattern | Problems |
|---------|----------|
| **1D Linear** | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 |
| **2D Grid** | 17, 18, 19, 27, 41 |
| **Subsequence** | 12, 13, 20, 21, 30, 50 |
| **Knapsack** | 22, 23, 24, 25, 35 |
| **Coin Change** | 14, 15 |
| **String Matching** | 16, 32, 38, 39 |
| **Interval DP** | 29, 31, 37, 44, 46, 49 |
| **Stock Problems** | 8, 9 |
| **State Machine** | 9, 43 |
| **Digit DP** | 45 |
| **Tree DP** | 28, 33, 55 |
| **Combinatorial** | 51, 52 |
| **Stack + DP** | 41, 42, 54 |
| **Monotonic Stack** | 54 |

---

# Quick Reference: Problem Difficulty Distribution

```
Easy (10):    Problems 1-10    - Basic patterns, must solve in <5 min each
Medium (25): Problems 11-35   - Standard patterns, 5-10 min each
Hard (20):   Problems 36-55   - Complex patterns, 10-20 min each

Total: 55 problems
Estimated total time: 8-12 hours for complete mastery
```

---

# Last-Minute Tips for Infosys SP DSE

1. **DP is about state definition** — Clearly define what dp[i] or dp[i][j] represents
2. **Write base cases first** — Always handle edge cases before recurrence
3. **Tabulation > Memoization** — Bottom-up is more cache-friendly and avoids recursion limits
4. **Space optimization** — Most 2D DP can be optimized to 1D if you only need previous row
5. **Pattern recognition** — The hardest part is recognizing which pattern applies
6. **Practice order** — Easy → Medium → Hard within each pattern
7. **Time yourself** — Easy: 5min, Medium: 10min, Hard: 15min
8. **Edge cases** — Empty arrays, single elements, all same elements

---

# Comprehensive Pattern Recognition Guide

> This section helps you identify which DP pattern to use based on problem keywords and constraints.

## How to Identify the Pattern

| Keywords in Problem | Pattern | Examples |
|---------------------|---------|----------|
| "ways to reach", "climbing", "steps" | 1D Linear DP | Problems 1, 2, 4 |
| "minimum/maximum cost" with linear structure | 1D Linear DP | Problems 2, 3 |
| "grid", "matrix", "paths" | 2D Grid DP | Problems 17, 18, 19 |
| "subsequence", "not necessarily contiguous" | Subsequence DP | Problems 12, 13, 20 |
| "substring", "contiguous" | Substring DP | Problems 21, 30 |
| "coins", "make amount" | Unbounded Knapsack | Problems 14, 15 |
| "subset", "partition", "target sum" | 0/1 Knapsack | Problems 22, 23, 24 |
| "two strings", "matching" | String DP | Problems 20, 21, 32 |
| "pattern", "regex", "wildcard" | Pattern Matching DP | Problems 38, 39 |
| "range", "interval", "between i and j" | Interval DP | Problems 29, 31, 37, 44, 46 |
| "buy/sell stock" | State Machine DP | Problems 8, 9 |
| "k colors", "adjacent different" | State Machine DP | Problems 10, 43 |
| "digit", "count occurrences" | Digit DP | Problem 45 |
| "tree", "subtree" | Tree DP | Problems 28, 33 |
| "player", "game", "win" | Game Theory DP | Problems 29, 47, 48 |
| "egg", "drop", "critical floor" | Binary Search + DP | Problem 42 |

## State Definition Templates

### 1D Linear DP
```python
# State: dp[i] = answer for prefix s[0:i]
dp = [0] * (n + 1)
dp[0] = base_case
for i in range(1, n + 1):
    dp[i] = function(dp[i-1], dp[i-2], ...)
```

### 2D Grid DP
```python
# State: dp[i][j] = answer for cell (i, j)
dp = [[0] * n for _ in range(m)]
dp[0][0] = base_case
for i in range(m):
    for j in range(n):
        dp[i][j] = function(dp[i-1][j], dp[i][j-1], ...)
```

### Interval DP
```python
# State: dp[i][j] = answer for range [i, j]
dp = [[0] * n for _ in range(n)]
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        for k in range(i, j):
            dp[i][j] = function(dp[i][k], dp[k+1][j], ...)
```

### Knapsack DP
```python
# 0/1 Knapsack (each item used once)
dp = [0] * (capacity + 1)
for item in items:
    for w in range(capacity, item.weight - 1, -1):  # backwards!
        dp[w] = max(dp[w], dp[w - item.weight] + item.value)

# Unbounded Knapsack (items unlimited)
dp = [0] * (capacity + 1)
for item in items:
    for w in range(item.weight, capacity + 1):  # forwards!
        dp[w] = max(dp[w], dp[w - item.weight] + item.value)
```

### String Matching DP
```python
# State: dp[i][j] = answer for s1[0:i] and s2[0:j]
dp = [[0] * (n + 1) for _ in range(m + 1)]
dp[0][0] = base_case
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if s1[i-1] == s2[j-1]:
            dp[i][j] = dp[i-1][j-1] + ...
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

### Game Theory DP (Score Difference)
```python
# State: dp[i][j] = max score difference for range [i, j]
dp = [[0] * n for _ in range(n)]
for i in range(n):
    dp[i][i] = arr[i]
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        dp[i][j] = max(arr[i] - dp[i+1][j], arr[j] - dp[i][j-1])
```

## Space Optimization Techniques

### 1. Rolling Array (2D → 1D)
When `dp[i]` only depends on `dp[i-1]`, use a single array:
```python
# Instead of dp[i][j] = dp[i-1][j] + dp[i][j-1]
dp = [0] * n
for i in range(m):
    for j in range(n):
        dp[j] = dp[j] + dp[j-1]  # dp[j] is from prev row, dp[j-1] is current row
```

### 2. Two Variables (1D → O(1))
When `dp[i]` only depends on `dp[i-1]` and `dp[i-2]`:
```python
prev2, prev1 = base1, base2
for i in range(3, n + 1):
    curr = prev1 + prev2
    prev2, prev1 = prev1, curr
```

### 3. Diagonal Traversal (String DP)
When computing `dp[i][j]` needs `dp[i-1][j-1]`:
```python
prev = 0
for j in range(1, n + 1):
    temp = dp[j]
    if match:
        dp[j] = prev + 1
    else:
        dp[j] = max(dp[j], dp[j-1])
    prev = temp
```

## Common Mistakes to Avoid

1. **Wrong loop order in knapsack**: 0/1 knapsack needs backwards iteration, unbounded needs forwards
2. **Off-by-one errors**: Be consistent with 0-indexed vs 1-indexed dp arrays
3. **Missing base cases**: Always handle empty string/array/single element
4. **Integer overflow**: Use modulo (10^9+7) when required
5. **Not handling negative numbers**: Some DP problems have negative values (Dungeon Game)
6. **Forgetting to initialize**: Use appropriate infinity value (float('inf') or n+1)
7. **Confusing subsequence vs substring**: Subsequence = not contiguous, substring = contiguous

## DP Problem Solving Checklist

Before coding, answer these questions:

- [ ] What does `dp[i]` or `dp[i][j]` represent?
- [ ] What are the base cases?
- [ ] What is the recurrence relation?
- [ ] What is the loop order?
- [ ] Can I optimize space?
- [ ] What are the edge cases?
- [ ] Do I need modulo arithmetic?

## Complexity Cheat Sheet

| Pattern | Time | Space | Space Optimized |
|---------|------|-------|-----------------|
| 1D Linear | O(n) | O(n) | O(1) |
| 2D Grid | O(m×n) | O(m×n) | O(n) |
| Interval | O(n³) | O(n²) | O(n²) |
| Knapsack | O(n×W) | O(n×W) | O(W) |
| String Match | O(m×n) | O(m×n) | O(n) |
| LIS (n²) | O(n²) | O(n) | O(n) |
| LIS (n log n) | O(n log n) | O(n) | O(n) |
| Coin Change | O(amount×k) | O(amount) | O(amount) |

---

# Final Notes

## Key Takeaways

1. **DP is not magic** — It's just recursion + memoization. Start with recursion, then optimize.
2. **State definition is everything** — If you define the state correctly, the recurrence almost writes itself.
3. **Practice pattern recognition** — The hardest part is knowing which pattern applies.
4. **Start with brute force** — Even a O(2^n) recursive solution shows you understand the problem.
5. **Draw the DP table** — For 2D problems, manually fill a small table to verify your recurrence.

## Recommended Study Order

**Week 1: Foundations**
- Problems 1-10 (Easy) — Master basic patterns
- Problems 11-15 (Medium) — Coin change, LIS

**Week 2: Core Patterns**
- Problems 16-25 (Medium) — String DP, Grid DP, Knapsack
- Problems 26-35 (Medium) — Advanced patterns

**Week 3: Advanced**
- Problems 36-45 (Hard) — Edit distance, Interval DP, Egg drop
- Problems 46-55 (Hard) — Game theory, Combinatorial DP

**Week 4: Review**
- Redo all problems you couldn't solve in target time
- Focus on patterns you find difficult

## Infosys SP DSE Specific Tips

1. **DP is guaranteed** — At least 1-2 DP problems will appear
2. **Medium difficulty most likely** — Focus on problems 11-35
3. **Time limit** — You have ~45 minutes per coding question
4. **Partial credit** — Even a correct recurrence without optimization may earn points
5. **Edge cases matter** — Test with empty arrays, single elements, max constraints

Good luck with your preparation! Remember: consistent practice beats last-minute cramming.
