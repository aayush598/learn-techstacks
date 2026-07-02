# Find Missing Number

## Missing in [0, n] — XOR

```java
public int missingNumber(int[] nums) {
    int xor = 0, i = 0;
    for (; i < nums.length; i++) {
        xor ^= i ^ nums[i];
    }
    return xor ^ i;
}
```

## Using Sum Formula

```java
public int missingNumber(int[] nums) {
    int n = nums.length;
    int expected = n * (n + 1) / 2;
    int actual = 0;
    for (int num : nums) actual += num;
    return expected - actual;
}
```

## Find Missing and Repeating

```java
public int[] findMissingRepeating(int[] nums) {
    int xor = 0;
    for (int i = 0; i < nums.length; i++) {
        xor ^= nums[i] ^ (i + 1);
    }
    int diffBit = xor & -xor;
    int a = 0, b = 0;
    for (int i = 0; i < nums.length; i++) {
        if ((nums[i] & diffBit) == 0) a ^= nums[i];
        else b ^= nums[i];
        if (((i + 1) & diffBit) == 0) a ^= (i + 1);
        else b ^= (i + 1);
    }
    for (int num : nums) {
        if (num == a) return new int[]{a, b};
    }
    return new int[]{b, a};
}
```
