# Max Flow / Min Cut

## Overview

**Max Flow**: Maximum amount of flow from source to sink in a flow network.
**Min Cut**: Minimum total capacity of edges to disconnect source from sink.
**Max-Flow Min-Cut Theorem**: Max flow = Min cut capacity.

## Ford-Fulkerson Algorithm (Edmonds-Karp variant)

Uses BFS to find augmenting paths:

```java
class Edge {
    int to, rev;  // rev = index of reverse edge in adjacency list of 'to'
    int capacity;
    Edge(int t, int r, int c) { to = t; rev = r; capacity = c; }
}

class MaxFlow {
    List<List<Edge>> graph;
    int[] level, iter;
    
    MaxFlow(int n) {
        graph = new ArrayList<>();
        for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
        level = new int[n];
        iter = new int[n];
    }
    
    void addEdge(int from, int to, int capacity) {
        graph.get(from).add(new Edge(to, graph.get(to).size(), capacity));
        graph.get(to).add(new Edge(from, graph.get(from).size() - 1, 0));  // reverse
    }
    
    // BFS to build level graph
    void bfs(int s) {
        Arrays.fill(level, -1);
        Queue<Integer> q = new LinkedList<>();
        level[s] = 0;
        q.offer(s);
        while (!q.isEmpty()) {
            int v = q.poll();
            for (Edge e : graph.get(v)) {
                if (e.capacity > 0 && level[e.to] < 0) {
                    level[e.to] = level[v] + 1;
                    q.offer(e.to);
                }
            }
        }
    }
    
    // DFS to find augmenting path
    int dfs(int v, int t, int f) {
        if (v == t) return f;
        for (; iter[v] < graph.get(v).size(); iter[v]++) {
            Edge e = graph.get(v).get(iter[v]);
            if (e.capacity > 0 && level[v] < level[e.to]) {
                int d = dfs(e.to, t, Math.min(f, e.capacity));
                if (d > 0) {
                    e.capacity -= d;
                    graph.get(e.to).get(e.rev).capacity += d;
                    return d;
                }
            }
        }
        return 0;
    }
    
    int maxFlow(int s, int t) {
        int flow = 0, INF = Integer.MAX_VALUE;
        while (true) {
            bfs(s);
            if (level[t] < 0) return flow;
            Arrays.fill(iter, 0);
            int f;
            while ((f = dfs(s, t, INF)) > 0) flow += f;
        }
    }
}
```

## Applications

1. **Bipartite Matching**: Add source→left, left→right, right→sink edges (capacity 1)
2. **Edge-Disjoint Paths**: All edges capacity 1, max flow = max disjoint paths
3. **Minimum Cut**: Remove minimum edges to separate source from sink
4. **Circulation**: Feasible flow with demands
