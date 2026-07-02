# Interleaving String

**Problem**: Given strings s1, s2, and s3, check if s3 is formed by interleaving s1 and s2 while preserving the relative order of characters from each.

**Example**: `s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"` → true
- a a d b b c b c a c
- ^ ^ ^ ^ ^ ^ ^ ^
- s1: a a   c c
- s2:   d b b   a

---

## Recurrence

```
dp[i][j] = true if s3[0..i+j-1] is formed by interleaving s1[0..i-1] and s2[0..j-1]

dp[i][j] = (s1[i-1] == s3[i+j-1] && dp[i-1][j])
        || (s2[j-1] == s3[i+j-1] && dp[i][j-1])

Base:
  dp[0][0] = true
  dp[i][0] = s1[0..i-1] == s3[0..i-1]
  dp[0][j] = s2[0..j-1] == s3[0..j-1]
```

---

## Bottom-Up DP

```java
public boolean isInterleave(String s1, String s2, String s3) {
    int m = s1.length(), n = s2.length(), l = s3.length();
    if (m + n != l) return false;

    boolean[][] dp = new boolean[m + 1][n + 1];
    dp[0][0] = true;

    // s1 only
    for (int i = 1; i <= m; i++) {
        dp[i][0] = dp[i - 1][0] && s1.charAt(i - 1) == s3.charAt(i - 1);
    }

    // s2 only
    for (int j = 1; j <= n; j++) {
        dp[0][j] = dp[0][j - 1] && s2.charAt(j - 1) == s3.charAt(j - 1);
    }

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            int k = i + j - 1; // index in s3
            if (s1.charAt(i - 1) == s3.charAt(k)) {
                dp[i][j] = dp[i][j] || dp[i - 1][j];
            }
            if (s2.charAt(j - 1) == s3.charAt(k)) {
                dp[i][j] = dp[i][j] || dp[i][j - 1];
            }
        }
    }

    return dp[m][n];
}
```

### Trace for s1="aabcc", s2="dbbca", s3="aadbbcbcac"

```
      ""    d     b     b     c     a
""  [ T,   F,    F,    F,    F,    F ]
a   [ T,   F,    F,    F,    F,    F ]
a   [ T,   T,    T,    T,    T,    F ]
b   [ F,   T,    T,    T,    T,    F ]
c   [ F,   F,    T,    T,    T,    T ]
c   [ F,   F,    F,    T,    T,    T ]
```

The path from (0,0) to (5,5) traces a valid interleaving.

---

## Space-Optimized

```java
public boolean isInterleave(String s1, String s2, String s3) {
    int m = s1.length(), n = s2.length(), l = s3.length();
    if (m + n != l) return false;

    boolean[] dp = new boolean[n + 1];

    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= n; j++) {
            if (i == 0 && j == 0) {
                dp[j] = true;
            } else if (i == 0) {
                dp[j] = dp[j - 1] && s2.charAt(j - 1) == s3.charAt(j - 1);
            } else if (j == 0) {
                dp[j] = dp[j] && s1.charAt(i - 1) == s3.charAt(i - 1);
            } else {
                int k = i + j - 1;
                dp[j] = (dp[j] && s1.charAt(i - 1) == s3.charAt(k))
                      || (dp[j - 1] && s2.charAt(j - 1) == s3.charAt(k));
            }
        }
    }

    return dp[n];
}
```

---

## Complexity

| Version | Time | Space |
|---|---|---|
| Full 2D | O(m*n) | O(m*n) |
| 1D | O(m*n) | O(n) |

## Key Takeaways

1. **State**: dp[i][j] = can s3[0..i+j-1] be formed from s1[0..i-1] and s2[0..j-1]
2. **Two ways to extend**: take from s1 or take from s2
3. **The s3 index is always i+j-1** — the combined length
4. **Base cases**: check if s3 matches s1 alone or s2 alone
5. **Length check first**: if m + n ≠ l, return false immediately
