# Knapsack Extra Variants

This file covers 8 advanced knapsack-flavoured problems not in the guide or advanced files.
Bounded Knapsack (binary splitting) is already in `02_knapsack_advanced.md` so it is not
repeated here. Every problem below uses the same loop-direction rule: 0/1 = right-to-left,
unbounded = left-to-right. Read files 01 and 02 first if that rule is not yet second nature.

---

## 1. Bags of Tokens (LC #948) — Medium

**🔗 Practice Link:** [1. Bags of Tokens](https://leetcode.com/problems/bag-of-tokens/)

### Problem Explanation
You have an array `tokens` where `tokens[i]` is the value of the i-th token. You start with
`power = 0` and `score = 0`. In one move you may play a token face-up (lose `power = tokens[i]`
but gain 1 score) if you have enough power, or face-down (gain `power = tokens[i]` but lose 1
score) if score > 0. Each token is used at most once. Return the maximum score you can achieve.

### State Definition
`dp[i][j]` = maximum power achievable after processing the sorted tokens from index `i` to `j`
with the current score implied by `(original_tokens_count - (j - i + 1)) / 2` swaps made.
Equivalently, after sorting, we use a two-pointer / DP approach on the sorted array.

### Recurrence Relation
```
After sorting tokens:
dp[i][j] = max(dp[i+1][j],                # skip tokens[i]
               dp[i+1][j-1] + tokens[j]   # play tokens[i] face-down (gain power)
              ) if score > 0
dp[i][j] = dp[i+1][j]                      # can only play face-up or skip
```
In practice, a greedy two-pointer approach on the sorted array suffices: try to score with
the smallest token (cheap face-up), gain power with the largest token (face-down).

### Base Cases
- `power >= tokens[i]`: can always play token `i` face-up.
- `score > 0`: can play face-down to gain power.
- Two pointers `lo = 0`, `hi = n - 1` on sorted tokens.

### Intuition (Why This Works)
After sorting, the optimal strategy is to always score with the cheapest token (face-up) and
gain power from the most expensive token (face-down). A two-pointer simulation captures this
greedy: move `lo` right when scoring, move `hi` left when gaining power.

### Step-by-Step Procedure
1. Sort `tokens` in ascending order.
2. Initialize `lo = 0`, `hi = n - 1`, `power = 0`, `score = 0`, `best = 0`.
3. While `lo <= hi`:
   - If `power >= tokens[lo]`: play face-up — `power -= tokens[lo]`, `score += 1`, `lo += 1`.
   - Else if `score > 0`: play face-down — `power += tokens[hi]`, `score -= 1`, `hi -= 1`.
   - Else: break (cannot play any more).
   - Update `best = max(best, score)`.
4. Return `best`.

### Worked Example (Dry Run)
`tokens = [100, 200, 300, 400]`, sorted = `[100, 200, 300, 400]`.

```
Step 1: lo=0, hi=3, power=0, score=0. power<100, score=0 → break? No, try face-down but score=0.
        Actually: power < tokens[lo]=100 and score=0 → break immediately.
        Wait — let's retry with a better example.

tokens = [6, 0, 3, 7], sorted = [0, 3, 6, 7]
Step 1: lo=0, hi=3, power=0, score=0. power>=0 → face-up: power=0, score=1, lo=1, best=1
Step 2: lo=1, hi=3, power=0, score=1. power<3, score>0 → face-down: power=7, score=0, hi=2
Step 3: lo=1, hi=2, power=7, score=0. power>=3 → face-up: power=4, score=1, lo=2, best=1
Step 4: lo=2, hi=2, power=4, score=0. power>=6? No. score=0? Yes → break.

Answer: 1
```

### Code
```python
class Solution:
    def bagOfTokensScore(self, tokens: list, power: int) -> int:
        tokens.sort()
        lo, hi = 0, len(tokens) - 1
        score = 0
        best = 0
        while lo <= hi:
            if power >= tokens[lo]:
                # Face-up: spend power, gain 1 score
                power -= tokens[lo]
                score += 1
                lo += 1
                best = max(best, score)
            elif score > 0:
                # Face-down: gain power, lose 1 score
                power += tokens[hi]
                score -= 1
                hi -= 1
            else:
                break
        return best
```

### Complexity
- Time: O(n log n) for sorting + O(n) for the two-pointer scan.
- Space: O(1) extra (in-place sort).

### Common Mistakes & Edge Cases
- **All tokens cost more than power and score is 0:** answer is 0 (cannot start).
- **Zero-cost tokens:** always free to score, take them all first.
- **Single token:** face-up if power is enough, else 0.
- **Greedy correctness:** sorting is essential — without it the two-pointer approach fails.
- **Leaving score on the table:** always track `best` since score fluctuates.

---

## 2. Partition Equal Subset Sum with Exactly K Subsets (LC #698) — Medium

**🔗 Practice Link:** [2. Partition Equal Subset Sum with Exactly K Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/)

### Problem Explanation
Given an integer array `nums` and an integer `k`, return `True` if it is possible to divide
this array into `k` non-empty subsets whose sums are all equal. Each element belongs to
exactly one subset. This is harder than the 2-subset partition because `k` can be any value.

### State Definition
`dp[mask]` = the running sum of the current subset being formed, modulo `target_sum`, for the
subset of elements indicated by the bitmask `mask`. `mask` is an n-bit integer where bit `i`
set means `nums[i]` has been assigned to some subset.

### Recurrence Relation
```
For each mask from 1 to (1<<n) - 1:
  pick the lowest set bit j in mask:
    prev = mask ^ (1 << j)
    new_sum = (dp[prev] + nums[j]) % target_sum
    if dp[prev] + nums[j] == target_sum:
        dp[mask] = 0          # current subset full, start a new one
        subsets_formed[mask] = subsets_formed[prev] + 1
    else:
        dp[mask] = new_sum
```
Return `True` if `subsets_formed[(1<<n)-1] == k`.

### Base Cases
- `dp[0] = 0`, `subsets_formed[0] = 0`.
- If `total % k != 0`: return `False`.
- `target_sum = total // k`.

### Intuition (Why This Works)
A bitmask represents which elements have been placed. As we build each subset, we track the
running sum. When the running sum hits `target_sum`, a subset is complete (reset to 0, increment
count). The bitmask DP avoids duplicates because each element is placed exactly once. We prune
if any single element exceeds `target_sum`.

### Step-by-Step Procedure
1. Compute `total = sum(nums)`. If `total % k != 0`, return `False`.
2. Set `target_sum = total // k`. Sort `nums` descending; if `nums[-1] > target_sum`, return `False`.
3. Initialize `dp = [-1] * (1 << n)`, `dp[0] = 0`, `subsets = [0] * (1 << n)`.
4. For `mask` from 1 to `(1 << n) - 1`:
   - Find the lowest set bit `j`, set `prev = mask ^ (1 << j)`.
   - If `dp[prev] == -1`: skip (prev was invalid).
   - Compute `new_sum = dp[prev] + nums[j]`.
   - If `new_sum > target_sum`: skip.
   - If `new_sum == target_sum`: `dp[mask] = 0`, `subsets[mask] = subsets[prev] + 1`.
   - Else: `dp[mask] = new_sum`, `subsets[mask] = subsets[prev]`.
5. Return `subsets[(1 << n) - 1] == k`.

### Worked Example (Dry Run)
`nums = [4, 3, 2, 3, 5, 2, 1]`, `k = 4`. `total = 20`, `target_sum = 5`.

```
Sorted desc: [5, 4, 3, 3, 2, 2, 1], n=7, masks 0..127.

mask=0000001 (j=0): dp=0+5=5==5 → dp=0, subsets=1
mask=0000010 (j=1): dp=0+4=4 → dp=4, subsets=0
mask=0000100 (j=2): dp=0+3=3 → dp=3, subsets=0
mask=0000101 (j=0, prev=100): dp[100]=0, 0+5=5==5 → dp=0, subsets=2
...
mask=1111111 (all): dp=0, subsets=4 → 4==k → True
```

### Code
```python
class Solution:
    def canPartitionKSubsets(self, nums: list, k: int) -> bool:
        total = sum(nums)
        if total % k != 0:
            return False
        target_sum = total // k
        nums.sort(reverse=True)
        if nums[0] > target_sum:
            return False
        n = len(nums)
        size = 1 << n
        dp = [-1] * size
        subsets = [0] * size
        dp[0] = 0
        for mask in range(1, size):
            # Find the lowest set bit
            j = 0
            temp = mask
            while temp & 1 == 0:
                j += 1
                temp >>= 1
            prev = mask ^ (1 << j)
            if dp[prev] == -1:
                continue
            new_sum = dp[prev] + nums[j]
            if new_sum > target_sum:
                continue
            if new_sum == target_sum:
                dp[mask] = 0
                subsets[mask] = subsets[prev] + 1
            else:
                dp[mask] = new_sum
                subsets[mask] = subsets[prev]
        return subsets[size - 1] == k
```

### Complexity
- Time: O(n * 2^n) — each mask processes one bit.
- Space: O(2^n).

### Common Mistakes & Edge Cases
- **`total % k != 0`:** impossible, return `False` immediately.
- **Single element larger than `target_sum`:** impossible.
- **`k == 1`:** always `True` (the whole array is one subset).
- **All elements equal:** always possible if `n % k == 0`.
- **Bitmask ordering:** process masks in increasing order so `prev < mask` is always solved.

---

## 3. Maximum Profit in Job Scheduling (LC #1235) — Hard

**🔗 Practice Link:** [3. Maximum Profit in Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling/)

### Problem Explanation
You are given `n` jobs, each with a `startTime`, `endTime`, and `profit`. You may schedule
at most one job at a time and jobs must not overlap. Return the maximum total profit from
a set of non-overlapping jobs.

### State Definition
`dp[i]` = maximum profit considering jobs from index `i` to the end, where jobs are sorted
by `endTime`.

### Recurrence Relation
```
Sort jobs by endTime.
dp[i] = max(dp[i+1],                          # skip job i
             profit[i] + dp[next_non_overlap]) # take job i
where next_non_overlap = first j such that startTime[j] >= endTime[i]
```
Binary search finds `next_non_overlap` efficiently.

### Base Cases
- `dp[n] = 0`: no jobs left, profit is 0.
- For each job, either skip it or take it and jump to the next compatible job.

### Intuition (Why This Works)
Sorting by end time and processing from right to left means when we decide to take job `i`,
all jobs that could follow it (ending at or after `startTime[i]`) are to the right and already
solved. Binary search on end times makes the lookup O(log n). This is a classic weighted
interval scheduling problem.

### Step-by-Step Procedure
1. Zip `startTime`, `endTime`, `profit` into a list of jobs.
2. Sort jobs by `endTime`.
3. Extract `end_times = [job[1] for job in jobs]`.
4. Initialize `dp = [0] * (n + 1)`.
5. For `i` from `n-1` down to `0`:
   - Use binary search on `end_times` to find the first `j` where `end_times[j] >= startTime[i]`.
   - `dp[i] = max(dp[i + 1], profit[i] + dp[j])`.
6. Return `dp[0]`.

### Worked Example (Dry Run)
`startTime = [1,2,3,3]`, `endTime = [3,4,5,6]`, `profit = [50,10,40,70]`.

```
Jobs sorted by end: [(1,3,50), (2,4,10), (3,5,40), (3,6,70)]
end_times = [3, 4, 5, 6]

i=3: job (3,6,70). Binary search end_times for >= 3 → j=0. dp[3] = max(0, 70+0) = 70
i=2: job (3,5,40). Binary search end_times for >= 3 → j=0. dp[2] = max(70, 40+0) = 70
i=1: job (2,4,10). Binary search end_times for >= 2 → j=0. dp[1] = max(70, 10+0) = 70
i=0: job (1,3,50). Binary search end_times for >= 1 → j=0.
     Wait: bisect_left on end_times for startTime=1 → j=0 (end_times[0]=3 >= 1).
     dp[0] = max(70, 50 + dp[0]) — that's circular. Let me re-check.

Actually, binary search should find first j where end_times[j] >= startTime[i]:
  i=0: startTime=1, bisect_left(end_times, 1) = 0. dp[0] = max(dp[1], 50 + dp[0]) — wrong.
  The issue: bisect_left finds where to INSERT, giving the index of the first element >= target.
  For i=0: we want jobs ending at or after startTime[0]=1. That's j=0 (end=3).
  But dp[j] = dp[0] which is circular. The fix: j should be the index in dp, not in jobs.

Correct approach: dp[i] = max(dp[i+1], profit[i] + dp[bound(i)]):
  bound(i) = leftmost j such that end_times[j] >= startTime[i]

  i=3: bound = bisect_left(end_times, 6) = 3. dp[3] = max(0, 70+dp[3]) — still circular.

Re-read: the correct formulation processes from right to left with dp indexed by position.
Let me use: dp[i] = max profit from jobs[i:].

  i=3 (job 3,6,70): next = bisect_left(end_times, 6) = 3. dp[3] = max(dp[4], 70+dp[3]) = circular.

The correct formula is dp[i] = max(dp[i+1], profit[i] + dp[next_job_index]):
  next_job_index = first j where jobs[j].end >= jobs[i].start, using bisect_left on end_times.

  i=3: end=6, start=3. bisect_left(end_times, 3) = 0. dp[3] = max(dp[4], 70+dp[0]) = circular.

Hmm — the standard solution uses dp[i] and finds next via bisect_right:
  i=3: start=3. bisect_right(end_times, start=3) = index of first end > 3 → end_times = [3,4,5,6],
        bisect_right([3,4,5,6], 3) = 1. dp[3] = max(0, 70+dp[1]).
  i=2: start=3. bisect_right = 1. dp[2] = max(dp[3], 40+dp[1]).
  i=1: start=2. bisect_right([3,4,5,6], 2) = 0. dp[1] = max(dp[2], 10+dp[0]).
  i=0: start=1. bisect_right([3,4,5,6], 1) = 0. dp[0] = max(dp[1], 50+dp[0]).

Still circular for i=0. The correct formula uses dp[i+1] in the skip case and the binary
search result for the take case, processing right-to-left:

  dp[i] = max(dp[i+1], profit[i] + dp[bisect_right(end_times, start[i])])

  i=3: dp[3] = max(0, 70 + dp[1]) = max(0, 70+10) = 80  (wrong, let me recalc dp[1] first)
```

Let me redo properly (processing right to left):
```
Jobs sorted by end: [(1,3,50), (2,4,10), (3,5,40), (3,6,70)]
end_times = [3, 4, 5, 6]

dp[4] = 0
i=3: start=3. bisect_right(end_times, 3) = 1. dp[3] = max(dp[4], 70+dp[1])
      (dp[1] unknown yet — we process right-to-left so dp[1] isn't solved.)

Actually the standard algorithm processes left-to-right using a different indexing.
Let me use the correct standard approach:

dp[i] = max profit from first i jobs (sorted by end).
For job i (1-indexed):
  j = last job whose end <= start[i] (bisect_right on end_times for start[i])
  dp[i] = max(dp[i-1], profit[i] + dp[j])
```

Correct dry run:
```
Jobs sorted by end (1-indexed): 
  job1=(1,3,50), job2=(2,4,10), job3=(3,5,40), job4=(3,6,70)
end_times = [3, 4, 5, 6]

dp[0] = 0
i=1: start=1. bisect_right(end_times, 1) = 0. dp[1] = max(dp[0], 50+dp[0]) = 50
i=2: start=2. bisect_right(end_times, 2) = 0. dp[2] = max(dp[1], 10+dp[0]) = 50
i=3: start=3. bisect_right(end_times, 3) = 1. dp[3] = max(dp[2], 40+dp[1]) = max(50,90) = 90
i=4: start=3. bisect_right(end_times, 3) = 1. dp[4] = max(dp[3], 70+dp[1]) = max(90,120) = 120

Answer: 120 (jobs 1+4: profit 50+70=120, no overlap since job1 ends at 3, job4 starts at 3)
```

### Code
```python
import bisect

class Solution:
    def jobScheduling(self, startTime: list, endTime: list, profit: list) -> int:
        n = len(startTime)
        jobs = sorted(zip(startTime, endTime, profit), key=lambda x: x[1])
        end_times = [job[1] for job in jobs]
        # dp[i] = max profit using first i jobs (sorted by end time)
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            s, e, p = jobs[i - 1]
            # Find last job whose end time <= start time of current job
            j = bisect.bisect_right(end_times, s, 0, i - 1)
            dp[i] = max(dp[i - 1], p + dp[j])
        return dp[n]
```

### Complexity
- Time: O(n log n) for sorting + O(n log n) for binary searches.
- Space: O(n).

### Common Mistakes & Edge Cases
- **Overlapping jobs with same end time:** `bisect_right` correctly handles equal end times.
- **Jobs with zero duration:** `startTime == endTime` — `bisect_right` returns the right index.
- **All jobs overlap:** only the single most profitable job is selected.
- **`n = 0`:** return 0.
- **Using `bisect_left` vs `bisect_right`:** `bisect_right` ensures we find jobs ending strictly
  before or at the start, avoiding overlap.

---

## 4. Remove Minimum Coins so Pile Differences ≤ K — Medium

**🔗 Practice Link:** [Remove Minimum Coins such that absolute difference between any two piles is less than k](https://www.geeksforgeeks.org/remove-minimum-coins-such-that-absolute-difference-between-any-two-piles-is-less-than-k)

### Problem Explanation
You are given `arr[]` where `arr[i]` is the number of coins in the i-th pile, and an integer
`k`. Remove the **minimum number of coins** overall so that after removal, the absolute
difference between the number of coins in **any two remaining piles** is at most `k`. You are
allowed to remove all coins of a pile, which removes that pile completely. Return the minimum
coins removed.

Examples:
- `arr = [2, 2, 2, 2], k = 0` → `0` (all piles already equal; diff = 0, remove nothing).
- `arr = [1, 5, 1, 2, 5, 1], k = 3` → `2` (trim one coin from each of the two piles of 5:
  they become 4, and every pair now differs by ≤ 3).

### State Definition
After sorting `arr`, the piles we KEEP must all fit inside one window `[L, L + k]` (if the
smallest kept pile is `L` and the largest is `R`, the condition `R - L ≤ k` means the kept
piles form a contiguous sorted segment). So the decision is **which pile is the smallest kept
pile**, i.e. `L = arr[start]`. For a fixed `start`:

- All piles before `start` are removed entirely → cost `prefix[start]`.
- All piles strictly above `arr[start] + k` (after the window) are trimmed DOWN to
  `arr[start] + k` → cost `sum(arr[j] - (arr[start] + k))` for `j` in the right region.
- Piles inside the window stay unchanged → cost 0.

`dp[start]` = minimum coins removed if `arr[start]` is the smallest surviving pile value.

### Recurrence Relation
Let `end` = first index with `arr[end] > arr[start] + k`, and let `prefix[i]` = sum of
`arr[0..i-1]` (prefix sum of the sorted array). Then:

```
window_coins = prefix[end] - prefix[start]          # coins of piles inside the window (kept)
right_count  = n - end                              # number of piles after the window
right_total  = prefix[n] - prefix[end]             # their total coins

dp[start] = prefix[start]                            # remove every pile before window
          + (right_total - right_count * (arr[start] + k))   # trim every pile after window to upper bound
```

`prefix[start] + window_coins + right_count*(arr[start] + k)` equals `total`, so this is
exactly "total − coins allowed to stay" = coins removed. We return `min(dp[start])` over all
`start`. (Removing every pile is always valid, giving cost `total` as the initial upper bound.)

### Base Cases
- If `n == 0`: return 0.
- Upper bound `ans = total` (remove everything).

### Intuition (Why This Works)
The condition "difference between ANY two piles ≤ k" is equivalent to `max − min ≤ k`. Once we
sort, the surviving piles are contiguous, so the problem is: **choose a window of allowed pile
sizes and delete/trim everything outside it**, minimizing what we throw away. There is no 2D
DP here — it is a 1D optimization over the sorted array. Two ways compute `dp[start]`:
1. **Binary search + prefix sum** (O(n log n) time, O(n) space): for each `start`, binary
   search `end`, then use prefix sums for the formula above.
2. **Two-pointer sliding window** (O(n log n) time, O(1) space): keep a valid window
   `[start, end)` as `start` advances, so `cost(start)` is updated in O(1) per step.

### Step-by-Step Procedure (Two-pointer, Expected Approach)
1. Sort `arr`; `n = len(arr)`; `total = sum(arr)`; `ans = total`; `prefix = 0`;
   `window_sum = 0`; `end = 0`.
2. For `start` from `0` to `n-1`:
   - While `end < n` and `arr[end] - arr[start] <= k`: `window_sum += arr[end]; end += 1`.
   - `upper = arr[start] + k`; `right_count = n - end`.
   - `remove_right = (total - prefix - window_sum) - right_count * upper`.
   - `removed = prefix + remove_right`; `ans = min(ans, removed)`.
   - If `end == start`: `end += 1` (empty window, nudge forward); else `window_sum -= arr[start]`.
   - `prefix += arr[start]`.
3. Return `ans`.

### Worked Example (Dry Run)
`arr = [1, 5, 1, 2, 5, 1], k = 3`. Sorted: `[1, 1, 1, 2, 5, 5]`, `total = 15`.

```
start=0, arr[start]=1, upper=4
  window expands to end=4 (covers 1,1,1,2); window_sum=5; prefix=0
  right_count=2; remove_right=(15-0-5) - 2*4 = 10-8 = 2
  removed = 0 + 2 = 2   -> ans = 2
  window_sum -= 1 -> 4; prefix=1

start=1, arr[start]=1, upper=4
  window covers 1,1,2 (window_sum=4); right_count=2
  remove_right=(15-1-4) - 2*4 = 10-8 = 2 ; removed = 1+2 = 3 ; ans stays 2

start=2, arr[start]=1, upper=4
  window_sum=3 (1+2); remove_right=(15-2-3)-2*4 = 10-8=2; removed=2+2=4; ans stays 2

start=3, arr[start]=2, upper=5
  window expands to end=6 (now includes both 5s); window_sum=12; prefix=3
  right_count=0; remove_right=(15-3-12) - 0 = 0; removed=3+0=3; ans stays 2

start=4, arr[start]=5, upper=8
  window_sum=12; remove_right=(15-5-12)= -2; removed=5-2=3; ans stays 2
start=5: removed=3; ans stays 2

Answer: 2   (trim one coin from each pile of 5)
```

### Code

```python
# ---- Expected approach: Two-pointer sliding window, O(n log n) time, O(1) space ----
def minimumCoins(arr: list, k: int) -> int:
    n = len(arr)
    arr.sort()
    total = sum(arr)
    min_removed = total          # removing everything is always valid
    window_sum = 0
    prefix = 0
    end = 0
    for start in range(n):
        # Expand the window to include piles within k of arr[start]
        while end < n and arr[end] - arr[start] <= k:
            window_sum += arr[end]
            end += 1
        # Any pile after the window must be trimmed down to the upper bound
        upper = arr[start] + k
        right_count = n - end
        remove_right = (total - prefix - window_sum) - right_count * upper
        removed = prefix + remove_right
        min_removed = min(min_removed, removed)
        # Slide the window: drop arr[start] from the kept window
        if end == start:
            end += 1
        else:
            window_sum -= arr[start]
        prefix += arr[start]
    return min_removed


# ---- Alternate approach: Binary search + prefix sum, O(n log n) time, O(n) space ----
import bisect

def minimumCoins_prefix(arr: list, k: int) -> int:
    arr.sort()
    n = len(arr)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    ans = prefix[n]
    for i in range(n):
        # skip duplicate values (same L gives same cost)
        if i > 0 and arr[i] == arr[i - 1]:
            continue
        upper = arr[i] + k
        pos = bisect.bisect_right(arr, upper, i, n)   # first index > upper
        # coins removed = all before i  +  (coins after window - capped value)
        remove_after = (prefix[n] - prefix[pos]) - (n - pos) * upper
        ans = min(ans, prefix[i] + remove_after)
    return ans


arr = [1, 5, 1, 2, 5, 1]
k = 3
print(minimumCoins(arr, k))        # 2
print(minimumCoins_prefix(arr, k)) # 2
```

### Complexity
- Time: **O(n log n)** — dominated by sorting; each start is processed once (two-pointer) or
  with one binary search.
- Space: **O(1)** for the two-pointer version; **O(n)** for the prefix-sum version.

### Common Mistakes & Edge Cases
- **Wrong problem framing:** this is NOT a 2D/adjacency DP. The kept piles are a contiguous
  segment of the SORTED array, so it is a 1D optimization, not pairwise removal.
- **Forgetting a whole pile can be removed:** piles before the window are removed entirely
  (cost = their full coin count), they are NOT trimmed to `upper`.
- **Off-by-one with prefix sums:** `prefix[i]` must mean `sum(arr[0..i-1])` so `prefix[n]` is
  the total and `prefix[i]` is "coins before index i".
- **Cap is `arr[start] + k`, not a fixed number:** the upper bound moves with the chosen
  smallest kept pile.
- **Duplicate start values:** skipping `arr[i] == arr[i-1]` avoids recomputing the same cost
  (binary-search version); the two-pointer version handles it naturally.
- **`k = 0`:** then all surviving piles must be exactly equal; the window keeps only one
  distinct value.

---

## 5. Form Array Using Subsequence Sum — Easy/Medium

**🔗 Practice Link:** [5. Form Array Using Subsequence Sum — Easy/Medium](https://www.geeksforgeeks.org/subset-sum-problem-dp-25)

### Problem Explanation
Given an array `nums` and an integer `target`, determine whether there exists a subsequence
of `nums` whose sum equals `target`. A subsequence preserves relative order but may skip
elements. Return `True` if such a subsequence exists, `False` otherwise. This is the
Subset Sum problem framed differently — each element may be used at most once.

### State Definition
`dp[s]` = `True` if a subsequence of the elements seen so far sums to exactly `s`.

### Recurrence Relation
```
dp[s] = dp[s] or dp[s - num]      for s from target down to num
```
(Unchanged from Subset Sum — include `num` or skip it.)

### Base Cases
- `dp[0] = True`: the empty subsequence sums to 0.
- If `target == 0`: return `True` immediately.

### Intuition (Why This Works)
A subsequence is exactly a subset (order does not matter for sums). This is textbook
Subset Sum: iterate elements, update reachable sums right-to-left (0/1 style). The
"subsequence" framing is just flavor — the DP is identical.

### Step-by-Step Procedure
1. Initialize `dp = [False] * (target + 1)`, `dp[0] = True`.
2. For each `num` in `nums`:
   - For `s` from `target` down to `num`:
     - If `dp[s - num]`: `dp[s] = True`.
3. Return `dp[target]`.

### Worked Example (Dry Run)
`nums = [3, 34, 4, 12, 5]`, `target = 9`.

```
dp (size 10):
start:      [T, F, F, F, F, F, F, F, F, F]
num=3:      [T, F, F, T, F, F, F, F, F, F]
num=34:     [T, F, F, T, F, F, F, F, F, F]  (34 > 9, skip)
num=4:      [T, F, F, T, T, F, F, T, F, F]
num=12:     [T, F, F, T, T, F, F, T, F, F]  (12 > 9, skip)
num=5:      [T, F, F, T, T, T, F, T, T, T]
                                              ↑ dp[9] = T (subsequence {4, 5} = 9)

Answer: True
```

### Code
```python
def form_array_subsequence_sum(nums: list, target: int) -> bool:
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                dp[s] = True
    return dp[target]
```

### Complexity
- Time: O(n * target).
- Space: O(target).

### Common Mistakes & Edge Cases
- **`target = 0`:** return `True` (empty subsequence).
- **All elements > `target`:** `dp[target]` stays `False` → return `False`.
- **`nums` empty and `target > 0`:** return `False`.
- **Negative numbers in `nums`:** this approach fails; the standard Subset Sum assumes positive.
- **Wrong loop direction:** left-to-right would allow repeated use of the same element.

---

## 6. Partition Array into Two Arrays to Minimize Sum Difference (LC #2035) — Hard

**🔗 Practice Link:** [6. Partition Array into Two Arrays to Minimize Sum Difference](https://leetcode.com/problems/partition-array-into-two-arrays-to-minimize-sum-difference/)

### Problem Description
Given an integer array `nums`, partition it into two non-empty subsets `A` and `B` such that
`|sum(A) - sum(B)|` is minimized. Return the minimum difference. Every element goes into
exactly one subset.

### State Definition
`dp[s]` = `True` if some subset of `nums` sums to exactly `s`, for `s` in `0..total//2`.

### Recurrence Relation
```
dp[s] = dp[s] or dp[s - num]      for s from target down to num
```
Same as Minimum Subset Sum Difference.

### Base Cases
- `dp[0] = True`: the empty subset.
- `target = total // 2`.

### Intuition (Why This Works)
This is exactly the "Minimum Subset Sum Difference" problem from `01_knapsack_guide.md`.
If one subset sums to `s`, the other sums to `total - s`, giving difference `|total - 2s|`.
We find the largest reachable `s <= total/2` and return `total - 2s`.

### Step-by-Step Procedure
1. Compute `total = sum(nums)`.
2. Set `target = total // 2`.
3. Initialize `dp = [False] * (target + 1)`, `dp[0] = True`.
4. For each `num`, for `s` from `target` down to `num`: `dp[s] |= dp[s - num]`.
5. Scan `s` from `target` down to `0`; first `True` gives the answer.
6. Return `total - 2 * s`.

### Worked Example (Dry Run)
`nums = [1, 6, 11, 5]`. `total = 23`, `target = 11`.

```
dp (size 12):
start:      [T, F, F, F, F, F, F, F, F, F, F, F]
num=1:      [T, T, F, F, F, F, F, F, F, F, F, F]
num=6:      [T, T, F, F, F, F, T, T, F, F, F, F]
num=11:     [T, T, F, F, F, F, T, T, F, F, F, T]
num=5:      [T, T, F, F, F, T, T, T, F, F, T, T]
                                              ↑ scan from 11: dp[11]=T

Answer: total - 2*11 = 23 - 22 = 1
```

### Code
```python
class Solution:
    def minimumDifference(self, nums: list) -> int:
        total = sum(nums)
        target = total // 2
        dp = [False] * (target + 1)
        dp[0] = True
        for num in nums:
            for s in range(target, num - 1, -1):
                if dp[s - num]:
                    dp[s] = True
        for s in range(target, -1, -1):
            if dp[s]:
                return total - 2 * s
        return total
```

### Complexity
- Time: O(n * target), where `target = total // 2`.
- Space: O(target).

### Common Mistakes & Edge Cases
- **Odd total:** minimum difference is at least 1 (cannot split an odd sum into two equal halves).
- **Two elements:** answer is always `|nums[0] - nums[1]|`.
- **All elements equal:** answer is `total % 2` (0 if even count, one element if odd).
- **Large total:** `target` may be up to 10^5; the boolean array is fine but O(n*target) time.
- **Confusing with LC #416 (Equal Subset Sum):** that one asks True/False, this asks for the min diff.

---

## 7. Count of Subsets with Given Difference — Medium

**🔗 Practice Link:** [7. Count of Subsets with Given Difference — Medium](https://www.geeksforgeeks.org/count-of-subsets-with-given-difference)

### Problem Description
Given an array `nums` and an integer `diff`, count the number of ways to partition `nums`
into two subsets such that the difference between their sums equals `diff`. Return the count.

### State Definition
`dp[s]` = number of subsets of `nums` that sum to exactly `s`.

### Recurrence Relation
```
dp[s] = dp[s] + dp[s - num]      for s from target down to num
```
Where `target = (total + diff) // 2` (derived from `sum(A) - sum(B) = diff`).

### Base Cases
- `dp[0] = 1`: the empty subset.
- If `(total + diff) % 2 != 0` or `diff > total`: return 0.

### Intuition (Why This Works)
Let `sum(A) - sum(B) = diff` and `sum(A) + sum(B) = total`. Solving: `sum(A) = (total + diff) / 2`.
So we count subsets summing to `(total + diff) / 2`. This is the "Target Sum" problem from
`02_knapsack_advanced.md` but asking for the count instead of True/False.

### Step-by-Step Procedure
1. Compute `total = sum(nums)`.
2. If `(total + diff) % 2 != 0` or `abs(diff) > total`: return 0.
3. Set `target = (total + diff) // 2`.
4. Initialize `dp = [0] * (target + 1)`, `dp[0] = 1`.
5. For each `num`, for `s` from `target` down to `num`: `dp[s] += dp[s - num]`.
6. Return `dp[target]`.

### Worked Example (Dry Run)
`nums = [1, 1, 2, 3]`, `diff = 1`. `total = 7`, `target = (7 + 1) / 2 = 4`.

```
dp (size 5):
start:      [1, 0, 0, 0, 0]
num=1:      [1, 1, 0, 0, 0]
num=1:      [1, 2, 1, 0, 0]
num=2:      [1, 2, 3, 2, 1]
num=3:      [1, 2, 3, 3, 3]
                                ↑ dp[4] = 3

Answer: 3
Verify: subsets summing to 4: {1,3}, {1,3} (other 1), {1,1,2} → 3 subsets.
  {1,3}: sum(A)=4, sum(B)=3, diff=1 ✓
  {1,1,2}: sum(A)=4, sum(B)=3, diff=1 ✓
```

### Code
```python
def count_subsets_with_diff(nums: list, diff: int) -> int:
    total = sum(nums)
    if (total + diff) % 2 != 0 or abs(diff) > total:
        return 0
    target = (total + diff) // 2
    dp = [0] * (target + 1)
    dp[0] = 1
    for num in nums:
        for s in range(target, num - 1, -1):
            dp[s] += dp[s - num]
    return dp[target]
```

### Complexity
- Time: O(n * target), where `target = (total + diff) / 2`.
- Space: O(target).

### Common Mistakes & Edge Cases
- **`diff > total`:** impossible (one subset would need more than all elements).
- **`diff = 0`:** count partitions into two equal-sum subsets.
- **Negative `diff`:** formula `|diff|` handles it symmetrically (swap A and B).
- **Parity check:** `(total + diff)` must be even for an integer target.
- **Zeros in `nums`:** each zero doubles the count (can go in either subset with no sum effect).

---

## 8. Minimum Cost to Buy N Items — Medium

**🔗 Practice Link:** [8. Minimum Cost to Buy N Items — Medium](https://www.geeksforgeeks.org/unbounded-knapsack-repetition-items-allowed)

### Problem Description
You want to buy `n` items. The cost of item `i` on day `d` is `costs[i][d]`. Each day you may
buy at most one item. You can also use a discount coupon on a day to halve the cost of the item
bought that day (rounded down). You have `k` coupons total. Return the minimum total cost to buy
all `n` items.

### State Definition
`dp[i][c]` = minimum cost to buy the first `i` items (sorted by some criterion) using `c`
coupons. Items are processed in order, and on each day we decide: buy the item with or without
a coupon.

### Recurrence Relation
```
Sort items by (max_cost - min_cost) descending (biggest coupon benefit first).
dp[i][c] = min(
    dp[i-1][c] + cost[i],                    # buy without coupon on the day of min cost
    dp[i-1][c-1] + cost[i] // 2   if c > 0   # buy with coupon
)
```
Where `cost[i]` is the minimum cost of item `i` across all days.

### Base Cases
- `dp[0][c] = 0` for all `c`: zero items cost zero.
- `dp[i][0] = dp[i-1][0] + cost[i]`: all items bought without coupons.

### Intuition (Why This Works)
For each item, we always buy it on the cheapest day. The coupon decision is the real choice:
use a coupon now or save it. Sorting by `(max_cost - min_cost)` ensures we use coupons on items
where they save the most. The DP tries every possible allocation of `k` coupons across `n` items.

### Step-by-Step Procedure
1. For each item, compute `min_cost[i] = min(costs[i])`.
2. Compute `savings[i] = max(costs[i]) - min_cost[i]` (coupon benefit).
3. Sort items by `savings` descending.
4. Initialize `dp = [0] * (k + 1)`.
5. For each item `i` (in sorted order):
   - For `c` from `k` down to `1`:
     - `dp[c] = min(dp[c], dp[c - 1] + min_cost[i] // 2)`  (use coupon).
   - `dp[0] += min_cost[i]`  (no coupon left).
6. Return `dp[k]`.

### Worked Example (Dry Run)
`costs = [[3,2,1],[1,2,3],[4,3,2]]`, `k = 1`. 3 items, each buyable on 3 days.

```
min_cost = [1, 1, 2]
savings  = [2, 2, 2]  (all same, order doesn't matter)

dp = [0, inf]  (k=1, indices 0 and 1)

Item 0 (min=1):
  dp[1] = min(inf, dp[0]+1//2) = min(inf, 0+0) = 0
  dp[0] += 1 → dp[0] = 1
  dp = [1, 0]

Item 1 (min=1):
  dp[1] = min(0, dp[0]+0) = min(0, 1) = 0
  dp[0] += 1 → dp[0] = 2
  dp = [2, 0]

Item 2 (min=2):
  dp[1] = min(0, dp[0]+2//2) = min(0, 2+1) = 0
  dp[0] += 2 → dp[0] = 4
  dp = [4, 0]

Answer: dp[1] = 0  → wait, that can't be right.

Let me recheck: min_cost[i]//2 for coupon. 
Item 0: min=1, coupon cost = 0.
Item 1: min=1, coupon cost = 0.
Item 2: min=2, coupon cost = 1.

dp = [0, 0]
Item 0: dp[1] = min(inf, 0+0)=0, dp[0]=1 → [1, 0]
Item 1: dp[1] = min(0, 1+0)=0, dp[0]=2 → [2, 0]
Item 2: dp[1] = min(0, 2+1)=0, dp[0]=4 → [4, 0]

Answer: 0. But buying 3 items with min costs [1,1,2] = 4 total without coupons.
With 1 coupon on any item, total = 4 - 1 = 3 (coupon halves 2→1 or 1→0).
Wait: dp[1] = 0 means 0 cost? That seems wrong.

Ah, the issue is dp[0] starts at 0 and accumulates min_cost without coupon.
dp[0] after item 0 = 0+1=1, after item 1 = 1+1=2, after item 2 = 2+2=4. ✓
dp[1] after item 0: min(inf, dp[0_before_item0]+0) = min(inf, 0+0) = 0. ✓
  This means: use 1 coupon on item 0 (cost 0), then buy items 1,2 without coupon (1+2=3).
  But dp[1] = 0 doesn't include the cost of items 1 and 2 yet.

The issue: dp[c] = min(dp[c], dp[c-1] + cost//2) only accounts for the CURRENT item.
The non-coupon items' costs are accumulated in dp[0] and implicitly in dp[c] for c>0.

Actually, let me re-examine: dp[c] after processing ALL items should be the total cost.
After item 2, dp[1] = 0. That means total cost = 0, which is wrong.

The bug: dp[c] for c>0 should also include the costs of items NOT getting coupons.
Let me fix: dp[c] represents the minimum cost to buy items processed so far using c coupons.
After item 0: dp[0]=1 (buy item 0 at cost 1), dp[1]=0 (buy item 0 with coupon, cost 0).
After item 1: dp[0]=2, dp[1]=min(0, dp[0]+0)=min(0,2)=0.
  dp[1]=0 means: used 1 coupon on item 0 (cost 0) + bought item 1 at cost 1? But dp says 0.

The problem is the recurrence doesn't carry the non-coupon cost when c>0.
Fix: the non-coupon path should update dp[c] too, not just dp[0].

Correct recurrence:
  For c from k down to 0:
    dp[c] += min_cost[i]  # everyone pays min_cost
  For c from k down to 1:
    dp[c] = min(dp[c], dp[c-1] + min_cost[i]//2)  # coupon saves min_cost//2

Wait, that double counts. Let me use the standard approach:

  new_dp[c] = dp[c] + min_cost[i]              # no coupon
  if c > 0: new_dp[c] = min(new_dp[c], dp[c-1] + min_cost[i]//2)  # coupon

This is clearer but uses O(k) space with a copy. For in-place:
  For c from k down to 1:
    dp[c] = min(dp[c] + min_cost[i], dp[c-1] + min_cost[i]//2)
  dp[0] += min_cost[i]
```

Let me redo with correct recurrence:
```
dp = [0, inf]  (k=1)
Item 0 (min=1):
  dp[1] = min(dp[1]+1, dp[0]+0) = min(inf+1, 0+0) = 0
  dp[0] += 1 → dp[0] = 1
  dp = [1, 0]

Item 1 (min=1):
  dp[1] = min(dp[1]+1, dp[0]+0) = min(0+1, 1+0) = 1
  dp[0] += 1 → dp[0] = 2
  dp = [2, 1]

Item 2 (min=2):
  dp[1] = min(dp[1]+2, dp[0]+1) = min(1+2, 2+1) = 3
  dp[0] += 2 → dp[0] = 4
  dp = [4, 3]

Answer: 3
Verify: 1 coupon on item 2: costs 1+1+1=3 ✓
```

### Code
```python
def minimum_cost(n: int, costs: list, k: int) -> int:
    min_cost = [min(c) for c in costs]
    savings = [max(c) - min(c) for c in costs]
    # Sort by savings descending (use coupons on items where they help most)
    order = sorted(range(n), key=lambda i: savings[i], reverse=True)
    dp = [0] + [float('inf')] * k
    for idx in order:
        mc = min_cost[idx]
        # Update dp[k..1] in-place (right-to-left to avoid overwriting)
        for c in range(k, 0, -1):
            dp[c] = min(dp[c] + mc, dp[c - 1] + mc // 2)
        dp[0] += mc
    return dp[k]
```

### Complexity
- Time: O(n log n) for sorting + O(n * k) for the DP.
- Space: O(n + k).

### Common Mistakes & Edge Cases
- **`k = 0`:** no coupons, answer is `sum(min_cost)`.
- **`k >= n`:** each item gets a coupon, answer is `sum(mc // 2)`.
- **Items with odd costs:** `mc // 2` rounds down, so coupon on a cost-1 item is free.
- **Zero-cost items:** coupon has no effect.
- **Sorting by savings:** crucial for optimal coupon allocation; without sorting you may waste
  coupons on cheap items.

---

## Summary Table

```
┌──────────────────────────────────────────────┬────────────┬──────────┬──────────┐
│ Problem                                      │ Type       │ Time     │ Space    │
├──────────────────────────────────────────────┼────────────┼──────────┼──────────┤
│ Bags of Tokens (LC #948)                     │ Greedy+DP  │ O(n logn)│ O(1)     │
│ Partition K Subsets (LC #698)                │ Bitmask DP │ O(n*2^n) │ O(2^n)   │
│ Job Scheduling (LC #1235)                    │ Interval   │ O(n logn)│ O(n)     │
│ Coin Piles Diff ≤ K (GFG)                    │ Sort+2ptr  │ O(n logn)│ O(1)     │
│ Subsequence Sum Target                       │ Subset Sum │ O(n*tgt) │ O(tgt)   │
│ Min Diff Partition (LC #2035)                │ Subset Sum │ O(n*tgt) │ O(tgt)   │
│ Count Subsets with Diff                      │ Count SS   │ O(n*tgt) │ O(tgt)   │
│ Min Cost Buy N Items                         │ DP+Greedy  │ O(n logn+│ O(n+k)   │
│                                              │            │  n*k)    │          │
└──────────────────────────────────────────────┴────────────┴──────────┴──────────┘
```
