# Binary Search Patterns

## Table of Contents
1. Classic Binary Search (Find Exact)
2. Lower Bound (First ≥ Target)
3. Upper Bound (First > Target)
4. Search in Rotated Array
5. Binary Search on Answer (Minimize Max, Maximize Min)
6. Binary Search on 2D Matrix
7. Pattern: Monotonic Feasibility Function
8. Common Mistakes and Pitfalls

---

## 1. Classic Binary Search (Find Exact)

**When to use:** Sorted array, need to find exact target.

**Template:**
```java
public int binarySearch(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2; // avoid overflow
        if (nums[mid] == target) {
            return mid;
        } else if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1; // not found
}
```

**Recursive version:**
```java
public int binarySearchRec(int[] nums, int target, int left, int right) {
    if (left > right) return -1;
    int mid = left + (right - left) / 2;
    if (nums[mid] == target) return mid;
    if (nums[mid] < target) return binarySearchRec(nums, target, mid + 1, right);
    return binarySearchRec(nums, target, left, mid - 1);
}
```

**Key variations:**
- `while (left <= right)` → finds exact, returns index or -1
- `while (left < right)` → narrows to single element, used in boundary search
- `int mid = left + (right - left) / 2;` → avoids integer overflow
- `int mid = left + (right - left + 1) / 2;` → upper mid, avoids infinite loop

---

## 2. Lower Bound (First ≥ Target)

**When to use:** Find first position where value >= target. Insert position for sorted array.

**Template:**
```java
public int lowerBound(int[] nums, int target) {
    int left = 0, right = nums.length; // not length - 1
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] >= target) {
            right = mid; // mid qualifies, search left
        } else {
            left = mid + 1; // mid too small, search right
        }
    }
    return left; // first index where value >= target
}
```

**Example:**
```java
// Find first bad version
public int firstBadVersion(int n) {
    int left = 1, right = n;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (isBadVersion(mid)) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    return left;
}
```

---

## 3. Upper Bound (First > Target)

**When to use:** Find first position where value > target. Count occurrences: upperBound - lowerBound.

**Template:**
```java
public int upperBound(int[] nums, int target) {
    int left = 0, right = nums.length;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] > target) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    return left; // first index where value > target
}
```

**Count occurrences of target:**
```java
public int countOccurrences(int[] nums, int target) {
    int lb = lowerBound(nums, target);
    int ub = upperBound(nums, target);
    return ub - lb; // if array is sorted
}
```

**Find first and last position:**
```java
public int[] searchRange(int[] nums, int target) {
    int first = lowerBound(nums, target);
    if (first == nums.length || nums[first] != target) return new int[]{-1, -1};
    int last = upperBound(nums, target) - 1;
    return new int[]{first, last};
}
```

---

## 4. Search in Rotated Array

**When to use:** Array was sorted then rotated. Find target in O(log n).

**Key insight:** At any mid, one half is always fully sorted. Check which half is sorted, then decide where target lies.

**Template:**
```java
public int searchRotated(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;

        // Left half is sorted
        if (nums[left] <= nums[mid]) {
            if (target >= nums[left] && target < nums[mid]) {
                right = mid - 1; // target in left half
            } else {
                left = mid + 1; // target in right half
            }
        }
        // Right half is sorted
        else {
            if (target > nums[mid] && target <= nums[right]) {
                left = mid + 1; // target in right half
            } else {
                right = mid - 1; // target in left half
            }
        }
    }
    return -1;
}
```

**Find minimum in rotated array:**
```java
public int findMin(int[] nums) {
    int left = 0, right = nums.length - 1;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] > nums[right]) {
            left = mid + 1; // min is in right half
        } else {
            right = mid; // min is in left half (including mid)
        }
    }
    return nums[left];
}
```

**Search in rotated array with duplicates:**
```java
public boolean searchRotatedDuplicates(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return true;

        // Handle duplicates: can't determine which half is sorted
        if (nums[left] == nums[mid] && nums[mid] == nums[right]) {
            left++;
            right--;
        } else if (nums[left] <= nums[mid]) {
            if (target >= nums[left] && target < nums[mid]) right = mid - 1;
            else left = mid + 1;
        } else {
            if (target > nums[mid] && target <= nums[right]) left = mid + 1;
            else right = mid - 1;
        }
    }
    return false;
}
```

---

## 5. Binary Search on Answer (Minimize Max / Maximize Min)

**When to use:** When the answer space is monotonic and you can test feasibility of a candidate answer.

The most common form is:
- **Minimize the maximum value** (e.g., split array largest sum)
- **Maximize the minimum value** (e.g., aggressive cows)

### Core Template
```java
public int binarySearchOnAnswer(int[] arr) {
    int left = possibleMinimum;
    int right = possibleMaximum;

    while (left < right) {
        int mid = left + (right - left) / 2;
        if (feasible(mid, arr)) {
            right = mid; // or left = mid + 1, depending on min/max
        } else {
            left = mid + 1; // or right = mid
        }
    }
    return left;
}

boolean feasible(int candidate, int[] arr) {
    // Returns true if candidate can be the answer
    // This is the monotonic check function
}
```

### Pattern: Minimize Maximum
```java
// Given an array, split into k subarrays to minimize the max sum
public int splitArray(int[] nums, int k) {
    int left = 0, right = 0;
    for (int num : nums) {
        left = Math.max(left, num);  // min possible: largest single element
        right += num;                 // max possible: sum of all elements
    }

    while (left < right) {
        int mid = left + (right - left) / 2;
        if (canSplit(nums, k, mid)) {
            right = mid; // try smaller max
        } else {
            left = mid + 1;
        }
    }
    return left;
}

boolean canSplit(int[] nums, int k, int maxSum) {
    int count = 1, currentSum = 0;
    for (int num : nums) {
        currentSum += num;
        if (currentSum > maxSum) {
            count++;
            currentSum = num;
            if (count > k) return false;
        }
    }
    return true;
}
```

### Pattern: Maximize Minimum
```java
// Place k cows in stalls to maximize minimum distance
public int aggressiveCows(int[] stalls, int k) {
    Arrays.sort(stalls);
    int left = 1; // minimum possible distance
    int right = stalls[stalls.length - 1] - stalls[0]; // max possible distance

    while (left < right) {
        int mid = left + (right - left + 1) / 2; // upper mid for maximize pattern
        if (canPlace(stalls, k, mid)) {
            left = mid; // try larger distance
        } else {
            right = mid - 1;
        }
    }
    return left;
}

boolean canPlace(int[] stalls, int k, int minDist) {
    int count = 1, last = stalls[0];
    for (int i = 1; i < stalls.length; i++) {
        if (stalls[i] - last >= minDist) {
            count++;
            last = stalls[i];
            if (count >= k) return true;
        }
    }
    return false;
}
```

### Common Binary Search on Answer Problems

| Problem | Search Space | Feasibility Check | Pattern |
|---------|-------------|-------------------|---------|
| Koko eating bananas | [1, max(piles)] | Can eat all in H hours with rate k | Min max |
| Split array largest sum | [max(nums), sum(nums)] | Can split into k parts with max ≤ mid | Min max |
| Aggressive cows | [1, max-min] | Can place cows with min dist ≥ mid | Max min |
| Book allocation | [max(pages), sum(pages)] | Can allocate with max ≤ mid | Min max |
| Smallest divisor | [1, max(nums)] | Can divide all within threshold | Min max |
| Min time to repair | [1, max(time)*cars²] | Can repair all cars in mid time | Min max |
| Capacity to ship packages | [max(w), sum(w)] | Can ship in D days | Min max |
| Kth smallest pair distance | [0, max-min] | Count pairs with dist ≤ mid | Two-pointer check |

---

## 6. Binary Search on 2D Matrix

### Search in row-wise and column-wise sorted matrix
```java
public boolean searchMatrix(int[][] matrix, int target) {
    int rows = matrix.length, cols = matrix[0].length;
    int row = 0, col = cols - 1;
    while (row < rows && col >= 0) {
        if (matrix[row][col] == target) return true;
        if (matrix[row][col] < target) row++;
        else col--;
    }
    return false;
}
```

### Search in fully sorted 2D matrix (treat as 1D)
```java
public boolean searchMatrix(int[][] matrix, int target) {
    int rows = matrix.length, cols = matrix[0].length;
    int left = 0, right = rows * cols - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        int midVal = matrix[mid / cols][mid % cols];
        if (midVal == target) return true;
        if (midVal < target) left = mid + 1;
        else right = mid - 1;
    }
    return false;
}
```

### Find Kth smallest in sorted matrix
```java
public int kthSmallest(int[][] matrix, int k) {
    int n = matrix.length;
    int left = matrix[0][0], right = matrix[n-1][n-1];
    while (left < right) {
        int mid = left + (right - left) / 2;
        int count = countLessOrEqual(matrix, mid);
        if (count >= k) right = mid;
        else left = mid + 1;
    }
    return left;
}

int countLessOrEqual(int[][] matrix, int target) {
    int count = 0, n = matrix.length;
    int row = n - 1, col = 0;
    while (row >= 0 && col < n) {
        if (matrix[row][col] <= target) {
            count += row + 1;
            col++;
        } else {
            row--;
        }
    }
    return count;
}
```

---

## 7. Pattern: Monotonic Feasibility Function

**This is the master pattern for all binary search variants.** A function `f(x)` is monotonic if it is always non-decreasing or non-increasing.

### Decision Flowchart
```
Is the search space monotonic (sorted array, or f(x) is monotonic)?
├── YES → Binary search applies
│   ├── Is the array sorted?
│   │   ├── YES → Find exact: classic BS
│   │   ├── Lower/upper bound: variant BS
│   │   └── Rotated: detect sorted half
│   └── Is it a "find min/max such that condition holds"?
│       ├── YES → Binary search on answer
│       │   ├── Minimize maximum → feasible(mid) ? right = mid : left = mid + 1
│       │   └── Maximize minimum → feasible(mid) ? left = mid : right = mid - 1
│       └── NO → Not applicable
└── NO → Not applicable, use other method
```

### Identifying Monotonic Feasibility
The check function `f(mid)` must satisfy:
- If `f(mid) = true`, then `f(mid+1) = true` (or vice versa, consistently)
- This creates a partition: false...false, true...true (or true...true, false...false)

### Template for Any Feasibility Function
```java
// Find boundary where function transitions from false to true
int left = LOW, right = HIGH;
while (left < right) {
    int mid = left + (right - left) / 2;
    if (f(mid)) {
        right = mid; // first true is at mid or left
    } else {
        left = mid + 1; // first true is after mid
    }
}
return left; // first index where f(index) is true

// Find boundary where function transitions from true to false
int left = LOW, right = HIGH;
while (left < right) {
    int mid = left + (right - left + 1) / 2; // upper mid
    if (f(mid)) {
        left = mid; // last true is at mid or right
    } else {
        right = mid - 1; // last true is before mid
    }
}
return left; // last index where f(index) is true
```

---

## 8. Common Mistakes and Pitfalls

### Infinite Loops
```java
// WRONG: potential infinite loop when left=mid, right=left+1
while (left < right) {
    int mid = left + (right - left) / 2; // left-mid
    if (feasible(mid)) left = mid; // never changes when left=mid
    else right = mid - 1;
}

// CORRECT for "find last true" pattern
while (left < right) {
    int mid = left + (right - left + 1) / 2; // upper-mid
    if (feasible(mid)) left = mid;
    else right = mid - 1;
}
```

### Memory Aid: When to use upper mid
| Pattern | Condition true | mid formula |
|---------|---------------|-------------|
| Find first true | right = mid | `(left+right)/2` (left-mid) |
| Find last true | left = mid | `(left+right+1)/2` (upper-mid) |

### Off-by-One in Right Boundary
```java
// For lower/upper bound, right = length (exclusive)
int left = 0, right = nums.length; // NOT length - 1
// This allows returning nums.length when all values < target

// For exact search, right = length - 1 (inclusive)
int left = 0, right = nums.length - 1;
```

### Overflow
```java
// WRONG
int mid = (left + right) / 2; // May overflow for large ints

// CORRECT
int mid = left + (right - left) / 2;
```

### Not Handling Duplicates
- Lower bound returns first occurrence
- Upper bound returns after last occurrence
- Classic BS returns any occurrence (not guaranteed which)

### Sorted Array ≠ Only Binary Search
If the array is sorted but you need to find something that can't be decided by comparison (e.g., peak element), binary search may not directly apply (use ternary or linear for peaks).

---

## Quick Reference

| Use Case | Template Variant | Termination |
|----------|-----------------|-------------|
| Find exact target | `while (left <= right)` | `left > right` |
| Lower bound (first ≥) | `while (left < right)` | `left == right` |
| Upper bound (first >) | `while (left < right)` | `left == right` |
| Min max (feasible? right=mid) | `while (left < right)` | `left == right` |
| Max min (feasible? left=mid) | `while (left < right)` with upper mid | `left == right` |
| Rotated search target | `while (left <= right)` with sorted half detection | `left > right` |
| Rotated find min | `while (left < right)` compare mid vs right | `left == right` |
