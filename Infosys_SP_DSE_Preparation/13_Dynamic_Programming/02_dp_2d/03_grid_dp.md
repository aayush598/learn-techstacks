# Grid DP — Advanced Grid Traversal

Beyond basic path counting and path sum (covered in the fundamentals file), many harder grid problems require simultaneous agents, backward passes, bitmask state, or multi-directional movement. This file covers the most common advanced grid DP patterns.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    GRID DP PATTERN RECOGNITION                           │
├──────────────────────────────┬───────────────────────────────────────────┤
│ Problem hints                │ Approach                                │
├──────────────────────────────┼───────────────────────────────────────────┤
│ "two paths / two agents"    │ Simultaneous-path DP (two row indices)  │
│ "visit every cell exactly"  │ Bitmask DP: dp[mask][i][j]             │
│ "falling / sliding down"    │ Row-by-row DP with 3-direction min     │
│ "cannot repeat column"      │ Track two minimums per row             │
│ "knight moves on grid"      │ Fixed transition table DP              │
│ "ball goes out of bounds"   │ 3D DP: dp[moves][i][j] counting paths │
│ "submatrix sum queries"     │ 2D prefix sum precomputation           │
└──────────────────────────────┴───────────────────────────────────────────┘
```

---

## 1. Cherry Pickup (LC #741) — Hard

### Problem Explanation
An n×n grid holds non-negative integers (cherries). Collect cherries by moving from `(0,0)` to `(n-1,n-1)` (right or down), then return from `(n-1,n-1)` to `(0,0)` (left or up). A cell's cherry is picked up on the first visit only. Maximize the total. The key insight is that two simultaneous paths from start to end are equivalent to one round trip, so we model both paths going forward together.

### State Definition
`dp[r1][r2]` = maximum cherries collected when path 1 is at row `r1` and path 2 is at row `r2` after `k` steps. Columns are implicit: `c1 = k - r1`, `c2 = k - r2`.

### Recurrence Relation
```
cherry = grid[r1][c1] + (grid[r2][c2] if r1 != r2 else 0)
dp_new[r1][r2] = cherry + max(dp_old[pr1][pr2]) over pr1 in {r1-1, r1}, pr2 in {r2-1, r2}
```
Each path came from either the cell above (column increased) or the same row (row increased). The max over 4 predecessor pairs yields the best combined total.

### Base Cases
- Step 0: `dp[0][0] = grid[0][0]` (both paths start at the top-left).
- Invalid positions (where `r > k` or `c >= n`) remain at `-inf` and are skipped.

### Intuition (Why This Works)
At step k, both paths have taken exactly k moves, so each is at a cell whose row+column = k. Only two row indices are needed to describe the joint state, reducing O(n^4) to O(n^3). The max over 4 predecessors captures all direction combinations (both right, both down, or one of each).

### Step-by-Step Procedure
1. Let `n = len(grid)`. If `n == 1`, return `max(grid[0][0], 0)`.
2. Initialize `dp[0][0] = grid[0][0]`, all other cells to `-inf`.
3. For each step `k` from 1 to `2(n-1)`:
4. For each valid `r1` in `[max(0, k-n+1), min(k, n-1)]`:
5. For each valid `r2` in the same range:
6. Compute `c1 = k-r1`, `c2 = k-r2`. Skip if either column is out of bounds.
7. Compute `cherry` (add both cells, but once if they overlap).
8. `dp_new[r1][r2] = cherry + max of valid predecessors`.
9. After all steps, return `max(dp[n-1][n-1], 0)`.

### Worked Example (Dry Run)
Input: `grid = [[1,2],[3,4]]`, n=2.

```
Step 0: dp[0][0] = 1

Step 1 (k=1):
  (r1=0,r2=0): c1=1,c2=1 -> both at (0,1). cherry=2. From (0,0): 1+2=3.
  (r1=0,r2=1): c1=1,c2=0 -> (0,1)&(1,0). cherry=2+3=5. From (0,0): 1+5=6.
  (r1=1,r2=0): symmetric -> 6.
  (r1=1,r2=1): both at (1,0). cherry=3. From (0,0): 1+3=4.

Step 2 (k=2): both at (1,1). cherry=4.
  From (0,0): 3+4=7.  From (0,1): 6+4=10.
  From (1,0): 6+4=10. From (1,1): 4+4=8.
  dp[1][1] = 10.
```

Answer: **10**. Together the paths visit all 4 cells: 1+2+3+4 = 10.

### Code
```python
class Solution:
    def cherryPickup(self, grid: list) -> int:
        n = len(grid)
        if n == 1:
            return max(grid[0][0], 0)
        inf = float('inf')
        dp = [[-inf] * n for _ in range(n)]
        dp[0][0] = grid[0][0]
        for k in range(1, 2 * n - 1):
            new_dp = [[-inf] * n for _ in range(n)]
            for r1 in range(max(0, k - n + 1), min(k, n - 1) + 1):
                c1 = k - r1
                if c1 >= n:
                    continue
                for r2 in range(max(0, k - n + 1), min(k, n - 1) + 1):
                    c2 = k - r2
                    if c2 >= n:
                        continue
                    cherry = grid[r1][c1]
                    if r1 != r2:
                        cherry += grid[r2][c2]
                    best = -inf
                    for pr1 in (r1 - 1, r1):
                        for pr2 in (r2 - 1, r2):
                            if 0 <= pr1 < n and 0 <= pr2 < n:
                                best = max(best, dp[pr1][pr2])
                    if best != -inf:
                        new_dp[r1][r2] = best + cherry
            dp = new_dp
        return max(dp[n - 1][n - 1], 0)
```

### Complexity
- Time: O(n^3) — 2n steps x n^2 row-pairs x 4 predecessors
- Space: O(n^2)

### Common Mistakes & Edge Cases
- Both paths at the same cell: count that cell's cherry only once (`if r1 != r2`).
- n=1: return `max(grid[0][0], 0)` since no round trip is needed.
- Negative cherries in some versions — clamp the final answer at 0.
- Skipping invalid positions where `r > k` or `c >= n` (they stay at `-inf`).
- Using `min` instead of `max` (this is a maximization problem).

---

## 2. Cherry Pickup II (LC #1463) — Hard

### Problem Explanation
An m×n grid of integers. Robot 1 starts at `(0,0)` and Robot 2 starts at `(0,n-1)`. Both collect cherries as they move down one row at a time (left, right, or staying in the same column). Both must reach the last row. Cherries from the same cell are counted once. Maximize the total. At each row, the two robots' columns fully describe the joint state.

### State Definition
`dp[c1][c2]` = maximum cherries collected when robot 1 is at column `c1` and robot 2 is at column `c2` in the current row.

### Recurrence Relation
```
cherry = grid[row][c1] + (grid[row][c2] if c1 != c2 else 0)
dp_new[nc1][nc2] = max(dp[c1][c2] + cherry) over all valid (nc1, nc2)
  where nc1 in {c1-1, c1, c1+1} and nc2 in {c2-1, c2, c2+1}
```
Each robot moves left, stays, or moves right (3 x 3 = 9 combinations per predecessor).

### Base Cases
- Row 0: `dp[0][n-1] = grid[0][0] + grid[0][n-1]` (both robots start positions).
- All other states at row 0 are `-inf` (unreachable).

### Intuition (Why This Works)
Since both robots move row by row, only the column indices matter as state. The row is implicit from the loop iteration. At each row, both robots independently choose one of 3 moves, giving 9 transitions per state pair. The overlapping-cell guard (`c1 != c2`) prevents double-counting.

### Step-by-Step Procedure
1. Initialize `dp[0][n-1] = grid[0][0] + grid[0][n-1]`.
2. For each row `i` from 1 to m-1:
3. Create `new_dp` filled with `-inf`.
4. For each `c1` and `c2` where `dp[c1][c2]` is valid:
5. For each move `d1 in {-1, 0, 1}` and `d2 in {-1, 0, 1}`:
6. Compute `nc1 = c1+d1`, `nc2 = c2+d2`. Skip if out of bounds.
7. `new_dp[nc1][nc2] = max(new_dp[nc1][nc2], dp[c1][c2] + cherry)`.
8. Set `dp = new_dp`. Return the max value in the final `dp`.

### Worked Example (Dry Run)
Input: `grid = [[3,1,1],[1,5,1],[1,1,9]]`.

```
Row 0: dp[0][2] = 3 + 1 = 4. All others = -inf.

Row 1 (from dp[0][2]=4):
  r1: col 0 -> {0,1}. r2: col 2 -> {1,2}.
  (0,1): cherry=grid[1][0]+grid[1][1]=1+5=6. dp[0][1]=4+6=10.
  (0,2): cherry=grid[1][0]+grid[1][2]=1+1=2. dp[0][2]=4+2=6.
  (1,1): same cell. cherry=grid[1][1]=5. dp[1][1]=4+5=9.
  (1,2): cherry=grid[1][1]+grid[1][2]=5+1=6. dp[1][2]=4+6=10.

Row 2 (best from dp[0][1]=10):
  (0,2): cherry=grid[2][0]+grid[2][2]=1+9=10. dp[0][2]=10+10=20.
  (many other transitions, 20 is the max)
```

Answer: **20**. Robot1: `(0,0)->(1,0)->(2,0)` collects 3,1,1. Robot2: `(0,2)->(1,1)->(2,2)` collects 1,5,9. Total: 20.

### Code
```python
class Solution:
    def cherryPickup(self, grid: list) -> int:
        m, n = len(grid), len(grid[0])
        inf = float('inf')
        dp = [[-inf] * n for _ in range(n)]
        dp[0][n - 1] = grid[0][0] + grid[0][n - 1]
        for i in range(1, m):
            new_dp = [[-inf] * n for _ in range(n)]
            for c1 in range(n):
                for c2 in range(n):
                    if dp[c1][c2] == -inf:
                        continue
                    for d1 in (-1, 0, 1):
                        nc1 = c1 + d1
                        if nc1 < 0 or nc1 >= n:
                            continue
                        for d2 in (-1, 0, 1):
                            nc2 = c2 + d2
                            if nc2 < 0 or nc2 >= n:
                                continue
                            cherry = grid[i][nc1]
                            if nc1 != nc2:
                                cherry += grid[i][nc2]
                            new_dp[nc1][nc2] = max(
                                new_dp[nc1][nc2],
                                dp[c1][c2] + cherry
                            )
            dp = new_dp
        return max(max(row) for row in dp)
```

### Complexity
- Time: O(m x n^2 x 9) = O(m x n^2)
- Space: O(n^2)

### Common Mistakes & Edge Cases
- Same-column overlap: count the cell's cherry only once when `c1 == c2`.
- Initializing only `dp[0][n-1]` — all other row-0 states are unreachable.
- Not checking bounds on `nc1` and `nc2` (columns must be in `[0, n)`).
- m=1: both robots are already in the last row, return `grid[0][0] + grid[0][n-1]`.

---

## 3. Unique Paths III (LC #980) — Hard

### Problem Explanation
An m×n grid where `1` marks the start, `2` marks the end, `0` marks empty cells, and `-1` marks obstacles. Count all paths from start to end that visit **every non-obstacle cell exactly once**. You may move in 4 directions (up, down, left, right). The grid has at most 20 cells total, making bitmask DP feasible.

### State Definition
`dp[mask][i][j]` = number of distinct paths to reach cell `(i, j)` having visited exactly the set of cells indicated by `mask` (bitmask where bit `k` means cell `k` has been visited). Cell index `k = i * n + j`.

### Recurrence Relation
```
dp[mask | (1 << nxt)][ni][nj] += dp[mask][i][j]
```
From `(i, j)` with visited set `mask`, try moving to each unvisited, non-obstacle neighbor `(ni, nj)`. The neighbor's bit is set in the new mask.

### Base Cases
- `dp[1 << start][si][sj] = 1` — one path at the start cell with only itself visited.
- The answer is `dp[full_mask][ei][ej]` where `full_mask` has all non-obstacle bits set.

### Intuition (Why This Works)
With <=20 cells, every subset of visited cells can be represented as a bitmask (2^20 ~ 1M states). The transition is a standard DFS with memoization: from each state, try all valid moves. The bitmask prevents revisiting cells and the final mask check ensures all required cells are covered.

### Step-by-Step Procedure
1. Scan the grid to find start `(si,sj)`, end `(ei,ej)`, and count `empty` (non-obstacle cells).
2. Build `full_mask` with bits set for all non-obstacle cells.
3. Use memoized DFS from `(si, sj)` with `mask = 1 << (si*n + sj)`.
4. At each cell, try all 4 neighbors: skip out-of-bounds, obstacles, and already-visited cells.
5. If `(i,j) == (ei,ej)`: return 1 if `popcount(mask) == empty`, else 0.
6. Return the total count from the DFS.

### Worked Example (Dry Run)
Input: `grid = [[1,0,0],[0,0,0],[0,0,2]]`, m=3, n=3. Start=(0,0), End=(2,2), empty=9.

```
full_mask = 0b111111111 (all 9 cells).
dp[1][0][0] = 1.

From (0,0) mask=000000001: can go to (0,1) or (1,0).
  -> dp[000000011][0][1] += 1
  -> dp[000001001][1][0] += 1

... (continues exploring all paths)

Final: dp[0b111111111][2][2] = 12.
```

Answer: **12** distinct paths visit all 9 cells exactly once from top-left to bottom-right.

### Code
```python
class Solution:
    def uniquePathsIII(self, grid: list) -> int:
        m, n = len(grid), len(grid[0])
        start = end = None
        empty = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] != -1:
                    empty += 1
                if grid[i][j] == 1:
                    start = (i, j)
                elif grid[i][j] == 2:
                    end = (i, j)
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dfs(i, j, mask):
            if (i, j) == end:
                return 1 if bin(mask).count('1') == empty else 0
            count = 0
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] != -1:
                    bit = ni * n + nj
                    if not (mask >> bit) & 1:
                        count += dfs(ni, nj, mask | (1 << bit))
            return count

        return dfs(start[0], start[1], 1 << (start[0] * n + start[1]))
```

### Complexity
- Time: O(2^(m*n) x m x n) — each state explores 4 neighbors
- Space: O(2^(m*n) x m x n) for the memo table

### Common Mistakes & Edge Cases
- The start cell must be pre-set in the initial mask, or it can be "revisited."
- Checking `bin(mask).count('1') == empty` at the end cell ensures all cells are covered.
- Obstacles (`-1`) are excluded from `empty` and from the bitmask entirely.
- Grid with no obstacles: all cells must be visited, making the problem harder than it looks.
- Single-cell grid (start == end with empty == 1): return 1.

---

## 4. Paths with Maximum Gold (LC #1219) — Medium

### Problem Explanation
An m×n grid of non-negative integers. Start from any cell containing gold and move up, down, left, or right. You may visit a cell at most once. Collect gold from every visited cell and return the maximum gold you can collect. The key insight is that because you cannot revisit cells, this is a DFS/backtracking problem on a grid — DP alone does not work because the path can go in any direction, creating cycles without the visited guard.

### State Definition
There is no DP state in the traditional sense. The state is `(i, j, visited_mask)` or equivalently `(i, j)` with a visited set. We use DFS with backtracking: from each cell, explore all 4 neighbors that have not been visited.

### Recurrence Relation
```
dfs(i, j) = grid[i][j] + max(dfs(ni, nj) for each valid neighbor (ni, nj))
```
The maximum gold collectible starting from cell `(i, j)` equals the cell's gold plus the best result from any unvisited neighbor. After exploring all neighbors, unmark the cell (backtrack).

### Base Cases
- If `(i, j)` is out of bounds, or `grid[i][j] == 0`, or `(i, j)` is already visited → return 0.

### Intuition (Why This Works)
Since we cannot revisit cells, the branching factor is at most 4 and the depth is bounded by the number of gold cells. Backtracking explores all valid paths from a starting cell. The visited set prevents cycles. Trying every cell as a starting point covers all possibilities. This is exponential in the worst case but practical because grids are small (max 25 cells with gold).

### Step-by-Step Procedure
1. Identify all cells with gold > 0 as potential starting points.
2. For each starting cell, run DFS with backtracking.
3. At each cell, mark it visited, add its gold, try all 4 neighbors.
4. After exploring all neighbors, unmark the cell (backtrack).
5. Track the global maximum across all starting cells.
6. Return the global maximum.

### Worked Example (Dry Run)
Input: `grid = [[1,0,7],[2,0,6],[3,8,1]]`

```
Start at (2,1) with gold=8:
  Visit (2,1): gold=8, visited={(2,1)}
  → (2,0): gold=3, visited={(2,1),(2,0)}
    → (1,0): gold=2, visited={(2,1),(2,0),(1,0)}
      → (0,0): gold=1, visited={(2,1),(2,0),(1,0),(0,0)}
        → no unvisited neighbors with gold → backtrack, return 1
      → (0,1): grid[0][1]=0 → skip
      → best from (1,0) = 2 + 1 = 3, backtrack
    → (2,2): gold=1, visited={(2,1),(2,0),(1,0),(2,2)}
      → (1,2): gold=6, visited adds (1,2)
        → (0,2): gold=7, visited adds (0,2)
          → no unvisited → return 7
        → best from (1,2) = 6 + 7 = 13
      → best from (2,2) = 1 + 13 = 14
    → best from (2,0) = 3 + 3 + ... 
```

The optimal path: `(0,2)→(1,2)→(2,2)→(2,1)→(2,0)→(1,0)→(0,0)` = 7+6+1+8+3+2+1 = 28. Wait, that revisits. Let me re-trace: `(2,1)→(1,1)=0(skip)→(2,0)→(1,0)→(0,0)→back→(2,2)→(1,2)→(0,2)` = 8+3+2+1+1+6+7 = 28? No, that's not a valid path since (2,0)→(2,2) isn't adjacent.

Correct path from (2,1): up to (1,1)=0, skip. Left to (2,0)=3, then up to (1,0)=2, then up to (0,0)=1. Back to (2,1), right to (2,2)=1, up to (1,2)=6, up to (0,2)=7. Total: 8+3+2+1+1+6+7 = 28? But (2,0)→(2,1)→(2,2) means (2,0) and (2,2) aren't adjacent — you go through (2,1) which is already visited.

Correct: from (2,1): go to (2,0)=3, then (1,0)=2, then (0,0)=1 = 8+3+2+1 = 14. Or from (2,1): go to (2,2)=1, then (1,2)=6, then (0,2)=7 = 8+1+6+7 = 22. Or: (1,0)→(2,0)→(2,1)→(2,2)→(1,2)→(0,2) = 2+3+8+1+6+7 = 27. Or (0,0)→(1,0)→(2,0)→(2,1)→(2,2)→(1,2)→(0,2) = 1+2+3+8+1+6+7 = 28.

Answer: **28**.

### Code
```python
class Solution:
    def getMaximumGold(self, grid: list) -> int:
        m, n = len(grid), len(grid[0])
        self.ans = 0

        def dfs(i, j):
            if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == 0:
                return 0
            orig = grid[i][j]
            grid[i][j] = 0  # mark visited
            best = orig + max(dfs(i+1,j), dfs(i-1,j), dfs(i,j+1), dfs(i,j-1))
            grid[i][j] = orig  # backtrack
            return best

        for i in range(m):
            for j in range(n):
                if grid[i][j] > 0:
                    self.ans = max(self.ans, dfs(i, j))
        return self.ans
```

### Complexity
- Time: O(m × n × 3^(m×n)) — at most 3 directions from each cell (cannot go back), depth up to m×n
- Space: O(m×n) recursion stack in worst case

### Common Mistakes & Edge Cases
- Forgetting to backtrack (restore grid value after DFS).
- Not handling cells with value 0 — they should not be visited.
- All zeros grid → return 0.
- Single cell with gold → return that value.
- Grid where gold forms disconnected components — must try every starting cell.

---

## 5. Grid Minimum Falling Path Sum (LC #931) — Medium

### Problem Explanation
An n×n grid of integers. A falling path starts at any cell in the first row and moves to a cell in the adjacent row — specifically to a cell directly below, below-left, or below-right (column `j-1`, `j`, or `j+1`). Find the minimum sum of a falling path from the first row to the last row. This is a classic row-by-row DP: the best sum reaching any cell depends only on three cells in the row above.

### State Definition
`dp[j]` = minimum falling path sum ending at column `j` of the current row.

### Recurrence Relation
```
dp_new[j] = grid[i][j] + min(dp[j-1], dp[j], dp[j+1])
```
(terms with out-of-range indices are treated as infinity)
Each cell's best sum is its own value plus the minimum of the three cells above it from which you could have descended.

### Base Cases
- Row 0: `dp[j] = grid[0][j]` for all j (the path starts here).
- Final answer: `min(dp)` after processing the last row.

### Intuition (Why This Works)
At each row, the only thing that matters is the minimum cost to reach each column. The transition looks at up to 3 predecessors (directly above, above-left, above-right). Processing row by row, each row only depends on the previous row, so space can be O(n). The choice at each cell is "which of the three parent cells gives the minimum total?"

### Step-by-Step Procedure
1. Initialize `dp = grid[0][:]` (copy of first row).
2. For each row `i` from 1 to n-1:
3. Create `new_dp` of size n.
4. For each column `j`: `new_dp[j] = grid[i][j] + min(dp[j-1] if j>0, dp[j], dp[j+1] if j<n-1)`.
5. Set `dp = new_dp`.
6. Return `min(dp)`.

### Worked Example (Dry Run)
Input: `grid = [[2,1,3],[6,5,4],[7,8,9]]`

```
Row 0: dp = [2, 1, 3]

Row 1:
  j=0: 6 + min(dp[-1]=inf, dp[0]=2, dp[1]=1) = 6 + 1 = 7
  j=1: 5 + min(dp[0]=2, dp[1]=1, dp[2]=3) = 5 + 1 = 6
  j=2: 4 + min(dp[1]=1, dp[2]=3, dp[3]=inf) = 4 + 1 = 5
  dp = [7, 6, 5]

Row 2:
  j=0: 7 + min(inf, 7, 6) = 7 + 6 = 13
  j=1: 8 + min(7, 6, 5) = 8 + 5 = 13
  j=2: 9 + min(6, 5, inf) = 9 + 5 = 14
  dp = [13, 13, 14]
```

Answer: **13**. Path: 1 → 5 → 7 (columns 1, 1, 0) or 1 → 4 → 8 (columns 1, 2, 1).

### Code
```python
class Solution:
    def minFallingPathSum(self, matrix: list) -> int:
        n = len(matrix)
        dp = matrix[0][:]
        for i in range(1, n):
            new_dp = [float('inf')] * n
            for j in range(n):
                for dj in (-1, 0, 1):
                    pj = j + dj
                    if 0 <= pj < n:
                        new_dp[j] = min(new_dp[j], dp[pj] + matrix[i][j])
            dp = new_dp
        return min(dp)
```

### Complexity
- Time: O(n²) — each row processes n cells, each looking at 3 predecessors.
- Space: O(n).

### Common Mistakes & Edge Cases
- Not handling boundary columns (j=0 and j=n-1 have only 2 predecessors).
- Using `float('inf')` correctly for out-of-range predecessors.
- n=1: return the single cell value.
- All negative values: still works, min handles them.
- Using `max` instead of `min` (would give maximum falling path).

---

## 6. Minimum Falling Path Sum II (LC #1289) — Hard

### Problem Explanation
Same as Minimum Falling Path Sum, but with one critical restriction: you **cannot** move to a cell in the same column as the previous row's cell. From `matrix[i-1][j]` you may only go to `matrix[i][k]` where `k != j`. Find the minimum falling path sum from any cell in the first row to any cell in the last row. The key insight is to track the two smallest values per row, so we can always pick the best predecessor that is not in the same column.

### State Definition
For each row, track `min1` (smallest value), `min1_col` (its column), and `min2` (second smallest value). This avoids checking all n predecessors per cell.

### Recurrence Relation
```
For each cell j in row i:
  if j != min1_col:  new_dp[j] = matrix[i][j] + min1
  else:              new_dp[j] = matrix[i][j] + min2
```
Each cell picks the minimum from the previous row excluding its own column. The two-smallest trick makes this O(1) per cell instead of O(n).

### Base Cases
- Row 0: `dp[j] = matrix[0][j]` for all j.
- Final answer: `min(dp)` after the last row.

### Intuition (Why This Works)
Without the column restriction, each cell looks at 3 predecessors. With the restriction, each cell must look at all n predecessors except one. Naively this is O(n²). The trick: if the global minimum of the previous row is NOT in the same column, use it. Otherwise use the second-best. Two minimums per row give O(1) per cell, yielding O(n²) total.

### Step-by-Step Procedure
1. Initialize `dp = matrix[0][:]`.
2. For each row `i` from 1 to n-1:
3. Find the two smallest values and their columns in `dp`.
4. For each column `j`: if `j != min1_col`, `new_dp[j] = matrix[i][j] + min1`; else `new_dp[j] = matrix[i][j] + min2`.
5. Set `dp = new_dp`.
6. Return `min(dp)`.

### Worked Example (Dry Run)
Input: `matrix = [[1,2,3],[4,5,6],[7,8,9]]`

```
Row 0: dp = [1, 2, 3]
  min1=1 (col 0), min2=2 (col 1)

Row 1:
  j=0: can't use min1 (col 0) → 4 + min2=2 = 6
  j=1: can use min1 → 5 + 1 = 6
  j=2: can use min1 → 6 + 1 = 7
  dp = [6, 6, 7]
  min1=6 (col 0), min2=6 (col 1)

Row 2:
  j=0: can't use min1 (col 0) → 7 + 6 = 13
  j=1: can't use min2 if col 1 = min1_col? min1 at col 0, so j=1≠0 → 8 + 6 = 14
  j=2: min1 at col 0, j=2≠0 → 9 + 6 = 15
  dp = [13, 14, 15]
```

Answer: **13**. Path: 1 (col 0) → 6 (col 2) → 7 (col 0) = 1+6+7=14? No: 1→5(col 1)→7(col 0) = 1+5+7=13. Or 2→4→8=14. Best: 1+5+7=13 (but same column issue: col 0→col 1→col 0, all different, valid).

### Code
```python
class Solution:
    def minFallingPathSum(self, matrix: list) -> int:
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        dp = matrix[0][:]
        for i in range(1, n):
            # Find two smallest in dp
            min1 = min2 = float('inf')
            min1_col = -1
            for j in range(n):
                if dp[j] < min1:
                    min2 = min1
                    min1 = dp[j]
                    min1_col = j
                elif dp[j] < min2:
                    min2 = dp[j]
            new_dp = [0] * n
            for j in range(n):
                if j != min1_col:
                    new_dp[j] = matrix[i][j] + min1
                else:
                    new_dp[j] = matrix[i][j] + min2
            dp = new_dp
        return min(dp)
```

### Complexity
- Time: O(n²) — each row: O(n) to find two minimums + O(n) to compute new dp.
- Space: O(n).

### Common Mistakes & Edge Cases
- n=1: return `matrix[0][0]` directly (no previous row to conflict with).
- When all values in previous row are the same: min1 == min2, column restriction still applies.
- Negative values: the two-minimum logic handles them correctly.
- Off-by-one in finding the two minimums — make sure min1 and min2 are distinct values, not just distinct columns.
- Forgetting that min1_col is a column index, not a value.

---

## 7. Knight Dialer (LC #935) — Medium

### Problem Explanation
A chess knight is placed on a standard phone keypad:
```
1 2 3
4 5 6
7 8 9
  0
```
The knight makes exactly `n-1` moves to dial an n-digit number. The knight's L-shaped moves are: (±2,±1) and (±1,±2). Given `n`, count how many distinct phone numbers of length n the knight can dial. Since cells like corners of the keypad are unreachable by a knight, the count is less than 10^n. Return the answer modulo 10^9+7.

### State Definition
`dp[step][pos]` = number of distinct sequences of length `step+1` ending at keypad position `pos`. Space-optimized to `dp[pos]` for the current step.

### Recurrence Relation
```
dp_new[next] += dp[curr]  for each valid knight move from curr to next
```
Each position contributes its count to all positions reachable by a knight move.

### Base Cases
- Step 0: `dp[pos] = 1` for all 10 positions (each digit alone is a 1-length number).

### Intuition (Why This Works)
The knight's moves form a fixed transition graph on 10 nodes. At each step, the count at each node is the sum of counts from all nodes that can reach it in one move. This is matrix exponentiation on the transition graph, or equivalently O(n × 10 × 6) DP (each node has at most 6 outgoing edges). The modulo prevents overflow.

### Step-by-Step Procedure
1. Define the move map: each digit maps to the digits reachable by a knight.
2. Initialize `dp = [1] * 10`.
3. Repeat `n-1` times:
4. Create `new_dp = [0] * 10`.
5. For each position `curr` with count `dp[curr]`, add `dp[curr]` to `new_dp[next]` for each valid `next`.
6. Set `dp = new_dp` (mod 10^9+7 after each addition).
7. Return `sum(dp) % MOD`.

### Worked Example (Dry Run)
Input: `n = 2`.

```
Moves: 0→(4,6), 1→(6,8), 2→(7,9), 3→(4,8), 4→(0,3,9),
       5→(none), 6→(0,1,7), 7→(2,6), 8→(1,3), 9→(2,4)

Step 0: dp = [1,1,1,1,1,1,1,1,1,1]

Step 1:
  dp_new[0] += dp[4]+dp[6] = 1+1 = 2
  dp_new[1] += dp[6]+dp[8] = 1+1 = 2
  dp_new[2] += dp[7]+dp[9] = 1+1 = 2
  dp_new[3] += dp[4]+dp[8] = 1+1 = 2
  dp_new[4] += dp[0]+dp[3]+dp[9] = 3
  dp_new[5] = 0
  dp_new[6] += dp[0]+dp[1]+dp[7] = 3
  dp_new[7] += dp[2]+dp[6] = 2
  dp_new[8] += dp[1]+dp[3] = 2
  dp_new[9] += dp[2]+dp[4] = 2

  dp = [2,2,2,2,3,0,3,2,2,2]
```

Answer: **sum = 2+2+2+2+3+0+3+2+2+2 = 20**.

### Code
```python
class Solution:
    def knightDialer(self, n: int) -> int:
        MOD = 10**9 + 7
        moves = {
            0: [4, 6], 1: [6, 8], 2: [7, 9], 3: [4, 8],
            4: [0, 3, 9], 5: [], 6: [0, 1, 7],
            7: [2, 6], 8: [1, 3], 9: [2, 4]
        }
        dp = [1] * 10
        for _ in range(n - 1):
            new_dp = [0] * 10
            for curr in range(10):
                for nxt in moves[curr]:
                    new_dp[nxt] = (new_dp[nxt] + dp[curr]) % MOD
            dp = new_dp
        return sum(dp) % MOD
```

### Complexity
- Time: O(n × 10 × 6) = O(n) — 10 positions, at most 6 moves each.
- Space: O(10) = O(1).

### Common Mistakes & Edge Cases
- n=1: return 10 (every digit is valid).
- Digit 5 has no knight moves — it cannot be reached after the first step.
- Modulo: apply at every addition, not just at the end.
- Incorrect move map — knight moves are L-shaped (2+1), not diagonal.
- Using a matrix exponentiation approach for O(log n) time is possible but DP is simpler.

---

## 8. Out of Boundary Paths (LC #576) — Medium

### Problem Explanation
There is an m×n grid with a ball at position `(startRow, startCol)`. You may move the ball up, down, left, or right at most `maxMove` times. Count the number of paths that move the ball out of the grid boundary. Return the count modulo 10^9+7. The ball leaves the grid as soon as it crosses any boundary — that counts as one valid path.

### State Definition
`dp[moves][i][j]` = number of ways to reach cell `(i, j)` after exactly `moves` steps without having left the grid. Alternatively, `dp[i][j]` = number of ways to be at `(i, j)` after the current number of steps (rolling array).

### Recurrence Relation
```
dp_new[ni][nj] += dp[i][j]  for each valid neighbor (ni, nj) inside the grid
out_of_bounds_count += dp[i][j] for neighbors outside the grid
```
At each step, each cell contributes its count to its 4 neighbors. If a neighbor is out of bounds, those paths are counted as completed boundary crossings.

### Base Cases
- Step 0: `dp[startRow][startCol] = 1`.

### Intuition (Why This Works)
At each step, the ball's position distributes among its neighbors. Paths that step out of bounds are "absorbed" — they contribute to the answer and don't continue. DP over the number of moves captures this: each step either moves within the grid (continue counting) or exits (add to answer). Rolling the dp array saves space.

### Step-by-Step Procedure
1. Initialize `dp[startRow][startCol] = 1`, all others 0.
2. For each move from 1 to maxMove:
3. Create `new_dp` all zeros.
4. For each cell `(i, j)` with count `dp[i][j] > 0`:
5. For each of 4 neighbors `(ni, nj)`:
6. If `(ni, nj)` is inside the grid, add `dp[i][j]` to `new_dp[ni][nj]`.
7. If outside, add `dp[i][j]` to the answer.
8. Set `dp = new_dp`.
9. Return `answer % MOD`.

### Worked Example (Dry Run)
Input: `m=2, n=2, maxMove=2, startRow=0, startCol=0`

```
Grid:  (0,0) (0,1)
       (1,0) (1,1)

Step 0: dp = [[1,0],[0,0]]

Step 1: from (0,0):
  → (0,1): in bounds, dp_new[0][1] += 1
  → (1,0): in bounds, dp_new[1][0] += 1
  → (-1,0): out of bounds, answer += 1
  → (0,-1): out of bounds, answer += 1
  dp = [[0,1],[1,0]], answer = 2

Step 2: from (0,1):
  → (0,0): dp_new[0][0] += 1
  → (1,1): dp_new[1][1] += 1
  → (-1,1): out, answer += 1
  → (0,2): out, answer += 1
  from (1,0):
  → (0,0): dp_new[0][0] += 1
  → (1,1): dp_new[1][1] += 1
  → (2,0): out, answer += 1
  → (1,-1): out, answer += 1
  dp = [[2,0],[0,2]], answer = 2+4 = 6
```

Answer: **6**.

### Code
```python
class Solution:
    def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
        MOD = 10**9 + 7
        dp = [[0] * n for _ in range(m)]
        dp[startRow][startColumn] = 1
        ans = 0
        for _ in range(maxMove):
            new_dp = [[0] * n for _ in range(m)]
            for i in range(m):
                for j in range(n):
                    if dp[i][j] == 0:
                        continue
                    for di, dj in [(0,1),(0,-1),(1,0),(-1,0)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < m and 0 <= nj < n:
                            new_dp[ni][nj] = (new_dp[ni][nj] + dp[i][j]) % MOD
                        else:
                            ans = (ans + dp[i][j]) % MOD
            dp = new_dp
        return ans
```

### Complexity
- Time: O(maxMove × m × n) — each step processes every cell.
- Space: O(m × n) (two grids swapped).

### Common Mistakes & Edge Cases
- maxMove=0: return 0 (cannot leave the grid).
- Ball starts on a boundary: still needs at least 1 move to exit.
- Very large grid with small maxMove: most cells stay at 0, could optimize with BFS-like propagation.
- Modulo at every addition to prevent overflow.
- Starting position already out of bounds is not possible per constraints.

---

## 9. Range Sum Query 2D — Immutable (LC #304) — Medium

### Problem Explanation
Given a 2D matrix `matrix`, compute the sum of elements inside a rectangle defined by its upper-left corner `(row1, col1)` and lower-right corner `(row2, col2)`. Multiple queries may be asked. The key technique is to precompute a 2D prefix sum array so each query is answered in O(1) time.

### State Definition
`prefix[i][j]` = sum of all elements in the sub-rectangle from `(0, 0)` to `(i-1, j-1)` (1-indexed padding for cleaner boundary handling).

### Recurrence Relation
```
prefix[i][j] = matrix[i-1][j-1] + prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1]
```
The sum of the rectangle ending at `(i,j)` equals the cell itself, plus the rectangle above, plus the rectangle to the left, minus the rectangle counted twice (above-left diagonal). This is the inclusion-exclusion principle.

### Base Cases
- `prefix[0][j] = 0` for all j (empty row above).
- `prefix[i][0] = 0` for all i (empty column to the left).

### Intuition (Why This Works)
The 2D prefix sum generalizes the 1D prefix sum. With 1D, `sum[l..r] = prefix[r+1] - prefix[l]`. In 2D, the sum of rectangle `(r1,c1)` to `(r2,c2)` uses four corners:
```
sum = prefix[r2+1][c2+1] - prefix[r1][c2+1] - prefix[r2+1][c1] + prefix[r1][c1]
```
The precomputation takes O(m×n) and each query takes O(1).

### Step-by-Step Procedure
1. Build `prefix` of size `(m+1) × (n+1)` filled with 0.
2. For each cell `(i, j)` from `(1,1)` to `(m,n)`:
3. `prefix[i][j] = matrix[i-1][j-1] + prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1]`.
4. For a query `(r1, c1, r2, c2)`:
5. Return `prefix[r2+1][c2+1] - prefix[r1][c2+1] - prefix[r2+1][c1] + prefix[r1][c1]`.

### Worked Example (Dry Run)
Input: `matrix = [[3,0,1],[5,6,2],[1,8,3]]`

```
Building prefix (1-indexed, 0-row and 0-col are padding):

prefix[1][1] = 3 + 0 + 0 - 0 = 3
prefix[1][2] = 0 + 0 + 3 - 0 = 3
prefix[1][3] = 1 + 0 + 3 - 0 = 4
prefix[2][1] = 5 + 0 + 3 - 0 = 8
prefix[2][2] = 6 + 5 + 3 - 0 = 14
prefix[2][3] = 2 + 1 + 14 - 3 = 14... 
```

Let me redo this properly:
```
prefix:
     0  1  2  3  4
  0  0  0  0  0  0
  1  0  3  3  4  4
  2  0  8 14 16 17
  3  0  9 23 32 34
```

Wait, let me be careful:
matrix:
```
[3, 0, 1]
[5, 6, 2]
[1, 8, 3]
```

prefix[1][1] = matrix[0][0] = 3
prefix[1][2] = matrix[0][1] + prefix[1][1] = 0 + 3 = 3
prefix[1][3] = matrix[0][2] + prefix[1][2] = 1 + 3 = 4
prefix[2][1] = matrix[1][0] + prefix[1][1] = 5 + 3 = 8
prefix[2][2] = matrix[1][1] + prefix[1][2] + prefix[2][1] - prefix[1][1] = 6 + 3 + 8 - 3 = 14
prefix[2][3] = matrix[1][2] + prefix[1][3] + prefix[2][2] - prefix[1][2] = 2 + 4 + 14 - 3 = 17
prefix[3][1] = matrix[2][0] + prefix[2][1] = 1 + 8 = 9
prefix[3][2] = matrix[2][1] + prefix[2][2] + prefix[3][1] - prefix[2][1] = 8 + 14 + 9 - 8 = 23
prefix[3][3] = matrix[2][2] + prefix[2][3] + prefix[3][2] - prefix[2][2] = 3 + 17 + 23 - 14 = 29

prefix:
     0  1  2  3
  0  0  0  0  0
  1  0  3  3  4
  2  0  8 14 17
  3  0  9 23 29
```

Query: sumRegion(1, 1, 2, 2) → sum of [[6,2],[8,3]] = 19
= prefix[3][3] - prefix[1][3] - prefix[3][1] + prefix[1][1]
= 29 - 4 - 9 + 3 = 19 ✓

### Code
```python
class NumMatrix:
    def __init__(self, matrix: list):
        m, n = len(matrix), len(matrix[0])
        self.prefix = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                self.prefix[i][j] = (matrix[i-1][j-1]
                                     + self.prefix[i-1][j]
                                     + self.prefix[i][j-1]
                                     - self.prefix[i-1][j-1])

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (self.prefix[row2+1][col2+1]
                - self.prefix[row1][col2+1]
                - self.prefix[row2+1][col1]
                + self.prefix[row1][col1])
```

### Complexity
- Preprocessing: O(m × n).
- Each query: O(1).
- Space: O(m × n).

### Common Mistakes & Edge Cases
- Off-by-one: the prefix array is `(m+1) × (n+1)` to handle `row1=0` or `col1=0` without special cases.
- The inclusion-exclusion signs: `+bottom-right -top-right -bottom-left +top-left`.
- Single-cell matrix: prefix is 2×2, queries work correctly.
- Multiple queries: preprocessing cost is amortized over all queries.
- Not using 1-indexed prefix: requires conditional checks for boundary rows/columns.
