# Combinatorics Guide for Infosys SP DSE

## 1. nCr Computation (with Modular Arithmetic)

### Basic nCr (Small Values)
```python
def nCr_basic(n, r):
    """Compute nCr without overflow (small values)."""
    if r > n or r < 0:
        return 0
    r = min(r, n - r)  # Use symmetry
    result = 1
    for i in range(r):
        result = result * (n - i) // (i + 1)
    return result

print(nCr_basic(10, 3))  # 120
print(nCr_basic(20, 10))  # 184756
```
**Time Complexity:** O(r)

### nCr with Modular Arithmetic (Precomputed Factorials)
```python
MOD = 10**9 + 7

def power_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
        base = base * base % mod
    return result

class Combinatorics:
    """Precompute factorials and inverse factorials for O(1) nCr queries."""
    def __init__(self, n, mod=MOD):
        self.mod = mod
        self.fact = [1] * (n + 1)
        self.inv_fact = [1] * (n + 1)

        for i in range(1, n + 1):
            self.fact[i] = self.fact[i - 1] * i % mod

        self.inv_fact[n] = power_mod(self.fact[n], mod - 2, mod)
        for i in range(n - 1, -1, -1):
            self.inv_fact[i] = self.inv_fact[i + 1] * (i + 1) % mod

    def nCr(self, n, r):
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv_fact[r] % self.mod * self.inv_fact[n - r] % self.mod

    def nPr(self, n, r):
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv_fact[n - r] % self.mod

# Usage
comb = Combinatorics(10**6)
print(comb.nCr(10, 3))    # 120
print(comb.nPr(10, 3))    # 720
```
**Preprocessing:** O(n)
**Query:** O(1)

---

## 2. Pascal's Triangle

```python
def pascal_triangle(n, mod=None):
    """Generate Pascal's triangle up to row n."""
    C = [[0] * (i + 1) for i in range(n + 1)]

    for i in range(n + 1):
        C[i][0] = 1
        C[i][i] = 1
        for j in range(1, i):
            if mod:
                C[i][j] = (C[i-1][j-1] + C[i-1][j]) % mod
            else:
                C[i][j] = C[i-1][j-1] + C[i-1][j]

    return C

# Without mod
triangle = pascal_triangle(5)
for row in triangle:
    print(row)
# [1]
# [1, 1]
# [1, 2, 1]
# [1, 3, 3, 1]
# [1, 4, 6, 4, 1]
# [1, 5, 10, 10, 5, 1]

# With mod
triangle_mod = pascal_triangle(5, mod=10**9 + 7)
```

### Build nCr Table from Pascal's
```python
def build_nCr_table(n, mod=10**9 + 7):
    """Build table where C[i][j] = iCr mod p."""
    C = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % mod
    return C

C = build_nCr_table(100)
print(C[10][3])  # 120
print(C[50][25]) # 50C25 mod 10^9+7
```
**Time Complexity:** O(n²)
**When to use:** Multiple queries, n ≤ 5000

---

## 3. nPr Computation

```python
MOD = 10**9 + 7

def power_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
        base = base * base % mod
    return result

def nPr(n, r, mod=MOD):
    """Compute nPr = n! / (n-r)! mod p."""
    if r > n or r < 0:
        return 0

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod

    # nPr = fact[n] / fact[n-r] = fact[n] * inv_fact[n-r]
    return fact[n] * power_mod(fact[n - r], mod - 2, mod) % mod

print(nPr(10, 3))  # 720 (10 * 9 * 8)
print(nPr(5, 5))   # 120 (5!)
```

---

## 4. Permutations with Repetition

When arranging n items where there are n1 identical items of type 1, n2 of type 2, etc.

```python
MOD = 10**9 + 7

def power_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
        base = base * base % mod
    return result

class Combinatorics:
    def __init__(self, n, mod=MOD):
        self.mod = mod
        self.fact = [1] * (n + 1)
        self.inv_fact = [1] * (n + 1)
        for i in range(1, n + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
        self.inv_fact[n] = power_mod(self.fact[n], mod - 2, mod)
        for i in range(n - 1, -1, -1):
            self.inv_fact[i] = self.inv_fact[i + 1] * (i + 1) % mod

    def nCr(self, n, r):
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv_fact[r] % self.mod * self.inv_fact[n - r] % self.mod

    def permutations_with_repetition(self, counts):
        """Given counts of each type, compute distinct permutations.
        Formula: n! / (n1! * n2! * ... * nk!)
        where n = sum(counts)"""
        n = sum(counts)
        result = self.fact[n]
        for c in counts:
            result = result * self.inv_fact[c] % self.mod
        return result

comb = Combinatorics(10**6)

# "MISSISSIPPI" has 11 letters: M=1, I=4, S=4, P=2
counts = [1, 4, 4, 2]  # M, I, S, P
print(comb.permutations_with_repetition(counts))  # 34650
```

---

## 5. Combinations with Repetition

Choose r items from n types with repetition allowed.

**Formula:** C(n+r-1, r) = C(n+r-1, n-1)

```python
MOD = 10**9 + 7

class Combinatorics:
    def __init__(self, n, mod=MOD):
        self.mod = mod
        self.fact = [1] * (n + 1)
        self.inv_fact = [1] * (n + 1)
        for i in range(1, n + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
        self.inv_fact[n] = pow(self.fact[n], mod - 2, mod)
        for i in range(n - 1, -1, -1):
            self.inv_fact[i] = self.inv_fact[i + 1] * (i + 1) % mod

    def nCr(self, n, r):
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv_fact[r] % self.mod * self.inv_fact[n - r] % self.mod

    def combinations_with_repetition(self, n, r):
        """Choose r items from n types with repetition.
        Formula: C(n+r-1, r)"""
        return self.nCr(n + r - 1, r)

comb = Combinatorics(10**6)

# How many ways to buy 5 fruits from 3 types (apple, banana, cherry)?
print(comb.combinations_with_repetition(3, 5))  # 21

# How many non-negative integer solutions to x1 + x2 + x3 = 10?
print(comb.combinations_with_repetition(3, 10))  # 66
```

---

## 6. Catalan Numbers

### Formula
C(n) = C(2n, n) / (n+1)

### Applications
- Valid bracket sequences with n pairs: `((()))`, `(()())`, etc.
- Number of full binary trees with n+1 leaves
- Ways to triangulate a convex polygon with n+2 sides
- Number of monotonic paths in nxgrid that don't cross diagonal

```python
MOD = 10**9 + 7

class Combinatorics:
    def __init__(self, n, mod=MOD):
        self.mod = mod
        self.fact = [1] * (n + 1)
        self.inv_fact = [1] * (n + 1)
        for i in range(1, n + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
        self.inv_fact[n] = pow(self.fact[n], mod - 2, mod)
        for i in range(n - 1, -1, -1):
            self.inv_fact[i] = self.inv_fact[i + 1] * (i + 1) % mod

    def nCr(self, n, r):
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv_fact[r] % self.mod * self.inv_fact[n - r] % self.mod

    def catalan(self, n):
        """nth Catalan number mod p."""
        return self.nCr(2 * n, n) * pow(n + 1, self.mod - 2, self.mod) % self.mod

    def catalan_direct(self, n):
        """Direct computation without precomputed factorials."""
        result = 1
        for i in range(n):
            result = result * (2 * n - i) // (i + 1)
        return result // (n + 1)

comb = Combinatorics(10**6)

# First 10 Catalan numbers
for i in range(10):
    print(f"C({i}) = {comb.catalan(i)}")
# C(0)=1, C(1)=1, C(2)=2, C(3)=5, C(4)=14, C(5)=42, ...

# Applications
print(f"Valid brackets with 4 pairs: {comb.catalan(4)}")  # 14
print(f"Full binary trees with 5 leaves: {comb.catalan(4)}")  # 14
print(f"Triangulate hexagon: {comb.catalan(4)}")  # 14
```

---

## 7. Stars and Bars Technique

Find number of non-negative integer solutions to: x1 + x2 + ... + xk = n

**Formula:** C(n + k - 1, k - 1)

```python
MOD = 10**9 + 7

class Combinatorics:
    def __init__(self, n, mod=MOD):
        self.mod = mod
        self.fact = [1] * (n + 1)
        self.inv_fact = [1] * (n + 1)
        for i in range(1, n + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
        self.inv_fact[n] = pow(self.fact[n], mod - 2, mod)
        for i in range(n - 1, -1, -1):
            self.inv_fact[i] = self.inv_fact[i + 1] * (i + 1) % self.mod

    def nCr(self, n, r):
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv_fact[r] % self.mod * self.inv_fact[n - r] % self.mod

    def stars_and_bars(self, n, k):
        """Number of non-negative solutions to x1 + x2 + ... + xk = n.
        Formula: C(n + k - 1, k - 1)"""
        return self.nCr(n + k - 1, k - 1)

    def stars_and_bars_positive(self, n, k):
        """Number of POSITIVE solutions to x1 + x2 + ... + xk = n.
        Each xi >= 1. Substitute yi = xi - 1, so yi >= 0 and sum = n - k.
        Formula: C(n - 1, k - 1)"""
        if n < k:
            return 0
        return self.nCr(n - 1, k - 1)

comb = Combinatorics(10**6)

# Distribute 10 identical balls into 3 distinct boxes (non-negative)
print(comb.stars_and_bars(10, 3))  # C(12, 2) = 66

# Distribute 10 identical balls into 3 distinct boxes (at least 1 each)
print(comb.stars_and_bars_positive(10, 3))  # C(9, 2) = 36

# Number of ways to write 10 as sum of 3 non-negative integers
print(comb.stars_and_bars(10, 3))  # 66
```

### Variant: Upper Bounds
```python
def stars_and_bars_with_upper_bound(n, k, upper_bounds):
    """Number of solutions to x1 + ... + xk = n where 0 <= xi <= ui.
    Uses inclusion-exclusion."""
    from itertools import combinations

    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        result = 1
        r = min(r, n - r)
        for i in range(r):
            result = result * (n - i) // (i + 1)
        return result

    total = nCr(n + k - 1, k - 1)  # Without upper bounds

    # Inclusion-exclusion
    for mask in range(1, 1 << k):
        subtract = 0
        bits = []
        for i in range(k):
            if mask & (1 << i):
                bits.append(i)

        # Sum of upper bounds exceeded
        sum_exceeded = n + 1
        for b in bits:
            sum_exceeded += upper_bounds[b] + 1

        sign = -1 if len(bits) % 2 == 1 else 1
        total += sign * nCr(sum_exceeded - 1, k - 1)

    return total
```

---

## 8. Inclusion-Exclusion Principle

```python
def inclusion_exclusion(n, properties):
    """
    Count elements that have NONE of the properties.
    properties[i] = count of elements with property i
    properties[intersection] = count of elements with all properties in subset
    """
    from itertools import combinations

    total = 0
    for mask in range(1, 1 << n):
        bits = [i for i in range(n) if mask & (1 << i)]
        intersection = properties[tuple(bits)]

        if len(bits) % 2 == 1:
            total -= intersection
        else:
            total += intersection

    return total

# Example: Count numbers from 1 to 100 divisible by 2, 3, or 5
def count_divisible_by_at_least_one(limit, divisors):
    """Count numbers in [1, limit] divisible by at least one of the divisors."""
    from math import gcd
    from functools import reduce

    def lcm(a, b):
        return a * b // gcd(a, b)

    def lcm_of_list(lst):
        return reduce(lcm, lst)

    total = 0
    n = len(divisors)

    for mask in range(1, 1 << n):
        subset = [divisors[i] for i in range(n) if mask & (1 << i)]
        l = lcm_of_list(subset)
        count = limit // l

        if len(subset) % 2 == 1:
            total += count
        else:
            total -= count

    return total

# How many numbers from 1 to 100 are divisible by 2, 3, or 5?
result = count_divisible_by_at_least_one(100, [2, 3, 5])
print(result)  # 74
```

### Classic Example: Derangements via Inclusion-Exclusion
```python
def derangements_inclusion_exclusion(n):
    """Count derangements using inclusion-exclusion."""
    from math import factorial, comb

    result = 0
    for k in range(n + 1):
        result += ((-1) ** k) * comb(n, k) * factorial(n - k)

    return result

for i in range(8):
    print(f"D({i}) = {derangements_inclusion_exclusion(i)}")
# D(0)=1, D(1)=0, D(2)=1, D(3)=2, D(4)=9, D(5)=44, D(6)=265, D(7)=1854
```

---

## 9. Derangements

A derangement is a permutation where no element appears in its original position.

**Formula:** D(n) = (n-1) * (D(n-1) + D(n-2))
**Base:** D(0) = 1, D(1) = 0

### Recursive with Memoization
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def derangement(n):
    if n == 0:
        return 1
    if n == 1:
        return 0
    return (n - 1) * (derangement(n - 1) + derangement(n - 2))

for i in range(10):
    print(f"D({i}) = {derangement(i)}")
```

### Iterative
```python
def derangement_iterative(n):
    if n == 0:
        return 1
    if n == 1:
        return 0

    d_prev2, d_prev1 = 1, 0  # D(0), D(1)
    for i in range(2, n + 1):
        d_curr = (i - 1) * (d_prev1 + d_prev2)
        d_prev2, d_prev1 = d_prev1, d_curr

    return d_prev1

for i in range(10):
    print(f"D({i}) = {derangement_iterative(i)}")
```

### Derangements with Modular Arithmetic
```python
MOD = 10**9 + 7

def derangement_mod(n, mod=MOD):
    if n == 0:
        return 1
    if n == 1:
        return 0

    d_prev2, d_prev1 = 1, 0
    for i in range(2, n + 1):
        d_curr = (i - 1) * (d_prev1 + d_prev2) % mod
        d_prev2, d_prev1 = d_prev1, d_curr

    return d_prev1

print(derangement_mod(10))  # 1334961
print(derangement_mod(10**6))  # Works for large n!
```

### Closed Form (Approximation)
```python
import math

def derangement_approx(n):
    """D(n) ≈ n! / e (round to nearest integer)."""
    return round(math.factorial(n) / math.e)

for i in range(10):
    print(f"D_approx({i}) = {derangement_approx(i)}")
```

**Time Complexity:** O(n)
**When to use:** "No element in its original position" problems

---

## Complete Example: Infosys-Style Combinatorics Problem

**Problem:** Count the number of ways to distribute n identical candies among k children such that each child gets at least 1 candy, modulo 10^9+7.

```python
MOD = 10**9 + 7

class Combinatorics:
    def __init__(self, n, mod=MOD):
        self.mod = mod
        self.fact = [1] * (n + 1)
        self.inv_fact = [1] * (n + 1)
        for i in range(1, n + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
        self.inv_fact[n] = pow(self.fact[n], mod - 2, mod)
        for i in range(n - 1, -1, -1):
            self.inv_fact[i] = self.inv_fact[i + 1] * (i + 1) % self.mod

    def nCr(self, n, r):
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv_fact[r] % self.mod * self.inv_fact[n - r] % self.mod

    def stars_and_bars_positive(self, n, k):
        """C(n-1, k-1)"""
        return self.nCr(n - 1, k - 1)

comb = Combinatorics(10**6)

# Distribute 10 candies among 3 children, each gets at least 1
print(comb.stars_and_bars_positive(10, 3))  # C(9,2) = 36

# With upper bounds (each child gets at most 4)
# Use inclusion-exclusion variant
```

---

## Quick Reference

| Problem | Formula | Complexity |
|---------|---------|------------|
| nCr | n! / (r! * (n-r)!) | O(1) after O(n) preprocessing |
| nPr | n! / (n-r)! | O(1) after O(n) preprocessing |
| Permutations with repetition | n! / (n1! * n2! * ... * nk!) | O(k) |
| Combinations with repetition | C(n+r-1, r) | O(1) after O(n) preprocessing |
| Catalan number | C(2n,n) / (n+1) | O(n) after O(n) preprocessing |
| Stars and bars | C(n+k-1, k-1) | O(1) after O(n) preprocessing |
| Derangements | (n-1) * (D(n-1) + D(n-2)) | O(n) |
| Inclusion-exclusion | Sum over subsets | O(2^k) |

### Common Patterns in Infosys Problems
1. **Count paths:** nCr(n+m, n) or nCr(n+m-2, n-1)
2. **Distribute identical items:** Stars and bars
3. **No element in place:** Derangements
4. **Valid parentheses:** Catalan numbers
5. **At least one property:** Inclusion-exclusion
6. **Choose committee:** nCr(n, k)
