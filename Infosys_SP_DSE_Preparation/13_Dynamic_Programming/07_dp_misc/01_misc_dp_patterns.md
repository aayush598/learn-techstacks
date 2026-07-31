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

Digit DP counts how many integers in a range `[0, high]` (or `[L, R]`) satisfy a property, by processing the digits of the numbers one position at a time, from the most significant digit to the least.

Key ideas:
- `pos` = current digit position (0-indexed from the left).
- `tight` = 1 if every digit chosen so far matched the upper bound exactly (so the next digit is capped by `high`'s digit); `tight` becomes 0 as soon as we pick a strictly smaller digit, after which every remaining position is free to be 0-9.
- `state` = problem-specific information carried along (e.g., running digit sum, parity, presence of a digit).

Generic template (memorize this shape):

```python
def digit_dp_template(high, is_valid_state, transition):
    """Generic digit DP template."""
    digits = list(map(int, str(high)))
    n = len(digits)
    memo = {}

    def dfs(pos, tight, state):
        if pos == n:
            return 1 if is_valid_state(state) else 0
        key = (pos, tight, state)
        if key in memo:
            return memo[key]
        limit = digits[pos] if tight else 9     # the bound only applies while tight
        total = 0
        for d in range(limit + 1):
            new_state = transition(state, d)
            total += dfs(pos + 1, tight and d == limit, new_state)
        memo[key] = total
        return total

    return dfs(0, True, 0)
```

Example sketch: count numbers in `[0, 999]` with digit sum 15. `digits of 999 = [9, 9, 9]`.
- At pos=0 (first digit), `tight=1`, limit=9: pick 9 -> tight stays 1, sum 9; pick 7 -> tight becomes 0, sum 7.
- At pos=1, if tight=1 the limit is 9; if tight=0 the limit is 9 (free).
- At pos=2 (last digit): return 1 if `sum_sofar == target`, else 0.

### Count Numbers with Digit Sum = Target

**Problem Explanation:**
Count how many integers in the range `[0, high]` have a digit sum exactly equal to `target`. The input is the upper bound `high` (inclusive) and the target sum; the output is the count. For example, among `0..25`, the numbers 3, 12, and 21 each have digit sum 3. The count includes 0 (digit sum 0) when `target == 0`.

**State Definition:**
`dfs(pos, tight, sum_sofar)` = number of ways to complete the number from digit position `pos` onward, given `tight` (whether the prefix so far equals the prefix of `high`) and `sum_sofar` (the sum of the digits chosen so far). The final answer is `dfs(0, True, 0)`.

**Recurrence Relation:**
```
dfs(pos, tight, sum) = sum over d in 0..limit of dfs(pos + 1, tight and d == limit, sum + d)
```
where `limit = digits[pos]` if `tight` else `9`.

Plain English: at each position we try every allowed digit; the count of complete numbers from this point on is the sum of the counts for each digit we could put here, and the "tight" flag just decides what the allowed digits are.

**Base Cases:**
- `pos == n` (all digits placed): return 1 if `sum_sofar == target`, else 0.
- Pruning: if `sum_sofar > target`, return 0 immediately — adding more digits can only increase the sum.
- The number of digits `n = len(str(high))`; shorter numbers are handled naturally by leading zeros (e.g., "7" is treated as "007" when `high = 999`).

**Intuition (Why This Works):**
The search space (all numbers up to `high`) is huge, but the set of relevant sub-problems is tiny: `pos x tight x sum`. Two different numbers that agree on the digits already placed, the tight flag, and the running sum are indistinguishable for the future, so they share one DP state. The `tight` flag is what enforces the upper bound `high` without enumerating numbers; memoizing on `(pos, tight, sum_sofar)` turns an exponential digit enumeration into a linear one.

**Step-by-Step Procedure:**
1. Convert `high` to a list of digits.
2. Define `dfs(pos, tight, sum_sofar)`.
3. If `sum_sofar > target`, return 0 (prune).
4. If `pos == len(digits)`, return 1 if `sum_sofar == target` else 0.
5. Compute `limit = digits[pos]` if tight else 9.
6. Loop `d` from 0 to `limit`, recursing with `pos + 1`, `tight and d == limit`, `sum_sofar + d`.
7. Sum the recursive results, memoize on `(pos, tight, sum_sofar)`, and return.
8. Return `dfs(0, True, 0)`.

**Worked Example (Dry Run):**
`high = 25`, `target = 3`. Digits `[2, 5]`, `n = 2`.

- `dfs(0, tight=True, 0)`: limit = 2.
  - `d=0` -> `dfs(1, False, 0)`: limit = 9; the only digit that reaches sum 3 is `d=3` -> returns 1.
  - `d=1` -> `dfs(1, False, 1)`: `d=2` reaches sum 3 -> returns 1.
  - `d=2` -> `dfs(1, True, 2)`: limit = 5 (still tight); `d=1` reaches sum 3 -> returns 1.
  - total = 1 + 1 + 1 = 3.

The three numbers are 3, 12, 21. Answer: **3**.

(As a second check, `count_digit_sum(999, 15)` returns 73 — verified against a brute-force scan of all numbers 0..999.)

**Code:**
```python
def count_digit_sum(high, target):
    """Count integers in [0, high] whose digit sum equals exactly target."""
    digits = list(map(int, str(high)))
    n = len(digits)
    memo = {}

    def dfs(pos, tight, sum_sofar):
        if sum_sofar > target:
            return 0                              # prune: more digits only grow the sum
        if pos == n:
            return 1 if sum_sofar == target else 0  # all digits placed: check the sum
        key = (pos, tight, sum_sofar)
        if key in memo:
            return memo[key]                      # reuse the cached sub-problem
        limit = digits[pos] if tight else 9       # tight caps the digit; otherwise free 0-9
        total = 0
        for d in range(limit + 1):
            total += dfs(pos + 1, tight and d == limit, sum_sofar + d)
        memo[key] = total
        return total

    return dfs(0, True, 0)
```

**Complexity:**
- Time: `O(n * 2 * target * 10)` — at most `n` positions, 2 tight values, `target+1` sums, 10 digit choices.
- Space: `O(n * 2 * target)` for the memo (plus recursion depth `n`).

**Common Mistakes & Edge Cases:**
- Forgetting the `tight and d == limit` update: if you stay tight after picking a smaller digit, you wrongly reject valid numbers.
- Forgetting that `tight` is a boolean used in the memo key; `True` and `False` must be distinct states.
- `target = 0`: only the number 0 qualifies (every non-zero number has positive digit sum), so the answer is 1.
- Pruning with `sum_sofar > target` is only safe because digit sums never decrease — never apply it for properties that can go back down.
- Leading zeros: numbers shorter than `n` digits are handled by allowing digit 0 at leading positions; do not add a separate "started" flag unless the problem forbids leading zeros explicitly.

---

### Count Binary Strings with No Consecutive 1s

**Problem Explanation:**
Count the number of binary strings (only characters '0' and '1') of length `n` that contain no two consecutive '1's. Input: length `n`. Output: the count. For example, for `n = 4` there are 8 valid strings: 0000, 0001, 0010, 0100, 0101, 1000, 1001, 1010.

**State Definition:**
This problem collapses to a 2-state linear DP (no mask needed):
- `dp0` = number of valid strings of the current length that **end with '0'**.
- `dp1` = number of valid strings of the current length that **end with '1'**.

**Recurrence Relation:**
```
new_dp0 = dp0 + dp1     # append '0' after any valid string
dp1     = dp0           # append '1' only after strings ending in '0'
```

Plain English: a '0' can follow either ending, but a '1' can only follow a '0', otherwise we would create "11". Each step processes one more character, doubling the length considered.

**Base Cases:**
- For length 1: `dp0 = 1` (the string "0"), `dp1 = 1` (the string "1").
- `n = 0`: the empty string is the only valid string, so the answer is 1.
- Answer = `dp0 + dp1` after processing length `n`.

**Intuition (Why This Works):**
The only thing that matters for the next character is the last character of the current string — "no consecutive 1s" is a constraint that depends only on the previous bit. This is a classic Fibonacci-style recurrence: the number of valid strings of length `n` equals the number of valid strings of length `n-1` (append 0) plus those of length `n-2` (append 1 after the strings that ended in 0). In fact `count(n) = fib(n + 2)`.

**Step-by-Step Procedure:**
1. If `n <= 0`, return 1.
2. Initialize `dp0 = 1`, `dp1 = 1` (length-1 strings).
3. Loop `length` from 2 to `n`.
4. Save `new_dp0 = dp0 + dp1` (append 0 anywhere).
5. Set `dp1 = dp0` (append 1 only after a 0).
6. Set `dp0 = new_dp0`.
7. After the loop, return `dp0 + dp1`.

**Worked Example (Dry Run):**
`n = 4`.

| length | dp0 (ends in 0) | dp1 (ends in 1) | total |
|--------|-----------------|-----------------|-------|
| 1      | 1               | 1               | 2     |
| 2      | 2               | 1               | 3     |
| 3      | 3               | 2               | 5     |
| 4      | 5               | 3               | 8     |

The 8 valid strings of length 4: 0000, 0001, 0010, 0100, 0101, 1000, 1001, 1010. Answer: **8**.

**Code:**
```python
def count_non_consecutive_ones(n):
    """Count binary strings of length n with no two adjacent 1s."""
    if n <= 0:
        return 1                                  # the empty string
    dp0 = 1                                       # length-1 strings ending in '0': "0"
    dp1 = 1                                       # length-1 strings ending in '1': "1"
    for _ in range(2, n + 1):                     # grow the length one bit at a time
        new_dp0 = dp0 + dp1                       # append '0' after any valid string
        dp1 = dp0                                 # append '1' only after a string ending in '0'
        dp0 = new_dp0
    return dp0 + dp1                              # total valid strings of length n
```

**Complexity:**
- Time: `O(n)` — one loop over the length.
- Space: `O(1)` — only two variables.

**Common Mistakes & Edge Cases:**
- The update order matters: `dp1` must use the OLD `dp0` (before this length's append-0 update). Swap the two updates and you count "11" strings.
- `n = 0` returns 1 (the empty string); some problems define `n >= 1`, in which case the guard is harmless.
- Values grow like Fibonacci; for large `n` use `%` (modulo) if the problem asks for a count modulo a prime.
- The recurrence is identical to the Fibonacci sequence shifted: `count(n) = fib(n + 2)`; this lets you switch to fast matrix exponentiation for huge `n`.

---

## Interval DP

Interval DP solves problems where the state is a contiguous interval `[i, j]` of the input, and larger intervals are built from smaller sub-intervals. The standard fill order is by increasing interval length.

### Matrix Chain Multiplication

**Problem Explanation:**
Given `n` matrices whose dimensions are stored in the array `p` (matrix `i` has dimensions `p[i-1] x p[i]`), find the minimum number of scalar multiplications needed to multiply all of them together. Matrix multiplication is associative but not commutative, so we may choose any parenthesization. Input: dimension array `p` of length `n + 1`. Output: the minimum scalar-multiplication cost.

**State Definition:**
`dp[i][j]` = the minimum cost to multiply together the contiguous block of matrices `i` through `j` (0-indexed). The final answer is `dp[0][n - 1]`, and `dp[i][i] = 0` (a single matrix costs nothing to "multiply").

**Recurrence Relation:**
```
dp[i][j] = min over k in [i, j-1] of ( dp[i][k] + dp[k+1][j] + p[i] * p[k+1] * p[j+1] )
             ────── left block ──────   ──── right block ────   ── merge cost ──
```

Plain English: pick the last multiplication performed — it joins the product of matrices `i..k` with the product of matrices `k+1..j`. The cost is the cost of the two sub-products plus the cost of multiplying their result matrices, whose dimensions are `p[i] x p[k+1]` and `p[k+1] x p[j+1]`.

**Base Cases:**
- `dp[i][i] = 0` for every `i`: multiplying one matrix costs nothing.
- Intervals are processed in increasing length, so `dp[i][k]` and `dp[k+1][j]` are always computed before `dp[i][j]`.

**Intuition (Why This Works):**
Any parenthesization has one "outermost" multiplication that splits the chain into a left block and a right block. By trying every possible split point `k`, we cover every possible parenthesization, and the optimal sub-costs are reused because the same sub-chain `i..j` appears inside many parenthesizations. This is optimal-substructure: the best way to multiply `i..j` must use the best ways to multiply both of its parts.

**Step-by-Step Procedure:**
1. Compute `n = len(p) - 1` (number of matrices).
2. Create an `n x n` table `dp` initialized to 0.
3. Loop `length` from 2 to `n` (interval size in matrices).
4. Loop `i` from 0 to `n - length` (left end); set `j = i + length - 1`.
5. Initialize `dp[i][j] = infinity`.
6. Loop split point `k` from `i` to `j - 1`.
7. Candidate = `dp[i][k] + dp[k+1][j] + p[i] * p[k+1] * p[j+1]`; take the minimum.
8. Return `dp[0][n - 1]`.

**Worked Example (Dry Run):**
`p = [10, 30, 5, 60]` -> matrices: A1 = 10x30, A2 = 30x5, A3 = 5x60. `n = 3`.

- Length 1 (base): `dp[0][0] = dp[1][1] = dp[2][2] = 0`.
- Length 2:
  - `dp[0][1] = 10 * 30 * 5 = 1500` (only one way: `(A1 x A2)`).
  - `dp[1][2] = 30 * 5 * 60 = 9000` (only one way: `(A2 x A3)`).
- Length 3: `dp[0][2]` = min over k:
  - `k = 0`: `dp[0][0] + dp[1][2] + p[0]*p[1]*p[3] = 0 + 9000 + 10*30*60 = 18000`.
  - `k = 1`: `dp[0][1] + dp[2][2] + p[0]*p[2]*p[3] = 1500 + 0 + 10*5*60 = 4500`  <- min.

DP table (0-indexed):

```
     j=0    j=1    j=2
i=0   0    1500   4500
i=1   -      0    9000
i=2   -      -       0
```

Answer: `dp[0][2] = 4500`, achieved by `(A1 x A2) x A3`.

**Code:**
```python
def matrix_chain(p):
    """p = dimensions: matrices are p[0]x p[1], p[1] x p[2], ..., p[n-1] x p[n]."""
    n = len(p) - 1                                 # number of matrices
    dp = [[0] * n for _ in range(n)]               # dp[i][j] = min cost for matrices i..j
    for length in range(2, n + 1):                 # build intervals by increasing size
        for i in range(n - length + 1):            # left end of the interval
            j = i + length - 1                     # right end of the interval
            dp[i][j] = float("inf")
            for k in range(i, j):                  # try every split point
                q = dp[i][k] + dp[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                #          left block    right block   cost to merge the two results
                dp[i][j] = min(dp[i][j], q)
    return dp[0][n - 1]                            # cost for the whole chain
```

**Complexity:**
- Time: `O(n^3)` — `n^2` intervals, each trying up to `n` splits.
- Space: `O(n^2)` for the table.

**Common Mistakes & Edge Cases:**
- Indexing: the merge cost is `p[i] * p[k+1] * p[j+1]` — using `p[k]` or `p[j]` silently computes the wrong dimensions.
- `n = 1` (a single matrix): the loop never runs and `dp[0][0] = 0` is returned — correct.
- `len(p)` must be at least 2; a single-dimension input is invalid and would crash on `dp[0][n-1]`.
- Processing order is critical: intervals must be filled by length so that both sub-intervals exist. Iterating `i` then `j` in arbitrary order reads uncomputed cells.
- For huge `n`, this stays cubic; there is a Knuth-optimization variant for the special case of optimal binary search trees, but plain MCM is O(n^3).

---

### Minimum Cost to Cut a Stick

**Problem Explanation:**
You have a wooden stick of length `n` (the segment from 0 to `n`) and a list of positions `cuts` where you must cut it. Each cut costs the length of the stick piece being cut. You may cut in any order. Find the minimum total cost to perform all cuts. Input: stick length `n` and list `cuts`. Output: the minimum total cost. For example, a 7-unit stick with cuts at `[1, 3, 4, 5]` costs at least 16.

**State Definition:**
Let `points = [0] + sorted(cuts) + [n]` (the boundaries plus every cut position, `m = len(points)` entries). `dp[i][j]` = the minimum cost to fully cut the piece of the stick that spans `points[i]` to `points[j]`, given that all cuts strictly inside that piece still need to be performed. The answer is `dp[0][m - 1]` (the whole stick).

**Recurrence Relation:**
```
dp[i][j] = min over k in (i, j) of ( dp[i][k] + dp[k][j] + (points[j] - points[i]) )
                ── cut the left piece ──   ── right piece ──   ── cost of this cut ──
```

Plain English: imagine the FIRST cut we make in this piece is at `points[k]`. It costs the whole piece length `points[j] - points[i]`, and afterwards the two remaining sub-pieces are independent and solved recursively. Trying every possible first cut covers every ordering.

**Base Cases:**
- `dp[i][j] = 0` whenever `i + 1 == j` (adjacent points): the piece contains no cut positions, so no cuts and no cost.
- Fill order: by increasing interval width `j - i`, so sub-intervals are ready.

**Intuition (Why This Works):**
After a cut, the two resulting stick pieces are independent sub-problems over contiguous ranges of the sorted cut positions — exactly an interval DP. The total cost depends only on the set of cuts inside a piece, not on the exact order of earlier cuts elsewhere. Optimal-substructure holds: the optimal way to cut a piece uses the optimal ways to cut both of its halves, so trying every first cut `k` is complete.

**Step-by-Step Procedure:**
1. Build `points = [0] + sorted(cuts) + [n]`; `m = len(points)`.
2. Create an `m x m` table `dp` initialized to 0.
3. Loop `length` from 2 to `m - 1` (interval width in number of gaps).
4. Loop `i` from 0 to `m - 1 - length`; set `j = i + length`.
5. Initialize `dp[i][j] = infinity`.
6. Loop the first-cut index `k` from `i + 1` to `j - 1`.
7. Candidate = `dp[i][k] + dp[k][j] + (points[j] - points[i])`; keep the minimum.
8. Return `dp[0][m - 1]`.

**Worked Example (Dry Run):**
`n = 7`, `cuts = [1, 3, 4, 5]`. `points = [0, 1, 3, 4, 5, 7]`, `m = 6`. (The piece length for `dp[i][j]` is always `points[j] - points[i]`.)

- Width 2 (exactly one cut inside; the cost is the piece length):
  - `dp[0][2] = 3` (cut at 1), `dp[1][3] = 3` (cut at 3), `dp[2][4] = 2` (cut at 4), `dp[3][5] = 3` (cut at 5).
- Width 3:
  - `dp[0][3]`: length 4. k=1: `0 + dp[1][3] + 4 = 0 + 3 + 4 = 7`; k=2: `dp[0][2] + 0 + 4 = 3 + 4 = 7` -> `7`.
  - `dp[1][4]`: length 4. k=2: `0 + dp[2][4] + 4 = 2 + 4 = 6`; k=3: `dp[1][3] + 0 + 4 = 3 + 4 = 7` -> `6`.
  - `dp[2][5]`: length 4. k=3: `0 + dp[3][5] + 4 = 3 + 4 = 7`; k=4: `dp[2][4] + 0 + 4 = 2 + 4 = 6` -> `6`.
- Width 4:
  - `dp[0][4]`: length 5. k=1: `0 + dp[1][4] + 5 = 11`; k=2: `dp[0][2] + dp[2][4] + 5 = 3 + 2 + 5 = 10`; k=3: `dp[0][3] + 0 + 5 = 12` -> `10`.
  - `dp[1][5]`: length 6. k=2: `0 + dp[2][5] + 6 = 12`; k=3: `dp[1][3] + dp[3][5] + 6 = 3 + 3 + 6 = 12`; k=4: `dp[1][4] + 0 + 6 = 12` -> `12`.
- Width 5 (whole stick, length 7):
  - `dp[0][5]`: k=1: `0 + dp[1][5] + 7 = 0 + 12 + 7 = 19`; k=2: `dp[0][2] + dp[2][5] + 7 = 3 + 6 + 7 = 16`; k=3: `dp[0][3] + dp[3][5] + 7 = 7 + 3 + 7 = 17`; k=4: `dp[0][4] + 0 + 7 = 10 + 7 = 17` -> `16`.

Answer: `dp[0][5] = 16`. One optimal order: cut at 3 first (cost 7), then cut at 1 in the left piece (cost 3), then in the right piece [3, 7] cut at 5 (cost 4) and finally at 4 (cost 2): total 7 + 3 + 4 + 2 = 16.

**Code:**
```python
def min_cost_to_cut(n, cuts):
    """Minimum total cost to cut a stick of length n at every position in cuts."""
    points = [0] + sorted(cuts) + [n]              # boundaries + cut positions (m entries)
    m = len(points)
    dp = [[0] * m for _ in range(m)]               # dp[i][j] = min cost to cut piece (points[i], points[j])
    for length in range(2, m):                     # interval width in gaps
        for i in range(m - length):
            j = i + length
            dp[i][j] = float("inf")
            for k in range(i + 1, j):              # k is the first cut performed in this piece
                dp[i][j] = min(dp[i][j],
                               dp[i][k] + dp[k][j] + points[j] - points[i])
                #                    left      right      cost of the first cut = piece length
    return dp[0][m - 1]                            # the whole stick
```

**Complexity:**
- Time: `O(m^3)` where `m = len(cuts) + 2`.
- Space: `O(m^2)` for the table.

**Common Mistakes & Edge Cases:**
- Do not forget to sort `cuts` and to prepend 0 / append `n`; the interval DP needs strictly ordered points.
- The cut cost is `points[j] - points[i]` (the full piece length), not a sub-interval length or the cut position itself.
- Cut positions are assumed strictly inside `(0, n)`; a cut at 0 or `n` is a boundary, not a real cut, and is not a valid input.
- The loop ranges: `length` goes to `m - 1` and `i` to `m - 1 - length`, so `j` never exceeds `m - 1`.
- With no cuts, `points = [0, n]`, `dp[0][1] = 0`, and the answer is 0 — cutting nothing costs nothing.

---

## Probability DP

Probability DP counts the number of ways (or tracks probabilities) over stochastic processes, one step at a time. In the dice example below, every outcome is equally likely, so the probability of a sum equals `ways / k^n`.

### Dice Throw (n dice, k faces, target sum)

**Problem Explanation:**
Throw `n` dice, each with faces numbered `1..k`. Count the number of ways the faces can sum to exactly `target`. Input: `n` dice, `k` faces, `target` sum. Output: the number of ways. For example, with 2 six-sided dice, the sum 7 can be rolled in 6 ways (1+6, 2+5, 3+4, 4+3, 5+2, 6+1). The faces are ordered: die 1 rolling 1 and die 2 rolling 6 is a different outcome from the reverse.

**State Definition:**
`dp[s]` (after processing `d` dice) = the number of ways to obtain a running sum of exactly `s`. The table is rebuilt once per die, so the index `d` is implicit in the outer loop rather than stored in the array.

**Recurrence Relation:**
```
new_dp[s + face] += dp[s]      for every face in 1..k with s + face <= target
```
Equivalently, `dp_d[s] = sum over face in 1..k of dp_{d-1}[s - face]`.

Plain English: a sum `s + face` can be reached by first making sum `s` with the previous dice and then rolling `face` on the current die; adding over all faces and all prior sums counts every outcome exactly once.

**Base Cases:**
- `dp[0] = 1`: with 0 dice, the only possible sum is 0, in one way.
- All other entries start at 0.
- If `target > n * k` or `target < n`, the answer is 0 (impossible sums).

**Intuition (Why This Works):**
The process is Markovian in the running sum: after each die, only the total so far matters, not which faces produced it. Each die adds an independent factor, so we just convolve the current distribution with the uniform face distribution. Using a fresh `new` array per die keeps the "number of dice used" implicit and lets us roll the DP forward one die at a time, which is why the 1D space optimization is valid.

**Step-by-Step Procedure:**
1. If `target > n * k` or `target < n`, return 0.
2. Initialize `dp = [0] * (target + 1)` and set `dp[0] = 1`.
3. Loop over each die (`n` times).
4. Create `new = [0] * (target + 1)`.
5. For every sum `s` with `dp[s] > 0`, loop every face `1..k`.
6. If `s + face <= target`, add `dp[s]` to `new[s + face]`.
7. Replace `dp = new`.
8. Return `dp[target]`.

**Worked Example (Dry Run):**
`n = 2`, `k = 6`, `target = 7`.

- Start: `dp = [1, 0, 0, 0, 0, 0, 0, 0]`.
- After die 1: `dp = [0, 1, 1, 1, 1, 1, 1, 0]` (sums 1-6 each reachable in 1 way).
- After die 2, `dp[7]` accumulates:
  `dp[6]+dp[5]+dp[4]+dp[3]+dp[2]+dp[1] = 1 + 1 + 1 + 1 + 1 + 1 = 6`.

Answer: **6** (outcomes 1+6, 2+5, 3+4, 4+3, 5+2, 6+1). If asked for probability, it is `6 / 6^2 = 6/36`.

**Code:**
```python
def dice_sum_prob(n, k, target):
    """Number of ways to get exactly `target` with n dice, each showing 1..k."""
    if target > n * k or target < n:
        return 0                                  # impossible sums
    dp = [0] * (target + 1)
    dp[0] = 1                                     # 0 dice, sum 0: one way
    for die in range(n):                          # add one die at a time
        new = [0] * (target + 1)
        for s in range(target + 1):
            if dp[s] == 0:
                continue                          # no outcomes reach this sum yet
            for face in range(1, k + 1):          # each face extends the sum
                if s + face <= target:
                    new[s + face] += dp[s]        # every prior outcome + this face = new outcome
        dp = new                                  # move to the next die
    return dp[target]
```

**Complexity:**
- Time: `O(n * target * k)` — `n` dice, `target` sums, `k` faces each.
- Space: `O(target)` — a single 1D array plus the temporary `new` array.

**Common Mistakes & Edge Cases:**
- Forgetting to guard `s + face <= target` can index out of range; trimming the inner loops to `range(1, min(k, target - s) + 1)` avoids wasted work too.
- The `target < n` check is needed: with `n` dice the minimum possible sum is `n`, so small targets must return 0 early.
- If the problem asks for probability, remember there are `k^n` total outcomes; the count alone is not the probability.
- The order of dice matters (die 1 = 1, die 2 = 6 differs from 6 then 1); this DP counts ordered outcomes automatically.
- A fresh `new` array per die is required; accumulating into `dp` in place would double-count outcomes using the same die more than once.

---

## String DP

String DP builds a 2D table `dp[i][j]` where `i` indexes a prefix of one string and `j` indexes a prefix of the other. The cell `dp[i][j]` answers a question about `s[:i]` and `p[:j]`, and transitions copy or OR together cells that represent one fewer character.

### Regular Expression Matching

**Problem Explanation:**
Given a string `s` and a pattern `p`, decide whether the entire string `s` matches `p`. In this version of regex: `'.'` matches any single character, and `'*'` means "zero or more of the preceding character" (e.g., `a*` matches `""`, `"a"`, `"aa"`, ...). Input: strings `s` and `p`. Output: `True` or `False`. Unlike wildcard matching, `'*'` here is always attached to a preceding character.

**State Definition:**
`dp[i][j]` = True if `s[:i]` (the first `i` characters of `s`) matches `p[:j]` (the first `j` characters of `p`). The answer is `dp[m][n]` where `m = len(s)`, `n = len(p)`.

**Recurrence Relation:**
```
if p[j-1] == s[i-1] or p[j-1] == '.':   dp[i][j] = dp[i-1][j-1]
if p[j-1] == '*':
    dp[i][j] = dp[i][j-2]                                   # '*' = zero of p[j-2]
    if p[j-2] == s[i-1] or p[j-2] == '.':                   # '*' = one or more
        dp[i][j] = dp[i][j] or dp[i-1][j]
```

Plain English: a normal character must match and consumes one character from both strings; `'.'` is a normal character that matches anything; `'*'` has two interpretations — ignore the pair `x*` entirely (skip 2 pattern chars), or match one more occurrence of `x` (consume one `s` character while keeping the `x*` in the pattern for further repetitions).

**Base Cases:**
- `dp[0][0] = True`: two empty strings match.
- `dp[0][j]` for `j >= 2`: a pattern like `a*`, `a*b*`, `a*b*c*` can match the empty string, so `dp[0][j] = dp[0][j-2]` when `p[j-1] == '*'`.
- `dp[i][0] = False` for `i > 0`: a non-empty string cannot match an empty pattern.

**Intuition (Why This Works):**
The `'*'` creates the only real branching, and it is local: it either "eats" one `s` character (decrementing `i`) or it "gives up" (decrementing `j` by 2). Every matching decision reduces at least one of `i` or `j`, so a 2D table of prefix-answers is complete. The `dp[i-1][j]` transition is the crux: it lets the same `x*` repeat against multiple `s` characters without consuming the pattern.

**Step-by-Step Procedure:**
1. Let `m = len(s)`, `n = len(p)`; create an `(m+1) x (n+1)` table filled with False.
2. Set `dp[0][0] = True`.
3. For `j` from 2 to `n`: if `p[j-1] == '*'`, set `dp[0][j] = dp[0][j-2]` (star can zero out the previous char against empty `s`).
4. Loop `i` from 1 to `m` and `j` from 1 to `n`.
5. If `p[j-1]` equals `s[i-1]` or is `'.'`, set `dp[i][j] = dp[i-1][j-1]`.
6. Else if `p[j-1] == '*'`: set `dp[i][j] = dp[i][j-2]` (zero occurrences); if `p[j-2] == s[i-1]` or `p[j-2] == '.'`, OR in `dp[i-1][j]` (one more occurrence).
7. Return `dp[m][n]`.

**Worked Example (Dry Run):**
`s = "aa"`, `p = "a*"`. Table rows = prefixes of `s` (plus empty), columns = prefixes of `p`.

```
        ""   a    *          pattern
""      T    F    T          a* as zero a's: same as dp[0][0] = T
a       F    T    T          a* matches one 'a': dp[0][2] = T
a       F    F    T          a* matches second 'a': dp[1][2] = T
```

Trace of the key cells:
- Row 0: `dp[0][2]` = `dp[0][0]` = True (star gives zero occurrences).
- `dp[1][1]` = `dp[0][0]` = True ('a' == 'a').
- `dp[1][2]`: star; `dp[1][0] = F`, then since `p[0]='a' == s[0]`, OR `dp[0][2] = T` -> True.
- `dp[2][2]`: star; `dp[2][0] = F`, then since `p[0] == s[1]`, OR `dp[1][2] = T` -> True.

Answer: `dp[2][2] = True`, so `"aa"` matches `"a*"`.

**Code:**
```python
def regex_match_tab(s, p):
    """Match s against regex p, where '.' matches any char and 'x*' means zero or more x."""
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]  # dp[i][j] = s[:i] matches p[:j]
    dp[0][0] = True
    for j in range(2, n + 1):                        # patterns like a*, a*b* match empty s
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]                  # '*' used as zero occurrences
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == s[i - 1] or p[j - 1] == ".":
                dp[i][j] = dp[i - 1][j - 1]          # one char consumed on both sides
            elif p[j - 1] == "*":
                dp[i][j] = dp[i][j - 2]              # zero occurrences of the prev char
                if p[j - 2] == s[i - 1] or p[j - 2] == ".":
                    dp[i][j] = dp[i][j] or dp[i - 1][j]  # one more occurrence of prev char
    return dp[m][n]
```

**Complexity:**
- Time: `O(m * n)` — every cell computed once with O(1) work.
- Space: `O(m * n)` for the table (can be compressed to two rows).

**Common Mistakes & Edge Cases:**
- Accessing `p[j - 2]` is only safe once `j >= 2`; valid inputs never place `'*'` at the start of the pattern, but guard `j` accordingly if inputs are unvalidated.
- `"aa"` vs `"a"` must be False; the `dp[i][j-2]` zero-occurrence transition is what stops the star from over-matching.
- `"ab"` vs `".*"` is True: `'.'` matches any char and `.*` repeats it — verify this against the DP before assuming it is false.
- The row-0 initialization loop starts at `j = 2`; a lone `'*'` at `j = 1` would be out of the problem's valid domain.
- An empty pattern matches only the empty string; `regex_match_tab("a", "")` must be False, which the table gives since `dp[1][0]` stays False.

---

### Wildcard Matching

**Problem Explanation:**
Given a string `s` and a wildcard pattern `p`, decide whether the entire string matches. Here `'?'` matches any single character, and `'*'` matches any sequence of characters (including the empty sequence). Input: strings `s` and `p`. Output: `True` or `False`. The key difference from regex matching: `'*'` is a standalone wildcard, not tied to a preceding character.

**State Definition:**
`dp[i][j]` = True if `s[:i]` matches `p[:j]`. The answer is `dp[m][n]` where `m = len(s)`, `n = len(p)`.

**Recurrence Relation:**
```
if p[j-1] == s[i-1] or p[j-1] == '?':  dp[i][j] = dp[i-1][j-1]
if p[j-1] == '*':                       dp[i][j] = dp[i-1][j] OR dp[i][j-1]
```

Plain English: a normal character or `'?'` consumes one character from both sides; a `'*'` either consumes one more character of `s` (stay on the `'*'`, move `i`) or consumes zero characters (move past the `'*'`, keep `i`). Either option being true means the prefixes match.

**Base Cases:**
- `dp[0][0] = True`: two empty strings match.
- `dp[0][j] = dp[0][j-1]` when `p[j-1] == '*'`: leading stars can match the empty string.
- `dp[i][0] = False` for `i > 0`: non-empty `s` cannot match an empty pattern.

**Intuition (Why This Works):**
The `'*'` transition is the whole trick: `dp[i-1][j]` says "the star already matched the first `i-1` chars, so it can also match the `i`-th", which lets one `'*'` cover arbitrarily many characters, while `dp[i][j-1]` says "the star matched nothing here". Because the star is context-free (not tied to a previous character), there is no need to look back at `p[j-2]` like in regex matching — the recurrence is a pure OR of the two adjacent cells.

**Step-by-Step Procedure:**
1. Let `m = len(s)`, `n = len(p)`; create an `(m+1) x (n+1)` table of False.
2. Set `dp[0][0] = True`.
3. For `j` from 1 to `n`: if `p[j-1] == '*'`, set `dp[0][j] = dp[0][j-1]` (stars match empty).
4. Loop `i` from 1 to `m`, `j` from 1 to `n`.
5. If `p[j-1]` equals `s[i-1]` or is `'?'`, set `dp[i][j] = dp[i-1][j-1]`.
6. Else if `p[j-1] == '*'`, set `dp[i][j] = dp[i-1][j] or dp[i][j-1]`.
7. Return `dp[m][n]`.

**Worked Example (Dry Run):**
`s = "adceb"`, `p = "*a*b"`. Rows = prefixes of `s`, columns = prefixes of `p`.

```
        ""   *    a    *    b      <- pattern
""      T    T    F    T    F      * matches empty; a*... needs 'a' so far
a       F    T    T    T    F      '*' at col1 matches "a"; b doesn't match 'a'
d       F    T    F    T    F
c       F    T    F    T    F
e       F    T    F    T    F
b       F    T    F    T    T      '*' at col3 matched "adce", then b == b
```

Answer: `dp[5][5] = True`, so `"adceb"` matches `"*a*b"`.

**Code:**
```python
def wildcard_match_tab(s, p):
    """Match s against glob p, where '?' matches one char and '*' matches any sequence."""
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]  # dp[i][j] = s[:i] matches p[:j]
    dp[0][0] = True
    for j in range(1, n + 1):                        # leading '*'s match the empty string
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 1]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == s[i - 1] or p[j - 1] == "?":
                dp[i][j] = dp[i - 1][j - 1]          # one char consumed on both sides
            elif p[j - 1] == "*":
                # '*' matches one more char of s (dp[i-1][j]) OR zero chars (dp[i][j-1])
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
    return dp[m][n]
```

**Complexity:**
- Time: `O(m * n)` — every cell computed once with O(1) work.
- Space: `O(m * n)` for the table (can be compressed to two rows).

**Common Mistakes & Edge Cases:**
- Do not use the regex rule (`dp[i][j-2]`) here: wildcard `'*'` is standalone, so `dp[i][j-1]` (skip the star) is the correct "match nothing" transition.
- `"aa"` vs `"*"` must be True: the `dp[i-1][j]` branch lets one star cover both characters.
- `"cb"` vs `"?a"` must be False: `'?'` matches exactly one character, it cannot "miss" the 'c'.
- Trailing stars: `"abc"` vs `"ab*"` is True because the star matches the empty tail via `dp[i][j-1]`.
- If `s` is empty, a pattern of only stars still matches (`dp[0][j]` propagation makes the last row's star column True only when `s` is empty — check `wildcard_match_tab("", "*")` returns True).

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



