# Greedy Algorithms Introduction

**Greedy**: Make the locally optimal choice at each step, hoping it leads to a globally optimal solution.

---

## What Is Greedy?

A greedy algorithm builds a solution piece by piece, always choosing the next piece that offers the most immediate benefit. Unlike dynamic programming, it never reconsiders a choice — once a decision is made, it's final.

```
Greedy Mindset:
1. Break problem into a sequence of decisions
2. At each step, pick the best option available RIGHT NOW
3. Never look back, never reconsider
4. Hope that local optimums → global optimum
```

**Key Insight**: Greedy works when making the locally optimal choice at each step guarantees a globally optimal solution. This is NOT always true — you must prove it or verify it before applying greedy.

---

## When Greedy Works

### Property 1: Greedy Choice Property

A global optimum can be arrived at by making a locally optimal choice. In other words, making the greedy choice never prevents us from finding the optimal solution.

```
Example: Activity Selection
Activities: [(1,4), (3,5), (0,6), (5,7), (3,9), (5,9), (6,10), (8,11), (8,12), (2,14), (12,16)]

Greedy choice: Always pick the activity with earliest finish time
1. Pick (1,4) — finishes earliest
2. Pick (5,7) — next compatible with earliest finish
3. Pick (8,11) — next compatible
4. Pick (12,16) — next compatible

Result: 4 activities (optimal)
Proof: Any optimal solution can be transformed to include (1,4) without reducing count
```

### Property 2: Optimal Substructure

An optimal solution to the problem contains optimal solutions to subproblems.

```
Example: Fractional Knapsack
- Pick highest value/weight ratio item first
- Fill remaining capacity with next best item
- Each subproblem (what to put in remaining capacity) is solved optimally

The overall optimal solution = greedy choice + optimal solution of remaining subproblem
```

---

## Proof Techniques

### Technique 1: Exchange Argument

Show that any optimal solution can be transformed into the greedy solution without making it worse.

```
Steps:
1. Assume an optimal solution O that differs from greedy solution G
2. Find the first point where O and G differ
3. Show that swapping O's choice with G's choice doesn't worsen O
4. Repeat until O = G
5. Therefore G is also optimal

Example proof (Activity Selection):
- Let G = greedy solution (earliest finish time)
- Let O = any optimal solution
- If O picks activity a1 first and G picks activity g1 first
- Since g1 finishes no later than a1, we can replace a1 with g1
- All activities compatible with a1 are also compatible with g1
- So O' = (O - {a1}) ∪ {g1} is also optimal
- Repeat: O' now agrees with G on first choice
- Eventually O becomes G, proving G is optimal
```

### Technique 2: Greedy Stays Ahead

Show that at each step, the greedy solution is at least as good as any other solution.

```
Steps:
1. Define a measure of progress (e.g., number of activities selected)
2. Show that after k steps, greedy is at least as good as any algorithm
3. By induction, greedy is optimal

Example proof (Activity Selection):
- After selecting k activities, greedy has selected k activities
- Each selection finishes as early or earlier than any other choice
- Therefore greedy always has maximum remaining capacity
- Greedy can always select at least as many activities as any other approach
```

---

## Matroid Theory (Brief)

Greedy algorithms work on matroid structures. A matroid is a mathematical structure where greedy is guaranteed to find the optimum.

```
Matroid = (S, I) where:
- S = finite set (elements)
- I = family of subsets of S (independent sets) satisfying:
  1. ∅ ∈ I (empty set is independent)
  2. If A ∈ I and B ⊆ A, then B ∈ I (hereditary property)
  3. If A, B ∈ I and |A| < |B|, then ∃ x ∈ B\A such that A ∪ {x} ∈ I (exchange property)

Examples of matroids:
- Graphic matroid: independent sets = forests (acyclic subgraphs)
- Used in MST algorithms (Kruskal's, Prim's)

Examples of non-matroids:
- Traveling Salesman Problem (greedy nearest-neighbor fails)
- 0/1 Knapsack (greedy by value/weight fails)
```

---

## Greedy vs DP Decision Framework

```
Ask yourself these questions:

1. Can I make a single optimal choice without revisiting?
   ├── YES → Candidate for Greedy
   └── NO  → DP or Backtracking

2. Do subproblems overlap? (same subproblem solved multiple times)
   ├── YES → DP (memoization avoids recomputation)
   └── NO  → Greedy or Divide & Conquer

3. Do I need to explore all possible combinations?
   ├── YES → Backtracking or DP
   └── NO  → Greedy

4. Is the problem about selecting a subset with constraints?
   ├── Knapsack 0/1 → DP
   ├── Knapsack Fractional → Greedy
   └── Activity Selection → Greedy

5. Can I prove greedy choice property?
   ├── YES → Greedy
   └── NO  → DP
```

### Decision Matrix

| Problem Type | Greedy? | DP? | Example |
|---|---|---|---|
| Select items with constraints | Maybe | Usually | Knapsack |
| Find shortest path | Yes (Dijkstra) | Yes (Bellman-Ford) | Shortest Path |
| Find minimum spanning tree | Yes (Kruskal) | No | MST |
| Sequence alignment | No | Yes | Edit Distance |
| Optimal ordering | Maybe | Usually | Job Scheduling |
| Partition problems | Sometimes | Usually | Partition Equal Subset |
| Coin change (canonical) | Yes | Yes | Min coins (standard denominations) |
| Coin change (general) | No | Yes | Min coins (arbitrary denominations) |

---

## Common Mistakes: Applying Greedy When DP Is Needed

### Mistake 1: 0/1 Knapsack

```java
// WRONG: Greedy by value/weight ratio
// Items: (weight=1, value=6), (weight=2, value=10), (weight=3, value=12)
// Capacity: 5
// Greedy picks: item1 (6/1=6), item2 (10/2=5), total=16
// Optimal: item2 + item3 = 10 + 12 = 22

// CORRECT: DP approach
public int knapsack(int[] weights, int[] values, int capacity) {
    int n = weights.length;
    int[][] dp = new int[n + 1][capacity + 1];
    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= capacity; w++) {
            dp[i][w] = dp[i - 1][w];  // don't take item i
            if (weights[i - 1] <= w) {
                dp[i][w] = Math.max(dp[i][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]);
            }
        }
    }
    return dp[n][capacity];
}
```

### Mistake 2: Coin Change (General Denominations)

```java
// WRONG: Greedy (pick largest coin first)
// Coins: [1, 3, 4], target: 6
// Greedy: 4 + 1 + 1 = 3 coins
// Optimal: 3 + 3 = 2 coins

// CORRECT: DP approach
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;
    for (int i = 1; i <= amount; i++) {
        for (int coin : coins) {
            if (coin <= i) {
                dp[i] = Math.min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```

### Mistake 3: Longest Increasing Subsequence

```java
// WRONG: Greedy (always pick next larger element)
// Array: [10, 9, 2, 5, 3, 7, 101, 18]
// Greedy: [10, 101] = length 2
// Optimal: [2, 3, 7, 101] or [2, 5, 7, 101] = length 4

// CORRECT: DP approach O(n²)
public int lengthOfLIS(int[] nums) {
    int n = nums.length;
    int[] dp = new int[n];
    Arrays.fill(dp, 1);
    int maxLen = 1;
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i]) {
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
        maxLen = Math.max(maxLen, dp[i]);
    }
    return maxLen;
}
```

---

## Examples Where Greedy Works

### 1. Activity Selection (Job Scheduling)

```java
// Sort by finish time, greedily select compatible activities
public int eraseOverlapIntervals(int[][] intervals) {
    if (intervals.length == 0) return 0;
    Arrays.sort(intervals, (a, b) -> a[1] - b[1]);  // sort by end time
    int end = intervals[0][1];
    int count = 1;  // number of non-overlapping intervals
    for (int i = 1; i < intervals.length; i++) {
        if (intervals[i][0] >= end) {  // no overlap
            count++;
            end = intervals[i][1];
        }
    }
    return intervals.length - count;  // intervals to remove
}
```

### 2. Fractional Knapsack

```java
// Sort by value/weight ratio, greedily take best ratio
public double fractionalKnapsack(int[] weights, int[] values, int capacity) {
    int n = weights.length;
    double[][] items = new double[n][2];  // [value/weight ratio, index]
    for (int i = 0; i < n; i++) {
        items[i][0] = (double) values[i] / weights[i];
        items[i][1] = i;
    }
    Arrays.sort(items, (a, b) -> Double.compare(b[0], a[0]));  // descending ratio

    double totalValue = 0;
    for (int i = 0; i < n && capacity > 0; i++) {
        int idx = (int) items[i][1];
        if (weights[idx] <= capacity) {
            totalValue += values[idx];
            capacity -= weights[idx];
        } else {
            totalValue += items[i][0] * capacity;  // take fraction
            break;
        }
    }
    return totalValue;
}
```

### 3. Huffman Coding

```java
// Merge two smallest frequencies until one tree remains
public TreeNode buildHuffmanTree(int[] frequencies) {
    PriorityQueue<TreeNode> pq = new PriorityQueue<>((a, b) -> a.freq - b.freq);
    for (int f : frequencies) {
        pq.add(new TreeNode(f));
    }
    while (pq.size() > 1) {
        TreeNode left = pq.poll();
        TreeNode right = pq.poll();
        TreeNode parent = new TreeNode(left.freq + right.freq);
        parent.left = left;
        parent.right = right;
        pq.add(parent);
    }
    return pq.poll();
}
```

### 4. Minimum Spanning Tree (Kruskal's)

```java
// Sort edges by weight, greedily add if no cycle
public int kruskal(int n, int[][] edges) {
    Arrays.sort(edges, (a, b) -> a[2] - b[2]);  // sort by weight
    int[] parent = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;
    int mstWeight = 0, edgesUsed = 0;
    for (int[] edge : edges) {
        int rootA = find(parent, edge[0]);
        int rootB = find(parent, edge[1]);
        if (rootA != rootB) {
            mstWeight += edge[2];
            parent[rootA] = rootB;
            edgesUsed++;
            if (edgesUsed == n - 1) break;
        }
    }
    return mstWeight;
}

private int find(int[] parent, int x) {
    if (parent[x] != x) parent[x] = find(parent, parent[x]);
    return parent[x];
}
```

### 5. Dijkstra's Shortest Path

```java
// Greedily visit closest unvisited node
public int[] dijkstra(List<List<int[]>> graph, int start) {
    int n = graph.size();
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[start] = 0;
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    pq.add(new int[]{start, 0});
    while (!pq.isEmpty()) {
        int[] curr = pq.poll();
        int node = curr[0], d = curr[1];
        if (d > dist[node]) continue;  // stale entry
        for (int[] edge : graph.get(node)) {
            int next = edge[0], weight = edge[1];
            if (dist[node] + weight < dist[next]) {
                dist[next] = dist[node] + weight;
                pq.add(new int[]{next, dist[next]});
            }
        }
    }
    return dist;
}
```

---

## 15 Decision Scenarios: Greedy or DP?

### Practice Problems

```
1. Maximum sum of non-adjacent elements
   → DP (taking or skipping each element changes future choices)

2. Minimum number of coins to make change (standard: 1,5,10,25)
   → Greedy (canonical coin system)

3. Minimum number of coins to make change (arbitrary denominations)
   → DP (greedy fails for [1,3,4], target=6)

4. Activity Selection (maximum number of non-overlapping activities)
   → Greedy (sort by finish time)

5. 0/1 Knapsack
   → DP (must consider all combinations)

6. Fractional Knapsack
   → Greedy (take by value/weight ratio)

7. Huffman Coding
   → Greedy (merge smallest frequencies)

8. Job Scheduling with deadlines and profits
   → Greedy (sort by profit, use Union-Find for slot allocation)

9. Longest Increasing Subsequence
   → DP (greedy picks don't guarantee longest)

10. Minimum Spanning Tree
    → Greedy (Kruskal's or Prim's)

11. Shortest path in unweighted graph
    → Greedy (BFS)

12. Shortest path in weighted graph (no negative weights)
    → Greedy (Dijkstra's)

13. Shortest path in weighted graph (negative weights)
    → DP (Bellman-Ford, not greedy)

14. Coin change — minimum coins for exact amount
    → DP (greedy fails in general)

15. Maximum product subarray
    → DP (track both max and min due to negatives)
```

### Quick Decision Flowchart

```
START
  │
  ├── Is there a clear "best" choice at each step?
  │     ├── YES → Can you prove it's always optimal?
  │     │           ├── YES → GREEDY ✓
  │     │           └── NO  → Try DP or test with counterexample
  │     └── NO  → DP or Backtracking
  │
  ├── Do subproblems overlap?
  │     ├── YES → DP (use memoization/tabulation)
  │     └── NO  → Divide & Conquer or Greedy
  │
  └── Is it a selection/partition problem?
        ├── With capacity constraint → DP (Knapsack-like)
        ├── Without constraint → Greedy (sort and select)
        └── With ordering constraint → DP
```

---

## Greedy Algorithm Template

```java
// General greedy template
public Result greedySolve(Input input) {
    // Step 1: Sort or organize data by greedy criterion
    Arrays.sort(data, greedyComparator);

    // Step 2: Initialize result
    Result result = new Result();

    // Step 3: Greedily select elements
    for (Element e : data) {
        if (canAdd(e, result)) {  // check constraint
            result.add(e);
        }
    }

    // Step 4: Return result
    return result;
}

// Example: Maximum number of activities
public int maxActivities(int[][] intervals) {
    // Step 1: Sort by finish time
    Arrays.sort(intervals, (a, b) -> a[1] - b[1]);

    // Step 2: Initialize
    int count = 0;
    int lastEnd = Integer.MIN_VALUE;

    // Step 3: Greedily select
    for (int[] interval : intervals) {
        if (interval[0] >= lastEnd) {  // compatible
            count++;
            lastEnd = interval[1];
        }
    }

    // Step 4: Return
    return count;
}

// Example: Jump Game (can you reach the end?)
public boolean canJump(int[] nums) {
    int maxReach = 0;
    for (int i = 0; i < nums.length; i++) {
        if (i > maxReach) return false;  // can't reach this position
        maxReach = Math.max(maxReach, i + nums[i]);
    }
    return true;
}
```

---

## Summary: Greedy Checklist

```
Before applying greedy, verify:

□ Can I define a clear greedy criterion? (earliest finish, highest ratio, etc.)
□ Does the greedy choice property hold? (local optimum → global optimum)
□ Can I prove it with exchange argument or greedy-stays-ahead?
□ Is there a counterexample where greedy fails? (test with small cases)
□ Is the problem a known greedy problem? (MST, activity selection, Huffman)

If any answer is "no" or "unsure":
→ Consider DP, backtracking, or other approaches
→ Test your greedy solution on edge cases
→ If it fails, you need DP
```
