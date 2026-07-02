# Binary Search Basics

## Concept

Binary search finds the position of a target value in a **sorted** array by repeatedly dividing the search interval in half.

**Time Complexity:** O(log n)  
**Space Complexity:** O(1) iterative, O(log n) recursive  
**Requirement:** Array must be sorted

## Iterative Binary Search

```java
public class BinarySearchIterative {
    public static int binarySearch(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;  // Avoid overflow

            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }

        return -1;
    }
}
```

## Recursive Binary Search

```java
public class BinarySearchRecursive {
    public static int binarySearch(int[] arr, int target) {
        return binarySearch(arr, target, 0, arr.length - 1);
    }

    private static int binarySearch(int[] arr, int target, int low, int high) {
        if (low > high) {
            return -1;
        }

        int mid = low + (high - low) / 2;

        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            return binarySearch(arr, target, mid + 1, high);
        } else {
            return binarySearch(arr, target, low, mid - 1);
        }
    }
}
```

## Mid Calculation: Avoiding Overflow

```java
// WRONG — can overflow for large arrays (near Integer.MAX_VALUE)
int mid = (low + high) / 2;

// CORRECT — avoids overflow
int mid = low + (high - low) / 2;

// ALSO CORRECT — unsigned shift (works for non-negative low/high)
int mid = (low + high) >>> 1;
```

**Why worry?** If `low` and `high` are each ~2¹⁵ or more, `low + high` can exceed `Integer.MAX_VALUE` (2³¹-1), wrapping to a negative number.

## Loop Condition: low <= high vs low < high

### low <= high (Standard)
Used when the search range is `[low, high]` inclusive. We check all elements.

```java
while (low <= high) {
    int mid = low + (high - low) / 2;
    if (arr[mid] == target) return mid;
    if (arr[mid] < target) low = mid + 1;
    else high = mid - 1;
}
return -1;
```

### low < high (Used for boundaries)
Used when narrowing down to a single element. The loop terminates when `low == high`.

```java
// Finding first occurrence or lower bound
while (low < high) {
    int mid = low + (high - low) / 2;
    if (arr[mid] >= target) {
        high = mid;  // mid could be the answer, so don't exclude it
    } else {
        low = mid + 1;
    }
}
return low;  // low == high, the boundary position
```

### When to use which?
- **`low <= high`**: When searching for exact match (standard search)
- **`low < high`**: When searching for boundaries (first/last occurrence, floor/ceil)
- **`low + 1 < high`**: When range must have at least 2 elements (avoid mid = low infinite loop)

## Common Pitfalls

### 1. Infinite Loop with `low < high`

```java
// POTENTIAL INFINITE LOOP
while (low < high) {
    int mid = (low + high) / 2;  // floor mid
    if (condition) {
        low = mid;  // BUG: if low=3, high=4, mid=3, condition true -> low stays 3
    } else {
        high = mid - 1;
    }
}
```

**Fix:** Use `low = mid + 1` when narrowing, or use the ceiling mid: `mid = low + (high - low + 1) / 2`

### 2. Off-by-One Errors

```java
// Correct ranges for each scenario:
// Standard search: arr[mid] < target -> low = mid + 1
//                   arr[mid] > target -> high = mid - 1
// Lower bound:      arr[mid] < target -> low = mid + 1
//                   arr[mid] >= target -> high = mid
// Upper bound:      arr[mid] <= target -> low = mid + 1
//                   arr[mid] > target -> high = mid - 1
```

### 3. Forgetting the Array Must Be Sorted

Binary search only works on sorted arrays. If the array isn't sorted, sort it first (O(n log n)) or use linear search.

### 4. Integer Overflow in Mid Calculation

Always use `low + (high - low) / 2` to avoid overflow.

## Lower Bound and Upper Bound

### Lower Bound (First position where arr[i] >= target)

```java
public class LowerBound {
    public static int lowerBound(int[] arr, int target) {
        int low = 0;
        int high = arr.length;  // Note: high = n, not n-1

        while (low < high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] >= target) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }

        return low;  // First index where arr[idx] >= target
    }
}
```

### Upper Bound (First position where arr[i] > target)

```java
public class UpperBound {
    public static int upperBound(int[] arr, int target) {
        int low = 0;
        int high = arr.length;

        while (low < high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] > target) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }

        return low;  // First index where arr[idx] > target
    }
}
```

### Using Lower and Upper Bound

```java
public class BoundDemo {
    public static void main(String[] args) {
        int[] arr = {1, 2, 2, 2, 3, 4, 5};

        int target = 2;
        int lb = lowerBound(arr, target);
        int ub = upperBound(arr, target);

        System.out.println("Lower bound of " + target + ": " + lb);
        System.out.println("Upper bound of " + target + ": " + ub);
        System.out.println("Count of " + target + ": " + (ub - lb));
        // Check if target exists
        System.out.println("Exists: " + (lb < arr.length && arr[lb] == target));

        // Insert position for a value (when not found)
        int insertPos = lowerBound(arr, 6);  // returns arr.length (6)
        System.out.println("Insert position for 6: " + insertPos);
    }
}
```

## Binary Search Template Reference

```java
public class BinarySearchTemplates {
    // Template 1: Exact match (standard)
    public int exactMatch(int[] arr, int target) {
        int lo = 0, hi = arr.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }

    // Template 2: Lower bound (first >= target)
    public int lowerBound(int[] arr, int target) {
        int lo = 0, hi = arr.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] >= target) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    // Template 3: Upper bound (first > target)
    public int upperBound(int[] arr, int target) {
        int lo = 0, hi = arr.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] > target) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    // Template 4: Search on answer (feasibility)
    public int searchOnAnswer(int lo, int hi) {
        int ans = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (feasible(mid)) {
                ans = mid;
                hi = mid - 1;  // Look for smaller feasible
            } else {
                lo = mid + 1;  // Need larger
            }
        }
        return ans;
    }

    private boolean feasible(int x) {
        return true;  // Problem-specific check
    }
}
```

## Key Takeaways

| Aspect | Binary Search |
|--------|--------------|
| Best Case | O(1) — target at middle |
| Worst Case | O(log n) |
| Space | O(1) iterative, O(log n) recursive |
| Data Requirement | Must be sorted |
| Stable | Yes (positional, depends on variant) |
| When to avoid | Unsorted data, small n, linked lists |

**Remember:** Binary search isn't just for finding a target. It's a general technique for solving problems with monotonic search spaces. If you can answer "is value x feasible?" in O(P) time, and the answer is monotonic (once feasible, always feasible), binary search can find the boundary in O(P log range) time.
