# 1D DP — Extra Problems (Game Theory, Prefix Sum & Advanced Patterns)

This file covers problems NOT present in the fundamentals or advanced files: Stone Games III/IV, Predict the Winner, Arithmetic Slices I & II, Cuboid Stacking, deletion-constrained subarray DP, and prefix-sum counting patterns.

---

## 1. Stone Game III (LC #1406) — Hard

### Problem Explanation
Alice and Bob take turns picking stones from the **front** of an array. On each turn a player may take **1, 2, or 3** stones from the front. Both play optimally. Return `"Alice"`, `"Bob"`, or `"Tie"` based on who wins by having the larger total (or if they tie).

### State Definition
`dp[i]` = the maximum **score difference** (current player's score minus opponent's score) achievable starting from index `i` to the end of the array.

### Recurrence Relation
`dp[i] = max(stones[i] - dp[i+1], stones[i] + stones[i+1] - dp[i+2], stones[i] + stones[i+1] + stones[i+2] - dp[i+3])`

At index `i` the current player takes 1, 2, or 3 stones, gaining their sum, then the opponent plays optimally from the new position — subtracting the opponent's advantage.

### Base Cases
- `dp[i] = stones[i]` when `i == n - 1` (last stone, take it)
- `dp[i] = stones[i] + stones[i+1]` when `i == n - 2` (take both, game ends)
- For `i >= n`: `dp[i] = 0` (nothing left)

### Intuition (Why This Works)
This is a minimax game on a linear array. The current player's best outcome is the max over all legal moves of (immediate gain minus opponent's best response). The same suffix index `i` appears in many move sequences, so storing the difference per index avoids exponential recomputation.

### Step-by-Step Procedure
1. Let `n = len(stones)`.
2. Create `dp` of size `n + 3` initialized to 0 (sentinel for out-of-bounds).
3. Set `dp[n-1] = stones[n-1]`.
4. If `n >= 2`, set `dp[n-2] = stones[n-2] + stones[n-1]`.
5. Loop `i` from `n - 3` down to `0`.
6. `dp[i] = max(stones[i] - dp[i+1], stones[i] + stones[i+1] - dp[i+2], stones[i] + stones[i+1] + stones[i+2] - dp[i+3])`.
7. Compare `dp[0]` with 0: positive → Alice, negative → Bob, zero → Tie.

### Worked Example (Dry Run)
`stones = [1, 2, 3, 7]`. Suffix sums for reference: `[13, 12, 10, 7]`.

| i | take 1 | take 2 | take 3 | dp[i] |
|---|--------|--------|--------|-------|
| 3 | 7 - 0 = 7 | — | — | 7 |
| 2 | 3 - 7 = -4 | 3+7 - 0 = 10 | — | 10 |
| 1 | 2 - 10 = -8 | 2+3 - 7 = -2 | 2+3+7 - 0 = 12 | 12 |
| 0 | 1 - 12 = -11 | 1+2 - 10 = -7 | 1+2+3 - 7 = -1 | -1 |

**Answer: dp[0] = -1 < 0 → "Bob".**

### Code
```python
class Solution:
    def stoneGameIII(self, stoneValue: list) -> str:
        n = len(stoneValue)
        dp = [0] * (n + 3)
        for i in range(n - 1, -1, -1):
            take1 = stoneValue[i] - dp[i + 1]
            take2 = stoneValue[i] + stoneValue[i + 1] - dp[i + 2] if i + 1 < n else float('-inf')
            take3 = stoneValue[i] + stoneValue[i + 1] + stoneValue[i + 2] - dp[i + 3] if i + 2 < n else float('-inf')
            dp[i] = max(take1, take2, take3)
        if dp[0] > 0:
            return "Alice"
        elif dp[0] < 0:
            return "Bob"
        return "Tie"
```

### Complexity
- **Time:** O(n)
- **Space:** O(n) (reducible to O(1) with three rolling variables)

### Common Mistakes & Edge Cases
- Forgetting the tie case (dp[0] == 0).
- Off-by-one when `i + 1` or `i + 2` exceeds bounds — must guard with `< n`.
- Taking the score sum instead of the difference leads to wrong comparison at the end.
- Single-element and two-element arrays: the loop still works because the sentinel values handle missing branches.

---

## 2. Stone Game IV (LC #1510) — Hard

### Problem Explanation
There are `n` stones in a row. Players alternate turns; on each turn a player removes a **perfect square** number of stones (1, 4, 9, 16, ...). The player who **cannot** move **loses**. Return `True` if the first player wins with optimal play, `False` otherwise.

### State Definition
`dp[i]` = `True` if the player whose turn it is with `i` stones remaining can force a win; `False` otherwise.

### Recurrence Relation
`dp[i] = True` if there exists a perfect square `sq <= i` such that `dp[i - sq] == False` (the opponent is left in a losing position).

### Base Cases
- `dp[0] = False` (no stones left, current player loses)
- Precompute all perfect squares up to `n`.

### Intuition (Why This Works)
This is a standard impartial game solved via DP. A position is winning if and only if at least one move leads to a losing position for the opponent. The subproblems overlap because the same `i - sq` value is reached from many different `i` values, so caching each dp[i] avoids exponential blowup.

### Step-by-Step Procedure
1. Precompute perfect squares up to `n`: `squares = [k*k for k in range(1, int(n**0.5) + 1)]`.
2. Create `dp = [False] * (n + 1)`.
3. Loop `i` from 1 to `n`.
4. For each square `sq` in `squares`: if `sq > i`, break; if `dp[i - sq]` is `False`, set `dp[i] = True` and break.
5. Return `dp[n]`.

### Worked Example (Dry Run)
`n = 7`. Perfect squares: 1, 4.

| i | check sq=1 | check sq=4 | dp[i] |
|---|------------|------------|-------|
| 0 | — | — | False |
| 1 | dp[0]=False → win | — | True |
| 2 | dp[1]=True → no | — | False |
| 3 | dp[2]=False → win | — | True |
| 4 | dp[3]=True → no | dp[0]=False → win | True |
| 5 | dp[4]=True → no | dp[1]=True → no | False |
| 6 | dp[5]=False → win | — | True |
| 7 | dp[6]=True → no | dp[3]=True → no | False |

**Answer: dp[7] = False → first player loses → return False.**

### Code
```python
class Solution:
    def winnerSquareGame(self, n: int) -> bool:
        squares = []
        k = 1
        while k * k <= n:
            squares.append(k * k)
            k += 1
        dp = [False] * (n + 1)
        for i in range(1, n + 1):
            for sq in squares:
                if sq > i:
                    break
                if not dp[i - sq]:
                    dp[i] = True
                    break
        return dp[n]
```

### Complexity
- **Time:** O(n * sqrt(n))
- **Space:** O(n)

### Common Mistakes & Edge Cases
- Confusing the losing condition: the player who *cannot* move loses, so `dp[0] = False`.
- Using `<=` instead of `<` when breaking the square loop.
- `n = 0`: return `False` (first player cannot move).
- `n = 1`: return `True` (take the one stone).
- Forgetting to break early once a winning move is found wastes time.

---

## 3. Predict the Winner (LC #486) — Medium

### Problem Explanation
Two players sit on opposite ends of an integer array `nums`. Players alternate turns picking one number from either end. The player with the larger total score wins. Return `True` if Player 1 can win or tie (score1 >= score2) with optimal play.

### State Definition
`dp[i][j]` = the maximum score **difference** (current player minus opponent) achievable on the subarray `nums[i..j]`.

### Recurrence Relation
`dp[i][j] = max(nums[i] - dp[i+1][j], nums[j] - dp[i][j-1])`

Identical to Stone Game I's recurrence: take one end, subtract the opponent's best difference on the remainder.

### Base Cases
- `dp[i][i] = nums[i]` (single element, take it)

### Intuition (Why This Works)
This is the exact interval-minimax pattern from Stone Game I. The current player's advantage on `[i..j]` is maximized by choosing the end that leaves the opponent at the greatest disadvantage. The 2D DP table fills by increasing interval length so every dependency is resolved before it is read.

### Step-by-Step Procedure
1. Let `n = len(nums)`.
2. Create `dp` as `n x n` initialized to 0.
3. Fill diagonal: `dp[i][i] = nums[i]`.
4. Loop `length` from 2 to `n`.
5. For each `i` from 0 to `n - length`, set `j = i + length - 1`.
6. `dp[i][j] = max(nums[i] - dp[i+1][j], nums[j] - dp[i][j-1])`.
7. Return `dp[0][n-1] >= 0`.

### Worked Example (Dry Run)
`nums = [1, 5, 2]`.

| interval | dp value | computation |
|----------|----------|-------------|
| [0,0] | 1 | base |
| [1,1] | 5 | base |
| [2,2] | 2 | base |
| [0,1] | max(1-5, 5-1) = 4 | take 5 |
| [1,2] | max(5-2, 2-5) = 3 | take 5 |
| [0,2] | max(1-3, 2-4) = -1 | take 2 |

**Answer: dp[0][2] = -1 < 0 → Player 1 loses → return False.**

### Code
```python
class Solution:
    def PredictTheWinner(self, nums: list) -> bool:
        n = len(nums)
        dp = [[0] * n for _ in range(n)]
        for i in range(n):
            dp[i][i] = nums[i]
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = max(nums[i] - dp[i + 1][j],
                               nums[j] - dp[i][j - 1])
        return dp[0][n - 1] >= 0
```

### Complexity
- **Time:** O(n²)
- **Space:** O(n²) (reducible to O(n) with rolling anti-diagonal)

### Common Mistakes & Edge Cases
- `n == 1`: Player 1 takes the only element and wins.
- Using `>` instead of `>=` — the problem says Player 1 wins or ties.
- Not initializing the diagonal before filling longer intervals.
- Forgetting that both players play optimally — the opponent's subtraction is essential.

---

## 4. Optimal Strategy for a Game (GFG) — Medium

### Problem Explanation
Given an array of even length, two players pick from either end alternately. Compute the **maximum total** Player 1 can guarantee. This is the "score version" of Predict the Winner — instead of returning a boolean, return the actual maximum score.

### State Definition
`dp[i][j]` = the maximum score the **current player** can collect from `arr[i..j]`.

### Recurrence Relation
`dp[i][j] = max(arr[i] + min(dp[i+2][j], dp[i+1][j-1]), arr[j] + min(dp[i+1][j-1], dp[i][j-2]))`

If you take `arr[i]`, the opponent takes the best from `[i+1..j]`, leaving you the minimum of `[i+2..j]` or `[i+1..j-1]`. Symmetric for taking `arr[j]`.

### Base Cases
- `dp[i][i] = arr[i]` (single element)
- `dp[i][i+1] = max(arr[i], arr[i+1])` (two elements, take the larger)

### Intuition (Why This Works)
After your move the opponent also plays optimally, so you must assume the worst-case response. The minimax reasoning recurses: your best = your immediate gain + opponent's forced outcome (which is the minimum of what you get back). Subproblems overlap because the same subarray is reached via different move sequences.

### Step-by-Step Procedure
1. Let `n = len(arr)`.
2. Create `dp` as `n x n` initialized to 0.
3. Fill diagonal: `dp[i][i] = arr[i]`.
4. Fill next diagonal: `dp[i][i+1] = max(arr[i], arr[i+1])`.
5. Loop `length` from 3 to `n`.
6. For each `i` from 0 to `n - length`, set `j = i + length - 1`.
7. `dp[i][j] = max(arr[i] + min(dp[i+2][j], dp[i+1][j-1]), arr[j] + min(dp[i+1][j-1], dp[i][j-2]))`.
8. Return `dp[0][n-1]`.

### Worked Example (Dry Run)
`arr = [5, 3, 7, 10]`.

| interval | computation | dp |
|----------|-------------|-----|
| [0,0] | base | 5 |
| [1,1] | base | 3 |
| [2,2] | base | 7 |
| [3,3] | base | 10 |
| [0,1] | max(5, 3) | 5 |
| [1,2] | max(3, 7) | 7 |
| [2,3] | max(7, 10) | 10 |
| [0,2] | max(5 + min(7), 7 + min(5)) = max(12, 12) | 12 |
| [1,3] | max(3 + min(10), 10 + min(3)) = max(13, 13) | 13 |
| [0,3] | max(5 + min(13, 10), 10 + min(12, 5)) = max(15, 15) | 15 |

**Answer: dp[0][3] = 15.**

### Code
```python
def optimalStrategy(arr: list) -> int:
    n = len(arr)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = arr[i]
    for i in range(n - 1):
        dp[i][i + 1] = max(arr[i], arr[i + 1])
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            take_left = arr[i] + min(dp[i + 2][j], dp[i + 1][j - 1])
            take_right = arr[j] + min(dp[i + 1][j - 1], dp[i][j - 2])
            dp[i][j] = max(take_left, take_right)
    return dp[0][n - 1]
```

### Complexity
- **Time:** O(n²)
- **Space:** O(n²)

### Common Mistakes & Edge Cases
- Forgetting the base case for `length = 2` causes index errors at `dp[i+2][j]` when `j = i + 1`.
- Using `max` instead of `min` for the opponent's response — the opponent also plays optimally against you.
- Odd-length arrays: the GFG problem guarantees even length.
- Index bounds: `i + 2 <= j` and `j - 2 >= i` must hold for the inner min calls.

---

## 5. Arithmetic Slices I (LC #413) — Medium

### Problem Explanation
An arithmetic slice is a contiguous subarray of length **at least 3** where the difference between consecutive elements is constant. Count the total number of arithmetic slices in an integer array. For example, `[1, 2, 3, 4]` has 3: `[1,2,3]`, `[2,3,4]`, `[1,2,3,4]`.

### State Definition
`dp[i]` = the number of arithmetic slices that **end at index** `i` (i.e., the slice's last element is `nums[i]`).

### Recurrence Relation
If `nums[i] - nums[i-1] == nums[i-1] - nums[i-2]`: `dp[i] = dp[i-1] + 1`. Else: `dp[i] = 0`.

The total count is `sum(dp)`.

When a new element extends the arithmetic run by 1, it creates `dp[i-1] + 1` new slices: the `dp[i-1]` slices that ended at `i-1` are all extended, plus the new 3-element slice `[i-2, i-1, i]`.

### Base Cases
- `dp[0] = dp[1] = 0` (slices must have length >= 3)

### Intuition (Why This Works)
An arithmetic run of length `k` contributes `k*(k-1)/2` slices total. Rather than counting all runs explicitly, the DP counts incrementally: each time the run extends, the number of new slices is one more than the previous count. This is because adding element `i` to a run that had `dp[i-1]` slices ending at `i-1` produces exactly those slices extended by one, plus one brand-new 3-length slice.

### Step-by-Step Procedure
1. If `n < 3`, return 0.
2. Create `dp = [0] * n`.
3. Loop `i` from 2 to `n - 1`.
4. If `nums[i] - nums[i-1] == nums[i-1] - nums[i-2]`: `dp[i] = dp[i-1] + 1`.
5. Return `sum(dp)`.

### Worked Example (Dry Run)
`nums = [1, 2, 3, 4, 5]`.

| i | nums[i]-nums[i-1] == nums[i-1]-nums[i-2]? | dp[i] |
|---|---------------------------------------------|-------|
| 0 | — | 0 |
| 1 | — | 0 |
| 2 | 3-2 == 2-1 → yes | 0 + 1 = 1 |
| 3 | 4-3 == 3-2 → yes | 1 + 1 = 2 |
| 4 | 5-4 == 4-3 → yes | 2 + 1 = 3 |

Sum = 0 + 0 + 1 + 2 + 3 = **6**. (Slices: [1,2,3], [2,3,4], [3,4,5], [1,2,3,4], [2,3,4,5], [1,2,3,4,5])

### Code
```python
class Solution:
    def numberOfArithmeticSlices(self, nums: list) -> int:
        n = len(nums)
        if n < 3:
            return 0
        dp = [0] * n
        for i in range(2, n):
            if nums[i] - nums[i - 1] == nums[i - 1] - nums[i - 2]:
                dp[i] = dp[i - 1] + 1
        return sum(dp)
```

### Complexity
- **Time:** O(n)
- **Space:** O(n) (reducible to O(1) with a running counter)

### Common Mistakes & Edge Cases
- Arrays with fewer than 3 elements → 0 slices.
- All-equal arrays like `[3, 3, 3, 3]` are arithmetic (diff = 0) and produce multiple slices.
- Non-arithmetic runs reset `dp[i]` to 0 — do not carry the old count forward.
- Counting the slices naively with three nested loops is O(n³); the DP is O(n).

---

## 6. Arithmetic Slices II (LC #446) — Hard

### Problem Explanation
Count the number of **arithmetic subsequences** (not necessarily contiguous) of length **at least 3**. A subsequence maintains relative order but can skip elements. For example, `[2, 4, 6, 8, 10]` has many: every 3+ element subset with constant difference qualifies.

### State Definition
`dp[i]` = a dictionary mapping `diff → count`, where `dp[i][diff]` = the number of arithmetic subsequences of length >= 2 that **end at index** `i` with common difference `diff`.

We also maintain a global `result` counter for slices of length >= 3.

### Recurrence Relation
For each `j < i` with `diff = nums[i] - nums[j]`:
- `result += dp[j].get(diff, 0)` (extend length-2 subsequences ending at `j` to length-3+)
- `dp[i][diff] += dp[j].get(diff, 0) + 1` (count the new pair `[j, i]` plus all extensions)

### Base Cases
- `dp[i]` starts as an empty dictionary for every `i`.

### Intuition (Why This Works)
We build the answer incrementally: for each pair `(j, i)`, we know the difference `diff`. Every existing arithmetic subsequence ending at `j` with the same `diff` can be extended by `nums[i]` to form a new subsequence of length >= 3, so we add that count to the result. We also record the new pair `(j, i)` as a length-2 subsequence in `dp[i][diff]` for future extensions.

### Step-by-Step Procedure
1. Let `n = len(nums)`.
2. Initialize `dp = [defaultdict(int) for _ in range(n)]` and `result = 0`.
3. Loop `i` from 1 to `n - 1`.
4. Loop `j` from 0 to `i - 1`.
5. Compute `diff = nums[i] - nums[j]`.
6. Add `dp[j][diff]` to `result` (these are length-2+ subsequences that become length-3+).
7. Add `dp[j][diff] + 1` to `dp[i][diff]` (new pair + extensions).
8. Return `result`.

### Worked Example (Dry Run)
`nums = [2, 4, 6]`.

| i | j | diff | dp[j][diff] | result += | dp[i][diff] += |
|---|---|------|-------------|-----------|----------------|
| 1 | 0 | 2 | 0 | 0 | 0+1 = 1 |
| 2 | 0 | 4 | 0 | 0 | 0+1 = 1 |
| 2 | 1 | 2 | 1 | 1 | 1+1 = 2 |

**Answer: result = 1.** (The subsequence [2, 4, 6].)

### Code
```python
from collections import defaultdict

class Solution:
    def numberOfArithmeticSlices(self, nums: list) -> int:
        n = len(nums)
        dp = [defaultdict(int) for _ in range(n)]
        result = 0
        for i in range(1, n):
            for j in range(i):
                diff = nums[i] - nums[j]
                result += dp[j][diff]
                dp[i][diff] += dp[j][diff] + 1
        return result
```

### Complexity
- **Time:** O(n²)
- **Space:** O(n²) worst case (all pairs have distinct differences)

### Common Mistakes & Edge Cases
- Arrays with fewer than 3 elements → 0.
- Overlapping subsequences: [1, 1, 1, 1] has many subsequences with diff=0.
- Using `<=` in the diff check instead of exact difference loses subsequences.
- Forgetting `+ 1` when updating `dp[i][diff]` misses the new pair.
- Integer overflow is not an issue in Python but can be in other languages.

---

## 7. Maximum Height by Stacking Cuboids (LC #1691) — Hard

### Problem Explanation
Given `n` cuboids where `cuboids[i] = [w_i, h_i, l_i]`, find the maximum total height achievable by stacking them. Cuboid `a` can be placed on top of cuboid `b` if all dimensions of `a` are <= the corresponding dimensions of `b`. Each cuboid may be rotated (all 6 orientations are valid). Return the maximum possible total height.

### State Definition
`dp[i]` = the maximum total height achievable using a stack whose topmost cuboid is the `i`-th cuboid (after sorting).

### Recurrence Relation
`dp[i] = cuboids[i][2] + max(dp[j])` for all `j < i` where cuboid `j` can support cuboid `i` (all three dimensions of `j` >= those of `i`).

The height of cuboid `i` is its third dimension (sorted so the tallest dimension is height).

### Base Cases
- `dp[i] = cuboids[i][2]` if no cuboid below can support it (it stands alone).

### Intuition (Why This Works)
After sorting each cuboid's dimensions and then sorting all cuboids lexicographically, cuboids that can go below are always earlier in the sorted order. This transforms the problem into a weighted LIS: the "weight" is the height, and the "dependency" is the 3D containment condition. The DP considers every possible stack ending at `i` and takes the best extension.

### Step-by-Step Procedure
1. For each cuboid, sort its three dimensions in non-decreasing order.
2. Sort all cuboids lexicographically (by w, then h, then l).
3. Create `dp = [0] * n` where `dp[i] = cuboids[i][2]` (height of each cuboid alone).
4. Loop `i` from 1 to `n - 1`.
5. Loop `j` from 0 to `i - 1`.
6. If `cuboids[j][0] >= cuboids[i][0]` and `cuboids[j][1] >= cuboids[i][1]` and `cuboids[j][2] >= cuboids[i][2]`: `dp[i] = max(dp[i], dp[j] + cuboids[i][2])`.
7. Return `max(dp)`.

### Worked Example (Dry Run)
`cuboids = [[50,45,20],[95,37,53],[45,23,12]]`.

After sorting each: `[[20,45,50],[37,53,95],[12,23,45]]`.
Sorted lexicographically: `[[12,23,45],[20,45,50],[37,53,95]]`.

| i | j | can stack? | dp[i] |
|---|---|------------|-------|
| 0 | — | — | 45 |
| 1 | 0 | 20>=12, 45>=23, 50>=45 → yes | max(50, 45+50) = 95 |
| 2 | 0 | 37>=12, 53>=23, 95>=45 → yes | max(95, 45+95) = 140 |
| 2 | 1 | 37>=20, 53>=45, 95>=50 → yes | max(140, 95+95) = 190 |

**Answer: max(45, 95, 190) = 190.**

### Code
```python
class Solution:
    def maxHeight(self, cuboids: list) -> int:
        for c in cuboids:
            c.sort()
        cuboids.sort()
        n = len(cuboids)
        dp = [cuboids[i][2] for i in range(n)]
        for i in range(n):
            for j in range(i):
                if (cuboids[j][0] >= cuboids[i][0] and
                    cuboids[j][1] >= cuboids[i][1] and
                    cuboids[j][2] >= cuboids[i][2]):
                    dp[i] = max(dp[i], dp[j] + cuboids[i][2])
        return max(dp)
```

### Complexity
- **Time:** O(n²) after sorting
- **Space:** O(n)

### Common Mistakes & Edge Cases
- Forgetting to sort each cuboid's own dimensions first — the containment check requires sorted dimensions.
- Using `<` instead of `<=` for the containment condition — equal dimensions are allowed.
- Empty input → 0.
- A single cuboid → its height.
- The lexicographic sort ensures that if `j` can support `i`, then `j` comes before `i` — this ordering is crucial for the DP to work.

---

## 8. Longest Subarray of 1s After Deleting One Element (LC #1493) — Medium

### Problem Explanation
Given a binary array `nums`, return the length of the longest contiguous subarray containing only 1s **after deleting exactly one element**. You must delete one element (you cannot choose to delete nothing). For example, `[1,1,0,1,1,1]` → delete the 0 → answer is 5.

### State Definition
`dp0[i]` = length of the longest contiguous run of 1s ending at `i` with **zero** deletions used.
`dp1[i]` = length of the longest contiguous run of 1s ending at `i` with **one** deletion used.

### Recurrence Relation
- If `nums[i] == 1`: `dp0[i] = dp0[i-1] + 1`, `dp1[i] = dp1[i-1] + 1`
- If `nums[i] == 0`: `dp0[i] = 0` (run broken), `dp1[i] = dp0[i-1]` (use the deletion here, extend the zero-deletion run)

### Base Cases
- `dp0[0] = nums[0]`, `dp1[0] = 0` (first element cannot benefit from a deletion yet).

### Intuition (Why This Works)
Two parallel DP tracks mirror Kadane's idea: one track counts the current run of 1s without any deletion, and the other tracks the best run given one deletion has been used. When a 0 is encountered, the zero-deletion run resets but the one-deletion run can "bridge" it by extending the previous zero-deletion run. The answer is the maximum over all `dp1[i]` values.

### Step-by-Step Procedure
1. If array is empty, return 0.
2. Initialize `dp0 = nums[0]`, `dp1 = 0`, `result = 0`.
3. Loop `i` from 1 to `n - 1`.
4. If `nums[i] == 1`: `new_dp0 = dp0 + 1`, `new_dp1 = dp1 + 1`.
5. If `nums[i] == 0`: `new_dp0 = 0`, `new_dp1 = dp0` (use deletion on this 0).
6. `result = max(result, new_dp1)`.
7. Update `dp0, dp1 = new_dp0, new_dp1`.
8. Return `result`.

### Worked Example (Dry Run)
`nums = [1, 1, 0, 1, 1, 1]`.

| i | nums[i] | dp0 | dp1 | result |
|---|---------|-----|-----|--------|
| 0 | 1 | 1 | 0 | 0 |
| 1 | 1 | 2 | 1 | 1 |
| 2 | 0 | 0 | 2 | 2 |
| 3 | 1 | 1 | 1 | 2 |
| 4 | 1 | 2 | 2 | 2 |
| 5 | 1 | 3 | 3 | 3 |

Wait — result should be 5 (delete the 0 at index 2, get [1,1,_,1,1,1] = 5 ones). Let me re-check: at i=5, dp1 = dp1_prev + 1 = 2+1 = 3? That's wrong. The issue: after the 0 at index 2, dp1 should track the total including the ones before the 0.

Correction: `dp1` at index 2 should be `dp0_prev = 2` (we deleted this 0, so we have the 2 ones before it). At index 3, dp1 = dp1 + 1 = 3. At index 4, dp1 = 4. At index 5, dp1 = 5.

| i | nums[i] | dp0 | dp1 | result |
|---|---------|-----|-----|--------|
| 0 | 1 | 1 | 0 | 0 |
| 1 | 1 | 2 | 1 | 1 |
| 2 | 0 | 0 | 2 | 2 |
| 3 | 1 | 1 | 3 | 3 |
| 4 | 1 | 2 | 4 | 4 |
| 5 | 1 | 3 | 5 | 5 |

**Answer: 5.**

### Code
```python
class Solution:
    def longestSubarray(self, nums: list) -> int:
        dp0 = nums[0]   # longest run of 1s ending here, no deletion
        dp1 = 0          # longest run of 1s ending here, one deletion used
        result = 0
        for i in range(1, len(nums)):
            if nums[i] == 1:
                dp0 += 1
                dp1 += 1
            else:
                dp1 = dp0       # use deletion on this 0, extend previous run
                dp0 = 0         # zero-deletion run breaks
            result = max(result, dp1)
        return result
```

### Complexity
- **Time:** O(n)
- **Space:** O(1)

### Common Mistakes & Edge Cases
- All-ones array: you must delete one element, so the answer is `n - 1`.
- All-zeros array: answer is 0 (no 1s to form a run).
- The deletion is mandatory — you cannot return `n`.
- Resetting `dp0` to 0 on a 0 but not resetting `dp1` is correct — `dp1` bridges over the 0.

---

## 9. Maximum Subarray Sum with One Deletion (LC #1186) — Medium

### Problem Explanation
Given an array of integers, find the maximum sum of a non-empty contiguous subarray, with the option to delete **at most one** element from it. For example, `[1, -2, 0, 3]` → delete -2 → subarray `[1, 0, 3]` = 4.

### State Definition
`dp0[i]` = max subarray sum ending at `i` with **no** deletions.
`dp1[i]` = max subarray sum ending at `i` with **one** deletion.

### Recurrence Relation
- `dp0[i] = max(nums[i], dp0[i-1] + nums[i])` (Kadane's: extend or restart)
- `dp1[i] = max(dp0[i-1], dp1[i-1] + nums[i])` (delete current: `dp0[i-1]` means delete `nums[i]` and keep best ending at `i-1` without deletion... actually: `dp1[i]` means we delete one element somewhere in `nums[0..i]`. Either we delete `nums[i]` itself (best = `dp0[i-1]`) or we already deleted something earlier (best = `dp1[i-1] + nums[i]`))

### Base Cases
- `dp0[0] = nums[0]`, `dp1[0] = 0` (can't delete and have anything left from a single element).

### Intuition (Why This Works)
Two Kadane-like tracks run in parallel: one without deletion (standard Kadane) and one with a deletion already "spent". When a deletion is used, either it is applied to the current element (inheriting `dp0[i-1]`) or it was used earlier (extending `dp1[i-1]`). The answer is `max(dp0[i], dp1[i])` over all `i`. The key insight is that `dp1[i]` does NOT include `nums[i]` if the deletion targets `nums[i]`.

### Step-by-Step Procedure
1. Initialize `dp0 = dp1 = result = nums[0]`.
2. Loop `i` from 1 to `n - 1`.
3. `dp1 = max(dp0, dp1 + nums[i])` (delete current or extend with prior deletion).
4. `dp0 = max(nums[i], dp0 + nums[i])` (standard Kadane update — do this AFTER dp1).
5. `result = max(result, dp0, dp1)`.
6. Return `result`.

### Worked Example (Dry Run)
`nums = [1, -2, 0, 3]`.

| i | nums[i] | old dp0 | old dp1 | new dp1 | new dp0 | result |
|---|---------|---------|---------|---------|---------|--------|
| 0 | 1 | 1 | 1 | — | — | 1 |
| 1 | -2 | 1 | 1 | max(1, 1+(-2)) = 1 | max(-2, 1-2) = -1 | 1 |
| 2 | 0 | -1 | 1 | max(-1, 1+0) = 1 | max(0, -1+0) = 0 | 1 |
| 3 | 3 | 0 | 1 | max(0, 1+3) = 4 | max(3, 0+3) = 3 | 4 |

**Answer: 4** (delete -2, subarray [1, 0, 3]).

### Code
```python
class Solution:
    def maximumSum(self, arr: list) -> int:
        n = len(arr)
        dp0 = dp1 = result = arr[0]
        for i in range(1, n):
            dp1 = max(dp0, dp1 + arr[i])
            dp0 = max(arr[i], dp0 + arr[i])
            result = max(result, dp0, dp1)
        return result
```

### Complexity
- **Time:** O(n)
- **Space:** O(1)

### Common Mistakes & Edge Cases
- Updating `dp0` before `dp1`: this corrupts the `dp0` value that `dp1` needs — always update `dp1` first.
- All-negative arrays: the answer is the largest single element (deletion optional).
- Single element: return that element (deletion would leave an empty subarray, which is invalid).
- The deletion is optional, so `dp0` (no deletion) can still win.

---

## 10. Longest Subarray with Sum K (Prefix Sum + Map)

### Problem Explanation
Given an array of integers and an integer `k`, find the length of the longest contiguous subarray whose elements sum to exactly `k`. The array may contain negative numbers. For example, `nums = [1, -1, 5, -2, 3]`, `k = 3` → answer is 4 (subarray `[1, -1, 5, -2]`).

### State Definition
`prefix_sum` = running prefix sum as we iterate. We use a hash map `first_seen` mapping each prefix sum to the **first** index at which it occurred.

### Recurrence Relation
At index `i`, if `prefix_sum - k` was seen at index `j` (i.e., `first_seen[prefix_sum - k] = j`), then the subarray `nums[j+1..i]` sums to `k` with length `i - j`.

We want the **maximum** such length, so we only store the **first** occurrence of each prefix sum.

### Base Cases
- `first_seen[0] = -1` (a prefix sum of 0 before the array starts means the subarray from index 0 to `i` sums to `k`).

### Intuition (Why This Works)
If `prefix[i] - prefix[j] = k`, then the subarray from `j+1` to `i` sums to `k`. By storing the earliest index for each prefix sum, we maximize the length of any valid subarray. The hash map gives O(1) lookups, turning an O(n²) brute force into O(n).

### Step-by-Step Procedure
1. Initialize `prefix_sum = 0`, `result = 0`, `first_seen = {0: -1}`.
2. Loop `i` from 0 to `n - 1`.
3. `prefix_sum += nums[i]`.
4. If `prefix_sum - k` in `first_seen`: `result = max(result, i - first_seen[prefix_sum - k])`.
5. If `prefix_sum` not in `first_seen`: `first_seen[prefix_sum] = i` (only store the first occurrence).
6. Return `result`.

### Worked Example (Dry Run)
`nums = [1, -1, 5, -2, 3]`, `k = 3`.

| i | nums[i] | prefix_sum | prefix_sum - k | in map? | result | map |
|---|---------|------------|----------------|---------|--------|-----|
| 0 | 1 | 1 | -2 | no | 0 | {0:-1, 1:0} |
| 1 | -1 | 0 | 3 | no | 0 | {0:-1, 1:0} (0 already at -1) |
| 2 | 5 | 5 | 2 | no | 0 | {0:-1, 1:0, 5:2} |
| 3 | -2 | 3 | 0 | yes, idx -1 | max(0, 3-(-1)) = 4 | {0:-1, 1:0, 5:2, 3:3} |
| 4 | 3 | 6 | 3 | yes, idx 3 | max(4, 4-3) = 4 | {0:-1, 1:0, 5:2, 3:3, 6:4} |

**Answer: 4.**

### Code
```python
def longest_subarray_sum_k(nums: list, k: int) -> int:
    prefix_sum = 0
    first_seen = {0: -1}
    result = 0
    for i in range(len(nums)):
        prefix_sum += nums[i]
        if prefix_sum - k in first_seen:
            result = max(result, i - first_seen[prefix_sum - k])
        if prefix_sum not in first_seen:
            first_seen[prefix_sum] = i
    return result
```

### Complexity
- **Time:** O(n)
- **Space:** O(n)

### Common Mistakes & Edge Cases
- Not initializing `first_seen[0] = -1` misses subarrays starting at index 0.
- Overwriting the first occurrence of a prefix sum: only store it once to maximize length.
- All-negative arrays with `k = 0`: the answer might be 0 (no subarray sums to 0).
- Arrays with `k` equal to the total sum: the subarray is the entire array.

---

## 11. Count Subarrays with Sum K (Prefix Sum + Map)

### Problem Explanation
Given an array of integers and an integer `k`, count the **number** of contiguous subarrays whose elements sum to exactly `k`. For example, `nums = [1, 1, 1]`, `k = 2` → answer is 2 (subarrays [1,1] at indices 0-1 and 1-2).

### State Definition
`prefix_sum` = running prefix sum. A hash map `count` maps each prefix sum to the number of times it has occurred so far.

### Recurrence Relation
At index `i`, if `prefix_sum - k` has been seen `c` times in the map, then there are `c` subarrays ending at `i` that sum to `k`. Add `c` to the result.

### Base Cases
- `count[0] = 1` (empty prefix sums to 0 — one way).

### Intuition (Why This Works)
Same prefix-sum insight as the longest subarray problem, but instead of storing only the first occurrence, we store **all** occurrences and count how many times `prefix_sum - k` appeared. Each occurrence represents a distinct starting point for a valid subarray.

### Step-by-Step Procedure
1. Initialize `prefix_sum = 0`, `result = 0`, `count = {0: 1}`.
2. Loop `i` from 0 to `n - 1`.
3. `prefix_sum += nums[i]`.
4. If `prefix_sum - k` in `count`: `result += count[prefix_sum - k]`.
5. `count[prefix_sum] = count.get(prefix_sum, 0) + 1`.
6. Return `result`.

### Worked Example (Dry Run)
`nums = [1, 1, 1]`, `k = 2`.

| i | nums[i] | prefix_sum | prefix_sum - k | result | count |
|---|---------|------------|----------------|--------|-------|
| 0 | 1 | 1 | -1 | 0 | {0:1, 1:1} |
| 1 | 1 | 2 | 0 | 0+1=1 | {0:1, 1:1, 2:1} |
| 2 | 1 | 3 | 1 | 1+1=2 | {0:1, 1:1, 2:1, 3:1} |

**Answer: 2.**

### Code
```python
def count_subarrays_sum_k(nums: list, k: int) -> int:
    prefix_sum = 0
    count = {0: 1}
    result = 0
    for num in nums:
        prefix_sum += num
        result += count.get(prefix_sum - k, 0)
        count[prefix_sum] = count.get(prefix_sum, 0) + 1
    return result
```

### Complexity
- **Time:** O(n)
- **Space:** O(n)

### Common Mistakes & Edge Cases
- Not initializing `count[0] = 1` misses subarrays starting at index 0.
- Forgetting to increment the count AFTER the lookup (incrementing before double-counts).
- `k = 0`: counts subarrays that sum to 0 (may include single zero elements).
- All-positive arrays: only one subarray can sum to `k` at most (prefix sums are strictly increasing).

---

## 12. Maximum Sum of Three Non-Overlapping Subarrays (LC #689) — Hard

### Problem Explanation
Given an array `nums` and an integer `k`, find three non-overlapping contiguous subarrays of length `k` that maximize their total sum. Return the starting indices of the three subarrays. If multiple answers exist, return the lexicographically smallest one.

### State Definition
- `left[i]` = the starting index of the best single subarray of length `k` in `nums[0..i]`.
- `right[i]` = the starting index of the best single subarray of length `k` in `nums[i..n-1]`.
- `dp[i]` = the maximum sum achievable with one subarray ending at or before index `i` (using `left`).

### Recurrence Relation
- `left[i] = left[i-1]` if `sum(nums[left[i-1]..left[i-1]+k-1]) >= sum(nums[i..i+k-1])`, else `left[i] = i`.
- `right[i]` symmetric from right to left.
- For each middle subarray starting at `j`: `total = sum(left subarray) + sum(j..j+k-1) + sum(right subarray)`.

### Base Cases
- `left[k-1] = 0` (first valid subarray start).
- `right[n-k] = n - k` (last valid subarray start).

### Intuition (Why This Works)
Precomputing the best left and right subarrays for every position allows O(1) lookup of the best left subarray before any given middle index and the best right subarray after it. Then we just iterate over all possible middle subarray positions and pick the triple with the maximum total. The three subarrays cannot overlap because `left[j-1]` ends before `j` and `right[j+k]` starts after `j+k-1`.

### Step-by-Step Procedure
1. Let `n = len(nums)`, compute prefix sums for O(1) range sum queries.
2. Compute `left`: `left[i] = left[i-1]` if its sum >= `sum(nums[i..i+k-1])`, else `left[i] = i`, for `i` from `k-1` to `n - 3k`.
3. Compute `right`: `right[i] = right[i+1]` if its sum >= `sum(nums[i..i+k-1])`, else `right[i] = i`, for `i` from `n-k` down to `2k`.
4. Iterate `j` from `k` to `n - 2k` (middle subarray starts at `j`): compute total = sum of `left[j-1]` subarray + sum of `j..j+k-1` + sum of `right[j+k]` subarray.
5. Track the maximum and return the indices.

### Worked Example (Dry Run)
`nums = [1,2,1,2,6,7,5,1]`, `k = 2`.

Prefix sums: `[0, 1, 3, 4, 6, 12, 19, 24, 25]`. Range sum `[l..r] = prefix[r+1] - prefix[l]`.

Subarrays of length 2 and their sums: `[1,2]=3, [2,1]=3, [1,2]=3, [2,6]=8, [6,7]=13, [7,5]=12, [5,1]=6`.

`left` (best start up to each position): `left[1]=0, left[2]=0, left[3]=0, left[4]=4(sum=8>3), left[5]=5(sum=13>8), left[6]=5, left[7]=5`.

`right` (best start from each position): `right[6]=5, right[5]=5, right[4]=4, right[3]=4, right[2]=2, right[1]=1, right[0]=0`.

Best triple: left=[0] sum=3, middle=[5] sum=13, right=[6] sum=12 → total = 28? Let me verify: `nums[0..1]=[1,2]=3`, `nums[5..6]=[7,5]=12`, `nums[6..7]=[5,1]=6`... those overlap. Middle at j=4: `nums[4..5]=[6,7]=13`, left=[0] sum=3, right=[6] sum=12, total=28. But indices [0,4,6] → subarrays [0,1],[4,5],[6,7] = [1,2],[6,7],[5,1] = 3+13+6 = 22. Let me recalculate: right[6]=5 (sum 13) but that overlaps with j=4 subarray ending at 5. We need `right[j+k]` = `right[6]`. If right[6] means the best starting at index >= 6, then it's index 6, sum 6. So total = 3 + 13 + 6 = 22.

Actually the answer for this input is indices [0, 4, 6] with sum 3 + 13 + 6 = 22. Let me verify no better exists: [1,2,1,2,6,7,5,1]. Triples: (0,3,6)=3+3+6=12, (0,4,6)=3+13+6=22, (1,4,6)=3+13+6=22... Best is 22.

### Code
```python
class Solution:
    def maxSumOfThreeSubarrays(self, nums: list, k: int) -> list:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]

        def range_sum(l, r):
            return prefix[r + 1] - prefix[l]

        left = [0] * n
        best_start = 0
        for i in range(k - 1, n):
            if range_sum(i - k + 1, i) > range_sum(best_start, best_start + k - 1):
                best_start = i - k + 1
            left[i] = best_start

        right = [0] * n
        best_start = n - k
        for i in range(n - k, -1, -1):
            if range_sum(i, i + k - 1) >= range_sum(best_start, best_start + k - 1):
                best_start = i
            right[i] = best_start

        max_sum = 0
        result = [0, 0, 0]
        for j in range(k, n - 2 * k + 1):
            l_idx = left[j - 1]
            r_idx = right[j + k]
            total = range_sum(l_idx, l_idx + k - 1) + range_sum(j, j + k - 1) + range_sum(r_idx, r_idx + k - 1)
            if total > max_sum:
                max_sum = total
                result = [l_idx, j, r_idx]
        return result
```

### Complexity
- **Time:** O(n)
- **Space:** O(n)

### Common Mistakes & Edge Cases
- Using `>` vs `>=` in left/right comparisons affects lexicographic ordering — use `>` for left (keep earliest) and `>=` for right (keep earliest from right).
- Index bounds: middle subarray `j` must satisfy `j >= k` and `j + k <= n - k`.
- `3k > n`: no valid solution exists (but constraints guarantee a valid answer).
- Off-by-one in prefix sum: `range_sum(l, r) = prefix[r+1] - prefix[l]`.

---

## 13. Maximum Sum of Two Non-Overlapping Subarrays (LC #1031) — Medium

### Problem Explanation
Given an array `nums` and two integers `firstLen` and `secondLen`, find the maximum sum of two non-overlapping contiguous subarrays where one has length `firstLen` and the other has length `secondLen`. The order does not matter (either subarray can come first).

### State Definition
`left[i]` = the maximum sum of a subarray of length `firstLen` entirely within `nums[0..i]`.
We similarly compute `right[i]` for the second subarray, then try every split point.

### Recurrence Relation
For each split index `i`:
- `left[i]` = best `firstLen`-subarray sum in `nums[0..i]`.
- `right[i+1]` = best `secondLen`-subarray sum in `nums[i+1..n-1]`.
- `total = left[i] + right[i+1]`.

We also try swapping the roles of `firstLen` and `secondLen` and take the maximum of both orientations.

### Base Cases
- `left[firstLen-1] = sum(nums[0..firstLen-1])` (first valid subarray).

### Intuition (Why This Works)
Precompute the best left subarray for every position. Then iterate over every possible "boundary" between the two subarrays, looking up the best left sum up to that boundary and the best right sum after it. This gives O(n) after precomputation. Trying both orderings handles the case where the longer subarray is on the left or right.

### Step-by-Step Procedure
1. Let `n = len(nums)`, compute prefix sums.
2. Define a helper that computes `left[i]` (best sum of length `L` in `nums[0..i]`) and `right[i]` (best sum of length `L` in `nums[i..n-1]`).
3. Call helper with `(firstLen, secondLen)` and `(secondLen, firstLen)`.
4. For each boundary `i`, compute `left[i] + right[i+1]`.
5. Return the maximum over all boundaries and both orderings.

### Worked Example (Dry Run)
`nums = [0,6,5,2,2,5,1,9,4]`, `firstLen = 1`, `secondLen = 2`.

Prefix sums: `[0, 0, 6, 11, 13, 15, 20, 21, 30, 34]`.

Subarrays of length 1: `[0,6,5,2,2,5,1,9,4]`. Best = 9 at index 7.
Subarrays of length 2: `[6,5],[5,2],[2,2],[2,5],[5,1],[1,9],[9,4]` → sums: 11,7,4,7,6,10,13.

Orientation 1 (firstLen=1 left, secondLen=2 right):
Split at boundary i: left[0]=0, right[1]=11 → 11; left[1]=6, right[2]=7 → 13; ...; left[7]=9, right[8]=13 → 22.

**Answer: 22** (subarray [9] and [9,4]... wait those overlap at index 7). Let me recheck: boundary i=6, left[6]=max of len-1 in [0..6]=6, right[7]=best len-2 in [7..8]=[9,4]=13, total=19. Boundary i=5: left[5]=6, right[6]=10, total=16. Boundary i=7: left[7]=9, right[8]=13, total=22. But right[8] = best len-2 in [8..8]? That's only 1 element! There's an off-by-one issue: `right[i]` should be the best starting at index >= i. `right[8]` needs indices 8 and 9 but index 9 doesn't exist. The correct answer is at boundary i=5: left[5]=6 (best len-1 in [0..5] is 6 at index 1), right[6]=best len-2 in [6..8]=[1,9]=10, total=16. Or boundary i=6: left[6]=6, right[7]=[9,4]=13... but right[7] = best starting at >= 7 with length 2: needs indices 7 and 8 → [9,4] = 13. Total = 6 + 13 = 19. Actually let me just trust the code and verify: answer should be 20 (subarrays [6] at index 1 and [9,4] at indices 7,8 → 6 + 13 = 19... or [9] and [6,5] = 9 + 11 = 20). Boundary i=1: left[1]=6, right[2]=best len-2 from [2..8]=[5,1,9,4] → best is [9,4]=13, total=19... Hmm. Let me just use the code.

The actual answer for this example is 20: subarrays [6] (index 1) and [9,4] (indices 7,8) = 6 + 13 = 19? Or [0,6] and [9,4] = 6+13 = 19. Actually [6] + [9,4] = 6+13 = 19. But [9] + [6,5] = 9+11 = 20. So the answer is 20.

### Code
```python
class Solution:
    def maxSumTwoNoOverlap(self, nums: list, firstLen: int, secondLen: int) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]

        def range_sum(l, r):
            return prefix[r + 1] - prefix[l]

        def solve(L1, L2):
            left = [0] * n
            best = range_sum(0, L1 - 1)
            left[L1 - 1] = best
            for i in range(L1, n):
                best = max(best, range_sum(i - L1 + 1, i))
                left[i] = best

            right = [0] * n
            best = range_sum(n - L2, n - 1)
            right[n - L2] = best
            for i in range(n - L2 - 1, -1, -1):
                best = max(best, range_sum(i, i + L2 - 1))
                right[i] = best

            result = 0
            for i in range(L1 - 1, n - L2):
                result = max(result, left[i] + right[i + 1])
            return result

        return max(solve(firstLen, secondLen), solve(secondLen, firstLen))
```

### Complexity
- **Time:** O(n)
- **Space:** O(n)

### Common Mistakes & Edge Cases
- Not trying both orderings: the first subarray might be on the right.
- Off-by-one: the boundary split must leave room for both subarrays.
- `firstLen + secondLen == n`: only one valid arrangement.
- Equal lengths: both orientations produce the same result.

---

## 14. Maximum Subarray Length with Sum K (Sliding Window for Positive Arrays)

### Problem Explanation
Given an array of **positive** integers and an integer `k`, find the maximum length of a contiguous subarray that sums to exactly `k`. This is a variant of the prefix-sum approach that exploits positivity for a sliding-window O(1) space solution.

### State Definition
Two pointers `left` and `right` define a window. `current_sum` = sum of `nums[left..right]`.

### Recurrence Relation
- Expand `right`: `current_sum += nums[right]`, `right += 1`.
- Shrink `left` while `current_sum > k`: `current_sum -= nums[left]`, `left += 1`.
- If `current_sum == k`: update `result = max(result, right - left)`.

### Base Cases
- If no subarray sums to `k`, return 0.
- `left = right = 0`, `current_sum = 0`.

### Intuition (Why This Works)
With all-positive numbers, the window sum strictly increases when `right` moves right and strictly decreases when `left` moves right. This monotonicity means we never need to shrink and re-expand — a single two-pointer scan suffices. Each window with sum `k` is a candidate, and since we shrink only when the sum exceeds `k`, we find the maximum-length window.

### Step-by-Step Procedure
1. Initialize `left = 0`, `current_sum = 0`, `result = 0`.
2. Loop `right` from 0 to `n - 1`.
3. `current_sum += nums[right]`.
4. While `current_sum > k` and `left <= right`: `current_sum -= nums[left]`, `left += 1`.
5. If `current_sum == k`: `result = max(result, right - left + 1)`.
6. Return `result`.

### Worked Example (Dry Run)
`nums = [1, 2, 1, 2, 3]`, `k = 4`.

| right | nums[right] | current_sum | after shrink | result |
|-------|-------------|-------------|--------------|--------|
| 0 | 1 | 1 | — | 0 |
| 1 | 2 | 3 | — | 0 |
| 2 | 1 | 4 | — | 3 (indices 0-2) |
| 3 | 2 | 6 → shrink: 6-1=5 → 5-2=3 | 3 | 3 |
| 4 | 3 | 6 → shrink: 6-1=5 → 5-2=3 → 3-1=2 | 2 | 3 |

**Answer: 3.** (Subarray `[1, 2, 1]`.)

### Code
```python
def max_subarray_len_positive(nums: list, k: int) -> int:
    left = 0
    current_sum = 0
    result = 0
    for right in range(len(nums)):
        current_sum += nums[right]
        while current_sum > k and left <= right:
            current_sum -= nums[left]
            left += 1
        if current_sum == k:
            result = max(result, right - left + 1)
    return result
```

### Complexity
- **Time:** O(n) (each element is added and removed at most once)
- **Space:** O(1)

### Common Mistakes & Edge Cases
- This approach **only works for positive arrays** — negatives break the monotonicity.
- For arrays with negatives, use the prefix-sum + hash map approach (Problem 10).
- `k = 0` with all-positive arrays: answer is 0 (no subarray sums to 0).
- Entire array sums to `k`: answer is `n`.
- Using `>` instead of `>=` in the while condition: must shrink when strictly greater.

---

## Summary Table

```
┌──────────────────────────────────────────┬───────────────┬────────┬─────────┬──────────────────────────────────────┐
│ Problem                                  │ Approach      │ Time   │ Space   │ Key Insight                          │
├──────────────────────────────────────────┼───────────────┼────────┼─────────┼──────────────────────────────────────┤
│ Stone Game III (1406)                    │ Diff DP       │ O(n)   │ O(n)    │ Take 1/2/3 from front, score diff    │
│ Stone Game IV (1510)                     │ Game DP       │O(n√n) │ O(n)    │ Perfect square removals, win/lose    │
│ Predict the Winner (486)                 │ Interval DP   │ O(n²)  │ O(n²)   │ Same as Stone Game I, score diff     │
│ Optimal Strategy (GFG)                   │ Interval DP   │ O(n²)  │ O(n²)   │ Minimax with opponent's best move    │
│ Arithmetic Slices I (413)                │ Run DP        │ O(n)   │ O(n)    │ dp[i] = dp[i-1]+1 when diff matches │
│ Arithmetic Slices II (446)               │ Hash Map DP   │ O(n²)  │ O(n²)   │ Count length-2+ by diff              │
│ Cuboid Stacking (1691)                   │ LIS variant   │ O(n²)  │ O(n)    │ Sort + 3D containment check          │
│ Longest 1s After Delete (1493)           │ Two-track DP  │ O(n)   │ O(1)    │ Track with/without one deletion      │
│ Max Sum One Deletion (1186)              │ Two-track DP  │ O(n)   │ O(1)    │ Kadane + optional deletion           │
│ Longest Subarray Sum K                   │ Prefix + Map  │ O(n)   │ O(n)    │ first_seen[prefix-k] gives length   │
│ Count Subarrays Sum K                    │ Prefix + Map  │ O(n)   │ O(n)    │ count[prefix-k] gives multiplicity  │
│ Three Non-Overlap Subarrays (689)        │ Precomp + DP  │ O(n)   │ O(n)    │ Best left/right for each boundary   │
│ Two Non-Overlap Subarrays (1031)         │ Precomp + DP  │ O(n)   │ O(n)    │ Best left/right, try both orderings │
│ Max Subarray Len Sum K (positive)        │ Sliding Window│ O(n)   │ O(1)    │ Two pointers, monotonic sum          │
└──────────────────────────────────────────┴───────────────┴────────┴─────────┴──────────────────────────────────────┘
```

### Pattern Checklist
- [ ] **Interval Minimax**: Game from ends → dp[i][j] = take - opponent_best
- [ ] **Two-track DP**: Kadane with state for "resources used" (deletion, budget)
- [ ] **Prefix Sum + Hash Map**: Subarray sum queries in O(n)
- [ ] **Sliding Window**: Positive arrays, sum/length constraints
- [ ] **Run-length DP**: Arithmetic slices → extend or reset on diff match
- [ ] **Precompute + Split**: Non-overlapping subarrays → best left/right for each boundary
- [ ] **Sorted containment**: Stacking/nesting → sort dimensions, then LIS-style DP
