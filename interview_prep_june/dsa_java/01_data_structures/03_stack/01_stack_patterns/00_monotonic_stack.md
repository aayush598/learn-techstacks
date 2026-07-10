# Monotonic Stack

> A monotonic stack is a stack where elements are always in sorted order (either increasing or decreasing). It's the single most powerful pattern for solving "next greater/smaller" type problems. If you master this one pattern, you unlock a dozen classic problems.

## The Core Idea

A **monotonic decreasing stack** maintains elements from bottom to top in non-increasing order. When a new element violates this order, we pop elements until the order is restored.

Why? Because any element that gets popped will never be needed again — the new element is its answer.

---

## Monotonic Decreasing Stack (Finding Next Greater)

```java
// For each element, find the next element that is GREATER than it
// Stack stores indices, maintains DECREASING values

public int[] nextGreaterElements(int[] arr) {
    int n = arr.length;
    int[] result = new int[n];
    Arrays.fill(result, -1);

    Deque<Integer> stack = new ArrayDeque<>();  // stores indices

    for (int i = 0; i < n; i++) {
        // While current element is greater than stack's top element
        while (!stack.isEmpty() && arr[stack.peek()] < arr[i]) {
            int idx = stack.pop();
            result[idx] = arr[i];  // arr[i] is the NGE for arr[idx]
        }
        stack.push(i);
    }

    return result;
}
```

### Step-by-Step Trace

```
arr = [2, 1, 2, 4, 3]

i=0: stack=[], push 0          stack=[0]    result=[-1,-1,-1,-1,-1]
i=1: arr[0]=2 > arr[1]=1? No   push 1       stack=[0,1]  result unchanged
i=2: arr[1]=1 < arr[2]=2? Yes! pop 1, result[1]=2
     arr[0]=2 < arr[2]=2? No   push 2       stack=[0,2]  result=[-1,2,-1,-1,-1]
i=3: arr[2]=2 < arr[3]=4? Yes! pop 2, result[2]=4
     arr[0]=2 < arr[3]=4? Yes! pop 0, result[0]=4
     stack empty, push 3       stack=[3]    result=[4,2,4,-1,-1]
i=4: arr[3]=4 > arr[4]=3? No  push 4       stack=[3,4]  result unchanged

Final: [4, 2, 4, -1, -1]
```

**Why does popping work?** When we pop index 1 (value 1) at i=2 (value 2), we know that 2 is the first element to the right of 1 that's greater. We can never find a "better" answer for index 1 later — the stack guarantees we process elements in order.

---

## Monotonic Increasing Stack (Finding Next Smaller)

```java
// For each element, find the next element that is SMALLER than it
// Stack stores indices, maintains INCREASING values

public int[] nextSmallerElements(int[] arr) {
    int n = arr.length;
    int[] result = new int[n];
    Arrays.fill(result, -1);

    Deque<Integer> stack = new ArrayDeque<>();

    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && arr[stack.peek()] > arr[i]) {
            int idx = stack.pop();
            result[idx] = arr[i];
        }
        stack.push(i);
    }

    return result;
}
```

Same logic, flipped condition. Decreasing stack finds next greater; increasing stack finds next smaller.

---

## The Template

Here's the mental model to internalize:

```
for each element in array:
    while (stack not empty AND current element violates order):
        process the popped element (this is where the answer is computed)
    push current index to stack
```

**What determines the "order"?**

| Stack Order | Condition in While | Finds |
|------------|-------------------|-------|
| Decreasing (top is smallest) | `arr[stack.peek()] < arr[i]` | Next Greater Element |
| Increasing (top is largest) | `arr[stack.peek()] > arr[i]` | Next Smaller Element |

---

## When to Use Monotonic Stack

Use it when you see these keywords in a problem:

1. **"Next greater/smaller element"** — classic
2. **"Previous greater/smaller element"** — reverse the iteration
3. **"For each element, find the first element to the right/left that..."** — scanning pattern
4. **Problems involving rectangles in histograms** — area computation needs boundary detection
5. **"Span" problems** — like stock span (consecutive smaller-or-equal before)
6. **"Trapping rain water"** — need to know boundaries

**Red flag pattern:** If you're looking for the "nearest X in some direction," monotonic stack is probably the answer.

---

## Storing Indices vs Values

Always prefer storing **indices** in the stack, not values. Why?

```java
// Indices give you position information for free
// You can compute distances, ranges, widths

// Wrong: storing values
Deque<Integer> stack = new ArrayDeque<>(); // stores arr[i] values
// stack.peek() gives you the value, but NOT where it was

// Right: storing indices
Deque<Integer> stack = new ArrayDeque<>(); // stores indices
// stack.peek() gives index i, then arr[i] is the value
// AND you can compute: i - stack.peek() (distance between elements)
```

This matters enormously for problems like "largest rectangle in histogram" where you need the **width** (distance between indices), not just the values.

---

## Template with Boundary Handling

For problems where you need to process remaining elements after the loop:

```java
// Option 1: Iterate 2*n for circular problems
for (int i = 0; i < 2 * n; i++) {
    int val = arr[i % n];
    while (!stack.isEmpty() && arr[stack.peek()] < val) {
        result[stack.pop() % n] = val;
    }
    if (i < n) stack.push(i);
}

// Option 2: Process remaining stack after loop
for (int i = 0; i < n; i++) {
    while (!stack.isEmpty() && arr[stack.peek()] < arr[i]) {
        result[stack.pop()] = arr[i];
    }
    stack.push(i);
}
// Remaining elements in stack have no greater element → result stays -1
```

---

## Practice Progression

Start with these, in order:

1. **Next Greater Element I** — direct application
2. **Next Greater Element II** — circular array variant
3. **Daily Temperatures** — "how many days until warmer"
4. **Stock Span Problem** — consecutive smaller-or-equal before
5. **Largest Rectangle in Histogram** — the boss fight
6. **Trapping Rain Water** — another boss fight

Each builds on the same pattern. Master the template, and these problems become mechanical.

---

## Common Pitfalls

```java
// 1. Using values instead of indices
stack.push(arr[i]);  // WRONG — lose position information

// 2. Wrong comparison direction
while (!stack.isEmpty() && arr[stack.peek()] > arr[i])  // finding NGE? WRONG direction
// Should be: arr[stack.peek()] < arr[i] for NGE

// 3. Forgetting to handle remaining elements
// After the loop, stack may contain elements with no answer
// Make sure you handle them (or know they default to -1)

// 4. Not using modulo for circular problems
for (int i = 0; i < 2 * n; i++) {
    // arr[i] would be out of bounds! Use arr[i % n]
}
```

---

## Key Takeaways

1. **Decreasing stack → Next Greater Element**
2. **Increasing stack → Next Smaller Element**
3. **Always store indices**, not values
4. **The while loop is the magic** — it processes all elements that the current element "resolves"
5. **Amortized O(n)** — each element is pushed and popped at most once
6. **Recognize the pattern**: "find the first X in some direction" = monotonic stack

This is one of the highest-ROI patterns in DSA. Invest the time to internalize it.
