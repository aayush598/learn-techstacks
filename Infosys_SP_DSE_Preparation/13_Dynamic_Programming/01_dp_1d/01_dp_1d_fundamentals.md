# 1D Dynamic Programming — Fundamentals

## What is Dynamic Programming?

Dynamic Programming is an algorithmic technique that solves problems by:
1. Dividing into **overlapping subproblems**
2. Solving each subproblem **once**
3. **Storing** the result for reuse

Two approaches:
- **Memoization (Top-Down):** Recursive + caching. Solve the problem naturally, cache results.
- **Tabulation (Bottom-Up):** Iterative table filling. Start from base cases, build up to target.

**When is 1D DP applicable?** A problem is a good 1D DP candidate when:
- The answer depends on a single integer "state" (e.g., position in an array, number of steps, length of a prefix).
- The optimal answer for that state can be computed from optimal answers of smaller states (**optimal substructure**).
- The same smaller states are needed over and over again (**overlapping subproblems**).

---

## Fibonacci-Style DP (Counting & Simple Recurrences)

### Fibonacci Numbers

**🔗 Practice Link:** [Fibonacci Numbers](https://www.geeksforgeeks.org/program-for-nth-fibonacci-number)

**Problem Explanation:**
The Fibonacci sequence is defined as F(0) = 0, F(1) = 1, and every later number is the sum of the two before it: F(n) = F(n-1) + F(n-2). Given an integer n (n >= 0), return the n-th Fibonacci number F(n). The sequence starts 0, 1, 1, 2, 3, 5, 8, 13, ... This is the simplest possible DP and the template for every other problem in this file.

**State Definition:**
`dp[i]` = the i-th Fibonacci number, F(i).

**Recurrence Relation:**
`dp[i] = dp[i-1] + dp[i-2]` for `i >= 2`
Every number is exactly the sum of the two previous numbers, so once dp[i-1] and dp[i-2] are known, dp[i] is known.

**Base Cases:**
- `dp[0] = 0`
- `dp[1] = 1`

**Intuition (Why This Works):**
F(n) depends only on F(n-1) and F(n-2), and those in turn depend on the *same* smaller values (overlapping subproblems). A naive recursion recomputes F(k) an exponential number of times. DP stores each F(k) once — this is the optimal substructure at work: the larger answer is a simple combination of smaller stored answers. The "choice" is trivial here (you always add the two previous values), so the whole file is really about how to store and reuse those values.

**Step-by-Step Procedure:**
1. If `n <= 1`, return `n` immediately (base case).
2. Create an array `dp` of size `n + 1`.
3. Set `dp[0] = 0` and `dp[1] = 1`.
4. Loop `i` from 2 to `n` (inclusive).
5. In each iteration set `dp[i] = dp[i - 1] + dp[i - 2]`.
6. After the loop, return `dp[n]`.
7. (Memoization alternative) Write a recursive function that returns `n` for `n <= 1`, otherwise computes and caches `fib(n-1) + fib(n-2)` before returning.
8. (Space optimization) Notice dp[i] only needs the two previous values — keep two rolling variables `prev2`, `prev1` instead of the whole array and slide them forward each iteration.

**Worked Example (Dry Run):**
n = 6. Initialize `dp = [0, 1, _, _, _, _, _]`.

| i | dp[i-2] | dp[i-1] | dp[i] = dp[i-1] + dp[i-2] |
|---|---------|---------|---------------------------|
| 2 | 0       | 1       | 1                         |
| 3 | 1       | 1       | 2                         |
| 4 | 1       | 2       | 3                         |
| 5 | 2       | 3       | 5                         |
| 6 | 3       | 5       | 8                         |

Final `dp = [0, 1, 1, 2, 3, 5, 8]`. **Answer: 8**, since F(6) = 8.

**Code:**
```python
# 1) Plain recursion (exponential) — shown for comparison only
def fib_recursive(n: int) -> int:
    if n <= 1:
        return n                     # Base case: F(0)=0, F(1)=1
    # Recomputed the same subproblems over and over -> O(2^n) time
    return fib_recursive(n - 1) + fib_recursive(n - 2)

# 2) Memoization (top-down): recursion + cache
def fib_memo(n: int, memo=None) -> int:
    if memo is None:
        memo = {}                    # Fresh cache on the first (outermost) call
    if n <= 1:
        return n                     # Base case
    if n not in memo:                # Compute and store only if not already known
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]                   # Reuse the cached answer

# 3) Tabulation (bottom-up): fill a table from the base up
def fib_tab(n: int) -> int:
    if n <= 1:
        return n
    dp = [0] * (n + 1)               # dp[i] will hold F(i)
    dp[1] = 1                        # Base case F(1) = 1 (F(0) is already 0)
    for i in range(2, n + 1):        # Fill from small to large
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

# 4) Space-optimized tabulation: only the last two values are ever needed
def fib_optimized(n: int) -> int:
    if n <= 1:
        return n
    prev2, prev1 = 0, 1              # F(0) and F(1)
    for _ in range(2, n + 1):
        curr = prev1 + prev2         # F(i) = F(i-1) + F(i-2)
        prev2, prev1 = prev1, curr   # Slide window forward
    return prev1                     # After the loop prev1 = F(n)
```

**Complexity:**
- Time: O(n) for memo, tab, and optimized; O(2^n) for plain recursion.
- Space: O(n) for memo (cache + recursion stack) and tab (array); O(1) for optimized.

**Common Mistakes & Edge Cases:**
- Forgetting base cases n = 0 and n = 1 causes out-of-bounds indexing or wrong answers.
- Using `range(2, n)` instead of `range(2, n + 1)` — the target `dp[n]` is never filled.
- With memoization, forgetting to write to the cache silently reverts to exponential time.
- Space-optimized swap order matters: update `prev2` from the old `prev1`, then `prev1` to `curr` — the opposite order loses data.
- Recursive versions overflow Python's recursion limit for very large n; use iteration.

### Climbing Stairs

**🔗 Practice Link:** [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/)

**Problem Explanation:**
You are climbing a staircase. It takes n steps to reach the top, and each move you can climb either 1 step or 2 steps. Count how many *distinct sequences* of moves reach the top. For example, with n = 3 the ways are (1,1,1), (1,2), (2,1) → 3 ways. The input is the integer n (number of steps); the output is the integer count of ways.

**State Definition:**
`dp[i]` = number of distinct ways to reach step i (with dp[0] = the starting position at the bottom).

**Recurrence Relation:**
`dp[i] = dp[i-1] + dp[i-2]`
To land on step i, your last move was either a 1-step from step i-1 or a 2-step from step i-2; these two cases are disjoint (different last moves) and together cover every path, so the counts simply add.

**Base Cases:**
- `dp[0] = 1` (there is exactly 1 way to be at the bottom: take no steps)
- `dp[1] = 1` (the only way to reach step 1 is a single 1-step)

**Intuition (Why This Works):**
The number of ways to reach step i only depends on the number of ways to reach steps i-1 and i-2, and those smaller subproblems are reused by many bigger ones — textbook overlapping subproblems. The "choice" at each step is which step you arrived from (one step back or two steps back). This is identical to Fibonacci: dp[i] = dp[i-1] + dp[i-2], just with different base values, so any Fibonacci solution works with `dp[0] = dp[1] = 1`.

**Step-by-Step Procedure:**
1. If `n <= 1`, return 1 (only one way when there are 0 or 1 steps).
2. Create `dp` of size `n + 1`.
3. Set `dp[0] = 1`, `dp[1] = 1`.
4. Loop `i` from 2 to `n`.
5. Set `dp[i] = dp[i - 1] + dp[i - 2]`.
6. Return `dp[n]`.
7. Optimize space: only `dp[i-1]` and `dp[i-2]` are needed, so keep two rolling variables.
8. For a memoized version, cache `climb(i) = climb(i-1) + climb(i-2)` with the same bases.

**Worked Example (Dry Run):**
n = 4. Initialize `dp[0] = 1`, `dp[1] = 1`.

| i | dp[i-1] | dp[i-2] | dp[i] | meaning |
|---|---------|---------|-------|---------|
| 2 | 1       | 1       | 2     | (1,1), (2) |
| 3 | 2       | 1       | 3     | (1,1,1), (1,2), (2,1) |
| 4 | 3       | 2       | 5     | (1,1,1,1), (1,1,2), (1,2,1), (2,1,1), (2,2) |

Final `dp = [1, 1, 2, 3, 5]`. **Answer: 5 distinct ways.**

**Code:**
```python
def climb_stairs_memo(n: int, memo=None) -> int:
    if memo is None:
        memo = {}                    # Fresh cache on first call
    if n <= 1:
        return 1                     # Base: 1 way for 0 or 1 steps
    if n not in memo:                # Compute once, store forever
        memo[n] = climb_stairs_memo(n - 1, memo) + climb_stairs_memo(n - 2, memo)
    return memo[n]

def climb_stairs_tab(n: int) -> int:
    if n <= 1:
        return 1
    dp = [0] * (n + 1)               # dp[i] = ways to reach step i
    dp[0], dp[1] = 1, 1              # Base cases
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]  # arrive from i-1 or from i-2
    return dp[n]

def climb_stairs_optimized(n: int) -> int:
    if n <= 1:
        return 1
    prev2, prev1 = 1, 1              # dp[0], dp[1]
    for _ in range(2, n + 1):
        curr = prev1 + prev2         # dp[i] = dp[i-1] + dp[i-2]
        prev2, prev1 = prev1, curr   # slide the two-window forward
    return prev1
```

**Complexity:**
- Time: O(n).
- Space: O(n) for memo/tab; O(1) for the optimized version.

**Common Mistakes & Edge Cases:**
- Using Fibonacci bases (0, 1) instead of (1, 1) — this undercounts by 1 for n >= 1 (e.g., n=2 would give 1 instead of 2).
- Treating dp[0] = 0; the bottom position still counts as "1 way".
- Off-by-one in `range(2, n + 1)` — the last iteration must fill dp[n].
- n = 0 is usually valid in the recurrence; make sure the function handles it (return 1).

### Min Cost Climbing Stairs

**🔗 Practice Link:** [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/)

**Problem Explanation:**
You are on a staircase with a cost array `cost` where `cost[i]` is the price you must pay to step on stair i. You may start on either stair 0 or stair 1 (for free), and from any stair you may climb 1 or 2 steps. "The top" is the floor just beyond the last stair. Return the minimum total cost to reach the top. For example, `cost = [10, 15, 20]`: starting on stair 1 (pay 15) and taking 2 steps to the roof costs 15 total.

**State Definition:**
`dp[i]` = the minimum total cost to step onto stair i (cost paid for stair i included). The final answer is `min(dp[n-1], dp[n-2])` — the roof is reached by a final 1-step from stair n-1 or 2-step from stair n-2.

**Recurrence Relation:**
`dp[i] = cost[i] + min(dp[i-1], dp[i-2])`
You must pay `cost[i]` to land on i, and you arrived from stair i-1 (one step) or i-2 (two steps) — take whichever accumulated cost is smaller.

**Base Cases:**
- `dp[0] = cost[0]` (starting on stair 0)
- `dp[1] = cost[1]` (starting on stair 1)

**Intuition (Why This Works):**
This is a minimization problem with optimal substructure: the cheapest way to stand on stair i is the cheapest way to reach a legal predecessor (i-1 or i-2) plus the unavoidable cost of stair i. Subproblems overlap heavily (dp[i-1] and dp[i-2] are reused constantly), so DP saves an exponential search. The "choice" is which stair you arrive from; choosing the cheaper one is always safe because the cost of stair i is identical no matter how you arrive.

**Step-by-Step Procedure:**
1. Let `n = len(cost)`.
2. Create `dp` of size `n + 1` (index n is a virtual "roof" stair costing 0).
3. Set `dp[0] = cost[0]`, `dp[1] = cost[1]`.
4. Loop `i` from 2 to `n`.
5. For each i, set `step_cost = cost[i] if i < n else 0` (the roof costs nothing).
6. Set `dp[i] = step_cost + min(dp[i-1], dp[i-2])`.
7. Return `dp[n]`.
8. Space-optimize: only the last two dp values are needed — two rolling variables, answer is `min(prev1, prev2)` at the end.
9. Memoized version: `solve(i) = cost[i] + min(solve(i-1), solve(i-2))`, base `solve(i) = cost[i]` for i in {0, 1}, and the driver returns `min(solve(n-1), solve(n-2))`.

**Worked Example (Dry Run):**
`cost = [10, 15, 20]`, n = 3.

| i | cost[i] | dp[i-1] | dp[i-2] | dp[i] = cost[i] + min(...) |
|---|---------|---------|---------|------------------------------|
| 0 | 10      | -       | -       | 10 (start here)              |
| 1 | 15      | -       | -       | 15 (start here)              |
| 2 | 20      | 15      | 10      | 20 + 10 = 30                 |
| 3 | 0 (roof)| 30      | 15      | 0 + min(30, 15) = 15         |

**Answer: 15** — start at stair 1 (pay 15), climb 2 steps to the roof.

**Code:**
```python
def min_cost_climbing_memo(cost: list, i: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if i is None:
        # Top is reached from stair n-1 or n-2; take the cheaper start
        return min(min_cost_climbing_memo(cost, len(cost) - 1, memo),
                   min_cost_climbing_memo(cost, len(cost) - 2, memo))
    if i < 0:
        return 0                     # No stair below index 0
    if i == 0 or i == 1:
        return cost[i]               # Base: you start on stair 0 or 1
    if i not in memo:
        # Pay for stair i, then keep the cheaper predecessor path
        memo[i] = cost[i] + min(min_cost_climbing_memo(cost, i - 1, memo),
                                min_cost_climbing_memo(cost, i - 2, memo))
    return memo[i]

def min_cost_climbing_tab(cost: list) -> int:
    n = len(cost)
    dp = [0] * (n + 1)               # index n = virtual roof stair
    dp[0], dp[1] = cost[0], cost[1]  # Base: starting stair costs its price
    for i in range(2, n + 1):
        step_cost = cost[i] if i < n else 0   # Roof step costs nothing
        dp[i] = step_cost + min(dp[i - 1], dp[i - 2])
    return dp[n]

def min_cost_climbing_optimized(cost: list) -> int:
    prev2, prev1 = cost[0], cost[1]  # dp[0], dp[1]
    for i in range(2, len(cost)):
        # Pay cost[i], add the cheaper of the two previous stair costs
        curr = cost[i] + min(prev1, prev2)
        prev2, prev1 = prev1, curr   # slide window
    # Roof reached from the last stair or the one before it
    return min(prev1, prev2)
```

**Complexity:**
- Time: O(n).
- Space: O(n) for memo/tab; O(1) for optimized.

**Common Mistakes & Edge Cases:**
- Forgetting that the roof is *beyond* the last index — the answer is `min(dp[n-1], dp[n-2])`, not `dp[n-1]`.
- Returning `dp[n-1] + cost[n-1]`-style sums that double-charge the final stair.
- Arrays with only 2 elements: `min(dp[1], dp[0])` still works — don't index dp[2].
- Starting cost semantics: standing on stair 0 or 1 means you already paid that cost (you don't get a free pass onto them).

---

## Maximization DP (Robbery & Painting)

### House Robber I

**🔗 Practice Link:** [House Robber I](https://leetcode.com/problems/house-robber/)

**Problem Explanation:**
You are a robber facing a row of houses. `nums[i]` is the money in house i. If you rob two *adjacent* houses on the same night, the police are alerted, so you may never rob consecutive houses. Return the maximum total money you can steal. For example, `nums = [1, 2, 3, 1]` → the best is 4 (rob house 0 and house 2: 1 + 3).

**State Definition:**
`dp[i]` = the maximum money obtainable from houses 0 through i, respecting the no-adjacent rule.

**Recurrence Relation:**
`dp[i] = max(dp[i-1], dp[i-2] + nums[i])`
At house i you make a binary choice: **skip** it (best up to i-1) or **rob** it (add nums[i] to the best up to i-2, since i-1 becomes unavailable). Take the larger of the two.

**Base Cases:**
- `dp[0] = nums[0]` (only one house to consider)
- `dp[1] = max(nums[0], nums[1])` (rob the richer of the first two)
- In the memoized formulation, `i < 0` returns 0 (nothing before index 0).

**Intuition (Why This Works):**
The decision at each house is independent of *how* the earlier maximum was achieved, only *what* the maximum value is — optimal substructure. The subproblem "best from houses 0..k" is needed for every later house, so caching each one turns an exponential tree of rob/skip choices into a single pass. The key "choice" is rob-or-skip, and both options are fully summarized by dp[i-1] and dp[i-2].

**Step-by-Step Procedure:**
1. If `nums` is empty, return 0.
2. If there is one house, return `nums[0]`.
3. Create `dp` of size `len(nums)`.
4. Set `dp[0] = nums[0]`, `dp[1] = max(nums[0], nums[1])`.
5. Loop `i` from 2 to `len(nums) - 1`.
6. Set `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`.
7. Return `dp[-1]`.
8. Space-optimize: two rolling variables `prev2`, `prev1` (both start at 0 — this automatically handles the empty/single cases).
9. Memoized version: `solve(i) = max(solve(i-1), solve(i-2) + nums[i])`, bases `solve(i<0)=0`, `solve(0)=nums[0]`.

**Worked Example (Dry Run):**
`nums = [1, 2, 3, 1]`.

| i | nums[i] | skip: dp[i-1] | rob: dp[i-2] + nums[i] | dp[i] |
|---|---------|---------------|------------------------|-------|
| 0 | 1       | -             | -                      | 1     |
| 1 | 2       | 1             | 0 + 2 = 2              | 2     |
| 2 | 3       | 2             | 1 + 3 = 4              | 4     |
| 3 | 1       | 4             | 2 + 1 = 3              | 4     |

**Answer: 4** — rob houses 0 and 2 (1 + 3).

**Code:**
```python
def rob_memo(nums: list, i: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if i is None:
        return rob_memo(nums, len(nums) - 1, memo)   # start at the last house
    if i < 0:
        return 0                     # No houses before index 0
    if i == 0:
        return nums[0]               # Base: only house 0 available
    if i not in memo:
        # Either skip house i, or rob it (then house i-1 is forbidden)
        memo[i] = max(rob_memo(nums, i - 1, memo),
                      rob_memo(nums, i - 2, memo) + nums[i])
    return memo[i]

def rob_tab(nums: list) -> int:
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])    # can only rob one of the first two
    for i in range(2, len(nums)):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
    return dp[-1]

def rob_optimized(nums: list) -> int:
    prev2, prev1 = 0, 0              # best up to i-2 and i-1 (0 for empty)
    for num in nums:
        # curr = max(skip current, rob current)
        curr = max(prev1, prev2 + num)
        prev2, prev1 = prev1, curr   # slide window
    return prev1
```

**Complexity:**
- Time: O(n).
- Space: O(n) for memo/tab; O(1) for optimized.

**Common Mistakes & Edge Cases:**
- Empty input (return 0) and single-element input (return nums[0]) — the tab version must guard both before indexing dp[1].
- Thinking the recurrence is `max(nums[i], dp[i-1])` — that double-counts or drops the accumulated best; the correct rob-option is `dp[i-2] + nums[i]`.
- All-negative arrays: the answer is 0 (rob nothing), which falls out naturally from the 0-initialized rolling variables.
- With memoization, forgetting the `i == 0` base causes infinite recursion (i-2 < 0).

### House Robber II (Circular)

**🔗 Practice Link:** [House Robber II](https://leetcode.com/problems/house-robber-ii/)

**Problem Explanation:**
Same rules as House Robber I — no two adjacent houses may be robbed — but now the houses are arranged in a **circle**, so the first house and the last house are adjacent to each other. Given the array `nums`, return the maximum amount you can rob. The circularity means you can never rob both house 0 and house n-1.

**State Definition:**
Reuses the linear House Robber state: `dp[i]` = maximum stealable from a linear stretch of houses 0..i. The circular problem splits into two linear problems on `nums[0:n-1]` (exclude last) and `nums[1:n]` (exclude first).

**Recurrence Relation:**
`answer = max(rob_linear(nums[:-1]), rob_linear(nums[1:]))`
where `rob_linear` uses `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`. Every valid circular plan must exclude either the first or the last house (they can't both be robbed), and each of those exclusions reduces the problem to a normal linear street — taking the better of the two is optimal.

**Base Cases:**
- A single house: `rob_circular` returns `nums[0]` directly.
- Empty input: both linear calls return 0.

**Intuition (Why This Works):**
The circle's only difference from a line is the edge between house 0 and house n-1. That edge is neutralized by removing one endpoint: if you forbid house n-1 you get a line from 0 to n-2, and if you forbid house 0 you get a line from 1 to n-1. Every robber plan respects the circle in at least one of these two reduced lines, and every plan valid in a reduced line is valid in the circle. So the maximum over the two cases is exactly the circular optimum — no more than two linear passes are needed.

**Step-by-Step Procedure:**
1. If `len(nums) == 1`, return `nums[0]`.
2. Write/borrow `rob_linear(arr)` implementing House Robber I with two rolling variables.
3. Compute `a = rob_linear(nums[:-1])` (last house excluded).
4. Compute `b = rob_linear(nums[1:])` (first house excluded).
5. Return `max(a, b)`.
6. Note: an empty or single-element array is handled by step 1 and by the 0-initialization inside `rob_linear`.

**Worked Example (Dry Run):**
`nums = [2, 3, 2]` (houses: 2, 3, 2; house 0 and house 2 are adjacent).

| case | subarray | rob_linear trace | result |
|------|----------|------------------|--------|
| exclude last | [2, 3] | dp0=2, dp1=max(2,3)=3 | 3 |
| exclude first | [3, 2] | dp0=3, dp1=max(3,2)=3 | 3 |

**Answer: 3** — rob the single middle house (value 3). (Robbing 2 + 2 is illegal: those two houses are adjacent in the circle.)

**Code:**
```python
def rob_linear(nums: list) -> int:
    # Standard House Robber I on a straight street, space-optimized
    prev2, prev1 = 0, 0
    for num in nums:
        curr = max(prev1, prev2 + num)  # skip or rob current house
        prev2, prev1 = prev1, curr      # slide window
    return prev1

def rob_circular(nums: list) -> int:
    if len(nums) == 1:
        return nums[0]               # only one house -> rob it
    # Case 1: skip last house. Case 2: skip first house. Best of both.
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

**Complexity:**
- Time: O(n) (two linear passes).
- Space: O(1) (slicing creates copies, so O(n) if you count the slices; use index bounds to avoid).

**Common Mistakes & Edge Cases:**
- Single house `[x]`: both slices would be empty and return 0 — must special-case it.
- Two houses `[a, b]`: answer is `max(a, b)`; the two linear calls produce exactly that.
- Empty input: `nums[:-1]` and `nums[1:]` are both `[]` → 0, which is correct.
- Forgetting that in the circle you also can't rob houses 0 and n-1 *together* even if they're not literally adjacent in the array.

### Paint Fence

**🔗 Practice Link:** [Paint Fence](https://www.geeksforgeeks.org/painting-fence-algorithm)

**Problem Explanation:**
There is a fence with n posts. Each post can be painted with one of k colors. The rule is that **no three adjacent posts may all be the same color** (equivalently, at most two consecutive posts may share a color — a run of 3 identical colors is forbidden). Count the number of ways to paint the fence. (Note: if the rule were "no two adjacent posts share a color," the answer would trivially be `k * (k-1)^(n-1)` and need no DP; the interesting problem, and what this code solves, is the no-three-in-a-row rule.)

**State Definition:**
`total[i]` = number of ways to paint the first i posts. To compute it we track two states:
- `same[i]` = ways where post i has the **same** color as post i-1 (forming a 2-run).
- `diff[i]` = ways where post i has a **different** color than post i-1.

**Recurrence Relation:**
- `same[i] = diff[i-1]`
- `diff[i] = (same[i-1] + diff[i-1]) * (k-1)`
- `total[i] = same[i] + diff[i]`
To paint post i the same as post i-1, post i-1 must have differed from post i-2 (else you'd create a 3-run), so `same[i]` only inherits `diff[i-1]`. To paint post i differently, you may extend any valid previous state, choosing any of the k-1 colors that are not post i-1's color.

**Base Cases:**
- `n == 0` → 0 ways.
- `n == 1` → k ways.
- `same[2] = k`, `diff[2] = k * (k-1)`, so `total[2] = k^2` (any two colors are allowed since a 2-run is fine).

**Intuition (Why This Works):**
The only thing that matters when extending the fence is whether the last two posts form a same-color pair — that single bit of history decides whether the next post may repeat a color. Tracking the count of "same-ending" vs "different-ending" sequences is exactly enough state (optimal substructure over a binary state), and the same sub-counts are reused at every step (overlapping subproblems). The "choice" is which color to give the next post, aggregated into the two counters.

**Step-by-Step Procedure:**
1. If `n == 0`, return 0; if `n == 1`, return k.
2. Initialize `same = k` and `diff = k * (k-1)` (the n = 2 case).
3. Loop `i` from 3 to `n`.
4. `new_same = diff` (only a differing previous pair may be extended into a same pair).
5. `new_diff = (same + diff) * (k-1)` (any state may be extended with a different color).
6. Set `same, diff = new_same, new_diff`.
7. After the loop, return `same + diff`.

**Worked Example (Dry Run):**
n = 4, k = 2 (binary strings of length 4 with no "000" or "111").

| i | same[i] (post i = post i-1) | diff[i] (post i != post i-1) | total |
|---|-----------------------------|------------------------------|-------|
| 2 | 2 (00, 11)                  | 2 (01, 10)                   | 4     |
| 3 | 2                           | (2+2)*(2-1) = 4              | 6     |
| 4 | 4                           | (2+4)*1 = 6                  | 10    |

Verify against brute force: of the 16 binary strings of length 4, the six bad ones are 0000, 0001, 1000, 1111, 1110, 0111, leaving **10** valid strings.

**Code:**
```python
def paint_fence_tab(n: int, k: int) -> int:
    if n == 0:
        return 0                   # No posts, no ways
    if n == 1:
        return k                   # One post: any of k colors
    # For two posts: same-color pair (k ways) + different-color pair (k*(k-1) ways)
    same, diff = k, k * (k - 1)
    for _ in range(3, n + 1):      # Build up from 3 posts to n posts
        new_same = diff            # same-color run can only follow a differing pair
        new_diff = (same + diff) * (k - 1)  # any state + a different color
        same, diff = new_same, new_diff     # roll forward
    return same + diff             # total ways for n posts
```

**Complexity:**
- Time: O(n).
- Space: O(1).

**Common Mistakes & Edge Cases:**
- Misreading the rule as "no two adjacent the same" — that closed-form problem needs no DP; the DP here implements the no-three-in-a-row rule.
- `k == 1` with `n >= 3`: there is no valid coloring, and the recurrence correctly produces 0.
- `n == 2`: the loop must not run (it starts at 3) so `same + diff = k^2` is returned.
- Large n and k: the count grows exponentially; in languages with fixed-width ints apply modulo or use big integers (Python handles this natively).
- Forgetting that a "same" state can only be entered from a "diff" state — this is the heart of the recurrence.

### Paint House I

**🔗 Practice Link:** [Paint House I](https://www.geeksforgeeks.org/minimize-cost-of-painting-n-houses-such-that-adjacent-houses-have-different-colors)

**Problem Explanation:**
There are n houses in a row. Each house can be painted red, green, or blue. `costs[i]` is a triple `[red, green, blue]` giving the cost of painting house i in each color. No two adjacent houses may share a color. Return the minimum total cost to paint every house. For example, `costs = [[17,2,17],[16,16,5],[14,3,19]]` → the minimum is 10 (green, blue, green).

**State Definition:**
`dp[i][c]` = minimum total cost to paint houses 0..i with house i painted color `c` (c in {red, green, blue}).

**Recurrence Relation:**
`dp[i][c] = costs[i][c] + min(dp[i-1][c'])` for every color `c' != c`
House i costs `costs[i][c]` and the previous house may only use a different color, so you add the cheapest valid way to paint the prefix ending in a non-c color.

**Base Cases:**
- `dp[0][red] = costs[0][0]`, `dp[0][green] = costs[0][1]`, `dp[0][blue] = costs[0][2]` (first house has no predecessor).
- Empty input → 0.

**Intuition (Why This Works):**
Each house's optimal cost depends only on the previous house's best costs *for each of the two other colors* — the color of the last house is the only history that matters. Keeping three running values (one per possible color of the current house) fully captures the state (optimal substructure), and those three values are recomputed per house in O(1) (no overlapping recomputation once stored). The "choice" is which color to give the current house, constrained to differ from the previous house's color.

**Step-by-Step Procedure:**
1. If `costs` is empty, return 0.
2. Read the first house's costs into variables `r, g, b` (these hold dp[0]).
3. Loop `i` from 1 to `len(costs) - 1`.
4. Compute `new_r = costs[i][0] + min(g, b)` (house i red, previous green or blue).
5. Compute `new_g = costs[i][1] + min(r, b)`.
6. Compute `new_b = costs[i][2] + min(r, g)`.
7. Replace `r, g, b` with the new values.
8. After the loop, return `min(r, g, b)`.

**Worked Example (Dry Run):**
`costs = [[17,2,17],[16,16,5],[14,3,19]]`.

| i | r = dp[i][red] | g = dp[i][green] | b = dp[i][blue] | how computed |
|---|----------------|------------------|-----------------|--------------|
| 0 | 17             | 2                | 17              | base (first house) |
| 1 | 16 + min(2,17) = 18 | 16 + min(17,17) = 33 | 5 + min(17,2) = 7 | extend with a different color |
| 2 | 14 + min(33,7) = 21 | 3 + min(18,7) = 10 | 19 + min(18,33) = 37 | extend with a different color |

**Answer: min(21, 10, 37) = 10** — paint house 0 green (2), house 1 blue (5), house 2 green (3); 2 + 5 + 3 = 10.

**Code:**
```python
def paint_house_tab(costs: list) -> int:
    if not costs:
        return 0
    # dp for house 0: one variable per possible color of the current house
    r, g, b = costs[0]
    for i in range(1, len(costs)):
        # Paint house i red: must differ from previous, so previous is green or blue
        new_r = costs[i][0] + min(g, b)
        new_g = costs[i][1] + min(r, b)
        new_b = costs[i][2] + min(r, g)
        r, g, b = new_r, new_g, new_b   # roll dp forward to house i
    return min(r, g, b)              # cheapest color for the last house
```

**Complexity:**
- Time: O(n) with a constant factor of 3 colors.
- Space: O(1) (three rolling variables; a full 2D table would be O(n)).

**Common Mistakes & Edge Cases:**
- Allowing the same color on adjacent houses (you must take `min` of the *other two* colors, not all three).
- Single-house input: the loop never runs, and `min(r, g, b)` is the first house's cheapest color — correct.
- Malformed rows (rows with fewer than 3 costs) cause IndexError; assume well-formed input.
- Updating `r`, `g`, `b` one at a time using already-updated values — compute all three new values from the *old* triple before overwriting.

---

## String DP

### Decode Ways

**🔗 Practice Link:** [Decode Ways](https://leetcode.com/problems/decode-ways/)

**Problem Explanation:**
A message is encoded by mapping each letter A–Z to its position: 'A'→'1', 'B'→'2', ..., 'Z'→'26'. Given a string `s` of digits, count how many different ways it can be decoded into letters. A digit can be decoded alone (as long as it is not '0'), or a pair of digits can be decoded as one letter (only if the pair is between 10 and 26 inclusive). Leading zeros are not allowed — e.g., "06" has 0 decodings. Return the integer count.

**State Definition:**
`dp[i]` = number of ways to decode the first i characters, `s[0:i]` (i is the number of characters consumed, from 0 to n).

**Recurrence Relation:**
`dp[i] = dp[i-1]` (if `s[i-1] != '0'`) `+ dp[i-2]` (if `i >= 2` and `10 <= int(s[i-2:i]) <= 26`)
The last character of the prefix either stands alone as a single-digit letter (only legal if it's not '0', leaving `dp[i-1]` ways for the rest) or joins the previous character as a two-digit letter (only legal if that pair is 10–26, leaving `dp[i-2]` ways). The two cases are disjoint and exhaustive.

**Base Cases:**
- `dp[0] = 1` (the empty prefix decodes in exactly one way — by using nothing).
- `dp[1] = 1` if `s[0] != '0'`, else 0.

**Intuition (Why This Works):**
Decoding is a classic "ways to partition a prefix" DP: every decoding of `s[0:i]` ends in exactly one of two ways (last digit alone or last two digits together), so the count is the sum of the counts for the two smaller prefixes. Subproblems are massively overlapping (dp[i-1] and dp[i-2] feed many later cells), and each is computed once. The "choice" is single-digit vs two-digit grouping, filtered by validity checks.

**Step-by-Step Procedure:**
1. If `s` is empty or `s[0] == '0'`, return 0 (no valid decoding).
2. Let `n = len(s)`; create `dp` of size `n + 1`.
3. Set `dp[0] = 1`; set `dp[1] = 1` if `s[0] != '0'` else 0.
4. Loop `i` from 2 to `n`.
5. If `s[i-1] != '0'`, add `dp[i-1]` to `dp[i]` (single-digit decode).
6. If `10 <= int(s[i-2:i]) <= 26`, add `dp[i-2]` to `dp[i]` (two-digit decode).
7. Return `dp[n]`.
8. Space-optimize: only `dp[i-1]` and `dp[i-2]` are needed → two rolling variables.
9. Memoized version: `solve(i)` returns ways to decode `s[0:i]`, with the same recurrence and bases.

**Worked Example (Dry Run):**
`s = "226"`, n = 3.

| i | char s[i-1] | single-digit? (s[i-1] != '0') | two-digit s[i-2:i] (10..26?) | dp[i] |
|---|-------------|-------------------------------|-------------------------------|-------|
| 0 | -           | -                             | -                             | 1     |
| 1 | '2'         | yes → +dp[0]=1                | -                             | 1     |
| 2 | '2'         | yes → +dp[1]=1                | "22" yes → +dp[0]=1           | 2     |
| 3 | '6'         | yes → +dp[2]=2                | "26" yes → +dp[1]=1           | 3     |

**Answer: 3** — "BBF" (2,2,6), "BZ" (2,26), "VF" (22,6).

**Code:**
```python
def num_decodings_memo(s: str, i: int = None, memo=None) -> int:
    if memo is None:
        memo = {}
    if i is None:
        return num_decodings_memo(s, len(s), memo)   # start at the full string
    if i == 0:
        return 1                     # Base: empty prefix decodes one way
    if i < 0:
        return 0                     # Defensive: no negative prefix
    if i in memo:
        return memo[i]
    ways = 0
    if s[i - 1] != '0':              # decode last char alone
        ways += num_decodings_memo(s, i - 1, memo)
    if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:   # decode last two chars together
        ways += num_decodings_memo(s, i - 2, memo)
    memo[i] = ways                   # store before returning
    return memo[i]

def num_decodings_tab(s: str) -> int:
    if not s or s[0] == '0':
        return 0                     # Leading zero can never be decoded
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1                        # empty prefix
    dp[1] = 1 if s[0] != '0' else 0  # first char alone
    for i in range(2, n + 1):
        if s[i - 1] != '0':          # last char forms a 1-digit letter
            dp[i] += dp[i - 1]
        if 10 <= int(s[i - 2:i]) <= 26:   # last two chars form a 2-digit letter
            dp[i] += dp[i - 2]
    return dp[n]

def num_decodings_optimized(s: str) -> int:
    if not s or s[0] == '0':
        return 0
    prev2, prev1 = 1, 1              # dp[0] and dp[1] (dp[1]=1 requires s[0]!='0')
    for i in range(2, len(s) + 1):
        curr = 0
        if s[i - 1] != '0':          # single-digit case
            curr += prev1
        if 10 <= int(s[i - 2:i]) <= 26:   # two-digit case
            curr += prev2
        prev2, prev1 = prev1, curr   # slide window
    return prev1
```

**Complexity:**
- Time: O(n).
- Space: O(n) for memo/tab; O(1) for optimized.

**Common Mistakes & Edge Cases:**
- Strings containing '0': a lone '0' cannot be decoded, and "00", "30", "40" are invalid pairs — the two validity checks handle all of these, returning 0 where appropriate.
- Leading zero ("06", "0"): return 0 immediately; the memo version reaches the same answer via base cases but the guard is simpler.
- `s[i-2:i]` such as "06" must NOT count as a valid two-digit letter (6 < 10) — always check the 10..26 range, not just "not starting with 0".
- Empty string: return 0 (even though dp[0]=1, an empty input has no message).
- Off-by-one: dp[i] decodes s[0:i], so iterate i from 2 to len(s) and index characters at i-1 and i-2.

---

## Subsequence DP

### Maximum Sum of Non-Adjacent Elements

**🔗 Practice Link:** [Maximum Sum of Non-Adjacent Elements](https://www.geeksforgeeks.org/maximum-sum-such-that-no-two-elements-are-adjacent)

**Problem Explanation:**
Given an array of numbers, find the maximum sum of a subsequence in which no two chosen elements are adjacent in the original array. "Subsequence" means you can pick any subset of elements, but you may never pick two elements that sit next to each other. This is exactly the same optimization problem as House Robber I, phrased differently. For example, `nums = [3, 2, 7, 10]` → 13 (pick 3 and 10, which are not adjacent).

**State Definition:**
`dp[i]` = maximum sum of a valid (no-adjacent) selection from the first i elements, `nums[0:i]`.

**Recurrence Relation:**
`dp[i] = max(dp[i-1], dp[i-2] + nums[i])`
At element i, either exclude it (best from the first i elements is the best from the first i-1) or include it (add nums[i] to the best from the first i-2, since element i-1 then becomes forbidden). Same structure as House Robber I.

**Base Cases:**
- `dp[0] = nums[0]`
- `dp[1] = max(nums[0], nums[1])`
- The rolling-variable implementation starts both counters at 0, which makes an empty selection worth 0 (important for all-negative arrays).

**Intuition (Why This Works):**
This is House Robber I under a different name: the only constraint is the adjacency ban, so the same skip/include choice applies at every element, and the best sum for each prefix is reused by all later prefixes (overlapping subproblems + optimal substructure). Storing one number per prefix converts the exponential set of choices into a linear scan.

**Step-by-Step Procedure:**
1. Initialize two rolling variables `prev2 = 0` and `prev1 = 0` (best for the last two prefixes before the current element).
2. Loop over each `num` in `nums`.
3. Compute `curr = max(prev1, prev2 + num)` (skip vs include).
4. Roll: `prev2, prev1 = prev1, curr`.
5. After the loop, return `prev1`.
6. Optionally, implement the explicit `dp` array version (identical to `rob_tab`) for clarity.

**Worked Example (Dry Run):**
`nums = [3, 2, 7, 10]`.

| step | num | prev2 (best i-2) | prev1 (best i-1) | curr = max(prev1, prev2 + num) |
|------|-----|------------------|------------------|--------------------------------|
| start | -  | 0                | 0                | -                              |
| 1    | 3  | 0                | 3                | max(0, 0+3) = 3                |
| 2    | 2  | 3                | 3                | max(3, 0+2) = 3                |
| 3    | 7  | 3                | 10               | max(3, 3+7) = 10               |
| 4    | 10 | 10               | 13               | max(10, 3+10) = 13             |

**Answer: 13** — pick indices 0 and 3 (3 + 10), which are not adjacent.

**Code:**
```python
def max_sum_nonadjacent(nums: list) -> int:
    # Identical to House Robber I: skip current or take it (then skip its neighbor)
    prev2, prev1 = 0, 0              # best sums ending two-back and one-back
    for num in nums:
        # include: prev2 + num  (element i-1 becomes unusable)
        # exclude: prev1
        curr = max(prev1, prev2 + num)
        prev2, prev1 = prev1, curr   # slide window
    return prev1
```

**Complexity:**
- Time: O(n).
- Space: O(1).

**Common Mistakes & Edge Cases:**
- Confusing "subsequence" with "subarray" — elements do not need to be contiguous here.
- All-negative arrays: the code returns 0 (an empty selection), which is the standard convention for this problem; if a non-empty selection is required, special-case it.
- Single-element arrays return that element; empty arrays return 0.
- Using `nums[i-1] + dp[i-2]`-style formulas that accidentally allow picking adjacent elements — the recurrence must skip one position after a pick.

### Longest Increasing Subsequence (O(n²))

**🔗 Practice Link:** [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/)

**Problem Explanation:**
Given an unsorted array of integers, find the length of the **longest increasing subsequence** (LIS). A subsequence keeps elements in their original relative order (skipping allowed) but is not necessarily contiguous, and "increasing" means strictly increasing: each chosen value must be greater than the previous chosen value. For example, in `nums = [10, 9, 2, 5, 3, 7, 101, 18]` the LIS is [2, 5, 7, 101] (or [2, 3, 7, 18]) → length 4.

**State Definition:**
`dp[i]` = length of the longest increasing subsequence that **ends at index i** (i.e., that includes `nums[i]` as its last element).

**Recurrence Relation:**
`dp[i] = max(1, max(dp[j] + 1 for all j < i where nums[j] < nums[i]))`
The LIS ending at i either contains only nums[i] (length 1) or extends the LIS of some earlier index j whose value is smaller than nums[i] — take the longest such chain plus one. The memoized variant below uses the equivalent formulation `f(i, prev)` = longest increasing subsequence starting at index i given that the previous chosen value is `prev`.

**Base Cases:**
- `dp[i] = 1` for every i (a single element is always an increasing subsequence of length 1).
- Empty array → 0.
- Memoized variant: `f(len(nums), prev) = 0` (no elements left).

**Intuition (Why This Works):**
Every LIS ending at i can be split into a smaller LIS (ending at some j < i) plus the element nums[i] — optimal substructure. The same subproblem `dp[j]` is consulted by every later index that has a bigger value, so caching it avoids an exponential search over all subsequences. The "choice" is which earlier index to extend; we only consider j with `nums[j] < nums[i]` because the sequence must stay strictly increasing.

**Step-by-Step Procedure:**
1. If `nums` is empty, return 0.
2. Create `dp` of size n, initialized to all 1s (every element alone is an LIS of length 1).
3. For each `i` from 0 to n-1 (outer loop over the end of the LIS):
4. For each `j` from 0 to i-1 (inner loop over candidate previous elements):
5. If `nums[j] < nums[i]`, update `dp[i] = max(dp[i], dp[j] + 1)`.
6. After both loops, return `max(dp)`.
7. (Memoized variant) `f(i, prev)`: if `i == n` return 0; otherwise return `max(f(i+1, prev), 1 + f(i+1, nums[i]))` when `nums[i] > prev`, else `f(i+1, prev)`; cache on the key `(i, prev)`.

**Worked Example (Dry Run):**
`nums = [10, 9, 2, 5, 3, 7, 101, 18]`.

| i | nums[i] | candidate chains from j < i with nums[j] < nums[i] | dp[i] |
|---|---------|-----------------------------------------------------|-------|
| 0 | 10      | none                                                | 1     |
| 1 | 9       | none (10 < 9 is false)                              | 1     |
| 2 | 2       | none                                                | 1     |
| 3 | 5       | j=2 (2<5): dp[2]+1 = 2                              | 2     |
| 4 | 3       | j=2 (2<3): dp[2]+1 = 2                              | 2     |
| 5 | 7       | j=2: 2; j=3 (5<7): 3; j=4 (3<7): 3                  | 3     |
| 6 | 101     | j=0:2; j=1:2; j=2:2; j=3:3; j=4:3; j=5 (7<101): 4   | 4     |
| 7 | 18      | j=2:2; j=3:3; j=4:3; j=5 (7<18): 4 (101<18? no)     | 4     |

**Answer: max(dp) = 4** (e.g., [2, 5, 7, 101]).

**Code:**
```python
def lis_n2_memo(nums: list, i: int = None, prev: int = None, memo=None) -> int:
    """Memoized: length of LIS from index i onward, given last chosen value prev."""
    if memo is None:
        memo = {}
    if i is None:
        return lis_n2_memo(nums, 0, float('-inf'), memo)  # start: no previous value
    if i == len(nums):
        return 0                     # Base: no elements left to add
    key = (i, prev)
    if key in memo:
        return memo[key]             # reuse cached answer for this state
    taken = 0
    if nums[i] > prev:               # we may take nums[i] (keeps sequence increasing)
        taken = 1 + lis_n2_memo(nums, i + 1, nums[i], memo)
    not_taken = lis_n2_memo(nums, i + 1, prev, memo)  # or skip it
    memo[key] = max(taken, not_taken)
    return memo[key]

def lis_n2_tab(nums: list) -> int:
    if not nums:
        return 0
    n = len(nums)
    dp = [1] * n                     # every element alone is length 1
    for i in range(n):               # i = end of the LIS
        for j in range(i):           # j = candidate previous element
            if nums[j] < nums[i]:    # only extend strictly increasing chains
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)                   # best chain can end anywhere
```

**Complexity:**
- Time: O(n²) — nested loops over pairs (i, j).
- Space: O(n) for the dp array (plus memo cache for the memoized version).

**Common Mistakes & Edge Cases:**
- "Increasing" is *strict*: equal values must not extend a chain (use `<`, not `<=`).
- Returning `dp[-1]` instead of `max(dp)` — the longest chain may not end at the last index.
- Empty array → 0, single element → 1.
- Strictly decreasing arrays (e.g., [5,4,3,2,1]) → 1.
- In the memoized version, the state key must include `prev`; forgetting it merges different states and gives wrong answers.

### Longest Increasing Subsequence (O(n log n) with Patience Sorting)

**🔗 Practice Link:** [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/)

**Problem Explanation:**
Same problem as above — return the length of the longest strictly increasing subsequence — but solved faster with a technique called **patience sorting** (named after the card game). Instead of storing one dp value per index, we maintain a list `piles` where `piles[k]` is the smallest possible tail value of an increasing subsequence of length `k+1`. The final length of `piles` is the LIS length.

**State Definition:**
`piles[k]` = the smallest possible last value of any increasing subsequence of length `k+1` seen so far. (The state is the whole `piles` array, kept sorted — not a scalar dp value.)

**Recurrence Relation:**
For each `num`: find `pos = bisect_left(piles, num)` (first index with `piles[pos] >= num`).
- If `pos == len(piles)`, append `num` (a new, longer LIS tail is possible).
- Else replace `piles[pos] = num` (a smaller tail for the same length is better).
`len(piles)` at the end is the LIS length.
For each length, keeping the *smallest* tail is always at least as good as keeping any larger tail, because a smaller tail gives future (larger) numbers more room to extend the chain — and `bisect_left` finds the exact spot that preserves this property.

**Base Cases:**
- `piles` starts empty.
- Empty array → 0.

**Intuition (Why This Works):**
Each new number either proves there is a chain one element longer than any seen before (it is bigger than every current tail) or improves an existing chain by giving it a smaller tail. Because `piles` is sorted, a binary search (`bisect_left`) locates the update point in O(log n). Note: `bisect_left` (not `bisect_right`) is essential — equal values must not extend the length, keeping the sequence strictly increasing. The answer is the number of piles, which equals the LIS length.

**Step-by-Step Procedure:**
1. Create an empty list `piles`.
2. For each `num` in `nums`:
3. Compute `pos = bisect.bisect_left(piles, num)`.
4. If `pos == len(piles)`, append `num` to `piles`.
5. Else set `piles[pos] = num`.
6. Return `len(piles)`.
7. (Trace check: write down `piles` after each step to confirm it is sorted and each pile is a minimal tail.)

**Worked Example (Dry Run):**
`nums = [10, 9, 2, 5, 3, 7, 101, 18]`.

| step | num | pos (bisect_left) | piles after |
|------|-----|-------------------|-------------|
| 1    | 10  | 0 (append)        | [10] |
| 2    | 9   | 0 (9 < 10, replace) | [9] |
| 3    | 2   | 0 (2 < 9, replace)  | [2] |
| 4    | 5   | 1 (append)        | [2, 5] |
| 5    | 3   | 1 (3 < 5, replace) | [2, 3] |
| 6    | 7   | 2 (append)        | [2, 3, 7] |
| 7    | 101 | 3 (append)        | [2, 3, 7, 101] |
| 8    | 18  | 3 (18 < 101, replace) | [2, 3, 7, 18] |

**Answer: len(piles) = 4.**

**Code:**
```python
import bisect

def lis_nlogn(nums: list) -> int:
    piles = []                       # piles[k] = smallest tail of an LIS of length k+1
    for num in nums:                 # process each element once
        # Find the leftmost pile whose top is >= num (bisect_left keeps it strict)
        pos = bisect.bisect_left(piles, num)
        if pos == len(piles):
            piles.append(num)        # num is bigger than all tails -> longer LIS possible
        else:
            piles[pos] = num         # smaller tail for the same length is better
    return len(piles)                # number of piles = LIS length
```

**Complexity:**
- Time: O(n log n) — n elements, binary search per element.
- Space: O(n) for the `piles` list.

**Common Mistakes & Edge Cases:**
- Using `bisect_right` instead of `bisect_left` — equal values would wrongly extend the length even though the LIS is strictly increasing.
- Confusing `piles` with the actual subsequence: `piles` only tracks minimal tails and lengths; it does not reconstruct the sequence itself.
- The code (as written above) returns only the *length*; reconstructing the actual subsequence requires extra bookkeeping.
- Empty array → 0; duplicates like [2, 2] → 1.
- The `numos` typo (a misspelled loop variable) in older versions of this file caused a NameError — the fixed loop variable is `nums`.

### Number of Longest Increasing Subsequence

**🔗 Practice Link:** [Number of Longest Increasing Subsequence](https://leetcode.com/problems/number-of-longest-increasing-subsequence/)

**Problem Explanation:**
Given an integer array, count how many distinct increasing subsequences achieve the *maximum* LIS length. For example, `nums = [1, 3, 5, 4, 7]` has LIS length 4 and there are 2 such subsequences: [1, 3, 5, 7] and [1, 3, 4, 7]. Return the count.

**State Definition:**
- `lengths[i]` = length of the LIS ending at index i.
- `counts[i]` = number of increasing subsequences of length `lengths[i]` that end at index i.

**Recurrence Relation:**
For each `j < i` with `nums[j] < nums[i]`:
- if `lengths[j] + 1 > lengths[i]`: set `lengths[i] = lengths[j] + 1` and `counts[i] = counts[j]`
- elif `lengths[j] + 1 == lengths[i]`: add `counts[i] += counts[j]`
Every LIS ending at j can be extended with nums[i] to make a chain ending at i; if that new chain is the longest seen, it replaces the count, and if it ties the current best, its count is added.

**Base Cases:**
- `lengths[i] = 1` and `counts[i] = 1` for all i (a subsequence consisting of just nums[i]).
- Empty array → 0.

**Intuition (Why This Works):**
This extends the O(n²) LIS by also tracking *how many* ways each dp value is achieved. Because every extension preserves the "ending at i" property, counts compose: chains ending at i are unions over earlier j of (all chains ending at j) plus nums[i]. Overlapping subproblems are handled by storing both the best length and its multiplicity per index. The final answer sums counts only for indices whose length equals the global maximum.

**Step-by-Step Procedure:**
1. If `nums` is empty, return 0.
2. Initialize `lengths = [1] * n` and `counts = [1] * n`.
3. For each `i` from 0 to n-1:
4. For each `j` from 0 to i-1:
5. If `nums[j] < nums[i]`, compare `lengths[j] + 1` with `lengths[i]`.
6. Update `lengths[i]` and `counts[i]` per the two rules above (replace or accumulate).
7. Compute `max_len = max(lengths)`.
8. Return `sum(counts[i] for i where lengths[i] == max_len)`.

**Worked Example (Dry Run):**
`nums = [1, 3, 5, 4, 7]`.

| i | nums[i] | lengths[i] | counts[i] | how updated |
|---|---------|------------|-----------|-------------|
| 0 | 1       | 1          | 1         | start |
| 1 | 3       | 2          | 1         | j=0: 1<3, 1+1=2 > 1 → lengths=2, counts=counts[0]=1 |
| 2 | 5       | 3          | 1         | j=1: 3<5, 2+1=3 > 2 → lengths=3, counts=counts[1]=1 |
| 3 | 4       | 3          | 1         | j=1: 2+1=3 > 1 → lengths=3, counts=1 (j=2: 5<4? no) |
| 4 | 7       | 4          | 2         | j=2: 3+1=4 > 1 → lengths=4, counts=counts[2]=1; j=3: 3+1=4 == 4 → counts += counts[3] = 2 |

**Answer: max_len = 4; sum counts with length 4 = counts[4] = 2.**

**Code:**
```python
def find_number_of_lis(nums: list) -> int:
    if not nums:
        return 0
    n = len(nums)
    lengths = [1] * n                # length of LIS ending at i
    counts = [1] * n                 # how many such LIS end at i
    for i in range(n):
        for j in range(i):           # extend some earlier chain ending at j
            if nums[j] < nums[i]:    # strictly increasing requirement
                if lengths[j] + 1 > lengths[i]:
                    # A strictly longer chain: adopt j's length and its count
                    lengths[i] = lengths[j] + 1
                    counts[i] = counts[j]
                elif lengths[j] + 1 == lengths[i]:
                    # An equally long chain: accumulate its count
                    counts[i] += counts[j]
    max_len = max(lengths)
    # Total = sum of counts for every index that achieves the max length
    return sum(c for l, c in zip(lengths, counts) if l == max_len)
```

**Complexity:**
- Time: O(n²).
- Space: O(n).

**Common Mistakes & Edge Cases:**
- Only tracking lengths without counts — you must mirror every length update with a count update (replace vs accumulate).
- Counting chains that don't achieve the maximum length — filter by `l == max_len`.
- Strictly increasing requirement: `nums[j] < nums[i]` (not `<=`).
- All-equal arrays, e.g., [2, 2, 2]: every element alone is an LIS of length 1, so the count is n (here 3).
- Empty array → 0 (there are no subsequences at all).

---

## Summary Table

| Problem | Approach | Time | Space |
|---------|----------|------|-------|
| Fibonacci | DP + Optimization | O(n) | O(1) |
| Climbing Stairs | DP + Fibonacci pattern | O(n) | O(1) |
| Min Cost Climbing Stairs | DP + min aggregation | O(n) | O(1) |
| House Robber I | DP with max of previous | O(n) | O(1) |
| House Robber II | Two linear passes | O(n) | O(n) |
| Paint Fence | DP with same/different tracking | O(n) | O(1) |
| Decode Ways | DP with conditional addition | O(n) | O(1) |
| LIS O(n²) | Nested loops DP | O(n²) | O(n) |
| LIS O(n log n) | Patience Sorting | O(n log n) | O(n) |
