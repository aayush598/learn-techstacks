# Divide Two Integers

Divide without using *, /, or % operators.

```java
public int divide(int dividend, int divisor) {
    if (divisor == 0) return Integer.MAX_VALUE;
    if (dividend == Integer.MIN_VALUE && divisor == -1) return Integer.MAX_VALUE;
    int sign = (dividend > 0) == (divisor > 0) ? 1 : -1;
    long dvd = Math.abs((long) dividend);
    long dvs = Math.abs((long) divisor);
    int result = 0;
    while (dvd >= dvs) {
        long temp = dvs, multiple = 1;
        while (dvd >= (temp << 1)) {
            temp <<= 1;
            multiple <<= 1;
        }
        dvd -= temp;
        result += multiple;
    }
    return sign * result;
}
```
