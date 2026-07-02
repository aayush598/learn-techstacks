# Backtracking Templates

## Table of Contents
1. Backtracking Fundamentals
2. Subset Template
3. Permutation Template
4. Combination Template
5. Constraint Satisfaction Template (N-Queens, Sudoku)
6. Pruning Strategies
7. Optimization vs Enumeration
8. Comparison Table

---

## 1. Backtracking Fundamentals

**Core idea:** Explore all possible solutions, backtrack when you reach a dead end.

**The three keys:**
1. **Choice** — At each step, what choices do we have?
2. **Constraint** — What constraints must the choice satisfy?
3. **Goal** — When do we have a complete solution?

**Standard template:**
```java
void backtrack(choices, path, result) {
    if (goal reached) {
        result.add(new path); // add copy
        return;
    }
    for (choice : choices) {
        if (choice is valid) {
            make choice // add to path
            backtrack(choices, path, result)
            undo choice // remove from path
        }
    }
}
```

**Time complexity:**
- Subsets: O(n × 2^n)
- Permutations: O(n × n!)
- Combinations: O(n × C(n,k))
- N-Queens: O(n!)

---

## 2. Subset Template

**Problem:** Find all subsets (power set) of a set of distinct integers.

**Key characteristic:** Each element can be either included or excluded. Order doesn't matter.

**Template:**
```java
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int start, List<Integer> current, List<List<Integer>> result) {
    result.add(new ArrayList<>(current)); // every prefix is a valid subset

    for (int i = start; i < nums.length; i++) {
        current.add(nums[i]);
        backtrack(nums, i + 1, current, result); // use i+1, not start+1
        current.remove(current.size() - 1);
    }
}
```

**Variations:**

**Subsets II (with duplicates):**
```java
public List<List<Integer>> subsetsWithDup(int[] nums) {
    Arrays.sort(nums); // must sort for duplicate handling
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int start, List<Integer> current, List<List<Integer>> result) {
    result.add(new ArrayList<>(current));
    for (int i = start; i < nums.length; i++) {
        if (i > start && nums[i] == nums[i - 1]) continue; // skip duplicates
        current.add(nums[i]);
        backtrack(nums, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```

---

## 3. Permutation Template

**Problem:** Find all permutations of distinct integers.

**Key characteristic:** Order matters. Each element must be used exactly once.

**Template (using used array):**
```java
public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    boolean[] used = new boolean[nums.length];
    backtrack(nums, used, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, boolean[] used, List<Integer> current, List<List<Integer>> result) {
    if (current.size() == nums.length) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        used[i] = true;
        current.add(nums[i]);
        backtrack(nums, used, current, result);
        current.remove(current.size() - 1);
        used[i] = false;
    }
}
```

**Template (using swapping — no extra space):**
```java
public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, result);
    return result;
}

private void backtrack(int[] nums, int start, List<List<Integer>> result) {
    if (start == nums.length) {
        List<Integer> current = new ArrayList<>();
        for (int num : nums) current.add(num);
        result.add(current);
        return;
    }
    for (int i = start; i < nums.length; i++) {
        swap(nums, start, i);
        backtrack(nums, start + 1, result);
        swap(nums, start, i); // backtrack
    }
}
```

**Permutations II (with duplicates):**
```java
public List<List<Integer>> permuteUnique(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    boolean[] used = new boolean[nums.length];
    backtrack(nums, used, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, boolean[] used, List<Integer> current, List<List<Integer>> result) {
    if (current.size() == nums.length) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        if (i > 0 && nums[i] == nums[i - 1] && !used[i - 1]) continue; // skip duplicates
        used[i] = true;
        current.add(nums[i]);
        backtrack(nums, used, current, result);
        current.remove(current.size() - 1);
        used[i] = false;
    }
}
```

---

## 4. Combination Template

**Problem:** Find all combinations of size k from [1..n].

**Key characteristic:** Subset of specific size. Order doesn't matter.

**Template:**
```java
public List<List<Integer>> combine(int n, int k) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(n, k, 1, new ArrayList<>(), result);
    return result;
}

private void backtrack(int n, int k, int start, List<Integer> current, List<List<Integer>> result) {
    if (current.size() == k) {
        result.add(new ArrayList<>(current));
        return;
    }
    // Optimization: remaining = k - current.size()
    for (int i = start; i <= n - (k - current.size()) + 1; i++) {
        current.add(i);
        backtrack(n, k, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```

**Combination Sum (unlimited use of elements):**
```java
public List<List<Integer>> combinationSum(int[] candidates, int target) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(candidates, target, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] candidates, int remain, int start, List<Integer> current, List<List<Integer>> result) {
    if (remain == 0) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int i = start; i < candidates.length; i++) {
        if (candidates[i] > remain) continue; // prune
        current.add(candidates[i]);
        backtrack(candidates, remain - candidates[i], i, current, result); // not i+1 (can reuse)
        current.remove(current.size() - 1);
    }
}
```

**Combination Sum II (each used once, no duplicates):**
```java
public List<List<Integer>> combinationSum2(int[] candidates, int target) {
    Arrays.sort(candidates);
    List<List<Integer>> result = new ArrayList<>();
    backtrack(candidates, target, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] candidates, int remain, int start, List<Integer> current, List<List<Integer>> result) {
    if (remain == 0) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int i = start; i < candidates.length; i++) {
        if (i > start && candidates[i] == candidates[i - 1]) continue; // skip duplicates
        if (candidates[i] > remain) break; // sorted, further will also exceed
        current.add(candidates[i]);
        backtrack(candidates, remain - candidates[i], i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```

---

## 5. Constraint Satisfaction Template

### N-Queens
**Goal:** Place n queens on n×n board such that no two queens threaten each other.

```java
public List<List<String>> solveNQueens(int n) {
    List<List<String>> result = new ArrayList<>();
    char[][] board = new char[n][n];
    for (char[] row : board) Arrays.fill(row, '.');
    backtrack(board, 0, result);
    return result;
}

private void backtrack(char[][] board, int row, List<List<String>> result) {
    if (row == board.length) {
        result.add(construct(board));
        return;
    }
    for (int col = 0; col < board.length; col++) {
        if (isValid(board, row, col)) {
            board[row][col] = 'Q';
            backtrack(board, row + 1, result);
            board[row][col] = '.';
        }
    }
}

private boolean isValid(char[][] board, int row, int col) {
    for (int i = 0; i < row; i++) {
        if (board[i][col] == 'Q') return false;
        int diff = row - i;
        if (col - diff >= 0 && board[i][col - diff] == 'Q') return false;
        if (col + diff < board.length && board[i][col + diff] == 'Q') return false;
    }
    return true;
}

private List<String> construct(char[][] board) {
    List<String> result = new ArrayList<>();
    for (char[] row : board) result.add(new String(row));
    return result;
}
```

**Optimized N-Queens (bitmask):**
```java
public List<List<String>> solveNQueens(int n) {
    List<List<String>> result = new ArrayList<>();
    char[][] board = new char[n][n];
    for (char[] row : board) Arrays.fill(row, '.');
    backtrack(board, 0, 0, 0, 0, result);
    return result;
}

private void backtrack(char[][] board, int row, int cols, int diag1, int diag2, List<List<String>> result) {
    int n = board.length;
    if (row == n) {
        result.add(construct(board));
        return;
    }
    for (int col = 0; col < n; col++) {
        int d1 = row - col + n - 1; // diagonal ↘
        int d2 = row + col;         // diagonal ↙
        if ((cols & (1 << col)) != 0 || (diag1 & (1 << d1)) != 0 || (diag2 & (1 << d2)) != 0) continue;
        board[row][col] = 'Q';
        backtrack(board, row + 1, cols | (1 << col), diag1 | (1 << d1), diag2 | (1 << d2), result);
        board[row][col] = '.';
    }
}
```

### Sudoku Solver
```java
public void solveSudoku(char[][] board) {
    solve(board);
}

private boolean solve(char[][] board) {
    for (int row = 0; row < 9; row++) {
        for (int col = 0; col < 9; col++) {
            if (board[row][col] == '.') {
                for (char c = '1'; c <= '9'; c++) {
                    if (isValid(board, row, col, c)) {
                        board[row][col] = c;
                        if (solve(board)) return true;
                        board[row][col] = '.';
                    }
                }
                return false; // no valid number
            }
        }
    }
    return true; // all filled
}

private boolean isValid(char[][] board, int row, int col, char c) {
    for (int i = 0; i < 9; i++) {
        if (board[row][i] == c) return false; // check row
        if (board[i][col] == c) return false; // check col
        int br = 3 * (row / 3) + i / 3;
        int bc = 3 * (col / 3) + i % 3;
        if (board[br][bc] == c) return false; // check 3×3 box
    }
    return true;
}
```

---

## 6. Pruning Strategies

### 1. Sorting + Early Break
```java
// For sorted candidates: if current exceeds remaining, break
Arrays.sort(candidates);
if (candidates[i] > target) break; // sorted ascending, further will also exceed
```

### 2. Duplicate Skip
```java
if (i > start && nums[i] == nums[i - 1]) continue;
```

### 3. Feasibility Pruning
```java
if (remaining elements can't reach solution) return;
// Example: for combination, if remaining numbers < needed count, prune
```

### 4. Branch and Bound (Optimization)
```java
if (current cost >= bestSoFar) return; // can't improve
```

### 5. Forward Checking (Constraint Satisfaction)
```java
// Before making a choice, check if it leaves any variable with no valid assignments
```

### 6. Constraint Propagation (Arc Consistency)
```java
// After a choice, propagate constraints to reduce domain of other variables
// Used in Sudoku, N-Queens, Cryptarithmetic
```

### Pruning Decision Table
| Technique | When to Use | Effect |
|-----------|------------|--------|
| Sort + skip duplicates | Input has duplicates | Avoids duplicate solutions |
| Sort + early break | Unsorted input with threshold | Prunes large subtrees |
| Upper/lower bound check | Optimization problems | Prunes non-optimal paths |
| Remaining capacity check | Knapsack-like | Prunes infeasible paths |
| Symmetry breaking | N-Queens, identical items | Eliminates symmetric solutions |
| Memoization (state caching) | Overlapping subproblems | Avoids recomputation |
| Ordering heuristics (MRV) | CSP (Sudoku) | Most constrained variable first |

---

## 7. Optimization vs Enumeration

| Aspect | Enumeration (Subsets, Perms) | Optimization (Knapsack, TSP) |
|--------|------------------------------|------------------------------|
| Goal | List ALL solutions | Find BEST solution |
| Terminal condition | All choices explored | Reach leaf OR prune |
| Result | List of solutions | Single best value |
| Pruning | Duplicate prevention only | Branch and bound |
| Best-so-far tracking | Not needed | track global optimum |

**Optimization template:**
```java
int bestSoFar = Integer.MAX_VALUE;

void backtrack(...) {
    if (current >= bestSoFar) return; // prune: can't improve
    if (complete solution) {
        bestSoFar = Math.min(bestSoFar, current);
        return;
    }
    for (choice : choices) {
        make choice
        backtrack(...)
        undo choice
    }
}
```

---

## 8. Comparison Table

| Problem | Use Case | Order Matters? | Duplicates? | Reuse Elements? | Parameter |
|---------|----------|---------------|-------------|-----------------|-----------|
| Subsets | All subsets | No | No (distinct input) | No | start index |
| Subsets II | All subsets with dup | No | Yes (skip in loop) | No | start index + sort |
| Permutations | All arrangements | Yes | No | Exactly once | used[] |
| Permutations II | Arrangements with dup | Yes | Yes (skip used+same) | Exactly once | used[] + sort |
| Combinations (nCk) | Subsets of size k | No | No | No | start index, size check |
| Combination Sum | Subsets summing to target | No | No | Yes (unbounded) | start index (not i+1) |
| Combination Sum II | Subsets sum to target, unique | No | Yes (skip in loop) | No | start index + sort |
| Palindrome Partitioning | Partition string | Yes (order fixed) | N/A | N/A | start index |
| Generate Parentheses | Valid parentheses | Yes | N/A | N/A | open/close count |
| Letter Combinations | Phone number mapping | Yes (order fixed) | N/A | N/A | index in digits |
| N-Queens | Place queens safely | Row by row | Symmetric | Each cell once | row index |
| Sudoku | Fill board | Cell by cell | N/A | Each cell once | cell row/col |

### Time Complexity Reference
| Algorithm | Time Complexity |
|-----------|----------------|
| Subsets (all) | O(n × 2^n) |
| Permutations | O(n × n!) |
| Combinations (nCk) | O(n × C(n,k)) |
| Combination Sum | O(2^(target/min)) |
| N-Queens | O(n!) |
| Sudoku Solver | O(9^(81)) with pruning |
| Generate Parentheses | O(4^n / n^(3/2)) |
