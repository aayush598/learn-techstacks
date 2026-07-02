# Bubble Sort

## Concept

Bubble sort repeatedly steps through the array, compares adjacent elements, and swaps them if they're in the wrong order. The pass is repeated until no swaps are needed.

The name comes from the way larger elements "bubble up" to the end of the array.

## Characteristics

| Property | Value |
|----------|-------|
| Time (Worst) | O(n²) |
| Time (Average) | O(n²) |
| Time (Best) | O(n) — optimized, when already sorted |
| Space | O(1) — in-place |
| Stable | Yes (equal elements maintain relative order) |
| Adaptive | Yes (when optimized) |

## Basic Implementation

```java
public class BubbleSort {
    public static void bubbleSort(int[] arr) {
        int n = arr.length;

        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    // Swap adjacent elements
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
}
```

## Optimized Implementation (with Early Break)

The optimization stops the algorithm if a complete pass produces no swaps, meaning the array is already sorted.

```java
public class BubbleSortOptimized {
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        boolean swapped;

        for (int i = 0; i < n - 1; i++) {
            swapped = false;

            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    swapped = true;
                }
            }

            // If no swaps, array is sorted
            if (!swapped) {
                break;
            }
        }
    }
}
```

## Further Optimization: Skip Already Sorted Tail

Track the last swap position to avoid checking already sorted elements.

```java
public class BubbleSortTailOptimized {
    public static void bubbleSort(int[] arr) {
        int n = arr.length;

        while (n > 1) {
            int lastSwap = 0;

            for (int j = 0; j < n - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    lastSwap = j + 1;  // Track where last swap happened
                }
            }

            n = lastSwap;  // Elements beyond lastSwap are sorted
        }
    }
}
```

## Cocktail Shaker Sort (Bidirectional Bubble Sort)

An extension of bubble sort that alternates direction each pass.

```java
public class CocktailShakerSort {
    public static void cocktailSort(int[] arr) {
        boolean swapped = true;
        int start = 0;
        int end = arr.length - 1;

        while (swapped) {
            swapped = false;

            // Forward pass: bubble largest to the end
            for (int i = start; i < end; i++) {
                if (arr[i] > arr[i + 1]) {
                    int temp = arr[i];
                    arr[i] = arr[i + 1];
                    arr[i + 1] = temp;
                    swapped = true;
                }
            }
            end--;

            if (!swapped) break;

            // Backward pass: bubble smallest to the start
            for (int i = end - 1; i >= start; i--) {
                if (arr[i] > arr[i + 1]) {
                    int temp = arr[i];
                    arr[i] = arr[i + 1];
                    arr[i + 1] = temp;
                    swapped = true;
                }
            }
            start++;
        }
    }
}
```

## Why Bubble Sort is Rarely Used in Practice

1. **O(n²) time** — Insertion sort is also O(n²) but does fewer comparisons for nearly sorted data
2. **O(n²) swaps** — Selection sort makes only O(n) swaps
3. **Simple but slow** — For small datasets, insertion sort is comparable; for large datasets, O(n log n) algorithms dominate

## When to Use Bubble Sort

- **Educational purposes:** Easy to understand and teach
- **Nearly sorted data:** The optimized version runs in O(n)
- **Very small arrays:** Simple code, no overhead
- **When stability matters and memory is extremely tight:** In-place and stable

## Complete Demo

```java
public class BubbleSortDemo {
    public static void main(String[] args) {
        int[] arr = {64, 34, 25, 12, 22, 11, 90};

        System.out.println("Original: " + Arrays.toString(arr));

        // Basic bubble sort
        int[] arr1 = arr.clone();
        BubbleSort.bubbleSort(arr1);
        System.out.println("Basic:    " + Arrays.toString(arr1));

        // Optimized bubble sort
        int[] arr2 = arr.clone();
        BubbleSortOptimized.bubbleSort(arr2);
        System.out.println("Optimized: " + Arrays.toString(arr2));

        // Tail-optimized
        int[] arr3 = arr.clone();
        BubbleSortTailOptimized.bubbleSort(arr3);
        System.out.println("Tail Opt: " + Arrays.toString(arr3));

        // Cocktail shaker
        int[] arr4 = arr.clone();
        CocktailShakerSort.cocktailSort(arr4);
        System.out.println("Cocktail: " + Arrays.toString(arr4));

        // Test with nearly sorted array (best case for optimized)
        int[] nearlySorted = {1, 2, 3, 4, 6, 5, 7, 8, 9, 10};
        System.out.println("\nNearly sorted: " + Arrays.toString(nearlySorted));

        long start = System.nanoTime();
        BubbleSort.bubbleSort(nearlySorted.clone());
        long basicTime = System.nanoTime() - start;

        start = System.nanoTime();
        BubbleSortOptimized.bubbleSort(nearlySorted.clone());
        long optimizedTime = System.nanoTime() - start;

        System.out.println("Basic time: " + basicTime + "ns");
        System.out.println("Optimized time: " + optimizedTime + "ns (early exit)");
    }
}
```

## Key Points

| Aspect | Detail |
|--------|--------|
| Number of passes | n-1 (worst), 1 (best with optimization) |
| Number of comparisons | n(n-1)/2 (worst), n-1 (best) |
| Number of swaps | n(n-1)/2 (worst), 0 (best) |
| In-place | Yes |
| Stable | Yes |
| Adaptive | Yes (with optimization) |

Bubble sort is primarily a **teaching tool** to introduce sorting concepts. In practice, use insertion sort for small/nearly sorted datasets and merge sort or quicksort for general purpose.
