# Binary Search on Answer (Search Space Concept)

## The Key Insight

Binary search isn't just for finding elements in a sorted array. It's a general technique for finding the boundary in a **monotonic search space**.

**Core idea:** If you can answer the question "Is value X feasible?" and the answer is monotonic (no false after true or vice versa), you can binary search on the answer.

## Identifying Monotonic Search Space

A function f(x) is monotonic if it never changes direction. For binary search, we need:

- **Monotonically increasing:** If f(x) is feasible, f(x+1) is also feasible
- **Monotonically decreasing:** If f(x) is feasible, f(x-1) is also feasible

```
Example: Koko Eating Bananas
f(speed) = can eat all bananas within H hours?

speed:  1    2    3    4    5    6    7
f(s):   F    F    F    T    T    T    T
                      ^
                 Answer: minimum feasible speed = 4
```

## When Can We Use Binary Search?

Checklist:
1. The problem asks for a **minimum** or **maximum** value
2. The answer lies in a **bounded range** [L, R]
3. You can write a **feasibility function** f(x) that checks if x is a valid answer
4. The feasibility function is **monotonic**

## F(x) = Feasibility Function

The feasibility function is the core of binary search on answer. It determines whether a candidate answer works.

```java
public class FeasibilityFunction {
    // Generic template
    static boolean isFeasible(int[] arr, int candidate, int k) {
        int count = 1;  // Or whatever tracking you need
        int sum = 0;    // Running sum / count

        for (int value : arr) {
            // Check if adding value still satisfies constraint
            if (sum + value <= candidate) {
                sum += value;
            } else {
                count++;
                sum = value;
            }
        }

        return count <= k;
    }
}
```

## Template: Minimum Feasible Value

Find the **smallest** value x such that f(x) is true.

```java
public class MinFeasible {
    // Find minimum x where isFeasible(x) is true
    public static int findMinimumFeasible(int low, int high) {
        int ans = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (isFeasible(mid)) {
                ans = mid;       // mid is feasible, save it
                high = mid - 1;  // Try to find smaller feasible
            } else {
                low = mid + 1;   // mid is not feasible, need larger
            }
        }

        return ans;
    }

    static boolean isFeasible(int x) {
        return true;  // Problem-specific
    }
}
```

## Template: Maximum Feasible Value

Find the **largest** value x such that f(x) is true.

```java
public class MaxFeasible {
    // Find maximum x where isFeasible(x) is true
    public static int findMaximumFeasible(int low, int high) {
        int ans = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (isFeasible(mid)) {
                ans = mid;       // mid is feasible, save it
                low = mid + 1;   // Try to find larger feasible
            } else {
                high = mid - 1;  // mid is not feasible, need smaller
            }
        }

        return ans;
    }

    static boolean isFeasible(int x) {
        return true;  // Problem-specific
    }
}
```

## Template: While(low < high) Without Ans Variable

For problems where the answer is guaranteed to exist and we want the boundary:

```java
public class BoundarySearch {
    // Find minimum feasible (guaranteed to exist)
    public static int minFeasible(int low, int high) {
        while (low < high) {
            int mid = low + (high - low) / 2;

            if (isFeasible(mid)) {
                high = mid;      // mid is feasible, look left
            } else {
                low = mid + 1;   // mid not feasible, look right
            }
        }

        return low;  // low == high is the minimum feasible
    }

    // Find maximum feasible (guaranteed to exist)
    public static int maxFeasible(int low, int high) {
        while (low < high) {
            // Use ceiling mid to avoid infinite loop
            int mid = low + (high - low + 1) / 2;

            if (isFeasible(mid)) {
                low = mid;       // mid is feasible, look right
            } else {
                high = mid - 1;  // mid not feasible, look left
            }
        }

        return low;
    }

    static boolean isFeasible(int x) {
        return true;
    }
}
```

## Identifying the Search Space

```java
public class SearchSpaceExamples {
    // Problem 1: Aggressive Cows
    // Place C cows in N stalls, maximize minimum distance
    // Search space: [1, max(stalls) - min(stalls)]
    
    // Problem 2: Book Allocation
    // Allocate M books to N students, minimize max pages
    // Search space: [max(book), sum(books)]
    
    // Problem 3: Koko Eating Bananas
    // Min bananas/hour to eat all within H hours
    // Search space: [1, max(piles)]
    
    // Problem 4: Split Array Largest Sum
    // Split into k subarrays, minimize largest sum
    // Search space: [max(nums), sum(nums)]

    // How to find low bound:
    // - The smallest possible answer (often 1 or max single element)
    // How to find high bound:
    // - The largest possible answer (often sum of all or max element)
}
```

## Complete Working Example: Finding Square Root

```java
public class SquareRootUsingBS {
    // Find integer square root of n (floor)
    public static int sqrt(int n) {
        if (n < 2) return n;

        int low = 1;
        int high = n;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if ((long) mid * mid <= n) {
                low = mid + 1;  // mid could be answer, try larger
            } else {
                high = mid - 1; // mid too large
            }
        }

        return high;
    }

    // With double precision
    public static double sqrtPrecision(int n, int precision) {
        double low = 0;
        double high = n;

        while (high - low > Math.pow(10, -precision)) {
            double mid = low + (high - low) / 2;

            if (mid * mid < n) {
                low = mid;
            } else {
                high = mid;
            }
        }

        return low;
    }

    public static void main(String[] args) {
        System.out.println("sqrt(10) = " + sqrt(10));
        System.out.println("sqrt(16) = " + sqrt(16));
        System.out.println("sqrt(25) = " + sqrt(25));
        System.out.println("sqrt(2) = " + sqrtPrecision(2, 4));
    }
}
```

## Recognizing Binary Search on Answer Problems

Look for these patterns in the problem statement:
1. "Minimize the maximum..." → binary search on answer
2. "Maximize the minimum..." → binary search on answer
3. "Find the largest minimum..." → binary search on answer
4. "Find the smallest maximum..." → binary search on answer
5. The answer is a single number with a feasible range

## Common Problems That Use This Pattern

| Problem | Search Space | Feasibility Check |
|---------|-------------|-------------------|
| Aggressive Cows | [1, max-min] | Can we place C cows with min distance ≥ X? |
| Book Allocation | [max, sum] | Can we allocate with max pages ≤ X? |
| Koko Eating Bananas | [1, max] | Can we eat all in ≤ H hours at speed X? |
| Split Array Largest Sum | [max, sum] | Can we split into ≤ K subarrays with max sum ≤ X? |
| Gas Stations | [0, maxDist] | Can we add K stations with max gap ≤ X? |
| Path with Minimum Effort | [0, maxDiff] | Can we reach end with max diff ≤ X? |
| Kth Missing Positive Number | [1, max] | Are there at least K missing numbers up to X? |
| Find Smallest Divisor | [1, max] | Can we divide all with sum ≤ threshold at divisor X? |

## Key Takeaway

> **Binary search on answer transforms an optimization problem into a decision problem.**
> 

Instead of directly finding the optimal answer, you guess an answer and check if it's feasible. The monotonicity guarantees correctness, and binary search guarantees O(log range) guesses.

**Always ask:** Can I write `isFeasible(x)` that returns true/false, and is that function monotonic?
