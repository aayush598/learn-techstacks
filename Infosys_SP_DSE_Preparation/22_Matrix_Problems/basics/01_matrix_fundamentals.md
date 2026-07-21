# Matrix Fundamentals - Python Implementation

## 1. Matrix Creation in Python (List of Lists)

```python
# Creating a matrix using list of lists
rows, cols = 3, 4

# Method 1: Nested list comprehension
matrix = [[0] * cols for _ in range(rows)]
# [[0, 0, 0, 0],
#  [0, 0, 0, 0],
#  [0, 0, 0, 0]]

# Method 2: Initialize with values
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]

# Method 3: Using numpy (if allowed)
import numpy as np
np_matrix = np.zeros((3, 4), dtype=int)
np_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Method 4: Create matrix from input
def create_matrix_from_input():
    rows, cols = map(int, input().split())
    matrix = []
    for i in range(rows):
        row = list(map(int, input().split()))
        matrix.append(row)
    return matrix

# Method 5: Identity matrix
n = 4
identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

# Method 6: Diagonal matrix
diagonal_values = [1, 2, 3, 4]
n = len(diagonal_values)
diag_matrix = [[diagonal_values[i] if i == j else 0 for j in range(n)] for i in range(n)]

# Print matrix nicely
def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))
```

---

## 2. Matrix Traversal (Row-Major, Column-Major)

```python
# Row-Major Traversal (left to right, top to bottom)
def row_major_traversal(matrix):
    result = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            result.append(matrix[i][j])
    return result

# Column-Major Traversal (top to bottom, left to right)
def column_major_traversal(matrix):
    result = []
    rows, cols = len(matrix), len(matrix[0])
    for j in range(cols):
        for i in range(rows):
            result.append(matrix[i][j])
    return result

# Example
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(row_major_traversal(matrix))      # [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(column_major_traversal(matrix))   # [1, 4, 7, 2, 5, 8, 3, 6, 9]
```

---

## 3. Spiral Order Traversal

```python
def spiral_order(matrix):
    if not matrix:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # Traverse right along top row
        for j in range(left, right + 1):
            result.append(matrix[top][j])
        top += 1
        
        # Traverse down along right column
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        
        # Traverse left along bottom row
        if top <= bottom:
            for j in range(right, left - 1, -1):
                result.append(matrix[bottom][j])
            bottom -= 1
        
        # Traverse up along left column
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    
    return result

# Example
matrix = [
    [1,  2,  3,  4],
    [5,  6,  7,  8],
    [9, 10, 11, 12]
]
print(spiral_order(matrix))
# Output: [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
```

---

## 4. Rotate Matrix 90 Degrees Clockwise (In-Place)

```python
def rotate_90_clockwise(matrix):
    """Rotate NxN matrix 90 degrees clockwise in-place.
    
    Algorithm: Transpose then reverse each row.
    Step 1: Transpose (swap matrix[i][j] with matrix[j][i])
    Step 2: Reverse each row
    """
    n = len(matrix)
    
    # Step 1: Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Step 2: Reverse each row
    for i in range(n):
        matrix[i].reverse()
    
    return matrix

# Example
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
rotate_90_clockwise(matrix)
# Result:
# [7, 4, 1]
# [8, 5, 2]
# [9, 6, 3]
```

---

## 5. Rotate Matrix 90 Degrees Counter-Clockwise

```python
def rotate_90_counter_clockwise(matrix):
    """Rotate NxN matrix 90 degrees counter-clockwise in-place.
    
    Algorithm: Transpose then reverse each column.
    Step 1: Transpose (swap matrix[i][j] with matrix[j][i])
    Step 2: Reverse each column
    """
    n = len(matrix)
    
    # Step 1: Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Step 2: Reverse each column
    for j in range(n):
        for i in range(n // 2):
            matrix[i][j], matrix[n - 1 - i][j] = matrix[n - 1 - i][j], matrix[i][j]
    
    return matrix

# Example
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
rotate_90_counter_clockwise(matrix)
# Result:
# [3, 6, 9]
# [2, 5, 8]
# [1, 4, 7]

# Alternative: Reverse rows then transpose
def rotate_90_ccw_v2(matrix):
    n = len(matrix)
    matrix.reverse()
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    return matrix
```

---

## 6. Transpose of Matrix

```python
# For NxN matrix (in-place)
def transpose_square(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    return matrix

# For MxN matrix (creates new matrix)
def transpose(matrix):
    rows, cols = len(matrix), len(matrix[0])
    result = [[0] * rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]
    return result

# Using zip
def transpose_pythonic(matrix):
    return [list(row) for row in zip(*matrix)]

# Example
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]
print(transpose(matrix))
# [[1, 4], [2, 5], [3, 6]]
```

---

## 7. Set Matrix Zeros (In-Place)

```python
def set_zeroes(matrix):
    """If an element is 0, set its entire row and column to 0.
    Uses first row and first column as markers (O(1) extra space).
    """
    m, n = len(matrix), len(matrix[0])
    first_row_zero = False
    first_col_zero = False
    
    # Check if first row has zero
    for j in range(n):
        if matrix[0][j] == 0:
            first_row_zero = True
            break
    
    # Check if first column has zero
    for i in range(m):
        if matrix[i][0] == 0:
            first_col_zero = True
            break
    
    # Use first row and column as markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    
    # Set cells to zero based on markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    
    # Handle first row
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0
    
    # Handle first column
    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0
    
    return matrix

# Example
matrix = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]
set_zeroes(matrix)
# Result:
# [1, 0, 1]
# [0, 0, 0]
# [1, 0, 1]
```

---

## 8. Search in Row-Sorted and Column-Sorted Matrix

```python
def search_sorted_matrix(matrix, target):
    """Search in a matrix where:
    - Each row is sorted left to right
    - Each column is sorted top to bottom
    Start from top-right corner.
    Time: O(m + n)
    """
    if not matrix:
        return False
    
    rows, cols = len(matrix), len(matrix[0])
    r, c = 0, cols - 1  # Start at top-right
    
    while r < rows and c >= 0:
        if matrix[r][c] == target:
            return (r, c)
        elif matrix[r][c] > target:
            c -= 1  # Move left
        else:
            r += 1  # Move down
    
    return (-1, -1)

# Example
matrix = [
    [10, 20, 30, 40],
    [15, 25, 35, 45],
    [27, 29, 37, 48],
    [32, 33, 39, 50]
]
print(search_sorted_matrix(matrix, 29))  # (2, 1)
print(search_sorted_matrix(matrix, 100)) # (-1, -1)
```

---

## 9. Search in a 2D Matrix (Binary Search)

```python
def search_matrix(matrix, target):
    """Search in a matrix where:
    - Each row's first element is greater than the previous row's last element
    - Rows are sorted, and first element of each row is greater than
      last element of previous row
    Treat matrix as a flat sorted array. Time: O(log(m*n))
    """
    if not matrix:
        return False
    
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        # Convert 1D index to 2D coordinates
        row, col = mid // n, mid % n
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    
    return False

# Alternative: Row-wise binary search
def search_matrix_rowwise(matrix, target):
    """Each row sorted, first element of row > last element of prev row."""
    for row in matrix:
        if row[0] <= target <= row[-1]:
            # Binary search in this row
            lo, hi = 0, len(row) - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if row[mid] == target:
                    return True
                elif row[mid] < target:
                    lo = mid + 1
                else:
                    hi = mid - 1
    return False

# Example
matrix = [
    [1,  3,  5,  7],
    [10, 11, 16, 20],
    [23, 30, 34, 60]
]
print(search_matrix(matrix, 3))   # True
print(search_matrix(matrix, 13))  # False
```

---

## 10. Matrix Diagonal Traversal

```python
def diagonal_traversal(matrix):
    """Traverse matrix in diagonal order (top-right to bottom-left diagonals).
    
    Diagonal 0: (0,0)
    Diagonal 1: (0,1), (1,0)
    Diagonal 2: (0,2), (1,1), (2,0)
    Diagonal 3: (1,2), (2,1)
    Diagonal 4: (2,2)
    """
    if not matrix:
        return []
    
    m, n = len(matrix), len(matrix[0])
    result = []
    
    for d in range(m + n - 1):
        # Collect elements in this diagonal
        diagonal = []
        r = 0 if d < n else d - n + 1
        c = d if d < n else n - 1
        
        while r < m and c >= 0:
            diagonal.append(matrix[r][c])
            r += 1
            c -= 1
        
        result.append(diagonal)
    
    return result

# Example
matrix = [
    [1,  2,  3],
    [4,  5,  6],
    [7,  8,  9]
]
print(diagonal_traversal(matrix))
# [[1], [4, 2], [7, 5, 3], [8, 6], [9]]
```

---

## 11. Zigzag Diagonal Traversal

```python
def zigzag_diagonal_traversal(matrix):
    """Traverse matrix diagonally in zigzag pattern.
    
    Diagonal 0 (upward): (0,0)
    Diagonal 1 (downward): (0,1), (1,0)
    Diagonal 2 (upward): (2,0), (1,1), (0,2)
    Diagonal 3 (downward): (1,2), (2,1)
    Diagonal 4 (upward): (2,2)
    """
    if not matrix:
        return []
    
    m, n = len(matrix), len(matrix[0])
    result = []
    
    for d in range(m + n - 1):
        diagonal = []
        r = 0 if d < n else d - n + 1
        c = d if d < n else n - 1
        
        while r < m and c >= 0:
            diagonal.append(matrix[r][c])
            r += 1
            c -= 1
        
        # Reverse for even diagonals (upward direction)
        if d % 2 == 0:
            result.extend(diagonal[::-1])
        else:
            result.extend(diagonal)
    
    return result

# Example
matrix = [
    [1,  2,  3],
    [4,  5,  6],
    [7,  8,  9]
]
print(zigzag_diagonal_traversal(matrix))
# [1, 2, 4, 7, 5, 3, 6, 8, 9]

# LeetCode style: return flat list
def find_diagonal_order(matrix):
    if not matrix:
        return []
    
    m, n = len(matrix), len(matrix[0])
    result = []
    
    for d in range(m + n - 1):
        diagonal = []
        r = 0 if d < n else d - n + 1
        c = d if d < n else n - 1
        
        while r < m and c >= 0:
            diagonal.append(matrix[r][c])
            r += 1
            c -= 1
        
        if d % 2 == 0:
            result.extend(diagonal[::-1])
        else:
            result.extend(diagonal)
    
    return result
```

---

## Quick Reference Cheat Sheet

| Operation | Time | Space |
|-----------|------|-------|
| Create NxN | O(n²) | O(n²) |
| Row-Major Traverse | O(m*n) | O(1) |
| Column-Major Traverse | O(m*n) | O(1) |
| Spiral Order | O(m*n) | O(1) |
| Rotate 90° CW (in-place) | O(n²) | O(1) |
| Rotate 90° CCW (in-place) | O(n²) | O(1) |
| Transpose (NxN) | O(n²) | O(1) |
| Set Matrix Zeroes | O(m*n) | O(1) |
| Search (sorted rows/cols) | O(m+n) | O(1) |
| Search (binary search) | O(log(m*n)) | O(1) |
| Diagonal Traversal | O(m*n) | O(m*n) |
| Zigzag Diagonal | O(m*n) | O(m*n) |
