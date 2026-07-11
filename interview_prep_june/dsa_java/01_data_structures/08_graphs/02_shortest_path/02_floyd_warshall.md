# Floyd-Warshall Algorithm

## Overview

**All-pairs shortest path** in a weighted graph. Works with negative weights, detects negative cycles.

## Algorithm

```java
void floydWarshall(int[][] graph) {
    int V = graph.length;
    int[][] dist = new int[V][V];
    
    // Initialize dist matrix
    for (int i = 0; i < V; i++) {
        for (int j = 0; j < V; j++) {
            dist[i][j] = graph[i][j];
        }
    }
    
    // Core DP: for each intermediate vertex k
    for (int k = 0; k < V; k++) {
        for (int i = 0; i < V; i++) {
            for (int j = 0; j < V; j++) {
                if (dist[i][k] != Integer.MAX_VALUE && 
                    dist[k][j] != Integer.MAX_VALUE &&
                    dist[i][k] + dist[k][j] < dist[i][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }
    
    // Check for negative cycles
    for (int i = 0; i < V; i++) {
        if (dist[i][i] < 0) {
            System.out.println("Negative cycle detected");
            return;
        }
    }
}
```

## Complexity

- Time: O(V³)
- Space: O(V²)

## When to Use

- Need **all pairs** shortest paths (not just single source)
- Graph is **dense** (E ≈ V²)
- V ≤ 400 (V³ must be feasible)

## Path Reconstruction

```java
int[][] next;  // next[i][j] = next vertex after i on path to j

void initNext(int V) {
    next = new int[V][V];
    for (int i = 0; i < V; i++) {
        for (int j = 0; j < V; j++) {
            if (graph[i][j] != INF) next[i][j] = j;
            else next[i][j] = -1;
        }
    }
}

List<Integer> getPath(int i, int j) {
    if (next[i][j] == -1) return null;
    List<Integer> path = new ArrayList<>();
    path.add(i);
    while (i != j) {
        i = next[i][j];
        path.add(i);
    }
    return path;
}
```

## Use Cases

1. City-to-city shortest routes (small map)
2. Detecting reachability (transitive closure)
3. Finding diameter of graph
4. Smallest maximum edge on path (minimax path)
