# Misc Hard Problems — Part 1 (#286–310)

Continuation of miscellaneous DP problems. Skipped: #304 (Minimum Falling Path Sum, LC #931 — covered in `02_dp_2d/03_grid_dp.md`) and #309 (Minimum Insertions to Form a Palindrome, LC #1312 — covered in `05_string_dp/01_string_dp.md`).

---

## 1. Frog Jump (LC #403) — Hard

**🔗 Practice Link:** [1. Frog Jump](https://leetcode.com/problems/frog-jump/)

### Problem Description
A frog attempts to cross a river represented as the x-axis. There are stones at given positions. The frog starts on stone 0 and must reach the last stone. From stone at position `x`, it can jump to `x + k - 1`, `x + k`, or `x + k + 1` where `k` is the size of the previous jump. Determine if the frog can cross. For example, `stones = [0,1,3,5,6,7,8,12]` → True (path: 0→1→3→5→7→8→12).

### State Definition
`dp[i][k]` = True if the frog can reach stone `i` with a previous jump of size `k`. Use a hash map: `dp[pos] = set of valid previous jump sizes at this position`.

### Recurrence Relation
```
For each stone i at position stones[i]:
  For each k in dp[i]:
    For next_k in {k-1, k, k+1} where next_k > 0:
      If stones[i] + next_k exists as a stone:
        add next_k to dp[stones[i] + next_k]
```
Plain English: from each reachable stone, try all three legal jump sizes and propagate reachability to the next stone.

### Base Cases
- `dp[0] = {0}` (starting stone, "virtual" jump of 0).
- Frog starts at position 0 with jump size 0.

### Intuition (Why This Works)
The jump-size set at each stone captures all ways to reach it. Since the frog can only arrive with specific jump sizes, we propagate only valid transitions. A hash map gives O(1) stone lookup, and the set at each stone prunes unreachable states.

### Step-by-Step Procedure
1. Build `stone_set = set(stones)` and `dp = defaultdict(set)`.
2. `dp[0] = {0}`.
3. For each `stone` in `stones`:
   a. For each `k` in `dp[stone]`:
      - For `next_k` in `{k-1, k, k+1}` (if `next_k > 0`):
        - If `stone + next_k` in `stone_set`: `dp[stone + next_k].add(next_k)`.
4. Return `len(dp[stones[-1]]) > 0`.

### Worked Example (Dry Run)
`stones = [0,1,3,5,6,7,8,12]`.

- `dp[0] = {0}`
- Stone 0: k=0 → next_k=1: stone 1 exists → `dp[1].add(1)`
- Stone 1: k=1 → next_k=0 (skip), 1: stone 2 doesn't exist, 2: stone 3 exists → `dp[3].add(2)`
- Stone 3: k=2 → next_k=1: stone 4 no, 2: stone 5 yes → `dp[5].add(2)`, next_k=3: stone 6 yes → `dp[6].add(3)`
- Stone 5: k=2 → next_k=1: 6 yes → `dp[6].add(1)`, 2: 7 yes → `dp[7].add(2)`, 3: 8 yes → `dp[8].add(3)`
- Stone 6: k=3 → 4: 10 no; k=1 → 2: 8 yes → `dp[8].add(2)`
- Stone 7: k=2 → 3: 10 no
- Stone 8: k=3 → 4: 12 yes → `dp[12].add(4)`; k=2 → 3: 11 no, 4: 12 yes → `dp[12].add(4)`
- `dp[12] = {4}` → non-empty → **True**.

### Code
```python
from collections import defaultdict

class Solution:
    def canCross(self, stones: list) -> bool:
        stone_set = set(stones)
        dp = defaultdict(set)
        dp[0] = {0}
        for stone in stones:
            for k in dp[stone]:
                for next_k in (k - 1, k, k + 1):
                    if next_k > 0 and stone + next_k in stone_set:
                        dp[stone + next_k].add(next_k)
        return len(dp[stones[-1]]) > 0
```

### Complexity
- Time: O(n²) — each stone's jump set has at most O(n) sizes.
- Space: O(n²) in worst case for the hash map.

### Common Mistakes & Edge Cases
- `stones[1] != 1`: frog can't make the first jump → False.
- `stones = [0,1]`: jump from 0 to 1 with k=1 → True.
- Jump size must be positive (`next_k > 0`).
- The frog cannot jump backward; only forward jumps to larger positions.

---

## 2. Minimum Cost to Make Array Equal (LC #2448) — Hard

**🔗 Practice Link:** [2. Minimum Cost to Make Array Equal](https://leetcode.com/problems/minimum-cost-to-make-array-equal/)

### Problem Description
Given arrays `nums` and `cost`, make all elements of `nums` equal. In one operation, you can increment or decrement any element by 1 at a cost equal to `cost[i]`. Find the minimum total cost. For example, `nums = [1,3,5]`, `cost = [1,1,1]` → target 3, cost = |1-3| + |3-3| + |5-3| = 4.

### State Definition
The optimal target is a **weighted median** of `nums` with weights `cost`. No DP table needed — this is a mathematical optimization.

### Recurrence Relation
```
total_cost(target) = sum of cost[i] * |nums[i] - target| for all i
```
The minimum occurs at the weighted median: sort by `nums`, then find where cumulative cost reaches half the total.

### Base Cases
- All `nums` equal → cost is 0.
- Single element → cost is 0.

### Intuition (Why This Works)
The cost function is piecewise linear and convex. Moving the target one unit right increases cost by `sum of costs to the left` and decreases by `sum of costs to the right`. The minimum is at the point where these balance — the weighted median.

### Step-by-Step Procedure
1. Pair `nums[i]` with `cost[i]` and sort by `nums`.
2. Compute `total_cost = sum(cost)`.
3. Find the weighted median: accumulate costs until reaching `total_cost / 2`.
4. The element at that position is the optimal target.
5. Compute the total cost for that target.

### Worked Example (Dry Run)
`nums = [1,3,5]`, `cost = [1,1,1]`. Already sorted. `total_cost = 3`, half = 1.5.
- Cumulative: 1 (at 1), 2 (at 3 ≥ 1.5) → target = 3.
- Cost = 1×|1-3| + 1×|3-3| + 1×|5-3| = 2+0+2 = **4**.

### Code
```python
class Solution:
    def minCost(self, nums: list, cost: list) -> int:
        pairs = sorted(zip(nums, cost))
        total = sum(cost)
        acc = 0
        target = 0
        for num, c in pairs:
            acc += c
            if acc >= (total + 1) // 2:
                target = num
                break
        return sum(c * abs(num - target) for num, c in pairs)
```

### Complexity
- Time: O(n log n) for sorting
- Space: O(n)

### Common Mistakes & Edge Cases
- For large numbers: use `int` (Python handles big integers natively).
- Even total cost: any target between the two middle values gives the same minimum.
- All costs equal: target is the regular median.
- All `nums` the same: cost is 0 regardless of costs.

---

## 3. Maximum Earnings from Taxi (LC #2002) — Medium

**🔗 Practice Link:** [3. Maximum Earnings from Taxi](https://leetcode.com/problems/maximum-earnings-from-taxi/)

### Problem Description
A taxi driver picks up passengers. There are `n` stops (1 to n). Each ride `(start, end, tip)` means picking up at `start`, dropping at `end`, earning `end - start + tip`. Rides don't overlap. Maximize total earnings. For example, `rides = [[2,5,4],[1,5,1]]` → ride [2,5,4] earns 7, ride [1,5,1] earns 5; pick the first (better).

### State Definition
`dp[i]` = maximum earnings considering stops up to `i`. Answer is `dp[n]`.

### Recurrence Relation
```
dp[i] = max(dp[i-1], dp[start] + end - start + tip)  for each ride ending at i
```
Plain English: at each stop, either skip (carry forward) or take a ride that ends here.

### Base Cases
- `dp[0] = 0` (no stops, no earnings).

### Intuition (Why This Works)
Sort rides by end stop. For each ride ending at `end`, the best earnings is the best dp at `start` plus the ride's profit. Binary search for the last ride ending before `start` to find `dp[start]`.

### Step-by-Step Procedure
1. Group rides by their end stop.
2. `dp[0] = 0`.
3. For `i` from 1 to `n`:
   a. `dp[i] = dp[i-1]` (skip stop i).
   b. For each ride `(start, end, tip)` ending at `i`:
      - `dp[i] = max(dp[i], dp[start] + end - start + tip)`.
4. Return `dp[n]`.

### Worked Example (Dry Run)
`n = 5`, `rides = [[2,5,4],[1,5,1]]`. Both end at 5.

- `dp[0..5] = [0, 0, 0, 0, 0, 0]`
- `dp[1] = dp[0] = 0` (no ride ends at 1)
- `dp[2] = dp[1] = 0` (no ride ends at 2)
- `dp[3] = dp[2] = 0`
- `dp[4] = dp[3] = 0`
- `dp[5]`: skip → dp[4]=0; ride (2,5,4): dp[2]+5-2+4=0+7=7; ride (1,5,1): dp[1]+5-1+1=0+5=5 → `dp[5] = 7`

Answer: **7**.

### Code
```python
class Solution:
    def taxEarnings(self, n: int, rides: list) -> int:
        from collections import defaultdict
        ride_map = defaultdict(list)
        for start, end, tip in rides:
            ride_map[end].append((start, end, tip))
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i - 1]
            for start, end, tip in ride_map[i]:
                dp[i] = max(dp[i], dp[start] + end - start + tip)
        return dp[n]
```

### Complexity
- Time: O(n + r) where r = number of rides
- Space: O(n + r)

### Common Mistakes & Edge Cases
- `start` can be 0: `dp[0] = 0` handles it.
- No rides: earnings = 0.
- Overlapping rides: the DP ensures only non-overlapping ones are selected (dp[start] uses the best before `start`).
- Multiple rides ending at the same stop: try all of them.

---

## 4. Minimum Number of Operations to Make Array Continuous (LC #2009) — Hard

**🔗 Practice Link:** [4. Minimum Number of Operations to Make Array Continuous](https://leetcode.com/problems/minimum-number-of-operations-to-make-array-continuous/)

### Problem Description
You are given an integer array `nums`. In one operation, you can replace any element with any integer. An array is **continuous** if all elements are distinct and `max(nums) - min(nums) == len(nums) - 1`. Find the minimum operations to make `nums` continuous. For example, `nums = [4,2,5,3]` → already continuous (2,3,4,5 → max-min=3=n-1), answer = 0.

### State Definition
Sort unique elements. Use two pointers: for each left pointer `i`, find the rightmost `j` where `nums[j] - nums[i] <= n - 1`. The elements within this window need no changes; the rest need replacement.

### Recurrence Relation
```
operations = n - (number of elements in the largest window where nums[j] - nums[i] <= n-1)
```
Minimize operations by maximizing the window size.

### Base Cases
- Already continuous → 0 operations.
- All elements same → n - 1 operations (keep one, replace rest).

### Intuition (Why This Works)
After sorting, the best continuous array must use existing elements as much as possible. The constraint `max - min == n - 1` means the valid window spans exactly `n - 1` in value range. Finding the largest subarray fitting this range minimizes replacements.

### Step-by-Step Procedure
1. Sort `nums` and remove duplicates (or sort and use two pointers with dedup).
2. Use two pointers `i` and `j` on the sorted unique array.
3. For each `i`, advance `j` while `unique[j] - unique[i] <= n - 1`.
4. Max window size = `j - i`. Answer = `n - max_window`.
5. Handle duplicates: subtract duplicate count from the answer (duplicates must be replaced regardless).

### Worked Example (Dry Run)
`nums = [4,2,5,3]`. Sorted unique: `[2,3,4,5]`, `n = 4`.

- i=0: j goes to 3 (5-2=3 ≤ 3). Window = 4.
- Max window = 4. Answer = 4 - 4 = **0**.

Another: `nums = [1,2,3,5,6]`, `n = 5`. Sorted unique: `[1,2,3,5,6]`.
- i=0: j=2 (3-1=2≤4), j=3 (5-1=4≤4), j=4 (6-1=5>4) → window = 4.
- i=1: j=4 (6-2=4≤4) → window = 4.
- i=2: j=4 (6-3=3≤4) → window = 3.
- Max = 4. Answer = 5 - 4 = **1**.

### Code
```python
class Solution:
    def minOperations(self, nums: list) -> int:
        n = len(nums)
        unique = sorted(set(nums))
        m = len(unique)
        max_keep = 0
        j = 0
        for i in range(m):
            while j < m and unique[j] - unique[i] <= n - 1:
                j += 1
            max_keep = max(max_keep, j - i)
        return n - max_keep
```

### Complexity
- Time: O(n log n) for sorting
- Space: O(n)

### Common Mistakes & Edge Cases
- Duplicates: must be replaced even if within range (use `set` first).
- All elements identical: answer = n - 1 (only one can stay).
- Single element: always continuous, answer = 0.
- Two pointers must use `j` that only moves forward (not reset for each `i`).

---

## 5. Number of Increasing Subsequences in an Array — Medium

**🔗 Practice Link:** [5. Number of Increasing Subsequences in an Array — Medium](https://www.geeksforgeeks.org/count-all-increasing-subsequences)

### Problem Description
Count the number of strictly increasing subsequences in an array. For example, `nums = [2, 1, 3]` → subsequences: [2], [1], [3], [2,3], [1,3] → answer = 5 (excluding empty).

### State Definition
`dp[i]` = number of increasing subsequences ending at index `i` (including the subsequence of length 1 containing just `nums[i]`).

### Recurrence Relation
```
dp[i] = 1 + sum(dp[j] for j < i if nums[j] < nums[i])
```
Plain English: each subsequence ending at `i` is either `[nums[i]]` alone (count 1) or an increasing subsequence ending at some smaller `nums[j]` extended by `nums[i]`.

### Base Cases
- `dp[i] = 1` for all `i` (the subsequence containing just `nums[i]`).

### Intuition (Why This Works)
This is a variant of LIS counting. Each position contributes all subsequences from earlier smaller elements, plus itself. The answer is `sum(dp)`.

### Step-by-Step Procedure
1. Initialize `dp = [1] * n`.
2. For each `i` from 1 to n-1:
   For each `j` from 0 to i-1:
     If `nums[j] < nums[i]`: `dp[i] += dp[j]`.
3. Return `sum(dp)`.

### Worked Example (Dry Run)
`nums = [2, 1, 3]`.

- dp = [1, 1, 1]
- i=1: j=0, 2 < 1? No → dp = [1, 1, 1]
- i=2: j=0, 2 < 3? Yes → dp[2] += 1 = 2; j=1, 1 < 3? Yes → dp[2] += 1 = 3
- dp = [1, 1, 3]. Answer = 1+1+3 = **5**.

### Code
```python
class Solution:
    def countSubsequences(self, nums: list) -> int:
        n = len(nums)
        dp = [1] * n
        for i in range(1, n):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] += dp[j]
        return sum(dp)
```

### Complexity
- Time: O(n²)
- Space: O(n)

### Common Mistakes & Edge Cases
- Include single-element subsequences (the `+1` in the recurrence).
- `n = 0` → 0, `n = 1` → 1.
- Strictly increasing: use `<`, not `<=`.
- The count can grow exponentially; use modulo if specified.

---

## 6. Minimum Moves to Make Array Complementary (LC #1674) — Medium

**🔗 Practice Link:** [6. Minimum Moves to Make Array Complementary](https://leetcode.com/problems/minimum-moves-to-make-array-complementary/)

### Problem Description
Given an array `nums` of even length `n` and a limit. A move increments or decrements any element by 1. An array is complementary if for every pair `(nums[i], nums[n-1-i])`, their sum equals `limit`. Find the minimum moves. For example, `nums = [1,2,4,3]`, `limit = 5` → pairs (1,4) sum 5, (2,3) sum 5 → 0 moves.

### State Definition
Use a **difference array** (sweep line) to track cost changes. For each pair `(a, b)`:
- Cost 0 at sum = a + b.
- Cost 1 at sums between min(a,b)+1 and max(a,b)+limit-1.
- Cost 2 at sums outside that range.

### Recurrence Relation
```
For each pair (a, b), with s = a + b:
  diff[s] -= 1        (cost drops by 1 at the optimal sum)
  diff[min(a,b)+1] += 1
  diff[max(a,b)+limit] += 1
  baseline += 2        (each pair starts with cost 2)
```
Plain English: sweep line tracks how the total cost changes as the target sum varies. The minimum cost = baseline + minimum prefix sum of diff.

### Base Cases
- `baseline = 2 * (n/2)` (every pair costs 2 moves before optimization).

### Intuition (Why This Works)
For a pair `(a, b)`, the cost to make `a + b == target` is: 0 if target = a+b, 1 if target is within range `[min+1, max+limit-1]` (adjust one element), 2 otherwise (adjust both). The difference array efficiently captures these cost transitions across all target sums.

### Step-by-Step Procedure
1. `baseline = n` (2 moves per pair, n/2 pairs).
2. Initialize `diff = [0] * (2 * limit + 2)`.
3. For each pair `(a, b)`:
   a. `s = a + b`.
   b. `diff[s] -= 1`.
   c. `diff[min(a,b)+1] += 1`.
   d. `diff[max(a,b)+limit+1] += 1`.
4. Compute running prefix sum over `diff`, find minimum.
5. Answer = `baseline + min_prefix`.

### Worked Example (Dry Run)
`nums = [1,2,4,3]`, `limit = 5`. Pairs: (1,4) and (2,3).

Baseline = 4. For (1,4): s=5, diff[5]-=1, diff[2]+=1, diff[10]+=1. For (2,3): s=5, diff[5]-=1, diff[3]+=1, diff[9]+=1.

diff[2]=1, diff[3]=1, diff[5]=-2, diff[9]=1, diff[10]=1.
Prefix: ..., at target=5: -2. Answer = 4 + (-2) = **2**... but the answer should be 0.

Let me recalculate: baseline should be 2 per pair = 4. diff[5] = -2 means at target 5, cost = 4-2 = 2. But we said 0 moves. The issue is the baseline. Each pair costs at most 2. With two pairs both at sum 5, the cost is 0+0 = 0. The correct baseline for each pair is 2, but if the pair already sums to target, it costs 0 (saving 2). So diff[s] -= 2 for the saving. Let me fix the approach.

For each pair (a,b), s=a+b, lo=min(a,b), hi=max(a,b):
- diff[s] -= 2 (save 2 at exact sum)
- diff[lo+1] += 1 (start paying 1 instead of 0 for sums > s but within one-element range)
- diff[hi+limit+1] += 1 (start paying 2 for sums outside one-element range)

Baseline = 2 * (n/2) = 4. At target 5: 4 + (-2) = 2... still not 0. Let me re-examine. Actually the correct approach: baseline = 0. For each pair, cost at target t is:
- 0 if t = a+b
- 1 if t in [lo+1, hi-1] or t = lo+limit or t = hi+limit... no, let me reconsider.

Cost of pair (a,b) for target t: min(|t-a-b+a-a|, ...) — it's |t-a-b| only when both move. Actually the cost for pair (a,b) to reach sum t:
- If t = a+b: 0
- If t is in [lo+1, hi+limit-1] where lo=min(a,b), hi=max(a,b): cost 1 (move one element)
- Otherwise: cost 2

So for (1,4), lo=1, hi=4: cost 0 at t=5, cost 1 for t in [2, 8], cost 2 otherwise.
For (2,3), lo=2, hi=3: cost 0 at t=5, cost 1 for t in [3, 6], cost 2 otherwise.

Total at t=5: 0+0=0. Correct!

### Code
```python
class Solution:
    def minMoves(self, nums: list, limit: int) -> int:
        n = len(nums)
        diff = [0] * (2 * limit + 2)
        baseline = 0
        for i in range(n // 2):
            a, b = nums[i], nums[n - 1 - i]
            lo, hi = min(a, b), max(a, b)
            s = a + b
            # cost 2 by default; save at specific ranges
            diff[2] += 1
            diff[s] -= 1
            diff[s + 1] += 1
            diff[lo + 1] += 1
            diff[hi + limit + 1] -= 1
        # Simplified: use the standard difference approach
        diff2 = [0] * (2 * limit + 2)
        for i in range(n // 2):
            a, b = nums[i], nums[n - 1 - i]
            lo, hi = min(a, b), max(a, b)
            s = a + b
            diff2[s] += 0  # cost 0
            diff2[lo + 1] += 1
            diff2[hi + limit + 1] -= 1
            diff2[hi + 1] -= 1
            diff2[lo + 1] += 1  # re-enter cost 2 zone
            diff2[2] += 2
        # The cleaner approach:
        events = [0] * (2 * limit + 2)
        base = 0
        for i in range(n // 2):
            a, b = nums[i], nums[n - 1 - i]
            lo, hi = min(a, b), max(a, b)
            s = a + b
            base += 2
            events[s] -= 2
            events[lo + 1] += 1
            events[hi + limit + 1] -= 1
            events[hi + 1] += 1
            events[lo + limit + 1] -= 1
        # Actually use the well-known O(n) sweep approach:
        sweep = [0] * (2 * limit + 2)
        base = 0
        for i in range(n // 2):
            a, b = nums[i], nums[n - 1 - i]
            lo, hi = min(a, b), max(a, b)
            s = a + b
            base += 2
            sweep[s] -= 2
            sweep[lo + 1] += 1
            sweep[hi + limit] += 1
        cur = base
        ans = base
        for v in sweep:
            cur += v
            ans = min(ans, cur)
        return ans
```

### Complexity
- Time: O(n + limit)
- Space: O(limit)

### Common Mistakes & Edge Cases
- `n = 2`: single pair, answer is 0, 1, or 2 depending on the sum.
- `limit` bounds the range of valid sums (2 to 2×limit).
- The sweep array size must accommodate sum up to 2×limit.
- Correct difference array updates are tricky; verify with small examples.

---

## 7. Maximum Profit from Selling Candies — Medium

**🔗 Practice Link:** [7. Maximum Profit from Selling Candies — Medium](https://www.geeksforgeeks.org/maximize-the-profit-by-selling-at-most-m-products)

### Problem Description
You have `n` candies and `m` customers. Customer `i` buys `buy[i]` candies at `price[i]` per candy, but only if they get exactly `buy[i]` candies. You can sell at most once to each customer. Maximize revenue. For example, `buy = [3,2]`, `price = [5,4]` → sell 2 to customer 2 (revenue 8) or 3 to customer 1 (revenue 15). Answer = 15.

### State Definition
Sort by `price` descending. For each customer, sell as many as possible (capped by remaining candies).

### Recurrence Relation
Greedy: sell to the highest-paying customer first.

### Base Cases
- `n = 0` → 0 revenue.
- No customers → 0 revenue.

### Intuition (Why This Works)
Always sell to the customer offering the highest price first. Sort by price descending, then greedily allocate candies. This is optimal because giving candies to a higher-paying customer always dominates a lower-paying one.

### Step-by-Step Procedure
1. Pair `(price[i], buy[i])` and sort by price descending.
2. `revenue = 0`, `remaining = n`.
3. For each `(price, need)`:
   a. `sold = min(need, remaining)`.
   b. `revenue += sold * price`.
   c. `remaining -= sold`.
   d. If `remaining == 0`: break.
4. Return `revenue`.

### Worked Example (Dry Run)
`n = 5`, `buy = [3,2,4]`, `price = [5,4,6]`. Sorted by price: [(6,4),(5,3),(2,2)].

- (6,4): sold = min(4,5) = 4, revenue = 24, remaining = 1
- (5,3): sold = min(3,1) = 1, revenue = 29, remaining = 0
- Answer: **29**.

### Code
```python
class Solution:
    def maxProfit(self, n: int, buy: list, price: list) -> int:
        customers = sorted(zip(price, buy), reverse=True)
        revenue = 0
        remaining = n
        for p, need in customers:
            sold = min(need, remaining)
            revenue += sold * p
            remaining -= sold
            if remaining == 0:
                break
        return revenue
```

### Complexity
- Time: O(m log m) for sorting (m = customers)
- Space: O(m)

### Common Mistakes & Edge Cases
- Must sort by price descending, not by need.
- `n` can be less than total demand: sell only what you have.
- Price ties: any order works.
- Negative prices: not expected in this problem.

---

## 8. Count Arrays with Bounded Difference — Medium

**🔗 Practice Link:** [8. Count Arrays with Bounded Difference — Medium](https://www.geeksforgeeks.org/count-of-arrays-of-size-n-having-absolute-difference-between-adjacent-elements-at-most-1)

### Problem Description
Given `n`, `lower`, `upper`, and `diff`, count arrays of length `n` where each element is in `[lower, upper]` and for all adjacent elements, `|arr[i] - arr[i+1]| <= diff`. For example, `n = 3, lower = 1, upper = 3, diff = 1` → arrays like [1,1,1], [1,2,1], etc.

### State Definition
`dp[i][v]` = number of valid arrays of length `i+1` ending with value `v`. Since `v` ranges from `lower` to `upper`, use the offset `v - lower` as the index.

### Recurrence Relation
```
dp[i][v] = sum(dp[i-1][v'] for all v' in [v-diff, v+diff] ∩ [lower, upper])
```
Plain English: extend any valid array ending at `v'` by appending `v` if the difference constraint holds.

### Base Cases
- `dp[0][v] = 1` for all `v` in `[lower, upper]` (single-element arrays).

### Intuition (Why This Works)
This is a bounded transition DP. For each position, each value's count is the sum of counts from the previous position within the allowed range. Using prefix sums on the previous row makes each transition O(1) instead of O(diff).

### Step-by-Step Procedure
1. `size = upper - lower + 1`.
2. `prev = [1] * size`.
3. For `i` from 1 to n-1:
   a. Compute prefix sum of `prev`.
   b. For each `v` from 0 to size-1:
      - `lo = max(0, v - diff)`, `hi = min(size-1, v + diff)`.
      - `curr[v] = prefix[hi+1] - prefix[lo]`.
   c. `prev = curr`.
4. Return `sum(prev) % (10^9 + 7)`.

### Worked Example (Dry Run)
`n = 3, lower = 1, upper = 3, diff = 1`. Values: 1, 2, 3. size = 3.

- `prev = [1, 1, 1]`
- i=1: prefix = [0,1,2,3]
  - v=0 (val 1): lo=0, hi=1 → 1+1=2
  - v=1 (val 2): lo=0, hi=2 → 1+1+1=3
  - v=2 (val 3): lo=1, hi=2 → 1+1=2
  - `curr = [2, 3, 2]`
- i=2: prefix = [0,2,5,7]
  - v=0: lo=0, hi=1 → 2+3=5
  - v=1: lo=0, hi=2 → 2+3+2=7
  - v=2: lo=1, hi=2 → 3+2=5
  - `curr = [5, 7, 5]`
- Answer = 5+7+5 = **17**.

### Code
```python
class Solution:
    def countArrays(self, n: int, lower: int, upper: int, diff: int) -> int:
        MOD = 10**9 + 7
        size = upper - lower + 1
        prev = [1] * size
        for _ in range(n - 1):
            prefix = [0] * (size + 1)
            for j in range(size):
                prefix[j + 1] = (prefix[j] + prev[j]) % MOD
            curr = [0] * size
            for j in range(size):
                lo = max(0, j - diff)
                hi = min(size - 1, j + diff)
                curr[j] = (prefix[hi + 1] - prefix[lo]) % MOD
            prev = curr
        return sum(prev) % MOD
```

### Complexity
- Time: O(n × size)
- Space: O(size)

### Common Mistakes & Edge Cases
- `diff >= size - 1`: every transition is allowed; answer = `size^n`.
- `n = 1`: answer = `upper - lower + 1`.
- `size = 1`: answer = 1 (only one value possible).
- Modulo: handle negative prefix sums with `(x % MOD + MOD) % MOD`.

---

## 9. Minimum Cost to Connect Sticks (LC #1167) — Medium

**🔗 Practice Link:** [9. Minimum Cost to Connect Sticks](https://www.geeksforgeeks.org/connect-n-ropes-minimum-cost)

### Problem Description
You have `sticks` where `sticks[i]` is the length of the `i`-th stick. Connect all sticks into one. The cost of connecting two sticks equals their combined length. Find the minimum total cost. For example, `sticks = [2,4,3]` → connect 2+3=5 (cost 5), then 5+4=9 (cost 9), total = 14.

### State Definition
No DP table — this is a **greedy** problem using a min-heap. Always connect the two shortest sticks.

### Recurrence Relation
```
while heap has more than 1 element:
    a = heappop, b = heappop
    cost += a + b
    heappush(a + b)
```

### Base Cases
- `len(sticks) <= 1` → cost = 0 (already one stick).
- Two sticks `[a, b]` → cost = a + b.

### Intuition (Why This Works)
Connecting the two shortest sticks first minimizes the number of times long sticks are added to the cost. This is a Huffman-coding-like greedy: short sticks should be summed early so they contribute less to later, larger sums.

### Step-by-Step Procedure
1. If `len(sticks) <= 1`, return 0.
2. Build a min-heap from `sticks`.
3. `cost = 0`.
4. While heap has more than 1 element:
   a. `a = heappop`, `b = heappop`.
   b. `cost += a + b`.
   c. `heappush(a + b)`.
5. Return `cost`.

### Worked Example (Dry Run)
`sticks = [2, 4, 3]`. Heap: [2, 3, 4].

- Pop 2, 3 → cost = 5, push 5 → heap: [4, 5]
- Pop 4, 5 → cost = 14, push 9 → heap: [9]
- Answer: **14**.

### Code
```python
import heapq

class Solution:
    def connectSticks(self, sticks: list) -> int:
        if len(sticks) <= 1:
            return 0
        heapq.heapify(sticks)
        cost = 0
        while len(sticks) > 1:
            a = heapq.heappop(sticks)
            b = heapq.heappop(sticks)
            cost += a + b
            heapq.heappush(sticks, a + b)
        return cost
```

### Complexity
- Time: O(n log n)
- Space: O(n)

### Common Mistakes & Edge Cases
- Single stick → 0 cost.
- Two sticks → sum of both.
- Large sticks: cost can overflow in fixed-width languages (fine in Python).
- Not a DP problem despite being in this category — pure greedy with heap.

---

## 10. Ways to Split Array into Three Subarrays (LC #1712) — Medium

**🔗 Practice Link:** [10. Ways to Split Array into Three Subarrays](https://leetcode.com/problems/ways-to-split-array-into-three-subarrays/)

### Problem Description
Count the number of ways to split `nums` into three non-empty contiguous subarrays `left`, `middle`, `right` such that `sum(left) <= sum(middle) <= sum(right)`. Return the count modulo 10^9+7. For example, `nums = [1,1,1]` → 1 way: [1], [1], [1].

### State Definition
`prefix[i]` = sum of `nums[0..i-1]`. Use prefix sums to express subarray sums. For each possible split `(i, j)` where `left = nums[0..i-1]`, `middle = nums[i..j-1]`, `right = nums[j..n-1]`.

### Recurrence Relation
```
For each i (left end):
  Find valid range of j (middle end) where:
    sum(left) <= sum(middle) and sum(middle) <= sum(right)
  Count valid j's using binary search.
```

### Base Cases
- `n < 3` → 0 ways (need 3 non-empty parts).

### Intuition (Why This Works)
Fix the first split point `i`. The constraints on `j` form a range: `j` must be large enough that `sum(middle) >= sum(left)` and small enough that `sum(middle) <= sum(right)`. Binary search for the bounds of this range.

### Step-by-Step Procedure
1. Compute `prefix` array.
2. `total = prefix[n]`, `count = 0`.
3. For `i` from 1 to n-2 (left has at least 1 element, right has at least 1):
   a. `left_sum = prefix[i]`.
   b. Binary search for `j_lo` (smallest j where `sum(middle) >= left_sum`).
   c. Binary search for `j_hi` (largest j where `sum(middle) <= sum(right)`).
   d. `count += max(0, j_hi - j_lo + 1)`.
4. Return `count % MOD`.

### Worked Example (Dry Run)
`nums = [1,1,1,1,1]`. prefix = [0,1,2,3,4,5]. total = 5. left_sum target = anything ≤ 5/3 ≈ 1.67.

- i=1: left_sum=1. mid_sum = prefix[j]-1. Need mid >= 1 and mid <= 5-mid → mid <= 2.5 → mid in [1,2]. j in [2,3]. Count = 2.
- i=2: left_sum=2. Need mid >= 2 and mid <= 5-2-mid → mid <= 1.5. No valid j. Count += 0.
- i=3: left_sum=3. mid >= 3 and mid <= 5-3-mid → mid <= 1. No valid.
- Answer: **2**. (Splits: [1],[1,1],[1,1] and [1],[1],[1,1,1]... let me verify.)

Actually for i=1: j=2 gives middle=[1], right=[1,1], sums 1,1,2 → 1<=1<=2 ✓. j=3 gives middle=[1,1], right=[1], sums 1,2,1 → 2<=1 ✗. So only j=2 works. Let me redo.

For i=1: left_sum=1, total=5. j=2: mid=1, right=3 → 1<=1<=3 ✓. j=3: mid=2, right=2 → 1<=2<=2 ✓. j=4: mid=3, right=1 → 1<=3 but 3<=1 ✗. Count = 2.
For i=2: left_sum=2, j=3: mid=1, right=2 → 2<=1 ✗. No valid.
Answer: **2**. ✓

### Code
```python
import bisect

class Solution:
    def waysToSplit(self, nums: list) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]
        total = prefix[n]
        count = 0
        for i in range(1, n - 1):
            left_sum = prefix[i]
            # mid_sum = prefix[j] - prefix[i], right_sum = total - prefix[j]
            # mid >= left and mid <= right → mid >= left and 2*mid <= total - left
            # prefix[j] - prefix[i] >= left_sum → prefix[j] >= 2*left_sum
            # prefix[j] - prefix[i] <= total - prefix[j] → 2*prefix[j] <= total + prefix[i]
            lo = max(i + 1, bisect.bisect_left(prefix, 2 * left_sum, i + 1, n))
            hi = min(n - 1, bisect.bisect_right(prefix, (total + prefix[i]) // 2, i + 1, n) - 1)
            if lo <= hi:
                count = (count + hi - lo + 1) % MOD
        return count
```

### Complexity
- Time: O(n log n) — binary search per index.
- Space: O(n) for prefix sums.

### Common Mistakes & Edge Cases
- Integer division: `(total + prefix[i]) // 2` floors correctly for the upper bound.
- `n < 3` → return 0.
- All zeros: every valid split counts (answer = C(n-1, 2) roughly).
- Overflow with large sums: Python handles big ints.

---

## 11. Minimum Cost to Reduce Array to Single Element — Medium

**🔗 Practice Link:** [11. Minimum Cost to Reduce Array to Single Element — Medium](https://www.geeksforgeeks.org/minimum-cost-to-merge-stones)

### Problem Description
Given an array, in one operation you can merge two adjacent elements at a cost equal to their sum. Find the minimum total cost to reduce the array to a single element. For example, `arr = [1, 2, 3]` → merge 1+2=3 (cost 3), then 3+3=6 (cost 6), total = 9. Or merge 2+3=5 (cost 5), then 1+5=6 (cost 6), total = 11. Answer = 9.

### State Definition
`dp[i][j]` = minimum cost to merge `arr[i..j]` into a single element.

### Recurrence Relation
```
dp[i][j] = min over k in [i, j-1] of (dp[i][k] + dp[k+1][j] + sum(arr[i..j]))
```
Plain English: split the range into two halves, merge each optimally, then merge the two results.

### Base Cases
- `dp[i][i] = 0` (single element, no merge needed).

### Intuition (Why This Works)
This is identical to the Matrix Chain Multiplication / Optimal Merge pattern. Every merge sequence has a last merge that splits the range, and the cost of that last merge is the total sum of the range. Optimal substructure and overlapping subproblems give O(n³) tabulation.

### Step-by-Step Procedure
1. Compute `prefix` sums for range sum queries.
2. `dp[i][i] = 0` for all `i`.
3. For `length` from 2 to n:
   a. For `i` from 0 to n-length:
      - `j = i + length - 1`.
      - `dp[i][j] = inf`.
      - For `k` from i to j-1:
        - `dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j] + prefix[j+1] - prefix[i])`.
4. Return `dp[0][n-1]`.

### Worked Example (Dry Run)
`arr = [1, 2, 3]`. prefix = [0, 1, 3, 6].

- dp[0][0] = dp[1][1] = dp[2][2] = 0
- dp[0][1]: k=0 → 0+0+3=3. dp[0][1] = 3.
- dp[1][2]: k=1 → 0+0+5=5. dp[1][2] = 5.
- dp[0][2]: k=0 → 0+5+6=11; k=1 → 3+0+6=9 → dp[0][2] = **9**.

### Code
```python
class Solution:
    def minCost(self, arr: list) -> int:
        n = len(arr)
        if n <= 1:
            return 0
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + arr[i]
        inf = float('inf')
        dp = [[0] * n for _ in range(n)]
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = inf
                total = prefix[j + 1] - prefix[i]
                for k in range(i, j):
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + total)
        return dp[0][n - 1]
```

### Complexity
- Time: O(n³)
- Space: O(n²)

### Common Mistakes & Edge Cases
- `n = 1` → 0 (nothing to merge).
- `n = 2` → sum of both elements.
- The merge cost is the **total sum** of the range, not the sum of just the two sub-roots.
- Prefix sums avoid recomputing range sums inside the inner loop.

---

## 12. Longest Arithmetic Subsequence (LC #1027) — Medium

**🔗 Practice Link:** [12. Longest Arithmetic Subsequence](https://leetcode.com/problems/longest-arithmetic-subsequence/)

### Problem Description
Given an array, find the length of the longest arithmetic subsequence. A subsequence is arithmetic if the difference between consecutive elements is constant. For example, `nums = [3,6,9,12]` → answer = 4 (the whole array). `nums = [9,4,7,2,10]` → answer = 3 (subsequence [4,7,10]).

### State Definition
`dp[i][d]` = length of the longest arithmetic subsequence ending at index `i` with common difference `d`. Use a dictionary at each index for sparse differences.

### Recurrence Relation
```
dp[i][d] = dp[j][d] + 1   for all j < i where nums[i] - nums[j] == d
```
If no such `j` exists, `dp[i][d] = 2` (the pair `[nums[j], nums[i]]`).

### Base Cases
- Every pair `(i, j)` with `j < i` creates a difference `d = nums[i] - nums[j]` with length 2.

### Intuition (Why This Works)
For each pair `(j, i)`, the difference `d = nums[i] - nums[j]` extends any existing arithmetic sequence ending at `j` with difference `d`. Using dictionaries per index handles arbitrary (possibly large) differences without wasting space.

### Step-by-Step Procedure
1. Initialize `dp = [defaultdict(int) for _ in range(n)]`, `ans = 2` (or 1 if n < 2).
2. For each `i` from 1 to n-1:
   a. For each `j` from 0 to i-1:
      - `d = nums[i] - nums[j]`.
      - `dp[i][d] = dp[j][d] + 1` if `dp[j][d] > 0` else 2.
      - `ans = max(ans, dp[i][d])`.
3. Return `ans`.

### Worked Example (Dry Run)
`nums = [9,4,7,2,10]`.

- i=1 (4): j=0, d=-5 → dp[1][-5]=2
- i=2 (7): j=0, d=-2 → dp[2][-2]=2; j=1, d=3 → dp[2][3]=2
- i=3 (2): j=0, d=-7 → 2; j=1, d=-2 → dp[3][-2]=dp[1][-2]+1=2 (no prev)→2; j=2, d=-5 → dp[3][-5]=dp[2][-5]+1=... dp[2][-5]=0 → 2
- i=4 (10): j=0, d=1 → 2; j=1, d=6 → 2; j=2, d=3 → dp[4][3]=dp[2][3]+1=3; j=3, d=8 → 2

Answer: **3** ([4,7,10] with d=3).

### Code
```python
from collections import defaultdict

class Solution:
    def longestArithSeqLength(self, nums: list) -> int:
        n = len(nums)
        if n <= 2:
            return n
        dp = [defaultdict(int) for _ in range(n)]
        ans = 2
        for i in range(1, n):
            for j in range(i):
                d = nums[i] - nums[j]
                dp[i][d] = dp[j][d] + 1 if dp[j][d] > 0 else 2
                ans = max(ans, dp[i][d])
        return ans
```

### Complexity
- Time: O(n²)
- Space: O(n²) worst case (all differences distinct)

### Common Mistakes & Edge Cases
- `n < 2` → return `n`.
- All elements equal: d=0, answer = n.
- Negative differences: dictionaries handle them naturally.
- The answer is at least 2 for n >= 2 (any pair).

---

## 13. Longest Arithmetic Subsequence of Given Difference (LC #1218) — Medium

**🔗 Practice Link:** [13. Longest Arithmetic Subsequence of Given Difference](https://leetcode.com/problems/longest-arithmetic-subsequence-of-given-difference/)

### Problem Description
Given an array `arr` and an integer `difference`, find the length of the longest subsequence where consecutive elements differ by exactly `difference`. For example, `arr = [1,2,3,4]`, `difference = 1` → answer = 4.

### State Definition
`dp[val]` = length of the longest subsequence ending with value `val`. Use a hash map.

### Recurrence Relation
```
dp[val] = dp[val - difference] + 1
```
If `val - difference` not in map, `dp[val] = 1`.

### Base Cases
- Each element starts a subsequence of length 1.

### Intuition (Why This Works)
Since the difference is fixed, the only valid predecessor of `val` is `val - difference`. A hash map gives O(1) lookup, making this O(n).

### Step-by-Step Procedure
1. `dp = {}`, `ans = 1`.
2. For each `val` in `arr`:
   a. `dp[val] = dp.get(val - difference, 0) + 1`.
   b. `ans = max(ans, dp[val])`.
3. Return `ans`.

### Worked Example (Dry Run)
`arr = [1,5,7,8,5,3,4,2,1]`, `difference = -2`.

- 1: dp[1]=1, ans=1
- 5: dp[5]=dp[7]+1=1, ans=1
- 7: dp[7]=dp[9]+1=1, ans=1
- 8: dp[8]=dp[10]+1=1
- 5: dp[5]=dp[7]+1=2, ans=2
- 3: dp[3]=dp[5]+1=3, ans=3
- 4: dp[4]=dp[6]+1=1
- 2: dp[2]=dp[4]+1=2
- 1: dp[1]=dp[3]+1=4, ans=4

Answer: **4** (subsequence [5,3,1]... wait, 5,3,1 has diff -2 but that's length 3. Actually dp[1]=4 means [8,5,3,1] — no, dp[5] was updated. Let me re-trace: dp[1]=1, dp[5]=1, dp[7]=1, dp[8]=1, dp[5]=dp[7]+1=2 (the second 5), dp[3]=dp[5]+1=3 (using dp[5]=2), dp[4]=1, dp[2]=dp[4]+1=2, dp[1]=dp[3]+1=4. So the chain is: second 5→3→1 using first 1? No: dp[3]=3 means [7,5,3] (first 7, second 5, then 3), then dp[1]=4 means [7,5,3,1]. But 7-5=2≠-2. Hmm, the difference is -2, so prev = val - (-2) = val + 2. dp[5] = dp[7]+1. First 5 (index 1): dp[7]=0 → dp[5]=1. Second 5 (index 4): dp[7]=1 → dp[5]=2. So the chain ending at second 5 goes through 7: [7,5]. Then dp[3]=dp[5]+1=3: [7,5,3]. Then dp[1]=dp[3]+1=4: [7,5,3,1]. But 7-5=2=-(-2)=2 ✓, 5-3=2 ✓, 3-1=2 ✓. The subsequence [7,5,3,1] has difference -2. ✓

Answer: **4**.

### Code
```python
class Solution:
    def longestSubsequence(self, arr: list, difference: int) -> int:
        dp = {}
        ans = 1
        for val in arr:
            dp[val] = dp.get(val - difference, 0) + 1
            ans = max(ans, dp[val])
        return ans
```

### Complexity
- Time: O(n)
- Space: O(n)

### Common Mistakes & Edge Cases
- `difference = 0`: count the most frequent element.
- All elements same: answer = n.
- Large values: hash map handles arbitrary keys.
- This is much simpler than the general case (LC #1027) because the difference is given.

---

## 14. Maximum Length of Subarray With Positive Product (LC #1567) — Medium

**🔗 Practice Link:** [14. Maximum Length of Subarray With Positive Product](https://leetcode.com/problems/maximum-length-of-subarray-with-positive-product/)

### Problem Description
Given an integer array, find the length of the longest contiguous subarray where the product of all elements is positive. For example, `nums = [1,-2,-3,4]` → subarray `[1,-2,-3,4]` has product 24 > 0, length 4.

### State Definition
`pos` = length of longest subarray ending at current index with positive product.
`neg` = length of longest subarray ending at current index with negative product.

### Recurrence Relation
```
if nums[i] > 0:
    pos = pos + 1
    neg = neg + 1 if neg > 0 else 0
elif nums[i] < 0:
    new_pos = neg + 1 if neg > 0 else 0
    neg = pos + 1
    pos = new_pos
else:
    pos = neg = 0
```
Plain English: a positive number extends both streaks; a negative number swaps them (positive becomes negative and vice versa); zero resets both.

### Base Cases
- `pos = neg = 0` before processing any elements.
- `ans = 0`.

### Intuition (Why This Works)
Tracking positive and negative streak lengths captures the sign flip: a negative number turns a negative streak positive (two negatives make a positive) and vice versa. Zero breaks all streaks.

### Step-by-Step Procedure
1. `pos = neg = 0`, `ans = 0`.
2. For each `num` in `nums`:
   a. If `num > 0`: `pos += 1`, `neg = neg + 1 if neg > 0 else 0`.
   b. If `num < 0`: swap and adjust: `new_pos = neg + 1 if neg > 0 else 0`; `neg = pos + 1`; `pos = new_pos`.
   c. If `num == 0`: `pos = neg = 0`.
   d. `ans = max(ans, pos)`.
3. Return `ans`.

### Worked Example (Dry Run)
`nums = [1, -2, -3, 4]`.

| i | num | pos | neg | ans |
|---|-----|-----|-----|-----|
| 0 | 1   | 1   | 0   | 1   |
| 1 | -2  | 0   | 2   | 1   |
| 2 | -3  | 3   | 0   | 3   |
| 3 | 4   | 4   | 0   | 4   |

Answer: **4**.

### Code
```python
class Solution:
    def getMaxLen(self, nums: list) -> int:
        pos = neg = 0
        ans = 0
        for num in nums:
            if num > 0:
                pos += 1
                neg = neg + 1 if neg > 0 else 0
            elif num < 0:
                new_pos = neg + 1 if neg > 0 else 0
                neg = pos + 1
                pos = new_pos
            else:
                pos = neg = 0
            ans = max(ans, pos)
        return ans
```

### Complexity
- Time: O(n)
- Space: O(1)

### Common Mistakes & Edge Cases
- All positive: answer = n.
- Starts with negative: neg=1, pos=0 (no positive product yet).
- Zero resets everything (breaks contiguous subarray).
- Single negative: answer = 0 (no positive product subarray).
- Two negatives: [−1,−2] → positive product of length 2.

---

## 15. Count Subarrays with Bounded Maximum (LC #795) — Medium

**🔗 Practice Link:** [15. Count Subarrays with Bounded Maximum](https://leetcode.com/problems/count-subarrays-with-bounded-maximum/)

### Problem Description
Given an integer array `nums` and two integers `left` and `right`, count the number of contiguous subarrays where the maximum element is in the range `[left, right]`. For example, `nums = [2,1,4,3]`, `left = 2`, `right = 3` → subarrays: [2], [2,1], [1], [3] → 4.

### State Definition
Count all subarrays minus those with max < left minus those with max > right. Or directly count using the "at most" trick.

### Recurrence Relation
```
atMost(right) - atMost(left - 1)
```
where `atMost(limit)` = number of subarrays where all elements ≤ limit.

### Base Cases
- Empty array → 0.

### Intuition (Why This Works)
The "at most" trick: subarrays with max in [left, right] = (subarrays with all elements ≤ right) − (subarrays with all elements ≤ left−1). The first includes subarrays with max too small, and subtracting the second removes them.

### Step-by-Step Procedure
1. Define `atMost(limit)`: scan with a counter of consecutive elements ≤ limit.
2. For each element > limit, reset counter. Otherwise increment.
3. Add counter to total at each step.
4. Return `atMost(right) - atMost(left - 1)`.

### Worked Example (Dry Run)
`nums = [2,1,4,3]`, `left = 2`, `right = 3`.

`atMost(3)`: elements ≤ 3: 2,1,_,3
- i=0: 2≤3, count=1, total=1
- i=1: 1≤3, count=2, total=3
- i=2: 4>3, count=0, total=3
- i=3: 3≤3, count=1, total=4
atMost(3) = 4

`atMost(1)`: elements ≤ 1: _,1,_,_
- i=0: 2>1, count=0, total=0
- i=1: 1≤1, count=1, total=1
- i=2: 4>1, count=0, total=1
- i=3: 3>1, count=0, total=1
atMost(1) = 1

Answer: 4 - 1 = **3**... but I said 4 earlier. Let me recount. Subarrays with max in [2,3]: [2] (max=2✓), [2,1] (max=2✓), [1] (max=1✗), [4] (max=4✗), [4,3] (max=4✗), [3] (max=3✓), [2,1,4] (max=4✗), [1,4] (max=4✗), [2,1,4,3] (max=4✗). Valid: [2], [2,1], [3] = 3. Answer is **3**.

### Code
```python
class Solution:
    def numSubarrayBoundedMax(self, nums: list, left: int, right: int) -> int:
        def atMost(limit):
            count = total = 0
            for num in nums:
                if num <= limit:
                    count += 1
                else:
                    count = 0
                total += count
            return total
        return atMost(right) - atMost(left - 1)
```

### Complexity
- Time: O(n)
- Space: O(1)

### Common Mistakes & Edge Cases
- `left > right` → 0 (impossible range).
- All elements in range → n*(n+1)/2 (all subarrays qualify).
- All elements outside range → 0.
- `atMost(left-1)` correctly handles the lower bound subtraction.

---

## 16. Minimum Number of Increments on Subarrays to Form Target Array (LC #1536) — Hard

**🔗 Practice Link:** [16. Minimum Number of Increments on Subarrays to Form Target Array](https://leetcode.com/problems/minimum-number-of-increments-on-subarrays-to-form-a-target-array/)

### Problem Description
Given an array `target`, start with all zeros. In one operation, you can increment all elements of a contiguous subarray by 1. Find the minimum operations to form `target`. For example, `target = [3,1,5,4,2]` → answer = 7.

### State Definition
Compare adjacent elements. The answer is `target[0] + sum(max(0, target[i] - target[i-1])` for i=1..n-1).

### Recurrence Relation
```
ops = target[0] + sum(max(0, target[i] - target[i-1]) for i in 1..n-1)
```
Plain English: each "new height" at position `i` that exceeds the previous requires additional operations. The first element always contributes its full value.

### Base Cases
- Empty array → 0.
- Single element → `target[0]`.

### Intuition (Why This Works)
Think of the target as a skyline. The first element needs `target[0]` operations (one unit at a time). Each subsequent element needs extra operations only if it's taller than its left neighbor (the difference must be built up separately). If it's shorter, the previous "layers" already covered it.

### Step-by-Step Procedure
1. If empty, return 0.
2. `ops = target[0]`.
3. For `i` from 1 to n-1:
   a. If `target[i] > target[i-1]`: `ops += target[i] - target[i-1]`.
4. Return `ops`.

### Worked Example (Dry Run)
`target = [3, 1, 5, 4, 2]`.

- ops = 3 (for target[0]=3)
- i=1: 1 < 3 → no addition
- i=2: 5 > 1 → ops += 4 → ops = 7
- i=3: 4 < 5 → no addition
- i=4: 2 < 4 → no addition

Answer: **7**. Visualization:
```
Layer 5:         X
Layer 4:     X   X X
Layer 3: X   X   X X   X
Layer 2: X   X X X X X X
Layer 1: X X X X X X X X
        3 1 5 4 2
Ops:    3 + 0 + 4 + 0 + 0 = 7
```

### Code
```python
class Solution:
    def minNumberOperations(self, target: list) -> int:
        if not target:
            return 0
        ops = target[0]
        for i in range(1, len(target)):
            if target[i] > target[i - 1]:
                ops += target[i] - target[i - 1]
        return ops
```

### Complexity
- Time: O(n)
- Space: O(1)

### Common Mistakes & Edge Cases
- All same values: answer = that value.
- Strictly increasing: answer = last element.
- Strictly decreasing: answer = first element.
- `target[0] = 0`: still counts (ops starts at 0).

---

## 17. Maximum Number of Non-overlapping Subarrays with Sum Zero (LC #1546) — Medium

**🔗 Practice Link:** [17. Maximum Number of Non-overlapping Subarrays with Sum Zero](https://leetcode.com/problems/maximum-number-of-non-overlapping-subarrays-with-sum-equals-target/)

### Problem Description
Given an array, find the maximum number of non-overlapping subarrays whose sum is zero. For example, `nums = [1,-1,1,-1]` → subarrays [0,1] and [2,3] each sum to 0 → answer = 2.

### State Definition
Use a prefix sum hash map. When a prefix sum repeats, a zero-sum subarray exists between the two occurrences.

### Recurrence Relation
```
if prefix_sum seen before:
    count += 1
    reset prefix_map (to ensure non-overlapping)
else:
    add prefix_sum to map
```

### Base Cases
- `prefix_sum = 0` at the start → counts as a valid subarray from the beginning.

### Intuition (Why This Works)
A zero-sum subarray exists between indices `i` and `j` iff `prefix[j] == prefix[i]`. To maximize non-overlapping count, greedily take the earliest zero-sum subarray and reset the map (so subsequent subarrays don't overlap).

### Step-by-Step Procedure
1. `prefix = 0`, `count = 0`, `seen = {0}`.
2. For each `num` in `nums`:
   a. `prefix += num`.
   b. If `prefix` in `seen`: `count += 1`, `seen = {0}` (reset).
   c. Else: `seen.add(prefix)`.
3. Return `count`.

### Worked Example (Dry Run)
`nums = [1,-1,1,-1]`.

- prefix=0, seen={0}, count=0
- num=1: prefix=1, not in seen → seen={0,1}
- num=-1: prefix=0, in seen → count=1, seen={0}
- num=1: prefix=1, not in seen → seen={0,1}
- num=-1: prefix=0, in seen → count=2, seen={0}

Answer: **2**.

### Code
```python
class Solution:
    def maxNonOverlapping(self, nums: list) -> int:
        count = 0
        prefix = 0
        seen = {0}
        for num in nums:
            prefix += num
            if prefix in seen:
                count += 1
                seen = {0}
            else:
                seen.add(prefix)
        return count
```

### Complexity
- Time: O(n)
- Space: O(n)

### Common Mistakes & Edge Cases
- Must reset the seen set after finding a subarray to ensure non-overlapping.
- `nums = [0]`: count = 1 (prefix goes to 0, which is in seen).
- All zeros: count = n (each element is a zero-sum subarray).
- No zero-sum subarray: count = 0.

---

## 18. Minimum Cost to Split Array (LC #2547) — Hard

**🔗 Practice Link:** [18. Minimum Cost to Split Array](https://leetcode.com/problems/minimum-cost-to-split-an-array/)

### Problem Description
Given an array `nums` and an integer `k`, split `nums` into consecutive subarrays. The cost of a subarray is `(length of subarray - 1) * k + (sum of subarray)`. Minimize the total cost of the split.

### State Definition
`dp[i]` = minimum cost to split `nums[0..i-1]`. Answer is `dp[n]`.

### Recurrence Relation
```
dp[i] = min over j < i of (dp[j] + (i - j - 1) * k + sum(nums[j..i-1]))
```
Plain English: try every possible last subarray ending at `i-1` starting at `j`.

### Base Cases
- `dp[0] = 0` (zero elements, zero cost).

### Intuition (Why This Works)
Every split has a last subarray. Trying all starting points for the last subarray and combining with the optimal cost of the prefix gives optimal substructure. The subarray sum is computed via prefix sums.

### Step-by-Step Procedure
1. Compute prefix sums.
2. `dp[0] = 0`, `dp[i] = inf` for i > 0.
3. For `i` from 1 to n:
   a. For `j` from 0 to i-1:
      - `cost = dp[j] + (i - j - 1) * k + (prefix[i] - prefix[j])`.
      - `dp[i] = min(dp[i], cost)`.
4. Return `dp[n]`.

### Worked Example (Dry Run)
`nums = [1,2,3,4]`, `k = 4`. prefix = [0,1,3,6,10].

- dp[0] = 0
- dp[1]: j=0 → 0 + 0*4 + 1 = 1
- dp[2]: j=0 → 0 + 1*4 + 3 = 7; j=1 → 1 + 0*4 + 2 = 3 → dp[2]=3
- dp[3]: j=0 → 0+2*4+6=14; j=1 → 1+1*4+3=8; j=2 → 3+0*4+3=6 → dp[3]=6
- dp[4]: j=0 → 0+3*4+10=22; j=1 → 1+2*4+7=16; j=2 → 3+1*4+4=11; j=3 → 6+0*4+4=10 → dp[4]=10

Answer: **10** (split as [1,2,3,4], one subarray, cost = 3*4 + 10 = 22... that's 22, not 10. Wait: dp[4]=10 from j=3: dp[3]+0*4+4=6+0+4=10. This means the last subarray is [4] (length 1, cost=0*4+4=4) and the prefix [1,2,3] has cost 6. So splits: [1,2,3] and [4]. Cost of [1,2,3]: dp[2]=3 + cost of [1,2]... no. dp[3]=6 means the optimal split of [1,2,3] costs 6. dp[3] came from j=2: dp[2]+0*4+3=3+0+3=6. So [1,2] costs 3 and [3] costs 3. Total: [1,2]=3, [3]=3, [4]=4 → 10. ✓

### Code
```python
class Solution:
    def minCost(self, nums: list, k: int) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]
        inf = float('inf')
        dp = [inf] * (n + 1)
        dp[0] = 0
        for i in range(1, n + 1):
            for j in range(i):
                cost = dp[j] + (i - j - 1) * k + (prefix[i] - prefix[j])
                dp[i] = min(dp[i], cost)
        return dp[n]
```

### Complexity
- Time: O(n²)
- Space: O(n)

### Common Mistakes & Edge Cases
- `k = 0`: cost = sum of elements regardless of split.
- `n = 1`: cost = 0 (single element subarray, length-1=0).
- The `(i-j-1)` factor counts the number of pairs in the subarray minus 1... actually it's `(length - 1) * k` where length = `i - j`.

---

## 19. Longest Substring with At Most 2 Distinct Characters — Medium

**🔗 Practice Link:** [19. Longest Substring with At Most 2 Distinct Characters — Medium](https://www.geeksforgeeks.org/longest-substring-with-at-most-two-distinct-characters)

### Problem Description
Find the length of the longest substring with at most 2 distinct characters. For example, `s = "eceba"` → "ece" has length 3.

### State Definition
Sliding window with a hash map tracking character frequencies within the window.

### Recurrence Relation
```
Expand right pointer; when distinct > 2, shrink left pointer until distinct ≤ 2.
max_length = max(max_length, window_size)
```

### Base Cases
- Empty string → 0.
- String length ≤ 2 → return length.

### Intuition (Why This Works)
The sliding window maintains at most 2 distinct characters. Expanding the right adds characters; when a third distinct character enters, we shrink from the left until one character's count drops to 0 (leaving at most 2 distinct).

### Step-by-Step Procedure
1. `left = 0`, `max_len = 0`, `count = {}`.
2. For `right` from 0 to n-1:
   a. Add `s[right]` to count.
   b. While `len(count) > 2`: remove `s[left]`, `left += 1`.
   c. `max_len = max(max_len, right - left + 1)`.
3. Return `max_len`.

### Worked Example (Dry Run)
`s = "eceba"`.

| right | char | count | left | window | len |
|-------|------|-------|------|--------|-----|
| 0     | e    | {e:1} | 0    | "e"    | 1   |
| 1     | c    | {e:1,c:1}| 0 | "ec"   | 2   |
| 2     | e    | {e:2,c:1}| 0 | "ece"  | 3   |
| 3     | b    | {e:2,c:1,b:1}| 2 | "ceb" | 3 |
| 4     | a    | {e:1,b:1,a:1}| 3 | "ba" | 2 |

Wait, at right=3: count has 3 distinct → shrink left. left=0: remove 'e', count={c:1,b:1}, left=1. Window="ceb", len=3. At right=4: count={c:1,b:1,a:1} → 3 distinct → remove s[1]='c', left=2, count={b:1,a:1}. Window="ba", len=2.

Answer: **3**.

### Code
```python
class Solution:
    def lengthOfLongestSubstringTwoDistinct(self, s: str) -> int:
        from collections import defaultdict
        count = defaultdict(int)
        left = 0
        max_len = 0
        for right in range(len(s)):
            count[s[right]] += 1
            while len(count) > 2:
                count[s[left]] -= 1
                if count[s[left]] == 0:
                    del count[s[left]]
                left += 1
            max_len = max(max_len, right - left + 1)
        return max_len
```

### Complexity
- Time: O(n)
- Space: O(1) (at most 3 characters in the map)

### Common Mistakes & Edge Cases
- Must delete the key from the map when count reaches 0 (for correct `len(count)` check).
- Empty string → 0.
- All same characters → entire string length.
- Exactly 2 distinct → entire string length.

---

## 20. Paint House IV — Hard

**🔗 Practice Link:** [20. Paint House IV — Hard](https://www.geeksforgeeks.org/minimize-cost-of-painting-n-houses-such-that-adjacent-houses-have-different-colors)

### Problem Description
There are `n` houses in a circle, each to be painted one of `k` colors. Painting house `i` with color `j` costs `cost[i][j]`. Adjacent houses (including first and last, since it's a circle) cannot share the same color. Minimize total cost. This is a circular constraint extension of the classic Paint House problem.

### State Definition
`dp[i][c]` = minimum cost to paint houses `0..i` where house `i` has color `c`. For the circular constraint, fix the first house's color and solve linearly.

### Recurrence Relation
```
dp[i][c] = cost[i][c] + min(dp[i-1][c'] for c' != c)
```
For the circle: try each possible color for house 0, solve the linear chain 1..n-1, and ensure house n-1's color ≠ house 0's color.

### Base Cases
- For each fixed color `first_color` of house 0: `dp[0][c] = cost[0][c]` if `c == first_color`, else infinity.
- Answer = min over `first_color` of `dp[n-1][c]` where `c != first_color`.

### Intuition (Why This Works)
Breaking the circular constraint by fixing the first color reduces it to a linear chain with an added constraint at the end. The linear chain is a standard DP with k states per position.

### Step-by-Step Procedure
1. `ans = inf`.
2. For each `first_color` in range(k):
   a. Initialize `dp = [inf] * k`; `dp[first_color] = cost[0][first_color]`.
   b. For `i` from 1 to n-1:
      - `new_dp = [inf] * k`.
      - For each color `c` in range(k):
        - For each color `c'` in range(k) where `c' != c`:
          - `new_dp[c] = min(new_dp[c], cost[i][c] + dp[c'])`.
      - `dp = new_dp`.
   c. For each `c` in range(k) where `c != first_color`:
      - `ans = min(ans, dp[c])`.
3. Return `ans`.

### Worked Example (Dry Run)
`cost = [[1,5],[2,3]]`, `k = 2`.

- first_color=0: dp=[1,inf]. i=1: new_dp[0]=min(inf, cost[1][0]+dp[1])=inf; new_dp[1]=min(inf, cost[1][1]+dp[0])=3+1=4. dp=[inf,4]. c!=0: dp[1]=4.
- first_color=1: dp=[inf,5]. i=1: new_dp[0]=cost[1][0]+dp[1]=2+5=7; new_dp[1]=inf. dp=[7,inf]. c!=1: dp[0]=7.
- ans = min(4,7) = **4**.

### Code
```python
class Solution:
    def minCostIII(self, cost: list, k: int) -> int:
        n = len(cost)
        if n == 0:
            return 0
        inf = float('inf')
        ans = inf
        for first in range(k):
            dp = [inf] * k
            dp[first] = cost[0][first]
            for i in range(1, n):
                new_dp = [inf] * k
                for c in range(k):
                    for c2 in range(k):
                        if c2 != c:
                            new_dp[c] = min(new_dp[c], cost[i][c] + dp[c2])
                dp = new_dp
            for c in range(k):
                if c != first:
                    ans = min(ans, dp[c])
        return ans
```

### Complexity
- Time: O(k² × n × k) = O(k² × n) with k iterations for the first color
- Space: O(k)

### Common Mistakes & Edge Cases
- Circular constraint: house 0 and house n-1 must differ.
- `n = 1`: only one house, cost = min(cost[0]).
- `k = 1` with `n > 1`: impossible (return -1 or inf).
- `k = 2` with `n` odd: may still be feasible.
- Optimization: precompute the two smallest values per row to avoid the O(k²) inner loop.

---

## 21. Maximum Weighted Job Scheduling — Hard

**🔗 Practice Link:** [21. Maximum Weighted Job Scheduling — Hard](https://leetcode.com/problems/maximum-profit-in-job-scheduling/)

### Problem Description
Given `n` jobs with start time, finish time, and weight (profit), select a subset of non-overlapping jobs to maximize total weight. This is the weighted interval scheduling problem. For example, `jobs = [(1,3,5),(2,5,6),(4,6,5),(6,7,4)]` → best selection: jobs 0 and 2 (weight 5+5=10).

### State Definition
`dp[i]` = maximum weight achievable considering jobs `0..i-1` (sorted by finish time).

### Recurrence Relation
```
dp[i] = max(dp[i-1], weight[i-1] + dp[p(i)])
```
where `p(i)` = rightmost job finishing before job `i` starts (found via binary search).

### Base Cases
- `dp[0] = 0`.

### Intuition (Why This Works)
Sorted by finish time, for each job we either skip it or take it plus the best compatible prefix. Binary search on finish times gives O(log n) predecessor lookup.

### Step-by-Step Procedure
1. Sort jobs by finish time.
2. Compute `p(i)` for each job (binary search).
3. `dp[0] = 0`.
4. For `i` from 1 to n: `dp[i] = max(dp[i-1], dp[p(i)] + weight[i-1])`.
5. Return `dp[n]`.

### Worked Example (Dry Run)
`jobs = [(1,3,5),(2,5,6),(4,6,5),(6,7,4)]`. Already sorted by finish.

- p(1)=0, p(2)=0, p(3)=1 (job 0 finishes at 3 ≤ start 4), p(4)=2 (job 1 finishes at 5 ≤ start 6).
- dp[0]=0
- dp[1]=max(0, dp[0]+5)=5
- dp[2]=max(5, dp[0]+6)=6
- dp[3]=max(6, dp[1]+5)=max(6,10)=10
- dp[4]=max(10, dp[2]+4)=max(10,10)=10

Answer: **10**.

### Code
```python
import bisect

class Solution:
    def jobScheduling(self, jobs: list) -> int:
        # jobs = [(start, finish, weight), ...]
        jobs.sort(key=lambda x: x[1])
        n = len(jobs)
        finishes = [j[1] for j in jobs]
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            start, finish, weight = jobs[i - 1]
            p = bisect.bisect_right(finishes, start, 0, i - 1)
            dp[i] = max(dp[i - 1], dp[p] + weight)
        return dp[n]
```

### Complexity
- Time: O(n log n)
- Space: O(n)

### Common Mistakes & Edge Cases
- `bisect_right` allows touching intervals (finish == start is compatible).
- Must sort by finish time, not start time.
- All jobs overlap: answer = max weight.
- No jobs overlap: answer = sum of all weights.

---

## 22. Longest Path in Matrix with Hops — Medium

**🔗 Practice Link:** [22. Longest Path in Matrix with Hops — Medium](https://www.geeksforgeeks.org/longest-path-in-a-directed-acyclic-graph-dynamic-programming)

### Problem Description
Given an `m x n` matrix where each cell has a value, find the longest path where each step moves to an adjacent cell (up, down, left, right) with a strictly greater value. You may optionally make `k` "hops" — jumps to any cell in the matrix (not just adjacent). Maximize the path length.

### State Definition
`dp[i][j][h]` = longest path starting at cell `(i,j)` with `h` hops remaining. Use DFS + memoization.

### Recurrence Relation
```
dp[i][j][h] = 1 + max(dp[ni][nj][h] for adjacent (ni,nj) with val > val[i][j])
             1 + max(dp[ni][nj][h-1] for all (ni,nj) with val > val[i][j])  # hop
```
Take the maximum of the adjacent move (no hop used) and the best hop (use one hop).

### Base Cases
- All cells have `dp[i][j][0] = 1 + max(dp[ni][nj][0])` for adjacent cells with greater value, or 1 if no such neighbor.

### Intuition (Why This Works)
DFS explores all paths; memoization caches `(i, j, h)` states. Hops provide shortcuts to distant high-value cells, extending the path beyond what adjacency allows.

### Step-by-Step Procedure
1. Create memo dictionary.
2. For each cell `(i,j)`, call `dfs(i, j, k)`.
3. `dfs(i, j, h)`: if memoized, return. Otherwise:
   a. `best = 1` (the cell itself).
   b. For each adjacent `(ni, nj)` with `matrix[ni][nj] > matrix[i][j]`:
      - `best = max(best, 1 + dfs(ni, nj, h))`.
   c. If `h > 0`: for each cell `(r, c)` with `matrix[r][c] > matrix[i][j]`:
      - `best = max(best, 1 + dfs(r, c, h - 1))`.
   d. Memoize and return `best`.
4. Answer = max over all `dfs(i, j, k)`.

### Worked Example (Dry Run)
`matrix = [[1,2],[3,4]]`, `k = 0`.

- (0,0)=1: adj (0,1)=2>1 → 1+dfs(0,1,0); (1,0)=3>1 → 1+dfs(1,0,0)
- (0,1)=2: adj (1,1)=4>2 → 1+dfs(1,1,0)=2; (0,0)=1<2 no; (1,0)=3>2 → 1+dfs(1,0,0)
- (1,0)=3: adj (1,1)=4>3 → 1+dfs(1,1,0)=2
- (1,1)=4: no adj > 4 → 1

Back: dfs(1,0)=2, dfs(0,1)=3 (via (0,1)→(1,0)→(1,1)), dfs(0,0)=4 (via (0,0)→(0,1)→(1,0)→(1,1)).

Answer: **4**.

### Code
```python
class Solution:
    def longestPath(self, matrix: list, k: int) -> int:
        m, n = len(matrix), len(matrix[0])
        memo = {}
        dirs = [(-1,0),(1,0),(0,-1),(0,1)]
        
        def dfs(i, j, hops):
            if (i, j, hops) in memo:
                return memo[(i, j, hops)]
            best = 1
            for di, dj in dirs:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] > matrix[i][j]:
                    best = max(best, 1 + dfs(ni, nj, hops))
            if hops > 0:
                for r in range(m):
                    for c in range(n):
                        if matrix[r][c] > matrix[i][j]:
                            best = max(best, 1 + dfs(r, c, hops - 1))
            memo[(i, j, hops)] = best
            return best
        
        ans = 0
        for i in range(m):
            for j in range(n):
                ans = max(ans, dfs(i, j, k))
        return ans
```

### Complexity
- Time: O(m × n × k × (m × n)) — each state explores all cells for hops.
- Space: O(m × n × k)

### Common Mistakes & Edge Cases
- `k = 0`: standard longest increasing path (DFS + memo).
- All same values: answer = 1 (no strictly greater neighbor).
- `k ≥ 1` with all cells: can chain any increasing values via hops.
- Memo key must include `hops` (not just `(i, j)`).

---

## 23. Maximum Product of Three Numbers (LC #1464) — Easy

**🔗 Practice Link:** [23. Maximum Product of Three Numbers](https://leetcode.com/problems/maximum-product-of-three-numbers/)

### Problem Description
Given an integer array, find the maximum product of three numbers. For example, `nums = [1,2,3]` → 6. `nums = [-10,-10,1,3,2]` → (-10)(-10)(3) = 300.

### State Definition
No DP — just track the three largest and two smallest values.

### Recurrence Relation
```
max_product = max(product of top 3 largest, product of bottom 2 smallest × largest)
```

### Base Cases
- `n = 3` → product of all three.

### Intuition (Why This Works)
The maximum product of three numbers is either from the three largest positive numbers or from two large negative numbers (which become positive) multiplied by the largest positive. Track both candidates.

### Step-by-Step Procedure
1. Sort the array.
2. `n = len(nums)`.
3. Return `max(nums[-1]*nums[-2]*nums[-3], nums[0]*nums[1]*nums[-1])`.

### Worked Example (Dry Run)
`nums = [-10, -10, 1, 3, 2]`. Sorted: `[-10, -10, 1, 2, 3]`.

- Top 3: 1×2×3 = 6
- Bottom 2 × top 1: (-10)×(-10)×3 = 300

Answer: **300**.

### Code
```python
class Solution:
    def maximumProduct(self, nums: list) -> int:
        nums.sort()
        n = len(nums)
        return max(nums[-1] * nums[-2] * nums[-3], nums[0] * nums[1] * nums[-1])
```

### Complexity
- Time: O(n log n) for sorting
- Space: O(1)

### Common Mistakes & Edge Cases
- All negative: answer = product of three largest (least negative).
- Mix of positive and negative: the two-negative-one-positive combo might win.
- `n = 3` exactly: just return the product.
- Overflow: Python handles big ints natively.

---

## Summary Table

```
┌────┬─────────────────────────────────────────────────────┬───────────┬──────────────────────┐
│ #  │ Problem                                             │ Difficulty│ Key Technique        │
├────┼─────────────────────────────────────────────────────┼───────────┼──────────────────────┤
│  1 │ Frog Jump (LC #403)                                 │ Hard      │ Hash map + DFS/BFS   │
│  2 │ Min Cost to Make Array Equal (LC #2448)             │ Hard      │ Weighted median      │
│  3 │ Maximum Earnings from Taxi (LC #2002)               │ Medium    │ Interval DP          │
│  4 │ Min Operations Array Continuous (LC #2009)          │ Hard      │ Two pointers + sort  │
│  5 │ Count Increasing Subsequences                       │ Medium    │ O(n²) counting DP    │
│  6 │ Min Moves Array Complementary (LC #1674)            │ Medium    │ Difference array     │
│  7 │ Maximum Profit from Selling Candies                 │ Medium    │ Greedy sort by price │
│  8 │ Count Arrays Bounded Difference                     │ Medium    │ DP + prefix sums     │
│  9 │ Min Cost Connect Sticks (LC #1167)                  │ Medium    │ Min-heap greedy      │
│ 10 │ Ways to Split Three Subarrays (LC #1712)            │ Medium    │ Prefix sum + binary  │
│ 11 │ Min Cost Reduce Array to Single Element             │ Medium    │ Interval DP (MCM)    │
│ 12 │ Longest Arithmetic Subsequence (LC #1027)           │ Medium    │ O(n²) DP + dict      │
│ 13 │ Longest Arithmetic Given Diff (LC #1218)            │ Medium    │ Hash map DP          │
│ 14 │ Max Length Positive Product (LC #1567)               │ Medium    │ Two-state tracking   │
│ 15 │ Count Subarrays Bounded Max (LC #795)               │ Medium    │ At-most trick        │
│ 16 │ Min Increments on Subarrays (LC #1536)              │ Hard      │ Greedy (skyline)     │
│ 17 │ Max Non-overlapping Zero Sum (LC #1546)             │ Medium    │ Prefix sum + greedy  │
│ 18 │ Min Cost to Split Array (LC #2547)                  │ Hard      │ O(n²) DP + prefix    │
│ 19 │ Longest Substring 2 Distinct                        │ Medium    │ Sliding window       │
│ 20 │ Paint House IV                                      │ Hard      │ Fix-first + linear DP│
│ 21 │ Maximum Weighted Job Scheduling                     │ Hard      │ Sort + DP + binary   │
│ 22 │ Longest Path in Matrix with Hops                    │ Medium    │ DFS + memoization    │
│ 23 │ Maximum Product of Three Numbers (LC #1464)         │ Easy      │ Sort + candidates    │
└────┴─────────────────────────────────────────────────────┴───────────┴──────────────────────┘
```
