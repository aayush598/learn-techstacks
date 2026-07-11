# Stack Using Queues

Implement a LIFO stack using only FIFO queues. Three distinct approaches with different trade-offs.

---

## Approach 1: Push O(n) / Pop O(1)

**Idea:** When pushing, rotate the queue so the newest element is always at the front.

```java
class StackUsingQueues {
    private Queue<Integer> queue = new LinkedList<>();

    // Push: O(n) — dequeue and re-enqueue all existing elements
    public void push(int x) {
        queue.offer(x);
        int size = queue.size();
        for (int i = 0; i < size - 1; i++) {
            queue.offer(queue.poll());
        }
    }

    // Pop: O(1) — front of queue is the top of stack
    public int pop() {
        return queue.poll();
    }

    public int top() {
        return queue.peek();
    }

    public boolean empty() {
        return queue.isEmpty();
    }
}
```

**Walkthrough of push(1), push(2), push(3):**
```
push(1): [1]
push(2): [2, 1]          ← rotate: dequeue 1, enqueue back
push(3): [3, 2, 1]       ← rotate: dequeue 2,1, enqueue back
pop():   returns 3, queue = [2, 1]
pop():   returns 2, queue = [1]
```

**Trade-off:** Push is expensive because every insert requires rotating all existing elements.

---

## Approach 2: Push O(1) / Pop O(n) (Two Queues)

**Idea:** Push directly to an input queue. On pop, transfer all but the last element to a second queue.

```java
class StackUsingQueues {
    private Queue<Integer> q1 = new LinkedList<>();
    private Queue<Integer> q2 = new LinkedList<>();

    // Push: O(1) — just enqueue to q1
    public void push(int x) {
        q1.offer(x);
    }

    // Pop: O(n) — move all but last to q2, dequeue last from q1
    public int pop() {
        while (q1.size() > 1) {
            q2.offer(q1.poll());
        }
        int top = q1.poll();
        // Swap q1 and q2
        Queue<Integer> temp = q1;
        q1 = q2;
        q2 = temp;
        return top;
    }

    public int top() {
        while (q1.size() > 1) {
            q2.offer(q1.poll());
        }
        int top = q1.poll();
        q2.offer(top);
        Queue<Integer> temp = q1;
        q1 = q2;
        q2 = temp;
        return top;
    }

    public boolean empty() {
        return q1.isEmpty();
    }
}
```

**Walkthrough:**
```
push(1): q1=[1], q2=[]
push(2): q1=[1,2], q2=[]
push(3): q1=[1,2,3], q2=[]
pop():
  Move 1→q2, 2→q2: q1=[3], q2=[1,2]
  Poll 3 from q1 → return 3
  Swap: q1=[1,2], q2=[]
```

---

## Approach 3: Single Queue (Push O(n))

**Idea:** Use a single queue. After enqueuing the new element, rotate (size-1) elements to the back.

```java
class StackUsingQueues {
    private Queue<Integer> queue = new LinkedList<>();

    public void push(int x) {
        queue.offer(x);
        int size = queue.size();
        // Rotate: move previous elements behind the new one
        for (int i = 1; i < size; i++) {
            queue.offer(queue.poll());
        }
    }

    public int pop() {
        return queue.poll();
    }

    public int top() {
        return queue.peek();
    }

    public boolean empty() {
        return queue.isEmpty();
    }
}
```

**This is the cleanest single-queue solution.** The rotation after each push ensures the most recently pushed element is always at the front.

---

## Comparison Table

| Approach | Push    | Pop     | Queues Used | When to Use            |
|----------|---------|---------|-------------|------------------------|
| 1        | O(n)    | O(1)    | 1           | Pop-heavy workload     |
| 2        | O(1)    | O(n)    | 2           | Push-heavy workload    |
| 3        | O(n)    | O(1)    | 1           | Cleanest implementation|

---

## Follow-up: Min Stack Using Queues

```java
class MinStack {
    private Queue<int[]> queue = new LinkedList<>(); // [value, currentMin]

    public void push(int x) {
        int currentMin = queue.isEmpty() ? x : Math.min(x, queue.peek()[1]);
        queue.offer(new int[]{x, currentMin});
        int size = queue.size();
        for (int i = 1; i < size; i++) {
            queue.offer(queue.poll());
        }
    }

    public int pop() {
        return queue.poll()[0];
    }

    public int getMin() {
        return queue.peek()[1];
    }
}
```

---

## Interview Tips

- **Clarify first:** Ask if you need `push`, `pop`, `top`, or `getMin`.
- **Approach 3 is usually preferred** for interviews — clean code, single queue, O(n) push is acceptable since it's a conceptual question.
- **Mention trade-offs** explicitly: "Approach 1 has O(1) pop but O(n) push, while Approach 2 is the reverse."
- **Edge cases:** Empty stack pop, push after all pops, single element stack.
