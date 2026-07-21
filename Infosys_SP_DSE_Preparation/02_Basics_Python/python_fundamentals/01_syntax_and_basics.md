# Python Syntax and Basics for Competitive Programming

## 1. Variables and Data Types

Python is dynamically typed — no need to declare variable types.

```python
# Variable assignment
n = 10              # int
pi = 3.14           # float
name = "Python"     # str
is_active = True    # bool
nothing = None      # NoneType

# Multiple assignment
a, b, c = 1, 2, 3
x = y = z = 0

# Type checking
print(type(n))      # <class 'int'>
print(type(pi))     # <class 'float'>

# Python integers have arbitrary precision — no overflow
big = 10**100
print(big)          # Works perfectly, no overflow
```

### Data Type Summary

```python
# int: unlimited precision
a = 999999999999999999999999999999

# float: double precision (64-bit), can lose precision
b = 0.1 + 0.2  # 0.30000000000000004

# bool: subclass of int (True=1, False=0)
print(True + True)  # 2
print(False * 10)   # 0

# str: immutable sequence of Unicode characters
s = "hello"

# None: null value
result = None
```

## 2. Type Casting

```python
# Explicit type conversion
x = "42"
n = int(x)          # 42
f = float(x)        # 42.0
s = str(42)         # "42"

# String to list of chars
chars = list("abc")  # ['a', 'b', 'c']

# List to string
word = "".join(chars)  # "abc"

# Int to binary string
bin_str = bin(10)    # '0b1010'
hex_str = hex(255)   # '0xff'
oct_str = oct(8)     # '0o10'

# Binary string to int
n = int("1010", 2)   # 10
n = int("ff", 16)    # 255

# Float to int (truncates toward zero)
print(int(3.7))      # 3
print(int(-3.7))     # -3
```

## 3. Input/Output — Fast I/O for CP

```python
import sys

# ============================================
# SLOW: For interactive / non-CP use
# ============================================
n = int(input())
a = list(map(int, input().split()))

# ============================================
# FAST: For competitive programming
# ============================================
input = sys.stdin.readline  # Override built-in input

# Reading a single integer
n = int(input())

# Reading a line of space-separated integers
a = list(map(int, input().split()))

# Reading multiple lines of integers
data = sys.stdin.read().split()
nums = list(map(int, data))

# ============================================
# Fast Output
# ============================================
# print() is fine for most cases, but for massive output:
output = []
for i in range(n):
    output.append(str(result))
sys.stdout.write("\n".join(output))

# ============================================
# Full Fast I/O Template
# ============================================
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        # Solution here
        print(result)

if __name__ == "__main__":
    main()
```

## 4. String Operations

```python
# ============================================
# String Creation and Basics
# ============================================
s = "Hello, World!"
s2 = 'Single quotes work too'
s3 = """Triple quotes
span multiple
lines"""

# f-strings (Python 3.6+) — fastest formatting
name = "Alice"
age = 25
print(f"{name} is {age} years old")  # "Alice is 25 years old"
print(f"{3.14159:.2f}")              # "3.14"

# % formatting (old style)
print("Name: %s, Age: %d" % (name, age))

# .format() method
print("Name: {}, Age: {}".format(name, age))

# ============================================
# String Slicing
# ============================================
s = "Python"
# s[start:stop:step]
print(s[0])      # 'P'       — first char
print(s[-1])     # 'n'       — last char
print(s[0:3])    # 'Pyt'     — index 0,1,2
print(s[2:])     # 'thon'    — from index 2 to end
print(s[:3])     # 'Pyt'     — first 3 chars
print(s[::2])    # 'Pto'     — every 2nd char
print(s[::-1])   # 'nohtyP'  — reversed string

# ============================================
# String Methods (all return new strings — strings are immutable)
# ============================================
s = "  Hello, World!  "

print(s.strip())         # "Hello, World!"  — removes whitespace
print(s.lower())         # "  hello, world!  "
print(s.upper())         # "  HELLO, WORLD!  "
print(s.replace("World", "Python"))  # "  Hello, Python!  "
print(s.split(","))      # ['  Hello', ' World!  ']
print(s.find("World"))   # 9 (index), -1 if not found
print(s.count("l"))      # 3
print(s.startswith("  H"))  # True
print(s.endswith("!  "))    # True

# Joining — efficient string concatenation
words = ["Python", "is", "awesome"]
print(" ".join(words))           # "Python is awesome"
print(",".join(["a", "b", "c"])) # "a,b,c"

# ============================================
# String Checking
# ============================================
print("abc".isalpha())   # True
print("123".isdigit())   # True
print("abc123".isalnum())  # True
print("  ".isspace())     # True
```

## 5. Operators

```python
# ============================================
# Arithmetic Operators
# ============================================
a, b = 17, 5
print(a + b)    # 22    — addition
print(a - b)    # 12    — subtraction
print(a * b)    # 85    — multiplication
print(a / b)    # 3.4   — true division (always float)
print(a // b)   # 3     — floor division
print(a % b)    # 2     — modulo
print(a ** b)   # 1419857  — exponentiation

# IMPORTANT: // does floor division (rounds toward -infinity)
print(-7 // 2)  # -4, NOT -3
print(-7 % 2)   # 1,  NOT -1

# ============================================
# Comparison Operators
# ============================================
# ==  !=  >  <  >=  <=
# Chained comparisons (Pythonic!)
x = 5
print(1 < x < 10)       # True
print(1 < x < 3)        # False
print(1 <= x <= 5)      # True

# ============================================
# Logical Operators
# ============================================
# and, or, not
# Short-circuit evaluation:
#   a and b → returns first falsy value, or last if all truthy
#   a or b  → returns first truthy value, or last if all falsy
print(0 and 5)    # 0
print(3 or 5)     # 3
print("" or "hi") # "hi"
print(None or []) # []
print([] or None) # None

# In CP, use: if x and y:  instead of  if x != 0 and y != 0:

# ============================================
# Bitwise Operators
# ============================================
a, b = 12, 10  # a=1100, b=1010

print(a & b)    # 8     — AND  (1000)
print(a | b)    # 14    — OR   (1110)
print(a ^ b)    # 6     — XOR  (0110)
print(~a)       # -13   — NOT  (bitwise complement)
print(a << 2)   # 48    — left shift  (110000)
print(a >> 2)   # 3     — right shift (11)

# Common bit tricks:
# Check if n is power of 2:  n > 0 and (n & (n - 1)) == 0
# Get ith bit:               (n >> i) & 1
# Set ith bit:               n | (1 << i)
# Clear ith bit:             n & ~(1 << i)
# Count set bits:            bin(n).count('1')
```

## 6. Conditional Statements

```python
# Basic if-elif-else
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

# Ternary expression (one-liner if-else)
x = 10
result = "even" if x % 2 == 0 else "odd"

# Pythonic conditional assignment
a, b = 5, 3
# Swap without temp variable
a, b = b, a

# Max/min of multiple values
print(max(a, b, 10, 20))  # 20
print(min(a, b, 1, 2))    # 1

# Conditional in list (useful for CP)
arr = [1 if x % 2 == 0 else x for x in range(10)]
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] → even numbers replaced with 1
```

## 7. Loops

```python
# ============================================
# For Loop
# ============================================
# Range
for i in range(5):         # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 8):      # 2, 3, 4, 5, 6, 7
    print(i)

for i in range(0, 10, 3):  # 0, 3, 6, 9
    print(i)

for i in range(10, 0, -1): # 10, 9, 8, ..., 1
    print(i)

# Iterating over list
arr = [10, 20, 30]
for i in range(len(arr)):
    print(f"index {i}: {arr[i]}")

# More Pythonic:
for i, val in enumerate(arr):
    print(f"index {i}: {val}")

# Iterating over string
for ch in "hello":
    print(ch)

# ============================================
# While Loop
# ============================================
n = 10
while n > 0:
    print(n)
    n -= 1

# ============================================
# Break, Continue, Else
# ============================================
# break — exit the loop immediately
for i in range(100):
    if i == 5:
        break  # stops at 5

# continue — skip to next iteration
for i in range(10):
    if i % 2 == 0:
        continue  # skip even numbers
    print(i)  # prints 1, 3, 5, 7, 9

# else — runs if loop completes WITHOUT break
def find_prime_factors(n):
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True  # No factor found → it's prime

# else on while
n = 5
while n > 0:
    n -= 1
else:
    print("Loop completed normally")

# ============================================
# Nested Loops — Pattern Printing
# ============================================
n = 5
for i in range(1, n + 1):
    print("*" * i)
# *
# **
# ***
# ****
# *****
```

## 8. List Comprehension

```python
# ============================================
# Basic List Comprehension
# ============================================
# [expression for item in iterable if condition]

# Squares of even numbers
squares = [x**2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]

# Flatten 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Map + filter in one line
result = [x * 2 for x in range(10) if x > 5]
# [12, 14, 16, 18]

# ============================================
# Dict Comprehension
# ============================================
# {key_expr: value_expr for item in iterable if condition}

# Index mapping
chars = "abcde"
char_index = {ch: i for i, ch in enumerate(chars)}
# {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}

# Frequency count
arr = [1, 2, 2, 3, 3, 3]
freq = {x: arr.count(x) for x in set(arr)}
# {1: 1, 2: 2, 3: 3}  — but use Counter in practice

# ============================================
# Set Comprehension
# ============================================
# {expr for item in iterable if condition}

nums = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squares = {x**2 for x in nums}
# {1, 4, 9, 16}
```

## 9. Lambda Functions, Map, Filter, Reduce

```python
from functools import reduce

# ============================================
# Lambda Functions
# ============================================
# lambda arguments: expression
square = lambda x: x ** 2
add = lambda a, b: a + b
print(square(5))  # 25
print(add(3, 4))  # 7

# Useful for sorting with custom keys
pairs = [(1, 'b'), (3, 'a'), (2, 'c')]
pairs.sort(key=lambda x: x[1])  # Sort by second element
# [(3, 'a'), (1, 'b'), (2, 'c')]

# ============================================
# Map — apply function to every element
# ============================================
nums = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, nums))
# [1, 4, 9, 16, 25]

# map with multiple iterables
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))
# [11, 22, 33]

# Practical: reading integers from input
nums = list(map(int, input().split()))

# ============================================
# Filter — keep elements where function returns True
# ============================================
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, nums))
# [2, 4, 6, 8, 10]

# Filter out None values
data = [1, None, 3, None, 5]
clean = list(filter(None, data))  # [1, 3, 5]

# ============================================
# Reduce — accumulate result from all elements
# ============================================
nums = [1, 2, 3, 4, 5]
total = reduce(lambda acc, x: acc + x, nums)  # 15
product = reduce(lambda acc, x: acc * x, nums)  # 120

# Find maximum without built-in max()
maximum = reduce(lambda a, b: a if a > b else b, nums)
# 5
```

## 10. Exception Handling

```python
# ============================================
# Basic try-except
# ============================================
try:
    n = int(input())
    result = 10 / n
except ValueError:
    print("Invalid input — not a number")
except ZeroDivisionError:
    print("Cannot divide by zero")

# ============================================
# Catching all exceptions
# ============================================
try:
    # some code
    risky_operation()
except Exception as e:
    print(f"Error: {e}")

# ============================================
# try-except-else-finally
# ============================================
try:
    f = open("data.txt", "r")
    data = f.read()
except FileNotFoundError:
    print("File not found")
else:
    # Runs only if no exception occurred
    print("File read successfully")
finally:
    # Always runs — cleanup code
    print("Done")

# ============================================
# Raising exceptions
# ============================================
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    return age

try:
    validate_age(-5)
except ValueError as e:
    print(e)  # "Age cannot be negative"

# ============================================
# Exception handling in CP
# ============================================
# Often used to handle edge cases quickly
def safe_divide(a, b):
    try:
        return a // b
    except ZeroDivisionError:
        return 0  # or some default

# Using assert for debugging
def solve(n, arr):
    assert n == len(arr), "n must equal array length"
    # ... solution
```

## 11. Quick Reference — CP Input Patterns

```python
import sys
input = sys.stdin.readline

# Pattern 1: Single integer
n = int(input())

# Pattern 2: Array of integers
arr = list(map(int, input().split()))

# Pattern 3: Grid
grid = [list(map(int, input().split())) for _ in range(n)]

# Pattern 4: Multiple test cases
t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    print(solve(n, arr))

# Pattern 5: Read everything at once (fastest)
data = sys.stdin.buffer.read().split()
it = iter(data)
n = int(next(it))
arr = [int(next(it)) for _ in range(n)]
```

## 12. Common CP Code Snippets

```python
# GCD and LCM
import math
from math import gcd
from math import lcm  # Python 3.9+

a, b = 12, 8
g = gcd(a, b)         # 4
l = (a * b) // g      # 24

# Modular exponentiation
def power(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result

# Check prime
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# Sieve of Eratosthenes
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return is_prime

# Binary Search
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
```
