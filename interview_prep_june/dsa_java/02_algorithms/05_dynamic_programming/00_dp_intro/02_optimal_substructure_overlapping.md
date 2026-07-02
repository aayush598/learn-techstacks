# Optimal Substructure & Overlapping Subproblems

These are the two essential properties that make a problem solvable with DP.

---

## Optimal Substructure

A problem has **optimal substructure** if an optimal solution to the whole problem contains optimal solutions to its subproblems.

### Formal Definition

```
If solution S* is optimal for problem P,
and S* = combine(S1*, S2*, ..., Sk*),
where S1*, S2*, ..., Sk* are optimal for subproblems P1, P2, ..., Pk,
then P has optimal substructure.
```

### ✅ Examples with Optimal Substructure

**Fibonacci**
```
fib(5) = fib(4) + fib(3)
The optimal (and only) value of fib(5) uses fib(4) and fib(3)
✓ Has optimal substructure
```

**Shortest Path**
```
shortestPath(A, C) = shortestPath(A, B) + shortestPath(B, C)
If we take the shortest path A→B→C, then A→B is the shortest path from A to B
✓ Has optimal substructure
```

**0/1 Knapsack**
```
Best value with capacity W and items [0..i]:
  = max(best with capacity W and items [0..i-1],  ← exclude i
        best with capacity W-wi and items [0..i-1] + vi)  ← include i
✓ Has optimal substructure
```

**Minimum Coin Change**
```
minCoins(amount) = 1 + min(minCoins(amount - coin)) for all coins
The optimal solution to amount depends on optimal solutions to amount-coin
✓ Has optimal substructure
```

### ❌ Examples WITHOUT Optimal Substructure

**Longest Path (in general graph)**
```
Longest path from A to C through B:
  longest(A, C) = longest(A, B) + longest(B, C)
  But the longest path from A to B might visit nodes that are needed for B to C!
✗ Does NOT have optimal substructure
```

**Why?** The longest simple path problem doesn't have optimal substructure because subproblem solutions are not independent. The longest path from A to B might use nodes that conflict with the longest path from B to C.

### Testing for Optimal Substructure

```
Ask: Does knowing the optimal solution to subproblems guarantee
      an optimal solution to the whole problem?

If the answer is YES → DP is a candidate.
If NO → DP likely doesn't work.
```

---

## Overlapping Subproblems

A problem has **overlapping subproblems** if the same subproblem is solved multiple times by a naive recursive algorithm.

### ✅ Examples with Overlapping Subproblems

**Fibonacci**
```
fib(5)
  = fib(4) + fib(3)
  = (fib(3) + fib(2)) + (fib(2) + fib(1))
  = ((fib(2) + fib(1)) + fib(2)) + (fib(2) + fib(1))

fib(3) is computed 2 times
fib(2) is computed 3 times
fib(1) is computed 2 times
✓ Massive overlap
```

### ❌ Examples WITHOUT Overlapping Subproblems

**Binary Search**
```
binarySearch(arr, target, 0, n-1):
  mid = (0+n-1)/2
  if arr[mid] == target: return mid
  if arr[mid] < target: return binarySearch(arr, target, mid+1, n-1)
  if arr[mid] > target: return binarySearch(arr, target, 0, mid-1)

Each recursive call is on a DIFFERENT subarray.
No two calls work on the same subarray.
✗ No overlap
```

**Mergesort**
```
mergesort(arr, 0, n-1):
  mergesort(arr, 0, mid)
  mergesort(arr, mid+1, n-1)
  merge(arr, 0, mid, n-1)

Each call divides the array into NON-OVERLAPPING parts.
No subarray is processed twice.
✗ No overlap
```

### Testing for Overlap

```
Draw the recursion tree:
  - If the same node appears multiple times → has overlap
  - If all nodes are distinct → no overlap

Size of state space vs number of calls:
  - If number of calls > number of possible states → overlap exists
  - If number of calls = number of states → no overlap
```

---

## Why Both Properties Are Needed for DP

| Property | Purpose | Analogy |
|---|---|---|
| Optimal substructure | Problem CAN be solved via subproblems | Break into pieces |
| Overlapping subproblems | Solving subproblems once is BENEFICIAL | Don't repeat work |

### What If Only One Property Holds?

**Only optimal substructure (no overlap): Use Divide & Conquer**
```
Mergesort: has optimal substructure but no overlap
→ Use recursion/divide-and-conquer, not DP
→ Memoization wouldn't help (each subproblem is unique)
```

**Only overlap (no optimal substructure): Use brute force or heuristics**
```
Longest path: has overlapping subproblems in naive recursion
  but no optimal substructure
→ DP doesn't guarantee correct solution
→ Use brute force for small graphs, or heuristics for large ones
```

---

## DP vs Greedy vs Divide & Conquer

```
                    Can be broken into subproblems?
                           /        \
                        YES          NO → Brute force
                       /    \
            Optimal substructure?
                  /        \
                YES         NO → Backtracking / Heuristics
              /      \
        Overlapping subproblems?
            /           \
          YES            NO
           |              |
           DP        Divide & Conquer
```

### Example: Fractional vs 0/1 Knapsack

```java
// FRACTIONAL KNAPSACK (Greedy works)
// Optimal substructure ✓, and greedy choice property holds
// → Greedy: sort by value/weight, take fractions

// 0/1 KNAPSACK (DP needed)
// Optimal substructure ✓, but greedy choice fails
// → DP: dp[i][w] = max(dp[i-1][w], dp[i-1][w-wi] + vi)
// → Overlapping subproblems: dp[i-1][w] is used in multiple computations
```

---

## Practical Examples Side by Side

| Problem | Opt. Substructure | Overlap | Best Approach |
|---|---|---|---|
| Fibonacci | ✓ | ✓ | DP |
| Binary Search | ✓ | ✗ | Divide & Conquer |
| Mergesort | ✓ | ✗ | Divide & Conquer |
| N-Queens | ✗ | ✗ | Backtracking |
| LCS | ✓ | ✓ | DP |
| Shortest Path (DAG) | ✓ | ✓ | DP |
| Minimum Spanning Tree | ✓ | ✗ | Greedy (Kruskal/Prim) |
| Knapsack 0/1 | ✓ | ✓ | DP |

## Key Insight

> Not every problem that can be divided into subproblems is suitable for DP. You need both properties: the ability to combine subproblem solutions (optimal substructure) AND the need to avoid recomputing them (overlapping subproblems).
