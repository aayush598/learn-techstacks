# Strings and Pattern Matching

Tested templates for string algorithms. All code is verified correct Python 3.

## String building / iteration patterns

```python
s = "abracadabra"              # sample value (lowercase for [0]*26 indexing)
c = s[0]
# Build result efficiently: list + join (strings are immutable; += is O(n^2))
out = []
for ch in s:
    out.append(ch.upper())
result = "".join(out)

# Reverse a string
rev = s[::-1]                      # O(n)

# Palindrome check
def is_palindrome(s):
    return s == s[::-1]

# Palindrome check with range (no extra string copy)
def is_pal_range(s, lo, hi):
    while lo < hi:
        if s[lo] != s[hi]:
            return False
        lo += 1; hi -= 1
    return True

# ASCII tricks — index into a 26-slot array
i = ord(c) - ord("a")              # 'a'->0, 'z'->25  (97 = ord('a'))
# iterate chars with index
for i, c in enumerate(s):
    ...

# Character frequency — Counter
from collections import Counter
cnt = Counter(s)                   # O(n)
# Character frequency — [0]*26 array (faster, works only for lowercase letters)
freq = [0] * 26
for c in s:
    freq[ord(c) - 97] += 1

# string -> list -> mutate -> string (for in-place edits / swaps)
a = list(s)                        # ['a','b','c']
a[0], a[-1] = a[-1], a[0]
s2 = "".join(a)

# sort a string
sorted_s = "".join(sorted(s))
```

## KMP — prefix function + search

```python
def kmp_prefix(p):
    n = len(p)
    lps = [0] * n                     # lps[i] = len of longest proper prefix == suffix of p[:i+1]
    j = 0
    for i in range(1, n):
        while j > 0 and p[i] != p[j]:  # fall back
            j = lps[j - 1]
        if p[i] == p[j]:
            j += 1
        lps[i] = j
    return lps

def kmp_search(text, pattern):
    lps = kmp_prefix(pattern)
    res = []
    j = 0
    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:   # mismatch -> fall back
            j = lps[j - 1]
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):                # match found
            res.append(i - j + 1)            # start index
            j = lps[j - 1]                   # continue searching overlaps
    return res

# kmp_prefix("aabaaab") == [0,1,0,1,2,2,3]
# kmp_search("aaaa", "aa") == [0, 1, 2]
```
Complexity: O(n + m) time (both functions), O(m) space for lps.
Verify prefix: `kmp_prefix("ababaca") == [0,0,1,2,3,0,1]`.

## Z-algorithm

```python
def z_algorithm(s):
    n = len(s)
    z = [0] * n                       # z[i] = len of longest prefix of s starting at i
    l = r = 0                         # current Z-box [l, r]
    for i in range(1, n):
        if i <= r:                    # i inside a previous box -> reuse
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1                 # naive extend
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z

def z_search(text, pattern):
    concat = pattern + "$" + text     # '$' separator not in either
    z = z_algorithm(concat)
    m = len(pattern)
    return [i - m - 1 for i, v in enumerate(z) if v == m]

# z_algorithm("aaaaa") == [0,4,3,2,1]
# z_search("abxabcabcaby", "abcaby") == [6]
```
Complexity: O(n + m) time, O(n + m) space.
Usage: substring search, count occurrences, find all prefix-suffix overlaps (longest prefix that is also suffix), compress a string.

## Rabin–Karp — rolling hash

```python
def rabin_karp(text, pattern):
    base = 256
    mod = 10**9 + 7                   # large prime to reduce collisions
    n, m = len(text), len(pattern)
    if m > n:
        return []

    hp = h = 0                        # hash of pattern; hash of first window
    hpow = 1                          # base^(m-1) mod mod
    for i in range(m):
        hp = (hp * base + ord(pattern[i])) % mod
        h = (h * base + ord(text[i])) % mod
        hpow = (hpow * base) % mod

    res = []
    for i in range(n - m + 1):
        if h == hp:                   # hash collision possible -> verify char-by-char
            if text[i:i + m] == pattern:
                res.append(i)
        if i < n - m:                 # roll hash forward: remove first char, add next
            h = (h * base - ord(text[i]) * hpow + ord(text[i + m])) % mod
            h %= mod                  # keep positive
    return res
```
Complexity: O(n + m) average, O(n·m) worst case (hash collisions); O(1) space.
`h = (h*base - ord(text[i])*hpow + ord(text[i+m])) % mod` — remove leftmost char, shift, add new char. Always verify matches with the direct compare.

## Longest palindromic substring — expand around center

```python
def longest_palindrome(s):
    res = ""
    for i in range(len(s)):
        # odd-length palindromes centered at i, even-length centered between i, i+1
        for l, r in ((i, i), (i, i + 1)):
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1; r += 1
            if r - l - 1 > len(res):        # window [l+1, r) is a palindrome
                res = s[l + 1:r]
    return res

# count palindromic substrings (LeetCode 647) — same expansion, count instead
def count_palindromes(s):
    n = len(s)
    cnt = 0
    for i in range(n):
        for l, r in ((i, i), (i, i + 1)):
            while l >= 0 and r < n and s[l] == s[r]:
                cnt += 1
                l -= 1; r += 1
    return cnt
# longest_palindrome("cbbd") == "bb"; count_palindromes("aaa") == 6
```
Complexity: O(n²) time, O(1) space. (Manacher is O(n) — rarely needed in interviews.)

## Anagram grouping

```python
from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        groups[tuple(sorted(w))].append(w)     # sorted string as key
    return list(groups.values())

def group_anagrams_count(words):               # faster: 26-counts tuple as key
    groups = defaultdict(list)
    for w in words:
        key = [0] * 26
        for c in w:
            key[ord(c) - 97] += 1
        groups[tuple(key)].append(w)
    return list(groups.values())
```
Complexity: O(n·k) time (k = max word length), O(n·k) space. Tuple keys are hashable; lists are not.

## Decode / encode patterns

```python
# Decode string "3[a2[c]]" -> "accaccacc"  (LeetCode 394)
def decode_string(s):
    stack = []
    num = 0
    cur = ""
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c == "[":
            stack.append((cur, num))
            cur, num = "", 0
        elif c == "]":
            prev, k = stack.pop()
            cur = prev + k * cur
        else:
            cur += c
    return cur
assert decode_string("3[a2[c]]") == "accaccacc"

# Encode: run-length encoding "aaabbc" -> "3a2b1c"
def run_length_encode(s):
    res = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        res.append(f"{j - i}{s[i]}")
        i = j
    return "".join(res)
```
Decode complexity: O(n) where n = length of decoded output.

## Parenthesis matching

```python
# Validate parentheses (LeetCode 20)
def is_valid(s):
    st = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for c in s:
        if c in pairs.values():        # opening bracket
            st.append(c)
        else:                          # closing bracket
            if not st or st.pop() != pairs[c]:
                return False
    return not st

# Score of parentheses (LeetCode 856): () = 1, (A) = 2*A, A+B = A+B
def score(s):
    st = [0]
    for c in s:
        if c == "(":
            st.append(0)
        else:
            v = st.pop()
            st[-1] += max(2 * v, 1)
    return st[0]
assert score("(())") == 2 and score("()()") == 2

# Longest valid parentheses (LeetCode 32) — stack of indices
def longest_valid(s):
    st = [-1]
    best = 0
    for i, c in enumerate(s):
        if c == "(":
            st.append(i)
        else:
            st.pop()
            if not st:
                st.append(i)           # reset base
            else:
                best = max(best, i - st[-1])
    return best
assert longest_valid(")()())") == 4
```
Complexity: O(n) time, O(n) space.

## String algorithm complexity summary

| Algorithm | Preprocess | Search | Space |
|---|---|---|---|
| KMP | O(m) | O(n) | O(m) |
| Z-algorithm | O(n+m) | — | O(n+m) |
| Rabin-Karp | O(m) | O(n) avg | O(1) |
| Expand around center | — | O(n²) | O(1) |
| Manacher | — | O(n) | O(n) |
