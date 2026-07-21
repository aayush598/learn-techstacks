# String Problems - Infosys SP DSE Preparation

## 50 Must-Know String Problems (Easy → Hard)

---

# ═══════════════════════════════════════════════════════════════
# EASY PROBLEMS (1-15)
# ═══════════════════════════════════════════════════════════════

---

## Problem 1: Valid Palindrome

**Problem:** Given a string `s`, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.

**Approach:** Use two pointers from both ends. Skip non-alphanumeric characters. Compare characters in lowercase.

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True

# Test
print(is_palindrome("A man, a plan, a canal: Panama"))  # True
print(is_palindrome("race a car"))                       # False
```

**Complexity:** O(n) time, O(1) space

**Trick:** Two pointers from outside is cleaner than building a filtered string. Always handle edge cases like empty string and single character.

---

## Problem 2: Valid Anagram

**Problem:** Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise.

**Approach:** Count character frequencies using a dictionary or array of size 26. If counts match, they are anagrams.

```python
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    count = [0] * 26
    for i in range(len(s)):
        count[ord(s[i]) - ord('a')] += 1
        count[ord(t[i]) - ord('a')] -= 1
    return all(c == 0 for c in count)

# Test
print(is_anagram("anagram", "nagaram"))  # True
print(is_anagram("rat", "car"))           # False
```

**Complexity:** O(n) time, O(1) space (fixed 26-size array)

**Trick:** If both strings have same length, single pass with increment/decrement is faster than two separate count dictionaries. Using array instead of dict avoids hash overhead.

---

## Problem 3: Reverse String

**Problem:** Given an array of characters `s`, reverse it in-place using O(1) extra memory.

**Approach:** Swap characters from both ends moving inward until pointers meet.

```python
def reverse_string(s):
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    return s

# Test
print(reverse_string(["h","e","l","l","o"]))  # ["o","l","l","e","h"]
print(reverse_string(["H","a","n","n","a","h"]))  # ["h","a","n","n","a","H"]
```

**Complexity:** O(n) time, O(1) space

**Trick:** In Python, `s.reverse()` or `s[::-1]` are built-in but interviewers want to see the two-pointer swap logic. Always confirm if input is list of chars vs string.

---

## Problem 4: Reverse Words in a String

**Problem:** Given a string `s`, reverse the order of words (words separated by spaces).

**Approach:** Split the string into words, reverse the list, and join. Or use two-pointer on words directly.

```python
def reverse_words(s):
    words = s.split()
    return " ".join(words[::-1])

def reverse_words_v2(s):
    words = s.split()
    left, right = 0, len(words) - 1
    while left < right:
        words[left], words[right] = words[right], words[left]
        left += 1
        right -= 1
    return " ".join(words)

# Test
print(reverse_words("  the sky is blue  "))  # "blue is sky the"
print(reverse_words("a good   example"))      # "example good a"
```

**Complexity:** O(n) time, O(n) space

**Trick:** Python's `split()` without arguments handles multiple spaces and leading/trailing spaces automatically. Use `" ".join()` to reconstruct.

---

## Problem 5: First Unique Character in a String

**Problem:** Given a string `s`, find the index of the first non-repeating character. Return -1 if none exists.

**Approach:** Count frequencies in one pass, then find first character with count 1 in second pass.

```python
def first_unique_char(s):
    count = {}
    for ch in s:
        count[ch] = count.get(ch, 0) + 1
    for i, ch in enumerate(s):
        if count[ch] == 1:
            return i
    return -1

# Test
print(first_unique_char("leetcode"))      # 0
print(first_unique_char("loveleetcode"))  # 2
print(first_unique_char("aabb"))          # -1
```

**Complexity:** O(n) time, O(1) space (at most 26 lowercase letters)

**Trick:** Two-pass approach is optimal. First pass builds the frequency map, second pass finds the answer. Cannot do better than O(n) since we must scan the entire string.

---

## Problem 6: Valid Parentheses

**Problem:** Given a string containing only `(){}[]`, determine if the input is valid (opened and closed in correct order).

**Approach:** Use a stack. Push opening brackets. When closing bracket appears, check if top of stack matches.

```python
def is_valid_parentheses(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for ch in s:
        if ch in mapping:
            if not stack or stack[-1] != mapping[ch]:
                return False
            stack.pop()
        else:
            stack.append(ch)
    return len(stack) == 0

# Test
print(is_valid_parentheses("()[]{}"))  # True
print(is_valid_parentheses("(]"))       # False
print(is_valid_parentheses("([)]"))     # False
print(is_valid_parentheses("{[]}"))     # True
```

**Complexity:** O(n) time, O(n) space worst case

**Trick:** The key insight is using closing-to-opening mapping. If stack is empty when encountering a closing bracket, it's invalid. Final check: stack must be empty.

---

## Problem 7: Merge Strings Alternately

**Problem:** Given two strings `word1` and `word2`, merge them by alternating characters. If one is longer, append the rest at the end.

**Approach:** Iterate up to min length, alternate characters, then append the remainder of the longer string.

```python
def merge_alternately(word1, word2):
    result = []
    i, j = 0, 0
    while i < len(word1) and j < len(word2):
        result.append(word1[i])
        result.append(word2[j])
        i += 1
        j += 1
    result.append(word1[i:])
    result.append(word2[j:])
    return "".join(result)

# Test
print(merge_alternately("abc", "pqr"))    # "apbqcr"
print(merge_alternately("ab", "pqrs"))    # "apbqrs"
print(merge_alternately("abcd", "pq"))    # "apbqcd"
```

**Complexity:** O(n + m) time, O(n + m) space

**Trick:** After the loop, one of `word1[i:]` or `word2[j:]` will be empty. Appending both is safe and clean. Using list and `join` is faster than string concatenation in Python.

---

## Problem 8: Length of Last Word

**Problem:** Given a string `s` containing words separated by spaces, return the length of the last word.

**Approach:** Split the string and return the length of the last element. Or traverse from the end.

```python
def length_of_last_word(s):
    words = s.strip().split()
    return len(words[-1])

def length_of_last_word_v2(s):
    length = 0
    i = len(s) - 1
    while i >= 0 and s[i] == ' ':
        i -= 1
    while i >= 0 and s[i] != ' ':
        length += 1
        i -= 1
    return length

# Test
print(length_of_last_word("Hello World"))        # 5
print(length_of_last_word("   fly me   to   the moon  "))  # 4
print(length_of_last_word("luffy is still joy"))  # 3
```

**Complexity:** O(n) time, O(1) space for v2, O(n) space for v1

**Trick:** Edge cases: trailing spaces, single word, empty string. The `strip().split()` approach is cleanest for Python. Manual traversal from end is O(1) space.

---

## Problem 9: Jewels and Stones

**Problem:** Given string `jewels` (types of jewels) and `stones` (characters you have), return how many of your stones are jewels. Letters are case-sensitive.

**Approach:** Put jewels in a set. Count how many characters in stones are in the set.

```python
def num_jewels_in_stones(jewels, stones):
    jewel_set = set(jewels)
    return sum(1 for s in stones if s in jewel_set)

# Test
print(num_jewels_in_stones("aA", "aAAbbbb"))  # 3
print(num_jewels_in_stones("z", "ZZ"))          # 0
```

**Complexity:** O(J + S) time, O(J) space

**Trick:** Using a set for O(1) lookup is the key. List comprehension with `sum` is the most Pythonic solution.

---

## Problem 10: Defanging IP Address

**Problem:** Given a valid IPv4 address, return a defanged version where every "." is replaced with "[.]".

**Approach:** Simply replace "." with "[.]" using string replace method.

```python
def defang_ipaddress(address):
    return address.replace(".", "[.]")

# Test
print(defang_ipaddress("1.1.1.1"))      # "1[.]1[.]1[.]1"
print(defang_ipaddress("255.100.50.0"))  # "255[.]100[.]50[.]0"
```

**Complexity:** O(n) time, O(n) space

**Trick:** Python's `str.replace()` is efficient and clean. For manual approach, build a list and join with "[.]" as separator (excluding the last element).

---

## Problem 11: Number of Good Pairs

**Problem:** Given an array `nums`, return the number of pairs (i, j) where i < j and nums[i] == nums[j].

**Approach:** Count frequencies. For each value with count c, number of pairs is c*(c-1)/2. Or use nested loops for brute force.

```python
def num_identical_pairs(nums):
    from collections import Counter
    count = Counter(nums)
    result = 0
    for freq in count.values():
        result += freq * (freq - 1) // 2
    return result

def num_identical_pairs_v2(nums):
    result = 0
    count = {}
    for num in nums:
        if num in count:
            result += count[num]
            count[num] += 1
        else:
            count[num] = 1
    return result

# Test
print(num_identical_pairs([1,2,3,1,1,3]))  # 4
print(num_identical_pairs([1,1,1,1]))        # 6
print(num_identical_pairs([1,2,3]))           # 0
```

**Complexity:** O(n) time, O(n) space

**Trick:** The cumulative counting approach (v2) is elegant: as you see each new element, it forms a pair with every previous occurrence of the same value. No need for combinatorics formula.

---

## Problem 12: Sort Characters By Frequency

**Problem:** Given a string `s`, sort it in decreasing order based on frequency of characters.

**Approach:** Count frequencies, sort characters by frequency descending, build result by repeating each character by its count.

```python
def frequency_sort(s):
    from collections import Counter
    count = Counter(s)
    sorted_chars = sorted(count.keys(), key=lambda ch: count[ch], reverse=True)
    result = []
    for ch in sorted_chars:
        result.append(ch * count[ch])
    return "".join(result)

# Test
print(frequency_sort("tree"))      # "eert"
print(frequency_sort("cccaaa"))    # "aaaccc"
print(frequency_sort("Aabb"))      # "bbAa"
```

**Complexity:** O(n log n) time (due to sort), O(n) space

**Trick:** Using `Counter` and `sorted` with a key function is clean. For O(n) average case, use bucket sort: create array of lists indexed by frequency, then traverse from high to low.

---

## Problem 13: Longest Common Prefix

**Problem:** Write a function to find the longest common prefix string amongst an array of strings.

**Approach:** Use the first string as reference. Compare each character with all other strings. Stop when mismatch is found.

```python
def longest_common_prefix(strs):
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

def longest_common_prefix_v2(strs):
    if not strs:
        return ""
    min_len = min(len(s) for s in strs)
    result = ""
    for i in range(min_len):
        char = strs[0][i]
        if all(s[i] == char for s in strs):
            result += char
        else:
            break
    return result

# Test
print(longest_common_prefix(["flower","flow","flight"]))  # "fl"
print(longest_common_prefix(["dog","racecar","car"]))     # ""
print(longest_common_prefix(["ab","a"]))                   # "a"
```

**Complexity:** O(S) time where S is sum of all characters, O(1) space

**Trick:** Vertical scanning (v2) is intuitive. Horizontal scanning (v1) is also good. Sorting strings first and comparing only first and last is another approach since they would be most different.

---

## Problem 14: Implement strStr() (Find First Occurrence)

**Problem:** Return the index of the first occurrence of `needle` in `haystack`, or -1 if not found.

**Approach:** Sliding window - iterate through haystack, check each substring of length len(needle).

```python
def str_str(haystack, needle):
    if not needle:
        return 0
    n, m = len(haystack), len(needle)
    for i in range(n - m + 1):
        if haystack[i:i + m] == needle:
            return i
    return -1

# Test
print(str_str("sadbutsad", "sad"))   # 0
print(str_str("leetcode", "leeto"))  # -1
print(str_str("hello", "ll"))         # 2
```

**Complexity:** O(n * m) time, O(1) space

**Trick:** For interviews, mention KMP algorithm for O(n + m) time. The brute force is acceptable but knowing KMP shows depth. Edge case: empty needle should return 0.

---

## Problem 15: Remove Outermost Parentheses

**Problem:** Given a valid parentheses string, remove the outermost parentheses of every primitive group.

**Approach:** Use a counter. When counter is 0, we start a new group. Skip the first and last parenthesis of each group.

```python
def remove_outer_parentheses(s):
    result = []
    depth = 0
    for ch in s:
        if ch == '(':
            if depth > 0:
                result.append(ch)
            depth += 1
        else:
            depth -= 1
            if depth > 0:
                result.append(ch)
    return "".join(result)

# Test
print(remove_outer_parentheses("(()())(())"))    # "()()()"
print(remove_outer_parentheses("(()())(())(()(()"))  # "()()()()()"
print(remove_outer_parentheses("()()"))           # ""
```

**Complexity:** O(n) time, O(n) space

**Trick:** Depth counter is key. When depth is 0, we've completed a primitive group. Add character only when depth > 0 (before increment for opening, after decrement for closing).

---

# ═══════════════════════════════════════════════════════════════
# MEDIUM PROBLEMS (16-45)
# ═══════════════════════════════════════════════════════════════

---

## Problem 16: Longest Substring Without Repeating Characters

**Problem:** Given a string `s`, find the length of the longest substring without repeating characters.

**Approach:** Sliding window with a set/map to track characters in current window. Move left pointer when duplicate is found.

```python
def length_of_longest_substring(s):
    char_index = {}
    left = 0
    max_length = 0
    for right in range(len(s)):
        if s[right] in char_index and char_index[s[right]] >= left:
            left = char_index[s[right]] + 1
        char_index[s[right]] = right
        max_length = max(max_length, right - left + 1)
    return max_length

# Test
print(length_of_longest_substring("abcabcbb"))  # 3
print(length_of_longest_substring("bbbbb"))      # 1
print(length_of_longest_substring("pwwkew"))     # 3
print(length_of_longest_substring(""))            # 0
```

**Complexity:** O(n) time, O(min(n, m)) space where m is charset size

**Trick:** Store the latest index of each character. When you see a duplicate, jump left pointer directly to after the last occurrence. This avoids shrinking window one step at a time.

---

## Problem 17: Longest Palindromic Substring

**Problem:** Given a string `s`, return the longest palindromic substring.

**Approach:** Expand around each possible center. For each center, expand outward while characters match.

```python
def longest_palindrome(s):
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

# Test
print(longest_palindrome("babad"))   # "bab" or "aba"
print(longest_palindrome("cbbd"))    # "bb"
print(longest_palindrome("a"))       # "a"
```

**Complexity:** O(n^2) time, O(1) space

**Trick:** There are 2n-1 possible centers (n for odd-length, n-1 for even-length). Expand from each center. This is simpler than DP and preferred in interviews.

---

## Problem 18: Group Anagrams

**Problem:** Given an array of strings, group anagrams together.

**Approach:** Use sorted string as key. All anagrams will have the same sorted form.

```python
def group_anagrams(strs):
    from collections import defaultdict
    anagram_map = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        anagram_map[key].append(s)
    return list(anagram_map.values())

# Alternative: use character count tuple as key
def group_anagrams_v2(strs):
    from collections import defaultdict
    anagram_map = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1
        anagram_map[tuple(count)].append(s)
    return list(anagram_map.values())

# Test
print(group_anagrams(["eat","tea","tan","ate","nat","bat"]))
# [["eat","tea","ate"],["tan","nat"],["bat"]]
print(group_anagrams([""]))  # [[""]]
```

**Complexity:** O(n * k log k) time where k is max string length, O(n * k) space

**Trick:** v2 using character count as key is O(n * k) time - slightly faster. Using `defaultdict(list)` avoids key-existence checks.

---

## Problem 19: Valid Palindrome II

**Problem:** Given a string `s`, return `True` if `s` is a palindrome after deleting at most one character.

**Approach:** Use two pointers. If mismatch found, try skipping left char or right char. Check if either resulting substring is palindrome.

```python
def valid_palindrome(s):
    def is_palindrome(left, right):
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return is_palindrome(left + 1, right) or is_palindrome(left, right - 1)
        left += 1
        right -= 1
    return True

# Test
print(valid_palindrome("aba"))       # True
print(valid_palindrome("abca"))      # True
print(valid_palindrome("abc"))       # False
```

**Complexity:** O(n) time, O(1) space

**Trick:** At most one deletion means at most one mismatch. When mismatch occurs, the two candidate substrings to check are (left+1, right) and (left, right-1).

---

## Problem 20: Minimum Window Substring

**Problem:** Given strings `s` and `t`, find the minimum window in `s` which contains all characters of `t` (including duplicates).

**Approach:** Sliding window with character frequency map. Expand right until all characters are included. Contract left to find minimum.

```python
def min_window(s, t):
    from collections import Counter
    if not t or not s:
        return ""
    t_count = Counter(t)
    required = len(t_count)
    formed = 0
    window_counts = {}
    left = 0
    min_len = float('inf')
    min_left = 0

    for right in range(len(s)):
        ch = s[right]
        window_counts[ch] = window_counts.get(ch, 0) + 1
        if ch in t_count and window_counts[ch] == t_count[ch]:
            formed += 1

        while formed == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left
            left_ch = s[left]
            window_counts[left_ch] -= 1
            if left_ch in t_count and window_counts[left_ch] < t_count[left_ch]:
                formed -= 1
            left += 1

    return "" if min_len == float('inf') else s[min_left:min_left + min_len]

# Test
print(min_window("ADOBECODEBANC", "ABC"))  # "BANC"
print(min_window("a", "a"))                 # "a"
print(min_window("a", "aa"))                # ""
```

**Complexity:** O(n) time, O(k) space where k is charset size

**Trick:** The `formed` counter tracks how many unique characters have reached their required frequency. Only shrink window when all characters are satisfied. This avoids checking all windows.

---

## Problem 21: Generate Parentheses

**Problem:** Given `n` pairs of parentheses, generate all combinations of well-formed parentheses.

**Approach:** Backtracking. Add '(' if count < n, add ')' if close_count < open_count.

```python
def generate_parenthesis(n):
    result = []

    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(current)
            return
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)

    backtrack("", 0, 0)
    return result

# Test
print(generate_parenthesis(3))
# ["((()))","(()())","(())()","()(())","()()()"]
print(generate_parenthesis(1))  # ["()"]
```

**Complexity:** O(4^n / sqrt(n)) time (Catalan number), O(n) recursion depth

**Trick:** Key insight: we can add '(' only if we haven't used all n, and ')' only if it won't make the string invalid (close < open). This generates only valid combinations.

---

## Problem 22: Letter Combinations of a Phone Number

**Problem:** Given a string containing digits 2-9, return all possible letter combinations (phone keypad mapping).

**Approach:** Backtracking/DFS through the digit-to-letter mapping. Build combinations recursively.

```python
def letter_combinations(digits):
    if not digits:
        return []
    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    result = []

    def backtrack(index, current):
        if index == len(digits):
            result.append(current)
            return
        for ch in phone[digits[index]]:
            backtrack(index + 1, current + ch)

    backtrack(0, "")
    return result

# Test
print(letter_combinations("23"))
# ["ad","ae","af","bd","be","bf","cd","ce","cf"]
print(letter_combinations(""))      # []
print(letter_combinations("2"))     # ["a","b","c"]
```

**Complexity:** O(4^n * n) time, O(n) recursion depth

**Trick:** Each digit maps to 3-4 letters. Total combinations = product of options. Use iterative approach too: start with empty list, for each digit, expand each existing combination.

---

## Problem 23: Integer to English Words

**Problem:** Convert a non-negative integer to its English words representation (up to billions).

**Approach:** Break number into chunks of 1000. Handle each chunk separately. Map numbers 1-999 to words, append scale (Thousand, Million, Billion).

```python
def number_to_words(num):
    if num == 0:
        return "Zero"
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
            "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
            "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty",
            "Sixty", "Seventy", "Eighty", "Ninety"]
    scales = ["", "Thousand", "Million", "Billion"]

    def chunk_to_words(n):
        result = ""
        if n >= 100:
            result += ones[n // 100] + " Hundred "
            n %= 100
        if n >= 20:
            result += tens[n // 10] + " "
            n %= 10
        if n >= 1:
            result += ones[n] + " "
        return result.strip()

    result = ""
    scale_index = 0
    while num > 0:
        chunk = num % 1000
        if chunk != 0:
            result = chunk_to_words(chunk) + " " + scales[scale_index] + " " + result
        num //= 1000
        scale_index += 1
    return result.strip()

# Test
print(number_to_words(123))    # "One Hundred Twenty Three"
print(number_to_words(12345))  # "Twelve Thousand Three Hundred Forty Five"
print(number_to_words(1234567))  # "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
```

**Complexity:** O(1) time (bounded by 32-bit int), O(1) space

**Trick:** Process number in chunks of 1000 from right to left. Each chunk (0-999) uses the same conversion logic with hundreds, tens, and ones.

---

## Problem 24: Count and Say

**Problem:** Given `n`, return the nth term of the count-and-say sequence. Start with "1".

**Approach:** Build sequence iteratively. For each term, count consecutive same digits and build next term.

```python
def count_and_say(n):
    result = "1"
    for _ in range(n - 1):
        next_result = []
        i = 0
        while i < len(result):
            count = 1
            while i + count < len(result) and result[i + count] == result[i]:
                count += 1
            next_result.append(str(count))
            next_result.append(result[i])
            i += count
        result = "".join(next_result)
    return result

# Test
print(count_and_say(1))  # "1"
print(count_and_say(4))  # "1211"
print(count_and_say(5))  # "111221"
```

**Complexity:** O(n * m) time where m is length of current string, O(m) space

**Trick:** The sequence grows roughly by factor of 1.3 each iteration. Use two pointers to count consecutive characters. Build result as list and join at end for efficiency.

---

## Problem 25: Decode String

**Problem:** Given encoded string `s = "3[a2[c]]"`, return the decoded string `"accaccacc"`.

**Approach:** Use two stacks - one for numbers, one for strings. Push current string and number when '[' encountered. Pop and repeat when ']' encountered.

```python
def decode_string(s):
    stack = []
    current_string = ""
    current_num = 0

    for ch in s:
        if ch.isdigit():
            current_num = current_num * 10 + int(ch)
        elif ch == '[':
            stack.append((current_string, current_num))
            current_string = ""
            current_num = 0
        elif ch == ']':
            prev_string, num = stack.pop()
            current_string = prev_string + current_string * num
        else:
            current_string += ch

    return current_string

# Test
print(decode_string("3[a2[c]]"))       # "accaccacc"
print(decode_string("3[ab]"))           # "ababab"
print(decode_string("2[abc]3[cd]ef"))  # "abcabccdcdcdef"
print(decode_string("3[a]2[bc]"))      # "aaabcbc"
```

**Complexity:** O(n * m) time where m is max nesting, O(n) space

**Trick:** Single stack approach is clean. Store the string before '[' and the repeat count. When ']', pop and concatenate. Handle nested brackets naturally through stack LIFO property.

---

## Problem 26: Basic Calculator II

**Problem:** Given a string `s` representing an arithmetic expression with +, -, *, /, compute the result.

**Approach:** Use a stack. Process * and / immediately. Push + and - operands. Sum stack at the end.

```python
def calculate(s):
    stack = []
    current_num = 0
    operator = '+'
    s = s.replace(" ", "")

    for i, ch in enumerate(s):
        if ch.isdigit():
            current_num = current_num * 10 + int(ch)
        if ch in '+-*/' or i == len(s) - 1:
            if operator == '+':
                stack.append(current_num)
            elif operator == '-':
                stack.append(-current_num)
            elif operator == '*':
                stack.append(stack.pop() * current_num)
            elif operator == '/':
                stack.append(int(stack.pop() / current_num))
            operator = ch
            current_num = 0

    return sum(stack)

# Test
print(calculate("3+2*2"))    # 7
print(calculate(" 3/2 "))    # 1
print(calculate(" 3+5 / 2 "))  # 5
```

**Complexity:** O(n) time, O(n) space

**Trick:** The key insight is that * and / have higher precedence. Process them immediately when you see the next operator. Use stack to defer + and - operations.

---

## Problem 27: Simplify Path

**Problem:** Given an absolute Unix path, simplify it to canonical path (single slash, no dots, no double slashes).

**Approach:** Split by '/'. Use stack. Push directory names. '..' pops. Ignore '.' and empty strings.

```python
def simplify_path(path):
    stack = []
    parts = path.split('/')

    for part in parts:
        if part == '..':
            if stack:
                stack.pop()
        elif part and part != '.':
            stack.append(part)

    return '/' + '/'.join(stack)

# Test
print(simplify_path("/home/"))           # "/home"
print(simplify_path("/../"))             # "/"
print(simplify_path("/home//foo/"))      # "/home/foo"
print(simplify_path("/a/./b/../../c/"))  # "/c"
```

**Complexity:** O(n) time, O(n) space

**Trick:** Splitting by '/' naturally handles double slashes. The empty string check handles consecutive slashes. Stack mirrors the directory hierarchy perfectly.

---

## Problem 28: Multiply Strings

**Problem:** Given two non-negative integers as strings, return their product as a string. Cannot use built-in big integer library.

**Approach:** Simulate grade-school multiplication. Position of digit in result is sum of positions in inputs.

```python
def multiply_strings(num1, num2):
    m, n = len(num1), len(num2)
    result = [0] * (m + n)

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            mul = int(num1[i]) * int(num2[j])
            p1, p2 = i + j, i + j + 1
            total = mul + result[p2]
            result[p2] = total % 10
            result[p1] += total // 10

    result_str = "".join(map(str, result)).lstrip("0")
    return result_str if result_str else "0"

# Test
print(multiply_strings("2", "3"))        # "6"
print(multiply_strings("123", "456"))    # "56088"
print(multiply_strings("999", "999"))    # "998001"
```

**Complexity:** O(m * n) time, O(m + n) space

**Trick:** The key formula: digit at position (i, j) in inputs goes to position (i+j, i+j+1) in result. Process from right to left. Handle carry propagation properly.

---

## Problem 29: Add Binary

**Problem:** Given two binary strings `a` and `b`, return their sum as a binary string.

**Approach:** Add from right to left with carry. Handle different lengths.

```python
def add_binary(a, b):
    result = []
    carry = 0
    i, j = len(a) - 1, len(b) - 1

    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += int(a[i])
            i -= 1
        if j >= 0:
            total += int(b[j])
            j -= 1
        result.append(str(total % 2))
        carry = total // 2

    return "".join(result[::-1])

# Test
print(add_binary("11", "1"))      # "100"
print(add_binary("1010", "1011")) # "10101"
```

**Complexity:** O(max(m, n)) time, O(max(m, n)) space

**Trick:** The while condition `i >= 0 or j >= 0 or carry` handles all cases: different lengths and final carry. Append to list and reverse at end is efficient.

---

## Problem 30: License Key Formatting

**Problem:** Given a license key `S` (letters, digits, dashes) and integer `K`, reformat so every group has exactly `K` characters (first group may be shorter).

**Approach:** Remove dashes, uppercase all, then build groups from right to left.

```python
def license_key_formatting(s, k):
    s = s.replace("-", "").upper()
    result = []
    count = 0

    for i in range(len(s) - 1, -1, -1):
        result.append(s[i])
        count += 1
        if count == k and i > 0:
            result.append("-")
            count = 0

    return "".join(result[::-1])

# Test
print(license_key_formatting("5F3Z-2e-9-w", 4))  # "5F3Z-2E9W"
print(license_key_formatting("2-5g-3-J", 2))      # "2-5G-3J"
```

**Complexity:** O(n) time, O(n) space

**Trick:** Build from right to left (where groups of K make sense). Add dash every K characters. Reverse at end. First group may have fewer than K characters.

---

## Problem 31: Reorganize String

**Problem:** Given a string `s`, rearrange it so no two adjacent characters are the same. Return any valid arrangement or "" if impossible.

**Approach:** Count frequencies. Place most frequent character at even indices, then odd indices. Check if max frequency > (n+1)/2.

```python
def reorganize_string(s):
    from collections import Counter
    count = Counter(s)
    max_count = max(count.values())
    if max_count > (len(s) + 1) // 2:
        return ""

    result = [''] * len(s)
    even, odd = 0, 1
    n = len(s)

    for ch, freq in count.most_common():
        while freq > 0 and even < n:
            result[even] = ch
            even += 2
            freq -= 1
        while freq > 0 and odd < n:
            result[odd] = ch
            odd += 2
            freq -= 1

    return "".join(result)

# Test
print(reorganize_string("aab"))    # "aba"
print(reorganize_string("aaab"))   # ""
```

**Complexity:** O(n log n) time (for sorting), O(n) space

**Trick:** Greedy approach: most frequent characters go to even indices (0, 2, 4...), rest to odd (1, 3, 5...). If max freq exceeds half the length, it's impossible.

---

## Problem 32: Palindrome Permutation

**Problem:** Given a string `s`, check if any permutation of it can form a palindrome.

**Approach:** Count character frequencies. A palindrome permutation is possible if at most one character has odd count.

```python
def can_permute_palindrome(s):
    from collections import Counter
    count = Counter(s)
    odd_count = sum(1 for freq in count.values() if freq % 2 == 1)
    return odd_count <= 1

# Alternative using bitmask
def can_permute_palindrome_v2(s):
    bit_mask = 0
    for ch in s:
        bit_mask ^= (1 << (ord(ch) - ord('a')))
    return bit_mask == 0 or (bit_mask & (bit_mask - 1)) == 0

# Test
print(can_permute_palindrome("code"))      # False
print(can_permute_palindrome("aab"))       # True
print(can_permute_palindrome("carerac"))   # True
```

**Complexity:** O(n) time, O(1) space

**Trick:** Bitmask approach is elegant: toggle bit for each character. At end, check if 0 or has exactly one set bit (power of 2 check: `n & (n-1) == 0`).

---

## Problem 33: String to Integer (atoi)

**Problem:** Implement `atoi` which converts a string to a 32-bit signed integer.

**Approach:** Skip whitespace, handle sign, read digits, clamp to 32-bit range.

```python
def my_atoi(s):
    i = 0
    n = len(s)
    result = 0
    sign = 1

    # Skip whitespace
    while i < n and s[i] == ' ':
        i += 1

    # Handle sign
    if i < n and s[i] in '+-':
        sign = -1 if s[i] == '-' else 1
        i += 1

    # Read digits
    while i < n and s[i].isdigit():
        result = result * 10 + int(s[i])
        i += 1

    result *= sign

    # Clamp to 32-bit range
    INT_MIN, INT_MAX = -2**31, 2**31 - 1
    result = max(INT_MIN, min(INT_MAX, result))

    return result

# Test
print(my_atoi("42"))          # 42
print(my_atoi("   -42"))      # -42
print(my_atoi("4193 with words"))  # 4193
print(my_atoi("words and 987"))    # 0
print(my_atoi("-91283472332"))     # -2147483648
```

**Complexity:** O(n) time, O(1) space

**Trick:** Handle all edge cases: leading whitespace, sign, non-digit characters, overflow. The order matters: whitespace → sign → digits. Stop at first non-digit.

---

## Problem 34: Longest Repeating Character Replacement

**Problem:** Given string `s` and integer `k`, find the length of the longest substring where you can replace at most `k` characters to make all characters the same.

**Approach:** Sliding window. Track max frequency in window. If window size - max_freq > k, shrink window.

```python
def character_replacement(s, k):
    count = {}
    left = 0
    max_freq = 0
    max_length = 0

    for right in range(len(s)):
        count[s[right]] = count.get(s[right], 0) + 1
        max_freq = max(max_freq, count[s[right]])

        while (right - left + 1) - max_freq > k:
            count[s[left]] -= 1
            left += 1

        max_length = max(max_length, right - left + 1)

    return max_length

# Test
print(character_replacement("ABAB", 2))    # 4
print(character_replacement("AABABBA", 1)) # 4
```

**Complexity:** O(n) time, O(1) space (at most 26 letters)

**Trick:** `window_size - max_freq` gives minimum replacements needed. If this exceeds k, shrink window. max_freq only increases, never decreases - this is correct because we only care about the maximum window found.

---

## Problem 35: Permutation in String

**Problem:** Given two strings `s1` and `s2`, return `True` if `s2` contains a permutation of `s1`.

**Approach:** Use sliding window of size len(s1) on s2. Check if character frequencies match.

```python
def check_inclusion(s1, s2):
    if len(s1) > len(s2):
        return False
    from collections import Counter
    s1_count = Counter(s1)
    window_count = Counter()

    for i in range(len(s2)):
        window_count[s2[i]] += 1
        if i >= len(s1):
            if window_count[s2[i - len(s1)]] == 1:
                del window_count[s2[i - len(s1)]]
            else:
                window_count[s2[i - len(s1)]] -= 1

        if window_count == s1_count:
            return True

    return False

# Test
print(check_inclusion("ab", "eidbaooo"))  # True
print(check_inclusion("ab", "eidboaoo"))  # False
```

**Complexity:** O(n) time where n is len(s2), O(1) space

**Trick:** Using Counter comparison is clean but slightly slow. Faster: maintain a `matches` counter that tracks how many characters have matching counts between window and s1. When matches == 26, return True.

---

## Problem 36: Find All Anagrams in a String

**Problem:** Given strings `s` and `p`, find all start indices of `p`'s anagrams in `s`.

**Approach:** Sliding window of size len(p). Track character frequencies. When window matches p's frequency, record start index.

```python
def find_anagrams(s, p):
    from collections import Counter
    p_count = Counter(p)
    window_count = Counter()
    result = []
    n = len(p)

    for i in range(len(s)):
        window_count[s[i]] += 1
        if i >= n:
            left_char = s[i - n]
            if window_count[left_char] == 1:
                del window_count[left_char]
            else:
                window_count[left_char] -= 1

        if window_count == p_count:
            result.append(i - n + 1)

    return result

# Test
print(find_anagrams("cbaebabacd", "abc"))  # [0, 6]
print(find_anagrams("abab", "ab"))          # [0, 1, 2]
```

**Complexity:** O(n) time, O(1) space

**Trick:** Same sliding window as Problem 35, but collect all matching positions. Make sure to remove character from Counter when count reaches 0 (not just decrement to 0).

---

## Problem 37: Minimum Add to Make Parentheses Valid

**Problem:** Given a string of parentheses, return the minimum number of parentheses to add to make the string valid.

**Approach:** Count unmatched opening and closing parentheses using a balance counter.

```python
def min_add_to_make_valid(s):
    open_count = 0
    close_count = 0

    for ch in s:
        if ch == '(':
            open_count += 1
        else:
            if open_count > 0:
                open_count -= 1
            else:
                close_count += 1

    return open_count + close_count

# Test
print(min_add_to_make_valid("(()))("))  # 1... wait
# "(()))(" -> open=1, close=1 -> need 2
print(min_add_to_make_valid("())"))       # 1
print(min_add_to_make_valid("((("))       # 3
print(min_add_to_make_valid("()"))        # 0
```

**Complexity:** O(n) time, O(1) space

**Trick:** `open_count` tracks unmatched '('. When we see ')', try to match with an open. If no open available, it's an unmatched ')'. Final answer = unmatched opens + unmatched closes.

---

## Problem 38: Partition Labels

**Problem:** Given a string `s`, partition into as many parts as possible so each letter appears in at most one part.

**Approach:** First, record last occurrence of each character. Iterate through string, tracking current partition's end. When i == end, cut partition.

```python
def partition_labels(s):
    last = {ch: i for i, ch in enumerate(s)}
    result = []
    start = 0
    end = 0

    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end:
            result.append(end - start + 1)
            start = end + 1

    return result

# Test
print(partition_labels("ababcbacadefegdehijhklij"))  # [9,7,8]
print(partition_labels("eccbbbbdec"))                  # [10]
```

**Complexity:** O(n) time, O(1) space (at most 26 letters)

**Trick:** The greedy approach works: extend partition to include the farthest occurrence of any character seen. When current index reaches the partition boundary, cut and start new partition.

---

## Problem 39: Verifying an Alien Dictionary

**Problem:** Given a sorted words array and alien order string, determine if the words are sorted lexicographically.

**Approach:** Create character order mapping. Compare adjacent words to check if they are in order.

```python
def is_alien_sorted(words, order):
    char_order = {ch: i for i, ch in enumerate(order)}

    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        # Check if word1 is prefix of word2 - should be shorter
        if len(word1) > len(word2) and word1.startswith(word2):
            return False
        for j in range(min(len(word1), len(word2))):
            if char_order[word1[j]] < char_order[word2[j]]:
                break
            elif char_order[word1[j]] > char_order[word2[j]]:
                return False

    return True

# Test
print(is_alien_sorted(["hello","leetcode"], "hlabcdefgijkmnopqrstuvwxyz"))  # True
print(is_alien_sorted(["word","world","row"], "worldabcefghijkmnpqstuvxyz"))  # False
print(is_alien_sorted(["apple","app"], "abcdefghijklmnopqrstuvwxyz"))  # False
```

**Complexity:** O(n * m) time where n is words count, m is max word length. O(1) space.

**Trick:** Convert order string to dictionary for O(1) character comparison. Compare word by word. Shorter word that is prefix of longer word should come first.

---

## Problem 40: Custom Sort String

**Problem:** Given strings `order` and `s`, rearrange `s` so characters are sorted by `order`. Characters not in `order` go at the end.

**Approach:** Count character frequencies in `s`. Build result by iterating through `order` and appending characters by their count.

```python
def custom_sort_string(order, s):
    from collections import Counter
    count = Counter(s)
    result = []

    for ch in order:
        if ch in count:
            result.append(ch * count[ch])
            del count[ch]

    for ch, freq in count.items():
        result.append(ch * freq)

    return "".join(result)

# Test
print(custom_sort_string("cba", "abcd"))  # "cbad"
print(custom_sort_string("bcafg", "abcdef"))  # "bcade..."
```

**Complexity:** O(n + m) time where n is len(s), m is len(order). O(n) space.

**Trick:** After processing all characters in order, remaining characters in Counter are those not in order - append them at end.

---

## Problem 41: Restore IP Addresses

**Problem:** Given a string `s` of digits, return all possible valid IP addresses.

**Approach:** Backtracking. Try all valid segments (1-3 digits, 0-255, no leading zeros).

```python
def restore_ip_addresses(s):
    result = []

    def backtrack(start, parts):
        if len(parts) == 4 and start == len(s):
            result.append(".".join(parts))
            return
        if len(parts) == 4 or start == len(s):
            return

        for length in range(1, 4):
            if start + length > len(s):
                break
            segment = s[start:start + length]
            if len(segment) > 1 and segment[0] == '0':
                break
            if int(segment) > 255:
                break
            backtrack(start + length, parts + [segment])

    backtrack(0, [])
    return result

# Test
print(restore_ip_addresses("25525511135"))
# ["255.255.11.135","255.255.111.35"]
print(restore_ip_addresses("0000"))  # ["0.0.0.0"]
print(restore_ip_addresses("1111"))  # ["1.1.1.1"]
print(restore_ip_addresses("010010"))  # ["0.10.0.10","0.100.1.0"]
```

**Complexity:** O(1) time (at most 3^4 = 81 combinations), O(1) space

**Trick:** IP address has exactly 4 parts, each 0-255, no leading zeros (except "0"). Backtrack with constraints on segment length and value.

---

## Problem 42: Decode Ways

**Problem:** Given a string `s` of digits, return the number of ways to decode it ("1" → "A", "2" → "B", ..., "26" → "Z").

**Approach:** DP. dp[i] = number of ways to decode first i characters. Check single digit (1-9) and two digits (10-26).

```python
def num_decodings(s):
    if not s or s[0] == '0':
        return 0

    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1

    for i in range(2, n + 1):
        if s[i-1] != '0':
            dp[i] += dp[i-1]
        two_digit = int(s[i-2:i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i-2]

    return dp[n]

# Test
print(num_decodings("12"))      # 2
print(num_decodings("226"))     # 3
print(num_decodings("06"))      # 0
print(num_decodings("27"))      # 1
```

**Complexity:** O(n) time, O(n) space (can be O(1) with two variables)

**Trick:** Key rules: '0' alone is invalid (can't decode). Two-digit number must be 10-26. Space-optimized version uses only prev1 and prev2 variables.

---

## Problem 43: Distinct Subsequences

**Problem:** Given strings `s` and `t`, count the number of distinct subsequences of `s` that equal `t`.

**Approach:** DP. dp[i][j] = count of subsequences of first i chars of s that form first j chars of t.

```python
def num_distinct(s, t):
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = 1

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i-1][j]
            if s[i-1] == t[j-1]:
                dp[i][j] += dp[i-1][j-1]

    return dp[m][n]

# Test
print(num_distinct("rabbbit", "rabbit"))  # 3
print(num_distinct("babgbag", "bag"))     # 5
```

**Complexity:** O(m * n) time, O(m * n) space (can optimize to O(n))

**Trick:** If characters match, we have two choices: use this character (dp[i-1][j-1]) or skip it (dp[i-1][j]). If no match, only skip. Space optimization: use single row with right-to-left update.

---

## Problem 44: Word Break

**Problem:** Given a string `s` and dictionary of words, determine if `s` can be segmented into dictionary words.

**Approach:** DP. dp[i] = True if s[:i] can be segmented. Check all possible last words.

```python
def word_break(s, word_dict):
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]

# Test
print(word_break("leetcode", ["leet", "code"]))          # True
print(word_break("applepenapple", ["apple", "pen"]))      # True
print(word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]))  # False
```

**Complexity:** O(n^2 * m) time where m is max word length, O(n) space

**Trick:** Check all possible split points j. If dp[j] is True and s[j:i] is in dictionary, then dp[i] is True. Early break when found helps performance.

---

## Problem 45: Word Break II

**Problem:** Given string `s` and dictionary, return all possible sentences where words are from dictionary.

**Approach:** Backtracking with memoization. At each position, try all dictionary words that match.

```python
def word_break_ii(s, word_dict):
    word_set = set(word_dict)
    memo = {}

    def backtrack(start):
        if start == len(s):
            return [""]
        if start in memo:
            return memo[start]

        result = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                for sentence in backtrack(end):
                    if sentence:
                        result.append(word + " " + sentence)
                    else:
                        result.append(word)

        memo[start] = result
        return result

    return backtrack(0)

# Test
print(word_break_ii("catsanddog", ["cat","cats","and","sand","dog"]))
# ["cat sand dog","cats and dog"]
print(word_break_ii("pineapplepenapple", ["apple","pen","applepen","pine","pineapple"]))
# ["pine apple pen apple","pineapple pen apple","pine applepen apple"]
```

**Complexity:** O(n * 2^n) worst case, O(n) space for memoization

**Trick:** Memoization is crucial to avoid recomputation. Without it, exponential time. Try all possible word endings at each position and recurse for the rest.

---

# ═══════════════════════════════════════════════════════════════
# HARD PROBLEMS (46-50)
# ═══════════════════════════════════════════════════════════════

---

## Problem 46: Edit Distance

**Problem:** Given two strings `word1` and `word2`, find the minimum number of operations (insert, delete, replace) to convert `word1` to `word2`.

**Approach:** 2D DP. dp[i][j] = min operations to convert word1[:i] to word2[:j]. If characters match, no operation needed.

```python
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],      # delete
                    dp[i][j-1],      # insert
                    dp[i-1][j-1]     # replace
                )

    return dp[m][n]

# Test
print(min_distance("horse", "ros"))      # 3
print(min_distance("intention", "execution"))  # 5
```

**Complexity:** O(m * n) time, O(m * n) space (can optimize to O(min(m, n)))

**Trick:** Three operations map to: dp[i-1][j] + 1 (delete from word1), dp[i][j-1] + 1 (insert into word1), dp[i-1][j-1] + 1 (replace). If characters match, just take diagonal.

---

## Problem 47: Regular Expression Matching

**Problem:** Implement regex matching with support for `.` (any single char) and `*` (zero or more of preceding element).

**Approach:** 2D DP. dp[i][j] = True if s[:i] matches p[:j]. Handle '*' by checking zero occurrence or one more match.

```python
def is_match(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Handle patterns like a*, a*b*, etc.
    for j in range(2, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                # Zero occurrences of preceding char
                dp[i][j] = dp[i][j-2]
                # One or more occurrences
                if p[j-2] == '.' or p[j-2] == s[i-1]:
                    dp[i][j] = dp[i][j] or dp[i-1][j]
            elif p[j-1] == '.' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]

    return dp[m][n]

# Test
print(is_match("aa", "a"))      # False
print(is_match("aa", "a*"))     # True
print(is_match("ab", ".*"))     # True
print(is_match("aab", "c*a*b")) # True
print(is_match("mississippi", "mis*is*p*."))  # False
```

**Complexity:** O(m * n) time, O(m * n) space

**Trick:** When encountering '*', two choices: (1) ignore pattern (dp[i][j-2]), or (2) if current chars match, keep consuming (dp[i-1][j]). '.' matches any char like normal comparison.

---

## Problem 48: Wildcard Pattern Matching

**Problem:** Given string `s` and pattern `p` with `?` (any single char) and `*` (any sequence including empty), determine if they match.

**Approach:** 2D DP. dp[i][j] = True if s[:i] matches p[:j]. '*' can match empty or extend.

```python
def is_match_wildcard(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    for j in range(1, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-1]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                # * matches empty (dp[i][j-1]) or extends (dp[i-1][j])
                dp[i][j] = dp[i][j-1] or dp[i-1][j]
            elif p[j-1] == '?' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]

    return dp[m][n]

# Test
print(is_match_wildcard("aa", "a"))      # False
print(is_match_wildcard("aa", "*"))      # True
print(is_match_wildcard("cb", "?a"))     # False
print(is_match_wildcard("adceb", "*a*b"))  # True
print(is_match_wildcard("acdcb", "a*c?b"))  # False
```

**Complexity:** O(m * n) time, O(m * n) space

**Trick:** Key difference from regex: `*` here matches ANY sequence (not just preceding char). So `dp[i][j] = dp[i][j-1] or dp[i-1][j]` - either * is empty, or * extends to cover s[i-1].

---

## Problem 49: Shortest Common Supersequence

**Problem:** Given two strings `str1` and `str2`, return the shortest string that has both as subsequences.

**Approach:** Find LCS first. Build supersequence by merging characters, inserting non-LCS characters at proper positions.

```python
def shortest_common_supersequence(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Build SCS by backtracking through LCS
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if str1[i-1] == str2[j-1]:
            result.append(str1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            result.append(str1[i-1])
            i -= 1
        else:
            result.append(str2[j-1])
            j -= 1

    while i > 0:
        result.append(str1[i-1])
        i -= 1
    while j > 0:
        result.append(str2[j-1])
        j -= 1

    return "".join(result[::-1])

# Test
print(shortest_common_supersequence("abac", "cab"))  # "cabac"
print(shortest_common_supersequence("geek", "eke"))  # "geeke"
```

**Complexity:** O(m * n) time, O(m * n) space

**Trick:** SCS length = len(str1) + len(str2) - LCS_length. To build the string, trace back through LCS table: common chars go once, non-common chars from both strings go in order.

---

## Problem 50: Longest Duplicate Substring

**Problem:** Given a string `s`, find the longest substring that appears at least twice.

**Approach:** Binary search on length + Rolling hash (Rabin-Karp). For each candidate length, check if any substring of that length appears twice.

```python
def longest_dup_substring(s):
    def has_duplicate(length):
        seen = set()
        h = 0
        base = 26
        mod = 2**64
        power = pow(base, length - 1, mod)

        for i in range(len(s)):
            h = (h * base + ord(s[i]) - ord('a')) % mod
            if i >= length:
                h = (h - (ord(s[i - length]) - ord('a')) * power % mod + mod) % mod
            if i >= length - 1:
                if h in seen:
                    return i - length + 1
                seen.add(h)

        return -1

    left, right = 0, len(s) - 1
    result = -1
    while left <= right:
        mid = (left + right) // 2
        pos = has_duplicate(mid)
        if pos != -1:
            result = pos
            left = mid + 1
        else:
            right = mid - 1

    return s[result:result + left - 1] if result != -1 else ""

# Test
print(longest_dup_substring("banana"))  # "ana"
print(longest_dup_substring("abcd"))    # ""
```

**Complexity:** O(n log n) time, O(n) space

**Trick:** Binary search reduces O(n^2) to O(n log n). Rolling hash allows O(1) substring hash update. Use large modulus to minimize collisions. Alternative: suffix array + LCP array approach.

---

# ═══════════════════════════════════════════════════════════════
# QUICK REFERENCE: KEY PATTERNS
# ═══════════════════════════════════════════════════════════════

## Pattern Summary

| Pattern | Problems |
|---------|----------|
| Two Pointers | 1, 3, 8, 19 |
| Sliding Window | 16, 20, 34, 35, 36 |
| Hash Map/Set | 2, 5, 9, 12, 18, 32, 39 |
| Stack | 6, 15, 25, 26, 27 |
| Backtracking | 21, 22, 41, 45 |
| Dynamic Programming | 42, 43, 44, 46, 47, 48, 49 |
| Binary Search | 50 |
| Greedy | 31, 38, 40 |
| Simulation | 14, 24, 28, 29, 33 |

## Complexity Cheat Sheet

| Problem | Time | Space |
|---------|------|-------|
| 1. Valid Palindrome | O(n) | O(1) |
| 2. Valid Anagram | O(n) | O(1) |
| 3. Reverse String | O(n) | O(1) |
| 4. Reverse Words | O(n) | O(n) |
| 5. First Unique Char | O(n) | O(1) |
| 6. Valid Parentheses | O(n) | O(n) |
| 7. Merge Alternately | O(n+m) | O(n+m) |
| 8. Length of Last Word | O(n) | O(1) |
| 9. Jewels and Stones | O(J+S) | O(J) |
| 10. Defang IP | O(n) | O(n) |
| 11. Good Pairs | O(n) | O(n) |
| 12. Sort by Frequency | O(n log n) | O(n) |
| 13. Longest Common Prefix | O(S) | O(1) |
| 14. strStr() | O(n*m) | O(1) |
| 15. Remove Outer Parens | O(n) | O(n) |
| 16. Longest No Repeat | O(n) | O(n) |
| 17. Longest Palindrome | O(n^2) | O(1) |
| 18. Group Anagrams | O(nk log k) | O(nk) |
| 19. Valid Palindrome II | O(n) | O(1) |
| 20. Min Window Substring | O(n) | O(k) |
| 21. Generate Parentheses | O(4^n/√n) | O(n) |
| 22. Letter Combinations | O(4^n * n) | O(n) |
| 23. Int to English | O(1) | O(1) |
| 24. Count and Say | O(n*m) | O(m) |
| 25. Decode String | O(n*m) | O(n) |
| 26. Basic Calculator II | O(n) | O(n) |
| 27. Simplify Path | O(n) | O(n) |
| 28. Multiply Strings | O(m*n) | O(m+n) |
| 29. Add Binary | O(max(m,n)) | O(max(m,n)) |
| 30. License Key | O(n) | O(n) |
| 31. Reorganize String | O(n log n) | O(n) |
| 32. Palindrome Perm | O(n) | O(1) |
| 33. String to Integer | O(n) | O(1) |
| 34. Longest Repeating | O(n) | O(1) |
| 35. Permutation in String | O(n) | O(1) |
| 36. Find All Anagrams | O(n) | O(1) |
| 37. Min Add Parentheses | O(n) | O(1) |
| 38. Partition Labels | O(n) | O(1) |
| 39. Alien Dictionary | O(n*m) | O(1) |
| 40. Custom Sort String | O(n+m) | O(n) |
| 41. Restore IP | O(1) | O(1) |
| 42. Decode Ways | O(n) | O(n) |
| 43. Distinct Subseq | O(m*n) | O(m*n) |
| 44. Word Break | O(n^2*m) | O(n) |
| 45. Word Break II | O(n*2^n) | O(n) |
| 46. Edit Distance | O(m*n) | O(m*n) |
| 47. Regex Matching | O(m*n) | O(m*n) |
| 48. Wildcard Matching | O(m*n) | O(m*n) |
| 49. Shortest Common Super | O(m*n) | O(m*n) |
| 50. Longest Dup Sub | O(n log n) | O(n) |

---

## Tips for Infosys SP DSE Interview

1. **Always clarify** - Ask about edge cases, empty strings, character sets
2. **Start brute force** - Explain the simple approach first, then optimize
3. **Think out loud** - Walk through your thought process
4. **Test your code** - Trace through 2-3 examples manually
5. **Know complexities** - Be ready to explain time/space of your solution
6. **Practice patterns** - Most string problems fall into 8-10 patterns
7. **Edge cases** - Empty string, single char, all same chars, no valid answer
8. **Python specifics** - Strings are immutable, use lists for mutability, `join` for efficiency

## Must-Know Built-in Functions

```python
# String methods
s.lower(), s.upper(), s.strip(), s.split(), s.replace()
s.startswith(), s.endswith(), s.isdigit(), s.isalnum()
s.find(), s.count(), s.encode()

# Collections
from collections import Counter, defaultdict, deque
Counter(s)                    # Character frequency
defaultdict(list)            # Auto-initializing dict
deque()                      # O(1) pop from both ends

# Useful patterns
char_map = [0] * 26          # Fixed-size frequency array
bit_mask = 0                 # Character presence tracking
seen = set()                 # O(1) membership check
```

---

## Interview Day Checklist

### Before Coding
- [ ] Understand the problem completely - ask clarifying questions
- [ ] Identify input constraints (string length, character set, etc.)
- [ ] Think about edge cases before writing code
- [ ] Discuss 2-3 approaches and their trade-offs
- [ ] Choose the optimal approach and explain why

### While Coding
- [ ] Use meaningful variable names
- [ ] Write clean, readable code
- [ ] Handle edge cases explicitly
- [ ] Add comments for complex logic
- [ ] Test with examples as you code

### After Coding
- [ ] Trace through at least 2 test cases manually
- [ ] Analyze time and space complexity
- [ ] Discuss potential optimizations
- [ ] Mention alternative approaches
- [ ] Consider follow-up questions

## Common Follow-Up Questions

| Problem | Likely Follow-Up |
|---------|------------------|
| Valid Palindrome | "What about Unicode characters?" |
| Valid Anagram | "Can you do it in O(1) space?" |
| Longest Substring Without Repeating | "What if string contains Unicode?" |
| Group Anagrams | "Can you solve it in O(nk) time?" |
| Minimum Window Substring | "What if pattern has duplicate chars?" |
| Word Break | "Can you return all possible segmentations?" |
| Edit Distance | "Can you find the actual operations?" |
| Decode Ways | "What if string can have leading zeros?" |
| Regular Expression Matching | "Can you handle '+' operator too?" |
| Sort Characters By Frequency | "Can you do it in O(n) time?" |

## Data Structures for String Problems

### Frequency Counting
```python
# For lowercase letters only
freq = [0] * 26
freq[ord(ch) - ord('a')] += 1

# For ASCII characters
freq = [0] * 128

# For Unicode / any character
from collections import Counter
freq = Counter(s)
```

### Sliding Window Template
```python
def sliding_window(s):
    left = 0
    window_state = {}  # or appropriate data structure
    result = 0

    for right in range(len(s)):
        # 1. Expand window: add s[right]
        char = s[right]
        window_state[char] = window_state.get(char, 0) + 1

        # 2. Shrink window while invalid
        while window_needs_shrink():
            left_char = s[left]
            window_state[left_char] -= 1
            left += 1

        # 3. Update result
        result = max(result, right - left + 1)

    return result
```

### Two Pointer Template
```python
def two_pointers(s):
    left, right = 0, len(s) - 1

    while left < right:
        if condition_met(s[left], s[right]):
            # Process and move both pointers
            left += 1
            right -= 1
        elif need_move_left(s[left]):
            left += 1
        else:
            right -= 1

    return result
```

### Backtracking Template
```python
def backtrack(path, choices):
    if base_case(path):
        result.append(path[:])  # or path.copy()
        return

    for choice in choices:
        if not is_valid(choice):
            continue
        path.append(choice)      # make choice
        backtrack(path, next_choices)  # recurse
        path.pop()               # undo choice (backtrack)
```

### DP Template for Strings
```python
def string_dp(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = ...  # initialization
    for j in range(n + 1):
        dp[0][j] = ...  # initialization

    # Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + ...  # match
            else:
                dp[i][j] = max/min(dp[i-1][j], dp[i][j-1], ...)  # mismatch

    return dp[m][n]
```

## Infosys SP DSE Specific Tips

### Technical Round Focus Areas
1. **String Manipulation** - This file covers 50 essential problems
2. **Array Operations** - Practice array-based problems too
3. **Basic Data Structures** - Stacks, Queues, HashMaps, Trees
4. **Algorithm Design** - Sorting, Searching, Basic DP, Greedy
5. **Complexity Analysis** - Be ready to explain O(n) vs O(n^2)

### Communication Tips
- Explain your approach before writing code
- Talk about trade-offs between different solutions
- Mention how you'd handle edge cases in production
- Show enthusiasm for problem-solving
- Ask clarifying questions to show thoroughness

### Time Management
- **Easy problems**: 5-10 minutes each
- **Medium problems**: 15-25 minutes each
- **Hard problems**: 25-40 minutes each
- Always allocate time for testing and optimization discussion

### Practice Schedule
- **Week 1**: Problems 1-15 (Easy) - Build confidence
- **Week 2**: Problems 16-30 (Medium Part 1) - Core patterns
- **Week 3**: Problems 31-45 (Medium Part 2) - Advanced patterns
- **Week 4**: Problems 46-50 (Hard) + Full review

## Quick Revision Cards

### Card 1: Two Pointers
**When to use:** Palindromes, sorted arrays, partition problems
**Key insight:** Move pointers based on conditions, meet in middle

### Card 2: Sliding Window
**When to use:** Substrings, subarrays, consecutive elements
**Key insight:** Expand right, shrink left, maintain window property

### Card 3: Hash Map
**When to use:** Counting, grouping, finding duplicates
**Key insight:** O(1) lookup for existence checks and frequency counts

### Card 4: Stack
**When to use:** Parentheses, expressions, nested structures
**Key insight:** LIFO for matching open/close brackets

### Card 5: Dynamic Programming
**When to use:** Optimal substructure, overlapping subproblems
**Key insight:** Build solution from smaller subproblems

### Card 6: Backtracking
**When to use:** Generate all combinations, permutations
**Key insight:** Try all options, undo choice if invalid

### Card 7: Greedy
**When to use:** Local optimal leads to global optimal
**Key insight:** Make best choice at each step

### Card 8: Binary Search
**When to use:** Sorted data, search space reduction
**Key insight:** Eliminate half the search space each step

---

## Final Notes

This comprehensive guide covers 50 essential string problems for Infosys SP DSE preparation. Each solution includes:
- Clear problem statement
- Approach explanation
- Complete working Python code
- Time and space complexity analysis
- Tips and tricks for interview success

**Key Takeaways:**
1. Master the 8 core patterns (Two Pointers, Sliding Window, Hash Map, Stack, DP, Backtracking, Greedy, Binary Search)
2. Practice explaining your thought process out loud
3. Always consider edge cases and optimize for time/space complexity
4. Build confidence with Easy problems before tackling Medium and Hard
5. Review the quick reference tables and revision cards regularly

**Good luck with your Infosys SP DSE preparation!** 🎯

---

*File: strings/string_problems.md*
*50 Problems | Easy (15) + Medium (25) + Hard (5)*
*Complete Python Solutions with Complexity Analysis*
*Prepared for Infosys SP DSE Preparation*
*Last Updated: July 2026*
