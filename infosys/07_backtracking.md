# Backtracking

## Problem 1: N-Queens
**Difficulty: Hard | Marks: 50**

```python
def solve_n_queens(n):
    cols = set()
    pos_diag = set()  # r + c
    neg_diag = set()  # r - c
    board = [['.'] * n for _ in range(n)]
    result = []

    def backtrack(r):
        if r == n:
            result.append([''.join(row) for row in board])
            return
        for c in range(n):
            if c in cols or (r + c) in pos_diag or (r - c) in neg_diag:
                continue
            cols.add(c)
            pos_diag.add(r + c)
            neg_diag.add(r - c)
            board[r][c] = 'Q'
            backtrack(r + 1)
            cols.remove(c)
            pos_diag.remove(r + c)
            neg_diag.remove(r - c)
            board[r][c] = '.'

    backtrack(0)
    return result

result = solve_n_queens(4)
for board in result:
    for row in board:
        print(row)
    print()
```

---

## Problem 2: Permutations
**Difficulty: Medium | Marks: 30**

```python
def permute(nums):
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                path.append(nums[i])
                backtrack(path, used)
                path.pop()
                used[i] = False
    result = []
    backtrack([], [False] * len(nums))
    return result

print(permute([1, 2, 3]))
```

---

## Problem 3: Unique Permutations (With Duplicates)
**Difficulty: Medium | Marks: 30**

```python
def permute_unique(nums):
    nums.sort()
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    result = []
    backtrack([], [False] * len(nums))
    return result

print(permute_unique([1, 1, 2]))
```

---

## Problem 4: Subsets (All Possible Subsets)
**Difficulty: Medium | Marks: 30**

```python
def subsets_backtrack(nums):
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    result = []
    backtrack(0, [])
    return result

print(subsets_backtrack([1, 2, 3]))
```

---

## Problem 5: Subsets II (With Duplicates)
**Difficulty: Medium | Marks: 30**

```python
def subsets_with_dup(nums):
    nums.sort()
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    result = []
    backtrack(0, [])
    return result

print(subsets_with_dup([1, 2, 2]))
```

---

## Problem 6: Combination Sum
**Difficulty: Medium | Marks: 30**

```python
def combination_sum(candidates, target):
    def backtrack(remaining, start, path):
        if remaining == 0:
            result.append(path[:])
            return
        if remaining < 0:
            return
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(remaining - candidates[i], i, path)
            path.pop()
    result = []
    candidates.sort()
    backtrack(target, 0, [])
    return result

print(combination_sum([2, 3, 6, 7], 7))
```

---

## Problem 7: Combination Sum II (Each Used Once)
**Difficulty: Medium | Marks: 30**

```python
def combination_sum2(candidates, target):
    candidates.sort()
    def backtrack(remaining, start, path):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            backtrack(remaining - candidates[i], i + 1, path)
            path.pop()
    result = []
    backtrack(target, 0, [])
    return result

print(combination_sum2([10, 1, 2, 7, 6, 1, 5], 8))
```

---

## Problem 8: Palindrome Partitioning
**Difficulty: Medium | Marks: 30**

```python
def partition(s):
    def is_palindrome(sub):
        return sub == sub[::-1]
    def backtrack(start, path):
        if start == len(s):
            result.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            if is_palindrome(s[start:end]):
                path.append(s[start:end])
                backtrack(end, path)
                path.pop()
    result = []
    backtrack(0, [])
    return result

print(partition("aab"))
```

---

## Problem 9: Sudoku Solver
**Difficulty: Hard | Marks: 50**

```python
def solve_sudoku(board):
    def is_valid(r, c, ch):
        for i in range(9):
            if board[r][i] == ch:
                return False
            if board[i][c] == ch:
                return False
            box_r, box_c = 3 * (r // 3) + i // 3, 3 * (c // 3) + i % 3
            if board[box_r][box_c] == ch:
                return False
        return True

    def backtrack():
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    for ch in '123456789':
                        if is_valid(r, c, ch):
                            board[r][c] = ch
                            if backtrack():
                                return True
                            board[r][c] = '.'
                    return False
        return True

    backtrack()
    return board

board = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"]
]
solve_sudoku(board)
for row in board:
    print(' '.join(row))
```

---

## Problem 10: Word Search
**Difficulty: Medium | Marks: 30**

```python
def exist(board, word):
    m, n = len(board), len(board[0])
    def dfs(i, j, k):
        if k == len(word):
            return True
        if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[k]:
            return False
        temp, board[i][j] = board[i][j], '#'
        found = dfs(i + 1, j, k + 1) or dfs(i - 1, j, k + 1) or \
                dfs(i, j + 1, k + 1) or dfs(i, j - 1, k + 1)
        board[i][j] = temp
        return found
    for i in range(m):
        for j in range(n):
            if board[i][j] == word[0] and dfs(i, j, 0):
                return True
    return False

board = [
    ['A', 'B', 'C', 'E'],
    ['S', 'F', 'C', 'S'],
    ['A', 'D', 'E', 'E']
]
print(exist(board, "ABCCED"))
print(exist(board, "SEE"))
print(exist(board, "ABCB"))
```

---

## Problem 11: Letter Combinations of a Phone Number
**Difficulty: Medium | Marks: 30**

```python
def letter_combinations(digits):
    if not digits:
        return []
    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    def backtrack(idx, path):
        if idx == len(digits):
            result.append(''.join(path))
            return
        for ch in phone[digits[idx]]:
            path.append(ch)
            backtrack(idx + 1, path)
            path.pop()
    result = []
    backtrack(0, [])
    return result

print(letter_combinations("23"))
```

---

## Problem 12: Generate Parentheses
**Difficulty: Medium | Marks: 30**

```python
def generate_parentheses(n):
    def backtrack(open_count, close_count, path):
        if open_count == close_count == n:
            result.append(path)
            return
        if open_count < n:
            backtrack(open_count + 1, close_count, path + '(')
        if close_count < open_count:
            backtrack(open_count, close_count + 1, path + ')')
    result = []
    backtrack(0, 0, '')
    return result

print(generate_parentheses(3))
```

---

## Problem 13: Restore IP Addresses
**Difficulty: Medium | Marks: 30**

```python
def restore_ip_addresses(s):
    def backtrack(start, path):
        if len(path) == 4 and start == len(s):
            result.append('.'.join(path))
            return
        if len(path) == 4 or start == len(s):
            return
        for end in range(start, min(start + 3, len(s))):
            segment = s[start:end + 1]
            if (segment[0] == '0' and len(segment) > 1) or int(segment) > 255:
                continue
            backtrack(end + 1, path + [segment])
    result = []
    backtrack(0, [])
    return result

print(restore_ip_addresses("25525511135"))
```

---

## Problem 14: Matchsticks to Square
**Difficulty: Medium | Marks: 30**

```python
def makesquare(matchsticks):
    total = sum(matchsticks)
    if total % 4 != 0:
        return False
    target = total // 4
    matchsticks.sort(reverse=True)
    sides = [0] * 4
    def backtrack(idx):
        if idx == len(matchsticks):
            return all(s == target for s in sides)
        for i in range(4):
            if sides[i] + matchsticks[idx] <= target:
                sides[i] += matchsticks[idx]
                if backtrack(idx + 1):
                    return True
                sides[i] -= matchsticks[idx]
            if sides[i] == 0:
                break
        return False
    return backtrack(0)

print(makesquare([1, 1, 2, 2, 2]))
print(makesquare([3, 3, 3, 3, 4]))
```

---

## Problem 15: Tug of War (Split Array into Two Equal Sum Subsets)
**Difficulty: Hard | Marks: 50**

```python
def tug_of_war(arr):
    n = len(arr)
    total = sum(arr)
    target = total // 2
    result_diff = float('inf')
    result_set = []

    def backtrack(idx, count, curr_sum, selected):
        nonlocal result_diff, result_set
        if count == n // 2:
            diff = abs(total - 2 * curr_sum)
            if diff < result_diff:
                result_diff = diff
                result_set = selected[:]
            return
        if idx >= n:
            return
        # include
        selected.append(arr[idx])
        backtrack(idx + 1, count + 1, curr_sum + arr[idx], selected)
        selected.pop()
        # exclude
        backtrack(idx + 1, count, curr_sum, selected)

    backtrack(0, 0, 0, [])
    return result_set, [x for x in arr if x not in result_set]

arr = [23, 45, -34, 12, 0, 98, -99, 4, 189, -1, 4]
print(tug_of_war(arr))
```
