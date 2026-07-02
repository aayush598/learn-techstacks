# Regular Expression Matching

**Problem**: Implement regular expression matching with support for:
- `.` matches any single character
- `*` matches zero or more of the **preceding element**

**Example**: `s = "aab", p = "c*a*b"` → true (c is zero times, a is two times, b is one time)

---

## Recurrence

```
dp[i][j] = true if s[0..i-1] matches p[0..j-1]

If p[j-1] != '*':
  dp[i][j] = dp[i-1][j-1] if p[j-1] == '.' or s[i-1] == p[j-1]

If p[j-1] == '*':
  // * means zero or more of p[j-2]
  
  // Zero occurrences: ignore p[j-2] and p[j-1]
  dp[i][j] = dp[i][j-2]
  
  // One or more occurrences: if p[j-2] matches s[i-1]
  if (p[j-2] == '.' || p[j-2] == s[i-1]):
      dp[i][j] = dp[i][j] || dp[i-1][j]
```

---

## Bottom-Up DP

```java
public boolean isMatch(String s, String p) {
    int m = s.length(), n = p.length();
    boolean[][] dp = new boolean[m + 1][n + 1];
    dp[0][0] = true;

    // Initialize: pattern like "a*b*" can match empty string
    for (int j = 2; j <= n; j++) {
        if (p.charAt(j - 1) == '*') {
            dp[0][j] = dp[0][j - 2];
        }
    }

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            char sc = s.charAt(i - 1);
            char pc = p.charAt(j - 1);

            if (pc == '.' || pc == sc) {
                dp[i][j] = dp[i - 1][j - 1];
            } else if (pc == '*') {
                // Zero occurrences of p[j-2]
                dp[i][j] = dp[i][j - 2];

                // One or more occurrences (if p[j-2] matches s[i-1])
                char prev = p.charAt(j - 2);
                if (prev == '.' || prev == sc) {
                    dp[i][j] = dp[i][j] || dp[i - 1][j];
                }
            }
        }
    }

    return dp[m][n];
}
```

### Understanding * for Regex vs Wildcard

```
Wildcard (*):        Matches any sequence of chars
                     dp[i][j] = dp[i][j-1] (empty) || dp[i-1][j] (absorb)

Regex (a*):          Matches zero or more of preceeding 'a'
                     dp[i][j] = dp[i][j-2] (zero 'a's)
                              || (match ? dp[i-1][j] : false) (one more 'a')
```

### Trace for s="aab", p="c*a*b"

```
         ""   c    *    a    *    b
""   [  T,   F,   T,   F,   T,   F]
a    [  F,   F,   F,   T,   T,   F]
a    [  F,   F,   F,   F,   T,   F]
b    [  F,   F,   F,   F,   F,   T]
```

- `dp[0][2]`: "c*" matches "" → true (zero c's)
- `dp[0][4]`: "c*a*" matches "" → true (zero of both)
- `dp[1][2]`: "a" vs "c*" → dp[1][0] = false
- `dp[1][4]`: "a" vs "c*a*" → zero a's: dp[1][2] = F; one a: dp[0][4] && c matches a? No... wait, prev='a', sc='a': dp[1][4] = F || dp[0][4] = T
- `dp[2][4]`: "aa" vs "c*a*" → dp[2][2] = F; dp[1][4] = T → T
- `dp[3][5]`: "aab" vs "c*a*b" → 'b' matches 'b' → dp[2][4] = T

---

## Complexity

| Version | Time | Space |
|---|---|---|
| Full 2D DP | O(m*n) | O(m*n) |
| Space-optimized | O(m*n) | O(n) |

## Key Takeaways

1. **Regex * is NOT wildcard *** — regex * modifies the preceeding character
2. **Key insight for ***: `dp[i][j-2]` handles zero occurrences; `dp[i-1][j]` handles one more
3. **`.` is simpler than `?` in wildcard** — both match any single character
4. **Initialize dp[0][j]** for patterns like "a*b*c*" that match empty string
5. **The prev = p.charAt(j-2)** check is critical for determining if the starred element matches
