# Bitmask DP — Extra Problems

Additional bitmask DP problems covering scheduling, subset partitioning,
worker assignment, and combinatorial optimization. Shortest Hamiltonian
Path, TSP, Hamiltonian Path Count, Assignment Problem, Max Weight
Independent Set, and Meet-in-the-Middle Knapsack are in the main guide.

---

## 1. Shortest Hamiltonian Path — Hard

### Problem Explanation
Given a complete weighted graph on `n` vertices (adjacency matrix), find
the minimum cost path starting at vertex 0 that visits every vertex
exactly once. Unlike TSP, no return edge is needed.

### State Definition
`dp[mask][last]` = minimum cost path visiting exactly vertices in `mask`,
ending at `last`.

### Recurrence Relation
```
dp[mask | (1 << nxt)][nxt] = min(dp[mask | (1 << nxt)][nxt],
                                  dp[mask][last] + graph[last][nxt])
```
Answer = `min(dp[(1<<n)-1])` — endpoint is not fixed.

### Base Cases
- `dp[1 << 0][0] = 0`. All others `inf`.

### Intuition (Why This Works)
The bitmask encodes the visited set; the future cost depends only on
(visited set, current vertex), not the ordering. O(2^n * n^2) is
feasible for n <= 20.

### Step-by-Step Procedure
1. Init `dp[1<<0][0] = 0`, rest `inf`.
2. For each mask, for each `last` in mask, for each unvisited `nxt`: relax.
3. Return `min(dp[(1<<n)-1])`.

### Worked Example (Dry Run)
```
n=4, graph:
     0   1   2   3
  0 [ 0, 10, 15, 20]
  1 [10,  0, 35, 25]
  2 [15, 35,  0, 30]
  3 [20, 25, 30,  0]

  dp[0001][0]=0
  dp[0011][1]=10 (0->1), dp[0101][2]=15 (0->2), dp[1001][3]=20 (0->3)
  dp[1011][3]=35 (0->1->3), dp[1111][2]=65 (0->1->3->2)
  dp[0111][2]=45 (0->1->2), dp[1111][3]=65 (via other routes)
Answer: min(dp[1111]) = 65
```

### Code
```python
def shortest_hamiltonian_path(graph):
    n = len(graph)
    inf = float('inf')
    dp = [[inf] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)) or dp[mask][last] == inf:
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue
                nm = mask | (1 << nxt)
                dp[nm][nxt] = min(dp[nm][nxt],
                                  dp[mask][last] + graph[last][nxt])
    return min(dp[(1 << n) - 1])
# Time: O(2^n * n^2), Space: O(2^n * n)
```

### Complexity
- Time: O(2^n * n^2), Space: O(2^n * n).

### Common Mistakes & Edge Cases
- Adding return edge `+ graph[i][0]` is TSP, not this problem.
- `n=1`: answer is `0`.

---

## 2. Shortest Hamiltonian Cycle — Hard

### Problem Explanation
Given a complete weighted graph, find the minimum cost tour that starts
at vertex 0, visits every vertex exactly once, and returns to vertex 0.
This is the classic TSP.

### State Definition
`dp[mask][last]` = minimum cost of a partial tour visiting vertices in
`mask`, ending at `last`.

### Recurrence Relation
```
dp[mask | (1 << nxt)][nxt] = min(dp[mask | (1 << nxt)][nxt],
                                  dp[mask][last] + graph[last][nxt])
answer = min(dp[full_mask][i] + graph[i][0] for i in range(n))
```

### Base Cases
- `dp[1 << 0][0] = 0`. All others `inf`.

### Intuition (Why This Works)
Identical to Hamiltonian path DP; the only difference is adding the
closing edge from the last vertex back to vertex 0.

### Step-by-Step Procedure
1. Init `dp[1][0] = 0`, rest `inf`.
2. Fill table with triple loop.
3. Add return edge: `min(dp[full][i] + graph[i][0])`.

### Worked Example (Dry Run)
```
Same n=4 graph. Final row:
  dp[1111][1]=70, dp[1111][2]=65, dp[1111][3]=75
Add return: 70+10=80, 65+15=80, 75+20=95
Answer: 80 (tour 0->1->3->2->0)
```

### Code
```python
def tsp(graph):
    n = len(graph)
    inf = float('inf')
    dp = [[inf] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)) or dp[mask][last] == inf:
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue
                nm = mask | (1 << nxt)
                dp[nm][nxt] = min(dp[nm][nxt],
                                  dp[mask][last] + graph[last][nxt])
    full = (1 << n) - 1
    return min(dp[full][i] + graph[i][0] for i in range(n))
# Time: O(2^n * n^2), Space: O(2^n * n)
```

### Complexity
- Time: O(2^n * n^2), Space: O(2^n * n).

### Common Mistakes & Edge Cases
- Forgetting the return edge `+ graph[i][0]`.
- `graph[i][0] == 0` means no edge: handle explicitly.
- `n=1`: answer is `0`.

---

## 3. Hamiltonian Path — Count All — Medium

### Problem Explanation
Given `n` vertices and an undirected edge list, count ALL Hamiltonian
paths. A path and its reverse are distinct. Start is NOT fixed.

### State Definition
`dp[mask][last]` = number of paths visiting vertices in `mask`, ending
at `last`.

### Recurrence Relation
```
dp[mask | (1 << nxt)][nxt] += dp[mask][last]
```
for every edge `(last, nxt)` where `nxt` not in `mask`.
Answer = `sum(dp[(1<<n)-1])`.

### Base Cases
- `dp[1 << i][i] = 1` for every vertex `i`.

### Intuition (Why This Works)
Counting uses `+=` instead of `min`. Each path reaching `(mask, last)`
extends to every unvisited neighbor. Sum over all ending vertices.

### Step-by-Step Procedure
1. Build adjacency matrix.
2. Seed `dp[1<<i][i] = 1` for all `i`.
3. Extend with `+=` for each valid edge.
4. Return `sum(dp[full_mask])`.

### Worked Example (Dry Run)
```
n=3, K3 (all edges): expected 3! = 6
  dp[001][0]=1, dp[010][1]=1, dp[100][2]=1
  dp[011][1]=1 (0->1), dp[011][0]=1 (1->0)
  dp[101][2]=1 (0->2), dp[101][0]=1 (2->0)
  dp[110][2]=1 (1->2), dp[110][1]=1 (2->1)
  dp[111][0]=2, dp[111][1]=2, dp[111][2]=2
Answer: 2+2+2 = 6
```

### Code
```python
def count_hamiltonian_paths(n, edges):
    adj = [[False] * n for _ in range(n)]
    for u, v in edges:
        adj[u][v] = adj[v][u] = True
    dp = [[0] * n for _ in range(1 << n)]
    for i in range(n):
        dp[1 << i][i] = 1
    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)) or dp[mask][last] == 0:
                continue
            for nxt in range(n):
                if (mask & (1 << nxt)) or not adj[last][nxt]:
                    continue
                dp[mask | (1 << nxt)][nxt] += dp[mask][last]
    return sum(dp[(1 << n) - 1])
# Time: O(2^n * n^2), Space: O(2^n * n)
```

### Complexity
- Time: O(2^n * n^2), Space: O(2^n * n).

### Common Mistakes & Edge Cases
- Seed ALL single-vertex states, not just vertex 0.
- Undirected: set both `adj[u][v]` and `adj[v][u]`.
- `n=1`: count is `1`.

---

## 4. Scheduling with Deadlines (Bitmask) — Hard

### Problem Explanation
Given `n` jobs with deadlines `d[i]` and profits `p[i]`, schedule jobs on
a single machine (each takes 1 unit of time) to maximize total profit.
A job must be completed by its deadline. Use bitmask DP over time slots.

### State Definition
`dp[mask]` = maximum profit when the set of occupied time slots is `mask`.
Bit `t` set means slot `t` is taken. Worker index = popcount(mask).

### Recurrence Relation
```
For each mask, job_idx = popcount(mask):
  d, p = jobs[job_idx]
  For t in range(min(d, max_time)-1, -1, -1):
    if slot t is free:
      dp[mask | (1 << t)] = max(dp[mask | (1 << t)], dp[mask] + p)
```

### Base Cases
- `dp[0] = 0`. Answer = `max(dp)`.

### Intuition (Why This Works)
Sort jobs by profit descending (greedy ordering). The bitmask tracks
which time slots are occupied. For each job, try the latest available
slot before its deadline to maximize flexibility for later jobs.

### Step-by-Step Procedure
1. Sort jobs by profit descending.
2. `dp = [0] * (1 << max_deadline)`.
3. For each mask, compute job_idx, try scheduling at each free slot.
4. Return `max(dp)`.

### Worked Example (Dry Run)
```
Jobs: deadlines=[2,1,2,1], profits=[50,10,20,30]
Sorted by profit: [(2,50),(1,30),(2,20),(1,10)]

  dp[000]=0
  mask=000 (job 0, d=2): try t=1 -> dp[001]=50; try t=0 -> dp[010]=50
  mask=001 (job 1, d=1): t=0 free -> dp[011]=50+30=80
  mask=010 (job 1, d=1): t=0 free -> dp[011]=max(80,50+30)=80
  (other branches explored but don't improve)

Answer: max(dp) = 80
```

### Code
```python
def schedule_deadlines(deadlines, profits):
    n = len(profits)
    jobs = sorted(zip(deadlines, profits), key=lambda x: -x[1])
    max_time = max(deadlines)
    dp = [0] * (1 << max_time)
    for mask in range(1 << max_time):
        idx = bin(mask).count('1')
        if idx >= n:
            continue
        d, p = jobs[idx]
        for t in range(min(d, max_time) - 1, -1, -1):
            if not (mask & (1 << t)):
                nm = mask | (1 << t)
                dp[nm] = max(dp[nm], dp[mask] + p)
    return max(dp)
# Time: O(n * 2^T), Space: O(2^T) where T = max deadline
```

### Complexity
- Time: O(n * 2^T), Space: O(2^T).

### Common Mistakes & Edge Cases
- Clamp deadline to `n` if `d[i] > n`.
- Multiple jobs competing for the same slot: DP tries all possibilities.
- `n = 0`: return `0`.

---

## 5. Minimum Cost to Hire Workers (Bitmask) — Hard

### Problem Explanation
Given `n` workers and `n` tasks, `cost[i][j]` = cost for worker `i` to
do task `j`. Each worker does exactly one task, each task needs one worker.
Find the minimum cost assignment using bitmask DP.

### State Definition
`dp[mask]` = minimum cost when the set of assigned tasks is `mask`. Worker
index = `popcount(mask)`.

### Recurrence Relation
```
worker = popcount(mask)
dp[mask | (1 << task)] = min(dp[mask | (1 << task)],
                              dp[mask] + cost[worker][task])
```
for each unassigned task.

### Base Cases
- `dp[0] = 0`. Answer = `dp[(1<<n)-1]`.

### Intuition (Why This Works)
Process workers 0,1,...,n-1 in order. The bitmask tracks which tasks are
taken. popcount gives which worker we are assigning. O(n * 2^n) is feasible
for n <= 20.

### Step-by-Step Procedure
1. `dp = [inf] * (1<<n)`, `dp[0] = 0`.
2. For each mask: worker = popcount(mask).
3. For each unassigned task: update `dp[mask | 1<<task]`.
4. Return `dp[(1<<n)-1]`.

### Worked Example (Dry Run)
```
n=3, cost = [[2,7,5],[3,1,9],[8,4,6]]

  dp[000]=0
  worker 0: dp[001]=2, dp[010]=7, dp[100]=5
  worker 1: dp[011]=2+1=3, dp[101]=2+9=11, dp[110]=7+9=16
             dp[011]=min(3,7+3)=3, dp[101]=min(11,5+3)=8, dp[110]=min(16,5+1)=6
  worker 2: dp[111]=3+6=9, min(9,8+4)=9, min(9,6+8)=9

Answer: dp[111] = 9
```

### Code
```python
def min_cost_workers(cost):
    n = len(cost)
    inf = float('inf')
    dp = [inf] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        w = bin(mask).count('1')
        if w >= n:
            continue
        for t in range(n):
            if mask & (1 << t):
                continue
            nm = mask | (1 << t)
            dp[nm] = min(dp[nm], dp[mask] + cost[w][t])
    return dp[(1 << n) - 1]
# Time: O(n * 2^n), Space: O(2^n)
```

### Complexity
- Time: O(n * 2^n), Space: O(2^n).

### Common Mistakes & Edge Cases
- Worker index = popcount(mask), not a separate loop variable.
- `n=0`: return `0`.
- Infeasible: `dp[full]` stays `inf`.

---

## 6. Partition to K Equal Sum Subsets (LC #698) — Hard

### Problem Explanation
Given `nums` and integer `k`, partition `nums` into `k` subsets of equal
sum. Return `True` if possible. Each element goes into exactly one subset.

### State Definition
`dp[mask]` = the running sum of the current subset being filled, modulo
target. `mask` tracks which elements are used.

### Recurrence Relation
```
For each mask, for each unused element i:
  new_sum = dp[mask] + nums[i]
  if new_sum <= target:
    dp[mask | (1<<i)] = 0 if new_sum == target else new_sum
```

### Base Cases
- `dp[0] = 0`. Answer: `dp[(1<<n)-1] == 0` (all subsets filled exactly).

### Intuition (Why This Works)
Fill subsets one at a time. When the running sum hits `target`, reset to
0 (start next subset). The bitmask ensures each element is used exactly
once. If the full mask is reached with sum 0, all k subsets are balanced.

### Step-by-Step Procedure
1. If `sum(nums) % k != 0`, return `False`.
2. `target = sum(nums) // k`.
3. `dp = [-1] * (1<<n)`, `dp[0] = 0`.
4. For each mask with `dp[mask] >= 0`: try adding each unused element.
5. Return `dp[(1<<n)-1] == 0`.

### Worked Example (Dry Run)
```
nums = [4,3,2,3,5,2,1], k=4, target = 20/4 = 5

  dp[0000000]=0
  mask=0000000: try elem 0 (val=4) -> dp[0000001]=4
  mask=0000001 (sum=4): try elem 1 (val=3) -> 4+3=7>5 skip
             try elem 2 (val=2) -> 4+2=6>5 skip
             try elem 6 (val=1) -> 4+1=5 -> dp[1000001]=0 (subset full!)
  ... continues filling subsets ...

After exploration: dp[1111111] = 0 -> True
```

### Code
```python
class Solution:
    def canPartitionKSubsets(self, nums: list, k: int) -> bool:
        total = sum(nums)
        if total % k != 0:
            return False
        target = total // k
        n = len(nums)
        dp = [-1] * (1 << n)
        dp[0] = 0
        for mask in range(1 << n):
            if dp[mask] < 0:
                continue
            for i in range(n):
                if mask & (1 << i):
                    continue
                s = dp[mask] + nums[i]
                if s <= target:
                    nm = mask | (1 << i)
                    dp[nm] = 0 if s == target else s
        return dp[(1 << n) - 1] == 0
# Time: O(n * 2^n), Space: O(2^n)
```

### Complexity
- Time: O(n * 2^n), Space: O(2^n).

### Common Mistakes & Edge Cases
- `sum(nums) % k != 0`: impossible → return `False`.
- Any element > target: impossible → return `False`.
- `dp[mask] == -1`: unreachable state, skip.

---

## 7. Number of Ways to Wear Different Hats (LC #1434) — Hard

### Problem Explanation
There are `n` people and `m` hats (numbered 1..m). Each person likes
some subset of hats. Count the number of ways to assign each person a
hat such that no two people wear the same hat. Return modulo 10^9+7.

### State Definition
`dp[mask]` = number of ways to assign hats for the set of people
represented by `mask`. For each hat, try assigning it to each person
who likes it and hasn't received a hat yet.

### Recurrence Relation
```
For each hat h from 1 to m:
  For each mask:
    For each person p who likes hat h and is not in mask:
      dp[mask | (1<<p)] += dp[mask]
```

### Base Cases
- `dp[0] = 1` (no people assigned, one way: do nothing).
- Answer = `dp[(1<<n)-1]`.

### Intuition (Why This Works)
Process hats one at a time. For each hat, we either assign it to one
of the people who like it (and who hasn't gotten a hat yet), or skip it.
The bitmask tracks which people are already assigned.

### Step-by-Step Procedure
1. Build `hats[h]` = bitmask of people who like hat `h`.
2. `dp = [0] * (1<<n)`, `dp[0] = 1`.
3. For each hat `h` from 1 to 12 (or m):
   For each mask (reverse order to avoid double-counting):
     For each person in `hats[h]` not in mask: update.
4. Return `dp[(1<<n)-1] % MOD`.

### Worked Example (Dry Run)
```
n=3 people, m=3 hats.
Person 0 likes hats {1,2}, Person 1 likes {2,3}, Person 2 likes {1,3}

  hats: {1: {0,2}, 2: {0,1}, 3: {1,2}}
  dp[000]=1
  Hat 1: from 000: assign to 0->dp[001]=1, assign to 2->dp[100]=1
  Hat 2: from 000: assign to 0->dp[001]+=1(=2), assign to 1->dp[010]=1
         from 001: assign to 1->dp[011]=1
         from 100: assign to 0->dp[101]=1, assign to 1->dp[110]=1
  Hat 3: from 000: assign to 1->dp[010]+=1(=2), assign to 2->dp[100]+=1(=2)
         from 001: assign to 1->dp[011]+=1(=2), assign to 2->dp[101]+=1(=2)
         from 010: assign to 2->dp[110]+=1(=2)
         from 011: assign to 2->dp[111]+=1
         from 100: assign to 1->dp[110]+=1(=3)
         from 101: assign to 1->dp[111]+=1(=2)
         from 110: assign to 0->dp[111]+=1(=3)

Answer: dp[111] = 3
```

### Code
```python
class Solution:
    def numberWays(self, hats: list) -> int:
        MOD = 10**9 + 7
        n = len(hats)
        # Build hat -> people bitmask
        hat_to_people = [0] * 13  # hats numbered 1..12
        for person, hat_list in enumerate(hats):
            for h in hat_list:
                hat_to_people[h] |= (1 << person)
        dp = [0] * (1 << n)
        dp[0] = 1
        for h in range(1, 13):
            for mask in range((1 << n) - 1, -1, -1):
                people_who_like = hat_to_people[h]
                # Try assigning hat h to each eligible person
                available = people_who_like & ~mask
                p = available
                while p:
                    bit = p & (-p)
                    dp[mask | bit] = (dp[mask | bit] + dp[mask]) % MOD
                    p -= bit
        return dp[(1 << n) - 1]
# Time: O(m * 2^n), Space: O(2^n) where m = number of hat types
```

### Complexity
- Time: O(m * 2^n), Space: O(2^n).

### Common Mistakes & Edge Cases
- Iterate masks in reverse when processing each hat to avoid double-counting.
- Multiple hats of the same type: handled by processing each hat independently.
- Person likes no hats: they can never be assigned → answer is `0`.

---

## 8. Minimum Number of Visited Cells in a Matrix (LC #2617) — Hard

### Problem Explanation
Given an `m x n` matrix where `mat[i][j]` is the maximum number of cells
you can jump right (same row) or down (same column) from cell `(i,j)`,
find the minimum number of cells visited to reach `(m-1, n-1)` from `(0,0)`.

### State Definition
`dp[r][c]` = minimum cells visited to reach `(r,c)`. For each cell, try
all valid jumps right and down, updating the destination.

### Recurrence Relation
```
For cell (r,c) with value v:
  For j in range(c+1, min(c+v+1, n)):
    dp[r][j] = min(dp[r][j], dp[r][c] + 1)
  For i in range(r+1, min(r+v+1, m)):
    dp[i][c] = min(dp[i][c], dp[r][c] + 1)
```

### Base Cases
- `dp[0][0] = 1`. All others `inf`.

### Intuition (Why This Works)
BFS/Dijkstra exploring cells in order of distance. Each cell `(r,c)` with
value `v` can jump up to `v` cells right or down. We update all reachable
cells and track the minimum visits.

### Step-by-Step Procedure
1. `dp[0][0] = 1`, rest `inf`.
2. Process cells in order (row by row, column by column).
3. For each cell, try all right and down jumps.
4. Return `dp[m-1][n-1]`.

### Worked Example (Dry Run)
```
Matrix:
  3  2  1
  1  4  1
  5  1  1

  dp[0][0]=1
  (0,0) val=3: right to (0,1)=2, (0,2)=2; down to (1,0)=2, (2,0)=2
  (0,1) val=2: right to (0,2)=min(2,3)=2; down to (1,1)=3, (2,1)=3
  (0,2) val=1: down to (1,2)=3
  (1,0) val=1: right to (1,1)=min(3,3)=3; down to (2,0)=min(2,3)=2
  (2,0) val=5: right to (2,1)=min(3,3)=3, (2,2)=4
  (1,1) val=4: right to (1,2)=min(3,4)=3; down to (2,1)=min(3,4)=3
  (1,2) val=1: down to (2,2)=min(4,4)=4
  (2,1) val=1: right to (2,2)=min(4,4)=4

Answer: dp[2][2] = 4
```

### Code
```python
class Solution:
    def minimumVisitedCells(self, grid: list) -> int:
        m, n = len(grid), len(grid[0])
        inf = float('inf')
        dp = [[inf] * n for _ in range(m)]
        dp[0][0] = 1
        for r in range(m):
            for c in range(n):
                if dp[r][c] == inf:
                    continue
                v = grid[r][c]
                # Jump right
                for j in range(c + 1, min(c + v + 1, n)):
                    dp[r][j] = min(dp[r][j], dp[r][c] + 1)
                # Jump down
                for i in range(r + 1, min(r + v + 1, m)):
                    dp[i][c] = min(dp[i][c], dp[r][c] + 1)
        return dp[m-1][n-1] if dp[m-1][n-1] < inf else -1
# Time: O(m * n * max(m,n)), Space: O(m * n)
```

### Complexity
- Time: O(m * n * max(m,n)), Space: O(m * n).

### Common Mistakes & Edge Cases
- `grid[0][0] = 0` and m,n > 1: unreachable → return `-1`.
- Single cell: return `1`.
- Large jump values: clamp to matrix bounds.

---

## 9. Maximum Score from Performing Multiplication Operations (LC #1770) — Hard

### Problem Explanation
Given arrays `nums` (length n) and `multipliers` (length m, m <= n),
perform `m` operations. At operation `i`, choose either the first or last
element of `nums`, multiply by `multipliers[i]`, add to score, and remove
the chosen element. Maximize the total score.

### State Definition
`dp[l][r]` = maximum score achievable from the subarray `nums[l..r]`
after performing some number of operations. Equivalently, `dp[i][l]` =
max score after `i` operations with `l` elements taken from the left.

### Recurrence Relation
```
dp[i][l] = max(
    dp[i+1][l] + multipliers[i] * nums[l],           # take from left
    dp[i+1][l] + multipliers[i] * nums[n-1-(i-l)]    # take from right
)
```
Or using two indices: `dp[l][r] = max(nums[l]*mult + dp[l+1][r], nums[r]*mult + dp[l][r-1])`.

### Base Cases
- `dp[l][r] = 0` when `l > r` (no elements left).
- `dp[l][l] = max(nums[l], nums[r]) * multipliers[0]` for single operation.

### Intuition (Why This Works)
At each step we choose left or right. The subarray `[l..r]` fully
captures the remaining state. Processing operations in order (0 to m-1)
and using the subarray bounds gives a clean O(m^2) DP.

### Step-by-Step Procedure
1. Use `dp[i][l]` where `i` = operation index, `l` = left pointer.
2. `r = n - 1 - (i - l)` (right pointer derived from l and i).
3. `dp[i][l] = max(nums[l]*multipliers[i] + dp[i+1][l], nums[r]*multipliers[i] + dp[i+1][l+1])`.
4. Base: `dp[m][l] = 0` for all valid `l`.
5. Answer = `dp[0][0]`.

### Worked Example (Dry Run)
```
nums = [1,2,3], multipliers = [3,2]
n=3, m=2. dp[i][l] = max score from operation i with l left-taken.

  dp[2][*] = 0 (no operations left)
  Operation 1 (i=1, mult=2):
    l=0: r=3-1-(1-0)=1, take left: 2*2+0=4, take right: 3*2+0=6 -> dp[1][0]=6
    l=1: r=3-1-(1-1)=1, take left: 2*2+0=4 -> dp[1][1]=4
  Operation 0 (i=0, mult=3):
    l=0: r=2, take left: 1*3+dp[1][0]=3+6=9, take right: 3*3+dp[1][1]=9+4=13
    dp[0][0] = 13

Answer: 13 (take right 3, then right 2 -> 3*3 + 2*2 = 13)
```

### Code
```python
class Solution:
    def maximumScore(self, nums: list, multipliers: list) -> int:
        n, m = len(nums), len(multipliers)
        # dp[i][l] = max score from operation i, having taken l from left
        dp = [[0] * (m + 1) for _ in range(m + 1)]
        for i in range(m - 1, -1, -1):
            for l in range(i + 1):
                r = n - 1 - (i - l)
                dp[i][l] = max(
                    multipliers[i] * nums[l] + dp[i + 1][l],
                    multipliers[i] * nums[r] + dp[i + 1][l + 1]
                )
        return dp[0][0]
# Time: O(m^2), Space: O(m^2)
```

### Complexity
- Time: O(m^2), Space: O(m^2).

### Common Mistakes & Edge Cases
- Right index calculation: `r = n - 1 - (i - l)`.
- `m == 0`: return `0`.
- All negative values in nums: still pick the max at each step.

---

## 10. Fair Candy Swap (LC #888) — Medium

### Problem Explanation
Alice and Bob have candy bars of different sizes. Alice has `aliceSizes`
and Bob has `bobSizes`. They want to exchange one candy each so that
after the exchange, they have the same total candy. Return `[a, b]` where
Alice gives candy of size `a` and receives candy of size `b`.

### State Definition
`bob_set` = set of Bob's candy sizes (for O(1) lookup). We iterate
Alice's candies and check if Bob has the matching complement.

### Recurrence Relation
```
total_a = sum(aliceSizes), total_b = sum(bobSizes)
diff = (total_a - total_b) // 2
For each a in aliceSizes:
  if (a - diff) in bob_set: return [a, a - diff]
```

### Base Cases
- `diff = (total_a - total_b) / 2` must be an integer.

### Intuition (Why This Works)
If Alice gives `a` and receives `b`, we need `total_a - a + b = total_b - b + a`,
so `b = a - diff` where `diff = (total_a - total_b) / 2`. For each of Alice's
candies, check if Bob has the required complement.

### Step-by-Step Procedure
1. Compute `diff = (sum(aliceSizes) - sum(bobSizes)) // 2`.
2. Build `bob_set` from `bobSizes`.
3. For each `a` in `aliceSizes`: if `a - diff` in `bob_set`, return `[a, a-diff]`.

### Worked Example (Dry Run)
```
aliceSizes = [1,1], bobSizes = [2,2]
total_a=2, total_b=4, diff=(2-4)//2=-1
bob_set = {2}
  a=1: 1-(-1)=2 in bob_set? Yes -> return [1, 2]

aliceSizes = [1,2], bobSizes = [2,3]
total_a=3, total_b=5, diff=-1
bob_set = {2,3}
  a=1: 1-(-1)=2 in bob_set? Yes -> return [1, 2]
```

### Code
```python
class Solution:
    def fairCandySwap(self, aliceSizes: list, bobSizes: list) -> list:
        diff = (sum(aliceSizes) - sum(bobSizes)) // 2
        bob_set = set(bobSizes)
        for a in aliceSizes:
            b = a - diff
            if b in bob_set:
                return [a, b]
        return []
# Time: O(n + m), Space: O(m)
```

### Complexity
- Time: O(n + m), Space: O(m) for the set.

### Common Mistakes & Edge Cases
- `(total_a - total_b)` must be even for an integer solution.
- If no valid pair exists, return `[]`.
- Duplicates in candy sizes: set handles them correctly.

---

## 11. Maximum AND of Two Subsets — Medium

### Problem Explanation
Given an array `nums` and integer `k`, choose `k` elements to form a
subset. Maximize the AND of all elements in the subset. Return the maximum
possible AND value.

### State Definition
Check each bit from high to low. For each candidate bit pattern, verify
if at least `k` elements have all those bits set.

### Recurrence Relation
```
For bit from 30 down to 0:
  candidate = answer | (1 << bit)
  count = number of elements where (num & candidate) == candidate
  if count >= k: answer = candidate
```

### Base Cases
- `answer = 0` initially.
- If fewer than `k` elements exist, the answer is the AND of all.

### Intuition (Why This Works)
Greedy bit-by-bit from MSB to LSB. For each bit, we check if setting it
(and keeping all previously set bits) is feasible (at least k elements
have all those bits). This is a classic "bit greedy + feasibility check".

### Step-by-Step Procedure
1. `answer = 0`.
2. For bit from 30 down to 0:
   candidate = answer | (1 << bit).
   Count elements `x` where `(x & candidate) == candidate`.
   If count >= k: set that bit in answer.
3. Return answer.

### Worked Example (Dry Run)
```
nums = [4, 8, 12, 16], k = 2

Binary: 100, 1000, 1100, 10000

  bit=4 (16): candidate=16, elements with all bits of 16: {16} count=1 < 2
  bit=3 (8):  candidate=8,  elements: {8,12} count=2 >= 2 -> answer=8
  bit=2 (4):  candidate=12, elements: {12} count=1 < 2
  bit=1 (2):  candidate=10, elements: {12} count=1 < 2
  bit=0 (1):  candidate=9,  elements: {} count=0 < 2

Answer: 8 (subset {8, 12} has AND = 8)
```

### Code
```python
class Solution:
    def maximumAND(self, nums: list, k: int) -> int:
        answer = 0
        for bit in range(30, -1, -1):
            candidate = answer | (1 << bit)
            count = sum(1 for x in nums if (x & candidate) == candidate)
            if count >= k:
                answer = candidate
        return answer
# Time: O(31 * n), Space: O(1)
```

### Complexity
- Time: O(31 * n), Space: O(1).

### Common Mistakes & Edge Cases
- `k > n`: impossible, but input guarantees `k <= n`.
- `k = 1`: answer is `max(nums)`.
- `k = n`: answer is AND of all elements.
- All elements identical: answer is that element.
