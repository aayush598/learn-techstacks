# Count Set Bits — Complete Reference

Counting 1-bits (popcount) is a fundamental operation in coding interviews,
used in bitmask DP, Hamming distance, parity checks, and more.

---

## 1. Naive Approach — Check Each Bit

O(32) = O(1) time, O(1) space.

```java
public int countBits(int n) {
    int count = 0;
    while (n != 0) {
        count += (n & 1);
        n >>>= 1;  // unsigned shift to avoid infinite loop on negatives
    }
    return count;
}
```

**Walkthrough with n = 13 (1101):**
```
n=1101: count += 1, n = 110  (bit 0 = 1)
n=0110: count += 0, n = 11   (bit 0 = 0)
n=0011: count += 1, n = 1    (bit 0 = 1)
n=0001: count += 1, n = 0    (bit 0 = 1)
count = 3 ✓
```

---

## 2. Brian Kernighan's Algorithm

Each iteration clears the lowest set bit. Runs in O(number of set bits) time.

**Key insight:** `n & (n - 1)` clears the lowest set bit of n.
Proof: `n - 1` flips all bits from the LSB to the rightmost 1. ANDing cancels
that 1 and everything below it.

```java
public int countBits(int n) {
    int count = 0;
    while (n != 0) {
        n &= (n - 1);
        count++;
    }
    return count;
}
```

**Walkthrough with n = 13 (1101):**
```
n = 1101
n & (n-1) = 1101 & 1100 = 1100  → count = 1
n & (n-1) = 1100 & 1011 = 1000  → count = 2
n & (n-1) = 1000 & 0111 = 0000  → count = 3
count = 3 ✓
```

**Walkthrough with n = 7 (111):**
```
n = 111 → 110 → 100 → 000  → count = 3 ✓
```

**Walkthrough with n = 0:**
```
loop doesn't execute → count = 0 ✓
```

---

## 3. Built-in: `Integer.bitCount()`

Java provides a hardware-accelerated popcount (uses POPCNT instruction on
modern CPUs). This is O(1).

```java
int count = Integer.bitCount(n);
```

**For `long`:**
```java
long count = Long.bitCount(n);
```

**Internal implementation (bit-parallel trick):**
```
Count bits in parallel by dividing and conquering:
  x = (x & 0x55555555) + ((x >> 1) & 0x55555555)  // count pairs
  x = (x & 0x33333333) + ((x >> 2) & 0x33333333)  // count nibbles
  x = (x & 0x0F0F0F0F) + ((x >> 4) & 0x0F0F0F0F)  // count bytes
  x = (x & 0x00FF00FF) + ((x >> 8) & 0x00FF00FF)  // count 16-bit
  x = (x & 0x0000FFFF) + (x >> 16)                 // count 32-bit
```

---

## 4. Precomputation for Multiple Queries

When you need to count bits for many numbers, precompute a table.

**Approach A — DP using `result[i] = result[i >> 1] + (i & 1)`:**

The number of set bits in i equals the set bits in `i/2` plus the lowest bit.

```java
public int[] countBitsPrecompute(int n) {
    int[] result = new int[n + 1];
    for (int i = 1; i <= n; i++) {
        result[i] = result[i >> 1] + (i & 1);
    }
    return result;
}
```

**Walkthrough:**
```
i=0: result[0] = 0
i=1: result[1] = result[0] + 1 = 1
i=2: result[2] = result[1] + 0 = 1
i=3: result[3] = result[1] + 1 = 2
i=4: result[4] = result[2] + 0 = 1
i=5: result[5] = result[2] + 1 = 2
i=6: result[6] = result[3] + 0 = 2
i=7: result[7] = result[3] + 1 = 3
→ [0, 1, 1, 2, 1, 2, 2, 3]
```

**Approach B — DP using `result[i] = result[i & (i-1)] + 1`:**

`i & (i-1)` clears the lowest set bit, so we already know its popcount.

```java
public int[] countBitsKBrianKernighan(int n) {
    int[] result = new int[n + 1];
    for (int i = 1; i <= n; i++) {
        result[i] = result[i & (i - 1)] + 1;
    }
    return result;
}
```

**Walkthrough:**
```
i=1:  1 & 0 = 0,  result[1] = result[0] + 1 = 1
i=2:  2 & 1 = 0,  result[2] = result[0] + 1 = 1
i=3:  3 & 2 = 2,  result[3] = result[2] + 1 = 2
i=4:  4 & 3 = 0,  result[4] = result[0] + 1 = 1
i=5:  5 & 4 = 4,  result[5] = result[4] + 1 = 2
i=6:  6 & 5 = 4,  result[6] = result[4] + 1 = 2
i=7:  7 & 6 = 6,  result[7] = result[6] + 1 = 3
→ [0, 1, 1, 2, 1, 2, 2, 3] ✓ same result
```

---

## 5. Parity Check (Odd/Even Number of 1s)

Parity = 1 if odd number of set bits, 0 if even.

**XOR-based reduction:**
```java
public int parity(int n) {
    n ^= n >>> 16;
    n ^= n >>> 8;
    n ^= n >>> 4;
    n ^= n >>> 2;
    n ^= n >>> 1;
    return n & 1;
}
```

**How it works:** Repeatedly XOR-fold the number in half. XOR cancels equal
pairs, so the final bit is the XOR of all bits = parity.

**Walkthrough with n = 13 (1101):**
```
n = 00000000 00000000 00000000 00001101

n ^= n>>>16: 00000000 00000000 00000000 00001101
              XOR with
              00000000 00000000 00000000 00000000
            = 00000000 00000000 00000000 00001101

n ^= n>>>8:  ... same (top bits are 0) → 00000000 00000000 00000000 00001101
n ^= n>>>4:  00000000 00000000 00000000 00001101 ^ 0000...0000
            = 00000000 00000000 00000000 00001101
n ^= n>>>2:  00000000 00000000 00000000 00001101 ^ 0000...0000
            = 00000000 00000000 00000000 00000110  ← wait, let me redo

Actually let me be more careful with n = 13 = ...00001101:

n     = 00001101
n>>>1 = 00000110
n^=n>>>1 = 00001011

n>>>2 = 00000010
n^=n>>>2 = 00001001

n>>>4 = 00000000
n^=n>>>4 = 00001001

n>>>8 = 00000000
n^=n>>>8 = 00001001

n>>>16 = 00000000
n^=n>>>16 = 00001001

n&1 = 1 → odd parity ✓ (3 set bits)
```

**Simpler approach:**
```java
public int parity(int n) {
    int p = 0;
    while (n != 0) {
        p ^= 1;
        n &= (n - 1);  // clear lowest set bit
    }
    return p;
}
```

---

## 6. Hamming Distance Between Two Integers

Hamming distance = number of positions where bits differ = popcount(a ^ b).

```java
public int hammingDistance(int a, int b) {
    return Integer.bitCount(a ^ b);
}
```

**Walkthrough: a = 5 (101), b = 3 (011):**
```
a ^ b = 110
popcount(110) = 2  → hamming distance = 2 ✓
(bits differ at positions 1 and 2)
```

**Hamming Distance of Array (LeetCode 477):**
Sum of hamming distances for all pairs:
```java
public int totalHammingDistance(int[] nums) {
    int total = 0;
    for (int i = 0; i < 32; i++) {
        int countOnes = 0;
        for (int num : nums) {
            countOnes += (num >>> i) & 1;
        }
        // Each bit position contributes: countOnes * (n - countOnes)
        total += countOnes * (nums.length - countOnes);
    }
    return total;
}
```

**Why this works:** For each bit position, countOnes numbers have that bit set.
Each such number pairs with (n - countOnes) numbers that don't, contributing
countOnes * (n - countOnes) to the total hamming distance.

---

## 7. Count Bits for All Numbers in Range [1, n]

Return an array where `result[i]` = number of 1-bits in binary representation of i.

```java
public int[] countBits(int n) {
    int[] result = new int[n + 1];
    for (int i = 1; i <= n; i++) {
        result[i] = result[i >> 1] + (i & 1);
    }
    return result;
}
```

**This is the same as Section 4, Approach A, and is the standard LeetCode 338.**

---

## 8. Count Set Bits from 1 to N (Total Count)

Count the total number of 1-bits in all numbers from 1 to N.

**Pattern-based O(log N) approach:**
For each bit position i, the pattern of bits repeats every 2^(i+1) positions:
- First half (2^i positions): bit is 0
- Second half (2^i positions): bit is 1

```java
public long countTotalSetBits(int n) {
    long total = 0;
    for (int i = 0; (1L << i) <= n; i++) {
        long cycleLen = 1L << (i + 1);  // 2^(i+1)
        long fullCycles = (n + 1) / cycleLen;
        long remainder = (n + 1) % cycleLen;

        total += fullCycles * (1L << i);          // full cycles contribute 2^i ones each
        total += Math.max(0, remainder - (1L << i)); // partial cycle
    }
    return total;
}
```

**Walkthrough with N = 7 (counting 1-bits in 1..7 = 001,010,011,100,101,110,111):**
```
Bit 0 (1s place): pattern 0,1,0,1,0,1,0,1 → four 1s
Bit 1 (2s place): pattern 0,0,1,1,0,0,1,1 → four 1s  Wait...

Actually counting 0 to 7:
0: 000
1: 001
2: 010
3: 011
4: 100
5: 101
6: 110
7: 111
Total = 0+1+1+2+1+2+2+3 = 12
```

---

## 9. Summary of Approaches

| Approach               | Time     | Use Case                          |
|------------------------|----------|-----------------------------------|
| Naive (shift each bit) | O(32)    | Simple, one-off                   |
| Brian Kernighan        | O(popcnt)| When few bits are set             |
| Integer.bitCount()     | O(1)     | Production code (fastest)         |
| DP precomputation      | O(n)     | Multiple queries on [0, n]        |
| XOR fold parity        | O(log32) | Parity check without popcount     |
| Bit pattern counting   | O(logN)  | Total set bits from 1 to N        |
