# Knapsack Variants — Complete Guide

## 0/1 Knapsack Problem

Given weights[i] and values[i], maximize value with capacity W. Each item chosen at most once.

**Concept:** dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i]] + val[i]) for each item i and weight w.

### Recursive

```python
def knapsack_recursive(W: int, wt: list, val: list, n: int = None) -> int:
    if n is None:
        n = len(wt)
    if n == 0 or W == 0:
        return 0
    if wt[n - 1] > W:
        return knapsack_recursive(W, wt, val, n - 1)
    return max(knapsack_recursive(W, wt, val, n - 1),
               val[n - 1] + knapsack_recursive(W - wt[n - 1], wt, val, n - 1))

# Time: O(2^n), Space: O(n) recursion stack
```

### Memoization

```python
def knapsack_memo(W: int, wt: list, val: list, n: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if n is None:
        n = len(wt)
    if n == 0 or W == 0:
        return 0
    key = (n, W)
    if key in memo:
        return memo[key]
    if wt[n - 1] > W:
        memo[key] = knapsack_memo(W, wt, val, n - 1, memo)
    else:
        memo[key] = max(knapsack_memo(W, wt, val, n - 1, memo),
                        val[n - 1] + knapsack_memo(W - wt[n - 1], wt, val, n - 1, memo))
    return memo[key]

# Time: O(n × W), Space: O(n × W) for memo
```

### Tabulation

```python
def knapsack_tab(W: int, wt: list, val: list) -> int:
    n = len(wt)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            if wt[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w],
                               val[i - 1] + dp[i - 1][w - wt[i - 1]])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][W]

# DP Table for wt=[1,3,4,5], val=[1,4,5,7], W=7:
#    0  1  2  3  4  5  6  7
# 0  0  0  0  0  0  0  0  0
# 1  0  1  1  1  1  1  1  1
# 2  0  1  1  4  5  5  5  5
# 3  0  1  1  4  5  6  6  9
# 4  0  1  1  4  5  7  8  9
# Answer: 9

# Time: O(n × W), Space: O(n × W)
```

### Space Optimized (1D array)

```python
def knapsack_optimized(W: int, wt: list, val: list) -> int:
    n = len(wt)
    dp = [0] * (W + 1)
    for i in range(n):
        for w in range(W, wt[i] - 1, -1):
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]])
    return dp[W]

# Time: O(n × W), Space: O(W)
```

---

## Subset Sum Problem

Given an array of positive integers, determine if there exists a subset with sum equal to target.

**Concept:** dp[i][s] = dp[i-1][s] or dp[i-1][s-nums[i]] if s >= nums[i]

```python
def subset_sum_memo(nums: list, target: int, i: int = None, memo=None) -> bool:
    if memo is None:
        memo = {}
    if i is None:
        return subset_sum_memo(nums, target, len(nums), memo)
    if target == 0:
        return True
    if i == 0:
        return False
    key = (i, target)
    if key in memo:
        return memo[key]
    ans = subset_sum_memo(nums, target, i - 1, memo)
    if not ans and nums[i - 1] <= target:
        ans = ans or subset_sum_memo(nums, target - nums[i - 1], i - 1, memo)
    memo[key] = ans
    return memo[key]

def subset_sum_tab(nums: list, target: int) -> bool:
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = True
    for i in range(1, n + 1):
        for s in range(1, target + 1):
            dp[i][s] = dp[i - 1][s]
            if nums[i - 1] <= s:
                dp[i][s] = dp[i][s] or dp[i - 1][s - nums[i - 1]]
    return dp[n][target]

def subset_sum_optimized(nums: list, target: int) -> bool:
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                dp[s] = True
        if dp[target]:
            return True
    return dp[target]

# Example: nums = [3, 34, 4, 12, 5, 2], target = 9
# Answer: True (4 + 5 = 9)

# Time: O(n × target), Space: O(target)
```

---

## Equal Subset Sum Partition

Given an array, check if it can be partitioned into two subsets with equal sum.

**Concpet:** target = sum/2, check subset sum exists.

```python
def can_partition(nums: list) -> bool:
    total = sum(nums)
    if total % 2 != 0:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                if s == target:
                    return True
                dp[s] = True
    return dp[target]

# Example: nums = [1, 5, 11, 5]
# Answer: True ([1, 5, 5] and [11])

# Time: O(n × target), Space: O(target)
```

---

## Count Subsets with Given Sum

Count the number of subsets that sum exactly to target.

```python
def count_subsets_memo(nums: list, target: int, i: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if i is None:
        return count_subsets_memo(nums, target, len(nums) - 1, memo)
    if target == 0:
        return 1
    if i < 0:
        return 0
    key = (i, target)
    if key in memo:
        return memo[key]
    ways = count_subsets_memo(nums, target, i - 1, memo)
    if nums[i] <= target:
        ways += count_subsets_memo(nums, target - nums[i], i - 1, memo)
    memo[key] = ways
    return ways

def count_subsets_tab(nums: list, target: int) -> int:
    n = len(nums)
    dp = [[0] * (target + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = 1
    for i in range(1, n + 1):
        for s in range(1, target + 1):
            dp[i][s] = dp[i - 1][s]
            if nums[i - 1] <= s:
                dp[i][s] += dp[i - 1][s - nums[i - 1]]
    return dp[n][target]

def count_subsets_optimized(nums: list, target: int) -> int:
    dp = [0] * (target + 1)
    dp[0] = 1
    for num in nums:
        for s in range(target, num - 1, -1):
            if dp[s - num] > 0:
                dp[s] += dp[s - num]
    return dp[target]

# Example: nums = [2, 3, 5, 6, 8, 10], target = 10
# Answer: 3 ({2, 8}, {10}, {2, 3, 5})

# Time: O(n × target), Space: O(target)
```

---

## Minimum Subset Sum Difference

Given an array, partition into two subsets minimizing absolute difference of their sums.

```python
def min_subset_diff(nums: list) -> int:
    total = sum(nums)
    n = len(nums)
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for num in numos:
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                dp[s] = True
    for s in range(target, -1, -1):
        if dp[s]:
            return total - 2 * s
    return total

# Example: nums = [1, 6, 11, 5]
# sum=23, target=11
# Closest sum reachable ≤ target = 11 (6+5)
# Answer: 23 - 2*11 = 1

# Time: O(n × target), Space: O(target)
```

---

## Unbounded Knapsack

Each item can be chosen unlimited times.

**Concept:** dp[w] = max(dp[w], val[i] + dp[w - wt[i]])

```python
def unbounded_knapsack_tab(W: int, wt: list, val: list) -> int:
    n = len(wt)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            if wt[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], val[i - 1] + dp[i][w - wt[i - 1]])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][W]

def unbounded_knapsack_optimized(W: int, wt: list, val: list) -> int:
    dp = [0] * (W + 1)
    for i in range(len(wt)):
        for w in range(wt[i], W + 1):
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]])
    return dp[W]

# Key difference from 0/1: inner loop goes left to right (allows reuse)
# 0/1 Knapsack: inner loop right to left (prevents reuse)
# Unbounded:   inner loop left to right  (allows reuse)

# Time: O(n × W), Space: O(W)
```

---

## Coin Change (Minimum Coins)

Given coins denominations and amount, find minimum number of coins needed.

```python
def coin_change_memo(coins: list, amount: int, memo=None) -> int:
    if memo is None:
        memo = {}
    if amount == 0:
        return 0
    if amount < 0:
        return float('inf')
    if amount in memo:
        return memo[amount]
    min_coins = float('inf')
    for coin in coins:
        res = coin_change_memo(coins, amount - coin, memo)
        if res != float('inf'):
            min_coins = min(min_coins, 1 + res)
    memo[amount] = min_coins
    return memo[amount]

def coin_change_tab(coins: list, amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

# Example: coins = [1, 2, 5], amount = 11 -> Answer: 3 (5 + 5 + 1)
# Example: coins = [2], amount = 3 -> Answer: -1

# Time: O(n × amount), Space: O(amount)
```

---

## Coin Change II (Number of Ways)

Count number of combinations that make up the amount.

```python
def change_memo(coins: list, amount: int, i: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if amount == 0:
        return 1
    if amount < 0 or i is None or i < 0:
        return 0
    key = (i, amount)
    if key in memo:
        return memo[key]
    ways = change_memo(coins, amount, i - 1, memo)
    if coins[i] <= amount:
        ways += change_memo(coins, amount - coins[i], i, memo)
    memo[key] = ways
    return memo[key]

def change_tab(coins: list, amount: int) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]
    return dp[amount]

# Example: coins = [1, 2, 5], amount = 5
# Answer: 4 ({5}, {2,2,1}, {2,1,1,1}, {1,1,1,1,1})
# NOT: {1,2,2} and {2,1,2} are the same set

# Time: O(n × amount), Space: O(amount)
```

---

## Rod Cutting

Given rod length n and price array price[i] (i+1 length price). Find max revenue by cutting optimally.

```python
def rod_cutting_memo(price: list, n: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if n is None:
        n = len(price)
    if n <= 0:
        return 0
    if n in memo:
        return memo[n]
    max_val = float('-inf')
    for i in range(1, n + 1):
        if i <= len(price):
            max_val = max(max_val, price[i - 1] + rod_cutting_memo(price, n - i, memo))
    memo[n] = max_val
    return memo[n]

def rod_cutting_tab(price: list, n: int = None) -> int:
    if n is None:
        n = len(price)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        max_val = float('-inf')
        for j in range(1, i + 1):
            if j <= len(price):
                max_val = max(max_val, price[j - 1] + dp[i - j])
        dp[i] = max_val
    return dp[n]

def rod_cutting_optimized(price: list) -> int:
    n = len(price)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            dp[i] = max(dp[i], price[j - 1] + dp[i - j])
    return dp[n]

# Example: price = [1, 5, 8, 9, 10, 17, 17, 20]
# n=8: Answer = 22 (2+6, cuts: 2+6, price 5+17)

# Time: O(n²), Space: O(n)
```

---

## Summary Table

| Problem | Type | Approach | Time | Space |
|---------|------|----------|------|-------|
| 0/1 Knapsack | 1 item limit | DP with W capacity | O(n×W) | O(W) |
| Subset Sum | Decision | Boolean DP | O(n×target) | O(target) |
| Equal Partition | Decision | target = sum/2 | O(n×target) | O(target) |
| Count Subsets | Count | Combinations DP | O(n×target) | O(target) |
| Min Subset Diff | Optimization | Closest sum to target | O(n×target) | O(target) |
| Unbounded Knapsack | Unlimited items | Left-to-right loop | O(n×W) | O(W) |
| Coin Change (min) | Minimization | Unbounded pattern | O(n×W) | O(W) |
| Coin Change II | Count combos | Unbounded pattern | O(n×W) | O(W) |
| Rod Cutting | Unbounded variant | O(n²) iteration | O(n²) | O(n) |
