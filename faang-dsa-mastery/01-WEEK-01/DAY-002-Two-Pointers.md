# DAY-002 | PATTERN FOCUS: Two Pointers | TARGET: 1H + 2M + 3E

> **Objective:** Master opposite-direction and same-direction two pointers. Learn when two pointers beats nested loops.

**Status:** NOT STARTED | **Time:** 00:00 | **Conf:** 0/10

## LEARNING GOAL
- [ ] Opposite pointers (left/right)
- [ ] Same pointers / fast-slow
- [ ] Handle sorted arrays efficiently
- [ ] Avoid duplicates correctly

---

## 1) EASY-1 | Valid Palindrome | Leetcode 125

### Problem
Check if string is palindrome, consider only alphanumeric, ignore case.

### Approach
Two pointers left=0,right=len-1, skip non-alnum, compare lowercase.

### Java Solution
```java
class Solution {
    public boolean isPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) left++;
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) right--;
            if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))) return false;
            left++; right--;
        }
        return true;
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 234 - Palindrome Linked List
2. Leetcode 9 - Palindrome Number
3. Leetcode 680 - Valid Palindrome II

---

## 2) EASY-2 | Merge Two Sorted Lists | Leetcode 21

### Problem
Merge two sorted linked lists into one sorted list.

### Approach
Dummy node + two pointers.

### Java Solution
```java
class ListNode {
    int val; ListNode next;
    ListNode() {}
    ListNode(int val){ this.val=val; }
    ListNode(int val,ListNode next){ this.val=val; this.next=next; }
}
class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummy = new ListNode(0);
        ListNode cur = dummy;
        while (list1 != null && list2 != null) {
            if (list1.val <= list2.val) {
                cur.next = list1;
                list1 = list1.next;
            } else {
                cur.next = list2;
                list2 = list2.next;
            }
            cur = cur.next;
        }
        cur.next = (list1 != null) ? list1 : list2;
        return dummy.next;
    }
}
```
**TC:** O(m+n) | **SC:** O(1)

### Similar
1. Leetcode 23 - Merge k Sorted Lists
2. Leetcode 88 - Merge Sorted Array
3. Leetcode 1669 - Merge In Between Linked Lists

---

## 3) EASY-3 | Two Sum II - Input Array Is Sorted | Leetcode 167

### Problem
Sorted ascending array, return 1-based indices of two numbers summing to target.

### Approach
left=0,right=n-1, if sum<target left++, if sum>target right-- else return.

### Java Solution
```java
class Solution {
    public int[] twoSum(int[] numbers, int target) {
        int left = 0, right = numbers.length - 1;
        while (left < right) {
            int sum = numbers[left] + numbers[right];
            if (sum == target) return new int[]{left+1, right+1};
            if (sum < target) left++;
            else right--;
        }
        return new int[]{};
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 1 - Two Sum
2. Leetcode 15 - 3Sum
3. Leetcode 16 - 3Sum Closest

---

## 4) MEDIUM-1 | 3Sum | Leetcode 15

### Problem
Find all triplets [a,b,c] with a+b+c==0, no duplicates.

### Approach
Sort array, fix i, use two pointers l=i+1,r=n-1, skip duplicates.

### Java Solution
```java
import java.util.*;

class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        Arrays.sort(nums);
        for (int i = 0; i < nums.length - 2; i++) {
            if (i > 0 && nums[i] == nums[i-1]) continue;
            int left = i+1, right = nums.length-1;
            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                if (sum == 0) {
                    res.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    while (left < right && nums[left] == nums[left+1]) left++;
                    while (left < right && nums[right] == nums[right-1]) right--;
                    left++; right--;
                } else if (sum < 0) left++;
                else right--;
            }
        }
        return res;
    }
}
```
**TC:** O(n^2) | **SC:** O(1) excluding output

### Similar
1. Leetcode 16 - 3Sum Closest
2. Leetcode 18 - 4Sum
3. Leetcode 259 - 3Sum Smaller

---

## 5) MEDIUM-2 | Container With Most Water | Leetcode 11

### Problem
Max area between vertical lines.

### Approach
Two pointers, area = min(h[l],h[r])*(r-l), move pointer with smaller height.

### Java Solution
```java
class Solution {
    public int maxArea(int[] height) {
        int left = 0, right = height.length - 1;
        int maxArea = 0;
        while (left < right) {
            int area = Math.min(height[left], height[right]) * (right - left);
            maxArea = Math.max(maxArea, area);
            if (height[left] < height[right]) left++;
            else right--;
        }
        return maxArea;
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 42 - Trapping Rain Water
2. Leetcode 407 - Trapping Rain Water II
3. Leetcode 84 - Largest Rectangle in Histogram

---

## 6) HARD-1 | Trapping Rain Water | Leetcode 42

### Problem
Compute trapped rain water after raining.

### Approach (Two Pointers - Optimal)
Track leftMax and rightMax, move pointer with smaller max.

### Java Solution
```java
class Solution {
    public int trap(int[] height) {
        if (height.length == 0) return 0;
        int left = 0, right = height.length - 1;
        int leftMax = 0, rightMax = 0;
        int water = 0;
        while (left < right) {
            if (height[left] < height[right]) {
                if (height[left] >= leftMax) leftMax = height[left];
                else water += leftMax - height[left];
                left++;
            } else {
                if (height[right] >= rightMax) rightMax = height[right];
                else water += rightMax - height[right];
                right--;
            }
        }
        return water;
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 407 - Trapping Rain Water II
2. Leetcode 11 - Container With Most Water
3. Leetcode 84 - Largest Rectangle in Histogram

---

## END OF DAY REVIEW
- **Learned:** Two pointers patterns, duplicate handling
- **Mistakes:** [Fill]
- **Weak Points:** [Fill]
- **Revision Due:** D+1 | D+3 | D+7 | D+14 | D+30
