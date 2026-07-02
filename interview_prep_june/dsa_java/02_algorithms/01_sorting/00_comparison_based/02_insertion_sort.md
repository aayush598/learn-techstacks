# Insertion Sort

## Concept

Insertion sort builds the sorted array one element at a time by picking an element and inserting it into its correct position among already sorted elements, shifting others to make room.

**Think of sorting a hand of playing cards.**

## Characteristics

| Property | Value |
|----------|-------|
| Time (Worst) | O(n²) — reverse sorted |
| Time (Average) | O(n²) |
| Time (Best) | O(n) — already sorted |
| Space | O(1) — in-place |
| Stable | Yes |
| Adaptive | Yes (O(n) for nearly sorted) |

## Implementation

```java
public class InsertionSort {
    public static void insertionSort(int[] arr) {
        int n = arr.length;

        for (int i = 1; i < n; i++) {
            int key = arr[i];     // Element to be inserted
            int j = i - 1;

            // Shift elements greater than key to the right
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }

            arr[j + 1] = key;     // Insert key at correct position
        }
    }
}
```

## How It Works (Step-by-Step)

```
Array: [12, 11, 13, 5, 6]

i=1, key=11: [11, 12, 13, 5, 6]  (12 shifted right)
i=2, key=13: [11, 12, 13, 5, 6]  (already in place)
i=3, key=5:  [5, 11, 12, 13, 6]   (11,12,13 shifted right)
i=4, key=6:  [5, 6, 11, 12, 13]   (11,12,13 shifted right)
```

## Binary Insertion Sort

Uses binary search to find the insertion position, reducing comparisons but still O(n²) due to shifting.

```java
public class BinaryInsertionSort {
    public static void binaryInsertionSort(int[] arr) {
        int n = arr.length;

        for (int i = 1; i < n; i++) {
            int key = arr[i];

            // Find insertion position using binary search
            int pos = findInsertPosition(arr, key, 0, i - 1);

            // Shift elements to make room
            for (int j = i - 1; j >= pos; j--) {
                arr[j + 1] = arr[j];
            }

            arr[pos] = key;
        }
    }

    // Binary search for insert position (first element > key)
    private static int findInsertPosition(int[] arr, int key, int low, int high) {
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] <= key) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return low;
    }
}
```

## Insertion Sort with Sentinel

Using a sentinel (smallest element at start) to eliminate bounds check:

```java
public class InsertionSortSentinel {
    public static void insertionSort(int[] arr) {
        int n = arr.length;

        // Find minimum and move it to first position (sentinel)
        int minIdx = 0;
        for (int i = 1; i < n; i++) {
            if (arr[i] < arr[minIdx]) {
                minIdx = i;
            }
        }
        // Swap min to position 0
        int temp = arr[0];
        arr[0] = arr[minIdx];
        arr[minIdx] = temp;

        // Now arr[0] is the smallest, so the inner loop
        // will always find arr[j] >= arr[0] and stop
        for (int i = 2; i < n; i++) {
            int key = arr[i];
            int j = i - 1;
            while (arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    }
}
```

## Why Insertion Sort is Used in Practice

Despite O(n²) worst case, insertion sort is widely used because:

1. **Adaptive:** O(n) for nearly sorted data — efficient for "online" sorting
2. **Fast for small n:** Low overhead makes it faster than O(n log n) sorts for n ≤ 20-50
3. **Stable:** Maintains relative order of equal elements
4. **In-place:** No extra memory needed
5. **Online:** Can sort as elements arrive

**This is why TimSort (used in Java's Arrays.sort() for objects) uses insertion sort for small subarrays.**

## Insertion Sort for Linked List

Insertion sort works naturally with linked lists (no shifting needed, just pointer manipulation):

```java
public class InsertionSortLinkedList {
    static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    public static ListNode insertionSortList(ListNode head) {
        if (head == null || head.next == null) return head;

        ListNode dummy = new ListNode(0);
        dummy.next = head;
        ListNode lastSorted = head;
        ListNode curr = head.next;

        while (curr != null) {
            if (lastSorted.val <= curr.val) {
                // curr is already in correct position
                lastSorted = curr;
            } else {
                // Find where to insert curr
                ListNode prev = dummy;
                while (prev.next.val <= curr.val) {
                    prev = prev.next;
                }

                // Insert curr between prev and prev.next
                lastSorted.next = curr.next;
                curr.next = prev.next;
                prev.next = curr;
            }

            curr = lastSorted.next;
        }

        return dummy.next;
    }
}
```

## Complete Demo

```java
public class InsertionSortDemo {
    public static void main(String[] args) {
        // Regular insertion sort
        int[] arr1 = {12, 11, 13, 5, 6};
        InsertionSort.insertionSort(arr1);
        System.out.println("Regular: " + Arrays.toString(arr1));

        // Binary insertion sort
        int[] arr2 = {12, 11, 13, 5, 6};
        BinaryInsertionSort.binaryInsertionSort(arr2);
        System.out.println("Binary:  " + Arrays.toString(arr2));

        // Performance: insertion sort vs O(n log n) for small n
        int[] small = {5, 3, 1, 4, 2};
        System.out.println("\nSmall array: " + Arrays.toString(small));
        InsertionSort.insertionSort(small);
        System.out.println("Sorted: " + Arrays.toString(small));

        // Nearly sorted performance
        int[] nearlySorted = {1, 2, 3, 5, 4, 6, 7, 8, 9, 10};
        System.out.println("\nNearly sorted: " + Arrays.toString(nearlySorted));
        long start = System.nanoTime();
        InsertionSort.insertionSort(nearlySorted);
        long end = System.nanoTime();
        System.out.println("Time: " + (end - start) + "ns (O(n) for nearly sorted)");

        // Reverse sorted (worst case)
        int[] reverseSorted = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
        System.out.println("\nReverse sorted: " + Arrays.toString(reverseSorted));
        start = System.nanoTime();
        InsertionSort.insertionSort(reverseSorted);
        end = System.nanoTime();
        System.out.println("Time: " + (end - start) + "ns (O(n²) for reverse)");
    }
}
```

## Comparison of O(n²) Sorts

| Property | Bubble Sort | Selection Sort | Insertion Sort |
|----------|------------|---------------|----------------|
| Comparisons | n²/2 | n²/2 | n²/4 (avg) |
| Swaps | n²/2 | n | n²/4 |
| Stable | Yes | No | Yes |
| Adaptive | Yes (optimized) | No | Yes |
| Good for | Teaching | Minimal swaps | Small/nearly sorted |

## Key Points

| Aspect | Detail |
|--------|--------|
| Online | Yes — can sort while receiving elements |
| Adaptive | O(n) for sorted, O(n²) for reverse sorted |
| Stable | Yes — `>` not `>=` in comparison |
| In-place | Yes — O(1) extra space |
| When to use | n ≤ 50, nearly sorted data, as subroutine |

**Insertion sort is the default choice for small arrays and is a key component of TimSort and introspective sort algorithms used in production systems.**
