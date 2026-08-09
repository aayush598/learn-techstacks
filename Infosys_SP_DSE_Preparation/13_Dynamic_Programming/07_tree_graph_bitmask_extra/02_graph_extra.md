# Graph DP — Extra Problems

Additional graph problems covering DAG shortest paths, BFS-based shortest
paths, topological sort for course scheduling, and constrained shortest
paths. Bellman-Ford, Floyd-Warshall, Longest Path DAG, Critical Path, and
Hamiltonian/TSP problems are in the main guide.

---

## 1. DAG Shortest Paths — Medium

**🔗 Practice Link:** [1. DAG Shortest Paths — Medium](https://www.geeksforgeeks.org/shortest-path-for-directed-acyclic-graphs)

### Problem Explanation
Given a DAG with V vertices, weighted directed edges, and a source vertex,
find the shortest distance from source to every other vertex. Since there
are no cycles, we can process vertices in topological order and relax edges
once — no need for multiple rounds like Bellman-Ford.

### State Definition
`dist[v]` = shortest distance from source to `v`. Process vertices in
topological order so when we relax edge `(u,v,w)`, `dist[u]` is final.

### Recurrence Relation
```
dist[v] = min(dist[v], dist[u] + w)  for each edge (u, v, w)
```
Processed in topological order: each edge is relaxed exactly once.

### Base Cases
- `dist[src] = 0`, all others `inf`.

### Intuition (Why This Works)
Topological order guarantees every predecessor of `v` is processed before
`v`. So a single pass through vertices in topo order is sufficient. This
is O(V+E) vs Bellman-Ford's O(V*E).

### Step-by-Step Procedure
1. Build adjacency list and indegree array.
2. Run Kahn's algorithm for topological sort.
3. Init `dist[src] = 0`, others `inf`.
4. For each `u` in topo order: for each edge `(u,v,w)`, relax `dist[v]`.
5. Return `dist`.

### Worked Example (Dry Run)
```
DAG (4 vertices):
  0 --2--> 1 --3--> 3
  0 --6--> 2 --1--> 3
  Source: 0

Topo order: 0, 1, 2, 3

  dist = [0, inf, inf, inf]
  Process 0: dist[1]=min(inf,0+2)=2, dist[2]=min(inf,0+6)=6
  Process 1: dist[3]=min(inf,2+3)=5
  Process 2: dist[3]=min(5,6+1)=5 (no improvement)
  Process 3: no outgoing edges

Answer: [0, 2, 6, 5]
```

### Code
```python
from collections import deque

def dag_shortest_paths(V, edges, src):
    adj = [[] for _ in range(V)]
    indeg = [0] * V
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1
    q = deque([i for i in range(V) if indeg[i] == 0])
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    dist = [float('inf')] * V
    dist[src] = 0
    for u in topo:
        if dist[u] != float('inf'):
            for v, w in adj[u]:
                dist[v] = min(dist[v], dist[u] + w)
    return dist
# Time: O(V+E), Space: O(V+E)
```

### Complexity
- Time: O(V+E), Space: O(V+E).

### Common Mistakes & Edge Cases
- Graph has a cycle: topo sort produces fewer than V vertices.
- Source unreachable from some vertex: `dist` stays `inf`.
- Empty graph (V=0): return empty list.

---

## 2. Minimum Cost Path in DAG — Medium

**🔗 Practice Link:** [2. Minimum Cost Path in DAG — Medium](https://www.geeksforgeeks.org/shortest-path-for-directed-acyclic-graphs)

### Problem Explanation
Given a DAG with weighted edges and source/destination vertices, find the
minimum-cost path from source to destination. Same as DAG shortest paths
but targeting a specific destination.

### State Definition
`dist[v]` = shortest distance from source to `v` in topological order.
Once `dist[dest]` is finalized, we can optionally stop early.

### Recurrence Relation
```
dist[v] = min(dist[v], dist[u] + w)
```
Same as DAG shortest paths; we just read `dist[dest]` at the end.

### Base Cases
- `dist[src] = 0`, others `inf`.
- If `dist[dest]` remains `inf`, no path exists.

### Intuition (Why This Works)
Topological ordering ensures each vertex's distance is final before its
outgoing edges are relaxed. This is the most efficient approach for DAGs.

### Step-by-Step Procedure
1. Build adjacency list and topological order via Kahn's.
2. Init `dist[src] = 0`.
3. Relax edges in topological order.
4. Return `dist[dest]` (or `inf` if unreachable).

### Worked Example (Dry Run)
```
DAG (5 vertices), src=0, dest=4:
  0 --1--> 1 --2--> 3 --1--> 4
  0 --5--> 2 --1--> 3
  1 --1--> 2

Topo order: 0, 1, 2, 3, 4

  dist = [0, inf, inf, inf, inf]
  Process 0: d[1]=1, d[2]=5
  Process 1: d[2]=min(5,1+1)=2, d[3]=min(inf,1+2)=3
  Process 2: d[3]=min(3,2+1)=3
  Process 3: d[4]=min(inf,3+1)=4
  Process 4: no outgoing

Answer: dist[4] = 4 (path: 0→1→2→3→4 = 1+1+1+1)
```

### Code
```python
from collections import deque

def min_cost_path_dag(V, edges, src, dest):
    adj = [[] for _ in range(V)]
    indeg = [0] * V
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1
    q = deque([i for i in range(V) if indeg[i] == 0])
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    dist = [float('inf')] * V
    dist[src] = 0
    for u in topo:
        if dist[u] != float('inf'):
            for v, w in adj[u]:
                dist[v] = min(dist[v], dist[u] + w)
    return dist[dest] if dist[dest] != float('inf') else -1
# Time: O(V+E), Space: O(V+E)
```

### Complexity
- Time: O(V+E), Space: O(V+E).

### Common Mistakes & Edge Cases
- Return `-1` (or sentinel) when `dest` is unreachable.
- Source equals destination: return `0`.
- Multiple paths to dest: the DP picks the minimum.

---

## 3. Word Ladder (LC #127) — Hard

**🔗 Practice Link:** [3. Word Ladder](https://leetcode.com/problems/word-ladder/)

### Problem Explanation
Given two words `beginWord` and `endWord` and a dictionary `wordList`,
find the shortest transformation sequence from `beginWord` to `endWord`,
changing one letter at a time, where every intermediate word must be in
`wordList`. Return the number of words in the sequence (beginWord counts).
If impossible, return `0`.

### State Definition
`dist[word]` = minimum steps from `beginWord` to `word`. BFS explores
words level by level (each level = one letter change).

### Recurrence Relation
```
For each word `curr` at distance d:
  For each position i in curr:
    For each letter c in 'a'..'z':
      neighbor = curr[:i] + c + curr[i+1:]
      if neighbor in wordSet and dist[neighbor] not set:
        dist[neighbor] = d + 1
```

### Base Cases
- `beginWord` distance = `1` (counting beginWord).
- If `endWord` not in `wordList`, return `0`.

### Intuition (Why This Works)
BFS finds the shortest path in an unweighted graph where nodes are words
and edges connect words differing by one letter. Level-by-level exploration
guarantees the first time we reach `endWord` is via the shortest path.

### Step-by-Step Procedure
1. Check `endWord` is in `wordList`; if not, return `0`.
2. Build a set from `wordList` for O(1) lookup.
3. BFS from `beginWord`: for each word, try all one-letter mutations.
4. If a mutation is in the set, add it to the queue at distance+1.
5. Remove visited words from the set to avoid revisiting.
6. Return `dist[endWord]` when found.

### Worked Example (Dry Run)
```
beginWord = "hit", endWord = "cog"
wordList = ["hot","dot","dog","lot","log","cog"]

BFS:
  Level 1: "hit" → mutate → "hot" (in dict)
  Level 2: "hot" → "dot", "lot"
  Level 3: "dot" → "dog"; "lot" → "log"
  Level 4: "dog" → "cog" ✓

Answer: 5 (hit→hot→dot→dog→cog)
```

### Code
```python
from collections import deque

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: list) -> int:
        word_set = set(wordList)
        if endWord not in word_set:
            return 0
        queue = deque([(beginWord, 1)])
        visited = {beginWord}
        while queue:
            word, steps = queue.popleft()
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    neighbor = word[:i] + c + word[i+1:]
                    if neighbor == endWord:
                        return steps + 1
                    if neighbor in word_set and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, steps + 1))
        return 0
# Time: O(N * L * 26), Space: O(N * L) where N = wordList size, L = word length
```

### Complexity
- Time: O(N * L * 26) — for each of N words, try L positions × 26 letters.
- Space: O(N) for the set and queue.

### Common Mistakes & Edge Cases
- `endWord` not in dictionary: return `0` immediately.
- `beginWord` equals `endWord`: return `1`.
- Single-letter words: mutations are just other single letters.
- Large dictionaries: BFS is efficient since it prunes by visited set.

---

## 4. Alien Dictionary (LC #269) — Hard

**🔗 Practice Link:** [4. Alien Dictionary](https://www.geeksforgeeks.org/given-sorted-dictionary-find-precedence-characters)

### Problem Explanation
Given a sorted list of words in an alien language, derive the character
ordering. The words are sorted lexicographically according to the alien
rules. Return any valid ordering of the characters.

### State Definition
Build a directed graph: for each pair of adjacent words, find the first
differing character; the first word's character must come before the second
word's character. Then topological sort the graph.

### Recurrence Relation
```
For adjacent words w1, w2:
  Find first index i where w1[i] != w2[i]
  Add edge: w1[i] -> w2[i]  (w1[i] comes before w2[i])
```
Topological sort gives the character ordering.

### Base Cases
- No differing characters between adjacent words but one is prefix of the
  other: the longer word must come after (invalid if shorter word is after).

### Intuition (Why This Works)
Sorted words encode pairwise constraints on character order. Each
constraint is a directed edge. Topological sort produces a valid ordering.
Cycle detection: if topo sort doesn't include all characters, the input
is inconsistent.

### Step-by-Step Procedure
1. Build graph: for each pair of adjacent words, find first difference.
2. Add directed edge from w1[i] to w2[i].
3. Also build indegree map.
4. Run Kahn's topological sort.
5. If result includes all characters, return it; else return `""`.

### Worked Example (Dry Run)
```
words = ["wrt","wrf","er","ett","rftt"]

Compare wrt vs wrf: diff at index 2: t→f  (t < f)
Compare wrf vs er:  diff at index 0: w→e  (w < e)
Compare er vs ett:  diff at index 1: r→t  (r < t)
Compare ett vs rftt: diff at index 0: e→r  (e < r)

Edges: t→f, w→e, r→t, e→r
Graph: w→e→r→t→f

Topo sort: w, e, r, t,  Answer: "wertf"
```

### Code
```python
from collections import deque, defaultdict

class Solution:
    def alienOrder(self, words: list) -> str:
        adj = defaultdict(set)
        indeg = {c: 0 for word in words for c in word}
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            min_len = min(len(w1), len(w2))
            if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
                return ""               # invalid: prefix comes after longer word
            for j in range(min_len):
                if w1[j] != w2[j]:
                    if w2[j] not in adj[w1[j]]:
                        adj[w1[j]].add(w2[j])
                        indeg[w2[j]] += 1
                    break
        q = deque([c for c in indeg if indeg[c] == 0])
        result = []
        while q:
            c = q.popleft()
            result.append(c)
            for nei in adj[c]:
                indeg[nei] -= 1
                if indeg[nei] == 0:
                    q.append(nei)
        return "".join(result) if len(result) == len(indeg) else ""
# Time: O(C) where C = total chars, Space: O(1) (at most 26 chars)
```

### Complexity
- Time: O(C) — sum of all word lengths for comparison + O(26) for topo sort.
- Space: O(1) — bounded by alphabet size (26 lowercase letters).

### Common Mistakes & Edge Cases
- Prefix word appearing after the longer word: invalid input → return `""`.
- Cycle in character constraints: topo sort fails → return `""`.
- Single word: any ordering of its characters is valid.

---

## 5. Course Schedule (LC #207) — Medium

**🔗 Practice Link:** [5. Course Schedule](https://leetcode.com/problems/course-schedule/)

### Problem Explanation
There are `numCourses` courses with prerequisites. Each prerequisite is
a pair `[a, b]` meaning course `b` must be taken before course `a`. Determine
if it is possible to take all courses (no cycle in the dependency graph).

### State Definition
Build a directed graph where edge `b→a` means `b` is prerequisite for `a`.
Detect cycle: if cycle exists, return `False`. Otherwise return `True`.

### Recurrence Relation
```
Kahn's topological sort: process vertices with indegree 0.
If all vertices are processed (count == numCourses), no cycle exists.
```

### Base Cases
- `numCourses == 0`: return `True`.
- All courses have no prerequisites: return `True`.

### Intuition (Why This Works)
A course schedule with prerequisites forms a DAG if and only if no cycle
exists. Kahn's algorithm detects cycles: if fewer than `numCourses` vertices
are output, a cycle prevents completion.

### Step-by-Step Procedure
1. Build adjacency list and indegree array.
2. Queue all vertices with indegree `0`.
3. Process queue: decrement indegrees, enqueue when indegree hits `0`.
4. Count processed vertices.
5. Return `count == numCourses`.

### Worked Example (Dry Run)
```
numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]

Graph: 0→1, 0→2, 1→3, 2→3
Indegrees: [0, 1, 1, 2]

  Queue: [0] (indeg 0)
  Process 0: indeg[1]→0, indeg[2]→0 → queue [1, 2]
  Process 1: indeg[3]→1 → queue [2]
  Process 2: indeg[3]→0 → queue [3]
  Process 3: done

Count = 4 == numCourses → True
```

### Code
```python
from collections import deque

class Solution:
    def canFinish(self, numCourses: int, prerequisites: list) -> bool:
        adj = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for a, b in prerequisites:
            adj[b].append(a)
            indeg[a] += 1
        q = deque([i for i in range(numCourses) if indeg[i] == 0])
        count = 0
        while q:
            u = q.popleft()
            count += 1
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return count == numCourses
# Time: O(V+E), Space: O(V+E)
```

### Complexity
- Time: O(V+E), Space: O(V+E).

### Common Mistakes & Edge Cases
- Self-prerequisite `[a, a]`: cycle → return `False`.
- No prerequisites: return `True`.
- Disconnected components: Kahn's handles them naturally.

---

## 6. Course Schedule II (LC #210) — Medium

**🔗 Practice Link:** [6. Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)

### Problem Explanation
Like Course Schedule I, but instead of just returning whether all courses
can be finished, return the actual ordering (one valid topological sort).
If impossible, return `[]`.

### State Definition
Same as Course Schedule I: build graph, run Kahn's, collect the order.

### Recurrence Relation
```
topo_order = []  (append vertices as they are dequeued with indegree 0)
```

### Base Cases
- If `len(topo_order) < numCourses`: cycle exists → return `[]`.

### Intuition (Why This Works)
Kahn's algorithm naturally produces a valid topological order. The order
of processing in the queue gives one valid course-taking sequence.

### Step-by-Step Procedure
1. Build adjacency list and indegree.
2. Queue all indegree-0 vertices.
3. BFS: dequeue, append to result, decrement neighbor indegrees.
4. If result length == numCourses, return it; else `[]`.

### Worked Example (Dry Run)
```
numCourses = 4, prereqs = [[1,0],[2,0],[3,1],[3,2]]

  Queue: [0]
  Pop 0 → result [0], indeg: [0,0,0,2] → queue [1,2]
  Pop 1 → result [0,1], indeg: [0,0,0,1] → queue [2]
  Pop 2 → result [0,1,2], indeg: [0,0,0,0] → queue [3]
  Pop 3 → result [0,1,2,3]

Answer: [0,1,2,3] (one valid ordering)
```

### Code
```python
from collections import deque

class Solution:
    def findOrder(self, numCourses: int, prerequisites: list) -> list:
        adj = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for a, b in prerequisites:
            adj[b].append(a)
            indeg[a] += 1
        q = deque([i for i in range(numCourses) if indeg[i] == 0])
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return order if len(order) == numCourses else []
# Time: O(V+E), Space: O(V+E)
```

### Complexity
- Time: O(V+E), Space: O(V+E).

### Common Mistakes & Edge Cases
- Multiple valid orderings: any one is accepted.
- Cycle: return `[]`.
- `numCourses == 0`: return `[]`.

---

## 7. Number of Ways to Arrive at Destination (LC #1976) — Hard

**🔗 Practice Link:** [7. Number of Ways to Arrive at Destination](https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/)

### Problem Explanation
Given `n` cities and weighted bidirectional roads, count the number of
shortest paths from city `0` to city `n-1`. Return the count modulo
10^9+7. The answer can be very large.

### State Definition
`dist[v]` = shortest distance from city 0 to `v`.
`ways[v]` = number of shortest paths from city 0 to `v`.
Use Dijkstra's algorithm (non-negative weights).

### Recurrence Relation
```
When relaxing edge (u, v, w):
  if dist[u] + w < dist[v]:
    dist[v] = dist[u] + w
    ways[v] = ways[u]
  elif dist[u] + w == dist[v]:
    ways[v] = (ways[v] + ways[u]) % MOD
```

### Base Cases
- `dist[0] = 0`, `ways[0] = 1`.
- All other `dist = inf`, `ways = 0`.

### Intuition (Why This Works)
Dijkstra explores vertices in order of distance. When we find a shorter
path to `v`, we reset `ways[v]` to `ways[u]`. When we find an equal-length
path, we add `ways[u]` to `ways[v]`. This correctly counts all shortest
paths.

### Step-by-Step Procedure
1. Build adjacency list.
2. Init `dist = [inf]*n`, `ways = [0]*n`, `dist[0]=0`, `ways[0]=1`.
3. Min-heap: `(distance, vertex)`.
4. Dijkstra: for each edge `(u,v,w)`:
   - If shorter: update dist, set ways = ways[u].
   - If equal: add ways[u] to ways[v].
5. Return `ways[n-1] % MOD`.

### Worked Example (Dry Run)
```
n=7, roads: [[0,6,7],[0,1,2],[1,2,3],[1,3,3],[6,3,3],[3,5,1],[6,5,1],[2,5,1],[0,4,5],[4,6,2]]

Dijkstra trace (showing dist, ways for each vertex):
  Start: dist=[0,inf,inf,inf,inf,inf,inf], ways=[1,0,0,0,0,0,0]
  Visit 0: d[6]=7,w=1; d[1]=2,w=1; d[4]=5,w=1
  Visit 1 (d=2): d[2]=5,w=1; d[3]=5,w=1
  Visit 4 (d=5): d[6]=min(7,7)=7,w=1+1=2
  Visit 2 (d=5): d[5]=6,w=1
  Visit 3 (d=5): d[6]=min(7,8)=7,w stays 2; d[5]=min(6,6)=6,w=1+1=2
  Visit 5 (d=6): d[6]=min(7,7)=7,w=2+2=4
  Visit 6 (d=7): no improvements

Answer: ways[6] = 4
```

### Code
```python
import heapq

class Solution:
    def countPaths(self, n: int, roads: list) -> int:
        MOD = 10**9 + 7
        adj = [[] for _ in range(n)]
        for u, v, w in roads:
            adj[u].append((v, w))
            adj[v].append((u, w))
        dist = [float('inf')] * n
        ways = [0] * n
        dist[0] = 0
        ways[0] = 1
        heap = [(0, 0)]  # (distance, vertex)
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    ways[v] = ways[u]
                    heapq.heappush(heap, (dist[v], v))
                elif dist[u] + w == dist[v]:
                    ways[v] = (ways[v] + ways[u]) % MOD
        return ways[n - 1] % MOD
# Time: O((V+E) log V), Space: O(V+E)
```

### Complexity
- Time: O((V+E) log V) — Dijkstra with heap.
- Space: O(V+E).

### Common Mistakes & Edge Cases
- Not using modulo for large counts.
- Updating `ways` before checking if the new path is shorter.
- Stale heap entries: check `d > dist[u]` on pop.
- No path exists: `ways[n-1]` is `0`.

---

## 8. Path with Maximum Probability (LC #1514) — Medium

**🔗 Practice Link:** [8. Path with Maximum Probability](https://leetcode.com/problems/path-with-maximum-probability/)

### Problem Explanation
Given `n` cities with edges having success probabilities (0 to 1), find
the path from `start` to `end` that maximizes the product of edge
probabilities. Return the maximum probability.

### State Definition
`max_prob[v]` = maximum probability of reaching `v` from `start`.
Modified Dijkstra: use max-heap instead of min-heap, and `max` instead
of `min` for relaxation.

### Recurrence Relation
```
max_prob[v] = max(max_prob[v], max_prob[u] * probability)
```

### Base Cases
- `max_prob[start] = 1.0`, all others `0.0`.

### Intuition (Why This Works)
This is Dijkstra with multiplication instead of addition, and max instead
of min. Probabilities multiply along a path, and we want the maximum
product. Non-negative probabilities guarantee the greedy approach works.

### Step-by-Step Procedure
1. Build adjacency list with probabilities.
2. Init `max_prob[start] = 1.0`.
3. Max-heap: `(-probability, vertex)` (negate for min-heap emulation).
4. For each edge `(u, v, p)`: if `max_prob[u] * p > max_prob[v]`, update.
5. Return `max_prob[end]`.

### Worked Example (Dry Run)
```
n=3, edges = [[0,1,0.5],[0,2,0.3],[1,2,0.9]], start=0, end=2

  max_prob = [1.0, 0.0, 0.0]
  Visit 0: prob[1]=0.5, prob[2]=0.3
  Visit 1 (prob=0.5): prob[2]=max(0.3, 0.5*0.9)=max(0.3,0.45)=0.45
  Visit 2: done

Answer: 0.45 (path 0→1→2 = 0.5*0.9)
```

### Code
```python
import heapq

class Solution:
    def maxProbability(self, n: int, edges: list, succProb: list,
                       start: int, end: int) -> float:
        adj = [[] for _ in range(n)]
        for (u, v), p in zip(edges, succProb):
            adj[u].append((v, p))
            adj[v].append((u, p))
        max_prob = [0.0] * n
        max_prob[start] = 1.0
        heap = [(-1.0, start)]  # min-heap with negated probabilities
        while heap:
            prob, u = heapq.heappop(heap)
            prob = -prob
            if prob < max_prob[u]:
                continue
            for v, p in adj[u]:
                if prob * p > max_prob[v]:
                    max_prob[v] = prob * p
                    heapq.heappush(heap, (-max_prob[v], v))
        return max_prob[end]
# Time: O((V+E) log V), Space: O(V+E)
```

### Complexity
- Time: O((V+E) log V), Space: O(V+E).

### Common Mistakes & Edge Cases
- No path from start to end: return `0.0`.
- `start == end`: return `1.0`.
- Probability `0.0` edges: they won't improve any path.

---

## 9. Network Delay Time (LC #743) — Medium

**🔗 Practice Link:** [9. Network Delay Time](https://leetcode.com/problems/network-delay-time/)

### Problem Explanation
Given `n` nodes and directed weighted edges `times[i] = (u, v, w)`,
send a signal from node `k`. The signal takes `w` time to travel edge
`u→v`. Find the minimum time for all nodes to receive the signal. If not
all nodes can receive it, return `-1`.

### State Definition
`dist[v]` = shortest time from `k` to `v`. Standard Dijkstra's algorithm.

### Recurrence Relation
```
dist[v] = min(dist[v], dist[u] + w)
```

### Base Cases
- `dist[k] = 0`, all others `inf`.

### Intuition (Why This Works)
All edges have non-negative weights, so Dijkstra gives exact shortest
paths. The answer is `max(dist)` — the time when the last node receives
the signal.

### Step-by-Step Procedure
1. Build adjacency list.
2. Dijkstra from node `k`.
3. If any `dist[v]` is `inf`: return `-1`.
4. Return `max(dist)`.

### Worked Example (Dry Run)
```
n=3, times = [[1,2,1],[2,3,2],[1,3,4]], k=1

  dist = [inf, inf, inf] (1-indexed: [inf,0,inf,inf])
  Visit 1: d[2]=1, d[3]=4
  Visit 2 (d=1): d[3]=min(4,1+2)=3
  Visit 3: done

  max(dist[1:]) = max(0,1,3) = 3

Answer: 3
```

### Code
```python
import heapq

class Solution:
    def networkDelayTime(self, times: list, n: int, k: int) -> int:
        adj = [[] for _ in range(n + 1)]
        for u, v, w in times:
            adj[u].append((v, w))
        dist = [float('inf')] * (n + 1)
        dist[k] = 0
        heap = [(0, k)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(heap, (dist[v], v))
        ans = max(dist[1:])
        return ans if ans < float('inf') else -1
# Time: O((V+E) log V), Space: O(V+E)
```

### Complexity
- Time: O((V+E) log V), Space: O(V+E).

### Common Mistakes & Edge Cases
- `n=1`: return `0` (only one node, already has signal).
- Unreachable nodes: return `-1`.
- Multiple edges between same pair: Dijkstra handles it.

---

## 10. Shortest Path in Binary Matrix (LC #1091) — Medium

**🔗 Practice Link:** [10. Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/)

### Problem Explanation
Given an `n x n` binary grid where `0` is open and `1` is blocked, find
the shortest path from top-left `(0,0)` to bottom-right `(n-1,n-1)` moving
in 8 directions. Return the path length (number of cells) or `-1` if no
path exists. Start and end cells must be `0`.

### State Definition
`dist[r][c]` = minimum steps from `(0,0)` to `(r,c)`. BFS explores all 8
neighbors level by level, guaranteeing the shortest path.

### Recurrence Relation
```
For each neighbor (nr, nc) of (r, c):
  if grid[nr][nc] == 0 and dist[nr][nc] == -1 (unvisited):
    dist[nr][nc] = dist[r][c] + 1
    enqueue (nr, nc)
```

### Base Cases
- `grid[0][0] == 1` or `grid[n-1][n-1] == 1`: return `-1`.
- `n == 1`: return `1` (start is end).

### Intuition (Why This Works)
BFS in an unweighted grid guarantees the shortest path. Each cell is a
node, each of the 8 directions is an edge of weight 1. The first time we
reach the bottom-right, it is via the shortest path.

### Step-by-Step Procedure
1. Check start/end cells are open.
2. BFS from `(0,0)` with `dist[0][0] = 1`.
3. For each cell, try all 8 neighbors.
4. Return `dist[n-1][n-1]` when BFS ends.

### Worked Example (Dry Run)
```
Grid (3x3):
  0 0 0
  1 1 0
  0 0 0

BFS:
  (0,0) d=1 → neighbors: (0,1)=1, (1,0)=blocked, (1,1)=1
  (0,1) d=2 → (0,2)=2, (1,2)=2
  (1,1) d=2 → already visited (0,2)
  (0,2) d=3 → (1,2) already set, done
  (1,2) d=3 → (2,1)=3, (2,2)=3

  dist[2][2] = 3

Answer: 3 (path: (0,0)→(1,1)→(2,2) diagonal moves)
```

### Code
```python
from collections import deque

class Solution:
    def shortestPathBinaryMatrix(self, grid: list) -> int:
        n = len(grid)
        if grid[0][0] == 1 or grid[n-1][n-1] == 1:
            return -1
        if n == 1:
            return 1
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        dist = [[-1] * n for _ in range(n)]
        dist[0][0] = 1
        queue = deque([(0, 0)])
        while queue:
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    if nr == n - 1 and nc == n - 1:
                        return dist[nr][nc]
                    queue.append((nr, nc))
        return -1
# Time: O(n^2), Space: O(n^2)
```

### Complexity
- Time: O(n²), Space: O(n²).

### Common Mistakes & Edge Cases
- Start or end blocked: return `-1`.
- `n == 1`: return `1` if cell is `0`.
- Path length counts cells, not edges.
- 8-directional movement (not 4).

---

## 11. Cheapest Flights Within K Stops (LC #787) — Medium

**🔗 Practice Link:** [11. Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/)

### Problem Explanation
Given `n` cities and flights `[from, to, price]`, find the cheapest price
from `src` to `dst` with at most `k` stops. If no such route, return `-1`.
Standard shortest path algorithms don't apply directly because of the
`k` stops constraint.

### State Definition
`dist[v][stops]` = minimum cost to reach `v` using exactly `stops` stops.
Bellman-Ford style: relax all edges for each stop level.

### Recurrence Relation
```
For each stop level s from 1 to k+1:
  For each edge (u, v, w):
    dist[v][s] = min(dist[v][s], dist[u][s-1] + w)
```
We need at most `k` stops, which means at most `k+1` edges.

### Base Cases
- `dist[src][0] = 0`, all others `inf`.
- Answer = `min(dist[dst][0..k+1])`.

### Intuition (Why This Works)
The `k` stops constraint means the shortest path uses at most `k+1` edges.
By iterating `k+1` rounds of edge relaxation (like Bellman-Ford with a
limited number of rounds), we guarantee the constraint is respected.
We use a copy of distances each round to prevent using updated values
within the same round.

### Step-by-Step Procedure
1. Init `dist[v] = inf` for all `v`, `dist[src] = 0`.
2. For `i` in `0..k`:
   a. Copy `dist` to `temp`.
   b. For each edge `(u, v, w)`: if `dist[u] + w < temp[v]`, update `temp[v]`.
   c. Set `dist = temp`.
3. Return `dist[dst]` if finite, else `-1`.

### Worked Example (Dry Run)
```
n=4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
src=0, dst=3, k=1

  dist = [0, inf, inf, inf]
  Round 1 (stop 0→1):
    temp = [0, inf, inf, inf]
    (0,1,100): temp[1] = min(inf, 0+100) = 100
    (1,2,100): dist[1]=inf → skip
    (2,0,100): skip, (1,3,600): skip, (2,3,200): skip
    dist = [0, 100, inf, inf]
  Round 2 (stop 1→2, up to k=1):
    temp = [0, 100, inf, inf]
    (0,1,100): temp[1]=min(100,0+100)=100 (no change)
    (1,2,100): temp[2]=min(inf,100+100)=200
    (1,3,600): temp[3]=min(inf,100+600)=700
    (2,3,200): dist[2]=inf → skip
    dist = [0, 100, 200, 700]

Answer: dist[3] = 700 (path: 0→1→3, 1 stop)
```

### Code
```python
class Solution:
    def findCheapestPrice(self, n: int, flights: list, src: int, dst: int,
                          k: int) -> int:
        # Bellman-Ford with at most k+1 edges (k stops).
        dist = [float('inf')] * n
        dist[src] = 0
        for i in range(k + 1):         # at most k+1 edges
            temp = dist[:]             # snapshot to avoid using same-round updates
            for u, v, w in flights:
                if dist[u] + w < temp[v]:
                    temp[v] = dist[u] + w
            dist = temp
        return dist[dst] if dist[dst] < float('inf') else -1
# Time: O(K * E), Space: O(V)
```

### Complexity
- Time: O(K * E) — K rounds, each scanning all edges.
- Space: O(V) — two distance arrays.

### Common Mistakes & Edge Cases
- Using a single `dist` array without snapshot: propagates through multiple
  edges in one round, violating the stops constraint.
- `k == 0`: at most 0 stops means direct flight only.
- No path exists: return `-1`.
- Cheapest path uses fewer than `k` stops: the DP naturally handles this.
