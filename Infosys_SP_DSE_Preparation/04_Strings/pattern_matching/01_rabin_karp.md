# Rabin-Karp Algorithm

## What is Rabin-Karp?

Rabin-Karp uses **hashing** to compare strings. Instead of comparing characters one by one, it compares hash values of the pattern and each text window.

```
  Core Idea:
  ┌─────────────────────────────────────────────────────────┐
  │ Instead of comparing strings character by character,    │
  │ compare their HASH VALUES first. If hashes match,      │
  │ then verify character by character (rare case).        │
  └─────────────────────────────────────────────────────────┘

  Rolling Hash Trick:
  ┌─────────────────────────────────────────────────────────┐
  │ When sliding the window by 1, we can compute the new   │
  │ hash from the old hash in O(1) time:                   │
  │                                                         │
  │  old_window = "ABCD"  (hash = h_old)                   │
  │  new_window = "BCDE"                                    │
  │                                                         │
  │  h_new = (h_old - hash('A') * base^(m-1)) * base       │
  │          + hash('E')                                    │
  │                                                         │
  │  Remove leftmost char, shift, add rightmost char.      │
  └─────────────────────────────────────────────────────────┘
```

## Algorithm Comparison

| Aspect          | Rabin-Karp        | KMP               |
|----------------|-------------------|-------------------|
| Time (Avg)     | O(n+m)            | O(n+m)            |
| Time (Worst)   | O(n*m)            | O(n+m)            |
| Space          | O(1)              | O(m)              |
| Multiple Pat.  | Excellent         | Needs modifications|
| Implementation | Simple            | Moderate          |
| Hash Collisions| Possible          | None              |

```
  ┌──────────────────────────────────────────────────────────┐
  │         RABIN-KARP PROBLEM DECISION GUIDE                │
  ├──────────────────────────────────────────────────────────┤
  │                                                          │
  │  Need to search for MULTIPLE patterns at once?           │
  │  └── Rabin-Karp is ideal (hash each pattern)            │
  │                                                          │
  │  Plagiarism / duplicate detection?                       │
  │  └── Rabin-Karp with rolling hash                        │
  │                                                          │
  │  Need guaranteed O(n+m) single pattern?                  │
  │  └── Use KMP instead (no hash collisions)                │
  │                                                          │
  │  Need O(1) space?                                        │
  │  └── Rabin-Karp uses O(1) vs KMP's O(m)                 │
  │                                                          │
  └──────────────────────────────────────────────────────────┘
```

---

## 1. Polynomial Rolling Hash

```python
def compute_hash(s, base=31, mod=10**9 + 7):
    """Compute polynomial hash of string"""
    hash_val = 0
    for c in s:
        hash_val = (hash_val * base + ord(c)) % mod
    return hash_val

def compute_prefix_hashes(s, base=31, mod=10**9 + 7):
    """Compute prefix hashes for O(1) substring hash queries"""
    n = len(s)
    prefix = [0] * (n + 1)
    powers = [1] * (n + 1)
    
    for i in range(n):
        prefix[i + 1] = (prefix[i] * base + ord(s[i])) % mod
        powers[i + 1] = (powers[i] * base) % mod
    
    return prefix, powers

def get_substring_hash(prefix, powers, l, r, mod=10**9 + 7):
    """Get hash of s[l:r+1] in O(1)"""
    return (prefix[r + 1] - prefix[l] * powers[r - l + 1]) % mod

# Example
s = "abcabc"
prefix, powers = compute_prefix_hashes(s)
print(f"Hash of 'abc' (0:3): {get_substring_hash(prefix, powers, 0, 2)}")
print(f"Hash of 'abc' (3:6): {get_substring_hash(prefix, powers, 3, 5)}")
```

### Visual: Polynomial Rolling Hash

```
  String "abc" with base=31:
  hash('abc') = 'a'*31^2 + 'b'*31^1 + 'c'*31^0
              = 97*961 + 98*31 + 99*1
              = 93217 + 3038 + 99
              = 96354

  Rolling Hash - Sliding Window:
  ┌──────────────────────────────────────────────────────┐
  │ Text: "ABCDABE"    Pattern: "ABD" (m=3)             │
  │                                                       │
  │ Window 1: "ABC"  -> hash = h_ABC                     │
  │                                                       │
  │ Slide to "BCD":                                        │
  │   h_BCD = (h_ABC - 'A'*base^2) * base + 'D'          │
  │   Remove 'A', shift left, add 'D'                    │
  │                                                       │
  │ This is O(1) per slide!                               │
  └──────────────────────────────────────────────────────┘

  Hash Formula:
  ┌──────────────────────────────────────────────────────┐
  │  h(s[l..r]) = prefix[r+1] - prefix[l] * base^(r-l+1)│
  │  All operations mod MOD to prevent overflow           │
  └──────────────────────────────────────────────────────┘
```

## 2. Basic Rabin-Karp Implementation

```python
def rabin_karp(text, pattern, base=31, mod=10**9 + 7):
    """
    Rabin-Karp string matching algorithm
    Time: O(n + m) average, O(n * m) worst case
    Space: O(1)
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    # Compute pattern hash
    pattern_hash = compute_hash(pattern, base, mod)
    
    # Compute initial window hash
    window_hash = compute_hash(text[:m], base, mod)
    
    result = []
    power = pow(base, m - 1, mod)
    
    for i in range(n - m + 1):
        # Compare hashes
        if window_hash == pattern_hash:
            # Verify to handle hash collisions
            if text[i:i + m] == pattern:
                result.append(i)
        
        # Compute next window hash
        if i < n - m:
            # Remove leftmost character, add new character
            window_hash = (window_hash - ord(text[i]) * power) % mod
            window_hash = (window_hash * base + ord(text[i + m])) % mod
            window_hash = (window_hash + mod) % mod
    
    return result

# Example
text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
print(f"Pattern found at: {rabin_karp(text, pattern)}")
```

### Visual: Rolling Hash Sliding Window

```
  text = "ABABDABACDABABCABAB"
  pattern = "ABABCABAB" (m=9)

  Step 1: Compute pattern hash
  h_pattern = hash("ABABCABAB") = some value

  Step 2: Slide window across text

  Window 0: "ABABDABAC" -> hash vs h_pattern -> mismatch
  Window 1: "BABDABACD" -> hash vs h_pattern -> mismatch
  ...
  Window 9: "DABABCABA" -> hash vs h_pattern -> mismatch
  Window 10:"ABABCABAB" -> hash == h_pattern -> VERIFY -> MATCH!

  Rolling hash update for each slide:
  ┌─────────────────────────────────────────────────────┐
  │ h_new = (h_old - ord(text[i]) * base^(m-1))        │
  │         * base + ord(text[i+m])                     │
  │ h_new = h_new % MOD                                 │
  │ h_new = (h_new + MOD) % MOD  (ensure non-negative) │
  └─────────────────────────────────────────────────────┘
```

## 3. Handling Hash Collisions

```python
def rabin_karp_with_collision_handling(text, pattern, base=31, mod=10**9 + 7):
    """Rabin-Karp with explicit collision handling"""
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    pattern_hash = compute_hash(pattern, base, mod)
    window_hash = compute_hash(text[:m], base, mod)
    
    result = []
    power = pow(base, m - 1, mod)
    
    collision_count = 0
    
    for i in range(n - m + 1):
        if window_hash == pattern_hash:
            # Hash match - verify
            if text[i:i + m] == pattern:
                result.append(i)
            else:
                collision_count += 1
        
        if i < n - m:
            window_hash = (window_hash - ord(text[i]) * power) % mod
            window_hash = (window_hash * base + ord(text[i + m])) % mod
            window_hash = (window_hash + mod) % mod
    
    if collision_count > 0:
        print(f"Handled {collision_count} hash collisions")
    
    return result

# Example with potential collisions
text = "aaaaaa"
pattern = "aaa"
print(rabin_karp_with_collision_handling(text, pattern))
```

## 4. Multiple Pattern Matching

```python
def rabin_karp_multiple(text, patterns, base=31, mod=10**9 + 7):
    """Search for multiple patterns simultaneously"""
    n = len(text)
    
    # Precompute hashes for all patterns
    pattern_hashes = {}
    max_len = 0
    
    for pattern in patterns:
        h = compute_hash(pattern, base, mod)
        pattern_hashes[h] = pattern
        max_len = max(max_len, len(pattern))
    
    # Precompute prefix hashes for text
    prefix, powers = compute_prefix_hashes(text, base, mod)
    
    results = {pattern: [] for pattern in patterns}
    
    # Check all possible lengths
    for length in range(1, max_len + 1):
        power = powers[length]
        seen = {}
        
        for i in range(n - length + 1):
            h = get_substring_hash(prefix, powers, i, i + length - 1, mod)
            
            if h in pattern_hashes:
                pattern = pattern_hashes[h]
                if len(pattern) == length and text[i:i + length] == pattern:
                    results[pattern].append(i)
    
    return results

# Example
text = "abcabcabc"
patterns = ["abc", "bca", "cab"]
print(rabin_karp_multiple(text, patterns))
```

## 5. Time Complexity Analysis

```python
"""
RABIN-KARP COMPLEXITY ANALYSIS:

Best Case: O(n + m)
- When pattern doesn't exist in text
- Hash comparison is O(m), but we do O(n) comparisons
- Total: O(n + m)

Average Case: O(n + m)
- With good hash function, few collisions
- Expected number of spurious hits: O(n/m) with good hash

Worst Case: O(n * m)
- When all hash values match but strings don't
- Example: text = "AAAAAAAA", pattern = "AAAB"
- Every window matches hash, but verification fails

Space Complexity: O(1)
- Only need to store hash values

ADVANTAGES:
1. Good for multiple pattern matching
2. Simple to implement
3. Can detect plagiarism (searching many patterns)

DISADVANTAGES:
1. Worst case O(n*m)
2. Hash collisions require verification
3. Not as efficient as KMP for single pattern
"""
```

## 6. Applications

```python
# APPLICATION 1: Plagiarism Detection
def detect_plagiarism(document, sentences, threshold=0.7):
    """Detect potential plagiarism using Rabin-Karp"""
    n = len(document)
    results = []
    
    for sentence in sentences:
        occurrences = rabin_karp(document, sentence)
        if occurrences:
            similarity = len(sentence) / n
            if similarity >= threshold:
                results.append({
                    'sentence': sentence,
                    'positions': occurrences,
                    'similarity': similarity
                })
    
    return results

# APPLICATION 2: Finding All Rotations of a String
def find_all_rotations(text, pattern):
    """Find all rotations of pattern in text"""
    if len(text) < len(pattern):
        return []
    
    results = []
    m = len(pattern)
    
    # Generate all rotations
    for i in range(m):
        rotation = pattern[i:] + pattern[:i]
        occurrences = rabin_karp(text, rotation)
        if occurrences:
            results.append((rotation, occurrences))
    
    return results

# APPLICATION 3: Longest Common Substring
def longest_common_substring(s1, s2):
    """Find longest common substring using Rabin-Karp"""
    n1, n2 = len(s1), len(s2)
    
    def check_length(length):
        """Check if common substring of given length exists"""
        if length == 0:
            return ""
        
        base, mod = 31, 10**9 + 7
        
        # Hashes of s1 substrings
        hashes1 = set()
        h = compute_hash(s1[:length], base, mod)
        hashes1.add(h)
        power = pow(base, length - 1, mod)
        
        for i in range(1, n1 - length + 1):
            h = (h - ord(s1[i - 1]) * power) % mod
            h = (h * base + ord(s1[i + length - 1])) % mod
            h = (h + mod) % mod
            hashes1.add(h)
        
        # Check s2 substrings
        h = compute_hash(s2[:length], base, mod)
        if h in hashes1:
            if s2[:length] in [s2[i:i+length] for i in range(n2 - length + 1)]:
                return s2[:length]
        
        for i in range(1, n2 - length + 1):
            h = (h - ord(s2[i - 1]) * power) % mod
            h = (h * base + s2[i + length - 1]) % mod
            h = (h + mod) % mod
            
            if h in hashes1:
                # Verify
                substr = s2[i:i + length]
                for j in range(n1 - length + 1):
                    if s1[j:j + length] == substr:
                        return substr
        
        return ""
    
    # Binary search for maximum length
    left, right = 0, min(n1, n2)
    result = ""
    
    while left <= right:
        mid = (left + right) // 2
        found = check_length(mid)
        if found:
            result = found
            left = mid + 1
        else:
            right = mid - 1
    
    return result

# APPLICATION 4: Search in 2D Grid
def search_2d_grid(grid, word):
    """Search for word in 2D grid using Rabin-Karp"""
    if not grid or not grid[0]:
        return []
    
    rows, cols = len(grid), len(grid[0])
    word_len = len(word)
    results = []
    
    # Convert grid to strings for each direction
    def get_horizontal_strings():
        strings = []
        for r in range(rows):
            for c in range(cols - word_len + 1):
                s = "".join(grid[r][c:c + word_len])
                strings.append((s, r, c, 'H'))
        return strings
    
    def get_vertical_strings():
        strings = []
        for c in range(cols):
            for r in range(rows - word_len + 1):
                s = "".join(grid[r + i][c] for i in range(word_len))
                strings.append((s, r, c, 'V'))
        return strings
    
    # Check all horizontal
    for s, r, c, direction in get_horizontal_strings():
        if rabin_karp(s, word):
            results.append((r, c, direction))
    
    # Check all vertical
    for s, r, c, direction in get_vertical_strings():
        if rabin_karp(s, word):
            results.append((r, c, direction))
    
    return results

# APPLICATION 5: Distinct Substrings
def count_distinct_substrings_rk(s):
    """Count distinct substrings using Rabin-Karp"""
    n = len(s)
    base, mod = 31, 10**9 + 7
    
    hashes = set()
    
    for length in range(1, n + 1):
        h = compute_hash(s[:length], base, mod)
        hashes.add(h)
        power = pow(base, length - 1, mod)
        
        for i in range(1, n - length + 1):
            h = (h - ord(s[i - 1]) * power) % mod
            h = (h * base + ord(s[i + length - 1])) % mod
            h = (h + mod) % mod
            hashes.add(h)
    
    return len(hashes)

# Test applications
print("Plagiarism detection:", detect_plagiarism(
    "This is a test document with some content",
    ["test document", "hello world"]
))

print("Longest common substring:", longest_common_substring("abcde", "abxde"))
print("Distinct substrings:", count_distinct_substrings_rk("abc"))
```

## 7. Practice Problems

```python
# PROBLEM 1: Find All Anagrams in a String
def find_anagrams(s, p):
    """Find all start indices of p's anagrams in s"""
    from collections import Counter
    
    n, m = len(s), len(p)
    if m > n:
        return []
    
    p_count = Counter(p)
    window_count = Counter(s[:m])
    
    result = []
    if window_count == p_count:
        result.append(0)
    
    for i in range(1, n - m + 1):
        # Remove left, add right
        window_count[s[i - 1]] -= 1
        if window_count[s[i - 1]] == 0:
            del window_count[s[i - 1]]
        window_count[s[i + m - 1]] += 1
        
        if window_count == p_count:
            result.append(i)
    
    return result

# PROBLEM 2: Longest Substring with At Most K Distinct Characters
def longest_substring_k_distinct(s, k):
    """Find longest substring with at most k distinct characters"""
    from collections import defaultdict
    
    n = len(s)
    if k == 0:
        return 0
    
    char_count = defaultdict(int)
    left = 0
    max_len = 0
    
    for right in range(n):
        char_count[s[right]] += 1
        
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len

# PROBLEM 3: Minimum Window Substring
def min_window(s, t):
    """Find minimum window in s that contains all characters of t"""
    from collections import Counter
    
    if not t or not s:
        return ""
    
    dict_t = Counter(t)
    required = len(dict_t)
    
    # Filter s and build tuples (char, index)
    filtered_s = [(c, i) for i, c in enumerate(s) if c in dict_t]
    
    l, r = 0, 0
    formed = 0
    window_counts = {}
    
    ans = float("inf"), None, None  # (window length, left, right)
    
    while r < len(filtered_s):
        character = filtered_s[r][0]
        window_counts[character] = window_counts.get(character, 0) + 1
        
        if window_counts[character] == dict_t[character]:
            formed += 1
        
        while l <= r and formed == required:
            character = filtered_s[l][0]
            
            end = filtered_s[r][1]
            start = filtered_s[l][1]
            
            if end - start + 1 < ans[0]:
                ans = (end - start + 1, start, end)
            
            window_counts[character] -= 1
            if window_counts[character] < dict_t[character]:
                formed -= 1
            
            l += 1
        
        r += 1
    
    return "" if ans[0] == float("inf") else s[ans[1]:ans[2] + 1]

# Test
print("Anagrams of 'ab' in 'abba':", find_anagrams("abba", "ab"))
print("Longest with 2 distinct in 'eceba':", longest_substring_k_distinct("eceba", 2))
print("Min window of 'ADOBECODEBANC' for 'ABC':", min_window("ADOBECODEBANC", "ABC"))
```

---

## Summary: Rabin-Karp Key Takeaways

```
  ┌──────────────────────────────────────────────────────────────────┐
  │              RABIN-KARP ALGORITHM CHEAT SHEET                    │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                  │
  │  Rolling Hash:                                                   │
  │  └── hash = s[0]*b^(m-1) + s[1]*b^(m-2) + ... + s[m-1]*b^0   │
  │  └── Slide window: remove leftmost, multiply by b, add right   │
  │  └── Always use MOD to prevent overflow                        │
  │                                                                  │
  │  Algorithm:                                                      │
  │  1. Compute pattern hash: O(m)                                 │
  │  2. Compute initial window hash: O(m)                          │
  │  3. Slide window, update hash in O(1) each step                │
  │  4. If hash matches, VERIFY (handle collisions!)               │
  │                                                                  │
  │  When to Use:                                                    │
  │  └── Multiple pattern search (best use case)                   │
  │  └── Plagiarism detection                                      │
  │  └── When O(1) space is needed (vs KMP's O(m))                │
  │  └── When average O(n+m) is acceptable                         │
  │                                                                  │
  │  Avoid When:                                                     │
  │  └── Guaranteed O(n+m) is required (use KMP)                   │
  │  └── High collision risk (many similar strings)                │
  │                                                                  │
  │  Pro Tips:                                                       │
  │  └── Choose base=31 or base=131, mod=10^9+7 or 10^9+9         │
  │  └── Use TWO mods to reduce collision probability to ~0       │
  │  └── Prefix hashes allow O(1) substring hash queries          │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
```
