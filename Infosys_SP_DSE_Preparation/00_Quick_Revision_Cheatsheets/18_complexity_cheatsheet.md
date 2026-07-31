# 18. Complexity Cheatsheet

Master reference for time and space complexity of every common algorithm and
data structure. Use to choose the right approach from the input constraints.

## Data structure operations

| Data structure | Access | Search | Insert | Delete | Space |
|---|---|---|---|---|---|
| Array (indexed) | O(1) | O(n) | O(n)* | O(n)* | O(n) |
| Array (append at end) | O(1) | O(n) | O(1) amortized | O(1) pop | O(n) |
| Hash table (dict/set) | O(1) avg | O(1) avg | O(1) avg | O(1) avg | O(n) |
| Hash table (worst) | O(n) | O(n) | O(n) | O(n) | O(n) |
| Linked list (singly) | O(n) | O(n) | O(1) at head | O(1) at head | O(n) |
| Stack | top O(1) | O(n) | push O(1) | pop O(1) | O(n) |
| Queue | front O(1) | O(n) | enqueue O(1) | dequeue O(1) | O(n) |
| Deque (collections.deque) | O(1) ends | O(n) | O(1) both ends | O(1) both ends | O(n) |

*Insert/delete at an arbitrary array index costs O(n) because of shifting.

## Sorting algorithms

| Algorithm | Best | Average | Worst | Space | Stable | In-place |
|---|---|---|---|---|---|---|
| Bubble | O(n) | O(n^2) | O(n^2) | O(1) | Yes | Yes |
| Selection | O(n^2) | O(n^2) | O(n^2) | O(1) | No | Yes |
| Insertion | O(n) | O(n^2) | O(n^2) | O(1) | Yes | Yes |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | No |
| Quick (random pivot) | O(n log n) | O(n log n) | O(n^2) | O(log n) stack | No | Yes |
| Heap | O(n log n) | O(n log n) | O(n log n) | O(1) | No | Yes |
| Counting | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes | No |
| Radix | O(d(n + k)) | O(d(n + k)) | O(d(n + k)) | O(n + k) | Yes | No |
| Timsort (Python sort) | O(n) | O(n log n) | O(n log n) | O(n) | Yes | Yes |

Note: Python's built-in `sorted`/`list.sort` is Timsort — use it, never
implement sorting in an interview unless asked.

## Searching

| Algorithm | Best | Average | Worst | Space |
|---|---|---|---|---|
| Linear search | O(1) | O(n) | O(n) | O(1) |
| Binary search (sorted) | O(1) | O(log n) | O(log n) | O(1) iterative |
| Binary search on answer (parametric) | O(1) | O(log range * check cost) | same | O(1) |

## Trees

| Structure | Search | Insert | Delete | Space |
|---|---|---|---|---|
| BST (unbalanced) | O(log n) avg, O(n) worst | same | same | O(n) |
| Balanced BST (AVL/Red-Black) | O(log n) | O(log n) | O(log n) | O(n) |
| Heap (min/max) | find-min O(1) | push O(log n) | pop O(log n) | O(n) |
| Trie | O(L) per word | O(L) | O(L) | O(total chars) |
| Segment tree | range query O(log n) | point update O(log n) | — | O(4n) |
| Fenwick / BIT | prefix sum O(log n) | point update O(log n) | — | O(n) |
| DSU / Union-Find | find O(alpha(n)) | union O(alpha(n)) | — | O(n) |

## Graph algorithms (V = vertices, E = edges)

| Algorithm | Time | Space |
|---|---|---|
| BFS / DFS | O(V + E) | O(V) |
| Topological sort (Kahn / DFS) | O(V + E) | O(V) |
| Detect cycle (directed, DFS colors) | O(V + E) | O(V) |
| Detect cycle (undirected, DSU) | O(E alpha(V)) | O(V) |
| Dijkstra (binary heap) | O((V + E) log V) | O(V) |
| Dijkstra (dense, array min) | O(V^2) | O(V) |
| Bellman-Ford (single source, negatives) | O(V * E) | O(V) |
| Floyd-Warshall (all pairs) | O(V^3) | O(V^2) |
| Prim's MST (binary heap) | O((V + E) log V) | O(V) |
| Kruskal's MST (sort + DSU) | O(E log E) | O(E) |
| Grid BFS/DFS | O(rows * cols) | O(rows * cols) |

## Classic DP problems

| Problem | Time | Space |
|---|---|---|
| Fibonacci (memoized) | O(n) | O(n) |
| 0/1 knapsack | O(n * W) | O(W) optimized |
| Unbounded knapsack | O(n * W) | O(W) optimized |
| LIS (patience sorting) | O(n log n) | O(n) |
| LCS (two strings) | O(m * n) | O(min(m, n)) |
| Longest palindromic substring | O(n^2) | O(n) |
| Edit distance | O(m * n) | O(min(m, n)) |
| Coin change (min coins) | O(n * amount) | O(amount) |
| Matrix chain multiplication | O(n^3) | O(n^2) |
| Bitmask DP (TSP, assignments) | O(2^n * n) | O(2^n) |
| Longest increasing path in matrix | O(mn) | O(mn) |

## Infer the required complexity from input size

If the constraints say `n` is at most..., you must design an algorithm of about
this cost:

| n | Acceptable complexity | Example approach |
|---|---|---|
| n <= 10 | O(n!) | permutations, brute force |
| n <= 20 | O(2^n) or O(n 2^n) | bitmask DP, subset enumeration |
| n <= 100 | O(n^3) | Floyd-Warshall, matrix chain, triple loop DP |
| n <= 500 | O(n^3) tight, O(n^2) safe | interval DP, all-pairs |
| n <= 10^3 | O(n^2) | LIS, LCS, 2D DP, double loop |
| n <= 10^4 | O(n sqrt n), O(n^2) borderline | sqrt decomposition, sieve+factorize per query |
| n <= 10^5 | O(n log n) | sort-based, binary search, segment tree, Dijkstra, divide & conquer |
| n <= 10^6 | O(n log n) tight, O(n) safe | linear scans, sieve, prefix sums, two pointers, sliding window |
| n <= 10^7 | O(n) | single pass, counting sort, linear algorithms |
| n <= 10^8 | O(n) tight or O(log n) | optimized single pass; often need O(log n) |
| n <= 10^9 or n is not the bottleneck | O(log n) or O(1) | binary search, math formulas, fast exponentiation |

How to read this: scan the largest constraint, multiply with other
dimensions, and confirm your intended algorithm's big-O fits. E.g. two arrays
of size 10^5 -> O(n^2) is 10^10, too slow; reach for O(n log n).

## How to count complexity

### Nested loops

```python
n = 100                         # placeholder — count the iterations

for i in range(n):              # O(n)
    for j in range(n):          # x n -> O(n^2)
        pass

for i in range(n):              # arithmetic loop
    for j in range(i, n):       # n + (n-1) + ... + 1 = O(n^2)
        pass

for i in range(n):              # halving inner loop
    for j in range(1, n, 2):    # n/2 iterations -> O(n^2) still
        pass

for i in range(n):              # O(n log n) total
    j = i                       # each outer step runs log n inner steps
    while j > 0:
        j //= 2
```

Rule: multiply the loop counts, but count the ACTUAL number of inner
iterations (arithmetic progressions collapse to n^2/2 which is still O(n^2)).
Independent loops ADD: O(n) + O(n) = O(n).

### Recursion trees (master theorem shortcuts)

| Recurrence | Complexity |
|---|---|
| T(n) = 2T(n/2) + O(n) | O(n log n) — merge sort, closest pair |
| T(n) = T(n/2) + O(1) | O(log n) — binary search |
| T(n) = T(n/2) + O(n) | O(n) — quickselect average |
| T(n) = 2T(n/2) + O(1) | O(n) — tree traversal |
| T(n) = 2T(n-1) + O(1) | O(2^n) — naive fib / permutations recursion |
| T(n) = T(n-1) + O(n) | O(n^2) — naive selection, insertion sort worst |
| T(n) = 2T(n/2) + O(n^2) | O(n^2) — naive matrix multiply, some D&C |
| T(n) = 3T(n/2) + O(n) | O(n^log2 3) ~ O(n^1.585) |

How to read a recursion tree: depth of the tree x work per level. Binary
search: depth log n, O(1) work per level -> O(log n). Merge sort: depth log n,
O(n) work per level -> O(n log n). Naive Fibonacci: 2^n leaves -> O(2^n).

### Common gotchas

- `str` concatenation in a loop is O(k^2) total (immutable). Build a list and
  `''.join` for O(n).
- `list.count`, `x in list`, `list.index`, `arr.remove` are all O(n) — use
  dict/set for membership O(1).
- `arr.pop(0)` / `del arr[0]` is O(n) — use `collections.deque` for queue.
- `sorted()` on already-sorted data is O(n) with Timsort, worst O(n log n).
- Slicing `arr[k:]` copies — O(n). Repeated slicing causes O(n^2). Use indices.
- `int(s)` on a huge string is O(len(s)) — fine, but repeated large int
  conversion in loops adds up.
- Grids: converting a string grid to lists is O(cells). DFS/BFS over a grid is
  O(rows*cols), not O(edges) of your input string length.
- `any`/`all` short-circuit, but generators pass over the sequence once.
