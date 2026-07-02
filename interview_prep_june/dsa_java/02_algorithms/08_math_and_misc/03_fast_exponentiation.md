# Fast Exponentiation (Binary Exponentiation)

Compute a^b in O(log b) time.

```java
public long fastPower(long base, long exp) {
    long result = 1;
    while (exp > 0) {
        if ((exp & 1) == 1) result *= base;
        base *= base;
        exp >>= 1;
    }
    return result;
}
```

## Modular Version

```java
public int modPow(int base, int exp, int mod) {
    long result = 1;
    long b = base % mod;
    while (exp > 0) {
        if ((exp & 1) == 1) result = (result * b) % mod;
        b = (b * b) % mod;
        exp >>= 1;
    }
    return (int) result;
}
```
