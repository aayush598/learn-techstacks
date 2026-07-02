# 05 — Backtracking Introduction

Backtracking is recursion with **the power to undo**. It's the art of exploring a decision space, and when you hit a dead end, backing up to try a different choice. Think of it as "reckless exploration with a safety rope."

---

## 1. What is Backtracking?

**Definition:** Backtracking incrementally builds candidates to a solution and abandons them ("backtracks") as soon as it determines the candidate cannot lead to a valid solution.

### The Core Idea

```
Start with empty solution
For each possible choice:
    Make the choice
    Recurse (try to solve from here)
    Unmake the choice (backtrack)
If no choice works, return to previous level
```

### Decision Space as a Tree

```
                    [] (start)
          /          |          \
        [1]        [2]         [3]
       /   \       /   \       /   \
    [1,2] [1,3] [2,1] [2,3] [3,1] [3,2]
     /      |     |      |    |      \
  [1,2,3] dead  dead  [2,3,1] dead  dead
```

Leaf nodes are solutions (or dead ends). The path from root to leaf is the sequence of choices.

---

## 2. General Backtracking Template

```java
void backtrack(candidate, result) {
    if (isValidSolution(candidate)) {
        result.add(new copy of candidate);  // found one solution
        return;                              // or continue searching
    }

    for (nextChoice : choices) {
        if (isValid(nextChoice)) {           // pruning (optional)
            makeChoice(candidate, nextChoice);
            backtrack(candidate, result);
            undoChoice(candidate, nextChoice);  // BACKTRACK
        }
    }
}
```

### Key Components

1. **Base case:** When we've found a valid solution, add to result
2. **Loop over choices:** Try each possible option
3. **Prune:** Skip invalid choices early (optional but crucial for performance)
4. **Make choice:** Modify state
5. **Recurse:** Explore further
6. **Undo choice:** Restore state (the backtrack step)

---

## 3. N-Queens — Complete Solution

Place N queens on an N×N board so no two attack each other.

```java
public class NQueens {
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> result = new ArrayList<>();
        char[][] board = new char[n][n];
        for (char[] row : board) Arrays.fill(row, '.');
        backtrack(board, 0, result);
        return result;
    }

    void backtrack(char[][] board, int row, List<List<String>> result) {
        if (row == board.length) {
            result.add(construct(board));
            return;
        }

        for (int col = 0; col < board.length; col++) {
            if (isSafe(board, row, col)) {
                board[row][col] = 'Q';          // place queen
                backtrack(board, row + 1, result);  // next row
                board[row][col] = '.';          // remove queen (backtrack)
            }
        }
    }

    boolean isSafe(char[][] board, int row, int col) {
        // Check column (above)
        for (int i = 0; i < row; i++) {
            if (board[i][col] == 'Q') return false;
        }
        // Upper-left diagonal
        for (int i = row, j = col; i >= 0 && j >= 0; i--, j--) {
            if (board[i][j] == 'Q') return false;
        }
        // Upper-right diagonal
        for (int i = row, j = col; i >= 0 && j < board.length; i--, j++) {
            if (board[i][j] == 'Q') return false;
        }
        return true;
    }

    List<String> construct(char[][] board) {
        List<String> solution = new ArrayList<>();
        for (char[] row : board) solution.add(new String(row));
        return solution;
    }
}

// N=4: 2 solutions
// N=8: 92 solutions
// N=10: 724 solutions
```

**Optimization:** Use `boolean[] cols, diag1, diag2` for O(1) safety check instead of O(n):

```java
void backtrack(int row, int n, boolean[] cols, boolean[] diag1, boolean[] diag2,
               char[][] board, List<List<String>> result) {
    if (row == n) {
        result.add(construct(board));
        return;
    }
    for (int col = 0; col < n; col++) {
        int d1 = row - col + n - 1;  // primary diagonal index
        int d2 = row + col;           // secondary diagonal index
        if (!cols[col] && !diag1[d1] && !diag2[d2]) {
            board[row][col] = 'Q';
            cols[col] = diag1[d1] = diag2[d2] = true;
            backtrack(row + 1, n, cols, diag1, diag2, board, result);
            cols[col] = diag1[d1] = diag2[d2] = false;
            board[row][col] = '.';
        }
    }
}
```

---

## 4. Sudoku Solver — Complete Solution

```java
public class SudokuSolver {
    public void solveSudoku(char[][] board) {
        solve(board);
    }

    boolean solve(char[][] board) {
        for (int row = 0; row < 9; row++) {
            for (int col = 0; col < 9; col++) {
                if (board[row][col] == '.') {  // empty cell
                    for (char num = '1'; num <= '9'; num++) {
                        if (isValid(board, row, col, num)) {
                            board[row][col] = num;    // place
                            if (solve(board)) return true;  // recurse
                            board[row][col] = '.';    // backtrack
                        }
                    }
                    return false;  // no number works
                }
            }
        }
        return true;  // all cells filled
    }

    boolean isValid(char[][] board, int row, int col, char num) {
        // Check row
        for (int x = 0; x < 9; x++) {
            if (board[row][x] == num) return false;
        }
        // Check column
        for (int x = 0; x < 9; x++) {
            if (board[x][col] == num) return false;
        }
        // Check 3x3 box
        int boxRow = row - row % 3;
        int boxCol = col - col % 3;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[boxRow + i][boxCol + j] == num) return false;
            }
        }
        return true;
    }
}

// Input: partially filled 9x9 board with '.' for empty cells
// Output: filled board in-place
```

```java
// Optimization: find empty cells upfront
boolean solveFast(char[][] board, List<int[]> emptyCells, int index) {
    if (index == emptyCells.size()) return true;

    int row = emptyCells.get(index)[0];
    int col = emptyCells.get(index)[1];

    for (char num = '1'; num <= '9'; num++) {
        if (isValid(board, row, col, num)) {
            board[row][col] = num;
            if (solveFast(board, emptyCells, index + 1)) return true;
            board[row][col] = '.';
        }
    }
    return false;
}
```

---

## 5. Maze All Paths (with Backtracking)

Find ALL paths from (0,0) to (n-1,n-1) in a maze, moving in all 4 directions, avoiding obstacles and revisiting cells.

```java
void findAllPaths(int[][] maze, int r, int c, int n,
                  boolean[][] visited, String path, List<String> result) {

    if (r < 0 || c < 0 || r >= n || c >= n ||
        maze[r][c] == 0 || visited[r][c]) {
        return;
    }

    if (r == n - 1 && c == n - 1) {
        result.add(path);
        return;
    }

    visited[r][c] = true;

    // Try all 4 directions
    findAllPaths(maze, r + 1, c, n, visited, path + "D", result);
    findAllPaths(maze, r - 1, c, n, visited, path + "U", result);
    findAllPaths(maze, r, c + 1, n, visited, path + "R", result);
    findAllPaths(maze, r, c - 1, n, visited, path + "L", result);

    visited[r][c] = false;  // backtrack
}

// Example maze
int[][] maze = {
    {1, 1, 1},
    {1, 1, 1},
    {1, 1, 1}
};
int n = 3;
List<String> paths = new ArrayList<>();
findAllPaths(maze, 0, 0, n, new boolean[n][n], "", paths);
System.out.println(paths.size());  // number of paths from (0,0) to (2,2)
```

---

## 6. Knight's Tour Introduction

Place a knight on an empty chessboard and visit every square exactly once.

```java
boolean knightsTour(int[][] board, int row, int col, int moveNumber, int n) {
    // All squares visited
    if (moveNumber == n * n) return true;

    // Knight's possible moves
    int[] rowMoves = {-2, -1, 1, 2, 2, 1, -1, -2};
    int[] colMoves = {1, 2, 2, 1, -1, -2, -2, -1};

    for (int i = 0; i < 8; i++) {
        int nextRow = row + rowMoves[i];
        int nextCol = col + colMoves[i];

        if (isValidMove(board, nextRow, nextCol, n)) {
            board[nextRow][nextCol] = moveNumber;       // place knight
            if (knightsTour(board, nextRow, nextCol, moveNumber + 1, n)) {
                return true;
            }
            board[nextRow][nextCol] = -1;               // backtrack
        }
    }
    return false;
}

boolean isValidMove(int[][] board, int r, int c, int n) {
    return r >= 0 && c >= 0 && r < n && c < n && board[r][c] == -1;
}

// Start
int n = 5;
int[][] board = new int[n][n];
for (int[] row : board) Arrays.fill(row, -1);
board[0][0] = 0;  // start position

knightsTour(board, 0, 0, 1, n);
// board now contains move numbers for a valid tour (if one exists)
```

**Complexity:** O(8^(n²)) worst case, but with Warnsdorff's heuristic (choose move with fewest onward options), it becomes much faster.

---

## 7. Common Backtracking Problems

### Generate All Subsets (LeetCode 78)

```java
List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

void backtrack(int[] nums, int start, List<Integer> current, List<List<Integer>> result) {
    result.add(new ArrayList<>(current));  // add at every step (not just leaf)

    for (int i = start; i < nums.length; i++) {
        current.add(nums[i]);
        backtrack(nums, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
// [1,2,3] → [[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]
```

### Generate All Permutations (LeetCode 46)

```java
List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, new boolean[nums.length], new ArrayList<>(), result);
    return result;
}

void backtrack(int[] nums, boolean[] used, List<Integer> current, List<List<Integer>> result) {
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
// [1,2,3] → [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

### Combination Sum (LeetCode 39)

```java
List<List<Integer>> combinationSum(int[] candidates, int target) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(candidates, target, 0, new ArrayList<>(), result);
    return result;
}

void backtrack(int[] candidates, int remaining, int start,
               List<Integer> current, List<List<Integer>> result) {
    if (remaining == 0) {
        result.add(new ArrayList<>(current));
        return;
    }
    if (remaining < 0) return;

    for (int i = start; i < candidates.length; i++) {
        current.add(candidates[i]);
        backtrack(candidates, remaining - candidates[i], i, current, result);  // same i = reuse allowed
        current.remove(current.size() - 1);
    }
}
// [2,3,6,7], target=7 → [[2,2,3],[7]]
```

---

## 8. Backtracking vs Simple Recursion

| Simple Recursion | Backtracking |
|-----------------|--------------|
| Makes one decision | Explores multiple choices |
| No "undo" needed | Must undo each choice |
| Usually returns a single value | Usually builds a list of solutions |
| Examples: factorial, fibonacci | Examples: N-Queens, Sudoku, maze |

All backtracking is recursion, but not all recursion is backtracking.

---

## 9. Pruning — The Art of Cutting Branches

Pruning eliminates dead branches early. It's what makes backtracking practical.

```java
// WITHOUT pruning — explores everything, then checks validity
void nQueensNoPrune(char[][] board, int row, List<List<String>> result) {
    if (row == board.length) {
        if (isValidBoard(board)) result.add(construct(board));
        return;
    }
    for (int col = 0; col < board.length; col++) {
        board[row][col] = 'Q';
        nQueensNoPrune(board, row + 1, result);  // places Q even in invalid spots
        board[row][col] = '.';
    }
    // Explores n^n possibilities! For n=8: 16M vs 92 valid solutions
}

// WITH pruning — only places in safe spots
void nQueensWithPrune(char[][] board, int row, List<List<String>> result) {
    if (row == board.length) {
        result.add(construct(board));
        return;
    }
    for (int col = 0; col < board.length; col++) {
        if (isSafe(board, row, col)) {  // PRUNE: only try safe positions
            board[row][col] = 'Q';
            nQueensWithPrune(board, row + 1, result);
            board[row][col] = '.';
        }
    }
    // Explores only valid positions → far fewer branches
}
```

**Pruning is the difference between O(n!) and O(n^n).** Always prune as early as possible.

---

## Backtracking Reference

```
TEMPLATE:
void backtrack(choices, path, result) {
    if (validSolution(path)) {
        result.add(copy(path));
        return;
    }
    for (choice : choices) {
        if (isValid(choice)) {
            make(choice);           // modify state
            backtrack(choices, path, result);
            undo(choice);           // restore state
        }
    }
}

KEY PROBLEMS:
Subsets        → for loop with start index (avoid duplicates)
Permutations   → for loop with used[] array (track usage)
Combinations   → for loop with start index (order doesn't matter)
N-Queens       → row by row, check columns/diagonals
Sudoku         → cell by cell, check row/col/box
Maze paths     → 4 directions, visited[][] matrix
Knight's tour  → 8 knight moves, visited[][] matrix
```

