# Binary Search on 2D Arrays

## Search in Row-Wise Sorted Matrix

Each row is sorted in ascending order. Perform binary search on each row.

```java
public class SearchInRowSortedMatrix {
    public static boolean searchMatrix(int[][] matrix, int target) {
        for (int[] row : matrix) {
            int idx = binarySearch(row, target);
            if (idx != -1) return true;
        }
        return false;
    }

    private static int binarySearch(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }
}
```

## Search in Row+Col Sorted Matrix (Staircase Search)

The matrix has both rows and columns sorted in ascending order. Use the "staircase" approach — start from top-right corner.

**Time:** O(m + n), **Space:** O(1)

```java
public class StaircaseSearch {
    public static boolean searchMatrix(int[][] matrix, int target) {
        if (matrix == null || matrix.length == 0) return false;

        int rows = matrix.length;
        int cols = matrix[0].length;

        int row = 0;
        int col = cols - 1;

        while (row < rows && col >= 0) {
            if (matrix[row][col] == target) {
                return true;
            } else if (matrix[row][col] > target) {
                col--;  // Move left (smaller values)
            } else {
                row++;  // Move down (larger values)
            }
        }

        return false;
    }

    // Return indices if found
    public static int[] searchMatrixWithIndices(int[][] matrix, int target) {
        int row = 0;
        int col = matrix[0].length - 1;

        while (row < matrix.length && col >= 0) {
            if (matrix[row][col] == target) {
                return new int[]{row, col};
            } else if (matrix[row][col] > target) {
                col--;
            } else {
                row++;
            }
        }

        return new int[]{-1, -1};
    }
}
```

**Why it works:** Starting from top-right:
- All elements to the left are smaller (same row, decreasing columns)
- All elements below are larger (same column, increasing rows)
- Each step eliminates either a row or a column

## Binary Search on Fully Sorted Matrix (Flattened)

When the matrix is sorted row-wise and the first element of each row is greater than the last of the previous row, treat it as a flattened sorted array.

```java
public class SearchInFlattenedMatrix {
    public static boolean searchMatrix(int[][] matrix, int target) {
        int rows = matrix.length;
        int cols = matrix[0].length;

        int low = 0;
        int high = rows * cols - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;
            int row = mid / cols;
            int col = mid % cols;

            if (matrix[row][col] == target) {
                return true;
            } else if (matrix[row][col] < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }

        return false;
    }
}
```

## Median of Row-Wise Sorted Matrix

Find the median of a matrix where each row is sorted. The matrix has an odd number of elements.

**Approach:** Binary search on the value range [min, max]. Count elements ≤ mid. Adjust range based on count vs target (n*m/2).

```java
public class MedianOfRowSortedMatrix {
    public static int findMedian(int[][] matrix) {
        int rows = matrix.length;
        int cols = matrix[0].length;
        int total = rows * cols;
        int target = total / 2;  // We need exactly this many elements ≤ median

        // Find min and max in the matrix
        int low = matrix[0][0];
        int high = matrix[0][cols - 1];

        for (int i = 1; i < rows; i++) {
            low = Math.min(low, matrix[i][0]);
            high = Math.max(high, matrix[i][cols - 1]);
        }

        // Binary search on value range
        while (low <= high) {
            int mid = low + (high - low) / 2;
            int count = countLessOrEqual(matrix, mid);

            if (count <= target) {
                low = mid + 1;  // Need larger value
            } else {
                high = mid - 1; // Can try smaller value
            }
        }

        return low;
    }

    // Count elements ≤ value in each row using binary search
    private static int countLessOrEqual(int[][] matrix, int value) {
        int count = 0;
        for (int[] row : matrix) {
            count += upperBound(row, value);
        }
        return count;
    }

    // Count elements ≤ target in a sorted row
    private static int upperBound(int[] arr, int target) {
        int low = 0;
        int high = arr.length;

        while (low < high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] > target) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }

        return low;  // Number of elements ≤ target
    }
}
```

### Alternative: Using Java's Arrays.binarySearch

```java
import java.util.Arrays;

public class MedianUsingArrays {
    public static int findMedian(int[][] matrix) {
        int rows = matrix.length;
        int cols = matrix[0].length;
        int target = (rows * cols) / 2;

        int low = matrix[0][0];
        int high = matrix[0][cols - 1];

        for (int i = 1; i < rows; i++) {
            low = Math.min(low, matrix[i][0]);
            high = Math.max(high, matrix[i][cols - 1]);
        }

        while (low <= high) {
            int mid = low + (high - low) / 2;
            int count = 0;

            for (int[] row : matrix) {
                int idx = Arrays.binarySearch(row, mid);
                if (idx < 0) {
                    idx = -idx - 1;  // Insertion point
                } else {
                    // Found equal elements — move past them
                    while (idx < row.length && row[idx] == mid) {
                        idx++;
                    }
                }
                count += idx;
            }

            if (count <= target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }

        return low;
    }
}
```

## Performance Analysis

| Problem | Time | Space | Approach |
|---------|------|-------|----------|
| Row-wise sorted search | O(m log n) | O(1) | Binary search each row |
| Row+col sorted (staircase) | O(m + n) | O(1) | Top-right, move left/down |
| Fully sorted (flattened) | O(log(mn)) | O(1) | 1D binary search |
| Median of row sorted | O(log(range) * m * log n) | O(1) | BS on value range |

## Complete Demo

```java
public class MatrixSearchDemo {
    public static void main(String[] args) {
        // Row-wise sorted matrix
        int[][] matrix1 = {
            {1, 3, 5, 7},
            {10, 11, 16, 20},
            {23, 30, 34, 60}
        };

        System.out.println("Row-wise sorted:");
        System.out.println("Search for 3: " +
            SearchInRowSortedMatrix.searchMatrix(matrix1, 3));
        System.out.println("Search for 13: " +
            SearchInRowSortedMatrix.searchMatrix(matrix1, 13));

        // Flattened sorted matrix
        System.out.println("\nFlattened search:");
        System.out.println("Search for 3: " +
            SearchInFlattenedMatrix.searchMatrix(matrix1, 3));
        System.out.println("Search for 20: " +
            SearchInFlattenedMatrix.searchMatrix(matrix1, 20));

        // Staircase matrix (different example)
        int[][] matrix2 = {
            {1, 4, 7, 11, 15},
            {2, 5, 8, 12, 19},
            {3, 6, 9, 16, 22},
            {10, 13, 14, 17, 24},
            {18, 21, 23, 26, 30}
        };

        System.out.println("\nStaircase search:");
        System.out.println("Search for 5: " +
            StaircaseSearch.searchMatrix(matrix2, 5));
        int[] idx = StaircaseSearch.searchMatrixWithIndices(matrix2, 5);
        System.out.println("Found at: [" + idx[0] + "][" + idx[1] + "]");
        System.out.println("Search for 20: " +
            StaircaseSearch.searchMatrix(matrix2, 20));

        // Median of row-wise sorted
        int[][] matrix3 = {
            {1, 3, 5},
            {2, 6, 9},
            {3, 6, 9}
        };
        System.out.println("\nMedian of row-wise sorted:");
        System.out.println("Median: " +
            MedianOfRowSortedMatrix.findMedian(matrix3));
    }
}
```

## Key Patterns Summary

| Matrix Type | Search Method | Time |
|-------------|--------------|------|
| Each row sorted | BS on each row | O(m log n) |
| Rows + cols sorted | Staircase from top-right | O(m + n) |
| Flattened sorted | 1D BS | O(log mn) |
| Find median | BS on value range | O(log range * m log n) |

## Common Interview Follow-ups

1. **Search in a matrix where rows are sorted left-to-right and each row's first integer > previous row's last** → Use flattened binary search (LeetCode 74)

2. **Search in a matrix where rows and columns are sorted separately** → Use staircase search (LeetCode 240)

3. **Find kth smallest element in a sorted matrix** → Use binary search on value range with count (LeetCode 378)
