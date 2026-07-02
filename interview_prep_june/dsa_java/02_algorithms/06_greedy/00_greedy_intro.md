# Greedy Algorithms Introduction

**Greedy**: Make the locally optimal choice at each step, hoping it leads to a globally optimal solution.

---

## When Greedy Works

Greedy works when the problem has:
1. **Greedy Choice Property**: A global optimum can be reached by making local optimal choices
2. **Optimal Substructure**: Optimal solution contains optimal solutions to subproblems

### Proving Greedy

1. **Greedy Stays Ahead**: Show that at each step, the greedy choice is at least as good as any other choice
2. **Exchange Argument**: Show that any optimal solution can be transformed into the greedy solution without worsening it

## Greedy vs DP

| Aspect | Greedy | DP |
|---|---|---|
| Decision | One choice, never reconsider | Explores all choices |
| Optimal | Makes one pass | Backtracking through states |
| Complexity | Usually O(n log n) | Usually O(n²) or more |
| Problems | Activity Selection, Huffman | Knapsack, LCS |

## Common Greedy Problems

| Problem | Greedy Strategy |
|---|---|
| Activity Selection | Earliest finish time |
| Huffman Coding | Merge smallest frequencies |
| Fractional Knapsack | Highest value/weight ratio |
| Minimum Spanning Tree | Kruskal/Prim |
| Dijkstra's Shortest Path | Smallest distance |
