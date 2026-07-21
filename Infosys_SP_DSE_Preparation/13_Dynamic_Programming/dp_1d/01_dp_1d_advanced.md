# 1D DP — Advanced Problems

## Maximum Subarray (Kadane's Algorithm)

Given an integer array nums, find the contiguous subarray (containing at least one number) with the largest sum.

**Concept:** At each position, choose to extend the existing subarray or start fresh.

```python
def max_subarray_kadane(nums: list) -> int:
    max_ending_here = max_so_far = nums[0]
    for num in nums[1:]:
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far

# Example: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
#          max_ending_here: -2 -> 1 -> -2 -> 4 -> 3 -> 5 -> 6 -> 1 -> 5
#          max_so_far:      -2 -> 1 -> 1 -> 4 -> 4 -> 5 -> 6 -> 6 -> 6

# Time: O(n), Space: O(1)

def max_subarray_with_indices(nums: list) -> tuple:
    max_ending_here = max_so_far = nums[0]
    start = end = temp_start = 0
    for i in range(1, len(nums)):
        if nums[i] > max_ending_here + nums[i]:
            max_ending_here = nums[i]
            temp_start = i
        else:
            max_ending_here += nums[i]
        if max_ending_here > max_so_far:
            max_so_far = max_ending_here
            start, end = temp_start, i
    return max_so_far, nums[start:end + 1]
```

---

## Maximum Circular Subarray Sum

Given a circular array, find max sum of a contiguous subarray (allowing wrap-around).

**Approach:** max(circular_sum, non_circular_sum) where:
- non_circular = Kadane
- circular = total_sum - (-Kadane on negated array) = total_sum - min_subarray sum

```python
def max_circular_subarray(nums: list) -> int:
    def kadane(arr: list) -> int:
        cur = res = arr[0]
        for v in arr[1:]:
            cur = max(v, cur + v)
            res = max(res, cur)
        return res

    non_circular = kadane(nums)
    total = sum(nums)
    # If all numbers are negative, total - min_subarray = 0, return non_circular
    min_subarray = kadane([-x for x in nums])
    circular = total + min_subarray  # because min_subarray = -(max negative subarray)
    if circular == 0:
        return non_circular
    return max(non_circular, circular)

# Time: O(n), Space: O(1)
```

---

## Maximum Product Subarray

Given an integer array nums, find the contiguous subarray with the largest product.

**Concept:** Track both max and min product ending at i (because a negative times negative can become positive).

```python
def max_product_subarray(nums: list) -> int:
    max_prod = min_prod = result = nums[0]
    for num in nums[1:]:
        candidates = (num, max_prod * num, min_prod * num)
        max_prod = max(candidates)
        min_prod = min(candidates)
        result = max(result, max_prod)
    return result

# Example: nums = [2, 3, -2, 4]
# max_prod: 2 -> 6 -> -2 -> 4
# min_prod: 2 -> 3 -> -12 -> -48
# result:   2 -> 6 -> 6 -> 6

# Time: O(n), Space: O(1)
```

---

## Longest Alternating Subsequence

Given an array, find longest subsequence that alternates between increasing and decreasing.

```python
def longest_alternating_subseq(nums: list) -> int:
    if not nums:
        return 0
    up = down = 1  # length of LDS ending with up/down trend
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            up = down + 1
        elif nums[i] < nums[i - 1]:
            down = up + 1
    return max(up, down)

# Time: O(n), Space: O(1)

def wiggly_max_length(nums: list) -> int:
    """Alternative name: Wiggle Subsequence"""
    if len(nums) < 2:
        return len(nums)
    prev_diff = nums[1] - nums[0]
    length = 2 if prev_diff != 0 else 1
    for i in range(2, len(nums)):
        diff = nums[i] - nums[i - 1]
        if (diff > 0 and prev_diff <= 0) or (diff < 0 and prev_diff >= 0):
            length += 1
            prev_diff = diff
    return length

# Time: O(n), Space: O(1)
```

---

## Maximum Length of Pair Chain

Given n pairs, chain p2 = (c,d) after p1 = (a,b) if b < c. Find the longest chain.

```python
def find_longest_chain(pairs: list) -> int:
    pairs.sort(key=lambda x: x[1])
    curr_end = float('-inf')
    count = 0
    for a, b in pairs:
        if a > curr_end:
            count += 1
            curr_end = b
    return count

# Time: O(n log n), Space: O(1)
```

---

## Longest Bitonic Subsequence

A subsequence that first increases then decreases. Find its maximum length.

**Concept:** LIS from left + LIS from right - 1

```python
def longest_bitonic_subseq(nums: list) -> int:
    n = len(nums)
    if n <= 2:
        return n
    # LIS from left
    lis = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                lis[i] = max(lis[i], lis[j] + 1)
    # LIS from right (LDS)
    lds = [1] * n
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if nums[j] < nums[i]:
                lds[i] = max(lds[i], lds[j] + 1)
    max_len = 0
    for i in range(n):
        max_len = max(max_len, lis[i] + lds[i] - 1)
    return max_len

# Example: nums = [1, 11, 2, 10, 4, 5, 2, 1]
# lis:  [1, 2, 2, 3, 3, 4, 2, 1]
# lds:  [4, 2, 3, 3, 2, 2, 1, 1]
# both: [5, 4, 5, 6, 5, 6, 3, 2]  -> max = 6

# Time: O(n²), Space: O(n)
```

---

## Egg Dropping Problem

Given k eggs and n floors, find min number of drops needed in worst case to find the threshold floor.

**Concept:** dp[k][n] = 1 + min(max(dp[k-1][x-1], dp[k][n-x]) for x in 1..n)

```python
def egg_drop_memo(k: int, n: int, memo=None) -> int:
    if memo is None:
        memo = {}
    if k == 1 or n <= 1:
        return n
    key = (k, n)
    if key in memo:
        return memo[key]
    # Binary search on x
    lo, hi = 1, n
    best = float('inf')
    while lo <= hi:
        mid = (lo + hi) // 2
        broken = egg_drop_memo(k - 1, mid - 1, memo)
        intact = egg_drop_memo(k, n - mid, memo)
        worst = 1 + max(broken, intact)
        if broken < intact:
            lo = mid + 1
        else:
            hi = mid - 1
        best = min(best, worst)
    memo[key] = best
    return best

def egg_drop_tab(k: int, n: int) -> int:
    dp = [[0] * (n + 1) for _ in range(k + 1)]
    for j in range(1, n + 1):
        dp[1][j] = j
    for i in range(2, k + 1):
        x = 1
        for j in range(1, n + 1):
            while x < j and max(dp[i - 1][x - 1], dp[i][j - x]) > max(dp[i - 1][x], dp[i][j - x - 1]):
                x += 1
            dp[i][j] = 1 + max(dp[i - 1][x - 1], dp[i][j - x])
    return dp[k][n]

# Time: O(k * n log n) for memo with BS, O(k * n) for tab with two-pointer
```

---

## Word Break

Given a string s and a word dictionary, determine if s can be segmented into dictionary words.

**Concept:** dp[i] = True if s[0:i] can be segmented. dp[i] = any(dp[j] and s[j:i] in wordSet)

```python
def word_break_memo(s: str, word_dict: list, start: int = 0, memo=None) -> bool:
    if memo is None:
        memo = {}
    if start == len(s):
        return True
    if start in memo:
        return memo[start]
    words = set(word_dict)
    for end in range(start + 1, len(s) + 1):
        if s[start:end] in words and word_break_memo(s, word_dict, end, memo):
            memo[start] = True
            return True
    memo[start] = False
    return False

def word_break_tab(s: str, word_dict: list) -> bool:
    words = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[n]

# Time: O(n² * L) with string slicing, Space: O(n)
```

---

## Minimum Jumps to Reach End

Given array arr where arr[i] max jump length from index i. Find min jumps.

```python
def min_jumps_memo(arr: list, i: int = 0, memo=None) -> int:
    if memo is None:
        memo = {}
    if i >= len(arr) - 1:
        return 0
    if i in memo:
        return memo[i]
    if arr[i] == 0:
        return float('inf')
    min_j = float('inf')
    for jump in range(1, arr[i] + 1):
        if i + jump < len(arr):
            min_j = min(min_j, 1 + min_jumps_memo(arr, i + jump, memo))
    memo[i] = min_j
    return min_j

def min_jumps_tab(arr: list) -> int:
    n = len(arr)
    dp = [float('inf')] * n
    dp[0] = 0
    for i in range(n):
        if dp[i] != float('inf'):
            for j in range(1, arr[i] + 1):
                if i + j < n:
                    dp[i + j] = min(dp[i + j], dp[i] + 1)
    return dp[n - 1] if dp[n - 1] != float('inf') else -1

# Time: O(n * max_jump) worst O(n²), Space: O(n)
```

---

## Jump Game II

Find minimum jumps to reach end. Each element tells max jump length.

**Greedy + BFS approach (O(n)):**

```python
def jump_game_ii(nums: list) -> int:
    n = len(nums)
    if n <= 1:
        return 0
    jumps = 0
    curr_end = 0
    farthest = 0
    for i in range(n - 1):
        farthest = max(farthest, i + nums[i])
        if i == curr_end:
            jumps += 1
            curr_end = farthest
            if curr_end >= n - 1:
                break
    return jumps

# Example: nums = [2, 3, 1, 1, 4]
#          farthest: 2 -> 4 -> 4 -> 4 -> 4
#          curr_end: 2 -> 2 -> 4 -> 4 -> 4
#          jumps:    0 -> 1 -> 1 -> 2 -> 2
# Answer: 2

# Time: O(n), Space: O(1)
```

---

## Stone Game Variants

### Stone Game I (Alice and Bob pick from ends)

```python
def stone_game_i(piles: list) -> bool:
    """Alice can always win with optimal play"""
    n = len(piles)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = piles[i]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(piles[i] - dp[i + 1][j],
                           piles[j] - dp[i][j - 1])
    return dp[0][n - 1] >= 0

# Time: O(n²), Space: O(n²) -> O(n)
```

### Stone Game II (pick 1 to 2x previous)

```python
def stone_game_ii(piles: list) -> int:
    n = len(piles)
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + piles[i]
    dp = [[0] * (n + 1) for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for m in range(1, n + 1):
            if i + 2 * m >= n:
                dp[i][m] = suffix[i]
            else:
                best = 0
                for x in range(1, 2 * m + 1):
                    if i + x < n:
                        best = max(best, suffix[i] - dp[i + x][max(x, m)])
                dp[i][m] = best
    return dp[0][1]

# Time: O(n³) worst, Space: O(n²)
# Can be optimized: dp[i][m] = max(dp[i][m], dp[i+2*m][m] + sum(i to i+2*m-1))
```

---

## Summary Table

| Problem | Approach | Time | Space |
|---------|----------|------|-------|
| Max Subarray | Kadane | O(n) | O(1) |
| Max Circular Subarray | MinKadane + Total | O(n) | O(1) |
| Max Product Subarray | Track max/min | O(n) | O(1) |
| L Alternating Subseq | Track up/down | O(n) | O(1) |
| L Bitonic Subseq | LIS left + right | O(n²) | O(n) |
| Egg Dropping | Minimax with BS | O(k n log n) | O(k n) |
| Word Break | String DP | O(n²) | O(n) |
| Min Jumps | DP with BFS | O(n²) worst | O(n) |
| Jump Game II | Greedy BFS | O(n) | O(1) |
| Stone Game | Minimax DP | O(n²) | O(n) |
