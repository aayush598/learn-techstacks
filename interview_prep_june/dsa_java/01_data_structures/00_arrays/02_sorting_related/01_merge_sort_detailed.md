# Merge Sort — Detailed

## Divide and Conquer

Merge Sort follows the divide-and-conquer paradigm:

1. **Divide:** Split the array into two halves
2. **Conquer:** Recursively sort each half
3. **Combine:** Merge the two sorted halves

### Full Implementation

```java
public class MergeSort {
    public static void sort(int[] arr) {
        if (arr == null || arr.length < 2) return;
        mergeSort(arr, 0, arr.length - 1);
    }

    private static void mergeSort(int[] arr, int left, int right) {
        if (left < right) {
            int mid = left + (right - left) / 2; // avoid overflow
            mergeSort(arr, left, mid);
            mergeSort(arr, mid + 1, right);
            merge(arr, left, mid, right);
        }
    }

    @SuppressWarnings("ManualArrayToCollectionCopy")
    private static void merge(int[] arr, int left, int mid, int right) {
        // Sizes of two subarrays
        int n1 = mid - left + 1;
        int n2 = right - mid;

        // Create temp arrays
        int[] leftArr = new int[n1];
        int[] rightArr = new int[n2];

        // Copy data
        System.arraycopy(arr, left, leftArr, 0, n1);
        System.arraycopy(arr, mid + 1, rightArr, 0, n2);

        // Merge the temp arrays back
        int i = 0, j = 0, k = left;
        while (i < n1 && j < n2) {
            if (leftArr[i] <= rightArr[j]) {
                arr[k] = leftArr[i];
                i++;
            } else {
                arr[k] = rightArr[j];
                j++;
            }
            k++;
        }

        // Copy remaining elements
        while (i < n1) {
            arr[k] = leftArr[i];
            i++;
            k++;
        }
        while (j < n2) {
            arr[k] = rightArr[j];
            j++;
            k++;
        }
    }
}
```

### Execution trace for `[38, 27, 43, 3, 9, 82, 10]`

```
                    [38, 27, 43, 3, 9, 82, 10]
                   /                           \
          [38, 27, 43]                      [3, 9, 82, 10]
         /            \                    /               \
     [38, 27]        [43]             [3, 9]            [82, 10]
     /      \           \            /     \            /      \
   [38]    [27]        [43]       [3]    [9]         [82]    [10]
     \      /           /          \     /             \      /
     [27, 38]        [43]          [3, 9]             [10, 82]
         \            /              \                  /
          [27, 38, 43]               [3, 9, 10, 82]
                 \                      /
               [3, 9, 10, 27, 38, 43, 82]
```

## Time Complexity Analysis

**Recurrence:** T(n) = 2T(n/2) + O(n)

Using the Master Theorem: T(n) = O(n log n) in all cases (best, average, worst).

**Why O(n) for merge?** Merging two sorted arrays of total size n requires comparing and placing each element exactly once.

## Space Complexity: O(n)

Merge Sort requires O(n) auxiliary space because:
- At each level of recursion, temp arrays of total size O(n) are created
- Maximum depth is O(log n), but temp arrays from different branches don't coexist in memory
- The total auxiliary space at any point is O(n) (one level's merge)

### Space-optimized version (reuse single temp array)

```java
public static void sortOptimized(int[] arr) {
    int[] temp = new int[arr.length];
    mergeSortOptimized(arr, temp, 0, arr.length - 1);
}

private static void mergeSortOptimized(int[] arr, int[] temp, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSortOptimized(arr, temp, left, mid);
        mergeSortOptimized(arr, temp, mid + 1, right);
        mergeOptimized(arr, temp, left, mid, right);
    }
}

private static void mergeOptimized(int[] arr, int[] temp, int left, int mid, int right) {
    System.arraycopy(arr, left, temp, left, right - left + 1);

    int i = left, j = mid + 1, k = left;
    while (i <= mid && j <= right) {
        if (temp[i] <= temp[j]) {
            arr[k] = temp[i];
            i++;
        } else {
            arr[k] = temp[j];
            j++;
        }
        k++;
    }
    while (i <= mid) {
        arr[k] = temp[i];
        i++;
        k++;
    }
    // Elements from j to right are already in place
}
```

This allocates one temp array for the entire sort, reducing memory allocation overhead significantly.

## Stable Sorting Property

Merge Sort is **stable** — equal elements maintain their relative order. This is because we use `<=` in the comparison when taking from the left array. If we used `<`, it would be unstable.

```java
if (leftArr[i] <= rightArr[j])  // stable: equal elements come from left first (original order preserved)
```

## Applications

### Counting Inversions

An inversion is a pair `(i, j)` where `i < j` and `arr[i] > arr[j]`. Counting inversions measures how far an array is from sorted.

```java
public static long countInversions(int[] arr) {
    int[] temp = new int[arr.length];
    return mergeSortAndCount(arr, temp, 0, arr.length - 1);
}

private static long mergeSortAndCount(int[] arr, int[] temp, int left, int right) {
    long count = 0;
    if (left < right) {
        int mid = left + (right - left) / 2;
        count += mergeSortAndCount(arr, temp, left, mid);
        count += mergeSortAndCount(arr, temp, mid + 1, right);
        count += mergeAndCount(arr, temp, left, mid, right);
    }
    return count;
}

private static long mergeAndCount(int[] arr, int[] temp, int left, int mid, int right) {
    System.arraycopy(arr, left, temp, left, right - left + 1);

    int i = left, j = mid + 1, k = left;
    long count = 0;

    while (i <= mid && j <= right) {
        if (temp[i] <= temp[j]) {
            arr[k] = temp[i];
            i++;
        } else {
            arr[k] = temp[j];
            j++;
            // All remaining elements in left subarray (i..mid) are > temp[j]
            count += (mid - i + 1);
        }
        k++;
    }
    while (i <= mid) {
        arr[k] = temp[i];
        i++;
        k++;
    }
    return count;
}
```

**Key insight:** When `temp[i] > temp[j]`, then `temp[i]` through `temp[mid]` are all > `temp[j]` (since both halves are sorted). So `temp[j]` forms `mid - i + 1` inversions.

## In-Place Merge Sort Discussion

**Can we do merge sort in O(1) space?** Yes, but with trade-offs:

1. **In-place merge via rotation** — O(log n) space for recursion, O(n²) time. The merge step becomes O(n²) because shifting elements is costly.

2. **Block merge sort** (a.k.a. in-place merge sort) — O(n log n) time, O(1) space. Complex to implement, uses "block rotations." Few compilers actually use this.

3. **Practical stance:** The standard O(n) space is acceptable for most applications. The in-place variants are more of academic interest unless you're in an extremely memory-constrained environment.

## When to Use Merge Sort

| Use Case | Why |
|----------|-----|
| Need stable sort | ✅ Guaranteed stable |
| Linked lists | ✅ O(1) extra space for lists (no random access needed) |
| External sorting | ✅ Great for data on disk (sequential access) |
| Large data | ✅ O(n log n) guaranteed |
| Tight memory | ❌ Needs O(n) auxiliary space |
| In-place required | ❌ Use Heap Sort or Quick Sort instead |

## Practice Problems

| Problem | Platform | Notes |
|---------|----------|-------|
| Sort an Array | LeetCode 912 | Implement merge sort |
| Count Inversions | GeeksForGeeks | Classic merge sort application |
| Merge Two Sorted Arrays | LeetCode 88 | Core merge operation |
| Merge Sorted Array | LeetCode 88 | In-place merge (from end) |
| Sort List | LeetCode 148 | Merge sort on linked list |
| Reverse Pairs | LeetCode 493 | Count i < j and arr[i] > 2*arr[j] |
