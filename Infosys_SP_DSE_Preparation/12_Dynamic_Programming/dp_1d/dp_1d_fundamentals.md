# 1D Dynamic Programming — Fundamentals

## What is Dynamic Programming?

Dynamic Programming is an algorithmic technique that solves problems by:
1. Dividing into **overlapping subproblems**
2. Solving each subproblem **once**
3. **Storing** the result for reuse

Two approaches:
- **Memoization (Top-Down):** Recursive + caching. Solve the problem naturally, cache results.
- **Tabulation (Bottom-Up):** Iterative table filling. Start from base cases, build up to target.

---

## Fibonacci Numbers

Classic DP. F(n) = F(n-1) + F(n-2). Base: F(0)=0, F(1)=1.

### Recursive (Exponential) — for comparison

```python
def fib_recursive(n: int) -> int:
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)

# Time: O(2^n), Space: O(n)
```

### Memoization (Top-Down)

```python
def fib_memo(n: int, memo=None) -> int:
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

# Time: O(n), Space: O(n)
```

### Tabulation (Bottom-Up)

```python
def fib_tab(n: int) -> int:
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

# Time: O(n), Space: O(n)
```

### Space Optimized Tabulation

```python
def fib_optimized(n: int) -> int:
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1

# Time: O(n), Space: O(1)
```

---

## Climbing Stairs

You are climbing a staircase. It takes n steps to reach the top. Each time you can climb 1 or 2 steps. In how many ways can you reach the top?

**Concept:** Same as Fibonacci. ways(n) = ways(n-1) + ways(n-2)

```python
def climb_stairs_memo(n: int, memo=None) -> int:
    if memo is None:
        memo = {}
    if n <= 1:
        return 1
    if n not in memo:
        memo[n] = climb_stairs_memo(n - 1, memo) + climb_stairs_memo(n - 2, memo)
    return memo[n]

def climb_stairs_tab(n: int) -> int:
    if n <= 1:
        return 1
    dp = [0] * (n + 1)
    dp[0], dp[1] = 1, 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

def climb_stairs_optimized(n: int) -> int:
    if n <= 1:
        return 1
    prev2, prev1 = 1, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1

# Time: O(n), Space: O(1) for optimized
```

---

## Min Cost Climbing Stairs

You start at index 0 or 1. cost[i] is the cost to step on stair i. You can climb 1 or 2 steps from any stair. Find min cost to reach the top (beyond last index).

**Concept:** dp[i] = cost[i] + min(dp[i-1], dp[i-2])

```python
def min_cost_climbing_memo(cost: list, i: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if i is None:
        return min(min_cost_climbing_memo(cost, len(cost) - 1, memo),
                   min_cost_climbing_memo(cost, len(cost) - 2, memo))
    if i < 0:
        return 0
    if i == 0 or i == 1:
        return cost[i]
    if i not in memo:
        memo[i] = cost[i] + min(min_cost_climbing_memo(cost, i - 1, memo),
                                min_cost_climbing_memo(cost, i - 2, memo))
    return memo[i]

def min_cost_climbing_tab(cost: list) -> int:
    n = len(cost)
    dp = [0] * (n + 1)
    dp[0], dp[1] = cost[0], cost[1]
    for i in range(2, n + 1):
        step_cost = cost[i] if i < n else 0
        dp[i] = step_cost + min(dp[i - 1], dp[i - 2])
    return dp[n]

def min_cost_climbing_optimized(cost: list) -> int:
    prev2, prev1 = cost[0], cost[1]
    for i in range(2, len(cost)):
        curr = cost[i] + min(prev1, prev2)
        prev2, prev1 = prev1, curr
    return min(prev1, prev2)

# Time: O(n), Space: O(1)
```

---

## House Robber I

Given an integer array nums. Adjacent houses cannot be robbed on the same night. Maximize sum.

**Concept:** dp[i] = max(dp[i-1], dp[i-2] + nums[i])

```python
def rob_memo(nums: list, i: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if i is None:
        return rob_memo(nums, len(nums) - 1, memo)
    if i < 0:
        return 0
    if i == 0:
        return nums[0]
    if i not in memo:
        memo[i] = max(rob_memo(nums, i - 1, memo),
                      rob_memo(nums, i - 2, memo) + nums[i])
    return memo[i]

def rob_tab(nums: list) -> int:
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    for i in range(2, len(nums)):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
    return dp[-1]

def rob_optimized(nums: list) -> int:
    prev2, prev1 = 0, 0
    for num in nums:
        curr = max(prev1, prev2 + num)
        prev2, prev1 = prev1, curr
    return prev1

# Time: O(n), Space: O(1)
```

---

## House Robber II (Circular)

Same as House Robber but houses are arranged in a circle. First and last are adjacent.

**Approach:** Solve House Robber I on arr[0:n-1] and arr[1:n], take max.

```python
def rob_linear(nums: list) -> int:
    prev2, prev1 = 0, 0
    for num in nums:
        curr = max(prev1, prev2 + num)
        prev2, prev1 = prev1, curr
    return prev1

def rob_circular(nums: list) -> int:
    if len(nums) == 1:
        return nums[0]
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))

# Time: O(n), Space: O(1)
```

---

## Paint Fence

There is a fence with n posts. Each post can be painted with one of k colors. No two adjacent posts can have the same color. No three adjacent posts can have the SAME color pattern.

**Concept:**
- same[i] = diff[i-1] (same color as previous)
- diff[i] = (same[i-1] + diff[i-1]) * (k-1) (different from previous)
- total[i] = same[i] + diff[i]

```python
def paint_fence_tab(n: int, k: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return k
    same, diff = k, k * (k - 1)
    for _ in range(3, n + 1):
        new_same = diff
        new_diff = (same + diff) * (k - 1)
        same, diff = new_same, new_diff
    return same + diff

# Time: O(n), Space: O(1)
```

### Paint House I

There are n houses in a row. Each house can be painted with red, blue, or green. The cost of painting each house with a certain color is given. No two adjacent houses can be the same color.

**Concept:** dp[i][color] = cost[i][color] + min(dp[i-1][other colors])

```python
def paint_house_tab(costs: list) -> int:
    if not costs:
        return 0
    r, g, b = costs[0]
    for i in range(1, len(costs)):
        new_r = costs[i][0] + min(g, b)
        new_g = costs[i][1] + min(r, b)
        new_b = costs[i][2] + min(r, g)
        r, g, b = new_r, new_g, new_b
    return min(r, g, b)

# Time: O(n), Space: O(1)
```

---

## Decode Ways

A message containing letters A-Z ('1' to '26') can be encoded into digits. Count number of ways to decode.

**Concept:** dp[i] = dp[i-1] (if s[i] is valid) + dp[i-2] (if s[i-1:i+1] is valid)

```python
def num_decodings_memo(s: str, i: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if i is None:
        return num_decodings_memo(s, len(s), memo)
    if i == 0:
        return 1
    if i < 0:
        return 0
    if i in memo:
        return memo[i]
    ways = 0
    if s[i - 1] != '0':
        ways += num_decodings_memo(s, i - 1, memo)
    if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:
        ways += num_decodings_memo(s, i - 2, memo)
    memo[i] = ways
    return memo[i]

def num_decodings_tab(s: str) -> int:
    if not s or s[0] == '0':
        return 0
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1 if s[0] != '0' else 0
    for i in range(2, n + 1):
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]
        if 10 <= int(s[i - 2:i]) <= 26:
            dp[i] += dp[i - 2]
    return dp[n]

def num_decodings_optimized(s: str) -> int:
    if not s or s[0] == '0':
        return 0
    prev2, prev1 = 1, 1
    for i in range(2, len(s) + 1):
        curr = 0
        if s[i - 1] != '0':
            curr += prev1
        if 10 <= int(s[i - 2:i]) <= 26:
            curr += prev2
        prev2, prev1 = prev1, curr
    return prev1

# Time: O(n), Space: O(1)
```

---

## Maximum Sum of Non-Adjacent Elements

Given an array, find max sum of subsequence where no two elements are adjacent.

**Concept:** Same as House Robber I.

```python
def max_sum_nonadjacent(nums: list) -> int:
    prev2, prev1 = 0, 0
    for num in nums:
        curr = max(prev1, prev2 + num)
        prev2, prev1 = prev1, curr
    return prev1

# Time: O(n), Space: O(1)
```

---

## Longest Increasing Subsequence (O(n²))

Given an unsorted array of integers, find length of longest increasing subsequence.

**Concept:** dp[i] = max(dp[i], dp[j] + 1) for all j < i where nums[j] < nums[i]

```python
def lis_n2_memo(nums: list, i: int = None, prev: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if i is None:
        return lis_n2_memo(nums, 0, float('-inf'), memo)
    if i == len(nums):
        return 0
    key = (i, prev)
    if key in memo:
        return memo[key]
    taken = 0
    if nums[i] > prev:
        taken = 1 + lis_n2_memo(nums, i + 1, nums[i], memo)
    not_taken = lis_n2_memo(nums, i + 1, prev, memo)
    memo[key] = max(taken, not_taken)
    return memo[key]

def lis_n2_tab(nums: list) -> int:
    if not nums:
        return 0
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

# Time: O(n²), Space: O(n)
```

---

## Longest Increasing Subsequence (O(n log n) with Patience Sorting)

Maintain piles where each pile's top is the smallest possible tail of an LIS of that length.

```python
import bisect

def lis_nlogn(nums: list) -> int:
    piles = []
    for num in numos:
        pos = bisect.bisect_left(piles, num)
        if pos == len(piles):
            piles.append(num)
        else:
            piles[pos] = num
    return len(piles)

# Example: nums = [10, 9, 2, 5, 3, 7, 101, 18]
# piles evolves: [10] -> [9] -> [2] -> [2,5] -> [2,3] -> [2,3,7] -> [2,3,7,101] -> [2,3,7,18]
# Answer: 4

# Time: O(n log n), Space: O(n)
```

---

## Number of Longest Increasing Subsequence

Given an array, find the count of LIS.

```python
def find_number_of_lis(nums: list) -> int:
    if not nums:
        return 0
    n = len(nums)
    lengths = [1] * n  # length of LIS ending at i
    counts = [1] * n   # count of LIS ending at i
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if lengths[j] + 1 > lengths[i]:
                    lengths[i] = lengths[j] + 1
                    counts[i] = counts[j]
                elif lengths[j] + 1 == lengths[i]:
                    counts[i] += counts[j]
    max_len = max(lengths)
    return sum(c for l, c in zip(lengths, counts) if l == max_len)

# Time: O(n²), Space: O(n)
```

---

## Summary Table

| Problem | Approach | Time | Space |
|---------|----------|------|-------|
| Fibonacci | DP + Optimization | O(n) | O(1) |
| Climbing Stairs | DP + Fibonacci pattern | O(n) | O(1) |
| Min Cost Climbing Stairs | DP + min aggregation | O(n) | O(1) |
| House Robber I | DP with max of previous | O(n) | O(1) |
| House Robber II | Two linear passes | O(n) | O(n) |
| Paint Fence | DP with same/different tracking | O(n) | O(1) |
| Decode Ways | DP with conditional addition | O(n) | O(1) |
| LIS O(n²) | Nested loops DP | O(n²) | O(n) |
| LIS O(n log n) | Patience Sorting | O(n log n) | O(n) |
