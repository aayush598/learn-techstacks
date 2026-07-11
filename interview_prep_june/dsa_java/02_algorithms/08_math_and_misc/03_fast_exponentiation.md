# Fast Exponentiation (Binary Exponentiation)

Compute a^b in O(log b) time by decomposing exponent into binary.

## Binary Exponentiation Concept

Any exponent b can be expressed in binary. For example, 13 = 1101₂, so:

```
3^13 = 3^(1101₂) = 3^8 · 3^4 · 3^1
```

Only O(log b) multiplications needed — square the base each iteration, multiply into result when the corresponding bit is 1.

### Step-by-Step: 3^13

| Step | exp (binary) | base | result | Bit operation |
|------|-------------|------|--------|---------------|
| 0    | 13 (1101)   | 3    | 1      | — |
| 1    | 6 (110)     | 9    | 3      | LSB=1 → result *= 3; base = 3² |
| 2    | 3 (11)      | 81   | 3      | LSB=0 → skip; base = 9² |
| 3    | 1 (1)       | 6561 | 243    | LSB=1 → result *= 81; base = 81² |
| 4    | 0           | —    | 1594323 | LSB=1 → result *= 6561 |

Result: 3^13 = 1,594,323 ✓

## Basic Implementation

```java
public class FastExponentiation {

    public static long fastPower(long base, long exp) {
        long result = 1;
        while (exp > 0) {
            if ((exp & 1) == 1) {
                result *= base;
            }
            base *= base;
            exp >>= 1;
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(fastPower(3, 13));    // 1594323
        System.out.println(fastPower(2, 10));    // 1024
        System.out.println(fastPower(5, 0));     // 1
    }
}
```

## Modular Exponentiation

Critical for cryptography (RSA) and DP where result exceeds long range.

(a^b) % m computed without overflow by taking mod after each multiplication.

```java
public class ModularExponentiation {

    public static int modPow(int base, int exp, int mod) {
        long result = 1;
        long b = base % mod;
        while (exp > 0) {
            if ((exp & 1) == 1) {
                result = (result * b) % mod;
            }
            b = (b * b) % mod;
            exp >>= 1;
        }
        return (int) result;
    }

    public static void main(String[] args) {
        System.out.println(modPow(3, 13, 1000));    // 323 → last 3 digits of 3^13
        System.out.println(modPow(2, 1_000_000, 7)); // fast even for huge exponents
    }
}
```

## Matrix Exponentiation (Fibonacci in O(log n))

Fibonacci: F(n) = F(n-1) + F(n-2) can be computed via matrix:

```
[F(n+1)  F(n)  ]   =   [1  1]^n
[F(n)    F(n-1)]       [1  0]
```

```java
public class MatrixExponentiation {

    static long[][] matMul(long[][] a, long[][] b) {
        int n = a.length;
        long[][] res = new long[n][n];
        for (int i = 0; i < n; i++) {
            for (int k = 0; k < n; k++) {
                if (a[i][k] == 0) continue;
                for (int j = 0; j < n; j++) {
                    res[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        return res;
    }

    static long[][] matPow(long[][] mat, int exp) {
        int n = mat.length;
        long[][] result = new long[n][n];
        for (int i = 0; i < n; i++) result[i][i] = 1; // identity

        while (exp > 0) {
            if ((exp & 1) == 1) {
                result = matMul(result, mat);
            }
            mat = matMul(mat, mat);
            exp >>= 1;
        }
        return result;
    }

    public static long fibonacci(int n) {
        if (n <= 1) return n;
        long[][] base = {{1, 1}, {1, 0}};
        long[][] powered = matPow(base, n - 1);
        return powered[0][0];
    }

    public static void main(String[] args) {
        System.out.println(fibonacci(10));  // 55
        System.out.println(fibonacci(50));  // 12586269025
        System.out.println(fibonacci(92));  // 7540113804746346429 (max for long)
    }
}
```

## Power of Two Check

```java
public class PowerOfTwo {

    // Using exponentiation approach
    public static boolean isPowerOfTwo(int n) {
        if (n <= 0) return false;
        // Check if n has exactly one bit set
        return (n & (n - 1)) == 0;
    }

    // Checking via repeated squaring (overkill but shows concept)
    public static boolean isPowerOfTwoExp(int n) {
        if (n <= 0) return false;
        long pow = 1;
        while (pow < n) {
            pow <<= 1;  // multiply by 2
        }
        return pow == n;
    }
}
```

## Edge Cases

```java
public class EdgeCases {

    public static void main(String[] args) {
        // exp = 0: any base^0 = 1
        System.out.println(fastPower(42, 0));  // 1

        // base = 0: 0^exp = 0 (except 0^0 which is undefined, treat as 1)
        System.out.println(fastPower(0, 5));   // 0

        // Large exponent, modular keeps result bounded
        System.out.println(modPow(2, 1_000_000_000, 1_000_000_007));

        // Negative exponent: use double (not handled by integer versions)
        // 2^(-3) = 1/8 = 0.125
        System.out.println(Math.pow(2, -3));   // 0.125
    }

    // Negative exponent using double
    public static double fastPowerDouble(double base, int exp) {
        if (exp == 0) return 1;
        if (exp < 0) {
            base = 1.0 / base;
            exp = -exp;
        }
        double result = 1.0;
        while (exp > 0) {
            if ((exp & 1) == 1) result *= base;
            base *= base;
            exp >>= 1;
        }
        return result;
    }
}
```

## Complexity

| Variant | Time | Space | Notes |
|---------|------|-------|-------|
| Integer power | O(log b) | O(1) | Danger of overflow |
| Modular | O(log b) | O(1) | Safe for crypto |
| Matrix (Fibonacci) | O(log n · d³) | O(d²) | d=2 for Fibonacci |

## Applications

1. **RSA cryptography**: modular exponentiation is the core operation
2. **Fibonacci in O(log n)**: matrix exponentiation
3. **DP with large exponents**: compute powers modulo M for combinatorial DP
4. **Check power of two**: fast bit check
5. **String periodicity / KMP border**: exponentiation on transition matrices

## Key Insight

> Binary exponentiation works because squaring gives us powers of two: base, base², base⁴, base⁸, ... and any exponent can be represented as a sum of powers of two (its binary representation). This is the same as saying: compute base^(2^k) by repeated squaring, then multiply the ones where bit k is set in the exponent.
