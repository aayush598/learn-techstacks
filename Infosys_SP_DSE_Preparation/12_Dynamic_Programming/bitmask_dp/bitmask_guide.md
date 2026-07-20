# Bitmask DP - Complete Guide

## What is Bitmask DP?

Bitmask DP uses an integer's bits to represent which elements are selected:
- mask = 0b0011 means elements 0 and 1 are picked
- dp[mask][i] = optimal value with visited set = mask, ending at node/task i

**n elements: 2^n states**

**Common bit operations:**
  mask | (1<<k)         -> pick/set k
  mask & (1<<k)         -> test if k is set
  mask & ~(1<<k)        -> clear/remove k
  mask ^ (1<<k)         -> toggle k
  (mask>>k) & 1         -> get bit k
  bin(mask).count('1')  -> popcount

**When to use:**
  n <= 20 (2^20 ~ 1 million states)
  elements have binary states
  dp[mask][last] when order matters

---

## Generic Bitmask DP Template

def bitmask_template(n, cost_fn):
    INF = 10**9
    dp = [[INF]*n for _ in range(1<<n)]
    for i in range(n):
        dp[1<<i][i] = 0
    for mask in range(1<<n):
        for last in range(n):
            if not (mask>>last & 1): continue
            if dp[mask][last] == INF: continue
            for nxt in range(n):
                if (mask>>nxt) & 1: continue
                cost = cost_fn(last, nxt)
                if cost == INF: continue
                nm = mask | (1<<nxt)
                dp[nm][nxt] = min(dp[nm][nxt], dp[mask][last] + cost)
    full = (1<<n)-1
    return min(dp[full])

This solves the shortest Hamiltonian path (no return). TSP adds return cost.

---

## Traveling Salesman Problem (TSP)

Find shortest tour visiting each city exactly once and returning to start.

def tsp_tab(cost):
    n = len(cost)
    INF = 10**9
    dp = [[INF]*n for _ in range(1<<n)]
    dp[1][0] = 0
    for mask in range(1<<n):
        for last in range(n):
            if not (mask>>last & 1): continue
            if dp[mask][last] == INF: continue
            for nxt in range(n):
                if (mask>>nxt) & 1: continue
                nm = mask | (1<<nxt)
                dp[nm][nxt] = min(dp[nm][nxt], dp[mask][last] + cost[last][nxt])
    full = (1<<n)-1
    ans = INF
    for i in range(1, n):
        if cost[i][0]:
            ans = min(ans, dp[full][i] + cost[i][0])
    return ans

def tsp_memo(cost):
    n = len(cost)
    memo = {}
    def dp(mask, pos):
        if mask == (1<<n)-1:
            return cost[pos][0]
        key = (mask, pos)
        if key in memo: return memo[key]
        best = INF
        for city in range(n):
            if mask & (1<<city): continue
            if cost[pos][city] == 0: continue
            best = min(best, cost[pos][city] + dp(mask | (1<<city), city))
        memo[key] = best
        return best
    return dp(1, 0)

---


## Assignment Problem

n workers, n tasks. cost[i][j] for worker i, task j. Minimize total cost. One-to-one.

def assignment_problem(cost):
    n = len(cost)
    dp = {0: 0}  # mask -> min cost
    for worker in range(n):
        new_dp = {}
        for mask, total in dp.items():
            for task in range(n):
                if not (mask & (1 << task)):
                    new_mask = mask | (1 << task)
                    new_cost = total + cost[worker][task]
                    if new_mask not in new_dp or new_cost < new_dp[new_mask]:
                        new_dp[new_mask] = new_cost
        dp = new_dp
    full = (1 << n) - 1
    return dp.get(full, -1)

# Time: O(n * 2^n), Space: O(2^n)

---

## Maximum Weight Independent Set (Graph)

Find max weight set of vertices with no edges between them. n <= 20.

def max_weight_independent_set(n, edges, weights):
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    memo = {}
    def solve(mask):
        if mask == 0: return 0
        if mask in memo: return memo[mask]
        v = (mask & -mask).bit_length() - 1
        bit = 1 << v
        exclude = solve(mask ^ bit)
        include = weights[v] + solve(mask & ~(bit | adj[v]))
        memo[mask] = max(include, exclude)
        return memo[mask]
    return solve((1 << n) - 1)

# Time: O(2^n), Space: O(2^n)

---

## Hamiltonian Path Count

def count_hamiltonian_paths(n, edges):
    adj = [[False]*n for _ in range(n)]
    for u, v in edges:
        adj[u][v] = adj[v][u] = True
    dp = [[0]*n for _ in range(1<<n)]
    for i in range(n):
        dp[1<<i][i] = 1
    for mask in range(1<<n):
        for last in range(n):
            if not (mask>>last & 1) or dp[mask][last] == 0: continue
            for nxt in range(n):
                if (mask>>nxt & 1) or not adj[last][nxt]: continue
                dp[mask | (1<<nxt)][nxt] += dp[mask][last]
    full = (1<<n)-1
    return sum(dp[full])

# Time: O(2^n * n^2), Space: O(2^n * n)

---

## Meet-in-the-Middle (n <= 40)

def meet_in_middle_knapsack(items, capacity):
    """
    items: list of (weight, value)
    Find max value with total weight <= capacity
    """
    n = len(items)
    def gen_subsets(start, end):
        res = []
        size = end - start
        for mask in range(1 << size):
            w = v = 0
            for j in range(size):
                if mask & (1 << j):
                    w += items[start + j][0]
                    v += items[start + j][1]
            if w <= capacity:
                res.append((w, v))
        return sorted(res)

    left = gen_subsets(0, n // 2)
    right = gen_subsets(n // 2, n)

    # Keep only Pareto-optimal right entries
    best_right = []
    max_v = -1
    for w, v in right:
        if v > max_v:
            best_right.append((w, v))
            max_v = v

    import bisect
    best = 0
    for w_l, v_l in left:
        remain = capacity - w_l
        idx = bisect.bisect_right(best_right, (remain, float("inf"))) - 1
        if idx >= 0:
            best = max(best, v_l + best_right[idx][1])
    return best

# Time: O(2^(n/2) * log(2^(n/2))), Space: O(2^(n/2))

---

