# DAY-005 | PATTERN FOCUS: Prefix Sum | TARGET: 1H + 2M + 3E

> **Objective:** Prefix sums for range sum, subarrays sum to target, 2D prefix sums basics.

---

## 1) EASY-1 | Range Sum Query - Immutable | Leetcode 303

### Problem
Build prefix sums array for range sum queries.

### Java Solution
```java
class NumArray {
    private int[] prefix;
    public NumArray(int[] nums) {
        prefix = new int[nums.length + 1];
        for (int i = 0; i < nums.length; i++) {
            prefix[i+1] = prefix[i] + nums[i];
        }
    }
    public int sumRange(int left, int right) {
        return prefix[right+1] - prefix[left];
    }
}
```
**TC:** Build O(n), query O(1) | **SC:** O(n)

### Similar
1. Leetcode 304 - Range Sum Query 2D
2. Leetcode 307 - Range Sum Query Mutable
3. Leetcode 525/560

---

## 2) EASY-2 | Find Pivot Index | Leetcode 724

### Problem
Index where left sum == right sum.

### Approach
Total sum S, left sum 0, if left==S-left-nums[i] return i.

### Java Solution
```java
class Solution {
    public int pivotIndex(int[] nums) {
        int total = 0, leftSum = 0;
        for (int num : nums) total += num;
        for (int i = 0; i < nums.length; i++) {
            if (leftSum == total - leftSum - nums[i]) return i;
            leftSum += nums[i];
        }
        return -1;
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 1991 - Find the Middle Index in Array
2. Leetcode 1480 - Running Sum of 1D Array
3. Leetcode 560

---

## 3) EASY-3 | Running Sum of 1D Array | Leetcode 1480

### Problem
Return running sum array.

### Java Solution
```java
class Solution {
    public int[] runningSum(int[] nums) {
        for (int i = 1; i < nums.length; i++) {
            nums[i] += nums[i-1];
        }
        return nums;
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 724
2. Leetcode 303
3. Leetcode 560

---

## 4) MEDIUM-1 | Subarray Sum Equals K | Leetcode 560

### Problem
Count continuous subarrays with sum = k.

### Approach
Prefix sum map: count of prefix sum value.

### Java Solution
```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        map.put(0, 1);
        int sum = 0, count = 0;
        for (int num : nums) {
            sum += num;
            count += map.getOrDefault(sum - k, 0);
            map.put(sum, map.getOrDefault(sum, 0) + 1);
        }
        return count;
    }
}
```
**TC:** O(n) | **SC:** O(n)

### Similar
1. Leetcode 523 - Continuous Subarray Sum
2. Leetcode 974 - Subarray Sums Divisible by K
3. Leetcode 525 - Contiguous Array

---

## 5) MEDIUM-2 | Continuous Subarray Sum | Leetcode 523

### Problem
Check if there is subarray of length >=2 with sum divisible by k.

### Approach
Prefix sum mod k, store first index of mod.

### Java Solution
```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public boolean checkSubarraySum(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        map.put(0, -1);
        int sum = 0;
        for (int i = 0; i < nums.length; i++) {
            sum += nums[i];
            int mod = sum % k;
            if (map.containsKey(mod)) {
                if (i - map.get(mod) >= 2) return true;
            } else {
                map.put(mod, i);
            }
        }
        return false;
    }
}
```
**TC:** O(n) | **SC:** O(k)

### Similar
1. Leetcode 560
2. Leetcode 974
3. Leetcode 525

---

## 6) HARD-1 | Subarray Sums Divisible by K | Leetcode 974

### Problem
Count subarrays with (sum % k == 0).

### Approach
Prefix sum mod k, map mod -> count.

### Java Solution
```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int subarraysDivByK(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        map.put(0, 1);
        int sum = 0, ans = 0;
        for (int num : nums) {
            sum += num;
            int mod = ((sum % k) + k) % k;
            ans += map.getOrDefault(mod, 0);
            map.put(mod, map.getOrDefault(mod, 0) + 1);
        }
        return ans;
    }
}
```
**TC:** O(n) | **SC:** O(k)

### Similar
1. Leetcode 523
2. Leetcode 560
3. Leetcode 1590 - Make Sum Divisible by P

---

## END OF DAY REVIEW
- **Learned:** Prefix sums + map tricks
- **Mistakes:** [Fill]
- **Weak Points:** [Fill]
- **Revision Due:** D+1 | D+3 | D+7 | D+14 | D+30
