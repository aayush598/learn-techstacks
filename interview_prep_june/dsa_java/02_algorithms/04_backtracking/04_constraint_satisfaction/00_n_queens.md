# N-Queens Problem

**Problem**: Place N queens on an N×N chessboard so that no two queens attack each other. Queens attack along rows, columns, and diagonals.

**Example**: `n = 4`
```
Output: 2 solutions
[".Q..",  // Solution 1
 "...Q",
 "Q...",
 "..Q."]

["..Q.",  // Solution 2
 "Q...",
 "...Q",
 ".Q.."]
```

---

## Approach: Column Placement Array

Instead of a 2D board, we use `int[] queens = new int[N]` where `queens[row] = col` indicates the column position of the queen in that row. This automatically ensures no two queens share a row.

### Validation

A queen at `(r1, c1)` attacks a queen at `(r2, c2)` if:
1. **Same column**: `c1 == c2`
2. **Same diagonal**: `|r1 - r2| == |c1 - c2|` (45° or 135° diagonal)

Since we place one queen per row (our `queens` array), we don't need to check rows.

```java
private boolean canPlace(int[] queens, int row, int col) {
    for (int prevRow = 0; prevRow < row; prevRow++) {
        int prevCol = queens[prevRow];
        // Same column or same diagonal?
        if (prevCol == col || Math.abs(prevRow - row) == Math.abs(prevCol - col)) {
            return false;
        }
    }
    return true;
}
```

### Full Backtracking Solution

```java
public List<List<String>> solveNQueens(int n) {
    List<List<String>> result = new ArrayList<>();
    int[] queens = new int[n]; // queens[row] = column
    backtrack(queens, 0, result);
    return result;
}

private void backtrack(int[] queens, int row, List<List<String>> result) {
    if (row == queens.length) {
        result.add(buildBoard(queens));
        return;
    }

    for (int col = 0; col < queens.length; col++) {
        if (canPlace(queens, row, col)) {
            queens[row] = col; // Place queen
            backtrack(queens, row + 1, result); // Explore next row
            // No need to "unplace" — we overwrite queens[row] next time
        }
    }
}

private List<String> buildBoard(int[] queens) {
    List<String> board = new ArrayList<>();
    for (int row = 0; row < queens.length; row++) {
        char[] chars = new char[queens.length];
        Arrays.fill(chars, '.');
        chars[queens[row]] = 'Q';
        board.add(new String(chars));
    }
    return board;
}

private boolean canPlace(int[] queens, int row, int col) {
    for (int prevRow = 0; prevRow < row; prevRow++) {
        int prevCol = queens[prevRow];
        if (prevCol == col || Math.abs(prevRow - row) == Math.abs(prevCol - col)) {
            return false;
        }
    }
    return true;
}
```

### Decision Tree for 4-Queens

```
Row 0:  . . . .          Q . . .    . Q . .    . . Q .    . . . Q
        |                                     |
Row 1:  . . . .   ...    . . Q .   ...       Q . . .  (invalid)
        |                (valid)
Row 2:  ...             Q . . . (invalid back) ...
        |
Row 3:  ...

Solution found! → [1, 3, 0, 2] → board:
  . Q . .
  . . . Q
  Q . . .
  . . Q .
```

---

## Optimized Validation with Sets

Instead of scanning all previous rows, we can use sets to track attacked columns and diagonals:

```java
public List<List<String>> solveNQueens(int n) {
    List<List<String>> result = new ArrayList<>();
    int[] queens = new int[n];

    // Sets to track attacked positions
    Set<Integer> cols = new HashSet<>();
    Set<Integer> diag1 = new HashSet<>(); // row - col (constant along NW-SE diag)
    Set<Integer> diag2 = new HashSet<>(); // row + col (constant along NE-SW diag)

    backtrack(queens, 0, cols, diag1, diag2, result);
    return result;
}

private void backtrack(int[] queens, int row,
                       Set<Integer> cols, Set<Integer> diag1, Set<Integer> diag2,
                       List<List<String>> result) {
    int n = queens.length;
    if (row == n) {
        result.add(buildBoard(queens));
        return;
    }

    for (int col = 0; col < n; col++) {
        int d1 = row - col;  // NW-SE diagonal
        int d2 = row + col;  // NE-SW diagonal

        if (cols.contains(col) || diag1.contains(d1) || diag2.contains(d2)) {
            continue;
        }

        // Place queen
        queens[row] = col;
        cols.add(col);
        diag1.add(d1);
        diag2.add(d2);

        backtrack(queens, row + 1, cols, diag1, diag2, result);

        // Remove queen
        cols.remove(col);
        diag1.remove(d1);
        diag2.remove(d2);
        // queens[row] will be overwritten
    }
}
```

### Why the Diagonal Formulas Work

```
NW-SE diagonal (top-left to bottom-right):  row - col is constant
  [0,0] → 0-0 = 0
  [1,1] → 1-1 = 0
  [2,2] → 2-2 = 0

NE-SW diagonal (top-right to bottom-left):  row + col is constant
  [0,3] → 0+3 = 3
  [1,2] → 1+2 = 3
  [2,1] → 2+1 = 3
```

For an 8×8 board:
- `row - col` ranges from -7 to 7 (15 values, can offset by n-1 for array indexing)
- `row + col` ranges from 0 to 14 (15 values)

---

## Count Solutions vs Print Solutions

### Count Only (N-Queens II)

```java
public int totalNQueens(int n) {
    return backtrack(n, 0, new boolean[n],
                     new boolean[2 * n], new boolean[2 * n]);
}

private int backtrack(int n, int row,
                      boolean[] cols, boolean[] diag1, boolean[] diag2) {
    if (row == n) return 1;

    int count = 0;
    for (int col = 0; col < n; col++) {
        int d1 = row - col + n - 1; // offset to make non-negative
        int d2 = row + col;

        if (cols[col] || diag1[d1] || diag2[d2]) continue;

        cols[col] = diag1[d1] = diag2[d2] = true;
        count += backtrack(n, row + 1, cols, diag1, diag2);
        cols[col] = diag1[d1] = diag2[d2] = false;
    }

    return count;
}
```

**Using boolean arrays** (more efficient than HashSet for small n):

| n | Solutions | Call Count |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 0 | 3 |
| 3 | 0 | 6 |
| 4 | 2 | 17 |
| 5 | 10 | 54 |
| 6 | 4 | 153 |
| 7 | 40 | 551 |
| 8 | 92 | 2,057 |
| 9 | 352 | 8,391 |
| 10 | 724 | 35,579 |

### Count With Symmetry Optimization

```java
public int totalNQueens(int n) {
    if (n == 1) return 1;
    int[] count = new int[1];
    boolean[] cols = new boolean[n];
    boolean[] diag1 = new boolean[2 * n];
    boolean[] diag2 = new boolean[2 * n];

    // Only place first queen in left half (exploit symmetry)
    for (int col = 0; col < n / 2; col++) {
        place(0, col, n, cols, diag1, diag2);
        backtrack(n, 1, cols, diag1, diag2, count);
        remove(0, col, n, cols, diag1, diag2);
    }
    count[0] *= 2; // symmetric solutions

    // If n is odd, handle center column separately
    if (n % 2 == 1) {
        place(0, n / 2, n, cols, diag1, diag2);
        backtrack(n, 1, cols, diag1, diag2, count);
        remove(0, n / 2, n, cols, diag1, diag2);
    }

    return count[0];
}
```

---

## Bitmask Solution (Most Efficient)

For n ≤ 32, we can use bitmasks for O(1) state tracking:

```java
public List<List<String>> solveNQueens(int n) {
    List<List<String>> result = new ArrayList<>();
    int[] queens = new int[n];
    backtrack(n, 0, queens, 0, 0, 0, result);
    return result;
}

private void backtrack(int n, int row, int[] queens,
                       int cols, int diag1, int diag2,
                       List<List<String>> result) {
    if (row == n) {
        result.add(buildBoard(queens));
        return;
    }

    // Available positions = ~(cols | diag1 | diag2) & ((1<<n)-1)
    int available = (~(cols | diag1 | diag2)) & ((1 << n) - 1);

    while (available != 0) {
        // Get least significant set bit
        int pos = available & -available;
        int col = Integer.bitCount(pos - 1); // column index

        queens[row] = col;
        backtrack(n, row + 1, queens,
                  cols | pos,
                  (diag1 | pos) << 1,  // shift for next row
                  (diag2 | pos) >> 1,  // shift for next row
                  result);

        // Remove LSB
        available &= available - 1;
    }
}
```

**Key insight for bitmask**: When moving to the next row:
- Column attacks: `cols | pos` (same, just mark column as used)
- NW-SE diagonal attacks: `(diag1 | pos) << 1` (shifts right one position)
- NE-SW diagonal attacks: `(diag2 | pos) >> 1` (shifts left one position)

---

## Complexity

- **Time**: O(n!) worst-case. Actually better due to pruning.
  - Tighter bound: O(n! / c^n) where c ≈ 2.54 for large n
- **Space**: O(n) for recursion + queens array

### Known Values

| n | Solutions |
|---|---|
| 1 | 1 |
| 4 | 2 |
| 8 | 92 |
| 10 | 724 |
| 12 | 14,200 |
| 14 | 365,596 |
| 16 | 14,772,512 |

---

## Key Takeaways

1. **1D array `queens[row] = col`** elegantly represents the board
2. **Column + diagonal tracking** is O(1) validation with sets/arrays/bitmasks
3. **Symmetry optimization** roughly halves the search space
4. **For counting**: use backtracking that returns int, not collecting results
5. **For n ≤ 32**: bitmask approach is fastest
6. **The backtracking structure**: try each column at each row, validate, recurse
7. **Validation simplifies because** one queen per row is guaranteed by the array structure
