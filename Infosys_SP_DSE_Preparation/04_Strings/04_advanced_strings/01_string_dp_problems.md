# String DP Problems

## Overview: String DP Problem Categories

```
  ┌──────────────────────────────────────────────────────────────────┐
  │               STRING DP PROBLEM FAMILY TREE                     │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                  │
  │  Subsequence Problems (characters can be non-contiguous)        │
  │  ├── Longest Common Subsequence (LCS)                           │
  │  ├── Edit Distance (Levenshtein)                                │
  │  ├── Longest Palindromic Subsequence                           │
  │  ├── Shortest Common Supersequence                              │
  │  └── Distinct Subsequences                                      │
  │                                                                  │
  │  Substring Problems (characters must be contiguous)             │
  │  ├── Longest Common Substring                                   │
  │  ├── Longest Palindromic Substring                              │
  │  └── Longest Repeating Substring                                │
  │                                                                  │
  │  Pattern Matching (with wildcards/regex)                        │
  │  ├── Wildcard Matching (*, ?)                                   │
  │  └── Regex Matching (.*, a*)                                    │
  │                                                                  │
  │  Interleaving / Combining                                       │
  │  └── Interleaving String                                        │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
```

## Complexity Cheat Sheet

| Problem                    | Time    | Space   | Key Recurrence                                      |
|---------------------------|---------|---------|-----------------------------------------------------|
| LCS                       | O(m*n)  | O(m*n)  | dp[i][j] = dp[i-1][j-1]+1 if match, else max      |
| Edit Distance             | O(m*n)  | O(m*n)  | dp[i][j] = 1+min(del,ins,rep) if mismatch          |
| Longest Common Substring  | O(m*n)  | O(m*n)  | dp[i][j] = dp[i-1][j-1]+1 if match, else 0         |
| Distinct Subsequences     | O(m*n)  | O(m*n)  | dp[i][j] = dp[i-1][j-1]+dp[i-1][j] if match        |
| Wildcard Matching         | O(m*n)  | O(m*n)  | * matches zero or more; ? matches exactly one       |
| Regex Matching            | O(m*n)  | O(m*n)  | a* matches zero or more of 'a'                      |
| Interleaving              | O(m*n)  | O(m*n)  | dp[i][j] = from s1 or s2 matching s3               |

## Quick Reference: When to Use What

```
  ┌──────────────────────────────────────────────────────────────┐
  │          STRING DP PROBLEM DECISION GUIDE                    │
  ├──────────────────────────────────────────────────────────────┤
  │                                                              │
  │  Compare two strings?                                        │
  │  ├── Both strings, find common parts -> LCS / Substring     │
  │  ├── Transform one to other -> Edit Distance                 │
  │  └── Combine both -> Shortest Common Supersequence           │
  │                                                              │
  │  Single string properties?                                   │
  │  ├── Palindrome related -> LPS / Palindromic Substring      │
  │  └── Count subsequences -> Distinct Subsequences            │
  │                                                              │
  │  Pattern matching with wildcards?                            │
  │  ├── '*' and '?' only -> Wildcard Matching (LeetCode 44)    │
  │  └── '.' and '*'   -> Regex Matching (LeetCode 10)          │
  │                                                              │
  │  Three strings involved?                                     │
  │  └── Interleaving String (LeetCode 97)                       │
  │                                                              │
  │  Space optimization needed?                                  │
  │  └── Most can be reduced from O(m*n) to O(min(m,n))         │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘
```

---

## 1. Longest Common Subsequence (LeetCode 1143)

```python
def longest_common_subsequence(text1, text2):
    """
    Find length of longest common subsequence
    Time: O(m * n)
    Space: O(m * n)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]

def lcs_optimized(text1, text2):
    """Space-optimized LCS"""
    m, n = len(text1), len(text2)
    prev = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    
    return prev[n]

# Test
print(longest_common_subsequence("abcde", "ace"))  # 3
print(lcs_optimized("abc", "abc"))                  # 3
```

### Visual: LCS DP Table

```
  text1 = "abcde", text2 = "ace"

       ""  a   c   e
    ┌───┬───┬───┬───┐
 "" │ 0 │ 0 │ 0 │ 0 │
    ├───┼───┼───┼───┤
 a  │ 0 │ 1 │ 1 │ 1 │  <- 'a'=='a': take diagonal+1
    ├───┼───┼───┼───┤
 b  │ 0 │ 1 │ 1 │ 1 │  <- 'b'!='c': take max(top,left)
    ├───┼───┼───┼───┤
 c  │ 0 │ 1 │ 2 │ 2 │  <- 'c'=='c': take diagonal+1
    ├───┼───┼───┼───┤
 d  │ 0 │ 1 │ 2 │ 2 │  <- 'd'!='e': take max(top,left)
    ├───┼───┼───┼───┤
 e  │ 0 │ 1 │ 2 │ 3 │  <- 'e'=='e': take diagonal+1
    └───┴───┴───┴───┘

  Answer: dp[5][3] = 3 (LCS = "ace")

  Recurrence:
  ┌─────────────────────────────────────────────────┐
  │ if text1[i-1] == text2[j-1]:                    │
  │     dp[i][j] = dp[i-1][j-1] + 1  (extend LCS)  │
  │ else:                                            │
  │     dp[i][j] = max(dp[i-1][j], dp[i][j-1])      │
  │     (skip one char from either string)           │
  └─────────────────────────────────────────────────┘
```

## 2. Edit Distance (Levenshtein Distance - LeetCode 72)

```python
def min_distance(word1, word2):
    """
    Minimum operations to convert word1 to word2
    Operations: insert, delete, replace
    Time: O(m * n)
    Space: O(m * n)
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Replace
                )
    
    return dp[m][n]

def min_distance_optimized(word1, word2):
    """Space-optimized edit distance"""
    m, n = len(word1), len(word2)
    prev = list(range(n + 1))
    
    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev = curr
    
    return prev[n]

# Test
print(min_distance("horse", "ros"))       # 3
print(min_distance_optimized("intention", "execution"))  # 5
```

### Visual: Edit Distance DP Table

```
  word1 = "horse", word2 = "ros"

         ""   r    o    s
      ┌────┬────┬────┬────┐
   "" │  0 │  1 │  2 │  3 │
      ├────┼────┼────┼────┤
   h  │  1 │  1 │  2 │  3 │
      ├────┼────┼────┼────┤
   o  │  2 │  2 │  1 │  2 │
      ├────┼────┼────┼────┤
   r  │  3 │  2 │  2 │  2 │
      ├────┼────┼────┼────┤
   s  │  4 │  3 │  3 │  2 │
      ├────┼────┼────┼────┤
   e  │  5 │  4 │  4 │  3 │
      └────┴────┴────┴────┘

  Three operations at each cell:
  ┌─────────────────────────────────────────────────────┐
  │ Delete:  dp[i-1][j] + 1   (remove char from w1)    │
  │ Insert:  dp[i][j-1] + 1   (add char to w1)         │
  │ Replace: dp[i-1][j-1] + 0 (if same) or + 1         │
  │                                                      │
  │ Take the MINIMUM of these three options.             │
  └─────────────────────────────────────────────────────┘

  Edit operations for "horse" -> "ros":
  1. h->r: replace h with r    "rorse"
  2. o->o: no change            "rorse"
  3. r->s: replace r with s    "rosse"
  4. Delete e                   "ross"
  5. Delete s                   "ros"
  Wait, that's not optimal. Let's trace the DP:
  dp[5][3] = 3: "horse" -> "orse" -> "ros" -> "ros"
  Actually: horse -> rorse (insert r) -> ros (delete r,o) -> ros (delete e) -- 3 operations
```

## 3. Longest Common Substring (LeetCode 718)

```python
def longest_common_substring(s1, s2):
    """
    Find length of longest common substring
    Time: O(m * n)
    Space: O(m * n)
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_len = max(max_len, dp[i][j])
            else:
                dp[i][j] = 0
    
    return max_len

def longest_common_substring_with_position(s1, s2):
    """Returns length and ending position"""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0
    end_pos = 0
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_pos = i
    
    return max_len, s1[end_pos - max_len:end_pos]

# Test
print(longest_common_substring("abcde", "abxde"))  # 2 ("de")
length, substr = longest_common_substring_with_position("GeeksforGeeks", "GeeksQuiz")
print(f"Length: {length}, Substring: {substr}")
```

### Visual: Longest Common Substring DP Table

```
  s1 = "abcde", s2 = "abxde"

       ""  a   b   x   d   e
    ┌───┬───┬───┬───┬───┬───┐
 "" │ 0 │ 0 │ 0 │ 0 │ 0 │ 0 │
    ├───┼───┼───┼───┼───┼───┤
 a  │ 0 │ 1 │ 0 │ 0 │ 0 │ 0 │  <- 'a'=='a': 0+1=1
    ├───┼───┼───┼───┼───┼───┤
 b  │ 0 │ 0 │ 2 │ 0 │ 0 │ 0 │  <- 'b'=='b': 1+1=2
    ├───┼───┼───┼───┼───┼───┤
 c  │ 0 │ 0 │ 0 │ 0 │ 0 │ 0 │  <- 'c'!='x': reset to 0!
    ├───┼───┼───┼───┼───┼───┤
 d  │ 0 │ 0 │ 0 │ 0 │ 1 │ 0 │  <- 'd'=='d': 0+1=1
    ├───┼───┼───┼───┼───┼───┤
 e  │ 0 │ 0 │ 0 │ 0 │ 0 │ 2 │  <- 'e'=='e': 1+1=2
    └───┴───┴───┴───┴───┴───┘

  max(dp[i][j]) = 2 (substring "de" at end of both strings)

  Key difference from LCS:
  ┌──────────────────────────────────────────────────────────┐
  │ LCS:    dp[i][j] = dp[i-1][j-1] + 1 (when match)       │
  │ Substring: dp[i][j] = dp[i-1][j-1] + 1 (when match)    │
  │              dp[i][j] = 0 (when NO match, reset!)       │
  │                                                          │
  │ Substring requires CONTIGUOUS match, so mismatch = 0    │
  └──────────────────────────────────────────────────────────┘
```

## 4. Longest Repeating Subsequence (LeetCode)

```python
def longest_repeating_subsequence(s):
    """
    Find longest subsequence that appears at least twice
    Time: O(n^2)
    Space: O(n^2)
    """
    n = len(s)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if s[i - 1] == s[j - 1] and i != j:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[n][n]

# Test
print(longest_repeating_subsequence("aab"))   # 1
print(longest_repeating_subsequence("aabebcdd"))  # 3 ("abd")
```

## 5. Shortest Common Supersequence (LeetCode 1092)

```python
def shortest_common_supersequence(str1, str2):
    """
    Find shortest string that has both str1 and str2 as subsequences
    Time: O(m * n)
    Space: O(m * n)
    """
    m, n = len(str1), len(str2)
    
    # First compute LCS
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Backtrack to build SCS
    i, j = m, n
    result = []
    
    while i > 0 and j > 0:
        if str1[i - 1] == str2[j - 1]:
            result.append(str1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            result.append(str1[i - 1])
            i -= 1
        else:
            result.append(str2[j - 1])
            j -= 1
    
    while i > 0:
        result.append(str1[i - 1])
        i -= 1
    
    while j > 0:
        result.append(str2[j - 1])
        j -= 1
    
    return ''.join(result[::-1])

# Test
print(shortest_common_supersequence("abac", "cab"))  # "cabac"
print(shortest_common_supersequence("abc", "def"))   # "abcdef"
```

### Visual: Shortest Common Supersequence

```
  str1 = "abac", str2 = "cab"

  Step 1: Find LCS first
  LCS("abac", "cab") = "ab" (or "ac")

  Step 2: Build SCS by merging LCS chars and adding remaining

  Backtrack through LCS DP table:
  ┌───────────────────────────────────────────────┐
  │                                               │
  │  LCS = "ab"                                   │
  │                                               │
  │  Merge:                                       │
  │  - Start from end of both strings             │
  │  - If char in LCS, take from both             │
  │  - Otherwise, take remaining char             │
  │                                               │
  │  Result: "cabac"                              │
  │  Contains "abac" as subsequence? YES          │
  │  Contains "cab" as subsequence? YES           │
  │  Length = 5 = len("abac") + len("cab") - LCS  │
  └───────────────────────────────────────────────┘
```

## 6. Distinct Subsequences (LeetCode 115)

```python
def num_distinct(s, t):
    """
    Count distinct subsequences of s which equal t
    Time: O(m * n)
    Space: O(m * n)
    """
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Empty t is subsequence of any s
    for i in range(m + 1):
        dp[i][0] = 1
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]
            else:
                dp[i][j] = dp[i - 1][j]
    
    return dp[m][n]

def num_distinct_optimized(s, t):
    """Space-optimized version"""
    m, n = len(s), len(t)
    prev = [1] * (n + 1)
    
    for i in range(1, m + 1):
        curr = [1] + [0] * n
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                curr[j] = prev[j - 1] + prev[j]
            else:
                curr[j] = prev[j]
        prev = curr
    
    return prev[n]

# Test
print(num_distinct("rabbbit", "rabbit"))  # 3
print(num_distinct_optimized("babgbag", "bag"))  # 5
```

### Visual: Distinct Subsequences DP

```
  s = "rabbbit", t = "rabbit"

  How many ways to delete chars from s to get t?

  s: r a b b b i t
  t: r a b b   i t

  The three 'b's in s can each serve as the 3rd 'b' in t:
  s: r a [b] b b i t  -> rabbit
  s: r a b [b] b i t  -> rabbit
  s: r a b b [b] i t  -> rabbit

  Answer: 3 ways

  Recurrence:
  ┌─────────────────────────────────────────────────────┐
  │ if s[i-1] == t[j-1]:                                │
  │   dp[i][j] = dp[i-1][j-1] + dp[i-1][j]             │
  │   (use this char)    (skip this char)               │
  │ else:                                                │
  │   dp[i][j] = dp[i-1][j]  (must skip)               │
  └─────────────────────────────────────────────────────┘
```

## 7. Interleaving String (LeetCode 97)

```python
def is_interleave(s1, s2, s3):
    """
    Check if s3 is formed by interleaving s1 and s2
    Time: O(m * n)
    Space: O(m * n)
    """
    m, n = len(s1), len(s2)
    
    if m + n != len(s3):
        return False
    
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    
    # Fill first row
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]
    
    # Fill first column
    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]
    
    # Fill rest
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = (
                (dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]) or
                (dp[i][j - 1] and s2[j - 1] == s3[i + j - 1])
            )
    
    return dp[m][n]

# Test
print(is_interleave("aabcc", "dbbca", "aadbbcbcac"))  # True
print(is_interleave("aabcc", "dbbca", "aadbbbaccc"))  # False
```

### Visual: Interleaving String DP Table

```
  s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"

  dp[i][j] = True if s3[0:i+j] can be formed by
             interleaving s1[0:i] and s2[0:j]

       ""  d   b   b   c   a
    ┌────┬────┬────┬────┬────┬────┐
 "" │ T  │ F  │ F  │ F  │ F  │ F  │
    ├────┼────┼────┼────┼────┼────┤
 a  │ T  │ F  │ F  │ F  │ F  │ F  │  <- s1[0]='a' matches s3[0]='a'
    ├────┼────┼────┼────┼────┼────┤
 a  │ T  │ F  │ F  │ F  │ F  │ F  │
    ├────┼────┼────┼────┼────┼────┤
 b  │ T  │ F  │ T  │ T  │ F  │ F  │
    ├────┼────┼────┼────┼────┼────┤
 c  │ F  │ F  │ F  │ T  │ T  │ F  │
    ├────┼────┼────┼────┼────┼────┤
 c  │ F  │ F  │ F  │ F  │ T  │ T  │
    └────┴────┴────┴────┴────┴────┘

  dp[5][5] = True -> s3 IS an interleaving
```

## 8. Wildcard Pattern Matching (LeetCode 44)

```python
def is_match_wildcard(s, p):
    """
    Check if s matches pattern with '?' and '*'
    Time: O(m * n)
    Space: O(m * n)
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    
    # Fill first row (empty string matching pattern)
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
            elif p[j - 1] == '?' or s[i - 1] == p[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = False
    
    return dp[m][n]

# Test
print(is_match_wildcard("aa", "a"))     # False
print(is_match_wildcard("aa", "*"))     # True
print(is_match_wildcard("cb", "?a"))    # False
print(is_match_wildcard("adceb", "*a*b"))  # True
```

### Visual: Wildcard Matching DP Table

```
  s = "adceb", p = "*a*b"

       ""  *   a   *   b
    ┌────┬────┬────┬────┬────┐
 "" │ T  │ T  │ F  │ F  │ F  │  <- empty string with wildcards
    ├────┼────┼────┼────┼────┤
 a  │ F  │ T  │ T  │ T  │ F  │  <- 'a'=='a'
    ├────┼────┼────┼────┼────┤
 d  │ F  │ T  │ F  │ T  │ F  │  <- 'd'!='a', but * matches 'd'
    ├────┼────┼────┼────┼────┤
 c  │ F  │ T  │ F  │ T  │ F  │  <- * still covering
    ├────┼────┼────┼────┼────┤
 e  │ F  │ T  │ F  │ T  │ F  │
    ├────┼────┼────┼────┼────┤
 b  │ F  │ T  │ F  │ T  │ T  │  <- 'b'=='b'
    └────┴────┴────┴────┴────┘

  Rules:
  ┌─────────────────────────────────────────────────────────┐
  │ '*' : matches zero or more of ANY character             │
  │   dp[i][j] = dp[i-1][j]    (* matches s[i])           │
  │            | dp[i][j-1]     (* matches empty)          │
  │                                                         │
  │ '?' : matches exactly ONE character                     │
  │   dp[i][j] = dp[i-1][j-1]                              │
  │                                                         │
  │ char: matches itself                                    │
  │   dp[i][j] = dp[i-1][j-1] if s[i]==p[j]              │
  └─────────────────────────────────────────────────────────┘
```

## 9. Regular Expression Matching (LeetCode 10)

```python
def is_match_regex(s, p):
    """
    Check if s matches regex with '.' and '*'
    Time: O(m * n)
    Space: O(m * n)
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    
    # Handle patterns like a*, a*b*, etc.
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # '*' matches zero or more of preceding character
                dp[i][j] = dp[i][j - 2]  # Zero occurrences
                
                if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]  # One or more
            
            elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = False
    
    return dp[m][n]

# Test
print(is_match_regex("aa", "a"))       # False
print(is_match_regex("aa", "a*"))      # True
print(is_match_regex("ab", ".*"))      # True
print(is_match_regex("aab", "c*a*b"))  # True
```

### Visual: Regex Matching DP Table

```
  s = "aab", p = "c*a*b"

       ""  c   *   a   *   b
    ┌────┬────┬────┬────┬────┬────┐
 "" │ T  │ F  │ T  │ F  │ T  │ F  │
    ├────┼────┼────┼────┼────┼────┤
 a  │ F  │ F  │ F  │ T  │ T  │ F  │  <- 'a' matches 'a'
    ├────┼────┼────┼────┼────┼────┤
 a  │ F  │ F  │ F  │ T  │ T  │ F  │  <- a* matches "aa"
    ├────┼────┼────┼────┼────┼────┤
 b  │ F  │ F  │ F  │ F  │ T  │ T  │  <- b matches b
    └────┴────┴────┴────┴────┴────┘

  c* matches "" (zero occurrences)
  a* matches "aa" (two occurrences)
  b matches "b"

  Rules for regex with '.' and '*':
  ┌─────────────────────────────────────────────────────────┐
  │ '.' : matches any single character                      │
  │                                                         │
  │ 'c*' : zero or more 'c' characters                     │
  │   dp[i][j] = dp[i][j-2]           (zero 'c')          │
  │            | dp[i-1][j] if s[i]==c  (one or more)     │
  │                                                         │
  │ The tricky part: 'a*' pattern at position j means      │
  │ look back TWO positions in pattern (j-2) for the char  │
  └─────────────────────────────────────────────────────────┘
```

## 10. Additional String DP Problems

```python
# Problem: Longest Palindromic Subsequence
def lps_dp(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    
    for i in range(n):
        dp[i][i] = 1
    
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    
    return dp[0][n - 1]

# Problem: Minimum Insertions to Make Palindrome
def min_insertions_palindrome(s):
    n = len(s)
    # Longest palindromic subsequence
    lps = lps_dp(s)
    return n - lps

# Problem: Longest Alternating Subsequence
def longest_alternating_subsequence(nums):
    n = len(nums)
    if n <= 1:
        return n
    
    up = [1] * n
    down = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j]:
                up[i] = max(up[i], down[j] + 1)
            elif nums[i] < nums[j]:
                down[i] = max(down[i], up[j] + 1)
    
    return max(max(up), max(down))

# Problem: Longest Palindromic Substring
def longest_palindrome_dp(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1
    
    for i in range(n):
        dp[i][i] = True
    
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            start, max_len = i, 2
    
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                if length > max_len:
                    start, max_len = i, length
    
    return s[start:start + max_len]

# Test all
print("LPS of 'bbbab':", lps_dp("bbbab"))  # 4
print("Min insertions 'abcde':", min_insertions_palindrome("abcde"))  # 3
print("Longest alternating [1,2,3,4]:", longest_alternating_subsequence([1, 2, 3, 4]))  # 2
print("Longest palindrome 'babad':", longest_palindrome_dp("babad"))  # "bab"
```

---

## Summary: Key Patterns to Remember

```
  ┌──────────────────────────────────────────────────────────────────┐
  │              STRING DP PATTERN CHEAT SHEET                       │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                  │
  │  1. TWO STRINGS, FIND COMMON:                                    │
  │     dp[i][j] = ... depends on whether s1[i]==s2[j]             │
  │     Use: LCS, Edit Distance, SCS, Distinct Subseq              │
  │                                                                  │
  │  2. SINGLE STRING, FIND PROPERTY:                                │
  │     dp[i][j] = best answer for s[i..j]                         │
  │     Use: LPS, Palindromic Substring, Partitioning              │
  │                                                                  │
  │  3. PATTERN MATCHING:                                            │
  │     dp[i][j] = does s[0..i] match p[0..j]?                    │
  │     Use: Wildcard, Regex, Interleaving                          │
  │                                                                  │
  │  4. SPACE OPTIMIZATION:                                          │
  │     If dp[i][j] only depends on previous row -> O(n) space     │
  │     Use two arrays: prev and curr                                │
  │                                                                  │
  │  5. FILL ORDER:                                                  │
  │     Usually top-left to bottom-right                            │
  │     For substring problems: by increasing length                │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
```
