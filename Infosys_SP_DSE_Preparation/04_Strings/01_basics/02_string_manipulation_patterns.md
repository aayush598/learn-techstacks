# String Manipulation Patterns - Hashing Techniques

## 1. Running Hash for Substring Comparison

```python
# Running hash allows O(1) comparison of any two substrings
# After O(n) preprocessing, we can get hash of any substring in O(1)

def compute_rolling_hash(s, base=31, mod=10**9 + 7):
    n = len(s)
    prefix_hash = [0] * (n + 1)
    power = [1] * (n + 1)
    
    for i in range(n):
        prefix_hash[i + 1] = (prefix_hash[i] * base + ord(s[i])) % mod
        power[i + 1] = (power[i] * base) % mod
    
    return prefix_hash, power

def get_substring_hash(prefix_hash, power, l, r, mod=10**9 + 7):
    """Get hash of s[l:r+1] in O(1)"""
    return (prefix_hash[r + 1] - prefix_hash[l] * power[r - l + 1]) % mod

# Example usage
s = "abcabcabc"
prefix_hash, power = compute_rolling_hash(s)

# Compare "abc" (0:3) with "abc" (3:6)
h1 = get_substring_hash(prefix_hash, power, 0, 2)
h2 = get_substring_hash(prefix_hash, power, 3, 5)
print(f"Hash of 'abc' at 0: {h1}")
print(f"Hash of 'abc' at 3: {h2}")
print(f"Equal: {h1 == h2}")  # True
```

## 2. Rolling Hash Concept

```python
class RollingHash:
    """Rolling hash for string matching"""
    
    def __init__(self, base=31, mod=10**9 + 7):
        self.base = base
        self.mod = mod
        self.hash = 0
        self.length = 0
        self.power = 1
    
    def add_char(self, c):
        """Add character to the right of current window"""
        self.hash = (self.hash * self.base + ord(c)) % self.mod
        self.length += 1
    
    def remove_char(self, c):
        """Remove character from the left of current window"""
        self.hash = (self.hash - ord(c) * self.power) % self.mod
        self.hash = (self.hash + self.mod) % self.mod  # Handle negative
        self.length -= 1
    
    def roll(self, remove_c, add_c):
        """Roll the window: remove left, add right"""
        self.power = pow(self.base, self.length - 1, self.mod)
        self.hash = (self.hash - ord(remove_c) * self.power) % self.mod
        self.hash = (self.hash * self.base + ord(add_c)) % self.mod
        self.hash = (self.hash + self.mod) % self.mod
    
    def get_hash(self):
        return self.hash

# Example: Find pattern in text using rolling hash
def find_pattern_rolling(text, pattern):
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    base, mod = 31, 10**9 + 7
    
    # Compute pattern hash
    pattern_hash = 0
    for c in pattern:
        pattern_hash = (pattern_hash * base + ord(c)) % mod
    
    # Compute initial window hash
    window_hash = 0
    for i in range(m):
        window_hash = (window_hash * base + ord(text[i])) % mod
    
    result = []
    power = pow(base, m - 1, mod)
    
    for i in range(n - m + 1):
        if window_hash == pattern_hash:
            # Verify (handle hash collisions)
            if text[i:i + m] == pattern:
                result.append(i)
        
        if i < n - m:
            # Roll the window
            window_hash = (window_hash - ord(text[i]) * power) % mod
            window_hash = (window_hash * base + ord(text[i + m])) % mod
            window_hash = (window_hash + mod) % mod
    
    return result

text = "abcabcabc"
pattern = "abc"
print(f"Pattern found at indices: {find_pattern_rolling(text, pattern)}")
# [0, 3, 6]
```

## 3. Rabin-Karp Algorithm

```python
def rabin_karp(text, pattern):
    """
    Rabin-Karp string matching algorithm
    Time: O(n + m) average, O(n*m) worst case
    Space: O(1)
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    base = 256
    mod = 10**9 + 7
    
    # Compute pattern hash
    pattern_hash = 0
    for c in pattern:
        pattern_hash = (pattern_hash * base + ord(c)) % mod
    
    # Compute initial window hash
    window_hash = 0
    for i in range(m):
        window_hash = (window_hash * base + ord(text[i])) % mod
    
    result = []
    power = pow(base, m - 1, mod)
    
    for i in range(n - m + 1):
        if window_hash == pattern_hash:
            # Verify to handle hash collisions
            if text[i:i + m] == pattern:
                result.append(i)
        
        if i < n - m:
            # Remove leftmost character, add new character
            window_hash = (window_hash - ord(text[i]) * power) % mod
            window_hash = (window_hash * base + ord(text[i + m])) % mod
            window_hash = (window_hash + mod) % mod
    
    return result

# Example
text = "ababcababcabc"
pattern = "abc"
print(f"Pattern found at: {rabin_karp(text, pattern)}")
```

## 4. String Hashing with Two Moduli

```python
def double_hash_string(s, bases=(31, 37), mods=(10**9 + 7, 10**9 + 9)):
    """
    Use two moduli to virtually eliminate hash collisions
    Time: O(n) preprocessing, O(1) per query
    """
    n = len(s)
    b1, b2 = bases
    m1, m2 = mods
    
    # First hash
    hash1 = [0] * (n + 1)
    pow1 = [1] * (n + 1)
    
    # Second hash
    hash2 = [0] * (n + 1)
    pow2 = [1] * (n + 1)
    
    for i in range(n):
        hash1[i + 1] = (hash1[i] * b1 + ord(s[i])) % m1
        pow1[i + 1] = (pow1[i] * b1) % m1
        hash2[i + 1] = (hash2[i] * b2 + ord(s[i])) % m2
        pow2[i + 1] = (pow2[i] * b2) % m2
    
    return (hash1, pow1, m1), (hash2, pow2, m2)

def get_double_hash(h1_data, h2_data, l, r):
    """Get double hash of s[l:r+1]"""
    hash1, pow1, m1 = h1_data
    hash2, pow2, m2 = h2_data
    
    h1 = (hash1[r + 1] - hash1[l] * pow1[r - l + 1]) % m1
    h2 = (hash2[r + 1] - hash2[l] * pow2[r - l + 1]) % m2
    
    return (h1, h2)

# Example
s = "abcabcabc"
h1_data, h2_data = double_hash_string(s)

# Compare substrings
hash_0_2 = get_double_hash(h1_data, h2_data, 0, 2)
hash_3_5 = get_double_hash(h1_data, h2_data, 3, 5)
hash_6_8 = get_double_hash(h1_data, h2_data, 6, 8)

print(f"Hash of s[0:3]: {hash_0_2}")
print(f"Hash of s[3:6]: {hash_3_5}")
print(f"Hash of s[6:9]: {hash_6_8}")
print(f"All equal: {hash_0_2 == hash_3_5 == hash_6_8}")  # True
```

## 5. Polynomial Rolling Hash

```python
class PolynomialHash:
    """Polynomial rolling hash with collision resistance"""
    
    def __init__(self, base=31, mod=10**9 + 7):
        self.base = base
        self.mod = mod
        self.hash = 0
        self.length = 0
    
    def update(self, old_char, new_char):
        """Update hash when sliding window"""
        self.hash = (self.hash * self.base - 
                     ord(old_char) * pow(self.base, self.length, self.mod) + 
                     ord(new_char)) % self.mod
        self.hash = (self.hash + self.mod) % self.mod
    
    def compute(self, s):
        """Compute hash of entire string"""
        self.hash = 0
        self.length = len(s)
        for c in s:
            self.hash = (self.hash * self.base + ord(c)) % self.mod
        return self.hash
    
    def get_hash(self):
        return self.hash

# Compute hash for multiple substrings
def compute_all_hashes(s, base=31, mod=10**9 + 7):
    """Compute prefix hashes for all substrings"""
    n = len(s)
    hash_vals = [0] * (n + 1)
    powers = [1] * (n + 1)
    
    for i in range(n):
        hash_vals[i + 1] = (hash_vals[i] * base + ord(s[i])) % mod
        powers[i + 1] = (powers[i] * base) % mod
    
    return hash_vals, powers

def substring_hash(hash_vals, powers, l, r, mod=10**9 + 7):
    """Get hash of s[l:r+1]"""
    return (hash_vals[r + 1] - hash_vals[l] * powers[r - l + 1]) % mod

# Example: Find all palindromic substrings using hashing
def count_palindromic_substrings_hash(s):
    """Count palindromic substrings using rolling hash"""
    n = len(s)
    if n == 0:
        return 0
    
    # Forward hash
    hash_vals, powers = compute_all_hashes(s)
    # Reverse hash
    rev_s = s[::-1]
    rev_hash_vals, rev_powers = compute_all_hashes(rev_s)
    
    count = 0
    
    # Check all odd length palindromes
    for center in range(n):
        left, right = center, center
        while left >= 0 and right < n:
            fwd = substring_hash(hash_vals, powers, left, right)
            # Map to reversed indices
            rev_left = n - 1 - right
            rev_right = n - 1 - left
            rev = substring_hash(rev_hash_vals, rev_powers, rev_left, rev_right)
            if fwd == rev:
                count += 1
                left -= 1
                right += 1
            else:
                break
    
    # Check all even length palindromes
    for center in range(n - 1):
        left, right = center, center + 1
        while left >= 0 and right < n:
            fwd = substring_hash(hash_vals, powers, left, right)
            rev_left = n - 1 - right
            rev_right = n - 1 - left
            rev = substring_hash(rev_hash_vals, rev_powers, rev_left, rev_right)
            if fwd == rev:
                count += 1
                left -= 1
                right += 1
            else:
                break
    
    return count

print(f"Palindromic substrings in 'abc': {count_palindromic_substrings_hash('abc')}")  # 3
print(f"Palindromic substrings in 'aaa': {count_palindromic_substrings_hash('aaa')}")  # 6
```

## 6. Applications

```python
# APPLICATION 1: Find Duplicate Substrings
def find_duplicate_substrings(s, k):
    """Find all substrings of length k that appear more than once"""
    n = len(s)
    if k > n:
        return []
    
    base, mod = 31, 10**9 + 7
    hash_count = {}
    
    # Compute initial hash
    current_hash = 0
    for i in range(k):
        current_hash = (current_hash * base + ord(s[i])) % mod
    
    hash_count[current_hash] = [0]
    
    power = pow(base, k - 1, mod)
    
    for i in range(1, n - k + 1):
        # Roll the hash
        current_hash = (current_hash - ord(s[i - 1]) * power) % mod
        current_hash = (current_hash * base + ord(s[i + k - 1])) % mod
        current_hash = (current_hash + mod) % mod
        
        if current_hash in hash_count:
            hash_count[current_hash].append(i)
        else:
            hash_count[current_hash] = [i]
    
    # Filter duplicates and verify
    duplicates = set()
    for h, positions in hash_count.items():
        if len(positions) > 1:
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    sub1 = s[positions[i]:positions[i] + k]
                    sub2 = s[positions[j]:positions[j] + k]
                    if sub1 == sub2:
                        duplicates.add(sub1)
    
    return list(duplicates)

print(find_duplicate_substrings("abcabcabc", 3))  # ['abc', 'bca', 'cab']
print(find_duplicate_substrings("abcdabcd", 4))   # ['abcd']


# APPLICATION 2: Count Distinct Substrings
def count_distinct_substrings(s):
    """Count all distinct non-empty substrings using hashing"""
    n = len(s)
    base, mod = 31, 10**9 + 7
    
    hash_set = set()
    
    for length in range(1, n + 1):
        current_hash = 0
        power = pow(base, length - 1, mod)
        
        for i in range(length):
            current_hash = (current_hash * base + ord(s[i])) % mod
        
        hash_set.add(current_hash)
        
        for i in range(1, n - length + 1):
            current_hash = (current_hash - ord(s[i - 1]) * power) % mod
            current_hash = (current_hash * base + ord(s[i + length - 1])) % mod
            current_hash = (current_hash + mod) % mod
            hash_set.add(current_hash)
    
    return len(hash_set)

print(f"Distinct substrings in 'abc': {count_distinct_substrings('abc')}")  # 6
print(f"Distinct substrings in 'aaa': {count_distinct_substrings('aaa')}")  # 6


# APPLICATION 3: Longest Duplicate Substring
def longest_duplicate_substring(s):
    """Find the longest substring that appears at least twice"""
    n = len(s)
    
    def check(length):
        """Check if any substring of given length appears twice"""
        if length == 0:
            return ""
        
        base, mod = 31, 10**9 + 7
        hash_map = {}
        
        current_hash = 0
        for i in range(length):
            current_hash = (current_hash * base + ord(s[i])) % mod
        
        hash_map[current_hash] = [0]
        
        power = pow(base, length - 1, mod)
        
        for i in range(1, n - length + 1):
            current_hash = (current_hash - ord(s[i - 1]) * power) % mod
            current_hash = (current_hash * base + ord(s[i + length - 1])) % mod
            current_hash = (current_hash + mod) % mod
            
            if current_hash in hash_map:
                for pos in hash_map[current_hash]:
                    if s[pos:pos + length] == s[i:i + length]:
                        return s[i:i + length]
                hash_map[current_hash].append(i)
            else:
                hash_map[current_hash] = [i]
        
        return ""
    
    # Binary search for maximum length
    left, right = 0, n - 1
    result = ""
    
    while left <= right:
        mid = (left + right) // 2
        found = check(mid)
        if found:
            result = found
            left = mid + 1
        else:
            right = mid - 1
    
    return result

print(f"Longest duplicate in 'abcabc': {longest_duplicate_substring('abcabc')}")  # "abc"
print(f"Longest duplicate in 'abcdabcd': {longest_duplicate_substring('abcdabcd')}")  # "abcd"


# APPLICATION 4: String Matching in O(n+m)
def string_match_hash(text, pattern):
    """Efficient string matching using rolling hash"""
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    base, mod = 31, 10**9 + 7
    
    # Pattern hash
    pattern_hash = 0
    for c in pattern:
        pattern_hash = (pattern_hash * base + ord(c)) % mod
    
    # Text hash
    text_hash = 0
    for i in range(m):
        text_hash = (text_hash * base + ord(text[i])) % mod
    
    result = []
    power = pow(base, m - 1, mod)
    
    for i in range(n - m + 1):
        if text_hash == pattern_hash:
            if text[i:i + m] == pattern:
                result.append(i)
        
        if i < n - m:
            text_hash = (text_hash - ord(text[i]) * power) % mod
            text_hash = (text_hash * base + ord(text[i + m])) % mod
            text_hash = (text_hash + mod) % mod
    
    return result

print(string_match_hash("ababcababcabc", "abc"))  # [2, 7, 11]
```
