# Prim's Algorithm

## Overview

Grows MST from a starting vertex, always adding the **minimum weight edge** connecting visited to unvisited vertices.

```java
class Edge { int to, weight; Edge(int t, int w) { to = t; weight = w; } }

int primMST(List<List<Edge>> graph, int V) {
    boolean[] visited = new boolean[V];
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    // [vertex, minWeightToReach]
    
    pq.offer(new int[]{0, 0});
    int mstWeight = 0;
    int edgesInMST = 0;
    
    while (!pq.isEmpty() && edgesInMST < V) {
        int[] curr = pq.poll();
        int u = curr[0], w = curr[1];
        
        if (visited[u]) continue;
        
        visited[u] = true;
        mstWeight += w;
        edgesInMST++;
        
        for (Edge e : graph.get(u)) {
            if (!visited[e.to]) {
                pq.offer(new int[]{e.to, e.weight});
            }
        }
    }
    
    return mstWeight;
}
```

## Complexity

- O((V+E) log V) with binary heap
- O(V²) with array (dense graphs)

## Kruskal vs Prim

| Feature | Kruskal | Prim |
|---------|---------|------|
| Approach | Edge-based | Vertex-based |
| Data Structure | Edge list + DSU | Adjacency list + Heap |
| Best for | Sparse graphs | Dense graphs |
| Time | O(E log E) | O((V+E) log V) |
