# Bitmask & Subsets

## Bitmask Operations

```java
// Check if i-th bit is set
if ((mask & (1 << i)) != 0) { ... }

// Set i-th bit
mask |= (1 << i);

// Unset (clear) i-th bit
mask &= ~(1 << i);

// Toggle i-th bit
mask ^= (1 << i);

// Isolate LSB (lowest set bit)
int lsb = mask & -mask;

// Remove LSB
mask &= mask - 1;

// Count set bits
Integer.bitCount(mask);
```

## Iterate Over All Subsets

```java
int n = 4;
for (int mask = 0; mask < (1 << n); mask++) {
    // mask represents a subset of {0, 1, 2, ..., n-1}
    // bit i is set → element i is in the subset
}
```

## Iterate Over Submasks of a Given Mask

```java
// Iterate over all subsets of a given mask
for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {
    // process sub
}
// Also consider empty set separately: sub = 0
```

## Enumerate All Subsets of K Elements

```java
int n = 5, k = 3;
// Gosper's hack
int mask = (1 << k) - 1;
while (mask < (1 << n)) {
    // process mask (has exactly k bits set)
    int c = mask & -mask;
    int r = mask + c;
    mask = (((r ^ mask) >> 2) / c) | r;
}
```

## Applications

### Subset Sum using Bitmask
```java
boolean subsetSum(int[] nums, int target) {
    int n = nums.length;
    BitSet possible = new BitSet(target + 1);
    possible.set(0);
    for (int num : nums) {
        BitSet next = (BitSet) possible.clone();
        next.or((BitSet) possible.clone().get(num, target + 1));
        possible = next;
    }
    return possible.get(target);
}
```

### Partition into K Subsets
```java
// Use bitmask DP: dp[mask] = possible to form subsets from mask
```
