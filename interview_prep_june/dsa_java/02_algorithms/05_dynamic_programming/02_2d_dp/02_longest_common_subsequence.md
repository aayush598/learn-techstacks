# Longest Common Subsequence (LCS)

**Problem**: Given two strings, find the length of the longest subsequence that appears in both.

**Example**: `s1 = "abcde", s2 = "ace"` → 3 ("ace")

---

## Recurrence

```
dp[i][j] = LCS of s1[0..i-1] and s2[0..j-1]

dp[i][j] = dp[i-1][j-1] + 1          if s1[i-1] == s2[j-1]
         = max(dp[i-1][j], dp[i][j-1])  otherwise

Base: dp[0][j] = 0, dp[i][0] = 0 (empty string has LCS 0)
```

---

## Bottom-Up DP

```java
public int longestCommonSubsequence(String text1, String text2) {
    int m = text1.length(), n = text2.length();
    int[][] dp = new int[m + 1][n + 1];

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    return dp[m][n];
}
```

### Trace for s1="abcde", s2="ace"

```
        ""   a   c   e
""  [0,   0,  0,  0]
a   [0,   1,  1,  1]
b   [0,   1,  1,  1]
c   [0,   1,  2,  2]
d   [0,   1,  2,  2]
e   [0,   1,  2,  3]
```

**DP table walkthrough**:
- `dp[1][1]`: s1[0]='a' == s2[0]='a' → dp[0][0]+1 = 1
- `dp[2][2]`: s1[1]='b' != s2[1]='c' → max(dp[1][2]=1, dp[2][1]=1) = 1
- `dp[3][2]`: s1[2]='c' == s2[1]='c' → dp[2][1]+1 = 2
- `dp[5][3]`: s1[4]='e' == s2[2]='e' → dp[4][2]+1 = 3

---

## Print LCS

Use the DP table to backtrack and reconstruct the actual LCS:

```java
public String printLCS(String text1, String text2) {
    int m = text1.length(), n = text2.length();
    int[][] dp = new int[m + 1][n + 1];

    // Fill DP table
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    // Backtrack
    StringBuilder sb = new StringBuilder();
    int i = m, j = n;
    while (i > 0 && j > 0) {
        if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
            sb.append(text1.charAt(i - 1));
            i--;
            j--;
        } else if (dp[i - 1][j] > dp[i][j - 1]) {
            i--;
        } else {
            j--;
        }
    }

    return sb.reverse().toString();
}
```

---

## Space-Optimized (Length Only)

```java
public int longestCommonSubsequence(String text1, String text2) {
    int m = text1.length(), n = text2.length();
    int[] dp = new int[n + 1];

    for (int i = 1; i <= m; i++) {
        int prev = 0; // dp[i-1][j-1]
        for (int j = 1; j <= n; j++) {
            int temp = dp[j]; // dp[i-1][j] (before overwrite)
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                dp[j] = prev + 1;
            } else {
                dp[j] = Math.max(dp[j], dp[j - 1]);
            }
            prev = temp;
        }
    }

    return dp[n];
}
```

---

## Applications

### Shortest Common Supersequence (SCS)

**Problem**: Shortest string that has both s1 and s2 as subsequences.

```java
public String shortestCommonSupersequence(String str1, String str2) {
    String lcs = printLCS(str1, str2);
    StringBuilder sb = new StringBuilder();
    int i = 0, j = 0;

    for (char c : lcs.toCharArray()) {
        while (i < str1.length() && str1.charAt(i) != c) {
            sb.append(str1.charAt(i++));
        }
        while (j < str2.length() && str2.charAt(j) != c) {
            sb.append(str2.charAt(j++));
        }
        sb.append(c);
        i++;
        j++;
    }

    sb.append(str1.substring(i));
    sb.append(str2.substring(j));

    return sb.toString();
}

// Length of SCS = m + n - LCS
```

### Minimum Insertions to Make Palindrome

**Problem**: Minimum characters to insert to make a string a palindrome.

```java
public int minInsertions(String s) {
    String rev = new StringBuilder(s).reverse().toString();
    int lcs = longestCommonSubsequence(s, rev);
    return s.length() - lcs;
}
```

### Delete Operation for Two Strings

**Problem**: Minimum deletions to make two strings equal.

```java
public int minDistance(String word1, String word2) {
    int lcs = longestCommonSubsequence(word1, word2);
    return word1.length() - lcs + word2.length() - lcs;
}
```

### Longest Palindromic Subsequence

```java
public int longestPalindromeSubseq(String s) {
    String rev = new StringBuilder(s).reverse().toString();
    return longestCommonSubsequence(s, rev);
}
```

---

## Complexity

| Version | Time | Space |
|---|---|---|
| Full 2D DP | O(m*n) | O(m*n) |
| Space-optimized | O(m*n) | O(min(m,n)) |
| LCS print | O(m*n) | O(m*n) |

## Key Takeaways

1. **LCS is the foundational 2D DP problem** — mastering it unlocks edit distance, SCS, and palindrome problems
2. **Recurrence is intuitive**: match → extend LCS by 1; mismatch → carry forward the best
3. **Space optimization**: since dp[i] only needs dp[i-1] and dp[i][j-1], we can use 1D + prev variable
4. **Backtracking the DP table** = reconstructing the actual LCS
5. **Many palindrome problems** = LCS of string and its reverse
