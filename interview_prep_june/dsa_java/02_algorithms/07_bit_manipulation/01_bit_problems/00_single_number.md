# Single Number Problems

## Single Number I — XOR All

**Problem**: Every element appears twice except one. Find the unique element.

```java
public int singleNumber(int[] nums) {
    int result = 0;
    for (int num : nums) result ^= num;
    return result;
}
```

**Why it works**: a ^ a = 0, a ^ 0 = a. All pairs cancel out.

## Single Number II — Appears 3 Times

**Problem**: Every element appears 3 times except one. Count bits modulo 3.

```java
public int singleNumber(int[] nums) {
    int ones = 0, twos = 0;
    for (int num : nums) {
        ones = (ones ^ num) & ~twos;
        twos = (twos ^ num) & ~ones;
    }
    return ones;
}
```

## Single Number III — Two Unique

**Problem**: Two elements appear once, others appear twice. Find both.

```java
public int[] singleNumber(int[] nums) {
    int xor = 0;
    for (int num : nums) xor ^= num;
    // xor = a ^ b (where a, b are the two unique numbers)

    // Find any set bit in xor
    int diffBit = xor & -xor;

    int a = 0, b = 0;
    for (int num : nums) {
        if ((num & diffBit) == 0) {
            a ^= num;
        } else {
            b ^= num;
        }
    }

    return new int[]{a, b};
}
```
