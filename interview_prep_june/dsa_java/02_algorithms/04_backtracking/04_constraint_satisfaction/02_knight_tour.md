# Knight's Tour

**Problem**: Given an N×N chessboard with a knight placed at a starting position, find a sequence of moves such that the knight visits every square exactly once.

**Types**:
- **Open tour**: Knight visits every square exactly once, ends anywhere
- **Closed tour**: Knight visits every square exactly once AND returns to the start in one more move

---

## Naive Backtracking Solution

```java
public class KnightTour {
    private static final int[] MOVE_X = {2, 1, -1, -2, -2, -1, 1, 2};
    private static final int[] MOVE_Y = {1, 2, 2, 1, -1, -2, -2, -1};
    private int N;
    private int[][] board;

    public KnightTour(int N) {
        this.N = N;
        this.board = new int[N][N];
        // Initialize with -1 (unvisited)
        for (int[] row : board) Arrays.fill(row, -1);
    }

    public boolean solve(int startX, int startY) {
        board[startX][startY] = 0; // First move
        if (backtrack(startX, startY, 1)) {
            printBoard();
            return true;
        }
        System.out.println("No solution exists");
        return false;
    }

    private boolean backtrack(int x, int y, int moveCount) {
        if (moveCount == N * N) return true; // visited all squares

        for (int i = 0; i < 8; i++) {
            int nextX = x + MOVE_X[i];
            int nextY = y + MOVE_Y[i];

            if (isValid(nextX, nextY)) {
                board[nextX][nextY] = moveCount;

                if (backtrack(nextX, nextY, moveCount + 1)) {
                    return true;
                }

                board[nextX][nextY] = -1; // backtrack
            }
        }

        return false;
    }

    private boolean isValid(int x, int y) {
        return x >= 0 && x < N && y >= 0 && y < N && board[x][y] == -1;
    }

    private void printBoard() {
        for (int[] row : board) {
            for (int cell : row) {
                System.out.printf("%2d ", cell);
            }
            System.out.println();
        }
    }
}
```

### Complexity

- **Time**: O(8^(N²)) in worst case — 8 choices per move, N² moves
- **Space**: O(N²) for board + O(N²) recursion stack

For N=8, naive backtracking would take years. But with heuristics, it solves in milliseconds.

---

## Warnsdorff's Rule (Heuristic)

**Rule**: At each step, choose the next move that has the **minimum number of onward moves**. This simple heuristic dramatically improves performance.

```java
private boolean backtrack(int x, int y, int moveCount) {
    if (moveCount == N * N) return true;

    // Get all valid next moves sorted by Warnsdorff's heuristic
    List<int[]> nextMoves = getSortedMoves(x, y);

    for (int[] move : nextMoves) {
        int nextX = move[0], nextY = move[1];

        board[nextX][nextY] = moveCount;
        if (backtrack(nextX, nextY, moveCount + 1)) return true;
        board[nextX][nextY] = -1;
    }

    return false;
}

private List<int[]> getSortedMoves(int x, int y) {
    List<int[]> moves = new ArrayList<>();

    for (int i = 0; i < 8; i++) {
        int nextX = x + MOVE_X[i];
        int nextY = y + MOVE_Y[i];
        if (isValid(nextX, nextY)) {
            int onwardMoves = countOnwardMoves(nextX, nextY);
            moves.add(new int[]{nextX, nextY, onwardMoves});
        }
    }

    // Sort by Warnsdorff's heuristic: fewest onward moves first
    moves.sort(Comparator.comparingInt(a -> a[2]));

    return moves;
}

private int countOnwardMoves(int x, int y) {
    int count = 0;
    for (int i = 0; i < 8; i++) {
        int nextX = x + MOVE_X[i];
        int nextY = y + MOVE_Y[i];
        if (isValid(nextX, nextY)) count++;
    }
    return count;
}
```

### Why It Works

Warnsdorff's rule prioritizes squares that are "most constrained" — squares with fewer escape routes. This is the same MRV (Minimum Remaining Values) heuristic used in Sudoku solving.

**Intuition**: If we delay visiting a square with few exit options, we might get stuck later when that square is the only unvisited neighbor but we can't reach it. By visiting constrained squares early, we avoid getting trapped.

### Performance Comparison

| N | Naive Backtracking | Warnsdorff's Rule |
|---|---|---|
| 5 | < 1s | Instant |
| 6 | ~5s | Instant |
| 7 | Hours | < 1s |
| 8 | Years | < 1s |
| 30 | Impossible | < 5s |

---

## Complete Warnsdorff Implementation (Non-Recursive)

Warnsdorff's rule is often implemented iteratively since it rarely needs backtracking:

```java
public class WarnsdorffKnightTour {
    private static final int[] MOVE_X = {2, 1, -1, -2, -2, -1, 1, 2};
    private static final int[] MOVE_Y = {1, 2, 2, 1, -1, -2, -2, -1};
    private int N;

    public WarnsdorffKnightTour(int N) {
        this.N = N;
    }

    public boolean solve(int startX, int startY) {
        int[][] board = new int[N][N];
        for (int[] row : board) Arrays.fill(row, -1);

        int x = startX, y = startY;
        board[x][y] = 0;

        for (int move = 1; move < N * N; move++) {
            List<int[]> moves = getSortedMoves(board, x, y);
            if (moves.isEmpty()) return false;

            int[] best = moves.get(0);
            x = best[0];
            y = best[1];
            board[x][y] = move;
        }

        printBoard(board);
        return true;
    }

    private List<int[]> getSortedMoves(int[][] board, int x, int y) {
        List<int[]> moves = new ArrayList<>();
        for (int i = 0; i < 8; i++) {
            int nx = x + MOVE_X[i];
            int ny = y + MOVE_Y[i];
            if (nx >= 0 && nx < N && ny >= 0 && ny < N && board[nx][ny] == -1) {
                int degree = countNeighbors(board, nx, ny);
                moves.add(new int[]{nx, ny, degree});
            }
        }
        moves.sort(Comparator.comparingInt(a -> a[2]));
        return moves;
    }

    private int countNeighbors(int[][] board, int x, int y) {
        int count = 0;
        for (int i = 0; i < 8; i++) {
            int nx = x + MOVE_X[i];
            int ny = y + MOVE_Y[i];
            if (nx >= 0 && nx < N && ny >= 0 && ny < N && board[nx][ny] == -1) {
                count++;
            }
        }
        return count;
    }
}
```

**Note**: The iterative version works for most boards (N ≥ 5) without backtracking. For cases where Warnsdorff's rule leads to a dead end, we fall back to backtracking with Warnsdorff's heuristic.

---

## Tie-Breaking Rules

When multiple moves have the same minimum number of onward moves, we need a tie-breaker. Common approaches:

### 1. Pohl's Tie-Breaker (Distance from Center)

Prefer squares closer to the center (more options on average):

```java
// In the comparator:
moves.sort((a, b) -> {
    if (a[2] != b[2]) return a[2] - b[2];
    // Tie-breaker: prefer squares closer to center
    double distA = Math.pow(a[0] - N/2.0, 2) + Math.pow(a[1] - N/2.0, 2);
    double distB = Math.pow(b[0] - N/2.0, 2) + Math.pow(b[1] - N/2.0, 2);
    return Double.compare(distA, distB);
});
```

### 2. Squirrel's Tie-Breaker (Random)

Random choice among ties:

```java
// Collect all moves with min degree, pick random
int minDegree = moves.get(0)[2];
List<int[]> bestMoves = new ArrayList<>();
for (int[] move : moves) {
    if (move[2] == minDegree) bestMoves.add(move);
}
int[] chosen = bestMoves.get(new Random().nextInt(bestMoves.size()));
```

---

## Closed Tour (Hamiltonian Cycle)

A closed tour returns to the starting square. Find it by:

```java
public boolean solveClosed(int startX, int startY) {
    board[startX][startY] = 0;
    if (backtrackClosed(startX, startY, 1, startX, startY)) {
        printBoard();
        return true;
    }
    return false;
}

private boolean backtrackClosed(int x, int y, int moveCount,
                                 int startX, int startY) {
    if (moveCount == N * N) {
        // Check if we can return to start
        for (int i = 0; i < 8; i++) {
            if (x + MOVE_X[i] == startX && y + MOVE_Y[i] == startY) {
                return true;
            }
        }
        return false;
    }

    List<int[]> moves = getSortedMoves(x, y);
    for (int[] move : moves) {
        int nx = move[0], ny = move[1];
        board[nx][ny] = moveCount;
        if (backtrackClosed(nx, ny, moveCount + 1, startX, startY)) {
            return true;
        }
        board[nx][ny] = -1;
    }
    return false;
}
```

---

## Key Insights

1. **Warnsdorff's rule** makes Knight's Tour practical — it's the textbook example of a heuristic that transforms an intractable problem into a trivial one
2. **The degree heuristic** (choosing the most constrained square first) is the same MRV principle used in Sudoku
3. **Tie-breaking matters** — Pohl's distance-to-center rule is effective
4. **For N < 5**, Knight's Tour has no solution on some board sizes
5. **Closed tours** exist for even N ≥ 6 (with some exceptions)

## Interview Points

If asked about Knight's Tour in an interview:
1. Start with naive backtracking
2. Mention that it's O(8^(N²)) and impractical for N=8
3. Introduce Warnsdorff's rule as the optimization
4. Explain WHY it works (visit constrained squares first)
5. Note that it usually finds a solution without backtracking
