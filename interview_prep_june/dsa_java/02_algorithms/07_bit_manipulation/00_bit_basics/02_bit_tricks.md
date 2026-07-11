# Bit Tricks — Complete Reference

Bit tricks are compact, branchless operations that replace multi-line logic
with a single bitwise expression. They are used extensively in competitive
programming, embedded systems, and high-performance Java.

---

## 1. Even / Odd Check

The lowest bit determines parity: 0 for even, 1 for odd.

```java
boolean isEven = (n & 1) == 0;
boolean isOdd  = (n & 1) == 1;
```

**Why not `n % 2 == 0`?** The bitwise version is faster on some architectures
and avoids issues with negative numbers in languages where `%` is remainder
(not modulo). In Java, `-3 % 2 == -1`, but `(-3 & 1) == 1` (odd), which is
the mathematically correct parity.

---

## 2. Multiply / Divide by Power of 2

Left shift multiplies; right shift divides.

```java
int doubled = n << 1;          // n * 2
int times8  = n << 3;          // n * 8
int half    = n >> 1;          // floor(n / 2)
int quarter = n >> 2;          // floor(n / 4)

// Multiply by arbitrary power
int times16 = n << 4;          // n * 16

// Signed right shift preserves sign
int negHalf = -7 >> 1;         // -4 (floor of -3.5)
```

**Pitfall — Shift by >= 32:**
In Java, the shift amount is masked by 31: `n << 32` is the same as `n << 0`.
For shifts >= 32, use `long`:
```java
long big = 1L << 40;           // correct: 1099511627776
int bad = 1 << 40;             // wrong: equivalent to 1 << 8 = 256
```

---

## 3. Swap Without Temp Variable

XOR swap: uses the self-canceling property of XOR.

```java
a ^= b;   // a = a ^ b
b ^= a;   // b = b ^ (a ^ b) = a
a ^= b;   // a = (a ^ b) ^ a = b
```

**Walkthrough with a=5 (101), b=3 (011):**
```
a = 101 ^ 011 = 110  (6)
b = 011 ^ 110 = 101  (5)  → b now holds original a
a = 110 ^ 101 = 011  (3)  → a now holds original b
```

**When to use:** Rarely in practice (compilers optimize `swap` with temp to the
same assembly). Useful in interview questions asking for this specific trick.

**Caveat:** Fails if `a` and `b` reference the same variable: `a ^= a; a ^= a;`
zeros out `a`.

---

## 4. Check If Two Numbers Have Opposite Signs

The sign bit is bit 31. XOR of two numbers with opposite signs has bit 31 set,
making the result negative.

```java
boolean oppositeSigns = (a ^ b) < 0;
```

**Walkthrough:**
```
a =  5:  0000...0101
b = -3:  1111...1101
a ^ b:   1111...1000  → negative → opposite signs

a =  5:  0000...0101
b =  7:  0000...0111
a ^ b:   0000...0010  → positive → same sign
```

---

## 5. Branchless Absolute Value

```java
int abs = (n ^ (n >> 31)) - (n >> 31);
```

**How it works:**
- If n >= 0: `n >> 31` = 0, so result = `n ^ 0 - 0` = `n`
- If n < 0: `n >> 31` = -1 (all 1s), so result = `n ^ (-1) - (-1)` = `~n + 1` = `-n`

**Walkthrough with n = -5:**
```
n >> 31  = -1  (1111...1111)
n ^ (-1) = ~n = 4  (bitwise NOT of -5 is 4)
4 - (-1)  = 5  ✓
```

**Edge case:** `Integer.MIN_VALUE` has no positive counterpart. The formula
returns `Integer.MIN_VALUE` (unchanged) — same as `Math.abs`.

---

## 6. Modulo by Power of 2

Since `2^k - 1` is a bitmask of k ones, ANDing with it gives the remainder.

```java
int mod4  = n & 3;       // n % 4
int mod8  = n & 7;       // n % 8
int mod16 = n & 15;      // n % 16
int modN  = n & (N - 1); // n % N, where N is a power of 2
```

**Walkthrough: n = 29, mod 8:**
```
29 = 11101
 7 = 00111
29 & 7 = 00101 = 5  → 29 % 8 = 5 ✓
```

**DSA use:** Hash table bucket index: `bucket = hashCode & (tableSize - 1)`.

---

## 7. Round Up to Next Power of 2

```java
public static int nextPowerOf2(int n) {
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

**How it works:** Starting from the highest set bit, fill all lower bits with 1,
then add 1. This produces the smallest power of 2 >= n.

**Walkthrough with n = 13 (1101):**
```
n--        = 12  = 1100
n |= n>>>1 = 1110  (fill from bit 3)
n |= n>>>2 = 1111  (fill from bit 2)
n |= n>>>4 = 1111  (already all filled)
n + 1      = 10000 = 16  ✓
```

---

## 8. Isolate Lowest Set Bit (LSB)

`n & -n` uses two's complement: `-n = ~n + 1`, which flips all bits and adds 1,
leaving only the lowest set bit common between n and -n.

```java
int lsb = n & -n;
```

**Walkthrough with n = 12 (1100):**
```
n  = 0000...1100
-n = 1111...0100  (two's complement)
n & -n = 0000...0100 = 4  ✓ (lowest set bit)
```

**Walkthrough with n = 18 (10010):**
```
n  = 0000...10010
-n = 1111...01110
n & -n = 0000...00010 = 2  ✓
```

**DSA use:** Brian Kernighan's algorithm, iterating over subsets of set bits.

---

## 9. Clear Lowest Set Bit

`n & (n-1)` clears the lowest set bit. (n-1) flips all bits from the LSB to the
rightmost 1, and ANDing clears that bit.

```java
int cleared = n & (n - 1);
```

**Walkthrough with n = 12 (1100):**
```
n   = 1100
n-1 = 1011
n & (n-1) = 1000 = 8  ✓ (lowest set bit cleared)
```

**DSA uses:**
- Count set bits: loop `n &= (n-1)` until n = 0, count iterations
- Check power of 2: `n > 0 && (n & (n-1)) == 0`
- Iterate over all subsets of set bits

---

## 10. Clear All Bits from LSB to Position i

```java
// Clear bits 0 through i (inclusive)
int result = n & (~((1 << (i + 1)) - 1));
```

**Walkthrough: n = 0b11010110, clear bits 0..3:**
```
1 << 4        = 10000
(1 << 4) - 1  =  1111
~(...)        = ...11110000
n & mask      = 11010000  ✓
```

---

## 11. Clear All Bits from Position i to MSB

```java
// Keep only bits 0 through i (inclusive)
int result = n & ((1 << (i + 1)) - 1);
```

**Walkthrough: n = 0b11010110, keep bits 0..3:**
```
(1 << 4) - 1 = 00001111
n & mask     = 00000110  ✓
```

---

## 12. Get Rightmost 0 Bit

`~n & (n + 1)` sets the rightmost 0 bit and clears all bits to its right.

```java
int rightmostZero = ~n & (n + 1);
```

**Walkthrough with n = 10101011:**
```
~n       = ...01010100
n + 1    = ...10101100  (carry ripples to first 0)
~n&(n+1) = ...00000100 = bit 2  ✓
```

---

## 13. Set All Bits from LSB to Position i

```java
int result = n | ((1 << (i + 1)) - 1);
```

---

## 14. Extract Byte k from Integer

```java
int byte0 = (n >> 0) & 0xFF;   // least significant byte
int byte1 = (n >> 8) & 0xFF;
int byte2 = (n >> 16) & 0xFF;
int byte3 = (n >> 24) & 0xFF;   // most significant byte
```

---

## 15. Reverse Bits of Integer

```java
public int reverseBits(int n) {
    int result = 0;
    for (int i = 0; i < 32; i++) {
        result = (result << 1) | (n & 1);
        n >>>= 1;
    }
    return result;
}
```

---

## 16. Minimum of Two Numbers (Branchless)

```java
int min = b ^ ((a ^ b) & -(a < b ? 1 : 0));
// Equivalent to: int min = (a < b) ? a : b;  without branch
```

**How it works:**
- If `a < b`: mask = -1 (all 1s), result = `b ^ ((a^b) & -1)` = `b ^ a ^ b` = `a`
- If `a >= b`: mask = 0, result = `b ^ 0` = `b`

---

## 17. Add One Without `+` Operator

```java
int next = -~n;    // -~n = -(~n) = -(-(n+1)) = n + 1
```

**Walkthrough with n = 5:**
```
~5     = -6
-(-6)  = 6  ✓
```

## 18. Subtract One Without `-` Operator

```java
int prev = ~-n;    // ~(-n) = ~(-(n)) = -(n) - 1 = n - 1  (wrong explanation, but works)
// Actually: ~(-n) = ~(-n). For n=5: -5, ~(-5) = 4  ✓
```

---

## 19. Divide by 2 Without `/` Operator

```java
int half = n >> 1;
// Or for unsigned: int half = n >>> 1;
```

---

## 20. Count Trailing Zeros (CTZ)

Number of 0 bits from LSB until the first 1.

```java
public int countTrailingZeros(int n) {
    if (n == 0) return 32;
    int count = 0;
    while ((n & 1) == 0) {
        n >>>= 1;
        count++;
    }
    return count;
}
// Or use: Integer.numberOfTrailingZeros(n)
```

---

## Quick Reference Card

| Trick                          | Expression                      |
|--------------------------------|---------------------------------|
| Is even                        | `(n & 1) == 0`                 |
| Multiply by 2^k               | `n << k`                       |
| Divide by 2^k (floor)         | `n >> k`                       |
| Swap without temp              | `a^=b; b^=a; a^=b;`           |
| Opposite signs                 | `(a ^ b) < 0`                  |
| Absolute value (branchless)    | `(n^(n>>31)) - (n>>31)`        |
| Mod by power of 2             | `n & (p2 - 1)`                 |
| Round up to power of 2        | see Section 7                   |
| Isolate LSB                    | `n & -n`                       |
| Clear LSB                      | `n & (n - 1)`                  |
| Clear bits 0..i               | `n & ~((1 << (i+1)) - 1)`     |
| Keep bits 0..i                | `n & ((1 << (i+1)) - 1)`      |
| Rightmost 0 bit               | `~n & (n + 1)`                 |
| Reverse bits                   | see Section 15                  |
| Add 1 without +               | `-~n`                          |
| Subtract 1 without -          | `~-n`                          |
| Branchless min/max            | see Section 16                  |
