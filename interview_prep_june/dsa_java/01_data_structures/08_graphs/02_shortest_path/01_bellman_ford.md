# Bellman-Ford Algorithm

## Overview

Finds shortest paths from source when **negative weights exist**. Also detects **negative cycles**.

## Key Idea

Relax all edges V-1 times. After V-1 iterations, we have shortest paths. One more iteration: if any distance still decreases → negative cycle.

## Implementation

```java
class Edge { int src, dest, weight; }

int[] bellmanFord(List<Edge> edges, int V, int source) {
    int[] dist = new int[V];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[source] = 0;
    
    // Relax all edges V-1 times
    for (int i = 0; i < V - 1; i++) {
        for (Edge e : edges) {
            if (dist[e.src] != Integer.MAX_VALUE && 
                dist[e.src] + e.weight < dist[e.dest]) {
                dist[e.dest] = dist[e.src] + e.weight;
            }
        }
    }
    
    // Check for negative cycle
    for (Edge e : edges) {
        if (dist[e.src] != Integer.MAX_VALUE && 
            dist[e.src] + e.weight < dist[e.dest]) {
            throw new RuntimeException("Graph contains negative cycle");
        }
    }
    
    return dist;
}
```

## Complexity

- Time: O(V × E)
- Space: O(V)

## When to Use

- Graph has **negative weights**
- Need to detect **negative cycles**
- V is small (E up to ~10⁴)

## Dijkstra vs Bellman-Ford

| Feature | Dijkstra | Bellman-Ford |
|---------|----------|--------------|
| Negative weights | No | Yes |
| Negative cycle detection | No | Yes |
| Time | O((V+E) log V) | O(V·E) |
| Greedy | Yes | No (DP) |
