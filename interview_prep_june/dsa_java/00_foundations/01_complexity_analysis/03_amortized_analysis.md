# 03 — Amortized Analysis

Amortized analysis is one of those concepts that sounds intimidating but is actually quite intuitive. It's about understanding the **average cost per operation** over a sequence of operations, even if individual operations are sometimes expensive.

---

## 1. Amortized vs Average-Case — The Key Difference

**Average-case analysis:** Considers the probability distribution of inputs. "On average, what's the runtime?"

**Amortized analysis:** Considers a **worst-case sequence** of operations and spreads the cost of rare expensive operations over all operations. "If I do N operations, what's the average cost per operation in the worst case?"

```
Average-case: What's typical?
Amortized:    What's the average over a worst-case sequence?
```

Amortized is stronger — it guarantees the average per operation in **any** sequence.

---

## 2. Dynamic Array (ArrayList) Growth

### The Problem

`ArrayList` wraps an internal array. When it's full and you add another element, it:
1. Creates a new array ~1.5× larger
2. Copies all elements from old array to new array
3. Replaces the old array reference

Step 2 costs O(n). So `add()` is sometimes O(1) (when there's space) and sometimes O(n) (when resizing).

**Is adding N elements O(n) or O(n²)?**

### The Analysis

```java
// Suppose we start with capacity = 1, growth factor = 2
// Adding n elements:

// Add 1st element: no resize → O(1)
// Add 2nd element: resize (1→2) → copy 1 element → O(1)
// Add 3rd element: resize (2→4) → copy 2 elements → O(2)
// Add 5th element: resize (4→8) → copy 4 elements → O(4)
// Add 9th element: resize (8→16) → copy 8 elements → O(8)
// ...

// Count total copies:
// 1 + 2 + 4 + 8 + ... + n/2 + n (if n is power of 2)
// = n + n/2 + n/4 + ... + 2 + 1
// = 2n - 1

// Total cost for n additions = n (ordinary adds) + (2n - 1) (copies) = 3n - 1
// Per operation: (3n - 1) / n ≈ 3 = O(1) amortized!
```

**So even though some individual adds cost O(n), the average over n adds is O(1).**

### Java's Actual Growth Factor

```java
// Java 8+: newCapacity = oldCapacity + (oldCapacity >> 1) = 1.5× growth
// This is more memory-efficient than doubling but still O(1) amortized

// To verify:
ArrayList<Integer> list = new ArrayList<>();  // initial capacity = 10
long start = System.nanoTime();
for (int i = 0; i < 1_000_000; i++) {
    list.add(i);
}
long end = System.nanoTime();
System.out.println((end - start) / 1_000_000 + " ms");
// Still fast — O(1) amortized per add
```

### Why Not Always Pre-allocate?

```java
// If you know the size, pre-allocation avoids resizing entirely:
ArrayList<Integer> list = new ArrayList<>(1_000_000);  // no resizing needed
for (int i = 0; i < 1_000_000; i++) {
    list.add(i);  // all O(1), no copies
}
```

---

## 3. HashMap Resizing

### How HashMap Grows

```java
HashMap<String, Integer> map = new HashMap<>();  // default: capacity=16, loadFactor=0.75

// Threshold = capacity × loadFactor = 16 × 0.75 = 12
// When size reaches 13, HashMap resizes to 2× capacity = 32 (power of 2)

// Resizing involves:
// 1. Create new array of size 32
// 2. Rehash ALL existing entries (recalculate bucket index)
// 3. Insert into new buckets
```

### Amortized Analysis

Same reasoning as ArrayList — resizing is O(n) but happens rarely.

```java
// Cost of n inserts starting from empty HashMap:
// Ordinary inserts: n × O(1) = O(n)
// Resize cost: total copies across all resizes = O(n)
// (Geometric series: 16 + 32 + 64 + ... + n/2 = O(n))
// Total: O(n)
// Amortized per insert: O(1)
```

### The Load Factor Tradeoff

```java
// loadFactor = 0.75 (default, recommended)
// Lower: 0.5 → more memory, fewer collisions, less resize cost
// Higher: 0.9 → less memory, more collisions, more resize cost (but happens later)

// Why 0.75? The Java team chose it as a compromise between time and space.
// It's based on the Poisson distribution — probability of collisions is acceptably low.

HashMap<String, Integer> map = new HashMap<>(1024, 0.5f);   // space-heavy, fast
HashMap<String, Integer> map = new HashMap<>(1024, 0.9f);   // space-light, slower lookups
```

---

## 4. Binary Counter Increment

### The Problem

Consider incrementing a binary counter from 0 to n:

```
0000 → 0001 (1 bit flip)
0001 → 0010 (2 bit flips)
0010 → 0011 (1 bit flip)
0011 → 0100 (3 bit flips)
0100 → 0101 (1 bit flip)
0101 → 0110 (2 bit flips)
0110 → 0111 (1 bit flip)
0111 → 1000 (4 bit flips)
```

```java
void increment(int[] bits) {
    int i = 0;
    while (i < bits.length && bits[i] == 1) {
        bits[i] = 0;  // flip
        i++;
    }
    if (i < bits.length) {
        bits[i] = 1;  // flip
    }
}
```

### The Analysis

**Naive view:** Each increment might flip up to k bits (where k = number of bits). So n increments = O(n·k) = O(n log n).

**Amortized view:** Count total flips across all increments:
- The rightmost bit flips every time: n flips
- The second bit flips every other time: n/2 flips
- The third bit flips every 4th time: n/4 flips
- The j-th bit flips every 2ʲ-th time: n/2ʲ flips

```java
// Total flips = n + n/2 + n/4 + n/8 + ... + 1
//            = n × (1 + 1/2 + 1/4 + 1/8 + ...)
//            = n × 2
//            = 2n
// Amortized per increment: 2n / n = 2 = O(1)!
```

**Counterintuitive:** Even though any single increment can flip O(log n) bits, n increments cost O(n) total, not O(n log n).

---

## 5. When Amortized Analysis Matters in Interviews

### Resizing Data Structures

When working with dynamic arrays, hash tables, or any structure that grows:

```java
// ❌ Unnecessarily pessimistic analysis:
// "Adding n elements to an ArrayList is O(n²) because resizing copies elements."
// This is WRONG — it's O(n) amortized.

// ✅ Correct:
// "Adding n elements to an ArrayList is O(n) amortized.
//  Each add is O(1) average due to geometric growth."
```

### StringBuilder Capacity

```java
// Appending n characters to StringBuilder:
// Default capacity = 16
// Growth: (oldCapacity + 1) × 2 (Java 8: oldCapacity × 2 + 2)
// Same geometric growth → O(n) amortized for n appends

// But if you pre-size: O(n) deterministic (no resizing)
StringBuilder sb = new StringBuilder(n);  // can hold n chars without resizing
```

### PriorityQueue Building

```java
// Building a heap from n elements:
// Method 1: Add one by one — O(n log n) worst case
PriorityQueue<Integer> pq = new PriorityQueue<>();
for (int x : arr) pq.offer(x);  // n × O(log n) = O(n log n)

// Method 2: heapify — O(n) using Floyd's algorithm
PriorityQueue<Integer> pq = new PriorityQueue<>(arr);
// No amortization here — the O(n) bound is a mathematical fact
```

### Resizing in Concurrent Contexts

```java
// HashMap in a single thread: O(1) amortized resizing
// HashMap in multiple threads with ConcurrentHashMap:
// Resizing is more expensive (needs synchronization)
// But still O(1) amortized in practice
```

---

## 6. Formal Methods of Amortized Analysis

You don't need these for interviews, but knowing they exist helps:

### Aggregate Method
Sum up the cost of all operations, divide by the number of operations.

### Accounting (Banker's) Method
Each "cheap" operation prepays for future "expensive" operations. Each operation deposits "coins"; expensive operations withdraw them.

### Potential (Physicist's) Method
Define a **potential function** Φ that represents the "prepaid work." Amortized cost = actual cost + ΔΦ.

```
Example for dynamic array:
Φ = 2 × size - capacity (when size ≥ capacity/2)
- After a cheap add: ΔΦ = 2 × 1 = 2 → amortized cost = 1 + 2 = 3
- After an expensive add (resize): ΔΦ = -(capacity + 2) → amortized cost = (capacity + 2) - (capacity + 2) = 0
Every operation has amortized cost ≤ 3 = O(1)
```

---

## 7. Common Misconceptions

```java
// ❌ "ArrayList.get() is O(1) amortized"
// → It's just O(1). There's no "amortized" because it's never expensive.
// Amortized only applies when some operations are occasionally expensive.

// ❌ "HashMap put is O(1) always"
// → Average O(1). Worst case O(n) with bad hashing. Amortized O(1) considering resizing.

// ❌ "Amortized means average case"
// → No. Amortized is worst-case sequence averaged over operations.
// Average case considers probability of inputs.
```

---

## Amortized Analysis Cheat Sheet

```
Dynamic array (ArrayList) add   → O(1) amortized
HashMap put                     → O(1) amortized
Binary counter increment        → O(1) amortized
StringBuilder append            → O(1) amortized

Growth factor > 1               → O(1) amortized
Growth factor = 1 (linear)      → O(n) amortized (bad!)

Key insight: Any data structure that doubles (or 1.5×)
when full gives O(1) amortized operations.
```

**Interview tip:** If a problem involves dynamic resizing, mention "amortized O(1)" — it shows depth of understanding.
