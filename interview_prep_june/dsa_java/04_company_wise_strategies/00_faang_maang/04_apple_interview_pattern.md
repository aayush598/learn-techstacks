# Apple Interview Pattern

## Table of Contents
1. Interview Format
2. Most Asked Topics
3. What Apple Values
4. Types of Problems
5. Example Problems
6. Preparation Strategy

---

## 1. Interview Format

### Phone Screen (30-45 min)
- Usually with a hiring manager or senior engineer
- Mix of behavioral + technical
- May ask about your projects or past experience
- Sometimes a light coding problem

### On-site (5-7 rounds, 45-60 min each)
- Apple has the most on-site rounds among FAANG
- **Coding rounds** (3-4): Varying difficulty
- **System Design** (1): For senior roles
- **Hiring Manager** (1): Past experience, cultural fit
- **Cross-functional** (1): Interview with a team you'd collaborate with
- May include a **whiteboard coding** session

### Key Differences
- Apple has NO standard process — each team interviews differently
- Questions are often practical, inspired by Apple products
- Performance and attention to detail are highly valued
- Interviewers may be reserved — don't expect much feedback during the interview
- Less focus on LeetCode-style problems, more on practical engineering

---

## 2. Most Asked Topics

| Topic | Frequency | Why Apple Asks It |
|-------|-----------|------------------|
| Arrays & Strings | Very High | Foundation, device data |
| Trees | High | File systems, UI hierarchy |
| Design (OOP) | High | Frameworks, system-level design |
| Graphs | Medium | Routing, connectivity |
| DP | Medium | Optimization, animation/timing |
| Concurrency | Medium | iOS/macOS thread safety |
| System-Level | Medium | Memory management, performance |
| Linked Lists | Low-Medium | General DSA knowledge |

### Topic Frequency Graph
```
Arrays:  ████████████████████
Strings: ████████████████████
Trees:   ████████████████
Design:  ████████████████
Graphs:  ████████
DP:      ██████
Concurr: ██████
System:  ██████
```

---

## 3. What Apple Values

### Performance
- Apple focuses heavily on efficiency
- "How would this work on a device with limited memory?"
- Memory usage, CPU cycles, battery impact — all fair game
- They love optimization questions

### Attention to Detail
- Edge cases must be handled perfectly
- Animation smoothness, UI responsiveness
- Memory leaks, off-by-one errors, null pointer checks
- Code quality matters — Apple writes clean, well-documented code

### User Focus
- "How would this affect the user experience?"
- Design decisions should consider real-world usage
- Accessibility, internationalization, localization awareness
- "Would this work on iPhone vs iPad vs Mac?"

### System-Level Thinking
- Understanding of memory hierarchy (cache, RAM, disk)
- How OS handles threads, processes, interrupts
- Performance profiling and optimization experience
- Hardware-software co-design awareness

---

## 4. Types of Problems

### Matrix Problems (Very Common)
- Rotate image (popular)
- Set matrix zeroes
- Game of Life
- Word search
- Spiral matrix

### String Parsing
- Parse and validate URLs
- Expression evaluation
- String encoding/decoding
- Text justification (Word-like)

### Cache Design
- LRU Cache
- Design an in-memory cache
- Thread-safe cache implementation
- Distributed cache

### Tree Manipulation
- Binary tree level order
- Lowest common ancestor
- Validate BST
- Build tree from traversals

### Concurrency
- Thread-safe singleton
- Producer-consumer
- Reader-writer lock
- Deadlock avoidance

---

## 5. Example Problems

### Problem 1: Rotate Image
**Problem:** Rotate n×n matrix 90 degrees clockwise in place.

**Approach:** Transpose + reverse each row.
```java
public void rotate(int[][] matrix) {
    int n = matrix.length;
    // Transpose
    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            int temp = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = temp;
        }
    }
    // Reverse each row
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n / 2; j++) {
            int temp = matrix[i][j];
            matrix[i][j] = matrix[i][n - 1 - j];
            matrix[i][n - 1 - j] = temp;
        }
    }
}
```

### Problem 2: LRU Cache (HIGHLY likely)
**Problem:** Design a cache with O(1) get and put, evicting least recently used.

**Approach:** HashMap + DoublyLinkedList.
```java
class LRUCache {
    class Node {
        int key, value;
        Node prev, next;
        Node(int k, int v) { key = k; value = v; }
    }
    Map<Integer, Node> map;
    Node head, tail;
    int capacity;

    public LRUCache(int capacity) {
        this.capacity = capacity;
        map = new HashMap<>();
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        Node node = map.get(key);
        if (node == null) return -1;
        moveToHead(node);
        return node.value;
    }

    public void put(int key, int value) {
        Node node = map.get(key);
        if (node != null) {
            node.value = value;
            moveToHead(node);
        } else {
            if (map.size() == capacity) {
                Node lru = tail.prev;
                map.remove(lru.key);
                removeNode(lru);
            }
            Node newNode = new Node(key, value);
            map.put(key, newNode);
            addToHead(newNode);
        }
    }

    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    private void addToHead(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
    private void moveToHead(Node node) {
        removeNode(node);
        addToHead(node);
    }
}
```

### Problem 3: Valid Anagram
**Problem:** Check if two strings are anagrams.

**Approach:** Count frequency.
```java
public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] freq = new int[26];
    for (char c : s.toCharArray()) freq[c - 'a']++;
    for (char c : t.toCharArray()) {
        if (--freq[c - 'a'] < 0) return false;
    }
    return true;
}
```

### Problem 4: Word Search
**Problem:** Find if word exists in character grid.

**Approach:** DFS with backtracking.
```java
public boolean exist(char[][] board, String word) {
    for (int i = 0; i < board.length; i++)
        for (int j = 0; j < board[0].length; j++)
            if (board[i][j] == word.charAt(0) && dfs(board, word, i, j, 0))
                return true;
    return false;
}
boolean dfs(char[][] board, String word, int i, int j, int idx) {
    if (idx == word.length()) return true;
    if (i < 0 || i >= board.length || j < 0 || j >= board[0].length) return false;
    if (board[i][j] != word.charAt(idx)) return false;
    char temp = board[i][j];
    board[i][j] = '#';
    boolean found = dfs(board, word, i+1, j, idx+1) ||
                    dfs(board, word, i-1, j, idx+1) ||
                    dfs(board, word, i, j+1, idx+1) ||
                    dfs(board, word, i, j-1, idx+1);
    board[i][j] = temp;
    return found;
}
```

---

## 6. Preparation Strategy

### Timeline: 6-8 weeks

**Weeks 1-2: Core**
- Arrays, strings, trees (all traversals)
- Matrix problems (rotate, spiral, word search)
- HashMap problems (anagram, frequency counting)

**Weeks 3-4: Advanced**
- Caching (LRU, LFU)
- Design patterns (Singleton, Factory, Observer)
- Backtracking with pruning
- Concurrency basics

**Weeks 5-6: Mock + Apple-Specific**
- Solve Apple-tagged LeetCode problems
- Practice system design for mobile
- Review memory management concepts
- 3-4 mock interviews with Apple-specific focus

### Must-Solve Apple Problems
- Rotate Image
- LRU Cache
- Valid Anagram
- Word Search
- Longest Substring Without Repeating
- Merge Intervals
- Design HashMap
- Number of Islands
- Spiral Matrix
- Best Time to Buy and Sell Stock (all variants)
- String Compression
- Game of Life

### Apple-Specific Tips
1. **Know Swift/ObjC** — Apple engineers prefer candidates familiar with their ecosystem
2. **Optimize for mobile** — Mention memory constraints and battery impact
3. **Attention to detail** — Handle every edge case, no matter how rare
4. **Design for Apple products** — If asked about design, consider iPhone/iPad/Mac
5. **Performance aware** — Discuss time/space complexity with hardware context
6. **Team-specific research** — Know what the team works on and tailor your answers
