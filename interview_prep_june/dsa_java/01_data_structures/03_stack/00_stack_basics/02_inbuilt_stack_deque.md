# Inbuilt Stack and Deque in Java

> Java gives you stack and deque implementations out of the box. But not all are created equal. Let's understand what you're using and when to reach for which one.

## java.util.Stack

`Stack<E>` extends `Vector<E>`, which means it inherits **synchronized** methods. Every operation acquires a lock. In a single-threaded program, that's pure waste.

```java
import java.util.Stack;

Stack<Integer> stack = new Stack<>();

// Core operations
stack.push(10);        // adds to top, returns the element
stack.push(20);
stack.push(30);

int top = stack.pop();     // 30 — removes and returns
int peek = stack.peek();   // 20 — returns without removing

boolean empty = stack.empty();  // true if size == 0
int size = stack.size();        // 3

// Search (unique to Stack, NOT in Deque)
int pos = stack.search(10);  // 1-based position from top (0 means not found)
// search(10) returns 3 because 10 is 3rd from top
```

### The full API

```java
// Standard Stack methods (all synchronized)
push(E item)   → E      // add to top
pop()          → E      // remove from top
peek()         → E      // view top
empty()        → boolean // isEmpty() equivalent
search(Object) → int     // 1-based distance from top

// Inherited from Vector (also synchronized)
add(E)         → boolean
insertElementAt(E, index)
removeElementAt(index)
elementAt(index) → E
firstElement() → E
lastElement()  → E
```

### Why `search` is weird

```java
Stack<Integer> s = new Stack<>();
s.push(10);
s.push(20);
s.push(30);

s.search(30); // 1 — top of stack
s.search(20); // 2
s.search(10); // 3
s.search(99); // 0 — not found (0, not -1!)
```

It's 1-based and measures distance from top. This is rarely useful and definitely not worth the synchronized overhead.

---

## Why ArrayDeque is Better

`ArrayDeque<E>` is a **resizable array** implementation of the `Deque` interface. It's faster than `Stack` because:

1. **No synchronization** — single-threaded performance
2. **No legacy Vector baggage** — cleaner API
3. **Better memory** — no Vector's capacity increment overhead
4. **Implements Deque** — can be used as both stack AND queue

Oracle's own documentation recommends:
> *"Deque interface should be used in preference to Stack class."*

### ArrayDeque as a Stack

```java
import java.util.ArrayDeque;
import java.util.Deque;

// Use Deque interface for flexibility
Deque<Integer> stack = new ArrayDeque<>();

// Stack operations
stack.push(10);    // addFirst — O(1)
stack.push(20);    // addFirst — O(1)
stack.push(30);    // addFirst — O(1)

int top = stack.pop();     // removeFirst — O(1), returns 30
int peek = stack.peek();   // getFirst — O(1), returns 20

boolean empty = stack.isEmpty();
int size = stack.size();

// Peek at all elements (for debugging)
System.out.println(stack); // [20, 10]
```

**Key insight:** `push()` adds to the **front** (head), not the end. This makes `pop()` a `removeFirst()` — both O(1) at the head of a circular array.

### Deque terminology mapping

| Stack Concept | Deque Method | Description |
|--------------|-------------|-------------|
| push | `push()` / `addFirst()` | Add to top (front) |
| pop | `pop()` / `removeFirst()` | Remove from top (front) |
| peek | `peek()` / `getFirst()` | View top (front) |
| isEmpty | `isEmpty()` | Check if empty |
| size | `size()` | Current count |

### Alternative: Deque as Queue

```java
Deque<Integer> queue = new ArrayDeque<>();

queue.offer(10);    // addLast — O(1)
queue.offer(20);    // addLast — O(1)
queue.offer(30);    // addLast — O(1)

int front = queue.poll();    // removeFirst — O(1), returns 10
int peek = queue.peek();     // getFirst — O(1), returns 20
```

Same data structure, completely different behavior. The interface is powerful.

---

## Complete Deque API

`Deque<E>` provides 12 methods for each end:

```java
// Element access
getFirst() / getLast()    — throws NoSuchElementException if empty
peekFirst() / peekLast()  — returns null if empty (safer)

// Insertion
addFirst(e) / addLast(e)  — throws IllegalStateException if capacity-constrained
offerFirst(e) / offerLast(e) — returns false if capacity-constrained

// Removal
removeFirst() / removeLast() — throws NoSuchElementException if empty
pollFirst() / pollLast()     — returns null if empty (safer)
```

### The `offer` vs `add` and `poll` vs `remove` distinction

For unbounded deques (like `ArrayDeque`), they're equivalent. For bounded deques (like `ArrayBlockingQueue`):

```
add/offer:  tries to add, fails with exception vs returns false
remove/poll: tries to remove, fails with exception vs returns null
element/peek: tries to view, fails with exception vs returns null
```

**Best practice:** Always use `offer`/`poll`/`peek` for safety.

---

## Performance Comparison

```java
// Benchmark results (rough, single-threaded, 1M operations)
//
// Operation          Stack<E>     ArrayDeque<E>
// ─────────────────────────────────────────────
// push                ~12ms        ~4ms
// pop                 ~11ms        ~3ms
// peek                ~3ms         ~2ms
// iteration           ~15ms        ~8ms
//
// Stack is 2-3x slower due to synchronization
```

### Memory layout

```
Stack (Vector-based):
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ 10  │ 20  │ 30  │  -  │  -  │  -  │  -  │  capacity=8
└─────┴─────┴─────┴─────┴─────┴─────┴─────┘
  ↑ synchronization lock acquired for EVERY operation

ArrayDeque (circular array):
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ 30  │  -  │  -  │  -  │  -  │ 10  │ 20  │  capacity=7
└─────┴─────┴─────┴─────┴─────┴─────┴─────┘
                  ↑ head              ↑ tail
  (circular: tail wraps around to index 0)
```

---

## Practical Examples

### Valid Parentheses

```java
import java.util.ArrayDeque;
import java.util.Deque;

public boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();

    for (char c : s.toCharArray()) {
        switch (c) {
            case '(': case '[': case '{':
                stack.push(c);
                break;
            case ')':
                if (stack.isEmpty() || stack.pop() != '(') return false;
                break;
            case ']':
                if (stack.isEmpty() || stack.pop() != '[') return false;
                break;
            case '}':
                if (stack.isEmpty() || stack.pop() != '{') return false;
                break;
        }
    }
    return stack.isEmpty();
}
```

### DFS Traversal

```java
import java.util.ArrayDeque;
import java.util.Deque;

public void dfs(TreeNode root) {
    if (root == null) return;

    Deque<TreeNode> stack = new ArrayDeque<>();
    stack.push(root);

    while (!stack.isEmpty()) {
        TreeNode node = stack.pop();
        System.out.println(node.val);

        // Push right first so left is processed first (LIFO)
        if (node.right != null) stack.push(node.right);
        if (node.left != null)  stack.push(node.left);
    }
}
```

### Using Deque as both Stack and Queue

```java
Deque<Integer> deque = new ArrayDeque<>();

// As stack
deque.push(1);
deque.push(2);
deque.push(3);
System.out.println(deque.pop());  // 3

// As queue
deque.offer(4);
deque.offer(5);
deque.offer(6);
System.out.println(deque.poll());  // 4 (first in was 4)
```

---

## When to Use What

| Scenario | Use |
|----------|-----|
| Single-threaded stack | `ArrayDeque` |
| Need synchronization | `Collections.synchronizedDeque()` wrapping `ArrayDeque` |
| Need `search()` | `Stack` (rarely needed) |
| Legacy code already uses `Stack` | Keep `Stack`, don't break things |
| Need both stack and queue | `ArrayDeque` (implements both) |
| Need thread-safe deque | `ConcurrentLinkedDeque` (lock-free) |

---

## Common Mistakes

```java
// ❌ Don't do this — mixing Stack and Deque terminology
Stack<Integer> stack = new ArrayDeque<>(); // can't! ArrayDeque isn't a Stack

// ✅ Do this
Deque<Integer> stack = new ArrayDeque<>();

// ❌ Don't use instanceof to check
if (stack instanceof Stack) { ... } // fragile

// ✅ Use interface-based checking
if (stack instanceof Deque) { ... }

// ❌ Don't synchronize when you don't need to
Stack<Integer> s = new Stack<>(); // unnecessary lock overhead

// ✅ Use ArrayDeque in single-threaded code
Deque<Integer> s = new ArrayDeque<>();
```

---

## Key Takeaways

1. **`Stack` is legacy** — synchronized, extends Vector, should be avoided
2. **`ArrayDeque` is the modern choice** — faster, cleaner, more flexible
3. **`push/pop` in ArrayDeque = addFirst/removeFirst** — head of circular array
4. **Use `Deque` interface** for type declarations — keeps you flexible
5. **`offer/poll/peek` are safer** than `add/remove/getFirst` — they return null/false instead of throwing
6. **Same ArrayDeque can be a stack OR queue** — it's the most versatile collection in Java

The Java docs say it best: prefer `Deque` over `Stack`. Now you know why.
