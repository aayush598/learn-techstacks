# Backtracking Practice Problems — 15 Problems

## Table of Contents
- [Easy (3)](#easy)
- [Medium (6)](#medium)
- [Hard (6)](#hard)

---

# Easy

## 1. Subsets (LeetCode 78)

**Problem**: Given a set of distinct integers, return all possible subsets (the power set).

**Approach**: At each index, decide whether to include or exclude the element. Use backtracking with a start index to avoid duplicates.

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

# Test
print(subsets([1, 2, 3]))
# [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
```

**Complexity**: O(2^N * N) time (2^N subsets, each copied in O(N)). O(N) space for recursion.

---

## 2. Permutations (LeetCode 46)

**Problem**: Given a collection of distinct integers, return all possible permutations.

**Approach**: Use a `used` array to track which elements are in the current path. When path length equals array length, record the permutation.

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

# Test
print(permute([1, 2, 3]))
# [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

**Complexity**: O(N * N!) time, O(N) space.

---

## 3. Letter Combinations of a Phone Number (LeetCode 17)

**Problem**: Given a string of digits (2-9), return all possible letter combinations (phone keypad mapping).

**Approach**: Recurse over each digit. For each digit, try all mapped letters. Build the combination string.

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

# Test
print(letter_combinations("23"))
# ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
```

**Complexity**: O(4^N * N) time where N = len(digits). O(N) space for recursion.

---

# Medium

## 4. Combination Sum (LeetCode 39)

**Problem**: Given an array of candidates and a target, find all unique combinations where candidates can be reused.

**Approach**: Sort candidates. At each step, try each candidate from `start` index (allows reuse). Prune if candidate exceeds remaining target.

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
            backtrack(i, path, remaining - candidates[i])  # i, not i+1
            path.pop()

    backtrack(0, [], target)
    return result

# Test
print(combination_sum([2, 3, 6, 7], 7))
# [[2,2,3], [7]]
```

**Complexity**: O(N^(T/M)) time where T = target, M = min candidate. O(T/M) space.

---

## 5. Subsets II (LeetCode 90)

**Problem**: Given a collection of integers that may contain duplicates, return all unique subsets.

**Approach**: Sort the array. At each level, skip `nums[i]` if it equals `nums[i-1]` and we haven't used `nums[i-1]` at this recursion level.

```python
def subsets_with_dup(nums):
    result = []
    nums.sort()

    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result

# Test
print(subsets_with_dup([1, 2, 2]))
# [[], [1], [1,2], [1,2,2], [2], [2,2]]
```

**Complexity**: O(2^N * N) time, O(N) space.

---

## 6. Permutations II (LeetCode 47)

**Problem**: Given a collection that might contain duplicates, return all unique permutations.

**Approach**: Sort the array. Use `used` array. Skip `nums[i]` if `nums[i] == nums[i-1]` and `used[i-1] is False` (same value not used at this level).

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
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result

# Test
print(permute_unique([1, 1, 2]))
# [[1,1,2], [1,2,1], [2,1,1]]
```

**Complexity**: O(N * N!) time, O(N) space.

---

## 7. Palindrome Partitioning (LeetCode 131)

**Problem**: Given a string s, partition s such that every substring is a palindrome. Return all valid partitionings.

**Approach**: At each position, try all possible ending positions. If the substring is a palindrome, include it and recurse on the remainder.

```python
def partition_palindrome(s):
    result = []

    def backtrack(start, path):
        if start == len(s):
            result.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            sub = s[start:end]
            if sub != sub[::-1]:
                continue
            path.append(sub)
            backtrack(end, path)
            path.pop()

    backtrack(0, [])
    return result

# Test
print(partition_palindrome("aab"))
# [["a", "a", "b"], ["aa", "b"]]
```

**Complexity**: O(N * 2^N) time (2^N partitions, O(N) to check each). O(N) space.

---

## 8. Word Search (LeetCode 79)

**Problem**: Given a 2D board and a word, find if the word exists in the grid. Move up/down/left/right. Each cell used once.

**Approach**: For each cell matching the first letter, DFS. Mark visited cells by modifying the board. Restore on backtrack.

```python
def exist(board, word):
    if not board:
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
        board[r][c] = '#'

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if backtrack(r + dr, c + dc, idx + 1):
                return True

        board[r][c] = temp
        return False

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0]:
                if backtrack(r, c, 0):
                    return True
    return False

# Test
board = [
    ['A','B','C','E'],
    ['S','F','C','S'],
    ['A','D','E','E']
]
print(exist(board, "ABCCED"))  # True
print(exist(board, "ABCB"))   # False
```

**Complexity**: O(M * N * 4^L) time where L = len(word). O(L) space for recursion.

---

## 9. N-Queens (LeetCode 51)

**Problem**: Place N queens on an N x N chessboard so no two queens attack each other. Return all distinct solutions.

**Approach**: Place row by row. Use sets for columns and diagonals for O(1) safety checks.

```python
def solve_n_queens(n):
    result = []
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col
    board = [-1] * n

    def backtrack(row):
        if row == n:
            # Build board string
            solution = []
            for c in range(n):
                row_str = '.' * c + 'Q' + '.' * (n - c - 1)
                solution.append(row_str)
            result.append(solution)
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

# Test
solutions = solve_n_queens(4)
for sol in solutions:
    for row in sol:
        print(row)
    print()
# .Q..
# ...Q
# Q...
# ..Q.
#
# ..Q.
# Q...
# ...Q
# .Q..
```

**Complexity**: O(N!) time, O(N) space.

---

# Hard

## 10. Sudoku Solver (LeetCode 37)

**Problem**: Fill a 9x9 grid so every row, column, and 3x3 box contains digits 1-9.

**Approach**: Find the next empty cell. Try digits 1-9. Check validity against row, column, and box. Backtrack on failure.

```python
def solve_sudoku(board):
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

**Complexity**: O(9^E) where E = empty cells (~20-30 typically). Space: O(E).

---

## 11. Expression Add Operators (LeetCode 282)

**Problem**: Given a string num and an integer target, add '+' or '-' between digits to form expressions that evaluate to target.

**Approach**: At each position, try forming numbers of length 1, 2, etc. Track the current value and the previous operand (for multiplication).

```python
def add_operators(num, target):
    result = []

    def backtrack(idx, prev, curr, expr):
        if idx == len(num):
            if curr == target:
                result.append(expr)
            return

        for i in range(idx, len(num)):
            # Skip numbers with leading zeros
            if i > idx and num[idx] == '0':
                break

            operand = int(num[idx:i + 1])
            next_idx = i + 1

            if idx == 0:
                # First number: no operator before it
                backtrack(next_idx, operand, operand, str(operand))
            else:
                # Addition
                backtrack(next_idx, operand, curr + operand, expr + '+' + str(operand))
                # Subtraction
                backtrack(next_idx, -operand, curr - operand, expr + '-' + str(operand))
                # Multiplication
                backtrack(next_idx, prev * operand, curr - prev + prev * operand,
                         expr + '*' + str(operand))

    backtrack(0, 0, 0, '')
    return result

# Test
print(add_operators("123", 6))
# ["1+2+3", "1*2*3"]
print(add_operators("232", 8))
# ["2*3+2", "2+3*2"]
```

**Complexity**: O(4^N) time (4 choices at each position: *, +, -, or extend number). O(N) space.

---

## 12. Alien Dictionary (LeetCode 269)

**Problem**: Given a sorted list of words in an alien language, find the character order (permutation of characters).

**Approach**: Build a directed graph by comparing adjacent words. The first differing character gives an ordering. Topological sort the graph.

```python
from collections import defaultdict, deque

def alien_order(words):
    # Build graph: edge from u to v means u comes before v
    adj = defaultdict(set)
    in_degree = {c: 0 for word in words for c in word}

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        # Invalid case: longer word comes before shorter word
        if len(w1) > len(w2) and w1[:len(w2)] == w2:
            return ""
        for j in range(min(len(w1), len(w2))):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break

    # Topological sort (Kahn's algorithm)
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    order = []

    while queue:
        c = queue.popleft()
        order.append(c)
        for neighbor in adj[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check if all characters are in the order (cycle detection)
    if len(order) != len(in_degree):
        return ""

    return ''.join(order)

# Test
print(alien_order(["wrt", "wrf", "er", "ett", "rftt"]))
# "wertf"
print(alien_order(["z", "x"]))
# "zx"
```

**Complexity**: O(C) time where C = total characters in all words. O(1) space (26 letters).

---

## 13. Palindrome Permutation II (LeetCode 267)

**Problem**: Given a string s, return all palindromic permutations of s.

**Approach**: First check if a palindrome is possible (at most one odd-frequency character). Generate permutations of half the characters, then mirror.

```python
def generate_palindrome(s):
    from collections import Counter

    char_count = Counter(s)
    odd_chars = [c for c, cnt in char_count.items() if cnt % 2 == 1]

    if len(odd_chars) > 1:
        return []  # impossible

    # Build half string (each char used half its frequency)
    half = []
    for c, cnt in char_count.items():
        half.extend([c] * (cnt // 2))

    result = []
    used = [False] * len(half)

    def backtrack(path):
        if len(path) == len(half):
            palindrome = ''.join(path)
            middle = odd_chars[0] if odd_chars else ''
            result.append(palindrome + middle + palindrome[::-1])
            return

        for i in range(len(half)):
            if used[i]:
                continue
            if i > 0 and half[i] == half[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(half[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result

# Test
print(generate_palindrome("aabb"))
# ["abba", "baab"]
print(generate_palindrome("abc"))
# [] (can't form palindrome)
```

**Complexity**: O(N/2)! * N/2 time. O(N) space.

---

## 14. Crossword Solver

**Problem**: Given a crossword grid with '-' for empty cells and '#' for blocked cells, and a list of words, place all words in the grid (horizontal or vertical).

**Approach**: Find all valid slots (sequences of '-' cells). For each slot, try placing words that fit. Check no conflicts.

```python
def solve_crossword(grid, words):
    rows, cols = len(grid), len(grid[0])
    word_set = set(words)

    def get_slots():
        """Find all horizontal and vertical slots."""
        slots = []
        # Horizontal
        for r in range(rows):
            c = 0
            while c < cols:
                if grid[r][c] == '-':
                    start = c
                    while c < cols and grid[r][c] == '-':
                        c += 1
                    length = c - start
                    if length in [len(w) for w in words]:
                        slots.append(('h', r, start, length))
                else:
                    c += 1
        # Vertical
        for c in range(cols):
            r = 0
            while r < rows:
                if grid[r][c] == '-':
                    start = r
                    while r < rows and grid[r][c] == '-':
                        r += 1
                    length = r - start
                    if length in [len(w) for w in words]:
                        slots.append(('v', start, c, length))
                else:
                    r += 1
        return slots

    def can_place(word, slot):
        direction, r, c, length = slot
        if len(word) != length:
            return False
        for i in range(length):
            if direction == 'h':
                cell = grid[r][c + i]
            else:
                cell = grid[r + i][c]
            if cell != '-' and cell != word[i]:
                return False
        return True

    def place(word, slot):
        direction, r, c, length = slot
        placed = []
        for i in range(length):
            if direction == 'h':
                if grid[r][c + i] == '-':
                    grid[r][c + i] = word[i]
                    placed.append((r, c + i))
            else:
                if grid[r + i][c] == '-':
                    grid[r + i][c] = word[i]
                    placed.append((r + i, c))
        return placed

    def undo(placed):
        for r, c in placed:
            grid[r][c] = '-'

    def backtrack(word_idx, slots, used_words):
        if word_idx == len(words):
            return True

        for slot_idx, slot in enumerate(slots):
            word = words[word_idx]
            if not can_place(word, slot):
                continue
            placed = place(word, slot)
            if backtrack(word_idx + 1, slots, used_words):
                return True
            undo(placed)

        return False

    slots = get_slots()
    if backtrack(0, slots, set()):
        return grid
    return None


# Example
grid = [
    ['-', '-', '-', '#'],
    ['#', '-', '-', '-'],
    ['-', '-', '#', '-'],
    ['#', '-', '-', '-']
]
words = ["cat", "act", "hat"]
result = solve_crossword(grid, words)
if result:
    for row in result:
        print(row)
```

**Complexity**: O(W! * S * L) where W = words, S = slots, L = word length.

---

## 15. Factor Combinations (LintCode 90)

**Problem**: Given an integer n, return all possible combinations of its factors (excluding 1 and n itself, and n).

**Approach**: Starting from 2, try dividing n. For each factor found, recurse on the quotient with factors >= current factor (to avoid duplicates).

```python
def get_factors(n):
    result = []

    def backtrack(start, path, remaining):
        if path:  # non-empty factorization
            result.append(path + [remaining])

        for i in range(start, int(remaining**0.5) + 1):
            if remaining % i == 0:
                path.append(i)
                backtrack(i, path, remaining // i)
                path.pop()

    backtrack(2, [], n)
    return result

# Test
print(get_factors(32))
# [[2,16], [2,2,8], [2,2,2,4], [2,2,2,2,2], [2,4,4], [4,8]]
print(get_factors(12))
# [[2,6], [2,2,3], [3,4]]
print(get_factors(1))
# []
```

### Alternative: Include all factors (including repeated)

```python
def get_factors_all(n):
    result = []

    def backtrack(start, path, remaining):
        if path:
            result.append(path[:])

        for i in range(start, remaining + 1):
            if remaining % i == 0:
                path.append(i)
                backtrack(i, path, remaining // i)
                path.pop()

    backtrack(2, [], n)
    return result
```

**Complexity**: O(sqrt(N)^(log N)) time. O(log N) space for recursion depth.

---

# Complexity Summary

| # | Problem | Difficulty | Time | Space |
|---|---------|------------|------|-------|
| 1 | Subsets | Easy | O(2^N * N) | O(N) |
| 2 | Permutations | Easy | O(N * N!) | O(N) |
| 3 | Letter Combinations | Easy | O(4^N * N) | O(N) |
| 4 | Combination Sum | Medium | O(N^(T/M)) | O(T/M) |
| 5 | Subsets II | Medium | O(2^N * N) | O(N) |
| 6 | Permutations II | Medium | O(N * N!) | O(N) |
| 7 | Palindrome Partition | Medium | O(N * 2^N) | O(N) |
| 8 | Word Search | Medium | O(M*N*4^L) | O(L) |
| 9 | N-Queens | Medium | O(N!) | O(N) |
| 10 | Sudoku Solver | Hard | O(9^E) | O(E) |
| 11 | Expression Add Operators | Hard | O(4^N) | O(N) |
| 12 | Alien Dictionary | Hard | O(C) | O(1) |
| 13 | Palindrome Perm II | Hard | O((N/2)! * N) | O(N) |
| 14 | Crossword Solver | Hard | O(W! * S * L) | O(S) |
| 15 | Factor Combinations | Hard | O(sqrt(N)^(log N)) | O(log N) |

Where: N = input size, T = target, M = min candidate, L = word length, E = empty cells, C = total chars, W = words, S = slots.
