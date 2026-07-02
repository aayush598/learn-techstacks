# TimSort and Shell Sort

## 1. TimSort

### Overview

TimSort is a **hybrid stable sorting algorithm** derived from merge sort and insertion sort. It was designed by Tim Peters in 2002 for Python's sort, and is now used in:
- **Java** `Arrays.sort()` for objects
- **Python** `list.sort()`
- **JavaScript** V8 engine

### Key Concepts

1. **Runs:** Find naturally occurring sorted (or reverse sorted) subsequences
2. **Galloping mode:** Binary search-based merging optimization
3. **Insertion sort:** Used for small runs (n ≤ 32-64)

### Understanding Runs

```java
public class TimSortConcepts {
    // A "run" is a contiguous subsequence that is:
    // - Non-decreasing: a[i] <= a[i+1] <= a[i+2] ...
    // - Strictly decreasing: a[i] > a[i+1] (reversed later)

    public static int findRun(int[] arr, int start) {
        int n = arr.length;
        if (start >= n - 1) return start;

        boolean increasing = arr[start] <= arr[start + 1];
        int end = start + 1;

        if (increasing) {
            while (end < n - 1 && arr[end] <= arr[end + 1]) {
                end++;
            }
        } else {
            while (end < n - 1 && arr[end] > arr[end + 1]) {
                end++;
            }
            // Reverse the decreasing run
            reverse(arr, start, end);
        }

        return end;
    }

    private static void reverse(int[] arr, int start, int end) {
        while (start < end) {
            int temp = arr[start];
            arr[start] = arr[end];
            arr[end] = temp;
            start++;
            end--;
        }
    }
}
```

### Minimal Run Length

Timsort computes a minimum run length (usually 32-64) to ensure efficient merging. If a run is shorter, it's extended using insertion sort.

```java
public class TimSortMinRun {
    // Compute minimum run length for n elements
    public static int minRunLength(int n) {
        int r = 0;
        while (n >= 64) {
            r |= (n & 1);
            n >>= 1;
        }
        return n + r;
    }
}
```

### Galloping Mode

When merging two runs, if one run's elements are consistently smaller, Timsort enters "galloping mode" — using binary search to find the insertion range in batches.

```java
public class GallopingMerge {
    // Galloping: when an element from run A wins 7 times in a row,
    // switch to binary search to find how many from run B are smaller

    public static void mergeWithGalloping(int[] arr, int left, int mid, int right) {
        int[] leftArr = Arrays.copyOfRange(arr, left, mid + 1);
        int[] rightArr = Arrays.copyOfRange(arr, mid + 1, right + 1);

        int i = 0, j = 0, k = left;
        int leftWins = 0;
        int GALLOP_THRESHOLD = 7;

        while (i < leftArr.length && j < rightArr.length) {
            if (leftArr[i] <= rightArr[j]) {
                arr[k++] = leftArr[i++];
                leftWins++;
                if (leftWins >= GALLOP_THRESHOLD) {
                    // Gallop: binary search to copy multiple elements
                    int gallopIdx = gallopLeft(leftArr, rightArr[j], i);
                    while (i < gallopIdx) {
                        arr[k++] = leftArr[i++];
                    }
                    leftWins = 0;
                }
            } else {
                arr[k++] = rightArr[j++];
                leftWins = 0;
            }
        }

        while (i < leftArr.length) arr[k++] = leftArr[i++];
        while (j < rightArr.length) arr[k++] = rightArr[j++];
    }

    private static int gallopLeft(int[] arr, int key, int start) {
        // Binary search for insertion point
        int low = start, high = arr.length;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] < key) low = mid + 1;
            else high = mid;
        }
        return low;
    }
}
```

### Simplified TimSort Implementation

```java
public class SimpleTimSort {
    private static final int MIN_MERGE = 32;

    public static void timSort(int[] arr) {
        int n = arr.length;
        if (n < 2) return;

        // Identify runs and sort them
        for (int i = 0; i < n; i += MIN_MERGE) {
            int end = Math.min(i + MIN_MERGE - 1, n - 1);
            insertionSort(arr, i, end);
        }

        // Merge runs
        for (int size = MIN_MERGE; size < n; size *= 2) {
            for (int left = 0; left < n; left += 2 * size) {
                int mid = left + size - 1;
                int right = Math.min(left + 2 * size - 1, n - 1);

                if (mid < right) {
                    merge(arr, left, mid, right);
                }
            }
        }
    }

    private static void insertionSort(int[] arr, int left, int right) {
        for (int i = left + 1; i <= right; i++) {
            int key = arr[i];
            int j = i - 1;
            while (j >= left && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    }

    private static void merge(int[] arr, int left, int mid, int right) {
        int[] temp = Arrays.copyOfRange(arr, left, mid + 1);
        int i = 0, j = mid + 1, k = left;

        while (i < temp.length && j <= right) {
            arr[k++] = temp[i] <= arr[j] ? temp[i++] : arr[j++];
        }
        while (i < temp.length) arr[k++] = temp[i++];
    }
}
```

## 2. Shell Sort

### Overview

Shell sort is an **in-place comparison sort** that generalizes insertion sort by allowing the exchange of far-apart elements (gap-based). It starts with a large gap and reduces it.

### Key Concepts

1. **Gap sequence:** The gap determines which elements are compared
2. **Insertion sort with gaps:** Each pass does an insertion sort on elements separated by `gap`
3. **Final pass:** gap = 1 is a standard insertion sort, but the array is now nearly sorted

### Implementation with Knuth's Sequence

```java
public class ShellSort {
    public static void shellSort(int[] arr) {
        int n = arr.length;

        // Find initial gap using Knuth's formula: (3^k - 1) / 2
        // Produces gaps: 1, 4, 13, 40, 121, 364, ...
        int gap = 1;
        while (gap < n / 3) {
            gap = 3 * gap + 1;
        }

        // Reduce gap and do insertion sort
        while (gap >= 1) {
            for (int i = gap; i < n; i++) {
                int temp = arr[i];
                int j = i;

                while (j >= gap && arr[j - gap] > temp) {
                    arr[j] = arr[j - gap];
                    j -= gap;
                }

                arr[j] = temp;
            }

            gap /= 3;  // Knuth's shrink factor
        }
    }
}
```

### Original Shell's Sequence (1959)

```java
public class ShellSortOriginal {
    public static void shellSort(int[] arr) {
        int n = arr.length;

        // Original: n/2, n/4, n/8, ..., 1
        for (int gap = n / 2; gap > 0; gap /= 2) {
            for (int i = gap; i < n; i++) {
                int temp = arr[i];
                int j = i;

                while (j >= gap && arr[j - gap] > temp) {
                    arr[j] = arr[j - gap];
                    j -= gap;
                }

                arr[j] = temp;
            }
        }
    }
}
```

### Various Gap Sequences

```java
public class GapSequences {
    // Shell's original: n/2, n/4, ..., 1 — O(n²) worst
    public static int[] shellGaps(int n) {
        List<Integer> gaps = new ArrayList<>();
        for (int gap = n / 2; gap > 0; gap /= 2) {
            gaps.add(gap);
        }
        return gaps.stream().mapToInt(i -> i).toArray();
    }

    // Knuth's: (3^k - 1) / 2 — O(n^(3/2)) worst
    public static int[] knuthGaps(int n) {
        List<Integer> gaps = new ArrayList<>();
        int gap = 1;
        while (gap < n) {
            gaps.add(gap);
            gap = 3 * gap + 1;
        }
        Collections.reverse(gaps);
        return gaps.stream().mapToInt(i -> i).toArray();
    }

    // Hibbard's: 2^k - 1 — O(n^(3/2)) worst
    public static int[] hibbardGaps(int n) {
        List<Integer> gaps = new ArrayList<>();
        int gap = 1;
        while (gap < n) {
            gaps.add(gap);
            gap = 2 * gap + 1;
        }
        Collections.reverse(gaps);
        return gaps.stream().mapToInt(i -> i).toArray();
    }

    // Sedgewick's: 4^k + 3*2^(k-1) + 1 — O(n^(4/3)) worst
    public static int[] sedgewickGaps(int n) {
        List<Integer> gaps = new ArrayList<>();
        gaps.add(1);
        int i = 0;
        while (true) {
            int gap = (int) (Math.pow(4, i) + 3 * Math.pow(2, i - 1) + 1);
            if (gap >= n) break;
            gaps.add(gap);
            i++;
        }
        Collections.reverse(gaps);
        return gaps.stream().mapToInt(g -> g).toArray();
    }
}
```

## Complete Demo

```java
public class TimShellDemo {
    public static void main(String[] args) {
        int[] arr = {5, 2, 8, 1, 9, 4, 7, 3, 6};

        System.out.println("Original: " + Arrays.toString(arr));

        // Shell sort (Knuth)
        int[] arr1 = arr.clone();
        ShellSort.shellSort(arr1);
        System.out.println("Shell (Knuth): " + Arrays.toString(arr1));

        // Simple TimSort
        int[] arr2 = arr.clone();
        SimpleTimSort.timSort(arr2);
        System.out.println("TimSort (simple): " + Arrays.toString(arr2));

        // Compare gap sequences
        System.out.println("\nShell sort gap sequences for n=100:");

        int[] testArr = generateRandomArray(10000);

        long start = System.nanoTime();
        ShellSortOriginal.shellSort(testArr.clone());
        System.out.println("Original gaps: " + (System.nanoTime() - start) / 1e6 + "ms");

        start = System.nanoTime();
        ShellSort.shellSort(testArr.clone());
        System.out.println("Knuth gaps: " + (System.nanoTime() - start) / 1e6 + "ms");
    }

    private static int[] generateRandomArray(int n) {
        Random rand = new Random(42);
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = rand.nextInt();
        return arr;
    }
}
```

## Performance Comparison

| Algorithm | Time (Worst) | Time (Avg) | Space | Stable |
|-----------|-------------|------------|-------|--------|
| Shell (Shell gaps) | O(n²) | O(n^(3/2)) | O(1) | No |
| Shell (Knuth gaps) | O(n^(3/2)) | O(n^(5/4)) | O(1) | No |
| Shell (Sedgewick) | O(n^(4/3)) | O(n^(7/6)) | O(1) | No |
| TimSort | O(n log n) | O(n log n) | O(n) | Yes |

## When to Use

| Use Case | Algorithm |
|----------|-----------|
| Sorting objects in Java | TimSort (Arrays.sort() for objects) |
| Sorting primitives | Dual-pivot QuickSort (Arrays.sort() for primitives) |
| Nearly sorted data | TimSort (O(n) for already sorted) |
| Learning sorting | Shell sort (easy to understand, decent performance) |
| Embedded/low memory | Shell sort (in-place, no recursion) |

## Key Takeaways

- **TimSort** is the standard for object sorting in Java, Python, and JavaScript. It exploits existing order in data.
- **Shell sort** is a good middle ground between simpler O(n²) sorts and advanced O(n log n) sorts. It's a good choice when code size matters and O(n log n) isn't strictly required.
- Both are **adaptive** — they perform better on partially sorted data.
