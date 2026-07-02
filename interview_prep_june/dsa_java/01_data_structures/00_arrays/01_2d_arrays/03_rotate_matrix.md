# Rotate Matrix

## Rotate by 90 Degrees Clockwise

**Problem:** Rotate an N×N matrix 90° clockwise. Must be in-place for the square case.

### Method 1: Transpose + Reverse Rows (Most intuitive)

```java
public static void rotate90(int[][] matrix) {
    int n = matrix.length;
    // Transpose: swap matrix[i][j] with matrix[j][i]
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int temp = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = temp;
        }
    }
    // Reverse each row
    for (int i = 0; i < n; i++) {
        int left = 0, right = n - 1;
        while (left < right) {
            int temp = matrix[i][left];
            matrix[i][left] = matrix[i][right];
            matrix[i][right] = temp;
            left++;
            right--;
        }
    }
}
```

### Method 2: Four-way Swap (Single Pass, In-place)

```java
public static void rotate90InPlace(int[][] matrix) {
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

**How the four-way swap works:** Each element participates in a cycle of 4. The element at `(i, j)` moves to `(j, n-1-i)`, which moves to `(n-1-i, n-1-j)`, which moves to `(n-1-j, i)`, which returns to `(i, j)`.

The loops cover only the top-left quadrant (excluding the center element for odd n). Each iteration rotates 4 elements simultaneously.

For n=4, the elements processed are:
```
Layer 0 (i=0): j=0,1,2  →  (4-1)=3, so j goes 0,1,2
Layer 1 (i=1): j=1,2    →  (n-1-i)=2, so j goes 1 only
```

## Rotate by 90 Degrees Anticlockwise

### Transpose + Reverse Columns

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
        int top = 0, bottom = n - 1;
        while (top < bottom) {
            int temp = matrix[top][j];
            matrix[top][j] = matrix[bottom][j];
            matrix[bottom][j] = temp;
            top++;
            bottom--;
        }
    }
}
```

### Alternative: Reverse rows first, then transpose

```java
public static void rotate90AnticlockwiseAlt(int[][] matrix) {
    int n = matrix.length;
    // Reverse rows
    for (int i = 0; i < n; i++) {
        int left = 0, right = n - 1;
        while (left < right) {
            int temp = matrix[i][left];
            matrix[i][left] = matrix[i][right];
            matrix[i][right] = temp;
            left++;
            right--;
        }
    }
    // Transpose
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int temp = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = temp;
        }
    }
}
```

## Rotate by 180 Degrees

**Method:** Reverse rows, then reverse each row (or rotate 90° twice).

```java
public static void rotate180(int[][] matrix) {
    int n = matrix.length;
    // Reverse order of rows
    int top = 0, bottom = n - 1;
    while (top < bottom) {
        int[] temp = matrix[top];
        matrix[top] = matrix[bottom];
        matrix[bottom] = temp;
        top++;
        bottom--;
    }
    // Reverse each row
    for (int i = 0; i < n; i++) {
        int left = 0, right = n - 1;
        while (left < right) {
            int temp = matrix[i][left];
            matrix[i][left] = matrix[i][right];
            matrix[i][right] = temp;
            left++;
            right--;
        }
    }
}
```

Or simply: `rotate90(matrix); rotate90(matrix);` — but that's 2 passes instead of 1.

## Rotate by 270 Degrees Clockwise (= 90° Anticlockwise)

Rotate 90° three times, or rotate 90° anticlockwise.

## Ring-by-Ring Rotation

An alternative layer-by-layer approach:

```java
public static void rotateRingByRing(int[][] matrix) {
    int n = matrix.length;
    for (int layer = 0; layer < n / 2; layer++) {
        int first = layer;
        int last = n - 1 - layer;
        for (int i = first; i < last; i++) {
            int offset = i - first;
            int top = matrix[first][i];

            // left -> top
            matrix[first][i] = matrix[last - offset][first];
            // bottom -> left
            matrix[last - offset][first] = matrix[last][last - offset];
            // right -> bottom
            matrix[last][last - offset] = matrix[i][last];
            // top -> right
            matrix[i][last] = top;
        }
    }
}
```

## Summary: Rotation Cheatsheet

| Rotation | Method | 
|----------|--------|
| 90° clockwise | Transpose + reverse each row |
| 90° anticlockwise | Transpose + reverse each column |
| 180° | Reverse rows + reverse each row |
| 270° clockwise | 90° clockwise × 3 (or anticlockwise once) |

Alternatively (non-in-place, for non-square matrices):

| Rotation | New Matrix Dimensions |
|----------|----------------------|
| 90° clockwise | `result[j][n-1-i] = matrix[i][j]` |
| 90° anticlockwise | `result[n-1-j][i] = matrix[i][j]` |
| 180° | `result[n-1-i][n-1-j] = matrix[i][j]` |

```java
public static int[][] rotate90NewMatrix(int[][] matrix) {
    int rows = matrix.length, cols = matrix[0].length;
    int[][] result = new int[cols][rows];
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            result[j][rows - 1 - i] = matrix[i][j];
        }
    }
    return result;
}
```

## Practice Problems

| Problem | LeetCode | Description |
|---------|----------|-------------|
| Rotate Image | 48 | 90° clockwise in-place |
| Determine Whether Matrix Can Be Obtained By Rotation | 1886 | Check if rotation matches |
| Rotating the Box | 1861 | 90° + gravity |

## Complexity

| Operation | Time | Space (in-place) |
|-----------|------|------------------|
| 90° (transpose + reverse) | O(n²) | O(1) |
| 90° (4-way swap) | O(n²) | O(1) |
| 180° | O(n²) | O(1) |
| New matrix rotation | O(m×n) | O(m×n) |
