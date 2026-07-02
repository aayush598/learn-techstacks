# Matrix Traversal Patterns

## Row-wise Traversal

Standard nested loop — outer loop over rows, inner over columns.

```java
public static void rowWise(int[][] matrix) {
    for (int i = 0; i < matrix.length; i++) {
        for (int j = 0; j < matrix[i].length; j++) {
            System.out.print(matrix[i][j] + " ");
        }
    }
}
```

## Column-wise Traversal

Outer loop over columns, inner over rows.

```java
public static void columnWise(int[][] matrix) {
    for (int j = 0; j < matrix[0].length; j++) {
        for (int i = 0; i < matrix.length; i++) {
            System.out.print(matrix[i][j] + " ");
        }
    }
}
```

## Boundary Traversal

Walk along the outer perimeter of the matrix.

```java
public static void boundaryTraversal(int[][] matrix) {
    int rows = matrix.length, cols = matrix[0].length;
    if (rows == 1) {
        for (int j = 0; j < cols; j++) System.out.print(matrix[0][j] + " ");
        return;
    }
    if (cols == 1) {
        for (int i = 0; i < rows; i++) System.out.print(matrix[i][0] + " ");
        return;
    }

    // Top row: left to right
    for (int j = 0; j < cols; j++) System.out.print(matrix[0][j] + " ");
    // Right column: top to bottom (skip first, already printed)
    for (int i = 1; i < rows; i++) System.out.print(matrix[i][cols - 1] + " ");
    // Bottom row: right to left (skip last)
    for (int j = cols - 2; j >= 0; j--) System.out.print(matrix[rows - 1][j] + " ");
    // Left column: bottom to top (skip first and last)
    for (int i = rows - 2; i > 0; i--) System.out.print(matrix[i][0] + " ");
}
```

**Edge cases:** Single row, single column. Handle separately to avoid printing the same element twice.

## Diagonal Traversal

### Left-to-right diagonals (\) — same i-j difference

```java
public static void mainDiagonal(int[][] matrix) {
    for (int i = 0; i < matrix.length; i++) {
        System.out.print(matrix[i][i] + " ");
    }
}
```

### All diagonals (top-left to bottom-right)

```java
public static void allDiagonals(int[][] matrix) {
    int rows = matrix.length, cols = matrix[0].length;

    // Starting from first row, moving right
    for (int startCol = 0; startCol < cols; startCol++) {
        int i = 0, j = startCol;
        while (i < rows && j < cols) {
            System.out.print(matrix[i][j] + " ");
            i++;
            j++;
        }
    }

    // Starting from first column (skip (0,0) already done)
    for (int startRow = 1; startRow < rows; startRow++) {
        int i = startRow, j = 0;
        while (i < rows && j < cols) {
            System.out.print(matrix[i][j] + " ");
            i++;
            j++;
        }
    }
}
```

### Anti-diagonals (top-right to bottom-left) — same i+j sum

```java
public static void antiDiagonals(int[][] matrix) {
    int rows = matrix.length, cols = matrix[0].length;

    for (int sum = 0; sum < rows + cols - 1; sum++) {
        int i = Math.min(sum, rows - 1);
        int j = sum - i;
        while (i >= 0 && j < cols) {
            System.out.print(matrix[i][j] + " ");
            i--;
            j++;
        }
    }
}
```

## Zigzag Traversal

Print the first row left-to-right, second row right-to-left, alternating.

```java
public static void zigzagTraversal(int[][] matrix) {
    for (int i = 0; i < matrix.length; i++) {
        if (i % 2 == 0) {
            for (int j = 0; j < matrix[i].length; j++) {
                System.out.print(matrix[i][j] + " ");
            }
        } else {
            for (int j = matrix[i].length - 1; j >= 0; j--) {
                System.out.print(matrix[i][j] + " ");
            }
        }
    }
}
```

## Transpose of a Matrix

### For square matrix (in-place)

```java
public static void transposeSquare(int[][] matrix) {
    int n = matrix.length;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int temp = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = temp;
        }
    }
}
```

**Notice:** j starts at i+1. Swapping `matrix[i][j]` with `matrix[j][i]` only for elements above the main diagonal. If we swapped all elements, we'd swap twice and end up with the original.

### For non-square matrix (new array)

```java
public static int[][] transpose(int[][] matrix) {
    int rows = matrix.length, cols = matrix[0].length;
    int[][] result = new int[cols][rows];
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            result[j][i] = matrix[i][j];
        }
    }
    return result;
}
```

## Rotate Image by 90 Degrees (Clockwise)

**Problem:** Rotate an N×N matrix 90° clockwise in-place.

### Step 1: Transpose
### Step 2: Reverse each row

```java
public static void rotate90Clockwise(int[][] matrix) {
    int n = matrix.length;

    // Transpose
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int temp = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = temp;
        }
    }

    // Reverse each row
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n / 2; j++) {
            int temp = matrix[i][j];
            matrix[i][j] = matrix[i][n - 1 - j];
            matrix[i][n - 1 - j] = temp;
        }
    }
}
```

### Four-way swap (single pass)

```java
public static void rotate90SinglePass(int[][] matrix) {
    int n = matrix.length;
    for (int i = 0; i < n / 2; i++) {
        for (int j = i; j < n - 1 - i; j++) {
            int temp = matrix[i][j];
            matrix[i][j] = matrix[n - 1 - j][i];
            matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j];
            matrix[n - 1 - i][n - 1 - j] = matrix[j][n - 1 - i];
            matrix[j][n - 1 - i] = temp;
        }
    }
}
```

This works in layers. For each element at `(i, j)`, four elements rotate: `(i,j) → (j,n-1-i) → (n-1-i,n-1-j) → (n-1-j,i) → (i,j)`.

### Anticlockwise rotation

Transpose + reverse each column:

```java
public static void rotate90Anticlockwise(int[][] matrix) {
    int n = matrix.length;
    // Transpose
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int temp = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = temp;
        }
    }
    // Reverse each column
    for (int j = 0; j < n; j++) {
        for (int i = 0; i < n / 2; i++) {
            int temp = matrix[i][j];
            matrix[i][j] = matrix[n - 1 - i][j];
            matrix[n - 1 - i][j] = temp;
        }
    }
}
```

## Practice Problems

| Problem | LeetCode | Key Technique |
|---------|----------|---------------|
| Transpose Matrix | 867 | New array or in-place |
| Rotate Image | 48 | Transpose + reverse |
| Diagonal Traverse | 498 | Anti-diagonals |
| Set Matrix Zeroes | 73 | Mark rows/cols with first row/col |
| Toeplitz Matrix | 766 | Check diagonals |
| Reshape the Matrix | 566 | Index mapping |

## Quick Reference

| Operation | Rectangular | Square | In-Place |
|-----------|-------------|--------|----------|
| Row-wise | ✓ | ✓ | n/a |
| Column-wise | ✓ | ✓ | n/a |
| Transpose | New array | ✓ | Only square |
| Rotate 90° | New array | ✓ | ✓ |
| Boundary | ✓ | ✓ | n/a |
| Diagonal | ✓ | ✓ | n/a |
| Zigzag | ✓ | ✓ | n/a |
