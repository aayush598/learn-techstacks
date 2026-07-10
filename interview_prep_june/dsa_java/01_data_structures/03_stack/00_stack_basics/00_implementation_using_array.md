# Stack Implementation Using Array

> A stack is the simplest data structure that embodies the LIFO (Last In, First Out) principle. Think of a stack of plates — you always add to the top and remove from the top. Let's build one from scratch.

## The Core Contract

Before writing code, let's be crystal clear about what a stack promises:

```
push(x)  → Add x to the top
pop()     → Remove and return the top element
peek()    → Return the top element without removing
isEmpty() → Is the stack empty?
isFull()  → Is the stack at capacity? (only for fixed-size)
```

Every single operation must be **O(1)**. If any operation starts looping, you've built something else.

---

## Fixed-Size Array Stack

The most basic version — an array with a `top` pointer.

```java
public class FixedStack<T> {
    private Object[] arr;
    private int top;  // index of the top element, -1 when empty

    @SuppressWarnings("unchecked")
    public FixedStack(int capacity) {
        if (capacity <= 0) throw new IllegalArgumentException("Capacity must be positive");
        arr = new Object[capacity];
        top = -1;
    }

    public void push(T item) {
        if (isFull()) throw new RuntimeException("Stack Overflow — cannot push to full stack");
        arr[++top] = item;
    }

    @SuppressWarnings("unchecked")
    public T pop() {
        if (isEmpty()) throw new RuntimeException("Stack Underflow — cannot pop from empty stack");
        T item = (T) arr[top];
        arr[top--] = null; // help GC, avoid loitering
        return item;
    }

    @SuppressWarnings("unchecked")
    public T peek() {
        if (isEmpty()) throw new RuntimeException("Stack is empty");
        return (T) arr[top];
    }

    public boolean isEmpty() { return top == -1; }
    public boolean isFull()  { return top == arr.length - 1; }
    public int size()        { return top + 1; }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        for (int i = top; i >= 0; i--) {
            sb.append(arr[i]);
            if (i > 0) sb.append(", ");
        }
        sb.append("] ← top");
        return sb.toString();
    }
}
```

### The `top` pointer trick

Notice `top` starts at `-1`. This is intentional:
- **Empty**: `top == -1`
- **First push**: `arr[++top]` → `arr[0]`, top becomes 0
- **Pop**: returns `arr[top]`, then `top--`

This gives us clean `isEmpty()` and `size()` checks with zero ambiguity. Some implementations use `top = 0` with `size` tracking separately — both work, but the `-1` convention is more common.

### Usage

```java
FixedStack<Integer> stack = new FixedStack<>(5);
stack.push(10);
stack.push(20);
stack.push(30);
System.out.println(stack);      // [30, 20, 10] ← top
System.out.println(stack.pop()); // 30
System.out.println(stack.peek()); // 20
System.out.println(stack.size()); // 2
```

---

## Dynamic Array Stack (Resizing)

The fixed-size stack's biggest limitation is obvious — what if you don't know the capacity ahead of time? The solution: **resize the array when it gets full**.

This is exactly how `ArrayList` and `java.util.Stack` work under the hood.

```java
public class DynamicStack<T> {
    private static final int DEFAULT_CAPACITY = 16;
    private static final double LOAD_FACTOR = 0.75;

    private Object[] arr;
    private int top;

    public DynamicStack() {
        arr = new Object[DEFAULT_CAPACITY];
        top = -1;
    }

    public DynamicStack(int initialCapacity) {
        arr = new Object[Math.max(initialCapacity, 2)];
        top = -1;
    }

    public void push(T item) {
        if (top + 1 >= arr.length) {
            resize(arr.length * 2);  // double the capacity
        }
        arr[++top] = item;
    }

    @SuppressWarnings("unchecked")
    public T pop() {
        if (isEmpty()) throw new RuntimeException("Stack is empty");
        T item = (T) arr[top];
        arr[top--] = null;

        // Optional: shrink when usage drops below 25%
        if (top > 0 && top + 1 < arr.length / 4) {
            resize(arr.length / 2);
        }
        return item;
    }

    @SuppressWarnings("unchecked")
    public T peek() {
        if (isEmpty()) throw new RuntimeException("Stack is empty");
        return (T) arr[top];
    }

    public boolean isEmpty() { return top == -1; }
    public int size()        { return top + 1; }

    private void resize(int newCapacity) {
        Object[] newArr = new Object[newCapacity];
        for (int i = 0; i <= top; i++) {
            newArr[i] = arr[i];
        }
        arr = newArr;
        // System.out.println("Resized to capacity: " + newCapacity);
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("Stack[");
        for (int i = top; i >= 0; i--) {
            sb.append(arr[i]);
            if (i > 0) sb.append(", ");
        }
        sb.append("]");
        return sb.toString();
    }
}
```

### Why resize to 2x (and shrink to 0.5x)?

This is the classic **amortized O(1)** argument:

| Operation | Cost | Amortized |
|-----------|------|-----------|
| Normal push | O(1) | O(1) |
| Push that triggers resize | O(n) | O(1) |
| **Overall** | — | **O(1)** |

If we only increased capacity by 1 each time, resize would happen every push → O(n) per push → terrible.

**The shrinking part** prevents memory waste. If you pushed 1 million elements and then popped them all, you'd still hold a million-element array. Shrinking at 25% threshold keeps memory proportional to actual usage.

---

## Generic Type Safety

Let's talk about the generics properly. You'll notice `@SuppressWarnings("unchecked")` and `Object[]` — that's because **Java doesn't support generic arrays**. Here's why:

```java
// This does NOT compile:
T[] arr = new T[capacity]; // error: generic array creation

// What we do instead:
Object[] arr = new Object[capacity];
// Then cast on retrieval:
T item = (T) arr[index]; // unchecked cast, hence @SuppressWarnings
```

This is a language limitation, not a design flaw. The cast is safe because we only ever put `T` objects into the array. The `@SuppressWarnings` tells the compiler "I know what I'm doing here."

### A cleaner pattern: separate the generic wrapper

```java
// Helper to create typed arrays (for more complex DS)
@SuppressWarnings("unchecked")
private T[] createArray(int size) {
    return (T[]) new Object[size];
}
```

---

## Edge Cases to Always Handle

These are the bugs that show up in production at 3 AM:

```java
// 1. Pushing null — debateable, but usually bad
public void push(T item) {
    if (item == null) throw new NullPointerException("Null elements not allowed");
    // ...
}

// 2. Pop/peek on empty — the #1 stack bug
// ALWAYS check isEmpty() before pop/peek, or throw a meaningful exception

// 3. Integer overflow on resize (theoretical but real)
// In practice, if top+1 overflows int, you have bigger problems

// 4. Concurrent access
// This is NOT thread-safe. For thread safety, use Collections.synchronizedDeque()
// or java.util.concurrent.ConcurrentLinkedDeque
```

---

## Testing Your Implementation

Always test with these scenarios:

```java
public static void main(String[] args) {
    DynamicStack<Integer> stack = new DynamicStack<>();

    // Test empty stack
    assert stack.isEmpty() : "New stack should be empty";

    // Test push and pop
    for (int i = 1; i <= 100; i++) {
        stack.push(i);
    }
    assert stack.size() == 100;

    // Verify LIFO order
    for (int i = 100; i >= 1; i--) {
        assert stack.pop() == i : "Expected " + i;
    }
    assert stack.isEmpty();

    // Test resize triggers
    for (int i = 0; i < 1000; i++) {
        stack.push(i * 10);
    }
    assert stack.size() == 1000;

    // Test shrink
    while (!stack.isEmpty()) {
        stack.pop();
    }
    assert stack.isEmpty();

    System.out.println("All tests passed!");
}
```

---

## Comparison: Fixed vs Dynamic

| Feature | Fixed-Size | Dynamic |
|---------|-----------|---------|
| Capacity | Known at creation | Grows as needed |
| Push | O(1) always | O(1) amortized |
| Memory | Exact, no waste | May over-allocate |
| Use case | Embedded, known bounds | General purpose |

---

## Key Takeaways

1. **`top = -1` is the cleanest convention** for empty detection
2. **Always null out popped references** to avoid memory leaks (loitering)
3. **Resize by doubling** for amortized O(1) push
4. **Shrink at 25%** to reclaim memory — don't let a million-element array sit around for 3 elements
5. **Generics use Object[] + casts** — this is the standard Java pattern, not a hack
6. **Never skip empty checks** — stack underflow/overflow is the most common bug

Next up: implementing a stack with a linked list, which eliminates the resizing complexity entirely.
