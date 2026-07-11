# Power of Two / Four / Three — Complete Reference

---

## 1. Check Power of 2

A number is a power of 2 if it has exactly one set bit in binary.

**Key Insight:** `n & (n - 1)` clears the lowest set bit. If n is a power of 2,
it has only one set bit, so the result is 0.

**Proof:**
```
Powers of 2 in binary: 1, 10, 100, 1000, ...
n - 1 for a power of 2: 0, 01, 011, 0111, ...
n & (n-1): each pair has no overlapping 1-bits → result = 0

For non-powers of 2, n has ≥ 2 set bits, so n & (n-1) ≠ 0
(because n-1 only clears the lowest set bit, others remain).
```

```java
public boolean isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
```

**Edge Cases:**
- `n = 0`: `0 & (-1) = 0` but 0 is not a power of 2 → `n > 0` check handles this
- `n = 1`: `1 & 0 = 0` → true (2^0 = 1, conventionally a power of 2)
- `n = -8`: negative → false

**Test Cases:**
```
isPowerOfTwo(1)  → true  (2^0)
isPowerOfTwo(2)  → true  (2^1)
isPowerOfTwo(4)  → true  (2^2)
isPowerOfTwo(16) → true  (2^4)
isPowerOfTwo(6)  → false (110)
isPowerOfTwo(0)  → false
isPowerOfTwo(-2) → false
```

**Alternative (bit count):**
```java
public boolean isPowerOfTwoBitCount(int n) {
    return n > 0 && Integer.bitCount(n) == 1;
}
```

---

## 2. Check Power of 4

Powers of 4 are: 1, 4, 16, 64, 256, ...
In binary: 1, 100, 10000, 1000000, ...

**Properties:**
1. Must be a power of 2 (single set bit)
2. The set bit must be at an **even** position (0-indexed): bits 0, 2, 4, 6, ...

**The mask `0x55555555`:**
```
0x55555555 = 0101 0101 0101 0101 0101 0101 0101 0101
           = bits 0, 2, 4, 6, 8, ..., 30 are set
```

ANDing with this mask checks if the single set bit is at an even position.

```java
public boolean isPowerOfFour(int n) {
    return n > 0 && (n & (n - 1)) == 0 && (n & 0x55555555) != 0;
}
```

**Walkthrough:**
```
n = 4  = 0000...0100
n & (n-1) = 0100 & 0011 = 0  → power of 2 ✓
n & 0x55555555 = 0100 & ...0101 = 0100 ≠ 0  → bit 2 (even) ✓  → true

n = 8  = 0000...1000
n & (n-1) = 1000 & 0111 = 0  → power of 2 ✓
n & 0x55555555 = 1000 & ...0101 = 0  → bit 3 (odd) ✗  → false

n = 16 = 00010000
n & (n-1) = 0  → power of 2 ✓
n & 0x55555555 = 00010000 & 00000101 = 0  Wait, let me recheck...
```

Actually `0x55555555` in full 32-bit:
```
bit 31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
  0   1  0  1  0  1  0  1  0  1  0  1  0  1  0  1  0  1  0  1  0  1  0  1  0  1  0  1  0  1  0  1
```
16 = bit 4 → `0x55555555` has bit 4 set? Position 4 is in the pattern 0,2,4,6... YES.
```
n = 16 = bit 4 → 0x55555555 has bit 4 = 1  → non-zero  → true ✓
n = 32 = bit 5 → 0x55555555 has bit 5 = 0  → zero  → false ✓
```

**Test Cases:**
```
isPowerOfFour(1)  → true  (4^0)
isPowerOfFour(4)  → true  (4^1)
isPowerOfFour(16) → true  (4^2)
isPowerOfFour(64) → true  (4^3)
isPowerOfFour(2)  → false (power of 2 but not 4)
isPowerOfFour(8)  → false (power of 2 but not 4)
isPowerOfFour(32) → false
```

---

## 3. Check Power of 3

There is no pure bit-manipulation trick for powers of 3. The standard approach
uses division or logarithms.

**Approach 1 — Iterative Division:**
```java
public boolean isPowerOfThree(int n) {
    if (n <= 0) return false;
    while (n % 3 == 0) {
        n /= 3;
    }
    return n == 1;
}
```

**Approach 2 — Largest Power of 3 in int Range:**
The largest power of 3 that fits in a 32-bit signed int is 3^19 = 1162261467.
If n is a power of 3, it must divide this number evenly.

```java
public boolean isPowerOfThree(int n) {
    return n > 0 && 1162261467 % n == 0;
}
```

**Why 3^19?**
```
3^0  = 1
3^1  = 3
3^2  = 9
...
3^19 = 1162261467   (fits in int, < 2^31 = 2147483648)
3^20 = 3486784401   (> 2^31 - 1, overflows)
```

**Approach 3 — Logarithms (O(1) but floating-point precision):**
```java
public boolean isPowerOfThreeLog(int n) {
    if (n <= 0) return false;
    double log = Math.log(n) / Math.log(3);
    return Math.abs(log - Math.round(log)) < 1e-10;
}
```

**Caveat:** Floating-point precision can give wrong answers for large n. The
modulo approach is preferred.

**Test Cases:**
```
isPowerOfThree(1)   → true  (3^0)
isPowerOfThree(3)   → true  (3^1)
isPowerOfThree(9)   → true  (3^2)
isPowerOfThree(27)  → true  (3^3)
isPowerOfThree(2)   → false
isPowerOfThree(6)   → false
isPowerOfThree(0)   → false
```

---

## 4. Find Nearest Power of 2 (>= n)

Used in hash table sizing, memory allocation, etc.

```java
public int nearestPowerOf2(int n) {
    if (n <= 0) return 1;
    n--;
    n |= n >>> 1;
    n |= n >>> 2;
    n |= n >>> 4;
    n |= n >>> 8;
    n |= n >>> 16;
    return n + 1;
}
```

**Walkthrough with n = 13:**
```
n--          = 12  = 1100
n |= n>>>1   = 1100 | 0110 = 1110
n |= n>>>2   = 1110 | 0011 = 1111
n |= n>>>4   = 1111 | 0000 = 1111  (already all 1s in top bits)
n + 1        = 10000 = 16  ✓
```

**Walkthrough with n = 1:**
```
n--    = 0  = 0000
ORs... = 0
n + 1  = 1  ✓
```

---

## 5. Find Nearest Power of 2 (<= n)

```java
public int largestPowerOf2(int n) {
    if (n <= 0) return 0;
    int p = 1 << 30;  // largest power of 2 in int range
    while (p > n) p >>= 1;
    return p;
}
```

**Or using bit length:**
```java
public int largestPowerOf2(int n) {
    if (n <= 0) return 0;
    int bits = 31 - Integer.numberOfLeadingZeros(n);
    return 1 << bits;
}
```

---

## 6. All Powers of 2 Up to n

```java
public List<Integer> allPowersOf2(int n) {
    List<Integer> powers = new ArrayList<>();
    for (int p = 1; p <= n; p <<= 1) {
        powers.add(p);
    }
    return powers;
}
```

**For `long` values (avoids overflow):**
```java
public List<Long> allPowersOf2(long n) {
    List<Long> powers = new ArrayList<>();
    for (long p = 1; p <= n; p <<= 1) {
        powers.add(p);
    }
    return powers;
}
```

---

## 7. Count Set Bits for Nearest Power of 2

To find the smallest power of 2 with at least k set bits in a range:

```java
// Number of bits needed to represent n
public int bitLength(int n) {
    if (n == 0) return 1;
    return 32 - Integer.numberOfLeadingZeros(n);
}
```

---

## 8. Power of 2 Related Utility

```java
// Check if n is a power of 2 and return log2(n)
public int logBase2(int n) {
    if (n <= 0 || (n & (n - 1)) != 0) return -1;  // not a power of 2
    return Integer.numberOfTrailingZeros(n);
}

// Examples:
// logBase2(1)  = 0
// logBase2(8)  = 3
// logBase2(16) = 4
```
