# Perfect Squares

**Problem**: Given an integer n, return the minimum number of perfect square numbers (1, 4, 9, 16, ...) that sum to n.

**Example**: `n = 12` → 3 (12 = 4 + 4 + 4)
**Example**: `n = 13` → 2 (13 = 4 + 9)

---

## Recurrence

```
dp[i] = minimum perfect squares summing to i
dp[0] = 0
dp[i] = min(dp[i], dp[i - j*j] + 1) for all j*j ≤ i
```

**Intuition**: To make sum i, pick a perfect square j². The remaining sum is i - j². We need the optimal solution for i - j², plus this one square.

---

## Bottom-Up DP

```java
public int numSquares(int n) {
    int[] dp = new int[n + 1];
    Arrays.fill(dp, Integer.MAX_VALUE);
    dp[0] = 0;

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j * j <= i; j++) {
            dp[i] = Math.min(dp[i], dp[i - j * j] + 1);
        }
    }

    return dp[n];
}
```

### Trace for n = 13

```
dp[0] = 0

dp[1] = min(dp[1], dp[0]+1=1) = 1  (j=1, 1*1=1)
dp[2] = min(dp[2], dp[1]+1=2) = 2  (j=1)
dp[3] = min(dp[3], dp[2]+1=3) = 3  (j=1)
dp[4] = min(dp[4], dp[3]+1=4, dp[0]+1=1) = 1  (j=2, 2*2=4)
dp[5] = min(dp[5], dp[4]+1=2, dp[1]+1=2) = 2  (j=1 or j=2)
dp[6] = min(dp[6], dp[5]+1=3, dp[2]+1=3) = 3
dp[7] = min(dp[7], dp[6]+1=4, dp[3]+1=4) = 4
dp[8] = min(dp[8], dp[7]+1=5, dp[4]+1=2) = 2  (j=2: 4+4)
dp[9] = min(dp[9], dp[8]+1=3, dp[5]+1=3, dp[0]+1=1) = 1  (j=3: 9)
dp[10] = min(dp[10], dp[9]+1=2, dp[6]+1=4, dp[1]+1=2) = 2  (9+1)
dp[11] = min(dp[11], dp[10]+1=3, dp[7]+1=5, dp[2]+1=3) = 3
dp[12] = min(dp[12], dp[11]+1=4, dp[8]+1=3, dp[3]+1=4) = 3  (4+4+4)
dp[13] = min(dp[13], dp[12]+1=4, dp[9]+1=2, dp[4]+1=2) = 2  (9+4)
```

Answer: 2

---

## Lagrange's Four-Square Theorem

Lagrange's theorem states that every natural number can be represented as the sum of at most 4 squares. This gives us:

```java
public int numSquares(int n) {
    // Based on Lagrange's four-square theorem

    // If n is a perfect square → 1
    if (isPerfectSquare(n)) return 1;

    // Check if n = a² + b² → 2
    for (int i = 1; i * i <= n; i++) {
        if (isPerfectSquare(n - i * i)) return 2;
    }

    // Check if n is NOT of the form 4^a(8b+7) → 3
    while (n % 4 == 0) n /= 4;
    if (n % 8 == 7) return 4;

    return 3;
}

private boolean isPerfectSquare(int n) {
    int sqrt = (int) Math.sqrt(n);
    return sqrt * sqrt == n;
}
```

### Explanation of the Mathematical Approach

1. If n is a perfect square → answer is 1
2. If n = a² + b² for some a, b → answer is 2
3. If n is NOT of the form 4^a(8b+7) → answer is 3 (by Legendre's three-square theorem)
4. Otherwise → answer is 4

The mathematical approach is O(√n) instead of O(n√n) for the DP.

---

## BFS Approach

Perfect squares can also be solved using BFS (shortest path in a graph of remainders):

```java
public int numSquares(int n) {
    List<Integer> squares = new ArrayList<>();
    for (int i = 1; i * i <= n; i++) {
        squares.add(i * i);
    }

    Queue<Integer> queue = new LinkedList<>();
    boolean[] visited = new boolean[n + 1];
    queue.offer(0);
    visited[0] = true;
    int level = 0;

    while (!queue.isEmpty()) {
        level++;
        int size = queue.size();
        for (int i = 0; i < size; i++) {
            int curr = queue.poll();
            for (int square : squares) {
                int next = curr + square;
                if (next == n) return level;
                if (next < n && !visited[next]) {
                    visited[next] = true;
                    queue.offer(next);
                }
            }
        }
    }

    return n; // worst case: n = 1+1+...+1 (n times)
}
```

BFS is efficient because we stop as soon as we reach n (shortest path).

---

## Comparison of Approaches

| Approach | Time | Space | Notes |
|---|---|---|---|
| DP | O(n√n) | O(n) | Works for any n |
| BFS | O(n√n) worst | O(n) | Good average case |
| Math (Lagrange) | O(√n) | O(1) | Fastest, O(1) space |

For n = 10,000:
- DP: ~10,000 * 100 = 1 million operations
- Math: ~100 + 10,000 operations = much faster
- BFS: varies, often faster than DP

---

## Reconstruct the Squares

```java
public List<Integer> numSquaresPath(int n) {
    int[] dp = new int[n + 1];
    int[] firstSquare = new int[n + 1];
    Arrays.fill(dp, Integer.MAX_VALUE);
    dp[0] = 0;

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j * j <= i; j++) {
            if (dp[i - j * j] + 1 < dp[i]) {
                dp[i] = dp[i - j * j] + 1;
                firstSquare[i] = j * j;
            }
        }
    }

    List<Integer> path = new ArrayList<>();
    int remaining = n;
    while (remaining > 0) {
        path.add(firstSquare[remaining]);
        remaining -= firstSquare[remaining];
    }
    return path;
}
```

---

## Key Takeaways

1. **Classic unbounded minimization DP** — same pattern as coin change, but with perfect squares as "coins"
2. **Mathematical optimization can reduce O(n√n) to O(√n)** — always mention Lagrange's theorem
3. **BFS is a valid alternative** — finds shortest path in state space
4. **Same recurrence as coin change**: `dp[i] = min(dp[i], dp[i - coin] + 1)` for each coin/square
5. **The j*j ≤ i boundary** is critical — avoids checking squares larger than i
