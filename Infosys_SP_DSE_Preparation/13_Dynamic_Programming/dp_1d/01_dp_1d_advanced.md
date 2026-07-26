# 1D DP — Advanced Problems

## When to Use 1D DP

```
┌─────────────────────────────────────────────────────────────────┐
│                    1D DP PATTERN RECOGNITION                    │
├─────────────────────────┬───────────────────────────────────────┤
│ Problem hints           │ Likely pattern                        │
├─────────────────────────┼───────────────────────────────────────┤
│ "max sum subarray"      │ Kadane's (track ending_here + global)│
│ "max product"           │ Track max AND min (negatives flip)    │
│ "can reach end?"        │ Greedy or BFS-style jump DP           │
│ "min jumps"             │ DP or greedy BFS                      │
│ "string segmentation"   │ Word Break (dp[i] = can reach i?)    │
│ "egg / drops / floors"  │ Egg Drop (2D state, minmax)           │
│ "alternating pattern"   │ Track up/down trend states            │
│ "chain pairs"           │ Greedy after sort (interval merge)   │
│ "game from ends"        │ Stone Game (interval minimax)         │
└─────────────────────────┴───────────────────────────────────────┘
```

---

## Maximum Subarray (Kadane's Algorithm)

Given an integer array nums, find the contiguous subarray (containing at least one number) with the largest sum.

### Intuition

Think of it as a traveler walking along the array. At each position they ask:
> "Is it better to continue the current streak, or start a new streak from here?"

```
Array:    -2    1    -3    4    -1    2    1    -5    4

Decision at each index:
─────────────────────────────────────────────────────────────
Index 0:  Start here. Current = -2.    Best = -2
Index 1:  1 > (-2+1)=-1 → START NEW.   Current =  1.  Best =  1
Index 2:  -3 < (1+-3)=-2 → CONTINUE.   Current = -2.  Best =  1
Index 3:  4 > (-2+4)=2  → START NEW.   Current =  4.  Best =  4
Index 4:  -1 < (4+-1)=3 → CONTINUE.    Current =  3.  Best =  4
Index 5:  2 < (3+2)=5   → CONTINUE.    Current =  5.  Best =  5
Index 6:  1 < (5+1)=6   → CONTINUE.    Current =  6.  Best =  6
Index 7:  -5 < (6+-5)=1 → CONTINUE.    Current =  1.  Best =  6
Index 8:  4 < (1+4)=5   → CONTINUE.    Current =  5.  Best =  6
─────────────────────────────────────────────────────────────

DP Table Visualization:
┌─────┬─────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
│ idx │  0  │  1   │  2   │  3   │  4   │  5   │  6   │  7   │  8   │
├─────┼─────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ num │ -2  │  1   │ -3   │  4   │ -1   │  2   │  1   │ -5   │  4   │
├─────┼─────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ cur │ -2  │  1   │ -2   │  4   │  3   │  5   │  6   │  1   │  5   │
├─────┼─────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│best │ -2  │  1   │  1   │  4   │  4   │  5   │  6   │  6   │  6   │
└─────┴─────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
                                                ▲
                                         Answer = 6
                              Subarray: [4, -1, 2, 1]
```

### Code with Comments

```python
def max_subarray_kadane(nums: list) -> int:
    # Initialize both with first element (not 0, because array may be all negative)
    max_ending_here = max_so_far = nums[0]
    for num in nums[1:]:
        # KEY DECISION: extend current subarray or start fresh?
        # If current element alone > extending, it's better to start new
        max_ending_here = max(num, max_ending_here + num)
        # Update global best across all positions seen so far
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far

# Time: O(n), Space: O(1)
```

### Variant: Return Indices

```python
def max_subarray_with_indices(nums: list) -> tuple:
    max_ending_here = max_so_far = nums[0]
    start = end = temp_start = 0
    for i in range(1, len(nums)):
        # If starting fresh gives a better value, update temp_start
        if nums[i] > max_ending_here + nums[i]:
            max_ending_here = nums[i]
            temp_start = i
        else:
            max_ending_here += nums[i]
        if max_ending_here > max_so_far:
            max_so_far = max_ending_here
            start, end = temp_start, i
    return max_so_far, nums[start:end + 1]

# Example: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
# Returns: (6, [4, -1, 2, 1])
```

---

## Maximum Circular Subarray Sum

Given a circular array, find max sum of a contiguous subarray (allowing wrap-around).

### Visual Intuition

In a circular array, the maximum subarray is either:
1. **Non-circular**: a regular subarray in the middle → Kadane's handles this
2. **Circular**: wraps around the ends → this equals `total - min_subarray`

```
Example: nums = [5, -3, 5]

Non-circular best subarray: [5] or [5] = 5
Circular wrap-around:       [5, 5] = 5 + 5 = 10  (skipping the middle -3)

Visualization of circular:
       ┌─── 5 ───┐
       │          │
      -3          5
       │          │
       └──────────┘

  Wrap-around subarray: [5 (end), 5 (start)] = total - (-3) = 10

Key insight:
  total = 5 + (-3) + 5 = 7
  min_subarray = -3
  circular = total - min_subarray = 7 - (-3) = 10  ✓

Special case: all negatives → circular = 0 (empty array), use non-circular
```

```python
def max_circular_subarray(nums: list) -> int:
    def kadane(arr: list) -> int:
        cur = res = arr[0]
        for v in arr[1:]:
            cur = max(v, cur + v)
            res = max(res, cur)
        return res

    non_circular = kadane(nums)          # Max subarray (normal)
    total = sum(nums)
    min_subarray = kadane([-x for x in nums])  # Max of negated = min of original
    circular = total + min_subarray      # total - (-min) = total + max_of_negated

    if circular == 0:  # All elements negative; circular would be empty
        return non_circular
    return max(non_circular, circular)

# Time: O(n), Space: O(1)
```

---

## Maximum Product Subarray

Given an integer array nums, find the contiguous subarray with the largest product.

### Why Track Both Max AND Min?

Unlike sum (where negatives just reduce value), in multiplication:
- **Negative × Negative = Positive** → a very negative product can become very positive!
- So we must track both the maximum and minimum product ending at each position.

```
Example: nums = [2, 3, -2, 4]

Step-by-step trace:
┌─────┬────┬──────────────────────────┬──────────────┬────────────┐
│ idx │num │ Candidates (num, max*num, │  max_prod    │  min_prod  │
│     │    │              min*num)     │              │            │
├─────┼────┼──────────────────────────┼──────────────┼────────────┤
│  0  │ 2  │ start: 2                  │      2       │      2     │
├─────┼────┼──────────────────────────┼──────────────┼────────────┤
│  1  │ 3  │ {3, 2*3=6, 2*3=6}        │      6       │      3     │
├─────┼────┼──────────────────────────┼──────────────┼────────────┤
│  2  │ -2 │ {-2, 6*-2=-12, 3*-2=-6}  │     -2  *    │    -12     │
│     │    │   (max picks -2, min picks -12)          │            │
├─────┼────┼──────────────────────────┼──────────────┼────────────┤
│  3  │ 4  │ {4, -2*4=-8, -12*4=-48}  │      4   *   │    -48     │
│     │    │  (max picks 4, but best overall = 6)     │            │
└─────┴────┴──────────────────────────┴──────────────┴────────────┘

  * marks the running maximum at each step

  Result: 6 (subarray [2, 3])
```

```python
def max_product_subarray(nums: list) -> int:
    # max_prod: max product of subarray ending at current position
    # min_prod: min product (needed because neg × neg = pos)
    max_prod = min_prod = result = nums[0]
    for num in nums[1:]:
        # Consider three candidates: starting fresh, extending max, extending min
        candidates = (num, max_prod * num, min_prod * num)
        max_prod = max(candidates)  # Current max ending here
        min_prod = min(candidates)  # Current min ending here (for future negatives)
        result = max(result, max_prod)
    return result

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

### Intuition with Visual

This is a **minimax** problem: we want to minimize the maximum drops in the worst case.

```
Key idea: When you drop an egg from floor x, two outcomes:

   Egg BREAKS                    Egg SURVIVES
   ─────────                     ────────────
   You lost 1 egg                Egg is still usable
   Answer is in [1, x-1]         Answer is in [x+1, n]
   Use (k-1) eggs, (x-1) floors  Use k eggs, (n-x) floors

   Worst case = 1 + max(broken_scenario, intact_scenario)

   You choose x to MINIMIZE this worst case.

DP Table for k=2 eggs, n=6 floors:
┌───────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ eggs  │  0  │  1  │  2  │  3  │  4  │  5  │  6  │  ← floors
├───────┼─────┼─────┼─────┼─────┼─────┼─────┤
│   1   │  0  │  1  │  2  │  3  │  4  │  5  │  6  │  (1 egg: linear scan)
├───────┼─────┼─────┼─────┼─────┼─────┼─────┤
│   2   │  0  │  1  │  2  │  2  │  3  │  3  │  3  │  ← answer
└───────┴─────┴─────┴─────┴─────┴─────┴─────┘

Reading dp[2][6] = 3 means: with 2 eggs and 6 floors, worst case = 3 drops.
Optimal strategy: drop at floors 2, 4, 5 (or similar).
```

### Code with Binary Search Optimization

```python
def egg_drop_memo(k: int, n: int, memo=None) -> int:
    if memo is None:
        memo = {}
    if k == 1 or n <= 1:
        return n  # 1 egg: must scan linearly; 0 floors: 0 drops
    key = (k, n)
    if key in memo:
        return memo[key]

    # Binary search for optimal floor x
    # As x increases, broken_scenario increases, intact_scenario decreases
    # The minimax point is where they are closest
    lo, hi = 1, n
    best = float('inf')
    while lo <= hi:
        mid = (lo + hi) // 2
        broken = egg_drop_memo(k - 1, mid - 1, memo)    # Egg breaks
        intact = egg_drop_memo(k, n - mid, memo)         # Egg survives
        worst = 1 + max(broken, intact)
        if broken < intact:
            lo = mid + 1   # Need to go higher to balance
        else:
            hi = mid - 1   # Need to go lower
        best = min(best, worst)
    memo[key] = best
    return best

# Tabulation approach:
def egg_drop_tab(k: int, n: int) -> int:
    dp = [[0] * (n + 1) for _ in range(k + 1)]
    for j in range(1, n + 1):
        dp[1][j] = j  # 1 egg, j floors → j drops needed
    for i in range(2, k + 1):
        x = 1  # Two-pointer: optimal floor x only increases
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

### Visual Walkthrough

```
s = "leetcode", wordDict = ["leet", "code"]

dp[i] = can we segment s[0:i]?

dp[0] = True   (empty string is always segmentable)
dp[1] = F      "l"    not in dict
dp[2] = F      "le"   not in dict
dp[3] = F      "lee"  not in dict
dp[4] = F      "leet" not in dict... wait, "leet" IS in dict!
              → need dp[0]=True (prefix up to j=0 is segmentable)
              → dp[4] = dp[0] && s[0:4] in dict = True ✓

dp[5] = F      "leetc" not in dict
dp[6] = F      "leetco" not in dict
dp[7] = F      "leetcod" not in dict
dp[8] = T      "leetcode": dp[4]=True && s[4:8]="code" in dict ✓

┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
│   │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │
├───┼───┼───┼───┼───┼───┼───┼───┼───┤
│ dp│ T │ F │ F │ F │ T │ F │ F │ F │ T │  ← answer
└───┴───┴───┴───┴───┴───┴───┴───┴───┘
         "l" "le"│"leet"                    "code"
                  │                           │
              j=0 found T                j=4 found T
              + s[0:4] in dict           + s[4:8] in dict

Answer: True ("leet" | "code")
```

```python
def word_break_tab(s: str, word_dict: list) -> bool:
    words = set(word_dict)  # O(1) lookup
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True  # Base: empty string is segmentable
    for i in range(1, n + 1):        # For each ending position
        for j in range(i):           # Try every split point j
            if dp[j] and s[j:i] in words:  # Prefix segmentable + suffix in dict
                dp[i] = True
                break                # No need to check other splits
    return dp[n]

# Time: O(n² * L) with string slicing, Space: O(n)
# L = average word length for the s[j:i] lookup
```

---

## Minimum Jumps to Reach End

Given array arr where arr[i] is the max jump length from index i. Find min jumps to reach end.

### Visual Walkthrough

```
arr = [2, 3, 1, 1, 4]

dp[i] = minimum jumps to reach index i from index 0

dp = [0, ∞, ∞, ∞, ∞]   (start at index 0 with 0 jumps)

Processing index 0 (arr[0]=2, can jump to 1 and 2):
  dp[1] = min(∞, 0+1) = 1
  dp[2] = min(∞, 0+1) = 1

Processing index 1 (arr[1]=3, can jump to 2, 3, 4):
  dp[2] = min(1, 1+1) = 1  (already better)
  dp[3] = min(∞, 1+1) = 2
  dp[4] = min(∞, 1+1) = 2

Processing index 2 (arr[2]=1, can jump to 3):
  dp[3] = min(2, 1+1) = 2  (already equal)

Processing index 3 (arr[3]=1, can jump to 4):
  dp[4] = min(2, 2+1) = 2  (already better)

Final dp = [0, 1, 1, 2, 2]

Visualization:
Index:     0     1     2     3     4
arr:      [2]   [3]   [1]   [1]   [4]
            │     │
            ├─────┤──→ can reach 1,2
            │     │
            ├─────┼──────→ can reach 2,3,4
            │     │
            └─────┴──→ min jumps = 2 (path: 0→1→4)
```

```python
def min_jumps_tab(arr: list) -> int:
    n = len(arr)
    dp = [float('inf')] * n
    dp[0] = 0  # Starting position: 0 jumps
    for i in range(n):
        if dp[i] != float('inf'):  # Only process reachable positions
            for j in range(1, arr[i] + 1):  # Try all possible jumps
                if i + j < n:
                    dp[i + j] = min(dp[i + j], dp[i] + 1)
    return dp[n - 1] if dp[n - 1] != float('inf') else -1

# Time: O(n * max_jump) worst O(n²), Space: O(n)
```

### Greedy BFS Approach (Optimal)

```python
def jump_game_ii(nums: list) -> int:
    """Think of it as BFS levels — each 'jump' = one BFS level"""
    n = len(nums)
    if n <= 1:
        return 0
    jumps = 0
    curr_end = 0    # End of current BFS level (current jump range)
    farthest = 0    # Farthest reachable point seen so far
    for i in range(n - 1):
        farthest = max(farthest, i + nums[i])  # Expand reach
        if i == curr_end:   # Finished current level
            jumps += 1       # Start new level
            curr_end = farthest
            if curr_end >= n - 1:
                break
    return jumps

# Example trace: nums = [2, 3, 1, 1, 4]
# i=0: farthest=2, curr_end=0 → jumps=1, curr_end=2
# i=1: farthest=4, curr_end=2
# i=2: i==curr_end → jumps=2, curr_end=4 (reached end!)

# Time: O(n), Space: O(1)
```

---

## Stone Game Variants

### Stone Game I — Visual Walkthrough

Alice and Bob take turns picking from either end. Alice picks first. Maximize your score.

```
piles = [5, 3, 1, 4]

This is an INTERVAL DP problem: dp[i][j] = best score difference for subarray [i..j]

Key insight: dp[i][j] = max(piles[i] - dp[i+1][j], piles[j] - dp[i][j-1])
  (what I take now) minus (opponent's best play on remainder)

DP Table (diagonal fill):
Subarrays of length 1:  dp[i][i] = piles[i]  (only one choice)
  dp[0][0]=5  dp[1][1]=3  dp[2][2]=1  dp[3][3]=4

Subarrays of length 2:
  dp[0][1] = max(5-3, 3-5) = max(2,-2) = 2   → pick 5
  dp[1][2] = max(3-1, 1-3) = max(2,-2) = 2   → pick 3
  dp[2][3] = max(1-4, 4-1) = max(-3,3) = 3   → pick 4

Subarrays of length 3:
  dp[0][2] = max(5-dp[1][2], 1-dp[0][1]) = max(5-2, 1-2) = max(3,-1) = 3
  dp[1][3] = max(3-dp[2][3], 4-dp[1][2]) = max(3-3, 4-2) = max(0,2) = 2

Full array (length 4):
  dp[0][3] = max(5-dp[1][3], 4-dp[0][2]) = max(5-2, 4-3) = max(3,1) = 3

dp[0][3] = 3 ≥ 0 → Alice can always win!
```

```python
def stone_game_i(piles: list) -> bool:
    """Alice can always win with optimal play on even-length arrays"""
    n = len(piles)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = piles[i]  # Base: single pile
    # Fill by increasing subarray length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            # Take left: get piles[i], opponent plays optimally on [i+1..j]
            # Take right: get piles[j], opponent plays optimally on [i..j-1]
            dp[i][j] = max(piles[i] - dp[i + 1][j],
                           piles[j] - dp[i][j - 1])
    return dp[0][n - 1] >= 0  # Positive = Alice wins

# Time: O(n²), Space: O(n²) → can optimize to O(n) with rolling array
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

## Summary Table & Quick Reference

```
┌─────────────────────────┬──────────────────┬──────────┬──────────┬──────────────────────────────┐
│ Problem                 │ Approach         │ Time     │ Space    │ Key Insight                  │
├─────────────────────────┼──────────────────┼──────────┼──────────┼──────────────────────────────┤
│ Max Subarray            │ Kadane           │ O(n)     │ O(1)     │ cur = max(num, cur+num)      │
│ Max Circular Subarray   │ MinKadane + Total│ O(n)     │ O(1)     │ circular = total - min_sub   │
│ Max Product Subarray    │ Track max/min    │ O(n)     │ O(1)     │ Neg×Neg can flip sign        │
│ L Alternating Subseq    │ Track up/down    │ O(n)     │ O(1)     │ Two state variables          │
│ Max Pair Chain          │ Greedy (sort end)│ O(n logn)│ O(1)     │ Sort by end, greedy pick     │
│ L Bitonic Subseq        │ LIS left + right │ O(n²)    │ O(n)     │ Combine LIS from both sides  │
│ Egg Dropping            │ Minimax + BS     │ O(kn lgn)│ O(kn)    │ Binary search optimal floor  │
│ Word Break              │ String DP        │ O(n²L)   │ O(n)     │ dp[j] && s[j:i] in dict     │
│ Min Jumps / Jump Game II│ DP or Greedy BFS │ O(n)     │ O(1)     │ BFS level = one jump         │
│ Stone Game I            │ Interval Minimax │ O(n²)    │ O(n)     │ Take - opponent_best         │
│ Stone Game II           │ Suffix + DP      │ O(n³)    │ O(n²)    │ suffix sum + DP on M         │
└─────────────────────────┴──────────────────┴──────────┴──────────┴──────────────────────────────┘
```

### Pattern Checklist
- [ ] **Kadane pattern**: Single pass, track local + global optimum
- [ ] **Two-state tracking**: When sign flips matter (products, alternating)
- [ ] **Interval DP**: Game from ends → dp[i][j] over subarrays
- [ ] **Minimax**: Egg drop → worst case of best choices
- [ ] **String segmentation**: dp[i] = "can I reach position i?"
- [ ] **Greedy BFS**: Jump problems → think in BFS levels
