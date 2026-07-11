# Eulerian Path & Circuit

## Definitions

- **Eulerian Trail**: visits every edge exactly once
- **Eulerian Circuit**: Eulerian trail starting and ending at same vertex
- **Eulerian Graph**: has Eulerian circuit

## Conditions

### Undirected Graph
| Property | Eulerian Circuit | Eulerian Trail |
|----------|-----------------|----------------|
| All vertices with non-zero degree | Connected | Connected |
| Vertex degrees | All even | Exactly 0 or 2 odd |

### Directed Graph
| Property | Eulerian Circuit | Eulerian Trail |
|----------|-----------------|----------------|
| All vertices with non-zero degree | Same SCC | Same |
| Vertex degrees | in-degree = out-degree for all | start: out - in = 1, end: in - out = 1, rest: equal |

## Hierholzer's Algorithm

Finds Eulerian circuit in O(E):

```java
List<Integer> findEulerianCircuit(List<List<Integer>> graph, int V, int start) {
    // Copy adjacency list for mutability (remove edges as used)
    Map<Integer, Queue<Integer>> adj = new HashMap<>();
    for (int i = 0; i < V; i++) {
        adj.put(i, new LinkedList<>(graph.get(i)));
    }
    
    List<Integer> circuit = new LinkedList<>();
    hierholzer(start, adj, circuit);
    return circuit;
}

void hierholzer(int u, Map<Integer, Queue<Integer>> adj, List<Integer> circuit) {
    Queue<Integer> neighbors = adj.get(u);
    while (neighbors != null && !neighbors.isEmpty()) {
        int v = neighbors.poll();
        hierholzer(v, adj, circuit);
    }
    circuit.add(0, u);  // add to front (or use stack and reverse)
}
```

## Problem: Reconstruct Itinerary

```java
List<String> findItinerary(List<List<String>> tickets) {
    Map<String, PriorityQueue<String>> graph = new HashMap<>();
    for (List<String> t : tickets) {
        graph.computeIfAbsent(t.get(0), k -> new PriorityQueue<>()).offer(t.get(1));
    }
    
    LinkedList<String> result = new LinkedList<>();
    dfsItinerary("JFK", graph, result);
    return result;
}

void dfsItinerary(String airport, Map<String, PriorityQueue<String>> graph, 
                  LinkedList<String> result) {
    PriorityQueue<String> dests = graph.get(airport);
    while (dests != null && !dests.isEmpty()) {
        dfsItinerary(dests.poll(), graph, result);
    }
    result.addFirst(airport);
}
```
