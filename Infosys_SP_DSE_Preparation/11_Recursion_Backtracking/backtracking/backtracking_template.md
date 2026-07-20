# Backtracking — Template & Classic Problems

## Table of Contents
1. [Universal Backtracking Template](#universal-backtracking-template)
2. [Decision Space Exploration](#decision-space-exploration)
3. [Pruning Techniques](#pruning-techniques)
4. [N-Queens](#n-queens)
5. [Sudoku Solver](#sudoku-solver)
6. [Word Search](#word-search)
7. [Palindrome Partitioning](#palindrome-partitioning)
8. [Restore IP Addresses](#restore-ip-addresses)
9. [Letter Combinations of Phone Number](#letter-combinations-of-phone-number)
10. [Combination Sum I, II, III](#combination-sum)
11. [Permutations I, II](#permutations)

---

## Universal Backtracking Template

```python
def backtrack(path, choices):
    # BASE CASE: when should we record a solution?
    if meet_condition:
        result.append(path[:])  # always copy!
        return

    for choice in choices:
        # PRUNING: skip invalid choices early
        if not valid(choice):
            continue

        # MAKE CHOICE
        path.append(choice)

        # RECURSE: explore with updated choices
        backtrack(path, new_choices_for(choice))

        # UNDO CHOICE (backtrack)
        path.pop()
```

### Template Variants

```python
# Variant 1: Find ONE solution (return True to stop early)
def backtrack_one(path, choices):
    if is_solution(path):
        return True  # stop searching

    for choice in choices:
        path.append(choice)
        if backtrack_one(path, next_choices(choice)):
            return True  # propagate stop signal
        path.pop()

    return False  # no solution found


# Variant 2: Count solutions
def backtrack_count(path, choices):
    if is_solution(path):
        return 1

    count = 0
    for choice in choices:
        path.append(choice)
        count += backtrack_count(path, next_choices(choice))
        path.pop()

    return count


# Variant 3: Find BEST solution (optimization)
def backtrack_best(path, choices):
    if is_solution(path):
        return evaluate(path)

    best = float('-inf')
    for choice in choices:
        path.append(choice)
        best = max(best, backtrack_best(path, next_choices(choice)))
        path.pop()

    return best
```

---

## Decision Space Exploration

The "decision space" is all the choices you can make at each step. How you structure it determines efficiency.

### Approach 1: Index-based (most common for combinations/subsets)

```python
# Avoid duplicates by only considering elements AFTER current index
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
```

### Approach 2: Used array (for permutations)

```python
def permutations(nums):
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
```

### Approach 3: Remaining set (cleaner but uses more memory)

```python
def permutations(nums):
    result = []

    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])
            return
        for num in list(remaining):
            current.append(num)
            backtrack(current, remaining - {num})
            current.pop()

    backtrack([], set(nums))
    return result
```

### Approach 4: Position-based (for placement problems like N-Queens)

```python
def solve_n_queens(n):
    result = []

    def backtrack(row, queens):
        if row == n:
            result.append(queens[:])
            return
        for col in range(n):
            if is_safe(row, col, queens):
                queens.append(col)
                backtrack(row + 1, queens)
                queens.pop()

    def is_safe(row, col, queens):
        for r, c in enumerate(queens):
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True

    backtrack(0, [])
    return result
```

---

## Pruning Techniques

Pruning eliminates branches of the search tree that cannot lead to a solution.

### 1. Sort and Early Termination (for sum/target problems)

```python
def combination_sum(candidates, target):
    result = []
    candidates.sort()  # Sort first!

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # PRUNE: all remaining are larger too
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])
            path.pop()

    backtrack(0, [], target)
    return result
```

### 2. Skip Duplicates

```python
def permutation_unique(nums):
    result = []
    nums.sort()

    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            # Skip duplicates: same value, previous same value not used
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False

    backtrack([], [False] * len(nums))
    return result
```

### 3. Bounds Checking

```python
def subsets_with_sum(nums, target):
    result = []
    nums.sort()

    def backtrack(start, path, current_sum):
        if current_sum == target:
            result.append(path[:])
            return
        for i in range(start, len(nums)):
            if current_sum + nums[i] > target:
                break  # PRUNE
            path.append(nums[i])
            backtrack(i + 1, path, current_sum + nums[i])
            path.pop()

    backtrack(0, [], 0)
    return result
```

### 4. Forward-Looking Pruning

```python
def partition_palindrome(s):
    result = []

    def backtrack(start, path):
        if start == len(s):
            result.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            substring = s[start:end]
            if substring != substring[::-1]:
                continue  # PRUNE: not a palindrome
            path.append(substring)
            backtrack(end, path)
            path.pop()

    backtrack(0, [])
    return result
```

---

## N-Queens

Place N queens on an N x N chessboard such that no two queens attack each other.

### Solution 1: Row-by-row placement

```python
def solve_n_queens(n):
    result = []
    board = [['.' for _ in range(n)] for _ in range(n)]

    def is_safe(row, col):
        for r in range(row):
            if board[r][col] == 'Q':
                return False
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0:
            if board[r][c] == 'Q':
                return False
            r -= 1
            c -= 1
        r, c = row - 1, col + 1
        while r >= 0 and c < n:
            if board[r][c] == 'Q':
                return False
            r -= 1
            c += 1
        return True

    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            if not is_safe(row, col):
                continue
            board[row][col] = 'Q'
            backtrack(row + 1)
            board[row][col] = '.'

    backtrack(0)
    return result


# Count solutions only
def n_queens_count(n):
    count = 0
    cols = set()
    diag1 = set()  # row + col
    diag2 = set()  # row - col

    def backtrack(row):
        nonlocal count
        if row == n:
            count += 1
            return
        for col in range(n):
            if col in cols or (row + col) in diag1 or (row - col) in diag2:
                continue
            cols.add(col)
            diag1.add(row + col)
            diag2.add(row - col)
            backtrack(row + 1)
            cols.remove(col)
            diag1.remove(row + col)
            diag2.remove(row - col)

    backtrack(0)
    return count
```

### Solution 2: Using sets for O(1) safety checks

```python
def solve_n_queens_optimized(n):
    result = []
    board = [-1] * n
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    def backtrack(row):
        if row == n:
            result.append(board[:])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row] = col
            backtrack(row + 1)
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            board[row] = -1

    backtrack(0)
    return result
```

**Complexity**: O(N!) time, O(N) space.

---

## Sudoku Solver

Fill a 9x9 grid so each row, column, and 3x3 box contains digits 1-9 exactly once.

```python
def solve_sudoku(board):
    def is_valid(row, col, num):
        for c in range(9):
            if board[row][c] == num:
                return False
        for r in range(9):
            if board[r][col] == num:
                return False
        box_r, box_c = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                if board[r][c] == num:
                    return False
        return True

    def find_empty():
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    return (r, c)
        return None

    def backtrack():
        pos = find_empty()
        if pos is None:
            return True
        row, col = pos
        for num in '123456789':
            if not is_valid(row, col, num):
                continue
            board[row][col] = num
            if backtrack():
                return True
            board[row][col] = '.'
        return False

    backtrack()
    return board


# Optimized with sets
def solve_sudoku_optimized(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []

    for r in range(9):
        for c in range(9):
            if board[r][c] == '.':
                empty.append((r, c))
            else:
                num = board[r][c]
                rows[r].add(num)
                cols[c].add(num)
                boxes[3 * (r // 3) + c // 3].add(num)

    def backtrack(idx):
        if idx == len(empty):
            return True
        r, c = empty[idx]
        b = 3 * (r // 3) + c // 3
        for num in '123456789':
            if num in rows[r] or num in cols[c] or num in boxes[b]:
                continue
            board[r][c] = num
            rows[r].add(num)
            cols[c].add(num)
            boxes[b].add(num)
            if backtrack(idx + 1):
                return True
            board[r][c] = '.'
            rows[r].remove(num)
            cols[c].remove(num)
            boxes[b].remove(num)
        return False

    backtrack(0)
    return board
```

**Complexity**: O(9^empty_cells) worst case, but pruning makes it fast in practice.

---

## Word Search

Given a 2D grid and a word, find if the word exists in the grid. Move up/down/left/right. Each cell used only once.

```python
def exist(board, word):
    if not board or not board[0]:
        return False
    rows, cols = len(board), len(board[0])

    def backtrack(r, c, idx):
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != word[idx]:
            return False

        temp = board[r][c]
        board[r][c] = '#'  # mark visited

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if backtrack(r + dr, c + dc, idx + 1):
                return True

        board[r][c] = temp  # restore
        return False

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0]:
                if backtrack(r, c, 0):
                    return True
    return False
```

**Complexity**: O(M * N * 4^L) where L = len(word). Space: O(L) for recursion stack.

---

## Palindrome Partitioning

Given a string s, partition s such that every substring is a palindrome.

```python
def partition_palindrome(s):
    result = []

    def is_palindrome(sub):
        return sub == sub[::-1]

    def backtrack(start, path):
        if start == len(s):
            result.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            substring = s[start:end]
            if not is_palindrome(substring):
                continue
            path.append(substring)
            backtrack(end, path)
            path.pop()

    backtrack(0, [])
    return result


# Optimized with memoized palindrome checks
def partition_palindrome_optimized(s):
    result = []
    n = len(s)
    # Precompute palindromes
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            sub = s[i:j + 1]
            is_pal[i][j] = (sub == sub[::-1])

    def backtrack(start, path):
        if start == n:
            result.append(path[:])
            return
        for end in range(start, n):
            if not is_pal[start][end]:
                continue
            path.append(s[start:end + 1])
            backtrack(end + 1, path)
            path.pop()

    backtrack(0, [])
    return result
```

**Complexity**: O(N * 2^N). There are 2^(N-1) possible partitions and each takes O(N) to check.

---

## Restore IP Addresses

Given a string containing only digits, restore all possible valid IP addresses.

```python
def restore_ip_addresses(s):
    result = []

    def backtrack(start, path):
        if len(path) == 4:
            if start == len(s):
                result.append('.'.join(path))
            return
        for length in range(1, 4):
            if start + length > len(s):
                break
            segment = s[start:start + length]
            # No leading zeros (except "0" itself)
            if len(segment) > 1 and segment[0] == '0':
                break
            if int(segment) > 255:
                continue
            path.append(segment)
            backtrack(start + length, path)
            path.pop()

    backtrack(0, [])
    return result
```

**Complexity**: O(1) — IP has at most 12 digits and 4 segments, so constant time.

---

## Letter Combinations of Phone Number

Given a string of digits (2-9), return all possible letter combinations.

```python
def letter_combinations(digits):
    if not digits:
        return []
    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    result = []

    def backtrack(idx, path):
        if idx == len(digits):
            result.append(''.join(path))
            return
        for letter in phone[digits[idx]]:
            path.append(letter)
            backtrack(idx + 1, path)
            path.pop()

    backtrack(0, [])
    return result
```

**Complexity**: O(4^N * N) where N = len(digits). Each digit maps to 3-4 letters.

---

## Combination Sum

### Combination Sum I (elements reusable)

Given an array of candidates and a target, find all unique combinations where elements can be reused.

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
                break
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i, not i+1 (reuse allowed)
            path.pop()

    backtrack(0, [], target)
    return result
```

### Combination Sum II (no duplicates, each element used once)

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
            backtrack(i + 1, path, remaining - candidates[i])  # i+1 (no reuse)
            path.pop()

    backtrack(0, [], target)
    return result
```

### Combination Sum III

Find all combinations of k numbers that add up to n (numbers from 1-9, each used once).

```python
def combination_sum_3(k, n):
    result = []

    def backtrack(start, path, remaining):
        if len(path) == k and remaining == 0:
            result.append(path[:])
            return
        if len(path) > k or remaining < 0:
            return
        for i in range(start, 10):
            path.append(i)
            backtrack(i + 1, path, remaining - i)
            path.pop()

    backtrack(1, [], n)
    return result
```

---

## Permutations

### Permutations I

```python
def permutations(nums):
    result = []

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for num in nums:
            if num in path:  # skip if already used
                continue
            path.append(num)
            backtrack(path)
            path.pop()

    backtrack([])
    return result


# More efficient: use used array
def permutations_efficient(nums):
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
```

### Permutations II (with duplicates)

```python
def permutations_unique(nums):
    result = []
    nums.sort()  # sort to group duplicates

    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            # Skip duplicate: same as prev, but prev wasn't used in this position
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False

    backtrack([], [False] * len(nums))
    return result
```

**Key insight for duplicates**: Sort the array first. When iterating, if `nums[i] == nums[i-1]` and `nums[i-1]` was NOT used at this recursion level (`not used[i-1]`), skip it. This ensures we only pick the first occurrence of a duplicate value at each position.

---

## Summary — Template Recognition Guide

| Pattern | Start Parameter | Loop Range | Key Pruning |
|---------|----------------|------------|-------------|
| Subsets | `start = 0` | `range(start, n)` | None usually |
| Permutations | No start | `range(n)` | `used` array |
| Combination Sum | `start = 0` | `range(start, n)` | Sort + break on overflow |
| Partition | `start = 0` | `range(start+1, n+1)` | Check palindrome |
| N-Queens | `row = 0` | `range(n)` | Check safety sets |
| Word Search | `(r, c)` | 4 directions | Bounds + match check |
