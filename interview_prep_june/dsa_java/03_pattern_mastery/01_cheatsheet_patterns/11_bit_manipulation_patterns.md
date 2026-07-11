# Bit Manipulation Patterns Cheatsheet

---

## When to Use Bit Manipulation

- Constraints: n ≤ 20 (try all subsets with bitmasks)
- Check if number is power of 2
- Set operations on small sets
- Need to pack/unpack multiple boolean states
- XOR-based problems (unique element, missing number)
- Parity/hamming weight computation

---

## Essential Bit Operations

```java
// Check if bit i is set
boolean isSet(int n, int i) {
    return (n & (1 << i)) != 0;
}

// Set bit i
int setBit(int n, int i) {
    return n | (1 << i);
}

// Clear bit i
int clearBit(int n, int i) {
    return n & ~(1 << i);
}

// Toggle bit i
int toggleBit(int n, int i) {
    return n ^ (1 << i);
}

// Isolate lowest set bit
int lowestSetBit(int n) {
    return n & (-n);
}

// Clear lowest set bit
int clearLowestBit(int n) {
    return n & (n - 1);
}
```

---

## Pattern 1: XOR Tricks

```java
// Single Number — every element appears twice except one
public int singleNumber(int[] nums) {
    int result = 0;
    for (int num : nums) {
        result ^= num;
    }
    return result;
}

// Single Number III — two elements appear once
public int[] singleNumberIII(int[] nums) {
    int xor = 0;
    for (int num : nums) xor ^= num;

    // Get lowest set bit (differs between the two unique numbers)
    int diffBit = xor & (-xor);

    int a = 0, b = 0;
    for (int num : nums) {
        if ((num & diffBit) != 0) {
            a ^= num;
        } else {
            b ^= num;
        }
    }
    return new int[]{a, b};
}

// Missing Number (0 to n)
public int missingNumber(int[] nums) {
    int result = nums.length;
    for (int i = 0; i < nums.length; i++) {
        result ^= i ^ nums[i];
    }
    return result;
}

// Find Duplicate Number (using XOR properties)
// Alternative approach using bit counting:
public int findDuplicate(int[] nums) {
    int result = 0;
    for (int bit = 0; bit < 32; bit++) {
        int mask = 1 << bit;
        int countInNums = 0, countInRange = 0;

        for (int num : nums) {
            if ((num & mask) != 0) countInNums++;
        }

        for (int i = 1; i <= nums.length; i++) {
            if ((i & mask) != 0) countInRange++;
        }

        if (countInNums > countInRange) {
            result |= mask;
        }
    }
    return result;
}
```

---

## Pattern 2: AND Tricks

```java
// Power of Two
public boolean isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}

// Count set bits (hamming weight)
public int hammingWeight(int n) {
    int count = 0;
    while (n != 0) {
        n &= (n - 1); // clear lowest set bit
        count++;
    }
    return count;
}

// Count bits from 0 to n
public int[] countBits(int n) {
    int[] result = new int[n + 1];
    for (int i = 1; i <= n; i++) {
        result[i] = result[i >> 1] + (i & 1);
    }
    return result;
}
```

---

## Pattern 3: Bit Masking (Subsets)

```java
// Generate all subsets
public List<List<Integer>> subsets(int[] nums) {
    int n = nums.length;
    List<List<Integer>> result = new ArrayList<>();

    for (int mask = 0; mask < (1 << n); mask++) {
        List<Integer> subset = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) {
                subset.add(nums[i]);
            }
        }
        result.add(subset);
    }
    return result;
}

// Bitmask DP — Traveling Salesman Problem
public int tsp(int[][] dist) {
    int n = dist.length;
    int[][] dp = new int[1 << n][n];
    for (int[] row : dp) Arrays.fill(row, Integer.MAX_VALUE);
    dp[1][0] = 0; // start at city 0

    for (int mask = 1; mask < (1 << n); mask++) {
        for (int u = 0; u < n; u++) {
            if (dp[mask][u] == Integer.MAX_VALUE) continue;
            if ((mask & (1 << u)) == 0) continue;

            for (int v = 0; v < n; v++) {
                if ((mask & (1 << v)) != 0) continue;
                int newMask = mask | (1 << v);
                dp[newMask][v] = Math.min(dp[newMask][v], dp[mask][u] + dist[u][v]);
            }
        }
    }

    int fullMask = (1 << n) - 1;
    int result = Integer.MAX_VALUE;
    for (int u = 0; u < n; u++) {
        result = Math.min(result, dp[fullMask][u] + dist[u][0]);
    }
    return result;
}
```

---

## Pattern 4: Bit Counting

```java
// Parity of bits (even or odd number of 1s)
public boolean hasParity(int n) {
    n ^= (n >> 16);
    n ^= (n >> 8);
    n ^= (n >> 4);
    n ^= (n >> 2);
    n ^= (n >> 1);
    return (n & 1) == 0;
}

// Minimum bit flips to convert A to B
public int minBitFlips(int a, int b) {
    return Integer.bitCount(a ^ b);
}
```

---

## Pattern 5: Divide and Multiply by 2

```java
// Divide without using +, -, *, /
public int divide(int dividend, int divisor) {
    if (dividend == Integer.MIN_VALUE && divisor == -1) return Integer.MAX_VALUE;

    boolean negative = (dividend < 0) ^ (divisor < 0);
    long a = Math.abs((long) dividend);
    long b = Math.abs((long) divisor);

    int result = 0;
    while (a >= b) {
        long temp = b;
        int multiple = 1;
        while (a >= (temp << 1)) {
            temp <<= 1;
            multiple <<= 1;
        }
        a -= temp;
        result += multiple;
    }

    return negative ? -result : result;
}

// Multiply without using +, -, *, /
public int multiply(int a, int b) {
    boolean negative = (a < 0) ^ (b < 0);
    a = Math.abs(a);
    b = Math.abs(b);

    int result = 0;
    while (b > 0) {
        if ((b & 1) == 1) {
            result += a;
        }
        a <<= 1;
        b >>= 1;
    }
    return negative ? -result : result;
}
```

---

## Pattern 6: Bit Packing (Store Multiple States)

```java
// Store RGB color in one integer
int packColor(int r, int g, int b) {
    return (r << 16) | (g << 8) | b;
}

int unpackRed(int color)   { return (color >> 16) & 0xFF; }
int unpackGreen(int color) { return (color >> 8) & 0xFF; }
int unpackBlue(int color)  { return color & 0xFF; }

// Store multiple boolean flags in one int
class Permissions {
    int flags;

    static final int READ    = 1;  // 001
    static final int WRITE   = 2;  // 010
    static final int EXECUTE = 4;  // 100

    void grant(int perm)    { flags |= perm; }
    void revoke(int perm)   { flags &= ~perm; }
    boolean has(int perm)   { return (flags & perm) != 0; }
    void toggle(int perm)   { flags ^= perm; }
}
```

---

## Pattern 7: Subsets of a Set

```java
// Enumerate all subsets using bitmask
void enumerateSubsets(int[] set) {
    int n = set.length;
    for (int mask = 0; mask < (1 << n); mask++) {
        System.out.print("{ ");
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) {
                System.out.print(set[i] + " ");
            }
        }
        System.out.println("}");
    }
}

// Iterate only subsets of a specific mask
void iterateSubsets(int mask) {
    int sub = mask;
    do {
        // process sub
        sub = (sub - 1) & mask;
    } while (sub != mask);
}
```

---

## Pattern 8: Bitwise Sieve

```java
// Check primes up to n using bit array
boolean[] sieve(int n) {
    boolean[] isPrime = new boolean[n + 1];
    Arrays.fill(isPrime, true);
    isPrime[0] = isPrime[1] = false;

    for (int i = 2; i * i <= n; i++) {
        if (isPrime[i]) {
            for (int j = i * i; j <= n; j += i) {
                isPrime[j] = false;
            }
        }
    }
    return isPrime;
}
```

---

## Template: Subset Enumeration

```java
// For problems where n ≤ 20, try all subsets
for (int mask = 0; mask < (1 << n); mask++) {
    // Process subset represented by mask
    int subsetSize = Integer.bitCount(mask);
    // Do something with the subset
}
```

---

## 10+ Bit Manipulation Problem Templates

| # | Problem | Bit Pattern |
|---|---------|-------------|
| 1 | Single Number | XOR all elements |
| 2 | Number of 1 Bits | Clear lowest bit repeatedly |
| 3 | Counting Bits | DP: result[i] = result[i/2] + i%2 |
| 4 | Power of Two | n & (n-1) == 0 |
| 5 | Missing Number | XOR index and value |
| 6 | Reverse Bits | Bit-by-bit reversal |
| 7 | UTF-8 Validation | Count leading 1 bits |
| 8 | Bitwise AND of Range | Shift until common prefix |
| 9 | Subsets | Bitmask enumeration |
| 10 | Traveling Salesman | Bitmask DP |
| 11 | Maximum XOR Subarray | Prefix XOR + bitmask |
| 12 | Minimum Bit Flips | XOR + popcount |
