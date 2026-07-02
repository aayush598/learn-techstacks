# Quick Sort

## Concept

Quick sort is a divide-and-conquer algorithm that selects a "pivot" element, partitions the array around it (elements < pivot on left, > pivot on right), then recursively sorts the partitions.

## Characteristics

| Property | Value |
|----------|-------|
| Time (Average) | O(n log n) |
| Time (Worst) | O(n²) — sorted array with bad pivot |
| Time (Best) | O(n log n) |
| Space | O(log n) — recursion stack |
| Stable | No (by default with most partition schemes) |
| In-place | Yes |

## Partition Schemes

### Lomuto Partition (Simple but O(n²) when sorted)

Picks the last element as pivot. Simpler but does 3x more swaps than Hoare.

```java
public class QuickSortLomuto {
    public static void quickSort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }

    private static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];  // Last element as pivot
        int i = low - 1;        // Index of smaller element

        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }

        swap(arr, i + 1, high);
        return i + 1;  // Pivot's final position
    }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

### Hoare Partition (Faster, ~3x fewer swaps)

Uses two pointers moving towards each other. Much fewer swaps on average.

```java
public class QuickSortHoare {
    public static void quickSort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }

    private static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi);
            quickSort(arr, pi + 1, high);
        }
    }

    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[low + (high - low) / 2];  // Middle element as pivot
        int i = low - 1;
        int j = high + 1;

        while (true) {
            do { i++; } while (arr[i] < pivot);
            do { j--; } while (arr[j] > pivot);

            if (i >= j) return j;

            swap(arr, i, j);
        }
    }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

### Lomuto vs Hoare Comparison

| Aspect | Lomuto | Hoare |
|--------|--------|-------|
| Pivot choice | Usually last element | Usually middle element |
| Swaps | ~3x more | Fewer |
| Partition result index | Pivot at its final position | Partition point (not necessarily pivot) |
| Recursion | (low, pi-1), (pi+1, high) | (low, pi), (pi+1, high) |
| When sorted | O(n²) | O(n log n) if pivot is median |
| Stable | No | No |

## Random Pivot (Avoiding Worst Case)

```java
import java.util.Random;

public class QuickSortRandomPivot {
    private static final Random random = new Random();

    public static void quickSort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }

    private static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = randomPartition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    private static int randomPartition(int[] arr, int low, int high) {
        int randomIdx = low + random.nextInt(high - low + 1);
        swap(arr, randomIdx, high);  // Move random pivot to end
        return partition(arr, low, high);
    }

    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }

        swap(arr, i + 1, high);
        return i + 1;
    }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

## Median-of-3 Pivot

Choose the median of first, middle, and last elements as pivot to reduce worst-case probability:

```java
public class QuickSortMedianOf3 {
    public static void quickSort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }

    private static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = medianPartition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    private static int medianPartition(int[] arr, int low, int high) {
        int mid = low + (high - low) / 2;

        // Sort low, mid, high to find median
        if (arr[mid] < arr[low]) swap(arr, low, mid);
        if (arr[high] < arr[low]) swap(arr, low, high);
        if (arr[high] < arr[mid]) swap(arr, mid, high);

        // Move median to end as pivot
        swap(arr, mid, high);
        return partition(arr, low, high);
    }

    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }

        swap(arr, i + 1, high);
        return i + 1;
    }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

## Quick Select: Kth Smallest Element

Uses partition to find the kth smallest element in O(n) average time:

```java
public class QuickSelect {
    public static int findKthSmallest(int[] arr, int k) {
        if (k < 1 || k > arr.length) throw new IllegalArgumentException();
        return quickSelect(arr, 0, arr.length - 1, k - 1);  // k-1 for 0-indexed
    }

    private static int quickSelect(int[] arr, int low, int high, int k) {
        if (low == high) return arr[low];

        int pi = partition(arr, low, high);

        if (k == pi) {
            return arr[pi];
        } else if (k < pi) {
            return quickSelect(arr, low, pi - 1, k);
        } else {
            return quickSelect(arr, pi + 1, high, k);
        }
    }

    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }

        swap(arr, i + 1, high);
        return i + 1;
    }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    public static void main(String[] args) {
        int[] arr = {7, 10, 4, 3, 20, 15};
        int k = 3;
        System.out.println(k + "rd smallest: " + findKthSmallest(arr, k));
        // Output: 7
    }
}
```

## 3-Way Partition (Dutch National Flag)

Handles duplicates efficiently by partitioning into three regions: < pivot, == pivot, > pivot:

```java
public class QuickSort3Way {
    public static void quickSort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }

    private static void quickSort(int[] arr, int low, int high) {
        if (low >= high) return;

        int lt = low;
        int gt = high;
        int pivot = arr[low];
        int i = low;

        // 3-way partition
        while (i <= gt) {
            if (arr[i] < pivot) {
                swap(arr, lt, i);
                lt++;
                i++;
            } else if (arr[i] > pivot) {
                swap(arr, i, gt);
                gt--;
            } else {
                i++;
            }
        }

        // Recursively sort < pivot and > pivot partitions
        quickSort(arr, low, lt - 1);
        quickSort(arr, gt + 1, high);
    }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

**Why 3-way is better:** When there are many duplicates, the == pivot partition is already sorted, reducing recursion depth significantly.

## Complete Demo

```java
public class QuickSortDemo {
    public static void main(String[] args) {
        int[] arr = {10, 7, 8, 9, 1, 5};

        System.out.println("Original: " + Arrays.toString(arr));

        // Lomuto
        int[] arr1 = arr.clone();
        QuickSortLomuto.quickSort(arr1);
        System.out.println("Lomuto:   " + Arrays.toString(arr1));

        // Hoare
        int[] arr2 = arr.clone();
        QuickSortHoare.quickSort(arr2);
        System.out.println("Hoare:    " + Arrays.toString(arr2));

        // Random pivot
        int[] arr3 = arr.clone();
        QuickSortRandomPivot.quickSort(arr3);
        System.out.println("Random:   " + Arrays.toString(arr3));

        // Median-of-3
        int[] arr4 = arr.clone();
        QuickSortMedianOf3.quickSort(arr4);
        System.out.println("MedOf3:   " + Arrays.toString(arr4));

        // 3-way
        int[] arr5 = arr.clone();
        QuickSort3Way.quickSort(arr5);
        System.out.println("3-Way:    " + Arrays.toString(arr5));

        // Quick Select
        int k = 3;
        arr = new int[]{7, 10, 4, 3, 20, 15};
        System.out.println("\nQuick Select:");
        System.out.println(k + "rd smallest in " +
            Arrays.toString(arr) + ": " +
            QuickSelect.findKthSmallest(arr, k));
    }
}
```

## Complexity Analysis

| Case | Time | Space (Stack) | Cause |
|------|------|---------------|-------|
| Best | O(n log n) | O(log n) | Pivot always splits evenly |
| Average | O(n log n) | O(log n) | Random partition |
| Worst | O(n²) | O(n) | Sorted array, bad pivot |

### Worst Case Analysis

For Lomuto partition on an already sorted array:
- Each partition splits into {n-1, 0} subsets
- Recurrence: T(n) = T(n-1) + O(n) → O(n²)

**How to avoid:**
- Random pivot (probabilistic guarantee)
- Median-of-3 (increases good pivot probability)
- IntroSort (switches to heap sort if recursion depth too deep)

## Key Points

| Aspect | Detail |
|--------|--------|
| Fastest in practice | Best cache performance among O(n log n) sorts |
| Not stable | Standard implementation is unstable |
| In-place | Works within the array (except recursion stack) |
| Tail recursion optimization | Can optimize to reduce stack depth |
| Worst case | O(n²) but probability is negligible with random pivot |

**Quick sort is the most widely used sorting algorithm in practice (C's qsort, C++'s std::sort, Java's Arrays.sort() for primitives). Its cache performance and in-place nature make it faster than merge sort for arrays.**
