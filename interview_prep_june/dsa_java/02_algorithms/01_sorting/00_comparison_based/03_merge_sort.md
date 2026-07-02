# Merge Sort

## Concept

Merge sort is a divide-and-conquer algorithm that splits the array into halves, recursively sorts each half, then merges the sorted halves back together.

1. **Divide:** Split array into two halves
2. **Conquer:** Recursively sort each half
3. **Combine:** Merge the two sorted halves

## Characteristics

| Property | Value |
|----------|-------|
| Time (All cases) | O(n log n) |
| Space | O(n) — auxiliary array for merging |
| Stable | Yes |
| In-place | No (needs O(n) extra space) |
| Divide and conquer | Yes |

## Implementation

```java
public class MergeSort {
    public static void mergeSort(int[] arr) {
        if (arr.length < 2) return;
        mergeSort(arr, 0, arr.length - 1);
    }

    private static void mergeSort(int[] arr, int left, int right) {
        if (left >= right) return;

        int mid = left + (right - left) / 2;

        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }

    private static void merge(int[] arr, int left, int mid, int right) {
        // Create temporary arrays
        int n1 = mid - left + 1;
        int n2 = right - mid;

        int[] leftArr = new int[n1];
        int[] rightArr = new int[n2];

        // Copy data
        System.arraycopy(arr, left, leftArr, 0, n1);
        System.arraycopy(arr, mid + 1, rightArr, 0, n2);

        // Merge
        int i = 0, j = 0, k = left;

        while (i < n1 && j < n2) {
            if (leftArr[i] <= rightArr[j]) {
                arr[k++] = leftArr[i++];
            } else {
                arr[k++] = rightArr[j++];
            }
        }

        // Copy remaining elements
        while (i < n1) arr[k++] = leftArr[i++];
        while (j < n2) arr[k++] = rightArr[j++];
    }
}
```

## Single Auxiliary Array Optimization

Instead of creating new arrays in every merge call, use a single auxiliary array:

```java
public class MergeSortOptimized {
    public static void mergeSort(int[] arr) {
        if (arr.length < 2) return;
        int[] temp = new int[arr.length];
        mergeSort(arr, temp, 0, arr.length - 1);
    }

    private static void mergeSort(int[] arr, int[] temp, int left, int right) {
        if (left >= right) return;

        int mid = left + (right - left) / 2;
        mergeSort(arr, temp, left, mid);
        mergeSort(arr, temp, mid + 1, right);
        merge(arr, temp, left, mid, right);
    }

    private static void merge(int[] arr, int[] temp, int left, int mid, int right) {
        // Copy to temp
        System.arraycopy(arr, left, temp, left, right - left + 1);

        int i = left;
        int j = mid + 1;
        int k = left;

        while (i <= mid && j <= right) {
            if (temp[i] <= temp[j]) {
                arr[k++] = temp[i++];
            } else {
                arr[k++] = temp[j++];
            }
        }

        while (i <= mid) arr[k++] = temp[i++];
        // No need to copy right half — it's already in place
    }
}
```

## Bottom-Up Iterative Merge Sort

Instead of recursion, merge subarrays of size 1, 2, 4, 8, ...:

```java
public class MergeSortIterative {
    public static void mergeSort(int[] arr) {
        int n = arr.length;
        int[] temp = new int[n];

        // Merge subarrays of increasing size
        for (int size = 1; size < n; size *= 2) {
            for (int left = 0; left < n - size; left += 2 * size) {
                int mid = left + size - 1;
                int right = Math.min(left + 2 * size - 1, n - 1);
                merge(arr, temp, left, mid, right);
            }
        }
    }

    private static void merge(int[] arr, int[] temp, int left, int mid, int right) {
        System.arraycopy(arr, left, temp, left, right - left + 1);

        int i = left, j = mid + 1, k = left;

        while (i <= mid && j <= right) {
            arr[k++] = temp[i] <= temp[j] ? temp[i++] : temp[j++];
        }
        while (i <= mid) arr[k++] = temp[i++];
    }
}
```

## In-Place Merge Sort Discussion

True in-place merge sort (O(1) space) is complex and not used in practice:

```java
public class MergeSortInPlace {
    // In-place merge using rotation (O(n²) worst-case)
    // Only for understanding — not practically useful

    public static void mergeSort(int[] arr) {
        mergeSort(arr, 0, arr.length - 1);
    }

    private static void mergeSort(int[] arr, int left, int right) {
        if (left >= right) return;

        int mid = left + (right - left) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        mergeInPlace(arr, left, mid, right);
    }

    private static void mergeInPlace(int[] arr, int left, int mid, int right) {
        int i = left;
        int j = mid + 1;

        while (i <= mid && j <= right) {
            if (arr[i] <= arr[j]) {
                i++;
            } else {
                // Rotate element at j into position i
                int temp = arr[j];
                for (int k = j; k > i; k--) {
                    arr[k] = arr[k - 1];
                }
                arr[i] = temp;
                i++;
                mid++;
                j++;
            }
        }
    }
}
```

**Note:** In-place merge is O(n²) in the worst case, defeating the purpose. Use the O(n) auxiliary space version.

## Application: Counting Inversions

Counting inversions (i < j and arr[i] > arr[j]) using merge sort modification:

```java
public class InversionCount {
    public static long countInversions(int[] arr) {
        int[] temp = new int[arr.length];
        return countInversions(arr, temp, 0, arr.length - 1);
    }

    private static long countInversions(int[] arr, int[] temp, int left, int right) {
        long inversions = 0;

        if (left < right) {
            int mid = left + (right - left) / 2;

            inversions += countInversions(arr, temp, left, mid);
            inversions += countInversions(arr, temp, mid + 1, right);
            inversions += mergeAndCount(arr, temp, left, mid, right);
        }

        return inversions;
    }

    private static long mergeAndCount(int[] arr, int[] temp, int left, int mid, int right) {
        System.arraycopy(arr, left, temp, left, right - left + 1);

        int i = left;
        int j = mid + 1;
        int k = left;
        long inversions = 0;

        while (i <= mid && j <= right) {
            if (temp[i] <= temp[j]) {
                arr[k++] = temp[i++];
            } else {
                // All remaining elements in left half (i..mid) are > temp[j]
                inversions += (mid - i + 1);
                arr[k++] = temp[j++];
            }
        }

        while (i <= mid) arr[k++] = temp[i++];
        while (j <= right) arr[k++] = temp[j++];

        return inversions;
    }

    public static void main(String[] args) {
        int[] arr = {1, 20, 6, 4, 5};
        System.out.println("Inversions: " + countInversions(arr));
        // Output: 5
        // Pairs: (20,6), (20,4), (20,5), (6,4), (6,5)
    }
}
```

## Merge Sort on Linked List

Merge sort is the preferred O(n log n) sort for linked lists (no random access needed):

```java
public class MergeSortLinkedList {
    static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    public static ListNode mergeSort(ListNode head) {
        if (head == null || head.next == null) return head;

        // Find middle
        ListNode mid = findMiddle(head);
        ListNode midNext = mid.next;
        mid.next = null;

        // Recursively sort
        ListNode left = mergeSort(head);
        ListNode right = mergeSort(midNext);

        // Merge
        return merge(left, right);
    }

    private static ListNode findMiddle(ListNode head) {
        ListNode slow = head;
        ListNode fast = head.next;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }

    private static ListNode merge(ListNode left, ListNode right) {
        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;

        while (left != null && right != null) {
            if (left.val <= right.val) {
                curr.next = left;
                left = left.next;
            } else {
                curr.next = right;
                right = right.next;
            }
            curr = curr.next;
        }

        if (left != null) curr.next = left;
        if (right != null) curr.next = right;

        return dummy.next;
    }
}
```

## Complete Demo

```java
public class MergeSortDemo {
    public static void main(String[] args) {
        int[] arr = {38, 27, 43, 3, 9, 82, 10};

        System.out.println("Original: " + Arrays.toString(arr));

        // Standard recursive
        int[] arr1 = arr.clone();
        MergeSort.mergeSort(arr1);
        System.out.println("Standard: " + Arrays.toString(arr1));

        // Optimized (single temp array)
        int[] arr2 = arr.clone();
        MergeSortOptimized.mergeSort(arr2);
        System.out.println("Optimized: " + Arrays.toString(arr2));

        // Iterative
        int[] arr3 = arr.clone();
        MergeSortIterative.mergeSort(arr3);
        System.out.println("Iterative: " + Arrays.toString(arr3));

        // Inversion count
        int[] arr4 = {1, 20, 6, 4, 5};
        System.out.println("\nInversions in " + Arrays.toString(arr4) +
            ": " + InversionCount.countInversions(arr4));
    }
}
```

## Complexity Analysis

| Step | Time |
|------|------|
| Dividing | O(log n) levels |
| Merging at each level | O(n) |
| Total | O(n log n) |
| Space (auxiliary) | O(n) |

### Why O(n log n)?

```
Level 0:    1 merge of size n     → n operations
Level 1:    2 merges of size n/2   → n operations
Level 2:    4 merges of size n/4   → n operations
...
Level k:    n/2^k merges of size 2 → n operations
Levels: log₂ n → Total: n * log₂ n
```

## Key Points

| Aspect | Detail |
|--------|--------|
| Guaranteed O(n log n) | Always, regardless of input |
| Stable | Equal elements maintain order |
| Extra space | O(n) — main drawback |
| Preferred for | Linked lists, external sorting, stability-critical |
| Cache performance | Poorer than quicksort due to extra memory accesses |

**Merge sort is the safest O(n log n) sort — no worst-case pitfalls, stable, and predictable. It's the default for object sorting in Java and for sorting linked lists.**
