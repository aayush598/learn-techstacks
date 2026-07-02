# LCS Pattern

## When to Use

Look for:
- "Compare two sequences/strings"
- "Minimum insertions/deletions to make equal"
- "Longest common..." between two strings
- "Edit distance" between strings

## Derivative Problems

| Problem | Relation to LCS |
|---|---|
| Shortest Common Supersequence | m + n - LCS |
| Min Deletions to Make Equal | (m - LCS) + (n - LCS) |
| Min Insertions to Make Palindrome | n - LCS(s, reverse(s)) |
| Longest Palindromic Subsequence | LCS(s, reverse(s)) |
| Delete Operation for Two Strings | (m - LCS) + (n - LCS) |

## Template

```java
int lcs(String s1, String s2) {
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

## Key Insight

> LCS DP table is the foundation for many string comparison problems. The recurrence captures the two choices: skip from s1 or skip from s2.
