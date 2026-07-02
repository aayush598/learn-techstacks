# Rabin-Karp Algorithm

## Rolling Hash

Rabin-Karp uses **hashing** to find pattern matches. The key innovation is the **rolling hash** — computing the hash of the next window in O(1) instead of O(m).

### Hash Function

For a string of length k, we use a polynomial hash:

```
hash(s[0..k-1]) = s[0]*d^(k-1) + s[1]*d^(k-2) + ... + s[k-1]*d^0
```

Where `d` is a base (typically 26 for lowercase letters, 256 for ASCII).

### Rolling the window

When the window slides from position `i` to `i+1`:

```
newHash = (oldHash - s[i]*d^(k-1)) * d + s[i+k]
```

This removes the contribution of the character leaving the window and adds the new character.

## Implementation

```java
public class RabinKarp {
    private final String pattern;
    private final long patternHash;
    private final int m;
    private final long d;  // base (radix)
    private final long q;  // modulus (prime)

    public RabinKarp(String pattern) {
        this.pattern = pattern;
        this.m = pattern.length();
        this.d = 256; // ASCII
        this.q = 101; // large prime
        this.patternHash = hash(pattern, m);
    }

    // Compute hash of first m characters
    private long hash(String s, int len) {
        long h = 0;
        for (int i = 0; i < len; i++) {
            h = (h * d + s.charAt(i)) % q;
        }
        return h;
    }

    public List<Integer> search(String text) {
        List<Integer> matches = new ArrayList<>();
        int n = text.length();
        if (n < m) return matches;

        // Precompute d^(m-1) mod q
        long h = 1;
        for (int i = 0; i < m - 1; i++) {
            h = (h * d) % q;
        }

        long textHash = hash(text, m);

        for (int i = 0; i <= n - m; i++) {
            if (patternHash == textHash) {
                // Verify character by character (handle spurious hits)
                if (checkEqual(text, i)) {
                    matches.add(i);
                }
            }

            // Compute next hash (slide window)
            if (i < n - m) {
                textHash = (d * (textHash - text.charAt(i) * h) + text.charAt(i + m)) % q;
                // Handle negative
                if (textHash < 0) textHash += q;
            }
        }
        return matches;
    }

    private boolean checkEqual(String text, int start) {
        for (int j = 0; j < m; j++) {
            if (pattern.charAt(j) != text.charAt(start + j)) return false;
        }
        return true;
    }
}
```

### Spurious Hits and How to Handle

A **spurious hit** occurs when hashes match but strings don't. This can happen because:
1. **Hash collisions** — two different strings can have the same hash mod q
2. **Modulo arithmetic** — we take mod q, so information is lost

**Solution:** When hashes match, always **verify character by character**. This is why we have `checkEqual()`.

### Probability of spurious hits

With a large prime q (≈ 10⁹), the probability of a collision is ~1/q ≈ 10⁻⁹ per comparison. For practical purposes, this is negligible.

### Without modulo (risking overflow)

If we skip the modulo, hash values grow exponentially — `d^(m-1)` for m=1000 and d=256 is enormous (256⁹⁹⁹). Integer overflow makes the hash wrap around, effectively giving us mod 2³² — which works but has more collisions than a proper prime.

## Applications

### Finding multiple pattern matches

Rabin-Karp is excellent when the pattern is long and the text is large. KMP is typically faster for single pattern search, but Rabin-Karp can be extended to multiple patterns.

### Multiple pattern search

```java
public class RabinKarpMultiple {
    private final Set<String> patterns;
    private final int m;
    private final long d = 256;
    private final long q = 101;
    private final Set<Long> patternHashes;

    public RabinKarpMultiple(Set<String> patterns) {
        this.patterns = patterns;
        this.m = patterns.iterator().next().length(); // assume same length
        this.patternHashes = new HashSet<>();
        for (String p : patterns) {
            patternHashes.add(hash(p, m));
        }
    }

    public List<Integer> search(String text) {
        List<Integer> matches = new ArrayList<>();
        int n = text.length();
        if (n < m) return matches;

        long h = 1;
        for (int i = 0; i < m - 1; i++) {
            h = (h * d) % q;
        }

        long textHash = hash(text, m);
        for (int i = 0; i <= n - m; i++) {
            if (patternHashes.contains(textHash)) {
                for (String pattern : patterns) {
                    if (checkEqual(text, i, pattern)) {
                        matches.add(i);
                        break;
                    }
                }
            }
            if (i < n - m) {
                textHash = (d * (textHash - text.charAt(i) * h) + text.charAt(i + m)) % q;
                if (textHash < 0) textHash += q;
            }
        }
        return matches;
    }

    // ... hash and checkEqual methods similar to single pattern
}
```

### Longest Duplicate Substring (LeetCode 1044)

Rabin-Karp combined with binary search:

```java
public static String longestDupSubstring(String s) {
    int n = s.length();
    int left = 1, right = n;
    String result = "";

    while (left <= right) {
        int mid = left + (right - left) / 2;
        String dup = hasDuplicate(s, mid);
        if (dup != null) {
            result = dup;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return result;
}

private static String hasDuplicate(String s, int len) {
    long d = 256, q = (1 << 31) - 1;
    long h = 1;
    for (int i = 0; i < len - 1; i++) h = (h * d) % q;

    Map<Long, List<Integer>> seen = new HashMap<>();
    long hash = 0;
    for (int i = 0; i < len; i++) hash = (hash * d + s.charAt(i)) % q;
    seen.computeIfAbsent(hash, k -> new ArrayList<>()).add(0);

    for (int i = 1; i <= s.length() - len; i++) {
        hash = (d * (hash - s.charAt(i - 1) * h) + s.charAt(i + len - 1)) % q;
        if (hash < 0) hash += q;

        if (seen.containsKey(hash)) {
            String candidate = s.substring(i, i + len);
            for (int start : seen.get(hash)) {
                if (s.substring(start, start + len).equals(candidate)) {
                    return candidate;
                }
            }
        }
        seen.computeIfAbsent(hash, k -> new ArrayList<>()).add(i);
    }
    return null;
}
```

## Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Preprocessing | O(m) | O(1) |
| Search (avg/best) | O(n + m) | O(1) |
| Search (worst) | O(n * m) | O(1) |

**Worst case:** When many spurious hits occur — e.g., matching "AAAAA" against "AAAAAAAAAAAAA". Every window produces a hash match that requires O(m) verification. In practice, a good hash function makes this extremely rare.

## Rabin-Karp vs KMP

| Aspect | Rabin-Karp | KMP |
|--------|------------|-----|
| Worst-case time | O(n*m) | O(n+m) |
| Average time | O(n+m) | O(n+m) |
| Multiple patterns | Easy extension | Needs separate automaton per pattern |
| Space | O(1) | O(m) |
| Rolling hash | Core technique | Not used |
| LPS array | Not used | Core technique |

## Practice Problems

| Problem | Platform | Notes |
|---------|----------|-------|
| Find the Index of the First Occurrence | LeetCode 28 | Implement with Rabin-Karp |
| Repeated DNA Sequences | LeetCode 187 | Fixed length rolling hash |
| Longest Duplicate Substring | LeetCode 1044 | Rolling hash + binary search |
| Distinct Echo Substrings | LeetCode 1316 | Rolling hash |
| String Matching in an Array | LeetCode 1408 | Multiple pattern search |
