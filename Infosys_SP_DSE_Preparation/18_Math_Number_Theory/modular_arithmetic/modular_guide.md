# Modular Arithmetic Guide for Infosys SP DSE

> **CRITICAL:** Most Infosys problems require answers modulo 10^9+7. Understanding modular arithmetic is essential.

## 1. What is Modular Arithmetic?

Modular arithmetic is "clock arithmetic" — numbers wrap around after reaching a modulus.

```python
# Basic modulo operation
print(17 % 5)   # 2 (17 = 3*5 + 2)
print(-3 % 5)   # 2 (Python handles negative modulo correctly!)
print(10 % 3)   # 1
```

### Key Property
```python
# If a ≡ b (mod m), then:
# (a + c) ≡ (b + c) (mod m)
# (a * c) ≡ (b * c) (mod m)
# (a - c) ≡ (b - c) (mod m)

# Example
a, b, m = 17, 7, 5
print(a % m == b % m)  # True (both ≡ 2 mod 5)
```

---

## 2. Modular Addition

```python
def add_mod(a, b, mod):
    return (a + b) % mod

# Or safely handle large numbers:
def add_mod_safe(a, b, mod):
    a %= mod
    b %= mod
    return (a + b) % mod

print(add_mod_safe(10**18, 10**18, 10**9 + 7))  # 999999999
```
**Rule:** `(a + b) % m = ((a % m) + (b % m)) % m`

---

## 3. Modular Subtraction

```python
def sub_mod(a, b, mod):
    return (a - b) % mod

# Python handles negative results correctly:
print(sub_mod(3, 5, 7))  # 5 (not -2!)
# (3 - 5) % 7 = -2 % 7 = 5 ✓
```
**Rule:** `(a - b) % m = ((a % m) - (b % m) + m) % m`

### Pitfall: Negative Numbers
```python
# WRONG (in some languages):
result = (a - b) % mod  # Might be negative

# CORRECT (Python does this automatically):
result = (a - b) % mod  # Always non-negative in Python

# For safety in any language:
result = (a - b) % mod
if result < 0:
    result += mod
```

---

## 4. Modular Multiplication

```python
def mul_mod(a, b, mod):
    return (a * b) % mod

# For very large numbers, Python handles big integers natively
print((10**18 * 10**18) % (10**9 + 7))  # Works fine in Python!
```
**Rule:** `(a * b) % m = ((a % m) * (b % m)) % m`

---

## 5. Modular Division (Modular Inverse)

Division in modular arithmetic means multiplying by the **modular inverse**.

```python
# a / b (mod m) = a * b^(-1) (mod m)
# where b^(-1) is the modular inverse of b

# The modular inverse of b mod m exists if gcd(b, m) = 1
```

### When Does Modular Inverse Exist?
```python
from math import gcd

def has_inverse(b, m):
    return gcd(b, m) == 1

print(has_inverse(3, 7))   # True (gcd(3,7)=1)
print(has_inverse(4, 6))   # False (gcd(4,6)=2)
```

---

## 6. Fermat's Little Theorem

If p is prime and gcd(a, p) = 1, then:
**a^(p-1) ≡ 1 (mod p)**

Therefore: **a^(-1) ≡ a^(p-2) (mod p)**

```python
def power_mod(base, exp, mod):
    """Binary exponentiation: base^exp % mod."""
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
        base = base * base % mod
    return result

def mod_inverse_fermat(a, mod):
    """Modular inverse using Fermat's Little Theorem.
    Only works when mod is PRIME."""
    return power_mod(a, mod - 2, mod)

# Example: Find 3^(-1) mod 7
inv = mod_inverse_fermat(3, 7)
print(inv)  # 5
print(3 * inv % 7)  # 1 ✓ (3 * 5 = 15 ≡ 1 mod 7)
```

### Usage in nCr
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

def nCr_mod(n, r, mod):
    if r > n or r < 0:
        return 0
    r = min(r, n - r)

    # Precompute factorials on the fly
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod

    # nCr = fact[n] / (fact[r] * fact[n-r])
    numerator = fact[n]
    denominator = fact[r] * fact[n - r] % mod
    return numerator * power_mod(denominator, mod - 2, mod) % mod

print(nCr_mod(10, 3, MOD))  # 120
print(nCr_mod(100, 50, MOD))  # Large number mod 10^9+7
```

---

## 7. Modular Exponentiation (Binary Exponentiation / Fast Power)

**This is the most important modular arithmetic technique.**

### Iterative Version
```python
def power_mod(base, exp, mod):
    """Compute base^exp % mod efficiently."""
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:  # If exp is odd
            result = result * base % mod
        exp >>= 1  # exp //= 2
        base = base * base % mod
    return result

print(power_mod(2, 10, 1000))  # 1024 % 1000 = 24
print(power_mod(2, 100, 10**9 + 7))  # Works for huge exponents!
```

### Recursive Version
```python
def power_mod_recursive(base, exp, mod):
    if exp == 0:
        return 1
    if exp % 2 == 0:
        half = power_mod_recursive(base, exp // 2, mod)
        return half * half % mod
    else:
        return base * power_mod_recursive(base, exp - 1, mod) % mod
```
**Time Complexity:** O(log exp) — from O(exp) to O(log exp)!

---

## 8. Modular Inverse using Extended Euclidean

Works for ANY modulus (not just prime).

```python
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    """Modular inverse using Extended Euclidean Algorithm.
    Works for any a and m where gcd(a, m) = 1."""
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        return None  # Inverse doesn't exist
    return x % m

print(mod_inverse(3, 7))   # 5
print(mod_inverse(10, 17)) # 12
print(mod_inverse(4, 6))   # None (gcd(4,6) ≠ 1)
```

### Comparison of Inverse Methods
| Method | Condition | When to Use |
|--------|-----------|-------------|
| Fermat's Little Theorem | mod is prime | Most CP problems (mod = 10^9+7) |
| Extended Euclidean | gcd(a, mod) = 1 | Any modulus |

---

## 9. Pre-computing Factorials and Inverse Factorials

**Essential pattern for Infosys problems involving combinations.**

```python
MOD = 10**9 + 7
MAX_N = 10**6

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

        # Precompute factorials
        for i in range(1, n + 1):
            self.fact[i] = self.fact[i - 1] * i % mod

        # Precompute inverse factorials using Fermat's Little Theorem
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
print(comb.nCr(100, 50))  # nCr(100,50) mod 10^9+7
print(comb.nPr(10, 3))    # 720
```
**Preprocessing Time:** O(n)
**Query Time:** O(1) per query

---

## 10. Pre-computing Powers of a Number

```python
MOD = 10**9 + 7

def precompute_powers(a, max_exp, mod=MOD):
    """Precompute a^0, a^1, a^2, ..., a^max_exp mod m."""
    powers = [1] * (max_exp + 1)
    for i in range(1, max_exp + 1):
        powers[i] = powers[i - 1] * a % mod
    return powers

# Example: Precompute powers of 2
pow2 = precompute_powers(2, 100)
print(pow2[10])  # 1024

# Usage in counting problems
# "How many subsets of size k from n elements?"
# Answer: 2^n mod 10^9+7
print(pow2[n])  # O(1) lookup
```

---

## 11. Why Mod 10^9+7?

```python
MOD = 10**9 + 7  # = 1000000007

# Reasons:
# 1. It's a prime number (allows modular inverse via Fermat)
# 2. It's large enough to avoid overflow in most problems
# 3. It fits in a 32-bit integer
# 4. 2 * 10^9+7 < 2^31 (safe for intermediate calculations)
# 5. Most competitive programming platforms use it

# Verify it's prime:
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

print(is_prime(10**9 + 7))  # True ✓
```

### Other Common Mods
```python
MOD1 = 10**9 + 7   # Most common
MOD2 = 998244353   # Used in NTT (Number Theoretic Transform)
MOD3 = 10**9 + 9   # Alternative prime
```

---

## 12. Common Pitfalls in Modular Arithmetic

### Pitfall 1: Integer Division Doesn't Work
```python
# WRONG: (a / b) % mod ≠ (a % mod) / (b % mod)
a, b, mod = 10, 3, 7
# (10 / 3) % 7 is NOT (10 % 7) / (3 % 7) = 3 / 1 = 3

# CORRECT: Use modular inverse
def power_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
        base = base * base % mod
    return result

def div_mod(a, b, mod):
    return a * power_mod(b, mod - 2, mod) % mod

print(div_mod(10, 3, 7))  # 10 * 3^5 mod 7 = 10 * 5 mod 7 = 5
```

### Pitfall 2: Subtraction Can Go Negative
```python
# In Python, modulo always returns non-negative:
print((-5) % 7)  # 2 ✓

# But be careful in other languages!
# C++/Java: (-5) % 7 = -5 (not 2!)
# Fix: ((a - b) % m + m) % m
```

### Pitfall 3: Forgetting to Mod Intermediate Results
```python
# WRONG for large numbers:
result = fact[n] * inv_fact[r] * inv_fact[n-r]  # May overflow!

# CORRECT:
result = fact[n] * inv_fact[r] % MOD
result = result * inv_fact[n-r] % MOD
```

### Pitfall 4: Mod Before Comparison
```python
# WRONG:
if result == expected:

# CORRECT (when dealing with modular results):
if result % MOD == expected % MOD:
```

### Pitfall 5: Mod with Negative Exponents
```python
# a^(-1) mod p = a^(p-2) mod p (Fermat's Little Theorem)
# NOT a^(-1) directly!

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
    return power_mod(a, mod - 2, mod)  # a^(p-2) not a^(-1)
```

---

## 13. Handling Negative Numbers in Modular Arithmetic

```python
MOD = 10**9 + 7

def normalize(x, mod):
    """Ensure result is in [0, mod-1]."""
    return x % mod

# Python's % operator already handles this:
print(normalize(-5, 7))   # 2
print(normalize(-100, 7)) # 5
print(normalize(100, 7))  # 2

# But for clarity in complex expressions:
def safe_add(a, b, mod):
    return (a + b) % mod

def safe_sub(a, b, mod):
    return (a - b) % mod  # Python: always non-negative

def safe_mul(a, b, mod):
    return (a * b) % mod

# Example: Computing (a - b + c) mod m safely
a, b, c, m = 5, 10, 3, 7
result = (a - b + c) % m
print(result)  # (5 - 10 + 3) % 7 = -2 % 7 = 5 ✓
```

---

## 14. Complete Example: Infosys-Style Problem

**Problem:** Find the number of ways to choose 2 items from n items, modulo 10^9+7, for multiple queries.

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

# Process queries
comb = Combinatorics(10**6)

queries = [(10, 2), (100, 50), (1000, 500)]
for n, r in queries:
    print(f"C({n},{r}) mod {MOD} = {comb.nCr(n, r)}")
```

---

## Quick Reference Table

| Operation | Formula | Code |
|-----------|---------|------|
| (a+b) mod m | ((a%m)+(b%m))%m | `(a+b) % m` |
| (a-b) mod m | ((a%m)-(b%m)+m)%m | `(a-b) % m` |
| (a*b) mod m | ((a%m)*(b%m))%m | `(a*b) % m` |
| (a/b) mod m | a * b^(m-2) mod m | `a * pow(b, m-2, m) % m` |
| a^n mod m | Binary exponentiation | `pow(a, n, m)` |
| a^(-1) mod m (prime) | a^(m-2) mod m | `pow(a, m-2, m)` |
| nCr mod p | fact[n]/(fact[r]*fact[n-r]) | See Combinatorics class |

---

## Python Built-in Modular Exponentiation

```python
# Python has built-in three-argument pow():
print(pow(2, 10, 1000))  # 24 (2^10 % 1000)
print(pow(3, 1000000, 10**9 + 7))  # Efficient!

# This is equivalent to our power_mod function
# and is implemented in C, so it's faster.
```
