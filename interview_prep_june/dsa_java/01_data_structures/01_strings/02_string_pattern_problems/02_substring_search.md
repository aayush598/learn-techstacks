# Substring Search Patterns

Finding substrings, matching patterns, and sliding windows are bread-and-butter string problems. This guide covers the essential tools.

---

## 1. Java Built-in String Methods

Before rolling your own solution, know what Java gives you for free.

```java
String s = "Hello, World!";

// contains — does s contain substring?
s.contains("World");        // true

// indexOf — first occurrence (-1 if not found)
s.indexOf("World");         // 7
s.indexOf("xyz");           // -1

// lastIndexOf — last occurrence
s.lastIndexOf('l');         // 9

// startsWith / endsWith
s.startsWith("Hello");      // true
s.endsWith("!");            // true

// substring
s.substring(7, 12);         // "World"

// regex matching
s.matches(".*World!");      // true
```

**When to use built-ins:** Quick checks, simple substrings, and cases where the problem doesn't ask you to implement search yourself.

---

## 2. Repeated Substring Pattern

**Problem:** Given a string `s`, check if it can be constructed by taking a substring of it repeatedly.

**Example:** `"abab"` → true (`"ab" + "ab"`), `"aba"` → false

### Approach: KMP LPS Array

**Key insight:** If `s` has a repeated substring pattern, then `lps[n-1]` (the last value in the KMP failure function) will satisfy: `(n - lps[n-1])` divides `n` evenly.

```java
public static boolean repeatedSubstringPattern(String s) {
    int n = s.length();

    // Build KMP LPS (longest proper prefix which is also suffix)
    int[] lps = new int[n];
    int len = 0;
    int i = 1;

    while (i < n) {
        if (s.charAt(i) == s.charAt(len)) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0) {
                len = lps[len - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }

    int lastLps = lps[n - 1];

    // If lps value is non-zero and n is divisible by (n - lastLps),
    // then the string has a repeated pattern of length (n - lastLps)
    return lastLps > 0 && n % (n - lastLps) == 0;
}
```

**Why this works:** The LPS array tells us the longest prefix that's also a suffix. If there's significant overlap, the string is likely built from a repeating unit. The divisibility check confirms it.

**Example walkthrough:** `"ababab"`
- LPS: `[0, 0, 1, 2, 3, 4]`
- `lastLps = 4`, `n = 6`
- `n - lastLps = 2`, `6 % 2 == 0` → true (repeated `"ab"`)

### Simpler (But Slower) Approach: String Concatenation Trick

```java
public static boolean repeatedSubstringPatternSimple(String s) {
    // If s appears in (s + s) with first and last chars removed,
    // then s has a repeated pattern
    String doubled = s + s;
    return doubled.substring(1, doubled.length() - 1).contains(s);
}
```

**Time:** O(n²) for the contains check (or O(n) with KMP internally). The LPS approach is O(n) guaranteed.

### Complexity

| Metric | KPS Approach | Concat Trick |
|--------|-------------|--------------|
| Time   | O(n)        | O(n)         |
| Space  | O(n)        | O(n)         |

---

## 3. Substring with Concatenation of All Words

**Problem:** Given a string `s` and an array of words of equal length, find all starting indices where `s` contains a concatenation of every word exactly once.

**Example:** `s = "barfoothefoobarman"`, `words = ["foo","bar"]` → `[0, 9]`

### Approach: HashMap + Sliding Window

```java
public static List<Integer> findSubstring(String s, String[] words) {
    List<Integer> result = new ArrayList<>();
    if (s == null || words == null || words.length == 0) return result;

    int wordLen = words[0].length();
    int totalLen = wordLen * words.length;

    // Build frequency map of words
    Map<String, Integer> wordCount = new HashMap<>();
    for (String w : words) {
        wordCount.put(w, wordCount.getOrDefault(w, 0) + 1);
    }

    // Try each starting position modulo wordLen
    for (int i = 0; i < wordLen; i++) {
        int left = i;
        int count = 0;
        Map<String, Integer> window = new HashMap<>();

        for (int j = i; j <= s.length() - wordLen; j += wordLen) {
            String word = s.substring(j, j + wordLen);

            if (wordCount.containsKey(word)) {
                window.put(word, window.getOrDefault(word, 0) + 1);
                count++;

                // If word appears too many times, shrink from left
                while (window.get(word) > wordCount.get(word)) {
                    String leftWord = s.substring(left, left + wordLen);
                    window.put(leftWord, window.get(leftWord) - 1);
                    left += wordLen;
                    count--;
                }

                // All words matched
                if (count == words.length) {
                    result.add(left);
                }
            } else {
                // Word not in dictionary, reset window
                window.clear();
                count = 0;
                left = j + wordLen;
            }
        }
    }

    return result;
}
```

**Why the outer loop from 0 to wordLen?** Words can only start at positions that are wordLen apart. We try each alignment (offset 0, offset 1, ..., offset wordLen-1) to cover all possible concatenation start points.

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n * wordLen) |
| Space  | O(m) where m = number of unique words |

---

## 4. Longest Substring Without Repeating Characters

**Problem:** Find the length of the longest substring without repeating characters.

**Example:** `"abcabcbb"` → 3 (`"abc"`)

### Approach: Sliding Window with HashMap

```java
public static int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> lastSeen = new HashMap<>();
    int maxLen = 0;
    int left = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);

        // If char was seen and is within our window, move left past it
        if (lastSeen.containsKey(c) && lastSeen.get(c) >= left) {
            left = lastSeen.get(c) + 1;
        }

        lastSeen.put(c, right);
        maxLen = Math.max(maxLen, right - left + 1);
    }

    return maxLen;
}
```

### Alternative: Array Instead of HashMap (for ASCII)

```java
public static int lengthOfLongestSubstringArray(String s) {
    int[] lastIndex = new int[128]; // ASCII characters
    Arrays.fill(lastIndex, -1);

    int maxLen = 0;
    int left = 0;

    for (int right = 0; right < s.length(); right++) {
        left = Math.max(left, lastIndex[s.charAt(right)] + 1);
        maxLen = Math.max(maxLen, right - left + 1);
        lastIndex[s.charAt(right)] = right;
    }

    return maxLen;
}
```

**Why `Math.max(left, lastIndex[c] + 1)`?** We never want `left` to move backward. If the duplicate character is before `left`, we ignore it.

### Walkthrough: `"abba"`

| right | char | lastIndex | left (before) | left (after) | maxLen |
|-------|------|-----------|---------------|--------------|--------|
| 0 | 'a' | a=0 | 0 | 0 | 1 |
| 1 | 'b' | b=1 | 0 | 0 | 2 |
| 2 | 'b' | b=2 | 0 | 2 | 2 |
| 3 | 'a' | a=3 | 2 | 1 → 2 | 2 |

Wait — the key subtlety at right=3: `lastIndex['a'] = 0`, which is `< left (2)`, so left stays at 2. Result: 2.

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(min(n, m)) where m is the charset size |

---

## 5. Longest Repeating Character Replacement

**Problem:** Given a string and an integer `k`, find the length of the longest substring where you can replace at most `k` characters to make all characters the same.

**Example:** `s = "AABABBA"`, `k = 1` → 4 (`"AABA"` → replace B with A)

### Approach: Sliding Window with Max Frequency Tracking

```java
public static int characterReplacement(String s, int k) {
    int[] count = new int[26];
    int maxFreq = 0;  // max frequency of any single char in current window
    int left = 0;
    int maxLen = 0;

    for (int right = 0; right < s.length(); right++) {
        count[s.charAt(right) - 'A']++;
        maxFreq = Math.max(maxFreq, count[s.charAt(right) - 'A']);

        // Window size - maxFreq = number of characters we need to replace
        // If that exceeds k, shrink from left
        while (right - left + 1 - maxFreq > k) {
            count[s.charAt(left) - 'A']--;
            left++;
        }

        maxLen = Math.max(maxLen, right - left + 1);
    }

    return maxLen;
}
```

**The key formula:** `windowSize - maxFreq <= k`

- `windowSize` = total characters in window
- `maxFreq` = count of the most frequent character
- `windowSize - maxFreq` = characters that need replacing
- If this exceeds `k`, the window is too big

**Why `maxFreq` only increases?** We track the all-time max frequency. The window might temporarily be "too small" but never incorrectly too large. This is a subtle optimization — even though `maxFreq` might not represent the current window perfectly, it's always >= the actual max frequency, which keeps the answer correct.

### Walkthrough: `"AABABBA"`, k=1

| right | Window | maxFreq | Replace needed | Valid? | maxLen |
|-------|--------|---------|----------------|--------|--------|
| 0 | A | 1 | 0 | yes | 1 |
| 1 | AA | 2 | 0 | yes | 2 |
| 2 | AAB | 2 | 1 | yes | 3 |
| 3 | AABA | 3 | 1 | yes | 4 |
| 4 | AABAB | 3 | 2 | no → shrink | 4 |
| 5 | ABAB | 2 | 2 | no → shrink | 4 |
| 6 | BABBA | 3 | 2 | no → shrink | 4 |

Answer: 4

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  | (fixed 26-size array) |

---

## Test Cases

```java
public static void main(String[] args) {
    // Test 1: Repeated Substring Pattern
    System.out.println(repeatedSubstringPattern("abab"));    // true
    System.out.println(repeatedSubstringPattern("aba"));     // false
    System.out.println(repeatedSubstringPattern("abcabcabc")); // true

    // Test 2: Substring Concatenation
    System.out.println(findSubstring(
        "barfoothefoobarman", new String[]{"foo", "bar"}));  // [0, 9]
    System.out.println(findSubstring(
        "wordgoodgoodgoodbestword", new String[]{"word","good","best","word"})); // []

    // Test 3: Longest Without Repeating
    System.out.println(lengthOfLongestSubstring("abcabcbb")); // 3
    System.out.println(lengthOfLongestSubstring("bbbbb"));    // 1
    System.out.println(lengthOfLongestSubstring("pwwkew"));   // 4
    System.out.println(lengthOfLongestSubstring(""));         // 0

    // Test 4: Longest Repeating Character Replacement
    System.out.println(characterReplacement("AABABBA", 1)); // 4
    System.out.println(characterReplacement("ABAB", 2));    // 4
}
```

---

## Quick Reference

| Problem | Key Pattern | Time |
|---------|------------|------|
| Repeated substring | KMP LPS array | O(n) |
| Concat all words | HashMap + sliding window | O(n·w) |
| Longest without repeating | Sliding window + last-seen map | O(n) |
| Longest repeating replacement | Sliding window + max frequency | O(n) |
