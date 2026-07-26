# Medium Mock Test - 60 Minutes

> 2 Questions: 30 minutes each. Balance speed with optimal approach.

---

## Timer Guide

```
Total Time: 60 minutes
├── Q1: 30 minutes
│   ├── 5 min: Understand problem + plan
│   ├── 15 min: Implement solution
│   ├── 5 min: Test with edge cases
│   └── 5 min: Optimize if needed
└── Q2: 30 minutes
    ├── 5 min: Understand problem + plan
    ├── 15 min: Implement solution
    ├── 5 min: Test with edge cases
    └── 5 min: Optimize if needed
```

---

## Question 1: Longest Substring Without Repeating Characters

### Problem Statement

Given a string `s`, find the length of the longest substring without repeating characters.

**Input Format:**
- Single line: string s

**Output Format:**
- Single integer: length of longest substring

**Constraints:**
- 0 ≤ |s| ≤ 5 * 10^4
- s consists of English letters, digits, symbols, and spaces

### Sample Test Cases

```
Input:  "abcabcbb"
Output: 3
Explanation: The answer is "abc", with length 3

Input:  "bbbbb"
Output: 1
Explanation: The answer is "b", with length 1

Input:  "pwwkew"
Output: 3
Explanation: The answer is "wke", with length 3

Input:  ""
Output: 0

Input:  " "
Output: 1

Input:  "au"
Output: 2
```

### Step-by-Step Thinking Process

```
Brainstorming:
├── "Substring" = contiguous block of characters
├── "Without repeating" = all chars in window are unique
├── Need to find LONGEST such substring
├── Brute force: Check all O(N²) substrings × O(N) validity = O(N³) → Too slow
└── Key insight: Use SLIDING WINDOW to maintain a "valid" window

Pattern Recognition:
┌─────────────────────────────────────────────────────────────┐
│  SLIDING WINDOW = two pointers (left, right)               │
│                                                             │
│  1. Expand right pointer to include new character           │
│  2. If invalid (repeating char), shrink from left           │
│  3. Track maximum window size seen                          │
│                                                             │
│  When to use sliding window:                                │
│  ✓ Contiguous subarray/substring problems                   │
│  ✓ Finding min/max length satisfying a condition            │
│  ✓ "Longest substring" type questions                       │
└─────────────────────────────────────────────────────────────┘
```

### Visual Walkthrough: Sliding Window with Set

```
String: "abcabcbb"

left=0, right=0: window=[a]         max_len=1
  "a b c a b c b b"
   ^
   L

left=0, right=1: window=[a,b]       max_len=2
  "a b c a b c b b"
   ^ ^
   L R

left=0, right=2: window=[a,b,c]     max_len=3
  "a b c a b c b b"
   ^   ^
   L   R

left=0, right=3: 'a' already in set!
  ┌──────────────────────────────────────────────┐
  │ Shrink: remove s[left]='a', left++           │
  │ Then add s[right]='a'                        │
  │ New window: [b,c,a]                          │
  └──────────────────────────────────────────────┘
  "a b c a b c b b"
     ^   ^
     L   R                    max_len=3

left=1, right=4: 'b' already in set!
  Shrink: remove 'b', left++. Add 'b'.
  window=[c,a,b]             max_len=3
  "a b c a b c b b"
       ^   ^
       L   R

left=2, right=5: 'c' already in set!
  Shrink: remove 'c', left++. Add 'c'.
  window=[a,b,c]             max_len=3
  "a b c a b c b b"
         ^   ^
         L   R

left=2, right=6: 'b' already in set!
  Shrink until 'b' removed: remove 'a'(left=3), remove 'b'(left=4)
  window=[c,b]               max_len=3
  "a b c a b c b b"
             ^ ^
             L R

left=4, right=7: 'b' already in set!
  Shrink: remove 'c'(left=5), remove 'b'(left=6)
  window=[b]                 max_len=3
  "a b c a b c b b"
               ^ ^
               L R

FINAL: max_len = 3 (substring "abc")
```

### Solution 1: Sliding Window with Set

```python
import sys
input = sys.stdin.readline

def length_of_longest_substring(s):
    char_set = set()
    left = 0
    max_length = 0

    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1

        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)

    return max_length

def main():
    s = input().strip()
    print(length_of_longest_substring(s))

main()
```

### Solution 2: Sliding Window with Dict (Optimal)

```python
import sys
input = sys.stdin.readline

def length_of_longest_substring_optimized(s):
    char_index = {}
    max_length = 0
    left = 0

    for right in range(len(s)):
        if s[right] in char_index and char_index[s[right]] >= left:
            left = char_index[s[right]] + 1

        char_index[s[right]] = right
        max_length = max(max_length, right - left + 1)

    return max_length

def main():
    s = input().strip()
    print(length_of_longest_substring_optimized(s))

main()
```

### Solution 3: Array for ASCII Characters

```python
import sys
input = sys.stdin.readline

def length_of_longest_substring_array(s):
    last_seen = [-1] * 128
    left = 0
    max_length = 0

    for right in range(len(s)):
        if last_seen[ord(s[right])] >= left:
            left = last_seen[ord(s[right])] + 1

        last_seen[ord(s[right])] = right
        max_length = max(max_length, right - left + 1)

    return max_length

def main():
    s = input().strip()
    print(length_of_longest_substring_array(s))

main()
```

### Complexity Analysis
- **Solution 1:** O(2N) time, O(min(M, N)) space - each character visited at most twice
- **Solution 2:** O(N) time, O(min(M, N)) space - single pass
- **Solution 3:** O(N) time, O(1) space - fixed size array (128 ASCII)

Where N = string length, M = character set size

### Key Points
- Sliding window is the optimal pattern for substring problems
- The dictionary approach is most elegant
- Edge cases: empty string, single character, all unique, all same

---

## Question 2: Merge Intervals

### Problem Statement

Given a collection of intervals, merge all overlapping intervals.

**Input Format:**
- First line: N (number of intervals)
- Next N lines: start end (two integers per line)

**Output Format:**
- Merged intervals, one per line (start end)

**Constraints:**
- 1 ≤ N ≤ 10^4
- 0 ≤ start ≤ end ≤ 10^4

### Sample Test Cases

```
Input:  N = 4
        1 3
        2 6
        8 10
        15 18
Output:
    1 6
    8 10
    15 18
Explanation: Intervals [1,3] and [2,6] overlap, so merge to [1,6]

Input:  N = 2
        1 4
        4 5
Output:
    1 5
Explanation: Intervals [1,4] and [4,5] are adjacent, merge to [1,5]

Input:  N = 1
        1 4
Output:
    1 4

Input:  N = 3
        1 10
        2 3
        5 7
Output:
    1 10
Explanation: All intervals are within [1,10]
```

### Step-by-Step Thinking Process

```
Brainstorming:
├── "Merge overlapping intervals" → Classic interval problem
├── Key: When do two intervals overlap?
│   └── [a,b] and [c,d] overlap if c <= b (assuming sorted by start)
├── First step: SORT intervals by start time
├── Then iterate and merge greedily
└── Edge case: Adjacent intervals [1,4] and [4,5] → merge to [1,5]

Algorithm:
┌─────────────────────────────────────────────────────────────┐
│  1. Sort intervals by start time                            │
│  2. Initialize result with first interval                   │
│  3. For each remaining interval:                            │
│     ├── If it overlaps with last result interval:           │
│     │   └── Merge: extend end = max(end, new_end)           │
│     └── If no overlap:                                      │
│         └── Add as new interval to result                   │
└─────────────────────────────────────────────────────────────┘
```

### Visual Walkthrough: Merge Intervals

```
Input intervals: [[1,3], [2,6], [8,10], [15,18]]

Step 1: SORT by start time
  Before: [[1,3], [2,6], [8,10], [15,18]]
  After:  [[1,3], [2,6], [8,10], [15,18]]  (already sorted)

Step 2: Process intervals

  ┌─── Number Line Visualization ───────────────────────────────┐
  │                                                              │
  │  0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18  │
  │     [=====]                                                  │
  │        [==========]                                          │
  │                          [========]                          │
  │                                                [========]    │
  └──────────────────────────────────────────────────────────────┘

  Start: result = [[1,3]]

  Process [2,6]:
    Does [2,6] overlap with [1,3]?
    Check: 2 <= 3? YES → Merge!
    New interval: [1, max(3,6)] = [1,6]
    result = [[1,6]]

    ┌─── After merge ───────────────────────────────────────┐
    │  1  2  3  4  5  6                                     │
    │  [===============]  ← merged [1,6]                    │
    └───────────────────────────────────────────────────────┘

  Process [8,10]:
    Does [8,10] overlap with [1,6]?
    Check: 8 <= 6? NO → No overlap
    result = [[1,6], [8,10]]

  Process [15,18]:
    Does [15,18] overlap with [8,10]?
    Check: 15 <= 10? NO → No overlap
    result = [[1,6], [8,10], [15,18]]

FINAL OUTPUT:
  1 6
  8 10
  15 18
```

### Another Example: Adjacent Intervals

```
Input: [[1,4], [4,5]]

Step 1: Already sorted
Step 2: Process
  result = [[1,4]]

  Process [4,5]:
    Check: 4 <= 4? YES → Merge!
    New: [1, max(4,5)] = [1,5]

OUTPUT: [1,5]  ← Adjacent intervals are merged!
```

### Solution 1: Sort and Merge (Optimal)

```python
import sys
input = sys.stdin.readline

def merge_intervals(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged

def main():
    n = int(input())
    intervals = []
    for _ in range(n):
        start, end = map(int, input().split())
        intervals.append([start, end])

    result = merge_intervals(intervals)
    for interval in result:
        print(f"{interval[0]} {interval[1]}")

main()
```

### Solution 2: Sort and Merge (Alternative)

```python
import sys
input = sys.stdin.readline

def merge_intervals_alt(intervals):
    if not intervals:
        return []

    intervals.sort()
    result = []

    for interval in intervals:
        if not result or result[-1][1] < interval[0]:
            result.append(interval)
        else:
            result[-1][1] = max(result[-1][1], interval[1])

    return result

def main():
    n = int(input())
    intervals = [list(map(int, input().split())) for _ in range(n)]

    result = merge_intervals_alt(intervals)
    for start, end in result:
        print(f"{start} {end}")

main()
```

### Solution 3: With Interval Class

```python
import sys
input = sys.stdin.readline

class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

def merge_intervals_class(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda x: x.start)
    result = [intervals[0]]

    for current in intervals[1:]:
        if current.start <= result[-1].end:
            result[-1].end = max(result[-1].end, current.end)
        else:
            result.append(current)

    return result

def main():
    n = int(input())
    intervals = []
    for _ in range(n):
        start, end = map(int, input().split())
        intervals.append(Interval(start, end))

    result = merge_intervals_class(intervals)
    for interval in result:
        print(f"{interval.start} {interval.end}")

main()
```

### Complexity Analysis
- **Time:** O(N log N) - Sorting dominates
- **Space:** O(N) - For the result array

### Key Points
- Always sort by start time first
- Check overlap: current.start <= previous.end
- Handle edge cases: empty input, single interval
- Practice variant: Insert Interval

---

## Quick Reference During Test

### Common Patterns

```python
# Sliding Window Template
def sliding_window(s):
    left = 0
    window = {}
    result = 0

    for right in range(len(s)):
        # Add right element
        window[s[right]] = window.get(s[right], 0) + 1

        # Shrink window if needed
        while window_needs_shrink:
            window[s[left]] -= 1
            left += 1

        # Update result
        result = max(result, right - left + 1)

    return result

# Merge Intervals Template
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged
```

### Edge Cases to Always Test

```
Sliding Window:
├── Empty string → 0
├── Single character → 1
├── All same characters → 1
├── All unique characters → N (entire string)
├── String with spaces → spaces count as characters
└── Very long string → ensure O(N) solution

Merge Intervals:
├── Empty input → return []
├── Single interval → return as-is
├── No overlapping intervals → return all
├── All overlapping → merge into one
├── Adjacent intervals [1,4][4,5] → should merge
└── Nested intervals [1,10][2,3] → outer absorbs inner
```

### Common Mistakes to Avoid

```
Sliding Window:
├── Using while loop to remove chars one-by-one instead of jumping
│   └── Solution 2 (dict approach) jumps directly → O(N) vs O(2N)
├── Forgetting that characters can be spaces/symbols (use 128 ASCII)
├── Not updating the left pointer when duplicate found
└── Confusing "substring" (contiguous) with "subsequence" (not contiguous)

Merge Intervals:
├── Not sorting first → wrong results!
├── Using < instead of <= for overlap check
│   └── [1,4] and [4,5] should merge (use <=)
├── Forgetting to handle empty input
├── Not using max() when merging ends → might shrink interval
└── Confusing "merge" with "insert interval"
```

### Speed Tips for Medium Round

```
Time Budget: 30 minutes per question
├── 0-5 min:  Read, identify pattern, plan approach
├── 5-20 min: Write solution
├── 20-25 min: Test with given samples
├── 25-28 min: Test edge cases
└── 28-30 min: Optimize if needed

Pattern Recognition Cheat Sheet:
├── "Longest substring without repeating" → SLIDING WINDOW
├── "Merge intervals" → SORT + MERGE
├── "Minimum window containing..." → SLIDING WINDOW
├── "Insert interval" → SORT + MERGE + INSERT
└── When stuck: draw the array/string and trace through manually!
```

### Post-Test Checklist
- [ ] Did I handle all edge cases?
- [ ] Is my solution optimal?
- [ ] Did I test with sample inputs?
- [ ] Did I test with edge cases?
- [ ] Is my code clean and readable?
- [ ] Did I sort intervals before merging?
- [ ] Is my sliding window O(N) not O(N²)?
