# Maximum XOR Subarray — Bitwise Trie

---

## Problem 1: Maximum XOR of Two Numbers in an Array

**LeetCode 421** — Given an array, find `max(a[i] XOR a[j])`.

### Approach: Bitwise Trie

Insert each number as a 32-bit binary string. For each number, try to take the **opposite bit** at each level of the trie to maximize XOR.

```java
class Solution {
    private static class TrieNode {
        TrieNode[] children = new TrieNode[2];
    }

    private TrieNode root = new TrieNode();

    private void insert(int num) {
        TrieNode node = root;
        for (int i = 31; i >= 0; i--) {
            int bit = (num >> i) & 1;
            if (node.children[bit] == null) {
                node.children[bit] = new TrieNode();
            }
            node = node.children[bit];
        }
    }

    private int maxXOR(int num) {
        TrieNode node = root;
        int result = 0;
        for (int i = 31; i >= 0; i--) {
            int bit = (num >> i) & 1;
            int desired = 1 - bit; // want opposite bit for max XOR

            if (node.children[desired] != null) {
                result |= (1 << i);  // this bit contributes to XOR
                node = node.children[desired];
            } else {
                node = node.children[bit]; // forced to take same bit
            }
        }
        return result;
    }

    public int findMaximumXOR(int[] nums) {
        for (int num : nums) {
            insert(num);
        }

        int maxVal = 0;
        for (int num : nums) {
            maxVal = Math.max(maxVal, maxXOR(num));
        }
        return maxVal;
    }
}
```

### Why This Works

For two 32-bit numbers `a` and `b`, `a XOR b` is maximized when bits differ at every position. The trie lets us greedily choose the opposite bit at each position.

```
Example: nums = [3, 10, 5, 25, 2, 8]

3  = 00000...00011
10 = 00000...01010
5  = 00000...00101
25 = 00000...11001

Insert 3, 10, 5, 25 into trie.

Query with 25 (11001):
  bit 31..5: all zeros, go left (opposite=1 not available, forced 0)
  bit 4: 1, want 0 → node.children[0] exists → result |= 16
  bit 3: 1, want 0 → node.children[0] exists → result |= 8
  bit 2: 0, want 1 → node.children[1] exists → result |= 4
  bit 1: 0, want 1 → node.children[1] exists → result |= 2
  bit 0: 1, want 0 → node.children[0] exists → result |= 1
  result = 31 (25 XOR 3 = 28... wait let me recalc)
  
Actually: 25 XOR 3 = 011001 (25=11001, 3=00011) = 11010 = 26
25 XOR 10 = 11001 XOR 01010 = 10011 = 19
25 XOR 5  = 11001 XOR 00101 = 11100 = 28
25 XOR 2  = 11001 XOR 00010 = 11011 = 27
25 XOR 8  = 11001 XOR 01000 = 10001 = 17

Best: 25 XOR 5 = 28
```

### Complexity

- **Time:** O(n × 32) = O(n) — insert n numbers, query n numbers, each 32 steps
- **Space:** O(n × 32) = O(n) — at most n×32 nodes in trie

---

## Problem 2: Maximum XOR Subarray

**LeetCode 421 variant** — Find max `a[i] XOR a[i+1] XOR ... XOR a[j]`.

### Key Insight: Prefix XOR

```
a[i] XOR a[i+1] XOR ... XOR a[j] = prefix[j+1] XOR prefix[i]
```

So we need `max(prefix[j+1] XOR prefix[i])` for all `i < j` — which is exactly Problem 1 on the prefix XOR array!

```java
class Solution {
    private static class TrieNode {
        TrieNode[] children = new TrieNode[2];
    }

    private TrieNode root = new TrieNode();

    private void insert(int num) {
        TrieNode node = root;
        for (int i = 31; i >= 0; i--) {
            int bit = (num >> i) & 1;
            if (node.children[bit] == null) {
                node.children[bit] = new TrieNode();
            }
            node = node.children[bit];
        }
    }

    private int maxXOR(int num) {
        TrieNode node = root;
        int result = 0;
        for (int i = 31; i >= 0; i--) {
            int bit = (num >> i) & 1;
            int desired = 1 - bit;
            if (node.children[desired] != null) {
                result |= (1 << i);
                node = node.children[desired];
            } else {
                node = node.children[bit];
            }
        }
        return result;
    }

    public int maximumSubarrayXOR(int[] nums) {
        int maxResult = 0;
        insert(0); // prefix[0] = 0

        int prefix = 0;
        for (int num : nums) {
            prefix ^= num;
            maxResult = Math.max(maxResult, maxXOR(prefix));
            insert(prefix);
        }
        return maxResult;
    }
}
```

### Walkthrough

```
nums = [1, 2, 3]

prefix[0] = 0
prefix[1] = 0 XOR 1 = 1
prefix[2] = 1 XOR 2 = 3
prefix[3] = 3 XOR 3 = 0

Insert 0, query with 1: max XOR with {0} = 1 XOR 0 = 1
Insert 1, query with 3: max XOR with {0,1} = 3 XOR 0 = 3
Insert 3, query with 0: max XOR with {0,1,3} = 0 XOR 3 = 3

Answer: 3 (subarray [1,2] → 1 XOR 2 = 3, or [3] → 3)
```

---

## Template: Bitwise Trie for XOR Problems

```java
class BitwiseTrie {
    private static class Node {
        Node[] children = new Node[2];
        int val = -1; // stores value at leaf (optional)
    }

    private Node root = new Node();

    public void insert(int num) {
        Node node = root;
        for (int i = 31; i >= 0; i--) {
            int bit = (num >> i) & 1;
            if (node.children[bit] == null) {
                node.children[bit] = new Node();
            }
            node = node.children[bit];
        }
        node.val = num;
    }

    public int query(int num) {
        Node node = root;
        for (int i = 31; i >= 0; i--) {
            int bit = (num >> i) & 1;
            int desired = 1 - bit;
            if (node.children[desired] != null) {
                node = node.children[desired];
            } else if (node.children[bit] != null) {
                node = node.children[bit];
            } else {
                return -1; // trie is empty
            }
        }
        return num ^ node.val;
    }
}
```

---

## Related Problems

| Problem | Key Idea |
|---------|----------|
| Max XOR of Two Numbers (421) | Insert all, query all |
| Max XOR Subarray | Prefix XOR + bitwise trie |
| XOR Queries of Subarray | Prefix XOR + hash map |
| Maximum XOR With an Element in Array | Offline: sort queries, insert prefix, query |

---

## Interview Tips

- **Always clarify** if numbers can be negative (negative numbers still have 32-bit representations).
- **Start from bit 31 (MSB)** for greedy — higher bits contribute more.
- **The prefix XOR trick** converts subarray problems to pair problems.
- **Edge case:** Empty subarray (prefix[0] = 0, handled by inserting 0 initially).
