# Stack Fundamentals - Complete Guide

## What is a Stack?

A stack is a **Last-In-First-Out (LIFO)** data structure. Think of a stack of plates:
- You add plates to the TOP
- You remove plates from the TOP
- The last plate added is the first one removed

### Visual: Stack Operations

```
push(1):     push(2):     push(3):     pop():
             
   [1]          [2]          [3]        Remove 3
                [1]          [2]        
                             [1]        [2]
                                        [1]

Stack: LIFO (Last In, First Out)
```

---

## Stack Implementation

### Using Python List

```python
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)  # Add to end
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()  # Remove from end
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]  # Look at end
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
```

### Quick Stack Operations (Python)

```python
# All operations are O(1)
stack = []
stack.append(1)      # push - O(1)
stack.append(2)      # push - O(1)
stack.pop()          # pop - O(1)
stack[-1]            # peek - O(1)
len(stack) == 0      # isEmpty - O(1)
```

---

## Problem 1: Valid Parentheses (LeetCode 20)

**Statement:** Given a string containing just characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

**Constraints:**
- Open brackets must be closed by same type
- Open brackets must be closed in correct order
- Every close bracket has corresponding open bracket

**Example:**
```
Input: s = "()[]{}"
Output: true
Explanation: All brackets are properly matched.

Input: s = "(]"
Output: false
Explanation: '(' is closed by ']', which is wrong type.
```

### Approach: Stack

**Key Insight:** When we see an opening bracket, push it. When we see a closing bracket, check if it matches the top of stack.

### Step-by-Step Walkthrough:

```
s = "({[]})"

Step 1: '(' → push to stack
        Stack: ['(']

Step 2: '{' → push to stack
        Stack: ['(', '{']

Step 3: '[' → push to stack
        Stack: ['(', '{', '[']

Step 4: ']' → closing bracket
        Top of stack = '[' (matches!)
        Pop '['
        Stack: ['(', '{']

Step 5: '}' → closing bracket
        Top of stack = '{' (matches!)
        Pop '{'
        Stack: ['(']

Step 6: ')' → closing bracket
        Top of stack = '(' (matches!)
        Pop '('
        Stack: []

Stack is empty → All matched! ✓
```

### Visual:

```
s = "({[]})"

Position:  0  1  2  3  4  5
Char:      (  {  [  ]  }  )

Stack evolution:
After '(':     ['(']
After '{':     ['(', '{']
After '[':     ['(', '{', '[']
After ']':     ['(', '{']     ← popped '['
After '}':     ['(']          ← popped '{'
After ')':     []             ← popped '('

Empty stack at end → Valid! ✓
```

### The Code:
```python
def is_valid_parentheses(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            # It's a closing bracket
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            # It's an opening bracket
            stack.append(char)
    
    return len(stack) == 0

# Test
print(is_valid_parentheses("()[]{}"))  # True
print(is_valid_parentheses("(]"))      # False
print(is_valid_parentheses("([)]"))    # False
print(is_valid_parentheses("{[]}"))    # True
```

**Time:** O(n) | **Space:** O(n)

---

## Problem 2: Min Stack (Design)

**Statement:** Design a stack that supports push, pop, top, and getMin in O(1) time.

**Example:**
```
MinStack.push(-2) → stack: [-2], min: -2
MinStack.push(0) → stack: [-2, 0], min: -2
MinStack.push(-3) → stack: [-2, 0, -3], min: -3
MinStack.getMin() → returns -3
MinStack.pop() → stack: [-2, 0], min: -2
MinStack.top() → returns 0
MinStack.getMin() → returns -2
```

### Approach: Two Stacks

**Key Insight:** Keep a separate stack that tracks the minimum at each level.

### Visual:

```
push(-2):
  stack: [-2]
  min_stack: [-2]
  
push(0):
  stack: [-2, 0]
  min_stack: [-2]  (0 > -2, don't push to min_stack)
  
push(-3):
  stack: [-2, 0, -3]
  min_stack: [-2, -3]  (-3 <= -2, push to min_stack)
  
getMin(): return min_stack[-1] = -3

pop():
  stack: [-2, 0]
  min_stack: [-2]  (removed -3 from min_stack)
  
getMin(): return min_stack[-1] = -2
```

### The Code:
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
```

**Time:** O(1) for all operations | **Space:** O(n)

---

## Problem 3: Evaluate Postfix Expression

**Statement:** Evaluate arithmetic expression in postfix (Reverse Polish Notation).

**Example:**
```
Input: "2 1 + 3 *"
Output: 9
Explanation: ((2 + 1) × 3) = 9

Input: "4 13 5 / +"
Output: 6
Explanation: (4 + (13 / 5)) = 4 + 2 = 6
```

### Approach: Stack

**Key Insight:** When we see a number, push it. When we see an operator, pop two numbers, apply operator, push result.

### Step-by-Step Walkthrough:

```
Expression: "2 1 + 3 *"

Step 1: '2' → push 2
        Stack: [2]

Step 2: '1' → push 1
        Stack: [2, 1]

Step 3: '+' → pop 1 and 2, compute 2+1=3, push 3
        Stack: [3]

Step 4: '3' → push 3
        Stack: [3, 3]

Step 5: '*' → pop 3 and 3, compute 3×3=9, push 9
        Stack: [9]

Result: 9 ✓
```

### Visual:

```
"2 1 + 3 *"

  2   1   +   3   *
  ↓   ↓   ↓   ↓   ↓
 [2] [2,1] [3] [3,3] [9]
           ↑
     2+1 = 3
           ↑
     3×3 = 9
```

### The Code:
```python
def evaluate_postfix(expression):
    stack = []
    operators = {'+', '-', '*', '/'}
    
    for token in expression.split():
        if token not in operators:
            stack.append(int(token))
        else:
            b = stack.pop()  # Second operand
            a = stack.pop()  # First operand
            
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(int(a / b))  # Truncate toward zero
    
    return stack[0]

# Test
print(evaluate_postfix("2 1 + 3 *"))  # 9
print(evaluate_postfix("4 13 5 / +"))  # 6
```

**Time:** O(n) | **Space:** O(n)

---

## Problem 4: Implement Queue Using Stacks

**Statement:** Implement a FIFO queue using only two stacks.

### Key Insight:

```
Stack: LIFO (Last In, First Out)
Queue: FIFO (First In, First Out)

To simulate queue with stacks:
- Use stack_in for enqueue (push)
- Use stack_out for dequeue (pop)
- When stack_out is empty, transfer all from stack_in to stack_out
```

### Visual:

```
Enqueue 1, 2, 3:
  stack_in: [1, 2, 3]
  stack_out: []

Dequeue():
  stack_out is empty, transfer!
  stack_in: []
  stack_out: [3, 2, 1]  (reversed!)
  
  Pop from stack_out: 1 ✓ (FIFO!)

Dequeue():
  stack_out: [3, 2]
  Pop: 2 ✓

Enqueue 4:
  stack_in: [4]
  stack_out: [3, 2]

Dequeue():
  stack_out not empty, pop from it
  Pop: 3 ✓
```

### The Code:
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

**Time:** O(1) amortized | **Space:** O(n)

---

## Problem 5: Infix to Postfix Conversion

**Statement:** Convert infix expression (A + B × C) to postfix (A B C × +).

### Precedence Rules:
```
^ (power) > * / > + -
Same precedence: left to right (except ^ which is right to left)
```

### Step-by-Step Walkthrough:

```
Infix: "A + B * C"

Step 1: 'A' → output
        Output: "A"
        
Step 2: '+' → push to stack
        Stack: ['+']
        
Step 3: 'B' → output
        Output: "A B"
        
Step 4: '*' → push (higher precedence than +)
        Stack: ['+', '*']
        
Step 5: 'C' → output
        Output: "A B C"
        
Step 6: End → pop all from stack
        Pop '*' → Output: "A B C *"
        Pop '+' → Output: "A B C * +"

Result: "A B C * +"
```

### Visual:

```
Infix: A + B * C

Output: A B C * +
        ↑ ↑ ↑ ↑ ↑
        A B C * +
              ↑
        * has higher precedence than +
        so * is applied first in postfix
```

### The Code:
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
```

**Time:** O(n) | **Space:** O(n)

---

## Quick Reference

| Operation | Time | Space |
|-----------|------|-------|
| push | O(1) | O(1) |
| pop | O(1) | O(1) |
| peek | O(1) | O(1) |
| isEmpty | O(1) | O(1) |
| Valid Parentheses | O(n) | O(n) |
| Min Stack | O(1) all | O(n) |
| Evaluate Postfix | O(n) | O(n) |
| Queue using Stacks | O(1) amortized | O(n) |
| Infix to Postfix | O(n) | O(n) |

## When to Use Stack

1. **Balanced parentheses** - matching brackets
2. **Undo/Redo** - last operation first
3. **Function calls** - recursion stack
4. **Expression evaluation** - postfix/prefix
5. **Monotonic stack** - next greater/smaller element
6. **DFS traversal** - explicit stack
