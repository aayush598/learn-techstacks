# Sliding Window Technique

## Core Concept

The sliding window technique maintains a **window** (contiguous segment) over a sequence and slides it to process all segments efficiently.

### Two flavors

1. **Fixed window size** — window moves one step at a time
2. **Variable window size** — window expands or shrinks based on conditions

**The superpower:** Instead of recomputing the entire window at each step (which would be O(n*k)), you update incrementally — removing the outgoing element and adding the incoming one. This gives O(n) instead of O(n*k).

## Fixed Size: Maximum Sum Subarray of Size K

```java
public static int maxSumSubarrayOfSizeK(int[] arr, int k) {
    int windowSum = 0;
    // Compute sum of first window
    for (int i = 0; i < k; i++) {
        windowSum += arr[i];
    }
    int maxSum = windowSum;

    // Slide the window
    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i] - arr[i - k]; // add new, remove old
        maxSum = Math.max(maxSum, windowSum);
    }
    return maxSum;
}
```

**Key operation:** `windowSum += arr[i] - arr[i - k]`. This is O(1) per slide instead of O(k).

## Fixed Size: First Negative in Every Window

```java
public static List<Integer> firstNegativeInWindow(int[] arr, int k) {
    List<Integer> result = new ArrayList<>();
    Deque<Integer> negatives = new ArrayDeque<>(); // store indices of negative numbers

    for (int i = 0; i < arr.length; i++) {
        // Add current element if negative
        if (arr[i] < 0) {
            negatives.addLast(i);
        }

        // Remove indices that are out of current window
        while (!negatives.isEmpty() && negatives.peekFirst() < i - k + 1) {
            negatives.pollFirst();
        }

        // Record result when window is fully formed
        if (i >= k - 1) {
            if (negatives.isEmpty()) {
                result.add(0); // or null depending on requirement
            } else {
                result.add(arr[negatives.peekFirst()]);
            }
        }
    }
    return result;
}
```

## Variable Size: Longest Substring Without Repeating Characters

```java
public static int lengthOfLongestSubstring(String s) {
    Set<Character> window = new HashSet<>();
    int left = 0, maxLen = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        // Shrink window until we can add c
        while (window.contains(c)) {
            window.remove(s.charAt(left));
            left++;
        }
        window.add(c);
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

**Optimized with HashMap (skip directly):**

```java
public static int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> lastSeen = new HashMap<>();
    int left = 0, maxLen = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        // If c was seen and is within current window, jump left past it
        if (lastSeen.containsKey(c) && lastSeen.get(c) >= left) {
            left = lastSeen.get(c) + 1;
        }
        lastSeen.put(c, right);
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

Instead of sliding left one step at a time, we directly jump to `lastSeen + 1`. This is still O(n) but with fewer iterations.

## Variable Size: Minimum Window Substring

**Problem:** Find the smallest substring of s that contains all characters of t.

```java
public static String minWindow(String s, String t) {
    Map<Character, Integer> required = new HashMap<>();
    for (char c : t.toCharArray()) {
        required.merge(c, 1, Integer::sum);
    }

    int left = 0, minLeft = 0, minLen = Integer.MAX_VALUE;
    int requiredCount = required.size(); // distinct chars needed
    int formed = 0; // distinct chars satisfied
    Map<Character, Integer> windowCounts = new HashMap<>();

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        windowCounts.merge(c, 1, Integer::sum);

        if (required.containsKey(c) && windowCounts.get(c).equals(required.get(c))) {
            formed++;
        }

        // Try to shrink window from left
        while (formed == requiredCount && left <= right) {
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                minLeft = left;
            }

            char leftChar = s.charAt(left);
            windowCounts.put(leftChar, windowCounts.get(leftChar) - 1);
            if (required.containsKey(leftChar) && windowCounts.get(leftChar) < required.get(leftChar)) {
                formed--;
            }
            left++;
        }
    }

    return minLen == Integer.MAX_VALUE ? "" : s.substring(minLeft, minLeft + minLen);
}
```

**Time:** O(m + n) — each character visited at most twice (once by right, once by left).

## Longest Subarray with Sum K (Positives Only)

```java
public static int longestSubarraySumK(int[] arr, int k) {
    int left = 0, sum = 0, maxLen = 0;
    for (int right = 0; right < arr.length; right++) {
        sum += arr[right];
        // Shrink while sum exceeds k
        while (sum > k && left <= right) {
            sum -= arr[left];
            left++;
        }
        if (sum == k) {
            maxLen = Math.max(maxLen, right - left + 1);
        }
    }
    return maxLen;
}
```

**Note:** This only works with **positive integers**. For arrays with negatives, use the prefix sum + HashMap approach.

## Longest Subarray with At Most K Distinct Characters

```java
public static int longestSubarrayKDistinct(int[] arr, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    int left = 0, maxLen = 0;

    for (int right = 0; right < arr.length; right++) {
        freq.merge(arr[right], 1, Integer::sum);

        while (freq.size() > k) {
            freq.put(arr[left], freq.get(arr[left]) - 1);
            if (freq.get(arr[left]) == 0) {
                freq.remove(arr[left]);
            }
            left++;
        }
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

## Sliding Window Maximum (with Deque)

**Problem:** Find the maximum in each sliding window of size k.

```java
public static int[] maxSlidingWindow(int[] arr, int k) {
    if (arr == null || arr.length == 0) return new int[0];

    int[] result = new int[arr.length - k + 1];
    Deque<Integer> deque = new ArrayDeque<>(); // store indices

    for (int i = 0; i < arr.length; i++) {
        // Remove elements out of current window (from front)
        while (!deque.isEmpty() && deque.peekFirst() < i - k + 1) {
            deque.pollFirst();
        }

        // Remove smaller elements from back (they'll never be max)
        while (!deque.isEmpty() && arr[deque.peekLast()] < arr[i]) {
            deque.pollLast();
        }

        deque.addLast(i);

        // Record max when window is formed
        if (i >= k - 1) {
            result[i - k + 1] = arr[deque.peekFirst()];
        }
    }
    return result;
}
```

### Why the deque works

The deque maintains **indices** in decreasing order of their values. The front is always the maximum in the current window. When a new element comes:
1. Remove indices that left the window
2. Remove indices whose values are ≤ the new element (they'll never be max again while this new element is in the window)
3. Add the new element

This is O(n) — each index is added and removed at most once.

## Count Subarrays with Condition (At Most K Odd Numbers)

```java
public static int countSubarraysWithAtMostKOdd(int[] arr, int k) {
    int left = 0, oddCount = 0, count = 0;
    for (int right = 0; right < arr.length; right++) {
        if (arr[right] % 2 != 0) oddCount++;

        while (oddCount > k) {
            if (arr[left] % 2 != 0) oddCount--;
            left++;
        }
        // All subarrays ending at 'right' starting from 'left' to 'right' are valid
        count += right - left + 1;
    }
    return count;
}
```

### The `count += right - left + 1` pattern

This is subtle but powerful. When the window `[left, right]` satisfies the condition, every subarray ending at `right` that starts at any position from `left` to `right` also satisfies the condition. There are `right - left + 1` such subarrays.

## Sliding Window Template

Here's a general template for variable-size sliding window:

```java
public int slidingWindow(int[] arr, int k) {
    int left = 0;
    int result = 0; // or min/max depending on problem
    // window state: sum, set, map, etc.

    for (int right = 0; right < arr.length; right++) {
        // Add arr[right] to window state

        // Shrink condition: while window is INVALID
        while (/* window violates condition */) {
            // Remove arr[left] from window state
            left++;
        }

        // Window is now valid — update result
        // result = Math.max(result, right - left + 1); // for length
        // result += right - left + 1; // for count
    }
    return result;
}
```

## When to Use Sliding Window

1. **Contiguous subarray/substring problems**
2. **Fixed window size** — sum, average, max/min in window
3. **Variable window with condition** — "longest subarray where condition holds"
4. **Two-pointer with window expansion/contraction**

## Practice Problems

| Problem | LeetCode | Type |
|---------|----------|------|
| Maximum Average Subarray I | 643 | Fixed |
| Sliding Window Maximum | 239 | Fixed + Deque |
| Longest Substring Without Repeating | 3 | Variable |
| Minimum Window Substring | 76 | Variable |
| Longest Subarray with K Distinct | 340 | Variable |
| Subarrays with K Different Integers | 992 | Count |
| Max Consecutive Ones III | 1004 | Variable |
