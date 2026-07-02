# Subsequence Patterns

## Subsequence vs Substring vs Subset

| Concept | Definition | Count for string of length n |
|---|---|---|
| **Subarray/Substring** | Contiguous elements | O(n²) — n*(n+1)/2 |
| **Subsequence** | Not necessarily contiguous, order preserved | 2ⁿ (each element taken or skipped) |
| **Subset** | Any selection, order doesn't matter | 2ⁿ (same count as subsequences for arrays) |

### Key Differences

```
String: "abc"

Substrings (contiguous):
  "a", "ab", "abc", "b", "bc", "c" → 6

Subsequences (order preserved, can skip):
  "", "a", "b", "c", "ab", "ac", "bc", "abc" → 8

Subsets of {a,b,c}:
  {}, {a}, {b}, {c}, {a,b}, {a,c}, {b,c}, {a,b,c} → 8
```

**For arrays of distinct elements**: subsequences (preserving order) and subsets are essentially equivalent because we can define the canonical order as the array order.

**For strings**: subsequences preserve character order, which matters for pattern matching.

---

## Generate All Subsequences of a String

```java
public List<String> generateSubsequences(String s) {
    List<String> result = new ArrayList<>();
    backtrack(s, 0, new StringBuilder(), result);
    return result;
}

private void backtrack(String s, int index,
                       StringBuilder current,
                       List<String> result) {
    if (index == s.length()) {
        result.add(current.toString());
        return;
    }

    // Option 1: EXCLUDE current character
    backtrack(s, index + 1, current, result);

    // Option 2: INCLUDE current character
    current.append(s.charAt(index));
    backtrack(s, index + 1, current, result);

    // Backtrack
    current.deleteCharAt(current.length() - 1);
}
```

### Using For-loop Pattern (Iterative)

```java
public List<String> generateSubsequences(String s) {
    List<String> result = new ArrayList<>();
    result.add(""); // empty subsequence

    for (char c : s.toCharArray()) {
        int size = result.size();
        for (int i = 0; i < size; i++) {
            result.add(result.get(i) + c);
        }
    }

    return result;
}
```

---

## Count Subsequences with Sum K

### Problem: Count subsequences of array whose sum equals K

```java
public int countSubsequencesWithSumK(int[] nums, int K) {
    return count(nums, 0, 0, K);
}

private int count(int[] nums, int index, int currentSum, int K) {
    if (index == nums.length) {
        return currentSum == K ? 1 : 0;
    }

    // Exclude current element
    int exclude = count(nums, index + 1, currentSum, K);

    // Include current element
    int include = count(nums, index + 1, currentSum + nums[index], K);

    return exclude + include;
}
```

### Efficient Version with Memoization (when K is small)

```java
public int countSubsequencesWithSumK(int[] nums, int K) {
    int n = nums.length;
    int[][] memo = new int[n + 1][K + 1];
    for (int[] row : memo) Arrays.fill(row, -1);
    return count(nums, 0, 0, K, memo);
}

private int count(int[] nums, int index, int currentSum, int K, int[][] memo) {
    if (currentSum > K) return 0;
    if (index == nums.length) {
        return currentSum == K ? 1 : 0;
    }
    if (memo[index][currentSum] != -1) {
        return memo[index][currentSum];
    }

    int exclude = count(nums, index + 1, currentSum, K, memo);
    int include = count(nums, index + 1, currentSum + nums[index], K, memo);

    memo[index][currentSum] = exclude + include;
    return memo[index][currentSum];
}
```

### DP Solution (Bottom-Up)

```java
public int countSubsequencesWithSumK(int[] nums, int K) {
    int n = nums.length;
    int[][] dp = new int[n + 1][K + 1];

    // Base case: sum = 0 with any number of elements = 1 (empty subsequence)
    for (int i = 0; i <= n; i++) {
        dp[i][0] = 1;
    }

    for (int i = 1; i <= n; i++) {
        for (int sum = 0; sum <= K; sum++) {
            // Exclude current element
            dp[i][sum] = dp[i - 1][sum];
            // Include current element (if possible)
            if (sum >= nums[i - 1]) {
                dp[i][sum] += dp[i - 1][sum - nums[i - 1]];
            }
        }
    }

    return dp[n][K];
}
```

### Print Subsequences with Sum K

```java
public void printSubsequencesWithSumK(int[] nums, int K) {
    print(nums, 0, K, 0, new ArrayList<>());
}

private void print(int[] nums, int index, int K, int sumSoFar,
                   List<Integer> current) {
    if (index == nums.length) {
        if (sumSoFar == K) {
            System.out.println(current);
        }
        return;
    }

    // Exclude
    print(nums, index + 1, K, sumSoFar, current);

    // Include
    current.add(nums[index]);
    print(nums, index + 1, K, sumSoFar + nums[index], current);
    current.remove(current.size() - 1);
}
```

### Count Subsequences with Sum = K (using subset-sum DP)

This becomes the classic subset-sum problem. See Dynamic Programming notes for more details.

---

## Subsequence Pattern Matching

### Problem: Given two strings s and p, check if p is a subsequence of s

```java
public boolean isSubsequence(String s, String t) {
    int si = 0, ti = 0;
    while (si < s.length() && ti < t.length()) {
        if (s.charAt(si) == t.charAt(ti)) {
            si++;
        }
        ti++;
    }
    return si == s.length();
}
```

### Count Distinct Subsequences of S that Equal T

This is a classic DP problem (see DP on Strings section), but here's the backtracking approach:

```java
// Naive backtracking — works for small strings
public int numDistinct(String s, String t) {
    return count(s, t, 0, 0);
}

private int count(String s, String t, int si, int ti) {
    if (ti == t.length()) return 1;  // matched all of t
    if (si == s.length()) return 0;  // ran out of s

    int result = 0;
    // Try skipping s[si] and keep trying to match from si+1
    result += count(s, t, si + 1, ti);

    // If characters match, try matching with both advancing
    if (s.charAt(si) == t.charAt(ti)) {
        result += count(s, t, si + 1, ti + 1);
    }

    return result;
}
```

### Print All Strings of S that Contain P as Subsequence

```java
public List<String> stringsContainingSubsequence(String s, String p) {
    List<String> result = new ArrayList<>();
    backtrack(s, p, 0, 0, new StringBuilder(), result);
    return result;
}

private void backtrack(String s, String p, int si, int pi,
                       StringBuilder current, List<String> result) {
    if (si == s.length()) {
        if (pi == p.length()) {
            result.add(current.toString());
        }
        return;
    }

    int len = current.length();

    // Option 1: Skip s[si]
    backtrack(s, p, si + 1, pi, current, result);

    // Option 2: Take s[si]
    current.append(s.charAt(si));

    // Check if it matches expected character from p
    if (pi < p.length() && s.charAt(si) == p.charAt(pi)) {
        // Matching p
        backtrack(s, p, si + 1, pi + 1, current, result);
    } else {
        // Not matching p — continue trying
        backtrack(s, p, si + 1, pi, current, result);
    }

    current.setLength(len);
}
```

### Longest Common Subsequence (LCS) — Brute Force

```java
// Naive backtracking — O(2^(m+n))
public int lcsLength(String s1, String s2) {
    return lcs(s1, s2, 0, 0);
}

private int lcs(String s1, String s2, int i, int j) {
    if (i == s1.length() || j == s2.length()) return 0;

    if (s1.charAt(i) == s2.charAt(j)) {
        return 1 + lcs(s1, s2, i + 1, j + 1);
    } else {
        return Math.max(lcs(s1, s2, i + 1, j),
                        lcs(s1, s2, i, j + 1));
    }
}
```

This is O(2^(m+n)) without memoization. With memoization, it becomes O(m*n) — the standard DP solution.

---

## Common Subsequence Problems

| Problem | Approach | Complexity |
|---|---|---|
| Check if p is subsequence of s | Two pointers | O(m + n) |
| Count distinct subsequences of S = T | DP | O(m * n) |
| Longest Common Subsequence | DP | O(m * n) |
| Number of subsequences with sum K | DP (subset sum) | O(n * K) |
| Generate all subsequences | Backtracking | O(n * 2ⁿ) |
| Shortest Common Supersequence | DP + backtracking | O(m * n) |

## Key Patterns

1. **Two-pointer** for checking subsequence: O(m+n), no extra space
2. **Backtracking** for generating/listing: O(2ⁿ), needs exponential time
3. **DP** for counting/optimal: O(m*n), uses table
4. **DP + generating** for printing SCS or LCS: backtrack through DP table

## Practical Tip

In interviews, if the problem says "subsequence" and asks about **existence, count, or optimal value**, it's almost always a DP problem. If it asks to **list/generate all** subsequences, it's backtracking.
