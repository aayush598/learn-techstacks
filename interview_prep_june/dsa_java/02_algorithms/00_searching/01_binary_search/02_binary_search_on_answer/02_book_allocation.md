# Book Allocation Problem

## Problem Statement

Given N books (with pages[i] pages each) and M students, allocate all books to students **contiguously** such that the **maximum number of pages assigned to a student is minimized**.

**Constraints:**
- Each student gets at least one book
- Books are allocated contiguously (a student gets a consecutive range)
- All books must be allocated

**Search space:** [max(pages), sum(pages)]
- Low = max pages of a single book (each student gets at least one book)
- High = sum of all pages (one student gets all books)

## Implementation

```java
public class BookAllocation {
    public static void main(String[] args) {
        int[] books = {12, 34, 67, 90};
        int students = 2;
        System.out.println("Minimum max pages: " +
            allocateBooks(books, students));
        // Output: 113
    }

    public static int allocateBooks(int[] books, int students) {
        // If more students than books, impossible
        if (students > books.length) return -1;

        int low = 0;
        int high = 0;

        // Set search range
        for (int pages : books) {
            low = Math.max(low, pages);  // Max single book
            high += pages;               // Sum of all books
        }

        int ans = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (isFeasible(books, students, mid)) {
                ans = mid;          // mid works, try smaller max
                high = mid - 1;
            } else {
                low = mid + 1;      // mid doesn't work, need larger max
            }
        }

        return ans;
    }

    // Check if we can allocate books with max pages <= limit
    private static boolean isFeasible(int[] books, int students, int limit) {
        int count = 1;          // Start with first student
        int currentSum = 0;

        for (int pages : books) {
            // If a single book exceeds limit, impossible
            if (pages > limit) return false;

            if (currentSum + pages <= limit) {
                currentSum += pages;
            } else {
                count++;                 // Assign to next student
                currentSum = pages;

                if (count > students) {
                    return false;        // Too many students needed
                }
            }
        }

        return true;
    }
}
```

## Dry Run

```
books = [12, 34, 67, 90], students = 2

Search range: low=90 (max page), high=203 (sum of all)

mid=146: Can allocate with max=146?
  Student 1: 12+34+67=113 ≤ 146
  Student 2: 90 ≤ 146
  count=2 ≤ 2 → YES, ans=146, high=145

mid=117: Can allocate with max=117?
  Student 1: 12+34+67=113 ≤ 117
  Student 2: 90 ≤ 117
  count=2 ≤ 2 → YES, ans=117, high=116

mid=103: Can allocate with max=103?
  Student 1: 12+34=46 ≤ 103
  Student 2: 67 ≤ 103
  Student 3: 90 ≤ 103
  count=3 > 2 → NO, low=104

mid=110: Can allocate with max=110?
  Student 1: 12+34+67=113 > 110 → 12+34=46
  Student 2: 67+90=157 > 110 → 67
  Student 3: 90
  count=3 > 2 → NO, low=111

mid=113: Can allocate with max=113?
  Student 1: 12+34+67=113 ≤ 113
  Student 2: 90 ≤ 113
  count=2 ≤ 2 → YES, ans=113, high=112

mid=112: Can allocate with max=112?
  Student 1: 12+34+67=113 > 112 → 12+34=46
  Student 2: 67+90=157 > 112 → 67
  Student 3: 90
  count=3 > 2 → NO, low=113

low=113 > high=112, exit → ans=113
```

## Complexity

| Operation | Complexity |
|-----------|------------|
| Setting search range | O(N) |
| Binary search | O(log(sum)) |
| Feasibility check per iteration | O(N) |
| Total | O(N log sum) |
| Space | O(1) |

## Edge Cases

```java
public class BookAllocationEdgeCases {
    // More students than books: impossible
    public static int allocateBooks(int[] books, int students) {
        if (students > books.length) return -1;

        int low = 0, high = 0;
        for (int pages : books) {
            low = Math.max(low, pages);
            high += pages;
        }

        // When students == 1, answer is sum of all pages
        if (students == 1) return high;

        // When students == books.length, answer is max page
        if (students == books.length) return low;

        int ans = -1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (isFeasible(books, students, mid)) {
                ans = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return ans;
    }

    // Check if single book exceeds limit early
    private static boolean isFeasible(int[] books, int students, int limit) {
        int count = 1;
        int sum = 0;

        for (int pages : books) {
            if (pages > limit) return false;
            if (sum + pages > limit) {
                count++;
                sum = pages;
                if (count > students) return false;
            } else {
                sum += pages;
            }
        }

        return true;
    }
}
```

## Variations and Similar Problems

### Split Array Largest Sum (LeetCode 410)
Exactly the same as book allocation. Given an array, split into K subarrays to minimize the largest sum.

```java
public class SplitArrayLargestSum {
    public int splitArray(int[] nums, int k) {
        return new BookAllocation().allocateBooks(nums, k);
    }
}
```

### Capacity To Ship Packages Within D Days (LeetCode 1011)
Same pattern — find minimum ship capacity to ship all packages within D days.

```java
public class ShipWithinDays {
    public static int shipWithinDays(int[] weights, int days) {
        int low = 0, high = 0;
        for (int w : weights) {
            low = Math.max(low, w);
            high += w;
        }

        // Same binary search as book allocation
        int ans = -1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (canShip(weights, days, mid)) {
                ans = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return ans;
    }

    private static boolean canShip(int[] weights, int days, int capacity) {
        int count = 1;
        int sum = 0;
        for (int w : weights) {
            if (sum + w > capacity) {
                count++;
                sum = w;
                if (count > days) return false;
            } else {
                sum += w;
            }
        }
        return true;
    }
}
```

## Key Pattern Recognition

**"Minimize the maximum" problems:**
1. The search space is [max_element, sum_of_elements]
2. The feasibility function checks if we can partition with max sum ≤ limit
3. Binary search finds the minimum feasible limit
4. The greedy allocation always assigns as many as possible to current partition

| Problem | Array | Partitions | Feasibility Logic |
|---------|-------|------------|-------------------|
| Book Allocation | pages | students | Contiguous books to each student |
| Split Array | nums | k | Contiguous subarrays |
| Ship Packages | weights | days | Packages shipped each day |
| Split Wood | wood lengths | cuts | Pieces from each wood |
