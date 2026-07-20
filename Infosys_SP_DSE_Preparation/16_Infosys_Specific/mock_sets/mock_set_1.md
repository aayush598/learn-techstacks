# Infosys SP DSE - Mock Test 1 (3 Hours)

> 3 questions: Easy (25 min) + Medium (50 min) + Hard (90 min)

---

## Question 1: Maximum Circular Subarray Sum (Easy - 25 minutes)

### Problem Statement

Given an array of integers, find the maximum sum of a circular contiguous subarray. The subarray can wrap around (i.e., the end connects to the beginning).

**Input Format:**
- First line: integer N (number of elements)
- Second line: N space-separated integers

**Output Format:**
- Single integer: maximum circular subarray sum

**Constraints:**
- 1 ≤ N ≤ 10^5
- -10^4 ≤ arr[i] ≤ 10^4

### Sample Test Cases

```
Input:  N = 7, arr = [8, -8, 9, -9, 10, -11, 12]
Output: 22
Explanation: The circular subarray [12, 8, -8, 9, -9, 10] = 22

Input:  N = 5, arr = [1, -2, 3, 4, -5]
Output: 11
Explanation: The circular subarray [3, 4, -5, 1] = 3
```

### Approach 1: Modified Kadane's (Optimal)

The maximum circular sum is either:
1. Normal Kadane's result (non-wrapping), or
2. Total sum - minimum subarray sum (wrapping case)

```python
def kadanes_max(arr):
    max_sum = arr[0]
    curr_sum = arr[0]
    for i in range(1, len(arr)):
        curr_sum = max(arr[i], curr_sum + arr[i])
        max_sum = max(max_sum, curr_sum)
    return max_sum

def kadanes_min(arr):
    min_sum = arr[0]
    curr_sum = arr[0]
    for i in range(1, len(arr)):
        curr_sum = min(arr[i], curr_sum + arr[i])
        min_sum = min(min_sum, curr_sum)
    return min_sum

def max_circular_sum(arr):
    n = len(arr)
    max_kadane = kadanes_max(arr)
    min_kadane = kadanes_min(arr)

    total_sum = sum(arr)

    # Edge case: all elements negative
    if total_sum == min_kadane:
        return max_kadane

    return max(max_kadane, total_sum - min_kadane)

N = int(input())
arr = list(map(int, input().split()))
print(max_circular_sum(arr))
```

### Approach 2: Deque-based Sliding Window

Maintain a deque for prefix sums to track maximum difference.

```python
from collections import deque

def max_circular_sum_deque(arr):
    n = len(arr)
    prefix = [0] * (2 * n + 1)
    for i in range(2 * n):
        prefix[i + 1] = prefix[i] + arr[i % n]

    result = float('-inf')
    dq = deque([0])

    for i in range(1, 2 * n + 1):
        while dq and dq[0] < i - n:
            dq.popleft()

        if dq:
            result = max(result, prefix[i] - prefix[dq[0]])

        while dq and prefix[dq[-1]] >= prefix[i]:
            dq.pop()

        dq.append(i)

    return result

N = int(input())
arr = list(map(int, input().split()))
print(max_circular_sum_deque(arr))
```

### Complexity Analysis
- **Approach 1:** O(N) time, O(1) space — Optimal
- **Approach 2:** O(N) time, O(N) space — Deque approach

### Tips
- The key insight is: max circular = total - min non-circular
- Edge case: all negative numbers (return max element)
- This appeared in Infosys 2023 SP round

---

## Question 2: Longest Palindromic Subsequence (Medium - 50 minutes)

### Problem Statement

Given a string `s`, find the length of the longest palindromic subsequence in `s`.

**Input Format:**
- Single line: string s

**Output Format:**
- Single integer: length of longest palindromic subsequence

**Constraints:**
- 1 ≤ |s| ≤ 1000
- s contains only lowercase English letters

### Sample Test Cases

```
Input:  "bbbab"
Output: 4
Explanation: "bbbb" is the longest palindromic subsequence

Input:  "cbbd"
Output: 2
Explanation: "bb" is the longest palindromic subsequence
```

### Approach 1: 2D DP (Classic)

LCS of string and its reverse gives LPS.

```python
def longest_palindromic_subsequence(s):
    n = len(s)
    # dp[i][j] = LPS length in s[i:j+1]
    dp = [[0] * n for _ in range(n)]

    # Every single character is a palindrome of length 1
    for i in range(n):
        dp[i][i] = 1

    # Fill for lengths 2 to n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]

s = input().strip()
print(longest_palindromic_subsequence(s))
```

### Approach 2: Space-Optimized DP

```python
def longest_palindromic_subsequence_optimized(s):
    n = len(s)
    prev = [0] * n

    for i in range(n - 1, -1, -1):
        curr = [0] * n
        curr[i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                curr[j] = prev[j - 1] + 2
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr

    return prev[n - 1]

s = input().strip()
print(longest_palindromic_subsequence_optimized(s))
```

### Approach 3: Recursive + Memoization

```python
from functools import lru_cache

def longest_palindromic_subsequence_memo(s):
    n = len(s)

    @lru_cache(maxsize=None)
    def lps(i, j):
        if i > j:
            return 0
        if i == j:
            return 1
        if s[i] == s[j]:
            return lps(i + 1, j - 1) + 2
        return max(lps(i + 1, j), lps(i, j - 1))

    return lps(0, n - 1)

s = input().strip()
print(longest_palindromic_subsequence_memo(s))
```

### Complexity Analysis
- **Approach 1:** O(n^2) time, O(n^2) space
- **Approach 2:** O(n^2) time, O(n) space — Optimal
- **Approach 3:** O(n^2) time, O(n^2) space (memoization)

### Tips
- LPS = LCS(s, reverse(s)) is an alternative approach
- Bottom-up is generally preferred over recursion in interviews
- Practice also: print the actual LPS string, not just length

---

## Question 3: Binary Tree Maximum Path Sum (Hard - 90 minutes)

### Problem Statement

Given a non-empty binary tree, find the maximum path sum. A path is defined as any sequence of nodes from some starting node to any node in the tree along parent-child connections. The path must contain at least one node and does not need to go through the root.

**Input Format:**
- Level-order traversal of the tree (-1 for null nodes)

**Output Format:**
- Single integer: maximum path sum

**Constraints:**
- 1 ≤ Number of nodes ≤ 3 * 10^4
- -1000 ≤ Node.val ≤ 1000

### Sample Test Cases

```
Input:
        1
       / \
      2   3
Output: 6
Explanation: Path 2 -> 1 -> 3 = 6

Input:
       -10
       /  \
      9    20
          /  \
         15   7
Output: 42
Explanation: Path 15 -> 20 -> 7 = 42

Input:
        -3
Output: -3
```

### Approach 1: DFS with Global Maximum (Optimal)

```python
import sys
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(values):
    if not values or values[0] == -1:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1

    while queue and i < len(values):
        node = queue.popleft()

        if i < len(values) and values[i] != -1:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        if i < len(values) and values[i] != -1:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root

def max_path_sum(root):
    max_sum = float('-inf')

    def dfs(node):
        nonlocal max_sum
        if not node:
            return 0

        left_gain = max(dfs(node.left), 0)
        right_gain = max(dfs(node.right), 0)

        # Path through this node as the "peak"
        price_new_path = node.val + left_gain + right_gain
        max_sum = max(max_sum, price_new_path)

        # Return max single-branch path (parent will extend one branch)
        return node.val + max(left_gain, right_gain)

    dfs(root)
    return max_sum

values = list(map(int, input().split()))
root = build_tree(values)
print(max_path_sum(root))
```

### Approach 2: Iterative with Post-order Traversal

```python
def max_path_sum_iterative(root):
    if not root:
        return 0

    max_sum = float('-inf')
    stack = [(root, False)]
    node_gain = {}

    while stack:
        node, visited = stack.pop()

        if not node:
            continue

        if visited:
            left_gain = max(node_gain.get(id(node.left), 0), 0)
            right_gain = max(node_gain.get(id(node.right), 0), 0)

            price_new_path = node.val + left_gain + right_gain
            max_sum = max(max_sum, price_new_path)

            node_gain[id(node)] = node.val + max(left_gain, right_gain)
        else:
            stack.append((node, True))
            stack.append((node.right, False))
            stack.append((node.left, False))

    return max_sum

values = list(map(int, input().split()))
root = build_tree(values)
print(max_path_sum_iterative(root))
```

### Complexity Analysis
- **Approach 1:** O(n) time, O(h) space (h = height, recursion stack)
- **Approach 2:** O(n) time, O(n) space (explicit stack)

### Tips
- Key insight: path through node = left_gain + node + right_gain
- Return value is only one branch: node + max(left, right)
- Negative gains should be treated as 0 (don't include negative paths)
- This is a very common Infosys SP L3 question

---

## Time Management Guide

| Question | Time | Target |
|----------|------|--------|
| Q1 (Easy) | 25 min | Solve + optimize + test |
| Q2 (Medium) | 50 min | Solve + test + explain |
| Q3 (Hard) | 90 min | Plan + code + verify |
| Buffer | 15 min | Review all solutions |

### Strategy
1. Start with Q1 to build confidence
2. Move to Q2 after solving Q1
3. Tackle Q3 last - even partial solution helps
4. Always explain approach before coding
5. Test with edge cases before finalizing
