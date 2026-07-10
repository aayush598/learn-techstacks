# Edge List Representation

## What is an Edge List?

An edge list is the simplest graph representation: just a list of all edges. Each edge stores its endpoints (and optionally a weight). No fancy data structures needed.

```
Graph:           Edge List:
  0---1          [(0,1), (0,2), (1,2), (1,3), (2,3)]
  |\  |
  | \ |
  2---3
```

## Basic Implementation

```java
import java.util.*;

class Edge {
    int src, dest, weight;

    Edge(int src, int dest) {
        this.src = src;
        this.dest = dest;
        this.weight = 1;
    }

    Edge(int src, int dest, int weight) {
        this.src = src;
        this.dest = dest;
        this.weight = weight;
    }

    @Override
    public String toString() {
        return src + " -> " + dest + " (w=" + weight + ")";
    }
}

class EdgeListGraph {
    private List<Edge> edges;
    private int numVertices;

    public EdgeListGraph(int numVertices) {
        this.numVertices = numVertices;
        this.edges = new ArrayList<>();
    }

    // Add edge — O(1)
    public void addEdge(int src, int dest) {
        addEdge(src, dest, 1);
    }

    public void addEdge(int src, int dest, int weight) {
        edges.add(new Edge(src, dest, weight));
    }

    // Remove edge — O(E)
    public void removeEdge(int src, int dest) {
        edges.removeIf(e -> e.src == src && e.dest == dest);
    }

    // Check if edge exists — O(E)
    public boolean hasEdge(int src, int dest) {
        return edges.stream().anyMatch(e -> e.src == src && e.dest == dest);
    }

    // Get all edges — O(1)
    public List<Edge> getEdges() {
        return edges;
    }

    // Get all edges sorted by weight — O(E log E)
    public List<Edge> getEdgesSortedByWeight() {
        List<Edge> sorted = new ArrayList<>(edges);
        sorted.sort(Comparator.comparingInt(e -> e.weight));
        return sorted;
    }

    // Get number of edges
    public int edgeCount() {
        return edges.size();
    }

    // Get vertices as array
    public int[] getVertices() {
        return new java.util.Random().ints(0, numVertices)
            .distinct().limit(numVertices).toArray();
    }

    // Print all edges
    public void print() {
        for (Edge edge : edges) {
            System.out.println(edge);
        }
    }
}
```

## Converting Edge List to Adjacency List

```java
class EdgeListConverter {

    // Edge list → Adjacency list
    public static List<List<int[]>> toAdjacencyList(
            int numVertices, int[][] edges, boolean directed) {

        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < numVertices; i++) {
            adj.add(new ArrayList<>());
        }

        for (int[] edge : edges) {
            int u = edge[0], v = edge[1];
            int w = edge.length > 2 ? edge[2] : 1;

            adj.get(u).add(new int[]{v, w});
            if (!directed) {
                adj.get(v).add(new int[]{u, w});
            }
        }

        return adj;
    }

    // Edge list → Adjacency matrix
    public static int[][] toAdjacencyMatrix(
            int numVertices, int[][] edges, boolean directed) {

        int[][] matrix = new int[numVertices][numVertices];

        for (int[] edge : edges) {
            int u = edge[0], v = edge[1];
            int w = edge.length > 2 ? edge[2] : 1;

            matrix[u][v] = w;
            if (!directed) {
                matrix[v][u] = w;
            }
        }

        return matrix;
    }
}
```

## When to Use Edge List

**Good for:**
- Kruskal's MST algorithm (sort edges by weight)
- Bellman-Ford algorithm (iterate all edges V-1 times)
- When you need to process edges globally
- Simple problems where you just need to iterate edges

**Bad for:**
- Neighbor queries: O(E) per query
- BFS/DFS: Need to find neighbors efficiently
- Dense graphs

## Kruskal's Algorithm with Edge List

```java
class KruskalWithEdgeList {

    // Find MST weight using edge list
    public static int mstWeight(int numVertices, List<Edge> edges) {
        // Sort edges by weight
        edges.sort(Comparator.comparingInt(e -> e.weight));

        int[] parent = new int[numVertices];
        int[] rank = new int[numVertices];
        for (int i = 0; i < numVertices; i++) parent[i] = i;

        int mstWeight = 0;
        int edgesUsed = 0;

        for (Edge edge : edges) {
            int rootSrc = find(parent, edge.src);
            int rootDest = find(parent, edge.dest);

            if (rootSrc != rootDest) {
                mstWeight += edge.weight;
                edgesUsed++;

                // Union by rank
                if (rank[rootSrc] < rank[rootDest]) {
                    parent[rootSrc] = rootDest;
                } else if (rank[rootSrc] > rank[rootDest]) {
                    parent[rootDest] = rootSrc;
                } else {
                    parent[rootDest] = rootSrc;
                    rank[rootSrc]++;
                }

                if (edgesUsed == numVertices - 1) break;
            }
        }

        return edgesUsed == numVertices - 1 ? mstWeight : -1;
    }

    private static int find(int[] parent, int x) {
        if (parent[x] != x) {
            parent[x] = find(parent, parent[x]); // path compression
        }
        return parent[x];
    }
}
```

## Bellman-Ford with Edge List

```java
class BellmanFordWithEdgeList {

    // Find shortest paths from source
    // Returns null if negative cycle exists
    public static int[] shortestPaths(int numVertices, int[][] edges, int source) {
        int[] dist = new int[numVertices];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[source] = 0;

        // Relax all edges V-1 times
        for (int i = 0; i < numVertices - 1; i++) {
            for (int[] edge : edges) {
                int u = edge[0], v = edge[1], w = edge[2];
                if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                }
            }
        }

        // Check for negative cycle
        for (int[] edge : edges) {
            int u = edge[0], v = edge[1], w = edge[2];
            if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) {
                return null; // negative cycle detected
            }
        }

        return dist;
    }
}
```

## Complexity Summary

| Operation | Time |
|-----------|------|
| Add edge | O(1) |
| Remove edge | O(E) |
| Check edge | O(E) |
| Get all neighbors of vertex | O(E) |
| Sort edges by weight | O(E log E) |
| Space | O(E) |

Edge list is the simplest representation but least efficient for most operations. Use it when your algorithm naturally processes edges globally (Kruskal, Bellman-Ford).
