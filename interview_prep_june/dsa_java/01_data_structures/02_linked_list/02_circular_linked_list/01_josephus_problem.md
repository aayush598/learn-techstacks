# Josephus Problem — Circular Linked List

The Josephus Problem is a classic application of circular linked lists. It's also a great example of how a problem can be solved with simulation, recursion, and iteration.

---

## Problem Statement

**n** people stand in a circle. Starting from a designated position, every **k-th** person is eliminated. The process repeats until only one person remains. Find the position of the survivor.

**Example:** n=7, k=3
- People: `1, 2, 3, 4, 5, 6, 7` in a circle
- Elimination order: 3, 6, 2, 7, 5, 1 → **survivor is 4**

---

## Approach 1: Simulation with Circular Linked List

The most intuitive approach — literally simulate the elimination process.

```java
public static int josephusSimulation(int n, int k) {
    // Create circular linked list with n people
    Node tail = null;
    for (int i = 1; i <= n; i++) {
        Node newNode = new Node(i);
        if (tail == null) {
            newNode.next = newNode;
            tail = newNode;
        } else {
            newNode.next = tail.next;
            tail.next = newNode;
            tail = newNode;
        }
    }

    // Simulate elimination
    Node current = tail; // start from the node before head

    while (current.next != current) { // while more than 1 person
        // Move k-1 steps (we're already at the previous position)
        for (int i = 1; i < k; i++) {
            current = current.next;
        }

        // Eliminate the next person
        Node eliminated = current.next;
        current.next = eliminated.next;
        // eliminated is now orphaned → garbage collected

        System.out.println("Eliminated: " + eliminated.data);
    }

    return current.data; // survivor
}
```

### Walkthrough: n=7, k=3

**Initial circle:** `1 → 2 → 3 → 4 → 5 → 6 → 7 → 1`

| Round | Move k-1=2 steps | Eliminate | Circle after |
|-------|-------------------|-----------|-------------|
| 1 | from 7: →1→2 | 3 | 1→2→4→5→6→7 |
| 2 | from 2: →4→5 | 6 | 1→2→4→5→7 |
| 3 | from 5: →7→1 | 2 | 1→4→5→7 |
| 4 | from 1: →4→5 | 7 | 1→4→5 |
| 5 | from 4: →1→4 | 5 | 1→4 |
| 6 | from 4: →1→4 | 1 | 4 |

**Survivor: 4** ✓

### Why does `current` start at `tail`?

We start one step before the head so that when we move `k-1` steps, the k-th person is `current.next`. This makes the elimination logic cleaner.

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n * k) |
| Space  | O(n) |

---

## Approach 2: Recursion

The recursive formula for the Josephus problem:

```
J(1, k) = 0                          (base case: 1 person, index 0 survives)
J(n, k) = (J(n-1, k) + k) % n       (recursive case)
```

**Note:** This uses 0-indexed positions. Add 1 to get the actual person number.

```java
public static int josephusRecursive(int n, int k) {
    if (n == 1) return 0; // base case: only one person, at index 0

    return (josephusRecursive(n - 1, k) + k) % n;
}

// Wrapper to return 1-indexed result
public static int josephusRecursiveOneIndexed(int n, int k) {
    return josephusRecursive(n, k) + 1;
}
```

### Why Does This Formula Work?

**Think of it as a mapping:**

1. We have n people in a circle. The k-th person (index `(k-1) % n`) is eliminated.
2. After elimination, we have n-1 people in a circle, starting from the person AFTER the eliminated one.
3. In the smaller circle of n-1 people, the survivor is at position `J(n-1, k)` (0-indexed).
4. We need to map that position back to the original circle:
   - The starting point in the smaller circle is offset by `k` from the eliminated person
   - So the survivor's position in the original circle is `(J(n-1, k) + k) % n`

### Walkthrough: n=7, k=3

| n | J(n, 3) | Calculation |
|---|---------|-------------|
| 1 | 0 | base case |
| 2 | (0 + 3) % 2 = 1 | |
| 3 | (1 + 3) % 3 = 1 | |
| 4 | (1 + 3) % 4 = 0 | |
| 5 | (0 + 3) % 5 = 3 | |
| 6 | (3 + 3) % 6 = 0 | |
| 7 | (0 + 3) % 7 = 3 | |

J(7, 3) = 3 (0-indexed) → person **4** (1-indexed) ✓

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(n)  | (recursion stack) |

---

## Approach 3: Iterative

Same formula, no recursion overhead.

```java
public static int josephusIterative(int n, int k) {
    int result = 0; // J(1, k) = 0

    for (int i = 2; i <= n; i++) {
        result = (result + k) % i;
    }

    return result + 1; // convert to 1-indexed
}
```

### Walkthrough: n=7, k=3

| i | result (before) | (result + k) | % i | result (after) |
|---|-----------------|-------------|-----|----------------|
| 2 | 0 | 3 | 1 | 1 |
| 3 | 1 | 4 | 1 | 1 |
| 4 | 1 | 4 | 0 | 0 |
| 5 | 0 | 3 | 3 | 3 |
| 6 | 3 | 6 | 0 | 0 |
| 7 | 0 | 3 | 3 | 3 |

Result: 3 + 1 = **4** ✓

### Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n)  |
| Space  | O(1)  |

---

## Test Cases

```java
public static void main(String[] args) {
    // Test 1: Simulation
    System.out.println("=== Simulation ===");
    System.out.println("n=7, k=3: " + josephusSimulation(7, 3));   // 4
    System.out.println("n=5, k=2: " + josephusSimulation(5, 2));   // 3
    System.out.println("n=1, k=1: " + josephusSimulation(1, 1));   // 1
    System.out.println("n=6, k=7: " + josephusSimulation(6, 7));   // 4

    // Test 2: Recursion
    System.out.println("\n=== Recursion ===");
    System.out.println("n=7, k=3: " + josephusRecursiveOneIndexed(7, 3));  // 4
    System.out.println("n=5, k=2: " + josephusRecursiveOneIndexed(5, 2));  // 3
    System.out.println("n=1, k=1: " + josephusRecursiveOneIndexed(1, 1));  // 1

    // Test 3: Iteration
    System.out.println("\n=== Iteration ===");
    System.out.println("n=7, k=3: " + josephusIterative(7, 3));  // 4
    System.out.println("n=5, k=2: " + josephusIterative(5, 2));  // 3
    System.out.println("n=1, k=1: " + josephusIterative(1, 1));  // 1

    // Verify all approaches agree
    System.out.println("\n=== Verification ===");
    for (int n = 1; n <= 20; n++) {
        for (int k = 1; k <= 10; k++) {
            int sim = josephusSimulation(n, k);
            int rec = josephusRecursiveOneIndexed(n, k);
            int iter = josephusIterative(n, k);
            if (sim != rec || rec != iter) {
                System.out.println("MISMATCH at n=" + n + " k=" + k
                    + ": sim=" + sim + " rec=" + rec + " iter=" + iter);
            }
        }
    }
    System.out.println("All tests passed!");
}
```

**Sample output from simulation:**
```
=== Simulation ===
Eliminated: 3
Eliminated: 6
Eliminated: 2
Eliminated: 7
Eliminated: 5
Eliminated: 1
n=7, k=3: 4
```

---

## Comparison of All Three Approaches

| Approach | Time | Space | Pros | Cons |
|----------|------|-------|------|------|
| Circular LL Simulation | O(n·k) | O(n) | Easy to understand, shows elimination order | Slow for large n or k |
| Recursion | O(n) | O(n) | Elegant one-liner | Stack overflow for huge n |
| Iteration | O(n) | O(1) | Fast, no extra space | Less intuitive |

---

## Variant: Find Elimination Order

If you need to know the ORDER in which people are eliminated (not just the survivor), use the simulation approach:

```java
public static List<Integer> josephusOrder(int n, int k) {
    List<Integer> order = new ArrayList<>();

    // Build circular linked list
    Node tail = null;
    for (int i = 1; i <= n; i++) {
        Node newNode = new Node(i);
        if (tail == null) {
            newNode.next = newNode;
            tail = newNode;
        } else {
            newNode.next = tail.next;
            tail.next = newNode;
            tail = newNode;
        }
    }

    Node current = tail;
    while (current.next != current) {
        for (int i = 1; i < k; i++) {
            current = current.next;
        }
        Node eliminated = current.next;
        order.add(eliminated.data);
        current.next = eliminated.next;
    }

    order.add(current.data); // survivor is last
    return order;
}

// Usage:
System.out.println(josephusOrder(7, 3)); // [3, 6, 2, 7, 5, 1, 4]
```

---

## When to Use Each Approach

| Scenario | Best Approach |
|----------|--------------|
| Just need the survivor | Iteration (O(n) time, O(1) space) |
| Need elimination order | Simulation with circular LL |
| n is very large, k is small | Iteration |
| Interview question, explain logic | Show simulation first, then optimize to formula |
| Need to prove correctness | Recursion (mathematical proof) |
