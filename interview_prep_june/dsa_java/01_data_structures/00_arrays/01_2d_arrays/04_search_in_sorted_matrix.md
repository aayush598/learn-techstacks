# Search in Sorted Matrix

## Search in Row-wise and Column-wise Sorted Matrix (Staircase Search)

**Problem:** Given a matrix where each row is sorted left-to-right and each column is sorted top-to-bottom, find a target value.

```
[ [1,  4,  7, 11],
  [2,  5,  8, 12],
  [3,  6,  9, 16],
  [10, 13, 14, 17] ]
```

### The Staircase Algorithm

Start from the **top-right corner** (or bottom-left). At each step:
- If current == target → found
- If current > target → move left (smaller values in this row)
- If current < target → move down (larger values in this column)

```java
public static boolean searchMatrix(int[][] matrix, int target) {
    if (matrix == null || matrix.length == 0) return false;

    int rows = matrix.length, cols = matrix[0].length;
    int row = 0, col = cols - 1; // start at top-right

    while (row < rows && col >= 0) {
        if (matrix[row][col] == target) {
            return true;
        } else if (matrix[row][col] > target) {
            col--; // move left
        } else {
            row++; // move down
        }
    }
    return false;
}
```

### Why this works

The matrix has a special property: when you're at `(r, c)`:
- Everything above `r` in column `c` is **smaller** (column sorted)
- Everything to the right of `c` in row `r` is **larger** (row sorted)
- Everything below `r` in column `c` is **larger**
- Everything to the left of `c` in row `r` is **smaller**

At top-right: if current > target, all elements below are even larger (since column is sorted), so we must go left. If current < target, all elements to the left are even smaller, so we must go down.

**Time:** O(m + n) — at most m + n steps.
**Space:** O(1).

### Starting from bottom-left

```java
public static boolean searchMatrixBL(int[][] matrix, int target) {
    int rows = matrix.length, cols = matrix[0].length;
    int row = rows - 1, col = 0;

    while (row >= 0 && col < cols) {
        if (matrix[row][col] == target) {
            return true;
        } else if (matrix[row][col] > target) {
            row--; // move up
        } else {
            col++; // move right
        }
    }
    return false;
}
```

## Search in Fully Sorted Matrix (Binary Search on Flattened)

**Problem:** Given a matrix where each row is sorted and the first element of each row is greater than the last element of the previous row, find target.

```
[ [1,  3,  5,  7],
  [10, 11, 16, 20],
  [23, 30, 34, 60] ]
```

This is essentially a sorted 1D array stored as a matrix. Binary search on it directly.

### Standard binary search

```java
public static boolean searchMatrixFullySorted(int[][] matrix, int target) {
    if (matrix == null || matrix.length == 0) return false;

    int rows = matrix.length, cols = matrix[0].length;
    int left = 0, right = rows * cols - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;
        int midValue = matrix[mid / cols][mid % cols];

        if (midValue == target) {
            return true;
        } else if (midValue < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return false;
}
```

**Time:** O(log(m×n)) — true binary search.
**Space:** O(1).

**Key mapping:** `mid / cols` gives row, `mid % cols` gives column.

### Two-step binary search (less efficient but more obvious)

```java
public static boolean searchMatrixTwoStep(int[][] matrix, int target) {
    // Step 1: find the correct row
    int top = 0, bottom = matrix.length - 1;
    while (top <= bottom) {
        int mid = top + (bottom - top) / 2;
        if (matrix[mid][0] == target) return true;
        if (matrix[mid][0] < target) {
            top = mid + 1;
        } else {
            bottom = mid - 1;
        }
    }
    // bottom is the last row where first element <= target
    if (bottom < 0) return false;

    // Step 2: binary search within that row
    int[] row = matrix[bottom];
    int left = 0, right = row.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (row[mid] == target) return true;
        if (row[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return false;
}
```

## Median of Row-wise Sorted Matrix

**Problem:** Find the median of a matrix where each row is sorted. The matrix has an odd number of elements.

```java
public static int findMedian(int[][] matrix) {
    int rows = matrix.length, cols = matrix[0].length;
    int totalElements = rows * cols;
    int requiredCount = totalElements / 2 + 1; // elements <= median

    // Find the min and max in the matrix
    int low = Integer.MAX_VALUE, high = Integer.MIN_VALUE;
    for (int[] row : matrix) {
        low = Math.min(low, row[0]);
        high = Math.max(high, row[cols - 1]);
    }

    // Binary search on value range
    while (low < high) {
        int mid = low + (high - low) / 2;
        int count = countLessOrEqual(matrix, mid);

        if (count < requiredCount) {
            low = mid + 1;
        } else {
            high = mid;
        }
    }
    return low;
}

// Count elements <= x in the sorted matrix
private static int countLessOrEqual(int[][] matrix, int x) {
    int rows = matrix.length, cols = matrix[0].length;
    int count = 0;
    for (int[] row : matrix) {
        // Binary search per row for upper bound of x
        int left = 0, right = cols;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (row[mid] <= x) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        count += left;
    }
    return count;
}
```

### How it works

Instead of searching for a position, we binary search on the **value** itself. We know the median must be between `min` and `max` of the matrix. For each guessed value `mid`, we count how many elements are ≤ `mid`. If the count is less than the required count for the median, we need a bigger value. Otherwise, `mid` might be the median (or too high).

**Time:** O(rows × log(cols) × log(range)) — binary search on value range (log of 2³¹ ≈ 31), each check does binary search in each row.
**Space:** O(1).

## Practice Problems

| Problem | LeetCode | Type | Complexity |
|---------|----------|------|------------|
| Search a 2D Matrix | 74 | Fully sorted | O(log m×n) |
| Search a 2D Matrix II | 240 | Row/col sorted | O(m + n) |
| Kth Smallest in Sorted Matrix | 378 | Row/col sorted | O(n × log(range)) |
| Median of Row Wise Sorted Matrix | - | Interview classic | O(rows × log(cols) × log(range)) |

## Which approach to use?

| Matrix Property | Best Approach | Complexity |
|----------------|---------------|------------|
| Each row sorted, first of each row > last of previous | Binary search on flattened | O(log m×n) |
| Each row sorted, each column sorted (not fully) | Staircase search | O(m + n) |
| Each row sorted, find median | Binary search on value range | O(m × log n × log range) |

## Common Mistakes

1. **Using staircase on a fully sorted matrix** — works but suboptimal (O(m+n) vs O(log(m×n)))
2. **Binary search on wrong dimension** — remember `mid / cols` for row, `mid % cols` for column
3. **Not handling empty matrix** — always check first
4. **Confusing row/col indexing** — `matrix[row][col]`, not `matrix[col][row]`
