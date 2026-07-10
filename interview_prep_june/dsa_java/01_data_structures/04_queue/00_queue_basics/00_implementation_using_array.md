# Queue Implementation Using Array

> A queue is FIFO (First In, First Out) — like a line at a coffee shop. Everyone waits their turn. Let's implement this with arrays and see why the naive approach fails, then fix it with a circular queue.

## Linear Queue — The Naive Approach

```java
public class LinearQueue<T> {
    private Object[] arr;
    private int front;  // index of first element
    private int rear;   // index of last element
    private int size;

    public LinearQueue(int capacity) {
        arr = new Object[capacity];
        front = 0;
        rear = -1;
        size = 0;
    }

    public void enqueue(T item) {
        if (isFull()) throw new RuntimeException("Queue is full");
        rear++;
        arr[rear] = item;
        size++;
    }

    @SuppressWarnings("unchecked")
    public T dequeue() {
        if (isEmpty()) throw new RuntimeException("Queue is empty");
        T item = (T) arr[front];
        arr[front] = null;  // help GC
        front++;
        size--;
        return item;
    }

    @SuppressWarnings("unchecked")
    public T peek() {
        if (isEmpty()) throw new RuntimeException("Queue is empty");
        return (T) arr[front];
    }

    public boolean isEmpty() { return size == 0; }
    public boolean isFull()  { return size == arr.length; }
    public int size()        { return size; }
}
```

### The fatal flaw

```
Initial:  [_, _, _, _, _]  front=0, rear=-1

enqueue(A): [A, _, _, _, _]  front=0, rear=0
enqueue(B): [A, B, _, _, _]  front=0, rear=1
enqueue(C): [A, B, C, _, _]  front=0, rear=2
dequeue():  [_, B, C, _, _]  front=1, rear=2  → A removed
dequeue():  [_, _, C, _, _]  front=2, rear=2  → B removed
enqueue(D): [_, _, C, D, _]  front=2, rear=3
enqueue(E): [_, _, C, D, E]  front=2, rear=4
enqueue(F): 💥 FULL! But positions 0 and 1 are EMPTY!
```

**We can't reuse the space at the front.** Even though slots 0 and 1 are free, `rear` only moves forward. This is the fundamental problem with linear queues.

---

## Circular Queue — The Fix

The solution: wrap around using modulo arithmetic. When `rear` reaches the end, it wraps to index 0.

```java
public class CircularQueue<T> {
    private Object[] arr;
    private int front;   // index of first element
    private int rear;    // index of last element
    private int size;
    private int capacity;

    public CircularQueue(int capacity) {
        this.capacity = capacity;
        arr = new Object[capacity];
        front = 0;
        rear = -1;
        size = 0;
    }

    public void enqueue(T item) {
        if (isFull()) throw new RuntimeException("Queue is full");
        rear = (rear + 1) % capacity;  // wrap around!
        arr[rear] = item;
        size++;
    }

    @SuppressWarnings("unchecked")
    public T dequeue() {
        if (isEmpty()) throw new RuntimeException("Queue is empty");
        T item = (T) arr[front];
        arr[front] = null;
        front = (front + 1) % capacity;  // wrap around!
        size--;
        return item;
    }

    @SuppressWarnings("unchecked")
    public T peek() {
        if (isEmpty()) throw new RuntimeException("Queue is empty");
        return (T) arr[front];
    }

    public boolean isEmpty() { return size == 0; }
    public boolean isFull()  { return size == capacity; }
    public int size()        { return size; }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < size; i++) {
            int idx = (front + i) % capacity;
            sb.append(arr[idx]);
            if (i < size - 1) sb.append(", ");
        }
        sb.append("]");
        return sb.toString();
    }
}
```

### Visual walkthrough

```
capacity = 5

enqueue(A): [A, _, _, _, _]  front=0, rear=0, size=1
enqueue(B): [A, B, _, _, _]  front=0, rear=1, size=2
enqueue(C): [A, B, C, _, _]  front=0, rear=2, size=3
dequeue():  [_, B, C, _, _]  front=1, rear=2, size=2  → A
dequeue():  [_, _, C, _, _]  front=2, rear=2, size=1  → B
dequeue():  [_, _, _, _, _]  front=3, rear=2, size=0  → C

Now front=3, rear=2. Enqueue wraps around!

enqueue(D): [_, _, _, D, _]  front=3, rear=3, size=1
enqueue(E): [_, _, _, D, E]  front=3, rear=4, size=2
enqueue(F): [F, _, _, D, E]  front=3, rear=0, size=3  ← wrapped!
enqueue(G): [F, G, _, D, E]  front=3, rear=1, size=4
enqueue(H): [F, G, H, D, E]  front=3, rear=2, size=5  → FULL

dequeue(): → D (front goes from 3 to 4→0, wrapped)
dequeue(): → E (front goes from 0 to 1)
dequeue(): → F (front goes from 1 to 2)
```

### The modulo magic

```
rear = (rear + 1) % capacity
     → When rear < capacity-1: just increments
     → When rear == capacity-1: wraps to 0

front = (front + 1) % capacity
     → Same wrapping behavior

isEmpty: size == 0
isFull:  size == capacity
size:    (rear - front + capacity) % capacity  ← alternative to tracking size separately
```

---

## Why `size` tracking is better than `rear - front`

You might see implementations that avoid a `size` variable:

```java
// Alternative: use front and rear only
// empty: rear == front (but so is "one element left after many dequeues" ambiguity)
// So we leave one slot empty:
// isFull: (rear + 1) % capacity == front
// isEmpty: front == rear
// size: (rear - front + capacity) % capacity
```

This wastes one slot and is more confusing. Tracking `size` explicitly is cleaner and uses the full capacity.

---

## Circular Queue: Array vs LinkedList

| Feature | Circular Array | Circular Linked List |
|---------|---------------|---------------------|
| Implementation | Array + front/rear | Single node with next pointer |
| Memory | Contiguous, cache-friendly | Scattered nodes |
| Resize | O(n) to copy | O(1) to insert, just link |
| Space | Wasted if not full | No waste, allocate per element |
| Best for | Known max size | Unknown/dynamic size |

The circular array is almost always preferred in practice for queue implementations due to cache locality.

---

## Key Takeaways

1. **Linear queues waste space** — can't reuse dequeued slots
2. **Circular queues fix this** with modulo arithmetic: `(index + 1) % capacity`
3. **`isEmpty: size == 0`** and **`isFull: size == capacity`** — the cleanest conditions
4. **Always track size explicitly** — the `rear - front` trick wastes a slot
5. **enqueue wraps `rear`**, dequeue wraps `front` — they move independently
6. **Array beats linked list** for circular queues in most cases (cache performance)

Next: a full circular queue with dynamic resizing.
