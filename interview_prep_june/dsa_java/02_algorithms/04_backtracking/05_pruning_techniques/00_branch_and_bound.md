# Branch and Bound

Branch and bound is an optimization technique for backtracking that **prunes branches that cannot lead to a better solution than the current best**. It's commonly used for optimization problems (minimization/maximization).

Unlike plain backtracking (which prunes only invalid solutions), branch and bound also prunes **valid but suboptimal** solutions.

---

## Core Concept

```
Backtracking:    Prune only when solution is INVALID
Branch & Bound:  Prune when solution is INVALID OR WORSE than current best
```

### The Key Components

1. **Branch**: Generate child nodes (like backtracking)
2. **Bound**: Calculate a lower/upper bound on the best possible solution from this branch
3. **Prune**: If bound is worse than current best, skip the branch

### Template

```java
double best = Double.POSITIVE_INFINITY; // for minimization
// or best = 0 for maximization

void branchAndBound(state, currentCost) {
    if (isComplete(state)) {
        best = min(best, currentCost); // update best
        return;
    }

    // Calculate optimistic bound
    double bound = calculateBound(state);

    // Prune: if even the optimistic bound is worse than best
    if (bound >= best) return; // for minimization

    for (choice : choices) {
        if (isValid(choice)) {
            makeChoice(choice);
            branchAndBound(newState, currentCost + cost(choice));
            unmakeChoice(choice);
        }
    }
}
```

---

## Traveling Salesman with Branch and Bound

**Problem**: Find the shortest Hamiltonian cycle visiting all cities exactly once and returning to the start.

### Simple Backtracking

```java
public int tsp(int[][] graph) {
    int n = graph.length;
    boolean[] visited = new boolean[n];
    visited[0] = true;
    return backtrack(graph, visited, 0, 0, 1, n);
}

private int backtrack(int[][] graph, boolean[] visited,
                      int currentCity, int currentCost,
                      int count, int n) {
    if (count == n) {
        return currentCost + graph[currentCity][0]; // return to start
    }

    int minCost = Integer.MAX_VALUE;

    for (int nextCity = 0; nextCity < n; nextCity++) {
        if (!visited[nextCity]) {
            visited[nextCity] = true;
            int cost = backtrack(graph, visited, nextCity,
                                 currentCost + graph[currentCity][nextCity],
                                 count + 1, n);
            minCost = Math.min(minCost, cost);
            visited[nextCity] = false;
        }
    }

    return minCost;
}
```

### With Branch and Bound

```java
public int tspBranchAndBound(int[][] graph) {
    int n = graph.length;

    // Precompute minimum edge from each city (for bound calculation)
    int[] minEdge = new int[n];
    for (int i = 0; i < n; i++) {
        minEdge[i] = Integer.MAX_VALUE;
        for (int j = 0; j < n; j++) {
            if (i != j) minEdge[i] = Math.min(minEdge[i], graph[i][j]);
        }
    }

    boolean[] visited = new boolean[n];
    visited[0] = true;
    int[] best = {Integer.MAX_VALUE};

    backtrack(graph, visited, 0, 0, 1, n, minEdge, best);
    return best[0];
}

private void backtrack(int[][] graph, boolean[] visited,
                       int currentCity, int currentCost,
                       int count, int n, int[] minEdge,
                       int[] best) {
    // Calculate lower bound for remaining cities
    int lowerBound = currentCost;

    // Add minimum edge cost from current city to any unvisited city
    int minFromCurrent = Integer.MAX_VALUE;
    for (int i = 1; i < n; i++) {
        if (!visited[i]) {
            minFromCurrent = Math.min(minFromCurrent, graph[currentCity][i]);
        }
    }
    if (minFromCurrent != Integer.MAX_VALUE) {
        lowerBound += minFromCurrent;
    }

    // Add minimum edge cost for each unvisited city (to come and go)
    for (int i = 1; i < n; i++) {
        if (!visited[i]) {
            lowerBound += minEdge[i];
        }
    }

    // PRUNE: if lower bound is already worse than best
    if (lowerBound >= best[0]) return;

    if (count == n) {
        int totalCost = currentCost + graph[currentCity][0];
        best[0] = Math.min(best[0], totalCost);
        return;
    }

    for (int nextCity = 1; nextCity < n; nextCity++) {
        if (!visited[nextCity]) {
            visited[nextCity] = true;
            backtrack(graph, visited, nextCity,
                     currentCost + graph[currentCity][nextCity],
                     count + 1, n, minEdge, best);
            visited[nextCity] = false;
        }
    }
}
```

### Better Bound: Minimum Spanning Tree

A tighter bound: the cost of the minimum spanning tree (MST) of the remaining unvisited cities plus entry/exit edges.

```java
private int calculateBound(int[][] graph, boolean[] visited,
                           int currentCity, int currentCost) {
    int n = graph.length;

    // Current cost so far
    int bound = currentCost;

    // Minimum edge from current city to any unvisited city
    int minToUnvisited = Integer.MAX_VALUE;
    // Minimum edge from any unvisited city back to start
    int minFromUnvisitedToStart = Integer.MAX_VALUE;

    for (int i = 1; i < n; i++) {
        if (!visited[i]) {
            minToUnvisited = Math.min(minToUnvisited, graph[currentCity][i]);
            minFromUnvisitedToStart = Math.min(minFromUnvisitedToStart, graph[i][0]);

            // Find minimum adjacent edge for this unvisited city
            int minAdj = Integer.MAX_VALUE;
            for (int j = 1; j < n; j++) {
                if (i != j) {
                    minAdj = Math.min(minAdj, graph[i][j]);
                }
            }
            bound += minAdj;
        }
    }

    if (minToUnvisited != Integer.MAX_VALUE) bound += minToUnvisited;
    if (minFromUnvisitedToStart != Integer.MAX_VALUE) bound += minFromUnvisitedToStart;

    return bound;
}
```

---

## N-Queens with Pruning

N-Queens naturally uses pruning (we check validity before placing). But we can add more pruning:

```java
public int totalNQueensWithPruning(int n) {
    boolean[] cols = new boolean[n];
    boolean[] diag1 = new boolean[2 * n];
    boolean[] diag2 = new boolean[2 * n];
    return backtrack(n, 0, cols, diag1, diag2);
}

private int backtrack(int n, int row,
                      boolean[] cols, boolean[] diag1, boolean[] diag2) {
    if (row == n) return 1;

    int count = 0;

    // Count remaining rows for pruning (optional, here for illustration)
    int remainingRows = n - row;

    // Check if we can still place remaining queens
    // (In N-Queens, we always can if there's at least one column free,
    //  but for heavily constrained variants, this matters)

    for (int col = 0; col < n; col++) {
        int d1 = row - col + n - 1;
        int d2 = row + col;

        if (cols[col] || diag1[d1] || diag2[d2]) continue;

        // Bound: after placing this queen, can we place remaining?
        if (remainingRows > 1) {
            // Quick check: are there enough free columns for remaining queens?
            int freeCols = 0;
            for (int c = 0; c < n; c++) {
                if (!cols[c]) freeCols++;
            }
            if (freeCols < remainingRows) continue; // prune
        }

        cols[col] = diag1[d1] = diag2[d2] = true;
        count += backtrack(n, row + 1, cols, diag1, diag2);
        cols[col] = diag1[d1] = diag2[d2] = false;
    }

    return count;
}
```

---

## 0/1 Knapsack with Branch and Bound

```java
public int knapsackBranchAndBound(int[] values, int[] weights, int capacity) {
    int n = values.length;

    // Items sorted by value/weight ratio
    Item[] items = new Item[n];
    for (int i = 0; i < n; i++) {
        items[i] = new Item(values[i], weights[i], i);
    }
    Arrays.sort(items, (a, b) -> Double.compare(b.ratio, a.ratio));

    int[] best = {0};
    backtrack(items, 0, 0, 0, capacity, best);
    return best[0];
}

private void backtrack(Item[] items, int index,
                       int currentValue, int currentWeight,
                       int capacity, int[] best) {
    // Bound: optimistic estimate = currentValue + fractional knapsack of remaining
    double bound = currentValue + fractionalBound(items, index, currentWeight, capacity);

    // Prune: if bound can't beat best
    if (bound <= best[0]) return;

    if (index == items.length) {
        best[0] = Math.max(best[0], currentValue);
        return;
    }

    // Try including this item
    if (currentWeight + items[index].weight <= capacity) {
        backtrack(items, index + 1,
                 currentValue + items[index].value,
                 currentWeight + items[index].weight,
                 capacity, best);
    }

    // Try excluding this item
    backtrack(items, index + 1, currentValue, currentWeight, capacity, best);
}

private double fractionalBound(Item[] items, int start,
                               int currentWeight, int capacity) {
    double bound = 0;
    int remaining = capacity - currentWeight;

    for (int i = start; i < items.length; i++) {
        if (items[i].weight <= remaining) {
            bound += items[i].value;
            remaining -= items[i].weight;
        } else {
            bound += items[i].ratio * remaining;
            break;
        }
    }

    return bound;
}

static class Item {
    int value, weight;
    double ratio;
    Item(int v, int w, int i) {
        this.value = v;
        this.weight = w;
        this.ratio = (double) v / w;
    }
}
```

---

## General Pruning Strategies

| Strategy | Description | Example |
|---|---|---|
| **Feasibility pruning** | Can't reach a valid solution | Sum exceeded target |
| **Optimality pruning** | Can't beat current best | Branch and bound |
| **Symmetry pruning** | Skip symmetric solutions | N-Queens half-board |
| **Dominance pruning** | Skip dominated choices | TSP: skip city if order doesn't matter |
| **Memorization** | Cache visited states | With identical subproblems |

### Pruning Template

```java
boolean shouldPrune(state) {
    // 1. Check feasibility
    if (!isFeasible(state)) return true;

    // 2. Check optimality (for optimization problems)
    if (lowerBound >= best) return true;

    // 3. Check symmetry
    if (isSymmetricDuplicate(state)) return true;

    // 4. Check dominance
    if (isDominated(state)) return true;

    return false;
}
```

---

## Branch and Bound vs Backtracking

| Aspect | Backtracking | Branch and Bound |
|---|---|---|
| Goal | Find all/any valid solutions | Find optimal solution |
| Pruning | Invalid branches | Invalid + suboptimal branches |
| Bounding | None | Lower/upper bound estimate |
| Use case | Combinatorial enumeration | Optimization problems |
| Examples | Subsets, permutations, N-Queens | TSP, Knapsack, Assignment |

## Key Takeaways

1. **Bound calculation is the key** — tighter bounds mean more pruning
2. **Order matters** — explore promising branches first (better best = more pruning later)
3. **For minimization**: prune if `lowerBound >= best`
4. **For maximization**: prune if `upperBound <= best`
5. **Branch and bound is exact** — it finds the optimal solution, just faster than blind search
6. **Heuristics for initial best** — running a greedy algorithm first gives a good initial best value
