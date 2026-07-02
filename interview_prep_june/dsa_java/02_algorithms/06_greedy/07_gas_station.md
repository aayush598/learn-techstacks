# Gas Station

**Problem**: Circular route with gas stations. Each station has gas[i] and cost[i] to reach next station. Find starting station to complete circuit.

**Greedy**: If total gas ≥ total cost, a solution exists. Start from station where running total deficit resets.

```java
public int canCompleteCircuit(int[] gas, int[] cost) {
    int totalGas = 0, totalCost = 0;
    for (int i = 0; i < gas.length; i++) {
        totalGas += gas[i];
        totalCost += cost[i];
    }

    if (totalGas < totalCost) return -1;

    int start = 0, tank = 0;
    for (int i = 0; i < gas.length; i++) {
        tank += gas[i] - cost[i];
        if (tank < 0) {
            start = i + 1;
            tank = 0;
        }
    }

    return start;
}
```

## Key Insight

> If you run out of gas before reaching a station, no station between start and that station works either. Reset start to the next station and continue.
