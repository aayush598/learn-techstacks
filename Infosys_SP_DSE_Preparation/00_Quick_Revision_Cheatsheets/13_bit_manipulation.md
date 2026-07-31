# 13. Bit Manipulation

Exam-oriented Python syntax for every bit trick used in coding rounds. All snippets are copy-paste ready.

## Core operators

| Operator | Name | Python | Notes |
|---|---|---|---|
| AND | bitwise and | `a & b` | |
| OR | bitwise or | `a \| b` | |
| XOR | exclusive or | `a ^ b` | `x ^ x == 0`, `x ^ 0 == x` |
| NOT | complement | `~a` | `~a == -(a+1)` — NOT does NOT flip all 32 bits like C |
| << | left shift | `a << i` | multiply by `2**i` |
| >> | right shift | `a >> i` | floor divide by `2**i` |

```python
a, b, i = 13, 7, 2          # a = 1101, b = 0111
print(a & b)                # 5   (0101) AND
print(a | b)                # 15  (1111) OR
print(a ^ b)                # 10  (1010) XOR
print(~a)                   # -14 (NOT)
print(a << i)               # 52  (110100)
print(a >> i)               # 3   (11)
```

## Bit set / clear / toggle / check

```python
def get_bit(n, i):          # is the i-th bit set?
    return (n >> i) & 1     # also (n & (1 << i)) != 0

def set_bit(n, i):          # force i-th bit to 1
    return n | (1 << i)

def clear_bit(n, i):        # force i-th bit to 0
    return n & ~(1 << i)

def toggle_bit(n, i):       # flip i-th bit
    return n ^ (1 << i)
```

```python
i = 2
n = 13                      # 1101, bits: bit3 bit2 bit1 bit0
print(get_bit(n, 3))        # 1
print(set_bit(n, 1))        # 15 -> 1111
print(clear_bit(n, 3))      # 5  -> 0101
print(toggle_bit(n, 0))     # 12 -> 1100
print(1 << i)               # 2**i
print(n << 2)               # n * 4  (multiply by power of two)
print(n >> 2)               # n // 4 (floor divide by power of two)
```

Complexity: O(1) each.

## Count set bits

```python
def count_set_bits(n):
    return bin(n).count('1')

# Brian Kernighan's algorithm — faster, loops only per set bit
def count_set_bits2(n):
    c = 0
    while n:
        n &= n - 1          # clears the lowest set bit
        c += 1
    return c

print(count_set_bits(13))   # 3
print(count_set_bits2(13))  # 3
```

Complexity: O(number of bits) for `bin().count`, O(k) where k = set-bit count for Kernighan.

## Lowest set bit

```python
def lowest_set_bit(n):
    return n & (-n)

print(lowest_set_bit(12))   # 4  -> 1100 & 0100
print(lowest_set_bit(16))   # 16 -> power of two gives itself
```

Complexity: O(1).

## Power of two

```python
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

print(is_power_of_two(1))     # True
print(is_power_of_two(1024))  # True
print(is_power_of_two(0))     # False
print(is_power_of_two(12))    # False
```

Complexity: O(1).

## XOR tricks

### Single number (every element appears twice, one appears once)

```python
def single_number(nums):
    x = 0
    for v in nums:
        x ^= v
    return x

print(single_number([4, 1, 2, 1, 2]))  # 4
```

Complexity: O(n) time, O(1) space.

### Missing number in [0..n]

```python
def missing_number(nums):
    n = len(nums)
    x = 0
    for i in range(n + 1):
        x ^= i
    for v in nums:
        x ^= v
    return x

print(missing_number([3, 0, 1]))               # 2
print(missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]))  # 8
```

Complexity: O(n) time, O(1) space.

### Two missing numbers (outline)

```python
def two_missing(nums, N):            # numbers 1..N, array holds N-2 of them
    total = N * (N + 1) // 2 - sum(nums)              # a + b
    sq = sum(i * i for i in range(1, N + 1)) - sum(x * x for x in nums)
    ab = (total * total - sq) // 2                    # a*b
    d = int((total * total - 4 * ab) ** 0.5)          # |a - b|
    a = (total - d) // 2
    b = total - a
    return sorted([a, b])

print(two_missing([1, 2, 4, 5], 6))  # [3, 6]
```

Complexity: O(N) time, O(1) space.

### XOR into two groups (two unique numbers)

```python
def two_single_numbers(nums):
    x = 0
    for v in nums:
        x ^= v                     # x = a ^ b (a, b unique)
    lb = x & (-x)                  # any set bit, a and b differ here
    a = b = 0
    for v in nums:
        if v & lb:
            a ^= v
        else:
            b ^= v
    return sorted([a, b])

print(two_single_numbers([1, 2, 1, 3, 2, 5]))  # [3, 5]
```

Complexity: O(n) time, O(1) space.

## Subsets via bitmask iteration

```python
def subsets(arr):
    res = []
    n = len(arr)
    for mask in range(1 << n):
        sub = [arr[i] for i in range(n) if mask & (1 << i)]
        res.append(sub)
    return res

print(subsets([1, 2, 3]))   # [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
```

Complexity: O(2^n * n) time, O(2^n * n) space.

## Bitmask DP basics

State is an integer `mask`; bit i of `mask` = 1 means element i is used.

```python
# subset sum: does any subset sum to target?
def subset_sum_exists(nums, target):
    sums = {0}
    for x in nums:
        sums |= {s + x for s in list(sums) if s + x <= target}
    return target in sums

print(subset_sum_exists([3, 34, 4, 12, 5, 2], 9))    # True
print(subset_sum_exists([3, 34, 4, 12, 5, 2], 30))   # False
```

```python
# TSP-style pattern: iterate over masks, extract lowest set bit
# lowest set bit index:  (mask & -mask).bit_length() - 1
# iterate over all submasks of a mask:
def submasks(mask):
    s = mask
    while s:
        yield s
        s = (s - 1) & mask
    yield 0

print(list(submasks(0b1101)))   # [13, 12, 9, 8, 5, 4, 1, 0]
```

Complexity: O(2^n * n) typical for bitmask DP (Hamiltonian path, TSP, assignments).

## Gray code

```python
def gray_code(n):
    return [i ^ (i >> 1) for i in range(1 << n)]

print(gray_code(3))   # [0, 1, 3, 2, 6, 7, 5, 4] — consecutive differ in 1 bit
```

Complexity: O(2^n) time and space.

## Reverse bits (32-bit)

```python
def reverse_bits(x):
    res = 0
    for _ in range(32):
        res = (res << 1) | (x & 1)
        x >>= 1
    return res

print(reverse_bits(43261596))  # 964176192
```

Complexity: O(32) = O(1) time, O(1) space.

## Sum without `+` operator (carry technique)

Works for non-negative ints directly. For negatives, Python ints are unbounded so
mask to 32 bits (two's complement) as shown:

```python
def add_without_plus(a, b):
    while b != 0:
        carry = (a & b) << 1    # carries that must be added at next position
        a = a ^ b               # sum without carries
        b = carry
    return a

print(add_without_plus(5, 7))   # 12
```

```python
# negative-safe variant (32-bit two's complement)
def add_without_plus32(a, b):
    MASK = 0xFFFFFFFF
    while b != 0:
        carry = (a & b) << 1
        a = (a ^ b) & MASK
        b = carry & MASK
    return a if a < 0x80000000 else a - 0x100000000

print(add_without_plus32(-5, 7))  # 2
print(add_without_plus32(-1, 1))  # 0
```

Complexity: O(number of bits) = O(1) amortized per standard int.

## Bit mask idioms (memorize)

| Goal | Expression |
|---|---|
| Set bit i | `n |= 1 << i` |
| Clear bit i | `n &= ~(1 << i)` |
| Toggle bit i | `n ^= 1 << i` |
| Check bit i | `n & (1 << i)` / `(n >> i) & 1` |
| Lowest set bit | `n & -n` |
| Clear lowest set bit | `n & (n - 1)` |
| Check power of two | `n > 0 and n & (n - 1) == 0` |
| Count bits | `bin(n).count('1')` |
| Isolate bit (0/1) | `(n >> i) & 1` |
| Divide/multiply by 2^k | `n >> k` / `n << k` |
| Mod power of two | `n & (2**k - 1)` (== n mod 2^k) |
