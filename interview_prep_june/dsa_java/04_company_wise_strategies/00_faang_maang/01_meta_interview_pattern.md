# Meta (Facebook) Interview Pattern

## Table of Contents
1. Interview Format
2. Most Asked Topics
3. What Meta Values
4. Types of Problems
5. Example Problems with Approaches
6. Preparation Strategy
7. Common Mistakes

---

## 1. Interview Format

### Phone Screen (45 min)
- 1-2 coding problems on CoderPad (shared editor)
- Meta uses a collaborative coding environment with run button
- You may need to actually compile and run your code
- Strong emphasis on WORKING code

### On-site (4-5 rounds, 45 min each)
- **Coding rounds** (2): Usually no system design unless senior
- **Behavioral / Culture fit** (1): "Why Meta?", "Tell me about a time..."
- **Design / Product sense** (1): For senior roles
- **Hiring manager** (1): Mix of behavior and technical

### Key Differences from Google
- Meta interviewers are MORE interactive — they give hints
- Focus is on WORKING code, not necessarily the most optimal
- You should code FAST — they want to see progress
- More emphasis on strings and arrays than graphs/DP

---

## 2. Most Asked Topics

| Topic | Frequency | Why Meta Asks It |
|-------|-----------|-----------------|
| Strings | Very High | Text processing, search, posts |
| Arrays | Very High | Foundation, data feed processing |
| Trees (BST, Binary Tree) | High | Social graph, page hierarchy |
| Recursion / Backtracking | High | Subset generation, search |
| Hashing | High | User data, caching |
| Intervals | Medium | Time-based features, scheduling |
| Linked Lists | Medium | Timeline, feed ordering |
| Heaps | Medium | Trending topics, Top K |
| Graphs (BFS) | Medium | Friend connections, groups |
| DP | Medium-Low | Optimization for ads, ranking |

### Topic Frequency Graph
```
Strings: ████████████████████
Arrays:  ████████████████████
Trees:   ████████████████
Recur.:  ██████████████
Hash:    ██████████████
Interv.: ████████
LL:      ████████
Heap:    ██████
Graphs:  ██████
DP:      ████
```

---

## 3. What Meta Values

### Working Code Above All
- Your code must compile and run
- 80% optimal + working > 100% optimal + not working
- Handle edge cases explicitly (null, empty, overflow)
- Use proper data structures (HashMap when you need O(1) lookup)

### Communication
- Meta interviews are collaborative conversations
- They want to see how you think through problems
- "Be loud" — talk through your reasoning
- Ask for hints if stuck (they're trained to give them)

### Trade-off Analysis
- "Why did you choose ArrayList over LinkedList?"
- "HashMap vs TreeMap — which is better here?"
- "Time vs space complexity trade-offs"

### Speed
- Meta interviewers expect quick coding
- Don't spend 10 minutes analyzing — start coding within 5 min
- They'd rather see you code a suboptimal solution and optimize it

---

## 4. Types of Problems

### Substring / Subarray Problems
- Longest substring without repeating (classic Meta)
- Minimum window substring
- Palindromic substrings
- Subarray sum equals K

### Tree Manipulation
- Binary tree level order traversal (very common)
- Validate BST
- Lowest common ancestor
- Binary tree right side view
- Serialize/Deserialize (less common than Google)

### Interval Problems
- Merge intervals
- Insert interval
- Meeting rooms II

### String Parsing
- Valid palindrome (with non-alphanumeric)
- String to integer (atoi)
- Expression evaluation
- Basic calculator

### Design Problems (for senior)
- Design Facebook News Feed
- Design a URL shortener
- Design a chat system

---

## 5. Example Problems with Approaches

### Problem 1: Valid Palindrome II
**Problem:** Can the string be a palindrome by deleting at most one character?

**Approach:** Two pointers from ends. On mismatch, check both skip-left and skip-right.

```java
public boolean validPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        if (s.charAt(left) != s.charAt(right)) {
            // Try skipping left OR skipping right
            return isPalindrome(s, left + 1, right)
                || isPalindrome(s, left, right - 1);
        }
        left++;
        right--;
    }
    return true;
}

private boolean isPalindrome(String s, int left, int right) {
    while (left < right) {
        if (s.charAt(left++) != s.charAt(right--)) return false;
    }
    return true;
}
```

### Problem 2: Binary Tree Level Order Traversal
**Problem:** Return level-by-level traversal of binary tree.

**Approach:** BFS with queue, track level size.

```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    while (!queue.isEmpty()) {
        int size = queue.size();
        List<Integer> level = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            level.add(node.val);
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        result.add(level);
    }
    return result;
}
```

### Problem 3: K Closest Points to Origin
**Problem:** Find K closest points to origin (0,0).

**Approach:** Max heap of size K.
```java
public int[][] kClosest(int[][] points, int k) {
    PriorityQueue<int[]> pq = new PriorityQueue<>(
        (a, b) -> (b[0]*b[0] + b[1]*b[1]) - (a[0]*a[0] + a[1]*a[1])
    );
    for (int[] p : points) {
        pq.offer(p);
        if (pq.size() > k) pq.poll();
    }
    int[][] result = new int[k][2];
    for (int i = 0; i < k; i++) result[i] = pq.poll();
    return result;
}
```

### Problem 4: Meeting Rooms II
**Problem:** Minimum number of conference rooms required.

**Approach:** Sort starts and ends separately, two pointers.
```java
public int minMeetingRooms(int[][] intervals) {
    int n = intervals.length;
    int[] start = new int[n], end = new int[n];
    for (int i = 0; i < n; i++) {
        start[i] = intervals[i][0];
        end[i] = intervals[i][1];
    }
    Arrays.sort(start);
    Arrays.sort(end);
    int rooms = 0, endIdx = 0;
    for (int i = 0; i < n; i++) {
        if (start[i] < end[endIdx]) rooms++;
        else endIdx++;
    }
    return rooms;
}
```

### Problem 5: Remove Invalid Parentheses
**Problem:** Remove minimum parentheses to make string valid.

**Approach:** BFS trying all removals, check validity.
```java
public List<String> removeInvalidParentheses(String s) {
    List<String> result = new ArrayList<>();
    if (s == null) return result;
    Set<String> visited = new HashSet<>();
    Queue<String> queue = new LinkedList<>();
    queue.offer(s);
    visited.add(s);
    boolean found = false;

    while (!queue.isEmpty()) {
        String curr = queue.poll();
        if (isValid(curr)) {
            result.add(curr);
            found = true;
            continue; // don't process further removals if found at this level
        }
        if (found) continue; // already found valid strings of this length

        for (int i = 0; i < curr.length(); i++) {
            if (curr.charAt(i) != '(' && curr.charAt(i) != ')') continue;
            String next = curr.substring(0, i) + curr.substring(i + 1);
            if (visited.add(next)) queue.offer(next);
        }
    }
    return result;
}

private boolean isValid(String s) {
    int count = 0;
    for (char c : s.toCharArray()) {
        if (c == '(') count++;
        if (c == ')') count--;
        if (count < 0) return false;
    }
    return count == 0;
}
```

---

## 6. Preparation Strategy

### Timeline: 6-8 weeks

**Weeks 1-2: Speed Building**
- Solve 50 LeetCode easies (arrays, strings) — timed
- Master HashMap, Two Pointers, Sliding Window
- Target: solve easy in <15 min, medium in <30 min

**Weeks 3-4: Core Patterns**
- Trees: all traversals (recursive + iterative), BST operations
- Recursion: subset, permutation, combination templates
- Intervals: merge, insert, meeting rooms
- Practice 5-6 problems daily

**Weeks 5-6: Mock Interviews**
- Meta-specific LeetCode tagged questions
- Practice coding on CoderPad (or similar)
- 2-3 mock interviews per week
- Focus on speed and correctness

### Meta LeetCode Tagged — Must Solve
- Valid Palindrome II
- Binary Tree Level Order Traversal
- K Closest Points to Origin
- Meeting Rooms II
- Remove Invalid Parentheses
- Longest Substring Without Repeating
- 3Sum
- Product of Array Except Self
- Range Sum of BST
- Lowest Common Ancestor III (with parent pointer)

---

## 7. Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Not running code mentally | Bugs in corner cases | Trace through example |
| Over-optimizing prematurely | Slow to finish | Write working code first |
| Poor variable naming | Confusion during coding | Use descriptive names |
| Ignoring edge cases | Code fails on null/single | Check null, empty, length=1 |
| Not verbalizing thought process | Interviewer doesn't know your plan | Talk while coding |
| Spending too long on analysis | Run out of time | Start coding within 5 min |
| Not handling overflow | Integer overflow in Java | Use long if needed |
| Complex solution for simple problem | Hard to debug | Simpler is better at Meta |
