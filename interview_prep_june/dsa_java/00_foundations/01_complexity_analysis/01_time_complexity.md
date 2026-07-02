# 01 — Time Complexity Analysis

Knowing Big-O theory is one thing; analyzing actual code is another. Let's build the skill of looking at code and determining its complexity — from simple loops to recursive functions.

---

## 1. Analyzing Loops

### Single Loop — O(n)

```java
for (int i = 0; i < n; i++) {
    System.out.println(arr[i]);  // O(1) operation
}
// Total: n × O(1) = O(n)
```

**Counterintuitive case — it's still O(n):**

```java
for (int i = 0; i < n; i++) {
    for (int j = 0; j < 100; j++) {  // 100 is constant!
        System.out.println(arr[i]);  // O(1)
    }
}
// Total: n × 100 = O(100n) → O(n)
// Constants don't matter!
```

### Nested Loops — O(n²) to O(n³)

```java
// Standard double nested: O(n²)
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
        // O(1) operation
    }
}
// Total: n × n = O(n²)

// Triple nested: O(n³)
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
        for (int k = 0; k < n; k++) {
            // O(1) operation
        }
    }
}
// Total: n × n × n = O(n³)
```

### Nested Loop with Variable Inner Range

```java
// Inner loop shrinks: still O(n²)
for (int i = 0; i < n; i++) {
    for (int j = i + 1; j < n; j++) {
        // O(1) operation
    }
}
// Operations: (n-1) + (n-2) + ... + 1 = n(n-1)/2 = O(n²)

// Inner loop grows: also O(n²)
for (int i = 0; i < n; i++) {
    for (int j = 0; j < i; j++) {
        // O(1) operation
    }
}
// Operations: 0 + 1 + 2 + ... + (n-1) = n(n-1)/2 = O(n²)
```

### Consecutive Loops — Add, Not Multiply

```java
for (int i = 0; i < n; i++) { ... }   // O(n)
for (int i = 0; i < n; i++) { ... }   // O(n)
for (int i = 0; i < n; i++) { ... }   // O(n)

// Total: O(n) + O(n) + O(n) = O(3n) = O(n)
// Add them! They run sequentially.

// Compare with nested:
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) { ... }  // O(n²)
}
```

---

## 2. Loop with Half Increments — O(log n)

```java
// i doubles/halves each iteration → O(log n)
for (int i = 1; i < n; i *= 2) {
    System.out.println(i);
}
// n = 16: i = 1, 2, 4, 8 → 4 iterations = log₂(16)

// Same thing, different direction
for (int i = n; i > 0; i /= 2) {
    System.out.println(i);
}
// n = 16: i = 16, 8, 4, 2, 1 → 5 iterations ≈ log₂(16)

// Variable doubling — O(log n) base depends on factor
for (int i = 1; i < n; i *= 3) { ... }  // O(log₃ n) = O(log n)
// Base doesn't matter asymptotically: log₃ n = log₂ n / log₂ 3 → still O(log n)
```

### Tricky: Loop with Half + Linear Inside

```java
for (int i = 1; i < n; i *= 2) {    // O(log n) iterations
    for (int j = 0; j < n; j++) {   // O(n) per iteration
        // O(1) operation
    }
}
// Total: O(log n) × O(n) = O(n log n)

for (int i = n; i > 0; i /= 2) {
    for (int j = 0; j < i; j++) {   // j goes up to i, not n!
        // O(1) operation
    }
}
// i: n, n/2, n/4, ..., 1
// Operations: n + n/2 + n/4 + ... + 1 = 2n = O(n)
```

---

## 3. Loop with sqrt — O(√n)

```java
// Condition: i*i < n → i < √n
for (int i = 0; i * i < n; i++) {
    System.out.println(i);
}
// n = 100: i = 0,1,2,3,4,5,6,7,8,9 → 10 iterations = √100

// Classic prime check
boolean isPrime(int n) {
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}  // O(√n)
```

---

## 4. Analyzing Recursive Complexity

### Linear Recursion: T(n) = T(n-1) + O(1) → O(n)

```java
int factorial(int n) {
    if (n <= 1) return 1;              // O(1)
    return n * factorial(n - 1);       // T(n-1) + O(1)
}
// T(n) = T(n-1) + 1
// T(n) = T(n-2) + 2
// ...
// T(n) = T(0) + n
// T(n) = O(n)

// Tree recursion: T(n) = T(n-1) + T(n-2) + O(1) → O(2ⁿ)
int fib(int n) {
    if (n <= 1) return n;              // O(1)
    return fib(n - 1) + fib(n - 2);    // T(n-1) + T(n-2)
}
// Binary tree of calls → roughly 2ⁿ nodes
// T(n) = O(2ⁿ) — exponential!
```

### Divide and Conquer: T(n) = 2T(n/2) + O(n) → O(n log n)

```java
void mergeSort(int[] arr, int l, int r) {
    if (l >= r) return;                 // O(1)
    int mid = l + (r - l) / 2;          // O(1)
    mergeSort(arr, l, mid);             // T(n/2)
    mergeSort(arr, mid + 1, r);         // T(n/2)
    merge(arr, l, mid, r);              // O(n)
}
// T(n) = 2T(n/2) + O(n)
// Using Master Theorem or recursion tree:
// Level 0: n work, Level 1: 2 × n/2 = n, Level 2: 4 × n/4 = n
// log n levels × n work per level = O(n log n)
```

### Binary Search: T(n) = T(n/2) + O(1) → O(log n)

```java
int binarySearch(int[] arr, int target, int l, int r) {
    if (l > r) return -1;               // O(1)
    int mid = l + (r - l) / 2;          // O(1)
    if (arr[mid] == target) return mid; // O(1)
    if (arr[mid] < target)
        return binarySearch(arr, target, mid + 1, r);  // T(n/2)
    else
        return binarySearch(arr, target, l, mid - 1);  // T(n/2)
}
// T(n) = T(n/2) + O(1)
// Recursion tree: each level does O(1) work, log n levels
// T(n) = O(log n)
```

---

## 5. Master Theorem — Quick Reference

For recurrences of the form: **T(n) = a·T(n/b) + O(nᵈ)**

| Condition | Result | Examples |
|-----------|--------|----------|
| a < bᵈ | O(nᵈ) | T(n) = 2T(n/4) + O(n): 2 < 4¹ → O(n) |
| a = bᵈ | O(nᵈ log n) | T(n) = 2T(n/2) + O(n): 2 = 2¹ → O(n log n) |
| a > bᵈ | O(n^(log_b a)) | T(n) = 4T(n/2) + O(n): 4 > 2¹ → O(n²) |

Wait — detailed coverage in the Master Theorem file. For now, just know it exists.

---

## 6. Complexity of Common Java Operations

### HashMap / HashSet (average)

```java
put(key, value);        // O(1)
get(key);               // O(1)
containsKey(key);       // O(1)
containsValue(value);   // O(n) — iterates over all entries!
remove(key);            // O(1)
```

### ArrayList

```java
get(index);             // O(1)
set(index, value);      // O(1)
add(value);             // O(1) amortized
add(index, value);      // O(n) — shifts elements
remove(index);          // O(n) — shifts elements
remove(value);          // O(n) — linear search + shift
contains(value);        // O(n) — linear search
indexOf(value);         // O(n) — linear search
```

### TreeMap / TreeSet

```java
put(key, value);        // O(log n)
get(key);               // O(log n)
containsKey(key);       // O(log n)
containsValue(value);   // O(n)
firstKey();             // O(log n) — leftmost node
```

### PriorityQueue (Heap)

```java
offer(value);           // O(log n)
poll();                 // O(log n)
peek();                 // O(1)
remove(value);          // O(n) — linear search then O(log n) heapify
```

### Arrays.sort / Collections.sort

```java
Arrays.sort(int[]);      // Dual-Pivot Quicksort: O(n log n) avg, O(n²) worst
Collections.sort(list);  // TimSort: O(n log n), O(n) on nearly sorted data
Arrays.sort(Object[]);   // TimSort: O(n log n)
```

### String Operations

```java
s.charAt(i);            // O(1) — array access
s.length();             // O(1)
s.substring(i, j);      // O(j-i) — creates copy (Java 7+)
s.equals(t);            // O(n) — character comparison
s.contains(t);          // O(n·m) worst case — but optimized
s.indexOf(t);           // O(n·m) worst case
s.split(regex);         // O(n) — iterates and builds array
```

---

## 7. Worst-Case vs Average-Case vs Best-Case

```java
// Quick sort
// Best: O(n log n) — pivot always splits evenly
// Average: O(n log n)
// Worst: O(n²) — pivot is always min/max (sorted array, bad pivot choice)

// Insertion sort
// Best: O(n) — already sorted (one comparison per element)
// Average: O(n²)
// Worst: O(n²) — reverse sorted

// HashMap get
// Best: O(1) — no collisions, direct bucket hit
// Average: O(1) — good hash distribution
// Worst: O(n) — all keys in same bucket (hash collision attack)

// Binary search
// Best: O(1) — mid element is target
// Average: O(log n)
// Worst: O(log n) — target not present
```

**Why average-case matters:** Quick sort's O(n²) worst case is extremely rare (probability ~2/n!) because robust implementations pick random or median-of-three pivots.

---

## 8. 15 Code Snippets — Analyze These

### Snippet 1
```java
for (int i = 0; i < n; i += 2) {
    System.out.println(arr[i]);
}
```
**Answer:** O(n) — i += 2 halves the constant factor but constants don't matter.

### Snippet 2
```java
for (int i = 0; i < n; i++) {
    for (int j = 0; j < 1000; j++) {
        System.out.println(i * j);
    }
}
```
**Answer:** O(n) — inner loop is constant (1000 iterations).

### Snippet 3
```java
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j += 2) {
        System.out.println(i + j);
    }
}
```
**Answer:** O(n²) — n × n/2 = O(n²).

### Snippet 4
```java
for (int i = 0; i < n; i++) {
    for (int j = i; j < n; j++) {
        for (int k = 0; k < 10; k++) {
            System.out.println(i + j + k);
        }
    }
}
```
**Answer:** O(n²) — nested i/j loops give n(n+1)/2 ≈ O(n²). The k loop is constant.

### Snippet 5
```java
for (int i = 0; i < n; i++) {
    for (int j = 0; j * j < n; j++) {
        System.out.println(i * j);
    }
}
```
**Answer:** O(n√n) — outer loop O(n), inner loop O(√n).

### Snippet 6
```java
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
        for (int k = 0; k < n; k++) {
            // O(1) operation
        }
    }
}
```
**Answer:** O(n³) — triple nested loops each going to n.

### Snippet 7
```java
int i = 1;
while (i < n) {
    for (int j = 0; j < n; j++) {
        System.out.println(i + j);
    }
    i *= 2;
}
```
**Answer:** O(n log n) — outer while is O(log n), inner for is O(n).

### Snippet 8
```java
int i = n;
while (i > 0) {
    int j = 0;
    while (j < i) {
        System.out.println(i + j);
        j++;
    }
    i /= 2;
}
```
**Answer:** O(n) — n + n/2 + n/4 + ... + 1 = 2n.

### Snippet 9
```java
int sum = 0;
for (int i = 0; i < n; i++) {
    sum += arr[i];                 // O(n)
}
Arrays.sort(arr);                   // O(n log n)
for (int i = 0; i < n; i++) {
    sum += arr[i];                 // O(n)
}
```
**Answer:** O(n log n) — dominated by the sort. The two O(n) passes are smaller.

### Snippet 10
```java
for (int i = 0; i < n; i++) {
    for (int j = 0; j < i; j++) {
        for (int k = 0; k < j; k++) {
            System.out.println(i + j + k);
        }
    }
}
```
**Answer:** O(n³) — sum of sum of sum. Approximately n³/6.

### Snippet 11 (Recursive)
```java
int f(int n) {
    if (n <= 1) return 1;
    return f(n - 1) + f(n - 1);
}
```
**Answer:** O(2ⁿ) — each call creates two more calls. Binary tree of height n.

### Snippet 12 (Recursive)
```java
int f(int n) {
    if (n <= 1) return 1;
    return f(n - 1) + f(n - 2);
}
```
**Answer:** O(2ⁿ) — Fibonacci recurrence. Approximately 1.618ⁿ (golden ratio).

### Snippet 13 (Recursive)
```java
int f(int n) {
    if (n <= 1) return 1;
    return f(n / 2) + 1;
}
```
**Answer:** O(log n) — each call halves the input. One call per level.

### Snippet 14 (Recursive)
```java
int f(int n) {
    if (n <= 1) return 1;
    return 2 * f(n / 2) + n;
}
```
**Answer:** O(n log n) — Master Theorem: T(n) = 2T(n/2) + n. a=2, b=2, d=1 → a = bᵈ → O(n log n).

### Snippet 15
```java
HashMap<Integer, Integer> map = new HashMap<>();
for (int i = 0; i < n; i++) {
    map.put(arr[i], map.getOrDefault(arr[i], 0) + 1);
}
for (int key : map.keySet()) {
    System.out.println(key + ": " + map.get(key));
}
```
**Answer:** O(n) — first loop: n O(1) puts = O(n). Second loop: iterates over unique keys (≤ n). Total: O(n).

---

## Time Complexity Cheat Sheet

```
Single loop                    → O(n)
Nested loops both to n        → O(n²)
Three nested loops to n       → O(n³)
Loop variable halves each time → O(log n)
Loop variable doubles         → O(log n)
Loop √n iterations            → O(√n)
Consecutive loops             → ADD complexities
Nested loops                  → MULTIPLY complexities
Linear recursion T(n-1)+O(1)  → O(n)
Binary recursion T(n-1)+T(...) → O(2ⁿ)
Divide & conquer T(n/2)+O(1)  → O(log n)
Divide & conquer 2T(n/2)+O(n) → O(n log n)
HashMap average operations    → O(1)
```

Practice analyzing every piece of code you write. After a few weeks, it becomes second nature.
