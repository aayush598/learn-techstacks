# Subsets Using Bitmask — Complete Reference

Bitmask enumeration is one of the most powerful techniques for problems on
small sets (n ≤ 20). Any subset of an n-element set can be represented as an
n-bit integer.

---

## 1. Core Concept

For a set of size n, represent each subset as a bitmask of n bits.
Bit i being set means element i is in the subset.

```
Set: {A, B, C}  (n=3)
Mask 0 (000): {}           → empty set
Mask 1 (001): {C}          → only element 0
Mask 2 (010): {B}          → only element 1
Mask 3 (011): {B, C}       → elements 0 and 1
Mask 4 (100): {A}          → only element 2
Mask 5 (101): {A, C}       → elements 0 and 2
Mask 6 (110): {A, B}       → elements 1 and 2
Mask 7 (111): {A, B, C}    → all elements
```

Total subsets = 2^n. Iterate `mask` from 0 to 2^n - 1.

---

## 2. Generate All Subsets (Basic)

```java
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
```

**Walkthrough with nums = [1, 2, 3]:**
```
mask=0 (000): subset = []
mask=1 (001): bit 0 set → [1]
mask=2 (010): bit 1 set → [2]
mask=3 (011): bits 0,1 → [1, 2]
mask=4 (100): bit 2 set → [3]
mask=5 (101): bits 0,2 → [1, 3]
mask=6 (110): bits 1,2 → [2, 3]
mask=7 (111): all bits → [1, 2, 3]
```

**Time: O(n * 2^n), Space: O(n * 2^n)**

---

## 3. Count Subsets with Sum Condition

```java
public int countSubsetsWithSum(int[] nums, int target) {
    int n = nums.length, count = 0;
    for (int mask = 0; mask < (1 << n); mask++) {
        int sum = 0;
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) sum += nums[i];
        }
        if (sum == target) count++;
    }
    return count;
}
```

**Walkthrough with nums = [1, 2, 3, 4], target = 5:**
```
mask=0: sum=0   ✗
mask=1: sum=1   ✗
mask=2: sum=2   ✗
mask=3: sum=3   ✗
mask=4: sum=4   ✗
mask=5: sum=5   ✓ ({1,4})
mask=6: sum=6   ✗
mask=7: sum=9   ✗
mask=8: sum=3   ✗
...checking all 16 masks...
{2,3} → sum=5 ✓
count = 2
```

---

## 4. Iterating Over Submasks

Iterate over all non-empty subsets (submasks) of a given mask:

```java
// Iterate over all non-empty submasks of mask
for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {
    // sub is a non-empty subset of mask
    // Process sub...
}
```

**Walkthrough with mask = 13 (1101):**
```
sub = 1101 (13) → {0, 2, 3}
sub = 1100 (12) → {2, 3}
sub = 1001 (9)  → {0, 3}
sub = 1000 (8)  → {3}
sub = 0101 (5)  → {0, 2}
sub = 0100 (4)  → {2}
sub = 0001 (1)  → {0}
sub = 0000 → stop (loop condition sub > 0)
```

**Total iterations = 2^(popcount(mask)) - 1 = 2^3 - 1 = 7 ✓**

**Why does `(sub - 1) & mask` work?**
`sub - 1` flips the lowest set bit of sub and sets all lower bits to 1.
ANDing with mask clears any bits that aren't in mask, producing the next
submask in decreasing order.

---

## 5. Generating Subsets of Exactly Size K (Gosper's Hack)

Generate all bitmasks with exactly K bits set, in increasing order:

```java
public void generateMasksOfWeightK(int n, int k) {
    int mask = (1 << k) - 1;  // smallest mask with k bits: 0...0111...1
    while (mask < (1 << n)) {
        // Process mask (has exactly k bits set)
        process(mask);

        // Gosper's hack: find next mask with same number of bits
        int c = mask & (-mask);        // lowest set bit
        int r = mask + c;              // carry
        mask = (((r ^ mask) >>> 2) / c) | r;
    }
}
```

**Walkthrough with n=5, k=3:**
```
mask = 00111 (7)  → bits {0,1,2}
mask = 01011 (11) → bits {0,1,3}
mask = 01101 (13) → bits {0,2,3}
mask = 01110 (14) → bits {1,2,3}
mask = 10011 (19) → bits {0,1,4}
mask = 10101 (21) → bits {0,2,4}
mask = 10110 (22) → bits {1,2,4}
mask = 11001 (25) → bits {0,3,4}
mask = 11010 (26) → bits {1,3,4}
mask = 11100 (28) → bits {2,3,4}
```

**Time: O(C(n,k))** — exactly the number of combinations.

---

## 6. Combinations Using Bitmask

Generate all C(n, k) combinations of choosing k elements from n:

```java
public List<List<Integer>> combine(int n, int k) {
    List<List<Integer>> result = new ArrayList<>();
    int mask = (1 << k) - 1;
    int limit = 1 << n;
    while (mask < limit) {
        List<Integer> combo = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) {
                combo.add(i + 1);  // 1-indexed
            }
        }
        result.add(combo);

        // Gosper's hack
        int c = mask & (-mask);
        int r = mask + c;
        mask = (((r ^ mask) >>> 2) / c) | r;
    }
    return result;
}
```

---

## 7. Subset Sum with Bitmask DP

For n ≤ 20, iterate over all subsets to find the minimum subset sum >= target:

```java
public int minSubsetSumGeqTarget(int[] nums, int target) {
    int n = nums.length;
    int minSum = Integer.MAX_VALUE;
    for (int mask = 0; mask < (1 << n); mask++) {
        int sum = 0;
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) sum += nums[i];
        }
        if (sum >= target) minSum = Math.min(minSum, sum);
    }
    return minSum;
}
```

---

## 8. Partition Array into Two Subsets with Minimum Difference

```java
public int minDifference(int[] nums) {
    int totalSum = 0;
    for (int x : nums) totalSum += x;
    int n = nums.length;
    int minDiff = totalSum;

    for (int mask = 0; mask < (1 << n); mask++) {
        int subsetSum = 0;
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) subsetSum += nums[i];
        }
        int otherSum = totalSum - subsetSum;
        minDiff = Math.min(minDiff, Math.abs(subsetSum - otherSum));
    }
    return minDiff;
}
```

**Walkthrough with nums = [1, 6, 11, 5]:**
```
totalSum = 23

Best partition: {11} and {1,6,5} → diff = |11 - 12| = 1

mask=0010 (bit 1 set, value 6): sum=6, other=17, diff=11
mask=0100 (bit 2 set, value 11): sum=11, other=12, diff=1 ← minimum
...
```

---

## 9. Maximum Subsets with Property (Exhaustive Search)

Find the maximum-weight subset satisfying a constraint:

```java
// Example: maximum subset with no two adjacent elements (small n)
public int maxNoAdjacent(int[] weights) {
    int n = weights.length;
    int maxWeight = 0;
    for (int mask = 0; mask < (1 << n); mask++) {
        boolean valid = true;
        int weight = 0;
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) {
                weight += weights[i];
                if (i > 0 && (mask & (1 << (i - 1))) != 0) {
                    valid = false;
                    break;
                }
            }
        }
        if (valid) maxWeight = Math.max(maxWeight, weight);
    }
    return maxWeight;
}
```

---

## 10. Enumerating All Partitions into Two Sets

```java
public void enumeratePartitions(int[] nums) {
    int n = nums.length;
    // Each mask represents one half of the partition; the other half is complement
    // Only iterate up to (1 << n) / 2 to avoid duplicate partitions
    for (int mask = 0; mask < (1 << (n - 1)); mask++) {
        List<Integer> setA = new ArrayList<>(), setB = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) {
                setA.add(nums[i]);
            } else {
                setB.add(nums[i]);
            }
        }
        // Process partition: setA, setB
    }
}
```

---

## 11. Quick Reference

| Operation                           | Code                                     |
|-------------------------------------|------------------------------------------|
| Check if bit i is set              | `(mask & (1 << i)) != 0`                |
| Set bit i                           | `mask \|= (1 << i)`                     |
| Clear bit i                         | `mask &= ~(1 << i)`                     |
| Toggle bit i                        | `mask ^= (1 << i)`                      |
| Count set bits                      | `Integer.bitCount(mask)`                 |
| Iterate all submasks               | `for (sub = mask; sub > 0; sub = (sub-1) & mask)` |
| Generate masks with K bits         | Gosper's hack (Section 5)                |
| Total subsets                       | `1 << n`                                |
| Check if A ⊆ B                     | `(A & B) == A`                          |
| Union                               | `A \| B`                                |
| Intersection                        | `A & B`                                 |
| Complement (in n-bit universe)      | `A ^ ((1 << n) - 1)`                    |
| Set difference A \ B               | `A & ~B`                                |
| Symmetric difference                | `A ^ B`                                 |
