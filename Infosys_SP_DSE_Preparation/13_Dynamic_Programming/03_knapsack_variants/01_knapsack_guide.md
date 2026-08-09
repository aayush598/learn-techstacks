# Knapsack Variants — Complete Guide

This guide teaches every classic knapsack variant from scratch. You do not need prior DP
knowledge. The single most important idea in this entire file is the **loop-direction rule**:
0/1-style problems iterate the capacity RIGHT-TO-LEFT, unbounded-style problems iterate it
LEFT-TO-RIGHT. Every problem below explains why its direction is what it is.

## Decision Tree for Knapsack Problems

Use this tree whenever you meet a new problem: answer the questions in order and you will
know exactly which pattern (and which loop direction) to use.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    KNAPSACK PATTERN DECISION TREE                        │
│                                                                          │
│  "Can I pick each item at most once?"                                    │
│       │                                                                  │
│       ├─ YES → 0/1 Knapsack (loop capacity RIGHT-TO-LEFT)              │
│       │                                                                  │
│       └─ NO → "Can I pick unlimited times?"                             │
│                │                                                         │
│                ├─ YES → Unbounded Knapsack (loop capacity LEFT-TO-RIGHT)│
│                │                                                         │
│                └─ NO → "Limited count[i] for each item?"                │
│                         │                                                │
│                         └─ YES → Bounded Knapsack (binary splitting)    │
│                                                                          │
│  Variants of 0/1 Knapsack:                                              │
│    - Subset Sum?      → dp[i][s] = dp[i-1][s] or dp[i-1][s-num[i]]    │
│    - Equal Partition? → target = sum/2, check subset sum                │
│    - Count subsets?   → dp[i][s] = dp[i-1][s] + dp[i-1][s-num[i]]     │
│    - Min diff?        → closest subset sum to total/2                   │
│                                                                          │
│  Variants of Unbounded:                                                  │
│    - Coin Change (min)?  → dp[a] = min(dp[a], dp[a-coin] + 1)          │
│    - Coin Change (count)?→ dp[a] += dp[a-coin]                          │
│    - Rod Cutting?        → dp[i] = max over all cut lengths             │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 0/1 Knapsack Problem

### 0/1 Knapsack

**🔗 Practice Link:** [0/1 Knapsack](https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10)

**Problem Explanation:**
You are a thief with a backpack of capacity `W`. You have `n` items; item `i` has weight
`wt[i]` and value `val[i]`. You must pick a set of items whose total weight is **at most** `W`
to maximize total value. The name "0/1" means each item is either fully taken (1) or skipped (0) —
you cannot take half an item, and you cannot take the same item twice. Return the maximum value.

**State Definition:**
`dp[i][w]` = maximum value achievable using only the first `i` items (items `0..i-1`) with a
backpack of capacity exactly up to `w` (i.e., total weight used `<= w`).

**Recurrence Relation:**
```
dp[i][w] = dp[i-1][w]                          if w < wt[i-1]
dp[i][w] = max(dp[i-1][w],                     skip item i-1
               val[i-1] + dp[i-1][w - wt[i-1]])   take item i-1, if it fits
```
(`dp[i][w]` is the better of two options: leave item `i-1` out, or put it in and add its value
to the best value that fits in the leftover capacity `w - wt[i-1]`.)

**Base Cases:**
- `dp[0][w] = 0` for every `w`: with zero items you can carry value 0.
- `dp[i][0] = 0` for every `i`: with zero capacity you can carry value 0.
- (The recurrence is only valid for `i >= 1`; the row `i = 0` is the "no items" row.)

**Intuition (Why This Works):**
At every item you face exactly one choice: **include it or skip it**. This binary choice,
made against a capacity budget, is what makes it a DP problem: the best value for capacity `w`
with `i` items depends only on the best value for smaller capacities with `i-1` items, so
subproblems overlap and can be reused. Because each item may be used **at most once**, the
1D version must iterate capacity **right-to-left**: that way `dp[w - wt[i]]` still holds the
value from the *previous* item's round and can never be contaminated by the current item —
so the current item can never be used twice. (A concrete counter-example is in the dry run.)

**Step-by-Step Procedure:**
1. Let `n = len(wt)`. Create a 2D table `dp` of size `(n+1) x (W+1)` filled with 0.
2. Set the entire base row `dp[0][:] = 0` (already 0) and the base column `dp[:][0] = 0`.
3. For `i` from `1` to `n` (item index `i-1` in the arrays):
   - For `w` from `0` to `W`:
     - If `wt[i-1] > w`, the item cannot fit → `dp[i][w] = dp[i-1][w]`.
     - Else `dp[i][w] = max(dp[i-1][w], val[i-1] + dp[i-1][w - wt[i-1]])`.
4. The answer is `dp[n][W]`.
5. (Space optimization) Notice `dp[i][w]` only reads row `i-1`. Keep one array `dp[0..W]`.
6. For each item, update capacities `w` from `W` **down to** `wt[i-1]`:
   `dp[w] = max(dp[w], val[i-1] + dp[w - wt[i-1]])`.
7. Return `dp[W]`. The 1D version gives the same answer with O(W) memory.

**Worked Example (Dry Run):**
Items `wt=[1,3,4,5]`, `val=[1,4,5,7]`, `W=7`. Full 2D table, row by row (each row means
"considering the first i items"):

```
dp[i][w] = max value using items 0..i-1 with capacity w

     Capacity →   0    1    2    3    4    5    6    7
  ┌─────────────────────────────────────────────────────┐
  │  0 items:  [  0    0    0    0    0    0    0    0 ]│  ← base row (no items → value 0)
  ├─────────────────────────────────────────────────────┤
  │  item 1:   [  0    1    1    1    1    1    1    1 ]│  wt=1, val=1
  ├─────────────────────────────────────────────────────┤     ↑ only 1 item of wt=1, fills any w≥1
  │  item 2:   [  0    1    1    4    5    5    5    5 ]│  wt=3, val=4
  ├─────────────────────────────────────────────────────┤     ↑ at w≥3 can take item 2
  │  item 3:   [  0    1    1    4    5    6    6    9 ]│  wt=4, val=5
  ├─────────────────────────────────────────────────────┤     ↑ at w=7: items 2+3 = 4+5 = 9
  │  item 4:   [  0    1    1    4    5    7    8    9 ]│  wt=5, val=7
  └─────────────────────────────────────────────────────┘     ↑ at w=7: 9 still best

Answer: 9  (take the items with weights 3 and 4: values 4 + 5 = 9)

Reading one cell: dp[3][7] = 9 means "using items {1,2,3} with capacity 7 the best is 9":
  dp[2][7] = 5 (skip item 3)  vs  val[3] + dp[2][7-4] = 5 + dp[2][3] = 5 + 4 = 9 (take item 3).
```

State transition used by the code:
```
  ┌───────────────────────────────────────────────────────────────┐
  │  if wt[i-1] > w:                                              │
  │      dp[i][w] = dp[i-1][w]           # Can't fit, skip item   │
  │  else:                                                         │
  │      dp[i][w] = max(dp[i-1][w],            # Skip item i      │
  │                     val[i-1] + dp[i-1][w-wt[i-1]]) # Take it │
  └───────────────────────────────────────────────────────────────┘
```

Tracing the space-optimized 1D version (`dp = [0]*8`, update `w` from 7 down to `wt[i-1]`):

```
Item 1 (wt=1, val=1), loop w=7→1:
  w=7: dp[7] = max(0, 1+dp[6]) = 1
  w=6: dp[6] = max(0, 1+dp[5]) = 1
  ...
  w=1: dp[1] = max(0, 1+dp[0]) = 1
  dp = [0, 1, 1, 1, 1, 1, 1, 1]

Item 2 (wt=3, val=4), loop w=7→3:
  w=7: dp[7] = max(1, 4+dp[4]) = max(1,4+1) = 5
  w=6: dp[6] = max(1, 4+dp[3]) = max(1,4+1) = 5
  w=5: dp[5] = max(1, 4+dp[2]) = max(1,4+1) = 5
  w=4: dp[4] = max(1, 4+dp[1]) = max(1,4+1) = 5
  w=3: dp[3] = max(1, 4+dp[0]) = max(1,4+0) = 4
  dp = [0, 1, 1, 4, 5, 5, 5, 5]

Item 3 (wt=4, val=5), loop w=7→4:
  w=7: dp[7] = max(5, 5+dp[3]) = max(5,5+4) = 9
  w=6: dp[6] = max(5, 5+dp[2]) = max(5,5+1) = 6
  w=5: dp[5] = max(5, 5+dp[1]) = max(5,5+1) = 6
  w=4: dp[4] = max(5, 5+dp[0]) = max(5,5+0) = 5
  dp = [0, 1, 1, 4, 5, 6, 6, 9]

Item 4 (wt=5, val=7), loop w=7→5:
  w=7: dp[7] = max(9, 7+dp[2]) = max(9,7+1) = 9
  w=6: dp[6] = max(6, 7+dp[1]) = max(6,7+1) = 8
  w=5: dp[5] = max(6, 7+dp[0]) = max(6,7+0) = 7
  dp = [0, 1, 1, 4, 5, 7, 8, 9]   ← Answer: 9
```

Counter-example proving you MUST go right-to-left in 0/1 knapsack. Take one item
`wt=[2]`, `val=[3]`, `W=6`:

```
LEFT-TO-RIGHT (WRONG for 0/1):           RIGHT-TO-LEFT (CORRECT for 0/1):
  w=2: dp[2]=max(0,3+dp[0])=3             w=6: dp[6]=max(0,3+dp[4])=3
  w=3: dp[3]=max(0,3+dp[1])=3             w=5: dp[5]=max(0,3+dp[3])=3
  w=4: dp[4]=max(0,3+dp[2])=6  ← reuse!   w=4: dp[4]=max(0,3+dp[2])=3
  w=5: dp[5]=max(0,3+dp[3])=6             w=3: dp[3]=max(0,3+dp[1])=3
  w=6: dp[6]=max(0,3+dp[4])=9  ← reuse!   w=2: dp[2]=max(0,3+dp[0])=3
  answer = 9 (used the item 3× !)          answer = 3 (item used once, correct)

Left-to-right reuses the item: dp[4] reads dp[2] which was ALREADY updated with item 1,
so the same item gets added twice. Right-to-left reads only stale (previous-item) values.
```

**Code:**

```python
def knapsack_2d(W: int, wt: list, val: list) -> int:
    n = len(wt)
    # dp[i][w] = max value using the first i items (indices 0..i-1) within capacity w
    # (n+1) rows (0 items .. all n items) and (W+1) columns (capacity 0..W)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):          # i-1 is the current item's index in wt/val
        for w in range(W + 1):         # try every capacity from 0 up to W
            if wt[i - 1] > w:
                # Item is heavier than this capacity -> it cannot be taken.
                dp[i][w] = dp[i - 1][w]
            else:
                # Two choices: skip the item, or take it and add its value to the
                # best value that fits in the remaining capacity w - wt[i-1].
                dp[i][w] = max(dp[i - 1][w],
                               val[i - 1] + dp[i - 1][w - wt[i - 1]])
    # Best value using all n items with the full capacity W
    return dp[n][W]


def knapsack_optimized(W: int, wt: list, val: list) -> int:
    n = len(wt)
    # 1D table: dp[w] = best value achievable with capacity w so far.
    # We overwrite it once per item, so after all items it equals the 2D last row.
    dp = [0] * (W + 1)
    for i in range(n):
        # CRITICAL: iterate capacity RIGHT-TO-LEFT to prevent using item i twice.
        # Going down to wt[i] ensures w - wt[i] >= 0 so we never index out of range.
        for w in range(W, wt[i] - 1, -1):
            # dp[w] (skip) vs take item i + best value in remaining capacity.
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]])
    return dp[W]

# Why right-to-left?
# If we go left-to-right, dp[w - wt[i]] might have ALREADY been updated in this
# iteration (using item i), allowing item i to be used twice. Example above shows
# the single item wt=[2], val=[3] producing 9 (3 copies) when going left-to-right.
#
# Right-to-left ensures dp[w - wt[i]] still reflects the PREVIOUS iteration,
# so each item is considered at most once.

# Time: O(n x W), Space: O(W)
```

**Complexity:**
- Time: O(n x W) for both versions (every item visits every capacity once).
- Space: O(n x W) for the 2D table; O(W) for the 1D optimized version.

**Common Mistakes & Edge Cases:**
- **Wrong loop direction in the 1D version.** Iterating capacity left-to-right lets the same
  item be taken multiple times (see the counter-example above). Always go `W -> wt[i]`.
- **Off-by-one on capacity.** The loop must stop at `wt[i]` (`range(W, wt[i]-1, -1)`), not at
  `wt[i]+1` or `0`. Starting below `wt[i]` would index `w - wt[i]` with a negative number.
- **Forgetting the base row.** In the 2D version row 0 must be all 0s; in the 1D version the
  array starts all 0s, which is the same thing.
- **Empty input** (`wt=[]`): every loop body is skipped and `dp[W]` stays 0 — correct (no items,
  no value).
- **An item heavier than W:** it can never be taken; the `if wt[i-1] > w` guard (2D) or the
  loop start `wt[i]` (1D) handles this automatically — no special case needed.

---

## Subset Sum Problem

### Subset Sum

**🔗 Practice Link:** [Subset Sum](https://www.geeksforgeeks.org/subset-sum-problem-dp-25)

**Problem Explanation:**
Given an array of **positive** integers `nums` and a target sum `target`, decide whether there
exists some subset of the numbers whose sum equals `target` exactly. A "subset" means each
number is used at most once (0/1!). Return `True` if such a subset exists, else `False`.

**State Definition:**
`dp[i][s]` = `True` if a subset of the first `i` numbers (`nums[0..i-1]`) sums to exactly `s`;
`False` otherwise.

**Recurrence Relation:**
```
dp[i][s] = dp[i-1][s]  or  dp[i-1][s - nums[i-1]]   (when nums[i-1] <= s)
```
(`dp[i][s]` is `True` if the sum `s` was already reachable without number `i-1`, or if it
becomes reachable by adding `nums[i-1]` to a previously reachable sum `s - nums[i-1]`.)

**Base Cases:**
- `dp[i][0] = True` for every `i`: the empty subset sums to 0.
- `dp[0][s] = False` for every `s > 0`: with no numbers, only sum 0 is reachable.

**Intuition (Why This Works):**
Subset Sum is 0/1 knapsack in disguise: the "weight" and "value" are both the number itself,
the capacity is `target`, and instead of maximizing value we just ask whether the full capacity
`target` is reachable. Each number is used at most once, so — exactly like 0/1 knapsack — the
1D version must update the sum loop **right-to-left**; going left-to-right would let the same
number be added multiple times (see the counter-example in the 0/1 section).

**Step-by-Step Procedure:**
1. Create `dp` of size `target + 1`, all `False`; set `dp[0] = True` (sum 0 = empty subset).
2. For each `num` in `nums`:
   - For `s` from `target` **down to** `num`:
     - If `dp[s - num]` is `True`, set `dp[s] = True` (this `num` can extend a reachable sum).
3. (Optional) After each number, if `dp[target]` is `True`, return `True` early.
4. Return `dp[target]`.
5. (2D version, for understanding only) Build `(n+1) x (target+1)` with row 0 = `True` only at
   column 0, then for each `(i, s)` apply the recurrence above.

**Worked Example (Dry Run):**
`nums = [3, 34, 4, 12, 5, 2]`, `target = 9`. Full 2D table (T = True, F = False):

```
dp[i][s] = True if subset of nums[0..i-1] sums to s

     Sum →      0    1    2    3    4    5    6    7    8    9
  ┌──────────────────────────────────────────────────────────────┐
  │  0 nums:  [  T    F    F    F    F    F    F    F    F    F ]│  ← empty subset = sum 0
  ├──────────────────────────────────────────────────────────────┤
  │  num=3:   [  T    F    F    T    F    F    F    F    F    F ]│  ← {3} reaches sum 3
  ├──────────────────────────────────────────────────────────────┤
  │  num=34:  [  T    F    F    T    F    F    F    F    F    F ]│  ← 34 > target, no new sums
  ├──────────────────────────────────────────────────────────────┤
  │  num=4:   [  T    F    F    T    T    F    F    T    F    F ]│  ← {4}=4, {3,4}=7
  ├──────────────────────────────────────────────────────────────┤     At s=7: dp[3]=T → dp[7]=T
  │  num=12:  [  T    F    F    T    T    F    F    T    F    F ]│     At s=4: dp[0]=T → dp[4]=T
  ├──────────────────────────────────────────────────────────────┤     12 > target, no new sums
  │  num=5:   [  T    F    F    T    T    T    F    T    T    T ]│  ← {5}=5, {3,5}=8, {4,5}=9
  ├──────────────────────────────────────────────────────────────┤     At s=9: dp[4]=T → dp[9]=T
  │  num=2:   [  T    F    T    T    T    T    T    T    T    T ]│  ← {2}=2, {4,2}=6, {5,2}=7
  └──────────────────────────────────────────────────────────────┘     everything stays reachable
                                                      ▲
                                            Answer: T ({3,4,2}=9, also {4,5}=9)
```

1D version, same input (early rows only; the full trace after every number is):
```
  start:       [T, F, F, F, F, F, F, F, F, F]
  after num=3: [T, F, F, T, F, F, F, F, F, F]
  after num=34:[T, F, F, T, F, F, F, F, F, F]   (34 > 9, no change)
  after num=4: [T, F, F, T, T, F, F, T, F, F]
  after num=12:[T, F, F, T, T, F, F, T, F, F]   (12 > 9, no change)
  after num=5: [T, F, F, T, T, T, F, T, T, T]   ← dp[9] just became T
  after num=2: [T, F, T, T, T, T, T, T, T, T]   ← dp[9] stays T → answer True
```

**Code:**

```python
def subset_sum_2d(nums: list, target: int) -> bool:
    n = len(nums)
    # dp[i][s] = True if a subset of the first i numbers sums to exactly s
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = True                 # empty subset always sums to 0

    for i in range(1, n + 1):           # consider number nums[i-1]
        for s in range(1, target + 1):
            # Option 1: ignore nums[i-1] -> previous answer carries over
            dp[i][s] = dp[i - 1][s]
            # Option 2: use nums[i-1] if it fits, extending a smaller reachable sum
            if nums[i - 1] <= s and dp[i - 1][s - nums[i - 1]]:
                dp[i][s] = True
    return dp[n][target]


def subset_sum_optimized(nums: list, target: int) -> bool:
    # 1D version: dp[s] = True if sum s is reachable with the numbers seen so far
    dp = [False] * (target + 1)
    dp[0] = True                        # base case: sum 0 is always achievable (empty subset)
    for num in nums:
        # Right-to-left (0/1 style!) so num is used at most once per path.
        for s in range(target, num - 1, -1):
            if dp[s - num]:             # if s-num was reachable, s becomes reachable
                dp[s] = True
        if dp[target]:                  # early termination once we have a solution
            return True
    return dp[target]

# Time: O(n x target), Space: O(target)
```

**Complexity:**
- Time: O(n x target).
- Space: O(n x target) for the 2D version; O(target) for the 1D version.

**Common Mistakes & Edge Cases:**
- **Wrong loop direction.** Going `s = num .. target` would reuse the same number multiple
  times (e.g., `nums=[3]`, `target=6` would wrongly return `True` as `3+3`).
- **`target = 0`:** must return `True` (empty subset). This is exactly the `dp[0] = True` base case.
- **Numbers larger than `target`:** skipped automatically because the inner loop starts at `num`.
- **`nums` empty with `target > 0`:** returns `False`, correct.
- **Early exit bugs:** returning `True` early is safe only after updating with the current
  number; return `False` only after processing all numbers.

---

## Equal Subset Sum Partition

### Equal Subset Sum Partition

**🔗 Practice Link:** [Equal Subset Sum Partition](https://leetcode.com/problems/partition-equal-subset-sum/)

**Problem Explanation:**
Given an array `nums`, can it be split into two subsets whose sums are equal? Both subsets are
non-empty partitions — every element goes into exactly one of the two. Return `True`/`False`.

**State Definition:**
Same as Subset Sum: `dp[s]` = `True` if some subset of the numbers seen so far sums to `s`
(here `s` ranges up to `target = total/2`).

**Recurrence Relation:**
```
dp[s] = dp[s]  or  dp[s - num]        (for each num, s iterated right-to-left)
```
(`dp[s]` becomes `True` once we can extend a reachable smaller sum `s - num` with `num`.)

**Base Cases:**
- `dp[0] = True`: the empty subset sums to 0.
- If `sum(nums)` is odd → return `False` immediately (two equal integer halves can't sum to an odd number).

**Intuition (Why This Works):**
If the array can be split into two equal-sum subsets, each half must sum to `total/2`. So this
problem is *exactly* Subset Sum with `target = total/2`: find one subset of sum `total/2`, and
the remaining elements automatically form the other half with the same sum. It is a 0/1 problem
(each element used once) so the sum loop runs **right-to-left** with the same counter-example
reasoning as Subset Sum / 0/1 knapsack.

**Step-by-Step Procedure:**
1. Compute `total = sum(nums)`.
2. If `total % 2 != 0`, return `False` (an odd total can't be halved into equal integers).
3. Set `target = total // 2`.
4. Initialize `dp = [False] * (target + 1)` and set `dp[0] = True`.
5. For each `num` in `nums`, for `s` from `target` down to `num`: set `dp[s] = True` if `dp[s - num]`.
6. (Optional) if `s == target` became `True`, return `True` immediately.
7. Return `dp[target]`.

**Worked Example (Dry Run):**
`nums = [1, 5, 11, 5]`: `total = 22` (even), `target = 11`.

```
dp (size 12)   s: 0     1     2     3     4     5     6     7     8     9     10    11
start:            T     F     F     F     F     F     F     F     F     F     F     F
after 1:          T     T     F     F     F     F     F     F     F     F     F     F
after 5:          T     T     F     F     F     T     T     F     F     F     F     F   ← {5}, {1,5}
after 11:         T     T     F     F     F     T     T     F     F     F     F     T   ← {11}
after 5:          T     T     F     F     F     T     T     F     F     F     T     T   ← +{5,5},{1,5,5}
                                                                    ↑ dp[10]=dp[5] (after 11) = T
```

Reading the last row: `dp[11] = T` because `dp[11 - 5] = dp[6] = T` (subset `{1, 5}` plus the new
`5` gives `{1, 5, 5} = 11`). The other subset `{11}` also sums to `11`. Answer: `True`.

A quick way to see it: `{1, 5, 5}` → sum 11, and `{11}` → sum 11. Both halves equal → partition works.

**Code:**

```python
def can_partition(nums: list) -> bool:
    total = sum(nums)
    if total % 2 != 0:
        return False                    # odd sum can't be split into two equal integers

    target = total // 2                 # each half must sum to exactly this
    dp = [False] * (target + 1)
    dp[0] = True                        # empty subset reaches sum 0
    for num in nums:
        # 0/1 knapsack style: right-to-left so each num is used at most once
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                dp[s] = True            # extend reachable sum s-num with this num
                if s == target:         # early exit as soon as the goal half is reachable
                    return True
    return dp[target]

# Time: O(n x target), Space: O(target)
```

**Complexity:**
- Time: O(n x target), where `target = total/2`.
- Space: O(target).

**Common Mistakes & Edge Cases:**
- **Forgetting the odd-sum check.** `[1,2,2]` sums to 5 (odd) → must be `False`; without the
  check you would compute `target = 2` and wrongly search the wrong half.
- **`nums` with a single element** like `[1]`: total = 1, odd → `False`. A single element can
  never be split into two non-empty equal halves.
- **All zeros** `[0,0]`: total = 0, target = 0 → returns `True` immediately; arguably correct
  (each half sums to 0), but be aware.
- **Wrong loop direction** lets one number be used in both halves → false positives.
- **`target` is large** (e.g., `total/2` near 10^6): the boolean DP array is fine memory-wise,
  but O(n x target) may be too slow — that is inherent to this approach.

---

## Count Subsets with Given Sum

### Count Subsets with Given Sum

**🔗 Practice Link:** [Count Subsets with Given Sum](https://www.geeksforgeeks.org/perfect-sum-problem)

**Problem Explanation:**
Given an array `nums` of positive integers and a target sum, count **how many different
subsets** sum to exactly `target`. Each element is used at most once, and the empty subset
counts toward `target = 0`. Return the count as an integer.

**State Definition:**
`dp[s]` = number of subsets (of the numbers seen so far) that sum to exactly `s`.
(2D: `dp[i][s]` = number of subsets of the first `i` numbers summing to `s`.)

**Recurrence Relation:**
```
dp[i][s] = dp[i-1][s]  +  dp[i-1][s - nums[i-1]]     (when nums[i-1] <= s)
```
(The subsets are partitioned into two disjoint groups: those that don't contain number
`i-1` (count `dp[i-1][s]`) plus those that do (count `dp[i-1][s - nums[i-1]]`), so we add.)

**Base Cases:**
- `dp[i][0] = 1` for every `i`: there is exactly one subset summing to 0 — the empty subset.
- `dp[0][s] = 0` for `s > 0`: with no numbers, no positive sum is reachable.

**Intuition (Why This Works):**
This is Subset Sum with "+=" instead of "or": at each number you make the same include/skip
choice, but now you accumulate the *number of ways* rather than a boolean. Skip keeps all
existing ways; include adds all ways that came from the smaller sum `s - num`. Since each
element is used once, the 1D loop must go **right-to-left**; left-to-right would count
solutions that reuse the same element. A word of caution: if `nums` contains `0`s, the count
becomes more subtle (see edge cases).

**Step-by-Step Procedure:**
1. Initialize `dp = [0] * (target + 1)`; set `dp[0] = 1`.
2. For each `num` in `nums`:
   - For `s` from `target` **down to** `num`:
     - `dp[s] += dp[s - num]` (every subset summing to `s - num` becomes one summing to `s`).
3. Return `dp[target]`.
4. (Memoized version) Define `count(i, target)` = ways using first `i+1` numbers; `1` if
   `target == 0`, `0` if `i < 0`; otherwise sum of the skip branch and the take branch
   (`take` only when `nums[i] <= target`). Cache by `(i, target)`.

**Worked Example (Dry Run):**
`nums = [2, 3, 5, 6, 8, 10]`, `target = 10`. 1D `dp` after each number:

```
          s:   0   1   2   3   4   5   6   7   8   9   10
start:        [1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
after  2:     [1,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0]    {2}
after  3:     [1,  0,  1,  1,  0,  1,  0,  0,  0,  0,  0]    +{3},{2,3}
after  5:     [1,  0,  1,  1,  0,  2,  0,  1,  1,  0,  1]    dp[5]=2 ({5},{2,3})
after  6:     [1,  0,  1,  1,  0,  2,  1,  1,  2,  1,  1]    dp[10]=1 ({2,3,5})
after  8:     [1,  0,  1,  1,  0,  2,  1,  1,  3,  1,  2]    dp[10]=2 (+{2,8})
after 10:     [1,  0,  1,  1,  0,  2,  1,  1,  3,  1,  3]    dp[10]=3 (+{10})
                                                                  ↑
Answer: 3  →  the subsets {2, 8}, {10}, {2, 3, 5} all sum to 10.
```

**Code:**

```python
def count_subsets_memo(nums: list, target: int, i: int = None, memo: dict = None) -> int:
    # Recursive version with memoization. count(i, target) = ways using nums[0..i].
    if memo is None:
        memo = {}
    if i is None:
        # Public entry point: start from the last index and an empty cache
        return count_subsets_memo(nums, target, len(nums) - 1, memo)
    if target == 0:
        return 1                        # base: exactly one way — the empty subset
    if i < 0:
        return 0                        # base: ran out of numbers before hitting target
    key = (i, target)
    if key in memo:
        return memo[key]                # subproblem already solved -> reuse it

    # Skip nums[i]: ways stay as if this number never existed
    ways = count_subsets_memo(nums, target, i - 1, memo)
    # Take nums[i] (only if it fits): add ways to reach (target - nums[i])
    if nums[i] <= target:
        ways += count_subsets_memo(nums, target - nums[i], i - 1, memo)
    memo[key] = ways                     # store before returning (memoization)
    return ways


def count_subsets_tab(nums: list, target: int) -> int:
    # 2D tabulation: dp[i][s] = # subsets of the first i numbers summing to s
    n = len(nums)
    dp = [[0] * (target + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = 1                    # base: exactly one empty subset per prefix
    for i in range(1, n + 1):
        for s in range(1, target + 1):
            dp[i][s] = dp[i - 1][s]     # subsets that skip nums[i-1]
            if nums[i - 1] <= s:
                # add subsets that include nums[i-1]
                dp[i][s] += dp[i - 1][s - nums[i - 1]]
    return dp[n][target]


def count_subsets_optimized(nums: list, target: int) -> int:
    # 1D version, 0/1 style (right-to-left so each number is used once per subset)
    dp = [0] * (target + 1)
    dp[0] = 1                           # empty subset sums to 0
    for num in nums:
        for s in range(target, num - 1, -1):
            if dp[s - num] > 0:         # only propagate nonzero counts
                dp[s] += dp[s - num]    # each subset summing to s-num yields one for s
    return dp[target]

# Example: nums = [2, 3, 5, 6, 8, 10], target = 10
# Answer: 3  ({2, 8}, {10}, {2, 3, 5})

# Time: O(n x target), Space: O(target)  (memo: O(n x target) cache)
```

**Complexity:**
- Time: O(n x target) for all three versions (memo visits each `(i, s)` state at most once).
- Space: O(n x target) for memo and the 2D table; O(target) for the 1D version.

**Common Mistakes & Edge Cases:**
- **Zeros in the array.** `nums=[0]`, `target=0`: every subset sums to 0, so the true count is
  2 (`{}`, `{0}`). The 1D version handles this (adding `num=0` doubles every count), but the
  memoized version as written returns 1 (it bails out as soon as `target == 0`). If zeros are
  possible, prefer the tabulated versions or adjust the memo base cases.
- **Wrong loop direction** counts permutations/reuses of the same number.
- **`target = 0`** returns 1 (the empty subset) — do not return 0.
- **`nums` empty and `target > 0`** returns 0, correct.
- **Overflow/performance:** counts can grow huge for many numbers; in interviews ask whether
  the count fits in an `int`.

---

## Minimum Subset Sum Difference

### Minimum Subset Sum Difference

**🔗 Practice Link:** [Minimum Subset Sum Difference](https://www.geeksforgeeks.org/partition-a-set-into-two-subsets-such-that-the-difference-of-subset-sums-is-minimum)

**Problem Explanation:**
Given an array `nums`, partition it into **two subsets** (every element in exactly one) so that
the absolute difference `|sum(S1) - sum(S2)|` is as small as possible. Return that minimum
difference. This is the same as "last stone weight II" (smash stones together).

**State Definition:**
`dp[s]` = `True` if some subset of the numbers seen so far sums to exactly `s`, where `s`
ranges `0..target` and `target = total // 2`.

**Recurrence Relation:**
```
dp[s] = dp[s]  or  dp[s - num]        (for each num, s iterated right-to-left)
```
(Subset Sum recurrence — a sum `s` is reachable once we can extend reachable sum `s - num`.)

**Base Cases:**
- `dp[0] = True`: the empty subset sums to 0.
- `total = sum(nums)`, `target = total // 2`.

**Intuition (Why This Works):**
If one subset sums to `s`, the other sums to `total - s`, so the difference is
`|total - 2s|`. To minimize it, we want the subset sum `s` as close to `total/2` as possible,
and since difference is symmetric (`s` vs `total - s`), we only need to scan reachable sums up
to `target = total/2`. We find the largest reachable `s <= target`, and the answer is
`total - 2s`. Still a 0/1 problem → the sum loop iterates **right-to-left**.

**Step-by-Step Procedure:**
1. Compute `total = sum(nums)` and `target = total // 2`.
2. Initialize `dp = [False] * (target + 1)`, set `dp[0] = True`.
3. For each `num`, for `s` from `target` down to `num`: set `dp[s] = True` if `dp[s - num]`.
4. Loop `s` from `target` down to `0`; the first `s` with `dp[s] == True` is the closest
   reachable sum to `total/2`.
5. Return `total - 2 * s`.

**Worked Example (Dry Run):**
`nums = [1, 6, 11, 5]`: `total = 23`, `target = 11`.

```
reachable sums within 0..11 (only sums up to target matter) after each number:
  start:    0
  after 1:  0 1
  after 6:  0 1 6 7
  after 11: 0 1 6 7 11
  after 5:  0 1 5 6 7 11
                               ↑ scan from 11 downward, first reachable sum is 11

Answer: total - 2*s = 23 - 2*11 = 1.
  (Partition {6,5} and {1,11}: sums 11 and 12 → difference 1.)
```

**Code:**

```python
def min_subset_diff(nums: list) -> int:
    total = sum(nums)
    target = total // 2                 # we only care about sums up to half the total
    dp = [False] * (target + 1)
    dp[0] = True                        # sum 0 always reachable (empty subset)
    for num in nums:                    # 0/1 style: each number used once
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                dp[s] = True            # mark s reachable via s-num + num
    # Find the closest reachable sum to total/2, scanning from largest to smallest
    for s in range(target, -1, -1):
        if dp[s]:
            return total - 2 * s        # |s - (total - s)| = |total - 2s|
    return total                        # unreachable in practice (s=0 always reachable)

# Example: nums = [1, 6, 11, 5]
# sum = 23, target = 11
# Closest reachable sum <= target is 11 ({6, 5})
# Answer: 23 - 2*11 = 1

# Time: O(n x target), Space: O(target)
```

**Complexity:**
- Time: O(n x target).
- Space: O(target).

**Common Mistakes & Edge Cases:**
- **Symmetric scanning is unnecessary below `target`.** The min difference is always achieved
  by the closest reachable `s <= total/2`; scanning only `0..target` (not the whole `0..total`)
  is correct because `s` and `total - s` are symmetric.
- **Odd vs even total.** With odd total the minimum difference can't be 0; e.g. `[1,2]` →
  answer 1, not 0.
- **Single element** `[5]`: total=5, target=2, reachable sums ≤2 are just {0} → answer 5
  (one empty subset, one full subset). Correct.
- **Wrong loop direction** reuses numbers and marks sums that are actually unreachable.
- **`dp[s - num]` index safety:** the inner loop must stop at `num` so `s - num >= 0`.

---

## Unbounded Knapsack

### Unbounded Knapsack

**🔗 Practice Link:** [Unbounded Knapsack](https://www.geeksforgeeks.org/unbounded-knapsack-repetition-items-allowed)

**Problem Explanation:**
Same as 0/1 knapsack (weights `wt`, values `val`, capacity `W`) with ONE difference: each item
can be chosen **any number of times** (unlimited copies). Maximize total value without exceeding
capacity `W`. Return the maximum value.

**State Definition:**
`dp[w]` = maximum value achievable with total capacity `w` using unlimited copies of the items
seen so far.

**Recurrence Relation:**
```
dp[w] = max(dp[w], val[i] + dp[w - wt[i]])       for w from wt[i] to W
```
(For each item, the best value for capacity `w` is either the previous best or the value of one
more copy of this item added to the best value for the remaining capacity `w - wt[i]`.)

**Base Cases:**
- `dp[0] = 0`: zero capacity gives zero value.
- (All other entries start at 0 — with no items chosen, value is 0.)

**Intuition (Why This Works):**
The recurrence is identical to 0/1 knapsack; only the **iteration direction changes**. In
unbounded knapsack we WANT `dp[w - wt[i]]` to potentially already include the current item,
because that's how one item gets used twice, three times, etc. So the inner loop goes
**left-to-right** (`wt[i] -> W`). In 0/1 knapsack we MUST NOT allow that, so it goes
right-to-left. This single flip of the loop direction is the entire difference between the
two problems — get it wrong and your answer is wrong by a huge margin.

**Step-by-Step Procedure:**
1. Initialize `dp = [0] * (W + 1)`.
2. For each item `i`:
   - For `w` from `wt[i]` to `W` (**left-to-right**):
     - `dp[w] = max(dp[w], val[i] + dp[w - wt[i]])`.
3. Return `dp[W]`.

**Worked Example (Dry Run):**
`wt=[2,3,4]`, `val=[3,4,5]`, `W=7`. Note: the same items solved as 0/1 give 9; as unbounded
they give 10.

```
          w:   0   1   2   3   4   5   6   7
start:        [0,  0,  0,  0,  0,  0,  0,  0]
item 1        [0,  0,  3,  3,  6,  6,  9,  9]   ← left-to-right: item 1 reused (3+3+3=9 at w=6)
item 2        [0,  0,  3,  4,  6,  7,  9, 10]   ← at w=7: 4+dp[4]=4+6=10 beats the old 9
item 3        [0,  0,  3,  4,  6,  7,  9, 10]   ← 5+dp[3]=5+4=9, no improvement
```

Reading the final row: `dp[7] = 10` comes from `val[2]=4 + dp[7-3]=dp[4]=6` → one copy of item 2
plus two copies of item 1 (`{2,2,3}` = value 3+3+4 = 10). Item 3 (`wt=4, val=5`) never helps
here. Answer: **10**.

The same items under 0/1 rules: each once → best is `{3,4}` = 9. The forward loop is exactly
what produces the extra copy of item 1.

Single-item contrast (`wt=[2]`, `val=[3]`, `W=6`):

```
Forward (unbounded, correct): dp = [0,0,3,3,6,6,9] → 9  (three copies of the item)
Backward (0/1, wrong here):   dp = [0,0,3,3,3,3,3] → 3  (only one copy allowed)
```

**Code:**

```python
def unbounded_knapsack_optimized(W: int, wt: list, val: list) -> int:
    # dp[w] = best value with capacity w using unlimited copies of items seen so far
    dp = [0] * (W + 1)
    for i in range(len(wt)):
        # LEFT-TO-RIGHT: dp[w - wt[i]] may already include item i from this same round,
        # which is exactly how an item gets used more than once (unbounded reuse).
        for w in range(wt[i], W + 1):
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]])
    return dp[W]

# If you swap this loop to right-to-left you get 0/1 knapsack behavior instead —
# one copy per item. The ONLY difference between the two algorithms is the loop direction.

# Time: O(n x W), Space: O(W)
```

**Complexity:**
- Time: O(n x W).
- Space: O(W).

**Common Mistakes & Edge Cases:**
- **Using the 0/1 loop direction here (right-to-left):** you silently forbid reuse and produce
  the 0/1 answer. The whole point of unbounded is reuse — go left-to-right.
- **Zero-weight items** (`wt[i] = 0`): `range(0, W+1)` loops forever adding value; guard
  against infinite loops (reject/limit zero-weight items or skip them).
- **Item heavier than W:** the loop `range(wt[i], W+1)` is empty, item never used — correct.
- **Very large counts:** unbounded solutions can use many copies; return the value only, not
  the set, unless the problem asks for it.
- **Empty input** `wt=[]`: returns 0 — correct.

---

## Coin Change (Minimum Coins)

### Coin Change (Minimum Coins)

**🔗 Practice Link:** [Coin Change](https://leetcode.com/problems/coin-change/)

**Problem Explanation:**
You have an unlimited supply of coins of denominations `coins` (each usable any number of
times). Given an `amount`, find the **minimum number of coins** needed to make exactly that
amount. If the amount cannot be made at all, return `-1`. (Classic example: make 11 using
denominations {1, 2, 5} → answer 3.)

**State Definition:**
`dp[a]` = minimum number of coins needed to make exactly amount `a` (using the coin
denominations seen so far, unlimited supply).

**Recurrence Relation:**
```
dp[a] = min(dp[a], dp[a - coin] + 1)         for a from coin to amount
```
(Using one coin of value `coin` reduces the problem to making `a - coin`, so the cost is
`1 + dp[a - coin]`; take the minimum over all coins.)

**Base Cases:**
- `dp[0] = 0`: making amount 0 needs 0 coins.
- All other entries start at `infinity` (a very large number meaning "not yet reachable").

**Intuition (Why This Works):**
This is **Unbounded Knapsack in disguise**: coins are items, `amount` is the capacity, and the
"value" we minimize is the count of coins instead of maximizing value. Since coins are
unlimited, the amount loop goes **left-to-right** so the same coin can be reused. Infinity
marks unreachable amounts; if `dp[amount]` is still infinity at the end, return `-1`.

**Step-by-Step Procedure:**
1. Initialize `dp = [inf] * (amount + 1)`; set `dp[0] = 0`.
2. For each `coin`:
   - For `a` from `coin` to `amount` (**left-to-right**, unbounded):
     - `dp[a] = min(dp[a], dp[a - coin] + 1)`.
3. Return `dp[amount]` if it is not `inf`, else `-1`.

**Worked Example (Dry Run):**
`coins = [1, 2, 5]`, `amount = 11`.

```
       a:    0   1   2   3   4   5   6   7   8   9   10  11
start:     [0,  ∞,  ∞,  ∞,  ∞,  ∞,  ∞,  ∞,  ∞,  ∞,  ∞,  ∞]
coin=1:    [0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11]   ← all 1s
coin=2:    [0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6]   ← use 2s where beneficial
coin=5:    [0,  1,  1,  2,  2,  1,  2,  2,  3,  3,  2,  3]   ← 5s improve 5..11
                                                              ↑     ↑
                                                    10=5+5=2  11=5+5+1=3

Answer: 3  (5 + 5 + 1)
```

**Code:**

```python
def coin_change_tab(coins: list, amount: int) -> int:
    # dp[a] = minimum coins to make exactly amount a
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0                           # base: 0 coins needed for amount 0

    for coin in coins:
        # Left-to-right = unbounded: the same coin may be reused many times.
        for a in range(coin, amount + 1):
            # Using one 'coin' leaves amount (a - coin); cost is 1 + that best cost.
            dp[a] = min(dp[a], dp[a - coin] + 1)

    # If dp[amount] never became finite, the amount is impossible to make.
    return dp[amount] if dp[amount] != float('inf') else -1

# Time: O(n x amount), Space: O(amount)
```

**Complexity:**
- Time: O(n x amount), where `n = len(coins)`.
- Space: O(amount).

**Common Mistakes & Edge Cases:**
- **Loop direction.** Going right-to-left turns this into a 0/1 problem where each coin can be
  used once — wrong. Unbounded → left-to-right.
- **`amount = 0`:** return 0 (base case), not `-1`.
- **Impossible amount:** e.g. `coins=[2]`, `amount=3` → `-1`; make sure you test for `inf`.
- **Large `inf` overflow risk:** using a huge integer like `10**9` instead of `float('inf')`
  can overflow in some languages; with Python `inf` is safe.
- **Duplicate coin denominations:** harmless (a duplicate just runs an identical update), but
  you can dedupe to save time.

---

## Coin Change II (Number of Ways)

### Coin Change II (Number of Ways)

**🔗 Practice Link:** [Coin Change II](https://leetcode.com/problems/coin-change-ii/)

**Problem Explanation:**
Given unlimited coins of denominations `coins` and a target `amount`, count the number of
**different combinations** of coins that sum to `amount`. A combination cares only about *how
many* of each coin are used, not the order: `{1, 2, 2}`, `{2, 1, 2}` and `{2, 2, 1}` are the
SAME combination and count once. Return the count.

**State Definition:**
`dp[a]` = number of combinations of coins (using the denominations seen so far) that sum to
exactly `a`.

**Recurrence Relation:**
```
dp[a] = dp[a]  +  dp[a - coin]            for a from coin to amount
```
(Every existing combination summing to `a - coin` becomes a combination summing to `a` when a
`coin` is appended; order-insensitivity comes from iterating coins in the OUTER loop.)

**Base Cases:**
- `dp[0] = 1`: exactly one way to make amount 0 — use no coins.

**Intuition (Why This Works):**
Same unbounded structure as Coin Change I, but with `+=` (counting) instead of `min`
(optimizing). The crucial detail for "combinations not permutations" is the **loop order**: the
coin loop must be the OUTER loop and the amount loop the INNER loop. Processing one coin
denomination fully before the next means each combination is built by using coins in the fixed
denomination order, so `{1,2,2}` is only ever counted once (as "two 2s after one 1"). If you
swap the loops (amount outside, coins inside), you count permutations instead. Loop direction
is still left-to-right because coins are unlimited.

**Step-by-Step Procedure:**
1. Initialize `dp = [0] * (amount + 1)`; set `dp[0] = 1`.
2. For each `coin` (outer loop — this guarantees combinations, not permutations):
   - For `a` from `coin` to `amount` (left-to-right, unbounded):
     - `dp[a] += dp[a - coin]`.
3. Return `dp[amount]`.

**Worked Example (Dry Run):**
`coins = [1, 2, 5]`, `amount = 5`.

```
       a:   0   1   2   3   4   5
start:    [1,  0,  0,  0,  0,  0]        ← base: one way to make 0
coin=1:   [1,  1,  1,  1,  1,  1]        ← {1,1,1,1,1} is the only combination so far
coin=2:   [1,  1,  2,  2,  3,  3]        ← +{2,2,1}, {2,1,1,1}, {2,2} (for 4)
coin=5:   [1,  1,  2,  2,  3,  4]        ← +{5}
                                          ↑
Answer: 4 ways:  {5}, {2,2,1}, {2,1,1,1}, {1,1,1,1,1}
Note: {1,2,2} = {2,1,2} = {2,2,1} — same combination, counted once because
denominations are processed in order (1s first, then 2s).
```

**Code:**

```python
def change_tab(coins: list, amount: int) -> int:
    # dp[a] = number of ways to make exactly amount a
    dp = [0] * (amount + 1)
    dp[0] = 1                       # one way to make amount 0: use no coins

    for coin in coins:              # coins FIRST -> counts combinations (order ignored)
        for a in range(coin, amount + 1):   # left-to-right: coin may be reused
            dp[a] += dp[a - coin]   # each way to make (a-coin) becomes one more way to make a
    return dp[amount]

# WARNING: If you swap the loops (amount first, then coins), you count PERMUTATIONS
# instead of combinations. Example above would count {1,2,2}, {2,1,2}, {2,2,1} as 3.
# Be careful about which one the problem asks for.

# Time: O(n x amount), Space: O(amount)
```

**Complexity:**
- Time: O(n x amount).
- Space: O(amount).

**Common Mistakes & Edge Cases:**
- **Swapped loops → permutations.** Amount outer + coins inner overcounts orderings. Always
  ask: "combinations" → coins outer; "permutations" (rare, e.g. LeetCode "Combination Sum IV")
  → amount outer.
- **Wrong loop direction** would forbid reusing a coin.
- **`amount = 0`:** return 1 (the "use no coins" combination), not 0.
- **Impossible amount:** e.g. `coins=[2]`, `amount=3` → 0.
- **Duplicate coin denominations** double-count combinations — dedupe the input if duplicates
  are possible.

---

## Rod Cutting

### Rod Cutting

**🔗 Practice Link:** [Rod Cutting](https://www.geeksforgeeks.org/cutting-a-rod-dp-13)

**Problem Explanation:**
You have a rod of length `n` and a price list `price[i]` = the price of a rod piece of length
`i+1`. You may cut the rod into any number of pieces (each piece's length must be an integer
from 1 to `n`), then sell the pieces at the per-length prices. Unlimited pieces of the same
length are allowed. Return the maximum revenue obtainable.

**State Definition:**
`dp[i]` = maximum revenue obtainable from a rod of length `i`.

**Recurrence Relation:**
```
dp[i] = max over j in 1..i of ( price[j-1] + dp[i-j] )
```
(For the first cut of length `j`, you earn `price[j-1]` and then solve optimally for the
remaining rod of length `i-j`; the first cut is the "choice" at each step.)

**Base Cases:**
- `dp[0] = 0`: a rod of length 0 earns nothing.
- `max_val` starts at `-inf` so at least one option is chosen.

**Intuition (Why This Works):**
Rod cutting is **Unbounded Knapsack** with a twist: pieces are the "items" and their weight
equals their length (1..n), but every length's price is always available, so the item loop is
replaced by trying every possible first-cut length `j` at each rod length `i`. The reuse
("unlimited pieces") shows up because `dp[i-j]` itself may already contain pieces of length `j`.
Rod cutting is the classic first-cut DP problem — the "choice" is which length to cut first.

**Step-by-Step Procedure:**
1. Initialize `dp = [0] * (n + 1)`; `dp[0] = 0`.
2. For `i` from `1` to `n` (rod lengths in increasing order):
   - Set `max_val = -inf`.
   - For `j` from `1` to `i` (possible length of the first piece):
     - `max_val = max(max_val, price[j-1] + dp[i-j])`.
   - `dp[i] = max_val`.
3. Return `dp[n]`.
4. (Memoized equivalent) `cut(n)` returns `0` if `n <= 0`, else the max over first-cut lengths
   of `price[j-1] + cut(n-j)`, cached per `n`.

**Worked Example (Dry Run):**
`price = [1, 5, 8, 9, 10, 17, 17, 20]`, `n = 8` (length 1 sells for 1, length 2 for 5, ...).

```
dp[i] built bottom-up (best revenue for rod length i):
  dp[0] = 0
  dp[1] = 1                                (one piece of length 1)
  dp[2] = max(1+dp[1], 5+dp[0]) = max(2, 5)   = 5
  dp[3] = max(1+dp[2], 5+dp[1], 8+dp[0])  = max(6, 6, 8) = 8
  dp[4] = max(1+3, 5+2, 8+1, 9+0)         = max(9, 10, 9, 9) = 10
  dp[5] = max(1+4, 5+3, 8+2, 9+1, 10+0)   = max(11, 13, 13, 10, 10) = 13
  dp[6] = max(1+5, 5+4, 8+3, 9+2, 10+1, 17+0) = max(14, 15, 16, 14, 11, 17) = 17
  dp[7] = max(1+6, 5+5, 8+4, 9+3, 10+2, 17+1, 17+0) = max(18, 18, 18, 17, 15, 18, 17) = 18
  dp[8] = max(1+7, 5+6, 8+5, 9+4, 10+3, 17+2, 17+1, 20+0)
        = max(19, 22, 21, 19, 18, 22, 18, 20) = 22

Answer: 22  (cut into lengths 2 + 6: 5 + 17 = 22)
```

**Code:**

```python
def rod_cutting_memo(price: list, n: int = None, memo: dict = None) -> int:
    # Recursive with memoization: revenue(i) = best money from rod of length i
    if memo is None:
        memo = {}
    if n is None:
        n = len(price)                  # default rod length = number of price entries
    if n <= 0:
        return 0                        # base: nothing left to sell
    if n in memo:
        return memo[n]                  # subproblem already solved
    max_val = float('-inf')
    for i in range(1, n + 1):           # try every possible first piece length i
        if i <= len(price):
            # sell first piece of length i, recurse on the remaining length (n - i)
            max_val = max(max_val, price[i - 1] + rod_cutting_memo(price, n - i, memo))
    memo[n] = max_val
    return memo[n]


def rod_cutting_tab(price: list, n: int = None) -> int:
    # 2D-ish bottom-up: dp[i] = best revenue for rod of length i
    if n is None:
        n = len(price)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):           # build up answers for every rod length 1..n
        max_val = float('-inf')
        for j in range(1, i + 1):       # j = length of the first piece
            if j <= len(price):
                # revenue = price of first piece + best revenue of the leftover (i - j)
                max_val = max(max_val, price[j - 1] + dp[i - j])
        dp[i] = max_val
    return dp[n]


def rod_cutting_optimized(price: list) -> int:
    # Clean 1D version using dp[i-j] which is always already computed (smaller index)
    n = len(price)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        for j in range(1, i + 1):       # every possible length for the first cut
            dp[i] = max(dp[i], price[j - 1] + dp[i - j])
    return dp[n]

# Example: price = [1, 5, 8, 9, 10, 17, 17, 20]
# n = 8: Answer = 22  (cuts 2 + 6 → price 5 + 17)

# Time: O(n²), Space: O(n)
```

**Complexity:**
- Time: O(n²) for all versions (each of `n` lengths tries up to `n` cut positions).
- Space: O(n) for the DP table/memo cache.

**Common Mistakes & Edge Cases:**
- **`n = 0`:** return 0, don't index `price[-1]` or run loops.
- **First-cut loop bound:** the first piece can be at most length `i` (you can't cut a piece
  longer than the rod). `range(1, i+1)` is required; `range(1, n+1)` would also "work" in the
  memo version only because of the `i <= len(price)` guard.
- **Infinite recursion:** always decrement `n` before recursing (`n - i` with `i >= 1`).
- **Piece longer than available rod:** guard with `if j <= len(price)` or ensure the loop only
  goes to `min(i, len(price))`.
- **Unlimited pieces:** unlike 0/1 problems there is no "each piece once" constraint — the
  same length can be used many times, which the left-to-right / bottom-up build already allows.

---

## Summary Table & Quick Reference

```
┌──────────────────────────┬──────────────────┬──────────┬──────────┬───────────────────────────────────┐
│ Problem                  │ Type             │ Time     │ Space    │ Key Insight                       │
├──────────────────────────┼──────────────────┼──────────┼──────────┼───────────────────────────────────┤
│ 0/1 Knapsack             │ 1 item limit     │ O(n×W)   │ O(W)     │ Loop R→L (prevent double use)    │
│ Subset Sum               │ Decision         │ O(n×tgt) │ O(tgt)   │ Boolean knapsack variant          │
│ Equal Partition          │ Decision         │ O(n×tgt) │ O(tgt)   │ target = total/2                  │
│ Count Subsets            │ Count            │ O(n×tgt) │ O(tgt)   │ dp[s] += dp[s-num]               │
│ Min Subset Diff          │ Optimization     │ O(n×tgt) │ O(tgt)   │ Closest subset sum to total/2     │
│ Unbounded Knapsack       │ Unlimited items  │ O(n×W)   │ O(W)     │ Loop L→R (allows reuse)           │
│ Coin Change (min coins)  │ Minimization     │ O(n×amt) │ O(amt)   │ Unbounded + min                   │
│ Coin Change II (ways)    │ Count combos     │ O(n×amt) │ O(amt)   │ Unbounded + count                 │
│ Rod Cutting              │ Unbounded variant│ O(n²)    │ O(n)     │ Try all cut positions             │
└──────────────────────────┴──────────────────┴──────────┴──────────┴───────────────────────────────────┘
```

### The Golden Rule of Loop Direction

```
╔══════════════════════════════════════════════════════════════════╗
║  0/1 Knapsack (each item once):                                  ║
║     for w in range(W, weight-1, -1):   ← RIGHT TO LEFT          ║
║     Ensures dp[w-wt] is from previous item's row                ║
║                                                                  ║
║  Unbounded Knapsack (each item unlimited):                       ║
║     for w in range(weight, W+1):        ← LEFT TO RIGHT         ║
║     Allows dp[w-wt] to include current item again               ║
║                                                                  ║
║  If you only remember one thing from this file, remember this:  ║
║  "each item once" → RIGHT-TO-LEFT,  "unlimited copies" → LEFT-TO-RIGHT. ║
╚══════════════════════════════════════════════════════════════════╝
```
