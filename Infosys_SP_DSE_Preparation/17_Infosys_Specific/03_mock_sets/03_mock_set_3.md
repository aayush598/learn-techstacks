# Infosys SP DSE - Mock Test 3 (3 Hours)

> 3 questions: Easy (25 min) + Medium (50 min) + Hard (90 min)

---

## Question 1: Valid Palindrome After Removing One Character (Easy - 25 minutes)

### Problem Statement

Given a string `s`, check if it can be a palindrome after removing at most one character.

### Visual Problem Understanding

```
String: "abca"

Two pointers from both ends:
  a  b  c  a
  L        R
  a == a ✓ → move both inward
  
  a  b  c  a
     L  R
  b != c ✗ → MISMATCH!
  
  Option 1: Skip L → check "bca" → b≠a → NOT palindrome
  Option 2: Skip R → check "abc" → a≠c → NOT palindrome
  
  Wait, that's wrong... Let me re-trace:
  
  Option 1: Remove L (skip 'b') → check "ca" → c≠a → NO
  Option 2: Remove R (skip 'c') → check "ba" → b≠a → NO
  
  Hmm, but "abca" can become "aca" by removing 'b' at index 1!
  That IS a palindrome!
  
  The issue: we should check if the SUBSTRING is palindrome:
  After removing index 1 ('b'): "aca" → YES palindrome ✅
  After removing index 2 ('c'): "aba" → YES palindrome ✅

DECISION FLOW:
┌─────────────────────────────────────────────────────┐
│  L and R match? → move both inward                 │
│  L and R DON'T match?                             │
│    → Try removing L (check if L+1..R is palindrome)│
│    → Try removing R (check if L..R-1 is palindrome)│
│    → If NEITHER works → return False               │
└─────────────────────────────────────────────────────┘

"deeee": 
  d  e  e  e  e
  L           R
  d != e ✗ → Try removing 'd' → check "eeee" → palindrome ✅
           → OR remove last 'e' → check "deee" → d≠e → NO
  At least one works → True ✅
```

### Complexity Analysis

```python
def valid_palindrome(s):
    def is_palindrome(s, left, right):
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return is_palindrome(s, left + 1, right) or is_palindrome(s, left, right - 1)
        left += 1
        right -= 1
    return True

s = input().strip()
print(valid_palindrome(s))
```

### Approach 2: Count Mismatches

```python
def valid_palindrome_count(s):
    mismatches = []
    left, right = 0, len(s) - 1

    while left < right:
        if s[left] != s[right]:
            mismatches.append((left, right))
        left += 1
        right -= 1

    if len(mismatches) == 0:
        return True
    if len(mismatches) > 1:
        return False

    left, right = mismatches[0]
    # Check if removing left or right char makes it palindrome
    return (s[left + 1:right + 1] == s[left + 1:right + 1][::-1] or
            s[left:right] == s[left:right][::-1])

s = input().strip()
print(valid_palindrome_count(s))
```

### Approach 3: Recursive with Removal Count

```python
def valid_palindrome_recursive(s):
    def check(left, right, removals):
        while left < right:
            if s[left] != s[right]:
                if removals == 0:
                    return False
                return check(left + 1, right, 0) or check(left, right - 1, 0)
            left += 1
            right -= 1
        return True

    return check(0, len(s) - 1, 1)

s = input().strip()
print(valid_palindrome_recursive(s))
```

### Complexity Analysis
- **Approach 1:** O(n) time, O(1) space — Optimal
- **Approach 2:** O(n) time, O(n) space
- **Approach 3:** O(n) time, O(n) stack space

### Tips
- At most one removal means at most one mismatch is allowed
- This is one of the most frequently asked Infosys questions
- Also practice: Longest Palindromic Substring

---

## Question 2: Coin Change - Number of Ways (Medium - 50 minutes)

### Problem Statement

Given a set of coin denominations and a target amount, find the number of distinct ways to make the amount using the given coins. You can use unlimited coins of each type.

### Visual: DP Table Construction

```
coins = [1, 2, 5], amount = 5

DP Table: dp[coin][amount] = number of ways using coins up to index

     ""  1  2  3  4  5     ← Amount
  ""  1  0  0  0  0  0     ← Base: 1 way to make amount 0 (use no coins)
   1  1  1  1  1  1  1     ← Using only [1]: 1 way for each amount
   2  1  1  2  2  3  3     ← Using [1,2]: more combinations
   5  1  1  2  2  3  4     ← Using [1,2,5]: final answer = 4

FILL RULE:
  dp[i][j] = dp[i-1][j] + dp[i][j-coins[i-1]]
              ↑ don't use  ↑ use at least one
  
  Example: dp[2][3] = dp[1][3] + dp[2][1] = 1 + 1 = 2
           (ways without 2) + (ways using at least one 2)

WAYS TO MAKE 5:
  {1,1,1,1,1}
  {1,1,1,2}
  {1,2,2}
  {5}
  Total = 4 ✅

CRITICAL: Loop order matters!
  coins in outer loop → counts COMBINATIONS (what we want)
  amount in outer loop → counts PERMUTATIONS (wrong!)
```

### 1D Space Optimization Visual

```
1D DP: dp[amount] = number of ways

Initial: dp = [1, 0, 0, 0, 0, 0]

After coin=1:  dp = [1, 1, 1, 1, 1, 1]
                ↑ for each amount j: dp[j] += dp[j-1]

After coin=2:  dp = [1, 1, 2, 2, 3, 3]
                ↑ for each amount j: dp[j] += dp[j-2]

After coin=5:  dp = [1, 1, 2, 2, 3, 4]
                ↑ for each amount j: dp[j] += dp[j-5]

dp[5] = 4 ✅
```

### Complexity Analysis

```python
def count_ways_2d(coins, amount):
    MOD = 10**9 + 7
    n = len(coins)
    dp = [[0] * (amount + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = 1

    for i in range(1, n + 1):
        for j in range(1, amount + 1):
            dp[i][j] = dp[i - 1][j]
            if coins[i - 1] <= j:
                dp[i][j] = (dp[i][j] + dp[i][j - coins[i - 1]]) % MOD

    return dp[n][amount]

n, amount = map(int, input().split())
coins = list(map(int, input().split()))
print(count_ways_2d(coins, amount))
```

### Approach 2: 1D DP (Space Optimized)

```python
def count_ways_1d(coins, amount):
    MOD = 10**9 + 7
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for j in range(coin, amount + 1):
            dp[j] = (dp[j] + dp[j - coin]) % MOD

    return dp[amount]

n, amount = map(int, input().split())
coins = list(map(int, input().split()))
print(count_ways_1d(coins, amount))
```

### Approach 3: Recursive + Memoization

```python
from functools import lru_cache

def count_ways_memo(coins, amount):
    MOD = 10**9 + 7

    @lru_cache(maxsize=None)
    def ways(idx, remaining):
        if remaining == 0:
            return 1
        if idx >= len(coins) or remaining < 0:
            return 0

        include = ways(idx, remaining - coins[idx]) if coins[idx] <= remaining else 0
        exclude = ways(idx + 1, remaining)

        return (include + exclude) % MOD

    return ways(0, amount)

n, amount = map(int, input().split())
coins = list(map(int, input().split()))
print(count_ways_memo(coins, amount))
```

### Complexity Analysis
- **Approach 1:** O(N * amount) time, O(N * amount) space
- **Approach 2:** O(N * amount) time, O(amount) space — Optimal
- **Approach 3:** O(N * amount) time, O(N * amount) space

### Tips
- Important: iterate coins in outer loop to avoid counting permutations
- The order of loops matters: coins first gives combinations, amount first gives permutations
- Modulo operation is important for large outputs
- Also practice: Minimum coins to make amount

---

## Question 3: Burst Balloons - Interval DP (Hard - 90 minutes)

### Problem Statement

Given `n` balloons indexed from 0 to n-1, each with a number on it represented by array `nums`. You are asked to burst all the balloons. If you burst balloon `i`, you will get `nums[i-1] * nums[i] * nums[i+1]` coins. If `i-1` or `i+1` goes out of bounds, treat it as 1. Find the maximum coins you can collect by bursting all balloons optimally.

### Visual: Why "Last Balloon" Strategy?

```
nums = [3, 1, 5, 8]
Add virtual balloons: [1, 3, 1, 5, 8, 1]
                       ↑                 ↑
                    virtual (value=1)

WHY THINK "LAST" NOT "FIRST"?
  If we think "first balloon to burst", the choice affects
  neighbors for future bursts - hard to track!
  
  If we think "LAST balloon to burst in range [L,R]":
  → When it's the last, its neighbors are ALREADY BURST
  → So its neighbors are the VIRTUAL balloons at L-1 and R+1!
  → Score = nums[L-1] * nums[k] * nums[R+1]

INTERVAL DP VISUAL:
  For range [L=1, R=4] (balloons 3,1,5,8):
  
  Try each as LAST:
  ┌─────┬───────────────────────────────┬────────────────┐
  │ Last │ Left part  │ Right part      │ Score          │
  ├─────┼────────────┼─────────────────┼────────────────┤
  │  k=1 │ [empty]=0  │ [5,8] (best)   │ 1*3*1 + 0+best│
  │  k=2 │ [3] (best) │ [5,8] (best)   │ 1*1*1 + best  │
  │  k=3 │ [3,1](best)│ [8] (best)     │ 1*5*1 + best  │
  │  k=4 │ [3,1,5](b) │ [empty]=0      │ 1*8*1 + best  │
  └─────┴────────────┴─────────────────┴────────────────┘

DP TABLE CONSTRUCTION (increasing length):
  Length 1: dp[i][i] = nums[i-1]*nums[i]*nums[i+1]
  Length 2: dp[i][i+1] = max over all k in [i,i+1]
  ...
  Length n: dp[1][n] = final answer
```

### Complexity Analysis

```python
def max_coins(nums):
    n = len(nums)
    # Add virtual balloons at boundaries
    nums = [1] + nums + [1]

    # dp[i][j] = max coins from bursting balloons between i and j (exclusive)
    dp = [[0] * (n + 2) for _ in range(n + 2)]

    # Process intervals of increasing length
    for length in range(1, n + 1):
        for left in range(1, n - length + 2):
            right = left + length - 1

            # Try each balloon as the last one to burst
            for k in range(left, right + 1):
                # k is the last balloon to burst in range [left, right]
                coins = nums[left - 1] * nums[k] * nums[right + 1]
                dp[left][right] = max(dp[left][right],
                                       dp[left][k - 1] + dp[k + 1][right] + coins)

    return dp[1][n]

def main():
    n = int(input())
    nums = list(map(int, input().split()))
    print(max_coins(nums))

main()
```

### Approach 2: Recursive + Memoization

```python
from functools import lru_cache

def max_coins_memo(nums):
    nums = [1] + nums + [1]
    n = len(nums)

    @lru_cache(maxsize=None)
    def solve(left, right):
        if left > right:
            return 0

        max_coins = 0
        for k in range(left, right + 1):
            coins = nums[left - 1] * nums[k] * nums[right + 1]
            max_coins = max(max_coins,
                           solve(left, k - 1) + solve(k + 1, right) + coins)

        return max_coins

    return solve(1, len(nums) - 2)

def main():
    n = int(input())
    nums = list(map(int, input().split()))
    print(max_coins_memo(nums))

main()
```

### Approach 3: Top-Down DP with 2D Array

```python
def max_coins_topdown(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    memo = [[-1] * (n + 2) for _ in range(n + 2)]

    def solve(left, right):
        if left > right:
            return 0
        if memo[left][right] != -1:
            return memo[left][right]

        result = 0
        for k in range(left, right + 1):
            coins = nums[left - 1] * nums[k] * nums[right + 1]
            result = max(result, solve(left, k - 1) + solve(k + 1, right) + coins)

        memo[left][right] = result
        return result

    return solve(1, len(nums) - 2)

def main():
    n = int(input())
    nums = list(map(int, input().split()))
    print(max_coins_topdown(nums))

main()
```

### Complexity Analysis
- **Approach 1:** O(n^3) time, O(n^2) space — Optimal
- **Approach 2:** O(n^3) time, O(n^2) space (memoization overhead)
- **Approach 3:** O(n^3) time, O(n^2) space

### Tips
- Key insight: think of it as which balloon to burst LAST in a range
- Adding virtual balloons at boundaries (value 1) simplifies edge cases
- This is a classic interval DP problem - understand the recurrence relation
- For n up to 300, O(n^3) is acceptable (27 million operations)

---

## Time Management Guide

| Question | Time | Target |
|----------|------|--------|
| Q1 (Easy) | 25 min | Quick solve + test |
| Q2 (Medium) | 50 min | Implement + optimize |
| Q3 (Hard) | 90 min | Plan DP + implement |
| Buffer | 15 min | Final review |

### Strategy
1. Q1 is straightforward - two pointers solve it
2. Q2 has multiple approaches - choose the one you're comfortable with
3. Q3 requires careful thinking about the DP state
4. Draw the recurrence on paper before coding
5. Test with sample cases before submitting

### Common Patterns in Infosys SP L3
- Palindrome variants are very common
- Coin change variants test DP understanding
- Interval DP (like Burst Balloons) differentiates top candidates
- Always mention time and space complexity

### Edge Cases to Test
- Q1: Empty string, single character, already palindrome
- Q2: Amount = 0, no valid combination, large coins
- Q3: Single balloon, all same values, sorted array
