# Number Theory Patterns for Infosys SP DSE

## 1. Euler's Totient Function

**φ(n)** = count of integers from 1 to n that are coprime with n.

**Formula:** If n = p1^a1 * p2^a2 * ... * pk^ak, then
φ(n) = n * (1 - 1/p1) * (1 - 1/p2) * ... * (1 - 1/pk)

### Basic Implementation
```python
def euler_totient(n):
    """Compute φ(n) using prime factorization."""
    result = n
    p = 2
    temp = n

    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1

    if temp > 1:
        result -= result // temp

    return result

print(euler_totient(12))  # 4 (numbers: 1, 5, 7, 11)
print(euler_totient(7))   # 6 (all numbers 1-6 since 7 is prime)
print(euler_totient(1))   # 1
```
**Time Complexity:** O(sqrt(n))

### Sieve for All Totients up to N
```python
def euler_totient_sieve(n):
    """Compute φ(i) for all i from 1 to n using modified sieve."""
    phi = list(range(n + 1))  # phi[i] = i initially

    for i in range(2, n + 1):
        if phi[i] == i:  # i is prime
            for j in range(i, n + 1, i):
                phi[j] -= phi[j] // i

    return phi

phi = euler_totient_sieve(20)
for i in range(1, 21):
    print(f"φ({i}) = {phi[i]}")
# φ(1)=1, φ(2)=1, φ(3)=2, φ(4)=2, φ(5)=4, φ(6)=2, φ(7)=6, φ(8)=4, ...
```
**Time Complexity:** O(n log log n)

### Applications of Euler's Totient
```python
def euler_totient(n):
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

# Application 1: Count coprime pairs
def count_coprime_pairs(n):
    """Count pairs (i,j) where 1 <= i < j <= n and gcd(i,j) = 1."""
    total = 0
    for i in range(1, n + 1):
        total += euler_totient(i)
    return total

print(count_coprime_pairs(10))  # 33

# Application 2: a^φ(n) ≡ 1 (mod n) when gcd(a,n) = 1
# Generalization of Fermat's Little Theorem (Euler's Theorem)
```

---

## 2. Chinese Remainder Theorem (CRT)

Solve system of congruences when moduli are pairwise coprime:
```
x ≡ a1 (mod m1)
x ≡ a2 (mod m2)
...
x ≡ ak (mod mk)
```

Result: x ≡ a (mod M) where M = m1 * m2 * ... * mk

### Implementation
```python
from math import prod

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        return None
    return x % m

def chinese_remainder_theorem(remainders, moduli):
    """
    Solve system of congruences:
    x ≡ remainders[i] (mod moduli[i])
    All moduli must be pairwise coprime.
    """
    M = prod(moduli)
    result = 0

    for i in range(len(moduli)):
        Mi = M // moduli[i]
        yi = mod_inverse(Mi, moduli[i])
        result += remainders[i] * Mi * yi

    return result % M

# Example: Find x such that:
# x ≡ 2 (mod 3)
# x ≡ 3 (mod 5)
# x ≡ 2 (mod 7)
remainders = [2, 3, 2]
moduli = [3, 5, 7]
print(chinese_remainder_theorem(remainders, moduli))  # 23
# 23 % 3 = 2 ✓
# 23 % 5 = 3 ✓
# 23 % 7 = 2 ✓
```

### CRT with Non-Coprime Moduli
```python
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def crt_two(a1, m1, a2, m2):
    """Solve x ≡ a1 (mod m1) and x ≡ a2 (mod m2).
    Works even when gcd(m1, m2) ≠ 1."""
    from math import gcd

    g = gcd(m1, m2)
    if (a2 - a1) % g != 0:
        return None  # No solution exists

    lcm = m1 * m2 // g
    _, p, _ = extended_gcd(m1 // g, m2 // g)
    x = (a1 + m1 * (p * ((a2 - a1) // g) % (m2 // g))) % lcm
    return x % lcm

# Example with non-coprime moduli
print(crt_two(2, 4, 3, 6))  # x ≡ 2 (mod 4) and x ≡ 3 (mod 6)
# Solution: x = 14 (14 % 4 = 2, 14 % 6 = 3) or x ≡ 14 (mod 12)
```
**Time Complexity:** O(k * log(max(moduli))) for k congruences

---

## 3. Lucas Theorem

Compute C(n, r) mod p for large n, r where p is small prime.

**Lucas Theorem:** If n = n0 + n1*p + n2*p² + ... and r = r0 + r1*p + r2*p² + ...
then C(n,r) ≡ C(n0,r0) * C(n1,r1) * C(n2,r2) * ... (mod p)

```python
MOD = 10**9 + 7

def nCr_small(n, r, p):
    """Compute C(n,r) mod p for small n, r."""
    if r > n or r < 0:
        return 0
    r = min(r, n - r)
    result = 1
    for i in range(r):
        result = result * (n - i) // (i + 1)
    return result % p

def lucas_theorem(n, r, p):
    """Compute C(n,r) mod p using Lucas Theorem.
    p must be prime. Works for very large n, r."""
    result = 1
    while n > 0 or r > 0:
        ni = n % p
        ri = r % p
        if ri > ni:
            return 0
        result = result * nCr_small(ni, ri, p) % p
        n //= p
        r //= p
    return result

# Compute C(1000000000, 500000000) mod 7
print(lucas_theorem(10**9, 5*10**8, 7))  # Works!

# Compare with direct computation (infeasible for large values)
print(nCr_small(10, 3, 7))  # 120 % 7 = 1
print(lucas_theorem(10, 3, 7))  # Same result
```
**Time Complexity:** O(log_p(n) * p) where p is the prime modulus

### Precompute Small nCr Table for Lucas
```python
def build_nCr_prime_table(p):
    """Build nCr table for 0 <= n,r < p mod p."""
    C = [[0] * p for _ in range(p)]
    for i in range(p):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % p
    return C

def lucas_theorem_fast(n, r, p, C_table):
    """Lucas theorem with precomputed table."""
    result = 1
    while n > 0 or r > 0:
        ni, ri = n % p, r % p
        if ri > ni:
            return 0
        result = result * C_table[ni][ri] % p
        n //= p
        r //= p
    return result

# Precompute for p=7
C7 = build_nCr_prime_table(7)
print(lucas_theorem_fast(10**9, 5*10**8, 7, C7))
```

---

## 4. Base Conversion

```python
def to_base(n, base):
    """Convert decimal number n to given base (as string)."""
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        digits.append(str(n % base))
        n //= base
    return ''.join(reversed(digits))

def from_base(s, base):
    """Convert number in given base to decimal."""
    result = 0
    for c in s:
        result = result * base + int(c)
    return result

# Examples
print(to_base(42, 2))    # "101010"
print(to_base(42, 8))    # "52"
print(to_base(42, 16))   # "2a"
print(from_base("101010", 2))  # 42
print(from_base("52", 8))      # 42
```

### Base Conversion with Arbitrary Digits
```python
def to_base_custom(n, base, digits="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    """Convert n to given base using custom digit characters."""
    if n == 0:
        return digits[0]
    result = []
    while n > 0:
        result.append(digits[n % base])
        n //= base
    return ''.join(reversed(result))

print(to_base_custom(255, 16))  # "FF"
print(to_base_custom(1000, 36))  # "RS"
```

---

## 5. Digit Manipulation Problems

### Sum of Digits
```python
def digit_sum(n):
    """Compute sum of digits of n."""
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total

# Or using string conversion:
def digit_sum_str(n):
    return sum(int(d) for d in str(abs(n)))

print(digit_sum(12345))  # 15
```

### Product of Digits
```python
def digit_product(n):
    """Compute product of digits of n."""
    if n == 0:
        return 0
    result = 1
    while n > 0:
        result *= n % 10
        n //= 10
    return result

print(digit_product(12345))  # 120
```

### Count Digits
```python
def count_digits(n):
    """Count number of digits in n."""
    if n == 0:
        return 1
    count = 0
    n = abs(n)
    while n > 0:
        count += 1
        n //= 10
    return count

# Or using math:
import math
def count_digits_math(n):
    if n == 0:
        return 1
    return int(math.log10(abs(n))) + 1

print(count_digits(12345))  # 5
```

### Reverse Digits
```python
def reverse_digits(n):
    """Reverse the digits of n."""
    reversed_num = 0
    sign = 1 if n >= 0 else -1
    n = abs(n)

    while n > 0:
        reversed_num = reversed_num * 10 + n % 10
        n //= 10

    return sign * reversed_num

print(reverse_digits(12345))  # 54321
print(reverse_digits(-12345))  # -54321
```

### Check Palindrome
```python
def is_palindrome_number(n):
    """Check if n is a palindrome."""
    if n < 0:
        return False
    original = n
    reversed_num = 0
    while n > 0:
        reversed_num = reversed_num * 10 + n % 10
        n //= 10
    return original == reversed_num

print(is_palindrome_number(12321))  # True
print(is_palindrome_number(12345))  # False
```

### Digit DP Template
```python
def count_numbers_with_property(n, property_check):
    """Template for digit DP problems."""
    digits = [int(d) for d in str(n)]
    length = len(digits)

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(pos, tight, state):
        """
        pos: current digit position
        tight: whether we're still bounded by n
        state: whatever state we need to track
        """
        if pos == length:
            return 1 if property_check(state) else 0

        limit = digits[pos] if tight else 9
        result = 0

        for d in range(0, limit + 1):
            new_tight = tight and (d == limit)
            new_state = update_state(state, d)
            result += dp(pos + 1, new_tight, new_state)

        return result

    return dp(0, True, initial_state)
```

---

## 6. Check if Number is Palindrome in All Bases

```python
def is_palindrome_in_base(n, base):
    """Check if n is palindrome when written in given base."""
    if n == 0:
        return True
    digits = []
    while n > 0:
        digits.append(n % base)
        n //= base
    return digits == digits[::-1]

def palindrome_in_all_bases(n, max_base=10):
    """Check if n is palindrome in all bases from 2 to max_base."""
    for base in range(2, max_base + 1):
        if not is_palindrome_in_base(n, base):
            return False
    return True

# Example: Numbers that are palindrome in multiple bases
print(f"5 is palindrome in base 2: {is_palindrome_in_base(5, 2)}")   # True (101)
print(f"5 is palindrome in base 3: {is_palindrome_in_base(5, 3)}")   # True (12)
print(f"5 is palindrome in base 4: {is_palindrome_in_base(5, 4)}")   # True (11)

# Find all numbers up to N that are palindromes in all bases 2-10
def find_universal_palindromes(limit):
    results = []
    for n in range(1, limit + 1):
        if palindrome_in_all_bases(n, 10):
            results.append(n)
    return results

print(find_universal_palindromes(100))  # [1]
```

### Alternative: Check All Bases Efficiently
```python
def is_palindrome_all_bases(n):
    """Check if n is palindrome in ALL bases b >= 2.
    Only 1, 2, 3, 4, 6 are palindromes in all bases."""
    if n <= 1:
        return True

    # For n >= 5, it's impossible to be palindrome in all bases
    # Proof: In base n-1, n = "11" (palindrome)
    # In base n, n = "10" (not palindrome)
    # So for n >= 3, check only up to base n-1
    if n >= 5:
        return False

    for base in range(2, n):
        if not is_palindrome_in_base(n, base):
            return False
    return True
```

---

## 7. Additional Number Theory Patterns

### GCD-Based Patterns
```python
from math import gcd

def count_pairs_with_gcd(arr, target_gcd):
    """Count pairs (i,j) where gcd(arr[i], arr[j]) = target_gcd."""
    from collections import Counter

    # Count multiples of target_gcd
    multiples = Counter()
    for x in arr:
        if x % target_gcd == 0:
            multiples[x // target_gcd] += 1

    # Use inclusion-exclusion on multiples
    distinct_multiples = sorted(multiples.keys(), reverse=True)
    count = {}

    for m in distinct_multiples:
        total = multiples[m]
        # Subtract pairs where gcd is a multiple of m
        for multiple in range(2 * m, distinct_multiples[0] + 1, m):
            if multiple in count:
                total -= count[multiple]
        count[m] = total

    return count.get(1, 0)

arr = [2, 4, 6, 8, 10]
print(count_pairs_with_gcd(arr, 2))  # Count pairs with gcd = 2
```

### Number Theory in Arrays
```python
from collections import Counter

def max_gcd_pair(arr):
    """Find maximum GCD among all pairs in array."""
    max_val = max(arr)

    # Count multiples of each number
    count = [0] * (max_val + 1)
    for x in arr:
        count[x] += 1

    # Check from largest to smallest
    for g in range(max_val, 0, -1):
        multiples = 0
        for j in range(g, max_val + 1, g):
            multiples += count[j]
        if multiples >= 2:
            return g

    return 1

print(max_gcd_pair([2, 4, 6, 8, 10]))  # 5 (pair: 10, 5)
```

### Digit Sum Patterns
```python
def digit_root(n):
    """Compute digit root (repeatedly sum digits until single digit).
    Formula: digit_root(n) = 1 + (n-1) % 9 for n > 0"""
    if n == 0:
        return 0
    return 1 + (n - 1) % 9

for i in range(1, 20):
    print(f"digit_root({i}) = {digit_root(i)}")
# 1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1
```

---

## Quick Reference

| Concept | Formula/Method | Use Case |
|---------|---------------|----------|
| Euler's Totient | φ(n) = n * Π(1-1/p) | Count coprime numbers |
| CRT | x ≡ a (mod M) | Solve simultaneous congruences |
| Lucas Theorem | C(n,r) mod p | Large nCr with small prime mod |
| Base Conversion | Repeated division | Representation problems |
| Digit Manipulation | Mod 10, // 10 | Number properties |
| Digit Root | 1 + (n-1) % 9 | Repeated digit sum |
| Palindrome Check | Reverse and compare | Number symmetry |
