# Connected Components

## What are Connected Components?

A connected component is a **maximal set of vertices** such that there's a path between every pair of vertices in the set. In simpler terms: it's a "group" of nodes that can all reach each other.

```
Graph:           Components:
0---1            [0, 1, 2]
|   |
2   3            [3, 4]
    |
    4            [5]
5
```

## Count Connected Components

```java
import java.util.*;

class ConnectedComponents {

    // Approach 1: BFS
    public static int countComponentsBFS(List<List<Integer>> adj) {
        int n = adj.size();
        boolean[] visited = new boolean[n];
        int components = 0;

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                bfs(adj, visited, i);
                components++;
            }
        }

        return components;
    }

    private static void bfs(List<List<Integer>> adj, boolean[] visited, int start) {
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

    // Approach 2: DFS
    public static int countComponentsDFS(List<List<Integer>> adj) {
        int n = adj.size();
        boolean[] visited = new boolean[n];
        int components = 0;

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                dfs(adj, visited, i);
                components++;
            }
        }

        return components;
    }

    private static void dfs(List<List<Integer>> adj, boolean[] visited, int node) {
        visited[node] = true;
        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) {
                dfs(adj, visited, neighbor);
            }
        }
    }
}
```

## Number of Islands (LeetCode 200)

Grid-based version of connected components:

```java
class NumberOfIslands {

    public int numIslands(char[][] grid) {
        int m = grid.length, n = grid[0].length;
        boolean[][] visited = new boolean[m][n];
        int islands = 0;

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == '1' && !visited[i][j]) {
                    dfs(grid, visited, i, j);
                    islands++;
                }
            }
        }

        return islands;
    }

    private void dfs(char[][] grid, boolean[][] visited, int r, int c) {
        int m = grid.length, n = grid[0].length;

        if (r < 0 || r >= m || c < 0 || c >= n) return;
        if (grid[r][c] == '0' || visited[r][c]) return;

        visited[r][c] = true;

        dfs(grid, visited, r - 1, c);
        dfs(grid, visited, r + 1, c);
        dfs(grid, visited, r, c - 1);
        dfs(grid, visited, r, c + 1);
    }

    // BFS version
    public int numIslandsBFS(char[][] grid) {
        int m = grid.length, n = grid[0].length;
        boolean[][] visited = new boolean[m][n];
        int islands = 0;
        int[][] dirs = {{-1,0},{1,0},{0,-1},{0,1}};

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == '1' && !visited[i][j]) {
                    // BFS to mark entire island
                    Queue<int[]> queue = new LinkedList<>();
                    visited[i][j] = true;
                    queue.offer(new int[]{i, j});

                    while (!queue.isEmpty()) {
                        int[] cell = queue.poll();
                        for (int[] d : dirs) {
                            int nr = cell[0] + d[0], nc = cell[1] + d[1];
                            if (nr >= 0 && nr < m && nc >= 0 && nc < n
                                && grid[nr][nc] == '1' && !visited[nr][nc]) {
                                visited[nr][nc] = true;
                                queue.offer(new int[]{nr, nc});
                            }
                        }
                    }

                    islands++;
                }
            }
        }

        return islands;
    }
}
```

## Number of Provinces (LeetCode 547)

Graph-based connected components (given adjacency matrix):

```java
class NumberOfProvinces {

    public int findCircleNum(int[][] isConnected) {
        int n = isConnected.length;
        boolean[] visited = new boolean[n];
        int provinces = 0;

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                dfs(isConnected, visited, i);
                provinces++;
            }
        }

        return provinces;
    }

    private void dfs(int[][] isConnected, boolean[] visited, int city) {
        visited[city] = true;

        for (int neighbor = 0; neighbor < isConnected.length; neighbor++) {
            if (isConnected[city][neighbor] == 1 && !visited[neighbor]) {
                dfs(isConnected, visited, neighbor);
            }
        }
    }
}
```

## Largest Component Size by Common Factor (LeetCode 952)

```java
class LargestComponent {

    // Using DSU to group numbers by common factors
    public int largestComponentSize(int[] nums) {
        int maxVal = 0;
        for (int num : nums) maxVal = Math.max(maxVal, num);

        DSU dsu = new DSU(maxVal + 1);

        for (int num : nums) {
            for (int factor = 2; factor * factor <= num; factor++) {
                if (num % factor == 0) {
                    dsu.union(num, factor);
                    dsu.union(num, num / factor);
                }
            }
        }

        // Count sizes
        Map<Integer, Integer> count = new HashMap<>();
        int maxCount = 0;

        for (int num : nums) {
            int root = dsu.find(num);
            count.merge(root, 1, Integer::sum);
            maxCount = Math.max(maxCount, count.get(root));
        }

        return maxCount;
    }

    private static class DSU {
        int[] parent, rank;

        DSU(int size) {
            parent = new int[size];
            rank = new int[size];
            for (int i = 0; i < size; i++) parent[i] = i;
        }

        int find(int x) {
            if (parent[x] != x) parent[x] = find(parent[x]);
            return parent[x];
        }

        void union(int x, int y) {
            int rx = find(x), ry = find(y);
            if (rx == ry) return;
            if (rank[rx] < rank[ry]) parent[rx] = ry;
            else if (rank[rx] > rank[ry]) parent[ry] = rx;
            else { parent[ry] = rx; rank[rx]++; }
        }
    }
}
```

## Get All Components

```java
class GetAllComponents {

    public static List<List<Integer>> getComponents(List<List<Integer>> adj) {
        int n = adj.size();
        boolean[] visited = new boolean[n];
        List<List<Integer>> components = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                List<Integer> component = new ArrayList<>();
                dfs(adj, visited, i, component);
                components.add(component);
            }
        }

        return components;
    }

    private static void dfs(List<List<Integer>> adj, boolean[] visited,
                             int node, List<Integer> component) {
        visited[node] = true;
        component.add(node);
        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) {
                dfs(adj, visited, neighbor, component);
            }
        }
    }
}
```

## Largest Component Size (LeetCode 1579)

```java
class LargestComponentSize {

    public int maxNumEdgesToRemove(int n, int[][] edges) {
        DSU alice = new DSU(n + 1);
        DSU bob = new DSU(n + 1);
        int edgesRemoved = 0;

        // Type 3 edges first (both Alice and Bob can use)
        for (int[] edge : edges) {
            if (edge[0] == 3) {
                boolean aliceUnion = alice.union(edge[1], edge[2]);
                boolean bobUnion = bob.union(edge[1], edge[2]);
                if (!aliceUnion && !bobUnion) edgesRemoved++;
            }
        }

        // Type 1 (Alice only) and Type 2 (Bob only)
        for (int[] edge : edges) {
            if (edge[0] == 1) {
                if (!alice.union(edge[1], edge[2])) edgesRemoved++;
            } else if (edge[0] == 2) {
                if (!bob.union(edge[1], edge[2])) edgesRemoved++;
            }
        }

        // Check if both have single component
        if (alice.componentCount() != 2 || bob.componentCount() != 2) {
            return -1;
        }

        return edgesRemoved;
    }

    private static class DSU {
        int[] parent, rank;
        int components;

        DSU(int size) {
            parent = new int[size];
            rank = new int[size];
            components = size - 1; // exclude index 0
            for (int i = 0; i < size; i++) parent[i] = i;
        }

        int find(int x) {
            if (parent[x] != x) parent[x] = find(parent[x]);
            return parent[x];
        }

        boolean union(int x, int y) {
            int rx = find(x), ry = find(y);
            if (rx == ry) return false;
            if (rank[rx] < rank[ry]) parent[rx] = ry;
            else if (rank[rx] > rank[ry]) parent[ry] = rx;
            else { parent[ry] = rx; rank[rx]++; }
            components--;
            return true;
        }

        int componentCount() {
            return components;
        }
    }
}
```

## Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Count components | O(V + E) | O(V) |
| Get all components | O(V + E) | O(V) |
| Grid version (Islands) | O(m × n) | O(m × n) |

## Key Patterns

1. **Graph given**: Standard BFS/DFS on adjacency list
2. **Grid given**: Treat each cell as a node, connect adjacent cells
3. **DSU approach**: Better for dynamic connectivity (adding edges over time)
4. **Union-Find**: Cleaner for counting when you don't need the actual components
