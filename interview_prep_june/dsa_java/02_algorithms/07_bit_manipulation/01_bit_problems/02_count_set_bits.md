# Count Set Bits

## Brian Kernighan's Algorithm

```java
public int countBits(int n) {
    int count = 0;
    while (n > 0) {
        n &= (n - 1);
        count++;
    }
    return count;
}
```

## Integer.bitCount()

```java
int count = Integer.bitCount(n);
```

## Count Bits in Range [1, n]

```java
public int[] countBits(int n) {
    int[] result = new int[n + 1];
    for (int i = 1; i <= n; i++) {
        result[i] = result[i >> 1] + (i & 1);
    }
    return result;
}
```
