# Heap Sort

## Concept

Heap sort uses a binary heap data structure:
1. **Build a max-heap** from the array (heapify)
2. **Repeatedly extract the maximum** element and place it at the end, reducing heap size

## Characteristics

| Property | Value |
|----------|-------|
| Time (All cases) | O(n log n) |
| Space | O(1) — in-place |
| Stable | No |
| Adaptive | No |

## Implementation

```java
public class HeapSort {
    public static void heapSort(int[] arr) {
        int n = arr.length;

        // Step 1: Build max-heap (heapify the array)
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }

        // Step 2: Extract elements one by one
        for (int i = n - 1; i > 0; i--) {
            // Move current root (max) to end
            swap(arr, 0, i);

            // Heapify the reduced heap
            heapify(arr, i, 0);
        }
    }

    // Heapify subtree rooted at index i
    // n = size of heap
    private static void heapify(int[] arr, int n, int i) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        // Find largest among root, left child, right child
        if (left < n && arr[left] > arr[largest]) {
            largest = left;
        }

        if (right < n && arr[right] > arr[largest]) {
            largest = right;
        }

        // If largest is not root, swap and continue heapifying
        if (largest != i) {
            swap(arr, i, largest);
            heapify(arr, n, largest);
        }
    }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

## Step-by-Step Example

```
Array: [4, 10, 3, 5, 1]

Step 1: Build max-heap
    4             10             10
   / \           / \            / \
  10  3    →    4   3    →     5   3
 / \           / \            / \
5   1         5   1          4   1

Step 2: Extract max repeatedly
Swap root (10) with last → [1, 5, 3, 4, 10], heapify
    5             4
   / \           / \
  1   3    →    1   3
 /
4

Swap root (5) with last → [4, 1, 3, 5, 10], heapify
    4
   / \
  1   3

Swap root (4) with last → [3, 1, 4, 5, 10], heapify
    3
   /
  1

Swap root (3) with last → [1, 3, 4, 5, 10]

Result: [1, 3, 4, 5, 10]
```

## Iterative Heapify (Non-Recursive)

```java
public class HeapSortIterative {
    public static void heapSort(int[] arr) {
        int n = arr.length;

        // Build max-heap
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapifyIterative(arr, n, i);
        }

        // Extract elements
        for (int i = n - 1; i > 0; i--) {
            swap(arr, 0, i);
            heapifyIterative(arr, i, 0);
        }
    }

    private static void heapifyIterative(int[] arr, int n, int i) {
        while (true) {
            int largest = i;
            int left = 2 * i + 1;
            int right = 2 * i + 2;

            if (left < n && arr[left] > arr[largest]) {
                largest = left;
            }

            if (right < n && arr[right] > arr[largest]) {
                largest = right;
            }

            if (largest == i) break;

            swap(arr, i, largest);
            i = largest;
        }
    }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

## Building Heap: O(n) Analysis

Building a max-heap from an array of size n using heapify from n/2 down to 0 is O(n), not O(n log n).

**Why?** Most elements are near the bottom and only move a few levels:
- n/2 nodes are leaves (level 0 moves)
- n/4 nodes can move at most 1 level
- n/8 nodes can move at most 2 levels
- ...

Total: n/2 * 0 + n/4 * 1 + n/8 * 2 + ... = n * Σ(i/2^i) = n * 2 = O(n)

## Partial Sort Using Heap

Heap sort can be used to find the k largest/smallest elements:

```java
public class PartialHeapSort {
    // Find k largest elements (using min-heap)
    public static int[] findKLargest(int[] arr, int k) {
        if (k <= 0 || k > arr.length) throw new IllegalArgumentException();

        // Build min-heap of first k elements
        PriorityQueue<Integer> minHeap = new PriorityQueue<>(k);
        for (int i = 0; i < k; i++) {
            minHeap.offer(arr[i]);
        }

        // Process remaining elements
        for (int i = k; i < arr.length; i++) {
            if (arr[i] > minHeap.peek()) {
                minHeap.poll();
                minHeap.offer(arr[i]);
            }
        }

        // Extract in sorted order
        int[] result = new int[k];
        for (int i = 0; i < k; i++) {
            result[i] = minHeap.poll();
        }
        return result;
    }

    // Sort first k elements completely (heap sort partial)
    public static void partiallySort(int[] arr, int k) {
        int n = Math.min(k, arr.length);

        // Build max-heap of first n elements from whole array
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }

        for (int i = n - 1; i > 0; i--) {
            swap(arr, 0, i);
            heapify(arr, i, 0);
        }
    }

    private static void heapify(int[] arr, int n, int i) {
        // Same as HeapSort.heapify
    }

    private static void swap(int[] arr, int i, int j) {
        // Same as HeapSort.swap
    }
}
```

## Complete Demo

```java
public class HeapSortDemo {
    public static void main(String[] args) {
        int[] arr = {4, 10, 3, 5, 1};

        System.out.println("Original: " + Arrays.toString(arr));

        // Standard heap sort
        int[] arr1 = arr.clone();
        HeapSort.heapSort(arr1);
        System.out.println("Sorted:   " + Arrays.toString(arr1));

        // Iterative heapify
        int[] arr2 = arr.clone();
        HeapSortIterative.heapSort(arr2);
        System.out.println("Iterative: " + Arrays.toString(arr2));

        // Performance comparison: heap sort vs quick sort
        int[] largeArr = new int[100000];
        Random rand = new Random(42);
        for (int i = 0; i < largeArr.length; i++) {
            largeArr[i] = rand.nextInt();
        }

        int[] heapArr = largeArr.clone();
        long start = System.currentTimeMillis();
        HeapSort.heapSort(heapArr);
        long heapTime = System.currentTimeMillis() - start;
        System.out.println("\nHeap sort time: " + heapTime + "ms");

        // Find k largest
        int[] sample = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5};
        System.out.println("\n3 largest in " + Arrays.toString(sample) + ": " +
            Arrays.toString(PartialHeapSort.findKLargest(sample, 3)));
    }
}
```

## Comparison with Quick Sort and Merge Sort

| Property | Heap Sort | Quick Sort | Merge Sort |
|----------|-----------|------------|------------|
| Time (Always) | O(n log n) | O(n log n) avg, O(n²) worst | O(n log n) |
| Space | O(1) | O(log n) stack | O(n) |
| Stable | No | No | Yes |
| Cache perf. | Poor (jumping around heap) | Good (sequential) | Moderate |
| Real-world | Moderate | Best | Good |

**Why heap sort is not as fast in practice despite O(n log n):**
1. **Cache unfriendly:** Heap accesses jump around the array (non-sequential)
2. **More constant factors:** Each sift-down requires 2-3 comparisons
3. **Poor with nearly sorted data:** Not adaptive — always O(n log n)

## Key Points

| Aspect | Detail |
|--------|--------|
| Guaranteed O(n log n) | Always, no worst-case degradation |
| In-place | O(1) extra space |
| Not stable | Equal elements may be reordered |
| Cache poor | Non-sequential memory access pattern |
| Good for | Priority queues, systems needing guaranteed time |

**Heap sort is often used when worst-case performance must be bounded (real-time systems) or when space is extremely constrained. Java's `PriorityQueue` uses a binary heap but not for sorting — it's primarily a queue implementation.**
