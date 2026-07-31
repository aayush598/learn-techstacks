# DP Practice Problems for Infosys SP DSE

25 carefully curated dynamic programming problems in order of difficulty. Every
problem below gets the full treatment: a plain-English problem explanation, a
precise state definition, the recurrence, base cases, the key intuition, a
step-by-step procedure, a worked dry run, fully commented code, complexity
analysis, and common pitfalls. All code is valid Python 3.

## Quick Pattern Reference for Practice

```text
┌──────────────────────────────────────────────────────────────────────────┐
│  Problem # → Pattern                                                   │
├──────────────────────────────────────────────────────────────────────────┤
│  1-3 (Easy)  → 1D DP, Fibonacci-style (build up from base cases)      │
│  4-8 (Medium)→ 2D DP, LIS, LCS, string comparison                     │
│  9-15 (Hard) → Interval DP, minimax, game theory, reverse DP           │
│  16-25 (SP L3)→ Bitmask DP, tree DP, advanced interval/string DP      │
└──────────────────────────────────────────────────────────────────────────┘

Before solving: ask yourself
  1. Is the problem asking for count, max/min, or yes/no?
  2. Are there choices at each step?
  3. Can I break the problem into overlapping subproblems?
  4. What state captures the necessary context?
```

---

## EASY

### 1. Climbing Stairs

**Problem Explanation:**
You are climbing a staircase with `n` steps to reach the top. At each step you
may climb either 1 step or 2 steps at a time. You need to return the total
number of distinct ways to reach the top. For example, with `n = 3` the ways
are `(1,1,1)`, `(1,2)`, `(2,1)`, so the answer is 3. Input is a single integer
`n`, output is a single integer (the count). This is the classic problem whose
answer follows the Fibonacci sequence.

**State Definition:**
`dp[i]` = number of distinct ways to reach step `i` (with `i` steps climbed
so far). We count from step 0 (the ground, already standing there) up to
step `n` (the top).

**Recurrence Relation:**
```
dp[i] = dp[i-1] + dp[i-2]
```
To stand on step `i`, your last move was either a 1-step climb from `i-1` or a
2-step climb from `i-2`. Every way of reaching `i-1` combined with a final
1-step move, plus every way of reaching `i-2` combined with a final 2-step
move, gives a distinct way of reaching `i`, so the two counts add.

**Base Cases:**
- `dp[0] = 1` (there is exactly 1 way to be on the ground: do nothing)
- `dp[1] = 1` (only the 1-step climb reaches step 1)

**Intuition (Why This Works):**
Each step's answer depends only on the two previous steps, so the whole
sequence can be built left-to-right in one pass. There is a "choice" at every
step (1-step or 2-step jump), and the count of ways to a state is the sum of
counts of ways to its predecessors. This is a count-type 1D DP with a
Fibonacci-shaped recurrence.

**Step-by-Step Procedure:**
1. Handle the small cases: if `n <= 1`, return 1.
2. Initialize two variables `a = 1` (representing `dp[0]`) and `b = 1`
   (representing `dp[1]`).
3. Loop `i` from 2 to `n` inclusive.
4. In each iteration compute the new value as `a + b`.
5. Slide the window: `a` takes the old `b`, `b` takes the new value.
6. After the loop, `b` holds `dp[n]`; return it.

**Worked Example (Dry Run):**
`n = 5`. We fill `dp[i]` step by step using `dp[i] = dp[i-1] + dp[i-2]`:

| i  | dp[i] | Explanation                          |
|----|-------|--------------------------------------|
| 0  | 1     | ground: 1 way (do nothing)           |
| 1  | 1     | 1 way: climb 1 step                  |
| 2  | 2     | 1+1=2: (1,1) and (2)                 |
| 3  | 3     | dp[2]+dp[1] = 2+1                    |
| 4  | 5     | dp[3]+dp[2] = 3+2                    |
| 5  | 8     | dp[4]+dp[3] = 5+3                    |

Final answer: `dp[5] = 8`.

**Code:**
```python
def climb_stairs(n):
    # Base case: 0 or 1 step has exactly 1 way.
    if n <= 1:
        return 1
    # Two variables track dp[i-2] and dp[i-1] (rolling Fibonacci).
    a, b = 1, 1  # a = dp[0], b = dp[1]
    for _ in range(2, n + 1):
        # dp[i] = dp[i-1] + dp[i-2]; then shift the window forward.
        a, b = b, a + b
    return b


def climb_stairs_memo(n, memo=None):
    # Top-down (memoized recursion): same recurrence, computed on demand.
    if memo is None:
        memo = {}
    if n <= 1:
        return 1
    if n in memo:          # subproblem already solved: reuse it
        return memo[n]
    # Last move was a 1-step or a 2-step jump, so the counts add.
    memo[n] = climb_stairs_memo(n - 1, memo) + climb_stairs_memo(n - 2, memo)
    return memo[n]
```

**Complexity:**
- Time: O(n) — one pass (memoized version is also O(n) over distinct states)
- Space: O(1) — two rolling variables (memoized version uses O(n) call stack)

**Common Mistakes & Edge Cases:**
- Forgetting that `n = 1` returns 1 (not 2).
- Confusing the ground (step 0, value 1) with step 1 when initializing.
- Using plain recursion without memoization, which blows up to O(2^n) because
  the same subproblem is recomputed exponentially many times.
- Off-by-one in the loop: it must run through `i = n` inclusive.
- Handling `n = 0`: the safe answer is 1 (one way: do nothing).

---

### 2. House Robber

**Problem Explanation:**
You are a robber along a street of houses. Each house `i` holds `nums[i]`
dollars. You cannot rob two adjacent houses (the security system alerts the
police if adjacent houses are hit on the same night). Return the maximum amount
of money you can rob without alerting the police. For example, with
`nums = [2, 7, 9, 3, 1]` the best plan is robbing houses 0, 2, 4 for
`2 + 9 + 1 = 12`. Input is the array `nums`, output is the max total.

**State Definition:**
`dp[i]` = maximum amount you can rob considering only houses `0..i`
(prefix of length `i + 1`).

**Recurrence Relation:**
```
dp[i] = max(dp[i-1], dp[i-2] + nums[i])
```
At house `i` there are exactly two choices: skip it (keep `dp[i-1]`, the best
from the previous prefix) or rob it (add `nums[i]` to `dp[i-2]`, the best from
two houses back, because house `i-1` must then be skipped). Take the maximum of
the two. This is correct because both choices are legal and every optimal plan
ends with either robbing or skipping house `i`.

**Base Cases:**
- With no houses: `dp[-1] = 0` (robbed nothing)
- With only house 0: `dp[0] = nums[0]`
- With only houses 0..1: `dp[1] = max(nums[0], nums[1])`

**Intuition (Why This Works):**
The only constraint is adjacency, so the state just needs one piece of
information: which prefix we have processed. At each house we make a binary
choice (rob or skip), and the two options only depend on the previous two
prefix answers. This yields a linear 1D DP solvable with just two rolling
variables.

**Step-by-Step Procedure:**
1. Initialize `prev2 = 0` (best up to two houses back) and `prev1 = 0`
   (best up to the previous house).
2. Loop over each house value `num` in `nums`.
3. Compute `curr = max(prev1, prev2 + num)` (skip vs rob).
4. Slide the window: `prev2 = prev1`, `prev1 = curr`.
5. After the loop, return `prev1`.

**Worked Example (Dry Run):**
`nums = [2, 7, 9, 3, 1]`. We track `(prev2, prev1, curr)` at each house:

| house | num | prev2 | prev1 | curr = max(prev1, prev2+num) | meaning                              |
|-------|-----|-------|-------|------------------------------|--------------------------------------|
| 0     | 2   | 0     | 0     | max(0, 0+2)=2                | rob house 0 → 2                     |
| 1     | 7   | 0     | 2     | max(2, 0+7)=7                | rob house 1 → 7                     |
| 2     | 9   | 2     | 7     | max(7, 2+9)=11               | rob 0 and 2 → 2+9=11                |
| 3     | 3   | 7     | 11    | max(11, 7+3)=11              | skip 3, keep 11                     |
| 4     | 1   | 11    | 11    | max(11, 11+1)=12             | rob 0, 2, 4 → 2+9+1=12              |

Final answer: `12` (rob houses 0, 2, 4).

**Code:**
```python
def rob(nums):
    # prev1 = best amount after considering the previous house
    # prev2 = best amount after considering the house before that
    prev2 = prev1 = 0
    for num in nums:
        # Choice A: rob this house -> prev2 + num (previous house is skipped).
        # Choice B: skip this house -> keep prev1.
        curr = max(prev1, prev2 + num)
        # Slide the two-variable window forward.
        prev2, prev1 = prev1, curr
    return prev1
```

**Complexity:**
- Time: O(n) — single pass over the houses
- Space: O(1) — two rolling variables

**Common Mistakes & Edge Cases:**
- Empty input `nums = []`: must return 0 (the code does, since the loop never
  runs and `prev1` stays 0).
- Single house `nums = [5]`: answer is 5, not 0 or 10.
- Using `prev1 + num` (robbing adjacent houses) instead of `prev2 + num`.
- Two houses `[1, 2]`: answer is `max(1, 2) = 2`; robbing both is illegal.
- All-negative amounts do not occur (money is non-negative), but if they did,
  the "skip" option correctly keeps the max from earlier houses.

---

### 3. Min Cost Climbing Stairs

**Problem Explanation:**
You stand on the floor below a staircase. There is an integer array `cost`
where `cost[i]` is the price you pay when you step onto stair `i`. You may
start on stair 0 or stair 1 (for free), and from any stair you may climb 1 or
2 steps. The "top" is one step beyond the last stair. Return the minimum total
cost to reach the top. For example, with `cost = [10, 15, 20]` the cheapest
way is to start on stair 1 (15) and jump 2 steps straight to the top, total 15.
Input is the array `cost`, output is the min total cost.

**State Definition:**
`dp[i]` = minimum total cost paid so far when you are standing on stair `i`
(you must pay `cost[i]` to stand there).

**Recurrence Relation:**
```
dp[i] = cost[i] + min(dp[i-1], dp[i-2])
```
You can arrive at stair `i` only from stair `i-1` (1-step climb) or stair
`i-2` (2-step climb), paying the cheaper of those two accumulated costs plus
the cost of stair `i` itself. Correct because those are the only two possible
previous positions and every optimal route to `i` passes through exactly one
of them.

**Base Cases:**
- `dp[0] = cost[0]` (start on stair 0, pay its cost)
- `dp[1] = cost[1]` (start on stair 1, pay its cost)

**Final answer:**
`min(dp[n-2], dp[n-1])` — the top is reached by stepping off from stair `n-1`,
or by jumping over stair `n-1` from stair `n-2`.

**Intuition (Why This Works):**
Each stair's minimum cost depends only on the two stairs below it, so a single
left-to-right pass with two rolling variables suffices. The "choice" at each
stair is which of the two lower stairs you came from; we always keep the
cheaper one because the future cost does not depend on anything else.

**Step-by-Step Procedure:**
1. Handle empty/singleton inputs (return 0 / `cost[0]`).
2. Set `a = cost[0]` and `b = cost[1]` (`a` = dp up to two stairs below,
   `b` = dp of the stair below the current one).
3. Loop `i` from 2 to `len(cost) - 1`.
4. Compute the cost of stair `i` as `cost[i] + min(a, b)`.
5. Slide the window: `a = b`, `b = new value`.
6. After the loop, return `min(a, b)`.

**Worked Example (Dry Run):**
`cost = [1, 100, 1, 1, 1]`. The two-variable state `(a, b)` tracks the last
two `dp` values.

| step | i  | state before  | computation                          | dp[i] |
|------|----|---------------|--------------------------------------|-------|
| base | -  | a=1, b=100    | dp[0]=1, dp[1]=100                   | -     |
| 1    | 2  | a=1, b=100    | cost[2]+min(a,b) = 1+min(1,100)=2    | 2     |
| 2    | 3  | a=100, b=2    | cost[3]+min(a,b) = 1+min(100,2)=3    | 3     |
| 3    | 4  | a=2, b=3      | cost[4]+min(a,b) = 1+min(2,3)=3      | 3     |

Final answer: `min(dp[3], dp[4]) = min(3, 3) = 3` (start at stair 0, go
0 → 2 → 3, then jump 2 steps over stair 4 to the top).

**Code:**
```python
def min_cost_climbing(cost):
    if not cost:
        return 0
    if len(cost) == 1:
        return cost[0]
    # a = min cost to reach the stair two below the current one,
    # b = min cost to reach the stair directly below.
    a, b = cost[0], cost[1]
    for i in range(2, len(cost)):
        # To stand on stair i we pay cost[i] plus the cheaper way of coming
        # from one stair below (b) or two stairs below (a).
        a, b = b, cost[i] + min(a, b)
    # The top is past the last stair: step off from n-1 (b) or jump over it
    # from n-2 (a); pick the cheaper.
    return min(a, b)
```

**Complexity:**
- Time: O(n) — single pass over the cost array
- Space: O(1) — two rolling variables

**Common Mistakes & Edge Cases:**
- Forgetting that you may START on stair 1 for free; this is captured by the
  base case `dp[1] = cost[1]`.
- The final answer is `min` of the last two dp values, not `dp[n-1]` alone
  (you can jump over the last stair).
- An empty or single-element array crashes naive `cost[0]`/`cost[1]` reads;
  guard the inputs.
- Misdining the recurrence as `cost[i] + min(dp[i-1], dp[i-2])` over all pairs
  of previously computed values instead of rolling two variables — the rolling
  version is equivalent and uses O(1) space.
- `cost = [10, 15]` → answer is `min(10, 15) = 10` (start on stair 0 and jump
  both steps to the top).
---

## MEDIUM

### 4. Longest Increasing Subsequence

**Problem Explanation:**
Given an array of integers `nums`, find the length of the longest strictly
increasing subsequence. A subsequence is a sequence you get by deleting some
(or zero) elements without changing the order of the rest. For example, with
`nums = [10, 9, 2, 5, 3, 7, 101, 18]` the longest increasing subsequence is
`[2, 3, 7, 101]` (or `[2, 3, 7, 18]`), length 4. Input is the array `nums`,
output is the integer length.

**State Definition:**
`dp[i]` = length of the longest increasing subsequence that ENDS at index `i`
(with `nums[i]` as its last element).

**Recurrence Relation:**
```
dp[i] = 1 + max(dp[j])  for all j < i with nums[j] < nums[i]
       (or 1 if no such j exists)
```
Any increasing subsequence ending at `i` is formed by appending `nums[i]` to
an increasing subsequence ending at some earlier `j` whose last value is
smaller. To maximize the result we take the longest such predecessor. This is
correct because appending `nums[i]` keeps the sequence strictly increasing
exactly when `nums[j] < nums[i]`.

**Base Cases:**
- `dp[i] = 1` for every `i` (each element alone is an increasing subsequence of
  length 1)

**Final answer:**
`max(dp)` — the longest subsequence can end at any index.

**Intuition (Why This Works):**
The length of the best subsequence ending at `i` only depends on the best
subsequence lengths at earlier positions — a classic optimal-substructure
property. The "choice" at each `i` is which earlier element `j` to extend
(or start fresh). An O(n log n) alternative called patience sorting exists: it
maintains piles whose tops are the smallest possible ending values for each
subsequence length, so longer tails can never be extended by smaller numbers.

**Step-by-Step Procedure:**
Both algorithms below solve the problem correctly; use the O(n log n) version
for large inputs, the O(n^2) version when you also need the sequence itself.

Procedure A — O(n^2) DP:
1. If `nums` is empty, return 0.
2. Create `dp = [1] * n` (every element alone is length 1).
3. Loop `i` over all indices.
4. Loop `j` from 0 to `i - 1`.
5. If `nums[j] < nums[i]`, update `dp[i] = max(dp[i], dp[j] + 1)`.
6. After both loops, return `max(dp)`.

Procedure B — O(n log n) patience sorting:
1. Create an empty list `piles`.
2. For each `num`, use binary search (`bisect_left`) to find the first pile
   top that is >= `num`.
3. If no such pile exists, append `num` to `piles` (a new, longer subsequence
   is possible).
4. Otherwise replace that pile top with `num` (a smaller ending is more
   flexible for future extensions).
5. Return `len(piles)`.

**Worked Example (Dry Run):**
`nums = [10, 9, 2, 5, 3, 7, 101, 18]`.

O(n^2) DP table:

| i | nums[i] | candidates (j where nums[j]<nums[i]) | dp[i] |
|---|---------|--------------------------------------|-------|
| 0 | 10      | none                                 | 1     |
| 1 | 9       | none                                 | 1     |
| 2 | 2       | none                                 | 1     |
| 3 | 5       | j=2 (2<5): dp[2]+1 = 2               | 2     |
| 4 | 3       | j=2 (2<3): dp[2]+1 = 2               | 2     |
| 5 | 7       | j=3 (5<7): 3; j=4 (3<7): 3           | 3     |
| 6 | 101     | j=5 (7<101): 4                       | 4     |
| 7 | 18      | j=5 (7<18): 4                        | 4     |

Answer: `max(dp) = 4`.

Patience sorting trace (`piles` after each number):

| num | piles after          | action                              |
|-----|----------------------|-------------------------------------|
| 10  | [10]                 | new pile                            |
| 9   | [9]                  | replace 10 with 9                   |
| 2   | [2]                  | replace 9 with 2                    |
| 5   | [2, 5]               | append: LIS length now 2            |
| 3   | [2, 3]               | replace 5 with 3                    |
| 7   | [2, 3, 7]            | append: length 3                    |
| 101 | [2, 3, 7, 101]       | append: length 4                    |
| 18  | [2, 3, 7, 18]        | replace 101 with 18 (keeps length)  |

Answer: `len(piles) = 4`.

**Code:**
```python
def length_of_lis_dp(nums):
    # Approach 1 -- O(n^2) DP.
    n = len(nums)
    if n == 0:
        return 0
    # dp[i] = length of the longest increasing subsequence ENDING at index i.
    dp = [1] * n  # every element alone is an increasing subsequence of length 1
    for i in range(n):
        for j in range(i):
            # nums[j] can be the predecessor of nums[i] only if it is smaller.
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    # The best subsequence may end anywhere, so take the overall max.
    return max(dp)


def length_of_lis(nums):
    # Approach 2 -- O(n log n) patience sorting.
    import bisect
    piles = []
    for num in nums:
        # bisect_left finds the first pile top that is >= num.
        i = bisect.bisect_left(piles, num)
        if i == len(piles):
            piles.append(num)  # no such pile: this num extends the longest tail
        else:
            # Replace that pile's top: a smaller ending is strictly better,
            # because it can extend any future number the old top could.
            piles[i] = num
    return len(piles)
```

**Complexity:**
- Time: O(n^2) for the DP version, O(n log n) for patience sorting
- Space: O(n) for the `dp`/`piles` array

**Common Mistakes & Edge Cases:**
- The subsequence is not necessarily contiguous — do not look only at the
  previous element.
- Strictly increasing means `nums[j] < nums[i]`, not `<=`; duplicates cannot
  extend each other.
- An empty array must return 0 (guard `max` on an empty list).
- Patience sorting's piles do NOT directly give the subsequence, only its
  length; reconstructing the actual sequence needs extra bookkeeping.
- `bisect_right` instead of `bisect_left` breaks strictly-increasing handling
  because it would treat equal values as extendable.

---

### 5. Coin Change

**Problem Explanation:**
Given an array `coins` of coin denominations (unlimited supply of each) and an
integer `amount`, return the minimum number of coins needed to make up exactly
`amount`. If the amount cannot be made, return `-1`. For example, with
`coins = [1, 2, 5]` and `amount = 11`, the answer is 3 (`5 + 5 + 1`). Input is
the coin list and the target amount; output is the minimum count or `-1`.

**State Definition:**
`dp[a]` = minimum number of coins needed to make exactly amount `a`.

**Recurrence Relation:**
```
dp[a] = min over all coins c of (dp[a - c] + 1), for c <= a
```
To make amount `a`, pick any coin `c` as the LAST coin added; the rest of the
amount `a - c` must be made optimally, and we add 1 for this coin. Taking the
min over all coins gives the best count. This is correct because every optimal
solution has a last coin, and the prefix before it must itself be optimal.

**Base Cases:**
- `dp[0] = 0` (amount 0 needs 0 coins)
- `dp[a] = infinity` for all other `a` initially (unreachable until improved)

**Intuition (Why This Works):**
This is the unbounded knapsack flavor of DP: each coin can be reused any number
of times. Looping coins on the outside and amounts left-to-right on the inside
lets the same coin be picked repeatedly (`dp[a - c]` may already include coin
`c`). The "choice" at each amount is which coin is added last, and the number
of coins used is naturally minimized by the `min` operation.

**Step-by-Step Procedure:**
1. Create `dp = [inf] * (amount + 1)`.
2. Set `dp[0] = 0`.
3. Loop over each `coin`.
4. Loop `a` from `coin` to `amount` (left-to-right, so coins are reusable).
5. Update `dp[a] = min(dp[a], dp[a - coin] + 1)`.
6. After all coins, return `dp[amount]` if it is finite, else `-1`.

**Worked Example (Dry Run):**
`coins = [1, 2, 5]`, `amount = 11`. After each coin pass the full `dp` array
(`index: value`) is:

| index  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|--------|---|---|---|---|---|---|---|---|---|---|----|----|
| after coin 1 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
| after coin 2 | 0 | 1 | 1 | 2 | 2 | 3 | 3 | 4 | 4 | 5 | 5  | 6  |
| after coin 5 | 0 | 1 | 1 | 2 | 2 | 1 | 2 | 2 | 3 | 3 | 2  | 3  |

Reading the last row: `dp[6] = 2` means 6 = 5 + 1 (two coins), `dp[10] = 2`
means 10 = 5 + 5, `dp[11] = 3` means 11 = 5 + 5 + 1. Final answer: `3`.

**Code:**
```python
def coin_change(coins, amount):
    # dp[a] = minimum number of coins needed to make exactly amount a.
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0  # zero coins make amount zero
    for coin in coins:
        # Loop left-to-right so the SAME coin can be reused (unbounded knapsack).
        for a in range(coin, amount + 1):
            # Use this coin as the last one: 1 coin plus the best for a - coin.
            dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != float("inf") else -1
```

**Complexity:**
- Time: O(n * amount), where n is the number of coin types
- Space: O(amount)

**Common Mistakes & Edge Cases:**
- `amount = 0` returns 0 (the empty combination), not `-1`.
- An unreachable amount stays `inf`; returning raw `inf` instead of `-1` is a
  classic bug.
- Greedy (always take the largest coin) does NOT work in general:
  `coins = [1, 3, 4]`, `amount = 6` → greedy gives `4 + 1 + 1` (3 coins), DP
  gives `3 + 3` (2 coins).
- Looping amounts right-to-left would convert this to a 0/1 knapsack and
  forbid reusing coins — the direction matters for "unlimited supply".
- If `dp[a - coin]` is `inf`, adding 1 keeps it `inf`, so no overflow worry
  when using Python floats.

---

### 6. Word Break

**Problem Explanation:**
Given a string `s` and a dictionary `word_dict` of words, determine whether `s`
can be segmented into a space-separated sequence of one or more dictionary
words. You may reuse dictionary words. For example, `s = "leetcode"` with
`word_dict = ["leet", "code"]` returns `True` because "leet code" splits it.
Input is the string and the word list; output is a boolean.

**State Definition:**
`dp[i]` = `True` if the prefix `s[0:i]` (first `i` characters) can be
segmented into dictionary words.

**Recurrence Relation:**
```
dp[i] = True if there exists j < i such that dp[j] is True AND s[j:i] is a word
```
Some valid segmentation of `s[0:i]` ends with the word `s[j:i]`; everything
before it (`s[0:j]`) must itself be segmentable. This is correct because a
segmentation is a chain of words, and any suffix word can only be appended to
a segmentable prefix.

**Base Cases:**
- `dp[0] = True` (the empty prefix is trivially segmented)

**Final answer:**
`dp[n]` where `n = len(s)`.

**Intuition (Why This Works):**
The problem is a yes/no "can it be built" DP. The only context needed is how
many characters of `s` we have consumed, so a 1D boolean array works. The
"choice" is the split point `j`: we try every way to take one word off the end
and check whether the remaining prefix is segmentable. Using a hash set for the
dictionary makes each membership check O(1).

**Step-by-Step Procedure:**
1. Convert `word_dict` to a set for O(1) membership checks.
2. Create `dp = [False] * (n + 1)` and set `dp[0] = True`.
3. Loop `i` from 1 to `n` (the prefix length being checked).
4. Loop `j` from 0 to `i - 1` (the split point).
5. If `dp[j]` is True and `s[j:i]` is in the set, set `dp[i] = True` and break.
6. Return `dp[n]`.

**Worked Example (Dry Run):**
`s = "leetcode"`, `word_dict = ["leet", "code"]`. Word list as a set.

| i | prefix s[0:i] | checks                             | dp[i] |
|---|---------------|------------------------------------|-------|
| 0 | ""            | base                               | True  |
| 1 | "l"           | j=0: "l" not in set                | False |
| 2 | "le"          | j=0 "le" no; j=1 "e" no            | False |
| 3 | "lee"         | "lee", "ee", "e" — none in set     | False |
| 4 | "leet"        | j=0: "leet" in set and dp[0]=True  | True  |
| 5 | "leetc"       | j=0 no; ... j=4: dp[4]=True but "c" not in set | False |
| 6 | "leetco"      | ... j=4: "co" not in set           | False |
| 7 | "leetcod"     | ... j=4: "cod" not in set          | False |
| 8 | "leetcode"    | j=4: dp[4]=True and "code" in set  | True  |

Final answer: `dp[8] = True`.

**Code:**
```python
def word_break(s, word_dict):
    words = set(word_dict)  # O(1) membership test per word
    n = len(s)
    # dp[i] = True if the prefix s[0:i] can be segmented into dictionary words.
    dp = [False] * (n + 1)
    dp[0] = True  # empty prefix is trivially segmentable
    for i in range(1, n + 1):
        for j in range(i):
            # A valid split: s[0:j] is segmentable AND s[j:i] is a word.
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break  # one good split is enough
    return dp[n]
```

**Complexity:**
- Time: O(n^2) substring checks (each substring is sliced; slicing is O(n), so
  a strict bound is O(n^3), but with typical small words it behaves as O(n^2))
- Space: O(n) for the dp array plus O(d) for the word set

**Common Mistakes & Edge Cases:**
- `dp` must have length `n + 1`; index `n` is the full string, and the empty
  prefix needs index 0.
- Forgetting to convert the dictionary to a set makes each check O(len(dict)).
- Reusing the same word is allowed, so the set lookup is sufficient (no
  consumption tracking needed).
- Empty string `s = ""`: `dp[0] = True`, answer `True` (guard for this if the
  problem forbids it).
- Whole word check: if the entire string is one word, `j = 0` with `dp[0]`
  catches it.

---

### 7. Unique Paths

**Problem Explanation:**
A robot sits at the top-left cell of an `m x n` grid. It can only move right or
down, one cell at a time. Return the number of distinct paths from the top-left
cell to the bottom-right cell. For example, on a `3 x 4` grid there are 10
distinct paths. Input is the two integers `m` (rows) and `n` (columns); output
is the path count.

**State Definition:**
`dp[i][j]` = number of distinct paths from the start cell to cell `(i, j)`.

**Recurrence Relation:**
```
dp[i][j] = dp[i-1][j] + dp[i][j-1]
```
The last move into cell `(i, j)` was either a step down from `(i-1, j)` or a
step right from `(i, j-1)`; every path to those neighbors extends to a unique
path to `(i, j)`, so the counts add. This is correct because those are the only
two possible predecessors.

**Base Cases:**
- The first row: `dp[0][j] = 1` for all `j` (only rightward moves possible)
- The first column: `dp[i][0] = 1` for all `i` (only downward moves possible)
- `dp[0][0] = 1`

**Intuition (Why This Works):**
Every cell is only reachable from two cells (above and left), so the grid can
be filled top-to-bottom, left-to-right and each cell depends only on already
computed values. Since we only ever need the previous row, a single 1D array
can hold the current row, giving O(n) space instead of O(m*n).

**Step-by-Step Procedure:**
1. Initialize `dp = [1] * n` (this represents the first row: all 1s).
2. Loop over rows 1 to `m - 1`.
3. Loop `j` from 1 to `n - 1`.
4. Update `dp[j] += dp[j - 1]` — the old `dp[j]` is "from above", `dp[j-1]` is
   "from the left".
5. After all rows, return `dp[-1]`.

**Worked Example (Dry Run):**
`m = 3`, `n = 4`. The rolling 1D array after each row (values equal to the full
2D table):

| row | dp after processing | explanation                                     |
|-----|---------------------|-------------------------------------------------|
| 0   | [1, 1, 1, 1]        | first row: only rightward moves                 |
| 1   | [1, 2, 3, 4]        | each cell = above + left: 2=1+1, 3=2+1, 4=3+1   |
| 2   | [1, 3, 6, 10]       | 3=2+1, 6=3+3, 10=4+6                           |

Final answer: `dp[-1] = 10`.

**Code:**
```python
def unique_paths(m, n):
    # dp[j] = number of paths to the current row's column j.
    # Row 0 is all 1s: from the left edge every cell has exactly one path.
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            # dp[j] (old value) counts paths from ABOVE,
            # dp[j-1] (already updated) counts paths from the LEFT.
            dp[j] += dp[j - 1]
    return dp[-1]
```

**Complexity:**
- Time: O(m * n)
- Space: O(n) (rolling row) — O(m * n) for the full table version

**Common Mistakes & Edge Cases:**
- `1 x 1` grid: exactly 1 path (the robot is already there).
- `m = 1` or `n = 1`: exactly 1 path (only one direction possible).
- Off-by-one when building the row: the first column stays 1 forever.
- Using combinations math (`C(m+n-2, m-1)`) is valid but overflows long
  integers for big grids unless computed carefully.
- Rolling-array bug: updating `dp[0]` would break the "1" in the first column.

---

### 8. Longest Common Subsequence

**Problem Explanation:**
Given two strings `text1` and `text2`, return the length of their longest
common subsequence. A subsequence is a sequence obtainable by deleting some
characters without reordering the rest. For example, `text1 = "abcde"` and
`text2 = "ace"` have the common subsequence "ace", length 3. Input is the two
strings; output is the integer length.

**State Definition:**
`dp[i][j]` = length of the longest common subsequence of the prefixes
`text1[:i]` and `text2[:j]`.

**Recurrence Relation:**
```
if text1[i-1] == text2[j-1]:  dp[i][j] = dp[i-1][j-1] + 1
else:                         dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```
If the last characters match, they must be paired in any LCS of the full
prefixes (pairing them can never hurt), extending the LCS of the shorter
prefixes. If they differ, at least one of the two characters is not in the
LCS, so the answer is the best of dropping either one. Correct by the classic
optimal-substructure argument for string DP.

**Base Cases:**
- `dp[0][j] = 0` for all `j` (empty first prefix shares nothing)
- `dp[i][0] = 0` for all `i` (empty second prefix shares nothing)

**Intuition (Why This Works):**
At each cell we compare one character from each string and make a decision:
pair them (if equal) or discard one of them (if different). The optimal choice
only depends on smaller prefix pairs, so filling a 2D table in row-major order
builds the answer from small to large. This is the canonical 2D string-DP
template reused by edit distance and similar problems.

**Step-by-Step Procedure:**
1. Let `m = len(text1)`, `n = len(text2)`.
2. Create `dp` as an `(m+1) x (n+1)` table of zeros (row/col 0 are base cases).
3. Loop `i` from 1 to `m`.
4. Loop `j` from 1 to `n`.
5. If `text1[i-1] == text2[j-1]`, set `dp[i][j] = dp[i-1][j-1] + 1`.
6. Else set `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.
7. Return `dp[m][n]`.

**Worked Example (Dry Run):**
`text1 = "abcde"`, `text2 = "ace"`. Rows are characters of "abcde", columns
are characters of "ace", with an empty "" row and column:

|     | "" | a | c | e |
|-----|----|---|---|---|
| ""  | 0  | 0 | 0 | 0 |
| a   | 0  | 1 | 1 | 1 |
| b   | 0  | 1 | 1 | 1 |
| c   | 0  | 1 | 2 | 2 |
| d   | 0  | 1 | 2 | 2 |
| e   | 0  | 1 | 2 | 3 |

- `dp[1][1] = 1`: "a" and "a" match → 0 + 1.
- `dp[3][2] = 2`: "abc" and "ac" → "c" matches, diagonal + 1.
- `dp[5][3] = 3`: "abcde" and "ace" → "e" matches, diagonal + 1.

Final answer: `dp[5][3] = 3`.

**Code:**
```python
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    # dp[i][j] = LCS length of prefixes text1[:i] and text2[:j].
    # The extra 0-th row/column encode the empty-prefix base cases.
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                # Matching characters: extend the LCS of the shorter prefixes.
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # Characters differ: keep the best of dropping either one.
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
```

**Complexity:**
- Time: O(m * n)
- Space: O(m * n) for the full table (O(min(m, n)) with a rolling row)

**Common Mistakes & Edge Cases:**
- Indexing: `text1[i - 1]` compares the `i`-th character; off-by-one here is
  the most common bug.
- The table needs `(m+1) x (n+1)` cells so the empty-prefix row/column exist.
- On mismatch, use `max`, not `min`.
- The subsequence is not contiguous — do not restrict to substrings.
- Empty string: if `text1 = ""`, the answer is 0 (handled by base row/column).
---

## HARD

### 9. Burst Balloons

**Problem Explanation:**
You are given `nums`, an array of balloons, each with a number on it. If you
burst balloon `i`, you collect `nums[i-1] * nums[i] * nums[i+1]` coins (using
the still-alive neighboring balloons; out-of-range neighbors count as 1).
Return the maximum coins you can collect by bursting all balloons in any order.
For example, `nums = [3, 1, 5, 8]` gives 167. Input is the array; output is
the max coins.

**State Definition:**
Pad the array with sentinels of value 1: `nums' = [1] + nums + [1]`. Then
`dp[i][j]` = maximum coins obtainable from bursting every balloon strictly
between positions `i` and `j` (the balloons at `i` and `j` are NOT burst, they
just act as fixed neighbors).

**Recurrence Relation:**
```
dp[i][j] = max over k in (i, j) of:
           nums[i] * nums[k] * nums[j] + dp[i][k] + dp[k][j]
```
Think backwards: pick balloon `k` as the LAST one to burst in the open interval
`(i, j)`. When `k` bursts, everything between `i` and `j` is already gone, so
its neighbors are exactly `i` and `j`. Before that, the two halves `(i, k)` and
`(k, j)` are burst optimally and independently. Trying every `k` and taking the
max explores all burst orders implicitly. This is correct because the last
balloon splits the problem into two independent subproblems.

**Base Cases:**
- `dp[i][i] = 0` and `dp[i][i+1] = 0` (no balloons strictly between)

**Final answer:**
`dp[0][n - 1]` where `n` is the length of the padded array.

**Intuition (Why This Works):**
Forward thinking (which balloon to burst first) is hard because the order
changes everyone's neighbors. Reversing the process — deciding which balloon
bursts LAST — fixes its neighbors as the fixed boundaries `i` and `j`, which
makes the subproblems independent. That reversal turns the problem into a clean
interval DP where we fill by increasing interval length.

**Step-by-Step Procedure:**
1. Pad: `nums = [1] + nums + [1]`; let `n = len(nums)`.
2. Create `dp` as an `n x n` zero table.
3. Loop `length` from 2 to `n - 1` (interval size).
4. Loop `i` from 0 to `n - length - 1`; set `j = i + length`.
5. Loop `k` from `i + 1` to `j - 1` (candidate last balloon).
6. Update `dp[i][j] = max(dp[i][j], nums[i]*nums[k]*nums[j] + dp[i][k] + dp[k][j])`.
7. Return `dp[0][n - 1]`.

**Worked Example (Dry Run):**
`nums = [3, 1, 5, 8]` → padded `[1, 3, 1, 5, 8, 1]` (indices 0..5). We fill
intervals by increasing length, showing only the interesting states:

| interval | computed value |
|----------|----------------|
| dp[0][2]: k=1 | 1*3*1 = 3 |
| dp[1][3]: k=2 | 3*1*5 = 15 |
| dp[2][4]: k=3 | 1*5*8 = 40 |
| dp[3][5]: k=4 | 5*8*1 = 40 |
| dp[1][4]: k=3 (best) | 3*5*8 + dp[1][3](15) + 0 = 135 |
| dp[0][3]: k=1 (best) | 1*3*5 + 0 + dp[1][3](15) = 30 |
| dp[0][4]: k=1 (best) | 1*3*8 + 0 + dp[1][4](135) = 159 |
| dp[1][5]: k=4 (best) | 3*8*1 + dp[1][4](135) + 0 = 159 |
| dp[0][5]: k=4 (best) | 1*8*1 + dp[0][4](159) + 0 = 167 |

Final answer: `dp[0][5] = 167` (burst order 1 → 5 → 3 → 8).

**Code:**
```python
def max_coins(nums):
    # Pad with 1s so boundary balloons always have two neighbors.
    nums = [1] + nums + [1]
    n = len(nums)
    # dp[i][j] = max coins from bursting every balloon STRICTLY between i and j.
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):        # grow the interval one at a time
        for i in range(n - length):   # left boundary index
            j = i + length            # right boundary index
            for k in range(i + 1, j): # k = the LAST balloon burst in (i, j)
                # When k bursts, i and j are its neighbors; the halves (i,k)
                # and (k,j) have already been cleared optimally.
                dp[i][j] = max(dp[i][j],
                    nums[i] * nums[k] * nums[j] + dp[i][k] + dp[k][j])
    return dp[0][n - 1]
```

**Complexity:**
- Time: O(n^3) — three nested loops over the padded size
- Space: O(n^2) for the dp table

**Common Mistakes & Edge Cases:**
- Forgetting to pad with 1s, which forces messy boundary conditionals.
- Treating the sentinels as burstable balloons (they must never be in the
  answer computation as a "last balloon").
- Single balloon `nums = [5]`: padded `[1, 5, 1]`, answer `1*5*1 = 5`.
- The recurrence uses `dp[i][k] + dp[k][j]` (k is excluded from both halves),
  NOT `dp[i][k] + dp[k+1][j]`.
- Burst order matters, so a greedy "always pick smallest" approach is wrong.

---

### 10. Edit Distance

**Problem Explanation:**
Given two strings `word1` and `word2`, return the minimum number of operations
to convert `word1` into `word2`. The allowed operations are: insert a character
(anywhere), delete a character, or replace a character with another. For
example, `word1 = "horse"`, `word2 = "ros"` takes 3 operations (replace 'h'
with 'r', delete 'r' at index 1... or equivalently replace + 2 deletes). Input
is the two strings; output is the minimum operation count.

**State Definition:**
`dp[i][j]` = minimum number of operations to convert the prefix `word1[:i]`
into the prefix `word2[:j]`.

**Recurrence Relation:**
```
if word1[i-1] == word2[j-1]:  dp[i][j] = dp[i-1][j-1]
else:                         dp[i][j] = 1 + min(dp[i-1][j],      # delete word1[i-1]
                                                  dp[i][j-1],      # insert word2[j-1]
                                                  dp[i-1][j-1])    # replace
```
If the last characters match, no operation is needed on them. If they differ,
the last operation must be one of the three: delete `word1[i-1]` (then convert
`word1[:i-1]` to `word2[:j]`), insert `word2[j-1]` (then convert `word1[:i]`
to `word2[:j-1]`), or replace `word1[i-1]` with `word2[j-1]` (then convert the
remaining prefixes). We take the cheapest. This is correct because any optimal
transformation has some well-defined last operation.

**Base Cases:**
- `dp[0][j] = j` (insert all `j` characters of `word2`)
- `dp[i][0] = i` (delete all `i` characters of `word1`)

**Intuition (Why This Works):**
Like LCS, we compare one character from each string at a time, but here a
mismatch has three distinct remedies instead of one max. The optimal choice
only depends on three neighboring cells, so a full table (or two rolling rows)
can be filled row by row. The three options are exactly the three allowed
operations, which is why the recurrence is complete.

**Step-by-Step Procedure:**
1. Let `m = len(word1)`, `n = len(word2)`.
2. Create `prev = list(range(n + 1))` (row 0: j inserts to build word2[:j]).
3. Loop `i` from 1 to `m`.
4. Create `curr` with `curr[0] = i` (i deletes to empty word2).
5. Loop `j` from 1 to `n`.
6. Apply the match/three-op recurrence using `prev` (previous row) and `curr`.
7. After the loop, assign `prev = curr`.
8. Return `prev[n]`.

**Worked Example (Dry Run):**
`word1 = "horse"`, `word2 = "ros"`. Full table (rows = chars of "horse", cols
= chars of "ros"):

|     | "" | r | o | s |
|-----|----|---|---|---|
| ""  | 0  | 1 | 2 | 3 |
| h   | 1  | 1 | 2 | 3 |
| o   | 2  | 2 | 1 | 2 |
| r   | 3  | 2 | 2 | 2 |
| s   | 4  | 3 | 3 | 2 |
| e   | 5  | 4 | 4 | 3 |

Highlights: `dp[2][2] = 1` ("ho" → "ro": replace 'h' with 'r'); `dp[4][3] = 2`
("hors" → "ros": delete 'h', replace 'r'... i.e. 2 ops). Final answer:
`dp[5][3] = 3`.

**Code:**
```python
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    # Rolling single-row version of dp[i][j].
    prev = list(range(n + 1))  # row 0: turning "" into word2[:j] needs j inserts
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        curr[0] = i            # turning word1[:i] into "" needs i deletes
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]  # matching chars: no operation needed
            else:
                # Cheapest last operation among:
                #   prev[j]     -> delete word1[i-1]
                #   curr[j - 1] -> insert word2[j-1]
                #   prev[j - 1] -> replace word1[i-1] with word2[j-1]
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev = curr
    return prev[n]
```

**Complexity:**
- Time: O(m * n)
- Space: O(n) with the rolling row (O(m * n) for the full table)

**Common Mistakes & Edge Cases:**
- One string empty: the answer is the other string's length (base rows handle
  it).
- The three operations must ALL be considered on a mismatch; forgetting the
  "replace" option (diagonal) is a classic error.
- On a match, copying `dp[i-1][j-1]` is right even if a cheaper alternative
  existed, because matching characters always pair together in an optimal edit
  script.
- Off-by-one when comparing `word1[i - 1]` with `word2[j - 1]`.
- Swap of `prev`/`curr` references corrupts the rolling table; assign
  `prev = curr` only after the full row is done.

---

### 11. Regular Expression Matching

**Problem Explanation:**
Given a string `s` and a pattern `p`, return `True` if the pattern matches the
entire string. The pattern supports two special characters: `.` matches any
single character, and `*` matches zero or more of the character that precedes
it (that preceding character must be a letter or `.`). For example,
`s = "aab"`, `p = "c*a*b"` is `True` (c* matches zero 'c's, a* matches "aa",
b matches "b"). Input is the two strings; output is a boolean.

**State Definition:**
`dp[i][j]` = `True` if the prefix `s[:i]` matches the pattern prefix `p[:j]`.

**Recurrence Relation:**
```
if p[j-1] == s[i-1] or p[j-1] == '.':  dp[i][j] = dp[i-1][j-1]
elif p[j-1] == '*':
    dp[i][j] = dp[i][j-2]                                # zero occurrences
    if p[j-2] == s[i-1] or p[j-2] == '.':                # one or more
        dp[i][j] = dp[i][j] or dp[i-1][j]
```
A plain character consumes one char from each side. A `*` can either match
zero of its preceding character (skip both `p[j-2]` and `p[j-1]`, keeping
`dp[i][j-2]`), or match one more occurrence of that character (the previous
string char matched, so `dp[i-1][j]` already holds). This is correct because
`*` is the only construct with a variable count, and its two behaviors cover
all possibilities.

**Base Cases:**
- `dp[0][0] = True` (empty string matches empty pattern)
- `dp[0][j]` for `j >= 2` with `p[j-1] == '*'`: `dp[0][j] = dp[0][j-2]`
  (patterns like `a*` or `.*` can match an empty string by taking zero
  occurrences)

**Intuition (Why This Works):**
The `*` quantifier makes the pattern length not directly comparable to the
string length, so a two-pointer greedy approach fails. The boolean DP table
captures the exact state "have we consumed i chars of s and j chars of p",
and each cell's truth depends on a small set of previously filled cells. The
zero-occurrence rule is what makes patterns that start with `x*` handle an
empty string.

**Step-by-Step Procedure:**
1. Create `dp` as an `(m+1) x (n+1)` table of `False`; set `dp[0][0] = True`.
2. Fill base row: for `j` from 2 to `n`, if `p[j-1] == '*'`, set
   `dp[0][j] = dp[0][j-2]`.
3. Loop `i` from 1 to `m`.
4. Loop `j` from 1 to `n`.
5. If `p[j-1]` matches `s[i-1]` directly (letter or `.`), take `dp[i-1][j-1]`.
6. Else if `p[j-1] == '*'`: set `dp[i][j] = dp[i][j-2]` (zero), then if
   `p[j-2]` matches `s[i-1]`, OR in `dp[i-1][j]` (one or more).
7. Return `dp[m][n]`.

**Worked Example (Dry Run):**
`s = "aab"`, `p = "c*a*b"`. Table (rows = s chars with empty, cols = p chars
with empty):

| s\p  | "" | c | * | a | * | b |
|------|----|---|---|---|---|---|
| ""   | T  | F | T | F | T | F |
| a    | F  | F | F | T | T | F |
| a    | F  | F | F | F | T | F |
| b    | F  | F | F | F | F | T |

- Row 0: `c*` and `a*` may match zero characters → dp[0][2] and dp[0][4] are T.
- `dp[1][3] = T`: "a" matched by `c*a` (zero c's, then one 'a').
- `dp[2][4] = T`: "aa" matched by `c*a*` (zero c's, two a's).
- `dp[3][5] = T`: "aab" matched by `c*a*b` (b consumes the last char).

Final answer: `dp[3][5] = True`.

**Code:**
```python
def is_match(s, p):
    m, n = len(s), len(p)
    # dp[i][j] = True if s[:i] matches pattern prefix p[:j].
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    # Base row: an empty string matches patterns like a*b* where every
    # trailing '*'-pair is taken as zero occurrences.
    for j in range(2, n + 1):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == s[i - 1] or p[j - 1] == ".":
                # Direct single-character match: consume one of each.
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j - 1] == "*":
                # Case 1: the '*' matches ZERO of its preceding character.
                dp[i][j] = dp[i][j - 2]
                # Case 2: one or more -- valid only if the preceding char
                # matches s[i-1]; then reuse dp[i-1][j].
                if p[j - 2] == s[i - 1] or p[j - 2] == ".":
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
    return dp[m][n]
```

**Complexity:**
- Time: O(m * n)
- Space: O(m * n)

**Common Mistakes & Edge Cases:**
- `.*` matches any string (including empty) because `.` can repeat; test
  `s = "ab", p = ".*"`.
- A `*` must be examined for the zero case first (`dp[i][j-2]`) before the
  repeat case; flipping the order still works but requires care with the OR.
- The pattern can be longer than the string (`s = "a", p = "ab*"`), so the
  table must be sized by both lengths, not just `len(s)`.
- `p = "a*b"` vs `s = "b"`: zero 'a's then 'b' → True; the zero case is
  essential.
- Patterns like `p = "c*c"` vs `s = "c"`: the first `c*` matches zero, the
  final `c` matches the char → True. Ensure you don't greedily force the `*`
  to consume the only 'c'.

---

### 12. Longest Palindromic Subsequence

**Problem Explanation:**
Given a string `s`, return the length of the longest palindromic subsequence
(a subsequence that reads the same forwards and backwards; characters need not
be contiguous). For example, `s = "bbbab"` has longest palindromic subsequence
"bbbb" (indices 0,1,3,4), length 4. Input is the string; output is the integer
length.

**State Definition:**
`dp[i][j]` = length of the longest palindromic subsequence within the substring
`s[i..j]`.

**Recurrence Relation:**
```
if s[i] == s[j]:  dp[i][j] = dp[i+1][j-1] + 2
else:             dp[i][j] = max(dp[i+1][j], dp[i][j-1])
```
If the two ends match, the optimal palindrome is obtained by wrapping the best
palindrome of the inside `s[i+1..j-1]` with `s[i]` and `s[j]`. If they differ,
at least one end cannot be part of any palindromic subsequence, so take the
best of dropping either end. This is correct by the same optimal-substructure
argument used for LCS, restricted to one string.

**Base Cases:**
- `dp[i][i] = 1` (a single character is a palindrome of length 1)
- `dp[i][j] = 0` when `i > j` (empty substring)

**Intuition (Why This Works):**
This is LCS of a string with its reverse, but computed directly with an
interval DP: `dp[i][j]` depends on the smaller intervals inside it, so we fill
the table from the bottom-right corner upward (decreasing `i`) and from left
to right (increasing `j`). The "choice" at each state is whether the two ends
form part of the palindrome or not.

**Step-by-Step Procedure:**
1. If `s` is empty, return 0; let `n = len(s)`.
2. Create an `n x n` zero table.
3. Loop `i` from `n - 1` down to 0.
4. Set `dp[i][i] = 1`.
5. Loop `j` from `i + 1` to `n - 1`.
6. If `s[i] == s[j]`, set `dp[i][j] = dp[i+1][j-1] + 2`; else
   `dp[i][j] = max(dp[i+1][j], dp[i][j-1])`.
7. Return `dp[0][n-1]`.

**Worked Example (Dry Run):**
`s = "bbbab"` (indices 0..4). Filling by decreasing `i`:

| i | j | comparison | dp[i][j] |
|---|---|------------|----------|
| 4 | 4 | base       | 1 |
| 3 | 3 | base       | 1 |
| 3 | 4 | a vs b     | max(1,1) = 1 |
| 2 | 2 | base       | 1 |
| 2 | 3 | b vs a     | max(1,1) = 1 |
| 2 | 4 | b vs b     | dp[3][3]+2 = 3 ("bbb") |
| 1 | 1 | base       | 1 |
| 1 | 2 | b vs b     | dp[2][1]+2 = 2 ("bb") |
| 1 | 3 | b vs a     | max(dp[2][3]=1, dp[1][2]=2) = 2 |
| 1 | 4 | b vs b     | dp[2][3]+2 = 3 ("bbb" or "bb...") |
| 0 | 0 | base       | 1 |
| 0 | 1 | b vs b     | dp[1][0]+2 = 2 ("bb") |
| 0 | 2 | b vs b     | dp[1][1]+2 = 3 ("bbb") |
| 0 | 3 | b vs a     | max(dp[1][3]=2, dp[0][2]=3) = 3 |
| 0 | 4 | b vs b     | dp[1][3]+2 = 4 ("bbbb") |

Final answer: `dp[0][4] = 4`.

**Code:**
```python
def longest_palindrome_subseq(s):
    if not s:
        return 0
    n = len(s)
    # dp[i][j] = longest palindromic subsequence length in s[i..j].
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):   # i must go DOWNWARD: dp[i][j] needs row i+1
        dp[i][i] = 1                 # single character is a palindrome
        for j in range(i + 1, n):
            if s[i] == s[j]:
                # Matching ends wrap the best palindrome of the inside.
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                # Ends differ: keep the best of dropping either end.
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]
```

**Complexity:**
- Time: O(n^2)
- Space: O(n^2)

**Common Mistakes & Edge Cases:**
- Loop direction: `i` must decrease (depends on `dp[i+1][...]`); going the
  wrong way reads unfilled cells.
- Single character string returns 1.
- All-same-character strings like "aaaa" return `n` (the whole string).
- Reading `dp[i+1][j-1]` when `j = i + 1` reads a cell with `i+1 > j-1`; the
  zero table handles it (empty inside).
- Not contiguous: "cbbd" has answer 2 (a palindrome like "bb"), even though
  no length-3 substring is a palindrome.

---

### 13. Maximal Rectangle

**Problem Explanation:**
Given a binary matrix of `"0"` and `"1"` characters, find the largest rectangle
containing only 1s and return its area. For example, the classic 4x5 matrix

```text
1 0 1 0 0
1 0 1 1 1
1 1 1 1 1
1 0 0 1 0
```

contains a 2x3 rectangle of 1s (rows 1-2, cols 2-4), area 6. Input is the
matrix; output is the max area.

**State Definition:**
No single 2D dp table is needed. Define a derived state: for each row, `heights[j]`
= number of consecutive `"1"`s ending at the current row in column `j` (a
histogram of vertical runs). The largest rectangle in that histogram is a
candidate answer for rectangles whose bottom edge is the current row.

**Recurrence Relation:**
```
heights[j] = heights[j] + 1 if matrix[row][j] == "1" else 0
area      = largest_rectangle_area(heights)   # monotonic-stack histogram solver
```
A rectangle whose bottom edge is the current row corresponds exactly to a
rectangle in this histogram, and the histogram solver finds its maximum via
the monotonic-stack rule: when a smaller height `h` appears, every taller bar
popped has `h` as its right boundary; the left boundary is the stack element
below it. Correct because the histogram captures all widths of consecutive 1s
ending at this row.

**Base Cases:**
- Empty matrix returns 0.
- A histogram of zeros yields area 0.

**Intuition (Why This Works):**
Any all-1s rectangle has a bottom row; if we process rows top to bottom,
the rectangle's columns at that row form a contiguous block in the histogram
with height equal to the rectangle's height. The largest-rectangle-in-histogram
subproblem is solved in O(n) per row with a monotonic stack, because each bar
is pushed and popped once. This reduces an m*n matrix problem to m histogram
problems.

**Step-by-Step Procedure:**
1. If the matrix is empty, return 0.
2. Initialize `heights = [0] * n` and `max_area = 0`.
3. For each row, update every `heights[j]`: `+1` if `matrix[row][j] == "1"`,
   else reset to 0.
4. Compute `largest_rectangle_area(heights)` with the monotonic stack:
   a. Append a 0 sentinel to force the stack to flush at the end.
   b. For each index with height `h`, pop while the stack top is taller than
      `h`; for each popped bar, its width is `current index - next top - 1`.
   c. Track the max `height * width`.
5. Update `max_area` with this row's best.
6. Return `max_area`.

**Worked Example (Dry Run):**
Matrix above. Histograms and their max areas:

| row | heights          | largest rectangle area |
|-----|------------------|------------------------|
| 0   | [1, 0, 1, 0, 0]  | 1 (single 1s)          |
| 1   | [2, 0, 2, 1, 1]  | 2 (e.g. height 2 width 1) |
| 2   | [3, 1, 3, 2, 2]  | 5 (height 1, width 5)  |
| 3   | [4, 0, 0, 3, 0]  | 4 (height 4 or height 3) |

For row 2, stack trace (heights `[3,1,3,2,2]` + sentinel 0): bars 0 (h3) and 2
(h3) each yield area 3; bar at index 1 (h1) with width 5 yields area 5; the
sentinel flushes bar 3 (h2, width 2) → 4 and bar 4 (h2, width 1) → 2. Max 5.
Final answer: `max = 6` (from the 2x3 block at rows 1-2, cols 2-4).

**Code:**
```python
def largest_rectangle_area(heights):
    # Monotonic-stack solver: largest rectangle inside ONE histogram.
    stack = []
    max_area = 0
    heights.append(0)  # sentinel: forces all bars to be popped at the end
    for i, h in enumerate(heights):
        # While the new height is smaller, the popped bar's rectangle ends here.
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            # Width: from the bar just below it in the stack to current index.
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    heights.pop()  # remove the sentinel to leave the caller's list intact
    return max_area


def maximal_rectangle(matrix):
    if not matrix:
        return 0
    n = len(matrix[0])
    heights = [0] * n   # histogram of consecutive 1s ending at the current row
    max_area = 0
    for row in matrix:
        for j in range(n):
            # Grow the run on a '1', reset the run on a '0'.
            heights[j] = heights[j] + 1 if row[j] == "1" else 0
        # The best rectangle touching this row is the best histogram rectangle.
        max_area = max(max_area, largest_rectangle_area(heights))
    return max_area
```

**Complexity:**
- Time: O(m * n) — each row's histogram solved in O(n)
- Space: O(n) for the heights array and the stack

**Common Mistakes & Edge Cases:**
- A matrix of all zeros must return 0, not some positive value.
- Single row `[["1", "1"]]` → histogram `[1, 1]` → area 2.
- Forgetting the sentinel 0 leaves the stack non-empty at the end, silently
  missing the last bars.
- Popped-bar width uses the new stack top, not the popped index.
- Mutating the caller's `heights` (the append/pop dance) is safe only if the
  sentinel is always removed; keep the helper self-contained.

---

### 14. Dungeon Game

**Problem Explanation:**
A knight starts at the top-left cell of a dungeon grid and must reach the
princess at the bottom-right. Each cell holds a number: negative = damage
(reduces health), positive = heals. The knight moves only right or down, and
his health must never drop below 1 at any point (including the start and the
princess's cell). Return the minimum initial health the knight needs to reach
the princess. For example, the dungeon

```text
-2 -3  3
-5 -10 1
10 30 -5
```

needs initial health 7. Input is the dungeon matrix; output is the minimum
starting HP.

**State Definition:**
`dp[i][j]` = minimum health required BEFORE entering cell `(i, j)` so that the
knight can still finish the rest of the path alive.

**Recurrence Relation:**
```
dp[i][j] = max(1, min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j])
```
After entering `(i, j)`, the knight's health changes by `dungeon[i][j]`, and
then he must meet the requirement of the cheaper of the two next cells. So
`required_before + dungeon[i][j] >= next_requirement`, i.e.
`required_before >= next_requirement - dungeon[i][j]`, clamped to at least 1.
Correct because the future depends only on the current cell, and we may choose
either move.

**Base Cases:**
- Just past the princess: `dp[m][n-1] = dp[m-1][n] = 1` (finish with at least
  1 HP).
- Out-of-bounds cells are `infinity` (can't go there), except the two cells
  adjacent to the princess's target.

**Intuition (Why This Works):**
Working FORWARD (minimize damage taken) fails because a heal-heavy path can be
better even if its cumulative sum dips lower — the constraint is a running
minimum, not a total. So we reverse the DP: from the princess back to the
start, each cell records the minimum health needed to enter it. The "choice" is
right vs down, and we always take the less demanding neighbor, then clamp to 1
because dead is not allowed.

**Step-by-Step Procedure:**
1. Let `m, n` be the dungeon dimensions.
2. Create `dp` as an `(m+1) x (n+1)` table of `inf`; set
   `dp[m][n-1] = dp[m-1][n] = 1`.
3. Loop `i` from `m-1` down to 0.
4. Loop `j` from `n-1` down to 0.
5. Compute `need = min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j]`.
6. Set `dp[i][j] = max(1, need)`.
7. Return `dp[0][0]`.

**Worked Example (Dry Run):**
Dungeon above. Filling bottom-up, right-to-left (`dp[i][j]` = min HP before
entering):

| cell (i,j) | value | next requirement | dp[i][j] |
|------------|-------|------------------|----------|
| (2,2) -5   | 1     | min(1,1)=1        | max(1, 1+5)=6 |
| (2,1) 30   | 1     | min(inf,6)=6      | max(1, -24)=1 |
| (2,0) 10   | 1     | min(inf,1)=1      | max(1, -9)=1 |
| (1,2) 1    | 5     | min(6,inf)=6      | max(1, 5)=5 |
| (1,1) -10  | 11    | min(1,5)=1        | max(1, 11)=11 |
| (1,0) -5   | 6     | min(1,11)=1       | max(1, 6)=6 |
| (0,2) 3    | 2     | min(5,inf)=5      | max(1, 2)=2 |
| (0,1) -3   | 5     | min(11,2)=2       | max(1, 5)=5 |
| (0,0) -2   | 7     | min(6,5)=5        | max(1, 7)=7 |

Final answer: `dp[0][0] = 7` (route right, right, down, down: health stays
`7 → 5 → 2 → 5 → 6 → 1`).

**Code:**
```python
def calculate_minimum_hp(dungeon):
    m, n = len(dungeon), len(dungeon[0])
    # dp[i][j] = minimum HP needed BEFORE entering cell (i, j).
    # Extra row/column of infinities make boundary checks uniform.
    dp = [[float("inf")] * (n + 1) for _ in range(m + 1)]
    # Just beyond the princess, finishing alive needs exactly 1 HP.
    dp[m][n - 1] = dp[m - 1][n] = 1
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            # After this cell you move to the cheaper of down/right, and the
            # cell itself changes your health by dungeon[i][j].
            need = min(dp[i + 1][j], dp[i][j + 1]) - dungeon[i][j]
            dp[i][j] = max(1, need)  # health can never drop below 1
    return dp[0][0]
```

**Complexity:**
- Time: O(m * n)
- Space: O(m * n) (O(n) with a rolling row)

**Common Mistakes & Edge Cases:**
- Negative cumulative logic: you cannot simply maximize the sum along the path;
  the minimum along the path is what matters.
- Never allowing health to drop below 1: `max(1, need)` is mandatory, not
  optional.
- A dungeon with all positive values, e.g. `[[0]]`, needs HP 1 (you start at
  the princess cell with 1 HP).
- Forgetting the two sentinel 1s leaves `dp[m][n-1]`/`dp[m-1][n]` at `inf` and
  the princess cell becomes unreachable in the DP.
- The knight must survive AT the princess cell too: that's exactly why
  `dp[m][n-1] = dp[m-1][n] = 1`.

---

### 15. Stone Game III

**Problem Explanation:**
Alice and Bob play with a row of stones `values`. On each turn, a player takes
1, 2, or 3 stones from the front. Each stone's value is its score, and both
players play optimally to maximize their own total. Return `"Alice"` if Alice
wins (strictly more score), `"Bob"` if Bob wins, or `"Tie"`. For example,
`values = [1, 2, 3, 7]` → Bob wins. Input is the values array; output is the
winner string.

**State Definition:**
`dp[i]` = the best SCORE DIFFERENCE (current player's score minus the
opponent's score from the remaining game) achievable starting at position `i`
(stone `i` is at the front of what remains).

**Recurrence Relation:**
```
dp[i] = max over take in {1, 2, 3} of ( suffix[i] - dp[i + take] )
        (only when i + take <= n)
```
If the current player takes `take` stones, they immediately collect
`suffix[i] - suffix[i + take]` points (all stones from `i` to `i + take - 1`).
The opponent then plays optimally from position `i + take`, earning a
difference of `dp[i + take]` in their own favor, so our net difference is
`(points collected) - dp[i + take]`. We pick the `take` maximizing this. This
is the classic minimax form: `my_score - opponent_best_rest`.

**Base Cases:**
- `dp[n] = 0` (no stones left, no more points, difference 0)

**Final answer:**
Alice's difference is `dp[0]`; Bob's total is `suffix[0] - dp[0]`. Compare and
return the winner.

**Intuition (Why This Works):**
Game DP flips perspective at every move: the value `dp[i]` is computed from the
opponent's optimal value `dp[i + take]`, which is exactly how minimax works.
Because a player's gain is the other's loss (all stones get claimed), tracking
the score difference compresses two totals into one number. The suffix-sum
array makes "points collected by taking k stones" an O(1) lookup.

**Step-by-Step Procedure:**
1. Let `n = len(values)`; create `dp = [inf_neg] * (n + 1)` and `dp[n] = 0`.
2. Build `suffix[i] = suffix[i + 1] + values[i]` for `i` from `n - 1` down to 0.
3. Loop `i` from `n - 1` down to 0.
4. For `take` in 1, 2, 3 with `i + take <= n`, update
   `dp[i] = max(dp[i], suffix[i] - dp[i + take])`.
5. After the loop, compute Alice's score `a = dp[0]` and Bob's
   `b = suffix[0] - dp[0]`.
6. Return `"Alice"` if `a > b`, `"Bob"` if `b > a`, else `"Tie"`.

**Worked Example (Dry Run):**
`values = [1, 2, 3, 7]`. `suffix = [13, 12, 10, 7, 0]`, `dp[4] = 0`.

| i | candidate values of suffix[i] - dp[i+take] | dp[i] |
|---|---------------------------------------------|-------|
| 3 | take=1: 7 - 0 = 7                          | 7     |
| 2 | take=1: 10-7=3; take=2: 10-0=10            | 10    |
| 1 | take=1: 12-10=2; take=2: 12-7=5; take=3: 12-0=12 | 12 |
| 0 | take=1: 13-12=1; take=2: 13-10=3; take=3: 13-7=6 | 6 |

Alice's difference `dp[0] = 6`, Bob's total `13 - 6 = 7`. Final answer: `"Bob"`.

**Code:**
```python
def stone_game_iii(values):
    n = len(values)
    # dp[i] = best score DIFFERENCE (current player - opponent) from position i.
    dp = [float("-inf")] * (n + 1)
    dp[n] = 0  # no stones remain: difference is 0
    # suffix[i] = total value of all stones from i to the end.
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + values[i]
    for i in range(n - 1, -1, -1):
        for take in range(1, 4):
            if i + take <= n:
                # Taking `take` stones gains suffix[i] - suffix[i+take]; the
                # opponent then holds an advantage of dp[i+take] over us.
                dp[i] = max(dp[i], suffix[i] - dp[i + take])
    a = dp[0]             # Alice's final advantage over Bob
    b = suffix[0] - dp[0] # Bob's final score
    return "Alice" if a > b else ("Bob" if b > a else "Tie")
```

**Complexity:**
- Time: O(n) — at most 3 transitions per position
- Space: O(n) for `dp` and `suffix`

**Common Mistakes & Edge Cases:**
- Negative stone values are allowed, so greedy "take as many as possible" is
  wrong; every `take` option must be evaluated.
- The recurrence is `suffix[i] - dp[i + take]`, not `dp[i + take] - suffix[i]`
  (the sign of the difference flips between turns).
- Forgetting the `i + take <= n` bound (or mis-setting it) reads past the end.
- A tie must return `"Tie"`, not just "Alice"/"Bob" fallback.
- `values = [1, 2, 3, 6]` ends in a tie (both 6); test it.
---

## SP L3 LEVEL

### 16. TSP (Bitmask DP)

**Problem Explanation:**
Given a `cost` matrix where `cost[i][j]` is the travel cost from city `i` to
city `j`, find the minimum cost of a tour that starts at city 0, visits every
other city exactly once, and returns to city 0. For example, with 4 cities the
optimal tour cost is 80. Input is the square cost matrix; output is the minimum
tour cost. This is the Traveling Salesperson Problem, solvable exactly for
small `n` (n <= ~20) with bitmask DP.

**State Definition:**
`dp[mask][last]` = minimum cost to visit exactly the cities whose bits are set
in `mask`, ending at city `last` (and having started at city 0, which is
always in `mask`).

**Recurrence Relation:**
```
dp[mask | (1 << nxt)][nxt] = min( dp[mask | (1 << nxt)][nxt],
                                  dp[mask][last] + cost[last][nxt] )
for all unvisited cities nxt reachable from `last`
```
Extending a tour that ends at `last` by traveling to the new city `nxt` adds
`cost[last][nxt]`. The final answer closes the loop: return to city 0.
Correct because the optimal tour from a set of visited cities ending at `last`
only depends on (mask, last) — the order of earlier cities doesn't matter for
the future.

**Base Cases:**
- `dp[1][0] = 0` (only city 0 visited, you are already there, cost 0)
- All other states are `infinity` (unreachable).

**Final answer:**
`min over i in 1..n-1 of (dp[full][i] + cost[i][0])`.

**Intuition (Why This Works):**
A plain "visited set" isn't enough to memoize because subsets need ordering; the
bitmask encodes the visited subset in one integer, and `last` pinpoints where
the tour currently is. There are 2^n masks, so every subset is a state. The
"choice" at each state is which unvisited city to go to next, and we try all of
them, keeping the cheapest continuation. n cities → 2^n * n states, each
exploring up to n transitions.

**Step-by-Step Procedure:**
1. Let `n = len(cost)`; create `dp` of size `(1 << n) x n` filled with a large
   `INF`.
2. Set `dp[1][0] = 0`.
3. Loop over every `mask` from 0 to `(1 << n) - 1`.
4. For every city `last` in `mask` with a finite `dp[mask][last]`:
5.   For every city `nxt` not in `mask`:
6.     Update `dp[mask | (1 << nxt)][nxt]` with
       `dp[mask][last] + cost[last][nxt]` (take the min).
7. Compute `full = (1 << n) - 1`.
8. Return `min(dp[full][i] + cost[i][0] for i in 1..n-1 where a return path exists)`.

**Worked Example (Dry Run):**
Cost matrix (4 cities):

```text
   0   1   2   3
0  0  10  15  20
1 10   0  35  25
2 15  35   0  30
3 20  25  30   0
```

Selected DP states (mask shown in binary):

| mask (binary) | last | dp | how it was reached |
|---------------|------|-----|--------------------|
| 0001          | 0    | 0  | start              |
| 0011          | 1    | 10 | 0→1                |
| 0101          | 2    | 15 | 0→2                |
| 1001          | 3    | 20 | 0→3                |
| 0111          | 2    | 45 | 0→1→2 (10+35)      |
| 1011          | 3    | 35 | 0→1→3 (10+25)      |
| 1101          | 3    | 45 | 0→2→3 (15+30)      |
| 1111          | 1    | 70 | 0→2→3→1 (15+30+25) |
| 1111          | 2    | 65 | 0→3→1→2 (20+25+30) |
| 1111          | 3    | 75 | 0→1→2→3 (10+35+30) |

Close the loop: `70 + cost[1][0] = 80`, `65 + cost[2][0] = 80`, `75 + 20 = 95`.
Final answer: `80` (e.g. tour 0 → 1 → 3 → 2 → 0 = 10 + 25 + 30 + 15).

**Code:**
```python
def tsp(cost):
    n = len(cost)
    INF = 10**9
    # dp[mask][last] = min cost to visit exactly the cities in `mask`,
    # ending at city `last` (bit `b` set in mask == city `b` visited).
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start: only city 0 visited, cost 0
    for mask in range(1 << n):
        for last in range(n):
            if not (mask >> last & 1):  # `last` is not in this mask
                continue
            if dp[mask][last] == INF:   # state unreachable so far
                continue
            for nxt in range(n):
                if (mask >> nxt) & 1:   # already visited: skip
                    continue
                # Extend the tour: move from `last` to unvisited city `nxt`.
                new_mask = mask | (1 << nxt)
                dp[new_mask][nxt] = min(dp[new_mask][nxt],
                    dp[mask][last] + cost[last][nxt])
    full = (1 << n) - 1                 # mask with all cities visited
    # Close the loop: return from the final city back to the start (city 0).
    ans = min(dp[full][i] + cost[i][0] for i in range(1, n) if cost[i][0])
    return ans
```

**Complexity:**
- Time: O(2^n * n^2) — 2^n masks, n endings, n transitions each
- Space: O(2^n * n) for the dp table

**Common Mistakes & Edge Cases:**
- City 0 must be visited exactly twice (start and return); make sure the loop
  doesn't add cost[0][0].
- `n = 1` (a single city): the tour is trivial, cost 0 — the `min` over an
  empty generator crashes; guard for it.
- Bit manipulation off-by-one: `mask >> last & 1` checks city `last`;
  `mask | (1 << nxt)` marks `nxt`.
- Forgetting to skip unreachable states wastes time and can propagate `INF`
  incorrectly.
- If a return path to city 0 is missing for some `i`, skip it (the
  `if cost[i][0]` guard).

---

### 17. Tree DP - Max Independent Set

**Problem Explanation:**
You are given a binary tree where every node has a value. An "independent set"
is a set of nodes with no two adjacent in the tree (no node and its parent or
children both chosen). Return the maximum sum of node values in any independent
set. For example, in the tree `[3, 2, 3, null, 3, null, 1]` the optimal set is
`{3 (root), 3 (left's right child), 1 (right's right child)}`, sum 7. Input is
the tree root; output is the max sum.

**State Definition:**
For each node, define a pair `(take, skip)`:
- `take` = best sum from this node's subtree when this node IS included,
- `skip` = best sum from this node's subtree when this node is NOT included.

**Recurrence Relation:**
```
take = node.val + left.skip + right.skip
skip = max(left.take, left.skip) + max(right.take, right.skip)
```
If we include the node, we must exclude both children (they are adjacent), so
we add the children's `skip` values. If we exclude the node, each child is free
to be included or not, so we take the better option for each child
independently. This is correct because the tree has no cycles: subtrees only
interact through the parent, so a post-order traversal can combine them.

**Base Cases:**
- An empty (null) subtree contributes `(0, 0)`.

**Final answer:**
`max(root.take, root.skip)`.

**Intuition (Why This Works):**
The adjacency constraint only couples a node with its children, and the optimal
subtree solution depends only on whether the parent is chosen — hence the
two-state DP. A post-order DFS computes children first, then combines their
answers, which is DP on a tree (each subtree is a subproblem solved exactly
once).

**Step-by-Step Procedure:**
1. Define a recursive `dfs(node)` that returns `(take, skip)`.
2. Base case: if `node` is None, return `(0, 0)`.
3. Recurse on `node.left` and `node.right`.
4. Compute `take = node.val + left[1] + right[1]`.
5. Compute `skip = max(left) + max(right)`.
6. Return `(take, skip)`.
7. Call `dfs(root)` and return `max` of the result.

**Worked Example (Dry Run):**
Tree `[3, 2, 3, null, 3, null, 1]`:

```text
        3
       / \
      2   3
       \   \
        3   1
```

Post-order results `(take, skip)`:

| node | take                  | skip               | returned |
|------|-----------------------|--------------------|----------|
| leaf 1   | 1 + 0 + 0 = 1        | 0                  | (1, 0)   |
| node 3 (right) | 3 + skip(1) = 3 + 0 = 3 | max(1) = 1      | (3, 1)   |
| leaf 3   | 3                     | 0                  | (3, 0)   |
| node 2   | 2 + 0 + skip(3)=1 → 3 | max(3) + 0 = 3    | (3, 3)   |
| root 3   | 3 + skip(2)=3 + skip(right3)=1 → 7 | max(3) + max(3) = 6 | (7, 6) |

Final answer: `max(7, 6) = 7`.

**Code:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_independent_set_tree(root):
    def dfs(node):
        # Returns (take, skip) for this node's subtree:
        #   take = best sum when this node IS included,
        #   skip = best sum when this node is NOT included.
        if not node:
            return (0, 0)
        left = dfs(node.left)
        right = dfs(node.right)
        # Include this node -> its children must both be excluded.
        take = node.val + left[1] + right[1]
        # Exclude this node -> each child may independently be taken or skipped.
        skip = max(left) + max(right)
        return (take, skip)
    return max(dfs(root))
```

**Complexity:**
- Time: O(n) — each node visited once
- Space: O(h) — recursion stack depth (h = tree height)

**Common Mistakes & Edge Cases:**
- An empty tree (None root) must return 0.
- The recurrence excludes a node's children only when the node is TAKEN;
  mixing up `take`/`skip` indices is the most common error.
- This is a max-SUM problem; a variant asks for the count of maximum-size
  independent sets, which needs a second DP value.
- Using a greedy "alternate levels" approach is wrong — it ignores that a skip
  at one level can allow two adjacent takes deeper down.
- For non-binary trees, generalize the same two-state DP over all children.

---

### 18. Interval DP - Matrix Chain

**Problem Explanation:**
Given a list `p` where matrix `A_i` has dimensions `p[i] x p[i+1]`, find the
minimum number of scalar multiplications needed to multiply the whole chain
`A_1 * A_2 * ... * A_n`. Different parenthesizations give very different costs.
For example, `p = [10, 30, 5, 60]` (three matrices: 10x30, 30x5, 5x60) has
optimal cost 4500 via `(A1 * A2) * A3`. Input is the dimension array `p` of
length `n + 1`; output is the minimum scalar multiplications.

**State Definition:**
`dp[i][j]` = minimum scalar multiplications to multiply the chain of matrices
`A_i ... A_j` (i.e. matrices with dimensions `p[i] x p[i+1]` through
`p[j] x p[j+1]`).

**Recurrence Relation:**
```
dp[i][j] = min over k in [i, j-1] of
           dp[i][k] + dp[k+1][j] + p[i] * p[k+1] * p[j+1]
```
Split the chain after matrix `k`: multiply `A_i..A_k` optimally, then
`A_{k+1}..A_j` optimally, then multiply the two results together. The final
matrix product has dimensions `p[i] x p[j+1]`, and the intermediate result from
the left half is `p[i] x p[k+1]`, from the right half `p[k+1] x p[j+1]`, so the
join costs `p[i] * p[k+1] * p[j+1]`. Correct because any parenthesization has
one outermost split, and each half must be optimal.

**Base Cases:**
- `dp[i][i] = 0` (a single matrix needs no multiplications)

**Intuition (Why This Works):**
The problem is fully characterized by the interval `[i, j]` of matrices to
multiply. The "choice" is where to place the outermost split `k`, and the cost
breaks into two independent subproblems plus one join cost. Filling intervals
by increasing length guarantees all sub-intervals are computed first.

**Step-by-Step Procedure:**
1. Let `n = len(p) - 1` (number of matrices).
2. Create `dp` as an `n x n` zero table.
3. Loop `length` from 2 to `n` (chain length).
4. Loop `i` from 0 to `n - length`; set `j = i + length - 1`.
5. Initialize `dp[i][j] = infinity`.
6. Loop `k` from `i` to `j - 1` and update
   `dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j] + p[i]*p[k+1]*p[j+1])`.
7. Return `dp[0][n - 1]`.

**Worked Example (Dry Run):**
`p = [10, 30, 5, 60]`; matrices A (10x30), B (30x5), C (5x60).

| interval | k | computation | dp |
|----------|---|-------------|-----|
| dp[0][1] | 0 | 10*30*5 = 1500 | 1500 |
| dp[1][2] | 1 | 30*5*60 = 9000 | 9000 |
| dp[0][2] | 0 | 0 + 9000 + 10*30*60 = 27000 | 27000 |
| dp[0][2] | 1 | 1500 + 0 + 10*5*60 = 4500 | **4500** |

Final answer: `dp[0][2] = 4500` (parenthesization `(A*B)*C`: 10x30 times 30x5
= 1500, then 10x5 times 5x60 = 3000, total 4500).

**Code:**
```python
def matrix_chain(p):
    n = len(p) - 1
    # dp[i][j] = min scalar multiplications to multiply matrices i..j
    # (matrix i has dimensions p[i] x p[i+1]).
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):          # grow the chain length
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                # Split after matrix k: optimal left, optimal right, then the
                # join cost (p[i] x p[k+1]) * (p[k+1] x p[j+1]).
                q = dp[i][k] + dp[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                dp[i][j] = min(dp[i][j], q)
    return dp[0][n - 1]
```

**Complexity:**
- Time: O(n^3) — three nested loops
- Space: O(n^2)

**Common Mistakes & Edge Cases:**
- `n = 1` (a single matrix): the loops don't run, `dp[0][0] = 0` is returned —
  correct, but beware of indexing `p[i+1]` inside loops.
- The join cost is `p[i] * p[k+1] * p[j+1]`, using the shared middle dimension
  exactly once; mixing up indices inflates the answer.
- The split loop is `k in [i, j-1]`, not `[i, j]`.
- Interval DP must fill by length so that `dp[i][k]` and `dp[k+1][j]` are
  already computed.
- `p = [40, 20, 30, 10, 30]` → 26000; use it to check your indices.

---

### 19. Palindrome Partitioning II

**Problem Explanation:**
Given a string `s`, you want to split it into as few pieces as possible such
that every piece is a palindrome. Return the minimum number of cuts needed.
For example, `s = "aab"` can be cut into `"aa" | "b"` with 1 cut. A string that
is already a palindrome needs 0 cuts. Input is the string; output is the
minimum number of cuts.

**State Definition:**
Two DP layers:
- `pal[i][j]` = `True` if `s[i..j]` is a palindrome.
- `dp[i]` = minimum cuts needed to partition the prefix `s[0..i]`.

**Recurrence Relation:**
```
pal[i][j] = s[i] == s[j] and (j - i <= 2 or pal[i+1][j-1])
dp[i] = 0                                   if pal[0][i]
dp[i] = min over j < i with pal[j+1][i] of (dp[j] + 1)
```
A substring is a palindrome if its ends match and its inner part is a
palindrome (or has length 0 or 1). For the cuts: if the whole prefix is a
palindrome, 0 cuts; otherwise make the last piece `s[j+1..i]` a palindrome and
add 1 cut after `j` to the best solution of `s[0..j]`. Correct because every
partition ends with a palindrome piece.

**Base Cases:**
- `pal[i][i] = True` (single character)
- `dp[0] = 0` when `s[0]` alone is trivially a palindrome piece

**Intuition (Why This Works):**
Naively re-checking whether every substring is a palindrome at each step would
be O(n^3); precomputing the palindrome table once makes each check O(1). The
main DP is then a clean 1D "minimum pieces" recurrence, identical in spirit to
word break but counting cuts instead of checking membership.

**Step-by-Step Procedure:**
1. If `len(s) <= 1`, return 0.
2. Build the `pal` table: loop `i` from `n - 1` down to 0, `j` from `i` to
   `n - 1`, using the recurrence above.
3. Initialize `dp = [inf] * n`.
4. For each `i` from 0 to `n - 1`:
5.   If `pal[0][i]`, set `dp[i] = 0`.
6.   Else loop `j` from 0 to `i - 1`; if `pal[j+1][i]`, update
       `dp[i] = min(dp[i], dp[j] + 1)`.
7. Return `dp[n - 1]`.

**Worked Example (Dry Run):**
`s = "aab"`.

Palindrome table (computed bottom-up): `pal[0][1] = T` ("aa"), `pal[2][2] = T`
("b"), all others False.

| i | prefix | pal[0][i]? | dp[i] |
|---|--------|-----------|-------|
| 0 | "a"    | T         | 0     |
| 1 | "aa"   | T         | 0     |
| 2 | "aab"  | F         | j=0: pal[1][2]="ab"? F. j=1: pal[2][2]=T → dp[1]+1 = 1 |

Final answer: `dp[2] = 1` (`"aa" | "b"`).

**Code:**
```python
def min_cut(s):
    n = len(s)
    if n <= 1:
        return 0
    # Precompute pal[i][j] = True iff s[i..j] is a palindrome.
    pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            # Ends match AND the inner part is a palindrome (or has size 0/1).
            if s[i] == s[j] and (j - i <= 2 or pal[i + 1][j - 1]):
                pal[i][j] = True
    # dp[i] = minimum cuts to partition the prefix s[0..i].
    dp = [float("inf")] * n
    for i in range(n):
        if pal[0][i]:
            dp[i] = 0               # whole prefix is already a palindrome
        else:
            for j in range(i):
                # Cut after j: s[j+1..i] is a palindrome, so this is one more
                # cut than the best partition of s[0..j].
                if pal[j + 1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)
    return dp[n - 1]
```

**Complexity:**
- Time: O(n^2) — palindrome precompute O(n^2), cut DP O(n^2)
- Space: O(n^2) for the palindrome table (the cut DP itself is O(n))

**Common Mistakes & Edge Cases:**
- `s = "aba"` is already a palindrome → 0 cuts.
- `s = "abc"` → 2 cuts (a | b | c), not 3; cuts split into n pieces cost n-1.
- The palindrome-table recurrence needs `pal[i+1][j-1]`, so `i` must loop
  downward.
- Off-by-one in `pal[j+1][i]`: the last piece is `s[j+1..i]`, and the cut
  happens right after index `j`.
- Single character or empty string: 0 cuts (guard before building the table).

---

### 20. Minimum Cost to Cut Stick

**Problem Explanation:**
You have a wooden stick of length `n`. You must cut it at the integer positions
listed in `cuts`. Each cut costs the current length of the stick being cut
(e.g., cutting a length-7 stick at position 3 costs 7). You may choose the
cutting order to minimize the total cost. Return the minimum total cost. For
example, `n = 7`, `cuts = [1, 3, 4, 5]` has minimum cost 16. Input is the stick
length and the cut positions; output is the min total cost.

**State Definition:**
Add the two endpoints 0 and `n` to the sorted cut positions to form an array
`cuts`. Then `dp[i][j]` = minimum cost to fully cut the segment between
`cuts[i]` and `cuts[j]` (cutting at every requested position strictly inside).

**Recurrence Relation:**
```
dp[i][j] = min over k in (i, j) of dp[i][k] + dp[k][j] + (cuts[j] - cuts[i])
```
Think of `k` as the FIRST cut made inside this segment: it costs the full
segment length `cuts[j] - cuts[i]`, and afterwards the two sub-segments
`(i, k)` and `(k, j)` are cut independently with no interaction. Trying every
`k` and minimizing covers all orderings. Correct because the first cut
splits the problem into two independent ones.

**Base Cases:**
- `dp[i][i] = 0` and `dp[i][i+1] = 0` (no requested cut strictly inside)

**Final answer:**
`dp[0][m - 1]` where `m` is the number of entries in the augmented cuts array.

**Intuition (Why This Works):**
As in Burst Balloons and Matrix Chain, the order-dependent part is handled by
deciding the FIRST action inside an interval, which leaves two independent
subintervals. The cost of the first cut is easy to compute (current segment
length), and the interval DP by increasing length builds up the answer.

**Step-by-Step Procedure:**
1. Build `cuts = [0] + sorted(cuts) + [n]`; let `m = len(cuts)`.
2. Create `dp` as an `m x m` zero table.
3. Loop `length` from 2 to `m - 1` (segment size in boundary points).
4. Loop `i` from 0 to `m - length - 1`; set `j = i + length`.
5. Initialize `dp[i][j] = infinity`.
6. Loop `k` from `i + 1` to `j - 1` and update
   `dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cuts[j] - cuts[i])`.
7. Return `dp[0][m - 1]`.

**Worked Example (Dry Run):**
`n = 7`, `cuts = [1, 3, 4, 5]` → augmented `[0, 1, 3, 4, 5, 7]`.

| interval | best k | cost | dp[i][j] |
|----------|--------|------|----------|
| dp[0][2] (0-3) | 1 | 0 + 0 + 3 | 3 |
| dp[1][3] (1-4) | 2 | 0 + 0 + 3 | 3 |
| dp[2][4] (3-5) | 3 | 0 + 0 + 2 | 2 |
| dp[3][5] (4-7) | 4 | 0 + 0 + 3 | 3 |
| dp[0][3] (0-4) | 1 or 2 | 3+0+4 / 0+3+4 | 7 |
| dp[1][4] (1-5) | 2 | 0 + 2 + 4 = 6 | 6 |
| dp[2][5] (3-7) | 4 | 2 + 0 + 4 = 6 | 6 |
| dp[0][4] (0-5) | 2 | dp[0][2](3) + dp[2][4](2) + 5 = 10 | 10 |
| dp[1][5] (1-7) | 4 | 3 + 0 + 6 = 9 | 9 |
| dp[0][5] (0-7) | 1 or 2 | 0+9+7=16 / 3+6+7=16 | 16 |

Final answer: `dp[0][5] = 16`.

**Code:**
```python
def min_cost_cut(n, cuts):
    # Add the two stick ends as fixed boundary positions, then sort.
    cuts = [0] + sorted(cuts) + [n]
    m = len(cuts)
    # dp[i][j] = min cost to fully cut the segment between cuts[i] and cuts[j].
    dp = [[0] * m for _ in range(m)]
    for length in range(2, m):        # grow the segment (number of boundaries)
        for i in range(m - length):
            j = i + length
            dp[i][j] = float("inf")
            for k in range(i + 1, j): # which cut happens FIRST in this segment
                # First cut costs the full current length cuts[j]-cuts[i];
                # afterwards the two sub-segments are fully independent.
                dp[i][j] = min(dp[i][j],
                    dp[i][k] + dp[k][j] + cuts[j] - cuts[i])
    return dp[0][m - 1]
```

**Complexity:**
- Time: O(m^3) where m = number of cut positions + 2
- Space: O(m^2)

**Common Mistakes & Edge Cases:**
- Always include endpoints 0 and `n` in the dp array; forgetting them makes the
  first/last cut costs wrong.
- With no cuts (`cuts = []`), the answer is 0 (no segment of length >= 2
  exists; the loops never run).
- The first-cut cost uses `cuts[j] - cuts[i]`, the segment length BEFORE any
  cut, not after.
- The k-loop is `(i+1, j)`, excluding the endpoints (they are not cut
  positions).
- Filling order must be by interval length so sub-segments are ready before
  their parent.
---

### 21. Longest Valid Parentheses

**Problem Explanation:**
Given a string `s` containing only `"("` and `")"`, return the length of the
longest (contiguous) substring that is a well-formed parentheses string. For
example, `s = ")()())"` contains the valid substring `"()()"` of length 4.
Input is the string; output is the integer length.

**State Definition:**
`dp[i]` = length of the longest valid parentheses substring that ENDS at index
`i` (inclusive).

**Recurrence Relation:**
```
if s[i] == ")":
    if s[i-1] == "(":                     # "...()" pair closes here
        dp[i] = dp[i-2] + 2
    elif s[i - dp[i-1] - 1] == "(":       # "...((...))" closing brace
        dp[i] = dp[i-1] + 2 + dp[i - dp[i-1] - 2]
```
A valid string ending at `i` is either a direct pair `()` (extending whatever
valid string ended before the opening bracket), or a big `(` that encloses a
valid block `dp[i-1]` and is followed by the closing `)`. In the second case
the enclosing pair adds 2 to the enclosed block and then chains with the valid
block that ended just before the big opening bracket. Correct because any valid
string ending at `i` has `s[i] == ")"` and one of these two shapes.

**Base Cases:**
- `dp[i] = 0` whenever `s[i] == "("` or no valid substring ends at `i`.

**Intuition (Why This Works):**
Valid parentheses are naturally hierarchical, and the "ends-at" formulation
captures the nesting exactly: when a pair closes, you add 2 and continue any
valid block before it. The key subtlety is the chaining term
`dp[i - dp[i-1] - 2]`, which glues together two adjacent valid blocks
separated by an enclosing pair.

**Step-by-Step Procedure:**
1. Create `dp = [0] * len(s)`.
2. Loop `i` from 1 to `len(s) - 1`.
3. If `s[i] == "("`, continue (nothing valid ends here).
4. If `s[i-1] == "("`: set `dp[i] = dp[i-2] + 2` (with bounds guard for i = 1).
5. Else check whether the character just before the valid block ending at
   `i-1` is `"("` (i.e. `s[i - dp[i-1] - 1]`); if so,
   `dp[i] = dp[i-1] + 2 + dp[i - dp[i-1] - 2]` (with bounds guards).
6. Track `max_len` over all `dp[i]`.
7. Return `max_len`.

**Worked Example (Dry Run):**
`s = ")()())"` (indices 0..5).

| i | s[i] | rule applied                                   | dp[i] |
|---|------|------------------------------------------------|-------|
| 0 | )    | starts with `)` — nothing valid ends here      | 0 |
| 1 | (    | opening bracket                                | 0 |
| 2 | )    | s[1]="(" → dp[0] + 2                          | 2 |
| 3 | (    | opening bracket                                | 0 |
| 4 | )    | s[3]="(" → dp[2] + 2 = 4                      | 4 |
| 5 | )    | s[4]=")"; s[5-4-1]=s[0]=")" not "(" → rule 2 fails | 0 |

Final answer: `max(dp) = 4` (the substring `"()()"` at indices 1-4).

**Code:**
```python
def longest_valid_parentheses(s):
    dp = [0] * len(s)
    # dp[i] = length of the longest valid parentheses substring ENDING at i.
    max_len = 0
    for i in range(1, len(s)):
        if s[i] == ")":
            if s[i - 1] == "(":
                # Pattern "...()": close a direct pair; chain with the valid
                # substring that ended just before the '('.
                dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
            elif i - dp[i - 1] - 1 >= 0 and s[i - dp[i - 1] - 1] == "(":
                # Pattern "...((...))": the ')' at i matches the '(' that sits
                # exactly before the valid block ending at i-1.
                prev = dp[i - 1]
                dp[i] = prev + 2  # enclose the valid block with the new pair
                if i - prev - 2 >= 0:
                    # Also chain with the valid block before the matching '('.
                    dp[i] += dp[i - prev - 2]
            max_len = max(max_len, dp[i])
    return max_len
```

**Complexity:**
- Time: O(n) — single pass
- Space: O(n) for the dp array (O(1) with a stack alternative)

**Common Mistakes & Edge Cases:**
- An empty string or one without any valid substring returns 0.
- `s = "()(())"` → 6: the chaining term is essential (inner `()`, then `(())`,
  then chain with the leading `()`).
- Bounds guards (`i >= 2`, `i - prev - 2 >= 0`) prevent negative indexing that
  silently reads from the end of the list.
- Forgetting the `dp[i] = 0` for `(` and stray `)` leaves stale values.
- `s = "(()"` → 2: the leading unmatched `(` makes only `()` count.

---

### 22. Count Different Palindromic Subsequences

**Problem Explanation:**
Given a string `s`, count the number of DISTINCT non-empty palindromic
subsequences. A subsequence is any sequence of characters keeping their order
(not necessarily contiguous), and "distinct" means the resulting strings must
differ, not just the index sets. For example, `s = "bccb"` has 6 distinct
palindromic subsequences: `"b"`, `"c"`, `"bb"`, `"cc"`, `"bcb"`, `"bccb"`.
Return the count modulo 10^9 + 7. Input is the string; output is the integer.

**State Definition:**
`dp[i][j]` = number of distinct palindromic subsequences of the substring
`s[i..j]` (modulo `mod`).

**Recurrence Relation:**
```
if s[i] != s[j]:
    dp[i][j] = dp[i+1][j] + dp[i][j-1] - dp[i+1][j-1]
else (s[i] == s[j]), with low = first index of s[i] in (i, j) and
     high = last index of s[i] in (i, j):
    if low > high:            dp[i][j] = 2 * dp[i+1][j-1] + 2
    elif low == high:         dp[i][j] = 2 * dp[i+1][j-1] + 1
    else:                     dp[i][j] = 2 * dp[i+1][j-1] - dp[low+1][high-1]
```
If the ends differ, they can never be the two ends of one palindrome, so count
palindromes inside `(i+1, j)` plus inside `(i, j-1)` minus the double-counted
intersection `(i+1, j-1)`. If the ends match, every palindrome inside can be
wrapped in `s[i]..s[j]`; the `+2`/`+1`/`-dp[...]` correction handles duplicates
created when the same character appears multiple times inside: wrapping
produces exactly one new palindrome per inner palindrome, plus the 1- and
2-character ones `s[i]` and `s[i]s[j]`, minus the ones already formed between
the first and last inner occurrences. This is the standard dedup argument for
this problem.

**Base Cases:**
- `dp[i][i] = 1` (a single character is one palindrome)
- `dp[i][j] = 0` when `i > j`

**Intuition (Why This Works):**
This is an interval DP where the tricky part is avoiding double-counting when
the boundary character repeats inside. The first/last occurrence scan (`low` /
`high`) precisely detects whether the two new boundary palindromes (`s[i]` and
`s[i]s[j]`) collide with inner ones, and the subtraction term removes exactly
the overlap. Modulo arithmetic must be applied after each cell because counts
grow exponentially.

**Step-by-Step Procedure:**
1. If `s` is empty, return 0; let `n = len(s)`.
2. Create an `n x n` zero table; set `dp[i][i] = 1` for all `i`.
3. Loop `length` from 2 to `n`.
4. Loop `i` from 0 to `n - length`; set `j = i + length - 1`.
5. If `s[i] != s[j]`, apply the union formula.
6. Else scan for `low` (first `s[i]` inside) and `high` (last `s[i]` inside)
   with while loops.
7. Apply the `2*inner + 2/1/-dp` formula according to `low` vs `high`.
8. Take `(dp[i][j] + mod) % mod` to stay non-negative.
9. Return `dp[0][n - 1]`.

**Worked Example (Dry Run):**
`s = "bccb"` (indices 0..3).

| interval | ends | computation | dp[i][j] |
|----------|------|-------------|----------|
| dp[1][2]: "cc" | match | low=2, high=1 → low>high: 2*0 + 2 | 2 (`"c"`, `"cc"`) |
| dp[0][1]: "bc" | differ | 1 + 1 - 0 | 2 (`"b"`, `"c"`) |
| dp[2][3]: "cb" | differ | 1 + 1 - 0 | 2 (`"c"`, `"b"`) |
| dp[0][2]: "bcc" | differ | dp[1][2] + dp[0][1] - dp[1][1] = 2+2-1 | 3 |
| dp[1][3]: "ccb" | differ | dp[2][3] + dp[1][2] - dp[2][2] = 2+2-1 | 3 |
| dp[0][3]: "bccb" | match | low=3, high=2 → low>high: 2*dp[1][2] + 2 = 2*2+2 | 6 |

Final answer: `dp[0][3] = 6`.

**Code:**
```python
def count_palindromic_subsequences(s):
    if not s:
        return 0
    mod = 10**9 + 7
    n = len(s)
    # dp[i][j] = number of DISTINCT palindromic subsequences of s[i..j].
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1  # single character: exactly one palindrome
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                # Every palindrome in s[i+1..j-1] can be wrapped in s[i]..s[j].
                # Find the first and last occurrence of s[i] inside (i, j) to
                # detect double-counting.
                low, high = i + 1, j - 1
                while low <= high and s[low] != s[i]:
                    low += 1
                while low <= high and s[high] != s[j]:
                    high -= 1
                if low > high:
                    # No inner s[i]: +2 for the palindromes s[i] and s[i]s[j].
                    dp[i][j] = 2 * dp[i + 1][j - 1] + 2
                elif low == high:
                    # One inner s[i]: the 2-character wrap s[i]s[j] is new, but
                    # s[i] alone already exists inside -- add 1.
                    dp[i][j] = 2 * dp[i + 1][j - 1] + 1
                else:
                    # Multiple inner s[i]: palindromes wholly between the first
                    # and last inner occurrence get wrapped twice -- subtract
                    # the ones already formed there.
                    dp[i][j] = 2 * dp[i + 1][j - 1] - dp[low + 1][high - 1]
            else:
                # Ends differ: they can never be the two ends of one palindrome.
                # Union of (i+1, j) and (i, j-1), minus their overlap (i+1, j-1).
                dp[i][j] = dp[i + 1][j] + dp[i][j - 1] - dp[i + 1][j - 1]
            dp[i][j] = (dp[i][j] + mod) % mod  # keep non-negative under modulo
    return dp[0][n - 1]
```

**Complexity:**
- Time: O(n^2) (the while loops amortize to O(n^2) overall)
- Space: O(n^2)

**Common Mistakes & Edge Cases:**
- Applying `% mod` only at the end overflows into huge integers for long
  strings; keep every cell reduced.
- The subtraction can go negative; always `+ mod` before `% mod`.
- `s = "aa"` has exactly 2 distinct palindromic subsequences (`"a"`, `"aa"`),
  not 3 — the two index-based "a"s are the same string.
- `low`/`high` scan bounds: `low` and `high` may run past each other; check
  `low > high` first, then `low == high`.
- Empty string guard, since `dp[i][i]` indexing fails on it.

---

### 23. Maximum Sum of 3 Non-Overlapping Subarrays

**Problem Explanation:**
Given an integer array `nums` and an integer `k`, find three non-overlapping
subarrays each of length exactly `k`, maximizing the sum of the three. Return
their starting indices as a list, choosing the LEFTMOST (lexicographically
smallest) set of indices among all answers with the maximum sum. For example,
`nums = [1, 2, 1, 2, 6, 7, 5, 1]`, `k = 2` → `[0, 3, 5]`. Input is the array
and `k`; output is a list of three starting indices.

**State Definition:**
Precompute `sums[i]` = sum of the length-k subarray starting at index `i`. Then
two auxiliary states:
- `left[i]` = the index `<= i` with the largest `sums` value (leftmost on ties).
- `right[i]` = the index `>= i` with the largest `sums` value (leftmost on ties).

**Recurrence Relation:**
```
left[i]  = argmax over j <= i of sums[j]        (leftmost on ties)
right[i] = argmax over j >= i of sums[j]        (leftmost on ties)
answer   = argmax over mid of
           sums[left[mid - k]] + sums[mid] + sums[right[mid + k]]
```
Fix the middle subarray at `mid`. The first must start no later than
`mid - k` and be the best in `sums[0..mid-k]` → `left[mid - k]`. The third must
start no earlier than `mid + k` and be the best in `sums[mid+k..]` →
`right[mid + k]`. The three are then independent, so summing the three best
gives the max for that `mid`. Correct because any optimal triple has some
middle subarray, and its neighbors are chosen optimally given the separation
constraint.

**Base Cases:**
- `left[0] = 0`, `right[len(sums) - 1] = len(sums) - 1`
- `n` must be at least `3*k` for a valid answer to exist.

**Intuition (Why This Works):**
Instead of a 3D DP (positions × three states), observe that once the middle
window is fixed, the left and right windows are independent of each other and
can be precomputed as running bests. This turns the problem into an O(n) scan.
The tie-breaking is critical: scanning left-to-right with strict `>` keeps the
leftmost best on the left side, and scanning right-to-left with `>=` keeps the
leftmost best on the right side.

**Step-by-Step Procedure:**
1. Compute `sums[i]` for every length-k window with a sliding window.
2. Compute `left`: scan left to right, track the best-so-far index, update only
   on strictly greater sums (ties keep the leftmost index).
3. Compute `right`: scan right to left, track the best-so-far index, update on
   `>=` (so a tie keeps the smaller index).
4. Loop `mid` from `k` to `len(sums) - k - 1`.
5. Get `l = left[mid - k]`, `r = right[mid + k]`, total = their sums plus
   `sums[mid]`.
6. Keep the first `[l, mid, r]` achieving the max total (strict `>`).
7. Return the best triple.

**Worked Example (Dry Run):**
`nums = [1, 2, 1, 2, 6, 7, 5, 1]`, `k = 2`. Windows (starting index: sum):
`0:3, 1:3, 2:3, 3:8, 4:13, 5:12, 6:6`.

| array | values |
|-------|--------|
| left[i]  | [0, 0, 0, 3, 4, 4, 4] |
| right[i] | [4, 4, 4, 4, 4, 5, 6] |

mid loop: `mid = 2`: l = left[0] = 0, r = right[4] = 4 → 3 + 3 + 13 = 19.
`mid = 3`: l = left[1] = 0, r = right[5] = 5 → 3 + 8 + 12 = 23 (better).
Final answer: `[0, 3, 5]`.

**Code:**
```python
def max_sum_of_three_subarrays(nums, k):
    n = len(nums)
    # sums[i] = sum of the length-k subarray starting at index i.
    sums = [0] * (n - k + 1)
    curr = sum(nums[:k])
    sums[0] = curr
    for i in range(1, len(sums)):
        # Slide the window: drop nums[i-1], add nums[i + k - 1].
        curr += nums[i + k - 1] - nums[i - 1]
        sums[i] = curr
    # left[i] = index of the best subarray among sums[0..i].
    # Strict '>' scanning left-to-right keeps the LEFTMOST index on ties.
    left = [0] * len(sums)
    best = 0
    for i in range(len(sums)):
        if sums[i] > sums[best]:
            best = i
        left[i] = best
    # right[i] = index of the best subarray among sums[i..end].
    # '>=' scanning right-to-left keeps the leftmost index on ties.
    right = [0] * len(sums)
    best = len(sums) - 1
    for i in range(len(sums) - 1, -1, -1):
        if sums[i] >= sums[best]:
            best = i
        right[i] = best
    max_sum = 0
    ans = [-1, -1, -1]
    # Fix the MIDDLE window; the other two must be k apart on each side.
    for mid in range(k, len(sums) - k):
        l, r = left[mid - k], right[mid + k]
        total = sums[l] + sums[mid] + sums[r]
        if total > max_sum:   # strict '>' keeps the first (leftmost) best triple
            max_sum = total
            ans = [l, mid, r]
    return ans
```

**Complexity:**
- Time: O(n) — sliding window plus two prefix scans plus one middle scan
- Space: O(n) for `sums`, `left`, `right`

**Common Mistakes & Edge Cases:**
- `n < 3*k`: no valid triple exists; the problem guarantees a valid answer, but
  the loops would skip and return `[-1, -1, -1]` — guard if needed.
- Tie-breaking: the problem demands the lexicographically smallest indices;
  the right-side scan must use `>=` (scanning rightward keeps the leftmost on
  ties), and the final mid scan must use strict `>`.
- The middle window's range is `[k, len(sums) - k - 1]` inclusive of the
  endpoints' constraints; an off-by-one here can pick an overlapping triple.
- Using `sum(nums[i:i+k])` for every window makes the precompute O(n*k); the
  sliding-window trick is required for O(n).
- All-equal arrays (every window ties) are the best stress test for the
  leftmost-index requirement.

---

### 24. Egg Dropping (SP L3 Version)

**Problem Explanation:**
You have `k` identical eggs and a building with `n` floors (numbered 1 to `n`).
There is a critical floor `f` such that eggs break when dropped from any floor
`> f` and survive from any floor `<= f`. You may drop eggs and observe
break/survive. Return the MINIMUM number of drops needed (in the worst case) to
determine `f` with certainty. For example, `k = 2`, `n = 6` → 3 drops. Input
is `k` (eggs) and `n` (floors); output is the minimum worst-case drops.

**State Definition:**
`dp(e, f)` = minimum number of drops needed in the worst case with `e` eggs and
`f` floors.

**Recurrence Relation:**
```
dp(e, f) = 1 + min over floor x of max( dp(e-1, x-1),     # egg breaks: below x
                                        dp(e,   f-x) )     # egg survives: above x
```
Drop from floor `x`: if it breaks, we lose an egg and must search the `x - 1`
floors below with `e - 1` eggs; if it survives, we keep `e` eggs and search the
`f - x` floors above. The `max` reflects the worst case (we must be safe for
both outcomes), and we pick the floor `x` that minimizes that worst case. This
is correct because the outcome at `x` splits the problem into two independent
search problems, and optimal substructure holds.

**Base Cases:**
- `dp(e, 0) = 0` (no floors to test)
- `dp(e, 1) = 1` (one floor: one drop decides)
- `dp(1, f) = f` (one egg: must test floors linearly from the bottom up)

**Intuition (Why This Works):**
This is a minimax DP: the adversary controls whether the egg breaks, so we
optimize for the worst outcome. The binary-search optimization exists because
`dp(e-1, x-1)` increases with `x` while `dp(e, f-x)` decreases with `x`; the
minimax optimum sits where they cross, so a binary search over `x` finds the
best drop floor without an O(f) scan per state.

**Step-by-Step Procedure:**
1. Handle trivial inputs: 1 egg or `n <= 1` → answer `n`.
2. Create a memo dict keyed by `(e, f)`.
3. Define recursive `dp(e, f)`:
4.   Apply base cases; check the memo.
5.   Binary search `x` in `[1, f]`:
6.     Compute `broken = dp(e-1, mid-1)` and `intact = dp(e, f-mid)`.
7.     If `broken > intact`, search lower (the max is skewed down-left); else
       search higher.
8.     Track `best = min(best, 1 + max(broken, intact))`.
9. Store and return `best`.
10. Return `dp(k, n)`.

**Worked Example (Dry Run):**
`k = 2`, `n = 6`. Key memoized values (`dp(e, f)`):

| state | computation | value |
|-------|-------------|-------|
| dp(1, x)  | linear: x  | 1..6 |
| dp(2, 1)  | base       | 1 |
| dp(2, 2)  | drop 1: max(0, 1)+1=2; drop 2: max(1, 0)+1=2 | 2 |
| dp(2, 3)  | drop 2: max(1, 1)+1=2 | 2 |
| dp(2, 4)  | drop 2: max(1, 2)+1=3; drop 3: max(2, 1)+1=3 | 3 |
| dp(2, 5)  | drop 3: max(2, 2)+1=3 | 3 |
| dp(2, 6)  | drop 3: max(dp(1,2), dp(2,3)) = max(2,2) → 3; drop 4: max(3, 2) → 4 | 3 |

Final answer: `dp(2, 6) = 3` drops (e.g. first drop at floor 3; both branches
finish in at most 2 more drops).

**Code:**
```python
def super_egg_drop(k, n):
    # Trivial cases: one egg forces a linear scan; few floors match directly.
    if k == 1 or n <= 1:
        return n
    memo = {}
    def dp(e, f):
        # Minimum worst-case drops with e eggs and f floors.
        if e == 1 or f <= 1:
            return f          # one egg -> linear; 0/1 floors -> that many drops
        key = (e, f)
        if key in memo:
            return memo[key]
        lo, hi = 1, f
        best = float("inf")
        # Binary search over the first drop floor x: dp(e-1,x-1) grows with x,
        # dp(e,f-x) shrinks, so the minimax optimum is where they cross.
        while lo <= hi:
            mid = (lo + hi) // 2
            broken = dp(e - 1, mid - 1)  # egg broke: search the floors below
            intact = dp(e, f - mid)      # egg survived: search the floors above
            # If the broken-side cost dominates, move the drop floor lower to
            # rebalance the worst case; otherwise move it higher.
            if broken > intact:
                hi = mid - 1
            else:
                lo = mid + 1
            best = min(best, 1 + max(broken, intact))
        memo[key] = best
        return best
    return dp(k, n)
```

**Complexity:**
- Time: O(k * n * log n) with memoization and binary search per state
  (the naive O(k * n^2) version drops the binary search)
- Space: O(k * n) for the memo table

**Common Mistakes & Edge Cases:**
- `k = 1` returns `n`, not 1 — a single egg must be tested floor by floor.
- One floor (`n = 1`) needs exactly 1 drop regardless of `k`.
- The recurrence takes `max` of the two outcomes (worst case) before the `min`
  over drop floors; swapping them gives the wrong answer.
- When the egg survives you still have `e` eggs (it is not consumed); use
  `dp(e, f - mid)`, not `dp(e - 1, ...)`.
- The binary-search termination must still try both sides of the crossing
  point; the `best` tracker must run on every iteration.

---

### 25. Count Vowels Permutation

**Problem Explanation:**
Count how many strings of length `n` can be built using only the vowels `a`,
`e`, `i`, `o`, `u` subject to vowel-ordering rules: each vowel may only be
FOLLOWED by certain vowels. The rules are: `a` must be followed by `e`;
`e` by `a` or `i`; `i` by `a`, `e`, `o`, or `u`; `o` by `i`; `u` by `a`. Return
the count modulo 10^9 + 7. For example, `n = 2` gives 10 valid strings. Input
is the integer `n`; output is the count.

**State Definition:**
Five scalar states, one per ending vowel: `a`, `e`, `i`, `o`, `u` = the number
of valid strings of the current length that END with that vowel.

**Recurrence Relation:**
```
a = (e + i + u)   # only e, i, u may precede a
e = (a + i)       # only a, i may precede e
i = (e + o)       # only e, o may precede i
o = (i)           # only i may precede o
u = (i + o)       # only i, o may precede u
```
To form a string of length `L` ending in `x`, take any valid string of length
`L - 1` ending in a vowel allowed to precede `x`, and append `x`. This is a
simple state-machine DP: the "state" is the last character, and the transitions
are exactly the follow rules. Correct because the follow constraint only ever
depends on the previous character.

**Base Cases:**
- Length 1: `a = e = i = o = u = 1` (one string per vowel)

**Final answer:**
`(a + e + i + o + u) % mod`.

**Intuition (Why This Works):**
The only memory needed is the previous character, so five counters are enough —
no table required. Each step applies all transitions simultaneously (using only
the old values; that is why we update the five variables together, not one at a
time). The rule set can also be read in reverse as "which vowels can come
before x", which is exactly the recurrence above.

**Step-by-Step Procedure:**
1. Initialize `a = e = i = o = u = 1` (length-1 strings).
2. Repeat `n - 1` times (each iteration extends the length by 1):
3.   Compute the new five counters simultaneously from the OLD values using
     the recurrence.
4.   Take each mod 10^9 + 7.
5. Return the sum of the five counters, mod 10^9 + 7.

**Worked Example (Dry Run):**
`n = 3` (start from `n = 1`, extend twice):

| step | a | e | i | o | u | sum |
|------|---|---|---|---|---|-----|
| base (n=1) | 1 | 1 | 1 | 1 | 1 | 5 |
| extend to n=2 | e+i+u=3 | a+i=2 | e+o=2 | i=1 | i+o=2 | 10 |
| extend to n=3 | e+i+u=2+2+2=6 | a+i=3+2=5 | e+o=2+1=3 | i=2 | i+o=2+1=3 | 19 |

Final answer for `n = 3`: `19`. (For `n = 2` the answer is the middle row's
sum, `10`.)

**Code:**
```python
def count_vowel_permutation(n):
    mod = 10**9 + 7
    # a, e, i, o, u = number of valid strings of the current length ending in
    # that vowel. Base case: length 1, one string per vowel.
    a = e = i = o = u = 1
    for _ in range(n - 1):
        # Follow rules translated to "which vowels may come BEFORE each vowel":
        #   a <- e, i, u        e <- a, i
        #   i <- e, o           o <- i          u <- i, o
        # All five must be computed from the OLD values simultaneously.
        a, e, i, o, u = (e + i + u) % mod, (a + i) % mod, \
                        (e + o) % mod, i % mod, (i + o) % mod
    return (a + e + i + o + u) % mod
```

**Complexity:**
- Time: O(n) — n - 1 iterations of constant work
- Space: O(1) — five counters

**Common Mistakes & Edge Cases:**
- `n = 1` → 5 (each single vowel is valid); the loop must run `n - 1` times,
  not `n`.
- Updating the counters one at a time (sequentially) corrupts the transitions
  because later counters read already-updated values; use a simultaneous
  tuple assignment.
- Missing a follow rule (e.g. forgetting that `i` may be followed by `u`)
  changes the count; `n = 5` must be 68.
- The mod must be applied at every step; values grow astronomically fast.
- Reverse the rules carefully: `a` followed by `e` means `e` gets contributions
  from `a`, not the other way around.

---

## Summary & Study Plan

```text
┌────────────┬─────────┬─────────────────────────────────────────────────────────┐
│ Difficulty │ Problems│ Key Techniques to Master                                │
├────────────┼─────────┼─────────────────────────────────────────────────────────┤
│ Easy       │ 1-3     │ 1D DP, Fibonacci recurrence, two-variable state       │
│            │         │ → Practice: climbing stairs, house robber, min cost    │
├────────────┼─────────┼─────────────────────────────────────────────────────────┤
│ Medium     │ 4-8     │ 2D DP tables, LIS (patience sort), LCS, string DP     │
│            │         │ → Practice: fill tables manually, understand transitions│
├────────────┼─────────┼─────────────────────────────────────────────────────────┤
│ Hard       │ 9-15    │ Interval DP, minimax game theory, reverse DP           │
│            │         │ → Practice: burst balloons, dungeon game, stone games  │
├────────────┼─────────┼─────────────────────────────────────────────────────────┤
│ SP L3      │ 16-25   │ Bitmask DP, tree DP, advanced interval, state machine  │
│            │         │ → Practice: TSP, matrix chain, egg drop, vowel perm    │
└────────────┴─────────┴─────────────────────────────────────────────────────────┘

Recommended study order:
  Week 1: Easy (1-3) + Medium (4-8) — master the basics
  Week 2: Hard (9-15) — interval DP and game theory
  Week 3: SP L3 (16-25) — advanced patterns
  Week 4: Mix all — solve under timed conditions (30 min each)
```

### Pattern Summary Table

```text
┌───────────────────────────────────────────────────────────────────────────────────────┐
│  Pattern         │ Problems    │ Template                                           │
├───────────────────┼─────────────┼───────────────────────────────────────────────────┤
│  Fibonacci/1D     │ 1, 2, 3     │ dp[i] = f(dp[i-1], dp[i-2])                      │
│  LIS              │ 4           │ Patience sort O(n log n) or O(n²) DP             │
│  Unbounded Knapsack│ 5, 6, 7    │ Coin change, word break (loop L→R for reuse)     │
│  LCS/Edit Distance│ 8, 10       │ 2D match/no-match transition                     │
│  Interval DP      │ 9, 12, 18, 19, 20 │ dp[i][j] on subarrays, fill by length    │
│  Reverse DP       │ 14          │ Work backwards (dungeon game)                     │
│  Game/Minimax     │ 15          │ dp[i] = best when opponent plays optimally       │
│  Bitmask DP       │ 16          │ dp[mask][last] for visiting subsets of cities    │
│  Tree DP          │ 17          │ Post-order DFS, (take, skip) tuple return        │
│  State Machine    │ 25          │ 5 vowel states with transition rules             │
│  Precompute+DP    │ 22, 23      │ Build palindrome table, then 1D DP on top       │
│  Binary Search DP │ 24          │ Minimax with BS on optimal floor choice          │
└───────────────────┴─────────────┴───────────────────────────────────────────────────┘
```
