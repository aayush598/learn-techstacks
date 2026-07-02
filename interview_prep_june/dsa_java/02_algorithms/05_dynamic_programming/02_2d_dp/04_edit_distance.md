# Edit Distance (Levenshtein Distance)

**Problem**: Given two strings, find the minimum number of operations (insert, delete, replace) to convert one string into the other.

**Example**: `word1 = "horse", word2 = "ros"` → 3

```
horse → rorse (replace 'h' with 'r')
rorse → rose  (delete 'r')
rose  → ros   (delete 'e')
```

---

## Recurrence

```
dp[i][j] = edit distance between word1[0..i-1] and word2[0..j-1]

dp[i][j] = dp[i-1][j-1]                     if word1[i-1] == word2[j-1]
         = 1 + min(
               dp[i-1][j],    // delete from word1
               dp[i][j-1],    // insert into word1 (delete from word2)
               dp[i-1][j-1]   // replace
           )                   otherwise

Base:
  dp[0][j] = j  (insert j characters)
  dp[i][0] = i  (delete i characters)
```

---

## Bottom-Up DP

```java
public int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[][] dp = new int[m + 1][n + 1];

    // Base cases
    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;

    // Fill DP table
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + Math.min(
                    dp[i - 1][j],      // delete
                    Math.min(
                        dp[i][j - 1],  // insert
                        dp[i - 1][j - 1] // replace
                    )
                );
            }
        }
    }

    return dp[m][n];
}
```

### Trace for word1="horse", word2="ros"

```
        ""   r    o    s
""  [  0,   1,   2,   3]
h   [  1,   1,   2,   3]
o   [  2,   2,   1,   2]
r   [  3,   2,   2,   2]
s   [  4,   3,   3,   2]
e   [  5,   4,   4,   3]
```

**Cell by cell**:
- `dp[1][1]`: 'h' vs 'r' → replace: 1 + dp[0][0] = 1
- `dp[2][2]`: 'o' vs 'o' → match: dp[1][1] = 1
- `dp[3][1]`: 'r' vs 'r' → match: dp[2][0] = 2
- `dp[4][3]`: 's' vs 's' → match: dp[3][2] = 2
- `dp[5][3]`: 'e' vs nothing → delete: 1 + dp[4][3] = 3

Answer: 3

---

## Understanding the Operations

```
dp[i-1][j-1] → replace word1[i-1] with word2[j-1] (cost 1)
dp[i-1][j]   → delete word1[i-1] (cost 1)
dp[i][j-1]   → insert word2[j-1] into word1 (cost 1)
```

Think of it as editing word1 into word2:
- **Delete**: skip current char of word1 (i-1 → i), keep word2 position
- **Insert**: keep word1 position, advance word2 (j-1 → j) — we added word2's char
- **Replace**: change word1[i-1] to word2[j-1], advance both

---

## Space-Optimized

```java
public int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[] dp = new int[n + 1];

    // Initialize for empty word1
    for (int j = 0; j <= n; j++) dp[j] = j;

    for (int i = 1; i <= m; i++) {
        int prev = dp[0]; // dp[i-1][0] = i-1
        dp[0] = i;        // dp[i][0] = i

        for (int j = 1; j <= n; j++) {
            int temp = dp[j]; // dp[i-1][j]

            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                dp[j] = prev; // dp[i-1][j-1]
            } else {
                dp[j] = 1 + Math.min(
                    dp[j],         // dp[i-1][j] → delete
                    Math.min(
                        dp[j - 1], // dp[i][j-1] → insert
                        prev       // dp[i-1][j-1] → replace
                    )
                );
            }

            prev = temp; // update prev for next j
        }
    }

    return dp[n];
}
```

---

## One Edit Distance Check

**Problem**: Check if two strings are at most one edit away.

```java
public boolean isOneEditDistance(String s, String t) {
    int m = s.length(), n = t.length();
    if (Math.abs(m - n) > 1) return false;

    for (int i = 0; i < Math.min(m, n); i++) {
        if (s.charAt(i) != t.charAt(i)) {
            if (m == n) {
                // Replace: check remaining strings are equal
                return s.substring(i + 1).equals(t.substring(i + 1));
            } else if (m > n) {
                // Delete from s: check s[i+1..] == t[i..]
                return s.substring(i + 1).equals(t.substring(i));
            } else {
                // Insert into s: check s[i..] == t[i+1..]
                return s.substring(i).equals(t.substring(i + 1));
            }
        }
    }

    // All characters matched — check length difference
    return Math.abs(m - n) == 1;
}
```

---

## Delete Operation for Two Strings (Only Delete)

**Problem**: Minimum deletions to make two strings equal (only delete operation).

```java
public int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[][] dp = new int[m + 1][n + 1];

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    int lcs = dp[m][n];
    return (m - lcs) + (n - lcs); // deletions from both strings
}
```

This is just LCS! Delete all characters not in the LCS.

---

## Applications

### Word Ladder Helper

```java
// Check if two words differ by exactly one character
private boolean isAdjacent(String a, String b) {
    int diff = 0;
    for (int i = 0; i < a.length(); i++) {
        if (a.charAt(i) != b.charAt(i)) diff++;
    }
    return diff == 1;
}
```

### Auto-correct / Spell Checker

Find closest dictionary word to an input word using edit distance.

---

## Complexity

| Version | Time | Space |
|---|---|---|
| Full 2D DP | O(m*n) | O(m*n) |
| Space-optimized | O(m*n) | O(min(m,n)) |

## Key Takeaways

1. **Edit distance is LCS with additional insert/delete operations** — the match case is identical
2. **Three operations**: insert, delete, replace — each costs 1
3. **The base cases are intuitive**: `dp[0][j] = j` (need j inserts), `dp[i][0] = i` (need i deletes)
4. **Space-optimized**: uses 1D array with prev variable to track dp[i-1][j-1]
5. **One edit distance** is a simpler variant — O(min(m,n)) time, O(1) space
6. **Delete-only** between two strings = LCS-based deletion count
