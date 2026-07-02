# Manacher's Algorithm

## Find All Palindromic Substrings in O(n)

Manacher's algorithm finds all palindromic substrings in **linear time** — a significant improvement over the O(n²) center expansion approach.

### Center Expansion (O(n²))

The naive approach for finding the longest palindromic substring:

```java
public static String longestPalindromeExpand(String s) {
    int n = s.length();
    int start = 0, maxLen = 0;

    for (int center = 0; center < n; center++) {
        // Odd length palindromes
        int len1 = expandAroundCenter(s, center, center);
        // Even length palindromes
        int len2 = expandAroundCenter(s, center, center + 1);
        int len = Math.max(len1, len2);

        if (len > maxLen) {
            maxLen = len;
            start = center - (len - 1) / 2;
        }
    }
    return s.substring(start, start + maxLen);
}

private static int expandAroundCenter(String s, int left, int right) {
    while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
        left--;
        right++;
    }
    return right - left - 1;
}
```

**Time:** O(n²) — each of the 2n-1 centers can expand up to O(n).  
**Space:** O(1).

## Palindrome Transformation (Inserting Separators)

Manacher's converts the string to handle odd and even palindromes uniformly by inserting separators:

```
Original: "ababa"
Transformed: "^#a#b#a#b#a#$"  (or just "#a#b#a#b#a#")
```

With separators, every palindrome in the original corresponds to an **odd-length** palindrome in the transformed string. Each palindrome in the transformed string has a center (either at a character or at a `#`).

## LPS Length Array Building

The core of Manacher's is the array `P[]` where `P[i]` is the **radius** of the palindrome centered at `i` (half-length, including center).

```
Index:   0 1 2 3 4 5 6 7 8
Trans:   # a # b # a # b # a #
P[i]:    1 2 1 4 1 6 1 4 1 2 1
```

At the center `i=5` (character 'a'), `P[5]=6` means the palindrome extends 6 characters in each direction: "a#b#a#b#a" (half-length including center).

### How P[i] gives the answer

- `P[i] - 1` is the length of the palindrome in the **original** string
- `(i - P[i]) / 2` is the start index in the original string

## Implementation

```java
public static String longestPalindrome(String s) {
    if (s == null || s.length() == 0) return "";

    // Transform: insert separators
    StringBuilder t = new StringBuilder("#");
    for (char c : s.toCharArray()) {
        t.append(c).append("#");
    }
    String transformed = t.toString();

    int n = transformed.length();
    int[] p = new int[n]; // palindrome radii
    int center = 0, rightBoundary = 0;
    int maxLen = 0, maxCenter = 0;

    for (int i = 0; i < n; i++) {
        // Mirror of i with respect to center
        int mirror = 2 * center - i;

        if (i < rightBoundary) {
            p[i] = Math.min(p[mirror], rightBoundary - i);
        }

        // Expand beyond the known palindrome
        int left = i - (p[i] + 1);
        int right = i + (p[i] + 1);
        while (left >= 0 && right < n && transformed.charAt(left) == transformed.charAt(right)) {
            p[i]++;
            left--;
            right++;
        }

        // Update center and right boundary if we expanded beyond it
        if (i + p[i] > rightBoundary) {
            center = i;
            rightBoundary = i + p[i];
        }

        // Track maximum
        if (p[i] > maxLen) {
            maxLen = p[i];
            maxCenter = i;
        }
    }

    // Extract original palindrome
    int start = (maxCenter - maxLen) / 2;
    return s.substring(start, start + maxLen - 1);
}
```

### How the algorithm works

1. **Transformation:** Insert `#` between every character. Now every palindrome is odd-length.
2. **Rightmost palindrome tracking:** Maintain `center` and `rightBoundary` of the palindrome that extends farthest to the right.
3. **Mirror property:** If `i` is within the right boundary, we can initialize `P[i]` to `Math.min(P[mirror], rightBoundary - i)` — the palindrome at `i` is at least as large as its mirror, but can't extend beyond the boundary.
4. **Expand:** Try to expand beyond the known palindrome.
5. **Update:** If this palindrome extends beyond the right boundary, update `center` and `rightBoundary`.

### Why this is O(n)

Each character is examined at most twice:
- Once when it's part of an expansion that increases the boundary
- Once when it's within an already-verified palindrome

The while loop only executes when the boundary expands, and the boundary only expands O(n) times total.

### Visual trace for "ababa"

```
Transformed: # a # b # a # b # a #
Index:       0 1 2 3 4 5 6 7 8 9 10

i=0: p[0]=1, center=0, RB=0
i=1: mirror=0, p[1] initialized to 0, expand to p[1]=2, center=1, RB=2
i=2: mirror=0, p[2]=min(1,0)=0, expand to p[2]=1
i=3: mirror=1, p[3]=min(2,1)=1, expand to p[3]=4, center=3, RB=6
i=4: mirror=2, p[4]=min(1,2)=1, expand to p[4]=3
i=5: mirror=1, p[5]=min(2,1)=1, expand to p[5]=6, center=5, RB=10
i=6: mirror=4, p[6]=min(3,4)=3, expand to p[6]=3
i=7: mirror=3, p[7]=min(4,3)=3, expand to p[7]=4
i=8: mirror=2, p[8]=min(1,3)=1, expand to p[8]=1
i=9: mirror=1, p[9]=min(2,2)=2, expand to p[9]=2
i=10: p[10]=1

Max: p[5]=6, center=5 → palindrome length = 6-1=5, start=(5-6)/2=0
Original: "ababa"
```

## Counting Palindromic Substrings

Same concept, just count instead of tracking max:

```java
public static int countPalindromicSubstrings(String s) {
    StringBuilder t = new StringBuilder("#");
    for (char c : s.toCharArray()) t.append(c).append("#");
    String transformed = t.toString();

    int n = transformed.length();
    int[] p = new int[n];
    int center = 0, rightBoundary = 0;
    int count = 0; // count palindromes in original string

    for (int i = 0; i < n; i++) {
        if (i < rightBoundary) {
            p[i] = Math.min(p[2 * center - i], rightBoundary - i);
        }

        int left = i - (p[i] + 1);
        int right = i + (p[i] + 1);
        while (left >= 0 && right < n && transformed.charAt(left) == transformed.charAt(right)) {
            p[i]++;
            left--;
            right++;
        }

        if (i + p[i] > rightBoundary) {
            center = i;
            rightBoundary = i + p[i];
        }

        // Each palindrome in transformed with odd radius r corresponds to
        // (r)/2 palindromes in original (centered at character or between chars)
        count += (p[i] + 1) / 2;
    }
    return count;
}
```

## Manacher's vs Center Expansion

| Aspect | Center Expansion | Manacher's |
|--------|-----------------|------------|
| Time | O(n²) | O(n) |
| Space | O(1) | O(n) |
| Complexity | Simple | Complex |
| Multiple queries | Same O(n²) each | Preprocess in O(n) |
| Count palindromes | O(n²) | O(n) |

**When to use Manacher's:**
- LeetCode problems specifically asking for O(n) solution
- Very long strings (10⁵+ characters)
- When counting palindromes, not just finding one

**When NOT to use Manacher's in an interview:**
- You're allowed O(n²) — center expansion is much simpler to code
- The string is short (< 1000 characters)
- You're being tested on understanding rather than optimal implementation

## Practice Problems

| Problem | Platform | Notes |
|---------|----------|-------|
| Longest Palindromic Substring | LeetCode 5 | Classic Manacher's |
| Palindromic Substrings | LeetCode 647 | Count all |
| Shortest Palindrome | LeetCode 214 | Can use Manacher's |
| Palindrome Pairs | LeetCode 336 | Variant |
| Longest Palindromic Subsequence | LeetCode 516 | Use DP, not Manacher's |
