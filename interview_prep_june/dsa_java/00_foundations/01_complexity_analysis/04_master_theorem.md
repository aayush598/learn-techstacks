# 04 — Master Theorem

The Master Theorem is a shortcut for analyzing divide-and-conquer recurrences. Instead of expanding the recursion tree every time, you plug numbers into a formula and get the answer.

---

## 1. The Standard Form

The Master Theorem applies to recurrences of the form:

```
T(n) = a · T(n/b) + f(n)
```

Where:
- **a** ≥ 1 = number of subproblems
- **b** > 1 = factor by which input shrinks
- **f(n)** = cost of dividing + combining

### Examples in This Form

```java
// Binary search: T(n) = T(n/2) + O(1)
// a = 1 (one subproblem), b = 2 (half the input), f(n) = O(1)

// Merge sort: T(n) = 2T(n/2) + O(n)
// a = 2 (two subproblems), b = 2, f(n) = O(n)

// Fibonacci (naive): T(n) = T(n-1) + T(n-2) + O(1)
// ❌ Does NOT fit — b is not constant (n-1, n-2)

// Binary tree traversal: T(n) = 2T(n/2) + O(1)
// a = 2, b = 2, f(n) = O(1)
```

---

## 2. The Three Cases — Simplified

We compare f(n) with n^(log_b a):

```
Case 1: f(n) = O(n^(log_b a - ε))     → T(n) = Θ(n^(log_b a))
         The recursion does more work than combining.
         Constraint: f(n) grows polynomially slower.

Case 2: f(n) = Θ(n^(log_b a) · log^k n) → T(n) = Θ(n^(log_b a) · log^(k+1) n)
         The recursion and combining do comparable work.
         Most common case: k = 0 → T(n) = Θ(n^(log_b a) · log n)

Case 3: f(n) = Ω(n^(log_b a + ε))     → T(n) = Θ(f(n))
         The combining step dominates.
         Constraint: a·f(n/b) ≤ c·f(n) for some c < 1 (regularity condition)
```

### Intuitive Way to Think

```
n^(log_b a) = cost of the "leaf level" (base cases)
f(n)        = cost of the "top level" (splitting/merging)

Case 1: Leaves dominate → answer is leaf cost
Case 2: Both matter     → answer is leaf cost × log n
Case 3: Top dominates   → answer is top cost
```

---

## 3. Applying the Theorem — Worked Examples

### Example 1: Binary Search — T(n) = T(n/2) + O(1)

```
a = 1, b = 2
n^(log_b a) = n^(log₂ 1) = n^0 = 1
f(n) = O(1) = Θ(1)

Compare: f(n) = Θ(1) = Θ(n^(log_b a))
→ Case 2 with k = 0
→ T(n) = Θ(n^(log_b a) · log n) = Θ(log n)
```

**Result: O(log n)** ✅

### Example 2: Merge Sort — T(n) = 2T(n/2) + O(n)

```
a = 2, b = 2
n^(log_b a) = n^(log₂ 2) = n^1 = n
f(n) = O(n) = Θ(n)

Compare: f(n) = Θ(n) = Θ(n^(log_b a))
→ Case 2 with k = 0
→ T(n) = Θ(n · log n)
```

**Result: O(n log n)** ✅

### Example 3: Unbalanced Tree — T(n) = T(n/2) + O(1)

```
a = 1, b = 2
n^(log_b a) = n^(log₂ 1) = n^0 = 1
f(n) = O(1)

Compare: f(n) = O(1) = Θ(1) = Θ(n^(log_b a))
→ Case 2, k = 0
→ T(n) = Θ(log n)
```

**Wait — this is the same as binary search?** Yes! Because only one subproblem is solved, and it's half the size. The other half is ignored.

### Example 4: Finding Maximum — T(n) = 2T(n/2) + O(1)

```
a = 2, b = 2
n^(log_b a) = n^(log₂ 2) = n
f(n) = O(1)

Compare: f(n) = O(1) = O(n^(1 - ε)) for ε = 0.5 (e.g.)
→ Case 1 (leaves dominate)
→ T(n) = Θ(n)
```

**Result: O(n)** — Makes sense. You can't find the max without looking at every element.

### Example 5: Strassen's Matrix Multiplication — T(n) = 7T(n/2) + O(n²)

```
a = 7, b = 2
n^(log_b a) = n^(log₂ 7) ≈ n^2.807
f(n) = O(n²)

Compare: n^(log₂ 7) ≈ n^2.807 vs n²
2.807 > 2, so we're in Case 1
→ T(n) = Θ(n^(log₂ 7)) ≈ Θ(n^2.807)
```

**Result: O(n^2.807)** — Better than naive O(n³), worse than O(n²).

### Example 6: Three Subproblems, Half Input — T(n) = 3T(n/2) + O(n)

```
a = 3, b = 2
n^(log_b a) = n^(log₂ 3) ≈ n^1.585
f(n) = O(n) = O(n¹)

Compare: n^1.585 vs n¹ → 1.585 > 1
→ Case 1 (leaves dominate since n^1.585 is polynomially larger than n)
→ T(n) = Θ(n^(log₂ 3)) ≈ Θ(n^1.585)
```

### Example 7: Ternary Search — T(n) = 3T(n/3) + O(1)

```
a = 3, b = 3
n^(log_b a) = n^(log₃ 3) = n^1 = n
f(n) = O(1)

Compare: f(n) = O(1) = O(n^(1 - ε)) for ε = 0.5
→ Case 1
→ T(n) = Θ(n)
```

**Wait — ternary search is O(n)?** Yes, if you search all three subproblems. But real ternary search only does 2 comparisons and discards one part, so it's T(n) = T(n/3) + O(1) = O(log n). The key is **a = 1** (one subproblem), not a = 3.

---

## 4. When the Master Theorem Does NOT Apply

### Case A: Non-Constant Reduction

```java
// Fibonacci (naive): T(n) = T(n-1) + T(n-2) + O(1)
// b is not a constant — input reduces by 1 or 2, not by a factor
// Master Theorem: ❌ Doesn't apply
// Solution: Recursion tree → O(2ⁿ)
```

### Case B: Uneven Subproblem Sizes

```java
// T(n) = T(n/3) + T(2n/3) + O(n)
// Different subproblem sizes — not in standard form
// Master Theorem: ❌ Doesn't apply directly
// Solution: Recursion tree → O(n log n)
```

### Case C: Gap Between Cases

```java
// T(n) = 2T(n/2) + O(n / log n)
// f(n) = n/log n is not O(n^(1-ε)) and not Θ(n) and not Ω(n^(1+ε))
// It falls in the "gap" between Case 2 and Case 3
// Master Theorem: ❌ Doesn't apply
// Solution: Extended Master Theorem or recursion tree
```

### Case D: f(n) is Not Polynomial

```java
// T(n) = 2T(n/2) + O(2^n)
// f(n) is exponential, not polynomial
// Master Theorem: ❌ Doesn't apply
// But it's obviously dominated by the exponential: T(n) = O(2ⁿ)
```

---

## 5. The Substitution Method — Alternative When MT Fails

When the Master Theorem doesn't apply, use the **substitution method**:

1. **Guess** the form of the solution
2. **Verify** by induction
3. **Solve** for constants

### Example: T(n) = T(√n) + O(1)

```
This doesn't fit the standard form (b is variable).
But we can transform it!

Let n = 2^m → √n = 2^(m/2)
T(2^m) = T(2^(m/2)) + O(1)
Let S(m) = T(2^m)
S(m) = S(m/2) + O(1)

Now it fits MT! a=1, b=2, f(m)=O(1)
S(m) = O(log m)
T(n) = S(log n) = O(log log n)
```

**Result: T(n) = O(log log n)** — Very fast!

### Example: T(n) = 2T(n-1) + O(1)

```
Doesn't fit MT (b is not constant).
Recursion tree:
Level 0: 1 node, O(1) work
Level 1: 2 nodes, 2 × O(1) = O(2)
Level 2: 4 nodes, 4 × O(1) = O(4)
...
Level k: 2^k nodes

Total work = 1 + 2 + 4 + ... + 2ⁿ = 2^(n+1) - 1 = O(2ⁿ)
```

---

## 6. Quick Reference Table

| Recurrence | a | b | f(n) | n^(log_b a) | Case | Result |
|------------|---|---|------|-------------|------|--------|
| T(n/2) + O(1) | 1 | 2 | O(1) | n⁰ = 1 | 2 | O(log n) |
| T(n/2) + O(n) | 1 | 2 | O(n) | n⁰ = 1 | 3 | O(n) |
| 2T(n/2) + O(1) | 2 | 2 | O(1) | n¹ = n | 1 | O(n) |
| 2T(n/2) + O(n) | 2 | 2 | O(n) | n¹ = n | 2 | O(n log n) |
| 2T(n/2) + O(n²) | 2 | 2 | O(n²) | n¹ = n | 3 | O(n²) |
| 4T(n/2) + O(n) | 4 | 2 | O(n) | n² | 1 | O(n²) |
| 4T(n/2) + O(n²) | 4 | 2 | O(n²) | n² | 2 | O(n² log n) |
| 4T(n/2) + O(n³) | 4 | 2 | O(n³) | n² | 3 | O(n³) |
| 3T(n/3) + O(1) | 3 | 3 | O(1) | n¹ = n | 1 | O(n) |
| 3T(n/3) + O(n) | 3 | 3 | O(n) | n¹ = n | 2 | O(n log n) |
| T(n/3) + T(2n/3) + O(n) | — | — | — | — | — | O(n log n)* |

\*Recursion tree method needed; not pure Master Theorem form.

---

## 7. Intuition — Why the Theorem Works

The recursion tree has:
- **log_b n** levels
- **a^k** nodes at level k (k = 0 at root)
- Each node at level k does **f(n/b^k)** work
- Total work at level k: **a^k · f(n/b^k)**
- Leaf level has **a^(log_b n) = n^(log_b a)** nodes, each O(1)

The three cases correspond to:
1. **Work decreases geometrically** from root to leaves → leaves dominate
2. **Work is roughly equal** at each level → all levels matter (× log n)
3. **Work increases geometrically** from root to leaves → root dominates

```
Case 1: Root →  nodes → even fewer nodes → leaves win
         [====] [===] [==] [=]
Case 2: Same work each level
         [====] [====] [====] [====]
Case 3: Leaves → nodes → even more nodes → root (top) wins
         [=] [==] [===] [====]
```

---

## Master Theorem Cheat Sheet

```
T(n) = aT(n/b) + O(n^d)

Compare d with log_b a:
  d < log_b a  →  O(n^(log_b a))          (Case 1: recursion dominates)
  d = log_b a  →  O(n^d · log n)          (Case 2: balanced)
  d > log_b a  →  O(n^d)                  (Case 3: combine dominates)

Three steps:
1. Compute log_b a
2. Compare f(n) with n^(log_b a)
3. Apply the appropriate case
```

**Final tip:** In an interview, don't just cite the Master Theorem. Show you understand **why** by sketching the recursion tree. It demonstrates deeper understanding.
