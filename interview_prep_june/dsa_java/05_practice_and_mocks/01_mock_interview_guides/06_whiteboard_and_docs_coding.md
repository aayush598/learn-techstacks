# Whiteboard & Google Docs Coding Guide

How to code effectively in non-IDE environments during interviews.

---

## 1. Whiteboard Coding

### Writing Clearly

```
Whiteboard Layout:
┌─────────────────────────────────────────────────┐
│  Problem Name: Two Sum                           │
│  Approach: HashMap                               │
│  Time: O(n)  Space: O(n)                        │
│                                                  │
│  public int[] twoSum(int[] nums, int target) {   │
│      Map<Integer, Integer> map = new HashMap<>(); │
│      for (int i = 0; i < nums.length; i++) {     │
│          int complement = target - nums[i];       │
│          if (map.containsKey(complement)) {       │
│              return new int[]{map.get(complement),│
│                                i};                │
│          }                                       │
│          map.put(nums[i], i);                    │
│      }                                           │
│      return new int[]{-1, -1};                   │
│  }                                               │
└─────────────────────────────────────────────────┘
```

### Space Management Rules

```
1. Leave 2-3 lines between sections (approach, code, edge cases)
2. Write code in blocks: signature, body, closing brace
3. Reserve right side for notes/edge cases
4. If you make a mistake, DON'T erase — strike through:
   WRONG: ~~for (int i = 0; i < arr.length; i++)~~
   RIGHT: for (int i = 0; i < nums.length; i++)
5. Use consistent indentation (2-4 spaces)
6. Write method signature first, then fill in body
```

### Compiler-in-Your-Head Technique

```
Before writing code, mentally trace:

1. What's the input type? int[], String, TreeNode?
2. What's the output type? int, boolean, List?
3. What are edge cases? null, empty, single element?
4. What's the variable naming convention?
5. What imports do I need? (usually java.util.*)

Then trace your code mentally:

Input: [2, 7, 11, 15], target = 9
Step 1: i=0, nums[0]=2, complement=7, map={}, map doesn't contain 7, put(2,0)
Step 2: i=1, nums[1]=7, complement=2, map={2:0}, map contains 2! Return [0,1]
Output: [0, 1] ✓
```

### Common Whiteboard Mistakes

```
Mistake 1: Writing too small
→ Write large enough to be readable from 3 feet away

Mistake 2: No line breaks
→ One long line of code is hard to follow
→ Break into logical blocks with blank lines

Mistake 3: Erasing everything when wrong
→ Strike through wrong line, write correct version nearby
→ Shows your thinking process

Mistake 4: Not writing the full signature
→ Always write: public ReturnType methodName(ParamType param)
→ Interviewer needs to see the complete interface

Mistake 5: Forgetting edge case handling
→ Write null checks at the top of the method
→ Write boundary checks before loops
```

---

## 2. Google Docs / Online Editor Coding

### No Auto-Complete Strategy

```
What you lose:
├── Method name suggestions
├── Parameter type suggestions
├── Import suggestions
├── Variable name completion
└── Syntax error detection

What you must do manually:
├── Write full method signatures (no shortcuts)
├── Remember import statements
├── Check brace matching yourself
├── Verify variable names are consistent
└── Test logic mentally (no compile checks)
```

### Tab vs Spaces

```
Google Docs:
├── Tab = inserts a tab character (varies by editor)
├── Best practice: use spaces for consistency
├── Press Space 4 times for one indent level
├── Or use Shift+Tab to un-indent (if supported)

Online editors (CoderPad, HackerRank):
├── Usually support Tab for indentation
├── Tab width varies (2, 4, or 8 spaces)
├── Ask interviewer: "What indentation do you prefer?"
└── Stick to one style throughout
```

### Brace Matching Without Highlighting

```
Manual brace tracking technique:

Count opens and closes as you write:
public int[] twoSum(int[] nums, int target) {  // opens: 1
    Map<Integer, Integer> map = new HashMap<>(); // opens: 1, closes: 0
    for (int i = 0; i < nums.length; i++) {     // opens: 2
        int complement = target - nums[i];       // opens: 2, closes: 0
        if (map.containsKey(complement)) {       // opens: 3
            return new int[]{map.get(complement), i}; // opens: 3, closes: 0
        }                                        // closes: 2
        map.put(nums[i], i);                    // opens: 2, closes: 0
    }                                            // closes: 1
    return new int[]{-1, -1};                   // opens: 1, closes: 0
}                                                // closes: 0 ✓

Tip: Write closing brace immediately after opening:
for (...) {
    // body
}  // ← write this right away
```

### Simple Syntax Over Clever Tricks

```
❌ AVOID (clever but hard to read on whiteboard):
int mid = (l + r) >>> 1;  // unsigned right shift
boolean contains = (mask & (1 << i)) != 0;
int[] result = Arrays.stream(arr).filter(x -> x > 0).toArray();

✅ USE (clear and correct):
int mid = low + (high - low) / 2;
boolean contains = false;
for (int x : arr) {
    if (x == target) {
        contains = true;
        break;
    }
}
// Or for simple checks:
boolean contains = false;
for (int x : arr) {
    if (x == target) contains = true;
}
```

---

## 3. Strategies for Both

### Helper Methods First

```java
// Write helper methods before main method
// Shows organized thinking, reduces main method complexity

// Helper 1: Check if index is valid
private boolean isValid(int row, int col, int rows, int cols) {
    return row >= 0 && row < rows && col >= 0 && col < cols;
}

// Helper 2: DFS traversal
private void dfs(char[][] grid, int row, int col, int rows, int cols) {
    if (!isValid(row, col, rows, cols) || grid[row][col] == '0') return;
    grid[row][col] = '0';
    dfs(grid, row + 1, col, rows, cols);
    dfs(grid, row - 1, col, rows, cols);
    dfs(grid, row, col + 1, rows, cols);
    dfs(grid, row, col - 1, rows, cols);
}

// Main method: clean and readable
public int numIslands(char[][] grid) {
    if (grid == null || grid.length == 0) return 0;
    int rows = grid.length, cols = grid[0].length;
    int count = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (grid[i][j] == '1') {
                dfs(grid, i, j, rows, cols);
                count++;
            }
        }
    }
    return count;
}
```

### Meaningful Variable Names

```
❌ Bad: a, b, c, tmp, res, cnt, idx, arr, s, t
✅ Good: left, right, maxSum, count, index, nums, source, target

❌ Bad: for (int i = 0; i < n; i++) { for (int j = 0; j < m; j++) {
✅ Good: for (int row = 0; row < rows; row++) { for (int col = 0; col < cols; col++) {

Exception: loop indices i, j, k are fine in simple loops
But for matrix traversal, prefer row/col for clarity
```

### Comments for Complex Logic

```
// GOOD: comment explains WHY, not WHAT
// Use HashMap because we need O(1) lookup for complements
Map<Integer, Integer> map = new HashMap<>();

// BAD: comment just restates the code
// increment i by 1
i++;

// GOOD: comment explains non-obvious approach
// Instead of checking all pairs (O(n²)), we use the fact that
// if a + b = target, then b = target - a
// So for each element, we check if its complement exists in the map
for (int i = 0; i < nums.length; i++) {
    int complement = target - nums[i];
    if (map.containsKey(complement)) {
        return new int[]{map.get(complement), i};
    }
    map.put(nums[i], i);
}

// GOOD: comment for tricky edge cases
// Handle case where all elements are the same
// In this case, we need at least 2 elements
if (arr.length < 2) return new int[]{-1, -1};
```

### Trace Through Example

```
After writing code, ALWAYS trace through with example:

Problem: Two Sum
Input: nums = [2, 7, 11, 15], target = 9

Trace:
i=0: nums[0]=2, complement=9-2=7, map={2:0}
i=1: nums[1]=7, complement=9-7=2, map has 2! → return [0, 1]
Output: [0, 1] ✓

Verify: nums[0] + nums[1] = 2 + 7 = 9 ✓
```

---

## 4. Common Mistakes in Non-IDE Coding

### Mistake 1: Forgetting Imports

```
// ALWAYS write this at the top (if needed):
import java.util.*;

// Common imports you'll need:
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Queue;
import java.util.LinkedList;
import java.util.Stack;
import java.util.PriorityQueue;
import java.util.HashSet;
import java.util.Set;
import java.util.Map;
import java.util.List;

// For online editors, imports are usually provided
// For whiteboard, mention: "I'll need java.util.* for HashMap"
```

### Mistake 2: Method Signature Errors

```
// WRONG (missing return type or access modifier):
twoSum(int[] nums, int target) { ... }
public twoSum(int[] nums, int target) { ... }

// CORRECT:
public int[] twoSum(int[] nums, int target) { ... }

// Common signatures to memorize:
public int methodName(int[] arr) { ... }
public boolean methodName(String s) { ... }
public List<List<Integer>> methodName(int[][] grid) { ... }
public void methodName(ListNode head) { ... }
public TreeNode methodName(TreeNode root) { ... }
```

### Mistake 3: Array Access Out of Bounds

```
// WRONG (off-by-one):
for (int i = 0; i <= arr.length; i++) {  // arr.length is out of bounds!

// CORRECT:
for (int i = 0; i < arr.length; i++) {  // last valid index is arr.length - 1

// WRONG (string index):
char c = s.charAt(s.length());  // out of bounds!

// CORRECT:
char c = s.charAt(s.length() - 1);

// WRONG (empty array):
int first = arr[0];  // ArrayIndexOutOfBoundsException if arr is empty

// CORRECT:
if (arr.length == 0) return;  // or handle empty case
int first = arr[0];
```

### Mistake 4: Null Pointer Exceptions

```
// WRONG (no null check):
public int maxDepth(TreeNode root) {
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
    // root could be null!
}

// CORRECT:
public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}

// WRONG (no null check on String):
public boolean isPalindrome(String s) {
    return s.equals(new StringBuilder(s).reverse().toString());
    // s could be null!
}

// CORRECT:
public boolean isPalindrome(String s) {
    if (s == null) return false;
    return s.equals(new StringBuilder(s).reverse().toString());
}
```

### Mistake 5: Integer Overflow

```
// WRONG (overflow in mid):
int mid = (low + high) / 2;  // low + high can overflow!

// CORRECT:
int mid = low + (high - low) / 2;

// WRONG (overflow in multiplication):
int area = width * height;  // can overflow for large values!

// CORRECT:
long area = (long) width * height;

// WRONG (overflow in sum):
int sum = 0;
for (int x : arr) sum += x;  // can overflow!

// CORRECT:
long sum = 0;
for (int x : arr) sum += x;
```

---

## 5. Practice Environment

### Practice Tools

```
Whiteboard practice:
├── Physical whiteboard (best simulation)
├── Paper and pen (good alternative)
├── paint.net or similar drawing tool
└── Excalidraw (digital whiteboard)

Online editor practice:
├── Google Docs (no syntax highlighting)
├── Notepad (no features at all)
├── pencilcode.net (simple online editor)
├── CoderPad (interview-like environment)
└── HackerRank code editor

Tips:
├── Practice without copy-paste (type everything)
├── Practice without undo (simulate whiteboard)
├── Time yourself for every practice session
└── Practice talking while coding
```

### Practice Session Structure

```
Session 1 (30 min): Whiteboard practice
├── Pick 1 easy problem
├── Write solution on whiteboard/paper
├── No erasing allowed (strike through only)
├── Trace through example
└── Check for errors

Session 2 (30 min): Google Docs practice
├── Pick 1 medium problem
├── Write in Google Docs (no syntax highlighting)
├── No auto-complete allowed
├── Verify braces match
└── Time yourself

Session 3 (30 min): Combined practice
├── Pick 1 hard problem
├── Explain approach out loud (whiteboard)
├── Code solution in Google Docs
├── Walk through test cases
└── Handle follow-up questions
```

---

## 6. Quick Reference Card

```
BEFORE CODING:
□ Write method signature
□ Mention imports needed
□ State time/space complexity goal
□ Handle null/empty input first

WHILE CODING:
□ Use meaningful variable names
□ Consistent indentation (4 spaces)
□ Write closing braces immediately
□ Comment complex logic
□ Check brace count

AFTER CODING:
□ Trace through example
□ Check for off-by-one errors
□ Check for null pointers
□ Check for integer overflow
□ State time/space complexity
□ Mention edge cases handled
```

### Common Java Snippets to Memorize

```java
// Array null/empty check
if (arr == null || arr.length == 0) return;

// String null/empty check
if (s == null || s.isEmpty()) return;

// Binary search template
int low = 0, high = arr.length - 1;
while (low <= high) {
    int mid = low + (high - low) / 2;
    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) low = mid + 1;
    else high = mid - 1;
}

// BFS template
Queue<Integer> queue = new LinkedList<>();
queue.add(start);
boolean[] visited = new boolean[n];
visited[start] = true;
while (!queue.isEmpty()) {
    int node = queue.poll();
    for (int next : neighbors) {
        if (!visited[next]) {
            visited[next] = true;
            queue.add(next);
        }
    }
}

// DFS template (recursive)
private void dfs(int node, boolean[] visited) {
    visited[node] = true;
    for (int next : neighbors) {
        if (!visited[next]) dfs(next, visited);
    }
}

// Two pointer template
int left = 0, right = arr.length - 1;
while (left < right) {
    int sum = arr[left] + arr[right];
    if (sum == target) return new int[]{left, right};
    else if (sum < target) left++;
    else right--;
}

// Linked list reverse
ListNode prev = null, curr = head;
while (curr != null) {
    ListNode next = curr.next;
    curr.next = prev;
    prev = curr;
    curr = next;
}
return prev;
```
