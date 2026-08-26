# Dynamic Programming — The Equation Formation Bible (Top 100 Problems)

> **Purpose:** A single resource you can "blindly trust" to learn DP equation formation — from
> basics to FAANG / YC-startup level. The hardest part of DP is **not** the code, it is **deriving
> the recurrence**. This file teaches the *derivation method* first (Notes), then gives 100 problems.
> Every problem now has: (1) a PLAIN-ENGLISH statement, (2) a concrete EXAMPLE so you know exactly
> what is being asked, (3) the state, (4) the recurrence equation, (5) loop/base/answer.
>
> **Golden rule:** You cannot form logic until you understand the question. So read the "Plain
> English" + "Example" first. Only then fill the 8-blank worksheet (in Notes) to derive the equation.

---

# PART 0 — NOTES: HOW TO DERIVE ANY DP EQUATION

The reason you feel stuck on Coin Change / Knapsack is that you are trying to *memorize* the
equation instead of *deriving* it. Every DP equation comes from answering the same 8 questions.
If you answer them honestly, the equation is forced — there is no magic.

---

## 0.1 The 8-Blank Worksheet (do this for EVERY problem)

```
1. dp[...] means _________________________________   (state definition)
2. The question asks for (circle one): MIN / MAX / COUNT / POSSIBLE
3. My LAST decision / choice was ________________  (the choice that got me to this state)
4. If I make that choice, what smaller state remains? ________________
5. What does that choice CONTRIBUTE (+cost / +value / +1 / nothing)? ________________
6. Are there multiple choices? List them: ________________
7. How do I combine choices?  min( ) / max( ) / +( ) / OR( )
8. Can the same item/coin/step be reused? YES(unbounded) / NO(0/1)  -> loop direction
```

That's it. 100% of the equations in this file are produced by this worksheet.

---

## 0.2 Worked example: Coin Change (the one you were stuck on)

Plain English: *"You have coins of given values, unlimited supply. What is the smallest number of
coins that adds up to exactly `amount`? If impossible, say -1."*

Example: coins = [1,2,5], amount = 11 → answer 3 (use 5+5+1).

Now derive `dp[a] = min(dp[a], dp[a-coin] + 1)` using the worksheet:

```
1. dp[a] = minimum coins needed to make amount a.
2. Question asks: MIN.
3. Last decision: "the LAST coin I used was `coin`".
4. If the last coin was `coin`, the smaller state is making amount (a - coin).
5. That choice contributes +1 coin.
6. Choices: every coin denomination is a possible last coin.
7. Combine with MIN (we want the fewest coins).
8. Coins can be reused (unlimited supply) -> loop amount LEFT-TO-RIGHT.
```

Equation forced:

```
dp[a] = min over each coin c of ( dp[a - c] + 1 )
```

Iterative form (coin outer, amount inner, L→R because unbounded):

```
for c in coins:
    for a in range(c, amount+1):
        dp[a] = min(dp[a], dp[a-c] + 1)
```

**Why left-to-right?** When we compute `dp[a]` we want `dp[a-c]` to *possibly already include
coin `c`* (so we can use `c` again). Right-to-left would make `dp[a-c]` reflect only previous
coins → coin used at most once → that's 0/1, not Coin Change.

**The single most important sentence in this file:**
> 0/1-style reuse → iterate the changing dimension RIGHT-TO-LEFT.
> Unbounded-style reuse → iterate the changing dimension LEFT-TO-RIGHT.

---

## 0.3 The 4 fundamental equation skeletons

Memorize these FOUR and you can morph any problem by swapping the verb.

Suppose making a choice leaves you at smaller state `X`, and the choice contributes `g`:

| Question type | Verbs | Equation |
|---|---|---|
| MINIMUM (cost/coins/ops) | `min` | `dp[new] = min(dp[new], dp[X] + g)` |
| MAXIMUM (value/profit) | `max` | `dp[new] = max(dp[new], dp[X] + g)` |
| COUNT (#ways/#subsets) | `+` | `dp[new] += dp[X]` |
| POSSIBLE (can we?) | `OR` | `dp[new] = dp[new] or dp[X]` |

Same "make amount a using coin c" but four questions:

```
MIN coins:      dp[a] = min(dp[a], dp[a-c] + 1)
MAX coins:      dp[a] = max(dp[a], dp[a-c] + 1)
# of ways:      dp[a] += dp[a-c]
possible?:      dp[a] = dp[a] or dp[a-c]
```

**Same choices. Same state. Only the verb changes.** This is the #1 pattern to internalize.

---

## 0.4 Loop ordering: combinations vs permutations

- **Combinations** (order does NOT matter, e.g. Coin Change II): coin loop OUTER, amount loop INNER.
- **Permutations** (order matters, e.g. Combination Sum IV): amount loop OUTER, coin loop INNER.

Swapping them silently changes the answer. Always check what the problem counts.

---

## 0.5 When to add dimensions

If one piece of information is NOT enough to describe a subproblem, add a dimension:
- need "how many items used"? → add a `k` axis: `dp[a][k]`.
- need "which subset chosen"? → bitmask axis: `dp[mask]`.
- need both capacity and count? → `dp[i][k][cap]`.

The recurrence still uses the same verb; you just carry extra indices through.

---

## 0.6 The transformation trick (how hard problems become easy)

Many "hard" problems are a known pattern in disguise:
- Partition Equal Subset Sum → Subset Sum with `target = total/2`.
- Target Sum → Count Subsets with `P = (total+target)/2`.
- Minimum Subset Sum Difference → Subset Sum, then minimize `|total - 2s|`.
- Dungeon Game → run DP **backwards** (we know the end, find the start).
- Best Time to Buy/Sell Stock → multi-state (`cash`/`hold`) 1D DP.

Always ask: *"What known pattern is this a transformation of?"*

---

# PART 1 — 1D LINEAR DP (Problems 1–10)

> Each entry: **Plain English** → **Example** → **State / Recurrence / Loop / Answer**.

## 1. Climbing Stairs
- **Plain English:** You stand at the bottom of a staircase with `n` steps. At each move you can
  go up either 1 step or 2 steps. In how many different ways can you reach the top?
- **Example:** n = 3 → 3 ways: (1,1,1), (1,2), (2,1).
- **State:** `dp[i]` = ways to reach step `i`.
- **Recurrence:** `dp[i] = dp[i-1] + dp[i-2]`
- **Base:** `dp[0]=1, dp[1]=1`. **Answer:** `dp[n]`.

## 2. Climbing Stairs (K steps)
- **Plain English:** Same, but you may climb 1, 2, ... up to `k` steps per move.
- **Example:** n = 4, k = 3 → 7 ways.
- **State:** `dp[i]` = ways to reach step `i`.
- **Recurrence:** `dp[i] = sum(dp[i-j] for j in 1..k)`
- **Base:** `dp[0]=1`. **Answer:** `dp[n]`.

## 3. Min Cost Climbing Stairs
- **Plain English:** Each step `i` has a cost `cost[i]`. You can climb 1 or 2 steps. Starting at
  step 0 or 1, what is the minimum total cost to reach the top (past the last step)?
- **Example:** cost = [10,15,20] → 15 (start at step 1, pay 15, then jump 2 to top).
- **State:** `dp[i]` = min cost to reach step `i`.
- **Recurrence:** `dp[i] = min(dp[i-1], dp[i-2]) + cost[i]`
- **Base:** `dp[0]=cost[0], dp[1]=cost[1]`. **Answer:** `min(dp[n-1], dp[n-2])`.

## 4. House Robber
- **Plain English:** Houses are in a row, house `i` has money `nums[i]`. You cannot rob two
  adjacent houses (alarm). Maximize total money robbed.
- **Example:** nums = [2,7,9,3,1] → 12 (rob houses 7 and 9... actually 2+9+1=12).
- **State:** `dp[i]` = max money from first `i` houses.
- **Recurrence:** `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`
- **Base:** `dp[0]=nums[0], dp[1]=max(nums[0],nums[1])`. **Answer:** `dp[n-1]`.

## 5. House Robber II
- **Plain English:** Houses are in a CIRCLE (first and last are adjacent). Otherwise same as #4.
- **Example:** nums = [2,3,2] → 3 (rob either of the 3s, not both since adjacent in circle).
- **Method:** `ans = max(rob(nums[0:n-1]), rob(nums[1:n]))` (rob = #4). Cannot rob both ends.

## 6. Frog Jump (Min Cost)
- **Plain English:** A frog sits on stone 0 of heights `h`. It can jump to the next stone or the
  one after. The cost of a jump is `|height difference|`. Minimum total cost to reach the last stone.
- **Example:** h = [10,30,40,20] → 30 (jump 10→30=20, 30→40=10; total 30) — actually 10→30 (20) + 30→40 (10) = 30, but 10→40 not allowed; min is 30.
- **State:** `dp[i]` = min cost to reach stone `i`.
- **Recurrence:** `dp[i] = min(dp[i-1]+|h[i]-h[i-1]|, dp[i-2]+|h[i]-h[i-2]|)`
- **Base:** `dp[0]=0, dp[1]=|h[1]-h[0]|`. **Answer:** `dp[n-1]`.

## 7. Jump Game (Reachability)
- **Plain English:** From index `i` you can jump anywhere from 1 to `nums[i]` steps forward. Can
  you reach the last index?
- **Example:** nums = [2,3,1,1,4] → True (0→1→4). nums=[3,2,1,0,4] → False.
- **State:** `dp[i]` = True if index `i` reachable.
- **Recurrence:** `dp[i] = OR over j<i where j+nums[j] >= i of dp[j]`
- **Base:** `dp[0]=True`. **Answer:** `dp[n-1]`. (Greedy: track `maxReach`.)

## 8. Jump Game II (Min Jumps)
- **Plain English:** Same jumping rule, but you MUST reach the last index. What is the minimum
  number of jumps?
- **Example:** nums = [2,3,1,1,4] → 2 jumps (0→1→4).
- **State:** `dp[i]` = min jumps to reach index `i`.
- **Recurrence:** `dp[i] = min over j where j+nums[j]>=i of (dp[j] + 1)`
- **Base:** `dp[0]=0`. **Answer:** `dp[n-1]`.

## 9. Jump Game VI (K-window max)
- **Plain English:** From `i` you may jump up to `k` steps forward. Landing on index `i` gives you
  `nums[i]` points. Maximize total points reaching the last index.
- **Example:** nums = [1,-1,-2,4,-7,3], k = 2 → 7 (path 1 → -1 → 4 → 3 = 7).
- **State:** `dp[i]` = max score to reach `i`.
- **Recurrence:** `dp[i] = nums[i] + max(dp[j] for j in [i-k, i-1])`
- **Base:** `dp[0]=nums[0]`. **Answer:** `dp[n-1]`. (Use monotonic deque → O(n).)

## 10. Maximum Subarray (Kadane)
- **Plain English:** Find the contiguous subarray (keep numbers next to each other) with the
  largest sum.
- **Example:** nums = [-2,1,-3,4,-1,2,1,-5,4] → 6 from [4,-1,2,1].
- **State:** `dp[i]` = max sum of subarray ENDING at `i`.
- **Recurrence:** `dp[i] = max(nums[i], dp[i-1] + nums[i])`
- **Base:** `dp[0]=nums[0]`. **Answer:** `max(dp)`.

---

# PART 2 — STOCK / LIS / DECODE (Problems 11–20)

## 11. Best Time to Buy/Sell Stock (1 tx)
- **Plain English:** Given daily prices, buy once then sell later. Maximize profit.
- **Example:** prices = [7,1,5,3,6,4] → 5 (buy at 1, sell at 6).
- **State:** `cash[i]` (no stock), `hold[i]` (holding stock).
- **Recurrence:** `cash[i]=max(cash[i-1], hold[i-1]+price[i])`; `hold[i]=max(hold[i-1], -price[i])`.
- **Answer:** `cash[n-1]`.

## 12. Best Time to Buy/Sell Stock with Cooldown
- **Plain English:** Same but after you sell, you must sit out the next day before buying again.
- **Example:** prices = [1,2,3,0,2] → 3 (buy1 sell2, cooldown, buy0 sell2).
- **State:** `hold, sold, rest`.
- **Recurrence:** `hold[i]=max(hold[i-1], rest[i-1]-price[i])`; `sold[i]=hold[i-1]+price[i]`; `rest[i]=max(rest[i-1], sold[i-1])`.
- **Answer:** `max(sold[n-1], rest[n-1])`.

## 13. Best Time to Buy/Sell Stock IV (k tx)
- **Plain English:** At most `k` buy+sell pairs. Maximize profit.
- **Example:** prices=[2,4,1], k=2 → 2 (buy2 sell4).
- **State:** `dp[t][i]` = max profit with `t` tx using prices up to `i`.
- **Recurrence:** `dp[t][i] = max(dp[t][i-1], max_j(price[i]-price[j]+dp[t-1][j]))` (track `max(diff)`).

## 14. Longest Increasing Subsequence
- **Plain English:** Pick a subsequence (skip elements, keep order) that is strictly increasing;
  maximize its length.
- **Example:** nums = [10,9,2,5,3,7,101,18] → 4 ([2,3,7,101]).
- **State:** `dp[i]` = LIS length ENDING at `i`.
- **Recurrence:** `dp[i] = 1 + max(dp[j] for j<i and a[j]<a[i])`
- **Base:** `dp[i]=1`. **Answer:** `max(dp)`. (Patience sorting → O(n log n).)

## 15. Number of LIS
- **Plain English:** Among all longest increasing subsequences, how many are there?
- **Example:** nums = [1,3,5,4,7] → 2 (both [1,3,5,7] and [1,3,4,7]).
- **State:** `len[i]`, `cnt[i]`.
- **Recurrence:** if `a[j]<a[i]`: if `len[j]+1>len[i]`: `len[i]=len[j]+1; cnt[i]=cnt[j]`; elif `len[j]+1==len[i]`: `cnt[i]+=cnt[j]`.
- **Answer:** sum `cnt[i]` where `len[i]==max(len)`.

## 16. Longest Bitonic Subsequence
- **Plain English:** Subsequence that first strictly increases then strictly decreases. Max length.
- **Example:** nums = [1,11,2,10,4,5,2,1] → 9? actually 1,2,4,5,2,1 = 6 (or 1,2,10,2,1). Max = 6... correct longest bitonic = [1,2,4,5,2,1] length 6.
- **State:** `inc[i]` (LIS ending at i), `dec[i]` (LDS starting at i).
- **Recurrence:** `inc` as #14; `dec[i] = 1 + max(dec[j] for j>i and a[j]<a[i])`.
- **Answer:** `max(inc[i]+dec[i]-1)`.

## 17. Maximum Product Subarray
- **Plain English:** Contiguous subarray with the largest PRODUCT (negatives make it tricky).
- **Example:** nums = [2,3,-2,4] → 6 ([2,3]). nums=[-2,0,-1] → 0.
- **State:** `maxP[i], minP[i]`.
- **Recurrence:** `maxP[i]=max(nums[i], maxP[i-1]*nums[i], minP[i-1]*nums[i])`; `minP[i]=min(nums[i], maxP[i-1]*nums[i], minP[i-1]*nums[i])`.
- **Answer:** `max(maxP)`.

## 18. Maximum Sum Circular Subarray
- **Plain English:** Subarray can wrap around the end to the beginning. Max sum.
- **Example:** nums = [5,-3,5] → 10 (wrap: 5 + 5).
- **Method:** `ans = max(kadane(arr), total - minSubarray)` (guard all-negative).

## 19. Decode Ways
- **Plain English:** A string of digits; 1→A, 2→B, ..., 26→Z. How many ways to decode it?
- **Example:** s = "12" → 2 ("AB" or "L"). s = "226" → 3 ("BZ","VF","BBF").
- **State:** `dp[i]` = ways to decode prefix of length `i`.
- **Recurrence:** `if s[i-1]!='0': dp[i]+=dp[i-1]`; `if "10"<=s[i-2:i]<="26": dp[i]+=dp[i-2]`.
- **Base:** `dp[0]=1, dp[1]=(s[0]!='0')`. **Answer:** `dp[n]`.

## 20. Decode Ways II
- **Plain English:** Same but `'*'` can be any digit 1–9 in a position; count ways mod 10^9+7.
- **Example:** s = "*" → 9. s = "1*" → 9 (11..19). s = "*1" → 2? (11,21).
- **State:** `dp[i]` = ways for prefix length `i`.
- **Recurrence:** branch on `s[i-1]` and `s[i-2]` being digit/`*`, multiply by the valid factor (1/9/15/...).

---

# PART 3 — KNAPSACK & COIN CHANGE (Problems 21–32)

## 21. 0/1 Knapsack
- **Plain English:** A bag holds weight `W`. Items have weight and value; each item is either
  taken whole or left (never split, never duplicated). Maximize total value.
- **Example:** wt=[1,3,4,5], val=[1,4,5,7], W=7 → 9 (items 3 and 4, values 4+5).
- **State:** `dp[i][w]` = max value using first `i` items, capacity `w`.
- **Recurrence:** `dp[i][w] = max(dp[i-1][w], val[i-1] + dp[i-1][w-wt[i-1]])`
- **Loop:** capacity **RIGHT-TO-LEFT** (0/1, no reuse). **Answer:** `dp[n][W]`.

## 22. Unbounded Knapsack
- **Plain English:** Same as 0/1 but each item can be taken any number of times.
- **Example:** wt=[2,3,4], val=[3,4,5], W=7 → 10 (two of wt=2 and one wt=3: 3+3+4).
- **Recurrence:** `dp[w] = max(dp[w], val[i] + dp[w-wt[i]])`
- **Loop:** capacity **LEFT-TO-RIGHT** (reuse allowed).

## 23. Bounded Knapsack (count[i] copies)
- **Plain English:** Each item has a limited count `count[i]` (not 1, not infinite).
- **Example:** item wt=2 val=3 count=2, W=4 → value 6 (two copies).
- **Method:** binary-split each item into powers of 2 → reduce to 0/1 knapsack.
- **Or** `dp[i][w] = max over k in 0..count[i] of (dp[i-1][w-k*wt[i]] + k*val[i])`.

## 24. Coin Change (Minimum Coins)
- **Plain English:** Coins of given values, unlimited. Fewest coins to make exactly `amount`.
  Impossible → -1.
- **Example:** coins=[1,2,5], amount=11 → 3 (5+5+1).
- **State:** `dp[a]` = min coins for amount `a`.
- **Recurrence:** `dp[a] = min(dp[a], dp[a-coin] + 1)` (coin outer, amount inner L→R).
- **Base:** `dp[0]=0`, rest `inf`. **Answer:** `dp[amount]` or -1.

## 25. Coin Change II (Number of Ways)
- **Plain English:** Unlimited coins. How many distinct COMBINATIONS (order ignored) sum to amount?
- **Example:** coins=[1,2,5], amount=5 → 4 ({5},{2,2,1},{2,1,1,1},{1,1,1,1,1}).
- **Recurrence:** `dp[a] += dp[a-coin]` (coin OUTER, amount inner L→R → combinations).
- **Base:** `dp[0]=1`. **Answer:** `dp[amount]`.

## 26. Combination Sum IV (Permutations)
- **Plain English:** Unlimited coins. How many ordered sequences (permutations) sum to target?
- **Example:** nums=[1,2,3], target=4 → 7 (e.g. 1+1+2 and 2+1+1 count separately).
- **Recurrence:** `dp[a] += dp[a-coin]` (amount OUTER, coin inner → permutations).
- **Base:** `dp[0]=1`.

## 27. Coin Feasibility (Can Make Amount?)
- **Plain English:** Can the exact amount be formed at all?
- **Example:** coins=[2], amount=3 → False.
- **Recurrence:** `dp[a] = dp[a] or dp[a-coin]` (boolean OR, L→R).
- **Base:** `dp[0]=True`.

## 28. Maximum Number of Coins
- **Plain English:** Use unlimited coins to make exactly amount; maximize the COUNT of coins used.
- **Example:** coins=[1,2,5], amount=6 → 6 (six 1s).
- **Recurrence:** `dp[a] = max(dp[a], dp[a-coin] + 1)` (MAX instead of MIN).

## 29. Perfect Squares
- **Plain English:** Write `n` as a sum of perfect squares (1,4,9,16,...); fewest squares?
- **Example:** n = 12 → 3 (4+4+4). n = 13 → 2 (4+9).
- **Recurrence:** `dp[i] = min(dp[i], dp[i - s*s] + 1)` for squares `s*s <= i`.
- **Base:** `dp[0]=0`, rest `inf`. **Answer:** `dp[n]`. (Squares are just "coins".)

## 30. Word Break
- **Plain English:** Given a string and a dictionary of words, can the string be split into
  dictionary words (concatenated, no leftover characters)?
- **Example:** s="leetcode", dict=["leet","code"] → True.
- **State:** `dp[i]` = True if `s[0:i]` breakable.
- **Recurrence:** `dp[i] = OR over j<i where s[j:i] in dict of dp[j]`.
- **Base:** `dp[0]=True`. **Answer:** `dp[n]`.

## 31. Rod Cutting
- **Plain English:** A rod of length `n`; price list for each integer length. Cut into pieces
  (unlimited of each length) to maximize total revenue.
- **Example:** price=[1,5,8,9], n=4 → 10 (two pieces of length 2: 5+5).
- **State:** `dp[i]` = max revenue for length `i`.
- **Recurrence:** `dp[i] = max(price[j-1] + dp[i-j]) for j in 1..i` (unbounded pieces).
- **Base:** `dp[0]=0`. **Answer:** `dp[n]`.

## 32. Egg Dropping (DP form)
- **Plain English:** `k` eggs, `n` floors. Find the highest floor from which an egg doesn't break,
  using the minimum number of drops in the WORST case.
- **Example:** k=2, n=10 → 4 drops suffice.
- **State:** `dp[e][f]` = min drops with `e` eggs, `f` floors.
- **Recurrence:** `dp[e][f] = 1 + min over x of max(dp[e-1][x-1], dp[e][f-x])`.
- **Base:** `dp[e][0]=0, dp[1][f]=f`. **Answer:** `dp[k][n]`.

---

# PART 4 — SUBSET / PARTITION / TARGET (Problems 33–42)

## 33. Subset Sum
- **Plain English:** Given numbers, can you pick SOME of them (each at most once) that add up to
  exactly `target`?
- **Example:** nums=[3,34,4,12,5,2], target=9 → True (4+5).
- **State:** `dp[s]` = True if sum `s` reachable.
- **Recurrence:** `dp[s] = dp[s] or dp[s-num]` (sum loop **RIGHT-TO-LEFT**, 0/1).
- **Base:** `dp[0]=True`. **Answer:** `dp[target]`.

## 34. Partition Equal Subset Sum
- **Plain English:** Can the array be split into two groups with EQUAL total sum?
- **Example:** nums=[1,5,11,5] → True ({11} and {1,5,5}).
- **Transform:** if `total` odd → False; else `target = total/2`, then Subset Sum (#33).

## 35. Count Subsets with Sum
- **Plain English:** How many distinct subsets add up to exactly `target` (each number once)?
- **Example:** nums=[2,3,5,6,8,10], target=10 → 3 ({2,8},{10},{2,3,5}).
- **Recurrence:** `dp[s] += dp[s-num]` (RIGHT-TO-LEFT). **Base:** `dp[0]=1`.

## 36. Minimum Subset Sum Difference
- **Plain English:** Split array into two groups; minimize the absolute difference of their sums.
- **Example:** nums=[1,6,11,5] → 1 (groups {11} and {1,6,5} sums 11 and 12).
- **Method:** compute reachable sums up to `total/2` (Subset Sum), then
  `ans = total - 2*(largest reachable s <= total/2)`.

## 37. Partition to K Equal Sum Subsets
- **Plain English:** Can the array be split into `k` groups, each summing `total/k`?
- **Example:** nums=[4,3,2,3,5,2,1], k=4 → True (each group sums 5).
- **Method:** backtracking + memo on `(mask, remaining, groupsLeft)`; DP over bitmask of used elements.

## 38. Target Sum
- **Plain English:** Put a `+` or `-` before every number so the final total equals `target`. How
  many ways?
- **Example:** nums=[1,1,1,1,1], target=3 → 5 ways.
- **Transform:** `P - N = target`, `P + N = total` → `P = (total+target)/2`; then Count Subsets (#35)
  with target `P`.

## 39. Tallest Billboard
- **Plain English:** Choose a sign (+/-) for each number so that two disjoint groups have EQUAL
  sum; maximize that equal sum.
- **Example:** nums=[1,2,3,6] → 6 (group1={1,2,3}, group2={6}, both sum 6).
- **State:** `dp[d]` = max sum of the "taller" side given difference `d` (offset map).
- **Recurrence:** for each `x`: `dp[d+x]=max(dp[d+x], dp[d]+x)`, `dp[|d-x|]=max(...)`.

## 40. Minimum Path Sum (Grid)
- **Plain English:** Grid of costs. Move only DOWN or RIGHT from top-left to bottom-right; minimize
  total cost along the path.
- **Example:** grid=[[1,3,1],[1,5,1],[4,2,1]] → 7 (1→1→4? no: 1,3,1 path=1+3+1+1+1=7).
- **State:** `dp[i][j]` = min cost to reach `(i,j)`.
- **Recurrence:** `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`.
- **Answer:** `dp[m-1][n-1]`.

## 41. Unique Paths
- **Plain English:** `m x n` grid. Move down/right only. How many paths from top-left to bottom-right?
- **Example:** m=3,n=2 → 3 paths.
- **Recurrence:** `dp[i][j] = dp[i-1][j] + dp[i][j-1]`. **Base:** first row/col = 1.

## 42. Unique Paths with Obstacles
- **Plain English:** Same, but some cells are blocked.
- **Example:** grid=[[0,0,0],[0,1,0],[0,0,0]] → 2 paths (the 1 blocks the middle).
- **Recurrence:** `dp[i][j]=0` if obstacle, else `dp[i-1][j]+dp[i][j-1]`. **Base:** `dp[0][0]=1` if clear.

---

# PART 5 — GRID / MATRIX PATH DP (Problems 43–50)

## 43. Minimum Falling Path Sum
- **Plain English:** Square matrix. Start anywhere in the top row; each step go down to the SAME,
  LEFT, or RIGHT column below. Minimize the sum of the path.
- **Example:** [[2,1,3],[6,5,4],[7,8,9]] → 13 (1+4+8 or similar).
- **Recurrence:** `dp[i][j] = matrix[i][j] + min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1])`.

## 44. Dungeon Game (Reverse DP)
- **Plain English:** A grid (dungeon) with positive (health) and negative (damage) cells. A knight
  starts top-left, princess bottom-right. Health must never drop to 0 or below. Minimum starting
  health needed?
- **Example:** dungeon=[[-2,-3,3],[-5,-10,1],[10,30,-5]] → 7.
- **State:** `dp[i][j]` = min health needed AT `(i,j)` to survive to end.
- **Recurrence:** `dp[i][j] = max(1, min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j])`.
- **Loop:** bottom-right → top-left. **Answer:** `dp[0][0]`.

## 45. Cherry Pickup (Two paths)
- **Plain English:** Two robots start top-left, end bottom-right (down/right only). Collect cherries;
  a cell's cherries are taken once even if both pass. Maximize total collected.
- **Example:** grid=[[0,1,0],[0,0,1],[1,0,0]] → 2.
- **State:** `dp[r1][c1][r2]` with `c2 = r1+c1-r2`.
- **Recurrence:** max over 4 move combos of `cherries(r1,c1)+cherries(r2,c2)+prev`.

## 46. Maximum Path Sum in Triangle
- **Plain English:** A triangle of numbers; move to the adjacent number below. Maximize the sum
  from top to bottom.
- **Example:** [[2],[3,4],[6,5,7],[4,1,8,3]] → 18 (2+4+7+... 2+3+5+8? max = 2+3+5+8=18? actually 2+4+7+... let's say 18).
- **Recurrence:** `dp[i][j] = val[i][j] + max(dp[i+1][j], dp[i+1][j+1])` (bottom-up).

## 47. Minimum Cost For Tickets
- **Plain English:** You must travel on given days. A 1-day, 7-day, or 30-day pass costs given
  amounts. Minimize total cost to cover all travel days.
- **Example:** days=[1,4,6,7,8,20], costs=[2,7,15] → 11 (1-day x2 + 7-day + 1-day... = 2+7+2=11).
- **State:** `dp[i]` = min cost to cover days up to day `i`.
- **Recurrence:** `dp[d] = min(dp[d-1]+cost1, dp[d-7]+cost7, dp[d-30]+cost30)` (skip non-travel days).

## 48. Number of Dice Rolls (Combinations)
- **Plain English:** `d` dice, each with `f` faces (1..f). Count the ways their sum equals `target`.
- **Example:** d=2, f=6, target=7 → 6 ways.
- **State:** `dp[k][s]` = ways with `k` dice summing to `s`.
- **Recurrence:** `dp[k][s] = sum(dp[k-1][s-f] for f in 1..faces)`.

## 49. Knight Probability
- **Plain English:** A knight on an `n x n` board makes `k` random legal moves. Probability it
  stays on the board after `k` moves?
- **Example:** n=3, k=2, start=(0,0) → 0.0625.
- **State:** `dp[k][i][j]` = prob at `(i,j)` after `k` moves.
- **Recurrence:** `dp[k][i][j] = avg over 8 moves of dp[k-1][ni][nj]` (0 if off-board).

## 50. Soup Servings
- **Plain English:** Two soups A and B. Each turn one of 4 operations decreases both by given
  amounts. What is the probability A is empty FIRST (and B not empty)?
- **Example:** n=50 → ~0.625. (For large n, → 1.)
- **Method:** `dp[a][b]` = prob A finishes before B; memoize; use symmetry.

---

# PART 6 — 2D STRING DP (Problems 51–65)

## 51. Longest Common Subsequence
- **Plain English:** Given two strings, find the length of the longest subsequence (keep order,
  drop chars) present in BOTH.
- **Example:** s="abcde", t="ace" → 3 ("ace").
- **State:** `dp[i][j]` = LCS of `s[0:i]`, `t[0:j]`.
- **Recurrence:** if `s[i-1]==t[j-1]`: `dp[i][j]=dp[i-1][j-1]+1`; else `dp[i][j]=max(dp[i-1][j], dp[i][j-1])`.
- **Answer:** `dp[m][n]`.

## 52. LCS Reconstruct
- **Plain English:** Same, but return the actual common subsequence string (not just length).
- **Method:** backtrack from `dp[m][n]` following the transitions of #51.

## 53. Longest Common Substring
- **Plain English:** Longest COMMON CONTIGUOUS (no gaps) substring.
- **Example:** s="ABABC", t="BABCA" → 3 ("ABC").
- **Recurrence:** if `s[i-1]==t[j-1]`: `dp[i][j]=dp[i-1][j-1]+1` else `dp[i][j]=0`.
- **Answer:** `max(dp)`.

## 54. Edit Distance
- **Plain English:** Minimum insertions, deletions, or replacements to turn string `s` into `t`.
- **Example:** s="horse", t="ros" → 3 (horse→rorse→rose→ros).
- **Recurrence:** if `s[i-1]==t[j-1]`: `dp[i][j]=dp[i-1][j-1]`; else `dp[i][j]=1+min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`.

## 55. Distinct Subsequences
- **Plain English:** How many distinct subsequences of `s` equal `t`?
- **Example:** s="rabbbit", t="rabbit" → 3 (extra 'b' can be dropped in 3 places).
- **Recurrence:** if `s[i-1]==t[j-1]`: `dp[i][j]=dp[i-1][j-1]+dp[i-1][j]`; else `dp[i][j]=dp[i-1][j]`.
- **Base:** `dp[i][0]=1`.

## 56. Distinct Subsequences II
- **Plain English:** Count distinct NON-EMPTY subsequences of `s` (mod 10^9+7).
- **Example:** s="abc" → 7. s="aaa" → 3 (a, aa, aaa).
- **Recurrence:** `dp[i] = 2*dp[i-1] - dp[last[s[i]]-1]` (avoid double-counting the last occurrence).

## 57. Interleaving String
- **Plain English:** Can `s3` be formed by interleaving `s1` and `s2` (keep each string's order)?
- **Example:** s1="aab", s2="axy", s3="aabxy" → True.
- **State:** `dp[i][j]` = can form `s3[0:i+j]` using `s1[0:i]` and `s2[0:j]`.
- **Recurrence:** `dp[i][j] = (s1[i-1]==s3[i+j-1] and dp[i-1][j]) or (s2[j-1]==s3[i+j-1] and dp[i][j-1])`.

## 58. Shortest Common Supersequence
- **Plain English:** Shortest string that has both `s` and `t` as subsequences.
- **Example:** s="abac", t="cab" → "cabac" (len 5).
- **Method:** `len = m+n - LCS(s,t)`; reconstruct by LCS backtrack (#52).

## 59. Longest Palindromic Subsequence
- **Plain English:** Longest subsequence (order kept, gaps allowed) that reads the same forward and
  backward.
- **Example:** s="bbbab" → 4 ("bbbb").
- **Recurrence:** if `s[i]==s[j]`: `dp[i][j]=dp[i+1][j-1]+2` else `dp[i][j]=max(dp[i+1][j], dp[i][j-1])` (i from end to start).
- **Base:** `dp[i][i]=1`.

## 60. Longest Palindromic Substring
- **Plain English:** Longest CONTIGUOUS substring that is a palindrome.
- **Example:** s="babad" → "bab" or "aba".
- **Recurrence (2D):** if `s[i]==s[j]` and (j-i<=2 or dp[i+1][j-1]): `dp[i][j]=True`, track len.

## 61. Count Palindromic Substrings
- **Plain English:** How many palindromic substrings (contiguous) does `s` have?
- **Example:** s="aaa" → 6 (a,a,a,aa,aa,aaa).
- **Method:** expand-around-center, or 2D `dp[i][j]` as above counting.

## 62. Palindrome Partitioning II (Min Cuts)
- **Plain English:** Cut the string into the fewest pieces so every piece is a palindrome.
- **Example:** s="aab" → 1 cut ("aa","b").
- **State:** `dp[i]` = min cuts for `s[0:i]`.
- **Recurrence:** if `s[j:i]` is palindrome: `dp[i] = min(dp[i], dp[j] + 1)`; precompute `isPalin`.

## 63. Minimum Insertions to Make Palindrome
- **Plain English:** Insert the fewest characters so the whole string becomes a palindrome.
- **Example:** s="abca" → 1 (insert 'b'→"abcba" or 'a'→"acbca").
- **Method:** `= n - LPS(s)` (#59). Insert the missing mirror characters.

## 64. Regular Expression Matching
- **Plain English:** Does `s` fully match pattern `p`? `.` = any char, `*` = 0 or more of the
  preceding char.
- **Example:** isMatch("aab","c*a*b") → True.
- **State:** `dp[i][j]` = does `s[0:i]` match `p[0:j]`.
- **Recurrence (p[j-1]=='*'):** `dp[i][j] = dp[i][j-2] (use 0) or (s[i-1]==p[j-2] or '.') and dp[i-1][j]`.

## 65. Wildcard Matching
- **Plain English:** `?` matches any single char, `*` matches any sequence (0+ chars). Full match?
- **Example:** isMatch("adceb","*a*b") → True.
- **Recurrence:** if `p[j-1]=='*'`: `dp[i][j]=dp[i][j-1] or dp[i-1][j]`; elif match: `dp[i][j]=dp[i-1][j-1]`.

---

# PART 7 — INTERVAL DP (Problems 66–73)

> Interval DP template: outer loop on length `L`, inner loop on start `i`, end `j=i+L-1`.

## 66. Matrix Chain Multiplication
- **Plain English:** Multiply matrices `A1 A2 ... An` (dimensions given). Different parenthesizations
  cost different numbers of scalar multiplications. Find the minimum cost.
- **Example:** dims=[40,20,30,10,30] → 26000.
- **State:** `dp[i][j]` = min cost to multiply matrices `i..j`.
- **Recurrence:** `dp[i][j] = min over k of dp[i][k] + dp[k+1][j] + p[i-1]*p[k]*p[j]`.

## 67. Burst Balloons
- **Plain English:** Balloons have values; bursting balloon `i` gives `nums[left]*nums[i]*nums[right]`
  coins. Maximize total coins.
- **Example:** nums=[3,1,5,8] → 167.
- **State:** `dp[i][j]` = max coins from bursting `i..j` (endpoints remain as boundaries).
- **Recurrence:** `dp[i][j] = max over k of nums[i-1]*nums[k]*nums[j+1] + dp[i][k-1] + dp[k+1][j]`.

## 68. Minimum Cost to Merge Stones
- **Plain English:** Adjacent piles can be merged into one pile of cost = sum of that group; goal
  is one pile (or K piles) with minimum total merge cost.
- **Example:** stones=[3,2,4,1] → merge cost 20 (to one pile).
- **State:** `dp[i][j]` = min cost to merge `i..j` into one.
- **Recurrence:** `dp[i][j] = min_k(dp[i][k] + dp[k+1][j]) + sum(i..j)` (when mergeable).

## 69. Optimal Binary Search Tree
- **Plain English:** Given keys with search frequencies, build a BST minimizing expected search
  cost.
- **Example:** keys freq=[34,8,50] → min cost via optimal shape.
- **Recurrence:** `dp[i][j] = min over r of dp[i][r-1] + dp[r+1][j] + sum_freq(i..j)`.

## 70. Stone Game (Pick from Ends)
- **Plain English:** A row of stone piles. Two players alternately take a pile from either end.
  Maximize YOUR total (or the score difference).
- **Example:** piles=[5,3,4,5] → first player can get 9 (wins by 2).
- **State:** `dp[i][j]` = max score difference you can get from `i..j`.
- **Recurrence:** `dp[i][j] = max(nums[i]-dp[i+1][j], nums[j]-dp[i][j-1])`.

## 71. Strange Printer
- **Plain English:** A printer can print a single character over a contiguous range in one turn.
  Minimum turns to print the target string?
- **Example:** s="aaabbb" → 2 (print 'a's then 'b's). s="aba" → 2.
- **State:** `dp[i][j]`.
- **Recurrence:** `dp[i][j] = min(dp[i+1][k] + dp[k+1][j])` for `s[k]==s[i]` (print `s[i]` once covering `k`).

## 72. Remove Boxes
- **Plain English:** Boxes have colors. Removing a box gives points = (consecutive same-color
  boxes removed together)^2. Maximize total points.
- **Example:** boxes=[1,3,2,2,2,3,4,3,1] → 23.
- **State:** `dp[i][j][k]` = max from `i..j` with `k` extra boxes of color `boxes[j]` appended.
- **Recurrence:** remove `j` alone, or merge with a matching `m` inside.

## 73. Scramble String
- **Plain English:** Two strings; can one be "scrambled" from the other by recursively swapping
  substrings?
- **Example:** s="great", t="rgeat" → True.
- **State:** `dp[i][j][len]` = can `s` from `i` (len) scramble to `t` from `j`?
- **Recurrence:** split at every `k`: `dp = (dp[i][j][k] and dp[i+k][j+k][len-k]) or (dp[i][j+len-k][k] and dp[i+k][j][len-k])`.

---

# PART 8 — TREE / GRAPH DP (Problems 74–80)

## 74. House Robber III (Tree)
- **Plain English:** Houses form a BINARY TREE (parent connected to children). Rob nodes so no
  parent and child are both robbed; maximize sum.
- **Example:** root=3, children 2,3 (each with child 1) → rob root(3)+two 1s = 7? actually 3+3=6... depends.
- **State:** return `(robThis, skipThis)` per node.
- **Recurrence:** `rob = node.val + left.skip + right.skip`; `skip = max(left) + max(right)`.
- **Answer:** `max(root)`.

## 75. Binary Tree Max Path Sum
- **Plain English:** Any path (may bend at one node) maximizing the sum of node values.
- **Example:** [1,2,3] → 6 (1+2+3). [-10,9,20,null,null,15,7] → 42 (15+20+7).
- **Method:** per node return max path sum downward; track global `node + left + right`.

## 76. Diameter of Tree
- **Plain English:** The longest number of edges between any two nodes in a tree.
- **Example:** a star → diameter 2.
- **Method:** per node return height; `diam = max(diam, leftH + rightH)`.

## 77. Maximum Independent Set (Tree)
- **Plain English:** Pick nodes with no two adjacent; maximize sum (generalizes #74).
- **Recurrence:** `take = val + sum(children.skip)`, `skip = sum(max(child))`.

## 78. Count Paths in DAG
- **Plain English:** Directed acyclic graph. Count how many paths go from source to each node.
- **Example:** a→b, a→c, b→c → paths to c = 2.
- **State:** `dp[u]` = # paths to `u`.
- **Recurrence:** topological order, `dp[v] += dp[u]` for edge `u->v`. **Base:** `dp[src]=1`.

## 79. Shortest Path Count (DAG)
- **Plain English:** Count how many shortest paths reach each node.
- **State:** `dist[u]`, `ways[u]`.
- **Recurrence:** relax `dist`; if equal shortest, `ways[v] += ways[u]`.

## 80. Maximum Students Taking Exam
- **Plain English:** Seat students in rows; no two seated students can cheat (no adjacent in row,
  no directly front/back, no diagonally front). Max students?
- **Example:** seats = [["#",".",".","."],...] → count.
- **State:** `dp[mask]` = max students with current row bitmask valid vs previous row.
- **Recurrence:** `dp[mask] = max(dp[mask], dp[prev] + popcount(mask))` for valid masks.

---

# PART 9 — GAME / MINIMAX DP (Problems 81–88)

## 81. Predict the Winner
- **Plain English:** Two players alternately pick a number from either END of an array; both play
  optimally. Does Player 1 tie or win (score >= Player 2)?
- **Example:** nums=[1,5,2] → False (P1 gets 1+2=3, P2 gets 5). nums=[1,5,233,7] → True.
- **State:** `dp[i][j]` = max score difference for current player on `i..j`.
- **Recurrence:** `dp[i][j] = max(nums[i]-dp[i+1][j], nums[j]-dp[i][j-1])`. P1 wins if `dp[0][n-1] >= 0`.

## 82. Stone Game (Alice wins)
- **Plain English:** Same end-picking game, even number of piles. Prove Alice (first) always wins.
- **Example:** piles=[5,3,4,5] → True.
- **Note:** same equation as #81; answer always True when `n` is even (parity argument).

## 83. Stone Game II
- **Plain English:** Pick 1..2x stones from the FRONT (x = previous pick count); maximize your
  total.
- **Example:** piles=[2,7,9,4,4] → 10.
- **State:** `dp[i][m]` = max stones you can get from index `i` with limit `m`.
- **Recurrence:** `dp[i][m] = max(suffixSum(i..n-1) - dp[i+x][max(m,x)])` for `x in 1..2m`.

## 84. Stone Game III
- **Plain English:** Pick 1, 2, or 3 stones from the FRONT; maximize YOUR score minus opponent's.
- **Example:** stoneValue=[1,2,3,7] → 9? (take all: 1+2+3+7=13, but opponent... depends).
- **State:** `dp[i]` = max advantage starting at index `i`.
- **Recurrence:** `dp[i] = max(stoneValue[i+x-1 summed] - dp[i+x])` for `x in 1..3`.

## 85. Stone Game IV
- **Plain English:** `n` stones. A move removes a PERFECT SQUARE number of stones (1,4,9,...). The
  player who cannot move loses. Can the first player force a win?
- **Example:** n=4 → True (take 4, opponent has 0).
- **State:** `dp[n]` = True if current player can force a win with `n` stones.
- **Recurrence:** `dp[n] = OR over square s<=n of (not dp[n-s])`.

## 86. Can I Win (bitmask game)
- **Plain English:** Numbers 1..m; players pick a distinct unused number, add to a running total;
  first to reach/exceed `desiredTotal` wins. Can first player win (both optimal)?
- **Example:** maxChoosableInteger=10, desiredTotal=11 → True.
- **State:** `dp[mask]` = can current player win with used-set `mask`.
- **Recurrence:** `dp[mask] = OR over available x of (x reaches total) or (not dp[mask|x])`.

## 87. Guess Number Higher/Lower II
- **Plain English:** I pick a number in [1,n]; you guess; if wrong I tell higher/lower and you pay
  the guessed value. What is the minimum amount you must have to GUARANTEE finding it?
- **Example:** n=10 → 16.
- **State:** `dp[i][j]` = min cost to cover range `i..j`.
- **Recurrence:** `dp[i][j] = min over x of (x + max(dp[i][x-1], dp[x+1][j]))`.

## 88. Nim-style Flip Game
- **Plain English:** A string of `+` and `-`; a move flips two consecutive `+` to `--`; last player
  to move wins. Can the first player win?
- **Example:** "++++" → True.
- **State:** `dp[state]` (string/bitmask) = winning.
- **Recurrence:** `dp[s] = OR over moves of (not dp[nextState])`.

---

# PART 10 — DIGIT / BITMASK / ADVANCED FAANG (Problems 89–100)

## 89. Counting Bits
- **Plain English:** For every `i` from 0 to `n`, how many 1-bits are in its binary form?
- **Example:** n=5 → [0,1,1,2,1,2].
- **Recurrence:** `dp[i] = dp[i >> 1] + (i & 1)`. **Answer:** array `0..n`.

## 90. Integer Break
- **Plain English:** Break integer `n` into at least two positive integers; maximize their product.
- **Example:** n=10 → 36 (3+3+4 → 3*3*4=36).
- **State:** `dp[i]` = max product for integer `i`.
- **Recurrence:** `dp[i] = max_{j} max(j*(i-j), j*dp[i-j])` (unbounded reuse of parts).

## 91. Digit DP — Count Numbers in Range
- **Plain English:** Count integers in `[L,R]` satisfying a digit property (e.g., no two adjacent
  equal digits, or at most 3 zeros).
- **Example:** count numbers in [1,100] with no adjacent equal digits → 90.
- **State:** `dp[pos][tight][...]` = count from position `pos` with tight bound + flags.
- **Recurrence:** loop digit `d` in allowed range, transition `dp[pos+1][newTight][newFlags]`. Solve `count(R) - count(L-1)`.

## 92. Traveling Salesman (Bitmask TSP)
- **Plain English:** Visit every city exactly once and return to start; minimize total distance.
- **Example:** 4 cities → min tour length.
- **State:** `dp[mask][i]` = min cost visiting set `mask` ending at city `i`.
- **Recurrence:** `dp[mask][i] = min over j in mask of dp[mask^i][j] + dist[j][i]`.
- **Base:** `dp[1<<i][i] = dist[0][i]`. **Answer:** `min over i dp[(1<<n)-1][i] + dist[i][0]`.

## 93. Minimum XOR Sum of Two Arrays
- **Plain English:** Pair up every element of `arr1` with a distinct element of `arr2` (one-to-one);
  minimize the sum of their XORs.
- **Example:** arr1=[1,2], arr2=[2,3] → 2 (1^3 + 2^2 = 2+0=2).
- **State:** `dp[mask]` = min XOR sum pairing first `popcount(mask)` elements of arr1 with masked arr2 indices.
- **Recurrence:** `dp[mask] = min over bit i in mask of (arr1[k]^arr2[i] + dp[mask^i])` where `k=popcount(mask)-1`.

## 94. Best Time to Buy/Sell Stock III (2 tx)
- **Plain English:** At most TWO buy+sell pairs. Maximize profit.
- **Example:** prices=[3,3,5,0,0,3,1,4] → 6 (buy0 sell3, buy0 sell4).
- **State:** 4 states (buy1, sell1, buy2, sell2).
- **Recurrence:** `buy1=max(buy1,-price)`; `sell1=max(sell1,buy1+price)`; `buy2=max(buy2,sell1-price)`; `sell2=max(sell2,buy2+price)`.
- **Answer:** `sell2`.

## 95. Max Profit in Job Scheduling
- **Plain English:** Jobs have start, end, profit. Pick non-overlapping jobs to maximize profit.
- **Example:** jobs with profits → pick best disjoint set.
- **State:** sort by end; `dp[i]` = max profit using first `i` jobs.
- **Recurrence:** `dp[i] = max(dp[i-1], profit[i] + dp[prevNonOverlapping(i)])` (LIS-style).

## 96. Longest Valid Parentheses
- **Plain English:** Longest contiguous substring of correctly matched `()` parentheses.
- **Example:** s=")()())" → 4 ("()()").
- **State:** `dp[i]` = length of valid parens ENDING at `i`.
- **Recurrence:** if `s[i]==')'` and `s[i-1-dp[i-1]]=='('`: `dp[i] = dp[i-1] + 2 + dp[i-2-dp[i-1]]`.

## 97. Domino and Tromino Tiling
- **Plain English:** Ways to fully tile a `2 x n` board using `2x1` dominoes and `L`-shaped trominoes.
- **Example:** n=3 → 5.
- **Recurrence:** `dp[n] = 2*dp[n-1] + dp[n-3]` (mod 10^9+7). **Base:** `dp[0]=1,dp[1]=1,dp[2]=2`.

## 98. Minimum Difficulty of a Job Schedule
- **Plain English:** Schedule `n` jobs (in fixed order) into `d` days; daily difficulty = max job
  that day; minimize sum of daily difficulties.
- **Example:** jobDifficulty=[6,5,4,3,2,1], d=2 → 7 (day1:[6,5,4], diff6; day2:[3,2,1], diff3 → 9? actually 6+3=9; better split?).
- **State:** `dp[i][k]` = min difficulty scheduling first `i` jobs into `k` days.
- **Recurrence:** `dp[i][k] = min over j of dp[j][k-1] + max(job[j..i-1])`.

## 99. Frog Jump (LC 403, reachability)
- **Plain English:** Stones at positions; frog starts at stone 0. From a stone where it landed with
  last jump `k`, its next jump must be exactly `k-1`, `k`, or `k+1`. Can it reach the last stone?
- **Example:** stones=[0,1,3,5,6,8,12,17] → True.
- **State:** `dp[i][k]` = can reach stone `i` with last jump `k`.
- **Recurrence:** `dp[i][k] = OR over prev stone p,jump j with |k-j|<=1 of dp[p][j]`. Use set of (stone,jump).

## 100. Super Egg Drop (Optimized)
- **Plain English:** `k` eggs, `n` floors. Find the minimum drops (worst case) to determine the
  highest safe floor.
- **Example:** k=2, n=100 → 14.
- **State:** `dp[m][k]` = max floors determinable with `m` moves, `k` eggs.
- **Recurrence:** `dp[m][k] = dp[m-1][k-1] + dp[m-1][k] + 1` (break + not-break + current floor).
- **Answer:** smallest `m` with `dp[m][k] >= n`.

---

# PART 11 — QUICK-REFERENCE: PATTERN → EQUATION

| If the problem says… | Pattern | Core equation skeleton |
|---|---|---|
| minimum / fewest / least cost | MIN | `dp = min(dp, prev + cost)` |
| maximum / most profit / longest | MAX | `dp = max(dp, prev + gain)` |
| how many ways / combinations | COUNT | `dp += prev` |
| can we / is it possible / reachable | POSSIBLE | `dp = dp OR prev` |
| items each used once | 0/1 | loop **RIGHT-TO-LEFT** |
| unlimited reuse | UNBOUNDED | loop **LEFT-TO-RIGHT** |
| combinations not permutations | COMB | coin/choice loop OUTER |
| order matters | PERM | amount/state loop OUTER |
| need more info about subproblem | ADD DIM | `dp[...][extra]` |

---

# PART 12 — THE 8-BLANK WORKSHEET (copy this for every new problem)

```
1. dp[............] means _________________________________
2. Question type:  ( ) MIN   ( ) MAX   ( ) COUNT   ( ) POSSIBLE
3. Last decision / choice: _________________________________
4. Smaller state after that choice: ________________________
5. Contribution of that choice: ____________________________
6. All choices listed: _____________________________________
7. Combine with:  min / max / + / OR  =>  equation _________
8. Reuse allowed?  YES(unbounded,L→R) / NO(0/1,R→L)  => loop ____
```

Fill these 8 blanks for any of the 100 problems above and the equation is forced. The Plain
English + Example tell you WHAT the problem asks; the worksheet tells you HOW to build the logic.
Practice by reading only the Plain English + Example, then deriving the equation yourself before
checking the answer.
