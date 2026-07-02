# Reduction Techniques

## Table of Contents
1. What is Reduction?
2. "Find Max with Constraints" → DP
3. "Can We Assign/Fit?" → Greedy or Backtracking
4. "Count Ways" → DP or Math
5. "Find if Exists" → Set, HashMap, Binary Search
6. "Find Optimal Path" → BFS, Dijkstra
7. "Relationship Between Pairs" → Graph
8. "Sorted + Search" → Binary Search
9. "Subarray/Substring" → Sliding Window or Prefix Sum
10. Quick Reference Table

---

## 1. What is Reduction?

**Reduction** is the process of transforming an unknown problem into a known problem that you already know how to solve.

**The key insight:** Most DSA problems are variations of a core set of ~20 patterns. When you encounter a new problem, ask: "What is this problem really asking?" and strip away the story/scenario to find the core algorithmic question.

```
"Word Ladder" = Shortest path in unweighted graph → BFS
"Alien Dictionary" = Topological sort from character ordering → Kahn's algorithm
"Russian Doll Envelopes" = Longest increasing subsequence in 2D → LIS with sorting
"Trapping Rain Water" = Pre-compute left/right maxes → Two pointers with running max
```

---

## 2. "Find Max with Constraints" → DP

**Core question:** What is the maximum/minimum/optimal value given certain constraints?

**Reduction path:**
```
"Is it optimal substructure?"
  → YES: Can I break into overlapping subproblems?
    → YES: DP
    → NO: Greedy or Divide & Conquer
  → NO: Brute force or Backtracking
```

### Examples

| Problem Statement | Reduced to | Pattern |
|-----------------|------------|---------|
| Max profit from stock trading with cooldown | DP with state (hold/sell/rest) | State machine DP |
| Max sum of non-adjacent elements | House robber | 1D DP with O(1) space |
| Max length of increasing subsequence | LIS | DP or patience sorting |
| Min cost to travel all cities | TSP | Bitmask DP |
| Max gold collected from grid | Grid DP | 2D DP |
| Min matrix multiplication cost | MCM | Interval DP |
| Longest common subsequence | LCS | 2-sequence DP |

### Recognition Checklist
```
[ ] Problem asks for max/min/longest/shortest
[ ] Decision at step n depends on step n-1
[ ] Same subproblem appears multiple times
[ ] Repeated calculations in brute force
```

### What DP not to use
```
[ ] Greedy works (Activity selection, coin greedy if denominations allow)
[ ] No overlapping subproblems (pure divide & conquer)
[ ] Constraint says n ≤ 20 (backtracking/bitmask better)
```

---

## 3. "Can We Assign/Fit?" → Greedy or Backtracking

**Core question:** Can we place items subject to constraints?

### Reduction: Greedy
When locally optimal choice leads to globally optimal solution.

**Key properties:**
- **Greedy choice property:** A global optimum can be reached by making locally optimal choices
- **Optimal substructure:** An optimal solution contains optimal solutions to subproblems

| Original Problem | Reduced to Greedy | Strategy |
|-----------------|-------------------|----------|
| Schedule max meetings in room | Activity selection | Sort by end time |
| Minimum coins for change (certain denominations) | Coin change (greedy) | Use largest coin first |
| Can you jump to the end? | Jump game | Track max reachable |
| Minimum refueling stops | Gas station | Max heap of stations |
| Partition labels | Greedy with last index | Extend partition as needed |

### Reduction: Backtracking
When you need to try all possibilities because greedy doesn't work.

| Original Problem | Reduced to Backtracking | Variation |
|-----------------|------------------------|-----------|
| Fill Sudoku board | Constraint satisfaction | Row/col/box validation |
| Place N queens | Constraint satisfaction | Check column/diagonal |
| Partition into k equal sum subsets | Backtracking with pruning | Try each element in each subset |
| Matchsticks to square | Backtracking with pruning | 4-way partition |

### Decision: Greedy vs Backtracking
```
Can we make decision once and never revisit?
├── YES → Greedy
├── NO → Do we need ALL solutions?
│   ├── YES → Backtracking (enumeration)
│   └── NO → Is there optimal substructure?
│       ├── YES → DP
│       └── NO → Backtracking with pruning
```

---

## 4. "Count Ways" → DP or Math

**Core question:** How many ways to achieve something?

### Reduction: DP (Counting DP)
When ways depend on previous ways.

| Original Problem | Reduced to | State Definition |
|-----------------|-----------|-----------------|
| Number of ways to make amount | Coin change II | dp[amount] = ways to make amount |
| Unique paths in grid | Grid DP | dp[i][j] = ways to reach (i,j) |
| Climbing stairs | Fibonacci DP | dp[n] = ways to reach step n |
| Number of LIS | Counting DP | dp[i] = count of LIS ending at i |
| Decode ways | String DP | dp[i] = ways to decode s[0..i] |
| Number of ways to stay in place | 2D DP | dp[steps][pos] = ways |

### Reduction: Combinatorics (Math)
When combinatorial formula works directly.

| Original Problem | Reduced to Math | Formula |
|-----------------|----------------|---------|
| Unique paths (m × n grid) | Combinations | C(m+n-2, m-1) |
| Count derangements | Recurrence | D(n) = (n-1)(D(n-1) + D(n-2)) |
| Catalan numbers | Various | C(n) = (2n)!/((n+1)!n!) |
| Count numbers with digit sum S | Digit DP (Math + DP) | DP on digits |

### Decision: DP vs Math
```
Is there a known closed-form formula?
├── YES → Math (compute directly, O(1))
├── NO → Does way[n] depend on way[n-1]?
│   ├── YES → DP
│   └── NO → Is there a combinatorial explanation?
│       ├── YES → Math
│       └── NO → DP + memoization
```

---

## 5. "Find if Exists" → Set, HashMap, Binary Search

**Core question:** Does a particular element, sum, or property exist?

### Reduction: Set/HashMap (O(1) lookup)

| Original Problem | Reduced to | Data Structure |
|-----------------|-----------|---------------|
| Two sum | HashMap of value → index | HashMap |
| Contains duplicate | HashSet | Set |
| Intersection of two arrays | HashSet intersection | Two Sets |
| First repeating character | HashSet or boolean[26] | Set/Array |
| Happy number cycle detection | HashSet of seen numbers | Set |
| Word break | Set of dictionary words | HashSet |

### Reduction: Binary Search (sorted data)

| Original Problem | Reduced to | Preprocessing |
|-----------------|-----------|---------------|
| Search in sorted matrix | Binary search on row/col | Already sorted |
| Find peak element | Binary search | Peak condition |
| First bad version | Lower bound | isBadVersion(mid) |
| Search for target in rotated array | Modified binary search | Detect sorted half |
| Find kth smallest in sorted matrix | Binary search on value | Count ≤ mid |

### Decision: Which data structure?
```
Is the data sorted?
├── YES → Binary search
└── NO → Is O(1) lookup needed?
    ├── YES → HashMap/HashSet
    └── NO → Can we sort first?
        ├── YES → Sort + Binary search
        └── NO → Linear scan with any DS
```

---

## 6. "Find Optimal Path" → BFS, Dijkstra

**Core question:** What is the shortest/cheapest/fastest path from A to B?

### Reduction: BFS (Unweighted Graph)

| Original Problem | Reduced to BFS | Node Definition |
|-----------------|---------------|-----------------|
| Word Ladder | BFS on word graph | Words are nodes, one-edit diff is edge |
| Shortest path in binary matrix | BFS on grid | Each cell is a node |
| Minimum steps to reach target | BFS state space | (position, state) as node |
| Snake and ladder | BFS on board | Board positions as nodes |
| Rotten oranges | Multi-source BFS | All rotten oranges = sources |

### Reduction: Dijkstra (Weighted, Non-negative)

| Original Problem | Reduced to Dijkstra | Edge Weight |
|-----------------|--------------------|-------------|
| Network delay time | Shortest path from source | Transmission time |
| Cheapest flights with max k stops | Modified Dijkstra or BFS+DP | Price |
| Min cost to connect points | Prim's (Dijkstra-like) | Manhattan distance |
| Path with minimum effort | Dijkstra on height diff | |adjacent diff|

### Reduction: Bellman-Ford (Negative weights allowed)

| Original Problem | Bellman-Ford? |
|-----------------|---------------|
| Find negative cycle | YES (cycle detection) |
| Cheapest flight with at most k stops | YES (k iterations) |
| Arbitrage detection | YES (log weights, detect cycle) |

### Decision: Which path algorithm?
```
Are edges unweighted?
├── YES → BFS
└── NO → Are there negative edges?
    ├── YES → Bellman-Ford
    └── NO → Dijkstra
```

---

## 7. "Relationship Between Pairs" → Graph

**Core question:** Elements have relationships/connections that affect the answer.

### Reduction Types

| Relationship | Graph Type | Algorithm |
|-------------|-----------|-----------|
| "A depends on B" | Directed edge B→A | Topological sort |
| "A and B are connected" | Undirected edge | Union-Find, DFS |
| "A is before B" | Directed edge A→B | Topological sort |
| "A conflicts with B" | Bipartite check | Graph coloring |
| "A is similar to B" | Weighted edge | Union-Find + weights |

### Common Reductions

| Original Problem | Graph Reduction | Algorithm |
|-----------------|----------------|-----------|
| Course prerequisites | Directed graph of courses | Topological sort |
| Alien dictionary | Directed graph of letters | Topological sort |
| Friend circles | Undirected graph | DFS count / Union-Find |
| Accounts merge | Bipartite of accounts↔emails | Union-Find |
| Equations (a == b, a != b) | Graph of equality | Union-Find + check |
| Bus routes | Graph of routes (shared stops) | BFS |
| Sequence reconstruction | Directed path graph | Topological sort unique |

---

## 8. "Sorted + Search" → Binary Search

**Core question:** Searching in sorted data or finding a threshold.

### Classic Binary Search Patterns

| Problem Statement | Reduced to | Key Insight |
|-----------------|-----------|-------------|
| Find target in sorted array | Classic BS | Compare mid to target |
| Insert position | Lower bound BS | First ≥ target |
| First/last occurrence | Lower + upper bound | Two binary searches |
| Search rotated array | Modified BS | Check which half is sorted |
| Find minimum in rotated | Modified BS | Compare mid to right |

### Binary Search on Answer

| Problem Statement | Feasibility Function F(x) |
|-----------------|--------------------------|
| Koko eating bananas | Can eat all bananas in H hours with speed x? |
| Split array largest sum | Can split into k with max ≤ x? |
| Aggressive cows | Can place cows with min distance ≥ x? |
| Nth root | Is mid^n ≤ m? |
| Capacity to ship | Can ship in D days with capacity x? |

---

## 9. "Subarray/Substring" → Sliding Window or Prefix Sum

**Core question:** Find a contiguous portion that satisfies a condition.

### Reduction: Sliding Window
When condition is monotonic (window becomes less valid as it grows).

| Original Problem | Window Type | Condition |
|-----------------|-------------|-----------|
| Max sum of size k | Fixed window | Aggregate sum |
| Longest substring without repeat | Variable window | All chars unique |
| Longest substring K distinct | Variable window | Distinct ≤ K |
| Min window substring | Variable window | Contains all chars of t |
| Max consecutive ones III | Variable window | Zeroes ≤ K |

### Reduction: Prefix Sum
When condition is based on cumulative sum.

| Original Problem | Reduced to | Key Insight |
|-----------------|-----------|-------------|
| Subarray sum = K | Prefix sum + HashMap | pre[i] - pre[j] = sum(j..i) |
| Subarray sum divisible by K | Prefix mod + HashMap | remainder repeats |
| Range sum query | Prefix sum array | pre[right] - pre[left] |
| Product of array except self | Left/right product arrays | Two passes |

### Decision: Sliding Window vs Prefix Sum
```
Is condition based on sum/product/count of subarray?
├── YES → Is the condition monotonic (can shrink)?
│   ├── YES → Sliding window
│   └── NO → Prefix sum + HashMap
└── NO → Other patterns (two pointers, etc.)
```

---

## 10. Quick Reference Table

| Core Question | Pattern to Reduce To | Secondary Pattern |
|--------------|---------------------|-------------------|
| Max/min with constraints | DP | Greedy (if optimal substructure) |
| Can we assign/fit? | Greedy | Backtracking (if no greedy) |
| Count ways | DP (counting) | Math (combinatorics) |
| Count numbers in range | Digit DP | - |
| Find if exists | HashMap/Set | Binary search (if sorted) |
| Find optimal path | BFS/Dijkstra | Bellman-Ford |
| Relationship between pairs | Graph | Union-Find |
| Sorted + search | Binary search | - |
| Subarray/substring | Sliding window | Prefix sum |
| All subsets/permutations | Backtracking | - |
| Top K / K smallest | Heap | QuickSelect |
| Intervals overlapping | Merge intervals | Sweep line |
| Linked list manipulation | In-place reversal | Fast & slow |
| Tree traversal | DFS/BFS | - |
| Break down into subproblems | Divide & Conquer | - |

### Remember: Most problems reduce to:
1. **Arrays + HashMaps** (simplest but powerful)
2. **Sorting + search** (binary search or two pointers)
3. **Graph traversal** (BFS/DFS for connectivity and paths)
4. **DP** (optimization with overlapping subproblems)
5. **Backtracking** (when you need to try all possibilities)
