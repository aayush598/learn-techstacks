# Counting Sort

## Concept

Counting sort is a non-comparison based sorting algorithm that sorts integers by counting the frequency of each distinct value and using arithmetic to determine positions.

**Unlike comparison sorts, it achieves O(n + k) time by using the actual values as indices.**

## Characteristics

| Property | Value |
|----------|-------|
| Time | O(n + k) where k = range of values |
| Space | O(k) |
| Stable | Yes (with cumulative sum approach) |
| In-place | No |
| Data requirement | Integers in a limited range |

## Basic Counting Sort

```java
public class CountingSort {
    public static void countingSort(int[] arr) {
        if (arr.length == 0) return;

        // Find the range of values
        int max = arr[0];
        int min = arr[0];
        for (int num : arr) {
            max = Math.max(max, num);
            min = Math.min(min, num);
        }

        int range = max - min + 1;
        int[] count = new int[range];

        // Step 1: Count frequencies
        for (int num : arr) {
            count[num - min]++;
        }

        // Step 2: Reconstruct sorted array
        int index = 0;
        for (int i = 0; i < range; i++) {
            while (count[i] > 0) {
                arr[index++] = i + min;
                count[i]--;
            }
        }
    }
}
```

## Stable Counting Sort

The stable version preserves the relative order of equal elements. This is critical when sorting by multiple keys or when used as a subroutine in radix sort.

```java
public class CountingSortStable {
    public static void countingSort(int[] arr) {
        if (arr.length == 0) return;

        int max = arr[0];
        int min = arr[0];
        for (int num : arr) {
            max = Math.max(max, num);
            min = Math.min(min, num);
        }

        int range = max - min + 1;
        int[] count = new int[range];

        // Step 1: Count frequencies
        for (int num : arr) {
            count[num - min]++;
        }

        // Step 2: Cumulative sum (now count[i] = last position + 1 of value i)
        for (int i = 1; i < range; i++) {
            count[i] += count[i - 1];
        }

        // Step 3: Build output array from end to start
        int[] output = new int[arr.length];
        for (int i = arr.length - 1; i >= 0; i--) {
            int val = arr[i];
            int pos = count[val - min] - 1;
            output[pos] = val;
            count[val - min]--;
        }

        // Copy back
        System.arraycopy(output, 0, arr, 0, arr.length);
    }
}
```

**Why traversing from end to start preserves stability:**
- For equal elements, the last one in the original array gets placed at the last position among equals
- This preserves their original relative order

## General Counting Sort (Object Sort by Integer Key)

```java
public class CountingSortObjects {
    static class Element {
        int key;
        String value;

        Element(int key, String value) {
            this.key = key;
            this.value = value;
        }

        public String toString() { return "(" + key + ", " + value + ")"; }
    }

    public static void countingSort(Element[] arr) {
        if (arr.length == 0) return;

        int max = arr[0].key;
        int min = arr[0].key;
        for (Element e : arr) {
            max = Math.max(max, e.key);
            min = Math.min(min, e.key);
        }

        int range = max - min + 1;
        int[] count = new int[range];

        for (Element e : arr) {
            count[e.key - min]++;
        }

        // Cumulative sum
        for (int i = 1; i < range; i++) {
            count[i] += count[i - 1];
        }

        // Build output
        Element[] output = new Element[arr.length];
        for (int i = arr.length - 1; i >= 0; i--) {
            int key = arr[i].key;
            int pos = count[key - min] - 1;
            output[pos] = arr[i];
            count[key - min]--;
        }

        System.arraycopy(output, 0, arr, 0, arr.length);
    }

    public static void main(String[] args) {
        Element[] arr = {
            new Element(3, "apple"),
            new Element(1, "banana"),
            new Element(2, "cherry"),
            new Element(1, "date"),
            new Element(3, "elderberry")
        };

        System.out.println("Before: " + Arrays.toString(arr));
        countingSort(arr);
        System.out.println("After:  " + Arrays.toString(arr));
        // Output: [(1, banana), (1, date), (2, cherry), (3, apple), (3, elderberry)]
        // Note: banana before date (stable), apple before elderberry (stable)
    }
}
```

## Complexity Analysis

```
Let n = array length, k = range of values (max - min + 1)

Time:  O(n) for counting + O(k) for cumulative sum + O(n) for output = O(n + k)
Space: O(k) for count array + O(n) for output (stable version)

When to use: k = O(n), i.e., range is comparable to array size
```

## Complete Demo

```java
public class CountingSortDemo {
    public static void main(String[] args) {
        // Basic counting sort
        int[] arr1 = {4, 2, 2, 8, 3, 3, 1};
        System.out.println("Original: " + Arrays.toString(arr1));
        CountingSort.countingSort(arr1);
        System.out.println("Basic:    " + Arrays.toString(arr1));

        // Stable counting sort
        int[] arr2 = {4, 2, 2, 8, 3, 3, 1};
        CountingSortStable.countingSort(arr2);
        System.out.println("Stable:   " + Arrays.toString(arr2));

        // Negative numbers
        int[] arr3 = {-5, -2, -8, -1, -3};
        System.out.println("\nNegatives: " + Arrays.toString(arr3));
        CountingSort.countingSort(arr3);
        System.out.println("Sorted:    " + Arrays.toString(arr3));

        // Large range (inefficient for counting sort)
        int[] arr4 = {1, 1000000, 500, 100};
        System.out.println("\nLarge range: " + Arrays.toString(arr4));
        // Counting sort would allocate size 1000000 — impractical!
        System.out.println("Counting sort NOT recommended (range too large)");

        // Performance: counting sort vs Arrays.sort for limited range
        int[] countingArr = new int[100000];
        Random rand = new Random(42);
        for (int i = 0; i < countingArr.length; i++) {
            countingArr[i] = rand.nextInt(1000);  // range = 1000
        }

        long start = System.currentTimeMillis();
        CountingSort.countingSort(countingArr.clone());
        long countingTime = System.currentTimeMillis() - start;
        System.out.println("\nCounting sort (range=1000): " + countingTime + "ms");

        start = System.currentTimeMillis();
        Arrays.sort(countingArr.clone());
        long quickTime = System.currentTimeMillis() - start;
        System.out.println("Arrays.sort: " + quickTime + "ms");
    }
}
```

## When to Use Counting Sort

| Scenario | Recommendation |
|----------|---------------|
| Small integer range (k ≈ n) | Counting sort is excellent |
| Very large range (k >> n) | Avoid — too much space |
| Non-integer keys | Can't use directly |
| Need stability | Use stable version |
| Negative values | Works with offset (subtract min) |

## Common Use Cases

1. **Sorting exam scores** (range 0-100)
2. **Sorting ages** (range 0-150)
3. **Subroutine for radix sort** (counting sort by digit)
4. **Sorting characters** (ASCII range 0-255)

## Key Points

| Aspect | Detail |
|--------|--------|
| Non-comparison | Uses values as indices, not comparisons |
| O(n + k) time | Linear when k = O(n) |
| O(k) space | Can be prohibitively large |
| Stable variant | Traverse from end to start |
| Integer only | Requires integer keys |

**Counting sort is the fastest sorting algorithm when the range of input values is small relative to the input size. It's a building block for radix sort.**
