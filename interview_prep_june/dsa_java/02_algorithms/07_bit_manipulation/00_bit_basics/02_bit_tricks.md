# Bit Tricks

## Common Operations

```java
// Check if even
boolean isEven = (n & 1) == 0;

// Set i-th bit (to 1)
n = n | (1 << i);

// Clear i-th bit (to 0)
n = n & ~(1 << i);

// Toggle i-th bit
n = n ^ (1 << i);

// Check i-th bit
boolean isSet = (n & (1 << i)) != 0;

// Remove last set bit
n = n & (n - 1);

// Isolate last set bit
int lsb = n & -n;

// Check if power of 2
boolean isPowerOf2 = n > 0 && (n & (n - 1)) == 0;

// Count set bits
int count = Integer.bitCount(n);

// Get bit length (position of highest set bit + 1)
int bitLength = 32 - Integer.numberOfLeadingZeros(n);

// Check if two numbers have opposite signs
boolean oppositeSigns = (a ^ b) < 0;

// Absolute value (branchless)
int abs = (n ^ (n >> 31)) - (n >> 31);

// Minimum of two numbers (branchless)
int min = b ^ ((a ^ b) & -(a < b ? 1 : 0));

// Maximum of two numbers (branchless)
int max = a ^ ((a ^ b) & -(a < b ? 1 : 0));

// Add 1 to a number (no + operator)
int next = -~n; // -~n = n + 1

// Subtract 1
int prev = ~-n; // ~-n = n - 1
```

## Most Useful Tricks

1. `n & (n-1)` — removes lowest set bit
2. `n & -n` — isolates lowest set bit
3. `n > 0 && (n & (n-1)) == 0` — check power of 2
