# Shortest Path in DAG

## Overview

In a Directed Acyclic Graph (DAG), we can find shortest paths from source in O(V+E) — **faster than Dijkstra**.

## Algorithm

1. Get topological order of DAG
2. Process vertices in order, relax outgoing edges

```java
int[] shortestPathDAG(List<List<int[]>> graph, int V, int source) {
    // Step 1: Topological sort
    int[] topo = topologicalSort(graph, V);
    
    // Step 2: Initialize distances
    int[] dist = new int[V];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[source] = 0;
    
    // Step 3: Process in topological order
    for (int u : topo) {
        if (dist[u] != Integer.MAX_VALUE) {
            for (int[] edge : graph.get(u)) {
                int v = edge[0], w = edge[1];
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                }
            }
        }
    }
    
    return dist;
}

int[] topologicalSort(List<List<int[]>> graph, int V) {
    int[] inDegree = new int[V];
    for (int u = 0; u < V; u++) {
        for (int[] edge : graph.get(u)) {
            inDegree[edge[0]]++;
        }
    }
    
    Queue<Integer> q = new LinkedList<>();
    for (int i = 0; i < V; i++) {
        if (inDegree[i] == 0) q.offer(i);
    }
    
    int[] topo = new int[V];
    int idx = 0;
    
    while (!q.isEmpty()) {
        int u = q.poll();
        topo[idx++] = u;
        for (int[] edge : graph.get(u)) {
            if (--inDegree[edge[0]] == 0) q.offer(edge[0]);
        }
    }
    
    return topo;
}
```

## Key Advantages

- **O(V+E)** — faster than Dijkstra
- Works with **negative weights** (as long as no cycles)
- No cycle detection needed (DAG guaranteed)

## Longest Path in DAG

Same approach but negate weights or use max instead of min:
```java
// For longest path: initialize dist = -INF, reverse comparison
if (dist[u] + w > dist[v]) dist[v] = dist[u] + w;
```

This is how we solve **Critical Path Method (CPM)** problems.
