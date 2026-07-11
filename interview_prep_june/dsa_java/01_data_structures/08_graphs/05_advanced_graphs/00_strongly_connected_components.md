# Strongly Connected Components (SCC)

## Overview

In a **directed graph**, SCC is a maximal set of vertices where every vertex is reachable from every other vertex.

## Kosaraju's Algorithm (Two DFS Passes)

```java
List<List<Integer>> kosarajuSCC(List<List<Integer>> graph, int V) {
    // Step 1: DFS on original graph → stack by finish time
    boolean[] visited = new boolean[V];
    Stack<Integer> stack = new Stack<>();
    
    for (int i = 0; i < V; i++) {
        if (!visited[i]) dfs(i, graph, visited, stack);
    }
    
    // Step 2: Reverse graph
    List<List<Integer>> reverse = new ArrayList<>();
    for (int i = 0; i < V; i++) reverse.add(new ArrayList<>());
    for (int u = 0; u < V; u++) {
        for (int v : graph.get(u)) reverse.get(v).add(u);
    }
    
    // Step 3: DFS on reverse graph in stack order
    visited = new boolean[V];
    List<List<Integer>> sccs = new ArrayList<>();
    
    while (!stack.isEmpty()) {
        int v = stack.pop();
        if (!visited[v]) {
            List<Integer> component = new ArrayList<>();
            dfsCollect(v, reverse, visited, component);
            sccs.add(component);
        }
    }
    
    return sccs;
}

void dfs(int u, List<List<Integer>> graph, boolean[] visited, Stack<Integer> stack) {
    visited[u] = true;
    for (int v : graph.get(u)) {
        if (!visited[v]) dfs(v, graph, visited, stack);
    }
    stack.push(u);  // post-order
}

void dfsCollect(int u, List<List<Integer>> graph, boolean[] visited, List<Integer> comp) {
    visited[u] = true;
    comp.add(u);
    for (int v : graph.get(u)) {
        if (!visited[v]) dfsCollect(v, graph, visited, comp);
    }
}
```

## Applications

1. **Condensation Graph**: Compress SCCs into DAG nodes
2. **2-SAT**: Boolean satisfiability with 2 variables per clause
3. **Kosaraju vs Tarjan**: Both O(V+E), Tarjan uses only one DFS
