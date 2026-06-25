# Python 500+ Interview Questions & Answers

> **Target:** YC Startups / Top Tech Companies  
> **Covers:** Python Basics, OOP, Advanced Python, Internals, Data Science, FastAPI, Coding Problems, Gotchas

---

## Python Basics (Q1-Q80)

### Q1: What are the primitive data types in Python?
**Answer:**
Python has several built-in data types:
- **int**: Integer values (`x = 5`)
- **float**: Floating-point numbers (`x = 3.14`)
- **complex**: Complex numbers (`x = 1+2j`)
- **bool**: Boolean values (`True`, `False`) — subclasses of int
- **str**: String (`x = "hello"`)
- **bytes**: Byte sequences (`x = b"hello"`)
- **bytearray**: Mutable byte array
- **NoneType**: Represents `None` (singleton)
- **list**: Mutable ordered collection
- **tuple**: Immutable ordered collection
- **set**: Unordered collection of unique elements
- **frozenset**: Immutable set
- **dict**: Key-value mapping

Python is dynamically typed — variables can change type at runtime:
```python
x = 5       # int
x = "hello" # now str
```

### Q2: How does type conversion work in Python?
**Answer:**
Type conversion can be implicit (coercion) or explicit (casting).

**Implicit conversion** happens automatically for compatible types:
```python
x = 5      # int
y = 3.14   # float
z = x + y  # 8.14 (float) — int promoted to float
```

**Explicit conversion** uses type constructors:
```python
int("42")        # 42
float("3.14")    # 3.14
str(42)          # "42"
list("hello")    # ['h', 'e', 'l', 'l', 'o']
tuple([1, 2, 3]) # (1, 2, 3)
set([1, 2, 2])   # {1, 2}
bool(0)          # False
bool(1)          # True
bool([])         # False — empty collections are falsy
```

**Dangerous conversions:**
```python
int("hello")  # ValueError
int("3.14")   # ValueError — use float() first
```

### Q3: What is the difference between mutable and immutable objects?
**Answer:**
**Mutable objects** can be changed after creation:
```python
lst = [1, 2, 3]
lst[0] = 99  # Works
lst.append(4)
```

**Immutable objects** cannot be changed after creation:
```python
tup = (1, 2, 3)
tup[0] = 99  # TypeError: 'tuple' object does not support item assignment
```

**Mutable types:** list, dict, set, bytearray, user-defined classes
**Immutable types:** int, float, complex, str, tuple, frozenset, bytes, NoneType, bool

When you "modify" an immutable object, a new object is created:
```python
s = "hello"
s += " world"  # Creates a new string, doesn't modify original
```

### Q4: How does Python manage memory?
**Answer:**
Python uses:
1. **Private heap**: All objects live in a private heap, managed by the memory manager
2. **Reference counting**: Each object tracks how many references point to it. When count reaches 0, it's deallocated
3. **Garbage collection**: The `gc` module handles cyclic references (objects referencing each other)

```python
import sys
x = []
sys.getrefcount(x)  # More than 1 due to function argument

import gc
gc.collect()  # Force garbage collection
```

### Q5: What are string slicing and common string methods?
**Answer:**
**Slicing syntax:** `string[start:stop:step]`
```python
s = "hello world"
s[0]        # 'h'
s[-1]       # 'd'
s[0:5]      # 'hello'
s[6:]       # 'world'
s[::-1]     # 'dlrow olleh' (reverse)
s[::2]      # 'hlowrd'
```

**Common string methods:**
```python
"hello".upper()           # 'HELLO'
"HELLO".lower()           # 'hello'
" hello ".strip()         # 'hello'
"hello world".split()     # ['hello', 'world']
" ".join(["a", "b"])      # 'a b'
"hello".replace("l", "x") # 'hexxo'
"hello".find("l")         # 2 (index, -1 if not found)
"hello".count("l")        # 2
"hello".startswith("he")  # True
"hello".endswith("lo")    # True
"hello123".isalpha()      # False
"hello".isalpha()         # True
```

### Q6: How do list comprehensions work? Give examples.
**Answer:**
List comprehensions provide a concise way to create lists:
```python
# Basic: [expression for item in iterable]
[x**2 for x in range(5)]          # [0, 1, 4, 9, 16]

# With condition: [expression for item in iterable if condition]
[x**2 for x in range(10) if x % 2 == 0]  # [0, 4, 16, 36, 64]

# Nested loops
[(x, y) for x in [1, 2] for y in [3, 4]]  # [(1,3), (1,4), (2,3), (2,4)]

# With if-else
["even" if x % 2 == 0 else "odd" for x in range(5)]
```

Equivalent to:
```python
result = []
for x in range(10):
    if x % 2 == 0:
        result.append(x**2)
```

**Set comprehensions** and **dict comprehensions**:
```python
{x for x in [1, 1, 2, 3]}        # {1, 2, 3}
{x: x**2 for x in range(5)}      # {0:0, 1:1, 2:4, 3:9, 4:16}
```

### Q7: What is the difference between list, tuple, set, and dict?
**Answer:**
| Feature | list | tuple | set | dict |
|---------|------|-------|-----|------|
| Mutable | Yes | No | Yes | Yes |
| Ordered | Yes (insertion) | Yes | No (Python <3.7), insertion order (3.7+) | Insertion order (3.7+) |
| Indexed | Yes | Yes | No | By key |
| Duplicates | Allowed | Allowed | No | No (keys) |
| Syntax | `[1, 2]` | `(1, 2)` | `{1, 2}` | `{1: 'a'}` |

```python
lst = [1, 2, 2, 3]
lst.append(4)

tup = (1, 2, 2, 3)
# tup[0] = 99  # TypeError

st = {1, 2, 3}
st.add(4)

d = {"a": 1, "b": 2}
d["c"] = 3
```

### Q8: Explain range(), enumerate(), and zip().
**Answer:**
**range(start, stop, step)**:
```python
list(range(5))            # [0, 1, 2, 3, 4]
list(range(2, 5))         # [2, 3, 4]
list(range(0, 10, 2))     # [0, 2, 4, 6, 8]
```

**enumerate(iterable, start=0)** — yields (index, value) pairs:
```python
for i, char in enumerate("hello"):
    print(i, char)
```

**zip(*iterables)** — aggregates elements from multiple iterables:
```python
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
list(zip(names, ages))  # [('Alice', 25), ('Bob', 30), ('Charlie', 35)]

# Unzipping
letters, numbers = zip(*[('a', 1), ('b', 2)])  # ('a', 'b'), (1, 2)
```

### Q9: Explain function parameters, return values, and scope in Python.
**Answer:**
**Parameters:**
```python
def func(a, b=2, *args, kw1, kw2=5, **kwargs):
    print(a, b, args, kw1, kw2, kwargs)

func(1, 2, 3, 4, kw1=10, extra=99)
# 1 2 (3, 4) 10 5 {'extra': 99}
```

**Return values:**
```python
def multi_return():
    return 1, 2, 3  # Returns a tuple

a, b, c = multi_return()
```

**Scope (LEGB rule):** Local → Enclosing → Global → Built-in
```python
x = "global"
def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)  # local
    inner()
outer()
```

### Q10: What are closures in Python?
**Answer:**
A closure is a function that remembers variables from its enclosing scope:
```python
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))  # 10
print(triple(5))  # 15
```

Closures are useful for data hiding, function factories, decorators, and callbacks.

### Q11: What are lambda functions?
**Answer:**
Lambda functions are anonymous, single-expression functions:
```python
square = lambda x: x ** 2
print(square(5))  # 25

numbers = [1, 2, 3, 4]
list(map(lambda x: x * 2, numbers))     # [2, 4, 6, 8]
list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]
sorted([(1, 2), (3, 1), (2, 3)], key=lambda x: x[1])
```

### Q12: How does try/except/else/finally work?
**Answer:**
```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Generic catch: {e}")
else:
    print(f"No exception, result: {result}")
finally:
    print("Always executes")
```
- `else` runs only if no exception
- `finally` always runs (cleanup)
- Most specific exceptions first

### Q13: How do you create custom exceptions?
**Answer:**
```python
class ValidationError(Exception):
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

def validate_age(age):
    if age < 0:
        raise ValidationError("age", "must be positive")
```

### Q14: Explain raise and assert.
**Answer:**
```python
raise ValueError("error")  # Explicit exception
raise                       # Re-raise current exception

assert x > 0, "Must be positive"  # Raises AssertionError
```
Note: `assert` disabled with `-O` flag. Don't use for production validation.

### Q15: How do you read and write files in Python?
**Answer:**
```python
# Writing
with open("file.txt", "w") as f:
    f.write("Hello, World!\n")

# Reading
with open("file.txt", "r") as f:
    content = f.read()

# Line by line
with open("file.txt", "r") as f:
    for line in f:
        print(line.strip())

# Append
with open("file.txt", "a") as f:
    f.write("appended\n")
```

### Q16: What are context managers (with statement)?
**Answer:**
Context managers manage resources with automatic setup/teardown:
```python
with open("file.txt", "r") as f:
    content = f.read()  # Auto-closed

# Custom context manager
class ManagedFile:
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
```

### Q17: How do you work with JSON in Python?
**Answer:**
```python
import json

# Serialize
data = {"name": "Alice", "age": 30}
json_str = json.dumps(data, indent=2)

# Deserialize
parsed = json.loads(json_str)

# File I/O
with open("data.json", "w") as f:
    json.dump(data, f)
with open("data.json") as f:
    data = json.load(f)
```

### Q18: How do you work with CSV in Python?
**Answer:**
```python
import csv

# Reading
with open("data.csv", "r") as f:
    for row in csv.reader(f):
        print(row)

# Writing
with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
    writer.writerow(["Alice", 30])
```

### Q19: What is `if __name__ == "__main__":`?
**Answer:**
It checks whether a script is run directly or imported:
```python
def main():
    print("Running directly")

if __name__ == "__main__":
    main()
```
- `__name__` is `"__main__"` when executed directly
- `__name__` is the module name when imported

### Q20: How does the Python import system work?
**Answer:**
Python uses finders and loaders via `sys.meta_path`:
1. Built-in modules (BuiltinImporter)
2. Frozen modules (FrozenImporter)
3. Path-based (PathFinder - searches `sys.path`)

```python
import sys
sys.path   # Search path
sys.modules  # Loaded modules cache
```

### Q21: What are variables and naming conventions in Python?
**Answer:**
Variables are names referencing objects:
```python
x = 5   # x references integer 5
y = x   # y references same object
```

**PEP 8 naming:**
- `snake_case` for variables/functions
- `CamelCase` for classes
- `UPPER_CASE` for constants
- `_private` / `__private` / `__dunder__`

### Q22: Explain boolean operations and short-circuit evaluation.
**Answer:**
```python
True and False  # False
True or False   # True
not True        # False
```

**Short-circuit:**
- `a and b` — if `a` is falsy, returns `a` (doesn't evaluate `b`)
- `a or b` — if `a` is truthy, returns `a` (doesn't evaluate `b`)

**Falsy values:** `False`, `0`, `""`, `[]`, `{}`, `()`, `None`

### Q23: What is type() and isinstance()?
**Answer:**
```python
type(5)           # <class 'int'>
isinstance(5, int)  # True

# isinstance handles inheritance (type doesn't)
class A: pass
class B(A): pass
isinstance(B(), A)  # True
type(B()) == A      # False
```

### Q24: Explain the global and nonlocal keywords.
**Answer:**
```python
counter = 0
def increment():
    global counter
    counter += 1

def outer():
    x = 0
    def inner():
        nonlocal x
        x += 1
    return inner
```

### Q25: How do you handle multiple exceptions in one except block?
**Answer:**
```python
try:
    result = risky_operation()
except (ValueError, TypeError, RuntimeError) as e:
    print(f"Caught: {e}")
```

### Q26: What is the purpose of else in try/except?
**Answer:**
`else` runs only when no exception occurs:
```python
try:
    file = open("data.txt")
except FileNotFoundError:
    print("File not found")
else:
    content = file.read()  # Only if file opened
finally:
    file.close()
```

### Q27: How do file modes work in Python?
**Answer:**
| Mode | Read | Write | Create | Truncate |
|------|------|-------|--------|----------|
| `r` | Yes | No | No | No |
| `w` | No | Yes | Yes | Yes |
| `a` | No | Yes | Yes | No |
| `r+` | Yes | Yes | No | No |
| `w+` | Yes | Yes | Yes | Yes |
| `a+` | Yes | Yes | Yes | No |
| `x` | No | Yes | Yes* | No |
| `t` | Text (default) | | | |
| `b` | Binary | | | |

### Q28: What is the difference between read(), readline(), and readlines()?
**Answer:**
```python
with open("file.txt") as f:
    content = f.read()       # Entire file as string
    line = f.readline()      # Next line
    lines = f.readlines()    # List of all lines
# Best: for line in f:  # Memory efficient
```

### Q29: Explain pickling in Python.
**Answer:**
```python
import pickle
data = {"key": [1, 2, 3]}
bytes_data = pickle.dumps(data)
restored = pickle.loads(bytes_data)
```
Caveats: Not secure (never unpickle untrusted data), Python-version-specific.

### Q30: What's the difference between is and ==?
**Answer:**
- `==` checks **value equality**
- `is` checks **identity** (same object)

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b  # True
a is b  # False

x is None  # Use is for None
```

### Q31: What is the difference between del and remove()?
**Answer:**
```python
lst = [1, 2, 3, 2, 4]
del lst[0]         # Remove by index: [2, 3, 2, 4]
lst.remove(2)      # Remove by value (first): [3, 2, 4]
lst.pop()          # Remove & return last: 4
lst.pop(0)         # Remove & return by index: 3
```

### Q32: Explain the copy module (shallow vs deep copy).
**Answer:**
```python
import copy
original = [[1, 2], [3, 4]]
shallow = copy.copy(original)     # New outer, shared inner
deep = copy.deepcopy(original)    # Completely independent

shallow[0][0] = 99
original[0][0]  # 99 (affected!)
```

### Q33: What are f-strings and how do they work?
**Answer:**
```python
name = "Alice"
f"Hello, {name}!"                     # 'Hello, Alice!'
f"2 + 2 = {2 + 2}"                    # '2 + 2 = 4'
f"Pi is {3.14159:.2f}"               # 'Pi is 3.14'
f"{'hello':>10}"                      # '     hello'
```

### Q34: How do you swap two variables in Python?
**Answer:**
```python
a, b = b, a
x, y, z = z, x, y  # Multiple swap
```

### Q35: Explain the input() function.
**Answer:**
```python
name = input("Enter name: ")  # Always returns str
age = int(input("Enter age: "))  # Must convert
```
Never use `eval(input())` — executes arbitrary code.

### Q36: What is the pass statement?
**Answer:**
`pass` is a no-op placeholder:
```python
def not_implemented():
    pass
class MyClass:
    pass
```

### Q37: Explain break and continue.
**Answer:**
```python
for i in range(10):
    if i == 5: break     # Exits loop at 5
    if i % 2: continue   # Skip odd numbers
    print(i)  # 0, 2, 4
```

### Q38: How does the else clause work on loops?
**Answer:**
`else` runs when loop completes normally (no `break`):
```python
for item in items:
    if found: break
else:
    print("Not found")  # Only runs if no break
```

### Q39: What is the difference between append() and extend()?
**Answer:**
```python
lst = [1, 2, 3]
lst.append([4, 5])   # [1, 2, 3, [4, 5]]
lst.extend([4, 5])   # [1, 2, 3, 4, 5]
lst += [6, 7]        # Extends
```

### Q40: How do you sort lists and dictionaries?
**Answer:**
```python
lst.sort()                    # In-place
sorted(lst)                   # New list
sorted(lst, key=len)          # Custom key
sorted(lst, reverse=True)     # Descending

d = {"b": 2, "a": 1}
sorted(d.items(), key=lambda x: x[1])  # Sort by value
```

### Q41: Explain dictionary operations and methods.
**Answer:**
```python
d = {"a": 1, "b": 2}
d.get("c", 0)         # 0 (default)
d.setdefault("c", [])   # Get or create
d.pop("a")            # Remove and return
d.update({"b": 99})   # Merge
{k: v for k, v in d.items()}

# Python 3.9+ merge
d1 | d2               # Merge
d1 |= d2              # In-place merge
```

### Q42: What is the difference between dict.get() and dict[key]?
**Answer:**
```python
d = {"a": 1}
d["a"]      # 1
d["b"]      # KeyError!
d.get("b")  # None (no error)
d.get("b", 0)  # 0 (custom default)
```

### Q43: What are set operations in Python?
**Answer:**
```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
a | b  # Union: {1,2,3,4,5,6}
a & b  # Intersection: {3,4}
a - b  # Difference: {1,2}
a ^ b  # Symmetric difference: {1,2,5,6}
```

### Q44: How do you iterate over a dictionary?
**Answer:**
```python
for key in d:           # Keys
for value in d.values():  # Values
for k, v in d.items():  # Both
```
Modify while iterating: use `list(d.keys())` to create a copy.

### Q45: What is the purpose of __name__ in Python?
**Answer:**
`__name__` is `"__main__"` when run directly, module name when imported.

### Q46: Explain the zip() function in detail.
**Answer:**
```python
list(zip([1, 2], [3, 4]))  # [(1, 3), (2, 4)]
list(zip([1, 2], [3, 4, 5]))  # [(1, 3), (2, 4)] (shortest)

# Unzip
pairs = [('a', 1), ('b', 2)]
letters, nums = zip(*pairs)

# Create dict
dict(zip(keys, values))

# Transpose matrix
matrix = [[1, 2], [3, 4]]
list(zip(*matrix))  # [(1, 3), (2, 4)]
```

### Q47: Explain map(), filter(), and reduce().
**Answer:**
```python
list(map(str.upper, ["a", "b"]))     # ['A', 'B']
list(filter(lambda x: x > 0, [-1, 2]))  # [2]

from functools import reduce
reduce(lambda a, b: a * b, [1, 2, 3, 4])  # 24
```

### Q48: Explain any() and all() built-ins.
**Answer:**
```python
any([False, True, False])  # True
all([True, 1, "hello"])    # True
all(x > 0 for x in nums)   # Check all positive
```

### Q49: What is the with statement and how does it work?
**Answer:**
Manages context managers via `__enter__` and `__exit__`:
```python
with open("file.txt") as f:
    data = f.read()
# Equivalent:
f = open("file.txt").__enter__()
try:
    data = f.read()
finally:
    f.__exit__(...)
```

### Q50: How do you create a virtual environment?
**Answer:**
```bash
python3 -m venv myenv
source myenv/bin/activate  # Linux/Mac
deactivate
```

### Q51: What are pip and requirements.txt?
**Answer:**
```bash
pip install requests==2.25.1
pip freeze > requirements.txt
pip install -r requirements.txt
```

### Q52: What are bytes and bytearray in Python?
**Answer:**
```python
b = b"hello"                    # Immutable bytes
ba = bytearray(b"hello")        # Mutable bytearray
ba[0] = 72                      # b"Hello"
```

### Q53: How do you convert between bytes and strings?
**Answer:**
```python
"hello".encode("utf-8")           # b"hello"
b"hello".decode("utf-8")          # "hello"
```

### Q54: What is the difference between str() and repr()?
**Answer:**
```python
# str() - human-readable
# repr() - unambiguous (should recreate object)
import datetime
str(datetime.now())    # '2024-03-15 10:30:00'
repr(datetime.now())   # 'datetime.datetime(2024, 3, 15, 10, 30, 0)'
```

### Q55: What is the [::-1] slicing syntax?
**Answer:**
```python
"hello"[::-1]   # 'olleh' (reverse)
[1, 2, 3][::-1] # [3, 2, 1]
```

### Q56: How do you check the size of an object?
**Answer:**
```python
import sys
sys.getsizeof(42)       # 28 (approx)
```

### Q57: What are the common string formatting methods?
**Answer:**
```python
f"{name} is {age}"           # f-strings (preferred)
"{} is {}".format(name, age)  # str.format()
"%s is %d" % (name, age)      # %-formatting
```

### Q58: How do you use match statement (Python 3.10+)?
**Answer:**
```python
match value:
    case 1: print("one")
    case 2: print("two")
    case _: print("other")
```

### Q59: What is the difference between __str__ and __repr__?
**Answer:**
```python
def __str__(self):  # User-friendly
    return f"Person({self.name})"
def __repr__(self):  # Developer-friendly
    return f"Person('{self.name}', {self.age})"
```

### Q60: What are truthy and falsy values?
**Answer:**
**Falsy:** `False`, `0`, `0.0`, `""`, `[]`, `{}`, `()`, `set()`, `None`, `range(0)`
**Truthy:** Everything else.

### Q61: How do you flatten a list of lists?
**Answer:**
```python
nested = [[1, 2], [3, 4, 5], [6]]
flat = [x for sublist in nested for x in sublist]  # [1,2,3,4,5,6]

from itertools import chain
list(chain.from_iterable(nested))
```

### Q62: How do you transpose a matrix?
**Answer:**
```python
matrix = [[1, 2, 3], [4, 5, 6]]
list(zip(*matrix))  # [(1, 4), (2, 5), (3, 6)]
```

### Q63: What is the walrus operator :=?
**Answer:**
Assigns within expressions (Python 3.8+):
```python
if (n := len(data)) > 10:
    print(f"Large: {n}")

while (line := file.readline()):
    print(line.strip())
```

### Q64: What is the difference between @staticmethod and @classmethod?
**Answer:**
```python
class MyClass:
    @classmethod
    def class_method(cls):    # Receives class
        return cls
    @staticmethod
    def static_method():      # No special first arg
        return "static"
```

### Q65: How do you create a list of unique elements while preserving order?
**Answer:**
```python
def unique(seq):
    return list(dict.fromkeys(seq))  # Python 3.7+
```

### Q66: What are __init__ and __new__?
**Answer:**
```python
class Point:
    def __new__(cls, x, y):     # Creates instance
        return super().__new__(cls)
    def __init__(self, x, y):   # Initializes instance
        self.x, self.y = x, y
```

### Q67: How do you handle keyboard interrupt (Ctrl+C)?
**Answer:**
```python
try:
    while True: pass
except KeyboardInterrupt:
    print("Interrupted")
```

### Q68: What is __pycache__ and .pyc files?
**Answer:**
Compiled bytecode for faster loading. Python regenerates if `.py` is newer. Disable with `-B` flag.

### Q69: What is the difference between deepcopy and copy?
**Answer:**
- `copy.copy()` — shallow copy (shared nested objects)
- `copy.deepcopy()` — fully independent copy

### Q70: How do you implement __slots__?
**Answer:**
```python
class Point:
    __slots__ = ("x", "y")  # No __dict__, saves memory
```

### Q71: How do you merge two dictionaries?
**Answer:**
```python
{**d1, **d2}  # Python 3.5+
d1 | d2       # Python 3.9+
d1 |= d2       # In-place 3.9+
```

### Q72: What is @lru_cache decorator?
**Answer:**
Caches function results:
```python
from functools import lru_cache
@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)
```

### Q73: What is __getattr__ vs __getattribute__?
**Answer:**
- `__getattribute__` called for EVERY attribute access
- `__getattr__` called only when attribute not found

### Q74: How does the in operator work for custom classes?
**Answer:**
```python
def __contains__(self, item):
    return item in self.items
```

### Q75: What is __call__ magic method?
**Answer:**
Makes instance callable:
```python
class Counter:
    def __call__(self):
        self.count += 1
        return self.count
```

### Q76: What is the difference between open() modes w, a, x?
**Answer:**
- `w`: write (truncates)
- `a`: append
- `x`: exclusive creation (fails if exists)

### Q77: How do you work with environment variables?
**Answer:**
```python
import os
os.environ.get("HOME", "/default")
os.environ["MY_VAR"] = "value"
```

### Q78: What are the different ways to concatenate strings?
**Answer:**
```python
"a" + "b"          # + operator
"".join(["a","b"])  # Efficient for many
f"{a}{b}"           # f-string
```

### Q79: How do you get the current date and time?
**Answer:**
```python
from datetime import datetime
datetime.now()           # Local time
datetime.utcnow()        # UTC
datetime.now().strftime("%Y-%m-%d")
```

### Q80: How do you generate random numbers?
**Answer:**
```python
import random
random.randint(1, 10)    # Random int
random.choice(["a","b"]) # Random choice
random.shuffle(lst)      # Shuffle in-place

import secrets
secrets.token_hex(16)    # Cryptographically secure
```

---

## OOP in Python (Q81-Q150)

### Q81: What is a class and object?
**Answer:**
A **class** is a blueprint. An **object** is an instance.
```python
class Dog:
    species = "Canis familiaris"  # Class attribute
    def __init__(self, name, age):
        self.name = name  # Instance attribute
        self.age = age
    def bark(self):
        return f"{self.name} says woof!"

rex = Dog("Rex", 3)
print(rex.bark())  # Rex says woof!
```

### Q82: What does self mean in Python?
**Answer:**
`self` refers to the instance. It's the first parameter of instance methods:
```python
class Point:
    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
p1.distance(p2) is same as Point.distance(p1, p2)
```

### Q83: How do you achieve constructor overloading?
**Answer:**
Use default args or `@classmethod` alternative constructors:
```python
class Rectangle:
    def __init__(self, width=0, height=0): ...
    @classmethod
    def from_square(cls, side): return cls(side, side)
```

### Q84: Explain single inheritance.
**Answer:**
```python
class Animal:
    def speak(self): raise NotImplementedError
class Dog(Animal):
    def speak(self): return "Woof!"
```

### Q85: What is multiple inheritance?
**Answer:**
```python
class Flyer: def fly(self): return "Flying"
class Swimmer: def swim(self): return "Swimming"
class Duck(Flyer, Swimmer): pass
```

### Q86: What is multilevel inheritance?
**Answer:**
```python
class A: pass
class B(A): pass
class C(B): pass  # C inherits from B inherits from A
```

### Q87: What is hierarchical inheritance?
**Answer:**
```python
class Vehicle: pass
class Car(Vehicle): pass
class Bike(Vehicle): pass  # Multiple subclasses of same parent
```

### Q88: Explain MRO (Method Resolution Order).
**Answer:**
MRO determines method lookup order using C3 linearization:
```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
print(D.__mro__)  # D, B, C, A, object
```

### Q89: How does super() work?
**Answer:**
`super()` delegates to the next class in MRO. Enables cooperative multiple inheritance:
```python
class A: def init(self): print("A")
class B(A):
    def init(self):
        super().init()  # Calls next in MRO
        print("B")
```

### Q90: What is polymorphism and method overriding?
**Answer:**
Polymorphism: same interface, different implementations. Overriding: subclass redefines parent method.
```python
class Shape:
    def area(self): pass
class Circle(Shape):
    def area(self): return 3.14 * r**2
class Rect(Shape):
    def area(self): return w * h
```

### Q91: What is operator overloading?
**Answer:**
```python
class Vector:
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
```

### Q92: What is encapsulation?
**Answer:**
Bundling data and methods, restricting direct access:
```python
class BankAccount:
    def __init__(self):
        self._balance = 0     # Protected
        self.__pin = "1234"   # Name-mangled private
    def get_balance(self): return self._balance
```

### Q93: What is the @property decorator?
**Answer:**
Turns method into computed attribute:
```python
class Temperature:
    @property
    def celsius(self): return self._celsius
    @celsius.setter
    def celsius(self, value):
        if value < -273.15: raise ValueError
        self._celsius = value
```

### Q94: What is name mangling?
**Answer:**
`__attr` becomes `_ClassName__attr` to prevent accidental access:
```python
class A:
    def __init__(self):
        self.__x = 1  # _A__x
class B(A):
    def __init__(self):
        self.__x = 2  # _B__x
```

### Q95: What are abstract classes and ABCs?
**Answer:**
```python
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self): pass
class Circle(Shape):
    def area(self): return 3.14 * r**2
```

### Q96: What are dataclasses?
**Answer:**
Auto-generate `__init__`, `__repr__`, `__eq__`:
```python
from dataclasses import dataclass
@dataclass
class Person:
    name: str
    age: int
    email: str = ""
```
Options: `frozen=True`, `order=True`, `slots=True` (3.10+)

### Q97: What are namedtuples?
**Answer:**
```python
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x    # 3
p._asdict()  # {'x': 3, 'y': 4}
```

### Q98: What are metaclasses?
**Answer:**
Classes of classes (default: `type`). Control class creation:
```python
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
```

### Q99: Composition vs inheritance?
**Answer:**
- Inheritance: "is-a" (`Dog extends Animal`)
- Composition: "has-a" (`Car has Engine`)
- Favor composition for flexibility

### Q100: Duck typing and EAFP vs LBYL?
**Answer:**
**Duck typing:** "If it quacks like a duck..."
```python
def process(obj): return obj.quack()
```
**EAFP** (Pythonic): `try: x = d[key] except KeyError: ...`
**LBYL**: `if key in d: x = d[key]`

### Q101: @staticmethod vs @classmethod vs regular methods?
**Answer:**
- Regular: receives `self` (instance)
- `@classmethod`: receives `cls` (class)
- `@staticmethod`: nothing special

### Q102: What are __str__, __repr__, __add__, __len__, __getitem__, __call__, __enter__/__exit__?
**Answer:**
```python
class MyClass:
    def __str__(self): return "user friendly"
    def __repr__(self): return "MyClass()"
    def __len__(self): return len(self.items)
    def __getitem__(self, i): return self.items[i]
    def __call__(self): return "called"
    def __enter__(self): return self
    def __exit__(self, *args): pass
```

### Q103: What is __enter__ and __exit__?
**Answer:**
Context manager protocol: `__enter__` sets up, `__exit__` cleans up.
```python
class ManagedFile:
    def __enter__(self):
        self.f = open(self.name, self.mode)
        return self.f
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()
```

### Q104: What is __slots__ and when to use it?
**Answer:**
Declares allowed attributes, saves memory by eliminating `__dict__`:
```python
class Point:
    __slots__ = ("x", "y")
```
Use for thousands of instances.

### Q105: How to implement singleton pattern?
**Answer:**
```python
# __new__ approach
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Q106: Explain __del__ method.
**Answer:**
Called when object is garbage collected:
```python
def __del__(self):
    print(f"{self} destroyed")
```
Not guaranteed to be called immediately. Use context managers for cleanup.

### Q107: What is __dict__ in classes/objects?
**Answer:**
Stores instance/class attributes:
```python
p.__dict__      # {'name': 'Alice'}
Person.__dict__ # {'species': 'human', '__init__': <function>}
```

### Q108: What is __weakref__?
**Answer:**
Allows weak references. Objects with `__slots__` may not have it unless declared.

### Q109: @classmethod vs @staticmethod difference?
**Answer:**
`@classmethod` receives class (`cls`) — can access/modify class state. `@staticmethod` is just a function in the class.

### Q110: What is super() in single inheritance?
**Answer:**
```python
class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)  # Calls Parent.__init__
        self.age = age
```

### Q111: What are ABCs and why use them?
**Answer:**
Abstract Base Classes define interfaces:
```python
from abc import ABC, abstractmethod
class Drawable(ABC):
    @abstractmethod
    def draw(self): pass
```
Enforces implementation in subclasses.

### Q112: What are protocols (PEP 544)?
**Answer:**
Structural subtyping (Python 3.8+):
```python
from typing import Protocol
class Drawable(Protocol):
    def draw(self) -> str: ...
def render(obj: Drawable): obj.draw()
```

### Q113: What is __init_subclass__?
**Answer:**
Hook called when subclassing:
```python
class Base:
    def __init_subclass__(cls, **kwargs):
        print(f"{cls.__name__} subclasses Base")
```

### Q114: __new__ vs __init__?
**Answer:**
`__new__` creates instance (static), `__init__` initializes it (called after `__new__`).

### Q115: Iterator protocol in custom class?
**Answer:**
```python
class Range:
    def __iter__(self): return self
    def __next__(self):
        if self.current >= self.end: raise StopIteration
        ...
```

### Q116: What are __lt__, __gt__, __le__, __ge__, __eq__, __ne__?
**Answer:**
Comparison operators. Use `@total_ordering` to auto-generate missing ones.

### Q117: What is __hash__?
**Answer:**
Makes object usable as dict key/set member:
```python
def __hash__(self):
    return hash((self.x, self.y))
```

### Q118: What is __bool__?
**Answer:**
Controls truthiness:
```python
def __bool__(self):
    return self.balance > 0
```

### Q119: Difference between class and type?
**Answer:**
`type` is the metaclass. `type(MyClass)` is `<class 'type'>`.

### Q120: How do you define private attributes?
**Answer:**
Conventions: `_protected` (single underscore) and `__private` (double underscore, name mangling).

### Q121: What is __init_subclass__ used for?
**Answer:**
Validate or register subclasses:
```python
class Plugin:
    plugins = {}
    def __init_subclass__(cls, name=None):
        if name: cls.plugins[name] = cls
```

### Q122: Multiple inheritance with different __init__?
**Answer:**
Use `super()` with keyword args:
```python
class A:
    def __init__(self, a, **kwargs): ...
class B:
    def __init__(self, b, **kwargs): ...
class C(A, B):
    def __init__(self, a, b, c):
        super().__init__(a=a, b=b)
```

### Q123: What is __getattr__ used for?
**Answer:**
Called when attribute not found:
```python
def __getattr__(self, name):
    return self._data.get(name)
```

### Q124: What is __setattr__ and __delattr__?
**Answer:**
Hooks for attribute setting/deletion. Use `super().__setattr__()` to avoid recursion.

### Q125: __subclasscheck__ and __instancecheck__?
**Answer:**
Customize `issubclass()` and `isinstance()` behavior.

### Q126: __iter__ and __next__?
**Answer:**
`__iter__` returns iterator, `__next__` returns next value or raises StopIteration.

### Q127: How to make object subscriptable?
**Answer:**
Implement `__getitem__`:
```python
def __getitem__(self, key):
    return self.data[key]
```

### Q128: What is __missing__ in dict subclasses?
**Answer:**
```python
class DefaultDict(dict):
    def __missing__(self, key): return 0
d = DefaultDict(); d["x"]  # 0 (not KeyError)
```

### Q129: Explain __prepare__ in metaclasses.
**Answer:**
Customizes class namespace creation:
```python
@classmethod
def __prepare__(cls, name, bases):
    return OrderedDict()
```

### Q130: How do properties work at class level?
**Answer:**
Properties are descriptors — they define `__get__`, `__set__`, `__delete__` on the class.

### Q131: __slots__ caveats with inheritance?
**Answer:**
Child must redeclare `__slots__` if it has its own. Multiple inheritance with slots is tricky.

### Q132: MRO with super()?
**Answer:**
`super()` follows MRO, not just parent class. Essential for cooperative multiple inheritance.

### Q133: Diamond inheritance problem?
**Answer:**
Python's C3 linearization resolves it deterministically: `D -> B -> C -> A` (not `D -> B -> A -> C`).

### Q134: Explain @dataclass in detail.
**Answer:**
```python
@dataclass(order=True, frozen=True)
class Student:
    name: str
    grades: list = field(default_factory=list)
    gpa: float = field(init=False)
    def __post_init__(self):
        self.gpa = sum(self.grades) / len(self.grades) if self.grades else 0
```

### Q135: Dataclass vs namedtuple?
**Answer:**
Dataclass: mutable, type hints, customizable. Namedtuple: immutable, lightweight, tuple methods.

### Q136: What is field() in dataclasses?
**Answer:**
Configures fields: `field(default_factory=list)`, `field(repr=False)`, `field(init=False)`, `field(compare=False)`.

### Q137: What is __post_init__ in dataclasses?
**Answer:**
Called after generated `__init__` for additional setup.

### Q138: __init_subclass__ with multiple inheritance?
**Answer:**
Works cooperatively via MRO — each class's `__init_subclass__` is called.

### Q139: What are descriptors?
**Answer:**
Objects defining `__get__`, `__set__`, `__delete__` that control attribute access. Properties are descriptors.

### Q140: What is __set_name__ in descriptors?
**Answer:**
Called at class creation with the attribute name:
```python
def __set_name__(self, owner, name):
    self.name = name
    self.private_name = f"_{name}"
```

### Q141: __prepare__ in metaclasses?
**Answer:**
Returns the namespace dict used during class body execution.

### Q142: How does super() work without arguments?
**Answer:**
Python 3 compiler inserts `__class__` and `self` automatically.

### Q143: Bound vs unbound methods?
**Answer:**
Bound: instance method with `self` filled in. Unbound: just the function.

### Q144: type vs isinstance?
**Answer:**
`type` checks exact class, `isinstance` checks inheritance chain.

### Q145: How to create a class factory?
**Answer:**
```python
def factory(name, **attrs):
    return type(name, (object,), attrs)
```

### Q146: What is __subclasshook__?
**Answer:**
Customizes `issubclass()` for ABCs using structural typing.

### Q147: What is total_ordering?
**Answer:**
Generates missing comparison methods from `__eq__` and one `__lt__`/`__le__`/`__gt__`/`__ge__`.

### Q148: What is __reversed__?
**Answer:**
Supports `reversed()` on custom objects.

### Q149: What is __sizeof__?
**Answer:**
Returns object's size in bytes. `sys.getsizeof()` uses it.

### Q150: __index__ vs __int__?
**Answer:**
`__int__` called by `int()`. `__index__` called when used as sequence index (must return int).

---

---

## Advanced Python (Q151-Q280)

### Q151: What are decorators in Python?
**Answer:**
Decorators modify functions/methods. They're callables that take a function and return a function:
```python
from functools import wraps

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log
def add(a, b):
    return a + b
```

### Q152: How do you preserve metadata with decorators?
**Answer:**
Use `@wraps` from functools:
```python
from functools import wraps
def decorator(func):
    @wraps(func)  # Preserves __name__, __doc__, __module__
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### Q153: How do you create decorators with arguments?
**Answer:**
```python
from functools import wraps

def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello {name}")
```

### Q154: How do class decorators work?
**Answer:**
```python
def singleton(cls):
    instances = {}
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("Creating connection")
```

### Q155: What are generators and yield?
**Answer:**
Generators produce values lazily:
```python
def count_up_to(n):
    i = 0
    while i < n:
        yield i
        i += 1

gen = count_up_to(3)
print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 2

# Generator expression (lazy)
gen_expr = (x**2 for x in range(10))
```

### Q156: How do send(), throw(), and close() work with generators?
**Answer:**
```python
def interactive():
    value = yield "ready"
    yield f"processed {value}"

gen = interactive()
print(gen.send(None))  # "ready"  (start)
print(gen.send("hello"))  # "processed hello"

gen.throw(ValueError)  # Exception inside generator
gen.close()  # GeneratorExit at yield point
```

### Q157: What is the difference between Iterable and Iterator?
**Answer:**
- **Iterable**: has `__iter__()` returning an iterator (e.g., list, dict)
- **Iterator**: has `__iter__()` and `__next__()` (e.g., generator)
- All iterators are iterable, not vice versa.

```python
from collections.abc import Iterable, Iterator
lst = [1, 2, 3]
isinstance(lst, Iterable)  # True
isinstance(lst, Iterator)  # False
isinstance(iter(lst), Iterator)  # True
```

### Q158: How does contextlib.contextmanager work?
**Answer:**
```python
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    print(f"Entering: {name}")
    resource = {"name": name}
    try:
        yield resource
    finally:
        print(f"Exiting: {name}")

with managed_resource("db") as res:
    print(f"Using {res['name']}")
```

### Q159: Explain *args and **kwargs in detail.
**Answer:**
```python
def func(a, b, *args, **kwargs):
    print(f"a={a}, b={b}")
    print(f"args={args}")    # Tuple of extra positional args
    print(f"kwargs={kwargs}")  # Dict of extra keyword args

func(1, 2, 3, 4, x=5, y=6)
# a=1, b=2, args=(3,4), kwargs={'x':5, 'y':6}

# Unpacking
def add(a, b, c): return a + b + c
add(*[1, 2, 3])   # 6
add(**{"a": 1, "b": 2, "c": 3})  # 6
```

### Q160: What are keyword-only arguments?
**Answer:**
Arguments after `*` or `*args` must be keywords:
```python
def func(a, b, *, verbose=False):
    pass
func(1, 2, verbose=True)  # OK
# func(1, 2, True)  # TypeError
```

### Q161: What are type hints and the typing module?
**Answer:**
```python
from typing import List, Dict, Optional, Union, Callable

x: int = 5
y: Optional[str] = None              # str | None (3.10+)
z: Union[int, str] = 42              # int | str (3.10+)
items: List[int] = [1, 2, 3]
func: Callable[[int, int], int] = lambda a, b: a + b

# Python 3.10+ simplified: int | str instead of Union[int, str]
```

### Q162: What is TypeVar and Generic?
**Answer:**
```python
from typing import TypeVar, Generic, List

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self):
        self._items: List[T] = []
    def push(self, item: T) -> None:
        self._items.append(item)
    def pop(self) -> T:
        return self._items.pop()

int_stack = Stack[int]()
int_stack.push(1)
str_stack = Stack[str]()
str_stack.push("hello")

# Constrained TypeVar
Number = TypeVar("Number", int, float)
def add(a: Number, b: Number) -> Number:
    return a + b
```

### Q163: What is Callable type?
**Answer:**
```python
from typing import Callable
# Callable[[args], return_type]
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)
```

### Q164: What is asyncio and the event loop?
**Answer:**
```python
import asyncio

async def hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

asyncio.run(hello())
```
The event loop manages and schedules coroutines, handling I/O without blocking.

### Q165: How do async and await work?
**Answer:**
`async def` creates a coroutine function. `await` suspends execution until the awaited coroutine completes:
```python
async def fetch_data(url):
    await asyncio.sleep(1)  # Non-blocking
    return f"Data from {url}"

async def main():
    # Sequential
    result = await fetch_data("url1")
    # Concurrent
    task = asyncio.create_task(fetch_data("url2"))
    result2 = await task
```

### Q166: What is asyncio.gather() vs asyncio.create_task()?
**Answer:**
```python
# create_task - schedule individual task
task1 = asyncio.create_task(worker("A", 2))
task2 = asyncio.create_task(worker("B", 1))

# gather - run multiple concurrently
results = await asyncio.gather(
    worker("C", 1),
    worker("D", 2),
    return_exceptions=True  # Return exceptions, don't raise
)
```

### Q167: What is asyncio.wait()?
**Answer:**
```python
done, pending = await asyncio.wait(
    tasks,
    return_when=asyncio.FIRST_COMPLETED
)
# Can wait for FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED
```

### Q168: What is asyncio.as_completed()?
**Answer:**
Yields completed tasks as they finish (like `futures.as_completed`):
```python
for coro in asyncio.as_completed(tasks):
    result = await coro
    print(result)
```

### Q169: Explain async context managers.
**Answer:**
```python
class AsyncResource:
    async def __aenter__(self):
        await asyncio.sleep(1)
        return self
    async def __aexit__(self, *args):
        await asyncio.sleep(1)

async with AsyncResource() as res:
    print("Using resource")

# contextlib approach
from contextlib import asynccontextmanager

@asynccontextmanager
async def managed():
    print("Enter")
    try:
        yield
    finally:
        print("Exit")
```

### Q170: What are async generators?
**Answer:**
```python
async def async_range(n):
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i

async for x in async_range(5):
    print(x)
```

### Q171: Threading vs multiprocessing vs asyncio?
**Answer:**
| Feature | Threading | Multiprocessing | Asyncio |
|---------|-----------|-----------------|---------|
| Concurrency type | Preemptive | Preemptive | Cooperative |
| GIL affected | Yes | No (separate processes) | No (single-threaded) |
| CPU-bound | Bad | Good | Bad |
| I/O-bound | Good | OK | Excellent |
| Memory | Shared | Separate | Shared |
| Overhead | Medium | High | Low |
| Debugging | Hard | Medium | Easier |

### Q172: Explain the GIL (Global Interpreter Lock) in depth.
**Answer:**
The GIL is a mutex that prevents multiple threads from executing Python bytecode simultaneously. This protects CPython's memory management but limits CPU-bound parallelism.

**Why it exists:**
- CPython's memory management (reference counting) isn't thread-safe
- Removing it would require massive refactoring and slow single-threaded performance

**Impact:**
- I/O-bound tasks: GIL is released during I/O → threading works well
- CPU-bound tasks: GIL prevents true parallelism → use multiprocessing

**Workarounds:**
- `multiprocessing` — separate processes, each with own GIL
- C extensions that release GIL (NumPy, Cython)
- `concurrent.futures.ProcessPoolExecutor`

```python
# Threading for I/O
import threading
def io_task():
    time.sleep(1)  # GIL released
# Effectively concurrent

# Multiprocessing for CPU
from multiprocessing import Pool
def cpu_task(n):
    return sum(i*i for i in range(n))
# Truly parallel
```

### Q173: What is ThreadPoolExecutor?
**Answer:**
```python
from concurrent.futures import ThreadPoolExecutor
import time

def task(n):
    time.sleep(1)
    return n * 2

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(task, i) for i in range(10)]
    results = [f.result() for f in futures]

    # Or use map
    results = list(executor.map(task, range(10)))
```

### Q174: What is ProcessPoolExecutor?
**Answer:**
```python
from concurrent.futures import ProcessPoolExecutor

def cpu_bound(n):
    return sum(i ** i for i in range(n))

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound, [1000, 2000, 3000]))
```
Note: Must guard with `if __name__ == "__main__"` on Windows.

### Q175: What is concurrent.futures module?
**Answer:**
Provides high-level async execution:
```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, wait

with ThreadPoolExecutor() as ex:
    futures = {ex.submit(task, i): i for i in range(10)}

    # As completed
    for future in as_completed(futures):
        result = future.result()

    # Wait for all
    done, not_done = wait(futures, timeout=5, return_when=ALL_COMPLETED)
```

### Q176: What is the collections.deque?
**Answer:**
Double-ended queue with O(1) appends/pops on both ends:
```python
from collections import deque

d = deque([1, 2, 3], maxlen=5)  # Fixed size
d.append(4)          # Right
d.appendleft(0)      # Left
d.pop()              # Remove right
d.popleft()          # Remove left
d.rotate(1)          # Right rotation

# Use as queue (FIFO)
queue = deque(["A", "B"])
queue.popleft()  # 'A'

# Use as stack (LIFO)
stack = deque()
stack.append("A")
stack.pop()  # 'A'
```

### Q177: What is collections.Counter?
**Answer:**
Dict subclass for counting hashable objects:
```python
from collections import Counter

words = ["a", "b", "a", "c", "b", "a"]
c = Counter(words)
print(c)         # Counter({'a': 3, 'b': 2, 'c': 1})
c.most_common(2) # [('a', 3), ('b', 2)]

# Operations
Counter(["a", "b"]) + Counter(["a", "c"])  # Counter({'a': 2, 'b': 1, 'c': 1})
Counter(["a", "b"]) - Counter(["a"])       # Counter({'b': 1})
Counter(["a"]) & Counter(["a", "b"])       # Intersection (min): Counter({'a': 1})
Counter(["a"]) | Counter(["a", "b"])       # Union (max): Counter({'a': 1, 'b': 1})

# String characters
Counter("hello")  # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})
```

### Q178: What is collections.defaultdict?
**Answer:**
Dict with default factory for missing keys:
```python
from collections import defaultdict

# List factory
d = defaultdict(list)
d["a"].append(1)  # No KeyError

# Int factory (counter)
d = defaultdict(int)
d["a"] += 1  # 1

# Set factory
d = defaultdict(set)
d["a"].add(1)

# Custom factory
d = defaultdict(lambda: "missing")
print(d["x"])  # "missing"

# vs dict.setdefault():
# defaultdict is faster for repeated access
regular = {}
regular.setdefault("key", []).append(1)
```

### Q179: What is collections.OrderedDict?
**Answer:**
Dict that maintains insertion order (Python 3.7+ dicts also preserve order, but OrderedDict has extra methods):
```python
from collections import OrderedDict

od = OrderedDict()
od["a"] = 1
od["b"] = 2
od["c"] = 3

# Move to end/beginning
od.move_to_end("a")           # Move "a" to end
od.move_to_end("c", last=False)  # Move "c" to front

# Pop item (LIFO)
od.popitem()       # ('c', 3)
od.popitem(last=False)  # ('a', 1)

# Equality is order-sensitive
od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
od1 == od2  # False (dict equality would be True)

# Reversed
list(reversed(od))  # ['c', 'b', 'a']
```

### Q180: What is collections.namedtuple?
**Answer:**
```python
from collections import namedtuple

# Create factory
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)

# Access
p.x     # 3
p[0]    # 3
x, y = p  # Unpacking

# Methods
p._asdict()         # {'x': 3, 'y': 4}
p._replace(x=5)    # Point(x=5, y=4) (new instance)
Point._make([1, 2])  # Point(x=1, y=2)

# Fields
Point._fields  # ('x', 'y')
```

### Q181: What is itertools.chain?
**Answer:**
```python
from itertools import chain

# Chain iterables
list(chain([1, 2], [3, 4], [5]))  # [1, 2, 3, 4, 5]

# Chain from iterable of iterables
list(chain.from_iterable([[1, 2], [3, 4]]))  # [1, 2, 3, 4]

# Flatten nested
nested = [[1, 2], [3, 4], [5]]
list(chain.from_iterable(nested))  # [1, 2, 3, 4, 5]
```

### Q182: What is itertools.cycle?
**Answer:**
```python
from itertools import cycle

# Infinite cycle
counter = 0
for item in cycle(["A", "B", "C"]):
    print(item)  # A, B, C, A, B, C, ...
    counter += 1
    if counter > 6: break

# Round-robin
colors = cycle(["red", "green", "blue"])
next(colors)  # red
next(colors)  # green
next(colors)  # blue
next(colors)  # red
```

### Q183: What is itertools.product?
**Answer:**
Cartesian product:
```python
from itertools import product

list(product([1, 2], ["a", "b"]))
# [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

list(product([1, 2], repeat=2))
# [(1, 1), (1, 2), (2, 1), (2, 2)]

# Equivalent to nested for loops
for x, y in product(range(3), range(3)):
    print(x, y)
```

### Q184: What is itertools.permutations?
**Answer:**
```python
from itertools import permutations

list(permutations([1, 2, 3], 2))
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

list(permutations("ABC"))
# [('A','B','C'), ('A','C','B'), ('B','A','C'), ...]

# Total: n! / (n-r)! permutations
len(list(permutations([1,2,3,4], 2)))  # 12
```

### Q185: What is itertools.combinations?
**Answer:**
```python
from itertools import combinations

list(combinations([1, 2, 3], 2))
# [(1, 2), (1, 3), (2, 3)]  (order doesn't matter)

list(combinations("ABC", 2))
# [('A','B'), ('A','C'), ('B','C')]

# With replacement
from itertools import combinations_with_replacement
list(combinations_with_replacement([1, 2, 3], 2))
# [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]

# Total: n! / (r! * (n-r)!) combinations
```

### Q186: What is itertools.groupby?
**Answer:**
Groups consecutive elements by key (must be sorted):
```python
from itertools import groupby

data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
for key, group in groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# A [('A',1), ('A',2)]
# B [('B',3), ('B',4)]

# Must sort first
data = [("B", 1), ("A", 2), ("A", 3)]
sorted_data = sorted(data, key=lambda x: x[0])
for key, group in groupby(sorted_data, key=lambda x: x[0]):
    print(key, list(group))
```

### Q187: What is functools.partial?
**Answer:**
Fixes arguments of a function:
```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125

# Real-world: callback with args
def send_email(to, subject, body):
    pass

send_to_alice = partial(send_email, to="alice@example.com")
send_to_alice("Hello", "Body text")

# Partial with builtins
int_base2 = partial(int, base=2)
int_base2("1010")  # 10
```

### Q188: What is functools.lru_cache?
**Answer:**
Caches function results (Least Recently Used):
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)

# Methods
fibonacci.cache_info()     # CacheInfo(hits=..., misses=...)
fibonacci.cache_clear()    # Clear cache

# Python 3.9+: unbounded
from functools import cache
@cache
def expensive(n): ...
```

### Q189: What is functools.reduce?
**Answer:**
Cumulatively applies function:
```python
from functools import reduce

reduce(lambda a, b: a * b, [1, 2, 3, 4])   # 24
reduce(lambda a, b: a + b, [1, 2, 3])      # 6
reduce(max, [3, 1, 4, 1, 5])              # 5
reduce(lambda a, b: a if a > b else b, [3, 1, 4])  # 4

# With initializer
reduce(lambda a, b: a + b, [], 0)  # 0 (empty with initializer)
reduce(lambda a, b: a * b, [1, 2], 10)  # 20 (10 * 1 * 2)
```

### Q190: What is functools.wraps?
**Answer:**
Copies metadata from decorated function to wrapper:
```python
from functools import wraps

def decorator(func):
    @wraps(func)  # Copy __name__, __doc__, __module__, __annotations__
    def wrapper(*args, **kwargs):
        """Wrapper doc"""
        return func(*args, **kwargs)
    return wrapper

@decorator
def my_func():
    """Original doc"""
    pass

print(my_func.__name__)  # 'my_func' (without wraps: 'wrapper')
print(my_func.__doc__)   # 'Original doc' (without wraps: 'Wrapper doc')
```

### Q191: What is functools.singledispatch?
**Answer:**
Single-dispatch generic function (function overloading by type):
```python
from functools import singledispatch

@singledispatch
def process(arg):
    print(f"Default: {arg}")

@process.register(int)
def _(arg):
    print(f"Integer: {arg}")

@process.register(list)
def _(arg):
    print(f"List of {len(arg)} items")

@process.register(str)
@process.register(bytes)  # Multiple types
def _(arg):
    print(f"Text: {arg.upper()}")

process(42)           # Integer: 42
process([1, 2, 3])    # List of 3 items
process("hello")      # Text: HELLO
```

### Q192: What is the re module (regex)?
**Answer:**
```python
import re

# search - first match anywhere
m = re.search(r"\\d+", "abc123def")
m.group()   # '123'
m.start()   # 3
m.end()     # 6

# match - from beginning only
re.match(r"\\d+", "123abc")  # Match
re.match(r"\\d+", "abc123")  # None

# findall - all matches
re.findall(r"\\d+", "a1b2c3")  # ['1', '2', '3']

# finditer - iterator of matches
for m in re.finditer(r"\\d+", "a1b2c3"):
    print(m.group())

# sub - replace
re.sub(r"\\d+", "#", "a1b2c3")  # 'a#b#c#'

# split
re.split(r"[,\\s]+", "a, b, c")  # ['a', 'b', 'c']

# compile for reuse
pattern = re.compile(r"\\d+")
pattern.findall("abc123")  # ['123']
```

### Q193: What are regex groups and named groups?
**Answer:**
```python
import re

# Groups
m = re.search(r"(\\d+)-(\\w+)", "123-abc")
m.group(0)    # '123-abc' (full match)
m.group(1)    # '123'
m.group(2)    # 'abc'
m.groups()    # ('123', 'abc')

# Named groups
m = re.search(r"(?P<id>\\d+)-(?P<name>\\w+)", "123-abc")
m.group("id")     # '123'
m.group("name")   # 'abc'
m.groupdict()     # {'id': '123', 'name': 'abc'}

# Non-capturing groups
re.search(r"(?:\\d+)-\\w+", "123-abc")  # No capture

# Backreferences
re.search(r"(\\w+) \\1", "hello hello")  # Match repeated word
```

### Q194: What are regex flags?
**Answer:**
```python
import re

text = "Hello\\nWorld"

# re.IGNORECASE (re.I)
re.search(r"hello", text, re.IGNORECASE)

# re.MULTILINE (re.M) - ^ and $ match line boundaries
re.findall(r"^\\w+", text, re.MULTILINE)  # ['Hello', 'World']

# re.DOTALL (re.S) - . matches newline
re.search(r"Hello.World", text, re.DOTALL)

# re.VERBOSE (re.X) - readable patterns
pattern = re.compile(r"""
    (\\d+)   # Number
    -        # Dash
    (\\w+)   # Word
""", re.VERBOSE)

# Combine flags
re.search(pattern, text, re.I | re.M)
```

### Q195: How do you use the logging module?
**Answer:**
```python
import logging

# Basic configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename="app.log"
)

# Logger per module
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")

# Logging with exception info
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("Division error")  # Includes traceback
```

### Q196: What are handlers, formatters, and loggers in logging?
**Answer:**
```python
import logging

# Root logger
root = logging.getLogger()
root.setLevel(logging.DEBUG)

# Handler: where logs go
console = logging.StreamHandler()  # stdout
file_handler = logging.FileHandler("app.log")

# Formatter: how logs look
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console.setFormatter(formatter)

# Add handler
root.addHandler(console)
root.addHandler(file_handler)

# Log levels: DEBUG < INFO < WARNING < ERROR < CRITICAL

# Custom handler
class SlackHandler(logging.Handler):
    def emit(self, record):
        send_to_slack(self.format(record))

# Filter
class ImportantFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.WARNING
```

### Q197: What are logging levels?
**Answer:**
```python
import logging

# Standard levels (increasing severity)
# DEBUG (10): Detailed info for debugging
# INFO (20): Confirmation things work
# WARNING (30): Something unexpected happened
# ERROR (40): Serious problem, function failed
# CRITICAL (50): Program may not continue

# Set level for logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Set level for handler
handler = logging.StreamHandler()
handler.setLevel(logging.ERROR)
```

### Q198: How do you configure logging from a config file?
**Answer:**
```python
# logging.conf
"""
[loggers]
keys=root

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler,fileHandler

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=WARNING
formatter=simpleFormatter
args=('app.log', 'a')

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
"""

import logging.config
logging.config.fileConfig("logging.conf")

# Also dict config
config = {
    "version": 1,
    "formatters": {"simple": {"format": "%(levelname)s: %(message)s"}},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "DEBUG",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}
logging.config.dictConfig(config)
```

### Q199: What is shallow copy vs deep copy?
**Answer:**
```python
import copy

# Shallow copy: copies the object, but not nested objects
original = [[1, 2, 3], [4, 5, 6]]
shallow = copy.copy(original)
shallow[0][0] = 99
original[0][0]  # 99 (shared nested reference)

# Deep copy: fully independent copy
deep = copy.deepcopy(original)
deep[0][0] = 999
original[0][0]  # 99 (unaffected)

# Shallow copy methods
list_copy = list(original)     # [:]
dict_copy = dict(original)     # {**original}
set_copy = set(original_set)
```

### Q200: What is PEP 8?
**Answer:**
PEP 8 is Python's style guide. Key rules:
- 4 spaces per indentation (no tabs)
- Max line length: 79 characters (72 for docstrings/comments)
- Two blank lines around functions, one around methods
- Imports: one per line, grouped (stdlib, third-party, local)
- `snake_case` for functions/variables, `CamelCase` for classes, `UPPER_CASE` for constants
- Spaces around operators, after commas
- Use `is` for None comparison
- Use `with` for file operations

### Q201: What is PEP 484?
**Answer:**
PEP 484 adds type hints to Python:
```python
def greeting(name: str) -> str:
    return f"Hello {name}"
```
Enables static type checking with tools like mypy.

### Q202: What is PEP 257 (docstrings)?
**Answer:**
PEP 257 defines docstring conventions:
```python
def add(a, b):
    \"\"\"Add two numbers and return the result.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    \"\"\"
    return a + b
```
- One-line docstrings for simple functions
- Multi-line with summary line, blank line, then details
- Triple quotes always (even for one-liners)

### Q203: What is garbage collection and reference counting?
**Answer:**
Python uses two mechanisms:
1. **Reference counting** (primary): Each object has a count of references.
   - Incremented on assignment, list append, etc.
   - Decremented on del, reassignment, going out of scope
   - When count reaches 0, memory is freed immediately

2. **Generational GC** (for cycles): The `gc` module handles cyclic references.

```python
import sys, gc

x = []
print(sys.getrefcount(x))  # 2 (one for x, one for arg)

# Cycle
a = {}; b = {}
a["b"] = b; b["a"] = a
del a, b  # Reference counts not zero (cycle)
gc.collect()  # Collects the cycle

# GC control
gc.disable()   # Disable (rarely needed)
gc.set_threshold(700, 10, 10)  # Tune collection frequency
```

### Q204: What are weak references (weakref module)?
**Answer:**
Weak references don't increase reference count — object can be GC'd:
```python
import weakref

class Expensive:
    def __del__(self):
        print("Deleted")

obj = Expensive()
r = weakref.ref(obj)

print(r())  # <Expensive object> (callback returns ref)
del obj     # Deleted
print(r())  # None (object gone)

# WeakValueDictionary
cache = weakref.WeakValueDictionary()
obj = Expensive()
cache["key"] = obj
del obj  # Automatically removed from cache

# WeakSet
ws = weakref.WeakSet()
ws.add(Expensive())

# Proxy (like ref but acts like the object)
obj = Expensive()
p = weakref.proxy(obj)
p.some_method()  # Works like obj.some_method()
del obj
# p.some_method()  # ReferenceError
```

### Q205: How does Python execute code? (CPython architecture)
**Answer:**
CPython processes code in stages:
1. **Lexing**: Source code → tokens
2. **Parsing**: Tokens → AST (Abstract Syntax Tree)
3. **Compilation**: AST → bytecode
4. **Execution**: PVM (Python Virtual Machine) executes bytecode

```bash
# View bytecode
python -m dis my_module.py
```

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
# Shows LOAD_FAST, BINARY_OP, RETURN_VALUE opcodes
```

### Q206: What is bytecode and the dis module?
**Answer:**
Bytecode is a low-level representation of Python code executed by the PVM:
```python
import dis

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Disassemble
dis.dis(factorial)

# Each instruction: line number, opcode name, argument
# Example output:
#   2           0 LOAD_FAST                0 (n)
#               2 LOAD_CONST               1 (1)
#               4 COMPARE_OP               1 (<=)
#               6 POP_JUMP_IF_FALSE        2 (to 12)

# View all opcodes
dis.opname  # dict of opcode numbers to names
```

### Q207: Is Python compiled or interpreted?
**Answer:**
Both. Python is:
- **Compiled** to bytecode (`.pyc` files)
- **Interpreted** by the Python Virtual Machine (PVM)

```mermaid
Source (.py) → Bytecode (.pyc) → PVM execution
```

This hybrid approach gives:
- Portability (bytecode is platform-independent)
- Faster loading (pre-compiled bytecode)
- Dynamic execution capabilities

### Q208: What are C extensions and ctypes?
**Answer:**
Python can interface with C libraries:
```python
from ctypes import CDLL, c_int

# Load C library
lib = CDLL("./mylib.so")

# Define function signature
lib.add.argtypes = [c_int, c_int]
lib.add.restype = c_int

result = lib.add(3, 4)  # Calls C function

# Working with strings
lib.process_string.argtypes = [c_char_p]
lib.process_string("hello")
```

### Q209: How does Python memory management work?
**Answer:**
Python uses a private heap:
1. **Object allocator**: allocates/deallocates at object level
2. **Raw memory allocator**: interacts with OS (`malloc`/`free`)
3. **Object-specific allocators**: for int, str, etc.

```python
import sys

# Object size (shallow)
sys.getsizeof(42)         # 28 bytes
sys.getsizeof("hello")    # 54 bytes
sys.getsizeof([])         # 56 bytes

# GC tracks objects with __del__ and cycles
import gc
gc.get_objects()  # All objects tracked by GC
```

**Memory pools:**
- Objects < 512 bytes use arenas/pools/blocks (efficient)
- Objects >= 512 bytes use system `malloc`

### Q210: What are interned strings?
**Answer:**
Python interns some strings (reuses same object) for optimization:
```python
a = "hello"
b = "hello"
a is b  # True (interned)

# Long/variable strings are not interned
c = "hello " + "world"
d = "hello " + "world"
c is d  # May be False

# Using sys.intern
import sys
a = sys.intern("hello world!" * 100)
b = sys.intern("hello world!" * 100)
a is b  # True (explicitly interned)
```
String interning saves memory and speeds up comparisons.

### Q211: What is small integer caching?
**Answer:**
Python caches integers in range [-5, 256] (by default):
```python
a = 256
b = 256
a is b  # True (cached)

a = 257
b = 257
a is b  # False (or True in CPython interactive, False in scripts)

# Don't rely on is for int comparison — always use ==
```
The range can be checked with `sys.getsmallest()` and modified at compile time.

### Q212: How does Python's import system work?
**Answer:**
When `import x` runs:
1. Check `sys.modules` cache
2. If not found, iterate `sys.meta_path` finders:
   - `BuiltinImporter` — built-in modules
   - `FrozenImporter` — frozen modules  
   - `PathFinder` — searches `sys.path` directories
3. Finder returns module spec (location, loader, etc.)
4. Loader creates module, executes it, adds to `sys.modules`

```python
import sys

# Search path
sys.path  # Current dir, PYTHONPATH, site-packages

# Already loaded
sys.modules.keys()

# Custom importer
class MyImporter:
    def find_module(self, name, path):
        if name == "mymodule":
            return self
        return None
    def load_module(self, name):
        # Create and return module
        pass
```

### Q213: What is sys.path?
**Answer:**
List of directories where Python searches for modules:
```python
import sys

# Current search path
print(sys.path)
# ['', '/usr/lib/python3.10', '/usr/lib/python3.10/lib-dynload',
#  '/usr/local/lib/python3.10/site-packages', ...]

# Modify at runtime
sys.path.insert(0, "/my/custom/path")

# PYTHONPATH environment variable
# $ export PYTHONPATH=/my/custom/path
```

### Q214: What are common sys module functions?
**Answer:**
```python
import sys

sys.argv           # Command-line args
sys.exit(0)        # Exit program
sys.version        # Python version string
sys.platform       # Platform identifier
sys.getrecursionlimit()    # Get recursion depth
sys.setrecursionlimit(5000)  # Increase recursion limit
sys.getsizeof(obj) # Object size
sys.modules        # Loaded modules dict
sys.path           # Module search path
sys.stdin/stdout/stderr  # Standard streams
sys.byteorder      # 'little' or 'big'
sys.executable     # Python interpreter path
sys.getdefaultencoding()  # Default encoding
```

### Q215: What is the os module?
**Answer:**
```python
import os

# Files and directories
os.getcwd()           # Current directory
os.chdir("/tmp")      # Change directory
os.listdir(".")       # List directory
os.mkdir("newdir")    # Create directory
os.makedirs("a/b/c")  # Create nested directories
os.remove("file.txt") # Delete file
os.rmdir("dir")       # Delete empty directory
os.rename("a", "b")   # Rename/move

# Path operations (prefer os.path)
os.path.join("a", "b")  # 'a/b'
os.path.exists("file")  # True/False
os.path.isfile("file")  # True/False
os.path.isdir("dir")    # True/False
os.path.basename("/a/b/c.txt")  # 'c.txt'
os.path.dirname("/a/b/c.txt")   # '/a/b'
os.path.splitext("file.txt")    # ('file', '.txt')

# Environment
os.environ["HOME"]   # Get env var
os.getenv("HOME", "default")

# Process
os.getpid()          # Current process ID
os.system("ls -la")  # Run command (discouraged; use subprocess)
```

### Q216: What is the shutil module?
**Answer:**
```python
import shutil

# Copy files
shutil.copy("src.txt", "dst.txt")     # Copy file
shutil.copy2("src.txt", "dst.txt")    # Copy with metadata
shutil.copytree("src_dir", "dst_dir") # Copy directory tree

# Move/Rename
shutil.move("src.txt", "dst/dst.txt") 

# Delete directory tree
shutil.rmtree("dir_to_delete")  # Careful!

# Disk usage
usage = shutil.disk_usage("/")
print(f"Free: {usage.free / 1e9:.1f} GB")

# Archives
shutil.make_archive("backup", "zip", "mydir")
shutil.unpack_archive("backup.zip", "extract_dir")

# Find files
shutil.which("python")  # '/usr/bin/python'
```

### Q217: What is the glob module?
**Answer:**
File pattern matching:
```python
import glob

# All .txt files in current directory
glob.glob("*.txt")

# Recursive
glob.glob("**/*.py", recursive=True)

# With path
glob.glob("/tmp/*.log")

# Character classes
glob.glob("[abc]*.py")  # Files starting with a, b, or c
glob.glob("[!0-9]*.py")  # Files not starting with digit
```

### Q218: What is argparse for CLI?
**Answer:**
```python
import argparse

parser = argparse.ArgumentParser(description="My CLI tool")
parser.add_argument("input", help="Input file")
parser.add_argument("-o", "--output", help="Output file", default="out.txt")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose")
parser.add_argument("-n", "--count", type=int, default=1, help="Count")
parser.add_argument("--format", choices=["json", "csv"], default="json")

args = parser.parse_args()
print(args.input, args.output, args.verbose, args.count, args.format)
```

### Q219: What is ConfigParser?
**Answer:**
```python
from configparser import ConfigParser

# Reading
config = ConfigParser()
config.read("config.ini")

# Access
config.get("database", "host")     # 'localhost'
config.getint("database", "port")  # 5432
config.getboolean("debug", "enabled")  # True
config.sections()                  # ['database', 'debug']

# Writing
config["database"] = {"host": "localhost", "port": "5432"}
with open("config.ini", "w") as f:
    config.write(f)

# Defaults
config = ConfigParser(defaults={"port": "8080"})
```

### Q220: What is the subprocess module?
**Answer:**
```python
import subprocess

# Run command
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
print(result.returncode)

# With shell (caution: security risk)
subprocess.run("ls -la", shell=True)

# Popen for more control
proc = subprocess.Popen(
    ["ping", "-c", "3", "google.com"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
stdout, stderr = proc.communicate(timeout=10)

# Pipe output
proc1 = subprocess.Popen(["ls"], stdout=subprocess.PIPE)
proc2 = subprocess.Popen(["grep", "py"], stdin=proc1.stdout, stdout=subprocess.PIPE)
output = proc2.communicate()[0]
```

### Q221: What is lru_cache internals?
**Answer:**
`lru_cache` uses a dict + doubly-linked list:
- Dictionary maps arguments → result
- Linked list maintains LRU order
- On cache hit: move to head (most recently used)
- On cache miss: add to head; if full, evict from tail

```python
from functools import lru_cache

@lru_cache(maxsize=3)
def f(x):
    print(f"Computing {x}")
    return x * 2

f(1)  # Computing 1
f(2)  # Computing 2
f(3)  # Computing 3
f(1)  # Cache hit (moved to front)
f(4)  # Computing 4; evicts 2 (LRU)
```

### Q222: What are partial functions in functools?
**Answer:**
Already covered in Q187. Additional details:
```python
from functools import partial

# partialmethod for classes
from functools import partialmethod

class Cell:
    def __init__(self):
        self._alive = False

    @property
    def alive(self): return self._alive

    def set_state(self, state):
        self._alive = state

    set_alive = partialmethod(set_state, True)
    set_dead = partialmethod(set_state, False)

cell = Cell()
cell.set_alive()
cell.alive  # True
```

### Q223: What is the functools.singledispatchmethod?
**Answer:**
Like `singledispatch` but for methods (Python 3.8+):
```python
from functools import singledispatchmethod

class Formatter:
    @singledispatchmethod
    def format(self, arg):
        raise NotImplementedError

    @format.register(int)
    def _(self, arg):
        return f"int: {arg}"

    @format.register(str)
    def _(self, arg):
        return f"str: {arg}"

f = Formatter()
f.format(42)     # 'int: 42'
f.format("hi")   # 'str: hi'
```

### Q224: What are slots and when to use them?
**Answer:**
Already in Q70/Q104. __slots__ prevents `__dict__` creation, saving memory and speeding attribute access:
```python
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Usage
p = Point(1, 2)
# p.z = 3  # AttributeError
# p.__dict__  # AttributeError

# Memory savings: ~50% for many instances
```

### Q225: What are descriptor protocols (__get__, __set__, __delete__)?
**Answer:**
Already covered in Q139. Descriptors control attribute access:
```python
class VerboseAttribute:
    def __get__(self, obj, objtype=None):
        print(f"Getting {self.name}")
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        print(f"Setting {self.name} = {value}")
        obj.__dict__[self.name] = value

class MyClass:
    x = VerboseAttribute()

obj = MyClass()
obj.x = 5   # Setting x = 5
print(obj.x)  # Getting x / 5
```

### Q226: How do you implement __del__ correctly?
**Answer:**
```python
class Resource:
    def __del__(self):
        # Warning: avoid circular references
        # Don't rely on this for critical cleanup
        print(f"Cleanup {id(self)}")

# Better: use context managers
class Resource:
    def __enter__(self): return self
    def __exit__(self, *args): self.cleanup()
    def cleanup(self):
        print("Cleanup done")

with Resource() as r:
    pass  # Guaranteed cleanup
```

### Q227: What is the __prepare__ method in metaclasses?
**Answer:**
```python
class TrackedNamespace(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        print(f"Preparing namespace for {name}")
        return {"_from_prepare": True}

    def __new__(metacls, name, bases, ns):
        print(f"Creating class {name}")
        return super().__new__(metacls, name, bases, ns)

class MyClass(metaclass=TrackedNamespace):
    x = 1
    y = 2

# Output:
# Preparing namespace for MyClass
# Creating class MyClass
```

### Q228: What are frozensets?
**Answer:**
Immutable version of set:
```python
fs = frozenset([1, 2, 3, 2, 1])
print(fs)  # frozenset({1, 2, 3})

# Set operations work
fs | frozenset([3, 4])  # frozenset({1, 2, 3, 4})

# Can be used as dict key (unlike set)
d = {frozenset([1, 2]): "value"}

# No add/remove methods
# fs.add(4)  # AttributeError
```

### Q229: What is the __set_name__ descriptor hook?
**Answer:**
Already covered in Q140. Called when class is created:
```python
class Field:
    def __set_name__(self, owner, name):
        self.name = name
        self.internal = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return getattr(obj, self.internal, None)

    def __set__(self, obj, value):
        setattr(obj, self.internal, value)

class Person:
    name = Field()
    age = Field()

p = Person()
p.name = "Alice"
print(p.name)  # Alice
```

### Q230: What is the difference between __call__ and a regular function?
**Answer:**
`__call__` makes an instance callable:
```python
class Adder:
    def __init__(self, n):
        self.n = n
    def __call__(self, x):
        return self.n + x

add5 = Adder(5)
print(add5(3))  # 8 (instance called as function)
print(add5(10))  # 15

# Useful for stateful callables
class Counter:
    def __init__(self):
        self.count = 0
    def __call__(self):
        self.count += 1
        return self.count

c = Counter()
c()  # 1
c()  # 2
```

### Q231: What is the __new__ method and when is it useful?
**Answer:**
Already in Q66/Q114. `__new__` is useful for:
- Immutable types (can't use __init__)
- Singleton pattern
- Object pooling

```python
# Immutable type
class Temperature(float):
    def __new__(cls, value, scale="C"):
        if scale == "F":
            value = (value - 32) * 5 / 9
        return super().__new__(cls, value)

t = Temperature(212, "F")
print(t)  # 100.0
```

### Q232: What are abstract methods and properties?
**Answer:**
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

class Circle(Shape):
    @property
    def name(self) -> str:
        return "Circle"

    def area(self) -> float:
        return 3.14 * self.radius ** 2

    def __init__(self, radius):
        self.radius = radius
```

### Q233: How do you create read-only properties?
**Answer:**
```python
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    # No setter — read-only
    # @name.setter is intentionally omitted

p = Person("Alice")
print(p.name)  # Alice
# p.name = "Bob"  # AttributeError
```

### Q234: What is the Union type in typing?
**Answer:**
```python
from typing import Union

# A variable that can be int or str
x: Union[int, str] = 42
x = "hello"  # OK

# Optional is Union[T, None]
y: Union[int, None] = None
y: Optional[int] = None  # Equivalent

# Python 3.10+
z: int | str = 42  # Same as Union[int, str]
w: int | None = None  # Same as Optional[int]
```

### Q235: What is the Any type?
**Answer:**
```python
from typing import Any

# Disables type checking for this variable
def process(data: Any) -> Any:
    return data  # Any operation allowed

# Use sparingly — defeats purpose of type hints
```

### Q236: What are Literal types?
**Answer:**
```python
from typing import Literal

def set_mode(mode: Literal["r", "w", "a"]) -> None:
    pass

set_mode("r")   # OK
set_mode("x")   # Type error

# Multiple acceptable values
def set_status(status: Literal[200, 404, 500]) -> None:
    pass
```

### Q237: What are TypedDict types?
**Answer:**
```python
from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int
    email: str

# Or using alternative syntax
Person = TypedDict("Person", {"name": str, "age": int})

def greet(p: Person) -> str:
    return f"Hello {p['name']}"

alice: Person = {"name": "Alice", "age": 30}
```

### Q238: What is the Final type?
**Answer:**
```python
from typing import Final

MAX_SIZE: Final = 100
# MAX_SIZE = 200  # Type error (mypy)

NAME: Final[str] = "Python"
```

### Q239: What are Protocols (structural subtyping)?
**Answer:**
```python
from typing import Protocol

class SupportsClose(Protocol):
    def close(self) -> None: ...

def cleanup(obj: SupportsClose) -> None:
    obj.close()

class FileHandler:
    def close(self) -> None:
        print("Closing")

class DBConnection:
    def close(self) -> None:
        print("Closing DB")

cleanup(FileHandler())      # OK
cleanup(DBConnection())     # OK
```

### Q240: What is TypeGuard?
**Answer:**
```python
from typing import TypeGuard, Any

def is_str_list(val: list[Any]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def process(items: list[Any]):
    if is_str_list(items):
        # Here items is narrowed to list[str]
        print(" ".join(items.upper()))  # OK
```

### Q241: What are the different ways to handle import errors?
**Answer:**
```python
# Try-import for optional dependencies
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

# Version checking
import sys
if sys.version_info < (3, 8):
    raise RuntimeError("Python 3.8+ required")

# Conditional import
if sys.platform == "win32":
    import msvcrt
else:
    import fcntl
```

### Q242: How do you reload a module?
**Answer:**
```python
import importlib
import mymodule

# Reload
importlib.reload(mymodule)

# Python 2: reload(mymodule)
```

### Q243: What is the difference between __init__.py usage?
**Answer:**
`__init__.py` makes a directory a Python package. It can:
- Execute initialization code
- Define `__all__` (what `from package import *` exports)
- Import submodules

```python
# mypackage/__init__.py
from . import module_a
from .module_b import useful_function

__all__ = ["module_a", "useful_function"]

# This is also a namespace package (Python 3.3+)
# Can omit __init__.py entirely
```

### Q244: What are relative imports?
**Answer:**
```python
# Inside mypackage/subpackage/module.py

# Absolute import
from mypackage import parent_module

# Relative import
from . import sibling_module      # Same package
from .. import parent_module      # Parent package
from ..subpackage2 import module   # Sibling package
```

### Q245: What is the `__all__` variable?
**Answer:**
Controls what `from module import *` exports:
```python
# mymodule.py
__all__ = ["public_func", "PublicClass"]

def public_func(): pass
def _private_func(): pass  # Not in __all__
class PublicClass: pass
```

### Q246: How do you debug Python code?
**Answer:**
```python
# Built-in debugger
import pdb

def buggy():
    pdb.set_trace()  # Start debugger here
    x = 1
    y = 0
    result = x / y

# pdb commands: n(next), s(step), c(continue), l(list), p(print), q(quit)

# Better: breakpoint() (Python 3.7+)
def buggy():
    breakpoint()  # Same as pdb.set_trace()
    ...

# Post-mortem
try:
    1 / 0
except:
    pdb.post_mortem()

# python -m pdb script.py  # Run script with debugger
# python -m trace --trace script.py  # Trace execution
```

### Q247: What is `__debug__`?
**Answer:**
Built-in constant that's `True` by default, `False` with `-O` flag:
```python
if __debug__:
    print("Debug mode")  # Removed with -O

# assert uses __debug__
assert x > 0  # Disabled with -O

# Check
print(__debug__)  # True or False
```

### Q248: What is the warnings module?
**Answer:**
```python
import warnings

# Issue warning
warnings.warn("This feature is deprecated", DeprecationWarning)

# Filter warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("error", category=UserWarning)

# Common categories
# DeprecationWarning, UserWarning, FutureWarning
# SyntaxWarning, RuntimeWarning, ImportWarning

# Context manager
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    deprecated_function()
```

### Q249: What is the traceback module?
**Answer:**
```python
import traceback

# Print exception traceback
try:
    1 / 0
except Exception:
    traceback.print_exc()  # Print to stderr

    # Get as string
    tb_str = traceback.format_exc()

# Extract current stack
stack = traceback.extract_stack()
for filename, lineno, name, line in stack:
    print(f"{filename}:{lineno} in {name}")

# Print stack
traceback.print_stack()
```

### Q250: What is the sys.settrace function?
**Answer:**
Sets a trace function for debugging/profiling:
```python
import sys

def trace(frame, event, arg):
    if event == "call":
        print(f"Calling {frame.f_code.co_name}")
    elif event == "line":
        print(f"Line {frame.f_lineno}")
    return trace

sys.settrace(trace)

# Used by debuggers (pdb) and profilers
```

### Q251: What are the different ways to format strings in Python?
**Answer:**
Already covered in Q33/Q57. Summary:
```python
name, age = "Alice", 30

# f-string (Python 3.6+) — preferred
f"{name} is {age}"

# str.format()
"{} is {}".format(name, age)
"{name} is {age}".format(name=name, age=age)

# %-formatting (old-style)
"%s is %d" % (name, age)

# Template strings (safe for user input)
from string import Template
Template("$name is $age").substitute(name=name, age=age)
```

### Q252: How do you handle circular imports?
**Answer:**
```python
# Problem: module_a imports module_b, module_b imports module_a

# Solutions:

# 1. Restructure — move shared code to third module
# 2. Lazy imports (inside function)
def get_b():
    from module_b import B
    return B()

# 3. Import after definition
class A:
    pass
from module_b import B  # Now B can use A

# 4. Use TYPE_CHECKING for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from module_b import B  # Only for type checking
```

### Q253: What is __future__?
**Answer:**
Allows using future Python features in older versions:
```python
from __future__ import annotations  # Lazy evaluation of annotations (3.7+)

from __future__ import division  # True division (Python 2)
from __future__ import print_function  # print() function (Python 2)

# Check current __future__ features
import __future__
```

### Q254: What is the built-in `compile()` function?
**Answer:**
Compiles source into code object:
```python
code_str = "x = 10\ny = 20\nprint(x + y)"
code_obj = compile(code_str, "test.py", "exec")
exec(code_obj)  # 30

# eval mode
expr = compile("2 + 2", "", "eval")
eval(expr)  # 4

# single mode (single statement)
stmt = compile("print('hello')", "", "single")
exec(stmt)
```

### Q255: What is the built-in `exec()` function?
**Answer:**
Dynamically executes Python code:
```python
code = """
def add(a, b):
    return a + b
result = add(10, 20)
"""
exec(code)
print(result)  # 30

# With namespace
namespace = {"x": 5}
exec("y = x * 2", namespace)
print(namespace["y"])  # 10

# Security warning: never exec() untrusted input
```

### Q256: What is the built-in `eval()` function?
**Answer:**
Evaluates a single expression:
```python
result = eval("2 + 3 * 4")  # 14

# With namespace
x = 10
result = eval("x + 5", {"x": x})  # 15

# Security risk: never eval() user input
# eval("__import__('os').system('rm -rf /')")
```

### Q257: What is `__import__` function?
**Answer:**
Low-level import function:
```python
# Import module by string name
math = __import__("math")
print(math.sqrt(16))  # 4.0

# With fromlist for submodule
os_path = __import__("os.path", fromlist=["path"])
# Now os_path is os.path

# Better to use importlib
import importlib
math = importlib.import_module("math")
```

### Q258: What is the `compileall` module?
**Answer:**
Compiles Python files to bytecode:
```bash
python -m compileall .  # Compile all .py files in directory
python -m compileall -f .  # Force recompilation
python -m compileall -o 2 .  # Optimization level 2
```

### Q259: What is the `py_compile` module?
**Answer:**
```python
import py_compile

# Compile single file
py_compile.compile("myscript.py")
# Creates __pycache__/myscript.cpython-310.pyc
```

### Q260: How does the `enum` module work?
**Answer:**
```python
from enum import Enum, auto

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Access
Color.RED            # <Color.RED: 1>
Color(1)             # <Color.RED: 1>
Color["RED"]         # <Color.RED: 1>

# Iteration
for c in Color:
    print(c.name, c.value)

# Auto-numbering
class Status(Enum):
    PENDING = auto()
    ACTIVE = auto()
    DONE = auto()

# StrEnum (3.11+)
from enum import StrEnum
class Mode(StrEnum):
    READ = "r"
    WRITE = "w"

# IntEnum
from enum import IntEnum
class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
```

### Q261: What is the `itertools.islice()` function?
**Answer:**
Slices an iterator (lazy):
```python
from itertools import islice

# Take first 5 items
list(islice(range(100), 5))  # [0, 1, 2, 3, 4]

# Slice with start, stop, step
list(islice(range(100), 10, 20, 2))  # [10, 12, 14, 16, 18]

# Useful for large iterators
def read_lines(path):
    with open(path) as f:
        for line in f:
            yield line.strip()

first_10 = islice(read_lines("big.txt"), 10)
```

### Q262: What is the `itertools.accumulate()` function?
**Answer:**
```python
from itertools import accumulate
import operator

list(accumulate([1, 2, 3, 4]))  # [1, 3, 6, 10] (cumulative sum)

# With function
list(accumulate([1, 2, 3, 4], operator.mul))  # [1, 2, 6, 24]
list(accumulate([3, 1, 4, 1, 5], max))  # [3, 3, 4, 4, 5]

# With initial value (3.8+)
list(accumulate([1, 2, 3], initial=0))  # [0, 1, 3, 6]
```

### Q263: What is the `itertools.count()` function?
**Answer:**
Infinite counter:
```python
from itertools import count

for i in count(10):  # 10, 11, 12, ...
    if i > 15: break
    print(i)

# With step
for i in count(0, 2):  # 0, 2, 4, 6, ...
    if i > 10: break

# enumerate replacement with start
for i, item in zip(count(start=1), items):
    print(i, item)
```

### Q264: What is the `itertools.repeat()` function?
**Answer:**
```python
from itertools import repeat

# Repeat value n times
list(repeat(42, 3))  # [42, 42, 42]

# Infinite (use with islice)
list(islice(repeat("A"), 5))  # ['A', 'A', 'A', 'A', 'A']

# Useful with map
list(map(pow, range(1, 6), repeat(2)))  # [1, 4, 9, 16, 25]
```

### Q265: What is the `itertools.zip_longest()` function?
**Answer:**
Like zip but fills shorter iterables:
```python
from itertools import zip_longest

list(zip_longest([1, 2], [3, 4, 5], fillvalue=0))
# [(1, 3), (2, 4), (0, 5)]

list(zip_longest("ab", "xyz"))
# [('a', 'x'), ('b', 'y'), (None, 'z')]
```

### Q266: What is the `itertools.starmap()` function?
**Answer:**
Like map but unpacks arguments from tuples:
```python
from itertools import starmap

pairs = [(2, 3), (4, 5), (6, 7)]
list(starmap(pow, pairs))  # [8, 1024, 279936]

# Equivalent to:
[pow(a, b) for a, b in pairs]
```

### Q267: What is `itertools.tee()`?
**Answer:**
Creates independent iterators from one:
```python
from itertools import tee, islice

it = iter(range(10))
it1, it2 = tee(it, 2)  # 2 independent iterators

list(it1)  # [0, 1, 2, ..., 9]
list(it2)  # [0, 1, 2, ..., 9] (same results)

# Warning: tee stores intermediate results in memory
```

### Q268: What is `itertools.pairwise()` (Python 3.10+)?
**Answer:**
Consecutive overlapping pairs:
```python
from itertools import pairwise

list(pairwise([1, 2, 3, 4]))
# [(1, 2), (2, 3), (3, 4)]

# Useful for differences
diffs = [b - a for a, b in pairwise(values)]

# String n-grams
word = "hello"
list(pairwise(word))  # [('h','e'), ('e','l'), ('l','l'), ('l','o')]
```

### Q269: How do you create custom itertools-like functions?
**Answer:**
```python
def take(n, iterable):
    return list(islice(iterable, n))

def chunked(iterable, size):
    """Split into chunks."""
    it = iter(iterable)
    return iter(lambda: list(islice(it, size)), [])

def distinct(iterable):
    """Unique elements preserving order."""
    seen = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            yield item

# Usage
list(chunked(range(10), 3))  # [[0,1,2], [3,4,5], [6,7,8], [9]]
list(distinct([1, 2, 1, 3, 2, 4]))  # [1, 2, 3, 4]
```

### Q270: What are the six most common itertools functions to know?
**Answer:**
1. **chain** — chain multiple iterables
2. **product** — cartesian product
3. **permutations** — all orderings
4. **combinations** — all subsets
5. **groupby** — group consecutive elements
6. **zip_longest** — zip with fill

### Q271: How does the math module work?
**Answer:**
```python
import math

# Constants
math.pi   # 3.141592653589793
math.e    # 2.718281828459045
math.inf  # float('inf')
math.nan  # float('nan')

# Rounding
math.floor(3.7)  # 3
math.ceil(3.2)   # 4
math.trunc(3.7)  # 3

# Log
math.log(100, 10)  # 2.0
math.log(100)      # 4.605... (natural log)
math.log2(1024)    # 10.0

# Trig
math.sin(math.pi/2)   # 1.0
math.degrees(math.pi) # 180.0
math.radians(180)     # pi

# Combinatorics
math.comb(5, 2)   # 10
math.perm(5, 2)   # 20
math.factorial(5) # 120
math.gcd(12, 8)   # 4

# Other
math.sqrt(16)    # 4.0
math.hypot(3, 4) # 5.0
math.isclose(0.1 + 0.2, 0.3)  # True
```

### Q272: What is the statistics module?
**Answer:**
```python
import statistics

data = [1, 2, 3, 4, 5, 6, 7]

statistics.mean(data)     # 4.0
statistics.median(data)   # 4
statistics.mode([1, 1, 2])  # 1

statistics.stdev(data)    # ~2.16 (sample standard deviation)
statistics.variance(data) # ~4.67

# For large datasets
statistics.quantiles(data, n=4)  # Quartiles
```

### Q273: What is the decimal module?
**Answer:**
```python
from decimal import Decimal, getcontext

# Avoid floating-point issues
Decimal("0.1") + Decimal("0.2")  # Decimal('0.3')

# Set precision
getcontext().prec = 50
Decimal(1) / Decimal(7)  # High precision

# Quantize (round)
price = Decimal("19.99")
tax = Decimal("0.08")
total = price * tax
total.quantize(Decimal("0.01"))  # Round to 2 decimal places

# vs float
0.1 + 0.2  # 0.30000000000000004
```

### Q274: What is the fractions module?
**Answer:**
```python
from fractions import Fraction

f = Fraction(3, 4)  # 3/4
Fraction(0.75)      # Fraction(3, 4)
Fraction("3/4")     # Fraction(3, 4)

# Arithmetic
Fraction(1, 3) + Fraction(1, 6)  # Fraction(1, 2)

# Properties
f.numerator   # 3
f.denominator # 4
float(f)      # 0.75
```

### Q275: What is the time module?
**Answer:**
```python
import time

# Timestamp
time.time()      # Current Unix timestamp

# Sleep
time.sleep(1.5)  # Sleep 1.5 seconds

# Local time
time.localtime()  # time.struct_time
time.gmtime()     # UTC struct_time

# Formatting
time.strftime("%Y-%m-%d %H:%M:%S")  # Current time as string
time.strptime("2024-01-01", "%Y-%m-%d")  # Parse string

# Performance counter (for benchmarking)
start = time.perf_counter()
# ... code ...
elapsed = time.perf_counter() - start
```

### Q276: What is the timeit module?
**Answer:**
```python
import timeit

# Measure time
timeit.timeit("'-'.join(str(n) for n in range(100))", number=10000)

# From command line
# python -m timeit -n 100000 'x = 2 + 2'

# In IPython/Jupyter
# %timeit [x**2 for x in range(100)]

# For accurate measurement
def test():
    return sum(range(1000))

timeit.timeit(test, number=1000)

# repeat for statistics
timeit.repeat(test, number=1000, repeat=5)
```

### Q277: What is the `__slots__` memory optimization in detail?
**Answer:**
Already covered. Key technical details:
- Each Python object normally has `__dict__` (about 56 bytes for dict, plus entries)
- `__slots__` replaces dict with fixed-size array of PyObject* pointers
- Savings: ~40-60 bytes per instance for simple objects
- Used in: ORMs (SQLAlchemy/Django models with thousands of instances), game objects

```python
class WithDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WithSlots:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y

import sys
d = WithDict(1, 2)
s = WithSlots(1, 2)
sys.getsizeof(d)  # ~56 (plus __dict__)
sys.getsizeof(s)  # ~32 (no __dict__)
```

### Q278: What are class variables vs instance variables?
**Answer:**
```python
class Dog:
    species = "Canine"  # Class variable (shared)

    def __init__(self, name):
        self.name = name  # Instance variable (unique per object)

# Access
d1 = Dog("Rex")
d2 = Dog("Buddy")
d1.species  # "Canine" (from class)
d2.species  # "Canine" (from class, same reference)

# Modify class variable via class
Dog.species = "Feline"
d1.species  # "Feline" (changed for all)

# Shadow via instance
d1.species = "Canine"  # Creates instance attribute
Dog.species  # Still "Feline" (unchanged)
d2.species   # "Feline" (unaffected by d1's change)

# Warning: mutable class variables
class Bad:
    items = []  # Shared by all instances!

a = Bad()
b = Bad()
a.items.append(1)
b.items  # [1]  # Shared!
```

### Q279: How do you create immutable objects?
**Answer:**
```python
# 1. Frozen dataclass
from dataclasses import dataclass
@dataclass(frozen=True)
class Point:
    x: float
    y: float

# 2. NamedTuple
from typing import NamedTuple
class Point(NamedTuple):
    x: float
    y: float

# 3. Custom with __setattr__ raising
class Immutable:
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError(f"Cannot modify {name}")
        super().__setattr__(name, value)

# 4. property without setter
class ReadOnly:
    @property
    def value(self):
        return 42
```

### Q280: What are the built-in functions for introspection?
**Answer:**
```python
type(obj)          # Get type of object
isinstance(obj, cls)   # Check type including inheritance
issubclass(cls, base)  # Check subclass
hasattr(obj, attr)  # Check if attribute exists
getattr(obj, attr, default)  # Get attribute
setattr(obj, attr, value)   # Set attribute
delattr(obj, attr)   # Delete attribute
dir(obj)            # List attributes
vars(obj)           # obj.__dict__
callable(obj)       # Check if callable
id(obj)             # Memory address
help(obj)           # Documentation

# Examples
class A: pass
a = A()
hasattr(a, "x")     # False
setattr(a, "x", 5)
getattr(a, "x")     # 5
getattr(a, "y", 42) # 42 (default)
delattr(a, "x")
dir(a)              # List of attributes
```

## Python Internals (Q281-Q350)

### Q281: How does Python memory management work?
**Answer:**
Python uses a private heap space. The Python memory manager handles allocation. It uses:
- **Reference counting**: Each object tracks how many references point to it. When count hits 0, memory is freed.
- **Garbage collection**: The `gc` module handles circular references via generational GC (3 generations).

```python
import sys
import gc

a = []
sys.getrefcount(a)  # 2 (ref in getrefcount + local var)

b = a
sys.getrefcount(a)  # 3

# Circular reference
x = []
y = []
x.append(y)
y.append(x)  # ref count never hits 0 without GC
del x, y
gc.collect()  # Force GC collection
```

### Q282: What is the GIL and how does it affect concurrency?
**Answer:**
The Global Interpreter Lock (GIL) is a mutex that protects Python objects, allowing only one thread to execute bytecode at a time. It simplifies CPython internals but limits CPU-bound multi-threading.

```python
import threading
import time

def count(n):
    while n > 0:
        n -= 1

# CPU-bound: threads don't speed up due to GIL
t1 = threading.Thread(target=count, args=(10**7,))
t2 = threading.Thread(target=count, args=(10**7,))
start = time.time()
t1.start(); t2.start()
t1.join(); t2.join()
print(f"Time: {time.time() - start:.2f}s")
# ~same as sequential
```

Workarounds: `multiprocessing` (separate processes with per-process GIL), C extensions, `asyncio` for I/O.

### Q283: Explain the difference between `is` and `==`
**Answer:**
`is` checks identity (same object, same `id()`), `==` checks equality (same value via `__eq__`).

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

a == b   # True  (same value)
a is b   # False (different objects)
a is c   # True  (same object)

# Small integer caching (Python caches -5 to 256)
x = 256
y = 256
x is y   # True (cached)

p = 257
q = 257
p is q   # False (not cached, but implementation-dependent)
```

### Q284: What is the difference between `deepcopy` and `shallow copy`?
**Answer:**
Shallow copy creates a new object but inserts references to the same child objects. Deep copy recursively copies all nested objects.

```python
import copy

original = [[1, 2, 3], [4, 5, 6]]

shallow = copy.copy(original)
deep = copy.deepcopy(original)

shallow[0][0] = 99
# original[0][0] is now 99 (shared reference)

deep[0][0] = 42
# original[0][0] is still 99 (independent)
```

### Q285: How does Python handle variable scope (LEGB rule)?
**Answer:**
Python resolves names in order: **L**ocal, **E**nclosing, **G**lobal, **B**uilt-in.

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)
    inner()
    print(x)

outer()    # local, enclosing
print(x)   # global

# Use nonlocal and global to modify scope
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
```

### Q286: Explain how Python's import system works
**Answer:**
`import` searches `sys.path` for modules. It first checks `sys.modules` cache, then finds the module, loads it, and executes it.

```python
import sys

# Module search path
print(sys.path)
# ['', '/usr/lib/python3...', ...]

# Check cached modules
print(type(sys.modules))  # <class 'dict'>

# Custom importer (PEP 302)
class MyImporter:
    def find_module(self, name, path):
        if name == "custom_module":
            return self
        return None
    def load_module(self, name):
        mod = type(sys)(name)
        mod.__file__ = "<custom>"
        mod.__loader__ = self
        code = "def hello(): print('custom hello')"
        exec(code, mod.__dict__)
        sys.modules[name] = mod
        return mod

sys.meta_path.insert(0, MyImporter())
import custom_module
custom_module.hello()  # custom hello
```

### Q287: What are descriptors in Python?
**Answer:**
Descriptors are objects that define `__get__`, `__set__`, or `__delete__` methods. They control attribute access. Properties, methods, and `@classmethod`/`@staticmethod` use descriptors.

```python
class Validator:
    def __init__(self, min_val):
        self.min_val = min_val

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if value < self.min_val:
            raise ValueError(f"{self.name} must be >= {self.min_val}")
        obj.__dict__[self.name] = value

class Product:
    price = Validator(0)

p = Product()
p.price = 100  # OK
p.price = -5   # ValueError
```

### Q288: How does Python's garbage collector handle circular references?
**Answer:**
The `gc` module uses generational GC. Objects are in 3 generations. When a generation runs out of space, GC collects it. Younger generations are collected more frequently.

```python
import gc

gc.get_threshold()  # (700, 10, 10) - default

# Objects that can participate in cycles
class Node:
    def __init__(self):
        self.parent = None

# Detect circular references
gc.set_debug(gc.DEBUG_SAVEALL)
a = Node()
b = Node()
a.parent = b
b.parent = a
del a, b
gc.collect()
print(gc.garbage)  # collected objects

# Disable GC
gc.disable()
# Manual collection
gc.collect()
```

### Q289: What are slots and when should you use them?
**Answer:**
`__slots__` restricts attribute assignment to a fixed set, reducing memory usage (no `__dict__` per instance).

```python
class WithoutSlots:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WithSlots:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

import sys
wos = WithoutSlots(1, 2)
ws = WithSlots(1, 2)
print(sys.getsizeof(wos))  # 56 (with __dict__)
print(sys.getsizeof(ws))   # 48 (no __dict__)

# Slots prevent adding new attributes
ws.z = 3  # AttributeError
```

### Q290: Explain Python's method resolution order (MRO)
**Answer:**
MRO determines the order in which base classes are searched. Python uses C3 linearization (depth-first, left-to-right, respecting monotonicity).

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D.__mro__)
# D -> B -> C -> A -> object

# MRO is important for super()
class Base:
    def method(self):
        print("Base")

class Left(Base):
    def method(self):
        print("Left")
        super().method()

class Right(Base):
    def method(self):
        print("Right")
        super().method()

class Bottom(Left, Right):
    def method(self):
        print("Bottom")
        super().method()

b = Bottom()
b.method()
# Bottom
# Left
# Right
# Base
```

### Q291: What is the difference between `__str__` and `__repr__`?
**Answer:**
`__repr__` is for developers (unambiguous representation), `__str__` is for users (readable). `__repr__` is used by `repr()` and fallback for `str()`.

```python
from datetime import datetime

now = datetime.now()
print(repr(now))  # datetime.datetime(2026, 6, 24, 12, 30, 0, 123456)
print(str(now))   # 2026-06-24 12:30:00.123456

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

p = Point(3, 4)
print(repr(p))  # Point(3, 4)
print(str(p))   # (3, 4)
print(p)        # (3, 4) - calls __str__
```

### Q292: How does Python's `with` statement work internally?
**Answer:**
The `with` statement uses context manager protocol: `__enter__` and `__exit__` methods. `__exit__` handles exceptions.

```python
class File:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        # Return True to suppress exceptions
        return False

# Equivalent implementation
class ContextManager:
    def __enter__(self):
        print("Entering context")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting context")
        if exc_type is not None:
            print(f"Exception: {exc_type}: {exc_value}")
        return False  # Don't suppress

# Using contextlib
from contextlib import contextmanager

@contextmanager
def managed_resource():
    resource = acquire()
    try:
        yield resource
    finally:
        release()
```

### Q293: What are Python's `__getattr__` and `__getattribute__` differences?
**Answer:**
`__getattribute__` is called for EVERY attribute access. `__getattr__` is only called when normal lookup fails (AttributeError).

```python
class Test:
    def __init__(self):
        self.x = 10

    def __getattribute__(self, name):
        print(f"__getattribute__: {name}")
        return super().__getattribute__(name)

    def __getattr__(self, name):
        print(f"__getattr__: {name} (fallback)")
        return "default"

t = Test()
print(t.x)  # __getattribute__: x -> 10
print(t.y)  # __getattribute__: y -> __getattr__: y -> "default"
```

### Q294: How does Python implement dictionaries (hash tables)?
**Answer:**
Python dicts use hash tables with open addressing. They use the hash of the key to compute an index, handle collisions with probing, and maintain insertion order (since Python 3.7).

```python
# Simplified dict implementation concept
class SimpleDict:
    def __init__(self):
        self.size = 8
        self.table = [None] * self.size

    def _hash(self, key):
        return hash(key) % self.size

    def __setitem__(self, key, value):
        idx = self._hash(key)
        while self.table[idx] is not None and self.table[idx][0] != key:
            idx = (idx + 1) % self.size  # Linear probing
        self.table[idx] = (key, value)

    def __getitem__(self, key):
        idx = self._hash(key)
        while self.table[idx] is not None:
            if self.table[idx][0] == key:
                return self.table[idx][1]
            idx = (idx + 1) % self.size
        raise KeyError(key)

# Performance characteristics
d = {}
d[1] = "one"     # O(1) average
d[2] = "two"
"one" in d       # O(1) average - checks keys, not values
```

### Q295: Explain Python's method resolution order (MRO) with C3 linearization
**Answer:**
C3 linearization ensures consistent MRO by maintaining three properties: consistent extended precedence, consistent monotonic ordering, and local precedence ordering.

```python
# Diamond inheritance
class O: pass
class A(O): pass
class B(O): pass
class C(A, B): pass

# C3 linearization:
# L[C] = C + merge(L[A], L[B], [A, B])
# L[A] = A, O
# L[B] = B, O
# L[C] = C + merge([A, O], [B, O], [A, B])
#      = C + A + merge([O], [B, O], [B])
#      = C + A + B + merge([O], [O])
#      = C + A + B + O

print(C.__mro__)
# (<class 'C'>, <class 'A'>, <class 'B'>, <class 'O'>, <class 'object'>)
```

### Q296: How does Python handle integers beyond 64-bit?
**Answer:**
Python 3 has arbitrary-precision integers (long ints). They grow as needed, limited only by memory. Operations are slower for very large ints.

```python
import sys

# Small integer
x = 42
print(sys.getsizeof(x))  # 28 bytes (includes overhead)

# Large integer
y = 10**100
print(y)
# 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

z = 2**10000
print(len(str(z)))  # 3011 digits

# Performance comparison
import time
start = time.time()
a = 2**1000000  # million-bit number
print(f"Time: {time.time() - start:.4f}s")
```

### Q297: What is the difference between processes and threads in Python?
**Answer:**
Threads share memory (same process), processes have separate memory. Threads are limited by GIL for CPU work; processes bypass GIL.

```python
import threading
import multiprocessing
import os

def worker(n):
    print(f"PID: {os.getpid()}, working on {n}")
    return n * 2

# Threads - shared memory, same PID
threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for t in threads: t.start()
for t in threads: t.join()

# Processes - separate memory, different PIDs
with multiprocessing.Pool(3) as pool:
    results = pool.map(worker, [1, 2, 3])

# When to use each
# Threads: I/O-bound tasks (network, file I/O)
# Processes: CPU-bound tasks (computation, ML training)
```

### Q298: How do Python generators and iterators work internally?
**Answer:**
Any object with `__iter__` and `__next__` is an iterator. Generators are functions with `yield` that return iterator objects. They maintain state between calls.

```python
# Manual iterator
class Counter:
    def __init__(self, max_val):
        self.max = max_val
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.n >= self.max:
            raise StopIteration
        self.n += 1
        return self.n

# Generator (same thing, less code)
def counter(max_val):
    n = 0
    while n < max_val:
        n += 1
        yield n

# Generator internals
gen = counter(3)
print(gen)          # <generator object counter at 0x...>
print(dir(gen))     # __iter__, __next__, send, throw, close
print(next(gen))    # 1
print(next(gen))    # 2
print(next(gen))    # 3
# print(next(gen))  # StopIteration
```

### Q299: What is the buffer protocol and `memoryview`?
**Answer:**
The buffer protocol allows objects to share memory access without copying. `memoryview` creates a view of an object's memory.

```python
import array

# Create a memory view
arr = array.array('i', [1, 2, 3, 4, 5])
mv = memoryview(arr)
print(mv[0])        # 1

# Modify through the view
mv[0] = 99
print(arr[0])       # 99 (original changed)

# Slicing without copy
slice_view = mv[1:3]
print(slice_view.tolist())  # [2, 3]

# Casting
bytes_arr = bytearray(b'hello')
mv_bytes = memoryview(bytes_arr)
mv_ints = mv_bytes.cast('B')  # Cast to unsigned bytes
print(mv_ints.tolist())  # [104, 101, 108, 108, 111]

# No copy involved
print(mv_bytes.nbytes)  # 5
```

### Q300: How does Python's `super()` work with multiple inheritance?
**Answer:**
`super()` follows the MRO. Without arguments, it uses the class and instance where it's called. It uses cooperative multiple inheritance.

```python
class Root:
    def method(self):
        print("Root")
        # Don't call super() here if Root is top

class A(Root):
    def method(self):
        print("A")
        super().method()

class B(Root):
    def method(self):
        print("B")
        super().method()

class C(A, B):
    def method(self):
        print("C")
        super().method()

c = C()
c.method()
# C
# A
# B
# Root

# The MRO ensures each class's method is called once
print(C.__mro__)
# C -> A -> B -> Root -> object
```

### Q301: How does Python's `__new__` differ from `__init__`?
**Answer:**
`__new__` creates the object (returns instance), `__init__` initializes it. `__new__` is called before `__init__`. Used for immutable objects and singletons.

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value):
        if not hasattr(self, 'initialized'):
            self.value = value
            self.initialized = True

a = Singleton(1)
b = Singleton(2)
print(a is b)   # True
print(a.value)  # 1 (first init wins)
print(b.value)  # 1

# Custom immutable
class ConstPoint:
    def __new__(cls, x, y):
        instance = super().__new__(cls)
        instance._x = x
        instance._y = y
        return instance

    @property
    def x(self): return self._x
    @property
    def y(self): return self._y
```

### Q302: What is pickling in Python?
**Answer:**
Pickling serializes Python objects to byte stream. Unpickling deserializes. Not secure (don't unpickle untrusted data).

```python
import pickle
import json

data = {
    'name': 'Alice',
    'scores': [95, 87, 91],
    'metadata': {'grade': 'A', 'active': True}
}

# Serialize
bytes_data = pickle.dumps(data)
print(type(bytes_data))  # <class 'bytes'>

# Deserialize
restored = pickle.loads(bytes_data)
print(restored == data)  # True

# Write to file
with open('data.pkl', 'wb') as f:
    pickle.dump(data, f)

with open('data.pkl', 'rb') as f:
    loaded = pickle.load(f)

# Pickle can serialize classes/functions
class MyClass:
    def __init__(self, n):
        self.n = n
    def double(self):
        return self.n * 2

obj = MyClass(5)
serialized = pickle.dumps(obj)
restored_obj = pickle.loads(serialized)
print(restored_obj.double())  # 10
```

### Q303: How does Python's `@property` decorator work internally?
**Answer:**
`@property` creates a descriptor. `obj.attr` calls the getter, `obj.attr = val` calls the setter, `del obj.attr` calls the deleter.

```python
# Property implementation (conceptual)
class Property:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel)

# Usage
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @Property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius can't be negative")
        self._radius = value
```

### Q304: What are coroutines and how do they differ from generators?
**Answer:**
Coroutines can send values back to the caller and receive values using `yield`. They use `.send()`, `.throw()`, and `.close()`.

```python
def coroutine():
    print("Coroutine started")
    x = yield  # Receive value
    print(f"Received: {x}")
    y = yield x * 2  # Send value back
    print(f"Received: {y}")
    return "Done"

c = coroutine()
next(c)           # Prime coroutine (start)
result1 = c.send(10)  # Send 10, gets 20 back
print(f"Got: {result1}")
result2 = c.send(20)  # Send 20
# Coroutine ends

# Coroutine as accumulator
def accumulator():
    total = 0
    while True:
        value = yield total
        total += value

acc = accumulator()
next(acc)  # Prime
print(acc.send(10))  # 10
print(acc.send(5))   # 15
print(acc.send(3))   # 18
acc.close()
```

### Q305: What is the difference between `__class__` and `type(obj)`?
**Answer:**
`obj.__class__` returns the class of the instance. `type(obj)` returns the same for most objects. However, with metaclasses, `type(obj)` can differ.

```python
class Meta(type):
    def __new__(mcs, name, bases, attrs):
        attrs['__class__'] = lambda self: "Custom"
        return super().__new__(mcs, name, bases, attrs)

class MyClass(metaclass=Meta):
    pass

obj = MyClass()
print(obj.__class__)  # "Custom" (overridden)
print(type(obj))      # <class '__main__.MyClass'>

# For normal classes
class Normal: pass
n = Normal()
print(n.__class__)  # <class '__main__.Normal'>
print(type(n))      # <class '__main__.Normal'>
```

### Q306: How does Python's `asyncio` event loop work?
**Answer:**
The event loop manages asynchronous tasks using cooperative multitasking. Tasks yield control with `await`, and the loop schedules other tasks.

```python
import asyncio
import time

async def fetch_data(n):
    print(f"Fetching {n}...")
    await asyncio.sleep(1)  # Yield control
    print(f"Done {n}")
    return n * 10

async def main():
    # Run concurrently
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )
    print(f"Results: {results}")

# Run the event loop
asyncio.run(main())
# Total time: ~1s (not 3s)

# Manual loop control
loop = asyncio.new_event_loop()
task = loop.create_task(fetch_data(42))
loop.run_until_complete(task)
loop.close()
```

### Q307: What is the `__slots__` memory savings in detail?
**Answer:**
`__slots__` eliminates per-instance `__dict__`, saving ~40-60 bytes per instance. For millions of objects, this is significant.

```python
import sys

class Slotted:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

class NonSlotted:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Memory comparison
s = Slotted(1, 2)
ns = NonSlotted(1, 2)

print(f"Slotted __dict__: {hasattr(s, '__dict__')}")     # False
print(f"NonSlotted __dict__: {hasattr(ns, '__dict__')}") # True

print(f"Slotted size: {sys.getsizeof(s)}")     # 48
print(f"NonSlotted size: {sys.getsizeof(ns)}") # 56

# Bulk comparison
slotted_list = [Slotted(i, i) for i in range(1000)]
nonslotted_list = [NonSlotted(i, i) for i in range(1000)]
print(f"Slotted total: {sys.getsizeof(slotted_list) + sum(sys.getsizeof(s) for s in slotted_list)}")
print(f"NonSlotted total: {sys.getsizeof(nonslotted_list) + sum(sys.getsizeof(ns) for ns in nonslotted_list)}")
```

### Q308: Explain Python's module cache mechanism
**Answer:**
`sys.modules` is a dict caching all imported modules. `import` first checks this cache. Reloading requires explicit `importlib.reload()`.

```python
import sys
import importlib

# Module cache
print('json' in sys.modules)  # False initially

import json
print('json' in sys.modules)  # True
print(sys.modules['json'])

# Modifying a cached module
import math
original_id = id(sys.modules['math'])
print(f"Original: {original_id}")

# Reimport doesn't re-execute
import math  # No-op, uses cache
print(id(sys.modules['math']) == original_id)  # True

# Force reload (executes again)
importlib.reload(math)
print(id(sys.modules['math']) == original_id)  # True (same object, re-executed)

# Remove from cache
del sys.modules['json']
import json  # Now re-executes
```

### Q309: How does Python resolve attribute access internally?
**Answer:**
Attribute lookup follows: `__getattribute__` -> data descriptor -> `__dict__` -> non-data descriptor -> `__getattr__`.

```python
class Descriptor:
    def __get__(self, obj, objtype=None):
        return "descriptor value"

class NonDataDescriptor:
    def __get__(self, obj, objtype=None):
        return "non-data descriptor"

class MyClass:
    data_desc = Descriptor()        # Data descriptor (has __set__ or __delete__)
    non_data = NonDataDescriptor()  # Non-data descriptor (only __get__)

    def __init__(self):
        self.data_desc = "instance value"
        self.non_data = "instance value"
        self.normal = "normal"

    def __getattr__(self, name):
        return f"fallback for {name}"

obj = MyClass()
print(obj.data_desc)  # "descriptor value" (data descriptor wins over instance)
print(obj.non_data)   # "instance value" (instance wins over non-data descriptor)
print(obj.normal)     # "normal" (instance __dict__)
print(obj.missing)    # "fallback for missing" (__getattr__)
```

### Q310: What is the difference between `__init_subclass__` and metaclasses?
**Answer:**
`__init_subclass__` is called when a subclass is created (PEP 487). It's simpler than metaclasses for class customization.

```python
# Using __init_subclass__
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.required_attr = getattr(cls, 'required_attr', None)
        if cls.required_attr is None:
            raise TypeError(f"{cls.__name__} must define required_attr")
        cls.created = True

class GoodChild(Base):
    required_attr = 42

# class BadChild(Base):
#     pass  # TypeError!

# Using metaclass (equivalent but more complex)
class RequiredMeta(type):
    def __new__(mcs, name, bases, attrs):
        if 'required_attr' not in attrs and not any(hasattr(b, 'required_attr') for b in bases):
            raise TypeError(f"{name} must define required_attr")
        return super().__new__(mcs, name, bases, attrs)

class GoodChild2(metaclass=RequiredMeta):
    required_attr = 42
```

### Q311: How does Python compile code to bytecode?
**Answer:**
Python source is compiled to bytecode (`.pyc` files) which the Python VM interprets. The `compile()` built-in and `dis` module show this.

```python
import dis
import py_compile
import marshal

# Source to bytecode
source = "x = 42; print(x * 2)"
code_obj = compile(source, '<string>', 'exec')

# Disassemble bytecode
dis.dis(code_obj)
#   0 RESUME                   0
#   2 LOAD_CONST               0 (42)
#   4 STORE_NAME               0 (x)
#   6 LOAD_NAME                0 (x)
#   8 LOAD_CONST               1 (2)
#  10 BINARY_OP                5 (*)
#  14 CALL_NAME                1 (print)
#  16 RETURN_VALUE

# Code object attributes
print(code_obj.co_code)      # Raw bytecode
print(code_obj.co_consts)    # (42, 2, None)
print(code_obj.co_names)     # ('x', 'print')
print(code_obj.co_stacksize) # Maximum stack size

# Cache bytecode
import importlib.util
spec = importlib.util.spec_from_file_location("module", "/tmp/test.py")
```

### Q312: What are Python's abstract base classes (ABC)?
**Answer:**
ABCs define interfaces that subclasses must implement. They use `@abstractmethod` to enforce method implementation.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

    def description(self):  # Concrete method
        return f"{self.__class__.__name__} with area {self.area()}"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius

# c = Shape()  # TypeError: Can't instantiate abstract class
c = Circle(5)
print(c.description())  # Circle with area 78.53975

# Virtual subclass (register as subclass without inheritance)
from collections.abc import Sequence

class MyList:
    def __getitem__(self, index):
        return index
    def __len__(self):
        return 42

Sequence.register(MyList)
print(isinstance(MyList(), Sequence))  # True
```

### Q313: What are context managers and how to create custom ones?
**Answer:**
Context managers handle setup/teardown via `__enter__`/`__exit__`. Can also use `@contextmanager` decorator.

```python
from contextlib import contextmanager
import time

# Class-based
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start
        print(f"Elapsed: {self.elapsed:.4f}s")
        return False  # Don't suppress exceptions

with Timer() as t:
    sum(range(10**6))
print(f"Timer said: {t.elapsed:.4f}s")

# Generator-based
@contextmanager
def timer():
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"Elapsed: {elapsed:.4f}s")

with timer():
    sum(range(10**6))

# Context manager with exception handling
class SafeOpen:
    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        if exc_type == FileNotFoundError:
            print(f"{self.filename} not found, continuing...")
            return True  # Suppress this specific exception
        return False
```

### Q314: How does the `__import__` function work?
**Answer:**
`__import__` is the built-in function that implements the import statement. It uses `importlib` internally.

```python
# Direct __import__ usage
module_name = "json"
json_module = __import__(module_name)
print(json_module.dumps({"a": 1}))

# With fromlist for from X import Y
# __import__("os.path") returns os (top-level)
# To get os.path:
path_module = __import__("os.path", fromlist=["path"])
print(path_module.join("a", "b"))

# Importlib equivalent (preferred)
import importlib
json_mod = importlib.import_module("json")

# Custom import hook
import sys
class LoggerFinder:
    def find_spec(self, fullname, path, target=None):
        print(f"Importing: {fullname}")
        return None  # Let default finders handle it

sys.meta_path.insert(0, LoggerFinder())
import math  # Prints "Importing: math"
```

### Q315: What is `sys.settrace` and how is it used?
**Answer:**
`sys.settrace` sets a trace function for debugging, coverage, or profiling. Called for each line/function call/exception.

```python
import sys

def trace_calls(frame, event, arg):
    if event == 'call':
        print(f"Calling {frame.f_code.co_name}")
    elif event == 'line':
        print(f"Line {frame.f_lineno} in {frame.f_code.co_name}")
    elif event == 'return':
        print(f"Returning from {frame.f_code.co_name} -> {arg}")
    return trace_calls  # Return to trace inside this function

# Set tracer
sys.settrace(trace_calls)

def example():
    x = 10
    y = x + 5
    return y

result = example()
sys.settrace(None)  # Disable tracing

# Practical use: debugger
import pdb
# pdb.set_trace()  # Drop into debugger
```

### Q316: How does Python implement string interning?
**Answer:**
Python interns some strings (reuses same object) for optimization. Small strings, identifiers, and some string literals are automatically interned.

```python
# Automatically interned: identifiers, keywords
a = "hello"
b = "hello"
print(a is b)  # True (interned)

# Not interned (typically)
c = "hello world!"
d = "hello world!"
print(c is d)  # False (not interned)

# Dynamic strings
e = " ".join(["hello", "world"])
f = " ".join(["hello", "world"])
print(e is f)  # False

# Explicit interning
import sys
g = sys.intern("".join(["he", "llo"]))
h = sys.intern("".join(["he", "llo"]))
print(g is h)  # True

# Performance benefit
import time
strings = ["hello_" + str(i) for i in range(10000)]
interned = [sys.intern(s) for s in strings]

# Dict lookup benefit with interning
d = {s: i for i, s in enumerate(interned)}
start = time.time()
for s in interned:
    _ = d[s]
print(f"With interning: {time.time() - start:.4f}s")
```

### Q317: What is the difference between `__new__` in Python 2 vs 3?
**Answer:**
Python 3 unified types and classes. In Python 3, `object.__new__` is always the base. `super().__new__(cls)` works consistently.

```python
# Python 3 style
class CustomList(list):
    def __new__(cls, iterable=None):
        if iterable is None:
            iterable = []
        instance = super().__new__(cls)
        # Don't initialize in __new__
        return instance

    def __init__(self, iterable=None):
        if iterable is None:
            iterable = []
        super().__init__(iterable)

cl = CustomList([1, 2, 3])
print(cl)        # [1, 2, 3]
print(type(cl))  # <class '__main__.CustomList'>

# Immutable requires __new__
class ConstTuple(tuple):
    def __new__(cls, data):
        # Filter out negatives
        filtered = tuple(x for x in data if x >= 0)
        return super().__new__(cls, filtered)

ct = ConstTuple([1, -2, 3, -4])
print(ct)  # (1, 3)
```

### Q318: How does Python handle keyword arguments internally?
**Answer:**
Python packs keyword arguments into a dict (using `**kwargs`) and passes them to functions. The `inspect` module reveals function signatures.

```python
import inspect

def func(a, b=2, *args, c=3, **kwargs):
    pass

sig = inspect.signature(func)
for name, param in sig.parameters.items():
    print(f"{name}: kind={param.kind.name}, default={param.default!r}")
# a: kind=POSITIONAL_OR_KEYWORD, default=<empty>
# b: kind=POSITIONAL_OR_KEYWORD, default=2
# args: kind=VAR_POSITIONAL, default=<empty>
# c: kind=KEYWORD_ONLY, default=3
# kwargs: kind=VAR_KEYWORD, default=<empty>

# Internal mechanics
def example(**kwargs):
    print(kwargs)  # Dict of keyword args

example(a=1, b=2)  # {'a': 1, 'b': 2}

# Binding arguments
ba = sig.bind(10, 20, 30, c=40, d=50)
ba.apply_defaults()
print(ba.arguments)
# {'a': 10, 'b': 20, 'args': (30,), 'c': 40, 'kwargs': {'d': 50}}
```

### Q319: Explain Python's `__prepare__` in metaclasses
**Answer:**
`__prepare__` returns a dict-like object for the class namespace. Allows ordered namespaces or custom class building.

```python
from collections import OrderedDict

class OrderedMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return OrderedDict()

    def __new__(mcs, name, bases, namespace):
        namespace['_order'] = list(namespace.keys())
        return super().__new__(mcs, name, bases, namespace)

class MyClass(metaclass=OrderedMeta):
    b = 2
    a = 1
    c = 3

print(MyClass._order)  # ['__module__', '__qualname__', 'b', 'a', 'c']

# Custom namespace with validation
class ValidatedNamespace(dict):
    def __setitem__(self, key, value):
        if key.startswith('_'):
            pass  # Allow private attributes
        elif not callable(value) and not isinstance(value, (int, float, str)):
            raise TypeError(f"Only primitives allowed, got {type(value)}")
        super().__setitem__(key, value)

class ValidatedMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return ValidatedNamespace()

class ValidClass(metaclass=ValidatedMeta):
    x = 10      # OK
    y = "hello" # OK
    # z = [1,2]  # TypeError
```

### Q320: How does Python's `secrets` module generate secure random data?
**Answer:**
The `secrets` module uses OS-provided cryptographically secure random sources (`/dev/urandom` on Linux, `CryptGenRandom` on Windows).

```python
import secrets
import string

# Random token generation
print(secrets.token_bytes(16))      # 16 random bytes
print(secrets.token_hex(16))        # 32 hex chars
print(secrets.token_urlsafe(16))    # URL-safe base64

# Secure password generation
alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
password = ''.join(secrets.choice(alphabet) for _ in range(20))
print(f"Password: {password}")

# Secure comparison (timing-attack resistant)
a = b'secret-key-123'
b = b'secret-key-456'
print(secrets.compare_digest(a, b))  # False
print(secrets.compare_digest(a, a))  # True

# Random integers in range [low, high]
print(secrets.randbelow(100))   # 0-99
print(secrets.choice(['a', 'b', 'c']))  # Random element
```

### Q321: How does the `async`/`await` syntax work internally?
**Answer:**
`async def` creates a coroutine function. `await` yields control to the event loop. Coroutines use `__await__` which returns an iterator.

```python
import asyncio
import types

# Manual coroutine implementation
@types.coroutine
def sleep(delay):
    yield from asyncio.sleep(delay)

async def hello():
    print("Hello")
    await sleep(1)  # Yield to event loop
    print("World")

# Running manually
coro = hello()
print(type(coro))  # <class 'coroutine'>
print(dir(coro))   # send, throw, close, __await__

# Manual step-through (without loop)
async def simple():
    return 42

coro2 = simple()
try:
    coro2.send(None)
except StopIteration as e:
    print(f"Result: {e.value}")  # 42

# Internally, awaitables must be:
# 1. A coroutine (from async def)
# 2. An object with __await__ returning iterator
class Awaitable:
    def __await__(self):
        yield from asyncio.sleep(0)
        return "done"

async def test():
    result = await Awaitable()
    print(result)
```

### Q322: What is `__all__` in Python modules?
**Answer:**
`__all__` defines the public API of a module. Controls what `from module import *` exports.

```python
# In a module named mymodule.py
# __all__ = ['public_func', 'PublicClass']

# _private_func is still importable explicitly
# but not with from mymodule import *

import types

# Create module-like example
module_code = ### Q351: How do you handle missing values in pandas?
**Answer:**
```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'A': [1, 2, np.nan, 4, 5],
    'B': [np.nan, 2, 3, np.nan, 5],
    'C': [1, 2, 3, 4, 5]
})

# Detect missing
print(df.isnull().sum())
print(df.isna().any())

# Drop missing
df_dropped_rows = df.dropna()           # Drop rows with any NaN
df_dropped_cols = df.dropna(axis=1)      # Drop columns with any NaN
df_drop_thresh = df.dropna(thresh=3)     # Keep rows with at least 3 non-NaN

# Fill missing
df_fill = df.fillna(0)                         # Fill with constant
df_ffill = df.fillna(method='ffill')            # Forward fill
df_bfill = df.fillna(method='bfill')            # Backward fill
df_interpolate = df.interpolate()               # Linear interpolation
df_mean_fill = df.fillna(df.mean())             # Fill with column mean

# Boolean indexing for missing
rows_with_missing = df[df.isnull().any(axis=1)]
```

### Q352: What is the difference between apply, map, and applymap in pandas?
**Answer:**
```python
import pandas as pd
import numpy as np

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# map - Series only
df['A_mapped'] = df['A'].map({1: 'one', 2: 'two', 3: 'three'})

# apply - DataFrame
df['sum_row'] = df.apply(lambda row: row['A'] + row['B'], axis=1)
df_sqrt = df.apply(np.sqrt)

# applymap - element-wise on DataFrame
df_formatted = df.applymap(lambda x: f"${x:.2f}")
```

### Q353: How do you merge, join, and concatenate DataFrames?
**Answer:**
```python
import pandas as pd

df1 = pd.DataFrame({'key': ['A', 'B', 'C'], 'val1': [1, 2, 3]})
df2 = pd.DataFrame({'key': ['B', 'C', 'D'], 'val2': [4, 5, 6]})

# Merge (SQL-like)
inner = pd.merge(df1, df2, on='key', how='inner')    # A B C -> B C
left = pd.merge(df1, df2, on='key', how='left')      # All df1 keys
right = pd.merge(df1, df2, on='key', how='right')     # All df2 keys
outer = pd.merge(df1, df2, on='key', how='outer')     # All keys

# Join (index-based)
df1_idx = df1.set_index('key')
df2_idx = df2.set_index('key')
joined = df1_idx.join(df2_idx, how='left')

# Concatenate (stack)
concat_rows = pd.concat([df1, df2], axis=0)   # Stack vertically
concat_cols = pd.concat([df1, df2], axis=1)   # Stack horizontally
```

### Q354: Explain pandas groupby operations
**Answer:**
```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'dept': ['HR', 'IT', 'HR', 'IT', 'HR'],
    'salary': [50000, 80000, 55000, 90000, 48000],
    'bonus': [2000, 5000, 3000, 7000, 1500]
})

# Basic groupby
grouped = df.groupby('dept')

# Aggregation
result = df.groupby('dept').agg({
    'salary': ['mean', 'std', 'min', 'max'],
    'bonus': 'sum'
})

# Transform (same shape as original)
df['salary_pct'] = df.groupby('dept')['salary'].transform(
    lambda x: x / x.sum()
)

# Filter groups
filtered = df.groupby('dept').filter(lambda x: x['salary'].mean() > 60000)

# Apply custom function
def top_salary(group, n=2):
    return group.nlargest(n, 'salary')

top = df.groupby('dept').apply(top_salary, n=1)
```

### Q355: What is the difference between iloc and loc in pandas?
**Answer:**
```python
import pandas as pd

df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
}, index=['x', 'y', 'z'])

# loc: label-based
print(df.loc['x'])           # Row with index 'x'
print(df.loc['x':'y'])       # Slicing by label (inclusive)
print(df.loc['x', 'A'])      # Specific cell
print(df.loc[:, ['A', 'B']]) # All rows, columns A and B

# iloc: integer position-based
print(df.iloc[0])            # First row
print(df.iloc[0:2])          # First 2 rows (exclusive)
print(df.iloc[0, 0])         # First row, first column
print(df.iloc[:, [0, 1]])    # All rows, first 2 columns

# Key differences
# loc includes endpoint in slice, iloc does not
# loc uses index labels, iloc uses integer positions
# loc can use boolean arrays, iloc uses integer/boolean positions
```

### Q356: How do you handle datetime data in pandas?
**Answer:**
```python
import pandas as pd

# Parse dates
df = pd.DataFrame({'date': ['2026-01-01', '2026-01-15', '2026-02-01']})
df['date'] = pd.to_datetime(df['date'])

# Date features
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['dayofweek'] = df['date'].dt.dayofweek  # Monday=0
df['quarter'] = df['date'].dt.quarter
df['is_weekend'] = df['date'].dt.dayofweek >= 5

# Date range
dates = pd.date_range('2026-01-01', periods=10, freq='D')
dates_monthly = pd.date_range('2026-01-01', periods=12, freq='M')

# Resampling
ts = pd.Series([1, 2, 3, 4], index=pd.date_range('2026-01-01', periods=4, freq='D'))
weekly = ts.resample('W').sum()
monthly = ts.resample('M').mean()

# Time differences
df['days_since_start'] = (df['date'] - pd.Timestamp('2026-01-01')).dt.days

# Shifting/lagging
df['prev_day'] = df['date'].shift(1)
df['next_day'] = df['date'].shift(-1)
```

### Q357: What is the difference between numpy array and Python list?
**Answer:**
```python
import numpy as np
import sys
import time

# Memory efficiency
py_list = list(range(1000))
np_array = np.arange(1000)
print(f"List: {sys.getsizeof(py_list)} bytes")
print(f"Array: {sys.getsizeof(np_array)} bytes")  # Smaller

# Homogeneous typing
np_array = np.array([1, 2, 3], dtype=np.float32)
# All elements same type

# Vectorized operations
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a + b)       # [5, 7, 9]
print(a * b)       # [4, 10, 18]
print(np.dot(a, b))  # 32

# Broadcasting
print(a + 10)  # [11, 12, 13]

# Performance
py = list(range(10**6))
np_arr = np.arange(10**6)

start = time.time()
py_sum = [x * 2 for x in py]
print(f"List comprehension: {time.time() - start:.3f}s")

start = time.time()
np_result = np_arr * 2
print(f"NumPy vectorized: {time.time() - start:.3f}s")  # ~10-50x faster
```

### Q358: How does numpy broadcasting work?
**Answer:**
```python
import numpy as np

# Broadcasting rules: compare dimensions from right to left,
# dimensions must be equal or one of them must be 1

a = np.array([[1, 2, 3],
              [4, 5, 6]])  # Shape (2, 3)
b = np.array([10, 20, 30])   # Shape (3,)

result = a + b
# b broadcasts to match a:
# [[10, 20, 30],
#  [10, 20, 30]]

# Scalars broadcast to everything
print(a * 2)
# [[2, 4, 6],
#  [8, 10, 12]]

# Column vector broadcasting
c = np.array([[10], [20]])  # Shape (2, 1)
print(a + c)
# [[11, 12, 13],
#  [24, 25, 26]]

# Broadcasting error
try:
    d = np.array([1, 2])  # Shape (2,)
    a + d  # ValueError: operands could not be broadcast together
except ValueError as e:
    print(f"Error: {e}")
```

### Q359: Explain numpy reshaping operations
**Answer:**
```python
import numpy as np

a = np.arange(12)

# Reshape
b = a.reshape(3, 4)     # 3 rows, 4 cols
c = a.reshape(2, -1)    # -1 infers dimension: (2, 6)

# Flatten / Ravel
d = b.flatten()          # Returns copy
e = b.ravel()            # Returns view (if possible)
e[0] = 99
print(b[0, 0])           # 99 (ravel modified original)

# Transpose
f = b.T                  # (4, 3)
g = b.transpose()        # Same

# Expand / squeeze
h = np.expand_dims(a, axis=0)  # (1, 12)
i = np.squeeze(h)              # Back to (12,)

# Stack / concatenate
a1 = np.array([1, 2, 3])
a2 = np.array([4, 5, 6])
vstack = np.vstack([a1, a2])   # Vertical (2, 3)
hstack = np.hstack([a1, a2])   # Horizontal (6,)
```

### Q360: How do you handle categorical data in pandas?
**Answer:**
```python
import pandas as pd

df = pd.DataFrame({
    'color': ['red', 'blue', 'green', 'red', 'blue'],
    'size': ['S', 'M', 'L', 'M', 'S']
})

# Convert to categorical
df['color'] = df['color'].astype('category')
print(df['color'].cat.categories)  # ['blue', 'green', 'red']

# One-hot encoding
one_hot = pd.get_dummies(df['color'], prefix='color')
print(one_hot)

# Label encoding
df['color_code'] = df['color'].cat.codes

# Factorize (alternative)
codes, uniques = pd.factorize(df['size'])
print(codes)    # [0, 1, 2, 1, 0]
print(uniques)  # ['S', 'M', 'L']

# Ordinal encoding with mapping
size_map = {'S': 1, 'M': 2, 'L': 3}
df['size_ordinal'] = df['size'].map(size_map)
```

### Q361: How does numpy handle random number generation?
**Answer:**
```python
import numpy as np

# Modern API (preferred)
rng = np.random.default_rng(seed=42)

# Distributions
print(rng.random(5))         # Uniform [0, 1)
print(rng.normal(0, 1, 5))   # Normal(mean=0, std=1)
print(rng.integers(0, 10, 5))  # Random integers [0, 10)
print(rng.uniform(0, 10, 5))   # Uniform [0, 10)

# Shuffle / permutation
arr = np.arange(10)
rng.shuffle(arr)             # In-place
perm = rng.permutation(10)   # New array

# Choice
print(rng.choice(['a', 'b', 'c'], size=5, p=[0.5, 0.3, 0.2]))

# Legacy API (still common)
np.random.seed(42)
print(np.random.rand(5))     # Uniform [0, 1)
print(np.random.randn(5))    # Standard normal
print(np.random.randint(0, 10, 5))
```

### Q362: How do you handle outliers in data?
**Answer:**
```python
import numpy as np
import pandas as pd

data = pd.Series([1, 2, 3, 4, 5, 100, 6, 7, 8, 9, -50])

# Z-score method
from scipy import stats
z_scores = np.abs(stats.zscore(data))
outliers_z = data[z_scores > 3]
cleaned_z = data[z_scores <= 3]

# IQR method
Q1 = data.quantile(0.25)
Q3 = data.quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers_iqr = data[(data < lower) | (data > upper)]
cleaned_iqr = data[(data >= lower) & (data <= upper)]

# Winsorization (cap instead of remove)
capped = data.clip(lower=lower, upper=upper)

# Percentile-based
lower_pct = data.quantile(0.01)
upper_pct = data.quantile(0.99)
capped_pct = data.clip(lower=lower_pct, upper=upper_pct)

print(f"Outliers (IQR): {outliers_iqr.tolist()}")
```

### Q363: Explain the difference between wide and long format data
**Answer:**
```python
import pandas as pd

# Wide format (one row per subject, one column per measurement)
wide = pd.DataFrame({
    'id': [1, 2, 3],
    'treatment_a': [5, 3, 7],
    'treatment_b': [6, 4, 8]
})

# Melt to long format
long = pd.melt(wide,
    id_vars=['id'],
    value_vars=['treatment_a', 'treatment_b'],
    var_name='treatment',
    value_name='score'
)
print(long)
#    id    treatment  score
# 0   1  treatment_a      5
# 1   2  treatment_a      3
# 2   3  treatment_a      7
# 3   1  treatment_b      6
# 4   2  treatment_b      4
# 5   3  treatment_b      8

# Pivot back to wide
wide_again = long.pivot(
    index='id',
    columns='treatment',
    values='score'
).reset_index()
```

### Q364: How do you handle time series data in pandas?
**Answer:**
```python
import pandas as pd
import numpy as np

# Create time series
dates = pd.date_range('2026-01-01', periods=100, freq='D')
ts = pd.Series(np.random.randn(100), index=dates)

# Rolling windows
ts_rolling_mean = ts.rolling(window=7).mean()
ts_rolling_std = ts.rolling(window=7).std()
ts_rolling_max = ts.rolling(window=7).max()

# Exponential weighted
ts_ewm = ts.ewm(span=10).mean()

# Differencing
ts_diff = ts.diff().dropna()          # First order
ts_diff2 = ts.diff().diff().dropna()  # Second order

# Lag features
pd.DataFrame({
    'value': ts,
    'lag_1': ts.shift(1),
    'lag_7': ts.shift(7),
    'rolling_mean_7': ts.rolling(7).mean()
})

# Stationarity test
from statsmodels.tsa.stattools import adfuller
result = adfuller(ts.dropna())
print(f"ADF Statistic: {result[0]:.4f}")
print(f"p-value: {result[1]:.4f}")
print("Stationary" if result[1] < 0.05 else "Non-stationary")
```

### Q365: What is the difference between train_test_split and cross-validation?
**Answer:**
```python
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Cross-validation
model = RandomForestClassifier(n_estimators=100)
scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
print(f"CV scores: {scores}")
print(f"Mean: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")

# Manual K-fold
kf = KFold(n_splits=5, shuffle=True, random_state=42)
for fold, (train_idx, val_idx) in enumerate(kf.split(X_train)):
    X_fold_train = X_train[train_idx]
    X_fold_val = X_train[val_idx]
    y_fold_train = y_train[train_idx]
    y_fold_val = y_train[val_idx]
    model.fit(X_fold_train, y_fold_train)
    score = model.score(X_fold_val, y_fold_val)
    print(f"Fold {fold + 1}: {score:.3f}")
```

### Q366: How do you handle imbalanced datasets?
**Answer:**
```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
import numpy as np

# Create imbalanced dataset
X, y = make_classification(
    n_samples=1000, weights=[0.9, 0.1], random_state=42
)
print(f"Class distribution: {np.bincount(y)}")  # [900, 100]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# 1. Resampling
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
print(f"After SMOTE: {np.bincount(y_resampled)}")

# 2. Class weights
model_weighted = RandomForestClassifier(class_weight='balanced')
model_weighted.fit(X_train, y_train)

# 3. Undersampling
undersampler = RandomUnderSampler(random_state=42)
X_under, y_under = undersampler.fit_resample(X_train, y_train)

# 4. Pipeline with resampling
pipeline = Pipeline([
    ('sampler', SMOTE()),
    ('classifier', RandomForestClassifier())
])
pipeline.fit(X_train, y_train)

# Evaluation (use precision/recall, not accuracy)
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))
```

### Q367: Explain feature scaling techniques
**Answer:**
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import numpy as np

data = np.array([[1, 100],
                 [2, 200],
                 [3, 300],
                 [4, 400],
                 [100, 500]])  # Outlier in first column

# StandardScaler (z-score): mean=0, std=1
standard = StandardScaler()
print(standard.fit_transform(data))

# MinMaxScaler: range [0, 1]
minmax = MinMaxScaler()
print(minmax.fit_transform(data))

# RobustScaler: robust to outliers (uses median, IQR)
robust = RobustScaler()
print(robust.fit_transform(data))

# When to use which:
# - StandardScaler: most ML algorithms (SVM, logistic regression, PCA)
# - MinMaxScaler: neural networks, distance-based algorithms (KNN)
# - RobustScaler: data with outliers
# - Normalizer: text classification, when magnitude doesn't matter
```

### Q368: What is the bias-variance tradeoff?
**Answer:**
```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

# Generate data
np.random.seed(42)
X = np.linspace(0, 10, 50).reshape(-1, 1)
y = np.sin(X).ravel() + np.random.normal(0, 0.3, 50)

# High bias (underfitting) - degree 1
# High variance (overfitting) - degree 15
# Good balance - degree 3

degrees = [1, 3, 15]
for d in degrees:
    model = Pipeline([
        ('poly', PolynomialFeatures(degree=d)),
        ('linear', LinearRegression())
    ])
    model.fit(X, y)
    pred = model.predict(X)
    mse = mean_squared_error(y, pred)
    print(f"Degree {d}: MSE = {mse:.4f}")

# Bias: error from wrong assumptions
# Variance: error from sensitivity to training data
# Tradeoff: increasing complexity reduces bias but increases variance
```

### Q369: Explain precision, recall, F1-score, and ROC-AUC
**Answer:**
```python
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix,
    classification_report
)
import numpy as np

y_true = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
y_pred = np.array([0, 1, 1, 1, 0, 0, 0, 1, 0, 1])
y_prob = np.array([0.1, 0.9, 0.6, 0.8, 0.2, 0.3, 0.1, 0.7, 0.4, 0.85])

# Confusion matrix
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
print(f"TP={tp}, TN={tn}, FP={fp}, FN={fn}")

# Metrics
precision = precision_score(y_true, y_pred)  # TP / (TP + FP)
recall = recall_score(y_true, y_pred)        # TP / (TP + FN)
f1 = f1_score(y_true, y_pred)                # 2 * P * R / (P + R)
auc = roc_auc_score(y_true, y_prob)

print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1: {f1:.3f}")
print(f"ROC-AUC: {auc:.3f}")

# Full report
print(classification_report(y_true, y_pred))
```

### Q370: How does PCA work?
**Answer:**
```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Generate correlated data
np.random.seed(42)
X = np.random.randn(100, 3)
X[:, 1] = X[:, 0] * 2 + np.random.randn(100) * 0.1  # Correlated
X[:, 2] = X[:, 0] * -1 + np.random.randn(100) * 0.1  # Correlated

# Standardize (required for PCA)
X_scaled = StandardScaler().fit_transform(X)

# Apply PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Explained variance
print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
print(f"Cumulative: {pca.explained_variance_ratio_.cumsum()}")

# Components (loadings)
print(f"Components:
{pca.components_}")

# Manual PCA
cov = np.cov(X_scaled.T)
eigenvalues, eigenvectors = np.linalg.eigh(cov)
idx = np.argsort(eigenvalues)[::-1]
print(f"Eigenvalues: {eigenvalues[idx]}")
```

### Q371: What is the difference between L1 and L2 regularization?
**Answer:**
```python
from sklearn.linear_model import Lasso, Ridge, ElasticNet
import numpy as np

np.random.seed(42)
X = np.random.randn(100, 10)
y = X[:, 0] * 2 + X[:, 1] * 0.5 + np.random.randn(100) * 0.1

# L1 (Lasso) - feature selection, sparse solutions
lasso = Lasso(alpha=0.1)
lasso.fit(X, y)
print(f"Lasso coefficients: {lasso.coef_}")
# Many coefficients become exactly zero

# L2 (Ridge) - small but non-zero coefficients
ridge = Ridge(alpha=0.1)
ridge.fit(X, y)
print(f"Ridge coefficients: {ridge.coef_}")
# All coefficients non-zero, shrunk toward zero

# ElasticNet - combination of L1 and L2
elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)
elastic.fit(X, y)

# L1 adds |coefficient| penalty (sum of absolute values)
# L2 adds coefficient^2 penalty (sum of squares)
# L1 produces sparsity, L2 handles multicollinearity better
```

### Q372: Explain the concept of overfitting and how to prevent it
**Answer:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import learning_curve
import numpy as np

# Overfitting symptoms:
# - High training accuracy, low test accuracy
# - Complex models that memorize noise
# - Learning curve shows large gap between train and test

# Prevention techniques:

# 1. Cross-validation
# 2. Regularization (L1/L2)
# 3. Pruning (decision trees)
# 4. Early stopping (gradient boosting, neural nets)
# 5. Dropout (neural networks)
# 6. Data augmentation
# 7. Feature selection
# 8. Ensembling (Random Forest reduces overfitting vs single tree)

# Example: Reducing overfitting in Random Forest
overfit_rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=None,      # Fully grown trees - overfits
    min_samples_leaf=1
)

regularized_rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,         # Limit depth
    min_samples_leaf=5,   # Require minimum samples per leaf
    max_features='sqrt',  # Limit features per split
    min_samples_split=10  # Minimum samples to split
)

# Learning curve helps detect overfitting
def plot_learning_curve(model, X, y):
    train_sizes, train_scores, test_scores = learning_curve(
        model, X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10)
    )
    train_mean = np.mean(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    gap = train_mean - test_mean
    print(f"Train-test gap: {gap[-1]:.4f}")
    return train_mean, test_mean
```

### Q373: How does gradient descent work?
**Answer:**
```python
import numpy as np

# Simple gradient descent for linear regression
np.random.seed(42)
X = np.random.randn(100, 1)
y = 3 * X.squeeze() + 2 + np.random.randn(100) * 0.5

# Gradient descent
def gradient_descent(X, y, lr=0.01, epochs=100):
    m = len(X)
    theta = np.random.randn(2)  # [bias, weight]
    X_b = np.c_[np.ones((m, 1)), X]  # Add bias term

    for epoch in range(epochs):
        gradients = 2/m * X_b.T @ (X_b @ theta - y)
        theta -= lr * gradients

        if epoch % 20 == 0:
            mse = np.mean((X_b @ theta - y) ** 2)
            print(f"Epoch {epoch}: MSE = {mse:.4f}, theta = {theta}")

    return theta

theta = gradient_descent(X, y, lr=0.1, epochs=100)
print(f"Found: intercept={theta[0]:.2f}, slope={theta[1]:.2f}")
print(f"True:  intercept=2.00, slope=3.00")
```

### Q374: What is the difference between bagging and boosting?
**Answer:**
```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

# Bagging (Bootstrap Aggregating)
# - Train models in parallel on bootstrap samples
# - Reduce variance
# - Random Forest is bagging on steroids
bagging = RandomForestClassifier(
    n_estimators=100,
    max_samples=0.8,  # Bootstrap sample size
    bootstrap=True
)

# Boosting
# - Train models sequentially, each correcting previous errors
# - Reduce bias
# - Gradient Boosting, AdaBoost, XGBoost
boosting = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3
)

# Key differences:
# Bagging: parallel, high bias models -> ensemble reduces variance
# Boosting: sequential, weak learners -> ensemble reduces bias
# Bagging: each model has equal weight
# Boosting: models weighted by performance
# Bagging: less prone to overfitting
# Boosting: more prone to overfitting (need careful tuning)
```

### Q375: Explain the Poisson distribution and when to use it
**Answer:**
```python
import numpy as np

# Poisson: models count of events in fixed interval
# lambda = average rate
# Used for: customer arrivals, defect counts, website visits

from scipy import stats

# PMF: P(X=k) = (lambda^k * e^-lambda) / k!
lam = 3  # Average 3 events per interval
poisson = stats.poisson(lam)

# Probability of exactly 2 events
print(f"P(X=2): {poisson.pmf(2):.4f}")

# Probability of <= 2 events
print(f"P(X<=2): {poisson.cdf(2):.4f}")

# Generate samples
samples = poisson.rvs(size=1000, random_state=42)
print(f"Mean: {samples.mean():.2f} (expected {lam})")
print(f"Var: {samples.var():.2f} (expected {lam})")

# Real-world example: website visits per minute
visits_per_minute = np.random.poisson(lam=5, size=60)
print(f"Visits in 60 min: mean={visits_per_minute.mean():.1f}")
```

### Q376: What is the difference between Type I and Type II errors?
**Answer:**
```python
import numpy as np
from scipy import stats

# Type I (False Positive): Reject null when it's true
# Type II (False Negative): Fail to reject null when it's false

# Example: A/B testing
np.random.seed(42)
control = np.random.normal(100, 15, 1000)
treatment = np.random.normal(103, 15, 1000)  # Small effect

# Two-sample t-test
t_stat, p_value = stats.ttest_ind(control, treatment)
print(f"t-stat: {t_stat:.3f}, p-value: {p_value:.4f}")

alpha = 0.05  # Significance level
if p_value < alpha:
    print("Reject null (significant difference)")
    # Risk of Type I error: alpha (5%)
else:
    print("Fail to reject null (no significant difference)")
    # Risk of Type II error: beta (depends on sample size, effect size)

# Power = 1 - beta (probability of detecting real effect)
from statsmodels.stats.power import TTestIndPower
power_analysis = TTestIndPower()
required_n = power_analysis.solve_power(
    effect_size=0.3, power=0.8, alpha=0.05
)
print(f"Required sample size for 80% power: {required_n:.0f}")
```

### Q377: How do you perform feature selection?
**Answer:**
```python
from sklearn.feature_selection import (
    SelectKBest, f_classif, mutual_info_classif,
    RFE, SelectFromModel
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(
    n_samples=100, n_features=20, n_informative=5,
    n_redundant=5, random_state=42
)

# 1. Filter methods (statistical tests)
selector_kbest = SelectKBest(score_func=f_classif, k=10)
X_kbest = selector_kbest.fit_transform(X, y)
print(f"Selected features (ANOVA): {selector_kbest.get_support(indices=True)}")

# 2. Mutual information
mi = mutual_info_classif(X, y, random_state=42)
top_features = np.argsort(mi)[-10:]
print(f"Top features (MI): {top_features}")

# 3. Wrapper methods (RFE)
model = RandomForestClassifier()
rfe = RFE(estimator=model, n_features_to_select=10)
X_rfe = rfe.fit_transform(X, y)
print(f"Selected features (RFE): {rfe.get_support(indices=True)}")

# 4. Embedded methods (feature importance)
model.fit(X, y)
importance = model.feature_importances_
top_idx = np.argsort(importance)[-5:]
print(f"Top 5 features (importance): {top_idx}")

# 5. SelectFromModel
sfm = SelectFromModel(model, threshold='median')
X_sfm = sfm.fit_transform(X, y)
```

### Q378: What is the central limit theorem?
**Answer:**
```python
import numpy as np
import matplotlib.pyplot as plt

# CLT: distribution of sample means approaches normal
# regardless of population distribution, as sample size increases

# Population: exponential distribution (very non-normal)
population = np.random.exponential(scale=2, size=100000)

# Draw many samples, compute means
def sampling_distribution(pop, sample_size, num_samples=1000):
    means = []
    for _ in range(num_samples):
        sample = np.random.choice(pop, size=sample_size)
        means.append(np.mean(sample))
    return np.array(means)

# With small samples (n=5)
means_5 = sampling_distribution(population, 5)
print(f"n=5: mean={means_5.mean():.3f}, std={means_5.std():.3f}")

# With large samples (n=50)
means_50 = sampling_distribution(population, 50)
print(f"n=50: mean={means_50.mean():.3f}, std={means_50.std():.3f}")

# As n increases:
# 1. Distribution becomes more normal
# 2. Mean stays close to population mean (~2)
# 3. Std decreases (sqrt(n) relationship)
# Standard error = population_std / sqrt(n)
```

### Q379: How does K-means clustering work?
**Answer:**
```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import numpy as np

# Generate clusters
X, y_true = make_blobs(
    n_samples=300, centers=4, cluster_std=0.6, random_state=42
)

# K-means
kmeans = KMeans(n_clusters=4, random_state=42, n_init='auto')
y_pred = kmeans.fit_predict(X)

# Results
print(f"Cluster centers:
{kmeans.cluster_centers_}")
print(f"Inertia: {kmeans.inertia_:.2f}")

# Elbow method to find optimal k
inertias = []
K_range = range(1, 10)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init='auto')
    km.fit(X)
    inertias.append(km.inertia_)

print("Inertia by K:")
for k, inertia in zip(K_range, inertias):
    print(f"  K={k}: {inertia:.2f}")
```

### Q380: Explain the difference between correlation and causation
**Answer:**
```python
import numpy as np
from scipy import stats

# Correlation measures linear relationship (-1 to 1)
# Causation means one variable directly affects another

# Example: spurious correlation
np.random.seed(42)
n = 100
ice_cream_sales = np.random.normal(100, 20, n)
drowning_incidents = ice_cream_sales * 0.5 + np.random.normal(0, 10, n)

corr, pval = stats.pearsonr(ice_cream_sales, drowning_incidents)
print(f"Correlation: {corr:.3f}, p-value: {pval:.3f}")
# Strong correlation but NO causation
# Confounding variable: hot weather increases both

# Types of correlation
x = np.array([1, 2, 3, 4, 5])
y1 = np.array([2, 4, 6, 8, 10])   # Perfect positive: r=1
y2 = np.array([-2, -4, -6, -8, -10])  # Perfect negative: r=-1
y3 = np.array([10, 8, 6, 4, 2])   # Some negative correlation

# Pearson (linear) vs Spearman (monotonic)
x_nonlinear = np.array([1, 2, 3, 4, 5])
y_nonlinear = np.array([1, 4, 9, 16, 25])  # Quadratic
pearson, _ = stats.pearsonr(x_nonlinear, y_nonlinear)
spearman, _ = stats.spearmanr(x_nonlinear, y_nonlinear)
print(f"Pearson: {pearson:.3f}, Spearman: {spearman:.3f}")
```

### Q381: How do you handle non-linear relationships in regression?
**Answer:**
```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import numpy as np

# Non-linear data
np.random.seed(42)
X = np.linspace(-3, 3, 100).reshape(-1, 1)
y = 0.5 * X.ravel() ** 2 + X.ravel() + 2 + np.random.normal(0, 0.5, 100)

# Polynomial regression
poly = Pipeline([
    ('poly', PolynomialFeatures(degree=2, include_bias=False)),
    ('linear', LinearRegression())
])
poly.fit(X, y)

# Spline regression (scipy)
from scipy.interpolate import UnivariateSpline
spline = UnivariateSpline(X.ravel(), y, k=3, s=1)

# Decision tree / Random Forest (non-parametric)
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators=100)
rf.fit(X, y)

# Compare R2 scores
from sklearn.metrics import r2_score
y_pred_poly = poly.predict(X)
y_pred_spline = spline(X.ravel())
y_pred_rf = rf.predict(X)

print(f"Polynomial R2: {r2_score(y, y_pred_poly):.3f}")
print(f"Spline R2: {r2_score(y, y_pred_spline):.3f}")
print(f"Random Forest R2: {r2_score(y, y_pred_rf):.3f}")
```

### Q382: What is the difference between parametric and non-parametric models?
**Answer:**
```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
import numpy as np

# Parametric models: fixed number of parameters
# - Linear regression, logistic regression, Naive Bayes
# - Assumes specific distribution of data
# - Less flexible, lower variance, higher bias
# - Good with small data

logistic = LogisticRegression()
# Parameters: coefficients for each feature (fixed by feature count)

# Non-parametric models: parameters grow with data
# - KNN, Decision Trees, Random Forest
# - No assumption about data distribution
# - More flexible, higher variance, lower bias
# - Need more data

knn = KNeighborsClassifier(n_neighbors=5)
# "Parameters": all training data (stored as reference)

tree = DecisionTreeClassifier()
# Parameters: split decisions learned from data

# Example
np.random.seed(42)
X_small = np.random.randn(20, 2)
y_small = (X_small[:, 0] ** 2 + X_small[:, 1] ** 2 > 1).astype(int)

# Parametric (limited by linear decision boundary)
logistic.fit(X_small, y_small)
print(f"Linear params: {logistic.coef_.size}")

# Non-parametric (can learn complex boundaries)
tree.fit(X_small, y_small)
print(f"Tree nodes: {tree.tree_.node_count}")
```

### Q383: How does the confusion matrix work for multi-class classification?
**Answer:**
```python
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

y_true = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])
y_pred = np.array([0, 1, 1, 0, 2, 2, 0, 1, 2])

# Confusion matrix (3x3 for 3 classes)
cm = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:")
print(cm)
# [[3 0 0]  # Class 0: 3 correct
#  [0 1 1]  # Class 1: 1 correct, 1 predicted as 2
#  [0 0 2]] # Class 2: 2 correct

# Per-class metrics
report = classification_report(y_true, y_pred, output_dict=True)
for cls in ['0', '1', '2']:
    print(f"Class {cls}: precision={report[cls]['precision']:.2f}, "
          f"recall={report[cls]['recall']:.2f}, "
          f"f1={report[cls]['f1-score']:.2f}")

# Macro avg (unweighted mean across classes)
print(f"Macro avg F1: {report['macro avg']['f1-score']:.3f}")

# Weighted avg (weighted by class support)
print(f"Weighted avg F1: {report['weighted avg']['f1-score']:.3f}")
```

### Q384: Explain the concept of entropy and information gain
**Answer:**
```python
import numpy as np

# Entropy = -sum(p * log2(p))
# Measures impurity/uncertainty in data

def entropy(labels):
    _, counts = np.unique(labels, return_counts=True)
    probs = counts / len(labels)
    return -np.sum(probs * np.log2(probs))

# Pure set (all same class)
pure = np.array([0, 0, 0, 0])
print(f"Pure entropy: {entropy(pure):.3f}")  # 0

# Impure set (50/50 split)
impure = np.array([0, 0, 1, 1])
print(f"Impure entropy: {entropy(impure):.3f}")  # 1

# Information gain = parent_entropy - weighted_child_entropy
def information_gain(parent, children):
    parent_ent = entropy(parent)
    total = len(parent)
    weighted_children = sum(
        len(c) / total * entropy(c) for c in children
    )
    return parent_ent - weighted_children

# Example
parent = np.array([0, 0, 0, 1, 1, 1, 1, 1])
left = np.array([0, 0, 1])     # 2 zero, 1 one
right = np.array([0, 1, 1, 1, 1])  # 1 zero, 4 ones

ig = information_gain(parent, [left, right])
print(f"Information gain: {ig:.3f}")

# Gini impurity (alternative to entropy)
def gini(labels):
    _, counts = np.unique(labels, return_counts=True)
    probs = counts / len(labels)
    return 1 - np.sum(probs ** 2)
```

### Q385: What is the difference between bag of words and TF-IDF?
**Answer:**
```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

corpus = [
    "the cat sat on the mat",
    "the dog sat on the log",
    "cats and dogs are pets"
]

# Bag of Words (BoW): raw counts
bow = CountVectorizer()
X_bow = bow.fit_transform(corpus)
print("BoW features:", bow.get_feature_names_out())
print("BoW matrix:
", X_bow.toarray())

# TF-IDF: term frequency * inverse document frequency
# tf-idf(t,d) = tf(t,d) * log(N / df(t))
# Downweights common words, upweights rare/important words
tfidf = TfidfVectorizer()
X_tfidf = tfidf.fit_transform(corpus)
print("
TF-IDF features:", tfidf.get_feature_names_out())
print("TF-IDF matrix:
", X_tfidf.toarray())

# Key differences:
# BoW: simple counts, treats all words equally
# TF-IDF: reduces importance of common words (the, and)
# TF-IDF: better for information retrieval and text classification
```

### Q386: How does DBSCAN clustering work?
**Answer:**
```python
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons
import numpy as np

# DBSCAN: density-based clustering
# eps: maximum distance between two points to be neighbors
# min_samples: minimum points to form dense region
# Finds arbitrary shaped clusters, handles outliers

X, _ = make_moons(n_samples=200, noise=0.05, random_state=42)

# DBSCAN
dbscan = DBSCAN(eps=0.3, min_samples=5)
labels = dbscan.fit_predict(X)

print(f"Number of clusters: {len(set(labels)) - (1 if -1 in labels else 0)}")
print(f"Noise points: {np.sum(labels == -1)}")

# eps parameter is crucial
# Too small: many points labeled as noise
# Too large: everything becomes one cluster

# Comparison with K-means
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2, random_state=42, n_init='auto')
kmeans_labels = kmeans.fit_predict(X)

# DBSCAN advantages:
# - No need to specify K
# - Finds arbitrary shapes (moons, spirals)
# - Handles outliers
# - Robust to noise
```

### Q387: Explain the concept of p-value and statistical significance
**Answer:**
```python
import numpy as np
from scipy import stats

# p-value: probability of observing results as extreme as actual
# assuming null hypothesis is true
# Low p-value (< 0.05) suggests rejecting null hypothesis

# Example: coin fairness test
np.random.seed(42)

# Fair coin: p(heads) = 0.5
# Observing 8 heads in 10 flips
n_flips = 10
n_heads = 8

# Binomial test
p_value = stats.binomtest(n_heads, n_flips, p=0.5).pvalue
print(f"Observed {n_heads} heads in {n_flips} flips")
print(f"p-value: {p_value:.4f}")

# Common misinterpretations:
# - p-value is NOT probability that null hypothesis is true
# - p-value is NOT probability that alternative hypothesis is false
# - p-value depends on sample size (large N = small p even for tiny effects)

# Effect size matters too!
def cohens_d(x, y):
    return (np.mean(x) - np.mean(y)) / np.sqrt(
        (np.var(x) + np.var(y)) / 2
    )

group1 = np.random.normal(100, 15, 1000)
group2 = np.random.nelian(102, 15, 1000)

t_stat, p_val = stats.ttest_ind(group1, group2)
d = cohens_d(group1, group2)
print(f"p-value: {p_val:.4f}, Cohen's d: {d:.3f}")
```

### Q388: How do you handle text preprocessing for NLP?
**Answer:**
```python
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

text = "The cats were running quickly through the city's parks!"

# 1. Lowercase
text = text.lower()

# 2. Remove punctuation/numbers
text = re.sub(r'[^\w\s]', '', text)
text = re.sub(r'\d+', '', text)

# 3. Tokenization
tokens = text.split()
# or: nltk.word_tokenize(text)

# 4. Remove stopwords
stop_words = set(stopwords.words('english'))
tokens = [t for t in tokens if t not in stop_words]

# 5. Stemming (cruder, faster)
stemmer = PorterStemmer()
stemmed = [stemmer.stem(t) for t in tokens]
print(f"Stemmed: {stemmed}")
# ['cat', 'were', 'run', 'quickli', 'citie', 'park']

# 6. Lemmatization (more accurate, needs POS tagging)
lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(t, pos='v') for t in tokens]
print(f"Lemmatized: {lemmatized}")
# ['cat', 'running', 'quickly', 'city', 'park']

# 7. N-grams
from nltk import ngrams
bigrams = list(ngrams(tokens, 2))
print(f"Bigrams: {bigrams}")
```

### Q389: What is the difference between random forest and gradient boosting?
**Answer:**
```python
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import cross_val_score
import numpy as np

X, y = make_regression(n_samples=500, n_features=10, noise=10, random_state=42)

# Random Forest
rf = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_leaf=5,
    random_state=42
)

# Gradient Boosting
gb = GradientBoostingRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    min_samples_leaf=5,
    random_state=42
)

rf_scores = cross_val_score(rf, X, y, cv=5, scoring='r2')
gb_scores = cross_val_score(gb, X, y, cv=5, scoring='r2')

print(f"RF R2: {rf_scores.mean():.3f} (+/- {rf_scores.std():.3f})")
print(f"GB R2: {gb_scores.mean():.3f} (+/- {gb_scores.std():.3f})")

# Key differences:
# RF: parallel trees, bagging, reduces variance
# GB: sequential trees, boosting, reduces bias
# RF: less hyperparameter tuning needed
# GB: more prone to overfitting (lower learning rate helps)
# RF: generally good out-of-box
# GB: better with proper tuning
```

### Q390: How does the decision tree split criteria work?
**Answer:**
```python
from sklearn.tree import DecisionTreeClassifier
import numpy as np

# Decision tree splits to maximize purity
# Criteria: Gini impurity or Entropy (information gain)

# Gini: 1 - sum(p_i^2)
# Entropy: -sum(p_i * log2(p_i))

np.random.seed(42)
X = np.random.randn(100, 2)
y = (X[:, 0] + X[:, 1] > 0).astype(int)

# Gini (default)
tree_gini = DecisionTreeClassifier(criterion='gini', max_depth=3)
tree_gini.fit(X, y)

# Entropy
tree_entropy = DecisionTreeClassifier(criterion='entropy', max_depth=3)
tree_entropy.fit(X, y)

print(f"Gini tree depth: {tree_gini.tree_.node_count}")
print(f"Entropy tree depth: {tree_entropy.tree_.node_count}")

# Tree structure
print("
Decision tree (first splits):")
n_nodes = tree_gini.tree_.node_count
children_left = tree_gini.tree_.children_left
children_right = tree_gini.tree_.children_right
feature = tree_gini.tree_.feature
threshold = tree_gini.tree_.threshold

for i in range(min(5, n_nodes)):
    if children_left[i] != -1:  # Not a leaf
        print(f"Node {i}: X[{feature[i]}] <= {threshold[i]:.3f}")
```

### Q391: What is the difference between precision and recall?
**Answer:**
```python
from sklearn.metrics import precision_recall_curve, average_precision_score
import numpy as np

# Precision: of predicted positives, how many are actually positive
# TP / (TP + FP) - "accuracy of positive predictions"

# Recall: of actual positives, how many did we catch
# TP / (TP + FN) - "coverage of actual positives"

y_true = np.array([1, 1, 0, 0, 1, 1, 0, 0, 1, 0])
y_scores = np.array([0.9, 0.8, 0.3, 0.1, 0.7, 0.6, 0.4, 0.2, 0.5, 0.35])

# Precision and recall at different thresholds
thresholds = [0.3, 0.5, 0.7]
for t in thresholds:
    y_pred = (y_scores >= t).astype(int)
    tp = np.sum((y_pred == 1) & (y_true == 1))
    fp = np.sum((y_pred == 1) & (y_true == 0))
    fn = np.sum((y_pred == 0) & (y_true == 1))
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    print(f"Threshold {t:.1f}: precision={precision:.2f}, recall={recall:.2f}")

# Tradeoff: higher threshold -> higher precision, lower recall
# Lower threshold -> lower precision, higher recall

# Precision-recall curve
precisions, recalls, _ = precision_recall_curve(y_true, y_scores)
print(f"AP: {average_precision_score(y_true, y_scores):.3f}")
```

### Q392: Explain how to detect multicollinearity
**Answer:**
```python
import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Multicollinearity: when predictors are highly correlated
# Problems: unstable coefficients, inflated standard errors

np.random.seed(42)
n = 100
x1 = np.random.normal(0, 1, n)
x2 = x1 * 2 + np.random.normal(0, 0.5, n)  # Correlated with x1
x3 = np.random.normal(0, 1, n)              # Independent
x4 = x1 * 0.5 + x2 * 0.3 + np.random.normal(0, 0.2, n)  # Highly correlated

df = pd.DataFrame({'x1': x1, 'x2': x2, 'x3': x3, 'x4': x4})

# Correlation matrix
print("Correlation matrix:")
print(df.corr())

# Variance Inflation Factor (VIF > 5-10 indicates multicollinearity)
def calculate_vif(df):
    vif_data = pd.DataFrame()
    vif_data['feature'] = df.columns
    vif_data['VIF'] = [
        variance_inflation_factor(df.values, i)
        for i in range(df.shape[1])
    ]
    return vif_data

print("
VIF scores:")
print(calculate_vif(df))

# Solutions:
# 1. Remove highly correlated features
# 2. PCA / dimensionality reduction
# 3. Ridge regression (L2 regularization)
# 4. Combine correlated features
```

### Q393: What is the difference between regression and classification metrics?
**Answer:**
```python
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score
)
import numpy as np

# Regression metrics (continuous targets)
y_true_reg = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y_pred_reg = np.array([1.1, 1.9, 3.2, 3.8, 5.1])

mse = mean_squared_error(y_true_reg, y_pred_reg)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_true_reg, y_pred_reg)
r2 = r2_score(y_true_reg, y_pred_reg)
mape = np.mean(np.abs((y_true_reg - y_pred_reg) / y_true_reg)) * 100

print(f"Regression:")
print(f"  MSE: {mse:.4f}")
print(f"  RMSE: {rmse:.4f}")
print(f"  MAE: {mae:.4f}")
print(f"  R2: {r2:.4f}")
print(f"  MAPE: {mape:.2f}%")

# Classification metrics (discrete labels)
y_true_cls = np.array([0, 1, 0, 1, 0, 1, 0, 1])
y_pred_cls = np.array([0, 1, 0, 0, 0, 1, 1, 1])

accuracy = accuracy_score(y_true_cls, y_pred_cls)
precision = precision_score(y_true_cls, y_pred_cls)
recall = recall_score(y_true_cls, y_pred_cls)
f1 = f1_score(y_true_cls, y_pred_cls)
tn, fp, fn, tp = np.array([[3, 1], [1, 3]]).ravel()
specificity = tn / (tn + fp)

print(f"
Classification:")
print(f"  Accuracy: {accuracy:.3f}")
print(f"  Precision: {precision:.3f}")
print(f"  Recall: {recall:.3f}")
print(f"  F1: {f1:.3f}")
print(f"  Specificity: {specificity:.3f}")
```

### Q394: How does cross-validation help prevent overfitting?
**Answer:**
```python
from sklearn.model_selection import (
    cross_val_score, KFold, StratifiedKFold,
    LeaveOneOut, TimeSeriesSplit
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

model = RandomForestClassifier(n_estimators=50, random_state=42)

# K-Fold CV (default k=5)
kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kf, scoring='accuracy')
print(f"K-Fold: {scores.mean():.3f} (+/- {scores.std():.3f})")

# Stratified K-Fold (preserves class proportions)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores_s = cross_val_score(model, X, y, cv=skf, scoring='accuracy')

# Leave-One-Out (expensive, good for small datasets)
loo = LeaveOneOut()
scores_loo = cross_val_score(model, X[:50], y[:50], cv=loo)
print(f"LOO: {scores_loo.mean():.3f}")

# Time Series CV
tscv = TimeSeriesSplit(n_splits=5)

# CV detects overfitting: high train score, low CV score
from sklearn.tree import DecisionTreeClassifier
overfit_tree = DecisionTreeClassifier(max_depth=None)
train_score = overfit_tree.fit(X, y).score(X, y)
cv_score = cross_val_score(overfit_tree, X, y, cv=5).mean()
print(f"Overfit tree - Train: {train_score:.3f}, CV: {cv_score:.3f}")
```

### Q395: Explain the concept of regularization paths
**Answer:**
```python
from sklearn.linear_model import Lasso, LassoCV
import numpy as np

np.random.seed(42)
n, p = 100, 20
X = np.random.randn(n, p)
y = X[:, 0] * 3 + X[:, 1] * 0.5 + np.random.randn(n) * 0.5

# As regularization (alpha) increases:
# - Coefficients shrink toward zero
# - Lasso: coefficients become exactly zero (feature selection)
# - Ridge: coefficients approach but never reach zero

alphas = np.logspace(-3, 1, 100)
lasso = Lasso(max_iter=10000)
coefs = []

for alpha in alphas:
    lasso.set_params(alpha=alpha)
    lasso.fit(X, y)
    coefs.append(lasso.coef_.copy())

coefs = np.array(coefs)
for i in range(3):  # First 3 features
    print(f"Feature {i}: alpha=0.001 coef={coefs[0, i]:.2f}, "
          f"alpha=1 coef={coefs[-1, i]:.2f}, "
          f"alpha=10 coef={coefs[-1, i]:.2f}")

# Cross-validated alpha selection
lasso_cv = LassoCV(alphas=alphas, cv=5, max_iter=10000)
lasso_cv.fit(X, y)
print(f"
Optimal alpha: {lasso_cv.alpha_:.4f}")
print(f"Selected features: {np.sum(lasso_cv.coef_ != 0)}")
```

### Q396: How do you handle different data types in a dataset?
**Answer:**
```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Sample mixed dataset
df = pd.DataFrame({
    'age': [25, 30, 35, 40],         # Numerical
    'gender': ['M', 'F', 'F', 'M'],   # Categorical
    'income': [50000, 60000, None, 80000],  # Numerical with missing
    'date': ['2026-01-01', '2026-02-01', '2026-03-01', '2026-04-01'],  # DateTime
    'text': ['good', 'bad', 'medium', 'good']  # Text
})

# Preprocessing pipelines
numerical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('encoder', OneHotEncoder(drop='first', sparse_output=False))
])

datetime_pipeline = Pipeline([
    ('extractor', FunctionTransformer(
        lambda x: pd.to_datetime(x).astype(np.int64) // 10**9,
        validate=False
    )),
    ('scaler', StandardScaler())
])

# ColumnTransformer
preprocessor = ColumnTransformer([
    ('num', numerical_pipeline, ['age', 'income']),
    ('cat', categorical_pipeline, ['gender']),
    ('date', datetime_pipeline, ['date'])
])

# X_processed = preprocessor.fit_transform(df)
# print(f"Shape after preprocessing: {X_processed.shape}")
```

### Q397: What is the difference between bagging, boosting, and stacking?
**Answer:**
```python
from sklearn.ensemble import (
    BaggingClassifier, AdaBoostClassifier, StackingClassifier
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

# Bagging: parallel training on bootstrap samples
bagging = BaggingClassifier(
    estimator=DecisionTreeClassifier(),
    n_estimators=50,
    max_samples=0.8,
    random_state=42
)

# Boosting: sequential training, correcting errors
boosting = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1),  # Stump
    n_estimators=50,
    learning_rate=1.0,
    random_state=42
)

# Stacking: different models, meta-learner
base_models = [
    ('rf', RandomForestClassifier(n_estimators=50)),
    ('svm', SVC(probability=True)),
    ('lr', LogisticRegression())
]
stacking = StackingClassifier(
    estimators=base_models,
    final_estimator=LogisticRegression(),
    cv=5
)

# Results
for name, model in [('Bagging', bagging), ('Boosting', boosting), ('Stacking', stacking)]:
    scores = cross_val_score(model, X, y, cv=5)
    print(f"{name}: {scores.mean():.3f} (+/- {scores.std():.3f})")
```

### Q398: How does the SVM kernel trick work?
**Answer:**
```python
from sklearn.svm import SVC
import numpy as np

# Kernel trick: project data to higher dimension without explicit computation
# Common kernels: linear, polynomial, RBF, sigmoid

np.random.seed(42)
# Non-linearly separable data (concentric circles)
n = 100
theta = np.random.uniform(0, 2*np.pi, n)
r = np.random.choice([1, 3], n)
X = np.column_stack([r * np.cos(theta), r * np.sin(theta)])
y = (r == 3).astype(int)

# Different kernels
kernels = ['linear', 'rbf', 'poly']
for kernel in kernels:
    svm = SVC(kernel=kernel, gamma='auto')
    svm.fit(X, y)
    score = svm.score(X, y)
    print(f"{kernel}: accuracy = {score:.3f}, support vectors = {svm.n_support_}")

# RBF kernel maps to infinite-dimensional space
# gamma controls RBF width (how far a point influences)
# Small gamma: broad influence (simpler boundary)
# Large gamma: narrow influence (complex boundary, overfitting)

# Manual RBF kernel computation
def rbf_kernel(x1, x2, gamma=1.0):
    return np.exp(-gamma * np.linalg.norm(x1 - x2) ** 2)

# Precomputed kernel matrix
K = np.zeros((len(X), len(X)))
for i in range(len(X)):
    for j in range(len(X)):
        K[i, j] = rbf_kernel(X[i], X[j], gamma=0.5)
svm_precomputed = SVC(kernel='precomputed')
svm_precomputed.fit(K, y)
```

### Q399: Explain A/B testing statistical methodology
**Answer:**
```python
import numpy as np
from scipy import stats

np.random.seed(42)
# Simulate A/B test
# Control: current design, Treatment: new design
n_per_group = 1000

# Conversion rates
control_rate = 0.10  # 10% conversion
treatment_rate = 0.12  # 12% conversion (hoped for improvement)

control = np.random.binomial(1, control_rate, n_per_group)
treatment = np.random.binomial(1, treatment_rate, n_per_group)

# Observed rates
print(f"Control conversion: {control.mean():.3f}")
print(f"Treatment conversion: {treatment.mean():.3f}")

# 1. Two-proportion z-test
from statsmodels.stats.proportion import proportions_ztest
counts = np.array([control.sum(), treatment.sum()])
nobs = np.array([n_per_group, n_per_group])
z_stat, p_value = proportions_ztest(counts, nobs)
print(f"Z-test: z={z_stat:.3f}, p={p_value:.4f}")

# 2. Chi-square test
from scipy.stats import chi2_contingency
contingency = pd.crosstab(
    pd.Series(control, name='control'),
    pd.Series(treatment, name='treatment')
)
# chi2, p_val, dof, expected = chi2_contingency(contingency)

# 3. Confidence interval
from statsmodels.stats.proportion import proportion_confint
ci_control = proportion_confint(control.sum(), n_per_group, alpha=0.05)
ci_treatment = proportion_confint(treatment.sum(), n_per_group, alpha=0.05)
print(f"Control 95% CI: [{ci_control[0]:.3f}, {ci_control[1]:.3f}]")
print(f"Treatment 95% CI: [{ci_treatment[0]:.3f}, {ci_treatment[1]:.3f}]")

# Required sample size
from statsmodels.stats.power import NormalIndPower
effect_size = (treatment_rate - control_rate) / np.sqrt(
    control_rate * (1 - control_rate)
)
power = NormalIndPower()
n_needed = power.solve_power(effect_size=effect_size, power=0.8, alpha=0.05)
print(f"Required N per group for 80% power: {n_needed:.0f}")
```

### Q400: What is the curse of dimensionality?
**Answer:**
```python
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_classification

# Curse of dimensionality: as dimensions increase,
# data becomes sparse, distance metrics break down

def analyze_dimensions(n_dims):
    np.random.seed(42)
    n_points = 100

    # Random points in n-dimensional space
    points = np.random.rand(n_points, n_dims)

    # Compute pairwise distances
    distances = []
    for i in range(n_points):
        for j in range(i + 1, n_points):
            dist = np.linalg.norm(points[i] - points[j])
            distances.append(dist)

    distances = np.array(distances)
    max_dist = distances.max()
    min_dist = distances.min()

    # Ratio: in high dimensions, max/min approaches 1
    # (all points become equally far)
    ratio = max_dist / min_dist
    avg_dist = distances.mean()
    std_dist = distances.std()

    return ratio, avg_dist, std_dist

for dims in [1, 2, 5, 10, 50, 100, 1000]:
    ratio, avg, std = analyze_dimensions(dims)
    print(f"Dimensions {dims:4d}: max/min ratio = {ratio:.3f}, "
          f"avg distance = {avg:.3f}, std = {std:.3f}")

# Impact on KNN: in high dimensions, nearest neighbor is almost as far
# as farthest neighbor, making KNN unreliable

# Solutions:
# - Dimensionality reduction (PCA, t-SNE, UMAP)
# - Feature selection
# - More data (exponentially more as dimensions increase)
```

### Q401: What is FastAPI and why use it?
**Answer:**
```python
from fastapi import FastAPI

# FastAPI: modern Python web framework for building APIs
# Key features:
# - High performance (on par with Node.js/Go)
# - Automatic OpenAPI/Swagger docs
# - Type validation via Pydantic
# - Async support
# - Dependency injection

app = FastAPI(title="My API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# Automatic features:
# - /docs -> Swagger UI
# - /redoc -> ReDoc UI
# - /openapi.json -> OpenAPI schema
```

### Q402: How do you define Pydantic models in FastAPI?
**Answer:**
```python
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, le=10000)
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)

class User(BaseModel):
    username: str = Field(..., pattern=r'^[a-zA-Z0-9_]+$', min_length=3)
    email: EmailStr
    age: int = Field(ge=0, le=150)

# Response model
from fastapi import FastAPI
app = FastAPI()

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    # FastAPI validates request body against Item schema
    # Validates response body against Item schema
    return item

# Nested models
class Order(BaseModel):
    items: List[Item]
    user: User
    total: float = Field(ge=0)

# Config
class Config:
    extra = "forbid"  # Reject unknown fields
    frozen = True     # Immutable
```

### Q403: How do you handle dependency injection in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Depends, HTTPException
from typing import Optional

app = FastAPI()

# Simple dependency
def common_params(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(params: dict = Depends(common_params)):
    return params

# Class-based dependency
class Database:
    def __init__(self, connection_string: str = "default"):
        self.conn = connection_string

    async def connect(self):
        return self.conn

def get_db():
    return Database("postgresql://localhost/mydb")

@app.get("/users/")
async def get_users(db: Database = Depends(get_db)):
    return {"db": db.connect()}

# Nested dependencies
def verify_token(x_token: str = None):
    if x_token != "secret":
        raise HTTPException(status_code=401, detail="Invalid token")
    return x_token

def get_current_user(token: str = Depends(verify_token)):
    return {"user": "admin", "token": token}

@app.get("/protected/")
async def protected(user: dict = Depends(get_current_user)):
    return user

# Yield dependencies (context managers)
async def get_session():
    session = DatabaseSession()
    try:
        yield session
    finally:
        session.close()
```

### Q404: How do FastAPI path operations and routing work?
**Answer:**
```python
from fastapi import FastAPI, Path, Query

app = FastAPI()

# Path parameters
@app.get("/items/{item_id}")
async def read_item(item_id: int = Path(..., ge=1, title="Item ID")):
    return {"item_id": item_id}

# Query parameters
@app.get("/search/")
async def search(
    q: str = Query(..., min_length=3, max_length=50),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    return {"query": q, "page": page, "size": size}

# Mixed
@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(
    user_id: int,
    item_id: int,
    detailed: bool = Query(False)
):
    return {"user_id": user_id, "item_id": item_id, "detailed": detailed}

# Multiple path operations for same path
@app.get("/products/")
async def list_products():
    return [{"id": 1, "name": "Product A"}]

@app.post("/products/")
async def create_product():
    return {"message": "Created"}

@app.put("/products/{product_id}")
async def update_product(product_id: int):
    return {"product_id": product_id, "updated": True}

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    return {"product_id": product_id, "deleted": True}
```

### Q405: How do you handle errors and exceptions in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from pydantic import BaseModel

app = FastAPI()

# HTTP exceptions
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id < 1:
        raise HTTPException(
            status_code=400,
            detail="Item ID must be >= 1",
            headers={"X-Error": "Invalid ID"}
        )
    return {"item_id": item_id}

# Custom exceptions
class NotFoundError(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": f"{exc.name} not found"}
    )

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id != 1:
        raise NotFoundError("User")
    return {"user_id": 1}

# Override default handlers
@app.exception_handler(HTTPException)
async def custom_http_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

# Validation errors
from fastapi.exceptions import RequestValidationError
@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body
        }
    )
```

### Q406: How does FastAPI handle background tasks?
**Answer:**
```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import time
import asyncio

app = FastAPI()

# Synchronous background task
def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{time.time()}: {message}\n")

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    # Task runs after response is sent
    background_tasks.add_task(write_log, f"Sent to {email}")
    return {"message": "Notification sent"}

# Multiple tasks
@app.post("/send-bulk/")
async def send_bulk(
    emails: list[str],
    background_tasks: BackgroundTasks
):
    for email in emails:
        background_tasks.add_task(write_log, f"Bulk sent to {email}")
    return {"message": f"Queued {len(emails)} notifications"}

# Async background task
async def send_email_async(email: str):
    await asyncio.sleep(1)  # Simulate email sending
    print(f"Email sent to {email}")

@app.post("/send-async/")
async def send_async(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email_async, email)
    return {"message": "Email queued"}

# Celery for heavy tasks (external worker)
# from celery import Celery
# celery = Celery("tasks", broker="redis://localhost:6379/0")
```

### Q407: How do you handle authentication in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

app = FastAPI()

# Security config
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None

class User(BaseModel):
    username: str
    email: str = None
    disabled: bool = False

# Mock user DB
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin",
        "email": "admin@example.com",
        "hashed_password": "$2b$12$...",
        "disabled": False,
    }
}

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Login endpoint
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)
    return {"username": username}
```

### Q408: How do you handle CORS in FastAPI?
**Answer:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",      # React dev server
    "http://localhost:5173",       # Vite dev server
    "https://myapp.com",           # Production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # List of allowed origins
    allow_credentials=True,        # Allow cookies
    allow_methods=["*"],           # Allow all methods
    allow_headers=["*"],           # Allow all headers
    expose_headers=["X-Custom"],   # Headers exposed to browser
    max_age=600,                   # Cache preflight response (seconds)
)

# For development (allow everything):
# allow_origins=["*"]

@app.get("/")
async def root():
    return {"message": "CORS enabled"}
```

### Q409: How do you use FastAPI with databases (SQLAlchemy)?
**Answer:**
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy model
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)

# Pydantic schema
class UserCreate(BaseModel):
    email: str
    name: str

class User(UserCreate):
    id: int
    class Config:
        from_attributes = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Q410: How does FastAPI handle file uploads?
**Answer:**
```python
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from typing import List
import shutil
import os

app = FastAPI()

# Single file upload
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Save file
    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(await file.read())
    }

# Multiple files
@app.post("/upload-multiple/")
async def upload_multiple(files: List[UploadFile] = File(...)):
    return [
        {
            "filename": f.filename,
            "content_type": f.content_type
        }
        for f in files
    ]

# File with form data
@app.post("/upload-with-metadata/")
async def upload_with_metadata(
    file: UploadFile = File(...),
    description: str = Form(...),
    tags: str = Form("")
):
    return {
        "filename": file.filename,
        "description": description,
        "tags": tags.split(","),
        "size": len(await file.read())
    }

# Streaming response
from fastapi.responses import StreamingResponse
@app.get("/download/{filename}")
async def download_file(filename: str):
    def iterfile():
        with open(f"uploads/{filename}", "rb") as f:
            yield from f
    return StreamingResponse(iterfile(), media_type="application/octet-stream")
```

### Q411: How do you handle WebSockets in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import asyncio

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} disconnected")

# Client example
# import asyncio
# import websockets
# async def test():
#     async with websockets.connect("ws://localhost:8000/ws/client1") as ws:
#         await ws.send("Hello!")
#         response = await ws.recv()
#         print(response)
```

### Q412: What are Pydantic validators and how do you use them?
**Answer:**
```python
from pydantic import BaseModel, validator, field_validator, model_validator
from typing import List

class UserModel(BaseModel):
    name: str
    username: str
    password1: str
    password2: str
    age: int

    # Field validators (v2 style)
    @field_validator('name')
    @classmethod
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('Must contain a space')
        return v.title()

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Must be alphanumeric')
        return v

    @field_validator('age')
    @classmethod
    def age_must_be_valid(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Invalid age')
        return v

    # Model validators (cross-field)
    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password1 != self.password2:
            raise ValueError('Passwords do not match')
        return self

# Pre-processing validators
class TrimmedModel(BaseModel):
    text: str

    @field_validator('text', mode='before')
    @classmethod
    def trim_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

# Multiple validators for same field
class StrictString(BaseModel):
    value: str

    @field_validator('value')
    @classmethod
    def check_length(cls, v):
        if len(v) < 3:
            raise ValueError('Too short')
        return v

    @field_validator('value')
    @classmethod
    def check_content(cls, v):
        if 'bad' in v.lower():
            raise ValueError('Contains bad content')
        return v
```

### Q413: How does FastAPI handle testing?
**Answer:**
```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

app = FastAPI()

@app.get("/")
async def read_root():
    return {"hello": "world"}

@app.post("/items/")
async def create_item(name: str, price: float):
    return {"name": name, "price": price, "id": 1}

# Tests
client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 9.99}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 9.99

def test_not_found():
    response = client.get("/nonexistent")
    assert response.status_code == 404

# Async tests
@pytest.mark.asyncio
async def test_async_endpoint():
    from httpx import AsyncClient
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200

# Fixture-based testing
@pytest.fixture
def client():
    return TestClient(app)

def test_with_fixture(client):
    response = client.get("/")
    assert response.status_code == 200
```

### Q414: How do you create middleware in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
import logging

app = FastAPI()

# Basic middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Logger middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("api")
    response = await call_next(request)
    logger.info(
        f"{request.method} {request.url.path} -> {response.status_code}"
    )
    return response

# Rate limiting middleware
class RateLimitMiddleware:
    def __init__(self, app, requests_per_minute=60):
        self.app = app
        self.requests = {}
        self.limit = requests_per_minute

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        client_ip = scope["client"][0]
        now = time.time()

        # Clean old entries
        self.requests[client_ip] = [
            t for t in self.requests.get(client_ip, [])
            if now - t < 60
        ]

        if len(self.requests.get(client_ip, [])) >= self.limit:
            response = JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"}
            )
            # Send response directly
            await response(scope, receive, send)
            return

        self.requests.setdefault(client_ip, []).append(now)
        await self.app(scope, receive, send)

# app.add_middleware(RateLimitMiddleware, requests_per_minute=30)
```

### Q415: How does Pydantic's Config class work?
**Answer:**
```python
from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

# Pydantic v2 uses ConfigDict
class Product(BaseModel):
    model_config = ConfigDict(
        frozen=True,           # Immutable
        extra="forbid",        # Reject extra fields
        validate_assignment=True,  # Validate on attribute set
        str_strip_whitespace=True, # Strip whitespace
        str_min_length=1,      # Minimum string length
        validate_default=True, # Validate default values
        arbitrary_types_allowed=True, # Allow custom types
    )

    id: int
    name: str
    price: float

# Or using model_config
class User(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str
    email: str

# Alias support
class ModelWithAlias(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,  # Allow both alias and name
        alias_generator=lambda s: s.upper()  # Auto-generate aliases
    )

    first_name: str
    last_name: str

data = {"FIRST_NAME": "John", "LAST_NAME": "Doe"}
m = ModelWithAlias(**data)
print(m.first_name)  # John

# Immutability
# p = Product(id=1, name="Laptop", price=999.99)
# p.name = "Desktop"  # TypeError if frozen=True
```

### Q416: How do you handle pagination in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Generic, TypeVar, Optional

app = FastAPI()

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    @classmethod
    def create(cls, items: List[T], total: int, page: int, size: int):
        pages = (total + size - 1) // size
        return cls(items=items, total=total, page=page, size=size, pages=pages)

class Item(BaseModel):
    id: int
    name: str
    price: float

# Mock data
all_items = [Item(id=i, name=f"Item {i}", price=10.0 * i) for i in range(1, 101)]

@app.get("/items/")
async def get_items(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page")
) -> PaginatedResponse[Item]:
    start = (page - 1) * size
    end = start + size
    items = all_items[start:end]
    total = len(all_items)

    return PaginatedResponse.create(
        items=items, total=total, page=page, size=size
    )

# Cursor-based pagination
@app.get("/items-cursor/")
async def get_items_cursor(
    cursor: Optional[int] = Query(None, description="Last seen ID"),
    limit: int = Query(10, le=100)
):
    if cursor:
        items = [i for i in all_items if i.id > cursor][:limit]
    else:
        items = all_items[:limit]

    next_cursor = items[-1].id if len(items) == limit else None
    return {
        "items": items,
        "next_cursor": next_cursor,
        "has_more": next_cursor is not None
    }
```

### Q417: What is the difference between Pydantic v1 and v2?
**Answer:**
```python
# Pydantic v2 is a complete rewrite with significant improvements:

# 1. Performance (5-50x faster validation)
# Uses Rust-based pydantic-core

# 2. Config changes
# v1: class Config:
# v2: model_config = ConfigDict(...)

# 3. Validator changes
# v1: @validator('field')
# v2: @field_validator('field')

# 4. Root validators
# v1: @root_validator
# v2: @model_validator(mode='before') or @model_validator(mode='after')

# 5. Type conversion
# v1: uses validator for conversion
# v2: uses @field_validator(mode='before')

# 6. Generic models
# v1: class Response(GenericModel, Generic[T]):
# v2: class Response(BaseModel, Generic[T]):

# 7. model_dump() vs dict()
# v1: obj.dict()
# v2: obj.model_dump()

# 8. model_validate() vs parse_obj()
# v1: obj = Model.parse_obj(data)
# v2: obj = Model.model_validate(data)

# Example comparison:
from pydantic import BaseModel, ConfigDict, field_validator

# v2 style
class UserV2(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    age: int

    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v

# In v1, this would be:
# class UserV1(BaseModel):
#     name: str
#     age: int
#
#     @validator('age')
#     def validate_age(cls, v):
#         if v < 0:
#             raise ValueError(...)
#         return v
#
#     class Config:
#         extra = "forbid"
```

### Q418: How do you use FastAPI with async database sessions?
**Answer:**
```python
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

app = FastAPI()

# Async dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("SELECT * FROM users WHERE id = :id"),
        {"id": user_id}
    )
    user = result.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}

# With SQLAlchemy 2.0 async
from sqlalchemy import select
from sqlalchemy.orm import selectinload

@app.get("/users/{user_id}/orders")
async def get_user_orders(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(User).options(
        selectinload(User.orders)
    ).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404)
    return user
```

### Q419: How do you implement rate limiting in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import time
from collections import defaultdict

app = FastAPI()

# In-memory rate limiter
class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)

    def check(self, key: str, max_requests: int, window: int) -> bool:
        now = time.time()
        # Remove expired entries
        self.requests[key] = [
            t for t in self.requests[key]
            if now - t < window
        ]
        if len(self.requests[key]) >= max_requests:
            return False
        self.requests[key].append(now)
        return True

rate_limiter = RateLimiter()

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Rate limit by IP
    client_ip = request.client.host

    if not rate_limiter.check(client_ip, max_requests=60, window=60):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"}
        )

    response = await call_next(request)
    return response

# Different limits for different endpoints
LIMITS = {
    "/login": (5, 60),      # 5 per minute
    "/api/": (60, 60),      # 60 per minute
    "/public/": (1000, 60),  # 1000 per minute
}

# Using slowapi library
# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address
# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter
# app.add_exception_handler(429, _rate_limit_exceeded_handler)
```

### Q420: How do you handle environment configuration in FastAPI?
**Answer:**
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # App
    APP_NAME: str = "FastAPI App"
    DEBUG: bool = False
    VERSION: str = "1.0.0"

    # Database
    DATABASE_URL: str = "sqlite:///./test.db"
    DATABASE_POOL_SIZE: int = 5

    # Auth
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis
    REDIS_URL: Optional[str] = None

    # External APIs
    OPENAI_API_KEY: Optional[str] = None

    class Config:
        env_prefix = ""  # No prefix

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Usage in app
from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "debug": settings.DEBUG
    }

# .env file example:
# APP_NAME=MyAPI
# DEBUG=true
# DATABASE_URL=postgresql://user:pass@localhost/db
# SECRET_KEY=super-secret-key
```
### Q421: How do you use FastAPI with WebSocket authentication?
**Answer:**
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import jwt

app = FastAPI()

async def verify_token(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001)
        return None
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return payload.get("sub")
    except jwt.PyJWTError:
        await websocket.close(code=4001)
        return None

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    user = await verify_token(websocket)
    if not user:
        return
    await websocket.accept()
    await websocket.send_text(f"Authenticated as {user}")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print(f"User {user} disconnected")
```

### Q422: How do you create custom response types in FastAPI?
**Answer:**
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse, FileResponse, StreamingResponse
import io, csv

app = FastAPI()

@app.get("/custom-json/")
async def custom_json():
    return JSONResponse(
        content={"message": "Hello"},
        status_code=200,
        headers={"X-Custom": "value"}
    )

@app.get("/text/", response_class=PlainTextResponse)
async def text():
    return "Hello, World!"

@app.get("/html/", response_class=HTMLResponse)
async def html():
    return "<h1>Hello</h1><p>World</p>"

@app.get("/csv/")
async def csv_endpoint():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows([["Name", "Age"], ["Alice", 30], ["Bob", 25]])
    return Response(content=output.getvalue(), media_type="text/csv")

@app.get("/stream/")
async def stream():
    def generate():
        for i in range(1000):
            yield f"line {i}\n"
    return StreamingResponse(generate(), media_type="text/plain")
```

### Q423: How do you handle database migrations with FastAPI?
**Answer:**
```python
# Using Alembic with FastAPI
# Install: pip install alembic
# Initialize: alembic init alembic
# Configure alembic/env.py to use your Base metadata

# from alembic import context
# from app.models import Base
# from app.database import engine
# target_metadata = Base.metadata

# Commands:
# alembic revision --autogenerate -m "create users table"
# alembic upgrade head        # Apply all pending
# alembic downgrade -1         # Rollback one
# alembic current              # Show current version

# FastAPI startup event (dev only - use Alembic in prod)
from fastapi import FastAPI
from app.database import engine
from app.models import Base

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

### Q424: What is the difference between Response and JSONResponse?
**Answer:**
```python
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, ORJSONResponse

app = FastAPI()

# Response: base class, manual serialization
@app.get("/raw/")
async def raw_response():
    return Response(content='{"message": "hello"}', media_type="application/json")

# JSONResponse: json.dumps (stdlib), datetime/UUID serialization built-in
@app.get("/json/")
async def json_response():
    return JSONResponse({"message": "hello"})

# ORJSONResponse: orjson (3-5x faster), needs pip install orjson
# @app.get("/orjson/", response_class=ORJSONResponse)
# async def orjson_response():
#     return {"message": "hello"}

# Default response_class can be set per route or globally
@app.get("/default/")
async def default_response():
    return {"message": "hello"}  # Auto-serialized to JSONResponse
```

### Q425: How do you implement caching in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Response
from functools import lru_cache
import json
import hashlib

app = FastAPI()

# 1. In-memory function cache
@lru_cache(maxsize=128)
def expensive_computation(n: int):
    return sum(i * i for i in range(n))

@app.get("/compute/{n}")
async def compute(n: int):
    return {"result": expensive_computation(n)}

# 2. HTTP caching headers
@app.get("/static/")
async def static_data(response: Response):
    response.headers["Cache-Control"] = "public, max-age=3600"
    return {"data": "cacheable for 1 hour"}

# 3. ETag caching
@app.get("/etag/")
async def etag_endpoint(response: Response):
    data = {"version": 2, "message": "Hello"}
    etag = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
    response.headers["ETag"] = etag
    return data

# 4. Redis cache (production)
# import aioredis
# redis = aioredis.from_url("redis://localhost:6379")
#
# async def get_or_cache(key: str, ttl: int = 300):
#     cached = await redis.get(key)
#     if cached:
#         return json.loads(cached)
#     data = await fetch_from_db(key)
#     await redis.setex(key, ttl, json.dumps(data))
#     return data
```

### Q426: How do you handle long-running tasks in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, BackgroundTasks
from celery import Celery
import asyncio, time

app = FastAPI()

# Option 1: BackgroundTasks (simple, same process)
@app.post("/send-email/")
async def send_email(email: str, background_tasks: BackgroundTasks):
    def send(email):
        time.sleep(5)
        print(f"Email sent to {email}")
    background_tasks.add_task(send, email)
    return {"message": "Email queued"}

# Option 2: Celery (distributed)
# celery_app = Celery("tasks", broker="redis://localhost:6379/0")
# @celery_app.task
# def process_data(data_id: int):
#     time.sleep(10)
#     return {"status": "done"}
#
# @app.post("/process/{data_id}")
# async def start_processing(data_id: int):
#     task = process_data.delay(data_id)
#     return {"task_id": task.id, "status": "queued"}
#
# @app.get("/status/{task_id}")
# async def get_status(task_id: str):
#     task = process_data.AsyncResult(task_id)
#     if task.ready():
#         return {"status": "completed", "result": task.result}
#     return {"status": "processing"}

# Option 3: asyncio background task
@app.post("/async-task/")
async def async_task(data: dict):
    async def long_task():
        await asyncio.sleep(10)
        print(f"Processed: {data}")
    asyncio.create_task(long_task())
    return {"message": "Task started"}
```

### Q427: How do you implement logging in FastAPI?
**Answer:**
```python
import logging, sys
from fastapi import FastAPI, Request
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    log.info(f"Request {request_id}: {request.method} {request.url.path}")
    response = await call_next(request)
    log.info(f"Response {request_id}: {response.status_code}")
    response.headers["X-Request-ID"] = request_id
    return response

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    log.info(f"Fetching user {user_id}")
    try:
        user = {"id": user_id, "name": "Alice"}
        return user
    except Exception as e:
        log.error(f"Error: {e}")
        raise

# Alternative: loguru
# from loguru import logger
# logger.add("app.log", rotation="500 MB")
```

### Q428: How does FastAPI handle response serialization?
**Answer:**
```python
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    price: Decimal
    created_at: datetime
    tags: list[str] = []

@app.get("/product/{product_id}", response_model=Product)
async def get_product(product_id: int):
    return Product(
        id=product_id,
        name="Widget",
        price=Decimal("19.99"),
        created_at=datetime.now(),
        tags=["new", "sale"]
    )

# model_dump(mode="json") converts Decimal, datetime, UUID automatically
@app.get("/product/{product_id}/dump")
async def get_product_dump(product_id: int):
    product = Product(id=product_id, name="Widget", price=Decimal("19.99"), created_at=datetime.now())
    return product.model_dump(mode="json")

# Response model ensures type safety and automatic documentation
# Use response_model_exclude_unset for partial updates
# Use response_model_include/exclude for field filtering
```

### Q429: How do you create WebSocket rooms in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List

app = FastAPI()

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, ws: WebSocket, room: str):
        await ws.accept()
        if room not in self.rooms:
            self.rooms[room] = []
        self.rooms[room].append(ws)
        await self.broadcast(room, {"type": "system", "message": "User joined"})

    def disconnect(self, ws: WebSocket, room: str):
        if room in self.rooms:
            self.rooms[room].remove(ws)
            if not self.rooms[room]:
                del self.rooms[room]

    async def broadcast(self, room: str, message: dict):
        if room in self.rooms:
            for ws in self.rooms[room]:
                await ws.send_json(message)

manager = RoomManager()

@app.websocket("/ws/{room}")
async def websocket_endpoint(ws: WebSocket, room: str):
    await manager.connect(ws, room)
    try:
        while True:
            data = await ws.receive_json()
            await manager.broadcast(room, {
                "type": "message",
                "user": data.get("user", "anonymous"),
                "content": data.get("content", ""),
                "room": room
            })
    except WebSocketDisconnect:
        manager.disconnect(ws, room)
        await manager.broadcast(room, {"type": "system", "message": "User left"})
```

### Q430: How do you use FastAPI lifespan events?
**Answer:**
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
import aioredis

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    app.state.redis = await aioredis.from_url("redis://localhost:6379")
    app.state.db = create_async_engine("postgresql+asyncpg://localhost/db")
    yield
    # Shutdown
    print("Shutting down...")
    await app.state.redis.close()
    await app.state.db.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health():
    return {
        "redis": "connected" if app.state.redis else "disconnected",
        "db": "connected" if app.state.db else "disconnected"
    }

# Alternative (deprecated in FastAPI 2.0+):
# @app.on_event("startup")
# async def startup():
#     await init_db()
#
# @app.on_event("shutdown")
# async def shutdown():
#     await close_db()
```

### Q431: How do you handle API versioning in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, APIRouter

# Option 1: URL path versioning
app_v1 = FastAPI(title="API v1")
app_v2 = FastAPI(title="API v2")

@app_v1.get("/items/")
async def list_items_v1():
    return [{"name": "Item", "price": 10.0}]

@app_v2.get("/items/")
async def list_items_v2():
    return [{"name": "Item", "price": 10.0, "currency": "USD"}]

main_app = FastAPI()
main_app.mount("/v1", app_v1)
main_app.mount("/v2", app_v2)

# Option 2: Header versioning
router = APIRouter()

@router.get("/items/")
async def get_items(accept_version: str = Header("v1")):
    if accept_version == "v1":
        return {"version": "v1", "items": []}
    elif accept_version == "v2":
        return {"version": "v2", "items": [], "metadata": {}}
    raise HTTPException(status_code=400, detail="Unsupported version")

# Option 3: Query parameter versioning
@app.get("/items/")
async def get_items(version: str = "v1"):
    return {"version": version, "data": "..."}
```

### Q432: What are Pydantic discriminated unions?
**Answer:**
```python
from typing import Literal, Union, Annotated
from pydantic import BaseModel, Field

class Cat(BaseModel):
    pet_type: Literal["cat"]
    meows: bool

class Dog(BaseModel):
    pet_type: Literal["dog"]
    barks: bool

class Lizard(BaseModel):
    pet_type: Literal["lizard"]
    scales: bool

# Without discriminator
class Animal(BaseModel):
    pet: Union[Cat, Dog, Lizard]

animal = Animal.model_validate({"pet": {"pet_type": "cat", "meows": True}})
print(type(animal.pet))  # Cat

# With discriminator (exact match enforcement)
class Animal2(BaseModel):
    pet: Annotated[Union[Cat, Dog, Lizard], Field(discriminator="pet_type")]

animal2 = Animal2.model_validate({"pet": {"pet_type": "dog", "barks": True}})
print(type(animal2.pet))  # Dog

# Error on unknown discriminator
# Animal2.model_validate({"pet": {"pet_type": "fish", "swims": True}})
# -> ValueError
```

### Q433: How do you implement health checks in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Response
from datetime import datetime
import json, os

app = FastAPI()

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/health/detailed")
async def detailed_health():
    checks = {
        "database": {"status": "ok", "latency_ms": 5},
        "memory": {"status": "ok", "usage_pct": 45},
        "disk": {"status": "ok", "free_gb": 50}
    }
    all_healthy = all(c["status"] == "ok" for c in checks.values())
    return Response(
        content=json.dumps({"status": "healthy" if all_healthy else "degraded", "checks": checks}),
        status_code=200 if all_healthy else 503,
        media_type="application/json"
    )

# Kubernetes probes
@app.get("/ready")
async def ready():
    return {"status": "ready"}

@app.get("/live")
async def live():
    return {"status": "alive"}
```

### Q434: How do you use FastAPI with MongoDB?
**Answer:**
```python
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from typing import Optional, List

app = FastAPI()
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.mydb
collection = db.items

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ItemInDB(Item):
    id: str

@app.post("/items/", response_model=ItemInDB)
async def create_item(item: Item):
    result = await collection.insert_one(item.model_dump())
    created = await collection.find_one({"_id": result.inserted_id})
    return ItemInDB(id=str(created["_id"]), **created)

@app.get("/items/{item_id}", response_model=ItemInDB)
async def get_item(item_id: str):
    item = await collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404)
    return ItemInDB(id=str(item["_id"]), **item)

@app.get("/items/")
async def list_items(skip: int = 0, limit: int = 10):
    items = []
    cursor = collection.find().skip(skip).limit(limit)
    async for doc in cursor:
        items.append(ItemInDB(id=str(doc["_id"]), **doc))
    return items
```

### Q435: How do you create request validation middleware in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import re, time

app = FastAPI()

# Request size limiter
@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 10 * 1024 * 1024:
        return JSONResponse(status_code=413, content={"detail": "Request too large"})
    return await call_next(request)

# SQL injection detection
SQL_PATTERN = re.compile(r"['\";\\-]{2,}|\b(OR|AND|DROP|UNION|SELECT)\b", re.IGNORECASE)

@app.middleware("http")
async def detect_injection(request: Request, call_next):
    for key, value in request.query_params.items():
        if SQL_PATTERN.search(value):
            return JSONResponse(status_code=400, content={"detail": "Invalid parameters"})
    return await call_next(request)

# API key validation
API_KEYS = {"key1": "user1", "key2": "user2"}

@app.middleware("http")
async def validate_api_key(request: Request, call_next):
    if request.url.path in ["/health", "/docs", "/openapi.json"]:
        return await call_next(request)
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key not in API_KEYS:
        return JSONResponse(status_code=401, content={"detail": "Invalid API key"})
    request.state.user = API_KEYS[api_key]
    return await call_next(request)
```

### Q436: How does Pydantic handle JSON serialization of special types?
**Answer:**
```python
from pydantic import BaseModel
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from uuid import UUID, uuid4
from enum import Enum
import json

class Color(str, Enum):
    RED = "red"
    GREEN = "green"

class Model(BaseModel):
    id: UUID
    created_at: datetime
    event_date: date
    event_time: time
    duration: timedelta
    price: Decimal
    color: Color

m = Model(
    id=uuid4(),
    created_at=datetime.now(),
    event_date=date.today(),
    event_time=time(14, 30),
    duration=timedelta(hours=2),
    price=Decimal("19.99"),
    color=Color.RED
)

# model_dump(mode="json") handles all special types
data = m.model_dump(mode="json")
print(json.dumps(data, indent=2))

# Custom serialization via @field_serializer
from pydantic import field_serializer

class CustomModel(BaseModel):
    binary: bytes

    @field_serializer("binary")
    def serialize_binary(self, v: bytes) -> str:
        return v.hex()

c = CustomModel(binary=b"hello")
print(c.model_dump(mode="json"))  # {"binary": "68656c6c6f"}
```

### Q437: How do you implement per-user rate limiting in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer
import time
from collections import defaultdict

app = FastAPI()
security = HTTPBearer()

class RateLimiter:
    def __init__(self):
        self.history = defaultdict(list)

    def check(self, key: str, max_req: int, window: int):
        now = time.time()
        self.history[key] = [t for t in self.history[key] if now - t < window]
        if len(self.history[key]) >= max_req:
            retry = int(self.history[key][0] + window - now)
            raise HTTPException(status_code=429, detail="Rate limit exceeded",
                              headers={"Retry-After": str(retry)})
        self.history[key].append(now)

limiter = RateLimiter()

@app.get("/api/data/")
async def get_data(credentials = Depends(security)):
    limiter.check(f"user:{credentials.credentials}", max_req=10, window=60)
    return {"data": "sensitive", "user": credentials.credentials}

@app.get("/public/")
async def public_endpoint(request: Request):
    limiter.check(f"ip:{request.client.host}", max_req=100, window=60)
    return {"message": "public"}
```

### Q438: How do you use FastAPI with GraphQL?
**Answer:**
```python
# Using Strawberry GraphQL with FastAPI
# Install: pip install strawberry-graphql

# import strawberry
# from strawberry.fastapi import GraphQLRouter
#
# @strawberry.type
# class User:
#     id: int
#     name: str
#     email: str
#
# @strawberry.type
# class Query:
#     @strawberry.field
#     def user(self, id: int) -> User:
#         return User(id=id, name="Alice", email="alice@test.com")
#
#     @strawberry.field
#     def users(self) -> list[User]:
#         return [
#             User(id=1, name="Alice", email="alice@test.com"),
#             User(id=2, name="Bob", email="bob@test.com")
#         ]
#
# @strawberry.type
# class Mutation:
#     @strawberry.mutation
#     def create_user(self, name: str, email: str) -> User:
#         return User(id=3, name=name, email=email)
#
# schema = strawberry.Schema(query=Query, mutation=Mutation)
# graphql_app = GraphQLRouter(schema)
#
# app = FastAPI()
# app.include_router(graphql_app, prefix="/graphql")

# Alternative: graphene with graphql-python
# from graphene import ObjectType, String, Schema
# from fastapi import FastAPI
# from starlette.graphql import GraphQLApp
```

### Q439: How do you handle database connection pooling in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/mydb"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,           # Maintained connections
    max_overflow=20,        # Extra when pool exhausted
    pool_timeout=30,        # Wait time
    pool_pre_ping=True,     # Verify before use
    pool_recycle=3600       # Recycle after 1 hour
)

# For serverless (no pooling):
# engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

app = FastAPI()

@app.get("/items/{item_id}")
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM items WHERE id = :id"), {"id": item_id})
    item = result.fetchone()
    if not item:
        raise HTTPException(status_code=404)
    return dict(item._mapping)
```

### Q440: How do you create custom Pydantic types?
**Answer:**
```python
from pydantic import BaseModel, GetCoreSchemaHandler, AfterValidator, Field
from pydantic_core import core_schema
from typing import Annotated, Any
import re

# Option 1: Annotated with constraints
PositiveInt = Annotated[int, Field(gt=0)]
NonEmptyStr = Annotated[str, Field(min_length=1)]
HexColor = Annotated[str, AfterValidator(lambda v: v if re.match(r'^#[0-9a-fA-F]{6}$', v) else (_ for _ in ()).throw(ValueError("Invalid hex")))]

# Option 2: Custom type class
class PhoneNumber:
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        def validate(v: str) -> str:
            cleaned = v.replace("-", "").replace(" ", "")
            if not re.match(r'^\+?1?\d{10}$', cleaned):
                raise ValueError("Invalid phone number")
            return v
        return core_schema.no_info_wrap_validator_function(validate, core_schema.str_schema())

class Contact(BaseModel):
    phone: PhoneNumber
    age: PositiveInt
    name: NonEmptyStr

c = Contact(phone="+1-555-555-5555", age=25, name="Alice")
print(c.phone)  # +1-555-555-5555

# Option 3: TypeAdapter for reusable types
from pydantic import TypeAdapter
PhoneAdapter = TypeAdapter(PhoneNumber)
phone = PhoneAdapter.validate_python("+1-555-555-5555")
```

### Q441: How do you implement cursor-based pagination in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional, List
import base64, json

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str

all_items = [Item(id=i, name=f"Item {i}") for i in range(1, 1001)]

@app.get("/items/")
async def get_items(
    cursor: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100)
):
    last_id = 0
    if cursor:
        try:
            last_id = json.loads(base64.urlsafe_b64decode(cursor).decode())["last_id"]
        except:
            pass

    items = [i for i in all_items if i.id > last_id][:limit]
    next_cursor = None
    if len(items) == limit:
        next_cursor = base64.urlsafe_b64encode(json.dumps({"last_id": items[-1].id}).encode()).decode()

    return {"items": items, "next_cursor": next_cursor, "has_more": next_cursor is not None}

# Offset-based (traditional)
@app.get("/items-offset/")
async def get_items_offset(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    start = (page - 1) * limit
    items = all_items[start:start + limit]
    total = len(all_items)
    return {"items": items, "total": total, "page": page, "pages": (total + limit - 1) // limit}
```

### Q442: How does async SQLAlchemy 2.0 work with FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404)
    return {"id": user.id, "name": user.name, "email": user.email}

@app.get("/users/")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).limit(100))
    users = result.scalars().all()
    return [{"id": u.id, "name": u.name} for u in users]
```

### Q443: How do you handle file uploads with progress in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, UploadFile, File
import uuid, os

app = FastAPI()

class UploadTracker:
    def __init__(self):
        self.progress = {}

tracker = UploadTracker()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    total = 0
    chunk_size = 1024 * 1024
    os.makedirs("uploads", exist_ok=True)

    with open(f"uploads/{file.filename}", "wb") as f:
        while chunk := await file.read(chunk_size):
            f.write(chunk)
            total += len(chunk)
            tracker.progress[file_id] = total

    return {"file_id": file_id, "filename": file.filename, "size": total}

# Resumable upload
@app.post("/upload/resumable/{filename}")
async def resumable_upload(filename: str, file: UploadFile = File(...), offset: int = 0):
    os.makedirs("uploads", exist_ok=True)
    with open(f"uploads/{filename}", "ab") as f:
        f.seek(offset)
        content = await file.read()
        f.write(content)
    file_size = os.path.getsize(f"uploads/{filename}")
    return {"filename": filename, "uploaded": len(content), "total": file_size}
```

### Q444: What makes FastAPI dependency injection unique?
**Answer:**
```python
# FastAPI DI is:
# 1. Built-in (no external container needed)
# 2. Hierarchical (deps can depend on deps)
# 3. Async-first
# 4. Type-based (uses type hints)
# 5. Per-request scope

from fastapi import FastAPI, Depends, Query

app = FastAPI()

# Simple dependency
def pagination(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    return {"skip": skip, "limit": limit}

# Dependency on dependency
def get_db():
    return {"connection": "db"}

def get_service(db=Depends(get_db)):
    return {"db": db, "service": "user_service"}

@app.get("/users/")
async def get_users(
    pag: dict = Depends(pagination),
    svc: dict = Depends(get_service)
):
    return {**pag, **svc}

# Compare:
# Flask: manual request.args extraction
# Django: class-based views, no DI
# FastAPI: automatic, type-safe, testable
```

### Q445: How do you implement OpenTelemetry in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Request
import time, uuid

# Auto-instrumentation (simplest):
# pip install opentelemetry-instrumentation-fastapi
# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
# FastAPIInstrumentor.instrument_app(app)

# Manual tracing
app = FastAPI()

@app.middleware("http")
async def trace_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.time()

    response = await call_next(request)
    duration = time.time() - start

    # Add tracing headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Duration-Ms"] = str(round(duration * 1000))
    return response

# OpenTelemetry setup (production):
# from opentelemetry import trace
# from opentelemetry.exporter.otlp.proto.grpc.exporter import OTLPSpanExporter
# from opentelemetry.sdk.trace import TracerProvider, export.BatchSpanProcessor
#
# provider = TracerProvider()
# provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
# trace.set_tracer_provider(provider)
# tracer = trace.get_tracer(__name__)
#
# @app.get("/users/{user_id}")
# async def get_user(user_id: int):
#     with tracer.start_as_current_span("get_user") as span:
#         span.set_attribute("user_id", user_id)
#         return {"user_id": user_id}
```

### Q446: How do you handle graceful shutdown in FastAPI?
**Answer:**
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import asyncio, signal

class GracefulShutdown:
    def __init__(self):
        self.shutting_down = False
        self.active_requests = 0

shutdown = GracefulShutdown()

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda: setattr(shutdown, 'shutting_down', True))
    yield

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def track_requests(request: Request, call_next):
    if shutdown.shutting_down:
        return JSONResponse(status_code=503, content={"detail": "Server shutting down"})
    shutdown.active_requests += 1
    try:
        return await call_next(request)
    finally:
        shutdown.active_requests -= 1

@app.get("/slow")
async def slow():
    await asyncio.sleep(10)
    return {"message": "Done"}
```

### Q447: How do you implement response compression in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Response
from starlette.middleware.gzip import GZipMiddleware
import gzip

app = FastAPI()

# Global compression via middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Manual compression per endpoint
@app.get("/large/")
async def large_response():
    data = "x" * 10000
    compressed = gzip.compress(data.encode())
    return Response(
        content=compressed,
        media_type="text/plain",
        headers={"Content-Encoding": "gzip"}
    )

# Brotli (better compression ratio)
# pip install brotli
# import brotli
# compressed = brotli.compress(data.encode())
# headers={"Content-Encoding": "br"}

# Compression levels: gzip 1-9, brotli 0-11
# Higher level = better compression, more CPU
```

### Q448: How do you handle database transactions in FastAPI?
**Answer:**
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

app = FastAPI()

# Automatic transaction (commit on success, rollback on error)
@app.post("/transfer/")
async def transfer_money(from_id: int, to_id: int, amount: float, db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("UPDATE accounts SET balance = balance - :amt WHERE id = :id"), {"amt": amount, "id": from_id})
        await db.execute(text("UPDATE accounts SET balance = balance + :amt WHERE id = :id"), {"amt": amount, "id": to_id})

        result = await db.execute(text("SELECT balance FROM accounts WHERE id = :id"), {"id": from_id})
        if result.scalar() < 0:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        await db.commit()
        return {"status": "success"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Nested transactions (savepoints)
@app.post("/complex/")
async def complex_transfer(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        await db.execute(text("UPDATE accounts SET balance = 100 WHERE id = 1"))
        async with db.begin_nested():
            await db.execute(text("UPDATE accounts SET balance = 200 WHERE id = 2"))
            # Can rollback just this savepoint
```

### Q449: How do you create custom exception handlers with Pydantic?
**Answer:**
```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from datetime import datetime

app = FastAPI()

class ErrorResponse(BaseModel):
    detail: str
    error_code: str
    timestamp: str

@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.detail,
            error_code=f"HTTP_{exc.status_code}",
            timestamp=str(datetime.now())
        ).model_dump()
    )

@app.exception_handler(ValidationError)
async def validation_error(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            detail="Validation failed",
            error_code="VALIDATION_ERROR",
            timestamp=str(datetime.now())
        ).model_dump()
    )

# Custom business exceptions
class BusinessError(Exception):
    def __init__(self, message: str, code: str, status: int = 400):
        self.message = message
        self.code = code
        self.status = status

@app.exception_handler(BusinessError)
async def business_error(request: Request, exc: BusinessError):
    return JSONResponse(
        status_code=exc.status,
        content={"error": exc.code, "message": exc.message, "timestamp": str(datetime.now())}
    )

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id == 0:
        raise BusinessError(message="Invalid user ID", code="INVALID_USER_ID")
    return {"user_id": user_id}
```

### Q450: How do you implement full CRUD with tests in FastAPI?
**Answer:**
```python
# schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

class ItemResponse(ItemCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

# main.py
from fastapi import FastAPI, Depends, HTTPException
app = FastAPI()

@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.model_dump())
    db.add(db_item); db.commit(); db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item: raise HTTPException(status_code=404)
    return item

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item: raise HTTPException(status_code=404)
    for key, val in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, val)
    db.commit(); db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item: raise HTTPException(status_code=404)
    db.delete(item); db.commit()
    return {"message": "Deleted"}

# test_main.py
from fastapi.testclient import TestClient
client = TestClient(app)

def test_crud():
    r = client.post("/items/", json={"name": "Test", "price": 9.99})
    assert r.status_code == 200
    item_id = r.json()["id"]

    r = client.get(f"/items/{item_id}")
    assert r.status_code == 200

    r = client.put(f"/items/{item_id}", json={"price": 15.0})
    assert r.json()["price"] == 15.0

    r = client.delete(f"/items/{item_id}")
    assert r.status_code == 200

    r = client.get(f"/items/{item_id}")
    assert r.status_code == 404
```

### Q451: Two Sum - Find pair that sums to target
**Answer:**
```python
# Given array and target, return indices of two numbers that sum to target
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# O(n) time, O(n) space
print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
print(two_sum([3, 2, 4], 6))       # [1, 2]

# Sorted version (two-pointer)
def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    nums.sort()
    l, r = 0, len(nums) - 1
    while l < r:
        s = nums[l] + nums[r]
        if s == target: return [l, r]
        elif s < target: l += 1
        else: r -= 1
    return []
```

### Q452: Valid Parentheses
**Answer:**
```python
# Determine if brackets are valid: () [] {}
def is_valid(s: str) -> bool:
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
        else:
            stack.append(char)
    return len(stack) == 0

# O(n) time, O(n) space
print(is_valid("()[]{}"))    # True
print(is_valid("([)]"))      # False
print(is_valid("{[]}"))      # True

# Minimum add to make valid
def min_add(s: str) -> int:
    open_needed = close_needed = 0
    for char in s:
        if char == '(':
            close_needed += 1
        else:
            if close_needed > 0:
                close_needed -= 1
            else:
                open_needed += 1
    return open_needed + close_needed
```

### Q453: Merge Two Sorted Lists
**Answer:**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_two_lists(l1: ListNode, l2: ListNode) -> ListNode:
    dummy = ListNode()
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next

# O(n+m) time, O(1) space

# Recursive
def merge_recursive(l1: ListNode, l2: ListNode) -> ListNode:
    if not l1: return l2
    if not l2: return l1
    if l1.val <= l2.val:
        l1.next = merge_recursive(l1.next, l2)
        return l1
    l2.next = merge_recursive(l1, l2.next)
    return l2

# Merge K sorted lists
import heapq
def merge_k_lists(lists: list[ListNode]) -> ListNode:
    heap = [(l.val, i, l) for i, l in enumerate(lists) if l]
    heapq.heapify(heap)
    dummy = curr = ListNode()
    while heap:
        _, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

### Q454: Maximum Subarray (Kadane's Algorithm)
**Answer:**
```python
# Find contiguous subarray with largest sum
def max_subarray(nums: list[int]) -> int:
    max_curr = max_global = nums[0]
    for num in nums[1:]:
        max_curr = max(num, max_curr + num)
        max_global = max(max_global, max_curr)
    return max_global

# O(n) time, O(1) space
print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6

# Return subarray
def max_subarray_with_indices(nums: list[int]) -> list[int]:
    max_curr = max_global = nums[0]
    start = end = temp = 0
    for i in range(1, len(nums)):
        if nums[i] > max_curr + nums[i]:
            max_curr = nums[i]
            temp = i
        else:
            max_curr += nums[i]
        if max_curr > max_global:
            max_global = max_curr
            start = temp
            end = i
    return nums[start:end+1]
```

### Q455: Reverse a Linked List
**Answer:**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Iterative
def reverse_list(head: ListNode) -> ListNode:
    prev = None
    curr = head
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    return prev

# O(n) time, O(1) space

# Recursive
def reverse_recursive(head: ListNode) -> ListNode:
    if not head or not head.next:
        return head
    new_head = reverse_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head

# Reverse between positions (left, right)
def reverse_between(head: ListNode, left: int, right: int) -> ListNode:
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next
    curr = prev.next
    for _ in range(right - left):
        next_node = curr.next
        curr.next = next_node.next
        next_node.next = prev.next
        prev.next = next_node
    return dummy.next
```

### Q456: Binary Search
**Answer:**
```python
# Find target in sorted array
def binary_search(nums: list[int], target: int) -> int:
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target: return mid
        elif nums[mid] < target: l = mid + 1
        else: r = mid - 1
    return -1

# O(log n) time, O(1) space
print(binary_search([1, 3, 5, 7, 9], 5))  # 2

# Lower bound (first position)
def lower_bound(nums: list[int], target: int) -> int:
    l, r = 0, len(nums)
    while l < r:
        mid = (l + r) // 2
        if nums[mid] >= target: r = mid
        else: l = mid + 1
    return l

# Upper bound (last position + 1)
def upper_bound(nums: list[int], target: int) -> int:
    l, r = 0, len(nums)
    while l < r:
        mid = (l + r) // 2
        if nums[mid] > target: r = mid
        else: l = mid + 1
    return l

# Search in rotated sorted array
def search_rotated(nums: list[int], target: int) -> int:
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target: return mid
        if nums[l] <= nums[mid]:
            if nums[l] <= target < nums[mid]: r = mid - 1
            else: l = mid + 1
        else:
            if nums[mid] < target <= nums[r]: l = mid + 1
            else: r = mid - 1
    return -1
```

### Q457: LRU Cache
**Answer:**
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# Manual: dict + doubly linked list
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = self.next = None

class LRUCacheManual:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}
        self.head = Node()  # most recent
        self.tail = Node()  # least recent
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.cache: return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.val

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._add_to_front(node)
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

### Q458: Longest Substring Without Repeating Characters
**Answer:**
```python
# Find length of longest substring without repeating chars
def length_of_longest_substring(s: str) -> int:
    char_set = set()
    l = max_len = 0
    for r in range(len(s)):
        while s[r] in char_set:
            char_set.remove(s[l])
            l += 1
        char_set.add(s[r])
        max_len = max(max_len, r - l + 1)
    return max_len

# O(n) time, O(min(m,n)) space
print(length_of_longest_substring("abcabcbb"))  # 3 ("abc")
print(length_of_longest_substring("bbbbb"))     # 1 ("b")
print(length_of_longest_substring("pwwkew"))    # 3 ("wke")

# Return substring
def longest_substring(s: str) -> str:
    used = {}
    start = max_len = 0
    for i, ch in enumerate(s):
        if ch in used and used[ch] >= start:
            start = used[ch] + 1
        used[ch] = i
        if i - start + 1 > max_len:
            max_len = i - start + 1
            result = s[start:i+1]
    return result
```

### Q459: Number of Islands
**Answer:**
```python
# Count islands in 2D grid (1=land, 0=water)
def num_islands(grid: list[list[str]]) -> int:
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == "0":
            return
        grid[r][c] = "0"  # sink
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            dfs(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)
    return count

# O(rows*cols) time

# BFS version
from collections import deque
def num_islands_bfs(grid):
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                q = deque([(r, c)])
                grid[r][c] = "0"
                while q:
                    cr, cc = q.popleft()
                    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                            grid[nr][nc] = "0"
                            q.append((nr, nc))
    return count
```

### Q460: Product of Array Except Self
**Answer:**
```python
# Return array where each element = product of all other elements
# Constraint: O(n) time, no division
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [1] * n

    left = 1
    for i in range(n):
        result[i] = left
        left *= nums[i]

    right = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right
        right *= nums[i]

    return result

# O(n) time, O(1) space (excluding output)
print(product_except_self([1, 2, 3, 4]))  # [24, 12, 8, 6]

# With division (when allowed)
def product_with_division(nums):
    total = 1
    zero_count = nums.count(0)
    for n in nums:
        if n != 0: total *= n
    if zero_count > 1: return [0] * len(nums)
    return [total if zero_count == 1 and n == 0 else (total // n if n != 0 else total) for n in nums]
```

### Q461: Container With Most Water
**Answer:**
```python
# Find lines forming container with most water
def max_area(height: list[int]) -> int:
    l, r = 0, len(height) - 1
    max_water = 0
    while l < r:
        h = min(height[l], height[r])
        max_water = max(max_water, (r - l) * h)
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return max_water

# O(n) time, O(1) space
print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # 49
```

### Q462: 3Sum - Find triplets summing to zero
**Answer:**
```python
def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []
    n = len(nums)

    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        l, r = i + 1, n - 1
        target = -nums[i]

        while l < r:
            total = nums[l] + nums[r]
            if total == target:
                result.append([nums[i], nums[l], nums[r]])
                l += 1; r -= 1
                while l < r and nums[l] == nums[l - 1]: l += 1
                while l < r and nums[r] == nums[r + 1]: r -= 1
            elif total < target: l += 1
            else: r -= 1

    return result

# O(n^2) time
print(three_sum([-1, 0, 1, 2, -1, -4]))  # [[-1,-1,2], [-1,0,1]]

# KSum generalization
def k_sum(nums: list[int], target: int, k: int) -> list[list[int]]:
    nums.sort()
    result = []
    def helper(start, target, k, path):
        if k == 2:
            l, r = start, len(nums) - 1
            while l < r:
                s = nums[l] + nums[r]
                if s == target:
                    result.append(path + [nums[l], nums[r]])
                    l += 1; r -= 1
                    while l < r and nums[l] == nums[l-1]: l += 1
                elif s < target: l += 1
                else: r -= 1
        else:
            for i in range(start, len(nums) - k + 1):
                if i > start and nums[i] == nums[i-1]: continue
                if nums[i] * k > target or nums[-1] * k < target: break
                helper(i + 1, target - nums[i], k - 1, path + [nums[i]])
    helper(0, target, k, [])
    return result
```

### Q463: Longest Palindromic Substring
**Answer:**
```python
def longest_palindrome(s: str) -> str:
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return s[l+1:r]

    result = ""
    for i in range(len(s)):
        odd = expand(i, i)
        even = expand(i, i + 1)
        result = max(result, odd, even, key=len)

    return result

# O(n^2) time, O(1) space
print(longest_palindrome("babad"))  # "bab" or "aba"
print(longest_palindrome("cbbd"))   # "bb"

# DP solution
def longest_palindrome_dp(s: str) -> str:
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start = max_len = 0

    for i in range(n): dp[i][i] = True
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if length == 2:
                dp[i][j] = s[i] == s[j]
            else:
                dp[i][j] = dp[i+1][j-1] and s[i] == s[j]
            if dp[i][j] and length > max_len:
                start = i; max_len = length
    return s[start:start + max_len]
```

### Q464: Climbing Stairs
**Answer:**
```python
# Ways to climb n stairs (1 or 2 steps)
def climb_stairs(n: int) -> int:
    if n <= 2: return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

# O(n) time, O(1) space
print(climb_stairs(5))  # 8

# Recursive with memo
def climb_stairs_memo(n: int) -> int:
    memo = {1: 1, 2: 2}
    def helper(k):
        if k not in memo:
            memo[k] = helper(k - 1) + helper(k - 2)
        return memo[k]
    return helper(n)

# With 1, 2, or 3 steps
def climb_stairs_v2(n: int) -> int:
    if n <= 2: return n
    if n == 3: return 4
    a, b, c = 1, 2, 4
    for _ in range(4, n + 1):
        a, b, c = b, c, a + b + c
    return c

# Minimum cost to climb stairs
def min_cost_climbing(cost: list[int]) -> int:
    a = b = 0
    for c in cost:
        a, b = b, min(a, b) + c
    return min(a, b)
```

### Q465: Validate Binary Search Tree
**Answer:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def is_valid_bst(root: TreeNode) -> bool:
    def validate(node, low=float('-inf'), high=float('inf')):
        if not node: return True
        if node.val <= low or node.val >= high: return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)
    return validate(root)

# O(n) time, O(h) space

# Inorder traversal
def is_valid_bst_inorder(root: TreeNode) -> bool:
    stack = []
    prev = float('-inf')
    while stack or root:
        while root:
            stack.append(root)
            root = root.left
        root = stack.pop()
        if root.val <= prev: return False
        prev = root.val
        root = root.right
    return True

# Test
root = TreeNode(2, TreeNode(1), TreeNode(3))
print(is_valid_bst(root))  # True
invalid = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
print(is_valid_bst(invalid))  # False
```

### Q466: Maximum Depth of Binary Tree
**Answer:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

# Recursive
def max_depth(root: TreeNode) -> int:
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# O(n) time, O(h) space

# BFS (level order)
from collections import deque
def max_depth_bfs(root: TreeNode) -> int:
    if not root: return 0
    q = deque([root])
    depth = 0
    while q:
        for _ in range(len(q)):
            node = q.popleft()
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        depth += 1
    return depth

# DFS (stack)
def max_depth_dfs(root: TreeNode) -> int:
    if not root: return 0
    stack = [(root, 1)]
    max_d = 0
    while stack:
        node, d = stack.pop()
        max_d = max(max_d, d)
        if node.left: stack.append((node.left, d + 1))
        if node.right: stack.append((node.right, d + 1))
    return max_d

# Minimum depth
def min_depth(root: TreeNode) -> int:
    if not root: return 0
    if not root.left: return 1 + min_depth(root.right)
    if not root.right: return 1 + min_depth(root.left)
    return 1 + min(min_depth(root.left), min_depth(root.right))
```

### Q467: Coin Change - Minimum coins
**Answer:**
```python
# Minimum coins to make amount
def coin_change(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

# O(coins * amount) time
print(coin_change([1, 2, 5], 11))  # 3 (5+5+1)
print(coin_change([2], 3))         # -1

# Number of ways to make change
def change_ways(coins: list[int], amount: int) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    return dp[amount]

print(change_ways([1, 2, 5], 5))  # 4

# Greedy (works for canonical systems)
def coin_change_greedy(coins: list[int], amount: int) -> int:
    coins.sort(reverse=True)
    count = 0
    for coin in coins:
        count += amount // coin
        amount %= coin
    return count if amount == 0 else -1
```

### Q468: Serialize and Deserialize Binary Tree
**Answer:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

class Codec:
    def serialize(self, root: TreeNode) -> str:
        vals = []
        def dfs(node):
            if not node: vals.append("null"); return
            vals.append(str(node.val))
            dfs(node.left); dfs(node.right)
        dfs(root)
        return ",".join(vals)

    def deserialize(self, data: str) -> TreeNode:
        vals = iter(data.split(","))
        def dfs():
            val = next(vals)
            if val == "null": return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node
        return dfs()

# Usage
codec = Codec()
root = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
s = codec.serialize(root)
print(s)  # "1,2,null,null,3,4,null,null,5,null,null"
d = codec.deserialize(s)

# BFS serialization
from collections import deque
class CodecBFS:
    def serialize(self, root: TreeNode) -> str:
        if not root: return "null"
        q = deque([root]); vals = []
        while q:
            node = q.popleft()
            if node:
                vals.append(str(node.val))
                q.append(node.left); q.append(node.right)
            else: vals.append("null")
        return ",".join(vals)

    def deserialize(self, data: str) -> TreeNode:
        if data == "null": return None
        vals = data.split(",")
        root = TreeNode(int(vals[0]))
        q = deque([root]); i = 1
        while q:
            node = q.popleft()
            if vals[i] != "null":
                node.left = TreeNode(int(vals[i])); q.append(node.left)
            i += 1
            if vals[i] != "null":
                node.right = TreeNode(int(vals[i])); q.append(node.right)
            i += 1
        return root
```

### Q469: Word Search
**Answer:**
```python
# Find if word exists in 2D grid
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])
    def dfs(r, c, i):
        if i == len(word): return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[i]:
            return False
        temp = board[r][c]
        board[r][c] = "#"
        found = any(dfs(r+dr, c+dc, i+1) for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)])
        board[r][c] = temp
        return found

    # Early exit: check character counts
    from collections import Counter
    word_counts = Counter(word)
    board_counts = Counter(c for row in board for c in row)
    for c, cnt in word_counts.items():
        if board_counts[c] < cnt: return False

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0] and dfs(r, c, 0):
                return True
    return False

# O(rows * cols * 4^len(word)) time
board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
print(exist(board, "ABCCED"))  # True
print(exist(board, "SEE"))     # True
print(exist(board, "ABCB"))    # False
```

### Q470: Group Anagrams
**Answer:**
```python
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for s in strs:
        groups[''.join(sorted(s))].append(s)
    return list(groups.values())

# O(n * k log k) time
print(group_anagrams(["eat","tea","tan","ate","nat","bat"]))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

# Optimized: char count as key (O(n * k))
def group_anagrams_count(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s: count[ord(c) - ord('a')] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())

# Prime product method
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]
def group_anagrams_prime(strs):
    groups = defaultdict(list)
    for s in strs:
        key = 1
        for c in s: key *= primes[ord(c) - ord('a')]
        groups[key].append(s)
    return list(groups.values())
```

### Q471: Find All Anagrams in a String
**Answer:**
```python
from collections import Counter

def find_anagrams(s: str, p: str) -> list[int]:
    result = []
    p_count = Counter(p)
    window = Counter()

    for i, char in enumerate(s):
        window[char] += 1
        if i >= len(p):
            left_char = s[i - len(p)]
            window[left_char] -= 1
            if window[left_char] == 0: del window[left_char]
        if window == p_count:
            result.append(i - len(p) + 1)
    return result

# O(n) time
print(find_anagrams("cbaebabacd", "abc"))  # [0, 6]

# Array version (faster)
def find_anagrams_array(s: str, p: str) -> list[int]:
    result = []
    p_arr = [0] * 26
    w_arr = [0] * 26
    for c in p: p_arr[ord(c) - ord('a')] += 1
    for i, c in enumerate(s):
        w_arr[ord(c) - ord('a')] += 1
        if i >= len(p): w_arr[ord(s[i-len(p)]) - ord('a')] -= 1
        if w_arr == p_arr: result.append(i - len(p) + 1)
    return result
```

### Q472: Kth Largest Element in an Array
**Answer:**
```python
import heapq, random

def find_kth_largest(nums: list[int], k: int) -> int:
    heap = nums[:k]
    heapq.heapify(heap)
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    return heap[0]

# O(n log k) time, O(k) space
print(find_kth_largest([3,2,1,5,6,4], 2))  # 5

# QuickSelect (O(n) average)
def find_kth_largest_qs(nums: list[int], k: int) -> int:
    k = len(nums) - k
    def partition(l, r):
        pivot = nums[random.randint(l, r)]
        i, j = l, r
        while i <= j:
            while nums[i] < pivot: i += 1
            while nums[j] > pivot: j -= 1
            if i <= j: nums[i], nums[j] = nums[j], nums[i]; i += 1; j -= 1
        return i
    l, r = 0, len(nums) - 1
    while l < r:
        pi = partition(l, r)
        if pi <= k: l = pi
        else: r = pi - 1
    return nums[k]
```

### Q473: Permutations
**Answer:**
```python
def permute(nums: list[int]) -> list[list[int]]:
    result = []
    def backtrack(path, remaining):
        if not remaining: result.append(path); return
        for i, num in enumerate(remaining):
            backtrack(path + [num], remaining[:i] + remaining[i+1:])
    backtrack([], nums)
    return result

# O(n * n!) time
print(permute([1, 2, 3]))
# [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

# Iterative
def permute_iterative(nums):
    result = [[]]
    for num in nums:
        new = []
        for perm in result:
            for i in range(len(perm) + 1):
                new.append(perm[:i] + [num] + perm[i:])
        result = new
    return result

# Next permutation
def next_permutation(nums):
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]: i -= 1
    if i >= 0:
        j = len(nums) - 1
        while nums[j] <= nums[i]: j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    l, r = i + 1, len(nums) - 1
    while l < r:
        nums[l], nums[r] = nums[r], nums[l]
        l += 1; r -= 1
```

### Q474: Merge Intervals
**Answer:**
```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals: return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

# O(n log n) time
print(merge_intervals([[1,3],[2,6],[8,10],[15,18]]))
# [[1,6],[8,10],[15,18]]

# Insert interval
def insert_interval(intervals: list[list[int]], new_int: list[int]) -> list[list[int]]:
    result = []; i = 0; n = len(intervals)
    while i < n and intervals[i][1] < new_int[0]:
        result.append(intervals[i]); i += 1
    while i < n and intervals[i][0] <= new_int[1]:
        new_int[0] = min(new_int[0], intervals[i][0])
        new_int[1] = max(new_int[1], intervals[i][1])
        i += 1
    result.append(new_int)
    while i < n: result.append(intervals[i]); i += 1
    return result

# Meeting rooms
def can_attend(intervals):
    intervals.sort()
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]: return False
    return True
```

### Q475: Rotate Image (Matrix)
**Answer:**
```python
# Rotate NxN matrix 90 degrees clockwise in-place
def rotate(matrix: list[list[int]]) -> None:
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()

# O(n^2) time, O(1) space
m = [[1,2,3],[4,5,6],[7,8,9]]
rotate(m)
print(m)  # [[7,4,1],[8,5,2],[9,6,3]]

# Anti-clockwise
def rotate_anticlockwise(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    matrix.reverse()

# Layer rotation
def rotate_layers(matrix):
    n = len(matrix)
    for layer in range(n // 2):
        first, last = layer, n - 1 - layer
        for i in range(first, last):
            offset = i - first
            top = matrix[first][i]
            matrix[first][i] = matrix[last-offset][first]
            matrix[last-offset][first] = matrix[last][last-offset]
            matrix[last][last-offset] = matrix[i][last]
            matrix[i][last] = top
```

### Q476: Set Matrix Zeroes
**Answer:**
```python
# If element is 0, set entire row and column to 0
def set_zeroes(matrix: list[list[int]]) -> None:
    rows, cols = len(matrix), len(matrix[0])
    first_row = any(matrix[0][j] == 0 for j in range(cols))
    first_col = any(matrix[i][0] == 0 for i in range(rows))

    for i in range(1, rows):
        for j in range(1, cols):
            if matrix[i][j] == 0:
                matrix[0][j] = 0
                matrix[i][0] = 0

    for i in range(1, rows):
        for j in range(1, cols):
            if matrix[0][j] == 0 or matrix[i][0] == 0:
                matrix[i][j] = 0

    if first_row:
        for j in range(cols): matrix[0][j] = 0
    if first_col:
        for i in range(rows): matrix[i][0] = 0

# O(1) space
```

### Q477: Spiral Matrix
**Answer:**
```python
def spiral_order(matrix: list[list[int]]) -> list[int]:
    result = []
    if not matrix: return result
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        for j in range(left, right + 1): result.append(matrix[top][j])
        top += 1
        for i in range(top, bottom + 1): result.append(matrix[i][right])
        right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1): result.append(matrix[bottom][j])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1): result.append(matrix[i][left])
            left += 1
    return result

print(spiral_order([[1,2,3],[4,5,6],[7,8,9]]))
# [1,2,3,6,9,8,7,4,5]

# Generate spiral matrix
def generate_spiral(n: int) -> list[list[int]]:
    matrix = [[0] * n for _ in range(n)]
    t, b, l, r = 0, n-1, 0, n-1
    num = 1
    while t <= b and l <= r:
        for j in range(l, r + 1): matrix[t][j] = num; num += 1
        t += 1
        for i in range(t, b + 1): matrix[i][r] = num; num += 1
        r -= 1
        for j in range(r, l - 1, -1): matrix[b][j] = num; num += 1
        b -= 1
        for i in range(b, t - 1, -1): matrix[i][l] = num; num += 1
        l += 1
    return matrix
```

### Q478: Combination Sum
**Answer:**
```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    result = []
    candidates.sort()
    def backtrack(remaining, path, start):
        if remaining == 0: result.append(path); return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining: break
            backtrack(remaining - candidates[i], path + [candidates[i]], i)
    backtrack(target, [], 0)
    return result

print(combination_sum([2, 3, 6, 7], 7))  # [[2,2,3],[7]]

# Combination Sum II (each used once)
def combination_sum_ii(candidates: list[int], target: int) -> list[list[int]]:
    result = []
    candidates.sort()
    def backtrack(remaining, path, start):
        if remaining == 0: result.append(path); return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining: break
            if i > start and candidates[i] == candidates[i-1]: continue
            backtrack(remaining - candidates[i], path + [candidates[i]], i+1)
    backtrack(target, [], 0)
    return result

# Combination Sum III (k numbers 1-9 summing to n)
def combination_sum_iii(k: int, n: int) -> list[list[int]]:
    result = []
    def backtrack(remaining_k, remaining_n, path, start):
        if remaining_k == 0 and remaining_n == 0: result.append(path); return
        if remaining_k == 0 or remaining_n <= 0: return
        for i in range(start, 10):
            if i > remaining_n: break
            backtrack(remaining_k - 1, remaining_n - i, path + [i], i + 1)
    backtrack(k, n, [], 1)
    return result
```

### Q479: House Robber
**Answer:**
```python
# Max sum without adjacent elements
def rob(nums: list[int]) -> int:
    prev2 = prev1 = 0
    for num in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + num)
    return prev1

print(rob([1, 2, 3, 1]))       # 4
print(rob([2, 7, 9, 3, 1]))    # 12

# Circular houses
def rob_ii(nums: list[int]) -> int:
    if len(nums) == 1: return nums[0]
    def linear(houses):
        a = b = 0
        for h in houses: a, b = b, max(b, a + h)
        return b
    return max(linear(nums[:-1]), linear(nums[1:]))

# Tree houses (House Robber III)
def rob_iii(root) -> int:
    def dfs(node):
        if not node: return (0, 0)
        l = dfs(node.left); r = dfs(node.right)
        rob = node.val + l[1] + r[1]
        skip = max(l) + max(r)
        return (rob, skip)
    return max(dfs(root))
```

### Q480: Decode Ways
**Answer:**
```python
# Count ways to decode string (A=1..Z=26)
def num_decodings(s: str) -> int:
    if not s or s[0] == "0": return 0
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        one = int(s[i-1])
        two = int(s[i-2:i])
        if 1 <= one <= 9: dp[i] += dp[i-1]
        if 10 <= two <= 26: dp[i] += dp[i-2]
    return dp[n]

print(num_decodings("12"))   # 2
print(num_decodings("226"))  # 3

# O(1) space
def num_decodings_opt(s):
    if not s or s[0] == "0": return 0
    a = b = 1
    for i in range(1, len(s)):
        curr = 0
        if s[i] != "0": curr += b
        if 10 <= int(s[i-1:i+1]) <= 26: curr += a
        a, b = b, curr
    return b
```

### Q481: Longest Increasing Subsequence
**Answer:**
```python
def length_of_lis(nums: list[int]) -> int:
    tails = []
    for num in nums:
        l, r = 0, len(tails)
        while l < r:
            mid = (l + r) // 2
            if tails[mid] < num: l = mid + 1
            else: r = mid
        if l == len(tails): tails.append(num)
        else: tails[l] = num
    return len(tails)

# O(n log n) time
print(length_of_lis([10,9,2,5,3,7,101,18]))  # 4

# DP O(n^2)
def length_of_lis_dp(nums):
    if not nums: return 0
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]: dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

# Number of LIS
def find_number_of_lis(nums):
    if not nums: return 0
    n = len(nums)
    length = [1] * n
    count = [1] * n
    max_len = 1
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i] = length[j] + 1
                    count[i] = count[j]
                elif length[j] + 1 == length[i]:
                    count[i] += count[j]
        max_len = max(max_len, length[i])
    return sum(c for l, c in zip(length, count) if l == max_len)
```

### Q482: Unique Paths
**Answer:**
```python
# Ways to reach bottom-right in grid
def unique_paths(m: int, n: int) -> int:
    row = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            row[j] += row[j - 1]
    return row[-1]

print(unique_paths(3, 7))  # 28

# With obstacles
def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[-1][-1] == 1: return 0
    dp = [0] * n; dp[0] = 1
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1: dp[j] = 0
            elif j > 0: dp[j] += dp[j-1]
    return dp[-1]

# With obstacles (2D DP)
def unique_paths_obstacles_2d(obstacle_grid):
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    dp = [[0] * n for _ in range(m)]
    for i in range(m):
        if obstacle_grid[i][0] == 1: break
        dp[i][0] = 1
    for j in range(n):
        if obstacle_grid[0][j] == 1: break
        dp[0][j] = 1
    for i in range(1, m):
        for j in range(1, n):
            if obstacle_grid[i][j] == 0:
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[-1][-1]
```

### Q483: Word Break
**Answer:**
```python
# Can string be segmented into dictionary words?
def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[-1]

print(word_break("leetcode", ["leet", "code"]))  # True
print(word_break("catsandog", ["cats","dog","sand","and","cat"]))  # False

# BFS
from collections import deque
def word_break_bfs(s, word_dict):
    words = set(word_dict)
    q = deque([0]); visited = {0}
    while q:
        start = q.popleft()
        if start == len(s): return True
        for end in range(start + 1, len(s) + 1):
            if end not in visited and s[start:end] in words:
                visited.add(end); q.append(end)
    return False

# Word Break II - return all sentences
def word_break_ii(s: str, word_dict: list[str]) -> list[str]:
    words = set(word_dict)
    memo = {}
    def dfs(start):
        if start in memo: return memo[start]
        if start == len(s): return [""]
        sentences = []
        for end in range(start + 1, len(s) + 1):
            if s[start:end] in words:
                for sub in dfs(end):
                    sentence = s[start:end]
                    if sub: sentence += " " + sub
                    sentences.append(sentence)
        memo[start] = sentences
        return sentences
    return dfs(0)
```

### Q484: Edit Distance (Levenshtein)
**Answer:**
```python
# Minimum ops to convert word1 to word2 (insert, delete, replace)
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[-1][-1]

print(min_distance("horse", "ros"))      # 3
print(min_distance("intention", "execution"))  # 5

# O(min(m,n)) space
def min_distance_opt(word1, word2):
    if len(word1) < len(word2): word1, word2 = word2, word1
    m, n = len(word1), len(word2)
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]: curr[j] = prev[j-1]
            else: curr[j] = 1 + min(prev[j], curr[j-1], prev[j-1])
        prev = curr
    return prev[n]
```

### Q485: First Missing Positive
**Answer:**
```python
# Find smallest missing positive integer
# O(n) time, O(1) space
def first_missing_positive(nums: list[int]) -> int:
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            correct = nums[i] - 1
            nums[i], nums[correct] = nums[correct], nums[i]
    for i in range(n):
        if nums[i] != i + 1: return i + 1
    return n + 1

print(first_missing_positive([1,2,0]))        # 3
print(first_missing_positive([3,4,-1,1]))     # 2
print(first_missing_positive([7,8,9,11,12]))  # 1
```

### Q486: Find the Duplicate Number
**Answer:**
```python
# Find duplicate in [1,n] array, O(1) space, no modify
def find_duplicate(nums: list[int]) -> int:
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast: break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow

print(find_duplicate([1,3,4,2,2]))  # 2
print(find_duplicate([3,1,3,4,2]))  # 3

# Binary search (counting)
def find_duplicate_bs(nums):
    l, r = 1, len(nums) - 1
    while l < r:
        mid = (l + r) // 2
        count = sum(1 for num in nums if num <= mid)
        if count > mid: r = mid
        else: l = mid + 1
    return l
```

### Q487: Trapping Rain Water
**Answer:**
```python
def trap(height: list[int]) -> int:
    if not height: return 0
    l, r = 0, len(height) - 1
    l_max = r_max = water = 0
    while l < r:
        if height[l] < height[r]:
            if height[l] >= l_max: l_max = height[l]
            else: water += l_max - height[l]
            l += 1
        else:
            if height[r] >= r_max: r_max = height[r]
            else: water += r_max - height[r]
            r -= 1
    return water

print(trap([0,1,0,2,1,0,1,3,2,1,2,1]))  # 6
```

### Q488: Sliding Window Maximum
**Answer:**
```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    result = []
    dq = deque()
    for i, num in enumerate(nums):
        while dq and dq[0] < i - k + 1: dq.popleft()
        while dq and nums[dq[-1]] < num: dq.pop()
        dq.append(i)
        if i >= k - 1: result.append(nums[dq[0]])
    return result

print(max_sliding_window([1,3,-1,-3,5,3,6,7], 3))  # [3,3,5,5,6,7]

# Heap version O(n log k)
import heapq
def max_sliding_window_heap(nums, k):
    result = []
    heap = [(-nums[i], i) for i in range(k)]
    heapq.heapify(heap)
    result.append(-heap[0][0])
    for i in range(k, len(nums)):
        heapq.heappush(heap, (-nums[i], i))
        while heap[0][1] <= i - k: heapq.heappop(heap)
        result.append(-heap[0][0])
    return result
```

### Q489: Longest Consecutive Sequence
**Answer:**
```python
def longest_consecutive(nums: list[int]) -> int:
    num_set = set(nums)
    longest = 0
    for num in num_set:
        if num - 1 not in num_set:
            curr = num; length = 1
            while curr + 1 in num_set: curr += 1; length += 1
            longest = max(longest, length)
    return longest

print(longest_consecutive([100,4,200,1,3,2]))  # 4
print(longest_consecutive([0,3,7,2,5,8,4,6,0,1]))  # 9

# Union-find
def longest_consecutive_uf(nums):
    if not nums: return 0
    parent = {n: n for n in nums}
    size = {n: 1 for n in nums}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        px, py = find(x), find(y)
        if px != py: parent[px] = py; size[py] += size[px]
    for num in nums:
        if num + 1 in parent: union(num, num + 1)
    return max(size.values())
```

### Q490: Subarray Sum Equals K
**Answer:**
```python
from collections import defaultdict

def subarray_sum(nums: list[int], k: int) -> int:
    prefix = 0; count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1
    for num in nums:
        prefix += num
        count += sum_count[prefix - k]
        sum_count[prefix] += 1
    return count

print(subarray_sum([1,1,1], 2))     # 2
print(subarray_sum([1,2,3], 3))     # 2

# Subarray divisible by K
def subarray_divisible(nums: list[int], k: int) -> int:
    prefix = 0; count = 0
    mod_count = defaultdict(int)
    mod_count[0] = 1
    for num in nums:
        prefix += num
        mod = prefix % k
        count += mod_count[mod]
        mod_count[mod] += 1
    return count

# Maximum subarray with exactly K elements
def max_subarray_k(nums, k):
    prefix = [0]
    for num in nums: prefix.append(prefix[-1] + num)
    dq = deque(); result = float('-inf')
    for i in range(len(prefix)):
        while dq and dq[0] < i - k: dq.popleft()
        if dq: result = max(result, prefix[i] - prefix[dq[0]])
        while dq and prefix[dq[-1]] >= prefix[i]: dq.pop()
        dq.append(i)
    return result
```

### Q491: Reorder Data in Log Files
**Answer:**
```python
def reorder_log_files(logs: list[str]) -> list[str]:
    letters, digits = [], []
    for log in logs:
        ident, *rest = log.split()
        if rest[0].isalpha():
            letters.append((ident, rest))
        else:
            digits.append(log)
    letters.sort(key=lambda x: (' '.join(x[1]), x[0]))
    result = [f"{ident} {' '.join(content)}" for ident, content in letters]
    result.extend(digits)
    return result

print(reorder_log_files([
    "dig1 8 1 5 1",
    "let1 art can",
    "dig2 3 6",
    "let2 own kit dig",
    "let3 art zero"
]))
# ['let1 art can', 'let3 art zero', 'let2 own kit dig', 'dig1 8 1 5 1', 'dig2 3 6']
```

### Q492: Top K Frequent Elements
**Answer:**
```python
from collections import Counter
import heapq

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)

print(top_k_frequent([1,1,1,2,2,3], 2))  # [1, 2]

# Bucket sort O(n)
def top_k_frequent_bucket(nums, k):
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items(): buckets[freq].append(num)
    result = []
    for freq in range(len(buckets) - 1, -1, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k: return result
    return result

# QuickSelect O(n) average
def top_k_frequent_qs(nums, k):
    count = Counter(nums)
    unique = list(count.keys())
    def partition(l, r):
        pivot = count[unique[(l+r)//2]]
        i, j = l, r
        while i <= j:
            while count[unique[i]] > pivot: i += 1
            while count[unique[j]] < pivot: j -= 1
            if i <= j: unique[i], unique[j] = unique[j], unique[i]; i += 1; j -= 1
        return i
    l, r = 0, len(unique) - 1
    while True:
        pi = partition(l, r)
        if pi == k: break
        elif pi < k: l = pi
        else: r = pi - 1
    return unique[:k]
```

### Q493: Task Scheduler
**Answer:**
```python
from collections import Counter

def least_interval(tasks: list[str], n: int) -> int:
    count = Counter(tasks)
    max_freq = max(count.values())
    max_count = sum(1 for v in count.values() if v == max_freq)
    return max(len(tasks), (max_freq - 1) * (n + 1) + max_count)

print(least_interval(["A","A","A","B","B","B"], 2))  # 8

# Simulated
def least_interval_simulated(tasks, n):
    count = Counter(tasks)
    heap = [-c for c in count.values()]
    heapq.heapify(heap)
    time = 0
    from collections import deque
    cool = deque()
    while heap or cool:
        time += 1
        if heap:
            remaining = heapq.heappop(heap) + 1
            if remaining < 0: cool.append((remaining, time + n))
        if cool and cool[0][1] == time:
            heapq.heappush(heap, cool.popleft()[0])
    return time
```

### Q494: Design a URL Shortener
**Answer:**
```python
import hashlib, string

class URLShortener:
    def __init__(self):
        self.url_to_code = {}
        self.code_to_url = {}
        self.base62 = string.ascii_letters + string.digits

    def _encode(self, num: int) -> str:
        code = []
        while num > 0:
            code.append(self.base62[num % 62])
            num //= 62
        return ''.join(reversed(code))

    def shorten(self, long_url: str) -> str:
        if long_url in self.url_to_code:
            return self.url_to_code[long_url]
        hash_obj = hashlib.md5(long_url.encode())
        num = int(hash_obj.hexdigest()[:8], 16)
        code = self._encode(num)
        self.url_to_code[long_url] = code
        self.code_to_url[code] = long_url
        return f"https://short.url/{code}"

    def resolve(self, short_url: str) -> str:
        code = short_url.split("/")[-1]
        return self.code_to_url.get(code, "Not found")

shortener = URLShortener()
short = shortener.shorten("https://example.com/very/long/url")
print(short)
print(shortener.resolve(short))
```

### Q495: Design a Rate Limiter
**Answer:**
```python
import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_req = max_requests
        self.window = window_seconds
        self.requests = {}

    def allow_request(self, user_id: str) -> bool:
        now = time.time()
        if user_id not in self.requests:
            self.requests[user_id] = deque()
        while self.requests[user_id] and self.requests[user_id][0] <= now - self.window:
            self.requests[user_id].popleft()
        if len(self.requests[user_id]) >= self.max_req:
            return False
        self.requests[user_id].append(now)
        return True

# Token Bucket
class TokenBucket:
    def __init__(self, capacity: int, fill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.fill_rate = fill_rate
        self.last_refill = time.time()

    def allow_request(self, tokens: int = 1) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.fill_rate)
        self.last_refill = now
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

limiter = SlidingWindowRateLimiter(10, 60)
for _ in range(15):
    print(limiter.allow_request("user1"))  # True x10, False x5
```

### Q496: Design a Thread-Safe Singleton
**Answer:**
```python
import threading

class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    def __init__(self):
        self.value = 0

def worker():
    s = Singleton()
    s.value += 1

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
print(Singleton().value)  # 10

# Simpler: module-level singleton
# _instance = None
# def get_instance():
#     global _instance
#     if _instance is None:
#         _instance = MyClass()
#     return _instance
```

### Q497: Design Producer-Consumer Queue
**Answer:**
```python
import threading, time, random
from collections import deque

class ThreadSafeQueue:
    def __init__(self, max_size: int = 10):
        self.queue = deque()
        self.max_size = max_size
        self.mutex = threading.Lock()
        self.not_full = threading.Condition(self.mutex)
        self.not_empty = threading.Condition(self.mutex)

    def put(self, item):
        with self.not_full:
            while len(self.queue) >= self.max_size:
                self.not_full.wait()
            self.queue.append(item)
            self.not_empty.notify()

    def get(self):
        with self.not_empty:
            while len(self.queue) == 0:
                self.not_empty.wait()
            item = self.queue.popleft()
            self.not_full.notify()
            return item

q = ThreadSafeQueue(5)
def producer():
    for i in range(10):
        q.put(i); print(f"Produced: {i}"); time.sleep(random.random() * 0.1)
def consumer():
    for _ in range(10):
        item = q.get(); print(f"Consumed: {item}"); time.sleep(random.random() * 0.2)
t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t1.start(); t2.start(); t1.join(); t2.join()
```

### Q498: Design Parking Lot
**Answer:**
```python
from enum import Enum

class VehicleType(Enum):
    CAR = 1; MOTORCYCLE = 2; TRUCK = 3

class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type

class ParkingSpot:
    def __init__(self, spot_id: int, vehicle_type: VehicleType):
        self.spot_id = spot_id
        self.vehicle_type = vehicle_type
        self.available = True
        self.vehicle = None

    def can_fit(self, vehicle: Vehicle) -> bool:
        return self.available and vehicle.vehicle_type == self.vehicle_type

    def park(self, vehicle: Vehicle) -> bool:
        if not self.can_fit(vehicle): return False
        self.vehicle = vehicle; self.available = False; return True

    def leave(self):
        self.vehicle = None; self.available = True

class ParkingLot:
    def __init__(self):
        self.spots = {
            VehicleType.CAR: [],
            VehicleType.MOTORCYCLE: [],
            VehicleType.TRUCK: []
        }

    def add_spot(self, spot: ParkingSpot):
        self.spots[spot.vehicle_type].append(spot)

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        for spot in self.spots[vehicle.vehicle_type]:
            if spot.can_fit(vehicle): return spot.park(vehicle)
        return False

    def get_available(self) -> dict:
        return {vt: sum(1 for s in spots if s.available) for vt, spots in self.spots.items()}

lot = ParkingLot()
lot.add_spot(ParkingSpot(1, VehicleType.CAR))
lot.add_spot(ParkingSpot(2, VehicleType.CAR))
car = Vehicle("ABC123", VehicleType.CAR)
print(lot.park_vehicle(car))  # True
print(lot.get_available())    # {CAR: 1, ...}
```

### Q499: Serialize and Deserialize N-ary Tree
**Answer:**
```python
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children else []

class CodecNary:
    def serialize(self, root: Node) -> str:
        if not root: return ""
        vals = []
        def dfs(node):
            vals.append(str(node.val))
            vals.append(str(len(node.children)))
            for child in node.children: dfs(child)
        dfs(root)
        return ",".join(vals)

    def deserialize(self, data: str) -> Node:
        if not data: return None
        vals = iter(data.split(","))
        def dfs():
            val = int(next(vals))
            n_children = int(next(vals))
            node = Node(val, [])
            for _ in range(n_children): node.children.append(dfs())
            return node
        return dfs()

# Test
root = Node(1, [Node(3, [Node(5), Node(6)]), Node(2), Node(4)])
codec = CodecNary()
s = codec.serialize(root)
print(s)
d = codec.deserialize(s)
print(d.val)  # 1
```

### Q500: Median of Two Sorted Arrays
**Answer:**
```python
def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)
    total = m + n
    half = (total + 1) // 2

    l, r = 0, m
    while l <= r:
        i = (l + r) // 2
        j = half - i

        left1 = nums1[i - 1] if i > 0 else float('-inf')
        right1 = nums1[i] if i < m else float('inf')
        left2 = nums2[j - 1] if j > 0 else float('-inf')
        right2 = nums2[j] if j < n else float('inf')

        if left1 <= right2 and left2 <= right1:
            if total % 2 == 0:
                return (max(left1, left2) + min(right1, right2)) / 2
            return max(left1, left2)
        elif left1 > right2:
            r = i - 1
        else:
            l = i + 1

    raise ValueError("Input arrays not sorted")
```
O(log(min(m,n))) time.
print(find_median_sorted_arrays([1,3], [2]))      # 2.0
print(find_median_sorted_arrays([1,2], [3,4]))    # 2.5
```

### Q501: What is the output of `[] == []` vs `[] is []`?
**Answer:**
```python
a = []
b = []
print(a == b)   # True (same value)
print(a is b)   # False (different objects)

# But:
print([] == [])  # True
print([] is [])  # False

# However, small integers are cached:
x = 256
y = 256
print(x is y)  # True (cached)

x = 257
y = 257
print(x is y)  # False (not cached, implementation dependent)

# Strings can be interned:
s1 = "hello"
s2 = "hello"
print(s1 is s2)  # True (interned at compile-time)

s3 = "hello!"
s4 = "hello!"
print(s3 is s4)  # False (not interned)
```

### Q502: What happens with default mutable arguments?
**Answer:**
```python
def append_to(element, target=[]):
    target.append(element)
    return target

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2]  <-- Gotcha!
print(append_to(3))  # [1, 2, 3]

# Default arguments are evaluated once at function definition time
# Fix: use None as default
def append_to_fixed(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target

print(append_to_fixed(1))  # [1]
print(append_to_fixed(2))  # [2]  <-- Fresh list each time
```

### Q503: What is the output of `1.1 + 2.2 == 3.3`?
**Answer:**
```python
print(1.1 + 2.2 == 3.3)  # False!

# Floating point: 1.1 + 2.2 = 3.3000000000000003
print(repr(1.1 + 2.2))  # 3.3000000000000003
print(repr(3.3))        # 3.2999999999999998

# Fix: use tolerance
import math
print(abs(1.1 + 2.2 - 3.3) < 1e-9)  # True

# Fix: use Decimal
from decimal import Decimal
print(Decimal('1.1') + Decimal('2.2') == Decimal('3.3'))  # True

# Avoid float for money / exact calculations
```

### Q504: Why does `0.1 + 0.2 - 0.3` not equal 0?
**Answer:**
```python
print(0.1 + 0.2 - 0.3)  # 5.551115123125783e-17

# IEEE 754 floating point representation
# 0.1 and 0.2 cannot be represented exactly in binary
# The error is ~5.5e-17

# Using math.isclose for comparison
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True

# Using round
print(round(0.1 + 0.2 - 0.3, 15))  # 0.0
```

### Q505: What is the scope of list comprehension variables?
**Answer:**
```python
# Python 2 (leaks variable):
# x = 'before'
# [x for x in range(3)]
# print(x)  # 2 (leaked from comprehension)

# Python 3 (no leak):
x = 'before'
y = [x for x in range(3)]
print(x)  # 'before' (not leaked)
print(y)  # [0, 1, 2]

# But in Python 3.8+ (walrus operator):
[y for x in [1, 2, 3] if (z := x > 0)]
# print(z)  # NameError - z is not leaked

# Nested comprehensions and generator expressions:
squares = [x * x for x in range(5)]
# x is not accessible here

# Generator expression variables:
gen = (x for x in range(5))
# x is not accessible here
```

### Q506: What is the difference between `==`, `is`, and `in`?
**Answer:**
```python
# == checks value equality (calls __eq__)
# is checks identity (same object, same id)
# in checks membership

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True (same content)
print(a is b)  # False (different objects)
print(a is c)  # True (same object)

# Surprising is:
# None is a singleton
x = None
print(x is None)  # True (idiomatic)
print(x == None)  # True but not idiomatic

# in with different types:
print(1 in [1, 2, 3])    # True
print("e" in "hello")     # True
print("a" in {"a": 1})    # True (checks keys)
print(1 in {1: "a"})      # True (checks keys)
```

### Q507: How does Python handle `+=` with mutable vs immutable types?
**Answer:**
```python
# Immutable (int, str, tuple): creates new object
x = 5
print(id(x))  # some id
x += 1
print(id(x))  # different id (new object)

# Mutable (list, set, dict): modifies in-place
a = [1, 2]
print(id(a))  # some id
a += [3]
print(id(a))  # same id (in-place modification)

# But: a = a + [3] (with + operator) creates new object
b = [1, 2]
print(id(b))  # some id
b = b + [3]
print(id(b))  # different id

# String concatenation creates new strings
s = ""
for i in range(100):
    s += str(i)  # Creates new string each time (O(n^2))
# Fix: use ''.join(str(i) for i in range(100))
```

### Q508: Why does `a = 256; b = 256; a is b` return True but `a = 257; b = 257` return False?
**Answer:**
```python
# Python caches small integers (-5 to 256)
a = 256
b = 256
print(a is b)  # True (cached)

a = 257
b = 257
print(a is b)  # False (not cached, implementation-dependent)

# But:
a, b = 257, 257
print(a is b)  # True! (same compile-time constant in tuple unpacking)

# At module/REPL level:
a = 257
b = 257
print(a is b)  # May be False (separate bytecode operations)

# Inside function:
def test():
    a = 257
    b = 257
    return a is b
print(test())  # True (PEP 523 - constant folding)
```

### Q509: What is the late binding closure gotcha?
**Answer:**
```python
# Common gotcha:
funcs = []
for i in range(3):
    funcs.append(lambda: i)

for f in funcs:
    print(f())  # 2, 2, 2 (all see last i value)

# Why: closures capture the variable reference, not the value
# By the time lambdas execute, i = 2

# Fix 1: default argument (early binding)
funcs = []
for i in range(3):
    funcs.append(lambda x=i: x)

for f in funcs:
    print(f())  # 0, 1, 2

# Fix 2: nested function with parameter
def make_func(x):
    return lambda: x

funcs = [make_func(i) for i in range(3)]
for f in funcs:
    print(f())  # 0, 1, 2

# Fix 3: functools.partial
from functools import partial
funcs = [partial(lambda x: x, i) for i in range(3)]
```

### Q510: What is the difference between `type` and `isinstance`?
**Answer:**
```python
class A: pass
class B(A): pass
b = B()

print(type(b) == A)       # False
print(isinstance(b, A))   # True (considers inheritance)

# isinstance is preferred for type checking:
# - isinstance handles inheritance
# - isinstance handles abstract base classes
from collections.abc import Iterable
print(isinstance([1,2], Iterable))  # True
print(type([1,2]) == Iterable)      # False

# type is useful for exact type check:
print(type(b) == B)       # True (exact match)
print(isinstance(b, B))   # True

# isinstance with tuple of types:
print(isinstance(42, (int, float, str)))  # True
```

### Q511: What happens when you modify a list while iterating?
**Answer:**
```python
# Removing elements while iterating causes issues:
lst = [1, 2, 3, 4, 5]
for i, item in enumerate(lst):
    if item % 2 == 0:
        del lst[i]
print(lst)  # [1, 3, 5]  (works in this case, but bug-prone)

# Better example (demonstrates skip):
lst = [1, 2, 2, 3, 4]
for item in lst:
    if item == 2:
        lst.remove(item)
print(lst)  # [1, 2, 3, 4]  (didn't remove second 2!)

# Why: when you remove at index i, all elements shift left
# The loop pointer advances past the shifted element

# Correct way: iterate over a copy
lst = [1, 2, 2, 3, 4]
for item in lst[:]:  # Copy
    if item == 2:
        lst.remove(item)
print(lst)  # [1, 3, 4]

# Or use list comprehension:
lst = [1, 2, 2, 3, 4]
lst = [x for x in lst if x != 2]
print(lst)  # [1, 3, 4]

# Similarly for dict:
d = {"a": 1, "b": 2, "c": 3}
for k in d:  # RuntimeError: dictionary changed size during iteration
    del d[k]
```

### Q512: What is the string interning gotcha with `==` vs `is`?
**Answer:**
```python
# String interning:
a = "hello_world"  # Contains underscore - may NOT be interned
b = "hello_world"

# CPython interns:
# - All identifiers (alphanumeric strings)
# - String literals at compile time
# - Small strings (implementation dependent)

# In CPython, "hello_world" as a literal is compiled to the same constant
# So usually:
print(a is b)  # True (same compile-time constant)

# But dynamically created strings:
s1 = "hello"
s2 = "".join(["h", "e", "l", "l", "o"])
print(s1 == s2)  # True
print(s1 is s2)  # False (different objects)

# Explicit interning:
import sys
s3 = sys.intern(s2)
print(s1 is s3)  # True (now interned)

# Good practice: always use == for string comparison
# Use is only for comparing with None (x is None)
```

### Q513: Why does `all([])` return True?
**Answer:**
```python
print(all([]))    # True
print(any([]))    # False

# all: "there are no False elements"
# any: "there is at least one True element"

# Vacuously true:
# For an empty iterable, all elements are true
# (there are no elements that are false)

print(all([True]))   # True
print(all([False]))  # False
print(any([True]))   # True
print(any([False]))  # False

# Practical gotcha:
def all_even(nums):
    return all(x % 2 == 0 for x in nums)

print(all_even([]))  # True (vacuously)
# Be careful with empty iterables - handle the edge case

# Other vacuous truths:
print(sum([]))       # 0
print(min([]))       # ValueError! (not vacuous)
```

### Q514: What is the difference between `extend` and `+=` on a list?
**Answer:**
```python
# extend modifies in-place
a = [1, 2]
b = a.extend([3, 4])
print(a)  # [1, 2, 3, 4]
print(b)  # None! extend returns None

# += also modifies in-place but returns the modified list
a = [1, 2]
b = a
a += [3, 4]       # In-place modification
print(a)  # [1, 2, 3, 4]
print(b)  # [1, 2, 3, 4] (same object, b modified too)

# but a = a + [3, 4] creates a new object
a = [1, 2]
b = a
a = a + [3, 4]    # New object
print(a)  # [1, 2, 3, 4]
print(b)  # [1, 2] (b unchanged)

# For tuples, += always creates a new object:
t = (1, 2)
print(id(t))
t += (3, 4)       # Creates new tuple
print(id(t))      # Different id
```

### Q515: What is the `else` clause in for/while loops?
**Answer:**
```python
# else clause executes when loop completes normally (no break)
for i in range(3):
    print(i)
else:
    print("Loop completed without break")
# 0 1 2 "Loop completed without break"

# else does NOT execute when break is hit
for i in range(3):
    if i == 1:
        break
    print(i)
else:
    print("This won't print")
# 0

# Practical use: search patterns
def find_value(lst, target):
    for item in lst:
        if item == target:
            print(f"Found {target}")
            break
    else:
        print(f"{target} not found")

find_value([1, 2, 3], 2)  # "Found 2"
find_value([1, 2, 3], 4)  # "4 not found"

# Same works with while loops:
n = 0
while n < 3:
    n += 1
else:
    print("While completed")  # Prints
n = 0
while n < 3:
    if n == 1: break
    n += 1
else:
    print("Won't print")  # Doesn't print
```

### Q516: How does Python's `or` and `and` short-circuiting work?
**Answer:**
```python
# or returns first truthy value or last falsy value
print(0 or False or 42 or 100)  # 42 (first truthy)
print(0 or False)                # False (both falsy)
print([] or {})                  # {} (last falsy)
print("" or "default")           # "default"

# and returns first falsy value or last truthy value
print(42 and "hello" and [])  # [] (first falsy)
print(42 and "hello")         # "hello" (last truthy)
print(0 and 42)               # 0 (first falsy)

# Short-circuiting means expressions on right may not evaluate
def expensive():
    print("Expensive called")
    return True

result = False and expensive()  # expensive() never called
print(result)  # False

result = True or expensive()    # expensive() never called
print(result)  # True

# Common idiom: default values
name = input_name or "Guest"  # Use "Guest" if input_name is falsy

# Chained comparisons (not related but similar gotcha):
print(1 < 2 < 3)    # True (Python evaluates as 1 < 2 and 2 < 3)
print(1 < 2 > 1)    # True (1 < 2 and 2 > 1)
```

### Q517: What is the difference between `copy.copy` and `copy.deepcopy`?
**Answer:**
```python
import copy

# Shallow copy: copies references
original = [[1, 2, 3], [4, 5, 6]]
shallow = copy.copy(original)

shallow[0][0] = 99
print(original[0][0])  # 99 (shared reference!)
print(shallow[0] is original[0])  # True

# Deep copy: recursively copies everything
original = [[1, 2, 3], [4, 5, 6]]
deep = copy.deepcopy(original)

deep[0][0] = 99
print(original[0][0])  # 1 (independent)

# Copy of immutable types doesn't matter:
import copy
x = 42
y = copy.copy(x)
print(x is y)  # True (immutable, same object)

# List slicing creates shallow copy
a = [[1, 2], [3, 4]]
b = a[:]
b[0][0] = 99
print(a[0][0])  # 99 (shallow!)
```

### Q518: What is the `__name__ == '__main__'` idiom?
**Answer:**
```python
# When a script is run directly, __name__ == '__main__'
# When imported as module, __name__ == module_name

# my_script.py
def main():
    print("Running directly")

if __name__ == '__main__':
    main()  # Only runs if executed directly

# Gotcha: __name__ is '__main__' in the main script
# But modules imported also have __name__ set

# Another gotcha: multiprocessing on Windows
# The if __name__ guard is REQUIRED for multiprocessing on Windows
# from multiprocessing import Process
# if __name__ == '__main__':
#     p = Process(target=func)
#     p.start()

# Testing gotcha:
# Some unit tests set __name__ = '__main__' which can cause issues
```

### Q519: What is the difference between `@staticmethod` and `@classmethod`?
**Answer:**
```python
class A:
    def instance_method(self):
        return "instance", self

    @classmethod
    def class_method(cls):
        return "class", cls

    @staticmethod
    def static_method():
        return "static"

a = A()
print(a.instance_method())  # ('instance', <A object>)
print(a.class_method())     # ('class', <class 'A'>)
print(a.static_method())    # 'static'

# classmethod receives cls, staticmethod receives nothing special

# Inheritance difference:
class B(A):
    pass

b = B()
print(b.class_method())     # ('class', <class 'B'>) <- cls is B, not A
print(b.static_method())    # 'static'

# classmethod is commonly used for alternative constructors:
class Date:
    def __init__(self, year, month, day):
        self.date = f"{year}-{month:02d}-{day:02d}"

    @classmethod
    def from_string(cls, date_str):
        year, month, day = map(int, date_str.split('-'))
        return cls(year, month, day)

d = Date.from_string("2026-06-24")
print(d.date)  # "2026-06-24"
```

### Q520: How does negative indexing work in Python?
**Answer:**
```python
# Negative indices count from the end
lst = [10, 20, 30, 40, 50]

print(lst[-1])  # 50 (last element)
print(lst[-2])  # 40
print(lst[-5])  # 10 (first element)
# print(lst[-6])  # IndexError

# Slicing with negative indices:
print(lst[-3:-1])   # [30, 40]
print(lst[-3:])     # [30, 40, 50]
print(lst[:-2])     # [10, 20, 30]
print(lst[::-1])    # [50, 40, 30, 20, 10] (reverse)
print(lst[-2::-1])  # [40, 30, 20, 10]

# Negative step:
print(lst[4:2:-1])  # [50, 40]
print(lst[::-2])    # [50, 30, 10]

# Gotcha: slice indices are clamped, direct access is not
lst = [1, 2, 3]
print(lst[5:])   # [] (clamped to empty)
# print(lst[5])  # IndexError (not clamped)
```

### Q521: What is the difference between `round` and bank rounding?
**Answer:**
```python
# Python 3 uses "banker's rounding" (round half to even)
print(round(2.5))   # 2 (rounds to even)
print(round(3.5))   # 4 (rounds to even)
print(round(2.4))   # 2
print(round(2.6))   # 3

# This differs from Python 2 (round half away from zero)
# and from most mathematical expectations

# For traditional rounding:
import math
def round_half_up(x):
    return math.floor(x + 0.5)

print(round_half_up(2.5))  # 3
print(round_half_up(3.5))  # 4

# Using Decimal:
from decimal import Decimal, ROUND_HALF_UP
print(Decimal('2.5').quantize(Decimal('1'), rounding=ROUND_HALF_UP))  # 3

# round with ndigits:
print(round(3.14159, 2))  # 3.14
print(round(3.14159, 3))  # 3.142
print(round(12345, -2))   # 12300 (round to hundreds)
print(round(12345, -3))   # 12000 (round to thousands)
```

### Q522: What are Python's `__slots__` pitfalls?
**Answer:**
```python
class MyClass:
    __slots__ = ('x', 'y')

obj = MyClass()
obj.x = 10  # OK
print(obj.x)  # 10
# obj.z = 20  # AttributeError: 'MyClass' object has no attribute 'z'

# Slots prevent __dict__ creation, saving memory
print(hasattr(obj, '__dict__'))  # False

# But this causes issues:
# 1. Can't add new attributes dynamically
# 2. Can't pickle by default (need __getstate__)
# 3. Inheritance quirks

# Inheritance:
class Base:
    __slots__ = ('a',)

class Child(Base):
    pass

c = Child()
c.a = 1   # OK
c.b = 2   # OK (Child has __dict__ because no __slots__)

# To add slots in child:
class Child2(Base):
    __slots__ = ('c',)

c2 = Child2()
c2.a = 1  # OK
c2.c = 2  # OK
# c2.d = 3  # AttributeError

# Multiple inheritance requires slots in all classes or none
```

### Q523: How does `super()` work with multiple inheritance?
**Answer:**
```python
class A:
    def __init__(self):
        print("A")

class B(A):
    def __init__(self):
        print("B")
        super().__init__()

class C(A):
    def __init__(self):
        print("C")
        super().__init__()

class D(B, C):
    def __init__(self):
        print("D")
        super().__init__()

d = D()
# D
# B
# C
# A

# MRO: D -> B -> C -> A
print(D.__mro__)

# super() follows MRO, not just parent
# This enables cooperative multiple inheritance

# Problem: if A doesn't call super(), chain breaks
class A:
    def __init__(self):
        print("A")  # No super() call

class B(A):
    def __init__(self):
        print("B")
        super().__init__()

class C(A):
    def __init__(self):
        print("C")
        super().__init__()

# C's super() goes to A, not to B because B hasn't been called yet
```

### Q524: What is the difference between `__str__` and `__repr__`?
**Answer:**
```python
import datetime

now = datetime.datetime.now()
print(str(now))   # "2026-06-24 12:30:00.123456" (readable)
print(repr(now))  # "datetime.datetime(2026, 6, 24, 12, 30, 0, 123456)" (unambiguous)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p = Point(3, 4)
print(str(p))    # (3, 4)
print(repr(p))   # Point(3, 4)
print(p)         # (3, 4) (print uses str)

# If __str__ is missing, Python falls back to __repr__
class NoStr:
    def __repr__(self):
        return "<NoStr object>"

print(NoStr())  # <NoStr object> (used __repr__ as fallback)

# Convention: __repr__ should be unambiguous, __str__ should be readable
# __repr__ should ideally be valid Python to recreate the object
```

### Q525: What is the `global` and `nonlocal` scope gotcha?
**Answer:**
```python
# global: access/modify variable in module scope
x = 10
def modify():
    global x
    x = 20
modify()
print(x)  # 20

# nonlocal: access/modify variable in enclosing scope
def outer():
    x = "outer"
    def inner():
        nonlocal x
        x = "inner"
    inner()
    print(x)  # "inner"

outer()

# Common gotcha: assignment creates local variable
x = 10
def test():
    print(x)  # UnboundLocalError!
    x = 5

# Why: Python sees x = 5 and treats x as local throughout the function
# The print statement tries to access a local variable before assignment

# Fix:
x = 10
def test():
    global x
    print(x)  # 10
    x = 5
```

### Q526: What is the `for` loop variable leak in generator expressions?
**Answer:**
```python
# In Python 2, list comprehensions leaked variables
# In Python 3, list comprehensions don't leak

# But generator expressions still don't leak:
gen = (x for x in range(3))
# print(x)  # NameError in Python 3

# However, there's a gotcha with closures in loops:
def make_counters():
    counters = []
    for i in range(3):
        def counter():
            return i
        counters.append(counter)
    return counters

for c in make_counters():
    print(c())  # 2, 2, 2 (late binding)

# Fix:
def make_counters():
    counters = []
    for i in range(3):
        def counter(i=i):  # Default argument binds early
            return i
        counters.append(counter)
    return counters

for c in make_counters():
    print(c())  # 0, 1, 2
```

### Q527: What is the `__del__` destructor gotcha?
**Answer:**
```python
import gc

class MyClass:
    def __del__(self):
        print(f"Deleting {self}")

# __del__ is called when reference count reaches 0
obj = MyClass()
del obj  # prints "Deleting ..."

# Circular references prevent immediate deletion
a = MyClass()
b = MyClass()
a.ref = b
b.ref = a
del a, b  # __del__ NOT called yet (circular reference)
gc.collect()  # Now __del__ is called

# __del__ pitfalls:
# 1. Not guaranteed to be called (program exit, exception in __del__)
# 2. Can cause resurrection (if __del__ stores reference to self)
# 3. Objects referenced in __del__ may already be collected
# 4. Exception in __del__ is silently ignored (prints to stderr)

# Better: use context managers (with statement)
class Resource:
    def __enter__(self): return self
    def __exit__(self, *args): self.close()
    def close(self): print("Resource closed")

with Resource() as r:
    pass  # Resource closed deterministically
```

### Q528: How does Python handle `except` and `finally` with return?
**Answer:**
```python
# finally always executes, even if there's a return
def test():
    try:
        return "from try"
    finally:
        print("finally runs")
        # return "from finally"  # This would override!

print(test())  # "from try", but "finally runs" printed first

# If finally has a return, it overrides try/except returns:
def test2():
    try:
        return "from try"
    finally:
        return "from finally"

print(test2())  # "from finally" (overrides!)

# except + finally:
def test3():
    try:
        1 / 0
    except ZeroDivisionError:
        return "from except"
    finally:
        print("finally runs")

print(test3())  # "from except" (finally prints first)

# finally also runs even if exception is not caught:
def test4():
    try:
        raise ValueError("error")
    finally:
        print("finally runs")
    # Exception propagates after finally

# test4()  # ValueError after "finally runs"
```

### Q529: What is the `__init_subclass__` vs metaclass gotcha?
**Answer:**
```python
# __init_subclass__ is called when a class inherits
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"Subclass {cls.__name__} created")

class Child(Base):  # prints "Subclass Child created"
    pass

# Gotcha: __init_subclass__ is NOT called for Base itself
# Only for subclasses

# Metaclass __new__ is called for every class creation
class Meta(type):
    def __new__(mcs, name, bases, namespace):
        print(f"Class {name} created via metaclass")
        return super().__new__(mcs, name, bases, namespace)

# Gotcha: metaclass is inherited but __init_subclass__ can conflict

# Both can exist:
class BaseWithMeta(metaclass=Meta):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"In __init_subclass__: {cls.__name__}")

class Child2(BaseWithMeta): pass
# Order: Meta.__new__ first, then __init_subclass__
```

### Q530: What are Python's truthiness rules?
**Answer:**
```python
# Falsy values:
print(bool(False))   # False
print(bool(None))    # False
print(bool(0))       # False
print(bool(0.0))     # False
print(bool(""))      # False
print(bool([]))      # False
print(bool({}))      # False
print(bool(set()))   # False
print(bool(()))      # False
print(bool(0j))      # False

# Truthy values:
print(bool(True))    # True
print(bool(1))       # True
print(bool(-1))      # True
print(bool(" "))     # True (non-empty string)
print(bool([0]))     # True (non-empty list)
print(bool(float('inf')))  # True

# Custom class truthiness:
class MyClass:
    def __bool__(self):
        return False  # Custom truthiness

print(bool(MyClass()))  # False

# If __bool__ not defined, Python uses __len__
class MyList:
    def __init__(self, items):
        self.items = items
    def __len__(self):
        return len(self.items)

print(bool(MyList([])))    # False (len=0)
print(bool(MyList([1])))   # True (len>0)

# Common gotcha:
if some_list:  # Pythonic way to check non-empty
    pass
if len(some_list) > 0:  # Works but less Pythonic
    pass
```

### Q531: How does Python's `__eq__` behave with inheritance?
**Answer:**
```python
class A:
    def __eq__(self, other):
        if isinstance(other, A):
            return True
        return NotImplemented

class B(A):
    def __eq__(self, other):
        if isinstance(other, B):
            return True
        return NotImplemented

a = A()
b = B()
print(a == b)  # True? False? Depends on Python version

# Python 3: returns NotImplemented
# Python checks reversed operands (b.__eq__(a))
# B.__eq__ returns NotImplemented (not instance of B)
# Falls back to A.__eq__ which returns True

# Better practice:
class A:
    def __eq__(self, other):
        return type(self) == type(other)

class B(A):
    pass

print(A() == B())  # False (different types)

# __hash__ requirement:
# If __eq__ is defined, __hash__ is set to None
class NoHash:
    def __eq__(self, other):
        return True
# d = {NoHash(): 1}  # TypeError: unhashable type
```

### Q532: What is the `__getattr__` vs `__getattribute__` difference?
**Answer:**
```python
class Test:
    def __init__(self):
        self.x = 10

    def __getattribute__(self, name):
        print(f"__getattribute__ called for {name}")
        return super().__getattribute__(name)

    def __getattr__(self, name):
        print(f"__getattr__ called for {name}")
        return f"default for {name}"

t = Test()

# __getattribute__ is called for EVERY attribute access
print(t.x)  # __getattribute__ called for x -> 10

# If __getattribute__ raises AttributeError, __getattr__ is called
print(t.y)  # __getattribute__ called for y
            # -> AttributeError -> __getattr__ called
            # -> "default for y"

# Gotcha: infinite recursion in __getattribute__
class Bad:
    def __getattribute__(self, name):
        return self.__dict__[name]  # Recursion! (calls __getattribute__)

# Fix: use object.__getattribute__
class Good:
    def __getattribute__(self, name):
        return object.__getattribute__(self, name)
```

### Q533: What is the difference between `del`, `remove`, and `pop`?
**Answer:**
```python
lst = [10, 20, 30, 40, 30]

# del: removes by index
del lst[1]
print(lst)  # [10, 30, 40, 30]

# remove: removes by value (first occurrence)
lst.remove(30)
print(lst)  # [10, 40, 30] (only first 30 removed)

# pop: removes and returns by index (default last)
last = lst.pop()
print(last)  # 30
print(lst)   # [10, 40]

first = lst.pop(0)
print(first)  # 10
print(lst)    # [40]

# Gotchas:
# remove raises ValueError if element not found
# pop raises IndexError if index out of range
# del can also delete slices: del lst[1:3]

# For dict:
d = {"a": 1, "b": 2, "c": 3}
del d["a"]      # Remove by key
value = d.pop("b")  # Remove and return
print(d)        # {"c": 3}
print(value)    # 2
```

### Q534: How does Python handle multiple inheritance and method resolution?
**Answer:**
```python
class A:
    def method(self): return "A"

class B(A):
    def method(self): return "B"

class C(A):
    def method(self): return "C"

class D(B, C):
    pass

d = D()
print(d.method())  # "B" (MRO: D->B->C->A)

# MRO is D -> B -> C -> A
print(D.__mro__)

# C3 linearization:
# L[D] = D + merge(L[B], L[C], [B, C])
# L[B] = B, A, object
# L[C] = C, A, object
# merge: take B (head of first list), check it's not in tail of others
# B is not in [C, A] or [C] -> take B
# Now: L[D] = D, B + merge(A, L[C], [C])
# A is in tail of L[C] (C, A, object) -> skip, take C
# L[D] = D, B, C + merge(A, A, [])
# Take A
# L[D] = D, B, C, A, object

# Diamond inheritance:
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
# D -> B -> C -> A -> object
```

### Q535: What is the `array` vs `list` performance difference?
**Answer:**
```python
import array
import sys
import time

# Memory efficiency
int_list = list(range(1000))
int_array = array.array('i', range(1000))

print(f"List: {sys.getsizeof(int_list)} bytes")
print(f"Array: {sys.getsizeof(int_array)} bytes")  # ~4x smaller

# Type restriction
int_array.append(42)     # OK
# int_array.append("hi") # TypeError

# Performance
n = 10**7
start = time.time()
sum(list(range(n)))
print(f"List sum: {time.time() - start:.3f}s")

start = time.time()
sum(array.array('i', range(n)))
print(f"Array sum: {time.time() - start:.3f}s")  # Usually similar or faster

# When to use array:
# - Large homogeneous numeric data
# - Memory constrained
# - Interop with C/other languages

# When to use list:
# - Heterogeneous data
# - Need flexibility (append different types)
# - Small collections
```

### Q536: How does Python's `with` statement handle multiple exceptions?
**Answer:**
```python
from contextlib import contextmanager

@contextmanager
def managed():
    print("Enter")
    try:
        yield
    except ValueError:
        print("Caught ValueError in context manager")
        # NOT re-raised (suppressed)
    except TypeError:
        print("Caught TypeError in context manager")
        # NOT re-raised (suppressed)
    finally:
        print("Exit")

# Exception is suppressed by the context manager
with managed():
    raise ValueError("test")
# Enter -> Caught ValueError -> Exit

# What __exit__ returns matters:
class Suppressor:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print("Suppressed ValueError")
            return True  # Suppress exception
        return False  # Don't suppress

with Suppressor():
    raise ValueError("won't propagate")
    print("This won't print but exception is suppressed")

with Suppressor():
    raise TypeError("will propagate")
    # TypeError propagates because __exit__ returned False
```

### Q537: What is the difference between `sort` and `sorted`?
**Answer:**
```python
# sort(): in-place, returns None
lst = [3, 1, 4, 1, 5]
result = lst.sort()
print(lst)     # [1, 1, 3, 4, 5]
print(result)  # None (gotcha!)

# sorted(): returns new list, original unchanged
lst = [3, 1, 4, 1, 5]
result = sorted(lst)
print(lst)     # [3, 1, 4, 1, 5] (unchanged)
print(result)  # [1, 1, 3, 4, 5] (new list)

# Reverse:
lst.sort(reverse=True)
sorted(lst, reverse=True)

# Key functions:
words = ["apple", "banana", "cherry", "date"]
words.sort(key=len)
print(words)  # ['date', 'apple', 'banana', 'cherry']

# Stability: Python sort is stable
pairs = [(1, 'b'), (2, 'a'), (1, 'a')]
pairs.sort()
print(pairs)  # [(1, 'b'), (1, 'a'), (2, 'a')]
# (1, 'b') before (1, 'a') because original order preserved

# Custom sort with - operator trick:
items = [(1, 10), (2, 5), (3, 8)]
items.sort(key=lambda x: x[1])  # Sort by second element
print(items)  # [(2, 5), (3, 8), (1, 10)]
```

### Q538: What is the `@lru_cache` gotcha with mutable arguments?
**Answer:**
```python
from functools import lru_cache

# lru_cache arguments must be hashable
# Lists, dicts, sets are NOT hashable

@lru_cache(maxsize=128)
def process_list(lst):
    return sum(lst)

# process_list([1, 2, 3])  # TypeError: unhashable type: 'list'

# Fix: use tuple instead
@lru_cache(maxsize=128)
def process_tuple(tpl):
    return sum(tpl)

print(process_tuple((1, 2, 3)))  # 6 (cached)

# Another gotcha: lru_cache with instance methods
class MyClass:
    def __init__(self, value):
        self.value = value

    @lru_cache(maxsize=128)
    def compute(self, x):
        return self.value + x

# Problem: self is included in cache key
# Different instances have different memory addresses
# Cache won't be shared between instances

# Fix: make method a staticmethod or move cache outside
# Or use __repr__/__hash__ properly implemented on the class
```

### Q539: How does Python's `for` loop behave with `range` vs list?
**Answer:**
```python
# range is lazy (generates on the fly)
import sys

r = range(10**6)
lst = list(range(10**6))

print(sys.getsizeof(r))    # 48 bytes (always same)
print(sys.getsizeof(lst))  # ~8MB (stores all elements)

# range supports O(1) indexing and contains
print(500000 in r)   # True (O(1) - calculated)
print(500000 in lst) # True (O(n) - scans)

# range only supports integers
# r[0.5]  # TypeError

# range slicing creates a new range:
r2 = r[10:20]
print(r2)   # range(10, 20)
print(list(r2))  # [10, 11, ..., 19]

# Gotcha: range doesn't support negative step with empty start
print(list(range(5, 1)))    # [] (step defaults to 1, not decreasing)
print(list(range(5, 1, -1))) # [5, 4, 3, 2]
```

### Q540: What is the difference between `bytes`, `bytearray`, and `memoryview`?
**Answer:**
```python
# bytes: immutable
b = b"hello"
# b[0] = 72  # TypeError: 'bytes' object does not support item assignment

# bytearray: mutable
ba = bytearray(b"hello")
ba[0] = 72  # OK
print(ba)  # bytearray(b'Hello')

# memoryview: shared memory access (no copy)
data = bytearray(b"hello world")
mv = memoryview(data)
mv[0] = 72  # Modifies original data
print(data)  # bytearray(b'Hello world')

# memoryview slicing doesn't copy:
slice_mv = mv[0:5]
print(slice_mv.tolist())  # [72, 101, 108, 108, 111]
# Modifying slice_mv modifies original data

# Casting views:
import array
arr = array.array('i', [1, 2, 3, 4])
mv = memoryview(arr)
mv2 = mv.cast('B')  # Cast to bytes view
print(mv2.tolist())  # Byte representation of integers

# Performance: memoryview avoids copying large data
```

### Q541: What is the GIL and how does `multiprocessing` bypass it?
**Answer:**
```python
import threading
import multiprocessing
import time

def cpu_bound(n):
    return sum(i * i for i in range(n))

# Threads: GIL prevents parallel execution for CPU-bound
def threaded():
    threads = [threading.Thread(target=cpu_bound, args=(10**7,)) for _ in range(4)]
    start = time.time()
    for t in threads: t.start()
    for t in threads: t.join()
    return time.time() - start

# Processes: bypass GIL (separate processes)
def process():
    with multiprocessing.Pool(4) as pool:
        start = time.time()
        pool.map(cpu_bound, [10**7] * 4)
        return time.time() - start

# print(f"Threads: {threaded():.2f}s")   # ~2-3x slower than sequential
# print(f"Process: {process():.2f}s")    # ~4x faster on 4 cores

# GIL is per-process, so multiprocessing has separate GILs
# Process overhead: memory (separate address space), IPC cost

# NumPy releases GIL for computation:
import numpy as np
# np.sum(np.array(range(10**7)))  # GIL released during computation
```

### Q542: What is the `__all__` variable in modules?
**Answer:**
```python
# __all__ controls what from module import * exports

# mymodule.py
# __all__ = ['public_func', 'PublicClass']
#
# def public_func(): pass
# def _private_func(): pass
# class PublicClass: pass

# With __all__, only those names are exported
# Without __all__, everything except _prefixed is exported

# __all__ is a convention, not enforced:
# from module import _private_func  # Still works (explicit import)

# Gotcha: __all__ doesn't affect attribute access
# module.public_func  # Works
# module._private_func  # Works (if you know it exists)

# __all__ in __init__.py controls package exports
# from package import *  # Uses __all__ from __init__.py
```

### Q543: How does Python's `__name__` affect import behavior?
**Answer:**
```python
# __name__ == '__main__' for the entry point script
# __name__ == 'module.name' for imported modules

# Gotcha: running a module as script changes import behavior

# File: mymodule.py
# if __name__ == '__main__':
#     main()

# Running: python mymodule.py -> main() executes
# Running: python -c "import mymodule" -> main() does NOT execute

# Gotcha: pickle requires importable module
import pickle

def func():
    return 42

# This works because func is in __main__
# But when unpickling from another process, func must be importable
# Pickle only stores the fully qualified name

# Fix: define functions in importable modules, not in __main__
# class MyClass: pass
# import mymodule
# obj = mymodule.MyClass()
# pickle.dumps(obj)  # Works because MyClass is in mymodule

# Gotcha: relative imports fail in __main__
# python -m package.module  # Works (correct __package__)
# python package/module.py  # Fails (__package__ is None)
```

### Q544: What is the walrus operator `:=` gotchas?
**Answer:**
```python
# Walrus operator (Python 3.8+): assign and evaluate

# Useful in comprehensions:
[expensive(x) for x in data if expensive(x) > 0]
# vs:
[val for x in data if (val := expensive(x)) > 0]

# Gotcha 1: operator precedence
print(x := 5)  # 5 (works)
# print(x = 5)  # SyntaxError

# Precedence: := is lower than comparison, arithmetic, etc.
# if (x := len(s)) > 5:  # Need parens
# if x := len(s) > 5:    # x = bool (len(s) > 5), not int!

# Gotcha 2: walrus in f-strings (Python 3.8+ f-strings)
# f"{(x := 5)}"  # Works in Python 3.8+ f-strings

# Gotcha 3: walrus in lambda
# lambda: (x := 5)  # Works
# lambda: x := 5   # SyntaxError

# Gotcha 4: walrus with assignment target
# (x := 5)  # OK
# (x, y := 5, 6)  # SyntaxError
# ((x, y) := (5, 6))  # SyntaxError (cannot unpack)

# Practical use: while loop
while (chunk := file.read(8192)):
    process(chunk)
```

### Q545: What is the difference between `__len__` and `__bool__`?
**Answer:**
```python
class MyContainer:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

    def __bool__(self):
        return len(self.items) > 0

c = MyContainer([])
print(bool(c))  # False (via __bool__)
print(len(c))   # 0

# If __bool__ is not defined, Python falls back to __len__
class OnlyLen:
    def __init__(self, items):
        self.items = items
    def __len__(self):
        return len(self.items)

print(bool(OnlyLen([])))    # False (len=0)
print(bool(OnlyLen([1])))   # True (len>0)

# Both defined: __bool__ takes precedence
class Both:
    def __len__(self): return 100
    def __bool__(self): return False

print(bool(Both()))  # False (__bool__ wins)

# Performance: bool check is faster than len check
# bool([]) uses __bool__ or __len__ directly (no method call overhead)
```

### Q546: How does Python's `int` handle arbitrarily large numbers?
**Answer:**
```python
import sys

# Python 3: arbitrary precision integers
small = 42
print(type(small))            # <class 'int'>
print(sys.getsizeof(small))   # 28 bytes

large = 2**1000
print(len(str(large)))        # 302 digits
print(sys.getsizeof(large))   # 160 bytes (grows with number)

# Operations work as expected:
print(2**10000)  # 3011-digit number

# But performance degrades:
import time
start = time.time()
result = 2**100000  # ~30k digits
print(f"Time: {time.time() - start:.4f}s")

# Bit operations also work on large ints:
x = 1 << 1000  # 2^1000 via bit shift
print(x.bit_length())  # 1001

# int.bit_count() (Python 3.8+): count set bits
print((12345).bit_count())  # Number of 1 bits in binary

# int.to_bytes / int.from_bytes:
b = (255).to_bytes(4, 'big')
print(b)  # b'\x00\x00\x00\xff'
print(int.from_bytes(b, 'big'))  # 255
```

### Q547: What are Python's `__init__` vs `__new__` differences?
**Answer:**
```python
# __new__: creates the object (returns instance)
# __init__: initializes the object (returns None)

class Point:
    def __new__(cls, x, y):
        print(f"__new__ called with ({x}, {y})")
        instance = super().__new__(cls)
        return instance

    def __init__(self, x, y):
        print(f"__init__ called with ({x}, {y})")
        self.x = x
        self.y = y

p = Point(3, 4)
# __new__ called with (3, 4)
# __init__ called with (3, 4)

# __new__ is used for:
# 1. Immutable types (int, str, tuple)
class ConstPoint(tuple):
    def __new__(cls, x, y):
        return super().__new__(cls, (x, y))

c = ConstPoint(3, 4)
print(c)  # (3, 4)
# c.x = 5  # TypeError (immutable)

# 2. Singleton pattern
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# 3. Metaclass customizations
# __init__ can't return anything (must be None)
# __new__ must return an instance (or None)
```

### Q548: How does Python's `@property` work with inheritance?
**Answer:**
```python
class Base:
    @property
    def value(self):
        return "base"

class Child(Base):
    @property
    def value(self):
        return "child"

print(Base().value)   # "base"
print(Child().value)  # "child"

# Overriding just the getter:
class Child2(Base):
    @Base.value.getter
    def value(self):
        return "child2"

print(Child2().value)  # "child2"

# Overriding just the setter:
class Person:
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

class Employee(Person):
    @Person.name.setter
    def name(self, value):
        print(f"Setting name to {value}")
        super(Employee, Employee).name.__set__(self, value)

# But properties are lazily evaluated - careful with exceptions:
class Lazy:
    @property
    def expensive(self):
        print("Computing...")
        return 42

l = Lazy()
print(l.expensive)  # "Computing..." then 42
print(l.expensive)  # "Computing..." then 42 (no cache!)
```

### Q549: What is the difference between `__class_getitem__` and `__getitem__`?
**Answer:**
```python
# __getitem__: instance method for obj[key]
# __class_getitem__: class method for Class[Type] (parameterized generics)

class MyList:
    def __getitem__(self, index):
        return f"item {index}"

ml = MyList()
print(ml[0])  # "item 0" (via __getitem__)

# __class_getitem__ enables generic syntax:
class MyGeneric:
    def __class_getitem__(cls, item):
        return f"Generic[{item}]"

print(MyGeneric[int])  # "Generic[int]"
print(MyGeneric[str])  # "Generic[str]"

# This is how typing.List[int] works under the hood:
from typing import List
print(List[int])  # list[int] (via __class_getitem__)

# Custom generic class:
class Box:
    def __class_getitem__(cls, item):
        # Return a dynamically created subclass
        new_class = type(f"{cls.__name__}[{item.__name__}]", (cls,), {"_type": item})
        return new_class

# Box[int]  # Creates Box[int] class with _type = int
```

### Q550: What are common Python performance gotchas?
**Answer:**
```python
import time

# 1. String concatenation in loops (O(n^2))
start = time.time()
s = ""
for i in range(10000):
    s += str(i)
print(f"String concat: {time.time() - start:.4f}s")
# Fix: ''.join()
start = time.time()
s = ''.join(str(i) for i in range(10000))
print(f"Join: {time.time() - start:.4f}s")

# 2. Attribute lookup in loops
class A:
    def __init__(self):
        self.x = 42

a = A()
start = time.time()
for _ in range(10**6):
    _ = a.x
print(f"Attribute: {time.time() - start:.4f}s")
# Fix: local variable binding
x = a.x
start = time.time()
for _ in range(10**6):
    _ = x
print(f"Local: {time.time() - start:.4f}s")

# 3. Using list when set is appropriate
# x in [1,2,3] -> O(n) vs x in {1,2,3} -> O(1)

# 4. Repeated len() calls
# for i in range(len(lst)):  # Avoid
# for item in lst:           # Better

# 5. Deep copy large structures
# import copy
# large = [[1]*1000 for _ in range(1000)]
# copy.deepcopy(large)  # Slow for large structures
```

