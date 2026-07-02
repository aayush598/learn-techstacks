# Spiral Matrix

## Spiral Matrix Traversal

**Problem:** Given an m×n matrix, return all elements in spiral order (clockwise from top-left).

```
Input:
[ [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9] ]

Output: [1, 2, 3, 6, 9, 8, 7, 4, 5]
```

### Implementation (Boundary Shrinking)

```java
public static List<Integer> spiralOrder(int[][] matrix) {
    List<Integer> result = new ArrayList<>();
    if (matrix == null || matrix.length == 0) return result;

    int top = 0, bottom = matrix.length - 1;
    int left = 0, right = matrix[0].length - 1;

    while (top <= bottom && left <= right) {
        // Top row: left to right
        for (int j = left; j <= right; j++) {
            result.add(matrix[top][j]);
        }
        top++;

        // Right column: top to bottom
        for (int i = top; i <= bottom; i++) {
            result.add(matrix[i][right]);
        }
        right--;

        // Bottom row: right to left (if still valid)
        if (top <= bottom) {
            for (int j = right; j >= left; j--) {
                result.add(matrix[bottom][j]);
            }
            bottom--;
        }

        // Left column: bottom to top (if still valid)
        if (left <= right) {
            for (int i = bottom; i >= top; i--) {
                result.add(matrix[i][left]);
            }
            left++;
        }
    }
    return result;
}
```

### Key insights

1. **Boundary variables** (`top, bottom, left, right`) track the unconquered region
2. **Four passes** per layer: top row, right column, bottom row, left column
3. **Two guards** (`if (top <= bottom)` and `if (left <= right)`) prevent double-counting in single-row or single-column cases
4. **Each boundary shrinks** after its pass — we "peel off" the outer layer

### Edge cases

| Case | Matrix | Behavior |
|------|--------|----------|
| Empty | `[]` | Return empty list |
| Single row | `[[1,2,3]]` | Just first for-loop executes |
| Single column | `[[1],[2],[3]]` | First + second for-loop |
| Single element | `[[5]]` | Just first for-loop |

## Spiral Matrix Generation

**Problem:** Generate an n×n matrix filled with numbers from 1 to n² in spiral order.

```java
public static int[][] generateSpiral(int n) {
    int[][] matrix = new int[n][n];
    int top = 0, bottom = n - 1;
    int left = 0, right = n - 1;
    int num = 1;

    while (top <= bottom && left <= right) {
        // Top row
        for (int j = left; j <= right; j++) {
            matrix[top][j] = num++;
        }
        top++;

        // Right column
        for (int i = top; i <= bottom; i++) {
            matrix[i][right] = num++;
        }
        right--;

        // Bottom row
        if (top <= bottom) {
            for (int j = right; j >= left; j--) {
                matrix[bottom][j] = num++;
            }
            bottom--;
        }

        // Left column
        if (left <= right) {
            for (int i = bottom; i >= top; i--) {
                matrix[i][left] = num++;
            }
            left++;
        }
    }
    return matrix;
}
```

For n=3, output:
```
[1, 2, 3]
[8, 9, 4]
[7, 6, 5]
```

## Anti-Spiral Traversal

Counter-clockwise spiral starting from top-left:

```java
public static List<Integer> antiSpiral(int[][] matrix) {
    List<Integer> result = new ArrayList<>();
    if (matrix == null || matrix.length == 0) return result;

    int top = 0, bottom = matrix.length - 1;
    int left = 0, right = matrix[0].length - 1;

    while (top <= bottom && left <= right) {
        // Left column: top to bottom
        for (int i = top; i <= bottom; i++) {
            result.add(matrix[i][left]);
        }
        left++;

        // Bottom row: left to right
        for (int j = left; j <= right; j++) {
            result.add(matrix[bottom][j]);
        }
        bottom--;

        // Right column: bottom to top
        if (left <= right) {
            for (int i = bottom; i >= top; i--) {
                result.add(matrix[i][right]);
            }
            right--;
        }

        // Top row: right to left
        if (top <= bottom) {
            for (int j = right; j >= left; j--) {
                result.add(matrix[top][j]);
            }
            top++;
        }
    }
    return result;
}
```

## Custom Filling Patterns

### Spiral from center outward (for odd-sized square matrix)

```java
public static int[][] spiralFromCenter(int n) {
    int[][] matrix = new int[n][n];
    int center = n / 2;
    int num = 1;
    matrix[center][center] = num++;

    for (int layer = 1; layer <= center; layer++) {
        // Move right one step, then spiral
        int row = center - layer;
        int col = center - layer + 1;

        // Right edge
        while (col <= center + layer) {
            matrix[row][col] = num++;
            col++;
        }
        col--;
        row++;

        // Bottom edge
        while (row <= center + layer) {
            matrix[row][col] = num++;
            row++;
        }
        row--;
        col--;

        // Left edge
        while (col >= center - layer) {
            matrix[row][col] = num++;
            col--;
        }
        col++;
        row--;

        // Top edge
        while (row > center - layer) {
            matrix[row][col] = num++;
            row--;
        }
    }
    return matrix;
}
```

## Variations Practice

| Problem | Description | Key Difference |
|---------|-------------|----------------|
| Spiral Matrix (LeetCode 54) | Clockwise spiral traversal | Standard |
| Spiral Matrix II (LeetCode 59) | Generate spiral matrix | Filling instead of reading |
| Spiral Matrix III (LeetCode 885) | Spiral starting from center | Non-rectangular path |
| Diagonal Traverse (LeetCode 498) | Zigzag diagonal | Alternating direction |

## Common Mistakes

1. **Not checking boundary validity** after shrinking each dimension — leads to repeated elements
2. **Using while loop without boundary check** — infinite loop
3. **Modifying original indices** — use temporary variables if you need originals
4. **Forgetting that matrices may not be square** — dimensions matter for bounds

## Complexity

| Operation | Time | Space (excluding output) |
|-----------|------|--------------------------|
| Spiral traversal | O(m×n) | O(1) |
| Spiral generation | O(n²) | O(1) |
