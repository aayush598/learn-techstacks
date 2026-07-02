# Catalan Numbers

## Definition

C₀ = 1, Cₙ₊₁ = Σ Cᵢ * Cₙ₋ᵢ for i=0..n

## Formula

```
C(n) = C(2n, n) / (n + 1) = (2n)! / (n! * (n+1)!)
```

## Sequence

C₀=1, C₁=1, C₂=2, C₃=5, C₄=14, C₅=42, C₆=132, C₇=429...

## Computation

```java
public long catalan(int n) {
    long[] dp = new long[n + 1];
    dp[0] = 1;
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j < i; j++) {
            dp[i] += dp[j] * dp[i - 1 - j];
        }
    }
    return dp[n];
}

// Using combinatorics
public long catalanCombinatorial(int n) {
    return binomial(2 * n, n) / (n + 1);
}
```

## Applications

| Problem | Catalan Number |
|---|---|
| BST count with n nodes | C(n) |
| Valid parentheses with n pairs | C(n) |
| Ways to triangulate polygon | C(n-2) |
| Dyck words of length 2n | C(n) |
| Paths on grid not crossing diagonal | C(n) |
