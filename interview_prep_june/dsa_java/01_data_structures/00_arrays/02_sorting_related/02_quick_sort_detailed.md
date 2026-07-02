# Quick Sort — Detailed

## Partition Schemes

### Lomuto Partition Scheme (Simpler, Less Efficient)

Picks the last element as pivot. Scans left to right, maintaining a boundary of elements ≤ pivot.

```java
public static int lomutoPartition(int[] arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1; // index of smaller element

    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(arr, i, j);
        }
    }
    swap(arr, i + 1, high); // place pivot at correct position
    return i + 1; // return pivot index
}
```

### Hoare Partition Scheme (More Efficient)

Picks the first element as pivot. Two pointers from both ends move toward each other.

```java
public static int hoarePartition(int[] arr, int low, int high) {
    int pivot = arr[low];
    int i = low - 1, j = high + 1;

    while (true) {
        do {
            i++;
        } while (arr[i] < pivot);

        do {
            j--;
        } while (arr[j] > pivot);

        if (i >= j) return j;
        swap(arr, i, j);
    }
}
```

### Lomuto vs Hoare

| Aspect | Lomuto | Hoare |
|--------|--------|-------|
| Pivot choice | Usually last element | Usually first element |
| Swaps | More (about 3× more) | Fewer |
| Avg comparisons | Same O(n log n) | Same O(n log n) |
| Equal elements | Degrades (many swaps) | Better |
| Return value | Returns final pivot index | Returns partition index (pivot not necessarily placed) |
| Use in Quick Sort | Both work; adjust recursion accordingly |

## Full Implementation with Lomuto

```java
public class QuickSortLomuto {
    public static void sort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }

    private static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = lomutoPartition(arr, low, high);
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
}
```

## Full Implementation with Hoare

```java
public class QuickSortHoare {
    public static void sort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }

    private static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = hoarePartition(arr, low, high);
            quickSort(arr, low, pivotIndex);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
}
```

**Key difference with Hoare:** The recursion is `(low, pivotIndex)` and `(pivotIndex + 1, high)`, NOT `(low, pivotIndex - 1)`. Hoare partitions elements into two groups: ≤ pivot and ≥ pivot. The pivot may end up anywhere in the left group.

## Pivot Selection Strategies

### First element (bad for sorted arrays)

```java
int pivot = arr[low]; // O(n²) for sorted input
```

### Last element (bad for sorted arrays)

```java
int pivot = arr[high]; // O(n²) for sorted input
```

### Middle element (better)

```java
int pivot = arr[low + (high - low) / 2]; // often good
```

### Random pivot (avoids worst-case in practice)

```java
int randomIndex = low + (int)(Math.random() * (high - low + 1));
swap(arr, randomIndex, high); // move pivot to end for Lomuto
int pivot = arr[high];
```

### Median-of-three (guards against nearly sorted)

```java
private static int medianOfThree(int[] arr, int low, int high) {
    int mid = low + (high - low) / 2;
    if (arr[mid] < arr[low]) swap(arr, low, mid);
    if (arr[high] < arr[low]) swap(arr, low, high);
    if (arr[high] < arr[mid]) swap(arr, mid, high);
    // Now arr[low] <= arr[mid] <= arr[high]
    // Use mid as pivot
    swap(arr, mid, high); // move to end for Lomuto
    return arr[high];
}
```

## Worst-Case O(n²) and How to Avoid

Quick Sort's worst case occurs when the partition always picks the smallest or largest element as pivot:
- Already sorted array + first/last element pivot
- All equal elements (Lomuto degrades)

**Avoidance strategies:**

1. **Random pivot** — probability of consistently picking min/max is 1/(2^n), essentially zero
2. **Median-of-three** — protect against sorted input
3. **Introsort** (used in C++ std::sort) — switch to Heap Sort when recursion depth exceeds log n
4. **3-way partition** (Dutch National Flag) — handles equal elements efficiently

### Three-way Quick Sort (for arrays with many duplicates)

```java
private static void quickSort3Way(int[] arr, int low, int high) {
    if (low >= high) return;

    int pivot = arr[low];
    int lt = low;  // arr[low..lt-1] < pivot
    int gt = high; // arr[gt+1..high] > pivot
    int i = low + 1;

    while (i <= gt) {
        if (arr[i] < pivot) {
            swap(arr, i, lt);
            lt++;
            i++;
        } else if (arr[i] > pivot) {
            swap(arr, i, gt);
            gt--;
        } else {
            i++;
        }
    }

    quickSort3Way(arr, low, lt - 1);
    quickSort3Way(arr, gt + 1, high);
}
```

**How this works:** Three pointers partition the array into three zones: less than pivot, equal to pivot, greater than pivot. Elements equal to the pivot are already in their final position, reducing the recursion depth.

## Space Complexity: O(log n) for Stack

Quick Sort uses O(log n) extra space for the **call stack** in the average case. In the worst case (already sorted), it uses O(n) stack space — but this is avoided with random pivoting.

**Optimization:** Always recurse on the smaller partition first (tail recursion elimination):

```java
private static void quickSortOptimized(int[] arr, int low, int high) {
    while (low < high) {
        int pivotIndex = partition(arr, low, high);
        if (pivotIndex - low < high - pivotIndex) {
            quickSortOptimized(arr, low, pivotIndex - 1);
            low = pivotIndex + 1; // tail call elimination
        } else {
            quickSortOptimized(arr, pivotIndex + 1, high);
            high = pivotIndex - 1;
        }
    }
}
```

This guarantees O(log n) stack space in the worst case.

## Quick Select: Kth Smallest in O(n) Average

Quick Select uses partitioning to find the kth smallest element without fully sorting.

```java
public static int quickSelect(int[] arr, int k) {
    if (k < 0 || k >= arr.length) throw new IllegalArgumentException();
    return quickSelect(arr, 0, arr.length - 1, k);
}

private static int quickSelect(int[] arr, int low, int high, int k) {
    if (low == high) return arr[low];

    int pivotIndex = lomutoPartition(arr, low, high);

    if (pivotIndex == k) {
        return arr[pivotIndex];
    } else if (k < pivotIndex) {
        return quickSelect(arr, low, pivotIndex - 1, k);
    } else {
        return quickSelect(arr, pivotIndex + 1, high, k);
    }
}
```

### Why O(n) average?

The recurrence is T(n) = T(n/2) + O(n), which solves to T(n) = O(n). Unlike QuickSort, Quick Select only recurses on one side. The worst case is still O(n²) (same as QuickSort), but randomized pivot makes this extremely unlikely.

**Time:** Average O(n), Worst O(n²).
**Space:** O(log n) for the stack (or O(1) with iterative implementation).

## Quick Sort vs Merge Sort

| Aspect | Quick Sort | Merge Sort |
|--------|------------|------------|
| Time (avg) | O(n log n) | O(n log n) |
| Time (worst) | O(n²) | O(n log n) |
| Space | O(log n) | O(n) |
| Stable | No | Yes |
| Cache-friendly | Yes (sequential access) | Yes (merge is sequential) |
| Linked lists | Poor (random access needed) | Excellent |

## Practice Problems

| Problem | Platform | Notes |
|---------|----------|-------|
| Sort an Array | LeetCode 912 | Implement QuickSort |
| Kth Largest Element | LeetCode 215 | Quick Select |
| K Closest Points to Origin | LeetCode 973 | Quick Select |
| Wiggle Sort II | LeetCode 324 | Quick Select for median |
| Sort Colors | LeetCode 75 | Three-way partition |
| Quick Sort on Linked List | - | Tricky, use merge sort instead |

## Common Mistakes

1. **Infinite recursion with Lomuto** — forgetting `if (low < high)` base case
2. **Hoare infinite loop with equal elements** — using `<=` instead of `<` in inner loops
3. **Wrong recursion bounds with Hoare** — using `(low, pivotIndex - 1)` instead of `(low, pivotIndex)`
4. **Stack overflow on sorted array** — using first/last pivot without randomization
5. **Quick Select off-by-one** — confusing 0-indexed and 1-indexed k
