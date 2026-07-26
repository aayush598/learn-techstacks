# Queue and Deque Fundamentals

## What is a Queue?

A queue is a **First-In-First-Out (FIFO)** data structure. Think of it like a line at a store — first person in line gets served first.

```
Queue Operations Visual:

  ENQUEUE (add to back)          DEQUEUE (remove from front)

  ┌─────┬─────┬─────┐           ┌─────┬─────┬─────┐
  │  A  │  B  │  C  │  → out    │  B  │  C  │     │
  └─────┴─────┴─────┘           └─────┴─────┴─────┘
  ↑                             ↑
  front                        front
  (first in)                   (A served first)

  FIFO: A was first in → A is first out
```

## What is a Deque?

A deque (double-ended queue) supports O(1) operations at **both** ends.

```
Deque Operations:

  append(3)       appendleft(1)      pop()         popleft()
  ─────────→      ←───────────       ─────────→    ←───────────

  [A, B] → [A, B, 3]    [1, A, B]    [A, B, 3] → [A, B]    [1, A, B] → [A, B]
                 ↑            ↑                                  ↑
              add to       add to                            remove from
               back         front                             front
```

## Queue Using collections.deque - O(1) for all operations
```python
from collections import deque

class Queue:
    """
    FIFO Queue implementation using collections.deque.

    deque provides O(1) append (right) and popleft (left),
    which are exactly the operations a queue needs.

    Visual:
      enqueue(1) → [1]
      enqueue(2) → [1, 2]
      enqueue(3) → [1, 2, 3]
                   ↑       ↑
                 front    rear
      dequeue()  → returns 1, queue becomes [2, 3]
      peek()     → returns 2 (front, no removal)
    """
    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        """Add item to the back of the queue. O(1)"""
        self.items.append(item)

    def dequeue(self):
        """Remove and return item from the front. O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items.popleft()

    def peek(self):
        """Return front item without removing. O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(list(self.items))
```

## Queue Using Two Stacks - Amortized O(1)

**Key Insight**: Two LIFO stacks can simulate FIFO by reversing the order.

```
The Trick:
  stack_in:  receives new elements (like enqueue)
  stack_out: serves elements (like dequeue)

  When stack_out is empty, transfer ALL elements from stack_in.
  This reversal makes the oldest element end up on top of stack_out.

Visual — Enqueue 1, 2, 3 then Dequeue:

  Step 1: enqueue(1)          Step 2: enqueue(2)          Step 3: enqueue(3)
  stack_in: [1]               stack_in: [1, 2]            stack_in: [1, 2, 3]
  stack_out: []               stack_out: []                stack_out: []

  Step 4: dequeue()
  stack_out is empty → transfer all from stack_in:

  TRANSFER: pop stack_in → push stack_out (reverses order!)
  ┌─────────┐          ┌─────────┐
  │ stack_in│  ──────→ │stack_out│
  │  [1,2,3]│  pop 3   │  [3]    │
  │  [1,2]  │  pop 2   │  [3,2]  │
  │  [1]    │  pop 1   │  [3,2,1]│
  └─────────┘          └─────────┘

  Now dequeue from stack_out: returns 1 (the oldest!)
  stack_out: [3, 2]     ← next dequeue returns 2

  Amortized O(1): each element is transferred at most once.
```

```python
class QueueTwoStacks:
    """
    Queue using two stacks with amortized O(1) operations.

    stack_in  = write buffer (enqueue goes here)
    stack_out = read buffer (dequeue comes from here)

    Transfer happens only when stack_out is empty AND we need to dequeue.
    Each element moves at most once → amortized O(1).
    """
    def __init__(self):
        self.stack_in = []    # Enqueue buffer
        self.stack_out = []   # Dequeue buffer

    def enqueue(self, item):
        """Always push to stack_in. O(1)"""
        self.stack_in.append(item)

    def dequeue(self):
        """Pop from stack_out (transferring from stack_in if needed)."""
        if self.stack_out:
            return self.stack_out.pop()

        if not self.stack_in:
            raise IndexError("Queue is empty")

        # Transfer: reverse stack_in into stack_out
        while self.stack_in:
            self.stack_out.append(self.stack_in.pop())

        return self.stack_out.pop()

    def peek(self):
        """Same transfer logic as dequeue, but don't remove."""
        if self.stack_out:
            return self.stack_out[-1]

        if not self.stack_in:
            raise IndexError("Queue is empty")

        while self.stack_in:
            self.stack_out.append(self.stack_in.pop())

        return self.stack_out[-1]

    def is_empty(self):
        return not self.stack_in and not self.stack_out
```

## Circular Queue - O(1)

**Why Circular?** A regular queue wastes space — once elements are dequeued, those array slots are never reused. A circular queue wraps around using modulo arithmetic.

```
Regular Queue (wastes space):
  After enqueue(1,2,3) and dequeue(1,2):
  [_, _, _, 3, _, _, _, _]  ← slots 0,1 wasted forever!

Circular Queue (reuses space):
  Capacity = 4
  After enqueue(A,B,C,D) and dequeue(A,B):
  Index:   0    1    2    3
         ┌────┬────┬────┬────┐
         │ C  │ D  │    │    │
         └────┴────┴────┴────┘
           ↑rear  ↑front
           rear=0 front=2

  enqueue(E): rear = (0+1) % 4 = 1
         ┌────┬────┬────┬────┐
         │ C  │ D  │ E  │    │
         └────┴────┴────┴────┘
           ↑front     ↑rear

  The modulo wraps rear back to index 0!
```

```python
class CircularQueue:
    """
    Fixed-size circular queue using an array with modulo wrapping.

    front: index of the first element
    rear:  index of the last element
    size:  current number of elements

    Key formula:
      rear  = (rear + 1) % capacity   — move rear forward (wrap around)
      front = (front + 1) % capacity  — move front forward (wrap around)
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def enqueue(self, item):
        if self.is_full():
            raise IndexError("Queue is full")

        self.rear = (self.rear + 1) % self.capacity  # Wrap around!
        self.queue[self.rear] = item
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")

        item = self.queue[self.front]
        self.queue[self.front] = None       # Help GC
        self.front = (self.front + 1) % self.capacity  # Wrap around!
        self.size -= 1
        return item

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.queue[self.front]

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity
```

## Priority Queue Using heapq - O(log n) for push/pop

**Difference from regular queue**: Elements are served by **priority**, not arrival order. Highest priority = served first.

```
Priority Queue vs Regular Queue:

  Regular Queue (FIFO):
    push(low, 1) → [low]
    push(high, 10) → [low, high]
    push(med, 5) → [low, high, med]
    pop() → low (first in, regardless of priority)

  Priority Queue:
    push(low, 1) → heap: [(1, low)]
    push(high, 10) → heap: [(1, low), (10, high)]
    push(med, 5) → heap: [(1, low), (10, high), (5, med)]
    pop() → high (highest priority comes out first!)

  Internally stored as a min-heap (smallest at top).
  We negate priorities to make "highest number = highest priority."
```

```python
import heapq

class PriorityQueue:
    """
    Priority Queue using Python's heapq (min-heap).

    heapq gives us a MIN-heap: smallest value on top.
    To make highest priority = highest number, we negate the priority.

    Tuple structure: (-priority, index, item)
      -priority: so higher priority numbers come out first
      index:     for FIFO tie-breaking (stability)
      item:      the actual data
    """
    def __init__(self):
        self.heap = []
        self.index = 0   # For FIFO tie-breaking

    def push(self, item, priority):
        """Push item with given priority. O(log n)"""
        heapq.heappush(self.heap, (-priority, self.index, item))
        self.index += 1

    def pop(self):
        """Remove and return highest-priority item. O(log n)"""
        if not self.heap:
            raise IndexError("Priority queue is empty")
        return heapq.heappop(self.heap)[2]  # Return just the item

    def peek(self):
        """View highest-priority item. O(1)"""
        if not self.heap:
            raise IndexError("Priority queue is empty")
        return self.heap[0][2]

    def is_empty(self):
        return len(self.heap) == 0


# Simpler version without tie-breaking:
class SimplePriorityQueue:
    """Simpler PQ when FIFO tie-breaking isn't needed."""
    def __init__(self):
        self.heap = []

    def push(self, item, priority):
        heapq.heappush(self.heap, (priority, item))

    def pop(self):
        if not self.heap:
            raise IndexError("Priority queue is empty")
        return heapq.heappop(self.heap)[1]

    def peek(self):
        if not self.heap:
            raise IndexError("Priority queue is empty")
        return self.heap[0][1]
```

## Deque Operations and When to Use - O(1)
```python
from collections import deque

# Deque supports O(1) operations at both ends
dq = deque()

# Add elements
dq.append(1)      # Add to right - O(1)
dq.appendleft(2)  # Add to left - O(1)

# Remove elements
dq.pop()          # Remove from right - O(1)
dq.popleft()      # Remove from left - O(1)

# When to use deque vs list:
# - deque: When you need to add/remove from both ends
# - list: When you mainly access by index
```

## Sliding Window Maximum Using Deque - O(n)

**Problem**: Given an array and window size k, find the maximum in each window position.

**Strategy**: Use a **monotonic decreasing deque** — the front always holds the max. Remove elements that are smaller (they can never be the max while the larger element exists in the window).

```
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

Window 1: [1, 3,-1]       → max = 3
Window 2: [3,-1,-3]       → max = 3
Window 3: [-1,-3, 5]      → max = 5
Window 4: [-3, 5, 3]      → max = 5
Window 5: [5, 3, 6]       → max = 6
Window 6: [3, 6, 7]       → max = 7

Result: [3, 3, 5, 5, 6, 7]

Deque state at each step (stores indices, values shown):
  i=0(1): dq=[0]        → vals:[1]
  i=1(3): 3>1, pop 0    → dq=[1]        → vals:[3]
  i=2(-1): push 2       → dq=[1,2]      → vals:[3,-1]
  Window complete → max = nums[dq[0]] = 3

  i=3(-3): push 3       → dq=[1,2,3]    → vals:[3,-1,-3]
  i=0 expired? 0<3-3+1=1? Yes, pop left → dq=[2,3] → vals:[-1,-3]
  Window complete → max = nums[2] = -1? No — wait, 1 is still in window!
  Actually dq[0]=1 (val=3), 1 >= 3-3+1=1 → still valid
  max = nums[dq[0]] = 3 ✓

  i=4(5): 5>-3, pop 3; 5>-1, pop 2; 5>3, pop 1 → dq=[4] → vals:[5]
  Window complete → max = 5 ✓

  i=5(3): push 5       → dq=[4,5] → vals:[5,3]
  i=3 expired? 4<5-3+1=3? No
  max = nums[4] = 5 ✓

  i=6(6): 6>3, pop 5; 6>5, pop 4 → dq=[6] → vals:[6]
  max = 6 ✓

  i=7(7): 7>6, pop 6 → dq=[7] → vals:[7]
  max = 7 ✓
```

```python
from collections import deque

def max_sliding_window(nums, k):
    """
    Find maximum in every sliding window of size k.

    Monotonic decreasing deque:
    - Front = index of current window's maximum
    - Back = candidates for future maximums (in decreasing order)

    Why it works:
    1. Remove from back: smaller elements can NEVER be max while larger
       ones are in the window.
    2. Remove from front: elements that have slid out of the window.
    3. Front of deque is always the max of the current window.
    """
    result = []
    dq = deque()  # Stores INDICES (not values!)

    for i in range(len(nums)):
        # Step 1: Remove elements that fell out of the window (left side)
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Step 2: Remove smaller elements from back (they're useless)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        # Step 3: Add current element
        dq.append(i)

        # Step 4: Once window is complete, front is the max
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

# Example walkthrough:
# nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
# Result: max_sliding_window(nums, k) = [3, 3, 5, 5, 6, 7]
```

## Sliding Window Minimum Using Deque - O(n)

**Strategy**: Same as max, but with an **increasing** deque — front holds the minimum.

```
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

Window 1: [1, 3,-1]  → min = -1
Window 2: [3,-1,-3]  → min = -3
Window 3: [-1,-3, 5] → min = -3
Window 4: [-3, 5, 3] → min = -3
Window 5: [5, 3, 6]  → min =  3
Window 6: [3, 6, 7]  → min =  3

Result: [-1, -3, -3, -3, 3, 3]

Difference from max: condition is `nums[dq[-1]] > nums[i]`
(pop from back when current is SMALLER, keeping deque increasing)
```

```python
from collections import deque

def min_sliding_window(nums, k):
    """
    Find minimum in every sliding window of size k.

    Monotonic INCREASING deque:
    - Front = index of current window's minimum
    - Back = candidates (in increasing order)

    Only difference from max: pop when nums[dq[-1]] > nums[i]
    (smaller elements dominate, so we remove larger ones)
    """
    result = []
    dq = deque()  # Stores indices of potential minimums

    for i in range(len(nums)):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove LARGER elements from back (we want smallest at front)
        while dq and nums[dq[-1]] > nums[i]:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

# Example walkthrough:
# nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
# Result: min_sliding_window(nums, k) = [-1, -3, -3, -3, 3, 3]
```

## First Unique Character in a Stream - O(n) per character

**Problem**: As characters arrive one by one, always return the first character (from the stream) that has appeared only once.

**Strategy**: Queue + Counter. Queue holds candidates (chars seen once). When a duplicate arrives, invalidate the front of the queue.

```
Stream: a → b → a → b → c

Step 1: add 'a'   queue: [a]     count: {a:1}   → first unique: 'a'
Step 2: add 'b'   queue: [a,b]   count: {a:1,b:1} → first unique: 'a'
Step 3: add 'a'   count: {a:2,b:1} → 'a' is duplicate, pop from queue
                   queue: [b]     → first unique: 'b'
Step 4: add 'b'   count: {a:2,b:2} → 'b' is duplicate, pop from queue
                   queue: []      → first unique: '#'
Step 5: add 'c'   queue: [c]     count: {a:2,b:2,c:1} → first unique: 'c'
```

```python
from collections import deque, Counter

class StreamChecker:
    """
    Track the first unique character in a character stream.

    queue: holds characters that have appeared exactly once (in order)
    count: tracks frequency of each character

    When adding a char:
    1. Push to queue and increment count
    2. While front of queue has count > 1, pop it (it's been invalidated)
    3. Front of queue (if any) is the first unique character
    """
    def __init__(self):
        self.queue = deque()
        self.count = Counter()

    def add_char(self, char):
        self.queue.append(char)
        self.count[char] += 1

        # Remove all invalid characters from front
        while self.queue and self.count[self.queue[0]] > 1:
            self.queue.popleft()

        return self.queue[0] if self.queue else '#'

# Usage:
sc = StreamChecker()
print(sc.add_char('a'))  # 'a'  — queue: [a]
print(sc.add_char('b'))  # 'a'  — queue: [a, b]
print(sc.add_char('a'))  # 'b'  — queue: [b]  (a invalidated)
print(sc.add_char('b'))  # '#'  — queue: []   (b invalidated)
print(sc.add_char('c'))  # 'c'  — queue: [c]
```

## Number of Visible People in a Queue - O(n)

**Problem**: People stand in a line. Person `i` can see person `j` (j>i) if all people between them are shorter than both. Count how many people each person can see.

**Strategy**: Monotonic **decreasing** stack. When a taller person arrives, all shorter people on the stack can see them (and only them to their right).

```
heights = [10, 6, 8, 5, 11, 9]

Person 0 (h=10): sees 6, 8, 5 (all shorter) and 11 (taller, blocks) → 3
Person 1 (h=6):  sees 8 (taller, blocks) → 1
Person 2 (h=8):  sees 5 (shorter) and 11 (taller, blocks) → 2
Person 3 (h=5):  sees 11 (taller, blocks) → 1
Person 4 (h=11): sees 9 (shorter) → 1
Person 5 (h=9):  nobody to the right → 0

Result: [3, 1, 2, 1, 1, 0]

Stack evolution:
  i=0(10): stack=[]        → push 0        stack: [0]
  i=1(6):  6<10            → push 1        stack: [0,1]
  i=2(8):  8>6, pop 1→+1   → push 2        stack: [0,2]
  i=3(5):  5<8             → push 3        stack: [0,2,3]
  i=4(11): 11>5, pop 3→+1  → result[3]+=1
           11>8, pop 2→+1  → result[2]+=1
           11>10, pop 0→+1 → result[0]+=1
           stack empty, push 4              stack: [4]
  i=5(9):  9<11, push 5    → result[4]+=1  stack: [4,5]
  Result: [3, 1, 2, 1, 1, 0] ✓
```

```python
def can_see_persons_count(heights):
    """
    Count how many people each person can see to their right.

    Key insight:
    - When a taller person arrives, ALL shorter people on the stack
      can see them (+1 each). The taller person "blocks" the view.
    - When the current person is shorter than stack top, they are
      visible to stack top (+1 to stack top's count).
    """
    n = len(heights)
    result = [0] * n
    stack = []

    for i in range(n):
        # Current person is taller — all shorter people can see them
        while stack and heights[stack[-1]] < heights[i]:
            result[stack.pop()] += 1

        # Current person is visible to the person still on stack top
        if stack:
            result[stack[-1]] += 1

        stack.append(i)

    return result

# Result: [3, 1, 2, 1, 1, 0]
```

## Complete Example Usage
```python
# Queue operations
queue = Queue()
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
print(f"Queue: {queue}")            # [1, 2, 3]
print(f"Dequeue: {queue.dequeue()}")  # 1
print(f"Peek: {queue.peek()}")        # 2

# Priority Queue
pq = PriorityQueue()
pq.push("low priority task", 1)
pq.push("high priority task", 10)
pq.push("medium priority task", 5)
print(f"Pop: {pq.pop()}")  # high priority task

# Sliding Window Maximum
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(f"Max Sliding Window: {max_sliding_window(nums, k)}")  # [3, 3, 5, 5, 6, 7]

# Sliding Window Minimum
print(f"Min Sliding Window: {min_sliding_window(nums, k)}")  # [-1, -3, -3, -3, 3, 3]

# Stream Checker
sc = StreamChecker()
for char in "aabc":
    print(f"Add {char}: {sc.add_char(char)}")
```

---

## Queue vs Deque vs Priority Queue

| Feature | Queue | Deque | Priority Queue |
|---------|-------|-------|----------------|
| Add to back | O(1) | O(1) | O(log n) |
| Add to front | O(n) | O(1) | N/A |
| Remove from front | O(1) | O(1) | O(log n) |
| Remove from back | O(n) | O(1) | O(log n) |
| Peek | O(1) | O(1) | O(1) |
| Use case | FIFO | Both ends | Priority-based |
| Python | `deque` | `deque` | `heapq` |

### When to Use What — Decision Guide

```
"Do I need FIFO order?"
├─ YES → Use Queue (deque with append/popleft)
│
├─ "Do I need to add/remove from BOTH ends?"
│   └─ YES → Use Deque
│
├─ "Do I need elements served by PRIORITY?"
│   └─ YES → Use Priority Queue (heapq)
│
└─ "Do I need a sliding window of max/min?"
    └─ YES → Use Monotonic Deque

Common Patterns:
┌──────────────────────────┬─────────────────────────────────┐
│ Problem Type             │ Data Structure                  │
├──────────────────────────┼─────────────────────────────────┤
│ BFS (shortest path)      │ Queue                          │
│ Sliding window max/min   │ Monotonic Deque                │
│ Top-K elements           │ Priority Queue (heapq)         │
│ Merge K sorted lists     │ Priority Queue (heapq)         │
│ Task scheduling by due   │ Priority Queue                 │
│ Palindrome check         │ Deque (check both ends)        │
│ Undo/Redo                │ Deque (two stacks)             │
│ Stream first unique       │ Queue + Counter                │
│ Rotating array/queue     │ Deque + modulo                 │
└──────────────────────────┴─────────────────────────────────┘
```
