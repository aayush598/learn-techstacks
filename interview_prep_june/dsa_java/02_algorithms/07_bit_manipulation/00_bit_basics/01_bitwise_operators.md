# Bitwise Operators — Complete Reference

Bitwise operators work on individual bits of integers. They are foundational
to competitive programming, system design (bitmasks, flags), and low-level
optimization.

---

## 1. AND (`&`)

Both bits must be 1 for the result to be 1.

**Truth Table:**
```
0 & 0 = 0    0 & 1 = 0
1 & 0 = 0    1 & 1 = 1
```

**Java Code:**
```java
int a = 12;  // 1100
int b = 10;  // 1010
int c = a & b; // 1000 = 8

// Practical uses:
// 1. Masking: extract specific bits
int lowNibble = value & 0x0F;       // keep only bits 0-3
int highNibble = value & 0xF0;      // keep only bits 4-7

// 2. Check if n is even
boolean even = (n & 1) == 0;

// 3. Clear the lowest set bit
int cleared = n & (n - 1);

// 4. Check if bit i is set
boolean bitSet = (n & (1 << i)) != 0;

// 5. Intersection of two sets represented as bitmasks
int common = setA & setB;
```

**DSA Example — Check if number is power of 2:**
A power of 2 has exactly one set bit. `n & (n-1)` clears that bit, so the
result is 0 only for powers of 2 (and 0).
```java
boolean isPow2 = n > 0 && (n & (n - 1)) == 0;
```

---

## 2. OR (`|`)

At least one bit must be 1 for the result to be 1.

**Truth Table:**
```
0 | 0 = 0    0 | 1 = 1
1 | 0 = 1    1 | 1 = 1
```

**Java Code:**
```java
int a = 12;  // 1100
int b = 10;  // 1010
int c = a | b; // 1110 = 14

// Practical uses:
// 1. Setting bits
int withBit3 = n | (1 << 3);    // force bit 3 to 1

// 2. Union of two sets
int union = setA | setB;

// 3. Building a mask from known set bits
int mask = 0;
mask |= (1 << a);
mask |= (1 << b);
// now mask has bits a and b set

// 4. Set all bits up to position k
int allOnesUpToK = (1 << (k + 1)) - 1;  // equivalent to (1 << k) | ((1 << k) - 1)
```

**DSA Example — Building adjacency bitmask for graphs:**
```java
// Node i is connected to nodes 1, 3, 7
int[] adj = new int[n];
adj[i] = (1 << 1) | (1 << 3) | (1 << 7);
// Check if i is connected to node j
boolean connected = (adj[i] & (1 << j)) != 0;
```

---

## 3. XOR (`^`)

Bits must differ for the result to be 1. XOR is its own inverse: `a ^ a = 0`,
`a ^ 0 = a`.

**Truth Table:**
```
0 ^ 0 = 0    0 ^ 1 = 1
1 ^ 0 = 1    1 ^ 1 = 0
```

**Java Code:**
```java
int a = 12;  // 1100
int b = 10;  // 1010
int c = a ^ b; // 0110 = 6

// Practical uses:
// 1. Toggle bits
int toggled = n ^ ((1 << k) - 1);   // flip lowest k bits

// 2. Swap two numbers without temp
a ^= b;  b ^= a;  a ^= b;

// 3. Find unique element (all others appear twice)
int unique = 0;
for (int x : arr) unique ^= x;

// 4. Difference of two sets
int diff = setA ^ setB;  // elements in exactly one set

// 5. Check if two numbers have opposite signs
boolean opposite = (a ^ b) < 0;

// 6. Prefix XOR for range queries
// xor[l..r] = prefixXor[r+1] ^ prefixXor[l]
```

**DSA Example — Find missing number (1 to n):**
```java
int xorAll = 0, xorArr = 0;
for (int i = 1; i <= n; i++) xorAll ^= i;
for (int x : arr) xorArr ^= x;
int missing = xorAll ^ xorArr;
```

---

## 4. NOT (`~`)

Flips every bit: 0 becomes 1 and vice versa. In Java, `~x = -(x+1)` for
two's complement.

**Truth Table (single bit):**
```
~0 = 1    ~1 = 0
```

**Java Code:**
```java
int a = 5;       // 00000000 00000000 00000000 00000101
int b = ~a;      // 11111111 11111111 11111111 11111010 = -6
int c = ~0;      // -1 (all bits set)

// Practical uses:
// 1. Clear specific bits
int cleared = n & ~(1 << i);     // clear bit i
int clearedRange = n & ~((1 << (j+1)) - 1);  // clear bits 0..j

// 2. Get two's complement (negate)
// -n == ~n + 1 == ~(n - 1)
```

**Pitfall:** `~` inverts ALL 32 bits, including sign. `~5 = -6`, not a small
positive number. This trips up beginners.

---

## 5. Left Shift (`<<`)

Shifts bits left by `k` positions. Vacated bits are filled with 0.
Equivalent to multiplying by 2^k.

**Java Code:**
```java
int a = 5;       // 0000...0101
int b = a << 1;  // 0000...1010 = 10
int c = a << 3;  // 0010...1000 = 40 (= 5 * 8)

// Practical uses:
// 1. Multiply by power of 2
int doubled = n << 1;
int times8 = n << 3;

// 2. Create bitmask
int mask = (1 << n) - 1;   // n ones: e.g. (1<<4)-1 = 15 = 1111

// 3. Set bit at position i
n |= (1 << i);

// 4. Build combinations using bitmask
for (int mask = 0; mask < (1 << n); mask++) { ... }
```

**Pitfall — Overflow:** `1 << 31` = `Integer.MIN_VALUE` (negative). Left
shifting into the sign bit is undefined behavior in languages with undefined
behavior; in Java it is well-defined but produces a negative number.

```java
int x = 1 << 31;          // -2147483648 (Integer.MIN_VALUE)
int y = 1 << 32;          // 1 (wraps: shift mod 32)
int z = 1L << 32;         // 4294967296L (use long for larger shifts)
```

---

## 6. Signed Right Shift (`>>`)

Shifts bits right by `k` positions. Vacated bits are filled with the
**sign bit** (arithmetic shift). Equivalent to floor division by 2^k.

**Java Code:**
```java
int a = 20;      // 0000...10100
int b = a >> 2;  // 0000...00101 = 5

int neg = -20;   // 1111...01100
int c = neg >> 2; // 1111...11101 = -5 (sign preserved)

// Practical uses:
// 1. Divide by power of 2 (floor)
int half = n >> 1;        // floor(n/2)
int quarter = n >> 2;     // floor(n/4)

// 2. Extract sign bit
int signBit = (n >> 31) & 1;  // 1 if negative, 0 if positive

// 3. Branchless absolute value
int abs = (n ^ (n >> 31)) - (n >> 31);

// 4. Get bit at position i
int bitI = (n >> i) & 1;
```

---

## 7. Unsigned Right Shift (`>>>`)

Same as `>>` but vacated bits are always filled with **0** (logical shift).
Java has no unsigned integer types, but `>>>` provides unsigned behavior for
right shifts.

**Java Code:**
```java
int a = -8;      // 1111...11000
int b = a >>> 3; // 0001...11111 = 536870911 (fills with 0s, not 1s)

int c = a >> 3;  // 1111...11111 = -1 (fills with sign bit)

// Practical uses:
// 1. Treat int as unsigned for comparison
boolean aLessThanB = (a >>> 0) < (b >>> 0);  // unsigned comparison

// 2. Get unsigned representation as long
long unsigned = Integer.toUnsignedLong(n);

// 3. Extract top bits without sign extension
int topBits = (n >>> 24) & 0xFF;  // top byte, unsigned
```

**Key difference:**
```java
int x = -1;
System.out.println(x >> 1);    // -1  (fills with 1s)
System.out.println(x >>> 1);   // 2147483647  (fills with 0s)
```

---

## 8. Bitwise Compound Assignments

```java
int a = 12;    // 1100
int b = 10;    // 1010

a &= b;    // a = a & b  = 8  (1000)
a |= b;    // a = a | b
a ^= b;    // a = a ^ b
a <<= 2;   // a = a << 2 (multiply by 4)
a >>= 1;   // a = a >> 1 (divide by 2)
a >>>= 1;  // a = a >>> 1 (unsigned divide by 2)
```

**Common pattern — Toggle with XOR-assignment:**
```java
int flags = 0;
flags ^= (1 << 3);  // toggle bit 3 on
flags ^= (1 << 3);  // toggle bit 3 off
```

---

## 9. Operator Precedence (Critical!)

In Java, bitwise operators have **lower** precedence than comparison operators:

```
<< >> >>>   (highest among these)
&           (lower)
^           (lower)
|           (lowest)
```

**Pitfall:** `if (a & 1 == 0)` is parsed as `a & (1 == 0)` = `a & 0` = 0. Always
use parentheses:

```java
if ((a & 1) == 0)  // correct: check if even
if ((a & (1 << i)) != 0)  // correct: check bit i
```

---

## 10. Summary Table

| Operator | Name          | Use Case                        | DSA Example                        |
|----------|---------------|---------------------------------|------------------------------------|
| `&`      | AND           | Mask, clear, check bits         | Power of 2 check, set intersection|
| `\|`     | OR            | Set bits, build masks           | Adjacency bitmask, union          |
| `^`      | XOR           | Toggle, cancel pairs            | Missing number, single number     |
| `~`      | NOT           | Invert, create bitmask          | Clear range of bits               |
| `<<`     | Left Shift    | Multiply by 2^k, create mask    | Subsets enumeration               |
| `>>`     | Signed RShift | Floor divide by 2^k             | Extract bits, signed arithmetic   |
| `>>>`    | Unsigned RShift| Treat as unsigned              | Unsigned comparison, top bits     |
