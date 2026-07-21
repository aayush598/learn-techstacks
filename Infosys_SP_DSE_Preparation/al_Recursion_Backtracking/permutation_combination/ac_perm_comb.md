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

### Approach: Backtracking with used array

```python
def permute(nums):
    result = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result

# Example
print(permute([1, 2, 3]))
# [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
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
    candidates.sort()

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # PRUNE: sorted, so all future are bigger
            path.append(candidates[i])
            # Use i (not i+1) because repetition is allowed
            backtrack(i, path, remaining - candidates[i])
            path.pop()

    backtrack(0, [], target)
    return result

# Example
print(combination_sum([2, 3, 6, 7], 7))
# [[2,2,3], [7]]
```

### Combination Sum II (no repetition, handle duplicates)

Each number can only be used once. Input may contain duplicates.

```python
def combination_sum_2(candidates, target):
    result = []
    candidates.sort()

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            # Skip duplicates at the same level
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])  # i+1: no reuse
            path.pop()

    backtrack(0, [], target)
    return result

# Example
print(combination_sum_2([10, 1, 2, 7, 6, 1, 5], 8))
# [[1,1,6], [1,2,5], [1,7], [2,6]]
```

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

```python
def subsets(nums):
    result = []

    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

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
        result += [subset + [num] for subset in result]
    return result
```

### Subsets II (with duplicates)

Given a collection that might contain duplicates, return all unique subsets.

```python
def subsets_with_dup(nums):
    result = []
    nums.sort()

    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            # Skip duplicates at the same level
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

For n=4, k=9 (1-indexed → k=8 0-indexed):
- Factorials: 3!=6, 2!=2, 1!=1
- Position 0: index = 8//6 = 1 → pick nums[1]=2. Remaining nums=[1,3,4]. k=8%6=2
- Position 1: index = 2//2 = 1 → pick nums[1]=3. Remaining nums=[1,4]. k=2%2=0
- Position 2: index = 0//1 = 0 → pick nums[0]=1. Remaining nums=[4]. k=0
- Position 3: index = 0 → pick nums[0]=4
- Result: "2314"

**Complexity**: Approach 1 is O(N! * N), Approach 2 is O(N^2) (or O(N) with a set for removal).

---

## Gray Code

### Problem
Generate n-bit Gray code sequence where successive values differ in only one bit.

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
