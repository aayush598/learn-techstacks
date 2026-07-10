# Find All Anagrams in a String

This is a fixed-size sliding window problem with a twist — instead of summing numbers, we're comparing character frequencies. It's a great example of how to adapt the sliding window template to different problems.

## Problem Statement

Given two strings `s` and `p`, find all start indices of `p`'s anagrams in `s`.

```
Input:  s = "cbaebabacd", p = "abc"
Output: [0, 6]
Explanation:
  s[0..2] = "cba" is an anagram of "abc"
  s[6..8] = "bac" is an anagram of "abc"

s:  c  b  a  e  b  a  b  a  c  d
    [---anagram---]              → index 0
                      [---anagram---] → index 6
```

## Brute Force (O(n·k·log k))

Sort each window and compare with sorted pattern. Slow.

```java
public List<Integer> findAnagramsBrute(String s, String p) {
    List<Integer> result = new ArrayList<>();
    int k = p.length();
    char[] pSorted = p.toCharArray();
    Arrays.sort(pSorted);

    for (int i = 0; i <= s.length() - k; i++) {
        char[] window = s.substring(i, i + k).toCharArray();
        Arrays.sort(window);
        if (Arrays.equals(window, pSorted)) {
            result.add(i);
        }
    }

    return result;
}
```

Sorting each window makes this O(n·k log k). We can do O(n) with frequency arrays.

## Frequency Array Approach (O(n·26))

```java
public List<Integer> findAnagrams(String s, String p) {
    List<Integer> result = new ArrayList<>();
    if (s.length() < p.length()) return result;

    int[] pFreq = new int[26];
    int[] wFreq = new int[26];
    int k = p.length();

    // Count frequency of pattern
    for (char c : p.toCharArray()) {
        pFreq[c - 'a']++;
    }

    // First window
    for (int i = 0; i < k; i++) {
        wFreq[s.charAt(i) - 'a']++;
    }

    // Check first window
    if (Arrays.equals(pFreq, wFreq)) {
        result.add(0);
    }

    // Slide the window
    for (int i = k; i < s.length(); i++) {
        // Add new char
        wFreq[s.charAt(i) - 'a']++;
        // Remove old char
        wFreq[s.charAt(i - k) - 'a']--;

        if (Arrays.equals(pFreq, wFreq)) {
            result.add(i - k + 1);
        }
    }

    return result;
}
```

### How It Works

1. Create frequency arrays for `p` and the current window
2. Initially, compute frequency of first `k` characters
3. For each subsequent position: add the new character, remove the old character
4. Compare the two frequency arrays

Each step is O(26) = O(1) for the array comparison. Total: O(n).

## Optimized: Matching Count (O(n))

Comparing two 26-element arrays at each step is still work. We can optimize by tracking how many characters *match* between the window and pattern.

```java
public List<Integer> findAnagramsOptimized(String s, String p) {
    List<Integer> result = new ArrayList<>();
    if (s.length() < p.length()) return result;

    int[] freq = new int[26];
    for (char c : p.toCharArray()) {
        freq[c - 'a']++;
    }

    int left = 0;
    int right = 0;
    int count = p.length(); // Number of characters we still need to match

    while (right < s.length()) {
        // Expand window: if the current char is needed, decrement count
        if (freq[s.charAt(right) - 'a'] > 0) {
            count--;
        }
        freq[s.charAt(right) - 'a']--;
        right++;

        // Window size matches pattern length
        if (right - left == p.length()) {
            if (count == 0) {
                result.add(left);
            }

            // Shrink window: if the left char was part of pattern, increment count
            if (freq[s.charAt(left) - 'a'] >= 0) {
                count++;
            }
            freq[s.charAt(left) - 'a']++;
            left++;
        }
    }

    return result;
}
```

### The Count Variable

`count` tracks how many characters from the pattern are *missing* from the current window:
- When `count == 0`, the window contains exactly the characters needed
- When we see a character from `p` (freq > 0 before decrementing), we reduce `count`
- When a character leaves the window and its freq becomes >= 0 (meaning it was part of `p`), we increase `count`

This is O(n) with no array comparison at each step!

### Dry Run

```
s = "cbaebabacd", p = "abc"
freq = [1,1,1,...], count = 3

right=0, c='c': freq['c']=1>0 → count=2, freq['c']=0,  right=1
  window size = 1 < 3 → skip shrink
right=1, c='b': freq['b']=1>0 → count=1, freq['b']=0,  right=2
  window size = 2 < 3 → skip shrink
right=2, c='a': freq['a']=1>0 → count=0, freq['a']=0,  right=3
  window size = 3 == 3, count=0 → add index 0!
  shrink: c='c', freq['c']=0>=0 → count=1, freq['c']=1, left=1

right=3, c='e': freq['e']=0 NOT >0 → count stays 1, freq['e']=-1, right=4
  window size = 4 > 3? No, right-left=3 == 3
  count=1≠0, skip add
  shrink: c='b', freq['b']=0>=0 → count=2, freq['b']=1, left=2

right=4, c='b': freq['b']=1>0 → count=1, freq['b']=0, right=5
  window size=3, count=1≠0
  shrink: c='a', freq['a']=0>=0 → count=2, freq['a']=1, left=3

...continues...
right=8, c='c': freq['c']=0 NOT >0 → freq['c']=-1, right=9
  window size=3, count=0 → add index 6!
  shrink: c='b', freq['b']=0>=0 → count=1, freq['b']=1, left=7

Result: [0, 6] ✓
```

## HashMap Version (for Any Character Set)

If the character set isn't limited to lowercase letters:

```java
public List<Integer> findAnagramsHashMap(String s, String p) {
    List<Integer> result = new ArrayList<>();
    if (s.length() < p.length()) return result;

    Map<Character, Integer> pMap = new HashMap<>();
    Map<Character, Integer> wMap = new HashMap<>();

    for (char c : p.toCharArray()) {
        pMap.put(c, pMap.getOrDefault(c, 0) + 1);
    }

    int k = p.length();
    for (int i = 0; i < k; i++) {
        char c = s.charAt(i);
        wMap.put(c, wMap.getOrDefault(c, 0) + 1);
    }

    if (wMap.equals(pMap)) result.add(0);

    for (int i = k; i < s.length(); i++) {
        // Add new char
        char add = s.charAt(i);
        wMap.put(add, wMap.getOrDefault(add, 0) + 1);

        // Remove old char
        char remove = s.charAt(i - k);
        wMap.put(remove, wMap.get(remove) - 1);
        if (wMap.get(remove) == 0) wMap.remove(remove);

        if (wMap.equals(pMap)) result.add(i - k + 1);
    }

    return result;
}
```

## Complexity Comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Sort each window | O(n·k log k) | O(k) | Avoid |
| Frequency arrays | O(n·26) | O(26) | Good for lowercase letters |
| Matching count | O(n) | O(26) | Best for lowercase |
| HashMap | O(n) | O(k) | General character set |

## Interview Tips

1. **Start with frequency arrays** — it's the most intuitive and works for the given constraint (lowercase letters)
2. **Optimize to matching count** — shows deeper understanding
3. **Mention the HashMap version** — shows you can handle any character set
4. **Explain the count variable carefully** — it's the trickiest part

## Edge Cases

```java
// Pattern longer than string
s = "ab", p = "abc" → []

// Empty pattern
s = "abc", p = "" → []

// Exact match
s = "abc", p = "abc" → [0]

// Multiple overlapping anagrams
s = "abab", p = "ab" → [0, 1, 2]

// No anagrams
s = "aaaa", p = "abc" → []
```

The key takeaway: when you need to compare substrings by character content (not order), frequency arrays + sliding window is the way to go. The matching count optimization removes the O(26) comparison overhead at each step.
