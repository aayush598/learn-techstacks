# 06 — Tail Recursion vs Iteration

Every recursive function can be written iteratively, and every iterative function can be written recursively. The question is: which is better for a given problem?

---

## 1. What is Tail Recursion?

A recursive function is **tail recursive** if the recursive call is the **last operation** in the function — meaning there's no pending work after the call returns.

```java
// Tail recursive — last action is the recursive call, result returned directly
int factorial(int n, int acc) {
    if (n <= 1) return acc;
    return factorial(n - 1, n * acc);   // no work after this call
}

// NOT tail recursive — multiplication happens AFTER the call returns
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);   // multiplication waiting!
}
```

### The Key Test

Look at what happens **after** the recursive call:

```java
// TAIL: the recursive call IS the return value
return f(n - 1, acc);

// NOT TAIL: there's work AFTER the recursive call
return n * f(n - 1);
return 1 + f(n - 1);
return f(n - 1) + f(n - 2);
```

---

## 2. Tail Call Optimization (TCO)

### What TCO Does

In a tail-recursive call, the current stack frame is **no longer needed** — there's no pending work. TCO reuses the current frame for the next call instead of creating a new one.

```
WITHOUT TCO (each call = new frame):
[factorial(5, 1)]
[factorial(5, 1)] → [factorial(4, 5)]
[factorial(5, 1)] → [factorial(4, 5)] → [factorial(3, 20)]
... 5 frames total

WITH TCO (frame reused):
[factorial(5, 1)] → [factorial(4, 5)] → [factorial(3, 20)] → ...
... 1 frame reused for all calls
```

TCO makes tail recursion **O(1) stack space** instead of O(n).

### Where TCO is Supported

```
✅ Functional languages:   Scheme, Haskell, Clojure, Scala
✅ Systems languages:     C, C++, Rust (with optimizations)
✅ Some dynamic languages: Lua, ES6 (strict mode JavaScript)
❌ Java:                  NO TAIL CALL OPTIMIZATION
❌ Python:                NO TAIL CALL OPTIMIZATION (Guido says no)
❌ Go:                    Generally no (implementation-specific)
```

---

## 3. Java and Tail Recursion

**Java does NOT have TCO.** Period. Every recursive call in Java creates a new stack frame.

```java
// Even perfectly tail-recursive code WILL overflow in Java
public class TCOInJava {
    static int sum(int n, int acc) {
        if (n == 0) return acc;
        return sum(n - 1, acc + n);  // tail recursive!
    }

    public static void main(String[] args) {
        System.out.println(sum(100_000, 0));  // StackOverflowError
    }
}
```

### Why No TCO in Java?

1. **Security:** The JVM security model relies on inspecting stack frames. TCO collapses frames, breaking this.
2. **Debugging:** Stack traces would show collapsed frames, confusing developers.
3. **Bytecode:** The JVM instruction set was designed without TCO in mind.
4. **Historical:** Early JVM specs didn't require it, and adding it later would break backward compatibility.

### Workarounds in Java

```java
// 1. Use explicit loop (standard solution)
int sum(int n) {
    int acc = 0;
    for (int i = 1; i <= n; i++) {
        acc += i;
    }
    return acc;
}

// 2. Trampolining (advanced, rarely needed in DSA)
// A trampoline is a loop that repeatedly invokes thunk-returning functions
interface Trampoline<T> {
    T get();
    default boolean isComplete() { return false; }
    default T result() { return null; }
    static <T> T trampoline(Trampoline<T> t) {
        while (!t.isComplete()) {
            t = t.get();  // unwrap the next thunk
        }
        return t.result();
    }
}
// Trampolining converts stack recursion into heap-allocated objects
```

---

## 4. Converting Tail Recursion to Iteration

The transformation is mechanical — the accumulator becomes a local variable, the recursive call becomes a loop.

### Template

```java
// RECURSIVE (tail)
Result function(Input input, Accumulator acc) {
    if (baseCase(input)) return acc;
    Acc newAcc = update(acc, input);
    return function(reduce(input), newAcc);
}

// ITERATIVE (equivalent)
Result function(Input input) {
    Accumulator acc = initialValue;
    while (!baseCase(input)) {
        acc = update(acc, input);
        input = reduce(input);
    }
    return acc;
}
```

### Examples

```java
// Factorial
// Recursive (tail):
int factorial(int n, int acc) {
    if (n <= 1) return acc;
    return factorial(n - 1, n * acc);
}
// Iterative:
int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; i++) result *= i;
    return result;
}

// Sum of array
// Recursive (tail):
int sum(int[] arr, int i, int acc) {
    if (i == arr.length) return acc;
    return sum(arr, i + 1, acc + arr[i]);
}
// Iterative:
int sum(int[] arr) {
    int total = 0;
    for (int x : arr) total += x;
    return total;
}

// Reverse string
// Recursive (tail):
String reverse(String s, int i, String acc) {
    if (i < 0) return acc;
    return reverse(s, i - 1, acc + s.charAt(i));
}
// Iterative:
String reverse(String s) {
    StringBuilder sb = new StringBuilder(s);
    return sb.reverse().toString();
}

// Check palindrome (tail recursive)
boolean isPalindrome(String s, int l, int r) {
    if (l >= r) return true;
    if (s.charAt(l) != s.charAt(r)) return false;
    return isPalindrome(s, l + 1, r - 1);
}
// Iterative:
boolean isPalindrome(String s) {
    int l = 0, r = s.length() - 1;
    while (l < r) {
        if (s.charAt(l) != s.charAt(r)) return false;
        l++; r--;
    }
    return true;
}
```

---

## 5. Converting Non-Tail Recursion to Iteration

This is harder — you often need an explicit **stack data structure**.

### Template (using explicit stack)

```java
// RECURSIVE (non-tail)
Result function(Input input) {
    if (baseCase(input)) return baseResult;
    Result sub = function(reduce(input));
    return combine(input, sub);
}

// ITERATIVE (with explicit stack)
Result function(Input input) {
    Stack<Input> stack = new Stack<>();
    while (!baseCase(input)) {
        stack.push(input);
        input = reduce(input);
    }
    Result result = baseResult;
    while (!stack.isEmpty()) {
        input = stack.pop();
        result = combine(input, result);
    }
    return result;
}
```

### Examples

```java
// Factorial (non-tail recursive version)
// Recursive:
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
// Iterative with stack:
int factorial(int n) {
    Stack<Integer> stack = new Stack<>();
    while (n > 1) {
        stack.push(n);
        n--;
    }
    int result = 1;
    while (!stack.isEmpty()) {
        result *= stack.pop();
    }
    return result;
}
// But the simple for loop is much cleaner!

// Tree traversal is a better use case for explicit stacks
// Recursive in-order:
void inOrder(TreeNode node, List<Integer> result) {
    if (node == null) return;
    inOrder(node.left, result);
    result.add(node.val);
    inOrder(node.right, result);
}
// Iterative with stack:
void inOrder(TreeNode root, List<Integer> result) {
    Stack<TreeNode> stack = new Stack<>();
    TreeNode curr = root;
    while (curr != null || !stack.isEmpty()) {
        while (curr != null) {
            stack.push(curr);
            curr = curr.left;
        }
        curr = stack.pop();
        result.add(curr.val);
        curr = curr.right;
    }
}
```

---

## 6. When to Use Recursion vs Iteration

### Use Recursion When:

**1. The problem is naturally recursive (tree/graph traversal)**

```java
void dfs(TreeNode node) {
    if (node == null) return;
    visit(node);
    dfs(node.left);
    dfs(node.right);
}
// Iterative DFS is possible but less intuitive (needs explicit stack)
```

**2. Backtracking is involved**

```java
void solveSudoku(char[][] board) {
    // Backtracking — the undo pattern maps naturally to recursion
    // Iterative version would need to manually manage undo state
}
```

**3. The recursive depth is bounded (O(log n))**

```java
// Binary search: depth = log n ≤ 60 for n up to 10^18
int binarySearch(int[] arr, int l, int r, int target) {
    if (l > r) return -1;
    int mid = l + (r - l) / 2;
    if (arr[mid] == target) return mid;
    if (arr[mid] < target) return binarySearch(arr, mid + 1, r, target);
    return binarySearch(arr, l, mid - 1, target);
}
```

**4. Divide-and-conquer algorithms**

```java
// Merge sort: naturally recursive, iterative version is complex
void mergeSort(int[] arr, int l, int r) {
    if (l >= r) return;
    int mid = l + (r - l) / 2;
    mergeSort(arr, l, mid);
    mergeSort(arr, mid + 1, r);
    merge(arr, l, mid, r);
}
```

### Use Iteration When:

**1. Simple linear operations**

```java
// Sum, product, linear search — for loops are cleaner
int sum = 0;
for (int x : arr) sum += x;
```

**2. The recursion depth could be large**

```java
// Quick sort worst-case depth = n!
// For an interview, mention that while recursion is natural,
// you'd use iteration or random pivot for production.

// Iterative quick sort with explicit stack
void quickSortIterative(int[] arr, int low, int high) {
    Stack<int[]> stack = new Stack<>();
    stack.push(new int[]{low, high});
    while (!stack.isEmpty()) {
        int[] range = stack.pop();
        int l = range[0], h = range[1];
        if (l >= h) continue;
        int pi = partition(arr, l, h);
        stack.push(new int[]{l, pi - 1});
        stack.push(new int[]{pi + 1, h});
    }
}
```

**3. Performance is critical**

```java
// Function call overhead is small but measurable
// For tight loops over millions of elements, iteration wins
```

---

## 7. Complete Examples

### Factorial — All 3 Styles

```java
// 1. Non-tail recursive
int factRecursive(int n) {
    if (n <= 1) return 1;
    return n * factRecursive(n - 1);  // O(n) stack
}

// 2. Tail recursive (still O(n) stack in Java!)
int factTailRec(int n, int acc) {
    if (n <= 1) return acc;
    return factTailRec(n - 1, n * acc);  // still O(n) stack in Java
}

// 3. Iterative
int factIterative(int n) {
    int result = 1;
    for (int i = 2; i <= n; i++) result *= i;
    return result;  // O(1) stack
}
```

### Fibonacci

```java
// 1. Recursive (naive) — O(2^n)
int fibRec(int n) {
    if (n <= 1) return n;
    return fibRec(n - 1) + fibRec(n - 2);
}

// 2. Recursive with memoization — O(n)
int fibMemo(int n, int[] memo) {
    if (n <= 1) return n;
    if (memo[n] != 0) return memo[n];
    memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
    return memo[n];
}

// 3. Iterative — O(n), O(1) space
int fibIter(int n) {
    if (n <= 1) return n;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}
```

### Binary Search

```java
// 1. Recursive — O(log n) stack depth
int binarySearchRec(int[] arr, int target, int l, int r) {
    if (l > r) return -1;
    int mid = l + (r - l) / 2;
    if (arr[mid] == target) return mid;
    if (arr[mid] < target) return binarySearchRec(arr, target, mid + 1, r);
    return binarySearchRec(arr, target, l, mid - 1);
}

// 2. Iterative — O(1) stack
int binarySearchIter(int[] arr, int target) {
    int l = 0, r = arr.length - 1;
    while (l <= r) {
        int mid = l + (r - l) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) l = mid + 1;
        else r = mid - 1;
    }
    return -1;
}
```

---

## 8. Decision Guide

```
Is the problem naturally recursive?
├── YES
│   ├── Is depth bounded (≤ 10,000)?
│   │   ├── YES → recursion is fine
│   │   └── NO  → use iteration with explicit stack
│   └── Is backtracking needed?
│       └── YES → recursion is much cleaner
│
└── NO
    └── use iteration

Is performance critical?
├── YES → prefer iteration (no function call overhead)
└── NO  → choose whichever is more readable
```

### Final Java-Specific Advice

```java
// 1. For simple loops → iteration (always)
// 2. For tree/graph DFS → recursion (depth ≤ 10^4 typically)
// 3. For backtracking/puzzles → recursion (natural fit)
// 4. For divide & conquer on small input → recursion
// 5. For anything with depth > 10,000 → iteration
// 6. Don't worry about TCO in Java — it doesn't exist
```

**The best code is readable code that doesn't overflow.** Choose the tool that fits the problem and the constraints.
