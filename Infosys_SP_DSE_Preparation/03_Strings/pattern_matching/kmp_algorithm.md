# KMP (Knuth-Morris-Pratt) Algorithm

## 1. LPS (Longest Prefix Suffix) Array

```python
def compute_lps(pattern):
    """
    Compute the LPS (Longest Prefix Suffix) array
    lps[i] = length of longest proper prefix of pattern[0:i+1]
              which is also a suffix
    
    Time: O(m) where m is length of pattern
    Space: O(m)
    """
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps

# Step-by-step LPS computation
def compute_lps_verbose(pattern):
    """Verbose version showing step-by-step computation"""
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    steps = []
    
    steps.append(f"Pattern: {pattern}")
    steps.append(f"Initial LPS: {lps}")
    steps.append("")
    
    while i < m:
        steps.append(f"i={i}, length={length}, comparing pattern[{i}]='{pattern[i]}' with pattern[{length}]='{pattern[length]}'")
        
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            steps.append(f"  Match! length={length}, lps[{i}]={length}")
            i += 1
        else:
            if length != 0:
                steps.append(f"  No match, jumping length to lps[{length-1}]={lps[length-1]}")
                length = lps[length - 1]
            else:
                steps.append(f"  No match, length=0, lps[{i}]=0")
                lps[i] = 0
                i += 1
    
    steps.append(f"\nFinal LPS: {lps}")
    return lps, "\n".join(steps)

# Example
pattern = "ABABCABABD"
lps, verbose = compute_lps_verbose(pattern)
print(verbose)
print(f"\nLPS Array: {lps}")
# LPS: [0, 0, 1, 2, 0, 1, 2, 3, 4, 0]
```

## 2. KMP Search Algorithm

```python
def kmp_search(text, pattern):
    """
    KMP String Matching Algorithm
    Time: O(n + m) where n = len(text), m = len(pattern)
    Space: O(m) for LPS array
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return []
    
    # Compute LPS array
    lps = compute_lps(pattern)
    
    result = []
    i = 0  # index for text
    j = 0  # index for pattern
    
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        
        if j == m:
            result.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return result

# Example
text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
print(f"Pattern found at indices: {kmp_search(text, pattern)}")
# [10]
```

## 3. KMP Step-by-Step Visualization

```python
def kmp_search_verbose(text, pattern):
    """KMP with step-by-step visualization"""
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    
    result = []
    i = j = 0
    steps = []
    
    steps.append(f"Text:    {text}")
    steps.append(f"Pattern: {pattern}")
    steps.append(f"LPS:     {lps}")
    steps.append("")
    
    while i < n:
        # Show current state
        pointer_text = " " * i + "^"
        pointer_pattern = " " * (i - j) + "^"
        steps.append(f"Text:    {text}")
        steps.append(f"         {pointer_text}")
        steps.append(f"Pattern: {' ' * (i - j) + pattern}")
        steps.append(f"         {' ' * (i - j) + pointer_pattern}")
        
        if text[i] == pattern[j]:
            steps.append(f"  Match: text[{i}]='{text[i]}' == pattern[{j}]='{pattern[j]}'")
            i += 1
            j += 1
        else:
            steps.append(f"  Mismatch: text[{i}]='{text[i]}' != pattern[{j}]='{pattern[j]}'")
            if j != 0:
                steps.append(f"  Jump j from {j} to lps[{j-1}]={lps[j-1]}")
                j = lps[j - 1]
            else:
                steps.append(f"  j=0, move i forward")
                i += 1
        
        if j == m:
            steps.append(f"  *** Pattern found at index {i - j}! ***")
            result.append(i - j)
            j = lps[j - 1]
        
        steps.append("")
    
    return result, "\n".join(steps)

# Example
text = "AABAACAADAABAAABAA"
pattern = "AABA"
result, verbose = kmp_search_verbose(text, pattern)
print(verbose)
print(f"Pattern found at indices: {result}")
```

## 4. KMP Variants

```python
# VARIANT 1: Count Occurrences
def kmp_count_occurrences(text, pattern):
    """Count how many times pattern appears in text"""
    return len(kmp_search(text, pattern))

# VARIANT 2: First Occurrence
def kmp_first_occurrence(text, pattern):
    """Find first occurrence of pattern in text"""
    result = kmp_search(text, pattern)
    return result[0] if result else -1

# VARIANT 3: Find All Overlapping Occurrences
def kmp_find_all_overlapping(text, pattern):
    """Find all overlapping occurrences of pattern"""
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    
    result = []
    i = j = 0
    
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        
        if j == m:
            result.append(i - j)
            j = lps[j - 1]  # Allow overlapping
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return result

# VARIANT 4: Search in Circular String
def kmp_search_circular(text, pattern):
    """Search pattern in circular text"""
    # Double the text to handle circular nature
    doubled_text = text + text
    return kmp_search(doubled_text, pattern[:len(pattern)])

# VARIANT 5: Longest Prefix Which is Also Suffix
def longest_prefix_suffix(s):
    """Find longest prefix which is also suffix"""
    lps = compute_lps(s)
    return lps[-1]

# Examples
text = "AAAAABAAABA"
pattern = "AAA"
print(f"Count: {kmp_count_occurrences(text, pattern)}")  # 4
print(f"All overlapping: {kmp_find_all_overlapping(text, pattern)}")  # [0, 1, 2, 7]

print(f"Longest prefix suffix of 'ABCABC': {longest_prefix_suffix('ABCABC')}")  # 3
```

## 5. Applications

```python
# APPLICATION 1: Find Pattern in Text
def find_pattern(text, pattern):
    """Basic pattern finding using KMP"""
    return kmp_search(text, pattern)

# APPLICATION 2: Count Occurrences of Pattern
def count_pattern_occurrences(text, pattern):
    """Count occurrences using KMP"""
    return kmp_count_occurrences(text, pattern)

# APPLICATION 3: Repeated Substring Pattern
def has_repeated_substring_pattern(s):
    """
    Check if string can be formed by repeating a substring
    Uses KMP: if lps[n-1] > 0 and n % (n - lps[n-1]) == 0
    """
    n = len(s)
    if n == 0:
        return False
    
    lps = compute_lps(s)
    last_lps = lps[n - 1]
    
    # Check if pattern repeats
    if last_lps > 0 and n % (n - last_lps) == 0:
        return True
    return False

# APPLICATION 4: Minimum Repeated Pattern
def min_repeated_pattern(s):
    """Find minimum pattern that repeats to form s"""
    n = len(s)
    lps = compute_lps(s)
    last_lps = lps[n - 1]
    
    if last_lps > 0 and n % (n - last_lps) == 0:
        return s[:n - last_lps]
    return s

# APPLICATION 5: Period of String
def string_period(s):
    """Find the smallest period of the string"""
    n = len(s)
    lps = compute_lps(s)
    period = n - lps[n - 1]
    
    if n % period == 0:
        return period
    return n

# APPLICATION 6: Search Multiple Patterns
def kmp_search_multiple(text, patterns):
    """Search for multiple patterns in text"""
    results = {}
    for pattern in patterns:
        occurrences = kmp_search(text, pattern)
        if occurrences:
            results[pattern] = occurrences
    return results

# Examples
print(has_repeated_substring_pattern("abcabc"))     # True
print(has_repeated_substring_pattern("abc"))        # False
print(min_repeated_pattern("abcabcabc"))            # "abc"
print(string_period("abcabc"))                      # 3
print(string_period("abc"))                         # 3

text = "ababcababcabc"
patterns = ["abc", "bab", "cab"]
print(kmp_search_multiple(text, patterns))
```

## 6. Practice Problems

```python
# PROBLEM 1: Implement strStr() (LeetCode 28)
def str_str(haystack, needle):
    """Return index of first occurrence of needle in haystack"""
    return kmp_first_occurrence(haystack, needle)

# PROBLEM 2: Repeated Substring Pattern (LeetCode 459)
def repeated_substring_pattern(s):
    return has_repeated_substring_pattern(s)

# PROBLEM 3: Longest Happy Prefix (LeetCode 1392)
def longest_happy_prefix(s):
    """Find longest prefix which is also suffix (not whole string)"""
    n = len(s)
    lps = compute_lps(s)
    return s[:lps[n - 1]]

# PROBLEM 4: Check If String Contains All Binary Codes of Size K
def has_all_codes(s, k):
    """Check if s contains all 2^k binary codes of length k"""
    needed = 1 << k  # 2^k
    seen = set()
    
    # Use KMP-style rolling
    for i in range(len(s) - k + 1):
        code = s[i:i + k]
        if code not in seen:
            seen.add(code)
            if len(seen) == needed:
                return True
    
    return False

# PROBLEM 5: Find the Index of the First Occurrence (with wildcards)
def kmp_with_wildcards(text, pattern):
    """KMP variant handling '.' as wildcard"""
    n, m = len(text), len(pattern)
    
    def compute_lps_wildcard(p):
        m = len(p)
        lps = [0] * m
        length = 0
        i = 1
        while i < m:
            if p[i] == '.' or p[i] == p[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    lps = compute_lps_wildcard(pattern)
    result = []
    i = j = 0
    
    while i < n:
        if pattern[j] == '.' or text[i] == pattern[j]:
            i += 1
            j += 1
        
        if j == m:
            result.append(i - j)
            j = lps[j - 1]
        elif i < n and (pattern[j] != '.' and text[i] != pattern[j]):
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return result

# Test all problems
print("strStr('hello', 'll'):", str_str("hello", "ll"))  # 2
print("repeatedSubstringPattern('abab'):", repeated_substring_pattern("abab"))  # True
print("longestHappyPrefix('level'):", longest_happy_prefix("level"))  # "le"
print("hasAllCodes('00110110', 2):", has_all_codes("00110110", 2))  # True
print("kmpWithWildcards('ab', '.b'):", kmp_with_wildcards("ab", ".b"))  # [0]
```
