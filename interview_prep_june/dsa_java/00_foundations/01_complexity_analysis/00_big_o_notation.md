# 00 — Big-O Notation

Big-O is the language we use to express how efficient an algorithm is. If you can't analyze complexity, you can't evaluate whether your solution is good enough. Let's build intuition first, then dive into details.

---

## 1. What is Asymptotic Analysis?

**The core idea:** How does the runtime (or memory) of an algorithm grow as the input size grows?

We don't care about exact time (milliseconds). We care about **growth rate** — how the algorithm scales.

**Example:** Your laptop runs insertion sort on 1000 elements in 0.01 seconds. Sorting 1 million elements:
- If it's insertion sort (O(n²)): ~10,000 seconds (~3 hours) — unusable
- If it's merge sort (O(n log n)): ~0.02 seconds — instant

Same machine. Same input size. Different algorithms. Dramatically different outcomes.

---

## 2. The Three Asymptotic Notations

### Big-O (O) — Upper Bound (Worst Case)

```
O(g(n)) = { f(n) | there exist c > 0, n₀ > 0 such that
           0 ≤ f(n) ≤ c·g(n) for all n ≥ n₀ }
```

**Plain English:** "The algorithm takes at most this long." This is what we use 99% of the time in interviews and DSA.

### Omega (Ω) — Lower Bound (Best Case)

```
Ω(g(n)) = { f(n) | there exist c > 0, n₀ > 0 such that
           0 ≤ c·g(n) ≤ f(n) for all n ≥ n₀ }
```

**Plain English:** "The algorithm takes at least this long." Less commonly used.

### Theta (Θ) — Tight Bound (Average Case)

```
Θ(g(n)) = O(g(n)) ∩ Ω(g(n))
```

**Plain English:** "The algorithm grows exactly like this." Used when worst = best = average (e.g., array access).

### Visualizing the Relationship

```
     c₂·g(n)
        /\
       /  \
f(n)  /    \
     /      \
    /        \
   / c₁·g(n)  \
  /____________\

O: f(n) ≤ c₂·g(n) — above is bound
Ω: f(n) ≥ c₁·g(n) — below is bound
Θ: c₁·g(n) ≤ f(n) ≤ c₂·g(n) — sandwiched
```

**In practice:** You'll say "it's O(n²)" even when it's technically Θ(n²). Everyone does this. It's fine.

---

## 3. Why We Drop Constants and Lower-Order Terms

### The "Drop Constants" Rule

```java
// Both are O(n):
for (int i = 0; i < n; i++) { ... }           // n operations
for (int i = 0; i < n; i++) { ... ; ... }     // 2n operations — still O(n)
for (int i = 0; i < n; i += 2) { ... }        // n/2 operations — still O(n)
```

Why? Because constants don't matter as n → ∞:
- 0.0001 × n vs 1000 × n — for n = 10⁹, both are dwarfed by n²
- What matters is the **shape** of the curve

### The "Drop Lower Terms" Rule

```java
// O(n² + n + 1) → O(n²)
// When n = 1000: n² = 1,000,000, n = 1000, 1 = 1
// The n² term dominates completely
```

**Think of it like this:** When comparing algorithms, you're asking "what happens when n is really big?" Not "what happens when n is 10?"

---

## 4. Common Complexity Classes — With Visual Intuition

### O(1) — Constant Time

**Doesn't depend on input size.** No matter if input has 10 or 10 million elements — same number of operations.

```java
// Array access
int x = arr[5];

// HashMap operations (average)
map.get(key);
map.put(key, value);

// Basic math
int max = Math.max(a, b);

// Queue peek
queue.peek();
```

**Growth:** Horizontal line. Flat.

```
Time
 ^
 |            _________
 |     _______/
 |
 +---------------------→ n
```

### O(log n) — Logarithmic Time

**Each operation cuts the problem size in half.** You can handle enormous inputs with very few operations.

```java
// Binary search
int low = 0, high = n - 1;
while (low <= high) {
    int mid = low + (high - low) / 2;
    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) low = mid + 1;
    else high = mid - 1;
}

// Balanced BST operations
TreeMap.get(key);
TreeSet.contains(value);
```

**Intuition:** n = 1,000,000 → ~20 operations (log₂ 1,000,000 ≈ 20). From 10 to 10M elements: only 5 more operations.

```
Time
 ^
 |
 |
 |       __________________
 |      /
 |_____/
 +---------------------→ n
```

### O(n) — Linear Time

**Processing each element once.** Double the input → double the time.

```java
// Single pass
for (int i = 0; i < n; i++) {
    sum += arr[i];
}

// Linear search
for (int i = 0; i < n; i++) {
    if (arr[i] == target) return i;
}
```

**Intuition:** n = 1,000,000 → 1,000,000 operations. Predictable, proportional.

```
Time
 ^
 |        /
 |       /
 |      /
 |     /
 |____/
 +---------------------→ n
```

### O(n log n) — Linearithmic Time

**The sweet spot for sorting.** Better than quadratic, worse than linear.

```java
// Efficient sorts
Arrays.sort(arr);                  // Dual-Pivot Quicksort
Collections.sort(list);            // TimSort (modified merge sort)

// Divide & conquer
Merge sort
Heap sort
```

**Intuition:** n = 1,000,000 → ~20 million operations. Far better than n²'s trillion.

```
Time
 ^
 |          _-~
 |      _-~
 |    /~
 |  /~
 |/~
 +---------------------→ n
```

### O(n²) — Quadratic Time

**Nested loops iterating over the same data.** With n = 10,000, this is already 100 million operations — often too slow.

```java
// Nested loops
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
        // compare/swap
    }
}

// Simple sorting algorithms
Bubble sort, Selection sort, Insertion sort (worst case)

// All pairs
for (int i = 0; i < n; i++) {
    for (int j = i + 1; j < n; j++) {
        // process pair
    }
}  // n*(n-1)/2 = O(n²)
```

**Intuition:** n = 10 → 100 ops (fine). n = 10,000 → 100M ops (slow). n = 1,000,000 → 10¹² ops (forget it).

```
Time
 ^
 |         /|
 |       /  |
 |     /    |
 |   /      |
 | /        |
 +---------------------→ n
```

### O(2ⁿ) — Exponential Time

**Each addition to n doubles the work.** Becomes unusable very quickly.

```java
// Recursive Fibonacci (naive)
int fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}

// Subset generation (naive recursion)
// Tower of Hanoi
```

**Intuition:** n = 20 → ~1 million ops. n = 30 → ~1 billion. n = 50 → forget it.

```
Time
 ^
 |
 |          /
 |        /
 |      /
 |    /
 |  /
 | /
 |/
 +---------------------→ n
```

### O(n!) — Factorial Time

**Generating all permutations.** Basically unusable for n > 12.

```java
// Generating all permutations
void permute(String s, String result) {
    if (s.isEmpty()) { System.out.println(result); return; }
    for (int i = 0; i < s.length(); i++) {
        permute(s.substring(0,i) + s.substring(i+1), result + s.charAt(i));
    }
}
```

**Intuition:** n = 10 → 3.6M ops. n = 12 → 479M ops. n = 15 → 1.3 trillion.

---

## 5. Visual Growth Rate Comparison

```
n          O(1)    O(log n)    O(n)    O(n log n)     O(n²)        O(2ⁿ)
10          1         3         10         33           100         1,024
100         1         7         100        664         10,000       10³⁰
1,000       1         10        1,000      9,966       1,000,000    impossible
10,000      1         13        10,000     132,877     100,000,000  impossible
100,000     1         17        100,000    1,660,964   10¹⁰         impossible
1,000,000   1         20        1,000,000  19,931,568  10¹²         impossible
```

**The cliff:** O(n²) is often borderline at n = 10⁴. O(2ⁿ) dies at n = 30. O(n!) dies at n = 12.

---

## 6. Quick Estimation Rules

1. **Single loop** → O(n)
2. **Two nested loops** → O(n²) (if both iterate over full input)
3. **Three nested loops** → O(n³)
4. **Problem halves each step** → O(log n)
5. **Divide and conquer with linear merge** → O(n log n)
6. **Recursive with two calls** → often O(2ⁿ) (unless memoized)
7. **HashMap/HashSet operations** → O(1) average
8. **TreeMap/TreeSet operations** → O(log n)

---

## 7. Space Complexity — The Same Idea But for Memory

Big-O also applies to **memory usage** (auxiliary space):

```java
// O(1) space
int sum = 0;
for (int x : arr) sum += x;  // only one extra variable

// O(n) space
int[] copy = new int[n];  // copy of same size
System.arraycopy(arr, 0, copy, 0, n);

// O(n²) space
int[][] matrix = new int[n][n];

// O(log n) space (recursion stack)
int binarySearch(...) { /* recursive — log n stack depth */ }
```

---

## 8. Real-World Rules of Thumb

| Complexity | Max n for 1 second (rough) | What you can do |
|-----------|---------------------------|-----------------|
| O(log n) | Any (billions) | Binary search, tree ops |
| O(n) | 10⁸ (100 million) | Single pass |
| O(n log n) | 10⁶ (1 million) | Sorting |
| O(n²) | 10⁴ (10,000) | Nested loops (careful) |
| O(n³) | 500 | Triple nested (rarely ok) |
| O(2ⁿ) | 25-30 | Only with pruning/memoization |
| O(n!) | 11-12 | Only tiny inputs |

**Context matters:** If n is always ≤ 100, O(n³) might be fine. If n can be 10⁵, even O(n²) can be too slow.

---

## Big-O at a Glance

```
Fastest → O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!) ← Slowest
```

When you solve a problem:
1. Brute force first (might be O(n²) or O(2ⁿ))
2. Analyze the constraints (n ≤ 10⁴? 10⁵? 10⁹?)
3. Optimize until complexity matches constraints
4. Use HashMap to trade space for speed (O(n²) → O(n))
5. Use sorting + binary search (O(n²) → O(n log n))
6. Use divide and conquer (O(n²) → O(n log n))

Big-O is your compass. It tells you whether your solution will pass or fail before you even run it.
