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

### Edge Cases to Test
- Empty string/array
- Single element
- All elements same
- No overlapping intervals
- All intervals overlap

### Time Management Tips
1. Don't spend more than 5 minutes planning
2. Code the solution quickly
3. Test with given examples first
4. Then test edge cases
5. Optimize only if time permits

### Post-Test Checklist
- [ ] Did I handle all edge cases?
- [ ] Is my solution optimal?
- [ ] Did I test with sample inputs?
- [ ] Did I test with edge cases?
- [ ] Is my code clean and readable?
