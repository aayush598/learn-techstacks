# Distinct Subsequences

**Problem**: Given two strings s and t, count the number of distinct subsequences of s that equal t.

**Example**: `s = "rabbbit", t = "rabbit"` → 3

```
s = rabb b it
    rab b bit
    ra b bbit
```

---

## Recurrence

```
dp[i][j] = number of distinct subsequences of s[0..i-1] that equal t[0..j-1]

dp[i][j] = dp[i-1][j]                              (skip s[i-1])
         + (s[i-1] == t[j-1] ? dp[i-1][j-1] : 0)   (match s[i-1] with t[j-1])

Base:
  dp[i][0] = 1 (empty t is subsequence of any s)
  dp[0][j] = 0 for j > 0 (non-empty t can't be subsequence of empty s)
```

---

## Bottom-Up DP

```java
public int numDistinct(String s, String t) {
    int m = s.length(), n = t.length();
    int[][] dp = new int[m + 1][n + 1];

    // Empty t is a subsequence of any prefix of s
    for (int i = 0; i <= m; i++) {
        dp[i][0] = 1;
    }

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            // Always skip current character of s
            dp[i][j] = dp[i - 1][j];

            // If characters match, we can also use it
            if (s.charAt(i - 1) == t.charAt(j - 1)) {
                dp[i][j] += dp[i - 1][j - 1];
            }
        }
    }

    return dp[m][n];
}
```

### Trace for s="rabbbit", t="rabbit"

```
     ""  r   a   b   b   i   t
"" [ 1,  0,  0,  0,  0,  0,  0]
r  [ 1,  1,  0,  0,  0,  0,  0]
a  [ 1,  1,  1,  0,  0,  0,  0]
b  [ 1,  1,  1,  1,  0,  0,  0]
b  [ 1,  1,  1,  2,  1,  0,  0]
b  [ 1,  1,  1,  3,  3,  0,  0]
i  [ 1,  1,  1,  3,  3,  3,  0]
t  [ 1,  1,  1,  3,  3,  3,  3]
```

The answer dp[7][6] = 3.

Observe how dp[4][3] = 1 (one way to make "rab"), dp[5][3] = 2 (two ways), dp[6][3] = 3 (three ways) — each extra 'b' adds more ways to match the "b" in "rabb".

---

## Space-Optimized

```java
public int numDistinct(String s, String t) {
    int n = t.length();
    int[] dp = new int[n + 1];
    dp[0] = 1;

    for (int i = 1; i <= s.length(); i++) {
        int prev = 1; // dp[i-1][0] = 1 for each row
        for (int j = 1; j <= n; j++) {
            int temp = dp[j]; // dp[i-1][j]

            if (s.charAt(i - 1) == t.charAt(j - 1)) {
                dp[j] += prev; // dp[i-1][j-1] + dp[i-1][j] (already in dp[j])
            }
            // else: dp[j] stays as dp[i-1][j]

            prev = temp;
        }
    }

    return dp[n];
}
```

---

## Large Numbers

For large results, use modulo:

```java
public int numDistinct(String s, String t) {
    int MOD = 1_000_000_007;
    int n = t.length();
    int[] dp = new int[n + 1];
    dp[0] = 1;

    for (int i = 1; i <= s.length(); i++) {
        int prev = 1;
        for (int j = 1; j <= n; j++) {
            int temp = dp[j];
            if (s.charAt(i - 1) == t.charAt(j - 1)) {
                dp[j] = (dp[j] + prev) % MOD;
            }
            prev = temp;
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

1. **Recurrence**: dp[i][j] = dp[i-1][j] (skip) + (match ? dp[i-1][j-1] : 0) (take)
2. **Base**: dp[i][0] = 1 for all i (empty string is a subsequence of everything)
3. **State interpretation**: "number of ways to match first j chars of t using first i chars of s"
4. **Space optimization**: 1D array + prev variable for dp[i-1][j-1]
5. **Same pattern** as other string DP: for each pair of chars, we have "skip or match" decisions
