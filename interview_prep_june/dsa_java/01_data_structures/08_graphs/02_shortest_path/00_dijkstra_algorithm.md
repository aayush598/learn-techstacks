# Dijkstra's Algorithm

## Overview

Finds **shortest path** from a source to all vertices in a weighted graph with **non-negative** weights.

## Algorithm

1. Initialize `dist[source] = 0`, all others = INF
2. Use **min-heap** (priority queue) of (distance, vertex)
3. While heap not empty: pop smallest distance, relax all neighbors
4. **Relax**: if `dist[u] + weight(u,v) < dist[v]`, update and push

## Implementation

```java
int[] dijkstra(List<List<int[]>> graph, int source) {
    int n = graph.size();
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[source] = 0;
    
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
    pq.offer(new int[]{0, source});  // [distance, vertex]
    
    while (!pq.isEmpty()) {
        int[] curr = pq.poll();
        int d = curr[0], u = curr[1];
        
        if (d > dist[u]) continue;  // skip outdated entries
        
        for (int[] edge : graph.get(u)) {
            int v = edge[0], w = edge[1];
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.offer(new int[]{dist[v], v});
            }
        }
    }
    
    return dist;
}
```

## Path Reconstruction

```java
int[] dijkstraWithPath(List<List<int[]>> graph, int source) {
    int n = graph.size();
    int[] dist = new int[n];
    int[] parent = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    Arrays.fill(parent, -1);
    dist[source] = 0;
    
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
    pq.offer(new int[]{0, source});
    
    while (!pq.isEmpty()) {
        int[] curr = pq.poll();
        int d = curr[0], u = curr[1];
        if (d > dist[u]) continue;
        
        for (int[] edge : graph.get(u)) {
            int v = edge[0], w = edge[1];
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                parent[v] = u;
                pq.offer(new int[]{dist[v], v});
            }
        }
    }
    return parent;
}

List<Integer> getPath(int[] parent, int target) {
    List<Integer> path = new ArrayList<>();
    for (int v = target; v != -1; v = parent[v]) path.add(v);
    Collections.reverse(path);
    return path;
}
```

## Complexity

- Time: O((V + E) log V) with binary heap
- Space: O(V)

## Key Points

- **Does NOT work with negative weights** (use Bellman-Ford)
- **Greedy algorithm**: always picks the globally minimum distance
- Each vertex processed once (when popped from heap)
- Can early-terminate when target is popped (if single-pair shortest path)

## Dijkstra on Grid

```java
int minPathSum(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    int[][] dist = new int[m][n];
    for (int[] row : dist) Arrays.fill(row, Integer.MAX_VALUE);
    dist[0][0] = grid[0][0];
    
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[2] - b[2]);
    pq.offer(new int[]{0, 0, grid[0][0]});
    int[][] dirs = {{0,1}, {1,0}, {0,-1}, {-1,0}};
    
    while (!pq.isEmpty()) {
        int[] curr = pq.poll();
        int r = curr[0], c = curr[1], d = curr[2];
        if (d > dist[r][c]) continue;
        
        for (int[] dir : dirs) {
            int nr = r + dir[0], nc = c + dir[1];
            if (nr >= 0 && nr < m && nc >= 0 && nc < n) {
                if (dist[r][c] + grid[nr][nc] < dist[nr][nc]) {
                    dist[nr][nc] = dist[r][c] + grid[nr][nc];
                    pq.offer(new int[]{nr, nc, dist[nr][nc]});
                }
            }
        }
    }
    
    return dist[m-1][n-1];
}
```
