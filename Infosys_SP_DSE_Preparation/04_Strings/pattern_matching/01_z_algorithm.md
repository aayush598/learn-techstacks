# Z Algorithm

## What is the Z Algorithm?

The Z Algorithm computes the **Z-array**: for each position i, Z[i] = length of the **longest substring starting at i** that is also a **prefix** of the string.

```
  Z-array Example: s = "aababcabd"

  Index: 0  1  2  3  4  5  6  7  8
  Char:  a  a  b  a  b  c  a  b  d
  Z:     0  1  0  2  1  0  2  1  0

  Z[0] = 0 (by convention, or n)
  Z[1] = 1 because "a" at index 1 matches prefix "a"
  Z[3] = 2 because "ab" at index 3 matches prefix "ab"
  Z[6] = 2 because "ab" at index 6 matches prefix "ab"

  Key Insight: Z[i] >= m means the pattern matches at position i!
```

## How Z-Array Differs from LPS

```
  ┌─────────────────────────────────────────────────────────┐
  │  LPS (for KMP):                                         │
  │  lps[i] = longest prefix of pattern[0..i] that is      │
  │           also a suffix of pattern[0..i]                │
  │  (looks INSIDE the pattern at each position)            │
  │                                                         │
  │  Z-array:                                               │
  │  z[i] = longest substring starting at position i       │
  │         that matches the PREFIX of the string           │
  │  (compares each position against the beginning)         │
  └─────────────────────────────────────────────────────────┘

  Example: s = "aabxaabxcaa"

  LPS approach (self-referencing):
    At position 4: "aabxa" - what prefix = suffix? "a" -> lps=1

  Z-array approach (prefix-referencing):
    At position 4: "aabxcaa" compared to prefix "aabxaabxcaa"
    "aab" matches prefix "aab" -> z[4] = 2... wait, let me check.
    Actually at position 4: s[4..] = "xaabxcaa", compare with prefix
    s[0..] = "aabxaabxcaa" -> x!=a -> z[4] = 0

  Z-array is easier to understand and implement!
```

## Algorithm Comparison

| Algorithm    | Time | Space | Key Feature                    |
|-------------|------|-------|--------------------------------|
| KMP         | O(n+m)| O(m) | LPS-based, no extra space     |
| Z-Algorithm | O(n+m)| O(n+m)| Z-array based, simpler code  |
| Rabin-Karp  | O(n+m)| O(1) | Hash-based, good for multi-pattern|

```
  ┌──────────────────────────────────────────────────────────┐
  │           Z-ALGORITHM PROBLEM DECISION GUIDE             │
  ├──────────────────────────────────────────────────────────┤
  │                                                          │
  │  Simple pattern matching?                                │
  │  └── Z-Algorithm: combined = pattern + '$' + text       │
  │      Any z[i] >= m means match at position i-m-1        │
  │                                                          │
  │  Count distinct substrings?                              │
  │  └── total = n*(n+1)/2 - sum(z[i])                      │
  │                                                          │
  │  Find string period?                                     │
  │  └── If i + z[i] == n, period = i                       │
  │                                                          │
  │  Need LPS for KMP?                                       │
  │  └── Compute Z-array of pattern + '$' + pattern         │
  │      LPS[i] = z[m+1+i] for pattern of length m         │
  │                                                          │
  └──────────────────────────────────────────────────────────┘
```

---

## 1. Z-Array Computation

```python
def compute_z_array(s):
    """
    Compute Z-array where Z[i] = length of longest substring
    starting from i that is also a prefix of s
    
    Z[0] is always 0 (or n by convention, but we use 0)
    
    Time: O(n)
    Space: O(n)
    """
    n = len(s)
    z = [0] * n
    l, r = 0, 0
    
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    
    return z

# Step-by-step Z-array computation
def compute_z_array_verbose(s):
    """Verbose version showing step-by-step computation"""
    n = len(s)
    z = [0] * n
    l, r = 0, 0
    steps = []
    
    steps.append(f"String: {s}")
    steps.append(f"Initial: z = {z}, l = {l}, r = {r}")
    steps.append("")
    
    for i in range(1, n):
        steps.append(f"Processing i={i}:")
        
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
            steps.append(f"  Inside box: z[{i}] = min({r - i + 1}, z[{i - l}]={z[i - l]}) = {z[i]}")
        
        # Extend the match
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            steps.append(f"  Comparing s[{z[i]}]='{s[z[i]]}' with s[{i + z[i]}]='{s[i + z[i]]}' - Match!")
            z[i] += 1
        
        if z[i] > 0:
            steps.append(f"  After extension: z[{i}] = {z[i]}")
        
        # Update box
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
            steps.append(f"  New box: l={l}, r={r}")
        
        steps.append(f"  z = {z}")
        steps.append("")
    
    return z, "\n".join(steps)

# Example
s = "aabaabcabd"
z, verbose = compute_z_array_verbose(s)
print(verbose)
print(f"\nZ-array: {z}")
# Z-array: [0, 1, 0, 2, 1, 0, 0, 2, 1, 0]
```

### Visual: Z-Array Computation with "Box" (L,R Window)

```
  s = "aabaabcabd"

  The algorithm maintains a "box" [L, R] representing
  the rightmost Z-box found so far.

  Index:  0  1  2  3  4  5  6  7  8  9
  Char:   a  a  b  a  a  b  c  a  b  d
  Z:      0  1  0  2  1  0  0  2  1  0

  ┌─────────────────────────────────────────────────────────┐
  │ i=1: z[1]=1 (extend match from prefix)                  │
  │      New box: L=1, R=1                                  │
  │                                                         │
  │ i=2: Inside box [1,1]? No (i > R)                      │
  │      Try matching from scratch: s[0]='a' != s[2]='b'  │
  │      z[2] = 0                                           │
  │                                                         │
  │ i=3: Inside box? No. Match from scratch:               │
  │      s[0]='a'==s[3]='a', s[1]='a'==s[4]='a'          │
  │      s[2]='b'==s[5]='b' -> z[3]=3, but wait...        │
  │      Actually s[2]='b'==s[5]='b' -> z[3]=3?           │
  │      New box: L=3, R=5                                  │
  │                                                         │
  │ i=4: Inside box [3,5]? YES! (i=4 <= R=5)              │
  │      z[4] = min(R-i+1, z[i-L]) = min(5-4+1, z[4-3])  │
  │      z[4] = min(2, z[1]) = min(2, 1) = 1              │
  │      Try extending from z[4]=1... s[1]='a'!=s[5]='b'  │
  │      z[4] stays at 1                                     │
  │                                                         │
  │ Continue for all i...                                    │
  └─────────────────────────────────────────────────────────┘
```

## 2. Pattern Matching Using Z Algorithm

```python
def z_algorithm_search(text, pattern):
    """
    Pattern matching using Z algorithm
    Time: O(n + m)
    Space: O(n + m)
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return []
    
    # Create concatenated string: pattern + '$' + text
    combined = pattern + '$' + text
    
    # Compute Z-array
    z = compute_z_array(combined)
    
    # Find matches: Z[i] >= m means pattern found at position i - m - 1 in text
    result = []
    for i in range(m + 1, len(combined)):
        if z[i] >= m:
            result.append(i - m - 1)
    
    return result

# Example
text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
print(f"Pattern found at: {z_algorithm_search(text, pattern)}")
```

### Visual: Z-Algorithm Pattern Matching

```
  text = "ABABDABACDABABCABAB"
  pattern = "ABABCABAB" (m=9)

  Combined string: "ABABCABAB$ABABDABACDABABCABAB"
                     ─────────  ──────────────────
                      pattern         text

  Compute Z-array of combined string:
  Combined: A B A B C A B A B $ A B A B D A B A C D A B A B C A B A B
  Z:        0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                                      ^
                                      Z[10]=4 means "ABAB" matches prefix
                                      But we need Z[i] >= 9 for full match

  For each position i in text section (i >= m+1):
    If z[i] >= m (pattern length), match found at position i-m-1

  ┌──────────────────────────────────────────────────────┐
  │ i=10: z[10]=4 < 9 -> no full match                   │
  │ i=11: z[11]=0 < 9 -> no match                        │
  │ ...                                                   │
  │ i=19: z[19]=9 >= 9 -> MATCH at text[19-9-1] = [10]  │
  └──────────────────────────────────────────────────────┘
```

## 3. Z Algorithm Step-by-Step Visualization

```python
def z_search_verbose(text, pattern):
    """Z algorithm with step-by-step visualization"""
    n, m = len(text), len(pattern)
    
    combined = pattern + '$' + text
    z = compute_z_array(combined)
    
    result = []
    steps = []
    
    steps.append(f"Pattern: {pattern}")
    steps.append(f"Text: {text}")
    steps.append(f"Combined: {combined}")
    steps.append(f"Z-array: {z}")
    steps.append("")
    
    for i in range(m + 1, len(combined)):
        if z[i] >= m:
            pos = i - m - 1
            result.append(pos)
            steps.append(f"Z[{i}]={z[i]} >= {m} => Pattern found at text[{pos}]")
        else:
            steps.append(f"Z[{i}]={z[i]} < {m} => No match at text[{i - m - 1}]")
    
    steps.append(f"\nAll occurrences: {result}")
    return result, "\n".join(steps)

# Example
text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
result, verbose = z_search_verbose(text, pattern)
print(verbose)
```

## 4. Z Algorithm Applications

```python
# APPLICATION 1: String Matching
def string_match_z(text, pattern):
    """Basic string matching using Z algorithm"""
    return z_algorithm_search(text, pattern)

# APPLICATION 2: Find All Occurrences
def find_all_occurrences_z(text, pattern):
    """Find all occurrences of pattern in text"""
    return z_algorithm_search(text, pattern)

# APPLICATION 3: Concatenation of All Words
def find_concatenation(text, words):
    """Find all indices where concatenation of words starts"""
    if not words or not words[0]:
        return []
    
    word_len = len(words[0])
    total_len = word_len * len(words)
    
    from collections import Counter
    word_count = Counter(words)
    
    result = []
    
    for i in range(len(text) - total_len + 1):
        # Check if this position is a valid concatenation
        seen = {}
        valid = True
        
        for j in range(0, total_len, word_len):
            word = text[i + j:i + j + word_len]
            seen[word] = seen.get(word, 0) + 1
            
            if seen[word] > word_count.get(word, 0):
                valid = False
                break
        
        if valid and seen == word_count:
            result.append(i)
    
    return result

# APPLICATION 4: Longest Common Substring using Z
def longest_common_substring_z(s1, s2):
    """Find longest common substring using Z algorithm"""
    n1, n2 = len(s1), len(s2)
    
    # For each position in s1, compute Z-array with s2 as pattern
    max_len = 0
    end_pos = 0
    
    for i in range(n1):
        combined = s2 + '$' + s1[i:]
        z = compute_z_array(combined)
        
        for j in range(n2 + 1, len(combined)):
            if z[j] > max_len:
                max_len = z[j]
                end_pos = i + j - n2 - 1
    
    if max_len == 0:
        return ""
    return s1[end_pos - max_len + 1:end_pos + 1]

# APPLICATION 5: Count Distinct Substrings
def count_distinct_substrings_z(s):
    """Count distinct substrings using Z algorithm"""
    n = len(s)
    total = n * (n + 1) // 2  # Total possible substrings
    
    # Subtract common prefixes
    z = compute_z_array(s)
    for i in range(n):
        total -= z[i]
    
    return total

# APPLICATION 6: Longest Prefix which is also Suffix
def longest_prefix_suffix_z(s):
    """Find longest prefix which is also suffix using Z"""
    z = compute_z_array(s)
    n = len(s)
    
    for i in range(n - 1, 0, -1):
        if z[i] == n - i:
            return s[:z[i]]
    return ""

# APPLICATION 7: Period of String
def string_period_z(s):
    """Find smallest period of string using Z"""
    n = len(s)
    z = compute_z_array(s)
    
    for i in range(1, n):
        if i + z[i] == n:
            return i
    return n

# Test applications
print("String match:", string_match_z("ABABDABACDABABCABAB", "ABABCABAB"))
print("Find concatenation:", find_concatenation("barfoofoobarthe", ["foo", "bar", "the"]))
print("Longest common substring:", longest_common_substring_z("abcdef", "xbcdefx"))
print("Distinct substrings:", count_distinct_substrings_z("abc"))
print("Longest prefix suffix:", longest_prefix_suffix_z("abcabc"))
print("String period:", string_period_z("abcabc"))
```

## 5. Comparison with KMP and Rabin-Karp

```python
"""
COMPARISON OF STRING MATCHING ALGORITHMS:

KMP (Knuth-Morris-Pratt):
- Time: O(n + m)
- Space: O(m)
- Preprocessing: Compute LPS array in O(m)
- Best for: Single pattern matching
- Pros: No hash collisions, guaranteed O(n+m)
- Cons: More complex to implement

Rabin-Karp:
- Time: O(n + m) average, O(n*m) worst
- Space: O(1)
- Preprocessing: Compute pattern hash in O(m)
- Best for: Multiple pattern matching, plagiarism detection
- Pros: Simple, good for multiple patterns
- Cons: Hash collisions, worst case O(n*m)

Z Algorithm:
- Time: O(n + m)
- Space: O(n + m)
- Preprocessing: Compute Z-array in O(n + m)
- Best for: Pattern matching, finding all occurrences
- Pros: Simple implementation, same complexity as KMP
- Cons: Extra space for combined string

WHEN TO USE WHICH:
1. Single pattern, guaranteed performance: KMP
2. Multiple patterns: Rabin-Karp
3. Simple implementation needed: Z Algorithm
4. Need to find all occurrences: Z Algorithm or KMP
5. Plagiarism detection: Rabin-Karp
"""
```

## 6. Practice Problems

```python
# PROBLEM 1: Implement Z-function
def z_function(s):
    """Standard Z-function implementation"""
    return compute_z_array(s)

# PROBLEM 2: Search Pattern (LeetCode)
def search_pattern(text, pattern):
    """Find all occurrences of pattern in text"""
    return z_algorithm_search(text, pattern)

# PROBLEM 3: Longest Substring Without Repeating Characters
def longest_unique_substring(s):
    """Find length of longest substring without repeating characters"""
    char_index = {}
    max_len = 0
    left = 0
    
    for right, c in enumerate(s):
        if c in char_index and char_index[c] >= left:
            left = char_index[c] + 1
        char_index[c] = right
        max_len = max(max_len, right - left + 1)
    
    return max_len

# PROBLEM 4: Minimum Window Substring
def min_window_substring(s, t):
    """Find minimum window in s containing all characters of t"""
    from collections import Counter
    
    if not s or not t:
        return ""
    
    dict_t = Counter(t)
    required = len(dict_t)
    
    filtered = [(c, i) for i, c in enumerate(s) if c in dict_t]
    l, r = 0, 0
    formed = 0
    window = {}
    
    ans = (float("inf"), 0, 0)
    
    while r < len(filtered):
        char = filtered[r][0]
        window[char] = window.get(char, 0) + 1
        
        if window[char] == dict_t[char]:
            formed += 1
        
        while l <= r and formed == required:
            char = filtered[l][0]
            end = filtered[r][1]
            start = filtered[l][1]
            
            if end - start + 1 < ans[0]:
                ans = (end - start + 1, start, end)
            
            window[char] -= 1
            if window[char] < dict_t[char]:
                formed -= 1
            l += 1
        
        r += 1
    
    return "" if ans[0] == float("inf") else s[ans[1]:ans[2] + 1]

# PROBLEM 5: Longest Duplicate Substring
def longest_duplicate_substring_z(s):
    """Find longest duplicate substring using Z algorithm"""
    n = len(s)
    
    def check_length(length):
        if length == 0:
            return ""
        
        seen = {}
        for i in range(n - length + 1):
            substr = s[i:i + length]
            if substr in seen:
                return substr
            seen[substr] = i
        return ""
    
    left, right = 1, n - 1
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

# Test
print("Z-function of 'aabaaab':", z_function("aabaaab"))
print("Longest unique substring 'abcabcbb':", longest_unique_substring("abcabcbb"))
print("Min window 'ADOBECODEBANC' for 'ABC':", min_window_substring("ADOBECODEBANC", "ABC"))
print("Longest duplicate in 'banana':", longest_duplicate_substring_z("banana"))
```

---

## Summary: Z Algorithm Key Takeaways

```
  ┌──────────────────────────────────────────────────────────────────┐
  │               Z ALGORITHM CHEAT SHEET                            │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                  │
  │  Z-array Definition:                                             │
  │  └── z[i] = length of longest substring starting at i that    │
  │             matches the PREFIX of the string                    │
  │  └── z[0] = 0 (or n by convention)                             │
  │                                                                  │
  │  Algorithm:                                                      │
  │  └── Maintain box [L, R] = rightmost Z-box                    │
  │  └── If i inside box: z[i] = min(R-i+1, z[i-L]) (copy)       │
  │  └── Then try extending: while match, z[i]++                  │
  │  └── Update box if match extends beyond R                      │
  │                                                                  │
  │  Pattern Matching:                                               │
  │  └── Create: pattern + '$' + text                              │
  │  └── Compute Z-array of combined string                        │
  │  └── Match at position i if z[i] >= len(pattern)              │
  │  └── Position in original text = i - len(pattern) - 1         │
  │                                                                  │
  │  Distinct Substrings:                                            │
  │  └── total = n*(n+1)/2 - sum(z[i])                            │
  │  └── Each z[i] value represents i duplicated substrings       │
  │                                                                  │
  │  String Period:                                                  │
  │  └── If i + z[i] == n, then i is a period                     │
  │  └── Example: "abcabc" has period 3 (z[3]=3, 3+3=6)          │
  │                                                                  │
  │  vs KMP:                                                         │
  │  └── Same time complexity O(n+m)                               │
  │  └── Z is simpler to code                                       │
  │  └── KMP uses less space O(m) vs O(n+m)                       │
  │  └── Z-array of pattern+'$'+pattern gives LPS array           │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
```
