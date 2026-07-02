# Power of Two

## Check Power of 2

```java
public boolean isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
```

## Check Power of 4

```java
public boolean isPowerOfFour(int n) {
    return n > 0 && (n & (n - 1)) == 0 && (n & 0x55555555) != 0;
}
```

## All Powers of 2

```java
List<Integer> powers = new ArrayList<>();
for (int p = 1; p <= n; p <<= 1) {
    powers.add(p);
}
```
