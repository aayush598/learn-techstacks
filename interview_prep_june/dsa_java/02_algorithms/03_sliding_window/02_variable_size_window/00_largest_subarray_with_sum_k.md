# Longest Subarray with Sum K

This is the first variable-size sliding window problem. The window grows when we need more elements, and shrinks when the sum exceeds the target.

## Problem Statement

Given an array of **positive integers**, find the length of the longest subarray whose sum equals `k`.

```
Input:  arr = [3, 1, 2, 7, 4, 2, 1, 1, 5], k = 7
Output: 4
Explanation: Subarray [4, 2, 1] or [2, 1, 1, 3]... wait.
Let me check: [3,1,2,1] sums to 7? 3+1+2+1=7, length=4. That's correct.

Actually let's trace:
[3, 1, 2, 1] = 7, length 4
[4, 2, 1] = 7, length 3
[2, 1, 1, 3] wait that's circular. Let's stick with [3,1,2,1]=7 length 4.
```

## The Solution (Positive Integers)

```java
public int longestSubarraySumK(int[] arr, int k) {
    int left = 0;
    int sum = 0;
    int maxLen = 0;

    for (int right = 0; right < arr.length; right++) {
        sum += arr[right]; // Expand window

        // Shrink if sum exceeds k
        while (sum > k) {
            sum -= arr[left];
            left++;
        }

        // Check if we found a valid sum
        if (sum == k) {
            maxLen = Math.max(maxLen, right - left + 1);
        }
    }

    return maxLen;
}
```

### Why This Works (for Positive Integers)

Because all numbers are positive, adding elements always increases the sum and removing elements always decreases it. The `while` loop correctly shrinks the window until `sum <= k`.

If the array had negative numbers, this wouldn't work — adding a negative element could decrease the sum, and we might miss valid windows.

### Dry Run

```
arr = [3, 1, 2, 7, 4, 2, 1, 1, 5], k = 7

left=0, sum=0, maxLen=0

right=0: sum=3,  sum<=k → sum!=k → maxLen=0
right=1: sum=4,  sum<=k → sum!=k → maxLen=0
right=2: sum=6,  sum<=k → sum!=k → maxLen=0
right=3: sum=13, sum>k  → shrink: left=1, sum=10 → still >k → left=2, sum=9 → still >k → left=3, sum=7
         sum==k → maxLen = max(0, 3-3+1) = 1
right=4: sum=11, sum>k  → shrink: left=4, sum=4
         sum!=k → maxLen=1
right=5: sum=6,  sum<=k → sum!=k → maxLen=1
right=6: sum=7,  sum==k → maxLen = max(1, 6-4+1) = 3
right=7: sum=8,  sum>k  → shrink: left=5, sum=7
         sum==k → maxLen = max(3, 7-5+1) = 3
right=8: sum=12, sum>k  → shrink: left=6, sum=5 → left=7, sum=4 → left=8, sum=0 → sum<k, stop
         sum!=k → maxLen=3

Result: 3
```

Wait, but [4, 2, 1] has length 3 — that checks out. Hmm, earlier I said [3,1,2,1]=7 length 4, but looking at the array [3, 1, 2, 7, 4, 2, 1, 1, 5], indices 0-3 are [3,1,2,7]=13, and [3,1,2,1] is not contiguous in this array. Let me re-check... yes, the array is `[3, 1, 2, 7, 4, 2, 1, 1, 5]`. Subarray [3,1,2,1] isn't contiguous here. So length 3 is correct.

## With HashMap (for Negative Numbers)

When the array has negative numbers, the two-pointer approach fails. We need prefix sums and a HashMap.

```java
public int longestSubarraySumKWithNegatives(int[] arr, int k) {
    Map<Long, Integer> prefixSum = new HashMap<>();
    long sum = 0;
    int maxLen = 0;

    prefixSum.put(0L, -1); // Important: sum 0 at index -1

    for (int i = 0; i < arr.length; i++) {
        sum += arr[i];

        // If (sum - k) exists, we found a subarray summing to k
        if (prefixSum.containsKey(sum - k)) {
            int len = i - prefixSum.get(sum - k);
            maxLen = Math.max(maxLen, len);
        }

        // Store first occurrence only (for longest subarray)
        if (!prefixSum.containsKey(sum)) {
            prefixSum.put(sum, i);
        }
    }

    return maxLen;
}
```

### Why Store First Occurrence Only?

For the *longest* subarray, we want the earliest index with a given prefix sum. If we overwrite with later indices, we'd get shorter subarrays.

```
arr = [1, -1, 5, -2, 3], k = 3

Prefix sums:
i=0: sum=1,  store {0:-1, 1:0}
i=1: sum=0,  sum-k=-3 not in map, store {0:1, 1:0} → update 0's index to 1? NO! We store first occurrence, so 0 stays at -1.
     Wait, prefixSum already has 0 at -1. So we skip storing 0→1.
i=2: sum=5,  sum-k=2 not in map, store 5→2
i=3: sum=3,  sum-k=0 in map at -1 → len = 3-(-1) = 4 → maxLen=4 (subarray [0..3])
     Store 3→3
i=4: sum=6,  sum-k=3 in map at 3 → len = 4-3 = 1 → maxLen stays 4

Result: 4
```

Subarray [0..3] = [1, -1, 5, -2] = 3, length 4.

## Count Subarrays with Sum K

This is a common variation — count how many subarrays sum to k.

```java
public int countSubarraysSumK(int[] arr, int k) {
    Map<Integer, Integer> prefixSum = new HashMap<>();
    int sum = 0;
    int count = 0;

    prefixSum.put(0, 1);

    for (int num : arr) {
        sum += num;

        if (prefixSum.containsKey(sum - k)) {
            count += prefixSum.get(sum - k);
        }

        prefixSum.put(sum, prefixSum.getOrDefault(sum, 0) + 1);
    }

    return count;
}
```

## Minimum Length Subarray with Sum K

Instead of longest, find the shortest.

```java
public int minSubarraySumK(int[] arr, int k) {
    int left = 0;
    int sum = 0;
    int minLen = Integer.MAX_VALUE;

    for (int right = 0; right < arr.length; right++) {
        sum += arr[right];

        while (sum >= k) {
            minLen = Math.min(minLen, right - left + 1);
            sum -= arr[left];
            left++;
        }
    }

    return minLen == Integer.MAX_VALUE ? 0 : minLen;
}
```

Note: this finds subarrays with sum `>= k` (minimum length). For `== k`, just modify the condition.

## Complexity

| Approach | Case | Time | Space |
|----------|------|------|-------|
| Two pointers | Positive numbers | O(n) | O(1) |
| HashMap | General (negatives) | O(n) | O(n) |

## Interview Tips

1. **Ask about negative numbers** — if they say no negatives, use the two-pointer approach (O(1) space)
2. **Ask for longest vs count vs shortest** — subtle differences in implementation
3. **For HashMap approach**, explain prefix sums — "the sum of subarray (i, j] = prefixSum[j] - prefixSum[i]"
4. **Edge cases**: empty array → 0, no valid subarray → 0, k=0 → what should happen?

## More Variations

### Longest Subarray with Sum Divisible by K

```java
public int longestSubarraySumDivisibleByK(int[] arr, int k) {
    Map<Integer, Integer> prefixMod = new HashMap<>();
    prefixMod.put(0, -1);
    int sum = 0;
    int maxLen = 0;

    for (int i = 0; i < arr.length; i++) {
        sum += arr[i];
        int mod = ((sum % k) + k) % k; // Handle negative mod

        if (prefixMod.containsKey(mod)) {
            maxLen = Math.max(maxLen, i - prefixMod.get(mod));
        } else {
            prefixMod.put(mod, i);
        }
    }

    return maxLen;
}
```

### Longest Subarray with Equal 0s and 1s (Treat 0 as -1)

```java
public int longestSubarrayEqual01(int[] arr) {
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == 0) arr[i] = -1;
    }
    return longestSubarraySumKWithNegatives(arr, 0);
}
```

### Check if Subarray with Sum K Exists (early exit)

```java
public boolean hasSubarraySumK(int[] arr, int k) {
    Set<Long> prefixSums = new HashSet<>();
    long sum = 0;
    prefixSums.add(0L);

    for (int num : arr) {
        sum += num;
        if (prefixSums.contains(sum - k)) return true;
        prefixSums.add(sum);
    }

    return false;
}
```

### Longest Subarray with Sum K (All Positive — Alternate Version)

If all numbers are positive and you want the longest, you can also expand first, then contract:

```java
public int longestSubarraySumKPositive(int[] arr, int k) {
    int left = 0, right = 0;
    int sum = 0;
    int maxLen = 0;

    while (right < arr.length) {
        sum += arr[right];

        while (sum > k && left <= right) {
            sum -= arr[left];
            left++;
        }

        if (sum == k) {
            maxLen = Math.max(maxLen, right - left + 1);
        }

        right++;
    }

    return maxLen;
}
```

## When to Use Which

| Scenario | Approach | Time | Space |
|----------|----------|------|-------|
| All positive | Two pointers | O(n) | O(1) |
| Has negatives | HashMap | O(n) | O(n) |
| Need count of subarrays | HashMap | O(n) | O(n) |
| Need existence check | Set | O(n) | O(n) |

## Interview Tips

1. **Ask about negative numbers** — if they say no negatives, use the two-pointer approach (O(1) space)
2. **Ask for longest vs count vs shortest** — subtle differences in implementation
3. **For HashMap approach**, explain prefix sums — "the sum of subarray (i, j] = prefixSum[j] - prefixSum[i]"
4. **Edge cases**: empty array → 0, no valid subarray → 0, k=0 → what should happen?

The two-pointer approach for positive arrays is O(n) and O(1) space. The HashMap approach for general arrays is O(n) and O(n) space. Know both!
