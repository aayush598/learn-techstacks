# DAY-007 | PATTERN FOCUS: WEEKLY REVISION MIX (WEEK-01) | TARGET: 1H + 2M + 3E

> **Objective:** Mixed revision from Days 1-6. Solve unaided. Fix all REVISIT from tracker.

**MANDATORY:** Do NOT peek. Time yourself strictly.

---

## 1) EASY-1 | Valid Palindrome (Revive) | Leetcode 125
Redo without looking at DAY-002 solution.

### Quick Approach Reminder
Two pointers skip non-alnum, compare case-insensitively.

### Java Solution
```java
class Solution {
    public boolean isPalindrome(String s) {
        int left = 0, right = s.length()-1;
        while (left < right) {
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) left++;
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) right--;
            if (Character.toLowerCase(s.charAt(left++)) != Character.toLowerCase(s.charAt(right--))) return false;
        }
        return true;
    }
}
```

---

## 2) EASY-2 | Contains Duplicate II (Revive) | Leetcode 219
Redo sliding window HashSet of size k.

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

---

## 3) EASY-3 | First Unique Character (Revive) | Leetcode 387
Redo frequency map.

### Java Solution
```java
class Solution {
    public int firstUniqChar(String s) {
        int[] count = new int[26];
        for (char c : s.toCharArray()) count[c-'a']++;
        for (int i = 0; i < s.length(); i++) if (count[s.charAt(i)-'a']==1) return i;
        return -1;
    }
}
```

---

## 4) MEDIUM-1 | 3Sum (Revive) | Leetcode 15
Critical for FAANG. Sort + two pointers + skip duplicates.

### Java Solution (Recall)
```java
import java.util.*;

class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        Arrays.sort(nums);
        for (int i = 0; i < nums.length - 2; i++) {
            if (i > 0 && nums[i] == nums[i-1]) continue;
            int l = i+1, r = nums.length-1;
            while (l < r) {
                int sum = nums[i] + nums[l] + nums[r];
                if (sum == 0) {
                    res.add(Arrays.asList(nums[i], nums[l], nums[r]));
                    while (l < r && nums[l] == nums[l+1]) l++;
                    while (l < r && nums[r] == nums[r-1]) r--;
                    l++; r--;
                } else if (sum < 0) l++;
                else r--;
            }
        }
        return res;
    }
}
```

---

## 5) MEDIUM-2 | Longest Repeating Character Replacement (Revive) | Leetcode 424
Sliding window with maxCount.

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

---

## 6) HARD-1 | Minimum Window Substring (Revive) | Leetcode 76
Do this with full approach explanation in mind.

### Java Solution (Recall)
```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public String minWindow(String s, String t) {
        if (s.length() < t.length()) return "";
        Map<Character, Integer> need = new HashMap<>();
        for (char c : t.toCharArray()) need.put(c, need.getOrDefault(c, 0) + 1);
        Map<Character, Integer> window = new HashMap<>();
        int left = 0, formed = 0, required = need.size();
        int len = Integer.MAX_VALUE, start = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            window.put(c, window.getOrDefault(c, 0) + 1);
            if (need.containsKey(c) && window.get(c).intValue() == need.get(c).intValue()) formed++;
            while (formed == required) {
                if (right - left + 1 < len) {
                    len = right - left + 1;
                    start = left;
                }
                char lc = s.charAt(left);
                window.put(lc, window.getOrDefault(lc, 0) - 1);
                if (need.containsKey(lc) && window.get(lc).intValue() < need.get(lc).intValue()) formed--;
                left++;
            }
        }
        return len == Integer.MAX_VALUE ? "" : s.substring(start, start + len);
    }
}
```

---

## WEEKLY AUDIT
- [ ] All 42 questions from Week 1 attempted (6/day)
- [ ] Revised REVISIT list
- [ ] Can explain Top 5 patterns without notes
- [ ] Timed at least 2 questions
- [ ] Updated `resources/DAILY-PROGRESS-TRACKER.md`

## NOTES
- **Strongest Pattern:** [Fill]
- **Weakest Pattern:** [Fill]
- **Focus for Week 2:** [Fill]
