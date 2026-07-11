# Disjoint Set Union (Advanced)

## DSU with Size Tracking

```java
class DSU {
    int[] parent, size;
    
    DSU(int n) {
        parent = new int[n];
        size = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
    }
    
    int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];  // path compression (half)
            x = parent[x];
        }
        return x;
    }
    
    void union(int x, int y) {
        int rootX = find(x), rootY = find(y);
        if (rootX == rootY) return;
        if (size[rootX] < size[rootY]) { int t = rootX; rootX = rootY; rootY = t; }
        parent[rootY] = rootX;
        size[rootX] += size[rootY];
    }
    
    int getSize(int x) { return size[find(x)]; }
}
```

## DSU on Grid (2D to 1D mapping)

```java
class DSUGrid {
    DSU dsu;
    int rows, cols;
    
    DSUGrid(int m, int n) {
        rows = m; cols = n;
        dsu = new DSU(m * n);
    }
    
    int id(int r, int c) { return r * cols + c; }
    boolean valid(int r, int c) { return r >= 0 && r < rows && c >= 0 && c < cols; }
    
    void union(int r1, int c1, int r2, int c2) {
        if (valid(r1, c1) && valid(r2, c2)) dsu.union(id(r1, c1), id(r2, c2));
    }
}
```

## Applications

### Dynamic Connectivity
```java
// After each edge addition, check connectivity in O(α(n))
```

### Kruskal's MST
```java
// Already covered in MST section
```

### Number of Islands II
```java
// Already covered
```

### Accounts Merge
```java
// Already covered
```

### Longest Consecutive Sequence
```java
// Already covered (see Union-Find detailed)
```

### Earliest Moment Everyone Becomes Friends
```java
int earliestAcq(int[][] logs, int n) {
    Arrays.sort(logs, (a, b) -> a[0] - b[0]);
    DSU dsu = new DSU(n);
    int components = n;
    
    for (int[] log : logs) {
        if (dsu.find(log[1]) != dsu.find(log[2])) {
            dsu.union(log[1], log[2]);
            components--;
            if (components == 1) return log[0];
        }
    }
    return -1;
}
```
