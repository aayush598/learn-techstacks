# Wildcard Matching

**Problem**: Given a string s and a pattern p, implement wildcard pattern matching with support for:
- `?` matches any single character
- `*` matches any sequence of characters (including empty)

---

## Recurrence

```
dp[i][j] = true if s[0..i-1] matches p[0..j-1]

dp[i][j] = dp[i-1][j-1]                         if p[j-1] == '?' or s[i-1] == p[j-1]
         = dp[i-1][j] || dp[i][j-1]              if p[j-1] == '*'
         = false                                  otherwise

Base:
  dp[0][0] = true (empty string matches empty pattern)
  dp[0][j] = dp[0][j-1] && p[j-1] == '*' (pattern of only *s matches empty)
  dp[i][0] = false (non-empty string doesn't match empty pattern)
```

---

## Bottom-Up DP

```java
public boolean isMatch(String s, String p) {
    int m = s.length(), n = p.length();
    boolean[][] dp = new boolean[m + 1][n + 1];

    dp[0][0] = true;

    // Pattern consisting of only * can match empty string
    for (int j = 1; j <= n; j++) {
        if (p.charAt(j - 1) == '*') {
            dp[0][j] = dp[0][j - 1];
        }
    }

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            char sc = s.charAt(i - 1);
            char pc = p.charAt(j - 1);

            if (pc == '?' || sc == pc) {
                dp[i][j] = dp[i - 1][j - 1];
            } else if (pc == '*') {
                // * matches empty: dp[i][j-1]
                // * matches one char: dp[i-1][j]
                dp[i][j] = dp[i][j - 1] || dp[i - 1][j];
            }
        }
    }

    return dp[m][n];
}
```

### Understanding the * Transitions

```
* matches empty sequence:
  dp[i][j-1] → pattern without * matches string (discard *)

* matches at least one character:
  dp[i-1][j] → pattern with * matches string without last character
                (the * "absorbs" one character)

Combined: dp[i][j] = dp[i][j-1] (empty) || dp[i-1][j] (non-empty)
```

### Trace for s="adceb", p="*a*b"

```
dp table:
       ""  *   a   *   b
""  [ T,  T,  F,  F,  F]
a   [ F,  T,  T,  T,  F]
d   [ F,  T,  F,  T,  F]
c   [ F,  T,  F,  T,  F]
e   [ F,  T,  F,  T,  F]
b   [ F,  T,  F,  T,  T]
```

- `dp[0][1]`: "*" matches "" → true
- `dp[1][2]`: "a" matches "a" → dp[0][1] = true
- `dp[1][3]`: "a" matches "*" → dp[1][2] || dp[0][3] = true || false = true
- `dp[5][5]`: "b" matches "b" → dp[4][4] = true

---

## Space-Optimized

```java
public boolean isMatch(String s, String p) {
    int m = s.length(), n = p.length();
    boolean[] dp = new boolean[n + 1];
    dp[0] = true;

    for (int j = 1; j <= n; j++) {
        if (p.charAt(j - 1) == '*') dp[j] = dp[j - 1];
    }

    for (int i = 1; i <= m; i++) {
        boolean prev = dp[0]; // dp[i-1][j-1]
        dp[0] = false; // dp[i][0]

        for (int j = 1; j <= n; j++) {
            char sc = s.charAt(i - 1);
            char pc = p.charAt(j - 1);

            boolean temp = dp[j]; // dp[i-1][j] before overwriting

            if (pc == '?' || sc == pc) {
                dp[j] = prev;
            } else if (pc == '*') {
                dp[j] = dp[j] || dp[j - 1];
            } else {
                dp[j] = false;
            }

            prev = temp;
        }
    }

    return dp[n];
}
```

---

## Greedy (Two Pointers) — O(n) time, O(1) space

For patterns with * but without ? at the beginning, a greedy approach works:

```java
public boolean isMatch(String s, String p) {
    int si = 0, pi = 0, starIdx = -1, match = 0;

    while (si < s.length()) {
        if (pi < p.length() && (p.charAt(pi) == '?' || p.charAt(pi) == s.charAt(si))) {
            si++;
            pi++;
        } else if (pi < p.length() && p.charAt(pi) == '*') {
            starIdx = pi;
            match = si;
            pi++;
        } else if (starIdx != -1) {
            pi = starIdx + 1;
            match++;
            si = match;
        } else {
            return false;
        }
    }

    // Check remaining pattern characters are all *
    while (pi < p.length() && p.charAt(pi) == '*') pi++;

    return pi == p.length();
}
```

## Complexity

| Approach | Time | Space |
|---|---|---|
| DP | O(m*n) | O(m*n) |
| Space-optimized DP | O(m*n) | O(n) |
| Greedy | O(m+n) | O(1) |

## Key Takeaways

1. **? matches exactly one char** — same logic as direct match
2. *** can match empty or multiple chars** — two transitions: empty (dp[i][j-1]) or absorb one (dp[i-1][j])
3. **Base cases**: dp[0][0]=true, dp[0][j] depends on *s, dp[i][0]=false
4. **Greedy works** for patterns with * (backtrack to last * if mismatch)
5. **The dp[i-1][j] transition for *** means "* absorbs one character" — this is the key insight
