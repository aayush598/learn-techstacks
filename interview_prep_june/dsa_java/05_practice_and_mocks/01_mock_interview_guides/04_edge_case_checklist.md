# Edge Case Identification Checklist

A systematic checklist for identifying edge cases during interviews. Run through this before submitting your solution.

---

## 1. Integer Overflow

**Why it matters**: Java `int` range is -2,147,483,648 to 2,147,483,647. Multiplication of two large ints easily overflows silently.

**Common scenarios**:
- Multiplication: `a * b` where both are large
- Addition in loops: accumulating sum that exceeds MAX_VALUE
- Mid calculation: `(low + high) / 2` when both are near MAX_VALUE
- Negative overflow: `Integer.MIN_VALUE` has no positive counterpart

**How to test**: Use inputs near `Integer.MAX_VALUE` and `Integer.MIN_VALUE`.

```java
// WRONG: overflow in mid calculation
int mid = (low + high) / 2;  // crashes when low + high > Integer.MAX_VALUE

// CORRECT
int mid = low + (high - low) / 2;

// WRONG: overflow in multiplication
int area = width * height;  // overflows for large values

// CORRECT: use long
long area = (long) width * height;

// Check before multiplying
public boolean willOverflow(int a, int b) {
    if (a == 0 || b == 0) return false;
    long result = (long) a * b;
    return result > Integer.MAX_VALUE || result < Integer.MIN_VALUE;
}

// SAFE: checking if sum will overflow
public int safeAdd(int a, int b) {
    if (b > 0 && a > Integer.MAX_VALUE - b) throw new ArithmeticException("Overflow");
    if (b < 0 && a < Integer.MIN_VALUE - b) throw new ArithmeticException("Overflow");
    return a + b;
}
```

---

## 2. Empty Input

**Why it matters**: Empty collections, strings, or arrays can cause `ArrayIndexOutOfBoundsException`, `NoSuchElementException`, or incorrect return values.

**Checklist**:
| Input Type | What to Check | Java Check |
|---|---|---|
| Array | `arr == null \|\| arr.length == 0` | NPE + empty |
| String | `s == null \|\| s.isEmpty()` | NPE + empty |
| List | `list == null \|\| list.isEmpty()` | NPE + empty |
| StringBuilder | `sb == null \|\| sb.length() == 0` | NPE + empty |
| Map | `map == null \|\| map.isEmpty()` | NPE + empty |

```java
// Robust empty check for any collection
public boolean isEmpty(int[] arr) {
    return arr == null || arr.length == 0;
}

public boolean isEmpty(String s) {
    return s == null || s.isEmpty();
}

public boolean isEmpty(List<?> list) {
    return list == null || list.isEmpty();
}

// For a method that processes arrays
public int findMax(int[] arr) {
    if (arr == null || arr.length == 0) {
        throw new IllegalArgumentException("Array must not be null or empty");
    }
    int max = arr[0];
    for (int i = 1; i < arr.length; i++) {
        max = Math.max(max, arr[i]);
    }
    return max;
}
```

---

## 3. Single Element

**Why it matters**: Many algorithms have base cases that assume at least 2 elements. Sorting 1 element, finding "pair" in 1 element, etc.

```java
// Binary search on single element
public int binarySearch(int[] arr, int target) {
    // arr.length == 1 is handled naturally by low=0, high=0
    int low = 0, high = arr.length - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

// Two pointer on single element
public boolean hasPairWithSum(int[] arr, int target) {
    if (arr.length < 2) return false;  // guard clause
    int left = 0, right = arr.length - 1;
    while (left < right) {
        int sum = arr[left] + arr[right];
        if (sum == target) return true;
        else if (sum < target) left++;
        else right--;
    }
    return false;
}

// Linked list with single node
public ListNode reverseList(ListNode head) {
    if (head == null || head.next == null) return head;  // handles 0 and 1 element
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

---

## 4. Two Elements

**Why it matters**: Often the base case for recursion and the simplest non-trivial case for two-pointer, sorting, and comparison logic.

```java
// Two elements: check both orderings
public int minOfTwo(int a, int b) {
    return a <= b ? a : b;
}

// Two elements in sorted array
public boolean twoSumSorted(int[] arr, int target) {
    // With 2 elements: just check if arr[0] + arr[1] == target
    if (arr.length == 2) return arr[0] + arr[1] == target;
    int left = 0, right = arr.length - 1;
    while (left < right) {
        int sum = arr[left] + arr[right];
        if (sum == target) return true;
        else if (sum < target) left++;
        else right--;
    }
    return false;
}

// Binary tree with 2 nodes
public boolean isSameTree(TreeNode p, TreeNode q) {
    if (p == null && q == null) return true;
    if (p == null || q == null) return false;  // one is null, other isn't
    return p.val == q.val
        && isSameTree(p.left, q.left)
        && isSameTree(p.right, q.right);
}
```

---

## 5. All Same Elements

**Why it matters**: Can cause infinite loops, wrong comparisons, or unexpected behavior in algorithms that assume distinct values.

```java
// Sorting: all same elements — stable sort should preserve order
int[] arr = {5, 5, 5, 5, 5};
Arrays.sort(arr);  // [5, 5, 5, 5, 5] — fine

// Binary search: all same — should find any valid index
public int searchInsert(int[] arr, int target) {
    int low = 0, high = arr.length;
    while (low < high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] < target) low = mid + 1;
        else high = mid;
    }
    return low;
}

// Two pointer: all same — sum will always be 2 * value
// Hash map: count occurrences
public int majorityElement(int[] nums) {
    // When all elements are same, any of them is majority
    int candidate = nums[0], count = 1;
    for (int i = 1; i < nums.length; i++) {
        if (count == 0) {
            candidate = nums[i];
            count = 1;
        } else if (nums[i] == candidate) {
            count++;
        } else {
            count--;
        }
    }
    return candidate;
}

// Graph: all nodes with same value — BFS/DFS visit tracking matters
// Don't rely on node values to distinguish visited nodes
```

---

## 6. Already Sorted / Reverse Sorted

**Why it matters**: Some algorithms have best/worst case behavior depending on input order.

```java
// Bubble sort: already sorted = O(n) with optimization, reverse = O(n²)
public void bubbleSort(int[] arr) {
    int n = arr.length;
    for (int i = 0; i < n - 1; i++) {
        boolean swapped = false;
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                swapped = true;
            }
        }
        if (!swapped) break;  // already sorted — O(n) best case
    }
}

// Quick sort: already sorted = O(n²) without random pivot
// Always check: does the problem guarantee sorted input?

// Merge sort: always O(n log n) regardless of input order

// Check if sorted
public boolean isSorted(int[] arr) {
    for (int i = 1; i < arr.length; i++) {
        if (arr[i] < arr[i - 1]) return false;
    }
    return true;
}
```

---

## 7. Negative Numbers

**Why it matters**: Comparisons, sums, and array indices behave differently with negatives.

```java
// Finding max subarray sum: negatives change everything
public int maxSubarraySum(int[] nums) {
    int maxSoFar = nums[0], maxEndingHere = nums[0];
    for (int i = 1; i < nums.length; i++) {
        maxEndingHere = Math.max(nums[i], maxEndingHere + nums[i]);
        maxSoFar = Math.max(maxSoFar, maxEndingHere);
    }
    return maxSoFar;
}

// Division with negatives
public int divide(int dividend, int divisor) {
    if (dividend == Integer.MIN_VALUE && divisor == -1) {
        return Integer.MAX_VALUE;  // overflow protection
    }
    return dividend / divisor;
}

// Absolute value can overflow
public int safeAbs(int x) {
    if (x == Integer.MIN_VALUE) return Integer.MAX_VALUE;  // or handle specially
    return Math.abs(x);
}

// Comparing negatives: be careful with unsigned operations
// Use long when comparing products of negatives
public boolean compare(int a, int b) {
    return (long) a * a < (long) b * b;  // correct for negatives
}
```

---

## 8. Zero

**Why it matters**: Division by zero, modulo by zero, zero as a valid input.

```java
// Division
public double safeDivide(int a, int b) {
    if (b == 0) throw new ArithmeticException("Division by zero");
    return (double) a / b;
}

// Modulo
public int safeMod(int a, int b) {
    if (b == 0) throw new ArithmeticException("Modulo by zero");
    return a % b;
}

// Zero in array: product of all except self
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] result = new int[n];
    result[0] = 1;
    for (int i = 1; i < n; i++) {
        result[i] = result[i - 1] * nums[i - 1];
    }
    int right = 1;
    for (int i = n - 1; i >= 0; i--) {
        result[i] *= right;
        right *= nums[i];
    }
    return result;
}

// Zero in tree: path sum — 0 is a valid value on path
public boolean hasPathSum(TreeNode root, int targetSum) {
    if (root == null) return false;
    if (root.left == null && root.right == null) {
        return targetSum - root.val == 0;
    }
    return hasPathSum(root.left, targetSum - root.val)
        || hasPathSum(root.right, targetSum - root.val);
}
```

---

## 9. Large Values / Performance

**Why it matters**: Stack overflow in recursion, TLE with large inputs, memory limits.

```java
// Recursion depth: can overflow stack for deep recursion
// n = 100,000 → StackOverflowError with naive recursion
public int fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);  // O(2^n) — useless for n > 40
}

// Tail recursion optimization (Java doesn't do it, but structure helps convert)
public int fibIterative(int n) {
    if (n <= 1) return n;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

// Large arrays: O(n²) may TLE for n = 10^5
// Acceptable complexities by input size:
// n <= 10: O(n!) feasible
// n <= 20: O(2^n) feasible
// n <= 500: O(n³) feasible
// n <= 10,000: O(n²) feasible
// n <= 10^6: O(n log n) feasible
// n <= 10^8: O(n) feasible

// String concatenation: O(n²) — use StringBuilder
public String repeat(String s, int n) {
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < n; i++) {
        sb.append(s);  // O(n) amortized per append
    }
    return sb.toString();
}
```

---

## 10. Cycle Detection

**Why it matters**: Linked lists and graphs can have cycles. Algorithms that don't detect them will infinite loop.

```java
// Linked list cycle detection: Floyd's tortoise and hare
public boolean hasCycle(ListNode head) {
    if (head == null || head.next == null) return false;
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}

// Find cycle start
public ListNode detectCycleStart(ListNode head) {
    if (head == null || head.next == null) return null;
    ListNode slow = head, fast = head;
    // Phase 1: detect cycle
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) break;
    }
    if (fast == null || fast.next == null) return null;  // no cycle
    // Phase 2: find start
    ListNode p = head;
    while (p != slow) {
        p = p.next;
        slow = slow.next;
    }
    return p;
}

// Graph cycle detection: DFS with state tracking
// 0 = unvisited, 1 = in current path, 2 = fully processed
public boolean hasCycle(int[][] graph) {
    int n = graph.length;
    int[] state = new int[n];
    for (int i = 0; i < n; i++) {
        if (state[i] == 0 && dfs(graph, i, state)) return true;
    }
    return false;
}

private boolean dfs(int[][] graph, int node, int[] state) {
    state[node] = 1;  // mark as in current path
    for (int neighbor : graph[node]) {
        if (state[neighbor] == 1) return true;   // cycle found
        if (state[neighbor] == 0 && dfs(graph, neighbor, state)) return true;
    }
    state[node] = 2;  // mark as fully processed
    return false;
}

// Topological sort: detect cycle using Kahn's algorithm
public boolean hasCycleKahn(List<List<Integer>> graph, int n) {
    int[] inDegree = new int[n];
    for (int i = 0; i < n; i++) {
        for (int next : graph[i]) inDegree[next]++;
    }
    Queue<Integer> queue = new LinkedList<>();
    for (int i = 0; i < n; i++) {
        if (inDegree[i] == 0) queue.add(i);
    }
    int count = 0;
    while (!queue.isEmpty()) {
        int node = queue.poll();
        count++;
        for (int next : graph.get(node)) {
            inDegree[next]--;
            if (inDegree[next] == 0) queue.add(next);
        }
    }
    return count != n;  // cycle if not all nodes processed
}
```

---

## 11. Boundary Indices

**Why it matters**: Off-by-one errors are the most common bugs in array/string problems.

```java
// First element
int first = arr[0];

// Last element
int last = arr[arr.length - 1];

// Off-by-one: loop bounds
// To process all elements: i from 0 to arr.length - 1
for (int i = 0; i < arr.length; i++) { ... }

// To process all pairs: j from i+1 to arr.length - 1
for (int i = 0; i < arr.length; i++) {
    for (int j = i + 1; j < arr.length; j++) { ... }
}

// Sliding window: right boundary
public int maxSumSubarray(int[] arr, int k) {
    if (arr.length < k) return -1;  // boundary check
    int windowSum = 0;
    for (int i = 0; i < k; i++) windowSum += arr[i];
    int maxSum = windowSum;
    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i] - arr[i - k];
        maxSum = Math.max(maxSum, windowSum);
    }
    return maxSum;
}

// String indices: last char is s.charAt(s.length() - 1)
// Empty string: s.length() == 0, s.charAt(0) throws

// Matrix: arr[row][col], row in [0, m-1], col in [0, n-1]
public boolean isValid(int row, int col, int m, int n) {
    return row >= 0 && row < m && col >= 0 && col < n;
}
```

---

## 12. Null Pointers

**Why it matters**: NPE is the most common runtime exception. Always check before dereferencing.

```java
// Tree null checks
public int maxDepth(TreeNode root) {
    if (root == null) return 0;  // ALWAYS check first
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}

// Graph adjacency: null check before accessing neighbors
public void bfs(Map<Integer, List<Integer>> graph, int start) {
    if (graph == null || !graph.containsKey(start)) return;
    Queue<Integer> queue = new LinkedList<>();
    queue.add(start);
    Set<Integer> visited = new HashSet<>();
    visited.add(start);
    while (!queue.isEmpty()) {
        int node = queue.poll();
        List<Integer> neighbors = graph.get(node);
        if (neighbors == null) continue;  // null check
        for (int next : neighbors) {
            if (!visited.contains(next)) {
                visited.add(next);
                queue.add(next);
            }
        }
    }
}

// String null
public boolean isEmptyOrNull(String s) {
    return s == null || s.isEmpty();
}

// Array of objects: check each element
public int countNonNull(Object[] arr) {
    int count = 0;
    for (Object obj : arr) {
        if (obj != null) count++;
    }
    return count;
}
```

---

## 13. Overflow in Mid Calculation

**Why it matters**: `(low + high) / 2` overflows when `low + high > Integer.MAX_VALUE`.

```java
// WRONG
int mid = (low + high) / 2;

// CORRECT
int mid = low + (high - low) / 2;

// In binary search templates
public int binarySearch(int[] arr, int target) {
    int low = 0, high = arr.length - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;  // safe
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

// In merge sort: also safe because mid is always < n
public void mergeSort(int[] arr, int low, int high) {
    if (low >= high) return;
    int mid = low + (high - low) / 2;
    mergeSort(arr, low, mid);
    mergeSort(arr, mid + 1, high);
    merge(arr, low, mid, high);
}
```

---

## 14. Character Set

**Why it matters**: Using fixed-size arrays for character counting assumes a specific character set.

```java
// 26 lowercase letters only
public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] count = new int[26];
    for (int i = 0; i < s.length(); i++) {
        count[s.charAt(i) - 'a']++;
        count[t.charAt(i) - 'a']--;
    }
    for (int c : count) {
        if (c != 0) return false;
    }
    return true;
}

// ASCII (128 characters)
public boolean isPermutation(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] count = new int[128];
    for (int i = 0; i < s.length(); i++) {
        count[s.charAt(i)]++;
        count[t.charAt(i)]--;
    }
    for (int c : count) {
        if (c != 0) return false;
    }
    return true;
}

// Extended ASCII (256 characters)
int[] count = new int[256];

// Unicode: use HashMap
public boolean isAnagramUnicode(String s, String t) {
    if (s.length() != t.length()) return false;
    Map<Character, Integer> map = new HashMap<>();
    for (int i = 0; i < s.length(); i++) {
        map.merge(s.charAt(i), 1, Integer::sum);
        map.merge(t.charAt(i), -1, Integer::sum);
    }
    return map.values().stream().allMatch(v -> v == 0);
}

// Ask interviewer: "What character set should I assume?"
```

---

## 15. Disconnected Graph

**Why it matters**: BFS/DFS from one node may not visit all nodes. Must iterate through all nodes.

```java
// BFS that handles disconnected components
public int countComponents(int n, int[][] edges) {
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
    for (int[] e : edges) {
        graph.get(e[0]).add(e[1]);
        graph.get(e[1]).add(e[0]);
    }
    boolean[] visited = new boolean[n];
    int components = 0;
    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            bfs(graph, i, visited);
            components++;
        }
    }
    return components;
}

private void bfs(List<List<Integer>> graph, int start, boolean[] visited) {
    Queue<Integer> queue = new LinkedList<>();
    queue.add(start);
    visited[start] = true;
    while (!queue.isEmpty()) {
        int node = queue.poll();
        for (int next : graph.get(node)) {
            if (!visited[next]) {
                visited[next] = true;
                queue.add(next);
            }
        }
    }
}

// Union-Find: naturally handles disconnected graphs
public int countComponentsUnionFind(int n, int[][] edges) {
    int[] parent = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;
    int components = n;
    for (int[] e : edges) {
        int rootA = find(parent, e[0]);
        int rootB = find(parent, e[1]);
        if (rootA != rootB) {
            parent[rootA] = rootB;
            components--;
        }
    }
    return components;
}

private int find(int[] parent, int x) {
    if (parent[x] != x) parent[x] = find(parent, parent[x]);
    return parent[x];
}
```

---

## 16. Tree Imbalance

**Why it matters**: Skewed trees degenerate to linked lists — O(n) for operations that should be O(log n).

```java
// Balanced BST operations: O(log n)
// Skewed BST (all left or all right children): O(n)

// Check if tree is balanced
public boolean isBalanced(TreeNode root) {
    return checkHeight(root) != -1;
}

private int checkHeight(TreeNode node) {
    if (node == null) return 0;
    int left = checkHeight(node.left);
    if (left == -1) return -1;
    int right = checkHeight(node.right);
    if (right == -1) return -1;
    if (Math.abs(left - right) > 1) return -1;
    return Math.max(left, right) + 1;
}

// Inorder traversal of skewed BST: sorted array but tree is a linked list
// This is why we need self-balancing trees (AVL, Red-Black)

// Worst case for BST operations with unbalanced tree
// insert n elements in sorted order → O(n²) total
// This is why we use TreeMap/TreeSet (Red-Black tree) not naive BST
```

---

## Quick Reference: Run-Through Order

Before submitting, check in this order:

1. **Null/Empty**: Is input null or empty?
2. **Single/Two elements**: Do these work?
3. **All same**: Are all elements identical?
4. **Sorted/Reverse**: How does order affect the algorithm?
5. **Negatives/Zero**: Are negative numbers or zero valid?
6. **Overflow**: Can values exceed int range?
7. **Boundaries**: First/last element, off-by-one?
8. **Null pointers**: Tree/graph neighbors?
9. **Cycles**: Can linked list or graph have cycles?
10. **Character set**: What characters are possible?
11. **Disconnected**: Graph with multiple components?
12. **Performance**: Is time/memory acceptable for max input?
