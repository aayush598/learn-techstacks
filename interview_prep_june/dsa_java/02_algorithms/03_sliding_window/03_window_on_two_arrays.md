# Window on Two Arrays / Advanced Counting

Some problems combine sliding window with clever counting techniques. The key pattern: **count of subarrays satisfying condition = atMost(K) - atMost(K-1)**.

## Count Number of Nice Subarrays

### Problem Statement
Given an array of integers and an integer `k`, count the number of contiguous subarrays that contain **exactly k odd numbers**.

```
Input:  nums = [1, 1, 2, 1, 1], k = 3
Output: 2
Explanation: 
  [1, 1, 2, 1] has 3 odd numbers
  [1, 2, 1, 1] has 3 odd numbers

Input:  nums = [2, 4, 6], k = 1
Output: 0
```

### The At-Most Trick

Count subarrays with `≤ k` odd numbers, then subtract those with `≤ k-1` odd numbers.

```java
public int numberOfSubarrays(int[] nums, int k) {
    return atMostKOdd(nums, k) - atMostKOdd(nums, k - 1);
}

private int atMostKOdd(int[] nums, int k) {
    if (k < 0) return 0;

    int left = 0;
    int count = 0;
    int oddCount = 0;

    for (int right = 0; right < nums.length; right++) {
        if (nums[right] % 2 == 1) {
            oddCount++;
        }

        while (oddCount > k) {
            if (nums[left] % 2 == 1) {
                oddCount--;
            }
            left++;
        }

        // All subarrays ending at 'right' are valid
        count += right - left + 1;
    }

    return count;
}
```

### Dry Run

```
nums = [1, 1, 2, 1, 1], k = 3

atMostKOdd(nums, 3):
left=0, oddCount=0, count=0

right=0, nums[0]=1: oddCount=1, ≤3, count+=1=1
right=1, nums[1]=1: oddCount=2, ≤3, count+=2=3
right=2, nums[2]=2: oddCount=2, ≤3, count+=3=6
right=3, nums[3]=1: oddCount=3, ≤3, count+=4=10
right=4, nums[4]=1: oddCount=4, >3
  → shrink: left=0, nums[0]=1 → oddCount=3, left=1
  → oddCount=3≤3, stop
  count+=4=14

atMostKOdd(nums, 3) = 14

atMostKOdd(nums, 2):
right=0: oddCount=1, count+=1=1
right=1: oddCount=2, count+=2=3
right=2: oddCount=2, count+=3=6
right=3: oddCount=3, >2
  → shrink: left=0, oddCount=2, left=1
  count+=3=9
right=4: oddCount=3, >2
  → shrink: left=1, oddCount=2, left=2
  count+=3=12

atMostKOdd(nums, 2) = 12

Result: 14 - 12 = 2 ✓
```

### Alternative: Prefix Sum of Odd Counts

```java
public int numberOfSubarraysPrefix(int[] nums, int k) {
    Map<Integer, Integer> prefixCount = new HashMap<>();
    prefixCount.put(0, 1);

    int oddCount = 0;
    int result = 0;

    for (int num : nums) {
        if (num % 2 == 1) oddCount++;

        if (prefixCount.containsKey(oddCount - k)) {
            result += prefixCount.get(oddCount - k);
        }

        prefixCount.put(oddCount, prefixCount.getOrDefault(oddCount, 0) + 1);
    }

    return result;
}
```

This treats odd numbers as 1 and even as 0, then counts subarrays with sum = k.

## Number of Subarrays with Bounded Maximum

### Problem Statement
Count subarrays where the maximum element is in `[left, right]`.

```
Input:  nums = [2, 1, 4, 3], left = 2, right = 3
Output: 3
Explanation: [2], [2,1], [3] have max in [2,3]
```

### Approach

Count subarrays with max ≤ right, subtract those with max ≤ left-1.

```java
public int numSubarrayBoundedMax(int[] nums, int left, int right) {
    return countSubarraysMaxAtMost(nums, right) - countSubarraysMaxAtMost(nums, left - 1);
}

private int countSubarraysMaxAtMost(int[] nums, int limit) {
    int count = 0;
    int windowStart = 0;

    for (int i = 0; i < nums.length; i++) {
        if (nums[i] > limit) {
            // Reset — can't include this element
            windowStart = i + 1;
        } else {
            // All subarrays ending at i are valid
            count += i - windowStart + 1;
        }
    }

    return count;
}
```

### How It Works

When `nums[i] > limit`, reset `windowStart`. Otherwise, all subarrays ending at `i` and starting at or after `windowStart` are valid.

The `count += i - windowStart + 1` counts subarrays ending at `i`:
- Starting at `windowStart`: `[windowStart, i]`
- Starting at `windowStart+1`: `[windowStart+1, i]`
- ...
- Starting at `i`: `[i, i]`

Total: `i - windowStart + 1` subarrays.

### Dry Run

```
nums = [2, 1, 4, 3], left=2, right=3

countSubarraysMaxAtMost(nums, 3):
windowStart=0, count=0
i=0, nums[0]=2 ≤ 3: count += 0-0+1 = 1  (subarrays: [2])
i=1, nums[1]=1 ≤ 3: count += 1-0+1 = 3  (subarrays: [2,1], [1])
i=2, nums[2]=4 > 3: windowStart=3, count stays 3
i=3, nums[3]=3 ≤ 3: count += 3-3+1 = 4  (subarrays: [3])
count = 4

countSubarraysMaxAtMost(nums, 1):
windowStart=0, count=0
i=0, nums[0]=2 > 1: windowStart=1
i=1, nums[1]=1 ≤ 1: count += 1-1+1 = 1 (subarrays: [1])
i=2, nums[2]=4 > 1: windowStart=3
i=3, nums[3]=3 > 1: windowStart=4
count = 1

Result: 4 - 1 = 3 ✓ (subarrays: [2], [2,1], [3])
```

## Count Subarrays with Exactly K Distinct Integers

We already saw this in the "K Unique Characters" section, but let's apply it to arrays:

```java
public int subarraysWithKDistinct(int[] nums, int k) {
    return atMostKDistinct(nums, k) - atMostKDistinct(nums, k - 1);
}

private int atMostKDistinct(int[] nums, int k) {
    if (k < 0) return 0;

    Map<Integer, Integer> freq = new HashMap<>();
    int left = 0;
    int count = 0;

    for (int right = 0; right < nums.length; right++) {
        freq.put(nums[right], freq.getOrDefault(nums[right], 0) + 1);

        while (freq.size() > k) {
            int leftVal = nums[left];
            freq.put(leftVal, freq.get(leftVal) - 1);
            if (freq.get(leftVal) == 0) freq.remove(leftVal);
            left++;
        }

        count += right - left + 1;
    }

    return count;
}
```

## Fruits into Baskets

### Problem Statement
You have two baskets, and each basket can hold only one type of fruit. Maximize the number of fruits you can collect.

This is just "longest subarray with at most 2 distinct values":

```java
public int totalFruit(int[] fruits) {
    Map<Integer, Integer> freq = new HashMap<>();
    int left = 0;
    int maxLen = 0;

    for (int right = 0; right < fruits.length; right++) {
        freq.put(fruits[right], freq.getOrDefault(fruits[right], 0) + 1);

        while (freq.size() > 2) {
            int leftFruit = fruits[left];
            freq.put(leftFruit, freq.get(leftFruit) - 1);
            if (freq.get(leftFruit) == 0) freq.remove(leftFruit);
            left++;
        }

        maxLen = Math.max(maxLen, right - left + 1);
    }

    return maxLen;
}
```

## The At-Most Pattern Summary

This is one of the most useful patterns in competitive programming:

```
count(exactly K) = count(atMost K) - count(atMost K-1)
```

It works when:
- The condition is **monotonic** — if `[L, R]` satisfies the condition, then all windows within `[L, R]` also satisfy it
- You can compute `atMost` efficiently with a sliding window

### Problems That Use This Pattern

| Problem | Condition | Variation |
|---------|-----------|-----------|
| Nice Subarrays | Exactly K odd | Subtract atMost |
| K Distinct Integers | Exactly K distinct | Subtract atMost |
| Subarrays with Bounded Max | Max in [L, R] | Subtract atMost |
| Exactly K unique chars | Exactly K distinct | Subtract atMost |

## Beyond "atMost": Direct Sliding Window

Some problems need a direct approach instead of the subtraction trick.

### Count Subarrays with Sum < K

```java
public int countSubarraysSumLessThanK(int[] nums, int k) {
    int left = 0;
    int sum = 0;
    int count = 0;

    for (int right = 0; right < nums.length; right++) {
        sum += nums[right];

        while (sum >= k) {
            sum -= nums[left];
            left++;
        }

        // All subarrays ending at right are valid
        count += right - left + 1;
    }

    return count;
}
```

### Count Subarrays with Product < K

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

        count += right - left + 1;
    }

    return count;
}
```

## Bonus: Count Substrings with Exactly One Character Different

Given two strings, count substrings that differ by exactly one character.

```java
public int countSubstringsWithOneDifference(String s, String t) {
    int n = s.length();
    int m = t.length();
    int count = 0;

    // For each possible center of difference
    for (int i = 0; i < n; i++) {
        count += expandFromCenter(s, t, i, i);
        count += expandFromCenter(s, t, i, i + 1);
    }

    return count;
}

private int expandFromCenter(String s, String t, int i, int j) {
    int count = 0;
    int diff = 0;

    while (i >= 0 && j < Math.min(s.length(), t.length())) {
        if (s.charAt(i) != t.charAt(j)) diff++;

        if (diff == 1) count++;
        else if (diff > 1) break;

        i--;
        j++;
    }

    return count;
}
```

This is more of a center-expansion (like palindrome) than sliding window, but it's a related pattern.

## Complexity Summary

All these solutions follow the same pattern:
- **Time**: O(n) — each element added/removed at most once
- **Space**: O(k) where k is the number of distinct values (or O(1) for fixed character sets)

## Interview Tips

1. **The atMost trick is your best friend** — "since count(exactly K) = count(atMost K) - count(atMost K-1)"
2. **Explain monotonicity** — "if a subarray has ≤ K distinct, any subarray within it also has ≤ K distinct"
3. **Know the `right - left + 1` trick** — it counts all subarrays ending at `right`
4. **Edge cases**: k=0, k=1, empty array, k larger than array length

The sliding window + atMost pattern is one of the most versatile in all of algorithm interviews. Master it, and you'll easily handle any subarray counting problem.
