# Gas Station

**Problem (LeetCode 134)**: There are `n` gas stations arranged in a circular route. You have a car with a gas tank that can store unlimited gas. Each station `i` provides `gas[i]` gallons of gas and costs `cost[i]` gallons to travel to the next station. Find the starting station index from which you can complete the circuit (visit all stations and return to start). Return `-1` if no solution exists.

**Example**:
```
Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
Output: 3

Explanation:
Start at station 3 (gas=4, cost=1):
  Station 3 → 4: tank = 4-1 + 5-3 = 5
  Station 4 → 0: tank = 5 + 1-2 = 4
  Station 0 → 1: tank = 4 + 1-3 = 2
  Station 1 → 2: tank = 2 + 2-4 = 0
  Station 2 → 3: tank = 0 + 3-5 = -2 ... wait, let me recalculate
```

---

## Brute Force: Try Each Station

```java
// Try starting from each station, see if we can complete the circuit
public int canCompleteCircuitBrute(int[] gas, int[] cost) {
    int n = gas.length;
    for (int start = 0; start < n; start++) {
        int tank = 0;
        boolean success = true;
        for (int step = 0; step < n; step++) {
            int station = (start + step) % n;
            tank += gas[station] - cost[station];
            if (tank < 0) {
                success = false;
                break;
            }
        }
        if (success) return start;
    }
    return -1;
}
// Time: O(n²) — for each start, we traverse n stations
// Space: O(1)
```

**Problem**: O(n²) is too slow for n up to 10,000.

---

## Greedy Insight 1: Total Gas Must Be >= Total Cost

```java
// If total gas < total cost, no solution exists
// This is a necessary condition but not sufficient
int totalGas = 0, totalCost = 0;
for (int i = 0; i < gas.length; i++) {
    totalGas += gas[i];
    totalCost += cost[i];
}
if (totalGas < totalCost) return -1;  // impossible
```

**Why this works**: If you sum up all gas gains and all cost losses across the entire circuit, the net must be non-negative. Otherwise, you'd end up with negative gas somewhere regardless of starting point.

---

## Greedy Insight 2: If Starting at i Fails at j, All Stations Between i and j Also Fail

This is the key insight that makes the algorithm O(n).

```
Suppose we start at station i and run out of gas at station j.

Station i → i+1 → ... → j (ran out here)

This means:
  gas[i] - cost[i] + gas[i+1] - cost[i+1] + ... + gas[j-1] - cost[j-1] < 0

Now consider starting at any station k where i < k < j:
  At station k, we'd have:
    tank = gas[k] - cost[k] + gas[k+1] - cost[k+1] + ... + gas[j-1] - cost[j-1]

  But since we started at i and still ran out by j, the segment from i to k-1
  must have been positive (otherwise we'd have failed before k).

  So the segment from k to j-1 is EVEN MORE NEGATIVE than from i to j-1.

Therefore: If start at i fails at j, all stations i, i+1, ..., j-1 also fail.
```

### Visualization

```
Stations:  0    1    2    3    4
Gas:      [1,   2,   3,   4,   5]
Cost:     [3,   4,   5,   1,   2]
Net:      [-2, -2, -2,  +3,  +3]

Start at 0: tank = -2 (fail immediately)
  → Station 0 fails. Try starting at 1.

Start at 1: tank = -2 (fail immediately)
  → Station 1 fails. Try starting at 2.

Start at 2: tank = -2 (fail immediately)
  → Station 2 fails. Try starting at 3.

Start at 3: tank = +3 → station 4: tank = 3+3 = 6 → station 0: 6-2 = 4
  → station 1: 4-2 = 2 → station 2: 2-2 = 0 → back to 3: SUCCESS!

Answer: 3
```

---

## Optimal Solution: One-Pass O(n)

```java
public int canCompleteCircuit(int[] gas, int[] cost) {
    int totalGas = 0;
    int totalCost = 0;
    int tank = 0;        // current gas in tank
    int start = 0;       // potential starting station

    for (int i = 0; i < gas.length; i++) {
        int diff = gas[i] - cost[i];
        totalGas += gas[i];
        totalCost += cost[i];
        tank += diff;

        // If tank goes negative, we can't start from 'start' or any station before i
        // Reset start to the next station
        if (tank < 0) {
            start = i + 1;
            tank = 0;
        }
    }

    // If total gas >= total cost, a solution is guaranteed to exist
    return totalGas >= totalCost ? start : -1;
}
// Time: O(n) — single pass
// Space: O(1)
```

### Step-by-Step Trace

```
gas  = [1, 2, 3, 4, 5]
cost = [3, 4, 5, 1, 2]
diff = [-2, -2, -2, 3, 3]

Iteration:
i=0: diff=-2, tank=-2, tank<0 → start=1, tank=0
i=1: diff=-2, tank=-2, tank<0 → start=2, tank=0
i=2: diff=-2, tank=-2, tank<0 → start=3, tank=0
i=3: diff=3,  tank=3,  tank≥0 → continue
i=4: diff=3,  tank=6,  tank≥0 → continue

totalGas = 1+2+3+4+5 = 15
totalCost = 3+4+5+1+2 = 15
15 >= 15 → return start = 3
```

---

## Why Does This Work? Proof

```
Key Lemma: If we start at station s and fail at station f (running out of gas),
then no station between s and f (inclusive of s, exclusive of f) can be a valid start.

Proof:
Let net[i] = gas[i] - cost[i]

Starting at s, we have:
  tank at s+1 = net[s]
  tank at s+2 = net[s] + net[s+1]
  ...
  tank at f = net[s] + net[s+1] + ... + net[f-1] < 0

Now try starting at any k where s < k < f:
  tank at k+1 = net[k]
  tank at k+2 = net[k] + net[k+1]
  ...
  tank at f = net[k] + net[k+1] + ... + net[f-1]

Since the sum from s to f-1 is negative, and the sum from s to k-1 is
non-negative (we passed those stations), the sum from k to f-1 must be
even more negative.

Therefore: starting at k also fails at f. ∎

Corollary: When we set start = i+1 after tank goes negative at i,
all stations from the previous start to i are guaranteed to fail.
We skip them all in one go.
```

---

## Handling the Circular Route

```java
// The algorithm naturally handles the circular route because:
// 1. We do ONE full pass (i from 0 to n-1)
// 2. If total gas >= total cost, the solution exists
// 3. The start index we found will work for the remaining stations

// But what if we need to verify? We can do a second pass:
public int canCompleteCircuitVerify(int[] gas, int[] cost) {
    int totalGas = 0, totalCost = 0;
    int tank = 0, start = 0;

    // First pass: find candidate start
    for (int i = 0; i < gas.length; i++) {
        int diff = gas[i] - cost[i];
        totalGas += gas[i];
        totalCost += cost[i];
        tank += diff;
        if (tank < 0) {
            start = i + 1;
            tank = 0;
        }
    }

    if (totalGas < totalCost) return -1;

    // Second pass: verify (optional, for correctness proof)
    tank = 0;
    for (int i = 0; i < gas.length; i++) {
        int station = (start + i) % gas.length;
        tank += gas[station] - cost[station];
        if (tank < 0) return -1;  // shouldn't happen if totalGas >= totalCost
    }

    return start;
}
```

---

## Edge Cases

```java
// Edge Case 1: Single station
// gas = [5], cost = [3] → start = 0 (net = 2 ≥ 0)
// gas = [2], cost = [5] → -1 (total gas < total cost)

// Edge Case 2: Two stations
// gas = [3, 3], cost = [2, 4] → start = 0
//   Start 0: tank = 1, then 1 + (3-4) = 0 → works!
// gas = [1, 2], cost = [2, 1] → start = 1
//   Start 0: tank = -1 (fail), start 1: tank = 1, then 1 + (1-2) = 0 → works!

// Edge Case 3: All stations same
// gas = [3, 3, 3], cost = [3, 3, 3] → start = 0 (net = 0 everywhere)

// Edge Case 4: Very large values
// gas = [1000000000, ...], cost = [1, ...]
// Use long for tank if values are large, but int is fine for this problem

// Edge Case 5: No solution
// gas = [1, 2, 3], cost = [4, 5, 6] → totalGas=6, totalCost=15, return -1

// Edge Case 6: Multiple valid starts
// The problem guarantees at most one valid start when totalGas >= totalCost
// But if all net values are 0, any start works (return first, which is 0)
```

---

## Variants

### Variant 1: Return All Valid Starting Stations

```java
public List<Integer> findAllStarts(int[] gas, int[] cost) {
    List<Integer> result = new ArrayList<>();
    int n = gas.length;

    // For each potential start, check if it works
    // This is O(n²) but needed if multiple starts are valid
    for (int start = 0; start < n; start++) {
        int tank = 0;
        boolean valid = true;
        for (int step = 0; step < n; step++) {
            int station = (start + step) % n;
            tank += gas[station] - cost[station];
            if (tank < 0) {
                valid = false;
                break;
            }
        }
        if (valid) result.add(start);
    }
    return result;
}
```

### Variant 2: Minimum Starting Gas

```java
// What if you can bring initial gas? Find minimum initial gas to complete circuit
public int minInitialGas(int[] gas, int[] cost) {
    int tank = 0;
    int minTank = 0;
    for (int i = 0; i < gas.length; i++) {
        tank += gas[i] - cost[i];
        minTank = Math.min(minTank, tank);
    }
    return minTank < 0 ? -minTank : 0;
}
```

### Variant 3: Maximum Stations Visited

```java
// If you can't complete circuit, how many stations can you visit?
public int maxStationsVisited(int[] gas, int[] cost) {
    int n = gas.length;
    int maxVisited = 0;
    for (int start = 0; start < n; start++) {
        int tank = 0;
        int visited = 0;
        for (int step = 0; step < n; step++) {
            int station = (start + step) % n;
            tank += gas[station] - cost[station];
            if (tank < 0) break;
            visited++;
        }
        maxVisited = Math.max(maxVisited, visited);
    }
    return maxVisited;
}
```

---

## Complexity Analysis

```
Time Complexity: O(n)
├── Single pass through gas/cost arrays
├── Each station visited at most once
└── Total work: n iterations

Space Complexity: O(1)
├── Only 4 variables: totalGas, totalCost, tank, start
└── No additional data structures

Comparison with brute force:
├── Brute force: O(n²) time, O(1) space
├── Greedy: O(n) time, O(1) space
└── Improvement: n times faster
```

---

## Common Mistakes

```java
// Mistake 1: Forgetting to check totalGas >= totalCost
// Without this, you might return a start that doesn't work
if (totalGas < totalCost) return -1;  // ESSENTIAL

// Mistake 2: Using int for tank with large values
// If gas[i] and cost[i] can be up to 10^4 and n up to 10^4
// max tank = 10^4 * 10^4 = 10^8 (fits in int)
// But if values are larger, use long

// Mistake 3: Off-by-one in modular arithmetic
// When checking circular route, use (start + step) % n
// NOT start + step (could exceed n)

// Mistake 4: Resetting tank incorrectly
// When tank < 0, set tank = 0 AND start = i + 1
// Don't forget to reset tank!

// Mistake 5: Not handling the case where all stations have net = 0
// totalGas == totalCost, start = 0 is valid
```
