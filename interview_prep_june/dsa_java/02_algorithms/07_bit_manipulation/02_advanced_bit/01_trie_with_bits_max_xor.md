# Maximum XOR of Two Numbers

## Bitwise Trie

```java
class TrieNode {
    TrieNode[] children = new TrieNode[2];
}

public int findMaximumXOR(int[] nums) {
    TrieNode root = new TrieNode();
    for (int num : nums) {
        TrieNode node = root;
        for (int i = 31; i >= 0; i--) {
            int bit = (num >> i) & 1;
            if (node.children[bit] == null) {
                node.children[bit] = new TrieNode();
            }
            node = node.children[bit];
        }
    }
    int maxXor = 0;
    for (int num : nums) {
        TrieNode node = root;
        int currXor = 0;
        for (int i = 31; i >= 0; i--) {
            int bit = (num >> i) & 1;
            int opposite = 1 - bit;
            if (node.children[opposite] != null) {
                currXor |= (1 << i);
                node = node.children[opposite];
            } else {
                node = node.children[bit];
            }
        }
        maxXor = Math.max(maxXor, currXor);
    }
    return maxXor;
}
```
