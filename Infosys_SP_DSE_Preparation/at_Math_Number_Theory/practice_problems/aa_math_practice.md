# Math & Number Theory Practice Problems for Infosys SP DSE

---

## EASY PROBLEMS

---

### Problem 1: Power of Two

**Statement:** Given an integer n, return True if it is a power of two.

**Approach:** A number is a power of two if it has exactly one set bit. Use the property: `n & (n-1) == 0`.

```python
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

# Alternative: count set bits
def is_power_of_two_v2(n):
    return n > 0 and bin(n).count('1') == 1

print(is_power_of_two(16))  # True
print(is_power_of_two(18))  # False
```
**Time Complexity:** O(1)
**Space Complexity:** O(1)

---

### Problem 2: Fibonacci Number

**Statement:** Return the nth Fibonacci number where F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).

**Approach:** Iterative DP with O(1) space.

```python
def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

print(fibonacci(10))  # 55
print(fibonacci(0))   # 0
print(fibonacci(1))   # 1
```
**Time Complexity:** O(n)
**Space Complexity:** O(1)

---

### Problem 3: Factorial Trailing Zeroes

**Statement:** Given n, return the number of trailing zeroes in n!.

**Approach:** Count factors of 5 in n!. Each factor of 5 pairs with a factor of 2 to make a trailing zero.

```python
def trailing_zeroes(n):
    count = 0
    while n >= 5:
        n //= 5
        count += n
    return count

print(trailing_zeroes(25))  # 6 (25! has 6 trailing zeroes)
print(trailing_zeroes(10))  # 2
```
**Time Complexity:** O(log₅ n)
**Space Complexity:** O(1)

---

### Problem 4: Count Primes

**Statement:** Count the number of prime numbers less than n.

**Approach:** Sieve of Eratosthenes.

```python
def count_primes(n):
    if n < 3:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n, i):
                is_prime[j] = False

    return sum(is_prime)

print(count_primes(10))   # 4 (primes: 2,3,5,7)
print(count_primes(20))   # 8
```
**Time Complexity:** O(n log log n)
**Space Complexity:** O(n)

---

### Problem 5: Happy Number

**Statement:** A happy number is one where repeatedly replacing it with the sum of squares of its digits eventually reaches 1. Determine if n is happy.

**Approach:** Use Floyd's cycle detection or a set to detect cycles.

```python
def is_happy(n):
    def get_next(num):
        total = 0
        while num > 0:
            total += (num % 10) ** 2
            num //= 10
        return total

    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = get_next(n)
    return n == 1

print(is_happy(19))  # True (19->82->68->100->1)
print(is_happy(2))   # False
```
**Time Complexity:** O(log n)
**Space Complexity:** O(log n)

---

## MEDIUM PROBLEMS

---

### Problem 6: Modular Arithmetic for Large Computations

**Statement:** Compute (a^b * c^d) % mod for very large values.

**Approach:** Use binary exponentiation (or Python's built-in pow with 3 args).

```python
def compute_modular(a, b, c, d, mod):
    """Compute (a^b * c^d) % mod."""
    return pow(a, b, mod) * pow(c, d, mod) % mod

# Or manually:
def compute_modular_manual(a, b, c, d, mod):
    def power_mod(base, exp, mod):
        result = 1
        base %= mod
        while exp > 0:
            if exp & 1:
                result = result * base % mod
            exp >>= 1
            base = base * base % mod
        return result

    part1 = power_mod(a, b, mod)
    part2 = power_mod(c, d, mod)
    return part1 * part2 % mod

print(compute_modular(2, 100, 3, 50, 10**9 + 7))
```
**Time Complexity:** O(log b + log d)
**Space Complexity:** O(1)

---

### Problem 7: Nth Fibonacci Number (Matrix Exponentiation)

**Statement:** Compute the nth Fibonacci number for very large n (up to 10^18), modulo 10^9+7.

**Approach:** Matrix exponentiation in O(log n).

```python
MOD = 10**9 + 7

def matrix_mult(A, B, mod):
    return [
        [(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % mod,
         (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % mod],
        [(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % mod,
         (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % mod]
    ]

def matrix_power(M, p, mod):
    result = [[1, 0], [0, 1]]
    while p > 0:
        if p & 1:
            result = matrix_mult(result, M, mod)
        M = matrix_mult(M, M, mod)
        p >>= 1
    return result

def fibonacci(n, mod=MOD):
    if n <= 1:
        return n
    M = [[1, 1], [1, 0]]
    result = matrix_power(M, n, mod)
    return result[0][1]

print(fibonacci(10))          # 55
print(fibonacci(10**18, MOD)) # Works for huge n!
```
**Time Complexity:** O(log n)
**Space Complexity:** O(1)

---

### Problem 8: Combination Sum IV

**Statement:** Given an array of distinct integers nums and a target integer target, return the number of combinations that add up to target. Order matters.

**Approach:** Bottom-up DP. For each target value, sum up ways to reach it from each num.

```python
def combination_sum4(nums, target):
    dp = [0] * (target + 1)
    dp[0] = 1

    for t in range(1, target + 1):
        for num in nums:
            if t >= num:
                dp[t] += dp[t - num]

    return dp[target]

# Example
print(combination_sum4([1, 2, 3], 4))  # 7
# Combinations: (1,1,1,1), (1,1,2), (1,2,1), (1,3), (2,1,1), (2,2), (3,1)
```
**Time Complexity:** O(target * len(nums))
**Space Complexity:** O(target)

### Variant with Modular Arithmetic
```python
MOD = 10**9 + 7

def combination_sum4_mod(nums, target):
    dp = [0] * (target + 1)
    dp[0] = 1

    for t in range(1, target + 1):
        for num in nums:
            if t >= num:
                dp[t] = (dp[t] + dp[t - num]) % MOD

    return dp[target]

print(combination_sum4_mod([1, 2, 3], 4))  # 7
```
**Time Complexity:** O(target * len(nums))
**Space Complexity:** O(target)

---

### Problem 9: Decode Ways

**Statement:** A message consisting of letters A-Z is encoded as digits ('A'=1, 'B'=2, ..., 'Z'=26). Given a string of digits, return the number of ways to decode it.

**Approach:** DP. At each position, check if single digit (1-9) and double digit (10-26) are valid.

```python
def num_decodings(s):
    if not s or s[0] == '0':
        return 0

    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1

    for i in range(2, n + 1):
        # Single digit decode
        if 1 <= int(s[i-1]) <= 9:
            dp[i] += dp[i-1]

        # Double digit decode
        two_digit = int(s[i-2:i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i-2]

    return dp[n]

print(num_decodings("12"))   # 2 ("AB" or "L")
print(num_decodings("226"))  # 3 ("BZ", "VF", "BBF")
print(num_decodings("06"))   # 0 (invalid)
```
**Time Complexity:** O(n)
**Space Complexity:** O(n) (can be optimized to O(1))

### Space-Optimized Version
```python
def num_decodings_optimized(s):
    if not s or s[0] == '0':
        return 0

    prev2, prev1 = 1, 1

    for i in range(1, len(s)):
        curr = 0
        if 1 <= int(s[i]) <= 9:
            curr += prev1
        if 10 <= int(s[i-1:i+1]) <= 26:
            curr += prev2
        prev2, prev1 = prev1, curr

    return prev1

print(num_decodings_optimized("226"))  # 3
```
**Time Complexity:** O(n)
**Space Complexity:** O(1)

---

### Problem 10: Unique Paths

**Statement:** Count unique paths from top-left to bottom-right of an m×n grid (can only move right or down).

**Approach:** Combinatorics. Answer is C(m+n-2, m-1).

```python
MOD = 10**9 + 7

def unique_paths(m, n):
    """Count paths using combinatorics."""
    # C(m+n-2, m-1)
    total = m + n - 2
    r = min(m - 1, n - 1)

    result = 1
    for i in range(r):
        result = result * (total - i) // (i + 1)
    return result

print(unique_paths(3, 7))  # 28
print(unique_paths(3, 3))  # 6

# With modular arithmetic
def unique_paths_mod(m, n, mod=MOD):
    def power_mod(base, exp, mod):
        result = 1
        base %= mod
        while exp > 0:
            if exp & 1:
                result = result * base % mod
            exp >>= 1
            base = base * base % mod
        return result

    total = m + n - 2
    r = min(m - 1, n - 1)

    fact = [1] * (total + 1)
    for i in range(1, total + 1):
        fact[i] = fact[i - 1] * i % mod

    return fact[total] * power_mod(fact[r], mod - 2, mod) % mod * power_mod(fact[total - r], mod - 2, mod) % mod

print(unique_paths_mod(3, 7))
```
**Time Complexity:** O(min(m, n))
**Space Complexity:** O(1) (basic) or O(m+n) (modular)

---

## HARD PROBLEMS

---

### Problem 11: Count Primes (Segmented Sieve)

**Statement:** Count primes in a range [L, R] where R can be up to 10^12 but R-L ≤ 10^6.

**Approach:** Segmented Sieve.

```python
import math

def segmented_sieve_count(low, high):
    """Count primes in range [low, high]."""
    if high < 2:
        return 0
    low = max(low, 2)

    # Get primes up to sqrt(high)
    limit = int(math.isqrt(high)) + 1
    is_prime_small = [True] * (limit + 1)
    is_prime_small[0] = is_prime_small[1] = False

    basic_primes = []
    for i in range(2, limit + 1):
        if is_prime_small[i]:
            basic_primes.append(i)
            for j in range(i * i, limit + 1, i):
                is_prime_small[j] = False

    # Segmented sieve
    size = high - low + 1
    is_prime_range = [True] * size

    for p in basic_primes:
        start = max(p * p, ((low + p - 1) // p) * p)
        for j in range(start, high + 1, p):
            is_prime_range[j - low] = False

    return sum(is_prime_range)

print(segmented_sieve_count(10, 50))      # 11
print(segmented_sieve_count(10**9, 10**9 + 1000))  # Count primes in range
```
**Time Complexity:** O((R-L) log log R + √R log log √R)
**Space Complexity:** O(R-L + √R)

---

### Problem 12: Largest Component Size by Common Factor

**Statement:** Given an array of unique integers, connect two integers if they share a common factor greater than 1. Return the size of the largest connected component.

**Approach:** Union-Find with prime factorization. Connect all elements sharing a prime factor.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

    def get_size(self, x):
        return self.size[self.find(x)]

def largest_component_size(nums):
    if not nums:
        return 0

    max_val = max(nums)
    uf = UnionFind(max_val + 1)

    def get_prime_factors(n):
        factors = set()
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.add(d)
                n //= d
            d += 1
        if n > 1:
            factors.add(n)
        return factors

    # Map each number to its first prime factor
    # and union all numbers sharing the same prime factor
    prime_to_num = {}

    for num in nums:
        factors = get_prime_factors(num)
        first_factor = min(factors)
        for f in factors:
            if f in prime_to_num:
                uf.union(num, prime_to_num[f])
            else:
                prime_to_num[f] = num

    return max(uf.get_size(num) for num in nums)

print(largest_component_size([4, 6, 15, 35]))  # 4
print(largest_component_size([20, 50, 9, 63]))  # 2
```
**Time Complexity:** O(n * √max_val)
**Space Complexity:** O(max_val)

---

### Problem 13: Orderly Queue

**Statement:** You have a string s and an integer k. You can perform two operations: if k=1, move the first character to the end; if k=2, swap the first two characters. Return the lexicographically smallest string possible.

**Approach:**
- If k=1: try all rotations, pick smallest
- If k=2: any permutation is reachable (for k≥2), so just sort

```python
def orderly_queue(s, k):
    if k == 1:
        # Try all rotations
        min_str = s
        rotated = s
        for _ in range(len(s) - 1):
            rotated = rotated[1:] + rotated[0]
            min_str = min(min_str, rotated)
        return min_str
    else:
        # k >= 2: we can generate any permutation
        return ''.join(sorted(s))

print(orderly_queue("cba", 1))  # "acb"
print(orderly_queue("baaca", 3))  # "aaabc"
```
**Time Complexity:** k=1: O(n²), k≥2: O(n log n)
**Space Complexity:** O(n)

---

### Problem 14: Max Points on a Line

**Statement:** Given an array of points, find the maximum number of points that lie on the same straight line.

**Approach:** For each point, compute slopes to all other points. Use a hash map to count points with same slope.

```python
from collections import defaultdict
from math import gcd

def max_points(points):
    if len(points) <= 2:
        return len(points)

    result = 0

    for i in range(len(points)):
        slopes = defaultdict(int)
        duplicates = 1

        for j in range(i + 1, len(points)):
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]

            if dx == 0 and dy == 0:
                duplicates += 1
                continue

            # Normalize slope using GCD
            g = gcd(dx, dy)
            dx //= g
            dy //= g

            # Ensure consistent representation
            if dx < 0:
                dx, dy = -dx, -dy
            if dx == 0:
                dy = 1
            if dy == 0:
                dx = 1

            slopes[(dx, dy)] += 1

        current_max = duplicates
        for count in slopes.values():
            current_max = max(current_max, count + duplicates)

        result = max(result, current_max)

    return result

print(max_points([[1,1],[2,2],[3,3]]))  # 3
print(max_points([[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]))  # 4
```
**Time Complexity:** O(n²)
**Space Complexity:** O(n)

---

### Problem 15: Integer Break

**Statement:** Given an integer n, break it into the sum of k positive integers (k ≥ 2) to maximize the product of these integers.

**Approach:** Greedy. Use as many 3s as possible (since 3 gives maximum product per unit).

```python
def integer_break(n):
    if n == 2:
        return 1
    if n == 3:
        return 2

    result = 1
    while n > 4:
        result *= 3
        n -= 3

    result *= n
    return result

print(integer_break(2))   # 1
print(integer_break(10))  # 36 (3+3+4 = 10, 3*3*4 = 36)
```

### DP Solution
```python
def integer_break_dp(n):
    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        for j in range(1, i):
            # j * max(dp[i-j], i-j)
            dp[i] = max(dp[i], j * max(dp[i - j], i - j))

    return dp[n]

print(integer_break_dp(10))  # 36
```
**Time Complexity:** Greedy: O(n), DP: O(n²)
**Space Complexity:** Greedy: O(1), DP: O(n)

---

## Summary: Key Patterns

| Pattern | Problems | Key Algorithm |
|---------|----------|---------------|
| Bit Manipulation | Power of Two | n & (n-1) == 0 |
| Fibonacci | Fibonacci Number | Iterative / Matrix Exponentiation |
| Factor Counting | Trailing Zeroes | Count factors of 5 |
| Sieve | Count Primes | Sieve of Eratosthenes |
| Cycle Detection | Happy Number | Floyd's / HashSet |
| Modular Arithmetic | Large Computations | Binary Exponentiation |
| Matrix Exponentiation | Nth Fibonacci | O(log n) matrix power |
| DP | Combination Sum IV, Decode Ways | Bottom-up DP |
| Combinatorics | Unique Paths | nCr computation |
| Segmented Sieve | Count Primes Range | Segmented approach |
| Union-Find | Largest Component | Prime factorization + UF |
| Greedy | Integer Break | Use as many 3s as possible |
| Geometry | Max Points on Line | Slope hash map |
