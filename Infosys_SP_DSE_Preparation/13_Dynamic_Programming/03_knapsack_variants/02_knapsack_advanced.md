# Knapsack Advanced Variants

## When to Use Advanced Knapsack

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

Each item has a limited quantity count[i]. Choose items to maximize value within W.

### Binary Splitting Technique

```
Why binary splitting? Naive expansion creates count[i] copies → too many items.

Binary splitting: decompose count[i] into powers of 2:
  count = 13 = 1 + 2 + 4 + 6  (binary representation)
  Create virtual items: (wt×1, val×1), (wt×2, val×2), (wt×4, val×4), (wt×6, val×6)
  Then solve as 0/1 knapsack with O(n × log(count)) virtual items.

Example: item with wt=2, val=3, count=5
  5 = 1 + 2 + 2  (or 1 + 4 in binary)
  Virtual items: (2,3)×1, (2,3)×2, (2,3)×2

  If W=10: can pick virtual items worth 1+2+2=5 pieces max = value 15
  This correctly represents picking the original item up to 5 times.
```

```python
def bounded_knapsack_direct(W: int, wt: list, val: list, count: list) -> int:
    """count[i] = max available pieces of item i"""
    dp = [0] * (W + 1)
    for i in range(len(wt)):
        c = count[i]
        w = wt[i]
        v = val[i]
        # Binary splitting: break count into powers of 2
        k = 1
        while c > 0:
            take = min(k, c)          # Number of items in this virtual group
            weight = take * w          # Total weight of this group
            value = take * v           # Total value of this group
            # 0/1 knapsack update (right-to-left, since each group is used once)
            for cap in range(W, weight - 1, -1):
                dp[cap] = max(dp[cap], dp[cap - weight] + value)
            c -= take
            k <<= 1  # Double the group size: 1, 2, 4, 8, ...
    return dp[W]

# Time: O(W × Σ log count[i]), Space: O(W)
```

---

## Multiple Knapsacks (Two Knapsacks)

Given two knapsacks with capacities W1, W2, maximize total value. Each item goes to one knapsack (or neither).

```
This is a 2D knapsack — dp[c1][c2] = max value with c1 capacity in bag 1,
                                     and c2 capacity in bag 2.

For each item, 3 choices:
  1. Skip it:      dp[c1][c2] unchanged
  2. Put in bag 1: dp[c1][c2] = max(..., dp[c1-w][c2] + v)  if c1 ≥ w
  3. Put in bag 2: dp[c1][c2] = max(..., dp[c1][c2-w] + v)  if c2 ≥ w
```

```python
def two_knapsack(W1: int, W2: int, wt: list, val: list) -> int:
    dp = [[0] * (W2 + 1) for _ in range(W1 + 1)]
    for i in range(len(wt)):
        w, v = wt[i], val[i]
        # Process BOTH bags for each item (must iterate both dims backward)
        for c1 in range(W1, -1, -1):      # Bag 1 capacity (backward)
            for c2 in range(W2, -1, -1):   # Bag 2 capacity (backward)
                if c1 >= w:
                    dp[c1][c2] = max(dp[c1][c2], dp[c1 - w][c2] + v)
                if c2 >= w:
                    dp[c1][c2] = max(dp[c1][c2], dp[c1][c2 - w] + v)
    return dp[W1][W2]

# Time: O(n × W1 × W2), Space: O(W1 × W2)
```

---

## Target Sum

Given nums and a target, assign each element + or - to reach target. Count ways.

### Transformation to Subset Sum

```
Let P = elements with + sign, N = elements with - sign

  sum(P) - sum(N) = target
  sum(P) + sum(N) = total

Adding:  2 × sum(P) = total + target
         sum(P) = (total + target) / 2

So the problem reduces to: Count subsets with sum = (total + target) / 2

Valid only if: (total + target) is even AND total ≥ |target|
```

```python
def find_target_sum_tab(nums: list, target: int) -> int:
    total = sum(nums)
    if (total + target) % 2 != 0 or abs(target) > total:
        return 0
    new_target = (total + target) // 2
    dp = [0] * (new_target + 1)
    dp[0] = 1
    for num in nums:
        for s in range(new_target, num - 1, -1):  # 0/1 style (right-to-left)
            dp[s] += dp[s - num]
    return dp[new_target]

# Example: nums = [1, 1, 1, 1, 1], target = 3
# total=5, new_target=(5+3)/2=4
# Count subsets summing to 4: pick 4 of 5 ones → C(5,4)=5 ways
# Answer: 5

# Time: O(n × new_target), Space: O(new_target)
```

---

## Last Stone Weight II

Given stones. Smash pairs together. Find smallest possible remaining stone.

### Same as Min Subset Sum Difference

```
stones = [2, 7, 4, 1, 8, 1]
total = 23, target = 11

Split into two groups with minimum difference.
If one group sums to S, other sums to 23-S, diff = |23-2S|
Minimize diff → make S as close to 11 as possible.

Best S ≤ 11: S=11 (can we? 2+1+8=11... or 4+7=11)
diff = 23 - 2×11 = 1
```

```python
def last_stone_weight_ii(stones: list) -> int:
    total = sum(stones)
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for stone in stones:
        for s in range(target, stone - 1, -1):
            dp[s] = dp[s] or dp[s - stone]
    # Find closest reachable sum to target
    for s in range(target, -1, -1):
        if dp[s]:
            return total - 2 * s  # Min difference
    return total

# Time: O(n × target), Space: O(target)
```

---

## Ones and Zeros (Binary Knapsack)

Given binary strings and m ones, n zeros. Find max subset size with at most m 1s and n 0s.

```
This is knapsack with TWO weight dimensions:
  weight1[i] = number of 1s in string i
  weight2[i] = number of 0s in string i
  capacity1 = m (max ones allowed)
  capacity2 = n (max zeros allowed)
  value = 1 (each string adds 1 to subset size)

dp[i][j] = max strings using at most i ones and j zeros
```

```python
def find_max_form(strs: list, m: int, n: int) -> int:
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        zeros = s.count('0')
        ones = s.count('1')
        # 0/1 style: both dimensions backward
        for i in range(m, zeros - 1, -1):
            for j in range(n, ones - 1, -1):
                dp[i][j] = max(dp[i][j], dp[i - zeros][j - ones] + 1)
    return dp[m][n]

# Example: strs = ["10","0001","111001","1","0"], m=5, n=3
# Answer: 4 ("10", "0001", "1", "0") — total: zeros=5, ones=3

# Time: O(k × m × n) where k = len(strs)
```

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
