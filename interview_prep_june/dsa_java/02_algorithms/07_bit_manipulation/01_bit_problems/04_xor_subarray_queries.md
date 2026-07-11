# XOR Subarray Queries — Complete Reference

XOR has special algebraic properties that make subarray XOR queries efficient.
This covers prefix XOR, counting subarrays with XOR = K, range queries, and
maximum XOR subarray.

---

## 1. XOR Properties (Foundation)

These properties are essential for all XOR-based algorithms:

```
1. a ^ a = 0          (self-cancel)
2. a ^ 0 = a          (identity)
3. a ^ b = b ^ a      (commutative)
4. a ^ (b ^ c) = (a ^ b) ^ c  (associative)
5. a ^ b ^ a = b      (from properties 1 and 4)
6. a ^ b ^ b = a      (from properties 1 and 4)
```

**Corollary:** If `xor[l..r] = K`, then `prefixXor[r+1] ^ prefixXor[l] = K`,
which means `prefixXor[r+1] = prefixXor[l] ^ K`.

---

## 2. Prefix XOR Array

Like prefix sums, but using XOR. This allows O(1) range XOR queries.

```java
public int[] buildPrefixXor(int[] nums) {
    int[] prefix = new int[nums.length + 1];
    for (int i = 0; i < nums.length; i++) {
        prefix[i + 1] = prefix[i] ^ nums[i];
    }
    return prefix;
}
```

**Walkthrough with nums = [4, 2, 6, 3]:**
```
prefix[0] = 0
prefix[1] = 0 ^ 4 = 4
prefix[2] = 4 ^ 2 = 6
prefix[3] = 6 ^ 6 = 0
prefix[4] = 0 ^ 3 = 3

prefix = [0, 4, 6, 0, 3]
```

**Range XOR query — XOR of nums[l..r]:**
```java
public int rangeXor(int[] prefix, int l, int r) {
    return prefix[r + 1] ^ prefix[l];
}
```

**Walkthrough — XOR of nums[1..2] = [2, 6]:**
```
rangeXor(prefix, 1, 2) = prefix[3] ^ prefix[1] = 0 ^ 4 = 4
Verification: 2 ^ 6 = 4 ✓
```

**Walkthrough — XOR of nums[0..3] = [4, 2, 6, 3]:**
```
rangeXor(prefix, 0, 3) = prefix[4] ^ prefix[0] = 3 ^ 0 = 3
Verification: 4 ^ 2 ^ 6 ^ 3 = 3 ✓
```

---

## 3. Count Subarrays with XOR = K (LeetCode 1177 variant)

**Approach — HashMap of prefix XOR counts:**

For each position r, we want to count how many l <= r satisfy:
`prefixXor[r+1] ^ prefixXor[l] = K`
Which means: `prefixXor[l] = prefixXor[r+1] ^ K`

So for each r, look up how many times `prefixXor[r+1] ^ K` has appeared.

```java
public int countSubarraysWithXorK(int[] nums, int k) {
    Map<Integer, Integer> prefixCount = new HashMap<>();
    prefixCount.put(0, 1);  // empty prefix has XOR = 0
    int xor = 0, count = 0;
    for (int num : nums) {
        xor ^= num;
        int target = xor ^ k;
        count += prefixCount.getOrDefault(target, 0);
        prefixCount.merge(xor, 1, Integer::sum);
    }
    return count;
}
```

**Walkthrough with nums = [4, 2, 2, 6], k = 6:**
```
prefixXor: [0, 4, 6, 4, 2]

Subarrays with XOR = 6:
[4,2,2] = 4^2^2 = 4  → no
[2,2,6] = 2^2^6 = 6  → yes
[4,2,2,6] = 4^2^2^6 = 6  → yes

Step by step:
xor=0, count=0, prefixCount={0:1}

num=4: xor=4, target=4^6=2, count += prefixCount.getOrDefault(2,0)=0
       prefixCount = {0:1, 4:1}

num=2: xor=4^2=6, target=6^6=0, count += prefixCount.getOrDefault(0,0)=1
       prefixCount = {0:1, 4:1, 6:1}  → count=1 (subarray [4,2,2])

num=2: xor=6^2=4, target=4^6=2, count += prefixCount.getOrDefault(2,0)=0
       prefixCount = {0:1, 4:2, 6:1}  → count=1

num=6: xor=4^6=2, target=2^6=4, count += prefixCount.getOrDefault(4,0)=2
       prefixCount = {0:1, 4:2, 6:1, 2:1}  → count=3
```

Wait, let me recount. The subarrays:
```
[4]     = 4
[4,2]   = 6  → yes (1)
[4,2,2] = 4
[4,2,2,6] = 6  → yes (2)
[2]     = 2
[2,2]   = 0
[2,2,6] = 6  → yes (3)
[2]     = 2
[2,6]   = 4
[6]     = 6  → yes (4)
```

Hmm, that's 4. Let me retrace more carefully:

```
prefixXor = [0, 4, 6, 4, 2]

Subarray [i..j] has XOR = prefixXor[j+1] ^ prefixXor[i]
We want prefixXor[j+1] ^ prefixXor[i] = 6

i=0,j=0: prefix[1]^prefix[0] = 4^0 = 4   ✗
i=0,j=1: prefix[2]^prefix[0] = 6^0 = 6   ✓
i=0,j=2: prefix[3]^prefix[0] = 4^0 = 4   ✗
i=0,j=3: prefix[4]^prefix[0] = 2^0 = 2   ✗
i=1,j=1: prefix[2]^prefix[1] = 6^4 = 2   ✗
i=1,j=2: prefix[3]^prefix[1] = 4^4 = 0   ✗
i=1,j=3: prefix[4]^prefix[1] = 2^4 = 6   ✓
i=2,j=2: prefix[3]^prefix[2] = 4^6 = 2   ✗
i=2,j=3: prefix[4]^prefix[2] = 2^6 = 4   ✗
i=3,j=3: prefix[4]^prefix[3] = 2^4 = 6   ✓

Total: 3 subarrays
```

**Algorithm trace (corrected):**
```
xor=0, count=0, prefixCount={0:1}

num=4: xor=4, target=4^6=2, count += 0
       prefixCount={0:1, 4:1}, count=0

num=2: xor=6, target=6^6=0, count += prefixCount[0]=1
       prefixCount={0:1, 4:1, 6:1}, count=1

num=2: xor=4, target=4^6=2, count += prefixCount[2]=0
       prefixCount={0:1, 4:2, 6:1}, count=1

num=6: xor=2, target=2^6=4, count += prefixCount[4]=2
       prefixCount={0:1, 4:2, 6:1, 2:1}, count=3 ✓
```

**Time: O(n), Space: O(n)**

---

## 4. XOR Queries on Array (LeetCode 1310)

Given an array and multiple queries `[l, r]`, return XOR for each query.

```java
public int[] xorQueries(int[] arr, int[][] queries) {
    int[] prefix = new int[arr.length + 1];
    for (int i = 0; i < arr.length; i++) {
        prefix[i + 1] = prefix[i] ^ arr[i];
    }
    int[] result = new int[queries.length];
    for (int i = 0; i < queries.length; i++) {
        int l = queries[i][0], r = queries[i][1];
        result[i] = prefix[r + 1] ^ prefix[l];
    }
    return result;
}
```

**Walkthrough with arr = [1,3,4,8], queries = [[0,1],[1,2],[0,3],[3,3]]:**
```
prefix = [0, 1, 2, 6, 14]

Query [0,1]: prefix[2] ^ prefix[0] = 2 ^ 0 = 2     (1^3 = 2) ✓
Query [1,2]: prefix[3] ^ prefix[1] = 6 ^ 1 = 7     (3^4 = 7) ✓
Query [0,3]: prefix[4] ^ prefix[0] = 14 ^ 0 = 14   (1^3^4^8 = 14) ✓
Query [3,3]: prefix[4] ^ prefix[3] = 14 ^ 6 = 8    (8 = 8) ✓
```

**Time: O(n + q)**

---

## 5. Maximum XOR Subarray

Find the subarray with maximum XOR value.

**Approach 1 — Brute Force O(n²):**
```java
public int maxSubarrayXor(int[] nums) {
    int maxXor = Integer.MIN_VALUE;
    for (int i = 0; i < nums.length; i++) {
        int xor = 0;
        for (int j = i; j < nums.length; j++) {
            xor ^= nums[j];
            maxXor = Math.max(maxXor, xor);
        }
    }
    return maxXor;
}
```

**Approach 2 — Trie O(n * 32):**

Build a binary trie of prefix XOR values. For each prefix XOR, query the trie
for the value that maximizes XOR.

```java
class TrieNode {
    TrieNode[] children = new TrieNode[2];
}

public int maxSubarrayXor(int[] nums) {
    TrieNode root = new TrieNode();
    insert(root, 0);  // prefix XOR = 0

    int prefixXor = 0, maxXor = 0;
    for (int num : nums) {
        prefixXor ^= num;
        maxXor = Math.max(maxXor, query(root, prefixXor));
        insert(root, prefixXor);
    }
    return maxXor;
}

private void insert(TrieNode root, int num) {
    TrieNode node = root;
    for (int i = 31; i >= 0; i--) {
        int bit = (num >> i) & 1;
        if (node.children[bit] == null) {
            node.children[bit] = new TrieNode();
        }
        node = node.children[bit];
    }
}

private int query(TrieNode root, int num) {
    TrieNode node = root;
    int result = 0;
    for (int i = 31; i >= 0; i--) {
        int bit = (num >> i) & 1;
        int want = 1 - bit;  // opposite bit maximizes XOR
        if (node.children[want] != null) {
            result |= (1 << i);
            node = node.children[want];
        } else {
            node = node.children[bit];
        }
    }
    return result;
}
```

**Walkthrough with nums = [3, 10, 5, 25, 2, 8]:**
```
prefixXor progression: 0, 3, 9, 12, 21, 23, 31

The subarray [5, 25, 2, 8] has XOR = 5^25^2^8 = 30
Actually let me verify: 5=101, 25=11001, 2=10, 8=1000
5^25 = 28 (11100)
28^2 = 30 (11110)
30^8 = 22 (10110)

Hmm, the maximum is actually prefixXor[5] ^ prefixXor[2] = 23 ^ 9 = 30
= nums[2..4] = [5, 25, 2] = 5^25^2 = 30 ✓
```

---

## 6. Maximum XOR with Query Element

Given an array and multiple queries, for each query find max XOR of query
with any element in the array.

```java
public int[] maxXorWithQueries(int[] arr, int[] queries) {
    TrieNode root = new TrieNode();
    for (int num : arr) {
        insert(root, num);
    }
    int[] result = new int[queries.length];
    for (int i = 0; i < queries.length; i++) {
        result[i] = query(root, queries[i]);
    }
    return result;
}
```

---

## 7. K-th Smallest XOR Pair Value (LeetCode 1882)

Given an array, find the k-th smallest value among all pairs (i,j) where i<j,
sorted by `nums[i] ^ nums[j]`.

**Approach — Binary search on answer + counting:**

```java
public int kthSmallestPairXor(int[] nums, int k) {
    int low = 0, high = Integer.MAX_VALUE;
    while (low < high) {
        int mid = low + (high - low) / 2;
        if (countPairsWithXorLessOrEqual(nums, mid) >= k) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    return low;
}

private long countPairsWithXorLessOrEqual(int[] nums, int target) {
    // Use trie to count pairs with XOR <= target
    // For each num, query trie: how many existing numbers give XOR <= target
    TrieNode root = new TrieNode();
    long count = 0;
    for (int num : nums) {
        count += countLessOrEqual(root, num, target);
        insert(root, num);
    }
    return count;
}

private long countLessOrEqual(TrieNode root, int num, int target) {
    TrieNode node = root;
    long count = 0;
    for (int i = 31; i >= 0 && node != null; i--) {
        int numBit = (num >> i) & 1;
        int tarBit = (target >> i) & 1;
        if (tarBit == 1) {
            // If target bit is 1, the path with opposite bit gives XOR=1 < target's 1
            // (all lower bits don't matter, it's already <)
            if (node.children[numBit] != null) {
                count += countLeaves(node.children[numBit]); // or subtree size
            }
            node = node.children[1 - numBit];
        } else {
            node = node.children[numBit];
        }
    }
    if (node != null) count += countLeaves(node);
    return count;
}
```

**Note:** This is a complex problem. The trie approach counts pairs in O(n * 32)
per binary search step, giving O(n * 32 * log(MAX)) overall.

---

## 8. XOR Linked List (Bonus)

XOR can be used to store a doubly linked list using only one pointer per node:

```java
class XORListNode {
    int val;
    long address;  // XOR of prev and next addresses
}
// address = prevAddress ^ nextAddress
// next = address ^ prevAddress
```

This is primarily an interview curiosity / memory optimization.

---

## 9. Summary

| Problem                       | Approach        | Time       | Space |
|-------------------------------|-----------------|------------|-------|
| Range XOR query               | Prefix XOR      | O(1)/query | O(n)  |
| Count subarrays with XOR = K  | HashMap prefix  | O(n)       | O(n)  |
| Multiple XOR queries          | Prefix XOR      | O(n+q)     | O(n)  |
| Max XOR subarray              | Trie + prefix   | O(32n)     | O(32n)|
| Max XOR with query element    | Trie            | O(32n+32q) | O(32n)|
| K-th smallest XOR pair        | Binary search   | O(32n logM) | O(32n)|
