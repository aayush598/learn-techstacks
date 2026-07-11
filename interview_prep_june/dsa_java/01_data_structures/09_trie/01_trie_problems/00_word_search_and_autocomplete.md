# Word Search & Autocomplete

## Problem 1: Word Search II

Find all words from dictionary that exist in a 2D board:

```java
List<String> findWords(char[][] board, String[] words) {
    // Build trie
    TrieNode root = buildTrie(words);
    
    int m = board.length, n = board[0].length;
    List<String> result = new ArrayList<>();
    
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            dfs(board, i, j, root, result);
        }
    }
    return result;
}

TrieNode buildTrie(String[] words) {
    TrieNode root = new TrieNode();
    for (String w : words) {
        TrieNode node = root;
        for (char c : w.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) node.children[idx] = new TrieNode();
            node = node.children[idx];
        }
        node.word = w;  // store word at end node
    }
    return root;
}

void dfs(char[][] board, int i, int j, TrieNode node, List<String> result) {
    char c = board[i][j];
    if (c == '#' || node.children[c - 'a'] == null) return;
    
    node = node.children[c - 'a'];
    if (node.word != null) {  // found a word
        result.add(node.word);
        node.word = null;  // avoid duplicates
    }
    
    board[i][j] = '#';  // mark visited
    int[][] dirs = {{0,1},{1,0},{0,-1},{-1,0}};
    for (int[] d : dirs) {
        int ni = i + d[0], nj = j + d[1];
        if (ni >= 0 && ni < board.length && nj >= 0 && nj < board[0].length) {
            dfs(board, ni, nj, node, result);
        }
    }
    board[i][j] = c;  // restore
}
```

## Problem 2: Autocomplete System

```java
class AutocompleteSystem {
    private TrieNode root;
    private StringBuilder currentInput;
    
    AutocompleteSystem(String[] sentences, int[] times) {
        root = new TrieNode();
        currentInput = new StringBuilder();
        for (int i = 0; i < sentences.length; i++) {
            addSentence(sentences[i], times[i]);
        }
    }
    
    private void addSentence(String s, int time) {
        TrieNode node = root;
        for (char c : s.toCharArray()) {
            int idx = c == ' ' ? 0 : c - 'a' + 1;  // simple space handling
            if (node.children[idx] == null) node.children[idx] = new TrieNode();
            node = node.children[idx];
        }
        node.isEnd = true;
        node.hotness += time;  // cumulative if added again
    }
    
    List<String> input(char c) {
        if (c == '#') {  // end of input
            addSentence(currentInput.toString(), 1);
            currentInput = new StringBuilder();
            return new ArrayList<>();
        }
        
        currentInput.append(c);
        List<String> result = new ArrayList<>();
        
        // Find node for current prefix
        TrieNode node = root;
        for (char ch : currentInput.toString().toCharArray()) {
            int idx = ch == ' ' ? 0 : ch - 'a' + 1;
            if (node.children[idx] == null) return result;
            node = node.children[idx];
        }
        
        // Collect all sentences from this node
        PriorityQueue<Map.Entry<String, Integer>> pq = new PriorityQueue<>(
            (a, b) -> a.getValue().equals(b.getValue()) 
                ? b.getKey().compareTo(a.getKey()) 
                : a.getValue() - b.getValue()
        );
        
        collect(node, currentInput.toString(), pq);
        
        while (!pq.isEmpty()) result.add(pq.poll().getKey());
        Collections.reverse(result);
        return result.size() > 3 ? result.subList(0, 3) : result;
    }
    
    private void collect(TrieNode node, String prefix, PriorityQueue<Map.Entry<String, Integer>> pq) {
        if (node.isEnd) {
            pq.offer(new AbstractMap.SimpleEntry<>(prefix, node.hotness));
            if (pq.size() > 3) pq.poll();
        }
        for (int i = 0; i < 27; i++) {
            if (node.children[i] != null) {
                char c = (i == 0) ? ' ' : (char)('a' + i - 1);
                collect(node.children[i], prefix + c, pq);
            }
        }
    }
}
```

## Problem 3: Word Break with Trie

```java
boolean wordBreak(String s, List<String> wordDict) {
    TrieNode root = buildTrie(wordDict);
    int n = s.length();
    boolean[] dp = new boolean[n + 1];
    dp[0] = true;
    
    for (int i = 0; i < n; i++) {
        if (!dp[i]) continue;
        TrieNode node = root;
        for (int j = i; j < n; j++) {
            int idx = s.charAt(j) - 'a';
            if (node.children[idx] == null) break;
            node = node.children[idx];
            if (node.isEnd) dp[j + 1] = true;
        }
    }
    return dp[n];
}
```
