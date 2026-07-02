# 2D Arrays — Basics

## Memory Representation

A 2D array in Java is an **array of arrays** (jagged array support built-in).

```java
int[][] matrix = new int[3][4];
```

In memory:
```
matrix (stack) → [ref] → [0]: [ref] → [0, 1, 2, 3]   (heap)
                           [1]: [ref] → [4, 5, 6, 7]
                           [2]: [ref] → [8, 9, 10, 11]
```

Each row is a separate object on the heap. The main array holds references to row arrays.

### Row-major vs Column-major

**Row-major:** Memory is laid out row by row. `arr[i][j]` is at `base + (i * cols + j) * elementSize`. Java uses row-major.

**Column-major:** Memory is laid out column by column. More common in Fortran.

**Why this matters:** Iterating row-wise (reading row by row) is cache-friendly in Java. Column-wise iteration jumps across memory locations, causing cache misses.

```java
// FAST (row-wise): memory access is sequential
for (int i = 0; i < rows; i++)
    for (int j = 0; j < cols; j++)
        process(matrix[i][j]);

// SLOW (column-wise): jumping across rows
for (int j = 0; j < cols; j++)
    for (int i = 0; i < rows; i++)
        process(matrix[i][j]);
```

## Declaration and Initialization

### Declaration

```java
int[][] matrix;           // 2D array
int matrix[][];           // C-style, works
int[] matrix[];           // weird but valid — DON'T
```

### Initialization

```java
// 1. Fixed rows and columns
int[][] grid = new int[3][4];

// 2. Jagged array (different column counts per row)
int[][] jagged = new int[3][];
jagged[0] = new int[2];
jagged[1] = new int[5];
jagged[2] = new int[3];

// 3. Inline initialization
int[][] matrix = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

// 4. Anonymous
new int[][]{{1, 2}, {3, 4}};
```

### Default Values

| Element Type | Default Value |
|--------------|---------------|
| int | 0 |
| double | 0.0 |
| boolean | false |
| Object | null |

## Getting Dimensions

```java
int rows = matrix.length;
int cols = matrix[0].length;  // careful: only if matrix[0] exists!
```

For jagged arrays, rows can have different lengths:

```java
for (int i = 0; i < jagged.length; i++) {
    int colsInRow = jagged[i].length; // varies per row
}
```

## Traversal Patterns

### Row-wise (outer loop over rows)

```java
for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
        System.out.print(matrix[i][j] + " ");
    }
    System.out.println();
}
```

### Column-wise (outer loop over columns)

```java
for (int j = 0; j < cols; j++) {
    for (int i = 0; i < rows; i++) {
        System.out.print(matrix[i][j] + " ");
    }
    System.out.println();
}
```

### Enhanced for-each

```java
for (int[] row : matrix) {
    for (int val : row) {
        System.out.print(val + " ");
    }
    System.out.println();
}
```

## Input Reading

### From Scanner

```java
Scanner sc = new Scanner(System.in);
int rows = sc.nextInt();
int cols = sc.nextInt();
int[][] matrix = new int[rows][cols];

for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
        matrix[i][j] = sc.nextInt();
    }
}
```

### From BufferedReader (faster for large input)

```java
BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
String[] dims = br.readLine().split(" ");
int rows = Integer.parseInt(dims[0]);
int cols = Integer.parseInt(dims[1]);
int[][] matrix = new int[rows][cols];

for (int i = 0; i < rows; i++) {
    String[] line = br.readLine().split(" ");
    for (int j = 0; j < cols; j++) {
        matrix[i][j] = Integer.parseInt(line[j]);
    }
}
```

## Printing

### Simple print

```java
for (int[] row : matrix) {
    System.out.println(Arrays.toString(row));
}
```

### Formatted print

```java
for (int[] row : matrix) {
    for (int val : row) {
        System.out.printf("%4d", val);
    }
    System.out.println();
}
```

### Deep toString

```java
System.out.println(Arrays.deepToString(matrix));
// Output: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

## Fill

### Using loops

```java
int[][] matrix = new int[3][3];
int count = 1;
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        matrix[i][j] = count++;
    }
}
```

### Using Arrays.fill (works per row)

```java
for (int[] row : matrix) {
    Arrays.fill(row, -1);
}
```

## Copy

### Shallow copy

```java
int[][] copy = matrix.clone(); // only clones the outer array, rows are shared
```

### Deep copy

```java
int[][] deepCopy = new int[matrix.length][];
for (int i = 0; i < matrix.length; i++) {
    deepCopy[i] = matrix[i].clone();
}
```

Or using streams (Java 8+):

```java
int[][] deepCopy = Arrays.stream(matrix)
    .map(int[]::clone)
    .toArray(int[][]::new);
```

## Ragged/Jagged Arrays

Jagged arrays have rows of different lengths. They're useful when each row represents variable-length data.

```java
int[][] triangle = new int[5][];
for (int i = 0; i < 5; i++) {
    triangle[i] = new int[i + 1]; // row i has i+1 elements
}

// Fill Pascal's triangle
for (int i = 0; i < 5; i++) {
    triangle[i][0] = triangle[i][i] = 1;
    for (int j = 1; j < i; j++) {
        triangle[i][j] = triangle[i-1][j-1] + triangle[i-1][j];
    }
}
```

## Common Pitfalls

1. **`ArrayIndexOutOfBoundsException`** — accessing `matrix[row][col]` where row/col out of bounds
2. **Assuming rectangular** — jagged arrays have different lengths per row
3. **Null pointer on `matrix[0]`** — for empty arrays or uninitialized rows
4. **Confusing row/col indices** — `matrix[i][j]`: i is the row index (vertical), j is the column index (horizontal)
5. **Copy by reference** — `int[][] copy = original` does NOT copy the matrix

## Quick Reference

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Access | O(1) | `matrix[i][j]` |
| Row-wise traversal | O(R*C) | Cache-friendly |
| Column-wise traversal | O(R*C) | Cache-inefficient |
| Deep copy | O(R*C) | Must copy each row |
| Transpose | O(R*C) | O(1) space for square only |
