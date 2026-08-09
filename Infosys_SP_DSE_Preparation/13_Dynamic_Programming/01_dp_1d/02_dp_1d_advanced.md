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

## Subarray DP (Max Sum / Max Product)

### Maximum Subarray (Kadane's Algorithm)

**🔗 Practice Link:** [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/)

**Problem Explanation:**
Given an integer array `nums`, find the contiguous subarray (a consecutive slice containing at least one element) with the largest sum, and return that sum. "Contiguous subarray" means elements must be adjacent in the array, unlike a subsequence where you may skip elements. For example, in `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]` the maximum-sum subarray is `[4, -1, 2, 1]`, whose sum is 6.

**State Definition:**
`dp[i]` = the maximum sum of any contiguous subarray that **ends at index i** (so it must include `nums[i]`). The overall answer is the maximum of `dp[i]` over all i, tracked as `max_so_far`.

**Recurrence Relation:**
`dp[i] = max(nums[i], dp[i-1] + nums[i])`
At index i there are exactly two ways to build the best subarray ending here: start a fresh subarray with `nums[i]` alone, or extend the best subarray that ended at i-1 by appending `nums[i]`. Whichever sum is larger wins — this is why the technique is called Kadane's algorithm.

**Base Cases:**
- `dp[0] = nums[0]` (the first element is the only subarray ending at index 0).
- The recurrence and answer tracking are initialized from `nums[0]` — never from 0, because the array may be entirely negative.

**Intuition (Why This Works):**
Think of a traveler walking along the array. At each position they ask: "Is it better to continue the current streak, or start a new streak from here?" A subarray is a contiguous block, so the best block ending at i can only come from the best block ending at i-1 (or a fresh start) — this gives optimal substructure with a single scalar state, and the same local decision repeats at every index (overlapping subproblems). Storing one best value per position turns the O(n²) check of every possible slice into a single O(n) pass.

**Step-by-Step Procedure:**
1. Initialize `max_ending_here = max_so_far = nums[0]`.
2. Loop over each `num` in `nums[1:]` (all elements after the first).
3. `max_ending_here = max(num, max_ending_here + num)` — extend or restart.
4. `max_so_far = max(max_so_far, max_ending_here)` — update the global best.
5. After the loop return `max_so_far`.
6. (Variant that also returns the subarray) track `start`, `end`, and a candidate `temp_start`; update `temp_start` only when a fresh subarray wins, and commit `start/end` whenever the global best improves.

**Worked Example (Dry Run):**
`nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`.

```
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

**Code:**
```python
def max_subarray_kadane(nums: list) -> int:
    # Initialize with the first element, NOT 0, because the array may be all negative
    max_ending_here = max_so_far = nums[0]
    for num in nums[1:]:
        # KEY DECISION: extend the current subarray or start fresh?
        # If the element alone is larger than the extended sum, restart
        max_ending_here = max(num, max_ending_here + num)
        # Track the best subarray sum seen at any position so far
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far

# Variant: also return the actual subarray (indices) that achieves the max
def max_subarray_with_indices(nums: list) -> tuple:
    max_ending_here = max_so_far = nums[0]
    start = end = temp_start = 0     # committed window + candidate window start
    for i in range(1, len(nums)):
        # If starting a new subarray here beats extending, move the candidate start
        if nums[i] > max_ending_here + nums[i]:
            max_ending_here = nums[i]
            temp_start = i
        else:
            max_ending_here += nums[i]
        # Whenever the running max improves, commit the candidate window
        if max_ending_here > max_so_far:
            max_so_far = max_ending_here
            start, end = temp_start, i
    return max_so_far, nums[start:end + 1]
```

**Complexity:**
- Time: O(n) — a single pass.
- Space: O(1) — only a few scalar variables.

**Common Mistakes & Edge Cases:**
- Initializing with 0 instead of `nums[0]`: for all-negative arrays this wrongly returns 0 instead of the largest (least negative) element.
- Empty array: index `nums[0]` raises IndexError; decide on a convention (return 0) and guard if needed.
- Forgetting to update `max_so_far` on the very first element.
- In the indices variant, updating `start/end` only on strict improvement (`>`), so the first occurrence of the max is kept.

### Maximum Circular Subarray Sum

**🔗 Practice Link:** [Maximum Circular Subarray Sum](https://leetcode.com/problems/maximum-sum-circular-subarray/)

**Problem Explanation:**
Same goal as Maximum Subarray, but the array is treated as a **circle**: the subarray may wrap around the end and continue at the beginning (but it still cannot use the same element twice). Given `nums`, return the maximum sum of a contiguous circular subarray. For example, `nums = [5, -3, 5]` → the best is 10, from the wrapping subarray [5, 5] that skips the middle -3.

**State Definition:**
Two cases are combined. For the non-wrapping case, reuse the Kadane state `dp[i]` = best subarray sum ending at i. For the wrapping case, the relevant quantity is the **minimum** subarray sum `minSubarray` of the middle slice (computed by running Kadane on the negated array).

**Recurrence Relation:**
`answer = max(nonCircular, total - minSubarray)` where `nonCircular = kadane(nums)`, `total = sum(nums)`, and `minSubarray = -kadane([-x for x in nums])`.
The best circular subarray is either a normal (non-wrapping) subarray, or it wraps around — and a wrapping subarray is exactly the complement of a contiguous middle slice with the minimum sum. So `max wrapping sum = total - minSubarray`.

**Base Cases:**
- Kadane's base: `dp[0] = arr[0]` for each of the two Kadane runs.
- Special case: if `total - minSubarray == 0` (which happens only when every element is negative, so "wrapping around" would select nothing), return `nonCircular` instead.

**Intuition (Why This Works):**
In a circle, every contiguous slice is either contained in the middle (no wrap) or contains both ends (wraps around). The wrapped slice's complement — the part it skips — is also a contiguous slice. To maximize the wrapped sum we must skip the *minimum* slice, so the best wrapped sum equals the total minus the minimum subarray. The minimum is found with the same Kadane recurrence by negating all elements (max of negatives = -min). This reduces the circular problem to two O(n) linear runs plus the all-negative correction.

**Step-by-Step Procedure:**
1. Define a helper `kadane(arr)` returning the max subarray sum (standard Kadane).
2. `non_circular = kadane(nums)`.
3. `total = sum(nums)`.
4. `min_subarray = kadane([-x for x in nums])` — Kadane on negated values yields the negation of the minimum subarray sum.
5. `circular = total + min_subarray` (this equals `total - (-minSubarray)`).
6. If `circular == 0` (all elements negative), return `non_circular`.
7. Otherwise return `max(non_circular, circular)`.

**Worked Example (Dry Run):**
`nums = [5, -3, 5]`.

```
Non-circular best subarray: [5, -3, 5] = 7   (whole array; Kadane finds it)
Circular wrap-around:       [5, 5] = 5 + 5 = 10  (skipping the middle -3)

Visualization of circular:
       ┌─── 5 ───┐
       │          │
      -3          5
       │          │
       └──────────┘

  Wrap-around subarray: [5 (end), 5 (start)] = total - min_subarray = 10

Step-by-step values:
  kadane([5, -3, 5]):    cur: 5 → 2 → 7,   res = 7          → non_circular = 7
  total = 5 + (-3) + 5 = 7
  kadane([-5, 3, -5]):   cur: -5 → 3 → -2, res = 3          → min_subarray = -3
  circular = total + min_subarray = 7 + 3 = 10   (= total - min_subarray)

  Answer: max(7, 10) = 10  (the wrapping [5, 5])
```

**Answer: 10** — the wrapping subarray [5, 5].

**Code:**
```python
def max_circular_subarray(nums: list) -> int:
    def kadane(arr: list) -> int:
        # Standard Kadane's algorithm for the max subarray sum
        cur = res = arr[0]
        for v in arr[1:]:
            cur = max(v, cur + v)   # extend or restart
            res = max(res, cur)     # keep global best
        return res

    non_circular = kadane(nums)                 # best middle (non-wrapping) subarray
    total = sum(nums)
    min_subarray = kadane([-x for x in nums])   # max of negated = -min of original
    circular = total + min_subarray             # total - (-min) = total + max_of_negated

    if circular == 0:   # All elements negative; circular would be empty
        return non_circular
    return max(non_circular, circular)
```

**Complexity:**
- Time: O(n) — two Kadane passes plus a sum.
- Space: O(1) (the negated list costs O(n) memory; use an inline generator to make it O(1)).

**Common Mistakes & Edge Cases:**
- Forgetting the all-negative special case: with, e.g., `[-3, -2, -3]`, `total - minSubarray = -8 + 8 = 0`, which would be returned as a bogus 0 instead of -2.
- Single-element arrays: `circular == 0` triggers and correctly returns the element itself.
- Confusing `minSubarray` with the *maximum* subarray — the negation trick is easy to sign-flip; always double check `circular = total + kadane(negated)`.
- The wrapping subarray cannot be the whole circle twice; complement logic inherently avoids double-use.

### Maximum Product Subarray

**🔗 Practice Link:** [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/)

**Problem Explanation:**
Given an integer array `nums`, find the contiguous subarray with the **largest product** (rather than sum) and return that product. Since products are involved, signs matter: a very negative running product can become a very positive one after multiplying by another negative number. For example, `nums = [2, 3, -2, 4]` → the answer is 6, from the subarray [2, 3] (6 beats 2·3·(-2)·4 = -48 and 3·(-2)·4 = -24).

**State Definition:**
- `max_prod[i]` = the largest product of any contiguous subarray ending at index i.
- `min_prod[i]` = the smallest (most negative) product of any contiguous subarray ending at index i — kept because a negative × negative can flip into a new maximum.

**Recurrence Relation:**
`max_prod[i] = max(nums[i], max_prod[i-1] * nums[i], min_prod[i-1] * nums[i])`
`min_prod[i] = min(nums[i], max_prod[i-1] * nums[i], min_prod[i-1] * nums[i])`
Unlike sums, multiplication by a negative number reverses ordering, so the best product ending at i is either a fresh start, the extension of the previous *maximum*, or the extension of the previous *minimum* — all three are candidates.

**Base Cases:**
- `max_prod[0] = min_prod[0] = nums[0]`.
- The global result is initialized to `nums[0]` (never 0 or 1).

**Intuition (Why This Works):**
For sums, "more is better" always, so one running value suffices. For products, the value that looks worst (most negative) can become the best after one negative multiplier — so the DP state must hold *two* values, the max and the min, for every prefix. This is still optimal substructure with a 2-element state vector: the max/min ending at i depend only on the max/min ending at i-1. Overlapping subproblems are avoided because each prefix's pair is computed exactly once and reused for the next step.

**Step-by-Step Procedure:**
1. Initialize `max_prod = min_prod = result = nums[0]`.
2. Loop over each `num` in `nums[1:]`.
3. Build the candidate triple `(num, max_prod * num, min_prod * num)`.
4. `max_prod = max(candidates)` — best product ending here.
5. `min_prod = min(candidates)` — worst product ending here (for future negatives).
6. `result = max(result, max_prod)` — update the global best.
7. Return `result`.

**Worked Example (Dry Run):**
`nums = [2, 3, -2, 4]`.

```
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

**Code:**
```python
def max_product_subarray(nums: list) -> int:
    # max_prod: max product of a subarray ending at the current position
    # min_prod: min product (needed because neg * neg = pos)
    max_prod = min_prod = result = nums[0]
    for num in nums[1:]:
        # Three candidates: start fresh, extend the max, extend the min
        candidates = (num, max_prod * num, min_prod * num)
        max_prod = max(candidates)   # current best product ending here
        min_prod = min(candidates)   # current worst product (for future negatives)
        result = max(result, max_prod)  # global best so far
    return result
```

**Complexity:**
- Time: O(n).
- Space: O(1).

**Common Mistakes & Edge Cases:**
- Tracking only the running max (sum-style): fails as soon as a negative number appears — the min must be tracked too.
- Initializing with 0 or 1: breaks all-negative arrays and arrays starting at 0; initialize with `nums[0]`.
- Zeros: a zero resets the product to 0 (a subarray containing 0 has product 0); the three-candidate formula handles this because `x * 0 = 0` gets compared against a fresh start.
- Arrays like `[-2, -3]` → 6 (both negatives multiply positive) — the min-tracking makes this work.
- Overflow in fixed-width languages; Python ints are unbounded so this is only a concern elsewhere.

---

## Subsequence & Chain DP

### Longest Alternating Subsequence

**🔗 Practice Link:** [Longest Alternating Subsequence](https://www.geeksforgeeks.org/longest-alternating-subsequence)

**Problem Explanation:**
Given an array, find the length of the **longest alternating (wiggle) subsequence**: a subsequence in which consecutive elements strictly alternate between increasing and decreasing. A subsequence preserves order but may skip elements. For example, in `[1, 7, 4, 9, 2, 5]` the whole array alternates (1 < 7 > 4 < 9 > 2 < 5) → length 6. The same problem is known as the **Wiggle Subsequence** on LeetCode.

**State Definition:**
- `up` = the length of the longest alternating subsequence of the prefix seen so far that ends with an **up** move (last step was increasing).
- `down` = the same, but ending with a **down** move (last step was decreasing).

**Recurrence Relation:**
- if `nums[i] > nums[i-1]`: `up = down + 1`
- if `nums[i] < nums[i-1]`: `down = up + 1`
An up move must follow a down move and vice versa, so when the current pair is increasing, the only way to extend an alternating sequence is to append to a sequence that ended *down*; symmetric logic applies for a decreasing pair. The answer is `max(up, down)`.

**Base Cases:**
- `up = down = 1` (a single element is an alternating sequence of length 1; its "last move" is unspecified, so both states start at 1).
- Empty array → 0.

**Intuition (Why This Works):**
Only the direction of the *last* move matters for extending an alternating sequence — the exact last value does not, because any extension direction is achievable with the current element. That gives a two-state DP (up/down), and scanning adjacent pairs with these two counters fully captures all possible alternating subsequences. When two adjacent elements are equal, no direction change happens and neither state changes. This is the same two-state tracking idea used by the max-product problem, applied to trend direction.

**Step-by-Step Procedure:**
1. If `nums` is empty, return 0.
2. Initialize `up = down = 1`.
3. Loop `i` from 1 to `len(nums) - 1`.
4. If `nums[i] > nums[i-1]`, set `up = down + 1`.
5. Elif `nums[i] < nums[i-1]`, set `down = up + 1`.
6. (Equal values update nothing.)
7. Return `max(up, down)`.
8. Alternative implementation (`wiggly_max_length`): compare the sign of consecutive differences and count only direction changes.

**Worked Example (Dry Run):**
`nums = [1, 7, 4, 9, 2, 5]`.

| i | compare | action | up | down |
|---|---------|--------|----|------|
| 0 | -       | start  | 1  | 1    |
| 1 | 7 > 1   | up = down + 1 | 2 | 1 |
| 2 | 4 < 7   | down = up + 1 | 2 | 3 |
| 3 | 9 > 4   | up = down + 1 | 4 | 3 |
| 4 | 2 < 9   | down = up + 1 | 4 | 5 |
| 5 | 5 > 2   | up = down + 1 | 6 | 5 |

**Answer: max(6, 5) = 6** — the entire array alternates.

**Code:**
```python
def longest_alternating_subseq(nums: list) -> int:
    if not nums:
        return 0
    up = down = 1                    # length ending with an up/down last move
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:    # current step goes up
            up = down + 1            # can only extend a sequence that ended down
        elif nums[i] < nums[i - 1]:  # current step goes down
            down = up + 1            # can only extend a sequence that ended up
    return max(up, down)

def wiggly_max_length(nums: list) -> int:
    """Alternative implementation of the same problem (Wiggle Subsequence)."""
    if len(nums) < 2:
        return len(nums)
    prev_diff = nums[1] - nums[0]    # direction of the first adjacent pair
    length = 2 if prev_diff != 0 else 1   # equal start -> only one element counts
    for i in range(2, len(nums)):
        diff = nums[i] - nums[i - 1]
        # Count only genuine direction changes (zero cancels either direction)
        if (diff > 0 and prev_diff <= 0) or (diff < 0 and prev_diff >= 0):
            length += 1
            prev_diff = diff         # remember the new direction
    return length
```

**Complexity:**
- Time: O(n).
- Space: O(1).

**Common Mistakes & Edge Cases:**
- Empty array → 0 (the `up = down = 1` version must guard it).
- Constant arrays like `[1, 1, 1]` → 1 (no direction change ever happens).
- Monotonic arrays like `[1, 2, 3, 4, 5]` → 2 (pick any two adjacent elements).
- Equal adjacent values in the middle do not reset the sequence — they are simply skipped (the diff-sign version uses `<= 0` / `>= 0` to ignore them).
- Mixing up `up` and `down` roles: an increasing pair extends a down-ending sequence, not an up-ending one.

### Maximum Length of Pair Chain

**🔗 Practice Link:** [Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/)

**Problem Explanation:**
Given a list of pairs `(a, b)` (think of them as time intervals), you want the longest **chain** of pairs `p1, p2, ...` where pair `(c, d)` may follow pair `(a, b)` only if `b < c` (strictly, the first ends before the second begins). Each pair may be used at most once, and the output is the length of the longest such chain. For example, `pairs = [[1, 2], [2, 3], [3, 4]]` → the longest chain is [1,2] → [3,4], length 2 (note [2,3] cannot follow [1,2] because 2 < 2 is false).

**State Definition:**
This is solvable greedily, not with a dp table. The state is simply:
- `curr_end` = the end value `b` of the last pair accepted into the chain.
- `count` = the number of pairs in the chain so far.

**Recurrence Relation:**
After sorting pairs by their end value `b`, for each pair `(a, b)`: if `a > curr_end`, accept it: `count += 1` and `curr_end = b`; otherwise skip it.
Sorting by the end means the currently accepted pair leaves the *most* room for the remaining pairs, so always taking the first compatible pair is optimal (classic interval-scheduling greedy: "earliest finish time first").

**Base Cases:**
- `curr_end = float('-inf')` (no pair chosen yet, so every first pair is compatible).
- `count = 0`.

**Intuition (Why This Works):**
The chain-ability condition `b < c` depends only on interval ends, so the problem is the interval scheduling / chain maximization family. The greedy exchange argument: if an optimal chain starts with a different pair whose end is no earlier than the smallest-end pair, swapping it for the smallest-end pair cannot hurt the rest of the chain. Therefore a single pass over pairs sorted by end picks the maximum chain.

**Step-by-Step Procedure:**
1. Sort `pairs` by the second element (end) using `pairs.sort(key=lambda x: x[1])`.
2. Initialize `curr_end = float('-inf')` and `count = 0`.
3. For each `(a, b)` in sorted pairs:
4. If `a > curr_end`, accept: `count += 1`, `curr_end = b`.
5. Else skip the pair (it overlaps the current chain end).
6. Return `count`.

**Worked Example (Dry Run):**
`pairs = [[1, 2], [2, 3], [3, 4]]` (already sorted by end).

| step | pair (a,b) | a > curr_end? | count | curr_end |
|------|------------|---------------|-------|----------|
| 0    | -          | -             | 0     | -inf     |
| 1    | [1, 2]     | 1 > -inf → yes| 1     | 2        |
| 2    | [2, 3]     | 2 > 2? no      | 1     | 2        |
| 3    | [3, 4]     | 3 > 2 → yes   | 2     | 4        |

**Answer: 2** — chain [1, 2] → [3, 4]. (A second classic input: `[[5,24],[39,60],[15,28],[27,40],[50,90]]` → 3.)

**Code:**
```python
def find_longest_chain(pairs: list) -> int:
    # Sort by interval END so each accepted pair leaves maximum room after it
    pairs.sort(key=lambda x: x[1])
    curr_end = float('-inf')         # end of the last accepted pair
    count = 0                        # chain length so far
    for a, b in pairs:
        if a > curr_end:             # compatible: this pair starts after our end
            count += 1
            curr_end = b             # accept it; it now defines the boundary
    return count
```

**Complexity:**
- Time: O(n log n) — dominated by the sort.
- Space: O(1) (ignoring the sort's internal storage).

**Common Mistakes & Edge Cases:**
- Sorting by the start instead of the end destroys the greedy guarantee.
- Using `>=` instead of `>`: the chain condition `b < c` is strict, so touching intervals like [1,2] and [2,3] must NOT be chained.
- Empty input → 0; a single pair → 1.
- Negative or zero interval values are fine — `float('-inf')` handles the first pair regardless.
- This greedy solves the *chain length*; if the actual chain pairs are required, collect them during the scan.

### Longest Bitonic Subsequence

**🔗 Practice Link:** [Longest Bitonic Subsequence](https://www.geeksforgeeks.org/longest-bitonic-subsequence-dp-15)

**Problem Explanation:**
Given an array, find the length of the longest **bitonic subsequence**: a subsequence that first strictly increases and then strictly decreases (it may be purely increasing or purely decreasing, in which case the "other half" is empty). Elements keep their relative order but need not be contiguous. For example, in `[1, 11, 2, 10, 4, 5, 2, 1]` the longest bitonic subsequence is `[1, 2, 4, 5, 2, 1]` (or `[1, 11, 10, 5, 2, 1]`), length 6.

**State Definition:**
- `lis[i]` = length of the longest strictly increasing subsequence **ending at** index i (computed left to right).
- `lds[i]` = length of the longest strictly decreasing subsequence **starting at** index i (computed right to left).

**Recurrence Relation:**
- `lis[i] = max(lis[i], lis[j] + 1)` for all `j < i` with `nums[j] < nums[i]`
- `lds[i] = max(lds[i], lds[j] + 1)` for all `j > i` with `nums[j] < nums[i]`
- `answer = max over i of (lis[i] + lds[i] - 1)`
A bitonic sequence has a peak at some index i: the left part is an increasing subsequence ending at i, and the right part is a decreasing subsequence starting at i. Index i is counted in both halves, so subtract 1.

**Base Cases:**
- `lis[i] = 1` and `lds[i] = 1` for all i (a single element alone is length 1 in either direction).
- `n <= 2` → the answer is `n` (any 1 or 2 elements are trivially bitonic).

**Intuition (Why This Works):**
The peak is the key structural insight: pick any index i as the peak, and the problem splits into two independent LIS problems on opposite sides. Since LIS has optimal substructure and its subproblems overlap heavily, the two standard O(n²) LIS passes (one forward, one backward) provide everything needed, and a single scan over all possible peaks combines them. The "choice" is where the peak sits and, within each half, which previous/next element extends the chain.

**Step-by-Step Procedure:**
1. Let `n = len(nums)`; if `n <= 2`, return `n`.
2. Compute `lis` left-to-right: for each i, for each j < i, if `nums[j] < nums[i]`, update `lis[i] = max(lis[i], lis[j] + 1)`.
3. Compute `lds` right-to-left: for each i from n-1 down to 0, for each j > i, if `nums[j] < nums[i]`, update `lds[i] = max(lds[i], lds[j] + 1)`.
4. For each i, compute `lis[i] + lds[i] - 1`.
5. Return the maximum over all i.

**Worked Example (Dry Run):**
`nums = [1, 11, 2, 10, 4, 5, 2, 1]`.

| i | nums[i] | lis[i] (left) | lds[i] (right) | lis + lds - 1 |
|---|---------|---------------|----------------|---------------|
| 0 | 1       | 1             | 1              | 1 |
| 1 | 11      | 2             | 5              | 6 |
| 2 | 2       | 2             | 2              | 3 |
| 3 | 10      | 3             | 4              | 6 |
| 4 | 4       | 3             | 3              | 5 |
| 5 | 5       | 4             | 3              | 6 |
| 6 | 2       | 2             | 2              | 3 |
| 7 | 1       | 1             | 1              | 1 |

(Check a few: `lis[5] = 4` from [1, 2, 4, 5]; `lds[1] = 5` from [11, 10, 5, 2, 1]; the maximum combined value is 6.)

**Answer: 6** — e.g., [1, 2, 4, 5, 2, 1] or [1, 11, 10, 5, 2, 1].

**Code:**
```python
def longest_bitonic_subseq(nums: list) -> int:
    n = len(nums)
    if n <= 2:
        return n                     # 1 or 2 elements are always bitonic

    # LIS computed from the LEFT: longest increasing subsequence ending at i
    lis = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:              # strictly increasing
                lis[i] = max(lis[i], lis[j] + 1)

    # LIS computed from the RIGHT (a decreasing subsequence starting at i):
    # reuse the same increasing logic scanning backward
    lds = [1] * n
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if nums[j] < nums[i]:              # nums[j] is smaller -> decreasing run
                lds[i] = max(lds[i], lds[j] + 1)

    max_len = 0
    for i in range(n):
        # peak at i: combine both halves, subtracting i's double count
        max_len = max(max_len, lis[i] + lds[i] - 1)
    return max_len
```

**Complexity:**
- Time: O(n²) — two nested-loop passes.
- Space: O(n).

**Common Mistakes & Edge Cases:**
- Forgetting the `- 1`: the peak element belongs to both the increasing and the decreasing half, so it gets counted twice.
- Using `<=` anywhere: strict increase/decrease is required.
- Purely increasing or purely decreasing arrays still return n (the other half contributes length 1), which is correct.
- `n <= 2` early return prevents pointless work; a single element is length 1, two elements always length 2.
- The decreasing half must scan from the right and compare `nums[j] < nums[i]` for `j > i` — flipping either the direction or the comparison breaks it.

---

## Minimax & String DP

### Egg Dropping Problem

**🔗 Practice Link:** [Egg Dropping Problem](https://leetcode.com/problems/super-egg-drop/)

**Problem Explanation:**
You have `k` identical eggs and a building with `n` floors. There is a threshold floor `f`: eggs do not break when dropped from any floor below `f`, and break when dropped from floor `f` or above. An egg that survives a drop can be reused; a broken egg is gone. Find the **minimum number of drops** (in the worst case) needed to determine `f`. This is a *minimax* problem: you must guarantee a strategy whose worst-case drop count is as small as possible. For example, with 2 eggs and 6 floors, the answer is 3.

**State Definition:**
`dp[k][n]` = the minimum number of drops needed in the worst case to find the threshold, given `k` eggs and `n` floors.

**Recurrence Relation:**
`dp[k][n] = 1 + min over x in 1..n of ( max(dp[k-1][x-1], dp[k][n-x]) )`
If you drop an egg from floor x, exactly one of two things happens:

```
   Egg BREAKS                    Egg SURVIVES
   ─────────                     ────────────
   You lost 1 egg                Egg is still usable
   Answer is in [1, x-1]         Answer is in [x+1, n]
   Use (k-1) eggs, (x-1) floors  Use k eggs, (n-x) floors

   Worst case = 1 + max(broken_scenario, intact_scenario)

   You choose x to MINIMIZE this worst case.
```

In plain English: if the egg breaks, you must search the x-1 floors below with only k-1 eggs (`dp[k-1][x-1]`); if it survives, you keep all k eggs and only the n-x floors above remain (`dp[k][n-x]`). You must be prepared for the worse of the two branches (the `max`), and you pick the first-drop floor x that minimizes that worst case (the `min`).

**Base Cases:**
- `dp[1][n] = n` — with one egg you must scan floors bottom-up, worst case n drops.
- `dp[k][0] = 0` — zero floors need zero drops.
- `dp[k][1] = 1` — one floor always takes one drop.

**Intuition (Why This Works):**
Every drop is a decision that splits the problem into two independent subproblems (below x with k-1 eggs, above x with k eggs), each a smaller instance of the same problem — optimal substructure. The same `(k, floors)` state reappears from many different paths, so caching (or tabulating) it avoids exponential branching. The "choice" is the drop floor x; for a fixed k the function `broken(x) = dp[k-1][x-1]` grows with x while `intact(x) = dp[k][n-x]` shrinks, so the minimax point is where they cross — which the binary-search memoization exploits, and the two-pointer tabulation exploits row by row.

**Step-by-Step Procedure:**
1. Base: if `k == 1` or `n <= 1`, return `n`.
2. Memoized with binary search: for the state `(k, n)`, binary search x in [1, n]:
   - `broken = dp(k-1, x-1)`, `intact = dp(k, n-x)`, `worst = 1 + max(broken, intact)`.
   - If `broken < intact`, move the search up (need a higher floor to balance); else move down.
   - Track `best = min(best, worst)` over every visited midpoint.
3. Cache the result for `(k, n)`.
4. Tabulated: build a `(k+1) x (n+1)` table; row 1 = 0,1,2,...,n; for each k from 2 upward use a pointer `x` that only moves right, filling each cell as `1 + max(dp[k-1][x-1], dp[k][j-x])`.
5. Return `dp[k][n]`.

**Worked Example (Dry Run):**
`k = 2, n = 6`. Complete table (floors across, eggs down):

```
┌───────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ eggs  │  0  │  1  │  2  │  3  │  4  │  5  │  6  │  ← floors
├───────┼─────┼─────┼─────┼─────┼─────┼─────┤
│   1   │  0  │  1  │  2  │  3  │  4  │  5  │  6  │  (1 egg: linear scan)
├───────┼─────┼─────┼─────┼─────┼─────┼─────┤
│   2   │  0  │  1  │  2  │  2  │  3  │  3  │  3  │  ← answer
└───────┴─────┴─────┴─────┴─────┴─────┴─────┘
```

How `dp[2][3] = 2` is computed: drop from floor 2. If it breaks, you have 1 egg and 1 floor below → 1 more drop. If it survives, you have 2 eggs and 1 floor above → 1 more drop. Worst case = 1 + max(1, 1) = 2, and no other first drop does better. Reading `dp[2][6] = 3`: with 2 eggs and 6 floors, 3 drops suffice in the worst case (drop at floors 2, 4, 5 or similar).

**Code:**
```python
def egg_drop_memo(k: int, n: int, memo=None) -> int:
    if memo is None:
        memo = {}
    if k == 1 or n <= 1:
        return n   # 1 egg: must scan linearly; 0 floors: 0 drops; 1 floor: 1 drop
    key = (k, n)
    if key in memo:
        return memo[key]

    # Binary search for the optimal first drop floor x.
    # broken(x) grows with x, intact(x) shrinks with x, so the minimax
    # crossing point is found by bracketing where broken and intact balance.
    lo, hi = 1, n
    best = float('inf')
    while lo <= hi:
        mid = (lo + hi) // 2
        broken = egg_drop_memo(k - 1, mid - 1, memo)   # egg breaks -> floors below
        intact = egg_drop_memo(k, n - mid, memo)       # egg survives -> floors above
        worst = 1 + max(broken, intact)                # you must plan for the worse branch
        if broken < intact:
            lo = mid + 1   # broken side is safer -> try higher to balance
        else:
            hi = mid - 1   # intact side is safer -> try lower to balance
        best = min(best, worst)
    memo[key] = best
    return best

# Tabulation approach:
def egg_drop_tab(k: int, n: int) -> int:
    dp = [[0] * (n + 1) for _ in range(k + 1)]
    for j in range(1, n + 1):
        dp[1][j] = j                       # one egg, j floors -> j drops (linear scan)
    for i in range(2, k + 1):
        x = 1   # Two-pointer: for fixed k, the optimal floor x only increases with j
        for j in range(1, n + 1):
            # Advance x while the next floor gives a better (smaller) worst case
            while x < j and max(dp[i - 1][x - 1], dp[i][j - x]) > \
                              max(dp[i - 1][x], dp[i][j - x - 1]):
                x += 1
            dp[i][j] = 1 + max(dp[i - 1][x - 1], dp[i][j - x])
    return dp[k][n]
```

**Complexity:**
- Time: O(k · n log n) for the memoized binary-search version; O(k · n) for the tabulation with the two-pointer optimization.
- Space: O(k · n) for memo cache / table (memo also has recursion depth O(k)).

**Common Mistakes & Edge Cases:**
- Forgetting the `1 +` before the `max`: every strategy costs the drop you just performed plus the worst continuation.
- Thinking "min" instead of "minimax": you don't get to choose which branch happens — you minimize the *maximum* over the two outcomes.
- Base cases: `k == 1` must return `n` (linear scan), and small n (0 or 1) must terminate quickly; the binary search assumes both `broken` and `intact` are well-defined.
- `k >= n`: the answer is at most `ceil(log2(n+1))` (binary search with unlimited eggs); the code still returns correct values but can be shortcut for speed.
- Deep recursion for large `(k, n)` in the memoized version — prefer tabulation or raise the recursion limit.

### Word Break

**🔗 Practice Link:** [Word Break](https://leetcode.com/problems/word-break/)

**Problem Explanation:**
Given a string `s` and a list of dictionary words `word_dict`, determine whether `s` can be segmented into a sequence of dictionary words. Every word in the segmentation must be in the dictionary, words may be reused, and the entire string must be consumed. For example, `s = "leetcode"`, `word_dict = ["leet", "code"]` → True ("leet" + "code"). Return a boolean.

**State Definition:**
`dp[i]` = True if the first i characters of s, i.e. `s[0:i]`, can be segmented into dictionary words (so dp[n] is the final answer).

**Recurrence Relation:**
`dp[i] = True` if there exists a split point `j` (0 <= j < i) such that `dp[j]` is True **and** `s[j:i]` is a dictionary word.
The prefix up to i is segmentable exactly when some earlier prefix up to j is segmentable and the remaining slice `s[j:i]` is itself one dictionary word — the last word in the segmentation.

**Base Cases:**
- `dp[0] = True` (the empty string is trivially segmentable — it's the start of any segmentation).

**Intuition (Why This Works):**
Think of dp as "can the robot reach position i in the string, stepping only over dictionary words". Every valid segmentation ends in exactly one last word, so the answer for each prefix depends only on answers for *shorter* prefixes that are in the dictionary-distance apart — optimal substructure with heavy overlap (the same prefix is re-examined from many split points), so each dp cell is computed once and reused. The "choice" is the split point j; as soon as one valid j is found for a given i, that cell is done.

**Step-by-Step Procedure:**
1. Convert `word_dict` to a `set` for O(1) membership checks.
2. Let `n = len(s)`; create `dp = [False] * (n + 1)`.
3. Set `dp[0] = True`.
4. For each ending position `i` from 1 to n:
5. For each split point `j` from 0 to i-1:
6. If `dp[j]` is True and `s[j:i]` is in the word set, set `dp[i] = True` and break out of the inner loop.
7. Return `dp[n]`.

**Worked Example (Dry Run):**
`s = "leetcode"`, `word_dict = ["leet", "code"]`.

```
dp[i] = can we segment s[0:i]?

dp[0] = True   (empty string is always segmentable)
dp[1] = F      "l"    not in dict
dp[2] = F      "le"   not in dict
dp[3] = F      "lee"  not in dict
dp[4] = T      "leet" IS in dict → dp[0]=True && s[0:4] in dict = True ✓

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
```

**Answer: True** ("leet" | "code").

**Code:**
```python
def word_break_tab(s: str, word_dict: list) -> bool:
    words = set(word_dict)           # O(1) membership lookup for each slice
    n = len(s)
    dp = [False] * (n + 1)           # dp[i] = s[0:i] segmentable?
    dp[0] = True                     # Base: empty string is segmentable
    for i in range(1, n + 1):        # for each ending position
        for j in range(i):           # try every split point j
            if dp[j] and s[j:i] in words:   # prefix segmentable + suffix is a word
                dp[i] = True
                break                # no need to check other splits for this i
    return dp[n]
```

**Complexity:**
- Time: O(n² · L) with string slicing, where L is the average word length of the `s[j:i]` comparisons (using a trie can reduce it).
- Space: O(n) for the dp array (plus the set of words).

**Common Mistakes & Edge Cases:**
- Forgetting `dp[0] = True` — without it, no word can ever be the "first" word.
- Empty string → True by the base case; empty dictionary with a non-empty string → False.
- Overlapping/duplicate dictionary words are harmless once you use a set.
- Returning True only if the *entire* string is consumed — dp[n], not any intermediate True.
- Naive substring checks make the inner loop O(i) slices; for long strings, break as soon as a valid split is found.

---

## Jump Game DP

### Minimum Jumps to Reach End

**🔗 Practice Link:** [Minimum Jumps to Reach End](https://leetcode.com/problems/jump-game-ii/)

**Problem Explanation:**
Given an array `arr` where `arr[i]` is the maximum jump length you can take from index i (you may jump anywhere from 1 to `arr[i]` steps forward), find the **minimum number of jumps** needed to reach the last index (n-1). If the end is unreachable, return -1. For example, `arr = [2, 3, 1, 1, 4]` → the minimum is 2 (jump from 0 to 1, then 1 to 4). The same idea appears as LeetCode 45 "Jump Game II".

**State Definition:**
`dp[i]` = the minimum number of jumps required to reach index i from index 0.

**Recurrence Relation:**
`dp[i] = min(dp[i], dp[j] + 1)` for every `j < i` with `j + arr[j] >= i`
Index i can be reached in one jump from any reachable index j that can leap at least as far as i (i.e., `j + arr[j] >= i`); adding that one jump to the best way of reaching j gives a candidate, and we take the minimum over all such j.

**Base Cases:**
- `dp[0] = 0` (you start there; zero jumps).
- All other `dp[i] = float('inf')` (unreachable until proven otherwise).
- Final answer is `dp[n-1]`, or -1 if it is still infinity.

**Intuition (Why This Works):**
Each index is a state whose cost depends only on cheaper states before it (optimal substructure), and the same index is a candidate predecessor for many later indices (overlapping subproblems). The "choice" is which previous index jumps into the current one. The same logic can be re-expressed as a BFS: every jump corresponds to a BFS "level", which is what the greedy `jump_game_ii` version below exploits for O(n) time.

**Step-by-Step Procedure:**
1. Let `n = len(arr)`; create `dp = [float('inf')] * n`; set `dp[0] = 0`.
2. For each index `i` from 0 to n-1:
3. If `dp[i]` is still infinity, skip it (unreachable).
4. Else for each jump size `j` in 1..arr[i]: if `i + j < n`, set `dp[i + j] = min(dp[i + j], dp[i] + 1)`.
5. Return `dp[n-1]` if it is not infinity, otherwise -1.
6. (Greedy BFS alternative — O(n)): walk the array once tracking `curr_end` (farthest point of the current jump window) and `farthest` (farthest point reachable anywhere in the window); each time `i` passes `curr_end`, increment the jump count and move the window to `farthest`.

**Worked Example (Dry Run):**
`arr = [2, 3, 1, 1, 4]`.

```
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

**Answer: 2** — path 0 → 1 → 4.

**Code:**
```python
def min_jumps_tab(arr: list) -> int:
    n = len(arr)
    dp = [float('inf')] * n
    dp[0] = 0                        # base: already at the start
    for i in range(n):
        if dp[i] != float('inf'):    # only propagate from reachable positions
            for j in range(1, arr[i] + 1):   # try every legal jump length
                if i + j < n:
                    # reaching i+j via i costs one more jump
                    dp[i + j] = min(dp[i + j], dp[i] + 1)
    return dp[n - 1] if dp[n - 1] != float('inf') else -1
```

**Greedy BFS Approach (Optimal):**
```python
def jump_game_ii(nums: list) -> int:
    """Think of it as BFS levels — each 'jump' = one BFS level."""
    n = len(nums)
    if n <= 1:
        return 0                     # already at the end
    jumps = 0
    curr_end = 0    # end of the current BFS level (current jump range)
    farthest = 0    # farthest reachable point seen so far within the level
    for i in range(n - 1):
        farthest = max(farthest, i + nums[i])  # expand the reach of this level
        if i == curr_end:   # walked the whole current level
            jumps += 1      # need one more jump to open the next level
            curr_end = farthest
            if curr_end >= n - 1:
                break       # the end is inside the new level
    return jumps

# Example trace: nums = [2, 3, 1, 1, 4]
# i=0: farthest=2, curr_end=0 → jumps=1, curr_end=2
# i=1: farthest=4, curr_end=2
# i=2: i==curr_end → jumps=2, curr_end=4 (reached end!)
```

**Complexity:**
- Time: O(n · max_jump) for `min_jumps_tab` (worst case O(n²)); O(n) for the greedy BFS.
- Space: O(n) for the dp version; O(1) for the greedy BFS.

**Common Mistakes & Edge Cases:**
- Unreachable end: with `arr = [3, 2, 1, 0, 4]` the dp version returns -1; the greedy BFS version assumes reachability (LeetCode 45 guarantees it), so it would give a wrong count on unreachable input.
- Single element → 0 jumps; `arr[0] = 0` with more than one element → unreachable (-1).
- When checking candidates, respect `i + j < n` — jumping past the end is not needed.
- In the greedy BFS, the loop runs `range(n - 1)`: the last index itself never needs a jump from itself, and this bound is what makes the algorithm correct.

---

## Game Theory (Interval DP)

### Stone Game I

**🔗 Practice Link:** [Stone Game I](https://leetcode.com/problems/stone-game/)

**Problem Explanation:**
A row of `piles` (each entry is a positive number of stones) lies in front of two players, Alice and Bob. They alternate turns; on each turn a player takes the **entire pile** from either the left end or the right end of the remaining row. Alice moves first. Both play optimally, and the goal is to maximize the total stones collected. Return True if Alice can win (her total strictly greater than Bob's total) assuming optimal play. (LeetCode 877 guarantees an even-length array, which makes Alice always able to win.)

**State Definition:**
`dp[i][j]` = the maximum score **difference** (current player's total minus opponent's total) achievable with optimal play on the subarray `piles[i..j]`. The final answer is `dp[0][n-1] >= 0`.

**Recurrence Relation:**
`dp[i][j] = max(piles[i] - dp[i+1][j], piles[j] - dp[i][j-1])`
If you take the left pile, you immediately gain `piles[i]`, but then your opponent faces `piles[i+1..j]` and will achieve a difference of `dp[i+1][j]` against you — so your net difference is `piles[i] - dp[i+1][j]`. Symmetrically for the right pile; choose the larger net.

**Base Cases:**
- `dp[i][i] = piles[i]` — with a single pile, the current player takes it and the difference is its full value.

**Intuition (Why This Works):**
This is an **interval DP**: the game's state is a contiguous slice `[i, j]` of the row, and each move shrinks the interval from one end. The two players' interests are zero-sum, so a single number (the difference) captures both sides — the current player's gain is exactly the opponent's loss, which is why the opponent's optimal play appears as a subtraction. Subproblems are intervals, and the same interval recurs from many move sequences, so filling the table by increasing interval length and reusing each cell is correct (optimal substructure + overlapping subproblems).

**Step-by-Step Procedure:**
1. Let `n = len(piles)`; create `dp` as an `n x n` table.
2. Fill the diagonal: `dp[i][i] = piles[i]` (single-pile intervals).
3. Loop `length` from 2 to n (interval size):
4. For each `i` from 0 to `n - length`:
5. Let `j = i + length - 1`.
6. Set `dp[i][j] = max(piles[i] - dp[i+1][j], piles[j] - dp[i][j-1])`.
7. Return `dp[0][n-1] >= 0` (Alice wins if her difference is non-negative).

**Worked Example (Dry Run):**
`piles = [5, 3, 1, 4]` (interval DP filled by increasing length).

```
Subarrays of length 1:  dp[i][i] = piles[i]
  dp[0][0]=5  dp[1][1]=3  dp[2][2]=1  dp[3][3]=4

Subarrays of length 2:
  dp[0][1] = max(5-3, 3-5) = max(2,-2) = 2   → take 5
  dp[1][2] = max(3-1, 1-3) = max(2,-2) = 2   → take 3
  dp[2][3] = max(1-4, 4-1) = max(-3,3) = 3   → take 4

Subarrays of length 3:
  dp[0][2] = max(5-dp[1][2], 1-dp[0][1]) = max(5-2, 1-2) = max(3,-1) = 3
  dp[1][3] = max(3-dp[2][3], 4-dp[1][2]) = max(3-3, 4-2) = max(0,2) = 2

Full array (length 4):
  dp[0][3] = max(5-dp[1][3], 4-dp[0][2]) = max(5-2, 4-3) = max(3,1) = 3
```

**Answer: dp[0][3] = 3 >= 0 → Alice can always win.**

**Code:**
```python
def stone_game_i(piles: list) -> bool:
    """Alice wins with optimal play; dp[i][j] = score difference on piles[i..j]."""
    n = len(piles)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = piles[i]          # Base: single pile -> take it all
    # Fill by increasing subarray length (intervals get longer each round)
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            # Take left:  gain piles[i], opponent plays optimally on [i+1..j]
            # Take right: gain piles[j], opponent plays optimally on [i..j-1]
            dp[i][j] = max(piles[i] - dp[i + 1][j],
                           piles[j] - dp[i][j - 1])
    return dp[0][n - 1] >= 0   # non-negative difference means Alice wins
```

**Complexity:**
- Time: O(n²).
- Space: O(n²) (only the previous anti-diagonal is needed, so it can be reduced to O(n) with a rolling array).

**Common Mistakes & Edge Cases:**
- Subtracting instead of adding the opponent's share: the opponent's optimal difference *against you* must be subtracted from what you take now.
- Filling order: you must fill by interval length, not by row or column, because `dp[i][j]` depends on the shorter intervals `[i+1][j]` and `[i][j-1]`.
- Single-pile intervals are the base — forget them and the length-2 cells read garbage.
- The code handles odd-length arrays fine, but LeetCode 877 guarantees even length (where the standard parity argument already proves Alice wins).
- Interpreting the boolean: return `dp[0][n-1] >= 0`, i.e., Alice's difference is non-negative (with the guarantee of even length it will always be > 0).

### Stone Game II (pick 1 to 2x previous)

**🔗 Practice Link:** [Stone Game II](https://leetcode.com/problems/stone-game-ii/)

**Problem Explanation:**
Alice and Bob again take stones from the left end of a row of `piles`. The twist: there is a parameter `M` that starts at 1. On each turn, the player may take the first **1 to 2·M** piles; if they take `x` piles, then `M` is updated to `max(M, x)` for the opponent. Both play optimally. Return the maximum number of stones Alice can collect. For example, `piles = [2, 7, 9, 4, 4]` → Alice can guarantee 10.

**State Definition:**
`dp[i][m]` = the maximum number of stones the **current player** can collect from the suffix `piles[i:]` (from index i to the end), given the current value of `M = m`.

**Recurrence Relation:**
- If `i + 2*m >= n`: `dp[i][m] = suffix[i]` (the player can take every remaining pile).
- Else: `dp[i][m] = max over x in 1..2m of ( suffix[i] - dp[i+x][max(x, m)] )`
After taking x piles, the opponent faces `piles[i+x:]` with the new M, and optimally collects `dp[i+x][max(x, m)]`. The stones that remain available to the current player total `suffix[i]`, so the current player's share is that total minus the opponent's optimal share.

**Base Cases:**
- `dp[i][m] = suffix[i]` whenever `i + 2*m >= n` — the whole remaining suffix can be taken in one move.
- The suffix sums themselves are precomputed from right to left.

**Intuition (Why This Works):**
The state is the pair (current index, current M) — the history of previous turns is fully summarized by M, because M only ever grows. This is optimal substructure: whatever Alice takes, the remainder is a smaller instance of the same game with a (possibly larger) M, and subproblems overlap because the same (i, m) can be reached by many different plays. The "choice" is how many piles x to take (from 1 up to 2m). The suffix-sum trick makes the "stones available from i onward" an O(1) lookup.

**Step-by-Step Procedure:**
1. Let `n = len(piles)`; compute `suffix[i] = sum(piles[i:])` by scanning right to left.
2. Create `dp` as an `n x (n+1)` table (m ranges 1..n).
3. For `i` from n-1 down to 0:
4. For `m` from 1 to n:
5. If `i + 2*m >= n`, set `dp[i][m] = suffix[i]` (can take everything now).
6. Else try every `x` in 1..2m: candidate = `suffix[i] - dp[i + x][max(x, m)]`; keep the maximum.
7. Return `dp[0][1]` (the game starts at index 0 with M = 1).

**Worked Example (Dry Run):**
`piles = [2, 7, 9, 4, 4]`, so `suffix = [26, 24, 17, 8, 4, 0]`.

| i | suffix[i] | dp[i][1] | reasoning |
|---|-----------|----------|-----------|
| 4 | 4         | 4        | i + 2 = 6 >= 5 → can take all remaining |
| 3 | 8         | 8        | i + 2 = 5 >= 5 → can take all remaining (piles[3:]) |
| 2 | 17        | 13       | take 1 pile: 17 - dp[3][1] = 9; take 2: 17 - dp[4][2] = 17 - 4 = 13 → 13 |
| 1 | 24        | 16       | take 1: 24 - dp[2][1] = 11; take 2: 24 - dp[3][2] = 24 - 8 = 16 → 16 |
| 0 | 26        | 10       | take 1: 26 - dp[1][1] = 10; take 2: 26 - dp[2][2] = 26 - 17 = 9 → 10 |

Alice takes piles[0] (= 2), leaving `[7, 9, 4, 4]` with M = 1 for Bob; Bob optimally collects 16, so Alice ends with 26 - 16 = 10. **Answer: 10.**

**Code:**
```python
def stone_game_ii(piles: list) -> int:
    n = len(piles)
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + piles[i]   # total stones from index i to the end

    # dp[i][m] = best stones the current player can get from piles[i:] with M = m
    dp = [[0] * (n + 1) for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for m in range(1, n + 1):
            if i + 2 * m >= n:
                dp[i][m] = suffix[i]           # can sweep up everything remaining
            else:
                best = 0
                for x in range(1, 2 * m + 1):  # choose how many piles to take now
                    if i + x < n:
                        # Total available minus opponent's optimal share afterwards
                        best = max(best, suffix[i] - dp[i + x][max(x, m)])
                dp[i][m] = best
    return dp[0][1]                            # start at index 0 with M = 1
```

**Complexity:**
- Time: O(n³) worst case (two outer dimensions plus the x loop).
- Space: O(n²).
- Can be optimized: `dp[i][m] = max(dp[i][m], dp[i+2*m][m] + sum(i .. i+2*m-1))` exploits monotonicity to remove the inner loop.

**Common Mistakes & Edge Cases:**
- Forgetting that M is updated to `max(M, x)`, not just `x` — when you take few piles, the opponent's M stays the old (larger) value.
- Reading dp cells before they are computed: the outer loop must go from the end of the array backward (or fill by decreasing i), because `dp[i][...]` depends on `dp[i+x][...]` for x > 0.
- Using a plain slice sum in the inner loop makes it O(n) per candidate — precompute suffix sums so the "available total" is O(1).
- Out-of-bounds: guard `i + x < n` inside the x loop, and let `i + 2*m >= n` short-circuit the whole move search.
- Only tracking Alice's total from a single play — the recurrence must model *both* players' optimal play (which is why the opponent's best share is subtracted).

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
