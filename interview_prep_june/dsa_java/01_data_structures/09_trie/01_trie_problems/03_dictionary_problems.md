# Dictionary / Trie Problems

Trie-based problems involving word dictionaries, prefix matching, and string operations.

---

## Problem 1: Word Break (DP + Trie Walk)

**LeetCode 139** — Can `s` be segmented into dictionary words?

```java
class Solution {
    private static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEnd = false;
    }

    private TrieNode root = new TrieNode();

    private void insert(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) {
                node.children[idx] = new TrieNode();
            }
            node = node.children[idx];
        }
        node.isEnd = true;
    }

    public boolean wordBreak(String s, List<String> wordDict) {
        for (String word : wordDict) {
            insert(word);
        }

        int n = s.length();
        boolean[] dp = new boolean[n + 1];
        dp[0] = true; // empty string is segmentable

        for (int i = 0; i < n; i++) {
            if (!dp[i]) continue;

            // Walk trie from position i
            TrieNode node = root;
            for (int j = i; j < n; j++) {
                int idx = s.charAt(j) - 'a';
                if (node.children[idx] == null) break; // no match
                node = node.children[idx];

                if (node.isEnd) {
                    dp[j + 1] = true; // s[i..j] is a valid word
                }
            }
        }
        return dp[n];
    }
}
```

**Complexity:** O(n²) in worst case (vs O(n² × k) with HashSet approach, where k = avg word length). Trie avoids redundant prefix checks.

---

## Problem 2: Replace Words

**LeetCode 648** — Replace each word in sentence with its shortest root from dictionary.

```java
class Solution {
    private static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        String word = null; // store the complete root at end
    }

    private TrieNode root = new TrieNode();

    private void insert(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) {
                node.children[idx] = new TrieNode();
            }
            node = node.children[idx];
            // First root found is shortest (if dict is sorted by length)
        }
        node.word = word;
    }

    private String findRoot(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) return word;
            node = node.children[idx];
            if (node.word != null) return node.word; // found shortest root
        }
        return word;
    }

    public String replaceWords(List<String> dictionary, String sentence) {
        // Sort by length so shortest roots are inserted first
        dictionary.sort(Comparator.comparingInt(String::length));
        for (String root : dictionary) {
            insert(root);
        }

        String[] words = sentence.split(" ");
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < words.length; i++) {
            if (i > 0) sb.append(" ");
            sb.append(findRoot(words[i]));
        }
        return sb.toString();
    }
}
```

---

## Problem 3: Add and Search Words (Wildcard '.' Support)

**LeetCode 211** — `addWord(word)` and `search(word)` where `.` matches any letter.

```java
class WordDictionary {
    private static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEnd = false;
    }

    private TrieNode root = new TrieNode();

    public void addWord(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) {
                node.children[idx] = new TrieNode();
            }
            node = node.children[idx];
        }
        node.isEnd = true;
    }

    public boolean search(String word) {
        return dfs(word, 0, root);
    }

    private boolean dfs(String word, int index, TrieNode node) {
        if (node == null) return false;
        if (index == word.length()) return node.isEnd;

        char c = word.charAt(index);
        if (c == '.') {
            // Try all 26 children
            for (TrieNode child : node.children) {
                if (child != null && dfs(word, index + 1, child)) {
                    return true;
                }
            }
            return false;
        } else {
            int idx = c - 'a';
            return dfs(word, index + 1, node.children[idx]);
        }
    }
}
```

**Key:** For `.`, we branch out and try all 26 possible children via DFS.

---

## Problem 4: Palindrome Pairs

**LeetCode 336** — Find all pairs (i, j) where `words[i] + words[j]` is a palindrome.

**Trie approach:** Insert all words reversed. For each word, traverse the trie checking palindrome conditions.

```java
class Solution {
    private static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        int wordIndex = -1;
        List<Integer> palindromesBelow = new ArrayList<>(); // indices of words that are palindromes from here to end
    }

    private TrieNode root = new TrieNode();

    private void insert(String word, int index) {
        TrieNode node = root;
        for (int i = word.length() - 1; i >= 0; i--) { // insert reversed
            int idx = word.charAt(i) - 'a';
            if (node.children[idx] == null) {
                node.children[idx] = new TrieNode();
            }
            node = node.children[idx];

            // If word[i..end] is a palindrome, this prefix can pair
            if (isPalindrome(word, 0, i)) {
                node.palindromesBelow.add(index);
            }
        }
        node.wordIndex = index;
    }

    public List<List<Integer>> palindromePairs(String[] words) {
        List<List<Integer>> result = new ArrayList<>();

        for (int i = 0; i < words.length; i++) {
            insert(words[i], i);
        }

        for (int i = 0; i < words.length; i++) {
            search(words[i], i, result);
        }
        return result;
    }

    private void search(String word, int index, List<List<Integer>> result) {
        TrieNode node = root;

        for (int j = 0; j < word.length(); j++) {
            // Case 1: current word is longer — check if remaining suffix is palindrome
            if (node.wordIndex >= 0 && node.wordIndex != index
                && isPalindrome(word, j, word.length() - 1)) {
                result.add(Arrays.asList(index, node.wordIndex));
            }

            int idx = word.charAt(j) - 'a';
            if (node.children[idx] == null) return;
            node = node.children[idx];
        }

        // Case 2: matched entire word in trie
        for (int other : node.palindromesBelow) {
            if (other != index) {
                result.add(Arrays.asList(index, other));
            }
        }
    }

    private boolean isPalindrome(String s, int left, int right) {
        while (left < right) {
            if (s.charAt(left++) != s.charAt(right--)) return false;
        }
        return true;
    }
}
```

---

## Problem 5: Longest Word in Dictionary

**LeetCode 720** — Find longest word that can be built one character at a time.

```java
class Solution {
    private static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        String word = null;
    }

    private TrieNode root = new TrieNode();
    private String best = "";

    public String longestWord(String[] words) {
        for (String word : words) {
            insert(word);
        }
        dfs(root, "");
        return best;
    }

    private void insert(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) {
                node.children[idx] = new TrieNode();
            }
            node = node.children[idx];
        }
        node.word = word;
    }

    private void dfs(TrieNode node, String current) {
        if (node == null) return;

        // Only continue if this node represents a complete word (or root)
        if (node.word != null) {
            if (current.length() > best.length()
                || (current.length() == best.length() && current.compareTo(best) < 0)) {
                best = current;
            }
            for (int i = 0; i < 26; i++) {
                if (node.children[i] != null) {
                    dfs(node.children[i], current + (char)('a' + i));
                }
            }
        }
    }
}
```

**Key insight:** Only DFS into children if the current node is a complete word — this ensures every prefix in the path is also a word in the dictionary.

---

## Pattern Summary

| Problem | Trie Usage |
|---------|-----------|
| Word Break | Trie replaces HashSet for prefix matching during DP |
| Replace Words | Insert roots, walk each word to find shortest prefix match |
| Wildcard Search | DFS on trie for `.` character |
| Palindrome Pairs | Insert reversed words, check palindrome conditions during traversal |
| Longest Buildable Word | DFS with pruning (only follow complete-word nodes) |

---

## Interview Tips

- **Trie vs HashSet:** Use Trie when you need prefix matching or wildcard support. HashSet is simpler for exact matches.
- **Insert reversed** for problems involving suffixes or palindrome checking from both ends.
- **DFS on Trie** is natural for wildcard problems — `.` triggers branching to all children.
