# Longest Substring Without Repeating Characters

This is the most classic variable-size sliding window problem. It appears in interviews constantly — Google, Amazon, Microsoft, Facebook, you name it.

## Problem Statement

Given a string, find the length of the longest substring without repeating characters.

```
Input:  "abcabcbb"
Output: 3
Explanation: "abc" is the longest substring without repeats

Input:  "bbbbb"
Output: 1
Explanation: "b" is the longest

Input:  "pwwkew"
Output: 3
Explanation: "wke" (not "pwke" which is a subsequence, not substring)
```

## Brute Force (O(n²))

Check every substring, verify no duplicates.

```java
public int lengthOfLongestSubstringBrute(String s) {
    int n = s.length();
    int maxLen = 0;

    for (int i = 0; i < n; i++) {
        Set<Character> seen = new HashSet<>();
        for (int j = i; j < n; j++) {
            if (seen.contains(s.charAt(j))) break;
            seen.add(s.charAt(j));
            maxLen = Math.max(maxLen, j - i + 1);
        }
    }

    return maxLen;
}
```

O(n²) — we can do much better.

## Sliding Window with HashMap (O(n))

The key insight: when we find a repeating character, we don't need to reset to `i+1`. We can jump `left` directly past the previous occurrence.

```java
public int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> lastSeen = new HashMap<>();
    int left = 0;
    int maxLen = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);

        // If character was seen and is within current window
        if (lastSeen.containsKey(c)) {
            // Move left to one past the previous occurrence
            left = Math.max(left, lastSeen.get(c) + 1);
        }

        // Update last seen position
        lastSeen.put(c, right);

        // Update max length
        maxLen = Math.max(maxLen, right - left + 1);
    }

    return maxLen;
}
```

### Why `Math.max(left, lastSeen.get(c) + 1)`?

This is important! Consider `"abba"`:

```
i=0 'a': lastSeen={a:0}, window=[0,0], len=1, max=1
i=1 'b': lastSeen={a:0, b:1}, window=[0,1], len=2, max=2
i=2 'b': lastSeen has 'b' at 1, newLeft = max(0, 2) = 2, window=[2,2], len=1, max=2
i=3 'a': lastSeen has 'a' at 0, BUT left=2, newLeft = max(2, 1) = 2
         window=[2,3], len=2, max=2
         
Result: 2 ("ba" or "ab") ✓
```

Without `Math.max`, when we get to `'a'` at index 3, we'd set `left = 0 + 1 = 1`, which moves `left` *backward* — making the window `[1, 3]` = "bba" which has a duplicate 'b'. The `Math.max` prevents this.

### Dry Run

```
s = "abcabcbb"

right=0, c='a': not in map, map={a:0}, window=[0,0], len=1, max=1
right=1, c='b': not in map, map={a:0,b:1}, window=[0,1], len=2, max=2
right=2, c='c': not in map, map={a:0,b:1,c:2}, window=[0,2], len=3, max=3
right=3, c='a': in map at 0, left=max(0,1)=1, map={a:3,b:1,c:2}, window=[1,3], len=3, max=3
right=4, c='b': in map at 1, left=max(1,2)=2, map={a:3,b:4,c:2}, window=[2,4], len=3, max=3
right=5, c='c': in map at 2, left=max(2,3)=3, map={a:3,b:4,c:5}, window=[3,5], len=3, max=3
right=6, c='b': in map at 4, left=max(3,5)=5, map={a:3,b:6,c:5}, window=[5,6], len=2, max=3
right=7, c='b': in map at 6, left=max(5,7)=7, map={a:3,b:7,c:5}, window=[7,7], len=1, max=3

Result: 3 ✓
```

## Sliding Window with HashSet (Alternative)

```java
public int lengthOfLongestSubstringHashSet(String s) {
    Set<Character> window = new HashSet<>();
    int left = 0;
    int maxLen = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);

        // Shrink window until no duplicate
        while (window.contains(c)) {
            window.remove(s.charAt(left));
            left++;
        }

        window.add(c);
        maxLen = Math.max(maxLen, right - left + 1);
    }

    return maxLen;
}
```

This uses a `Set` instead of a `Map`. The `while` loop incrementally removes characters from the left until the duplicate is gone. It's simpler but slightly less efficient in practice (multiple removals vs one jump).

### HashMap vs HashSet

| HashMap | HashSet |
|---------|---------|
| `left` jumps directly past previous occurrence | `left` increments one by one |
| Needs `Math.max` to prevent going backward | No such issue |
| O(n) — each operation is O(1) | O(n) — but may do more operations |
| Slightly more complex | Simpler to understand |

Both are O(n). Pick the one you're more comfortable explaining.

## ASCII Optimization (O(n), O(128))

If the character set is known (ASCII):

```java
public int lengthOfLongestSubstringASCII(String s) {
    int[] lastSeen = new int[128]; // ASCII has 128 characters
    Arrays.fill(lastSeen, -1);

    int left = 0;
    int maxLen = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);

        if (lastSeen[c] >= left) {
            left = lastSeen[c] + 1;
        }

        lastSeen[c] = right;
        maxLen = Math.max(maxLen, right - left + 1);
    }

    return maxLen;
}
```

No HashMap overhead — just an array of size 128.

## Dry Run for "bbbbb"

```
s = "bbbbb"

HashMap version:
right=0, c='b': not in map, map={b:0}, window=[0,0], len=1, max=1
right=1, c='b': in map at 0, left=max(0,1)=1, map={b:1}, window=[1,1], len=1, max=1
right=2, c='b': in map at 1, left=max(1,2)=2, map={b:2}, window=[2,2], len=1, max=1
...all same...

Result: 1 ✓
```

## Dry Run for "pwwkew"

```
s = "pwwkew"

right=0, c='p': not in map, map={p:0}, window=[0,0], len=1, max=1
right=1, c='w': not in map, map={p:0,w:1}, window=[0,1], len=2, max=2
right=2, c='w': in map at 1, left=max(0,2)=2, map={p:0,w:2}, window=[2,2], len=1, max=2
right=3, c='k': not in map, map={p:0,w:2,k:3}, window=[2,3], len=2, max=2
right=4, c='e': not in map, map={p:0,w:2,k:3,e:4}, window=[2,4], len=3, max=3
right=5, c='w': in map at 2, left=max(2,3)=3, map={p:0,w:5,k:3,e:4}, window=[3,5], len=3, max=3

Result: 3 ✓ (substring "wke" or "kew")
```

## Complexity

| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(min(n, m)) |
| HashMap | O(n) | O(min(n, m)) |
| HashSet | O(n) | O(min(n, m)) |
| ASCII Array | O(n) | O(128) = O(1) |

Where `m` is the size of the character set.

## Edge Cases

```java
// Empty string → 0
lengthOfLongestSubstring("") → 0

// Single character → 1
lengthOfLongestSubstring("a") → 1

// All unique → n
lengthOfLongestSubstring("abcdef") → 6

// All same → 1
lengthOfLongestSubstring("aaa") → 1

// With spaces
lengthOfLongestSubstring("ab c de") → 6 (spaces are characters too)
```

## Interview Tips

1. **Start with brute force** — "check every substring" is the baseline
2. **Introduce the sliding window** — "we can maintain a window of non-repeating characters"
3. **Explain the `Math.max`** trick — prevents left from going backward
4. **Mention the ASCII optimization** — shows you care about performance
5. **Trace through examples** — "abba" and "pwwkew" are good test cases

## Common Mistakes

1. **Not using `Math.max`** on the left update — causes left to go backward
2. **Off-by-one on left position** — left should be `previous + 1`, not `previous`
3. **Using `Map<Character, Boolean>`** instead of storing indices — you need the position to jump
4. **Forgetting to update the map** after finding a duplicate — always update `lastSeen` to the current index

This is the quintessential sliding window problem. If you understand this one, you understand 80% of variable-size sliding window.
