# Knapsack Advanced Variants

## Bounded Knapsack

Each item has a limited quantity count[i]. Choose items to maximize value within W.

**Concept:** Apply binary splitting to convert to 0/1 with O(n log c) items, or use modulo DP.

```python
def bounded_knapsack_direct(W: int, wt: list, val: list, count: list) -> int:
    """count[i] = max available pieces of item i"""
    dp = [0] * (W + 1)
    for i in range(len(wt)):
        c = count[i]
        w = wt[i]
        v = val[i]
        # Use binary splitting for O(W log c) per item
        k = 1
        while c > 0:
            take = min(k, c)
            weight = take * w
            value = take * v
            for cap in range(W, weight - 1, -1):
                dp[cap] = max(dp[cap], dp[cap - weight] + value)
            c -= take
            k <<= 1
    return dp[W]

# Example: wt=[2,3,5], val=[3,4,6], cnt=[2,3,1], W=10
# Available items: two of wt=2, three of wt=3, one of wt=5

# Time: O(W × Σ log count[i]), Space: O(W)
```

### Using Modulo DP for Bounded Knapsack (O(nW))

```python
def bounded_knapsack_modulo(W: int, wt: list, val: list, count: list) -> int:
    """Alternative: used for problems like "count limited supply" """
    dp = [-1] * (W + 1)
    dp[0] = 0
    for i in range(len(wt)):
        for w in range(W + 1):
            if dp[w] >= 0:
                dp[w] = count[i]
            elif w >= wt[i] and dp[w - wt[i]] > 0:
                dp[w] = dp[w - wt[i]] - 1
            else:
                dp[w] = -1
    max_val = 0
    # Not directly for max value; usually this tracks remaining count
    return max_val

# Time: O(n × W), Space: O(W)
```

---

## Multiple Knapsack (Two Knapsacks)

Given two knapsacks with capacities W1, W2, maximize total value. Each item goes to one knapsack.

```python
def two_knapsack(W1: int, W2: int, wt: list, val: list) -> int:
    dp = [[0] * (W2 + 1) for _ in range(W1 + 1)]
    for i in range(len(wt)):
        w, v = wt[i], val[i]
        for c1 in range(W1, -1, -1):
            for c2 in range(W2, -1, -1):
                if c1 >= w:
                    dp[c1][c2] = max(dp[c1][c2], dp[c1 - w][c2] + v)
                if c2 >= w:
                    dp[c1][c2] = max(dp[c1][c2], dp[c1][c2 - w] + v)
    return dp[W1][W2]

# Time: O(n × W1 × W2), Space: O(W1 × W2)
```

---

## Palindrome Partitioning II

Given a string s, cut it into palindromes. Find minimum cuts.

```python
def min_cut_palindrome_memo(s: str, i: int = 0, memo=None) -> int:
    if memo is None:
        memo = {}
    if i >= len(s) or s[i:] == s[i:][::-1]:
        return 0
    if i in memo:
        return memo[i]
    cuts = float('inf')
    for j in range(i, len(s)):
        if s[i:j + 1] == s[i:j + 1][::-1]:
            cuts = min(cuts, 1 + min_cut_palindrome_memo(s, j + 1, memo))
    memo[i] = cuts
    return cuts

def min_cut_palindrome_tab(s: str) -> int:
    n = len(s)
    if n <= 1:
        return 0
    # palindrome[i][j] = True if s[i:j+1] is palindrome
    pal = [[False] * n for _ in range(n)]
    dp = [float('inf')] * n

    # Precompute palindromes
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or pal[i + 1][j - 1]):
                pal[i][j] = True

    for i in range(n):
        if pal[0][i]:
            dp[i] = 0
        else:
            for j in range(i):
                if pal[j + 1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)
    return dp[n - 1]

# Example: s = "aab"
# Answer: 1 ("aa" | "b")

# Time: O(n²), Space: O(n²)
```

---

## Partition Equal Subset Sum (Print Subsets)

Same as detecting equal partition, but also prints the subsets.

```python
def partition_equal_subsets(nums: list) -> list:
    total = sum(nums)
    if total % 2 != 0:
        return []
    target = total // 2
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = True

    for i in range(1, n + 1):
        for s in range(1, more_get_more_1):
            dp[i][s] = dp[i - 1][s]
            if nums[i - 1] <= s:
                dp[i][s] = dp[i][s] or dp[i - 1][s - nums[i - 1]]

    if not dp[n][target]:
        return []

    # Backtrack
    s = target
    subset1, subset2 = [], []
    for i in range(n, 0, -1):
        if dp[i - 1][s]:
            subset2.append(nums[i - 1])
        else:
            subset1.append(nums[i - 1])
            s -= nums[i - 1]
    return [subset1, subset2]

# Time: O(n × target), Space: O(n × target)
```

---

## Target Sum

Given nums and a target, assign each element + or - to reach target. Count ways.

**Concept:** Transform to subset sum.
```
sum(P) - sum(N) = target
sum(P) + sum(N) = total  =>  sum(P) = (total + target) / 2
```

```python
def find_target_sum_memo(nums: list, target: int, i: int = 0, memo=None) -> int:
    if memo is None:
        memo = {}
    if i == len(nums):
        return 1 if target == 0 else 0
    key = (i, target)
    if key in memo:
        return memo[key]
    ways = find_target_sum_memo(nums, target + nums[i], i + 1, memo) + \
           find_target_sum_memo(nums, target - nums[i], i + 1, memo)
    memo[key] = ways
    return ways

def find_target_sum_tab(nums: list, target: int) -> int:
    total = sum(nums)
    if (total + target) % 2 != 0 or abs(target) > total:
        return 0
    new_target = (total + target) // 2
    dp = [0] * (new_target + 1)
    dp[0] = 1
    for num in nums:
        for s in range(new_target, num - 1, -1):
            dp[s] += dp[s - num]
    return dp[new_target]

# Example: nums = [1, 1, 1, 1, 1], target = 3
# Answer: 5
# +1+1+1+1-1, +1+1+1-1+1, +1+1-1+1+1, +1-1+1+1+1, -1+1+1+1+1

# Time: O(n × new_target), Space: O(new_target)
```

---

## Last Stone Weight II

Given stones. Smash pairs together. Find smallest possible remaining stone.

**Concept:** Same as minimum subset sum difference.

```python
def last_stone_weight_ii(stones: list) -> int:
    total = sum(stones)
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for stone in stones:
        for s in range(target, stone - 1, -1):
            dp[s] = dp[s] or dp[s - stone]
    for s in range(target, -1, -1):
        if dp[s]:
            return total - 2 * s
    return total

# Example: stones = [2, 7, 4, 1, 8, 1]
# Answer: 1
# (2+8)-(7+4+1+1) = 10-13 = -1 -> absolute = 1

# Time: O(n × target), Space: O(target)
```

---

## Ones and Zeros (Binary Knapsack)

Given array of binary strings and m ones, n zeros. Find max subset size with at most m 1s and n 0s.

```python
def find_max_form(strs: list, m: int, n: int) -> int:
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        zeros = s.count('0')
        ones = s.count('1')
        for i in range(m, zeros - 1, -1):
            for j in range(n, ones - 1, -1):
                dp[i][j] = max(dp[i][j], dp[i - zeros][j - ones] + 1)
    return dp[m][n]

# Example: strs = ["10","0001","111001","1","0"], m=5, n=3
# Answer: 4 ("10", "0001", "1", "0")
# Totals: zeros=5, ones=3

# Time: O(k × m × n) where k = len(strs)
```

---

## Summary Table

| Problem | Key Insight | Time | Space |
|---------|-------------|------|-------|
| Bounded Knapsack | Binary splitting | O(W log c) | O(W) |
| Multiple Knapsack | 2D capacities | O(n×W1×W2) | O(W1×W2) |
| Palindrome Cut | Precompute palindromes | O(n²) | O(n²) |
| Equal Subset sum | Backtrack print | O(n×target) | O(n×target) |
| Target Sum | Transform to subset | O(n×target) | O(target) |
| Last Stone II | Min subset diff same | O(n×target) | O(target) |
| Ones and Zeros | 2-cost knapsack | O(k×m×n) | O(m×n) |
