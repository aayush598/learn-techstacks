# 03 — Recursion on Strings

Strings are naturally recursive — every string is a character followed by a smaller string. This makes them perfect for recursive thinking.

---

## 1. Skip a Character

Remove all occurrences of a character from a string.

```java
// Approach 1: Return new string
String skipChar(String s, char skip) {
    if (s.isEmpty()) return "";
    char ch = s.charAt(0);
    if (ch == skip) {
        return skipChar(s.substring(1), skip);
    } else {
        return ch + skipChar(s.substring(1), skip);
    }
}

// Usage
System.out.println(skipChar("baccad", 'a'));  // "bccd"

// Approach 2: Pass result as parameter (efficient, no substring copies)
void skipChar(String s, char skip, StringBuilder result) {
    if (s.isEmpty()) return;
    if (s.charAt(0) != skip) result.append(s.charAt(0));
    skipChar(s.substring(1), skip, result);
}

StringBuilder sb = new StringBuilder();
skipChar("baccad", 'a', sb);
System.out.println(sb);  // "bccd"
```

---

## 2. Skip a Substring

Skip an entire substring when it appears.

```java
String skipSubstring(String s, String skip) {
    if (s.isEmpty()) return "";

    if (s.startsWith(skip)) {
        return skipSubstring(s.substring(skip.length()), skip);
    } else {
        return s.charAt(0) + skipSubstring(s.substring(1), skip);
    }
}

// Skip "apple" but not "app" within "apple"
System.out.println(skipSubstring("bacapplecdah", "apple"));  // "baccdah"

// Skip "app" but not when it's part of "apple"
String skipAppNotApple(String s) {
    if (s.isEmpty()) return "";
    if (s.startsWith("apple")) {
        return skipAppNotApple(s.substring(5));  // skip entire "apple"
    } else if (s.startsWith("app")) {
        return skipAppNotApple(s.substring(3));  // skip "app"
    } else {
        return s.charAt(0) + skipAppNotApple(s.substring(1));
    }
}

System.out.println(skipAppNotApple("appmangoapple"));  // "mango"
```

---

## 3. Subsequence Generation

Generate all subsequences of a string (not necessarily contiguous, but maintain order).

```java
void subsequences(String s, int index, String current, List<String> result) {
    if (index == s.length()) {
        result.add(current);
        return;
    }
    // Exclude current character
    subsequences(s, index + 1, current, result);
    // Include current character
    subsequences(s, index + 1, current + s.charAt(index), result);
}

List<String> result = new ArrayList<>();
subsequences("abc", 0, "", result);
System.out.println(result);
// ["", "c", "b", "bc", "a", "ac", "ab", "abc"]
// Order depends on include/exclude sequencing

// With substring (simpler API but O(n) per call)
void subsequences(String s, String current, List<String> result) {
    if (s.isEmpty()) {
        result.add(current);
        return;
    }
    char ch = s.charAt(0);
    subsequences(s.substring(1), current, result);          // exclude
    subsequences(s.substring(1), current + ch, result);     // include
}

// ASCII subsequences: include char, include uppercase, skip
void subseqAscii(String s, int index, String current, List<String> result) {
    if (index == s.length()) {
        result.add(current);
        return;
    }
    char ch = s.charAt(index);
    subseqAscii(s, index + 1, current, result);
    subseqAscii(s, index + 1, current + ch, result);
    subseqAscii(s, index + 1, current + (char)(ch - 32), result);  // uppercase
}
```

**Complexity:** O(2^n) subsequences, each taking O(n) to print → O(n * 2^n).

---

## 4. Permutations of a String

Generate all permutations of a string.

```java
void permutations(String s, String current, List<String> result) {
    if (s.isEmpty()) {
        result.add(current);
        return;
    }
    for (int i = 0; i < s.length(); i++) {
        char ch = s.charAt(i);
        String remaining = s.substring(0, i) + s.substring(i + 1);
        permutations(remaining, current + ch, result);
    }
}

List<String> perms = new ArrayList<>();
permutations("abc", "", perms);
System.out.println(perms);
// [abc, acb, bac, bca, cab, cba] — 6 = 3! permutations

// Number of permutations: n! (3! = 6, 4! = 24, 5! = 120)
// Complexity: O(n * n!) — n! permutations, each building an O(n) string
```

### Permutations of Array (Like LeetCode 46)

```java
void permute(int[] nums, List<Integer> current, List<List<Integer>> result) {
    if (current.size() == nums.length) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int num : nums) {
        if (current.contains(num)) continue;  // skip used elements
        current.add(num);
        permute(nums, current, result);
        current.remove(current.size() - 1);
    }
}
```

**More efficient with visited boolean array:**

```java
void permute(int[] nums, boolean[] used, List<Integer> current, List<List<Integer>> result) {
    if (current.size() == nums.length) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        used[i] = true;
        current.add(nums[i]);
        permute(nums, used, current, result);
        current.remove(current.size() - 1);
        used[i] = false;
    }
}
```

---

## 5. Palindrome Check

```java
boolean isPalindrome(String s, int left, int right) {
    if (left >= right) return true;
    if (s.charAt(left) != s.charAt(right)) return false;
    return isPalindrome(s, left + 1, right - 1);
}

// Overloaded helper
boolean isPalindrome(String s) {
    return isPalindrome(s, 0, s.length() - 1);
}

// Usage
System.out.println(isPalindrome("racecar"));  // true
System.out.println(isPalindrome("hello"));    // false

// Recursive without two pointers (O(n^2) due to substring)
boolean isPalindromeSubstring(String s) {
    if (s.length() <= 1) return true;
    if (s.charAt(0) != s.charAt(s.length() - 1)) return false;
    return isPalindromeSubstring(s.substring(1, s.length() - 1));
}
```

---

## 6. Letter Combinations (Phone Number Problem)

LeetCode 17: Given digits "23", return all letter combinations.

```java
void letterCombinations(String digits, int index, String current, List<String> result) {
    if (index == digits.length()) {
        result.add(current);
        return;
    }
    String letters = getLetters(digits.charAt(index));
    for (int i = 0; i < letters.length(); i++) {
        letterCombinations(digits, index + 1, current + letters.charAt(i), result);
    }
}

String getLetters(char digit) {
    switch (digit) {
        case '2': return "abc";
        case '3': return "def";
        case '4': return "ghi";
        case '5': return "jkl";
        case '6': return "mno";
        case '7': return "pqrs";
        case '8': return "tuv";
        case '9': return "wxyz";
        default: return "";
    }
}

List<String> result = new ArrayList<>();
if (!digits.isEmpty()) letterCombinations("23", 0, "", result);
System.out.println(result);
// [ad, ae, af, bd, be, bf, cd, ce, cf]
```

**Complexity:** O(4^n) where n = number of digits (max 4 letters per digit).

---

## 7. Complete Example: All String Operations

```java
public class RecursiveStringOps {

    // Remove consecutive duplicates
    static String removeConsecutiveDupes(String s) {
        if (s.length() <= 1) return s;
        if (s.charAt(0) == s.charAt(1))
            return removeConsecutiveDupes(s.substring(1));
        return s.charAt(0) + removeConsecutiveDupes(s.substring(1));
    }
    // "aabbccdde" -> "abcde"

    // Count vowels
    static int countVowels(String s, int i) {
        if (i == s.length()) return 0;
        char c = Character.toLowerCase(s.charAt(i));
        int count = (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') ? 1 : 0;
        return count + countVowels(s, i + 1);
    }

    // Replace character
    static String replace(String s, char oldChar, char newChar, int i) {
        if (i == s.length()) return "";
        char c = (s.charAt(i) == oldChar) ? newChar : s.charAt(i);
        return c + replace(s, oldChar, newChar, i + 1);
    }

    // Reverse string
    static String reverse(String s) {
        if (s.isEmpty()) return "";
        return reverse(s.substring(1)) + s.charAt(0);
    }

    // Move all 'x' to the end
    static String moveXToEnd(String s) {
        if (s.isEmpty()) return "";
        char ch = s.charAt(0);
        String rest = moveXToEnd(s.substring(1));
        if (ch == 'x') return rest + ch;
        return ch + rest;
    }
    // "axbcxdx" -> "abcxxxx"

    public static void main(String[] args) {
        System.out.println(removeConsecutiveDupes("aabbccdde"));
        System.out.println(countVowels("Hello World", 0));  // 3
        System.out.println(reverse("hello"));  // "olleh"
        System.out.println(moveXToEnd("axbcxdx"));  // "abcxxxx"
    }
}
```

---

## 8. The Substring Performance Trap

Using `s.substring(1)` in recursion creates a **new String** every call. For a string of length n, this is O(n^2) total characters copied.

```java
// O(n^2) due to substring copies
String skipCharBad(String s) {
    if (s.isEmpty()) return "";
    if (s.charAt(0) == 'a') return skipCharBad(s.substring(1));
    return s.charAt(0) + skipCharBad(s.substring(1));
}

// Better: pass index
void skipCharBetter(String s, int index, StringBuilder result) {
    if (index == s.length()) return;
    if (s.charAt(index) != 'a') result.append(s.charAt(index));
    skipCharBetter(s, index + 1, result);
}
```

---

## Cheat Sheet

```java
Skip char        -> s.isEmpty() ? "" : (match ? skip : keep + recurse)
Skip substring   -> s.startsWith(skip) ? recurse(skip.len) : keep + recurse
Subsequences     -> include/exclude current char (O(2^n))
Permutations     -> for each char: remove, recurse on rest, add back
Palindrome       -> check ends, recurse inward
Phone letters    -> for each letter of digit: append, recurse
```

