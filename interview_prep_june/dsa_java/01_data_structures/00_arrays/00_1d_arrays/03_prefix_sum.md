# Prefix Sum Technique

## Core Concept

A prefix sum array stores cumulative sums from the start. This precomputation lets you answer **range sum queries** in O(1) time.

```plaintext
Original:  [3,  1,  4,  1,  5,  9,  2]
Prefix:    [3,  4,  8,  9, 14, 23, 25]
```

`prefix[i]` = sum of elements from index 0 to i (inclusive).

**Range sum from L to R:** `prefix[R] - prefix[L-1]` (handle L=0 as just `prefix[R]`).

### Why this matters

Without prefix sums, each query `sum(L, R)` takes O(R-L) time. With prefix sums, it's O(1) after O(n) precomputation. When you have many queries (say 10⁵), this is the difference between O(n*q) and O(n+q).

## 1D Prefix Sum Implementation

```java
public static int[] buildPrefixSum(int[] arr) {
    int[] prefix = new int[arr.length];
    prefix[0] = arr[0];
    for (int i = 1; i < arr.length; i++) {
        prefix[i] = prefix[i - 1] + arr[i];
    }
    return prefix;
}

public static int rangeSum(int[] prefix, int L, int R) {
    if (L == 0) return prefix[R];
    return prefix[R] - prefix[L - 1];
}
```

## Subarray Sum Equals K

**Problem:** Count the number of subarrays whose sum equals K.

```java
public static int subarraySumEqualsK(int[] arr, int k) {
    Map<Integer, Integer> prefixSumCount = new HashMap<>();
    prefixSumCount.put(0, 1); // empty prefix has sum 0

    int currentSum = 0;
    int count = 0;

    for (int num : arr) {
        currentSum += num;
        // If prefixSum - k exists, subarray from that index+1 to current has sum k
        count += prefixSumCount.getOrDefault(currentSum - k, 0);
        prefixSumCount.merge(currentSum, 1, Integer::sum);
    }
    return count;
}
```

### Intuition

We want subarrays where `sum(L, R) = k`. This means `prefix[R] - prefix[L-1] = k`, i.e., `prefix[L-1] = prefix[R] - k`. As we compute the running prefix sum, we check: "has any previous prefix equaled `current - k`?" If so, the subarray between that previous index and current index sums to k.

**Time:** O(n), **Space:** O(n) for the map.

## Equilibrium Index (Pivot Index)

**Problem:** Find an index where sum of left elements equals sum of right elements.

```java
public static int pivotIndex(int[] arr) {
    int totalSum = 0;
    for (int num : arr) totalSum += num;

    int leftSum = 0;
    for (int i = 0; i < arr.length; i++) {
        int rightSum = totalSum - leftSum - arr[i];
        if (leftSum == rightSum) return i;
        leftSum += arr[i];
    }
    return -1;
}
```

**Time:** O(n), **Space:** O(1).

## Range Sum Query (Immutable)

**Problem:** Given an array, answer multiple range sum queries.

```java
class NumArray {
    private int[] prefix;

    public NumArray(int[] nums) {
        prefix = new int[nums.length + 1]; // extra slot for sum(0,i)
        for (int i = 0; i < nums.length; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
    }

    public int sumRange(int left, int right) {
        return prefix[right + 1] - prefix[left];
    }
}
```

Using `prefix[i+1] = sum(0, i)` avoids the L=0 edge case. Cleaner.

## Product of Array Except Self

**Problem:** Return an array where `output[i]` equals product of all elements except `arr[i]`. **Cannot use division.**

```java
public static int[] productExceptSelf(int[] arr) {
    int n = arr.length;
    int[] result = new int[n];

    // Left pass: product of all elements to the left
    result[0] = 1;
    for (int i = 1; i < n; i++) {
        result[i] = result[i - 1] * arr[i - 1];
    }

    // Right pass: multiply by product of all elements to the right
    int rightProduct = 1;
    for (int i = n - 1; i >= 0; i--) {
        result[i] *= rightProduct;
        rightProduct *= arr[i];
    }

    return result;
}
```

### Why no division?

The problem explicitly forbids division to avoid the "divide by zero" issue. But even without that constraint, this O(n) time, O(1) extra space solution (output doesn't count as extra space) is elegant.

**How it works:**
- Left pass: `result[i]` = product of `arr[0]` through `arr[i-1]`
- Right pass: multiply each `result[i]` by product of `arr[i+1]` through `arr[n-1]`

## Subarray Sum Divisible by K

**Problem:** Count subarrays where sum is divisible by K.

```java
public static int subarraysDivByK(int[] arr, int k) {
    Map<Integer, Integer> remainderCount = new HashMap<>();
    remainderCount.put(0, 1); // empty prefix has remainder 0

    int currentSum = 0;
    int count = 0;

    for (int num : arr) {
        currentSum += num;
        int remainder = currentSum % k;

        // Java's % can be negative; normalize
        if (remainder < 0) remainder += k;

        count += remainderCount.getOrDefault(remainder, 0);
        remainderCount.merge(remainder, 1, Integer::sum);
    }
    return count;
}
```

### Key difference from "subarray sum equals k"

Here we check if `prefix[R] % k == prefix[L-1] % k`. If two prefixes have the same remainder, the subarray between them has sum divisible by k. Same pattern as subarray sum equals K, but with modulo arithmetic.

### Why normalize remainder?

Java's `%` operator returns a negative remainder when the dividend is negative. `(-3) % 5 = -3` in Java, but mathematically we want `2`. Adding `k` when negative normalizes it.

## Contiguous Array (Equal 0s and 1s)

**Problem:** Find the longest subarray with equal number of 0s and 1s.

```java
public static int findMaxLength(int[] arr) {
    // Treat 0 as -1, 1 as +1. Equal zeros and ones means sum = 0.
    Map<Integer, Integer> firstOccurrence = new HashMap<>();
    firstOccurrence.put(0, -1); // sum 0 at index -1

    int sum = 0;
    int maxLen = 0;

    for (int i = 0; i < arr.length; i++) {
        sum += (arr[i] == 0) ? -1 : 1;

        if (firstOccurrence.containsKey(sum)) {
            maxLen = Math.max(maxLen, i - firstOccurrence.get(sum));
        } else {
            firstOccurrence.put(sum, i); // store first occurrence
        }
    }
    return maxLen;
}
```

### Insight

Replace 0 → -1 and 1 → +1. A subarray with equal zeros and ones will have sum 0. Two prefix sums being equal means the subarray between them has sum 0. We store only the first occurrence of each prefix sum to maximize the length.

## When to Use Prefix Sum

1. **Range sum queries** — multiple queries over a static array
2. **Subarray sum equals a target** — with HashMap for O(n) solution
3. **Modulo-based conditions** — subarrays divisible by K
4. **Product except self** — prefix and suffix products
5. **Running computation** — equilibrium index, max length subarray

## Common Pitfalls

1. **1-indexing vs 0-indexing** — be consistent. Using `prefix[i+1]` avoids edge cases.
2. **Integer overflow** — prefix sums can exceed int range. Use `long` when sum can be large.
3. **HashMap for subarray problems** — don't forget the empty prefix `(0, -1)` or `(0, 1)` for counting.
4. **Negative numbers** — subarray sum equals K works fine with negatives. Kadane is for maximum, prefix sum for exact match.

## Practice Problems

| Problem | LeetCode | Approach |
|---------|----------|----------|
| Range Sum Query - Immutable | 303 | Prefix array |
| Subarray Sum Equals K | 560 | Prefix sum + HashMap |
| Product of Array Except Self | 238 | Left + right product |
| Contiguous Array | 525 | 0→-1, 1→+1, prefix + HashMap |
| Subarray Sums Divisible by K | 974 | Prefix remainder + HashMap |
| Find Pivot Index | 724 | Total sum - left sum |
