# Infosys SP DSE - Mock Test 2 (3 Hours)

> 3 questions: Easy (25 min) + Medium (50 min) + Hard (90 min)

---

## Question 1: Two Sum - Find All Unique Pairs (Easy - 25 minutes)

### Problem Statement

Given an array of integers and a target sum, find all unique pairs of elements that add up to the target. Return pairs in sorted order.

**Input Format:**
- First line: N (number of elements) and K (target sum)
- Second line: N space-separated integers

**Output Format:**
- Each line: a pair of numbers (sorted)
- If no pairs exist, print "No pairs found"

**Constraints:**
- 1 ≤ N ≤ 10^5
- -10^9 ≤ arr[i], K ≤ 10^9

### Sample Test Cases

```
Input:  N=7, K=6, arr=[1, 5, 7, -1, 5, 1, 6]
Output:
    -1 7
    1 5
Explanation: (-1,7) and (1,5) sum to 6

Input:  N=4, K=0, arr=[1, 2, 3, -3]
Output:
    -3 3
```

### Approach 1: Hash Map (Optimal)

```python
def find_all_pairs(arr, target):
    from collections import Counter
    freq = Counter(arr)
    result = []
    visited = set()

    for num in arr:
        complement = target - num
        if complement in freq:
            pair = (min(num, complement), max(num, complement))
            if num not in visited:
                if num == complement:
                    if freq[num] > 1:
                        result.append(pair)
                else:
                    result.append(pair)
                visited.add(num)

    result.sort()
    return result

def main():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    pairs = find_all_pairs(arr, k)

    if not pairs:
        print("No pairs found")
    else:
        for pair in pairs:
            print(f"{pair[0]} {pair[1]}")

main()
```

### Approach 2: Sorting + Two Pointers

```python
def find_all_pairs_two_pointer(arr, target):
    arr.sort()
    result = []
    left, right = 0, len(arr) - 1

    while left < right:
        curr_sum = arr[left] + arr[right]
        if curr_sum == target:
            result.append((arr[left], arr[right]))
            while left < right and arr[left] == arr[left + 1]:
                left += 1
            while left < right and arr[right] == arr[right - 1]:
                right -= 1
            left += 1
            right -= 1
        elif curr_sum < target:
            left += 1
        else:
            right -= 1

    return result

def main():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    pairs = find_all_pairs_two_pointer(arr, k)

    for pair in pairs:
        print(f"{pair[0]} {pair[1]}")

main()
```

### Complexity Analysis
- **Approach 1:** O(n) time, O(n) space — Optimal
- **Approach 2:** O(n log n) time, O(1) space

### Tips
- Handle duplicate elements carefully
- When num == complement, need at least 2 occurrences
- This is a variant of the classic Two Sum problem frequently asked at Infosys

---

## Question 2: Minimum Cost to Hire K Workers (Medium - 50 minutes)

### Problem Statement

There are N workers. The i-th worker has quality[i] and minimum wage expectation wage[i]. We want to hire exactly K workers to form a paid group. When hiring a group, we must pay each worker in the group at least their minimum wage expectation AND in proportion to their quality. Find the minimum total cost.

**Input Format:**
- First line: N and K
- Second line: quality[i]
- Third line: wage[i]

**Output Format:**
- Single float: minimum cost rounded to 2 decimal places

**Constraints:**
- 1 ≤ K ≤ N ≤ 10^4
- 1 ≤ quality[i], wage[i] ≤ 10^4

### Sample Test Cases

```
Input:  N=3, K=2
        quality = [10, 20, 5]
        wage = [70, 100, 50]
Output: 105.00
Explanation: Pay worker 0 and worker 2.
- Ratio: min(70/10, 50/5) = min(7, 10) = 7
- Total: 7*10 + 7*5 = 70 + 35 = 105

Input:  N=3, K=1
        quality = [10, 20, 5]
        wage = [70, 100, 50]
Output: 50.00
```

### Approach 1: Sort by Wage-to-Quality Ratio + Min-Heap (Optimal)

```python
import heapq

def min_cost_to_hire_workers(quality, wage, k):
    n = len(quality)
    # Sort by wage/quality ratio
    workers = sorted([(wage[i] / quality[i], quality[i]) for i in range(n)])

    result = float('inf')
    quality_sum = 0
    max_heap = []

    for ratio, q in workers:
        quality_sum += q
        heapq.heappush(max_heap, -q)

        if len(max_heap) > k:
            quality_sum += heapq.heappop(max_heap)

        if len(max_heap) == k:
            result = min(result, quality_sum * ratio)

    return round(result, 2)

def main():
    n, k = map(int, input().split())
    quality = list(map(int, input().split()))
    wage = list(map(int, input().split()))
    print(f"{min_cost_to_hire_workers(quality, wage, k):.2f}")

main()
```

### Approach 2: Brute Force with Pruning

```python
from itertools import combinations

def min_cost_brute(quality, wage, k):
    n = len(quality)
    min_cost = float('inf')

    for combo in combinations(range(n), k):
        max_ratio = 0
        total_quality = 0
        for i in combo:
            ratio = wage[i] / quality[i]
            max_ratio = max(max_ratio, ratio)
            total_quality += quality[i]

        cost = max_ratio * total_quality
        min_cost = min(min_cost, cost)

    return round(min_cost, 2)

def main():
    n, k = map(int, input().split())
    quality = list(map(int, input().split()))
    wage = list(map(int, input().split()))
    print(f"{min_cost_brute(quality, wage, k):.2f}")

main()
```

### Complexity Analysis
- **Approach 1:** O(n log n) time, O(n) space — Optimal
- **Approach 2:** O(C(n,k) * k) time — Brute force, too slow for large n

### Tips
- Key insight: sort by ratio, then use heap to track k smallest qualities
- The maximum ratio in the group determines the payment multiplier
- Heap stores negative values for max-heap in Python's min-heap

---

## Question 3: Word Break II - Find All Valid Sentences (Hard - 90 minutes)

### Problem Statement

Given a string `s` and a dictionary of words `wordDict`, return all possible sentences where each word is from the dictionary.

**Input Format:**
- First line: string s
- Second line: number of words in dictionary
- Next lines: dictionary words

**Output Format:**
- Each line: a valid sentence
- Sentences should be in lexicographic order

**Constraints:**
- 1 ≤ |s| ≤ 20
- 1 ≤ |wordDict| ≤ 1000
- 1 ≤ |wordDict[i]| ≤ 10

### Sample Test Cases

```
Input:  s = "catsanddog"
        wordDict = ["cat", "cats", "and", "sand", "dog"]
Output:
    cat sand dog
    cats and dog

Input:  s = "pineapplepenapple"
        wordDict = ["apple", "pen", "applepen", "pine", "pineapple"]
Output:
    pine apple pen apple
    pine applepen apple
    pineapple pen apple
```

### Approach 1: Backtracking with Memoization (Optimal)

```python
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

    return backtrack(0)

def main():
    s = input().strip()
    n = int(input())
    word_dict = [input().strip() for _ in range(n)]
    sentences = word_break_ii(s, word_dict)
    for sentence in sorted(sentences):
        print(sentence)

main()
```

### Approach 2: BFS Approach

```python
from collections import deque

def word_break_bfs(s, word_dict):
    word_set = set(word_dict)
    result = []
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

### Approach 3: DP + Backtracking

```python
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
- **Approach 1:** O(2^n) time (worst), O(n * 2^n) space with memo
- **Approach 2:** O(2^n) time, O(2^n) space — BFS explores all paths
- **Approach 3:** O(n^2 + 2^n) time — DP first, then backtrack

### Tips
- Always check if word break is possible first (DP check)
- Memoization significantly prunes the search space
- Sort output for lexicographic order
- Practice both Word Break I (true/false) and II (all sentences)

---

## Time Management Guide

| Question | Time | Target |
|----------|------|--------|
| Q1 (Easy) | 25 min | Clean solution + test |
| Q2 (Medium) | 50 min | Optimal approach + verify |
| Q3 (Hard) | 90 min | Plan + implement + test |
| Buffer | 15 min | Review edge cases |

### Strategy
1. Q1 should be solved quickly - it's a Two Sum variant
2. Q2 requires heap knowledge - sketch approach first
3. Q3 is the hardest - even partial solutions earn marks
4. For Q3, start with approach explanation before coding
5. Handle edge cases: empty dictionary, no valid sentences

### Common Mistakes to Avoid
- Q1: Forgetting to handle duplicates
- Q2: Using integer division instead of float
- Q3: Not sorting the output
- Q3: Running out of time due to no memoization
