# Two Pointer Technique

## Concept

The two-pointer technique uses two pointers that move through the data structure, usually toward each other or in the same direction. It's a staple for array and string problems, typically reducing O(n²) brute force to O(n).

### Why it works

When a brute force solution uses nested loops (i from 0..n, j from i+1..n), you're re-examining the same elements many times. Two pointers eliminate this by:
- Maintaining a **window** or **range** that shrinks/grows
- Using the **sorted property** to make decisions about which pointer to move
- Tracking meaningful information as the pointers move

## Pair Sum in Sorted Array

**Problem:** Find two numbers in a sorted array that sum to a target.

```java
public static int[] twoSumSorted(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left < right) {
        int sum = arr[left] + arr[right];
        if (sum == target) {
            return new int[]{left, right};
        } else if (sum < target) {
            left++;  // need bigger sum
        } else {
            right--; // need smaller sum
        }
    }
    return new int[]{-1, -1}; // no pair found
}
```

**Time:** O(n). **Space:** O(1).

**Why this works:** Sorting guarantees that moving left increases the sum, moving right decreases it. This is a **binary search-like** reduction of the search space.

## Triplet Sum (3Sum)

**Problem:** Find all unique triplets `[nums[i], nums[j], nums[k]]` that sum to zero.

```java
public static List<List<Integer>> threeSum(int[] arr) {
    List<List<Integer>> result = new ArrayList<>();
    Arrays.sort(arr);

    for (int i = 0; i < arr.length - 2; i++) {
        // Skip duplicate values for i
        if (i > 0 && arr[i] == arr[i - 1]) continue;

        int left = i + 1, right = arr.length - 1;
        while (left < right) {
            int sum = arr[i] + arr[left] + arr[right];
            if (sum == 0) {
                result.add(Arrays.asList(arr[i], arr[left], arr[right]));
                left++;
                right--;
                // Skip duplicates
                while (left < right && arr[left] == arr[left - 1]) left++;
                while (left < right && arr[right] == arr[right + 1]) right--;
            } else if (sum < 0) {
                left++;
            } else {
                right--;
            }
        }
    }
    return result;
}
```

**Time:** O(n²) — sort O(n log n) + nested loops O(n²).
**Space:** O(1) extra (excluding output).

### Why not O(n³)?

Each iteration of `i` triggers a two-pointer scan from i+1 to end. That scan is O(n), and we have O(n) iterations of i, so O(n²) total. The two-pointer scan is linear because each step eliminates exactly one element from consideration.

## Three Sum Closest

**Problem:** Find the triplet sum closest to a target.

```java
public static int threeSumClosest(int[] arr, int target) {
    Arrays.sort(arr);
    int closest = arr[0] + arr[1] + arr[2];

    for (int i = 0; i < arr.length - 2; i++) {
        int left = i + 1, right = arr.length - 1;
        while (left < right) {
            int sum = arr[i] + arr[left] + arr[right];
            if (Math.abs(sum - target) < Math.abs(closest - target)) {
                closest = sum;
            }
            if (sum < target) {
                left++;
            } else if (sum > target) {
                right--;
            } else {
                return sum; // exact match
            }
        }
    }
    return closest;
}
```

## 4Sum Problem

**Problem:** Find all unique quadruplets that sum to target.

```java
public static List<List<Integer>> fourSum(int[] arr, int target) {
    List<List<Integer>> result = new ArrayList<>();
    Arrays.sort(arr);
    int n = arr.length;

    for (int i = 0; i < n - 3; i++) {
        if (i > 0 && arr[i] == arr[i - 1]) continue;
        for (int j = i + 1; j < n - 2; j++) {
            if (j > i + 1 && arr[j] == arr[j - 1]) continue;

            int left = j + 1, right = n - 1;
            while (left < right) {
                long sum = (long) arr[i] + arr[j] + arr[left] + arr[right];
                if (sum == target) {
                    result.add(Arrays.asList(arr[i], arr[j], arr[left], arr[right]));
                    left++;
                    right--;
                    while (left < right && arr[left] == arr[left - 1]) left++;
                    while (left < right && arr[right] == arr[right + 1]) right--;
                } else if (sum < target) {
                    left++;
                } else {
                    right--;
                }
            }
        }
    }
    return result;
}
```

**Time:** O(n³). Each added number layers another nested loop with two-pointer optimization on the innermost two.

## Remove Duplicates from Sorted Array

**Problem:** In-place removal of duplicates, return new length.

```java
public static int removeDuplicates(int[] arr) {
    if (arr.length == 0) return 0;
    int write = 1; // position to write next unique element
    for (int read = 1; read < arr.length; read++) {
        if (arr[read] != arr[read - 1]) {
            arr[write] = arr[read];
            write++;
        }
    }
    return write;
}
```

**Key insight:** Two pointers — `read` traverses the whole array, `write` marks where the next unique value goes. `write` is always ≤ `read`, so we never overwrite data we haven't processed.

## Move Zeros to End

**Problem:** Move all zeros to the end while maintaining relative order of non-zero elements.

```java
public static void moveZeros(int[] arr) {
    int nonZeroIndex = 0;
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] != 0) {
            arr[nonZeroIndex] = arr[i];
            nonZeroIndex++;
        }
    }
    // Fill remaining with zeros
    while (nonZeroIndex < arr.length) {
        arr[nonZeroIndex] = 0;
        nonZeroIndex++;
    }
}
```

**Variant with swap (one-pass):**

```java
public static void moveZerosSwap(int[] arr) {
    for (int i = 0, j = 0; i < arr.length; i++) {
        if (arr[i] != 0) {
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
            j++;
        }
    }
}
```

## Sort Colors (Dutch National Flag)

**Problem:** Sort an array of 0s, 1s, and 2s in-place. Three pointers.

```java
public static void sortColors(int[] arr) {
    int low = 0, mid = 0, high = arr.length - 1;

    while (mid <= high) {
        switch (arr[mid]) {
            case 0:
                swap(arr, low, mid);
                low++;
                mid++;
                break;
            case 1:
                mid++;
                break;
            case 2:
                swap(arr, mid, high);
                high--;
                break;
        }
    }
}

private static void swap(int[] arr, int i, int j) {
    int temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}
```

### How it works

- `low` tracks the boundary of 0s
- `high` tracks the boundary of 2s
- `mid` scans unknown territory between low and high

```
Initial:  [2, 0, 2, 1, 1, 0]
           L,M              H

After partitioning:
           [0, 0, 1, 1, 2, 2]
                  L  M
                           H
```

This is O(n), one pass, O(1) space. No sorting algorithm needed because we know the exact set of values.

## Container with Most Water

**Problem:** Given array of heights, find two lines that form a container holding the most water.

```java
public static int maxArea(int[] height) {
    int left = 0, right = height.length - 1;
    int maxWater = 0;

    while (left < right) {
        int width = right - left;
        int h = Math.min(height[left], height[right]);
        maxWater = Math.max(maxWater, width * h);

        // Move the pointer with the smaller height inward
        if (height[left] < height[right]) {
            left++;
        } else {
            right--;
        }
    }
    return maxWater;
}
```

### Why move the smaller height?

The area is `min(h[left], h[right]) * (right - left)`. Moving the larger height inward can't increase the area because the width decreases and the height is still limited by the smaller one. By moving the smaller height, we might find a taller line that increases the area.

## Summary of Two-Pointer Patterns

| Pattern | Direction | Example |
|---------|-----------|---------|
| Opposite ends | `i→` `←j` | Pair sum, container with water |
| Same direction (slow/fast) | `i→` `j→` | Remove duplicates, move zeros |
| Three pointers | `i→` `mid→` `←j` | Dutch national flag |
| Sliding window variant | `i→` `j→` with window | Subarray problems (covered separately) |

## When to Use Two Pointers

1. **Sorted array** — always consider two pointers from opposite ends
2. **In-place modification** — read/write pointers
3. **Partitioning problems** — three-way partition
4. **O(n²) → O(n) reduction** — nested loops where j depends on i

## Common Interview Questions

| Problem | LeetCode | Difficulty |
|---------|----------|------------|
| Two Sum II (sorted) | 167 | Easy |
| 3Sum | 15 | Medium |
| 3Sum Closest | 16 | Medium |
| 4Sum | 18 | Medium |
| Remove Duplicates | 26 | Easy |
| Move Zeroes | 283 | Easy |
| Sort Colors | 75 | Medium |
| Container With Most Water | 11 | Medium |
| Trapping Rain Water | 42 | Hard |
