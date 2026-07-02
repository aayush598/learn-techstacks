# Floor and Ceiling in Sorted Array

## Floor: Largest Element <= Target

The floor of a target is the greatest element in the array that is less than or equal to the target.

```java
public class FloorInSortedArray {
    public static int floor(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;
        int result = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] <= target) {
                // arr[mid] could be the floor (it's <= target)
                // Save it and look for a larger one on the right
                result = arr[mid];
                low = mid + 1;
            } else {
                // arr[mid] > target, floor must be on the left
                high = mid - 1;
            }
        }

        return result;  // -1 if no floor exists (all elements > target)
    }

    // Return index instead of value
    public static int floorIndex(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;
        int result = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] <= target) {
                result = mid;
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }

        return result;
    }
}
```

## Ceil: Smallest Element >= Target

The ceiling of a target is the smallest element in the array that is greater than or equal to the target.

```java
public class CeilInSortedArray {
    public static int ceil(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;
        int result = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] >= target) {
                // arr[mid] could be the ceil (it's >= target)
                // Save it and look for a smaller one on the left
                result = arr[mid];
                high = mid - 1;
            } else {
                // arr[mid] < target, ceil must be on the right
                low = mid + 1;
            }
        }

        return result;  // -1 if no ceil exists (all elements < target)
    }

    // Return index instead of value
    public static int ceilIndex(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;
        int result = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] >= target) {
                result = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }

        return result;
    }
}
```

## Find the Smallest Letter Greater Than Target

This is a ceiling problem on a circular sorted array of letters.

```java
public class SmallestLetterGreaterThanTarget {
    // Letters wrap around: if target >= last letter, return first letter
    public static char nextGreatestLetter(char[] letters, char target) {
        int low = 0;
        int high = letters.length;

        while (low < high) {
            int mid = low + (high - low) / 2;

            if (letters[mid] > target) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }

        // If low == letters.length, wrap around to first element
        return letters[low % letters.length];
    }
}
```

## Find Position Where to Insert (Insert Position)

Given a sorted array and a target, find the index where target should be inserted to maintain order. This is exactly the **lower bound**.

```java
public class SearchInsertPosition {
    public static int searchInsert(int[] arr, int target) {
        int low = 0;
        int high = arr.length;

        while (low < high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] >= target) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }

        return low;  // Insert position
    }

    // Alternative implementation with inclusive bounds
    public static int searchInsertInclusive(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }

        return low;  // When loop ends, low is the insert position
    }
}
```

## Closest Element to Target in Sorted Array

Find the element in the sorted array closest to the target. If two are equally close, return the smaller one.

```java
public class ClosestElement {
    public static int closestElement(int[] arr, int target) {
        int n = arr.length;

        // Edge cases
        if (target <= arr[0]) return arr[0];
        if (target >= arr[n - 1]) return arr[n - 1];

        // Binary search to find the closest
        int low = 0;
        int high = n - 1;

        while (low < high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] == target) {
                return arr[mid];
            }

            if (arr[mid] < target) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }

        // After loop, low is the ceil (smallest >= target)
        // Compare arr[low] (ceil) and arr[low-1] (floor)
        if (Math.abs(arr[low] - target) < Math.abs(arr[low - 1] - target)) {
            return arr[low];
        } else {
            return arr[low - 1];
        }
    }

    // Find K closest elements to target (return in sorted order)
    public static List<Integer> findClosestElements(int[] arr, int k, int target) {
        int n = arr.length;

        // Binary search to find the insert position of target
        int pos = SearchInsertPosition.searchInsert(arr, target);

        // Two pointers expanding outward
        int left = pos - 1;
        int right = pos;

        List<Integer> result = new ArrayList<>();

        while (result.size() < k) {
            if (left < 0) {
                result.add(arr[right++]);
            } else if (right >= n) {
                result.add(arr[left--]);
            } else if (Math.abs(arr[left] - target) <= Math.abs(arr[right] - target)) {
                result.add(arr[left--]);
            } else {
                result.add(arr[right++]);
            }
        }

        Collections.sort(result);
        return result;
    }
}
```

## Complete Demo

```java
public class FloorCeilDemo {
    public static void main(String[] args) {
        int[] arr = {1, 3, 5, 7, 9, 11};

        System.out.println("Array: " + Arrays.toString(arr));

        // Floor tests
        System.out.println("\nFloor:");
        System.out.println("Floor of 4: " + FloorInSortedArray.floor(arr, 4));
        System.out.println("Floor of 5: " + FloorInSortedArray.floor(arr, 5));
        System.out.println("Floor of 0: " + FloorInSortedArray.floor(arr, 0));
        System.out.println("Floor of 12: " + FloorInSortedArray.floor(arr, 12));

        // Ceil tests
        System.out.println("\nCeil:");
        System.out.println("Ceil of 4: " + CeilInSortedArray.ceil(arr, 4));
        System.out.println("Ceil of 5: " + CeilInSortedArray.ceil(arr, 5));
        System.out.println("Ceil of 0: " + CeilInSortedArray.ceil(arr, 0));
        System.out.println("Ceil of 12: " + CeilInSortedArray.ceil(arr, 12));

        // Insert position
        System.out.println("\nInsert Position:");
        System.out.println("Insert 4: " + SearchInsertPosition.searchInsert(arr, 4));
        System.out.println("Insert 5: " + SearchInsertPosition.searchInsert(arr, 5));
        System.out.println("Insert 0: " + SearchInsertPosition.searchInsert(arr, 0));
        System.out.println("Insert 12: " + SearchInsertPosition.searchInsert(arr, 12));

        // Closest element
        System.out.println("\nClosest Element:");
        System.out.println("Closest to 4: " + ClosestElement.closestElement(arr, 4));
        System.out.println("Closest to 6: " + ClosestElement.closestElement(arr, 6));
        System.out.println("Closest to 10: " + ClosestElement.closestElement(arr, 10));

        // K closest elements
        System.out.println("\n3 Closest to 4: " +
            ClosestElement.findClosestElements(arr, 3, 4));

        // Smallest letter greater than target
        char[] letters = {'c', 'f', 'j'};
        System.out.println("\nSmallest letter > 'a': " +
            SmallestLetterGreaterThanTarget.nextGreatestLetter(letters, 'a'));
        System.out.println("Smallest letter > 'c': " +
            SmallestLetterGreaterThanTarget.nextGreatestLetter(letters, 'c'));
        System.out.println("Smallest letter > 'z': " +
            SmallestLetterGreaterThanTarget.nextGreatestLetter(letters, 'z'));
    }
}
```

## Key Insights

| Problem | Maps To | Return Value |
|---------|---------|--------------|
| Floor | Largest ≤ target | arr[lb - 1] or -1 |
| Ceil | Smallest ≥ target | arr[lb] or -1 |
| Next greater letter | Ceil with wrap | arr[lb % n] |
| Insert position | Lower bound of target | lb |
| K closest elements | Binary search + two pointers | Window of size k |

**Notes:**
- Floor and ceiling are inverse operations: floor of target = arr[lowerBound(target) - 1] if lowerBound > 0
- Ceil of target = arr[lowerBound(target)] if lowerBound < n
- Insert position = lowerBound(target) when target not present
- For the smallest letter greater than target, it's `upperBound(target)` since we need > not >=
