# DP Misc Patterns

## Pattern Decision Guide

```
┌──────────────────────────────────────────────────────────────────────────┐
│                   MISC DP PATTERN GUIDE                                  │
├─────────────────────────────┬────────────────────────────────────────────┤
│ Problem hints               │ Pattern                                  │
├─────────────────────────────┼────────────────────────────────────────────┤
│ "count numbers in [L, R]"   │ Digit DP (pos, tight, state)             │
│ "matrix multiplication"     │ Interval DP on dimensions                │
│ "cut stick into pieces"     │ Interval DP on cut positions             │
│ "probability of event"      │ Probability DP (floating point or counting)│
│ "regex / wildcard match"    │ 2D string DP with special char handling   │
│ "no consecutive pattern"    │ Fibonacci / linear recurrence            │
└─────────────────────────────┴────────────────────────────────────────────┘
```

---

## Digit DP

Count numbers in [0, high] satisfying a property, processed digit by digit.

### Visual Walkthrough

```
Key idea: Process the number digit by digit from left to right.
State: dp[pos][tight][state]
  pos      = current digit position (0-indexed from left)
  tight    = 1 if all previous digits matched the upper bound exactly
             0 if we already chose a smaller digit (free to pick 0-9)
  state    = problem-specific state (e.g., digit sum, parity, etc.)

Example: Count numbers in [0, 999] with digit sum = 15
  digits of 999 = [9, 9, 9]

  At pos=0 (first digit):
    tight=1, limit=9 → can pick 0-9
    If pick 9 → tight stays 1, sum=9
    If pick 7 → tight becomes 0, sum=7

  At pos=1 (second digit):
    tight=1 → limit=9; tight=0 → limit=9 (free!)
    
  At pos=2 (last digit):
    Return 1 if sum_sofar == target, else 0

Template:
  func(pos, tight, state):
    if pos == len(digits):
      return 1 if state is valid else 0
    
    limit = digits[pos] if tight else 9
    for d in 0..limit:
      new_tight = tight and (d == limit)
      new_state = transition(state, d)
      total += func(pos+1, new_tight, new_state)

  Memoize on (pos, tight, state)
```

### Template Code

```python
def digit_dp_template(high, is_valid_state, transition):
    """Generic digit DP template"""
    digits = list(map(int, str(high)))
    n = len(digits)
    memo = {}

    def dfs(pos, tight, state):
        if pos == n:
            return 1 if is_valid_state(state) else 0
        key = (pos, tight, state)
        if key in memo:
            return memo[key]
        limit = digits[pos] if tight else 9
        total = 0
        for d in range(limit + 1):
            new_state = transition(state, d)
            total += dfs(pos + 1, tight and d == limit, new_state)
        memo[key] = total
        return total

    return dfs(0, True, 0)
```

### Example: Count Numbers with Digit Sum = Target

```python
def count_digit_sum(high, target):
    digits = list(map(int, str(high)))
    n = len(digits)
    memo = {}

    def dfs(pos, tight, sum_sofar):
        if sum_sofar > target:
            return 0  # Pruning: already exceeded target
        if pos == n:
            return 1 if sum_sofar == target else 0
        key = (pos, tight, sum_sofar)
        if key in memo:
            return memo[key]
        limit = digits[pos] if tight else 9
        total = 0
        for d in range(limit + 1):
            total += dfs(pos + 1, tight and d == limit, sum_sofar + d)
        memo[key] = total
        return total

    return dfs(0, True, 0)
```

### Example: Count Binary Strings with No Consecutive 1s

```python
def count_non_consecutive_ones(n):
    """Count binary strings of length n with no consecutive 1s"""
    if n <= 0:
        return 1
    dp0 = 1  # Ends with 0
    dp1 = 1  # Ends with 1
    for _ in range(2, n + 1):
        new_dp0 = dp0 + dp1   # Can append 0 after either
        dp1 = dp0             # Can append 1 only after 0
        dp0 = new_dp0
    return dp0 + dp1

# This is equivalent to Fibonacci! fib(n+2) or fib(n+1) + fib(n)
# For n=4: 0000, 0001, 0010, 0100, 0101, 1000, 1001, 1010 → 8 strings
```

---

## Interval DP

State: dp[i][j] over interval [i, j]

### Visual Walkthrough — Matrix Chain Multiplication

```
Matrices: A₁(10×30) × A₂(30×5) × A₃(5×60)

Dimensions array: p = [10, 30, 5, 60]
  p[i-1] × p[i] = dimensions of matrix i

Goal: Find parenthesization to minimize scalar multiplications.

DP Table (fill by increasing chain length):
  dp[i][j] = min cost to multiply matrices i through j

     j→  1    2
  i↓  ┌──────┬──────┐
  1   │  0   │ 1500 │   dp[1][2] = 10×30×5 = 1500 (only one way)
      ├──────┼──────┤
  2   │  .   │  0   │   dp[2][2] = 0 (single matrix)
      └──────┴──────┘

  Chain length 3:
  dp[1][3] = min over k:
    k=1: dp[1][1] + dp[2][3] + p[0]*p[1]*p[3] = 0+0+10*30*60 = 18000
    k=2: dp[1][2] + dp[3][3] + p[0]*p[2]*p[3] = 1500+0+10*5*60 = 4500  ← min!

  dp[1][3] = 4500  (parenthesization: (A₁×A₂)×A₃)

State transition:
  dp[i][j] = min over k in [i, j-1]:
    dp[i][k] + dp[k+1][j] + p[i]*p[k+1]*p[j+1]
    ────────   ───────────   ────────────────────
    left part   right part    cost to merge results

Fill order: by increasing chain length (1, 2, 3, ..., n)
```

```python
def matrix_chain(p):
    """p = dimensions: matrices p[0]×p[1], p[1]×p[2], ..., p[n-1]×p[n]"""
    n = len(p) - 1  # number of matrices
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):          # chain length
        for i in range(n - length + 1):     # start
            j = i + length - 1              # end
            dp[i][j] = float("inf")
            for k in range(i, j):           # split point
                q = dp[i][k] + dp[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                dp[i][j] = min(dp[i][j], q)
    return dp[0][n - 1]

# Time: O(n³), Space: O(n²)
```

---

### Minimum Cost to Cut a Stick

```python
def min_cost_to_cut(n, cuts):
    """n = stick length, cuts = positions to cut"""
    cuts = [0] + sorted(cuts) + [n]
    m = len(cuts)
    dp = [[0] * m for _ in range(m)]
    for length in range(2, m):           # interval length (number of cut points)
        for i in range(m - length):      # left boundary
            j = i + length               # right boundary
            dp[i][j] = float("inf")
            for k in range(i + 1, j):    # split point (cut position)
                dp[i][j] = min(dp[i][j],
                               dp[i][k] + dp[k][j] + cuts[j] - cuts[i])
                #                    ───── left ──── + ──── right ──── + ── cut cost ──
    return dp[0][m - 1]

# Time: O(m³) where m = len(cuts), Space: O(m²)
```

---

## Probability DP

### Dice Throw (n dice, each k faces, sum = target)

```
dp[d][s] = number of ways to get sum s with d dice

  dice 1: dp[1][s] = 1 for s in 1..k, else 0
  dice 2: dp[2][s] = sum of dp[1][s-face] for face in 1..k
  
  Space-optimized: use 1D array, process each die separately.

Example: n=2 dice, k=6 faces, target=7
  After die 1: dp = [0, 1, 1, 1, 1, 1, 1]  (sums 1-6 each have 1 way)
  After die 2: dp[7] = dp[6]+dp[5]+dp[4]+dp[3]+dp[2]+dp[1] = 6 ways
  Answer: 6
```

```python
def dice_sum_prob(n, k, target):
    """Count ways to get target sum with n dice of k faces (1..k)"""
    dp = [0] * (target + 1)
    dp[0] = 1  # Base: 0 dice, sum 0 = 1 way
    for die in range(n):
        new = [0] * (target + 1)
        for s in range(target + 1):
            if dp[s] == 0:
                continue
            for face in range(1, k + 1):
                if s + face <= target:
                    new[s + face] += dp[s]
        dp = new
    return dp[target]

# Time: O(n × target × k), Space: O(target)
```

---

## String DP

### Regular Expression Matching — Visual

```
s = "aa", p = "a*"

Key insight: '*' means zero or more of the PREVIOUS character.
At each (i, j), check p[j]:
  - If p[j] is a regular char: match if s[i]==p[j], move both forward
  - If p[j] is '.' : matches any char, move both forward
  - If p[j] is '*' :
      Option 1: Use '*' as zero occurrences → skip p[j-1]*, try dp[i][j-2]
      Option 2: Use '*' as 1+ occurrences → if s[i] matches p[j-1], try dp[i+1][j]

DP Table for s="aa", p="a*":
     ""  a  *        ← pattern (columns)
  ┌────┬────┬────┐
""│  T │  F │  T │   dp[0][2]: a* = 0 a's → same as dp[0][0] = T
  ├────┼────┼────┤
 a│  F │  T │  T │   dp[1][2]: a* can match one 'a' → dp[0][2]=T
  ├────┼────┼────┤
 a│  F │  F │  T │   dp[2][2]: a* can match second 'a' → dp[1][2]=T
  └────┴────┴────┘
  Answer: dp[2][2] = True

Rules:
  s[i] matches p[j]     → dp[i][j] = dp[i-1][j-1]   (normal match)
  p[j] = '*'            → dp[i][j] = dp[i][j-2]      (zero occurrences)
                        → + dp[i-1][j] if s[i] matches p[j-1] (1+ occurrences)
```

```python
def regex_match_tab(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    # Handle patterns like a*, a*b*, a*b*c* matching empty string
    for j in range(2, n + 1):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]  # '*' can make previous char appear 0 times

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == s[i - 1] or p[j - 1] == ".":
                dp[i][j] = dp[i - 1][j - 1]   # Direct match
            elif p[j - 1] == "*":
                dp[i][j] = dp[i][j - 2]        # Zero occurrences of prev char
                if p[j - 2] == s[i - 1] or p[j - 2] == ".":
                    dp[i][j] = dp[i][j] or dp[i - 1][j]  # 1+ occurrences
    return dp[m][n]

# Time: O(m × n), Space: O(m × n)
```

---

### Wildcard Matching

```
s = "adceb", p = "*a*b"

Key difference from regex: '*' matches ANY sequence (not tied to a previous char)

DP Table:
     ""  *  a  *  b       ← pattern
  ┌────┬────┬────┬────┬────┐
""│  T │  T │  F │  T │  F │   * at j=1 matches empty, * at j=3 also
  ├────┼────┼────┼────┼────┤
 a│  F │  T │  T │  T │  F │   * at j=4: b doesn't match a
  ├────┼────┼────┼────┼────┤
 d│  F │  T │  F │  T │  F │
  ├────┼────┼────┼────┼────┤
 c│  F │  T │  F │  T │  F │
  ├────┼────┼────┼────┼────┤
 e│  F │  T │  F │  T │  F │
  ├────┼────┼────┼────┼────┤
 b│  F │  T │  F │  T │  T │   * at j=3 matches "adce", b matches b
  └────┴────┴────┴────┴────┘
  Answer: True

Rules:
  s[i] matches p[j] or p[j]='?' → dp[i][j] = dp[i-1][j-1]
  p[j]='*' → dp[i][j] = dp[i-1][j] (match one more char)
           or dp[i][j] = dp[i][j-1] (match zero chars)
```

```python
def wildcard_match_tab(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    # Leading *'s can match empty string
    for j in range(1, n + 1):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 1]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == s[i - 1] or p[j - 1] == "?":
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j - 1] == "*":
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
                # dp[i-1][j]: * matches one more character of s
                # dp[i][j-1]: * matches zero characters (skip *)
    return dp[m][n]

# Time: O(m × n), Space: O(m × n)
```

---

## Summary Table & Quick Reference

```
┌──────────────────────────┬──────────────────────────┬───────────────┬───────────────────────────────────┐
│ Pattern                  │ Technique                │ Complexity    │ When to Use                       │
├──────────────────────────┼──────────────────────────┼───────────────┼───────────────────────────────────┤
│ Digit DP                 │ pos + tight + state      │ O(pos×10×st)  │ Count numbers in [L,R] with property│
│ Interval DP              │ length, i, k             │ O(n³)         │ MCM, palindrome partition, cuts   │
│ Probability DP           │ dp[s] += dp[s-face]     │ O(n×k×target) │ Dice problems, stochastic DP      │
│ Regex Matching           │ 2D char-by-char          │ O(m×n)        │ '.' and '*' pattern matching      │
│ Wildcard Matching        │ 2D with '*' expansion    │ O(m×n)        │ '?' and '*' glob matching         │
│ No Consecutive Pattern   │ Fibonacci recurrence     │ O(n)          │ Binary strings with restrictions  │
└──────────────────────────┴──────────────────────────┴───────────────┴───────────────────────────────────┘
```

### Pattern Recognition Cheat Sheet

```
╔══════════════════════════════════════════════════════════════════════╗
║  "Count in range [0, N]" with digit constraint  → DIGIT DP         ║
║  "Matrix chain multiply" or "optimal split"     → INTERVAL DP      ║
║  "Rolling dice, find probability/ways"          → PROBABILITY DP   ║
║  "Pattern matching with special chars"          → 2D STRING DP     ║
║  "No two consecutive 1s" type constraint        → FIBONACCI-like   ║
╚══════════════════════════════════════════════════════════════════════╝
```
