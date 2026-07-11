# BFS Queue Patterns

BFS explores nodes level-by-level using a queue. Master these patterns and you'll solve most BFS problems.

---

## Pattern 1: Level-Order Tree Traversal

```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;

    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);

    while (!queue.isEmpty()) {
        int levelSize = queue.size();
        List<Integer> currentLevel = new ArrayList<>();

        for (int i = 0; i < levelSize; i++) {
            TreeNode node = queue.poll();
            currentLevel.add(node.val);
            if (node.left != null)  queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        result.add(currentLevel);
    }
    return result;
}
```

**Key pattern:** `levelSize = queue.size()` before the inner loop processes exactly one level.

---

## Pattern 2: Shortest Path in Unweighted Graph

```java
public int shortestPath(int[][] graph, int start, int end) {
    int n = graph.length;
    boolean[] visited = new boolean[n];
    Queue<Integer> queue = new LinkedList<>();

    queue.offer(start);
    visited[start] = true;
    int distance = 0;

    while (!queue.isEmpty()) {
        int size = queue.size();
        for (int i = 0; i < size; i++) {
            int node = queue.poll();
            if (node == end) return distance;

            for (int neighbor : graph[node]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.offer(neighbor);
                }
            }
        }
        distance++;
    }
    return -1; // unreachable
}
```

**Key insight:** BFS guarantees shortest path in unweighted graphs because we explore all nodes at distance d before any at distance d+1.

---

## Pattern 3: Grid BFS — Number of Islands

```java
public int numIslands(char[][] grid) {
    int count = 0;
    int rows = grid.length, cols = grid[0].length;

    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (grid[r][c] == '1') {
                count++;
                bfs(grid, r, c);
            }
        }
    }
    return count;
}

private void bfs(char[][] grid, int startR, int startC) {
    Queue<int[]> queue = new LinkedList<>();
    queue.offer(new int[]{startR, startC});
    grid[startR][startC] = '0'; // mark visited immediately

    int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};

    while (!queue.isEmpty()) {
        int[] cell = queue.poll();
        for (int[] d : dirs) {
            int nr = cell[0] + d[0];
            int nc = cell[1] + d[1];
            if (nr >= 0 && nr < grid.length &&
                nc >= 0 && nc < grid[0].length &&
                grid[nr][nc] == '1') {
                grid[nr][nc] = '0'; // mark visited
                queue.offer(new int[]{nr, nc});
            }
        }
    }
}
```

---

## Pattern 4: Multi-Source BFS — Rotting Oranges

Multiple starting points processed simultaneously.

```java
public int orangesRotting(int[][] grid) {
    Queue<int[]> queue = new LinkedList<>();
    int rows = grid.length, cols = grid[0].length;
    int fresh = 0;

    // Enqueue ALL rotten oranges at once (multi-source)
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (grid[r][c] == 2) {
                queue.offer(new int[]{r, c});
            } else if (grid[r][c] == 1) {
                fresh++;
            }
        }
    }

    if (fresh == 0) return 0;

    int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};
    int minutes = 0;

    while (!queue.isEmpty()) {
        int size = queue.size();
        boolean rotted = false;

        for (int i = 0; i < size; i++) {
            int[] cell = queue.poll();
            for (int[] d : dirs) {
                int nr = cell[0] + d[0];
                int nc = cell[1] + d[1];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols
                    && grid[nr][nc] == 1) {
                    grid[nr][nc] = 2;
                    fresh--;
                    rotted = true;
                    queue.offer(new int[]{nr, nc});
                }
            }
        }
        if (rotted) minutes++;
    }

    return fresh == 0 ? minutes : -1;
}
```

**Multi-source BFS pattern:** Initialize queue with ALL sources, process level by level.

---

## Pattern 5: 0-1 BFS (Deque for Weighted Edges 0 or 1)

Use a **Deque** instead of Queue. Edges with weight 0 go to **front**, weight 1 go to **back**.

```java
public int shortestPathBinaryMatrix(int[][] grid) {
    int n = grid.length;
    if (grid[0][0] == 1 || grid[n-1][n-1] == 1) return -1;

    int[][] dist = new int[n][n];
    for (int[] row : dist) Arrays.fill(row, Integer.MAX_VALUE);
    dist[0][0] = 0;

    Deque<int[]> deque = new ArrayDeque<>();
    deque.offerFirst(new int[]{0, 0});

    int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0},{1,1},{1,-1},{-1,1},{-1,-1}};

    while (!deque.isEmpty()) {
        int[] cell = deque.pollFirst();
        int r = cell[0], c = cell[1];

        for (int[] d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] == 0) {
                int newDist = dist[r][c] + 1; // all edges weight 1 here
                if (newDist < dist[nr][nc]) {
                    dist[nr][nc] = newDist;
                    deque.offerLast(new int[]{nr, nc});
                }
            }
        }
    }
    return dist[n-1][n-1] == Integer.MAX_VALUE ? -1 : dist[n-1][n-1] + 1;
}
```

**General 0-1 BFS pattern:**
```java
// For graph where edge weights are 0 or 1:
Deque<int[]> deque = new ArrayDeque<>();
deque.offerFirst(start);

while (!deque.isEmpty()) {
    int[] node = deque.pollFirst();
    for (Edge e : neighbors(node)) {
        if (dist[node] + e.weight < dist[e.target]) {
            dist[e.target] = dist[node] + e.weight;
            if (e.weight == 0) deque.offerFirst(e.target);
            else               deque.offerLast(e.target);
        }
    }
}
```

---

## Pattern Recognition Guide

| Scenario | Pattern | Data Structure |
|----------|---------|---------------|
| Level-by-level processing | Standard BFS | Queue |
| Shortest path in unweighted graph | BFS | Queue |
| Multiple starting points | Multi-source BFS | Queue (init with all sources) |
| Edge weights 0 or 1 | 0-1 BFS | Deque |
| Minimum effort with small weights | Dijkstra (or 0-1 BFS if only 0/1) | PriorityQueue or Deque |
| Word ladder / transformation | BFS on implicit graph | Queue |
| State space search | BFS on state graph | Queue + visited set |

---

## Common BFS Gotchas

1. **Forgetting to mark visited on enqueue** (not dequeue) → causes TLE from re-processing.
2. **Not handling empty queue initially** → check `root != null` or grid bounds.
3. **Using DFS when BFS is needed** → DFS doesn't guarantee shortest path.
4. **Multi-source: enqueue all sources before processing** → don't process level 0 partially.
