# Kadane's Algorithm — Maximum Subarray Sum

## The Problem

Given an array of integers (which can include negative numbers), find the **contiguous subarray** with the largest sum.

```
Input:  [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6   (subarray [4, -1, 2, 1])
```

## The Intuition

Kadane's insight is brilliantly simple: **carry forward a positive sum, restart when it goes negative.**

Imagine you're adding numbers. If the running sum dips below zero, keeping it would only drag down future sums. So you drop it and start fresh from the current element.

This is a **dynamic programming** pattern where:
- `maxEndingHere` = maximum sum of subarray ending at current position
- `maxSoFar` = overall maximum seen so far

### Why this works (proof sketch)

At any index i, the maximum subarray ending at i is either:
1. `arr[i]` alone (start new subarray)
2. `maxEndingHere + arr[i]` (extend previous subarray)

We take whichever is larger. "Ending at i" is the key — we force the subarray to include i, which means we can build the answer incrementally.

## Implementation

```java
public static int kadane(int[] arr) {
    int maxEndingHere = arr[0];
    int maxSoFar = arr[0];

    for (int i = 1; i < arr.length; i++) {
        // Either extend or restart
        maxEndingHere = Math.max(arr[i], maxEndingHere + arr[i]);
        maxSoFar = Math.max(maxSoFar, maxEndingHere);
    }
    return maxSoFar;
}
```

**Time:** O(n) — single pass.
**Space:** O(1) — just two ints.

### Returning the actual subarray

```java
public static int[] kadaneWithSubarray(int[] arr) {
    int maxEndingHere = arr[0], maxSoFar = arr[0];
    int start = 0, end = 0, tempStart = 0;

    for (int i = 1; i < arr.length; i++) {
        if (arr[i] > maxEndingHere + arr[i]) {
            maxEndingHere = arr[i];
            tempStart = i;
        } else {
            maxEndingHere = maxEndingHere + arr[i];
        }

        if (maxEndingHere > maxSoFar) {
            maxSoFar = maxEndingHere;
            start = tempStart;
            end = i;
        }
    }
    return Arrays.copyOfRange(arr, start, end + 1);
}
```

## All Negative Array Handling

If ALL elements are negative, Kadane's returns the **least negative** element (the largest value).

Consider `[-5, -2, -8, -1, -7]`:
- At i=0: maxEndingHere = -5, maxSoFar = -5
- At i=1: maxEndingHere = max(-2, -5 + -2) = -2, maxSoFar = -2
- At i=2: maxEndingHere = max(-8, -2 + -8) = -8, maxSoFar = -2
- At i=3: maxEndingHere = max(-1, -8 + -1) = -1, maxSoFar = -1
- Result: -1

This is correct behavior. Some implementations modify Kadane to return 0 for all-negative arrays (resetting count at 0), but that's a **different problem** — it conflates "empty subarray allowed" with the standard problem.

## Maximum Circular Subarray Sum

**Problem:** The subarray can wrap around from end to start.

```
Input:  [5, -3, 5]
Output: 7   (5 + 5 wraps around: index 2 and 0)
```

### Key insight

A circular maximum subarray is either:
1. The regular Kadane maximum (non-wrapping)
2. **Total sum - minimum subarray sum** (wrapping — we remove the minimum interior segment)

```java
public static int maxCircularSubarray(int[] arr) {
    // Case 1: standard Kadane
    int maxKadane = kadane(arr);

    // Case 2: circular — total sum - minimum subarray
    int totalSum = 0;
    int minEndingHere = arr[0];
    int minSoFar = arr[0];

    for (int i = 0; i < arr.length; i++) {
        totalSum += arr[i];
    }

    for (int i = 1; i < arr.length; i++) {
        minEndingHere = Math.min(arr[i], minEndingHere + arr[i]);
        minSoFar = Math.min(minSoFar, minEndingHere);
    }

    int circularMax = totalSum - minSoFar;

    // Edge case: if all numbers are negative, circularMax = 0 which is wrong
    if (circularMax == 0) return maxKadane;

    return Math.max(maxKadane, circularMax);
}
```

**Edge case:** If all numbers are negative, `totalSum - minSoFar` equals 0, but the answer should be the max (least negative). We handle this by returning maxKadane when circularMax is 0.

## Minimum Subarray Sum

Same as Kadane but with `Math.min` instead of `Math.max`:

```java
public static int minSubarraySum(int[] arr) {
    int minEndingHere = arr[0];
    int minSoFar = arr[0];
    for (int i = 1; i < arr.length; i++) {
        minEndingHere = Math.min(arr[i], minEndingHere + arr[i]);
        minSoFar = Math.min(minSoFar, minEndingHere);
    }
    return minSoFar;
}
```

## Maximum Product Subarray

This is the **tricky** one. Unlike sum, product has sign flips. A negative number can turn a minimum product into a maximum product.

```
Input:  [2, 3, -2, 4]
Output: 6   (subarray [2, 3])

Input:  [-2, 3, -4]
Output: 24  (subarray [-2, 3, -4] — two negatives make positive!)
```

### The insight

We need to track BOTH max and min ending at each position because:
- `max(arr[i], maxEndingHere * arr[i])` — standard Kadane idea
- But if `arr[i]` is negative, `minEndingHere * arr[i]` could become the new max!

```java
public static int maxProductSubarray(int[] arr) {
    int maxEndingHere = arr[0];
    int minEndingHere = arr[0];
    int maxSoFar = arr[0];

    for (int i = 1; i < arr.length; i++) {
        int temp = maxEndingHere;

        // At negative, max becomes min and min becomes max
        maxEndingHere = Math.max(arr[i], Math.max(maxEndingHere * arr[i], minEndingHere * arr[i]));
        minEndingHere = Math.min(arr[i], Math.min(temp * arr[i], minEndingHere * arr[i]));

        maxSoFar = Math.max(maxSoFar, maxEndingHere);
    }
    return maxSoFar;
}
```

**Why `temp`?** We need the old `maxEndingHere` to compute the new `minEndingHere`, but we already updated `maxEndingHere`. Storing the old value avoids this issue.

### Two-pass alternative (simpler, O(n))

```java
public static int maxProductSubarrayTwoPass(int[] arr) {
    int n = arr.length;
    int max = Integer.MIN_VALUE;
    int product = 1;

    // Left to right
    for (int i = 0; i < n; i++) {
        product *= arr[i];
        max = Math.max(max, product);
        if (product == 0) product = 1;
    }

    // Right to left (catches cases where odd negatives split the max)
    product = 1;
    for (int i = n - 1; i >= 0; i--) {
        product *= arr[i];
        max = Math.max(max, product);
        if (product == 0) product = 1;
    }

    return max;
}
```

**Why two passes?** Consider `[3, -1, 4]`. Left pass: 3, -3, -12 → max=3. Right pass: 4, -4, -12 → max=4. But the actual max is `[4]` = 4. Yet if we have `[-1, -2, -3]`, left pass: -1, 2, -6 → max=2. Right pass: -3, 6, -6 → max=6 (correct). The two-pass handles cases where the maximum subarray doesn't start at either end.

## Practice Problems

| Problem | Approach |
|---------|----------|
| Maximum Subarray (LeetCode 53) | Standard Kadane |
| Maximum Sum Circular Subarray (LeetCode 918) | Kadane + min subarray |
| Maximum Product Subarray (LeetCode 152) | Track both min and max |
| Maximum Subarray Sum with One Deletion | Kadane with "skip" DP state |
| Best Time to Buy/Sell Stock (LeetCode 121) | Kadane on price differences |
| Maximum Absolute Sum of Any Subarray (LeetCode 1749) | max of Kadane and min absolute |

## Interview Tips

- **Always ask:** "Can the array be empty? All negative? What should I return for empty?"
- **State the recurrence:** `dp[i] = max(arr[i], dp[i-1] + arr[i])` — showing you understand DP behind it
- **Mention follow-ups:** "For circular, we can use total - min subarray"
- **Differentiate from divide-and-conquer:** "Kadane is O(n), the divide-and-conquer approach for max subarray is O(n log n)"
- **The product variant** is the real differentiator. If you can explain why tracking both min and max is necessary, you demonstrate depth.
