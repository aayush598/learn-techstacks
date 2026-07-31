# 10. Recursion & Backtracking Cheatsheet

One-page dense reference for recursion fundamentals, backtracking permutations/combinations/subsets, grid/constraint puzzles (N-Queens, Sudoku, Word Search), and memoization. All code verified on Python 3.

## Recursion Fundamentals

### Base Case + Recursion Skeleton

Every recursive function needs: (1) a base case that returns without recursing, (2) a recursive step that moves toward the base case.

```python
def solve(n):
    if n <= 1:            # base case
        return 1
    return n * solve(n - 1)  # recursive step toward base
```

| Property | Rule |
|---|---|
| Base case | Must be reachable from every call; handles smallest input directly |
| Recursive case | Make progress (shrink input), combine sub-results |
| Stack depth | Python default recursion limit ~1000 (`sys.setrecursionlimit(10**6)` for trees/grids) |
| Tail recursion | Python does **NOT** optimize tail calls (no TCO) — a deep tail-recursive function will still blow the stack; convert to a loop when the recursive call is the last operation |

```python
# tail-recursive style (still O(n) stack in Python!)
def sum_to_n(n, acc=0):
    if n == 0:
        return acc
    return sum_to_n(n - 1, acc + n)   # does NOT become a loop

# Python-idiomatic: iterative
def sum_to_n(n):
    return sum(range(n + 1))
```

## The Backtracking Framework

### Master Template — choose → recurse → unchoose

```python
def backtrack(choices, path, *extra):   # *extra = any extra state (start, remaining, ...)
    if is_solution(path):        # base case: record result
        results.append(path[:])  # COPY, never append path directly
        return
    for choice in choices:       # branching
        if not is_valid(choice, path):   # pruning (optional)
            continue
        make_choice(path, choice)        # choose
        backtrack(choices, path, *extra) # recurse (pass updated state)
        undo_choice(path, choice)        # unchoose (the backtrack)
```

- **Results live in `path`**, appended as a **copy** `path[:]` (or `"".join(path)`) at the base case.
- **The prune step** (`if not is_valid(...): continue`) is where you cut branches — permute-unique dedup, combination-sum `> remaining`, N-Queens diagonal checks.
- The `unchoose` step is mandatory so sibling branches see the same state (the classic "backtracking bug" is forgetting `pop()`).

## Permutations

### Without Duplicates (visited array)

```python
def permute(nums):
    n = len(nums)
    used = [False] * n
    res = []

    def backtrack(path):
        if len(path) == n:
            res.append(path[:])
            return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return res

assert permute([1, 2, 3]) == [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

**Complexity:** O(n · n!) time, O(n) recursion depth (+ O(n!) output). Number of results = n!.

### With Duplicates (sort + skip equal-and-unused)

```python
def permute_unique(nums):
    nums.sort()
    n = len(nums)
    used = [False] * n
    res = []

    def backtrack(path):
        if len(path) == n:
            res.append(path[:])
            return
        for i in range(n):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue          # skip duplicate at same depth
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return res

assert sorted(permute_unique([1, 1, 2])) == [[1,1,2],[1,2,1],[2,1,1]]
```

**Key idea:** sort first; when `nums[i] == nums[i-1]` and `nums[i-1]` is **not** used in the current path, this branch is identical to one already explored at this depth — skip it.

**Complexity:** O(n · n!) worst case, O(n) depth.

## Combinations

### All C(n, k) — start index prevents reorder duplicates

```python
def combine(n, k):
    res = []

    def backtrack(start, path):
        if len(path) == k:
            res.append(path[:])
            return
        for i in range(start, n + 1):   # only choices >= start
            path.append(i)
            backtrack(i + 1, path)      # next choice strictly greater
            path.pop()

    backtrack(1, [])
    return res

assert len(combine(4, 2)) == 6   # C(4,2)
```

**Complexity:** O(C(n,k) · k), O(k) depth. Using `start` (never revisit earlier indices) enforces the combination invariant and prunes duplicates automatically.

## Subsets (Powerset)

### Without Duplicates — append every path

```python
def subsets(nums):
    res = []

    def backtrack(start, path):
        res.append(path[:])             # every node is a valid subset
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return res

assert len(subsets([1, 2, 3])) == 8
```

### With Duplicates

```python
def subsets_with_dup(nums):
    nums.sort()
    res = []

    def backtrack(start, path):
        res.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue            # skip duplicates within same level
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return res

assert len(subsets_with_dup([1, 2, 2])) == 6
```

**Complexity:** O(2^n) subsets, O(n) depth. Rule of thumb: `i > start` skip (not `i > 0`) is the subset/combination-sum-II dedup; `not used[i-1]` is the permutation dedup.

## Combination Sum

### I — unlimited use of each number (`backtrack(i, ...)`)

```python
def combination_sum(candidates, target):
    res = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                continue          # prune: can't fit
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i (not i+1): reuse allowed
            path.pop()

    backtrack(0, [], target)
    return res

assert len(combination_sum([2, 3, 6, 7], 7)) == 2   # [[2,2,3],[7]]
```

### II — each number once, no duplicate combos (sort + skip, `backtrack(i+1, ...)`)

```python
def combination_sum2(candidates, target):
    candidates.sort()
    res = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break               # sorted => prune whole tail
            if i > start and candidates[i] == candidates[i - 1]:
                continue            # dedup identical combos
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])  # i+1: no reuse
            path.pop()

    backtrack(0, [], target)
    return res

assert len(combination_sum2([10, 1, 2, 7, 6, 1, 5], 8)) == 4
```

**Complexity (both):** O(N^(T/M)) worst case, O(T/M) depth (T = target, M = min candidate). Distinguishing detail: **reuse allowed → recurse with same index `i`; reuse forbidden → `i + 1`**.

## N-Queens

```python
def solve_n_queens(n):
    cols = [False] * n
    diag1 = [False] * (2 * n - 1)   # r + c
    diag2 = [False] * (2 * n - 1)   # r - c + (n - 1)
    board = [["."] * n for _ in range(n)]
    res = []

    def backtrack(r):
        if r == n:
            res.append(["".join(row) for row in board])
            return
        for c in range(n):
            if cols[c] or diag1[r + c] or diag2[r - c + n - 1]:
                continue
            cols[c] = diag1[r + c] = diag2[r - c + n - 1] = True
            board[r][c] = "Q"
            backtrack(r + 1)
            board[r][c] = "."
            cols[c] = diag1[r + c] = diag2[r - c + n - 1] = False

    backtrack(0)
    return res

assert len(solve_n_queens(8)) == 92
```

**Diagonal trick:** one queen per row, so state is only the columns + two diagonal axes:
- `r + c` is constant on the `/` (NW-SE) diagonal — index in `[0, 2n-2]`.
- `r - c` is constant on the `\` (NE-SW) diagonal — offset by `+ n - 1` to avoid negatives.

**Complexity:** O(n!) worst case, O(n²) to build each board output, O(n) depth.

## Sudoku Solver Skeleton

```python
def solve_sudoku(board):
    def is_valid(r, c, ch):
        for i in range(9):
            if board[r][i] == ch or board[i][c] == ch:
                return False
            if board[r // 3 * 3 + i // 3][c // 3 * 3 + i % 3] == ch:
                return False
        return True

    def backtrack():
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    for ch in "123456789":
                        if is_valid(r, c, ch):
                            board[r][c] = ch
                            if backtrack():
                                return True
                            board[r][c] = "."
                    return False        # no digit fits => invalid board
        return True                     # full board found

    backtrack()
    return board
```

- **Find empty cell → try each digit → recurse → unchoose on failure.** Return early with `True` once solved (this is a "find one solution" search, not "collect all").
- **3×3 box indexing:** `r // 3 * 3 + i // 3` and `c // 3 * 3 + i % 3` iterate the 9 cells of the box containing `(r, c)`.
- **Complexity:** O(9^(empty cells)) worst case; in practice pruned heavily by `is_valid`.

## Generate Parentheses

```python
def generate_parenthesis(n):
    res = []

    def backtrack(open_count, close_count, path):
        if len(path) == 2 * n:
            res.append("".join(path))
            return
        if open_count < n:                       # may still open
            path.append("(")
            backtrack(open_count + 1, close_count, path)
            path.pop()
        if close_count < open_count:             # must not close more than opened
            path.append(")")
            backtrack(open_count, close_count + 1, path)
            path.pop()

    backtrack(0, 0, [])
    return res

assert len(generate_parenthesis(3)) == 5   # Catalan(3)
```

**Invariant:** only ever add `)` when `close < open` — this guarantees validity at every prefix, so no validation pass needed. Results count = Catalan number. **Complexity:** O(4^n / √n), O(n) depth.

## Word Search on Grid

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    on_path = set()                    # cells used by current path

    def dfs(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if board[r][c] != word[i] or (r, c) in on_path:
            return False               # mismatch or revisit
        on_path.add((r, c))            # choose
        for dr, dc in dirs:
            if dfs(r + dr, c + dc, i + 1):
                return True
        on_path.remove((r, c))         # unchoose
        return False

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False

assert exist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED")
assert not exist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCB")
```

- The `on_path` set (or `board[r][c] = "#"` sentinel) prevents reusing the same cell — mandatory on grids.
- Early-exit `i == len(word)` before bounds check; bounds/mismatch checks reject invalid branches cheaply.
- **Complexity:** O(rows·cols·4^L) worst case, O(L) depth (L = len(word)).

## Memoization

### functools.lru_cache (top-down, cleanest)

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(500))   # instant; recursion memoized by arguments
```

Rules: arguments must be **hashable** (int, str, tuples OK; lists/None not directly — convert lists to tuples or use frozenset for sets). Cache key = the tuple of arguments; identical calls are O(1) lookups after first computation.

### Manual dict memo (works for any state, incl. objects)

```python
memo = {}

def fib(n):
    if n < 2:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]
```

Use the manual dict when the state is composite (e.g. `(i, mask)`), when `lru_cache` is awkward, or when you must clear the cache between test cases (`memo.clear()`).

### Generic memoized backtracking pattern

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def dfs(state):                # state = tuple of "remaining" params
    if base_case(state):
        return ...
    best = -inf
    for move in moves(state):
        best = max(best, dfs(next_state(state, move)))
    return best
```

Memoization turns exponential brute force into polynomial when subproblems overlap — the single highest-leverage trick for DP-on-recursion interview problems.

## Complexity Reference Table

| Problem | Time | Space (excluding output) |
|---|---|---|
| Permutations | O(n · n!) | O(n) |
| Permutations with dups | O(n · n!) | O(n) |
| Combinations C(n,k) | O(C(n,k) · k) | O(k) |
| Subsets | O(n · 2^n) | O(n) |
| Combination Sum | O(N^(T/M)) | O(T/M) |
| N-Queens | O(n!) | O(n) |
| Generate Parentheses | O(4^n / √n) | O(n) |
| Word Search | O(m·n·4^L) | O(L) |
