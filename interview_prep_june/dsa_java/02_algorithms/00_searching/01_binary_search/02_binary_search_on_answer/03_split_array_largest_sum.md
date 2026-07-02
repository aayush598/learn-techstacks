# Split Array Largest Sum

## Problem Statement

Given an integer array `nums` and an integer `k`, split the array into `k` non-empty contiguous subarrays such that the **largest sum** among them is **minimized**. Return the minimized largest sum.

This is exactly the Book Allocation problem with different naming. Let's implement it with a focus on this specific problem since it's a LeetCode favorite.

## Implementation

```java
public class SplitArrayLargestSum {
    public static void main(String[] args) {
        int[] nums = {7, 2, 5, 10, 8};
        int k = 2;
        System.out.println("Minimized largest sum: " +
            splitArray(nums, k));
        // Output: 18
        // Explanation: Split as [7,2,5] = 14 and [10,8] = 18, largest = 18
    }

    public static int splitArray(int[] nums, int k) {
        int low = 0;
        int high = 0;

        for (int num : nums) {
            low = Math.max(low, num);  // At least max single element
            high += num;               // At most sum of all
        }

        int ans = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (canSplit(nums, k, mid)) {
                ans = mid;          // mid works, try smaller
                high = mid - 1;
            } else {
                low = mid + 1;      // mid doesn't work, need larger
            }
        }

        return ans;
    }

    private static boolean canSplit(int[] nums, int k, int maxSum) {
        int subarrays = 1;   // At least one subarray
        int currentSum = 0;

        for (int num : nums) {
            // If a single element > maxSum, impossible
            if (num > maxSum) return false;

            if (currentSum + num <= maxSum) {
                currentSum += num;
            } else {
                subarrays++;
                currentSum = num;

                if (subarrays > k) {
                    return false;
                }
            }
        }

        return true;
    }
}
```

## Detailed Dry Run

```
nums = [7, 2, 5, 10, 8], k = 2

Search range: low=10 (max), high=32 (sum)

mid = 21: Can split with max sum ≤ 21?
  [7+2+5+10=24] > 21 → split
  [7+2+5=14] ≤ 21, [10+8=18] ≤ 21
  subarrays = 2 ≤ 2 → YES, ans=21, high=20

mid = 15: Can split with max sum ≤ 15?
  [7+2+5=14] ≤ 15, [10+8=18] > 15 → split
  [7+2+5=14], [10], [8] → subarrays=3 > 2 → NO, low=16

mid = 18: Can split with max sum ≤ 18?
  [7+2+5=14] ≤ 18, [10+8=18] ≤ 18
  subarrays = 2 ≤ 2 → YES, ans=18, high=17

mid = 16: Can split with max sum ≤ 16?
  [7+2+5=14] ≤ 16, [10+8=18] > 16 → split
  [7+2+5=14], [10], [8] → subarrays=3 > 2 → NO, low=17

mid = 17: Can split with max sum ≤ 17?
  [7+2+5=14] ≤ 17, [10+8=18] > 17 → split
  [7+2+5=14], [10], [8] → subarrays=3 > 2 → NO, low=18

low=18 > high=17, exit → ans=18
```

## Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(N log S) where S = sum(nums) |
| Space | O(1) |
| Search space size | sum - max ≈ sum (for large arrays) |
| Feasibility check | O(N) per iteration |

## LeetCode Submissions and Variations

```java
public class SplitArrayVariants {
    // LeetCode 410: Split Array Largest Sum
    public int splitArray(int[] nums, int k) {
        return splitArrayHelper(nums, k);
    }

    // LeetCode 1011: Capacity To Ship Packages Within D Days
    public int shipWithinDays(int[] weights, int days) {
        return splitArrayHelper(weights, days);
    }

    // LeetCode 875: Koko Eating Bananas
    public int minEatingSpeed(int[] piles, int h) {
        int low = 1;
        int high = 0;
        for (int p : piles) high = Math.max(high, p);

        while (low < high) {
            int mid = low + (high - low) / 2;
            int hours = 0;
            for (int p : piles) {
                hours += (p + mid - 1) / mid;  // ceil division
            }
            if (hours <= h) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }
        return low;
    }
}
```

## Key Differences from Book Allocation

| Aspect | Book Allocation | Split Array Largest Sum |
|--------|----------------|------------------------|
| Input | pages array + students | nums array + k |
| Constraint | contiguous books | contiguous subarrays |
| Objective | minimize max pages | minimize max sum |
| Same | ✓ | ✓ |

Both are identical in logic. The only difference is context and problem framing.

## DFS + Memoization Alternative (for small n)

```java
public class SplitArrayDFS {
    // DP approach for understanding (O(n²*k) time)
    public static int splitArrayDP(int[] nums, int k) {
        int n = nums.length;
        int[][] dp = new int[n + 1][k + 1];
        int[] prefixSum = new int[n + 1];

        for (int i = 1; i <= n; i++) {
            prefixSum[i] = prefixSum[i - 1] + nums[i - 1];
        }

        for (int i = 0; i <= n; i++) {
            Arrays.fill(dp[i], Integer.MAX_VALUE);
        }

        dp[0][0] = 0;

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= Math.min(i, k); j++) {
                for (int p = j - 1; p < i; p++) {
                    int currentSum = prefixSum[i] - prefixSum[p];
                    dp[i][j] = Math.min(dp[i][j],
                        Math.max(dp[p][j - 1], currentSum));
                }
            }
        }

        return dp[n][k];
    }
}
```

The DP approach is O(n² * k), which is worse than binary search O(N log S). The binary search approach is preferred for this problem.

## When to Use Binary Search Over DP

| Criteria | Binary Search | DP |
|----------|--------------|-----|
| n ≤ 100 | Either works | DP works |
| n ≤ 10⁵ | Binary search | DP too slow |
| Need exact min max | Binary search | DP |
| Understanding structure | - | Better |
