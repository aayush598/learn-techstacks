# Queue Using Stacks

Implement a FIFO queue using only LIFO stacks. The key insight: **two stacks can reverse order**, turning LIFO into FIFO.

---

## Approach: Amortized O(1) (Two Stacks)

**Idea:**
- `inputStack`: receives all pushes.
- `outputStack`: provides all pops/peeks.
- When `outputStack` is empty, dump all elements from `inputStack` (reverses order → FIFO).

```java
class MyQueue {
    private Deque<Integer> inputStack;
    private Deque<Integer> outputStack;

    public MyQueue() {
        inputStack = new ArrayDeque<>();
        outputStack = new ArrayDeque<>();
    }

    // O(1) — just push to input
    public void push(int x) {
        inputStack.push(x);
    }

    // Amortized O(1) — transfer only when output is empty
    public int pop() {
        if (outputStack.isEmpty()) {
            transferInputToOutput();
        }
        return outputStack.pop();
    }

    // Amortized O(1)
    public int peek() {
        if (outputStack.isEmpty()) {
            transferInputToOutput();
        }
        return outputStack.peek();
    }

    public boolean empty() {
        return inputStack.isEmpty() && outputStack.isEmpty();
    }

    private void transferInputToOutput() {
        while (!inputStack.isEmpty()) {
            outputStack.push(inputStack.pop());
        }
    }
}
```

---

## Walkthrough

```
push(1): input=[1], output=[]
push(2): input=[1,2], output=[]
push(3): input=[1,2,3], output=[]
pop():
  output empty → transfer:
    pop 3 from input, push to output
    pop 2 from input, push to output
    pop 1 from input, push to output
  input=[], output=[3,2,1]  (top is 1 — FIFO order!)
  pop from output → return 1 ✓

push(4): input=[4], output=[3,2]
pop():  output not empty → pop 2 ✓  (no transfer needed)
pop():  output not empty → pop 3 ✓
pop():  output empty → transfer input[4] to output → pop 4 ✓
```

**Key insight:** Each element is moved at most twice (push to input, dump to output). So across n operations, total work for transfers is O(n), giving amortized O(1) per operation.

---

## Amortized Analysis (Aggregate Method)

| Operation | Total work over n operations |
|-----------|------------------------------|
| `push`    | n × O(1) = O(n)             |
| `transfer`| Each element transferred at most once → O(n) total |
| `pop`     | n × O(1) + O(n) transfers = O(n) |
| **Per operation** | **O(1) amortized** |

---

## Alternative: Lazy Transfer Variant

```java
class MyQueue {
    private Deque<Integer> stack1 = new ArrayDeque<>();
    private Deque<Integer> stack2 = new ArrayDeque<>();
    private int front; // cache the front element

    public void push(int x) {
        if (stack1.isEmpty()) {
            front = x;
        }
        stack1.push(x);
    }

    public int pop() {
        if (stack2.isEmpty()) {
            while (!stack1.isEmpty()) {
                stack2.push(stack1.pop());
            }
        }
        return stack2.pop();
    }

    public int peek() {
        if (!stack2.isEmpty()) return stack2.peek();
        return front;
    }

    public boolean empty() {
        return stack1.isEmpty() && stack2.isEmpty();
    }
}
```

**Note:** `front` is updated whenever `stack1` was empty before a push, guaranteeing it always holds the oldest element.

---

## Comparison

| Approach          | Push    | Pop     | Peek    | Space |
|-------------------|---------|---------|---------|-------|
| Lazy transfer     | O(1)    | Amort. O(1) | Amort. O(1) | 2n  |
| Eager transfer    | O(1)    | Amort. O(1) | Amort. O(1) | 2n  |

Both approaches are equivalent in complexity. The lazy variant is cleaner in practice.

---

## Interview Tips

- **Start with the two-stack approach** — it's the standard answer.
- **Explain amortized O(1)** clearly: "Each element is pushed and popped at most twice, so total work across n operations is O(n)."
- **Don't use 3 stacks** — it's over-engineering for this problem.
- **Common follow-up:** "What if we need O(1) worst-case for both?" → Answer: Not possible with standard stacks alone.
