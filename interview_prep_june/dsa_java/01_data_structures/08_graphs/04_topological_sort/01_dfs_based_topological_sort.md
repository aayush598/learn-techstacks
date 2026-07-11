# DFS-based Topological Sort

## Overview

Use DFS to find a post-order. When DFS finishes processing all neighbors of a node, add it to stack. Pop stack for topological order.

```java
int[] topologicalSortDFS(List<List<Integer>> graph, int V) {
    boolean[] visited = new boolean[V];
    boolean[] inStack = new boolean[V];  // for cycle detection
    Stack<Integer> stack = new Stack<>();
    
    for (int i = 0; i < V; i++) {
        if (!visited[i]) {
            if (dfs(i, graph, visited, inStack, stack)) {
                throw new RuntimeException("Graph has a cycle");
            }
        }
    }
    
    int[] result = new int[V];
    for (int i = 0; i < V; i++) result[i] = stack.pop();
    return result;
}

// Returns true if cycle detected
boolean dfs(int u, List<List<Integer>> graph, boolean[] visited, 
            boolean[] inStack, Stack<Integer> stack) {
    if (inStack[u]) return true;  // cycle
    if (visited[u]) return false;
    
    visited[u] = true;
    inStack[u] = true;
    
    for (int v : graph.get(u)) {
        if (dfs(v, graph, visited, inStack, stack)) return true;
    }
    
    inStack[u] = false;
    stack.push(u);
    return false;
}
```

## Cycle Detection with 3 States

```java
static final int UNVISITED = 0;
static final int VISITING = 1;
static final int VISITED = 2;

boolean hasCycle(List<List<Integer>> graph, int V) {
    int[] state = new int[V];
    
    for (int i = 0; i < V; i++) {
        if (state[i] == UNVISITED) {
            if (dfs(i, graph, state)) return true;
        }
    }
    return false;
}

boolean dfs(int u, List<List<Integer>> graph, int[] state) {
    state[u] = VISITING;
    
    for (int v : graph.get(u)) {
        if (state[v] == VISITING) return true;  // back edge → cycle
        if (state[v] == UNVISITED) {
            if (dfs(v, graph, state)) return true;
        }
    }
    
    state[u] = VISITED;
    return false;
}
```

## Kahn's vs DFS Topological Sort

| Feature | Kahn's (BFS) | DFS |
|---------|-------------|-----|
| Approach | In-degree tracking | Post-order traversal |
| Cycle detection | Check if result size == V | Back edge detection |
| Output order | Natural (dependency first) | Reverse of finish time |
| Queue/Stack | Queue | Stack |
| Code complexity | Simple | Slightly more complex |
