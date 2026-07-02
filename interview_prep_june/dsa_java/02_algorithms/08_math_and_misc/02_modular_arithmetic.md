# Modular Arithmetic

## Basic Properties

```java
int mod = 1_000_000_007;

int addMod(int a, int b) { return (a % mod + b % mod) % mod; }
int subMod(int a, int b) { return (a % mod - b % mod + mod) % mod; }
int mulMod(int a, int b) { return (int)((long)a % mod * (b % mod) % mod); }
```

## Modular Exponentiation (Fast Power Mod)

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

## Modular Inverse

Using Fermat's Little Theorem (when mod is prime): a^(m-2) ≡ a^(-1) (mod m)

```java
public int modInverse(int a, int mod) {
    return modPow(a, mod - 2, mod);
}
```

Using Extended Euclidean (works when gcd(a, mod) = 1):

```java
public int modInverse(int a, int mod) {
    int[] result = extendedGcd(a, mod);
    int x = result[1];
    return (x % mod + mod) % mod;
}
```
