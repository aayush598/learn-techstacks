# Python Cheat Sheet for Infosys SP DSE

> Complete reference for all Python operations needed in competitive programming.

## Quick Reference: Python Data Structure Selection

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WHICH DATA STRUCTURE TO USE?                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Need ordered collection + fast access?     → list                  │
│  Need fast lookup + no duplicates?          → set                   │
│  Need key-value mapping?                    → dict                  │
│  Need FIFO queue (fast both ends)?          → deque                 │
│  Need priority ordering?                    → heapq                 │
│  Need frequency counting?                   → Counter               │
│  Need default dict values?                  → defaultdict           │
│  Need to check membership frequently?       → set (O(1) vs O(n))    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Operation Speed Comparison

```
┌──────────────────┬──────────┬──────────┬────────────────────────┐
│ Operation        │ list     │ set/dict │ When to prefer         │
├──────────────────┼──────────┼──────────┼────────────────────────┤
│ Check "x in Y"   │ O(n)     │ O(1)     │ set/dict (100x faster) │
│ Append           │ O(1)     │ O(1)     │ Either                 │
│ Insert at 0      │ O(n)     │ N/A      │ Use deque.appendleft   │
│ Delete at 0      │ O(n)     │ O(1)     │ set/dict               │
│ Find max/min     │ O(n)     │ O(n)     │ Use heapq instead      │
│ Sort             │ O(nlogn) │ N/A      │ list only              │
└──────────────────┴──────────┴──────────┴────────────────────────┘

KEY INSIGHT for CP:
  if "x in collection" appears in inner loop → use set/dict, NOT list!
  This single change can make O(n²) → O(n)
```

## Built-in Functions

### Type Conversion
```python
int(x)          # Convert to integer
float(x)        # Convert to float
str(x)          # Convert to string
list(x)         # Convert to list
tuple(x)        # Convert to tuple
set(x)          # Convert to set
dict(x)         # Convert to dictionary
bool(x)         # Convert to boolean
complex(real, imag)  # Create complex number
```

### Math Operations
```python
abs(x)          # Absolute value
min(a, b, c)    # Minimum value
max(a, b, c)    # Maximum value
sum([1,2,3])    # Sum of iterable
pow(x, y)       # x raised to power y
round(3.14, 1)  # Round to 1 decimal
divmod(7, 2)    # Returns (3, 1) - (quotient, remainder)
```

### Iterables
```python
len(s)          # Length
sorted([3,1,2]) # Returns new sorted list
reversed([1,2]) # Returns reverse iterator
enumerate([a,b])# Returns (index, value) pairs
zip([1,2],[3,4])# Pairs elements from iterables
map(func, iter) # Apply function to all elements
filter(func, iter)# Filter elements
any([0,1,0])    # True if any element is truthy
all([1,1,1])    # True if all elements are truthy
```

### Input/Output
```python
input()         # Read string from input
print(x, y)     # Print with space separator
print(x, end=" ")  # Print without newline
```

---

## String Methods

### Creation and Access

```python
s = "hello"
s = 'hello'
s = """multi
line"""
s[0]            # First character  → 'h'
s[-1]           # Last character   → 'o'
s[1:3]          # Slice (index 1 to 2) → 'el'
s[::2]          # Every other character → 'hlo'
s[::-1]         # Reverse string   → 'olleh'
```

### String Slicing Visual Guide

```
String:   h  e  l  l  o
Index:    0  1  2  3  4
Neg Idx: -5 -4 -3 -2 -1

s[1:4]   → 'ell'    (start at 1, stop before 4)
s[::2]   → 'hlo'    (every 2nd char: 0, 2, 4)
s[::-1]  → 'olleh'  (reverse the string)
s[1:]    → 'ello'   (from index 1 to end)
s[:3]    → 'hel'    (from start to index 2)

CRITICAL for CP:
  String reversal: s[::-1]        → O(n)
  Substring check: s1 in s2       → O(n*m) naive, use KMP for large
  Char count:      s.count('a')   → O(n)
```

### String Methods
```python
s.upper()       # "HELLO"
s.lower()       # "hello"
s.title()       # "Hello"
s.capitalize()  # "Hello"
s.swapcase()    # "HELLO"

s.strip()       # Remove whitespace
s.lstrip()      # Remove left whitespace
s.rstrip()      # Remove right whitespace

s.replace("l", "L")  # Replace all occurrences
s.split(",")    # Split by delimiter
",".join(lst)   # Join list with delimiter

s.find("ll")    # Index of first occurrence (-1 if not found)
s.rfind("l")    # Index of last occurrence
s.count("l")    # Count occurrences

s.startswith("he")  # Check prefix
s.endswith("lo")    # Check suffix

s.isalpha()     # All alphabetic
s.isdigit()     # All digits
s.isalnum()     # Alphanumeric
s.isspace()     # All whitespace

s.center(10, "*")  # Center with padding
s.zfill(10)     # Zero-padded
s.ljust(10, "*") # Left justified
s.rjust(10, "*") # Right justified

s.encode()      # Encode to bytes
bytes.decode()  # Decode from bytes
```

### String Formatting
```python
name = "Alice"
age = 25
f"My name is {name} and I am {age}"  # f-string
"My name is {} and I am {}".format(name, age)  # format
"My name is %s and I am %d" % (name, age)  # % formatting
```

---

## List Methods

### Creation
```python
lst = [1, 2, 3]
lst = list(range(5))
lst = [0] * 10  # [0, 0, ..., 0]
lst = [[0]*3 for _ in range(3)]  # 2D list
```

### List Methods
```python
lst.append(4)       # Add to end
lst.insert(0, 0)    # Insert at index
lst.extend([5, 6])  # Add multiple elements
lst += [7, 8]       # Same as extend

lst.pop()           # Remove and return last
lst.pop(0)          # Remove and return at index
lst.remove(3)       # Remove first occurrence
del lst[0]          # Delete at index
del lst[1:3]        # Delete slice

lst.index(3)        # Index of first occurrence
lst.count(3)        # Count occurrences

lst.sort()          # Sort in place
lst.sort(reverse=True)  # Sort descending
lst.reverse()       # Reverse in place
lst.copy()          # Shallow copy

lst.clear()         # Remove all elements
```

### List Comprehensions

```python
# Basic: [expression for item in iterable]
squares = [x**2 for x in range(10)]
# Result: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With condition: [expression for item in iterable if condition]
evens = [x for x in range(10) if x % 2 == 0]
# Result: [0, 2, 4, 6, 8]

# Nested: [[expression for j in range(cols)] for i in range(rows)]
matrix = [[i*3+j+1 for j in range(3)] for i in range(3)]
# Result: [[1,2,3], [4,5,6], [7,8,9]]

# Flatten: [item for sublist in list for item in sublist]
flat = [x for row in matrix for x in row]
# Result: [1, 2, 3, 4, 5, 6, 7, 8, 9]

# With transformation
words = ["hello", "world"]
upper = [w.upper() for w in words]
# Result: ['HELLO', 'WORLD']
```

### List Comprehension vs Loop (Equivalent Code)

```
LIST COMPREHENSION:              FOR LOOP:
┌──────────────────────┐        ┌──────────────────────────┐
│ squares =            │        │ squares = []             │
│   [x**2              │   =    │ for x in range(10):      │
│    for x             │        │     squares.append(x**2) │
│    in range(10)]     │        │                          │
└──────────────────────┘        └──────────────────────────┘

List comprehension is:
  ✅ Faster (optimized internally by Python)
  ✅ More concise (1 line vs 3)
  ✅ Preferred in CP for speed

Nested comprehension reading order:
  [[... for j in ...] for i in ...]
   ↑ expression     ↑ outer loop
           ↑ inner loop
```

---

## Dictionary Methods

### Creation
```python
d = {"a": 1, "b": 2}
d = dict(a=1, b=2)
d = dict([("a", 1), ("b", 2)])
d = {x: x**2 for x in range(5)}  # Dict comprehension
```

### Dictionary Methods
```python
d.keys()        # All keys
d.values()      # All values
d.items()       # All (key, value) pairs

d.get("a", 0)   # Get with default value
d.setdefault("c", 0)  # Set if not exists

d["a"]          # Get value (raises KeyError if missing)
d["a"] = 10     # Set value
del d["a"]      # Delete key

d.update({"d": 4})  # Update with another dict
d.pop("a")      # Remove and return
d.popitem()     # Remove and return last item

d.copy()        # Shallow copy
d.clear()       # Remove all items
```

### Dictionary Comprehensions
```python
# From two lists
keys = ["a", "b", "c"]
vals = [1, 2, 3]
d = {k: v for k, v in zip(keys, vals)}

# Filter
d = {k: v for k, v in old_dict.items() if v > 0}

# Transform values
d = {k: v*2 for k, v in old_dict.items()}
```

---

## Set Methods

### Creation
```python
s = {1, 2, 3}
s = set([1, 2, 3])
s = set()  # Empty set (NOT {})
```

### Set Methods
```python
s.add(4)            # Add element
s.update([5, 6])    # Add multiple
s |= {7, 8}         # Same as update

s.remove(3)         # Remove (raises KeyError if missing)
s.discard(3)        # Remove (no error if missing)
s.pop()             # Remove and return arbitrary element

s.union(other)      # s | other
s.intersection(other)  # s & other
s.difference(other)    # s - other
s.symmetric_difference(other)  # s ^ other

s.issubset(other)   # s <= other
s.issuperset(other) # s >= other
s.isdisjoint(other) # No common elements
```

### Set Comprehensions
```python
s = {x**2 for x in range(10)}
s = {x for x in range(10) if x % 2 == 0}
```

---

## Collections Module

### Counter - Frequency Counter

```python
from collections import Counter

s = "hello"
c = Counter(s)  # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})
c.most_common(2)  # [('l', 2), ('h', 1)]
c["l"]  # 2
c.update("world")  # Update counts
```

### Visual: Counter Usage in CP

```
String: "aabbbcccc"
Counter: {'a': 2, 'b': 3, 'c': 4}

CP USE CASES:
  1. Anagram check: Counter(s1) == Counter(s2)
  2. Frequency sort: sorted(c.items(), key=lambda x: -x[1])
  3. Most common element: c.most_common(1)[0][0]
  4. Count pairs with sum: build Counter, then check complement

  Counter is O(n) to build, O(1) to lookup
  vs manual counting: O(n) to build, O(n) to lookup (with list)
```

### defaultdict - No KeyError

```python
from collections import defaultdict

d = defaultdict(int)    # Default value 0
d = defaultdict(list)   # Default value []
d = defaultdict(lambda: 0)  # Custom default

d["a"] += 1  # No KeyError - creates d["a"] = 0 first, then adds 1
d["b"].append(1)  # No KeyError - creates d["b"] = [] first, then appends
```

### defaultdict vs Normal Dict

```
NORMAL DICT:                    DEFAULTDICT:
┌──────────────────────┐       ┌──────────────────────┐
│ d = {}               │       │ d = defaultdict(int) │
│ if key not in d:     │       │ d[key] += 1          │
│     d[key] = 0       │       │ # Just works! ✅     │
│ d[key] += 1          │       │                      │
│ # 3 lines            │       │ # 1 line ✅          │
└──────────────────────┘       └──────────────────────┘

Use defaultdict(list) for adjacency lists in graphs:
  graph = defaultdict(list)
  graph[u].append(v)  # No need to check if u exists!
```

### deque
```python
from collections import deque

dq = deque([1, 2, 3])
dq.append(4)        # Add to right
dq.appendleft(0)    # Add to left
dq.pop()            # Remove from right
dq.popleft()        # Remove from left
dq.rotate(1)        # Rotate right
dq.rotate(-1)       # Rotate left
dq[0]               # First element
dq[-1]              # Last element
```

### namedtuple
```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
p.x  # 1
p.y  # 2
```

### OrderedDict (Python 3.7+ dicts maintain insertion order)
```python
from collections import OrderedDict
od = OrderedDict()
od['a'] = 1
od['b'] = 2
od.move_to_end('a')  # Move to end
od.popitem(last=False)  # Pop from beginning
```

---

## Itertools Module

### Infinite Iterators
```python
import itertools

# count(start, step)
for i in itertools.count(0, 2):
    if i > 10: break
    print(i)  # 0, 2, 4, 6, 8, 10

# cycle(iterable)
c = itertools.cycle([1, 2, 3])
next(c)  # 1, 2, 3, 1, 2, 3, ...

# repeat(value, times)
r = itertools.repeat(5, 3)  # 5, 5, 5
```

### Finite Iterators
```python
# accumulate(iterable, func)
list(itertools.accumulate([1, 2, 3, 4]))  # [1, 3, 6, 10]

# chain(*iterables)
list(itertools.chain([1, 2], [3, 4]))  # [1, 2, 3, 4]

# compress(data, selectors)
list(itertools.compress("ABC", [1, 0, 1]))  # ['A', 'C']

# dropwhile(pred, iterable)
list(itertools.dropwhile(lambda x: x<5, [1,3,6,2,1]))  # [6, 2, 1]

# takewhile(pred, iterable)
list(itertools.takewhile(lambda x: x<5, [1,3,6,2,1]))  # [1, 3]

# filterfalse(pred, iterable)
list(itertools.filterfalse(lambda x: x%2, range(6)))  # [0, 2, 4]

# islice(iterable, stop)
list(itertools.islice(range(10), 5))  # [0, 1, 2, 3, 4]

# starmap(func, iterable)
list(itertools.starmap(pow, [(2,3), (3,2)]))  # [8, 9]

# zip_longest(*iterables)
list(itertools.zip_longest([1,2], [3], fillvalue=0))  # [(1,3), (2,0)]
```

### Combinatoric Iterators
```python
# permutations(iterable, r)
list(itertools.permutations([1,2,3], 2))
# [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]

# combinations(iterable, r)
list(itertools.combinations([1,2,3], 2))
# [(1,2), (1,3), (2,3)]

# combinations_with_replacement
list(itertools.combinations_with_replacement([1,2], 2))
# [(1,1), (1,2), (2,2)]

# product(*iterables)
list(itertools.product([0,1], repeat=3))
# [(0,0,0), (0,0,1), (0,1,0), ..., (1,1,1)]
```

---

## Bisect Module

### Visual: bisect_left vs bisect_right

```
Sorted List: [1, 3, 3, 3, 5, 7, 9]
               0  1  2  3  4  5  6

bisect_left(lst, 3)  → 1  (leftmost position to insert 3)
                         ↑
                         First 3 is at index 1

bisect_right(lst, 3) → 4  (rightmost position to insert 3)
                              ↑
                              After last 3 (index 3)

bisect_left(lst, 6)  → 4  (where 6 would go to maintain sorted order)
                         ↑
                         Between 5 and 7

bisect_left(lst, 0)  → 0  (smaller than all → insert at start)
bisect_left(lst, 10) → 7  (larger than all → insert at end)

CP APPLICATION: Count elements in range [lo, hi]
  count = bisect_right(lst, hi) - bisect_left(lst, lo)
```

```python
import bisect

lst = [1, 3, 5, 7, 9]

# bisect_left(lst, x) - Leftmost position to insert x
bisect.bisect_left(lst, 5)  # 2
bisect.bisect_left(lst, 6)  # 3

# bisect_right(lst, x) - Rightmost position to insert x
bisect.bisect_right(lst, 5)  # 3
bisect.bisect_right(lst, 6)  # 3

# insort_left(lst, x) - Insert x in sorted order (leftmost)
bisect.insort_left(lst, 5)

# insort_right(lst, x) - Insert x in sorted order (rightmost)
bisect.insort_right(lst, 5)

# Finding range of elements
def find_range(lst, x):
    left = bisect.bisect_left(lst, x)
    right = bisect.bisect_right(lst, x)
    return left, right

# Number of elements less than x
def count_less_than(lst, x):
    return bisect.bisect_left(lst, x)

# Number of elements greater than x
def count_greater_than(lst, x):
    return len(lst) - bisect.bisect_right(lst, x)
```

---

## heapq Module

### Visual: Min-Heap Structure

```
Min-Heap: parent ≤ children

        1              Array representation:
       / \             [1, 3, 2, 5, 4, 6, 7]
      3   2            Index: 0  1  2  3  4  5  6
     / \ / \           
    5  4 6  7          Parent of i: (i-1)//2
                       Left child:  2*i + 1
                       Right child: 2*i + 2

heappush: O(log n)    - add to end, bubble up
heappop:  O(log n)    - remove root, bubble down
heapify:  O(n)        - convert list to heap in-place
heap[0]:  O(1)        - peek at minimum
```

```python
import heapq

# Min heap (default)
heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)
smallest = heapq.heappop(heap)  # 1

# Build heap from list
lst = [5, 3, 1, 4, 2]
heapq.heapify(lst)  # In-place, O(n)

# Peek at smallest
smallest = heap[0]

# Get n largest/smallest
heapq.nlargest(3, [5, 3, 1, 4, 2])  # [5, 4, 3]
heapq.nsmallest(3, [5, 3, 1, 4, 2])  # [1, 2, 3]

# Merge sorted iterables
merged = heapq.merge([1, 3, 5], [2, 4, 6])
list(merged)  # [1, 2, 3, 4, 5, 6]

# Max heap (negate values)
max_heap = []
heapq.heappush(max_heap, -3)
heapq.heappush(max_heap, -1)
largest = -heapq.heappop(max_heap)  # 3

# Kth largest element
def kth_largest(lst, k):
    return heapq.nlargest(k, lst)[-1]

# Median of stream
class MedianFinder:
    def __init__(self):
        self.lo = []  # Max heap (negated)
        self.hi = []  # Min heap

    def add(self, num):
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def median(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2
```

---

## Math Module

```python
import math

# Constants
math.pi  # 3.141592653589793
math.e   # 2.718281828459045
math.inf  # infinity
math.nan  # not a number

# Basic math
math.ceil(3.2)     # 4
math.floor(3.8)    # 3
math.fabs(-5)      # 5.0
math.factorial(5)  # 120
math.gcd(12, 8)    # 4
math.lcm(4, 6)     # 12

# Power and roots
math.pow(2, 3)     # 8.0
math.sqrt(16)      # 4.0

# Logarithmic
math.log(100, 10)  # 2.0
math.log2(8)       # 3.0
math.log10(100)    # 2.0

# Trigonometry
math.sin(math.pi/2)  # 1.0
math.cos(0)          # 1.0
math.radians(180)    # pi
math.degrees(math.pi)  # 180

# Combinatorics
math.comb(5, 2)    # 10 (5 choose 2)
math.perm(5, 2)    # 20 (5 permute 2)
```

---

## Common Imports for CP

```python
# Always import these
import sys
from collections import defaultdict, Counter, deque
from functools import lru_cache
import heapq
import bisect
import math

# For recursion limit
sys.setrecursionlimit(10**6)

# Fast I/O
input = sys.stdin.readline

# For large numbers
MOD = 10**9 + 7

# Quick I/O wrapper
def read_int():
    return int(input())

def read_ints():
    return list(map(int, input().split()))

def read_str():
    return input().strip()

def read_strs():
    return input().split()
```

---

## Quick Reference: All Operations

### Time Complexities
```python
# List
len()           # O(1)
append()        # O(1)
pop()           # O(1)
insert(0, x)    # O(n)
pop(0)          # O(n)
in (search)     # O(n)

# Dict
len()           # O(1)
get()           # O(1)
set()           # O(1)
in (search)     # O(1)

# Set
len()           # O(1)
add()           # O(1)
remove()        # O(1)
in (search)     # O(1)

# String
len()           # O(1)
concatenation   # O(n)
slice           # O(k)
```

### Useful Patterns
```python
# Check if number is power of 2
def is_power_of_2(n):
    return n & (n - 1) == 0

# Count set bits
def count_bits(n):
    return bin(n).count('1')

# Bit manipulation
n & (1 << k)    # Check kth bit
n | (1 << k)    # Set kth bit
n & ~(1 << k)   # Clear kth bit
n ^ (1 << k)    # Toggle kth bit

# Modular arithmetic
(a + b) % MOD
(a * b) % MOD
pow(a, b, MOD)  # Fast modular exponentiation

# Prime sieve
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return is_prime
```

> **Tip:** Memorize these operations. Infosys coding rounds require speed, and knowing Python's built-in functions can save minutes.
