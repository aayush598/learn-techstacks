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

**Problem Explanation:**
Given a string `s`, find the length of the longest subsequence that reads the same forwards and backwards (a palindrome). Recall a subsequence may skip characters but must keep the remaining characters in order. Input: one string; output: the integer length. Example: `s = "bbbab"` — the answer is 4 because `"bbbb"` (drop the `a`) is a palindromic subsequence of length 4.

**State Definition:**
`dp[i][j]` = length of the longest palindromic subsequence within the substring `s[i..j]` (characters from index `i` to `j` inclusive).

**Recurrence Relation:**
```
if s[i] == s[j]:  dp[i][j] = dp[i+1][j-1] + 2   (both ends match → wrap them)
else:             dp[i][j] = max(dp[i+1][j], dp[i][j-1])   (skip one end)
```
If the two boundary characters are equal, they can wrap the best palindrome of the inside substring (adding 2). Otherwise the palindrome must live entirely inside after dropping either the left or the right end, so we keep the better of those two options.

**Base Cases:**
- `dp[i][i] = 1` — a single character is a palindrome of length 1.
- `dp[i][j] = 0` for `i > j` — an empty interval (this happens for substrings of length 2 whose ends match, e.g. `dp[i+1][j-1]` with `i+1 > j-1`).

**Intuition (Why This Works):**
This is an **interval DP**: the problem on `s[i..j]` depends on strictly smaller intervals (`s[i+1][j-1]`, `s[i+1][j]`, `s[i][j-1]`), so filling by increasing interval length guarantees dependencies are solved first. The choice at each step is "do the ends match?" — if yes we extend, if no we drop one end. Because a palindrome is symmetric, matching ends always combine into a strictly better answer than the best either side could do alone.

**Step-by-Step Procedure:**
1. Build an `n×n` table; if `s` is empty, return 0.
2. Loop `i` from `n-1` down to `0` (this processes shorter intervals first).
3. Set `dp[i][i] = 1`.
4. For `j` from `i+1` to `n-1` (intervals grow to the right):
5. If `s[i] == s[j]`: `dp[i][j] = dp[i+1][j-1] + 2`.
6. Else: `dp[i][j] = max(dp[i+1][j], dp[i][j-1])`.
7. Return `dp[0][n-1]`.

**Worked Example (Dry Run):**
Input: `s = "bbbab"`.

```
DP Table (filled bottom-left to top-right):
      b   b   b   a   b      ← j (right pointer)
   ┌────┬────┬────┬────┬────┐
 i=0 b│ 1  │ 2  │ 3  │ 3  │ 4  │  ← dp[0][4]: s[0]=b, s[4]=b match → dp[1][3]+2 = 4
   ├────┼────┼────┼────┼────┤
 i=1 b│ .  │ 1  │ 2  │ 2  │ 3  │
   ├────┼────┼────┼────┼────┤
 i=2 b│ .  │ .  │ 1  │ 1  │ 3  │
   ├────┼────┼────┼────┼────┤
 i=3 a│ .  │ .  │ .  │ 1  │ 1  │
   ├────┼────┼────┼────┼────┤
 i=4 b│ .  │ .  │ .  │ .  │ 1  │
   └────┴────┴────┴────┴────┘
   ↑ i (left pointer, filled bottom-up)

Fill order (diagonals, length increasing):
  Diagonal 0 (i==j): dp[i][i] = 1  (single char = palindrome of length 1)
  Diagonal 1:        dp[i][i+1] → s[i]==s[i+1] ? 2 : 1
  Diagonal 2, 3, 4:  increasing lengths
```

Cell-by-cell:
- Diagonal 0: `dp[0][0]=dp[1][1]=...=dp[4][4]=1`.
- `dp[3][4]`: `a ≠ b` → `max(dp[4][4]=1, dp[3][3]=1) = 1`.
- `dp[2][4]`: `b == b` → `dp[3][3] + 2 = 1 + 2 = 3` — palindrome `"bb"` wrapped around the `a`? No: inside `s[3..3]="a"`, so result covers `s[2..4]="bab"`, whose LPS is `"bab"` (length 3). Correct.
- `dp[1][4]`: `b == b` → `dp[2][3] + 2 = 1 + 2 = 3`.
- `dp[0][4]`: `b == b` → `dp[1][3] + 2 = 2 + 2 = 4` — LPS of `"bbbab"` is `"bbbb"`, length 4.

**Final answer: 4.**

**Code:**
```python
def longest_palindrome_subseq_tab(s: str) -> int:
    if not s:
        return 0                     # empty string has no palindrome
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    # Fill by decreasing i (i.e. by increasing interval length):
    # a longer interval needs the shorter intervals already solved.
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1                 # base: a single character is length 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                # Ends match: wrap the palindrome inside s[i+1..j-1].
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                # Ends differ: the palindrome skips one of them.
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]
```

**Complexity:**
- Time: O(n²)
- Space: O(n²) (can be optimized to O(n) with careful rolling, since only `dp[i+1][*]` and `dp[i][*]` are needed)

**Common Mistakes & Edge Cases:**
- Empty string crashes with `dp[0][-1]` — guard `if not s: return 0`.
- Forgetting that `dp[i+1][j-1]` for a 2-character interval is the empty interval `dp[j][i]` region (0), not an out-of-bounds cell.
- Filling in the wrong order (e.g. top-left to bottom-right) reads unsolved cells.
- A string of all identical characters: the answer is `n` (the whole string is a palindrome).
- `"cbbd"` → 2 (either `"bb"`); make sure both `match` and `skip` paths are exercised.

---

## Shortest Common Supersequence

**Problem Explanation:**
Given two strings `a` and `b`, find the shortest string that contains both `a` and `b` as subsequences (in order, not necessarily contiguously). Input: two strings; output: the shortest such supersequence string. Key relationship: `len(SCS) = len(a) + len(b) - len(LCS)` — the shared characters of the LCS need to appear only once in the merged string. Example: `a = "abac"`, `b = "cab"` → `"cabac"` (length 5).

**State Definition:**
`dp[i][j]` = length of the LCS of `a[0:i]` and `b[0:j]` (this is exactly the LCS table; it is used to decide how to merge the two strings during backtracking).

**Recurrence Relation:**
```
if a[i-1] == b[j-1]:  dp[i][j] = dp[i-1][j-1] + 1
else:                 dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```
This is identical to LCS. During the backtracking phase:
```
if a[i-1] == b[j-1]:   take the char once;  i--, j--
elif dp[i-1][j] > dp[i][j-1]:  take a[i-1];  i--
else:                  take b[j-1];  j--
```
Matching characters appear once in the SCS (they serve both strings); for mismatches we must include the character from whichever string we are advancing — that is the entire trick of the construction.

**Base Cases:**
- `dp[0][j] = 0`, `dp[i][0] = 0` (LCS bases — empty prefixes share nothing).
- After the backtracking loop, flush any leftover characters of `a` (`while i > 0`) and `b` (`while j > 0`).

**Intuition (Why This Works):**
A supersequence is formed by "fusing" the two strings at their common subsequence: every LCS character can be shared, and every non-LCS character must be included once from its own string. DP applies because the fusion decisions decompose into the same prefix-pair subproblems as LCS. The choice at each backtrack step is "whose next character do I emit?" — identical characters emit once, differing ones emit the character of the string we advance.

**Step-by-Step Procedure:**
1. Fill the full LCS table for `a` and `b`.
2. Start at `i = len(a), j = len(b)`, with an empty result list.
3. While both `i > 0` and `j > 0`:
4. If `a[i-1] == b[j-1]`: append the shared char, move diagonal.
5. Else if `dp[i-1][j] > dp[i][j-1]`: append `a[i-1]`, `i--`.
6. Else: append `b[j-1]`, `j--`.
7. Append leftover `a` characters, then leftover `b` characters.
8. Reverse the result (it was built tail-first) and join.

**Worked Example (Dry Run):**
Input: `a = "abac"`, `b = "cab"`.

LCS table:
```
     ""  c  a  b
""    0  0  0  0
 a    0  0  1  1
 b    0  0  1  2
 a    0  0  1  2
 c    0  1  1  2   → dp[4][3] = 2, so SCS length = 4 + 3 - 2 = 5
```

Backtracking from `(4,3)`:
- `(4,3)`: `a[3]='c' == b[2]='b'`? No. `dp[3][3]=2 > dp[4][2]=1` → take `'c'`, `i=3`.
- `(3,3)`: `a[2]='a' == b[2]='b'`? No. `dp[2][3]=2 > dp[3][2]=1` → take `'a'`, `i=2`.
- `(2,3)`: `a[1]='b' == b[2]='b'`? Yes → take `'b'`, `i=1, j=2`.
- `(1,2)`: `a[0]='a' == b[1]='a'`? Yes → take `'a'`, `i=0, j=1`.
- Loop ends (`i==0`). Flush `b`: take `'b'`? `j=1` → append `b[0]='c'`, `j=0`.
- Collected tail-first: `['c','a','b','a','c']` → reversed → `"cabac"`.

**Final answer: `"cabac"` (length 5).**

**Code:**
```python
def shortest_common_supersequence(a: str, b: str) -> str:
    m, n = len(a), len(b)
    # Fill the LCS table: dp[i][j] = LCS length of a[0:i] and b[0:j].
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack to build the SCS, starting from the bottom-right corner.
    i, j = m, n
    result = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            # Shared character: emit it ONCE (it belongs to both strings).
            result.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            # LCS came from above → 'a' is the extra character here.
            result.append(a[i - 1])
            i -= 1
        else:
            # LCS came from left → 'b' is the extra character here.
            result.append(b[j - 1])
            j -= 1
    # Flush any characters that were never consumed by the merge.
    while i > 0:
        result.append(a[i - 1])
        i -= 1
    while j > 0:
        result.append(b[j - 1])
        j -= 1
    # Built from the end backwards → reverse before returning.
    return ''.join(reversed(result))
```

**Complexity:**
- Time: O(m×n)
- Space: O(m×n) (the full table is required for backtracking)

**Common Mistakes & Edge Cases:**
- Forgetting the leftover-flush loops — characters at the front of one string would silently vanish.
- Forgetting to reverse the result (the backtrack builds from the tail).
- One empty string: the SCS is simply the other string.
- Two disjoint strings (LCS = 0): the SCS is `a + b` (or `b + a`).
- Using `>=` on the "from above" comparison instead of `>` on the "from left" check only picks a different valid SCS of the same length.

---

## Maximum Square in Binary Matrix

**Problem Explanation:**
Given an `m×n` matrix whose cells are the characters `'1'` and `'0'`, find the **area** of the largest square consisting entirely of `'1'`s. Input: the matrix; output: the integer area (`side × side`). Example: in the matrix below the largest all-`'1'` square has side 2, so the answer is 4.

**State Definition:**
`dp[i][j]` = side length of the largest square of `'1'`s whose **bottom-right corner** is cell `(i-1, j-1)` of the original matrix (the `+1` indexing absorbs a padding row/column).

**Recurrence Relation:**
```
if matrix[i-1][j-1] == '1':  dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
else:                        dp[i][j] = 0
```
A `'1'` cell extends a square exactly when the cell above, the cell left, and the diagonal cell above-left can each already support a square of that size. The side is limited by the **smallest** of the three, plus this cell itself.

**Base Cases:**
- Row 0 and column 0 of `dp` are all 0 (the padding border) — they exist so `i-1` / `j-1` never go negative.
- A `'1'` on the matrix border gives `dp = 1` (its other neighbors are the zero border).
- Track `max_side = max(max_side, dp[i][j])`; answer = `max_side * max_side`.

**Intuition (Why This Works):**
A square ending at `(i,j)` must be built out of three smaller squares that end one cell up, one cell left, and one cell up-left — all three must be at least `k-1` to make a `k×k` square. This is why we take the **min** of the three: any one being too small caps the square, preserving the square shape (min prevents rectangles). DP applies because the side length at each cell depends only on three already-computed neighbor cells.

**Step-by-Step Procedure:**
1. If the matrix is empty, return 0.
2. Build a `(m+1) × (n+1)` table of zeros; set `max_side = 0`.
3. For `i` from 1 to `m`, for `j` from 1 to `n`:
4. If `matrix[i-1][j-1] == '1'`: `dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`.
5. Update `max_side`.
6. Return `max_side * max_side`.

**Worked Example (Dry Run):**
Input: `matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]`.

```
matrix:                   DP (with 0 padding):
1 0 1 0 0                 0 0 0 0 0 0
1 0 1 1 1                 0 1 0 1 0 0
1 1 1 1 1                 0 1 0 1 1 1
1 0 0 1 0                 0 1 1 1 2 2
                          0 1 0 0 1 0
```

Cell-by-cell (dp index = matrix index + 1):
- `dp[1][1]`: `matrix[0][0]='1'` → `1 + min(0,0,0) = 1`.
- `dp[2][4]`: `'1'` → `1 + min(dp[1][4]=1, dp[2][3]=1, dp[1][3]=1) = 2` — first 2×2 block (matrix rows 1-2, cols 3-4 are all `'1'`).
- `dp[3][4]`: `'1'` → `1 + min(dp[2][4]=1, dp[3][3]=1, dp[2][3]=1) = 2` — still capped at 2 because `dp[3][3]` is only 1 (matrix[2][2] is `'1'` but matrix[1][1] is `'0'`).
- `dp[3][5]`: `'1'` → `1 + min(dp[2][5]=1, dp[3][4]=2, dp[2][4]=1) = 2` — the cap is `dp[2][5]` (only 1), so 2.
- `dp[4][4]`: `matrix[3][3]='1'` → `1 + min(dp[3][4]=2, dp[4][3]=0, dp[3][3]=1) = 1` — the `'0'` at `dp[4][3]` caps it.
- `max_side` never exceeds 2 → area = `2 × 2 = 4`.

**Final answer: 4.**

**Code:**
```python
def maximal_square(matrix: list) -> int:
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    # dp[i][j] = side of the largest all-'1' square ending at (i-1, j-1).
    # The 0-padded border makes the first row/column compute safely.
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_side = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if matrix[i - 1][j - 1] == '1':
                # A bigger square needs all three neighbors to already support it:
                # above, left, and diagonal. The smallest of the three is the cap.
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # square from above
                    dp[i][j - 1],      # square from left
                    dp[i - 1][j - 1]   # square from the diagonal
                )
                max_side = max(max_side, dp[i][j])
    return max_side * max_side  # Area = side²


# Space-optimized version: only the previous row is needed.
def maximal_square_optimized(matrix: list) -> int:
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    prev = [0] * (n + 1)      # row i-1 of dp
    max_side = 0
    for i in range(1, m + 1):
        curr = [0] * (n + 1)  # row i of dp
        for j in range(1, n + 1):
            if matrix[i - 1][j - 1] == '1':
                # prev[j]=above, curr[j-1]=left, prev[j-1]=diagonal.
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
                max_side = max(max_side, curr[j])
        prev = curr           # slide the window down one row
    return max_side * max_side
```

**Complexity:**
- Time: O(m×n)
- Space: O(m×n) tab, O(n) optimized

**Common Mistakes & Edge Cases:**
- Forgetting to multiply by itself at the end (returning the side, not the area).
- Treating cells as integers instead of the characters `'1'`/`'0'` — `matrix[i][j] == 1` is False for the string `'1'`.
- Using `max` of the three neighbors instead of `min` — that creates rectangles/slanted shapes, not squares.
- Empty matrix or a matrix with only `'0'`s must return 0.
- A single `'1'` anywhere must yield area 1.

---

## Maximal Rectangle

**Problem Explanation:**
Given an `m×n` matrix of characters `'1'` and `'0'`, find the area of the largest **rectangle** (any width × height) containing only `'1'`s. Input: the matrix; output: the integer area. Unlike Maximum Square, width and height are independent — so we reuse a classic 1D tool (Largest Rectangle in Histogram) on top of a DP-computed height table. Example: the matrix below has answer 6.

**State Definition:**
`heights[j]` (after processing row `i`) = number of consecutive `'1'`s ending at row `i` in column `j` (the height of the column-`j` bar above and including row `i`).

**Recurrence Relation:**
```
if matrix[i][j] == '1':  heights[j] = heights[j] + 1   (bar keeps growing)
else:                    heights[j] = 0                (bar resets)
```
Then `max_area = max(max_area, largest_rectangle_in_histogram(heights))` for every row. Within the histogram, a bar of height `h` at index `i` can extend left to the previous strictly-smaller bar and right to the next strictly-smaller bar, giving a rectangle `h × width`.

**Base Cases:**
- Before any row, `heights = [0]*n` — empty bars.
- `largest_rectangle` appends a sentinel `0` to flush every remaining bar at the end.

**Intuition (Why This Works):**
Any all-`'1'` rectangle has a bottom edge on some row. If we treat each column as a bar whose height is the number of consecutive `'1'`s ending at that row, then every rectangle resting on that row is just a rectangle inside that histogram. DP applies because bar heights build incrementally row by row (each cell extends or resets its column's bar), and the monotonic stack answers "for each bar, how far can it stretch left/right?" in O(n). The choice per cell is binary: extend the column's bar or reset it.

**Step-by-Step Procedure:**
1. If the matrix is empty, return 0.
2. Initialize `heights = [0]*n` and `max_area = 0`.
3. For each row `i`:
4. Update each `heights[j]` with the extend/reset rule.
5. Compute `largest_rectangle(heights)` and update `max_area`.
6. Return `max_area`.

**Worked Example (Dry Run):**
Input: the same matrix as Maximum Square.
```
row 0: heights = [1,0,1,0,0]   → largest histogram rect = 1
row 1: heights = [2,0,2,1,1]   → largest = 2  (the two 1-wide bars of height 2; also 3 cols of height 1)
row 2: heights = [3,1,3,2,2]   → largest = 6  (height 2 over columns 2,3,4)
row 3: heights = [1,0,0,1,0]   → largest = 1
```
`largest_rectangle([3,1,3,2,2])` step by step (sentinel `0` appended → `[3,1,3,2,2,0]`):
- Stack walk: push index 0 (height 3). At height 1, pop bar 0 → `3×1 = 3`. Push 1.
- Height 3: push 2. Height 2: pop bar 2 → `3×(3-1-1) = 3`. Push 3. Height 2: push 4.
- Sentinel 0: pop bar 4 → `2×(5-3-1) = 2`; pop bar 3 → `2×(5-1-1) = 6`; pop bar 1 → `1×5 = 5`.
- Max across all rows = 6.

**Final answer: 6.**

**Code:**
```python
def maximal_rectangle(matrix: list) -> int:
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    heights = [0] * n            # bar heights for the current bottom row
    max_area = 0
    for i in range(m):
        # Rebuild the histogram: extend bars through '1's, reset at '0's.
        for j in range(n):
            heights[j] = heights[j] + 1 if matrix[i][j] == '1' else 0
        max_area = max(max_area, largest_rectangle(heights))
    return max_area


def largest_rectangle(heights: list) -> int:
    # Monotonic-stack histogram solver: for each bar find the stretch it can span.
    stack = []
    max_area = 0
    heights.append(0)            # sentinel: forces every bar to be popped at the end
    for i, h in enumerate(heights):
        # While the current height is shorter, the bar on top can no longer extend.
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            # Width = distance to the previous (shorter) bar on the stack.
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    heights.pop()                # remove the sentinel we appended (restore input)
    return max_area
```

**Complexity:**
- Time: O(m×n) (each histogram scan is O(n), done for all m rows)
- Space: O(n)

**Common Mistakes & Edge Cases:**
- Forgetting that `largest_rectangle` temporarily appends `0` to `heights` and must pop it back — otherwise the input list grows by one each row.
- Rebuilding heights from scratch each row instead of incrementing — that becomes O(m²n).
- A row of all `'0'`s must reset the heights to all zeros.
- All-`'1'` matrix: answer is `m × n` (the whole matrix is a rectangle).
- The stack width math (`i - stack[-1] - 1`) is the classic off-by-one trap — double-check it with a small histogram like `[2,1,5,6,2,3]` → 10.

---

## Count Squares in Binary Matrix

**Problem Explanation:**
Given an `m×n` matrix of integers `1` and `0`, count the total number of squares of **all sizes** (1×1, 2×2, 3×3, ...) that consist entirely of `'1'`s. Input: the matrix; output: the integer count. Example: a 2×2 block of ones contains 5 squares (four 1×1 + one 2×2). This is a counting variant of Maximum Square.

**State Definition:**
`dp[i][j]` = side length of the largest square of `'1'`s whose bottom-right corner is `(i, j)` — which also equals the number of square sizes (1×1 up to that side) that end at this cell.

**Recurrence Relation:**
```
if matrix[i][j] == 1:
    if i == 0 or j == 0:   dp[i][j] = 1
    else:                  dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
total += dp[i][j]
```
Same "min of three neighbors + 1" rule as Maximum Square; the sum accumulates counts because each cell that can support a `k×k` square also supports every smaller square of sizes `1..k`.

**Base Cases:**
- Row 0 / column 0 cells: `dp[i][j] = 1` if the cell is `1` (only a 1×1 square can end on the border).
- `'0'` cells contribute `dp = 0` and are skipped.
- `total` starts at 0 and adds each `dp[i][j]`.

**Intuition (Why This Works):**
The `dp` value at a cell is simultaneously "largest square side" AND "number of square sizes ending here" — if the largest square ending at a cell has side `k`, then that cell is the bottom-right corner of exactly `k` squares (sizes 1, 2, ..., k). DP applies because the same three-neighbor min recurrence gives the largest side, and summing those per-cell counts partitions every square in the matrix exactly once (each square is counted at its unique bottom-right corner).

**Step-by-Step Procedure:**
1. If the matrix is empty, return 0.
2. Build `dp` with the same shape; set `total = 0`.
3. For `i` from 0 to `m-1`, for `j` from 0 to `n-1`:
4. If `matrix[i][j] == 1`: set `dp[i][j]` (border → 1, else the min-of-3 + 1).
5. Add `dp[i][j]` to `total`.
6. Return `total`.

**Worked Example (Dry Run):**
Input: `matrix = [[0,1,1,1,0],[1,1,1,1,0],[0,1,1,1,0],[0,0,1,1,0]]`.

```
dp:
[0, 1, 1, 1, 0]
[1, 1, 2, 2, 0]
[0, 1, 2, 3, 0]
[0, 0, 1, 2, 0]
```

Cell-by-cell (notable ones):
- Row 0: each `'1'` → `1` (border). `dp[1][0]=1` (border). Row 1: `dp[1][1] = 1 + min(1,1,1) = 2`; `dp[1][2] = 1 + min(1,1,1) = 2`.
- `dp[2][3] = 1 + min(2,2,2) = 3` — the 3×3 square ending at matrix rows 0-2, cols 1-3.
- `dp[3][3] = 1 + min(2,1,1) = 2` (the `'0'` at `dp[3][2]`? no — `min(dp[2][3]=3, dp[3][2]=1, dp[2][2]=2) = 1` → 2).
- `dp[3][4]` is `'0'` → 0.
- Sum: 1+1+1+1+1+2+2+1+2+3+1+2 = 18.

**Final answer: 18 squares.**

**Code:**
```python
def count_squares(matrix: list) -> int:
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    # dp[i][j] = largest square side ending at (i,j) = count of square sizes ending here.
    dp = [[0] * n for _ in range(m)]
    total = 0
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 1:
                if i == 0 or j == 0:
                    dp[i][j] = 1                 # border cell: only a 1×1 square
                else:
                    # Largest square ending here, capped by the smallest neighbor.
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
                total += dp[i][j]                # each dp value counts all sizes 1..side
    return total
```

**Complexity:**
- Time: O(m×n)
- Space: O(m×n)

**Common Mistakes & Edge Cases:**
- Forgetting the border rule (`i == 0 or j == 0`) — the min-of-3 would read out-of-range or rely on a zero-padded table that is not built here.
- Summing `dp` values but using `max` instead of `min` in the recurrence — overcounts squares that don't exist.
- All-`'1'` matrix: the count is `1 + 4 + 9 + ...` per prefix; e.g. a 2×2 all-ones block → 5.
- Empty matrix or all-`'0'` matrix → 0.
- A single `'1'` → exactly 1 (the 1×1 square).

---

## Burst Balloons

**Problem Explanation:**
Given an array `nums` of `n` balloons, each with a number written on it. When you burst balloon `i`, you collect `nums[left] × nums[i] × nums[right]` coins, where `left` and `right` are the nearest **still-unburst** neighbors of `i` (or the boundary `1` if none exist). You may burst balloons in any order. Find the maximum total coins. Input: the list of balloon numbers; output: the integer maximum. The boundary trick is key: imagine a virtual balloon `1` at each end so the formula always has a left and right neighbor.

**State Definition:**
`dp[l][r]` = maximum coins obtainable by bursting all balloons **strictly between** indices `l` and `r` of the augmented array `[1] + nums + [1]` (exclusive of `l` and `r`, which stay unburst as boundaries).

**Recurrence Relation:**
```
dp[l][r] = max over k in (l, r):   nums[l] * nums[k] * nums[r] + dp[l][k] + dp[k][r]
```
Think backwards: make balloon `k` the **LAST** balloon burst in the range `(l, r)`. When `k` finally bursts, all the others in `(l, r)` are already gone, so its only neighbors are the boundary balloons at `l` and `r` — the coin payoff is fixed. The balloons to the left (`(l,k)`) and right (`(k,r)`) were already burst optimally before, and those coin totals are independent.

**Base Cases:**
- `dp[l][r] = 0` whenever `r - l <= 1` — no balloons between the boundaries, nothing to burst.
- The augmented array `[1] + nums + [1]` supplies the fixed boundary coins; the final answer is `dp[0][n-1]`.

**Intuition (Why This Works):**
The order of bursting matters and a naive brute force is O(n!), but the "last balloon" perspective tames it: once you decide which balloon bursts last in a range, the left and right halves become **independent** subproblems (their bursts happen before `k` and never interact with each other). DP applies because every subproblem is a contiguous interval, and intervals of smaller length are solved first. The choice at each step is "which balloon is the last to burst here?".

**Step-by-Step Procedure:**
1. Build `nums = [1] + nums + [1]`; let `n = len(nums)`.
2. Build an `n×n` table of zeros.
3. For `length` from 2 to `n-1` (the gap between the two boundaries):
4. For `i` from 0 to `n - length - 1` (left boundary):
5. Set `j = i + length` (right boundary).
6. For `k` from `i+1` to `j-1` (candidate last balloon):
7. `dp[i][j] = max(dp[i][j], nums[i]*nums[k]*nums[j] + dp[i][k] + dp[k][j])`.
8. Return `dp[0][n-1]`.

**Worked Example (Dry Run):**
Input: `nums = [3, 1, 5, 8]`. Augmented: `[1, 3, 1, 5, 8, 1]`, so `n = 6`.

```
dp[l][r] = max coins from bursting all balloons between l and r (exclusive).
Boundary values: index 0=1, 1=3, 2=1, 3=5, 4=8, 5=1

Length 2: dp[l][l+2] (exactly one balloon between the boundaries)
  dp[0][2] = 1*3*1 = 3     dp[1][3] = 3*1*5 = 15
  dp[2][4] = 1*5*8 = 40    dp[3][5] = 5*8*1 = 40

Length 3: dp[l][l+3] (two balloons between)
  dp[0][3]: k=1: 1*3*5 + dp[1][3]=15 → 30;  k=2: 1*1*5 + dp[0][2]=3 → 8   → best 30
  dp[1][4]: k=2: 3*1*8 + dp[2][4]=40 → 64;  k=3: 3*5*8 + dp[1][3]=15 → 135 → best 135
  dp[2][5]: k=3: 1*5*1 + dp[3][5]=40 → 45;  k=4: 1*8*1 + dp[2][4]=40 → 48 → best 48

Length 4: dp[l][l+4] (three balloons between)
  dp[0][4]: k=1: 1*3*8 + dp[1][4]=135 → 159  ← best (k=2 → 51, k=3 → 70)
  dp[1][5]: k=2: 3*1*1 + dp[2][5]=48 → 51;  k=3: 3*5*1 + dp[1][3]=15 + dp[3][5]=40 → 70
            k=4: 3*8*1 + dp[1][4]=135 → 159  → best 159

Length 5: dp[0][5] (the whole array between the two outer 1s)
  k=1: 1*3*1 + dp[1][5]=159 → 162
  k=2: 1*1*1 + dp[0][2]=3 + dp[2][5]=48 → 52
  k=3: 1*5*1 + dp[0][3]=30 + dp[3][5]=40 → 75
  k=4: 1*8*1 + dp[0][4]=159 → 167  ← best
```

The winning strategy: burst balloon 1 (15 coins), then 5 (120), then 3 (24), then 8 (8) → 15 + 120 + 24 + 8 = 167.

**Final answer: 167.**

**Code:**
```python
def max_coins_tab(nums: list) -> int:
    nums = [1] + nums + [1]  # sentinel boundaries: always have a neighbor to multiply
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    # Fill by increasing range length: smaller intervals must be solved first.
    for length in range(2, n):          # length = gap between the two boundaries
        for i in range(n - length):     # i = left boundary
            j = i + length              # j = right boundary
            # Try each balloon k as the LAST one to burst in (i, j).
            for k in range(i + 1, j):
                # When k bursts, neighbors are the boundaries i and j (everything
                # between is already gone). Add the coins from the already-burst
                # left and right halves, which are independent subproblems.
                dp[i][j] = max(dp[i][j],
                               nums[i] * nums[k] * nums[j] + dp[i][k] + dp[k][j])
    return dp[0][n - 1]
```

**Complexity:**
- Time: O(n³) (three nested loops over intervals and split points)
- Space: O(n²) where n = len(nums) + 2 (with sentinels)

**Common Mistakes & Edge Cases:**
- Forgetting the sentinel `1`s — without them the first/last balloon would need special cases.
- Thinking forwards ("first to burst") instead of backwards ("last to burst") — the forward version's neighbors are not fixed.
- Using the *mutated* augmented `nums` for index math — the array grew by 2; index carefully.
- A single balloon `[5]`: augmented `[1,5,1]`, answer `1*5*1 = 5`.
- Empty array `[]`: augmented `[1,1]`, the loops never run, answer 0.

---

## Stone Game III

**Problem Explanation:**
Alice and Bob play a game on an array of integers. On each turn, a player removes 1, 2, or 3 stones from the **front** of the array and takes their sum as points. Both play optimally (each assumes the opponent will also maximize their own score). Return `"Alice"`, `"Bob"`, or `"Tie"` depending on who ends with the higher total. Input: the list of stone values; output: a string.

**State Definition:**
`dp[i]` = the maximum **total score** the player whose turn it is can collect from the suffix `values[i:]` (playing optimally from here on). The opponent then receives the rest: `suffix[i] - dp[i]`.

**Recurrence Relation:**
```
dp[i] = max over take in {1,2,3} (with i+take <= n):   suffix[i] - dp[i+take]
```
If the current player takes `take` stones, they collect `taken = suffix[i] - suffix[i+take]` immediately. The opponent then plays optimally from `i+take` and will collect `dp[i+take]` of the remaining `suffix[i+take]`. So the current player's total is `taken + (suffix[i+take] - dp[i+take]) = suffix[i] - dp[i+take]`.

**Base Cases:**
- `dp[n] = 0` — an empty suffix yields zero points.
- `suffix[i] = sum(values[i:])` — precomputed so each `take` query is O(1).

**Intuition (Why This Works):**
This is a zero-sum game: whatever the current player takes, the opponent takes from the same pool, so `total = mine + opponent's`. Working **backwards** from the end, each position's decision only needs the outcomes of the three positions ahead — perfect optimal substructure. The choice at each step is "take 1, 2, or 3 stones?", and the minimax logic (maximize my score, assuming the opponent maximizes theirs) is captured by subtracting the opponent's optimal total.

**Step-by-Step Procedure:**
1. Let `n = len(values)`; build `dp` of size `n+1` and a `suffix` array of size `n+1`.
2. Set `dp[n] = 0`; fill `suffix` from the back (`suffix[i] = suffix[i+1] + values[i]`).
3. For `i` from `n-1` down to `0`:
4. For `take` in `{1,2,3}` with `i+take <= n`:
5. `dp[i] = max(dp[i], suffix[i] - dp[i+take])`.
6. Compare Alice's total `dp[0]` against Bob's `suffix[0] - dp[0]` and return the verdict.

**Worked Example (Dry Run):**
Input: `values = [1, 2, 3, 7]` (total 13).

```
suffix = [13, 12, 10, 7, 0]
dp[n]  = dp[4] = 0

dp[3]: take 1 → 7 - 0 = 7                → dp[3] = 7
       (player facing [7] takes it all)
dp[2]: take 1 → 10 - 7 = 3
       take 2 → 10 - 0 = 10              → dp[2] = 10
       (player facing [3,7] takes both)
dp[1]: take 1 → 12 - 10 = 2
       take 2 → 12 - 7 = 5
       take 3 → 12 - 0 = 12              → dp[1] = 12
       (player facing [2,3,7] takes all)
dp[0]: take 1 → 13 - 12 = 1
       take 2 → 13 - 10 = 3
       take 3 → 13 - 7 = 6               → dp[0] = 6
```

Alice's best total is 6 (taking 1+2+3), leaving `[7]` for Bob → Bob gets 7. Compare `dp[0] = 6` vs `suffix[0] - dp[0] = 7`.

**Final answer: "Bob".**

**Code:**
```python
def stone_game_iii(values: list) -> str:
    n = len(values)
    # dp[i] = best TOTAL score the player to move can take from values[i:].
    # Initialize with -inf so max() over the three take options works.
    dp = [float('-inf')] * (n + 1)
    dp[n] = 0                            # empty suffix: nothing left to take
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + values[i]   # suffix sums for O(1) range totals

    for i in range(n - 1, -1, -1):
        for take in range(1, 4):                 # can take 1, 2, or 3 stones
            if i + take <= n:
                # If I take 'take' stones, the opponent optimally gets dp[i+take]
                # out of the remaining suffix → my total is suffix[i] - that.
                dp[i] = max(dp[i], suffix[i] - dp[i + take])

    # dp[0] is Alice's best total; Bob gets the rest of the whole sum.
    if dp[0] > suffix[0] - dp[0]:
        return "Alice"
    elif dp[0] < suffix[0] - dp[0]:
        return "Bob"
    return "Tie"
```

**Complexity:**
- Time: O(n)
- Space: O(n)

**Common Mistakes & Edge Cases:**
- Confusing `dp[i]` as a *score* versus an *advantage* — this recurrence stores the score; the verdict comes from `dp[0]` vs `suffix[0] - dp[0]`.
- Forgetting `dp[n] = 0` or the `i + take <= n` bound — takes would read past the end.
- Misreading "from the front" as "from either end" — that is a different game (Predict the Winner).
- A single stone: whoever takes it wins unless it is worth 0 → careful with the tie comparison.
- If the totals come out equal (e.g. `[1,2,3,6]`), return `"Tie"`.

---

## Game Theory DP

### Predict the Winner (Nim-style)

**Problem Explanation:**
Given an array of non-negative scores, two players alternate. On each turn a player may take the score from either the left or the right end of the remaining array. Player 1 (you) wins if your final total is **greater than or equal to** the opponent's total. Both play optimally. Input: the array; output: a boolean — whether player 1 can force a win or tie.

**State Definition:**
`dp[i][j]` = the maximum **net advantage** (my score minus opponent's score) the player to move can achieve from the subarray `nums[i..j]`.

**Recurrence Relation:**
```
dp[i][j] = max( nums[i] - dp[i+1][j], nums[j] - dp[i][j-1] )
```
If I take the left end `nums[i]`, I gain it, and the opponent then nets `dp[i+1][j]` from the rest — which is my loss. So my net is `nums[i] - dp[i+1][j]`. Same reasoning for taking the right end; pick the better.

**Base Cases:**
- `dp[i][i] = nums[i]` — with one number left, the player takes it outright.
- Subarrays grow by increasing length; the answer is `dp[0][n-1] >= 0`.

**Intuition (Why This Works):**
This is a minimax interval DP: my gain is directly the opponent's loss, so every move's value is "what I take now minus the opponent's best net on what's left". DP applies because the state is a contiguous subarray and each move shrinks it from one end — smaller intervals solve first. The choice at each step is "left end or right end?".

**Step-by-Step Procedure:**
1. Build an `n×n` table.
2. For `i` from `n-1` down to `0`:
3. Set `dp[i][i] = nums[i]`.
4. For `j` from `i+1` to `n-1`:
5. `dp[i][j] = max(nums[i] - dp[i+1][j], nums[j] - dp[i][j-1])`.
6. Return `dp[0][n-1] >= 0`.

**Worked Example (Dry Run):**
Input: `nums = [1, 5, 2]`.

```
dp[i][i] = nums[i]: dp[0][0]=1, dp[1][1]=5, dp[2][2]=2
dp[1][2] = max(5 - dp[2][2]=2, 2 - dp[1][1]=5) = max(3, -3) = 3
dp[0][1] = max(1 - dp[1][1]=5, 5 - dp[0][0]=1) = max(-4, 4) = 4
dp[0][2] = max(1 - dp[1][2]=3, 2 - dp[0][1]=4) = max(-2, -2) = -2
```

Player 1 can net at most `-2` — whatever they take, player 2 grabs the 5. Player 1 loses.

**Final answer: `False`.** (Counter-check with `[1, 5, 233, 7]`: player 1 takes 7, then 233 → net `7 - dp[1][2]` where `dp[1][2] = max(5-233, 233-5) = 228` → negative. Taking 1 first: `dp[1][3] = max(5 - dp[2][3], 7 - dp[1][2]) = max(5-233, 7-228) = -221`, so net `1 - (-221) = 222 >= 0` → True.)

**Code:**
```python
def predict_the_winner(nums: list) -> bool:
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    # dp[i][j] = max net score (mine - opponent's) the player to move can get
    # from the subarray [i, j]. Fill by increasing interval size (i downward).
    for i in range(n - 1, -1, -1):
        dp[i][i] = nums[i]               # one number left → take it outright
        for j in range(i + 1, n):
            # Take left end: gain nums[i], then I *lose* dp[i+1][j] to the
            # opponent's optimal play on the rest. Same for the right end.
            dp[i][j] = max(nums[i] - dp[i + 1][j],
                           nums[j] - dp[i][j - 1])
    return dp[0][n - 1] >= 0             # player 1 wins on any non-negative net
```

**Complexity:**
- Time: O(n²)
- Space: O(n²)

**Common Mistakes & Edge Cases:**
- Forgetting the minus sign — it is `nums[i] - dp[i+1][j]`, not `nums[i] + dp[i+1][j]` (the opponent's gains are my losses).
- A single-element array always returns True.
- Equal final scores count as a win for player 1 (the `>= 0`).
- Building the table top-left to bottom-right reads unsolved intervals — fill by increasing length.

### Nim Game

**Problem Explanation:**
One pile of `n` stones. Two players alternate removing 1, 2, or 3 stones. The player who takes the **last stone** wins. Given `n`, determine whether you (moving first) can force a win. Input: an integer `n`; output: a boolean. Classic insight: multiples of 4 are losing positions — whatever you take (1-3), your opponent can complete the remaining stones to the next multiple of 4.

**State Definition:**
Not needed as a table — this reduces to a closed-form number-theory answer on `n`.

**Recurrence Relation (derivation):**
A position is winning if there exists a move to a losing position. Position `n` is losing when `n` is a multiple of 4: from `4k`, every move leaves `4k-1, 4k-2, or 4k-3` stones, from which the opponent can respond to bring it back to `4(k-1)`. Formally: `win(n) = not (n % 4 == 0)`.

**Base Cases:**
- `n = 1, 2, 3`: winning (take them all).
- `n = 4`: losing (any take leaves a winning count for the opponent).

**Intuition (Why This Works):**
Both players can always adjust their take so that each pair of turns consumes exactly 4 stones (I take `x`, opponent takes `4 - x`). Starting from a multiple of 4, the opponent can force the pattern back to 4 repeatedly and take the last stone. From any non-multiple, I first take `n mod 4` stones and hand the opponent a multiple of 4. This is DP solved in closed form.

**Step-by-Step Procedure:**
1. Compute `n % 4`.
2. If it is 0, return `False` (I'm doomed). Otherwise return `True`.

**Worked Example (Dry Run):**
- `n = 1`: `1 % 4 = 1 ≠ 0` → True (take the stone).
- `n = 4`: `4 % 4 = 0` → False (I take 1-3, opponent finishes).
- `n = 5`: `5 % 4 = 1` → True (take 1 → 4 left for opponent, which is losing for them).
- `n = 7`: `7 % 4 = 3` → True (take 3 → 4 left for opponent).

**Final answer:** `True` for `n = 1, 2, 3, 5, 6, 7, ...`; `False` for `n = 4, 8, 12, ...`.

**Code:**
```python
def can_win_nim(n: int) -> bool:
    # Multiples of 4 are losing positions: the opponent can always mirror my
    # take to keep the count a multiple of 4. Any other n wins by first
    # leaving the opponent a multiple of 4.
    return n % 4 != 0
```

**Complexity:**
- Time: O(1)
- Space: O(1)

**Common Mistakes & Edge Cases:**
- `n = 0` has no stones — the puzzle normally assumes `n >= 1`; guard it if needed.
- Confusing "last stone wins" with "cannot move loses" (misère variants differ).
- Testing large multiples of 4 — the closed form is exact, no loop needed.

### Nim Game II (DP version)

**Problem Explanation:**
Same game as Nim Game (take 1-3 stones per turn, last stone wins) but solved with an explicit DP table so the pattern is visible programmatically. Input: an integer `n`; output: a boolean — whether the first player wins. This is the general template you'd use if the move set were irregular.

**State Definition:**
`dp[i]` = True iff the player to move **wins** with `i` stones remaining.

**Recurrence Relation:**
```
dp[i] = (not dp[i-1]) or (not dp[i-2]) or (not dp[i-3])
```
A position is winning if **at least one** legal move leads to a position that is losing for the opponent (the opponent then cannot force a win).

**Base Cases:**
- `dp[1] = dp[2] = dp[3] = True` — take the remaining stones and win immediately.
- `dp[0]` would be losing by definition (no move), used implicitly for small `n`.

**Intuition (Why This Works):**
Game-tree reasoning collapses into a 1D DP because the only state that matters is the stone count: from `i` stones, each move lands in exactly one of `i-1`, `i-2`, `i-3`, whose win/loss status is already known. This is the "winning iff some move leads to a losing state" principle, computed bottom-up. The choice per state is "which take size (1, 2, or 3) leaves my opponent a losing position?".

**Step-by-Step Procedure:**
1. If `n <= 3`, return True.
2. Build `dp` of size `n+1`; set `dp[1] = dp[2] = dp[3] = True`.
3. For `i` from 4 to `n`:
4. `dp[i] = (not dp[i-1]) or (not dp[i-2]) or (not dp[i-3])`.
5. Return `dp[n]`.

**Worked Example (Dry Run):**
Input: `n = 5`.

```
dp[1] = T, dp[2] = T, dp[3] = T
dp[4] = (not T) or (not T) or (not T) = False      → 4 stones: I lose
dp[5] = (not False) or (not T) or (not T) = True   → take 1, hand 4 to opponent
```

**Final answer: `True`.** The table reproduces the closed form: `dp[i] = True` except for multiples of 4.

**Code:**
```python
def nim_game_dp(n: int) -> bool:
    if n <= 3:
        return True                  # can take all the stones at once
    dp = [False] * (n + 1)
    dp[1] = dp[2] = dp[3] = True     # base: one move ends the game
    for i in range(4, n + 1):
        # Winning if any legal take (1, 2, or 3) hands the opponent a
        # LOSING position. `not dp[i - take]` is "opponent loses".
        dp[i] = not dp[i - 1] or not dp[i - 2] or not dp[i - 3]
    return dp[n]
```

**Complexity:**
- Time: O(n)
- Space: O(n)

**Common Mistakes & Edge Cases:**
- Using AND instead of OR (a position is winning if *any* move works, not all).
- Forgetting to special-case `n <= 3` before indexing `dp[1..3]`.
- `n = 0`: conventionally a losing position (no moves); the loop would read `dp` correctly if `dp[0]` were False.
- This exact recurrence also yields the closed form `n % 4 != 0` — use the formula for speed, the table for clarity.

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
│ Predict Winner           │ Minimax interval     │ O(n²)    │ O(n²)    │ take - opponent_best        │
│ Nim Game                 │ Number theory        │ O(1)     │ O(1)     │ n % 4 != 0                   │
│ Nim Game II              │ 1D win/loss DP       │ O(n)     │ O(n)     │ any move → opponent loses   │
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
