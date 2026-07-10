# Minimum Window Substring

This is the hardest of the classic sliding window problems. It combines variable-size window with frequency tracking, and the window shrinks on *both* sides.

## Problem Statement

Given two strings `s` and `t`, find the **minimum window** in `s` that contains **all characters** of `t`.

```
Input:  s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: "BANC" contains A, B, C and is the shortest such window.

s:  A  D  O  B  E  C  O  D  E  B  A  N  C
    [---A---]      [-----C-----]       
    [-----B---]         [--B--A--N--C--]
    Minimum window: BANC (indices 9-12)
```

## The Approach

This is a **variable-size sliding window with two stages**:

1. **Expand** the window until it contains all characters of `t`
2. **Contract** from the left to minimize the window while still containing all characters

### Requirements Tracking

We use a frequency map for `t`, and a `have` counter to track how many characters we've matched.

```
have tracks: how many distinct characters currently meet or exceed their required frequency
need tracks: how many distinct characters are in t
```

When `have == need`, the window is "valid" (contains all of `t`).

## The Solution

```java
public String minWindow(String s, String t) {
    if (s.length() < t.length()) return "";

    Map<Character, Integer> needMap = new HashMap<>();
    for (char c : t.toCharArray()) {
        needMap.put(c, needMap.getOrDefault(c, 0) + 1);
    }

    Map<Character, Integer> haveMap = new HashMap<>();
    int have = 0;
    int need = needMap.size();

    int left = 0;
    int minLen = Integer.MAX_VALUE;
    int minStart = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);

        // Add character to current window
        if (needMap.containsKey(c)) {
            haveMap.put(c, haveMap.getOrDefault(c, 0) + 1);
            if (haveMap.get(c).intValue() == needMap.get(c).intValue()) {
                have++;
            }
        }

        // Try to shrink the window from the left
        while (have == need) {
            // Update minimum window
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                minStart = left;
            }

            char leftChar = s.charAt(left);
            if (needMap.containsKey(leftChar)) {
                haveMap.put(leftChar, haveMap.get(leftChar) - 1);
                if (haveMap.get(leftChar) < needMap.get(leftChar)) {
                    have--;
                }
            }
            left++;
        }
    }

    return minLen == Integer.MAX_VALUE ? "" : s.substring(minStart, minStart + minLen);
}
```

### Understanding `have` and `need`

- `need` = number of *distinct* characters in `t` (not total length)
- `have` = number of distinct characters where the frequency in the window >= required frequency

When `t = "AABC"`:
- `needMap = {A:2, B:1, C:1}`, `need = 3`
- A window with `[A:2, B:1, C:0]` has `have = 2` (A and B match, C doesn't)
- A window with `[A:2, B:2, C:1]` has `have = 3` (all match)

### Dry Run

```
s = "ADOBECODEBANC", t = "ABC"
needMap = {A:1, B:1, C:1}, need = 3

right=0, c='A': haveMap={A:1}, have=1,  have≠need
right=1, c='D': not in needMap
right=2, c='O': not in needMap
right=3, c='B': haveMap={A:1,B:1}, have=2,  have≠need
right=4, c='E': not in needMap
right=5, c='C': haveMap={A:1,B:1,C:1}, have=3,  have==need!
  → window [0..5] = "ADOBEC", len=6, minLen=6, minStart=0
  → shrink: leftChar='A', haveMap={A:0,B:1,C:1}, have=2 → break shrink
right=6, c='O': not in needMap
right=7, c='D': not in needMap
right=8, c='E': not in needMap
right=9, c='B': haveMap={A:0,B:2,C:1}, have=2 (B had 2 > needed 1, but have was already 2)
  Wait, let's re-check. After right=5 shrink, have=2 (B and C matched, A not matched).
  haveMap was {A:0, B:1, C:1}. At right=9, B becomes 2. Since B already matched (1 >= 1), have doesn't change.
  have=2 ≠ need=3
right=10, c='A': haveMap={A:1,B:2,C:1}, have=3,  have==need!
  → window [5..10] = "ECODEB A" wait no, left was 1 after first shrink.
  
Hmm, let me re-trace more carefully.

After right=5 (found first valid window "ADOBEC"):
  left=0, have=3
  
  Shrink:
  leftChar='A': haveMap={A:0,B:1,C:1}, have=2 (A:0 < need 1), left=1
  have≠need → stop shrinking
  
  Current window: [1..5] = "DOBEC", minLen=6, minStart=0

right=6, c='O': not needed
right=7, c='D': not needed
right=8, c='E': not needed
right=9, c='B': haveMap={A:0,B:2,C:1}, have=2 (B is 2, need 1, already matched)
right=10, c='A': haveMap={A:1,B:2,C:1}, have=3! have==need!
  → window [1..10] = "DOBECODEBA", len=10, minLen stays 6
  
  Shrink:
  leftChar='D': not needed → left=2
  leftChar='O': not needed → left=3
  leftChar='B': haveMap={A:1,B:1,C:1}, have=3 (B:1 >= need 1, still matched) → left=4
  leftChar='E': not needed → left=5
  leftChar='C': haveMap={A:1,B:1,C:0}, have=2 (C:0 < need 1) → stop
  
  Current window: [6..10] = "ODEBA"? No, left=5 so from char at index 5 which is 'C'.
  
  Hmm wait, after removing left chars up to index 5, the window is [6..10] = "ODEB A".
  Actually left=6 now (after we removed index 5 'C').
  Window [6..10] = "CODEB"? No.
  
  Let me just index the string properly:
  s = A(0) D(1) O(2) B(3) E(4) C(5) O(6) D(7) E(8) B(9) A(10) N(11) C(12)
  
  After shrink at right=10, left=6. Window [6..10] = "ODEBA" = O(6) D(7) E(8) B(9) A(10).
  len=5, minLen → update to 5, minStart=6.

right=11, c='N': not needed
right=12, c='C': haveMap={A:1,B:1,C:1}, have=3! have==need!
  → window [6..12] = "ODEBANC", len=7, minLen stays 5
  
  Shrink:
  leftChar='O': not needed → left=7
  leftChar='D': not needed → left=8
  leftChar='E': not needed → left=9
  leftChar='B': haveMap={A:1,B:0,C:1}, have=2 (B:0 < need 1) → stop
  
  And left=9... wait, that's the start of "BANC"!
  
  Window [9..12] = "BANC", len=4. Update minLen=4, minStart=9.

Result: s.substring(9, 9+4) = "BANC" ✓
```

## Optimized: Array for ASCII

```java
public String minWindowArray(String s, String t) {
    if (s.length() < t.length()) return "";

    int[] need = new int[128];
    for (char c : t.toCharArray()) need[c]++;

    int[] have = new int[128];
    int required = 0;
    for (int count : need) {
        if (count > 0) required++;
    }

    int matched = 0;
    int left = 0;
    int minLen = Integer.MAX_VALUE;
    int minStart = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        have[c]++;

        if (need[c] > 0 && have[c] == need[c]) {
            matched++;
        }

        while (matched == required) {
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                minStart = left;
            }

            char leftChar = s.charAt(left);
            have[leftChar]--;
            if (need[leftChar] > 0 && have[leftChar] < need[leftChar]) {
                matched--;
            }
            left++;
        }
    }

    return minLen == Integer.MAX_VALUE ? "" : s.substring(minStart, minStart + minLen);
}
```

## Complexity

| Aspect | Value |
|--------|-------|
| Time | O(n + m) — each character visited at most twice (right expands, left contracts) |
| Space | O(k) — where k is the character set size (128 for ASCII) |

## Interview Tips

1. **This is HARD** — don't worry if it takes time. Start with brute force: "find all substrings and check."
2. **Explain the two phases** — "First expand until valid, then contract to minimize."
3. **`have` vs `need`** — explain carefully. `need` is distinct characters, `have` is how many distinct are satisfied.
4. **Know the array version** — for ASCII, arrays are faster than HashMaps.
5. **Edge cases**: t longer than s → "", s = t → exact match, single character match.

## Common Mistakes

1. **Not using `intValue()` for Integer comparison** — `Integer(1) == Integer(1)` can be false! Use `.intValue()` or `(int)` cast for != 127 comparisons.
2. **Counting `have` wrong** — increment when `have[c] == need[c]`, not when `have[c] <= need[c]`.
3. **Not updating `minStart`** — always update both `minLen` and `minStart`.
4. **Forgetting to handle the case where t has duplicate characters** — `t = "AABC"` needs `A:2` in the window.

## Variations

### Minimum Window Subsequence
Same idea but the window must preserve the *order* of characters (not just contain them). This is harder — uses a different DP approach.

### Minimum Window with At Most K Distinct Characters
Already covered in the "Longest K Unique Characters" problem but inverted.

## Summary

The Minimum Window Substring is the ultimate sliding window test. If you can solve this from scratch in an interview, you've mastered the pattern.

Remember the structure:
1. Build `needMap` from `t`
2. Expand `right`, update `have` count
3. When `have == need`, shrink from `left` and track minimum
4. Return the substring
