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

### Visual: The Two Ingredients of Recursion

```
  RECURSIVE PROBLEM SOLVING
  =========================

  Original Problem          Smaller Problem          Even Smaller
  ┌──────────────┐          ┌──────────────┐          ┌──────────────┐
  │  factorial(5)│ ──────►  │  factorial(4)│ ──────►  │  factorial(3)│ ──► ...
  │              │ calls    │              │ calls    │              │
  └──────────────┘ itself   └──────────────┘ itself   └──────────────┘
                              (smaller input)

  ... ──► ┌──────────────┐   ┌──────────────┐
          │  factorial(1)│   │  factorial(0)│ ← BASE CASE: stops here!
          │              │   │  returns 1   │
          └──────────────┘   └──────────────┘

  KEY RULE: Every recursive call MUST move toward the base case.
            Otherwise → infinite recursion → stack overflow!
```

### Real-World Analogy

```
  Think of Russian Nesting Dolls (Matryoshka):
  ┌─────────────────────────────────────┐
  │  ┌─────────────────────────────┐    │
  │  │  ┌─────────────────────┐    │    │
  │  │  │  ┌─────────────┐    │    │    │
  │  │  │  │  ┌───────┐   │    │    │    │
  │  │  │  │  │  🪆    │   │    │    │    │  ← base case (smallest)
  │  │  │  │  └───────┘   │    │    │    │
  │  │  │  └─────────────┘    │    │    │
  │  │  └─────────────────────┘    │    │
  │  └─────────────────────────────┘    │
  └─────────────────────────────────────┘
  Open a doll → find a smaller one → repeat until smallest.
  Then put them back together (return values).
```

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

```
  DECISION CHECKLIST — Every recursive function:
  ┌─────────────────────────────────────────────────────────┐
  │ 1. Do I have a base case?          (stops recursion)   │
  │ 2. Does every call move toward it? (prevents infinite)  │
  │ 3. Will I eventually reach it?     (guarantees halting)  │
  └─────────────────────────────────────────────────────────┘
```

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

```python
# COMMON BASE CASES to memorize:
# ┌──────────────────────┬─────────────────────────────────────┐
# │ Pattern              │ Base Case                           │
# ├──────────────────────┼─────────────────────────────────────┤
# │ Count down           │ if n == 0: return / print           │
# │ Factorial            │ if n == 0: return 1                 │
# │ Fibonacci            │ if n <= 1: return n                 │
# │ Tree traversal       │ if node is None: return             │
# │ String processing    │ if len(s) == 0: return              │
# │ Array processing     │ if len(arr) == 0 or idx == len:     │
# │ Power                │ if exp == 0: return 1               │
# │ GCD                  │ if b == 0: return a                 │
# └──────────────────────┴─────────────────────────────────────┘
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

### Recursion Tree for Fibonacci(5)

```
                          fib(5)
                         /      \
                    fib(4)        fib(3)
                   /      \      /      \
              fib(3)    fib(2) fib(2)   fib(1)=1
             /    \    /    \   /    \
         fib(2) fib(1) fib(1) fib(0) fib(1) fib(0)
        /    \    |      |     |       |       |
    fib(1) fib(0) 1      1     1       1       1
      |      |
      1      0

  TOTAL NODES: 15    Unique subproblems: only 5!
  This is WHY we need memoization — without it, O(2^n) redundant work.

  Memoization table:
  ┌─────┬───────┬────────────────────┐
  │  n  │ fib(n)│ Times Computed     │
  ├─────┼───────┼────────────────────┤
  │  0  │   0   │ 5x → cache after 1 │
  │  1  │   1   │ 3x → cache after 1 │
  │  2  │   1   │ 3x → cache after 1 │
  │  3  │   2   │ 2x → cache after 1 │
  │  4  │   3   │ 1x                  │
  │  5  │   5   │ 1x                  │
  └─────┴───────┴────────────────────┘
  With memoization: O(n) time, O(n) space
```

### Recursion Tree for Merge Sort — Divide and Conquer

```
                    merge_sort([38, 27, 43, 3])
                    /                            \
          merge_sort([38, 27])          merge_sort([43, 3])
          /              \              /              \
   merge_sort([38])  merge_sort([27]) merge_sort([43]) merge_sort([3])
        |                  |               |                |
      [38]              [27]             [43]             [3]
          \              /                   \            /
           merge([38,27])                   merge([43,3])
           [27, 38]                          [3, 43]
                    \                        /
                      merge([27,38,3,43])
                      [3, 27, 38, 43]  ← sorted!

  DEPTH: log₂(4) = 2 levels of merging
  WORK PER LEVEL: O(n) for merging
  TOTAL: O(n log n)
```

---

## Head Recursion vs Tail Recursion

### Visual Comparison

```
  HEAD RECURSION:  Work AFTER recursive call
  ═══════════════════════════════════════════
  def f(n):
      if base: return
      f(n-1)      ← recurse FIRST
      <work>      ← then do work  (must remember to do this!)

  Call stack frame must STAY alive to do work after return.
  Stack:  ┌──────────┐
          │ f(3):    │
          │  f(2)    │ ← waiting for f(2) to return
          │  <work>  │ ← work pending after f(2) returns
          └──────────┘

  TAIL RECURSION:  Work BEFORE recursive call (call is last op)
  ═══════════════════════════════════════════════════════════
  def f(n, acc):
      if base: return acc
      <work>      ← do work first
      f(n-1, acc) ← recurse LAST  (nothing left to do!)

  Stack frame NOT needed after call — some languages optimize this away.
  Stack:  ┌──────────┐
          │ f(3, 6): │
          │  <work>   │ ← already done
          │  f(2,6)   │ ← no pending work, can reuse frame!
          └──────────┘

  MIDDLE RECURSION: Work on BOTH sides
  ══════════════════════════════════════
  def traverse(node):
      print(node.val)       ← work BEFORE
      traverse(node.left)   ← recurse
      traverse(node.right)  ← recurse
      # Both sides need the frame alive
```

### Side-by-Side Factorial Examples

```python
# HEAD RECURSION — must multiply AFTER the recursive call returns
def factorial_head(n):
    if n == 0:
        return 1
    result = factorial_head(n - 1)  # go all the way down first
    return n * result               # then multiply on the way back up
    # Frame must be kept alive to compute n * result

# TAIL RECURSION — accumulator carries the result, no work after call
def factorial_tail(n, accumulator=1):
    if n == 0:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)  # LAST operation
    # No pending work → frame can be reused (in languages that optimize)

# Both produce: factorial(5) = 120
# factorial_head(5)  → 5 * (4 * (3 * (2 * (1 * 1)))) = 120
# factorial_tail(5)  → f(4, 5) → f(3, 20) → f(2, 60) → f(1, 120) → f(0, 120) = 120
```

```
  FACTORIAL HEAD vs TAIL — Step-by-step:

  HEAD (build-up on return):        TAIL (carry forward):
  ═════════════════════════          ═══════════════════════
  factorial_head(5):                 factorial_tail(5, 1):
    → call f_h(4)                      → call f_t(4, 5)
      → call f_h(3)                      → call f_t(3, 20)
        → call f_h(2)                      → call f_t(2, 60)
          → call f_h(1)                      → call f_t(1, 120)
            → call f_h(0) → return 1          → call f_t(0, 120) → return 120
            ← return 1*1 = 1                ← return 120
          ← return 2*1 = 2                ← return 120
        ← return 3*2 = 6                ← return 120
      ← return 4*6 = 24               ← return 120
    ← return 5*24 = 120               ← return 120

  Work happens on THE WAY BACK       Result accumulated on THE WAY DOWN
```

---

## Direct vs Indirect Recursion

### Visual Comparison

```
  DIRECT RECURSION: Function calls ITSELF
  ═══════════════════════════════════════════

       ┌───────────┐
       │           │
       ▼           │
    ┌──────┐       │
    │ f(n) │───────┘
    └──────┘
    calls itself

  def countdown(n):
      if n == 0: return
      print(n)
      countdown(n - 1)  # calls countdown → direct recursion

  ═══════════════════════════════════════════════════════════

  INDIRECT RECURSION: A calls B, B calls A (cycle)
  ═══════════════════════════════════════════════════════════

    ┌──────┐     ┌──────┐
    │  A   │────▶│  B   │
    │      │◀────│      │
    └──────┘     └──────┘
    calls B       calls A

  def is_even(n):
      if n == 0: return True
      return is_odd(n - 1)   # A calls B

  def is_odd(n):
      if n == 0: return False
      return is_even(n - 1)  # B calls A

  Call chain for is_even(4):
  is_even(4) → is_odd(3) → is_even(2) → is_odd(1) → is_even(0) → True

  WARNING: Indirect recursion is harder to debug!
  Always ensure BOTH functions have base cases.
```

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

```
  RECURSION LIMIT VISUALIZATION:
  ═══════════════════════════════

  Stack Frame 1000:  ┌──────────┐  ← RecursionError if you go deeper!
  Stack Frame  999:  │          │
  Stack Frame  998:  │          │
       ...            │          │
  Stack Frame    2:  │          │
  Stack Frame    1:  │          │
  Stack Frame    0:  │  MAIN    │  ← First call
                     └──────────┘

  Python default: max 1000 frames
  sys.setrecursionlimit(10000): max 10000 frames
  sys.setrecursionlimit(1 << 25): ~33 million frames (use with caution!)

  ⚠️  WARNING: Setting too high can cause:
  - Segmentation fault (crashes Python entirely)
  - System instability
  - Use iterative approach instead for very deep recursion
```

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

### Without vs With Memoization — Visual Impact

```
  WITHOUT MEMOIZATION: fib(5) — O(2^n) = O(32) calls, most are repeats!

                          fib(5)
                         /       \
                    fib(4)         fib(3)
                   /     \        /     \
              fib(3)   fib(2)  fib(2)  fib(1)
             /   \     /   \    /   \
        fib(2) fib(1) fib(1) fib(0) fib(1) fib(0)
        /   \
    fib(1) fib(0)

  Redundant: fib(3) computed 2x, fib(2) computed 3x, fib(1) computed 5x!

  ═══════════════════════════════════════════════════════════════════

  WITH MEMOIZATION: fib(5) — O(n) = O(5) unique calls!

                          fib(5) → computed, STORED
                         /       \
                    fib(4)         fib(3)
                   /     \        /     \
              fib(3)→CACHED  fib(2)→CACHED  fib(1)→BASE
             /   \
        fib(2)→CACHED  fib(1)→BASE

  Memo Table After:
  ┌────┬──────┬──────────────────────────────────────┐
  │ n  │ fib(n)│ Status                              │
  ├────┼──────┼──────────────────────────────────────┤
  │  0 │   0  │ computed (base case)                 │
  │  1 │   1  │ computed (base case)                 │
  │  2 │   1  │ computed once, cached                │
  │  3 │   2  │ computed once, cached                │
  │  4 │   3  │ computed once, cached                │
  │  5 │   5  │ computed once, cached                │
  └────┴──────┴──────────────────────────────────────┘
  Speedup for fib(40): ~1 second vs ~30 MINUTES (O(2^40) vs O(40))
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

## Common Recursion Mistakes & How to Fix Them

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MISTAKE #1: Missing Base Case                                         │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │  def countdown(n):            def countdown(n):                          │
  │      print(n)                    if n == 0:  # ✓ FIXED                  │
  │      countdown(n - 1)            print(n)                               │
  │      # NO BASE CASE!           countdown(n - 1)                          │
  │      # → RecursionError!                                                    │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MISTAKE #2: Not Moving Toward Base Case                               │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │  def power(b, e):              def power(b, e):                          │
  │      if e == 0: return 1           if e == 0: return 1                  │
  │      return b * power(b, e)  # ←   return b * power(b, e - 1) # ✓      │
  │      # e never changes!             # e decreases → reaches 0           │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MISTAKE #3: Forgetting to Undo State (in backtracking)                 │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │  def backtrack(path, remaining):                                        │
  │      for choice in choices:                                             │
  │          path.append(choice)                                            │
  │          backtrack(path, remaining - choice)                            │
  │          path.pop()  # ← MUST undo! Otherwise path keeps growing       │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MISTAKE #4: Off-by-One in Base Case                                    │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │  def factorial(n):                                                      │
  │      if n == 1: return 1  # ← Should be n == 0 for factorial!          │
  │                           # factorial(0) should return 1, not recurse   │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MISTAKE #5: Returning None When You Should Return a Value              │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │  def find_max(node):                                                    │
  │      if not node: return None  # ← Should return -inf or min_value     │
  │      left = find_max(node.left)  # left could be None → crash!          │
  │                                                                         │
  │  def find_max(node):                  # ✓ FIXED                        │
  │      if not node: return float('-inf')                                  │
  │      return max(node.val, find_max(node.left), find_max(node.right))   │
  └─────────────────────────────────────────────────────────────────────────┘
```

### Debugging Recursive Functions — A Systematic Approach

```python
# TIP 1: Add indentation to trace the call stack
def fib_debug(n, depth=0):
    indent = "  " * depth
    print(f"{indent}fib({n}) called")
    if n <= 1:
        print(f"{indent}  → base case, returning {n}")
        return n
    result = fib_debug(n - 1, depth + 1) + fib_debug(n - 2, depth + 1)
    print(f"{indent}  → fib({n}) = {result}")
    return result

# fib_debug(4) produces:
# fib(4) called
#   fib(3) called
#     fib(2) called
#       fib(1) called
#         → base case, returning 1
#       fib(0) called
#         → base case, returning 0
#     → fib(2) = 1
#     fib(1) called
#       → base case, returning 1
#   → fib(3) = 2
#   fib(2) called
#     fib(1) called
#       → base case, returning 1
#     fib(0) called
#       → base case, returning 0
#   → fib(2) = 1
# → fib(4) = 3

# TIP 2: For small inputs, manually trace the call stack on paper
# TIP 3: Add assertions at key points
def factorial_safe(n):
    assert n >= 0, f"n must be non-negative, got {n}"
    if n == 0:
        return 1
    result = n * factorial_safe(n - 1)
    assert result > 0, f"factorial overflow at n={n}"
    return result
```

---

## Quick Reference — When to Use What

| Problem Type | Pattern | Example | Recurrence |
|-------------|---------|---------|------------|
| Split into subproblems | Divide & Conquer | Merge sort, BST validation | T(n) = aT(n/b) + O(n^d) |
| Reduce to one subproblem | Decrease & Conquer | Binary search, power | T(n) = T(n/b) + O(1) |
| Explore all solutions | Backtracking | Permutations, N-Queens | O(branches^depth) |
| Overlapping subproblems | Memoization/DP | Fibonacci, knapsack | Depends on subproblems |
| Tree traversal | Recursion (DFS) | Inorder, preorder, postorder | O(n) |
| Graph traversal | Recursion or Iterative | DFS, topological sort | O(V + E) |

### Complexity Cheat Sheet

```
  Common Recursion Complexities:
  ╔══════════════════════════════╦════════════════╦════════════════╗
  ║ Recurrence                   ║ Time           ║ Example        ║
  ╠══════════════════════════════╬════════════════╬════════════════╣
  ║ T(n) = T(n-1) + O(1)       ║ O(n)           ║ Factorial      ║
  ║ T(n) = T(n-1) + O(n)       ║ O(n²)          ║ Selection Sort ║
  ║ T(n) = T(n-1) + O(n²)     ║ O(n³)          ║ Naive matrix   ║
  ║ T(n) = 2T(n-1) + O(1)     ║ O(2^n)         ║ Tower of Hanoi ║
  ║ T(n) = T(n-1) + T(n-2)    ║ O(2^n)         ║ Naive Fib      ║
  ║ T(n) = T(n/2) + O(1)       ║ O(log n)       ║ Binary search  ║
  ║ T(n) = 2T(n/2) + O(1)     ║ O(n)           ║ Tree traversal ║
  ║ T(n) = 2T(n/2) + O(n)     ║ O(n log n)     ║ Merge sort     ║
  ║ T(n) = aT(n/b) + O(n^d)   ║ See Master Th. ║ General D&C    ║
  ╚══════════════════════════════╩════════════════╩════════════════╝

  Master Theorem: T(n) = aT(n/b) + O(n^d)
  ┌──────────┬───────────────────────┐
  │ Compare  │ Result                │
  ├──────────┼───────────────────────┤
  │ d < log(a)/log(b) │ O(n^log_b(a)) │
  │ d = log(a)/log(b) │ O(n^d · log n) │
  │ d > log(a)/log(b) │ O(n^d)         │
  └──────────┴───────────────────────┘
```

---

## Key Takeaways for Infosys SP DSE

1. **Always identify the base case first** — it prevents infinite recursion
2. **Every recursive call must move toward the base case**
3. **Use memoization** when you see overlapping subproblems (TLE on recursive solutions)
4. **Convert to iterative** if recursion depth exceeds ~10^5
5. **Backtracking is the most tested recursion pattern** — master the template
6. **Time complexity of naive recursion** for combination/permutation problems is typically O(n!) or O(2^n)
7. **Practice tracing through the call stack** — it helps you understand what's happening at each step
