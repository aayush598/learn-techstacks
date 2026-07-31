# Stacks, Queues & Monotonic Stacks — Last-Minute Revision

Copy-paste ready, tested Python 3 templates for stack/queue problems and every monotonic-stack direction.

## Python's Built-ins: Everything You Need

```python
# list as STACK (LIFO) — push/pop from the RIGHT end
stack = []
stack.append(1)        # push   O(1)
stack.append(2)
top = stack[-1]        # peek   O(1)
x = stack.pop()        # pop    O(1)
# use with caution: if not stack:  before peek/pop on possibly-empty stack

# collections.deque as QUEUE (FIFO) — append right, pop left
from collections import deque
q = deque()
q.append(1)            # enqueue   O(1)
front = q.popleft()    # dequeue   O(1)
front = q[0]           # peek      O(1)
q.appendleft(5)        # also a stack push to the left, O(1)

# deque as STACK works too
s = deque()
s.append(1); x = s.pop()
```

| Data structure | Push/append | Pop | Peek | Use for |
|---|---|---|---|---|
| `list` stack | `append` O(1) | `pop()` O(1) | `s[-1]` | monotonic stack, parsing |
| `deque` queue | `append` O(1) | `popleft` O(1) | `d[0]` | BFS, sliding window |

## Implement Queue With Two Stacks

Two stacks: `inbox` for enqueue, `outbox` for dequeue. Only drain `inbox` into `outbox` when `outbox` is empty (amortized O(1)).

```python
class MyQueue:
    def __init__(self):
        self.inbox = []
        self.outbox = []

    def push(self, x):          # enqueue
        self.inbox.append(x)

    def pop(self):              # dequeue  -> amortized O(1)
        self._move()
        return self.outbox.pop()

    def peek(self):
        self._move()
        return self.outbox[-1]

    def empty(self):
        return not self.inbox and not self.outbox

    def _move(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())
```

| Operation | Time | Space |
|---|---|---|
| push | O(1) | O(n) total |
| pop / peek | amortized O(1), worst O(n) | O(n) |

## Circular Queue With Array (ring buffer)

```python
class MyCircularQueue:
    def __init__(self, k):
        self.q = [0] * k
        self.head = 0
        self.size = 0
        self.cap = k

    def enQueue(self, value):
        if self.isFull():
            return False
        self.q[(self.head + self.size) % self.cap] = value
        self.size += 1
        return True

    def deQueue(self):
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % self.cap
        self.size -= 1
        return True

    def Front(self):
        return -1 if self.isEmpty() else self.q[self.head]

    def Rear(self):
        return -1 if self.isEmpty() else self.q[(self.head + self.size - 1) % self.cap]

    def isEmpty(self):
        return self.size == 0

    def isFull(self):
        return self.size == self.cap
```

| Operation | Time | Space |
|---|---|---|
| all ops | O(1) | O(k) |

## Monotonic Stack — The Master Template

A monotonic stack keeps its elements strictly increasing or decreasing. When the new element breaks monotonicity, we POP until it holds, and those pops are the "answers" for the outgoing elements.

```python
def monotonic_template(nums):
    stack = []          # stores indices (or values)
    result = [0] * len(nums)
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:   # condition depends on direction
            idx = stack.pop()
            result[idx] = i - idx              # compute answer at pop time
        stack.append(i)
    return result
```

The ONLY thing that changes between the 4 directions is the comparison and the direction you iterate:

| Variant | What it finds | Iterate | Pop condition | Answer for popped `i` | Remaining stack |
|---|---|---|---|---|---|
| Next Greater Element (NGE) | next index with `nums[j] > nums[i]` | left to right | `nums[top] < nums[i]` | `j = i` | decreasing stack |
| Next Smaller Element | next index with `nums[j] < nums[i]` | left to right | `nums[top] > nums[i]` | `j = i` | increasing stack |
| Previous Greater Element | prev index with `nums[j] > nums[i]` | right to left | `nums[top] < nums[i]` | `j = i` | decreasing stack |
| Previous Smaller Element | prev index with `nums[j] < nums[i]` | right to left | `nums[top] > nums[i]` | `j = i` | increasing stack |

## Next Greater Element (NGE) — right

```python
def next_greater(nums):
    n = len(nums)
    res = [-1] * n
    stack = []                 # indices of candidates, values decreasing top to bottom
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            res[stack.pop()] = nums[i]
        stack.append(i)
    return res

# next_greater([2,1,4,3]) -> [4,4,-1,-1]
```

## Next Smaller Element — right

```python
def next_smaller(nums):
    n = len(nums)
    res = [-1] * n
    stack = []
    for i in range(n):
        while stack and nums[stack[-1]] > nums[i]:
            res[stack.pop()] = nums[i]
        stack.append(i)
    return res

# next_smaller([2,1,4,3]) -> [1,-1,3,-1]
```

## Previous Greater Element — left (iterate reversed, mirror of NGE)

```python
def prev_greater(nums):
    n = len(nums)
    res = [-1] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] < nums[i]:
            res[stack.pop()] = nums[i]
        stack.append(i)
    return res

# prev_greater([2,1,4,3]) -> [-1,2,-1,4]
```

## Previous Smaller Element — left

```python
def prev_smaller(nums):
    n = len(nums)
    res = [-1] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] > nums[i]:
            res[stack.pop()] = nums[i]
        stack.append(i)
    return res

# prev_smaller([2,1,4,3]) -> [-1,-1,1,1]
```

| Template | Time | Space |
|---|---|---|
| any monotonic variant | O(n) (each element pushed/popped once) | O(n) |

## Daily Temperatures (same as NGE, but store index distance)

```python
def daily_temperatures(temperatures):
    n = len(temperatures)
    res = [0] * n
    stack = []
    for i in range(n):
        while stack and temperatures[stack[-1]] < temperatures[i]:
            idx = stack.pop()
            res[idx] = i - idx
        stack.append(i)
    return res

# daily_temperatures([73,74,75,71,69,72,76,73]) -> [1,1,4,2,1,1,0,0]
```

| Template | Time | Space |
|---|---|---|
| daily temperatures | O(n) | O(n) |

## Sliding Window Maximum — monotonic DECREASING deque (indices)

Deque holds indices; `d[0]` is always the max of the current window. Pop from the back while the new value is larger (they can never be the max while this one lives).

```python
from collections import deque

def max_sliding_window(nums, k):
    d = deque()          # indices, values strictly decreasing
    res = []
    for i, x in enumerate(nums):
        while d and nums[d[-1]] <= x:
            d.pop()
        d.append(i)
        if d[0] <= i - k:      # index fell out of window
            d.popleft()
        if i >= k - 1:         # window is full
            res.append(nums[d[0]])
    return res

# max_sliding_window([1,3,-1,-3,5,3,6,7], 3) -> [3,3,5,5,6,7]
```

| Template | Time | Space |
|---|---|---|
| sliding window max | O(n) (each index pushed/popped once) | O(k) |

## Balanced Parentheses (multiple bracket types)

```python
def is_valid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in pairs:                 # closing bracket
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        else:
            stack.append(ch)            # opening bracket
    return not stack

# is_valid("()[]{}") -> True | is_valid("([)]") -> False
```

| Template | Time | Space |
|---|---|---|
| balanced parentheses | O(n) | O(n) |

## Basic Calculator Pattern (operator stack, single digit numbers, no parens)

Shunting-yard-ish: hold operators on a stack, track `num` and `sign` as you scan. This evaluates `"1+2-3"`, `"2*3+4"`, `"2+3*4"` correctly by respecting precedence.

```python
def evaluate(tokens):          # tokens like ["2","+","3","*","4"]
    nums = []
    ops = []
    prec = {'+': 1, '-': 1, '*': 2, '/': 2}
    for t in tokens:
        if t not in prec:
            nums.append(int(t))
        else:
            while ops and prec[ops[-1]] >= prec[t]:
                b = nums.pop()
                a = nums.pop()
                op = ops.pop()
                nums.append(apply(a, b, op))
            ops.append(t)
    while ops:
        b = nums.pop()
        a = nums.pop()
        nums.append(apply(a, b, ops.pop()))
    return nums[0]

def apply(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    return int(a / b)          # truncate toward zero

# evaluate(["2","+","3","*","4"]) -> 14
```

For the classic LeetCode basic-calculator-with-`+`/`-`/`(`/`)` variant:

```python
def basic_calculator(s):       # handles + - ( ) , spaces; e.g. " (1+(4+5+2)-3)+(6+8) "
    stack = []
    num = 0
    sign = 1
    res = 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == '+':
            res += sign * num
            num = 0
            sign = 1
        elif ch == '-':
            res += sign * num
            num = 0
            sign = -1
        elif ch == '(':
            stack.append(res)
            stack.append(sign)
            res = 0
            sign = 1
        elif ch == ')':
            res += sign * num
            num = 0
            res *= stack.pop()      # sign
            res += stack.pop()      # outer accumulated
    res += sign * num
    return res

# basic_calculator(" 2-1 + 2 ") -> 3
```

| Template | Time | Space |
|---|---|---|
| operator stack / calculator | O(n) | O(n) |

## Largest Rectangle in Histogram (monotonic increasing stack)

For each bar, it's the shortest bar in some rectangle. When a shorter bar arrives, every taller bar in the stack gets its right boundary, and its left boundary is the new stack top.

```python
def largest_rectangle_area(heights):
    heights.append(0)          # sentinel: forces all bars to pop at the end
    stack = [-1]               # sentinel index: left boundary for the first bar
    max_area = 0
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i - stack[-1] - 1    # between the two smaller bars
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area

# largest_rectangle_area([2,1,5,6,2,3]) -> 10
```

| Template | Time | Space |
|---|---|---|
| largest rectangle | O(n) | O(n) |

## Quick Reference Table

| Template | Key idea | Time | Space |
|---|---|---|---|
| list / deque basics | built-ins | O(1) per op | O(n) |
| queue with 2 stacks | drain only when outbox empty | amortized O(1) | O(n) |
| circular queue | modular index `(head+size)%cap` | O(1) | O(k) |
| monotonic stack (4 dirs) | pop = answer for outgoing index | O(n) | O(n) |
| sliding window max | monotonic decreasing deque | O(n) | O(k) |
| balanced parens | stack of opens | O(n) | O(n) |
| calculator | operator stack + precedence | O(n) | O(n) |
| largest rectangle | monotonic increasing + sentinels | O(n) | O(n) |

Memory hook: **monotonic stacks answer "what is the nearest element that is greater/smaller than me on one side" in O(n).** Pop-time is answer-time.
