# Selection Sort

## Concept

Selection sort divides the array into a sorted and unsorted region. It repeatedly finds the minimum element from the unsorted region and swaps it with the first element of the unsorted region.

## Characteristics

| Property | Value |
|----------|-------|
| Time (All cases) | O(n²) — no best-case improvement |
| Space | O(1) — in-place |
| Stable | NOT stable by default (can be made stable with shifts) |
| Adaptive | No |
| Swaps | O(n) — minimal swaps |

## Basic Implementation

```java
public class SelectionSort {
    public static void selectionSort(int[] arr) {
        int n = arr.length;

        for (int i = 0; i < n - 1; i++) {
            // Find the minimum element in unsorted portion
            int minIdx = i;

            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIdx]) {
                    minIdx = j;
                }
            }

            // Swap found minimum with the first unsorted position
            if (minIdx != i) {
                int temp = arr[i];
                arr[i] = arr[minIdx];
                arr[minIdx] = temp;
            }
        }
    }
}
```

## Stable Selection Sort (Using Shifts)

The regular selection sort is not stable because swapping can move an equal element past another. A stable version uses shifting instead of swapping:

```java
public class StableSelectionSort {
    public static void stableSelectionSort(int[] arr) {
        int n = arr.length;

        for (int i = 0; i < n - 1; i++) {
            int minIdx = i;

            // Find minimum element
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIdx]) {
                    minIdx = j;
                }
            }

            // Shift elements right instead of swapping
            int minVal = arr[minIdx];
            for (int k = minIdx; k > i; k--) {
                arr[k] = arr[k - 1];
            }
            arr[i] = minVal;
        }
    }
}
```

## Why Selection Sort is Good for Memory Writes

Selection sort makes exactly O(n) swaps (at most n-1). This is the minimum possible among comparison-based sorts that work by swapping.

```java
public class SelectionSortDemo {
    public static void main(String[] args) {
        int[] arr = {64, 25, 12, 22, 11};

        System.out.println("Selection Sort - Minimal Swaps");
        System.out.println("Original: " + Arrays.toString(arr));

        int swapCount = selectionSortWithCount(arr);
        System.out.println("Sorted:   " + Arrays.toString(arr));
        System.out.println("Total swaps: " + swapCount);
        // Only 4 swaps for 5 elements (n-1)
    }

    public static int selectionSortWithCount(int[] arr) {
        int n = arr.length;
        int swaps = 0;

        for (int i = 0; i < n - 1; i++) {
            int minIdx = i;
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIdx]) {
                    minIdx = j;
                }
            }

            if (minIdx != i) {
                int temp = arr[i];
                arr[i] = arr[minIdx];
                arr[minIdx] = temp;
                swaps++;
            }
        }

        return swaps;
    }
}
```

## Comparison with Bubble Sort

| Aspect | Selection Sort | Bubble Sort |
|--------|---------------|-------------|
| Swaps | O(n) | O(n²) |
| Comparisons | O(n²) | O(n²) |
| Stable | No | Yes |
| Adaptive | No | Yes (optimized) |
| Best for | Memory writes are expensive | Educational, nearly sorted data |

## Edge Cases and Partial Sorting

```java
public class SelectionSortVariants {
    // Sort only first k elements
    public static void partialSort(int[] arr, int k) {
        int n = Math.min(k, arr.length);

        for (int i = 0; i < n - 1; i++) {
            int minIdx = i;
            for (int j = i + 1; j < arr.length; j++) {
                if (arr[j] < arr[minIdx]) {
                    minIdx = j;
                }
            }
            if (minIdx != i) {
                int temp = arr[i];
                arr[i] = arr[minIdx];
                arr[minIdx] = temp;
            }
        }
    }

    // Sort in descending order
    public static void selectionSortDescending(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            int maxIdx = i;
            for (int j = i + 1; j < n; j++) {
                if (arr[j] > arr[maxIdx]) {
                    maxIdx = j;
                }
            }
            if (maxIdx != i) {
                int temp = arr[i];
                arr[i] = arr[maxIdx];
                arr[maxIdx] = temp;
            }
        }
    }

    // Bidirectional selection sort (find min and max in one pass)
    public static void bidirectionalSelectionSort(int[] arr) {
        int n = arr.length;
        for (int i = 0, j = n - 1; i < j; i++, j--) {
            int minIdx = i;
            int maxIdx = i;

            for (int k = i; k <= j; k++) {
                if (arr[k] < arr[minIdx]) minIdx = k;
                if (arr[k] > arr[maxIdx]) maxIdx = k;
            }

            // Swap min to position i
            int temp = arr[i];
            arr[i] = arr[minIdx];
            arr[minIdx] = temp;

            // If max was at i, it was swapped to minIdx
            if (maxIdx == i) maxIdx = minIdx;

            // Swap max to position j
            temp = arr[j];
            arr[j] = arr[maxIdx];
            arr[maxIdx] = temp;
        }
    }
}
```

## Complete Demo

```java
public class SelectionSortDemoComplete {
    public static void main(String[] args) {
        // Regular selection sort
        int[] arr1 = {64, 25, 12, 22, 11};
        SelectionSort.selectionSort(arr1);
        System.out.println("Regular: " + Arrays.toString(arr1));

        // Stable selection sort
        int[] arr2 = {64, 25, 12, 22, 11};
        StableSelectionSort.stableSelectionSort(arr2);
        System.out.println("Stable:  " + Arrays.toString(arr2));

        // Bidirectional
        int[] arr3 = {64, 25, 12, 22, 11};
        SelectionSortVariants.bidirectionalSelectionSort(arr3);
        System.out.println("Bidir:   " + Arrays.toString(arr3));

        // Partial sort (first 3 elements)
        int[] arr4 = {64, 25, 12, 22, 11};
        SelectionSortVariants.partialSort(arr4, 3);
        System.out.println("Partial: " + Arrays.toString(arr4));

        // Descending
        int[] arr5 = {64, 25, 12, 22, 11};
        SelectionSortVariants.selectionSortDescending(arr5);
        System.out.println("Desc:    " + Arrays.toString(arr5));

        // Stability demo
        int[] arr6 = {4, 2, 2, 8};  // Two 2s (let's track them)
        System.out.println("\nStability test:");
        System.out.println("Original: " + Arrays.toString(arr6));
        SelectionSort.selectionSort(arr6);
        System.out.println("Standard: " + Arrays.toString(arr6) + " (relative order of 2s lost)");

        arr6 = new int[]{4, 2, 2, 8};
        StableSelectionSort.stableSelectionSort(arr6);
        System.out.println("Stable:   " + Arrays.toString(arr6) + " (relative order of 2s preserved)");
    }
}
```

## Use Cases

| Scenario | Recommendation |
|----------|---------------|
| Memory writes expensive | Selection Sort (minimal swaps) |
| Flash storage (EEPROM) | Selection Sort (minimizes write cycles) |
| Stability required | Use stable sort instead |
| Large datasets | Avoid O(n²) entirely |
| Educational | Good for teaching algorithm analysis |

## Key Points

- **Minimizes swaps:** Only O(n) swaps, making it ideal when swap operations are costly
- **Not stable:** The swap can change relative order of equal elements
- **Not adaptive:** Always O(n²) regardless of input ordering
- **Simple to implement:** Straightforward logic, easy to verify correctness
