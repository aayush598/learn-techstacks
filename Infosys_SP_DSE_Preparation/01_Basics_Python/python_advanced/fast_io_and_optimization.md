# Fast I/O and Python Optimization for Competitive Programming

## 1. sys.stdin.readline vs input()

```python
import sys

# ============================================
# SLOW: Built-in input()
# ============================================
# def main():
#     n = int(input())
#     arr = list(map(int, input().split()))

# ============================================
# FAST: sys.stdin.readline
# ============================================
input = sys.stdin.readline  # Override built-in input

def main():
    n = int(input())
    arr = list(map(int, input().split()))

# ============================================
# FASTEST: sys.stdin.buffer.read
# ============================================
import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    n = int(next(it))
    arr = [int(next(it)) for _ in range(n)]

# ============================================
# Performance Comparison (10^6 integers):
# input():           ~2-3 seconds
# sys.stdin.readline: ~0.5-1 second
# sys.stdin.buffer:   ~0.1-0.2 seconds
# ============================================
```

## 2. sys.stdout.write vs print()

```python
import sys

# ============================================
# print() — adds newline by default, slower
# ============================================
for i in range(100000):
    print(i)

# ============================================
# sys.stdout.write — no automatic newline, faster
# ============================================
output = []
for i in range(100000):
    output.append(str(i))
sys.stdout.write('\n'.join(output))

# ============================================
# For single prints, print() is fine
# For massive output, build string and write once
# ============================================
# SLOW:
for x in result:
    print(x)

# FAST:
print('\n'.join(map(str, result)))

# Or for binary outputs:
print(*result, sep='\n')
```

## 3. Reading Multiple Inputs Efficiently

```python
import sys

# ============================================
# Method 1: Using iter (clean and fast)
# ============================================
def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    
    t = int(next(it))
    results = []
    
    for _ in range(t):
        n = int(next(it))
        arr = [int(next(it)) for _ in range(n)]
        results.append(str(sum(arr)))
    
    sys.stdout.write('\n'.join(results) + '\n')

# ============================================
# Method 2: Using index pointer
# ============================================
def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    
    def read_int():
        nonlocal idx
        val = int(data[idx])
        idx += 1
        return val
    
    t = read_int()
    for _ in range(t):
        n = read_int()
        arr = [read_int() for _ in range(n)]
        # Process arr...

# ============================================
# Method 3: Line by line (when you need lines)
# ============================================
def solve():
    input = sys.stdin.readline
    t = int(input())
    
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        # Process arr...

# ============================================
# Reading a grid
# ============================================
def read_grid(n, m):
    grid = []
    for _ in range(n):
        row = list(map(int, input().split()))
        grid.append(row)
    return grid

# Or faster:
def read_grid_fast(n):
    data = sys.stdin.buffer.read().split()
    grid = [data[i*n:(i+1)*n] for i in range(n)]
    return grid
```

## 4. String Building — join Instead of +

```python
# ============================================
# SLOW: String concatenation with +
# ============================================
result = ""
for i in range(10000):
    result += str(i) + " "  # Creates new string each time — O(n²)

# ============================================
# FAST: Using join
# ============================================
result = " ".join(str(i) for i in range(10000))  # O(n)

# ============================================
# For building output
# ============================================
# SLOW:
output = ""
for x in arr:
    output += str(x) + "\n"
print(output)

# FAST:
output = "\n".join(map(str, arr))
sys.stdout.write(output + "\n")

# ============================================
# For building strings character by character
# ============================================
# SLOW:
s = ""
for ch in "hello world":
    if ch != " ":
        s += ch

# FAST:
s = "".join(ch for ch in "hello world" if ch != " ")

# ============================================
# List append + join pattern (common in CP)
# ============================================
result = []
for i in range(n):
    result.append(str(answer[i]))
sys.stdout.write("\n".join(result) + "\n")
```

## 5. Using array Module vs List

```python
from array import array

# ============================================
# array.array — typed arrays, more memory efficient
# ============================================
# List of integers (each int is an object — heavy)
lst = [1, 2, 3, 4, 5]  # Each int takes ~28 bytes

# Array of integers (typed — compact)
arr = array('i', [1, 2, 3, 4, 5])  # Each int takes ~4 bytes

# For very large arrays, array is more memory efficient
# But list operations are often faster due to Python optimization

# ============================================
# array types:
# 'b' — signed char
# 'i' — signed int
# 'l' — signed long
# 'f' — float
# 'd' — double
# ============================================

# In practice, for CP:
# Use lists for most cases
# Use array only when memory is a concern
# NumPy is fastest but usually not available in CP
```

## 6. PyPy vs CPython

```python
# ============================================
# PyPy:
#   - JIT-compiled Python
#   - 10-100x faster for loops
#   - Slower startup time
#   - Higher memory usage
#   - Most CP platforms support it
#
# CPython (default Python):
#   - Interpreter-based
#   - Standard library
#   - Lower memory usage
# ============================================

# Tips for PyPy:
# 1. Use simple loops — PyPy optimizes them well
# 2. Avoid large lists of objects — use simple types
# 3. Use recursion carefully (higher overhead)
# 4. PyPy handles int operations well

# Code that's fast in both:
def solve():
    import sys
    input = sys.stdin.readline
    
    n = int(input())
    arr = list(map(int, input().split()))
    arr.sort()
    print(sum(arr[::2]))

# ============================================
# Common PyPy-specific optimizations:
# ============================================
# 1. Use bit operations instead of modulo when possible
# 2. Avoid creating many small objects
# 3. Use local variable lookups (assign to local inside function)
```

## 7. Common TLE Causes and Fixes

```python
# ============================================
# TLE CAUSE 1: Using input() instead of sys.stdin.readline
# FIX:
import sys
input = sys.stdin.readline

# ============================================
# TLE CAUSE 2: String concatenation in loop
# FIX:
# BAD:
s = ""
for item in items:
    s += str(item) + " "

# GOOD:
s = " ".join(map(str, items))

# ============================================
# TLE CAUSE 3: Using list.index() in loop
# FIX:
# BAD (O(n²)):
for i in range(n):
    idx = arr.index(target)

# GOOD (O(n)):
index_map = {val: i for i, val in enumerate(arr)}

# ============================================
# TLE CAUSE 4: Checking membership in list
# FIX:
# BAD (O(n)):
if target in my_list:  # Very slow for large lists

# GOOD (O(1)):
my_set = set(my_list)
if target in my_set:

# ============================================
# TLE CAUSE 5: Unnecessary sorting
# FIX:
# BAD:
arr.sort()
# If you only need min/max, don't sort the whole thing

# GOOD:
minimum = min(arr)
maximum = max(arr)

# ============================================
# TLE CAUSE 6: Using recursion instead of iteration
# FIX:
# BAD:
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)  # O(2^n)

# GOOD:
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# ============================================
# TLE CAUSE 7: Creating unnecessary copies
# FIX:
# BAD:
for x in arr[:]:  # Creates copy
    process(x)

# GOOD:
for x in arr:  # Direct iteration
    process(x)

# ============================================
# TLE CAUSE 8: Using dictionary.get() in tight loop
# FIX:
# Often fine, but if really tight:
# BAD:
d = {}
for x in arr:
    d[x] = d.get(x, 0) + 1

# GOOD:
from collections import Counter
d = Counter(arr)  # Implemented in C
```

## 8. Using Built-in Functions (C-Optimized)

```python
# ============================================
# Python built-ins are implemented in C and are FAST
# ============================================

# sum, min, max, len — all C-optimized
total = sum(arr)
minimum = min(arr)
maximum = max(arr)
length = len(arr)

# sorted() — uses Timsort (C implementation)
sorted_arr = sorted(arr)

# any, all — short-circuit, C-optimized
has_even = any(x % 2 == 0 for x in arr)
all_positive = all(x > 0 for x in arr)

# enumerate — faster than manual indexing
for i, val in enumerate(arr):
    process(val)

# zip — parallel iteration
for a, b in zip(arr1, arr2):
    process(a, b)

# map — applies function to each element (C loop)
result = list(map(str, arr))

# abs, round — C-optimized
magnitude = abs(-42)
rounded = round(3.14159, 2)

# ============================================
# Key insight: Avoid writing Python loops for simple operations
# Let built-in functions do the heavy lifting
# ============================================

# SLOW (pure Python loop):
total = 0
for x in arr:
    total += x

# FAST (C-optimized built-in):
total = sum(arr)

# SLOW:
max_val = arr[0]
for x in arr:
    if x > max_val:
        max_val = x

# FAST:
max_val = max(arr)
```

## 9. bisect Module

```python
import bisect

# ============================================
# bisect — binary search in sorted lists
# ============================================
arr = [1, 2, 4, 4, 4, 5, 7, 9, 10]

# bisect_left — find leftmost position to insert
print(bisect.bisect_left(arr, 4))   # 2 (index of first 4)
print(bisect.bisect_left(arr, 6))   # 6 (would insert before index 6)

# bisect_right — find rightmost position to insert
print(bisect.bisect_right(arr, 4))  # 5 (index after last 4)
print(bisect.bisect_right(arr, 6))  # 6

# Count occurrences
def count_occurrences(arr, x):
    return bisect.bisect_right(arr, x) - bisect.bisect_left(arr, x)

print(count_occurrences(arr, 4))  # 3 (three 4s in arr)

# ============================================
# bisect.insort — insert maintaining sorted order
# ============================================
arr = [1, 2, 4, 5]
bisect.insort(arr, 3)
print(arr)  # [1, 2, 3, 4, 5]

bisect.insort(arr, 4)  # Duplicate
print(arr)  # [1, 2, 3, 4, 4, 5]

# ============================================
# CP Usage: Find closest element to target
# ============================================
def closest_element(arr, target):
    idx = bisect.bisect_left(arr, target)
    
    candidates = []
    if idx > 0:
        candidates.append(arr[idx - 1])
    if idx < len(arr):
        candidates.append(arr[idx])
    
    return min(candidates, key=lambda x: abs(x - target))

arr = [1, 3, 5, 7, 9]
print(closest_element(arr, 4))  # 3
print(closest_element(arr, 6))  # 5

# ============================================
# CP Usage: Find first element >= target
# ============================================
def lower_bound(arr, target):
    idx = bisect.bisect_left(arr, target)
    if idx < len(arr):
        return arr[idx]
    return None

print(lower_bound([1, 3, 5, 7, 9], 6))  # 7
print(lower_bound([1, 3, 5, 7, 9], 10)) # None

# ============================================
# CP Usage: Find last element <= target
# ============================================
def upper_bound(arr, target):
    idx = bisect.bisect_right(arr, target) - 1
    if idx >= 0:
        return arr[idx]
    return None

print(upper_bound([1, 3, 5, 7, 9], 6))  # 5
print(upper_bound([1, 3, 5, 7, 9], 0))  # None
```

## 10. functools.lru_cache for Memoization

```python
from functools import lru_cache, cache
import sys

sys.setrecursionlimit(10000)

# ============================================
# @lru_cache — Least Recently Used cache
# ============================================
@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# ============================================
# Cache info
# ============================================
print(fibonacci(50))
print(fibonacci.cache_info())
# CacheInfo(hits=48, misses=51, maxsize=None, currsize=51)

# ============================================
# Clear cache (important for multiple test cases!)
# ============================================
fibonacci.cache_clear()

# ============================================
# @cache (Python 3.9+) — simpler, no maxsize
# ============================================
@cache
def dp(state):
    # ... computation
    pass

# ============================================
# CP Template with memoization
# ============================================
import sys
sys.setrecursionlimit(10000)
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    @lru_cache(maxsize=None)
    def dfs(node, mask):
        if mask == (1 << n) - 1:
            return 0
        
        result = float('inf')
        for neighbor in graph[node]:
            if not (mask & (1 << neighbor)):
                result = min(result, 1 + dfs(neighbor, mask | (1 << neighbor)))
        
        return result
    
    return dfs(0, 1)  # Start at node 0, visited mask with only bit 0 set
```

## 11. Complete Fast I/O Template

```python
import sys
from collections import defaultdict, deque, Counter
from heapq import heappush, heappop, heapify
from functools import lru_cache
import bisect
import math

# ============================================
# Fast I/O setup
# ============================================
input = sys.stdin.readline
def read_int():
    return int(input())
def read_ints():
    return list(map(int, input().split()))
def read_ints_all():
    return list(map(int, sys.stdin.buffer.read().split()))

# ============================================
# Solution template
# ============================================
def solve():
    n = read_int()
    arr = read_ints()
    
    # Your solution here
    result = sum(arr)
    
    print(result)

# ============================================
# Main
# ============================================
def main():
    t = read_int()
    for _ in range(t):
        solve()

if __name__ == "__main__":
    main()
```

## 12. Advanced Optimization Tricks

```python
# ============================================
# Trick 1: Local variable lookup (faster than global)
# ============================================
def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    
    # Assign to local variables for speed
    max_func = max
    min_func = min
    sum_func = sum
    
    result = sum_func(arr)  # Faster than sum(arr) in tight loops

# ============================================
# Trick 2: Avoid function calls in tight loops
# ============================================
# SLOW:
for i in range(n):
    arr.append(i * 2)

# FAST:
append = arr.append
for i in range(n):
    append(i * 2)

# ============================================
# Trick 3: Use bit operations
# ============================================
# Check even: x & 1 == 0  (faster than x % 2 == 0)
# Divide by 2: x >> 1     (faster than x // 2)
# Multiply by 2: x << 1   (faster than x * 2)
# Check power of 2: x & (x-1) == 0

# ============================================
# Trick 4: Early termination
# ============================================
def solve():
    for i in range(n):
        if condition_met:
            print("YES")
            break
    else:
        print("NO")

# ============================================
# Trick 5: Use sets for O(1) membership
# ============================================
# BAD: O(n) lookup
if target in arr:  # arr is a list

# GOOD: O(1) lookup
arr_set = set(arr)
if target in arr_set:

# ============================================
# Trick 6: Precompute when repeated queries
# ============================================
# If you need to answer many range sum queries:
prefix = [0] * (n + 1)
for i in range(n):
    prefix[i + 1] = prefix[i] + arr[i]

# Range sum [l, r] in O(1):
range_sum = prefix[r + 1] - prefix[l]
```
