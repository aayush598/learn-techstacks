# 01 — Recursion Patterns

Not all recursion is the same. There are distinct patterns that map to different types of problems. Once you recognize the pattern, the solution structure follows naturally.

---

## 1. Decrease and Conquer — T(n) = T(n-1) + ...

**One subproblem, reduced by a constant amount.** The simplest recursion pattern.

### Template

```java
Result solve(Problem p) {
    if (isBaseCase(p)) {
        return baseResult;
    }
    // Reduce problem: p → smaller instance
    Result subResult = solve(reducedProblem);
    // Combine: subResult + current work
    return combine(currentWork, subResult);
}
```

### Examples

```java
// Factorial: T(n) = T(n-1) + O(1)
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// Sum of first n numbers: T(n) = T(n-1) + O(1)
int sum(int n) {
    if (n == 0) return 0;
    return n + sum(n - 1);
}

// Power: T(n) = T(n-1) + O(1)
int power(int base, int exp) {
    if (exp == 0) return 1;
    return base * power(base, exp - 1);
}

// Linear search: T(n) = T(n-1) + O(1)
int linearSearch(int[] arr, int target, int index) {
    if (index >= arr.length) return -1;
    if (arr[index] == target) return index;
    return linearSearch(arr, target, index + 1);
}
```

### Complexity: O(n) time, O(n) stack space

---

## 2. Divide and Conquer — T(n) = 2T(n/2) + ...

**Two (or more) subproblems, each half (or fraction) the size.** The dominant pattern for efficient algorithms.

### Template

```java
Result solve(Problem p) {
    if (isBaseCase(p)) {
        return baseResult;
    }
    // Divide
    Problem left = leftHalf(p);
    Problem right = rightHalf(p);
    // Conquer
    Result leftResult = solve(left);
    Result rightResult = solve(right);
    // Combine
    return merge(leftResult, rightResult);
}
```

### Examples

```java
// Binary search (a=1, not 2 — one subproblem)
int binarySearch(int[] arr, int target, int low, int high) {
    if (low > high) return -1;
    int mid = low + (high - low) / 2;
    if (arr[mid] == target) return mid;
    if (arr[mid] < target)
        return binarySearch(arr, target, mid + 1, high);
    return binarySearch(arr, target, low, mid - 1);
}
// T(n) = T(n/2) + O(1) → O(log n) — only ONE subproblem

// Find max in array (two subproblems)
int findMax(int[] arr, int low, int high) {
    if (low == high) return arr[low];
    int mid = low + (high - low) / 2;
    int leftMax = findMax(arr, low, mid);
    int rightMax = findMax(arr, mid + 1, high);
    return Math.max(leftMax, rightMax);
}
// T(n) = 2T(n/2) + O(1) → O(n)

// Merge sort
void mergeSort(int[] arr, int low, int high) {
    if (low >= high) return;
    int mid = low + (high - low) / 2;
    mergeSort(arr, low, mid);
    mergeSort(arr, mid + 1, high);
    merge(arr, low, mid, high);
}
// T(n) = 2T(n/2) + O(n) → O(n log n)
```

---

## 3. Multiple (2+) Recursive Calls — T(n) = T(n-1) + T(n-2) + ...

**Exponential explosion!** Each call makes multiple calls, creating a tree of recursive calls.

### Template

```java
Result solve(Problem p) {
    if (isBaseCase(p)) {
        return baseResult;
    }
    // Make multiple recursive calls to smaller instances
    Result r1 = solve(reduce1(p));
    Result r2 = solve(reduce2(p));
    // ...
    return combine(r1, r2, ...);
}
```

### Examples

```java
// Fibonacci (naive): T(n) = T(n-1) + T(n-2) + O(1)
int fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}
// Recursion tree: binary tree of height n → O(2ⁿ) nodes

// Staircase problem: climb 1 or 2 steps
int countWays(int n) {
    if (n <= 1) return 1;
    return countWays(n - 1) + countWays(n - 2);
}
// Same pattern as Fibonacci!

// Triple-step: climb 1, 2, or 3 steps
int countWays(int n) {
    if (n < 0) return 0;
    if (n == 0) return 1;
    return countWays(n - 1) + countWays(n - 2) + countWays(n - 3);
}
// T(n) ≈ T(n-1) + T(n-2) + T(n-3) → O(3ⁿ) even worse!
```

### The Memoization Fix

```java
// Fibonacci with memoization — O(n)!
int fib(int n, int[] memo) {
    if (n <= 1) return n;
    if (memo[n] != 0) return memo[n];
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo);
    return memo[n];
}
// Now each n is computed once → O(n) time, O(n) space
```

---

## 4. Include/Exclude Pattern — T(n) = 2T(n-1)

**At each step, decide whether to include the current element.** Used for subsets, combinations, and knapsack-like problems.

### Template

```java
void solve(int[] arr, int index, List<Integer> current, List<List<Integer>> result) {
    if (index == arr.length) {
        result.add(new ArrayList<>(current));
        return;
    }

    // EXCLUDE current element
    solve(arr, index + 1, current, result);

    // INCLUDE current element
    current.add(arr[index]);
    solve(arr, index + 1, current, result);
    current.remove(current.size() - 1);  // backtrack!
}
```

### Examples

```java
// Generate all subsets (power set)
void subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    generate(nums, 0, new ArrayList<>(), result);
    System.out.println(result);
}

void generate(int[] nums, int index, List<Integer> current, List<List<Integer>> result) {
    if (index == nums.length) {
        result.add(new ArrayList<>(current));
        return;
    }
    // Exclude
    generate(nums, index + 1, current, result);
    // Include
    current.add(nums[index]);
    generate(nums, index + 1, current, result);
    current.remove(current.size() - 1);  // backtrack
}
// Subsets of [1,2,3]: [[], [3], [2], [2,3], [1], [1,3], [1,2], [1,2,3]]
// T(n) = 2T(n-1) → O(2ⁿ)

// Subset sum — does any subset sum to target?
boolean subsetSum(int[] arr, int index, int remaining) {
    if (remaining == 0) return true;
    if (index == arr.length) return false;

    // Exclude
    if (subsetSum(arr, index + 1, remaining)) return true;
    // Include
    if (subsetSum(arr, index + 1, remaining - arr[index])) return true;

    return false;
}
// T(n) = 2T(n-1) + O(1) → O(2ⁿ)
```

---

## 5. Recursion Tree Method

The recursion tree helps you visualize the recursive calls and calculate total work.

### How to Draw

1. Root = initial problem of size n
2. Children = subproblems
3. Each node = work at that level (without recursion)
4. Sum work at each level
5. Sum across all levels

### Example: Merge Sort T(n) = 2T(n/2) + n

```
Level 0:                   [n]
                         /     \
Level 1:              [n/2]   [n/2]
                     /   \    /    \
Level 2:         [n/4] [n/4] [n/4] [n/4]
                 / \    / \   / \   / \
Level 3:      n/8 n/8 n/8 n/8 n/8 n/8 n/8 n/8
```

```
Level 0: 1 node, work = n
Level 1: 2 nodes, each n/2, total = n
Level 2: 4 nodes, each n/4, total = n
Level 3: 8 nodes, each n/8, total = n
...
Level log₂n: n nodes, each 1, total = n

Total work = n × log₂n = O(n log n)
```

### Example: T(n) = 3T(n/2) + O(n²)

```
Level 0: 1 node × n²            = n²
Level 1: 3 nodes × (n/2)²       = (3/4)n²
Level 2: 9 nodes × (n/4)²       = (9/16)n²
Level 3: 27 nodes × (n/8)²      = (27/64)n²
```

Geometric series: n² × [1 + 3/4 + (3/4)² + (3/4)³ + ...]
= n² × 1/(1-3/4) = n² × 4 = O(n²)

Since 3/4 < 1, the series converges! Top level dominates → Case 3 of MT.

### Example: T(n) = T(n/3) + T(2n/3) + O(n)

```
Level 0:                 [n]
                       /     \
Level 1:           [n/3]   [2n/3]
                 /    \     /    \
Level 2:      [n/9] [2n/9][2n/9][4n/9]
```

Each level sums to n. The longest path (always taking the 2n/3 branch) has length log_{3/2}n. So total = n × log_{3/2}n = O(n log n).

---

## 6. 10 Pattern Templates with Code

### Pattern 1: Linear Single Call

```java
void linear(int n) {
    if (n == 0) return;
    // do work
    linear(n - 1);
}
// T(n) = T(n-1) + O(1) → O(n)
```

### Pattern 2: Logarithmic Single Call

```java
void logarithmic(int n) {
    if (n <= 1) return;
    // do O(1) work
    logarithmic(n / 2);
}
// T(n) = T(n/2) + O(1) → O(log n)
```

### Pattern 3: Logarithmic with Linear Work

```java
void logLinear(int n) {
    if (n <= 1) return;
    // do O(n) work
    for (int i = 0; i < n; i++) { /* O(1) */ }
    logarithmic(n / 2);
}
// T(n) = T(n/2) + O(n) → O(n) — dominated by top level
```

### Pattern 4: Divide and Conquer Split

```java
void divideConquer(int[] arr, int l, int r) {
    if (l >= r) return;
    int mid = l + (r - l) / 2;
    divideConquer(arr, l, mid);
    divideConquer(arr, mid + 1, r);
    // combine — O(1) or O(n)
}
// T(n) = 2T(n/2) + O(1) → O(n)
// T(n) = 2T(n/2) + O(n) → O(n log n)
```

### Pattern 5: Two Recursive Calls (Exponential)

```java
int exponential(int n) {
    if (n <= 1) return 1;
    return exponential(n - 1) + exponential(n - 2);
}
// T(n) = T(n-1) + T(n-2) + O(1) → O(2ⁿ)
```

### Pattern 6: Include/Exclude

```java
void includeExclude(int[] arr, int i, List<Integer> curr, List<List<Integer>> result) {
    if (i == arr.length) {
        result.add(new ArrayList<>(curr));
        return;
    }
    // Exclude
    includeExclude(arr, i + 1, curr, result);
    // Include
    curr.add(arr[i]);
    includeExclude(arr, i + 1, curr, result);
    curr.remove(curr.size() - 1);
}
// T(n) = 2T(n-1) + O(1) → O(2ⁿ)
```

### Pattern 7: For Loop Recursion

```java
void forLoopRecursion(int[] nums, List<Integer> curr, List<List<Integer>> result) {
    if (isValid(curr)) {
        result.add(new ArrayList<>(curr));
    }
    for (int i = start; i < nums.length; i++) {
        curr.add(nums[i]);
        forLoopRecursion(nums, i + 1, curr, result);
        curr.remove(curr.size() - 1);
    }
}
// Used in combinations, permutations, subsets
// T(n) = n × T(n-1) approximately → O(n!) for permutations
```

### Pattern 8: Multiple Branches

```java
void multipleBranches(int n, String path, List<String> paths) {
    if (n == 0) {
        paths.add(path);
        return;
    }
    // Try all possible choices
    for (Choice choice : getChoices()) {
        multipleBranches(n - 1, path + choice, paths);
    }
}
// T(n) = k × T(n-1) where k = number of choices → O(kⁿ)
```

### Pattern 9: Accumulator / Tail Recursion Helper

```java
int factorialHelper(int n, int acc) {
    if (n <= 1) return acc;
    return factorialHelper(n - 1, n * acc);
}
// Still O(n) stack in Java (no TCO), but pattern is useful for some problems
```

### Pattern 10: Nested Recursion (Rare)

```java
int nested(int n) {
    if (n > 100) return n - 10;
    return nested(nested(n + 11));
}
// Ackermann function style — unusual, but appears in some theory problems
```

---

## 7. Pattern Recognition Guide

| Problem | Pattern | Complexity |
|---------|---------|------------|
| Factorial, Sum, Linear search | Decrease & Conquer (T(n-1)) | O(n) |
| Binary search | Divide & Conquer (T(n/2)) | O(log n) |
| Find max, Tree traversal | Divide & Conquer (2T(n/2)) | O(n) |
| Merge sort, Quick sort | Divide & Conquer with merge | O(n log n) |
| Fibonacci, Staircase | Multiple calls | O(2ⁿ) |
| Subset generation | Include/Exclude | O(2ⁿ) |
| Permutations | For-loop recursion | O(n!) |
| Combination generation | For-loop with start index | O(C(n,k)) |
| Maze paths | Multiple branches | O(branches^depth) |
| N-Queens | For-loop + isSafe | O(n!) |

**The insight:** Most recursive problems follow one of these patterns. Identify the pattern → write the template → adapt to problem specifics.

---

## Pattern Reference

```
Decrease & Conquer  →  T(n) = a·T(n-b) + f(n)       → linear or exponential
Divide & Conquer    →  T(n) = a·T(n/b) + f(n)       → log, n, or n log n
Multiple Branches   →  T(n) = k·T(n-1)              → exponential (O(kⁿ))
Include/Exclude     →  T(n) = 2·T(n-1)              → exponential (O(2ⁿ))
For-Loop Recursion  →  T(n) = n·T(n-1)              → factorial (O(n!))
```

Recognize the pattern, apply the template, solve the problem.
