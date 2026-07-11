# Subarray Problems with Hashing

## Key Insight

Many subarray problems reduce to **prefix sum + HashMap**. The subarray sum from index `l` to `r` is `prefix[r] - prefix[l-1]`.

## Problem 1: Subarray Sum Equals K

Count number of subarrays with sum = k:
```java
int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> prefixSum = new HashMap<>();  // sum -> count
    prefixSum.put(0, 1);  // empty prefix
    int sum = 0, count = 0;
    
    for (int num : nums) {
        sum += num;
        // If prefix[r] - prefix[l-1] = k, then prefix[l-1] = prefix[r] - k
        count += prefixSum.getOrDefault(sum - k, 0);
        prefixSum.merge(sum, 1, Integer::sum);
    }
    return count;
}
```
O(n) time, O(n) space.

## Problem 2: Subarray Sum Divisible by K

```java
int subarraysDivByK(int[] nums, int k) {
    Map<Integer, Integer> modCount = new HashMap<>();
    modCount.put(0, 1);
    int sum = 0, count = 0;
    
    for (int num : nums) {
        sum += num;
        int mod = ((sum % k) + k) % k;  // handle negative
        count += modCount.getOrDefault(mod, 0);
        modCount.merge(mod, 1, Integer::sum);
    }
    return count;
}
```

## Problem 3: Continuous Subarray Sum (Multiple of K)

Check if subarray sum is multiple of k (size >= 2):
```java
boolean checkSubarraySum(int[] nums, int k) {
    Map<Integer, Integer> modIndex = new HashMap<>();  // mod -> first index
    modIndex.put(0, -1);
    int sum = 0;
    
    for (int i = 0; i < nums.length; i++) {
        sum += nums[i];
        int mod = k == 0 ? sum : ((sum % k) + k) % k;
        
        if (modIndex.containsKey(mod)) {
            if (i - modIndex.get(mod) >= 2) return true;
        } else {
            modIndex.put(mod, i);
        }
    }
    return false;
}
```

## Problem 4: Longest Subarray with Sum K

```java
int longestSubarraySumK(int[] nums, int k) {
    Map<Integer, Integer> firstIndex = new HashMap<>();  // sum -> first index
    firstIndex.put(0, -1);
    int sum = 0, maxLen = 0;
    
    for (int i = 0; i < nums.length; i++) {
        sum += nums[i];
        if (firstIndex.containsKey(sum - k)) {
            maxLen = Math.max(maxLen, i - firstIndex.get(sum - k));
        }
        firstIndex.putIfAbsent(sum, i);
    }
    return maxLen;
}
```

## Problem 5: Contiguous Array (Equal 0s and 1s)

```java
int findMaxLength(int[] nums) {
    Map<Integer, Integer> firstIndex = new HashMap<>();
    firstIndex.put(0, -1);
    int count = 0, maxLen = 0;
    
    for (int i = 0; i < nums.length; i++) {
        count += nums[i] == 0 ? -1 : 1;
        if (firstIndex.containsKey(count)) {
            maxLen = Math.max(maxLen, i - firstIndex.get(count));
        } else {
            firstIndex.put(count, i);
        }
    }
    return maxLen;
}
```

## The Pattern

All these follow the same structure:
1. Maintain running `sum` (or count or mod)
2. Store first occurrence or frequency in HashMap
3. For each element, check if `(sum - target)` or `sum % k` exists in map
4. Compute result

| Problem | Map Key | Map Value | Condition |
|---------|---------|-----------|-----------|
| Subarray Sum = K | prefix sum | frequency | sum - k in map |
| Subarray sum % K = 0 | prefix % k | frequency | mod in map |
| Longest subarray sum = K | prefix sum | first index | sum - k in map |
| Equal 0/1 | count (+1/-1) | first index | count in map |
| Longest sum >= K | prefix sum | first index | binary search on keys |
