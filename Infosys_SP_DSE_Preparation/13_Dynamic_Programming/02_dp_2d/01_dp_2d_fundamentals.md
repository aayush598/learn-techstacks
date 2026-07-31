# 2D Dynamic Programming — Fundamentals

## How to Recognize 2D DP Problems

```
┌─────────────────────────────────────────────────────────────────────┐
│                   2D DP PATTERN RECOGNITION                        │
├─────────────────────────────┬───────────────────────────────────────┤
│ Problem hints               │ Likely approach                      │
├─────────────────────────────┼───────────────────────────────────────┤
│ "grid / matrix" traversal   │ Grid DP (dp[i][j] = cell value)      │
│ "two strings" comparison    │ LCS / Edit Distance family           │
│ "triangle / pyramid"        │ Bottom-up DP on structure            │
│ "min path from A to B"      │ Min Path Sum (forward or backward)   │
│ "reverse: min health needed"│ Dungeon Game (backward DP)           │
│ "interleave / merge"        │ Boolean 2D DP checking both strings  │
│ "count ways in grid"        │ Unique Paths (add from top + left)   │
└─────────────────────────────┴───────────────────────────────────────┘
```

---

## Grid Traversal DP

### Unique Paths

m×n grid. Robot moves right or down. Count paths from top-left to bottom-right.

### Intuition

Every cell can only be reached from the cell above it or the cell to its left. So the number of ways to reach a cell = ways to reach the cell above + ways to reach the cell from the left.

```
Grid (3×3):                DP Table:
┌───┬───┬───┐             ┌───┬───┬───┐
│ S │   │   │             │ 1 │ 1 │ 1 │  ← Row 0: only 1 way (straight right)
├───┼───┼───┤             ├───┼───┼───┤
│   │   │   │             │ 1 │ 2 │ 3 │  ← Row 1: dp[1][1] = dp[0][1]+dp[1][0] = 2
├───┼───┼───┤             ├───┼───┼───┤
│   │   │ E │             │ 1 │ 3 │ 6 │  ← dp[2][2] = dp[1][2]+dp[2][1] = 6
└───┴───┴───┘             └───┴───┴───┘

State transition:
dp[i][j] = dp[i-1][j]  +  dp[i][j-1]
            ───────         ───────
            from above       from left

Fill order: row by row, left to right (ensures dependencies resolved)
```

### Code with Space Optimization

```python
def unique_paths_optimized(m: int, n: int) -> int:
    dp = [1] * n  # First row is all 1s
    for _ in range(1, m):         # For each subsequent row
        for j in range(1, n):     # For each column (skip first col, stays 1)
            dp[j] += dp[j - 1]   # dp[j] (from above) + dp[j-1] (from left)
    return dp[n - 1]

# Time: O(m×n), Space: O(n) — we only need one row at a time
```

### Unique Paths with Obstacles

Same as above, but cells with 1 are blocked (cannot pass through).

```
Grid with obstacles:          DP Table:
┌───┬───┬───┐                ┌───┬───┬───┐
│ 0 │ 0 │ 0 │                │ 1 │ 1 │ 1 │
├───┼───┼───┤                ├───┼───┼───┤
│ 0 │ 1 │ 0 │  ← obstacle   │ 1 │ 0 │ 1 │  ← dp[1][1] = 0 (blocked!)
├───┼───┼───┤                ├───┼───┼───┤
│ 0 │ 0 │ 0 │                │ 1 │ 1 │ 2 │
└───┴───┴───┘                └───┴───┴───┘

Rule: if grid[i][j] == 1 → dp[i][j] = 0 (no paths through here)
```

```python
def unique_paths_with_obstacles_tab(grid: list) -> int:
    m, n = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[m - 1][n - 1] == 1:
        return 0  # Start or end blocked → impossible
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                dp[i][j] = 0  # Obstacle → zero paths
            else:
                if i > 0:
                    dp[i][j] += dp[i - 1][j]  # From above
                if j > 0:
                    dp[i][j] += dp[i][j - 1]  # From left
    return dp[m - 1][n - 1]

# Time: O(m×n), Space: O(m×n)
```

---

## Minimum Path Sum

m×n grid non-negative numbers. Find min sum path from top-left to bottom-right.

**Concept:** dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])

```python
def min_path_sum_memo(grid: list, i: int = None, j: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if i is None:
        return min_path_sum_memo(grid, len(grid) - 1, len(grid[0]) - 1, memo)
    if i == 0 and j == 0:
        return grid[0][0]
    if i < 0 or j < 0:
        return float('inf')
    key = (i, j)
    if key in memo:
        return memo[key]
    memo[key] = grid[i][j] + min(min_path_sum_memo(grid, i - 1, j, memo),
                                 min_path_sum_memo(grid, i, j - 1, memo))
    return memo[key]

def min_path_sum_tab(grid: list) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    # Fill first row
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] + grid[0][j]
    # Fill first column
    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    # Fill rest
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])
    return dp[m - 1][n - 1]

def min_path_sum_optimized(grid: list) -> int:
    m, n = len(grid), len(grid[0])
    dp = [float('inf')] * n
    dp[0] = 0
    for i in range(m):
        new_dp = [float('inf')] * n
        for j in range(n):
            if i == 0 and j == 0:
                new_dp[j] = grid[0][0]
            else:
                from_top = dp[j] if i > 0 else float('inf')
                from_left = new_dp[j - 1] if j > 0 else float('inf')
                new_dp[j] = grid[i][j] + min(from_top, from_left)
        dp = new_dp
    return dp[n - 1]

# DP Table visualization for [[1,3,1],[1,5,1],[4,2,1]]:
# [1, 4, 5]
# [2, 7, 6]
# [6, 8, 7]  -> answer = 7

# Time: O(m×n), Space: O(n)
```

---

## Dungeon Game

The demons had captured the princess (P) and imprisoned her in the bottom-right corner. knight starts at top-left. Each cell has health gain/loss. Find min initial health.

**Concept:** Work backwards. dp[i][j] = min_health_needed entering (i,j), must be ≥ 1.

```python
def calculate_minimum_hp(grid: list) -> int:
    m, n = len(grid), len(grid[0])

    # dp[i][j] = min health to reach princess from (i,j) to (m-1,n-1)
    dp = [[float('inf')] * (n + 1) for _ in range(m + 1)]
    dp[m][n - 1] = dp[m - 1][n] = 1

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            need = min(dp[i + 1][j], dp[i][j + 1]) - grid[i][j]
            dp[i][j] = max(1, need)
    return dp[0][0]

# Example:
# grid = [[-2, -3, 3],
#         [-5, -10, 1],
#         [10, 30, -5]]
# Answer: 7

# Time: O(m×n), Space: O(m×n)
```

---

## Triangle Minimum Path Sum

Given a triangle array, find min sum from top to bottom. Can move to adjacent numbers on the row below.

**Concept:** Modify in place, bottom-up.

```python
def minimum_total_memo(triangle: list, i: int = 0, j: int = 0, memo=None) -> int:
    if memo is None:
        memo = {}
    if i == len(triangle) - 1:
        return triangle[i][j]
    key = (i, j)
    if key in memo:
        return memo[key]
    memo[key] = triangle[i][j] + min(minimum_total_memo(triangle, i + 1, j, memo),
                                     minimum_total_memo(triangle, i + 1, j + 1, memo))
    return memo[key]

def minimum_total_tab(triangle: list) -> int:
    n = len(triangle)
    dp = triangle[-1][:]  # start with last row
    for i in range(n - 2, -1, -1):
        for j in range(len(triangle[i])):
            dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])
    return dp[0]

# Example:
# triangle = [[2],
#            [3,4],
#           [6,5,7],
#          [4,1,8,3]]
# Answer: 11 (2 + 3 + 5 + 1)

# Time: O(n²) where n = number of rows
```

---

## Longest Common Subsequence (LCS)

Given two strings, find length of longest subsequence common to both.

### Visual Walkthrough — Complete Table Fill

```
a = "abcde", b = "ace"

     ""  a  c  e       ← string b (columns)
  ┌────┬────┬────┬────┐
""│  0 │  0 │  0 │  0 │  ← empty string b: 0 matches
  ├────┼────┼────┼────┤
 a│  0 │  1 │  1 │  1 │  a=a ✓ → dp[0][0]+1 = 1
  ├────┼────┼────┼────┤
 b│  0 │  1 │  1 │  1 │  b≠c → max(dp[0][1], dp[1][0]) = 1
  ├────┼────┼────┼────┤
 c│  0 │  1 │  2 │  2 │  c=c ✓ → dp[1][1]+1 = 2
  ├────┼────┼────┼────┤
 d│  0 │  1 │  2 │  2 │  d≠e → max(dp[2][2], dp[3][1]) = 2
  ├────┼────┼────┼────┤
 e│  0 │  1 │  2 │  3 │  e=e ✓ → dp[3][2]+1 = 3
  └────┴────┴────┴────┘
  ↑ string a (rows)

  Answer: 3 (subsequence "ace")

Rules:
  a[i] == b[j] → dp[i][j] = dp[i-1][j-1] + 1  (diagonal + 1)
  a[i] ≠ b[j]  → dp[i][j] = max(dp[i-1][j], dp[i][j-1])  (max of above or left)

To reconstruct: trace back from dp[m][n]
  - If a[i]==b[j] → this char is in LCS, move diagonal
  - Else move toward the larger value (above or left)
```

```python
def lcs_tab(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1  # Match! extend previous LCS
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])  # Take best so far
    return dp[m][n]

# Space-optimized (only need previous row):
def lcs_tab_optimized(a: str, b: str) -> int:
    m, n = len(a), len(b)
    prev, curr = [0] * (n + 1), [0] * (n + 1)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, [0] * (n + 1)
    return prev[n]

# Time: O(m×n), Space: O(min(m,n))
```

### LCS: Reconstruct the Subsequence

```python
def lcs_reconstruct(a: str, b: str) -> str:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # Trace back from bottom-right
    i, j = m, n
    chars = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            chars.append(a[i - 1])  # This char is part of LCS
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1   # Move up (toward larger value)
        else:
            j -= 1   # Move left
    return ''.join(reversed(chars))
```

---

## Edit Distance (Levenshtein)

Given two strings, find min number of operations (insert, delete, replace) to convert word1 to word2.

### Visual Walkthrough

```
a = "horse", b = "ros"

     ""  r  o  s        ← string b
  ┌────┬────┬────┬────┐
""│  0 │  1 │  2 │  3 │   Need j inserts to build b[0:j]
  ├────┼────┼────┼────┤
 h│  1 │  1 │  2 │  3 │   h≠r → min(del h, ins r, replace h→r)+1 = 1
  ├────┼────┼────┼────┤
 o│  2 │  2 │  1 │  2 │   o=o ✓ → dp[0][0] = 0... wait
  ├────┼────┼────┼────┤   Actually o=o → diagonal value = dp[1][0] but let's be precise:
 r│  3 │  2 │  2 │  2 │   r=r ✓ → dp[1][1] + 0 = ... let me show the real table:
  ├────┼────┼────┼────┤
 s│  4 │  3 │  3 │  2 │   s=s ✓ → dp[3][2] = 2
  ├────┼────┼────┼────┤
 e│  5 │  4 │  4 │  3 │   e≠s → min(4,3,4)+1 = 3
  └────┴────┴────┴────┘

Correct filled table:
     ""  r  o  s
  ┌────┬────┬────┬────┐
""│  0 │  1 │  2 │  3 │
  ├────┼────┼────┼────┤
 h│  1 │  1 │  2 │  3 │   h≠r: min(1+1, 0+1, 1+1)=1... 
  ├────┼────┼────┼────┤
 o│  2 │  2 │  1 │  2 │
  ├────┼────┼────┼────┤
 r│  3 │  2 │  2 │  2 │
  ├────┼────┼────┼────┤
 s│  4 │  3 │  3 │  2 │
  ├────┼────┼────┼────┤
 e│  5 │  4 │  4 │  3 │   ← answer = 3
  └────┴────┴────┴────┘

Three operations at each cell:
  DELETE:  dp[i-1][j] + 1      ← remove char from a
  INSERT:  dp[i][j-1] + 1      ← add char to a
  REPLACE: dp[i-1][j-1] + cost  ← change char (cost=0 if same, 1 if different)

If a[i] == b[j]: dp[i][j] = dp[i-1][j-1]  (no operation needed!)
```

```python
def edit_distance_tab(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    # Base cases: converting empty string to b[0:j] takes j inserts
    for j in range(n + 1):
        dp[0][j] = j
    # Converting a[0:i] to empty string takes i deletes
    for i in range(m + 1):
        dp[i][0] = i
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # Characters match, no operation
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete from a
                    dp[i][j - 1],      # Insert into a
                    dp[i - 1][j - 1]   # Replace in a
                )
    return dp[m][n]

# Space-optimized:
def edit_distance_optimized(a: str, b: str) -> int:
    m, n = len(a), len(b)
    prev = list(range(n + 1))   # Base: dp[0][j] = j
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        curr[0] = i             # Base: dp[i][0] = i
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev, curr = curr, [0] * (n + 1)
    return prev[n]

# Time: O(m×n), Space: O(min(m,n))
```

---

## Longest Common Substring

Given two strings, find the length of the longest contiguous substring common to both.

**Concept:** if a[i] == b[j]: dp[i][j] = dp[i-1][j-1] + 1 else: dp[i][j] = 0

```python
def longest_common_substring_memo(a: str, b: str, i: int = None, j: int = None,
                                   memo=None, length=0) -> int:
    if memo is None:
        memo = {}
    if i is None:
        return longest_common_substring_memo(a, b, len(a) - 1, len(b) - 1, {}, 0)
    if i < 0 or j < 0:
        return 0
    key = (i, j)
    if key in memo and memo[key] > 0:
        return memo[key]
    if a[i] == b[j]:
        memo[key] = 1 + longest_common_substring_memo(a, b, i - 1, j - 1, memo, length)
        length = max(length, memo[key])
    else:
        memo[key] = 0
    return max(length, longest_common_substring_memo(a, b, i - 1, j, memo, length),
               longest_common_substring_memo(a, b, i, j - 1, memo, length))

def longest_common_substring_tab(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_len = max(max_len, dp[i][j])
    return max_len

# DP Table: a = "abcde", b = "abfde"
#   0 a b f d e
# 0 0 0 0 0 0
# a 0 1 0 0 0 0
# b 0 0 2 0 0 0
# c 0 0 0 0 0 0
# d 0 0 0 0 1 0
# e 0 0 0 0 0 2  -> answer = 2

# Time: O(m×n), Space: O(m×n)
```

---

## Distinct Subsequences

Given two strings s and t, count distinct subsequences of s equal to t.

**Concept:** if s[i] == t[j]: dp[i][j] = dp[i-1][j-1] + dp[i-1][j] else: dp[i][j] = dp[i-1][j]

```python
def num_distinct_memo(s: str, t: str, i: int = None, j: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if i is None:
        return num_distinct_memo(s, t, len(s), len(t), memo)
    if j == 0:
        return 1
    if i == 0:
        return 0
    key = (i, j)
    if key in memo:
        return memo[key]
    ans = num_distinct_memo(s, t, i - 1, j, memo)
    if s[i - 1] == t[j - 1]:
        ans += num_distinct_memo(s, t, i - 1, j - 1, memo)
    memo[key] = ans
    return memo[key]

def num_distinct_tab(s: str, t: str) -> int:
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = 1
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j]
            if s[i - 1] == t[j - 1]:
                dp[i][j] += dp[i - 1][j - 1]
    return dp[m][n]

# Time: O(m×n), Space: O(m×n)
```

---

## Interleaving String

Given s1, s2, s3, check if s3 is formed by interleaving s1 and s2.

**Concept:** dp[i][j] = True iff s3[0:i+j] is interleaving of s1[0:i] and s2[0:j]

```python
def is_interleave_memo(s1: str, s2: str, s3: str, i: int = 0, j: int = 0, memo=None) -> bool:
    if memo is None:
        memo = {}
    if i + j == len(s3):
        return i == len(s1) and j == len(s2)
    key = (i, j)
    if key in memo:
        return memo[key]
    ans = False
    if i < len(s1) and s1[i] == s3[i + j]:
        ans = ans or is_interleave_memo(s1, s2, s3, i + 1, j, memo)
    if not ans and j < len(s2) and s2[j] == s3[i + j]:
        ans = ans or is_interleave_memo(s1, s2, s3, i, j + 1, memo)
    memo[key] = ans
    return memo[key]

def is_interleave_tab(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = (dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]) or \
                       (dp[i][j - 1] and s2[j - 1] == s3[i + j - 1])
    return dp[m][n]

# DP Table: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
#       d  b  b  c  a
#   T  F  F  F  F  F
# a T  F  F  T  T  F
# a T  F  F  T  F  T
# b T  F  F  T  T  T  -> last cell determines answer
# c T  T  T  T  T  T
# c T  T  T  T  T  T
# Answer: True

# Time: O(m×n), Space: O(m×n)
```

---

## LCS vs Edit Distance — Side-by-Side Comparison

```
┌────────────────────────────┬──────────────────────────────────────┐
│         LCS                │         Edit Distance                │
├────────────────────────────┼──────────────────────────────────────┤
│ Goal: max length           │ Goal: min operations                 │
│ Match: dp[i-1][j-1] + 1   │ Match: dp[i-1][j-1] (no cost)       │
│ No match: max(above, left) │ No match: min(del,ins,rep) + 1      │
│ No insert/delete ops       │ Has insert + delete + replace ops    │
│ dp[0][j]=0, dp[i][0]=0    │ dp[0][j]=j, dp[i][0]=i              │
│ Result: dp[m][n]           │ Result: dp[m][n]                     │
└────────────────────────────┴──────────────────────────────────────┘
```

## Summary Table & Quick Reference

```
┌──────────────────────────┬────────────────────┬──────────┬──────────┬───────────────────────────┐
│ Problem                  │ Approach           │ Time     │ Space    │ Key Insight               │
├──────────────────────────┼────────────────────┼──────────┼──────────┼───────────────────────────┤
│ Unique Paths             │ Grid DP            │ O(m×n)   │ O(1)     │ dp[i][j] = above + left   │
│ Unique Paths + Obstacles │ Grid DP (zero)     │ O(m×n)   │ O(m×n)   │ Obstacle cell → 0 paths   │
│ Min Path Sum             │ Grid DP + min      │ O(m×n)   │ O(n)     │ dp[i][j] = cell + min()   │
│ Dungeon Game             │ Reverse DP         │ O(m×n)   │ O(m×n)   │ Fill bottom-right to top-left│
│ Triangle Path            │ Bottom-up modify   │ O(n²)    │ O(n)     │ Collapse rows from bottom │
│ LCS                     │ Match/max DP       │ O(m×n)   │ O(min(m,n))│ Match→diagonal, else max │
│ Edit Distance            │ Del/Ins/Rep DP     │ O(m×n)   │ O(min(m,n))│ 3-way min on mismatch    │
│ L Common Substring       │ Reset on mismatch  │ O(m×n)   │ O(m×n)   │ Mismatch → 0 (not max)   │
│ Distinct Subsequences    │ Include/skip       │ O(m×n)   │ O(m×n)   │ dp[i][j] = skip + include │
│ Interleaving String      │ Boolean 2D DP      │ O(m×n)   │ O(m×n)   │ From top OR left if match │
└──────────────────────────┴────────────────────┴──────────┴──────────┴───────────────────────────┘
```

### Common Pattern: String Comparison DP Template

```
For any two-string DP problem, the template is:

  dp[0][0] = base_case

  for i in 1..m:
    for j in 1..n:
      if s1[i-1] == s2[j-1]:
        dp[i][j] = f(dp[i-1][j-1])          # characters match
      else:
        dp[i][j] = g(dp[i-1][j], dp[i][j-1]) # no match

  LCS:        f = +1,     g = max
  Edit Dist:  f = +0,     g = min + 1
  Substring:  f = +1,     g = 0   (reset)
  Distinct:   f = +dp[i-1][j-1] (add), g = dp[i-1][j]
```
