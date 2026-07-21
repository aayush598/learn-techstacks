# String DP Problems

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
