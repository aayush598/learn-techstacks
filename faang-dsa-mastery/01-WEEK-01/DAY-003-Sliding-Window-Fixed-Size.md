# DAY-003 | PATTERN FOCUS: Sliding Window - Fixed Size | TARGET: 1H + 2M + 3E

> **Objective:** Master fixed-window expansion/shrinkage, running sum/max/avg patterns.

**Status:** NOT STARTED

---

## 1) EASY-1 | Maximum Average Subarray I | Leetcode 643

### Problem
Find max average of subarray of length k.

### Approach
Compute sum of first window, track max, slide by removing left adding right.

### Java Solution
```java
class Solution {
    public double findMaxAverage(int[] nums, int k) {
        double sum = 0;
        for (int i = 0; i < k; i++) sum += nums[i];
        double maxSum = sum;
        for (int i = k; i < nums.length; i++) {
            sum = sum - nums[i-k] + nums[i];
            maxSum = Math.max(maxSum, sum);
        }
        return maxSum / k;
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 1343 - Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold
2. Leetcode 1424 - Diagonal Traverse II (contextual)
3. Leetcode 2090 - K Radius Subarray Averages

---

## 2) EASY-2 | Contains Duplicate II | Leetcode 219

### Problem
Check if nums[i]==nums[j] with |i-j| <= k.

### Approach
HashSet window of size k or HashMap value->index.

### Java Solution
```java
import java.util.HashSet;
import java.util.Set;

class Solution {
    public boolean containsNearbyDuplicate(int[] nums, int k) {
        Set<Integer> set = new HashSet<>();
        for (int i = 0; i < nums.length; i++) {
            if (set.contains(nums[i])) return true;
            set.add(nums[i]);
            if (set.size() > k) set.remove(nums[i-k]);
        }
        return false;
    }
}
```
**TC:** O(n) | **SC:** O(k)

### Similar
1. Leetcode 217 - Contains Duplicate
2. Leetcode 220 - Contains Duplicate III
3. Leetcode 1 context

---

## 3) EASY-3 | Number of Subarrays with Bounded Maximum | Leetcode 795 (Intro level variant) OR Leetcode 1499? Better Leetcode 1343 style

But better solid: **Leetcode 1984 - Minimum Difference Between Highest and Lowest of K Scores**

### Problem
Sort array, find min(nums[i+k-1]-nums[i]) over all windows of k.

### Approach
Sort ascending, slide window of k.

### Java Solution
```java
import java.util.Arrays;

class Solution {
    public int minimumDifference(int[] nums, int k) {
        Arrays.sort(nums);
        int minDiff = Integer.MAX_VALUE;
        for (int i = 0; i <= nums.length - k; i++) {
            minDiff = Math.min(minDiff, nums[i+k-1] - nums[i]);
        }
        return minDiff;
    }
}
```
**TC:** O(n log n) | **SC:** O(1)

### Similar
1. Leetcode 643
2. Leetcode 1052 - Grumpy Bookstore Owner
3. Leetcode 1208 - Get Equal Substrings Within Budget

---

## 4) MEDIUM-1 | Grumpy Bookstore Owner | Leetcode 1052

### Problem
Max satisfied customers using at most X minutes of grumpy technique.

### Approach
Fixed window of X: gain = sum of grumpy customers in window, slide to maximize gain, answer = satisfied + maxGain.

### Java Solution
```java
class Solution {
    public int maxSatisfied(int[] customers, int[] grumpy, int minutes) {
        int n = customers.length;
        int satisfied = 0;
        for (int i = 0; i < n; i++) {
            if (grumpy[i] == 0) satisfied += customers[i];
        }
        int gain = 0;
        for (int i = 0; i < minutes; i++) {
            if (grumpy[i] == 1) gain += customers[i];
        }
        int maxGain = gain;
        for (int i = minutes; i < n; i++) {
            if (grumpy[i] == 1) gain += customers[i];
            if (grumpy[i - minutes] == 1) gain -= customers[i - minutes];
            maxGain = Math.max(maxGain, gain);
        }
        return satisfied + maxGain;
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 643
2. Leetcode 1423 - Maximum Points You Can Obtain from Cards
3. Leetcode 1424 context

---

## 5) MEDIUM-2 | Maximum Number of Vowels in a Substring of Given Length | Leetcode 1456

### Problem
Max count of vowels in any substring of length k.

### Approach
Count vowels in first window, slide window updating count.

### Java Solution
```java
class Solution {
    private boolean isVowel(char c) {
        return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' ||
               c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U';
    }
    public int maxVowels(String s, int k) {
        int count = 0;
        for (int i = 0; i < k; i++) if (isVowel(s.charAt(i))) count++;
        int maxCount = count;
        for (int i = k; i < s.length(); i++) {
            if (isVowel(s.charAt(i-k))) count--;
            if (isVowel(s.charAt(i))) count++;
            maxCount = Math.max(maxCount, count);
        }
        return maxCount;
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 643
2. Leetcode 1876 - Substrings of Size Three with Distinct Characters
3. Leetcode 438

---

## 6) HARD-1 | Sliding Window Maximum | Leetcode 239

### Problem
Return array of max in every window of size k.

### Approach
Use Deque to maintain indices of useful elements in every window.

### Java Solution
```java
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;

class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        if (nums.length == 0) return new int[0];
        int[] res = new int[nums.length - k + 1];
        Deque<Integer> deque = new ArrayDeque<>();
        for (int i = 0; i < nums.length; i++) {
            while (!deque.isEmpty() && deque.peekFirst() <= i - k) deque.pollFirst();
            while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[i]) deque.pollLast();
            deque.offerLast(i);
            if (i >= k - 1) res[i - k + 1] = nums[deque.peekFirst()];
        }
        return res;
    }
}
```
**TC:** O(n) | **SC:** O(k)

### Similar
1. Leetcode 239 is standard
2. Leetcode 480 - Sliding Window Median
3. Leetcode 1438 - Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit

---

## END OF DAY REVIEW
- **Learned:** Fixed window, monotonic deque intuition
- **Mistakes:** [Fill]
- **Weak Points:** [Fill]
- **Revision Due:** D+1 | D+3 | D+7 | D+14 | D+30
