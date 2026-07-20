# Recursion and Lambda in Python — Complete Guide for CP

## 1. Recursion Basics

```python
# ============================================
# What is Recursion?
# A function that calls itself.
# Every recursive function needs:
#   1. BASE CASE — when to stop
#   2. RECURSIVE CASE — smaller subproblem
# ============================================

# Example 1: Factorial
def factorial(n):
    if n <= 1:          # Base case
        return 1
    return n * factorial(n - 1)  # Recursive case

print(factorial(5))  # 120

# Example 2: Fibonacci
def fibonacci(n):
    if n <= 1:          # Base case
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(10))  # 55

# Example 3: Sum of digits
def digit_sum(n):
    if n == 0:          # Base case
        return 0
    return n % 10 + digit_sum(n // 10)

print(digit_sum(1234))  # 10

# Example 4: Power
def power(base, exp):
    if exp == 0:        # Base case
        return 1
    return base * power(base, exp - 1)

print(power(2, 10))  # 1024
```

## 2. Recursion Limit

```python
import sys

# ============================================
# Python's default recursion limit is 1000
# ============================================
print(sys.getrecursionlimit())  # 1000

# Increase it (if needed)
sys.setrecursionlimit(10000)

# Check current limit
sys.setrecursionlimit(5000)
print(sys.getrecursionlimit())  # 5000

# ============================================
# WARNING: Deep recursion can cause stack overflow
# Python recursion is slower than iteration
# For CP: prefer iteration when possible
# ============================================

# Bad recursion (will hit limit):
def countdown(n):
    if n == 0:
        return
    countdown(n - 1)

# countdown(2000)  # RecursionError!

# Good recursion (base case is reachable):
def countdown(n):
    if n <= 0:       # Safe base case
        print("Done!")
        return
    print(n)
    countdown(n - 1)
```

## 3. Tail Recursion vs Head Recursion

```python
# ============================================
# HEAD RECURSION — recursive call at the beginning
# ============================================
def print_numbers_head(n):
    if n == 0:
        return
    print_numbers_head(n - 1)  # Recursive call BEFORE processing
    print(n)

print_numbers_head(3)
# Output: 1 2 3

# ============================================
# TAIL RECURSION — recursive call at the end
# ============================================
def print_numbers_tail(n, acc=1):
    if n == 0:
        return acc
    return print_numbers_tail(n - 1, acc * n)  # Recursive call is LAST operation

print(print_numbers_tail(5))  # 120

# ============================================
# Python does NOT optimize tail recursion!
# Unlike languages like Scheme or Haskell.
# So both head and tail recursion use stack frames.
# ============================================
```

## 4. Memoization — Avoiding Redundant Computations

```python
import sys
from functools import lru_cache, cache

# ============================================
# Problem: Naive Fibonacci is O(2^n)
# ============================================
def fib_slow(n):
    if n <= 1:
        return n
    return fib_slow(n - 1) + fib_slow(n - 2)

# fib_slow(40) takes several seconds!

# ============================================
# Solution 1: Manual memoization with dict
# ============================================
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

print(fib_memo(40))  # Instant!

# ============================================
# Solution 2: @lru_cache decorator (Python 3.2+)
# ============================================
@lru_cache(maxsize=None)  # None = unlimited cache
def fib_lru(n):
    if n <= 1:
        return n
    return fib_lru(n - 1) + fib_lru(n - 2)

print(fib_lru(100))  # 354224848179261915075 — instant!
print(fib_lru.cache_info())  # Shows hits, misses, size

# ============================================
# Solution 3: @cache decorator (Python 3.9+)
# ============================================
@cache
def fib_cache(n):
    if n <= 1:
        return n
    return fib_cache(n - 1) + fib_cache(n - 2)

print(fib_cache(100))

# ============================================
# Memoization with complex arguments
# ============================================
@lru_cache(maxsize=None)
def grid_paths(r, c):
    """Count paths in grid from (0,0) to (r,c) going only right/down"""
    if r == 0 or c == 0:
        return 1
    return grid_paths(r - 1, c) + grid_paths(r, c - 1)

print(grid_paths(10, 10))  # 184756

# ============================================
# Memoization with tuples (for 2D state)
# ============================================
@lru_cache(maxsize=None)
def knapsack(idx, weight):
    """0/1 Knapsack with memoization"""
    if idx == len(items) or weight == 0:
        return 0
    
    val, wt = items[idx]
    
    if wt > weight:
        return knapsack(idx + 1, weight)
    
    take = val + knapsack(idx + 1, weight - wt)
    skip = knapsack(idx + 1, weight)
    
    return max(take, skip)

# ============================================
# CLEARING CACHE (important for CP with multiple test cases)
# ============================================
@lru_cache(maxsize=None)
def solve(n):
    # ...
    pass

# After each test case:
solve.cache_clear()
```

## 5. Lambda Functions

```python
# ============================================
# Lambda — anonymous one-line functions
# ============================================
# syntax: lambda arguments: expression

# Regular function
def square(x):
    return x ** 2

# Lambda equivalent
square_lambda = lambda x: x ** 2

print(square_lambda(5))  # 25

# Multiple arguments
add = lambda a, b: a + b
print(add(3, 4))  # 7

# No arguments
get_pi = lambda: 3.14159

# Conditional expression
is_even = lambda x: "even" if x % 2 == 0 else "odd"
print(is_even(7))  # "odd"

# ============================================
# Lambda with sorting
# ============================================
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]

# Sort by grade (second element)
students.sort(key=lambda x: x[1])
# [('Charlie', 78), ('Alice', 85), ('Bob', 92)]

# Sort by name length
students.sort(key=lambda x: len(x[0]))

# Sort by grade descending
students.sort(key=lambda x: -x[1])

# Sort dictionaries
data = [{"name": "c", "age": 30}, {"name": "a", "age": 20}, {"name": "b", "age": 25}]
data.sort(key=lambda x: x["name"])

# ============================================
# Lambda with filter, map, reduce
# ============================================
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Filter even numbers
evens = list(filter(lambda x: x % 2 == 0, nums))

# Square all numbers
squares = list(map(lambda x: x ** 2, nums))

# Sum all numbers
from functools import reduce
total = reduce(lambda acc, x: acc + x, nums)

# ============================================
# Lambda — when NOT to use
# ============================================
# BAD: Complex logic in lambda
# This hurts readability:
process = lambda x: x ** 2 if x > 0 else -x if x < -100 else 0

# GOOD: Use regular function for complex logic
def process(x):
    if x > 0:
        return x ** 2
    elif x < -100:
        return -x
    return 0
```

## 6. Higher-Order Functions

```python
from functools import reduce

# ============================================
# map — apply function to every element
# ============================================
nums = [1, 2, 3, 4, 5]

# Convert strings to integers
str_nums = ["1", "2", "3", "4", "5"]
int_nums = list(map(int, str_nums))

# Multiple iterables
a = [1, 2, 3]
b = [10, 20, 30]
c = [100, 200, 300]
result = list(map(lambda x, y, z: x + y + z, a, b, c))
# [111, 222, 333]

# ============================================
# filter — keep elements where function returns True
# ============================================
nums = range(1, 21)

# Primes using filter
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

primes = list(filter(is_prime, range(1, 50)))

# Filter None values
data = [1, None, 2, None, 3]
clean = list(filter(None, data))  # [1, 2, 3]

# ============================================
# reduce — accumulate result
# ============================================
nums = [1, 2, 3, 4, 5]

# Sum
total = reduce(lambda acc, x: acc + x, nums)

# Product
product = reduce(lambda acc, x: acc * x, nums)

# Maximum
maximum = reduce(lambda a, b: a if a > b else b, nums)

# Flatten list of lists
nested = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda acc, lst: acc + lst, nested)
# [1, 2, 3, 4, 5, 6]

# ============================================
# sorted with key — custom sorting
# ============================================
# Sort by absolute value
nums = [-5, 3, -1, 4, -2]
sorted_nums = sorted(nums, key=abs)  # [-1, -2, 3, 4, -5]

# Sort strings by last character
words = ["apple", "banana", "cherry"]
words.sort(key=lambda x: x[-1])  # ['banana', 'apple', 'cherry']

# Sort by multiple criteria
students = [("Alice", 85), ("Bob", 92), ("Charlie", 85)]
students.sort(key=lambda x: (-x[1], x[0]))  # By grade desc, then name asc
# [('Bob', 92), ('Alice', 85), ('Charlie', 85)]

# ============================================
# all() and any()
# ============================================
nums = [2, 4, 6, 8, 10]
print(all(x % 2 == 0 for x in nums))  # True — all even

nums = [1, 2, 3, 4, 5]
print(any(x > 3 for x in nums))  # True — at least one > 3
print(all(x > 10 for x in nums))  # False — not all > 10
```

## 7. Nested Functions and Closures

```python
# ============================================
# Nested functions — function inside a function
# ============================================
def outer(msg):
    def inner():
        print(f"Message: {msg}")
    return inner

greeting = outer("Hello")
greeting()  # "Message: Hello"

# ============================================
# Closure — inner function remembers outer's variables
# ============================================
def multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = multiplier(2)
triple = multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15

# ============================================
# Closure as counter (alternative to class)
# ============================================
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c = make_counter()
print(c())  # 1
print(c())  # 2
print(c())  # 3

# ============================================
# CP Usage: Creating custom comparators
# ============================================
def make_comparator(key_func):
    """Create a comparison function for sorting"""
    def compare(a, b):
        ka, kb = key_func(a), key_func(b)
        if ka < kb:
            return -1
        elif ka > kb:
            return 1
        return 0
    return compare

# Note: Python's sorted() doesn't use compare functions
# Use key= parameter instead
```

## 8. Generator Functions with yield

```python
# ============================================
# Generators — lazy evaluation, memory efficient
# ============================================
# Regular function: returns all values at once
def get_squares_list(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result  # Returns entire list

# Generator: yields one value at a time
def get_squares_gen(n):
    for i in range(n):
        yield i ** 2  # Produces values lazily

# Usage
squares_list = get_squares_list(1000000)  # Creates huge list in memory
squares_gen = get_squares_gen(1000000)    # No memory overhead

# Iterate over generator
for s in squares_gen:
    if s > 100:
        break
    print(s)

# ============================================
# Generator with return value
# ============================================
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for i in countdown(5):
    print(i)  # 5, 4, 3, 2, 1

# ============================================
# CP Usage: Reading large input efficiently
# ============================================
def read_ints():
    for line in sys.stdin:
        for num in line.split():
            yield int(num)

# Usage:
# nums = read_ints()
# n = next(nums)
# arr = [next(nums) for _ in range(n)]

# ============================================
# CP Usage: Lazy Fibonacci generator
# ============================================
def fibonacci_gen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Get first 10 Fibonacci numbers
fib = fibonacci_gen()
first_10 = [next(fib) for _ in range(10)]
print(first_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# ============================================
# Generator expressions (like list comprehensions but lazy)
# ============================================
# List comprehension: creates entire list
squares_list = [x**2 for x in range(1000000)]  # Uses memory

# Generator expression: lazy evaluation
squares_gen = (x**2 for x in range(1000000))   # Uses almost no memory

# Sum with generator (doesn't create intermediate list)
total = sum(x**2 for x in range(1000000))
```

## 9. itertools — Powerful Iteration Tools

```python
import itertools

# ============================================
# combinations — choose k items (order doesn't matter)
# ============================================
items = [1, 2, 3, 4]
print(list(itertools.combinations(items, 2)))
# [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]

print(list(itertools.combinations(items, 3)))
# [(1,2,3), (1,2,4), (1,3,4), (2,3,4)]

# CP Usage: Check all pairs
arr = [1, 2, 3, 4, 5]
for a, b in itertools.combinations(arr, 2):
    if a + b == target:
        print(f"Found: {a} + {b}")

# ============================================
# permutations — all arrangements (order matters)
# ============================================
items = [1, 2, 3]
print(list(itertools.permutations(items)))
# [(1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,1,2), (3,2,1)]

print(list(itertools.permutations(items, 2)))
# [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]

# ============================================
# product — Cartesian product
# ============================================
print(list(itertools.product([0, 1], repeat=3)))
# [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)]

# All positions in a grid
print(list(itertools.product(range(3), range(3))))
# [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

# ============================================
# chain — concatenate iterables
# ============================================
a = [1, 2, 3]
b = [4, 5, 6]
c = [7, 8, 9]
combined = list(itertools.chain(a, b, c))
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Flattening nested lists
nested = [[1, 2], [3, 4], [5, 6]]
flat = list(itertools.chain.from_iterable(nested))
# [1, 2, 3, 4, 5, 6]

# ============================================
# groupby — group consecutive elements
# ============================================
data = [("a", 1), ("a", 2), ("b", 3), ("b", 4), ("a", 5)]
data.sort(key=lambda x: x[0])  # MUST sort first!

for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# a [('a', 1), ('a', 2), ('a', 5)]
# b [('b', 3), ('b', 4)]

# Group by length
words = ["hi", "hello", "hey", "hola", "howdy"]
words.sort(key=len)
for length, group in itertools.groupby(words, key=len):
    print(f"Length {length}: {list(group)}")
# Length 2: ['hi', 'hey']
# Length 3: ['hola']
# Length 5: ['hello', 'howdy']

# ============================================
# accumulate — running accumulation
# ============================================
nums = [1, 2, 3, 4, 5]
print(list(itertools.accumulate(nums)))
# [1, 3, 6, 10, 15] — running sum

import operator
print(list(itertools.accumulate(nums, operator.mul)))
# [1, 2, 6, 24, 120] — running product

# Running maximum
print(list(itertools.accumulate(nums, max)))
# [1, 2, 3, 4, 5]

# ============================================
# permutations for CP
# ============================================
# Check all permutations of a string
def all_permutations(s):
    return [''.join(p) for p in itertools.permutations(s)]

# All binary strings of length n
binary_strings = list(itertools.product('01', repeat=3))
# ['000', '001', '010', '011', '100', '101', '110', '111']

# ============================================
# Combinations with replacement
# ============================================
print(list(itertools.combinations_with_replacement([1, 2, 3], 2)))
# [(1,1), (1,2), (1,3), (2,2), (2,3), (3,3)]
```

## 10. Advanced Recursion Patterns

```python
# ============================================
# Pattern 1: Recursive backtracking
# ============================================
def subsets(nums):
    """Generate all subsets of nums"""
    result = []
    
    def backtrack(start, current):
        result.append(current[:])  # Copy current subset
        
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()  # Undo choice
    
    backtrack(0, [])
    return result

print(subsets([1, 2, 3]))
# [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]

# ============================================
# Pattern 2: N-Queens
# ============================================
def solve_n_queens(n):
    """Find all solutions to N-Queens problem"""
    results = []
    board = [-1] * n  # board[i] = column of queen in row i
    
    def is_safe(row, col):
        for prev_row in range(row):
            prev_col = board[prev_row]
            if prev_col == col or abs(prev_row - row) == abs(prev_col - col):
                return False
        return True
    
    def backtrack(row):
        if row == n:
            results.append(board[:])
            return
        
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1
    
    backtrack(0)
    return results

solutions = solve_n_queens(4)
print(f"Found {len(solutions)} solutions")
# [[1, 3, 0, 2], [2, 0, 3, 1]]

# ============================================
# Pattern 3: Generate parentheses
# ============================================
def generate_parentheses(n):
    result = []
    
    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(current)
            return
        
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)
    
    backtrack('', 0, 0)
    return result

print(generate_parentheses(3))
# ['((()))', '(()())', '(())()', '()(())', '()()()']

# ============================================
# Pattern 4: Word search in grid
# ============================================
def word_search(board, word):
    rows, cols = len(board), len(board[0])
    
    def dfs(r, c, idx):
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != word[idx]:
            return False
        
        temp = board[r][c]
        board[r][c] = '#'  # Mark visited
        
        found = (dfs(r+1, c, idx+1) or
                 dfs(r-1, c, idx+1) or
                 dfs(r, c+1, idx+1) or
                 dfs(r, c-1, idx+1))
        
        board[r][c] = temp  # Restore
        return found
    
    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False

board = [['A','B','C','E'],
         ['S','F','C','S'],
         ['A','D','E','E']]
print(word_search(board, "ABCCED"))  # True
```
