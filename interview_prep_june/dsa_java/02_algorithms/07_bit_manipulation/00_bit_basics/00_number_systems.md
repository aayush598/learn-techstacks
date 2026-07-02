# Number Systems

## Binary to Decimal

```java
int binaryToDecimal(String binary) {
    int result = 0;
    for (char c : binary.toCharArray()) {
        result = result * 2 + (c - '0');
    }
    return result;
}
```

## Decimal to Binary

```java
String decimalToBinary(int n) {
    if (n == 0) return "0";
    StringBuilder sb = new StringBuilder();
    while (n > 0) {
        sb.append(n % 2);
        n /= 2;
    }
    return sb.reverse().toString();
}
```

## Two's Complement (Negative Numbers)

Java uses two's complement for negative integers:
- Positive numbers: same as binary
- Negative numbers: flip all bits, add 1

```java
int a = -5; // stored as two's complement of 5
```

## Integer Bounds

```java
int max = Integer.MAX_VALUE;  // 2^31 - 1 = 2,147,483,647
int min = Integer.MIN_VALUE;  // -2^31 = -2,147,483,648
```
