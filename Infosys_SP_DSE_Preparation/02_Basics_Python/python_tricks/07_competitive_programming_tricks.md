# Competitive Programming Tricks in Python

## 1. One-Liner Solutions

```python
# ============================================
# Count occurrences
# ============================================
from collections import Counter
freq = Counter(arr)

# ============================================
# Find min/max in 2D grid
# ============================================
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat_max = max(max(row) for row in grid)
flat_min = min(min(row) for row in grid)

# ============================================
# Matrix transpose
# ============================================
transpose = [list(row) for row in zip(*grid)]

# ============================================
# Flatten 2D list
# ============================================
flat = [num for row in matrix for num in row]

# ============================================
# Run-length encoding
# ============================================
def rle(s):
    return ''.join(f"{len(list(g))}{k}" for k, g in __import__('itertools').groupby(s))

# ============================================
# Binary search one-liner (bisect)
# ============================================
import bisect
idx = bisect.bisect_left(arr, target)

# ============================================
# Check if number is power of 2
# ============================================
is_power_of_2 = lambda n: n > 0 and (n & (n - 1)) == 0
```

## 2. defaultdict to Avoid Key Errors

```python
from collections import defaultdict

# ============================================
# Without defaultdict — verbose
# ============================================
d = {}
for key, value in pairs:
    if key not in d:
        d[key] = []
    d[key].append(value)

# ============================================
# With defaultdict — clean
# ============================================
d = defaultdict(list)
for key, value in pairs:
    d[key].append(value)

# ============================================
# Common patterns
# ============================================
# List grouping
d = defaultdict(list)
for item in items:
    d[category].append(item)

# Counter alternative
d = defaultdict(int)
for x in arr:
    d[x] += 1

# Set grouping
d = defaultdict(set)
for item in items:
    d[category].add(item)

# Nested defaultdict (2D)
d = defaultdict(lambda: defaultdict(int))
d[x][y] += 1
```

## 3. Counter for Frequency Analysis

```python
from collections import Counter

# ============================================
# Basic frequency count
# ============================================
arr = [1, 2, 2, 3, 3, 3]
c = Counter(arr)  # Counter({3: 3, 2: 2, 1: 1})

# ============================================
# Most common elements
# ============================================
c.most_common(3)  # Top 3 most frequent
c.most_common(1)[0][0]  # Most frequent element

# ============================================
# Check if all frequencies are equal
# ============================================
c = Counter(arr)
if len(set(c.values())) == 1:
    print("All elements have same frequency")

# ============================================
# Check if string can be rearranged to palindrome
# ============================================
def can_form_palindrome(s):
    c = Counter(s)
    odd_count = sum(1 for v in c.values() if v % 2 == 1)
    return odd_count <= 1

# ============================================
# Character frequency comparison
# ============================================
def is_anagram(s, t):
    return Counter(s) == Counter(t)

# ============================================
# Counter arithmetic
# ============================================
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)  # Counter({'a': 4, 'b': 3})
print(c1 - c2)  # Counter({'a': 2})  — only positive
print(c1 & c2)  # Counter({'a': 1, 'b': 1})  — min
print(c1 | c2)  # Counter({'a': 3, 'b': 2})  — max
```

## 4. Sorting Tricks

```python
# ============================================
# Custom sort key
# ============================================
# Sort by absolute value
arr = [-5, 3, -1, 4, -2]
arr.sort(key=abs)  # [-1, -2, 3, 4, -5]

# Sort by last digit
arr = [13, 25, 47, 31]
arr.sort(key=lambda x: x % 10)  # [31, 13, 25, 47]

# Sort by string length
words = ["banana", "hi", "cherry", "go"]
words.sort(key=len)  # ['go', 'hi', 'banana', 'cherry']

# ============================================
# Stable sort (preserves relative order of equal elements)
# ============================================
# Python's sort is stable by default
# Useful for multi-key sorting:
students = [("Alice", "B"), ("Bob", "A"), ("Charlie", "B")]
students.sort(key=lambda x: x[0])  # Sort by name first (stable)
students.sort(key=lambda x: x[1])  # Then by grade (stable)
# Result: sorted by grade, with same grades sorted by name

# ============================================
# Reverse sort
# ============================================
arr.sort(reverse=True)  # Descending order

# ============================================
# Sort tuples by specific element
# ============================================
pairs = [(1, 'b'), (3, 'a'), (2, 'c')]
pairs.sort(key=lambda x: x[0])  # Sort by first element
pairs.sort(key=lambda x: x[1])  # Sort by second element

# ============================================
# Sort with tie-breaking
# ============================================
# Sort by (-frequency, value) — most frequent first, then by value
c = Counter(arr)
sorted_arr = sorted(set(arr), key=lambda x: (-c[x], x))
```

## 5. enumerate vs range(len())

```python
# ============================================
# SLOW: range(len())
# ============================================
arr = [10, 20, 30, 40, 50]
for i in range(len(arr)):
    print(f"index {i}: {arr[i]}")

# ============================================
# FAST: enumerate (Pythonic, slightly faster)
# ============================================
for i, val in enumerate(arr):
    print(f"index {i}: {val}")

# Start enumerate from 1
for i, val in enumerate(arr, 1):
    print(f"{i}. {val}")

# ============================================
# CP Usage: Find index of element
# ============================================
# SLOW:
target = 30
for i in range(len(arr)):
    if arr[i] == target:
        print(f"Found at index {i}")
        break

# FAST:
for i, val in enumerate(arr):
    if val == target:
        print(f"Found at index {i}")
        break

# Even faster:
if target in arr:
    print(arr.index(target))
```

## 6. Zip for Parallel Iteration

```python
# ============================================
# Basic zip
# ============================================
names = ["Alice", "Bob", "Charlie"]
grades = [85, 92, 78]

for name, grade in zip(names, grades):
    print(f"{name}: {grade}")

# ============================================
# Zip for dict creation
# ============================================
d = dict(zip(names, grades))  # {'Alice': 85, 'Bob': 92, 'Charlie': 78}

# ============================================
# Zip for matrix transpose
# ============================================
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transpose = [list(row) for row in zip(*matrix)]
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

# ============================================
# Zip for parallel processing
# ============================================
arr1 = [1, 2, 3]
arr2 = [4, 5, 6]
sums = [a + b for a, b in zip(arr1, arr2)]  # [5, 7, 9]

# ============================================
# Zip for string interleaving
# ============================================
s1 = "abc"
s2 = "123"
interleaved = ''.join(a + b for a, b in zip(s1, s2))  # "a1b2c3"
```

## 7. any() and all()

```python
# ============================================
# any() — True if ANY element is True
# ============================================
nums = [1, 2, 3, 4, 5]
print(any(x > 3 for x in nums))  # True (4 and 5 exist)

# Check if any element is even
print(any(x % 2 == 0 for x in nums))  # True

# ============================================
# all() — True if ALL elements are True
# ============================================
print(all(x > 0 for x in nums))  # True (all positive)

# Check if all elements are unique
print(len(nums) == len(set(nums)))

# ============================================
# CP Usage: Early termination
# ============================================
# Check if array is sorted
is_sorted = all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

# Check if all rows have same length
all_same_len = all(len(row) == len(grid[0]) for row in grid)

# ============================================
# any/all with empty iterable
# ============================================
print(any([]))  # False
print(all([]))  # True — vacuously true!
```

## 8. Chained Comparisons

```python
# ============================================
# Python supports chained comparisons
# ============================================
x = 5

# SLOW (evaluates x twice):
result = x > 0 and x < 10

# FAST (Pythonic):
result = 0 < x < 10

# Multiple chains:
result = 1 <= x <= 100
result = 0 < x < y < 100

# ============================================
# CP Usage: Range checking
# ============================================
def in_bounds(r, c, n, m):
    return 0 <= r < n and 0 <= c < m

# ============================================
# Chained equality
# ============================================
a, b, c = 5, 5, 5
print(a == b == c)  # True
```

## 9. Dict as Hash Map

```python
# ============================================
# Dictionary as hash map — O(1) lookup
# ============================================
# Two Sum pattern
def two_sum(arr, target):
    seen = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# ============================================
# Frequency count
# ============================================
freq = {}
for x in arr:
    freq[x] = freq.get(x, 0) + 1

# ============================================
# Memoization
# ============================================
memo = {}
def fib(n):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n-1) + fib(n-2)
    return memo[n]

# ============================================
# Character mapping
# ============================================
s = "hello"
char_index = {ch: i for i, ch in enumerate(s)}
# {'h': 0, 'e': 1, 'l': 2, 'o': 4}

# ============================================
# Grouping
# ============================================
from itertools import groupby
from collections import defaultdict
d = defaultdict(list)
for item in items:
    d[key_func(item)].append(item)
```

## 10. List as Boolean

```python
# ============================================
# Empty list is False, non-empty is True
# ============================================
lst = []
if not lst:
    print("Empty")  # This runs

lst = [1, 2, 3]
if lst:
    print("Not empty")  # This runs

# ============================================
# CP Usage: Check if list has elements
# ============================================
def find_path(graph, start, end, visited):
    if start == end:
        return [start]
    
    visited.add(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            path = find_path(graph, neighbor, end, visited)
            if path:  # If path found
                return [start] + path
    return []  # Empty list = no path found

# ============================================
# Using truthiness
# ============================================
result = []
if result:
    print("Found")  # Won't print
else:
    print("Not found")  # Will print
```

## 11. Set for O(1) Lookups

```python
# ============================================
# Converting list to set for fast membership testing
# ============================================
arr = list(range(1000000))
target = 999999

# SLOW — O(n):
if target in arr:
    print("Found")

# FAST — O(1):
arr_set = set(arr)
if target in arr_set:
    print("Found")

# ============================================
# CP Pattern: Two Sum with set
# ============================================
def two_sum_exists(arr, target):
    seen = set()
    for num in arr:
        if target - num in seen:
            return True
        seen.add(num)
    return False

# ============================================
# CP Pattern: Find duplicates
# ============================================
def find_duplicates(arr):
    seen = set()
    duplicates = set()
    for x in arr:
        if x in seen:
            duplicates.add(x)
        seen.add(x)
    return list(duplicates)

# ============================================
# Set operations for comparison
# ============================================
def common_elements(arr1, arr2):
    return list(set(arr1) & set(arr2))

def all_unique(arr):
    return len(arr) == len(set(arr))
```

## 12. Negative Indexing Tricks

```python
# ============================================
# Access from end
# ============================================
arr = [1, 2, 3, 4, 5]
print(arr[-1])    # 5 — last element
print(arr[-2])    # 4 — second to last
print(arr[-3:])   # [3, 4, 5] — last 3 elements

# ============================================
# Reverse using negative step
# ============================================
arr = [1, 2, 3, 4, 5]
reversed_arr = arr[::-1]  # [5, 4, 3, 2, 1]

# ============================================
# Rotate using slicing
# ============================================
# Left rotate by k
k = 2
rotated = arr[k:] + arr[:k]  # [3, 4, 5, 1, 2]

# Right rotate by k
rotated = arr[-k:] + arr[:-k]  # [4, 5, 1, 2, 3]

# ============================================
# Extract last n elements
# ============================================
arr = [1, 2, 3, 4, 5, 6, 7]
last_3 = arr[-3:]  # [5, 6, 7]

# ============================================
# Exclude last element
# ============================================
arr = [1, 2, 3, 4, 5]
without_last = arr[:-1]  # [1, 2, 3, 4]
```

## 13. Slice Assignment

```python
# ============================================
# Replace a range of elements
# ============================================
arr = [1, 2, 3, 4, 5]
arr[1:3] = [20, 30]  # [1, 20, 30, 4, 5]

# ============================================
# Insert using slice
# ============================================
arr = [1, 2, 5]
arr[2:2] = [3, 4]  # [1, 2, 3, 4, 5]

# ============================================
# Delete using slice
# ============================================
arr = [1, 2, 3, 4, 5]
del arr[1:3]  # [1, 4, 5]

# ============================================
# Replace with different length list
# ============================================
arr = [1, 2, 3, 4, 5]
arr[1:4] = [10, 20]  # [1, 10, 20, 5]

# ============================================
# Clear a portion
# ============================================
arr = [1, 2, 3, 4, 5]
arr[1:4] = []  # [1, 5]
```

## 14. Walrus Operator (:=) — Python 3.8+

```python
# ============================================
# Walrus operator — assign and use in one expression
# ============================================
# Without walrus:
n = int(input())
while n != 0:
    process(n)
    n = int(input())

# With walrus:
while (n := int(input())) != 0:
    process(n)

# ============================================
# In list comprehension
# ============================================
# Without walrus:
results = [transform(x) for x in arr if (y := compute(x)) > threshold]

# More complex example:
data = ["hello", "world", "python"]
filtered = [upper for s in data if (upper := s.upper()) and len(upper) > 4]
# ['HELLO', 'WORLD', 'PYTHON']

# ============================================
# In function calls
# ============================================
# Without walrus:
result = expensive_function(input())
print(result)

# With walrus:
print(result := expensive_function(input()))

# ============================================
# CP Usage: Reading input with processing
# ============================================
# Read n pairs and process
data = sys.stdin.read().split()
pairs = [(int(data[i]), int(data[i+1])) for i in range(0, len(data), 2)]
```

## 15. Common CP Templates

```python
# ============================================
# TEMPLATE 1: Fast Input
# ============================================
import sys
input = sys.stdin.readline

def read_int():
    return int(input())
def read_ints():
    return list(map(int, input().split()))

# ============================================
# TEMPLATE 2: BFS
# ============================================
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    distance = {start: 0}
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    
    return distance

# ============================================
# TEMPLATE 3: DFS
# ============================================
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    
    return visited

# ============================================
# TEMPLATE 4: Dijkstra's Shortest Path
# ============================================
import heapq

def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    heap = [(0, start)]
    
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    
    return dist

# ============================================
# TEMPLATE 5: Binary Search
# ============================================
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# Binary search on answer:
def can_solve(mid):
    # Check if answer mid is valid
    pass

lo, hi = min_possible, max_possible
while lo < hi:
    mid = (lo + hi) // 2
    if can_solve(mid):
        hi = mid
    else:
        lo = mid + 1
# lo is the answer

# ============================================
# TEMPLATE 6: Union-Find
# ============================================
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

# ============================================
# TEMPLATE 7: Sieve of Eratosthenes
# ============================================
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return is_prime

# ============================================
# TEMPLATE 8: Modular arithmetic
# ============================================
MOD = 10**9 + 7

def add(a, b):
    return (a + b) % MOD

def mul(a, b):
    return (a * b) % MOD

def power(base, exp, mod=MOD):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result

def mod_inv(a, mod=MOD):
    return power(a, mod - 2, mod)  # Fermat's little theorem

# ============================================
# TEMPLATE 9: Combinations
# ============================================
def nCr(n, r, mod=MOD):
    if r > n:
        return 0
    if r == 0 or r == n:
        return 1
    
    num = 1
    den = 1
    for i in range(r):
        num = (num * (n - i)) % mod
        den = (den * (i + 1)) % mod
    
    return (num * mod_inv(den)) % mod

# ============================================
# TEMPLATE 10: Fenwick Tree (Binary Indexed Tree)
# ============================================
class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, i, delta):
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)
    
    def query(self, i):
        i += 1
        result = 0
        while i > 0:
            result += self.tree[i]
            i -= i & (-i)
        return result
    
    def range_query(self, l, r):
        return self.query(r) - (self.query(l - 1) if l > 0 else 0)
```
