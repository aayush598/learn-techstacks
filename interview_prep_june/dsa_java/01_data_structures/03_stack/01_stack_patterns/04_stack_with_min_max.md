# Stack with Min/Max

> "Design a stack that supports push, pop, top, and retrieving the minimum element in O(1) time." This is a classic interview question that tests your ability to maintain auxiliary state alongside a primary data structure.

## Min Stack — Two Stacks Approach

**Idea:** Maintain a second stack (`minStack`) that tracks the minimum at each level. When we push a value that is ≤ current minimum, we also push it to `minStack`.

```java
public class MinStack {
    private Deque<Integer> stack;
    private Deque<Integer> minStack;

    public MinStack() {
        stack = new ArrayDeque<>();
        minStack = new ArrayDeque<>();
    }

    public void push(int val) {
        stack.push(val);

        // Push to minStack if it's empty or val ≤ current min
        // Use <= so that duplicate minimums are tracked correctly
        if (minStack.isEmpty() || val <= minStack.peek()) {
            minStack.push(val);
        }
    }

    public int pop() {
        int val = stack.pop();

        // If the popped value was the current min, also pop from minStack
        if (val == minStack.peek()) {
            minStack.pop();
        }

        return val;
    }

    public int top() {
        return stack.peek();
    }

    public int getMin() {
        return minStack.peek();
    }
}
```

### Why `<=` and not `<`?

```java
// Consider: push(2), push(2), pop(), getMin()
//
// With <=:
//   push(2): stack=[2], minStack=[2]
//   push(2): stack=[2,2], minStack=[2,2]  ← both 2s tracked
//   pop():   stack=[2], minStack=[2]      ← min popped too
//   getMin() → 2 ✓
//
// With < only:
//   push(2): stack=[2], minStack=[2]
//   push(2): stack=[2,2], minStack=[2]   ← only one 2 tracked
//   pop():   stack=[2], minStack=[]      ← EMPTY! 💥
//   getMin() → exception!
```

### Trace

```
push(5): stack=[5], minStack=[5]
push(3): stack=[5,3], minStack=[5,3]      ← 3 ≤ 5, push to minStack
push(7): stack=[5,3,7], minStack=[5,3]    ← 7 > 3, don't push
push(1): stack=[5,3,7,1], minStack=[5,3,1] ← 1 ≤ 3, push
getMin(): 1 ✓
pop():    stack=[5,3,7], minStack=[5,3]    ← popped 1, removed from minStack
getMin(): 3 ✓
pop():    stack=[5,3], minStack=[5]        ← popped 7, not in minStack, nothing removed
getMin(): 3 ✓
pop():    stack=[5], minStack=[]            ← popped 3, removed from minStack
getMin(): 5 ✓
```

---

## Min Stack — Single Stack with Difference (Clever but Risky)

**Idea:** Store the difference between the current value and the minimum, instead of the value itself.

```java
public class MinStackDiff {
    private Deque<Long> stack;  // use long to avoid integer overflow
    private long min;

    public MinStackDiff() {
        stack = new ArrayDeque<>();
    }

    public void push(int val) {
        if (stack.isEmpty()) {
            stack.push(0L);  // diff = 0 when first element
            min = val;
        } else {
            long diff = (long) val - min;
            stack.push(diff);
            if (diff < 0) {
                min = val;  // new minimum, diff is negative
            }
        }
    }

    public int pop() {
        long diff = stack.pop();
        int val;
        if (diff < 0) {
            // The stored diff was negative → min was the actual value
            val = (int) min;
            min = min - diff;  // restore previous min
        } else {
            val = (int) (diff + min);
        }
        return val;
    }

    public int top() {
        long diff = stack.peek();
        if (diff < 0) return (int) min;
        return (int) (diff + min);
    }

    public int getMin() {
        return (int) min;
    }
}
```

### How the difference encoding works

```
push(5): stack=[], min=5
         diff=0, stack=[0]

push(3): stack=[0], min=5
         diff=3-5=-2 (negative!), min becomes 3
         stack=[0,-2]

push(7): stack=[0,-2], min=3
         diff=7-3=4 (positive), min stays 3
         stack=[0,-2,4]

getMin(): min=3 ✓

pop(): diff=4 (positive) → val=4+3=7 ✓
pop(): diff=-2 (negative) → val=3 (current min), min=3-(-2)=5 ✓
pop(): diff=0 → val=0+5=5 ✓
```

### The overflow risk

```java
// If values can be very large, (long) val - min might overflow even long
// This is why the two-stack approach is generally preferred in interviews
// The difference trick is clever but fragile
// Use it when the interviewer asks for "optimal space"
```

---

## MinStack Using Linked List (Clean Alternative)

Each node stores the value AND the minimum at that point:

```java
public class MinStackLinkedList {
    private class Node {
        int val;
        int min;
        Node next;

        Node(int val, int min, Node next) {
            this.val = val;
            this.min = min;
            this.next = next;
        }
    }

    private Node head;

    public void push(int val) {
        int newMin = (head == null) ? val : Math.min(val, head.min);
        head = new Node(val, newMin, head);
    }

    public int pop() {
        if (head == null) throw new RuntimeException("Stack is empty");
        int val = head.val;
        head = head.next;
        return val;
    }

    public int top() {
        if (head == null) throw new RuntimeException("Stack is empty");
        return head.val;
    }

    public int getMin() {
        if (head == null) throw new RuntimeException("Stack is empty");
        return head.min;
    }
}
```

This is O(1) for everything and avoids the `<=` vs `<` confusion. The trade-off is extra memory per node (one extra int for min).

---

## Stack with getMin AND getMax

Maintain three stacks: main, minStack, and maxStack.

```java
public class MinMaxStack {
    private Deque<Integer> stack;
    private Deque<Integer> minStack;
    private Deque<Integer> maxStack;

    public MinMaxStack() {
        stack = new ArrayDeque<>();
        minStack = new ArrayDeque<>();
        maxStack = new ArrayDeque<>();
    }

    public void push(int val) {
        stack.push(val);

        // Min tracking
        if (minStack.isEmpty() || val <= minStack.peek()) {
            minStack.push(val);
        }

        // Max tracking
        if (maxStack.isEmpty() || val >= maxStack.peek()) {
            maxStack.push(val);
        }
    }

    public int pop() {
        int val = stack.pop();
        if (!minStack.isEmpty() && val == minStack.peek()) minStack.pop();
        if (!maxStack.isEmpty() && val == maxStack.peek()) maxStack.pop();
        return val;
    }

    public int top()    { return stack.peek(); }
    public int getMin() { return minStack.peek(); }
    public int getMax() { return maxStack.peek(); }

    public boolean isEmpty() { return stack.isEmpty(); }
}
```

---

## Space Analysis

| Approach | Space | Extra per push | Notes |
|----------|-------|---------------|-------|
| Two stacks | O(n) | 0 or 1 extra int | Only pushes to minStack when needed |
| Difference | O(n) | 0 extra (encoded) | Clever but overflow risk |
| Linked list | O(n) | 1 extra int + pointer | Always stores min in node |
| Min+Max stacks | O(n) | 0-2 extra ints | Tracks both min and max |

**Amortized space of two-stack approach:** In the best case (sorted input), minStack only has O(1) elements. In the worst case (reverse sorted), it mirrors the main stack.

---

## Practice Problems

Once you master these, try:

1. **Get Min/Max in O(1) with O(1) extra space** — the "impossible" version using bit manipulation (stores encoded value)
2. **Min Stack with operations: push, pop, top, getMin, and getRandom** — add a HashMap with indices
3. **Max Stack (LeetCode 716)** — supports peekMax and popMax in O(log n) or O(1) amortized
4. **Sliding Window Minimum** — combines min stack concept with deque

---

## Key Takeaways

1. **Two-stack approach is the interview gold standard** — simple, correct, O(1) everything
2. **Use `<=` not `<`** when pushing to minStack to handle duplicate minimums
3. **Difference encoding** saves a stack but risks overflow — know it, but prefer two stacks
4. **Linked list with min-per-node** is the cleanest but uses more memory
5. **Max tracking** is identical to min tracking — just flip the comparison
6. **All approaches are O(1)** for push, pop, top, and getMin — that's the whole point

The Min Stack problem is deceptively simple but reveals a lot about how you think about trade-offs. Master it.
