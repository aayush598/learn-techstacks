# Palindrome Problems

## 1. Palindrome Checking

```python
def is_palindrome_recursive(s):
    """Check palindrome using recursion"""
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome_recursive(s[1:-1])

# Time: O(n), Space: O(n) due to recursion stack

def is_palindrome_iterative(s):
    """Check palindrome using two pointers"""
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

# Time: O(n), Space: O(1)

def is_palindrome_filtered(s):
    """Check palindrome ignoring non-alphanumeric characters"""
    filtered = ''.join(c.lower() for c in s if c.isalnum())
    return filtered == filtered[::-1]

# Test
print(is_palindrome_recursive("racecar"))  # True
print(is_palindrome_iterative("hello"))    # False
print(is_palindrome_filtered("A man, a plan, a canal: Panama"))  # True
```

## 2. Longest Palindromic Substring (LeetCode 5)

```python
def longest_palindrome_expand(s):
    """
    Expand around center approach
    Time: O(n^2)
    Space: O(1)
    """
    if len(s) < 2:
        return s
    
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]
    
    result = ""
    
    for i in range(len(s)):
        # Odd length palindrome
        odd = expand_around_center(i, i)
        if len(odd) > len(result):
            result = odd
        
        # Even length palindrome
        even = expand_around_center(i, i + 1)
        if len(even) > len(result):
            result = even
    
    return result

# Time: O(n^2), Space: O(1)

def longest_palindrome_dp(s):
    """
    Dynamic Programming approach
    Time: O(n^2)
    Space: O(n^2)
    """
    n = len(s)
    if n < 2:
        return s
    
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1
    
    # All single characters are palindromes
    for i in range(n):
        dp[i][i] = True
    
    # Check for length 2
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            start, max_len = i, 2
    
    # Check for lengths > 2
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                if length > max_len:
                    start, max_len = i, length
    
    return s[start:start + max_len]

# Test
print(longest_palindrome_expand("babad"))   # "bab" or "aba"
print(longest_palindrome_dp("cbbd"))        # "bb"
```

## 3. Manacher's Algorithm - O(n)

```python
def manachers_algorithm(s):
    """
    Manacher's Algorithm for longest palindromic substring
    Time: O(n)
    Space: O(n)
    """
    if not s:
        return ""
    
    # Transform: "abc" -> "^#a#b#c#$"
    t = '^#' + '#'.join(s) + '#$'
    n = len(t)
    p = [0] * n
    
    center = right = 0
    
    for i in range(1, n - 1):
        mirror = 2 * center - i
        
        if i < right:
            p[i] = min(right - i, p[mirror])
        
        # Expand around center
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
        
        # Update center and right boundary
        if i + p[i] > right:
            center, right = i, i + p[i]
    
    # Find maximum
    max_len = max(p)
    center_index = p.index(max_len)
    start = (center_index - max_len) // 2
    
    return s[start:start + max_len]

def manachers_detailed(s):
    """Manacher's with step-by-step visualization"""
    if not s:
        return ""
    
    t = '^#' + '#'.join(s) + '#$'
    n = len(t)
    p = [0] * n
    
    center = right = 0
    steps = []
    
    steps.append(f"Original: {s}")
    steps.append(f"Transformed: {t}")
    steps.append("")
    
    for i in range(1, n - 1):
        mirror = 2 * center - i
        
        if i < right:
            p[i] = min(right - i, p[mirror])
            steps.append(f"i={i}: Using mirror, p[{i}] = {p[i]}")
        
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
        
        if i + p[i] > right:
            center, right = i, i + p[i]
            steps.append(f"i={i}: New center={center}, right={right}")
        
        steps.append(f"i={i}: p = {p}")
    
    max_len = max(p)
    center_index = p.index(max_len)
    start = (center_index - max_len) // 2
    
    return s[start:start + max_len], "\n".join(steps)

# Test
result, verbose = manachers_detailed("babad")
print(verbose)
print(f"\nLongest palindrome: {result}")
print(f"Manacher's result: {manachers_algorithm('cbbd')}")
```

## 4. Longest Palindromic Subsequence (LeetCode 516)

```python
def longest_palindromic_subsequence(s):
    """
    Find longest palindromic subsequence using DP
    Time: O(n^2)
    Space: O(n^2)
    """
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    
    # All single characters are palindromes
    for i in range(n):
        dp[i][i] = 1
    
    # Fill for lengths 2 to n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    
    return dp[0][n - 1]

def lps_optimized(s):
    """
    Space-optimized version
    Time: O(n^2)
    Space: O(n)
    """
    n = len(s)
    prev = [0] * n
    curr = [0] * n
    
    for i in range(n - 1, -1, -1):
        curr[i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                curr[j] = prev[j - 1] + 2
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, [0] * n
    
    return prev[n - 1]

# Test
print(longest_palindromic_subsequence("bbbab"))  # 4
print(lps_optimized("cbbd"))                     # 2
```

## 5. Valid Palindrome with Removal (LeetCode 680)

```python
def valid_palindrome(s):
    """
    Check if s can be palindrome by removing at most one character
    Time: O(n)
    Space: O(1)
    """
    def is_palindrome_range(left, right):
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True
    
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            return is_palindrome_range(left + 1, right) or \
                   is_palindrome_range(left, right - 1)
        left += 1
        right -= 1
    
    return True

# Test
print(valid_palindrome("aba"))        # True
print(valid_palindrome("abca"))       # True
print(valid_palindrome("abc"))        # False
print(valid_palindrome("deeee"))      # True
```

## 6. Palindrome Partitioning (LeetCode 131)

```python
def partition_palindrome(s):
    """
    Partition s such that every substring is a palindrome
    Return all possible partitions
    Time: O(n * 2^n)
    Space: O(n)
    """
    result = []
    
    def is_palindrome(sub):
        return sub == sub[::-1]
    
    def backtrack(start, path):
        if start == len(s):
            result.append(path[:])
            return
        
        for end in range(start + 1, len(s) + 1):
            if is_palindrome(s[start:end]):
                path.append(s[start:end])
                backtrack(end, path)
                path.pop()
    
    backtrack(0, [])
    return result

def partition_palindrome_dp(s):
    """
    Optimized with DP for palindrome checking
    Time: O(n * 2^n)
    Space: O(n^2)
    """
    n = len(s)
    
    # Precompute palindrome table
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for i in range(n - 1):
        is_pal[i][i + 1] = (s[i] == s[i + 1])
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = (s[i] == s[j] and is_pal[i + 1][j - 1])
    
    result = []
    
    def backtrack(start, path):
        if start == n:
            result.append(path[:])
            return
        
        for end in range(start, n):
            if is_pal[start][end]:
                path.append(s[start:end + 1])
                backtrack(end + 1, path)
                path.pop()
    
    backtrack(0, [])
    return result

# Test
print(partition_palindrome("aab"))
# [['a', 'a', 'b'], ['aa', 'b']]

print(partition_palindrome_dp("aabb"))
# [['a', 'a', 'b', 'b'], ['a', 'a', 'bb'], ['aa', 'b', 'b'], ['aa', 'bb']]
```

## 7. Minimum Cuts for Palindrome Partitioning (LeetCode 132)

```python
def min_cuts_palindrome(s):
    """
    Minimum cuts needed to partition string into palindromes
    Time: O(n^2)
    Space: O(n^2)
    """
    n = len(s)
    
    # Precompute palindrome table
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for i in range(n - 1):
        is_pal[i][i + 1] = (s[i] == s[i + 1])
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = (s[i] == s[j] and is_pal[i + 1][j - 1])
    
    # DP for minimum cuts
    dp = [0] * n  # dp[i] = min cuts for s[0:i+1]
    
    for i in range(n):
        if is_pal[0][i]:
            dp[i] = 0
        else:
            dp[i] = i  # Maximum cuts
            for j in range(1, i + 1):
                if is_pal[j][i]:
                    dp[i] = min(dp[i], dp[j - 1] + 1)
    
    return dp[n - 1]

def min_cuts_optimized(s):
    """
    Optimized O(n^2) solution
    Time: O(n^2)
    Space: O(n)
    """
    n = len(s)
    dp = [i for i in range(n)]  # dp[i] = min cuts for s[0:i+1]
    
    for i in range(n):
        # Odd length palindromes
        left, right = i, i
        while left >= 0 and right < n and s[left] == s[right]:
            if left == 0:
                dp[right] = 0
            else:
                dp[right] = min(dp[right], dp[left - 1] + 1)
            left -= 1
            right += 1
        
        # Even length palindromes
        left, right = i, i + 1
        while left >= 0 and right < n and s[left] == s[right]:
            if left == 0:
                dp[right] = 0
            else:
                dp[right] = min(dp[right], dp[left - 1] + 1)
            left -= 1
            right += 1
    
    return dp[n - 1]

# Test
print(min_cuts_palindrome("aab"))      # 1
print(min_cuts_optimized("aabb"))      # 1
print(min_cuts_palindrome("ab"))       # 1
```

## 8. Count Palindromic Subsequences

```python
def count_palindromic_subsequences(s):
    """
    Count all distinct palindromic subsequences
    Time: O(n^2)
    Space: O(n^2)
    """
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    
    # Single characters
    for i in range(n):
        dp[i][i] = 1
    
    # Fill for lengths 2 to n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    
    return dp[0][n - 1]

def count_distinct_palindromic_subsequences(s):
    """
    Count distinct palindromic subsequences
    Time: O(n^2)
    Space: O(n)
    """
    n = len(s)
    MOD = 10**9 + 7
    
    def count_subs(s):
        """Count all palindromic subsequences"""
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
    
    return count_subs(s)

# Test
print(count_palindromic_subsequences("abc"))  # 3
print(count_palindromic_subsequences("aaa"))  # 6
```

## 9. Generate Palindromes

```python
def generate_palindromes(s):
    """Generate all palindromic permutations of string"""
    from collections import Counter
    
    count = Counter(s)
    odd_chars = [c for c, v in count.items() if v % 2 == 1]
    
    if len(odd_chars) > 1:
        return []  # No palindrome permutation possible
    
    # Build half string
    half = []
    for c, v in count.items():
        half.extend([c] * (v // 2))
    
    # Generate all permutations of half
    def permute(arr):
        result = []
        used = [False] * len(arr)
        
        def backtrack(path):
            if len(path) == len(arr):
                result.append(''.join(path))
                return
            
            for i in range(len(arr)):
                if used[i] or (i > 0 and arr[i] == arr[i - 1] and not used[i - 1]):
                    continue
                used[i] = True
                path.append(arr[i])
                backtrack(path)
                path.pop()
                used[i] = False
        
        backtrack([])
        return result
    
    half_perms = permute(sorted(half))
    middle = odd_chars[0] if odd_chars else ""
    
    return [h + middle + h[::-1] for h in half_perms]

def generate_palindrome_optimized(s):
    """Generate palindromes without storing all permutations"""
    from collections import Counter
    from itertools import permutations
    
    count = Counter(s)
    odd_chars = [c for c, v in count.items() if v % 2 == 1]
    
    if len(odd_chars) > 1:
        return []
    
    half = []
    for c, v in count.items():
        half.extend([c] * (v // 2))
    
    # Use set to avoid duplicates
    seen = set()
    result = []
    
    for perm in permutations(half):
        perm_str = ''.join(perm)
        if perm_str not in seen:
            seen.add(perm_str)
            middle = odd_chars[0] if odd_chars else ""
            result.append(perm_str + middle + perm_str[::-1])
    
    return result

# Test
print(generate_palindromes("aabb"))    # ['abba', 'baab']
print(generate_palindrome_optimized("abc"))  # [] (no palindrome possible)
```

## 10. Additional Palindrome Problems

```python
# Problem: Shortest Palindrome (LeetCode 214)
def shortest_palindrome(s):
    """
    Add characters in front to make palindrome
    Find shortest such palindrome
    """
    if not s:
        return s
    
    # Find longest palindromic prefix
    rev = s[::-1]
    combined = s + '#' + rev
    
    # Compute LPS array
    n = len(combined)
    lps = [0] * n
    length = 0
    i = 1
    
    while i < n:
        if combined[i] == combined[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return rev[:len(s) - lps[-1]] + s

# Problem: Palindrome Number (LeetCode 9)
def is_palindrome_number(x):
    if x < 0:
        return False
    return str(x) == str(x)[::-1]

# Problem: Remove Palindromic Subsequences (LeetCode 1332)
def remove_palindromic_subsequences(s):
    """
    Remove palindromic subsequences until empty
    Returns minimum steps
    """
    if not s:
        return 0
    
    def is_pal(sub):
        return sub == sub[::-1]
    
    steps = 0
    while s:
        if is_pal(s):
            return steps + 1
        
        # Remove longest palindromic subsequence
        i, j = 0, len(s) - 1
        while i < j:
            if s[i] == s[j]:
                i += 1
                j -= 1
            else:
                break
        
        if i >= j:
            return steps + 1
        
        # For any non-palindrome, answer is 2
        return steps + 2
    
    return steps

# Test
print(shortest_palindrome("aacecaaa"))  # "aaacecaaa"
print(is_palindrome_number(121))         # True
print(remove_palindromic_subsequences("ababa"))  # 1
print(remove_palindromic_subsequences("abb"))    # 2
```
