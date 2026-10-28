# DAY-001 | PATTERN FOCUS: Arrays + Hashing Fundamentals | TARGET: 1H + 2M + 3E

> **Objective:** Build rock-solid foundation in arrays, frequency maps and lookup-based thinking. Train yourself to think in terms of "Can I use a HashMap/HashSet here?"

**Date:** [DD-MM-YYYY]  
**Status:** NOT STARTED  
**Time Spent:** 00:00  
**Confidence:** 0/10

## LEARNING GOAL FOR TODAY
- [ ] Master array traversal & edge cases
- [ ] Use HashMap for frequency/count
- [ ] Spot O(1) lookup opportunities
- [ ] Write clean Java solutions with TC/SC

---

## 1) EASY-1 | Find The Highest Altitude | Leetcode 1732

### Problem Statement
There is a biker going on a road trip. The road trip consists of `n + 1` points at different altitudes. You are given an integer array `gain` of length `n` where `gain[i]` is the net gain in altitude between point `i` and `i+1` (i.e., `altitude[i+1] = altitude[i] + gain[i]`). The altitude at point 0 is `0`. Return the highest altitude of a point.

### Constraints
- `n == gain.length`
- `1 <= n <= 100`
- `-100 <= gain[i] <= 100`

### Examples
**Example 1:** gain = [5,19,8,3] -> Output: 35  
**Example 2:** gain = [-5,1,5,0,-7] -> Output: 1

### Approach
1. Track current altitude starting from 0, maintain maxAltitude = 0
2. For each g in gain: currentAltitude += g; maxAltitude = max(maxAltitude, currentAltitude)
3. Return maxAltitude

### Java Solution
```java
class Solution {
    public int largestAltitude(int[] gain) {
        int currentAltitude = 0;
        int maxAltitude = 0;
        for (int g : gain) {
            currentAltitude += g;
            maxAltitude = Math.max(maxAltitude, currentAltitude);
        }
        return maxAltitude;
    }
}
```

### Complexity
- Time: O(n)
- Space: O(1)

### Edge Cases
- [ ] All negative
- [ ] All zero
- [ ] Single element

### Similar Questions (Must Do On Revision)
1. Leetcode 1486 - XOR Operation in an Array
2. Leetcode 1672 - Richest Customer Wealth
3. Leetcode 1920 - Build Array from Permutation

**Self Check:** [ ] Solved unaided  [ ] Explained  [ ] Tested edge cases

---

## 2) EASY-2 | Valid Anagram | Leetcode 242

### Problem Statement
Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, else `false`.

### Constraints
- `1 <= s.length, t.length <= 5e4`
- lowercase English letters

### Examples
s="anagram", t="nagaram" -> true  
s="rat", t="car" -> false

### Approach
1. If lengths different return false
2. Frequency array of 26, count[s[i]-'a']++, count[t[i]-'a']--
3. Check all zero

### Java Solution
```java
class Solution {
    public boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;
        int[] count = new int[26];
        for (int i = 0; i < s.length(); i++) {
            count[s.charAt(i) - 'a']++;
            count[t.charAt(i) - 'a']--;
        }
        for (int c : count) if (c != 0) return false;
        return true;
    }
}
```

### Complexity
- Time: O(n)
- Space: O(1)

### Similar Questions
1. Leetcode 49 - Group Anagrams
2. Leetcode 438 - Find All Anagrams in a String
3. Leetcode 383 - Ransom Note

---

## 3) EASY-3 | Two Sum | Leetcode 1

### Problem Statement
Return indices [i,j] such that nums[i]+nums[j]==target, different elements, exactly one solution.

### Approach
HashMap value -> index, check complement in one pass.

### Java Solution
```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int comp = target - nums[i];
            if (map.containsKey(comp)) {
                return new int[]{map.get(comp), i};
            }
            map.put(nums[i], i);
        }
        return new int[]{};
    }
}
```

### Complexity
- Time: O(n)
- Space: O(n)

### Similar Questions
1. Leetcode 167 - Two Sum II
2. Leetcode 15 - 3Sum
3. Leetcode 1 variations

---

## 4) MEDIUM-1 | Longest Substring Without Repeating Characters | Leetcode 3

### Problem Statement
Length of longest substring without repeating characters.

### Approach
Sliding window [left,right] + HashMap char->index, shrink left when duplicate seen.

### Java Solution
```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> map = new HashMap<>();
        int left = 0, maxLen = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            if (map.containsKey(c) && map.get(c) >= left) {
                left = map.get(c) + 1;
            }
            map.put(c, right);
            maxLen = Math.max(maxLen, right - left + 1);
        }
        return maxLen;
    }
}
```

### Complexity
- Time: O(n)
- Space: O(min(n,128))

### Similar Questions
1. Leetcode 159 - At Most Two Distinct
2. Leetcode 340 - At Most K Distinct
3. Leetcode 424 - Longest Repeating Character Replacement

---

## 5) MEDIUM-2 | Group Anagrams | Leetcode 49

### Problem Statement
Group strings that are anagrams.

### Approach
HashMap<String,List<String>>, key = sorted string of each group.

### Java Solution
```java
import java.util.*;

class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for (String s : strs) {
            char[] arr = s.toCharArray();
            Arrays.sort(arr);
            String key = new String(arr);
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
        }
        return new ArrayList<>(map.values());
    }
}
```

### Complexity
- Time: O(m*k log k)
- Space: O(m*k)

### Similar Questions
1. Leetcode 242
2. Leetcode 438
3. Leetcode 249

---

## 6) HARD-1 | Minimum Window Substring | Leetcode 76

### Problem Statement
Minimum window in s containing all chars of t (with counts).

### Approach
need map, window map, formed count, expand right, shrink left while valid.

### Java Solution
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
            if (need.containsKey(c) && window.get(c).intValue() == need.get(c).intValue()) {
                formed++;
            }
            while (formed == required && left <= right) {
                if (right - left + 1 < len) {
                    len = right - left + 1;
                    start = left;
                }
                char leftChar = s.charAt(left);
                window.put(leftChar, window.get(leftChar) - 1);
                if (need.containsKey(leftChar) && window.get(leftChar).intValue() < need.get(leftChar).intValue()) {
                    formed--;
                }
                left++;
            }
        }
        return len == Integer.MAX_VALUE ? "" : s.substring(start, start + len);
    }
}
```

### Complexity
- Time: O(m+n)
- Space: O(m+n)

### Similar Questions
1. Leetcode 30 - Substring with Concatenation of All Words
2. Leetcode 438
3. Leetcode 567 - Permutation in String

---

## END OF DAY REVIEW
- **Learned:** HashMap lookups, sliding window, frequency counting
- **Mistakes:** [Fill]
- **Weak Points:** [Fill]
- **Action:** Revise weak ones
- **Revision Due:** D+1 | D+3 | D+7 | D+14 | D+30
