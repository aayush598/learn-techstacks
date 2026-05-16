# Dynamic Programming

## Problem 1: 0/1 Knapsack
**Difficulty: Medium | Marks: 30-50**

```python
def knapsack_01(weights, values, capacity):
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w],
                               dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][capacity]

weights = [10, 20, 30]
values = [60, 100, 120]
capacity = 50
print(knapsack_01(weights, values, capacity))
```

### Space Optimized

```python
def knapsack_01_optimized(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for i in range(len(weights)):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]

print(knapsack_01_optimized(weights, values, capacity))
```

---

## Problem 2: Unbounded Knapsack (Coin Change - Max Ways)
**Difficulty: Medium | Marks: 30-50**

```python
def coin_change_max_ways(coins, amount):
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    return dp[amount]

coins = [1, 2, 5]
amount = 5
print(coin_change_max_ways(coins, amount))
```

---

## Problem 3: Coin Change - Minimum Coins
**Difficulty: Medium | Marks: 30**

```python
def coin_change_min_coins(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

coins = [1, 2, 5]
amount = 11
print(coin_change_min_coins(coins, amount))
```

---

## Problem 4: Longest Increasing Subsequence (LIS)
**Difficulty: Medium | Marks: 30**

```python
def length_of_lis(nums):
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

nums = [10, 9, 2, 5, 3, 7, 101, 18]
print(length_of_lis(nums))
```

### LIS with Binary Search (O(n log n))

```python
import bisect

def length_of_lis_optimized(nums):
    tails = []
    for num in nums:
        i = bisect.bisect_left(tails, num)
        if i == len(tails):
            tails.append(num)
        else:
            tails[i] = num
    return len(tails)

print(length_of_lis_optimized(nums))
```

---

## Problem 5: Longest Common Subsequence (LCS)
**Difficulty: Medium | Marks: 30**

```python
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

text1 = "abcde"
text2 = "ace"
print(longest_common_subsequence(text1, text2))
```

---

## Problem 6: Edit Distance (Levenshtein Distance)
**Difficulty: Hard | Marks: 50**

```python
def edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]

word1 = "horse"
word2 = "ros"
print(edit_distance(word1, word2))
```

---

## Problem 7: Longest Palindromic Subsequence
**Difficulty: Medium | Marks: 30**

```python
def longest_palindromic_subsequence(s):
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

s = "bbbab"
print(longest_palindromic_subsequence(s))
```

---

## Problem 8: Matrix Chain Multiplication
**Difficulty: Hard | Marks: 50**

```python
def matrix_chain_order(dims):
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                dp[i][j] = min(dp[i][j], cost)
    return dp[0][n - 1]

dims = [10, 30, 5, 60]
print(matrix_chain_order(dims))
```

---

## Problem 9: Maximum Sum Increasing Subsequence
**Difficulty: Medium | Marks: 30**

```python
def max_sum_increasing_subseq(nums):
    n = len(nums)
    dp = nums[:]
    for i in range(n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + nums[i])
    return max(dp)

nums = [1, 101, 2, 3, 100, 4, 5]
print(max_sum_increasing_subseq(nums))
```

---

## Problem 10: Subset Sum Problem
**Difficulty: Medium | Marks: 30**

```python
def subset_sum(nums, target):
    n = len(nums)
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
    return dp[target]

nums = [3, 34, 4, 12, 5, 2]
target = 9
print(subset_sum(nums, target))
```

---

## Problem 11: Partition Equal Subset Sum
**Difficulty: Medium | Marks: 30**

```python
def can_partition(nums):
    total = sum(nums)
    if total % 2 != 0:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
    return dp[target]

nums = [1, 5, 11, 5]
print(can_partition(nums))
```

---

## Problem 12: Unique Paths (Grid)
**Difficulty: Easy-Medium | Marks: 20-30**

```python
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]

print(unique_paths(3, 7))
```

---

## Problem 13: Unique Paths with Obstacles
**Difficulty: Medium | Marks: 30**

```python
def unique_paths_with_obstacles(obstacle_grid):
    if obstacle_grid[0][0]:
        return 0
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1
    for j in range(1, n):
        dp[0][j] = 0 if obstacle_grid[0][j] else dp[0][j - 1]
    for i in range(1, m):
        dp[i][0] = 0 if obstacle_grid[i][0] else dp[i - 1][0]
    for i in range(1, m):
        for j in range(1, n):
            if obstacle_grid[i][j]:
                dp[i][j] = 0
            else:
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]

grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
print(unique_paths_with_obstacles(grid))
```

---

## Problem 14: Minimum Path Sum
**Difficulty: Medium | Marks: 30**

```python
def min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    for i in range(1, m):
        grid[i][0] += grid[i - 1][0]
    for j in range(1, n):
        grid[0][j] += grid[0][j - 1]
    for i in range(1, m):
        for j in range(1, n):
            grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])
    return grid[m - 1][n - 1]

grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
print(min_path_sum(grid))
```

---

## Problem 15: House Robber
**Difficulty: Easy-Medium | Marks: 20-30**

```python
def rob(nums):
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

nums = [2, 7, 9, 3, 1]
print(rob(nums))
```

---

## Problem 16: House Robber II (Circular)
**Difficulty: Medium | Marks: 30**

```python
def rob_circular(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    def rob_linear(arr):
        if not arr:
            return 0
        prev2 = prev1 = 0
        for num in arr:
            curr = max(prev1, prev2 + num)
            prev2 = prev1
            prev1 = curr
        return prev1
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))

nums = [2, 3, 2]
print(rob_circular(nums))
```

---

## Problem 17: Decode Ways
**Difficulty: Medium | Marks: 30**

```python
def num_decodings(s):
    if not s or s[0] == '0':
        return 0
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    for i in range(2, n + 1):
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]
        if 10 <= int(s[i - 2:i]) <= 26:
            dp[i] += dp[i - 2]
    return dp[n]

s = "226"
print(num_decodings(s))
```

---

## Problem 18: Word Break
**Difficulty: Medium | Marks: 30**

```python
def word_break(s, word_dict):
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]

s = "leetcode"
word_dict = ["leet", "code"]
print(word_break(s, word_dict))
```

---

## Problem 19: Integer Break (Max Product)
**Difficulty: Medium | Marks: 30**

```python
def integer_break(n):
    if n == 2:
        return 1
    if n == 3:
        return 2
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        for j in range(1, i):
            dp[i] = max(dp[i], j * (i - j), j * dp[i - j])
    return dp[n]

print(integer_break(10))
```

---

## Problem 20: Count Arrays with Divisibility Condition
**Difficulty: Hard | Marks: 50**

Asked in Infosys SP/DSE exam - count arrays of length K with a[i] in [1,N] and a[i+1] divisible by a[i].

```python
def count_divisible_arrays(n, k):
    MOD = 10000
    dp = [[0] * (n + 1) for _ in range(k + 1)]
    for j in range(1, n + 1):
        dp[1][j] = 1
    for i in range(2, k + 1):
        for j in range(1, n + 1):
            for m in range(j, n + 1, j):
                dp[i][m] = (dp[i][m] + dp[i - 1][j]) % MOD
    return sum(dp[k]) % MOD

n, k = 2, 2
print(count_divisible_arrays(n, k))
```

---

## Problem 21: Longest Bitwise AND/OR Subsequence
**Difficulty: Hard | Marks: 50**

Asked in Infosys SP exam - longest increasing subsequence with condition (A[i] & A[i+1]) * 2 < (A[i] | A[i+1]).

```python
def bitwise_lis(arr):
    n = len(arr)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if arr[i] > arr[j] and (arr[j] & arr[i]) * 2 < (arr[j] | arr[i]):
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp) if dp else 0

arr = [15, 6, 5, 12, 1]
print(bitwise_lis(arr))
```

---

## Problem 22: Egg Dropping
**Difficulty: Hard | Marks: 50**

```python
def egg_drop(eggs, floors):
    dp = [[0] * (floors + 1) for _ in range(eggs + 1)]
    for i in range(1, floors + 1):
        dp[1][i] = i
    for e in range(2, eggs + 1):
        for f in range(1, floors + 1):
            dp[e][f] = float('inf')
            for k in range(1, f + 1):
                res = 1 + max(dp[e - 1][k - 1], dp[e][f - k])
                dp[e][f] = min(dp[e][f], res)
    return dp[eggs][floors]

print(egg_drop(2, 100))
```

---

## Problem 23: Maximum Product Subarray
**Difficulty: Medium | Marks: 30**

```python
def max_product_subarray(nums):
    if not nums:
        return 0
    max_prod = min_prod = result = nums[0]
    for num in nums[1:]:
        candidates = (num, max_prod * num, min_prod * num)
        max_prod = max(candidates)
        min_prod = min(candidates)
        result = max(result, max_prod)
    return result

nums = [2, 3, -2, 4]
print(max_product_subarray(nums))
```

---

## Problem 24: Palindromic Substrings Count
**Difficulty: Medium | Marks: 30**

```python
def count_substrings(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    count = 0
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 3 or dp[i + 1][j - 1]):
                dp[i][j] = True
                count += 1
    return count

s = "abc"
print(count_substrings(s))
```

---

## Problem 25: Distinct Subsequences
**Difficulty: Hard | Marks: 50**

```python
def num_distinct(s, t):
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = 1
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]
            else:
                dp[i][j] = dp[i - 1][j]
    return dp[m][n]

s = "rabbbit"
t = "rabbit"
print(num_distinct(s, t))
```
