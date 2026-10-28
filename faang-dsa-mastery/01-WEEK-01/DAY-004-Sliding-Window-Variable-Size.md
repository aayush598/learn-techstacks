# DAY-004 | PATTERN FOCUS: Sliding Window - Variable Size | TARGET: 1H + 2M + 3E

> **Objective:** Expand right, shrink left while condition holds. Master "smallest/largest window" with condition.

---

## 1) EASY-1 | Max Consecutive Ones | Leetcode 485

### Problem
Max number of consecutive 1's.

### Approach
Count, track max.

### Java Solution
```java
class Solution {
    public int findMaxConsecutiveOnes(int[] nums) {
        int count = 0, maxCount = 0;
        for (int num : nums) {
            if (num == 1) count++;
            else {
                maxCount = Math.max(maxCount, count);
                count = 0;
            }
        }
        return Math.max(maxCount, count);
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 487 - Max Consecutive Ones II
2. Leetcode 1004 - Max Consecutive Ones III
3. Leetcode 485

---

## 2) EASY-2 | Longest Substring with Distinct Characters (basic) - Leetcode 159 context OR Leetcode 3 done? Do Leetcode 904? Or **Fruit Into Baskets** variant logic

Better: **Leetcode 1428? Or Leetcode 340** scaled. Do **Leetcode 3** is done. Use **Leetcode 159 - Longest Substring with At Most Two Distinct Characters**

### Problem
Longest substring with at most 2 distinct characters.

### Approach
Variable window + HashMap count of distinct.

### Java Solution
```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int lengthOfLongestSubstringTwoDistinct(String s) {
        Map<Character, Integer> map = new HashMap<>();
        int left = 0, maxLen = 0;
        for (int right = 0; right < s.length(); right++) {
            map.put(s.charAt(right), map.getOrDefault(s.charAt(right), 0) + 1);
            while (map.size() > 2) {
                map.put(s.charAt(left), map.get(s.charAt(left)) - 1);
                if (map.get(s.charAt(left)) == 0) map.remove(s.charAt(left));
                left++;
            }
            maxLen = Math.max(maxLen, right - left + 1);
        }
        return maxLen;
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 3
2. Leetcode 340 - At Most K Distinct
3. Leetcode 76

---

## 3) EASY-3 | Subarray Product Less Than K | Leetcode 713

### Problem
Count contiguous subarrays where product < k.

### Approach
Expand right, while product>=k divide by nums[left] and left++, add (right-left+1).

### Java Solution
```java
class Solution {
    public int numSubarrayProductLessThanK(int[] nums, int k) {
        if (k <= 1) return 0;
        int left = 0, product = 1, count = 0;
        for (int right = 0; right < nums.length; right++) {
            product *= nums[right];
            while (product >= k && left <= right) {
                product /= nums[left++];
            }
            count += (right - left + 1);
        }
        return count;
    }
}
```
**TC:** O(n) (left/right move once) | **SC:** O(1)

### Similar
1. Leetcode 209 - Minimum Size Subarray Sum
2. Leetcode 713
3. Leetcode 152 - Maximum Product Subarray

---

## 4) MEDIUM-1 | Longest Repeating Character Replacement | Leetcode 424

### Problem
Find length of longest substring containing same letter after replacing at most k characters.

### Approach
Window, count max frequency in window, window size - maxCount <= k valid.

### Java Solution
```java
class Solution {
    public int characterReplacement(String s, int k) {
        int[] count = new int[26];
        int left = 0, maxCount = 0, maxLen = 0;
        for (int right = 0; right < s.length(); right++) {
            maxCount = Math.max(maxCount, ++count[s.charAt(right) - 'A']);
            while (right - left + 1 - maxCount > k) {
                count[s.charAt(left) - 'A']--;
                left++;
            }
            maxLen = Math.max(maxLen, right - left + 1);
        }
        return maxLen;
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 3
2. Leetcode 159/340
3. Leetcode 1004

---

## 5) MEDIUM-2 | Max Consecutive Ones III | Leetcode 1004

### Problem
Longest subarray of 1's after flipping at most k 0's.

### Approach
Same as character replacement but only '0' count.

### Java Solution
```java
class Solution {
    public int longestOnes(int[] nums, int k) {
        int left = 0, zeroCount = 0, maxLen = 0;
        for (int right = 0; right < nums.length; right++) {
            if (nums[right] == 0) zeroCount++;
            while (zeroCount > k) {
                if (nums[left] == 0) zeroCount--;
                left++;
            }
            maxLen = Math.max(maxLen, right - left + 1);
        }
        return maxLen;
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 487
2. Leetcode 424
3. Leetcode 1493 - Longest Subarray of 1's After Deleting One Element

---

## 6) HARD-1 | Minimum Window Subsequence | Leetcode 727 (Advanced Variant)

### Problem
Find minimum window in S containing T as subsequence.

### Approach
For each start in S, expand to find T as subsequence, track min window.

### Java Solution
```java
class Solution {
    public String minWindow(String s1, String s2) {
        int n1 = s1.length(), n2 = s2.length();
        String res = "";
        int minLen = Integer.MAX_VALUE;
        for (int i = 0; i < n1; i++) {
            if (s1.charAt(i) == s2.charAt(0)) {
                int j = i, k = 0;
                while (j < n1 && k < n2) {
                    if (s1.charAt(j) == s2.charAt(k)) k++;
                    j++;
                }
                if (k == n2 && (j - i) < minLen) {
                    minLen = j - i;
                    res = s1.substring(i, j);
                }
            }
        }
        return res;
    }
}
```
**TC:** O(n1*n2) in worst bad case, often efficient enough; optimal can be done with DP. Understand this approach.

### Similar
1. Leetcode 76 - Minimum Window Substring
2. Leetcode 30
3. Leetcode 392 - Is Subsequence

---

## END OF DAY REVIEW
- **Learned:** Variable window conditions
- **Mistakes:** [Fill]
- **Weak Points:** [Fill]
- **Revision Due:** D+1 | D+3 | D+7 | D+14 | D+30
