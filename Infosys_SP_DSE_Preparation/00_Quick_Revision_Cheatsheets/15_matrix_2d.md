# 15. Matrix & 2D Arrays

All matrix patterns for coding rounds. Indices: `matrix[r][c]`, r = row, c = column.

## Creating a 2D list — and the classic bug

```python
m, n = 3, 4

# CORRECT: independent rows
grid = [[0] * n for _ in range(m)]
grid[0][0] = 5
print(grid[1][0])   # 0  (rows are independent)

# BUG: rows are the SAME list object (shallow copy of the row)
bug = [[0] * n] * m
bug[0][0] = 5
print(bug[1][0])    # 5  — WRONG! all rows share one list
```

Always build with `[[0] * n for _ in range(m)]`. Never `[[0] * n] * m`.

## Traversal

```python
rows, cols = len(grid), len(grid[0])

# row-major
for r in range(rows):
    for c in range(cols):
        val = grid[r][c]

# column-major
for c in range(cols):
    for r in range(rows):
        val = grid[r][c]
```

## 4-directional and 8-directional moves

```python
def neighbors4(grid, r, c):
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            yield nr, nc

def neighbors8(grid, r, c):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                yield nr, nc
```

Complexity: O(1) per neighbor, used inside BFS/DFS giving O(rows*cols).

## Transpose

```python
# square matrix, in-place
def transpose_square(a):
    n = len(a)
    for i in range(n):
        for j in range(i + 1, n):
            a[i][j], a[j][i] = a[j][i], a[i][j]

# rectangular, returns a NEW matrix
def transpose_rect(a):
    return [list(col) for col in zip(*a)]

print(transpose_rect([[1, 2, 3], [4, 5, 6]]))   # [[1, 4], [2, 5], [3, 6]]
```

Complexity: O(n^2) time, O(1) extra space (square); O(mn) time and space (rectangular).

## Rotate 90 degrees

```python
# clockwise: transpose + reverse each row
def rotate90_cw(a):
    n = len(a)
    for i in range(n):
        for j in range(i + 1, n):
            a[i][j], a[j][i] = a[j][i], a[i][j]
    for row in a:
        row.reverse()

# counterclockwise: reverse each row + transpose
def rotate90_ccw(a):
    for row in a:
        row.reverse()
    n = len(a)
    for i in range(n):
        for j in range(i + 1, n):
            a[i][j], a[j][i] = a[j][i], a[i][j]

a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rotate90_cw(a)
print(a)   # [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
rotate90_ccw(a)
print(a)   # [[1, 2, 3], [4, 5, 6], [7, 8, 9]] (round trip)
```

Complexity: O(n^2) time, O(1) extra space.

## Spiral traversal

```python
def spiral_order(matrix):
    res = []
    if not matrix:
        return res
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for j in range(left, right + 1):            # right along top
            res.append(matrix[top][j])
        top += 1
        for i in range(top, bottom + 1):            # down along right
            res.append(matrix[i][right])
        right -= 1
        if top <= bottom:                           # left along bottom
            for j in range(right, left - 1, -1):
                res.append(matrix[bottom][j])
            bottom -= 1
        if left <= right:                           # up along left
            for i in range(bottom, top - 1, -1):
                res.append(matrix[i][left])
            left += 1
    return res

print(spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
# [1, 2, 3, 6, 9, 8, 7, 4, 5]
```

Complexity: O(mn) time, O(1) extra space (excluding result).

## Set matrix zeroes (in-place, O(1) extra space)

```python
def set_zeroes(matrix):
    if not matrix:
        return
    rows, cols = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][j] == 0 for j in range(cols))
    first_col_zero = any(matrix[i][0] == 0 for i in range(rows))
    for i in range(1, rows):                        # use first row/col as markers
        for j in range(1, cols):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    for i in range(1, rows):
        for j in range(1, cols):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if first_row_zero:
        for j in range(cols):
            matrix[0][j] = 0
    if first_col_zero:
        for i in range(rows):
            matrix[i][0] = 0
```

Complexity: O(mn) time, O(1) extra space.

## Search in a row+column sorted matrix (staircase)

```python
def search_matrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
    rows, cols = len(matrix), len(matrix[0])
    r, c = 0, cols - 1                        # start top-right
    while r < rows and c >= 0:
        if matrix[r][c] == target:
            return True
        elif matrix[r][c] > target:           # go left (smaller)
            c -= 1
        else:                                 # go down (bigger)
            r += 1
    return False

mat = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16]]
print(search_matrix(mat, 5))    # True
print(search_matrix(mat, 10))   # False
```

Complexity: O(rows + cols) time, O(1) space.

## Diagonal traversal (zig-zag)

```python
def diagonal_traverse(matrix):
    if not matrix:
        return []
    rows, cols = len(matrix), len(matrix[0])
    res = []
    for d in range(rows + cols - 1):
        if d % 2 == 0:                        # up-right
            r = min(d, rows - 1)
            c = d - r
            while r >= 0 and c < cols:
                res.append(matrix[r][c])
                r -= 1
                c += 1
        else:                                 # down-left
            c = min(d, cols - 1)
            r = d - c
            while c >= 0 and r < rows:
                res.append(matrix[r][c])
                c -= 1
                r += 1
    return res

print(diagonal_traverse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
# [1, 2, 4, 7, 5, 3, 6, 8, 9]
```

Complexity: O(mn) time, O(1) extra space (excluding result).

## Matrix multiplication

```python
def matmul(a, b):
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])
    assert cols_a == rows_b
    res = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for k in range(cols_a):          # k-outer order: cache friendly
            if a[i][k]:
                for j in range(cols_b):
                    res[i][j] += a[i][k] * b[k][j]
    return res

print(matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]]))   # [[19, 22], [43, 50]]
```

Complexity: O(pqr) time where a is p x q and b is q x r; O(p*r) space.

## 2D prefix sum — build + rectangle query

```python
class PrefixSum2D:
    def __init__(self, grid):
        m, n = len(grid), len(grid[0])
        self.ps = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                self.ps[i + 1][j + 1] = (grid[i][j] + self.ps[i][j + 1]
                                         + self.ps[i + 1][j] - self.ps[i][j])

    def query(self, r1, c1, r2, c2):     # inclusive rectangle (r1,c1)-(r2,c2)
        return (self.ps[r2 + 1][c2 + 1] - self.ps[r1][c2 + 1]
                - self.ps[r2 + 1][c1] + self.ps[r1][c1])

grid = [[3, 0, 1, 4], [5, 6, 3, 2], [1, 2, 0, 1], [4, 1, 0, 2]]
ps = PrefixSum2D(grid)
print(ps.query(0, 0, 1, 1))   # 3+0+5+6 = 14
print(ps.query(1, 1, 3, 3))   # 6+3+2+2+0+1+1+0+2 = 17
```

Complexity: O(mn) build, O(1) per query, O(mn) space.

## Longest increasing path in a matrix (DFS + memo)

```python
def longest_increasing_path(matrix):
    if not matrix:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    memo = [[0] * cols for _ in range(rows)]
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def dfs(r, c):
        if memo[r][c]:
            return memo[r][c]
        best = 1
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))
        memo[r][c] = best
        return best

    return max(dfs(r, c) for r in range(rows) for c in range(cols))

print(longest_increasing_path([[9, 9, 4], [6, 6, 8], [2, 1, 1]]))   # 4
```

Complexity: O(mn) time, O(mn) space (memo + recursion).
