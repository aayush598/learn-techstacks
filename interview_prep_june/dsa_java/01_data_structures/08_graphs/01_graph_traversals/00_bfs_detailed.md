# BFS — Breadth-First Search

## The Core Idea

BFS explores a graph **level by level**. Starting from a source node, it visits all neighbors at distance 1, then all neighbors at distance 2, and so on. Think of dropping a stone in a pond — the ripples expand outward uniformly.

**Key insight**: The first time BFS reaches a node, that's the **shortest path** (in terms of number of edges) from the source.

## Basic BFS

```java
import java.util.*;

class BFS {

    // Standard BFS — returns nodes in BFS order
    public static List<Integer> bfs(List<List<Integer>> adj, int start) {
        List<Integer> order = new ArrayList<>();
        boolean[] visited = new boolean[adj.size()];
        Queue<Integer> queue = new LinkedList<>();

        visited[start] = true;
        queue.offer(start);

        while (!queue.isEmpty()) {
            int node = queue.poll();
            order.add(node);

            for (int neighbor : adj.get(node)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.offer(neighbor);
                }
            }
        }

        return order;
    }

    // BFS with distance tracking
    public static int[] bfsWithDistance(List<List<Integer>> adj, int start) {
        int n = adj.size();
        int[] dist = new int[n];
        Arrays.fill(dist, -1); // -1 means unreachable
        Queue<Integer> queue = new LinkedList<>();

        dist[start] = 0;
        queue.offer(start);

        while (!queue.isEmpty()) {
            int node = queue.poll();

            for (int neighbor : adj.get(node)) {
                if (dist[neighbor] == -1) {
                    dist[neighbor] = dist[node] + 1;
                    queue.offer(neighbor);
                }
            }
        }

        return dist;
    }
}
```

## Shortest Path in Unweighted Graph

BFS naturally finds shortest paths — first time reaching a node is the shortest way.

```java
class ShortestPathBFS {

    // Find shortest path and reconstruct it
    public static List<Integer> shortestPath(
            List<List<Integer>> adj, int start, int end) {

        int n = adj.size();
        int[] parent = new int[n];
        Arrays.fill(parent, -1);
        boolean[] visited = new boolean[n];

        Queue<Integer> queue = new LinkedList<>();
        visited[start] = true;
        queue.offer(start);

        while (!queue.isEmpty()) {
            int node = queue.poll();

            if (node == end) break; // found target

            for (int neighbor : adj.get(node)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    parent[neighbor] = node;
                    queue.offer(neighbor);
                }
            }
        }

        // Reconstruct path from end to start
        if (!visited[end]) return new ArrayList<>(); // no path

        List<Integer> path = new ArrayList<>();
        for (int at = end; at != -1; at = parent[at]) {
            path.add(at);
        }
        Collections.reverse(path);
        return path;
    }

    // BFS on grid — find shortest path from (sr, sc) to (tr, tc)
    public static int shortestPathGrid(int[][] grid, int sr, int sc, int tr, int tc) {
        int m = grid.length, n = grid[0].length;

        if (grid[sr][sc] == 0 || grid[tr][tc] == 0) return -1;

        int[][] dirs = {{-1,0},{1,0},{0,-1},{0,1}};
        boolean[][] visited = new boolean[m][n];
        Queue<int[]> queue = new LinkedList<>();

        visited[sr][sc] = true;
        queue.offer(new int[]{sr, sc});
        int steps = 0;

        while (!queue.isEmpty()) {
            int size = queue.size();

            for (int i = 0; i < size; i++) {
                int[] cell = queue.poll();
                int r = cell[0], c = cell[1];

                if (r == tr && c == tc) return steps;

                for (int[] d : dirs) {
                    int nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < m && nc >= 0 && nc < n
                        && !visited[nr][nc] && grid[nr][nc] == 1) {
                        visited[nr][nc] = true;
                        queue.offer(new int[]{nr, nc});
                    }
                }
            }

            steps++;
        }

        return -1; // unreachable
    }
}
```

## Connected Components with BFS

```java
class ConnectedComponentsBFS {

    // Count connected components in undirected graph
    public static int countComponents(List<List<Integer>> adj) {
        int n = adj.size();
        boolean[] visited = new boolean[n];
        int components = 0;

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                bfsComponent(adj, visited, i);
                components++;
            }
        }

        return components;
    }

    private static void bfsComponent(List<List<Integer>> adj, boolean[] visited, int start) {
        Queue<Integer> queue = new LinkedList<>();
        visited[start] = true;
        queue.offer(start);

        while (!queue.isEmpty()) {
            int node = queue.poll();
            for (int neighbor : adj.get(node)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.offer(neighbor);
                }
            }
        }
    }

    // Get all connected components
    public static List<List<Integer>> getComponents(List<List<Integer>> adj) {
        int n = adj.size();
        boolean[] visited = new boolean[n];
        List<List<Integer>> components = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                List<Integer> component = new ArrayList<>();
                bfsComponentCollect(adj, visited, i, component);
                components.add(component);
            }
        }

        return components;
    }

    private static void bfsComponentCollect(
            List<List<Integer>> adj, boolean[] visited,
            int start, List<Integer> component) {

        Queue<Integer> queue = new LinkedList<>();
        visited[start] = true;
        queue.offer(start);

        while (!queue.isEmpty()) {
            int node = queue.poll();
            component.add(node);

            for (int neighbor : adj.get(node)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.offer(neighbor);
                }
            }
        }
    }
}
```

## BFS on Grid — Number of Islands (LeetCode 200)

```java
class NumberOfIslands {

    public int numIslands(char[][] grid) {
        int m = grid.length, n = grid[0].length;
        boolean[][] visited = new boolean[m][n];
        int islands = 0;

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == '1' && !visited[i][j]) {
                    bfs(grid, visited, i, j);
                    islands++;
                }
            }
        }

        return islands;
    }

    private void bfs(char[][] grid, boolean[][] visited, int sr, int sc) {
        int m = grid.length, n = grid[0].length;
        int[][] dirs = {{-1,0},{1,0},{0,-1},{0,1}};

        Queue<int[]> queue = new LinkedList<>();
        visited[sr][sc] = true;
        queue.offer(new int[]{sr, sc});

        while (!queue.isEmpty()) {
            int[] cell = queue.poll();
            int r = cell[0], c = cell[1];

            for (int[] d : dirs) {
                int nr = r + d[0], nc = c + d[1];
                if (nr >= 0 && nr < m && nc >= 0 && nc < n
                    && grid[nr][nc] == '1' && !visited[nr][nc]) {
                    visited[nr][nc] = true;
                    queue.offer(new int[]{nr, nc});
                }
            }
        }
    }
}
```

## Multi-source BFS — Rotting Oranges (LeetCode 994)

```java
class RottingOranges {

    public int orangesRotting(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        Queue<int[]> queue = new LinkedList<>();
        int fresh = 0;

        // Add all rotten oranges to queue simultaneously
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 2) {
                    queue.offer(new int[]{i, j});
                } else if (grid[i][j] == 1) {
                    fresh++;
                }
            }
        }

        if (fresh == 0) return 0; // no fresh oranges

        int[][] dirs = {{-1,0},{1,0},{0,-1},{0,1}};
        int minutes = 0;

        while (!queue.isEmpty()) {
            int size = queue.size();
            boolean rotted = false;

            for (int i = 0; i < size; i++) {
                int[] cell = queue.poll();
                int r = cell[0], c = cell[1];

                for (int[] d : dirs) {
                    int nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < m && nc >= 0 && nc < n
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
}
```

## BFS Template for Interviews

```java
class BFSTemplate {

    // Generic BFS template
    public void bfs(List<List<Integer>> adj, int start) {
        boolean[] visited = new boolean[adj.size()];
        Queue<Integer> queue = new LinkedList<>();

        visited[start] = true;
        queue.offer(start);

        while (!queue.isEmpty()) {
            int size = queue.size(); // process level by level

            for (int i = 0; i < size; i++) {
                int node = queue.poll();

                // Process node here

                for (int neighbor : adj.get(node)) {
                    if (!visited[neighbor]) {
                        visited[neighbor] = true;
                        queue.offer(neighbor);
                    }
                }
            }
        }
    }
}
```

## Complexity

| Aspect | Complexity |
|--------|-----------|
| Time | O(V + E) — visit each vertex and edge once |
| Space | O(V) — for visited array and queue |

## When to Use BFS

- Shortest path in unweighted graph
- Level-order traversal
- Connected components
- Bipartite check
- Multi-source problems (simultaneous starts)
- When you need to explore all nodes at distance k before k+1
