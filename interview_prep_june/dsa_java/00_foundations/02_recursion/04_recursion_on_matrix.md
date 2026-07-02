# 04 — Recursion on Matrix (Grid Problems)

Matrix recursion is all about **paths and exploration**. You're at a cell, and you need to decide where to go next. The recursive call stack naturally maps to the path you've taken.

---

## 1. Print All Paths in a Maze (Right/Down Only)

Starting from (0,0) to (rows-1, cols-1), moving only right or down.

```java
void printPaths(int r, int c, int rows, int cols, String path) {
    if (r == rows - 1 && c == cols - 1) {
        System.out.println(path);
        return;
    }
    if (r < rows - 1) {
        printPaths(r + 1, c, rows, cols, path + "D");  // Down
    }
    if (c < cols - 1) {
        printPaths(r, c + 1, rows, cols, path + "R");  // Right
    }
}

printPaths(0, 0, 3, 3, "");
// DDRR, DRDR, DRRD, RDDR, RDRD, RRDD — 6 paths for 3x3
// Number of paths = C((m-1)+(n-1), m-1) = C(4,2) = 6
```

### Count paths (return count instead of printing)

```java
int countPaths(int r, int c, int rows, int cols) {
    if (r == rows - 1 || c == cols - 1) {
        return 1;  // only one way from here (all rights or all downs)
    }
    int down = countPaths(r + 1, c, rows, cols);
    int right = countPaths(r, c + 1, rows, cols);
    return down + right;
}

System.out.println(countPaths(0, 0, 3, 3));  // 6
```

**Complexity:** O(2^(m+n)) naive (exponential). With DP: O(m*n).

---

## 2. Maze with Obstacles

Same maze, but some cells are blocked (marked as `true` for obstacle).

```java
void pathsWithObstacles(boolean[][] maze, int r, int c, String path, List<String> result) {
    int rows = maze.length;
    int cols = maze[0].length;

    if (r == rows - 1 && c == cols - 1) {
        result.add(path);
        return;
    }

    // If this cell is an obstacle, can't proceed
    if (maze[r][c]) return;  // true = obstacle

    if (r < rows - 1) {
        pathsWithObstacles(maze, r + 1, c, path + "D", result);
    }
    if (c < cols - 1) {
        pathsWithObstacles(maze, r, c + 1, path + "R", result);
    }
}

// Example maze (3x3 with obstacle at 1,1)
boolean[][] maze = {
    {false, false, false},
    {false, true,  false},
    {false, false, false}
};
// Paths: DRDR, DDRR — cannot go through (1,1)
```

---

## 3. Diagonal Moves Allowed

Now we can also move diagonally.

```java
void pathsWithDiagonal(int r, int c, int rows, int cols, String path, List<String> result) {
    if (r == rows - 1 && c == cols - 1) {
        result.add(path);
        return;
    }

    if (r < rows - 1) {
        pathsWithDiagonal(r + 1, c, rows, cols, path + "D", result);
    }
    if (c < cols - 1) {
        pathsWithDiagonal(r, c + 1, rows, cols, path + "R", result);
    }
    if (r < rows - 1 && c < cols - 1) {
        pathsWithDiagonal(r + 1, c + 1, rows, cols, path + "G", result);  // diagonal
    }
}

// 3x3 with diagonal:
// DDRR, DRDR, DRRD, RDRD, RRDD, RDDR,
// DGR, RDG, GDR, GRD, DGR... many more
```

---

## 4. Rat in a Maze

Standard problem: rat starts at (0,0), needs to reach (n-1,n-1). Can move in all 4 directions (up, down, left, right). Cannot visit cells with 0 or revisit cells.

```java
void ratInMaze(int[][] maze, int r, int c, int n,
               boolean[][] visited, String path, List<String> result) {

    // Out of bounds, blocked cell, or already visited
    if (r < 0 || c < 0 || r >= n || c >= n ||
        maze[r][c] == 0 || visited[r][c]) {
        return;
    }

    // Reached destination
    if (r == n - 1 && c == n - 1) {
        result.add(path);
        return;
    }

    // Mark current cell as visited
    visited[r][c] = true;

    // Try all 4 directions
    ratInMaze(maze, r + 1, c, n, visited, path + "D", result);  // Down
    ratInMaze(maze, r - 1, c, n, visited, path + "U", result);  // Up
    ratInMaze(maze, r, c + 1, n, visited, path + "R", result);  // Right
    ratInMaze(maze, r, c - 1, n, visited, path + "L", result);  // Left

    // Backtrack — unmark
    visited[r][c] = false;
}

// Example maze
int[][] maze = {
    {1, 0, 0, 0},
    {1, 1, 0, 1},
    {0, 1, 0, 0},
    {1, 1, 1, 1}
};

int n = maze.length;
List<String> paths = new ArrayList<>();
boolean[][] visited = new boolean[n][n];
ratInMaze(maze, 0, 0, n, visited, "", paths);
System.out.println(paths);
// [DRDDRR, DDRRDR] — possible paths
```

**Key difference from earlier:** Because we can move in all 4 directions (including up/left), we need `visited` to prevent infinite loops.

---

## 5. N-Queens Introduction

Place N queens on an NxN board such that no two queens attack each other.

```java
boolean isSafe(boolean[][] board, int row, int col) {
    int n = board.length;

    // Check vertical column (above current row)
    for (int i = 0; i < row; i++) {
        if (board[i][col]) return false;
    }

    // Check diagonal left (upper-left)
    for (int i = row, j = col; i >= 0 && j >= 0; i--, j--) {
        if (board[i][j]) return false;
    }

    // Check diagonal right (upper-right)
    for (int i = row, j = col; i >= 0 && j < n; i--, j++) {
        if (board[i][j]) return false;
    }

    return true;
}

void nQueens(boolean[][] board, int row, List<List<String>> result) {
    int n = board.length;
    if (row == n) {
        result.add(boardToString(board));
        return;
    }

    for (int col = 0; col < n; col++) {
        if (isSafe(board, row, col)) {
            board[row][col] = true;  // place queen
            nQueens(board, row + 1, result);
            board[row][col] = false; // remove queen (backtrack)
        }
    }
}

List<String> boardToString(boolean[][] board) {
    List<String> solution = new ArrayList<>();
    for (boolean[] row : board) {
        StringBuilder sb = new StringBuilder();
        for (boolean cell : row) {
            sb.append(cell ? "Q" : ".");
        }
        solution.add(sb.toString());
    }
    return solution;
}

// N-Queens for N=4
int N = 4;
boolean[][] board = new boolean[N][N];
List<List<String>> result = new ArrayList<>();
nQueens(board, 0, result);
System.out.println(result.size());  // 2 solutions for 4x4
// [[".Q..","...Q","Q...","..Q."],
//  ["..Q.","Q...","...Q",".Q.."]]
```

---

## 6. Flood Fill Algorithm

Change the color of a connected region in an image.

```java
void floodFill(int[][] image, int r, int c, int newColor, int originalColor) {
    // Out of bounds or not the original color or already changed
    if (r < 0 || c < 0 || r >= image.length || c >= image[0].length
        || image[r][c] != originalColor || image[r][c] == newColor) {
        return;
    }

    // Change this pixel
    image[r][c] = newColor;

    // Fill in all 4 directions
    floodFill(image, r + 1, c, newColor, originalColor);  // down
    floodFill(image, r - 1, c, newColor, originalColor);  // up
    floodFill(image, r, c + 1, newColor, originalColor);  // right
    floodFill(image, r, c - 1, newColor, originalColor);  // left
}

int[][] image = {
    {1, 1, 1, 0},
    {1, 1, 0, 0},
    {1, 0, 1, 1},
    {0, 0, 1, 1}
};

int originalColor = image[2][2];  // 1
floodFill(image, 2, 2, 2, originalColor);
// All connected '1's starting from (2,2) become '2'
```

**Complexity:** O(rows × cols) in worst case (fill entire image).

---

## 7. Word Search (LeetCode 79)

Find if a word exists in a grid by traversing adjacent cells.

```java
boolean wordSearch(char[][] board, String word, int r, int c, int index) {
    if (index == word.length()) return true;

    if (r < 0 || c < 0 || r >= board.length || c >= board[0].length
        || board[r][c] != word.charAt(index)) {
        return false;
    }

    // Mark as visited
    char temp = board[r][c];
    board[r][c] = '*';

    // Search in all 4 directions
    boolean found = wordSearch(board, word, r + 1, c, index + 1)
                 || wordSearch(board, word, r - 1, c, index + 1)
                 || wordSearch(board, word, r, c + 1, index + 1)
                 || wordSearch(board, word, r, c - 1, index + 1);

    // Backtrack
    board[r][c] = temp;

    return found;
}

boolean exist(char[][] board, String word) {
    for (int i = 0; i < board.length; i++) {
        for (int j = 0; j < board[0].length; j++) {
            if (wordSearch(board, word, i, j, 0)) return true;
        }
    }
    return false;
}

char[][] board = {
    {'A','B','C','E'},
    {'S','F','C','S'},
    {'A','D','E','E'}
};
System.out.println(exist(board, "ABCCED"));  // true
System.out.println(exist(board, "SEE"));     // true
System.out.println(exist(board, "ABCB"));    // false
```

---

## 8. Counting Paths — Complete Solutions

```java
public class MazeSolver {

    // Count paths right/down
    static int countRD(int r, int c, int m, int n) {
        if (r == m - 1 || c == n - 1) return 1;
        return countRD(r + 1, c, m, n) + countRD(r, c + 1, m, n);
    }

    // Count paths right/down/diagonal
    static int countRDD(int r, int c, int m, int n) {
        if (r == m - 1 || c == n - 1) return 1;
        int count = countRDD(r + 1, c, m, n) + countRDD(r, c + 1, m, n);
        if (r < m - 1 && c < n - 1)
            count += countRDD(r + 1, c + 1, m, n);
        return count;
    }

    // Print paths in matrix with obstacles and all directions
    static void printAllPaths(int[][] maze, int r, int c,
                              boolean[][] visited, String path) {
        int n = maze.length;
        if (r < 0 || c < 0 || r >= n || c >= n ||
            maze[r][c] == 0 || visited[r][c]) return;

        if (r == n - 1 && c == n - 1) {
            System.out.println(path);
            return;
        }

        visited[r][c] = true;
        printAllPaths(maze, r + 1, c, visited, path + "D");
        printAllPaths(maze, r - 1, c, visited, path + "U");
        printAllPaths(maze, r, c + 1, visited, path + "R");
        printAllPaths(maze, r, c - 1, visited, path + "L");
        visited[r][c] = false;
    }

    public static void main(String[] args) {
        System.out.println("3x3 paths (R/D): " + countRD(0, 0, 3, 3));
        System.out.println("3x3 paths (R/D/G): " + countRDD(0, 0, 3, 3));
    }
}
```

---

## Cheat Sheet

| Problem | Moves | Visited Tracking | Complexity |
|---------|-------|-----------------|------------|
| Right/Down paths | R, D | No (only forward) | O(2^(m+n)) |
| With obstacles | R, D | Obstacle check | O(2^(m+n)) |
| With diagonal | R, D, G | No | O(3^(m+n)) |
| Rat in a maze | U, D, L, R | Yes (boolean[][]) | O(4^(m*n)) |
| N-Queens | Place per row | Row check | O(n!) |
| Flood fill | U, D, L, R | Color change | O(m×n) |
| Word search | U, D, L, R | Temp marker | O(m×n×4^L) |

