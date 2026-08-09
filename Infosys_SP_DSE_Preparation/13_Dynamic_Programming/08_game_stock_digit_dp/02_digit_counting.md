# Digit DP & Counting DP Problems

This file covers **digit DP** (counting numbers in a range with a digit
constraint) and **counting DP** (counting combinatorial structures like trees,
subsequences, and sequences). Digit DP processes numbers digit by digit using a
tight flag; counting DP builds counts using combinatorial recurrences.

**Note:** "Count Numbers with Digit Sum = Target" and "Unique Binary Search
Trees (LC #96)" are already covered in `07_dp_misc/01_misc_dp_patterns.md` and
are omitted here to avoid duplicates.

---

# Part A: Digit DP (9 Problems)

## 1. Count Numbers with No Consecutive 1s — Medium

**🔗 Practice Link:** [1. Count Numbers with No Consecutive 1s — Medium](https://www.geeksforgeeks.org/count-number-binary-strings-without-consecutive-1s)

### Problem Explanation
Count integers in `[0, N]` whose binary representation has no two consecutive
1s. For example, in `[0, 7]`: valid are 0(000), 1(001), 2(010), 4(100),
5(101) → count = 5. We use digit DP on the binary digits with a tight bound.

### State Definition
`dfs(pos, tight, prev_one)` = count of valid numbers from digit position `pos`
onward, where `tight` means the prefix matches `N`'s prefix exactly, and
`prev_one` indicates if the previous digit was 1.

### Recurrence Relation
For each bit `d` in `{0, 1}` (capped by `N`'s bit if tight):
- If `prev_one` is True and `d == 1`: skip (consecutive 1s).
- Else: recurse with `pos+1`, updated tight and `prev_one = (d == 1)`.

### Base Cases
- `pos == num_bits`: return 1 (valid number constructed).
- If `prev_one` and `d == 1`: return 0 (prune consecutive 1s).

### Intuition (Why This Works)
The binary representation of N defines a digit DP with 2 bits per position.
The `prev_one` flag captures the only constraint (no "11"). The tight flag
ensures we don't exceed N. Memoizing on `(pos, tight, prev_one)` gives O(bits)
states.

### Step-by-Step Procedure
1. Convert `N` to binary, get the bit array.
2. Define `dfs(pos, tight, prev_one)`.
3. At each position, try bits 0 and 1 (respecting tight bound).
4. Skip d=1 if prev_one is True.
5. Memoize and return the count.
6. Call `dfs(0, True, False)`.

### Worked Example (Dry Run)
`N = 5` → binary `101`, 3 bits.

- `dfs(0, T, F)`: limit = 1.
  - d=0 → `dfs(1, F, F)`: free, 2 bits left.
    - d=0 → `dfs(2, F, F)`: d=0 → `dfs(3,...)` = 1; d=1 → `dfs(3,...)` = 1 → 2
    - d=1 → `dfs(2, F, T)`: d=0 → `dfs(3,...)` = 1; d=1 → skip → 1
    - Total: 3
  - d=1 → `dfs(1, T, T)`: limit = 0. d=0 → `dfs(2, F, F)` = 2 → 2.
- Total: 3 + 2 = 5.

**Answer: 5** (numbers 0, 1, 2, 4, 5).

### Code
```python
class Solution:
    def countNoConsecutiveOnes(self, N: int) -> int:
        if N < 0:
            return 0
        bits = list(map(int, bin(N)[2:]))
        n = len(bits)
        memo = {}

        def dfs(pos, tight, prev_one):
            if pos == n:
                return 1
            key = (pos, tight, prev_one)
            if key in memo:
                return memo[key]
            limit = bits[pos] if tight else 1
            total = 0
            for d in range(limit + 1):
                if prev_one and d == 1:
                    continue
                total += dfs(pos + 1, tight and d == limit, d == 1)
            memo[key] = total
            return total

        return dfs(0, True, False)
```

### Complexity
- Time: O(bits * 2 * 2 * 2) = O(log N).
- Space: O(log N) for memo + recursion.

### Common Mistakes & Edge Cases
- `N = 0`: return 1 (binary "0" has no consecutive 1s).
- Don't forget to count 0 itself.
- The tight bound must be applied correctly at each position.

---

## 2. Number of Digit One (LC #233) — Hard

**🔗 Practice Link:** [2. Number of Digit One](https://leetcode.com/problems/number-of-digit-one/)

### Problem Explanation
Count how many times the digit `1` appears in all integers from `0` to `n`.
For example, `n = 13` → 1 appears in 1, 10, 11 (twice), 12, 13 → total = 6.

### State Definition
`dfs(pos, tight, count_ones)` = count of all 1s contributed by digits from
position `pos` onward, given tight constraint and `count_ones` 1s seen so far.

Actually, a more efficient formulation: for each digit position, count how many
times 1 appears at that position across all numbers.

### Recurrence Relation
For each position `pos` (power of 10), decompose `n` into `high`, `cur`, `low`:
- If `cur == 0`: contribution = `high * factor`
- If `cur == 1`: contribution = `high * factor + low + 1`
- If `cur > 1`: contribution = `(high + 1) * factor`

### Base Cases
- `factor = 1` stops the recursion.

### Intuition (Why This Works)
For each digit position, we count how many numbers have a `1` at that position.
The position's digit, higher digits, and lower digits determine the count.
This mathematical approach avoids full digit DP and runs in O(log n).

### Step-by-Step Procedure
1. Initialize `factor = 1`, `count = 0`.
2. While `factor <= n`: extract `high = n // (factor * 10)`, `cur = (n // factor) % 10`, `low = n % factor`.
3. Add the contribution based on `cur`.
4. Multiply `factor` by 10.
5. Return `count`.

### Worked Example (Dry Run)
`n = 13`.

| factor | high | cur | low | contribution |
|--------|------|-----|-----|-------------|
| 1      | 1    | 3   | 0   | (1+1)*1 = 2 (ones: 1, 11's units) |
| 10     | 0    | 1   | 3   | 0*10 + 3 + 1 = 4 (tens: 10,11,12,13) |

**Answer: 2 + 4 = 6**.

### Code
```python
class Solution:
    def countDigitOne(self, n: int) -> int:
        count = 0
        factor = 1
        while factor <= n:
            high = n // (factor * 10)
            cur = (n // factor) % 10
            low = n % factor
            if cur == 0:
                count += high * factor
            elif cur == 1:
                count += high * factor + low + 1
            else:
                count += (high + 1) * factor
            factor *= 10
        return count
```

### Complexity
- Time: O(log n).
- Space: O(1).

### Common Mistakes & Edge Cases
- `n = 0`: return 0.
- Double-counting: the formula handles each position independently.
- `cur == 1` needs the `low + 1` term for the partial last group.

---

## 3. Non-negative Integers without Consecutive Ones (LC #600) — Medium

**🔗 Practice Link:** [3. Non-negative Integers without Consecutive Ones](https://leetcode.com/problems/non-negative-integers-without-consecutive-ones/)

### Problem Explanation
Count non-negative integers <= `n` whose binary representation has no consecutive
1s. For example, `n = 5` (101): valid = 0, 1, 2, 4, 5 → count = 5.
This is digit DP on binary with the consecutive-ones constraint.

### State Definition
`dfs(pos, tight, prev_one)` = count of valid numbers from bit `pos` onward.

### Recurrence Relation
For each bit `d` in `{0, 1}` (capped by N's bit if tight):
- If `prev_one and d == 1`: skip.
- Else: recurse.

### Base Cases
- `pos == num_bits`: return 1.

### Intuition (Why This Works)
Identical structure to Problem 1. The tight flag enforces the upper bound, and
`prev_one` tracks the constraint. This is a classic digit DP template problem.

### Step-by-Step Procedure
1. Convert `n` to binary bits.
2. Define recursive DFS with memo on `(pos, tight, prev_one)`.
3. At each position, try valid bits and accumulate the count.
4. Return `dfs(0, True, False)`.

### Worked Example (Dry Run)
`n = 5` → bits `101`. Same as Problem 1 above.

**Answer: 5**.

### Code
```python
class Solution:
    def findIntegers(self, n: int) -> int:
        bits = list(map(int, bin(n)[2:]))
        n_bits = len(bits)
        memo = {}

        def dfs(pos, tight, prev_one):
            if pos == n_bits:
                return 1
            key = (pos, tight, prev_one)
            if key in memo:
                return memo[key]
            limit = bits[pos] if tight else 1
            total = 0
            for d in range(limit + 1):
                if prev_one and d == 1:
                    continue
                total += dfs(pos + 1, tight and d == limit, d == 1)
            memo[key] = total
            return total

        return dfs(0, True, False)
```

### Complexity
- Time: O(log n).
- Space: O(log n).

### Common Mistakes & Edge Cases
- `n = 0`: return 1.
- Same as Problem 1 — they are the same LC problem framed differently.
- Must handle `N = 0` (binary "0") correctly.

---

## 4. Count Integers with Digit Sum Equal to Target in Range — Medium

**🔗 Practice Link:** [4. Count Integers with Digit Sum Equal to Target in Range — Medium](https://www.geeksforgeeks.org/count-of-n-digit-numbers-whose-sum-of-digits-equals-to-given-sum)

### Problem Explanation
Count integers in `[L, R]` whose digit sum equals `target`. Solve via
`count(R, target) - count(L-1, target)` where `count(N, target)` uses digit DP.

### State Definition
`dfs(pos, tight, digit_sum)` = count of numbers in `[0, N]` with remaining
digit sum to distribute from position `pos` onward.

### Recurrence Relation
For each digit `d` from 0 to `limit`: if `digit_sum + d <= target`, recurse
with `pos+1`, updated tight, and `digit_sum + d`.

### Base Cases
- `pos == len(digits)`: return 1 if `digit_sum == target` else 0.
- Prune: if `digit_sum > target`, return 0.

### Intuition (Why This Works)
Standard digit DP: process digits left to right, track the running digit sum,
and count numbers that hit the target exactly. The tight flag bounds the search
to `[0, N]`. Use prefix subtraction for range queries.

### Step-by-Step Procedure
1. Define `count_upto(N, target)` using digit DP.
2. Return `count_upto(R, target) - count_upto(L-1, target)`.

### Worked Example (Dry Run)
`L=1, R=25, target=3`. From `07_misc`, we know `count(25, 3) = 3` (numbers 3, 12, 21). `count(0, 3) = 0`.
Answer: 3 - 0 = 3.

### Code
```python
class Solution:
    def countInRange(self, L: int, R: int, target: int) -> int:
        def count_upto(high, target):
            if high < 0:
                return 0
            digits = list(map(int, str(high)))
            n = len(digits)
            memo = {}

            def dfs(pos, tight, digit_sum):
                if digit_sum > target:
                    return 0
                if pos == n:
                    return 1 if digit_sum == target else 0
                key = (pos, tight, digit_sum)
                if key in memo:
                    return memo[key]
                limit = digits[pos] if tight else 9
                total = 0
                for d in range(limit + 1):
                    total += dfs(pos + 1, tight and d == limit, digit_sum + d)
                memo[key] = total
                return total

            return dfs(0, True, 0)

        return count_upto(R, target) - count_upto(L - 1, target)
```

### Complexity
- Time: O(20 * 2 * target * 10) per call.
- Space: O(20 * 2 * target).

### Common Mistakes & Edge Cases
- `L = 0`: handle `count_upto(-1)` returning 0.
- Target > 9 * num_digits: return 0 immediately.
- Leading zeros are handled naturally (they add 0 to digit_sum).

---

## 5. Numbers At Most N Given Digit Set (LC #902) — Hard

**🔗 Practice Link:** [5. Numbers At Most N Given Digit Set](https://leetcode.com/problems/numbers-at-most-n-given-digit-set/)

### Problem Explanation
Given a set of allowed digits `digits` and a number `n`, count how many positive
integers can be formed using only those digits that are <= `n`. Digits may be
repeated. For example, `digits = [1,2,3], n = 312` → many numbers.

### State Definition
`dfs(pos, tight, started)` = count of valid numbers from position `pos` onward,
where `started` tracks if a non-leading-zero digit has been placed.

### Recurrence Relation
For each allowed digit `d` (capped by N's digit if tight):
- If not started and d == 0: recurse with `started = False`.
- Else: recurse with `started = True`.

### Base Cases
- `pos == len(digits)`: return 1 if `started` else 0 (exclude zero unless needed).

### Intuition (Why This Works)
The leading-zero handling is key: numbers with fewer digits are also valid.
The `started` flag lets us count shorter numbers. The tight flag enforces the
bound. We only iterate over allowed digits, not 0-9.

### Step-by-Step Procedure
1. Convert `n` to digit array.
2. Sort the allowed digits.
3. DFS with `(pos, tight, started)`.
4. At each position, try each allowed digit within the tight bound.
5. Count numbers where `started = True`.

### Worked Example (Dry Run)
`digits = [1, 3, 5], n = 53`. Valid numbers: 1, 3, 5, 11, 13, 15, 31, 33, 35, 51, 53.

Count: 3 (single-digit) + 9 (two-digit) = 12... but 53 includes 51 and 53 only.
Let me count: 1,3,5 (3) + 11,13,15,31,33,35,51,53 (8) = **11**.

### Code
```python
class Solution:
    def atMostNGivenDigitSet(self, digits: list, n: int) -> int:
        digits_str = list(map(int, str(n)))
        num_digits = len(digits)
        memo = {}

        def dfs(pos, tight, started):
            if pos == len(digits_str):
                return 1 if started else 0
            key = (pos, tight, started)
            if key in memo:
                return memo[key]
            total = 0
            limit = digits_str[pos] if tight else 9
            # Option: don't start yet (place leading zero)
            if not started:
                total += dfs(pos + 1, False, False)
            for d in digits:
                if d > limit:
                    break
                total += dfs(pos + 1, tight and d == limit, True)
            memo[key] = total
            return total

        return dfs(0, True, False)
```

### Complexity
- Time: O(log n * 2 * 2 * |digits|).
- Space: O(log n).

### Common Mistakes & Edge Cases
- Leading zeros: must count numbers with fewer digits than n.
- `digits` may not contain 0 (most formulations exclude 0).
- All digits greater than n's digits: only shorter numbers count.

---

## 6. Count Special Numbers (LC #2376) — Hard

**🔗 Practice Link:** [6. Count Special Numbers](https://leetcode.com/problems/count-special-integers/)

### Problem Explanation
A "special number" has all unique digits. Count special numbers in `[1, n]`.
For example, `n = 20` → 1,2,...,9,10,12,13,...,19,20 → valid: 1-9 (9) + 10,12-19
(8) + 20 (1) = 18.

### State Definition
`dfs(pos, tight, mask)` where `mask` is a bitmask of used digits (10 bits).

### Recurrence Relation
For each digit `d` from 0 to `limit`:
- If bit `d` is already set in `mask`, skip.
- Else recurse with `mask | (1 << d)`.

### Base Cases
- `pos == len(digits)`: return 1 if at least one digit was placed (not all leading zeros).

### Intuition (Why This Works)
The bitmask tracks which digits 0-9 have been used, giving at most 10 * 2^10
states per position. The tight flag bounds to `[1, n]`. This is a clean digit DP
with bitmask state.

### Step-by-Step Procedure
1. Convert `n` to digits.
2. DFS with `(pos, tight, mask)`.
3. Skip digits already in the mask.
4. Handle leading zeros (don't set bit for 0 until started).

### Worked Example (Dry Run)
`n = 20`. Binary digits `[2, 0]`.

- Position 0 (tens): d=0 (leading zero, recurse free); d=1 (mask=010); d=2 (mask=100).
  - d=0 → position 1 (free): d=0-9, skip repeats. d=0 → not started → return 0. d=1-9 → 9 valid.
  - d=1 → position 1 (tight, limit=0): d=0 → mask=011 → 1 valid.
  - d=2 → position 1 (tight, limit=0): d=0 → mask=101 → 1 valid.
- Total: 9 + 1 + 1 = 11... hmm, let me recount. Actually from 1-20: 1-9 (9) + 10 (yes), 11 (no, repeated 1), 12,13,14,15,16,17,18,19 (8), 20 (yes) = 19.

Wait, I'm making an error. Let me recount: The answer for n=20 is 19. Numbers 1-9: all valid (9). 10: valid (1). 11: invalid. 12-19: all valid (8). 20: valid (1). Total: 9+1+8+1 = 19.

The DP handles leading zeros by not placing bits for them. When the recursion ends with `mask != 0`, the number is valid.

### Code
```python
class Solution:
    def countSpecialNumbers(self, n: int) -> int:
        digits = list(map(int, str(n)))
        num_digits = len(digits)
        memo = {}

        def dfs(pos, tight, mask, started):
            if pos == num_digits:
                return 1 if started else 0
            key = (pos, tight, mask)
            if key in memo:
                return memo[key]
            total = 0
            limit = digits[pos] if tight else 9
            # Leading zero: don't consume a digit
            if not started:
                total += dfs(pos + 1, False, mask, False)
            for d in range(0 if started else 1, limit + 1):
                if mask & (1 << d):
                    continue
                total += dfs(pos + 1, tight and d == limit, mask | (1 << d), True)
            memo[key] = total
            return total

        return dfs(0, True, 0, False)
```

### Complexity
- Time: O(log n * 2 * 2^10 * 10).
- Space: O(log n * 2 * 2^10).

### Common Mistakes & Edge Cases
- Leading zeros: must not set the bit for 0 until a non-zero digit is placed.
- `n = 0`: return 0 (no positive integers in [1, 0]).
- All digits 0-9 used: no more special numbers possible.

---

## 7. At Most K Digits / At Most K Swaps — Medium

**🔗 Practice Link:** [7. At Most K Digits / At Most K Swaps — Medium](https://www.geeksforgeeks.org/find-maximum-number-possible-by-doing-at-most-k-swaps)

### Problem Explanation
Given a number as a string `num` and integer `k`, find the largest number by
performing at most `k` swaps of adjacent digits. For example,
`num = "12345", k = 2` → swap to get "12435" (no improvement needed actually).
A more standard variant: find the largest number achievable with at most k swaps
of any two digits.

### State Definition
`dfs(num_list, k)` = maximum number achievable from current configuration with
`k` swaps remaining. Use memoization on `(tuple(num_list), k)`.

### Recurrence Relation
For each pair `(i, j)` with `i < j`: if swapping `num[i]` and `num[j]` improves
the result, swap and recurse with `k-1`. Try all possible swaps.

### Base Cases
- `k == 0`: return current number.
- No improvement possible: return current number.

### Intuition (Why This Works)
At each step, try every possible swap and keep the best result. The state is the
current digit arrangement plus remaining swaps. Memoization avoids recomputing
the same (arrangement, k) pair. Greedy: always try to place the largest digit
at the leftmost position.

### Step-by-Step Procedure
1. Convert string to list of characters.
2. For each position `i`, find the largest digit in positions `i+1` to end.
3. Swap it to position `i`, recurse with `k-1`.
4. Track the best result across all branches.
5. Memoize on `(tuple(num_list), k)`.

### Worked Example (Dry Run)
`num = "7599", k = 2`. Swap 7↔9 (pos 0,3): "9597", k=1. Swap 5↔9 (pos 1,2): "9957".
**Answer: "9957"**.

### Code
```python
class Solution:
    def maxSwap(self, num: str, k: int) -> str:
        chars = list(num)
        n = len(chars)
        memo = {}

        def dfs(arr, swaps):
            state = (tuple(arr), swaps)
            if state in memo:
                return memo[state]
            best = arr[:]
            if swaps > 0:
                for i in range(n):
                    for j in range(i + 1, n):
                        arr[i], arr[j] = arr[j], arr[i]
                        candidate = dfs(arr, swaps - 1)
                        if candidate > best:
                            best = candidate[:]
                        arr[i], arr[j] = arr[j], arr[i]
            memo[state] = best
            return best

        result = dfs(chars, k)
        return ''.join(result)
```

### Complexity
- Time: O(n^2 * k * n^k) worst case (exponential in k, but memo helps).
- Space: O(n^k) for memo.

### Common Mistakes & Edge Cases
- Swaps are of any two digits, not just adjacent (unless specified).
- Must track remaining swaps carefully.
- The memo key must include the full arrangement for correctness.

---

## 8. Find All Good Numbers in Range — Medium

**🔗 Practice Link:** [8. Find All Good Numbers in Range — Medium](https://leetcode.com/problems/numbers-at-most-n-given-digit-set/)

### Problem Explanation
A "good number" has no digit equal to `d` at any position. Count good numbers
in `[L, R]`. Use digit DP to count up to R minus count up to L-1.

### State Definition
`dfs(pos, tight)` = count of numbers from position `pos` onward that don't
contain digit `d`.

### Recurrence Relation
For each digit from 0 to `limit`:
- If `digit == d`, skip.
- Else recurse.

### Base Cases
- `pos == num_digits`: return 1 (valid number formed).

### Intuition (Why This Works)
Simple digit DP: exclude the forbidden digit at each position. The tight flag
ensures the upper bound. Use prefix subtraction for range counting.

### Step-by-Step Procedure
1. Define `count_upto(N, d)` via digit DP.
2. Return `count_upto(R, d) - count_upto(L-1, d)`.

### Worked Example (Dry Run)
`L=1, R=25, d=3`. Numbers 1-25 without digit 3: 1,2,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19,20,21,22,24,25.
**Answer: 22**.

### Code
```python
class Solution:
    def countGoodNumbers(self, L: int, R: int, d: int) -> int:
        def count_upto(high, d):
            if high < 0:
                return 0
            digits = list(map(int, str(high)))
            n = len(digits)
            memo = {}

            def dfs(pos, tight):
                if pos == n:
                    return 1
                key = (pos, tight)
                if key in memo:
                    return memo[key]
                limit = digits[pos] if tight else 9
                total = 0
                for dd in range(limit + 1):
                    if dd == d:
                        continue
                    total += dfs(pos + 1, tight and dd == limit)
                memo[key] = total
                return total

            return dfs(0, True)

        return count_upto(R, d) - count_upto(L - 1, d)
```

### Complexity
- Time: O(20 * 2 * 10) per call.
- Space: O(20 * 2).

### Common Mistakes & Edge Cases
- `d = 0`: many numbers excluded (10, 20, 30, ...).
- `L = 0`: handle `count_upto(-1)` returning 0.
- The digit `d` can be 0-9.

---

## 9. Generate All Numbers with Digit Sum S — Easy

**🔗 Practice Link:** [9. Generate All Numbers with Digit Sum S — Easy](https://www.geeksforgeeks.org/digit-dp-introduction)

### Problem Explanation
Generate all positive integers whose digits sum to exactly `S`. For example,
`S = 5` → 5, 14, 23, 32, 41, 50, 104, 113, ... (infinitely many).

### State Definition
`dfs(remaining, current)` where `remaining` is the digit sum left to allocate
and `current` is the number being built (as a string).

### Recurrence Relation
For each digit `d` from 0 to 9 (or 1 if building the first digit):
- If `d <= remaining`: append `d` and recurse with `remaining - d`.

### Base Cases
- `remaining == 0`: add `current` to results.
- `remaining < 0`: return.

### Intuition (Why This Works)
This is a backtracking / DFS problem, not strictly digit DP (no upper bound).
Build numbers digit by digit, choosing each digit 0-9 and tracking the remaining
sum. The first digit cannot be 0 to avoid leading zeros.

### Step-by-Step Procedure
1. Define DFS with `(remaining_sum, current_number)`.
2. For first digit, try 1-9; for subsequent digits, try 0-9.
3. When `remaining == 0`, save the number.
4. This generates infinitely many numbers; limit by number of digits if needed.

### Worked Example (Dry Run)
`S = 3`. DFS builds: "3", "12", "21", "30", "102", "111", "120", "201", "210", "300", ...

### Code
```python
class Solution:
    def generateNumbers(self, S: int, max_digits: int = 5) -> list:
        results = []

        def dfs(remaining, current, is_first):
            if remaining == 0 and not is_first:
                results.append(int(current))
                return
            if remaining < 0:
                return
            start = 1 if is_first else 0
            for d in range(start, 10):
                if d <= remaining:
                    dfs(remaining - d, current + str(d), False)

        dfs(S, "", True)
        return sorted(results)
```

### Complexity
- Time: O(9^max_digits) worst case (bounded by max_digits).
- Space: O(max_digits) recursion depth.

### Common Mistakes & Edge Cases
- Leading zeros: first digit must be 1-9.
- `S = 0`: return empty list (no positive integer has digit sum 0).
- Infinite results without a digit limit; use `max_digits` to bound.

---

# Part B: Counting DP (8 Problems)

## 10. Catalan Numbers / Unique BSTs (LC #96) — Medium

**🔗 Practice Link:** [10. Catalan Numbers / Unique BSTs](https://leetcode.com/problems/unique-binary-search-trees/)

### Problem Explanation
Count the number of structurally unique BSTs that store values 1 to `n`. Each
node has a unique value. For `n = 3`, there are 5 unique BSTs. This is the
nth Catalan number: `C(n) = C(2n,n)/(n+1)`.

### State Definition
`dp[i]` = number of unique BSTs with `i` nodes.

### Recurrence Relation
`dp[i] = sum(dp[j] * dp[i-1-j] for j in range(i))`
Choose root `j+1` (0-indexed): left subtree has `j` nodes, right has `i-1-j`.

### Base Cases
- `dp[0] = 1` (empty tree).
- `dp[1] = 1` (single node).

### Intuition (Why This Works)
For each possible root, the left and right subtrees are independent BSTs on
smaller node counts. This is the Catalan recurrence: the root splits the nodes
into left and right, and the total count is the sum over all root choices of
the product of left and right subtree counts.

### Step-by-Step Procedure
1. Initialize `dp[0] = 1`, `dp[1] = 1`.
2. For `i` from 2 to `n`: `dp[i] = sum(dp[j] * dp[i-1-j] for j in range(i))`.
3. Return `dp[n]`.

### Worked Example (Dry Run)
`n = 4`.

| i | computation | dp[i] |
|---|-------------|-------|
| 0 | base        | 1     |
| 1 | base        | 1     |
| 2 | dp[0]*dp[1] + dp[1]*dp[0] = 2 | 2 |
| 3 | 1*2 + 1*1 + 2*1 = 5 | 5 |
| 4 | 1*5 + 1*2 + 2*1 + 5*1 = 14 | 14 |

**Answer: 14**.

### Code
```python
class Solution:
    def numTrees(self, n: int) -> int:
        dp = [0] * (n + 1)
        dp[0] = dp[1] = 1
        for i in range(2, n + 1):
            for j in range(i):
                dp[i] += dp[j] * dp[i - 1 - j]
        return dp[n]
```

### Complexity
- Time: O(n^2).
- Space: O(n).

### Common Mistakes & Edge Cases
- `dp[0] = 1` is essential (multiplicative identity for the product).
- The Catalan formula `C(2n,n)/(n+1)` is an O(n) alternative.
- `n = 0`: return 1 (empty tree).

---

## 11. Count Number of Balanced Binary Trees — Medium

**🔗 Practice Link:** [11. Count Number of Balanced Binary Trees — Medium](https://www.geeksforgeeks.org/count-balanced-binary-trees-height-h)

### Problem Explanation
Count balanced binary trees of height `h` (each node's left and right subtree
heights differ by at most 1). Return count modulo 10^9+7.

### State Definition
`dp[h]` = number of balanced trees of height `h`.
Also track `perfect[h]` = number of perfect trees of height `h`.

### Recurrence Relation
- `perfect[h] = perfect[h-1]^2` (both subtrees must be perfect).
- `dp[h] = dp[h-1]^2 + 2 * dp[h-1] * dp[h-2]`
  (both subtrees height h-1, or one h-1 and one h-2).

### Base Cases
- `dp[0] = 1`, `dp[1] = 1`.
- `perfect[0] = 1`, `perfect[1] = 1`.

### Intuition (Why This Works)
A balanced tree of height `h` has subtrees of heights (h-1, h-1), (h-1, h-2),
or (h-2, h-1). The count is the product of subtree counts for each combination.
This builds up from height 0 using the recurrence.

### Step-by-Step Procedure
1. Initialize `dp[0] = 1`, `dp[1] = 1`.
2. For `h` from 2 to target: compute using the recurrence.
3. Apply modulo at each step.

### Worked Example (Dry Run)
`h = 3`.

| h | dp[h] | computation |
|---|-------|-------------|
| 0 | 1     | base        |
| 1 | 1     | base        |
| 2 | 1+2=3 | 1^2 + 2*1*1 |
| 3 | 9+6=15| 3^2 + 2*3*1 |

**Answer: 15**.

### Code
```python
class Solution:
    def countBalancedTrees(self, h: int) -> int:
        MOD = 10**9 + 7
        dp = [0] * (h + 1)
        dp[0] = dp[1] = 1
        for i in range(2, h + 1):
            dp[i] = (dp[i-1] * dp[i-1] + 2 * dp[i-1] * dp[i-2]) % MOD
        return dp[h]
```

### Complexity
- Time: O(h).
- Space: O(h) (or O(1) with rolling variables).

### Common Mistakes & Edge Cases
- `h = 0`: return 1 (empty tree).
- Must apply modulo to prevent overflow.
- The factor of 2 accounts for two asymmetric combinations.

---

## 12. Count of Distinct Subsequences — Hard

**🔗 Practice Link:** [12. Count of Distinct Subsequences — Hard](https://leetcode.com/problems/distinct-subsequences-ii/)

### Problem Explanation
Given a string `s`, count the number of distinct subsequences (including empty).
For `s = "abc"`, subsequences: "", "a", "b", "c", "ab", "ac", "bc", "abc" → 8.

### State Definition
`dp[i]` = number of distinct subsequences of `s[:i]`. Track `last[ch]` = last
index where character `ch` appeared.

### Recurrence Relation
`dp[i] = 2 * dp[i-1]` (all previous subsequences, with or without `s[i-1]`).
If `s[i-1]` appeared before at index `j`: subtract `dp[j]` to remove duplicates.

### Base Cases
- `dp[0] = 1` (empty string has one subsequence: "").

### Intuition (Why This Works)
Each character doubles the count (include or exclude it). But if a character
repeats, the subsequences formed by the second occurrence that don't use any
earlier occurrence are already counted — subtract the duplicate contribution.

### Step-by-Step Procedure
1. Initialize `dp[0] = 1`, `last = {}`.
2. For `i` from 1 to `n`: `dp[i] = 2 * dp[i-1]`.
3. If `s[i-1]` in `last`: `dp[i] -= dp[last[s[i-1]] - 1]`.
4. Update `last[s[i-1]] = i`.
5. Return `dp[n]`.

### Worked Example (Dry Run)
`s = "aba"`.

| i | char | dp[i] = 2*dp[i-1] | last | correction | final dp[i] |
|---|------|--------------------|------|------------|-------------|
| 0 | -    | -                  | {}   | -          | 1           |
| 1 | a    | 2                  | {a:1}| -          | 2           |
| 2 | b    | 4                  | {a:1,b:2}| -    | 4           |
| 3 | a    | 8                  | {a:3,b:2}| -dp[0]=-1 | 7      |

Subsequences: "", "a", "b", "ab", "a"(2nd), "ba", "aba" → 7 distinct.

**Answer: 7**.

### Code
```python
class Solution:
    def distinctSubseqCount(self, s: str) -> int:
        MOD = 10**9 + 7
        dp = [0] * (len(s) + 1)
        dp[0] = 1
        last = {}
        for i, ch in enumerate(s):
            dp[i + 1] = (2 * dp[i]) % MOD
            if ch in last:
                dp[i + 1] = (dp[i + 1] - dp[last[ch] - 1]) % MOD
            last[ch] = i + 1
        return dp[len(s)]
```

### Complexity
- Time: O(n).
- Space: O(n) (or O(1) with a single variable).

### Common Mistakes & Edge Cases
- Empty subsequences count (dp[0] = 1).
- Modulo arithmetic: subtract before taking modulo to avoid negatives.
- `s = ""`: return 1 (just the empty subsequence).

---

## 13. Pascal's Triangle (LC #118) — Easy

**🔗 Practice Link:** [13. Pascal's Triangle](https://leetcode.com/problems/pascals-triangle/)

### Problem Explanation
Generate the first `numRows` of Pascal's triangle. Each row's values are the
sum of the two values directly above. Row 0: [1], Row 1: [1,1], Row 2: [1,2,1].

### State Definition
`dp[i][j]` = value at row `i`, position `j` (0-indexed).

### Recurrence Relation
`dp[i][j] = dp[i-1][j-1] + dp[i-1][j]` for `0 < j < i`.

### Base Cases
- `dp[i][0] = dp[i][i] = 1` (edges are always 1).

### Intuition (Why This Works)
Each interior element is the sum of the two elements above it. This is the
fundamental property of binomial coefficients: `C(n,k) = C(n-1,k-1) + C(n-1,k)`.

### Step-by-Step Procedure
1. Initialize row 0 as `[1]`.
2. For each row `i` from 1 to `numRows-1`:
3. Start and end with 1.
4. Interior values: `row[j] = prev[j-1] + prev[j]`.

### Worked Example (Dry Run)
`numRows = 5`.

| row | values |
|-----|--------|
| 0   | [1]    |
| 1   | [1,1]  |
| 2   | [1,2,1] |
| 3   | [1,3,3,1] |
| 4   | [1,4,6,4,1] |

### Code
```python
class Solution:
    def generate(self, numRows: int) -> list:
        triangle = [[1]]
        for i in range(1, numRows):
            prev = triangle[-1]
            row = [1] + [prev[j-1] + prev[j] for j in range(1, i)] + [1]
            triangle.append(row)
        return triangle
```

### Complexity
- Time: O(numRows^2).
- Space: O(numRows^2) for the full triangle.

### Common Mistakes & Edge Cases
- `numRows = 0`: return empty list.
- Each row has exactly `i+1` elements.
- Edges are always 1.

---

## 14. Minimum Number of Taps to Open to Water Garden (LC #1326) — Hard

**🔗 Practice Link:** [14. Minimum Number of Taps to Open to Water Garden](https://leetcode.com/problems/minimum-number-of-taps-to-open-to-water-a-garden/)

### Problem Explanation
A garden of length `n` has taps at various positions. Tap `i` waters the range
`[i - ranges[i], i + ranges[i]]`. Find the minimum taps to open to water the
entire garden `[0, n]`. For example, `ranges = [3,4,1,1,0,0]` → open taps 0
and 1 to cover [0,5].

### State Definition
`dp[i]` = minimum taps to water up to position `i`.

### Recurrence Relation
`dp[i] = min(dp[j] + 1)` for all `j` where tap `j` can reach position `i`.
Preprocess: for each position `i`, compute the farthest left tap `j` can reach.

### Base Cases
- `dp[0] = 0` (nothing to water before position 0).
- All other `dp[i] = inf`.

### Intuition (Why This Works)
Convert taps into intervals, then use a jump-game-like DP. For each position `i`,
the minimum taps to reach `i` is 1 + the minimum taps to reach any position that
a tap can extend to `i`. This is essentially the minimum number of intervals to
cover `[0, n]`.

### Step-by-Step Procedure
1. Precompute `max_reach[i]` = farthest position reachable from `i` by a tap.
2. Use interval DP or greedy: `dp[i] = min(dp[j] + 1)` for all j where
   `max_reach[j] >= i`.
3. Return `dp[n]` if finite, else -1.

### Worked Example (Dry Run)
`n = 5, ranges = [3,4,1,1,0,0]`.
Tap 0: [0-3, 0+3] = [0, 3]. Tap 1: [0, 5]. Tap 2: [1, 3]. Tap 3: [2, 4]. Tap 4: [4, 4]. Tap 5: [5, 5].

DP: dp[0]=0. Tap 1 covers [0,5] → dp[5] = 1.
**Answer: 1** (just open tap 1).

### Code
```python
class Solution:
    def minTaps(self, n: int, ranges: list) -> int:
        max_reach = [0] * (n + 1)
        for i in range(n + 1):
            start = max(0, i - ranges[i])
            end = min(n, i + ranges[i])
            max_reach[start] = max(max_reach[start], end)
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        for i in range(n + 1):
            for j in range(i + 1, max_reach[i] + 1):
                dp[j] = min(dp[j], dp[i] + 1)
        return dp[n] if dp[n] != float('inf') else -1
```

### Complexity
- Time: O(n^2).
- Space: O(n).

### Common Mistakes & Edge Cases
- Tap with `ranges[i] = 0` only waters its exact position.
- Unreachable positions: return -1.
- The garden is `[0, n]`, not `[0, n-1]`.

---

## 15. Count Ways to Build Staircase — Medium

**🔗 Practice Link:** [15. Count Ways to Build Staircase — Medium](https://www.geeksforgeeks.org/count-ways-reach-nth-stair)

### Problem Explanation
Count the number of ways to build a staircase with `n` blocks where each step
must have at least one more block than the previous step. For `n = 7`: ways
are [7], [3,4], [1,2,4], [1,2,3,1]... actually [1,2,4] and [2,5]... this is
the number of partitions of `n` into strictly increasing parts.

### State Definition
`dp[i][j]` = number of ways to partition `i` using parts of size at least `j`.

### Recurrence Relation
`dp[i][j] = dp[i][j+1] + dp[i-j][j+1]` (skip part j, or use part j and continue
with parts >= j+1).

### Base Cases
- `dp[0][j] = 1` for any `j` (empty partition).
- `dp[i][j] = 0` if `j > i`.

### Intuition (Why This Works)
This is a constrained partition problem. At each step, we decide whether to use
a part of size `j` or skip to `j+1`. The strictly increasing constraint means
each subsequent part must be larger. This naturally forms a 2D DP.

### Step-by-Step Procedure
1. Define DFS with `(remaining, min_part)`.
2. If `remaining == 0`, return 1.
3. If `min_part > remaining`, return 0.
4. `dfs(remaining, min_part) = dfs(remaining, min_part+1) + dfs(remaining-min_part, min_part+1)`.

### Worked Example (Dry Run)
`n = 7`. Partitions into strictly increasing parts:
7, 1+6, 2+5, 3+4, 1+2+4 → 5 ways.

### Code
```python
class Solution:
    def countStaircaseWays(self, n: int) -> int:
        memo = {}

        def dfs(remaining, min_part):
            if remaining == 0:
                return 1
            if min_part > remaining:
                return 0
            key = (remaining, min_part)
            if key in memo:
                return memo[key]
            result = dfs(remaining, min_part + 1) + dfs(remaining - min_part, min_part + 1)
            memo[key] = result
            return result

        return dfs(n, 1)
```

### Complexity
- Time: O(n^2) (number of distinct states).
- Space: O(n^2).

### Common Mistakes & Edge Cases
- `n = 0`: return 1 (empty staircase).
- `n = 1`: return 1 (single step).
- Parts must be strictly increasing (not non-decreasing).

---

## 16. Number of Ways to Split Array into Two Parts — Medium

**🔗 Practice Link:** [16. Number of Ways to Split Array into Two Parts — Medium](https://leetcode.com/problems/number-of-ways-to-split-array/)

### Problem Explanation
Given an array, count the number of ways to split it into two non-empty
contiguous parts such that the sum of the left part >= sum of the right part.
For `nums = [10, 4, -8, 7]`: split after index 1 → left=[10,4]=14, right=[-8,7]=-1,
14 >= -1 ✓. **Answer: 2**.

### State Definition
`dp[i]` = 1 if `sum(nums[0:i]) >= sum(nums[i:n])`, else 0.

### Recurrence Relation
Precompute prefix sums. For each split point `i` (1 to n-1):
`valid[i] = 1 if prefix[i] >= (total - prefix[i]) else 0`.
Answer = `sum(valid[i])`.

### Base Cases
- No valid splits: return 0.

### Intuition (Why This Works)
The total sum is fixed, so the condition `left >= right` becomes
`prefix[i] >= total / 2`. A single prefix-sum pass with a counter suffices.

### Step-by-Step Procedure
1. Compute `total = sum(nums)`.
2. Compute prefix sum as you iterate.
3. For each split point, check if `prefix >= total - prefix`.
4. Count valid splits.

### Worked Example (Dry Run)
`nums = [10, 4, -8, 7]`, total = 13.

| i | prefix | total-prefix | valid? |
|---|--------|-------------|--------|
| 1 | 14     | -1          | Yes    |
| 2 | 6      | 7           | No     |
| 3 | -2     | 15          | No     |

**Answer: 1**. (Wait, I said 2 earlier — let me recount. Actually only split at i=1 works. The answer is 1.)

### Code
```python
class Solution:
    def waysToSplitArray(self, nums: list) -> int:
        total = sum(nums)
        prefix = 0
        count = 0
        for i in range(len(nums) - 1):
            prefix += nums[i]
            if prefix >= total - prefix:
                count += 1
        return count
```

### Complexity
- Time: O(n).
- Space: O(1).

### Common Mistakes & Edge Cases
- The split must be into two non-empty parts (don't check at the last element).
- Negative numbers are allowed; the comparison still holds.
- `total` can be negative (all negative numbers).

---

## 17. Count All Valid Pickup and Delivery Options (LC #1359) — Hard

**🔗 Practice Link:** [17. Count All Valid Pickup and Delivery Options](https://leetcode.com/problems/count-all-valid-pickup-and-delivery-options/)

### Problem Explanation
There are `n` orders. Each order has a pickup (P) and delivery (D). Count the
number of valid sequences where every D comes after its corresponding P. For
`n = 2`, valid sequences: PPDD, PDPD, PD PD... actually 6 sequences.

### State Definition
`dp[i]` = number of valid sequences for `i` orders.

### Recurrence Relation
When adding the i-th order (P_i and D_i), there are `2*i - 1` positions to
insert them (P_i before D_i). `dp[i] = dp[i-1] * (2*i - 1) * i`.

Actually: `dp[i] = dp[i-1] * C(2i, 2) / 1 = dp[i-1] * i * (2*i - 1)`.
We choose 2 positions out of 2i for the new P and D (P before D), multiplied
by the arrangements of the previous orders.

### Base Cases
- `dp[0] = 1` (no orders → one empty sequence).

### Intuition (Why This Works)
Add orders one at a time. When adding order i, there are `2i - 1` valid
insertion positions for P_i and D_i (P_i must come before D_i). The count
multiplies by `(2i-1) * i` (choosing where to place P and D among the 2i
positions, with P before D).

### Step-by-Step Procedure
1. `dp[0] = 1`.
2. For `i` from 1 to `n`: `dp[i] = dp[i-1] * i * (2*i - 1)`.
3. Return `dp[n]`.

### Worked Example (Dry Run)
`n = 3`.

| i | dp[i] | computation |
|---|-------|-------------|
| 0 | 1     | base        |
| 1 | 1     | 1 * 1 * 1   |
| 2 | 6     | 1 * 2 * 3   |
| 3 | 90    | 6 * 3 * 5   |

**Answer: 90**.

### Code
```python
class Solution:
    def countOrders(self, n: int) -> int:
        MOD = 10**9 + 7
        dp = 1
        for i in range(1, n + 1):
            dp = dp * i * (2 * i - 1) % MOD
        return dp
```

### Complexity
- Time: O(n).
- Space: O(1).

### Common Mistakes & Edge Cases
- `n = 1`: return 1 (only PD).
- The multiplier `(2i-1) * i` comes from: choose 2 of 2i positions for P,D
  with P before D, which is C(2i,2) = i*(2i-1).
- Apply modulo to prevent overflow.
- `n = 0`: return 1 (empty sequence).
