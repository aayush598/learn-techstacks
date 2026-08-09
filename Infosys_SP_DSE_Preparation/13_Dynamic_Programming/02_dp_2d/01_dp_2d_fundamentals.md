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

**🔗 Practice Link:** [Unique Paths](https://leetcode.com/problems/unique-paths/)

**Problem Explanation:**
A robot starts at the top-left corner of an `m×n` grid and can only move **right** or **down** one cell at a time. It must reach the bottom-right corner. Count how many distinct paths exist. The input is two integers `m` and `n`; the output is the total number of unique paths. This is a **counting** problem (not a "best of" problem), so we sum values — never take a min or max.

**State Definition:**
`dp[i][j]` = number of distinct paths to reach cell `(i, j)` from the top-left cell `(0, 0)`.

**Recurrence Relation:**
`dp[i][j] = dp[i - 1][j] + dp[i][j - 1]`

Every path into `(i, j)` comes through exactly one of two previous cells: the cell above `(i-1, j)` (last move was **down**) or the cell to the left `(i, j-1)` (last move was **right**), so the counts simply add.

**Base Cases:**
- `dp[0][0] = 1` — there is exactly one path (do nothing) to reach the start cell.
- First row `dp[0][j] = 1` — the only route along the top edge is moving right repeatedly.
- First column `dp[i][0] = 1` — the only route along the left edge is moving down repeatedly.

**Intuition (Why This Works):**
The answer for a large grid is built from answers for smaller grids: reaching any cell depends only on its two "parent" cells. That is the **optimal substructure** of DP. The choice at each cell is "did I arrive from above or from the left?" — and because both are counted, no path is missed and no path is double-counted (every path has a unique last move). Storing each `dp[i][j]` once lets us reuse it for every cell to its right and below.

**Step-by-Step Procedure:**
1. Create an `m×n` table `dp`.
2. Set `dp[0][0] = 1`.
3. Fill row 0: every `dp[0][j] = 1` (straight right).
4. Fill column 0: every `dp[i][0] = 1` (straight down).
5. For `i` from 1 to `m-1`, for `j` from 1 to `n-1`: set `dp[i][j] = dp[i-1][j] + dp[i][j-1]`.
6. Fill row by row, left to right, so both dependencies are already computed.
7. Return `dp[m-1][n-1]`.

**Worked Example (Dry Run):**
Input: `m = 3, n = 3`.

```
DP Table fill order (top-left corner is the start):
      j=0  j=1  j=2
i=0    1    1    1
i=1    1    2    3
i=2    1    3    6   ← dp[2][2] = 6
```

Cell-by-cell:
- `dp[0][0] = 1` (base case: the start).
- `dp[0][1] = 1`, `dp[0][2] = 1` (first row: only "move right" exists).
- `dp[1][0] = 1`, `dp[2][0] = 1` (first column: only "move down" exists).
- `dp[1][1] = dp[0][1] + dp[1][0] = 1 + 1 = 2` — paths "right,down" and "down,right".
- `dp[1][2] = dp[0][2] + dp[1][1] = 1 + 2 = 3` — R,R,D / R,D,R / D,R,R.
- `dp[2][1] = dp[1][1] + dp[2][0] = 2 + 1 = 3` — D,D,R / D,R,D / R,D,D.
- `dp[2][2] = dp[1][2] + dp[2][1] = 3 + 3 = 6` — all 6 orderings of "2 downs + 2 rights".

**Final answer: 6.**

**Code:**
```python
def unique_paths_2d(m: int, n: int) -> int:
    # dp[i][j] = number of paths to reach cell (i, j) from (0, 0).
    # The first row and first column are all 1s: only one route along an edge.
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):          # skip row 0 (already all 1s)
        for j in range(1, n):      # skip col 0 (already all 1s)
            # Paths into (i,j) = paths from above + paths from the left.
            # Both are already computed thanks to the row-major fill order.
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]


def unique_paths_optimized(m: int, n: int) -> int:
    # dp[j] = number of paths to the CURRENT row's column j.
    # Reuses a single row: after processing a row, dp IS that row.
    dp = [1] * n                    # row 0: all 1s (only moving right)
    for _ in range(1, m):           # for each subsequent row
        for j in range(1, n):       # first column stays 1 (only moving down)
            # dp[j] still holds the "from above" value of the previous row;
            # dp[j-1] already holds the "from left" value of this row.
            # Adding them produces this row's value for column j.
            dp[j] += dp[j - 1]
    return dp[n - 1]
```

**Complexity:**
- Time: O(m×n)
- Space: O(m×n) for `unique_paths_2d`, O(n) for `unique_paths_optimized`

**Common Mistakes & Edge Cases:**
- Off-by-one on the return: the bottom-right cell is `dp[m-1][n-1]`, not `dp[m][n]`.
- Filling with `[[1]*n]*m` shares one row object — every mutation affects all rows. Always use a list comprehension.
- A `1×1` grid must return 1 (the single cell is both start and finish).
- A single row (`m=1`) or single column (`n=1`) has exactly 1 path — the optimized loop must not touch index 0.

---

### Unique Paths with Obstacles

**🔗 Practice Link:** [Unique Paths with Obstacles](https://leetcode.com/problems/unique-paths-ii/)

**Problem Explanation:**
Same grid as above (move right/down, count paths from top-left to bottom-right) but now some cells are blocked. A blocked cell (value `1`) cannot be entered. The input is an `m×n` grid of `0`s and `1`s; return the number of valid paths that never step on a `1`. If the start or finish cell is itself blocked, no path exists and the answer is 0.

**State Definition:**
`dp[i][j]` = number of distinct obstacle-free paths to reach cell `(i, j)` from `(0, 0)`.

**Recurrence Relation:**
```
if grid[i][j] == 1:   dp[i][j] = 0
else:                 dp[i][j] = dp[i - 1][j] + dp[i][j - 1]   (terms with out-of-range indices = 0)
```
A blocked cell contributes nothing (zero paths pass through it); a free cell inherits the sum of its two parents, exactly like plain Unique Paths.

**Base Cases:**
- `dp[0][0] = 1` if `grid[0][0] == 0`, otherwise the whole answer is 0.
- Edge row 0 / column 0: the path count is 1 only while all earlier edge cells are free; the first obstacle on the edge zeroes out everything after it.
- `grid[m-1][n-1] == 1` → return 0 immediately.

**Intuition (Why This Works):**
Obstacles do not change the structure of the problem — paths still flow only right/down, so every free cell's count is still the sum of its above/left neighbors. The only new rule is that a blocked cell must be treated as "0 paths". DP still applies because the subproblem (paths to some cell) depends only on two smaller subproblems, and blocking a cell just clips that dependency chain.

**Step-by-Step Procedure:**
1. Check if `grid[0][0] == 1` or `grid[m-1][n-1] == 1`; if so, return 0.
2. Create an `m×n` table `dp` filled with 0.
3. Set `dp[0][0] = 1`.
4. Loop over every cell `(i, j)` in row-major order.
5. If `grid[i][j] == 1`: set `dp[i][j] = 0`.
6. Else: add `dp[i-1][j]` (if `i > 0`) and `dp[i][j-1]` (if `j > 0`) into `dp[i][j]`.
7. Return `dp[m-1][n-1]`.

**Worked Example (Dry Run):**
Input: `grid = [[0,0,0],[0,1,0],[0,0,0]]`.

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

Cell-by-cell:
- `dp[0][0] = 1`; row 0 → `1, 1, 1` (all free).
- `dp[1][0] = dp[0][0] = 1`.
- `dp[1][1]` — blocked → `0`. Both paths that used the center die here.
- `dp[1][2] = dp[0][2] + dp[1][1] = 1 + 0 = 1` — only the top-row path survives.
- `dp[2][0] = dp[1][0] = 1`.
- `dp[2][1] = dp[1][1] + dp[2][0] = 0 + 1 = 1`.
- `dp[2][2] = dp[1][2] + dp[2][1] = 1 + 1 = 2` — paths: R,R,D,D and D,D,R,R (the two that go around the obstacle).

**Final answer: 2.**

**Code:**
```python
def unique_paths_with_obstacles_tab(grid: list) -> int:
    m, n = len(grid), len(grid[0])
    # If either endpoint is blocked, no path can exist at all.
    if grid[0][0] == 1 or grid[m - 1][n - 1] == 1:
        return 0
    dp = [[0] * n for _ in range(m)]   # zeros: default "no paths" for every cell
    dp[0][0] = 1                       # exactly one way to be at the start
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                dp[i][j] = 0           # obstacle → zero paths, no parents pass through
            else:
                # Sum of the two possible last moves.
                if i > 0:
                    dp[i][j] += dp[i - 1][j]   # came from above (moved down)
                if j > 0:
                    dp[i][j] += dp[i][j - 1]   # came from left (moved right)
    return dp[m - 1][n - 1]
```

**Complexity:**
- Time: O(m×n)
- Space: O(m×n)

**Common Mistakes & Edge Cases:**
- Forgetting the early return when `grid[0][0] == 1` — `dp[0][0]` must be reachable first.
- Blocked end cell: must return 0, never something accidentally positive.
- An all-free grid must behave exactly like plain Unique Paths.
- Do not use `[[0]*n]*m` (shared rows); use a comprehension.
- Edge rows/columns after an obstacle become 0 permanently — do not reset them later.

---

## Minimum Path Sum

**Problem Explanation:**
Given an `m×n` grid of non-negative numbers, start at the top-left and move only right or down, ending at the bottom-right. Find the minimum possible sum of cell values along such a path. Input is the grid; output is the smallest path sum. This is the **optimization** twin of Unique Paths: same movement, but we keep the *best* (min) of the two parents instead of summing them.

**State Definition:**
`dp[i][j]` = minimum path sum to reach cell `(i, j)` from `(0, 0)`, including the value of cell `(i, j)` itself.

**Recurrence Relation:**
`dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])`

To reach `(i, j)` you must pay the cell's own value, plus the cheaper of reaching the cell above or the cell to the left — taking the minimum guarantees the cheapest overall path.

**Base Cases:**
- `dp[0][0] = grid[0][0]` — the path starts here and pays this cell.
- First row: `dp[0][j] = dp[0][j-1] + grid[0][j]` — forced to come from the left.
- First column: `dp[i][0] = dp[i-1][0] + grid[i][0]` — forced to come from above.

**Intuition (Why This Works):**
The cheapest way to reach a cell is the cell's value plus the cheapest way to reach its best parent — a "local" choice that provably produces the global optimum because the path is broken into independent segments by its last move. The choice at each step is "which of my two predecessors gives the smaller accumulated cost?". Storing the best cost per cell means later cells only ever look at two small values, never re-explore the whole grid.

**Step-by-Step Procedure:**
1. Build `dp` with the same shape as `grid`.
2. Set `dp[0][0] = grid[0][0]`.
3. Fill the first row (accumulate left-to-right) and first column (top-to-bottom).
4. For `i` from 1 to `m-1`, for `j` from 1 to `n-1`: `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`.
5. Return `dp[m-1][n-1]`.
6. Optional: keep only one row and overwrite it in place to save memory.

**Worked Example (Dry Run):**
Input: `grid = [[1,3,1],[1,5,1],[4,2,1]]`.

```
DP Table:
      j=0  j=1  j=2
i=0    1    4    5
i=1    2    7    6
i=2    6    8    7   ← answer = 7
```

Cell-by-cell:
- `dp[0][0] = grid[0][0] = 1`.
- Row 0: `dp[0][1] = 1 + 3 = 4`; `dp[0][2] = 4 + 1 = 5` (only one route along the top).
- Col 0: `dp[1][0] = 1 + 1 = 2`; `dp[2][0] = 2 + 4 = 6` (only one route down the left edge).
- `dp[1][1] = grid[1][1] + min(dp[0][1], dp[1][0]) = 5 + min(4, 2) = 7` — prefers coming from the left (cost 2) over above (cost 4).
- `dp[1][2] = 1 + min(dp[0][2]=5, dp[1][1]=7) = 6` — comes from above.
- `dp[2][1] = 2 + min(dp[1][1]=7, dp[2][0]=6) = 8` — comes from the left.
- `dp[2][2] = 1 + min(dp[1][2]=6, dp[2][1]=8) = 7` — the best path is right,right,down,down: 1 + 3 + 1 + 1 + 1 = 7.

**Final answer: 7.**

**Code:**
```python
def min_path_sum_memo(grid: list, i: int = None, j: int = None, memo=None) -> int:
    # Memoized recursion, solved backwards from the finish cell.
    if memo is None:
        memo = {}
    if i is None:
        # Entry point: solve for the bottom-right corner.
        return min_path_sum_memo(grid, len(grid) - 1, len(grid[0]) - 1, memo)
    if i == 0 and j == 0:
        return grid[0][0]                    # base: the start cell
    if i < 0 or j < 0:
        return float('inf')                  # outside the grid → not a valid parent
    key = (i, j)
    if key in memo:
        return memo[key]                     # already solved → reuse
    # Cheapest way into (i,j) = own value + cheaper parent (above or left).
    memo[key] = grid[i][j] + min(min_path_sum_memo(grid, i - 1, j, memo),
                                 min_path_sum_memo(grid, i, j - 1, memo))
    return memo[key]


def min_path_sum_tab(grid: list) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]                    # base case
    # First row: can only be reached from the left.
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] + grid[0][j]
    # First column: can only be reached from above.
    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    # Everything else: pick the cheaper parent.
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])
    return dp[m - 1][n - 1]


def min_path_sum_optimized(grid: list) -> int:
    m, n = len(grid), len(grid[0])
    # dp[j] holds the previous row's minimum path sum for column j.
    dp = [float('inf')] * n
    dp[0] = 0                                # sentinel so the first cell computes cleanly
    for i in range(m):
        new_dp = [float('inf')] * n
        for j in range(n):
            if i == 0 and j == 0:
                new_dp[j] = grid[0][0]       # base case
            else:
                from_top = dp[j] if i > 0 else float('inf')        # previous row, same col
                from_left = new_dp[j - 1] if j > 0 else float('inf')  # this row, left col
                new_dp[j] = grid[i][j] + min(from_top, from_left)
        dp = new_dp                          # move to the next row
    return dp[n - 1]
```

**Complexity:**
- Time: O(m×n) for all three variants
- Space: O(m×n) (memo / tab), O(n) (optimized)

**Common Mistakes & Edge Cases:**
- Using `max` instead of `min` (turns it into the "maximum path sum" variant).
- Not seeding row 0 / column 0 correctly — every later cell then misreads infinity/zero as a parent.
- Returning `float('inf')` for an empty grid; guard with `if not grid: return 0`.
- A `1×1` grid must return `grid[0][0]`.
- In the optimized version, reading `dp[j]` for row 0 (where "above" does not exist) must be guarded.

---

## Dungeon Game

**Problem Explanation:**
A knight starts at the top-left room of an `m×n` dungeon and must rescue the princess in the bottom-right room, moving only right or down. Every room has a value: positive = health gained, negative = health lost, 0 = nothing. The knight's health must never drop to 0 or below at any point. Find the minimum initial health needed so the knight can always survive. Input is the `m×n` grid of room values; output is that minimum integer initial health (at least 1). "Initial health" means the health you carry into `(0,0)` **before** applying that room's effect.

**State Definition:**
`dp[i][j]` = minimum health the knight must have **upon entering** room `(i, j)` to be able to reach `(m-1, n-1)` alive.

**Recurrence Relation:**
`dp[i][j] = max(1, min(dp[i + 1][j], dp[i][j + 1]) - grid[i][j])`

From `(i, j)` the knight needs enough health to survive this room AND the cheaper of the two exit routes. If the room heals (positive value), less starting health is required; if it drains (negative), more is needed — and since health must stay at least 1, we clamp with `max(1, ...)`.

**Base Cases:**
- `dp[m][n-1] = dp[m-1][n] = 1` — the "dummy" cells just below / beside the princess's room require 1 health so the last room computes correctly (the knight needs at least 1 health to "leave" alive).
- Fill order is **backwards**: from `(m-1, n-1)` up to `(0, 0)`.

**Intuition (Why This Works):**
Greedy forward thinking fails because health is a *running total* — you cannot know the minimum start without knowing the future. Working **backwards** fixes this: `dp[i][j]` states "assuming I am already here, what is the least health I need to finish?". That subproblem is self-contained (it only depends on the two rooms ahead), so DP applies. The choice at each room is "exit via the right or via the bottom — whichever demands less starting health". Clamping with 1 encodes the rule that health is never allowed to be 0.

**Step-by-Step Procedure:**
1. Build an `(m+1) × (n+1)` table `dp` filled with `inf`.
2. Set `dp[m][n-1] = dp[m-1][n] = 1` (virtual boundary rooms).
3. Loop `i` from `m-1` down to 0, `j` from `n-1` down to 0.
4. Compute `need = min(dp[i+1][j], dp[i][j+1]) - grid[i][j]`.
5. Store `dp[i][j] = max(1, need)`.
6. Return `dp[0][0]`.

**Worked Example (Dry Run):**
Input: `grid = [[-2,-3,3],[-5,-10,1],[10,30,-5]]`.

```
dp (min health needed upon entering each room):
      j=0  j=1  j=2
i=0    7    5    2
i=1    6   11    5
i=2    1    1    6
```

Room-by-room (bottom-right first):
- Boundary sentinels: `dp[3][2] = dp[2][3] = 1`.
- `dp[2][2]`: enter room `-5`, must leave with at least 1 → `max(1, 1 - (-5)) = 6`. Need 6 HP to lose 5 and still be at 1.
- `dp[2][1]`: room `30` (big heal) → `max(1, min(inf, 6) - 30) = max(1, -24) = 1` (a healing room means you just need 1 HP).
- `dp[2][0]`: room `10` → `max(1, min(inf, 1) - 10) = 1`.
- `dp[1][2]`: room `1` → `max(1, min(6, inf) - 1) = 5`.
- `dp[1][1]`: room `-10` → `max(1, min(1, 5) - (-10)) = 11` — the `-10` trap demands big reserves.
- `dp[1][0]`: room `-5` → `max(1, min(1, 11) - (-5)) = 6`.
- `dp[0][2]`: room `3` → `max(1, min(5, inf) - 3) = 2`.
- `dp[0][1]`: room `-3` → `max(1, min(11, 2) - (-3)) = 5`.
- `dp[0][0]`: room `-2` → `max(1, min(6, 5) - (-2)) = 7`.

Sanity check: 7 HP −2 → 5; −3 → 2; +3 → 5; +1 → 6; −5 → 1 (alive). The route avoids the `-10` trap.

**Final answer: 7.**

**Code:**
```python
def calculate_minimum_hp(grid: list) -> int:
    m, n = len(grid), len(grid[0])
    # dp[i][j] = min health needed ON ENTRY so the knight can still win.
    # Use an (m+1)x(n+1) table so the boundary "dummy" row/column hold sentinels.
    dp = [[float('inf')] * (n + 1) for _ in range(m + 1)]
    dp[m][n - 1] = dp[m - 1][n] = 1   # below/beside the princess: need 1 HP

    # Backward fill: future rooms (subproblems) must be solved first.
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            # The cheaper exit route (right or down) decides what we must survive to.
            # Subtract this room's value: positive heals (need less), negative drains.
            need = min(dp[i + 1][j], dp[i][j + 1]) - grid[i][j]
            dp[i][j] = max(1, need)   # health must never drop to 0 → clamp at 1
    return dp[0][0]
```

**Complexity:**
- Time: O(m×n)
- Space: O(m×n)

**Common Mistakes & Edge Cases:**
- Filling forward instead of backward — forward answers depend on the unknown future.
- Forgetting the `max(1, ...)` clamp — the knight must survive *entering* the room, so health can never start at 0.
- Confusing the sign: a **negative** room *increases* required HP (subtracting a negative adds), a **positive** room decreases it.
- The virtual boundary cells must be `1`, not `0`, otherwise the princess's own room under-requires health.
- Always clamp after subtracting, never before — a healing room can make `need` hugely negative.

---

## Triangle Minimum Path Sum

**Problem Explanation:**
A "triangle" is a 2D list where row `i` has `i+1` numbers. Start at the apex (row 0). From `triangle[i][j]` you may move down to either `triangle[i+1][j]` or `triangle[i+1][j+1]` (adjacent numbers in the next row). Find the minimum path sum from the apex to some cell in the bottom row. Input is the triangle list; output is the minimum sum. The answer can be computed bottom-up by collapsing the last row upward.

**State Definition:**
`dp[j]` (during the upward sweep) = minimum path sum from the current row's position `j` down to the bottom, i.e. the best "remaining" cost if you stand at `triangle[i][j]`.

**Recurrence Relation:**
`dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])`

From `(i, j)` you pay the current cell and then continue via the cheaper of the two children below — `dp[j]` and `dp[j+1]` already hold the best bottom-up costs for the previous (lower) row.

**Base Cases:**
- `dp = triangle[-1]` (copy of the last row): the cost of standing on a bottom cell is just that cell's value, with no further moves.
- Then rows `n-2` down to `0` overwrite `dp[j]` for `j` in `0..len(triangle[i])-1`.

**Intuition (Why This Works):**
The structure is a tiny DAG where every node has exactly two children; the best path out of a node depends only on the best paths out of its children. Processing from the bottom row upward, each row collapses the problem into a shorter list — the apex's collapsed value is the global answer. The choice at each cell is "left child or right child?", and because the collapse is done in place, space stays O(n).

**Step-by-Step Procedure:**
1. Copy the last row into `dp` (the bottom has no moves left).
2. For `i` from `n-2` down to `0` (second-to-last row down to the apex):
3. For `j` from 0 to `len(triangle[i]) - 1`:
4. `dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])`.
5. After the apex is processed, `dp[0]` is the answer.

**Worked Example (Dry Run):**
Input: `triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]`.

```
Triangle:
      2
     3 4
    6 5 7
   4 1 8 3
```

Collapsing upward:
- Start: `dp = [4, 1, 8, 3]` (bottom row).
- Row 2 (`[6,5,7]`): `dp[0] = 6 + min(4,1) = 7`; `dp[1] = 5 + min(1,8) = 6`; `dp[2] = 7 + min(8,3) = 10` → `dp = [7, 6, 10]`.
- Row 1 (`[3,4]`): `dp[0] = 3 + min(7,6) = 9`; `dp[1] = 4 + min(6,10) = 10` → `dp = [9, 10]`.
- Row 0 (`[2]`): `dp[0] = 2 + min(9,10) = 11` → `dp = [11]`.

Best path: `2 → 3 → 5 → 1 = 11`.

**Final answer: 11.**

**Code:**
```python
def minimum_total_memo(triangle: list, i: int = 0, j: int = 0, memo=None) -> int:
    # Memoized top-down: best sum from (i, j) down to the bottom row.
    if memo is None:
        memo = {}
    if i == len(triangle) - 1:
        return triangle[i][j]            # base: bottom row, no further moves
    key = (i, j)
    if key in memo:
        return memo[key]                 # reuse an already-computed subproblem
    # Pay the current cell, then take the cheaper of the two children below.
    memo[key] = triangle[i][j] + min(minimum_total_memo(triangle, i + 1, j, memo),
                                     minimum_total_memo(triangle, i + 1, j + 1, memo))
    return memo[key]


def minimum_total_tab(triangle: list) -> int:
    n = len(triangle)
    # dp starts as the bottom row: the cost of standing on the last row is itself.
    dp = triangle[-1][:]
    # Work upward: each row collapses two adjacent children into one parent.
    for i in range(n - 2, -1, -1):
        for j in range(len(triangle[i])):
            # dp[j] and dp[j+1] hold the best sums from the row BELOW.
            dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])
    return dp[0]                         # the apex is the single remaining value
```

**Complexity:**
- Time: O(n²) where n = number of rows
- Space: O(n²) memo (one entry per cell), O(n) tab

**Common Mistakes & Edge Cases:**
- Mutating `triangle[-1]` in place — always copy it (`triangle[-1][:]`) so the input is not destroyed.
- Iterating `j` past `len(triangle[i])` — smaller rows would index out of bounds.
- A single-row triangle returns that cell's value directly.
- Off-by-one in the downward move: children are `j` and `j+1`, not `j-1`.
- Negative numbers in the triangle are fine — `min` handles them; do not clamp at 0.

---

## Longest Common Subsequence (LCS)

**Problem Explanation:**
Given two strings `a` and `b`, find the length of the longest subsequence common to both. A **subsequence** keeps characters in order but may skip any number of characters in between (e.g. `"ace"` is a subsequence of `"abcde"`, but `"aec"` is not). Input: two strings; output: the integer length. Note: the characters need NOT be contiguous, which is exactly why this differs from Longest Common Substring.

**State Definition:**
`dp[i][j]` = length of the longest common subsequence of `a[0:i]` (the first `i` characters of `a`) and `b[0:j]` (the first `j` characters of `b`).

**Recurrence Relation:**
```
if a[i-1] == b[j-1]:  dp[i][j] = dp[i-1][j-1] + 1   (diagonal + 1)
else:                 dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```
If the last characters match, they can both be appended to the LCS of the two shorter prefixes — adding 1. If they differ, at least one of them is not in the LCS, so we keep whichever prefix pair gives the longer result.

**Base Cases:**
- `dp[0][j] = 0` for all `j` — an empty `a` shares nothing with `b`.
- `dp[i][0] = 0` for all `i` — `a` shares nothing with an empty `b`.

**Intuition (Why This Works):**
The answer for two full strings is decided by their tails: either the tails match (extend a smaller LCS) or they don't (drop one of the tails and keep the best). Every subproblem is about shorter prefixes, so there is a natural chain of smaller instances — DP's optimal substructure. The choice per cell is "match or skip", and storing each `(i,j)` result avoids recomputing overlapping prefix pairs exponentially many times.

**Step-by-Step Procedure:**
1. Build an `(m+1) × (n+1)` table of zeros (the `+1` keeps room for empty prefixes).
2. For `i` from 1 to `m`, for `j` from 1 to `n`:
3. If `a[i-1] == b[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`.
4. Else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.
5. Return `dp[m][n]`.
6. (Optional space optimization) keep only the previous row and update in place.

**Worked Example (Dry Run):**
Input: `a = "abcde"`, `b = "ace"`.

```
     ""  a  c  e       ← string b (columns)
  ┌────┬────┬────┬────┐
""│  0 │  0 │  0 │  0 │  ← empty prefix: 0 matches
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

Rules:
  a[i] == b[j] → dp[i][j] = dp[i-1][j-1] + 1  (diagonal + 1)
  a[i] ≠ b[j]  → dp[i][j] = max(dp[i-1][j], dp[i][j-1])  (max of above or left)
```

Cell-by-cell (several notable ones):
- Row 0 / col 0: all 0 (empty prefixes).
- `dp[1][1]`: `a == a` → `dp[0][0] + 1 = 1` — LCS of `"a"` and `"a"`.
- `dp[1][3]`: `a ≠ e` → `max(dp[0][3], dp[1][2]) = max(0, 1) = 1` — still just `"a"`.
- `dp[3][2]`: `c == c` → `dp[2][1] + 1 = 1 + 1 = 2` — LCS of `"abc"`,`"ac"` is `"ac"`.
- `dp[4][3]`: `d ≠ e` → `max(dp[3][3], dp[4][2]) = max(2, 2) = 2`.
- `dp[5][3]`: `e == e` → `dp[4][2] + 1 = 2 + 1 = 3` — the full LCS `"ace"`.

**Final answer: 3 (the subsequence `"ace"`).**

**Code:**
```python
def lcs_tab(a: str, b: str) -> int:
    m, n = len(a), len(b)
    # dp[i][j] = LCS length of a[0:i] and b[0:j]. Rows/cols 0 are for empty prefixes.
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                # Tail chars match: they join the LCS of the two shorter prefixes.
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # Tails differ: at least one is excluded → keep the better prefix pair.
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


# Space-optimized: each cell only needs the previous row, so keep just two rows.
def lcs_tab_optimized(a: str, b: str) -> int:
    m, n = len(a), len(b)
    prev, curr = [0] * (n + 1), [0] * (n + 1)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1] + 1          # prev[j-1] is the diagonal
            else:
                curr[j] = max(prev[j], curr[j - 1])  # above (prev row) vs left (this row)
        prev, curr = curr, [0] * (n + 1)           # slide the window down a row
    return prev[n]
```

**Complexity:**
- Time: O(m×n)
- Space: O(m×n) full table, O(min(m,n)) with the two-row optimization

**Common Mistakes & Edge Cases:**
- Using `max` but forgetting the `+1` on a match (or adding it on a mismatch).
- Off-by-one: compare `a[i-1]` / `b[j-1]` because the table is padded with the empty-prefix row/column.
- Confusing subsequence (skips allowed) with substring (contiguous) — the recurrences differ.
- Empty input strings must return 0 (the zero-padded table handles this for free).
- For reconstruction, if `dp[i-1][j]` and `dp[i][j-1]` are equal, moving left (or up) is still correct — the result may just be a different valid LCS.

### LCS: Reconstruct the Subsequence

**🔗 Practice Link:** [LCS: Reconstruct the Subsequence](https://leetcode.com/problems/longest-common-subsequence/)

**Problem Explanation:**
Beyond just the length, produce one actual longest common subsequence string. After filling the LCS table, we **trace back** from the bottom-right corner: matched characters are collected, and mismatches make us move toward the larger adjacent value. Input: two strings; output: a string that is a longest common subsequence (any one if several exist).

**State Definition:**
The same `dp[i][j]` table as LCS — used as a "map" to walk back through the decisions.

**Recurrence Relation:**
Trace-back rules:
```
if a[i-1] == b[j-1]:   append a[i-1];  i--, j--          (this char is in the LCS)
elif dp[i-1][j] > dp[i][j-1]:  i--                       (better answer came from above)
else:                 j--                                (better answer came from left)
```
Each matched character was created by a diagonal `+1` in the forward fill, so collecting those characters during the walk yields exactly the LCS.

**Base Cases:**
- Stop when `i == 0` or `j == 0` (an empty prefix is reached — no more characters to collect).

**Intuition (Why This Works):**
The forward fill records *how* every value was produced. A `+1` came from a diagonal (a real match); every `max` came from above or left. Walking the table backwards following the arrows "un-plays" the construction, and the characters collected at diagonals spell out the subsequence in reverse (hence the final `reversed()`).

**Step-by-Step Procedure:**
1. Fill the full LCS table (all rows are needed for the walk).
2. Start at `i = m, j = n`.
3. While both `i > 0` and `j > 0`:
4. If `a[i-1] == b[j-1]`, push that char, then `i -= 1; j -= 1`.
5. Else if `dp[i-1][j] > dp[i][j-1]`, `i -= 1`; else `j -= 1`.
6. After the loop, reverse the collected chars and join.

**Worked Example (Dry Run):**
Input: `a = "abcde"`, `b = "ace"` (table filled in LCS above).
- Start `(5,3)`: `a[4]='e' == b[2]='e'` → collect `'e'`, go `(4,2)`.
- `(4,2)`: `'d' ≠ 'c'`; `dp[3][2] = 2 > dp[4][1] = 1` → move up to `(3,2)` (skip `'d'`).
- `(3,2)`: `a[2]='c' == b[1]='c'` → collect `'c'`, go `(2,1)`.
- `(2,1)`: `'b' ≠ 'a'`; `dp[1][1] = 1 > dp[2][0] = 0` → move up to `(1,1)` (skip `'b'`).
- `(1,1)`: `a[0]='a' == b[0]='a'` → collect `'a'`, go `(0,0)`.
- Loop ends (`i == 0`). Collected `['e','c','a']` → reversed → `"ace"`.

**Final answer: `"ace"`.**

**Code:**
```python
def lcs_reconstruct(a: str, b: str) -> str:
    m, n = len(a), len(b)
    # First fill the full LCS table (every row is needed for backtracking).
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # Trace back from the bottom-right corner.
    i, j = m, n
    chars = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            # Both tails match → this character is part of the LCS.
            chars.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1           # the larger value came from above → skip a[i-1]
        else:
            j -= 1           # the larger value came from left → skip b[j-1]
    # We collected from the end backwards, so reverse the list.
    return ''.join(reversed(chars))
```

**Complexity:**
- Time: O(m×n)
- Space: O(m×n) (must keep the full table to walk back)

**Common Mistakes & Edge Cases:**
- Forgetting to reverse the collected characters (they are gathered tail-first).
- Walking past `i == 0` / `j == 0` — always guard the loop with both bounds.
- Ties (`dp[i-1][j] == dp[i][j-1]`) must go to the `else` branch; using `>=` on the "above" check instead of `>` on "left" only changes which valid LCS you get.
- Two identical strings reconstruct the whole string; two disjoint strings reconstruct `""`.

---

## Edit Distance (Levenshtein)

**Problem Explanation:**
Given two strings `a` (source) and `b` (target), find the minimum number of single-character operations needed to convert `a` into `b`. The allowed operations are **insert** a character, **delete** a character, and **replace** a character (each costs 1). Input: two strings; output: the minimum operation count. This is the classic Levenshtein distance. Example: `"horse" → "ros"` needs 3 operations.

**State Definition:**
`dp[i][j]` = minimum operations to convert the prefix `a[0:i]` into the prefix `b[0:j]`.

**Recurrence Relation:**
```
if a[i-1] == b[j-1]:  dp[i][j] = dp[i-1][j-1]                       (no cost)
else:                 dp[i][j] = 1 + min( dp[i-1][j],    (delete a[i-1])
                                          dp[i][j-1],    (insert b[j-1] into a)
                                          dp[i-1][j-1] ) (replace a[i-1] with b[j-1])
```
If the tails are equal, no operation is needed — copy the diagonal. Otherwise the last step was one of the three operations, so we pay 1 plus the best way to reach the state before that operation.

**Base Cases:**
- `dp[0][j] = j` — building `b[0:j]` from the empty string needs `j` inserts.
- `dp[i][0] = i` — emptying `a[0:i]` down to `""` needs `i` deletes.

**Intuition (Why This Works):**
Converting two strings is a sequence of local decisions on their tails, and the minimum is built from minimums of smaller prefixes — perfect optimal substructure. The choice at each cell is among the three operations, each expressed as "one operation + the cost of converting the remaining prefixes". Because DP stores each prefix-pair answer, the exponential space of operation sequences collapses into a single O(m×n) table.

**Step-by-Step Procedure:**
1. Build an `(m+1) × (n+1)` table.
2. Fill row 0 with `0..n` and column 0 with `0..m` (the empty-prefix base cases).
3. For `i` from 1 to `m`, for `j` from 1 to `n`:
4. If `a[i-1] == b[j-1]`: copy `dp[i-1][j-1]`.
5. Else: `1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`.
6. Return `dp[m][n]`.

**Worked Example (Dry Run):**
Input: `a = "horse"`, `b = "ros"`.

```
     ""  r  o  s        ← string b
  ┌────┬────┬────┬────┐
""│  0 │  1 │  2 │  3 │   Need j inserts to build b[0:j]
  ├────┼────┼────┼────┤
 h│  1 │  1 │  2 │  3 │   h≠r → 1 + min(1,1,0) = 1 (replace h→r)
  ├────┼────┼────┼────┤
 o│  2 │  2 │  1 │  2 │   o=o ✓ → diagonal dp[1][1] = 1 (no op)
  ├────┼────┼────┼────┤
 r│  3 │  2 │  2 │  2 │   r=r ✓ → diagonal dp[2][1] = 2
  ├────┼────┼────┼────┤
 s│  4 │  3 │  3 │  2 │   s=s ✓ → diagonal dp[3][2] = 2
  ├────┼────┼────┼────┤
 e│  5 │  4 │  4 │  3 │   e≠s → 1 + min(2,4,3) = 3  ← answer = 3
  └────┴────┴────┴────┘

Three operations at each cell:
  DELETE:  dp[i-1][j] + 1      ← remove char from a
  INSERT:  dp[i][j-1] + 1      ← add char to a
  REPLACE: dp[i-1][j-1] + 1    ← change char (cost 0 if same → just copy diagonal)
```

Cell-by-cell:
- Base row/col: `dp[0][*] = 0,1,2,3` and `dp[*][0] = 0,1,2,3,4,5`.
- `dp[1][1]`: `h ≠ r` → `1 + min(dp[0][1]=1, dp[1][0]=1, dp[0][0]=0) = 1` (replace `h`→`r`).
- `dp[1][2]`: `h ≠ o` → `1 + min(2, 1, 1) = 2`.
- `dp[2][2]`: `o == o` → copy `dp[1][1] = 1`.
- `dp[2][3]`: `o ≠ s` → `1 + min(3, 1, 2) = 2`.
- `dp[3][3]`: `r ≠ s` → `1 + min(2, 2, 1) = 2`.
- `dp[5][3]`: `e ≠ s` → `1 + min(dp[4][3]=2, dp[5][2]=4, dp[4][2]=3) = 3`.

The 3 operations: `horse → rorse (replace h→r) → rose (delete 2nd r) → ros (delete e)`.

**Final answer: 3.**

**Code:**
```python
def edit_distance_tab(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    # Base: converting the empty string to b[0:j] takes j inserts.
    for j in range(n + 1):
        dp[0][j] = j
    # Base: converting a[0:i] to the empty string takes i deletes.
    for i in range(m + 1):
        dp[i][0] = i
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                # Characters already match: no operation, keep the diagonal cost.
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Pay 1 for the final operation, then take the cheapest predecessor:
                # delete the tail of a, insert the tail of b, or replace them.
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # delete a[i-1]
                    dp[i][j - 1],      # insert b[j-1] into a
                    dp[i - 1][j - 1]   # replace a[i-1] with b[j-1]
                )
    return dp[m][n]


# Space-optimized: the recurrence only looks at the previous row and the current row.
def edit_distance_optimized(a: str, b: str) -> int:
    m, n = len(a), len(b)
    prev = list(range(n + 1))   # base row: dp[0][j] = j
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        curr[0] = i             # base col: dp[i][0] = i
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1]                # match: diagonal, no cost
            else:
                # prev[j] = delete, curr[j-1] = insert, prev[j-1] = replace.
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev, curr = curr, [0] * (n + 1)             # move to the next row
    return prev[n]
```

**Complexity:**
- Time: O(m×n)
- Space: O(m×n) tab, O(min(m,n)) optimized

**Common Mistakes & Edge Cases:**
- Copying the diagonal on a **mismatch** (or paying 1 on a match) — reverses the whole cost model.
- Omitting one of the three operations in the `min`.
- One empty string: the answer is simply the other string's length (handled by the base row/col).
- Identical strings return 0.
- The optimized version must re-seed `curr[0] = i` every row, or the first column goes stale.

---

## Longest Common Substring

**Problem Explanation:**
Given two strings `a` and `b`, find the length of the longest substring (characters **contiguous**) present in both. Input: two strings; output: the integer length. This differs from LCS in one crucial rule: a break in the match **resets** the count to 0 instead of carrying the max forward.

**State Definition:**
`dp[i][j]` = length of the longest common substring that **ends exactly at** `a[i-1]` and `b[j-1]` (it must include both of those characters).

**Recurrence Relation:**
```
if a[i-1] == b[j-1]:  dp[i][j] = dp[i-1][j-1] + 1
else:                 dp[i][j] = 0      ← reset, NOT max(above, left)
```
Matching extends the common run by 1; the first mismatch in the run cuts it down to 0, which is what enforces contiguity.

**Base Cases:**
- `dp[0][j] = 0`, `dp[i][0] = 0` — empty prefixes share no characters.
- The answer is tracked separately as `max_len = max(max_len, dp[i][j])` over the whole table.

**Intuition (Why This Works):**
If a common substring had a gap, it would not be contiguous — so any mismatch must "break" the chain, which is why we reset instead of keeping a max. DP applies because a contiguous run ending at `(i,j)` is just the run ending at `(i-1,j-1)` extended by one matching character. The choice per cell is binary: "continue the current run (diagonal)" or "break it (0)"; the global answer is simply the longest run anywhere in the table.

**Step-by-Step Procedure:**
1. Build an `(m+1) × (n+1)` table of zeros; keep a `max_len` variable at 0.
2. For `i` from 1 to `m`, for `j` from 1 to `n`:
3. If `a[i-1] == b[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`; update `max_len`.
4. Else: `dp[i][j] = 0` (do NOT update `max_len`).
5. Return `max_len`.

**Worked Example (Dry Run):**
Input: `a = "abcde"`, `b = "abfde"`.

```
     ""  a  b  f  d  e
""    0  0  0  0  0  0
 a    0  1  0  0  0  0
 b    0  0  2  0  0  0
 c    0  0  0  0  0  0
 d    0  0  0  0  1  0
 e    0  0  0  0  0  2   → answer = 2
```

Cell-by-cell:
- `dp[1][1]`: `a==a` → `dp[0][0]+1 = 1` (run "a").
- `dp[2][2]`: `b==b` → `dp[1][1]+1 = 2` (run "ab").
- `dp[2][3]`: `b≠f` → `0` — the run breaks; if this were LCS it would stay 2.
- `dp[3][3]`: `c≠f` → `0`.
- `dp[4][4]`: `d==d` → `dp[3][3]+1 = 1` (run "d").
- `dp[5][5]`: `e==e` → `dp[4][4]+1 = 2` (run "de").

`max_len` reaches 2 twice ("ab" and "de").

**Final answer: 2.**

**Code:**
```python
def longest_common_substring_memo(a: str, b: str, i: int = None, j: int = None,
                                  memo=None) -> int:
    # memo[(i,j)] = length of the common substring ENDING at a[i] and b[j]
    # (0 if the two characters differ). The top-level call computes every
    # "ends here" value and returns the largest one.
    if memo is None:
        memo = {}
    if i is None:
        # Entry point: evaluate every aligned pair and take the maximum.
        best = 0
        for p in range(len(a)):
            for q in range(len(b)):
                best = max(best, longest_common_substring_memo(a, b, p, q, memo))
        return best
    if i < 0 or j < 0:
        return 0                       # ran off the start of a string → run length 0
    key = (i, j)
    if key in memo:
        return memo[key]               # reuse a previously computed run length
    if a[i] == b[j]:
        # Extend the run that ended one position earlier in both strings.
        memo[key] = 1 + longest_common_substring_memo(a, b, i - 1, j - 1, memo)
    else:
        memo[key] = 0                  # mismatch breaks contiguity → reset
    return memo[key]


def longest_common_substring_tab(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0                        # track the longest run seen anywhere
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                # Continue the diagonal run; then check if it's the longest yet.
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_len = max(max_len, dp[i][j])
            # else dp[i][j] stays 0 → the contiguous run is broken.
    return max_len
```

**Complexity:**
- Time: O(m×n)
- Space: O(m×n) (both variants); can be reduced to O(min(m,n)) with rolling rows

**Common Mistakes & Edge Cases:**
- Using the LCS `max(dp[i-1][j], dp[i][j-1])` on a mismatch — that silently produces a (non-contiguous) subsequence answer instead.
- Forgetting to track `max_len` separately — the value at `dp[m][n]` is NOT the answer (it is only the run ending at the last character).
- Empty string input returns 0.
- All characters matching: the bottom-right cell equals the whole string length, and `max_len` must catch it.
- Repeated patterns (e.g. `"aaaa"` vs `"aaaa"`) still work because each diagonal keeps extending.

---

## Distinct Subsequences

**Problem Explanation:**
Given strings `s` (source) and `t` (target), count how many distinct ways you can delete characters from `s` so that what remains equals `t`. Equivalently: count the number of subsequences of `s` that are exactly equal to `t`. Input: two strings; output: a non-negative integer. Example: `s = "rabbbit"`, `t = "rabbit"` → 3 (delete any one of the three `b`s). Counts can be large but fit in a normal integer.

**State Definition:**
`dp[i][j]` = number of distinct ways to obtain `t[0:j]` as a subsequence of `s[0:i]`.

**Recurrence Relation:**
```
dp[i][j] = dp[i-1][j]                      (always: skip s[i-1])
if s[i-1] == t[j-1]:  dp[i][j] += dp[i-1][j-1]   (also: use s[i-1] to match t[j-1])
```
The current character of `s` is either skipped or — if it matches the current character of `t` — used to complete one more match; both options are valid, so their counts add.

**Base Cases:**
- `dp[i][0] = 1` for all `i` — one way to obtain the empty target: delete everything.
- `dp[0][j] = 0` for `j > 0` — an empty source cannot produce a non-empty target.

**Intuition (Why This Works):**
This is the "count" version of a two-string DP. At every position in `s` there are exactly two choices: ignore this character or (if it matches) consume it against the current target character. Since the choices are independent and every valid construction is a unique sequence of those choices, the counts simply add — a natural fit for DP because the count for prefixes depends only on counts of smaller prefixes. Storing each `dp[i][j]` lets us sum without enumerating subsequences.

**Step-by-Step Procedure:**
1. Build an `(m+1) × (n+1)` table; set every `dp[i][0] = 1`.
2. For `i` from 1 to `m`, for `j` from 1 to `n`:
3. Start with `dp[i][j] = dp[i-1][j]` (skip `s[i-1]`).
4. If `s[i-1] == t[j-1]`, add `dp[i-1][j-1]` (consume both).
5. Return `dp[m][n]`.

**Worked Example (Dry Run):**
Input: `s = "rabbbit"`, `t = "rabbit"`.

```
     ""  r  a  b  b  i  t
""    1  0  0  0  0  0  0
 r    1  1  0  0  0  0  0
 a    1  1  1  0  0  0  0
 b    1  1  1  1  1  0  0
 b    1  1  1  2  1  0  0
 b    1  1  1  3  3  0  0
 i    1  1  1  3  3  3  0
 t    1  1  1  3  3  3  3   → answer = 3
```

Cell-by-cell:
- Col 0: all 1s (empty target). Row 0: 0s (empty source).
- `dp[3][3]`: `s[2]='b' == t[2]='b'` → skip `= dp[2][3] = 0`; match `= dp[2][2] = 1`; total `1`.
- `dp[4][3]`: `b == b` → skip `= dp[3][3] = 1`; match `= dp[3][2] = 1`; total `2` — the two `b`s at positions 2 and 3.
- `dp[5][3]`: `b == b` → skip `= dp[4][3] = 2`; match `= dp[4][2] = 1`; total `3` — now three choices of which `b` to drop.
- `dp[5][4]`: `b == b` → skip `= dp[4][4] = 1`; match `= dp[4][3] = 2`; total `3`.
- `dp[6][5]`: `i == i` → skip `= dp[5][5] = 0`; match `= dp[5][4] = 3`; total `3`.
- `dp[7][6]`: `t == t` → skip `= dp[6][6] = 0`; match `= dp[6][5] = 3`; total `3`.

**Final answer: 3.**

**Code:**
```python
def num_distinct_memo(s: str, t: str, i: int = None, j: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if i is None:
        # Entry point: solve for the full strings.
        return num_distinct_memo(s, t, len(s), len(t), memo)
    if j == 0:
        return 1                     # empty target: exactly one way (delete all of s)
    if i == 0:
        return 0                     # empty source can't match a non-empty target
    key = (i, j)
    if key in memo:
        return memo[key]             # reuse a previously computed count
    # Choice 1: skip s[i-1] entirely → solve the smaller prefix.
    ans = num_distinct_memo(s, t, i - 1, j, memo)
    # Choice 2: if the tail characters match, also consume both.
    if s[i - 1] == t[j - 1]:
        ans += num_distinct_memo(s, t, i - 1, j - 1, memo)
    memo[key] = ans
    return memo[key]


def num_distinct_tab(s: str, t: str) -> int:
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    # Base: one way to form the empty target from any prefix of s.
    for i in range(m + 1):
        dp[i][0] = 1
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j]        # skip s[i-1]
            if s[i - 1] == t[j - 1]:
                dp[i][j] += dp[i - 1][j - 1]   # also match s[i-1] with t[j-1]
    return dp[m][n]
```

**Complexity:**
- Time: O(m×n)
- Space: O(m×n)

**Common Mistakes & Edge Cases:**
- Forgetting the "skip" option on a match — the target can always be formed without using the matching character.
- Empty target `t`: the answer is 1, not 0.
- Target longer than source: the answer is 0.
- Using only `dp[i-1][j-1]` (match) and dropping the skip case undercounts every problem with repeated characters (like the `b`s here).
- Very large counts can overflow 32-bit integers — use Python ints (arbitrary precision) or a big-integer language type.

---

## Interleaving String

**Problem Explanation:**
Given three strings `s1`, `s2`, and `s3`, decide whether `s3` can be formed by **interleaving** `s1` and `s2` — that is, by merging the characters of `s1` and `s2` while preserving each string's internal order. Input: three strings; output: a boolean. Example: `s1="aabcc"`, `s2="dbbca"`, `s3="aadbbcbcac"` → True. Key detail: all characters of both `s1` and `s2` must be used, so `len(s3)` must equal `len(s1) + len(s2)`.

**State Definition:**
`dp[i][j]` = True iff the first `i+j` characters of `s3` (i.e. `s3[0:i+j]`) form a valid interleaving of `s1[0:i]` and `s2[0:j]`.

**Recurrence Relation:**
```
dp[i][j] = ( dp[i-1][j] and s1[i-1] == s3[i+j-1] )  OR
           ( dp[i][j-1] and s2[j-1] == s3[i+j-1] )
```
The last character of the interleaved prefix comes either from `s1` (whose own last char must match `s3`'s) or from `s2` — if either route is valid, the cell is True.

**Base Cases:**
- `dp[0][0] = True` — empty strings interleave to empty.
- `dp[i][0]` — only `s1` is being consumed: `dp[i-1][0] and s1[i-1] == s3[i-1]`.
- `dp[0][j]` — only `s2` is being consumed: `dp[0][j-1] and s2[j-1] == s3[j-1]`.
- Quick reject: if `len(s1) + len(s2) != len(s3)`, return False immediately.

**Intuition (Why This Works):**
At every step the "next" character of `s3` must be supplied by whichever string is used next — a binary choice that needs no look-ahead beyond the already-matched prefix, giving DP's optimal substructure. The stored boolean answers "can these two exact prefixes be interleaved into this exact prefix of `s3`?", and each cell derives from the cell above (last char from `s1`) or the cell left (last char from `s2`). Memoization avoids re-exploring the same `(i,j)` state from many different paths.

**Step-by-Step Procedure:**
1. If lengths mismatch, return False.
2. Build an `(m+1) × (n+1)` boolean table; set `dp[0][0] = True`.
3. Fill column 0 (only `s1`) and row 0 (only `s2`) with the chained match conditions.
4. For `i` from 1 to `m`, for `j` from 1 to `n`:
5. Check "from above": `dp[i-1][j] and s1[i-1] == s3[i+j-1]`.
6. Check "from left": `dp[i][j-1] and s2[j-1] == s3[i+j-1]`.
7. `dp[i][j] =` (step 5) OR (step 6).
8. Return `dp[m][n]`.

**Worked Example (Dry Run):**
Input: `s1 = "aabcc"`, `s2 = "dbbca"`, `s3 = "aadbbcbcac"`.

```
s3 =  a  a  d  b  b  c  b  c  a  c
idx =  0  1  2  3  4  5  6  7  8  9

       ""    d     b     b     c     a       ← s2 (columns)
""     T     F     F     F     F     F
 a     T     F     F     F     F     F
 a     T     T     T     T     T     F
 b     T     T     T     F     T     F
 c     T     F     T     T     T     T
 c     T     F     F     T     F     T   ← dp[5][5] = T
 ↑ s1 (rows)
```

Cell-by-cell (notable ones):
- `dp[0][0] = True`; row 0: only `s2` can be consumed, and `s2[0]='d' ≠ s3[0]='a'`, so all F.
- `dp[1][0]`: `s1[0]='a' == s3[0]='a'` → True. `dp[2][0]`: `'a'=='a'` → True. `dp[3][0]`: `'b'≠'a'` → False.
- `dp[2][1]`: from left `dp[2][0]=T and s2[0]='d' == s3[2]='d'` → True ("aa" + "d" = "aad").
- `dp[2][3]`: from left `dp[2][2]=T and s2[2]='b' == s3[4]='b'` → True ("aa" + "dbb" = "aadbb").
- `dp[3][3]`: from above `dp[2][3]=T and s1[2]='b' == s3[5]='c'` → F; from left `dp[3][2]=T and s2[2]='b' == s3[5]='c'` → F; cell is False.
- `dp[5][5]`: from above `dp[4][5]=T and s1[4]='c' == s3[9]='c'` → True.

**Final answer: True.** (An interleaving: `a a d b b c b c a c` = s1 positions 0,1,2,3,4 interleaved with s2 positions 0,1,2,4.)

**Code:**
```python
def is_interleave_memo(s1: str, s2: str, s3: str, i: int = 0, j: int = 0,
                       memo=None) -> bool:
    if memo is None:
        memo = {}
    if i + j == len(s3):
        # Consumed the whole of s3 — success only if both strings are also fully used.
        return i == len(s1) and j == len(s2)
    key = (i, j)
    if key in memo:
        return memo[key]             # reuse previously computed state
    ans = False
    if i < len(s1) and s1[i] == s3[i + j]:
        # Next char can come from s1 → try that branch.
        ans = ans or is_interleave_memo(s1, s2, s3, i + 1, j, memo)
    if not ans and j < len(s2) and s2[j] == s3[i + j]:
        # Otherwise try taking the next char from s2.
        ans = ans or is_interleave_memo(s1, s2, s3, i, j + 1, memo)
    memo[key] = ans
    return memo[key]


def is_interleave_tab(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False                 # lengths must line up or it's impossible
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True                  # empty interleaving of empty strings
    # First column: only s1 is consumed, so each char must match s3 in order.
    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]
    # First row: only s2 is consumed.
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Either the last char came from s1 (above cell, match s1) ...
            dp[i][j] = (dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]) or \
                       (dp[i][j - 1] and s2[j - 1] == s3[i + j - 1])
    return dp[m][n]
```

**Complexity:**
- Time: O(m×n)
- Space: O(m×n)

**Common Mistakes & Edge Cases:**
- Skipping the length check — unequal lengths always answer False.
- Indexing `s3` with `i+j` instead of `i+j-1` (the table is padded with an empty-prefix row/col).
- In the memo version, forgetting that success requires BOTH strings to be exhausted (`i == len(s1) and j == len(s2)`), not just `i+j == len(s3)`.
- Empty `s1` or `s2`: the answer reduces to a plain substring match of `s3` against the non-empty string.
- All three strings empty → True.

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
