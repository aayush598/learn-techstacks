# Deque — Detailed Guide

> Deque (double-ended queue, pronounced "deck") is the most versatile linear data structure. It supports insertion and deletion at both ends in O(1). It can be a stack AND a queue. It's the Swiss Army knife of Java collections.

## Deque Interface vs Implementations

```
Deque<E> (interface)
├── ArrayDeque<E>    — resizable circular array (recommended)
├── LinkedList<E>    — doubly linked list
├── PriorityQueue<E> — DOES NOT implement Deque (common mistake!)
└── ConcurrentLinkedDeque<E> — lock-free concurrent
```

**Always use `ArrayDeque`** unless you have a specific reason not to.

---

## Complete API with ArrayDeque

```java
import java.util.ArrayDeque;
import java.util.Deque;

Deque<String> deque = new ArrayDeque<>();

// ─── Adding Elements ───

deque.addFirst("A");     // add to front, throws IllegalStateException if bounded
deque.addLast("B");      // add to rear, throws IllegalStateException if bounded
deque.offerFirst("C");   // add to front, returns false if bounded
deque.offerLast("D");    // add to rear, returns false if bounded
deque.add("E");          // same as addLast()
deque.offer("F");        // same as offerLast()
deque.push("G");         // same as addFirst() (stack push)

// deque: [G, C, A, B, D, E, F]  ← front is left
//        ↑ push adds here

// ─── Removing Elements ───

String first = deque.removeFirst();  // remove from front, throws if empty
String last  = deque.removeLast();   // remove from rear, throws if empty
String f     = deque.pollFirst();    // remove from front, returns null if empty
String l     = deque.pollLast();     // remove from rear, returns null if empty
String elem  = deque.remove();       // same as removeFirst()
String p     = deque.poll();         // same as pollFirst()
String popped = deque.pop();         // same as removeFirst() (stack pop)

// ─── Examining Elements ───

String peekFirst = deque.peekFirst();  // view front, null if empty
String peekLast  = deque.peekLast();   // view rear, null if empty
String peekF     = deque.peek();       // same as peekFirst()
String top       = deque.element();    // same as peekFirst(), throws if empty

// ─── Utility ───

int size = deque.size();
boolean empty = deque.isEmpty();
boolean hasA = deque.contains("A");     // O(n) search
boolean removed = deque.remove("A");    // remove first occurrence, O(n)
deque.clear();
```

---

## As a Stack (LIFO)

```java
Deque<Integer> stack = new ArrayDeque<>();

// Push → addFirst
stack.push(1);     // [1]
stack.push(2);     // [2, 1]
stack.push(3);     // [3, 2, 1]

// Pop → removeFirst
int top = stack.pop();  // 3, deque: [2, 1]

// Peek → peekFirst
int peek = stack.peek();  // 2

// isEmpty
while (!stack.isEmpty()) {
    System.out.println(stack.pop());
}
// Output: 2, 1
```

---

## As a Queue (FIFO)

```java
Deque<Integer> queue = new ArrayDeque<>();

// Enqueue → addLast
queue.offer(1);     // [1]
queue.offer(2);     // [1, 2]
queue.offer(3);     // [1, 2, 3]

// Dequeue → removeFirst
int front = queue.poll();  // 1, deque: [2, 3]

// Peek → peekFirst
int peek = queue.peek();  // 2

// isEmpty
while (!queue.isEmpty()) {
    System.out.println(queue.poll());
}
// Output: 2, 3
```

**Notice:** Stack and Queue both remove from the front. The difference is where you ADD:
- Stack: `addFirst` (push), remove from front (pop) — LIFO
- Queue: `addLast` (offer), remove from front (poll) — FIFO

---

## ArrayDeque Internals

`ArrayDeque` uses a circular array, just like our manual implementation:

```java
// Simplified internal structure of ArrayDeque
transient Object[] elements;
transient int head;  // index of first element
transient int tail;  // index next available slot (NOT last element!)

// Key constants
static final int MIN_INITIAL_CAPACITY = 8;

// addLast:
elements[tail] = e;
tail = (tail + 1) & (elements.length - 1);  // & mask for power-of-2 mod

// removeFirst:
E result = (E) elements[head];
elements[head] = null;
head = (head + 1) & (elements.length - 1);
```

**Why `tail` points to the next empty slot, not the last element?**
- It simplifies the `isEmpty` check: `head == tail`
- It simplifies the `isFull` check for bounded deques: `(tail + 1) & mask == head`
- The last element is at `(tail - 1) & mask`

---

## Performance

```
ArrayDeque all operations: O(1) amortized
─────────────────────────────────────────
addFirst(E)        O(1) amortized    — resize when full
addLast(E)         O(1) amortized    — resize when full
removeFirst()      O(1) amortized    — shrink when too empty
removeLast()       O(1) amortized    — shrink when too empty
peekFirst()        O(1)              — no resize needed
peekLast()         O(1)              — no resize needed
contains(Object)   O(n)              — linear search
size()             O(1)              — tracked variable
```

LinkedList vs ArrayDeque:

```
                    ArrayDeque    LinkedList
addFirst            O(1)          O(1)
addLast             O(1)          O(1)
removeFirst         O(1)          O(1)
removeLast          O(1)          O(1)*
contains            O(n)          O(n)
Memory per element  ~0 bytes      24 bytes (node + 2 pointers)
Cache performance   Excellent     Poor

* LinkedList.removeLast() is O(1) if you have the node reference,
  but O(n) to find the last node without a tail pointer.
  Java's LinkedList DOES have a tail pointer, so it's O(1).
```

---

## Practical Patterns

### Using Deque for BFS

```java
public void bfs(TreeNode root) {
    Deque<TreeNode> queue = new ArrayDeque<>();
    queue.offer(root);

    while (!queue.isEmpty()) {
        int levelSize = queue.size();
        for (int i = 0; i < levelSize; i++) {
            TreeNode node = queue.poll();
            System.out.print(node.val + " ");

            if (node.left != null)  queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        System.out.println(); // new level
    }
}
```

### Using Deque for DFS

```java
public void dfs(TreeNode root) {
    Deque<TreeNode> stack = new ArrayDeque<>();
    stack.push(root);

    while (!stack.isEmpty()) {
        TreeNode node = stack.pop();
        System.out.println(node.val);

        // Note: push right first, so left is processed first
        if (node.right != null) stack.push(node.right);
        if (node.left != null)  stack.push(node.left);
    }
}
```

### Using Deque for sliding window

```java
public int[] maxSlidingWindow(int[] nums, int k) {
    Deque<Integer> deque = new ArrayDeque<>();  // stores indices
    int[] result = new int[nums.length - k + 1];

    for (int i = 0; i < nums.length; i++) {
        // Remove indices outside window
        while (!deque.isEmpty() && deque.peekFirst() <= i - k) {
            deque.pollFirst();
        }

        // Remove indices of smaller elements (they'll never be max)
        while (!deque.isEmpty() && nums[deque.peekLast()] < nums[i]) {
            deque.pollLast();
        }

        deque.offerLast(i);

        // Window is formed starting at i - k + 1
        if (i >= k - 1) {
            result[i - k + 1] = nums[deque.peekFirst()];
        }
    }

    return result;
}
```

---

## Common Mistakes

```java
// 1. Confusing addFirst with offerFirst
// add* throws exception on failure, offer* returns false
// For unbounded deques (ArrayDeque), they're equivalent

// 2. Using getFirst/getLast when queue might be empty
// Use peekFirst/peekLast instead — they return null
String s = deque.getFirst();  // throws NoSuchElementException if empty!

// 3. Confusing remove(Object) with removeFirst()
// remove(Object) searches and removes first occurrence — O(n)
// removeFirst() removes from front — O(1)

// 4. Using PriorityQueue as a Deque — it doesn't implement Deque
// PriorityQueue implements Queue only (offer/poll/peek)

// 5. Creating a stack from Deque using addLast/removeLast
// This is a valid stack, but push/pop use addFirst/removeFirst
// Mixing them creates confusing code
```

---

## Key Takeaways

1. **`ArrayDeque` is the default choice** — faster than LinkedList, no synchronization overhead
2. **Stack: `push`/`pop`/`peek`** = addFirst/removeFirst/getFirst
3. **Queue: `offer`/`poll`/`peek`** = addLast/removeFirst/getFirst
4. **Internal: circular array** with power-of-2 capacity and `& mask` modulo
5. **All core operations are O(1)** amortized
6. **Prefer `peek`/`poll` over `get`/`remove`** — they don't throw exceptions

`ArrayDeque` is one of the most useful classes in Java. Master its API and you'll reach for it constantly.
