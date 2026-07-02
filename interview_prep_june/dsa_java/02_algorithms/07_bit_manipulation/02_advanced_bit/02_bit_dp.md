# Bitmask DP

## Common Problems

| Problem | State | Transition |
|---|---|---|
| TSP | dp[mask][last] | dp[mask\|1<<k][k] = min(dp[mask][last] + dist[last][k]) |
| Assignment | dp[mask] | dp[mask\|1<<k] = min(dp[mask] + cost[pop][k]) |
| Hamiltonian Path | dp[mask][last] | Count paths visiting all nodes |

## Key Operations

```java
int all = (1 << n) - 1;
boolean allUsed = mask == all;

// Iterate over unused items
for (int i = 0; i < n; i++) {
    if ((mask & (1 << i)) == 0) { /* use item i */ }
}

// Iterate over submasks
for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {
    // sub is a non-empty subset of mask
}
```

See full details in 05_dynamic_programming/06_dp_with_bitmask/.
