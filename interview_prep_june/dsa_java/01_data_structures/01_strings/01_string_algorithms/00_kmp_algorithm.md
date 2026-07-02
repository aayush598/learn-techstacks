# KMP Algorithm (Knuth-Morris-Pratt)

## Problem: Pattern Search

Given a text `T` of length n and a pattern `P` of length m, find all occurrences of `P` in `T`.

### Why not O(n*m)?

The naive approach checks every position in T against P:
```java
for (int i = 0; i <= n - m; i++) {
    for (int j = 0; j < m; j++) {
        if (T[i + j] != P[j]) break;
    }
}
```
Worst case: O(n*m) — e.g., searching "AAAAAAB" in "AAAAAAAAAAAAAAB".

**KMP eliminates the backtracking** in the text. Once a mismatch occurs at position `i` in T, we don't reset `i`. We use what we already know about the pattern to skip ahead intelligently.

**Time:** O(n + m) — each character in T is examined at most twice.

## LPS Array: Longest Proper Prefix which is also Suffix

The key to KMP. For each prefix of the pattern, we compute the length of the longest proper prefix that is also a suffix.

```
Pattern: "ABABCABAB"

lps[0] = 0 (A has no proper prefix)
lps[1] = 0 (AB: "A" != "B")
lps[2] = 1 (ABA: "A" == "A" → length 1)
lps[3] = 2 (ABAB: "AB" == "AB" → length 2)
lps[4] = 0 (ABABC: no match)
lps[5] = 1 (ABABCA: "A" == "A")
lps[6] = 2 (ABABCAB: "AB" == "AB")
lps[7] = 3 (ABABCABA: "ABA" == "ABA")
lps[8] = 4 (ABABCABAB: "ABAB" == "ABAB")
```

### Building LPS: Two-Pointer Approach

```java
public static int[] buildLPS(String pattern) {
    int m = pattern.length();
    int[] lps = new int[m];
    int len = 0; // length of previous longest prefix suffix
    int i = 1;

    while (i < m) {
        if (pattern.charAt(i) == pattern.charAt(len)) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0) {
                // Fall back to previous LPS value
                len = lps[len - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }
    return lps;
}
```

### Step-by-step LPS building for "AAACAAAA"

```
i=0: lps[0]=0
i=1: P[1]=A == P[0]=A → len=1, lps[1]=1
i=2: P[2]=A == P[1]=A → len=2, lps[2]=2
i=3: P[3]=C != P[2]=A → len=lps[1]=1
     P[3]=C != P[1]=A → len=lps[0]=0
     P[3]=C != P[0]=A → lps[3]=0
i=4: P[4]=A == P[0]=A → len=1, lps[4]=1
i=5: P[5]=A == P[1]=A → len=2, lps[5]=2
i=6: P[6]=A == P[2]=A → len=3, lps[6]=3
i=7: P[7]=A != P[3]=C → len=lps[2]=2
     P[7]=A == P[2]=A → len=3, lps[7]=3
```

### Why the fallback works

When `P[i] != P[len]`, we don't reset `len` to 0 immediately. We use the previously computed LPS to find a shorter prefix that we know matches the suffix. This is the "prefix function" insight.

## Full KMP Search Implementation

```java
public static List<Integer> KMPSearch(String text, String pattern) {
    List<Integer> matches = new ArrayList<>();
    int n = text.length(), m = pattern.length();
    if (m == 0) return matches;

    int[] lps = buildLPS(pattern);
    int i = 0; // index for text
    int j = 0; // index for pattern

    while (i < n) {
        if (text.charAt(i) == pattern.charAt(j)) {
            i++;
            j++;
        }

        if (j == m) {
            matches.add(i - j); // found pattern at index i-j
            j = lps[j - 1]; // continue searching
        } else if (i < n && text.charAt(i) != pattern.charAt(j)) {
            if (j != 0) {
                j = lps[j - 1]; // use LPS to skip
            } else {
                i++; // nothing to fall back to, advance text
            }
        }
    }
    return matches;
}
```

### Visualization

```
Text:    A B A B C A B A B A B A
Pattern: A B A B C A B A B
LPS:     [0 0 1 2 0 1 2 3 4]

Step 1: Compare from start
A B A B C A B A B A B A
A B A B C A B A B    ← match at indices 0-7

Mismatch at i=8, j=8
j = lps[7] = 3 (skip pattern ahead by 3)

A B A B C A B A B A B A
        A B A B C A B A B   ← compare from pattern[3]
```

The text pointer `i` doesn't go backward. We only adjust `j` using LPS. This guarantees O(n).

## Applications

### Shortest Palindrome

**Problem:** Given a string, find the shortest palindrome by adding characters in front.

```java
public static String shortestPalindrome(String s) {
    // Create: s + "#" + reverse(s)
    String rev = new StringBuilder(s).reverse().toString();
    String combined = s + "#" + rev;

    // LPS of combined tells us the longest palindromic prefix
    int[] lps = buildLPS(combined);
    int longestPalPrefix = lps[lps.length - 1];

    // Append reverse of remaining part
    String suffix = rev.substring(0, rev.length() - longestPalPrefix);
    return suffix + s;
}
```

**How it works:** The `#` separator ensures LPS doesn't cross the boundary. The last LPS value gives the longest prefix of `s` that matches a suffix of `rev` — which is the longest palindromic prefix of `s`.

### String Period

**Problem:** Find the smallest period of a string (e.g., "ABABAB" → period 2, "ABABABA" → no period).

```java
public static boolean hasPeriod(String s) {
    int[] lps = buildLPS(s);
    int n = s.length();
    int period = n - lps[n - 1];
    return n % period == 0;
}

public static int getPeriod(String s) {
    int[] lps = buildLPS(s);
    int n = s.length();
    int period = n - lps[n - 1];
    if (n % period == 0) return period;
    return -1; // no period
}
```

**Why this works:** `s.length() - lps[s.length() - 1]` gives the smallest period. If `s` has period k, then the longest prefix-suffix is `s.length() - k`.

### Repeated Substring Pattern (LeetCode 459)

```java
public static boolean repeatedSubstringPattern(String s) {
    int[] lps = buildLPS(s);
    int n = s.length();
    int period = n - lps[n - 1];
    return lps[n - 1] > 0 && n % period == 0;
}
```

## Practice Problems

| Problem | Platform | Notes |
|---------|----------|-------|
| Implement strStr() | LeetCode 28 | KMP implementation |
| Shortest Palindrome | LeetCode 214 | KMP + concatenation |
| Repeated Substring Pattern | LeetCode 459 | LPS last value |
| Find the String in Grid | LeetCode | KMP per row |
| Longest Happy Prefix | LeetCode 1392 | LPS of whole string |

## Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Build LPS | O(m) | O(m) |
| Search | O(n) | O(m) (for LPS) |
| Total | O(n + m) | O(m) |
