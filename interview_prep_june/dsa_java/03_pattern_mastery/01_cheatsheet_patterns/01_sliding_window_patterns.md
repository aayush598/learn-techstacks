# Sliding Window Patterns

## Table of Contents
1. When to Use Sliding Window
2. Fixed Size Window
3. Variable Size Window (Expand/Contract)
4. Longest Subarray/Substring Satisfying Condition
5. Minimum Window Satisfying Condition
6. Window with Auxiliary Data Structure
7. Pattern Recognition Checklist
8. Common Mistakes and Pitfalls

---

## 1. When to Use Sliding Window

**Core criteria:**
- The problem involves a linear data structure (array, string, linked list)
- You need to find a contiguous subarray/substring that satisfies a condition
- The answer asks for: longest/shortest/minimum/maximum/contains/count

**Complexity:**
- Without sliding window: O(n²) or O(n³)
- With sliding window: O(n) time, O(1) or O(k) space

**Not a good fit when:**
- The array is not contiguous (subsequence problems)
- The condition cannot be checked incrementally
- The data structure is not linear (trees, graphs — use DFS/BFS)

---

## 2. Fixed Size Window

**Pattern:** Window size `k` is given. Slide the window across the array, computing something at each position.

**Template:**
```java
int fixedWindow(int[] arr, int k) {
    int n = arr.length;
    if (n < k) return -1; // or handle edge case

    // Compute first window
    int windowSum = 0;
    for (int i = 0; i < k; i++) {
        windowSum += arr[i];
    }
    int maxSum = windowSum;

    // Slide window
    for (int right = k; right < n; right++) {
        // Add new element, remove leftmost element
        windowSum += arr[right] - arr[right - k];
        maxSum = Math.max(maxSum, windowSum);
    }
    return maxSum;
}
```

**Common problems:**
- Maximum sum subarray of size K
- First negative in every window of size K
- Count occurrences of anagram in a string (sliding window + char frequency map)
- Max average subarray I
- Sliding window maximum (use Deque)

**Example: Max Average Subarray**

```java
public double findMaxAverage(int[] nums, int k) {
    int n = nums.length;
    int sum = 0;
    for (int i = 0; i < k; i++) sum += nums[i];
    int maxSum = sum;
    for (int i = k; i < n; i++) {
        sum += nums[i] - nums[i - k];
        maxSum = Math.max(maxSum, sum);
    }
    return (double) maxSum / k;
}
```

---

## 3. Variable Size Window (Expand/Contract)

**Pattern:** Window size is not fixed. Expand right pointer, and when condition is broken, move left pointer until condition is restored.

**Template:**
```java
int variableWindow(String s) {
    int left = 0, n = s.length();
    int[] freq = new int[256]; // or HashMap
    int maxLen = 0;
    // ... other state variables

    for (int right = 0; right < n; right++) {
        char c = s.charAt(right);
        freq[c]++; // expand window

        while (/* condition violated */) {
            char lc = s.charAt(left);
            freq[lc]--; // shrink window
            left++;
        }

        // Condition satisfied, update answer
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

**Common problems:**
- Longest substring without repeating characters
- Longest substring with at most K distinct characters
- Longest substring with at least K repeating characters
- Max consecutive ones III
- Fruit into baskets

**Example: Longest Substring Without Repeating Characters**

```java
public int lengthOfLongestSubstring(String s) {
    int[] freq = new int[128];
    int left = 0, maxLen = 0;
    for (int right = 0; right < s.length(); right++) {
        freq[s.charAt(right)]++;
        while (freq[s.charAt(right)] > 1) {
            freq[s.charAt(left)]--;
            left++;
        }
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

---

## 4. Longest Subarray/Substring Satisfying Condition

**Approach:** Expand right until condition is violated, then shrink left until condition is restored. Track max window size.

**Template:**
```java
int longestSatisfying(int[] arr, int k) {
    int left = 0, n = arr.length;
    int state = 0; // tracks violation condition
    int maxLen = 0;

    for (int right = 0; right < n; right++) {
        // Update state with arr[right]

        while (/* state is INVALID */) {
            // Update state by removing arr[left]
            left++;
        }

        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

**Variations:**
- Largest subarray with sum <= K
- Longest subarray with at most K zeroes (max consecutive ones III)
- Longest substring with K distinct characters
- Longest substring with all characters > K frequency

**Example: Max Consecutive Ones III**
```java
public int longestOnes(int[] nums, int k) {
    int left = 0, zeroes = 0, maxLen = 0;
    for (int right = 0; right < nums.length; right++) {
        if (nums[right] == 0) zeroes++;
        while (zeroes > k) {
            if (nums[left] == 0) zeroes--;
            left++;
        }
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

---

## 5. Minimum Window Satisfying Condition

**Approach:** Find the smallest window that satisfies a condition. Expand right until condition is satisfied, then try to shrink left while condition still holds.

**Template:**
```java
String minWindow(String s, String t) {
    int[] need = new int[128];
    for (char c : t.toCharArray()) need[c]++;
    int required = t.length();

    int left = 0, minLen = Integer.MAX_VALUE, start = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        if (need[c] > 0) required--;
        need[c]--;

        while (required == 0) { // condition met
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                start = left;
            }
            char lc = s.charAt(left);
            need[lc]++;
            if (need[lc] > 0) required++;
            left++;
        }
    }
    return minLen == Integer.MAX_VALUE ? "" : s.substring(start, start + minLen);
}
```

**Common problems:**
- Minimum window substring
- Minimum size subarray sum
- Minimum window with K distinct characters
- Smallest subarray with sum greater than target

**Example: Minimum Size Subarray Sum**
```java
public int minSubArrayLen(int target, int[] nums) {
    int left = 0, sum = 0, minLen = Integer.MAX_VALUE;
    for (int right = 0; right < nums.length; right++) {
        sum += nums[right];
        while (sum >= target) {
            minLen = Math.min(minLen, right - left + 1);
            sum -= nums[left];
            left++;
        }
    }
    return minLen == Integer.MAX_VALUE ? 0 : minLen;
}
```

---

## 6. Window with Auxiliary Data Structure

### HashMap / Frequency Array
**When:** Need to track frequency of elements in the window (anagrams, distinct characters).

```java
int countAnagrams(String s, String pattern) {
    int[] need = new int[26];
    for (char c : pattern.toCharArray()) need[c - 'a']++;
    int[] have = new int[26];
    int k = pattern.length(), count = 0;

    for (int right = 0; right < s.length(); right++) {
        have[s.charAt(right) - 'a']++;
        if (right >= k - 1) {
            if (Arrays.equals(need, have)) count++;
            have[s.charAt(right - k + 1) - 'a']--;
        }
    }
    return count;
}
```

### Deque (Monotonic Queue)
**When:** Need min/max in sliding window.

```java
// Sliding Window Maximum
public int[] maxSlidingWindow(int[] nums, int k) {
    int n = nums.length;
    int[] result = new int[n - k + 1];
    Deque<Integer> dq = new ArrayDeque<>(); // stores indices

    for (int i = 0; i < n; i++) {
        // Remove out-of-window indices
        while (!dq.isEmpty() && dq.peekFirst() < i - k + 1)
            dq.pollFirst();

        // Remove smaller elements (maintain decreasing order)
        while (!dq.isEmpty() && nums[dq.peekLast()] <= nums[i])
            dq.pollLast();

        dq.offerLast(i);

        if (i >= k - 1)
            result[i - k + 1] = nums[dq.peekFirst()];
    }
    return result;
}
```

### Multiset / TreeMap
**When:** Need to query order statistics in the window (sliding window median).

```java
// Sliding Window Median
public double[] medianSlidingWindow(int[] nums, int k) {
    double[] result = new double[nums.length - k + 1];
    TreeMap<Integer, Integer> left = new TreeMap<>(Collections.reverseOrder());
    TreeMap<Integer, Integer> right = new TreeMap<>();
    // ... balancing logic similar to two heaps
    return result;
}
```

### Set
**When:** Contains Duplicate in window (presence check).

```java
public boolean containsNearbyDuplicate(int[] nums, int k) {
    Set<Integer> window = new HashSet<>();
    for (int i = 0; i < nums.length; i++) {
        if (window.contains(nums[i])) return true;
        window.add(nums[i]);
        if (window.size() > k) window.remove(nums[i - k]);
    }
    return false;
}
```

---

## 7. Pattern Recognition Checklist

Use this checklist to decide if sliding window applies:

```
Does the problem involve:
[ ] Array or String
[ ] Contiguous subarray/substring
[ ] "Maximum/minimum/longest/shortest satisfying condition"
[ ] "Count subarrays where condition holds"
[ ] Sorted array (optional — helps but not required)

If 3+ checks, sliding window is likely applicable
```

**Distinguish subarray vs subsequence:**
- Subarray → contiguous → Sliding Window or Prefix Sum
- Subsequence → not necessarily contiguous → DP, Two Pointers, or Greedy

**Distinguish fixed vs variable:**
- Fixed K given → Fixed window
- "Longest with condition" → Variable window (expand right, contract when invalid)
- "Shortest with condition" → Variable window (expand until valid, contract to minimize)
- "Count subarrays with condition" → Variable window (count contributions on each expansion)

---

## 8. Common Mistakes and Pitfalls

| Mistake | Solution |
|---------|----------|
| Not handling empty/null input | Add early return checks |
| Off-by-one in window boundaries | Template: right is inclusive, left is inclusive |
| Forgetting to update answer for all windows | In fixed: update every slide. In variable: update after inner while |
| Using O(n²) when O(n) suffices | Don't nest loops that re-traverse the window |
| Not resetting state properly when shrinking | Ensure removal logic mirrors addition logic |
| Integer overflow for sum | Use `long` if needed |
| Conflating subarray with subsequence | Check if contiguous is required |
| Wrong inner loop direction | Expand right in outer, shrink left in inner |

---

## Quick Reference

| Problem Type | Window Type | State Tracking | When to Record |
|-------------|-------------|----------------|----------------|
| Max sum subarray of size K | Fixed | Sum | After each full window |
| Longest substring w/o repeat | Variable | Char frequency | After fixing violation |
| Min window substring | Variable | Required count | After condition met, while shrinking |
| Sliding window max | Fixed (or var) | Deque indices | Every slide |
| Count anagram occurrences | Fixed | Frequency arrays | When arrays match |
| Max consecutive ones III | Variable | Zero count | After fixing violation |
| Fruit into baskets | Variable | Distinct count | After fixing violation |
| Subarray product less than K | Variable | Product | Right - left + 1 contribution |
