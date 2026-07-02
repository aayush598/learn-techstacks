# Huffman Coding

**Problem**: Given character frequencies, build optimal prefix codes (variable-length codes where no code is prefix of another).

**Greedy**: Merge the two smallest frequencies repeatedly.

```java
class Node {
    char ch;
    int freq;
    Node left, right;

    Node(char ch, int freq) {
        this.ch = ch; this.freq = freq;
    }
}

public Map<Character, String> huffmanCodes(char[] chars, int[] freqs) {
    PriorityQueue<Node> pq = new PriorityQueue<>(
        (a, b) -> a.freq - b.freq);

    for (int i = 0; i < chars.length; i++) {
        pq.offer(new Node(chars[i], freqs[i]));
    }

    while (pq.size() > 1) {
        Node left = pq.poll();
        Node right = pq.poll();
        Node parent = new Node('\0', left.freq + right.freq);
        parent.left = left;
        parent.right = right;
        pq.offer(parent);
    }

    Map<Character, String> codes = new HashMap<>();
    buildCodes(pq.peek(), "", codes);
    return codes;
}

void buildCodes(Node node, String code, Map<Character, String> codes) {
    if (node == null) return;
    if (node.left == null && node.right == null) {
        codes.put(node.ch, code);
        return;
    }
    buildCodes(node.left, code + "0", codes);
    buildCodes(node.right, code + "1", codes);
}
```

## Key Insight

> Huffman coding is optimal because merging the two smallest frequencies minimizes the weighted path length. This is proven by exchange argument.
