# Koko Eating Bananas

## Problem Statement

Koko loves bananas. There are `n` piles of bananas, the ith pile has `piles[i]` bananas. The guards have gone and will return in `H` hours.

Koko can decide her bananas-per-hour eating speed `k`. Each hour she chooses a pile and eats `k` bananas from it (if less than `k`, she eats the whole pile and won't eat more that hour).

Find the **minimum integer k** such that she can eat all bananas within H hours.

## Key Insight

This is a "minimize speed" problem. The answer is monotonic: if Koko can eat at speed `k`, she can also eat at speed `k+1`. We binary search to find the minimum feasible speed.

## Implementation

```java
public class KokoEatingBananas {
    public static void main(String[] args) {
        int[] piles = {3, 6, 7, 11};
        int h = 8;
        System.out.println("Minimum eating speed: " +
            minEatingSpeed(piles, h));
        // Output: 4
    }

    public static int minEatingSpeed(int[] piles, int h) {
        // The maximum possible speed is the largest pile
        // (eating more than max pile in an hour doesn't help)
        int low = 1;
        int high = 0;
        for (int p : piles) {
            high = Math.max(high, p);
        }

        int ans = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (canEatAll(piles, h, mid)) {
                ans = mid;          // mid works, try slower
                high = mid - 1;
            } else {
                low = mid + 1;      // mid too slow, need faster
            }
        }

        return ans;
    }

    // Can Koko eat all bananas within H hours at speed k?
    private static boolean canEatAll(int[] piles, int h, int speed) {
        int hours = 0;

        for (int pile : piles) {
            // Ceil division: (pile + speed - 1) / speed
            hours += (pile + speed - 1) / speed;

            if (hours > h) {
                return false;  // Early exit
            }
        }

        return hours <= h;
    }
}
```

## Detail: Ceil Division

The number of hours to eat a pile of `p` bananas at speed `k` is:

```
hours = ceil(p / k)
```

Two ways to compute ceil division without floating point:

```java
// Method 1: (p + k - 1) / k
int hours = (pile + speed - 1) / speed;

// Method 2: p / k + (p % k == 0 ? 0 : 1)
int hours = pile / speed;
if (pile % speed != 0) hours++;

// Method 3: (p - 1) / k + 1 (for positive integers)
int hours = (pile - 1) / speed + 1;
```

## Dry Run

```
piles = [3, 6, 7, 11], h = 8

Search range: low=1, high=11

mid=6: Can eat all at speed 6?
  pile 3: ceil(3/6) = 1h
  pile 6: ceil(6/6) = 1h
  pile 7: ceil(7/6) = 2h
  pile 11: ceil(11/6) = 2h
  total = 6h ≤ 8h → YES, ans=6, high=5

mid=3: Can eat all at speed 3?
  pile 3: ceil(3/3) = 1h
  pile 6: ceil(6/3) = 2h
  pile 7: ceil(7/3) = 3h
  pile 11: ceil(11/3) = 4h
  total = 10h > 8h → NO, low=4

mid=4: Can eat all at speed 4?
  pile 3: ceil(3/4) = 1h
  pile 6: ceil(6/4) = 2h
  pile 7: ceil(7/4) = 2h
  pile 11: ceil(11/4) = 3h
  total = 8h ≤ 8h → YES, ans=4, high=3

mid=5: (low=4, high=5)
  mid = 4 + (5-4)/2 = 4 → feasiable → high=3

  Wait, low=4, high=3, loop exits.

  Actually let me re-do:
  After mid=4 works: ans=4, high=3
  low=4, high=3 → loop exits (4 > 3)

ans=4
```

## Complexity

| Operation | Complexity |
|-----------|------------|
| Finding max pile | O(N) |
| Binary search | O(log maxPile) |
| Feasibility check | O(N) per iteration |
| Total | O(N log maxPile) |
| Space | O(1) |

## Edge Cases and Optimizations

```java
public class KokoEdgeCases {
    // When h >= piles.length * something, we need to handle large h

    public static int minEatingSpeed(int[] piles, int h) {
        int low = 1;
        int high = 1_000_000_000;  // Constraint-based max

        // Optimization: find actual max only if h is small
        for (int p : piles) {
            if (p > high) break;  // Already at max constraint
        }

        // Better: set high to max pile (can't need more than max)
        int maxPile = 0;
        for (int p : piles) {
            maxPile = Math.max(maxPile, p);
        }

        // Optimization: if h == piles.length, Koko must eat max pile/hour
        if (h == piles.length) {
            return maxPile;
        }

        high = maxPile;

        // Optimization: early guess from total bananas
        long total = 0;
        for (int p : piles) total += p;
        low = (int) Math.max(1, total / h);

        int ans = -1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (canEatAll(piles, h, mid)) {
                ans = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }

        return ans;
    }

    private static boolean canEatAll(int[] piles, int h, int speed) {
        long hours = 0;  // Use long to avoid overflow
        for (int p : piles) {
            hours += (p - 1) / speed + 1;
            if (hours > h) return false;
        }
        return true;
    }
}
```

## Variants

### Minimum Number of Days to Make M Bouquets (LeetCode 1482)

```java
public class MinDaysToMakeBouquets {
    public static int minDays(int[] bloomDay, int m, int k) {
        int n = bloomDay.length;
        if ((long) m * k > n) return -1;  // Not enough flowers

        int low = 1;
        int high = 0;
        for (int day : bloomDay) {
            high = Math.max(high, day);
        }

        int ans = -1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (canMake(bloomDay, m, k, mid)) {
                ans = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return ans;
    }

    private static boolean canMake(int[] bloomDay, int m, int k, int day) {
        int bouquets = 0;
        int flowers = 0;

        for (int b : bloomDay) {
            if (b <= day) {
                flowers++;
                if (flowers == k) {
                    bouquets++;
                    flowers = 0;
                }
            } else {
                flowers = 0;  // Reset (non-contiguous)
            }
        }

        return bouquets >= m;
    }
}
```

### Find the Smallest Divisor Given a Threshold (LeetCode 1283)

```java
public class SmallestDivisor {
    public static int smallestDivisor(int[] nums, int threshold) {
        int low = 1;
        int high = 1_000_000;

        while (low < high) {
            int mid = low + (high - low) / 2;
            int sum = 0;
            for (int num : nums) {
                sum += (num - 1) / mid + 1;
            }
            if (sum <= threshold) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }
        return low;
    }
}
```

## Pattern Summary

**"Minimize some constraint with monotonic feasibility" → Binary Search on Answer**

```
Problem:                      Search Space:          Feasibility:
Koko Eating Bananas           [1, max(piles)]        hours(speed) ≤ H
Smallest Divisor              [1, max(nums)]         sum(ceil(num/div)) ≤ threshold
Make M Bouquets               [1, max(bloomDay)]     bouquets(day) ≥ m
Ship Packages                 [max, sum(weights)]    days(capacity) ≤ D
```
