# Lists and Tuples in Python — Complete Guide for CP

## 1. List Creation

```python
# Empty list
empty = []
empty = list()

# From values
nums = [1, 2, 3, 4, 5]

# From string
chars = list("hello")  # ['h', 'e', 'l', 'l', 'o']

# From range
nums = list(range(1, 11))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Repeat
zeros = [0] * 5           # [0, 0, 0, 0, 0]
ones = [1] * 10           # [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# WARNING: Nested list trap
grid = [[0] * 3] * 3
# This creates 3 references to the SAME list!
grid[0][0] = 1
print(grid)  # [[1, 0, 0], [1, 0, 0], [1, 0, 0]] — ALL rows changed!

# Correct way:
grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 1
print(grid)  # [[1, 0, 0], [0, 0, 0], [0, 0, 0]] — Only first row changed
```

## 2. Indexing and Slicing

```python
arr = [10, 20, 30, 40, 50]

# Positive indexing: 0-based
print(arr[0])    # 10
print(arr[2])    # 30

# Negative indexing
print(arr[-1])   # 50 (last element)
print(arr[-2])   # 40 (second to last)

# Slicing: arr[start:stop:step]
# Includes start, excludes stop
print(arr[1:4])     # [20, 30, 40]
print(arr[0:3])     # [10, 20, 30]
print(arr[:3])      # [10, 20, 30] — same as above
print(arr[2:])      # [30, 40, 50]
print(arr[::2])     # [10, 30, 50] — every 2nd element
print(arr[::-1])    # [50, 40, 30, 20, 10] — reversed

# Slice assignment (modifying in-place)
arr[1:3] = [200, 300]
print(arr)  # [10, 200, 300, 40, 50]

# Insert using slice
arr[1:1] = [15, 25]  # Insert before index 1
print(arr)  # [10, 15, 25, 200, 300, 40, 50]

# Delete using slice
arr[1:3] = []
print(arr)  # [10, 200, 40, 50]
```

## 3. List Methods — Complete Reference

```python
arr = [3, 1, 4, 1, 5, 9]

# ============================================
# Adding Elements
# ============================================
arr.append(2)        # [3, 1, 4, 1, 5, 9, 2] — adds to END
arr.insert(0, 0)     # [0, 3, 1, 4, 1, 5, 9, 2] — inserts at index
arr.extend([6, 7])   # [0, 3, 1, 4, 1, 5, 9, 2, 6, 7]

# extend vs append:
# append adds the argument as a single element
# extend iterates over the argument and adds each element
arr.append([8, 9])   # [0, 3, ..., 7, [8, 9]] — nested list!
arr.extend([8, 9])   # [0, 3, ..., 7, 8, 9] — flat list

# ============================================
# Removing Elements
# ============================================
arr = [3, 1, 4, 1, 5, 9, 2, 6, 7]

arr.remove(1)        # Removes FIRST occurrence of 1 → [3, 4, 1, 5, 9, 2, 6, 7]
arr.pop()            # Removes and returns LAST element → 7
arr.pop(0)           # Removes and returns element at index 0 → 3
del arr[0]           # Removes element at index 0 → [4, 1, 5, 9, 2, 6]
del arr[1:3]         # Removes index 1 and 2 → [4, 9, 2, 6]

arr.clear()          # Empty the list → []

# ============================================
# Searching
# ============================================
arr = [3, 1, 4, 1, 5, 9, 2, 6]
print(arr.index(5))     # 4 (first occurrence index)
print(arr.index(1))     # 1 (first occurrence)
print(arr.count(1))     # 2 (appears 2 times)
print(5 in arr)         # True — O(n) lookup
print(7 in arr)         # False

# ============================================
# Sorting
# ============================================
arr = [3, 1, 4, 1, 5, 9, 2, 6]

# In-place sort (modifies original)
arr.sort()              # [1, 1, 2, 3, 4, 5, 6, 9]
arr.sort(reverse=True)  # [9, 6, 5, 4, 3, 2, 1, 1]

# Custom sort key
words = ["banana", "apple", "cherry"]
words.sort(key=len)     # Sort by length → ['apple', 'banana', 'cherry']
words.sort(key=str.lower)  # Case-insensitive sort

# Sort list of tuples by specific element
pairs = [(1, 'b'), (3, 'a'), (2, 'c')]
pairs.sort(key=lambda x: x[0])  # Sort by first element → [(1,'b'), (2,'c'), (3,'a')]

# Returns new sorted list (doesn't modify original)
new_arr = sorted(arr)

# ============================================
# Other Useful Methods
# ============================================
arr = [1, 2, 3]
arr.reverse()          # [3, 2, 1] — in-place reversal
# OR
arr = arr[::-1]        # Creates new reversed list

arr = [1, 2, 3]
copy = arr.copy()      # Shallow copy
copy = arr[:]          # Also a shallow copy

# List multiplication (shallow copy trap)
a = [[0]] * 3
a[0][0] = 1
print(a)  # [[1], [1], [1]] — ALL sublists changed!

a = [[0] for _ in range(3)]
a[0][0] = 1
print(a)  # [[1], [0], [0]] — Only first changed
```

## 4. List as Stack (LIFO — Last In, First Out)

```python
# Stack: push to top, pop from top
stack = []

# Push
stack.append(1)
stack.append(2)
stack.append(3)
print(stack)  # [1, 2, 3]

# Pop
top = stack.pop()  # Returns 3, stack is [1, 2]
top = stack.pop()  # Returns 2, stack is [1]

# Peek at top (without removing)
top = stack[-1]    # Returns 1

# Check if empty
if not stack:
    print("Stack is empty")

# Stack size
print(len(stack))  # 1

# ============================================
# CP Example: Valid Parentheses
# ============================================
def is_valid(s):
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    
    for ch in s:
        if ch in mapping:
            if not stack or stack[-1] != mapping[ch]:
                return False
            stack.pop()
        else:
            stack.append(ch)
    
    return len(stack) == 0

print(is_valid("()[]{}"))  # True
print(is_valid("(]"))      # False
```

## 5. List as Queue (FIFO — First In, First Out)

```python
from collections import deque

# ============================================
# Using deque for O(1) queue operations
# ============================================
queue = deque()

# Enqueue
queue.append(1)
queue.append(2)
queue.append(3)

# Dequeue
front = queue.popleft()  # Returns 1, queue is deque([2, 3])

# Peek
front = queue[0]  # Returns 2

# ============================================
# WARNING: Don't use list as queue!
# ============================================
# queue = []
# queue.append(1)    # O(1)
# queue.pop(0)       # O(n) — ALL elements shift left!
# This causes TLE in CP. Always use deque.

# ============================================
# CP Example: BFS
# ============================================
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return order

graph = {0: [1, 2], 1: [0, 3], 2: [0, 4], 3: [1], 4: [2]}
print(bfs(graph, 0))  # [0, 1, 2, 3, 4]
```

## 6. Nested Lists (2D Arrays)

```python
# ============================================
# Creating 2D Arrays
# ============================================
# Correct way
n, m = 3, 4
grid = [[0] * m for _ in range(n)]
# [[0, 0, 0, 0],
#  [0, 0, 0, 0],
#  [0, 0, 0, 0]]

# WRONG way (all rows reference same list)
grid = [[0] * m] * n  # Don't do this!

# From input
grid = []
for _ in range(n):
    row = list(map(int, input().split()))
    grid.append(row)

# One-liner
grid = [list(map(int, input().split())) for _ in range(n)]

# ============================================
# Accessing and Traversing
# ============================================
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Access element
print(grid[1][2])  # 6 (row 1, col 2)

# Row-major traversal
for i in range(len(grid)):
    for j in range(len(grid[0])):
        print(grid[i][j], end=" ")
    print()

# Using enumerate
for i, row in enumerate(grid):
    for j, val in enumerate(row):
        print(f"grid[{i}][{j}] = {val}")

# Column-major traversal
for j in range(len(grid[0])):
    for i in range(len(grid)):
        print(grid[i][j], end=" ")
    print()

# ============================================
# Transpose of a Matrix
# ============================================
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# Method 1
transpose = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

# Method 2 (using zip)
transpose = [list(row) for row in zip(*grid)]
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

## 7. Tuple Operations

```python
# ============================================
# Tuple Creation
# ============================================
t = (1, 2, 3)
t = 1, 2, 3          # Parentheses optional
t = tuple([1, 2, 3]) # From list
t = tuple("hello")   # ('h', 'e', 'l', 'l', 'o')

# Single element tuple (note the comma!)
single = (42)     # This is just an int: 42
single = (42,)    # This is a tuple: (42,)

# Empty tuple
empty = ()

# ============================================
# Tuple Unpacking
# ============================================
# Basic unpacking
point = (3, 4)
x, y = point
print(x, y)  # 3 4

# Swap
a, b = b, a

# Star unpacking
first, *middle, last = (1, 2, 3, 4, 5)
# first = 1, middle = [2, 3, 4], last = 5

# Ignore values with _
_, second, _ = (10, 20, 30)
print(second)  # 20

# ============================================
# Tuple Methods
# ============================================
t = (1, 2, 3, 2, 2, 4)
print(t.count(2))  # 3
print(t.index(3))  # 2

# Tuple concatenation
t1 = (1, 2)
t2 = (3, 4)
t3 = t1 + t2  # (1, 2, 3, 4)

# Tuple repetition
t = (0,) * 5  # (0, 0, 0, 0, 0)

# Membership test
print(3 in t)  # True
```

## 8. Tuple vs List — When to Use What

```python
# ============================================
# USE TUPLE when:
# ============================================
# 1. Data shouldn't change (immutable)
coordinates = (40.7128, -74.0060)

# 2. As dictionary keys (lists can't be keys!)
locations = {(40.71, -74.00): "New York", (51.51, -0.13): "London"}

# 3. Return multiple values from function
def get_min_max(arr):
    return min(arr), max(arr)

lo, hi = get_min_max([3, 1, 4, 1, 5, 9])

# 4. Slightly faster iteration and less memory

# ============================================
# USE LIST when:
# ============================================
# 1. Data needs to change
arr = [1, 2, 3]
arr.append(4)
arr[0] = 100

# 2. Need list methods (sort, reverse, etc.)
arr.sort()

# 3. Need to add/remove elements frequently
# ============================================

# In CP: Use tuples as dictionary keys or set elements
# when you need to store pairs/positions
visited = set()
visited.add((0, 0))
visited.add((0, 1))
print((0, 0) in visited)  # True

# Lists for most other things
adj = [[] for _ in range(1000)]  # Adjacency list
```

## 9. List Comprehensions for CP

```python
# ============================================
# Pattern 1: Generate sequence
# ============================================
squares = [x**2 for x in range(1, 11)]
evens = [x for x in range(1, 101) if x % 2 == 0]

# ============================================
# Pattern 2: Filter and transform
# ============================================
words = ["hello", "world", "python", "hi"]
long_words = [w.upper() for w in words if len(w) > 3]
# ['HELLO', 'WORLD', 'PYTHON']

# ============================================
# Pattern 3: Flatten 2D list
# ============================================
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]

# ============================================
# Pattern 4: Build adjacency list
# ============================================
edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
n = 4
adj = [[] for _ in range(n)]
for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)

# ============================================
# Pattern 5: Prefix sums
# ============================================
arr = [1, 2, 3, 4, 5]
prefix = [0] * (len(arr) + 1)
for i in range(len(arr)):
    prefix[i + 1] = prefix[i] + arr[i]
# prefix = [0, 1, 3, 6, 10, 15]
# Range sum [l, r] = prefix[r+1] - prefix[l]
```

## 10. Common List Tricks in CP

```python
# ============================================
# Trick 1: Check if list is sorted
# ============================================
arr = [1, 2, 3, 4, 5]
is_sorted = all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

# ============================================
# Trick 2: Remove duplicates (loses order)
# ============================================
arr = [3, 1, 2, 1, 3, 2, 4]
unique = list(set(arr))  # [1, 2, 3, 4] — order may vary

# Remove duplicates keeping order
unique = list(dict.fromkeys(arr))  # [3, 1, 2, 4]

# ============================================
# Trick 3: Rotation
# ============================================
arr = [1, 2, 3, 4, 5]
k = 2
# Left rotate by k
rotated = arr[k:] + arr[:k]  # [3, 4, 5, 1, 2]

# Right rotate by k
rotated = arr[-k:] + arr[:-k]  # [4, 5, 1, 2, 3]

# ============================================
# Trick 4: Chunking a list
# ============================================
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
chunk_size = 3
chunks = [arr[i:i+chunk_size] for i in range(0, len(arr), chunk_size)]
# [[1,2,3], [4,5,6], [7,8,9]]

# ============================================
# Trick 5: Finding majority element
# ============================================
from collections import Counter
arr = [3, 3, 4, 2, 3, 3, 3, 1]
majority = Counter(arr).most_common(1)[0][0]  # 3

# ============================================
# Trick 6: Running maximum/minimum
# ============================================
arr = [3, 1, 4, 1, 5, 9, 2, 6]
running_max = []
current_max = float('-inf')
for x in arr:
    current_max = max(current_max, x)
    running_max.append(current_max)
# [3, 3, 4, 4, 5, 9, 9, 9]

# ============================================
# Trick 7: Kadane's Algorithm (Max Subarray Sum)
# ============================================
def kadane(arr):
    max_sum = arr[0]
    current_sum = arr[0]
    for i in range(1, len(arr)):
        current_sum = max(arr[i], current_sum + arr[i])
        max_sum = max(max_sum, current_sum)
    return max_sum

print(kadane([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6
```
