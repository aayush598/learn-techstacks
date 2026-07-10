# Maximum Sum Subarray of Size K

This is the "Hello World" of sliding window problems. It's the simplest possible fixed-size window and the perfect starting point.

## Problem Statement

Given an array of integers and a number `k`, find the maximum sum of any contiguous subarray of size `k`.

```
Input:  arr = [2, 1, 5, 1, 3, 2], k = 3
Output: 9
Explanation: Subarray [5, 1, 3] has sum = 9
```

## The Solution

```java
public int maxSumSubarray(int[] arr, int k) {
    int n = arr.length;
    if (n < k) return -1;

    // Compute sum of first window
    int maxSum = 0;
    for (int i = 0; i < k; i++) {
        maxSum += arr[i];
    }

    // Slide the window
    int windowSum = maxSum;
    for (int i = k; i < n; i++) {
        windowSum += arr[i] - arr[i - k];
        maxSum = Math.max(maxSum, windowSum);
    }

    return maxSum;
}
```

### Dry Run

```
arr = [2, 1, 5, 1, 3, 2], k = 3

First window: sum = 2 + 1 + 5 = 8, maxSum = 8

i=3: sum = 8 + 1 - 2 = 7, maxSum = max(8, 7) = 8
i=4: sum = 7 + 3 - 1 = 9, maxSum = max(8, 9) = 9
i=5: sum = 9 + 2 - 5 = 6, maxSum = max(9, 6) = 9

Result: 9
```

## Return the Subarray Indices

```java
public int[] maxSumSubarrayWithIndices(int[] arr, int k) {
    int n = arr.length;
    if (n < k) return new int[]{-1, -1};

    int maxSum = 0;
    for (int i = 0; i < k; i++) maxSum += arr[i];

    int windowSum = maxSum;
    int start = 0;

    for (int i = k; i < n; i++) {
        windowSum += arr[i] - arr[i - k];
        if (windowSum > maxSum) {
            maxSum = windowSum;
            start = i - k + 1;
        }
    }

    return new int[]{start, start + k - 1};
}
```

## Maximum Average Subarray

Same thing but with averages instead of sums.

```java
public double findMaxAverage(int[] nums, int k) {
    int n = nums.length;
    if (n < k) return -1;

    int sum = 0;
    for (int i = 0; i < k; i++) {
        sum += nums[i];
    }

    int maxSum = sum;
    for (int i = k; i < n; i++) {
        sum += nums[i] - nums[i - k];
        maxSum = Math.max(maxSum, sum);
    }

    return (double) maxSum / k;
}
```

## With Negative Numbers

Works perfectly with negatives since `Math.max` handles it:

```java
public int maxSumSubarrayNegatives(int[] arr, int k) {
    int n = arr.length;
    if (n < k) return -1;

    int sum = 0;
    for (int i = 0; i < k; i++) sum += arr[i];

    int maxSum = sum;
    for (int i = k; i < n; i++) {
        sum += arr[i] - arr[i - k];
        maxSum = Math.max(maxSum, sum);
    }

    return maxSum;
}
```

```
arr = [-1, -2, -3, -4, -5], k = 2
First window: sum = -3, maxSum = -3
i=2: sum = -3 + (-3) - (-1) = -5, maxSum = -3
i=3: sum = -5 + (-4) - (-2) = -7, maxSum = -3
i=4: sum = -7 + (-5) - (-3) = -9, maxSum = -3

Result: -3
```

## Minimum Sum Subarray of Size K

```java
public int minSumSubarray(int[] arr, int k) {
    int n = arr.length;
    if (n < k) return -1;

    int sum = 0;
    for (int i = 0; i < k; i++) sum += arr[i];

    int minSum = sum;
    for (int i = k; i < n; i++) {
        sum += arr[i] - arr[i - k];
        minSum = Math.min(minSum, sum);
    }

    return minSum;
}
```

## Subarray Product Less Than K (Variable Size)

Not fixed size, but related — count contiguous subarrays where product < k.

```java
public int numSubarrayProductLessThanK(int[] nums, int k) {
    if (k <= 1) return 0;

    int left = 0;
    int product = 1;
    int count = 0;

    for (int right = 0; right < nums.length; right++) {
        product *= nums[right];

        while (product >= k) {
            product /= nums[left];
            left++;
        }

        // All subarrays ending at 'right' are valid
        count += right - left + 1;
    }

    return count;
}
```

The trick: `right - left + 1` counts all subarrays ending at `right` that have product < k. For example, if window is `[3, 2, 4]` and product < k, the subarrays are `[4]`, `[2, 4]`, `[3, 2, 4]`.

## Common Variations

```java
// Maximum sum of subarray with size at most K
public int maxSumAtMostK(int[] arr, int k) {
    int n = arr.length;
    int left = 0, sum = 0, maxSum = Integer.MIN_VALUE;

    for (int right = 0; right < n; right++) {
        sum += arr[right];

        while (right - left + 1 > k) {
            sum -= arr[left];
            left++;
        }

        maxSum = Math.max(maxSum, sum);
    }

    return maxSum;
}
```

## Practice Problems

Once you master this one, try:
- **Maximum of all subarrays of size K** (sliding window max)
- **First negative integer in every window of size K**
- **Count occurrences of anagram in a string**
- **Average of all contiguous subarrays of size K**

This is the foundation. The slide operation `sum += arr[i] - arr[i-k]` will be in every fixed-size window problem you encounter.
