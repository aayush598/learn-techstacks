# Radix Sort

## Concept

Radix sort is a non-comparison based sorting algorithm that processes digits of numbers one at a time, from least significant digit (LSD) to most significant digit (MSD), using a stable subroutine (usually counting sort) at each step.

**Time Complexity:** O(d × (n + b)) where d = number of digits, b = base (e.g., 10)  
**Space Complexity:** O(n + b)

## LSD Radix Sort (Least Significant Digit First)

```java
public class RadixSort {
    public static void radixSort(int[] arr) {
        if (arr.length == 0) return;

        // Find the maximum number to determine number of digits
        int max = arr[0];
        for (int num : arr) {
            max = Math.max(max, Math.abs(num));
        }

        // Handle negative numbers
        // For simplicity, let's use the approach of separating negatives

        // Do counting sort for every digit
        for (int exp = 1; max / exp > 0; exp *= 10) {
            countingSortByDigit(arr, exp);
        }
    }

    // Counting sort based on a specific digit (exp = 1, 10, 100, ...)
    private static void countingSortByDigit(int[] arr, int exp) {
        int n = arr.length;
        int[] output = new int[n];
        int[] count = new int[10];  // Base 10 (digits 0-9)

        // Count frequencies of digits at current position
        for (int i = 0; i < n; i++) {
            int digit = (arr[i] / exp) % 10;
            count[digit]++;
        }

        // Cumulative sum (for stable placement)
        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }

        // Build output array (traverse from end for stability)
        for (int i = n - 1; i >= 0; i--) {
            int digit = (arr[i] / exp) % 10;
            int pos = count[digit] - 1;
            output[pos] = arr[i];
            count[digit]--;
        }

        // Copy back
        System.arraycopy(output, 0, arr, 0, n);
    }
}
```

## Radix Sort with Negative Numbers

```java
public class RadixSortWithNegatives {
    public static void radixSort(int[] arr) {
        if (arr.length == 0) return;

        // Separate positive and negative
        int[] negatives = Arrays.stream(arr).filter(x -> x < 0).toArray();
        int[] positives = Arrays.stream(arr).filter(x -> x >= 0).toArray();

        // Sort positives (normal radix sort)
        if (positives.length > 0) sortPositives(positives);

        // Sort negatives: make them positive, sort, then negate back
        if (negatives.length > 0) {
            for (int i = 0; i < negatives.length; i++) {
                negatives[i] = -negatives[i];
            }
            sortPositives(negatives);
            // After sorting, negatives are sorted ascending
            // But we need descending (most negative first)
            // So reverse and negate
            for (int i = 0; i < negatives.length; i++) {
                negatives[i] = -negatives[negatives.length - 1 - i];
            }
        }

        // Merge: negatives first (already reversed), then positives
        int idx = 0;
        for (int val : negatives) arr[idx++] = val;
        for (int val : positives) arr[idx++] = val;
    }

    private static void sortPositives(int[] arr) {
        int max = arr[0];
        for (int num : arr) {
            max = Math.max(max, num);
        }

        for (int exp = 1; max / exp > 0; exp *= 10) {
            countingSortByDigit(arr, exp);
        }
    }

    private static void countingSortByDigit(int[] arr, int exp) {
        int n = arr.length;
        int[] output = new int[n];
        int[] count = new int[10];

        for (int i = 0; i < n; i++) {
            int digit = (arr[i] / exp) % 10;
            count[digit]++;
        }

        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }

        for (int i = n - 1; i >= 0; i--) {
            int digit = (arr[i] / exp) % 10;
            output[count[digit] - 1] = arr[i];
            count[digit]--;
        }

        System.arraycopy(output, 0, arr, 0, n);
    }
}
```

## MSD Radix Sort (Most Significant Digit First)

MSD radix sort processes the most significant digit first, useful for lexicographic sorting:

```java
public class RadixSortMSD {
    public static void radixSortMSD(int[] arr) {
        if (arr.length == 0) return;

        int max = arr[0];
        for (int num : arr) max = Math.max(max, num);

        msdRadixSort(arr, 0, arr.length - 1, getMaxExp(max));
    }

    private static int getMaxExp(int num) {
        int exp = 1;
        while (num / exp >= 10) exp *= 10;
        return exp;
    }

    private static void msdRadixSort(int[] arr, int low, int high, int exp) {
        if (low >= high || exp == 0) return;

        // Count frequencies of current digit
        int[] count = new int[10];
        int[] index = new int[10];

        for (int i = low; i <= high; i++) {
            int digit = (arr[i] / exp) % 10;
            count[digit]++;
        }

        // Calculate start indices for each digit
        index[0] = low;
        for (int i = 1; i < 10; i++) {
            index[i] = index[i - 1] + count[i - 1];
        }

        // Partition elements by current digit
        int[] temp = new int[high - low + 1];
        int[] tempIdx = index.clone();

        for (int i = low; i <= high; i++) {
            int digit = (arr[i] / exp) % 10;
            temp[tempIdx[digit] - low] = arr[i];
            tempIdx[digit]++;
        }

        System.arraycopy(temp, 0, arr, low, temp.length);

        // Recursively sort each digit group
        for (int i = 0; i < 10; i++) {
            msdRadixSort(arr, index[i] - low + low,
                index[i] - low + low + count[i] - 1, exp / 10);
        }
    }
}
```

## Radix Sort on Strings

Radix sort can sort strings lexicographically (treat characters as "digits"):

```java
public class RadixSortStrings {
    public static void radixSort(String[] arr) {
        if (arr.length == 0) return;

        // Find maximum length
        int maxLen = 0;
        for (String s : arr) {
            maxLen = Math.max(maxLen, s.length());
        }

        // Pad strings to same length
        String[] padded = new String[arr.length];
        for (int i = 0; i < arr.length; i++) {
            padded[i] = String.format("%-" + maxLen + "s", arr[i]);
        }

        // Sort from last character to first
        for (int pos = maxLen - 1; pos >= 0; pos--) {
            countingSortByChar(padded, pos);
        }

        // Copy back (unpadded)
        for (int i = 0; i < arr.length; i++) {
            arr[i] = padded[i].trim();
        }
    }

    private static void countingSortByChar(String[] arr, int pos) {
        int n = arr.length;
        String[] output = new String[n];
        int[] count = new int[256];  // Extended ASCII

        for (String s : arr) {
            char c = s.charAt(pos);
            count[c]++;
        }

        for (int i = 1; i < 256; i++) {
            count[i] += count[i - 1];
        }

        for (int i = n - 1; i >= 0; i--) {
            char c = arr[i].charAt(pos);
            output[count[c] - 1] = arr[i];
            count[c]--;
        }

        System.arraycopy(output, 0, arr, 0, n);
    }
}
```

## Complete Demo

```java
import java.util.Arrays;
import java.util.Random;

public class RadixSortDemo {
    public static void main(String[] args) {
        // Standard radix sort
        int[] arr1 = {170, 45, 75, 90, 802, 24, 2, 66};
        System.out.println("Original: " + Arrays.toString(arr1));
        RadixSort.radixSort(arr1);
        System.out.println("Radix:    " + Arrays.toString(arr1));

        // With negative numbers
        int[] arr2 = {-5, 10, -3, 0, 8, -1, 7};
        System.out.println("\nWith negatives: " + Arrays.toString(arr2));
        RadixSortWithNegatives.radixSort(arr2);
        System.out.println("Sorted:         " + Arrays.toString(arr2));

        // String radix sort
        String[] arr3 = {"cat", "dog", "apple", "bat", "elephant", "car"};
        System.out.println("\nStrings original: " + Arrays.toString(arr3));
        RadixSortStrings.radixSort(arr3);
        System.out.println("Strings sorted:   " + Arrays.toString(arr3));

        // Performance comparison
        int[] radixArr = new int[100000];
        Random rand = new Random(42);
        for (int i = 0; i < radixArr.length; i++) {
            radixArr[i] = rand.nextInt(1000000);
        }

        long start = System.currentTimeMillis();
        RadixSort.radixSort(radixArr.clone());
        System.out.println("\nRadix sort: " + (System.currentTimeMillis() - start) + "ms");

        start = System.currentTimeMillis();
        Arrays.sort(radixArr.clone());
        System.out.println("Arrays.sort: " + (System.currentTimeMillis() - start) + "ms");
    }
}
```

## Complexity Analysis

| Aspect | Value |
|--------|-------|
| Time | O(d × (n + b)) |
| d = number of digits | log_b(max value) |
| b = base | Usually 10 |
| Space | O(n + b) |
| Stable | Yes (when using stable counting sort) |

**For 32-bit integers:** d = 10 (decimal) or d = 4 (hex) or d = 32 (binary)

## Radix Sort vs Comparison Sorts

| Scenario | Radix Sort | Quick Sort |
|----------|-----------|------------|
| n = 10⁶, range = 10⁶ | 6×10⁶ operations | ~20×10⁶ comparisons |
| n = 10⁶, range = 10¹² | 12×10⁶ operations | ~20×10⁶ comparisons |
| Memory | O(n + b) | O(log n) |
| Stability | Yes | No |

## Key Points

| Aspect | Detail |
|--------|--------|
| Non-comparison | Sorts by digit processing |
| Linear time | O(n) when d is constant |
| Stable | LSD version preserves order |
| Space | O(n + b) extra |
| Best for | Large n, small digit count |
| Limitation | Integer/string keys only |

**Radix sort is the go-to algorithm when you need to sort large numbers of integers or fixed-length strings in linear time. It's widely used in suffix array construction and other string-processing algorithms.**
