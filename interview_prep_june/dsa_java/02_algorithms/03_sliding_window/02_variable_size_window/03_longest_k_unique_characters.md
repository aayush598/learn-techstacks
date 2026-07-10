# Longest Substring with At Most K Distinct Characters

This is a classic variable-size sliding window problem that tests your ability to handle a constraint on **distinct elements** in the window.

## Problem Statement

Given a string, find the length of the longest substring that contains **at most K distinct characters**.

```
Input:  s = "eceba", k = 2
Output: 3
Explanation: "ece" has 2 distinct characters (e, c), length 3
             "ceb" has 3 distinct characters — invalid
             "eba" has 3 distinct characters — invalid
             So the longest with at most 2 is "ece"

Input:  s = "aa", k = 1
Output: 2
Explanation: "aa" has 1 distinct character (a), length 2
```

## The Solution

```java
public int longestKDistinct(String s, int k) {
    if (k == 0 || s.isEmpty()) return 0;

    Map<Character, Integer> freq = new HashMap<>();
    int left = 0;
    int maxLen = 0;

    for (int right = 0; right < s.length(); right++) {
        // Add current character to window
        char c = s.charAt(right);
        freq.put(c, freq.getOrDefault(c, 0) + 1);

        // Shrink if we exceed k distinct characters
        while (freq.size() > k) {
            char leftChar = s.charAt(left);
            freq.put(leftChar, freq.get(leftChar) - 1);
            if (freq.get(leftChar) == 0) {
                freq.remove(leftChar);
            }
            left++;
        }

        // Update max length
        maxLen = Math.max(maxLen, right - left + 1);
    }

    return maxLen;
}
```

### The Key: Removing Characters from HashMap

When we shrink the window, we decrement the frequency. If it reaches 0, we **remove** the key from the map. Otherwise, `freq.size()` would still count it as a distinct character.

### Dry Run

```
s = "eceba", k = 2

left=0, freq={}, maxLen=0

right=0, c='e': freq={e:1}, size=1≤2, window=[0,0], len=1, maxLen=1
right=1, c='c': freq={e:1,c:1}, size=2≤2, window=[0,1], len=2, maxLen=2
right=2, c='e': freq={e:2,c:1}, size=2≤2, window=[0,2], len=3, maxLen=3
right=3, c='b': freq={e:2,c:1,b:1}, size=3>2
  → shrink: leftChar='e', freq={e:1,c:1,b:1}, left=1
  → size still 3>2, shrink: leftChar='c', freq={e:1,c:0,b:1}, remove c, freq={e:1,b:1}, left=2
  → size=2≤2, stop
  window=[2,3], len=2, maxLen=3
right=4, c='a': freq={e:1,b:1,a:1}, size=3>2
  → shrink: leftChar='e', freq={e:0,b:1,a:1}, remove e, freq={b:1,a:1}, left=3
  → size=2≤2, stop
  window=[3,4], len=2, maxLen=3

Result: 3 ("ece") ✓
```

## Array Optimization (for ASCII)

```java
public int longestKDistinctArray(String s, int k) {
    if (k == 0 || s.isEmpty()) return 0;

    int[] freq = new int[128];
    int distinct = 0;
    int left = 0;
    int maxLen = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        if (freq[c] == 0) distinct++;
        freq[c]++;

        while (distinct > k) {
            char leftChar = s.charAt(left);
            freq[leftChar]--;
            if (freq[leftChar] == 0) distinct--;
            left++;
        }

        maxLen = Math.max(maxLen, right - left + 1);
    }

    return maxLen;
}
```

## Longest Substring with *At Least* K Distinct Characters

Less common, but tests the same concept:

```java
public int longestAtLeastKDistinct(String s, int k) {
    // Instead of limiting, it's the entire string if we have at least k
    boolean[] seen = new boolean[128];
    int distinct = 0;

    for (char c : s.toCharArray()) {
        if (!seen[c]) {
            seen[c] = true;
            distinct++;
        }
    }

    return distinct >= k ? s.length() : 0;
}
```

Trivial — if we have at least k distinct characters somewhere, the longest substring with at least k distinct is the whole string (since we can always expand and maintain the "at least" condition).

Wait, that's not quite right. Actually the longest substring with at least k distinct is just the whole string if it has >= k distinct, because a bigger substring always has >= distinct characters compared to a smaller one. So it's the entire string.

## Longest Substring with *Exactly* K Distinct Characters

This is trickier. We can use the "at most K" trick:

```java
public int longestExactlyKDistinct(String s, int k) {
    return longestKDistinct(s, k) - longestKDistinct(s, k - 1);
}
```

Or implement it directly:

```java
public int longestExactlyKDistinctDirect(String s, int k) {
    if (k == 0) return 0;

    Map<Character, Integer> freq = new HashMap<>();
    int left = 0;
    int maxLen = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        freq.put(c, freq.getOrDefault(c, 0) + 1);

        while (freq.size() > k) {
            char leftChar = s.charAt(left);
            freq.put(leftChar, freq.get(leftChar) - 1);
            if (freq.get(leftChar) == 0) freq.remove(leftChar);
            left++;
        }

        // Only update when exactly k
        if (freq.size() == k) {
            maxLen = Math.max(maxLen, right - left + 1);
        }
    }

    return maxLen;
}
```

## Generalization: At Most K

The "at most K" pattern is powerful. Here's a template that works for many problems:

```java
public int atMostK(int[] arr, int k, <condition>) {
    int left = 0;
    int result = 0;

    // Some state tracking
    int current = 0;

    for (int right = 0; right < arr.length; right++) {
        // Update state with arr[right]

        while (<condition violates "at most k">) {
            // Remove arr[left] from state
            left++;
        }

        // All windows ending at 'right' are valid
        result = Math.max(result, right - left + 1);
    }

    return result;
}
```

## Counting Substrings with At Most K Distinct

This counts the *number* of substrings (not the longest):

```java
public int countSubstringsAtMostK(String s, int k) {
    Map<Character, Integer> freq = new HashMap<>();
    int left = 0;
    int count = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        freq.put(c, freq.getOrDefault(c, 0) + 1);

        while (freq.size() > k) {
            char leftChar = s.charAt(left);
            freq.put(leftChar, freq.get(leftChar) - 1);
            if (freq.get(leftChar) == 0) freq.remove(leftChar);
            left++;
        }

        // All substrings ending at 'right' are valid
        count += right - left + 1;
    }

    return count;
}
```

The `right - left + 1` counts: `[left, right]`, `[left+1, right]`, ..., `[right, right]` — all substrings ending at `right`.

For example, with `s = "ece"` and `k = 2`:
- `right=0` ("e"): count += 1 → substrings ending at 0: "e"
- `right=1` ("ec"): count += 2 → substrings ending at 1: "ec", "c"
- `right=2` ("ece"): count += 3 → substrings ending at 2: "ece", "ce", "e"
- Total: 1+2+3 = 6

Let's verify: substrings with ≤2 distinct in "ece": "e", "c", "e", "ec", "ce", "ece" = 6 ✓

## Subarrays with Exactly K Distinct Integers

Same pattern, applied to arrays:

```java
public int subarraysWithKDistinct(int[] nums, int k) {
    return atMostKDistinct(nums, k) - atMostKDistinct(nums, k - 1);
}

private int atMostKDistinct(int[] nums, int k) {
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

## Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Each element added once | O(n) | O(k) for HashMap |
| Each element removed at most once | O(n) | O(1) for array |
| Total | O(n) | O(k) |

## Common Variations

| Problem | K Constraint | Notes |
|---------|-------------|-------|
| Longest with K distinct | At most K | Basic version |
| Longest with exactly K distinct | Exactly K | Use `atMost(K) - atMost(K-1)` |
| Count substrings with K distinct | Exactly K | Similar formula |
| Fruits into baskets | At most 2 | K=2 version |
| Longest with K repeating | Any char | Different problem (use frequency) |

## Fruits Into Baskets

This is the same problem with a story. Each basket can hold one type of fruit. You want to collect the maximum number of fruits with at most 2 types.

```java
public int totalFruit(int[] fruits) {
    return longestKDistinctArray(fruits, 2); // Custom version for int[]
    // Or just call with k=2
}
```

## Interview Tips

1. **The HashMap `size()` is your distinct count** — use it strategically
2. **Always remove keys when count hits 0** — otherwise `size()` is wrong
3. **Expand-first, then shrink** — the standard variable window flow
4. **"At most K" is easier than "exactly K"** — use the subtraction trick
5. **Edge cases**: k=0 (return 0), k larger than distinct count (return whole string)

## Common Mistakes

1. **Not removing from map** when count hits 0 — `size()` stays inflated
2. **Using `freq.size() > k` instead of `>=`** — "at most K" means ≤ K, so shrink when > K
3. **Forgetting to update `maxLen` in the right place** — update after shrinking, inside the right loop
4. **Using `<=` in the while condition** — would shrink unnecessarily

The "at most K distinct" pattern is the foundation for many harder problems. Once you understand this, you can handle "exactly K" (via subtraction) and "count subarrays with K distinct" (via the `right - left + 1` trick).
