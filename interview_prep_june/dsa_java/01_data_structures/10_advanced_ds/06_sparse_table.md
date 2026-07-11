# Sparse Table

## Overview

Data structure for **immutable arrays** with **idempotent** range queries (min, max, gcd, lcm) in O(1).

## Implementation: Range Minimum Query

```java
class SparseTable {
    private int[][] st;  // st[i][j] = min of range [i, i + 2^j - 1]
    private int[] log;
    
    SparseTable(int[] arr) {
        int n = arr.length;
        int k = (int) (Math.log(n) / Math.log(2)) + 1;
        
        st = new int[n][k];
        log = new int[n + 1];
        
        // Precompute logs (floor)
        for (int i = 2; i <= n; i++) log[i] = log[i / 2] + 1;
        
        // Initialize with original array
        for (int i = 0; i < n; i++) st[i][0] = arr[i];
        
        // Build sparse table
        for (int j = 1; j < k; j++) {
            for (int i = 0; i + (1 << j) <= n; i++) {
                st[i][j] = Math.min(st[i][j - 1], st[i + (1 << (j - 1))][j - 1]);
            }
        }
    }
    
    int query(int l, int r) {
        int j = log[r - l + 1];
        return Math.min(st[l][j], st[r - (1 << j) + 1][j]);
    }
}
```

## Complexity

| Operation | Time |
|-----------|------|
| Build | O(n log n) |
| Query | O(1) |
| Space | O(n log n) |

## When to Use

- **No updates** to the array (immutable)
- **Idempotent** queries: min, max, gcd, lcm (x ∘ x = x)
- For **range sum** (not idempotent), use prefix sum or segment tree

## Use Cases

```java
// GCD query
st[i][j] = gcd(st[i][j-1], st[i + (1 << (j-1))][j-1]);

// Max query
st[i][j] = Math.max(st[i][j-1], st[i + (1 << (j-1))][j-1]);
```
