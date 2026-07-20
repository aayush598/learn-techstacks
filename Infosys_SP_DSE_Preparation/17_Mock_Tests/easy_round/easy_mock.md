# Easy Mock Test - 30 Minutes

> 2 Questions: 15 minutes each. Focus on speed and accuracy.

---

## Timer Guide

```
Total Time: 30 minutes
├── Q1: 15 minutes (5 min plan, 8 min code, 2 min test)
└── Q2: 15 minutes (5 min plan, 8 min code, 2 min test)
```

---

## Question 1: Maximum Subarray Sum (Kadane's Algorithm)

### Problem Statement

Given an array of integers, find the contiguous subarray (containing at least one number) which has the largest sum and return that sum.

**Input Format:**
- First line: N (number of elements)
- Second line: N space-separated integers

**Output Format:**
- Single integer: maximum subarray sum

**Constraints:**
- 1 ≤ N ≤ 10^5
- -10^4 ≤ arr[i] ≤ 10^4

### Sample Test Cases

```
Input:  N = 9
        arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6
Explanation: Subarray [4, -1, 2, 1] has sum = 6

Input:  N = 1
        arr = [1]
Output: 1

Input:  N = 5
        arr = [5, 4, -1, 7, 8]
Output: 23
Explanation: Entire array has sum = 23

Input:  N = 5
        arr = [-1, -2, -3, -4, -5]
Output: -1
Explanation: Maximum subarray is [-1]
```

### Solution 1: Kadane's Algorithm (Optimal)

```python
import sys
input = sys.stdin.readline

def max_subarray_sum(arr):
    max_sum = arr[0]
    current_sum = arr[0]

    for i in range(1, len(arr)):
        current_sum = max(arr[i], current_sum + arr[i])
        max_sum = max(max_sum, current_sum)

    return max_sum

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    print(max_subarray_sum(arr))

main()
```

### Solution 2: With Subarray Recovery

```python
import sys
input = sys.stdin.readline

def max_subarray_with_indices(arr):
    max_sum = arr[0]
    current_sum = arr[0]
    start = end = temp_start = 0

    for i in range(1, len(arr)):
        if arr[i] > current_sum + arr[i]:
            current_sum = arr[i]
            temp_start = i
        else:
            current_sum += arr[i]

        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i

    return max_sum, arr[start:end + 1]

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    result, subarray = max_subarray_with_indices(arr)
    print(f"Maximum Sum: {result}")
    print(f"Subarray: {subarray}")

main()
```

### Complexity Analysis
- **Time:** O(N) - Single pass through array
- **Space:** O(1) - Only two variables

### Key Points
- Kadane's algorithm is the standard approach
- Key insight: at each position, decide whether to extend current subarray or start new
- Handle all negative numbers case (result is max element)

---

## Question 2: Check if Two Strings are Anagrams

### Problem Statement

Given two strings, check if they are anagrams of each other. Two strings are anagrams if they contain the same characters with the same frequencies.

**Input Format:**
- First line: string s1
- Second line: string s2

**Output Format:**
- "True" if anagrams, "False" otherwise

**Constraints:**
- 1 ≤ |s1|, |s2| ≤ 10^5
- Strings contain only lowercase English letters

### Sample Test Cases

```
Input:  s1 = "listen"
        s2 = "silent"
Output: True

Input:  s1 = "hello"
        s2 = "bello"
Output: False

Input:  s1 = "anagram"
        s2 = "nagaram"
Output: True

Input:  s1 = "rat"
        s2 = "car"
Output: False

Input:  s1 = ""
        s2 = ""
Output: True
```

### Solution 1: Sorting Approach

```python
import sys
input = sys.stdin.readline

def are_anagrams_sort(s1, s2):
    if len(s1) != len(s2):
        return False
    return sorted(s1) == sorted(s2)

def main():
    s1 = input().strip()
    s2 = input().strip()
    print(are_anagrams_sort(s1, s2))

main()
```

### Solution 2: Character Counting (Optimal)

```python
import sys
from collections import Counter
input = sys.stdin.readline

def are_anagrams(s1, s2):
    if len(s1) != len(s2):
        return False

    count1 = Counter(s1)
    count2 = Counter(s2)

    return count1 == count2

def main():
    s1 = input().strip()
    s2 = input().strip()
    print(are_anagrams(s1, s2))

main()
```

### Solution 3: Manual Counting (No Extra Libraries)

```python
import sys
input = sys.stdin.readline

def are_anagrams_manual(s1, s2):
    if len(s1) != len(s2):
        return False

    count = [0] * 26

    for i in range(len(s1)):
        count[ord(s1[i]) - ord('a')] += 1
        count[ord(s2[i]) - ord('a')] -= 1

    for c in count:
        if c != 0:
            return False

    return True

def main():
    s1 = input().strip()
    s2 = input().strip()
    print(are_anagrams_manual(s1, s2))

main()
```

### Complexity Analysis
- **Solution 1:** O(N log N) time, O(N) space (sorting)
- **Solution 2:** O(N) time, O(1) space (26 letters)
- **Solution 3:** O(N) time, O(1) space (no imports)

### Key Points
- First check: lengths must be equal
- Sorting approach is simpler but slower
- Counting approach is optimal for interviews
- Edge cases: empty strings, single character, all same characters

---

## Quick Reference During Test

### Common Mistakes to Avoid
1. Forgetting to handle empty array/string
2. Integer overflow (not in Python but conceptually)
3. Off-by-one errors
4. Not reading input correctly
5. Forgetting to import modules

### Speed Tips
1. Use `sys.stdin.readline` instead of `input()`
2. Pre-compute when possible
3. Use built-in functions
4. Don't optimize prematurely
5. Test with edge cases quickly

### Post-Test Checklist
- [ ] Did I handle all edge cases?
- [ ] Is my solution optimal?
- [ ] Did I test with sample inputs?
- [ ] Is my code clean and readable?
- [ ] Did I explain the approach?
