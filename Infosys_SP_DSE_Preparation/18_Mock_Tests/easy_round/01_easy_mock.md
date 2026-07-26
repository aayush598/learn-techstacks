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

### Step-by-Step Thinking Process

```
Brainstorming:
├── What is a subarray? → A CONTIGUOUS block of elements
├── Can all elements be negative? → YES! Result is the least negative
├── Brute force? → Check all O(N²) subarrays → Too slow for N=10^5
└── Key insight: At each position, should I EXTEND the current subarray or START NEW?

Decision at each element arr[i]:
┌─────────────────────────────────────────────────────────┐
│  Should I include arr[i] in current subarray?           │
│                                                         │
│  If current_sum + arr[i] > arr[i]:                      │
│      → EXTEND (current_sum = current_sum + arr[i])      │
│  Else:                                                  │
│      → START NEW (current_sum = arr[i])                 │
└─────────────────────────────────────────────────────────┘
```

### Visual Walkthrough: Kadane's Algorithm

```
Array: [-2, 1, -3, 4, -1, 2, 1, -5, 4]

Step-by-step processing:
═══════════════════════════════════════════════════════════════

Index 0: arr[0] = -2
  current_sum = -2 (initialize)
  max_sum     = -2
  ┌──────────────────────────────────┐
  │ [-2] ← current subarray         │
  │  ▲                               │
  │  max_sum = -2                    │
  └──────────────────────────────────┘

Index 1: arr[1] = 1
  Decision: max(1, -2 + 1) = max(1, -1) = 1 → START NEW
  current_sum = 1
  max_sum     = max(-2, 1) = 1
  ┌──────────────────────────────────┐
  │ [-2] [1] ← new subarray starts  │
  │        ▲                         │
  │        max_sum = 1               │
  └──────────────────────────────────┘

Index 2: arr[2] = -3
  Decision: max(-3, 1 + (-3)) = max(-3, -2) = -2 → EXTEND
  current_sum = -2
  max_sum     = max(1, -2) = 1
  ┌──────────────────────────────────┐
  │        [1, -3] ← extending      │
  │  max_sum = 1 (unchanged)        │
  └──────────────────────────────────┘

Index 3: arr[3] = 4
  Decision: max(4, -2 + 4) = max(4, 2) = 4 → START NEW
  current_sum = 4
  max_sum     = max(1, 4) = 4
  ┌──────────────────────────────────┐
  │              [4] ← new start!    │
  │              ▲                   │
  │              max_sum = 4         │
  └──────────────────────────────────┘

Index 4: arr[4] = -1
  Decision: max(-1, 4 + (-1)) = max(-1, 3) = 3 → EXTEND
  current_sum = 3
  max_sum     = max(4, 3) = 4
  ┌──────────────────────────────────┐
  │              [4, -1]             │
  │  max_sum = 4 (unchanged)        │
  └──────────────────────────────────┘

Index 5: arr[5] = 2
  Decision: max(2, 3 + 2) = max(2, 5) = 5 → EXTEND
  current_sum = 5
  max_sum     = max(4, 5) = 5
  ┌──────────────────────────────────┐
  │              [4, -1, 2]          │
  │              ▲                   │
  │              max_sum = 5         │
  └──────────────────────────────────┘

Index 6: arr[6] = 1
  Decision: max(1, 5 + 1) = max(1, 6) = 6 → EXTEND
  current_sum = 6
  max_sum     = max(5, 6) = 6  ★ NEW MAX!
  ┌──────────────────────────────────┐
  │              [4, -1, 2, 1]       │
  │              ▲                   │
  │              max_sum = 6 ★       │
  └──────────────────────────────────┘

Index 7: arr[7] = -5
  Decision: max(-5, 6 + (-5)) = max(-5, 1) = 1 → EXTEND
  current_sum = 1
  max_sum     = 6 (unchanged)
  ┌──────────────────────────────────┐
  │              [4,-1,2,1,-5]       │
  │  max_sum = 6 (unchanged)        │
  └──────────────────────────────────┘

Index 8: arr[8] = 4
  Decision: max(4, 1 + 4) = max(4, 5) = 5 → EXTEND
  current_sum = 5
  max_sum     = 6 (unchanged)
  ┌──────────────────────────────────┐
  │           [4,-1,2,1,-5,4]        │
  │  max_sum = 6 (final answer)     │
  └──────────────────────────────────┘

FINAL ANSWER: max_sum = 6
Best subarray: [4, -1, 2, 1] (indices 3 to 6)
```

### All Negative Numbers Example

```
Array: [-1, -2, -3, -4, -5]

Index 0: current = -1, max = -1
Index 1: max(-2, -1+(-2)) = -2 → start new. max = max(-1,-2) = -1
Index 2: max(-3, -2+(-3)) = -3 → start new. max = max(-1,-3) = -1
Index 3: max(-4, -3+(-4)) = -4 → start new. max = max(-1,-4) = -1
Index 4: max(-5, -4+(-5)) = -5 → start new. max = max(-1,-5) = -1

ANSWER: -1 (the least negative element)
KEY: Even when all negative, algorithm correctly picks the maximum single element
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

### Step-by-Step Thinking Process

```
Brainstorming:
├── What is an anagram? → Same characters, same frequencies, different order
├── "listen" and "silent" → Both have: l=1, i=1, s=1, t=1, e=1, n=1 ✓
├── Quick check first: lengths must be equal!
└── Two main approaches: Sort or Count

Approach Comparison:
┌──────────────────┬───────────────┬──────────────┐
│ Approach         │ Time          │ Space        │
├──────────────────┼───────────────┼──────────────┤
│ Sorting          │ O(N log N)    │ O(N)         │
│ Counter (dict)   │ O(N)          │ O(1)*        │
│ Array counting   │ O(N)          │ O(1)         │
└──────────────────┴───────────────┴──────────────┘
* O(1) because only 26 lowercase letters
```

### Visual Walkthrough: Character Counting Approach

```
s1 = "listen"    s2 = "silent"

Step 1: Check lengths → 6 == 6 ✓

Step 2: Build frequency difference array (count[26])

Processing s1="listen" (INCREMENT):
  l → count[11] += 1  →  1
  i → count[8]  += 1  →  1
  s → count[18] += 1  →  1
  t → count[19] += 1  →  1
  e → count[4]  += 1  →  1
  n → count[13] += 1  →  1

Processing s2="silent" (DECREMENT):
  s → count[18] -= 1  →  0  ✓
  i → count[8]  -= 1  →  0  ✓
  l → count[11] -= 1  →  0  ✓
  e → count[4]  -= 1  →  0  ✓
  n → count[13] -= 1  →  0  ✓
  t → count[19] -= 1  →  0  ✓

Final count array: all zeros → ANAGRAMS ✓

═══════════════════════════════════════

Counter-example: s1="hello" s2="bello"

Processing:
  h → count[7]  += 1  →  1
  e → count[4]  += 1  →  1
  l → count[11] += 1  →  2
  l → count[11] += 1  →  3
  o → count[14] += 1  →  1

  b → count[1]  -= 1  → -1  ← NON-ZERO!
  e → count[4]  -= 1  →  0
  l → count[11] -= 1  →  2
  l → count[11] -= 1  →  1
  o → count[14] -= 1  →  0

Count array has non-zero entries → NOT ANAGRAMS ✓
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

### Edge Cases to Always Test

```
Kadane's Algorithm:
├── All negative numbers → Answer is max element (not 0!)
├── Single element → Answer is that element
├── All positive → Answer is sum of entire array
├── Mixed with large negatives → Subarray might be very short
└── Maximum integer boundaries → Watch for overflow in C++/Java

Anagram Check:
├── Empty strings → True (both empty)
├── Different lengths → False (check first!)
├── Same character repeated → "aaa" vs "aaa" → True
├── Single character → "a" vs "a" → True, "a" vs "b" → False
└── All same characters → "aaaa" vs "aaaa" → True
```

### Common Mistakes to Avoid

```
MISTAKE 1: Forgetting the all-negative case in Kadane's
├── Wrong: initializing max_sum = 0
├── Right: initializing max_sum = arr[0]
└── Why: If all negative, max_sum should be the largest (least negative)

MISTAKE 2: Not checking length first in anagram
├── Wrong: counting characters without length check
├── Right: if len(s1) != len(s2): return False
└── Why: Saves unnecessary computation and avoids errors

MISTAKE 3: Off-by-one in Kadane's loop
├── Wrong: starting loop from i=0 (already initialized with arr[0])
├── Right: starting loop from i=1
└── Why: current_sum already set to arr[0]

MISTAKE 4: Using == on sorted lists in Python
├── Note: sorted() returns a list, and list comparison is element-wise
├── This is fine in Python but be aware
└── Alternative: use Counter for O(N) approach
```

### Speed Tips for Easy Round

```
Time Budget: 15 minutes per question
├── 0-3 min:  Read problem, identify pattern
├── 3-10 min: Write solution
├── 10-13 min: Test with sample inputs
└── 13-15 min: Test edge cases, submit

Quick Wins:
1. Use sys.stdin.readline for faster input
2. Know Kadane's by heart (one-liner logic)
3. Know Counter(s1) == Counter(s2) for anagrams
4. Always check edge cases BEFORE writing full solution
5. If stuck, start with brute force, then optimize
```

### Post-Test Checklist
- [ ] Did I handle all edge cases?
- [ ] Is my solution optimal?
- [ ] Did I test with sample inputs?
- [ ] Is my code clean and readable?
- [ ] Did I explain the approach?
- [ ] Did I check for all-negative array (Kadane)?
- [ ] Did I check string lengths first (Anagram)?
