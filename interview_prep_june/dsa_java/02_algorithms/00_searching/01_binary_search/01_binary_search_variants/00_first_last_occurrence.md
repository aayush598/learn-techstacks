# First & Last Occurrence and Rotated Array

## First Occurrence in Sorted Array (With Duplicates)

When the array has duplicates, binary search can be modified to find the first occurrence by not stopping at the first match but continuing to search left.

```java
public class FirstOccurrence {
    public static int firstOccurrence(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;
        int result = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] == target) {
                result = mid;       // Found, but check left for earlier
                high = mid - 1;
            } else if (arr[mid] < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }

        return result;
    }
}
```

## Last Occurrence in Sorted Array

```java
public class LastOccurrence {
    public static int lastOccurrence(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;
        int result = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] == target) {
                result = mid;       // Found, but check right for later
                low = mid + 1;
            } else if (arr[mid] < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }

        return result;
    }
}
```

## Count Occurrences in Sorted Array

```java
public class CountOccurrences {
    public static int countOccurrences(int[] arr, int target) {
        int first = firstOccurrence(arr, target);
        if (first == -1) return 0;

        int last = lastOccurrence(arr, target);
        return last - first + 1;
    }

    // Alternative using upper bound - lower bound
    public static int countUsingBounds(int[] arr, int target) {
        int lb = lowerBound(arr, target);
        int ub = upperBound(arr, target);
        return ub - lb;
    }

    private static int lowerBound(int[] arr, int target) {
        int lo = 0, hi = arr.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] >= target) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    private static int upperBound(int[] arr, int target) {
        int lo = 0, hi = arr.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] > target) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    private static int firstOccurrence(int[] arr, int target) {
        // implementation from above
        int lo = 0, hi = arr.length - 1, ans = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] == target) { ans = mid; hi = mid - 1; }
            else if (arr[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return ans;
    }

    private static int lastOccurrence(int[] arr, int target) {
        int lo = 0, hi = arr.length - 1, ans = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] == target) { ans = mid; lo = mid + 1; }
            else if (arr[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return ans;
    }
}
```

## Find Peak Index in Mountain Array

A mountain array is an array that increases to a peak then decreases. Find the peak index.

**Property:** `arr[mid] < arr[mid+1]` → peak is on the right; otherwise peak is on the left (or at mid).

```java
public class PeakIndexInMountainArray {
    public static int peakIndexInMountainArray(int[] arr) {
        int low = 0;
        int high = arr.length - 1;

        while (low < high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] < arr[mid + 1]) {
                // We're in the ascending part, peak is to the right
                low = mid + 1;
            } else {
                // We're in the descending part, peak is at mid or to the left
                high = mid;
            }
        }

        return low;  // Peak index
    }
}
```

## Find Minimum in Rotated Sorted Array

A rotated sorted array is a sorted array that has been rotated at some pivot. Find the minimum element.

**Observation:** The minimum is the only element where `arr[mid] > arr[mid+1]` (in a distinct array). Equivalently, compare `arr[mid]` with `arr[high]`:
- If `arr[mid] > arr[high]`: minimum is in the right half (mid+1 to high)
- If `arr[mid] <= arr[high]`: minimum is in the left half (low to mid)

```java
public class FindMinInRotatedSortedArray {
    // Distinct elements
    public static int findMin(int[] arr) {
        int low = 0;
        int high = arr.length - 1;

        while (low < high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] > arr[high]) {
                // Minimum is in the right half
                low = mid + 1;
            } else {
                // Minimum is in the left half (including mid)
                high = mid;
            }
        }

        return arr[low];
    }

    // With duplicates
    public static int findMinWithDuplicates(int[] arr) {
        int low = 0;
        int high = arr.length - 1;

        while (low < high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] > arr[high]) {
                low = mid + 1;
            } else if (arr[mid] < arr[high]) {
                high = mid;
            } else {
                // arr[mid] == arr[high], can't decide, shrink
                high--;
            }
        }

        return arr[low];
    }
}
```

## Search in Rotated Sorted Array

Search for a target in a rotated sorted array.

**Strategy:**
1. Find which half is sorted (compare arr[low] with arr[mid])
2. Check if target lies in the sorted half
3. Eliminate the other half

```java
public class SearchInRotatedSortedArray {
    // Without duplicates
    public static int search(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] == target) return mid;

            // Check which half is sorted
            if (arr[low] <= arr[mid]) {
                // Left half is sorted
                if (target >= arr[low] && target < arr[mid]) {
                    high = mid - 1;  // Target in left half
                } else {
                    low = mid + 1;   // Target in right half
                }
            } else {
                // Right half is sorted
                if (target > arr[mid] && target <= arr[high]) {
                    low = mid + 1;   // Target in right half
                } else {
                    high = mid - 1;  // Target in left half
                }
            }
        }

        return -1;
    }

    // With duplicates
    public static boolean searchWithDuplicates(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] == target) return true;

            // When arr[low] == arr[mid] == arr[high], we can't decide
            if (arr[low] == arr[mid] && arr[mid] == arr[high]) {
                low++;
                high--;
                continue;
            }

            if (arr[low] <= arr[mid]) {
                if (target >= arr[low] && target < arr[mid]) {
                    high = mid - 1;
                } else {
                    low = mid + 1;
                }
            } else {
                if (target > arr[mid] && target <= arr[high]) {
                    low = mid + 1;
                } else {
                    high = mid - 1;
                }
            }
        }

        return false;
    }
}
```

## Complete Demo

```java
public class FirstLastRotatedDemo {
    public static void main(String[] args) {
        int[] arr = {1, 2, 2, 2, 3, 4, 5, 5, 6};

        System.out.println("First occurrence of 2: " +
            FirstOccurrence.firstOccurrence(arr, 2));
        System.out.println("Last occurrence of 2: " +
            LastOccurrence.lastOccurrence(arr, 2));
        System.out.println("Count of 2: " +
            CountOccurrences.countOccurrences(arr, 2));

        // Mountain array
        int[] mountain = {1, 3, 5, 7, 6, 4, 2};
        System.out.println("Peak index: " +
            PeakIndexInMountainArray.peakIndexInMountainArray(mountain));

        // Rotated array
        int[] rotated = {4, 5, 6, 7, 0, 1, 2};
        System.out.println("Min in rotated: " +
            FindMinInRotatedSortedArray.findMin(rotated));
        System.out.println("Search for 0: " +
            SearchInRotatedSortedArray.search(rotated, 0));
        System.out.println("Search for 3: " +
            SearchInRotatedSortedArray.search(rotated, 3));
    }
}
```

## Key Patterns Summary

| Problem | Approach | Key Condition |
|---------|----------|--------------|
| First occurrence | Binary search, don't stop at match, move left | `arr[mid] == target → high = mid-1` |
| Last occurrence | Binary search, don't stop at match, move right | `arr[mid] == target → low = mid+1` |
| Count occurrences | last - first + 1 | Use first + last or ub - lb |
| Peak in mountain | Compare mid with mid+1 | `arr[mid] < arr[mid+1] → low=mid+1` else `high=mid` |
| Min in rotated | Compare mid with high | `arr[mid] > arr[high] → low=mid+1` else `high=mid` |
| Search in rotated | Find sorted half, check if target in it | Check `arr[low] <= arr[mid]` for left sorted |
