# Graph Problems - Batch 2 (Additional 40 Problems)

---

## Problem 1: Find the Town Judge

**Problem Explanation:** We have n people labeled 1 to n. Some people trust others (given as pairs [a,b] meaning a trusts b). We need to find the town judge — a person who is trusted by EVERYONE else but trusts NOBODY. If no such person exists, return -1.

**Algorithm Steps:**
1. Create a `balance` array of size n+1 (ignore index 0).
2. For each trust relationship `[a, b]`: decrement balance[a] (a trusts someone → -1), increment balance[b] (b is trusted → +1).
3. After processing all edges, scan indices 1..n.
4. If `balance[i] == n-1`, that person is the judge (trusted by all n-1 others, trusts none).
5. If no match, return -1.

**Visual Walkthrough:** n = 4, trust = [[1,3],[2,3],[3,1]]
```
Initial balance: [0, 0, 0, 0, 0]
After [1,3]:     [0, -1,  0, +1,  0]   # 1 trusts 3
After [2,3]:     [0, -1, -1, +2,  0]   # 2 trusts 3
After [3,1]:     [0,  0, -1, +1,  0]   # 3 trusts 1
Scan: balance[1]=0, balance[2]=-1, balance[3]=1, none = n-1=3 → return -1
```

**Key Insight:** The judge has trust score = n-1 (in-degree from everyone, out-degree to nobody). Track net trust balance in one pass.

**Edge Cases:** n=1 with no trust → person 1 is judge (returns 1). Multiple people with balance n-1 → still return first found (but only one should exist per problem constraints).

**Common Mistakes:** Forgetting index 0 is unused (people are 1-indexed). Confusing who trusts whom (a trusts b means b is trusted, not a).

**Pattern Recognition:** **Graph Indegree/Outdegree Pattern**: Track net flow of trust/relationships. Used in: Find Celebrity, Employee Importance.

**Statement:** In a town of n people, person 1 to n. Trust[i] = [a,b] means a trusts b. Town judge trusts nobody, everybody trusts town judge. Find the judge.

**Approach:** Use an array to track trust balance. +1 for being trusted, -1 for trusting. Judge has balance = n-1.

```python
# findTownJudge: implement solution
def findTownJudge(n, trust):
    balance = [0] * (n + 1)
    for a, b in trust:
        balance[a] -= 1
        balance[b] += 1
    for i in range(1, n + 1):
        if balance[i] == n - 1:
            return i
    return -1
```
**Time:** O(n) | **Space:** O(n)

---

## Problem 2: Find Center of Star Graph

**Problem Explanation:** A star graph has one central node connected to every other node. Given the list of edges (each connecting two nodes), find the center node — the one that appears in every edge.

**Algorithm Steps:**
1. Look at the first edge: it connects two nodes `[a, b]`.
2. Look at the second edge: it connects two nodes `[c, d]`.
3. If `a` equals `c` or `a` equals `d`, then `a` is the center; otherwise `b` is the center.

**Visual Walkthrough:** edges = [[1,2],[2,3],[4,2]]
```
First edge:  [1, 2]
Second edge: [2, 3]
Common node between first two edges → 2 is the center
(You can verify: 2 appears in ALL three edges)
```

**Key Insight:** The center appears in EVERY edge. Checking just the first two edges is sufficient because the center is guaranteed to be in both.

**Edge Cases:** Only 2 nodes (one edge) → either node could be center. n=2 edge case is handled automatically.

**Common Mistakes:** Building an entire adjacency list when O(1) observation suffices.

**Pattern Recognition:** **Graph Properties Observation**: Sometimes the answer is found by simple property analysis rather than full traversal. Used in: Find the Town Judge, Degree of Graph.

**Statement:** Find the center node of a star graph (all edges connect to center).

**Approach:** The center appears in every edge. Just check first two edges - common node is center.

```python
# findCenter: implement solution
def findCenter(edges):
    if edges[0][0] == edges[1][0] or edges[0][0] == edges[1][1]:
        return edges[0][0]
    return edges[0][1]
```
**Time:** O(1) | **Space:** O(1)

---

## Problem 3: Find if Path Exists in Graph

**Problem Explanation:** You're given n nodes (0 to n-1), an edge list, a source node, and a destination node. Determine whether there's any path (sequence of edges) from source to destination. The graph is undirected.

**Algorithm Steps:**
1. Build an adjacency list from the edge list.
2. BFS/DFS from `source`, tracking visited nodes.
3. If at any point we reach `destination`, return True.
4. If BFS/DFS completes without reaching destination, return False.

**Visual Walkthrough:** n=6, edges=[[0,1],[0,2],[3,5],[5,4],[4,3]], source=0, destination=5
```
Graph:  0 ─ 1         3 ─ 5
        │              │
        2              4
BFS from 0: visit 0, then 1, 2. Queue empty. Never reached 5.
Return: False (nodes 0-2 and 3-5 are separate components)
```

**Key Insight:** Can't reach destination if they're in different connected components. BFS gives shortest path; DFS uses less memory for deep graphs.

**Edge Cases:** source == destination → return True immediately. Disconnected graph → return False. Single node with no edges → True if source == dest.

**Common Mistakes:** Forgetting to add reverse edges (graph is undirected). Not using visited set → infinite loop in cycles.

**Pattern Recognition:** **Graph Traversal Pattern**: BFS/DFS to check connectivity between nodes. Used in: Number of Connected Components, Valid Tree, Course Schedule.

**Statement:** Given n nodes, edges, source, destination. Check if path exists.

**Approach:** Simple BFS/DFS from source to see if we reach destination.

```python
# validPath: implement solution
def validPath(n, edges, source, destination):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    visited = set([source])
    queue = deque([source])
    while queue:
        node = queue.popleft()
        if node == destination:
            return True
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                queue.append(nei)
    return False
```
**Time:** O(n+e) | **Space:** O(n+e)

---

## Problem 4: Number of Connected Components

**Problem Explanation:** A connected component is a group of nodes where every node can reach every other node via edges. Count how many such groups exist in the graph. Isolated nodes count as their own component.

**Algorithm Steps:**
1. Build adjacency list from edges.
2. Initialize visited set and component count = 0.
3. For each node 0 to n-1: if not visited, run DFS to mark all nodes in its component, increment count.
4. Return the count.

**Visual Walkthrough:** n=5, edges=[[0,1],[1,2],[3,4]]
```
Graph Visualization:
  0 ─ 1 ─ 2        3 ─ 4
Component 1: {0,1,2} → DFS from 0 marks 0,1,2
Component 2: {3,4}   → DFS from 3 marks 3,4
Return: 2
```

**Key Insight:** Each DFS/BFS call from an unvisited node discovers exactly one entire connected component. Count the number of such calls.

**Edge Cases:** n=0 → return 0. No edges → n components (each node alone). Fully connected → 1 component.

**Common Mistakes:** Iterating edges while marking instead of adjacency list traversal. Not handling isolated nodes.

**Pattern Recognition:** **Component Counting Pattern**: DFS/BFS from each unvisited node. Used in: Number of Islands, Number of Provinces, Accounts Merge.

**Statement:** Count connected components in undirected graph.

**Approach:** DFS/BFS from each unvisited node, increment count.

```python
# countComponents: implement solution
def countComponents(n, edges):
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    visited = set()
    count = 0
    def dfs(node):
        visited.add(node)
        for nei in graph[node]:
            if nei not in visited:
                dfs(nei)
    for i in range(n):
        if i not in visited:
            dfs(i)
            count += 1
    return count
```
**Time:** O(n+e) | **Space:** O(n+e)

---

## Problem 5: Is Graph Bipartite

**Problem Explanation:** A graph is bipartite if we can split its nodes into two groups such that every edge connects a node from one group to the other (no edges within a group). This is the same as 2-coloring where no adjacent nodes share the same color.

**Algorithm Steps:**
1. Initialize a `color` array of length n with -1 (uncolored).
2. For each uncolored node (handles disconnected graphs):
   - Color it 0, push to stack/BFS queue.
   - While stack not empty: pop node, for each neighbor:
     - If uncolored: assign opposite color (1 - color[node]), push.
     - If same color as current node: return False.
3. If all nodes colored without conflict, return True.

**Visual Walkthrough:** graph = [[1,2,3],[0,2],[0,1,3],[0,2]]
```
Start at node 0 → color 0
  Neighbors: 1(color 1), 2(color 1), 3(color 1)
Node 1: neighbors 0(0)✓, 2 → conflict! 2 is color 1 but should be 0
         ↓
Return: False (this is an odd cycle, not bipartite)
```

**Key Insight:** A graph is bipartite iff it contains no odd-length cycles. 2-coloring either succeeds or reveals a conflict that proves odd cycle exists.

**Edge Cases:** Single node → bipartite. Empty graph → bipartite. Triangle (3-cycle) → NOT bipartite.

**Common Mistakes:** Not handling disconnected components (each must be 2-colorable). Checking only one component and assuming the whole graph is bipartite.

**Pattern Recognition:** **Graph Coloring Pattern**: 2-coloring via BFS/DFS with alternating colors. Used in: Possible Bipartition, Is Graph Bipartite (adjacency matrix), Course Schedule (cycle detection variant).

**Statement:** Check if graph can be colored with 2 colors such that no adjacent nodes have same color.

**Approach:** BFS/DFS coloring. If we find a node with same color as current, not bipartite.

```python
# isBipartite: implement solution
def isBipartite(graph):
    n = len(graph)
    color = [-1] * n
    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        stack = [start]
        while stack:
            node = stack.pop()
            for nei in graph[node]:
                if color[nei] == -1:
                    color[nei] = 1 - color[node]
                    stack.append(nei)
                elif color[nei] == color[node]:
                    return False
    return True
```
**Time:** O(n+e) | **Space:** O(n)

---

## Problem 6: Number of Nodes in Sub-Tree With Same Label

**Problem Explanation:** You're given a tree where each node has a letter label. For each node, count how many nodes in its subtree (including itself) share the same label. Return an array of size n with these counts.

**Algorithm Steps:**
1. Build adjacency list. Root the tree at node 0 with parent -1.
2. Run DFS from (0, -1). Each DFS returns a frequency map of labels in that subtree.
3. At each node: start with `{label: 1}`, merge children's frequency maps.
4. Set `result[node] = count[label_of_node]`.
5. Return the merged frequency map to parent.

**Visual Walkthrough:** n=7, edges=[[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]], labels="abaedcd"
```
Tree Structure:     a(0)
                  /    \
                b(1)   a(2)
               /   \    /   \
             a(3) e(4) d(5) c(6)
             
Leaf nodes: 3→{a:1} result[3]=1, 4→{e:1} result[4]=1, 
            5→{d:1} result[5]=1, 6→{c:1} result[6]=1
Node 1 merges {a:1,b:1} → result[1]=1 (b appears once)
Node 2 merges {d:1,c:1,a:1} → result[2]=1 (a appears once)
Node 0 merges all → {a:3,b:1,e:1,d:1,c:1} → result[0]=3
```

**Key Insight:** Post-order DFS naturally collects subtree info. Merge children's frequency maps, add current node's label, and set result.

**Edge Cases:** n=1 → result[0]=1. All same labels → result[i] = size of subtree at i.

**Common Mistakes:** Not passing parent to avoid traversing back up. Using O(n²) merge (copying entire maps).

**Pattern Recognition:** **Tree DFS with Post-order Merge**: Collect subtree information by merging children's results. Used in: Count Nodes Equal to Average of Subtree, Sum of Distances in Tree.

**Statement:** For each node, find number of nodes in its subtree with the same label.

**Approach:** DFS returning frequency map of labels in subtree. Merge children's maps.

```python
# countSubTrees: implement solution
def countSubTrees(n, edges, labels):
    from collections import defaultdict
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    result = [0] * n
    def dfs(node, parent):
        count = {labels[node]: 1}
        for nei in graph[node]:
            if nei != parent:
                child_count = dfs(nei, node)
                for k, v in child_count.items():
                    count[k] = count.get(k, 0) + v
        result[node] = count[labels[node]]
        return count
    dfs(0, -1)
    return result
```
**Time:** O(n) | **Space:** O(n)

---

## Problem 7: Maximum Number of Edges to Make Graph Fully Connected

**Problem Explanation:** You have n nodes and some edges that can be used by Alice only (type 1), Bob only (type 2), or both (type 3). Find the maximum number of edges you can remove such that both Alice and Bob can still traverse all nodes. This is about finding redundant edges while keeping connectivity for both.

**Algorithm Steps:**
1. Use two Union-Find structures (Alice and Bob).
2. Process type-3 edges first (benefit both) — unite in both UFs.
3. Then process type-1 (Alice) and type-2 (Bob) edges separately.
4. Track edges used. If either UF has >1 component after all edges, return -1.
5. Return total_edges - edges_used.

**Visual Walkthrough:** n=4, edges=[[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]]
```
Type 3 first: [1,2] unite for both, [2,3] unite for both → components=2
Alice type 1: [1,3] already connected skip, [2,4] unite → components=1
Bob type 2: [3,4] unite → components=1
Edges used = 3, total = 6, max removable = 3
```

**Key Insight:** Type-3 edges are most valuable because they connect for both people at once. Process them first (greedy).

**Edge Cases:** Not enough edges to connect all nodes → return -1. n=1 with no edges → return 0.

**Common Mistakes:** Processing type-1/2 before type-3 (misses optimal removal count). Not tracking components separately for Alice and Bob.

**Pattern Recognition:** **Union-Find with Types**: Process shared resources before exclusive ones. Used in: Accounts Merge, Number of Operations to Make Network Connected.

**Statement:** Given n nodes and edges, find max edges to add to make graph fully connected.

**Approach:** Count connected components using Union-Find. Need (components-1) more edges.

```python
# maxNumEdgesToRemove: implement solution
def maxNumEdgesToRemove(n, edges):
    class UnionFind:
        def __init__(self, n):
            self.p = list(range(n+1))
            self.r = [0]*(n+1)
            self.components = n
        def find(self, x):
            if self.p[x] != x: self.p[x] = self.find(self.p[x])
            return self.p[x]
        def union(self, x, y):
            px, py = self.find(x), self.find(y)
            if px == py: return False
            if self.r[px] < self.r[py]: px, py = py, px
            self.p[py] = px
            if self.r[px] == self.r[py]: self.r[px] += 1
            self.components -= 1
            return True
    alice, bob = UnionFind(n), UnionFind(n)
    edges_used = 0
    for t, u, v in sorted(edges, reverse=True):
        if t == 3:
            if alice.union(u, v):
                bob.union(u, v)
                edges_used += 1
        elif t == 1:
            if alice.union(u, v):
                edges_used += 1
        else:
            if bob.union(u, v):
                edges_used += 1
    if alice.components == 1 and bob.components == 1:
        return len(edges) - edges_used
    return -1
```
**Time:** O(e*α(n)) | **Space:** O(n)

---

## Problem 8: Is Graph Bipartite (DFS)

**Problem Explanation:** Same as Problem 5 — check if graph can be 2-colored so adjacent nodes have different colors. This version uses DFS (recursive) instead of BFS/iterative stack.

**Algorithm Steps:**
1. Initialize `color` array with -1 (uncolored).
2. For each uncolored node, call DFS with color 0.
3. In DFS: assign color, recurse neighbors with opposite color.
4. If neighbor has same color → conflict → return False.

**Visual Walkthrough:** Same logic as Problem 5 but uses recursion. The DFS version is more intuitive for coloring problems and allows early exit via return values.

**Key Insight:** Recursive DFS naturally explores deep into a component, coloring as it goes. The function returns False immediately on first conflict.

**Edge Cases:** Deep recursion may exceed Python's recursion limit (~1000) for graphs with 1000+ nodes. Use iterative stack or set recursionlimit.

**Common Mistakes:** Not returning False propagation correctly (must check `if not dfs(nei, 1-c): return False`).

**Pattern Recognition:** **DFS Coloring Pattern**: Recursive DFS with alternating colors. Used in: Possible Bipartition, Graph Valid Tree.

**Statement:** Same as Problem 5 but using DFS approach.

```python
# isBipartite: implement solution
def isBipartite(graph):
    n = len(graph)
    color = [-1] * n
    def dfs(node, c):
        color[node] = c
        for nei in graph[node]:
            if color[nei] == -1:
                if not dfs(nei, 1 - c):
                    return False
            elif color[nei] == c:
                return False
        return True
    for i in range(n):
        if color[i] == -1:
            if not dfs(i, 0):
                return False
    return True
```
**Time:** O(n+e) | **Space:** O(n)

---

## Problem 9: All Paths from Source to Target

**Problem Explanation:** Given a Directed Acyclic Graph (DAG) as an adjacency list, find all possible paths from node 0 to the last node (n-1). Return them as a list of node sequences.

**Algorithm Steps:**
1. Initialize an empty result list.
2. Start DFS from node 0 with path = [0].
3. At each node: if it's the target (n-1), add path copy to result.
4. Otherwise, for each neighbor, append neighbor to path, recurse, then backtrack (pop).
5. Return all collected paths.

**Visual Walkthrough:** graph = [[1,2],[3],[3],[]]
```
The DAG: 0 → 1 → 3
         0 → 2 → 3

DFS(0, [0]):
  → DFS(1, [0,1]): → DFS(3, [0,1,3]): target! add [0,1,3]
  → DFS(2, [0,2]): → DFS(3, [0,2,3]): target! add [0,2,3]
Return: [[0,1,3], [0,2,3]]
```

**Key Insight:** In a DAG, no cycles means simple DFS without visited set works (can't revisit nodes). Backtracking ensures we explore all paths.

**Edge Cases:** Single node (n=1) → return [[0]]. Disconnected graph → target unreachable → return [].

**Common Mistakes:** Forgetting to copy the path (using same list reference). Trying to BFS for all paths (BFS works but DFS+backtrack is cleaner).

**Pattern Recognition:** **Backtracking on DAG Pattern**: DFS + path tracking for exhaustive path enumeration. Used in: Word Search II, N-Queens, Combination Sum.

**Statement:** Find all paths from node 0 to node n-1 in DAG.

**Approach:** Simple DFS, add path when reaching target.

```python
# allPathsSourceTarget: implement solution
def allPathsSourceTarget(graph):
    n = len(graph)
    result = []
    def dfs(node, path):
        if node == n - 1:
            result.append(path[:])
            return
        for nei in graph[node]:
            path.append(nei)
            dfs(nei, path)
            path.pop()
    dfs(0, [0])
    return result
```
**Time:** O(2^n) | **Space:** O(n)

---

## Problem 10: Keys and Rooms

**Problem Explanation:** There are n rooms numbered 0 to n-1, all locked except room 0 (unlocked). Each room contains keys that unlock other rooms. Determine if you can unlock and visit ALL rooms by collecting keys as you go.

**Algorithm Steps:**
1. Use a DFS/BFS starting from room 0.
2. Maintain a `visited` set (rooms you've entered).
3. When visiting a room, you get its keys. For each key, if that room is not yet visited, add it to the stack/queue to visit.
4. After traversal, check if visited count == n (all rooms visited).

**Visual Walkthrough:** rooms = [[1],[2],[3],[]]
```
Room 0: key to room 1 → visit room 1
Room 1: key to room 2 → visit room 2
Room 2: key to room 3 → visit room 3
Room 3: no keys → done
All 4 rooms visited! → True
```

**Key Insight:** This is a graph traversal problem where rooms are nodes and keys are edges. You start from node 0 and explore reachable nodes.

**Edge Cases:** Single room → True. Room 0 contains no keys but has all keys elsewhere → depends on connectivity.

**Common Mistakes:** Thinking all keys must be found in room 0. Keys can appear later — just maintain a "to-visit" set of discovered but unentered rooms.

**Pattern Recognition:** **Graph Reachability Pattern**: Starting from a source, can we reach all nodes? Used in: Find if Path Exists, Can Visit All Rooms, Open the Lock.

**Statement:** You have n rooms. Room 0 is unlocked. Each room has keys to other rooms. Can you visit all rooms?

**Approach:** DFS/BFS from room 0, count visited rooms.

```python
# canVisitAllRooms: implement solution
def canVisitAllRooms(rooms):
    visited = set([0])
    stack = [0]
    while stack:
        room = stack.pop()
        for key in rooms[room]:
            if key not in visited:
                visited.add(key)
                stack.append(key)
    return len(visited) == len(rooms)
```
**Time:** O(n+e) | **Space:** O(n)

---

## Problem 11: Number of Provinces

**Problem Explanation:** An n x n adjacency matrix `isConnected[i][j] = 1` if city i and city j are directly connected. A province is a group of cities connected directly or indirectly. Count the number of provinces.

**Algorithm Steps:**
1. Maintain a `visited` set.
2. For each unvisited city, start DFS to mark all cities in its province, increment province count.
3. In DFS, visit all neighbors j where `isConnected[node][j] == 1` and j not visited.

**Visual Walkthrough:** isConnected = [[1,1,0],[1,1,0],[0,0,1]]
```
Matrix:    City0  City1  City2
City0:      1      1      0
City1:      1      1      0
City2:      0      0      1

City0 connected to City1 → one province {0,1}
City2 isolated → another province {2}
Return: 2
```

**Key Insight:** The adjacency matrix makes neighbor iteration O(n) per node, but the total is still O(n²). Each DFS call discovers one complete connected component (province).

**Edge Cases:** n=1 → 1 province. All cities isolated → n provinces. Fully connected → 1 province.

**Common Mistakes:** Confusing adjacency matrix index with node value. Not marking visited before recursing.

**Pattern Recognition:** **Matrix Connectivity Pattern**: Count components in adjacency matrix graph. Used in: Friend Circles, Number of Connected Components, Accounts Merge.

**Statement:** Given adjacency matrix of connections, find number of provinces (connected components).

**Approach:** DFS on adjacency matrix.

```python
# findCircleNum: implement solution
def findCircleNum(isConnected):
    n = len(isConnected)
    visited = set()
    def dfs(node):
        visited.add(node)
        for j in range(n):
            if isConnected[node][j] == 1 and j not in visited:
                dfs(j)
    count = 0
    for i in range(n):
        if i not in visited:
            dfs(i)
            count += 1
    return count
```
**Time:** O(n^2) | **Space:** O(n)

---

## Problem 12: Possible Bipartition

**Problem Explanation:** We have n people numbered 1 to n, and a list of dislikes where `[a,b]` means a and b cannot be in the same group. Determine if we can split all people into two groups satisfying all dislikes.

**Algorithm Steps:**
1. Build an undirected graph from dislikes (adjacency list).
2. Use BFS/DFS 2-coloring: assign color 0 to person 1, propagate to neighbors with opposite color.
3. If any neighbor has the same color as current → return False.
4. If all colored without conflict → return True.

**Visual Walkthrough:** n=5, dislikes=[[1,2],[2,3],[3,4],[4,5],[1,5]]
```
Graph edges: 1-2, 2-3, 3-4, 4-5, 1-5 (a pentagon)
Try coloring: 1=0, 2=1, 3=0, 4=1, 5=0
But edge 1-5: both color 0 → conflict!
Return: False (odd cycle exists)
```

**Key Insight:** This is exactly the bipartite graph problem with people as nodes and dislikes as edges. Odd cycles make bipartition impossible.

**Edge Cases:** Single person → always possible. No dislikes → always possible (put everyone in one group).

**Common Mistakes:** People are 1-indexed (not 0-indexed). Must handle disconnected components.

**Pattern Recognition:** **Bipartite Graph Pattern**: Same as Is Graph Bipartite but with explicit dislike edges. Used in: Is Graph Bipartite, Possible Bipartition.

**Statement:** Divide people into two groups such that no two people in same group dislike each other.

**Approach:** Build graph, check bipartite using BFS coloring.

```python
# possibleBipartition: implement solution
def possibleBipartition(n, dislikes):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    for u, v in dislikes:
        graph[u].append(v)
        graph[v].append(u)
    color = [-1] * (n + 1)
    for start in range(1, n + 1):
        if color[start] != -1:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nei in graph[node]:
                if color[nei] == -1:
                    color[nei] = 1 - color[node]
                    queue.append(nei)
                elif color[nei] == color[node]:
                    return False
    return True
```
**Time:** O(n+e) | **Space:** O(n+e)

---

## Problem 13: As Far from Land as Possible

**Problem Explanation:** Given an n x n grid where 1 = land, 0 = water, find the maximum Manhattan distance from any water cell to its nearest land cell. If no land or no water exists, return -1.

**Algorithm Steps:**
1. Multi-source BFS: push all land cells into queue, set their distance = 0.
2. BFS layer by layer, expanding to adjacent water cells.
3. Track distance level (each BFS layer = distance + 1).
4. After BFS completes, the last distance measured is the answer.

**Visual Walkthrough:** grid = [[1,0,0],[0,0,0],[0,0,0]]
```
Initial:           After BFS:
1  0  0           1  1  2
0  0  0    →      1  2  3
0  0  0           2  3  4
Max distance = 4 (bottom-right cell is farthest from any land)
```

**Key Insight:** Multi-source BFS from ALL land simultaneously guarantees each cell gets the shortest distance to the nearest land. The answer is the maximum such distance.

**Edge Cases:** All water → -1. All land → -1. Single land cell → answer is max Manhattan distance from that cell.

**Common Mistakes:** Running BFS from each water cell (O(n⁴)). Using Manhattan distance formula instead of BFS (BFS handles obstacles naturally).

**Pattern Recognition:** **Multi-source BFS Pattern**: Push all sources initially, BFS expands evenly. Used in: Rotting Oranges, Walls and Gates, 01 Matrix.

**Statement:** Grid with 1s (land) and 0s (water). Find max distance from water to nearest land. Return -1 if no water or no land.

**Approach:** Multi-source BFS from all land cells simultaneously.

```python
# maxDistance: implement solution
def maxDistance(grid):
    from collections import deque
    n = len(grid)
    queue = deque()
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                queue.append((i, j))
    if not queue or len(queue) == n*n:
        return -1
    dist = -1
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    while queue:
        dist += 1
        for _ in range(len(queue)):
            x, y = queue.popleft()
            for dx, dy in dirs:
                nx, ny = x+dx, y+dy
                if 0<=nx<n and 0<=ny<n and grid[nx][ny] == 0:
                    grid[nx][ny] = 1
                    queue.append((nx, ny))
    return dist
```
**Time:** O(n^2) | **Space:** O(n^2)

---

## Problem 14: Surrounded Regions

**Problem Explanation:** In a board of 'X' and 'O', flip all 'O' that are completely surrounded by 'X' in all four directions. 'O' on the border or connected to a border 'O' are NOT surrounded and should stay as 'O'.

**Algorithm Steps:**
1. Run DFS from all border 'O's, marking them as 'S' (safe).
2. After marking all safe cells, traverse the entire board.
3. Flip 'O' → 'X' (surrounded), flip 'S' → 'O' (safe border-connected).

**Visual Walkthrough:**
```
Before:            After marking 'S':     Final:
X X X X X         X X X X X             X X X X X
X O O X X         X O O X X             X X X X X
X X O X X         X X O X X             X X X X X
X O X X X    →    X S X X X       →     X O X X X
X X X O X         X X X S X             X X X O X
```

**Key Insight:** Reverse thinking: instead of finding surrounded 'O's, find UNSURROUNDED ones (connected to border). Everything else is surrounded.

**Edge Cases:** No 'O's → nothing to change. All 'O's → all are border-connected, stay 'O'.

**Common Mistakes:** Border cells are at rows 0/m-1 and columns 0/n-1. DFS may overflow (use iterative stack for large boards).

**Pattern Recognition:** **Reverse Border Traversal Pattern**: Start from borders and mark reachable cells. Used in: Pacific Atlantic Water Flow, Number of Enclaves.

**Statement:** Capture all 'O' regions completely surrounded by 'X'. Border 'O's are not captured.

**Approach:** DFS from border 'O's, mark safe. Then flip remaining 'O's to 'X'.

```python
# solve: implement solution
def solve(board):
    if not board: return
    m, n = len(board), len(board[0])
    def dfs(i, j):
        if i<0 or i>=m or j<0 or j>=n or board[i][j]!='O': return
        board[i][j] = 'S'
        dfs(i+1,j); dfs(i-1,j); dfs(i,j+1); dfs(i,j-1)
    for i in range(m):
        dfs(i, 0); dfs(i, n-1)
    for j in range(n):
        dfs(0, j); dfs(m-1, j)
    for i in range(m):
        for j in range(n):
            if board[i][j]=='O': board[i][j]='X'
            elif board[i][j]=='S': board[i][j]='O'
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Problem 15: Number of Enclaves

**Problem Explanation:** Given a binary grid (1 = land, 0 = water), count land cells that are completely surrounded by water and cannot reach the grid's boundary. Only land cells connected to the boundary are considered reachable.

**Algorithm Steps:**
1. Run DFS from all boundary 1s, marking them visited (or turning to 0).
2. After marking all boundary-connected land, count remaining 1s.
3. Return the count of unvisited 1s (enclaves).

**Visual Walkthrough:**
```
Before:            After boundary DFS:
0 1 1 0           0 1 1 0
0 0 1 0     →     0 0 1 0
1 0 0 0           0 0 0 0  ← top-left 1 was reachable, now 0
0 1 1 0           0 1 1 0  ← bottom 1s can't reach boundary
```
Remaining 1s: bottom row → 2 enclaves.

**Key Insight:** This is Surrounded Regions but counting the "captured" cells. Same reverse border traversal technique.

**Edge Cases:** No land → 0. All land → 0 (all can reach boundary). Landlocked interior → count those cells.

**Common Mistakes:** Boundary rows are 0 and m-1, columns 0 and n-1. Forgetting 4-directional connectivity.

**Pattern Recognition:** **Boundary DFS Pattern**: Reverse thinking from border. Used in: Surrounded Regions, Pacific Atlantic Water Flow, Number of Enclaves.

**Statement:** Count 1s (land) that cannot reach boundary of grid.

**Approach:** DFS from boundary 1s, mark reachable. Count remaining 1s.

```python
# numEnclaves: implement solution
def numEnclaves(grid):
    m, n = len(grid), len(grid[0])
    def dfs(i, j):
        if i<0 or i>=m or j<0 or j>=n or grid[i][j]!=1: return
        grid[i][j] = 0
        dfs(i+1,j); dfs(i-1,j); dfs(i,j+1); dfs(i,j-1)
    for i in range(m):
        dfs(i,0); dfs(i,n-1)
    for j in range(n):
        dfs(0,j); dfs(m-1,j)
    return sum(grid[i][j] for i in range(m) for j in range(n))
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Problem 16: Clone Graph

**Problem Explanation:** Given a reference to a node in a connected undirected graph, create a deep copy (entirely new nodes with same connections). The original graph structure must be preserved in the copy.

**Algorithm Steps:**
1. Use a hashmap `visited` mapping original nodes → cloned nodes.
2. DFS from the given node: if node already cloned, return the clone.
3. Create a new Node with the same value, store in visited map.
4. For each neighbor, recursively clone and append to clone's neighbors list.
5. Return the clone of the starting node.

**Visual Walkthrough:** Original: 1 ─ 2 ─ 4, 1 ─ 3
```
DFS(1): create clone1, then:
  DFS(2): create clone2, add clone2 → clone1.neighbors
    DFS(4): create clone4, add clone4 → clone2.neighbors
  DFS(3): create clone3, add clone3 → clone1.neighbors
Result: new independent graph with same structure
```

**Key Insight:** The hashmap is essential — it prevents infinite loops in cycles and ensures each node is cloned exactly once.

**Edge Cases:** None node → return None. Single node with no neighbors → return its clone.

**Common Mistakes:** Not checking `visited` before recursion → stack overflow from cycles. Shallow copy (new node but same neighbor references).

**Pattern Recognition:** **Graph Copy with Hashmap Pattern**: Use map to track original→clone. Used in: Clone Graph, Copy List with Random Pointer.

**Statement:** Deep copy of undirected graph.

**Approach:** DFS + HashMap to map original nodes to copies.

```python
# cloneGraph: implement solution
def cloneGraph(node):
    if not node: return None
    visited = {}
    def dfs(n):
        if n in visited: return visited[n]
        copy = Node(n.val)
        visited[n] = copy
        for nei in n.neighbors:
            copy.neighbors.append(dfs(nei))
        return copy
    return dfs(node)
```
**Time:** O(n+e) | **Space:** O(n)

---

## Problem 17: Number of Operations to Make Network Connected

**Problem Explanation:** You have n computers and ethernet cables (edges). One operation = disconnect a cable and reconnect it elsewhere. Find the minimum operations needed to make all computers connected. If impossible (not enough cables), return -1.

**Algorithm Steps:**
1. If `edges < n-1` → impossible, return -1 (need at least n-1 edges for connectivity).
2. Count connected components using Union-Find or DFS.
3. Answer = components - 1 (need this many cable moves).

**Visual Walkthrough:** n=6, connections=[[0,1],[0,2],[3,4],[2,3]]
```
Graph:  0 ─ 1    3 ─ 4
        │     ╱
        2 ─ 3

Components: 1 ({0,1,2,3,4}) and 1 isolated ({5}) = 2 components
Edges: 4, n-1=5 → can't connect. Wait, 4>=5? No → actually 4<5, so impossible.
Return -1.

Let's check edges=[[0,1],[0,2],[0,3],[1,2],[3,4]]:
Components: {0,1,2,3} and {4} = 2 components
Need: 2-1 = 1 operation
```

**Key Insight:** For connecting k components, you need exactly k-1 cables. Count extra cables and components separately.

**Edge Cases:** n=1 → 0 operations. Already connected → 0. Not enough cables (edges < n-1) → -1.

**Common Mistakes:** Forgetting to check if total edges < n-1 first. Thinking you need more operations than components-1.

**Pattern Recognition:** **Union-Find Component Counting Pattern**: Components - 1 = minimum connections needed. Used in: Number of Connected Components, Make Network Connected, Connecting Cities.

**Statement:** Given n computers and cables, find min operations to connect all. One operation = remove a cable and connect to another.

**Approach:** Need (components-1) cables to connect. Count extra cables and components.

```python
# makeConnected: implement solution
def makeConnected(n, connections):
    if len(connections) < n - 1: return -1
    class UF:
        def __init__(self,n): self.p=list(range(n)); self.r=[0]*n; self.c=n
        def find(self,x):
            if self.p[x]!=x: self.p[x]=self.find(self.p[x])
            return self.p[x]
        def union(self,x,y):
            px,py=self.find(x),self.find(y)
            if px==py: return False
            if self.r[px]<self.r[py]: px,py=py,px
            self.p[py]=px
            if self.r[px]==self.r[py]: self.r[px]+=1
            self.c-=1
            return True
    uf = UF(n)
    for u,v in connections:
        uf.union(u,v)
    return uf.c - 1
```
**Time:** O(e*α(n)) | **Space:** O(n)

---

## Problem 18: Find the City With Smallest Number of Neighbors

**Problem Explanation:** You have n cities connected by weighted edges. A city is "reachable" from another if the shortest path distance ≤ distanceThreshold. Find the city that can reach the fewest other cities. If multiple, return the one with the largest city number.

**Algorithm Steps:**
1. Use Floyd-Warshall to compute all-pairs shortest paths.
2. For each city i, count how many cities j have `dist[i][j] <= distanceThreshold`.
3. Track the city with the minimum count, using larger city ID as tiebreaker.
4. Return that city.

**Visual Walkthrough:** n=4, edges=[[0,1,3],[1,2,1],[1,3,4],[2,3,1]], distanceThreshold=4
```
Floyd-Warshall all-pairs distances:
        0  1  2  3
    0   0  3  4  5
    1   3  0  1  2
    2   4  1  0  1
    3   5  2  1  0

City 0: ≤4 → {0,1,2} = 3 cities
City 1: ≤4 → {0,1,2,3} = 4 cities
City 2: ≤4 → {0,1,2,3} = 4 cities
City 3: ≤4 → {1,2,3} = 3 cities
Answer: max(0,3) = 3 (tie between 0 and 3, pick larger)
```

**Key Insight:** All-pairs shortest paths needed because any city could be the starting point. Floyd-Warshall (O(n³)) works for n ≤ 500.

**Edge Cases:** All cities isolated → each city reaches 0 others, return largest city. Single city → return 0.

**Common Mistakes:** Forgetting diagonal distances (dist[i][i]=0) which counts the city itself as reachable. Tie-breaker is larger city number.

**Pattern Recognition:** **All-Pairs Shortest Path Pattern**: When you need distances between ALL pairs, use Floyd-Warshall. Used in: City With Smallest Neighbors, Network Delay Time variant.

**Statement:** Find city with smallest number of cities reachable within threshold distance. Tie-break: larger city number.

**Approach:** Floyd-Warshall or Dijkstra from each city.

```python
# findTheCity: implement solution
def findTheCity(n, edges, distanceThreshold):
    dist = [[float('inf')]*n for _ in range(n)]
    for i in range(n): dist[i][i] = 0
    for u,v,w in edges:
        dist[u][v] = dist[v][u] = w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k]+dist[k][j])
    min_reachable = n
    result = -1
    for i in range(n):
        count = sum(1 for j in range(n) if dist[i][j] <= distanceThreshold)
        if count <= min_reachable:
            min_reachable = count
            result = i
    return result
```
**Time:** O(n^3) | **Space:** O(n^2)

---

## Problem 19: Keys and Rooms (BFS)

**Problem Explanation:** Same as Problem 10 — determine if you can visit all rooms starting from room 0. This version uses BFS (iterative queue) instead of DFS/stack.

**Algorithm Steps:**
1. Initialize `visited = {0}`, `queue = [0]`.
2. While queue: pop room, add all its keys that lead to unvisited rooms.
3. After BFS, return `len(visited) == len(rooms)`.

**Key Insight:** BFS explores rooms level-by-level (by number of key-collections), but since all edges cost 1, both BFS and DFS work identically for reachability.

**Edge Cases:** Single room → visited={0} → True. Room 0 locked (but spec says it's unlocked).

**Common Mistakes:** Same as Problem 10. BFS/DFS choice doesn't matter for reachability.

**Pattern Recognition:** **Graph Reachability (BFS)**: BFS finds if all nodes reachable from source. Used in: Same as Problem 10.

```python
# canVisitAllRooms: implement solution
def canVisitAllRooms(rooms):
    from collections import deque
    visited = {0}
    queue = deque([0])
    while queue:
        room = queue.popleft()
        for key in rooms[room]:
            if key not in visited:
                visited.add(key)
                queue.append(key)
    return len(visited) == len(rooms)
```
**Time:** O(n+e) | **Space:** O(n)

---

## Problem 20: Shortest Path in Binary Matrix

**Problem Explanation:** Given an n x n binary grid (0 = open, 1 = blocked), find the shortest path from (0,0) to (n-1,n-1). You can move in all 8 directions. Return the path length (number of cells visited) or -1 if no path exists.

**Algorithm Steps:**
1. If start or end is blocked → return -1.
2. BFS from (0,0) with distance = 1 (counts the starting cell).
3. Mark visited cells by setting grid to 1.
4. When reaching (n-1,n-1), return distance.

**Visual Walkthrough:** grid = [[0,0,0],[1,1,0],[1,1,1]]
```
Grid:     BFS distances:
0 0 0     1 2 3
1 1 0  →  - - 4
1 1 1     - - -

(0,0)→(0,1)→(0,2)→(1,2)→(2,2) = 4 steps
Or diagonal: (0,0)→(1,1) is blocked
Shortest = 4
```

**Key Insight:** 8-directional movement means diagonal steps cost 1, same as orthogonal. BFS finds shortest path because the graph is unweighted.

**Edge Cases:** Start or end blocked → -1. n=1 grid[0][0]=0 → return 1. n=1 grid[0][0]=1 → -1.

**Common Mistakes:** Using DFS (won't find shortest). Forgetting 8 directions (only using 4).

**Pattern Recognition:** **Grid BFS Pattern**: Shortest path in unweighted grid. Used in: Minimum Path Sum, Shortest Path in Grid with Obstacles, The Maze.

**Statement:** Find shortest path from top-left to bottom-right in binary grid (8 directions). Return length or -1.

**Approach:** BFS on grid (unweighted, BFS gives shortest path).

```python
# shortestPathBinaryMatrix: implement solution
def shortestPathBinaryMatrix(grid):
    from collections import deque
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1: return -1
    queue = deque([(0, 0, 1)])
    grid[0][0] = 1
    dirs = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    while queue:
        x, y, d = queue.popleft()
        if x == n-1 and y == n-1: return d
        for dx,dy in dirs:
            nx,ny = x+dx, y+dy
            if 0<=nx<n and 0<=ny<n and grid[nx][ny]==0:
                grid[nx][ny] = 1
                queue.append((nx,ny,d+1))
    return -1
```
**Time:** O(n^2) | **Space:** O(n^2)

---

## Problem 21: Number of Islands

**Problem Explanation:** Given a 2D grid of '1' (land) and '0' (water), count the number of islands. An island is surrounded by water and formed by connecting adjacent lands horizontally or vertically (4-directional).

**Algorithm Steps:**
1. Iterate through every cell in the grid.
2. When '1' is found, increment count and start DFS to mark the entire island as visited (set to '0').
3. DFS visits all 4-directional neighbors that are '1'.
4. Return count after processing all cells.

**Visual Walkthrough:** grid = [["1","1","0"],["1","0","1"],["0","0","1"]]
```
1 1 0     0 0 0     Island 1 found at (0,0), DFS sinks it
1 0 1  →  0 0 1     Island 2 found at (1,2), DFS sinks it
0 0 1     0 0 0     Wait (2,2) was part of island 2's DFS
Number of islands = 2
```

**Key Insight:** Each DFS call discovers one complete island. Sinking visited land avoids recounting the same island.

**Edge Cases:** Empty grid → 0. All water → 0. All land → 1.

**Common Mistakes:** Only checking 4 directions (not 8). Not handling grid boundaries.

**Pattern Recognition:** **Grid Component Counting Pattern**: Count connected components in grid. Used in: Max Area of Island, Number of Enclaves, Surrounded Regions.

**Statement:** Count islands in 2D grid ('1' land, '0' water).

**Approach:** DFS/BFS to mark connected land.

```python
# numIslands: implement solution
def numIslands(grid):
    if not grid: return 0
    count = 0
    m, n = len(grid), len(grid[0])
    def dfs(i, j):
        if i<0 or i>=m or j<0 or j>=n or grid[i][j]!='1': return
        grid[i][j] = '0'
        dfs(i+1,j); dfs(i-1,j); dfs(i,j+1); dfs(i,j-1)
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                dfs(i, j)
                count += 1
    return count
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Problem 22: Flood Fill

**Problem Explanation:** An image is an m x n grid of pixels. Starting from (sr, sc), replace its color and all adjacent pixels of the same original color with the new color (like the paint bucket tool).

**Algorithm Steps:**
1. Get the original color at (sr, sc). If it's the same as new color, return image (no change).
2. DFS from (sr, sc): change color, then recurse on 4-directional neighbors with the same original color.

**Visual Walkthrough:** image = [[1,1,1],[1,1,0],[1,0,1]], sr=1, sc=1, newColor=2
```
Before:      After DFS:
1 1 1        2 2 2
1 1 0   →    2 2 0
1 0 1        2 0 1
```

**Key Insight:** The early return when `old == newColor` prevents infinite recursion since there's no visited set.

**Edge Cases:** Starting pixel with same color → no change. Single pixel grid.

**Common Mistakes:** Not checking pixel match before recursing. Not returning early when old==new (stack overflow).

**Pattern Recognition:** **Grid DFS Pixel Fill Pattern**: Flood fill via DFS from seed. Used in: Same as Problem 21 (Number of Islands variant).

**Statement:** Replace all connected pixels of same color with new color.

**Approach:** DFS from starting pixel.

```python
# floodFill: implement solution
def floodFill(image, sr, sc, newColor):
    m, n = len(image), len(image[0])
    old = image[sr][sc]
    if old == newColor: return image
    def dfs(i, j):
        if i<0 or i>=m or j<0 or j>=n or image[i][j]!=old: return
        image[i][j] = newColor
        dfs(i+1,j); dfs(i-1,j); dfs(i,j+1); dfs(i,j-1)
    dfs(sr, sc)
    return image
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Problem 23: Rotting Oranges

**Problem Explanation:** In an m x n grid, 0 = empty, 1 = fresh orange, 2 = rotten orange. Each minute, any fresh orange 4-directionally adjacent to a rotten one becomes rotten. Return minutes until all are rotten, or -1 if impossible.

**Algorithm Steps:**
1. Count fresh oranges. Push all initially rotten oranges into BFS queue.
2. BFS level by level — each level = 1 minute.
3. When a fresh orange rots, decrement fresh count, add to queue.
4. After BFS, if fresh == 0 return minutes, else return -1.

**Visual Walkthrough:** grid = [[2,1,1],[1,1,0],[0,1,1]]
```
Minute 0:  2 1 1    Minute 1:  2 2 1    Minute 2:  2 2 2
           1 1 0               2 2 0               2 2 0
           0 1 1               0 1 1               0 2 2
All rotten after 2 minutes. But wait:
Minute 3:  2 2 2    → still fresh at (1,2)? No.
           2 2 0    Actually all rot by minute 2.
           0 2 2    Answer: 2
```

**Key Insight:** Multi-source BFS perfectly models the simultaneous rotting process. Each BFS layer = 1 minute of rotting.

**Edge Cases:** No fresh oranges → 0. Fresh oranges unreachable from any rotten → -1.

**Common Mistakes:** Not counting fresh oranges initially. Off-by-one on minutes (incrementing before processing first level).

**Pattern Recognition:** **Multi-source BFS (Time Propagation)**: Spread from multiple sources level by level. Used in: As Far from Land as Possible, Walls and Gates, 01 Matrix.

**Statement:** Find minutes until all fresh oranges rot. Each minute, adjacent fresh oranges rot.

**Approach:** Multi-source BFS from all rotten oranges.

```python
# orangesRotting: implement solution
def orangesRotting(grid):
    from collections import deque
    m, n = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 2: queue.append((i,j))
            elif grid[i][j] == 1: fresh += 1
    if fresh == 0: return 0
    minutes = 0
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    while queue:
        minutes += 1
        for _ in range(len(queue)):
            x,y = queue.popleft()
            for dx,dy in dirs:
                nx,ny = x+dx, y+dy
                if 0<=nx<m and 0<=ny<n and grid[nx][ny]==1:
                    grid[nx][ny] = 2
                    fresh -= 1
                    queue.append((nx,ny))
    return minutes-1 if fresh==0 else -1
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Problem 24: Pacific Atlantic Water Flow

**Problem Explanation:** Given an m x n grid of heights, water flows from a cell to adjacent cells of equal or lower height. The Pacific ocean touches the top and left borders, Atlantic touches the bottom and right borders. Find all cells where water can flow to both oceans.

**Algorithm Steps:**
1. Reverse thinking: start from ocean borders and flow INWARD only to cells with height ≥ current cell.
2. Run DFS from all Pacific border cells, marking reachable cells in a `pacific` set.
3. Run DFS from all Atlantic border cells, marking reachable cells in an `atlantic` set.
4. Return the intersection of both sets.

**Visual Walkthrough:** grid = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
```
Pacific ← top row and left column
Atlantic ← bottom row and right column
Reverse DFS from Pacific borders marks cells that can reach Pacific.
Reverse DFS from Atlantic borders marks cells that can reach Atlantic.
Intersection = [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
```

**Key Insight:** Reverse DFS is the key insight — finding where water CAN flow FROM a cell is hard, but finding which cells CAN REACH an ocean (reverse flow) is easy: start from the ocean and move inward following height ≥ current.

**Edge Cases:** Single cell → both oceans reachable (touches all borders). Varying heights.

**Common Mistakes:** Using forward flow (from cell to ocean) is O(n²) BFS per cell. Reverse approach is O(m*n).

**Pattern Recognition:** **Reverse Boundary Flow Pattern**: DFS from borders inward with reverse height condition. Used in: Surrounded Regions, Number of Enclaves.

**Statement:** Find cells where water can flow to both Pacific (top/left) and Atlantic (bottom/right) oceans.

**Approach:** Reverse DFS from both oceans, find intersection.

```python
# pacificAtlantic: implement solution
def pacificAtlantic(grid):
    if not grid: return []
    m, n = len(grid), len(grid[0])
    pacific = set()
    atlantic = set()
    def dfs(i, j, prev, visited):
        if i<0 or i>=m or j<0 or j>=n or (i,j) in visited or grid[i][j]<prev: return
        visited.add((i,j))
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            dfs(i+dx,j+dy,grid[i][j],visited)
    for i in range(m):
        dfs(i,0,0,pacific); dfs(i,n-1,0,atlantic)
    for j in range(n):
        dfs(0,j,0,pacific); dfs(m-1,j,0,atlantic)
    return list(pacific & atlantic)
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Problem 25: Walls and Gates

**Problem Explanation:** Given an m x n grid where INF = empty room (2147483647), 0 = gate, -1 = wall. Fill each empty room with its shortest distance to the nearest gate. If unreachable, leave as INF.

**Algorithm Steps:**
1. Push all gate positions (value 0) into BFS queue.
2. BFS: for each cell, check 4-directional neighbors.
3. If neighbor is INF (empty), set its value to current cell's value + 1, push to queue.
4. BFS ensures each room gets its shortest distance.

**Visual Walkthrough:**
```
Before:           After BFS:
INF -1  0  INF    3  -1   0   1
INF INF INF -1  → 2   2   1  -1
INF -1 INF -1     1  -1   2  -1
0   -1 INF INF    0  -1   3   4
```

**Key Insight:** Multi-source BFS from all gates simultaneously ensures every room is filled with the distance from the nearest gate in one pass.

**Edge Cases:** Empty grid. No gates → all remain INF. No empty rooms → nothing to fill.

**Common Mistakes:** Running BFS from each gate separately (O(gates * m * n)). Forgetting to check neighbor is INF before updating.

**Pattern Recognition:** **Multi-source BFS (Distance Fill)**: Fill distances from multiple sources simultaneously. Used in: As Far from Land as Possible, Rotting Oranges, 01 Matrix.

**Statement:** Fill each empty room with distance to nearest gate. Empty = INF, Gate = 0, Wall = -1.

**Approach:** Multi-source BFS from all gates.

```python
# wallsAndGates: implement solution
def wallsAndGates(rooms):
    from collections import deque
    m, n = len(rooms), len(rooms[0])
    queue = deque()
    for i in range(m):
        for j in range(n):
            if rooms[i][j] == 0: queue.append((i,j))
    while queue:
        x,y = queue.popleft()
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx,ny = x+dx, y+dy
            if 0<=nx<m and 0<=ny<n and rooms[nx][ny]==2147483647:
                rooms[nx][ny] = rooms[x][y]+1
                queue.append((nx,ny))
```
**Time:** O(m*n) | **Space:** O(m*n)

---

## Problem 26: Redundant Connection

**Problem Explanation:** A tree has n nodes and n-1 edges. If one extra edge is added, a cycle forms. Find the edge that can be removed to restore the graph to a tree. If multiple answers, return the last edge in the input.

**Algorithm Steps:**
1. Initialize Union-Find with n+1 nodes (1-indexed).
2. Process each edge [u,v] in order:
   - If u and v are already connected → this edge creates a cycle → return [u,v].
   - Otherwise, union(u, v).

**Visual Walkthrough:** edges = [[1,2],[1,3],[2,3]]
```
Process [1,2]: union 1-2
Process [1,3]: union 1-3 (1 connected to 2, so 2-3 connects)
Process [2,3]: find(2)=1, find(3)=1 → already connected! Return [2,3]
```

**Key Insight:** In Union-Find, if both endpoints of an edge are already in the same set, this edge completes a cycle.

**Edge Cases:** n=1 no edges. Multiple valid answers → return the last one in input (since we process in order).

**Common Mistakes:** Not 1-indexing (nodes are 1..n). Finding the wrong edge — the one that completes the cycle, not the first edge in the cycle.

**Pattern Recognition:** **Union-Find Cycle Detection Pattern**: Detect cycle in undirected graph using UF. Used in: Number of Operations to Make Network Connected, Accounts Merge.

**Statement:** Find edge that creates cycle when added to tree.

**Approach:** Union-Find. Edge where both nodes already connected is the answer.

```python
# findRedundantConnection: implement solution
def findRedundantConnection(edges):
    class UF:
        def __init__(self,n): self.p=list(range(n+1))
        def find(self,x):
            if self.p[x]!=x: self.p[x]=self.find(self.p[x])
            return self.p[x]
        def union(self,x,y):
            px,py=self.find(x),self.find(y)
            if px==py: return False
            self.p[py]=px; return True
    uf = UF(len(edges))
    for u,v in edges:
        if not uf.union(u,v):
            return [u,v]
```
**Time:** O(e*α(n)) | **Space:** O(n)

---

## Problem 27: Accounts Merge

**Problem Explanation:** Given a list of accounts where each account has a name and email addresses, merge accounts that share any common email. Two accounts belong to the same person if they share at least one email.

**Algorithm Steps:**
1. Map each email to a unique ID and record its owner name.
2. Union emails within the same account (union first email with each subsequent email).
3. After all unions: group emails by root ID using a hashmap.
4. Return `[[name] + sorted(emails) for each group]`.

**Visual Walkthrough:** accounts = [["John","j1","j2"],["John","j2","j3"],["Mary","m1"]]
```
Email IDs: j1→0, j2→1, j3→2, m1→3
Account 0: union(0,1) → j1,j2 connected
Account 1: union(1,2) → j1,j2,j3 all connected
Account 2: union(3,3) (only one email) → m1 alone
Groups: {0: {j1,j2,j3}, 3: {m1}}
Output: [["John","j1","j2","j3"], ["Mary","m1"]]
```

**Key Insight:** Union-Find connects emails within each account. If two accounts share even one email, their email groups merge via UF's transitive property.

**Edge Cases:** Name collisions (same names different people) — emails prevent merging. Single email accounts.

**Common Mistakes:** Using names to group (names aren't unique). Not sorting emails within each group.

**Pattern Recognition:** **Union-Find on Emails Pattern**: Connect items that should be grouped together. Used in: Number of Provinces, Redundant Connection.

**Statement:** Merge accounts that share common emails.

**Approach:** Union-Find on email indices. Group emails by owner.

```python
# accountsMerge: implement solution
def accountsMerge(accounts):
    from collections import defaultdict
    email_to_id = {}
    email_to_name = {}
    id_counter = 0
    for account in accounts:
        name = account[0]
        for email in account[1:]:
            email_to_name[email] = name
            if email not in email_to_id:
                email_to_id[email] = id_counter
                id_counter += 1
    class UF:
        def __init__(self,n): self.p=list(range(n))
        def find(self,x):
            if self.p[x]!=x: self.p[x]=self.find(self.p[x])
            return self.p[x]
        def union(self,x,y):
            px,py=self.find(x),self.find(y)
            if px!=py: self.p[py]=px
    uf = UF(id_counter)
    for account in accounts:
        first = email_to_id[account[1]]
        for email in account[2:]:
            uf.union(first, email_to_id[email])
    groups = defaultdict(set)
    for email, eid in email_to_id.items():
        groups[uf.find(eid)].add(email)
    return [[email_to_name[next(iter(emails))]] + sorted(emails) for emails in groups.values()]
```
**Time:** O(n*k*log(n*k)) | **Space:** O(n*k)

---

## Problem 28: Course Schedule

**Problem Explanation:** There are numCourses courses labeled 0 to n-1. Prerequisites are given as [course, prereq] pairs. Determine if it's possible to finish all courses (no cyclic dependencies).

**Algorithm Steps:**
1. Build adjacency list from prerequisites.
2. Use DFS with 3-color state: 0=unvisited, 1=visiting (in current DFS path), 2=visited (processed).
3. For each unvisited course, DFS: if neighbor state is 1 → cycle found → return False.
4. If all courses visited without cycles → return True.

**Visual Walkthrough:** numCourses=4, prerequisites=[[1,0],[2,1],[3,2],[1,3]]
```
Graph: 0 → 1 → 2 → 3
            ↑         ↓
            ←─────────
DFS from 0: visit 0→1→2→3→1 (state[1]==1 visiting!) → cycle! → False
```

**Key Insight:** State 1 (visiting) detects back edges in DFS traversal of a directed graph. A back edge means a cycle.

**Edge Cases:** No prerequisites → True. Single course → True. Self-loop → False.

**Common Mistakes:** Building graph in wrong direction. Not using proper state management (visited set alone doesn't detect cycles in directed graphs).

**Pattern Recognition:** **DFS Cycle Detection Pattern**: 3-color DFS for directed cycle detection. Used in: Course Schedule II, Alien Dictionary.

**Statement:** Can you finish all courses? (Cycle detection in directed graph)

**Approach:** DFS with state array (0=unvisited, 1=visiting, 2=visited).

```python
# canFinish: implement solution
def canFinish(numCourses, prerequisites):
    from collections import defaultdict
    graph = defaultdict(list)
    for u,v in prerequisites: graph[v].append(u)
    state = [0] * numCourses
    def dfs(node):
        state[node] = 1
        for nei in graph[node]:
            if state[nei] == 1: return False
            if state[nei] == 0 and not dfs(nei): return False
        state[node] = 2
        return True
    return all(dfs(i) for i in range(numCourses) if state[i]==0)
```
**Time:** O(n+e) | **Space:** O(n+e)

---

## Problem 29: Course Schedule II

**Problem Explanation:** Same prerequisites setup as Course Schedule, but now return the ordering of courses (a topological order) that satisfies all prerequisites. If impossible (cycle exists), return empty list.

**Algorithm Steps:**
1. Build adjacency list and indegree array.
2. Kahn's algorithm: push all courses with indegree 0 to queue.
3. Process queue: pop course, add to order, decrement indegree of neighbors, push neighbors with indegree 0.
4. If len(order) == numCourses → return order, else return [].

**Visual Walkthrough:** numCourses=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]]
```
Graph: 0 → 1 → 3
       0 → 2 → 3
Indegrees: [0, 1, 1, 2]
Queue initially: [0]
Process 0 → order=[0], indeg[1]=0, indeg[2]=0 → queue=[1,2]
Process 1 → order=[0,1], indeg[3]=1
Process 2 → order=[0,1,2], indeg[3]=0 → queue=[3]
Process 3 → order=[0,1,2,3]
Return [0,1,2,3] (also valid: [0,2,1,3])
```

**Key Insight:** Kahn's algorithm indegree counts are prerequisites. When indegree hits 0, all prerequisites are satisfied.

**Edge Cases:** No prerequisites → any order (e.g., [0,1,2,...]). Cycle → return [].

**Common Mistakes:** Not handling all nodes having prerequisites (graph must have at least one source node). Building adjacency in wrong direction.

**Pattern Recognition:** **Topological Sort (Kahn's) Pattern**: Indegree-based BFS for DAG ordering. Used in: Course Schedule, Alien Dictionary, Parallel Courses.

**Statement:** Return ordering to finish all courses. Return empty if impossible.

**Approach:** Topological sort using DFS or Kahn's.

```python
# findOrder: implement solution
def findOrder(numCourses, prerequisites):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    indeg = [0]*numCourses
    for u,v in prerequisites:
        graph[v].append(u); indeg[u]+=1
    queue = deque([i for i in range(numCourses) if indeg[i]==0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nei in graph[node]:
            indeg[nei]-=1
            if indeg[nei]==0: queue.append(nei)
    return order if len(order)==numCourses else []
```
**Time:** O(n+e) | **Space:** O(n+e)

---

## Problem 30: Network Delay Time

**Problem Explanation:** A network has n nodes and weighted directed edges (times: [u, v, w] = time w for signal to travel u→v). A signal starts from node k. Find the minimum time for ALL nodes to receive the signal. If any node is unreachable, return -1.

**Algorithm Steps:**
1. Build adjacency list `graph[u] = [(v, w)]`.
2. Run Dijkstra from k: maintain min distances using a min-heap.
3. After Dijkstra completes, the answer is the maximum distance among all reachable nodes.
4. If not all nodes reached (len(dist) < n), return -1.

**Visual Walkthrough:** times=[[2,1,1],[2,3,1],[3,4,1]], n=4, k=2
```
Graph: 2 → 1 (1), 2 → 3 (1), 3 → 4 (1)
Dijkstra from 2:
  dist = {2:0}
  Process 2 → update 1(1), 3(1) → heap=[(1,1),(1,3)]
  Process 1 → no outgoing edges
  Process 3 → update 4(2) → heap=[(2,4)]
  Process 4 → no outgoing edges
  dist = {2:0, 1:1, 3:1, 4:2}
Max dist = 2 → answer: 2
```

**Key Insight:** Dijkstra finds shortest paths from a single source to all nodes. The maximum of these shortest paths is the time for the last node to receive the signal.

**Edge Cases:** n=1 → 0. Source disconnected from some nodes → -1. Negative weights (won't occur if constraints say non-negative).

**Common Mistakes:** Not skipping stale heap entries (if d > dist[node], continue). Using BFS on weighted graph.

**Pattern Recognition:** **Single Source Shortest Path (Dijkstra) Pattern**: Min-heap based shortest path. Used in: Cheapest Flights Within K Stops (variant), Path with Maximum Probability.

**Statement:** Time for signal from source to reach all nodes.

**Approach:** Dijkstra's shortest path, return max distance.

```python
# networkDelayTime: implement solution
def networkDelayTime(times, n, k):
    import heapq
    from collections import defaultdict
    graph = defaultdict(list)
    for u,v,w in times: graph[u].append((v,w))
    dist = {k: 0}
    heap = [(0, k)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist.get(node, float('inf')): continue
        for nei, w in graph[node]:
            nd = d + w
            if nd < dist.get(nei, float('inf')):
                dist[nei] = nd
                heapq.heappush(heap, (nd, nei))
    return max(dist.values()) if len(dist)==n else -1
```
**Time:** O(e*log(e)) | **Space:** O(n+e)

---

## Problem 31: Cheapest Flights Within K Stops

**Problem Explanation:** There are n cities connected by flights [from, to, price]. Find the cheapest price from src to dst with at most k stops (k+1 legs total). Return -1 if no such route exists.

**Algorithm Steps:**
1. Initialize `prices` array with INF, `prices[src] = 0`.
2. Iterate k+1 times (allowing up to k stops):
   - Copy prices to `temp`.
   - For each flight [u,v,w]: if prices[u] + w < temp[v], update temp[v].
   - Set prices = temp.
3. Return prices[dst] if not INF, else -1.

**Visual Walkthrough:** n=4, flights=[[0,1,100],[1,2,100],[2,3,100],[0,2,500]], src=0, dst=3, k=1
```
Iteration 0 (0 stops allowed):
  prices = [0, INF, INF, INF]
Iteration 1 (at most 1 stop):
  temp = [0, 100, 500, INF]
  → 0→1=100, 0→2=500
  prices = [0, 100, 500, INF]
Iteration 2 (at most 2 stops):
  temp = [0, 100, 200, 600]
  → 1→2=200(100+100), 2→3=600(500+100)
  prices = [0, 100, 200, 600]
At k=1 (stop at city 1): 0→1→2→3 = 3 stops, too many
At k=1: only 0→2→3 possible, but flight 2→3 not priced yet in first pass
Answer: 500 (0→2→3 is not available, need more stops)
Wait, with k=1, we can check: 0→1→2→3 needs 2 stops (cities 1 and 2).
0→2→3 needs 1 stop (city 2). So answer is 500.
```

**Key Insight:** Bellman-Ford variant that limits path length. Each iteration adds exactly one more edge to the path. The `temp` copy ensures we don't use multiple edges beyond the current iteration limit.

**Edge Cases:** src == dst → 0. No path within k stops → -1. k=0 → direct flight only.

**Common Mistakes:** Not using temp copy (using same array allows using more than k stops). Forgetting to check INF before adding.

**Pattern Recognition:** **Bellman-Ford (K-Stops) Pattern**: Iterative DP with level limiting. Used in: Network Delay Time variant, Minimum Cost to Reach Destination.

**Statement:** Find cheapest price from src to dst with at most k stops.

**Approach:** Bellman-Ford variant or BFS with stops tracking.

```python
# findCheapestPrice: implement solution
def findCheapestPrice(n, flights, src, dst, k):
    prices = [float('inf')] * n
    prices[src] = 0
    for _ in range(k + 1):
        temp = prices[:]
        for u, v, w in flights:
            if prices[u] + w < temp[v]:
                temp[v] = prices[u] + w
        prices = temp
    return prices[dst] if prices[dst] != float('inf') else -1
```
**Time:** O(k*e) | **Space:** O(n)

---

## Problem 32: Alien Dictionary

**Problem Explanation:** Given a sorted list of words from an alien language, use the order to determine the character ordering (lexicographical rules). The words are sorted lexicographically according to some unknown order of the alphabet. Return the order as a string. If invalid, return "".

**Algorithm Steps:**
1. Build graph from adjacent word comparisons: for each pair (w1, w2), find first mismatched character c1, c2 → edge c1→c2 (c1 comes before c2).
2. If w1 is a prefix of w2 and longer → invalid, return "".
3. Run topological sort (Kahn's) on the graph.
4. If result length < total unique characters → cycle detected → return "".

**Visual Walkthrough:** words = ["wrt","wrf","er","ett","rftt"]
```
Compare "wrt" vs "wrf": t→f
Compare "wrf" vs "er":  w→e
Compare "er" vs "ett":  r→t
Compare "ett" vs "rftt": e→r
Graph: t→f, w→e, r→t, e→r
Topological: w→e→r→t→f
Answer: "wertf"
```

**Key Insight:** Only the first differing character between adjacent words gives ordering information. If word A is prefix of B and A comes before B, no info; if A is longer and prefix of B → invalid.

**Edge Cases:** All words identical → any order (return all unique chars). Cycle in character graph → return "".

**Common Mistakes:** Comparing non-adjacent words (only adjacent words are guaranteed to be sorted). Not handling the prefix edge case (w1="abc", w2="ab" is invalid).

**Pattern Recognition:** **Topological Sort (Character Graph) Pattern**: Build order from pairwise comparisons. Used in: Course Schedule II, Reconstruct Itinerary (variant).

**Statement:** Derive character order from sorted list of words.

**Approach:** Build graph from adjacent character comparisons, topological sort.

```python
# alienOrder: implement solution
def alienOrder(words):
    from collections import defaultdict, deque
    graph = defaultdict(set)
    indeg = {c:0 for word in words for c in word}
    for i in range(len(words)-1):
        w1, w2 = words[i], words[i+1]
        if len(w1) > len(w2) and w1.startswith(w2):
            return ""
        for c1, c2 in zip(w1, w2):
            if c1 != c2 and c2 not in graph[c1]:
                graph[c1].add(c2)
                indeg[c2] += 1
    queue = deque([c for c in indeg if indeg[c]==0])
    result = []
    while queue:
        c = queue.popleft()
        result.append(c)
        for nei in graph[c]:
            indeg[nei] -= 1
            if indeg[nei] == 0:
                queue.append(nei)
    return "".join(result) if len(result)==len(indeg) else ""
```
**Time:** O(n*m) | **Space:** O(1) limited by alphabet

---

## Problem 33: Swim in Rising Water

**Problem Explanation:** In an n x n grid where each cell has an elevation, you can swim from a cell to adjacent ones (4-directional). The time to swim = the maximum elevation encountered along the path. Find the minimum possible time (minimum possible maximum elevation) from (0,0) to (n-1,n-1).

**Algorithm Steps:**
1. Use Dijkstra-like approach with a min-heap: `(max_elevation, x, y)`.
2. Start from (0,0) with max_elevation = grid[0][0].
3. For each neighbor: new_max = max(current_max, neighbor_elevation).
4. Push (new_max, nx, ny) to heap if not visited.
5. When reaching (n-1,n-1), return the max_elevation.

**Visual Walkthrough:** grid = [[0,2],[1,3]]
```
Paths:
(0,0)→(0,1)→(1,1): max(0,2,3) = 3
(0,0)→(1,0)→(1,1): max(0,1,3) = 3
Both paths have max elevation 3 → answer: 3
```

**Key Insight:** This is a minimax path problem — find path minimizing the maximum edge/node weight. Dijkstra's greedy property still works: the first time we pop a cell from heap, we have the minimal possible maximum elevation for that cell.

**Edge Cases:** n=1 → return grid[0][0]. Single cell path.

**Common Mistakes:** Using sum (Dijkstra) instead of max (minimax). Not checking visited before processing.

**Pattern Recognition:** **Minimax Path Pattern**: Dijkstra with max instead of sum. Used in: Path with Maximum Minimum Value, The Maze II, Find the Safest Path.

**Statement:** Find minimum time to swim from (0,0) to (n-1,n-1). Grid[i][j] = elevation, time = max elevation along path.

**Approach:** Binary search + BFS/DFS, or Dijkstra.

```python
# swimInWater: implement solution
def swimInWater(grid):
    import heapq
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]
    visited = {(0,0)}
    while heap:
        t, x, y = heapq.heappop(heap)
        if x==n-1 and y==n-1: return t
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx,ny = x+dx, y+dy
            if 0<=nx<n and 0<=ny<n and (nx,ny) not in visited:
                visited.add((nx,ny))
                heapq.heappush(heap, (max(t,grid[nx][ny]),nx,ny))
    return -1
```
**Time:** O(n^2*log(n^2)) | **Space:** O(n^2)

---

## Problem 34: Path with Maximum Probability

**Problem Explanation:** Given an undirected weighted graph where edge weights are success probabilities (0 to 1), find the path from start to end that maximizes the product of probabilities along the path.

**Algorithm Steps:**
1. Build adjacency list with probabilities.
2. Use max-heap (store negative probabilities) or min-heap with maximization logic.
3. Start with `dist[start] = 1.0`.
4. For each node, update neighbor: `new_prob = prob[node] * edge_prob`.
5. If `new_prob > dist[nei]`, update and push to heap.
6. Return `dist[end]` or 0.0 if unreachable.

**Visual Walkthrough:** n=3, edges=[[0,1],[1,2],[0,2]], succProb=[0.5,0.5,0.2], start=0, end=2
```
Paths:
0→2: prob = 0.2
0→1→2: prob = 0.5 * 0.5 = 0.25
Answer: 0.25
```

**Key Insight:** Since log(prob) is negative and additive, this reduces to shortest paths with -log(prob). But directly maximizing probability via modified Dijkstra also works because multiplication preserves order.

**Edge Cases:** start == end → 1.0. No path → 0.0. Single edge.

**Common Mistakes:** Using sum instead of product. Not initializing dist to 0 (float) for unreachable nodes.

**Pattern Recognition:** **Dijkstra (Maximization) Pattern**: Heap-based maximization of product. Used in: Path with Maximum Gold, Minimum Cost Path with probability.

**Statement:** Find path from start to end with maximum success probability.

**Approach:** Modified Dijkstra (maximize instead of minimize).

```python
# maxProbability: implement solution
def maxProbability(n, edges, succProb, start, end):
    import heapq
    from collections import defaultdict
    graph = defaultdict(list)
    for i in range(len(edges)):
        u,v = edges[i]
        graph[u].append((v,succProb[i]))
        graph[v].append((u,succProb[i]))
    dist = {start: 1.0}
    heap = [(-1.0, start)]
    while heap:
        d, node = heapq.heappop(heap)
        d = -d
        if node == end: return d
        if d < dist.get(node, 0): continue
        for nei, prob in graph[node]:
            nd = d * prob
            if nd > dist.get(nei, 0):
                dist[nei] = nd
                heapq.heappush(heap, (-nd, nei))
    return 0.0
```
**Time:** O(e*log(n)) | **Space:** O(n+e)

---

## Problem 35: Parallel Courses III

**Problem Explanation:** There are n courses (1-indexed) each with a duration. Prerequisites: you must take course b before a. You can take any number of courses simultaneously (in parallel). Find the minimum time to complete all courses.

**Algorithm Steps:**
1. Build adjacency list and indegree array.
2. Initialize `dp[i] = time[i]` for courses with indegree 0.
3. Kahn's topological sort: for each neighbor, `dp[nei] = max(dp[nei], dp[node] + time[nei])` — you must finish all prerequisites before starting nei.
4. Decrement indegree, push when 0.
5. Return `max(dp)`.

**Visual Walkthrough:** n=3, relations=[[1,3],[2,3]], time=[3,2,5]
```
Graph: 1→3, 2→3
Course 1: duration 3, no prereqs → dp[1]=3
Course 2: duration 2, no prereqs → dp[2]=2
Course 3: duration 5, needs 1 and 2
  dp[3] = max(dp[1], dp[2]) + 5 = max(3,2)+5 = 8
Answer: max(dp) = max(3,2,8) = 8
```

**Key Insight:** With parallel execution, the time to complete a course = max completion time of all prerequisites + its own duration. This is DP on DAG with topological ordering.

**Edge Cases:** No prerequisites → answer = max(time). Single course → return time[0].

**Common Mistakes:** Not 1-indexing correctly. Using sum instead of max (you don't need to wait for ALL prereqs sequentially — they run in parallel).

**Pattern Recognition:** **Topological DP Pattern**: DP on DAG processed in topological order. Used in: Longest Path in DAG, Minimum Time to Complete All Tasks.

**Statement:** Find minimum time to complete all courses with prerequisites and durations.

**Approach:** Topological sort + DP (max time to reach each course).

```python
# minimumTime: implement solution
def minimumTime(n, relations, time):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    indeg = [0]*n
    for u,v in relations:
        graph[u-1].append(v-1); indeg[v-1]+=1
    dp = [0]*n
    queue = deque()
    for i in range(n):
        if indeg[i]==0:
            queue.append(i)
            dp[i] = time[i]
    while queue:
        node = queue.popleft()
        for nei in graph[node]:
            dp[nei] = max(dp[nei], dp[node]+time[nei])
            indeg[nei]-=1
            if indeg[nei]==0: queue.append(nei)
    return max(dp)
```
**Time:** O(n+e) | **Space:** O(n+e)

---

## Problem 36: Longest Path in DAG

**Problem Explanation:** Given a Directed Acyclic Graph (DAG) with n nodes and edges, find the length of the longest path (number of edges). The graph is guaranteed to have no cycles.

**Algorithm Steps:**
1. Build adjacency list and indegree array.
2. Initialize `dp[i] = 0` for all nodes.
3. Kahn's algorithm: for each node, update `dp[nei] = max(dp[nei], dp[node] + 1)`.
4. After processing all nodes, answer = `max(dp)`.

**Visual Walkthrough:** n=5, edges=[[0,1],[1,2],[2,3],[1,3],[0,4]]
```
Graph: 0→1→2→3
            ↘
          0→4
DP:
  Start: node 0 (indeg=0) → dp=[0,0,0,0,0]
  Process 0: update 1(1), 4(1) → dp=[0,1,0,0,1]
  Process 1: update 2(2), 3(2) → dp=[0,1,2,2,1]
  Process 4: no outgoing
  Process 2: update 3(3) → dp=[0,1,2,3,1]
  Process 3: no outgoing
Longest path: 0→1→2→3 = 3 edges
Answer: 3
```

**Key Insight:** Topological order guarantees that when we process a node, all its incoming paths have already been considered — `dp[node]` is already the longest path to that node.

**Edge Cases:** Single node → 0. Disconnected DAG → 0 (isolated nodes).

**Common Mistakes:** Forgetting indegree tracking. Processing nodes in wrong order (not topological).

**Pattern Recognition:** **DAG DP (Topological) Pattern**: Longest/Shortest path in DAG using topological order. Used in: Parallel Courses III, Minimum Time to Complete All Courses.

**Statement:** Find longest path in directed acyclic graph.

**Approach:** Topological sort + DP.

```python
# longestPath: implement solution
def longestPath(n, edges):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    indeg = [0]*n
    for u,v in edges:
        graph[u].append(v); indeg[v]+=1
    dp = [0]*n
    queue = deque([i for i in range(n) if indeg[i]==0])
    while queue:
        node = queue.popleft()
        for nei in graph[node]:
            dp[nei] = max(dp[nei], dp[node]+1)
            indeg[nei]-=1
            if indeg[nei]==0: queue.append(nei)
    return max(dp)
```
**Time:** O(n+e) | **Space:** O(n+e)

---

## Problem 37: Minimum Height Trees

**Problem Explanation:** Given n nodes forming a tree (connected, n-1 edges), find all root nodes that minimize the height of the tree. Height = longest distance from root to leaf. The answer is always 1 or 2 nodes.

**Algorithm Steps:**
1. If n==1 return [0].
2. Build adjacency list. Find all leaves (nodes with degree 1).
3. While remaining nodes > 2:
   - Remove all current leaves from graph.
   - Update neighbor degrees — if neighbor becomes degree 1, add to next leaves.
   - Decrease remaining count.
4. Return remaining nodes (1 or 2 centroids).

**Visual Walkthrough:** n=6, edges=[[3,0],[3,1],[3,2],[3,4],[5,4]]
```
Tree:   0-3-1    Original leaves: [0,1,2,5]
          |     Remove leaves: remaining = 4
          2     New leaves: [3,4]
          |     Remove leaves: remaining = 2
          4-5   Centroids: [3,4] → answer
```

**Key Insight:** The centroid(s) of a tree are the nodes that minimize the tree's height. A tree has 1 or 2 centroids. Leaf-stripping finds them because centroids are the "middle" of the longest path.

**Edge Cases:** n=1 → [0]. n=2 → [0,1]. Path graph → centroids are the middle 1 or 2 nodes.

**Common Mistakes:** Not making a copy of degrees when removing leaves. Using edges list instead of adjacency (O(n²)).

**Pattern Recognition:** **Topological Leaf Removal Pattern**: Strip leaves iteratively to find centroids. Used in: Find Minimum Height Trees, Maximum Path Quality.

**Statement:** Find root nodes that give minimum height tree.

**Approach:** Strip leaves iteratively until 1-2 nodes remain.

```python
# findMinHeightTrees: implement solution
def findMinHeightTrees(n, edges):
    if n == 1: return [0]
    from collections import defaultdict, deque
    graph = defaultdict(set)
    for u,v in edges:
        graph[u].add(v); graph[v].add(u)
    leaves = [i for i in range(n) if len(graph[i])==1]
    remaining = n
    while remaining > 2:
        remaining -= len(leaves)
        new_leaves = []
        for leaf in leaves:
            nei = graph[leaf].pop()
            graph[nei].discard(leaf)
            if len(graph[nei])==1: new_leaves.append(nei)
        leaves = new_leaves
    return leaves
```
**Time:** O(n) | **Space:** O(n)

---

## Problem 38: Find the Safest Path in a Grid

**Problem Explanation:** A grid where 1 = thief, 0 = empty. Safeness factor of a cell = Manhattan distance to nearest thief. Safeness of a path = minimum safeness factor along the path. Find the maximum possible safeness factor for a path from (0,0) to (n-1,n-1).

**Algorithm Steps:**
1. Multi-source BFS from all thieves to compute safeness factor for each cell.
2. Use Dijkstra (max-heap) starting from (0,0): `max_min_factor`.
3. For each neighbor, new_factor = min(current_factor, safeness[neighbor]).
4. Push to heap if new_factor > visited_factor[neighbor].
5. When reaching (n-1,n-1), return that factor.

**Visual Walkthrough:** grid = [[0,0,1],[0,0,0],[0,0,0]]
```
Safeness factors (from multi-source BFS):
2 1 1
2 2 2  ← Actually from thief at (0,2): dist to (1,1)=2, (2,0)=3, etc.
3 3 3   Let's compute: 
Thief at (0,2). Distances:
(0,0)=2, (0,1)=1, (0,2)=0
(1,0)=3, (1,1)=2, (1,2)=1
(2,0)=4, (2,1)=3, (2,2)=2
Path: (0,0)→(0,1)→(1,1)→(2,1)→(2,2) → min factor = min(2,1,2,3,2)=1
Better: (0,0)→(1,0)→(2,0)→(2,1)→(2,2) → min(2,3,4,3,2)=2
Answer: 2
```

**Key Insight:** This is a maximin path problem. The safeness values form a "peak" landscape — Dijkstra with max-heap finds the path maximizing the minimum safeness factor.

**Edge Cases:** n=1 with thief → 0. n=1 no thief → INF (but problem expects 0). Start or end is thief → 0.

**Common Mistakes:** Not computing distances first (multi-source BFS). Using Manhattan distance instead of BFS (BFS handles obstacles if any).

**Pattern Recognition:** **Maximin Path (Dijkstra) Pattern**: Maximize the minimum value along a path. Used in: Swim in Rising Water (minimax), Path with Maximum Minimum Value.

**Statement:** Find safest path where minimum distance to thief is maximized.

**Approach:** Multi-source BFS for distances, then binary search + BFS.

```python
# maximumSafenessFactor: implement solution
def maximumSafenessFactor(grid):
    from collections import deque
    n = len(grid)
    if grid[0][0]==1 or grid[n-1][n-1]==1: return 0
    dist = [[-1]*n for _ in range(n)]
    queue = deque()
    for i in range(n):
        for j in range(n):
            if grid[i][j]==1: queue.append((i,j)); dist[i][j]=0
    while queue:
        x,y = queue.popleft()
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx,ny=x+dx,y+dy
            if 0<=nx<n and 0<=ny<n and dist[nx][ny]==-1:
                dist[nx][ny]=dist[x][y]+1
                queue.append((nx,ny))
    import heapq
    heap = [(-dist[0][0],0,0)]
    visited = {(0,0)}
    while heap:
        d,x,y = heapq.heappop(heap)
        if x==n-1 and y==n-1: return -d
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx,ny=x+dx,y+dy
            if 0<=nx<n and 0<=ny<n and (nx,ny) not in visited:
                visited.add((nx,ny))
                heapq.heappush(heap, (min(d,-dist[nx][ny]),nx,ny))
    return 0
```
**Time:** O(n^2*log(n^2)) | **Space:** O(n^2)

---

## Problem 39: All Paths from Source to Target (BFS)

**Problem Explanation:** Same as Problem 9 — find all paths from node 0 to node n-1 in a DAG. This version uses BFS instead of DFS/backtracking.

**Algorithm Steps:**
1. Initialize queue with (0, [0]).
2. BFS: pop node and path. If node is target, add path to result.
3. For each neighbor, push (neighbor, path + [neighbor]).
4. Return all collected paths.

**Key Insight:** BFS also works for enumerating all paths in a DAG because all paths are finite (no cycles). BFS explores paths level-by-level (by path length).

**Edge Cases:** Same as Problem 9.

**Common Mistakes:** Same as Problem 9. BFS may use more memory than DFS since it stores all partial paths simultaneously.

**Pattern Recognition:** **Path Enumeration (BFS)**: BFS alternative for enumerating paths. Used in: Same as Problem 9.

```python
# allPathsSourceTarget: implement solution
def allPathsSourceTarget(graph):
    from collections import deque
    n = len(graph)
    result = []
    queue = deque([(0, [0])])
    while queue:
        node, path = queue.popleft()
        if node == n-1:
            result.append(path)
            continue
        for nei in graph[node]:
            queue.append((nei, path+[nei]))
    return result
```
**Time:** O(2^n) | **Space:** O(2^n)

---

## Problem 40: Reconstruct Itinerary

**Problem Explanation:** Given a list of airline tickets where each ticket is [from, to], construct an itinerary starting from "JFK" that uses all tickets exactly once. If multiple valid itineraries exist, return the one with the smallest lexical order.

**Algorithm Steps:**
1. Build adjacency list, sorting destinations in reverse order (so the smallest pops last for correct result).
2. DFS from "JFK": for each destination from the current airport, pop and recurse.
3. After processing all destinations, append current airport to result.
4. Return reversed result (post-order appending reverses the sequence).

**Visual Walkthrough:** tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
```
Graph: JFK→MUC, MUC→LHR, LHR→SFO, SFO→SJC (a simple path)
DFS JFK→MUC→LHR→SFO→SJC (dead end, append SJC)
  Back: append SFO, LHR, MUC, JFK
Result reversed: [JFK,MUC,LHR,SFO,SJC]
```

**Key Insight:** Hierholzer's algorithm for Eulerian path: DFS and post-order append gives the correct itinerary. Reversing the adjacency list ensures lexical smallest order.

**Edge Cases:** Single ticket → [JFK, dest]. Multiple tickets from same source → lexical order matters.

**Common Mistakes:** Not using the edge-removal pattern (each ticket used exactly once). Not reversing the result at the end.

**Pattern Recognition:** **Eulerian Path (Hierholzer) Pattern**: Find path using all edges exactly once. Used in: Reconstruct Itinerary, Valid Arrangement of Pairs.

**Statement:** Given tickets, find itinerary starting from JFK (smallest lexical order).

**Approach:** DFS with stack, remove edges as used.

```python
# findItinerary: implement solution
def findItinerary(tickets):
    from collections import defaultdict
    graph = defaultdict(list)
    for u,v in sorted(tickets, reverse=True):
        graph[u].append(v)
    result = []
    def dfs(airport):
        while graph[airport]:
            dfs(graph[airport].pop())
        result.append(airport)
    dfs("JFK")
    return result[::-1]
```
**Time:** O(e*log(e)) | **Space:** O(n+e)

---

