# 2D DP — Advanced Problems

## Longest Palindromic Subsequence

Given a string, find the length of the longest subsequence that is a palindrome.

**Concept:** if s[i] == s[j]: dp[i][j] = dp[i+1][j-1] + 2 else: dp[i][j] = max(dp[i+1][j], dp[i][j-1])

```python
def longest_palindrome_subseq_memo(s: str, i: int = None, j: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if i is None:
        return longest_palindrome_subseq_memo(s, 0, len(s) - 1, memo)
    if i > j:
        return 0
    if i == j:
        return 1
    key = (i, j)
    if key in memo:
        return memo[key]
    if s[i] == s[j]:
        memo[key] = 2 + longest_palindrome_subseq_memo(s, i + 1, j - 1, memo)
    else:
        memo[key] = max(longest_palindrome_subseq_memo(s, i + 1, j, memo),
                        longest_palindrome_subseq_memo(s, i, j - 1, memo))
    return memo[key]

def longest_palindrome_subseq_tab(s: str) -> int:
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

# DP Table for "bbbab":
#   b b b a b
# b 1 2 3 3 4
# b 0 1 2 2 3
# b 0 0 1 1 3
# a 0 0 0 1 1
# b 0 0 0 0 1
# Answer: 4

# Time: O(n²), Space: O(n²)
```

---

## Shortest Common Supersequence

Given two strings, find the shortest string that has both as subsequences.

```python
def shortest_common_supersequence(a: str, b: str) -> str:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack to build SCS
    i, j = m, n
    result = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            result.append(a[i - 1])
            i -= 1
        else:
            result.append(b[j - 1])
            j -= 1
    while i > 0:
        result.append(a[i - 1])
        i -= 1
    while j > 0:
        result.append(b[j - 1])
        j -= 1
    return ''.join(reversed(result))

# Example: a = "abac", b = "cab"
# Answer: "cabac"
# SCS length = len(a) + len(b) - LCS_length

# Time: O(m×n), Space: O(m×n)
```

---

## Maximum Square in Binary Matrix

Given a matrix of 0s and 1s, find the area of the largest square containing only 1s.

**Concept:** dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) if matrix[i][j] == '1'

```python
def maximal_square(matrix: list) -> int:
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_side = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if matrix[i - 1][j - 1] == '1':
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
                max_side = max(max_side, dp[i][j])
    return max_side * max_side

# DP Table for:
# 1 0 1 0 0
# 1 0 1 1 1
# 1 1 1 1 1
# 1 0 0 1 0
# Result: 4 (max side = 2)

# Time: O(m×n), Space: O(m×n)
```

### With space optimization

```python
def maximal_square_optimized(matrix: list) -> int:
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    prev = [0] * (n + 1)
    max_side = 0
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if matrix[i - 1][j - 1] == '1':
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
                max_side = max(max_side, curr[j])
        prev = curr
    return max_side * max_side

# Time: O(m×n), Space: O(n)
```

---

## Maximal Rectangle

Given a matrix of 0s and 1s, find the largest rectangle containing only 1s.

**Approach:** For each row, treat heights histogram and use largest rectangle in histogram.

```python
def maximal_rectangle(matrix: list) -> int:
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    heights = [0] * n
    max_area = 0
    for i in range(m):
        for j in range(n):
            heights[j] = heights[j] + 1 if matrix[i][j] == '1' else 0
        max_area = max(max_area, largest_rectangle(heights))
    return max_area

def largest_rectangle(heights: list) -> int:
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

# Example:
# matrix = [["1","0","1","0","0"],
#           ["1","0","1","1","1"],
#           ["1","1","1","1","1"],
#           ["1","0","0","1","0"]]
# Answer: 6

# Time: O(m×n), Space: O(n)
```

---

## Count Squares in Binary Matrix

Count total squares of all sizes that consist of only 1s.

```python
def count_squares(matrix: list) -> int:
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * n for _ in range(m)]
    total = 0
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 1:
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
                total += dp[i][j]
    return total

# Example:
# matrix = [[0,1,1,1,0],
#           [1,1,1,1,0],
#           [0,1,1,1,0],
#           [0,0,1,1,0]]
# dp:        [0,1,1,1,0]
#           [1,1,2,2,0]
#           [0,1,2,3,0]
#           [0,0,1,2,0]
# Answer: 1+1+1+1+1+2+2+1+2+3+1+2 = 18 squares

# Time: O(m×n), Space: O(m×n)
```

---

## Burst Balloons

Given n balloons, each with a number. Burst balloon i gets nums[i-1] * nums[i] * nums[i+1] coins. Find max coins.

**Concept:** Add sentinel 1s at both ends. dp[i][j] = max coins from bursting all balloons between i and j.

```python
def max_coins_memo(nums: list) -> int:
    nums = [1] + nums + [1]
    n = len(nums)
    memo = {}

    def solve(l: int, r: int) -> int:
        if l >= r:
            return 0
        key = (l, r)
        if key in memo:
            return memo[key]
        best = 0
        for k in range(l + 1, r):
            coins = nums[l] * nums[k] * nums[r] + solve(l, k) + solve(k, r)
            best = max(best, coins)
        memo[key] = best
        return best

    return solve(0, n - 1)

def max_coins_tab(nums: list) -> int:
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):  # length from 2 to n-1
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):
                dp[i][j] = max(dp[i][j],
                               nums[i] * nums[k] * nums[j] + dp[i][k] + dp[k][j])
    return dp[0][n - 1]

# Example: nums = [3, 1, 5, 8]
# Answer: 167 (burst order: 1 → 5 → 3 → 8)

# Time: O(n³), Space: O(n²)
```

---

## Stone Game III

Alice and Bob take turns, each takes 1, 2, or 3 stones from the end. Maximize Alice's score.

```python
def stone_game_iii(values: list) -> str:
    n = len(values)
    dp = [float('-inf')] * (n + 1)
    dp[n] = 0
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + values[i]

    for i in range(n - 1, -1, -1):
        for take in range(1, 4):
            if i + take <= n:
                dp[i] = max(dp[i], suffix[i] - dp[i + take])

    if dp[0] > suffix[0] - dp[0]:
        return "Alice"
    elif dp[0] < suffix[0] - dp[0]:
        return "Bob"
    return "Tie"

# Time: O(n), Space: O(n)
```

---

## Game Theory DP

### Predict the Winner (Nim-style)

Given an array of scores. Players take from either end. Player 1 wins if score ≥ opponent.

```python
def predict_the_winner(nums: list) -> bool:
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    # dp[i][j] = max net score player can achieve from subarray [i, j]
    for i in range(n - 1, -1, -1):
        dp[i][i] = nums[i]
        for j in range(i + 1, n):
            dp[i][j] = max(nums[i] - dp[i + 1][j],
                           nums[j] - dp[i][j - 1])
    return dp[0][n - 1] >= 0

# Time: O(n²), Space: O(n²)
```

### Nim Game

One pile of stones. Each player can take 1-3 stones. Player who takes the last stone wins.

```python
def can_win_nim(n: int) -> bool:
    return n % 4 != 0

# Time: O(1), Space: O(1)
```

### Nim Game II (DP version)

```python
def nim_game_dp(n: int) -> bool:
    if n <= 3:
        return True
    dp = [False] * (n + 1)
    dp[1] = dp[2] = dp[3] = True
    for i in range(4, n + 1):
        dp[i] = not dp[i - 1] or not dp[i - 2] or not dp[i - 3]
    return dp[n]

# Time: O(n), Space: O(n)
```

---

## Summary Table

| Problem | Approach | Time | Space |
|---------|----------|------|-------|
| L Palindromic Subseq | Interval DP | O(n²) | O(n²) |
| Shortest Common Super | LCS + Backtrack | O(m×n) | O(m×n) |
| Max Square in Matrix | Min of three | O(m×n) | O(n) |
| Max Rectangle | Histogram method | O(m×n) | O(n) |
| Count Squares | Bottom-up DP | O(m×n) | O(m×n) |
| Burst Balloons | Interval DP O(n³) | O(n³) | O(n²) |
| Stone Game III | Suffix sum DP | O(n) | O(n) |
| Predict Winner | Minmax DP | O(n²) | O(n²) |
