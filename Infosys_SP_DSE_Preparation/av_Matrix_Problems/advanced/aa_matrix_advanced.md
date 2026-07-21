# Matrix Advanced Problems - Python Implementation

## 1. Multiply Two Matrices

```python
def multiply_matrices(A, B):
    """Multiply matrix A (m x n) with matrix B (n x p).
    Result is matrix C (m x p).
    Time: O(m * n * p)
    """
    m, n = len(A), len(A[0])
    n2, p = len(B), len(B[0])
    
    if n != n2:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    
    # Initialize result matrix with zeros
    C = [[0] * p for _ in range(m)]
    
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    
    return C

# Strassen's Algorithm (faster for large matrices, O(n^2.807))
def add_matrices(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def subtract_matrices(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def strassen_multiply(A, B):
    """Strassen's algorithm for square matrices (n x n, n is power of 2)."""
    n = len(A)
    
    if n <= 2:
        return multiply_matrices(A, B)
    
    mid = n // 2
    
    # Divide matrices into quadrants
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]
    
    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]
    
    # 7 Strassen products
    M1 = strassen_multiply(add_matrices(A11, A22), add_matrices(B11, B22))
    M2 = strassen_multiply(add_matrices(A21, A22), B11)
    M3 = strassen_multiply(A11, subtract_matrices(B12, B22))
    M4 = strassen_multiply(A22, subtract_matrices(B21, B11))
    M5 = strassen_multiply(add_matrices(A11, A12), B22)
    M6 = strassen_multiply(subtract_matrices(A21, A11), add_matrices(B11, B12))
    M7 = strassen_multiply(subtract_matrices(A12, A22), add_matrices(B21, B22))
    
    # Combine results
    C11 = add_matrices(subtract_matrices(add_matrices(M1, M4), M5), M7)
    C12 = add_matrices(M3, M5)
    C21 = add_matrices(M2, M4)
    C22 = add_matrices(subtract_matrices(add_matrices(M1, M3), M2), M6)
    
    # Merge quadrants
    C = [[0] * n for _ in range(n)]
    for i in range(mid):
        for j in range(mid):
            C[i][j] = C11[i][j]
            C[i][j + mid] = C12[i][j]
            C[i + mid][j] = C21[i][j]
            C[i + mid][j + mid] = C22[i][j]
    
    return C

# Example
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
print(multiply_matrices(A, B))
# [[19, 22], [43, 50]]
```

---

## 2. Rotate Image by 90 Degrees (4 Ways)

```python
def rotate_90_cw_transpose_reverse(matrix):
    """90° Clockwise: Transpose then reverse each row."""
    n = len(matrix)
    # Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Reverse each row
    for i in range(n):
        matrix[i].reverse()
    return matrix

def rotate_90_cw_layer_by_layer(matrix):
    """90° Clockwise: Rotate layer by layer (onion layers)."""
    n = len(matrix)
    for layer in range(n // 2):
        first, last = layer, n - 1 - layer
        for i in range(first, last):
            offset = i - first
            # Save top
            top = matrix[first][i]
            # Left -> Top
            matrix[first][i] = matrix[last - offset][first]
            # Bottom -> Left
            matrix[last - offset][first] = matrix[last][last - offset]
            # Right -> Bottom
            matrix[last][last - offset] = matrix[i][last]
            # Top -> Right
            matrix[i][last] = top
    return matrix

def rotate_90_ccw_transpose_reverse(matrix):
    """90° Counter-clockwise: Reverse each row then transpose."""
    n = len(matrix)
    # Reverse each row
    for i in range(n):
        matrix[i].reverse()
    # Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    return matrix

def rotate_180(matrix):
    """180° rotation: Reverse each row then reverse the order of rows."""
    n = len(matrix)
    matrix.reverse()
    for i in range(n):
        matrix[i].reverse()
    return matrix

# Example
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(rotate_90_cw_transpose_reverse([row[:] for row in matrix]))
# [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

print(rotate_90_ccw_transpose_reverse([row[:] for row in matrix]))
# [[3, 6, 9], [2, 5, 8], [1, 4, 7]]

print(rotate_180([row[:] for row in matrix]))
# [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
```

---

## 3. Spiral Matrix II (Generate Matrix)

```python
def generate_matrix(n):
    """Generate an n x n matrix filled with numbers 1 to n² in spiral order."""
    matrix = [[0] * n for _ in range(n)]
    top, bottom = 0, n - 1
    left, right = 0, n - 1
    num = 1
    
    while top <= bottom and left <= right:
        # Fill top row (left to right)
        for j in range(left, right + 1):
            matrix[top][j] = num
            num += 1
        top += 1
        
        # Fill right column (top to bottom)
        for i in range(top, bottom + 1):
            matrix[i][right] = num
            num += 1
        right -= 1
        
        # Fill bottom row (right to left)
        if top <= bottom:
            for j in range(right, left - 1, -1):
                matrix[bottom][j] = num
                num += 1
            bottom -= 1
        
        # Fill left column (bottom to top)
        if left <= right:
            for i in range(bottom, top - 1, -1):
                matrix[i][left] = num
                num += 1
            left += 1
    
    return matrix

# Example
print(generate_matrix(3))
# [[1, 2, 3],
#  [8, 9, 4],
#  [7, 6, 5]]

print(generate_matrix(4))
# [[ 1,  2,  3,  4],
#  [12, 13, 14,  5],
#  [11, 16, 15,  6],
#  [10,  9,  8,  7]]
```

---

## 4. Pascal's Triangle

```python
def pascals_triangle(num_rows):
    """Generate first num_rows of Pascal's triangle."""
    triangle = []
    for i in range(num_rows):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)
    return triangle

# Print Pascal's triangle
def print_pascal(num_rows):
    triangle = pascals_triangle(num_rows)
    max_width = len(" ".join(map(str, triangle[-1])))
    for row in triangle:
        row_str = " ".join(map(str, row))
        print(row_str.center(max_width))

# Get specific row (0-indexed) - O(k) space
def get_pascal_row(row_index):
    result = [1]
    for i in range(1, row_index + 1):
        result.append(result[i - 1] * (row_index - i + 1) // i)
    return result

# Get element at (row, col) - O(min(row, col)) time
def pascal_element(row, col):
    if col > row - col:
        col = row - col
    result = 1
    for i in range(col):
        result = result * (row - i) // (i + 1)
    return result

# Example
print_pascal(6)
#            1
#          1   1
#        1   2   1
#      1   3   3   1
#    1   4   6   4   1
#  1   5  10  10   5   1

print(get_pascal_row(5))  # [1, 5, 10, 10, 5, 1]
print(pascal_element(5, 2))  # 10
```

---

## 5. Game of Life

```python
def game_of_life(board):
    """In-place simulation of Conway's Game of Life.
    
    Rules:
    1. Live cell with < 2 live neighbors dies (underpopulation)
    2. Live cell with 2 or 3 live neighbors survives
    3. Live cell with > 3 live neighbors dies (overpopulation)
    4. Dead cell with exactly 3 live neighbors becomes live (reproduction)
    
    Uses encoding: 0->0, 1->1, 0->2 (dead->alive), 1->3 (alive->dead)
    """
    if not board or not board[0]:
        return
    
    m, n = len(board), len(board[0])
    
    def count_neighbors(r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    # Count only cells that were originally alive
                    if board[nr][nc] in (1, 3):
                        count += 1
        return count
    
    # Step 1: Mark cells that will change state
    for i in range(m):
        for j in range(n):
            neighbors = count_neighbors(i, j)
            if board[i][j] == 1:
                if neighbors < 2 or neighbors > 3:
                    board[i][j] = 3  # alive -> dead
            else:
                if neighbors == 3:
                    board[i][j] = 2  # dead -> alive
    
    # Step 2: Update to final state
    for i in range(m):
        for j in range(n):
            if board[i][j] == 2:
                board[i][j] = 1
            elif board[i][j] == 3:
                board[i][j] = 0
    
    return board

# Example
board = [
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1],
    [0, 0, 0]
]
game_of_life(board)
# Result:
# [[0, 0, 0],
#  [1, 0, 1],
#  [0, 1, 1],
#  [0, 1, 0]]
```

---

## 6. Valid Sudoku

```python
def is_valid_sudoku(board):
    """Check if a 9x9 Sudoku board is valid (partially filled).
    No duplicate digits in any row, column, or 3x3 box.
    """
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    
    for i in range(9):
        for j in range(9):
            if board[i][j] == '.':
                continue
            
            num = board[i][j]
            box_idx = (i // 3) * 3 + (j // 3)
            
            # Check row
            if num in rows[i]:
                return False
            rows[i].add(num)
            
            # Check column
            if num in cols[j]:
                return False
            cols[j].add(num)
            
            # Check 3x3 box
            if num in boxes[box_idx]:
                return False
            boxes[box_idx].add(num)
    
    return True

# Example
board = [
    ['5', '3', '.', '.', '7', '.', '.', '.', '.'],
    ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
    ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
    ['8', '.', '.', '.', '6', '.', '.', '.', '3'],
    ['4', '.', '.', '8', '.', '3', '.', '.', '1'],
    ['7', '.', '.', '.', '2', '.', '.', '.', '6'],
    ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
    ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
    ['.', '.', '.', '.', '8', '.', '.', '7', '9']
]
print(is_valid_sudoku(board))  # True
```

---

## 7. Sudoku Solver

```python
def solve_sudoku(board):
    """Solve a Sudoku puzzle using backtracking."""
    
    def is_valid(board, row, col, num):
        # Check row
        for j in range(9):
            if board[row][j] == num:
                return False
        
        # Check column
        for i in range(9):
            if board[i][col] == num:
                return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def solve(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    for num in '123456789':
                        if is_valid(board, i, j, num):
                            board[i][j] = num
                            if solve(board):
                                return True
                            board[i][j] = '.'  # backtrack
                    return False  # No valid number found
        return True  # All cells filled
    
    solve(board)
    return board

# Optimized with constraint sets
def solve_sudoku_optimized(board):
    """Optimized Sudoku solver using sets for O(1) constraint checking."""
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []
    
    for i in range(9):
        for j in range(9):
            if board[i][j] != '.':
                num = int(board[i][j])
                box_idx = (i // 3) * 3 + (j // 3)
                rows[i].add(num)
                cols[j].add(num)
                boxes[box_idx].add(num)
            else:
                empty.append((i, j))
    
    def solve(idx):
        if idx == len(empty):
            return True
        
        row, col = empty[idx]
        box_idx = (row // 3) * 3 + (col // 3)
        
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

# Example
board = [
    ['5', '3', '.', '.', '7', '.', '.', '.', '.'],
    ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
    ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
    ['8', '.', '.', '.', '6', '.', '.', '.', '3'],
    ['4', '.', '.', '8', '.', '3', '.', '.', '1'],
    ['7', '.', '.', '.', '2', '.', '.', '.', '6'],
    ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
    ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
    ['.', '.', '.', '.', '8', '.', '.', '7', '9']
]
solve_sudoku(board)
for row in board:
    print(" ".join(row))
```

---

## 8. Smallest Range Covering Elements from K Lists

```python
import heapq

def smallest_range(nums):
    """Find the smallest range [A, B] that contains at least one element
    from each of the K sorted lists.
    
    Approach: Min-heap + tracking max element.
    Start with first element from each list. Pop min, push next from same list.
    Track range each time.
    """
    k = len(nums)
    current_max = float('-inf')
    heap = []
    
    # Initialize heap with first element from each list
    for i in range(k):
        heapq.heappush(heap, (nums[i][0], i, 0))
        current_max = max(current_max, nums[i][0])
    
    best_range = float('inf')
    best_start, best_end = 0, 0
    
    while True:
        val, list_idx, elem_idx = heapq.heappop(heap)
        
        # Update best range
        if current_max - val < best_range:
            best_range = current_max - val
            best_start, best_end = val, current_max
        
        # If any list is exhausted, stop
        if elem_idx + 1 >= len(nums[list_idx]):
            break
        
        # Push next element from the same list
        next_val = nums[list_idx][elem_idx + 1]
        heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
        current_max = max(current_max, next_val)
    
    return [best_start, best_end]

# Example
nums = [[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]
print(smallest_range(nums))  # [20, 24]
```

---

## 9. Median in Row-Wise Sorted Matrix

```python
import bisect

def median_in_row_sorted_matrix(matrix):
    """Find median in a row-wise sorted matrix.
    
    Approach: Binary search on answer.
    For each candidate value, count how many elements are <= it.
    The median is the smallest value where count >= (m*n+1)//2.
    """
    if not matrix or not matrix[0]:
        return -1
    
    m, n = len(matrix), len(matrix[0])
    low = min(row[0] for row in matrix)
    high = max(row[-1] for row in matrix)
    target = (m * n + 1) // 2
    
    def count_less_equal(val):
        """Count elements <= val in the matrix."""
        count = 0
        for row in matrix:
            # Binary search: count elements <= val in this row
            count += bisect.bisect_right(row, val)
        return count
    
    while low < high:
        mid = (low + high) // 2
        if count_less_equal(mid) < target:
            low = mid + 1
        else:
            high = mid
    
    return low

# Alternative: Using min-heap
def median_in_row_sorted_matrix_heap(matrix):
    """Min-heap approach: O(m * log n) space."""
    import heapq
    
    m, n = len(matrix), len(matrix[0])
    heap = []
    
    # Push first element from each row
    for i in range(m):
        heapq.heappush(heap, (matrix[i][0], i, 0))
    
    total = m * n
    target = (total - 1) // 2
    
    for _ in range(target):
        val, row, col = heapq.heappop(heap)
        if col + 1 < n:
            heapq.heappush(heap, (matrix[row][col + 1], row, col + 1))
    
    return heap[0][0]

# Example
matrix = [
    [1, 3, 5],
    [2, 6, 9],
    [3, 6, 9]
]
print(median_in_row_sorted_matrix(matrix))  # 5
```

---

## Quick Reference - Advanced Matrix Techniques

| Problem | Technique | Time | Space |
|---------|-----------|------|-------|
| Matrix Multiplication | Triple loop | O(m*n*p) | O(m*p) |
| Strassen's | Divide & conquer | O(n^2.807) | O(n²) |
| Rotate (4 ways) | Transpose/Reverse | O(n²) | O(1) |
| Spiral Generation | Layer-by-layer | O(n²) | O(n²) |
| Pascal's Triangle | Iterative | O(n²) | O(n) or O(1) |
| Game of Life | State encoding | O(m*n) | O(1) |
| Valid Sudoku | Hash sets | O(1) fixed | O(1) fixed |
| Sudoku Solver | Backtracking | O(9^(empty)) | O(empty) |
| Smallest Range (K lists) | Min-heap | O(N log k) | O(k) |
| Median Row-Sorted | Binary search | O(m * log n * log(max-min)) | O(1) |
