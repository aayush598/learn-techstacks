# Stack Implementation Using Linked List

> The array-based stack is clean, but it has one unavoidable pain point: resizing. A linked list eliminates that entirely — each push just allocates a new node. Let's build it.

## Why Linked List for Stack?

With a linked list, we only need to insert and delete at the **head** (beginning). Both are O(1) with no resizing, no capacity limits, and no wasted memory. The trade-off? Each element costs extra memory for the pointer.

**Perfect for stack operations:**
- `push` → insert at head → O(1)
- `pop` → delete from head → O(1)
- `peek` → read head → O(1)

**Terrible for everything else** (random access, search) — but that's not what a stack does.

---

## Node Class

```java
public class Node<T> {
    T data;
    Node<T> next;

    public Node(T data) {
        this(data, null);
    }

    public Node(T data, Node<T> next) {
        this.data = data;
        this.next = next;
    }

    @Override
    public String toString() {
        return data == null ? "null" : data.toString();
    }
}
```

Keep it simple. No getters/setters — we're building a stack, not a library.

---

## Full Linked List Stack

```java
public class LinkedStack<T> {
    private Node<T> top;  // head of the list = top of the stack
    private int size;

    public LinkedStack() {
        top = null;
        size = 0;
    }

    // ─── Core Operations ───

    public void push(T item) {
        // New node points to current top, then becomes the new top
        top = new Node<>(item, top);
        size++;
    }

    public T pop() {
        if (isEmpty()) throw new RuntimeException("Stack is empty");
        T data = top.data;
        top = top.next;  // unlink the old top
        size--;
        return data;
    }

    public T peek() {
        if (isEmpty()) throw new RuntimeException("Stack is empty");
        return top.data;
    }

    public boolean isEmpty() { return top == null; }
    public int size()        { return size; }

    // ─── Utility ───

    public void clear() {
        // Help GC by unlinking all nodes
        Node<T> current = top;
        while (current != null) {
            Node<T> next = current.next;
            current.next = null;
            current.data = null;
            current = next;
        }
        top = null;
        size = 0;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("Top -> ");
        Node<T> current = top;
        while (current != null) {
            sb.append(current.data);
            if (current.next != null) sb.append(" -> ");
            current = current.next;
        }
        sb.append(" -> null");
        return sb.toString();
    }
}
```

### Visual Walkthrough

```
push(10):   top → [10] -> null

push(20):   top → [20] -> [10] -> null

push(30):   top → [30] -> [20] -> [10] -> null

pop():      returns 30
            top → [20] -> [10] -> null

peek():     returns 20 (top unchanged)

pop():      returns 20
            top → [10] -> null

pop():      returns 10
            top → null  (empty)
```

Notice how each operation touches **only the top node**. No loops, no resizing — pure O(1).

---

## The `clear()` Method Matters

You might think `top = null; size = 0;` is enough. It's not. If another reference exists to a node in the middle of the chain, all nodes after it stay in memory. Explicitly unlinking prevents memory leaks in long-running applications.

For interview purposes, `top = null; size = 0;` is acceptable. For production code, use `clear()`.

---

## Enhanced Version: With Iterator Support

```java
import java.util.Iterator;
import java.util.NoSuchElementException;

public class LinkedStack<T> implements Iterable<T> {
    private Node<T> top;
    private int size;

    public LinkedStack() {
        top = null;
        size = 0;
    }

    public void push(T item) {
        top = new Node<>(item, top);
        size++;
    }

    public T pop() {
        if (isEmpty()) throw new RuntimeException("Stack is empty");
        T data = top.data;
        top = top.next;
        size--;
        return data;
    }

    public T peek() {
        if (isEmpty()) throw new RuntimeException("Stack is empty");
        return top.data;
    }

    public boolean isEmpty() { return top == null; }
    public int size()        { return size; }

    @Override
    public Iterator<T> iterator() {
        return new Iterator<T>() {
            private Node<T> current = top;

            @Override
            public boolean hasNext() { return current != null; }

            @Override
            public T next() {
                if (!hasNext()) throw new NoSuchElementException();
                T data = current.data;
                current = current.next;
                return data;
            }
        };
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        Node<T> curr = top;
        while (curr != null) {
            sb.append(curr.data);
            if (curr.next != null) sb.append(", ");
            curr = curr.next;
        }
        sb.append("]");
        return sb.toString();
    }
}
```

Now you can do:

```java
LinkedStack<Integer> stack = new LinkedStack<>();
stack.push(1);
stack.push(2);
stack.push(3);

for (int val : stack) {
    System.out.println(val);  // prints 3, 2, 1 (top to bottom)
}
```

---

## Array Stack vs Linked List Stack

| Feature | Array Stack | Linked List Stack |
|---------|------------|-------------------|
| Push | O(1) amortized | O(1) always |
| Pop | O(1) amortized | O(1) always |
| Peek | O(1) | O(1) |
| Memory per element | 0 extra bytes | 1 pointer (8 bytes on 64-bit) |
| Cache performance | Excellent (contiguous) | Poor (scattered nodes) |
| Resize overhead | O(n) when it happens | Never needed |
| Memory waste | Up to 2x capacity | None (allocate per use) |

**The surprise winner for most real-world use?** Array stack. Despite the amortized resizing, the cache locality advantage of arrays is enormous. A single cache miss on a linked list node can cost more than 100 array operations.

Use linked list stacks when:
- You need guaranteed O(1) worst-case (real-time systems)
- You genuinely don't know the size range
- Memory fragmentation is not a concern

---

## Tricky Interview Question: Min Stack with Linked List

```java
public class MinLinkedStack<T extends Comparable<T>> {
    private Node<T> top;
    private Node<T> minTop;  // separate stack for minimums

    public void push(T item) {
        top = new Node<>(item, top);

        // Push to min stack if it's empty or item <= current min
        if (minTop == null || item.compareTo(minTop.data) <= 0) {
            minTop = new Node<>(item, minTop);
        }
    }

    public T pop() {
        if (isEmpty()) throw new RuntimeException("Stack is empty");
        T data = top.data;
        top = top.next;

        if (data.equals(minTop.data)) {
            minTop = minTop.next;
        }
        return data;
    }

    public T getMin() {
        if (minTop == null) throw new RuntimeException("Stack is empty");
        return minTop.data;
    }

    public boolean isEmpty() { return top == null; }
}
```

Two linked lists doing two stacks' jobs. Clean separation of concerns.

---

## Key Takeaways

1. **Push/pop at head = O(1)** — this is why linked lists work for stacks
2. **Never traverse the list** in a stack operation — if you are, you're doing it wrong
3. **Array stacks win on cache performance** for most workloads
4. **Linked list stacks win on worst-case guarantees** and flexibility
5. **Always null out references** in `pop()` to help garbage collection
6. **`clear()` matters** in production — don't just null the head pointer

The linked list stack is the textbook implementation. In interviews, it's often the first thing they'll ask you to build.
