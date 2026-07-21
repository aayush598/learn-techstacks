# Trie Data Structure Guide

## What is Trie?

A Trie (pronounced "try") is a tree-like data structure used for efficient storage and retrieval of strings. Each node represents a character, and paths from root to nodes represent prefixes.

**When to use:**
- Autocomplete/prefix matching
- Word search problems
- String dictionary operations
- IP routing (longest prefix match)
- Spell checkers

**Key Properties:**
- Root is empty
- Each node has at most 26 children (for lowercase English)
- Each node stores: children, is_end_of_word flag
- Prefix of any word can be found in O(m) where m = word length

**Comparison with other structures:**
| Operation | Array | HashSet | Trie |
|-----------|-------|---------|------|
| Insert | O(n) | O(1) | O(m) |
| Search | O(n) | O(1) | O(m) |
| Prefix Search | O(n*m) | O(n*m) | O(m) |
| Space | O(n*m) | O(n*m) | O(sum of lengths) |

---

## 1. Basic Trie Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0  # Number of words with this prefix

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """Insert a word into the trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.count += 1
        node.is_end = True
    
    def search(self, word):
        """Check if word exists in trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def starts_with(self, prefix):
        """Check if any word starts with given prefix"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    
    def count_words_with_prefix(self, prefix):
        """Count words that start with given prefix"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.count
    
    def delete(self, word):
        """Delete a word from trie"""
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                return len(node.children) == 0
            
            char = word[depth]
            if char not in node.children:
                return False
            
            should_delete = _delete(node.children[char], word, depth + 1)
            
            if should_delete:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end
            
            return False
        
        _delete(self.root, word, 0)
    
    def get_all_words(self, prefix=""):
        """Get all words with given prefix"""
        result = []
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return result
            node = node.children[char]
        
        def dfs(node, current_word):
            if node.is_end:
                result.append(current_word)
            
            for char, child in node.children.items():
                dfs(child, current_word + char)
        
        dfs(node, prefix)
        return result

# Test
trie = Trie()
trie.insert("apple")
trie.insert("app")
trie.insert("application")
trie.insert("bat")
trie.insert("ball")

print(f"Search 'apple': {trie.search('apple')}")  # True
print(f"Search 'app': {trie.search('app')}")  # True
print(f"Search 'ap': {trie.search('ap')}")  # False
print(f"Starts with 'app': {trie.starts_with('app')}")  # True
print(f"Words with prefix 'app': {trie.get_all_words('app')}")
print(f"Count words with prefix 'ap': {trie.count_words_with_prefix('ap')}")

trie.delete("apple")
print(f"After delete, search 'apple': {trie.search('apple')}")  # False
print(f"After delete, search 'app': {trie.search('app')}")  # True
```

**Time Complexity:** O(m) for insert/search/delete, where m = word length
**Space Complexity:** O(sum of all word lengths) worst case O(26^m)

---

## 2. Implement Trie (LC 208)

```python
class Trie:
    def __init__(self):
        self.children = [None] * 26
        self.is_end = False
    
    def _char_to_index(self, char):
        return ord(char) - ord('a')
    
    def insert(self, word):
        node = self
        for char in word:
            idx = self._char_to_index(char)
            if not node.children[idx]:
                node.children[idx] = Trie()
            node = node.children[idx]
        node.is_end = True
    
    def search(self, word):
        node = self._search_prefix(word)
        return node is not None and node.is_end
    
    def startsWith(self, prefix):
        return self._search_prefix(prefix) is not None
    
    def _search_prefix(self, prefix):
        node = self
        for char in prefix:
            idx = self._char_to_index(char)
            if not node.children[idx]:
                return None
            node = node.children[idx]
        return node

# Test
trie = Trie()
trie.insert("apple")
print(trie.search("apple"))   # True
print(trie.search("app"))     # False
print(trie.startsWith("app")) # True
trie.insert("app")
print(trie.search("app"))     # True
```

---

## 3. Word Search II (LC 212)

```python
def find_words(board, words):
    """Find all words from dictionary that can be formed in board"""
    # Build trie from words
    trie = {}
    for word in words:
        node = trie
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['#'] = word  # Mark end of word
    
    rows, cols = len(board), len(board[0])
    result = []
    
    def dfs(i, j, parent):
        char = board[i][j]
        
        if char not in parent:
            return
        
        node = parent[char]
        
        # Check if this is end of a word
        if '#' in node:
            result.append(node['#'])
            del node['#']
        
        # Mark visited
        board[i][j] = '#'
        
        # Explore neighbors
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = i + dx, j + dy
            if 0 <= ni < rows and 0 <= nj < cols and board[ni][nj] != '#':
                dfs(ni, nj, node)
        
        # Restore
        board[i][j] = char
        
        # Prune: remove empty nodes
        if not node:
            del parent[char]
    
    for i in range(rows):
        for j in range(cols):
            dfs(i, j, trie)
    
    return result

# Test
board = [
    ['o', 'a', 'a', 'n'],
    ['e', 't', 'a', 'e'],
    ['i', 'h', 'k', 'r'],
    ['i', 'f', 'l', 'v']
]
words = ["oath", "pea", "eat", "rain"]
print(f"Found words: {find_words(board, words)}")  # ["oath", "eat"]
```

**Time Complexity:** O(M * N * 4^L) where M,N = board dimensions, L = max word length
**Space Complexity:** O(W * L) for trie where W = number of words

---

## 4. Maximum XOR of Two Numbers (LC 421)

```python
def find_maximum_xor(nums):
    """Find maximum XOR of two numbers in array"""
    # Build trie for binary representation
    trie = {}
    
    def insert(num):
        node = trie
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            if bit not in node:
                node[bit] = {}
            node = node[bit]
    
    def query(num):
        node = trie
        result = 0
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            toggled = 1 - bit
            
            if toggled in node:
                result |= (1 << i)
                node = node[toggled]
            else:
                node = node[bit]
        return result
    
    max_xor = 0
    for num in nums:
        insert(num)
        max_xor = max(max_xor, query(num))
    
    return max_xor

# Alternative using class
class TrieNode:
    def __init__(self):
        self.children = {}

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, num):
        node = self.root
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            if bit not in node.children:
                node.children[bit] = TrieNode()
            node = node.children[bit]
    
    def query(self, num):
        node = self.root
        result = 0
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            desired = 1 - bit
            
            if desired in node.children:
                result |= (1 << i)
                node = node.children[desired]
            elif bit in node.children:
                node = node.children[bit]
            else:
                return 0
        return result

def find_maximum_xor_v2(nums):
    trie = Trie()
    max_xor = 0
    
    for num in nums:
        trie.insert(num)
        max_xor = max(max_xor, trie.query(num))
    
    return max_xor

# Test
print(f"Maximum XOR: {find_maximum_xor([3, 10, 5, 25, 2, 8])}")  # 28
print(f"Maximum XOR v2: {find_maximum_xor_v2([3, 10, 5, 25, 2, 8])}")  # 28
```

**Time Complexity:** O(31n) = O(n)
**Space Complexity:** O(31n) for trie

---

## 5. Palindrome Pairs (LC 336)

```python
def palindrome_pairs(words):
    """Find all pairs of indices (i, j) such that words[i] + words[j] is palindrome"""
    # Build trie for reversed words
    trie = {}
    word_indices = {}
    
    def insert_reversed(word, idx):
        node = trie
        for char in reversed(word):
            if char not in node:
                node[char] = {}
            node = node[char]
        node['#'] = idx
    
    def search_complement(word, idx):
        """Find words that when concatenated with word form palindrome"""
        node = trie
        result = []
        n = len(word)
        
        # Case 1: Other word is shorter and matches prefix
        for i, char in enumerate(word):
            if '#' in node:
                other_idx = node['#']
                # Check if remaining part of word is palindrome
                remaining = word[i:]
                if remaining == remaining[::-1]:
                    result.append(other_idx)
            
            if char not in node:
                return result
            node = node[char]
        
        # Case 2: Other word is longer
        if '#' in node:
            other_idx = node['#']
            if other_idx != idx:
                result.append(other_idx)
        
        return result
    
    # Insert all reversed words
    for i, word in enumerate(words):
        insert_reversed(word, i)
    
    # Find pairs
    result = set()
    for i, word in enumerate(words):
        matches = search_complement(word, i)
        for j in matches:
            if i != j:
                pair = (min(i, j), max(i, j))
                result.add(pair)
    
    return [list(pair) for pair in result]

# Test
words = ["abcd", "dcba", "lls", "s", "sssll"]
print(f"Palindrome pairs: {palindrome_pairs(words)}")  # [[0,1],[1,0],[3,2],[2,4]]
```

**Time Complexity:** O(n * k^2) where k = average word length
**Space Complexity:** O(n * k)

---

## 6. Map Sum Pairs (LC 677)

```python
class MapSum:
    def __init__(self):
        self.trie = {}
        self.values = {}
    
    def insert(self, key, val):
        node = self.trie
        for char in key:
            if char not in node:
                node[char] = {}
            node = node[char]
        
        # Update value difference
        old_val = self.values.get(key, 0)
        self.values[key] = val
        node['#'] = node.get('#', 0) + (val - old_val)
    
    def sum(self, prefix):
        node = self.trie
        for char in prefix:
            if char not in node:
                return 0
            node = node[char]
        return self._sum_tree(node)
    
    def _sum_tree(self, node):
        total = node.get('#', 0)
        for char, child in node.items():
            if char != '#':
                total += self._sum_tree(child)
        return total

# Alternative with class
class TrieNode:
    def __init__(self):
        self.children = {}
        self.value = 0
        self.sum = 0

class MapSumV2:
    def __init__(self):
        self.root = TrieNode()
        self.values = {}
    
    def insert(self, key, val):
        diff = val - self.values.get(key, 0)
        self.values[key] = val
        
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.sum += diff
        
        node.value = val
    
    def sum(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.sum

# Test
ms = MapSum()
ms.insert("apple", 3)
print(f"Sum 'ap': {ms.sum('ap')}")  # 3
ms.insert("app", 2)
print(f"Sum 'ap': {ms.sum('ap')}")  # 5
```

**Time Complexity:** O(k) for insert, O(k + subtree size) for sum
**Space Complexity:** O(n * k)

---

## 7. Replace Words (LC 648)

```python
def replace_words(dictionary, sentence):
    """Replace roots in sentence with shortest root"""
    # Build trie from dictionary
    trie = {}
    for root in dictionary:
        node = trie
        for char in root:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['#'] = root
    
    def find_shortest_root(word):
        node = trie
        for i, char in enumerate(word):
            if '#' in node:
                return node['#']
            if char not in node:
                return word
            node = node[char]
        return word
    
    words = sentence.split()
    result = []
    
    for word in words:
        root = find_shortest_root(word)
        result.append(root)
    
    return ' '.join(result)

# Alternative using Trie class
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_root = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_root = True
    
    def search_shortest_root(self, word):
        node = self.root
        for i, char in enumerate(word):
            if node.is_root:
                return word[:i]
            if char not in node.children:
                return word
            node = node.children[char]
        return word

def replace_words_v2(dictionary, sentence):
    trie = Trie()
    for root in dictionary:
        trie.insert(root)
    
    words = sentence.split()
    return ' '.join(trie.search_shortest_root(word) for word in words)

# Test
dictionary = ["cat", "bat", "rat"]
sentence = "the cattle was rattled by the battery"
print(f"Replaced: {replace_words(dictionary, sentence)}")
# Output: "the cat was rat by the bat"
```

**Time Complexity:** O(D * L + S) where D = dictionary size, L = avg root length, S = sentence length
**Space Complexity:** O(D * L)

---

## 8. Longest Word in Dictionary (LC 720)

```python
def longest_word(words):
    """Find longest word that can be built one character at a time"""
    trie = {}
    
    for word in words:
        node = trie
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['#'] = word
    
    def dfs(node):
        result = node.get('#', '')
        
        for char, child in node.items():
            if char != '#' and '#' in child:
                candidate = dfs(child)
                if len(candidate) > len(result):
                    result = candidate
        
        return result
    
    return dfs(trie)

# Alternative using Trie class
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

def longest_word_v2(words):
    root = TrieNode()
    
    # Build trie
    for word in words:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.word = word
    
    # DFS to find longest word
    def dfs(node):
        result = node.word or ''
        
        for child in node.children.values():
            if child.word:  # Only continue if this is a complete word
                candidate = dfs(child)
                if len(candidate) > len(result):
                    result = candidate
        
        return result
    
    return dfs(root)

# Test
words = ["w", "wo", "wor", "worl", "world"]
print(f"Longest word: {longest_word(words)}")  # "world"

words2 = ["a", "app", "appl", "apple", "b", "ba", "ban", "banana"]
print(f"Longest word: {longest_word(words2)}")  # "banana"
```

**Time Complexity:** O(sum of all word lengths)
**Space Complexity:** O(sum of all word lengths)

---

## 9. Additional Applications

### 9.1 Autocomplete System (LC 642)

```python
class AutocompleteSystem:
    def __init__(self, sentences, times):
        self.trie = {}
        self.search_cache = {}
        
        for i in range(len(sentences)):
            self._insert(sentences[i], times[i])
    
    def _insert(self, sentence, time):
        node = self.trie
        for char in sentence:
            if char not in node:
                node[char] = {}
            node = node[char]
        
        if '#' not in node:
            node['#'] = {'count': 0, 'sentences': []}
        
        node['#']['count'] += time
    
    def input(self, c):
        if c == '#':
            # End of input, record the sentence
            sentence = ''.join(self.current_input)
            self._insert(sentence, 1)
            self.current_input = []
            return []
        
        self.current_input.append(c)
        prefix = ''.join(self.current_input)
        
        # Search in trie
        node = self.trie
        for char in prefix:
            if char not in node:
                return []
            node = node[char]
        
        # Get all sentences with this prefix
        sentences = []
        self._collect_sentences(node, sentences)
        
        # Sort by count (descending), then lexicographically
        sentences.sort(key=lambda x: (-x[1], x[0]))
        
        return [s[0] for s in sentences[:3]]
    
    def _collect_sentences(self, node, result):
        if '#' in node:
            result.append((node['#'].get('sentence', ''), node['#']['count']))
        
        for char, child in node.items():
            if char != '#':
                self._collect_sentences(child, result)

# Simplified version for LC 642
class AutocompleteSystemSimple:
    def __init__(self):
        self.trie = {}
        self.sentences = {}
        self.current = []
    
    def input(self, c):
        if c == '#':
            sentence = ''.join(self.current)
            self.sentences[sentence] = self.sentences.get(sentence, 0) + 1
            self._insert(sentence)
            self.current = []
            return []
        
        self.current.append(c)
        prefix = ''.join(self.current)
        
        # Find all matching sentences
        node = self.trie
        for char in prefix:
            if char not in node:
                return []
            node = node[char]
        
        # Collect and sort
        matches = []
        self._collect(node, matches)
        matches.sort(key=lambda x: (-self.sentences[x], x))
        
        return matches[:3]
    
    def _insert(self, sentence):
        node = self.trie
        for char in sentence:
            if char not in node:
                node[char] = {}
            node = node[char]
    
    def _collect(self, node, result):
        if not any(c.isalpha() for c in node.keys()):
            # Reached end of a sentence
            for sentence in self.sentences:
                if all(sentence[i] in node for i in range(len(sentence))):
                    result.append(sentence)
        
        for char, child in node.items():
            if char.isalpha():
                self._collect(child, result)

# Test
ac = AutocompleteSystemSimple()
ac.input('i')
ac.input('#')  # Record "i"
ac.input('a')
ac.input('#')  # Record "ia"
print(f"Autocomplete 'i': {ac.input('i')}")  # ['i', 'ia']
```

### 9.2 Word Search II Optimized

```python
def find_words_optimized(board, words):
    """Optimized Word Search II using Trie with backtracking"""
    # Build trie
    trie = {}
    for word in words:
        node = trie
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['$'] = word
    
    rows, cols = len(board), len(board[0])
    result = set()
    
    def dfs(i, j, parent):
        if '$' in parent:
            result.add(parent['$'])
        
        if i < 0 or i >= rows or j < 0 or j >= cols:
            return
        
        char = board[i][j]
        if char == '#' or char not in parent:
            return
        
        node = parent[char]
        board[i][j] = '#'
        
        dfs(i + 1, j, node)
        dfs(i - 1, j, node)
        dfs(i, j + 1, node)
        dfs(i, j - 1, node)
        
        board[i][j] = char
        
        # Optimization: remove leaf nodes
        if not node:
            del parent[char]
    
    for i in range(rows):
        for j in range(cols):
            dfs(i, j, trie)
    
    return list(result)
```

---

## Summary

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Insert | O(m) | O(m) |
| Search | O(m) | O(1) |
| StartsWith | O(m) | O(1) |
| Delete | O(m) | O(m) |
| Space (total) | - | O(sum of lengths) |

Where m = word length

---

## Key Patterns for Infosys SP DSE

1. **Prefix Matching:** Use Trie when all queries share prefixes
2. **XOR Problems:** Use binary Trie for maximum/minimum XOR
3. **String Matching:** Trie for multiple pattern matching
4. **Dictionary Operations:** Autocomplete, spell check
5. **Bitwise Trie:** For XOR-based problems

---

## Tips for Interview

1. **Start simple:** Implement basic TrieNode with children dict
2. **Explain clearly:** Use diagrams for tree structure
3. **Handle edge cases:** Empty strings, single character words
4. **Optimization:** Mention space optimization using arrays vs dict
5. **Application:** Connect to real-world use cases
