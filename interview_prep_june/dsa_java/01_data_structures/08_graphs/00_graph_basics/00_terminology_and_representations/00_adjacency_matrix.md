# Adjacency Matrix Representation

## What is an Adjacency Matrix?

An adjacency matrix is a 2D array where `matrix[i][j]` indicates whether there's an edge from vertex `i` to vertex `j`. It's one of the simplest ways to represent a graph.

```
Graph:       Matrix:
  0---1       [0, 1, 0, 0]
  |\  |       [1, 0, 1, 1]
  | \ |       [0, 1, 0, 1]
  2---3       [0, 1, 1, 0]
```

## Basic Implementation

```java
class AdjacencyMatrixGraph {
    private int[][] matrix;
    private int numVertices;
    private boolean directed;

    public AdjacencyMatrixGraph(int numVertices, boolean directed) {
        this.numVertices = numVertices;
        this.directed = directed;
        this.matrix = new int[numVertices][numVertices];
    }

    // Add edge (weighted, default weight = 1)
    public void addEdge(int from, int to) {
        addEdge(from, to, 1);
    }

    public void addEdge(int from, int to, int weight) {
        matrix[from][to] = weight;
        if (!directed) {
            matrix[to][from] = weight; // undirected: both directions
        }
    }

    // Remove edge
    public void removeEdge(int from, int to) {
        matrix[from][to] = 0;
        if (!directed) {
            matrix[to][from] = 0;
        }
    }

    // Check if edge exists — O(1)
    public boolean hasEdge(int from, int to) {
        return matrix[from][to] != 0;
    }

    // Get weight of edge
    public int getWeight(int from, int to) {
        return matrix[from][to];
    }

    // Get all neighbors of a vertex — O(V)
    public java.util.List<Integer> getNeighbors(int vertex) {
        java.util.List<Integer> neighbors = new java.util.ArrayList<>();
        for (int i = 0; i < numVertices; i++) {
            if (matrix[vertex][i] != 0) {
                neighbors.add(i);
            }
        }
        return neighbors;
    }

    // Count edges
    public int edgeCount() {
        int count = 0;
        for (int i = 0; i < numVertices; i++) {
            for (int j = 0; j < numVertices; j++) {
                if (matrix[i][j] != 0) {
                    count++;
                }
            }
        }
        return directed ? count : count / 2;
    }

    // Print the matrix
    public void print() {
        System.out.print("  ");
        for (int i = 0; i < numVertices; i++) {
            System.out.printf("%3d", i);
        }
        System.out.println();

        for (int i = 0; i < numVertices; i++) {
            System.out.printf("%d ", i);
            for (int j = 0; j < numVertices; j++) {
                System.out.printf("%3d", matrix[i][j]);
            }
            System.out.println();
        }
    }
}
```

## Weighted Graph Variant

```java
class WeightedAdjacencyMatrix {
    private double[][] matrix;
    private int numVertices;
    public static final double INF = Double.POSITIVE_INFINITY;

    public WeightedAdjacencyMatrix(int numVertices) {
        this.numVertices = numVertices;
        this.matrix = new double[numVertices][numVertices];

        // Initialize with infinity (no edge)
        for (int i = 0; i < numVertices; i++) {
            for (int j = 0; j < numVertices; j++) {
                matrix[i][j] = INF;
            }
            matrix[i][i] = 0; // self-loop weight = 0
        }
    }

    public void addEdge(int from, int to, double weight) {
        matrix[from][to] = weight;
        matrix[to][from] = weight; // undirected
    }

    public double getWeight(int from, int to) {
        return matrix[from][to];
    }

    public boolean hasEdge(int from, int to) {
        return matrix[from][to] != INF;
    }

    public java.util.List<Integer> getNeighbors(int vertex) {
        java.util.List<Integer> neighbors = new java.util.ArrayList<>();
        for (int i = 0; i < numVertices; i++) {
            if (matrix[vertex][i] != INF && i != vertex) {
                neighbors.add(i);
            }
        }
        return neighbors;
    }
}
```

## Adjacency Matrix for Floyd-Warshall

The matrix naturally fits Floyd-Warshall (all-pairs shortest path):

```java
class FloydWarshall {
    public static double[][] shortestPaths(double[][] graph) {
        int n = graph.length;
        double[][] dist = new double[n][n];

        // Initialize distance matrix
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                dist[i][j] = graph[i][j];
            }
        }

        // Floyd-Warshall: try each vertex as intermediate
        for (int k = 0; k < n; k++) {
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if (dist[i][k] + dist[k][j] < dist[i][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                    }
                }
            }
        }

        return dist;
    }
}
```

## Space Complexity Analysis

| Type | Space | Notes |
|------|-------|-------|
| Unweighted | O(V²) | Store 0 or 1 |
| Weighted | O(V²) | Store weight or INF |
| Dense graph (E ≈ V²) | O(V²) | Efficient |
| Sparse graph (E << V²) | O(V²) | Wasteful |

## When to Use Adjacency Matrix

**Good for:**
- Dense graphs (many edges)
- Floyd-Warshall (all-pairs shortest path)
- Checking if edge exists: O(1)
- Small graphs (V ≤ 1000)

**Bad for:**
- Sparse graphs (wastes space)
- Iterating neighbors: O(V) vs O(degree) in adjacency list
- Memory: V² integers even if few edges

## Comparison with Adjacency List

| Operation | Matrix | List |
|-----------|--------|------|
| Space | O(V²) | O(V + E) |
| Add edge | O(1) | O(1) |
| Remove edge | O(1) | O(E) |
| Check edge | O(1) | O(degree) |
| Get neighbors | O(V) | O(degree) |
| Best for | Dense | Sparse |
