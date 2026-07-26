# Stack and Queue Practice Problems

## Problem Difficulty Map

```
┌─────────────────────────────────────────────────────────────┐
│  EASY (Foundation)          │  MEDIUM (Pattern Recognition) │
│  1. Valid Parentheses       │  6. Daily Temperatures         │
│  2. Min Stack               │  7. Stock Span                 │
│  3. Queue using Stacks      │  8. Evaluate RPN               │
│  4. Baseball Game           │  9. Simplify Path              │
│  5. Crawler Log Folder      │  10. Decode String             │
├─────────────────────────────┼────────────────────────────────┤
│  HARD (Advanced Patterns)   │  Key Technique                 │
│  11. Largest Rectangle      │  → Monotonic Stack             │
│  12. Maximal Rectangle      │  → Histogram Reduction         │
│  13. Trapping Rain Water    │  → Valley Detection            │
│  14. Sliding Window Max     │  → Monotonic Deque             │
│  15. Car Fleet              │  → Sorting + Stack             │
└─────────────────────────────┴────────────────────────────────┘
```

---

## Easy Problems

### 1. Valid Parentheses
**Problem**: Given a string containing just '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

**Approach**: Use stack to match opening and closing brackets. Push opening brackets, pop when you see a closing bracket and check if it matches.

```
Visual — Walking through "({[]})":

  Char: (     {     [     ]     }     )
  Stack: [(]  [(,{] [(,{,[]
                                    Pop [ → matches ] ✓
                                    Stack: [(,{]
                          Pop { → matches } ✓
                          Stack: [(]
                                    Pop ( → matches ) ✓
                                    Stack: [] → VALID ✓

Visual — Walking through "([)]":

  Char: (     [     (     )     ]
  Stack: [(]  [(,[] [(,[](
                                    Pop ( → matches ) ✓
                                    Stack: [(,[]
                          [ doesn't match ) ✗ → INVALID!
```

**Solution**:
```python
def is_valid(s):
    """
    Check if parentheses string is valid using a stack.

    Rules:
    1. Every opening bracket must have a matching closing bracket
    2. Brackets must close in the correct order (LIFO)

    Algorithm:
    - Push every opening bracket onto the stack
    - When you see a closing bracket:
      - If stack is empty → no matching opener → invalid
      - If top of stack doesn't match → wrong order → invalid
      - If matches → pop and continue
    - At end, stack must be empty (all openers were matched)
    """
    stack = []
    # Map closing brackets to their matching opening brackets
    mapping = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in mapping:
            # It's a closing bracket — check if it matches
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            # It's an opening bracket — push to stack
            stack.append(char)

    return len(stack) == 0
    # Stack must be empty: all openers were matched

# Walkthrough: "({[]})"
#   '(' → push, stack: ['(']
#   '{' → push, stack: ['(', '{']
#   '[' → push, stack: ['(', '{', '[']
#   '}' → stack[-1]='{' matches mapping['}']='{'? YES → pop → stack: ['(']
#   ']' → stack[-1]='(' matches mapping[']']='['? NO → return False
#   Wait — actually for "({[]})" the ) is the last char, not }. Let me re-trace:
#   '(' → push, stack: ['(']
#   '{' → push, stack: ['(', '{']
#   '[' → push, stack: ['(', '{', '[']
#   ']' → pop → '[' matches mapping[']']='[' ✓ → stack: ['(', '{']
#   '}' → pop → '{' matches mapping['}']='{' ✓ → stack: ['(']
#   ')' → pop → '(' matches mapping[')']='(' ✓ → stack: []
#   len(stack)==0 → True ✓
```

**Complexity**: O(n) time, O(n) space

---

### 2. Min Stack
**Problem**: Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

**Approach**: Use two stacks — one for values, one for minimums. The min_stack only pushes when a new minimum (or equal) is found.

```
Visual — push(3), push(5), push(2), push(1), pop():

  Operation     stack       min_stack    get_min()
  ─────────     ─────       ────────     ─────────
  push(3)       [3]         [3]          3
  push(5)       [3,5]       [3]          3   ← 5>3, don't push to min
  push(2)       [3,5,2]     [3,2]        2   ← 2<3, push to min
  push(1)       [3,5,2,1]   [3,2,1]      1   ← 1<2, push to min
  pop()         [3,5,2]     [3,2]        2   ← popped 1, min goes back to 2

  Key: min_stack[-1] always holds the current minimum.
  On pop: if removed value == min_stack[-1], also pop min_stack.
```

**Solution**:
```python
class MinStack:
    """
    Stack that supports O(1) minimum retrieval.

    Two stacks work together:
    - stack:    holds ALL values
    - min_stack: holds only values that ARE or WERE the minimum

    Invariant: min_stack[-1] == minimum element in stack
    """
    def __init__(self):
        self.stack = []       # Main stack: all values
        self.min_stack = []   # Min stack: decreasing sequence of minimums

    def push(self, val):
        """Push value. Update min_stack if this is a new minimum."""
        self.stack.append(val)
        # Push to min_stack only if it's ≤ current minimum
        # Use <= (not <) to handle duplicates correctly
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self):
        """Pop value. Restore min_stack if needed."""
        if not self.stack:
            raise IndexError("Stack is empty")
        val = self.stack.pop()
        # If we're popping the current minimum, also pop from min_stack
        if val == self.min_stack[-1]:
            self.min_stack.pop()
        return val

    def top(self):
        if not self.stack:
            raise IndexError("Stack is empty")
        return self.stack[-1]

    def get_min(self):
        """O(1) minimum retrieval — just peek at min_stack top."""
        if not self.min_stack:
            raise IndexError("Stack is empty")
        return self.min_stack[-1]
```

**Complexity**: O(1) for all operations

---

### 3. Implement Queue using Stacks
**Problem**: Implement a FIFO queue using only two stacks.

**Approach**: Use two stacks — one for enqueue, one for dequeue. Transfer elements only when needed.

```
Visual — Enqueue 1,2,3 then pop, enqueue 4, pop, pop:

  enqueue(1): stack_in=[1], stack_out=[]
  enqueue(2): stack_in=[1,2], stack_out=[]
  enqueue(3): stack_in=[1,2,3], stack_out=[]

  pop(): stack_out empty → transfer all from stack_in
         stack_in=[1,2,3] → stack_out=[3,2,1] (reversed!)
         pop stack_out → returns 1 (oldest!) ✓

  enqueue(4): stack_in=[4], stack_out=[3,2]

  pop(): stack_out has elements → pop stack_out → returns 2 ✓

  pop(): stack_out=[3] → pop → returns 3 ✓

  Order: 1, 2, 3 → FIFO! ✓
```

**Solution**:
```python
class MyQueue:
    """
    FIFO queue using two LIFO stacks.

    stack_in:  receives all enqueue operations
    stack_out: serves all dequeue/peek operations

    Amortized O(1): each element is moved from stack_in to stack_out
    at most once during its lifetime.
    """
    def __init__(self):
        self.stack_in = []
        self.stack_out = []

    def push(self, x):
        """Enqueue: always push to stack_in. O(1)"""
        self.stack_in.append(x)

    def pop(self):
        """Dequeue: transfer if needed, then pop from stack_out."""
        self.peek()  # Ensure stack_out is populated
        return self.stack_out.pop()

    def peek(self):
        """
        Peek: transfer elements only when stack_out is empty.
        This is the amortized O(1) trick.
        """
        if not self.stack_out:
            # Transfer all at once: reverses order → FIFO!
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
        return self.stack_out[-1]

    def empty(self):
        return not self.stack_in and not self.stack_out
```

**Complexity**: Amortized O(1) for all operations

---

### 4. Baseball Game
**Problem**: You are keeping score for a baseball game. Return the sum of all the scores.

**Approach**: Use stack to handle special operations (+, D, C).

```
Visual — Operations ["5", "2", "C", "D", "+"]:

  "5"  → stack: [5]           (record 5)
  "2"  → stack: [5, 2]        (record 2)
  "C"  → stack: [5]           (cancel last → remove 2)
  "D"  → stack: [5, 10]       (double → 2×5=10)
  "+"  → stack: [5, 10, 15]   (sum last two → 5+10=15)

  Total = 5 + 10 + 15 = 30
```

**Solution**:
```python
def cal_points(operations):
    """
    Process baseball operations using a stack.

    Operations:
      Integer string → record that score
      "+"            → sum of last two scores
      "D"            → double of last score
      "C"            → cancel (remove) last score
    """
    stack = []

    for op in operations:
        if op == '+':
            # Add sum of last two (don't pop — we keep both)
            stack.append(stack[-1] + stack[-2])
        elif op == 'D':
            # Double the last score
            stack.append(2 * stack[-1])
        elif op == 'C':
            # Cancel/remove last score
            stack.pop()
        else:
            # Integer score
            stack.append(int(op))

    return sum(stack)
    # sum all valid scores remaining in the stack
```

**Complexity**: O(n) time, O(n) space

---

### 5. Crawler Log Folder
**Problem**: Return the minimum number of operations to go back to the main folder.

**Approach**: Use stack to track folder changes. "../" pops, "./" is ignored, anything else is pushed.

```
Visual — logs = ["d1/", "d2/", "../", "d21/", "./"]:

  "d1/"    → stack: [d1]      (enter d1)
  "d2/"    → stack: [d1, d2]  (enter d2)
  "../"    → stack: [d1]      (go up → pop d2)
  "d21/"   → stack: [d1, d21] (enter d21)
  "./"     → stack: [d1, d21] (stay → ignore)

  Answer: len(stack) = 2 (we're at /d1/d21/)
```

**Solution**:
```python
def min_operations(logs):
    """
    Track folder depth using a stack.

    "../" = go up one level (pop)
    "./"  = stay in current folder (ignore)
    else  = enter a subfolder (push)
    """
    stack = []

    for log in logs:
        if log == '../':
            if stack:          # Don't pop if already at root
                stack.pop()
        elif log != './':      # Skip "./" — it's a no-op
            stack.append(log)

    return len(stack)
    # Remaining stack depth = depth from root
```

**Complexity**: O(n) time, O(n) space

---

## Medium Problems

### 6. Daily Temperatures
**Problem**: Given an array of temperatures, return an array where answer[i] is the number of days you have to wait to get a warmer temperature.

**Approach**: Use monotonic decreasing stack. Store indices and compute distances.

```
Visual — temps = [73, 74, 75, 71, 69, 72, 76, 73]:

  Day 0 (73°): wait 1 day → 74°  ← answer[0] = 1
  Day 1 (74°): wait 1 day → 75°  ← answer[1] = 1
  Day 2 (75°): wait 4 days → 76° ← answer[2] = 4
  Day 3 (71°): wait 2 days → 72° ← answer[3] = 2
  Day 4 (69°): wait 1 day → 72°  ← answer[4] = 1
  Day 5 (72°): wait 1 day → 76°  ← answer[5] = 1
  Day 6 (76°): no warmer day     ← answer[6] = 0
  Day 7 (73°): no warmer day     ← answer[7] = 0

  Result: [1, 1, 4, 2, 1, 1, 0, 0]
```

**Solution**:
```python
def daily_temperatures(temperatures):
    """
    Monotonic decreasing stack — find days until warmer temperature.

    Same as Next Greater Element (Right), but store distance:
      result[prev_day] = i - prev_day

    Each element pushed and popped at most once → O(n).
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # Stack of INDICES (values decrease toward bottom)

    for i in range(n):
        # Current day is warmer → resolves all cooler days
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev_day = stack.pop()
            result[prev_day] = i - prev_day  # Distance, not value!

        stack.append(i)

    return result
```

**Complexity**: O(n) time, O(n) space

---

### 7. Stock Span Problem
**Problem**: The span of the stock's price today is defined as the maximum number of consecutive days for which the price was less than or equal to today's price.

**Approach**: Use monotonic decreasing stack with span accumulation.

```
prices = [100, 80, 60, 70, 60, 75, 85]

Day 0 (100): only itself → span = 1
Day 1 (80):  100 > 80, blocked → span = 1
Day 2 (60):  80 > 60, blocked → span = 1
Day 3 (70):  60 ≤ 70, merged → span = 1 + 1 = 2
Day 4 (60):  70 > 60, blocked → span = 1
Day 5 (75):  60 ≤ 75 + 70 ≤ 75 + 60 ≤ 75 → span = 1 + 1 + 2 = 4
Day 6 (85):  75 ≤ 85 + 80 ≤ 85 + ... → span = 1 + 4 + 1 = 6

Stack stores (price, accumulated_span):
  After day 0: [(100, 1)]
  After day 1: [(100, 1), (80, 1)]
  After day 2: [(100, 1), (80, 1), (60, 1)]
  After day 3: [(100, 1), (80, 1), (70, 2)]     ← 60 merged
  After day 4: [(100, 1), (80, 1), (70, 2), (60, 1)]
  After day 5: [(100, 1), (75, 4)]               ← 80 still there, (60,70,60) merged into (75,4)
  After day 6: [(85, 6)]                         ← everything merged!

Result: [1, 1, 1, 2, 1, 4, 6]
```

**Solution**:
```python
def calculate_span(prices):
    """
    Find consecutive days (including current) where price <= current price.

    Key difference from NGE: we ACCUMULATE spans by merging.
    Stack stores (price, span) tuples — when a larger price arrives,
    it absorbs all smaller/equal spans into one.

    Time: O(n) — each element pushed/popped once
    Space: O(n) — for the stack
    """
    n = len(prices)
    result = [0] * n
    stack = []  # Stores (price, span) tuples

    for i in range(n):
        span = 1  # At minimum, today counts for itself

        # Merge all smaller/equal priced days into today's span
        while stack and prices[i] >= stack[-1][0]:
            span += stack[-1][1]  # Accumulate their spans
            stack.pop()

        stack.append((prices[i], span))
        result[i] = span

    return result
```

**Complexity**: O(n) time, O(n) space

---

### 8. Evaluate Reverse Polish Notation
**Problem**: Evaluate the value of an arithmetic expression in Reverse Polish Notation.

**Approach**: Use stack to store operands. When you see an operator, pop two operands and push the result.

```
Visual — tokens = ["2", "1", "+", "3", "*"]:

  This represents: (2 + 1) × 3 = 9

  Token: "2"  → stack: [2]
  Token: "1"  → stack: [2, 1]
  Token: "+"  → pop 1, pop 2 → push 2+1=3  → stack: [3]
  Token: "3"  → stack: [3, 3]
  Token: "*"  → pop 3, pop 3 → push 3×3=9  → stack: [9]

  Result: 9

Order matters: second popped is the LEFT operand!
  pop() → b (right operand)
  pop() → a (left operand)
  result = a OP b
```

**Solution**:
```python
def eval_rpn(tokens):
    """
    Evaluate Reverse Polish Notation expression.

    RPN (postfix): operator comes AFTER its operands.
    "2 1 +" means "2 + 1".

    Algorithm:
    - Numbers → push to stack
    - Operator → pop two operands, compute, push result

    IMPORTANT: second pop() is the LEFT operand!
      For "5 3 -": pop 3, pop 5 → result = 5 - 3 = 2 (not 3 - 5!)
    """
    stack = []
    operators = {'+', '-', '*', '/'}

    for token in tokens:
        if token not in operators:
            stack.append(int(token))
        else:
            b = stack.pop()   # RIGHT operand (popped first)
            a = stack.pop()   # LEFT operand (popped second)

            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)     # a - b, NOT b - a!
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(int(a / b))  # Truncate toward zero

    return stack[0]
```

**Complexity**: O(n) time, O(n) space

---

### 9. Simplify Path
**Problem**: Given a string path, which is an absolute path starting with '/', simplify it.

**Approach**: Use stack to track directory changes. Split by '/' and process each component.

```
Visual — path = "/a/./b/../../c/":

  Split by '/': ["", "a", ".", "b", "..", "..", "c", ""]

  Component  ""   → skip (empty)
  Component  "a"  → push → stack: [a]
  Component  "."  → skip (current dir, no-op)
  Component  "b"  → push → stack: [a, b]
  Component  ".." → pop → stack: [a]      (go up one level)
  Component  ".." → pop → stack: []       (go up one more)
  Component  "c"  → push → stack: [c]
  Component  ""   → skip (empty)

  Join: "/" + "c" = "/c"
```

**Solution**:
```python
def simplify_path(path):
    """
    Simplify Unix-style absolute path.

    Rules:
    - '/' is the root
    - '.' means stay in current directory
    - '..' means go up one directory
    - Multiple consecutive '/' are treated as one
    - A valid path starts with '/' and doesn't end with '/'
    """
    stack = []
    components = path.split('/')

    for component in components:
        if component == '..':
            if stack:
                stack.pop()     # Go up one level
        elif component and component != '.':
            stack.append(component)  # Valid directory name

    return '/' + '/'.join(stack)
    # Join with '/' and add leading '/'
```

**Complexity**: O(n) time, O(n) space

---

### 10. Decode String
**Problem**: Given an encoded string, return its decoded string.

**Approach**: Use two stacks — one for counts, one for strings. Handle nesting with `[` and `]`.

```
Visual — s = "3[a2[c]]":

  Process: "3"  → current_num = 3
  Process: "["  → push(3, "") to stacks
                   stack_count: [3]
                   stack_string: [""]
                   current_string = "", current_num = 0
  Process: "a"  → current_string = "a"
  Process: "2"  → current_num = 2
  Process: "["  → push(2, "a") to stacks
                   stack_count: [3, 2]
                   stack_string: ["", "a"]
                   current_string = "", current_num = 0
  Process: "c"  → current_string = "c"
  Process: "]"  → pop: count=2, prev="a"
                   current_string = "a" + "c"*2 = "acc"
  Process: "]"  → pop: count=3, prev=""
                   current_string = "" + "acc"*3 = "accaccacc"

  Result: "accaccacc"

  Nested case visual:
  ┌──────────────────────────────────────┐
  │  3 [ a 2 [ c ] ]                     │
  │  │     │     │                       │
  │  │     │     └─ inner decode: "cc"   │
  │  │     └─ prefix "a" + "cc" = "acc"  │
  │  └─ repeat 3 times: "accaccacc"      │
  └──────────────────────────────────────┘
```

**Solution**:
```python
def decode_string(s):
    """
    Decode strings like "3[a2[c]]" → "accaccacc".

    Two stacks handle nested brackets:
    - stack_count: saves the repeat count when entering a bracket
    - stack_string: saves the string built so far when entering a bracket

    When we see ']':
    1. Pop the count and previous string
    2. current_string = prev_string + current_string × count
    """
    stack_count = []
    stack_string = []
    current_string = ""
    current_num = 0

    for char in s:
        if char.isdigit():
            # Build multi-digit number
            current_num = current_num * 10 + int(char)
        elif char == '[':
            # Entering a nested section — save current state
            stack_count.append(current_num)
            stack_string.append(current_string)
            current_string = ""
            current_num = 0
        elif char == ']':
            # Exiting a nested section — decode and combine
            count = stack_count.pop()
            prev_string = stack_string.pop()
            current_string = prev_string + current_string * count
        else:
            # Regular character — append to current string
            current_string += char

    return current_string
```

**Complexity**: O(n) time, O(n) space

---

## Hard Problems

### 11. Largest Rectangle in Histogram
**Problem**: Given n non-negative integers representing the histogram's bar height, find the area of the largest rectangle.

**Approach**: Use monotonic increasing stack with sentinel. When a shorter bar is found, compute area for all taller bars on the stack.

```
heights = [2, 1, 5, 6, 2, 3]

Visual of the histogram:
  6 │          ████
  5 │    █     ████
  4 │    █     ████
  3 │    █     ████     ████
  2 │█████     ████  █  ████
  1 │█████  █  ████  █  ████
  0 └──────────────────────────
      0  1  2  3  4  5

Largest rectangle: bars 2,3 (height=5, width=2) → area = 10

How the stack finds it (with sentinel h=0 at end):
  i=0(h=2): push 0                    → stack: [0]
  i=1(h=1): 1<2, pop 0→h=2,stack→[],w=1, area=2
            push 1                     → stack: [1]
  i=2(h=5): push 2                     → stack: [1,2]
  i=3(h=6): push 3                     → stack: [1,2,3]
  i=4(h=2): 2<6, pop 3→h=6,w=4-2-1=1, area=6
            2<5, pop 2→h=5,w=4-1-1=2, area=10 ← MAX!
            2>1, push 4                 → stack: [1,4]
  i=5(h=3): push 5                     → stack: [1,4,5]
  i=6(sentinel 0):
            0<3, pop 5→h=3,area=3
            0<2, pop 4→h=2,w=6-1-1=4, area=8
            0<1, pop 1→h=1,w=6, area=6
  Final max_area = 10 ✓
```

**Solution**:
```python
def largest_rectangle_area(heights):
    """
    Find the largest rectangular area in a histogram.

    Key insight: Add a sentinel height=0 at the end to flush all
    remaining bars from the stack.

    For each popped bar at index popped_idx:
      - height = heights[popped_idx]
      - width = current_i - (new stack top) - 1
      - area = height × width

    Why it works: Each bar extends as far left and right as possible
    until it hits a shorter bar. The stack maintains this info.
    """
    stack = []
    max_area = 0
    n = len(heights)

    for i in range(n + 1):
        # Use 0 as sentinel to flush remaining bars
        current_height = heights[i] if i < n else 0

        # Current bar is shorter → all taller bars are "resolved"
        while stack and current_height < heights[stack[-1]]:
            height = heights[stack.pop()]
            # Width: between previous stack top and current index
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)

        stack.append(i)

    return max_area
```

**Complexity**: O(n) time, O(n) space

---

### 12. Maximal Rectangle
**Problem**: Given a 2D binary matrix filled with 0s and 1s, find the largest rectangle containing only 1s.

**Approach**: Build histogram heights for each row, then apply Largest Rectangle in Histogram.

```
Matrix:
  1 0 1 0 0       Row 0 heights: [1, 0, 1, 0, 0]  → max_area = 1
  1 0 1 1 1       Row 1 heights: [2, 0, 2, 1, 1]  → max_area = 3
  1 1 1 1 1       Row 2 heights: [3, 1, 3, 2, 2]  → max_area = 6 ← BEST
  1 0 0 1 0       Row 3 heights: [4, 0, 0, 3, 0]  → max_area = 4

Row 2 histogram: [3, 1, 3, 2, 2]
                  │     │  │  │
                  │     │  └──┘  → 2×2 = 4
                  │     └──────  → 3×1 = 3
                  └────────────  → 3×1 = 3

  The best is actually indices 2,3,4 → heights [3,2,2]
  Rectangle of height 2 spanning 3 bars: area = 2×3 = 6 ✓
```

**Solution**:
```python
def maximal_rectangle(matrix):
    """
    Find the largest rectangle of 1s in a binary matrix.

    Strategy: Build a histogram for each row where heights[j] represents
    the number of consecutive 1s above (including) matrix[i][j].

    Then apply Largest Rectangle in Histogram for each row.
    """
    if not matrix:
        return 0

    rows, cols = len(matrix), len(matrix[0])
    heights = [0] * cols  # Running histogram — builds up row by row
    max_area = 0

    for i in range(rows):
        # Update histogram: extend column if 1, reset if 0
        for j in range(cols):
            if matrix[i][j] == '1':
                heights[j] += 1   # Extend column upward
            else:
                heights[j] = 0    # Column broken — reset

        # Find largest rectangle in current row's histogram
        max_area = max(max_area, largest_rectangle_area(heights))

    return max_area

# largest_rectangle_area() is the same function from problem #11
```

**Complexity**: O(m * n) time, O(n) space

---

### 13. Trapping Rain Water
**Problem**: Given n non-negative integers representing an elevation map, compute how much water it can trap.

**Approach**: Use monotonic increasing stack to detect "valleys" where water gets trapped.

```
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]

Visual (water = ~, walls = █):
  3 │                        █
  2 │        █     █~~█      ███
  1 │   █    ████  █~~███  █████
  0 │██~███~~███████~~█████████████
    └──────────────────────────────
      0 1 2 3 4 5 6 7 8 9 10 11

Water trapped by the stack approach (horizontal strips):
  When we encounter a bar taller than stack top:
  - Stack top = bottom of a trough
  - New stack top = left wall
  - Current bar = right wall

  Example: indices [1,2,3] → heights [1,0,2]
    bottom=2(h=0), left_wall=1(h=1), right_wall=3(h=2)
    trapped = min(1,2) - 0 = 1, width = 3-1-1 = 1
    water += 1 × 1 = 1

  Total trapped water = 6 ✓
```

**Solution**:
```python
def trap(height):
    """
    Compute trapped rain water using monotonic increasing stack.

    Water is trapped in "valleys" — places where bars on both sides
    are taller than the bottom. The stack tracks potential valley bottoms.

    When we find a taller bar:
    1. Pop the bottom (valley floor)
    2. Left wall = new stack top
    3. Right wall = current bar
    4. Water = width × min(left_height, right_height) - bottom_height
    """
    if not height:
        return 0

    stack = []
    water = 0

    for i, h in enumerate(height):
        # Current bar is taller → forms troughs with stack elements
        while stack and h > height[stack[-1]]:
            bottom = stack.pop()  # Valley floor

            if stack:
                # Left wall = stack top, Right wall = current bar i
                width = i - stack[-1] - 1
                trapped_height = min(h, height[stack[-1]]) - height[bottom]
                water += width * trapped_height

        stack.append(i)

    return water
```

**Complexity**: O(n) time, O(n) space

---

### 14. Sliding Window Maximum
**Problem**: Given an array nums and a sliding window of size k, return the max in each window.

**Approach**: Use monotonic decreasing deque to maintain potential maximums.

```
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

Windows and their max:
  [1, 3,-1] → 3    [3,-1,-3] → 3    [-1,-3, 5] → 5
  [-3, 5, 3] → 5    [5, 3, 6] → 6    [3, 6, 7] → 7

Result: [3, 3, 5, 5, 6, 7]

Deque tracks indices (values shown):
  i=0(1): dq=[0]        → [1]
  i=1(3): pop 0(1<3)    → dq=[1]      → [3]
  i=2(-1): push          → dq=[1,2]    → [3,-1]
  → window complete, max=nums[dq[0]]=3 ✓

  i=3(-3): push          → dq=[1,2,3]  → [3,-1,-3]
  → window complete, max=3 ✓

  i=4(5): pop 3(-3<5), pop 2(-1<5), pop 1(3<5) → dq=[4] → [5]
  → max=5 ✓

  i=5(3): push           → dq=[4,5]    → [5,3]
  → max=5 ✓

  i=6(6): pop 5(3<6), pop 4(5<6) → dq=[6] → [6]
  → max=6 ✓

  i=7(7): pop 6(6<7) → dq=[7] → [7]
  → max=7 ✓
```

**Solution**:
```python
from collections import deque

def max_sliding_window(nums, k):
    """
    Find maximum in every sliding window of size k.

    Monotonic decreasing deque:
    - Front = index of current window's maximum
    - Back = candidates for future max (decreasing order)
    - Remove from front: elements that slid out of window
    - Remove from back: elements smaller than current (useless)

    Each element pushed/popped at most once → O(n).
    """
    result = []
    dq = deque()  # Stores INDICES (not values!)

    for i in range(len(nums)):
        # Remove elements that fell outside the window (left side)
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements from back (they'll never be max)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        dq.append(i)

        # Window is complete — front holds the max
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

**Complexity**: O(n) time, O(k) space

---

### 15. Car Fleet
**Problem**: There are n cars going to the same destination. A car fleet is a non-empty set of cars driving at the same speed. Return the number of car fleets.

**Approach**: Sort by position (closest to target first), use stack to track arrival times.

```
Example: target=12, position=[10,8,0,5,3], speed=[2,4,1,1,3]

Step 1: Sort by position (descending — closest first):
  Car 0: pos=10, speed=2 → time = (12-10)/2 = 1.0
  Car 1: pos=8,  speed=4 → time = (12-8)/4  = 1.0
  Car 4: pos=5,  speed=1 → time = (12-5)/1  = 7.0
  Car 3: pos=3,  speed=1 → time = (12-3)/1  = 9.0
  Car 2: pos=0,  speed=3 → time = (12-0)/3  = 4.0

Step 2: Process in order, stack tracks fleet arrival times:

  Car 0 (time=1.0): stack empty → push 1.0    stack: [1.0]
  Car 1 (time=1.0): 1.0 ≤ 1.0, merges →      stack: [1.0]     (no push!)
  Car 4 (time=7.0): 7.0 > 1.0, new fleet →   stack: [1.0, 7.0]
  Car 3 (time=9.0): 9.0 > 7.0, new fleet →   stack: [1.0, 7.0, 9.0]
  Car 2 (time=4.0): 4.0 ≤ 7.0, merges →      stack: [1.0, 7.0, 9.0]

  Wait — let me re-check. The stack should be:
  Car 0 (time=1.0): push → [1.0]
  Car 1 (time=1.0): 1.0 ≤ 1.0 → don't push (merges with fleet ahead)
  Car 4 (time=7.0): 7.0 > 1.0 → push → [1.0, 7.0]
  Car 3 (time=9.0): 9.0 > 7.0 → push → [1.0, 7.0, 9.0]
  Car 2 (time=4.0): 4.0 ≤ 9.0? No, 4.0 > 9.0? No. 4.0 < 9.0 → merges with fleet

  Wait, I need to re-order. position sorted descending: [10,8,5,3,0]
  Car at pos 10: time=1.0
  Car at pos 8:  time=1.0
  Car at pos 5:  time=7.0
  Car at pos 3:  time=9.0
  Car at pos 0:  time=4.0

  Stack: [1.0] → [1.0, 7.0] → [1.0, 7.0, 9.0]
  4.0 < 9.0 → merges → stack: [1.0, 7.0, 9.0]
  Result: 3 fleets ✓
```

**Solution**:
```python
def car_fleet(target, position, speed):
    """
    Count car fleets arriving at the target.

    Key insight: Sort cars by position (closest to target first).
    A car joins the fleet ahead if it arrives no later (time <= fleet time).
    A car starts a new fleet if it arrives later (time > fleet time).

    Stack tracks arrival times of each fleet.
    """
    n = len(position)
    # Pair up and sort by position descending (closest to target first)
    cars = sorted(zip(position, speed), reverse=True)
    stack = []  # Stack of arrival times

    for pos, spd in cars:
        time = (target - pos) / spd  # Time to reach target

        # If this car arrives later than the fleet ahead, it's a new fleet
        if not stack or time > stack[-1]:
            stack.append(time)
        # Otherwise, it catches up and merges with the fleet ahead

    return len(stack)
    # Each stack element represents one fleet
```

**Complexity**: O(n log n) time, O(n) space

---

## Summary Table

| # | Problem | Difficulty | Time | Space | Key Technique |
|---|---------|------------|------|-------|---------------|
| 1 | Valid Parentheses | Easy | O(n) | O(n) | Stack matching |
| 2 | Min Stack | Easy | O(1) | O(n) | Auxiliary min stack |
| 3 | Queue using Stacks | Easy | O(1)* | O(n) | Two-stack transfer |
| 4 | Baseball Game | Easy | O(n) | O(n) | Stack operations |
| 5 | Crawler Log Folder | Easy | O(n) | O(n) | Stack depth tracking |
| 6 | Daily Temperatures | Medium | O(n) | O(n) | Monotonic decreasing stack |
| 7 | Stock Span | Medium | O(n) | O(n) | Monotonic stack + merge |
| 8 | Evaluate RPN | Medium | O(n) | O(n) | Operand stack |
| 9 | Simplify Path | Medium | O(n) | O(n) | Path component stack |
| 10 | Decode String | Medium | O(n) | O(n) | Nested string/count stacks |
| 11 | Largest Rectangle | Hard | O(n) | O(n) | Monotonic stack + sentinel |
| 12 | Maximal Rectangle | Hard | O(m*n) | O(n) | Histogram reduction |
| 13 | Trapping Rain Water | Hard | O(n) | O(n) | Monotonic stack (valley) |
| 14 | Sliding Window Max | Hard | O(n) | O(k) | Monotonic deque |
| 15 | Car Fleet | Hard | O(n log n) | O(n) | Sort + stack |

*Amortized O(1)

---

## Pattern Recognition Guide

```
┌────────────────────────────────────────────────────────────────────┐
│  "I see BRACKETS/PARENTHESES"                                      │
│  → Use a Stack for matching (#1)                                    │
├────────────────────────────────────────────────────────────────────┤
│  "I need MIN/MAX at all times in a stack"                          │
│  → Use auxiliary Min/Max Stack (#2)                                 │
├────────────────────────────────────────────────────────────────────┤
│  "Convert one data structure to another"                           │
│  → Two Stacks = Queue (#3)                                          │
├────────────────────────────────────────────────────────────────────┤
│  "Process SPECIAL OPERATIONS on a sequence"                        │
│  → Stack for state management (#4, #5)                              │
├────────────────────────────────────────────────────────────────────┤
│  "Find NEXT GREATER/SMALLER element"                               │
│  → Monotonic Stack (#6, #7)                                         │
├────────────────────────────────────────────────────────────────────┤
│  "Evaluate EXPRESSIONS"                                            │
│  → Operand Stack (#8)                                               │
├────────────────────────────────────────────────────────────────────┤
│  "Process NESTED STRUCTURES (paths, strings, brackets)"            │
│  → Stack (#9, #10)                                                  │
├────────────────────────────────────────────────────────────────────┤
│  "Find LARGEST RECTANGLE in histogram-like structure"              │
│  → Monotonic Stack + Sentinel (#11, #12)                            │
├────────────────────────────────────────────────────────────────────┤
│  "Calculate TRAPPED WATER"                                         │
│  → Monotonic Stack for valley detection (#13)                      │
├────────────────────────────────────────────────────────────────────┤
│  "SLIDING WINDOW max/min"                                          │
│  → Monotonic Deque (#14)                                            │
├────────────────────────────────────────────────────────────────────┤
│  "SORT + decide GROUPS/FLEETS"                                     │
│  → Sort + Stack (#15)                                               │
└────────────────────────────────────────────────────────────────────┘
```

*Amortized O(1)
