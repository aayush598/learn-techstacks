# Microsoft Interview Pattern

## Table of Contents
1. Interview Format
2. Most Asked Topics
3. What Microsoft Values
4. Types of Problems
5. Example Problems with Approaches
6. Preparation Strategy

---

## 1. Interview Format

### Phone Screen (45-60 min)
- 1-2 coding problems on Microsoft Teams/CodeSignal
- Sometimes brief behavioral questions
- Recruiter may ask about past experience and projects

### On-site / Virtual On-site (4-5 rounds, 45-60 min each)
- **Coding rounds** (2-3): Data structures and algorithms
- **System Design** (1): For senior roles (usually SDE II+)
- **Behavioral / "Fit"** (1): "Why Microsoft?", past experiences
- **Ask Me Anything (AMA)**: Reverse interview with hiring manager
- May include a **live coding** session on whiteboard or shared editor

### Key Differences from Other FAANG
- Microsoft has a more relaxed interview atmosphere
- Questions tend to be more "academic" — focus on algorithm knowledge
- More likely to ask math-based problems (prime numbers, GCD, etc.)
- Very focused on tree problems (BST, LCA, etc.)
- They value product sense — "How would you improve Word/Outlook?"

---

## 2. Most Asked Topics

| Topic | Frequency | Why Microsoft Asks It |
|-------|-----------|---------------------|
| Trees (BST, Binary Tree) | Very High | File systems, compilers, databases |
| Strings | High | Text processing, editing tools |
| Linked Lists | High | Memory management, document editing |
| Math / Number Theory | High | Cryptography, algorithms foundation |
| DP | Medium-High | Optimization problems |
| Arrays | Medium-High | General problem solving |
| Graphs | Medium | Dependency resolution, social features |
| Design / OOP | Medium | Windows, Office extensibility |

### Topic Frequency Graph
```
Trees:   ████████████████████
Strings: ████████████████
LL:      ████████████████
Math:    ██████████████
DP:      ████████████
Arrays:  ████████████
Graphs:  ██████
Design:  ██████
```

---

## 3. What Microsoft Values

### Problem-Solving Approach
- How do you break down a complex problem?
- Can you identify patterns?
- Do you consider multiple approaches before coding?
- Microsoft interviewers like to see structured thinking

### Algorithm Knowledge
- Do you know the fundamentals well?
- Can you implement classic algorithms from scratch?
- Do you understand time/space complexity deeply?
- They often ask "What's the best/worst/average case?"

### Product Sense
- How would you improve Microsoft products?
- Understanding of user experience
- "How would you design a feature for Excel/Word/Outlook?"
- Less emphasis on this than Amazon LPs, but still present

### Coding Quality
- Clean, readable code
- Properly named variables
- Modular functions
- Error handling and edge cases

---

## 4. Types of Problems

### BST Problems (Very Common)
- Validate BST
- Lowest Common Ancestor
- Serialize/Deserialize BST
- Convert sorted array to BST
- Kth smallest in BST
- Inorder successor in BST

### Linked List Problems
- Reverse Linked List
- Merge two sorted lists
- LRU Cache (also common)
- Remove nth from end
- Intersection of two linked lists

### String Manipulation
- String to Integer (atoi) — very common
- Longest palindromic substring
- Reverse words in a string
- Implement strStr() / indexOf
- Compare version numbers

### Math Problems
- Check if a number is palindrome
- Prime number checks / Sieve of Eratosthenes
- GCD / LCM
- Power / Square root without library
- Excel sheet column title/number conversion

### Matrix Problems
- Spiral matrix
- Rotate image
- Set matrix zeroes
- Search in 2D matrix

---

## 5. Example Problems with Approaches

### Problem 1: Reverse Linked List
**Problem:** Reverse a singly linked list.

**Approach (Iterative):**
```java
public ListNode reverseList(ListNode head) {
    ListNode prev = null, curr = head;
    while (curr != null) {
        ListNode next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}
```

**Approach (Recursive):**
```java
public ListNode reverseList(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode p = reverseList(head.next);
    head.next.next = head;
    head.next = null;
    return p;
}
```

### Problem 2: Lowest Common Ancestor of BST
**Problem:** Find LCA in binary search tree.

**Approach:** Use BST property — if both values are on one side, go that way.
```java
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (root.val > p.val && root.val > q.val) {
        return lowestCommonAncestor(root.left, p, q);
    } else if (root.val < p.val && root.val < q.val) {
        return lowestCommonAncestor(root.right, p, q);
    } else {
        return root; // split point = LCA
    }
}
```

### Problem 3: String to Integer (atoi)
**Problem:** Convert string to integer, handle whitespace, signs, overflow.

**Approach:** Step by step parsing.
```java
public int myAtoi(String s) {
    int i = 0, n = s.length(), sign = 1, result = 0;
    while (i < n && s.charAt(i) == ' ') i++;
    if (i < n && (s.charAt(i) == '+' || s.charAt(i) == '-')) {
        sign = (s.charAt(i) == '-') ? -1 : 1;
        i++;
    }
    while (i < n && Character.isDigit(s.charAt(i))) {
        int digit = s.charAt(i) - '0';
        // Check overflow
        if (result > Integer.MAX_VALUE / 10 ||
            (result == Integer.MAX_VALUE / 10 && digit > 7)) {
            return sign == 1 ? Integer.MAX_VALUE : Integer.MIN_VALUE;
        }
        result = result * 10 + digit;
        i++;
    }
    return result * sign;
}
```

### Problem 4: Spiral Matrix
**Problem:** Return elements of matrix in spiral order.

**Approach:** Layer by layer traversal.
```java
public List<Integer> spiralOrder(int[][] matrix) {
    List<Integer> result = new ArrayList<>();
    int top = 0, bottom = matrix.length - 1;
    int left = 0, right = matrix[0].length - 1;
    while (top <= bottom && left <= right) {
        for (int j = left; j <= right; j++) result.add(matrix[top][j]);
        top++;
        for (int i = top; i <= bottom; i++) result.add(matrix[i][right]);
        right--;
        if (top <= bottom) {
            for (int j = right; j >= left; j--) result.add(matrix[bottom][j]);
            bottom--;
        }
        if (left <= right) {
            for (int i = bottom; i >= top; i--) result.add(matrix[i][left]);
            left++;
        }
    }
    return result;
}
```

### Problem 5: String to Integer (another common variant)
**Problem:** Compare two version numbers.
```java
public int compareVersion(String version1, String version2) {
    String[] v1 = version1.split("\\.");
    String[] v2 = version2.split("\\.");
    int n = Math.max(v1.length, v2.length);
    for (int i = 0; i < n; i++) {
        int num1 = i < v1.length ? Integer.parseInt(v1[i]) : 0;
        int num2 = i < v2.length ? Integer.parseInt(v2[i]) : 0;
        if (num1 < num2) return -1;
        if (num1 > num2) return 1;
    }
    return 0;
}
```

---

## 6. Preparation Strategy

### Timeline: 6-8 weeks

**Weeks 1-2: Core Data Structures**
- All tree traversals (recursive + iterative)
- BST operations (insert, delete, search, validate)
- Linked list operations (reverse, merge, detect cycle)
- String/Number parsing

**Weeks 3-4: Algorithms Deep Dive**
- Sorting algorithms and their properties
- Divide and Conquer (merge sort, quicksort)
- Binary search variations
- Basic DP (Fibonacci, grid paths, LCS)

**Weeks 5-6: Microsoft-Specific**
- Solve Microsoft-tagged LeetCode problems
- Practice matrix problems (spiral, rotate, search)
- Review math problems (prime, GCD, palindromes)
- 3-4 mock interviews

### Must-Solve Microsoft Problems
- Reverse Linked List
- LCA of BST
- String to Integer (atoi)
- Spiral Matrix
- Rotate Image
- Validate Binary Search Tree
- Merge Two Sorted Lists
- LRU Cache
- Trapping Rain Water
- Longest Palindromic Substring
- Serialize and Deserialize Binary Tree
- N-Queens

### Microsoft Specific Tips
1. **Know your BSTs cold** — they will ask at least one BST problem
2. **Practice without autocomplete** — Microsoft uses whiteboard/simple editor
3. **Be ready for follow-ups** — they like to ask "What if the input changes?"
4. **Math problems** — review prime numbers, GCD, palindrome numbers
5. **Ask good questions** — "What should I improve in this product?" shows interest
