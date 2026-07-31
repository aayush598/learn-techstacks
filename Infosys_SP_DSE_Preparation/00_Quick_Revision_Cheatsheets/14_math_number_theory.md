# 14. Math & Number Theory

All essential math routines for coding rounds in exact, copy-paste ready Python.

## GCD and LCM

```python
import math

print(math.gcd(48, 36))   # 12 (fastest, use this)
print(math.lcm(4, 6))     # 12 (Python 3.9+)

# custom Euclidean (write this if asked to implement)
def gcd_custom(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a // gcd_custom(a, b) * b   # divide first to avoid overflow risk
```

Complexity: O(log(min(a, b))) time, O(1) space.

## Prime check

```python
def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

print(is_prime(2), is_prime(97), is_prime(91))  # True True False
```

Complexity: O(sqrt(n)) time, O(1) space.

## Sieve of Eratosthenes

```python
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return is_prime

is_prime = sieve(20)
print(is_prime[2], is_prime[19])   # True True
print(is_prime[1], is_prime[15])   # False False
```

Complexity: O(n log log n) time, O(n) space.

## Smallest prime factor sieve

```python
def smallest_prime_factor(n):
    spf = list(range(n + 1))
    for i in range(2, int(n ** 0.5) + 1):
        if spf[i] == i:                       # i is prime
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

spf = smallest_prime_factor(30)
print(spf[12])   # 2
print(spf[25])   # 5
print(spf[29])   # 29
```

Complexity: O(n log log n) time, O(n) space. Factorize any number in O(log n) by repeatedly dividing by `spf[n]`.

## Prime factorization (count dict)

```python
def prime_factorize(n):
    fac = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            fac[d] = fac.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2      # 2, 3, 5, 7, ... (skip evens after 2)
    if n > 1:
        fac[n] = fac.get(n, 0) + 1
    return fac

print(prime_factorize(84))   # {2: 2, 3: 1, 7: 1}
print(prime_factorize(29))   # {29: 1}
```

Complexity: O(sqrt(n)) time, O(number of distinct primes) space.

## Modular arithmetic

```python
MOD = 10 ** 9 + 7

# modular exponentiation — always use built-in pow
print(pow(2, 10, MOD))      # 1024
print(pow(2, 10, 1000))     # 24  (last three digits)

# modular inverse: pow(a, -1, mod) works when gcd(a, mod) == 1
print(pow(7, -1, 5))        # 3   (3 * 7 = 21 ≡ 1 mod 5)

# Fermat: when mod is prime, a^(mod-2) is the inverse
def mod_inverse_fermat(a, mod):
    return pow(a, mod - 2, mod)

print((mod_inverse_fermat(7, 5) * 7) % 5)  # 1
```

Complexity: O(log exp) time, O(1) space for `pow`.

## Fast exponentiation template (iterative)

```python
def fast_pow(base, exp, mod=None):
    result = 1
    b, e = base, exp
    while e:
        if e & 1:
            result = result * b % mod if mod else result * b
        b = b * b % mod if mod else b * b
        e >>= 1
    return result

print(fast_pow(2, 10))          # 1024
print(fast_pow(2, 10, 1000))    # 24
```

Complexity: O(log exp) time, O(1) space.

## nCr / nPr

```python
import math

print(math.comb(10, 3))     # 120  (no modulo, huge ints fine in Python)
print(math.perm(10, 3))     # 720

def nPr(n, r):
    return math.factorial(n) // math.factorial(n - r)
```

### nCr under a prime modulus with precomputed factorials

```python
MOD = 10 ** 9 + 7
MAXN = 10 ** 6

fact = [1] * (MAXN + 1)
for i in range(1, MAXN + 1):
    fact[i] = fact[i - 1] * i % MOD

inv_fact = [1] * (MAXN + 1)
inv_fact[MAXN] = pow(fact[MAXN], MOD - 2, MOD)          # Fermat inverse
for i in range(MAXN - 1, -1, -1):
    inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD

def nCr(n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD

print(nCr(5, 2))    # 10
print(nCr(10, 0))   # 1
```

Complexity: O(MAXN) precompute, O(1) per query, O(MAXN) space.

## Digit sum and reverse integer

```python
def digit_sum(n):
    return sum(map(int, str(n)))

print(digit_sum(1234))   # 10

def reverse_int(x):
    sign = -1 if x < 0 else 1
    x = abs(x)
    rev = 0
    while x:
        rev = rev * 10 + x % 10
        x //= 10
    return sign * rev

print(reverse_int(123))    # 321
print(reverse_int(-120))   # -21
```

Complexity: O(number of digits) time, O(1) space.

## Fibonacci fast doubling

```python
def fib_fast(n):
    """Returns (F(n), F(n+1))."""
    if n == 0:
        return (0, 1)
    a, b = fib_fast(n >> 1)
    c = a * ((b << 1) - a)
    d = a * a + b * b
    if n & 1:
        return (d, c + d)
    return (c, d)

print([fib_fast(i)[0] for i in range(10)])  # 0 1 1 2 3 5 8 13 21 34
print(fib_fast(50)[0])                       # 12586269025
```

Complexity: O(log n) time, O(log n) recursion stack.

## Catalan numbers

```python
import math

def catalan(n):
    return math.comb(2 * n, n) // (n + 1)

print([catalan(i) for i in range(6)])   # [1, 1, 2, 5, 14, 42]
# Counts: valid parentheses, BSTs with n nodes, triangulations, Dyck paths
```

Complexity: O(n) via `math.comb` (single binomial), or O(n) DP recurrence `C(n) = C(n-1) * 2*(2n-1)//(n+1)`.

## Random numbers

```python
import random

print(random.randint(1, 100))       # random int in [1, 100] inclusive
print(random.choice([1, 2, 3, 4]))  # random element
print(random.shuffle([1, 2, 3]))    # in-place shuffle (returns None)
print(random.sample(range(50), 5))  # 5 distinct elements
print(random.random())              # float in [0.0, 1.0)
```

## Floor division and rounding

```python
import math

print(7 // 3)         # 2
print(-7 // 3)        # -3   floor division rounds DOWN (towards -inf)
print(7 // -3)        # -3
print(math.floor(-7 / 3))  # -3
print(math.ceil(-7 / 3))   # -2
print(int(-7 / 3))         # -2   int() truncates towards zero — different!
print(round(2.5))          # 2    banker's rounding — avoid for ties
```

Watch out: `n // 10` with negative n gives `-3` for `-25 // 10`, which is floor,
not truncation. Use `int(n / 10)` if you want C-style truncation.

## Integer overflow is NOT an issue in Python

Python integers have arbitrary precision — no overflow, no wrap-around, no
signed/unsigned 32/64-bit limits.

```python
print(10 ** 100)                     # 1 followed by 100 zeros — works fine
print(2 ** 10000 // 7 % 12345)       # arbitrary precision arithmetic just works
```

But beware: big numbers are SLOWER. If a problem defines a MOD (usually
`10**9 + 7`), apply `% MOD` after every multiplication to keep numbers small.
In C++-style loop solutions written in Python, always reduce mod inside the
loop, never just at the end.
