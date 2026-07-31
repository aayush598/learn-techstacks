# 11. Dynamic Programming Cheatsheet

The highest-value file for coding round prep. Every template gives: state definition `dp[i]` meaning, recurrence, base case, complexity, and copy-paste Python 3 code. All code verified.

## DP Fundamentals

### Memoization vs Tabulation

| | Memoization (top-down) | Tabulation (bottom-up) |
|---|---|---|
| Direction | Start from the target, recurse down to base | Fill from base up to target |
| Code style | Recursion + `@lru_cache` / dict | Iteration + array/table |
| Dependencies | Only computes states actually needed | Computes all states in the table |
| Risk | Recursion limit; hashability of args | Getting iteration order right |
| Use when | Sparse state space, complex transitions | Dense table, easy order |

### How to identify DP (and which table row applies)

1. **Overlapping subproblems** — the brute-force recursion recomputes the same sub-calls.
2. **Optimal substructure** — the optimal answer composes from optimal answers of subproblems.
3. Identify the **state** = the minimal set of variables that fully determines a subproblem. `dp[i]` (1D), `dp[i][j]` (2D), `dp[mask]` (bitmask), `dp[node]` (trees).
4. Write the **recurrence** in terms of strictly-smaller states, then define **base cases**.

### 1D Space-Optimization Pattern

When `dp[i]` only depends on `dp[i-1]`, `dp[i-2]` (or a window of size k), replace the array with k rolling variables. This cuts memory from O(n) to O(k) — the interviewer's favorite follow-up.

## The 1D "Linear Sequence" Templates

### Fibonacci

```python
def fib(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

- **State:** `dp[i]` = i-th Fibonacci number. **Base:** `dp[0]=0, dp[1]=1`. **Recurrence:** `dp[i] = dp[i-1] + dp[i-2]`.
- **Complexity:** O(n) time, O(1) space (rolling two variables).

### Climbing Stairs

```python
def climb_stairs(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

assert climb_stairs(5) == 8
```

- **State:** `dp[i]` = number of distinct ways to reach step i (steps 1 or 2 at a time).
- **Base:** `dp[1]=1, dp[2]=2`. **Recurrence:** `dp[i] = dp[i-1] + dp[i-2]` (last move was 1 step or 2 steps).
- **Complexity:** O(n) time, O(1) space.

### House Robber (cannot take adjacent)

```python
def rob(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    prev2, prev1 = 0, nums[0]           # dp[i-2], dp[i-1]
    for i in range(1, len(nums)):
        prev2, prev1 = prev1, max(prev1, prev2 + nums[i])
    return prev1

assert rob([2, 7, 9, 3, 1]) == 12
assert rob([2, 1, 1, 2]) == 4
```

- **State:** `dp[i]` = max money robbing houses `0..i`. **Base:** `dp[0]=nums[0]`, `dp[-1]=0`.
- **Recurrence:** `dp[i] = max(dp[i-1], nums[i] + dp[i-2])` — skip house i, or rob it and skip i-1.
- **Complexity:** O(n) time, O(1) space. Circular variant: run `rob(nums[1:])` vs `rob(nums[:-1])`, take max.

### Coin Change (minimum coins)

```python
def coin_change(coins, amount):
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i], dp[i - c] + 1)
    return dp[amount] if dp[amount] != float("inf") else -1

assert coin_change([1, 2, 5], 11) == 3   # 5+5+1
assert coin_change([2], 3) == -1
```

- **State:** `dp[i]` = min coins to make amount i. **Base:** `dp[0]=0`, others `inf`.
- **Recurrence:** `dp[i] = min(dp[i], dp[i-c] + 1)` for each coin c.
- **Complexity:** O(amount × len(coins)) time, O(amount) space.
- Unbounded problem → looping `i` in **forward** order inside each coin is fine; order of `i` vs `c` loops is irrelevant for the **min** (ways version below is order-sensitive).

### Coin Change 2 (number of ways) — UNBOUNDED, coin-loop OUTSIDE

```python
def coin_change_ways(coins, amount):
    dp = [0] * (amount + 1)
    dp[0] = 1
    for c in coins:                     # coin loop OUTER
        for i in range(c, amount + 1):  # forward direction
            dp[i] += dp[i - c]
    return dp[amount]

assert coin_change_ways([1, 2, 5], 5) == 4   # {5},{2+2+1},{2+1+1+1},{1*5}
```

- **State:** `dp[i]` = number of coin combinations that sum to i.
- **Recurrence:** `dp[i] += dp[i - c]`.
- **Complexity:** O(amount × len(coins)) time, O(amount) space.
- **CRITICAL iteration-direction rules:**
  - **Ways (combinations), unbounded:** coins outer, `range(c, amount+1)` forward → each combination counted once.
  - **Permutations of coins (order matters, e.g. "coin change #377"):** amount outer, inner coin loop.
  - **0/1 knapsack:** single item use → **reverse** inner loop.

## Knapsack

### 0/1 Knapsack — 2D table

```python
def knapsack_2d(weights, values, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for cap in range(W + 1):
            if cap >= w:
                dp[i][cap] = max(dp[i - 1][cap], dp[i - 1][cap - w] + v)
            else:
                dp[i][cap] = dp[i - 1][cap]
    return dp[n][W]

assert knapsack_2d([2, 3, 4, 5], [3, 4, 5, 6], 5) == 7   # items 1 (w2) + 2 (w3)
```

- **State:** `dp[i][cap]` = max value using first i items within capacity cap.
- **Base:** row/col 0 = 0. **Recurrence:** `dp[i][cap] = max(dp[i-1][cap], dp[i-1][cap-w] + v)`.
- **Complexity:** O(n·W) time, O(n·W) space.

### 0/1 Knapsack — 1D rolling array (REVERSE loop)

```python
def knapsack_1d(weights, values, W):
    dp = [0] * (W + 1)
    for w, v in zip(weights, values):
        for cap in range(W, w - 1, -1):     # REVERSE: each item used once
            dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[W]

assert knapsack_1d([2, 3, 4, 5], [3, 4, 5, 6], 5) == 7
```

- **State:** `dp[cap]` = max value within capacity cap using processed items.
- **Why reverse?** The recurrence reads `dp[cap - w]` from the *previous* item's row. Reverse order guarantees we never update the same item's row into itself (which would allow reuse = unbounded).
- **Complexity:** O(n·W) time, O(W) space.

### Unbounded Knapsack — FORWARD loop (each item unlimited)

```python
def unbounded_knapsack(weights, values, W):
    dp = [0] * (W + 1)
    for w, v in zip(weights, values):
        for cap in range(w, W + 1):          # FORWARD: reuse allowed
            dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[W]

assert unbounded_knapsack([1, 2], [1, 3], 4) == 6   # 2+2
```

- **Memory rule:** reverse loop = 0/1 (each item at most once); forward loop = unbounded (item reusable). This is the single most-tested iteration-direction detail — memorize it.

## Longest Increasing Subsequence (LIS)

### O(n log n) — patience-sort tails array (interview gold)

```python
from bisect import bisect_left

def length_of_lis(nums):
    tails = []                          # tails[i] = min tail of an increasing subseq of length i+1
    for x in nums:
        i = bisect_left(tails, x)       # first index where tails[i] >= x
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x                # replace: strictly better tail
    return len(tails)

assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4
```

- **State:** `tails` array; invariant — sorted, `tails[i]` = smallest possible ending value of an increasing subsequence of length `i+1`.
- **Binary search:** `bisect_left` → strictly increasing LIS (length 4 above); **`bisect_right` → non-decreasing LIS** (allows equal elements).

```python
from bisect import bisect_right

def length_of_lis_non_decreasing(nums):
    tails = []
    for x in nums:
        i = bisect_right(tails, x)      # allow equal -> non-decreasing
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)

assert length_of_lis_non_decreasing([2, 2, 2]) == 3
```

- **Complexity:** O(n log n) time, O(n) space. The O(n²) `dp[i] = max(dp[j]+1 for j<i if nums[j]<nums[i])` version is the fallback and also reconstructs the sequence.

## Longest Common Subsequence (LCS)

### Length + reconstruction

```python
def lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

assert lcs("abcde", "ace") == 3
assert lcs("AGGTAB", "GXTXAYB") == 4
```

```python
def lcs_string(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # reconstruct by walking back from dp[m][n]
    i, j = m, n
    chars = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            chars.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(chars))

assert lcs_string("abcde", "ace") == "ace"
```

- **State:** `dp[i][j]` = LCS length of prefixes `a[:i]`, `b[:j]`.
- **Base:** first row/col = 0. **Recurrence:** match → `dp[i-1][j-1] + 1`; mismatch → `max(dp[i-1][j], dp[i][j-1])`.
- **Complexity:** O(m·n) time, O(m·n) space (O(min(m,n)) with rolling rows).

## Edit Distance (Levenshtein)

```python
def edit_distance(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i                  # delete all of a
    for j in range(n + 1):
        dp[0][j] = j                  # insert all of b
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]              # no op
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],        # delete a[i-1]
                    dp[i][j - 1],        # insert b[j-1]
                    dp[i - 1][j - 1],    # replace
                )
    return dp[m][n]

assert edit_distance("horse", "ros") == 3
assert edit_distance("intention", "execution") == 5
```

- **State:** `dp[i][j]` = min ops to turn `a[:i]` into `b[:j]`.
- **Base:** converting to empty string = delete everything / insert everything.
- **Complexity:** O(m·n) time, O(m·n) space.

## Palindromic Problems

### Longest Palindromic Substring

```python
def longest_palindrome(s):
    n = len(s)
    if n < 2:
        return s
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1
    for i in range(n):
        dp[i][i] = True                       # length 1
    for i in range(n - 1):
        if s[i] == s[i + 1]:                  # length 2
            dp[i][i + 1] = True
            start, max_len = i, 2
    for length in range(3, n + 1):            # length >= 3
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                start, max_len = i, length
    return s[start:start + max_len]

assert longest_palindrome("babad") in ("bab", "aba")
assert longest_palindrome("cbbd") == "bb"
```

- **State:** `dp[i][j]` = True if `s[i:j+1]` is a palindrome.
- **Base:** single chars, double chars. **Recurrence:** `dp[i][j] = s[i]==s[j] and dp[i+1][j-1]`.
- **Iterate by increasing length** (window size), not by i — guarantees `dp[i+1][j-1]` is filled.
- **Complexity:** O(n²) time, O(n²) space. (Alternative O(n²)/O(1) expand-around-center is equally accepted.)

### Longest Palindromic Subsequence

```python
def longest_pal_subseq(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]

assert longest_pal_subseq("bbbab") == 4   # "bbbb"
assert longest_pal_subseq("cbbd") == 2
```

- **State:** `dp[i][j]` = longest palindromic subsequence of `s[i:j+1]`.
- **Recurrence:** equal ends → `dp[i+1][j-1] + 2`; else `max(dp[i+1][j], dp[i][j-1])` (drop one end).
- **Complexity:** O(n²) time, O(n²) space. Alternate view: LPS(s) = LCS(s, reversed(s)).

## Subset-Sum Style: Partition Equal Subset Sum

```python
def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for s in range(target, x - 1, -1):    # REVERSE: 0/1 style
            dp[s] = dp[s] or dp[s - x]
    return dp[target]

assert can_partition([1, 5, 11, 5])          # True: {1,5,5} + {11}
assert not can_partition([1, 2, 3, 5])
```

- **Reduction:** split exists ⇔ a subset sums to `total/2`. This is 0/1 knapsack with weights=nums and target capacity.
- **State:** `dp[s]` = subset with sum s reachable. **Base:** `dp[0]=True`.
- **Complexity:** O(n·total/2) time, O(total/2) space. Remember the reverse loop.

## Word Break

```python
def word_break(s, word_dict):
    words = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[n]

assert word_break("leetcode", ["leet", "code"])
assert not word_break("catsandog", ["cats", "dog", "sand", "and", "cat"])
```

- **State:** `dp[i]` = prefix `s[:i]` is segmentable into dictionary words.
- **Base:** `dp[0]=True`. **Recurrence:** `dp[i] = any(dp[j] and s[j:i] in words for j < i)`.
- **Complexity:** O(n² · avg-word-len) time, O(n) space.

## Decode Ways

```python
def num_decodings(s):
    if not s or s[0] == "0":
        return 0
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    for i in range(2, n + 1):
        one = int(s[i - 1:i])
        two = int(s[i - 2:i])
        if 1 <= one <= 9:
            dp[i] += dp[i - 1]      # decode last single digit
        if 10 <= two <= 26:
            dp[i] += dp[i - 2]      # decode last two digits
    return dp[n]

assert num_decodings("12") == 2
assert num_decodings("226") == 3
assert num_decodings("06") == 0
```

- **State:** `dp[i]` = ways to decode prefix `s[:i]`.
- **Base:** `dp[0]=dp[1]=1` (when `s[0] != "0"`).
- **Recurrence:** single-digit 1–9 contributes `dp[i-1]`; two-digit 10–26 contributes `dp[i-2]`.
- **Complexity:** O(n) time, O(n) space (can roll to two vars).

## Grid DP

### Unique Paths (1D space optimization)

```python
def unique_paths(m, n):
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]      # top + left
    return dp[n - 1]

assert unique_paths(3, 7) == 28
```

- **State:** `dp[j]` = paths to current row's cell j. **Recurrence:** `dp[j] += dp[j-1]` (top + left).
- **Complexity:** O(m·n) time, O(n) space (full 2D O(m·n) is equally fine).

### Unique Paths II (with obstacles) — 1D

```python
def unique_paths_obstacles(grid):
    if not grid or not grid[0] or grid[0][0] == 1:
        return 0
    rows, cols = len(grid), len(grid[0])
    dp = [0] * cols
    dp[0] = 1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                dp[c] = 0
            elif c > 0:
                dp[c] += dp[c - 1]
    return dp[cols - 1]

assert unique_paths_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
```

- Obstacle cell → force `dp[c] = 0`. Recurrence otherwise identical.

### Minimum Path Sum

```python
def min_path_sum(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    dp = [float("inf")] * cols
    dp[0] = 0
    for r in range(rows):
        for c in range(cols):
            if c == 0:
                dp[c] += grid[r][c]                 # only from above
            else:
                dp[c] = min(dp[c], dp[c - 1]) + grid[r][c]  # top vs left
    return dp[cols - 1]

assert min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
```

- **State:** `dp[j]` = min sum to reach cell j of current row. **Complexity:** O(m·n) time, O(n) space.

### Maximal Square

```python
def maximal_square(matrix):
    if not matrix:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    dp = [0] * (cols + 1)
    max_side = 0
    prev = 0
    for r in range(rows):
        for c in range(cols):
            temp = dp[c + 1]
            if matrix[r][c] == "1":
                dp[c + 1] = min(dp[c], dp[c + 1], prev) + 1
                max_side = max(max_side, dp[c + 1])
            else:
                dp[c + 1] = 0
            prev = temp
    return max_side * max_side

assert maximal_square([["1","0","1","0","0"],
                       ["1","0","1","1","1"],
                       ["1","1","1","1","1"],
                       ["1","0","0","1","0"]]) == 4
```

- **State:** `dp[c+1]` = side of largest all-1 square ending at (r, c). **Recurrence:** `1 + min(top, left, top-left)` — the square's size is capped by its 3 neighbors.
- `prev` holds the old `dp[c+1]` (= top-left) before overwrite; 1D trick to avoid a full 2D table.
- **Complexity:** O(m·n) time, O(cols) space.

## String-Stack-Style: Longest Valid Parentheses

```python
def longest_valid_parentheses(s):
    dp = [0] * len(s)
    res = 0
    for i in range(1, len(s)):
        if s[i] == ")":
            if s[i - 1] == "(":                      # "()" pair
                dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
            elif i - dp[i - 1] > 0 and s[i - dp[i - 1] - 1] == "(":
                # ")..valid..)" where dp[i-1] is inner valid block
                dp[i] = dp[i - 1] + 2 + (
                    dp[i - dp[i - 1] - 2] if i - dp[i - 1] >= 2 else 0)
            res = max(res, dp[i])
    return res

assert longest_valid_parentheses("(()") == 2
assert longest_valid_parentheses(")()())") == 4
assert longest_valid_parentheses("()(())") == 6
```

- **State:** `dp[i]` = length of longest valid parentheses substring ending at i.
- **Complexity:** O(n) time, O(n) space. (Stack-based O(n)/O(n) and two-pass counters O(1) space are alternates.)

## Interval DP: Burst Balloons (basics)

```python
def max_coins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):                       # window size
        for left in range(n - length):
            right = left + length
            for k in range(left + 1, right):         # k = last balloon burst in (left, right)
                dp[left][right] = max(
                    dp[left][right],
                    dp[left][k] + dp[k][right]
                    + nums[left] * nums[k] * nums[right],
                )
    return dp[0][n - 1]

assert max_coins([3, 1, 5, 8]) == 167
```

- **State:** `dp[left][right]` = max coins from bursting all balloons strictly between left and right.
- **Key insight (reverse thinking):** pick k as the *last* balloon burst; its neighbors are left and right, so it contributes `nums[left]*nums[k]*nums[right]` and splits into two independent subproblems.
- **Complexity:** O(n³) time, O(n²) space.

## DP on Trees: Diameter

```python
def diameter(edges, n):
    from collections import defaultdict
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    best = 0

    def dfs(u, parent):
        nonlocal best
        max_down = 0                                # longest downward path from u
        for v in adj[u]:
            if v == parent:
                continue
            d = dfs(v, u) + 1
            best = max(best, max_down + d)          # path through u
            max_down = max(max_down, d)
        return max_down

    dfs(0, -1)
    return best

assert diameter([(0, 1), (0, 2), (1, 3), (1, 4)], 5) == 3   # 3-1-0-2
```

- **State:** `dfs(u)` returns the longest path from u down into its subtree; `best` tracks the longest path that passes through u (combine two child depths).
- **Complexity:** O(n) time, O(n) recursion stack.

## DP Problem Identification Table

| Problem | State | Recurrence (essence) | Complexity |
|---|---|---|---|
| Fibonacci / stairs | `dp[i]` = value / ways to i | `dp[i]=dp[i-1]+dp[i-2]` | O(n), O(1) |
| House robber | `dp[i]` = max gain up to i | `dp[i]=max(dp[i-1], nums[i]+dp[i-2])` | O(n), O(1) |
| Coin change (min) | `dp[i]` = min coins for amount i | `dp[i]=min(dp[i-c])+1` | O(amt·c), O(amt) |
| Coin change (ways) | `dp[i]` = #combos summing to i | `dp[i]+=dp[i-c]`, coin outer, forward | O(amt·c), O(amt) |
| 0/1 knapsack | `dp[cap]` = max value | `max(dp[cap], dp[cap-w]+v)`, reverse | O(n·W), O(W) |
| Unbounded knapsack | `dp[cap]` = max value | same, forward | O(n·W), O(W) |
| LIS | `tails[i]` = min tail of len i+1 | binary search replace | O(n log n), O(n) |
| LCS | `dp[i][j]` = LCS of prefixes | match `+1`, else max of up/left | O(mn), O(mn) |
| Edit distance | `dp[i][j]` = min ops | `1+min(del,ins,rep)` | O(mn), O(mn) |
| LPS substring | `dp[i][j]` = is pal | `s[i]==s[j] and dp[i+1][j-1]` | O(n²), O(n²) |
| LPS subsequence | `dp[i][j]` = LPS len | equal `+2`, else max(drop end) | O(n²), O(n²) |
| Partition equal subset | `dp[s]` = reachable sum s | `dp[s] or= dp[s-x]`, reverse | O(n·S), O(S) |
| Word break | `dp[i]` = prefix segmentable | `dp[j] and s[j:i] in dict` | O(n²), O(n) |
| Decode ways | `dp[i]` = #ways to decode prefix | 1-digit + 2-digit contributions | O(n), O(n) |
| Unique paths | `dp[j]` = paths to cell | `dp[j]+=dp[j-1]` | O(mn), O(n) |
| Min path sum | `dp[j]` = min sum to cell | `min(top,left)+grid` | O(mn), O(n) |
| Maximal square | `dp[c]` = max side ending here | `1+min(top,left,topleft)` | O(mn), O(n) |
| Longest valid paren | `dp[i]` = valid len ending at i | extend pair / join blocks | O(n), O(n) |
| Burst balloons | `dp[l][r]` = coins in (l,r) | last-burst split, O(n³) | O(n³), O(n²) |
| Tree diameter | `dfs(u)` = max depth down | `best = max(best, d1+d2)` | O(n), O(n) |

## Top Rules to Nail in the Interview

1. **State** is the hardest part — say it out loud: "`dp[i]` means …" before writing code.
2. **Base cases** first, always — they define the whole table.
3. **Iteration order** matters: increasing length for interval/palindrome DP; reverse for 0/1; forward for unbounded; coins-outer for combinations, amount-outer for permutations.
4. Reconstruct solutions by walking the table backwards from the final cell.
5. Roll 2D to 1D only when the recurrence reads a single previous row — never juggle `prev` mid-iteration without a temp variable.
