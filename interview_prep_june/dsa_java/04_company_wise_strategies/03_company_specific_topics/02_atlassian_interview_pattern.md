# Atlassian Interview Pattern

> "Atlassian has a unique interview process focused on practical problems and product thinking. They test arrays, strings, trees, and design with emphasis on CRUD operations, search/rank, and permission systems."

---

## 1. Company Overview

- **Package:** ₹20-45 LPA (freshers), higher for experienced
- **Hiring:** Campus + Off-campus + Referrals
- **Rounds:** Online Test → Phone Screen → Onsite (4-5 rounds)
- **Focus:** DSA, System Design, Product Thinking, Practical Problems
- **Key Differentiator:** **Practical problems** and **product thinking**

---

## 2. Interview Format

### Recruiter Screen (30 min)
- Background review and role discussion
- Focus on product-oriented engineering
- Discussion of past projects and impact

### Technical Phone Screen (45-60 min)
- 1-2 coding problems (Medium to Hard)
- Often includes system design discussion
- Focus on practical, production-ready solutions
- Strong communication expected

### On-site (4-5 rounds, 45-60 min each)

| Round | Focus | Difficulty |
|-------|-------|------------|
| Round 1 | DSA Coding (Arrays/Strings) | Medium-Hard |
| Round 2 | DSA Coding (Trees/Design) | Medium-Hard |
| Round 3 | System Design | Medium |
| Round 4 | Product Sense / Behavioral | Culture fit |
| Round 5 | Hiring Manager | Team fit |

### Key Differences from Other Companies
- **Practical problems** — They want production-ready solutions
- **Product thinking** — How does this feature affect users?
- **CRUD operations** — Database-backed problems
- **Search/rank problems** — Jira, Confluence-like features
- **Permission systems** — Access control, roles
- **Well-structured** — Clear, fair interview process

---

## 3. Most Asked Topics

### Topic Priority

| Priority | Topic | Frequency | Notes |
|----------|-------|-----------|-------|
| 1 | Arrays | 85% | Medium-Hard, optimization |
| 2 | Strings | 80% | Parsing, pattern matching |
| 3 | Trees | 75% | BST, binary tree, trie |
| 4 | System Design | 70% | Scalable, product-focused |
| 5 | HashMaps | 60% | Frequency, grouping |
| 6 | DP | 55% | Medium difficulty |
| 7 | Graphs | 45% | Basic graph problems |

### Topic Frequency Graph
```
Arrays:     ████████████████████
Strings:    ██████████████████
Trees:      █████████████████
Sys Design: ██████████████
HashMaps:   ████████████
DP:         ███████████
Graphs:     █████████
```

### What Makes Atlassian Different
- **Practical problems** — Not just algorithms, but real systems
- **Product thinking** — How does this feature serve users?
- **CRUD operations** — Database-backed problems
- **Search/rank** — Jira, Confluence-like features
- **Permission systems** — Access control, roles, inheritance
- **Clean code** — Production-ready solutions

---

## 4. Types of Problems

### Practical / CRUD Problems
- Design a task management system (Jira-like)
- Design a wiki page system (Confluence-like)
- Implement search functionality
- Implement ranking/filtering
- Design permission/access control

### Array/String Problems
- Sliding window variants
- Two pointer techniques
- String parsing
- Subarray problems
- Sorting and searching

### Tree Problems
- BST operations
- Trie for autocomplete
- Tree serialization
- Path problems
- Level-order traversal

### Design Problems
- Design a project management tool
- Design a collaboration feature
- Design a notification system
- Design a search engine
- Design a permission system

---

## 5. Example Problems

### Problem 1: Search in Rotated Sorted Array
**Why Atlassian asks this:** Search problems are fundamental; tests binary search mastery.

```java
public class SearchRotated {

    // APPROACH: Modified binary search
    // At least one half is always sorted
    // Determine which half is sorted, then search accordingly
    
    public static int search(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (nums[mid] == target) return mid;
            
            // Left half is sorted
            if (nums[left] <= nums[mid]) {
                if (target >= nums[left] && target < nums[mid]) {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            }
            // Right half is sorted
            else {
                if (target > nums[mid] && target <= nums[right]) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
        }
        
        return -1;
    }

    public static void main(String[] args) {
        int[] nums = {4, 5, 6, 7, 0, 1, 2};
        System.out.println(search(nums, 0)); // 4
        System.out.println(search(nums, 3)); // -1
    }
}
```

**Time:** O(log n) | **Space:** O(1)

---

### Problem 2: Trie (Prefix Search)
**Why Atlassian asks this:** Autocomplete and search are core to Jira/Confluence.

```java
public class Trie {

    static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEnd = false;
    }
    
    private TrieNode root;
    
    public Trie() {
        root = new TrieNode();
    }
    
    public void insert(String word) {
        TrieNode current = root;
        for (char c : word.toCharArray()) {
            int index = c - 'a';
            if (current.children[index] == null) {
                current.children[index] = new TrieNode();
            }
            current = current.children[index];
        }
        current.isEnd = true;
    }
    
    public boolean search(String word) {
        TrieNode node = findNode(word);
        return node != null && node.isEnd;
    }
    
    public boolean startsWith(String prefix) {
        return findNode(prefix) != null;
    }
    
    private TrieNode findNode(String prefix) {
        TrieNode current = root;
        for (char c : prefix.toCharArray()) {
            int index = c - 'a';
            if (current.children[index] == null) return null;
            current = current.children[index];
        }
        return current;
    }

    public static void main(String[] args) {
        Trie trie = new Trie();
        trie.insert("apple");
        trie.insert("app");
        trie.insert("application");
        
        System.out.println(trie.search("apple"));     // true
        System.out.println(trie.search("app"));       // true
        System.out.println(trie.search("appl"));      // false
        System.out.println(trie.startsWith("appl"));  // true
    }
}
```

**Time:** O(m) for insert/search/startsWith where m = word length | **Space:** O(n × m × alphabet)

---

### Problem 3: LRU Cache
**Why Atlassian asks this:** Cache management is core to Jira/Confluence performance.

```java
import java.util.*;

public class LRUCache {

    private class Node {
        int key, value;
        Node prev, next;
        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }
    
    private int capacity;
    private Map<Integer, Node> map;
    private Node head, tail;
    
    public LRUCache(int capacity) {
        this.capacity = capacity;
        map = new HashMap<>();
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head.next = tail;
        tail.prev = head;
    }
    
    private void addToFront(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
    
    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    private void moveToHead(Node node) {
        removeNode(node);
        addToFront(node);
    }
    
    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        moveToHead(node);
        return node.value;
    }
    
    public void put(int key, int value) {
        if (map.containsKey(key)) {
            Node node = map.get(key);
            node.value = value;
            moveToHead(node);
        } else {
            Node newNode = new Node(key, value);
            map.put(key, newNode);
            addToFront(newNode);
            
            if (map.size() > capacity) {
                Node lru = tail.prev;
                removeNode(lru);
                map.remove(lru.key);
            }
        }
    }

    public static void main(String[] args) {
        LRUCache cache = new LRUCache(2);
        cache.put(1, 1);
        cache.put(2, 2);
        System.out.println(cache.get(1)); // 1
        cache.put(3, 3); // Evicts key 2
        System.out.println(cache.get(2)); // -1
    }
}
```

**Time:** O(1) for get/put | **Space:** O(capacity)

---

### Problem 4: Number of Islands
```java
public class NumberOfIslands {

    public static int numIslands(char[][] grid) {
        if (grid == null || grid.length == 0) return 0;
        
        int count = 0;
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[0].length; j++) {
                if (grid[i][j] == '1') {
                    count++;
                    dfs(grid, i, j);
                }
            }
        }
        return count;
    }
    
    private static void dfs(char[][] grid, int row, int col) {
        if (row < 0 || row >= grid.length || col < 0 
            || col >= grid[0].length || grid[row][col] == '0') {
            return;
        }
        
        grid[row][col] = '0';
        
        dfs(grid, row + 1, col);
        dfs(grid, row - 1, col);
        dfs(grid, row, col + 1);
        dfs(grid, row, col - 1);
    }

    public static void main(String[] args) {
        char[][] grid = {
            {'1','1','0','0','0'},
            {'1','1','0','0','0'},
            {'0','0','1','0','0'},
            {'0','0','0','1','1'}
        };
        System.out.println(numIslands(grid)); // 3
    }
}
```

**Time:** O(m × n) | **Space:** O(m × n)

---

### Problem 5: Merge Intervals
```java
import java.util.*;

public class MergeIntervals {

    public static int[][] merge(int[][] intervals) {
        if (intervals.length <= 1) return intervals;
        
        Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
        List<int[]> merged = new ArrayList<>();
        merged.add(intervals[0]);
        
        for (int i = 1; i < intervals.length; i++) {
            int[] last = merged.get(merged.size() - 1);
            if (intervals[i][0] <= last[1]) {
                last[1] = Math.max(last[1], intervals[i][1]);
            } else {
                merged.add(intervals[i]);
            }
        }
        
        return merged.toArray(new int[0][]);
    }

    public static void main(String[] args) {
        int[][] intervals = {{1,3},{2,6},{8,10},{15,18}};
        int[][] result = merge(intervals);
        for (int[] interval : result) {
            System.out.print(Arrays.toString(interval) + " ");
        }
        // [[1,6], [8,10], [15,18]]
    }
}
```

**Time:** O(n log n) | **Space:** O(n)

---

## 6. Preparation Strategy

### Focus Areas (4-Week Plan)

#### Week 1: Arrays and Strings
- [ ] Sliding window problems (10 problems)
- [ ] Two pointer technique (10 problems)
- [ ] String parsing (10 problems)
- [ ] Binary search variants (5 problems)
- [ ] Practice: 25 problems

#### Week 2: Trees and HashMaps
- [ ] BST operations (10 problems)
- [ ] Trie implementation (5 problems)
- [ ] Binary tree traversals (10 problems)
- [ ] HashMap patterns (5 problems)
- [ ] Practice: 20 problems

#### Week 3: Design and Practical Problems
- [ ] LRU Cache (master this)
- [ ] CRUD system design
- [ ] Search/rank implementation
- [ ] Permission system design
- [ ] Practice: 5 designs + 10 coding problems

#### Week 4: System Design and Mocks
- [ ] Jira-like system design
- [ ] Confluence-like system design
- [ ] Scalability concepts
- [ ] Mock interviews (3-5 sessions)
- [ ] Review and consolidate

### Atlassian-Specific Tips
1. **Practical problems** — Think about real systems, not just algorithms
2. **Product thinking** — How does this feature serve users?
3. **CRUD operations** — Database-backed problems are common
4. **Search/rank** — Jira, Confluence-like features
5. **Permission systems** — Access control, roles
6. **Clean code** — Production-ready solutions
7. **System design** — Scalable, product-focused
8. **Communication** — Explain your thought process clearly

### Common Follow-up Questions
- "How would this work for millions of users?"
- "How would you handle concurrent edits?"
- "What if the data doesn't fit in memory?"
- "How would you implement search/filter?"
- "How would you handle permissions/roles?"

### Resources
- LeetCode Medium-Hard problems
- System design for collaboration tools
- Trie implementation patterns
- Permission system design patterns

---

> **Remember:** Atlassian values practical, product-focused engineering. They want you to build systems, not just solve algorithms. Think about Jira and Confluence when approaching problems — search, filtering, permissions, and collaboration are key.
