# DAY-006 | PATTERN FOCUS: HashMap Mastery | TARGET: 1H + 2M + 3E

> **Objective:** Deep HashMap usage - frequency, mapping, two-sum family, groupings.

---

## 1) EASY-1 | Ransom Note | Leetcode 383

### Problem
Can ransomNote be constructed from magazine?

### Java Solution
```java
class Solution {
    public boolean canConstruct(String ransomNote, String magazine) {
        int[] count = new int[26];
        for (char c : magazine.toCharArray()) count[c - 'a']++;
        for (char c : ransomNote.toCharArray()) {
            if (--count[c - 'a'] < 0) return false;
        }
        return true;
    }
}
```
**TC:** O(m+n) | **SC:** O(1)

### Similar
1. Leetcode 242
2. Leetcode 387 - First Unique Character in a String
3. Leetcode 205

---

## 2) EASY-2 | First Unique Character in a String | Leetcode 387

### Problem
Index of first non-repeating character.

### Java Solution
```java
class Solution {
    public int firstUniqChar(String s) {
        int[] count = new int[26];
        for (char c : s.toCharArray()) count[c - 'a']++;
        for (int i = 0; i < s.length(); i++) {
            if (count[s.charAt(i) - 'a'] == 1) return i;
        }
        return -1;
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 383
2. Leetcode 451 - Sort Characters By Frequency
3. Leetcode 389 - Find the Difference

---

## 3) EASY-3 | Isomorphic Strings | Leetcode 205

### Problem
s and t isomorphic if chars map one-to-one.

### Approach
Two maps or map + set.

### Java Solution
```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public boolean isIsomorphic(String s, String t) {
        Map<Character, Character> map1 = new HashMap<>();
        Map<Character, Character> map2 = new HashMap<>();
        for (int i = 0; i < s.length(); i++) {
            char c1 = s.charAt(i), c2 = t.charAt(i);
            if (map1.containsKey(c1) && map1.get(c1) != c2) return false;
            if (map2.containsKey(c2) && map2.get(c2) != c1) return false;
            map1.put(c1, c2);
            map2.put(c2, c1);
        }
        return true;
    }
}
```
**TC:** O(n) | **SC:** O(1)

### Similar
1. Leetcode 290 - Word Pattern
2. Leetcode 205
3. Leetcode 49

---

## 4) MEDIUM-1 | Top K Frequent Elements | Leetcode 347

### Problem
Return k most frequent elements.

### Approach
HashMap frequency + Bucket sort by frequency OR PriorityQueue.

### Java Solution (Bucket Sort)
```java
import java.util.*;

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> count = new HashMap<>();
        for (int num : nums) count.put(num, count.getOrDefault(num, 0) + 1);
        List<Integer>[] buckets = new List[nums.length + 1];
        for (int i = 0; i < buckets.length; i++) buckets[i] = new ArrayList<>();
        for (int key : count.keySet()) {
            buckets[count.get(key)].add(key);
        }
        List<Integer> res = new ArrayList<>();
        for (int i = buckets.length - 1; i >= 0 && res.size() < k; i--) {
            res.addAll(buckets[i]);
        }
        int[] ans = new int[k];
        for (int i = 0; i < k; i++) ans[i] = res.get(i);
        return ans;
    }
}
```
**TC:** O(n) | **SC:** O(n)

### Similar
1. Leetcode 451 - Sort Characters By Frequency
2. Leetcode 692 - Top K Frequent Words
3. Leetcode 973 - K Closest Points to Origin

---

## 5) MEDIUM-2 | Sort Characters By Frequency | Leetcode 451

### Problem
Sort string by frequency descending.

### Java Solution (Bucket)
```java
import java.util.*;

class Solution {
    public String frequencySort(String s) {
        Map<Character, Integer> count = new HashMap<>();
        for (char c : s.toCharArray()) count.put(c, count.getOrDefault(c, 0) + 1);
        List<Character>[] buckets = new List[s.length() + 1];
        for (int i = 0; i < buckets.length; i++) buckets[i] = new ArrayList<>();
        for (char c : count.keySet()) buckets[count.get(c)].add(c);
        StringBuilder sb = new StringBuilder();
        for (int i = buckets.length - 1; i >= 0; i--) {
            for (char c : buckets[i]) {
                for (int j = 0; j < i; j++) sb.append(c);
            }
        }
        return sb.toString();
    }
}
```
**TC:** O(n log M) where M unique | **SC:** O(n)

### Similar
1. Leetcode 347
2. Leetcode 692
3. Leetcode 1636 - Sort Array by Increasing Frequency

---

## 6) HARD-1 | Longest Substring with At Most K Distinct Characters | Leetcode 340

### Problem
Longest substring with at most k distinct chars.

### Java Solution
```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int lengthOfLongestSubstringKDistinct(String s, int k) {
        Map<Character, Integer> map = new HashMap<>();
        int left = 0, maxLen = 0;
        for (int right = 0; right < s.length(); right++) {
            map.put(s.charAt(right), map.getOrDefault(s.charAt(right), 0) + 1);
            while (map.size() > k) {
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
**TC:** O(n) | **SC:** O(k)

### Similar
1. Leetcode 159 - At Most Two
2. Leetcode 3
3. Leetcode 904 - Fruit Into Baskets

---

## END OF DAY REVIEW
- **Learned:** Frequency maps, bucket sort, distinct count
- **Mistakes:** [Fill]
- **Weak Points:** [Fill]
- **Revision Due:** D+1 | D+3 | D+7 | D+14 | D+30
