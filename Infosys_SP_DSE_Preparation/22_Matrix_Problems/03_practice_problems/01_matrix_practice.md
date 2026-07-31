# Matrix Practice Problems - Infosys SP DSE

> **Problem Difficulty Guide:**
> ```
> ┌─────────────────────────────────────────────────────────────┐
> │  EASY: Basic traversal, simple transformations             │
> │        Time: O(m×n), Space: O(1) typically                 │
> │                                                             │
> │  MEDIUM: Pattern recognition, boundary simulation           │
> │          Time: O(m×n), may need extra space                 │
> │                                                             │
> │  HARD: Backtracking, binary search on answer                │
> │        Time: O(9^e) or O(m×logn×logV)                      │
> └─────────────────────────────────────────────────────────────┘
> ```

---

## EASY

---

### Problem 1: Transpose Matrix

**Problem Statement:**
Given a 2D integer array `matrix`, return the transpose of the matrix. The transpose of a matrix is the matrix flipped over its main diagonal (swap rows with columns).

```
Input: matrix = [[1,2,3],[4,5,6]]
Output: [[1,4],[2,5],[3,6]]
```

**Approach:**
- For an MxN matrix, the transpose is NxM.
- Swap `result[j][i] = matrix[i][j]`.

**Solution:**
```python
def transpose(matrix):
    m, n = len(matrix), len(matrix[0])
    result = [[0] * m for _ in range(n)]
    for i in range(m):
        for j in range(n):
            result[j][i] = matrix[i][j]
    return result
```

**Complexity:** Time O(m*n), Space O(m*n)

---

### Problem 2: Reshape Matrix

**Problem Statement:**
Reshape a matrix to a new shape (r x c). If not possible, return the original matrix.

```
Input: matrix = [[1,2],[3,4]], r=1, c=4
Output: [[1,2,3,4]]
```

**Approach:**
- Check if `r*c == m*n`. If not, return original.
- Flatten the matrix, then reshape.

**Solution:**
```python
def matrixReshape(matrix, r, c):
    m, n = len(matrix), len(matrix[0])
    if m * n != r * c:
        return matrix
    
    flat = [matrix[i][j] for i in range(m) for j in range(n)]
    result = []
    for i in range(r):
        result.append(flat[i * c : (i + 1) * c])
    return result
```

**Complexity:** Time O(m*n), Space O(m*n)

---

### Problem 3: Flipping an Image

**Problem Statement:**
Given an n x n binary matrix, flip the image horizontally (reverse each row), then invert it (0 -> 1, 1 -> 0).

```
Input: [[1,1,0],[1,0,1],[0,0,0]]
Output: [[1,0,0],[0,1,0],[1,1,1]]
```

**Approach:**
- Reverse each row, then flip bits.
- Optimized: Two pointers swapping while flipping.

**Solution:**
```python
def flipAndInvertImage(matrix):
    n = len(matrix)
    for row in matrix:
        left, right = 0, n - 1
        while left <= right:
            # Swap and flip simultaneously
            row[left], row[right] = 1 - row[right], 1 - row[left]
            left += 1
            right -= 1
        # Handle middle element for odd-length rows
        if n % 2 == 1:
            row[n // 2] = 1 - row[n // 2]
    return matrix
```

**Complexity:** Time O(n²), Space O(1)

---

### Problem 4: Toeplitz Matrix

**Problem Statement:**
Return True if the matrix is Toeplitz (every diagonal from top-left to bottom-right has the same elements).

```
Visual: What is a Toeplitz Matrix?

  ┌───┬───┬───┬───┐
  │ 1 │ 2 │ 3 │ 4 │
  ├───┼───┼───┼───┤
  │ 5 │ 1 │ 2 │ 3 │    All diagonals (top-left to bottom-right)
  ├───┼───┼───┼───┤    have the same element:
  │ 9 │ 5 │ 1 │ 2 │
  └───┴───┴───┴───┘

  Diagonals:
    ↘ 1 (single)     → [1]
    ↘ 2, 2 (pair)    → [2, 2]
    ↘ 3, 1, 3 (triple) → wait, that's wrong...
    
  Let me show the actual diagonals:
  
  Diagonal 1 (starts at [0,0]): 1, 1, 1
  Diagonal 2 (starts at [0,1]): 2, 2
  Diagonal 3 (starts at [0,2]): 3
  Diagonal 4 (starts at [1,0]): 5, 5
  Diagonal 5 (starts at [2,0]): 9
  
  Each diagonal has the SAME element. ✓

  Key insight: For each cell (i,j), check if matrix[i][j] == matrix[i+1][j+1]
  You only need to check rows 0..m-2 and cols 0..n-2.
```

```
Input: [[1,2,3,4],[5,1,2,3],[9,5,1,2]]
Output: True
```

**Approach:**
- For each cell `(i, j)`, check if `matrix[i][j] == matrix[i+1][j+1]`.
- Only need to check from row 0 and column 0.

**Solution:**
```python
def isToeplitzMatrix(matrix):
    m, n = len(matrix), len(matrix[0])
    for i in range(m - 1):
        for j in range(n - 1):
            if matrix[i][j] != matrix[i + 1][j + 1]:
                return False
    return True
```

**Complexity:** Time O(m*n), Space O(1)

---

## MEDIUM

---

### Problem 5: Spiral Matrix

**Problem Statement:**
Given an m x n matrix, return all elements in spiral order.

```
Visual: Spiral Traversal Animation

For input: [[1,2,3],[4,5,6],[7,8,9]]

Step 1: RIGHT (top row)          Step 2: DOWN (right col)
┌───┬───┬───┐                    ┌───┬───┬───┐
│→→→│→→→│→→→│                    │ 1 │ 2 │ 3 │
├───┼───┼───┤                    ├───┼───┼───┤
│ 4 │ 5 │ 6 │                    │ 4 │ 5 │ ↓ │
├───┼───┼───┤                    ├───┼───┼───┤
│ 7 │ 8 │ 9 │                    │ 7 │ 8 │ ↓ │
└───┴───┴───┘                    └───┴───┴───┘
Result so far: [1,2,3]           Result: [1,2,3,6,9]

Step 3: LEFT (bottom row)        Step 4: UP (left col)
┌───┬───┬───┐                    ┌───┬───┬───┐
│ 1 │ 2 │ 3 │                    │ 1 │ 2 │ 3 │
├───┼───┼───┤                    ├───┼───┼───┤
│ 4 │ 5 │ 6 │                    │ ↑ │ 5 │ 6 │
├───┼───┼───┤                    ├───┼───┼───┤
│←←←│←←←│←←←│                    │ 7 │ 8 │ 9 │
└───┴───┴───┘                    └───┴───┴───┘
Result: [1,2,3,6,9,8,7]         Result: [1,2,3,6,9,8,7,4]

Inner element: 5
Final result: [1,2,3,6,9,8,7,4,5]
```

```
Input: [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]
```

**Approach:**
- Use four boundaries: top, bottom, left, right.
- Traverse right -> down -> left -> up, shrinking boundaries each time.

**Solution:**
```python
def spiralOrder(matrix):
    if not matrix:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            result.append(matrix[top][j])
        top += 1
        
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        
        if top <= bottom:
            for j in range(right, left - 1, -1):
                result.append(matrix[bottom][j])
            bottom -= 1
        
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    
    return result
```

**Complexity:** Time O(m*n), Space O(1)

---

### Problem 6: Rotate Image

**Problem Statement:**
Given an n x n matrix, rotate it 90 degrees clockwise in-place.

```
Visual: Two-Step Rotation

Step 1: TRANSPOSE (swap rows ↔ columns)
  Before:           After Transpose:
  ┌───┬───┬───┐    ┌───┬───┬───┐
  │ 1 │ 2 │ 3 │    │ 1 │ 4 │ 7 │
  ├───┼───┼───┤    ├───┼───┼───┤
  │ 4 │ 5 │ 6 │ →  │ 2 │ 5 │ 8 │
  ├───┼───┼───┤    ├───┼───┼───┤
  │ 7 │ 8 │ 9 │    │ 3 │ 6 │ 9 │
  └───┴───┴───┘    └───┴───┴───┘

  How: matrix[i][j] ↔ matrix[j][i] for i < j
  (0,1)↔(1,0): 2 ↔ 4
  (0,2)↔(2,0): 3 ↔ 7
  (1,2)↔(2,1): 6 ↔ 8

Step 2: REVERSE each row
  Before:           After Reverse:
  ┌───┬───┬───┐    ┌───┬───┬───┐
  │ 1 │ 4 │ 7 │    │ 7 │ 4 │ 1 │
  ├───┼───┼───┤    ├───┼───┼───┤
  │ 2 │ 5 │ 8 │ →  │ 8 │ 5 │ 2 │
  ├───┼───┼───┤    ├───┼───┼───┤
  │ 3 │ 6 │ 9 │    │ 9 │ 6 │ 3 │
  └───┴───┴───┘    └───┴───┴───┘

  Result: 90° clockwise rotation! ✓
```

```
Input: [[1,2,3],[4,5,6],[7,8,9]]
Output: [[7,4,1],[8,5,2],[9,6,3]]
```

**Approach:**
- Transpose the matrix, then reverse each row.

**Solution:**
```python
def rotate(matrix):
    n = len(matrix)
    # Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Reverse each row
    for i in range(n):
        matrix[i].reverse()
    return matrix
```

**Complexity:** Time O(n²), Space O(1)

---

### Problem 7: Set Matrix Zeroes

**Problem Statement:**
Given an m x n matrix, if an element is 0, set its entire row and column to 0. Do it in-place.

```
Input: [[1,1,1],[1,0,1],[1,1,1]]
Output: [[1,0,1],[0,0,0],[1,0,1]]
```

**Approach:**
- Use first row and first column as markers.
- Track separately if first row/col had zeros.

**Solution:**
```python
def setZeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_zero = any(matrix[i][0] == 0 for i in range(m))
    
    # Mark zeros in first row/col
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    
    # Set cells to zero
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0
    
    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0
```

**Complexity:** Time O(m*n), Space O(1)

---

### Problem 8: Word Search

**Problem Statement:**
Given a 2D grid of characters and a word, return True if the word exists in the grid. The word can be constructed from letters of sequentially adjacent cells (horizontally or vertically). Same cell cannot be reused.

```
Visual: DFS Backtracking for Word Search

Board:                    Word: "ABCCED"
┌───┬───┬───┬───┐
│ A │ B │ C │ E │         Search path for "ABCCED":
├───┼───┼───┼───┤
│ S │ F │ C │ S │         ┌───┬───┬───┬───┐
├───┼───┼───┼───┤         │ A │→B│→C│   │
│ A │ D │ E │ E │         ├───┼───┼───┼───┤
└───┴───┴───┴───┘         │   │   │↓C│   │
                          ├───┼───┼───┼───┤
Starting from (0,0)='A':  │   │   │→E│→D│→E│
                          └───┴───┴───┴───┘
                          Path: A→B→C→C→E→D→E? No!
                          
Actually the path is:
  A(0,0) → B(0,1) → C(0,2) → C(1,2) → E(2,2) → D(2,1)
  That's only 6 chars, but "ABCCED" is 6 chars! ✓
  
  Let me recount: A-B-C-C-E-D = 6 chars ✓

DFS explores 4 directions from each cell:
  ┌───┬───┬───┐
  │   │ ↑ │   │    From current cell, try:
  ├───┼───┼───┤    UP, DOWN, LEFT, RIGHT
  │ ← │ X │ → │    (if within bounds, matches next char,
  ├───┼───┼───┤     and hasn't been visited)
  │   │ ↓ │   │
  └───┴───┴───┘
  
  Mark visited: change cell to '#'
  After exploring: restore cell (backtrack)
```

```
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
Output: True
```

**Approach:**
- DFS + backtracking from each cell that matches the first character.
- Mark visited cells temporarily, restore after exploring.

**Solution:**
```python
def exist(board, word):
    if not board or not word:
        return False
    
    m, n = len(board), len(board[0])
    
    def dfs(i, j, k):
        if k == len(word):
            return True
        if i < 0 or i >= m or j < 0 or j >= n:
            return False
        if board[i][j] != word[k]:
            return False
        
        temp = board[i][j]
        board[i][j] = '#'  # mark visited
        
        found = (dfs(i + 1, j, k + 1) or
                 dfs(i - 1, j, k + 1) or
                 dfs(i, j + 1, k + 1) or
                 dfs(i, j - 1, k + 1))
        
        board[i][j] = temp  # restore
        return found
    
    for i in range(m):
        for j in range(n):
            if dfs(i, j, 0):
                return True
    return False
```

**Complexity:** Time O(m*n * 4^L) where L is word length, Space O(L)

---

### Problem 9: Pascal's Triangle

**Problem Statement:**
Given an integer `numRows`, generate the first numRows of Pascal's triangle.

```
Input: numRows = 5
Output: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]
```

**Approach:**
- Each element is the sum of the two elements directly above it.

**Solution:**
```python
def generate(numRows):
    triangle = []
    for i in range(numRows):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)
    return triangle
```

**Complexity:** Time O(n²), Space O(n²) (excluding output)

---

## HARD

---

### Problem 10: Sudoku Solver

**Problem Statement:**
Write a program to solve a Sudoku puzzle by filling the empty cells. A valid Sudoku has a unique solution.

```
Visual: Sudoku Constraints

A valid Sudoku requires:
  1. Each ROW contains 1-9 exactly once
  2. Each COLUMN contains 1-9 exactly once
  3. Each 3×3 BOX contains 1-9 exactly once

  ┌───────┬───────┬───────┐
  │       │       │       │
  │  Box  │  Box  │  Box  │
  │   0   │   1   │   2   │    9 boxes labeled 0-8
  │       │       │       │
  ├───────┼───────┼───────┤
  │       │       │       │
  │  Box  │  Box  │  Box  │
  │   3   │   4   │   5   │    Box index = (row//3)*3 + col//3
  │       │       │       │
  ├───────┼───────┼───────┤
  │       │       │       │
  │  Box  │  Box  │  Box  │
  │   6   │   7   │   8   │
  │       │       │       │
  └───────┴───────┴───────┘

Backtracking approach:
  1. Find next empty cell (marked with '.')
  2. Try digits 1-9
  3. For each digit, check:
     • Not in the same row
     • Not in the same column  
     • Not in the same 3×3 box
  4. If valid, place it and recurse
  5. If no digit works, backtrack (restore '.')

Visual recursion:
  Try '1' at (0,2):
    ├─ Valid? Check row 0, col 2, box 0
    ├─ YES: Place '1', recurse to next empty
    │   ├─ Try '1' at next cell... eventually fails
    │   ├─ Backtrack, try '2'...
    │   └─ If all 9 digits fail → backtrack to parent
    └─ NO: Try next digit

Optimization: Use sets to track used digits per row/col/box
  for O(1) validity checking instead of O(9) scan
```

```
Input: (partially filled 9x9 grid with '.' for empty cells)
Output: (completed valid grid)
```

**Approach:**
- Backtracking: try digits 1-9 in each empty cell, check validity, recurse.

**Solution:**
```python
def solveSudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []
    
    for i in range(9):
        for j in range(9):
            if board[i][j] != '.':
                num = int(board[i][j])
                rows[i].add(num)
                cols[j].add(num)
                boxes[(i // 3) * 3 + j // 3].add(num)
            else:
                empty.append((i, j))
    
    def solve(idx):
        if idx == len(empty):
            return True
        
        row, col = empty[idx]
        box_idx = (row // 3) * 3 + col // 3
        
        for num in range(1, 10):
            if num not in rows[row] and num not in cols[col] and num not in boxes[box_idx]:
                board[row][col] = str(num)
                rows[row].add(num)
                cols[col].add(num)
                boxes[box_idx].add(num)
                
                if solve(idx + 1):
                    return True
                
                board[row][col] = '.'
                rows[row].remove(num)
                cols[col].remove(num)
                boxes[box_idx].remove(num)
        
        return False
    
    solve(0)
    return board
```

**Complexity:** Time O(9^(empty cells)), Space O(empty cells)

---

### Problem 11: Median in Row-Sorted Matrix

**Problem Statement:**
Given an m x n matrix where each row is sorted in ascending order, find the median of the matrix.

```
Visual: Binary Search on Answer

Matrix:
  ┌───┬───┬───┐
  │ 1 │ 3 │ 5 │    Rows are sorted
  ├───┼───┼───┤    Total elements = 3×3 = 9
  │ 2 │ 6 │ 9 │    Median is the 5th smallest element
  ├───┼───┼───┤    (position = (9+1)//2 = 5)
  │ 3 │ 6 │ 9 │
  └───┴───┴───┘

Binary search on the VALUE range:
  low = min(matrix) = 1
  high = max(matrix) = 9
  
  For each candidate mid, count elements ≤ mid:
  
  mid = 5:   Count elements ≤ 5
    Row 1: [1,3,5] → 3 elements ≤ 5 (bisect_right gives index 3)
    Row 2: [2,6,9] → 1 element ≤ 5
    Row 3: [3,6,9] → 1 element ≤ 5
    Total = 5 ≥ 5 (target) → high = 5
    
  mid = 3:   Count elements ≤ 3
    Row 1: [1,3,5] → 2 elements ≤ 3
    Row 2: [2,6,9] → 1 element ≤ 3
    Row 3: [3,6,9] → 1 element ≤ 3
    Total = 4 < 5 → low = 4
    
  mid = 4:   Count elements ≤ 4
    Row 1: [1,3,5] → 2 elements ≤ 4
    Row 2: [2,6,9] → 1 element ≤ 4
    Row 3: [3,6,9] → 1 element ≤ 4
    Total = 4 < 5 → low = 5
    
  low == high == 5 → Answer is 5 ✓
  
  Verification: Sorted all elements = [1,2,3,3,5,6,6,9,9]
  5th element = 5 ✓
```

```
Input: matrix = [[1,3,5],[2,6,9],[3,6,9]]
Output: 5
```

**Approach:**
- Binary search on the answer (value range from min to max in matrix).
- For each candidate, count elements <= using binary search in each row.

**Solution:**
```python
import bisect

def medianMatrix(matrix):
    low = min(row[0] for row in matrix)
    high = max(row[-1] for row in matrix)
    m, n = len(matrix), len(matrix[0])
    target = (m * n + 1) // 2
    
    while low < high:
        mid = (low + high) // 2
        count = sum(bisect.bisect_right(row, mid) for row in matrix)
        if count < target:
            low = mid + 1
        else:
            high = mid
    
    return low
```

**Complexity:** Time O(m * log n * log(max_val - min_val)), Space O(1)

---

### Problem 12: Search in 2D Matrix II

**Problem Statement:**
Write an efficient algorithm that searches for a value in an m x n matrix where:
- Each row is sorted left to right
- Each column is sorted top to bottom

```
Visual: Top-Right Corner Search Strategy

Matrix with target = 5:
  ┌────┬────┬────┬────┬────┐
  │  1 │  4 │  7 │ 11 │ 15 │  ← Row 0 sorted →
  ├────┼────┼────┼────┼────┤
  │  2 │  5 │  8 │ 12 │ 19 │  ← Row 1 sorted →
  ├────┼────┼────┼────┼────┤
  │  3 │  6 │  9 │ 16 │ 22 │  ← Row 2 sorted →
  └────┴────┴────┴────┴────┘
       ↑    ↑    ↑    ↑    ↑
     Col sorted top to bottom

Start at top-right corner: matrix[0][4] = 15

Step 1: 15 > 5 → move LEFT (eliminate column 4)
  ┌────┬────┬────┬────┐
  │  1 │  4 │  7 │ 11 │
  ├────┼────┼────┼────┤
  │  2 │  5 │  8 │ 12 │
  ├────┼────┼────┼────┤
  │  3 │  6 │  9 │ 16 │
  └────┴────┴────┴────┘

Step 2: 11 > 5 → move LEFT (eliminate column 3)
  ┌────┬────┬────┐
  │  1 │  4 │  7 │
  ├────┼────┼────┤
  │  2 │  5 │  8 │
  ├────┼────┼────┤
  │  3 │  6 │  9 │
  └────┴────┴────┘

Step 3: 7 > 5 → move LEFT (eliminate column 2)
  ┌────┬────┐
  │  1 │  4 │
  ├────┼────┤
  │  2 │  5 │  ← Found it!
  ├────┼────┤
  │  3 │  6 │
  └────┴────┘

Step 4: 4 < 5 → move DOWN (eliminate row 0)
  Target found at (1,1)! ✓

Why this works:
  • If current > target: everything below is also > target (col sorted)
    → eliminate column (move left)
  • If current < target: everything left is also < target (row sorted)
    → eliminate row (move down)
  • At each step, we eliminate either a row or a column → O(m+n)
```

```
Input: matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22]], target = 5
Output: True
```

**Approach:**
- Start from top-right corner.
- If current == target: found
- If current > target: move left
- If current < target: move down

**Solution:**
```python
def searchMatrix(matrix, target):
    if not matrix:
        return False
    
    m, n = len(matrix), len(matrix[0])
    r, c = 0, n - 1  # top-right corner
    
    while r < m and c >= 0:
        if matrix[r][c] == target:
            return True
        elif matrix[r][c] > target:
            c -= 1
        else:
            r += 1
    
    return False
```

**Complexity:** Time O(m + n), Space O(1)

---

## Problem Summary Table

| # | Problem | Difficulty | Key Technique | Time | Space | Key Insight |
|---|---------|------------|---------------|------|-------|-------------|
| 1 | Transpose Matrix | Easy | Index swap | O(m*n) | O(m*n) | result[j][i] = matrix[i][j] |
| 2 | Reshape Matrix | Easy | Flatten + reshape | O(m*n) | O(m*n) | Check r*c == m*n first |
| 3 | Flipping Image | Easy | Two pointers | O(n²) | O(1) | Swap + flip simultaneously |
| 4 | Toeplitz Matrix | Easy | Diagonal check | O(m*n) | O(1) | matrix[i][j] == matrix[i+1][j+1] |
| 5 | Spiral Matrix | Medium | Boundary simulation | O(m*n) | O(1) | Maintain 4 boundaries |
| 6 | Rotate Image | Medium | Transpose + reverse | O(n²) | O(1) | Two clean steps |
| 7 | Set Matrix Zeroes | Medium | First row/col markers | O(m*n) | O(1) | Use matrix itself as storage |
| 8 | Word Search | Medium | DFS + backtracking | O(m*n*4^L) | O(L) | Mark visited, restore on backtrack |
| 9 | Pascal's Triangle | Medium | Iterative | O(n²) | O(n²) | Each cell = sum of two above |
| 10 | Sudoku Solver | Hard | Backtracking + sets | O(9^e) | O(e) | Sets for O(1) constraint check |
| 11 | Median Row-Sorted | Hard | Binary search on answer | O(m*logn*logV) | O(1) | Count elements ≤ mid |
| 12 | Search 2D Matrix II | Hard | Top-right traversal | O(m+n) | O(1) | Eliminate row or column each step |

### Quick Pattern Recognition

```
See these keywords? Use these techniques:

"transpose"         → Swap matrix[i][j] with matrix[j][i]
"rotate 90°"        → Transpose + Reverse rows
"spiral"            → 4 boundaries (top, bottom, left, right)
"set zeroes"        → First row/col as markers
"search in sorted"  → Top-right corner walk
"search sorted row" → Binary search on value range
"word search"       → DFS + backtracking
"sudoku"            → Backtracking + constraint sets
"median in matrix"  → Binary search on answer
"diagonal"          → Check matrix[i][j] vs matrix[i+1][j+1]
```
