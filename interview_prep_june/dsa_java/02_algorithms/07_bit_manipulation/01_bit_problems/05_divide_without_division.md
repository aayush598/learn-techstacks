# Divide Two Integers Without Division — Complete Reference

**Problem:** Divide two integers without using `*`, `/`, or `%` operators.
Return the quotient truncated toward zero.

This is a classic bit manipulation problem (LeetCode 29).

---

## 1. Understanding the Problem

Division can be thought of as: how many times does `divisor` fit into `dividend`?

The naive approach is repeated subtraction (O(dividend/divisor) = O(2^31) worst case).
The efficient approach uses bit shifting to double the divisor repeatedly,
similar to how long division works in binary.

---

## 2. Binary Long Division (Intuition)

In decimal, to divide 100 by 7:
```
100 = 7 * 10 + 30
 30 = 7 *  4 +  2
  2 = 7 *  0 +  2
Result: 14 remainder 2
```

In binary, each "digit" is a power of 2. We find the largest power of 2
such that `divisor * 2^k <= dividend`, subtract, and repeat.

Example: 10 / 3
```
Binary of 10: 1010

Step 1: 3 << 3 = 24 > 10  → too big
Step 2: 3 << 2 = 12 > 10  → too big
Step 3: 3 << 1 = 6  <= 10 → fits! subtract 6, quotient += 2
        Remaining: 10 - 6 = 4
Step 4: 3 << 0 = 3  <= 4  → fits! subtract 3, quotient += 1
        Remaining: 4 - 3 = 1
Step 5: 3 << 0 = 3  > 1   → doesn't fit anymore

Result: quotient = 3, remainder = 1
```

---

## 3. Step-by-Step Walkthrough

### Example: 10 / 3

```
dividend = 10, divisor = 3
Both positive → sign = 1

Iteration 1:
  temp = 3, multiple = 1
  3 << 1 = 6 <= 10 → temp=6, multiple=2
  6 << 1 = 12 > 10 → stop inner loop
  dvd = 10 - 6 = 4, result = 2

Iteration 2:
  temp = 3, multiple = 1
  3 << 1 = 6 > 4 → stop inner loop immediately
  dvd = 4 - 3 = 1, result = 3

Iteration 3:
  temp = 3, multiple = 1
  3 > 1 → dvd < dvs, loop ends

Result: 3 ✓
```

### Example: 7 / -3

```
dividend = 7, divisor = -3
sign = (7 > 0) == (-3 > 0) ? 1 : -1 → false → sign = -1

dvd = |7| = 7, dvs = |-3| = 3

Iteration 1:
  3 << 1 = 6 <= 7 → temp=6, multiple=2
  6 << 1 = 12 > 7 → stop
  dvd = 7 - 6 = 1, result = 2

Iteration 2:
  3 > 1 → loop ends

Result: sign * result = -1 * 2 = -2 ✓ (truncated toward zero)
```

### Edge Case: Integer.MIN_VALUE / -1

```
dividend = -2147483648 (Integer.MIN_VALUE)
divisor  = -1

Without overflow handling, MIN_VALUE * -1 = 2147483648 > MAX_VALUE → overflow!

Java spec says: Integer.MIN_VALUE / -1 = Integer.MIN_VALUE
But the problem (LeetCode 29) says return Integer.MAX_VALUE on overflow.
```

---

## 4. Complete Java Solution

```java
public int divide(int dividend, int divisor) {
    // Handle overflow
    if (dividend == Integer.MIN_VALUE && divisor == -1) {
        return Integer.MAX_VALUE;
    }
    // Handle division by zero (problem may assume valid input)
    if (divisor == 0) {
        return Integer.MAX_VALUE; // or throw
    }

    // Determine sign
    int sign = ((dividend < 0) ^ (divisor < 0)) ? -1 : 1;

    // Use long to safely handle absolute values (MIN_VALUE edge case)
    long dvd = Math.abs((long) dividend);
    long dvs = Math.abs((long) divisor);

    int result = 0;

    while (dvd >= dvs) {
        long temp = dvs;
        long multiple = 1;

        // Find the largest multiple of divisor that fits
        while (dvd >= (temp << 1)) {
            temp <<= 1;
            multiple <<= 1;
        }

        // Subtract and accumulate result
        dvd -= temp;
        result += multiple;
    }

    return sign * result;
}
```

---

## 5. Alternative: Bit-by-Bit Construction

Instead of the inner while loop, precompute all shifts and check each bit
from high to low:

```java
public int divideBitByBit(int dividend, int divisor) {
    if (dividend == Integer.MIN_VALUE && divisor == -1) {
        return Integer.MAX_VALUE;
    }

    int sign = ((dividend < 0) ^ (divisor < 0)) ? -1 : 1;

    long dvd = Math.abs((long) dividend);
    long dvs = Math.abs((long) divisor);

    int result = 0;

    // Find the highest power of 2 such that dvs * 2^i <= dvd
    for (int i = 31; i >= 0; i--) {
        if ((dvs << i) <= dvd) {
            result |= (1 << i);
            dvd -= (dvs << i);
        }
    }

    return sign * result;
}
```

**Walkthrough with 10 / 3:**
```
dvd=10, dvs=3

i=31: 3 << 31 overflows (negative) → skip
...skip down to...
i=2: 3 << 2 = 12 > 10 → skip
i=1: 3 << 1 = 6 <= 10 → result |= 2, dvd = 10-6 = 4
i=0: 3 << 0 = 3 <= 4  → result |= 1, dvd = 4-3 = 1

result = 2 | 1 = 3 ✓
```

**Time: O(32) = O(1), Space: O(1)**
This is cleaner than the while-loop approach.

---

## 6. Why Use `long` for Absolute Values?

`Math.abs(Integer.MIN_VALUE)` returns `Integer.MIN_VALUE` (still negative) because
the positive value 2147483648 doesn't fit in an int. Using `long` avoids this:

```java
long dvd = Math.abs((long) dividend);
// If dividend = Integer.MIN_VALUE = -2147483648:
// (long)dividend = -2147483648L
// Math.abs(-2147483648L) = 2147483648L ✓ (fits in long)
```

---

## 7. Complexity Analysis

| Approach         | Time      | Space | Notes                          |
|------------------|-----------|-------|--------------------------------|
| Repeated subtract| O(q)      | O(1)  | q = quotient, worst case 2^31 |
| Inner while loop | O(log²q)  | O(1)  | Each iteration doubles temp    |
| Bit-by-bit       | O(32)     | O(1)  | Fixed 32 iterations            |

**Why O(log²q) for the inner while loop?** Each outer iteration removes at
least one bit from the dividend (dvd decreases), giving O(log(dvd)) outer
iterations. The inner while loop also runs O(log(dvd)) times. But in practice
the inner loop doesn't fully restart — the total work across all iterations
is O(log²q).

---

## 8. Edge Cases

| Input                    | Output        | Reason                                  |
|--------------------------|---------------|-----------------------------------------|
| `10 / 3`                | `3`           | Standard case                           |
| `7 / -3`                | `-2`          | Truncated toward zero                   |
| `-7 / 3`                | `-2`          | Truncated toward zero                   |
| `0 / 5`                 | `0`           | Zero dividend                           |
| `1 / 1`                 | `1`           | Equal values                            |
| `Integer.MIN_VALUE / 1` | `MIN_VALUE`   | No overflow                             |
| `Integer.MIN_VALUE / -1`| `MAX_VALUE`   | Overflow → clamp to MAX_VALUE           |
| `Integer.MAX_VALUE / 1` | `MAX_VALUE`   | No overflow                             |
| `Integer.MAX_VALUE / -1`| `-MAX_VALUE`  | No overflow (abs(MAX_VALUE) < MIN_VALUE)|
| `x / 1`                | `x`           | Dividing by 1                           |
| `-2147483648 / 2`       | `-1073741824` | Large negative dividend                 |
| `1000000000 / 1`        | `1000000000`  | Large quotient                          |

---

## 9. Testing Framework

```java
public static void main(String[] args) {
    DivideSolution sol = new DivideSolution();

    // Standard cases
    assert sol.divide(10, 3) == 3;
    assert sol.divide(7, -3) == -2;
    assert sol.divide(-7, 3) == -2;
    assert sol.divide(-7, -3) == 2;

    // Edge cases
    assert sol.divide(0, 5) == 0;
    assert sol.divide(1, 1) == 1;
    assert sol.divide(Integer.MIN_VALUE, -1) == Integer.MAX_VALUE;
    assert sol.divide(Integer.MIN_VALUE, 1) == Integer.MIN_VALUE;
    assert sol.divide(Integer.MAX_VALUE, 1) == Integer.MAX_VALUE;

    // Large values
    assert sol.divide(2147483647, 2) == 1073741823;
    assert sol.divide(-2147483648, 2) == -1073741824;

    System.out.println("All tests passed!");
}
```
