# String Problems Batch 2 — Infosys SP DSE Preparation

## 50 More String Problems (Easy → Hard)

---

## EASY PROBLEMS (1–15)

---

### Problem 1: Reverse String

**Statement:** Write a function that reverses a character array `s` in-place using O(1) extra memory.

**Approach:** Use two pointers — one at the start (`left = 0`) and one at the end (`right = len(s) - 1`). Swap characters at both positions, then move `left` forward and `right` backward. Continue until they meet or cross.

**Edge Cases:**
- Empty string: do nothing
- Single character: already reversed
- Even and odd length strings both work

**Python Code:**
```python
def reverse_string(s: list[str]) -> None:
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
```

**Time Complexity:** O(n) — each element is swapped at most once  
**Space Complexity:** O(1) — in-place swaps only

---

### Problem 2: Reverse Words in String III

**Statement:** Given a string `s` consisting of words separated by spaces, reverse each word in place while preserving whitespace and original word order.

**Approach:** Split the string by spaces to get individual words. Reverse each word using slicing `[::-1]`. Join the reversed words back with spaces. This preserves the original spacing structure.

**Edge Cases:**
- Multiple spaces between words
- Leading/trailing spaces
- Single character words
- Single word string

**Python Code:**
```python
def reverse_words(s: str) -> str:
    words = s.split(' ')
    for i in range(len(words)):
        words[i] = words[i][::-1]
    return ' '.join(words)

def reverse_words_v2(s: str) -> str:
    # More Pythonic one-liner approach
    return ' '.join(word[::-1] for word in s.split(' '))
```

**Time Complexity:** O(n) — we visit each character once during split, reverse, and join  
**Space Complexity:** O(n) — for storing the split words and result

---

### Problem 3: Unique Email Addresses

**Statement:** Given a list of emails where each has a local name and domain name, process them: `.` in local name is ignored (treated as same), `+` ignores everything after it until `@`. Count unique processed email addresses.

**Approach:** For each email, split by `@` into local and domain. Process local name: take only the part before `+`, then remove all `.` characters. Combine processed local with domain. Use a hash set to track unique addresses.

**Edge Cases:**
- Multiple `+` symbols
- Multiple `.` symbols
- `+` before any `.`
- Same local name with different processing yielding same result

**Python Code:**
```python
def num_unique_emails(emails: list[str]) -> int:
    unique = set()
    for email in emails:
        local, domain = email.split('@')
        # Ignore everything after '+'
        local = local.split('+')[0]
        # Remove all dots
        local = local.replace('.', '')
        unique.add(f"{local}@{domain}")
    return len(unique)
```

**Time Complexity:** O(n * m) where n = number of emails, m = average email length  
**Space Complexity:** O(n * m) — storing unique addresses in the set

---

### Problem 4: Robot Return to Origin

**Statement:** A robot starts at position (0,0) on a 2D plane. Given a string of moves where `U` = up (y+1), `D` = down (y-1), `R` = right (x+1), `L` = left (x-1), determine if the robot returns to the origin.

**Approach:** Track the x and y coordinates. For each move, update the corresponding coordinate. After all moves, check if both x and y are zero. This works because opposite moves cancel each other out.

**Edge Cases:**
- Empty move string: robot stays at origin → True
- All same direction: robot moves away → False
- Equal numbers of opposite moves → True

**Python Code:**
```python
def judge_circle(moves: str) -> bool:
    x = y = 0
    for move in moves:
        if move == 'U':
            y += 1
        elif move == 'D':
            y -= 1
        elif move == 'R':
            x += 1
        elif move == 'L':
            x -= 1
    return x == 0 and y == 0
```

**Time Complexity:** O(n) — single pass through all moves  
**Space Complexity:** O(1) — only two integer variables

---

### Problem 5: Destination City

**Statement:** You are given a list of paths where `paths[i] = [cityA, cityB]` means there is a direct path from `cityA` to `cityB`. Each city has at most one outgoing path. Find the destination city — the city that is not a starting point of any path.

**Approach:** Put all starting (source) cities into a set for O(1) lookup. Iterate through all paths; the destination city that does NOT appear as a source city is the answer. Since it's guaranteed exactly one destination exists.

**Edge Cases:**
- Only two cities (A → B)
- Chain of cities (A → B → C → D)
- All paths form a cycle except the destination (not possible per problem constraints)

**Python Code:**
```python
def dest_city(paths: list[list[str]]) -> str:
    starts = set(path[0] for path in paths)
    for path in paths:
        if path[1] not in starts:
            return path[1]
```

**Time Complexity:** O(n) — building the set and searching are both O(n)  
**Space Complexity:** O(n) — for storing source cities in the set

---

### Problem 6: Maximum Nesting Depth of Parentheses

**Statement:** Given a valid parentheses string `s` (containing only `(`, `)`, and lowercase letters), find its maximum nesting depth. Letters don't affect depth.

**Approach:** Maintain a running depth counter. Increment on `(`, decrement on `)`. Track the maximum depth seen at any point. Since the string is valid, depth never goes negative.

**Edge Cases:**
- String with no parentheses → depth 0
- Fully nested like "((((" → depth = length
- Single pair "()" → depth 1
- Letters interspersed → ignored

**Python Code:**
```python
def max_depth(s: str) -> int:
    depth = 0
    max_d = 0
    for ch in s:
        if ch == '(':
            depth += 1
            max_d = max(max_d, depth)
        elif ch == ')':
            depth -= 1
    return max_d
```

**Time Complexity:** O(n) — single pass  
**Space Complexity:** O(1) — just two integer variables

---

### Problem 7: Split a String in Balanced Strings

**Statement:** A balanced string has an equal number of `L` and `R` characters. Given a balanced string `s`, split it into the maximum number of balanced substrings. Return the count.

**Approach:** Greedy left-to-right scan. Maintain a balance counter (+1 for `L`, -1 for `R`). Every time balance hits 0, we've found a balanced substring. The greedy approach maximizes the count because we split at every possible opportunity.

**Edge Cases:**
- Single balanced pair "LR" → 1
- All consecutive "LLLLRRRR" → 1
- Alternating "LRLRLR" → 3

**Python Code:**
```python
def balanced_string_split(s: str) -> int:
    count = 0
    balance = 0
    for ch in s:
        if ch == 'L':
            balance += 1
        else:
            balance -= 1
        if balance == 0:
            count += 1
    return count
```

**Time Complexity:** O(n) — single pass  
**Space Complexity:** O(1) — just two counters

---

### Problem 8: Remove Palindromic Subsequences

**Statement:** Given a string `s` consisting of only `a` and `b`, remove palindromic subsequences to make it empty. Return the minimum number of operations needed. A subsequence doesn't need to be contiguous.

**Approach:** Key insight: any string of `a`s and `b`s can be cleared in at most 2 operations (remove all `a`s as one subsequence, then all `b`s). If already a palindrome, 1 operation suffices. If empty, 0 operations.

**Edge Cases:**
- Empty string → 0
- Already a palindrome → 1
- All same characters → 1
- Any other case → 2 (always)

**Python Code:**
```python
def remove_palindrome_sub(s: str) -> int:
    if not s:
        return 0
    if s == s[::-1]:
        return 1
    return 2
```

**Time Complexity:** O(n) — for the palindrome check (reversal and comparison)  
**Space Complexity:** O(n) — for the reversed string copy

---

### Problem 9: Count Binary Substrings

**Statement:** Given a binary string `s`, count the number of non-empty substrings that have the same number of consecutive `0`s and consecutive `1`s. The groups must be contiguous.

**Approach:** First, group consecutive identical characters and record the size of each group. Then, for every pair of adjacent groups, the number of valid binary substrings that can be formed from them is `min(size[i], size[i+1])`.

**Why this works:** For groups of sizes m and n (adjacent), you can form `min(m, n)` substrings like "01", "0011", etc.

**Edge Cases:**
- All same characters → 0
- Alternating "010101" → n/2
- "001100" → groups [2,2,2] → min(2,2) + min(2,2) = 4

**Python Code:**
```python
def count_binary_substrings(s: str) -> int:
    groups = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            groups.append(count)
            count = 1
    groups.append(count)

    result = 0
    for i in range(len(groups) - 1):
        result += min(groups[i], groups[i + 1])
    return result
```

**Time Complexity:** O(n) — single pass to build groups, single pass to sum  
**Space Complexity:** O(n) — for the groups array

---

### Problem 10: Check If Two String Arrays are Equivalent

**Statement:** Two string arrays are equivalent if the concatenation of all strings in `word1` equals the concatenation of all strings in `word2`.

**Approach:** Simply join all strings in each array and compare the results. This is the most straightforward approach. An alternative generator-based approach avoids building the full strings.

**Edge Cases:**
- Empty arrays
- Single element arrays
- Very long concatenations

**Python Code:**
```python
def array_strings_are_equal(word1: list[str], word2: list[str]) -> bool:
    return ''.join(word1) == ''.join(word2)

def array_strings_are_equal_v2(word1: list[str], word2: list[str]) -> bool:
    def gen(words):
        for word in words:
            for ch in word:
                yield ch
    return all(a == b for a, b in zip(gen(word1), gen(word2)))
```

**Time Complexity:** O(n) where n = total characters across all strings  
**Space Complexity:** O(n) — for the concatenated result

---

### Problem 11: Goal Parser Interpretation

**Statement:** Given a string `command` consisting of characters `G`, `()`, and `(al)`, return the interpretation: `G` → `"G"`, `()` → `"o"`, `(al)` → `"al"`.

**Approach:** Scan through the string character by character. When encountering `G`, append `G` and move forward 1. When encountering `(`, look at the next character: if `)` append `o` (move forward 2), otherwise it's `(al)` append `al` (move forward 4).

**Edge Cases:**
- Only `G` characters
- Mixed patterns
- Empty string → empty result

**Python Code:**
```python
def interpret(command: str) -> str:
    result = []
    i = 0
    while i < len(command):
        if command[i] == 'G':
            result.append('G')
            i += 1
        elif command[i:i + 2] == '()':
            result.append('o')
            i += 2
        else:
            result.append('al')
            i += 4
    return ''.join(result)

def interpret_v2(command: str) -> str:
    return command.replace('()', 'o').replace('(al)', 'al')
```

**Time Complexity:** O(n) — single pass (or O(n) for string replacements)  
**Space Complexity:** O(n) — for the result string

---

### Problem 12: Determine if String Has All Unique Characters

**Statement:** Determine if a string contains all unique characters. Try to do it without using additional data structures (constant extra space).

**Approach 1:** Use a boolean array of size 256 (for extended ASCII). For each character, check if it's been seen before. If yes, return False. Otherwise mark it as seen.

**Approach 2:** Without extra data structures, compare every pair of characters — O(n²) time but O(1) space.

**Approach 3:** Sort the string first, then check adjacent characters — O(n log n) time.

**Edge Cases:**
- Empty string → True
- Single character → True
- All same characters → False
- Case sensitivity: 'A' and 'a' are different

**Python Code:**
```python
def is_unique(s: str) -> bool:
    seen = [False] * 256
    for ch in s:
        if seen[ord(ch)]:
            return False
        seen[ord(ch)] = True
    return True

def is_unique_no_extra(s: str) -> bool:
    # O(n^2) time but O(1) space
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            if s[i] == s[j]:
                return False
    return True

def is_unique_sort(s: str) -> bool:
    # O(n log n) time, O(n) space for sorted copy
    sorted_s = sorted(s)
    for i in range(len(sorted_s) - 1):
        if sorted_s[i] == sorted_s[i + 1]:
            return False
    return True
```

**Time Complexity:** O(n) / O(n²) / O(n log n) for the three approaches  
**Space Complexity:** O(1) / O(1) / O(n)

---

### Problem 13: Check if String is a Prefix of Array

**Statement:** Given a string `s` and an array of strings `words`, return True if `s` is a prefix of the concatenation of all strings in `words` in order.

**Approach:** Incrementally build the concatenation string from `words`. After appending each word, check if the built string matches `s`. If it exceeds `s`'s length without matching, return False.

**Edge Cases:**
- `s` is empty → True (empty string is prefix of everything)
- `words` is empty → False (unless s is empty)
- `s` matches exactly the full concatenation → True
- `s` is longer than concatenation → False

**Python Code:**
```python
def is_prefix_string(s: str, words: list[str]) -> bool:
    built = ''
    for word in words:
        built += word
        if built == s:
            return True
        if len(built) > len(s):
            return False
    return False
```

**Time Complexity:** O(n) where n = total characters in words  
**Space Complexity:** O(n) — for the built string

---

### Problem 14: Determine if String Halves Are Alike

**Statement:** Given a string `s` of even length, split it into two halves of equal length. Check if both halves contain the same number of vowels (`a, e, i, o, u` — both uppercase and lowercase).

**Approach:** Count vowels in the first half (indices 0 to n/2-1) and the second half (indices n/2 to n-1). Compare the two counts.

**Edge Cases:**
- No vowels → both 0, return True
- All vowels → both n/2, return True
- Vowels concentrated in one half → False

**Python Code:**
```python
def halves_are_alike(s: str) -> bool:
    vowels = set('aeiouAEIOU')
    n = len(s)
    first = sum(1 for i in range(n // 2) if s[i] in vowels)
    second = sum(1 for i in range(n // 2, n) if s[i] in vowels)
    return first == second
```

**Time Complexity:** O(n) — single pass  
**Space Complexity:** O(1) — only a small set for vowels

---

### Problem 15: Capitalize the Title

**Statement:** Given a string `title` consisting of words separated by single spaces, capitalize each word following these rules: if the word length is 1 or 2, make it all lowercase. If 3 or more, capitalize the first letter and make the rest lowercase.

**Approach:** Split the title into words. For each word, check its length. Apply the appropriate transformation. Join the words back with spaces.

**Edge Cases:**
- Single character words
- Two character words
- Words with mixed casing
- All uppercase input
- All lowercase input

**Python Code:**
```python
def capitalize_title(title: str) -> str:
    words = title.split()
    result = []
    for word in words:
        if len(word) <= 2:
            result.append(word.lower())
        else:
            result.append(word[0].upper() + word[1:].lower())
    return ' '.join(result)

def capitalize_title_v2(title: str) -> str:
    return ' '.join(
        w.capitalize() if len(w) > 2 else w.lower()
        for w in title.split()
    )
```

**Time Complexity:** O(n) — processing each character once  
**Space Complexity:** O(n) — for storing the result words

---

## MEDIUM PROBLEMS (16–45)

---

### Problem 16: Group Shifted Strings

**Statement:** Given a list of strings, group all strings that belong to the same "shift" pattern. A shift is defined by the relative differences between consecutive characters (mod 26). For example, "abc" and "def" belong to the same group because both shift forward by 1.

**Approach:** For each string, compute a normalized pattern by calculating the difference between each character and the first character (mod 26). Strings with the same pattern belong to the same group. Use a hash map to group them.

**Edge Cases:**
- Empty strings
- Single character strings (all map to empty tuple)
- Strings wrapping around 'z' → 'a'

**Python Code:**
```python
from collections import defaultdict

def group_strings(strings: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for s in strings:
        if not s:
            groups[()].append(s)
            continue
        # Normalize: compute relative differences from first char
        pattern = tuple((ord(s[i]) - ord(s[0])) % 26 for i in range(len(s)))
        groups[pattern].append(s)
    return list(groups.values())
```

**Time Complexity:** O(n * m) where n = number of strings, m = average string length  
**Space Complexity:** O(n * m) — for storing all strings in groups

---

### Problem 17: Compare Version Numbers

**Statement:** Compare two version numbers `version1` and `version2`. Return 1 if version1 > version2, -1 if version1 < version2, and 0 if they are equal. Version numbers consist of revisions separated by dots (e.g., "1.01" == "1.001").

**Approach:** Split both version strings by `.` to get revision lists. Pad the shorter list with zeros. Compare corresponding revisions lexicographically — first difference determines the result.

**Edge Cases:**
- Different number of revisions ("1.0" vs "1.0.0")
- Leading zeros ("1.01" == "1.1")
- Single revision versions ("2" vs "10")

**Python Code:**
```python
def compare_version(version1: str, version2: str) -> int:
    v1 = list(map(int, version1.split('.')))
    v2 = list(map(int, version2.split('.')))
    max_len = max(len(v1), len(v2))
    for i in range(max_len):
        num1 = v1[i] if i < len(v1) else 0
        num2 = v2[i] if i < len(v2) else 0
        if num1 > num2:
            return 1
        elif num1 < num2:
            return -1
    return 0
```

**Time Complexity:** O(n) where n = number of revision parts  
**Space Complexity:** O(n) — for the integer arrays

---

### Problem 18: String Compression

**Statement:** Given a character array `chars`, compress it in-place using the following rule: groups of consecutive identical characters are replaced by the character followed by the count (if count > 1). Return the new length.

**Approach:** Use two pointers: `read` scans through the array, `write` builds the compressed result. Count consecutive characters. Write the character, then write each digit of the count (only if count > 1). Return `write` position.

**Edge Cases:**
- Single character → "a" (no count)
- All same characters → "a4" for "aaaa"
- Already compressed → unchanged
- No consecutive duplicates → unchanged

**Python Code:**
```python
def compress(chars: list[str]) -> int:
    write = 0
    read = 0
    while read < len(chars):
        char = chars[read]
        count = 0
        # Count all consecutive occurrences
        while read < len(chars) and chars[read] == char:
            read += 1
            count += 1
        # Write the character
        chars[write] = char
        write += 1
        # Write the count if > 1
        if count > 1:
            for digit in str(count):
                chars[write] = digit
                write += 1
    return write
```

**Time Complexity:** O(n) — each character is read and written once  
**Space Complexity:** O(1) — in-place modification

---

### Problem 19: Reorganize String

**Statement:** Given a string `s`, rearrange it so that no two adjacent characters are the same. Return the rearranged string, or an empty string if it's impossible.

**Approach:** Count character frequencies. The most frequent character must not exceed `(n+1)/2`. Place the most frequent character at even indices (0, 2, 4...), then fill remaining characters at odd indices and subsequent positions.

**Why even indices first:** This ensures the most frequent character is maximally separated.

**Edge Cases:**
- Single character → return it
- Two different characters → always possible
- One character dominates → impossible
- All characters same length 1 → return it

**Python Code:**
```python
from collections import Counter

def reorganize_string(s: str) -> str:
    count = Counter(s)
    n = len(s)
    max_char, max_count = count.most_common(1)[0]
    if max_count > (n + 1) // 2:
        return ""
    result = [''] * n
    idx = 0
    # Place most frequent at even indices
    for _ in range(max_count):
        result[idx] = max_char
        idx += 2
    # Place remaining characters
    for ch, c in count.items():
        if ch == max_char:
            continue
        for _ in range(c):
            if idx >= n:
                idx = 1  # Switch to odd indices
            result[idx] = ch
            idx += 2
    return ''.join(result)
```

**Time Complexity:** O(n)  
**Space Complexity:** O(n) — for the result array

---

### Problem 20: Repeated Substring Pattern

**Statement:** Given a string `s`, check if it can be constructed by taking a substring and appending multiple copies of it (at least 2 copies). Return True/False.

**Approach 1:** Mathematical — if `s` has this property, then `s` must be found in `(s + s)[1:-1]` (concatenation minus first and last character). This works because the doubled string contains all possible rotations/substrings.

**Approach 2:** Check all possible substring lengths that divide `n`. For each, verify if repeating the substring gives back `s`.

**Edge Cases:**
- Length 1 → False (need at least 2 copies)
- "abab" → True ("ab" repeated)
- "aba" → False
- "abcabc" → True ("abc" repeated)
- "abcabd" → False

**Python Code:**
```python
def repeated_substring_pattern(s: str) -> bool:
    # Elegant O(n) approach
    doubled = (s + s)[1:-1]
    return s in doubled

def repeated_substring_pattern_v2(s: str) -> bool:
    # Brute force approach for understanding
    n = len(s)
    for length in range(1, n // 2 + 1):
        if n % length == 0:
            substring = s[:length]
            if substring * (n // length) == s:
                return True
    return False
```

**Time Complexity:** O(n) for the first, O(n²) for the second  
**Space Complexity:** O(n) — for the doubled string

---

### Problem 21: Longest Uncommon Subsequence I

**Statement:** Given two strings `a` and `b`, find the length of the longest uncommon subsequence. An uncommon subsequence is a string that is a subsequence of one but not the other. Return -1 if none exists.

**Approach:** If strings are equal, they have the same subsequences, so return -1. Otherwise, the longer string (or either string if equal length) is itself an uncommon subsequence since it cannot be a subsequence of the shorter one.

**Key Insight:** If `a != b`, then `a` is not a subsequence of `b` (or vice versa), so the longer one is the answer.

**Edge Cases:**
- `a == b` → -1
- Different lengths → return length of longer
- Same length but different → return length of either

**Python Code:**
```python
def find_lu_slength(a: str, b: str) -> int:
    if a == b:
        return -1
    return max(len(a), len(b))
```

**Time Complexity:** O(n) — for string comparison  
**Space Complexity:** O(1)

---

### Problem 22: Longest Uncommon Subsequence II

**Statement:** Given a list of strings `strs`, find the length of the longest uncommon subsequence among them. An uncommon subsequence of a group is a string that is not a subsequence of any other string in the group.

**Approach:** Sort strings by length (descending). For each string (longest first), check if it's a subsequence of any longer or equal-length string. The first string that is NOT a subsequence of any other is the answer.

**Why sort by length:** The longest string can't be a subsequence of a shorter one, so we only need to check strings of equal or greater length.

**Edge Cases:**
- All strings identical → -1
- One string is a subsequence of another → use the longer one
- Multiple strings of same length → check each

**Python Code:**
```python
def find_lu_slength_ii(strs: list[str]) -> int:
    def is_subsequence(a: str, b: str) -> bool:
        it = iter(b)
        return all(ch in it for ch in a)

    # Sort by length descending
    strs.sort(key=len, reverse=True)
    for i in range(len(strs)):
        is_sub = False
        for j in range(len(strs)):
            if i != j and len(strs[i]) <= len(strs[j]):
                if is_subsequence(strs[i], strs[j]):
                    is_sub = True
                    break
        if not is_sub:
            return len(strs[i])
    return -1
```

**Time Complexity:** O(n² * m) where n = number of strings, m = max string length  
**Space Complexity:** O(1) — excluding input storage

---

### Problem 23: Count Substrings with Only One Distinct Letter

**Statement:** Given a string `s`, return the number of substrings that contain only one distinct letter. The answer can be very large, return modulo 10^9 + 7.

**Approach:** Identify runs of consecutive identical characters. For a run of length `k`, the number of valid substrings is `k * (k + 1) / 2` (all contiguous substrings within the run). Sum across all runs.

**Why k*(k+1)/2:** For a run of length k, substrings of length 1: k, length 2: k-1, ..., length k: 1. Total = k(k+1)/2.

**Edge Cases:**
- All same characters "aaaa" → 4*5/2 = 10
- Alternating "abab" → 4 (each single char)
- Single character → 1

**Python Code:**
```python
def count_homogenous_substrings(s: str) -> int:
    result = 0
    count = 1
    MOD = 10**9 + 7
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result = (result + count * (count + 1) // 2) % MOD
            count = 1
    # Don't forget the last run
    result = (result + count * (count + 1) // 2) % MOD
    return result
```

**Time Complexity:** O(n) — single pass  
**Space Complexity:** O(1)

---

### Problem 24: Minimum Distance Between Adjacent Sorted Strings

**Statement:** Given a list of strings, sort them alphabetically and find the minimum "distance" between any two adjacent strings. The distance is the number of positions where characters differ (padding shorter string with nothing).

**Approach:** Sort the strings. For each adjacent pair, compute character-wise Hamming distance plus the length difference. Track the minimum across all pairs.

**Edge Cases:**
- Single string → undefined (return 0)
- All identical strings → 0
- Very different strings → large distance
- Different length strings

**Python Code:**
```python
def min_distance_adjacent(words: list[str]) -> int:
    words.sort()
    min_dist = float('inf')
    for i in range(len(words) - 1):
        a, b = words[i], words[i + 1]
        # Count character differences
        dist = sum(1 for ca, cb in zip(a, b) if ca != cb)
        # Add length difference
        dist += abs(len(a) - len(b))
        min_dist = min(min_dist, dist)
    return min_dist
```

**Time Complexity:** O(n log n + n * m) where m = average string length  
**Space Complexity:** O(1)

---

### Problem 25: Longest Nice Substring

**Statement:** A string is "nice" if for every lowercase letter, its uppercase version also exists in the string (and vice versa). Find the longest nice substring. Return empty string if none exists.

**Approach:** Divide and conquer. Find any character that violates the nice property (its swapcase counterpart is not in the string). Split the string at that character's positions. Recursively solve both halves. Return the longer result.

**Edge Cases:**
- Length < 2 → no nice substring possible
- Already nice → return entire string
- "YazaAa" → "aAa" (length 3)

**Python Code:**
```python
def longest_nice_substring(s: str) -> str:
    if len(s) < 2:
        return ""
    chars = set(s)
    for i, ch in enumerate(s):
        if ch.swapcase() not in chars:
            left = longest_nice_substring(s[:i])
            right = longest_nice_substring(s[i + 1:])
            return left if len(left) >= len(right) else right
    return s  # Entire string is nice
```

**Time Complexity:** O(n) per level × O(n) levels worst case = O(n²)  
**Space Complexity:** O(n) — for recursive call stack and substrings

---

### Problem 26: Count Number of Homogenous Substrings

**Statement:** Given a string `s`, return the number of homogenous substrings (where all characters are the same) modulo 10^9 + 7.

**Approach:** Scan for consecutive runs of identical characters. For each run of length `k`, contribute `k*(k+1)/2` to the total. Sum all contributions.

**Edge Cases:**
- Single character → 1
- "aab" → 3 (aa, a, b) → actually "a", "a", "b", "aa" = 4
- All same "aaaa" → 10

**Python Code:**
```python
def count_homogenous(s: str) -> int:
    result = 0
    count = 1
    MOD = 10**9 + 7
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result = (result + count * (count + 1) // 2) % MOD
            count = 1
    result = (result + count * (count + 1) // 2) % MOD
    return result
```

**Time Complexity:** O(n)  
**Space Complexity:** O(1)

---

### Problem 27: Check if Word Equals Sum of Two Words

**Statement:** Given string arrays `firstWord` and `secondWord`, and a string `targetWord`, each string represents a number where `'a'` = 1, `'b'` = 2, ..., `'z'` = 26. Check if the numeric value of `firstWord + secondWord` equals that of `targetWord`.

**Approach:** Create a helper function that converts a word to its numeric value by summing `(ord(ch) - ord('a') + 1)` for each character. Compare the sums.

**Edge Cases:**
- Empty strings → sum is 0
- Single character words
- Large values (sum can exceed integer range? No, Python handles big integers)

**Python Code:**
```python
def is_sum_equal(first_word: str, second_word: str, target_word: str) -> bool:
    def word_to_num(word: str) -> int:
        return sum(ord(ch) - ord('a') + 1 for ch in word)
    return word_to_num(first_word) + word_to_num(second_word) == word_to_num(target_word)
```

**Time Complexity:** O(n) where n = total characters in all three words  
**Space Complexity:** O(1)

---

### Problem 28: Maximum Number of Vowels in Substring of Given Length

**Statement:** Given a string `s` and integer `k`, find the maximum number of vowels in any substring of length `k`.

**Approach:** Sliding window. Count vowels in the first window of size `k`. Then slide the window right: add the new character's contribution, subtract the character leaving the window. Track the maximum.

**Edge Cases:**
- k equals string length → count all vowels
- No vowels → 0
- All vowels → k
- k = 1 → 1 if any vowel present

**Python Code:**
```python
def max_vowels(s: str, k: int) -> int:
    vowels = set('aeiou')
    count = sum(1 for i in range(k) if s[i] in vowels)
    max_count = count
    for i in range(k, len(s)):
        if s[i] in vowels:
            count += 1
        if s[i - k] in vowels:
            count -= 1
        max_count = max(max_count, count)
    return max_count
```

**Time Complexity:** O(n) — single pass with sliding window  
**Space Complexity:** O(1) — fixed set of vowels

---

### Problem 29: Grumpy Bookstore Owner

**Statement:** A bookstore owner is grumpy at certain minutes. `customers[i]` customers arrive at minute `i`, and `grumpy[i]` is 1 if the owner is grumpy then (customers leave unsatisfied). The owner can use a secret technique for `minutes` consecutive minutes to suppress grumpiness. Find the maximum number of satisfied customers.

**Approach:** Without the technique, count all customers when the owner is NOT grumpy. Then use a sliding window of size `minutes` to find the maximum number of additional customers that could be saved (customers who arrive during grumpy periods within the window). Add base + max saved.

**Edge Cases:**
- minutes = 0 → only base satisfaction
- minutes >= len(customers) → save all grumpy customers
- No grumpy minutes → all customers satisfied

**Python Code:**
```python
def max_satisfied(customers: list[int], grumpy: list[int], minutes: int) -> int:
    # Base satisfaction: customers when not grumpy
    base = sum(c for c, g in zip(customers, grumpy) if g == 0)
    # Sliding window: find max customers that can be saved
    window_save = sum(c * g for c, g in zip(customers[:minutes], grumpy[:minutes]))
    max_save = window_save
    for i in range(minutes, len(customers)):
        window_save += customers[i] * grumpy[i]
        window_save -= customers[i - minutes] * grumpy[i - minutes]
        max_save = max(max_save, window_save)
    return base + max_save
```

**Time Complexity:** O(n)  
**Space Complexity:** O(1)

---

### Problem 30: Minimum Number of Flips to Make Binary String Alternating

**Statement:** Given a binary string `s`, you can perform two operations: flip any character to its opposite, or rotate the string by one position (move last char to front). Find the minimum number of flips needed to make the string alternating.

**Approach:** Since rotation is free (we just consider all rotations), and any rotation of an alternating string is also alternating, we just need to find the minimum flips to make `s` (or any rotation) match one of two alternating patterns: "0101..." or "1010...". Use a sliding window on the doubled string.

**Edge Cases:**
- Already alternating → 0
- All same characters → n/2
- Length 1 → 0

**Python Code:**
```python
def min_flips(s: str) -> int:
    n = len(s)
    doubled = s + s
    # Count mismatches for pattern starting with '0' and '1'
    count0 = count1 = 0
    for i in range(n):
        if doubled[i] != str(i % 2):
            count0 += 1
        if doubled[i] != str(1 - i % 2):
            count1 += 1
    result = min(count0, count1)
    # Slide the window through the doubled string
    for i in range(n, 2 * n):
        if doubled[i] != str(i % 2):
            count0 += 1
        if doubled[i] != str(1 - i % 2):
            count1 += 1
        if doubled[i - n] != str((i - n) % 2):
            count0 -= 1
        if doubled[i - n] != str(1 - (i - n) % 2):
            count1 -= 1
        result = min(result, count0, count1)
    return result
```

**Time Complexity:** O(n) — sliding window on doubled string  
**Space Complexity:** O(n) — for the doubled string

---

### Problem 31: Find the Index of the First Occurrence

**Statement:** Implement `strStr()` — find the index of the first occurrence of substring `needle` in string `haystack`. Return -1 if `needle` is not found. If `needle` is empty, return 0.

**Approach:** Slide a window of size `len(needle)` over `haystack`. For each position, check if the substring matches `needle`. Return the first matching index.

**Edge Cases:**
- Empty needle → 0
- Needle longer than haystack → -1
- Needle at the start → 0
- Needle at the end → n - m
- Needle not found → -1

**Python Code:**
```python
def str_str(haystack: str, needle: str) -> int:
    if not needle:
        return 0
    n, m = len(haystack), len(needle)
    for i in range(n - m + 1):
        if haystack[i:i + m] == needle:
            return i
    return -1
```

**Time Complexity:** O(n * m) worst case  
**Space Complexity:** O(m) — for the substring comparison

---

### Problem 32: Remove All Adjacent Duplicates in String II

**Statement:** Given a string `s` and integer `k`, remove `k` adjacent and identical characters repeatedly until no more removals are possible.

**Approach:** Use a stack where each element is `(character, consecutive_count)`. For each new character: if it matches the top of the stack, increment the count; if count reaches `k`, pop it. Otherwise push a new entry with count 1.

**Edge Cases:**
- k = 1 → remove all characters
- No duplicates → return original
- Multiple cascading removals (e.g., "deeedbbccbdb" with k=3)
- Result could be empty

**Python Code:**
```python
def remove_duplicates(s: str, k: int) -> str:
    stack = []  # Each element: (char, count)
    for ch in s:
        if stack and stack[-1][0] == ch:
            stack[-1] = (ch, stack[-1][1] + 1)
            if stack[-1][1] == k:
                stack.pop()
        else:
            stack.append((ch, 1))
    return ''.join(ch * count for ch, count in stack)
```

**Time Complexity:** O(n) — each character pushed and popped at most once  
**Space Complexity:** O(n) — stack storage

---

### Problem 33: Repeated String Match

**Statement:** Given two strings `a` and `b`, find the minimum number of times `a` must be repeated so that `b` becomes a substring of the repeated string. Return -1 if impossible.

**Approach:** Repeat `a` until the total length is at least `len(b)`. Check if `b` is a substring. If not, repeat one more time and check again. If still not found, return -1 (because at most `ceil(len(b)/len(a)) + 1` repeats are needed).

**Edge Cases:**
- `b` is empty → 0
- `a` already contains `b` → 1
- `a` and `b` share no characters → -1
- `b` requires exactly `ceil(len(b)/len(a))` repeats

**Python Code:**
```python
def repeated_string_match(a: str, b: str) -> int:
    repeated = a
    count = 1
    # Keep repeating until long enough
    while len(repeated) < len(b):
        repeated += a
        count += 1
    # Check current and one more repeat
    if b in repeated:
        return count
    if b in repeated + a:
        return count + 1
    return -1
```

**Time Complexity:** O(n * m) where n = len(repeated), m = len(b)  
**Space Complexity:** O(n + m) — for the repeated string

---

### Problem 34: Check if a String Contains All Binary Codes of Size K

**Statement:** Given a binary string `s` and integer `k`, check if every possible binary code of length `k` exists as a substring of `s`.

**Approach:** There are exactly `2^k` possible binary codes of length `k`. Use a sliding window to extract all substrings of length `k` from `s` and store them in a set. If the set size reaches `2^k`, all codes exist.

**Edge Cases:**
- k = 0 → return True (empty string is always present)
- s shorter than k → impossible, return False
- s length exactly k → check if it's the only code

**Python Code:**
```python
def has_all_codes(s: str, k: int) -> bool:
    required = 1 << k  # 2^k
    seen = set()
    for i in range(len(s) - k + 1):
        seen.add(s[i:i + k])
        if len(seen) == required:
            return True
    return False
```

**Time Complexity:** O(n) where n = len(s)  
**Space Complexity:** O(2^k) — for storing all unique substrings

---

### Problem 35: Minimum Deletions to Make Character Frequencies Unique

**Statement:** Given a string `s`, find the minimum number of deletions needed so that every character appears a unique number of times.

**Approach:** Count character frequencies. Sort them in descending order. For each frequency, if it's already used, decrease it until it's unique (or zero, meaning delete all remaining). Track total deletions.

**Edge Cases:**
- All characters unique frequency → 0 deletions
- All same frequency → reduce each to unique values
- "aabbcc" → frequencies [2,2,2] → [2,1,0] → 2 deletions

**Python Code:**
```python
def min_deletions(s: str) -> int:
    from collections import Counter
    freq = list(Counter(s).values())
    freq.sort(reverse=True)
    deletions = 0
    used = set()
    for f in freq:
        # Decrease f until it's unique or zero
        while f > 0 and f in used:
            f -= 1
            deletions += 1
        used.add(f)
    return deletions
```

**Time Complexity:** O(n + k log k) where k = unique characters (k ≤ 26)  
**Space Complexity:** O(k) — for the frequency set

---

### Problem 36: Sum of Digits of String After Convert

**Statement:** Given a string `s` of lowercase letters and integer `k`, first convert each letter to its position (a→1, b→2, ..., z→26), concatenate all digits, then perform digit sum operation `k` times.

**Approach:** First, build a numeric string by converting each character. Then, in each of `k` iterations, compute the sum of digits. The result after `k` transforms is the answer.

**Edge Cases:**
- k = 0 → return the initial digit sum
- Very large intermediate values
- Single character input
- Letters mapping to multi-digit numbers (z → 26)

**Python Code:**
```python
def get_lucky(s: str, k: int) -> int:
    # Step 1: Convert letters to digits
    num_str = ''
    for ch in s:
        num_str += str(ord(ch) - ord('a') + 1)
    # Step 2: Apply digit sum k times
    total = sum(int(ch) for ch in num_str)
    for _ in range(k - 1):
        total = sum(int(ch) for ch in str(total))
    return total
```

**Time Complexity:** O(n + k * log(total)) where log(total) is digits count  
**Space Complexity:** O(n) — for the numeric string

---

### Problem 37: Largest Substring Between Two Equal Characters

**Statement:** Given a string `s`, find the length of the largest substring between two equal characters, not including the characters themselves. Return -1 if no two characters are the same.

**Approach:** For each character, store its first occurrence. When the same character appears again, calculate the distance between the two occurrences minus 2 (excluding both endpoints). Track the maximum.

**Edge Cases:**
- All unique characters → -1
- First and last characters are the same → n - 2
- "abca" → "bc" between a's → length 2
- "cbzxy" → -1 (all unique)

**Python Code:**
```python
def max_length_between_equal_characters(s: str) -> int:
    first_occurrence = {}
    max_len = -1
    for i, ch in enumerate(s):
        if ch in first_occurrence:
            # Length between first and current occurrence (exclusive)
            max_len = max(max_len, i - first_occurrence[ch] - 1)
        else:
            first_occurrence[ch] = i
    return max_len
```

**Time Complexity:** O(n) — single pass  
**Space Complexity:** O(n) — for the hash map

---

### Problem 38: Minimum Length of String After Deleting Similar Ends

**Statement:** Given a string `s`, you can remove characters from both ends if the characters at both ends are the same. Return the minimum possible length after performing any number of such operations.

**Approach:** Two pointers from both ends. When both pointers point to the same character, remove all occurrences of that character from both ends (advance left past all matching chars, retreat right past all matching chars). Repeat until characters differ or pointers cross.

**Edge Cases:**
- Empty string → 0
- All same characters → 0
- Different characters at ends → return original length
- "cabaabac" → 0

**Python Code:**
```python
def minimum_length(s: str) -> int:
    left, right = 0, len(s) - 1
    while left < right and s[left] == s[right]:
        ch = s[left]
        # Skip all matching characters from left
        while left <= right and s[left] == ch:
            left += 1
        # Skip all matching characters from right
        while left <= right and s[right] == ch:
            right -= 1
    return right - left + 1
```

**Time Complexity:** O(n) — each character visited at most once  
**Space Complexity:** O(1)

---

### Problem 39: Longest Substring with At Most K Distinct Characters

**Statement:** Given a string `s` and integer `k`, find the length of the longest substring that contains at most `k` distinct characters.

**Approach:** Sliding window with a frequency dictionary. Expand the right boundary. When distinct character count exceeds `k`, shrink from the left until the constraint is satisfied. Track the maximum window size.

**Edge Cases:**
- k = 0 → return 0 (no characters allowed)
- k ≥ number of unique characters → return n
- All same characters → return n
- k = 1 → longest run of same character

**Python Code:**
```python
def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    from collections import defaultdict
    count = defaultdict(int)
    left = 0
    max_len = 0
    for right in range(len(s)):
        count[s[right]] += 1
        while len(count) > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len
```

**Time Complexity:** O(n) — each character added and removed at most once  
**Space Complexity:** O(k) — at most k entries in the dictionary

---

### Problem 40: Minimum Window Subsequence

**Statement:** Given strings `s1` and `s2`, find the minimum (smallest) window in `s1` that contains `s2` as a subsequence. If no such window exists, return empty string.

**Approach:** For each starting position in `s1` where `s2[0]` matches, greedily find the shortest window by: (1) scan forward to match all of `s2`, (2) scan backward from the end to find the tightest window. Track the minimum length window across all starting positions.

**Edge Cases:**
- `s2` empty → return empty string
- `s2` longer than `s1` → impossible
- `s1` == `s2` → return `s1`
- Multiple valid windows → return the shortest

**Python Code:**
```python
def min_window(s1: str, s2: str) -> str:
    n, m = len(s1), len(s2)
    result = ""
    min_len = float('inf')
    for i in range(n):
        if s1[i] == s2[0]:
            # Forward pass: match s2
            j, k = 0, i
            while k < n and j < m:
                if s1[k] == s2[j]:
                    j += 1
                k += 1
            if j == m:
                # Backward pass: find tightest start
                end = k - 1
                j = m - 1
                start = end
                while j >= 0:
                    if s1[start] == s2[j]:
                        j -= 1
                    start -= 1
                start += 1
                if end - start + 1 < min_len:
                    min_len = end - start + 1
                    result = s1[start:end + 1]
    return result
```

**Time Complexity:** O(n * m) — for each start position, O(n + m) work  
**Space Complexity:** O(1) — only pointers and result tracking

---

### Problem 41: Number of Matching Subsequences

**Statement:** Given a string `s` and a list of words, count how many words are subsequences of `s`.

**Approach:** For each word, check if it's a subsequence of `s` using binary search. Precompute positions of each character in `s`. For each character in the word, binary search for the next valid position. Optimize by grouping words by their first character.

**Edge Cases:**
- Empty words → all are subsequences
- Words with characters not in `s` → 0
- Duplicates in words → each counted separately

**Python Code:**
```python
def num_matching_subseq(s: str, words: list[str]) -> int:
    from collections import defaultdict
    # Build position index for each character
    positions = defaultdict(list)
    for i, ch in enumerate(s):
        positions[ch].append(i)
    count = 0
    for word in words:
        prev = -1
        is_sub = True
        for ch in word:
            if ch not in positions:
                is_sub = False
                break
            # Binary search for next position > prev
            idx = -1
            lo, hi = 0, len(positions[ch]) - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if positions[ch][mid] > prev:
                    idx = mid
                    hi = mid - 1
                else:
                    lo = mid + 1
            if idx == -1:
                is_sub = False
                break
            prev = positions[ch][idx]
        if is_sub:
            count += 1
    return count
```

**Time Complexity:** O(n + m * log(n)) where m = total characters in all words  
**Space Complexity:** O(n) — for the position index

---

### Problem 42: Valid Palindrome III

**Statement:** Given a string `s` and integer `k`, return True if `s` is a palindrome or can become one by removing at most `k` characters.

**Approach:** Find the length of the Longest Palindromic Subsequence (LPS) of `s`. The LPS can be found using LCS of `s` and `reverse(s)`. If `len(s) - LPS <= k`, it's possible.

**Why this works:** We need to keep a palindromic subsequence. The longer the LPS, the fewer deletions needed. If deletions needed ≤ k, it's valid.

**Edge Cases:**
- k = 0 → s must already be a palindrome
- k ≥ n - 1 → always possible (keep at least one char)
- Already a palindrome → True

**Python Code:**
```python
def is_valid_palindrome(s: str, k: int) -> bool:
    n = len(s)
    # Space-optimized LCS of s and reverse(s)
    prev = [0] * n
    curr = [0] * n
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j]:
                curr[j] = (prev[j - 1] + 2) if j > i else 1
            else:
                curr[j] = max(prev[j], curr[j - 1]) if j > i else 0
        prev, curr = curr, [0] * n
    lps = prev[n - 1]
    return n - lps <= k
```

**Time Complexity:** O(n²) — for the LPS DP computation  
**Space Complexity:** O(n) — space-optimized DP

---

### Problem 43: Stream of Characters

**Statement:** Design a stream system that receives characters one at a time. After each character, check if any suffix of the accumulated string matches a word in a given word list. Return True/False for each query.

**Approach:** Build a trie of all words in reverse (since we check suffixes). For each incoming character, traverse the trie from the latest character backward through the stream. If any word boundary is reached, return True.

**Edge Cases:**
- Words of varying lengths
- Stream shorter than any word → False
- Multiple words can match at different points

**Python Code:**
```python
class StreamChecker:
    def __init__(self, words: list[str]):
        self.trie = {}
        self.stream = []
        # Build trie with words inserted in reverse
        for word in words:
            node = self.trie
            for ch in reversed(word):
                if ch not in node:
                    node[ch] = {}
                node = node[ch]
            node['#'] = True  # Mark end of word

    def query(self, letter: str) -> bool:
        self.stream.append(letter)
        node = self.trie
        # Traverse stream in reverse (check suffix)
        for ch in reversed(self.stream):
            if '#' in node:
                return True
            if ch not in node:
                return False
            node = node[ch]
        return '#' in node
```

**Time Complexity:** O(k) per query where k = max word length  
**Space Complexity:** O(sum of all word lengths) — for the trie

---

### Problem 44: Camelcase Matching

**Statement:** Given a list of words and a pattern, check which words match the pattern. A word matches if pattern characters appear in order within the word, with uppercase characters in the word needing exact matches.

**Approach:** For each word, use two pointers — one for the word, one for the pattern. Match pattern characters in order. Any uppercase character in the word that doesn't match the pattern means failure. After exhausting the pattern, remaining word characters must be lowercase.

**Edge Cases:**
- Pattern contains uppercase → must match uppercase in word
- Word with no uppercase → only lowercase matching
- Pattern longer than word → impossible
- Empty pattern → all lowercase words match

**Python Code:**
```python
def camel_match(queries: list[str], pattern: str) -> list[bool]:
    def matches(word: str) -> bool:
        i, j = 0, 0  # i for word, j for pattern
        while i < len(word) and j < len(pattern):
            if word[i] == pattern[j]:
                i += 1
                j += 1
            elif word[i].isupper():
                return False  # Uppercase doesn't match pattern
            else:
                i += 1  # Skip lowercase that doesn't match
        # Any remaining uppercase in word means mismatch
        while i < len(word):
            if word[i].isupper():
                return False
            i += 1
        return j == len(pattern)  # All pattern chars consumed

    return [matches(q) for q in queries]
```

**Time Complexity:** O(n * m) where n = number of queries, m = max word length  
**Space Complexity:** O(1) — excluding output

---

### Problem 45: Alert Using Same Key-Card Three or More Times in a One Hour Period

**Statement:** Given lists of names, times, and key-cards, find all people who swiped their key-card 3 or more times within any 1-hour period (60 minutes). Return sorted list of names.

**Approach:** Group all swipe times by person's name. Sort each person's times. Use a sliding window of size 3: if the difference between the 3rd and 1st swipe in any window is ≤ 60 minutes, that person gets an alert.

**Edge Cases:**
- Fewer than 3 swipes → no alert
- Exactly 60 minutes apart → alert (≤ 60)
- Multiple alerting windows for same person → report once
- Times across midnight → not applicable per constraints

**Python Code:**
```python
def alert_names(name: list[str], time: list[str]) -> list[str]:
    from collections import defaultdict
    # Group times by name
    logs = defaultdict(list)
    for n, t in zip(name, time):
        h, m = map(int, t.split(':'))
        logs[n].append(h * 60 + m)
    result = []
    for person in sorted(logs.keys()):
        times = sorted(logs[person])
        # Check every window of 3 consecutive swipes
        for i in range(len(times) - 2):
            if times[i + 2] - times[i] <= 60:
                result.append(person)
                break  # One alert is enough per person
    return result
```

**Time Complexity:** O(n log n) — for sorting times per person  
**Space Complexity:** O(n) — for storing the grouped logs

---

## HARD PROBLEMS (46–50)

---

### Problem 46: Minimum Replacement to Sort the Array

**Statement:** Given an integer array `nums`, in one operation you can replace any element with two non-negative integers that sum to it. Find the minimum number of operations to make the array sorted in non-decreasing order.

**Approach:** Traverse from right to left. Track the current maximum allowed value. If `nums[i] > max_allowed`, calculate how many parts to split into: `ceil(nums[i] / max_allowed)`. The minimum of the resulting parts becomes the new `max_allowed`.

**Key Insight:** By splitting optimally, we ensure each piece is ≤ the next element. The greedy approach from right to left ensures minimal splits.

**Edge Cases:**
- Already sorted → 0 operations
- Decreasing array → many operations needed
- Single element → 0
- Large numbers requiring many splits

**Python Code:**
```python
def min_operations(nums: list[int]) -> int:
    n = len(nums)
    operations = 0
    last = nums[-1]  # Rightmost element is the initial max allowed
    for i in range(n - 2, -1, -1):
        if nums[i] > last:
            # Need to split nums[i] into parts where each ≤ last
            parts = (nums[i] + last - 1) // last  # ceil division
            operations += parts - 1
            # The minimum part becomes the new bound
            last = nums[i] // parts
        else:
            last = nums[i]
    return operations
```

**Time Complexity:** O(n) — single pass from right to left  
**Space Complexity:** O(1) — only a few variables

---

### Problem 47: Longest Palindromic Subsequence

**Statement:** Given a string `s`, find the length of the longest palindromic subsequence. A subsequence is obtained by deleting some (or no) characters without changing the order.

**Approach:** The LPS of `s` equals the LCS (Longest Common Subsequence) of `s` and `reverse(s)`. Use space-optimized DP for LCS. Alternatively, use direct DP where `dp[i][j]` = LPS length for `s[i..j]`.

**Key Insight:** A palindromic subsequence reads the same forward and backward, which is exactly what LCS with reversed string computes.

**Edge Cases:**
- Single character → 1
- All same characters → n
- "abcba" → 5 (entire string)
- "ace" → 1 (any single character)
- "aab" → 2 ("aa")

**Python Code:**
```python
def longest_palindrome_subseq(s: str) -> int:
    n = len(s)
    # Space-optimized: use two rows
    prev = [0] * n
    curr = [0] * n
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j]:
                curr[j] = (prev[j - 1] + 2) if j > i else 1
            else:
                curr[j] = max(prev[j], curr[j - 1]) if j > i else 0
        prev, curr = curr, [0] * n
    return prev[n - 1]

def longest_palindrome_subseq_dp(s: str) -> int:
    # Full n×n DP approach for clarity
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1  # Single character is palindrome of length 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]
```

**Time Complexity:** O(n²) — for both approaches  
**Space Complexity:** O(n) for the first, O(n²) for the second

---

### Problem 48: Max Value of Equation

**Statement:** Given a list of 2D points sorted by x-coordinate and an integer `k`, find the maximum value of `yi + yj - |xi - xj|` for any two points where `|xi - xj| ≤ k`.

**Approach:** Since points are sorted by x, `|xi - xj| = xj - xi` when `j > i`. The expression becomes `(yi + xi) + (yj - xj)`. Use a deque to maintain the maximum `yi + xi` within the sliding window of size `k`.

**Why deque:** We need the maximum of `yi + xi` among points within distance `k`. The deque stores candidates in decreasing order of `yi + xi`.

**Edge Cases:**
- Only two points → compute directly
- All points within distance k → check all pairs
- Points at exactly distance k → included (≤ k)

**Python Code:**
```python
from collections import deque

def find_max_value_of_equation(points: list[list[int]], k: int) -> int:
    dq = deque()  # Stores (x, y+x) in decreasing order of y+x
    max_val = float('-inf')
    for x, y in points:
        # Remove points outside the window
        while dq and x - dq[0][0] > k:
            dq.popleft()
        # Compute with best candidate
        if dq:
            max_val = max(max_val, dq[0][1] + y - x)
        # Maintain deque property: remove smaller y+x values
        while dq and y + x >= dq[-1][1]:
            dq.pop()
        dq.append((x, y + x))
    return max_val
```

**Time Complexity:** O(n) — each point enters and leaves deque at most once  
**Space Complexity:** O(n) — worst case all points in deque

---

### Problem 49: Number of Ways to Split a String

**Statement:** Given a binary string `s`, count the number of ways to split it into three non-empty parts that each contain the same number of `1`s. Return the answer modulo 10^9 + 7.

**Approach:** Count total `1`s. If not divisible by 3, return 0. If all zeros, the answer is `C(n-1, 2)` (choose any 2 split points). Otherwise, find how many positions end the first third and second third of `1`s. The answer is `count1 × count2`.

**Edge Cases:**
- No `1`s → `(n-1 choose 2)` ways to split
- Total `1`s not divisible by 3 → 0
- `1`s concentrated → fewer valid splits
- Minimum string length 3

**Python Code:**
```python
def num_ways(s: str) -> int:
    total_ones = s.count('1')
    MOD = 10**9 + 7
    if total_ones == 0:
        # Any two split points work
        n = len(s) - 1
        return n * (n - 1) // 2 % MOD
    if total_ones % 3 != 0:
        return 0
    target = total_ones // 3
    # Count positions where 1st third ends and 2nd third ends
    count1 = count2 = 0
    ones = 0
    for i in range(len(s)):
        if s[i] == '1':
            ones += 1
        if ones == target:
            count1 += 1
        if ones == 2 * target:
            count2 += 1
    return (count1 * count2) % MOD
```

**Time Complexity:** O(n) — single pass  
**Space Complexity:** O(1) — only counters

---

### Problem 50: Longest Substring with At Most Two Distinct Characters

**Statement:** Given a string `s`, find the length of the longest substring that contains at most two distinct characters.

**Approach:** Sliding window with a frequency dictionary. Expand the right pointer. When more than 2 distinct characters exist in the window, shrink from the left until the constraint is restored. Track maximum window size throughout.

**Note:** This is the k=2 special case of Problem 39, but included as it's a classic interview problem.

**Edge Cases:**
- Empty string → 0
- All same characters → n
- Two distinct characters → n
- Three or more distinct → need to shrink window

**Python Code:**
```python
def length_of_longest_substring_two_distinct(s: str) -> int:
    from collections import defaultdict
    count = defaultdict(int)
    left = 0
    max_len = 0
    for right in range(len(s)):
        count[s[right]] += 1
        # Shrink window if more than 2 distinct characters
        while len(count) > 2:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len
```

**Time Complexity:** O(n) — each character added and removed at most once  
**Space Complexity:** O(1) — at most 3 entries in the dictionary

---

---

## Additional Practice Notes

### String Problem Patterns to Master

1. **Two Pointers:** Problems 1, 14, 38, 50 — use two pointers to scan from both ends or maintain a window.

2. **Sliding Window:** Problems 28, 29, 30, 39, 40, 50 — fixed or variable-size window with a hash map for tracking.

3. **Hash Map / Frequency Count:** Problems 3, 5, 9, 16, 19, 35, 41, 45 — count occurrences and use sets/dicts for lookups.

4. **Stack-Based:** Problems 6, 7, 32 — use stack to track state or handle nested structures.

5. **Greedy:** Problems 7, 19, 33, 46 — make locally optimal choices at each step.

6. **Divide and Conquer:** Problem 25 — split the problem and solve recursively.

7. **Dynamic Programming:** Problems 42, 47 — build solutions bottom-up using subproblem results.

8. **Trie:** Problem 43 — use prefix/suffix trees for efficient string matching.

9. **Binary Search:** Problem 41 — use binary search to optimize lookups in sorted data.

10. **Monotonic Deque:** Problem 48 — maintain a deque with ordered elements for sliding window maximum.

### Key Techniques for Infosys SP DSE Interviews

- **In-place modification:** Problems 1, 18 — use two pointers to avoid extra space.
- **Modular arithmetic:** Problems 23, 26, 49 — always mod by 10^9 + 7 when dealing with large counts.
- **String normalization:** Problems 16, 11 — convert strings to a canonical form for comparison.
- **Edge case handling:** Always check for empty inputs, single elements, and boundary conditions.
- **Pattern recognition:** Many string problems reduce to counting, grouping, or searching with specific constraints.

### Complexity Cheat Sheet

| Technique | Typical Time | Typical Space |
|-----------|-------------|---------------|
| Single pass | O(n) | O(1) |
| Two pointers | O(n) | O(1) |
| Sliding window | O(n) | O(k) |
| Hash map | O(n) | O(n) |
| Sorting | O(n log n) | O(n) |
| DP (1D) | O(n) | O(n) |
| DP (2D) | O(n²) | O(n²) |
| Trie operations | O(m) per op | O(ALPHABET × total chars) |

---

## Common String Algorithms Reference

### KMP (Knuth-Morris-Pratt) Pattern Matching
Used in: Problem 33 (Repeated String Match), Problem 31 (First Occurrence)

```python
def kmp_search(text: str, pattern: str) -> int:
    def build_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length > 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
        return lps

    if not pattern:
        return 0
    lps = build_lps(pattern)
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j
        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1
    return -1
```

### Rolling Hash (Rabin-Karp)
Used in: Problem 34 (Binary Codes of Size K)

```python
def rabin_karp(text: str, pattern: str) -> list[int]:
    n, m = len(text), len(pattern)
    if m > n:
        return []
    base, mod = 26, 10**9 + 7
    # Compute pattern hash and first window hash
    pattern_hash = 0
    window_hash = 0
    power = 1
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        window_hash = (window_hash * base + ord(text[i])) % mod
        if i < m - 1:
            power = (power * base) % mod
    result = []
    for i in range(n - m + 1):
        if window_hash == pattern_hash:
            if text[i:i + m] == pattern:
                result.append(i)
        if i < n - m:
            window_hash = (window_hash - ord(text[i]) * power) % mod
            window_hash = (window_hash * base + ord(text[i + m])) % mod
    return result
```

### Trie (Prefix Tree)
Used in: Problem 43 (Stream of Characters)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
```

### Monotonic Stack/Deque
Used in: Problem 48 (Max Value of Equation), Problem 32 (Remove Duplicates II)

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq = deque()  # Stores indices, front is always max
    result = []
    for i in range(len(nums)):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # Remove smaller elements from back
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

### Sliding Window Template
Used in: Problems 28, 29, 39, 50

```python
def sliding_window(s: str, k: int) -> int:
    window = {}
    left = 0
    result = 0
    for right in range(len(s)):
        # Expand: add right character to window
        window[s[right]] = window.get(s[right], 0) + 1
        # Shrink: remove left characters while invalid
        while window_invalid(window, k):
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        # Update result with current valid window
        result = max(result, right - left + 1)
    return result

def window_invalid(window, k):
    # Customize this based on problem constraints
    return len(window) > k
```

### Two Pointer Template
Used in: Problems 1, 14, 38

```python
def two_pointer(s: str) -> int:
    left, right = 0, len(s) - 1
    while left < right:
        if condition_met(s, left, right):
            # Process or update result
            left += 1
            right -= 1
        elif need_move_left(s, left, right):
            left += 1
        else:
            right -= 1
    return result
```

### Prefix Sum Template
Used in: Problem 49 (Ways to Split String)

```python
def prefix_sum(s: str) -> list[int]:
    prefix = [0] * (len(s) + 1)
    for i in range(len(s)):
        prefix[i + 1] = prefix[i] + (1 if s[i] == '1' else 0)
    return prefix

# To count elements in range [l, r]:
# count = prefix[r + 1] - prefix[l]
```

### Binary Search on Answer
Used in: Problem 33 (Repeated String Match), Problem 40 (Min Window Subsequence)

```python
def binary_search_answer(s: str, t: str) -> int:
    lo, hi = 0, len(s)  # Search space
    result = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if is_valid(s, t, mid):
            result = mid
            hi = mid - 1  # Try smaller
        else:
            lo = mid + 1  # Need larger
    return result

def is_valid(s, t, k):
    # Check if condition is satisfied with parameter k
    pass
```

---

## Summary Table

| # | Problem | Difficulty | Time | Space |
|---|---------|------------|------|-------|
| 1 | Reverse String | Easy | O(n) | O(1) |
| 2 | Reverse Words in String III | Easy | O(n) | O(n) |
| 3 | Unique Email Addresses | Easy | O(n*m) | O(n*m) |
| 4 | Robot Return to Origin | Easy | O(n) | O(1) |
| 5 | Destination City | Easy | O(n) | O(n) |
| 6 | Max Nesting Depth | Easy | O(n) | O(1) |
| 7 | Split Balanced Strings | Easy | O(n) | O(1) |
| 8 | Remove Palindromic Subseq | Easy | O(n) | O(n) |
| 9 | Count Binary Substrings | Easy | O(n) | O(n) |
| 10 | String Arrays Equivalent | Easy | O(n) | O(n) |
| 11 | Goal Parser | Easy | O(n) | O(n) |
| 12 | All Unique Characters | Easy | O(n) | O(1) |
| 13 | Prefix of Array | Easy | O(n) | O(n) |
| 14 | String Halves Alike | Easy | O(n) | O(1) |
| 15 | Capitalize Title | Easy | O(n) | O(n) |
| 16 | Group Shifted Strings | Medium | O(n*m) | O(n*m) |
| 17 | Compare Version Numbers | Medium | O(n) | O(n) |
| 18 | String Compression | Medium | O(n) | O(1) |
| 19 | Reorganize String | Medium | O(n) | O(n) |
| 20 | Repeated Substring Pattern | Medium | O(n) | O(n) |
| 21 | Longest Uncommon Sub I | Medium | O(n) | O(1) |
| 22 | Longest Uncommon Sub II | Medium | O(n²*m) | O(1) |
| 23 | One Distinct Letter Subs | Medium | O(n) | O(1) |
| 24 | Min Distance Strings | Medium | O(n log n) | O(1) |
| 25 | Longest Nice Substring | Medium | O(n²) | O(n) |
| 26 | Homogenous Substrings | Medium | O(n) | O(1) |
| 27 | Word Equals Sum | Medium | O(n) | O(1) |
| 28 | Max Vowels in Substring | Medium | O(n) | O(1) |
| 29 | Grumpy Bookstore Owner | Medium | O(n) | O(1) |
| 30 | Min Flips Alternating | Medium | O(n) | O(n) |
| 31 | First Occurrence | Medium | O(n*m) | O(m) |
| 32 | Remove Duplicates II | Medium | O(n) | O(n) |
| 33 | Repeated String Match | Medium | O(n*m) | O(n+m) |
| 34 | All Binary Codes Size K | Medium | O(n) | O(2^k) |
| 35 | Min Deletions Unique | Medium | O(n + k log k) | O(k) |
| 36 | Sum Digits After Convert | Medium | O(n + k log n) | O(n) |
| 37 | Largest Substring Equal Ch | Medium | O(n) | O(n) |
| 38 | Min Length Delete Ends | Medium | O(n) | O(1) |
| 39 | At Most K Distinct | Medium | O(n) | O(k) |
| 40 | Min Window Subsequence | Medium | O(n*m) | O(1) |
| 41 | Matching Subsequences | Medium | O(n + m log n) | O(n) |
| 42 | Valid Palindrome III | Medium | O(n²) | O(n) |
| 43 | Stream of Characters | Medium | O(k) | O(sum) |
| 44 | Camelcase Matching | Medium | O(n*m) | O(1) |
| 45 | Key-Card Alerts | Medium | O(n log n) | O(n) |
| 46 | Min Replacement Sort | Hard | O(n) | O(1) |
| 47 | Longest Palindromic Subseq | Hard | O(n²) | O(n) |
| 48 | Max Value of Equation | Hard | O(n) | O(n) |
| 49 | Ways to Split String | Hard | O(n) | O(1) |
| 50 | At Most Two Distinct | Hard | O(n) | O(1) |

---

## Interview Tips for String Problems

### Before Coding
1. **Clarify the input:** Ask about character set (ASCII? Unicode?), string length constraints, and whether the string is mutable.
2. **Identify the pattern:** Most string problems fall into two-pointer, sliding window, hash map, or DP categories.
3. **Check edge cases:** Empty strings, single characters, all same characters, no valid answer possible.

### Common Python String Pitfalls
- Strings are immutable in Python — `s[i] = 'a'` won't work. Use list conversion: `s = list(s)`.
- `s.split()` without arguments splits on any whitespace and removes empty strings. Use `s.split(' ')` to preserve empty strings.
- `s[::-1]` creates a reversed copy — O(n) time and space.
- `ord()` returns ASCII value; `chr()` converts back.

### Optimization Strategies
- **Early termination:** If you found the answer, stop processing (Problems 5, 25, 41).
- **Precomputation:** Build prefix sums or position indices before answering queries (Problems 41, 43).
- **Space optimization:** Use two rows instead of full DP matrix when only previous row is needed (Problems 42, 47).
- **Bit manipulation:** For binary strings, use bit operations for efficiency (Problem 34).

### Follow-up Questions Interviewers Love
- "Can you solve it in O(1) space?" — Usually requires in-place modification or mathematical tricks.
- "What if the input is a stream?" — Requires online algorithms or data structures like tries (Problem 43).
- "Can you handle multiple queries?" — Precompute and cache results.
- "What about Unicode characters?" — Consider using hash maps instead of fixed arrays.

### Practice Progression
- Start with Easy problems (1-15) to build confidence and speed.
- Move to Medium problems (16-45) for pattern recognition.
- Tackle Hard problems (46-50) for optimization and edge case handling.
- Time yourself: aim for 15 minutes per Easy, 25 minutes per Medium, 35 minutes per Hard.

---

*Total: 50 problems | All in Python | Covers Easy/Medium/Hard*
