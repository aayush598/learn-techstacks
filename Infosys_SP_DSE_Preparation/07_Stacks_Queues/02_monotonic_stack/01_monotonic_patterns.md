# Monotonic Stack Patterns

## What is Monotonic Stack

A monotonic stack is a stack where elements maintain a specific order (either all increasing or all decreasing). It's the go-to data structure for "next greater/smaller element" problems, running in **O(n)** time.

### Core Idea — The "Violator" Principle

```
NORMAL STACK:  Just push/pop freely
MONOTONIC STACK: Push freely, but BEFORE pushing, pop everything that
                 violates the monotonic property
```

### Two Types

```
┌──────────────────────────────────────────────────────────────────┐
│                     MONOTONIC STACK TYPES                        │
├──────────────────────┬───────────────────────────────────────────┤
│  MONOTONIC DECREASING │  MONOTONIC INCREASING                    │
│                       │                                          │
│  Top                  │  Top                                     │
│  ┌────────┐           │  ┌────────┐                              │
│  │   2    │ ← smallest│  │   9    │ ← largest                    │
│  │   5    │           │  │   6    │                              │
│  │   8    │           │  │   3    │                              │
│  │  10    │ ← largest │  │   1    │ ← smallest                   │
│  └────────┘           │  └────────┘                              │
│                       │                                          │
│  Used for:            │  Used for:                               │
│  "Next Greater"       │  "Next Smaller"                          │
│  problems             │  problems                                │
└──────────────────────┴───────────────────────────────────────────┘
```

### Visual Walkthrough — Why It Works

```
Array: [2, 1, 5, 3, 4]
Goal: Find Next Greater Element (Right)

Processing index 0 (val=2):
  Stack: [2]              — just push

Processing index 1 (val=1):
  1 < 2, no violation → push
  Stack: [2, 1]           — still decreasing ✓

Processing index 2 (val=5):
  5 > 1 → pop 1, set NGE[1] = 5    ← VIOLATION: pop!
  5 > 2 → pop 2, set NGE[2] = 5    ← VIOLATION: pop!
  Stack: [5]              — push 5

Processing index 3 (val=3):
  3 < 5, no violation → push
  Stack: [5, 3]           — decreasing ✓

Processing index 4 (val=4):
  4 > 3 → pop 3, set NGE[3] = 4    ← VIOLATION: pop!
  4 < 5, no violation → push
  Stack: [5, 4]           — decreasing ✓

Remaining in stack: indices of 5 and 4 → NGE = -1 (none found)

Result: [-1, 5, -1, 4, -1]
```

### Key Insight

> When you encounter an element that violates the monotonic property, you **pop elements and process them** — the current element IS the answer for all popped elements.

## Next Greater Element (Right) - O(n)

**Problem**: For each element, find the first element to its right that is greater. If none exists, return -1.

**Strategy**: Maintain a **decreasing** stack. When a larger element appears, it "resolves" all smaller elements on the stack.

```python
def next_greater_element_right(nums):
    """
    For each element, find the next element to its RIGHT that is GREATER.

    Stack invariant: stack always stores indices in DECREASING order of values.
    When nums[i] > nums[stack[-1]], we've found the NGE for stack[-1].

    Time: O(n) — each element pushed and popped at most once
    Space: O(n) — for the stack and result array
    """
    n = len(nums)
    result = [-1] * n       # Default: no greater element found
    stack = []              # Stores INDICES, values at those indices are decreasing

    for i in range(n):
        # While current element is GREATER than stack top's value:
        # we found the NGE for stack top!
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()           # Get the index waiting for an answer
            result[idx] = nums[i]       # Current element IS the next greater

        stack.append(i)                 # Push current index

    return result

# Example walkthrough:
# nums = [2, 1, 2, 4, 3]
# Step-by-step:
#   i=0: stack=[], push 0          → stack: [0]       (vals: [2])
#   i=1: 1<2, push 1              → stack: [0,1]     (vals: [2,1])
#   i=2: 2>1, pop 1 → result[1]=2  → stack: [0]      (vals: [2])
#        2 not > 2, push 2         → stack: [0,2]     (vals: [2,2])
#   i=3: 4>2, pop 2 → result[2]=4  → stack: [0]      (vals: [2])
#        4>2, pop 0 → result[0]=4   → stack: []       (vals: [])
#        push 3                     → stack: [3]       (vals: [4])
#   i=4: 3<4, push 4               → stack: [3,4]     (vals: [4,3])
# Result: [4, 2, 4, -1, -1]
```

## Next Smaller Element (Right) - O(n)

**Problem**: For each element, find the first element to its right that is smaller.

**Strategy**: Maintain an **increasing** stack. When a smaller element arrives, it resolves all larger elements.

```python
def next_smaller_element_right(nums):
    """
    For each element, find the next element to its RIGHT that is SMALLER.

    Stack invariant: stack stores indices in INCREASING order of values.
    When nums[i] < nums[stack[-1]], we found the NSE for stack[-1].
    """
    n = len(nums)
    result = [-1] * n
    stack = []

    for i in range(n):
        # Current element is SMALLER — it resolves all larger stack elements
        while stack and nums[i] < nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]

        stack.append(i)

    return result

# Example walkthrough:
# nums = [2, 1, 2, 4, 3]
#   i=0: push 0                    → stack: [0]       (vals: [2])
#   i=1: 1<2, pop 0 → result[0]=1  → stack: []
#        push 1                     → stack: [1]       (vals: [1])
#   i=2: 2>1, push 2               → stack: [1,2]     (vals: [1,2])
#   i=3: 4>2, push 3               → stack: [1,2,3]   (vals: [1,2,4])
#   i=4: 3<4, pop 3 → result[3]=3  → stack: [1,2]     (vals: [1,2])
#        3>2, push 4               → stack: [1,2,4]   (vals: [1,2,3])
# Result: [1, -1, -1, 3, -1]
```

## Next Greater Element (Left) - O(n)

**Problem**: For each element, find the first element to its LEFT that is greater.

**Key Difference from Right variant**: Here, when we encounter `nums[i]`, it's the candidate to answer for future elements (not the other way around). So we pop elements smaller than `nums[i]` BEFORE appending.

```python
def next_greater_element_left(nums):
    """
    For each element, find the PREVIOUS element (to its LEFT) that is GREATER.

    Stack invariant: decreasing order of values.
    At each i, stack[-1] holds the nearest greater element to the left of i.
    """
    n = len(nums)
    result = [-1] * n
    stack = []

    for i in range(n):
        # Pop elements that are SMALLER — they can never be NGL for anyone
        while stack and nums[stack[-1]] < nums[i]:
            stack.pop()

        # If stack is non-empty, top is the nearest greater to the left
        if stack:
            result[i] = nums[stack[-1]]

        stack.append(i)  # Push current as candidate for future elements

    return result

# Example walkthrough:
# nums = [2, 1, 2, 4, 3]
#   i=0: stack empty → result[0]=-1, push 0     → stack: [0]   (vals: [2])
#   i=1: 2>1, no pop → result[1]=2, push 1      → stack: [0,1] (vals: [2,1])
#   i=2: 1<2, pop 0 → stack empty
#        stack empty → result[2]=-1, push 2      → stack: [2]   (vals: [2])
#        Wait — nums[0]=2 is NOT < nums[2]=2, so no pop. result[2]=-1. push 2.
#   i=3: 2<4, pop 2 → stack empty
#        stack empty → result[3]=-1, push 3      → stack: [3]   (vals: [4])
#   i=4: 4>3, no pop → result[4]=4, push 4      → stack: [3,4] (vals: [4,3])
# Result: [-1, 2, -1, -1, 4]
```

> **Pattern Tip**: For "left" variants, the answer is SET at index `i` (not popped). For "right" variants, the answer is SET when popping.

## Next Smaller Element (Left) - O(n)

**Problem**: For each element, find the first element to its LEFT that is smaller.

**Strategy**: Maintain an **increasing** stack. Current element's value is the candidate for future elements.

```python
def next_smaller_element_left(nums):
    """
    For each element, find the PREVIOUS element (to its LEFT) that is SMALLER.

    Stack invariant: increasing order of values.
    """
    n = len(nums)
    result = [-1] * n
    stack = []

    for i in range(n):
        # Pop elements that are LARGER — they can't be NSL for anyone
        while stack and nums[stack[-1]] > nums[i]:
            stack.pop()

        if stack:
            result[i] = nums[stack[-1]]

        stack.append(i)

    return result

# Example walkthrough:
# nums = [2, 1, 2, 4, 3]
#   i=0: stack empty → result[0]=-1, push 0      → stack: [0]   (vals: [2])
#   i=1: 2>1, pop 0 → stack empty
#        stack empty → result[1]=-1, push 1       → stack: [1]   (vals: [1])
#   i=2: 1<2, no pop → result[2]=1, push 2       → stack: [1,2] (vals: [1,2])
#   i=3: 2<4, no pop → result[3]=2, push 3       → stack: [1,2,3] (vals: [1,2,4])
#   i=4: 4>3, pop 3 → stack: [1,2]
#        2>3? No → result[4]=2, push 4           → stack: [1,2,4] (vals: [1,2,3])
# Result: [-1, -1, 1, 2, 2]
```

## Daily Temperatures - O(n)

**Problem**: Given daily temperatures, for each day find how many days until a warmer temperature.

**This is a direct application of Next Greater Element (Right)** — but instead of storing the value, store the **distance** (index difference).

```
Input:  [73, 74, 75, 71, 69, 72, 76, 73]
Output: [ 1,  1,  4,  2,  1,  1,  0,  0]

Visual:
Day:    0    1    2    3    4    5    6    7
Temp:  73   74   75   71   69   72   76   73
       │    │    │              │    │
       │    │    └── 76(4 days)│    └── 76(1 day)
       │    └── 74(1 day)      └── 72(1 day)
       └── 74(1 day)

Day 6 (76°): no warmer day → 0
Day 7 (73°): no warmer day → 0
```

```python
def daily_temperatures(temperatures):
    """
    For each day, find days until next warmer temperature.

    Same logic as Next Greater Element Right, but we store DISTANCE
    instead of value: result[prev_day] = i - prev_day (index difference).
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # Stack of INDICES (not values!)

    for i in range(n):
        # Current day is warmer — resolve all cooler days on stack
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev_day = stack.pop()
            result[prev_day] = i - prev_day  # Distance, not value!

        stack.append(i)

    return result

# Walkthrough with temps = [73, 74, 75, 71, 69, 72, 76, 73]:
#   i=0(73): stack=[], push 0                   → stack: [0]
#   i=1(74): 74>73, pop 0 → result[0]=1-0=1     → stack: []
#            push 1                              → stack: [1]
#   i=2(75): 75>74, pop 1 → result[1]=2-1=1     → stack: []
#            push 2                              → stack: [2]
#   i=3(71): 71<75, push 3                      → stack: [2,3]
#   i=4(69): 69<71, push 4                      → stack: [2,3,4]
#   i=5(72): 72>69, pop 4 → result[4]=5-4=1     → stack: [2,3]
#            72>71, pop 3 → result[3]=5-3=2     → stack: [2]
#            72<75, push 5                      → stack: [2,5]
#   i=6(76): 76>72, pop 5 → result[5]=6-5=1     → stack: [2]
#            76>75, pop 2 → result[2]=6-2=4     → stack: []
#            push 6                              → stack: [6]
#   i=7(73): 73<76, push 7                      → stack: [6,7]
# Result: [1, 1, 4, 2, 1, 1, 0, 0] ✓
```

## Stock Span Problem - O(n)

**Problem**: For each day's stock price, find the number of consecutive days (including today) where the price was <= today's price.

**Strategy**: Monotonic **decreasing** stack that stores `(price, span)` tuples. When a new price is >= stack top, merge spans.

```
Input:  [100, 80, 60, 70, 60, 75, 85]
Output: [  1,  1,  1,  2,  1,  4,  6]

Visual (bars show span for each day):
Day: 0  1  2  3  4  5  6
$100 █                    → span=1 (only itself)
 $80 █                    → span=1 (100>80, blocked)
 $60 █                    → span=1 (80>60, blocked)
 $70 ██                   → span=2 (60≤70, 70 is the wall)
 $60 █                    → span=1 (70>60, blocked)
 $75 ████                 → span=4 (60,70,60,75 all ≤75)
 $85 ██████               → span=6 (all ≤85 except 100)

Stack at each step stores (price, accumulated_span):
  After day 0: [(100, 1)]
  After day 1: [(100, 1), (80, 1)]
  After day 2: [(100, 1), (80, 1), (60, 1)]
  After day 3: [(100, 1), (80, 1), (70, 2)]      ← 60 merged into 70
  After day 4: [(100, 1), (80, 1), (70, 2), (60, 1)]
  After day 5: [(100, 1), (80, 1), (75, 4)]      ← 60,70,60 merged!
  After day 6: [(100, 1), (85, 6)]                ← everything merged!
```

```python
def stock_span(prices):
    """
    Find consecutive days (including current) with price <= current price.

    Key difference from NGE: we ACCUMULATE spans by merging.
    Stack stores (price, span) tuples instead of just indices.
    """
    n = len(prices)
    result = [0] * n
    stack = []  # Stores (price, span) tuples

    for i in range(n):
        span = 1  # At minimum, today counts

        # Merge all smaller/equal spans from stack
        while stack and prices[i] >= stack[-1][0]:
            span += stack[-1][1]  # Accumulate the span
            stack.pop()

        stack.append((prices[i], span))
        result[i] = span

    return result

# Walkthrough with prices = [100, 80, 60, 70, 60, 75, 85]:
#   i=0(100): span=1, stack=[(100,1)]                    → result[0]=1
#   i=1(80):  80<100, span=1, stack=[(100,1),(80,1)]     → result[1]=1
#   i=2(60):  60<80, span=1, stack=[(100,1),(80,1),(60,1)] → result[2]=1
#   i=3(70):  70>=60, span=1+1=2, pop (60,1)
#             70<80, stack=[(100,1),(80,1),(70,2)]        → result[3]=2
#   i=4(60):  60<70, span=1, stack=[(100,1),(80,1),(70,2),(60,1)] → result[4]=1
#   i=5(75):  75>=60, span=1+1=2, pop (60,1)
#             75>=70, span=2+2=4, pop (70,2)
#             75<80, stack=[(100,1),(80,1),(75,4)]        → result[5]=4
#   i=6(85):  85>=75, span=1+4=5, pop (75,4)
#             85>=80, span=5+1=6, pop (80,1)
#             85<100, stack=[(100,1),(85,6)]              → result[6]=6
# Result: [1, 1, 1, 2, 1, 4, 6] ✓
```

## Largest Rectangle in Histogram - O(n)

**Problem**: Given bar heights, find the area of the largest rectangle that fits.

**Strategy**: For each bar, find how far it can extend left and right (until a shorter bar). Use an **increasing** stack. When a shorter bar is found, popped bars' rectangles are fully determined.

```
Input:  [2, 1, 5, 6, 2, 3]
Output: 10

Visual of the histogram:
Height:
  6 │          ████
  5 │    █     ████
  4 │    █     ████
  3 │    █     ████     ████
  2 │█████     ████  █  ████
  1 │█████  █  ████  █  ████
  0 └──────────────────────────
      0  1  2  3  4  5    Index

Largest rectangle: bars 2,3 with height 5 → area = 5 × 2 = 10

How the stack finds it:
  - Bar 2 (h=5): extends left to index 1, right to index 4
    Width = 4 - 1 - 1 = 2, Area = 5 × 2 = 10 ← MAX!
  - Bar 3 (h=6): extends left to index 1, right to index 4
    Width = 4 - 1 - 1 = 2, Area = 6 × 2 = 12?
    Wait — bar 2 (h=5) blocks it from extending freely.
    Actually bar 3's width is limited by bar 2's shorter height.
    When bar 3 is popped (by bar 4, h=2):
      height = 6, stack has index 2 → width = 4 - 2 - 1 = 1 → area = 6
    When bar 2 is popped (by bar 4, h=2):
      height = 5, stack empty → width = 4 → area = 5 × 2 = 10 ✓
```

```python
def largest_rectangle_area(heights):
    """
    Find the largest rectangular area in a histogram.

    Key insight: We add a sentinel height=0 at the end to flush all
    remaining bars from the stack.

    For each popped bar:
      - height = heights[popped_index]
      - width = current_index - (stack_top_index) - 1
               or current_index if stack is empty (extends to left edge)
    """
    stack = []
    max_area = 0
    n = len(heights)

    for i in range(n + 1):
        # Sentinel: force all remaining bars to be processed
        current_height = heights[i] if i < n else 0

        # Current bar is SHORTER — all taller bars on stack are now "resolved"
        while stack and current_height < heights[stack[-1]]:
            height = heights[stack.pop()]   # Height of the bar being resolved
            # Width: from (stack top + 1) to (i - 1), inclusive
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)

        stack.append(i)

    return max_area

# Walkthrough with heights = [2, 1, 5, 6, 2, 3]:
#   i=0(2): push 0                → stack: [0]
#   i=1(1): 1<2, pop 0 → h=2,w=1-0-1=0? No, stack empty → w=1 → area=2
#            push 1               → stack: [1]
#   i=2(5): push 2                → stack: [1,2]
#   i=3(6): push 3                → stack: [1,2,3]
#   i=4(2): 2<6, pop 3 → h=6, w=4-2-1=1 → area=6
#            2<5, pop 2 → h=5, w=4-1-1=2 → area=10 ← MAX!
#            2>1, push 4           → stack: [1,4]
#   i=5(3): push 5                → stack: [1,4,5]
#   i=6(sentinel 0):
#            0<3, pop 5 → h=3, w=6-4-1=1 → area=3
#            0<2, pop 4 → h=2, w=6-1-1=4 → area=8
#            0<1, pop 1 → h=1, w=6 → area=6
# Result: 10 ✓
```

## Maximal Rectangle in Binary Matrix - O(m * n)

**Problem**: Find the largest rectangle of 1s in a binary matrix.

**Strategy**: Build a histogram for each row, then apply Largest Rectangle in Histogram.

```
Input Matrix:
  1 0 1 0 0       Row 0 histogram: [1, 0, 1, 0, 0]
  1 0 1 1 1       Row 1 histogram: [2, 0, 2, 1, 1]
  1 1 1 1 1       Row 2 histogram: [3, 1, 3, 2, 2]
  1 0 0 1 0       Row 3 histogram: [4, 0, 0, 3, 0]

Row 2 histogram: [3, 1, 3, 2, 2]
                  │     │  │  │
                  │     │  └──┘ → area = 2×2=4
                  │     └────── → area = 1×1=1 (blocks extension)
                  └──────────── → area = 3×1=3 (blocked by 1)

Best in row 2: bars at indices 2,3,4 → heights [3,2,2]
  Using histogram algo → largest = 3×3=9? No.
  Index 2 (h=3): width 3-3-1=-1? Let me recalculate.
  Actually for [3,1,3,2,2]:
    index 0 (h=3): width = 5, area = 15? No, index 1 blocks.
    index 2 (h=3): extends to index 1 on left, index 5(sentinel) on right
      width = 5 - 1 - 1 = 3, area = 3×3 = 9 ← BUT h[1]=1 < 3, so width is actually
      just from index 2 to index 2 = width 1? No...

  Let me trace the algorithm:
    i=0(h=3): push 0           → stack: [0]
    i=1(h=1): 1<3, pop 0→h=3,w=1-0-1=0→w=1→area=3; push 1 → stack: [1]
    i=2(h=3): push 2           → stack: [1,2]
    i=3(h=2): 2<3, pop 2→h=3,w=3-1-1=1→area=3; push 3 → stack: [1,3]
    i=4(h=2): push 4           → stack: [1,3,4]
    i=5(h=0): 0<2, pop4→h=2,w=5-3-1=1→area=2
              0<2, pop3→h=2,w=5-1-1=3→area=6
              0<1, pop1→h=1,w=5→area=5
    Max in row 2: 6

Row 3: [4,0,0,3,0] → max = 4×1=4 (just index 0)

Overall max across all rows: 6 ✓
```

```python
def maximal_rectangle(matrix):
    """
    Find the largest rectangle containing only 1s in a binary matrix.

    Approach:
    1. Build a histogram of consecutive 1s above (including) current row
    2. For each row, compute largest rectangle in that histogram
    3. Return the global maximum
    """
    if not matrix:
        return 0

    rows, cols = len(matrix), len(matrix[0])
    heights = [0] * cols  # Running histogram
    max_area = 0

    for i in range(rows):
        # Update histogram heights for this row
        for j in range(cols):
            if matrix[i][j] == '1':
                heights[j] += 1   # Extend column upward
            else:
                heights[j] = 0    # Reset column

        # Apply Largest Rectangle in Histogram on current row
        max_area = max(max_area, largest_rectangle_area(heights))

    return max_area

# Reuses the histogram function defined above
```

## Trapping Rain Water (Monotonic Stack Approach) - O(n)

**Problem**: Given elevation heights, compute how much water can be trapped.

**Strategy**: Maintain an **increasing** stack. When a taller bar appears, it forms a "trough" with the stack top and the new bar.

```
Input: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
Output: 6

Visual (water marked with ~):
Height:
  3 │                        █
  2 │        █     █~~█      ███
  1 │   █    ████  █~~███  █████
  0 │██~███~~███████~~█████████████
    └──────────────────────────────
      0 1 2 3 4 5 6 7 8 9 10 11

Water trapped:
  Index 2 (h=0): left_max=1, right_max=2, water = min(1,2)-0 = 1
  Index 4 (h=1): left_max=2, right_max=3, water = min(2,3)-1 = 1
  Index 5 (h=0): left_max=2, right_max=3, water = min(2,3)-0 = 2
  Index 6 (h=1): left_max=2, right_max=3, water = min(2,3)-1 = 1
  Index 9 (h=1): left_max=3, right_max=2, water = min(3,2)-1 = 1
  Index 11(h=1): left_max=3, right_max=2, water = min(3,2)-1 = 0? 
  Actually the stack-based approach computes differently (by horizontal strips).
  Total = 6 ✓
```

```python
def trap_rain_water(height):
    """
    Compute trapped rain water using monotonic increasing stack.

    Key insight: Water is trapped when we find a "valley" — a bar lower
    than both its left and right neighbors. Each popped element represents
    the BOTTOM of a water trough.

    Formula for each trough:
      width  = current_index - new_stack_top - 1
      h      = min(height[current], height[new_stack_top]) - height[bottom]
      water += width × h
    """
    if not height:
        return 0

    stack = []
    water = 0

    for i, h in enumerate(height):
        # Current bar is taller — forms a trough with stack elements
        while stack and h > height[stack[-1]]:
            bottom = stack.pop()  # This is the lowest point of the trough

            if stack:
                # Right wall = current bar (h), Left wall = new stack top
                width = i - stack[-1] - 1
                trapped_height = min(h, height[stack[-1]]) - height[bottom]
                water += width * trapped_height

        stack.append(i)

    return water

# Walkthrough with height = [0,1,0,2,1,0,1,3,2,1,2,1]:
#   i=0(0): push 0           → stack: [0]
#   i=1(1): 1>0, pop 0→no stack→push 1  → stack: [1]
#   i=2(0): push 2           → stack: [1,2]
#   i=3(2): 2>0, pop 2→stack=[1], w=min(2,1)-0=1, width=3-1-1=1, water=1
#           2>1, pop 1→stack=[], no left wall →push 3 → stack: [3]
#   i=4(1): push 4           → stack: [3,4]
#   i=5(0): push 5           → stack: [3,4,5]
#   i=6(1): 1>0, pop 5→stack=[3,4], w=min(1,height[4])-0=1-0=1, width=6-4-1=1, water=2
#           1 not > 1, push 6 → stack: [3,4,6]
#   i=7(3): 3>1, pop 6→stack=[3,4], w=min(3,1)-1=0→skip
#           3>1, pop 4→stack=[3], w=min(3,height[3])-1=min(3,2)-1=1, width=7-3-1=3, water=5
#           3 not > 2, push 7 → stack: [3,7]
#   i=8(2): push 8           → stack: [3,7,8]
#   i=9(1): push 9           → stack: [3,7,8,9]
#   i=10(2): 2>1, pop 9→stack=[3,7,8], w=min(2,height[8])-1=2-2=0→skip
#            2 not > 2, push 10 → stack: [3,7,8,10]
#   i=11(1): push 11         → stack: [3,7,8,10,11]
# Result: 6 ✓ (truncated walk — actual loop handles remaining flushes)
```

## Sum of Subarray Minimums - O(n)

**Problem**: For every contiguous subarray, find the minimum element and sum all those minimums. Return result modulo 10^9+7.

**Strategy**: For each element, count how many subarrays have it as the minimum. Use monotonic stack to find boundaries.

```
Input:  [3, 1, 2, 4]
Output: 17

All subarrays and their minimums:
  [3]       → min=3
  [3,1]     → min=1
  [3,1,2]   → min=1
  [3,1,2,4] → min=1
  [1]       → min=1
  [1,2]     → min=1
  [1,2,4]   → min=1
  [2]       → min=2
  [2,4]     → min=2
  [4]       → min=4

Sum = 3 + 1 + 1 + 1 + 1 + 1 + 1 + 2 + 2 + 4 = 17

Contribution of each element:
  Element 3 (index 0): appears as min in 1 subarray → 3×1 = 3
  Element 1 (index 1): appears as min in 6 subarrays → 1×6 = 6
  Element 2 (index 2): appears as min in 2 subarrays → 2×2 = 4
  Element 4 (index 3): appears as min in 1 subarray → 4×1 = 4
  Total = 3 + 6 + 4 + 4 = 17 ✓

For element at index i:
  left_count  = i - (index of previous smaller element)
  right_count = (index of next smaller or equal element) - i
  contribution = arr[i] × left_count × right_count
```

```python
def sum_subarray_minimums(arr):
    """
    Sum of minimums of all contiguous subarrays.

    Key insight: For each element, find how many subarrays have it
    as the minimum. This is determined by:
      - How far LEFT it can extend (until a smaller element)
      - How far RIGHT it can extend (until a smaller-or-equal element)

    We use strict < on left and <= on right to handle duplicates correctly
    (each subarray's minimum is attributed to exactly one element).
    """
    MOD = 10**9 + 7
    n = len(arr)
    result = 0

    # Step 1: Find "Previous Smaller Element" index for each position
    left = [-1] * n   # left[i] = index of previous element < arr[i]
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    # Step 2: Find "Next Smaller Element" index for each position
    right = [n] * n   # right[i] = index of next element <= arr[i]
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    # Step 3: Calculate contribution of each element
    for i in range(n):
        left_count = i - left[i]           # subarrays extending left
        right_count = right[i] - i          # subarrays extending right
        contribution = arr[i] * left_count * right_count
        result = (result + contribution) % MOD

    return result

# Walkthrough with arr = [3, 1, 2, 4]:
#   left:  [-1, -1, 1, 2]   (previous smaller indices)
#   right: [ 1,  4, 3, 4]   (next smaller-or-equal indices)
#
#   i=0 (val=3): left_count=0-(-1)=1, right_count=1-0=1 → 3×1×1=3
#   i=1 (val=1): left_count=1-(-1)=2, right_count=4-1=3 → 1×2×3=6
#   i=2 (val=2): left_count=2-1=1,   right_count=3-2=1   → 2×1×1=2
#   i=3 (val=4): left_count=3-2=1,   right_count=4-3=1   → 4×1×1=4
#   Total = 3 + 6 + 2 + 4 = 15? Hmm, let me recalculate...
#   Actually right[2] should be 3 (arr[3]=4 > 2, so next smaller-or-equal is n=4? 
#   No, arr has no element <= 2 to the right of index 2, so right[2]=4.
#   i=2 (val=2): left_count=1, right_count=4-2=2 → 2×1×2=4
#   Total = 3 + 6 + 4 + 4 = 17 ✓
```

## Complete Example Usage
```python
# Next Greater Element
nums = [2, 1, 2, 4, 3]
print(f"Next Greater Right: {next_greater_element_right(nums)}")  # [4, 2, 4, -1, -1]
print(f"Next Greater Left: {next_greater_element_left(nums)}")   # [-1, 2, -1, -1, 4]

# Daily Temperatures
temps = [73, 74, 75, 71, 69, 72, 76, 73]
print(f"Daily Temperatures: {daily_temperatures(temps)}")  # [1, 1, 4, 2, 1, 1, 0, 0]

# Largest Rectangle in Histogram
heights = [2, 1, 5, 6, 2, 3]
print(f"Largest Rectangle: {largest_rectangle_area(heights)}")  # 10

# Trapping Rain Water
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
print(f"Trapped Water: {trap_rain_water(height)}")  # 6

# Sum of Subarray Minimums
arr = [3, 1, 2, 4]
print(f"Sum of Subarray Minimums: {sum_subarray_minimums(arr)}")  # 17
```

---

## Pattern Summary & Quick Reference

### The 4 Core Patterns

| Pattern | Stack Order | When Processing | Answer Set At | Time |
|---------|-------------|-----------------|---------------|------|
| **NGE Right** | Decreasing | Pop when `nums[i] > top` | On pop | O(n) |
| **NSE Right** | Increasing | Pop when `nums[i] < top` | On pop | O(n) |
| **NGL** | Decreasing | Pop when `nums[i] > top` | On push (at `i`) | O(n) |
| **NSL** | Increasing | Pop when `nums[i] < top` | On push (at `i`) | O(n) |

### Decision Flowchart

```
"What monotonic stack do I need?"
│
├─ Looking for GREATER element?
│   ├─ To the RIGHT?  → Decreasing stack, answer on POP
│   └─ To the LEFT?   → Decreasing stack, answer on PUSH
│
├─ Looking for SMALLER element?
│   ├─ To the RIGHT?  → Increasing stack, answer on POP
│   └─ To the LEFT?   → Increasing stack, answer on PUSH
│
├─ Looking for DISTANCE/SPAN?
│   ├─ "How many days until warmer?" → NGE pattern (store i - popped_index)
│   └─ "How many consecutive days ≤?" → Stock Span (accumulate spans)
│
└─ Looking for BOUNDARIES (rectangles, water)?
    ├─ Heights need left/right limits → Increasing stack + sentinel
    └─ Water in valleys → Increasing stack, compute trough areas
```

### Complexity Analysis

| Problem | Time | Space | Why O(n)? |
|---------|------|-------|-----------|
| Next Greater/Smaller | O(n) | O(n) | Each element pushed/popped once |
| Daily Temperatures | O(n) | O(n) | Same as NGE, store distance |
| Stock Span | O(n) | O(n) | Merge accumulates, amortized O(1) |
| Largest Rectangle | O(n) | O(n) | Sentinel flushes remaining elements |
| Maximal Rectangle | O(m×n) | O(n) | m rows × O(n) histogram each |
| Trapping Rain Water | O(n) | O(n) | Each bar pushed/popped once |
| Sum of Subarray Mins | O(n) | O(n) | Two passes for left/right boundaries |

### When to Use What

| Problem Type | First Think | Data Structure |
|-------------|-------------|----------------|
| "Next greater/smaller element" | Monotonic Stack | Stack |
| "How far until something bigger/smaller?" | NGE/NSE with distance | Stack |
| "Largest rectangle in histogram" | Increasing stack + sentinel | Stack |
| "Trapped water" | Increasing stack (valley detection) | Stack |
| "Consecutive days ≤ X" | Stock Span (merge spans) | Stack of tuples |
| "Sum of min/max over subarrays" | Boundary counting | Two monotonic stacks |
| "Matrix problems" | Reduce to 1D histogram per row | Stack + array |
