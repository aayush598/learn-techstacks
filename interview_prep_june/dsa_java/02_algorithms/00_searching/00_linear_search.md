# Linear Search

## Concept

Linear search is the simplest searching algorithm. It sequentially checks each element in the array until the target is found or the array ends.

**Time Complexity:** O(n)  
**Space Complexity:** O(1)  
**Suitable for:** Unsorted arrays, small datasets, single-pass needs

## Basic Linear Search

```java
public class LinearSearch {
    public static int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }
}
```

## Searching for Multiple Occurrences

Return all indices where the target appears:

```java
import java.util.ArrayList;
import java.util.List;

public class LinearSearchMultiple {
    public static List<Integer> findAllOccurrences(int[] arr, int target) {
        List<Integer> indices = new ArrayList<>();
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                indices.add(i);
            }
        }
        return indices;
    }
}
```

## Searching in 2D Array

```java
public class LinearSearch2D {
    public static int[] searchIn2D(int[][] matrix, int target) {
        for (int row = 0; row < matrix.length; row++) {
            for (int col = 0; col < matrix[row].length; col++) {
                if (matrix[row][col] == target) {
                    return new int[]{row, col};
                }
            }
        }
        return new int[]{-1, -1};
    }

    // Find maximum in 2D
    public static int findMax(int[][] matrix) {
        int max = matrix[0][0];
        for (int[] row : matrix) {
            for (int val : row) {
                if (val > max) max = val;
            }
        }
        return max;
    }
}
```

## Linear Search with Early Break

If the target is likely to be at the beginning, or we have constraints:

```java
public class LinearSearchEarlyBreak {
    // Search only first n elements
    public static int searchWithLimit(int[] arr, int target, int limit) {
        int end = Math.min(limit, arr.length);
        for (int i = 0; i < end; i++) {
            if (arr[i] == target) return i;
        }
        return -1;
    }

    // Search while condition holds (e.g., sorted portion)
    public static int searchWhileLessThan(int[] arr, int target) {
        for (int i = 0; i < arr.length && arr[i] <= target; i++) {
            if (arr[i] == target) return i;
        }
        return -1;
    }
}
```

## When Linear Search Beats Binary Search

Linear search is sometimes faster despite O(n) vs O(log n):

1. **Very small n (n < 10-20):** Binary search overhead (pivot calculations, recursive calls) dominates
2. **Unsorted data:** Binary search requires sorting first (O(n log n)), which is worse than O(n) linear
3. **Single-use search:** If searching only once, O(n) linear may beat O(log n) after O(n log n) sort
4. **Data in cache-friendly layout:** Sequential memory access is CPU-cache friendly; binary search jumps around
5. **Target near the beginning:** Average case of linear search is n/2, but early elements are found fast

```java
public class LinearVsBinary {
    // When to prefer linear search:
    // - n < 20
    // - Unsorted array, single search
    // - Data in linked list (no random access)
    // - Streaming data (can't sort infinite stream)

    public static int searchAdaptive(int[] arr, int target) {
        if (arr.length < 20) {
            return linearSearch(arr, target);
        }
        // For larger sorted arrays, use binary search
        // For unsorted, we might still prefer linear for single use
        return linearSearch(arr, target);
    }

    private static int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) return i;
        }
        return -1;
    }
}
```

## Sentinel Linear Search (Optimization)

Instead of checking `i < n` in every loop iteration, place the target at the end as a sentinel. This eliminates one comparison per iteration.

**Standard loop makes 2 comparisons per iteration:** `i < n` and `arr[i] == target`  
**Sentinel loop makes 1 comparison per iteration:** only `arr[i] == target`

```java
public class SentinelLinearSearch {
    public static int sentinelSearch(int[] arr, int target) {
        int n = arr.length;

        // Save the last element
        int last = arr[n - 1];

        // Place sentinel at the end
        arr[n - 1] = target;

        int i = 0;
        while (arr[i] != target) {
            i++;
        }

        // Restore the last element
        arr[n - 1] = last;

        // If found before last position (or last was the target)
        if (i < n - 1 || last == target) {
            return i;
        }

        return -1;
    }
}
```

**Why it's faster:** The sentinel guarantees the target will be found, so we don't need the bounds check `i < n`. This reduces branch instructions, improving pipelining in modern CPUs.

## Complete Example with Performance Comparison

```java
public class LinearSearchDemo {
    public static void main(String[] args) {
        int[] arr = {4, 2, 8, 1, 9, 5, 3, 7, 6};

        // Basic search
        int idx = linearSearch(arr, 5);
        System.out.println("Found 5 at: " + idx);

        // Multiple occurrences
        int[] arrWithDups = {1, 3, 5, 3, 7, 3, 9};
        List<Integer> all3 = findAllOccurrences(arrWithDups, 3);
        System.out.println("All positions of 3: " + all3);

        // Search in 2D
        int[][] matrix = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        int[] pos = searchIn2D(matrix, 5);
        System.out.println("Found 5 at: [" + pos[0] + "][" + pos[1] + "]");

        // Sentinel search
        int sentinelIdx = sentinelSearch(arr, 9);
        System.out.println("Sentinel found 9 at: " + sentinelIdx);
    }
}
```

## Key Takeaways

| Aspect | Linear Search |
|--------|--------------|
| Best Case | O(1) — target at first position |
| Worst Case | O(n) — target at last or absent |
| Average Case | O(n) — n/2 comparisons |
| Space | O(1) — in-place |
| Data Requirement | None — works on any array |
| Stability | N/A |
| Adaptive | No — always scans full array in worst case |

**Use linear search when:**
- Array is unsorted and you're searching only once
- n is small (under ~20-50)
- You're working with a linked list (no O(1) random access)
- Data is streaming and you can't index arbitrarily
- You need to find all occurrences, not just the first
