# Trie Operations

## Delete Operation (Reference Count)

```java
boolean delete(String word) {
    return delete(root, word, 0);
}

boolean delete(TrieNode node, String word, int depth) {
    if (depth == word.length()) {
        if (!node.isEnd) return false;
        node.isEnd = false;
        node.wordCount--;
        node.prefixCount--;
        // Return true if no children (safe to delete)
        return hasNoChildren(node);
    }
    
    int idx = word.charAt(depth) - 'a';
    if (node.children[idx] == null) return false;
    
    boolean shouldDelete = delete(node.children[idx], word, depth + 1);
    
    if (shouldDelete) {
        node.children[idx] = null;
        node.prefixCount--;
    } else {
        node.prefixCount--;
    }
    
    return hasNoChildren(node);
}

boolean hasNoChildren(TrieNode node) {
    for (TrieNode child : node.children) {
        if (child != null) return false;
    }
    return !node.isEnd;
}
```

## Get All Words (DFS)

```java
List<String> getAllWords() {
    List<String> result = new ArrayList<>();
    dfs(root, new StringBuilder(), result);
    return result;
}

void dfs(TrieNode node, StringBuilder prefix, List<String> result) {
    if (node == null) return;
    if (node.isEnd) result.add(prefix.toString());
    
    for (char c = 'a'; c <= 'z'; c++) {
        int idx = c - 'a';
        if (node.children[idx] != null) {
            prefix.append(c);
            dfs(node.children[idx], prefix, result);
            prefix.deleteCharAt(prefix.length() - 1);
        }
    }
}
```

## Longest Common Prefix using Trie

```java
String longestCommonPrefix(String[] strs) {
    Trie trie = new Trie();
    for (String s : strs) {
        if (s.isEmpty()) return "";
        trie.insert(s);
    }
    
    StringBuilder prefix = new StringBuilder();
    TrieNode node = trie.root;
    
    while (true) {
        int childCount = 0;
        char nextChar = ' ';
        for (char c = 'a'; c <= 'z'; c++) {
            if (node.children[c - 'a'] != null) {
                childCount++;
                nextChar = c;
            }
        }
        // Only continue if exactly one child and not at end
        if (childCount != 1 || node.isEnd) break;
        
        prefix.append(nextChar);
        node = node.children[nextChar - 'a'];
    }
    
    return prefix.toString();
}
```

## Wildcard Search

```java
boolean searchWildcard(String word) {
    return searchWildcard(root, word, 0);
}

boolean searchWildcard(TrieNode node, String word, int idx) {
    if (idx == word.length()) return node != null && node.isEnd;
    
    char c = word.charAt(idx);
    if (c == '.') {  // '.' matches any character
        for (TrieNode child : node.children) {
            if (child != null && searchWildcard(child, word, idx + 1)) {
                return true;
            }
        }
        return false;
    } else {
        int childIdx = c - 'a';
        if (node.children[childIdx] == null) return false;
        return searchWildcard(node.children[childIdx], word, idx + 1);
    }
}
```
