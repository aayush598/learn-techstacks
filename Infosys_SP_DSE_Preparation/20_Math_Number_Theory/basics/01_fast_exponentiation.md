# Fast Exponentiation (Binary Exponentiation)

## Why Fast Exponentiation?

Computing a^n naively takes O(n) multiplications. Binary exponentiation does it in **O(log n)**.

```
Naive: a^n = a * a * a * ... * a (n times) → O(n)
Binary: a^n = a^(b_k) * a^(b_{k-1}) * ... where n = binary(b_k...b_0) → O(log n)
```

---

## 1. Binary Exponentiation (Recursive)

```python
def power_recursive(base, exp, mod=None):
    """Compute base^exp, optionally mod m."""
    if exp == 0:
        return 1

    half = power_recursive(base, exp // 2, mod)

    if mod:
        result = half * half % mod
        if exp % 2 == 1:
            result = result * base % mod
    else:
        result = half * half
        if exp % 2 == 1:
            result *= base

    return result

print(power_recursive(2, 10))        # 1024
print(power_recursive(2, 10, 1000))  # 24
```

**Logic:**
- If exp is even: a^n = (a^(n/2))^2
- If exp is odd: a^n = a * (a^(n/2))^2

**Time Complexity:** O(log exp)
**Space Complexity:** O(log exp) due to recursion stack

---

## 2. Binary Exponentiation (Iterative)

```python
def power_iterative(base, exp, mod=None):
    """Compute base^exp, optionally mod m. Iterative version."""
    result = 1
    if mod:
        base %= mod

    while exp > 0:
        if exp & 1:  # If exp is odd (check last bit)
            result = result * base
            if mod:
                result %= mod
        exp >>= 1  # Right shift (divide by 2)
        base = base * base
        if mod:
            base %= mod

    return result

print(power_iterative(2, 10))        # 1024
print(power_iterative(2, 10, 1000))  # 24
print(power_iterative(3, 13, 100))   # 3^13 % 100 = 97
```

**Step-by-step trace for power_iterative(2, 13):**
```
exp=13 (binary: 1101), base=2, result=1

Step 1: exp=13 (odd)  → result = 1*2 = 2,   base = 4,   exp = 6
Step 2: exp=6  (even) → result = 2,          base = 16,  exp = 3
Step 3: exp=3  (odd)  → result = 2*16 = 32,  base = 256, exp = 1
Step 4: exp=1  (odd)  → result = 32*256=8192, base = 65536, exp = 0
Result: 8192 = 2^13 ✓
```

**Time Complexity:** O(log exp)
**Space Complexity:** O(1) — preferred over recursive version

---

## 3. Matrix Exponentiation for Fibonacci

Compute Fibonacci(n) for extremely large n (e.g., 10^18).

### Matrix Formulation
```
| F(n+1)  F(n)   |   | 1  1 |^n
| F(n)    F(n-1) | = | 1  0 |
```

### Implementation
```python
def matrix_mult(A, B, mod=None):
    """Multiply two 2x2 matrices."""
    if mod:
        return [
            [(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % mod,
             (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % mod],
            [(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % mod,
             (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % mod]
        ]
    return [
        [A[0][0]*B[0][0] + A[0][1]*B[1][0],
         A[0][0]*B[0][1] + A[0][1]*B[1][1]],
        [A[1][0]*B[0][0] + A[1][1]*B[1][0],
         A[1][0]*B[0][1] + A[1][1]*B[1][1]]
    ]

def matrix_power(M, p, mod=None):
    """Compute M^p using binary exponentiation."""
    # Start with identity matrix
    result = [[1, 0], [0, 1]]
    while p > 0:
        if p & 1:
            result = matrix_mult(result, M, mod)
        M = matrix_mult(M, M, mod)
        p >>= 1
    return result

def fibonacci(n, mod=None):
    """Compute nth Fibonacci number using matrix exponentiation."""
    if n <= 1:
        return n % mod if mod else n

    M = [[1, 1], [1, 0]]
    result = matrix_power(M, n, mod)
    return result[0][1]

# Examples
print(fibonacci(10))                    # 55
print(fibonacci(100))                   # 354224848179261915075
print(fibonacci(10**18, 10**9 + 7))     # Works for huge n!
```

### Generalized Fibonacci
```python
def generalized_fibonacci(n, a, b, c, d, mod=None):
    """Compute terms of a generalized recurrence:
    f(n) = a*f(n-1) + b*f(n-2) with initial values f(0)=c, f(1)=d
    Uses matrix: | a b |^n     applied to | d |
                 | 1 0 |                 | c |
    """
    if n == 0:
        return c % mod if mod else c
    if n == 1:
        return d % mod if mod else d

    M = [[a, b], [1, 0]]
    result = matrix_power(M, n - 1, mod)

    if mod:
        return (result[0][0] * d + result[0][1] * c) % mod
    return result[0][0] * d + result[0][1] * c

# Standard Fibonacci: f(n) = f(n-1) + f(n-2)
print(generalized_fibonacci(10, 1, 1, 0, 1))  # 55

# Lucas numbers: L(n) = L(n-1) + L(n-2), L(0)=2, L(1)=1
print(generalized_fibonacci(10, 1, 1, 2, 1))  # 123
```

**Time Complexity:** O(log n) with O(1) matrix operations
**When to use:** n > 10^7 (DP won't work), or when mod is required

---

## 4. Power of a Number Modulo M

```python
def power_mod(base, exp, mod):
    """Standard binary exponentiation modulo m."""
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
        base = base * base % mod
    return result

# Python built-in (most efficient, implemented in C):
print(pow(2, 100, 10**9 + 7))  # Equivalent to power_mod(2, 100, 10**9+7)
```

### Edge Cases
```python
def power_mod_safe(base, exp, mod):
    """Handles edge cases: negative base, zero exponent, etc."""
    if mod == 1:
        return 0  # Everything mod 1 is 0
    if exp == 0:
        return 1  # a^0 = 1 for any a

    result = 1
    base %= mod  # Handle negative base

    while exp > 0:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
        base = base * base % mod

    return result

print(power_mod_safe(0, 0, 7))    # 1 (0^0 = 1 by convention)
print(power_mod_safe(-3, 2, 7))   # 2 ((-3)^2 % 7 = 9 % 7 = 2)
print(power_mod_safe(2, 0, 7))    # 1
```

---

## 5. Computing Large Powers Efficiently

### Large Base and Large Exponent
```python
def power_large(base, exp, mod):
    """Handle base > mod and exp > mod."""
    # Reduce base first
    base %= mod

    # If exp is very large and mod is prime, use Fermat:
    # a^(p-1) ≡ 1 (mod p)
    # So a^exp ≡ a^(exp % (p-1)) (mod p) when gcd(a,p) = 1

    # For general case, just use binary exponentiation
    return power_mod(base, exp, mod)

def power_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
        base = base * base % mod
    return result

# Compute 2^1000000 mod 10^9+7
print(power_large(2, 10**6, 10**9 + 7))
```

### When Base is a Product
```python
def power_of_product_mod(factors, exp, mod):
    """Compute (f1 * f2 * ... * fk)^exp mod m."""
    result = 1
    for f in factors:
        result = result * power_mod(f, exp, mod) % mod
    return result

# (2 * 3 * 5)^4 mod 7 = 30^4 mod 7
print(power_of_product_mod([2, 3, 5], 4, 7))  # 30^4 % 7 = 4
```

---

## 6. Applications

### Application 1: Power of Large Numbers
```python
def is_power_of_two(n):
    """Check if n is a power of 2."""
    return n > 0 and (n & (n - 1)) == 0

# Or using bit count:
def is_power_of_two_v2(n):
    return n > 0 and bin(n).count('1') == 1
```

### Application 2: Count Ways with Combinatorics
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

def count_ways_to_climb_stairs(n):
    """Count ways to climb n stairs (1 or 2 steps at a time).
    This is Fibonacci(n+1)."""
    # Using matrix exponentiation
    if n <= 1:
        return n + 1

    def matrix_mult(A, B):
        return [
            [A[0][0]*B[0][0] + A[0][1]*B[1][0],
             A[0][0]*B[0][1] + A[0][1]*B[1][1]],
            [A[1][0]*B[0][0] + A[1][1]*B[1][0],
             A[1][0]*B[0][1] + A[1][1]*B[1][1]]
        ]

    def matrix_power(M, p):
        result = [[1, 0], [0, 1]]
        while p > 0:
            if p & 1:
                result = matrix_mult(result, M)
            M = matrix_mult(M, M)
            p >>= 1
        return result

    M = [[1, 1], [1, 0]]
    result = matrix_power(M, n)
    return (result[0][0] + result[0][1]) % MOD

print(count_ways_to_climb_stairs(10))  # 89
```

### Application 3: Matrix Chain Exponentiation
```python
def matrix_mult(A, B, mod=None):
    """Multiply two n x n matrices."""
    n = len(A)
    if mod:
        return [[sum(A[i][k] * B[k][j] for k in range(n)) % mod
                 for j in range(n)] for i in range(n)]
    return [[sum(A[i][k] * B[k][j] for k in range(n))
             for j in range(n)] for i in range(n)]

def matrix_power(M, p, mod=None):
    """Compute M^p using binary exponentiation."""
    n = len(M)
    # Identity matrix
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    while p > 0:
        if p & 1:
            result = matrix_mult(result, M, mod)
        M = matrix_mult(M, M, mod)
        p >>= 1
    return result

# Example: Compute M^10 for a 3x3 matrix
M = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]

result = matrix_power(M, 10)
for row in result:
    print(row)
```

### Application 4: Number of Paths in Grid
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

def paths_in_grid(n, m):
    """Count paths from (0,0) to (n,m) moving only right or down.
    Answer: C(n+m, n)"""
    # This requires nCr computation
    # Using precomputed factorials
    max_val = n + m
    fact = [1] * (max_val + 1)
    for i in range(1, max_val + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (max_val + 1)
    inv_fact[max_val] = power_mod(fact[max_val], MOD - 2, MOD)
    for i in range(max_val - 1, -1, -1):
        inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD

    return fact[n + m] * inv_fact[n] % MOD * inv_fact[m] % MOD

print(paths_in_grid(3, 3))  # 20
```

### Application 5: Fast Modular Inverse
```python
def power_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
        base = base * base % mod
    return result

def mod_inverse(a, mod):
    """Modular inverse using Fermat's Little Theorem (mod must be prime)."""
    return power_mod(a, mod - 2, mod)

print(mod_inverse(3, 10**9 + 7))  # 333333336
print(3 * mod_inverse(3, 10**9 + 7) % (10**9 + 7))  # 1 ✓
```

---

## 7. Advanced: Multi-Exponentiation

```python
def power_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
        base = base * base % mod
    return result

def multi_power_mod(bases, exponents, mod):
    """Compute (b1^e1 * b2^e2 * ... * bk^ek) mod m."""
    result = 1
    for b, e in zip(bases, exponents):
        result = result * power_mod(b, e, mod) % mod
    return result

# Example: 2^10 * 3^5 * 5^3 mod 100
print(multi_power_mod([2, 3, 5], [10, 5, 3], 100))  # 72
```

---

## Quick Reference

| Function | Time | Space | Use Case |
|----------|------|-------|----------|
| power_recursive | O(log n) | O(log n) | When recursion is acceptable |
| power_iterative | O(log n) | O(1) | Preferred for scalar power |
| matrix_power | O(k³ log n) | O(k²) | Linear recurrences, k=dim |
| pow(a, n, m) | O(log n) | O(1) | Python built-in (fastest) |

### Key Formulas
```
a^0 = 1
a^1 = a
a^n = (a^(n/2))^2        if n is even
a^n = a * (a^(n/2))^2    if n is odd
a^(-1) mod p = a^(p-2) mod p   (Fermat, p prime)
Fibonacci(n) via matrix: [[1,1],[1,0]]^n
```
