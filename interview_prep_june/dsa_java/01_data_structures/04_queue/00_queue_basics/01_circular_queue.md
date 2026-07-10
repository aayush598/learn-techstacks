# Circular Queue — Full Implementation with Resize

> The fixed-size circular queue has one limitation: what happens when you need more capacity? Let's build a production-quality circular queue that resizes dynamically.

## Full Implementation

```java
public class DynamicCircularQueue<T> {
    private static final int DEFAULT_CAPACITY = 16;
    private Object[] arr;
    private int front;
    private int rear;
    private int size;

    public DynamicCircularQueue() {
        arr = new Object[DEFAULT_CAPACITY];
        front = 0;
        rear = -1;
        size = 0;
    }

    public DynamicCircularQueue(int initialCapacity) {
        arr = new Object[Math.max(initialCapacity, 2)];
        front = 0;
        rear = -1;
        size = 0;
    }

    // ─── Core Operations ───

    public void enqueue(T item) {
        if (size == arr.length) {
            resize(arr.length * 2);
        }
        rear = (rear + 1) % arr.length;
        arr[rear] = item;
        size++;
    }

    @SuppressWarnings("unchecked")
    public T dequeue() {
        if (isEmpty()) throw new RuntimeException("Queue is empty");
        T item = (T) arr[front];
        arr[front] = null;  // help GC
        front = (front + 1) % arr.length;
        size--;

        // Shrink if too empty (but keep minimum capacity)
        if (size > 0 && size < arr.length / 4 && arr.length > DEFAULT_CAPACITY) {
            resize(Math.max(arr.length / 2, DEFAULT_CAPACITY));
        }

        return item;
    }

    @SuppressWarnings("unchecked")
    public T peek() {
        if (isEmpty()) throw new RuntimeException("Queue is empty");
        return (T) arr[front];
    }

    @SuppressWarnings("unchecked")
    public T peekRear() {
        if (isEmpty()) throw new RuntimeException("Queue is empty");
        return (T) arr[rear];
    }

    public boolean isEmpty() { return size == 0; }
    public boolean isFull()  { return size == arr.length; }
    public int size()        { return size; }
    public int capacity()    { return arr.length; }

    // ─── Resize ───

    private void resize(int newCapacity) {
        Object[] newArr = new Object[newCapacity];

        // Copy elements in order: front → rear (may wrap around)
        for (int i = 0; i < size; i++) {
            newArr[i] = arr[(front + i) % arr.length];
        }

        arr = newArr;
        front = 0;        // reset front to 0 after linearizing
        rear = size - 1;  // rear is last valid index
    }

    // ─── Utility ───

    public boolean contains(T item) {
        for (int i = 0; i < size; i++) {
            int idx = (front + i) % arr.length;
            if (arr[idx].equals(item)) return true;
        }
        return false;
    }

    public void clear() {
        for (int i = 0; i < size; i++) {
            arr[(front + i) % arr.length] = null;
        }
        front = 0;
        rear = -1;
        size = 0;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("Queue[");
        for (int i = 0; i < size; i++) {
            int idx = (front + i) % arr.length;
            sb.append(arr[idx]);
            if (i < size - 1) sb.append(", ");
        }
        sb.append("] (front=").append(front)
          .append(", rear=").append(rear)
          .append(", size=").append(size)
          .append(", cap=").append(arr.length).append(")");
        return sb.toString();
    }
}
```

### The resize operation — the hard part

```
Before resize (wrapped around):
capacity=6, front=4, rear=2, size=5
arr = [D, E, F, _, A, B, C]  ← wait, that's 7 elements in a 6-slot array?
No: arr = [D, E, _, _, A, B]  with front=4, rear=1, size=4
Actually let me show a clearer example:

arr = [_, _, C, D, A, B]  capacity=6, front=4, rear=1, size=4
                                 ↑ A is at index 4 (front)
                     ↑ B is at index 1 (rear, wrapped)

After resize to 12:
newArr = [A, B, C, D, _, _, _, _, _, _, _, _]
front=0, rear=3, size=4

The key insight: we iterate from front to front+size, wrapping with mod,
to copy elements in the correct logical order into a fresh linear array.
```

---

## Circular Queue as a Ring Buffer

The "ring buffer" is the same concept used in real-time systems, networking, and audio processing:

```java
public class RingBuffer<T> {
    private final Object[] buffer;
    private int head = 0;  // read position
    private int tail = 0;  // write position
    private final int mask;  // capacity - 1 (for fast modulo with &)

    public RingBuffer(int capacity) {
        // Capacity must be power of 2 for the & mask trick
        if (Integer.bitCount(capacity) != 1) {
            throw new IllegalArgumentException("Capacity must be power of 2");
        }
        buffer = new Object[capacity];
        mask = capacity - 1;
    }

    public boolean offer(T item) {
        if (tail - head == buffer.length) return false;  // full
        buffer[tail & mask] = item;
        tail++;
        return true;
    }

    @SuppressWarnings("unchecked")
    public T poll() {
        if (tail == head) return null;  // empty
        T item = (T) buffer[head & mask];
        head++;
        return item;
    }

    public int size() { return tail - head; }
    public boolean isEmpty() { return tail == head; }
}
```

**The power of power-of-2 capacity:** `index % capacity` becomes `index & mask` — a single bitwise AND operation instead of a division. This is measurably faster in tight loops.

---

## Using ArrayDeque as a Queue

In practice, you'd use Java's built-in `ArrayDeque`:

```java
import java.util.ArrayDeque;
import java.util.Deque;

Deque<Integer> queue = new ArrayDeque<>();

queue.offer(1);    // enqueue to rear
queue.offer(2);
queue.offer(3);

int front = queue.poll();    // dequeue from front → 1
int peek = queue.peek();     // view front → 2
int size = queue.size();     // 2

System.out.println(queue);   // [2, 3]
```

`ArrayDeque` IS a circular array internally. It resizes by doubling. You get all the benefits without writing any code.

---

## Performance: When to Use What

| Approach | Enqueue | Dequeue | Resize Cost | Best For |
|----------|---------|---------|-------------|----------|
| Linear array | O(1) | O(n)* | N/A | Never (wasteful) |
| Circular fixed | O(1) | O(1) | N/A | Known max size |
| Circular dynamic | O(1) amortized | O(1) amortized | O(n) | General purpose |
| ArrayDeque (built-in) | O(1) amortized | O(1) amortized | O(n) | Production code |
| Linked list queue | O(1) | O(1) | O(1) per insert | Truly unbounded |

*Linear dequeue is O(n) because we shift all elements forward (or waste space).

---

## Key Takeaways

1. **Resize on full** — double the capacity, linearize the circular data
2. **`front = 0` after resize** — this is the whole point of resizing (unwrap the circle)
3. **Shrink at 25% usage** — prevent memory bloat after many dequeues
4. **Power-of-2 capacity** enables `& mask` instead of `% capacity` — micro-optimization
5. **Ring buffer** is the same concept used in high-performance systems
6. **Just use `ArrayDeque`** in production — it does all of this for you

The circular queue teaches you how real systems handle FIFO buffering efficiently.
