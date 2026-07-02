# Google Interview Pattern

## Table of Contents
1. Interview Format
2. Most Asked Topics
3. What Google Values
4. Types of Problems
5. Example Problems with Approaches
6. Preparation Strategy
7. Common Mistakes

---

## 1. Interview Format

### Phone Screen (45-60 min)
- 1-2 coding problems on Google Docs (no syntax highlighting)
- Focus on algorithmic thinking, not perfect syntax
- Interviewer shares a Doc, you write code
- Expect follow-ups and complexity analysis

### On-site (4-5 rounds, each 45 min)
- **Coding rounds** (2-3): Algorithm-heavy, data structure manipulation
- **General Cognitive Ability** (1): Problem-solving without clear right answer
- **Googleyness** (1): Leadership, cultural fit
- Sometimes: **System Design** (for senior positions)

### Key Differences from Other FAANG
- More emphasis on optimal algorithms (not just working code)
- Questions often have hidden complexity
- Interviewers are trained to NOT give hints (unlike Meta)
- Heavy focus on scalability and optimization

---

## 2. Most Asked Topics

| Topic | Frequency | Why Google Asks It |
|-------|-----------|-------------------|
| Graphs (BFS/DFS) | Very High | Maps, search, ranking, dependency resolution |
| Dynamic Programming | Very High | Caching, optimization, path finding |
| Trees (BST, Binary Tree) | High | Search indices, hierarchical data |
| Arrays & Strings | High | Foundation of most problems |
| HashMaps | High | Fast lookup is essential |
| Prefix Sum / Range Queries | Medium | Large-scale data processing |
| Tries | Medium | Search, autocomplete |
| Union-Find | Medium | Connectivity, clustering |
| Design (OOP + DS) | Medium | LRU, serialization |

### Topic Frequency Graph
```
Graphs: ████████████████████
DP:     ████████████████████
Trees:  ████████████████
Arrays: ████████████████
Hash:   ████████████
Design: ████████
Trie:   ██████
UF:     ██████
```

---

## 3. What Google Values

### Optimal Solutions
- Brute force then optimize is expected, but they want O(n) or O(n log n) final solutions
- Always analyze time and space complexity after coding
- Be ready to discuss trade-offs between approaches

### Scalability
- "What if the input is 10x larger?"
- "How would you handle streaming data?"
- "Can this work in a distributed system?"

### Clean Code
- Meaningful variable names (not `a`, `b`, `c`)
- Modular functions with single responsibility
- Proper handling of edge cases (null, empty, large values)
- No magic numbers

### Communication
- Explain your thought process as you code
- Discuss trade-offs before implementing
- Ask clarifying questions early
- Summarize your approach before writing code

---

## 4. Types of Problems

### Tricky Binary Search
```java
// Google loves "find in rotated sorted array" variants
public int search(int[] nums, int target) {
    // Detect sorted half, binary search within it
}
```

### Graph Traversal
```java
// Number of Islands, Word Ladder, Robot Room Cleaner
```

### DP Optimization
```java
// Usually can't be solved with just O(n²) — needs optimization
// Google: "Minimum number of coins" but with constraints that require O(amount)
```

### Design Questions
- Serialize/Deserialize Binary Tree (almost every Google onsite has a variant)
- LRU Cache (classic)
- Design a data structure with specific operations in O(1)

### Mathematical / Number Theory
- Count primes (Sieve of Eratosthenes)
- Random pick with weight
- Power function (fast exponentiation)

---

## 5. Example Problems with Approaches

### Problem 1: Word Ladder
**Problem:** Begin word → end word, change one letter at a time, each intermediate must be in dictionary.

**Approach:**
- BFS on implicit graph (words are nodes, one-character diff is edge)
- Bidirectional BFS for optimization (O(n^(k/2)) instead of O(n^k))
- Preprocess dictionary: for each word, generate all possible intermediate patterns

```java
public int ladderLength(String beginWord, String endWord, List<String> wordList) {
    Set<String> dict = new HashSet<>(wordList);
    if (!dict.contains(endWord)) return 0;

    Set<String> beginSet = new HashSet<>(Arrays.asList(beginWord));
    Set<String> endSet = new HashSet<>(Arrays.asList(endWord));
    Set<String> visited = new HashSet<>();
    int steps = 1;

    while (!beginSet.isEmpty() && !endSet.isEmpty()) {
        // Always expand the smaller set (bidirectional BFS)
        if (beginSet.size() > endSet.size()) {
            Set<String> temp = beginSet;
            beginSet = endSet;
            endSet = temp;
        }

        Set<String> nextSet = new HashSet<>();
        for (String word : beginSet) {
            char[] chars = word.toCharArray();
            for (int i = 0; i < chars.length; i++) {
                char orig = chars[i];
                for (char c = 'a'; c <= 'z'; c++) {
                    chars[i] = c;
                    String next = new String(chars);
                    if (endSet.contains(next)) return steps + 1;
                    if (dict.contains(next) && visited.add(next)) {
                        nextSet.add(next);
                    }
                }
                chars[i] = orig;
            }
        }
        beginSet = nextSet;
        steps++;
    }
    return 0;
}
```

### Problem 2: Serialize and Deserialize Binary Tree
**Problem:** Design algorithms to serialize and deserialize a binary tree.

**Approach:** Preorder traversal with null markers.
```java
public String serialize(TreeNode root) {
    StringBuilder sb = new StringBuilder();
    serialize(root, sb);
    return sb.toString();
}
private void serialize(TreeNode node, StringBuilder sb) {
    if (node == null) { sb.append("null,"); return; }
    sb.append(node.val).append(",");
    serialize(node.left, sb);
    serialize(node.right, sb);
}

public TreeNode deserialize(String data) {
    Queue<String> nodes = new LinkedList<>(Arrays.asList(data.split(",")));
    return deserialize(nodes);
}
private TreeNode deserialize(Queue<String> nodes) {
    String val = nodes.poll();
    if (val.equals("null")) return null;
    TreeNode node = new TreeNode(Integer.parseInt(val));
    node.left = deserialize(nodes);
    node.right = deserialize(nodes);
    return node;
}
```

### Problem 3: Trapping Rain Water
**Problem:** Compute trapped water between bars.

**Approach:** Two pointers with leftMax/rightMax (O(n) time, O(1) space).

### Problem 4: Longest Substring Without Repeating Characters
**Problem:** Find length of longest substring without repeating chars.

**Approach:** Sliding window with index array (O(n)).

---

## 6. Preparation Strategy

### Timeline: 8-12 weeks

**Weeks 1-2: Foundations**
- Review all data structures (Arrays, LinkedList, Stack, Queue, Tree, Heap, HashMap)
- Master recursion and tree traversals
- Practice 10 easy problems daily

**Weeks 3-4: Core Algorithms**
- Graphs: BFS, DFS, Topological sort, Union-Find
- DP: Knapsack, LCS, LIS, Grid DP, Interval DP
- Practice 5 medium problems daily

**Weeks 5-6: Advanced Topics**
- Tries, Segment Trees, Binary Indexed Trees
- Monotonic Stack/Queue
- Backtracking with pruning
- Practice 4-5 hard problems daily

**Weeks 7-8: Mock Interviews + Review**
- 3-4 full-length mock interviews per week
- Review mistakes and weak areas
- Focus on speed (45 min per problem, not 3 hours)

### Recommended Resources
- **LeetCode**: Google tagged questions (last 6 months)
- **System Design**: "Designing Data-Intensive Applications" (DDIA)
- **Cracking the Coding Interview**: General prep
- **Google's Technical Development Guide**: Online resource

---

## 7. Common Mistakes to Avoid

| Mistake | Why It Hurts | Better Approach |
|---------|-------------|-----------------|
| Jumping to code too fast | Miss edge cases, wrong approach | Spend 5 min analyzing |
| Not asking clarifying questions | Solve wrong problem | "Are there constraints?" "Is the input sorted?" |
| Ignoring edge cases | Solution breaks on empty/single | Handle null, empty, large tests |
| Not analyzing complexity | Can't justify your solution | State O() before coding |
| Using brute force without optimizing | Expected optimal solution | Brute force → identify redundant work → optimize |
| Poor communication | Interviewer can't follow | Narrate your thought process |
| Giving up too easily | Shows lack of persistence | Try something, even if suboptimal |
| Over-complicating solution | Unnecessary complexity | Start simple, then optimize |
| Not testing with examples | Miss obvious bugs | Trace through 1-2 examples |

### Google-Specific Mistakes
1. **Not considering scale:** "What if this runs on Google Search index?"
2. **Writing unmodifiable code:** Single giant method, no helper functions
3. **Forgetting to ask about the problem context:** E.g., "Is this real-time or batch?"
4. **Assuming too much:** "This is just like LeetCode problem X" — they always have twists
