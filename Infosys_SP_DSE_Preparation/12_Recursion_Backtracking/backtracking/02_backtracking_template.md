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

### Visual: The 4-Step Backtracking Cycle

```
  ┌──────────────────────────────────────────────────────────────────┐
  │                  BACKTRACKING LIFECYCLE                          │
  │                                                                  │
  │  ┌─────────┐    ┌──────────┐    ┌───────────┐    ┌──────────┐  │
  │  │ 1. CHOOSE │──►│ 2. RECURSE│──►│ 3. UNDO   │──►│ 4. NEXT  │  │
  │  │           │    │ (explore) │    │ (backtrack)│    │ CHOICE   │  │
  │  │ path.append│   │ go deeper │    │ path.pop() │    │ continue │  │
  │  └─────────┘    └──────────┘    └───────────┘    └─────┬────┘  │
  │       ▲                                                  │       │
  │       └──────────────── loop back ───────────────────────┘       │
  └──────────────────────────────────────────────────────────────────┘

  EXAMPLE: Generating subsets of [1, 2, 3]

  path=[] ──choose(1)──► path=[1] ──choose(2)──► path=[1,2] ──choose(3)──► path=[1,2,3]
                          │                          │                          │
                     record []                  record [1]               record [1,2]
                     (at every node)            (at every node)          (at every node)
                          │                          │                          │
                     undo(1)─► path=[]        undo(2)─► path=[1]       undo(3)─► path=[1,2]
                       │                          │                          │
                    choose(2)──► path=[2]    choose(3)──► path=[1,3]   record [1,2,3]
                       │                          │
                  record [2]                record [1,3]
                       │                          │
                    undo(2)─► path=[]        undo(3)─► path=[1]
                       │                          │
                    choose(3)──► path=[3]    undo(1)─► path=[]
                       │                          │
                  record [2]                choose(2)──► path=[2]
                       │                          │
                    undo(3)─► path=[]        record [2]
                                                 │
                                              undo(2)─► path=[]
                                                 │
                                              choose(3)──► path=[3]
                                                 │
                                            record [2,3]
                                                 │
                                              undo(3)─► path=[2]
                                                 │
                                              undo(2)─► path=[]
                                                 │
                                              ... and so on
```

### Template Variants

```python
# Variant 1: Find ONE solution (return True to stop early)
def backtrack_one(path, choices):
    if is_solution(path):
        return True  # stop searching

    for choice in choices:
        path.append(choice)                    # 1. MAKE choice
        if backtrack_one(path, next_choices(choice)):
            return True                        # 2. PROPAGATE stop signal up
        path.pop()                             # 3. UNDO choice

    return False  # no solution found from this state


# Variant 2: Count solutions
def backtrack_count(path, choices):
    if is_solution(path):
        return 1  # found one solution

    count = 0
    for choice in choices:
        path.append(choice)                    # 1. MAKE choice
        count += backtrack_count(path, next_choices(choice))  # 2. ACCUMULATE
        path.pop()                             # 3. UNDO choice

    return count  # total solutions from this state


# Variant 3: Find BEST solution (optimization)
def backtrack_best(path, choices):
    if is_solution(path):
        return evaluate(path)  # return score

    best = float('-inf')
    for choice in choices:
        path.append(choice)                    # 1. MAKE choice
        best = max(best, backtrack_best(path, next_choices(choice)))  # 2. TRACK best
        path.pop()                             # 3. UNDO choice

    return best  # best score from this state
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

### Visual: What Pruning Does

```
  WITHOUT PRUNING: Full search tree for Combination Sum [2,3,6,7], target=7

                          []
                     /  / |  \
                   [2] [3] [6] [7] ✓ ← found!
                  / |\  |
             [2,2] [2,3]... [3,3]
             / |\
        [2,2,2] [2,2,3]...
         /|        \
  [2,2,2,2]...  [2,2,3,2]  ← exploring MANY dead ends

  ═══════════════════════════════════════════════════════════════════

  WITH PRUNING (sort + break on overflow):

                          []
                     /  / |  \         ← after [6] > 7, break
                   [2] [3] [6] [7] ✓    (no need to try larger)
                  / |\  
             [2,2] [2,3] ✓   ← found!
             / |
        [2,2,2] ...          ← [2,2,2]=6, can still try [2,2,3]=7 ✓
                               BUT [2,2,2,2]=8 > 7, PRUNE!

  PRUNED branches = eliminated without exploring → massive speedup!
```

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

## Common Backtracking Mistakes

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MISTAKE #1: Forgetting to copy path (path[:] not path)               │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │  result.append(path)      # ❌ All results point to the SAME list!      │
  │  result.append(path[:])   # ✓ Creates a COPY of current path            │
  │                                                                         │
  │  WHY: path is a reference. After backtracking, path changes.            │
  │  Without copy, all results become the final state of path.              │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MISTAKE #2: Wrong start index (causes duplicates or misses)           │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │  COMBINATIONS/SUBSETS: Use 'i' not 'i+1' for reuse, 'i+1' for no dup  │
  │  backtrack(i, ...)   ← reuse allowed (Combination Sum I)               │
  │  backtrack(i+1, ...) ← no reuse (Subsets, Combination Sum II)          │
  │                                                                         │
  │  PERMUTATIONS: Use used array, loop over ALL indices                    │
  │  for i in range(len(nums))  ← try every element                        │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MISTAKE #3: Not undoing state before returning                        │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │  path.append(choice)                                                    │
  │  backtrack(path)                                                        │
  │  path.pop()     # ← MUST pop! Otherwise path accumulates choices       │
  │                                                                         │
  │  same for: used[i] = True / used[i] = False                            │
  │  same for: board[r][c] = 'Q' / board[r][c] = '.'                       │
  │  same for: cols.add(col) / cols.remove(col)                             │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MISTAKE #4: Not sorting before duplicate pruning                      │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │  nums.sort()  # ← MUST sort first!                                     │
  │  # Then: if i > start and nums[i] == nums[i-1]: continue               │
  │  # Without sorting, duplicates aren't adjacent → can't detect them      │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## N-Queens

Place N queens on an N x N chessboard such that no two queens attack each other.

### Visual: N-Queens Problem for N=4

```
  QUEEN ATTACK PATTERNS:
  ═══════════════════════

  A queen attacks: entire row, column, and both diagonals

         Q ←──── ROW ────→
         |
       DIAG              DIAG
      (row-col)        (row+col)
         ↓                 ↓
       ╲ | ╱            ╲ | ╱
        ╲|╱              ╲|╱
  ───────Q───────    ───────Q───────
        ╱|╲              ╱|╲
       ╱ | ╲            ╱ | ╲

  ┌─────────────┐     ┌─────────────┐
  │ Q . . . . . │     │ . . . Q . . │
  │ . Q . . . . │     │ . . . . . . │
  │ . . Q . . . │     │ . . . . . . │
  │ . . . Q . . │     │ Q . . . . . │
  │ . . . . Q . │     │ . . . . . . │
  │ . . . . . Q │     │ . . . . . Q │
  └─────────────┘     └─────────────┘
   VALID (diagonal)     INVALID! Queen at (0,3)
                        attacks queen at (5,3) — same column!
```

### Step-by-Step: Solving N-Queens for N=4

```
  PLACEMENT ATTEMPTS (row by row):
  ════════════════════════════════════

  Row 0: Try col=0
  ┌───┬───┬───┬───┐
  │ Q │   │   │   │  ← place Q at (0,0)
  ├───┼───┼───┼───┤
  │   │   │   │   │
  ├───┼───┼───┼───┤
  │   │   │   │   │
  ├───┼───┼───┼───┤
  │   │   │   │   │
  └───┴───┴───┴───┘

  Row 1: Try col=0 ❌ (same col)
         Try col=1 ❌ (same diagonal)
         Try col=2 ✓ place at (1,2)
  ┌───┬───┬───┬───┐
  │ Q │   │   │   │
  ├───┼───┼───┼───┤
  │   │   │ Q │   │  ← place Q at (1,2)
  ├───┼───┼───┼───┤
  │   │   │   │   │
  ├───┼───┼───┼───┤
  │   │   │   │   │
  └───┴───┴───┴───┘

  Row 2: Try col=0 ❌ (same diag ↗)
         Try col=1 ❌ (same diag ↘ from Q(1,2))
         Try col=2 ❌ (same col)
         Try col=3 ❌ (same diag ↗ from Q(0,0))
         → DEAD END! No valid position for row 2
         → BACKTRACK: remove Q from (1,2)

  After exhaustive search from (0,0):
  ┌───┬───┬───┬───┐
  │   │ Q │   │   │  ← try (0,1) instead
  ├───┼───┼───┼───┤
  │   │   │   │ Q │  ← (1,3) works
  ├───┼───┼───┼───┤
  │ Q │   │   │   │  ← (2,0) works
  ├───┼───┼───┼───┤
  │   │   │ Q │   │  ← (3,2) works
  └───┴───┴───┴───┘
  ✓ SOLUTION FOUND!

  THE COMPLETE DECISION TREE (N=4):
  ════════════════════════════════════
                              []
                   ┌────┬────┼────┬────┐
                 col=0  col=1 col=2 col=3
                 [0]    [1]   [2]   [3]
                / | \    / \    X     / \
            col  col col col  DEAD  col col
            0,1  0,2 0,3    END   3,0 3,1
             X    |   X              |    X
                col=2             col=1   DEAD
                [1,2]            [3,1]   END
                 X                 |
               DEAD              col=0
               END              [3,1,0]
                                 |
                               col=2
                               [3,1,0,2]
                                ✓ VALID!

  Key insight: We place row by row (not all combinations).
  Each row gets exactly ONE queen.
```

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
    board = [-1] * n          # board[row] = col (which column queen is in)
    cols = set()              # columns that have queens
    diag1 = set()             # main diagonals: row - col (constant on each diag)
    diag2 = set()             # anti diagonals: row + col (constant on each diag)

    def backtrack(row):
        if row == n:
            result.append(board[:])    # found a valid placement
            return

        for col in range(n):
            # CHECK 3 CONSTRAINTS IN O(1):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue               # this column is attacked — skip

            # PLACE QUEEN
            cols.add(col)              # mark column as occupied
            diag1.add(row - col)       # mark main diagonal as occupied
            diag2.add(row + col)       # mark anti diagonal as occupied
            board[row] = col           # record which column queen is in

            backtrack(row + 1)         # move to next row

            # REMOVE QUEEN (backtrack)
            cols.remove(col)           # unmark column
            diag1.remove(row - col)    # unmark main diagonal
            diag2.remove(row + col)    # unmark anti diagonal
            board[row] = -1            # clear record

    backtrack(0)
    return result
```

**Complexity**: O(N!) time, O(N) space.

---

## Sudoku Solver

Fill a 9x9 grid so each row, column, and 3x3 box contains digits 1-9 exactly once.

### Visual: Sudoku Constraints

```
  ROW CONSTRAINT: Each row has 1-9
  ┌───────┬───────┬───────┐
  │ 5 3 _ │ _ 7 _ │ _ _ _ │  ← must contain all digits 1-9
  │ 6 _ _ │ 1 9 5 │ _ _ _ │
  │ _ 9 8 │ _ _ _ │ _ 6 _ │
  ├───────┼───────┼───────┤
  │ 8 _ _ │ _ 6 _ │ _ _ 3 │
  │ 4 _ _ │ 8 _ 3 │ _ _ 1 │
  │ 7 _ _ │ _ 2 _ │ _ _ 6 │
  ├───────┼───────┼───────┤
  │ _ 6 _ │ _ _ _ │ 2 8 _ │
  │ _ _ _ │ 4 1 9 │ _ _ 5 │
  │ _ _ _ │ _ 8 _ │ _ 7 9 │
  └───────┴───────┴───────┘
      ↑                 ↑
  COLUMN            3x3 BOX
  CONSTRAINT:       CONSTRAINT:
  Each column       Each 3x3 box
  has 1-9           has 1-9

  BOX NUMBERING:
  ┌─────┬─────┬─────┐
  │  0  │  1  │  2  │
  ├─────┼─────┼─────┤
  │  3  │  4  │  5  │
  ├─────┼─────┼─────┤
  │  6  │  7  │  8  │
  └─────┴─────┴─────┘
  Box index = 3 * (row // 3) + (col // 3)
```

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

### Visual: Word Search Example

```
  Finding "ABCCED" in the grid:
  ══════════════════════════════

  ┌───┬───┬───┬───┐
  │ A │ B │ C │ E │    Step 1: Find 'A' → (0,0)
  ├───┼───┼───┼───┤    Step 2: From A, look for 'B' → (0,1) ✓
  │ S │ F │ C │ S │    Step 3: From B, look for 'C' → (0,2) ✓
  ├───┼───┼───┼───┤    Step 4: From C, look for 'C' → (1,2) ✓
  │ A │ D │ E │ E │    Step 5: From C, look for 'E' → (2,2) ✓
  └───┴───┴───┴───┘    Step 6: From E, look for 'D' → (2,1) ✓ DONE!

  PATH MARKED:
  ┌───┬───┬───┬───┐
  │ A→│ B→│ C │ E │
  ├───┼───┼───┼───┤
  │ S │ F │ C↓│ S │
  ├───┼───┼───┼───┤
  │ A │ D←│ E←│ E │
  └───┴───┴───┴───┘

  "ABCB" would FAIL: after finding A→B→C, the next 'B' is at (0,1)
  which is already visited. No other 'B' is adjacent. → False
```

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

### Decision Flowchart: Which Backtracking Approach?

```
  ┌─────────────────────────────────────────────────────────────┐
  │           CHOOSING YOUR BACKTRACKING APPROACH               │
  └─────────────────────────────┬───────────────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │ Need to find ALL      │
                    │ solutions/possibilities?│
                    └───────────┬───────────┘
                         YES    │
                    ┌───────────▼───────────┐
                    │ Is order important?   │
                    └───────────┬───────────┘
                     YES        │         NO
                ┌───────────────▼──┐  ┌───▼──────────────┐
                │ PERMUTATION      │  │ SUBSET/COMBINATION│
                │ (used array)     │  │ (start index)     │
                │                  │  │                   │
                │ Try all elements │  │ Only look forward │
                │ at each position │  │ from start index  │
                └──────────────────┘  └───────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │ Need to find ONE      │
                    │ valid arrangement?    │
                    └───────────┬───────────┘
                         YES    │
                    ┌───────────▼───────────┐
                    │ Is it a GRID/BOARD?   │
                    └───────────┬───────────┘
                     YES        │         NO
                ┌───────────────▼──┐  ┌───▼──────────────┐
                │ N-QUEENS /        │  │ GRAPH COLORING /  │
                │ SUDOKU /          │  │ HAMILTONIAN PATH  │
                │ WORD SEARCH       │  │ (visited set)     │
                │ (position-based)  │  │                   │
                └──────────────────┘  └───────────────────┘

  KEY INSIGHT: The "start index" pattern naturally avoids duplicates
  by only considering elements after the current position.
  The "used array" pattern allows any order but needs explicit tracking.
```

### Template Quick-Reference Card

```
  ╔═══════════════════════════════════════════════════════════════════╗
  ║  BACKTRACKING TEMPLATE CHEAT SHEET                               ║
  ╠═══════════════════════════════════════════════════════════════════╣
  ║                                                                   ║
  ║  1. DEFINE state:    What represents current progress?            ║
  ║  2. DEFINE choices:  What options at each step?                   ║
  ║  3. DEFINE validity: What constraints must be satisfied?          ║
  ║  4. DEFINE base:     When is a solution complete?                 ║
  ║  5. ALWAYS undo:     Restore state before returning               ║
  ║                                                                   ║
  ║  COMMON BUGS:                                                     ║
  ║  • Forgot path[:] (copy) → all results share same list           ║
  ║  • Forgot path.pop() → path keeps growing                        ║
  ║  • Wrong start index → duplicate solutions                        ║
  ║  • Missing pruning → TLE on large inputs                          ║
  ║                                                                   ║
  ╚═══════════════════════════════════════════════════════════════════╝
```
