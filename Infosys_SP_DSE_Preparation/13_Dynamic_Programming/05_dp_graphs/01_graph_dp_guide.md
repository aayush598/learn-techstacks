# DP on Graphs — Complete Guide

## Graph DP Decision Tree

Before solving, classify the problem: the type of DP depends entirely on the
graph's structure (a DAG, a weighted graph with negative edges, a complete
graph) and what the question asks (shortest, longest, count, existence).

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    GRAPH DP PATTERN GUIDE                                │
├─────────────────────────────┬────────────────────────────────────────────┤
│ Problem hints               │ Approach                                 │
├─────────────────────────────┼────────────────────────────────────────────┤
│ "shortest paths, neg edges" │ Bellman-Ford (V-1 edge relaxations)      │
│ "all-pairs shortest paths"  │ Floyd-Warshall (DP over intermediate k)  │
│ "longest path in DAG"       │ Topo sort + DP on DAG                    │
│ "critical path / scheduling"│ Forward + backward DP on topo order      │
│ "visit all nodes exactly once"│ TSP / Hamiltonian (bitmask DP, O(2ⁿn²))│
│ "shortest Hamiltonian path"  │ Bitmask DP: dp[mask][last]              │
│ "count Hamiltonian paths"    │ Bitmask counting DP                     │
└─────────────────────────────┴────────────────────────────────────────────┘
```

Two essential rules: (1) DP on graphs needs an acyclic dependency order — a
topological order for DAGs, the edge-list order for Bellman-Ford, or the
increasing-bitmask order for Hamiltonian problems; (2) negative edge weights are
legal for Bellman-Ford and Floyd-Warshall but make Dijkstra and greedy
"longest path" approaches invalid.

---

## Shortest Paths with DP

The shortest-path family of DP: repeatedly relax (improve) distance estimates
using the rule "a shorter path to v can go through u". Bellman-Ford fixes the
*number of edges* as the DP layer; Floyd-Warshall fixes the *set of intermediate
vertices* as the DP layer.

### Bellman-Ford (Single-Source Shortest Paths with Negative Weights)

**🔗 Practice Link:** [Bellman-Ford](https://www.geeksforgeeks.org/bellman-ford-algorithm-dp-23)

**Problem Explanation:**
Given a directed weighted graph with V vertices (numbered `0..V-1`), an edge
list `edges = [(u, v, w), ...]` (edge from `u` to `v` with weight `w`, weights
may be negative), and a source `src`, find the shortest distance from `src` to
every vertex. Return the distance array; if the graph contains a reachable
*negative cycle* (a cycle whose total weight is negative, allowing infinitely
decreasing distances), return `None` instead.

**State Definition:**
`dist[v]` = the shortest distance from `src` to `v` found so far, using at most
`k` edges during the `k`-th round. The DP layer is the round number `k`: after
round `k`, every shortest path using `≤ k` edges has been discovered. The
`path[v] = u` array records the predecessor of `v` so the shortest path can be
reconstructed later.

**Recurrence Relation:**
```
dist[v] = min(dist[v], dist[u] + w)   for every edge (u, v, w)
```
Plain-English reason: any shortest path to `v` must arrive via some edge
`(u, v, w)`, so the best new candidate for `dist[v]` is the best distance to `u`
plus the edge weight — relaxing every edge once per round is exactly this
update applied to all candidates in parallel.

**Base Cases:**
- `dist[src] = 0`; every other `dist[v] = ∞` (not yet reachable).
- A simple shortest path has at most `V-1` edges (it cannot repeat a vertex), so
  `V-1` full relaxation rounds are enough.
- Termination: if a full round changes nothing (`updated == False`), the
  distances are already final and we stop early.

**Intuition (Why This Works):**
Bellman-Ford is DP over the path length: round `k` computes the shortest paths
that use at most `k` edges, and each round builds on the previous one via the
relaxation rule. After `V-1` rounds, every simple path has been examined; if a
path with `V` edges is still improving, it must contain a negative cycle
(because any path of `V` edges repeats a vertex, forming a cycle), so one extra
relaxation round detects it. Unlike Dijkstra, the order of edges does not
matter — the DP just needs every edge tried once per round.

**Step-by-Step Procedure:**
1. Initialize `dist = [INF] * V`, set `dist[src] = 0`, and `path = [-1] * V`.
2. Repeat `V - 1` times:
   a. Set `updated = False`.
   b. For every edge `(u, v, w)`: if `dist[u]` is finite and
      `dist[u] + w < dist[v]`, update `dist[v]`, set `path[v] = u`, mark
      `updated = True`.
   c. If not `updated`, break early (distances are final).
3. Negative-cycle check: run one more pass over all edges; if any relaxation
   still improves a distance, a reachable negative cycle exists → return `None`.
4. Return `dist`.

**Worked Example (Dry Run):**
```
Directed weighted graph, 5 vertices, 9 edges (only edge (4→3) is negative):

The path that wins because of the negative edge:
     4           3           -5
  0 ────▶ 1 ────▶ 4 ────────▶ 3
  │       ▲
  │       │ 1
  2       │
  ▼       │
  2 ──────┘
  (0 → 2 → 1 → 4 → 3 has total 2 + 1 + 3 − 5 = 1)

Full edge list (u→v, w): (0,1,4) (0,2,2) (1,2,3) (1,3,2) (1,4,3)
                          (2,1,1) (2,3,4) (2,4,5) (4,3,-5)

Rounds (relax ALL edges each round):
  Init:          dist = [0, ∞, ∞, ∞, ∞]
  Round 1:       dist = [0, 3, 2, 2, 7]
                   highlights: (0,2,2) sets dist[2]=2; then (2,1,1) improves
                   dist[1] 4→3; (4,3,-5) improves dist[3] 6→2
  Round 2:       dist = [0, 3, 2, 1, 6]
                   (1,4,3) improves dist[4] 7→6; (4,3,-5) improves dist[3] 2→1
  Round 3:       no distance changes → early termination

Final answer: dist = [0, 3, 2, 1, 6]
  Shortest paths:  0→1 = 0→2→1 = 2+1 = 3
                   0→2 = 2
                   0→3 = 0→2→1→4→3 = 2+1+3−5 = 1
                   0→4 = 0→2→1→4 = 2+1+3 = 6
```

**Code:**

```python
def bellman_ford(edges: list, V: int, src: int) -> list:
    """Shortest distances from src to every vertex; None if a negative cycle exists."""
    INF = float('inf')
    dist = [INF] * V               # dist[v] = shortest distance to v so far
    dist[src] = 0                  # distance to the source is 0
    path = [-1] * V                # path[v] = predecessor of v (for reconstruction)

    # Any simple shortest path uses at most V-1 edges, so V-1 full relax rounds.
    for _ in range(V - 1):
        updated = False
        for u, v, w in edges:      # try to improve every edge once
            # If u is reachable and going through u is cheaper, update v.
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                path[v] = u
                updated = True
        if not updated:            # nothing improved → already optimal, stop early
            break

    # Negative cycle detection: in the (V-th) extra round, a shortest path that
    # still improves must pass through a cycle of negative total weight.
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None            # negative cycle reachable from src

    return dist

# Time: O(V × E), Space: O(V)
```

**Complexity:**
- Time: O(V × E) — up to V−1 rounds, each scanning all E edges (O(V·E); the
  extra negative-cycle pass is another O(E)).
- Space: O(V) — the `dist` and `path` arrays.

**Common Mistakes & Edge Cases:**
- Skipping the `dist[u] != INF` check — relaxing from an unreachable vertex
  would turn `∞ + w` into a bogus finite value.
- Forgetting the negative-cycle pass — the algorithm would silently return
  incorrect (too-small) distances.
- A negative cycle that is NOT reachable from `src` should not trigger `None`;
  the check only inspects edges whose tail is reachable.
- `V-1` rounds is the correct number: `V` rounds would already re-relax through
  the longest possible simple path.
- Disconnected vertices keep `dist[v] = INF` — that is correct output, not a bug.

---

### Floyd-Warshall (All-Pairs Shortest Paths)

**🔗 Practice Link:** [Floyd-Warshall](https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16)

**Problem Explanation:**
Given a directed weighted graph as an adjacency matrix `graph[i][j]` = weight of
the edge `i→j` (with `graph[i][i] = 0` and `INF` where no edge exists), compute
the shortest path distance between every ordered pair of vertices. Return the
resulting V×V distance matrix. Negative weights are allowed, but negative cycles
are not (a diagonal entry would become negative).

**State Definition:**
The DP state is indexed by three things: `dp[k][i][j]` = shortest distance from
`i` to `j` using only intermediate vertices from the set `{0, 1, ..., k}`. The
"layer" `k` is which vertices we are allowed to route through; increasing `k`
monotonically grows the allowed intermediate set.

**Recurrence Relation:**
```
dp[k][i][j] = min(dp[k-1][i][j], dp[k-1][i][k] + dp[k-1][k][j])
```
Plain-English reason: when vertex `k` becomes allowed as an intermediate, a path
`i→j` either ignores `k` (previous value) or splits into `i→k` followed by
`k→j`, both of which only use intermediates from `{0..k-1}`; the DP takes the
cheaper of these two options.

**Base Cases:**
- `dp[-1][i][j] = graph[i][j]` (no intermediates allowed — just the direct edges).
- `dp[k][i][i] = 0` (an empty path to yourself costs nothing).

**Intuition (Why This Works):**
This is DP over a *growing set of allowed waypoints*, which is a valid acyclic
ordering even though the graph itself has cycles: each `k` layer depends only on
the previous layer. Since every shortest path uses only vertices from the set of
all vertices, after processing `k = V-1` every pair's true distance is final.
The classic 2D in-place version is safe because in round `k`, `dist[i][k]` and
`dist[k][j]` never change during that same round (routing through `k` twice is
never beneficial).

**Step-by-Step Procedure:**
1. Copy the input matrix into `dist` (this becomes the `k = -1` layer).
2. For each intermediate vertex `k` from `0` to `V-1`:
   a. For each source `i`: skip if `dist[i][k] == INF` (unreachable).
   b. For each target `j`: if `dist[k][j]` is finite, update
      `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`.
3. Return `dist`.

**Worked Example (Dry Run):**
```
Graph (3 vertices), direct edges as an adjacency matrix:

        0    1    2
     ┌────┬────┬────┐
   0 │  0 │  5 │  ∞ │
     ├────┼────┼────┤
   1 │  ∞ │  0 │  3 │
     ├────┼────┼────┤
   2 │  2 │  ∞ │  0 │
     └────┴────┴────┘

  k=0 (allow vertex 0 as an intermediate):
    dist[2][1] = min(∞, dist[2][0] + dist[0][1]) = min(∞, 2+5) = 7

        0    1    2
     ┌────┬────┬────┐
   0 │  0 │  5 │  ∞ │
     ├────┼────┼────┤
   1 │  ∞ │  0 │  3 │
     ├────┼────┼────┤
   2 │  2 │  7 │  0 │  ← 2→0→1 = 7
     └────┴────┴────┘

  k=1 (allow vertex 1): no improvements (5+3=8 is not better than anything).
  k=2 (allow vertex 2): dist[1][0] = min(∞, dist[1][2] + dist[2][0]) = 3+2 = 5
                        dist[0][1] = min(5, dist[0][2] + dist[2][1]) = min(5, ∞+7) = 5

Final matrix:
        0    1    2
     ┌────┬────┬────┐
   0 │  0 │  5 │  8 │   (0→1→2 = 5+3 = 8)
     ├────┼────┼────┤
   1 │  5 │  0 │  3 │   (1→2→0 = 3+2 = 5)
     ├────┼────┼────┤
   2 │  2 │  7 │  0 │
     └────┴────┴────┘
```

**Code:**

```python
def floyd_warshall(graph: list) -> list:
    """All-pairs shortest path distances; input is a VxV adjacency matrix."""
    V = len(graph)
    INF = float('inf')
    dist = [row[:] for row in graph]   # copy: the k=-1 layer (direct edges only)

    for k in range(V):                 # 'k' = newest allowed intermediate vertex
        for i in range(V):             # 'i' = source
            if dist[i][k] == INF:
                continue               # i cannot reach k → no route through k
            for j in range(V):         # 'j' = target
                if dist[k][j] != INF:
                    # cheaper: ignore k, or go i -> k -> j (both use 0..k-1 only)
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist

# Time: O(V³), Space: O(V²)
```

**Complexity:**
- Time: O(V³) — triple nested loop over k, i, j.
- Space: O(V²) — one distance matrix (the input copy).

**Common Mistakes & Edge Cases:**
- Not copying the input matrix — mutating the caller's graph is a side-effect
  bug that can corrupt later test cases.
- Checking `dist[k][j] != INF` (and `dist[i][k] != INF`) — skipping finite
  checks lets `INF + w` and `INF + INF` poison real entries.
- A negative cycle shows up as `dist[i][i] < 0` after the run; detect it
  explicitly if your problem forbids negative cycles.
- `dist[i][i] = 0` must be preserved by the input matrix, or self-paths can be
  computed as huge positive values.
- For dense graphs (V ≤ ~400) this beats running Bellman-Ford V times, but it is
  O(V³) — too slow for large sparse graphs.

---

## Longest Path and Critical Path in a DAG

A DAG (directed acyclic graph) has a topological order, which turns the graph
into a linear DP: process vertices in that order, and every vertex is finalized
before any of its outgoing neighbors. This is why the NP-hard "longest path in a
general graph" becomes polynomial on a DAG.

### Longest Path in a DAG

**🔗 Practice Link:** [Longest Path in a DAG](https://www.geeksforgeeks.org/longest-path-in-a-directed-acyclic-graph-dynamic-programming)

**Problem Explanation:**
Given a DAG with V vertices and weighted directed edges `edges = [(u, v, w)]`,
find the length of the longest path (maximum sum of edge weights along a path).
The path must start at a vertex with no incoming edges (the source; in the
implementation below, the first vertex of the topological order). Return the
total weight of the longest such path.

**State Definition:**
`dist[u]` = the maximum total weight of a path ending at `u`. Because vertices
are processed in topological order, when we relax edge `(u, v, w)` the value
`dist[u]` is already the best possible distance to `u`, so `dist[v]` can be
finalized greedily.

**Recurrence Relation:**
```
dist[v] = max(dist[v], dist[u] + w)   for every outgoing edge (u, v, w)
```
Plain-English reason: every path ending at `v` arrives via some edge `(u, v, w)`,
so the best one is the best path to `u` extended by that edge — processed in
topological order this single relaxation per edge is sufficient and exact.

**Base Cases:**
- `dist[source] = 0` (the first vertex in the topological order).
- All other `dist[v] = -∞` (unreachable so far; max-ed into later).
- Empty graph returns `0`.

**Intuition (Why This Works):**
A DAG is the perfect DP structure because a topological order gives a valid
linear dependency chain: `dist[v]` only ever depends on `dist[u]` for `u`
earlier in the order, and those are already computed. The greedy per-edge relax
(using `max` instead of Bellman-Ford's `min`) is safe only because there are no
cycles — on a general graph, longer paths would be missed. Kahn's algorithm
produces the topological order in O(V+E), and the single forward pass computes
all distances.

**Step-by-Step Procedure:**
1. Build the adjacency list `adj[u] = [(v, w), ...]` and the indegree array.
2. Run Kahn's algorithm: put all zero-indegree vertices in a queue; repeatedly
   pop a vertex `u` into `topo`, decrement the indegree of each neighbor, and
   enqueue any neighbor whose indegree hits 0.
3. Initialize `dist = [-∞] * V` and set `dist[topo[0]] = 0`.
4. For each `u` in `topo`: if `dist[u]` is finite, relax every edge
   `(v, w)`: `dist[v] = max(dist[v], dist[u] + w)`.
5. Return `max(dist)`.

**Worked Example (Dry Run):**
```
DAG with 6 vertices:

  0 ──5──▶ 1 ──6──▶ 3 ──(-1)──▶ 4 ──(-2)──▶ 5
  │        │        ▲            ▲
  3        2        │            │
  ▼        ▼        │            │
  2 ──7──▶ 3 ───────┘            │
  │                              │
  ├──────4──▶ 4 ─────────────────┘
  │
  └──────2──▶ 5

Edges: (0,1,5) (0,2,3) (1,2,2) (1,3,6) (2,4,4) (2,5,2) (2,3,7) (3,4,-1) (4,5,-2)

Topological order: 0, 1, 2, 3, 4, 5   (indegrees 0,1,2,2,2,2 → Kahn's queue)

DP pass:
  dist[0] = 0
  Process 0:  dist[1] = max(-∞, 0+5) = 5;   dist[2] = max(-∞, 0+3) = 3
  Process 1:  dist[2] = max(3, 5+2) = 7;    dist[3] = max(-∞, 5+6) = 11
  Process 2:  dist[3] = max(11, 7+7) = 14;  dist[4] = max(-∞, 7+4) = 11
              dist[5] = max(-∞, 7+2) = 9
  Process 3:  dist[4] = max(11, 14-1) = 13
  Process 4:  dist[5] = max(9, 13-2) = 11

Final: dist = [0, 5, 7, 14, 13, 11]  →  longest path = 14  (0 → 1 → 2 → 3)
```

**Code:**

```python
def longest_path_dag(V: int, edges: list) -> int:
    """Longest path in a DAG, measured by the sum of edge weights."""
    adj = [[] for _ in range(V)]
    indeg = [0] * V
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1                # count incoming edges for Kahn's algorithm

    # Step 1: topological sort via Kahn's BFS.
    from collections import deque
    q = deque([i for i in range(V) if indeg[i] == 0])   # start from all sources
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1            # remove edge u→v
            if indeg[v] == 0:        # all prerequisites done → v is ready
                q.append(v)

    # Step 2: DP in topological order. Max over max because it's a LONGEST path.
    dist = [float('-inf')] * V
    dist[topo[0]] = 0 if V > 0 else 0   # the first topo vertex is the source
    for u in topo:
        if dist[u] != float('-inf'):    # skip unreachable vertices
            for v, w in adj[u]:
                dist[v] = max(dist[v], dist[u] + w)   # extend path u → v

    return max(dist) if dist else 0

# Time: O(V + E), Space: O(V + E)
```

**Complexity:**
- Time: O(V + E) — Kahn's algorithm plus one pass over every edge.
- Space: O(V + E) — adjacency list and indegree/topo arrays.

**Common Mistakes & Edge Cases:**
- Applying this to a cyclic graph: the topological sort fails (fewer than V
  vertices output) and the DP silently produces wrong results — detect leftover
  vertices and treat them as a cycle.
- Using `max` on a graph with cycles would be incorrect anyway; longest path is
  NP-hard in general graphs, so the DAG assumption is load-bearing.
- Only `dist[topo[0]]` is seeded to 0. If a problem asks for the longest path
  starting at ANY vertex, seed every zero-indegree vertex to 0 instead.
- The empty graph (`V = 0`) must return 0, not crash on `topo[0]`.
- Negative weights are allowed on DAGs and the algorithm handles them; `-∞`
  seeding keeps unreachable vertices from faking a "path".

---

### Critical Path (Project Scheduling) in a DAG

**🔗 Practice Link:** [Critical Path](https://www.geeksforgeeks.org/find-longest-path-directed-acyclic-graph)

**Problem Explanation:**
Given a set of tasks (vertices) with durations (edge weights representing
dependencies: task `u` must finish before task `v`, taking `w` time units),
find the *critical path*: the longest dependency chain, whose total length is the
earliest time the whole project can finish. Return the total project duration and
the list of tasks with zero slack (the critical tasks — delaying any of them
delays the whole project).

**State Definition:**
Two arrays:
- `earliest[u]` = earliest start time of task `u` (max over all parents: parent
  start + dependency duration).
- `latest[u]` = latest start time of task `u` that still lets the project finish
  in the minimum total time (min over all children: child start − duration).
A task `u` is critical iff `earliest[u] == latest[u]` (zero slack).

**Recurrence Relation:**
```
Forward pass:  earliest[v] = max(earliest[v], earliest[u] + w)   for edge u→v
Backward pass: latest[u]   = min(latest[u],   latest[v] - w)    for edge u→v
```
Plain-English reason: a task cannot start until its slowest predecessor chain
completes (forward max), and to keep the project on schedule a task cannot start
later than its tightest successor allows (backward min); tasks whose start
window has zero width lie on the critical path.

**Base Cases:**
- `earliest[u] = 0` for every task (the max relaxes these upward).
- `latest[u] = total_time` (the project finish time) for every task, so the
  backward min relaxes these downward.
- Tasks with no predecessors start at 0; tasks with no successors must finish by
  `total_time`.

**Intuition (Why This Works):**
A DAG has a topological order, so the forward pass is a longest-path DP (like the
previous problem) computing the earliest feasible schedule, and its max value is
the project duration. Reversing the topological order makes the backward pass a
"latest start" DP that computes, for each task, the latest time it can begin
without pushing the finish past the minimum. The slack of a task is the width of
its start window; tasks with zero slack force the project length and are exactly
the critical path.

**Step-by-Step Procedure:**
1. Build the adjacency list and indegree array; run Kahn's algorithm to get
   `topo`.
2. Forward pass: for each `u` in `topo`, relax all edges `u→v`:
   `earliest[v] = max(earliest[v], earliest[u] + w)`.
3. Set `total_time = max(earliest)`.
4. Backward pass: initialize `latest = [total_time] * V`; for each `u` in
   `reversed(topo)`, relax all edges `u→v`:
   `latest[u] = min(latest[u], latest[v] - w)`.
5. Collect `critical = [i for i in range(V) if earliest[i] == latest[i]]`.
6. Return `(total_time, critical)`.

**Worked Example (Dry Run):**
```
Project DAG (task dependencies, durations as edge weights):

  0 ──3──▶ 1 ──4──▶ 3 ──2──▶ 4     ← the critical chain (0→1→3→4 = 9)
   │                    ▲
   └────2──▶ 2 ──1──────┘          (0→2 = 2, 2→3 = 1)

Edges: (0,1,3) (0,2,2) (1,3,4) (2,3,1) (3,4,2)
Topological order: 0, 1, 2, 3, 4

Forward pass (earliest start):
  earliest = [0, 0, 0, 0, 0]
  Process 0: earliest[1] = max(0, 0+3) = 3;  earliest[2] = max(0, 0+2) = 2
  Process 1: earliest[3] = max(0, 3+4) = 7
  Process 2: earliest[3] = max(7, 2+1) = 7
  Process 3: earliest[4] = max(0, 7+2) = 9
  total_time = 9

Backward pass (latest start), latest init = [9,9,9,9,9]:
  Process 4: no edges
  Process 3: latest[3] = min(9, 9-2) = 7
  Process 2: latest[2] = min(9, 7-1) = 6
  Process 1: latest[1] = min(9, 7-4) = 3
  Process 0: latest[0] = min(9, 3-3, 6-2) = 0

Slack check (earliest == latest):
  task 0: 0 == 0 ✓    task 1: 3 == 3 ✓    task 2: 2 == 6 ✗
  task 3: 7 == 7 ✓    task 4: 9 == 9 ✓

Answer: total_time = 9, critical tasks = [0, 1, 3, 4]
```

**Code:**

```python
def critical_path_tasks(V: int, edges: list) -> tuple:
    """Return (total project time, list of critical tasks with zero slack)."""
    adj = [[] for _ in range(V)]
    indeg = [0] * V
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1

    # Topological order (Kahn's BFS) — required for both passes below.
    from collections import deque
    q = deque([i for i in range(V) if indeg[i] == 0])
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    # Forward pass: earliest start = longest chain of predecessors (longest path).
    earliest = [0] * V
    for u in topo:
        for v, w in adj[u]:
            earliest[v] = max(earliest[v], earliest[u] + w)

    total_time = max(earliest)       # project finishes when the longest chain ends

    # Backward pass: latest start = what the tightest successor allows.
    latest = [total_time] * V
    for u in reversed(topo):
        for v, w in adj[u]:
            latest[u] = min(latest[u], latest[v] - w)

    # Critical tasks have no slack: they must start at their earliest possible time.
    critical = [i for i in range(V) if earliest[i] == latest[i]]

    return total_time, critical

# Time: O(V + E), Space: O(V + E)
```

**Complexity:**
- Time: O(V + E) — topological sort plus two linear passes.
- Space: O(V + E) — adjacency list plus three linear arrays.

**Common Mistakes & Edge Cases:**
- Running the backward pass in forward topological order — the pass must use
  `reversed(topo)` so every child's `latest` is final before its parents read it.
- Forgetting that a task's `latest` must consider ALL its successors (use `min`
  over every edge), otherwise the schedule can exceed `total_time`.
- Multiple disconnected components: `max(earliest)` handles them, but critical
  tasks are found per component — there can be more than one critical path.
- Vertices with no outgoing edges keep `latest = total_time` and (if their
  `earliest` also equals it) are always critical — that is correct.
- If the graph has a cycle, Kahn's algorithm outputs fewer than V vertices;
  detect and reject the input before trusting the answer.

---

## Hamiltonian Paths and TSP (Bitmask DP)

These problems require visiting every vertex exactly once. The DP state must
remember which vertices were already visited — that is an exponential amount of
information, so we encode the visited set as a bitmask: `dp[mask][last]` where
`mask` is a V-bit integer (bit `i` set = vertex `i` visited) and `last` is the
vertex the path currently ends at.

### Shortest Hamiltonian Path

**🔗 Practice Link:** [Shortest Hamiltonian Path](https://www.geeksforgeeks.org/travelling-salesman-problem-using-dynamic-programming)

**Problem Explanation:**
Given a complete directed weighted graph on `n` vertices, represented as an
adjacency matrix `graph[i][j]` = cost of moving from `i` to `j`, find the
cheapest path that starts at vertex 0, visits every other vertex exactly once,
and does NOT need to return to the start. Return the minimum total cost. This is
the "shortest path that visits all nodes" problem.

**State Definition:**
`dp[mask][last]` = the minimum cost of a path that has visited exactly the
vertices in `mask` and currently ends at vertex `last` (where `last` is always a
vertex in `mask`). The size of the table is `2^n × n`.

**Recurrence Relation:**
```
dp[mask | (1 << nxt)][nxt] = min(dp[mask | (1 << nxt)][nxt],
                                 dp[mask][last] + graph[last][nxt])
for every nxt not in mask
```
Plain-English reason: extending a valid partial path to a new vertex `nxt` costs
the existing path's cost plus the edge `last → nxt`, and we try every possible
extension, keeping the cheapest arrival at each `(mask, last)` state.

**Base Cases:**
- `dp[1 << i][i] = 0` for the starting vertex (vertex 0), `∞` for every other
  single-vertex state (we are forced to start at 0).
- Only states where `last` is in `mask` are meaningful; others stay `∞`.

**Intuition (Why This Works):**
The brute-force approach would try `(n-1)!` orderings; DP collapses all
orderings that visit the same set and end at the same vertex into one state,
because their future cost depends only on the set visited and the last vertex —
the internal ordering is irrelevant. Increasing `mask` is a valid DP order: every
transition adds exactly one bit, so all states with fewer visited vertices are
computed first. This brings the time down to O(2ⁿ·n²), feasible for `n ≤ 20`.

**Step-by-Step Procedure:**
1. Let `n = len(graph)`; initialize `dp = [[INF] * n for _ in range(1 << n)]`.
2. Seed `dp[1][0] = 0` (vertex 0 visited, cost 0); all other single-vertex
   states stay `∞`.
3. For `mask` from `0` to `2^n - 1`:
   a. For each `last` in `range(n)`: skip if `last` not in `mask` or
      `dp[mask][last] == INF`.
   b. For each `nxt` in `range(n)`: skip if `nxt` already in `mask`; otherwise
      relax `dp[mask | (1 << nxt)][nxt]` with
      `dp[mask][last] + graph[last][nxt]`.
4. Answer = `min(dp[(1 << n) - 1])` — any vertex can be the final one, since no
   return trip is required.

**Worked Example (Dry Run):**
```
n = 4, costs (symmetric example):

     0  1   2   3
   ┌─────────────────┐
 0 │ 0  10  15  20   │
 1 │10  0   35  25   │
 2 │15 35   0   30   │
 3 │20 25  30   0    │
   └─────────────────┘

Key states (showing only the best entries):
  dp[0001][0] = 0                                (start at 0)
  dp[0011][1] = dp[0001][0] + 10 = 10            (0→1)
  dp[0101][2] = dp[0001][0] + 15 = 15            (0→2)
  dp[1001][3] = dp[0001][0] + 20 = 20            (0→3)
  dp[1011][3] = dp[0011][1] + 25 = 35            (0→1→3)
  dp[1111][2] = dp[1011][3] + 30 = 65            (0→1→3→2)
  dp[1111][3] = dp[1011][2] + ...  → stays higher

Final: min over dp[1111] = 65  (path 0 → 1 → 3 → 2)
```

**Code:**

```python
def shortest_hamiltonian_path(graph: list) -> int:
    """Cheapest path visiting every vertex exactly once, starting at vertex 0."""
    n = len(graph)
    INF = float('inf')
    # dp[mask][last] = min cost to reach state (visited set = mask, end = last)
    dp = [[INF] * n for _ in range(1 << n)]
    for i in range(n):
        # Only vertex 0 is allowed as a starting point; others stay INF.
        dp[1 << i][i] = 0 if i == 0 else INF

    for mask in range(1 << n):            # grow the visited set bit by bit
        for last in range(n):
            if not (mask & (1 << last)):  # 'last' must actually be in the mask
                continue
            if dp[mask][last] == INF:     # unreachable state
                continue
            for nxt in range(n):
                if mask & (1 << nxt):     # already visited — can't revisit
                    continue
                # Extend the path by edge last→nxt and keep the cheaper arrival.
                new_mask = mask | (1 << nxt)
                dp[new_mask][nxt] = min(dp[new_mask][nxt],
                                        dp[mask][last] + graph[last][nxt])

    full_mask = (1 << n) - 1
    # No return to start needed: the path may end at any vertex.
    return min(dp[full_mask][i] for i in range(n))

# Example: n=4, graph = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
# Answer: 10 + 25 + 30 = 65 (path: 0→1→3→2)

# Time: O(2^n × n²), Space: O(2^n × n)
```

**Complexity:**
- Time: O(2ⁿ·n²) — for each of the 2ⁿ masks, n candidate `last` vertices each
  try up to n extensions.
- Space: O(2ⁿ·n) — the dp table. Feasible for n ≤ 20 (about 20 million states).

**Common Mistakes & Edge Cases:**
- Forgetting the `mask & (1 << last)` guard — states whose "last" vertex isn't
  in the mask are nonsense and would poison the transitions.
- Forgetting the `mask & (1 << nxt)` guard — revisiting a vertex breaks the
  "exactly once" rule.
- Answering `min(dp[full_mask])` instead of `min(dp[full_mask][i] + graph[i][0])`:
  this version does NOT return to the start; that difference is what separates a
  Hamiltonian path from a TSP tour.
- `n = 1`: `dp[1][0] = 0`, answer `0` (a single vertex path costs nothing).
- Large n (n > 20) blows up memory — the table alone is 2ⁿ·n entries.

---

### Traveling Salesman Problem (TSP)

**🔗 Practice Link:** [Traveling Salesman Problem](https://www.geeksforgeeks.org/travelling-salesman-problem-using-dynamic-programming)

**Problem Explanation:**
Given a complete weighted graph where `graph[i][j]` is the cost of traveling from
city `i` to city `j`, find the cheapest route that starts at city 0, visits every
other city exactly once, and returns to city 0. Return the minimum total cost.
TSP is identical to the Hamiltonian path above except for the mandatory return
edge.

**State Definition:**
`dp[mask][last]` = the minimum cost of a tour *prefix* that has visited exactly
the cities in `mask` and currently stands at `last`. The full tour closes with
the edge `last → 0`. The table has `2^n × n` states.

**Recurrence Relation:**
```
dp[mask | (1 << nxt)][nxt] = min(dp[mask | (1 << nxt)][nxt],
                                 dp[mask][last] + graph[last][nxt])
answer = min(dp[full_mask][i] + graph[i][0] for i in 1..n-1)
```
Plain-English reason: extensions are identical to the Hamiltonian path; the only
new part is the closing step, where the best complete tour is the cheapest full
path ending at some `i` plus the return edge `i → 0`.

**Base Cases:**
- `dp[1][0] = 0` (only city 0 visited, standing at 0).
- All other single-city states `∞`.
- Answer only considers `i` with a valid return edge (`graph[i][0] > 0`).

**Intuition (Why This Works):**
Any TSP tour is "some ordering of the other n−1 cities plus the closing edge", so
its cost splits into a Hamiltonian-path prefix cost plus `graph[last][0]`. Since
the prefix cost depends only on (visited set, last city), the same bitmask table
solves it; the memoized (top-down) and tabulated (bottom-up) implementations
below are the same DP expressed two ways. `graph[i][0] > 0` is used as the "edge
exists" test, so treat a 0-cost return edge as missing (or build the matrix with
`INF` for missing edges).

**Step-by-Step Procedure:**
1. `n = len(graph)`; build `dp = [[INF] * n for _ in range(1 << n)]`; seed
   `dp[1][0] = 0`.
2. For each `mask`, for each `last` in the mask with a finite cost, for each
   unvisited `nxt`: relax `dp[mask | (1 << nxt)][nxt]`.
3. After all masks, let `full_mask = (1 << n) - 1`.
4. Answer = `min(dp[full_mask][i] + graph[i][0] for i in range(n) if graph[i][0] > 0)`.
5. The memoized version does the same recursion top-down: stop when `mask` is
   full and return `graph[pos][0]`.

**Worked Example (Dry Run):**
```
n = 4, same cost matrix as the Hamiltonian path example:
  0→1=10, 0→2=15, 0→3=20; 1→3=25; 3→2=30; 2→0=15  (symmetric)

Trace of the optimal tour 0 → 1 → 3 → 2 → 0:
  dp[0001][0] = 0              (start)
  dp[0011][1] = 0 + 10 = 10    (0→1)
  dp[1011][3] = 10 + 25 = 35   (1→3)
  dp[1111][2] = 35 + 30 = 65   (3→2)
  Close: 65 + graph[2][0] = 65 + 15 = 80

Full answer = min(dp[1111][i] + graph[i][0]) = 80
  (path 0→1→3→2→0 = 10+25+30+15; the reverse tour 0→2→3→1→0 is also 80)
```

**Code:**

```python
def tsp_memo(graph: list) -> int:
    """TSP via memoized top-down DP. Returns min tour cost (start = city 0)."""
    n = len(graph)
    INF = float('inf')
    memo = {}

    def dp(mask: int, pos: int) -> int:
        # All cities visited: close the tour by returning to city 0.
        if mask == (1 << n) - 1:
            return graph[pos][0] if graph[pos][0] > 0 else INF  # 0 = 'no edge'
        key = (mask, pos)              # memoize on (visited set, current city)
        if key in memo:
            return memo[key]
        best = INF
        for city in range(n):
            if mask & (1 << city) or graph[pos][city] == 0:
                continue               # skip visited cities and missing edges
            # Visit 'city' next: pay edge pos→city plus the rest recursively.
            best = min(best, graph[pos][city] + dp(mask | (1 << city), city))
        memo[key] = best
        return best

    return dp(1, 0)                    # start: only city 0 visited


def tsp_tab(graph: list) -> int:
    """TSP via iterative bottom-up DP. Returns min tour cost (start = city 0)."""
    n = len(graph)
    INF = 10**9                        # large finite sentinel (safe with ints)
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0                       # base: only city 0 visited, cost 0

    for mask in range(1 << n):         # grow the visited set
        for last in range(n):
            if not (mask & (1 << last)):
                continue               # 'last' must be in the visited set
            if dp[mask][last] == INF:
                continue               # unreachable state
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue           # already visited — no revisits allowed
                new_mask = mask | (1 << nxt)
                dp[new_mask][nxt] = min(dp[new_mask][nxt],
                                        dp[mask][last] + graph[last][nxt])

    full_mask = (1 << n) - 1
    # Close the tour: every completed path + its return edge to city 0.
    return min(dp[full_mask][i] + graph[i][0] for i in range(n) if graph[i][0] > 0)

# Time: O(2^n × n²), Space: O(2^n × n)
# Feasible for n ≤ 20
```

**Complexity:**
- Time: O(2ⁿ·n²) — n² transitions per mask, 2ⁿ masks.
- Space: O(2ⁿ·n) — the memo/table. Feasible for n ≤ 20.

**Common Mistakes & Edge Cases:**
- Forgetting the return edge: without `+ graph[i][0]` you computed a Hamiltonian
  path, not a TSP tour.
- Using `graph[i][0] == 0` to mean "no edge" fails if a real 0-cost edge exists;
  model missing edges with `INF` explicitly in the matrix.
- The memoized base case must return `INF` (not 0) when the return edge is
  missing, or the answer is silently understated.
- Overlapping subproblems are huge; do not brute-force permutations — the whole
  point of the bitmask table is to collapse them.
- Asymmetric matrices are fine; the DP never assumes `graph[i][j] == graph[j][i]`.

---

### Shortest Hamiltonian Path Without Returning to Start

**🔗 Practice Link:** [Shortest Hamiltonian Path Without Returning to Start](https://www.geeksforgeeks.org/travelling-salesman-problem-using-dynamic-programming)

**Problem Explanation:**
Same problem as the shortest Hamiltonian path — visit all vertices exactly once,
starting at vertex 0, with no return trip — but with the slightly different
initialization `dp[1][0] = 0`. This variant is listed separately because the
answer is `min(dp[full_mask])` with no closing edge. Return the minimum cost.

**State Definition:**
Identical: `dp[mask][last]` = minimum cost of a path visiting exactly the
vertices in `mask` and ending at `last`.

**Recurrence Relation:**
```
dp[mask | (1 << nxt)][nxt] = min(dp[mask | (1 << nxt)][nxt],
                                 dp[mask][last] + graph[last][nxt])
answer = min(dp[(1 << n) - 1])
```
Plain-English reason: extension is the same bit-add transition as before; because
no return to the start is required, the answer simply takes the cheapest path
over all possible final vertices.

**Base Cases:**
- `dp[1][0] = 0` (start at vertex 0).
- All other states `∞`.

**Intuition (Why This Works):**
The two variants are the same DP table; only the final aggregation differs (with
vs. without the closing edge). This is worth calling out because the standard
TSP template's last line (`min(dp[full][i] + graph[i][0])`) is frequently
copy-pasted into path problems by mistake.

**Step-by-Step Procedure:**
1. Initialize `dp[1][0] = 0`, rest `∞`.
2. Fill the table with the same triple loop: `mask` → `last` → unvisited `nxt`.
3. Return `min(dp[full_mask])` (note: no `+ graph[i][0]`).

**Worked Example (Dry Run):**
```
n = 3, costs:
  0→1=1, 0→2=2, 1→2=3, 2→1=3

  dp[001][0] = 0
  dp[011][1] = 1   (0→1)
  dp[101][2] = 2   (0→2)
  dp[111][2] = dp[011][1] + 3 = 4   (0→1→2)
  dp[111][1] = dp[101][2] + 3 = 5   (0→2→1)

Answer: min(4, 5) = 4   (path 0→1→2; there is no closing edge)
```

**Code:**

```python
def shortest_hamiltonian_path(graph: list) -> int:
    """Cheapest path visiting all vertices exactly once (start 0, no return)."""
    n = len(graph)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0                       # base: vertex 0 visited, cost 0

    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue               # 'last' must be in the visited set
            if dp[mask][last] == INF:
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue           # never revisit a vertex
                new_mask = mask | (1 << nxt)
                dp[new_mask][nxt] = min(dp[new_mask][nxt],
                                        dp[mask][last] + graph[last][nxt])

    full_mask = (1 << n) - 1
    return min(dp[full_mask])          # no return edge needed — path ends anywhere

# Time: O(2^n × n²), Space: O(2^n × n)
```

**Complexity:**
- Time: O(2ⁿ·n²).
- Space: O(2ⁿ·n).

**Common Mistakes & Edge Cases:**
- Adding `+ graph[i][0]` at the end — that would turn this into a TSP tour and
  overstate the cost (or error on `INF` return edges).
- Assuming the path must end at a specific vertex; it may end anywhere.
- `n = 1` → answer 0; `n = 2` → answer `graph[0][1]`.

---

### Counting Hamiltonian Paths

**🔗 Practice Link:** [Counting Hamiltonian Paths](https://www.geeksforgeeks.org/hamiltonian-cycle)

**Problem Explanation:**
Given an undirected simple graph (n vertices and a list of edges `(u, v)`), count
how many Hamiltonian paths exist: paths that visit every vertex exactly once. A
Hamiltonian path and its reverse (e.g., `0→1→2` and `2→1→0`) are counted as two
distinct paths. Return the integer count.

**State Definition:**
`dp[mask][last]` = the NUMBER of ways to arrange a path that visits exactly the
vertices in `mask` and ends at `last`. Transitions add up counts instead of
taking minimums.

**Recurrence Relation:**
```
dp[mask | (1 << nxt)][nxt] += dp[mask][last]    for every edge (last, nxt), nxt not in mask
answer = sum(dp[full_mask])                     # sum over all possible last vertices
```
Plain-English reason: every arrangement that reaches `(mask, last)` can be
extended by the edge `(last, nxt)` into a distinct arrangement of the larger
set, so the counts of all predecessors add together.

**Base Cases:**
- `dp[1 << i][i] = 1` for every single vertex `i` — a path of one vertex starts
  anywhere (unlike TSP, the start is not fixed).

**Intuition (Why This Works):**
The mask+last state encodes everything that affects the future, so all partial
orderings that share a state are interchangeable — we just count how many there
are and sum them forward. Addition-based transitions make this a pure counting
DP; the symmetry with the shortest-path DP is total, with `min`/`+cost` replaced
by `+`/`*1`. Because every complete ordering ends at exactly one `last`, summing
over the last row counts each Hamiltonian path exactly once.

**Step-by-Step Procedure:**
1. Build an adjacency boolean matrix `adj` from the edge list (undirected).
2. Initialize `dp = [[0] * n for _ in range(1 << n)]`.
3. Seed every single-vertex state: `dp[1 << i][i] = 1`.
4. For each `mask`, for each `last` in the mask with a nonzero count, for each
   `nxt` not in the mask connected to `last`: `dp[mask | (1 << nxt)][nxt] += dp[mask][last]`.
5. Return `sum(dp[(1 << n) - 1])`.

**Worked Example (Dry Run):**
```
Triangle graph: n = 3, edges (0,1), (0,2), (1,2)  → complete graph K3

Seeding: dp[001][0] = 1, dp[010][1] = 1, dp[100][2] = 1

  mask=011 (0,1):  dp[011][1] = dp[001][0] = 1   (path 0→1)
                   dp[011][0] = dp[010][1] = 1   (path 1→0)
  mask=101 (0,2):  dp[101][2] = dp[001][0] = 1   (0→2)
                   dp[101][0] = dp[100][2] = 1   (2→0)
  mask=110 (1,2):  dp[110][2] = dp[010][1] = 1   (1→2)
                   dp[110][1] = dp[100][2] = 1   (2→1)
  mask=111 (all):  dp[111][0] = dp[011][1] + dp[101][2] = 1+1 = 2   (0→1→2, 0→2→1)
                   dp[111][1] = dp[011][0] + dp[110][2] = 1+1 = 2   (1→0→2, 1→2→0)
                   dp[111][2] = dp[101][0] + dp[110][1] = 1+1 = 2   (2→0→1, 2→1→0)

Answer: 2+2+2 = 6   (all 3! orderings of a triangle are valid paths)
```

**Code:**

```python
def hamiltonian_path_count(n: int, edges: list) -> int:
    """Count Hamiltonian paths (visit every vertex exactly once) in an undirected graph."""
    # adj[u][v] = True if an edge exists (undirected).
    adj = [[False] * n for _ in range(n)]
    for u, v in edges:
        adj[u][v] = adj[v][u] = True

    # dp[mask][last] = number of arrangements visiting exactly 'mask', ending at 'last'
    dp = [[0] * n for _ in range(1 << n)]

    # A one-vertex path can start at ANY vertex (the start is not fixed here).
    for i in range(n):
        dp[1 << i][i] = 1

    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)) or dp[mask][last] == 0:
                continue               # 'last' not in set, or this state is unreachable
            for nxt in range(n):
                if mask & (1 << nxt) or not adj[last][nxt]:
                    continue           # already visited, or no edge to extend on
                # Every arrangement reaching (mask, last) yields one new
                # arrangement reaching (mask+nxt, nxt), so we ADD the counts.
                dp[mask | (1 << nxt)][nxt] += dp[mask][last]

    # Every Hamiltonian path ends at exactly one vertex: sum over all of them.
    return sum(dp[(1 << n) - 1])

# Time: O(2^n × n²), Space: O(2^n × n)
```

**Complexity:**
- Time: O(2ⁿ·n²).
- Space: O(2ⁿ·n).

**Common Mistakes & Edge Cases:**
- Forgetting that the start is NOT fixed (unlike TSP): seeding must set every
  single-vertex state to 1, or paths starting at non-zero vertices are lost.
- Treating the graph as directed when the input is undirected — remember to set
  `adj[u][v] = adj[v][u] = True`.
- Counting each path twice: a Hamiltonian path and its reverse are both valid
  DISTINCT paths (this is the standard definition for undirected graphs);
  divide by 2 only if the problem explicitly wants "up to reversal".
- `n = 1` → count is 1. A graph with no edges and n ≥ 2 → count is 0.
- Reusing the cost-based TSP template without swapping `min`/`+` for `+` — the
  aggregation operator changes the whole meaning.

---

## Summary Table & Quick Reference

```
┌──────────────────────────┬─────────────────────────┬──────────┬──────────┬────────────────────────────────┐
│ Problem                  │ Approach                │ Time     │ Space    │ When to Use                    │
├──────────────────────────┼─────────────────────────┼──────────┼──────────┼────────────────────────────────┤
│ Bellman-Ford             │ Edge relaxation ×V-1    │ O(V×E)   │ O(V)     │ Single source, neg edges OK   │
│ Floyd-Warshall           │ DP over intermediates   │ O(V³)    │ O(V²)    │ All-pairs shortest paths       │
│ Longest Path DAG         │ Topo sort + DP          │ O(V+E)   │ O(V)     │ DAG + longest path             │
│ Critical Path            │ Forward + backward pass │ O(V+E)   │ O(V)     │ Task scheduling / project mgmt │
│ Shortest Hamiltonian     │ Bitmask dp[mask][last]  │ O(2ⁿn²) │ O(2ⁿn)  │ Visit all nodes, shortest path │
│ TSP                      │ Bitmask + return        │ O(2ⁿn²) │ O(2ⁿn)  │ Visit all, return to start     │
│ Hamiltonian Path Count   │ Bitmask counting DP     │ O(2ⁿn²) │ O(2ⁿn)  │ Count all valid paths          │
└──────────────────────────┴─────────────────────────┴──────────┴──────────┴────────────────────────────────┘
```

### Bitmask DP Pattern for TSP/Hamiltonian

```python
# Universal bitmask DP template for graph traversal (TSP flavour):
def bitmask_tsp_template(graph: list, start: int = 0) -> int:
    """Shortest tour visiting every vertex exactly once and returning to start."""
    n = len(graph)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1 << start][start] = 0              # base: only 'start' visited, cost 0

    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue                   # 'last' is not in the mask
            if dp[mask][last] == INF:
                continue                   # unreachable state
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue               # 'nxt' already visited
                new_mask = mask | (1 << nxt)
                dp[new_mask][nxt] = min(dp[new_mask][nxt],
                                        dp[mask][last] + graph[last][nxt])

    full_mask = (1 << n) - 1
    # Close the tour with edge i → start. For a Hamiltonian PATH (no return),
    # instead return min(dp[full_mask]); for COUNTING, use '+= dp[mask][last]'
    # instead of min and seed every single-vertex state with 1.
    closing = [dp[full_mask][i] + graph[i][start] for i in range(n)
               if i != start and graph[i][start] < INF]
    return min(closing) if closing else dp[full_mask][start]

# Feasible for n ≤ 20; the table has 2^n × n entries.
```

### Bitmask Visualization for n=4

```
mask = 0000: no cities visited
mask = 0001: city 0 visited
mask = 0011: cities 0,1 visited
mask = 1011: cities 0,1,3 visited
mask = 1111: all cities visited (full_mask)

Transitions:
  From mask=0011 (0,1 visited), last=1:
    → try nxt=2: mask=0111, nxt=2
    → try nxt=3: mask=1011, nxt=3

  From mask=0111 (0,1,2 visited), last=2:
    → try nxt=3: mask=1111, nxt=3  (all visited!)
```
