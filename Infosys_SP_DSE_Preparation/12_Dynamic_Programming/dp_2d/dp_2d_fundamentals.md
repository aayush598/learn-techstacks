# 2D Dynamic Programming — Fundamentals

## Grid Traversal DP

### Unique Paths

m×n grid. Robot moves right or down. Count paths from top-left to bottom-right.

**Concept:** dp[i][j] = dp[i-1][j] + dp[i][j-1]

```python
def unique_paths_memo(m: int, n: int, i: int = 0, j: int = 0, memo=None) -> int:
    if memo is None:
        memo = {}
    if i == m - 1 and j == n - 1:
        return 1
    if i >= m or j >= n:
        return 0
    key = (i, j)
    if key in memo:
        return memo[key]
    memo[key] = unique_paths_memo(m, n, i + 1, j, memo) + unique_paths_memo(m, n, i, j + 1, memo)
    return memo[key]

def unique_paths_tab(m: int, n: int) -> int:
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]

def unique_paths_optimized(m: int, n: int) -> int:
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    return dp[n - 1]

# DP Table visualization for 3×3:
# [1, 1, 1]
# [1, 2, 3]
# [1, 3, 6]  -> answer = 6

# Time: O(m×n), Space: O(min(m,n))
```

### Unique Paths with Obstacles

Same as above, but some cells are blocked (1).

```python
def unique_paths_with_obstacles_memo(grid: list, i: int = 0, j: int = 0, memo=None) -> int:
    if memo is None:
        memo = {}
    m, n = len(grid), len(grid[0])
    if i >= m or j >= n or grid[i][j] == 1:
        return 0
    if i == m - 1 and j == n - 1:
        return 1
    key = (i, j)
    if key in memo:
        return memo[key]
    memo[key] = unique_paths_with_obstacles_memo(grid, i + 1, j, memo) + \
                unique_paths_with_obstacles_memo(grid, i, j + 1, memo)
    return memo[key]

def unique_paths_with_obstacles_tab(grid: list) -> int:
    m, n = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[m - 1][n - 1] == 1:
        return 0
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                dp[i][j] = 0
            else:
                if i > 0:
                    dp[i][j] += dp[i - 1][j]
                if j > 0:
                    dp[i][j] += dp[i][j - 1]
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

**Concept:** if a[i] == b[j]: dp[i][j] = dp[i-1][j-1] + 1 else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])

```python
def lcs_memo(a: str, b: str, i: int = None, j: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if i is None:
        return lcs_memo(a, b, len(a) - 1, len(b) - 1, memo)
    if i < 0 or j < 0:
        return 0
    key = (i, j)
    if key in memo:
        return memo[key]
    if a[i] == b[j]:
        memo[key] = 1 + lcs_memo(a, b, i - 1, j - 1, memo)
    else:
        memo[key] = max(lcs_memo(a, b, i - 1, j, memo),
                        lcs_memo(a, b, i, j - 1, memo))
    return memo[key]

def lcs_tab(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

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

# DP Table: a = "abcde", b = "ace"
#   0 a c e
# 0 0 0 0 0
# a 0 1 1 1
# b 0 1 1 1
# c 0 1 2 2
# d 0 1 2 2
# e 0 1 2 3  -> answer = 3

# Time: O(m×n), Space: O(min(m,n))
```

### LCS: Reconstruct the subsequence

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
    i, j = m, n
    chars = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            chars.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return ''.join(reversed(chars))
```

---

## Edit Distance (Levenshtein)

Given two strings, find min number of operations (insert, delete, replace) to convert one to another.

**Concept:** if a[i] == b[j]: dp[i][j] = dp[i-1][j-1] else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

```python
def edit_distance_memo(a: str, b: str, i: int = None, j: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if i is None:
        return edit_distance_memo(a, b, len(a) - 1, len(b) - 1, memo)
    if i < 0:
        return j + 1
    if j < 0:
        return i + 1
    key = (i, j)
    if key in memo:
        return memo[key]
    if a[i] == b[j]:
        memo[key] = edit_distance_memo(a, b, i - 1, j - 1, memo)
    else:
        memo[key] = 1 + min(edit_distance_memo(a, b, i - 1, j, memo),
                            edit_distance_memo(a, b, i, j - 1, memo),
                            edit_distance_memo(a, b, i - 1, j - 1, memo))
    return memo[key]

def edit_distance_tab(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]

def edit_distance_optimized(a: str, b: str) -> int:
    m, n = len(a), len(b)
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev, curr = curr, [0] * (n + 1)
    return prev[n]

# DP Table: a = "horse", b = "ros"
#   0 r o s
# 0 0 1 2 3
# h 1 1 2 3
# o 2 2 1 2
# r 3 2 2 2
# s 4 3 3 2
# e 5 4 4 3  -> answer = 3

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

## Summary Table

| Problem | Approach | Time | Space |
|---------|----------|------|-------|
| Unique Paths | Combinatorial | O(m×n) | O(1) |
| Unique Paths w/ Obstacles | 2D DP | O(m×n) | O(m×n) |
| Min Path Sum | 2D DP + min | O(m×n) | O(n) |
| Dungeon Game | Reverse DP | O(m×n) | O(m×n) |
| Triangle Path | Bottom-up in-place | O(n²) | O(n) |
| LCS | Match/max DP | O(m×n) | O(min(m,n)) |
| Edit Distance | Insert/Delete/Replace | O(m×n) | O(min(m,n)) |
| L Common Substring | Reset on mismatch | O(m×n) | O(m×n) |
| Distinct Subsequences | DP with inclusion | O(m×n) | O(m×n) |
| Interleaving String | Boolean DP | O(m×n) | O(m×n) |
