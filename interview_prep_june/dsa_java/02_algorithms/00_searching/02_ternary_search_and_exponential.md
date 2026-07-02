# Ternary Search, Exponential Search, and Interpolation Search

## 1. Ternary Search

### Concept

Ternary search is a divide-and-conquer algorithm for finding the maximum or minimum of a **unimodal function** (strictly increasing then strictly decreasing, or vice versa).

It divides the search range into **three** equal parts and eliminates one of the outer thirds based on function evaluation.

**Time Complexity:** O(log₃ n) ≈ O(log n) — but in practice, binary search is often faster due to fewer comparisons.

### Finding Peak in a Unimodal Array

```java
public class TernarySearch {
    public static int ternarySearch(int[] arr) {
        int low = 0;
        int high = arr.length - 1;

        while (high - low > 2) {  // Need at least 3 elements
            int mid1 = low + (high - low) / 3;
            int mid2 = high - (high - low) / 3;

            if (arr[mid1] < arr[mid2]) {
                // Peak is in [mid1, high]
                low = mid1;
            } else {
                // Peak is in [low, mid2]
                high = mid2;
            }
        }

        // Find max in the remaining 1-3 elements
        int maxVal = arr[low];
        int maxIdx = low;
        for (int i = low + 1; i <= high; i++) {
            if (arr[i] > maxVal) {
                maxVal = arr[i];
                maxIdx = i;
            }
        }

        return maxIdx;
    }

    // For finding maximum of a unimodal function
    public static double ternarySearchContinuous(double low, double high, double eps) {
        while (high - low > eps) {
            double mid1 = low + (high - low) / 3;
            double mid2 = high - (high - low) / 3;

            double f1 = f(mid1);
            double f2 = f(mid2);

            if (f1 < f2) {
                low = mid1;
            } else {
                high = mid2;
            }
        }

        return (low + high) / 2;
    }

    // Unimodal function f(x) = -(x-3)² + 5 (peak at x=3)
    private static double f(double x) {
        return -(x - 3) * (x - 3) + 5;
    }
}
```

### When to Use Ternary Search

- Finding peak/valley in unimodal array
- Finding minimum/maximum of convex/concave functions
- Any function where f(x) has a single maximum/minimum

### Ternary Search vs Binary Search

| Aspect | Ternary Search | Binary Search |
|--------|---------------|---------------|
| Division | 3 parts | 2 parts |
| Function requirement | Unimodal | Monotonic |
| Comparisons per iteration | 2 function evaluations | 1 comparison |
| Iterations | log₃ n | log₂ n |
| Best for | Continuous optimization | Discrete search |

**Note:** Despite O(log₃ n) vs O(log₂ n), binary search is usually preferred because:
- Ternary search does 2 evaluations per iteration vs binary's 1
- The 2 * log₃ n ≈ 1.26 * log₂ n, so binary search is actually more efficient

## 2. Exponential Search

### Concept

Exponential search finds the position of a target in a sorted array by:
1. Finding a range [2^(k-1), 2^k] that contains the target (doubling)
2. Performing binary search within that range

**Time Complexity:** O(log i) where i is the target's index  
**Space Complexity:** O(1)

### Implementation

```java
public class ExponentialSearch {
    public static int exponentialSearch(int[] arr, int target) {
        if (arr[0] == target) return 0;

        // Find range where target exists
        int i = 1;
        while (i < arr.length && arr[i] <= target) {
            i *= 2;
        }

        // Binary search in [i/2, min(i, n-1)]
        return binarySearch(arr, target, i / 2, Math.min(i, arr.length - 1));
    }

    private static int binarySearch(int[] arr, int target, int low, int high) {
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }
}
```

### Exponential Search for Unbounded Arrays

When the array size is unknown (or infinite), exponential search is the standard approach:

```java
public class UnboundedArraySearch {
    // Interface for an unbounded/infinite array
    interface UnboundedArray {
        int get(int index);  // Returns Integer.MAX_VALUE if beyond bounds
    }

    public static int searchUnbounded(UnboundedArray arr, int target) {
        // Find the upper bound
        int high = 1;
        while (arr.get(high) != Integer.MAX_VALUE && arr.get(high) < target) {
            high *= 2;
        }

        // If exceeded bounds, cap at last valid index
        int low = high / 2;

        // Binary search in [low, high]
        while (low <= high) {
            int mid = low + (high - low) / 2;
            int val = arr.get(mid);

            if (val == target) return mid;
            if (val == Integer.MAX_VALUE || val > target) {
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }

        return -1;
    }
}
```

### Why Exponential Search?

- **For unbounded arrays:** Binary search can't work because we don't know the high bound
- **For bounded arrays:** When the target is near the beginning, exponential search is faster than binary search (O(log i) vs O(log n))
- **Time complexity:** O(log i) where i is the target's position — much better than O(log n) when i << n

## 3. Interpolation Search

### Concept

Interpolation search is an improved variant of binary search for **uniformly distributed** sorted data. Instead of always checking the middle element, it probes at a position proportional to the target value.

**Time Complexity:** 
- Average: O(log log n) for uniform distribution
- Worst: O(n) for non-uniform distribution

### Implementation

```java
public class InterpolationSearch {
    public static int interpolationSearch(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;

        while (low <= high && target >= arr[low] && target <= arr[high]) {
            if (low == high) {
                return arr[low] == target ? low : -1;
            }

            // Probing position formula
            int probe = low + (high - low) *
                (target - arr[low]) / (arr[high] - arr[low]);

            if (arr[probe] == target) {
                return probe;
            }

            if (arr[probe] < target) {
                low = probe + 1;
            } else {
                high = probe - 1;
            }
        }

        return -1;
    }
}
```

### How the Probe Position Works

```
probe = low + (high - low) * (target - arr[low]) / (arr[high] - arr[low])

This is linear interpolation:
- If target ≈ arr[low], probe ≈ low
- If target ≈ arr[high], probe ≈ high
- If target ≈ mid-value, probe ≈ mid
```

### Interpolation vs Binary Search

```java
public class SearchComparison {
    public static void main(String[] args) {
        // Uniform distribution: interpolation wins
        int[] uniform = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20};
        int target = 17;

        long start = System.nanoTime();
        int idx1 = interpolationSearch(uniform, target);
        long end = System.nanoTime();
        System.out.println("Interpolation: " + idx1 + " in " + (end-start) + "ns");

        start = System.nanoTime();
        int idx2 = binarySearch(uniform, target);
        end = System.nanoTime();
        System.out.println("Binary: " + idx2 + " in " + (end-start) + "ns");

        // Non-uniform: binary search is safer
        int[] nonUniform = {1, 2, 10, 100, 1000, 10000, 100000};
        target = 100;

        start = System.nanoTime();
        idx1 = interpolationSearch(nonUniform, target);
        end = System.nanoTime();
        System.out.println("\nInterpolation (non-uniform): " + idx1 + " in " + (end-start) + "ns");

        start = System.nanoTime();
        idx2 = binarySearch(nonUniform, target);
        end = System.nanoTime();
        System.out.println("Binary (non-uniform): " + idx2 + " in " + (end-start) + "ns");
    }

    private static int binarySearch(int[] arr, int target) {
        int lo = 0, hi = arr.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }

    private static int interpolationSearch(int[] arr, int target) {
        int lo = 0, hi = arr.length - 1;
        while (lo <= hi && target >= arr[lo] && target <= arr[hi]) {
            int probe = lo + (hi - lo) * (target - arr[lo]) / (arr[hi] - arr[lo]);
            if (arr[probe] == target) return probe;
            if (arr[probe] < target) lo = probe + 1;
            else hi = probe - 1;
        }
        return -1;
    }
}
```

## Complete Search Algorithm Comparison

```java
public class SearchDemo {
    public static void main(String[] args) {
        int[] arr = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21};
        int target = 13;

        System.out.println("Array: " + Arrays.toString(arr));
        System.out.println("Target: " + target);

        // Ternary search on unimodal (mountain) array
        int[] mountain = {1, 4, 7, 10, 13, 15, 12, 8, 5, 2};
        System.out.println("\nTernary search on mountain array:");
        int peakIdx = TernarySearch.ternarySearch(mountain);
        System.out.println("Peak index: " + peakIdx + ", value: " + mountain[peakIdx]);

        // Exponential search
        System.out.println("\nExponential search:");
        int expIdx = ExponentialSearch.exponentialSearch(arr, target);
        System.out.println("Target " + target + " at index: " + expIdx);

        // Interpolation search
        System.out.println("\nInterpolation search:");
        int interpIdx = InterpolationSearch.interpolationSearch(arr, target);
        System.out.println("Target " + target + " at index: " + interpIdx);
    }
}
```

## When to Use What

| Algorithm | Best For | Time | Data Requirement |
|-----------|----------|------|-----------------|
| Linear Search | Small n, unsorted, one-time | O(n) | None |
| Binary Search | General purpose on sorted | O(log n) | Sorted, random access |
| Ternary Search | Unimodal functions (peak/valley) | O(log n) | Unimodal array |
| Exponential Search | Unbounded arrays, target near start | O(log i) | Sorted, random access |
| Interpolation Search | Uniformly distributed data | O(log log n) | Sorted, uniform distribution |

**Rule of thumb:** For most interview problems, **binary search** is the default. The others are niche optimizations for specific scenarios.
