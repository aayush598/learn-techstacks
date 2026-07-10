# DFS — Depth-First Search

## The Core Idea

DFS explores a graph by going **as deep as possible** along each branch before backtracking. Think of exploring a maze — you keep going down one path until you hit a dead end, then backtrack and try another path.

DFS can be implemented with **recursion** (call stack) or an **explicit stack**.

## Basic DFS — Recursive

```java
import java.util.*;

class DFS {

    // Recursive DFS — returns nodes in visit order
    public static List<Integer> dfsRecursive(List<List<Integer>> adj, int start) {
        List<Integer> order = new ArrayList<>();
        boolean[] visited = new boolean[adj.size()];
        dfsHelper(adj, start, visited, order);
        return order;
    }

    private static void dfsHelper(
            List<List<Integer>> adj, int node,
            boolean[] visited, List<Integer> order) {

        visited[node] = true;
        order.add(node); // PRE-ORDER: process before children

        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) {
                dfsHelper(adj, neighbor, visited, order);
            }
        }
    }

    // DFS for all components (handles disconnected graphs)
    public static List<Integer> dfsAll(List<List<Integer>> adj) {
        List<Integer> order = new ArrayList<>();
        boolean[] visited = new boolean[adj.size()];

        for (int i = 0; i < adj.size(); i++) {
            if (!visited[i]) {
                dfsHelper(adj, i, visited, order);
            }
        }

        return order;
    }
}
```

## DFS — Iterative with Stack

```java
class DFSIterative {

    // Iterative DFS using explicit stack
    public static List<Integer> dfsIterative(List<List<Integer>> adj, int start) {
        List<Integer> order = new ArrayList<>();
        boolean[] visited = new boolean[adj.size()];
        Deque<Integer> stack = new ArrayDeque<>();

        stack.push(start);

        while (!stack.isEmpty()) {
            int node = stack.pop();

            if (visited[node]) continue;
            visited[node] = true;
            order.add(node);

            // Push neighbors in reverse order for correct left-to-right traversal
            List<Integer> neighbors = adj.get(node);
            for (int i = neighbors.size() - 1; i >= 0; i--) {
                if (!visited[neighbors.get(i)]) {
                    stack.push(neighbors.get(i));
                }
            }
        }

        return order;
    }
}
```

## Pre-order vs Post-order

```java
class DFSTraversalOrders {

    // PRE-ORDER: Process node BEFORE children
    public static void preorder(List<List<Integer>> adj, int node,
                                 boolean[] visited, List<Integer> result) {
        visited[node] = true;
        result.add(node); // ← HERE: before children

        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) {
                preorder(adj, neighbor, visited, result);
            }
        }
    }

    // POST-ORDER: Process node AFTER all children
    public static void postorder(List<List<Integer>> adj, int node,
                                  boolean[] visited, List<Integer> result) {
        visited[node] = true;

        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) {
                postorder(adj, neighbor, visited, result);
            }
        }

        result.add(node); // ← HERE: after children
    }
}
```

## Connected Components with DFS

```java
class ConnectedComponentsDFS {

    // Count connected components
    public static int countComponents(List<List<Integer>> adj) {
        int n = adj.size();
        boolean[] visited = new boolean[n];
        int components = 0;

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                dfsComponent(adj, visited, i);
                components++;
            }
        }

        return components;
    }

    private static void dfsComponent(List<List<Integer>> adj,
                                      boolean[] visited, int node) {
        visited[node] = true;
        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) {
                dfsComponent(adj, visited, neighbor);
            }
        }
    }

    // Get all connected components
    public static List<List<Integer>> getAllComponents(List<List<Integer>> adj) {
        int n = adj.size();
        boolean[] visited = new boolean[n];
        List<List<Integer>> components = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                List<Integer> component = new ArrayList<>();
                dfsCollect(adj, visited, i, component);
                components.add(component);
            }
        }

        return components;
    }

    private static void dfsCollect(List<List<Integer>> adj, boolean[] visited,
                                    int node, List<Integer> component) {
        visited[node] = true;
        component.add(node);
        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) {
                dfsCollect(adj, visited, neighbor, component);
            }
        }
    }
}
```

## DFS on Grid — Flood Fill (LeetCode 733)

```java
class FloodFill {

    public int[][] floodFill(int[][] image, int sr, int sc, int newColor) {
        int originalColor = image[sr][sc];
        if (originalColor == newColor) return image;

        dfs(image, sr, sc, originalColor, newColor);
        return image;
    }

    private void dfs(int[][] image, int r, int c, int originalColor, int newColor) {
        int m = image.length, n = image[0].length;

        if (r < 0 || r >= m || c < 0 || c >= n) return;
        if (image[r][c] != originalColor) return;

        image[r][c] = newColor;

        dfs(image, r - 1, c, originalColor, newColor);
        dfs(image, r + 1, c, originalColor, newColor);
        dfs(image, r, c - 1, originalColor, newColor);
        dfs(image, r, c + 1, originalColor, newColor);
    }
}
```

## DFS on Grid — Island Perimeter (LeetCode 463)

```java
class IslandPerimeter {

    public int islandPerimeter(int[][] grid) {
        int m = grid.length, n = grid[0].length;

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1) {
                    return dfs(grid, i, j);
                }
            }
        }
        return 0;
    }

    private int dfs(int[][] grid, int r, int c) {
        int m = grid.length, n = grid[0].length;

        // Out of bounds or water → count as perimeter edge
        if (r < 0 || r >= m || c < 0 || c >= n || grid[r][c] == 0) {
            return 1;
        }

        // Already visited
        if (grid[r][c] == -1) return 0;

        // Mark as visited
        grid[r][c] = -1;

        // Sum perimeter from all 4 directions
        return dfs(grid, r - 1, c)
             + dfs(grid, r + 1, c)
             + dfs(grid, r, c - 1)
             + dfs(grid, r, c + 1);
    }
}
```

## Cycle Detection in Undirected Graph

```java
class CycleDetectionUndirected {

    // DFS-based cycle detection
    public boolean hasCycle(List<List<Integer>> adj) {
        int n = adj.size();
        boolean[] visited = new boolean[n];

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                if (dfsCycle(adj, visited, i, -1)) {
                    return true;
                }
            }
        }

        return false;
    }

    // Returns true if cycle is found
    // parent: the node we came from (to avoid false positive on undirected edges)
    private boolean dfsCycle(List<List<Integer>> adj, boolean[] visited,
                              int node, int parent) {
        visited[node] = true;

        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) {
                if (dfsCycle(adj, visited, neighbor, node)) {
                    return true;
                }
            } else if (neighbor != parent) {
                // Visited neighbor that's NOT the parent → cycle!
                return true;
            }
        }

        return false;
    }
}
```

## Cycle Detection in Directed Graph

```java
class CycleDetectionDirected {

    // DFS with 3 states: 0=unvisited, 1=visiting, 2=done
    public boolean hasCycle(List<List<Integer>> adj) {
        int n = adj.size();
        int[] state = new int[n]; // 0=unvisited, 1=visiting, 2=done

        for (int i = 0; i < n; i++) {
            if (state[i] == 0) {
                if (dfsCycle(adj, state, i)) {
                    return true;
                }
            }
        }

        return false;
    }

    private boolean dfsCycle(List<List<Integer>> adj, int[] state, int node) {
        state[node] = 1; // mark as visiting

        for (int neighbor : adj.get(node)) {
            if (state[neighbor] == 1) {
                return true; // back edge → cycle!
            }
            if (state[neighbor] == 0) {
                if (dfsCycle(adj, state, neighbor)) {
                    return true;
                }
            }
        }

        state[node] = 2; // mark as done
        return false;
    }
}
```

## DFS Complexity

| Aspect | Complexity |
|--------|-----------|
| Time | O(V + E) — visit each vertex and edge once |
| Space | O(V) — for visited array + recursion stack (worst case O(V) deep) |

## When to Use DFS

- Cycle detection
- Connected components
- Path finding (all paths, specific constraints)
- Topological sort
- Backtracking problems (N-queens, Sudoku)
- When you need to explore all possibilities
- Grid problems (flood fill, island counting)
