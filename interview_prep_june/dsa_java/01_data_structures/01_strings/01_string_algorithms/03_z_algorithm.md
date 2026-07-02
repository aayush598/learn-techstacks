# Z Algorithm

## Z-Array Definition

The Z-array for a string `S` of length `n` stores, for each position `i`, the length of the longest substring starting at `S[i]` that matches the **prefix** of `S`.

```
S = "a a a b a a a"
Z = [7, 2, 1, 0, 3, 2, 1]
```

- `Z[0]` is defined as `n` (the full string length)
- `Z[1]=2` because `S[1..2]="aa"` matches `S[0..1]="aa"`
- `Z[2]=1` because `S[2]="a"` matches `S[0]="a"`
- `Z[3]=0` because `S[3]="b"` != `S[0]="a"`
- `Z[4]=3` because `S[4..6]="aaa"` matches `S[0..2]="aaa"`

## Z-Box: Maintaining [l, r] Interval

The efficiency comes from maintaining a **Z-box** — the interval `[l, r]` that represents the rightmost prefix match found so far. This is analogous to Manacher's rightmost palindrome.

```
When we know S[l..r] matches S[0..r-l], and we're at position i:
- If i <= r, then Z[i] can be initialized using Z[i-l]:
  - If Z[i-l] < r-i+1: Z[i] = Z[i-l] (completely inside known box)
  - Else: Z[i] = r-i+1, then extend manually
- If i > r: compute Z[i] from scratch
```

## Implementation

```java
public static int[] buildZArray(String s) {
    int n = s.length();
    int[] z = new int[n];
    if (n == 0) return z;

    int l = 0, r = 0;
    for (int i = 1; i < n; i++) {
        // Case 1: i is within the Z-box
        if (i <= r) {
            z[i] = Math.min(r - i + 1, z[i - l]);
        }

        // Extend manually
        while (i + z[i] < n && s.charAt(z[i]) == s.charAt(i + z[i])) {
            z[i]++;
        }

        // Update Z-box if we extended beyond r
        if (i + z[i] - 1 > r) {
            l = i;
            r = i + z[i] - 1;
        }
    }

    z[0] = n; // by convention
    return z;
}
```

### Step-by-Step Example: "aaabaab"

```
i=0: Z[0]=7 (by convention)
i=1: i>r, compare S[1..] with S[0..], Z[1]=2, l=1, r=2
     (S[1..2]="aa" matches prefix "aa")
i=2: i<=r, mirror=2-1=1, Z[1]=2, r-i+1=1
     z[2]=min(2,1)=1, then extend: S[3]='b' != S[1]='a', no extension
     Z[2]=1
i=3: i>r, compare: S[3]='b' != S[0]='a', Z[3]=0
i=4: i>r, compare: S[4]='a' == S[0]='a', S[5]='a' == S[1]='a', S[6]='b' != S[2]='a'
     Z[4]=2, l=4, r=5
i=5: i<=r, mirror=5-4=1, Z[1]=2, r-i+1=1
     z[5]=min(2,1)=1, then extend: S[6]='b' != S[1]='a'
     Z[5]=1
i=6: i>r, compare: S[6]='b' != S[0]='a', Z[6]=0

Z = [7, 2, 1, 0, 2, 1, 0]
```

## Applications

### Pattern Search (like KMP)

To search for pattern P in text T, create the combined string `P + "$" + T` (where `$` is a character not in either string):

```java
public static List<Integer> zSearch(String text, String pattern) {
    String combined = pattern + "$" + text;
    int[] z = buildZArray(combined);
    int patternLen = pattern.length();
    List<Integer> matches = new ArrayList<>();

    for (int i = patternLen + 1; i < combined.length(); i++) {
        if (z[i] == patternLen) {
            matches.add(i - patternLen - 1);
        }
    }
    return matches;
}
```

**Time:** O(n + m) — same as KMP.

### String Compression

Find the smallest period of a string:

```java
public static int getPeriod(String s) {
    int[] z = buildZArray(s);
    int n = s.length();

    for (int i = 1; i < n; i++) {
        if (z[i] == n - i && n % i == 0) {
            return i;
        }
    }
    return n;
}
```

**Why:** If `Z[i] == n-i`, the suffix starting at i matches the prefix of length `n-i`. If `i` divides `n`, the string has period `i`.

### Distinct Substrings Count

Count distinct substrings by computing Z-array for each suffix:

```java
public static int countDistinctSubstrings(String s) {
    int n = s.length();
    int count = 0;
    StringBuilder current = new StringBuilder();

    for (int i = 0; i < n; i++) {
        // Add character by character
        current.append(s.charAt(i));
        String cur = current.toString();

        // Compute Z for cur$cur (or use a rolling approach)
        String combined = cur + "$" + cur;
        int[] z = buildZArray(combined);
        int maxPrefix = 0;
        for (int j = cur.length() + 1; j < combined.length(); j++) {
            maxPrefix = Math.max(maxPrefix, z[j]);
        }
        count += cur.length() - maxPrefix;
    }
    return count;
}
```

A more efficient O(n²) approach: for each suffix, compute Z-array of the suffix and count distinct prefixes.

### Longest Common Prefix of Two Suffixes

Given two suffixes starting at i and j, the LCP is Z[i] in the string `S.substring(i) + "$" + S.substring(j)`.

Or more efficiently using suffix array + LCP array, but Z-algorithm works for O(n) per pair.

## Z-Algorithm vs KMP

| Aspect | Z-Algorithm | KMP |
|--------|-------------|-----|
| Core array | Z-array | LPS array |
| Z[i] = longest prefix match at i | ✓ | ✗ |
| LPS[i] = longest proper prefix-suffix of prefix | ✗ | ✓ |
| Pattern search | Concatenate P$T | Build LPS of P |
| Space | O(n) | O(m) |
| Ease of understanding | Moderate | Moderate |
| String compression | Direct | Uses LPS last value |

Both are O(n + m). The Z-algorithm is conceptually simpler for pattern search (no separate search phase, just build Z and scan).

## Common Mistakes

1. **Z[0] = 0 for some implementations** — make sure you set Z[0] = n. Some implementations leave it as 0, which is valid if you never use Z[0] for matching.
2. **Not handling the separator carefully** — the separator `$` must not appear in P or T.
3. **Z-box updates** — forgetting to update l and r when extending beyond the current Z-box.
4. **Off-by-one in substring matching** — careful with string indices.

## Practice Problems

| Problem | Platform | Notes |
|---------|----------|-------|
| Implement strStr() | LeetCode 28 | Z-algorithm approach |
| Repeated Substring Pattern | LeetCode 459 | Z-based period |
| Longest Happy Prefix | LeetCode 1392 | Z[n-1] or LPS |
| Minimum Time to Make String Sorted | - | Z for period |
| String Compression | - | Z for period finding |
| Shortest Palindrome | LeetCode 214 | Z on s$rev |
