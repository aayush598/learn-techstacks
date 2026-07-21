# Dynamic Programming Problems - Batch 2 (60 Problems)
## Infosys SP DSE Preparation - DP Mastery
### DP is the GATE for SP L2/L3. Master every pattern here.

---

## Table of Contents
1. [EASY (10 Problems)](#easy)
2. [MEDIUM (30 Problems)](#medium)
3. [HARD (20 Problems)](#hard)

---

<a id="easy"></a>
## EASY (10 Problems)

---

### Problem 1: Min Cost Climbing Stairs

**Problem Statement:**
You are climbing a staircase with `n` steps. Each step `i` has a cost `cost[i]`. You can start from step 0 or step 1. After paying the cost, you can climb one or two steps. Find the minimum cost to reach the top (past the last step).

**Example:**
```
Input: cost = [10, 15, 20]
Output: 15
Explanation: Start at index 1 (cost 15), climb to top.
```

**State Definition:**
- `dp[i]` = minimum cost to reach step `i`

**Recurrence Relation:**
- `dp[i] = cost[i] + min(dp[i-1], dp[i-2])`

**Base Case:**
- `dp[0] = cost[0]`
- `dp[1] = cost[1]`

**Python Code (Tabulation):**
```python
def minCostClimbingStairs(cost):
    n = len(cost)
    if n == 1:
        return cost[0]
    if n == 2:
        return min(cost[0], cost[1])
    
    dp = [0] * n
    dp[0] = cost[0]
    dp[1] = cost[1]
    
    for i in range(2, n):
        dp[i] = cost[i] + min(dp[i-1], dp[i-2])
    
    return min(dp[n-1], dp[n-2])

# Space optimized
def minCostClimbingStairsOptimized(cost):
    n = len(cost)
    if n == 1:
        return cost[0]
    if n == 2:
        return min(cost[0], cost[1])
    
    prev2 = cost[0]
    prev1 = cost[1]
    
    for i in range(2, n):
        curr = cost[i] + min(prev1, prev2)
        prev2 = prev1
        prev1 = curr
    
    return min(prev1, prev2)
```

**Complexity:**
- Time: O(n)
- Space: O(n) tabulation, O(1) optimized

**Trick/Tip:** We can start from step 0 or 1, so the answer is `min(dp[n-1], dp[n-2])` since from the last two steps we can always reach the top.

---

### Problem 2: Range Sum Query - Immutable

**Problem Statement:**
Design a data structure to compute the sum of elements between indices `left` and `right` (inclusive) where `0 <= left <= right < n`. Multiple queries are made.

**Example:**
```
Input: nums = [-2, 0, 3, -5, 2, -1]
sumRange(0, 2) -> 1
sumRange(2, 5) -> -1
```

**State Definition:**
- `dp[i]` = sum of all elements from index 0 to i-1 (prefix sum)

**Recurrence Relation:**
- `dp[i] = dp[i-1] + nums[i-1]`

**Base Case:**
- `dp[0] = 0`

**Python Code (Tabulation):**
```python
class NumArray:
    def __init__(self, nums):
        self.n = len(nums)
        self.dp = [0] * (self.n + 1)
        for i in range(1, self.n + 1):
            self.dp[i] = self.dp[i-1] + nums[i-1]
    
    def sumRange(self, left, right):
        return self.dp[right + 1] - self.dp[left]

# Alternative with prefix array
class NumArray2:
    def __init__(self, nums):
        self.prefix = [0] * (len(nums) + 1)
        for i in range(len(nums)):
            self.prefix[i+1] = self.prefix[i] + nums[i]
    
    def sumRange(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]
```

**Complexity:**
- Preprocessing: O(n)
- Query: O(1)
- Space: O(n)

**Trick/Tip:** Prefix sum is fundamental. `sum(i..j) = prefix[j+1] - prefix[i]`.

---

### Problem 3: Is Subsequence

**Problem Statement:**
Given strings `s` and `t`, return `True` if `s` is a subsequence of `t`, or `False` otherwise.

**Example:**
```
Input: s = "abc", t = "ahbgdc"
Output: True
```

**State Definition:**
- `dp[i][j]` = True if `s[0..i-1]` is a subsequence of `t[0..j-1]`

**Recurrence Relation:**
- If `s[i-1] == t[j-1]`: `dp[i][j] = dp[i-1][j-1]`
- Else: `dp[i][j] = dp[i][j-1]`

**Base Case:**
- `dp[0][j] = True` for all j
- `dp[i][0] = False` for i > 0

**Python Code (Tabulation):**
```python
def isSubsequence(s, t):
    m, n = len(s), len(t)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    
    for j in range(n + 1):
        dp[0][j] = True
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = dp[i][j-1]
    
    return dp[m][n]

# Two pointer approach (more efficient for this problem)
def isSubsequenceTwoPointer(s, t):
    i, j = 0, 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1
        j += 1
    return i == len(s)
```

**Complexity:**
- DP: O(m * n) time, O(m * n) space
- Two pointer: O(n) time, O(1) space

**Trick/Tip:** Two pointer is optimal here. DP is useful when there are multiple queries with the same `t`.

---

### Problem 4: Maximum Ascending Subarray Sum

**Problem Statement:**
Given an array of positive integers, find the maximum sum of a strictly ascending subarray (contiguous).

**Example:**
```
Input: nums = [10, 20, 30, 5, 10, 50]
Output: 65
Explanation: [5, 10, 50] has the maximum sum
```

**State Definition:**
- `dp[i]` = maximum sum of ascending subarray ending at index `i`

**Recurrence Relation:**
- If `nums[i] > nums[i-1]`: `dp[i] = dp[i-1] + nums[i]`
- Else: `dp[i] = nums[i]`

**Base Case:**
- `dp[0] = nums[0]`

**Python Code (Tabulation):**
```python
def maxAscendingSum(nums):
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    result = nums[0]
    
    for i in range(1, n):
        if nums[i] > nums[i-1]:
            dp[i] = dp[i-1] + nums[i]
        else:
            dp[i] = nums[i]
        result = max(result, dp[i])
    
    return result

# Space optimized
def maxAscendingSumOptimized(nums):
    curr_sum = nums[0]
    max_sum = nums[0]
    
    for i in range(1, len(nums)):
        if nums[i] > nums[i-1]:
            curr_sum += nums[i]
        else:
            curr_sum = nums[i]
        max_sum = max(max_sum, curr_sum)
    
    return max_sum
```

**Complexity:**
- Time: O(n)
- Space: O(1) optimized

**Trick/Tip:** Similar to Kadane's algorithm but for ascending subarrays specifically.

---

### Problem 5: Counting Bits

**Problem Statement:**
Given an integer `n`, return an array of length `n + 1` where `ans[i]` is the number of 1's in the binary representation of `i`.

**Example:**
```
Input: n = 5
Output: [0, 1, 1, 2, 1, 2]
```

**State Definition:**
- `dp[i]` = number of set bits in binary representation of `i`

**Recurrence Relation:**
- `dp[i] = dp[i >> 1] + (i & 1)`

**Base Case:**
- `dp[0] = 0`

**Python Code (Tabulation):**
```python
def countBits(n):
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    
    return dp

# Alternative: using Brian Kernighan's algorithm
def countBitsKernighan(n):
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1):
        dp[i] = dp[i & (i - 1)] + 1
    
    return dp
```

**Complexity:**
- Time: O(n)
- Space: O(n)

**Trick/Tip:** `i >> 1` gives the number with the last bit removed. Adding `i & 1` gives the count for `i`.

---

### Problem 6: XOR Subarrays

**Problem Statement:**
Given an integer array `arr` and an integer `k`, return the number of non-empty subarrays that have a bitwise XOR equal to `k`.

**Example:**
```
Input: arr = [4, 2, 2, 6, 4], k = 6
Output: 4
```

**State Definition:**
- `prefix_xor` = running XOR of elements
- Hash map to count prefix XOR occurrences

**Recurrence Relation:**
- If `prefix_xor ^ k` exists in hash map, add its count to result

**Base Case:**
- `prefix_map[0] = 1` (empty prefix)

**Python Code (DP with Hash):**
```python
from collections import defaultdict

def xorSubarrays(arr, k):
    prefix_xor = 0
    count = 0
    prefix_map = defaultdict(int)
    prefix_map[0] = 1
    
    for num in arr:
        prefix_xor ^= num
        target = prefix_xor ^ k
        if target in prefix_map:
            count += prefix_map[target]
        prefix_map[prefix_xor] += 1
    
    return count
```

**Complexity:**
- Time: O(n)
- Space: O(n)

**Trick/Tip:** Key insight: if `prefix[j] ^ prefix[i-1] = k`, then subarray `i..j` has XOR = k. So we look for `prefix[i-1] = prefix[j] ^ k`.

---

### Problem 7: Can Place Flowers

**Problem Statement:**
You have a flowerbed (array of 0s and 1s) and `n` new flowers to plant. No two flowers can be adjacent. Return `True` if you can plant all `n` flowers.

**Example:**
```
Input: flowerbed = [1, 0, 0, 0, 1], n = 1
Output: True
```

**State Definition:**
- Greedy: count maximum flowers that can be planted

**Recurrence Relation:**
- Plant at position `i` if `flowerbed[i] == 0` and neighbors are 0

**Base Case:**
- If `n == 0`, return True

**Python Code (Greedy/DP):**
```python
def canPlaceFlowers(flowerbed, n):
    m = len(flowerbed)
    if n == 0:
        return True
    
    count = 0
    for i in range(m):
        if flowerbed[i] == 0:
            left_ok = (i == 0) or (flowerbed[i-1] == 0)
            right_ok = (i == m-1) or (flowerbed[i+1] == 0)
            if left_ok and right_ok:
                flowerbed[i] = 1
                count += 1
                if count >= n:
                    return True
    return count >= n

# True DP approach
def canPlaceFlowersDP(flowerbed, n):
    m = len(flowerbed)
    dp = [[0] * 2 for _ in range(m + 1)]
    # dp[i][0] = max flowers without planting i-th
    # dp[i][1] = max flowers planting i-th
    
    dp[0][0] = 0
    dp[0][1] = 0
    
    for i in range(1, m + 1):
        dp[i][0] = max(dp[i-1][0], dp[i-1][1])
        if flowerbed[i-1] == 0:
            dp[i][1] = dp[i-1][0] + 1
        else:
            dp[i][1] = 0
    
    return max(dp[m][0], dp[m][1]) >= n
```

**Complexity:**
- Time: O(m)
- Space: O(1) greedy, O(m) DP

**Trick/Tip:** Greedy works perfectly here. When you can plant, plant immediately - it's always optimal.

---

### Problem 8: House Robber

**Problem Statement:**
You are a robber planning to rob houses along a street. Each house has a certain amount of money. You cannot rob two adjacent houses. Find the maximum amount you can rob.

**Example:**
```
Input: nums = [1, 2, 3, 1]
Output: 4
Explanation: Rob house 1 (money=1) and house 3 (money=3) = 4
```

**State Definition:**
- `dp[i]` = maximum money that can be robbed from first `i` houses

**Recurrence Relation:**
- `dp[i] = max(dp[i-1], dp[i-2] + nums[i-1])`

**Base Case:**
- `dp[0] = 0`
- `dp[1] = nums[0]`

**Python Code (Tabulation):**
```python
def rob(nums):
    n = len(nums)
    if n == 1:
        return nums[0]
    if n == 2:
        return max(nums[0], nums[1])
    
    dp = [0] * (n + 1)
    dp[1] = nums[0]
    dp[2] = max(nums[0], nums[1])
    
    for i in range(3, n + 1):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i-1])
    
    return dp[n]

# Space optimized
def robOptimized(nums):
    n = len(nums)
    if n == 1:
        return nums[0]
    if n == 2:
        return max(nums[0], nums[1])
    
    prev2 = nums[0]
    prev1 = max(nums[0], nums[1])
    
    for i in range(2, n):
        curr = max(prev1, prev2 + nums[i])
        prev2 = prev1
        prev1 = curr
    
    return prev1
```

**Complexity:**
- Time: O(n)
- Space: O(1) optimized

**Trick/Tip:** Classic 1D DP. The recurrence `max(skip, take)` pattern appears in many problems.

---

### Problem 9: Fibonacci Number

**Problem Statement:**
Calculate the nth Fibonacci number where F(0) = 0, F(1) = 1, and F(n) = F(n-1) + F(n-2) for n > 1.

**Example:**
```
Input: n = 4
Output: 3
```

**State Definition:**
- `dp[i]` = the ith Fibonacci number

**Recurrence Relation:**
- `dp[i] = dp[i-1] + dp[i-2]`

**Base Case:**
- `dp[0] = 0`
- `dp[1] = 1`

**Python Code (Multiple Approaches):**
```python
def fib(n):
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]

# Space optimized
def fibOptimized(n):
    if n <= 1:
        return n
    
    prev2 = 0
    prev1 = 1
    
    for i in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    
    return prev1

# With memoization
def fibMemo(n):
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def helper(i):
        if i <= 1:
            return i
        return helper(i-1) + helper(i-2)
    
    return helper(n)

# Matrix exponentiation (O(log n))
def fibMatrix(n):
    def matrix_mult(A, B):
        return [
            [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
            [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
        ]
    
    def matrix_pow(M, p):
        result = [[1, 0], [0, 1]]
        while p:
            if p & 1:
                result = matrix_mult(result, M)
            M = matrix_mult(M, M)
            p >>= 1
        return result
    
    if n <= 1:
        return n
    
    M = [[1, 1], [1, 0]]
    result = matrix_pow(M, n)
    return result[0][1]
```

**Complexity:**
- Tabulation/Iterative: O(n) time, O(1) space
- Matrix: O(log n) time, O(1) space

**Trick/Tip:** Fibonacci is the foundation of many DP problems. The iterative approach with two variables is the standard pattern.

---

### Problem 10: Tribonacci Number

**Problem Statement:**
The Tribonacci sequence T(n) is defined as:
- T(0) = 0, T(1) = 1, T(2) = 1
- T(n) = T(n-1) + T(n-2) + T(n-3) for n >= 3

**Example:**
```
Input: n = 4
Output: 4
```

**State Definition:**
- `dp[i]` = the ith Tribonacci number

**Recurrence Relation:**
- `dp[i] = dp[i-1] + dp[i-2] + dp[i-3]`

**Base Case:**
- `dp[0] = 0`, `dp[1] = 1`, `dp[2] = 1`

**Python Code (Tabulation):**
```python
def tribonacci(n):
    if n == 0:
        return 0
    if n <= 2:
        return 1
    
    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1
    dp[2] = 1
    
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2] + dp[i-3]
    
    return dp[n]

# Space optimized
def tribonacciOptimized(n):
    if n == 0:
        return 0
    if n <= 2:
        return 1
    
    prev3, prev2, prev1 = 0, 1, 1
    
    for i in range(3, n + 1):
        curr = prev1 + prev2 + prev3
        prev3 = prev2
        prev2 = prev1
        prev1 = curr
    
    return prev1
```

**Complexity:**
- Time: O(n)
- Space: O(1) optimized, O(n) with memoization

**Trick/Tip:** Same pattern as Fibonacci but with 3 previous values. For k-step generalized versions, use a sliding window of k values.

---
<a id="medium"></a>
## MEDIUM (30 Problems)

---

### Problem 11: Longest Palindromic Subsequence

**Problem Statement:**
Given a string `s`, find the length of the longest palindromic subsequence.

**Example:**
```
Input: s = "bbbab"
Output: 4
```

**State Definition:**
- `dp[i][j]` = length of longest palindromic subsequence in `s[i..j]`

**Recurrence Relation:**
- If `s[i] == s[j]`: `dp[i][j] = dp[i+1][j-1] + 2`
- Else: `dp[i][j] = max(dp[i+1][j], dp[i][j-1])`

**Base Case:**
- `dp[i][i] = 1`
- `dp[i][j] = 0` when `i > j`

**Python Code (Tabulation):**
```python
def longestPalindromeSubseq(s):
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

# Using LCS: LPS(s) = LCS(s, reverse(s))
def longestPalindromeSubseqLCS(s):
    def lcs(s1, s2):
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return dp[m][n]
    return lcs(s, s[::-1])
```

**Complexity:**
- Time: O(n^2)
- Space: O(n^2)

**Trick/Tip:** LPS of string = LCS of string and its reverse.

---

### Problem 12: Longest Common Subsequence (LCS)

**Problem Statement:**
Given two strings `text1` and `text2`, return the length of their longest common subsequence.

**Example:**
```
Input: text1 = "abcde", text2 = "ace"
Output: 3
```

**State Definition:**
- `dp[i][j]` = length of LCS of `text1[0..i-1]` and `text2[0..j-1]`

**Recurrence Relation:**
- If `text1[i-1] == text2[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`
- Else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

**Base Case:**
- `dp[0][j] = 0`, `dp[i][0] = 0`

**Python Code (Tabulation):**
```python
def longestCommonSubsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]

# With path reconstruction
def lcsWithPath(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    i, j = m, n
    lcs_str = []
    while i > 0 and j > 0:
        if text1[i-1] == text2[j-1]:
            lcs_str.append(text1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    return dp[m][n], ''.join(reversed(lcs_str))

# Space optimized
def lcsOptimized(text1, text2):
    m, n = len(text1), len(text2)
    if m < n:
        text1, text2 = text2, text1
        m, n = n, m
    
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(prev[j], curr[j-1])
        prev, curr = curr, [0] * (n + 1)
    
    return prev[n]
```

**Complexity:**
- Time: O(m * n)
- Space: O(m * n) tabulation, O(min(m, n)) optimized

**Trick/Tip:** LCS is the most fundamental string DP problem. Many other problems reduce to LCS.

---

### Problem 13: Edit Distance

**Problem Statement:**
Given two strings `word1` and `word2`, return the minimum number of operations (insert, delete, replace) required to convert `word1` to `word2`.

**Example:**
```
Input: word1 = "horse", word2 = "ros"
Output: 3
```

**State Definition:**
- `dp[i][j]` = minimum operations to convert `word1[0..i-1]` to `word2[0..j-1]`

**Recurrence Relation:**
- If `word1[i-1] == word2[j-1]`: `dp[i][j] = dp[i-1][j-1]`
- Else: `dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`

**Base Case:**
- `dp[i][0] = i` (delete all)
- `dp[0][j] = j` (insert all)

**Python Code (Tabulation):**
```python
def minDistance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    return dp[m][n]

# Space optimized
def minDistanceOptimized(word1, word2):
    m, n = len(word1), len(word2)
    if m < n:
        word1, word2 = word2, word1
        m, n = n, m
    
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                curr[j] = prev[j-1]
            else:
                curr[j] = 1 + min(prev[j], curr[j-1], prev[j-1])
        prev = curr[:]
    
    return prev[n]
```

**Complexity:**
- Time: O(m * n)
- Space: O(m * n) tabulation, O(min(m, n)) optimized

**Trick/Tip:** The three operations map to: delete (dp[i-1][j]+1), insert (dp[i][j-1]+1), replace (dp[i-1][j-1]+1).

---

### Problem 14: Distinct Subsequences

**Problem Statement:**
Given two strings `s` and `t`, return the number of distinct subsequences of `s` which equal `t`.

**Example:**
```
Input: s = "rabbbit", t = "rabbit"
Output: 3
```

**State Definition:**
- `dp[i][j]` = number of distinct subsequences of `s[0..i-1]` that equal `t[0..j-1]`

**Recurrence Relation:**
- If `s[i-1] == t[j-1]`: `dp[i][j] = dp[i-1][j-1] + dp[i-1][j]`
- Else: `dp[i][j] = dp[i-1][j]`

**Base Case:**
- `dp[i][0] = 1`
- `dp[0][j] = 0` for j > 0

**Python Code (Tabulation):**
```python
def numDistinct(s, t):
    m, n = len(s), len(t)
    if n > m:
        return 0
    
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = 1
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
            else:
                dp[i][j] = dp[i-1][j]
    
    return dp[m][n]

# Space optimized
def numDistinctOptimized(s, t):
    m, n = len(s), len(t)
    if n > m:
        return 0
    
    prev = [0] * (n + 1)
    prev[0] = 1
    
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        curr[0] = 1
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                curr[j] = prev[j-1] + prev[j]
            else:
                curr[j] = prev[j]
        prev = curr
    
    return prev[n]
```

**Complexity:**
- Time: O(m * n)
- Space: O(m * n) tabulation, O(n) optimized

**Trick/Tip:** When characters match, we have two choices: use this character (dp[i-1][j-1]) or skip it (dp[i-1][j]).

---

### Problem 15: Interleaving String

**Problem Statement:**
Given strings `s1`, `s2`, and `s3`, return `True` if `s3` is formed by interleaving `s1` and `s2`.

**Example:**
```
Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
Output: True
```

**State Definition:**
- `dp[i][j]` = True if `s3[0..i+j-1]` is formed by interleaving `s1[0..i-1]` and `s2[0..j-1]`

**Recurrence Relation:**
- `dp[i][j] = (dp[i-1][j] and s1[i-1] == s3[i+j-1]) or (dp[i][j-1] and s2[j-1] == s3[i+j-1])`

**Base Case:**
- `dp[0][0] = True`

**Python Code (Tabulation):**
```python
def isInterleave(s1, s2, s3):
    m, n = len(s1), len(s2)
    
    if m + n != len(s3):
        return False
    
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] and s1[i-1] == s3[i-1]
    
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] and s2[j-1] == s3[j-1]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = (dp[i-1][j] and s1[i-1] == s3[i+j-1]) or \
                       (dp[i][j-1] and s2[j-1] == s3[i+j-1])
    
    return dp[m][n]
```

**Complexity:**
- Time: O(m * n)
- Space: O(m * n)

**Trick/Tip:** At each position, check if current character of s3 matches either s1 or s2.

---

### Problem 16: Minimum ASCII Delete Sum for Two Strings

**Problem Statement:**
Given two strings `s1` and `s2`, return the lowest ASCII sum of deleted characters to make the two strings equal.

**Example:**
```
Input: s1 = "sea", s2 = "eat"
Output: 231
```

**State Definition:**
- `dp[i][j]` = minimum ASCII delete sum to make `s1[0..i-1]` and `s2[0..j-1]` equal

**Recurrence Relation:**
- If `s1[i-1] == s2[j-1]`: `dp[i][j] = dp[i-1][j-1]`
- Else: `dp[i][j] = min(dp[i-1][j] + ord(s1[i-1]), dp[i][j-1] + ord(s2[j-1]))`

**Base Case:**
- `dp[i][0] = sum of ASCII of s1[0..i-1]`
- `dp[0][j] = sum of ASCII of s2[0..j-1]`

**Python Code (Tabulation):**
```python
def minimumDeleteSum(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] + ord(s1[i-1])
    
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] + ord(s2[j-1])
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i-1][j] + ord(s1[i-1]),
                              dp[i][j-1] + ord(s2[j-1]))
    
    return dp[m][n]
```

**Complexity:**
- Time: O(m * n)
- Space: O(m * n)

**Trick/Tip:** When characters match, we don't delete anything. Otherwise, we must delete from one string.

---

### Problem 17: Longest Increasing Subsequence II

**Problem Statement:**
Given an integer array `nums` and an integer `k`, find the length of the longest subsequence such that the difference between adjacent elements is at most `k`.

**Example:**
```
Input: nums = [4, 2, 1, 4, 3, 4, 5, 8, 15], k = 5
Output: 5
```

**State Definition:**
- `dp[i]` = length of longest valid subsequence ending at index `i`

**Recurrence Relation:**
- `dp[i] = 1 + max(dp[j])` for all `j < i` where `abs(nums[i] - nums[j]) <= k`

**Base Case:**
- `dp[i] = 1` for all i

**Python Code (Tabulation):**
```python
def longestSubarray(nums, k):
    n = len(nums)
    dp = [1] * n
    result = 1
    
    for i in range(1, n):
        for j in range(i):
            if abs(nums[i] - nums[j]) <= k:
                dp[i] = max(dp[i], dp[j] + 1)
        result = max(result, dp[i])
    
    return result

# Optimized with segment tree for range max query
def longestSubarrayOptimized(nums, k):
    n = len(nums)
    dp = [1] * n
    result = 1
    
    sorted_nums = sorted(set(nums))
    rank = {v: i for i, v in enumerate(sorted_nums)}
    m = len(sorted_nums)
    
    tree = [0] * (4 * m)
    
    def update(node, start, end, idx, val):
        if start == end:
            tree[node] = max(tree[node], val)
            return
        mid = (start + end) // 2
        if idx <= mid:
            update(2*node, start, mid, idx, val)
        else:
            update(2*node+1, mid+1, end, idx, val)
        tree[node] = max(tree[2*node], tree[2*node+1])
    
    def query(node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return tree[node]
        mid = (start + end) // 2
        return max(query(2*node, start, mid, l, r),
                   query(2*node+1, mid+1, end, l, r))
    
    for i in range(n):
        r = rank[nums[i]]
        left, right = 0, m - 1
        while left < m and sorted_nums[left] < nums[i] - k:
            left += 1
        while right >= 0 and sorted_nums[right] > nums[i] + k:
            right -= 1
        
        if left <= right:
            dp[i] = 1 + query(1, 0, m-1, left, right)
        result = max(result, dp[i])
        update(1, 0, m-1, r, dp[i])
    
    return result
```

**Complexity:**
- Brute: O(n^2) time
- Optimized: O(n log n) time, O(n) space

**Trick/Tip:** Use segment tree for efficient range maximum queries.

---

### Problem 18: Longest Arithmetic Subsequence

**Problem Statement:**
Given an array `nums`, return the length of the longest arithmetic subsequence.

**Example:**
```
Input: nums = [3, 6, 9, 12]
Output: 4
```

**State Definition:**
- `dp[i][d]` = length of longest arithmetic subsequence ending at index `i` with common difference `d`

**Recurrence Relation:**
- `dp[i][d] = dp[j][d] + 1` for all `j < i` where `nums[i] - nums[j] = d`

**Base Case:**
- `dp[i][d] = 2` for any valid pair

**Python Code (Tabulation + Hash Map):**
```python
def longestArithSeqLength(nums):
    n = len(nums)
    if n <= 2:
        return n
    
    dp = [{} for _ in range(n)]
    result = 2
    
    for i in range(1, n):
        for j in range(i):
            diff = nums[i] - nums[j]
            if diff in dp[j]:
                dp[i][diff] = dp[j][diff] + 1
            else:
                dp[i][diff] = 2
            result = max(result, dp[i][diff])
    
    return result
```

**Complexity:**
- Time: O(n^2)
- Space: O(n^2)

**Trick/Tip:** Hash map at each index stores {difference: length} pairs.

---

### Problem 19: Arithmetic Slices

**Problem Statement:**
An arithmetic slice is a contiguous subarray with at least 3 elements where the difference is constant. Count the number of arithmetic slices.

**Example:**
```
Input: nums = [1, 2, 3, 4]
Output: 3
```

**State Definition:**
- `dp[i]` = number of arithmetic slices ending at index `i`

**Recurrence Relation:**
- If `nums[i] - nums[i-1] == nums[i-1] - nums[i-2]`: `dp[i] = dp[i-1] + 1`
- Else: `dp[i] = 0`

**Base Case:**
- `dp[0] = dp[1] = 0`

**Python Code (Tabulation):**
```python
def numberOfArithmeticSlices(nums):
    n = len(nums)
    if n < 3:
        return 0
    
    dp = [0] * n
    result = 0
    
    for i in range(2, n):
        if nums[i] - nums[i-1] == nums[i-1] - nums[i-2]:
            dp[i] = dp[i-1] + 1
            result += dp[i]
    
    return result

# Space optimized
def numberOfArithmeticSlicesOptimized(nums):
    n = len(nums)
    if n < 3:
        return 0
    
    curr = 0
    total = 0
    
    for i in range(2, n):
        if nums[i] - nums[i-1] == nums[i-1] - nums[i-2]:
            curr += 1
            total += curr
        else:
            curr = 0
    
    return total
```

**Complexity:**
- Time: O(n)
- Space: O(1) optimized

**Trick/Tip:** Each time we extend a valid slice, we add all new slices formed.

---

### Problem 20: Maximum Length of Subarray With Positive Product

**Problem Statement:**
Given an array `nums`, find the maximum length of a contiguous subarray with a positive product.

**Example:**
```
Input: nums = [1, -2, -3, 4]
Output: 4
```

**State Definition:**
- `pos[i]` = max length of subarray ending at `i` with positive product
- `neg[i]` = max length of subarray ending at `i` with negative product

**Recurrence Relation:**
- If `nums[i] > 0`: `pos[i] = pos[i-1] + 1`, `neg[i] = neg[i-1] + 1` if neg[i-1] > 0
- If `nums[i] < 0`: `pos[i] = neg[i-1] + 1` if neg[i-1] > 0, `neg[i] = pos[i-1] + 1`
- If `nums[i] == 0`: both 0

**Base Case:**
- `pos[0] = 1` if `nums[0] > 0`, `neg[0] = 1` if `nums[0] < 0`

**Python Code (Tabulation):**
```python
def getMaxLen(nums):
    n = len(nums)
    pos = [0] * n
    neg = [0] * n
    
    if nums[0] > 0:
        pos[0] = 1
    elif nums[0] < 0:
        neg[0] = 1
    
    result = pos[0]
    
    for i in range(1, n):
        if nums[i] > 0:
            pos[i] = pos[i-1] + 1
            neg[i] = neg[i-1] + 1 if neg[i-1] > 0 else 0
        elif nums[i] < 0:
            pos[i] = neg[i-1] + 1 if neg[i-1] > 0 else 0
            neg[i] = pos[i-1] + 1
        result = max(result, pos[i])
    
    return result

# Space optimized
def getMaxLenOptimized(nums):
    pos = neg = 0
    result = 0
    
    for num in nums:
        if num > 0:
            pos += 1
            neg = neg + 1 if neg > 0 else 0
        elif num < 0:
            pos, neg = neg + 1 if neg > 0 else 0, pos + 1
        else:
            pos = neg = 0
        result = max(result, pos)
    
    return result
```

**Complexity:**
- Time: O(n)
- Space: O(1) optimized

**Trick/Tip:** Track both positive and negative lengths. When we see a negative number, they swap.


---

### Problem 21: Maximum Product Subarray

**Problem Statement:**
Given an integer array `nums`, find a contiguous non-empty subarray that has the largest product.

**Example:**
```
Input: nums = [2, 3, -2, 4]
Output: 6
```

**State Definition:**
- `max_prod[i]` = maximum product of subarray ending at `i`
- `min_prod[i]` = minimum product of subarray ending at `i`

**Recurrence Relation:**
- `max_prod[i] = max(nums[i], max_prod[i-1] * nums[i], min_prod[i-1] * nums[i])`
- `min_prod[i] = min(nums[i], max_prod[i-1] * nums[i], min_prod[i-1] * nums[i])`

**Base Case:**
- `max_prod[0] = min_prod[0] = nums[0]`

**Python Code (Tabulation):**
```python
def maxProduct(nums):
    n = len(nums)
    max_prod = [0] * n
    min_prod = [0] * n
    
    max_prod[0] = min_prod[0] = nums[0]
    result = nums[0]
    
    for i in range(1, n):
        candidates = [nums[i], max_prod[i-1] * nums[i], min_prod[i-1] * nums[i]]
        max_prod[i] = max(candidates)
        min_prod[i] = min(candidates)
        result = max(result, max_prod[i])
    
    return result

# Space optimized
def maxProductOptimized(nums):
    max_prod = min_prod = result = nums[0]
    
    for i in range(1, len(nums)):
        candidates = [nums[i], max_prod * nums[i], min_prod * nums[i]]
        max_prod = max(candidates)
        min_prod = min(candidates)
        result = max(result, max_prod)
    
    return result
```

**Complexity:**
- Time: O(n)
- Space: O(1) optimized

**Trick/Tip:** Track both max and min because a negative number can turn min into max.

---

### Problem 22: Stone Game IV

**Problem Statement:**
Alice and Bob play a game with `n` stones. On each turn, remove a positive square number of stones. The player who cannot move loses. Return `True` if Alice wins.

**Example:**
```
Input: n = 1
Output: True
```

**State Definition:**
- `dp[i]` = True if current player can win with `i` stones

**Recurrence Relation:**
- `dp[i] = True` if there exists a square `s` such that `dp[i-s] == False`

**Base Case:**
- `dp[0] = False`

**Python Code (Tabulation):**
```python
def winnerSquareGame(n):
    dp = [False] * (n + 1)
    
    for i in range(1, n + 1):
        k = 1
        while k * k <= i:
            if not dp[i - k * k]:
                dp[i] = True
                break
            k += 1
    
    return dp[n]
```

**Complexity:**
- Time: O(n * sqrt(n))
- Space: O(n)

**Trick/Tip:** Game theory: a position is winning if you can move to a losing position.

---

### Problem 23: Longest String Chain

**Problem Statement:**
Given a list of words, find the longest word chain where each word differs from the previous by exactly one character (insertion).

**Example:**
```
Input: words = ["a","b","ba","bca","bda","bdca"]
Output: 4
```

**State Definition:**
- `dp[word]` = length of longest chain ending with `word`

**Recurrence Relation:**
- `dp[word] = max(dp[predecessor]) + 1` for all valid predecessors

**Base Case:**
- `dp[word] = 1` for all words

**Python Code (Tabulation + Sorting):**
```python
def longestStrChain(words):
    words.sort(key=len)
    dp = {}
    result = 1
    
    for word in words:
        dp[word] = 1
        for i in range(len(word)):
            predecessor = word[:i] + word[i+1:]
            if predecessor in dp:
                dp[word] = max(dp[word], dp[predecessor] + 1)
        result = max(result, dp[word])
    
    return result
```

**Complexity:**
- Time: O(n * L^2) where L is max word length
- Space: O(n)

**Trick/Tip:** Sort words by length. For each word, try removing each character and check if it exists.

---

### Problem 24: Minimum Path Sum in Triangular Grid

**Problem Statement:**
Given a triangle array, find the minimum path sum from top to bottom.

**Example:**
```
Input: triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
Output: 11
```

**State Definition:**
- `dp[i][j]` = minimum path sum to reach `triangle[i][j]`

**Recurrence Relation:**
- `dp[i][j] = triangle[i][j] + min(dp[i-1][j-1], dp[i-1][j])`

**Base Case:**
- `dp[0][0] = triangle[0][0]`

**Python Code (Tabulation):**
```python
def minimumTotal(triangle):
    n = len(triangle)
    dp = [[0] * (i + 1) for i in range(n)]
    dp[0][0] = triangle[0][0]
    
    for i in range(1, n):
        dp[i][0] = dp[i-1][0] + triangle[i][0]
        dp[i][i] = dp[i-1][i-1] + triangle[i][i]
        for j in range(1, i):
            dp[i][j] = triangle[i][j] + min(dp[i-1][j-1], dp[i-1][j])
    
    return min(dp[n-1])

# Space optimized (bottom-up)
def minimumTotalOptimized(triangle):
    n = len(triangle)
    dp = triangle[-1][:]
    
    for i in range(n - 2, -1, -1):
        for j in range(i + 1):
            dp[j] = triangle[i][j] + min(dp[j], dp[j+1])
    
    return dp[0]
```

**Complexity:**
- Time: O(n^2)
- Space: O(n) optimized

**Trick/Tip:** Bottom-up approach is elegant - start from last row and work up.

---

### Problem 25: Unique Binary Search Trees II

**Problem Statement:**
Given an integer `n`, return all structurally unique BSTs with exactly `n` nodes with values from 1 to n.

**Example:**
```
Input: n = 3
Output: 5 unique BSTs
```

**State Definition:**
- `generate(start, end)` = list of all unique BSTs from values `start` to `end`

**Recurrence Relation:**
- For each root `i` from `start` to `end`: left = `generate(start, i-1)`, right = `generate(i+1, end)`

**Base Case:**
- If `start > end`: return `[None]`

**Python Code (Recursion + Memoization):**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def generateTrees(n):
    def generate(start, end):
        if start > end:
            return [None]
        
        all_trees = []
        for root_val in range(start, end + 1):
            left_trees = generate(start, root_val - 1)
            right_trees = generate(root_val + 1, end)
            
            for left in left_trees:
                for right in right_trees:
                    root = TreeNode(root_val)
                    root.left = left
                    root.right = right
                    all_trees.append(root)
        
        return all_trees
    
    return generate(1, n) if n > 0 else []

# Count only (Catalan number)
def numTrees(n):
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    
    for nodes in range(2, n + 1):
        for root in range(1, nodes + 1):
            dp[nodes] += dp[root - 1] * dp[nodes - root]
    
    return dp[n]
```

**Complexity:**
- Time: O(n^2) for counting, O(n * 4^n / n^(3/2)) for generation
- Space: O(n) for counting

**Trick/Tip:** This is Catalan number. For each root, left and right subtrees are independent.

---

### Problem 26: Generate Parentheses (DP Approach)

**Problem Statement:**
Given `n` pairs of parentheses, generate all combinations of well-formed parentheses.

**Example:**
```
Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]
```

**State Definition:**
- `dp[i]` = list of all valid parentheses strings with `i` pairs

**Recurrence Relation:**
- For each `j` from 0 to i-1: `"(" + dp[j] + ")" + dp[i-1-j]`

**Base Case:**
- `dp[0] = [""]`

**Python Code (Tabulation):**
```python
def generateParenthesis(n):
    dp = [[] for _ in range(n + 1)]
    dp[0] = [""]
    
    for i in range(1, n + 1):
        for j in range(i):
            for left in dp[j]:
                for right in dp[i - 1 - j]:
                    dp[i].append("(" + left + ")" + right)
    
    return dp[n]

# Backtracking approach
def generateParenthesisBacktrack(n):
    result = []
    
    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(current)
            return
        if open_count < n:
            backtrack(current + "(", open_count + 1, close_count)
        if close_count < open_count:
            backtrack(current + ")", open_count, close_count + 1)
    
    backtrack("", 0, 0)
    return result
```

**Complexity:**
- Time: O(4^n / sqrt(n))
- Space: O(4^n / sqrt(n))

**Trick/Tip:** DP approach builds strings by combining smaller valid strings. The key insight is `(A)B` decomposition.

---

### Problem 27: Decode Ways II

**Problem Statement:**
A message is encoded using `1->A`, `2->B`, ..., `26->Z`. Given a string `s` with digits and `*` wildcards, return the number of ways to decode it.

**Example:**
```
Input: s = "1*"
Output: 18
```

**State Definition:**
- `dp[i]` = number of ways to decode `s[0..i-1]`

**Recurrence Relation:**
- Handle single digit and two-digit cases with wildcards

**Base Case:**
- `dp[0] = 1`

**Python Code (Tabulation):**
```python
def numDecodings(s):
    MOD = 10**9 + 7
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    
    for i in range(n):
        # 1-digit decode
        if s[i] == '*':
            dp[i+1] = (dp[i+1] + dp[i] * 9) % MOD
        elif s[i] != '0':
            dp[i+1] = (dp[i+1] + dp[i]) % MOD
        
        # 2-digit decode
        if i + 1 < n:
            if s[i] == '*' and s[i+1] == '*':
                dp[i+2] = (dp[i+2] + dp[i] * 15) % MOD
            elif s[i] == '*':
                if '0' <= s[i+1] <= '6':
                    dp[i+2] = (dp[i+2] + dp[i] * 2) % MOD
                else:
                    dp[i+2] = (dp[i+2] + dp[i]) % MOD
            elif s[i+1] == '*':
                if s[i] == '1':
                    dp[i+2] = (dp[i+2] + dp[i] * 9) % MOD
                elif s[i] == '2':
                    dp[i+2] = (dp[i+2] + dp[i] * 6) % MOD
            elif s[i] != '0' and 10 <= int(s[i:i+2]) <= 26:
                dp[i+2] = (dp[i+2] + dp[i]) % MOD
    
    return dp[n]
```

**Complexity:**
- Time: O(n)
- Space: O(n)

**Trick/Tip:** Handle wildcards carefully. `*` can represent 1-9 for single digit, and various ranges for two digits.

---

### Problem 28: Minimum Cost for Tickets

**Problem Statement:**
You are planning a trip on certain days. You can buy 1-day ($20), 7-day ($70), or 30-day ($150) passes. Find the minimum cost.

**Example:**
```
Input: days = [1, 4, 6, 7, 8, 20], costs = [2, 7, 15]
Output: 11
```

**State Definition:**
- `dp[i]` = minimum cost to cover travel days up to day `i`

**Recurrence Relation:**
- `dp[i] = min(dp[i-1] + costs[0], dp[max(0, i-7)] + costs[1], dp[max(0, i-30)] + costs[2])`

**Base Case:**
- `dp[0] = 0`

**Python Code (Tabulation):**
```python
def mincostTickets(days, costs):
    travel_days = set(days)
    last_day = days[-1]
    dp = [0] * (last_day + 1)
    
    for i in range(1, last_day + 1):
        if i not in travel_days:
            dp[i] = dp[i-1]
        else:
            dp[i] = min(
                dp[i-1] + costs[0],
                dp[max(0, i-7)] + costs[1],
                dp[max(0, i-30)] + costs[2]
            )
    
    return dp[last_day]
```

**Complexity:**
- Time: O(last_day)
- Space: O(last_day)

**Trick/Tip:** The set of travel days is sparse. You can optimize by only computing dp for days that matter.

---

### Problem 29: Longest Common Substring

**Problem Statement:**
Given two strings `s1` and `s2`, find the length of the longest common substring.

**Example:**
```
Input: s1 = "abcde", s2 = "abfce"
Output: 2
```

**State Definition:**
- `dp[i][j]` = length of longest common substring ending at `s1[i-1]` and `s2[j-1]`

**Recurrence Relation:**
- If `s1[i-1] == s2[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`
- Else: `dp[i][j] = 0`

**Base Case:**
- `dp[0][j] = 0`, `dp[i][0] = 0`

**Python Code (Tabulation):**
```python
def longestCommonSubstring(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    result = 0
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                result = max(result, dp[i][j])
    
    return result

# Space optimized
def longestCommonSubstringOptimized(s1, s2):
    m, n = len(s1), len(s2)
    prev = [0] * (n + 1)
    result = 0
    
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                curr[j] = prev[j-1] + 1
                result = max(result, curr[j])
        prev = curr
    
    return result
```

**Complexity:**
- Time: O(m * n)
- Space: O(m * n) tabulation, O(n) optimized

**Trick/Tip:** Unlike LCS, substring must be contiguous. When characters don't match, reset to 0.

---

### Problem 30: Maximum Length of Repeated Subarray

**Problem Statement:**
Given two integer arrays `nums1` and `nums2`, return the maximum length of a subarray that appears in both.

**Example:**
```
Input: nums1 = [1,2,3,2,1], nums2 = [3,2,1,4,7]
Output: 3
```

**State Definition:**
- `dp[i][j]` = length of longest common subarray ending at `nums1[i-1]` and `nums2[j-1]`

**Recurrence Relation:**
- If `nums1[i-1] == nums2[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`
- Else: `dp[i][j] = 0`

**Base Case:**
- `dp[0][j] = 0`, `dp[i][0] = 0`

**Python Code (Tabulation):**
```python
def findLength(nums1, nums2):
    m, n = len(nums1), len(nums2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    result = 0
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if nums1[i-1] == nums2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                result = max(result, dp[i][j])
    
    return result

# Space optimized
def findLengthOptimized(nums1, nums2):
    m, n = len(nums1), len(nums2)
    prev = [0] * (n + 1)
    result = 0
    
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if nums1[i-1] == nums2[j-1]:
                curr[j] = prev[j-1] + 1
                result = max(result, curr[j])
        prev = curr
    
    return result
```

**Complexity:**
- Time: O(m * n)
- Space: O(m * n) tabulation, O(n) optimized

**Trick/Tip:** Identical to longest common substring. Rolling hash with binary search is faster for large inputs.


---

### Problem 31: Paint House III

**Problem Statement:**
There are `n` houses, each to be painted with one of `m` colors. `cost[i][j]` is the cost of painting house `i` with color `j+1`. Given `target` (number of contiguous color groups), find minimum cost or -1 if impossible.

**Example:**
```
Input: costs = [[1,5],[2,4]], target = 2
Output: 5
```

**State Definition:**
- `dp[i][j][k]` = minimum cost to paint first `i` houses with `j` color groups, where the `i`-th house has color `k`

**Recurrence Relation:**
- For each color `k` at house `i`:
  - Same color as previous: `dp[i-1][j][k] + cost`
  - Different color: `min(dp[i-1][j-1][c]) + cost` for all `c != k`

**Base Case:**
- `dp[0][0][*] = 0`

**Python Code (Tabulation):**
```python
def minCost(costs, target):
    n, m = len(costs), len(costs[0])
    INF = float('inf')
    
    dp = [[INF] * m for _ in range(target + 1)]
    
    for k in range(m):
        if costs[0][k] != -1:
            dp[1][k] = costs[0][k]
    
    for i in range(1, n):
        new_dp = [[INF] * m for _ in range(target + 1)]
        for j in range(1, target + 1):
            for k in range(m):
                if costs[i-1][k] == -1:
                    continue
                # Same color
                if dp[j][k] < INF:
                    new_dp[j][k] = min(new_dp[j][k], dp[j][k] + costs[i-1][k])
                # Different color
                for c in range(m):
                    if c != k and dp[j-1][c] < INF:
                        new_dp[j][k] = min(new_dp[j][k], dp[j-1][c] + costs[i-1][k])
        dp = new_dp
    
    result = min(dp[target])
    return result if result < INF else -1
```

**Complexity:**
- Time: O(n * target * m^2)
- Space: O(target * m)

**Trick/Tip:** Handle same-color and different-color transitions separately.

---

### Problem 32: Longest Alternating Subsequence

**Problem Statement:**
Given an array `nums`, find the length of the longest subsequence where elements alternate between increasing and decreasing.

**Example:**
```
Input: nums = [1, 5, 4, 7]
Output: 4
```

**State Definition:**
- `up[i]` = length of longest alternating subsequence ending at `i` with last step being up
- `down[i]` = length of longest alternating subsequence ending at `i` with last step being down

**Recurrence Relation:**
- If `nums[i] > nums[j]`: `up[i] = max(up[i], down[j] + 1)`
- If `nums[i] < nums[j]`: `down[i] = max(down[i], up[j] + 1)`

**Base Case:**
- `up[i] = down[i] = 1`

**Python Code (Tabulation):**
```python
def longestAlternatingSubsequence(nums):
    n = len(nums)
    up = [1] * n
    down = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j]:
                up[i] = max(up[i], down[j] + 1)
            elif nums[i] < nums[j]:
                down[i] = max(down[i], up[j] + 1)
    
    return max(max(up), max(down))

# O(n) greedy approach
def longestAlternatingSubsequenceGreedy(nums):
    n = len(nums)
    if n <= 1:
        return n
    
    up = down = 1
    
    for i in range(1, n):
        if nums[i] > nums[i-1]:
            up = down + 1
        elif nums[i] < nums[i-1]:
            down = up + 1
    
    return max(up, down)
```

**Complexity:**
- DP: O(n^2) time, O(n) space
- Greedy: O(n) time, O(1) space

**Trick/Tip:** The greedy approach works because we only care about the last direction.

---

### Problem 33: Longest Bitonic Subsequence

**Problem Statement:**
A bitonic subsequence first increases then decreases. Find the length of the longest bitonic subsequence.

**Example:**
```
Input: nums = [1, 11, 2, 10, 4, 5, 2, 1]
Output: 6
```

**State Definition:**
- `lis[i]` = length of longest increasing subsequence ending at `i`
- `lds[i]` = length of longest decreasing subsequence starting at `i`

**Recurrence Relation:**
- `lis[i] = 1 + max(lis[j])` for `j < i` where `nums[j] < nums[i]`
- `lds[i] = 1 + max(lds[j])` for `j > i` where `nums[j] < nums[i]`

**Base Case:**
- `lis[i] = lds[i] = 1`

**Python Code (Tabulation):**
```python
def longestBitonicSubsequence(nums):
    n = len(nums)
    lis = [1] * n
    lds = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                lis[i] = max(lis[i], lis[j] + 1)
    
    for i in range(n - 2, -1, -1):
        for j in range(i + 1, n):
            if nums[j] < nums[i]:
                lds[i] = max(lds[i], lds[j] + 1)
    
    result = 0
    for i in range(n):
        if lis[i] > 1 and lds[i] > 1:
            result = max(result, lis[i] + lds[i] - 1)
    
    return result
```

**Complexity:**
- Time: O(n^2)
- Space: O(n)

**Trick/Tip:** Compute LIS from left and LDS from right. Peak element is counted twice, subtract 1.

---

### Problem 34: Maximum Sum Increasing Subsequence

**Problem Statement:**
Given an array of positive integers, find the maximum sum of an increasing subsequence.

**Example:**
```
Input: nums = [1, 101, 2, 3, 100, 4, 5]
Output: 106
```

**State Definition:**
- `dp[i]` = maximum sum of increasing subsequence ending at index `i`

**Recurrence Relation:**
- `dp[i] = max(dp[j] + nums[i])` for `j < i` where `nums[j] < nums[i]`
- Also `dp[i] = max(dp[i], nums[i])`

**Base Case:**
- `dp[i] = nums[i]`

**Python Code (Tabulation):**
```python
def maxSumIS(nums):
    n = len(nums)
    dp = nums[:]
    result = max(dp)
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + nums[i])
        result = max(result, dp[i])
    
    return result

# With path reconstruction
def maxSumISWithPath(nums):
    n = len(nums)
    dp = nums[:]
    parent = [-1] * n
    result = max(dp)
    end_idx = 0
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + nums[i] > dp[i]:
                dp[i] = dp[j] + nums[i]
                parent[i] = j
        if dp[i] > result:
            result = dp[i]
            end_idx = i
    
    path = []
    while end_idx != -1:
        path.append(nums[end_idx])
        end_idx = parent[end_idx]
    
    return result, path[::-1]
```

**Complexity:**
- Time: O(n^2)
- Space: O(n)

**Trick/Tip:** Similar to LIS, but track maximum sum instead of length.

---

### Problem 35: Number of Ways to Reach a Position After Exactly K Steps

**Problem Statement:**
You are at position `start` on a number line. In one step, move to `start+1` or `start-1`. Return the number of ways to reach `endPos` after exactly `k` steps.

**Example:**
```
Input: start = 1, endPos = 2, k = 3
Output: 3
```

**State Definition:**
- `dp[i][j]` = number of ways to reach position `j` in `i` steps

**Recurrence Relation:**
- `dp[i][j] = dp[i-1][j-1] + dp[i-1][j+1]`

**Base Case:**
- `dp[0][start] = 1`

**Python Code (Tabulation):**
```python
def numberOfWays(startPos, endPos, k):
    MOD = 10**9 + 7
    offset = k
    
    prev = [0] * (2 * offset + 1)
    prev[offset] = 1
    
    for i in range(1, k + 1):
        curr = [0] * (2 * offset + 1)
        for j in range(2 * offset + 1):
            if j > 0:
                curr[j] = (curr[j] + prev[j-1]) % MOD
            if j < 2 * offset:
                curr[j] = (curr[j] + prev[j+1]) % MOD
        prev = curr
    
    return prev[endPos - startPos + offset]
```

**Complexity:**
- Time: O(k^2)
- Space: O(k)

**Trick/Tip:** Use offset to handle negative positions. Position range is bounded by [-k, k].

---

### Problem 36: Minimum Jumps to Reach Home

**Problem Statement:**
Given forbidden positions, jump forward by `a` or backward by `b` (cannot jump backward twice in a row), find minimum jumps to reach position 0 from `start`.

**Example:**
```
Input: forbidden = [14,4,18,1,15], a = 3, b = 15, start = 9
Output: 3
```

**State Definition:**
- `dp[i][0]` = min jumps to reach `i` (last move not backward)
- `dp[i][1]` = min jumps to reach `i` (last move was backward)

**Recurrence Relation:**
- Forward: `dp[i+a][0] = min(dp[i+a][0], dp[i][0] + 1)`
- Backward: `dp[i-b][1] = min(dp[i-b][1], dp[i][0] + 1)` (only if last not backward)

**Base Case:**
- `dp[start][0] = 0`

**Python Code (BFS):**
```python
def minimumJumps(forbidden, a, b, start):
    forbidden_set = set(forbidden)
    max_pos = max(max(forbidden) + a + b, start + a) + 100
    
    from collections import deque
    queue = deque([(start, 0, False)])
    visited = {(start, False)}
    
    while queue:
        pos, steps, was_backward = queue.popleft()
        
        if pos == 0:
            return steps
        
        next_pos = pos + a
        if next_pos <= max_pos and next_pos not in forbidden_set and (next_pos, False) not in visited:
            visited.add((next_pos, False))
            queue.append((next_pos, steps + 1, False))
        
        if not was_backward:
            next_pos = pos - b
            if next_pos >= 0 and next_pos not in forbidden_set and (next_pos, True) not in visited:
                visited.add((next_pos, True))
                queue.append((next_pos, steps + 1, True))
    
    return -1
```

**Complexity:**
- Time: O(max_pos)
- Space: O(max_pos)

**Trick/Tip:** The constraint "cannot jump backward twice in a row" is key. Track last move direction.

---

### Problem 37: Count Number of Ways to Place Houses

**Problem Statement:**
There is a street with `n` plots on each side. Place houses such that no two adjacent on the same side. Return the number of ways modulo 10^9 + 7.

**Example:**
```
Input: n = 3
Output: 64
```

**State Definition:**
- `dp[i]` = number of ways on one side up to plot `i`

**Recurrence Relation:**
- `dp[i] = dp[i-1] + dp[i-2]` (Fibonacci-like)

**Base Case:**
- `dp[0] = 1`, `dp[1] = 2`

**Python Code (Tabulation):**
```python
def countHousePlacements(n):
    MOD = 10**9 + 7
    
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 2
    
    for i in range(2, n + 1):
        dp[i] = (dp[i-1] + dp[i-2]) % MOD
    
    ways_one_side = dp[n]
    return (ways_one_side * ways_one_side) % MOD

# Space optimized
def countHousePlacementsOptimized(n):
    MOD = 10**9 + 7
    
    prev2 = 1
    prev1 = 2
    
    for i in range(2, n + 1):
        curr = (prev1 + prev2) % MOD
        prev2 = prev1
        prev1 = curr
    
    return (prev1 * prev1) % MOD
```

**Complexity:**
- Time: O(n)
- Space: O(1) optimized

**Trick/Tip:** Ways on one side follows Fibonacci. Square the result since sides are independent.

---

### Problem 38: Minimum Difficulty of a Job Schedule

**Problem Statement:**
Given `jobDifficulty` and `d` days, partition jobs into `d` non-empty contiguous groups. Difficulty of a day = max difficulty that day. Minimize total difficulty.

**Example:**
```
Input: jobDifficulty = [6,5,4,3,2,1], d = 2
Output: 7
```

**State Definition:**
- `dp[i][j]` = minimum difficulty to schedule first `i` jobs in `j` days

**Recurrence Relation:**
- `dp[i][j] = min over k of (dp[k][j-1] + max(jobDifficulty[k..i-1]))`

**Base Case:**
- `dp[0][0] = 0`

**Python Code (Tabulation):**
```python
def minDifficulty(jobDifficulty, d):
    n = len(jobDifficulty)
    if n < d:
        return -1
    
    INF = float('inf')
    dp = [[INF] * (d + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    
    for i in range(1, n + 1):
        for j in range(1, min(i + 1, d + 1)):
            max_diff = 0
            for k in range(i - 1, j - 2, -1):
                max_diff = max(max_diff, jobDifficulty[k])
                if dp[k][j-1] < INF:
                    dp[i][j] = min(dp[i][j], dp[k][j-1] + max_diff)
    
    return dp[n][d] if dp[n][d] < INF else -1
```

**Complexity:**
- Time: O(n^2 * d)
- Space: O(n * d)

**Trick/Tip:** Iterate backwards to track running maximum difficulty efficiently.

---

### Problem 39: Number of Ways to Wear Different Hats to Each Person

**Problem Statement:**
There are `n` people and 40 types of hats. Each person has a list of hats they like. Return the number of ways to assign a unique hat to each person.

**Example:**
```
Input: hats = [[3,4],[4,5],[5]]
Output: 1
```

**State Definition:**
- `dp[hat][mask]` = number of ways to assign hats from `hat..40` to people in `mask`

**Recurrence Relation:**
- Skip hat: `dp[hat+1][mask]`
- Assign hat to person: `dp[hat+1][mask | (1<<person)]`

**Base Case:**
- `dp[41][full_mask] = 1`

**Python Code (DP with Bitmask):**
```python
def numberWays(hats):
    MOD = 10**9 + 7
    n = len(hats)
    
    hat_to_people = [[] for _ in range(41)]
    for person, hat_list in enumerate(hats):
        for hat in hat_list:
            hat_to_people[hat].append(person)
    
    full_mask = (1 << n) - 1
    
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def dp(hat, mask):
        if mask == full_mask:
            return 1
        if hat > 40:
            return 0
        
        result = dp(hat + 1, mask)
        
        for person in hat_to_people[hat]:
            if not (mask & (1 << person)):
                result = (result + dp(hat + 1, mask | (1 << person))) % MOD
        
        return result
    
    return dp(1, 0)
```

**Complexity:**
- Time: O(40 * 2^n)
- Space: O(40 * 2^n) with memoization

**Trick/Tip:** Process hats one by one and use bitmask to track which people already have hats.

---

### Problem 40: Frog Jump

**Problem Statement:**
A frog crosses a river with stones. It starts at stone 0 and jumps with distance `k-1`, `k`, or `k+1` where `k` is the previous jump distance. Return `True` if the frog can cross.

**Example:**
```
Input: stones = [0,1,3,5,6,7,8,9]
Output: True
```

**State Definition:**
- `dp[i]` = set of possible jump distances to reach stone `i`

**Recurrence Relation:**
- For each `jump` in `dp[stone]`, try `jump-1`, `jump`, `jump+1`

**Base Case:**
- `dp[0] = {0}`

**Python Code (Tabulation):**
```python
def canCross(stones):
    stone_set = set(stones)
    dp = {stone: set() for stone in stones}
    dp[0].add(0)
    
    for stone in stones:
        for jump in dp[stone]:
            for next_jump in [jump - 1, jump, jump + 1]:
                if next_jump > 0:
                    next_stone = stone + next_jump
                    if next_stone in stone_set:
                        dp[next_stone].add(next_jump)
    
    return len(dp[stones[-1]]) > 0
```

**Complexity:**
- Time: O(n^2)
- Space: O(n^2)

**Trick/Tip:** At each stone, store all possible jump distances. The next jump must be k-1, k, or k+1.


<a id="hard"></a>
## HARD (20 Problems)

---

### Problem 41: Burst Balloons

**Problem Statement:**
Given `n` balloons with numbers, burst them one by one. Bursting balloon `i` gives `nums[left] * nums[i] * nums[right]` coins where `left` and `right` are adjacent to `i`. Find maximum coins.

**Example:**
```
Input: nums = [3, 1, 5, 8]
Output: 167
```

**State Definition:**
- `dp[i][j]` = maximum coins from bursting balloons in range `[i, j]`

**Recurrence Relation:**
- `dp[i][j] = max over k of (dp[i][k-1] + dp[k+1][j] + nums[k] * nums[i-1] * nums[j+1])`

**Base Case:**
- `dp[i][j] = 0` when `i > j`

**Python Code (Tabulation):**
```python
def maxCoins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    
    for length in range(1, n - 1):
        for i in range(1, n - length):
            j = i + length - 1
            for k in range(i, j + 1):
                dp[i][j] = max(dp[i][j],
                              dp[i][k-1] + dp[k+1][j] + nums[k] * nums[i-1] * nums[j+1])
    
    return dp[1][n-2]
```

**Complexity:**
- Time: O(n^3)
- Space: O(n^2)

**Trick/Tip:** Think of it as: what is the LAST balloon to burst in range `[i, j]`?

---

### Problem 42: Minimum Cost to Merge Stones

**Problem Statement:**
Given `n` stones with values, merge `k` adjacent stones at a time with cost equal to their sum. Find minimum cost to merge all stones into one.

**Example:**
```
Input: stones = [3, 2, 4, 1], k = 2
Output: 20
```

**State Definition:**
- `dp[i][j]` = minimum cost to merge stones `i..j`

**Recurrence Relation:**
- `dp[i][j] = min over split point p of (dp[i][p] + dp[p+1][j])` + sum if `(j-i) % (k-1) == 0`

**Base Case:**
- `dp[i][i] = 0`

**Python Code (Tabulation):**
```python
def mergeStones(stones, k):
    n = len(stones)
    if (n - 1) % (k - 1) != 0:
        return -1
    
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i+1] = prefix[i] + stones[i]
    
    INF = float('inf')
    dp = [[0] * n for _ in range(n)]
    
    for length in range(k, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = INF
            
            for t in range(i, j, k - 1):
                dp[i][j] = min(dp[i][j], dp[i][t] + dp[t+1][j])
            
            if (j - i) % (k - 1) == 0:
                dp[i][j] += prefix[j+1] - prefix[i]
    
    return dp[0][n-1]
```

**Complexity:**
- Time: O(n^3)
- Space: O(n^2)

**Trick/Tip:** Only merge `k` stones at a time. `(j-i) % (k-1) == 0` checks if range can be fully merged.

---

### Problem 43: Minimum Cost to Cut a Stick

**Problem Statement:**
Given a stick of length `n` and cuts at positions, cutting at position `x` costs `x` (current stick length). Find minimum total cost to make all cuts.

**Example:**
```
Input: n = 7, cuts = [1, 3, 4, 5]
Output: 16
```

**State Definition:**
- `dp[i][j]` = minimum cost to make all cuts between `cuts[i]` and `cuts[j]`

**Recurrence Relation:**
- `dp[i][j] = min over k of (dp[i][k] + dp[k][j] + cuts[j] - cuts[i])`

**Base Case:**
- `dp[i][i] = 0`

**Python Code (Tabulation):**
```python
def minCost(n, cuts):
    cuts = [0] + sorted(cuts) + [n]
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

**Complexity:**
- Time: O(m^3) where m is number of cuts
- Space: O(m^2)

**Trick/Tip:** Sort cuts and add boundaries. Cost of cutting a range is the range length.

---

### Problem 44: Strange Printer

**Problem Statement:**
A strange printer can only print the same character in a row. It can print over previously printed characters. Find minimum turns to print a given string.

**Example:**
```
Input: s = "aaabbb"
Output: 2
```

**State Definition:**
- `dp[i][j]` = minimum turns to print `s[i..j]`

**Recurrence Relation:**
- `dp[i][j] = dp[i+1][j] + 1` (print s[i] separately)
- For each `k` where `s[i] == s[k]`: `dp[i][j] = min(dp[i][j], dp[i+1][k] + dp[k+1][j])`

**Base Case:**
- `dp[i][i] = 1`

**Python Code (Tabulation):**
```python
def strangePrinter(s):
    if not s:
        return 0
    
    t = [s[0]]
    for c in s[1:]:
        if c != t[-1]:
            t.append(c)
    s = t
    n = len(s)
    
    dp = [[0] * n for _ in range(n)]
    
    for i in range(n):
        dp[i][i] = 1
    
    for i in range(n - 2, -1, -1):
        for j in range(i + 1, n):
            dp[i][j] = dp[i+1][j] + 1
            for k in range(i + 1, j + 1):
                if s[i] == s[k]:
                    dp[i][j] = min(dp[i][j], dp[i+1][k] + (dp[k+1][j] if k + 1 <= j else 0))
    
    return dp[0][n-1]
```

**Complexity:**
- Time: O(n^3)
- Space: O(n^2)

**Trick/Tip:** First remove consecutive duplicates. When s[i] == s[k], we can print them together.

---

### Problem 45: Stone Game III

**Problem Statement:**
Alice and Bob pick stones from a line. On each turn, pick 1, 2, or 3 stones. The player with maximum sum wins. Return "Alice", "Bob", or "Tie".

**Example:**
```
Input: stoneValue = [1, 2, 3, 7]
Output: "Bob"
```

**State Definition:**
- `dp[i]` = maximum score difference from stones `i..n-1`

**Recurrence Relation:**
- `dp[i] = max(stoneValue[i] - dp[i+1], stoneValue[i] + stoneValue[i+1] - dp[i+2], stoneValue[i] + stoneValue[i+1] + stoneValue[i+2] - dp[i+3])`

**Base Case:**
- `dp[i] = 0` for `i >= n`

**Python Code (Tabulation):**
```python
def stoneGameIII(stoneValue):
    n = len(stoneValue)
    dp = [0] * (n + 3)
    
    for i in range(n - 1, -1, -1):
        dp[i] = float('-inf')
        take = 0
        for k in range(1, 4):
            if i + k - 1 < n:
                take += stoneValue[i + k - 1]
                dp[i] = max(dp[i], take - dp[i + k])
    
    if dp[0] > 0:
        return "Alice"
    elif dp[0] < 0:
        return "Bob"
    else:
        return "Tie"
```

**Complexity:**
- Time: O(n)
- Space: O(n)

**Trick/Tip:** `take - dp[next]` means current player gains `take` then opponent plays optimally.

---

### Problem 46: Stone Game IV (Hard Version)

**Problem Statement:**
Alice and Bob play with `n` stones. Remove positive square number of stones. Player who cannot move loses. Return `True` if Alice wins.

**Example:**
```
Input: n = 1
Output: True
```

**State Definition:**
- `dp[i]` = True if current player can win with `i` stones

**Recurrence Relation:**
- `dp[i] = any(not dp[i - k*k])` for all valid `k`

**Base Case:**
- `dp[0] = False`

**Python Code (Tabulation):**
```python
def winnerSquareGame(n):
    dp = [False] * (n + 1)
    
    for i in range(1, n + 1):
        k = 1
        while k * k <= i:
            if not dp[i - k * k]:
                dp[i] = True
                break
            k += 1
    
    return dp[n]
```

**Complexity:**
- Time: O(n * sqrt(n))
- Space: O(n)

**Trick/Tip:** Game theory: winning if you can move to a losing position.

---

### Problem 47: Remove Boxes

**Problem Statement:**
Given boxes with colors, remove contiguous boxes of same color to earn `k*k` points where `k` is number of boxes removed. Find maximum points.

**Example:**
```
Input: boxes = [1,3,2,2,2,3,4,3,1]
Output: 23
```

**State Definition:**
- `dp[i][j][k]` = maximum points from boxes `i..j` with `k` boxes of same color as `boxes[i]` appended

**Recurrence Relation:**
- Remove now: `(k+1)^2 + dp[i+1][j][0]`
- Merge: `dp[i+1][m-1][0] + dp[m][j][k+1]` for each `m` where `boxes[m] == boxes[i]`

**Base Case:**
- `dp[i][j][k] = 0` when `i > j`

**Python Code (Memoization):**
```python
def removeBoxes(boxes):
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def dp(i, j, k):
        if i > j:
            return 0
        
        result = (k + 1) ** 2 + dp(i + 1, j, 0)
        
        for m in range(i + 1, j + 1):
            if boxes[m] == boxes[i]:
                result = max(result, dp(i + 1, m - 1, 0) + dp(m, j, k + 1))
        
        return result
    
    return dp(0, len(boxes) - 1, 0)
```

**Complexity:**
- Time: O(n^4)
- Space: O(n^3)

**Trick/Tip:** The third parameter `k` represents "virtual" boxes of same color appended to the left.

---

### Problem 48: Minimum Swaps to Make Sequences Increasing

**Problem Statement:**
Given two sequences `nums1` and `nums2`, return minimum swaps to make both strictly increasing.

**Example:**
```
Input: nums1 = [1,3,5,4], nums2 = [1,2,3,7]
Output: 1
```

**State Definition:**
- `swap[i]` = min swaps with swap at index `i`
- `noswap[i]` = min swaps without swap at index `i`

**Recurrence Relation:**
- If `nums1[i] > nums1[i-1]` and `nums2[i] > nums2[i-1]`:
  - `noswap[i] = noswap[i-1]`, `swap[i] = swap[i-1] + 1`
- If `nums1[i] > nums2[i-1]` and `nums2[i] > nums1[i-1]`:
  - `noswap[i] = min(noswap[i], swap[i-1])`, `swap[i] = min(swap[i], noswap[i-1] + 1)`

**Base Case:**
- `swap[0] = 1`, `noswap[0] = 0`

**Python Code (Tabulation):**
```python
def minSwap(nums1, nums2):
    n = len(nums1)
    swap = [0] * n
    noswap = [0] * n
    
    swap[0] = 1
    
    for i in range(1, n):
        swap[i] = noswap[i] = float('inf')
        
        if nums1[i] > nums1[i-1] and nums2[i] > nums2[i-1]:
            noswap[i] = noswap[i-1]
            swap[i] = swap[i-1] + 1
        
        if nums1[i] > nums2[i-1] and nums2[i] > nums1[i-1]:
            noswap[i] = min(noswap[i], swap[i-1])
            swap[i] = min(swap[i], noswap[i-1] + 1)
    
    return min(swap[n-1], noswap[n-1])

# Space optimized
def minSwapOptimized(nums1, nums2):
    n = len(nums1)
    swap = 1
    noswap = 0
    
    for i in range(1, n):
        new_swap = new_noswap = float('inf')
        
        if nums1[i] > nums1[i-1] and nums2[i] > nums2[i-1]:
            new_noswap = noswap
            new_swap = swap + 1
        
        if nums1[i] > nums2[i-1] and nums2[i] > nums1[i-1]:
            new_noswap = min(new_noswap, swap)
            new_swap = min(new_swap, noswap + 1)
        
        swap, noswap = new_swap, new_noswap
    
    return min(swap, noswap)
```

**Complexity:**
- Time: O(n)
- Space: O(1) optimized

**Trick/Tip:** Track two states: swapped and not-swapped. Only two valid transitions exist.

---

### Problem 49: Maximal Square

**Problem Statement:**
Given a binary matrix, find the area of the largest square containing only 1s.

**Example:**
```
Input: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
Output: 4
```

**State Definition:**
- `dp[i][j]` = side length of largest square with bottom-right corner at `(i, j)`

**Recurrence Relation:**
- If `matrix[i][j] == '1'`: `dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1`
- Else: `dp[i][j] = 0`

**Base Case:**
- First row and column: `dp[i][j] = matrix[i][j]`

**Python Code (Tabulation):**
```python
def maximalSquare(matrix):
    if not matrix or not matrix[0]:
        return 0
    
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    result = 0
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if matrix[i-1][j-1] == '1':
                dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
                result = max(result, dp[i][j])
    
    return result * result

# Space optimized
def maximalSquareOptimized(matrix):
    if not matrix or not matrix[0]:
        return 0
    
    m, n = len(matrix), len(matrix[0])
    prev = [0] * (n + 1)
    result = 0
    
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if matrix[i-1][j-1] == '1':
                curr[j] = min(prev[j], curr[j-1], prev[j-1]) + 1
                result = max(result, curr[j])
        prev = curr
    
    return result * result
```

**Complexity:**
- Time: O(m * n)
- Space: O(m * n) tabulation, O(n) optimized

**Trick/Tip:** The minimum of top, left, and top-left gives the largest square that can be formed.

---

### Problem 50: Dungeon Game

**Problem Statement:**
A knight starts at top-left of a dungeon grid. Each cell has a demon (negative HP) or orb (positive HP). The knight must have HP > 0 at all times. Find minimum initial HP to reach bottom-right.

**Example:**
```
Input: dungeon = [[-2,-3,3],[-5,-10,1],[10,30,-5]]
Output: 7
```

**State Definition:**
- `dp[i][j]` = minimum HP needed at `(i, j)` to reach the end

**Recurrence Relation:**
- `dp[i][j] = max(1, min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j])`

**Base Case:**
- `dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])`

**Python Code (Tabulation - Bottom Right to Top Left):**
```python
def calculateMinimumHP(dungeon):
    m, n = len(dungeon), len(dungeon[0])
    dp = [[0] * n for _ in range(m)]
    
    dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])
    
    for i in range(m - 2, -1, -1):
        dp[i][n-1] = max(1, dp[i+1][n-1] - dungeon[i][n-1])
    
    for j in range(n - 2, -1, -1):
        dp[m-1][j] = max(1, dp[m-1][j+1] - dungeon[m-1][j])
    
    for i in range(m - 2, -1, -1):
        for j in range(n - 2, -1, -1):
            min_hp = min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j]
            dp[i][j] = max(1, min_hp)
    
    return dp[0][0]

# Space optimized
def calculateMinimumHPOptimized(dungeon):
    m, n = len(dungeon), len(dungeon[0])
    dp = [0] * n
    
    dp[n-1] = max(1, 1 - dungeon[m-1][n-1])
    
    for j in range(n - 2, -1, -1):
        dp[j] = max(1, dp[j+1] - dungeon[m-1][j])
    
    for i in range(m - 2, -1, -1):
        dp[n-1] = max(1, dp[n-1] - dungeon[i][n-1])
        for j in range(n - 2, -1, -1):
            dp[j] = max(1, min(dp[j+1], dp[j]) - dungeon[i][j])
    
    return dp[0]
```

**Complexity:**
- Time: O(m * n)
- Space: O(m * n) tabulation, O(n) optimized

**Trick/Tip:** Work backwards from destination. At each cell, calculate minimum HP needed to survive.


---

### Problem 51: Longest Palindromic Substring (DP Approach)

**Problem Statement:**
Given a string `s`, find the longest palindromic substring.

**Example:**
```
Input: s = "babad"
Output: "bab" or "aba"
```

**State Definition:**
- `dp[i][j]` = True if `s[i..j]` is a palindrome

**Recurrence Relation:**
- If `s[i] == s[j]` and `dp[i+1][j-1]`: `dp[i][j] = True`

**Base Case:**
- `dp[i][i] = True`
- `dp[i][i+1] = (s[i] == s[i+1])`

**Python Code (Tabulation):**
```python
def longestPalindrome(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start = 0
    max_len = 1
    
    for i in range(n):
        dp[i][i] = True
    
    for i in range(n - 1):
        if s[i] == s[i+1]:
            dp[i][i+1] = True
            start = i
            max_len = 2
    
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i+1][j-1]:
                dp[i][j] = True
                if length > max_len:
                    start = i
                    max_len = length
    
    return s[start:start + max_len]

# Space optimized (expand around center)
def longestPalindromeExpand(s):
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left+1:right]
    
    result = ""
    for i in range(len(s)):
        odd = expand(i, i)
        even = expand(i, i + 1)
        result = max(result, odd, even, key=len)
    
    return result
```

**Complexity:**
- DP: O(n^2) time, O(n^2) space
- Expand: O(n^2) time, O(1) space

**Trick/Tip:** DP fills diagonal by diagonal. Expand around center is more space efficient.

---

### Problem 52: Palindrome Partitioning II

**Problem Statement:**
Given a string `s`, partition it such that every substring is a palindrome. Return the minimum number of cuts.

**Example:**
```
Input: s = "aab"
Output: 1
```

**State Definition:**
- `dp[i]` = minimum cuts for `s[0..i]`
- `is_pal[i][j]` = True if `s[i..j]` is palindrome

**Recurrence Relation:**
- If `s[0..i]` is palindrome: `dp[i] = 0`
- Else: `dp[i] = min(dp[j] + 1)` for all `j < i` where `s[j+1..i]` is palindrome

**Base Case:**
- `dp[i] = i` (worst case: cut every character)

**Python Code (Tabulation):**
```python
def minCut(s):
    n = len(s)
    
    # Precompute palindromes
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for i in range(n - 1):
        is_pal[i][i+1] = (s[i] == s[i+1])
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = (s[i] == s[j] and is_pal[i+1][j-1])
    
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

# Optimized approach
def minCutOptimized(s):
    n = len(s)
    dp = [i for i in range(n)]
    
    for i in range(n):
        # Odd length palindrome
        left, right = i, i
        while left >= 0 and right < n and s[left] == s[right]:
            if left == 0:
                dp[right] = 0
            else:
                dp[right] = min(dp[right], dp[left-1] + 1)
            left -= 1
            right += 1
        
        # Even length palindrome
        left, right = i, i + 1
        while left >= 0 and right < n and s[left] == s[right]:
            if left == 0:
                dp[right] = 0
            else:
                dp[right] = min(dp[right], dp[left-1] + 1)
            left -= 1
            right += 1
    
    return dp[n-1]
```

**Complexity:**
- Time: O(n^2)
- Space: O(n^2) or O(n) optimized

**Trick/Tip:** Expand around center approach avoids precomputing all palindromes.

---

### Problem 53: Word Break II

**Problem Statement:**
Given a string `s` and a dictionary `wordDict`, return all possible sentences where each word is in the dictionary.

**Example:**
```
Input: s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]
Output: ["cats and dog","cat sand dog"]
```

**State Definition:**
- `dp[i]` = list of all valid sentences for `s[i..]`

**Recurrence Relation:**
- For each word `w` in dictionary that starts at `i`:
  - `dp[i] += [w + " " + sent] for sent in dp[i + len(w)]`

**Base Case:**
- `dp[n] = [""]`

**Python Code (Memoization):**
```python
def wordBreak(s, wordDict):
    word_set = set(wordDict)
    n = len(s)
    
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def dp(i):
        if i == n:
            return [""]
        
        result = []
        for end in range(i + 1, n + 1):
            word = s[i:end]
            if word in word_set:
                for sent in dp(end):
                    if sent:
                        result.append(word + " " + sent)
                    else:
                        result.append(word)
        
        return result
    
    return dp(0)

# Alternative with backtracking
def wordBreakBacktrack(s, wordDict):
    word_set = set(wordDict)
    n = len(s)
    result = []
    
    def backtrack(start, path):
        if start == n:
            result.append(" ".join(path))
            return
        
        for end in range(start + 1, n + 1):
            word = s[start:end]
            if word in word_set:
                path.append(word)
                backtrack(end, path)
                path.pop()
    
    backtrack(0, [])
    return result
```

**Complexity:**
- Time: O(2^n) in worst case
- Space: O(2^n) for storing results

**Trick/Tip:** Use memoization to avoid recomputing suffixes. Backtracking with pruning is also effective.

---

### Problem 54: Count Different Subsequence GCDs

**Problem Statement:**
Given an array `nums`, return the number of different GCDs among all non-empty subsequences.

**Example:**
```
Input: nums = [6,10,3]
Output: 5
Explanation: GCDs are: 1, 2, 3, 5, 6
```

**State Definition:**
- For each possible GCD `g`, check if there's a subsequence with that GCD

**Recurrence Relation:**
- GCD `g` is achievable if there exist elements that are all multiples of `g` and their GCD is exactly `g`

**Base Case:**
- Count each possible GCD

**Python Code (DP on GCD):**
```python
from math import gcd
from collections import Counter

def countDifferentSubsequenceGCDs(nums):
    max_val = max(nums)
    count = Counter(nums)
    
    result = 0
    for g in range(1, max_val + 1):
        multiple_gcd = 0
        for multiple in range(g, max_val + 1, g):
            if multiple in count:
                multiple_gcd = gcd(multiple_gcd, multiple)
        if multiple_gcd == g:
            result += 1
    
    return result
```

**Complexity:**
- Time: O(max_val * log(max_val))
- Space: O(max_val)

**Trick/Tip:** For each GCD `g`, find all multiples in the array and compute their GCD. If result is `g`, it's achievable.

---

### Problem 55: Number of Ways to Form a Target String

**Problem Statement:**
Given a list of `words` (all same length) and a `target` string, form `target` by picking characters from words. Each character at position `j` can be picked from any word's `j`-th position. Return ways modulo 10^9 + 7.

**Example:**
```
Input: words = ["acca","bbbb","caca"], target = "aba"
Output: 6
```

**State Definition:**
- `dp[i][j]` = number of ways to form `target[0..i-1]` using first `j` columns

**Recurrence Relation:**
- `dp[i][j] = dp[i][j-1] + dp[i-1][j-1] * count[j][target[i-1]]`

**Base Case:**
- `dp[0][j] = 1` for all j

**Python Code (Tabulation):**
```python
def numWays(words, target):
    MOD = 10**9 + 7
    m, n = len(target), len(words[0])
    k = len(words)
    
    # Count occurrences of each character at each position
    char_count = [[0] * 26 for _ in range(n)]
    for word in words:
        for j, c in enumerate(word):
            char_count[j][ord(c) - ord('a')] += 1
    
    dp = [0] * (m + 1)
    dp[0] = 1
    
    for j in range(n):
        new_dp = dp[:]
        for i in range(m):
            c = ord(target[i]) - ord('a')
            if char_count[j][c] > 0:
                new_dp[i+1] = (new_dp[i+1] + dp[i] * char_count[j][c]) % MOD
        dp = new_dp
    
    return dp[m]
```

**Complexity:**
- Time: O(n * (m + 26 * k))
- Space: O(m)

**Trick/Tip:** Process columns one by one. At each column, either skip it or use it to match the next character in target.

---

### Problem 56: Minimum Cost to Make Array Equal

**Problem Statement:**
Given arrays `nums` and `cost`, you can increase or decrease any element by 1 at a cost of `cost[i]`. Make all elements equal with minimum total cost.

**Example:**
```
Input: nums = [1,3,5], cost = [1,1,1]
Output: 7
```

**State Definition:**
- Sort by nums. For each target value, compute total cost.

**Recurrence Relation:**
- Prefix sums to compute cost efficiently

**Base Case:**
- Try all possible target values

**Python Code (Binary Search + Prefix Sum):**
```python
def minCost(nums, cost):
    n = len(nums)
    pairs = sorted(zip(nums, cost))
    
    prefix_cost = [0] * n
    prefix_cost[0] = pairs[0][1]
    for i in range(1, n):
        prefix_cost[i] = prefix_cost[i-1] + pairs[i][1]
    
    total_cost = 0
    for i in range(1, n):
        total_cost += (pairs[i][0] - pairs[0][0]) * pairs[i][1]
    
    result = total_cost
    
    for i in range(1, n):
        diff = pairs[i][0] - pairs[i-1][0]
        total_cost += diff * prefix_cost[i-1]
        total_cost -= diff * (prefix_cost[n-1] - prefix_cost[i])
        result = min(result, total_cost)
    
    return result

# Binary search approach
def minCostBinarySearch(nums, cost):
    def compute_cost(target):
        return sum(abs(num - target) * c for num, c in zip(nums, cost))
    
    left, right = min(nums), max(nums)
    result = compute_cost(left)
    
    while left <= right:
        mid = (left + right) // 2
        cost_mid = compute_cost(mid)
        cost_mid_plus = compute_cost(mid + 1)
        result = min(result, cost_mid, cost_mid_plus)
        
        if cost_mid < cost_mid_plus:
            right = mid - 1
        else:
            left = mid + 1
    
    return result
```

**Complexity:**
- Time: O(n log n) for binary search, O(n) for prefix sum approach
- Space: O(n)

**Trick/Tip:** The cost function is convex. Binary search or weighted median gives optimal solution.

---

### Problem 57: Maximum Score from Performing Multiplication Operations

**Problem Statement:**
Given arrays `nums` and `multipliers` of size `n`, perform exactly `m` operations. Each operation picks either first or last element and multiplies with `multipliers[i]`. Maximize score.

**Example:**
```
Input: nums = [-5,-3,-3,-2,7,1], multipliers = [-10,3,4]
Output: 102
```

**State Definition:**
- `dp[i][j]` = maximum score using first `i` elements from left and `j` from right

**Recurrence Relation:**
- `dp[i][j] = max(dp[i-1][j] + nums[left] * mult[i+j], dp[i][j-1] + nums[right] * mult[i+j])`

**Base Case:**
- `dp[0][0] = 0`

**Python Code (Tabulation):**
```python
def maximumScore(nums, multipliers):
    n, m = len(nums), len(multipliers)
    dp = [[0] * (m + 1) for _ in range(m + 1)]
    
    for ops in range(1, m + 1):
        for left in range(ops + 1):
            right = ops - left
            if left > 0:
                dp[left][right] = max(dp[left][right],
                                     dp[left-1][right] + nums[left-1] * multipliers[ops-1])
            if right > 0:
                dp[left][right] = max(dp[left][right],
                                     dp[left][right-1] + nums[n-right] * multipliers[ops-1])
    
    return dp[m][0]  # Or any dp[left][right] where left + right = m

# Space optimized
def maximumScoreOptimized(nums, multipliers):
    n, m = len(nums), len(multipliers)
    dp = [0] * (m + 1)
    
    for ops in range(m, 0, -1):
        new_dp = [0] * (m + 1)
        for left in range(ops + 1):
            right = ops - left
            if left > 0:
                new_dp[left] = max(new_dp[left],
                                  dp[left-1] + nums[left-1] * multipliers[ops-1])
            if right > 0:
                new_dp[left] = max(new_dp[left],
                                  dp[left] + nums[n-right] * multipliers[ops-1])
        dp = new_dp
    
    return dp[0]
```

**Complexity:**
- Time: O(m^2)
- Space: O(m^2) tabulation, O(m) optimized

**Trick/Tip:** Track how many elements picked from left; right picks = ops - left picks.

---

### Problem 58: Number of Increasing Subsequences in a Tree

**Problem Statement:**
Given a binary tree, count the number of increasing subsequences in the tree (paths from root to any node where values increase).

**Example:**
```
Input: root = [2,1,3]
Output: 4
Explanation: [2], [2,3], [1], [3]
```

**State Definition:**
- `dp[node]` = number of increasing subsequences ending at `node`

**Recurrence Relation:**
- For each child: if `child.val > node.val`: `dp[child] += dp[node]`
- Also count single-node subsequences

**Base Case:**
- `dp[node] = 1` (the node itself)

**Python Code (DFS):**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def countSubsequences(root):
    MOD = 10**9 + 7
    
    def dfs(node, parent_val):
        if not node:
            return 0
        
        count = 1  # The node itself
        
        if node.left:
            left_count = dfs(node.left, node.val)
            if node.val < node.left.val:
                count += left_count
            count += left_count
        
        if node.right:
            right_count = dfs(node.right, node.val)
            if node.val < node.right.val:
                count += right_count
            count += right_count
        
        return count % MOD
    
    return dfs(root, float('-inf'))

# Better approach: count all increasing paths
def countIncreasingPaths(root):
    result = 0
    
    def dfs(node, min_val):
        if not node:
            return 0
        
        count = 0
        if node.val > min_val:
            count = 1
            count += dfs(node.left, node.val)
            count += dfs(node.right, node.val)
        else:
            count += dfs(node.left, min_val)
            count += dfs(node.right, min_val)
        
        return count
    
    return dfs(root, float('-inf'))
```

**Complexity:**
- Time: O(n^2) worst case, O(n log n) for balanced trees
- Space: O(h) where h is tree height

**Trick/Tip:** Pass the minimum value down. At each node, decide whether to include it in the increasing path.

---

### Problem 59: Profitable Schemes

**Problem Statement:**
There are `n` members in a gang. Each crime has `group` (members needed), `profit` earned, and `minProfit` minimum required. Find number of schemes that earn at least `minProfit`.

**Example:**
```
Input: n = 5, minProfit = 3, group = [2,2], profit = [2,3]
Output: 2
```

**State Definition:**
- `dp[i][j][k]` = number of ways using first `i` crimes, with `j` members, earning at least `k` profit

**Recurrence Relation:**
- Skip crime: `dp[i-1][j][k]`
- Take crime: `dp[i-1][j-group[i-1]][max(0, k-profit[i-1])]`

**Base Case:**
- `dp[0][0][0] = 1`

**Python Code (Tabulation):**
```python
def profitableSchemes(n, minProfit, group, profit):
    MOD = 10**9 + 7
    m = len(group)
    
    dp = [[[0] * (minProfit + 1) for _ in range(n + 1)] for _ in range(m + 1)]
    dp[0][0][0] = 1
    
    for i in range(1, m + 1):
        for j in range(n + 1):
            for k in range(minProfit + 1):
                dp[i][j][k] = dp[i-1][j][k]
                if j >= group[i-1]:
                    prev_profit = max(0, k - profit[i-1])
                    dp[i][j][k] = (dp[i][j][k] + dp[i-1][j-group[i-1]][prev_profit]) % MOD
    
    result = 0
    for j in range(n + 1):
        result = (result + dp[m][j][minProfit]) % MOD
    
    return result

# Space optimized
def profitableSchemesOptimized(n, minProfit, group, profit):
    MOD = 10**9 + 7
    m = len(group)
    
    dp = [[0] * (minProfit + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(m):
        new_dp = [row[:] for row in dp]
        for j in range(n + 1):
            for k in range(minProfit + 1):
                if dp[j][k] > 0 and j + group[i] <= n:
                    new_k = min(minProfit, k + profit[i])
                    new_dp[j + group[i]][new_k] = (new_dp[j + group[i]][new_k] + dp[j][k]) % MOD
        dp = new_dp
    
    result = 0
    for j in range(n + 1):
        result = (result + dp[j][minProfit]) % MOD
    
    return result
```

**Complexity:**
- Time: O(m * n * minProfit)
- Space: O(m * n * minProfit) tabulation, O(n * minProfit) optimized

**Trick/Tip:** Cap profit at `minProfit` since earning more doesn't change the result.

---

### Problem 60: Last Stone Weight II

**Problem Statement:**
You have `n` stones with weights. On each turn, smash two stones together. The result is `abs(stone1 - stone2)`. Find the minimum possible weight of the last remaining stone.

**Example:**
```
Input: stones = [2,7,4,1,8,1]
Output: 1
```

**State Definition:**
- `dp[i]` = True if we can form a subset with sum `i`

**Recurrence Relation:**
- For each stone, update dp: `dp[j] = dp[j] or dp[j - stone]`

**Base Case:**
- `dp[0] = True`

**Python Code (Subset Sum DP):**
```python
def lastStoneWeightII(stones):
    total = sum(stones)
    target = total // 2
    
    dp = [False] * (target + 1)
    dp[0] = True
    
    for stone in stones:
        for j in range(target, stone - 1, -1):
            dp[j] = dp[j] or dp[j - stone]
    
    # Find closest sum to target
    for i in range(target, -1, -1):
        if dp[i]:
            return total - 2 * i
    
    return 0

# Alternative approach
def lastStoneWeightIIAlt(stones):
    total = sum(stones)
    target = total // 2
    
    dp = {0}
    
    for stone in stones:
        new_dp = set()
        for s in dp:
            new_dp.add(s)
            new_dp.add(s + stone)
        dp = new_dp
    
    best = 0
    for s in dp:
        if s <= target:
            best = max(best, s)
    
    return total - 2 * best
```

**Complexity:**
- Time: O(n * total)
- Space: O(total)

**Trick/Tip:** This is a partition problem. We want to split stones into two groups with minimum difference. The answer is `total - 2 * max_subset_sum_where_sum <= total/2`.

---

## Summary of DP Patterns

### 1D DP
- Fibonacci, Tribonacci, House Robber, Climbing Stairs

### 2D String DP
- LCS, Edit Distance, Distinct Subsequences, Interleaving String

### Interval DP
- Burst Balloons, Merge Stones, Cut Stick, Strange Printer

### Bitmask DP
- Number of Ways to Wear Hats, Stone Game variants

### Game Theory DP
- Stone Game III/IV, Winner Square Game

### Knapsack Variants
- Profitable Schemes, Last Stone Weight II, Minimum Cost for Tickets

### Matrix Chain Multiplication
- Burst Balloons, Minimum Cost to Cut a Stick

### Tree DP
- Unique BST, Increasing Subsequences in Tree

---

**End of DP Problems Batch 2**
**Total: 60 Problems with Complete Solutions**
