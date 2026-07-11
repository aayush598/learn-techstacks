# Union-Find (Disjoint Set Union)

## Overview

Tracks elements partitioned into disjoint (non-overlapping) subsets. Supports:
- **find(x)**: which set does x belong to?
- **union(x,y)**: merge sets containing x and y

## Implementation with Path Compression + Union by Rank

```java
class DSU {
    private int[] parent;
    private int[] rank;  // or size
    
    DSU(int n) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    
    // Path compression: make every node point directly to root
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }
    
    // Union by rank: attach smaller tree under larger tree
    void union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        if (rootX == rootY) return;
        
        if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
        } else if (rank[rootX] > rank[rootY]) {
            parent[rootY] = rootX;
        } else {
            parent[rootY] = rootX;
            rank[rootX]++;
        }
    }
    
    boolean isConnected(int x, int y) {
        return find(x) == find(y);
    }
    
    int countComponents() {
        Set<Integer> roots = new HashSet<>();
        for (int i = 0; i < parent.length; i++) {
            roots.add(find(i));
        }
        return roots.size();
    }
}
```

## Complexity

With path compression + union by rank:
- **find**: O(α(n)) — inverse Ackermann (practically constant)
- **union**: O(α(n))
- Total for m operations: O(m α(n))

## Applications

### 1. Cycle Detection in Graph
```java
boolean hasCycle(List<int[]> edges, int V) {
    DSU dsu = new DSU(V);
    for (int[] edge : edges) {
        if (dsu.find(edge[0]) == dsu.find(edge[1])) return true;
        dsu.union(edge[0], edge[1]);
    }
    return false;
}
```

### 2. Number of Connected Components
```java
int countComponents(int n, int[][] edges) {
    DSU dsu = new DSU(n);
    for (int[] e : edges) dsu.union(e[0], e[1]);
    return dsu.countComponents();
}
```

### 3. Number of Islands II (Dynamic)
```java
List<Integer> numIslands2(int m, int n, int[][] positions) {
    DSU dsu = new DSU(m * n);
    int[][] grid = new int[m][n];
    int[][] dirs = {{0,1},{1,0},{0,-1},{-1,0}};
    List<Integer> result = new ArrayList<>();
    int count = 0;
    
    for (int[] pos : positions) {
        int r = pos[0], c = pos[1];
        if (grid[r][c] == 1) { result.add(count); continue; }
        grid[r][c] = 1;
        count++;
        
        for (int[] d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr >= 0 && nr < m && nc >= 0 && nc < n && grid[nr][nc] == 1) {
                int id1 = r * n + c;
                int id2 = nr * n + nc;
                if (dsu.find(id1) != dsu.find(id2)) {
                    dsu.union(id1, id2);
                    count--;
                }
            }
        }
        result.add(count);
    }
    return result;
}
```

### 4. Accounts Merge
```java
List<List<String>> accountsMerge(List<List<String>> accounts) {
    DSU dsu = new DSU(accounts.size());
    Map<String, Integer> emailToId = new HashMap<>();
    
    for (int i = 0; i < accounts.size(); i++) {
        for (int j = 1; j < accounts.get(i).size(); j++) {
            String email = accounts.get(i).get(j);
            if (emailToId.containsKey(email)) {
                dsu.union(i, emailToId.get(email));
            } else {
                emailToId.put(email, i);
            }
        }
    }
    
    Map<Integer, TreeSet<String>> idToEmails = new HashMap<>();
    for (Map.Entry<String, Integer> e : emailToId.entrySet()) {
        int root = dsu.find(e.getValue());
        idToEmails.computeIfAbsent(root, k -> new TreeSet<>()).add(e.getKey());
    }
    
    List<List<String>> result = new ArrayList<>();
    for (Map.Entry<Integer, TreeSet<String>> e : idToEmails.entrySet()) {
        List<String> list = new ArrayList<>();
        list.add(accounts.get(e.getKey()).get(0));  // name
        list.addAll(e.getValue());
        result.add(list);
    }
    return result;
}
```

### 5. Longest Consecutive Sequence
```java
int longestConsecutive(int[] nums) {
    Map<Integer, Integer> map = new HashMap<>();
    DSU dsu = new DSU(nums.length);
    int maxLen = 0;
    
    for (int i = 0; i < nums.length; i++) {
        if (map.containsKey(nums[i])) continue;
        map.put(nums[i], i);
        
        if (map.containsKey(nums[i] - 1)) dsu.union(i, map.get(nums[i] - 1));
        if (map.containsKey(nums[i] + 1)) dsu.union(i, map.get(nums[i] + 1));
    }
    
    Map<Integer, Integer> size = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int root = dsu.find(i);
        size.merge(root, 1, Integer::sum);
        maxLen = Math.max(maxLen, size.get(root));
    }
    return maxLen;
}
```
