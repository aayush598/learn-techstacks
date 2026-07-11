# Samsung R&D Interview

> "Samsung R&D is one of India's biggest campus recruiters. Known for hard problems, grid/2D-array challenges, and sometimes 'no internet' coding rounds. They want complete, working solutions with all edge cases handled."

---

## 1. Company Overview

- **Package:** ₹10-20 LPA (freshers), higher for NITs/IITs
- **Hiring:** Campus recruitment (massive hiring), off-campus rare
- **Rounds:** Online Test → Technical (2-3 rounds) → HR
- **Focus:** DSA, implementation, grid problems, optimization
- **Key Differentiator:** **Hard problems** and **offline coding rounds** (no internet)

---

## 2. Interview Process

### Online Test (HackerRank or Offline)
- 3-4 coding problems (Medium to Hard)
- Time limit: 90-120 minutes
- Sometimes conducted **offline** — no internet, no auto-complete
- Topics: Arrays, Graphs, DP, Implementation
- Cutoff is competitive — aim for all test cases

### Technical Rounds (2-3 rounds, 45-60 min each)

| Round | Focus | Difficulty |
|-------|-------|------------|
| Round 1 | DSA Coding (Arrays/Grid) | Medium-Hard |
| Round 2 | DSA Coding (Graphs/DP) | Hard |
| Round 3 | System Design / CS Fundamentals | Medium |

### HR Round (30 min)
- Basic behavioral questions
- Salary negotiation
- Location preference

### What Makes Samsung R&D Different
- **Hard problems** — They don't shy away from difficulty
- **Grid/2D-array problems** are very common
- **Implementation-heavy** — They want complete, working code
- **No internet coding** — Some rounds are offline (no IDE, no Google)
- **Edge case handling** — They test thoroughly
- **Simulation problems** — Model real-world scenarios in code

---

## 3. Most Asked Topics

### Topic Priority

| Priority | Topic | Frequency | Example Problems |
|----------|-------|-----------|-----------------|
| 1 | Arrays | 90% | Kadane's, merge, rotate |
| 2 | Graphs | 80% | BFS/DFS, shortest path, islands |
| 3 | DP | 75% | Knapsack, LIS, grid DP |
| 4 | Backtracking | 65% | N-Queens, Sudoku, permutations |
| 5 | Implementation | 60% | Simulation, string manipulation |
| 6 | Trees | 50% | BST basics, traversals |
| 7 | HashMaps | 45% | Frequency, grouping |

### Topic Frequency Graph
```
Arrays:     ████████████████████
Graphs:     ██████████████████
DP:         █████████████████
Backtrack:  █████████████
Implement:  ████████████
Trees:      ██████████
HashMaps:   █████████
```

### What Makes Samsung Different
- **Grid problems** are king — they love 2D array challenges
- **Simulation** — Model real-world scenarios in code
- **Complete solutions** — Partial credit is minimal
- **Edge cases** — They test boundary conditions thoroughly
- **Offline coding** — Practice without internet/IDE

---

## 4. Common Problems (Top 20)

### Grid / 2D Array Problems
1. Number of Islands
2. Rotting Oranges (BFS)
3. Maximal Rectangle in Binary Matrix
4. Spiral Matrix
5. Game of Life (in-place update)
6. Word Search in Grid
7. Unique Paths in Grid

### Graph Problems
8. Shortest Path in Binary Matrix
9. Course Schedule (Topological Sort)
10. Clone Graph
11. Number of Provinces
12. Flood Fill

### DP Problems
13. 0/1 Knapsack
14. Longest Increasing Subsequence
15. Edit Distance
16. Unique Paths with Obstacles
17. Maximum Square in Binary Matrix

### Implementation
18. N-Queens
19. Sudoku Solver
20. Spiral Matrix Generation

---

## 5. Example Problems with Approaches

### Problem 1: Number of Islands
**Why Samsung asks this:** Grid traversal is fundamental; tests BFS/DFS mastery.

```java
public class NumberOfIslands {

    public static int numIslands(char[][] grid) {
        if (grid == null || grid.length == 0) return 0;
        
        int count = 0;
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[0].length; j++) {
                if (grid[i][j] == '1') {
                    count++;
                    dfs(grid, i, j);
                }
            }
        }
        return count;
    }
    
    private static void dfs(char[][] grid, int row, int col) {
        if (row < 0 || row >= grid.length || col < 0 
            || col >= grid[0].length || grid[row][col] == '0') {
            return;
        }
        
        grid[row][col] = '0'; // Mark visited
        
        dfs(grid, row + 1, col);
        dfs(grid, row - 1, col);
        dfs(grid, row, col + 1);
        dfs(grid, row, col - 1);
    }
    
    public static void main(String[] args) {
        char[][] grid = {
            {'1','1','0','0','0'},
            {'1','1','0','0','0'},
            {'0','0','1','0','0'},
            {'0','0','0','1','1'}
        };
        System.out.println(numIslands(grid)); // 3
    }
}
```

**Time:** O(m × n) | **Space:** O(m × n) for recursion stack

---

### Problem 2: Rotting Oranges (BFS on Grid)
**Why Samsung asks this:** Multi-source BFS — simulates spread/propagation.

```java
import java.util.*;

public class RottingOranges {

    // APPROACH: Multi-source BFS
    // Add all rotten oranges to queue simultaneously
    // Each level of BFS = one minute
    // Count minutes until no fresh orange can be reached
    
    public static int orangesRotting(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        Queue<int[]> queue = new LinkedList<>();
        int fresh = 0;
        
        // Add all rotten oranges and count fresh
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == 2) {
                    queue.offer(new int[]{i, j});
                } else if (grid[i][j] == 1) {
                    fresh++;
                }
            }
        }
        
        if (fresh == 0) return 0;
        
        int[][] dirs = {{-1,0},{1,0},{0,-1},{0,1}};
        int minutes = 0;
        
        while (!queue.isEmpty()) {
            int size = queue.size();
            boolean rotted = false;
            
            for (int i = 0; i < size; i++) {
                int[] cell = queue.poll();
                
                for (int[] dir : dirs) {
                    int newRow = cell[0] + dir[0];
                    int newCol = cell[1] + dir[1];
                    
                    if (newRow >= 0 && newRow < rows && newCol >= 0 
                        && newCol < cols && grid[newRow][newCol] == 1) {
                        grid[newRow][newCol] = 2;
                        fresh--;
                        rotted = true;
                        queue.offer(new int[]{newRow, newCol});
                    }
                }
            }
            
            if (rotted) minutes++;
        }
        
        return fresh == 0 ? minutes : -1;
    }
    
    public static void main(String[] args) {
        int[][] grid1 = {{2,1,1},{1,1,0},{0,1,1}};
        System.out.println(orangesRotting(grid1)); // 4
        
        int[][] grid2 = {{2,1,1},{0,1,1},{1,0,1}};
        System.out.println(orangesRotting(grid2)); // -1 (some remain fresh)
    }
}
```

**Time:** O(m × n) | **Space:** O(m × n)

---

### Problem 3: 0/1 Knapsack
**Why Samsung asks this:** Classic optimization problem; tests DP understanding.

```java
public class Knapsack {

    // APPROACH: 2D DP
    // dp[i][w] = max value using first i items with capacity w
    // For each item: either include it or skip it
    
    public static int knapsack(int[] weights, int[] values, int capacity) {
        int n = weights.length;
        int[][] dp = new int[n + 1][capacity + 1];
        
        for (int i = 1; i <= n; i++) {
            for (int w = 0; w <= capacity; w++) {
                // Skip current item
                dp[i][w] = dp[i - 1][w];
                
                // Include current item (if it fits)
                if (weights[i - 1] <= w) {
                    dp[i][w] = Math.max(
                        dp[i][w],
                        dp[i - 1][w - weights[i - 1]] + values[i - 1]
                    );
                }
            }
        }
        
        return dp[n][capacity];
    }
    
    // SPACE OPTIMIZED: 1D DP
    public static int knapsackOptimized(int[] weights, int[] values, int capacity) {
        int[] dp = new int[capacity + 1];
        
        for (int i = 0; i < weights.length; i++) {
            for (int w = capacity; w >= weights[i]; w--) {
                dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
            }
        }
        
        return dp[capacity];
    }

    public static void main(String[] args) {
        int[] weights = {2, 3, 4, 5};
        int[] values = {3, 4, 5, 6};
        int capacity = 8;
        
        System.out.println(knapsack(weights, values, capacity)); // 10
        System.out.println(knapsackOptimized(weights, values, capacity)); // 10
    }
}
```

**Time:** O(n × capacity) | **Space:** O(n × capacity) for 2D, O(capacity) for 1D

---

### Problem 4: Unique Paths in Grid
```java
public class UniquePaths {

    public static int uniquePaths(int m, int n) {
        int[][] dp = new int[m][n];
        
        // Base cases: first row and first column have only 1 path
        for (int i = 0; i < m; i++) dp[i][0] = 1;
        for (int j = 0; j < n; j++) dp[0][j] = 1;
        
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
            }
        }
        
        return dp[m - 1][n - 1];
    }
    
    public static void main(String[] args) {
        System.out.println(uniquePaths(3, 7)); // 28
        System.out.println(uniquePaths(3, 2)); // 3
    }
}
```

**Time:** O(m × n) | **Space:** O(m × n), can optimize to O(n)

---

### Problem 5: N-Queens
**Why Samsung asks this:** Backtracking mastery — they love this problem.

```java
import java.util.*;

public class NQueens {

    public static int solveNQueens(int n) {
        char[][] board = new char[n][n];
        for (char[] row : board) Arrays.fill(row, '.');
        return backtrack(board, 0);
    }
    
    private static int backtrack(char[][] board, int row) {
        if (row == board.length) return 1;
        
        int count = 0;
        for (int col = 0; col < board.length; col++) {
            if (isSafe(board, row, col)) {
                board[row][col] = 'Q';
                count += backtrack(board, row + 1);
                board[row][col] = '.';
            }
        }
        return count;
    }
    
    private static boolean isSafe(char[][] board, int row, int col) {
        int n = board.length;
        
        for (int i = 0; i < row; i++) {
            if (board[i][col] == 'Q') return false;
        }
        for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
            if (board[i][j] == 'Q') return false;
        }
        for (int i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++) {
            if (board[i][j] == 'Q') return false;
        }
        
        return true;
    }
    
    public static void main(String[] args) {
        System.out.println(solveNQueens(4));  // 2
        System.out.println(solveNQueens(8));  // 92
    }
}
```

**Time:** O(n!) | **Space:** O(n²)

---

## 6. Preparation Strategy

### Focus Areas (5-Week Plan — Samsung needs extra prep)

#### Week 1: Grid/2D Array Mastery
- [ ] BFS/DFS on grids (10 problems)
- [ ] Spiral matrix, rotation (5 problems)
- [ ] Matrix search problems (5 problems)
- [ ] Practice: 15 problems

#### Week 2: Graph Algorithms
- [ ] BFS/DFS on graphs (10 problems)
- [ ] Shortest path (5 problems)
- [ ] Topological sort (5 problems)
- [ ] Flood fill variants (5 problems)
- [ ] Practice: 15 problems

#### Week 3: DP Patterns
- [ ] 1D DP (10 problems)
- [ ] 2D DP (10 problems)
- [ ] Knapsack variants (5 problems)
- [ ] Grid DP (5 problems)
- [ ] Practice: 15 problems

#### Week 4: Backtracking and Implementation
- [ ] N-Queens, Sudoku (5 problems)
- [ ] Permutation/combination (5 problems)
- [ ] Simulation problems (5 problems)
- [ ] Practice: 10 problems

#### Week 5: Offline Practice + Mocks
- [ ] Practice without internet (write code on paper)
- [ ] Mock interviews (3-5 sessions)
- [ ] Review and consolidate
- [ ] Focus on complete, working solutions

### Samsung-Specific Tips
1. **Grid problems are key** — Practice BFS/DFS on 2D arrays
2. **Complete solutions** — Partial credit is minimal
3. **Handle all edge cases** — Empty grid, single cell, no path
4. **Practice offline** — Write code on paper without IDE
5. **Simulation problems** — Model real-world scenarios
6. **Time yourself** — They have strict time limits
7. **Don't use libraries** — Offline rounds may not have them
8. **Test thoroughly** — Samsung tests edge cases aggressively

### Common Follow-up Questions
- "What if the grid is very large (10^6 × 10^6)?"
- "Can you optimize the space complexity?"
- "What if there are obstacles in the grid?"
- "How would you handle concurrent modifications?"
- "Can you do it without recursion?"

### Resources
- LeetCode Grid problems tag
- Graph algorithm implementations
- Backtracking problem collections
- Practice writing code on paper

---

> **Remember:** Samsung R&D wants complete, working solutions. Grid problems are their specialty — master BFS/DFS on 2D arrays. Practice offline coding — you may not have internet or IDE during the actual test.
