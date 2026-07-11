# Trie Implementation

## What is a Trie?

A **prefix tree** — efficient for string search, prefix matching, autocomplete.

## TrieNode

```java
class TrieNode {
    TrieNode[] children = new TrieNode[26];  // a-z
    boolean isEnd;
    int wordCount;      // optional: number of words ending here
    int prefixCount;    // optional: number of words with this prefix
    
    TrieNode() {
        children = new TrieNode[26];
        isEnd = false;
        wordCount = 0;
        prefixCount = 0;
    }
}
```

## Trie Implementation

```java
class Trie {
    private TrieNode root;
    
    Trie() { root = new TrieNode(); }
    
    void insert(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) {
                node.children[idx] = new TrieNode();
            }
            node = node.children[idx];
            node.prefixCount++;
        }
        node.isEnd = true;
        node.wordCount++;
    }
    
    boolean search(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) return false;
            node = node.children[idx];
        }
        return node.isEnd;
    }
    
    boolean startsWith(String prefix) {
        TrieNode node = root;
        for (char c : prefix.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) return false;
            node = node.children[idx];
        }
        return true;
    }
    
    // Delete word (decrement counters)
    boolean delete(String word) {
        if (!search(word)) return false;
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            node = node.children[idx];
            node.prefixCount--;
        }
        node.wordCount--;
        if (node.wordCount == 0) node.isEnd = false;
        return true;
    }
    
    // Count words with given prefix
    int countPrefix(String prefix) {
        TrieNode node = root;
        for (char c : prefix.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) return 0;
            node = node.children[idx];
        }
        return node.prefixCount;
    }
}
```

## Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Insert | O(L) | O(L·alphabet) |
| Search | O(L) | O(1) |
| StartsWith | O(L) | O(1) |
| Delete | O(L) | O(1) |

Where L = word length, alphabet = 26 (or character set size).

## HashMap-based Trie (for any character set)

```java
class TrieNode {
    Map<Character, TrieNode> children = new HashMap<>();
    boolean isEnd;
}
```
Use when character set is large or unknown (emojis, Unicode, etc.).
