# Knapsack Variants — Complete Guide

## Decision Tree for Knapsack Problems

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    KNAPSACK PATTERN DECISION TREE                        │
│                                                                          │
│  "Can I pick each item at most once?"                                    │
│       │                                                                  │
│       ├─ YES → 0/1 Knapsack (loop capacity RIGHT-TO-LEFT)              │
│       │                                                                  │
│       └─ NO → "Can I pick unlimited times?"                             │
│                │                                                         │
│                ├─ YES → Unbounded Knapsack (loop capacity LEFT-TO-RIGHT)│
│                │                                                         │
│                └─ NO → "Limited count[i] for each item?"                │
│                         │                                                │
│                         └─ YES → Bounded Knapsack (binary splitting)    │
│                                                                          │
│  Variants of 0/1 Knapsack:                                              │
│    - Subset Sum?      → dp[i][s] = dp[i-1][s] or dp[i-1][s-num[i]]    │
│    - Equal Partition? → target = sum/2, check subset sum                │
│    - Count subsets?   → dp[i][s] = dp[i-1][s] + dp[i-1][s-num[i]]     │
│    - Min diff?        → closest subset sum to total/2                   │
│                                                                          │
│  Variants of Unbounded:                                                  │
│    - Coin Change (min)?  → dp[a] = min(dp[a], dp[a-coin] + 1)          │
│    - Coin Change (count)?→ dp[a] += dp[a-coin]                          │
│    - Rod Cutting?        → dp[i] = max over all cut lengths             │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 0/1 Knapsack Problem

Given weights[i] and values[i], maximize value with capacity W. Each item chosen at most once.

### Visual Walkthrough

```
Items:    wt=[1,3,4,5], val=[1,4,5,7], W=7

dp[i][w] = max value using items 0..i-1 with capacity w

     Capacity →   0    1    2    3    4    5    6    7
  ┌─────────────────────────────────────────────────────┐
  │  0 items:  [  0    0    0    0    0    0    0    0 ]│  ← base row
  ├─────────────────────────────────────────────────────┤
  │  item 1:   [  0    1    1    1    1    1    1    1 ]│  wt=1, val=1
  ├─────────────────────────────────────────────────────┤     ↑ only 1 item of wt=1
  │  item 2:   [  0    1    1    4    5    5    5    5 ]│  wt=3, val=4
  ├─────────────────────────────────────────────────────┤     ↑ at w≥3: can take item2
  │  item 3:   [  0    1    1    4    5    6    6    9 ]│  wt=4, val=5
  ├─────────────────────────────────────────────────────┤     ↑ at w=7: items 2+3 = 4+5=9
  │  item 4:   [  0    1    1    4    5    7    8    9 ]│  wt=5, val=7
  └─────────────────────────────────────────────────────┘

Answer: 9 (items with weight 3+4 = values 4+5 = 9)

State transition for dp[i][w]:
  ┌───────────────────────────────────────────────────────────────┐
  │  if wt[i-1] > w:                                              │
  │      dp[i][w] = dp[i-1][w]           # Can't fit, skip item   │
  │  else:                                                         │
  │      dp[i][w] = max(dp[i-1][w],            # Skip item i      │
  │                     val[i-1] + dp[i-1][w-wt[i-1]]) # Take it │
  └───────────────────────────────────────────────────────────────┘
```

### Space-Optimized 1D Version

```python
def knapsack_optimized(W: int, wt: list, val: list) -> int:
    n = len(wt)
    dp = [0] * (W + 1)
    for i in range(n):
        # CRITICAL: iterate capacity RIGHT-TO-LEFT to prevent using item twice
        for w in range(W, wt[i] - 1, -1):
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]])
    return dp[W]

# Why right-to-left?
# If we go left-to-right, dp[w - wt[i]] might have ALREADY been updated
# in this iteration (using item i), allowing item i to be used twice!
#
# Right-to-left ensures dp[w - wt[i]] still reflects the PREVIOUS iteration.

# Time: O(n × W), Space: O(W)
```

### Tracing the 1D Optimization

```
wt=[1,3,4,5], val=[1,4,5,7], W=7

Initial: dp = [0, 0, 0, 0, 0, 0, 0, 0]

Item 1 (wt=1, val=1), loop w=7→1:
  w=7: dp[7] = max(0, 1+dp[6]) = 1
  w=6: dp[6] = max(0, 1+dp[5]) = 1
  ...
  w=1: dp[1] = max(0, 1+dp[0]) = 1
  dp = [0, 1, 1, 1, 1, 1, 1, 1]

Item 2 (wt=3, val=4), loop w=7→3:
  w=7: dp[7] = max(1, 4+dp[4]) = max(1,4+1) = 5
  w=6: dp[6] = max(1, 4+dp[3]) = max(1,4+1) = 5
  w=5: dp[5] = max(1, 4+dp[2]) = max(1,4+1) = 5
  w=4: dp[4] = max(1, 4+dp[1]) = max(1,4+1) = 5
  w=3: dp[3] = max(1, 4+dp[0]) = max(1,4+0) = 4
  dp = [0, 1, 1, 4, 5, 5, 5, 5]

Item 3 (wt=4, val=5), loop w=7→4:
  w=7: dp[7] = max(5, 5+dp[3]) = max(5,5+4) = 9
  w=6: dp[6] = max(5, 5+dp[2]) = max(5,5+1) = 6
  w=5: dp[5] = max(5, 5+dp[1]) = max(5,5+1) = 6
  w=4: dp[4] = max(5, 5+dp[0]) = max(5,5+0) = 5
  dp = [0, 1, 1, 4, 5, 6, 6, 9]

Item 4 (wt=5, val=7), loop w=7→5:
  w=7: dp[7] = max(9, 7+dp[2]) = max(9,7+1) = 9
  w=6: dp[6] = max(6, 7+dp[1]) = max(6,7+1) = 8
  w=5: dp[5] = max(6, 7+dp[0]) = max(6,7+0) = 7
  dp = [0, 1, 1, 4, 5, 7, 8, 9]  ← Answer: 9
```

---

## Subset Sum Problem

Given an array of positive integers, determine if there exists a subset with sum equal to target.

### Visual Walkthrough

```
nums = [3, 34, 4, 12, 5, 2], target = 9

dp[i][s] = True if subset of nums[0..i-1] sums to s

     Sum →      0    1    2    3    4    5    6    7    8    9
  ┌──────────────────────────────────────────────────────────────┐
  │  0 nums:  [  T    F    F    F    F    F    F    F    F    F ]│  ← sum 0 always possible (empty set)
  ├──────────────────────────────────────────────────────────────┤
  │  num=3:   [  T    F    F    T    F    F    F    F    F    F ]│  ← 3 in subset
  ├──────────────────────────────────────────────────────────────┤
  │  num=34:  [  T    F    F    T    F    F    F    F    F    F ]│  ← 34 > target, no new sums
  ├──────────────────────────────────────────────────────────────┤
  │  num=4:   [  T    F    F    T    T    F    F    F    F    F ]│  ← 3+4=7... wait:
  ├──────────────────────────────────────────────────────────────┤     At s=7: dp[s-4]=dp[3]=T → dp[7]=T
  │  num=12:  [  T    F    F    T    T    F    F    F    F    F ]│     At s=4: dp[s-4]=dp[0]=T → dp[4]=T
  ├──────────────────────────────────────────────────────────────┤
  │  num=5:   [  T    F    F    T    T    T    F    F    F    F ]│  ← 5 directly: dp[5]=T
  ├──────────────────────────────────────────────────────────────┤     4+5=9: dp[9]=T!
  │  num=2:   [  T    F    T    T    T    T    T    F    T    T ]│
  └──────────────────────────────────────────────────────────────┘
                                                     ▲
                                                Answer: T (3+4+2=9)

Space-optimized 1D version:
  dp = [T, F, F, F, F, F, F, F, F, F]
  After num=3:  dp = [T, F, F, T, F, F, F, F, F, F]
  After num=4:  dp = [T, F, F, T, T, F, F, T, F, F]
  After num=5:  dp = [T, F, F, T, T, T, F, T, T, T]  ← dp[9]=T!
```

```python
def subset_sum_optimized(nums: list, target: int) -> bool:
    dp = [False] * (target + 1)
    dp[0] = True  # Base: sum 0 is always achievable (empty subset)
    for num in nums:
        for s in range(target, num - 1, -1):  # Right-to-left (0/1 style!)
            if dp[s - num]:
                dp[s] = True
        if dp[target]:  # Early termination
            return True
    return dp[target]

# Time: O(n × target), Space: O(target)
```

---

## Equal Subset Sum Partition

Given an array, check if it can be partitioned into two subsets with equal sum.

### Key Insight

```
If total_sum is odd → impossible (can't split odd into two equal halves)
If total_sum is even → check if subset with sum = total_sum/2 exists!

Example: nums = [1, 5, 11, 5]
  total = 22, target = 11
  Subset [1, 5, 5] sums to 11 ✓  (other subset [11] also sums to 11)
```

```python
def can_partition(nums: list) -> bool:
    total = sum(nums)
    if total % 2 != 0:
        return False  # Can't split odd sum equally
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                dp[s] = True
                if s == target:  # Early exit
                    return True
    return dp[target]

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

### Critical Difference from 0/1 Knapsack

```
0/1 Knapsack:  inner loop goes RIGHT → LEFT  (prevents reuse)
Unbounded:     inner loop goes LEFT → RIGHT  (allows reuse)

Why? In 0/1 knapsack, right-to-left ensures dp[w-wt[i]] is from the
     PREVIOUS item's row (not yet updated for this item).

     In unbounded, left-to-right means dp[w-wt[i]] may have been
     updated already in this iteration, effectively allowing item i
     to be used again.

  0/1 Knapsack:                Unbounded:
  for w in range(W, wt[i]-1, -1)  for w in range(wt[i], W+1)
       ← ← ← ←                     → → → →
  (fresh values)                   (may reuse current item)
```

```python
def unbounded_knapsack_optimized(W: int, wt: list, val: list) -> int:
    dp = [0] * (W + 1)
    for i in range(len(wt)):
        for w in range(wt[i], W + 1):  # LEFT TO RIGHT!
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]])
    return dp[W]

# Time: O(n × W), Space: O(W)
```

---

## Coin Change (Minimum Coins)

Given coins denominations and amount, find minimum number of coins needed.

### This is Unbounded Knapsack!

```
coins = [1, 2, 5], amount = 11

dp[a] = min coins needed to make amount a

dp = [0, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞]
      0  1  2  3  4  5  6  7  8  9  10 11

After coin=1:
dp = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

After coin=2:
dp = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6]
      ↑ using 2s where beneficial

After coin=5:
dp = [0, 1, 1, 2, 2, 1, 2, 2, 3, 3, 2, 3]
                                     ↑   ↑
                              10=5+5=2   11=5+5+1=3

Answer: 3 (5 + 5 + 1)
```

```python
def coin_change_tab(coins: list, amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base: 0 coins needed for amount 0
    for coin in coins:
        for a in range(coin, amount + 1):  # Left-to-right (unbounded!)
            dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

# Time: O(n × amount), Space: O(amount)
```

---

## Coin Change II (Number of Ways)

Count number of combinations that make up the amount.

### Key Difference from Coin Change I

```
Coin Change I:   min(dp[a], dp[a-coin] + 1)   → minimizing
Coin Change II:  dp[a] += dp[a-coin]           → counting

coins = [1, 2, 5], amount = 5

dp = [1, 0, 0, 0, 0, 0]
      ↑ base: 1 way to make amount 0

After coin=1: dp = [1, 1, 1, 1, 1, 1]   (all 1s)
After coin=2: dp = [1, 1, 2, 2, 3, 3]
After coin=5: dp = [1, 1, 2, 2, 3, 4]
                                     ↑
Answer: 4 ways
  {5}
  {2, 2, 1}
  {2, 1, 1, 1}
  {1, 1, 1, 1, 1}
  Note: {1,2,2} = {2,1,2} = {2,2,1} (same combination, counted once!)
```

```python
def change_tab(coins: list, amount: int) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1  # One way to make amount 0: use no coins
    for coin in coins:          # Iterate coins first → combinations (not permutations)
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]  # Add number of ways
    return dp[amount]

# WARNING: If you swap the loops (amount first, then coins), you count
# PERMUTATIONS instead of combinations! Be careful about problem requirements.

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

## Summary Table & Quick Reference

```
┌──────────────────────────┬──────────────────┬──────────┬──────────┬───────────────────────────────────┐
│ Problem                  │ Type             │ Time     │ Space    │ Key Insight                       │
├──────────────────────────┼──────────────────┼──────────┼──────────┼───────────────────────────────────┤
│ 0/1 Knapsack             │ 1 item limit     │ O(n×W)   │ O(W)     │ Loop R→L (prevent double use)    │
│ Subset Sum               │ Decision         │ O(n×tgt) │ O(tgt)   │ Boolean knapsack variant          │
│ Equal Partition          │ Decision         │ O(n×tgt) │ O(tgt)   │ target = total/2                  │
│ Count Subsets            │ Count            │ O(n×tgt) │ O(tgt)   │ dp[s] += dp[s-num]               │
│ Min Subset Diff          │ Optimization     │ O(n×tgt) │ O(tgt)   │ Closest subset sum to total/2     │
│ Unbounded Knapsack       │ Unlimited items  │ O(n×W)   │ O(W)     │ Loop L→R (allows reuse)           │
│ Coin Change (min coins)  │ Minimization     │ O(n×amt) │ O(amt)   │ Unbounded + min                   │
│ Coin Change II (ways)    │ Count combos     │ O(n×amt) │ O(amt)   │ Unbounded + count                 │
│ Rod Cutting              │ Unbounded variant│ O(n²)    │ O(n)     │ Try all cut positions             │
└──────────────────────────┴──────────────────┴──────────┴──────────┴───────────────────────────────────┘
```

### The Golden Rule of Loop Direction

```
╔══════════════════════════════════════════════════════════════════╗
║  0/1 Knapsack (each item once):                                  ║
║     for w in range(W, weight-1, -1):   ← RIGHT TO LEFT          ║
║     Ensures dp[w-wt] is from previous item's row                ║
║                                                                  ║
║  Unbounded Knapsack (each item unlimited):                       ║
║     for w in range(weight, W+1):        ← LEFT TO RIGHT         ║
║     Allows dp[w-wt] to include current item again               ║
╚══════════════════════════════════════════════════════════════════╝
```
