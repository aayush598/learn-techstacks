# Recursion Fundamentals

## Table of Contents
1. [What is Recursion](#what-is-recursion)
2. [Base Case and Recursive Case](#base-case-and-recursive-case)
3. [How Recursion Works — Call Stack](#how-recursion-works--call-stack)
4. [Head Recursion vs Tail Recursion](#head-recursion-vs-tail-recursion)
5. [Direct vs Indirect Recursion](#direct-vs-indirect-recursion)
6. [Recursion vs Iteration](#recursion-vs-iteration)
7. [Time & Space Complexity](#time--space-complexity)
8. [sys.setrecursionlimit](#syssetrecursionlimit)
9. [Memoization](#memoization)
10. [Recursive Thinking Patterns](#recursive-thinking-patterns)

---

## What is Recursion

A function that **calls itself** to solve a smaller instance of the same problem until it reaches a base case.

```python
def factorial(n):
    if n == 0:          # base case
        return 1
    return n * factorial(n - 1)  # recursive case
```

Every recursive solution has two parts:
1. **Base case** — the condition that stops the recursion
2. **Recursive case** — the part where the function calls itself with a smaller/simpler input

---

## Base Case and Recursive Case

```python
# Bad: no base case → infinite recursion → RecursionError
def bad(n):
    return bad(n - 1)

# Good: base case present
def good(n):
    if n == 0:          # BASE CASE — must be reached
        return 1
    return n * good(n - 1)  # RECURSIVE CASE — moves toward base case
```

**Rule**: Every recursive call must move the problem **closer** to the base case.

```python
# Moving toward base case
def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)  # exp decreases each time

# NOT moving toward base case — infinite loop
def bad_power(base, exp):
    if exp == 0:
        return 1
    return base * bad_power(base, exp)  # exp never changes!
```

---

## How Recursion Works — Call Stack

Python uses a **call stack** to manage recursive calls. Each call pushes a new **stack frame** onto the stack. When a base case is reached, frames start popping off.

### Visualization: `factorial(4)`

```
Call Stack (growing downward):

factorial(4)
│  4 * factorial(3)
│
├── factorial(3)
│   │  3 * factorial(2)
│   │
│   ├── factorial(2)
│   │   │  2 * factorial(1)
│   │   │
│   │   ├── factorial(1)
│   │   │   │  1 * factorial(0)
│   │   │   │
│   │   │   ├── factorial(0)  → returns 1  (BASE CASE)
│   │   │   │
│   │   │   └── returns 1 * 1 = 1
│   │   │
│   │   └── returns 2 * 1 = 2
│   │
│   └── returns 3 * 2 = 6
│
└── returns 4 * 6 = 24
```

```python
# To visualize the call stack yourself
def factorial_verbose(n, depth=0):
    indent = "  " * depth
    print(f"{indent}factorial({n}) called")
    if n == 0:
        print(f"{indent}  Base case reached, returning 1")
        return 1
    result = n * factorial_verbose(n - 1, depth + 1)
    print(f"{indent}  factorial({n}) = {n} * factorial({n-1}) = {result}")
    return result

factorial_verbose(4)
# Output:
# factorial(4) called
#   factorial(3) called
#     factorial(2) called
#       factorial(1) called
#         factorial(0) called
#           Base case reached, returning 1
#         factorial(1) = 1 * factorial(0) = 1
#       factorial(2) = 2 * factorial(1) = 2
#     factorial(3) = 3 * factorial(2) = 6
#   factorial(4) = 4 * factorial(3) = 24
```

---

## Head Recursion vs Tail Recursion

### Tail Recursion
The recursive call is the **last operation** in the function. The current frame is not needed after the call returns.

```python
# TAIL RECURSION — recursive call is the LAST thing done
def factorial_tail(n, accumulator=1):
    if n == 0:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)  # nothing after this
```

### Head Recursion
The recursive call is **not the last operation**. Work remains after the call returns.

```python
# HEAD RECURSION — work done AFTER recursive call returns
def factorial_head(n):
    if n == 0:
        return 1
    result = factorial_head(n - 1)  # recursive call first
    return n * result               # work done after
```

### Middle Recursion
Work done both before and after the recursive call.

```python
# MIDDLE RECURSION — work on both sides
def print_tree(node):
    if node is None:
        return
    print(node.val)              # work before
    print_tree(node.left)        # recursive call
    print_tree(node.right)       # recursive call
```

**Key insight**: Tail recursion can be optimized by some languages (not Python) into a loop. In Python, tail recursion still uses stack frames.

---

## Direct vs Indirect Recursion

### Direct Recursion
Function calls **itself**.

```python
def countdown(n):
    if n == 0:
        print("Go!")
        return
    print(n)
    countdown(n - 1)  # calls itself
```

### Indirect Recursion
Function A calls Function B, which calls Function A.

```python
def is_even(n):
    if n == 0:
        return True
    return is_odd(n - 1)  # calls is_odd

def is_odd(n):
    if n == 0:
        return False
    return is_even(n - 1)  # calls is_even

print(is_even(4))  # True
print(is_odd(3))   # True
```

### Mutual Recursion Chain
```python
def A(n):
    if n <= 0:
        return 1
    return B(n - 1)

def B(n):
    if n <= 0:
        return 0
    return A(n - 1)
```

---

## Recursion vs Iteration

| Aspect | Recursion | Iteration |
|--------|-----------|-----------|
| Code clarity | Cleaner for tree/graph problems | Can be verbose |
| Memory | O(n) call stack | O(1) extra (usually) |
| Speed | Slower (function call overhead) | Faster |
| Stack overflow risk | Yes (deep recursion) | No |
| Natural fit | Trees, graphs, divide & conquer | Linear loops |

```python
# RECURSIVE approach
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

# ITERATIVE approach
def fibonacci_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# When to use recursion:
# - Tree traversals (DFS, BST operations)
# - Graph algorithms (DFS, cycle detection)
# - Divide and conquer (merge sort, quicksort)
# - Backtracking (permutations, combinations, N-Queens)
# - Dynamic programming (top-down)
# - Problems that are naturally recursive (factorial, Fibonacci)

# When to use iteration:
# - Simple linear problems
# - When memory is critical
# - When stack depth could be very large
```

---

## Time & Space Complexity

### Time Complexity — Recurrence Relations

Recursive time complexity is expressed as **recurrences**.

```python
# Example 1: Factorial — T(n) = T(n-1) + O(1) → O(n)
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

# Example 2: Fibonacci — T(n) = T(n-1) + T(n-2) + O(1) → O(2^n)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# Example 3: Tower of Hanoi — T(n) = 2*T(n-1) + O(1) → O(2^n)
def tower_of_hanoi(n, src, aux, dst):
    if n == 0:
        return
    tower_of_hanoi(n - 1, src, dst, aux)
    print(f"Move disk {n} from {src} to {dst}")
    tower_of_hanoi(n - 1, aux, src, dst)

# Example 4: Binary search — T(n) = T(n/2) + O(1) → O(log n)
def binary_search(arr, target, lo, hi):
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, hi)
    else:
        return binary_search(arr, target, lo, mid - 1)
```

### Space Complexity — Call Stack

```python
# Space: O(n) due to call stack depth of n
def recursive_sum(n):
    if n == 0:
        return 0
    return n + recursive_sum(n - 1)
# Maximum call stack depth: n + 1 frames

# Space: O(log n) — binary recursion tree depth
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
# Each level uses O(n) for merging, depth is O(log n)
# Total space: O(n) for the arrays + O(log n) for the stack
```

---

## sys.setrecursionlimit

Python's default recursion limit is **1000**. For deeper recursion, increase it.

```python
import sys

# Default limit
print(sys.getrecursionlimit())  # 1000

# Increase limit
sys.setrecursionlimit(10000)

# WARNING: Setting too high can cause segmentation fault (crashes Python)
# The actual limit depends on OS stack size

# Best practice for competitive programming
def setup():
    import sys
    sys.setrecursionlimit(1 << 25)  # ~33 million

# If you need very deep recursion, convert to iterative
# or use an explicit stack

# Example: DFS on large graph (10^5 nodes)
import sys
sys.setrecursionlimit(200000)

def dfs(u, graph, visited):
    visited.add(u)
    for v in graph[u]:
        if v not in visited:
            dfs(v, graph, visited)

# For very large inputs, prefer iterative DFS with an explicit stack:
def dfs_iterative(start, graph):
    visited = set()
    stack = [start]
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        for v in graph[u]:
            if v not in visited:
                stack.append(v)
```

---

## Memoization

### Using `@functools.lru_cache`

```python
import functools

@functools.lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(100))  # Instant! Without memoization: would take forever
print(fib.cache_info())  # Shows hits, misses, size
```

### Using `@cache` (Python 3.9+)

```python
from functools import cache

@cache
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# Same as lru_cache(maxsize=None) but slightly faster
# No cache_info() method
```

### Manual Memoization

```python
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

### Memoization with 2D state

```python
from functools import lru_cache

def knapsack(n, W, weights, values):
    @lru_cache(maxsize=None)
    def dp(i, remaining_w):
        if i == n or remaining_w == 0:
            return 0
        # Don't take item i
        result = dp(i + 1, remaining_w)
        # Take item i (if it fits)
        if weights[i] <= remaining_w:
            result = max(result, values[i] + dp(i + 1, remaining_w - weights[i]))
        return result
    return dp(0, W)
```

---

## Recursive Thinking Patterns

### Pattern 1: Divide and Conquer

**Idea**: Split the problem into **two or more subproblems**, solve each independently, combine results.

```python
# Merge Sort — classic divide and conquer
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])     # DIVIDE
    right = merge_sort(arr[mid:])    # DIVIDE
    return merge(left, right)        # CONQUER (combine)

def merge(l, r):
    result = []
    i = j = 0
    while i < len(l) and j < len(r):
        if l[i] <= r[j]:
            result.append(l[i])
            i += 1
        else:
            result.append(r[j])
            j += 1
    result.extend(l[i:])
    result.extend(r[j:])
    return result

# Maximum subarray (Kadane's as divide and conquer)
def max_crossing_subarray(arr, lo, mid, hi):
    left_sum = float('-inf')
    s = 0
    for i in range(mid, lo - 1, -1):
        s += arr[i]
        left_sum = max(left_sum, s)

    right_sum = float('-inf')
    s = 0
    for i in range(mid + 1, hi + 1):
        s += arr[i]
        right_sum = max(right_sum, s)

    return left_sum + right_sum

def max_subarray(arr, lo, hi):
    if lo == hi:
        return arr[lo]
    mid = (lo + hi) // 2
    left_max = max_subarray(arr, lo, mid)
    right_max = max_subarray(arr, mid + 1, hi)
    cross_max = max_crossing_subarray(arr, lo, mid, hi)
    return max(left_max, right_max, cross_max)
```

**When to use**: Problem can be split into independent subproblems of the same type.
**Recurrence**: T(n) = aT(n/b) + O(n^d) → solved via Master Theorem.

### Pattern 2: Decrease and Conquer

**Idea**: Reduce the problem to **one smaller subproblem**, solve it, extend the result.

```python
# Binary search — decrease by half each time
def binary_search(arr, target, lo=0, hi=None):
    if hi is None:
        hi = len(arr) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, hi)
    else:
        return binary_search(arr, target, lo, mid - 1)

# Power computation — decrease by half
def power(base, exp):
    if exp == 0:
        return 1
    if exp % 2 == 0:
        half = power(base, exp // 2)
        return half * half
    else:
        return base * power(base, exp - 1)

# Linked list operations (reverse, length, etc.)
def reverse_list(head):
    if head is None or head.next is None:
        return head
    new_head = reverse_list(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

**When to use**: Problem naturally reduces to a single smaller instance.

### Pattern 3: Backtracking

**Idea**: Explore all possible solutions by **making a choice**, **recursing**, and **undoing the choice** (backtrack) if it doesn't lead to a solution.

```python
# Generate all permutations
def permutations(nums):
    result = []

    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])
            return

        for i in range(len(remaining)):
            # Make choice
            current.append(remaining[i])
            # Explore
            backtrack(current, remaining[:i] + remaining[i+1:])
            # Undo choice
            current.pop()

    backtrack([], nums)
    return result

# Solve N-Queens
def solve_n_queens(n):
    result = []
    board = ['.' * n for _ in range(n)]

    def is_safe(row, col):
        for r in range(row):
            c = board[r].index('Q') if 'Q' in board[r] else -1
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True

    def backtrack(row):
        if row == n:
            result.append(board[:])
            return
        for col in range(n):
            if is_safe(row, col):
                board[row] = '.' * col + 'Q' + '.' * (n - col - 1)
                backtrack(row + 1)
                board[row] = '.' * n  # undo

    backtrack(0)
    return result
```

**When to use**: 
- Need to explore all combinations/permutations
- Need to find one valid solution among many possibilities
- Constraint satisfaction problems

**This is the most important pattern for Infosys SP DSE — see the backtracking files for more.**

---

## Quick Reference — When to Use What

| Problem Type | Pattern | Example |
|-------------|---------|---------|
| Split into subproblems | Divide & Conquer | Merge sort, BST validation |
| Reduce to one subproblem | Decrease & Conquer | Binary search, power |
| Explore all solutions | Backtracking | Permutations, N-Queens |
| Overlapping subproblems | Memoization/DP | Fibonacci, knapsack |
| Tree traversal | Recursion (DFS) | Inorder, preorder, postorder |
| Graph traversal | Recursion or Iterative | DFS, topological sort |

---

## Key Takeaways for Infosys SP DSE

1. **Always identify the base case first** — it prevents infinite recursion
2. **Every recursive call must move toward the base case**
3. **Use memoization** when you see overlapping subproblems (TLE on recursive solutions)
4. **Convert to iterative** if recursion depth exceeds ~10^5
5. **Backtracking is the most tested recursion pattern** — master the template
6. **Time complexity of naive recursion** for combination/permutation problems is typically O(n!) or O(2^n)
7. **Practice tracing through the call stack** — it helps you understand what's happening at each step
