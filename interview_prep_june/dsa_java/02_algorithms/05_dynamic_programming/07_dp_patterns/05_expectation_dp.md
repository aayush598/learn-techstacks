# Expected Value DP

**Problem**: Calculate the expected number of steps/time to reach a goal state in a probabilistic process.

## Formula

```
E[i] = expected value from state i

E[i] = sum(p[i→j] * (cost[i→j] + E[j])) for all transitions j

Base: E[goal] = 0 (no more steps needed at goal)
```

## Example: Expected Dice Rolls to Reach Target Sum

```java
public double expectedRollsToReachTarget(int target) {
    double[] dp = new double[target + 1];
    // dp[i] = expected rolls to reach target from sum i

    for (int i = target - 1; i >= 0; i--) {
        double sum = 0;
        for (int die = 1; die <= 6; die++) {
            int next = Math.min(target, i + die);
            sum += (1.0 / 6) * (1 + dp[next]);
        }
        dp[i] = sum;
    }

    return dp[0];
}
```

## Example: Frog Jump (Expected Value)

```java
public double frogExpectedJumps(int n, int[] stones) {
    // frog at stone i jumps to next stone with some probability
    double[] dp = new double[n];
    // dp[i] = expected jumps from stone i to reach the end

    for (int i = n - 2; i >= 0; i--) {
        int reachable = Math.min(6, n - 1 - i);
        double sum = 0;
        for (int j = 1; j <= reachable; j++) {
            sum += (1.0 / reachable) * (1 + dp[i + j]);
        }
        dp[i] = sum;
    }

    return dp[0];
}
```

## Key Insights

1. **Process from goal backwards** — E[goal] = 0, compute E[i] for i < goal
2. **Each transition**: probability × (cost + expected value from next state)
3. **Base case**: E[goal] = 0 (no more steps needed)
4. **Simultaneous equations** when there are cycles — use linear algebra

## Key Takeaways

1. **For DAG processes**: compute from end to start (backward DP)
2. **For processes with cycles**: solve system of linear equations
3. **Formula**: E[i] = 1 + Σ(p_j * E[j]) when cost = 1 per step
4. **Expected value problems** often appear as "expected number of steps"
