# Longest Palindromic Subsequence (LPS)

**Problem**: Given a string, find the length of the longest subsequence that is a palindrome.

**Example**: `s = "bbabcbcab"` → 7 ("babcbab" or "bbcabb")

---

## Approach 1: LCS of String and Its Reverse

LPS(s) = LCS(s, reverse(s))

```java
public int longestPalindromeSubseq(String s) {
    String rev = new StringBuilder(s).reverse().toString();
    return longestCommonSubsequence(s, rev);
}

private int longestCommonSubsequence(String s1, String s2) {
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

---

## Approach 2: Interval DP on Substring

Define: `dp[i][j]` = LPS of substring s[i..j] (inclusive)

```java
public int longestPalindromeSubseq(String s) {
    int n = s.length();
    int[][] dp = new int[n][n];

    // Every single character is a palindrome of length 1
    for (int i = 0; i < n; i++) {
        dp[i][i] = 1;
    }

    // Fill for increasing substring lengths
    for (int len = 2; len <= n; len++) {
        for (int i = 0; i + len - 1 < n; i++) {
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

### Trace for s = "bbbab"

```
Length 1: dp[0][0]=1, dp[1][1]=1, dp[2][2]=1, dp[3][3]=1, dp[4][4]=1

Length 2:
  "bb": s[0]=='b'==s[1] → dp[0][1]=dp[1][0]+2=0+2=2
  "bb": s[1]=='b'==s[2] → dp[1][2]=dp[2][1]+2=0+2=2
  "ba": s[2]!='a' → dp[2][3]=max(dp[3][3]=1, dp[2][2]=1)=1
  "ab": s[3]!='b' → dp[3][4]=max(dp[4][4]=1, dp[3][3]=1)=1

Length 3:
  "bbb": s[0]=='b'==s[2] → dp[0][2]=dp[1][1]+2=1+2=3
  "bba": s[1]!='a' → dp[1][3]=max(dp[2][3]=1, dp[1][2]=2)=2
  "bab": s[2]=='b'==s[4] → dp[2][4]=dp[3][3]+2=1+2=3

Length 4:
  "bbba": s[0]!='a' → dp[0][3]=max(dp[1][3]=2, dp[0][2]=3)=3
  "bbab": s[1]=='b'==s[4] → dp[1][4]=dp[2][3]+2=1+2=3

Length 5:
  "bbbab": s[0]!='b' → dp[0][4]=max(dp[1][4]=3, dp[0][3]=3)=3

Answer: 3 ("bbb" or "bb" or "bab")
```

### Why the Two Approaches Give Same Result

- LCS with reverse: finds characters that appear in both forward and backward order → palindrome
- Interval DP: directly reasons about palindromes by checking outer characters

---

## Reconstruct LPS

```java
public String printLongestPalindromeSubseq(String s) {
    int n = s.length();
    int[][] dp = new int[n][n];

    for (int i = 0; i < n; i++) dp[i][i] = 1;

    for (int len = 2; len <= n; len++) {
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            if (s.charAt(i) == s.charAt(j)) {
                dp[i][j] = dp[i + 1][j - 1] + 2;
            } else {
                dp[i][j] = Math.max(dp[i + 1][j], dp[i][j - 1]);
            }
        }
    }

    // Reconstruct
    StringBuilder sb = new StringBuilder();
    int i = 0, j = n - 1;

    while (i <= j) {
        if (i == j) {
            sb.append(s.charAt(i));
            break;
        }
        if (s.charAt(i) == s.charAt(j)) {
            sb.append(s.charAt(i));
            i++;
            j--;
        } else if (dp[i + 1][j] > dp[i][j - 1]) {
            i++;
        } else {
            j--;
        }
    }

    // The first half is in sb, add the reverse
    String firstHalf = sb.toString();
    String secondHalf = new StringBuilder(firstHalf).reverse().toString();
    if (s.charAt(i) == s.charAt(j) && i < j) {
        // middle character counted twice in firstHalf
        firstHalf = firstHalf.substring(0, firstHalf.length() - 1);
    }
    return firstHalf + secondHalf;
}
```

---

## Minimum Deletions to Make Palindrome

```java
public int minDeletions(String s) {
    return s.length() - longestPalindromeSubseq(s);
}
```

---

## Complexity

| Approach | Time | Space | Notes |
|---|---|---|---|
| LCS with reverse | O(n²) | O(n²) | Simpler, reuses LCS |
| Interval DP | O(n²) | O(n²) | More direct, easier to optimize space |

Space can be optimized to O(n) for length, but reconstruction needs O(n²).

## Key Pattern

The interval DP approach for LPS is:
```
dp[i][j] = dp[i+1][j-1] + 2   if s[i] == s[j]
         = max(dp[i+1][j], dp[i][j-1])  otherwise
```

This is the same pattern used in:
- Minimum insertions to make palindrome
- Longest palindromic substring (but substring, not subsequence)
- Palindrome partitioning (with modifications)
