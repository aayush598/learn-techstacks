# GCD, LCM & Euclidean Algorithm

## Euclidean Algorithm

```java
public int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a % b);
}

// Iterative
public int gcdIterative(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
```

## LCM

```java
public int lcm(int a, int b) {
    return a / gcd(a, b) * b; // divide first to avoid overflow
}
```

## GCD of Array

```java
public int gcdArray(int[] arr) {
    int result = arr[0];
    for (int i = 1; i < arr.length; i++) {
        result = gcd(result, arr[i]);
    }
    return result;
}
```

## Extended Euclidean Algorithm

Finds x, y such that ax + by = gcd(a, b)

```java
public int[] extendedGcd(int a, int b) {
    if (b == 0) return new int[]{a, 1, 0}; // gcd, x, y
    int[] result = extendedGcd(b, a % b);
    int gcd = result[0], x1 = result[1], y1 = result[2];
    return new int[]{gcd, y1, x1 - (a / b) * y1};
}
```
