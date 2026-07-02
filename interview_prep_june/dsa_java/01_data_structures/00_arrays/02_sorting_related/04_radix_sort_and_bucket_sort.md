# Radix Sort and Bucket Sort

## Radix Sort: Sorting by Digits

Radix Sort processes digits one at a time, from least significant to most significant (LSD) or vice versa (MSD). Each digit pass uses a **stable** sort — typically Counting Sort.

### Why it works

If we sort by each digit position from LSD to MSD, after processing all digits, the array is fully sorted. Stability is crucial: earlier digit sorts are preserved when later digits have equal values.

### LSD Radix Sort Implementation

```java
public static void radixSort(int[] arr) {
    if (arr.length == 0) return;

    int max = Arrays.stream(arr).max().getAsInt();

    // Do counting sort for each digit (exp = 1, 10, 100, ...)
    for (int exp = 1; max / exp > 0; exp *= 10) {
        countingSortByDigit(arr, exp);
    }
}

private static void countingSortByDigit(int[] arr, int exp) {
    int n = arr.length;
    int[] output = new int[n];
    int[] count = new int[10]; // digits 0-9

    // Count occurrences of each digit
    for (int num : arr) {
        int digit = (num / exp) % 10;
        count[digit]++;
    }

    // Cumulative count (for stable placement)
    for (int i = 1; i < 10; i++) {
        count[i] += count[i - 1];
    }

    // Build output (traverse from end for stability)
    for (int i = n - 1; i >= 0; i--) {
        int digit = (arr[i] / exp) % 10;
        output[count[digit] - 1] = arr[i];
        count[digit]--;
    }

    // Copy back
    System.arraycopy(output, 0, arr, 0, n);
}
```

### Handling Negative Numbers

```java
public static void radixSortWithNegatives(int[] arr) {
    if (arr.length == 0) return;

    // Separate positive and negative
    int min = Arrays.stream(arr).min().getAsInt();

    // Shift all values to non-negative range
    if (min < 0) {
        for (int i = 0; i < arr.length; i++) {
            arr[i] -= min;
        }
    }

    // Standard radix sort
    int max = Arrays.stream(arr).max().getAsInt();
    for (int exp = 1; max / exp > 0; exp *= 10) {
        countingSortByDigit(arr, exp);
    }

    // Shift back
    if (min < 0) {
        for (int i = 0; i < arr.length; i++) {
            arr[i] += min;
        }
    }
}
```

### Time and Space

- **Time:** O(d × (n + b)) where d = number of digits, b = base (10)
- For 32-bit integers: d = 10 (since 2³¹ ≈ 2.1B, 10 digits), so O(10 × (n + 10)) = O(n)
- **Space:** O(n + b) = O(n) for the output array

### LSD vs MSD Radix Sort

| Aspect | LSD | MSD |
|--------|-----|-----|
| Direction | Right to left | Left to right |
| Stability | Requires stable per-pass sort | Can be recursive |
| Performance | More consistent | Better for variable-length strings |
| Use case | Fixed-width integers | Strings, variable-length data |

**LSD is simpler** and more commonly used for integers. **MSD** is useful for strings — sort by first character, then recursively sort each group.

### MSD Radix Sort for Strings

```java
public static void msdRadixSort(String[] arr) {
    msdSort(arr, 0, arr.length - 1, 0);
}

private static void msdSort(String[] arr, int low, int high, int d) {
    if (low >= high) return;

    // Counting sort by character at position d
    int R = 256; // extended ASCII
    int[] count = new int[R + 2];
    String[] aux = new String[high - low + 1];

    // Count frequencies
    for (int i = low; i <= high; i++) {
        int c = charAt(arr[i], d);
        count[c + 2]++;
    }

    // Cumulative
    for (int r = 0; r < R + 1; r++) {
        count[r + 1] += count[r];
    }

    // Distribute
    for (int i = low; i <= high; i++) {
        int c = charAt(arr[i], d);
        aux[count[c + 1]++] = arr[i];
    }

    // Copy back
    System.arraycopy(aux, 0, arr, low, high - low + 1);

    // Recursively sort each group
    for (int r = 0; r < R; r++) {
        msdSort(arr, low + count[r], low + count[r + 1] - 1, d + 1);
    }
}

private static int charAt(String s, int d) {
    if (d < s.length()) return s.charAt(d);
    return -1; // end of string marker
}
```

## Bucket Sort

Bucket Sort distributes elements into a fixed number of "buckets," sorts each bucket (usually with Insertion Sort), and concatenates.

```java
public static void bucketSort(float[] arr) {
    if (arr.length == 0) return;

    // Create buckets
    int n = arr.length;
    @SuppressWarnings("unchecked")
    List<Float>[] buckets = new List[n];
    for (int i = 0; i < n; i++) {
        buckets[i] = new ArrayList<>();
    }

    // Distribute into buckets
    for (float num : arr) {
        int bucketIndex = (int) (num * n); // assumes uniform [0, 1) distribution
        buckets[bucketIndex].add(num);
    }

    // Sort each bucket
    for (List<Float> bucket : buckets) {
        Collections.sort(bucket); // uses TimSort
    }

    // Concatenate
    int index = 0;
    for (List<Float> bucket : buckets) {
        for (float num : bucket) {
            arr[index++] = num;
        }
    }
}
```

### For uniform distribution in [0, 1)

- Each bucket gets roughly n/k elements
- Insertion Sort per bucket: O((n/k)²) each, total O(k × (n/k)²) = O(n²/k)
- With k = n, each bucket has about 1 element: O(n)

### For arbitrary range

```java
public static void bucketSort(int[] arr, int bucketSize) {
    if (arr.length == 0) return;

    int min = Arrays.stream(arr).min().getAsInt();
    int max = Arrays.stream(arr).max().getAsInt();

    int bucketCount = (max - min) / bucketSize + 1;
    @SuppressWarnings("unchecked")
    List<Integer>[] buckets = new List[bucketCount];
    for (int i = 0; i < bucketCount; i++) {
        buckets[i] = new ArrayList<>();
    }

    for (int num : arr) {
        int bucketIndex = (num - min) / bucketSize;
        buckets[bucketIndex].add(num);
    }

    int index = 0;
    for (List<Integer> bucket : buckets) {
        Collections.sort(bucket);
        for (int num : bucket) {
            arr[index++] = num;
        }
    }
}
```

### Bucket Sort Analysis

| Aspect | Value |
|--------|-------|
| Best case | O(n + k) — uniform distribution |
| Average case | O(n + k) — assuming even distribution |
| Worst case | O(n²) — all elements in one bucket |
| Space | O(n + k) |
| Stable | Yes (if individual bucket sort is stable) |

## When to Use Each

| Algorithm | When to Use | Example |
|-----------|-------------|---------|
| Counting Sort | Small integer range (k < n) | Ages, grades, colors |
| LSD Radix Sort | Fixed-width integers | 32-bit ints, student IDs |
| MSD Radix Sort | Strings, variable-length | Names, words |
| Bucket Sort | Uniformly distributed real numbers | GPA distribution, probability data |

## Practice Problems

| Problem | Platform | Approach |
|---------|----------|----------|
| Sort an Array | LeetCode 912 | Radix sort |
| Maximum Gap | LeetCode 164 | Radix/bucket sort |
| Top K Frequent Elements | LeetCode 347 | Bucket sort by frequency |
| Sort Characters By Frequency | LeetCode 451 | Bucket sort |
| Minimum Time Difference | LeetCode 539 | Radix/bucket on time |
| Sort Colors | LeetCode 75 | Counting sort |
