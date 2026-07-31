# 2D DP — Advanced Problems

## When to Use These Advanced Patterns

```
┌──────────────────────────────────────────────────────────────────────┐
│                2D ADVANCED DP PATTERN GUIDE                         │
├─────────────────────────────┬────────────────────────────────────────┤
│ Problem hints               │ Pattern                              │
├─────────────────────────────┼────────────────────────────────────────┤
│ "palindrome subsequence"    │ Interval DP: dp[i][j] on s[i..j]    │
│ "shortest supersequence"    │ LCS-based construction               │
│ "largest square/rectangle"  │ Min of 3 neighbors + 1              │
│ "burst balloons / partition"│ Interval DP with O(n³) splitting     │
│ "game from both ends"       │ Minimax interval DP                  │
│ "count all squares"         │ Sum up dp[i][j] values               │
└─────────────────────────────┴────────────────────────────────────────┘
```

---

## Longest Palindromic Subsequence

Given a string, find the length of the longest subsequence that is a palindrome.

### Visual Walkthrough

```
s = "bbbab"

The LPS = "bbbb" (length 4) — remove the 'a'

DP Table (filled bottom-left to top-right):
     b  b  b  a  b      ← j (right pointer)
  ┌────┬────┬────┬────┬────┐
 b│ 1  │ 2  │ 3  │ 3  │ 4  │  ← dp[0][4]: s[0]=b, s[4]=b match! → dp[1][3]+2=4
  ├────┼────┼────┼────┼────┤
 b│ .  │ 1  │ 2  │ 2  │ 3  │
  ├────┼────┼────┼────┼────┤
 b│ .  │ .  │ 1  │ 1  │ 3  │
  ├────┼────┼────┼────┼────┤
 a│ .  │ .  │ .  │ 1  │ 1  │
  ├────┼────┼────┼────┼────┤
 b│ .  │ .  │ .  │ .  │ 1  │
  └────┴────┴────┴────┴────┘
  ↑ i (left pointer, fill bottom-up)

Fill order (diagonals, length increasing):
  Diagonal 0 (i==j): dp[i][i] = 1  (single char = palindrome of length 1)
  Diagonal 1:        dp[i][i+1] → s[i]==s[i+1] ? 2 : 1
  Diagonal 2, 3, 4:  Increasing lengths

  dp[0][4] = 4 means: longest palindromic subsequence of "bbbab" has length 4
```

```python
def longest_palindrome_subseq_tab(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    # Fill by increasing interval length
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1  # Base: single character is palindrome of length 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2  # Both ends match
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])  # Skip one end
    return dp[0][n - 1]

# Time: O(n²), Space: O(n²)
# Note: this is also O(n²) space; can optimize to O(n) with careful rolling
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

### Visual Walkthrough

```
matrix:                DP table:
1 0 1 0 0              0 0 0 0 0 0
1 0 1 1 1              0 1 0 1 1 1
1 1 1 1 1              0 1 2 2 2 2
1 0 0 1 0              0 1 0 0 1 0

Rule: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                       ─────────────────────────────────────────
                       If ALL three neighbors are ≥ X, then this
                       cell can form an (X+1)×(X+1) square

Why? A square needs:
  -  □ □       Above must support this width
  -  □ ■  ←    Left must support this height
  -            Diagonal ensures square shape (not just rectangle)

Visual at dp[3][4] (matrix[2][3]='1'):
    1  1        dp values:  2  2
    2  2 ■                   2  [2] ← this = 1 + min(2,2,2) = 3
    0  0                       0   0
                            Wait, let me recompute:

matrix[2][3] = '1' → dp[3][4] = 1 + min(dp[2][4], dp[3][3], dp[2][3])
                          = 1 + min(2, 2, 2) = 3  ← No wait, indexing...

Let me use 0-indexed with padding:

Original matrix:        DP (with 0 padding):
1 0 1 0 0               0 0 0 0 0 0
1 0 1 1 1               0 1 0 1 1 1
1 1 1 1 1               0 1 2 2 2 2
1 0 0 1 0               0 1 0 0 1 0

At (2,3): matrix=1, dp=1+min(dp[1][3],dp[2][2],dp[1][2])=1+min(1,2,1)=2
At (2,4): matrix=1, dp=1+min(dp[1][4],dp[2][3],dp[1][3])=1+min(1,2,1)=2

max_side=2 → area = 2×2 = 4

Largest square:
  1 1
  1 1   (at rows 2-3, cols 2-3 in 0-indexed matrix)
```

```python
def maximal_square(matrix: list) -> int:
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    # dp[i][j] = side length of largest square ending at (i-1, j-1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_side = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if matrix[i - 1][j - 1] == '1':
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # square from above
                    dp[i][j - 1],      # square from left
                    dp[i - 1][j - 1]   # square from diagonal
                )
                max_side = max(max_side, dp[i][j])
    return max_side * max_side  # Area = side²

# Space-optimized version:
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

# Time: O(m×n), Space: O(n) optimized
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

Given n balloons with numbers. Burst balloon i and get nums[i-1] × nums[i] × nums[i+1] coins. Find max coins.

### Visual Walkthrough

```
nums = [3, 1, 5, 8]

Add sentinels: [1, 3, 1, 5, 8, 1]

Key insight: Think of it as "which balloon is the LAST to burst in a range?"

If balloon k is the LAST to burst in range [l..r]:
  - Before bursting k, balloons in [l..k-1] and [k+1..r] are already gone
  - When k bursts, its neighbors are the sentinels/boundaries at l and r
  - Coins = nums[l] × nums[k] × nums[r]  (k is adjacent to boundaries!)
         + solve(l, k) + solve(k, r)       (burst balloons in left and right sub-ranges)

DP Table for [1, 3, 1, 5, 8, 1]:

  dp[l][r] = max coins from bursting all balloons between l and r (exclusive)

  Length 2: dp[l][l+2] for all valid l (need at least one balloon between)
    dp[0][2] = nums[0]*nums[1]*nums[2] = 1*3*1 = 3   (only balloon 1 to burst)
    dp[1][3] = nums[1]*nums[2]*nums[3] = 3*1*5 = 15  (only balloon 1 to burst)
    dp[2][4] = nums[2]*nums[3]*nums[4] = 1*5*8 = 40
    dp[3][5] = nums[3]*nums[4]*nums[5] = 5*8*1 = 40

  Length 3: dp[l][l+3]
    dp[0][3]: k=1: 1*3*1 + dp[0][1]+dp[1][3] = 3+0+0 = 3
              k=2: 1*1*5 + dp[0][2]+dp[2][3] = 5+3+0 = 8  ← best!
    dp[1][4]: k=2: 3*1*5 + dp[1][2]+dp[2][4] = 15+0+0 = 15
              k=3: 3*5*8 + dp[1][3]+dp[3][4] = 120+15+0 = 135 ← best!

  ...continuing fills dp[0][5] = 167

Answer: 167
```

```python
def max_coins_tab(nums: list) -> int:
    nums = [1] + nums + [1]  # Add sentinel boundaries
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    # Fill by increasing range length
    for length in range(2, n):       # length = gap between boundaries
        for i in range(n - length):  # i = left boundary
            j = i + length           # j = right boundary
            # Try each balloon k as the LAST one to burst in (i, j)
            for k in range(i + 1, j):
                # Bursting k: coins from k + left subproblem + right subproblem
                dp[i][j] = max(dp[i][j],
                               nums[i] * nums[k] * nums[j] + dp[i][k] + dp[k][j])
    return dp[0][n - 1]

# Time: O(n³), Space: O(n²)
# n = len(nums) + 2 (with sentinels)
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

## Summary Table & Quick Reference

```
┌──────────────────────────┬──────────────────────┬──────────┬──────────┬──────────────────────────────┐
│ Problem                  │ Approach             │ Time     │ Space    │ Key Insight                  │
├──────────────────────────┼──────────────────────┼──────────┼──────────┼──────────────────────────────┤
│ L Palindromic Subseq     │ Interval DP          │ O(n²)    │ O(n²)    │ dp[i][j] on s[i..j]         │
│ Shortest Common Super    │ LCS + Backtrack      │ O(m×n)   │ O(m×n)   │ len(a)+len(b)-LCS           │
│ Max Square in Matrix     │ Min of 3 + 1         │ O(m×n)   │ O(n)     │ All 3 neighbors must be big │
│ Max Rectangle            │ Histogram + Stack    │ O(m×n)   │ O(n)     │ Row-by-row height accumulation│
│ Count Squares            │ Sum dp[i][j] values  │ O(m×n)   │ O(m×n)   │ Each cell counts all squares │
│ Burst Balloons           │ Interval O(n³)       │ O(n³)    │ O(n²)    │ "last burst" perspective     │
│ Stone Game III           │ Suffix sum + DP      │ O(n)     │ O(n)     │ suffix[i] - dp[i+take]      │
│ Predict Winner           │ Minimax interval     │ O(n²)    │ O(n²)    │ take - opponent_best         │
└──────────────────────────┴──────────────────────┴──────────┴──────────┴──────────────────────────────┘
```

### Interval DP Pattern (for Burst Balloons, Stone Games, etc.)

```
The standard interval DP template:

  for length in range(2, n+1):          # increasing range size
      for i in range(n - length + 1):   # left boundary
          j = i + length - 1            # right boundary
          for k in range(i, j):         # split point / last element
              dp[i][j] = optimize(dp[i][j], combine(dp[i][k], dp[k+1][j]))

  Fill order ensures subproblems are solved before larger problems.
  Diagonal fill: length=1 → diagonal 0, length=2 → diagonal 1, etc.
```
