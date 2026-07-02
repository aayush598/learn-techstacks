# Rat in a Maze

**Problem**: Given an N×N maze where cells with value 1 are open and 0 are blocked, find a path from (0,0) to (N-1,N-1). The rat can move in all four directions (up, down, left, right).

**Example**:
```
Maze:
1  0  0  0
1  1  0  1
0  1  0  0
1  1  1  1

Output path: (0,0) → (1,0) → (1,1) → (2,1) → (3,1) → (3,2) → (3,3)
```

---

## Basic Solution (All Directions)

```java
public class RatInMaze {
    private static final int[] ROW_DIR = {-1, 1, 0, 0}; // U, D, L, R
    private static final int[] COL_DIR = {0, 0, -1, 1};
    private static final char[] DIR = {'U', 'D', 'L', 'R'};

    public List<String> findPath(int[][] maze) {
        List<String> paths = new ArrayList<>();
        int n = maze.length;

        // Edge case: start or end is blocked
        if (maze[0][0] == 0 || maze[n-1][n-1] == 0) return paths;

        boolean[][] visited = new boolean[n][n];
        visited[0][0] = true;
        StringBuilder currentPath = new StringBuilder();

        backtrack(maze, 0, 0, visited, currentPath, paths);
        return paths;
    }

    private void backtrack(int[][] maze, int row, int col,
                           boolean[][] visited, StringBuilder currentPath,
                           List<String> paths) {
        int n = maze.length;

        // Reached destination
        if (row == n - 1 && col == n - 1) {
            paths.add(currentPath.toString());
            return;
        }

        for (int i = 0; i < 4; i++) {
            int nextRow = row + ROW_DIR[i];
            int nextCol = col + COL_DIR[i];

            if (isValid(maze, nextRow, nextCol, visited)) {
                visited[nextRow][nextCol] = true;
                currentPath.append(DIR[i]);

                backtrack(maze, nextRow, nextCol, visited, currentPath, paths);

                currentPath.deleteCharAt(currentPath.length() - 1);
                visited[nextRow][nextCol] = false;
            }
        }
    }

    private boolean isValid(int[][] maze, int row, int col, boolean[][] visited) {
        int n = maze.length;
        return row >= 0 && row < n && col >= 0 && col < n
               && maze[row][col] == 1 && !visited[row][col];
    }
}
```

---

## Lexicographical Order

If paths need to be in lexicographical order, order the directions as D, L, R, U:

```java
// Order directions so paths come out in lexicographic order
private static final char[] DIR = {'D', 'L', 'R', 'U'};
private static final int[] ROW_DIR = {1, 0, 0, -1}; // D, L, R, U
private static final int[] COL_DIR = {0, -1, 1, 0};
```

**Why D, L, R, U?** Lexicographic order of path strings: all D-paths first, then L-paths, etc.

---

## Print All Paths

```java
public void printAllPaths(int[][] maze) {
    int n = maze.length;
    if (maze[0][0] == 0 || maze[n-1][n-1] == 0) return;

    int[][] path = new int[n][n];
    path[0][0] = 1; // mark start

    explore(maze, 0, 0, path);
}

private void explore(int[][] maze, int row, int col, int[][] path) {
    int n = maze.length;

    if (row == n - 1 && col == n - 1) {
        printPath(path);
        return;
    }

    for (int i = 0; i < 4; i++) {
        int nextRow = row + ROW_DIR[i];
        int nextCol = col + COL_DIR[i];

        if (isSafe(maze, nextRow, nextCol, path)) {
            path[nextRow][nextCol] = 1;
            explore(maze, nextRow, nextCol, path);
            path[nextRow][nextCol] = 0;
        }
    }
}

private boolean isSafe(int[][] maze, int row, int col, int[][] path) {
    int n = maze.length;
    return row >= 0 && row < n && col >= 0 && col < n
           && maze[row][col] == 1 && path[row][col] == 0;
}

private void printPath(int[][] path) {
    for (int[] row : path) {
        for (int cell : row) {
            System.out.print(cell + " ");
        }
        System.out.println();
    }
    System.out.println();
}
```

---

## Finding Shortest Path (BFS)

Backtracking finds ALL paths. For the shortest path, use BFS:

```java
public List<int[]> findShortestPath(int[][] maze) {
    int n = maze.length;
    if (maze[0][0] == 0 || maze[n-1][n-1] == 0) return new ArrayList<>();

    boolean[][] visited = new boolean[n][n];
    int[][] parent = new int[n][n]; // store parent direction
    Queue<int[]> queue = new LinkedList<>();

    queue.offer(new int[]{0, 0});
    visited[0][0] = true;
    parent[0][0] = -1;

    int[] rowDir = {-1, 1, 0, 0};
    int[] colDir = {0, 0, -1, 1};
    int[] dirCode = {0, 1, 2, 3}; // U, D, L, R

    while (!queue.isEmpty()) {
        int[] curr = queue.poll();
        int r = curr[0], c = curr[1];

        if (r == n - 1 && c == n - 1) {
            return reconstructPath(parent, r, c, rowDir, colDir);
        }

        for (int i = 0; i < 4; i++) {
            int nr = r + rowDir[i];
            int nc = c + colDir[i];

            if (nr >= 0 && nr < n && nc >= 0 && nc < n
                && maze[nr][nc] == 1 && !visited[nr][nc]) {
                visited[nr][nc] = true;
                parent[nr][nc] = i; // store direction from parent
                queue.offer(new int[]{nr, nc});
            }
        }
    }

    return new ArrayList<>(); // no path
}

private List<int[]> reconstructPath(int[][] parent, int endR, int endC,
                                     int[] rowDir, int[] colDir) {
    List<int[]> path = new ArrayList<>();
    int r = endR, c = endC;

    while (parent[r][c] != -1) {
        path.add(0, new int[]{r, c});
        int dir = parent[r][c];
        // Go backwards: subtract the direction that was added
        r -= rowDir[dir];
        c -= colDir[dir];
    }
    path.add(0, new int[]{0, 0}); // add start

    return path;
}
```

---

## Optimization: Mark Visited to Avoid Cycles

The `visited` array is crucial — without it, the rat would move back and forth forever:

```
Without visited: (0,0) → (1,0) → (0,0) → (1,0) → (0,0) → ... (infinite loop)
With visited: Each cell visited at most once per path
```

### Alternative: Modify the Maze In-Place

```java
// Use maze itself as visited marker (modifying input)
private boolean explore(int[][] maze, int row, int col, String path) {
    int n = maze.length;
    if (row == n - 1 && col == n - 1) {
        System.out.println(path);
        return true;
    }

    int original = maze[row][col];
    maze[row][col] = 0; // mark visited

    // Try all directions
    for (int i = 0; i < 4; i++) {
        int nr = row + ROW_DIR[i];
        int nc = col + COL_DIR[i];
        if (nr >= 0 && nr < n && nc >= 0 && nc < n && maze[nr][nc] == 1) {
            if (explore(maze, nr, nc, path + DIR[i])) return true;
        }
    }

    maze[row][col] = original; // restore
    return false;
}
```

---

## Variants

### 1. Multiple Rats

```java
// Place multiple rats, each needing a non-overlapping path
// More complex — requires paths to share no cells
```

### 2. Maze with Jumps

```java
// Rat can jump k steps in any direction
private void backtrack(int[][] maze, int row, int col, int jump,
                       boolean[][] visited, List<int[]> path) {
    // Try jumping 1..jump steps in each direction
    for (int step = 1; step <= jump; step++) {
        for (int dir = 0; dir < 4; dir++) {
            int nr = row + ROW_DIR[dir] * step;
            int nc = col + COL_DIR[dir] * step;
            // ... proceed as normal
        }
    }
}
```

### 3. Maze with Keys and Doors

```java
// Rat needs to collect keys to open doors
// State includes collected keys (bitmask)
private void backtrack(int[][] maze, int row, int col,
                       int keys, boolean[][][] visited) {
    // visited[row][col][keys] — state includes key configuration
    // ...
}
```

### 4. Count Number of Paths

```java
public int countPaths(int[][] maze) {
    int n = maze.length;
    if (maze[0][0] == 0 || maze[n-1][n-1] == 0) return 0;
    boolean[][] visited = new boolean[n][n];
    visited[0][0] = true;
    return count(maze, 0, 0, visited);
}

private int count(int[][] maze, int row, int col, boolean[][] visited) {
    int n = maze.length;
    if (row == n - 1 && col == n - 1) return 1;

    int total = 0;
    for (int i = 0; i < 4; i++) {
        int nr = row + ROW_DIR[i];
        int nc = col + COL_DIR[i];
        if (isValid(maze, nr, nc, visited)) {
            visited[nr][nc] = true;
            total += count(maze, nr, nc, visited);
            visited[nr][nc] = false;
        }
    }
    return total;
}
```

---

## Complexity Analysis

| Variant | Time | Space |
|---|---|---|
| All paths (backtracking) | O(4^(N²)) worst | O(N²) |
| Any path (backtracking + early exit) | O(4^(N²)) worst, much better avg | O(N²) |
| Shortest path (BFS) | O(N²) | O(N²) |
| Count paths | O(4^(N²)) | O(N²) |

---

## Key Takeaways

1. **Visited array is essential** — prevents infinite loops
2. **Backtracking finds ALL paths** — BFS/Dijkstra for shortest
3. **Four-direction movement** requires careful visited tracking
4. **Lexicographic order** requires specific direction ordering (D, L, R, U)
5. **Rat in a Maze** is the foundational grid backtracking problem — variations include obstacles, keys, multiple rats, and jumps

## Common Interview Follow-ups

1. "Can you modify to find the shortest path?" → Switch to BFS
2. "What if the rat can move diagonally?" → Add 4 more directions
3. "What if there are multiple destinations?" → Check any destination
4. "What if the maze is very large?" → Consider A* or IDA* for better performance
