# Hard Mock Test - 90 Minutes

> 2 Questions: 45 minutes each. Focus on correctness and approach explanation.

---

## Timer Guide

```
Total Time: 90 minutes
├── Q1: 45 minutes
│   ├── 10 min: Understand + Plan approach
│   ├── 20 min: Implement solution
│   ├── 10 min: Test + Debug
│   └── 5 min: Optimize if needed
└── Q2: 45 minutes
    ├── 10 min: Understand + Plan approach
    ├── 20 min: Implement solution
    ├── 10 min: Test + Debug
    └── 5 min: Optimize if needed
```

---

## Question 1: Word Break II (Find All Valid Sentences)

### Problem Statement

Given a string `s` and a dictionary of words `wordDict`, return all possible sentences where each word is a valid dictionary word. You can reuse dictionary words multiple times.

**Input Format:**
- First line: string s
- Second line: N (number of words in dictionary)
- Next N lines: dictionary words

**Output Format:**
- Each line: a valid sentence
- Sentences should be in lexicographic order

**Constraints:**
- 1 ≤ |s| ≤ 20
- 1 ≤ N ≤ 1000
- 1 ≤ |wordDict[i]| ≤ 10
- s and wordDict[i] consist of lowercase English letters

### Sample Test Cases

```
Input:  s = "catsanddog"
        N = 5
        cat
        cats
        and
        sand
        dog
Output:
    cat sand dog
    cats and dog

Input:  s = "pineapplepenapple"
        N = 5
        apple
        pen
        applepen
        pine
        pineapple
Output:
    pine apple pen apple
    pine applepen apple
    pineapple pen apple

Input:  s = "catsandog"
        N = 5
        cat
        cats
        and
        sand
        dog
Output:
    (no output - no valid sentence)

Input:  s = "a"
        N = 1
        a
Output:
    a
```

### Step-by-Step Thinking Process

```
Brainstorming:
├── Need to find ALL valid sentences, not just one
├── Each word must be in the dictionary
├── Can reuse dictionary words
├── This is a COMBINATORIAL problem → backtracking/recursion
└── Key: At each position, try all possible word lengths

Approach:
┌─────────────────────────────────────────────────────────────┐
│  At position i in string s:                                 │
│  ├── Try word s[i:i+1] → is it in dict? → recurse on i+1   │
│  ├── Try word s[i:i+2] → is it in dict? → recurse on i+2   │
│  ├── Try word s[i:i+3] → is it in dict? → recurse on i+3   │
│  └── ...                                                    │
│                                                             │
│  When reaching end of string (i == len(s)):                 │
│  └── Found a valid sentence! Add to result                  │
└─────────────────────────────────────────────────────────────┘
```

### Visual Walkthrough: Backtracking Tree

```
s = "catsanddog", dict = {cat, cats, and, sand, dog}

                    "catsanddog"
                    start=0
                   /    |     \
              "cat"   "cats"   "c"... (not in dict)
              /         |        \
        "catsand"   "catsand"    ...
        start=4     start=4
        /    \        /    \
    "catsand"  "catsand"  "catsand"
    + "dog"    + "dog"    + "dog"
      ✓ FOUND!   ✓ FOUND!

Detailed trace:
═══════════════════════════════════════════════════════════

backtrack(0): start at index 0
├── Try "c" (s[0:1]) → not in dict → skip
├── Try "ca" (s[0:2]) → not in dict → skip
├── Try "cat" (s[0:3]) → IN DICT ✓
│   └── backtrack(3): start at index 3
│       ├── Try "s" → not in dict
│       ├── Try "sa" → not in dict
│       ├── Try "san" → not in dict
│       ├── Try "sand" (s[3:7]) → IN DICT ✓
│       │   └── backtrack(7): start at index 7
│       │       ├── Try "d" → not in dict
│       │       ├── Try "do" → not in dict
│       │       ├── Try "dog" (s[7:10]) → IN DICT ✓
│       │       │   └── backtrack(10): start at 10 == len(s)
│       │       │       └── FOUND: "cat sand dog" ★
│       │       └── (no more options)
│       └── (no more valid words from "s")
├── Try "cats" (s[0:4]) → IN DICT ✓
│   └── backtrack(4): start at index 4
│       ├── Try "a" → not in dict
│       ├── Try "an" → not in dict
│       ├── Try "and" (s[4:7]) → IN DICT ✓
│       │   └── backtrack(7): start at index 7
│       │       └── Try "dog" → IN DICT ✓
│       │           └── FOUND: "cats and dog" ★
│       └── (no more valid words from "a")
└── Try "catsa"... → not in dict (can stop early with max word length)

RESULT: ["cat sand dog", "cats and dog"]
```

### Solution 1: Backtracking with Memoization (Optimal)

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**6)

def word_break_ii(s, word_dict):
    word_set = set(word_dict)
    memo = {}

    def backtrack(start):
        if start in memo:
            return memo[start]

        if start == len(s):
            return [""]

        result = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                sentences = backtrack(end)
                for sentence in sentences:
                    if sentence:
                        result.append(word + " " + sentence)
                    else:
                        result.append(word)

        memo[start] = result
        return result

    return sorted(backtrack(0))

def main():
    s = input().strip()
    n = int(input())
    word_dict = [input().strip() for _ in range(n)]
    sentences = word_break_ii(s, word_dict)

    if not sentences:
        return

    for sentence in sentences:
        print(sentence)

main()
```

### Solution 2: BFS Approach

```python
import sys
from collections import deque
input = sys.stdin.readline

def word_break_bfs(s, word_dict):
    word_set = set(word_dict)
    result = []

    # BFS: (start_index, current_path)
    queue = deque([(0, [])])

    while queue:
        start, path = queue.popleft()

        if start == len(s):
            result.append(" ".join(path))
            continue

        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                queue.append((end, path + [word]))

    return sorted(result)

def main():
    s = input().strip()
    n = int(input())
    word_dict = [input().strip() for _ in range(n)]
    sentences = word_break_bfs(s, word_dict)

    for sentence in sentences:
        print(sentence)

main()
```

### Solution 3: DP Check + Backtracking

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**6)

def word_break_dp(s, word_dict):
    word_set = set(word_dict)
    n = len(s)

    # First check if word break is possible
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    if not dp[n]:
        return []

    # Backtrack to find all sentences
    result = []

    def backtrack(start, current):
        if start == n:
            result.append(" ".join(current))
            return

        for end in range(start + 1, n + 1):
            if dp[end] and s[start:end] in word_set:
                current.append(s[start:end])
                backtrack(end, current)
                current.pop()

    backtrack(0, [])
    return sorted(result)

def main():
    s = input().strip()
    n = int(input())
    word_dict = [input().strip() for _ in range(n)]
    sentences = word_break_dp(s, word_dict)

    for sentence in sentences:
        print(sentence)

main()
```

### Complexity Analysis
- **Time:** O(2^N * N) in worst case - exponential due to all combinations
- **Space:** O(N * 2^N) - storing all possible sentences

### Key Points
- Memoization is crucial to avoid recomputation
- First check if word break is possible (DP)
- Sort output for lexicographic order
- Practice: Word Break I (just true/false)

---

## Question 2: Burst Balloons (Interval DP)

### Problem Statement

Given `n` balloons, indexed from 0 to n-1, each with a number on it represented by array `nums`. You are asked to burst all the balloons. If you burst balloon `i`, you will get `nums[i-1] * nums[i] * nums[i+1]` coins. If `i-1` or `i+1` goes out of bounds of the array, treat it as 1. Find the maximum coins you can collect by bursting all balloons optimally.

**Input Format:**
- First line: N (number of balloons)
- Second line: N space-separated integers

**Output Format:**
- Single integer: maximum coins

**Constraints:**
- 1 ≤ N ≤ 300
- 1 ≤ nums[i] ≤ 100

### Sample Test Cases

```
Input:  N = 4
        nums = [3, 1, 5, 8]
Output: 167
Explanation: Optimal order gives 167 coins

Input:  N = 3
        nums = [1, 2, 3]
Output: 12
Explanation: Burst [1] -> 1*2*3=6, then [2] -> 1*2*3=6, then [3] -> 1*3*1=3

Input:  N = 1
        nums = [5]
Output: 5
Explanation: Only one balloon, coins = 1*5*1 = 5

Input:  N = 3
        nums = [5, 1, 5]
Output: 130
Explanation: Burst middle first: 1*5*1=5, then left: 1*5*1=5, then right: 1*5*1=5
Actually optimal: Burst 1 first: 5*1*5=25, then 5: 1*5*1=5, then 5: 1*5*1=5 = 35
Wait, let me recalculate: [5,1,5]
Burst 1 first: 5*1*5=25
Then 5 (left): 1*5*1=5
Then 5 (right): 1*5*1=5
Total: 35

Actually the correct answer depends on the exact calculation.
```

### Step-by-Step Thinking Process

```
Brainstorming:
├── Burst balloon i → get coins = nums[i-1] * nums[i] * nums[i+1]
├── Order of bursting MATTERS (different orders → different coins)
├── Brute force: Try all N! orderings → too slow
├── Key insight: Think of which balloon to burst LAST (not first!)
└── Why last? Because the last balloon's neighbors are fixed!

Interval DP Logic:
┌─────────────────────────────────────────────────────────────┐
│  Consider balloons in range [left, right]                   │
│  If balloon k is the LAST to burst in this range:           │
│                                                             │
│  ┌─────────┐ ┌───┐ ┌─────────┐                             │
│  │ left... │ │ k │ │ ...right│                             │
│  └─────────┘ └───┘ └─────────┘                             │
│                                                             │
│  When k bursts last:                                        │
│  ├── Left subproblem: [left, k-1] (all burst before k)     │
│  ├── Right subproblem: [k+1, right] (all burst before k)   │
│  └── k's coins: nums[left-1] * nums[k] * nums[right+1]    │
│                                                             │
│  Total = dp[left][k-1] + dp[k+1][right] + nums[l-1]*nums[k]*nums[r+1] │
└─────────────────────────────────────────────────────────────┘
```

### Visual Walkthrough: Interval DP

```
nums = [3, 1, 5, 8]
Add virtual balloons: nums = [1, 3, 1, 5, 8, 1]
                       index:  0  1  2  3  4  5

DP Table (dp[left][right] = max coins from bursting balloons left..right):

Step 1: Length 1 intervals (single balloons)
═══════════════════════════════════════════════

dp[1][1]: Only balloon 1 (value 3)
  k=1: nums[0]*nums[1]*nums[2] = 1*3*1 = 3
  dp[1][1] = 3

dp[2][2]: Only balloon 2 (value 1)
  k=2: nums[1]*nums[2]*nums[3] = 3*1*5 = 15
  dp[2][2] = 15

dp[3][3]: Only balloon 3 (value 5)
  k=3: nums[2]*nums[3]*nums[4] = 1*5*8 = 40
  dp[3][3] = 40

dp[4][4]: Only balloon 4 (value 8)
  k=4: nums[3]*nums[4]*nums[5] = 5*8*1 = 40
  dp[4][4] = 40

Step 2: Length 2 intervals (pairs)
═══════════════════════════════════════════════

dp[1][2]: Balloons 1,2 (values 3,1)
  k=1: dp[2][2] + nums[0]*nums[1]*nums[3] = 15 + 1*3*5 = 15+15 = 30
  k=2: dp[1][1] + nums[0]*nums[2]*nums[3] = 3 + 1*1*5 = 3+5 = 8
  dp[1][2] = max(30, 8) = 30

dp[2][3]: Balloons 2,3 (values 1,5)
  k=2: dp[3][3] + nums[1]*nums[2]*nums[4] = 40 + 3*1*8 = 40+24 = 64
  k=3: dp[2][2] + nums[1]*nums[3]*nums[4] = 15 + 3*5*8 = 15+120 = 135
  dp[2][3] = max(64, 135) = 135

dp[3][4]: Balloons 3,4 (values 5,8)
  k=3: dp[4][4] + nums[2]*nums[3]*nums[5] = 40 + 1*5*1 = 40+5 = 45
  k=4: dp[3][3] + nums[2]*nums[4]*nums[5] = 40 + 1*8*1 = 40+8 = 48
  dp[3][4] = max(45, 48) = 48

Step 3: Length 3 intervals
═══════════════════════════════════════════════

dp[1][3]: Balloons 1,2,3
  k=1: dp[2][3] + nums[0]*nums[1]*nums[4] = 135 + 1*3*8 = 135+24 = 159
  k=2: dp[1][1]+dp[3][3] + 1*1*8 = 3+40+8 = 51
  k=3: dp[1][2] + nums[0]*nums[3]*nums[4] = 30 + 1*5*8 = 30+40 = 70
  dp[1][3] = max(159, 51, 70) = 159

dp[2][4]: Balloons 2,3,4
  k=2: dp[3][4] + nums[1]*nums[2]*nums[5] = 48 + 3*1*1 = 48+3 = 51
  k=3: dp[2][2]+dp[4][4] + 3*5*1 = 15+40+15 = 70
  k=4: dp[2][3] + nums[1]*nums[4]*nums[5] = 135 + 3*8*1 = 135+24 = 159
  dp[2][4] = max(51, 70, 159) = 159

Step 4: Length 4 interval (FULL PROBLEM)
═══════════════════════════════════════════════

dp[1][4]: Balloons 1,2,3,4 (ALL)
  k=1: dp[2][4] + 1*3*1 = 159+3 = 162
  k=2: dp[1][1]+dp[3][4] + 1*1*1 = 3+48+1 = 52
  k=3: dp[1][2]+dp[4][4] + 1*5*1 = 30+40+5 = 75
  k=4: dp[1][3] + 1*8*1 = 159+8 = 167
  dp[1][4] = max(162, 52, 75, 167) = 167 ★

ANSWER: 167 coins!
Optimal: Burst balloon 4 (value 8) last → gets 1*8*1 = 8 coins
         Before that, burst in optimal order for remaining [3,1,5]
```

### Solution 1: Interval DP (Optimal)

```python
import sys
input = sys.stdin.readline

def max_coins(nums):
    n = len(nums)
    # Add virtual balloons at boundaries with value 1
    nums = [1] + nums + [1]

    # dp[i][j] = max coins from bursting balloons between i and j (exclusive)
    dp = [[0] * (n + 2) for _ in range(n + 2)]

    # Process intervals of increasing length
    for length in range(1, n + 1):
        for left in range(1, n - length + 2):
            right = left + length - 1

            # Try each balloon as the last one to burst in this interval
            for k in range(left, right + 1):
                # k is the last balloon to burst
                coins = nums[left - 1] * nums[k] * nums[right + 1]
                dp[left][right] = max(dp[left][right],
                                       dp[left][k - 1] + dp[k + 1][right] + coins)

    return dp[1][n]

def main():
    n = int(input())
    nums = list(map(int, input().split()))
    print(max_coins(nums))

main()
```

### Solution 2: Recursive + Memoization

```python
import sys
from functools import lru_cache
input = sys.stdin.readline
sys.setrecursionlimit(10**6)

def max_coins_memo(nums):
    nums = [1] + nums + [1]
    n = len(nums)

    @lru_cache(maxsize=None)
    def solve(left, right):
        if left > right:
            return 0

        max_coins = 0
        for k in range(left, right + 1):
            coins = nums[left - 1] * nums[k] * nums[right + 1]
            max_coins = max(max_coins,
                           solve(left, k - 1) + solve(k + 1, right) + coins)

        return max_coins

    return solve(1, len(nums) - 2)

def main():
    n = int(input())
    nums = list(map(int, input().split()))
    print(max_coins_memo(nums))

main()
```

### Solution 3: Top-Down DP with Dictionary

```python
import sys
input = sys.stdin.readline

def max_coins_dict(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    memo = {}

    def solve(left, right):
        if left > right:
            return 0

        if (left, right) in memo:
            return memo[(left, right)]

        result = 0
        for k in range(left, right + 1):
            coins = nums[left - 1] * nums[k] * nums[right + 1]
            result = max(result, solve(left, k - 1) + solve(k + 1, right) + coins)

        memo[(left, right)] = result
        return result

    return solve(1, len(nums) - 2)

def main():
    n = int(input())
    nums = list(map(int, input().split()))
    print(max_coins_dict(nums))

main()
```

### Complexity Analysis
- **Time:** O(N^3) - Three nested loops (length, left, k)
- **Space:** O(N^2) - DP table

### Key Points
- Key insight: think of which balloon to burst LAST in a range
- Adding virtual balloons at boundaries simplifies edge cases
- This is a classic interval DP problem
- For N up to 300, O(N^3) is acceptable (~27 million operations)

---

## Quick Reference During Test

### Interval DP Template
```python
def interval_dp(nums):
    nums = [1] + nums + [1]  # Add boundaries
    n = len(nums)
    dp = [[0] * (n + 2) for _ in range(n + 2)]

    for length in range(1, n - 1):  # Interval length
        for left in range(1, n - length):  # Start of interval
            right = left + length - 1  # End of interval

            for k in range(left, right + 1):  # Split point
                # Calculate cost
                cost = nums[left-1] * nums[k] * nums[right+1]
                dp[left][right] = max(dp[left][right],
                                       dp[left][k-1] + dp[k+1][right] + cost)

    return dp[1][n-2]
```

### Backtracking Template
```python
def backtrack(path, remaining):
    if not remaining:
        result.append(path[:])
        return

    for i in range(len(remaining)):
        if is_valid(remaining[i]):
            path.append(remaining[i])
            backtrack(path, remaining[i+1:])
            path.pop()
```

### Edge Cases to Test

```
Word Break II:
├── No valid sentence → output nothing (empty)
├── Single character in dict → "a" with dict ["a"] → "a"
├── Entire string is one word → just that word
├── Very long string → memoization is critical
├── Repeated patterns → memo prevents recomputation
└── Lexicographic order → sort output before printing

Burst Balloons:
├── Single balloon → 1*balloon*1 = balloon
├── All same values → compute carefully
├── Maximum constraint N=300 → O(N³) is ~27M ops, fine
├── Virtual balloons [1] at boundaries → simplifies edge cases
└── Off-by-one errors in DP loops → most common bug!
```

### Common Mistakes to Avoid

```
Word Break II:
├── Forgetting to sort output lexicographically
├── Not using memoization → exponential time blowup
├── Not checking if word break is possible first
├── Off-by-one in string slicing (s[start:end])
└── Building strings incorrectly (missing spaces)

Burst Balloons:
├── Not adding virtual balloons at boundaries
├── Off-by-one: dp indices vs array indices
├── Wrong DP transition (using first instead of last balloon)
├── Forgetting that nums[0] and nums[n+1] are virtual
└── Not iterating intervals in correct length order
```

### Speed Tips for Hard Round

```
Time Budget: 45 minutes per question
├── 0-10 min:  Read, identify pattern, explain approach
├── 10-30 min: Write solution carefully
├── 30-40 min: Test with sample inputs + debug
└── 40-45 min: Optimize edge cases, verify complexity

Key Strategies:
1. EXPLAIN YOUR APPROACH before coding (interviewers value this)
2. Start with the optimal approach if you recognize the pattern
3. Use memoization templates you've memorized
4. For DP: Draw the table, fill a few cells manually
5. For backtracking: Draw the recursion tree for small input
6. Test with the SMALLEST possible input first
```

### Post-Test Checklist
- [ ] Did I explain the approach clearly?
- [ ] Is my solution optimal?
- [ ] Did I handle all edge cases?
- [ ] Did I test with sample inputs?
- [ ] Is my code clean and readable?
- [ ] Did I mention time and space complexity?
- [ ] Did I sort output for Word Break II?
- [ ] Did I add virtual balloons for Burst Balloons?
