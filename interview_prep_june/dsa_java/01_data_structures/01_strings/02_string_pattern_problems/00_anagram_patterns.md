# Anagram Patterns

Anagrams are one of the most frequently tested string concepts in interviews. Master these patterns and you'll have a solid toolkit for any anagram-related problem.

---

## 1. Check If Two Strings Are Anagrams

**Core Idea:** Two strings are anagrams if they have the same characters with the same frequencies. We can use a frequency array of size 26 (for lowercase English letters) to compare.

### Approach: Frequency Array (int[26])

```java
public static boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;

    int[] freq = new int[26];

    for (int i = 0; i < s.length(); i++) {
        freq[s.charAt(i) - 'a']++;
        freq[t.charAt(i) - 'a']--;
    }

    for (int count : freq) {
        if (count != 0) return false;
    }
    return true;
}
```

**How it works:**
- Increment for characters in `s`, decrement for characters in `t`
- If every slot in `freq[]` is zero, the strings are anagrams
- We process both strings in a single pass, so it's O(n)

### Alternative: Count Approach (Single Array, Two Passes)

```java
public static boolean isAnagramCount(String s, String t) {
    if (s.length() != t.length()) return false;

    int[] count = new int[26];

    for (char c : s.toCharArray()) {
        count[c - 'a']++;
    }

    for (char c : t.toCharArray()) {
        count[c - 'a']--;
        if (count[c - 'a'] < 0) return false; // early exit
    }
    return true;
}
```

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  | (fixed 26-size array) |

### Edge Cases

- Different lengths → immediately not anagrams
- Strings with Unicode characters → use `HashMap<Character, Integer>` instead
- Case sensitivity → convert to lowercase first

---

## 2. Group Anagrams

**Problem:** Given an array of strings, group the anagrams together.

**Example:** `["eat","tea","tan","ate","nat","bat"]` → `[["eat","tea","ate"],["tan","nat"],["bat"]]`

### Approach 1: Sorted String as HashMap Key

```java
public static List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> map = new HashMap<>();

    for (String s : strs) {
        char[] chars = s.toCharArray();
        Arrays.sort(chars);
        String key = new String(chars);

        map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }

    return new ArrayList<>(map.values());
}
```

**Why this works:** All anagrams produce the same sorted string, so they map to the same key.

**Time:** O(n * k log k) where k is the max string length (sorting each string)

### Approach 2: Char Count Signature (O(n*k))

```java
public static List<List<String>> groupAnagramsOptimized(String[] strs) {
    Map<String, List<String>> map = new HashMap<>();

    for (String s : strs) {
        int[] count = new int[26];
        for (char c : s.toCharArray()) {
            count[c - 'a']++;
        }

        // Build a signature string like "#1#0#0...#1" (26 counts separated by '#')
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 26; i++) {
            sb.append('#');
            sb.append(count[i]);
        }
        String key = sb.toString();

        map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }

    return new ArrayList<>(map.values());
}
```

**Why this is faster:** We avoid sorting. Building the count signature is O(k) vs O(k log k).

### Complexity Comparison

| Approach | Time | Space |
|----------|------|-------|
| Sorted key | O(n * k log k) | O(n * k) |
| Count signature | O(n * k) | O(n * k) |

---

## 3. Find All Anagrams of Pattern P in String S

**Problem:** Given strings `s` and `p`, find all starting indices of `p`'s anagrams in `s`.

**Example:** `s = "cbaebabacd"`, `p = "abc"` → `[0, 6]`

### Approach: Sliding Window + Frequency Array

```java
public static List<Integer> findAnagrams(String s, String p) {
    List<Integer> result = new ArrayList<>();
    if (s.length() < p.length()) return result;

    int[] pCount = new int[26];
    int[] sCount = new int[26];

    // Build pattern frequency
    for (char c : p.toCharArray()) {
        pCount[c - 'a']++;
    }

    // Initialize first window
    for (int i = 0; i < p.length(); i++) {
        sCount[s.charAt(i) - 'a']++;
    }

    if (Arrays.equals(pCount, sCount)) {
        result.add(0);
    }

    // Slide the window
    for (int i = p.length(); i < s.length(); i++) {
        // Add new character on the right
        sCount[s.charAt(i) - 'a']++;

        // Remove character on the left
        sCount[s.charAt(i - p.length()) - 'a']--;

        if (Arrays.equals(pCount, sCount)) {
            result.add(i - p.length() + 1);
        }
    }

    return result;
}
```

### Optimization: Track Match Count Instead of Comparing Arrays

```java
public static List<Integer> findAnagramsOptimized(String s, String p) {
    List<Integer> result = new ArrayList<>();
    if (s.length() < p.length()) return result;

    int[] count = new int[26];

    for (int i = 0; i < p.length(); i++) {
        count[p.charAt(i) - 'a']++;
        count[s.charAt(i) - 'a']--;
    }

    if (allZero(count)) result.add(0);

    for (int i = p.length(); i < s.length(); i++) {
        int right = s.charAt(i) - 'a';
        int left = s.charAt(i - p.length()) - 'a';

        count[right]--;    // add right char
        count[left]++;     // remove left char

        if (allZero(count)) {
            result.add(i - p.length() + 1);
        }
    }

    return result;
}

private static boolean allZero(int[] count) {
    for (int c : count) {
        if (c != 0) return false;
    }
    return true;
}
```

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  | (fixed 26-size array) |

---

## 4. Minimum Changes to Make Two Strings Anagrams

**Problem:** Given two strings, find the minimum number of character deletions to make them anagrams.

**Example:** `s1 = "abc"`, `s2 = "amnop"` → Answer: 6 (delete 'm','n','o','p' from s2 and 'b','c' from s1)

### Approach: Frequency Count Difference

```java
public static int minChanges(String s1, String s2) {
    int[] freq = new int[26];

    for (char c : s1.toCharArray()) {
        freq[c - 'a']++;
    }

    for (char c : s2.toCharArray()) {
        freq[c - 'a']--;
    }

    int changes = 0;
    for (int count : freq) {
        changes += Math.abs(count);
    }

    return changes / 2; // each mismatch accounts for 2 deletions
}
```

**Why divide by 2:** If `freq['a'] = 3`, it means s1 has 3 extra 'a's and s2 has 0. We need to delete 3 from s1. But if `freq['a'] = -2`, s2 has 2 extra. We sum absolute values and divide by 2 because each absolute difference represents a pair of excess characters.

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## 5. Valid Palindrome After Removing at Most One Character

**Problem:** Given a string, determine if it can be a palindrome after removing at most one character.

**Example:** `"aba"` → true, `"abca"` → true (remove 'b'), `"abc"` → false

### Approach: Two Pointers with Tolerance

```java
public static boolean validPalindrome(String s) {
    int left = 0;
    int right = s.length() - 1;

    while (left < right) {
        if (s.charAt(left) != s.charAt(right)) {
            // Try skipping left char OR right char
            return isPalindrome(s, left + 1, right)
                || isPalindrome(s, left, right - 1);
        }
        left++;
        right--;
    }
    return true; // already a palindrome
}

private static boolean isPalindrome(String s, int left, int right) {
    while (left < right) {
        if (s.charAt(left) != s.charAt(right)) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}
```

**Key insight:** When we find a mismatch, we have exactly two choices — skip the left character or skip the right character. If either choice leads to a palindrome, the answer is true.

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## Test Cases

```java
public static void main(String[] args) {
    // Test 1: Is Anagram
    System.out.println(isAnagram("listen", "silent"));  // true
    System.out.println(isAnagram("hello", "world"));    // false
    System.out.println(isAnagram("a", "a"));            // true
    System.out.println(isAnagram("ab", "a"));           // false

    // Test 2: Group Anagrams
    String[] strs = {"eat", "tea", "tan", "ate", "nat", "bat"};
    System.out.println(groupAnagrams(strs));
    // [[eat, tea, ate], [tan, nat], [bat]]

    // Test 3: Find Anagrams
    System.out.println(findAnagrams("cbaebabacd", "abc"));  // [0, 6]
    System.out.println(findAnagrams("abab", "ab"));          // [0, 1, 2]

    // Test 4: Min Changes
    System.out.println(minChanges("abc", "amnop"));  // 6
    System.out.println(minChanges("aabb", "abcc"));  // 2

    // Test 5: Valid Palindrome with Removal
    System.out.println(validPalindrome("aba"));    // true
    System.out.println(validPalindrome("abca"));   // true
    System.out.println(validPalindrome("abc"));    // false
}
```

---

## Quick Reference Cheat Sheet

| Problem | Approach | Time | Space |
|---------|----------|------|-------|
| Is anagram | freq array + single pass | O(n) | O(1) |
| Group anagrams | sorted key or count sig | O(n·k log k) or O(n·k) | O(n·k) |
| Find anagrams | sliding window + freq | O(n) | O(1) |
| Min changes | freq diff sum | O(n) | O(1) |
| Palindrome + 1 removal | two pointers with skip | O(n) | O(1) |

---

## Common Pitfalls

1. **Forgetting to check lengths first** in `isAnagram` — always do an early return
2. **Off-by-one in sliding window** — the window size is `p.length()`, so the left index to remove is `i - p.length()`
3. **Case sensitivity** — these solutions assume lowercase only. For mixed case, add `Character.toLowerCase()` conversion
4. **Integer overflow in signature strings** — not an issue with char counts, but be careful if using other hash strategies
5. **Confusing anagrams with palindromes** — anagrams reorder all characters; palindromes read the same forwards and backwards
