# Complete Graph Implementation

## A Reusable Graph Class

Here's a complete, production-ready graph class that supports both directed/undirected and weighted/unweighted graphs.

```java
import java.util.*;

class Graph {
    private int numVertices;
    private boolean directed;
    private boolean weighted;
    private List<List<int[]>> adj; // [neighbor, weight]
    private Set<Integer> vertices;

    public Graph(int numVertices, boolean directed, boolean weighted) {
        this.numVertices = numVertices;
        this.directed = directed;
        this.weighted = weighted;
        this.vertices = new HashSet<>();

        adj = new ArrayList<>();
        for (int i = 0; i < numVertices; i++) {
            adj.add(new ArrayList<>());
            vertices.add(i);
        }
    }

    // Convenience constructors
    public Graph(int numVertices, boolean directed) {
        this(numVertices, directed, false);
    }

    public Graph(int numVertices) {
        this(numVertices, false, false);
    }

    // Add vertex (for dynamic graphs)
    public int addVertex() {
        int newVertex = numVertices++;
        adj.add(new ArrayList<>());
        vertices.add(newVertex);
        return newVertex;
    }

    // Add edge
    public void addEdge(int from, int to) {
        addEdge(from, to, 1);
    }

    public void addEdge(int from, int to, int weight) {
        adj.get(from).add(new int[]{to, weight});
        if (!directed) {
            adj.get(to).add(new int[]{from, weight});
        }
    }

    // Remove edge
    public void removeEdge(int from, int to) {
        adj.get(from).removeIf(e -> e[0] == to);
        if (!directed) {
            adj.get(to).removeIf(e -> e[0] == from);
        }
    }

    // Check edge existence
    public boolean hasEdge(int from, int to) {
        return adj.get(from).stream().anyMatch(e -> e[0] == to);
    }

    // Get neighbors (unweighted)
    public List<Integer> getNeighbors(int vertex) {
        List<Integer> neighbors = new ArrayList<>();
        for (int[] edge : adj.get(vertex)) {
            neighbors.add(edge[0]);
        }
        return neighbors;
    }

    // Get neighbors with weights
    public List<int[]> getNeighborsWithWeight(int vertex) {
        return adj.get(vertex);
    }

    // Get degree
    public int getDegree(int vertex) {
        return adj.get(vertex).size();
    }

    // Get all vertices
    public Set<Integer> getVertices() {
        return vertices;
    }

    // Get number of vertices
    public int getNumVertices() {
        return numVertices;
    }

    // Get number of edges
    public int getNumEdges() {
        int count = 0;
        for (int i = 0; i < numVertices; i++) {
            count += adj.get(i).size();
        }
        return directed ? count : count / 2;
    }

    // Build from edge list
    public static Graph fromEdgeList(int numVertices, int[][] edges, boolean directed) {
        Graph graph = new Graph(numVertices, directed);
        for (int[] edge : edges) {
            graph.addEdge(edge[0], edge[1]);
        }
        return graph;
    }

    // Build weighted graph from edge list
    public static Graph weightedFromEdgeList(int numVertices, int[][] edges, boolean directed) {
        Graph graph = new Graph(numVertices, directed, true);
        for (int[] edge : edges) {
            graph.addEdge(edge[0], edge[1], edge[2]);
        }
        return graph;
    }

    // Get transpose (reverse all edges)
    public Graph getTranspose() {
        Graph transpose = new Graph(numVertices, directed, weighted);
        for (int u = 0; u < numVertices; u++) {
            for (int[] edge : adj.get(u)) {
                int v = edge[0], w = edge[1];
                transpose.addEdge(v, u, w);
            }
        }
        return transpose;
    }

    // Print adjacency list
    public void print() {
        for (int i = 0; i < numVertices; i++) {
            StringBuilder sb = new StringBuilder();
            sb.append(i).append(" -> ");
            for (int j = 0; j < adj.get(i).size(); j++) {
                int[] edge = adj.get(i).get(j);
                if (weighted) {
                    sb.append(String.format("(%d, w=%d)", edge[0], edge[1]));
                } else {
                    sb.append(edge[0]);
                }
                if (j < adj.get(i).size() - 1) sb.append(", ");
            }
            System.out.println(sb);
        }
    }
}
```

## Usage Examples

```java
class GraphDemo {
    public static void main(String[] args) {
        // Example 1: Simple undirected graph
        System.out.println("=== Undirected Graph ===");
        Graph g1 = new Graph(5);
        g1.addEdge(0, 1);
        g1.addEdge(0, 4);
        g1.addEdge(1, 2);
        g1.addEdge(1, 3);
        g1.addEdge(1, 4);
        g1.addEdge(2, 3);
        g1.addEdge(3, 4);
        g1.print();

        // Example 2: Weighted directed graph
        System.out.println("\n=== Weighted Directed Graph ===");
        Graph g2 = new Graph(4, true, true);
        g2.addEdge(0, 1, 5);
        g2.addEdge(0, 2, 3);
        g2.addEdge(1, 2, 2);
        g2.addEdge(1, 3, 6);
        g2.addEdge(2, 3, 7);
        g2.addEdge(3, 1, -2);
        g2.print();

        // Example 3: Build from edge list
        System.out.println("\n=== From Edge List ===");
        int[][] edges = {{0,1}, {1,2}, {2,3}, {3,0}};
        Graph g3 = Graph.fromEdgeList(4, edges, false);
        g3.print();

        // Example 4: Weighted from edge list
        System.out.println("\n=== Weighted From Edge List ===");
        int[][] weightedEdges = {{0,1,4}, {0,2,1}, {1,3,1}, {2,1,2}, {2,3,5}};
        Graph g4 = Graph.weightedFromEdgeList(4, weightedEdges, true);
        g4.print();

        // Example 5: Get neighbors
        System.out.println("\nNeighbors of vertex 1: " + g1.getNeighbors(1));
        System.out.println("Neighbors with weight: " + g4.getNeighborsWithWeight(2));
    }
}
```

## Quick Reference: Graph Construction Patterns

```java
class GraphPatterns {

    // Pattern 1: N-queen, grid problems
    // Build graph from grid
    public static Graph gridToGraph(char[][] grid) {
        int m = grid.length, n = grid[0].length;
        int totalCells = m * n;
        Graph graph = new Graph(totalCells);

        int[][] dirs = {{-1,0},{1,0},{0,-1},{0,1}};
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == '1') {
                    int u = i * n + j;
                    for (int[] d : dirs) {
                        int ni = i + d[0], nj = j + d[1];
                        if (ni >= 0 && ni < m && nj >= 0 && nj < n
                            && grid[ni][nj] == '1') {
                            int v = ni * n + nj;
                            graph.addEdge(u, v);
                        }
                    }
                }
            }
        }
        return graph;
    }

    // Pattern 2: Topological sort prerequisite graph
    // numCourses courses, prerequisites[i] = [a, b] means b → a
    public static Graph courseScheduleGraph(int numCourses, int[][] prerequisites) {
        Graph graph = new Graph(numCourses, true);
        for (int[] pre : prerequisites) {
            graph.addEdge(pre[1], pre[0]); // b → a
        }
        return graph;
    }
}
```

## When to Choose Which Representation

| Scenario | Best Choice |
|----------|-------------|
| General purpose | Adjacency List |
| Dense graph (E > V²/2) | Adjacency Matrix |
| Kruskal's MST | Edge List |
| Bellman-Ford | Edge List |
| BFS/DFS | Adjacency List |
| Floyd-Warshall | Adjacency Matrix |
| Need O(1) edge check | Adjacency Matrix |
| Memory constrained, sparse | Adjacency List |
