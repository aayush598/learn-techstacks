# Search in Rotated Sorted Array

## Problem Context

A sorted array is rotated at some unknown pivot. Example: `[0,1,2,4,5,6,7]` rotated at index 3 becomes `[4,5,6,7,0,1,2]`.

## Find Minimum in Rotated Sorted Array (Distinct)

```java
public class FindMinInRotatedSortedArray {
    public static int findMin(int[] arr) {
        int low = 0;
        int high = arr.length - 1;

        // If not rotated, first element is min
        if (arr[low] <= arr[high]) {
            return arr[low];
        }

        while (low < high) {
            int mid = low + (high - low) / 2;

            // If mid > high, min is in right half [mid+1, high]
            // Otherwise, min is in left half [low, mid]
            if (arr[mid] > arr[high]) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }

        return arr[low];
    }

    // Alternative: compare adjacent elements
    public static int findMinByPivot(int[] arr) {
        int low = 0;
        int high = arr.length - 1;

        while (low < high) {
            int mid = low + (high - low) / 2;

            // If mid > mid+1, then mid+1 is the minimum
            if (arr[mid] > arr[mid + 1]) {
                return arr[mid + 1];
            }

            // If mid-1 > mid, then mid is the minimum
            if (mid > 0 && arr[mid - 1] > arr[mid]) {
                return arr[mid];
            }

            if (arr[mid] > arr[low]) {
                // Left half is sorted, min is in the right half
                low = mid + 1;
            } else {
                // Right half is sorted, min is in the left half
                high = mid - 1;
            }
        }

        return arr[0];  // Array is not rotated
    }
}
```

## Find Minimum in Rotated Sorted Array (With Duplicates)

When duplicates exist, `arr[mid] == arr[high]` creates ambiguity. We shrink the search space by decrementing `high`.

```java
public class FindMinInRotatedSortedArrayDuplicates {
    public static int findMin(int[] arr) {
        int low = 0;
        int high = arr.length - 1;

        while (low < high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] > arr[high]) {
                // Min is in the right half
                low = mid + 1;
            } else if (arr[mid] < arr[high]) {
                // Min is in the left half (or at mid)
                high = mid;
            } else {
                // arr[mid] == arr[high], can't decide
                high--;  // Shrink search space
            }
        }

        return arr[low];
    }
}
```

**Why `high--` works:** If `arr[mid] == arr[high]`:
- If the minimum is at position `high`, we'd still find it (the min exists at multiple positions)
- If the min is elsewhere, decrementing `high` doesn't remove the candidate
- This approach has worst-case O(n) when all elements are equal

## Search Target in Rotated Sorted Array

### Without Duplicates

```java
public class SearchInRotatedSortedArray {
    public static int search(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] == target) return mid;

            // Determine which half is sorted
            if (arr[low] <= arr[mid]) {
                // Left half [low, mid] is sorted
                if (target >= arr[low] && target < arr[mid]) {
                    high = mid - 1;  // Target is in left sorted half
                } else {
                    low = mid + 1;   // Target is in right half
                }
            } else {
                // Right half [mid, high] is sorted
                if (target > arr[mid] && target <= arr[high]) {
                    low = mid + 1;   // Target is in right sorted half
                } else {
                    high = mid - 1;  // Target is in left half
                }
            }
        }

        return -1;
    }
}
```

### With Duplicates

```java
public class SearchInRotatedSortedArrayDuplicates {
    public static boolean search(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] == target) return true;

            // Handle duplicates: if arr[low] == arr[mid] == arr[high]
            if (arr[low] == arr[mid] && arr[mid] == arr[high]) {
                low++;
                high--;
                continue;
            }

            // Standard rotated array logic
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

### Two-Pass Approach: Find Pivot Then Binary Search

```java
public class SearchInRotatedSortedArrayTwoPass {
    public static int search(int[] arr, int target) {
        int n = arr.length;

        // Step 1: Find the pivot (index of minimum)
        int pivot = findPivot(arr);

        // Step 2: Binary search in the appropriate half
        if (target >= arr[pivot] && target <= arr[n - 1]) {
            return binarySearch(arr, target, pivot, n - 1);
        } else {
            return binarySearch(arr, target, 0, pivot - 1);
        }
    }

    private static int findPivot(int[] arr) {
        int low = 0;
        int high = arr.length - 1;

        while (low < high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] > arr[high]) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }

        return low;  // Index of minimum element
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

## Count Rotations (Index of Minimum)

The number of rotations equals the index of the minimum element.

```java
public class CountRotations {
    public static int countRotations(int[] arr) {
        int low = 0;
        int high = arr.length - 1;

        // If not rotated
        if (arr[low] <= arr[high]) return 0;

        while (low <= high) {
            int mid = low + (high - low) / 2;
            int next = (mid + 1) % arr.length;
            int prev = (mid - 1 + arr.length) % arr.length;

            // Check if mid is the minimum
            if (arr[mid] <= arr[prev] && arr[mid] <= arr[next]) {
                return mid;  // Number of rotations = index of min
            }

            if (arr[mid] <= arr[high]) {
                high = mid - 1;
            } else if (arr[mid] >= arr[low]) {
                low = mid + 1;
            }
        }

        return 0;
    }

    // Simpler: find minimum index
    public static int countRotationsSimple(int[] arr) {
        int low = 0;
        int high = arr.length - 1;

        while (low < high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] > arr[high]) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }

        return low;
    }
}
```

## Complete Demo

```java
public class RotatedArrayDemo {
    public static void main(String[] args) {
        // Test distinct arrays
        int[] arr1 = {4, 5, 6, 7, 0, 1, 2};
        System.out.println("Array: " + Arrays.toString(arr1));

        System.out.println("Min: " +
            FindMinInRotatedSortedArray.findMin(arr1));
        System.out.println("Rotations: " +
            CountRotations.countRotations(arr1));

        System.out.println("Search for 0: " +
            SearchInRotatedSortedArray.search(arr1, 0));
        System.out.println("Search for 3: " +
            SearchInRotatedSortedArray.search(arr1, 3));

        // Test with duplicates
        int[] arr2 = {2, 2, 2, 0, 2, 2};
        System.out.println("\nWith duplicates: " + Arrays.toString(arr2));
        System.out.println("Min: " +
            FindMinInRotatedSortedArrayDuplicates.findMin(arr2));
        System.out.println("Search for 0: " +
            SearchInRotatedSortedArrayDuplicates.search(arr2, 0));

        // Edge cases
        int[] arr3 = {1};
        System.out.println("\nSingle element: " + Arrays.toString(arr3));
        System.out.println("Min: " +
            FindMinInRotatedSortedArray.findMin(arr3));

        int[] arr4 = {1, 3};
        System.out.println("\nTwo elements: " + Arrays.toString(arr4));
        System.out.println("Min: " +
            FindMinInRotatedSortedArray.findMin(arr4));

        int[] arr5 = {1, 2, 3, 4, 5};
        System.out.println("\nNot rotated: " + Arrays.toString(arr5));
        System.out.println("Min: " +
            FindMinInRotatedSortedArray.findMin(arr5));
        System.out.println("Rotations: " +
            CountRotations.countRotations(arr5));
    }
}
```

## Complexity Analysis

| Problem | Time | Space | Notes |
|---------|------|-------|-------|
| Min in rotated (distinct) | O(log n) | O(1) | Standard binary search |
| Min in rotated (duplicates) | O(log n) avg, O(n) worst | O(1) | Worst case when all equal |
| Search in rotated (distinct) | O(log n) | O(1) | One-pass binary search |
| Search in rotated (duplicates) | O(log n) avg, O(n) worst | O(1) | Need to skip equal elements |
| Count rotations | O(log n) | O(1) | Same as finding min index |

## Key Insight

The key observation for rotated array problems: **At least one half is always sorted** (completely). By checking `arr[low] <= arr[mid]`, we can determine which half is sorted and eliminate accordingly.

```
Original: [0, 1, 2, 4, 5, 6, 7]
Rotated:  [4, 5, 6, 7, 0, 1, 2]
            ^        ^
            low      mid = (0+6)/2 = 3
            arr[low]=4 <= arr[mid]=7 => left half is sorted
```
