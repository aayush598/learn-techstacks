# Queue and Deque Fundamentals

## Queue Implementation Using collections.deque - O(1) for all operations
```python
from collections import deque

class Queue:
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items.popleft()
    
    def peek(self):
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
```python
class QueueTwoStacks:
    def __init__(self):
        self.stack_in = []
        self.stack_out = []
    
    def enqueue(self, item):
        self.stack_in.append(item)
    
    def dequeue(self):
        if self.stack_out:
            return self.stack_out.pop()
        
        if not self.stack_in:
            raise IndexError("Queue is empty")
        
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

## Circular Queue - O(1)
```python
class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0
    
    def enqueue(self, item):
        if self.is_full():
            raise IndexError("Queue is full")
        
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = item
        self.size += 1
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        
        item = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.capacity
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
```python
import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.index = 0
    
    def push(self, item, priority):
        heapq.heappush(self.heap, (-priority, self.index, item))
        self.index += 1
    
    def pop(self):
        if not self.heap:
            raise IndexError("Priority queue is empty")
        return heapq.heappop(self.heap)[2]
    
    def peek(self):
        if not self.heap:
            raise IndexError("Priority queue is empty")
        return self.heap[0][2]
    
    def is_empty(self):
        return len(self.heap) == 0

# Simple priority queue with tuples
class SimplePriorityQueue:
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

# Example: nums = [1,3,-1,-3,5,3,6,7], k = 3 -> [3,3,5,5,6,7]
```

## Sliding Window Minimum Using Deque - O(n)
```python
from collections import deque

def min_sliding_window(nums, k):
    result = []
    dq = deque()  # Stores indices of potential minimums
    
    for i in range(len(nums)):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove larger elements from back
        while dq and nums[dq[-1]] > nums[i]:
            dq.pop()
        
        dq.append(i)
        
        # Add to result when window is complete
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

# Example: nums = [1,3,-1,-3,5,3,6,7], k = 3 -> [-1,-3,-3,-3,3,3]
```

## First Unique Character in a Stream - O(n) per character
```python
from collections import deque, Counter

class StreamChecker:
    def __init__(self):
        self.queue = deque()
        self.count = Counter()
    
    def add_char(self, char):
        self.queue.append(char)
        self.count[char] += 1
        
        # Remove unique characters from front
        while self.queue and self.count[self.queue[0]] > 1:
            self.queue.popleft()
        
        return self.queue[0] if self.queue else '#'

# Example
sc = StreamChecker()
print(sc.add_char('a'))  # 'a'
print(sc.add_char('b'))  # 'a'
print(sc.add_char('a'))  # 'b'
print(sc.add_char('b'))  # '#'
print(sc.add_char('c'))  # 'c'
```

## Number of Visible People in a Queue - O(n)
```python
def can_see_persons_count(heights):
    n = len(heights)
    result = [0] * n
    stack = []
    
    for i in range(n):
        # People that current person can see
        while stack and heights[stack[-1]] < heights[i]:
            result[stack.pop()] += 1
        
        # Current person blocks view of stack top
        if stack:
            result[stack[-1]] += 1
        
        stack.append(i)
    
    return result

# Example: heights = [10,6,8,5,11,9] -> [3,1,2,1,1,0]
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

## Queue vs Deque vs Priority Queue

| Feature | Queue | Deque | Priority Queue |
|---------|-------|-------|----------------|
| Add to back | O(1) | O(1) | O(log n) |
| Add to front | O(n) | O(1) | N/A |
| Remove from front | O(1) | O(1) | O(log n) |
| Remove from back | O(n) | O(1) | O(log n) |
| Peek | O(1) | O(1) | O(1) |
| Use case | FIFO | Both ends | Priority-based |
