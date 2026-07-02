# Brute Force to Optimal: Step-by-Step Evolutions

## Table of Contents
1. Two Sum: O(n²) → O(n)
2. Maximum Subarray Sum: O(n³) → O(n²) → O(n)
3. Longest Substring Without Repeat: O(n³) → O(n²) → O(n)
4. 3Sum: O(n³) → O(n²)
5. Subarray Sum Equals K: O(n²) → O(n)
6. Longest Increasing Subsequence: O(2ⁿ) → O(n²) → O(n log n)
7. Minimum Window Substring: O(n³) → O(n²) → O(n)
8. Edit Distance: O(3ⁿ) → O(mn)

---

## 1. Two Sum: O(n²) → O(n)

**Problem:** Given array `nums` and integer `target`, return indices of two numbers that add to target.

### Step 1: Brute Force — O(n²)
```java
public int[] twoSum(int[] nums, int target) {
    for (int i = 0; i < nums.length; i++) {
        for (int j = i + 1; j < nums.length; j++) {
            if (nums[i] + nums[j] == target) {
                return new int[]{i, j};
            }
        }
    }
    return new int[]{-1, -1};
}
```

**Observation:** For each element at index `i`, we need to find `target - nums[i]`. Instead of scanning the rest of the array (O(n)), we can store previously seen elements in a HashMap for O(1) lookup.

### Step 2: HashMap — O(n)
```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[]{map.get(complement), i};
        }
        map.put(nums[i], i);
    }
    return new int[]{-1, -1};
}
```

**Optimization key:** Trade space for time. O(1) lookup replaces O(n) inner loop.

---

## 2. Max Subarray Sum: O(n³) → O(n²) → O(n)

**Problem:** Find contiguous subarray with maximum sum (Kadane's algorithm).

### Step 1: Brute Force — O(n³)
```java
public int maxSubArray(int[] nums) {
    int n = nums.length, max = Integer.MIN_VALUE;
    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            int sum = 0;
            for (int k = i; k <= j; k++) sum += nums[k];
            max = Math.max(max, sum);
        }
    }
    return max;
}
```

**Observation:** Computing sum[i..j] from scratch for each (i,j) is wasteful. The sum of subarray i..j+1 = sum[i..j] + nums[j+1].

### Step 2: Improved Brute Force — O(n²)
```java
public int maxSubArray(int[] nums) {
    int n = nums.length, max = Integer.MIN_VALUE;
    for (int i = 0; i < n; i++) {
        int sum = 0;
        for (int j = i; j < n; j++) {
            sum += nums[j]; // incremental sum
            max = Math.max(max, sum);
        }
    }
    return max;
}
```

**Observation:** When sum so far becomes negative, it never helps to include it in any future subarray. Starting fresh from current element is always better.

### Step 3: Kadane's Algorithm — O(n)
```java
public int maxSubArray(int[] nums) {
    int maxEndingHere = nums[0];
    int maxSoFar = nums[0];
    for (int i = 1; i < nums.length; i++) {
        maxEndingHere = Math.max(nums[i], maxEndingHere + nums[i]);
        maxSoFar = Math.max(maxSoFar, maxEndingHere);
    }
    return maxSoFar;
}
```

**Optimization key:** If maxEndingHere becomes negative, discard it (reset to current element). This is a DP reduction with O(1) space.

---

## 3. Longest Substring Without Repeating: O(n³) → O(n²) → O(n)

**Problem:** Find longest substring without repeating characters.

### Step 1: Brute Force — O(n³)
```java
public int lengthOfLongestSubstring(String s) {
    int n = s.length(), maxLen = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            if (allUnique(s, i, j)) {
                maxLen = Math.max(maxLen, j - i + 1);
            }
        }
    }
    return maxLen;
}
boolean allUnique(String s, int start, int end) {
    Set<Character> set = new HashSet<>();
    for (int i = start; i <= end; i++) {
        if (set.contains(s.charAt(i))) return false;
        set.add(s.charAt(i));
    }
    return true;
}
```

### Step 2: Sliding Window with Set — O(n²) worst, O(2n) average
```java
public int lengthOfLongestSubstring(String s) {
    int n = s.length(), maxLen = 0;
    Set<Character> set = new HashSet<>();
    int left = 0;
    for (int right = 0; right < n; right++) {
        while (set.contains(s.charAt(right))) {
            set.remove(s.charAt(left));
            left++;
        }
        set.add(s.charAt(right));
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

**Observation:** Instead of scanning each substring from scratch, maintain a running window. When we see a duplicate, remove characters from the left until the duplicate is gone.

### Step 3: Optimized Sliding Window — O(n)
```java
public int lengthOfLongestSubstring(String s) {
    int[] index = new int[128]; // stores next index for each char
    int maxLen = 0, left = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        left = Math.max(left, index[c]); // jump left past any previous occurrence
        maxLen = Math.max(maxLen, right - left + 1);
        index[c] = right + 1; // store next valid starting position
    }
    return maxLen;
}
```

**Optimization key:** Instead of incrementally moving left (which can take O(n) per iteration), jump directly to the correct position using stored indices.

---

## 4. 3Sum: O(n³) → O(n²)

**Problem:** Find all unique triplets (i, j, k) where nums[i] + nums[j] + nums[k] = 0.

### Step 1: Brute Force — O(n³)
```java
public List<List<Integer>> threeSum(int[] nums) {
    Set<List<Integer>> result = new HashSet<>(); // avoid duplicates
    for (int i = 0; i < nums.length; i++) {
        for (int j = i + 1; j < nums.length; j++) {
            for (int k = j + 1; k < nums.length; k++) {
                if (nums[i] + nums[j] + nums[k] == 0) {
                    List<Integer> triplet = Arrays.asList(nums[i], nums[j], nums[k]);
                    Collections.sort(triplet);
                    result.add(triplet);
                }
            }
        }
    }
    return new ArrayList<>(result);
}
```

**Observation:** For each element, the remaining two-sum problem can be solved with two pointers in O(n) after sorting. Sorting enables duplicate skipping.

### Step 2: Sort + Two Pointers — O(n²)
```java
public List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    for (int i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue; // skip duplicates
        int left = i + 1, right = nums.length - 1;
        while (left < right) {
            int sum = nums[i] + nums[left] + nums[right];
            if (sum == 0) {
                result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                while (left < right && nums[left] == nums[left + 1]) left++;
                while (left < right && nums[right] == nums[right - 1]) right--;
                left++; right--;
            } else if (sum < 0) {
                left++;
            } else {
                right--;
            }
        }
    }
    return result;
}
```

**Optimization key:** Sorting (O(n log n)) + two pointers (O(n)) per element gives O(n²). Duplicate skipping avoids HashSet overhead.

---

## 5. Subarray Sum Equals K: O(n²) → O(n)

**Problem:** Count subarrays where sum = k.

### Step 1: Brute Force — O(n²)
```java
public int subarraySum(int[] nums, int k) {
    int count = 0;
    for (int i = 0; i < nums.length; i++) {
        int sum = 0;
        for (int j = i; j < nums.length; j++) {
            sum += nums[j];
            if (sum == k) count++;
        }
    }
    return count;
}
```

**Observation:** sum(i..j) = prefixSum[j+1] - prefixSum[i]. If we track prefix sums in a HashMap, we can find how many previous prefix sums equal current prefix sum - k.

### Step 2: Prefix Sum + HashMap — O(n)
```java
public int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> prefixCount = new HashMap<>();
    prefixCount.put(0, 1); // empty prefix has sum 0
    int sum = 0, count = 0;
    for (int num : nums) {
        sum += num;
        // If there exists prefix with sum = sum - k,
        // then subarray from that prefix to here has sum = k
        count += prefixCount.getOrDefault(sum - k, 0);
        prefixCount.put(sum, prefixCount.getOrDefault(sum, 0) + 1);
    }
    return count;
}
```

**Optimization key:** Replace O(n) inner loop with O(1) HashMap lookup by leveraging prefix sums.

---

## 6. LIS: O(2ⁿ) → O(n²) → O(n log n)

**Problem:** Find length of longest strictly increasing subsequence.

### Step 1: Brute Force — O(2ⁿ)
```java
public int lengthOfLIS(int[] nums) {
    return dfs(nums, Integer.MIN_VALUE, 0);
}
int dfs(int[] nums, int prev, int index) {
    if (index == nums.length) return 0;
    int take = 0;
    if (nums[index] > prev) {
        take = 1 + dfs(nums, nums[index], index + 1);
    }
    int skip = dfs(nums, prev, index + 1);
    return Math.max(take, skip);
}
```

**Observation:** At each step, we either take or skip. 2 choices per element → O(2ⁿ). Many overlapping subproblems (same (index, prevValue) repeated).

### Step 2: DP — O(n²)
```java
public int lengthOfLIS(int[] nums) {
    int n = nums.length, maxLen = 1;
    int[] dp = new int[n];
    Arrays.fill(dp, 1);
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i]) {
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
        maxLen = Math.max(maxLen, dp[i]);
    }
    return maxLen;
}
```

**Observation:** dp[i] = max(dp[i], dp[j] + 1) for all j < i where nums[j] < nums[i]. This is O(n²).

### Step 3: Patience Sorting — O(n log n)
```java
public int lengthOfLIS(int[] nums) {
    int[] tails = new int[nums.length];
    int size = 0; // length of LIS so far
    for (int num : nums) {
        int i = Arrays.binarySearch(tails, 0, size, num);
        if (i < 0) i = -(i + 1);
        tails[i] = num;
        if (i == size) size++;
    }
    return size;
}
```

**Key insight:** `tails[i]` = minimum possible last element of an increasing subsequence of length `i+1`. Binary search finds where to place the current number. This maintains the invariant that tails is always sorted.

---

## 7. Minimum Window Substring: O(n³) → O(n²) → O(n)

**Problem:** Find minimum window in s that contains all characters of t.

### Step 1: Brute Force — O(n³)
```java
public String minWindow(String s, String t) {
    int minLen = Integer.MAX_VALUE, start = 0;
    for (int i = 0; i < s.length(); i++) {
        for (int j = i; j < s.length(); j++) {
            String sub = s.substring(i, j + 1);
            if (containsAll(sub, t) && sub.length() < minLen) {
                minLen = sub.length();
                start = i;
            }
        }
    }
    return minLen == Integer.MAX_VALUE ? "" : s.substring(start, start + minLen);
}

boolean containsAll(String s, String t) {
    int[] need = new int[128];
    for (char c : t.toCharArray()) need[c]++;
    for (char c : s.toCharArray()) need[c]--;
    for (int n : need) if (n > 0) return false;
    return true;
}
```

**Observation:** O(n³) — O(n²) substrings, each checked in O(n). Too slow.

### Step 2: Sliding Window (Basic) — O(n²) worst
```java
public String minWindow(String s, String t) {
    int[] need = new int[128];
    for (char c : t.toCharArray()) need[c]++;
    int required = t.length();
    int minLen = Integer.MAX_VALUE, start = 0;

    for (int left = 0; left < s.length(); left++) {
        int[] copy = need.clone();
        int req = required;
        for (int right = left; right < s.length(); right++) {
            char c = s.charAt(right);
            if (copy[c] > 0) req--;
            copy[c]--;
            if (req == 0) {
                if (right - left + 1 < minLen) {
                    minLen = right - left + 1;
                    start = left;
                }
                break;
            }
        }
    }
    return minLen == Integer.MAX_VALUE ? "" : s.substring(start, start + minLen);
}
```

**Observation:** For each left, find the first right that satisfies. Still O(n²) because we start from scratch for each left.

### Step 3: Optimized Sliding Window — O(n)
```java
public String minWindow(String s, String t) {
    int[] need = new int[128];
    for (char c : t.toCharArray()) need[c]++;
    int required = t.length();
    int left = 0, minLen = Integer.MAX_VALUE, start = 0;

    for (int right = 0; right < s.length(); right++) {
        if (need[s.charAt(right)]-- > 0) required--;

        while (required == 0) {
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                start = left;
            }
            if (++need[s.charAt(left)] > 0) required++;
            left++;
        }
    }
    return minLen == Integer.MAX_VALUE ? "" : s.substring(start, start + minLen);
}
```

**Optimization key:** The window only moves forward. left and right each move O(n) total = O(n). The key insight is that we don't reset left when we find a new window — we continue from where we were.

---

## 8. Edit Distance: O(3ⁿ) → O(mn)

**Problem:** Minimum operations (insert, delete, replace) to convert word1 to word2.

### Step 1: Brute Force Recursion — O(3ⁿ)
```java
public int minDistance(String word1, String word2) {
    return edit(word1, word2, word1.length(), word2.length());
}
int edit(String w1, String w2, int i, int j) {
    if (i == 0) return j; // insert j chars
    if (j == 0) return i; // delete i chars
    if (w1.charAt(i - 1) == w2.charAt(j - 1)) {
        return edit(w1, w2, i - 1, j - 1); // chars match
    }
    return 1 + Math.min(
        edit(w1, w2, i, j - 1),     // insert
        Math.min(
            edit(w1, w2, i - 1, j), // delete
            edit(w1, w2, i - 1, j - 1) // replace
        )
    );
}
```

**Observation:** Each recursive call branches into 3 possibilities. Total calls = 3^(m+n) in worst case. Many overlapping subproblems: same (i, j) computed multiple times.

### Step 2: DP with Memoization — O(mn)
```java
public int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    Integer[][] memo = new Integer[m + 1][n + 1];
    return edit(word1, word2, m, n, memo);
}
int edit(String w1, String w2, int i, int j, Integer[][] memo) {
    if (i == 0) return j;
    if (j == 0) return i;
    if (memo[i][j] != null) return memo[i][j];
    if (w1.charAt(i - 1) == w2.charAt(j - 1)) {
        memo[i][j] = edit(w1, w2, i - 1, j - 1, memo);
    } else {
        memo[i][j] = 1 + Math.min(
            edit(w1, w2, i, j - 1, memo),
            Math.min(
                edit(w1, w2, i - 1, j, memo),
                edit(w1, w2, i - 1, j - 1, memo)
            )
        );
    }
    return memo[i][j];
}
```

**Observation:** Only m × n unique states. Each computed once → O(mn). But recursion still uses O(mn) stack space in worst case.

### Step 3: Bottom-up DP — O(mn) time, O(mn) space
```java
public int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], // replace
                               Math.min(dp[i - 1][j],     // delete
                                        dp[i][j - 1]));  // insert
            }
        }
    }
    return dp[m][n];
}
```

### Step 4: Space Optimized — O(mn) time, O(n) space
```java
public int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[] prev = new int[n + 1];
    for (int j = 0; j <= n; j++) prev[j] = j;
    for (int i = 1; i <= m; i++) {
        int[] curr = new int[n + 1];
        curr[0] = i;
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                curr[j] = prev[j - 1];
            } else {
                curr[j] = 1 + Math.min(prev[j - 1],
                               Math.min(prev[j], curr[j - 1]));
            }
        }
        prev = curr;
    }
    return prev[n];
}
```

**Optimization key:** We only need the previous row (prev) and current row (curr). This reduces space from O(mn) to O(n).

---

## Summary: Optimization Techniques Used

| Technique | Applied In | Savings |
|-----------|-----------|---------|
| HashMap for O(1) lookup | Two Sum, Subarray Sum | O(n) → O(1) inner loop |
| Negative prefix discard | Kadane's Algorithm | O(n²) → O(n) |
| Sliding window (no reset) | LSWR, Min Window | O(n²) → O(n) |
| Sort + two pointers | 3Sum | O(n³) → O(n²) |
| Prefix sum + HashMap | Subarray Sum = K | O(n²) → O(n) |
| Patience + binary search | LIS | O(n²) → O(n log n) |
| Memoization | Edit Distance | O(3ⁿ) → O(mn) |
| Space-optimized DP | Edit Distance | O(mn) → O(n) |
| Deque monotonic queue | Sliding Window Max | O(nk) → O(n) |
| Binary search on answer | Koko, Split Array | O(n×range) → O(n log range) |
