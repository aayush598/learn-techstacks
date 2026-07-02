# Digit DP

**Problem**: Count numbers in range [L, R] that satisfy a property (e.g., sum of digits = K, no digit 4, divisible by K).

## State Definition

```
dp[pos][tight][leadingZero][state]
  pos = current position (0 = most significant)
  tight = are we bound by the upper limit?
  leadingZero = are we still placing leading zeros? (for numbers with fewer digits)
  state = property-specific (sum so far, remainder, etc.)
```

## Template

```java
// Count numbers from 0 to limit with sum of digits = K
public int countNumbers(int limit, int K) {
    String s = String.valueOf(limit);
    int n = s.length();
    Integer[][][][] memo = new Integer[n + 1][2][2][K + 1];
    return dp(s, 0, true, true, 0, K, memo);
}

private int dp(String s, int pos, boolean tight, boolean leadingZero,
               int sum, int K, Integer[][][][] memo) {
    if (pos == s.length()) {
        return (sum == K && !leadingZero) ? 1 : 0;
    }

    if (memo[pos][tight ? 1 : 0][leadingZero ? 1 : 0][sum] != null) {
        return memo[pos][tight ? 1 : 0][leadingZero ? 1 : 0][sum];
    }

    int limit = tight ? s.charAt(pos) - '0' : 9;
    int count = 0;

    for (int d = 0; d <= limit; d++) {
        boolean nextTight = tight && (d == limit);
        boolean nextLeadingZero = leadingZero && (d == 0);

        if (sum + d > K) continue; // prune

        count += dp(s, pos + 1, nextTight, nextLeadingZero,
                   sum + d, K, memo);
    }

    memo[pos][tight ? 1 : 0][leadingZero ? 1 : 0][sum] = count;
    return count;
}
```

## Key Insights

1. **Solve for [0, R], subtract [0, L-1]** to get [L, R]
2. **tight** flag ensures we don't exceed the limit
3. **leadingZero** handles numbers with fewer digits
4. **pos** goes from most significant to least significant digit
5. **All states are bounded**: pos ≤ 20 (max digits), tight = 2, leadingZero = 2, state ≤ small number
