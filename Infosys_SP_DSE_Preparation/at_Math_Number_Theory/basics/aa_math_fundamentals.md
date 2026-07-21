# Math Fundamentals for Infosys SP DSE

## 1. GCD (Greatest Common Divisor)

### Using math.gcd (Built-in)
```python
import math

a, b = 12, 18
print(math.gcd(a, b))  # 6

# Python 3.9+ supports multiple arguments
print(math.gcd(12, 18, 24))  # 6
```
**Time Complexity:** O(log(min(a, b)))
**When to use:** Default choice in CP

### Euclidean Algorithm (Recursive)
```python
def gcd_recursive(a, b):
    if b == 0:
        return a
    return gcd_recursive(b, a % b)
```
**Time Complexity:** O(log(min(a, b)))
**Space Complexity:** O(log(min(a, b))) due to recursion stack

### Euclidean Algorithm (Iterative)
```python
def gcd_iterative(a, b):
    while b:
        a, b = b, a % b
    return a
```
**Time Complexity:** O(log(min(a, b)))
**Space Complexity:** O(1)

### GCD of Array
```python
from math import gcd
from functools import reduce

def gcd_of_array(arr):
    return reduce(gcd, arr)

print(gcd_of_array([12, 18, 24]))  # 6
```

---

## 2. LCM (Least Common Multiple)

### Using math.lcm (Built-in, Python 3.9+)
```python
import math

a, b = 4, 6
print(math.lcm(a, b))  # 12
```

### Using Formula: LCM(a,b) = a*b // GCD(a,b)
```python
from math import gcd

def lcm(a, b):
    return a * b // gcd(a, b)

print(lcm(4, 6))  # 12
```
**Time Complexity:** O(log(min(a, b)))
**When to use:** When math.lcm is unavailable

### LCM of Array
```python
from math import gcd
from functools import reduce

def lcm(a, b):
    return a * b // gcd(a, b)

def lcm_of_array(arr):
    return reduce(lcm, arr)

print(lcm_of_array([4, 6, 8]))  # 24
```

---

## 3. Extended Euclidean Algorithm

Finds x, y such that: **ax + by = gcd(a, b)**

```python
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Example
gcd, x, y = extended_gcd(35, 15)
print(f"gcd={gcd}, x={x}, y={y}")  # gcd=5, x=1, y=-2
# Verification: 35*1 + 15*(-2) = 35 - 30 = 5 ✓
```

### Iterative Version
```python
def extended_gcd_iterative(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t
```
**Time Complexity:** O(log(min(a, b)))
**When to use:** Finding modular inverse, solving linear Diophantine equations

---

## 4. Sieve of Eratosthenes

Find all primes up to N.

```python
def sieve_of_eratosthenes(n):
    """Returns list of all primes up to n."""
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    return [i for i in range(2, n + 1) if is_prime[i]]

primes = sieve_of_eratosthenes(50)
print(primes)  # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

### Optimized Sieve (Memory Efficient)
```python
def sieve_optimized(n):
    """Bit-level optimization using bytearray."""
    if n < 2:
        return []
    is_prime = bytearray([1]) * (n + 1)
    is_prime[0] = is_prime[1] = 0

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = bytearray(len(is_prime[i*i::i]))

    return [i for i in range(2, n + 1) if is_prime[i]]
```

### Smallest Prime Factor Sieve
```python
def smallest_prime_factor_sieve(n):
    """Returns array where spf[i] = smallest prime factor of i."""
    spf = list(range(n + 1))
    for i in range(2, int(n**0.5) + 1):
        if spf[i] == i:  # i is prime
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

spf = smallest_prime_factor_sieve(50)
print(spf[45])  # 3 (smallest prime factor of 45)
```
**Time Complexity:** O(n log log n)
**Space Complexity:** O(n)
**When to use:** Need all primes up to 10^6 or 10^7

---

## 5. Segmented Sieve

For finding primes in a large range [L, R] when R can be up to 10^12 but R-L is small.

```python
import math

def segmented_sieve(low, high):
    """Find all primes in range [low, high]."""
    # Get primes up to sqrt(high) using basic sieve
    limit = int(math.isqrt(high)) + 1
    basic_primes = []
    is_prime_small = [True] * (limit + 1)
    is_prime_small[0] = is_prime_small[1] = False

    for i in range(2, limit + 1):
        if is_prime_small[i]:
            basic_primes.append(i)
            for j in range(i * i, limit + 1, i):
                is_prime_small[j] = False

    # Segmented sieve
    size = high - low + 1
    is_prime_range = [True] * size

    for p in basic_primes:
        # Find the first multiple of p in [low, high]
        start = max(p * p, ((low + p - 1) // p) * p)
        for j in range(start, high + 1, p):
            is_prime_range[j - low] = False

    # Handle edge case for 0 and 1
    if low == 0:
        is_prime_range[0] = is_prime_range[1] = False
    elif low == 1:
        is_prime_range[0] = False

    return [low + i for i in range(size) if is_prime_range[i]]

primes = segmented_sieve(10, 50)
print(primes)  # [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```
**Time Complexity:** O((R-L) log log R + sqrt(R) log log sqrt(R))
**When to use:** R up to 10^12, but R-L ≤ 10^6

---

## 6. Primality Check

### Trial Division
```python
def is_prime_trial(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
```
**Time Complexity:** O(sqrt(n))
**When to use:** n ≤ 10^12

### Miller-Rabin Primality Test
```python
import random

def power_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = result * base % mod
        exp //= 2
        base = base * base % mod
    return result

def miller_rabin(n, k=20):
    """Probabilistic primality test. k = number of rounds."""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = power_mod(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = power_mod(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Composite

    return True  # Probably prime
```
**Time Complexity:** O(k * log²(n))
**When to use:** n > 10^12, need fast primality check

---

## 7. Prime Factorization

### Trial Division
```python
def prime_factorization(n):
    """Returns dict of {prime: exponent}."""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

print(prime_factorization(360))  # {2: 3, 3: 2, 5: 1}
```

### Using SPF Sieve (for multiple queries)
```python
def smallest_prime_factor_sieve(n):
    spf = list(range(n + 1))
    for i in range(2, int(n**0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

def factorize_with_spf(spf, n):
    """Factorize n using precomputed SPF array."""
    factors = {}
    while n > 1:
        p = spf[n]
        factors[p] = factors.get(p, 0) + 1
        n //= p
    return factors

# Precompute once
spf = smallest_prime_factor_sieve(10**6)
print(factorize_with_spf(spf, 360))  # {2: 3, 3: 2, 5: 1}
```
**Time Complexity:** Trial: O(sqrt(n)), SPF: O(log(n)) per query after O(n log log n) preprocessing

---

## 8. Number of Divisors

```python
def count_divisors(n):
    count = 1
    d = 2
    while d * d <= n:
        exp = 0
        while n % d == 0:
            exp += 1
            n //= d
        if exp > 0:
            count *= (exp + 1)
        d += 1
    if n > 1:
        count *= 2
    return count

print(count_divisors(360))  # 24
# 360 = 2^3 * 3^2 * 5^1
# divisors = (3+1)(2+1)(1+1) = 24
```

### Using Prime Factorization
```python
from math import prod

def count_divisors_from_factors(factors):
    """Given {prime: exponent} dict, compute number of divisors."""
    return prod(exp + 1 for exp in factors.values())
```
**Time Complexity:** O(sqrt(n))

---

## 9. Sum of Divisors

```python
def sum_of_divisors(n):
    total = 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            power_sum = 1
            power_d = 1
            while n % d == 0:
                power_d *= d
                power_sum += power_d
                n //= d
            total *= power_sum
        d += 1
    if n > 1:
        total *= (1 + n)
    return total

print(sum_of_divisors(28))  # 56 (1+2+4+7+14+28)
```
**Time Complexity:** O(sqrt(n))

---

## 10. Factorial Computation

### Basic
```python
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print(factorial(10))  # 3628800
```

### Factorial Modulo M
```python
def factorial_mod(n, mod):
    result = 1
    for i in range(2, n + 1):
        result = result * i % mod
    return result

print(factorial_mod(10, 10**9 + 7))  # 3628800
```

### Precompute Factorials
```python
def precompute_factorials(n, mod):
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    return fact

fact = precompute_factorials(10**6, 10**9 + 7)
```
**Time Complexity:** O(n)

---

## 11. nCr (Combination)

### Basic (for small n)
```python
def nCr(n, r):
    if r > n:
        return 0
    r = min(r, n - r)
    result = 1
    for i in range(r):
        result = result * (n - i) // (i + 1)
    return result

print(nCr(10, 3))  # 120
```

### nCr with Modular Arithmetic
```python
def power_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = result * base % mod
        exp //= 2
        base = base * base % mod
    return result

def nCr_mod(n, r, mod):
    """nCr mod p using Fermat's Little Theorem."""
    if r > n:
        return 0
    r = min(r, n - r)

    # Precompute factorials
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod

    # nCr = fact[n] / (fact[r] * fact[n-r])
    numerator = fact[n]
    denominator = fact[r] * fact[n - r] % mod
    return numerator * power_mod(denominator, mod - 2, mod) % mod

print(nCr_mod(10, 3, 10**9 + 7))  # 120
```

### Precompute nCr Table (Pascal's Triangle)
```python
def build_nCr_table(n, mod):
    C = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % mod
    return C
```
**Time Complexity:** Basic: O(r), Modular: O(n), Table: O(n²)

---

## 12. Fibonacci Numbers

### Basic (DP)
```python
def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

print(fibonacci(10))  # 55
```
**Time Complexity:** O(n)

### Matrix Exponentiation (O(log n))
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
    result = [[1, 0], [0, 1]]  # Identity matrix
    while p > 0:
        if p % 2 == 1:
            result = matrix_mult(result, M, mod)
        M = matrix_mult(M, M, mod)
        p //= 2
    return result

def fibonacci_matrix(n, mod=None):
    """Compute nth Fibonacci number using matrix exponentiation."""
    if n <= 1:
        return n
    M = [[1, 1], [1, 0]]
    result = matrix_power(M, n, mod)
    return result[0][1]

print(fibonacci_matrix(10))  # 55
print(fibonacci_matrix(10**18, 10**9 + 7))  # Works for huge n!
```
**Time Complexity:** O(log n) for any n

---

## 13. Catalan Numbers

The nth Catalan number: C(n) = C(2n, n) / (n + 1)

```python
def catalan(n):
    """Compute nth Catalan number."""
    if n <= 1:
        return 1
    # C(n) = C(2n, n) / (n+1)
    result = 1
    for i in range(n):
        result = result * (2 * n - i) // (i + 1)
    return result // (n + 1)

# First 10 Catalan numbers: 1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862
for i in range(10):
    print(f"C({i}) = {catalan(i)}")
```

### Catalan with Modular Arithmetic
```python
def power_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = result * base % mod
        exp //= 2
        base = base * base % mod
    return result

def catalan_mod(n, mod):
    """nth Catalan number mod p."""
    # C(n) = C(2n, n) / (n+1)
    # = fact[2n] * inv(fact[n]) * inv(fact[n]) * inv(n+1)

    fact = [1] * (2 * n + 1)
    for i in range(1, 2 * n + 1):
        fact[i] = fact[i - 1] * i % mod

    num = fact[2 * n]
    den = fact[n] * fact[n] % mod
    den = den * (n + 1) % mod

    return num * power_mod(den, mod - 2, mod) % mod

print(catalan_mod(5, 10**9 + 7))  # 42
```

### Applications of Catalan Numbers
- Number of valid bracket sequences with n pairs
- Number of full binary trees with n+1 leaves
- Number of ways to triangulate a convex polygon
- Number of monotonic paths in nxn grid that don't cross diagonal

---

## Quick Reference: When to Use What

| Problem | Algorithm | Complexity |
|---------|-----------|------------|
| GCD of two numbers | Euclidean | O(log(min(a,b))) |
| LCM of two numbers | GCD formula | O(log(min(a,b))) |
| All primes ≤ N | Sieve of Eratosthenes | O(N log log N) |
| Primes in [L,R] | Segmented Sieve | O((R-L) log log R) |
| Is n prime? (n≤10^12) | Trial Division | O(sqrt(n)) |
| Is n prime? (large) | Miller-Rabin | O(k log²n) |
| Factorize n | Trial Division | O(sqrt(n)) |
| Count divisors | From factorization | O(sqrt(n)) |
| Fibonacci(n) | Matrix Exponentiation | O(log n) |
| nCr mod p | Fermat's Little Theorem | O(n) |
| Catalan numbers | Formula | O(n) |
