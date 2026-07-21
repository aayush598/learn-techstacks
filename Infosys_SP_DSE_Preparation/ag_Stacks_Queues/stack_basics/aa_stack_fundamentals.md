# Stack Fundamentals

## Stack Implementation Using List
```python
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def __str__(self):
        return str(self.items)
```

## Stack Using collections.deque - O(1) for all operations
```python
from collections import deque

class StackDeque:
    def __init__(self):
        self.items = deque()
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
```

## Stack Operations Summary
```python
# All operations are O(1)
stack = []
stack.append(1)      # push - O(1)
stack.append(2)      # push - O(1)
stack.pop()          # pop - O(1)
stack[-1]            # peek - O(1)
len(stack) == 0      # isEmpty - O(1)
len(stack)           # size - O(1)
```

## Balanced Parentheses Problems

### Basic Valid Parentheses
```python
def is_valid_parentheses(s):
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

# Test
print(is_valid_parentheses("()[]{}"))  # True
print(is_valid_parentheses("(]"))      # False
print(is_valid_parentheses("([)]"))    # False
print(is_valid_parentheses("{[]}"))    # True
```

### Longest Valid Parentheses
```python
def longest_valid_parentheses(s):
    stack = [-1]
    max_length = 0
    
    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                max_length = max(max_length, i - stack[-1])
    
    return max_length
```

## Min Stack (Design) - O(1) for all operations
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val):
        self.stack.append(val)
        
        # Push to min_stack if it's empty or val <= current min
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

# Alternative: Store (val, current_min) tuples
class MinStackTuple:
    def __init__(self):
        self.stack = []
    
    def push(self, val):
        if self.stack:
            current_min = min(val, self.stack[-1][1])
        else:
            current_min = val
        self.stack.append((val, current_min))
    
    def pop(self):
        if not self.stack:
            raise IndexError("Stack is empty")
        return self.stack.pop()[0]
    
    def top(self):
        if not self.stack:
            raise IndexError("Stack is empty")
        return self.stack[-1][0]
    
    def get_min(self):
        if not self.stack:
            raise IndexError("Stack is empty")
        return self.stack[-1][1]
```

## Max Stack (Design) - O(1) for all operations
```python
class MaxStack:
    def __init__(self):
        self.stack = []
        self.max_stack = []
    
    def push(self, val):
        self.stack.append(val)
        
        if not self.max_stack or val >= self.max_stack[-1]:
            self.max_stack.append(val)
    
    def pop(self):
        if not self.stack:
            raise IndexError("Stack is empty")
        
        val = self.stack.pop()
        
        if val == self.max_stack[-1]:
            self.max_stack.pop()
        
        return val
    
    def top(self):
        if not self.stack:
            raise IndexError("Stack is empty")
        return self.stack[-1]
    
    def get_max(self):
        if not self.max_stack:
            raise IndexError("Stack is empty")
        return self.max_stack[-1]
```

## Implement Queue Using Stacks - Amortized O(1)
```python
class QueueUsingStacks:
    def __init__(self):
        self.stack_in = []   # For enqueue
        self.stack_out = []  # For dequeue
    
    def enqueue(self, x):
        self.stack_in.append(x)
    
    def dequeue(self):
        if self.stack_out:
            return self.stack_out.pop()
        
        if not self.stack_in:
            raise IndexError("Queue is empty")
        
        # Transfer all elements from stack_in to stack_out
        while self.stack_in:
            self.stack_out.append(self.stack_in.pop())
        
        return self.stack_out.pop()
    
    def peek(self):
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

## Implement Stack Using Queues - O(n) for push
```python
from collections import deque

class StackUsingQueues:
    def __init__(self):
        self.q1 = deque()
        self.q2 = deque()
    
    def push(self, x):
        # Push to q2
        self.q2.append(x)
        
        # Move all elements from q1 to q2
        while self.q1:
            self.q2.append(self.q1.popleft())
        
        # Swap q1 and q2
        self.q1, self.q2 = self.q2, self.q1
    
    def pop(self):
        if not self.q1:
            raise IndexError("Stack is empty")
        return self.q1.popleft()
    
    def top(self):
        if not self.q1:
            raise IndexError("Stack is empty")
        return self.q1[0]
    
    def is_empty(self):
        return len(self.q1) == 0

# Alternative: O(1) push, O(n) pop
class StackUsingQueuesV2:
    def __init__(self):
        self.q = deque()
    
    def push(self, x):
        self.q.append(x)
        
        # Rotate to make last element front
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())
    
    def pop(self):
        if not self.q:
            raise IndexError("Stack is empty")
        return self.q.popleft()
    
    def top(self):
        if not self.q:
            raise IndexError("Stack is empty")
        return self.q[0]
    
    def is_empty(self):
        return len(self.q) == 0
```

## Evaluate Postfix Expression - O(n)
```python
def evaluate_postfix(expression):
    stack = []
    operators = {'+', '-', '*', '/'}
    
    for token in expression.split():
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
                # Integer division with truncation toward zero
                stack.append(int(a / b))
    
    return stack[0]

# Test
print(evaluate_postfix("2 1 + 3 *"))  # 9
print(evaluate_postfix("4 13 5 / +"))  # 6
```

## Infix to Postfix Conversion - O(n)
```python
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    right_associative = {'^'}
    
    stack = []
    output = []
    tokens = expression.split()
    
    for token in tokens:
        if token.isalnum():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Remove '('
        else:
            while (stack and stack[-1] != '(' and
                   (stack[-1] in precedence and
                    (precedence[stack[-1]] > precedence[token] or
                     (precedence[stack[-1]] == precedence[token] and
                      token not in right_associative)))):
                output.append(stack.pop())
            stack.append(token)
    
    while stack:
        output.append(stack.pop())
    
    return ' '.join(output)

# Test
print(infix_to_postfix("A + B * C"))  # A B C * +
print(infix_to_postfix("( A + B ) * C"))  # A B + C *
print(infix_to_postfix("A + B * C - D / E"))  # A B C * + D E / -
```

## Complete Example Usage
```python
# Stack operations
stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)
print(f"Stack: {stack}")          # [1, 2, 3]
print(f"Peek: {stack.peek()}")    # 3
print(f"Pop: {stack.pop()}")      # 3
print(f"Size: {stack.size()}")    # 2

# Min stack
min_stack = MinStack()
min_stack.push(5)
min_stack.push(3)
min_stack.push(7)
min_stack.push(1)
print(f"Min: {min_stack.get_min()}")  # 1
min_stack.pop()
print(f"Min: {min_stack.get_min()}")  # 3

# Queue using stacks
queue = QueueUsingStacks()
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
print(f"Dequeue: {queue.dequeue()}")  # 1
print(f"Peek: {queue.peek()}")        # 2

# Evaluate postfix
print(f"Postfix: {evaluate_postfix('2 1 + 3 *')}")  # 9

# Infix to postfix
print(f"Postfix: {infix_to_postfix('A + B * C')}")  # A B C * +
```
