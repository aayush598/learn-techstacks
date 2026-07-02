# Aggressive Cows

## Problem Statement

Given N stalls at positions `stalls[i]` and C cows, place the cows in the stalls such that the **minimum distance between any two cows is maximized**.

**Why binary search?** "Maximize the minimum distance" is a classic hint for binary search on answer.

## Approach

**Search space:** [1, max(stalls) - min(stalls)] — the possible range of minimum distances.

**Feasibility function:** Can we place C cows such that distance between any two is at least X?

```java
import java.util.Arrays;

public class AggressiveCows {
    public static void main(String[] args) {
        int[] stalls = {1, 2, 4, 8, 9};
        int cows = 3;
        System.out.println("Maximum minimum distance: " +
            aggressiveCows(stalls, cows));
        // Output: 3 (place at 1, 4, 8 or 1, 4, 9)
    }

    public static int aggressiveCows(int[] stalls, int cows) {
        Arrays.sort(stalls);

        int n = stalls.length;
        int low = 1;
        int high = stalls[n - 1] - stalls[0];
        int ans = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (canPlaceCows(stalls, cows, mid)) {
                ans = mid;         // mid is feasible, try for larger
                low = mid + 1;
            } else {
                high = mid - 1;    // mid is not feasible, need smaller
            }
        }

        return ans;
    }

    // Check if we can place C cows with minimum distance >= dist
    private static boolean canPlaceCows(int[] stalls, int cows, int dist) {
        int count = 1;            // Place first cow at first stall
        int lastPlaced = stalls[0];

        for (int i = 1; i < stalls.length; i++) {
            if (stalls[i] - lastPlaced >= dist) {
                count++;
                lastPlaced = stalls[i];

                if (count >= cows) {
                    return true;
                }
            }
        }

        return false;
    }
}
```

## Dry Run

```
stalls = [1, 2, 4, 8, 9], cows = 3, sorted = [1, 2, 4, 8, 9]

Binary search range: low=1, high=9-1=8

mid=4: Can we place with dist>=4?
  place at 1, then 8 → count=2 < 3 → NO, high=3

mid=2: Can we place with dist>=2?
  place at 1, 4, 8 → count=3 → YES, ans=2, low=3

mid=3: Can we place with dist>=3?
  place at 1, 4, 8 → count=3 → YES, ans=3, low=4

mid=4: Can we place with dist>=4?
  place at 1, 8 → count=2 < 3 → NO, high=3

low=4 > high=3, exit → ans=3
```

## Edge Cases

```java
public class AggressiveCowsEdgeCases {
    // When cows == 2, answer is always max-min
    // When cows == stalls.length, answer is minimum adjacent difference
    // When all stalls are same position, answer is 0

    public static int aggressiveCows(int[] stalls, int cows) {
        if (stalls.length < cows) return -1;  // Impossible

        Arrays.sort(stalls);

        // Optimization: when cows == 2, answer is max-min
        if (cows == 2) {
            return stalls[stalls.length - 1] - stalls[0];
        }

        int low = 1;
        int high = stalls[stalls.length - 1] - stalls[0];
        int ans = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (canPlace(stalls, cows, mid)) {
                ans = mid;
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }

        return ans;
    }

    private static boolean canPlace(int[] stalls, int cows, int dist) {
        int count = 1;
        int last = stalls[0];

        for (int i = 1; i < stalls.length; i++) {
            if (stalls[i] - last >= dist) {
                count++;
                last = stalls[i];
                if (count >= cows) return true;
            }
        }

        return false;
    }
}
```

## Complexity

| Operation | Complexity |
|-----------|------------|
| Sorting | O(N log N) |
| Binary search | O(log range) where range = max-min |
| Feasibility check per iteration | O(N) |
| Total | O(N log N + N log range) |
| Space | O(1) |

## Variants and Follow-ups

### E-Scooter Placement
Place K charging stations along a road of length L, minimize maximum distance between stations.

### Magnetic Force Between Two Balls (LeetCode 1552)
Same as aggressive cows — place balls in baskets to maximize minimum magnetic force.

```java
public class MagneticForce {
    public static int maxDistance(int[] position, int m) {
        Arrays.sort(position);
        // Same logic as aggressive cows
        return new AggressiveCows().aggressiveCows(position, m);
    }
}
```

### Split Array With Same Average
More complex variant using binary search on average.

## Key Takeaway

The "maximize minimum distance" pattern is a signature of binary search on answer:
1. **Sort** the array (positions need ordering for feasibility check)
2. **Binary search** on the distance
3. **Greedy check** if we can place with that minimum distance
4. Set answer and adjust range based on feasibility
