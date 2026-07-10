# Palindrome Patterns

Palindromes show up everywhere in interviews. From simple two-pointer checks to complex DP problems, these patterns form a complete toolkit.

---

## 1. Valid Palindrome (Two Pointers)

**Problem:** Determine if a string is a palindrome, considering only alphanumeric characters and ignoring cases.

**Example:** `"A man, a plan, a canal: Panama"` → true

```java
public static boolean isPalindrome(String s) {
    int left = 0;
    int right = s.length() - 1;

    while (left < right) {
        // Skip non-alphanumeric characters
        while (left < right && !Character.isLetterOrDigit(s.charAt(left))) {
            left++;
        }
        while (left < right && !Character.isLetterOrDigit(s.charAt(right))) {
            right--;
        }

        if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))) {
            return false;
        }

        left++;
        right--;
    }
    return true;
}
```

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

**Key detail:** We use `Character.isLetterOrDigit()` to skip spaces, punctuation, and special characters. We normalize with `toLowerCase()` for case-insensitive comparison.

---

## 2. Valid Palindrome II (Delete at Most One Char)

**Problem:** Can the string become a palindrome after deleting at most one character?

**Example:** `"abca"` → true (delete 'b'), `"abc"` → false

```java
public static boolean validPalindrome(String s) {
    return helper(s, 0, s.length() - 1, 0);
}

private static boolean helper(String s, int left, int right, int deletions) {
    if (deletions > 1) return false;

    while (left < right) {
        if (s.charAt(left) != s.charAt(right)) {
            // Try deleting left char OR deleting right char
            return helper(s, left + 1, right, deletions + 1)
                || helper(s, left, right - 1, deletions + 1);
        }
        left++;
        right--;
    }
    return true;
}
```

### Cleaner Iterative Version (No Recursion)

```java
public static boolean validPalindromeII(String s) {
    int left = 0, right = s.length() - 1;

    while (left < right) {
        if (s.charAt(left) != s.charAt(right)) {
            return isPalin(s, left + 1, right) || isPalin(s, left, right - 1);
        }
        left++;
        right--;
    }
    return true;
}

private static boolean isPalin(String s, int left, int right) {
    while (left < right) {
        if (s.charAt(left++) != s.charAt(right--)) return false;
    }
    return true;
}
```

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## 3. Longest Palindromic Substring (Expand Around Center)

**Problem:** Find the longest palindromic substring in a given string.

**Example:** `"babad"` → `"bab"` or `"aba"`

### Approach: Expand Around Center — O(n²)

Every single character and every pair of adjacent characters can be the center of a palindrome. We try expanding from each center.

```java
public static String longestPalindrome(String s) {
    if (s == null || s.length() < 2) return s;

    String longest = "";

    for (int i = 0; i < s.length(); i++) {
        // Odd-length palindromes (single center)
        String odd = expand(s, i, i);
        // Even-length palindromes (two centers)
        String even = expand(s, i, i + 1);

        if (odd.length() > longest.length()) longest = odd;
        if (even.length() > longest.length()) longest = even;
    }

    return longest;
}

private static String expand(String s, int left, int right) {
    while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
        left--;
        right++;
    }
    // When the loop ends, left and right have gone one step too far
    return s.substring(left + 1, right);
}
```

**Why two expansions per center?**
- Odd-length: center is a single character, e.g., `"aba"` centers at index 1
- Even-length: center is between two characters, e.g., `"abba"` centers between indices 1 and 2

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n²) |
| Space  | O(1)  | (ignoring output string) |

---

## 4. Count Palindromic Substrings

**Problem:** Count how many palindromic substrings exist in a string.

**Example:** `"aaa"` → 6 (`"a"`, `"a"`, `"a"`, `"aa"`, `"aa"`, `"aaa"`)

```java
public static int countPalindromicSubstrings(String s) {
    int count = 0;

    for (int i = 0; i < s.length(); i++) {
        // Odd-length palindromes
        count += expandCount(s, i, i);
        // Even-length palindromes
        count += expandCount(s, i, i + 1);
    }

    return count;
}

private static int expandCount(String s, int left, int right) {
    int count = 0;
    while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
        count++;
        left--;
        right++;
    }
    return count;
}
```

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n²) |
| Space  | O(1)  |

---

## 5. Longest Palindromic Subsequence (DP)

**Problem:** Find the length of the longest subsequence that is a palindrome.

**Example:** `"bbbab"` → 4 (`"bbbb"`)

### Approach: DP — O(n²)

Let `dp[i][j]` = length of longest palindromic subsequence in `s[i..j]`.

```java
public static int longestPalindromicSubsequence(String s) {
    int n = s.length();
    int[][] dp = new int[n][n];

    // Every single character is a palindrome of length 1
    for (int i = 0; i < n; i++) {
        dp[i][i] = 1;
    }

    // Fill for increasing lengths
    for (int len = 2; len <= n; len++) {
        for (int i = 0; i <= n - len; i++) {
            int j = i + len - 1;

            if (s.charAt(i) == s.charAt(j)) {
                dp[i][j] = dp[i + 1][j - 1] + 2;
            } else {
                dp[i][j] = Math.max(dp[i + 1][j], dp[i][j - 1]);
            }
        }
    }

    return dp[0][n - 1];
}
```

### Alternative: LCS with Reverse

The longest palindromic subsequence is the LCS of the string and its reverse.

```java
public static int lpsUsingLCS(String s) {
    String rev = new StringBuilder(s).reverse().toString();
    return lcs(s, rev);
}

private static int lcs(String s1, String s2) {
    int m = s1.length(), n = s2.length();
    int[][] dp = new int[m + 1][n + 1];

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    return dp[m][n];
}
```

### Complexity

| Approach | Time | Space |
|----------|------|-------|
| Direct DP | O(n²) | O(n²) |
| LCS with reverse | O(n²) | O(n²) |

**Key difference from "substring":** A subsequence does NOT need to be contiguous. `"ace"` is a subsequence of `"abcde"`.

---

## 6. Break a Palindrome

**Problem:** Given a palindromic string, replace exactly one character to make it non-palindromic. Return the result, or empty string if impossible.

**Example:** `"abccba"` → `"aaccba"`, `"a"` → `""`

```java
public static String breakPalindrome(String palindrome) {
    int n = palindrome.length();
    if (n == 1) return ""; // single char can't become non-palindrome

    char[] chars = palindrome.toCharArray();

    // Change the first non-'a' character to 'a'
    for (int i = 0; i < n / 2; i++) {
        if (chars[i] != 'a') {
            chars[i] = 'a';
            return new String(chars);
        }
    }

    // All characters are 'a' — change the last one to 'b'
    chars[n - 1] = 'b';
    return new String(chars);
}
```

**Why only check first half?**
- Changing a character in the first half breaks the palindrome (we pick the first non-'a' to minimize the result)
- If the string is all 'a's, the only option is to change the last character to 'b'
- We only need to iterate through `n/2` positions because of palindrome symmetry

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(n)  | (for char array) |

---

## Test Cases

```java
public static void main(String[] args) {
    // Test 1: Valid Palindrome
    System.out.println(isPalindrome("A man, a plan, a canal: Panama")); // true
    System.out.println(isPalindrome("race a car"));                     // false

    // Test 2: Valid Palindrome II
    System.out.println(validPalindromeII("aba"));   // true
    System.out.println(validPalindromeII("abca"));  // true
    System.out.println(validPalindromeII("abc"));   // false

    // Test 3: Longest Palindromic Substring
    System.out.println(longestPalindrome("babad")); // "bab" or "aba"
    System.out.println(longestPalindrome("cbbd"));  // "bb"

    // Test 4: Count Palindromic Substrings
    System.out.println(countPalindromicSubstrings("aaa")); // 6
    System.out.println(countPalindromicSubstrings("abc")); // 3

    // Test 5: Longest Palindromic Subsequence
    System.out.println(longestPalindromicSubsequence("bbbab")); // 4
    System.out.println(longestPalindromicSubsequence("cbbd"));  // 2

    // Test 6: Break Palindrome
    System.out.println(breakPalindrome("abccba")); // "aaccba"
    System.out.println(breakPalindrome("a"));      // ""
    System.out.println(breakPalindrome("aaa"));    // "aab"
}
```

---

## Pattern Recognition Guide

| Problem Type | Key Technique |
|-------------|---------------|
| Is the string a palindrome? | Two pointers from both ends |
| Delete one char to make palindrome? | Two pointers + one skip tolerance |
| Longest palindromic substring? | Expand around center (odd + even) |
| Count palindromic substrings? | Expand around center, count each |
| Longest palindromic subsequence? | DP (or LCS with reverse) |
| Break a palindrome? | Greedy: change first non-'a' to 'a' |

---

## Substring vs. Subsequence — Don't Confuse Them!

| Term | Meaning | Example from "abcde" |
|------|---------|---------------------|
| Substring | Contiguous characters | `"bcd"`, `"abc"` |
| Subsequence | Non-contiguous, preserve order | `"ace"`, `"ae"` |

This distinction is critical. Longest palindromic **substring** uses expand-around-center. Longest palindromic **subsequence** uses DP.
