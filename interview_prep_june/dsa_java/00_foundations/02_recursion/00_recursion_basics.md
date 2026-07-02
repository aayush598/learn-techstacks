# 00 — Recursion Basics

Recursion is the foundation of most advanced algorithms — trees, graphs, divide-and-conquer, backtracking, dynamic programming. Mastering recursion means mastering the art of **delegation**: a function solves a big problem by calling itself on a smaller version of the same problem.

---

## 1. What is Recursion?

**Recursion** is when a function calls itself.

```java
void callMe() {
    callMe();  // infinite recursion!
}
```

That's the idea. But without a **base case**, it runs forever (until stack overflow). Every recursive function needs two parts:

```
1. Base case:   The simplest version of the problem (stopping condition)
2. Recursive case: Break the problem into a smaller version of itself
```

### The First Recursion: Countdown

```java
void countdown(int n) {
    // Base case
    if (n == 0) {
        System.out.println("Go!");
        return;
    }

    // Recursive case
    System.out.println(n);
    countdown(n - 1);
}

// countdown(5) prints:
// 5
// 4
// 3
// 2
// 1
// Go!
```

---

## 2. The Call Stack — How Recursion Works

Every function call creates a **stack frame** (or activation record) containing:
- Local variables
- Parameters
- Return address (where to continue executing)

When a function calls itself recursively, a **new frame** is pushed onto the call stack.

### Visualizing countdown(3)

```
Step 1: main() calls countdown(3)
Stack:
[countdown(3)]         → n=3, print "3", calls countdown(2)

Step 2: countdown(3) calls countdown(2)
Stack:
[countdown(2)]         → n=2, print "2", calls countdown(1)
[countdown(3)]

Step 3: countdown(2) calls countdown(1)
Stack:
[countdown(1)]         → n=1, print "1", calls countdown(0)
[countdown(2)]
[countdown(3)]

Step 4: countdown(1) calls countdown(0)
Stack:
[countdown(0)]         → n=0, print "Go!", returns
[countdown(1)]
[countdown(2)]
[countdown(3)]

Step 5: countdown(0) returns, pop frame
Stack:
[countdown(1)]         → resumes, returns
[countdown(2)]
[countdown(3]

Step 6: countdown(1) returns, pop frame
[countdown(2)]         → resumes, returns
[countdown(3)]

Step 7: countdown(2) returns, pop frame
[countdown(3)]         → resumes, returns

Step 8: countdown(3) returns → back to main()
```

**Key insight:** The "unwinding" happens in reverse order. The last called function returns first (LIFO — Last In, First Out).

---

## 3. Types of Recursion

### Head Recursion

The recursive call is the **first** thing in the function.

```java
void printNto1(int n) {
    if (n == 0) return;
    System.out.print(n + " ");      // work happens BEFORE recursion
    printNto1(n - 1);               // recursive call
}
// printNto1(5) → 5 4 3 2 1
```

### Tail Recursion

The recursive call is the **last** thing in the function (no pending work after).

```java
void print1toN(int n) {
    if (n == 0) return;
    print1toN(n - 1);               // recursive call
    System.out.print(n + " ");      // work happens AFTER recursion returns
}
// print1toN(5) → 1 2 3 4 5
```

Wait — the recursive call is first here, not last. Let's fix:

```java
// TRUE tail recursion: recursive call is the LAST operation
void print1toNTail(int n, int current) {
    if (current > n) return;
    System.out.print(current + " ");   // do work
    print1toNTail(n, current + 1);     // recursive call is LAST
}
// print1toNTail(5, 1) → 1 2 3 4 5
```

**Tail recursion importance:** If the language supports **Tail Call Optimization (TCO)**, the compiler can reuse the current stack frame instead of creating a new one, making tail recursion O(1) stack space instead of O(n).

**Java does NOT have TCO.** Every recursive call in Java creates a new stack frame, regardless of head/tail.

### Head vs Tail — When Work Happens

```java
// HEAD recursion: print happens BEFORE recursion
// Order: print(5), print(4), print(3), print(2), print(1)
void head(int n) {
    if (n == 0) return;
    System.out.println(n);
    head(n - 1);
}

// TAIL recursion: print happens AFTER recursion
// Order: print(1), print(2), print(3), print(4), print(5)
void tail(int n) {
    if (n == 0) return;
    tail(n - 1);
    System.out.println(n);
}
```

**Think of it this way:** Head recursion builds the result on the way **down** the stack. Tail recursion builds it on the way **back up**.

---

## 4. The 3-Step Method to Write Recursion

### Step 1: Identify the Base Case(s)

What's the simplest input? The one you can solve without recursion.

```java
// Factorial
if (n == 0) return 1;   // 0! = 1
if (n == 1) return 1;   // 1! = 1

// Sum of array
if (index == arr.length) return 0;

// Fibonacci
if (n <= 1) return n;
```

### Step 2: Find the Recurrence Relation

How does the problem relate to a smaller version of itself?

```java
// Factorial
n! = n × (n-1)!           // T(n) = n × T(n-1)

// Sum of array
sum(arr, n) = arr[n-1] + sum(arr, n-1)

// Fibonacci
fib(n) = fib(n-1) + fib(n-2)
```

### Step 3: Trust the Recursion

Assume the recursive call will work correctly for the smaller input. Don't trace through every call — your brain can't hold more than 3-4 levels.

```java
int factorial(int n) {
    // Step 1: Base case
    if (n <= 1) return 1;

    // Step 2: Recurrence
    // Step 3: Trust that factorial(n-1) returns the right answer
    return n * factorial(n - 1);
}
```

**Trust is the hardest part.** Beginners want to trace every call. Experts write the recurrence and trust that it works.

---

## 5. Stack Overflow — Why It Happens

```java
int factorial(int n) {
    return n * factorial(n - 1);  // ❌ No base case!
    // Eventually: StackOverflowError
}
```

Without a base case, recursion never stops. Each call adds a frame to the stack. The stack has finite size (~8 MB default on most JVMs).

### How Deep Can We Go?

```java
// Experiment: how many recursive calls before overflow?
int depth = 0;
void recurse() {
    depth++;
    recurse();
}
// Typically: ~10,000 to 40,000 calls (varies by JVM config)
```

```java
// ❌ This will overflow for n = 100,000
void countUp(int n) {
    if (n == 0) return;
    countUp(n - 1);  // 100,000 frames on stack!
}

// ✅ This is fine (iterative)
void countUp(int n) {
    for (int i = 1; i <= n; i++) {
        System.out.println(i);
    }
}
```

### Stack Size Configuration

```bash
java -Xss1m Main        # 1 MB stack (default on many JVMs)
java -Xss256k Main      # 256 KB stack (minimal)
java -Xss4m Main        # 4 MB stack (larger)
```

**Rule of thumb:** If your recursion depth could exceed a few thousand, prefer iteration. In DSA, recursive depth is usually O(log n) or O(n) with n ≤ 10⁵ — borderline but often okay for O(log n) cases.

---

## 6. Classic Examples

### Factorial

```java
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
// factorial(5) = 5 × 4 × 3 × 2 × 1 = 120
```

### Fibonacci (Naive)

```java
int fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}
// fib(6) = 8
// ⚠️ This is O(2ⁿ) — will be slow for n > 30
```

**The problem:** `fib(5)` calls `fib(4)` and `fib(3)`. `fib(4)` calls `fib(3)` and `fib(2)`. `fib(3)` is computed twice! The call tree has 2ⁿ nodes.

### Print 1 to N

```java
void print1toN(int n) {
    if (n == 0) return;
    print1toN(n - 1);       // go to base first
    System.out.println(n);  // print on way back
}
// print1toN(5) → 1 2 3 4 5
```

### Print N to 1

```java
void printNto1(int n) {
    if (n == 0) return;
    System.out.println(n);  // print first
    printNto1(n - 1);       // then recurse
}
// printNto1(5) → 5 4 3 2 1
```

### Sum of First N Natural Numbers

```java
int sum(int n) {
    if (n == 0) return 0;
    return n + sum(n - 1);
}
// sum(5) = 5 + 4 + 3 + 2 + 1 + 0 = 15
```

### Power (Exponentiation)

```java
int power(int base, int exp) {
    if (exp == 0) return 1;
    return base * power(base, exp - 1);
}
// power(2, 5) = 2 × 2 × 2 × 2 × 2 = 32
// O(n) — but we can do better with fast exponentiation
```

### Fast Exponentiation (O(log n))

```java
int fastPower(int base, int exp) {
    if (exp == 0) return 1;
    int half = fastPower(base, exp / 2);
    if (exp % 2 == 0) {
        return half * half;
    } else {
        return base * half * half;
    }
}
// fastPower(2, 10) → halves exp: 10 → 5 → 2 → 1 → 0
// Only O(log n) recursive calls!
```

---

## 7. Common Recursion Pitfalls

### Pitfall 1: Missing Base Case

```java
int sum(int n) {
    return n + sum(n - 1);  // ❌ never stops! StackOverflowError
}
```

Fix: Add `if (n <= 0) return 0;`

### Pitfall 2: Base Case Never Reached

```java
int factorial(int n) {
    if (n == 0) return 1;   // base case at 0
    return n * factorial(n - 2);  // ❌ skips by 2 — n=5 → 3 → 1 → -1 → never hits 0!
}
```

Fix: Ensure progression reaches the base case. `if (n <= 1) return 1;`

### Pitfall 3: Wrong Return Type

```java
void sum(int n) {  // ❌ returns void!
    if (n == 0) return;
    return n + sum(n - 1);  // error: can't add int to void
}
```

### Pitfall 4: Exponential Blowup (Naive Fibonacci)

```java
int fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);  // O(2ⁿ) — fib(50) will never finish
}
```

Fix: Use memoization or iteration.

### Pitfall 5: Passing the Same Data Inefficiently

```java
// Bad — creates substring (copy) each call
boolean isPalindromeBAD(String s) {
    if (s.length() <= 1) return true;
    if (s.charAt(0) != s.charAt(s.length() - 1)) return false;
    return isPalindromeBAD(s.substring(1, s.length() - 1));  // O(n) copy!
}

// Good — uses indices
boolean isPalindrome(String s, int left, int right) {
    if (left >= right) return true;
    if (s.charAt(left) != s.charAt(right)) return false;
    return isPalindrome(s, left + 1, right - 1);  // O(1) per call
}
```

---

## 8. Recursion vs Iteration — When to Use Which

| Aspect | Recursion | Iteration |
|--------|-----------|-----------|
| Code clarity | Better for tree/graph/backtracking | Better for simple loops |
| Stack space | O(depth) — can overflow | O(1) |
| Performance | Overhead of function calls | Faster |
| Complexity | Harder to reason about some patterns | More straightforward |

**Use recursion when:**
- The problem is naturally recursive (trees, graphs, divide-and-conquer)
- The recursive depth is small (O(log n))
- You're doing backtracking (undo choices)
- The iterative solution would need explicit stack management

**Use iteration when:**
- The problem is a simple linear operation
- Recursive depth could be large (n > 10,000)
- Performance is critical and the overhead matters

---

## Recursion Cheat Sheet

```java
// FORMULA:
// 1. Base case — when to stop
// 2. Recursive case — how to break down
// 3. Trust — assume the recursion works

// EXAMPLES:
factorial(n)     → n * factorial(n-1), base n≤1
fib(n)           → fib(n-1) + fib(n-2), base n≤1 (O(2ⁿ) naive)
sum(n)           → n + sum(n-1), base n=0
power(b, e)      → b * power(b, e-1), base e=0
print1toN(n)     → print1toN(n-1) then print(n)
printNto1(n)     → print(n) then printNto1(n-1)

// KEY INSIGHT:
// Head recursion: work before call → processes forward (n to 1)
// Tail recursion: work after call → processes backward (1 to n)
// Java has no TCO → every call creates a frame
```

The best way to learn recursion is to write it. Start with the examples here, trace through a few small inputs, then trust the recursion.
