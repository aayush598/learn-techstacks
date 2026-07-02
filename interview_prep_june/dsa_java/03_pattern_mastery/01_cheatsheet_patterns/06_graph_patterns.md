# Graph Patterns

## Table of Contents
1. Graph Representation
2. BFS: Shortest Path Unweighted, Level Order, Connected Components
3. DFS: Connectivity, Cycles, Topological, SCC
4. Topological Sort: Dependency Resolution
5. Shortest Path Patterns
6. MST: Kruskal vs Prim
7. Union-Find: Dynamic Connectivity
8. Graph Problem Solver

---

## 1. Graph Representation: Which to Choose

### Adjacency Matrix
**Use when:** Dense graph (E ≈ V²). Need O(1) edge lookup.
```java
boolean[][] adj = new boolean[n][n];
// adj[u][v] = true if edge u→v exists
```
**Pros:** Simple, fast edge check
**Cons:** O(V²) space, wasteful for sparse graphs

### Adjacency List
**Use when:** Most problems. Sparse graph (E << V²).
```java
List<Integer>[] adj = new List[n];
for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
for (int[] edge : edges) {
    adj[edge[0]].add(edge[1]);
    adj[edge[1]].add(edge[0]); // undirected
}
```
**Pros:** O(V + E) space, good for traversal
**Cons:** Edge existence check is O(deg(v))

### Edge List
**Use when:** Input is edge list, Kruskal's MST, Bellman-Ford.
```java
int[][] edges = {{u1, v1, w1}, {u2, v2, w2}, ...};
```
**Pros:** Storage efficient, easy to sort
**Cons:** Not good for traversal

### HashMap for Nodes (Sparse / Graph not labeled 0..n-1)
**Use when:** Nodes are strings or arbitrary objects.
```java
Map<String, List<String>> graph = new HashMap<>();
```

### Decision Table
| Criteria | Adj Matrix | Adj List | Edge List | HashMap |
|----------|-----------|----------|-----------|---------|
| Dense graph | ✅ Best | ❌ | ❌ | ❌ |
| Sparse graph | ❌ | ✅ Best | ✅ | ✅ |
| Edge lookup O(1) | ✅ | ❌ | ❌ | ❌ |
| All neighbors quickly | ❌ O(V) | ✅ | ❌ | ✅ |
| Need to sort edges | ❌ | ❌ | ✅ Best | ❌ |
| Node labels are strings | ❌ | ❌ | ❌ | ✅ Best |
| Traversal (BFS/DFS) | ❌ O(V²) | ✅ O(V+E) | ❌ | ✅ |

---

## 2. BFS — Shortest Path Unweighted, Level Order, Connected Components

**When to use:**
- Shortest path in unweighted graph
- Connected components / islands
- Level-order processing
- Minimum steps to reach target

**Template:**
```java
void bfs(List<Integer>[] adj, int start) {
    int n = adj.length;
    boolean[] visited = new boolean[n];
    Queue<Integer> queue = new LinkedList<>();
    int[] dist = new int[n];
    Arrays.fill(dist, -1);

    visited[start] = true;
    dist[start] = 0;
    queue.offer(start);

    while (!queue.isEmpty()) {
        int u = queue.poll();
        for (int v : adj[u]) {
            if (!visited[v]) {
                visited[v] = true;
                dist[v] = dist[u] + 1;
                queue.offer(v);
            }
        }
    }
}
```

**Number of Islands (Grid BFS):**
```java
public int numIslands(char[][] grid) {
    int m = grid.length, n = grid[0].length, count = 0;
    int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == '1') {
                count++;
                grid[i][j] = '0';
                Queue<int[]> q = new LinkedList<>();
                q.offer(new int[]{i, j});
                while (!q.isEmpty()) {
                    int[] p = q.poll();
                    for (int[] d : dirs) {
                        int r = p[0] + d[0], c = p[1] + d[1];
                        if (r >= 0 && r < m && c >= 0 && c < n && grid[r][c] == '1') {
                            grid[r][c] = '0';
                            q.offer(new int[]{r, c});
                        }
                    }
                }
            }
        }
    }
    return count;
}
```

**Word Ladder (shortest transformation path):**
```java
public int ladderLength(String beginWord, String endWord, List<String> wordList) {
    Set<String> wordSet = new HashSet<>(wordList);
    if (!wordSet.contains(endWord)) return 0;
    Queue<String> queue = new LinkedList<>();
    queue.offer(beginWord);
    int level = 1;
    while (!queue.isEmpty()) {
        int size = queue.size();
        for (int i = 0; i < size; i++) {
            String curr = queue.poll();
            char[] chars = curr.toCharArray();
            for (int j = 0; j < curr.length(); j++) {
                char orig = chars[j];
                for (char c = 'a'; c <= 'z'; c++) {
                    chars[j] = c;
                    String next = new String(chars);
                    if (next.equals(endWord)) return level + 1;
                    if (wordSet.contains(next)) {
                        wordSet.remove(next);
                        queue.offer(next);
                    }
                }
                chars[j] = orig;
            }
        }
        level++;
    }
    return 0;
}
```

---

## 3. DFS — Connectivity, Cycles, Topological, SCC

**When to use:**
- Connectivity check (is there a path from u to v?)
- Detect cycles in directed/undirected graph
- Topological ordering (post-order reversal)
- Strongly connected components (Kosaraju, Tarjan)
- Bipartite graph check
- All paths from source to target

**Template:**
```java
void dfs(List<Integer>[] adj, int u, boolean[] visited) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) {
            dfs(adj, v, visited);
        }
    }
}
```

**Cycle Detection in Directed Graph (DFS with state):**
```java
// 0 = unvisited, 1 = in current path, 2 = done
boolean hasCycle(List<Integer>[] adj) {
    int n = adj.length;
    int[] state = new int[n];
    for (int i = 0; i < n; i++) {
        if (state[i] == 0 && dfsCycle(adj, i, state)) return true;
    }
    return false;
}
boolean dfsCycle(List<Integer>[] adj, int u, int[] state) {
    state[u] = 1;
    for (int v : adj[u]) {
        if (state[v] == 1) return true;
        if (state[v] == 0 && dfsCycle(adj, v, state)) return true;
    }
    state[u] = 2;
    return false;
}
```

**Bipartite Graph Check (DFS coloring):**
```java
boolean isBipartite(int[][] graph) {
    int n = graph.length;
    int[] color = new int[n]; // 0 = uncolored, 1, -1
    for (int i = 0; i < n; i++) {
        if (color[i] == 0) {
            color[i] = 1;
            if (!dfsColor(graph, i, color)) return false;
        }
    }
    return true;
}
boolean dfsColor(int[][] graph, int u, int[] color) {
    for (int v : graph[u]) {
        if (color[v] == color[u]) return false;
        if (color[v] == 0) {
            color[v] = -color[u];
            if (!dfsColor(graph, v, color)) return false;
        }
    }
    return true;
}
```

---

## 4. Topological Sort — Dependency Resolution

**When to use:** Prerequisite/course schedule, build order, dependency resolution.

### Kahn's Algorithm (BFS with indegree)
**Use when:** Need lexicographically smallest order, or any valid order.
```java
int[] topologicalSort(int n, int[][] edges) {
    List<Integer>[] adj = new List[n];
    int[] indegree = new int[n];
    for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
    for (int[] e : edges) {
        adj[e[0]].add(e[1]);
        indegree[e[1]]++;
    }
    Queue<Integer> queue = new LinkedList<>();
    for (int i = 0; i < n; i++)
        if (indegree[i] == 0) queue.offer(i);

    int[] order = new int[n];
    int idx = 0;
    while (!queue.isEmpty()) {
        int u = queue.poll();
        order[idx++] = u;
        for (int v : adj[u]) {
            if (--indegree[v] == 0) queue.offer(v);
        }
    }
    return idx == n ? order : new int[0]; // empty = cycle
}
```

### DFS-based Topological Sort
**Use when:** Need to process dependencies recursively.
```java
List<Integer> order = new ArrayList<>();
int[] state = new int[n]; // 0=unvisited, 1=visited, 2=done

boolean topoSort(List<Integer>[] adj, int u) {
    state[u] = 1;
    for (int v : adj[u]) {
        if (state[v] == 1) return false; // cycle
        if (state[v] == 0 && !topoSort(adj, v)) return false;
    }
    state[u] = 2;
    order.add(u);
    return true;
}
// Reverse order list to get topological order
```

### Problems Mapping to Topological Sort
| Problem | Application |
|---------|-------------|
| Course schedule I | Can all courses be taken? |
| Course schedule II | Order of courses |
| Alien dictionary | Order of letters from sorted words |
| Sequence reconstruction | Is topological order unique? |
| Parallel courses | Min semesters to complete |
| Minimum height trees | Topological removal of leaves |
| Build order | Compilation order |
| Find all possible recipes | Recipe → ingredient dependencies |

**Alien Dictionary:**
```java
public String alienOrder(String[] words) {
    Map<Character, Set<Character>> graph = new HashMap<>();
    Map<Character, Integer> indegree = new HashMap<>();
    for (String w : words)
        for (char c : w.toCharArray()) {
            graph.putIfAbsent(c, new HashSet<>());
            indegree.putIfAbsent(c, 0);
        }
    for (int i = 0; i < words.length - 1; i++) {
        String a = words[i], b = words[i + 1];
        int len = Math.min(a.length(), b.length());
        for (int j = 0; j < len; j++) {
            if (a.charAt(j) != b.charAt(j)) {
                if (!graph.get(a.charAt(j)).contains(b.charAt(j))) {
                    graph.get(a.charAt(j)).add(b.charAt(j));
                    indegree.put(b.charAt(j), indegree.get(b.charAt(j)) + 1);
                }
                break;
            }
            if (j == len - 1 && a.length() > b.length()) return "";
        }
    }
    Queue<Character> queue = new LinkedList<>();
    for (char c : indegree.keySet())
        if (indegree.get(c) == 0) queue.offer(c);
    StringBuilder sb = new StringBuilder();
    while (!queue.isEmpty()) {
        char c = queue.poll();
        sb.append(c);
        for (char next : graph.get(c)) {
            indegree.put(next, indegree.get(next) - 1);
            if (indegree.get(next) == 0) queue.offer(next);
        }
    }
    return sb.length() == indegree.size() ? sb.toString() : "";
}
```

---

## 5. Shortest Path Patterns

### BFS (Unweighted) — O(V + E)
**Use when:** All edges have equal weight (or no weight).

### Dijkstra's Algorithm — O((V + E) log V)
**Use when:** Non-negative edge weights.
```java
int[] dijkstra(List<int[]>[] adj, int start) {
    int n = adj.length;
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[start] = 0;
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    pq.offer(new int[]{start, 0});

    while (!pq.isEmpty()) {
        int[] cur = pq.poll();
        int u = cur[0], d = cur[1];
        if (d > dist[u]) continue;
        for (int[] edge : adj[u]) {
            int v = edge[0], w = edge[1];
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.offer(new int[]{v, dist[v]});
            }
        }
    }
    return dist;
}
```

### Bellman-Ford — O(VE)
**Use when:** Negative edge weights, detect negative cycles.
```java
int[] bellmanFord(int n, int[][] edges, int start) {
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[start] = 0;
    for (int i = 0; i < n - 1; i++) {
        for (int[] e : edges) {
            int u = e[0], v = e[1], w = e[2];
            if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
            }
        }
    }
    // Check for negative cycle
    for (int[] e : edges) {
        int u = e[0], v = e[1], w = e[2];
        if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) {
            return new int[0]; // Negative cycle exists
        }
    }
    return dist;
}
```

### Floyd-Warshall — O(V³)
**Use when:** All pairs shortest path, small graph (n ≤ 500).
```java
void floydWarshall(int[][] dist) {
    int n = dist.length;
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (dist[i][k] != Integer.MAX_VALUE && dist[k][j] != Integer.MAX_VALUE)
                    dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
}
```

### Decision: Which Shortest Path Algorithm?
| Criteria | Algorithm | Complexity |
|----------|-----------|------------|
| Unweighted graph | BFS | O(V + E) |
| Non-negative weights | Dijkstra | O((V+E) log V) |
| Negative weights | Bellman-Ford | O(VE) |
| All pairs, small n | Floyd-Warshall | O(V³) |
| All pairs, large n | Dijkstra from each node | O(V (V+E) log V) |
| Single source DAG | Topological sort + DP | O(V + E) |

---

## 6. MST — Kruskal vs Prim

### Kruskal's Algorithm — O(E log V)
**Use when:** Edge list is available, sparse graph.
```java
int kruskal(int n, int[][] edges) {
    Arrays.sort(edges, (a, b) -> a[2] - b[2]); // sort by weight
    int[] parent = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;
    int cost = 0, count = 0;
    for (int[] e : edges) {
        if (union(parent, e[0], e[1])) {
            cost += e[2];
            if (++count == n - 1) break;
        }
    }
    return cost;
}
```

### Prim's Algorithm — O(E log V)
**Use when:** Adjacency list available, dense graph.
```java
int prim(List<int[]>[] adj) {
    int n = adj.length;
    boolean[] visited = new boolean[n];
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    pq.offer(new int[]{0, 0}); // {node, cost}
    int cost = 0, count = 0;
    while (!pq.isEmpty()) {
        int[] cur = pq.poll();
        int u = cur[0], w = cur[1];
        if (visited[u]) continue;
        visited[u] = true;
        cost += w;
        if (++count == n) break;
        for (int[] edge : adj[u]) {
            if (!visited[edge[0]]) {
                pq.offer(new int[]{edge[0], edge[1]});
            }
        }
    }
    return cost;
}
```

### Kruskal vs Prim
| Criteria | Kruskal | Prim |
|----------|---------|------|
| Data structure | Union-Find | Min-Heap |
| Edge focus | Picks smallest edges | Grows from a node |
| Best for | Sparse graphs (E ≈ V) | Dense graphs (E ≈ V²) |
| Sort needed | Yes (sort all edges) | No (heap) |
| Complexity | O(E log E) | O(E log V) |

---

## 7. Union-Find (Disjoint Set Union)

**When to use:** Dynamic connectivity, Kruskal's MST, detecting cycles in undirected graph, connected components in dynamic graph.

### Template
```java
class UnionFind {
    int[] parent, rank;
    UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    int find(int x) {
        if (parent[x] != x)
            parent[x] = find(parent[x]); // path compression
        return parent[x];
    }
    boolean union(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false;
        // union by rank
        if (rank[px] < rank[py]) {
            parent[px] = py;
        } else if (rank[px] > rank[py]) {
            parent[py] = px;
        } else {
            parent[py] = px;
            rank[px]++;
        }
        return true;
    }
}
```

### Problems Mapping to Union-Find
| Problem | How Union-Find Helps |
|---------|---------------------|
| Number of connected components | Count unions |
| Detect cycle in undirected graph | union returns false if already connected |
| Redundant connection | First edge where union returns false |
| Accounts merge | Union accounts that share emails |
| Number of islands II (dynamic) | Union adjacent land cells |
| Longest consecutive sequence | Union adjacent numbers |
| Satisfiability of equations | Union equal variables, check unequal |
| Regions cut by slashes | Encode cells, union adjacent |
| Minimum cost to connect cities | Kruskal's MST |
| Friend circles | Count components after union |

---

## 8. Graph Problem Solver

### Decision Flowchart
```
What type of graph problem?
├── Shortest path between two nodes?
│   ├── Unweighted → BFS
│   ├── Non-negative weights → Dijkstra
│   ├── Negative weights → Bellman-Ford
│   └── All pairs → Floyd-Warshall
│
├── Connectivity / Components?
│   ├── Static graph → DFS/BFS count
│   ├── Dynamic additions → Union-Find
│   └── Bridges / Articulation → Tarjan DFS
│
├── Ordering / Dependencies?
│   ├── Topological order → Kahn's Algorithm or DFS
│   └── Check if DAG → Cycle detection
│
├── Cycle detection?
│   ├── Undirected → DFS with parent or Union-Find
│   └── Directed → DFS with state (0/1/2)
│
├── Minimum spanning tree?
│   ├── Sparse graph → Kruskal
│   └── Dense graph → Prim
│
├── Bipartite check?
│   └── DFS coloring (2-coloring)
│
└── Strongly connected components?
    └── Kosaraju or Tarjan
```
