# Articulation Points & Bridges

## Articulation Points (Cut Vertices)

A vertex whose removal disconnects the graph.

### Tarjan's Algorithm
```java
List<Integer> findArticulationPoints(List<List<Integer>> graph, int V) {
    boolean[] visited = new boolean[V];
    int[] disc = new int[V];    // discovery time
    int[] low = new int[V];     // lowest discovery reachable
    int[] parent = new int[V];
    boolean[] ap = new boolean[V];
    
    Arrays.fill(parent, -1);
    int[] time = new int[1];  // wrapper for mutable int
    
    for (int i = 0; i < V; i++) {
        if (!visited[i]) dfsAP(i, graph, visited, disc, low, parent, ap, time);
    }
    
    List<Integer> result = new ArrayList<>();
    for (int i = 0; i < V; i++) if (ap[i]) result.add(i);
    return result;
}

void dfsAP(int u, List<List<Integer>> graph, boolean[] visited, int[] disc, 
           int[] low, int[] parent, boolean[] ap, int[] time) {
    visited[u] = true;
    disc[u] = low[u] = ++time[0];
    int children = 0;
    
    for (int v : graph.get(u)) {
        if (!visited[v]) {
            children++;
            parent[v] = u;
            dfsAP(v, graph, visited, disc, low, parent, ap, time);
            
            low[u] = Math.min(low[u], low[v]);
            
            // Case 1: root with 2+ children
            if (parent[u] == -1 && children > 1) ap[u] = true;
            // Case 2: non-root, no back edge from subtree
            if (parent[u] != -1 && low[v] >= disc[u]) ap[u] = true;
        } else if (v != parent[u]) {
            low[u] = Math.min(low[u], disc[v]);  // back edge
        }
    }
}
```

## Bridges (Cut Edges)

An edge whose removal disconnects the graph.

```java
List<int[]> findBridges(List<List<Integer>> graph, int V) {
    boolean[] visited = new boolean[V];
    int[] disc = new int[V];
    int[] low = new int[V];
    int[] parent = new int[V];
    List<int[]> bridges = new ArrayList<>();
    
    Arrays.fill(parent, -1);
    int[] time = new int[1];
    
    for (int i = 0; i < V; i++) {
        if (!visited[i]) dfsBridge(i, graph, visited, disc, low, parent, bridges, time);
    }
    return bridges;
}

void dfsBridge(int u, List<List<Integer>> graph, boolean[] visited, int[] disc,
               int[] low, int[] parent, List<int[]> bridges, int[] time) {
    visited[u] = true;
    disc[u] = low[u] = ++time[0];
    
    for (int v : graph.get(u)) {
        if (!visited[v]) {
            parent[v] = u;
            dfsBridge(v, graph, visited, disc, low, parent, bridges, time);
            
            low[u] = Math.min(low[u], low[v]);
            
            // Bridge condition: low[v] > disc[u]
            if (low[v] > disc[u]) {
                bridges.add(new int[]{u, v});
            }
        } else if (v != parent[u]) {
            low[u] = Math.min(low[u], disc[v]);
        }
    }
}
```

## Key Difference

| Concept | Condition | Meaning |
|---------|-----------|---------|
| Articulation Point | low[v] >= disc[u] | No back edge from child to ancestor |
| Bridge | low[v] > disc[u] | No back edge from child (strictly greater) |
| Root AP | ≥2 children | Root needs special handling |
