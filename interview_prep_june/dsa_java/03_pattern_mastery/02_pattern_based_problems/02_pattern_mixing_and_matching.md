# Pattern Mixing and Matching

## Table of Contents
1. When a Problem Requires 2+ Patterns
2. Sliding Window + HashMap → Min Window Substring
3. Binary Search + Sliding Window → Median of Two Sorted Arrays
4. Trie + Backtracking → Word Search II
5. Heap + HashMap → Top K Frequent
6. DFS + DP → Tree DP
7. Union-Find + HashMap → Accounts Merge
8. Multiple Pattern Combinations
9. How to Decompose Complex Problems

---

## 1. When a Problem Requires 2+ Patterns

Complex interview problems rarely test just one pattern. The ability to recognize and combine patterns is what distinguishes strong candidates.

**Why patterns combine:**
- Different aspects of the problem need different algorithms
- One pattern solves a subproblem, another pattern uses that result
- You need optimized data structure access + specific algorithm logic

**Common pattern pairs:**
- Data structure access pattern + search pattern (HashMap + Sliding Window)
- Search pattern + optimization pattern (Binary Search + Greedy)
- Enumeration pattern + validation pattern (Backtracking + Trie)
- Preprocessing pattern + core algorithm (Sorting + Two Pointers)

---

## 2. Sliding Window + HashMap → Min Window Substring

**Problem:** Find minimum window in s that contains all characters of t.

**Why both patterns are needed:**
- **Sliding Window:** Find contiguous substring that satisfies condition, then minimize
- **HashMap:** Track character frequency requirements (O(1) updates for window state)

**Pattern interaction:**
```
Sliding Window (expand/contract) ← window boundaries
               ↓
         HashMap (need[] array) ← required matches
               ↓
         When required == 0 → record window → contract
```

**Implementation:**
```java
public String minWindow(String s, String t) {
    // HashMap component (frequency array)
    int[] need = new int[128];
    for (char c : t.toCharArray()) need[c]++;

    // Sliding window component
    int required = t.length(), left = 0, minLen = Integer.MAX_VALUE, start = 0;

    for (int right = 0; right < s.length(); right++) {
        // Expand window — HashMap update
        if (need[s.charAt(right)]-- > 0) required--;

        // Contract window when condition met
        while (required == 0) {
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                start = left;
            }
            // Remove left — HashMap update
            if (++need[s.charAt(left)] > 0) required++;
            left++;
        }
    }
    return minLen == Integer.MAX_VALUE ? "" : s.substring(start, start + minLen);
}
```

**Other problems using this pair:**
- Longest substring without repeating characters (Sliding Window + boolean freq array)
- Find all anagrams in a string (Sliding Window + freq array comparison)
- Minimum window subsequence (Sliding Window + two-pointer matching)
- Substring with concatenation of all words (Sliding Window + HashMap of word counts)

---

## 3. Binary Search + Sliding Window → Median of Two Sorted Arrays

**Problem:** Find median of two sorted arrays in O(log(min(n,m))).

**Why both patterns:**
- **Binary Search:** Partition the smaller array to find correct split point
- **Sliding Window (partitioning):** The partition creates a "window" that splits both arrays into left/right halves

**Pattern interaction:**
```
Binary Search on partition index in smaller array
        ↓
Check if leftMax ≤ rightMin in both arrays
        ↓
Adjust binary search boundaries based on comparison
```

**Implementation:**
```java
public double findMedianSortedArrays(int[] nums1, int[] nums2) {
    if (nums1.length > nums2.length) return findMedianSortedArrays(nums2, nums1);

    int m = nums1.length, n = nums2.length;
    int left = 0, right = m;

    while (left <= right) {
        int partition1 = left + (right - left) / 2;  // Binary search on partition
        int partition2 = (m + n + 1) / 2 - partition1; // Derived partition

        int maxLeft1 = (partition1 == 0) ? Integer.MIN_VALUE : nums1[partition1 - 1];
        int minRight1 = (partition1 == m) ? Integer.MAX_VALUE : nums1[partition1];
        int maxLeft2 = (partition2 == 0) ? Integer.MIN_VALUE : nums2[partition2 - 1];
        int minRight2 = (partition2 == n) ? Integer.MAX_VALUE : nums2[partition2];

        if (maxLeft1 <= minRight2 && maxLeft2 <= minRight1) {
            if ((m + n) % 2 == 0) {
                return (Math.max(maxLeft1, maxLeft2) + Math.min(minRight1, minRight2)) / 2.0;
            } else {
                return Math.max(maxLeft1, maxLeft2);
            }
        } else if (maxLeft1 > minRight2) {
            right = partition1 - 1; // too far right
        } else {
            left = partition1 + 1; // too far left
        }
    }
    return 0.0;
}
```

**Other problems using binary search + another pattern:**
- Split array largest sum (Binary Search + Greedy simulation)
- Kth smallest element in sorted matrix (Binary Search + Counting in 2D)
- Find kth smallest pair distance (Binary Search + Two Pointers)

---

## 4. Trie + Backtracking → Word Search II

**Problem:** Find all words from dictionary that exist in a character grid.

**Why both patterns:**
- **Trie:** Efficiently store and search dictionary by prefix (O(L) for each prefix check)
- **Backtracking (DFS):** Explore all possible paths in the grid, pruning when prefix doesn't match

**Pattern interaction:**
```
Backtracking (DFS on grid) traverses paths
        ↓
At each cell, check Trie for current prefix
        ↓
If prefix doesn't exist → prune (backtrack)
If word found → add to result (keep searching for longer words)
```

**Implementation:**
```java
class Solution {
    class TrieNode {
        TrieNode[] children = new TrieNode[26];
        String word;
    }

    public List<String> findWords(char[][] board, String[] words) {
        // Build Trie (Trie pattern)
        TrieNode root = new TrieNode();
        for (String w : words) {
            TrieNode node = root;
            for (char c : w.toCharArray()) {
                int idx = c - 'a';
                if (node.children[idx] == null) node.children[idx] = new TrieNode();
                node = node.children[idx];
            }
            node.word = w;
        }

        // Backtracking on grid
        List<String> result = new ArrayList<>();
        for (int i = 0; i < board.length; i++) {
            for (int j = 0; j < board[0].length; j++) {
                backtrack(board, i, j, root, result);
            }
        }
        return result;
    }

    private void backtrack(char[][] board, int i, int j, TrieNode node, List<String> result) {
        if (i < 0 || i >= board.length || j < 0 || j >= board[0].length) return;
        char c = board[i][j];
        if (c == '#' || node.children[c - 'a'] == null) return;

        node = node.children[c - 'a'];
        if (node.word != null) {
            result.add(node.word);
            node.word = null; // avoid duplicates
        }

        board[i][j] = '#'; // mark visited
        backtrack(board, i + 1, j, node, result);
        backtrack(board, i - 1, j, node, result);
        backtrack(board, i, j + 1, node, result);
        backtrack(board, i, j - 1, node, result);
        board[i][j] = c; // unmark
    }
}
```

**Other problems using Trie + another pattern:**
- Palindrome pairs (Trie + custom search)
- Design search autocomplete system (Trie + Heap for top results)
- Stream of characters (Trie + Sliding Window for string matching)
- Word break II (Trie + DP/Backtracking)

---

## 5. Heap + HashMap → Top K Frequent

**Problem:** Find K most frequent elements in an array.

**Why both patterns:**
- **HashMap:** Count frequency of each element (O(n) pass)
- **Heap:** Maintain top K elements (O(n log k))

**Pattern interaction:**
```
HashMap (element → frequency count)
        ↓
For each entry → add to Min-Heap (ordered by frequency)
        ↓
Keep heap size ≤ K → poll smallest when > K
        ↓
Heap contains K most frequent elements
```

**Implementation:**
```java
public int[] topKFrequent(int[] nums, int k) {
    // HashMap pattern
    Map<Integer, Integer> freq = new HashMap<>();
    for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);

    // Min-Heap pattern (ordered by frequency)
    PriorityQueue<Integer> heap = new PriorityQueue<>((a, b) -> freq.get(a) - freq.get(b));

    for (int key : freq.keySet()) {
        heap.offer(key);
        if (heap.size() > k) heap.poll();
    }

    int[] result = new int[k];
    for (int i = k - 1; i >= 0; i--) result[i] = heap.poll();
    return result;
}
```

**Alternative with Bucket Sort (HashMap + Bucket Sort):**
```java
public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);

    // Bucket sort: index = frequency
    List<Integer>[] buckets = new List[nums.length + 1];
    for (int key : freq.keySet()) {
        int f = freq.get(key);
        if (buckets[f] == null) buckets[f] = new ArrayList<>();
        buckets[f].add(key);
    }

    int[] result = new int[k];
    int idx = 0;
    for (int f = buckets.length - 1; f >= 0 && idx < k; f--) {
        if (buckets[f] != null) {
            for (int num : buckets[f]) {
                result[idx++] = num;
                if (idx == k) break;
            }
        }
    }
    return result;
}
```

**Other problems using Heap + HashMap:**
- Top K frequent words (Heap + HashMap, tie-break lexicographically)
- Sort characters by frequency (Heap + HashMap, rebuild string)
- Frequency sort (Heap + HashMap)
- Top K frequent elements in data stream (Heap + HashMap, dynamic)

---

## 6. DFS + DP → Tree DP

**How to identify:** Problems where you need to compute something at each node using its children's results, AND the results depend on different states of the node.

**Common tree DP problems:**
- House Robber III (with/without node)
- Binary tree cameras (3 states per node)
- Maximum path sum (path through node vs not)
- Largest BST subtree

**Template:**
```java
// Post-order DFS + State DP
int[] dfs(TreeNode node) {
    if (node == null) return new int[]{baseCase, baseCase};

    // DFS on children (post-order)
    int[] left = dfs(node.left);
    int[] right = dfs(node.right);

    // DP: combine child results based on node state
    int state0 = compute using left[1] + right[1]; // node is in state 0
    int state1 = compute using left[0] + right[0]; // node is in state 1
    // etc.

    return new int[]{state0, state1};
}
```

**House Robber III (DFS + DP):**
```java
public int rob(TreeNode root) {
    int[] result = robHelper(root);
    return Math.max(result[0], result[1]);
}
// [0] = max with robbing this node, [1] = max without robbing this node
int[] robHelper(TreeNode node) {
    if (node == null) return new int[]{0, 0};
    int[] left = robHelper(node.left);
    int[] right = robHelper(node.right);
    int withNode = node.val + left[1] + right[1]; // can't rob children
    int withoutNode = Math.max(left[0], left[1]) + Math.max(right[0], right[1]);
    return new int[]{withNode, withoutNode};
}
```

**Binary Tree Cameras (DFS + DP with 3 states):**
```java
int cameras = 0;
public int minCameraCover(TreeNode root) {
    int state = dfs(root); // 0 = covered, 1 = has camera, 2 = needs coverage
    return state == 2 ? cameras + 1 : cameras;
}
int dfs(TreeNode node) {
    if (node == null) return 0; // covered (null doesn't need camera)
    int left = dfs(node.left);
    int right = dfs(node.right);
    if (left == 2 || right == 2) {
        cameras++; // need to place camera here
        return 1;
    }
    if (left == 1 || right == 1) return 0; // covered by child
    return 2; // needs coverage from parent
}
```

---

## 7. Union-Find + HashMap → Accounts Merge

**Problem:** Merge accounts that share common emails.

**Why both patterns:**
- **Union-Find:** Group accounts that share emails into connected components
- **HashMap:** Map each email to the first account that has it (for union operation)

**Pattern interaction:**
```
HashMap: email → first account index
        ↓
For each account's emails:
  If email already in HashMap → union(current account, mapped account)
  Else → add email to HashMap with current account index
        ↓
Build result: for each root → combine all emails → sort → add name
```

**Implementation:**
```java
public List<List<String>> accountsMerge(List<List<String>> accounts) {
    int n = accounts.size();
    UnionFind uf = new UnionFind(n);
    Map<String, Integer> emailToId = new HashMap<>();

    // Union-Find + HashMap: build connections
    for (int i = 0; i < n; i++) {
        for (int j = 1; j < accounts.get(i).size(); j++) {
            String email = accounts.get(i).get(j);
            if (emailToId.containsKey(email)) {
                uf.union(emailToId.get(email), i);
            } else {
                emailToId.put(email, i);
            }
        }
    }

    // Build result: root → list of emails
    Map<Integer, TreeSet<String>> rootToEmails = new HashMap<>();
    for (String email : emailToId.keySet()) {
        int root = uf.find(emailToId.get(email));
        rootToEmails.computeIfAbsent(root, k -> new TreeSet<>()).add(email);
    }

    // Format output
    List<List<String>> result = new ArrayList<>();
    for (int root : rootToEmails.keySet()) {
        List<String> list = new ArrayList<>(rootToEmails.get(root));
        list.add(0, accounts.get(root).get(0)); // add name at front
        result.add(list);
    }
    return result;
}
```

**Other problems using Union-Find + another pattern:**
- Number of islands II (Union-Find + Grid traversal)
- Evaluate division (Union-Find + weighted edges)
- Redundant connection II (Union-Find + in-degree tracking for directed)
- Longest consecutive sequence (Union-Find + HashMap for value → index)

---

## 8. Multiple Pattern Combinations

### Example 1: Design a Search Autocomplete System
**Patterns used: Trie + Heap + HashMap**

```
Trie: Store phrases by prefix (fast prefix search)
  ↓
Heap: At each node, maintain top 3 hot sentences
  ↓
HashMap: Map sentence → frequency (for updating counts)
```

### Example 2: Minimum Window Subsequence (not substring)
**Patterns used: Sliding Window + DP + Two Pointers**

```
Two Pointers: Match t in s forward
  ↓
DP: Store next occurrence positions for each character
  ↓
Sliding Window: Find min window that contains t as subsequence
```

### Example 3: Bus Routes (Minimum Buses)
**Patterns used: BFS + HashMap + Graph Construction**

```
HashMap: Route → bus stops, Bus stop → routes (bidirectional)
  ↓
Graph: Routes as nodes, shared stops as edges
  ↓
BFS: Shortest path from source route to target route
```

### Example 4: Design Twitter (News Feed)
**Patterns used: HashMap + Heap + OOP Design + Merge K Lists**

```
HashMap: user → tweets, user → followers (OOP)
  ↓
Merge K sorted lists: Get recent tweets from followees
  ↓
Heap: Combine tweets from all followees by timestamp
```

---

## 9. How to Decompose Complex Problems

### Step-by-step decomposition process

**1. Identify what the problem asks for** — parse the output:
- Is it a number (min, max, count)? → Optimization/DP/Counting
- Is it a list? → Enumeration/Search
- Is it yes/no? → Feasibility/Existence

**2. Break the problem into subproblems:**
```
Example: "Find all words from dictionary in a character grid"
Subproblems:
  (a) Efficiently store dictionary for prefix lookup → Trie
  (b) Explore all paths in grid → Backtracking/DFS
  (c) Avoid redundant search → Prune with Trie prefix check
```

**3. Identify the core pattern:**
- Look at the input type: array, string, tree, graph
- Look at constraints: array size, value ranges, sorted?
- Look at keywords: "contiguous", "subsequence", "minimum", "maximum"

**4. Map each subproblem to a pattern:**
| Subproblem | Pattern | Why |
|------------|---------|-----|
| Quick lookup by prefix | Trie | O(L) prefix check |
| Explore paths in 2D grid | Backtracking | Need to try all paths |
| Skip invalid prefixes | Pruning | Stop early when prefix invalid |
| Avoid visiting same cell | Mark visited | Standard backtracking |

**5. Connect the patterns:**
- How does the output of pattern 1 feed into pattern 2?
- What data structure bridges them?

**6. Verify the combination works:**
- Do the time/space complexities combine well?
- Are there any conflicting assumptions?

### Common Pattern Combinations Matrix

| Primary Pattern | Can Combine With | Example |
|----------------|-----------------|---------|
| Sliding Window | HashMap, Deque, Heap | Min window substring |
| Two Pointers | Sorting, Prefix Sum | 3Sum |
| Binary Search | Greedy, Sliding Window, DP | Split array |
| Backtracking | Trie, DP (memo), Pruning | Word search |
| BFS | HashMap, PriorityQueue | Word Ladder |
| DFS | DP (memo), Stack, Coloring | Tree DP |
| Union-Find | HashMap, Graph construction | Accounts merge |
| Heap | HashMap, K-way merge | Top K frequent |
| Trie | Backtracking, Heap | Search autocomplete |
| DP | Binary Search, DFS, Bitmask | LIS with patience |
