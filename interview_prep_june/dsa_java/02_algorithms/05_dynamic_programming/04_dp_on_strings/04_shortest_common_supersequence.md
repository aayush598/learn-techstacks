# Shortest Common Supersequence (SCS)

**Problem**: Given two strings, find the shortest string that has both strings as subsequences.

**Example**: `s1 = "abac", s2 = "cab"` → SCS = "cabac" (length 5)

---

## Length of SCS

```
SCS length = s1.length() + s2.length() - LCS(s1, s2)
```

The supersequence is formed by merging s1 and s2, keeping the LCS characters only once.

```java
public int shortestCommonSupersequenceLength(String s1, String s2) {
    int m = s1.length(), n = s2.length();
    int lcsLength = lcs(s1, s2);
    return m + n - lcsLength;
}
```

---

## Print SCS

Use DP table backtracking — similar to printing LCS, but with different logic.

```java
public String shortestCommonSupersequence(String str1, String str2) {
    int m = str1.length(), n = str2.length();
    int[][] dp = new int[m + 1][n + 1];

    // Fill LCS DP table
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    // Backtrack to build SCS
    StringBuilder sb = new StringBuilder();
    int i = m, j = n;

    while (i > 0 && j > 0) {
        if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
            // Common character — include once
            sb.append(str1.charAt(i - 1));
            i--;
            j--;
        } else if (dp[i - 1][j] > dp[i][j - 1]) {
            // str1's character is not in LCS — include it and move i back
            sb.append(str1.charAt(i - 1));
            i--;
        } else {
            // str2's character is not in LCS — include it and move j back
            sb.append(str2.charAt(j - 1));
            j--;
        }
    }

    // Add remaining characters
    while (i > 0) {
        sb.append(str1.charAt(i - 1));
        i--;
    }
    while (j > 0) {
        sb.append(str2.charAt(j - 1));
        j--;
    }

    return sb.reverse().toString();
}
```

### Trace for str1="abac", str2="cab"

```
LCS table:
     ""  c   a   b
"" [ 0,  0,  0,  0]
a  [ 0,  0,  1,  1]
b  [ 0,  0,  1,  2]
a  [ 0,  0,  1,  2]
c  [ 0,  1,  1,  2]

LCS = "ab" or "ac" (length 2)
SCS length = 4 + 3 - 2 = 5

Backtrack:
i=4,j=3: 'c' != 'b', dp[3][3]=2 > dp[4][2]=1 → take str2[2]='b', j=2
i=4,j=2: 'c' == 'c'! dp[3][1]=1, dp[4][1]=1. They're equal → take str2[1]='a', j=1
Actually they're equal so either works. Let me trace properly:

dp table:
     ""  c   a   b
"" [ 0,  0,  0,  0]
a  [ 0,  0,  1,  1]
b  [ 0,  0,  1,  2]
a  [ 0,  0,  1,  2]
c  [ 0,  1,  1,  2]

i=4(j=3): str1[3]='c', str2[2]='b', not equal
  dp[3][3]=2, dp[4][2]=1, dp[3][3] > dp[4][2] → take str1[3]='c', i=3
i=3(j=3): str1[2]='a', str2[2]='b', not equal
  dp[2][3]=2, dp[3][2]=1, dp[2][3] > dp[3][2] → take str2[2]='b', j=2
i=3(j=2): str1[2]='a', str2[1]='a', EQUAL! → take 'a', i=2, j=1
i=2(j=1): str1[1]='b', str2[0]='c', not equal
  dp[1][1]=0, dp[2][0]=0 → equal, follow any
  → take str2[0]='c', j=0
i=2(j=0): remaining str1[1]='b', str1[0]='a' → take 'b', then 'a'

Result reverse: c, b, a, a, c → "cabac" ✓
```

---

## Alternative: Using LCS String

```java
public String shortestCommonSupersequence(String str1, String str2) {
    String lcs = longestCommonSubsequence(str1, str2);

    StringBuilder sb = new StringBuilder();
    int i = 0, j = 0;

    for (char c : lcs.toCharArray()) {
        // Add all chars from str1 up to this LCS char
        while (i < str1.length() && str1.charAt(i) != c) {
            sb.append(str1.charAt(i++));
        }
        // Add all chars from str2 up to this LCS char
        while (j < str2.length() && str2.charAt(j) != c) {
            sb.append(str2.charAt(j++));
        }
        // Add the LCS character
        sb.append(c);
        i++;
        j++;
    }

    // Add remaining characters
    sb.append(str1.substring(i));
    sb.append(str2.substring(j));

    return sb.toString();
}
```

---

## Complexity

| Operation | Time | Space |
|---|---|---|
| Length of SCS | O(m*n) | O(m*n) |
| Print SCS | O(m*n) | O(m*n) |
| SCS via LCS | O(m*n) | O(m*n) |

## Key Takeaways

1. **SCS length = m + n - LCS** — simple formula once you know LCS
2. **Backtracking merges two strings** while keeping LCS once
3. **The backtrack logic**: take characters from str1 or str2 based on which way LCS increased
4. **Always include extra characters** that aren't part of LCS
5. **Same DP table as LCS** — just different backtracking
