# Bitmask DP - Complete Guide

## What is Bitmask DP?

Bitmask DP uses a single integer to represent which elements are selected. Each bit of the integer is a flag: bit `k` set to 1 means element `k` is in the set, bit `k` set to 0 means it is not.

- `mask = 0b0011` means elements 0 and 1 are picked (element 2 is not).
- `dp[mask][i]` = optimal value for the problem when the visited/selected set is `mask` and we end at node/task `i`.

**Why it matters:** the number of distinct subsets of `n` elements is `2^n`, so we get an exponential but structured state space.

**Common bit operations:**

```
mask | (1 << k)         -> pick/set element k
mask & (1 << k)         -> test if bit k is set (nonzero means yes)
mask & ~(1 << k)        -> clear/remove element k
mask ^ (1 << k)         -> toggle element k
(mask >> k) & 1         -> get the value of bit k
bin(mask).count('1')    -> popcount (number of set bits)
mask & -mask            -> lowest set bit only (isolates the least-significant 1)
```

**When to use bitmask DP:**
- `n <= 20` because `2^20 ~ 1 million` states and `2^n * n^2` must stay feasible.
- Elements have binary states (selected / not selected).
- `dp[mask][last]` is the right shape when the ORDER matters (path problems, TSP, Hamiltonian paths).

---

## Hamiltonian Path & TSP Problems

### Shortest Hamiltonian Path (Generic Bitmask DP Template)

**Problem Explanation:**
Given `n` nodes and a cost function `cost(a, b)` = the cost to travel from node `a` to node `b`, find the minimum total cost of a path that starts at any node, visits every node **exactly once**, and may end at any node. This is the shortest Hamiltonian path. The input is `n` and a cost function; the output is the minimum path cost. Note this is NOT the TSP: there is no requirement to return to the start.

**State Definition:**
`dp[mask][last]` = the minimum cost to have visited exactly the nodes in `mask` and to currently be at node `last`. Here `mask` is an integer whose bit `k` is 1 exactly when node `k` has been visited.

**Recurrence Relation:**
```
dp[mask | (1 << nxt)][nxt] = min( dp[mask | (1 << nxt)][nxt],
                                  dp[mask][last] + cost(last, nxt) )
```
for every `last` inside `mask` and every `nxt` not inside `mask`.

Plain English: the cheapest way to end at `nxt` having visited `mask + {nxt}` is to extend some cheapest path that already ended at a node `last` in `mask` with the single edge `last -> nxt`.

**Base Cases:**
- `dp[1 << i][i] = 0` for every node `i`: a path that starts at `i` with only `i` visited costs 0.
- All other entries start at `INF` (unreachable state).
- Answer = `min(dp[(1 << n) - 1])` over all possible ending nodes.

**Intuition (Why This Works):**
The bitmask is the right state representation because the future cost depends only on *which* nodes have been visited (a set) and *where we are* — the internal order of the already-visited nodes is irrelevant to the future. The choice being made at each state is "which unvisited node do I visit next." Memoization works because there are only `n * 2^n` distinct `(mask, last)` pairs, and the optimal value of each pair is computed once, then reused by every path that ever reaches that configuration.

**Step-by-Step Procedure:**
1. Set `INF = 10**9` and `full = (1 << n) - 1`.
2. Allocate `dp` as `(1 << n)` rows by `n` columns, all filled with `INF`. Use a list comprehension, never `[[INF]*n] * (1 << n)` (that shares row references).
3. Initialize `dp[1 << i][i] = 0` for every node `i`, because any node may be the starting point.
4. Loop `mask` from `0` to `full`.
5. For each `last` in `range(n)`: skip if `last` is not a set bit of `mask`, or if `dp[mask][last] == INF`.
6. For each `nxt` in `range(n)`: skip if `nxt` is already a set bit of `mask`.
7. Relax: `dp[mask | (1 << nxt)][nxt] = min(dp[mask | (1 << nxt)][nxt], dp[mask][last] + cost_fn(last, nxt))`.
8. After all masks are processed, return `min(dp[full])`.
9. (Optional) store a parent table `(mask, last)` to reconstruct the actual path.

**Worked Example (Dry Run):**
Let `n = 3` with cost matrix:

```
     0  1  2
0  [ 0, 2, 9]
1  [ 2, 0, 1]
2  [ 9, 1, 0]
```

Initialize: `dp[001][0] = 0`, `dp[010][1] = 0`, `dp[100][2] = 0` (start anywhere, cost 0).

Process masks in increasing order (binary):
- `mask=001` ({0}), last=0, cost 0:
  - `nxt=1` -> `dp[011][1] = 0 + 2 = 2`
  - `nxt=2` -> `dp[101][2] = 0 + 9 = 9`
- `mask=010` ({1}), last=1, cost 0:
  - `nxt=0` -> `dp[011][0] = 0 + 2 = 2`
  - `nxt=2` -> `dp[110][2] = 0 + 1 = 1`
- `mask=100` ({2}), last=2, cost 0:
  - `nxt=0` -> `dp[101][0] = 0 + 9 = 9`
  - `nxt=1` -> `dp[110][1] = 0 + 1 = 1`

- `mask=011` ({0,1}): last=1 (cost 2) -> `dp[111][2] = 2 + 1 = 3`. last=0 (cost 2) -> `dp[111][2] = min(3, 2 + 9 = 11) = 3`.
- `mask=101` ({0,2}): last=0 (cost 9) -> `dp[111][1] = 9 + 2 = 11`. last=2 (cost 9) -> `dp[111][1] = min(11, 9 + 1 = 10) = 10`.
- `mask=110` ({1,2}): last=2 (cost 1) -> `dp[111][0] = 1 + 9 = 10`. last=1 (cost 1) -> `dp[111][0] = min(10, 1 + 2 = 3) = 3`.

Final row `dp[111] = [3, 10, 3]`, so `answer = min(3, 10, 3) = 3`.

The best path is `0 -> 1 -> 2` (cost 2 + 1 = 3) or symmetrically `2 -> 1 -> 0`.

**Code:**
```python
def bitmask_template(n, cost_fn):
    """Shortest Hamiltonian path: min cost to visit all n nodes exactly once,
    starting anywhere, ending anywhere."""
    INF = 10**9
    full = (1 << n) - 1
    # dp[mask][last] = min cost of visiting exactly the nodes in `mask`,
    # currently standing at node `last`. 1<<n rows, n columns.
    dp = [[INF] * n for _ in range(1 << n)]
    for i in range(n):
        dp[1 << i][i] = 0                     # a path that starts at node i costs 0
    for mask in range(1 << n):                # enumerate every possible visited-set
        for last in range(n):
            if not (mask >> last) & 1:        # `last` must already be in the set
                continue
            if dp[mask][last] == INF:         # this state was never reached
                continue
            for nxt in range(n):              # try every possible next node
                if (mask >> nxt) & 1:         # `nxt` is already visited: skip
                    continue
                cost = cost_fn(last, nxt)     # cost of moving last -> nxt
                if cost == INF:               # no such edge exists
                    continue
                nm = mask | (1 << nxt)        # add nxt to the visited set
                dp[nm][nxt] = min(dp[nm][nxt], dp[mask][last] + cost)
    return min(dp[full])                      # best full path; may end at any node
```

**Complexity:**
- Time: `O(2^n * n^2)` — `2^n` masks, `n` choices of `last`, `n` choices of `nxt`.
- Space: `O(2^n * n)` for the DP table.

**Common Mistakes & Edge Cases:**
- Using `[[INF]*n] * (1 << n)` creates shared row objects; a change to one row corrupts all rows. Always use a list comprehension.
- Forgetting the `(mask >> last) & 1` guard lets you "extend" states whose ending node was never actually visited.
- Off-by-one on bits: node `i` is bit `i`, so its mask is `1 << i`, not `1 << (i - 1)`.
- `n = 1`: `dp[1][0] = 0`, `full = 1`, answer is `0` — a single-node path costs nothing.
- `2^n * n^2` blows up beyond `n = 20`; keep `n <= 20` inputs only.

---

### Traveling Salesman Problem (TSP)

**Problem Explanation:**
Find the shortest tour that starts at city 0, visits every other city **exactly once**, and returns to city 0. Input is an `n x n` matrix `cost` where `cost[i][j]` is the travel cost from city `i` to city `j`. Output is the minimum total tour cost. This is exactly the Hamiltonian path above plus one extra edge: the return trip from the last city back to city 0.

**State Definition:**
`dp[mask][last]` = minimum cost of a path that has visited exactly the cities in `mask` and ends at city `last`, **without** yet including the return edge. `mask` is an integer where bit `k` is 1 iff city `k` has been visited.

**Recurrence Relation:**
```
dp[mask | (1 << nxt)][nxt] = min( dp[mask | (1 << nxt)][nxt],
                                  dp[mask][last] + cost[last][nxt] )
```
for every `last` in `mask` and `nxt` not in `mask`.

Plain English: the optimal partial tour ending at `nxt` is obtained by taking the optimal partial tour ending at some `last` already in the set and appending the edge `last -> nxt`. The return cost is handled separately at the very end.

**Base Cases:**
- `dp[1][0] = 0`: start the tour at city 0 (`mask = 1` means only bit 0 is set), cost 0.
- All other entries start at `INF`.
- Final answer = `min over i of ( dp[(1 << n) - 1][i] + cost[i][0] )` for every possible last city `i`.

**Intuition (Why This Works):**
The tour is a Hamiltonian path plus one return edge. The set of visited cities (`mask`) plus the current city (`last`) completely determines the remaining choices, because the problem is symmetric in the cities still to visit. The key choice at each state is which unvisited city to go to next. Memoization is effective because the number of `(mask, last)` states is only `n * 2^n`, while the number of possible tours is `(n-1)!` — DP collapses the factorial blow-up.

**Step-by-Step Procedure:**
1. Set `INF = 10**9` and `full = (1 << n) - 1`.
2. Create `dp` with `(1 << n)` rows and `n` columns, all `INF`.
3. Initialize `dp[1][0] = 0` (start at city 0).
4. Loop `mask` from `0` to `full`.
5. Loop `last`; skip unless `last` is in `mask` and `dp[mask][last] != INF`.
6. Loop `nxt`; skip if `nxt` is already in `mask`.
7. Relax `dp[mask | (1 << nxt)][nxt]` using `cost[last][nxt]`.
8. After processing all masks, add the return edge: for each `i` from 1 to `n-1`, candidate = `dp[full][i] + cost[i][0]`.
9. Return the minimum candidate. (City 0 itself is skipped because it is the fixed start.)

**Worked Example (Dry Run):**
Classic 4-city example:

```
     0   1   2   3
0  [ 0, 10, 15, 20]
1  [10,  0, 35, 25]
2  [15, 35,  0, 30]
3  [20, 25, 30,  0]
```

Initialize `dp[0001][0] = 0`. Relevant intermediate DP values (mask in binary; `-` = INF):

```
mask   last=1   last=2   last=3
0011      10       -       -      <- 0->1
0101       -       15      -      <- 0->2
1001       -        -      20     <- 0->3
0111      50       45      -      <- 0->1->2 =45, 0->2->1 =50
1011      45        -      35     <- 0->1->3 =35, 0->3->1 =45
1101       -       50      45     <- 0->2->3 =45, 0->3->2 =50
1111      70       65      75     <- best full paths (without return)
```

Now add the return edge to city 0:
- end at 1: `70 + cost[1][0] = 70 + 10 = 80`
- end at 2: `65 + cost[2][0] = 65 + 15 = 80`
- end at 3: `75 + cost[3][0] = 75 + 20 = 95`

`answer = min(80, 80, 95) = 80`. The optimal tour is `0 -> 1 -> 3 -> 2 -> 0` (10 + 25 + 30 + 15 = 80), and equally `0 -> 2 -> 3 -> 1 -> 0`.

**Code:**
```python
def tsp_tab(cost):
    """TSP: min-cost tour starting at city 0, visiting every city once, returning to 0."""
    n = len(cost)
    INF = 10**9
    dp = [[INF] * n for _ in range(1 << n)]   # dp[mask][last] = best partial tour
    dp[1][0] = 0                              # tour starts at city 0 (only bit 0 set)
    for mask in range(1 << n):
        for last in range(n):
            if not (mask >> last) & 1:        # `last` must be a visited city
                continue
            if dp[mask][last] == INF:         # state not reachable
                continue
            for nxt in range(n):
                if (mask >> nxt) & 1:         # `nxt` already visited
                    continue
                nm = mask | (1 << nxt)        # mark nxt as visited
                dp[nm][nxt] = min(dp[nm][nxt], dp[mask][last] + cost[last][nxt])
    full = (1 << n) - 1
    ans = INF
    for i in range(1, n):                     # close the loop: return from city i to city 0
        if cost[i][0]:                        # guard: a real return edge must exist
            ans = min(ans, dp[full][i] + cost[i][0])
    return ans


def tsp_memo(cost):
    """TSP solved top-down with memoization on (mask, pos)."""
    n = len(cost)
    INF = 10**9                               # INF must be defined inside this function
    memo = {}                                 # cache: (mask, pos) -> min remaining cost

    def dp(mask, pos):
        if mask == (1 << n) - 1:              # every city visited: go back to city 0
            return cost[pos][0]
        key = (mask, pos)
        if key in memo:                       # reuse previously computed subproblem
            return memo[key]
        best = INF
        for city in range(n):
            if mask & (1 << city):            # city already visited
                continue
            if cost[pos][city] == 0:          # no edge from pos to city
                continue
            best = min(best, cost[pos][city] + dp(mask | (1 << city), city))
        memo[key] = best
        return best

    return dp(1, 0)                           # start at city 0 with {0} visited
```

**Complexity:**
- Time: `O(2^n * n^2)` — for each of `2^n` masks we loop over `n * n` (last, nxt) pairs.
- Space: `O(2^n * n)` for the DP table (tabular version); `O(2^n * n)` memo dict (top-down version).

**Common Mistakes & Edge Cases:**
- In the original `tsp_memo`, `INF` was used but never defined in scope — define it inside the function (or at module level) or you get a `NameError`.
- The `if cost[i][0]:` guard skips return edges of cost 0. If a legitimate zero-cost return edge exists, that candidate would be skipped; only use this guard when cost 0 definitely means "no edge".
- `dp[1][0] = 0` fixes the start at city 0. If the problem allows starting anywhere, initialize all `dp[1 << i][i] = 0` instead.
- A single city (`n = 1`): the loop over `i` in `range(1, 1)` is empty, so the answer stays `INF`; handle `n == 1` separately (answer 0).
- Asymmetric cost matrices (`cost[i][j] != cost[j][i]`) work fine — the recurrence only ever reads `cost[last][nxt]` forward.

---

## Subset Optimization & Counting Problems

### Assignment Problem

**Problem Explanation:**
There are `n` workers and `n` tasks, and `cost[i][j]` is the cost of assigning worker `i` to task `j`. Every worker must be assigned exactly one task and every task must be done by exactly one worker (a one-to-one matching). Find the minimum total cost assignment. Input: an `n x n` cost matrix. Output: the minimum total cost, or `-1` if no complete assignment is possible.

**State Definition:**
`dp[mask]` = the minimum total cost after processing the first `worker` workers, where `mask` is an integer whose bit `j` is 1 exactly when task `j` has already been assigned to one of those workers. A dict maps each reachable task-set to its best cost.

**Recurrence Relation:**
```
new_dp[mask | (1 << task)] = min( new_dp[mask | (1 << task)],
                                  dp[mask] + cost[worker][task] )
```
for every `task` not already set in `mask`.

Plain English: the cheapest way to assign workers `0..worker` using exactly the tasks in `mask + {task}` is to take a cheapest assignment of the earlier workers to `mask` and give the current worker the still-free `task`.

**Base Cases:**
- `dp = {0: 0}`: before any worker is processed, no tasks are used and the cost is 0.
- After all `n` workers are processed, answer = `dp.get((1 << n) - 1, -1)`: the best cost for using every task.
- `-1` is returned if the full task-set is unreachable.

**Intuition (Why This Works):**
Only *which tasks are still free* matters, not the specific order workers were assigned in — so a single bitmask over tasks fully captures the state. The choice being made is which task the current worker takes. Memoization works because, after `k` workers, only `C(n, k)` task-sets are reachable, and keeping only the best cost per set is enough: any two assignments of workers `0..k` that use the same task-set have identical future possibilities.

**Step-by-Step Procedure:**
1. Start with `dp = {0: 0}` (a dict: task-mask -> best cost).
2. Loop over workers `0` to `n-1`.
3. Create an empty `new_dp` dict for this worker.
4. For each `(mask, total)` in `dp` and each task `0` to `n-1`: skip tasks already in `mask`.
5. Compute `new_mask = mask | (1 << task)` and `new_cost = total + cost[worker][task]`.
6. Store `new_dp[new_mask] = min(new_dp.get(new_mask, big), new_cost)`.
7. Replace `dp = new_dp` and move to the next worker.
8. After the last worker, return `dp.get((1 << n) - 1, -1)`.

**Worked Example (Dry Run):**
`n = 3` workers/tasks with cost matrix:

```
     0  1  2
0  [ 2, 7, 5]
1  [ 3, 1, 9]
2  [ 8, 4, 6]
```

- Start: `dp = {0: 0}`.
- Worker 0: `{1: 2, 2: 7, 4: 5}` (task0 cost 2, task1 cost 7, task2 cost 5).
- Worker 1 (extend each mask):
  - from mask `1` (task0 taken, cost 2): task1 -> mask `3` = 2+1 = 3; task2 -> mask `5` = 2+9 = 11.
  - from mask `2` (task1 taken, cost 7): task0 -> mask `3` = 7+3 = 10 (keep 3); task2 -> mask `6` = 7+9 = 16.
  - from mask `4` (task2 taken, cost 5): task0 -> mask `5` = 5+3 = 8 (keep 5); task1 -> mask `6` = 5+1 = 6 (keep 6).
  - `dp = {3: 3, 5: 8, 6: 6}`.
- Worker 2:
  - from mask `3` (tasks 0,1; cost 3): task2 -> mask `7` = 3+6 = 9.
  - from mask `5` (tasks 0,2; cost 8): task1 -> mask `7` = 8+4 = 12 (keep 9).
  - from mask `6` (tasks 1,2; cost 6): task0 -> mask `7` = 6+8 = 14.
  - `dp = {7: 9}`.
- `full = 111 (7)`, answer = `9`. Optimal assignment: worker0->task0 (2), worker1->task1 (1), worker2->task2 (6), total 9.

**Code:**
```python
def assignment_problem(cost):
    """Minimum one-to-one assignment of n workers to n tasks."""
    n = len(cost)
    dp = {0: 0}                                # task-mask -> minimum total cost
    for worker in range(n):                    # assign one task per worker, in order
        new_dp = {}
        for mask, total in dp.items():         # every reachable task-set so far
            for task in range(n):
                if not (mask & (1 << task)):   # this task is still unassigned
                    new_mask = mask | (1 << task)      # mark the task as taken
                    new_cost = total + cost[worker][task]
                    if new_mask not in new_dp or new_cost < new_dp[new_mask]:
                        new_dp[new_mask] = new_cost    # keep only the best cost per task-set
        dp = new_dp                           # move to the next worker
    full = (1 << n) - 1
    return dp.get(full, -1)                   # -1 if the full assignment is impossible
```

**Complexity:**
- Time: `O(n * 2^n)` — `n` worker layers, each visiting up to `2^n` masks and trying `n` tasks.
- Space: `O(2^n)` — the dict holds at most one entry per task-set (two layers live at once).

**Common Mistakes & Edge Cases:**
- The worker loop must run exactly `n` times, one task per worker; the mask always gains exactly one bit per worker.
- The task-mask and worker index are different domains: bit `j` is task `j`, the loop variable is the worker. Do not confuse them.
- If `n = 0`, `dp = {0: 0}`, `full = 0`, and the answer is `0` (no workers, no tasks, no cost).
- Keep only the minimum cost per mask — keeping multiple assignments with the same task-set wastes space and is unnecessary.
- If some row/column makes a full assignment impossible, `dp` will never contain `full`, so return `-1` instead of crashing on a missing key.

---

### Maximum Weight Independent Set (Graph)

**Problem Explanation:**
Given an undirected graph with `n <= 20` vertices and vertex weights `weights[i]`, find the maximum total weight of a set of vertices with **no edge** between any two chosen vertices (an independent set). Input: `n`, a list of `(u, v)` edges, and `weights`. Output: the maximum possible total weight.

**State Definition:**
`solve(mask)` = the maximum weight of an independent set that can be chosen using only the vertices whose bits are set in `mask`. `mask` is an integer where bit `k` is 1 iff vertex `k` is still available to be picked.

**Recurrence Relation:**
```
solve(mask) = max( solve(mask without v),                 # exclude the pivot vertex v
                   weights[v] + solve(mask without v and without v's neighbours) )
```
where `v` is any vertex in `mask` (the code uses the lowest set bit).

Plain English: pick one vertex `v` as a pivot; either we do not take it (just remove `v` from consideration), or we take it and therefore must also remove every neighbour of `v`, because an independent set may not contain adjacent vertices.

**Base Cases:**
- `solve(0) = 0`: no vertices available, so no weight can be added.
- The final answer is `solve((1 << n) - 1)` — all vertices are initially available.

**Intuition (Why This Works):**
A bitmask is ideal because the only information needed is *which vertices are still usable* — the already-decided vertices never influence the future. The choice being made is "take the pivot or not," and taking it collapses the available set by removing the pivot and all its neighbours, which guarantees the no-adjacency invariant forever. Memoization works because the number of distinct masks is `2^n`, far smaller than the number of subsets we would otherwise try.

**Step-by-Step Procedure:**
1. Build `adj[v]` as a bitmask of the neighbours of `v` (for each edge `(u,v)`, set bit `v` in `adj[u]` and bit `u` in `adj[v]`).
2. Create an empty memo dict.
3. Define `solve(mask)`:
   - If `mask == 0`, return 0.
   - If `mask` is in memo, return the cached value.
4. Find the pivot `v` = index of the lowest set bit using `(mask & -mask).bit_length() - 1`.
5. Compute `exclude = solve(mask ^ (1 << v))`.
6. Compute `include = weights[v] + solve(mask & ~((1 << v) | adj[v]))`.
7. Cache and return `max(include, exclude)`.
8. Call `solve((1 << n) - 1)` and return the result.

**Worked Example (Dry Run):**
`n = 3`, edge list `[(0, 1)]`, weights `[10, 5, 7]`.

- `adj[0] = 010`, `adj[1] = 001`, `adj[2] = 000`.
- `solve(111)` (all three available): pivot `v = 0`.
  - `exclude = solve(111 ^ 001) = solve(110)` = {1, 2}:
    - pivot `v = 1`: `exclude = solve(100)` = {2} -> weight 7.
    - `include = 5 + solve(110 & ~(010 | 001)) = 5 + solve(110 & ~011) = 5 + solve(100) = 5 + 7 = 12`.
    - `solve(110) = max(7, 12) = 12` (pick vertices 1 and 2).
  - `include = 10 + solve(111 & ~(001 | 010)) = 10 + solve(111 & 100) = 10 + solve(100) = 10 + 7 = 17`.
  - `solve(111) = max(12, 17) = 17`.
- `answer = 17`, achieved by the independent set `{0, 2}` (weights 10 + 7), since vertices 0 and 2 are not adjacent.

**Code:**
```python
def max_weight_independent_set(n, edges, weights):
    """Maximum weight set of non-adjacent vertices. n <= 20."""
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v                        # store neighbours of u as a bitmask
        adj[v] |= 1 << u                        # ... and neighbours of v
    memo = {}

    def solve(mask):
        """Max independent-set weight using only the vertices set in `mask`."""
        if mask == 0:
            return 0                            # nothing left to choose from
        if mask in memo:                        # reuse the cached answer for this set
            return memo[mask]
        v = (mask & -mask).bit_length() - 1     # index of the lowest set bit (pivot vertex)
        bit = 1 << v
        exclude = solve(mask ^ bit)             # OPTION A: skip vertex v
        include = weights[v] + solve(mask & ~(bit | adj[v]))
        # OPTION B: take v, so also remove v and all its neighbours from availability
        memo[mask] = max(include, exclude)
        return memo[mask]

    return solve((1 << n) - 1)                  # start with every vertex available
```

**Complexity:**
- Time: `O(2^n)` — each of the `2^n` masks is solved once (the `~` removal only ever shrinks the mask).
- Space: `O(2^n)` for the memo dict (plus recursion depth at most `n`).

**Common Mistakes & Edge Cases:**
- The pivot trick `(mask & -mask).bit_length() - 1` extracts the lowest set bit — easy to get wrong if you copy it carelessly.
- `~` in Python is an infinite-width two's complement; `mask & ~(bit | adj[v])` is safe because `mask` bounds the result. In languages with fixed-width ints (C++/Java), mask the result or use `mask ^ ((bit | adj[v]) & mask)` to avoid sign/overflow issues.
- When a vertex is taken, you must remove both the vertex itself and ALL of its neighbours; removing only the vertex lets the DP pick an adjacent vertex, breaking the invariant.
- Disconnected vertices: `adj[v] == 0`, so taking `v` only removes `v` — the empty graph case returns the sum of all weights.
- The memo dictionary must key on `mask` alone — the graph structure never changes, so the available set fully determines the answer.

---

### Hamiltonian Path Count

**Problem Explanation:**
Given `n` vertices and an undirected edge list, count the number of distinct Hamiltonian paths — paths that visit every vertex exactly once. Input: `n` and a list of edges. Output: the number of such paths. A path and its reverse are counted as two different paths (order matters), and a path may start at any vertex.

**State Definition:**
`dp[mask][last]` = the number of paths that have visited exactly the vertices in `mask` and end at vertex `last`. `mask` is an integer where bit `k` is 1 iff vertex `k` has been visited.

**Recurrence Relation:**
```
dp[mask | (1 << nxt)][nxt] += dp[mask][last]
```
for every `last` in `mask` and every `nxt` not in `mask` such that the edge `(last, nxt)` exists.

Plain English: every path that ends at `last` can be extended to `nxt` along the edge `last -> nxt`, producing one new path for each existing path — so we simply add the counts.

**Base Cases:**
- `dp[1 << i][i] = 1` for every vertex `i`: one trivial path that starts and ends at `i`.
- All other entries are 0.
- Answer = `sum(dp[(1 << n) - 1][last])` over all `last` — total paths using every vertex.

**Intuition (Why This Works):**
A bitmask is the right representation because whether a vertex can be visited next depends only on which vertices are already used and on the last vertex — not on the full ordering of the previous vertices. The choice is which unvisited neighbour of `last` to extend the path to. Counting works because every path reaching a given `(mask, last)` has exactly the same set of legal continuations, so we only need to store how many paths got there.

**Step-by-Step Procedure:**
1. Build a boolean adjacency matrix `adj` from the edge list (edges are undirected, so set both `adj[u][v]` and `adj[v][u]`).
2. Create `dp` with `(1 << n)` rows and `n` columns, all 0.
3. Set `dp[1 << i][i] = 1` for all `i`.
4. Loop `mask` from `0` to `(1 << n) - 1`.
5. Loop `last`; skip if `last` is not in `mask` or `dp[mask][last] == 0`.
6. Loop `nxt`; skip if `nxt` is in `mask` or there is no edge `last -> nxt`.
7. Add: `dp[mask | (1 << nxt)][nxt] += dp[mask][last]`.
8. Return `sum(dp[(1 << n) - 1])`.

**Worked Example (Dry Run):**
`n = 3`, complete graph `K3` with edges `(0,1), (0,2), (1,2)`. Every ordering of the 3 vertices is a valid Hamiltonian path, so the expected answer is `3! = 6`.

- Initialize `dp[001][0] = 1`, `dp[010][1] = 1`, `dp[100][2] = 1`.
- `mask=001` ({0}), last=0: nxt=1 -> `dp[011][1] += 1`; nxt=2 -> `dp[101][2] += 1`.
- `mask=010` ({1}), last=1: nxt=0 -> `dp[011][0] += 1`; nxt=2 -> `dp[110][2] += 1`.
- `mask=100` ({2}), last=2: nxt=0 -> `dp[101][0] += 1`; nxt=1 -> `dp[110][1] += 1`.
- `mask=011` ({0,1}): last=0 (count 1): nxt=2 -> `dp[111][2] += 1`; last=1 (count 1): nxt=2 -> `dp[111][2] += 1`, so `dp[111][2] = 2`.
- `mask=101` ({0,2}): last=0 (1): nxt=1 -> `dp[111][1] += 1`; last=2 (1): nxt=1 -> `dp[111][1] += 1`, so `dp[111][1] = 2`.
- `mask=110` ({1,2}): last=1 (1): nxt=0 -> `dp[111][0] += 1`; last=2 (1): nxt=0 -> `dp[111][0] += 1`, so `dp[111][0] = 2`.

`answer = dp[111][0] + dp[111][1] + dp[111][2] = 2 + 2 + 2 = 6`. (The two paths per ending vertex are the two orderings that end there.)

**Code:**
```python
def count_hamiltonian_paths(n, edges):
    """Count distinct Hamiltonian paths (visit every vertex exactly once) in an
    undirected graph. Each direction of a path counts separately."""
    adj = [[False] * n for _ in range(n)]
    for u, v in edges:
        adj[u][v] = adj[v][u] = True            # undirected edge: usable both ways
    dp = [[0] * n for _ in range(1 << n)]       # dp[mask][last] = number of paths
    for i in range(n):
        dp[1 << i][i] = 1                       # one trivial path: just vertex i
    for mask in range(1 << n):
        for last in range(n):
            if not (mask >> last) & 1 or dp[mask][last] == 0:
                continue                        # `last` unused, or no path reaches it
            for nxt in range(n):
                if (mask >> nxt) & 1 or not adj[last][nxt]:
                    continue                    # `nxt` visited, or no edge last -> nxt
                dp[mask | (1 << nxt)][nxt] += dp[mask][last]   # extend every existing path
    full = (1 << n) - 1
    return sum(dp[full])                        # total over all possible ending vertices
```

**Complexity:**
- Time: `O(2^n * n^2)` — `2^n` masks, `n` choices of `last`, `n` choices of `nxt`.
- Space: `O(2^n * n)` for the DP table.

**Common Mistakes & Edge Cases:**
- The adjacency matrix must be symmetric (`adj[u][v] = adj[v][u] = True`); setting only one side makes half the paths disappear.
- The graph need not be complete: any missing edge simply contributes 0 extensions.
- `n = 1`: `dp[1][0] = 1`, answer `1` (a single-vertex path exists).
- With `n = 0` the function would misbehave (no rows/columns); require `n >= 1`.
- Counts can grow like `n!`; Python integers handle this natively, but in C++/Java this needs a 64-bit type (or modulo if the problem asks for it).

---

### Meet-in-the-Middle Knapsack (n <= 40)

**Problem Explanation:**
Given up to `n = 40` items, each with `(weight, value)`, and a knapsack `capacity`, find the maximum total value of a subset whose total weight is at most `capacity`. Output: the maximum value. Plain `O(2^n)` enumeration is impossible for `n = 40` (`2^40 ~ 10^12`), so we split the items into two halves and enumerate each half separately.

**State Definition:**
There is no DP table in the usual sense. Instead:
- `left` = sorted list of `(weight, value)` for every subset of the first `n // 2` items that fits the capacity.
- `right` = same for the second half, then reduced to Pareto-optimal entries (entries where value strictly improves as weight grows).

**Recurrence Relation:**
```
answer = max over (w_l, v_l) in left of ( v_l + best_value(right subset with weight <= capacity - w_l) )
```
where the right-side lookup is done with binary search over the Pareto-optimal list.

Plain English: every subset of all items is the union of one left-half subset and one right-half subset, so we combine every left subset with the best compatible right subset instead of enumerating all `2^n` unions.

**Base Cases:**
- The empty subset `(0, 0)` is always in both halves, so the answer is at least 0.
- If no right subset fits the remaining capacity, contribute only `v_l`.

**Intuition (Why This Works):**
`2^40` is too large, but `2^20` (about one million) per half is fine. The "meet in the middle" insight is that the answer is a pair of halves, so enumerating each half and combining with binary search costs only `2^(n/2)` per half plus `2^(n/2) * log(2^(n/2))` for the lookups. The Pareto filter is the second key idea: for the right half, once an entry `(w2, v2)` is heavier than `(w1, v1)` but not more valuable, it is dominated and can never be part of an optimal answer.

**Step-by-Step Procedure:**
1. Define `gen_subsets(start, end)`: loop `mask` from `0` to `2^(end-start) - 1`, sum the weight and value of the chosen items, and keep `(w, v)` if `w <= capacity`.
2. Sort the subset list by `(weight, value)`.
3. Build `left = gen_subsets(0, n // 2)` and `right = gen_subsets(n // 2, n)`.
4. Filter `right` to Pareto-optimal entries: keep `(w, v)` only when `v` is strictly greater than the best value seen so far.
5. Initialize `best = 0`.
6. For each `(w_l, v_l)` in `left`, compute `remain = capacity - w_l`.
7. Binary search `best_right` for the heaviest entry with weight `<= remain` (use `bisect_right`).
8. Update `best = max(best, v_l + that entry's value)`.
9. Return `best`.

**Worked Example (Dry Run):**
`items = [(2,3), (3,4), (4,5), (5,6)]`, `capacity = 5`. `n = 4`, so the split is items `[0,1]` (left) and `[2,3]` (right).

- Left half subsets of `[(2,3), (3,4)]` (all fit capacity 5):
  - `{} -> (0,0)`, `{0} -> (2,3)`, `{1} -> (3,4)`, `{0,1} -> (5,7)`.
  - `left = [(0,0), (2,3), (3,4), (5,7)]`.
- Right half subsets of `[(4,5), (5,6)]`:
  - `{} -> (0,0)`, `{2} -> (4,5)`, `{3} -> (5,6)`, `{2,3} -> (9,11)` (weight 9 > 5, dropped).
  - `right = [(0,0), (4,5), (5,6)]` (already sorted).
- Pareto filter on `right`: keep `(0,0)` (v=0), then `(4,5)` (5>0), then `(5,6)` (6>5). `best_right = [(0,0), (4,5), (5,6)]`.
- Combine with each left entry:
  - `(0,0)`: remain 5 -> best right entry is `(5,6)` -> `0 + 6 = 6`.
  - `(2,3)`: remain 3 -> heaviest right weight `<= 3` is `(0,0)` -> `3 + 0 = 3`.
  - `(3,4)`: remain 2 -> `(0,0)` -> `4 + 0 = 4`.
  - `(5,7)`: remain 0 -> `(0,0)` -> `7 + 0 = 7`.
- `best = max(6, 3, 4, 7) = 7`. The optimal subset is `{0, 1}` (weight 5, value 7).

**Code:**
```python
import bisect

def meet_in_middle_knapsack(items, capacity):
    """
    items: list of (weight, value) pairs.
    Returns max value with total weight <= capacity.
    n can be up to ~40 because we enumerate 2^(n/2) subsets, not 2^n.
    """
    n = len(items)

    def gen_subsets(start, end):
        """Sorted list of (weight, value) for every subset of items[start:end]."""
        res = []
        size = end - start
        for mask in range(1 << size):            # enumerate all 2^size subsets
            w = v = 0
            for j in range(size):                # sum up the chosen items
                if mask & (1 << j):
                    w += items[start + j][0]
                    v += items[start + j][1]
            if w <= capacity:                    # only feasible subsets
                res.append((w, v))
        return sorted(res)                       # sorted by weight, then value

    left = gen_subsets(0, n // 2)                # first-half subsets
    right = gen_subsets(n // 2, n)               # second-half subsets

    # Pareto filter: keep only right subsets where value strictly improves as weight grows.
    best_right = []
    max_v = -1
    for w, v in right:
        if v > max_v:                            # heavier but strictly better value
            best_right.append((w, v))
            max_v = v

    best = 0
    for w_l, v_l in left:                        # fix a left subset
        remain = capacity - w_l                  # remaining capacity for the right half
        idx = bisect.bisect_right(best_right, (remain, float("inf"))) - 1
        if idx >= 0:                             # best right subset that fits in `remain`
            best = max(best, v_l + best_right[idx][1])
    return best
```

**Complexity:**
- Time: `O(2^(n/2) * log(2^(n/2)))` — enumerate `2^(n/2)` subsets per half, plus a binary search per left subset.
- Space: `O(2^(n/2))` — one list of subsets per half.

**Common Mistakes & Edge Cases:**
- The halves must cover all items: `[0 : n//2]` and `[n//2 : n]`. If `n` is odd, the second half has one more item — the code handles this correctly.
- The Pareto filter only works because `right` is sorted by weight first; filtering an unsorted list silently drops valid entries.
- The empty subset `(0, 0)` is generated by `mask = 0` and guarantees the answer is at least 0.
- `bisect_right(..., (remain, inf))` finds the last entry with weight `<= remain`; using `bisect_left` here would miss the boundary entry of weight exactly `remain`.
- If every item is heavier than `capacity`, both halves still contain `(0, 0)`, so the answer is `0`.



