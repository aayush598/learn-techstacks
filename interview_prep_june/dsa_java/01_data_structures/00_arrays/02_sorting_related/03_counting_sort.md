# Counting Sort

## Non-Comparison Sort

Counting Sort is the first algorithm we encounter that doesn't use comparisons. Instead, it counts occurrences of each value and uses those counts to place elements in their correct positions.

**Key constraint:** Only works for integer keys within a known, limited range.

**Time:** O(n + k) where k is the range of input (max - min + 1)
**Space:** O(k)

## When to Use

- Range k is small relative to n (e.g., sorting ages 0-150, or exam scores 0-100)
- You need linear time
- You need a stable sort

**Do NOT use when:** k is large (e.g., sorting 32-bit integers). O(n + k) becomes O(n + 2³²) = O(2³²), which is worse than O(n log n).

## Basic Counting Sort (Positive Integers)

```java
public static void countingSort(int[] arr) {
    if (arr.length == 0) return;

    // Find the range
    int max = Arrays.stream(arr).max().getAsInt();
    int min = Arrays.stream(arr).min().getAsInt();
    int range = max - min + 1;

    // Count frequencies
    int[] count = new int[range];
    for (int num : arr) {
        count[num - min]++;
    }

    // Reconstruct sorted array
    int index = 0;
    for (int i = 0; i < range; i++) {
        while (count[i] > 0) {
            arr[index] = i + min;
            index++;
            count[i]--;
        }
    }
}
```

**Time:** O(n + k) — one pass to count, one pass to reconstruct.
**Space:** O(k) for the count array.

## Stable Counting Sort Implementation

The basic version above is **unstable** — it doesn't preserve the relative order of equal elements. For stability, we need cumulative counts.

```java
public static void countingSortStable(int[] arr) {
    if (arr.length == 0) return;

    int max = Arrays.stream(arr).max().getAsInt();
    int min = Arrays.stream(arr).min().getAsInt();
    int range = max - min + 1;

    // Count frequencies
    int[] count = new int[range];
    for (int num : arr) {
        count[num - min]++;
    }

    // Convert to cumulative counts (prefix sum)
    // After this, count[i] = number of elements ≤ (i + min)
    for (int i = 1; i < range; i++) {
        count[i] += count[i - 1];
    }

    // Build output array (traverse input from end for stability)
    int[] output = new int[arr.length];
    for (int i = arr.length - 1; i >= 0; i--) {
        int value = arr[i];
        int position = count[value - min] - 1;
        output[position] = value;
        count[value - min]--;
    }

    // Copy back
    System.arraycopy(output, 0, arr, 0, arr.length);
}
```

### Why traverse from the end?

Stability requires that if two elements have the same value, the one that appeared later in the original array ends up later in the sorted array. By traversing from the end, later elements are placed at higher positions (since we decrement count after each placement).

### Step-by-step example

```
Original: [4, 2, 2, 8, 3, 3, 1]
min=1, max=8, range=8

Count:    [1, 2, 2, 1, 0, 0, 0, 1]   (indices 0-7 for values 1-8)
Cumulative: [1, 3, 5, 6, 6, 6, 6, 7]

Traverse from end:
   arr[6]=1 → count[0]→pos=0, output[0]=1, count[0]=0
   arr[5]=3 → count[2]→pos=4, output[4]=3, count[2]=4
   arr[4]=3 → count[2]→pos=3, output[3]=3, count[2]=3
   arr[3]=8 → count[7]→pos=6, output[6]=8, count[7]=6
   arr[2]=2 → count[1]→pos=2, output[2]=2, count[1]=2
   arr[1]=2 → count[1]→pos=1, output[1]=2, count[1]=1
   arr[0]=4 → count[3]→pos=5, output[5]=4, count[3]=5

Output: [1, 2, 2, 3, 3, 4, 8]
```

## Applications

### Sort Colors (LeetCode 75)

```java
public static void sortColorsCounting(int[] arr) {
    // Values are 0, 1, 2 — perfect for counting sort
    int[] count = new int[3];
    for (int num : arr) count[num]++;

    int idx = 0;
    for (int i = 0; i < 3; i++) {
        while (count[i]-- > 0) {
            arr[idx++] = i;
        }
    }
}
```

But Dutch National Flag (three-pointer) is more efficient here (O(1) space vs O(k)).

### Sort Characters by Frequency (LeetCode 451)

```java
public static String frequencySort(String s) {
    // Count frequencies
    Map<Character, Integer> freq = new HashMap<>();
    for (char c : s.toCharArray()) {
        freq.merge(c, 1, Integer::sum);
    }

    // Bucket sort by frequency
    int maxFreq = Collections.max(freq.values());
    List<Character>[] buckets = new List[maxFreq + 1];
    for (char c : freq.keySet()) {
        int f = freq.get(c);
        if (buckets[f] == null) buckets[f] = new ArrayList<>();
        buckets[f].add(c);
    }

    // Build result
    StringBuilder sb = new StringBuilder();
    for (int f = maxFreq; f > 0; f--) {
        if (buckets[f] != null) {
            for (char c : buckets[f]) {
                for (int i = 0; i < f; i++) sb.append(c);
            }
        }
    }
    return sb.toString();
}
```

## Comparison with Other Sorts

| Aspect | Counting Sort | Quick Sort | Merge Sort |
|--------|---------------|------------|------------|
| Time | O(n + k) | O(n log n) avg | O(n log n) |
| Space | O(k) | O(log n) | O(n) |
| Stable version | ✓ (with cumulative) | ✗ | ✓ |
| Data type | Integers only | Any comparable | Any comparable |
| Large range | Bad | Good | Good |
| Small range | Excellent | Good | Good |

## Limitations

1. **Integers only** — cannot sort strings, objects (unless mapped to integers)
2. **Large range kills performance** — O(n + k) where k could be 2³¹ for 32-bit ints
3. **More space for large range** — count array of size 2³¹ ≈ 8 GB of memory
4. **Not in-place** — needs O(k) extra space

## Practice Problems

| Problem | Platform | Notes |
|---------|----------|-------|
| Sort Colors | LeetCode 75 | Count 0,1,2 |
| Sort Characters By Frequency | LeetCode 451 | Counting + bucket |
| Height Checker | LeetCode 1051 | Counting sort indices |
| Minimum Increment to Make Array Unique | LeetCode 945 | Counting sort idea |
| Maximum Gap | LeetCode 164 | Radix/bucket sort approach |
