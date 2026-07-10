# Adjacency List Representation

## What is an Adjacency List?

An adjacency list stores the graph as an array of lists, where each list contains the neighbors (and optionally edge weights) of a vertex. This is the **most commonly used** graph representation in coding interviews.

```
Graph:           Adjacency List:
  0---1          0: [1, 2]
  |\  |          1: [0, 2, 3]
  | \ |          2: [0, 1, 3]
  2---3          3: [1, 2]
```

## Unweighted Graph

```java
import java.util.*;

class AdjacencyListGraph {
    private List<List<Integer>> adj;
    private int numVertices;
    private boolean directed;

    public AdjacencyListGraph(int numVertices, boolean directed) {
        this.numVertices = numVertices;
        this.directed = directed;
        this.adj = new ArrayList<>();

        for (int i = 0; i < numVertices; i++) {
            adj.add(new ArrayList<>());
        }
    }

    // Add edge — O(1)
    public void addEdge(int from, int to) {
        adj.get(from).add(to);
        if (!directed) {
            adj.get(to).add(from);
        }
    }

    // Remove edge — O(degree)
    public void removeEdge(int from, int to) {
        adj.get(from).remove(Integer.valueOf(to));
        if (!directed) {
            adj.get(to).remove(Integer.valueOf(from));
        }
    }

    // Check if edge exists — O(degree)
    public boolean hasEdge(int from, int to) {
        return adj.get(from).contains(to);
    }

    // Get neighbors — O(1)
    public List<Integer> getNeighbors(int vertex) {
        return adj.get(vertex);
    }

    // Get degree of vertex — O(1)
    public int getDegree(int vertex) {
        return adj.get(vertex).size();
    }

    // Print graph
    public void print() {
        for (int i = 0; i < numVertices; i++) {
            System.out.println(i + " -> " + adj.get(i));
        }
    }
}
```

## Weighted Graph

```java
class WeightedAdjacencyList {
    // Each entry: [neighbor, weight]
    private List<List<int[]>> adj;
    private int numVertices;
    private boolean directed;

    public WeightedAdjacencyList(int numVertices, boolean directed) {
        this.numVertices = numVertices;
        this.directed = directed;
        this.adj = new ArrayList<>();

        for (int i = 0; i < numVertices; i++) {
            adj.add(new ArrayList<>());
        }
    }

    public void addEdge(int from, int to, int weight) {
        adj.get(from).add(new int[]{to, weight});
        if (!directed) {
            adj.get(to).add(new int[]{from, weight});
        }
    }

    public void removeEdge(int from, int to) {
        adj.get(from).removeIf(edge -> edge[0] == to);
        if (!directed) {
            adj.get(to).removeIf(edge -> edge[0] == from);
        }
    }

    public boolean hasEdge(int from, int to) {
        return adj.get(from).stream().anyMatch(e -> e[0] == to);
    }

    // Get neighbors with weights
    public List<int[]> getNeighbors(int vertex) {
        return adj.get(vertex);
    }

    // Get weight of specific edge
    public int getWeight(int from, int to) {
        for (int[] edge : adj.get(from)) {
            if (edge[0] == to) return edge[1];
        }
        return -1; // edge doesn't exist
    }

    public void print() {
        for (int i = 0; i < numVertices; i++) {
            System.out.print(i + " -> ");
            for (int[] edge : adj.get(i)) {
                System.out.printf("(%d, w=%d) ", edge[0], edge[1]);
            }
            System.out.println();
        }
    }
}
```

## Building Graph from Edge List

```java
class GraphBuilder {

    // Build unweighted graph from edge list
    public static AdjacencyListGraph fromEdgeList(
            int numVertices, int[][] edges, boolean directed) {

        AdjacencyListGraph graph = new AdjacencyListGraph(numVertices, directed);

        for (int[] edge : edges) {
            graph.addEdge(edge[0], edge[1]);
        }

        return graph;
    }

    // Build weighted graph from edge list
    public static WeightedAdjacencyList weightedFromEdgeList(
            int numVertices, int[][] edges, boolean directed) {

        WeightedAdjacencyList graph = new WeightedAdjacencyList(numVertices, directed);

        for (int[] edge : edges) {
            graph.addEdge(edge[0], edge[1], edge[2]);
        }

        return graph;
    }
}
```

## Space Complexity

| Type | Space | Notes |
|------|-------|-------|
| Unweighted | O(V + E) | Each edge stored twice (undirected) |
| Weighted | O(V + E) | Each edge stores neighbor + weight |

## When to Use Adjacency List

**Good for:**
- Sparse graphs (most real-world graphs)
- Iterating neighbors efficiently: O(degree)
- BFS/DFS traversals
- Most graph algorithms

**Bad for:**
- Checking if specific edge exists: O(degree) vs O(1) for matrix
- Dense graphs (E close to V²)

## Adjacency List vs Matrix

| Operation | List | Matrix |
|-----------|------|--------|
| Space | O(V+E) | O(V²) |
| Add edge | O(1) | O(1) |
| Remove edge | O(E) worst | O(1) |
| Check edge | O(degree) | O(1) |
| Get all neighbors | O(degree) | O(V) |
| Get degree | O(1) | O(V) |
| Best for | Sparse | Dense |

**Default choice**: Use adjacency list unless you specifically need O(1) edge checks or the graph is very dense.
