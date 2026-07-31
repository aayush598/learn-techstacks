# Knapsack Advanced Variants

This file builds on `01_knapsack_guide.md`. It covers harder problems that twist the basic
knapsack idea: limited item counts, multiple knapsacks, sign assignments, stone smashing,
two-resource knapsacks, and palindrome cutting. Read file 01 first if the loop-direction rule
(0/1 = right-to-left, unbounded = left-to-right) is not yet second nature.

## When to Use Advanced Knapsack

Use this table to recognize which advanced pattern a new problem is really asking for:

```
┌──────────────────────────────────────────────────────────────────────┐
│              ADVANCED KNAPSACK PATTERN GUIDE                         │
├─────────────────────────────┬────────────────────────────────────────┤
│ Problem hints               │ Pattern                              │
├─────────────────────────────┼────────────────────────────────────────┤
│ "limited count of each"     │ Bounded Knapsack (binary splitting)  │
│ "two bags / knapsacks"      │ 2D capacity knapsack                 │
│ "cut string into palindromes"│ Interval DP on precomputed palindromes│
│ "print the actual subsets"  │ Backtrack through filled DP table     │
│ "assign +/- to reach target"│ Transform to subset sum              │
│ "smash stones together"     │ Min subset sum difference             │
│ "two constraints (0s, 1s)"  │ 2D capacity knapsack                 │
└─────────────────────────────┴────────────────────────────────────────┘
```

---

## Bounded Knapsack

### Bounded Knapsack (Binary Splitting)

**Problem Explanation:**
Like 0/1 knapsack (weights `wt`, values `val`, capacity `W`) but each item `i` has a **limited
quantity** `count[i]`: you may take between 0 and `count[i]` copies of it. Maximize total value
within capacity `W`. Return the maximum value.

**State Definition:**
`dp[cap]` = maximum value achievable with capacity `cap` using the virtual (split) items
processed so far. A "virtual item" is a pre-packaged bundle of `take` copies of one original item,
with total weight `take * wt[i]` and total value `take * val[i]`.

**Recurrence Relation:**
```
dp[cap] = max(dp[cap], dp[cap - take*wt[i]] + take*val[i])   for cap from W down to take*wt[i]
```
(Each virtual bundle is used like a single 0/1 item: either take the whole bundle of `take`
copies or skip it.)

**Base Cases:**
- `dp[cap] = 0` for all `cap`: with nothing chosen, value is 0.

**Intuition (Why This Works):**
Naively expanding every item into `count[i]` separate copies gives `sum(count)` items — too
many when counts are large. Binary splitting fixes this: any quantity `count` can be written as
`1 + 2 + 4 + ... + remainder` using O(log count) parts, and any number of copies from 0 to
`count` can be assembled from those parts (binary representation). Each part becomes one
virtual 0/1 item, so the whole problem collapses to a normal 0/1 knapsack with
`O(n * log(count))` items. Because each virtual item may be used at most once, the capacity
loop runs **right-to-left** (0/1 rule).

**Step-by-Step Procedure:**
1. Initialize `dp = [0] * (W + 1)`.
2. For each original item `i` with `(wt[i], val[i], count[i])`:
   - Let `k = 1`. While `count[i]` still has copies left:
     - `take = min(k, count[i])` — pack this many copies into one virtual item.
     - Virtual item has `weight = take * wt[i]`, `value = take * val[i]`.
     - Update 0/1 style: for `cap` from `W` down to `weight`:
       `dp[cap] = max(dp[cap], dp[cap - weight] + value)`.
     - Subtract `take` from `count[i]`; double `k` (1, 2, 4, 8, ...).
3. Return `dp[W]`.

**Worked Example (Dry Run):**
One item with `wt=2, val=3, count=5`, `W=10`. Splitting: `5 = 1 + 2 + 2`, so the virtual items
are `(wt=2,val=3)`, `(wt=4,val=6)`, `(wt=4,val=6)`.

```
dp after each virtual item (0/1 update, right-to-left):
  start:        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  group 1×2:    [0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3]    can take at most 1 copy
  group 2×2:    [0, 0, 3, 3, 6, 6, 9, 9, 9, 9, 9]    now 2 or 3 copies possible
  group 2×2:    [0, 0, 3, 3, 6, 6, 9, 9, 12, 12, 15] now up to 5 copies possible

Answer: 15  (= 5 copies × 3, exactly filling capacity 10)
The virtual groups allow choosing 1, 2, 3, 4, or 5 copies:
  5 = group1(1) + group2(2) + group3(2).
```

**Code:**

```python
def bounded_knapsack_direct(W: int, wt: list, val: list, count: list) -> int:
    """count[i] = max available pieces of item i."""
    # dp[cap] = max value with capacity cap from the virtual items seen so far
    dp = [0] * (W + 1)
    for i in range(len(wt)):
        c = count[i]                     # copies still to be packed
        w = wt[i]                        # weight of one copy
        v = val[i]                       # value of one copy
        # Binary splitting: break count into powers of 2 (1, 2, 4, ...) + remainder.
        k = 1
        while c > 0:
            take = min(k, c)             # number of copies in this virtual group
            weight = take * w            # total weight of the group
            value = take * v             # total value of the group
            # 0/1 knapsack update (right-to-left), since each group is used once.
            # This also skips groups heavier than W automatically.
            for cap in range(W, weight - 1, -1):
                dp[cap] = max(dp[cap], dp[cap - weight] + value)
            c -= take                    # consume the packed copies
            k <<= 1                      # double the group size: 1, 2, 4, 8, ...
    return dp[W]

# Time: O(W x sum(log2 count[i])), Space: O(W)
```

**Complexity:**
- Time: O(W x Σ log(count[i])), where log is base 2 (each item creates ~log2(count)+1 groups).
- Space: O(W).

**Common Mistakes & Edge Cases:**
- **Forgetting the remainder.** `count = 13` splits as `1 + 2 + 4 + 6`, not `1 + 2 + 4 + 8`
  (that would sum to 15, more copies than you own). `take = min(k, c)` handles it.
- **Using left-to-right updates:** the virtual groups would be reusable, letting you exceed
  `count[i]`. Bounded knapsack reduces to 0/1 → right-to-left.
- **`count[i] = 0`:** the `while c > 0` loop never runs — item contributes nothing, correct.
- **Group heavier than W:** `range(W, weight-1, -1)` is empty, so the group is ignored.
- **Large counts:** log-splitting keeps the item count small; without it the naive expansion
  can blow up memory/time.

---

## Multiple Knapsacks (Two Knapsacks)

### Multiple Knapsacks (Two Knapsacks)

**Problem Explanation:**
You have **two** knapsacks with capacities `W1` and `W2`. Each item (weight `wt[i]`, value
`val[i]`) may go into the first bag, into the second bag, or into neither — never both, and
never split across them. Maximize the total value carried by both bags. Return the maximum value.

**State Definition:**
`dp[c1][c2]` = maximum total value achievable with the items processed so far, using exactly
`c1` capacity in bag 1 and `c2` capacity in bag 2.

**Recurrence Relation:**
```
dp[c1][c2] = max( dp[c1][c2],                          # skip item i
                  dp[c1 - w][c2] + v,   if c1 >= w     # put item i in bag 1
                  dp[c1][c2 - w] + v,   if c2 >= w )   # put item i in bag 2
```
(For each item there are three choices; the max over them is the best value for state
`(c1, c2)`.)

**Base Cases:**
- `dp[0][0] = 0` and every other entry starts at 0 (choosing no items yields value 0).

**Intuition (Why This Works):**
Adding a second bag just adds a second capacity dimension to the state — a "2D capacity"
knapsack. Each item is a 0/1 item (used at most once), so BOTH capacity loops must iterate
**right-to-left**. Iterating both backward guarantees that `dp[c1-w][c2]` and `dp[c1][c2-w]`
still hold values from the *previous* item, so the same item can never be placed in both bags
or placed twice in one bag.

**Step-by-Step Procedure:**
1. Create `dp` of size `(W1+1) x (W2+1)` filled with 0.
2. For each item `i` with weight `w` and value `v`:
   - For `c1` from `W1` down to 0:
     - For `c2` from `W2` down to 0:
       - If `c1 >= w`: consider putting the item in bag 1 (`dp[c1-w][c2] + v`).
       - If `c2 >= w`: consider putting the item in bag 2 (`dp[c1][c2-w] + v`).
3. Return `dp[W1][W2]`.

**Worked Example (Dry Run):**
`wt=[1,2]`, `val=[3,4]`, `W1=3`, `W2=3`. Grid rows = `c1` (bag 1), columns = `c2` (bag 2).

```
After item 1 (wt=1, val=3) — any state with c1>=1 or c2>=1 can hold it:
  c2:     0    1    2    3
  c1=0: [ 0,   3,   3,   3 ]
  c1=1: [ 3,   3,   3,   3 ]
  c1=2: [ 3,   3,   3,   3 ]
  c1=3: [ 3,   3,   3,   3 ]

After item 2 (wt=2, val=4) — best of skip / bag1 / bag2:
  c2:     0    1    2    3
  c1=0: [ 0,   3,   4,   7 ]   ← (0,3): bag2 = item2(4)+item1(3)
  c1=1: [ 3,   3,   7,   7 ]   ← (1,2): item2 in bag2 + item1 in bag1 = 4+3
  c1=2: [ 4,   7,   7,   7 ]   ← (2,0): bag1 = item2
  c1=3: [ 7,   7,   7,   7 ]

Answer: dp[3][3] = 7  (e.g. item 1 in bag 1, item 2 in bag 2: 3 + 4 = 7)
```

**Code:**

```python
def two_knapsack(W1: int, W2: int, wt: list, val: list) -> int:
    # dp[c1][c2] = max value using c1 capacity of bag 1 and c2 capacity of bag 2
    dp = [[0] * (W2 + 1) for _ in range(W1 + 1)]
    for i in range(len(wt)):
        w, v = wt[i], val[i]
        # Process BOTH bags for each item; both dimensions must go backward so
        # the current item is never reused (0/1 rule applied twice).
        for c1 in range(W1, -1, -1):      # Bag 1 capacity (backward)
            for c2 in range(W2, -1, -1):  # Bag 2 capacity (backward)
                if c1 >= w:               # option: item goes into bag 1
                    dp[c1][c2] = max(dp[c1][c2], dp[c1 - w][c2] + v)
                if c2 >= w:               # option: item goes into bag 2
                    dp[c1][c2] = max(dp[c1][c2], dp[c1][c2 - w] + v)
                # (skipping the item is the implicit third option: keep dp as-is)
    return dp[W1][W2]

# Time: O(n x W1 x W2), Space: O(W1 x W2)
```

**Complexity:**
- Time: O(n x W1 x W2).
- Space: O(W1 x W2).

**Common Mistakes & Edge Cases:**
- **Iterating either capacity forward** lets an item be used twice in that bag (0/1 violation).
- **An item heavier than both bags:** both `if` guards fail → item is skipped, correct.
- **An item exactly fitting the leftover space of both bags:** it still goes into only ONE bag
  because the two transitions use different cells and can't combine in one item pass.
- **One bag empty (`W2=0`):** degenerates to ordinary 0/1 knapsack with the other bag.
- **Very large `W1 x W2` grid:** O(W1 x W2) memory can explode; a sparse/hash-map DP or
  dimension reduction may be needed.

---

## Target Sum

### Target Sum

**Problem Explanation:**
Given an array of non-negative integers `nums` and an integer `target`, assign each number a
`+` or `-` sign so that the signed sum equals `target`. Count how many different sign
assignments work. Each number is used exactly once (with either sign). Return the count.

**State Definition:**
`dp[s]` = number of subsets (of the numbers seen so far) that sum to exactly `s`, where
`s` ranges `0..new_target` and `new_target = (total + target) // 2`.

**Recurrence Relation:**
```
dp[s] = dp[s] + dp[s - num]        for s from new_target down to num
```
(Every subset summing to `s - num` becomes a subset summing to `s` by adding `num` — this is
exactly the "count subsets with given sum" recurrence.)

**Base Cases:**
- `dp[0] = 1`: the empty subset sums to 0.
- Early exits: if `(total + target)` is odd, or `abs(target) > total`, return 0 (no assignment
  can reach that target).

**Intuition (Why This Works):**
This is a pure algebra trick that converts "+/-" assignments into a subset-sum count. Let
`P` = the sum of numbers assigned `+`, `N` = the sum assigned `-`. Then
`P - N = target` and `P + N = total`. Adding gives `2P = total + target`, so
`P = (total + target)/2`. Counting sign assignments that hit `target` is identical to counting
subsets whose sum is `P`. The formula is valid only when `total + target` is even and
`target` is within `[-total, total]`. Because each number is used once, the loop runs
**right-to-left** (0/1).

**Step-by-Step Procedure:**
1. Compute `total = sum(nums)`.
2. If `(total + target) % 2 != 0` or `abs(target) > total`, return 0.
3. Set `new_target = (total + target) // 2`.
4. Initialize `dp = [0] * (new_target + 1)`; set `dp[0] = 1`.
5. For each `num`, for `s` from `new_target` **down to** `num`: `dp[s] += dp[s - num]`.
6. Return `dp[new_target]`.

**Worked Example (Dry Run):**
`nums = [1, 1, 1, 1, 1]`, `target = 3`. `total = 5`, `new_target = (5+3)/2 = 4` — so we count
subsets of five 1s summing to 4: any 4 of the 5 ones, i.e. `C(5,4) = 5`.

```
dp (size 5)   s: 0    1    2    3    4
start:           [1,   0,   0,   0,   0]
after 1st 1:     [1,   1,   0,   0,   0]
after 2nd 1:     [1,   2,   1,   0,   0]
after 3rd 1:     [1,   3,   3,   1,   0]
after 4th 1:     [1,   4,   6,   4,   1]
after 5th 1:     [1,   5,  10,  10,   5]
                                      ↑
Answer: 5  (choose which of the 5 ones gets the + sign; the rest get -:
            e.g. +1+1+1-1-1 = 3)
```

**Code:**

```python
def find_target_sum_tab(nums: list, target: int) -> int:
    total = sum(nums)
    # Algebra: with P = sum of + numbers, 2P = total + target.
    # If P is not an integer or out of range, no assignment can hit the target.
    if (total + target) % 2 != 0 or abs(target) > total:
        return 0
    new_target = (total + target) // 2   # count subsets summing to this value instead
    dp = [0] * (new_target + 1)
    dp[0] = 1                           # one empty subset sums to 0
    for num in nums:
        # 0/1 style (right-to-left): each number used at most once
        for s in range(new_target, num - 1, -1):
            dp[s] += dp[s - num]        # each subset summing to s-num yields one for s
    return dp[new_target]

# Example: nums = [1, 1, 1, 1, 1], target = 3
# total = 5, new_target = (5 + 3) / 2 = 4
# Count subsets summing to 4: pick 4 of the 5 ones -> C(5,4) = 5 ways
# Answer: 5

# Time: O(n x new_target), Space: O(new_target)
```

**Complexity:**
- Time: O(n x new_target), where `new_target = (total + target) / 2`.
- Space: O(new_target).

**Common Mistakes & Edge Cases:**
- **Parity check:** `total + target` odd → return 0 (e.g. `nums=[1,2,3]`, `target=1` gives
  7/2 = 3.5, impossible).
- **`abs(target) > total`:** even the all-`+` assignment can't reach it → return 0.
- **Negative `target`:** the formula handles it symmetrically (assigning `-` to the right
  subset), no extra code needed.
- **Wrong loop direction** reuses numbers and overcounts.
- **Zeros in `nums`:** each 0 can be `+` or `-` with no effect; the DP automatically doubles
  those ways when the inner loop reaches `s=0`, but the memoized base-case caveat from the
  count-subsets problem applies if you use recursion.

---

## Last Stone Weight II

### Last Stone Weight II

**Problem Explanation:**
You have stones with weights `stones`. Repeatedly pick any two stones and smash them together:
the heavier stone loses the lighter one's weight and survives (i.e., a stone of weight `a`
smashing one of weight `b` leaves a stone of weight `|a - b|`; if equal, both vanish). You
smash until at most one stone remains. Return the **smallest possible weight** of the final
stone (0 if all can be destroyed).

**State Definition:**
`dp[s]` = `True` if some subset of the stones seen so far sums to exactly `s`, for
`s` ranging `0..target` with `target = total // 2`.

**Recurrence Relation:**
```
dp[s] = dp[s]  or  dp[s - stone]        for s from target down to stone
```
(The subset-sum reachability recurrence: a sum `s` becomes reachable by extending reachable
`(s - stone)` with one stone.)

**Base Cases:**
- `dp[0] = True`: the empty subset sums to 0.

**Intuition (Why This Works):**
Smashing is secretly partitioning. Any sequence of smashes on two groups with sums `S` and
`total - S` can only ever leave a stone of weight `|S - (total - S)| = |total - 2S|`, because
every smash between the two groups subtracts and equal weights cancel. So the problem reduces to
**minimum subset-sum difference**: find a subset sum `S` as close to `total/2` as possible and
return `total - 2S`. Each stone is used once → the sum loop iterates **right-to-left**.

**Step-by-Step Procedure:**
1. Compute `total = sum(stones)` and `target = total // 2`.
2. Initialize `dp = [False] * (target + 1)`; set `dp[0] = True`.
3. For each `stone`, for `s` from `target` down to `stone`:
   `dp[s] = dp[s] or dp[s - stone]`.
4. Scan `s` from `target` down to 0; the first `True` gives the closest reachable `S`.
5. Return `total - 2 * s`.

**Worked Example (Dry Run):**
`stones = [2, 7, 4, 1, 8, 1]`: `total = 23`, `target = 11`.

```
reachable sums within 0..11 after each stone:
  start:    0
  after 2:  0 2
  after 7:  0 2 7 9
  after 4:  0 2 4 6 7 9 11          ← {2,4,7}=13? no—{4,7}=11 ✓
  after 1:  0 1 2 3 4 5 6 7 8 9 10 11
  after 8:  0 1 2 3 4 5 6 7 8 9 10 11 (everything up to 11 now reachable)
  after 1:  unchanged within 0..11

Scanning from 11 down: S = 11 is reachable ({4,7} = 11).
Answer: total - 2*S = 23 - 22 = 1.
  (Group A = {4,7} sums to 11, group B = {2,1,8,1} sums to 12 → one smash leaves |11-12| = 1.)
```

**Code:**

```python
def last_stone_weight_ii(stones: list) -> int:
    total = sum(stones)
    target = total // 2                 # we only need subset sums up to half the total
    dp = [False] * (target + 1)
    dp[0] = True                        # sum 0 reachable via the empty subset
    for stone in stones:
        # 0/1 style: right-to-left so each stone is used at most once
        for s in range(target, stone - 1, -1):
            dp[s] = dp[s] or dp[s - stone]   # mark s reachable via s-stone + stone
    # Find the closest reachable sum to total/2, scanning from largest to smallest.
    # The final stone is |S - (total - S)| = |total - 2S|, minimized when S is closest
    # to total/2.
    for s in range(target, -1, -1):
        if dp[s]:
            return total - 2 * s        # minimum possible remaining stone weight
    return total                        # unreachable in practice (s=0 always works)

# Time: O(n x target), Space: O(target)
```

**Complexity:**
- Time: O(n x target), where `target = total/2`.
- Space: O(target).

**Common Mistakes & Edge Cases:**
- **Two stones `[a, b]`:** answer is always `|a - b|` — check the DP gives the same.
- **One stone** `[5]`: `total=5`, `target=2`, reachable sums ≤2 = {0} → answer 5 (stone stays).
- **Confusing this with Last Stone Weight I:** version I smashes the two LARGEST stones each
  time (a greedy/priority-queue problem); version II (this one) allows any pairing and is a
  partition/DP problem.
- **Wrong loop direction** reuses stones and marks unreachable sums → wrong minimum.
- **Odd totals:** answer can never be 0 (total - 2S is odd), which is fine — no special casing.

---

## Ones and Zeros (Binary Knapsack)

### Ones and Zeros (2D Capacity Knapsack)

**Problem Explanation:**
You are given `strs`, a list of binary strings (only '0' and '1' characters), and two integers
`m` and `n`. A **subset** of the strings is valid if, counting all the strings together, it
contains at most `m` zeros total and at most `n` ones total. Return the maximum number of
strings in a valid subset. Each string is used at most once.

**State Definition:**
`dp[i][j]` = maximum number of strings that can be formed using at most `i` zeros and at most
`j` ones (from the strings processed so far). Note: `i` is the **zeros** budget and `j` is the
**ones** budget — `m` limits zeros, `n` limits ones.

**Recurrence Relation:**
```
dp[i][j] = max(dp[i][j], dp[i - zeros][j - ones] + 1)
            for i from m down to zeros, j from n down to ones
```
(Taking string `s` consumes `zeros` zeros and `ones` ones, so the best answer for `(i, j)` is
one more than the best answer for the remaining budgets `(i - zeros, j - ones)`.)

**Base Cases:**
- Every entry starts at 0: with no strings chosen, the count is 0.

**Intuition (Why This Works):**
Each string is an item with **two weights** (its zero count and its one count) and a value of 1
(one string). That makes it a knapsack with a 2-dimensional capacity — `dp` is a 2D table over
(zeros used, ones used). A string is used at most once, so **both** capacity dimensions iterate
**right-to-left** (the 0/1 rule applied twice, exactly like the two-knapsack problem). A string
is skipped automatically whenever the loop bounds require more zeros or ones than are available.

**Step-by-Step Procedure:**
1. Initialize `dp` as an `(m+1) x (n+1)` grid of zeros.
2. For each string `s`:
   - Count `zeros = s.count('0')` and `ones = s.count('1')`.
   - For `i` from `m` **down to** `zeros` (zeros budget, backward):
     - For `j` from `n` **down to** `ones` (ones budget, backward):
       - `dp[i][j] = max(dp[i][j], dp[i - zeros][j - ones] + 1)`.
3. Return `dp[m][n]`.

**Worked Example (Dry Run):**
`strs = ["10", "0001", "111001", "1", "0"]`, `m = 5` (max zeros), `n = 3` (max ones).
Grid rows = zeros budget `i` (0..5), columns = ones budget `j` (0..3).

```
after "10"    (z=1, o=1):  rows 1..5, cols 1..3 can take it
  [[0,0,0,0], [0,1,1,1], [0,1,1,1], [0,1,1,1], [0,1,1,1], [0,1,1,1]]
after "0001"  (z=3, o=1):  needs 3 zeros and 1 one
  [[0,0,0,0], [0,1,1,1], [0,1,1,1], [0,1,1,1], [0,1,2,2], [0,1,2,2]]
                                                ↑ dp[4][2] = dp[1][1]+1 = 1+1 = 2 ("10"+"0001")
after "111001" (z=2, o=4): 4 ones > n=3, inner loop empty → no update (string can never fit)
  (unchanged)
after "1"     (z=0, o=1):  zero-cost zeros, one one
  [[0,1,1,1], [0,1,2,2], [0,1,2,2], [0,1,2,2], [0,1,2,3], [0,1,2,3]]
after "0"     (z=1, o=0):  one zero, zero ones
  [[0,1,1,1], [1,2,2,2], [1,2,3,3], [1,2,3,3], [1,2,3,3], [1,2,3,4]]
```

Final cell `dp[5][3] = 4`: the subset `{"10", "0001", "1", "0"}` uses 1+3+0+1 = 5 zeros and
1+1+1+0 = 3 ones — exactly the budget. Answer: **4**.

**Code:**

```python
def find_max_form(strs: list, m: int, n: int) -> int:
    # dp[i][j] = max strings using at most i ZEROS and j ONES
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        zeros = s.count('0')            # weight in the zeros dimension
        ones = s.count('1')             # weight in the ones dimension
        # 0/1 style: BOTH dimensions backward so each string is used at most once.
        # The loops start at m/n and stop exactly at zeros/ones, which guarantees
        # i - zeros >= 0 and j - ones >= 0 (no negative indexing).
        for i in range(m, zeros - 1, -1):
            for j in range(n, ones - 1, -1):
                # Take s: one more string, consuming zeros and ones from the budget.
                dp[i][j] = max(dp[i][j], dp[i - zeros][j - ones] + 1)
    return dp[m][n]

# Example: strs = ["10","0001","111001","1","0"], m=5, n=3
# Answer: 4  ("10", "0001", "1", "0") — total zeros = 5, total ones = 3
# NOTE: m is the ZEROS limit and n is the ONES limit (the standard LeetCode convention).

# Time: O(k x m x n) where k = len(strs)
```

**Complexity:**
- Time: O(k x m x n), where `k = len(strs)`.
- Space: O(m x n).

**Common Mistakes & Edge Cases:**
- **Swapping `m` and `n`:** the example only works if `m` = zeros and `n` = ones. If your loop
  bounds and the `dp` array disagree about which dimension is which, you get wrong answers.
- **Swapped loop bounds:** the loops must go down to `zeros` (in the `i` loop) and `ones`
  (in the `j` loop). Mixing them up can index `dp[i - zeros][j - ones]` with a **negative
  index**, which Python silently wraps to the end of the list — a nasty silent bug.
- **Forgetting a string can never fit** (e.g. `ones > n`): the inner loop is empty and the
  string is ignored — no special case needed.
- **Empty `strs`:** returns 0, correct.
- **Zero-count strings** (`"0"` has `ones=0`): the `j` loop still runs; the string adds to
  every column it can afford in the zeros dimension.

---

## Palindrome Partitioning (Palindrome Cut)

### Palindrome Cut

**Problem Explanation:**
Given a string `s`, you may cut it into pieces such that every piece is a **palindrome** (reads
the same forward and backward; a single character is always a palindrome). Find the **minimum
number of cuts** needed. An already-palindromic string needs 0 cuts. Return the minimum cut count.

**State Definition:**
`is_pal[i][j]` = `True` if `s[i..j]` is a palindrome. `dp[i]` = minimum cuts needed for the
prefix `s[0..i]` so that every piece is a palindrome.

**Recurrence Relation:**
```
is_pal[i][j] = (s[i] == s[j])  and  (j - i <= 2  or  is_pal[i+1][j-1])
dp[i] = 0                                if is_pal[0][i]
dp[i] = min( dp[j] + 1 ) over j < i      such that is_pal[j+1][i] == True
```
(`s[i..j]` is a palindrome if its two ends match and its interior is a palindrome; the last cut
for prefix `s[0..i]` splits it into the solved prefix `s[0..j]` plus the palindromic suffix
`s[j+1..i]`.)

**Base Cases:**
- `is_pal[i][i] = True` for all `i` (single characters).
- `is_pal[i][i+1] = (s[i] == s[i+1])` (two-character palindromes).
- `dp[0] = 0` (a one-character prefix is already a palindrome).

**Intuition (Why This Works):**
The "choice" at every prefix is where to place the **last cut**. If the suffix after that cut is
a palindrome, the problem reduces to the prefix before the cut (an overlapping subproblem), so
DP applies. Checking "is this substring a palindrome" cheaply for every `(i, j)` pair requires
precomputing the `is_pal` table first (interval DP: short substrings build the truth of longer
ones), after which filling `dp` takes O(n²). Note this problem is a cousin of knapsack patterns
mainly in that the min-cut recurrence is the classic DP "try every previous breakpoint" form.

**Step-by-Step Procedure:**
1. If `len(s) <= 1`, return 0.
2. Build `is_pal` (n x n, all `False`): for each `j`, for each `i <= j`, set
   `is_pal[i][j] = (s[i] == s[j]) and (j - i <= 2 or is_pal[i+1][j-1])`.
3. Initialize `dp = [inf] * n`.
4. For `i` from 0 to `n-1`:
   - If `is_pal[0][i]`: `dp[i] = 0` (whole prefix is a palindrome, zero cuts).
   - Else for `j` from 0 to `i-1`:
     - If `is_pal[j+1][i]`: `dp[i] = min(dp[i], dp[j] + 1)`.
5. Return `dp[n-1]`.

**Worked Example (Dry Run):**
`s = "aab"`, `n = 3`.

```
is_pal table:
        j=0    j=1    j=2
  i=0   "a"T   "aa"T  "aab"F
  i=1          "a"T   "ab"F
  i=2                 "b"T

dp fill:
  i=0: is_pal[0][0] = T → dp[0] = 0
  i=1: is_pal[0][1] = T ("aa") → dp[1] = 0
  i=2: is_pal[0][2] = F, so try last-cut positions j:
         j=0: is_pal[1][2] = "ab" = F
         j=1: is_pal[2][2] = "b" = T → dp[2] = dp[1] + 1 = 0 + 1 = 1
Answer: 1  (cut "aa | b")
```

**Code:**

```python
def palindrome_cut(s: str) -> int:
    n = len(s)
    if n <= 1:
        return 0                        # empty / single char needs no cut

    # is_pal[i][j] = True if s[i..j] is a palindrome.
    # Fill by increasing j (right end): a substring is a palindrome if the two ends
    # match and the interior is a palindrome (or it is length 1 or 2).
    is_pal = [[False] * n for _ in range(n)]
    for j in range(n):
        for i in range(j + 1):
            if s[i] == s[j] and (j - i <= 2 or is_pal[i + 1][j - 1]):
                is_pal[i][j] = True

    # dp[i] = min cuts to make prefix s[0..i] all-palindromic
    dp = [float('inf')] * n
    for i in range(n):
        if is_pal[0][i]:
            dp[i] = 0                   # whole prefix is one palindrome: no cuts
            continue
        # Place the LAST cut at j: prefix s[0..j] is already solved, and the suffix
        # s[j+1..i] must itself be a palindrome. Pick the best j.
        for j in range(i):
            if is_pal[j + 1][i]:
                dp[i] = min(dp[i], dp[j] + 1)
    return dp[n - 1]

# Example: s = "aab" → 1  ("aa | b")
# Time: O(n²), Space: O(n²)
```

**Complexity:**
- Time: O(n²) (building `is_pal` and filling `dp` are each O(n²)).
- Space: O(n²) for the `is_pal` table (plus O(n) for `dp`).

**Common Mistakes & Edge Cases:**
- **Building `is_pal` in the wrong order:** `is_pal[i+1][j-1]` must already be computed when
  you read it. Iterating `j` outer, `i` inner (as above) guarantees the interior `(i+1..j-1)`
  was filled earlier because its right end is `j-1 < j`.
- **Off-by-one on the last cut:** the suffix is `s[j+1..i]`, not `s[j..i]`; using `s[j..i]`
  double-counts character `j` and gives wrong answers.
- **`s` empty or length 1:** return 0 before indexing `is_pal`.
- **All characters the same** (`"aaa"`): `is_pal[0][n-1] = True` → 0 cuts.
- **Single-char check `j - i <= 2`:** this correctly covers length-1 (`j==i`) and length-2
  (`j==i+1`) palindromes without out-of-range access to `is_pal[i+1][j-1]`.

---

## Summary Table & Quick Reference

```
┌──────────────────────────┬────────────────────────┬──────────┬──────────┬───────────────────────────────┐
│ Problem                  │ Key Insight            │ Time     │ Space    │ When to Use                   │
├──────────────────────────┼────────────────────────┼──────────┼──────────┼───────────────────────────────┤
│ Bounded Knapsack         │ Binary splitting       │ O(W logc)│ O(W)     │ Limited item counts           │
│ Multiple Knapsacks       │ 2D capacity DP         │ O(n×W1×W2)│ O(W1×W2)│ Two bags to fill             │
│ Palindrome Cut           │ Precompute palindromes │ O(n²)    │ O(n²)    │ Min cuts in string            │
│ Equal Subset (print)     │ Backtrack DP table     │ O(n×tgt) │ O(n×tgt) │ Need actual partition         │
│ Target Sum               │ Transform to subset    │ O(n×tgt) │ O(tgt)   │ +/- assignment problems       │
│ Last Stone II            │ Min subset diff same   │ O(n×tgt) │ O(tgt)   │ Stone smashing = partition    │
│ Ones and Zeros           │ 2-cost knapsack        │ O(k×m×n) │ O(m×n)   │ Two resource constraints      │
└──────────────────────────┴────────────────────────┴──────────┴──────────┴───────────────────────────────┘
```

### Transformation Patterns

```
Many problems REDUCE to Subset Sum:

  Target Sum (assign +/-)    → subset sum with sum = (total+target)/2
  Last Stone Weight II       → min subset sum difference
  Equal Partition            → subset sum with sum = total/2
  Min Subset Diff            → closest subset sum to total/2
  Partition with min diff    → subset sum variants

Key formula:
  sum(positive_group) = (total + target) / 2
  If this is integer and achievable → problem solved!
```
