# Permutations & Combinations — Complete Guide

## Table of Contents
1. [Permutations of Array](#permutations-of-array)
2. [Permutations II (with duplicates)](#permutations-ii)
3. [Combinations](#combinations)
4. [Combination Sum I, II, III](#combination-sum)
5. [Subsets I, II](#subsets)
6. [Next Permutation](#next-permutation)
7. [Permutation Sequence](#permutation-sequence)
8. [Gray Code](#gray-code)

---

## Permutations of Array

### Problem
Given an array of distinct integers, return all possible permutations.

### Visual: How Permutations Work

```
  PERMUTATIONS OF [1, 2, 3]:
  ═══════════════════════════

  Total permutations = 3! = 3 × 2 × 1 = 6

  Decision Tree (using "used" array):
  ════════════════════════════════════

                              []
                  ┌──────────┼──────────┐
                pick 1     pick 2     pick 3
                [1]        [2]        [3]
                /  \       /  \       /  \
             2    3     1    3     1    2
            [1,2][1,3] [2,1][2,3] [3,1][3,2]
             |    |     |    |     |    |
            3    2     3    1     2    1
          [1,2,3][1,3,2][2,1,3][2,3,1][3,1,2][3,2,1]
            ✓     ✓     ✓     ✓     ✓     ✓

  At each level, we pick from REMAINING elements (not yet used):

  Level 0: 3 choices (pick 1, 2, or 3)
  Level 1: 2 choices (remaining elements)
  Level 2: 1 choice  (last element)
  Total: 3 × 2 × 1 = 6 = 3!

  VISUAL: Used Array State at Each Step
  ══════════════════════════════════════
  Pick 1 → Pick 2 → Pick 3:
  used=[T,F,F] → used=[T,T,F] → used=[T,T,T] → record [1,2,3]
  Then backtrack: used=[T,F,F] → Pick 3 → Pick 2:
  used=[T,F,T] → used=[T,T,T] → record [1,3,2]
  Then backtrack all the way: Pick 2 → ...
```

### Approach: Backtracking with used array

```python
def permute(nums):
    result = []
    used = [False] * len(nums)  # track which indices are in current path

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])  # COPY! Without [:], all results share same list
            return

        for i in range(len(nums)):
            if used[i]:
                continue  # skip already-used elements

            # MAKE CHOICE
            used[i] = True
            path.append(nums[i])

            # RECURSE with updated state
            backtrack(path)

            # UNDO CHOICE (backtrack)
            path.pop()
            used[i] = False

    backtrack([])
    return result

# Example
print(permute([1, 2, 3]))
# [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

### Why path[:] matters

```
  WITHOUT path[:]:
  ════════════════
  result.append(path)
  After all recursions, path = [] (empty at the end)
  So result = [[], [], [], [], [], []]  ← All point to the SAME empty list!

  WITH path[:]:
  ══════════════
  result.append(path[:])  # creates a COPY
  Each result entry is an independent snapshot:
  result = [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]  ✓
```

### Alternative: Swap-based (in-place)

```python
def permute_swap(nums):
    result = []

    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]  # swap
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]  # undo swap

    backtrack(0)
    return result
```

### Visual: Swap-Based Permutation Walkthrough

```
  SWAP METHOD: [1, 2, 3]
  ════════════════════════

  Start at index 0, swap each element to position 0:

  [1, 2, 3]  ← start=0
    swap(0,0) → [1, 2, 3]
      start=1: swap(1,1) → [1, 2, 3]
        start=2: swap(2,2) → [1, 2, 3] ✓ RECORD
      start=1: swap(1,2) → [1, 3, 2]
        start=2: swap(2,2) → [1, 3, 2] ✓ RECORD
      undo swap → [1, 2, 3]
    swap(0,1) → [2, 1, 3]
      start=1: swap(1,1) → [2, 1, 3]
        start=2: swap(2,2) → [2, 1, 3] ✓ RECORD
      start=1: swap(1,2) → [2, 3, 1]
        start=2: swap(2,2) → [2, 3, 1] ✓ RECORD
      undo swap → [2, 1, 3]
    swap(0,2) → [3, 2, 1]
      start=1: swap(1,1) → [3, 2, 1]
        start=2: swap(2,2) → [3, 2, 1] ✓ RECORD
      start=1: swap(1,2) → [3, 1, 2]
        start=2: swap(2,2) → [3, 1, 2] ✓ RECORD
      undo swap → [3, 2, 1]
    undo all swaps → [1, 2, 3]

  KEY INSIGHT: swap(i, start) puts element i at position 'start'
  Then recurse on start+1, and all elements after start are still available.
  This avoids the need for a "used" array!
```

**Complexity**: O(N * N!) time, O(N) space (recursion stack).

---

## Permutations II

### Problem
Given a collection that might contain duplicates, return all unique permutations.

### Approach: Sort + skip duplicates

```python
def permute_unique(nums):
    result = []
    nums.sort()
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            # KEY PRUNING: skip duplicates
            # If current equals previous and previous was NOT used,
            # we would generate the same permutation again
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result

# Example
print(permute_unique([1, 1, 2]))
# [[1,1,2], [1,2,1], [2,1,1]]
```

### Why the duplicate condition works

```
  SORTING [1, 1, 2] FIRST:
  ═════════════════════════

  After sorting: [1_a, 1_b, 2]  (labeling duplicates as 1_a and 1_b)
                  ^^^^  ^^^^
                  same value but different indices

  WITHOUT duplicate pruning (produces duplicates):
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │  Pick at pos 0:  Pick at pos 0:  Pick at pos 0:            │
  │  [1_a]           [1_b]           [2]                        │
  │   / \            / \             / \                        │
  │ 1_b  2        1_a  2          1_a  1_b                     │
  │  |    |        |    |          |    |                       │
  │  2   1_b      2   1_a        1_b  1_a                      │
  │                                                             │
  │  [1_a,1_b,2]   [1_b,1_a,2]   [2,1_a,1_b]                  │
  │  [1_a,2,1_b]   [1_b,2,1_a]   [2,1_b,1_a]                  │
  │                                                             │
  │  DUPLICATES: [1_a,1_b,2] same as [1_b,1_a,2]!             │
  └─────────────────────────────────────────────────────────────┘

  WITH duplicate pruning:
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │  Pick at pos 0:  Pick at pos 0:  Pick at pos 0:            │
  │  [1_a]           [1_b] ❌ SKIP   [2]                        │
  │   / \            (1_a was tried  / \                        │
  │ 1_b  2           at this pos   1_a  1_b                     │
  │  |    |          but 1_a was   |    |                       │
  │  2   1_b         NOT used, so  1_b  1_a                     │
  │                  same value → skip)                          │
  │  [1_a,1_b,2]    SKIPPED!       [2,1_a,1_b]                 │
  │  [1_a,2,1_b]                  [2,1_b,1_a] ❌ SKIP           │
  │                                                             │
  │  FINAL: [1,1,2], [1,2,1], [2,1,1]  ← 3 unique perms       │
  │  (instead of 6 total with duplicates)                       │
  └─────────────────────────────────────────────────────────────┘

  THE KEY LOGIC:
  ═══════════════
  if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
      continue

  "If current value == previous value AND previous was NOT used
   at this recursion level, skip current."

  WHY: If previous (same value) was already tried and undone at this level,
  then trying current (same value) would produce the same permutation.
  We only allow the FIRST occurrence of a duplicate value at each level.
```

After sorting `[1, 1, 2]`:
- At position 0: we pick index 0 (value 1). used = [T, F, F]
- At position 1: index 1 has same value as index 0, but index 0 IS used, so we allow it
- At position 1: index 1 (value 1). We pick it. used = [T, T, F]
- Backtrack. Now try position 1 with index 0 (value 1) again
- BUT index 0 is already used. Skip.
- **The key**: when we backtrack and `used[i-1]` is False (meaning we already tried this value at this position with a different previous), we skip.

**Complexity**: O(N * N!) time in worst case (fewer duplicates = closer to N!). Space: O(N).

---

## Combinations

### Problem
Given n and k, return all combinations of k numbers from 1 to n.

### Visual: Combination Tree for combine(4, 2)

```
  COMBINATIONS OF 2 FROM {1, 2, 3, 4}:
  ═══════════════════════════════════════

  Total = C(4,2) = 4! / (2! × 2!) = 6

  Decision Tree:
                              []
                    ┌────┬────┼────┐
                  pick 1 pick 2 pick 3 pick 4
                  [1]    [2]    [3]    [4]
                  / \    / \     |      |
                2   3  3   4   4      DONE
               / \   |  |   |
              3   4  4  4  DONE
               |   |
              DONE DONE

  ALL PATHS:
  ══════════
  [1] → [1,2] → record    (picked 1 then 2)
  [1] → [1,3] → record    (picked 1 then 3)
  [1] → [1,4] → record    (picked 1 then 4)
  [2] → [2,3] → record    (picked 2 then 3)
  [2] → [2,4] → record    (picked 2 then 4)
  [3] → [3,4] → record    (picked 3 then 4)

  NOTE: [2,1] is NOT generated because we only pick
  elements AFTER the current index. This avoids duplicates
  because order doesn't matter in combinations: {1,2} = {2,1}

  PRUNING VISUALIZED:
  ════════════════════
  For combine(4, 2), at each level:
  - Level 0 (picking 1st): need 2 more elements
    → can only pick up to index n - remaining + 1 = 4 - 2 + 1 = 3
    → range(1, 4) = [1, 2, 3] (skip 4, not enough room for 2nd pick)

  - Level 1 (picking 2nd): need 1 more element
    → range(pick+1, 5) = [pick+1, ..., 4]

  Without pruning: we'd try all starting positions including impossible ones.
  With pruning: we skip branches where not enough elements remain.
```

### Approach: Backtracking with start index

```python
def combine(n, k):
    result = []

    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        # Pruning: not enough numbers left to fill the path
        for i in range(start, n - (k - len(path)) + 2):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()

    backtrack(1, [])
    return result

# Example
print(combine(4, 2))
# [[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]
```

**Pruning explained**: At any point, if we have `remaining = k - len(path)` spots to fill, we need at least `remaining` numbers. The last number we can pick is `n - remaining + 1`. So `range(start, n - remaining + 2)`.

**Complexity**: O(C(n,k) * k) time, O(k) space.

---

## Combination Sum

### Combination Sum I (repetition allowed)

Given candidates and target, find all unique combinations. Same number can be reused unlimited times.

```python
def combination_sum(candidates, target):
    result = []
    candidates.sort()  # SORT FIRST: enables pruning (break when > remaining)

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])  # COPY the current path
            return

        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # PRUNE: sorted, so all future candidates are also > remaining

            path.append(candidates[i])                           # MAKE CHOICE
            backtrack(i, path, remaining - candidates[i])        # RECURSE (i, not i+1!)
            path.pop()                                           # UNDO CHOICE

    backtrack(0, [], target)
    return result

# Example
print(combination_sum([2, 3, 6, 7], 7))
# [[2,2,3], [7]]
```

**KEY INSIGHT**: We pass `i` (not `i+1`) as the start index. This allows the same element to be reused. If we passed `i+1`, each element could only be used once (like Combination Sum II).

### Combination Sum II (no repetition, handle duplicates)

Each number can only be used once. Input may contain duplicates.

```python
def combination_sum_2(candidates, target):
    result = []
    candidates.sort()  # SORT: enables pruning AND duplicate detection

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return

        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # PRUNE: sorted, so all remaining are too large

            # SKIP DUPLICATES at the same recursion level
            # If current == previous, and we're not at the start of this level,
            # skip to avoid generating the same combination twice
            if i > start and candidates[i] == candidates[i - 1]:
                continue

            path.append(candidates[i])                              # MAKE CHOICE
            backtrack(i + 1, path, remaining - candidates[i])      # i+1: NO REUSE
            path.pop()                                             # UNDO CHOICE

    backtrack(0, [], target)
    return result

# Example
print(combination_sum_2([10, 1, 2, 7, 6, 1, 5], 8))
# [[1,1,6], [1,2,5], [1,7], [2,6]]
```

**KEY DIFFERENCE from Combination Sum I**:
- Pass `i+1` (not `i`) → each element used at most once
- Skip duplicates at same level → avoid duplicate combinations
- Combination Sum I: `backtrack(i, ...)` + no duplicate skip needed
- Combination Sum II: `backtrack(i+1, ...)` + skip `if i > start and nums[i]==nums[i-1]`

### Combination Sum III

Find all combinations of k numbers (1-9) that sum to n.

```python
def combination_sum_3(k, n):
    result = []

    def backtrack(start, path, remaining):
        if len(path) == k and remaining == 0:
            result.append(path[:])
            return
        for i in range(start, 10):
            if i > remaining:
                break
            path.append(i)
            backtrack(i + 1, path, remaining - i)
            path.pop()

    backtrack(1, [], n)
    return result

# Example
print(combination_sum_3(3, 7))
# [[1,2,4]]
```

**Complexity Summary**:
| Problem | Time | Space |
|---------|------|-------|
| Comb Sum I | O(N^(T/M)) where M=min candidate | O(T/M) |
| Comb Sum II | O(2^N) | O(N) |
| Comb Sum III | O(C(9,k)) | O(k) |

---

## Subsets

### Subsets I

Given a set of distinct integers, return all possible subsets.

### Visual: Subset Generation for [1, 2, 3]

```
  POWER SET OF {1, 2, 3}:
  ════════════════════════

  Total subsets = 2^3 = 8

  BINARY REPRESENTATION (each bit = include/exclude):
  ┌─────┬─────┬─────┬───────────────┐
  │  1  │  2  │  3  │ Subset        │
  ├─────┼─────┼─────┼───────────────┤
  │  0  │  0  │  0  │ []            │ ← empty set (always included)
  │  0  │  0  │  1  │ [3]           │
  │  0  │  1  │  0  │ [2]           │
  │  0  │  1  │  1  │ [2, 3]        │
  │  1  │  0  │  0  │ [1]           │
  │  1  │  0  │  1  │ [1, 3]        │
  │  1  │  1  │  0  │ [1, 2]        │
  │  1  │  1  │  1  │ [1, 2, 3]     │ ← full set
  └─────┴─────┴─────┴───────────────┘

  DECISION TREE (start-index approach):
  ═════════════════════════════════════

                              [] ← record empty set
                    ┌────┬────┼────┐
                  pick 1 pick 2 pick 3
                  [1]    [2]    [3]  ← record each single
                  / \    / \     |
               2    3  3   DONE  DONE
              / \    |
             3  DONE DONE
              |
           DONE

  Path: [] → [1] → [1,2] → [1,2,3]
                                    ↓
  Backtrack:                 [1,2] → record
                                    ↓
  Backtrack:                 [1] → [1,3] → record
                                    ↓
  Backtrack:             [1] → record, then []
                                    ↓
                           [] → [2] → [2,3] → record
                                    ↓
                           [] → [2] → record, then []
                                    ↓
                           [] → [3] → record, then []

  NOTE: At each node, we RECORD the current path as a subset!
  This is different from permutations where we only record at leaves.
```

```python
def subsets(nums):
    result = []

    def backtrack(start, path):
        result.append(path[:])  # Record current subset at EVERY node (not just leaves!)
        for i in range(start, len(nums)):
            path.append(nums[i])         # MAKE CHOICE: include nums[i]
            backtrack(i + 1, path)       # RECURSE: only consider elements AFTER i
            path.pop()                   # UNDO CHOICE: remove nums[i]

    backtrack(0, [])
    return result

# Example
print(subsets([1, 2, 3]))
# [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
```

### Iterative approach (BFS-style)

```python
def subsets_iterative(nums):
    result = [[]]
    for num in nums:
        # For each existing subset, create a new one with 'num' added
        result += [subset + [num] for subset in result]
    return result

# Step by step for [1, 2, 3]:
# Start: result = [[]]
# num=1: result = [[], [1]]
# num=2: result = [[], [1], [2], [1,2]]
# num=3: result = [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
```

### Subsets II (with duplicates)

Given a collection that might contain duplicates, return all unique subsets.

### Visual: Duplicate Handling for [1, 2, 2]

```
  SORTED INPUT: [1, 2, 2]
                  ^  ^ ^
                  a  b c  (two 2's)

  WITHOUT DUPLICATE PRUNING:
  ┌─────────────────────────────────────────────────────────────┐
  │  [] → [1] → [1,2_a] → [1,2_a,2_b] ✓                       │
  │       [1] → [1,2_b] → [1,2_b,2_a] ❌ DUPLICATE of above!  │
  │       [2_a] → [2_a,2_b] ✓                                   │
  │       [2_b] → [2_b,2_a] ❌ DUPLICATE!                       │
  │  ...                                                        │
  │  Total: 8 subsets (with duplicates)                         │
  └─────────────────────────────────────────────────────────────┘

  WITH DUPLICATE PRUNING (if i > start and nums[i] == nums[i-1]):
  ┌─────────────────────────────────────────────────────────────┐
  │  [] → [1] → [1,2_a] → [1,2_a,2_b] ✓                       │
  │       [1] → [1,2_b] ❌ SKIPPED (2_b==2_a at same level)   │
  │       [2_a] → [2_a,2_b] ✓                                   │
  │       [2_b] ❌ SKIPPED (2_b==2_a at same level)             │
  └─────────────────────────────────────────────────────────────┘
  Total: 6 unique subsets

  THE PRUNING RULE:
  if i > start and nums[i] == nums[i-1]:
      continue
  This skips the SECOND (and subsequent) occurrences of a value
  at the same recursion level, preventing duplicate subsets.
```

```python
def subsets_with_dup(nums):
    result = []
    nums.sort()  # SORT FIRST: duplicates must be adjacent for pruning to work

    def backtrack(start, path):
        result.append(path[:])  # Record at every node (subset pattern)
        for i in range(start, len(nums)):
            # Skip duplicates at the same recursion level
            # i > start: not the first element in this loop iteration
            # nums[i] == nums[i-1]: same value as previous
            # Together: skip repeated values at the same level
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result

# Example
print(subsets_with_dup([1, 2, 2]))
# [[], [1], [1,2], [1,2,2], [2], [2,2]]
```

**Complexity**: O(2^N) time, O(N) space for both. Subsets II prunes duplicate subsets.

---

## Next Permutation

### Problem
Rearrange numbers into the lexicographically next greater permutation. If no greater permutation, rearrange to the lowest.

### Approach: One-pass from right

```python
def next_permutation(nums):
    n = len(nums)

    # Step 1: Find the rightmost element that is smaller than its next
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    if i >= 0:
        # Step 2: Find the rightmost element greater than nums[i]
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        # Step 3: Swap
        nums[i], nums[j] = nums[j], nums[i]

    # Step 4: Reverse the suffix starting at i+1
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1

    return nums

# Example
print(next_permutation([1, 2, 3]))   # [1, 3, 2]
print(next_permutation([3, 2, 1]))   # [1, 2, 3] (wraps around)
print(next_permutation([1, 1, 5]))   # [1, 5, 1]
```

### Walkthrough with [1, 3, 5, 4, 2]

```
Step 1: Find i where nums[i] < nums[i+1]
  1  3  5  4  2
        ^  i=2 is 5 > 4, no
     ^  i=1 is 3 < 5, YES → i=1

Step 2: Find j where nums[j] > nums[i]=3
  1  3  5  4  2
           ^  j=3 is 4 > 3, YES → j=3

Step 3: Swap nums[i] and nums[j]
  1 [4] 5 [3] 2

Step 4: Reverse suffix from i+1=2
  1  4  [5, 3, 2] → [2, 3, 5]
  1  4  2  3  5
```

**Complexity**: O(N) time, O(1) space. This is a classic interview problem.

---

## Permutation Sequence

### Problem
Given n and k, return the k-th permutation sequence (lexicographic order).

### Approach 1: Backtracking (brute force — TLE on large inputs)

```python
def get_permutation(n, k):
    nums = list(range(1, n + 1))
    result = []
    used = [False] * n

    def backtrack(path):
        if len(path) == n:
            result.append(''.join(map(str, path)))
            return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False
            if len(result) == k:
                return

    backtrack([])
    return result[k - 1]
```

### Approach 2: Math-based (optimal)

```python
def get_permutation_math(n, k):
    import math
    nums = list(range(1, n + 1))
    k -= 1  # 0-indexed
    result = []

    for i in range(n, 0, -1):
        fact = math.factorial(i - 1)
        index = k // fact
        k %= fact
        result.append(str(nums[index]))
        nums.pop(index)

    return ''.join(result)

# Example
print(get_permutation_math(3, 3))   # "213"
print(get_permutation_math(4, 9))   # "2314"
```

### How the math approach works

```
  FINDING THE 9th PERMUTATION OF {1, 2, 3, 4} (1-indexed):
  ══════════════════════════════════════════════════════════

  There are 4! = 24 permutations. In lex order, they're grouped by first digit:
  ┌─────────────────────────────────────────────────────────────────┐
  │  First digit │ Permutations │ Count │ Cumulative                │
  ├─────────────────────────────────────────────────────────────────┤
  │     1        │ 1xxx         │  6    │  1-6                     │
  │     2        │ 2xxx         │  6    │  7-12  ← 9 falls here!  │
  │     3        │ 3xxx         │  6    │  13-18                   │
  │     4        │ 4xxx         │  6    │  19-24                   │
  └─────────────────────────────────────────────────────────────────┘

  For n=4, k=9 (1-indexed → k=8 0-indexed):
  Factorials: 3!=6, 2!=2, 1!=1, 0!=1

  Step-by-step:
  ┌──────────────────────────────────────────────────────────────────┐
  │  Step 1: k=8, 3!=6                                              │
  │    index = 8 // 6 = 1 → pick nums[1] = 2                       │
  │    remaining = [1, 3, 4], k = 8 % 6 = 2                         │
  │                                                                  │
  │  Step 2: k=2, 2!=2                                              │
  │    index = 2 // 2 = 1 → pick nums[1] = 3                       │
  │    remaining = [1, 4], k = 2 % 2 = 0                            │
  │                                                                  │
  │  Step 3: k=0, 1!=1                                              │
  │    index = 0 // 1 = 0 → pick nums[0] = 1                       │
  │    remaining = [4], k = 0                                        │
  │                                                                  │
  │  Step 4: k=0, 0!=1                                              │
  │    index = 0 → pick nums[0] = 4                                 │
  │                                                                  │
  │  Result: "2314"                                                  │
  └──────────────────────────────────────────────────────────────────┘

  WHY IT WORKS:
  =============
  The first digit divides all permutations into n!/n equal groups.
  k // (n-1)! tells us WHICH group → which first digit.
  k % (n-1)! tells us the POSITION within that group → recurse.

  Think of it like a number system:
  - Position 0 uses factorials: k = d₁×3! + d₂×2! + d₃×1! + d₄×0!
  - Each dᵢ is the index into remaining digits
```

**Complexity**: Approach 1 is O(N! * N), Approach 2 is O(N^2) (or O(N) with a set for removal).

---

## Gray Code

### Problem
Generate n-bit Gray code sequence where successive values differ in only one bit.

### Visual: Gray Code for n=3

```
  GRAY CODE vs BINARY:
  ════════════════════

  Decimal │ Binary │ Gray Code
  ────────┼────────┼──────────
     0    │  000   │  000
     1    │  001   │  001  ← differs from 000 in bit 0
     2    │  010   │  011  ← differs from 001 in bit 1
     3    │  011   │  010  ← differs from 011 in bit 0
     4    │  100   │  110  ← differs from 010 in bit 2
     5    │  101   │  111  ← differs from 110 in bit 0
     6    │  110   │  101  ← differs from 111 in bit 1
     7    │  111   │  100  ← differs from 101 in bit 2

  KEY: Each consecutive pair differs by EXACTLY 1 bit!
  Binary: 011 → 100 changes 3 bits ❌
  Gray:   010 → 110 changes 1 bit  ✓

  RECURSIVE STRUCTURE:
  ════════════════════
  Gray(1): [0, 1]

  Gray(2): Take Gray(1), mirror it with prefix 0 and 1:
           0: [0, 1]  →  00, 01
           1: [1, 0]  →  11, 10  (reversed, with leading 1)
           Result: [00, 01, 11, 10]

  Gray(3): Take Gray(2), mirror with prefix 0 and 1:
           0: [00, 01, 11, 10]  →  000, 001, 011, 010
           1: [10, 11, 01, 00]  →  110, 111, 101, 100
           Result: [000, 001, 011, 010, 110, 111, 101, 100]
```

### Approach 1: Formula-based

```python
def gray_code(n):
    return [i ^ (i >> 1) for i in range(2 ** n)]

# Example
print(gray_code(3))
# [0, 1, 3, 2, 6, 7, 5, 4]
# Binary: 000, 001, 011, 010, 110, 111, 101, 100
```

### Approach 2: Recursive

```python
def gray_code_recursive(n):
    if n == 1:
        return [0, 1]
    prev = gray_code_recursive(n - 1)
    result = []
    for code in prev:
        result.append(code)
    for code in reversed(prev):
        result.append(code + (1 << (n - 1)))
    return result

# Example
print(gray_code_recursive(3))
# [0, 1, 3, 2, 6, 7, 5, 4]
```

### Approach 3: Backtracking (build one by one)

```python
def gray_code_backtrack(n):
    result = [0]
    visited = {0}

    def backtrack():
        if len(result) == 2 ** n:
            return True
        current = result[-1]
        for bit in range(n):
            next_val = current ^ (1 << bit)
            if next_val not in visited:
                visited.add(next_val)
                result.append(next_val)
                if backtrack():
                    return True
                result.pop()
                visited.remove(next_val)
        return False

    backtrack()
    return result

# Example
print(gray_code_backtrack(3))
# [0, 1, 3, 2, 6, 7, 5, 4]
```

**Complexity**: O(2^N) for all approaches. Formula-based is O(2^N) time and space.

---

## Quick Reference

| Problem | Time Complexity | Space Complexity | Key Technique |
|---------|----------------|------------------|---------------|
| Permutations | O(N * N!) | O(N) | Used array |
| Permutations II | O(N * N!) | O(N) | Sort + skip dupes |
| Combinations | O(C(N,K) * K) | O(K) | Start index |
| Combination Sum I | O(N^(T/M)) | O(T/M) | Sort + reuse |
| Combination Sum II | O(2^N) | O(N) | Sort + skip dupes |
| Subsets | O(2^N * N) | O(N) | Start index |
| Subsets II | O(2^N * N) | O(N) | Sort + skip dupes |
| Next Permutation | O(N) | O(1) | One-pass from right |
| Permutation Sequence | O(N^2) | O(N) | Factorial math |
| Gray Code | O(2^N) | O(2^N) | Bit manipulation |
