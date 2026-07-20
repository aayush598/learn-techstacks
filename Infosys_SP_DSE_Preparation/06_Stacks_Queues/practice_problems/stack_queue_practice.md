# Stack and Queue Practice Problems

## Easy Problems

### 1. Valid Parentheses
**Problem**: Given a string containing just '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

**Approach**: Use stack to match opening and closing brackets.

**Solution**:
```python
def is_valid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    
    return len(stack) == 0
```

**Complexity**: O(n) time, O(n) space

---

### 2. Min Stack
**Problem**: Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

**Approach**: Use two stacks - one for values, one for minimums.

**Solution**:
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self):
        if not self.stack:
            raise IndexError("Stack is empty")
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()
        return val
    
    def top(self):
        if not self.stack:
            raise IndexError("Stack is empty")
        return self.stack[-1]
    
    def get_min(self):
        if not self.min_stack:
            raise IndexError("Stack is empty")
        return self.min_stack[-1]
```

**Complexity**: O(1) for all operations

---

### 3. Implement Queue using Stacks
**Problem**: Implement a FIFO queue using only two stacks.

**Approach**: Use two stacks - one for enqueue, one for dequeue.

**Solution**:
```python
class MyQueue:
    def __init__(self):
        self.stack_in = []
        self.stack_out = []
    
    def push(self, x):
        self.stack_in.append(x)
    
    def pop(self):
        self.peek()
        return self.stack_out.pop()
    
    def peek(self):
        if not self.stack_out:
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

**Approach**: Use stack to handle special operations.

**Solution**:
```python
def cal_points(operations):
    stack = []
    
    for op in operations:
        if op == '+':
            stack.append(stack[-1] + stack[-2])
        elif op == 'D':
            stack.append(2 * stack[-1])
        elif op == 'C':
            stack.pop()
        else:
            stack.append(int(op))
    
    return sum(stack)
```

**Complexity**: O(n) time, O(n) space

---

### 5. Crawler Log Folder
**Problem**: Return the minimum number of operations to go back to the main folder.

**Approach**: Use stack to track folder changes.

**Solution**:
```python
def min_operations(logs):
    stack = []
    
    for log in logs:
        if log == '../':
            if stack:
                stack.pop()
        elif log != './':
            stack.append(log)
    
    return len(stack)
```

**Complexity**: O(n) time, O(n) space

---

## Medium Problems

### 6. Daily Temperatures
**Problem**: Given an array of temperatures, return an array where answer[i] is the number of days you have to wait to get a warmer temperature.

**Approach**: Use monotonic decreasing stack.

**Solution**:
```python
def daily_temperatures(temperatures):
    n = len(temperatures)
    result = [0] * n
    stack = []  # Stack of indices
    
    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev_day = stack.pop()
            result[prev_day] = i - prev_day
        stack.append(i)
    
    return result
```

**Complexity**: O(n) time, O(n) space

---

### 7. Stock Span Problem
**Problem**: The span of the stock's price today is defined as the maximum number of consecutive days for which the price was less than or equal to today's price.

**Approach**: Use monotonic stack to track spans.

**Solution**:
```python
def calculate_span(prices):
    n = len(prices)
    result = [0] * n
    stack = []  # Stack of (price, span)
    
    for i in range(n):
        span = 1
        
        while stack and prices[i] >= stack[-1][0]:
            span += stack[-1][1]
            stack.pop()
        
        stack.append((prices[i], span))
        result[i] = span
    
    return result
```

**Complexity**: O(n) time, O(n) space

---

### 8. Evaluate Reverse Polish Notation
**Problem**: Evaluate the value of an arithmetic expression in Reverse Polish Notation.

**Approach**: Use stack to store operands.

**Solution**:
```python
def eval_rpn(tokens):
    stack = []
    operators = {'+', '-', '*', '/'}
    
    for token in tokens:
        if token not in operators:
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(int(a / b))
    
    return stack[0]
```

**Complexity**: O(n) time, O(n) space

---

### 9. Simplify Path
**Problem**: Given a string path, which is an absolute path starting with '/', simplify it.

**Approach**: Use stack to track directory changes.

**Solution**:
```python
def simplify_path(path):
    stack = []
    components = path.split('/')
    
    for component in components:
        if component == '..':
            if stack:
                stack.pop()
        elif component and component != '.':
            stack.append(component)
    
    return '/' + '/'.join(stack)
```

**Complexity**: O(n) time, O(n) space

---

### 10. Decode String
**Problem**: Given an encoded string, return its decoded string.

**Approach**: Use two stacks - one for counts, one for strings.

**Solution**:
```python
def decode_string(s):
    stack_count = []
    stack_string = []
    current_string = ""
    current_num = 0
    
    for char in s:
        if char.isdigit():
            current_num = current_num * 10 + int(char)
        elif char == '[':
            stack_count.append(current_num)
            stack_string.append(current_string)
            current_string = ""
            current_num = 0
        elif char == ']':
            count = stack_count.pop()
            prev_string = stack_string.pop()
            current_string = prev_string + current_string * count
        else:
            current_string += char
    
    return current_string
```

**Complexity**: O(n) time, O(n) space

---

## Hard Problems

### 11. Largest Rectangle in Histogram
**Problem**: Given n non-negative integers representing the histogram's bar height, find the area of the largest rectangle.

**Approach**: Use monotonic stack to find left and right boundaries.

**Solution**:
```python
def largest_rectangle_area(heights):
    stack = []
    max_area = 0
    n = len(heights)
    
    for i in range(n + 1):
        current_height = heights[i] if i < n else 0
        
        while stack and current_height < heights[stack[-1]]:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        
        stack.append(i)
    
    return max_area
```

**Complexity**: O(n) time, O(n) space

---

### 12. Maximal Rectangle
**Problem**: Given a 2D binary matrix filled with 0s and 1s, find the largest rectangle containing only 1s.

**Approach**: Convert to histogram problem for each row.

**Solution**:
```python
def maximal_rectangle(matrix):
    if not matrix:
        return 0
    
    rows, cols = len(matrix), len(matrix[0])
    heights = [0] * cols
    max_area = 0
    
    for i in range(rows):
        # Update heights
        for j in range(cols):
            if matrix[i][j] == '1':
                heights[j] += 1
            else:
                heights[j] = 0
        
        # Calculate largest rectangle in histogram
        max_area = max(max_area, largest_rectangle_area(heights))
    
    return max_area

def largest_rectangle_area(heights):
    stack = []
    max_area = 0
    n = len(heights)
    
    for i in range(n + 1):
        current_height = heights[i] if i < n else 0
        
        while stack and current_height < heights[stack[-1]]:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        
        stack.append(i)
    
    return max_area
```

**Complexity**: O(m * n) time, O(n) space

---

### 13. Trapping Rain Water
**Problem**: Given n non-negative integers representing an elevation map, compute how much water it can trap.

**Approach**: Use monotonic stack to find water trapped.

**Solution**:
```python
def trap(height):
    if not height:
        return 0
    
    stack = []
    water = 0
    
    for i, h in enumerate(height):
        while stack and h > height[stack[-1]]:
            bottom = stack.pop()
            
            if stack:
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

**Approach**: Use deque to maintain potential maximums.

**Solution**:
```python
from collections import deque

def max_sliding_window(nums, k):
    result = []
    dq = deque()  # Stores indices of potential maximums
    
    for i in range(len(nums)):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements from back
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        dq.append(i)
        
        # Add to result when window is complete
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result
```

**Complexity**: O(n) time, O(k) space

---

### 15. Car Fleet
**Problem**: There are n cars going to the same destination. A car fleet is a non-empty set of cars driving at the same speed. Return the number of car fleets.

**Approach**: Sort by position, use stack to track fleets.

**Solution**:
```python
def car_fleet(target, position, speed):
    n = len(position)
    cars = sorted(zip(position, speed), reverse=True)
    stack = []
    
    for pos, spd in cars:
        time = (target - pos) / spd
        
        if not stack or time > stack[-1]:
            stack.append(time)
    
    return len(stack)
```

**Complexity**: O(n log n) time, O(n) space

---

## Summary Table

| # | Problem | Difficulty | Time | Space |
|---|---------|------------|------|-------|
| 1 | Valid Parentheses | Easy | O(n) | O(n) |
| 2 | Min Stack | Easy | O(1) | O(n) |
| 3 | Queue using Stacks | Easy | O(1)* | O(n) |
| 4 | Baseball Game | Easy | O(n) | O(n) |
| 5 | Crawler Log Folder | Easy | O(n) | O(n) |
| 6 | Daily Temperatures | Medium | O(n) | O(n) |
| 7 | Stock Span | Medium | O(n) | O(n) |
| 8 | Evaluate RPN | Medium | O(n) | O(n) |
| 9 | Simplify Path | Medium | O(n) | O(n) |
| 10 | Decode String | Medium | O(n) | O(n) |
| 11 | Largest Rectangle | Hard | O(n) | O(n) |
| 12 | Maximal Rectangle | Hard | O(m*n) | O(n) |
| 13 | Trapping Rain Water | Hard | O(n) | O(n) |
| 14 | Sliding Window Max | Hard | O(n) | O(k) |
| 15 | Car Fleet | Hard | O(n log n) | O(n) |

*Amortized O(1)
