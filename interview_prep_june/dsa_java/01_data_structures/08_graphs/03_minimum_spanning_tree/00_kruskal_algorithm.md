# Kruskal's Algorithm

## Overview

Finds **Minimum Spanning Tree** (MST) by processing edges in ascending weight order, adding only those that don't form cycles.

## Algorithm

```java
class Edge implements Comparable<Edge> {
    int src, dest, weight;
    Edge(int s, int d, int w) { src = s; dest = d; weight = w; }
    public int compareTo(Edge other) { return this.weight - other.weight; }
}

List<Edge> kruskalMST(List<Edge> edges, int V) {
    // Step 1: Sort edges by weight
    Collections.sort(edges);
    
    // Step 2: Initialize DSU
    int[] parent = new int[V];
    int[] rank = new int[V];
    for (int i = 0; i < V; i++) parent[i] = i;
    
    List<Edge> mst = new ArrayList<>();
    int mstWeight = 0;
    
    // Step 3: Process edges
    for (Edge e : edges) {
        int rootSrc = find(parent, e.src);
        int rootDest = find(parent, e.dest);
        
        if (rootSrc != rootDest) {  // No cycle
            union(parent, rank, rootSrc, rootDest);
            mst.add(e);
            mstWeight += e.weight;
        }
    }
    
    return mst;  // or mstWeight
}

int find(int[] parent, int x) {
    if (parent[x] != x) parent[x] = find(parent, parent[x]);
    return parent[x];
}

void union(int[] parent, int[] rank, int x, int y) {
    if (rank[x] < rank[y]) parent[x] = y;
    else if (rank[x] > rank[y]) parent[y] = x;
    else { parent[y] = x; rank[x]++; }
}
```

## Complexity

- O(E log E) for sorting
- O(E α(V)) for DSU operations
- Total: O(E log E) ≈ O(E log V)

## Key Properties

- **Greedy**: always picks smallest weight edge
- **Works on edge list** — good for sparse graphs
- Uses Union-Find for cycle detection
- Produces MST (minimum total weight connecting all vertices)
