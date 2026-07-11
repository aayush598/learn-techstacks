# Union-Find (DSU) Patterns Cheatsheet

---

## When to Use Union-Find

- **Dynamic connectivity:** Are two nodes connected? How many components?
- **Cycle detection** in undirected graph
- **Grouping** elements into equivalence classes
- **Incremental graph** problems (adding edges one by one)
- Problems involving "becoming friends", "merging accounts", "connected islands"

---

## Core Implementation

```java
class UnionFind {
    private int[] parent;
    private int[] rank;
    private int components;

    public UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        components = n;
        for (int i = 0; i < n; i++) {
            parent[i] = i; // each node is its own parent
        }
    }

    // Find with path compression
    public int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]); // path compression
        }
        return parent[x];
    }

    // Union by rank
    public boolean union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);

        if (rootX == rootY) return false; // already connected

        // Attach smaller rank tree under root of higher rank
        if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
        } else if (rank[rootX] > rank[rootY]) {
            parent[rootY] = rootX;
        } else {
            parent[rootY] = rootX;
            rank[rootX]++;
        }

        components--;
        return true;
    }

    public boolean connected(int x, int y) {
        return find(x) == find(y);
    }

    public int getComponents() {
        return components;
    }
}
```

**Complexity:** O(α(n)) per operation — α is the inverse Ackermann function, effectively O(1).

---

## Pattern 1: Connected Components

### Number of Provinces (LeetCode 547)

```java
public int findCircleNum(int[][] isConnected) {
    int n = isConnected.length;
    UnionFind uf = new UnionFind(n);

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (isConnected[i][j] == 1) {
                uf.union(i, j);
            }
        }
    }
    return uf.getComponents();
}
```

### Accounts Merge (LeetCode 721)

```java
public List<List<String>> accountsMerge(List<List<String>> accounts) {
    Map<String, Integer> emailToId = new HashMap<>();
    Map<String, String> emailToName = new HashMap<>();
    int id = 0;

    UnionFind uf = new UnionFind(accounts.size());

    for (List<String> account : accounts) {
        String name = account.get(0);
        for (int i = 1; i < account.size(); i++) {
            String email = account.get(i);
            emailToName.put(email, name);

            if (!emailToId.containsKey(email)) {
                emailToId.put(email, id++);
            }
            uf.union(emailToId.get(account.get(1)), emailToId.get(email));
        }
    }

    Map<Integer, List<String>> merged = new HashMap<>();
    for (String email : emailToId.keySet()) {
        int root = uf.find(emailToId.get(email));
        merged.computeIfAbsent(root, k -> new ArrayList<>()).add(email);
    }

    List<List<String>> result = new ArrayList<>();
    for (List<String> emails : merged.values()) {
        Collections.sort(emails);
        List<String> account = new ArrayList<>();
        account.add(emailToName.get(emails.get(0)));
        account.addAll(emails);
        result.add(account);
    }
    return result;
}
```

---

## Pattern 2: Cycle Detection

### Graph Valid Tree (LeetCode 261)

```java
public boolean validTree(int n, int[][] edges) {
    if (edges.length != n - 1) return false; // tree must have exactly n-1 edges

    UnionFind uf = new UnionFind(n);
    for (int[] edge : edges) {
        if (!uf.union(edge[0], edge[1])) {
            return false; // cycle detected (already connected)
        }
    }
    return true; // connected and no cycles
}
```

### Redundant Connection (LeetCode 684)

```java
public int[] findRedundantConnection(int[][] edges) {
    UnionFind uf = new UnionFind(edges.length + 1);

    for (int[] edge : edges) {
        if (!uf.union(edge[0], edge[1])) {
            return edge; // first edge that creates a cycle
        }
    }
    return new int[]{};
}
```

---

## Pattern 3: Union on Grid

### Number of Islands II (LeetCode 305)

Incrementally add land cells and track number of islands after each addition.

```java
public List<Integer> numIslands2(int m, int n, int[][] positions) {
    UnionFind uf = new UnionFind(m * n);
    char[][] grid = new char[m][n];
    int count = 0;
    List<Integer> result = new ArrayList<>();

    int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};

    for (int[] pos : positions) {
        int r = pos[0], c = pos[1];
        if (grid[r][c] == '1') {
            result.add(count);
            continue;
        }

        grid[r][c] = '1';
        count++;

        for (int[] d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr >= 0 && nr < m && nc >= 0 && nc < n && grid[nr][nc] == '1') {
                if (uf.union(r * n + c, nr * n + nc)) {
                    count--;
                }
            }
        }
        result.add(count);
    }
    return result;
}
```

### Regions Cut By Slashes (LeetCode 959)

```java
public int regionsBySlashes(String[] grid) {
    int n = grid.length;
    int points = (n + 1) * (n + 1);
    UnionFind uf = new UnionFind(points);

    // Union border points
    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= n; j++) {
            if (i == 0 || j == 0 || i == n || j == n) {
                uf.union(0, i * (n + 1) + j);
            }
        }
    }

    int regions = 1;
    for (int r = 0; r < n; r++) {
        for (int c = 0; c < n; c++) {
            int cell = r * (n + 1) + c;

            if (grid[r].charAt(c) == '/') {
                if (uf.union(cell, cell + n + 2)) {
                    regions++;
                }
            } else if (grid[r].charAt(c) == '\\') {
                if (uf.union(cell + 1, cell + n + 1)) {
                    regions++;
                }
            } else {
                if (uf.union(cell, cell + 1)) regions++;
                if (uf.union(cell, cell + n + 1)) regions++;
            }
        }
    }
    return regions;
}
```

---

## Pattern 4: Union by Order (Time-based)

### Earliest Moment When Everyone Becomes Friends (LeetCode 1101)

```java
public int earliestAcq(int[][] logs, int n) {
    Arrays.sort(logs, (a, b) -> Integer.compare(a[0], b[0]));

    UnionFind uf = new UnionFind(n);

    for (int[] log : logs) {
        uf.union(log[1], log[2]);
        if (uf.getComponents() == 1) {
            return log[0];
        }
    }
    return -1;
}
```

---

## Pattern 5: Kruskal's MST

```java
public int minimumCost(int n, int[][] connections) {
    Arrays.sort(connections, (a, b) -> Integer.compare(a[2], b[2]));

    UnionFind uf = new UnionFind(n);
    int totalCost = 0, edgesUsed = 0;

    for (int[] conn : connections) {
        if (uf.union(conn[0] - 1, conn[1] - 1)) {
            totalCost += conn[2];
            edgesUsed++;
            if (edgesUsed == n - 1) break;
        }
    }

    return edgesUsed == n - 1 ? totalCost : -1;
}
```

---

## DSU Template with Path Compression + Union by Rank

```java
class DSU {
    int[] parent, rank;

    DSU(int n) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    int find(int x) {
        return parent[x] == x ? x : (parent[x] = find(parent[x]));
    }

    boolean union(int x, int y) {
        x = find(x); y = find(y);
        if (x == y) return false;
        if (rank[x] < rank[y]) { int t = x; x = y; y = t; }
        parent[y] = x;
        if (rank[x] == rank[y]) rank[x]++;
        return true;
    }
}
```

---

## 10+ DSU Problem Templates

| # | Problem | DSU Pattern |
|---|---------|-------------|
| 1 | Number of Provinces | Simple connected components |
| 2 | Accounts Merge | Union emails, group by root |
| 3 | Graph Valid Tree | n-1 edges + no cycle |
| 4 | Redundant Connection | First edge creating cycle |
| 5 | Number of Islands II | Incremental union on grid |
| 6 | Smallest String With Swaps | Union indices, sort per group |
| 7 | Accounts Merge II | Union by email ID |
| 8 | Regions Cut By Slashes | Triangulate cells, union edges |
| 9 | Earliest Acq | Sort by time, union until 1 component |
| 10 | Make Network Connected | Check if n-1 edges suffice |
| 11 | Detect Cycles in Grid | Union with directional offsets |
| 12 | Minimum Spanning Tree | Kruskal's with DSU |
