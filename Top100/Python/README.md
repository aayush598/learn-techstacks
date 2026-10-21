# Python Interview Questions and Answers

## Q1: What is Python?
**A:** Python is a high-level, interpreted, general-purpose programming language created by Guido van Rossum and first released in 1991. It emphasizes code readability through significant indentation and supports multiple programming paradigms including procedural, object-oriented, and functional programming.
**Code:**
```python
print("Hello, world!")  # high-level, readable, general-purpose
```

## Q2: What are Python's key features?
**A:** Key features include: interpreted nature (no compilation step), dynamically typed, garbage collected, large standard library, support for multiple paradigms, extensive package ecosystem (PyPI), cross-platform compatibility, and strong community support.
**Code:**
```python
x = 5
x = "now a string"          # dynamic typing
print(x.upper(), len(x))    # batteries included (stdlib)
```

## Q3: Explain the difference between list and tuple in Python.
**A:** Lists are mutable (can be modified after creation), defined with square brackets `[]`, and are slower than tuples. Tuples are immutable (cannot be modified), defined with parentheses `()`, and can be used as dictionary keys. Tuples are generally faster due to immutability.
**Code:**
```python
lst = [1, 2]
lst.append(3)          # list is mutable
tup = (1, 2)           # tuple is immutable
print(lst, tup)
d = {tup: "tuple key"}   # tuples are hashable -> dict keys
```

## Q4: What is PEP 8?
**A:** PEP 8 is Python's official style guide. It provides conventions for writing readable Python code, including indentation (4 spaces), line length (79 characters), naming conventions (snake_case for variables/functions, CamelCase for classes), and whitespace usage.
**Code:**
```python
def calculate_total(items):   # snake_case function
    total = 0               # 4-space indentation
    for item in items:
        total += item
    return total

print(calculate_total([1, 2, 3, 4]))
```

## Q5: What are Python decorators?
**A:** Decorators are functions that modify the behavior of other functions or methods. They use the `@decorator` syntax and are commonly used for logging, access control, memoization, and timing. A decorator takes a function as input, wraps it with additional functionality, and returns the wrapped function.
**Code:**
```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    return a + b

add(2, 3)
```

## Q6: Explain the Global Interpreter Lock (GIL).
**A:** The GIL is a mutex in CPython that prevents multiple native threads from executing Python bytecode simultaneously. It simplifies memory management and makes single-threaded code faster, but limits CPU-bound parallelism in multi-threaded programs. For true parallelism, use multiprocessing or async I/O.
**Code:**
```python
import threading, time

def work():
    time.sleep(1)              # I/O-bound: GIL released, thread can run

t1 = threading.Thread(target=work)   # GIL lets one thread run bytecode at a time
t2 = threading.Thread(target=work)
t1.start(); t2.start(); t1.join(); t2.join()
print("done")
```

## Q7: What is the difference between `deepcopy` and `shallow copy`?
**A:** Shallow copy creates a new object but inserts references to the original nested objects. Deep copy creates a new object and recursively copies all nested objects. `copy.copy()` does shallow copy, `copy.deepcopy()` does deep copy. Changes to nested objects in a shallow copy affect the original.
**Code:**
```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

shallow[0].append(99)     # shallow: inner object is shared
print(original)           # [[1, 2, 99], [3, 4]]
print(deep)               # [[1, 2], [3, 4]] unaffected
```

## Q8: How does Python manage memory?
**A:** Python uses automatic memory management with reference counting and a garbage collector. Each object has a reference count; when it reaches zero, memory is deallocated. The garbage collector handles circular references that reference counting can't resolve. The `gc` module provides control over the garbage collector.
**Code:**
```python
import sys
x = []
print(sys.getrefcount(x) - 1)   # references to x
del x                           # refcount reaches 0 -> deallocated

import gc
gc.collect()                    # handles circular references
```

## Q9: What are *args and **kwargs?
**A:** `*args` allows a function to accept any number of positional arguments as a tuple. `**kwargs` allows a function to accept any number of keyword arguments as a dictionary. They're often used in decorators, function wrappers, and when delegating arguments to other functions.
**Code:**
```python
def intro(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)

intro(1, 2, name="Alice", age=30)
# args: (1, 2)   kwargs: {'name': 'Alice', 'age': 30}
```

## Q10: Explain list comprehensions with an example.
**A:** List comprehensions provide a concise way to create lists. Syntax: `[expression for item in iterable if condition]`. Example: `[x**2 for x in range(10) if x % 2 == 0]` produces `[0, 4, 16, 36, 64]`. They're faster than traditional for loops for creating lists.
**Code:**
```python
squares = [x**2 for x in range(10) if x % 2 == 0]
print(squares)   # [0, 4, 16, 36, 64]
```

## Q11: What is a lambda function?
**A:** A lambda function is an anonymous, one-line function defined with the `lambda` keyword. Syntax: `lambda arguments: expression`. Example: `lambda x, y: x + y`. Lambdas are limited to single expressions and are commonly used with `map()`, `filter()`, and `sorted()`.
**Code:**
```python
add = lambda x, y: x + y          # anonymous single-expression function
print(add(2, 3))

words = ["banana", "apple", "cherry"]
print(sorted(words, key=lambda w: len(w)))   # uses lambda as key
```

## Q12: How do you handle exceptions in Python?
**A:** Exceptions are handled using `try`, `except`, `else`, and `finally` blocks. `try` contains code that may raise an exception. `except` catches specific exceptions. `else` runs if no exception occurred. `finally` always executes, typically for cleanup. Custom exceptions can be created by subclassing `Exception`.
**Code:**
```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print("caught:", e)
else:
    print("no error")
finally:
    print("always runs")
```

## Q13: What is the difference between `is` and `==`?
**A:** `==` checks value equality (whether objects have the same value). `is` checks identity equality (whether two variables reference the same object in memory). For small integers (-5 to 256) and small strings, Python may intern objects, making `is` behave like `==`.
**Code:**
```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)   # True  - value equality
print(a is b)   # False - different objects
print(256 is 256)  # True - small ints are interned
```

## Q14: Explain Python's `with` statement and context managers.
**A:** The `with` statement manages resources like files, locks, and database connections by ensuring proper acquisition and release. Context managers implement `__enter__` and `__exit__` methods. Example: `with open('file.txt') as f:` automatically closes the file when done, even if exceptions occur.
**Code:**
```python
with open("demo.txt", "w") as f:   # __enter__ opens, __exit__ closes
    f.write("hello")
# f is automatically closed, even if an exception occurs
```

## Q15: What are Python generators?
**A:** Generators are functions that use `yield` instead of `return` to produce a sequence of values lazily. They maintain state between iterations and don't store all values in memory. Generators are memory-efficient for large datasets and can be created with generator expressions: `(x**2 for x in range(1000000))`.
**Code:**
```python
def countdown(n):
    while n > 0:
        yield n            # generator: lazy sequence
        n -= 1

print(list(countdown(3)))              # [3, 2, 1]
print(sum(x**2 for x in range(5)))     # generator expression: 30
```

## Q16: What is the difference between `__str__` and `__repr__`?
**A:** `__repr__` aims for an unambiguous representation of an object, ideally one that can recreate the object. `__str__` aims for a readable representation for end-users. If `__str__` is not defined, `__repr__` is used as fallback. `repr()` calls `__repr__`, `str()` and `print()` call `__str__`.
**Code:**
```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):                     # unambiguous, dev-facing
        return f"Point({self.x}, {self.y})"
    def __str__(self):                      # readable, user-facing
        return f"({self.x}, {self.y})"

p = Point(1, 2)
print(str(p))    # (1, 2)
print(repr(p))   # Point(1, 2)
```

## Q17: Explain method resolution order (MRO) in Python.
**A:** MRO defines the order in which Python searches for methods in a class hierarchy. For single inheritance, it's the chain of classes. For multiple inheritance, Python uses the C3 linearization algorithm. MRO can be viewed with `ClassName.__mro__` or `ClassName.mro()`. It ensures each class is visited only once.
**Code:**
```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print([c.__name__ for c in D.__mro__])
# ['D', 'B', 'C', 'A', 'object']
```

## Q18: What is a Python module and package?
**A:** A module is a single `.py` file containing Python definitions and statements. A package is a directory containing `__init__.py` file and sub-modules or sub-packages. Packages allow hierarchical organization of modules. Modules are imported using `import module_name` or `from module import name`.
**Code:**
```python
import math                      # module: a .py file
from math import sqrt           # import a name directly

print(math.pi)                  # qualify via module
print(sqrt(16))                 # already in this namespace
```

## Q19: How does Python handle type hints?
**A:** Type hints were introduced in Python 3.5 via PEP 484. They allow declaring expected types for variables, function parameters, and return values using syntax like `def func(name: str) -> int:`. Type hints are not enforced at runtime but are used by static type checkers like mypy, IDEs, and linters.
**Code:**
```python
def greet(name: str, age: int = 0) -> str:   # type hints
    return f"{name} ({age})"

print(greet("Ada", 36))
print(greet.__annotations__)
```

## Q20: What is the difference between `classmethod`, `staticmethod`, and instance methods?
**A:** Instance methods take `self` as first parameter and can access/modify instance state. Classmethods take `cls` as first parameter (`@classmethod`) and can access/modify class state. Staticmethods (`@staticmethod`) don't receive self or cls and behave like regular functions but belong to the class namespace.
**Code:**
```python
class Demo:
    cls_data = 0

    def instance_method(self):          # takes self, instance state
        return f"instance {self}"

    @classmethod
    def class_method(cls):              # takes cls, class state
        cls.cls_data += 1
        return cls.cls_data

    @staticmethod
    def static_method():                # no self / cls
        return "static"

d = Demo()
print(d.instance_method())
print(Demo.class_method(), Demo.class_method())
print(Demo.static_method())
```

## Q21: Explain Python's `__slots__`.
**A:** `__slots__` is a class attribute that restricts which attributes instances can have. It saves memory by preventing the creation of `__dict__` per instance. When a class defines `__slots__`, only those attributes can be assigned. It's useful when creating many instances of a class.
**Code:**
```python
class Point:
    __slots__ = ("x", "y")          # fixed attribute set
    def __init__(self, x, y):
        self.x, self.y = x, y

p = Point(1, 2)
print(p.x, p.y)
print(hasattr(p, "__dict__"))       # False -> memory saved
```

## Q22: What are Python metaclasses?
**A:** Metaclasses are classes of classes. A metaclass defines how a class behaves, just as a class defines how instances behave. `type` is the default metaclass. Metaclasses can intercept class creation, modify class attributes, and implement singleton patterns or ORMs. They're an advanced feature rarely needed.
**Code:**
```python
class Meta(type):
    def __new__(mcs, name, bases, ns):
        ns["created_by"] = "metaclass"
        return super().__new__(mcs, name, bases, ns)

class Widget(metaclass=Meta):
    pass

print(Widget.created_by)   # metaclass intercepted class creation
```

## Q23: How do you achieve multithreading in Python?
**A:** Multithreading is achieved using the `threading` module. Threads share the same memory space and are lightweight but limited by the GIL for CPU-bound tasks. The `Thread` class, locks (`Lock`, `RLock`), semaphores, and queues help manage thread synchronization and communication.
**Code:**
```python
import threading

def worker(name):
    print(f"{name} running")

threads = [threading.Thread(target=worker, args=(f"T{i}",)) for i in range(3)]
for t in threads: t.start()
for t in threads: t.join()
```

## Q24: What is the difference between multiprocessing and threading?
**A:** Threading runs in a single process, shares memory, and is limited by the GIL—suitable for I/O-bound tasks. Multiprocessing creates separate processes with independent memory, bypasses the GIL, and is suitable for CPU-bound tasks. Multiprocessing has higher overhead due to process creation and IPC.
**Code:**
```python
import threading
from multiprocessing import Process

def job():
    total = sum(range(1000))
    print(f"computed {total}")

# threads: one process, shared memory, GIL-limited
t = threading.Thread(target=job); t.start(); t.join()

# processes: own memory + GIL, true parallelism
p = Process(target=job); p.start(); p.join()

# Use ProcessPoolExecutor for CPU-bound work in parallel:
from concurrent.futures import ProcessPoolExecutor
if __name__ == "__main__":
    with ProcessPoolExecutor(2) as ex:
        print(list(ex.map(lambda x: x * x, [1, 2, 3, 4])))
```

## Q25: Explain Python's asyncio module.
**A:** `asyncio` provides infrastructure for writing single-threaded concurrent code using coroutines, event loops, and futures. It uses `async def` for coroutines and `await` for yielding control. It's ideal for I/O-bound tasks like web requests, database queries, and network operations without threads or processes.
**Code:**
```python
import asyncio

async def fetch(i):
    await asyncio.sleep(0.1)          # non-blocking wait
    return f"result-{i}"

async def main():
    results = await asyncio.gather(fetch(1), fetch(2))
    print(results)

asyncio.run(main())   # ['result-1', 'result-2']
```

## Q26: What is the difference between `await` and `yield from`?
**A:** `yield from` (Python 3.3+) delegates to a subgenerator in generator-based coroutines. `await` (Python 3.5+) is used with `async def` coroutines and works with awaitables (coroutines, tasks, futures). `await` is more restrictive and designed for asyncio, while `yield from` is more general.
**Code:**
```python
import asyncio

async def inner():
    return "value"

async def outer_await():
    v = await inner()        # await: awaits an awaitable
    return v

print(asyncio.run(outer_await()))   # value

def gen():
    yield from range(3)      # yield from: delegate to a subgenerator

print(list(gen()))   # [0, 1, 2]
```

## Q27: How does Python's `__init__` vs `__new__` work?
**A:** `__new__` is a static method that creates and returns a new object instance (called first). `__init__` initializes the created instance (called after `__new__`). `__new__` is rarely overridden and is used for immutable types or singleton patterns. `__init__` is the common constructor.
**Code:**
```python
class Point:
    def __new__(cls, x, y):          # creates the instance (called first)
        print("__new__")
        return super().__new__(cls)
    def __init__(self, x, y):        # initializes it (after __new__)
        print("__init__")
        self.x, self.y = x, y

p = Point(1, 2)
# __new__
# __init__
```

## Q28: Explain Python's property decorator.
**A:** `@property` allows defining methods that can be accessed like attributes. It's used for getters, setters, and deleters. Example: `@property def name(self):` for getter, `@name.setter` for setter. Properties enable computed attributes, validation, and backward compatibility when refactoring attributes to methods.
**Code:**
```python
class Person:
    def __init__(self, name):
        self._name = name
    @property
    def name(self):                 # getter: accessed like attribute
        return self._name
    @name.setter
    def name(self, value):          # setter with validation
        if not value:
            raise ValueError("empty name")
        self._name = value

p = Person("Ada")
p.name = "Grace"
print(p.name)
```

## Q29: What are Python's built-in data types?
**A:** Mutable types: `list`, `dict`, `set`, `bytearray`. Immutable types: `int`, `float`, `complex`, `str`, `tuple`, `frozenset`, `bytes`, `bool`, `NoneType`. Sequence types: `list`, `str`, `tuple`, `range`. Mapping type: `dict`. Set types: `set`, `frozenset`.
**Code:**
```python
from typing import get_type_hints

mutable = [1, 2]          # list
immutable = (1, 2)        # tuple
mapping = {"a": 1}        # dict
myset = {1, 2, 3}         # set
frozen = frozenset({1})   # frozenset
print(type(mutable), type(immutable), type(mapping), type(myset), type(frozen))
```

## Q30: How do you reverse a list in Python?
**A:** Multiple ways: `list.reverse()` (in-place), `reversed(list)` (returns iterator), `list[::-1]` (creates reversed copy), `list[-1::-1]`. For in-place reversal without modifying original, use slicing `[::-1]` which creates a new list.
**Code:**
```python
lst = [1, 2, 3, 4]

lst.reverse()                # in-place
print(lst)

print(list(reversed([1, 2, 3])))   # iterator
print([1, 2, 3][::-1])            # reversed copy
```

## Q31: What is the difference between `remove`, `del`, and `pop` for lists?
**A:** `remove(x)` removes the first occurrence of value `x`. `del list[i]` removes element at index `i`. `pop(i)` removes and returns element at index `i` (default last). `remove` searches by value, `del` and `pop` work by index. `pop` returns the removed element.
**Code:**
```python
lst = [1, 2, 3, 2]
lst.remove(2)       # removes first occurrence of value 2
print(lst)          # [1, 3, 2]

del lst[1]          # deletes by index
popped = lst.pop()  # removes & returns last item
print(lst, popped)
```

## Q32: Explain Python's garbage collection.
**A:** Python uses reference counting as primary GC (immediate deallocation when refcount hits 0) and a generational cyclic garbage collector (in `gc` module) to handle circular references. The GC divides objects into 3 generations and runs collection when thresholds are exceeded. `gc.collect()` forces collection.
**Code:**
```python
import gc

class Ref:
    pass

a, b = Ref(), Ref()
a.other = b
b.other = a            # circular reference - refcounting can't free these
del a, b

print(gc.collect())    # cyclic collector reclaims them
```

## Q33: What is the walrus operator (:=)?
**A:** Introduced in Python 3.8, the walrus operator `:=` allows assignment within expressions. Example: `if (n := len(x)) > 10:` assigns `len(x)` to `n` and checks the condition. It's useful in list comprehensions and while loops to avoid redundant computations.
**Code:**
```python
values = [1, 2, 3, 4, 5]
if (n := len(values)) > 3:          # walrus: assign within expression
    print(f"list has {n} items")
```

## Q34: How do you merge two dictionaries in Python?
**A:** In Python 3.9+: `dict1 | dict2` (union operator). Older versions: `{**dict1, **dict2}` (unpacking), `dict1.copy(); dict1.update(dict2)`, or `dict(dict1, **dict2)`. Later keys overwrite earlier ones. The `|` operator creates a new dictionary without modifying originals.
**Code:**
```python
d1, d2 = {"a": 1}, {"b": 2}

merged = d1 | d2              # Python 3.9+
print(merged)                 # {'a': 1, 'b': 2}

also = {**d1, **d2}          # older versions
print(also)
```

## Q35: What is monkey patching in Python?
**A:** Monkey patching is dynamically modifying classes or modules at runtime. Example: replacing a method on a class to change its behavior. It's commonly used in testing (mocking), but can make code harder to understand and debug. Frameworks like gevent and eventlet use monkey patching.
**Code:**
```python
class Calc:
    def add(self, a, b):
        return a + b

def fake_add(self, a, b):
    return "mocked"

Calc.add = fake_add            # monkey patch at runtime
print(Calc().add(1, 2))        # mocked
```

## Q36: Explain the difference between `@classmethod`, `@staticmethod`, and `@property`.
**A:** `@classmethod` binds the method to the class, receiving `cls` as first arg. `@staticmethod` is a regular function in the class namespace, doesn't receive `self` or `cls`. `@property` allows a method to be accessed as an attribute, with optional setter/deleter.
**Code:**
```python
class Circle:
    pi = 3.14159

    def _init(self):
        pass

    @classmethod
    def with_diameter(cls, d):      # cls instead of self
        return cls(d / 2)

    @staticmethod
    def how_beautiful():            # no self, no cls
        return "very"

    @property
    def radius(self):               # accessed like an attribute
        return getattr(self, "_r", 0)

c = Circle.with_diameter(4)
print(Circle.how_beautiful(), c.radius)
```

## Q37: What are Python's module search paths?
**A:** Python searches modules in `sys.path`, which includes: the directory of the input script, `PYTHONPATH` environment variable, standard library directories, and paths in `.pth` files. `sys.path` can be modified at runtime. Current directory is first in the search path.
**Code:**
```python
import sys
print(sys.path[0])               # script dir / current dir
# plus PYTHONPATH, stdlib dirs, and .pth paths - all in sys.path
```

## Q38: How do you create a virtual environment in Python?
**A:** Using `python -m venv /path/to/new/venv` (Python 3.3+). This creates a self-contained directory with its own Python interpreter and packages. Activate with `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows). Deactivate with `deactivate`.
**Code:**
```python
import os
# python -m venv /path/to/venv   -> creates isolated interpreter
print(os.popen("python -m venv /tmp/demo_venv").read())
print(os.path.isdir("/tmp/demo_venv/bin"))   # activation script dir
```

## Q39: What is pip and how do you use it?
**A:** pip is Python's package installer. Common commands: `pip install package`, `pip uninstall package`, `pip list`, `pip freeze > requirements.txt`, `pip install -r requirements.txt`. It installs packages from PyPI and manages dependencies with automatic resolution.
**Code:**
```python
import subprocess, sys
# pip install requests, pip freeze > requirements.txt
result = subprocess.run([sys.executable, "-m", "pip", "--version"],
                        capture_output=True, text=True)
print(result.stdout)
```

## Q40: Explain the difference between `requirements.txt` and `setup.py`.
**A:** `requirements.txt` lists dependencies for deployment (pinned versions), used by `pip install -r`. `setup.py` defines package metadata and dependencies for distribution, used with `pip install .` or `python setup.py install`. `setup.py` is for packages meant to be shared; `requirements.txt` is for environments.
**Code:**
```python
# requirements.txt  ->  pip install -r requirements.txt (deployment pins)
#    requests==2.32.0
#
# setup.py  ->  pip install . (package metadata & deps for distribution)

print("pip install -r requirements.txt")
print("pip install .")
```

## Q41: What are Python's `__dunder__` methods?
**A:** Dunder (double underscore) methods are special methods that enable operator overloading and protocol implementation. Examples: `__init__`, `__str__`, `__repr__`, `__len__`, `__eq__`, `__hash__`, `__call__`, `__enter__`, `__exit__`, `__getitem__`, `__iter__`, `__next__`. They're called implicitly by Python.
**Code:**
```python
class Vec:
    def __init__(self, x):
        self.x = x
    def __len__(self):          # supports len(v)
        return 1
    def __str__(self):          # supports str(v) / print(v)
        return f"Vec({self.x})"
    def __add__(self, other):   # supports v + other
        return Vec(self.x + other.x)

v = Vec(3) + Vec(4)
print(len(v), v)
```

## Q42: How does `__hash__` and `__eq__` work together?
**A:** Objects used as dictionary keys or set members must implement `__hash__` (returns integer) and `__eq__` (checks equality). Equal objects must have the same hash. If `__eq__` is overridden, `__hash__` should also be defined or set to `None`. Immutable objects are typically hashable.
**Code:**
```python
class Money:
    def __init__(self, amount):
        self.amount = amount
    def __eq__(self, other):                    # needed for dict/set use
        return isinstance(other, Money) and self.amount == other.amount
    def __hash__(self):                         # same hash for equal objects
        return hash(self.amount)

wallet = {Money(5), Money(5)}
print(len(wallet))      # 1 - equal objects hash alike
```

## Q43: What is the difference between `__getattr__` and `__getattribute__`?
**A:** `__getattribute__` is called unconditionally for every attribute access. `__getattr__` is called only when the attribute is not found through normal mechanisms. `__getattribute__` must be used carefully to avoid infinite recursion. `__getattr__` is simpler for implementing fallback behavior.
**Code:**
```python
class Proxy:
    def __getattr__(self, name):      # only when normal lookup fails
        return f"fallback for {name}"

    def __getattribute__(self, name):  # called for every access
        return super().__getattribute__(name)

p = Proxy()
print(p.anything)      # fallback for anything
```

## Q44: Explain Python's `functools.lru_cache`.
**A:** `lru_cache` is a decorator for memoization. It caches function results based on arguments, using a least-recently-used eviction policy. Syntax: `@functools.lru_cache(maxsize=128)`. Useful for expensive, pure functions. `cache_info()` returns hit/miss statistics. `cache_clear()` clears the cache.
**Code:**
```python
import functools

@functools.lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(30))                   # 832040, cached fast
print(fib.cache_info())
```

## Q45: What is the difference between `__init__.py` and `__main__.py`?
**A:** `__init__.py` makes a directory a Python package and is executed when the package is imported. `__main__.py` allows a package to be run as a script with `python -m package_name`. `__init__.py` can be empty; `__main__.py` typically contains argument parsing and entry point.
**Code:**
```python
# pkg/__init__.py  -> makes pkg a package, runs on import
# pkg/__main__.py   -> allows:  python -m pkg
print("python -m pkg  executes pkg/__main__.py")
```

## Q46: How do you write unit tests in Python?
**A:** Using the `unittest` standard library or `pytest` framework. `unittest` requires test classes inheriting `unittest.TestCase` with `assertEqual`, `assertTrue`, etc. `pytest` uses plain functions with `assert` statements. Tests are discovered by filename patterns (`test_*.py`, `*_test.py`).
**Code:**
```python
import unittest

def add(a, b):
    return a + b

class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertGreater(add(1, 1), 1)

if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
```

## Q47: Explain mocking in Python tests.
**A:** Mocking replaces real objects with test doubles. `unittest.mock` provides `Mock` and `MagicMock` classes. `patch` decorator/context manager temporarily replaces objects during tests. Mocks track calls, return configured values, and can raise exceptions. Useful for isolating tests from external services.
**Code:**
```python
from unittest.mock import Mock, patch

mock = Mock()
mock.fetch.return_value = {"id": 1}
print(mock.fetch())          # {'id': 1}
mock.fetch.assert_called_once()

func = lambda: "real"
with patch("__main__.func", return_value="stubbed"):
    print(func())            # stubbed
```

## Q48: What is the difference between `pytest` and `unittest`?
**A:** `pytest` has simpler syntax (plain functions, plain asserts), auto-discovery, fixtures, parameterization, and extensive plugins. `unittest` is built-in, requires class-based test cases, and has more verbose assertion methods. `pytest` is preferred for new projects and can run `unittest` tests.
**Code:**
```python
import unittest

# pytest style
def test_add():
    assert 1 + 1 == 2

# unittest style
class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)

unittest.main(argv=[""], exit=False)
```

## Q49: How does Python's with statement work internally?
**A:** The `with` statement requires a context manager implementing `__enter__` (acquires resource, returns value assigned by `as`) and `__exit__(self, exc_type, exc_val, exc_tb)` (releases resource, suppresses exception if returns True). The `contextlib` module provides utilities like `contextmanager` decorator and `closing`.
**Code:**
```python
class Managed:
    def __enter__(self):            # acquire resource
        print("enter")
        return self
    def __exit__(self, exc_type, exc, tb):   # release, called even on errors
        print("exit")
        return False                # False -> don't swallow exceptions

with Managed():
    print("inside")
```

## Q50: Explain the difference between `__getitem__` and `__setitem__`.
**A:** `__getitem__(self, key)` is called for index/attribute access like `obj[key]`. `__setitem__(self, key, value)` is called for assignment like `obj[key] = value`. They enable bracket notation for custom classes and are fundamental for creating container-like objects.
**Code:**
```python
class MyDict(dict):
    def __getitem__(self, key):         # obj[key]  read
        print("get", key)
        return super().__getitem__(key)
    def __setitem__(self, key, value):  # obj[key] = value  write
        print("set", key, value)
        super().__setitem__(key, value)

d = MyDict()
d["a"] = 1
print(d["a"])
```

## Q51: What are Python's iterators and iterables?
**A:** An iterable has `__iter__()` or `__getitem__()` method and can be used in for loops (lists, strings, dicts). An iterator has `__next__()` and `__iter__()` (returns self). Iterators are produced by `iter()` and consumed element by element. All iterators are iterables, but not vice versa.
**Code:**
```python
nums = [1, 2, 3]              # iterable: has __iter__()
it = iter(nums)              # iterator: has __next__()
print(next(it), next(it))    # 1 2
```

## Q52: How do you create a custom iterator?
**A:** Implement `__iter__()` (returns self) and `__next__()` (returns next item, raises `StopIteration` when done). Example: `class Counter: def __init__(self, n): self.n = n; self.i = 0` then implement the methods. Or use generator functions which are simpler.
**Code:**
```python
class Counter:
    def __init__(self, limit):
        self.limit = limit
        self.n = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.n >= self.limit:
            raise StopIteration
        self.n += 1
        return self.n

print(list(Counter(3)))   # [1, 2, 3]
```

## Q53: What is the difference between `__iter__` and `__next__`?
**A:** `__iter__` returns an iterator object and is called once at the start of iteration (for loops call `iter()` which calls `__iter__`). `__next__` returns the next value and is called each iteration step; it raises `StopIteration` when exhausted. `__iter__` can return `self` for simple iterators.
**Code:**
```python
class Down:
    def __init__(self, top):
        self.top = top
    def __iter__(self):          # called once by iter()
        self.n = self.top
        return self
    def __next__(self):          # called each iteration step
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

print(list(Down(3)))   # [3, 2, 1]
```

## Q54: Explain Python's `collections` module.
**A:** The `collections` module provides specialized container datatypes: `namedtuple` (tuple with named fields), `deque` (double-ended queue), `Counter` (dict subclass for counting), `OrderedDict` (ordered dictionary), `defaultdict` (dict with default factory), `ChainMap` (multiple dicts as one), `UserDict`, `UserList`, `UserString`.
**Code:**
```python
from collections import namedtuple, deque, Counter, defaultdict, OrderedDict

Point = namedtuple("Point", ["x", "y"])
print(Point(1, 2))                      # tuple with named fields
print(deque([1, 2], maxlen=2))          # double-ended queue
print(Counter("aabbb"))                 # counting
print(defaultdict(list))                # dict with default factory
print(OrderedDict(a=1, b=2))            # insertion-ordered dict
```

## Q55: What is `defaultdict` and when would you use it?
**A:** `defaultdict` is a dictionary subclass that calls a factory function for missing keys. Instead of raising `KeyError`, it creates and returns a default value. Example: `defaultdict(list)` appends without checking key existence. Useful for grouping, counting, and nested dictionary patterns.
**Code:**
```python
from collections import defaultdict

dd = defaultdict(list)
dd["fruits"].append("apple")     # no KeyError; key auto-created
print(dd)
print(dd["nonexistent"])         # [] instead of raising
```

## Q56: How does `NamedTuple` work?
**A:** `NamedTuple` creates tuple subclasses with named fields. Syntax: `Point = namedtuple('Point', ['x', 'y'])` or using class syntax with `typing.NamedTuple`. Fields can be accessed by name (`point.x`) or index (`point[0]`). Namedtuples are immutable, lightweight, and more readable than regular tuples.
**Code:**
```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])   # tuple subclass with fields
p = Point(3, 4)
print(p.x, p[0])              # named and positional access
print(p._asdict())            # OrderedDict? No - dict support
```

## Q57: What is `__slots__` and why use it?
**A:** `__slots__` is a class variable defining allowed attributes, which saves memory by eliminating `__dict__` per instance. It also speeds up attribute access. Trade-offs: can't add new attributes dynamically, can't inherit `__slots__` automatically, and breaks pickling by default.
**Code:**
```python
class Slim:
    __slots__ = ("x", "y")      # no __dict__ per instance
    def __init__(self, x, y):
        self.x, self.y = x, y

s = Slim(1, 2)
print(hasattr(s, "__dict__"))   # False -> memory saved, faster access
```

## Q58: Explain Python's `enum` module.
**A:** The `enum` module supports enumerations via classes inheriting `Enum`. Members are constants with names and values. Features: auto-numbering (`auto()`), iteration over members, comparison, and custom methods. `IntEnum` integrates with integers. `Flag` supports bitwise operations.
**Code:**
```python
from enum import Enum, auto

class Color(Enum):
    RED = auto()          # auto-numbered
    GREEN = auto()
    BLUE = auto()

for c in Color:
    print(c.name, c.value)
```

## Q59: What's the difference between `Enum` and `IntEnum`?
**A:** `IntEnum` members are also instances of `int`, so they can be used in arithmetic operations and compared to integers. `Enum` members are not integers and cannot be compared to other types. `IntEnum` is useful when enum values need to behave like integers in existing code.
**Code:**
```python
from enum import Enum, IntEnum

class Colors(Enum):
    RED = 1

class Numbers(IntEnum):
    ONE = 1

print(Colors.RED == 1)   # False - Enum is not an int
print(Numbers.ONE == 1)  # True  - IntEnum inherits int
print(Numbers.ONE + 2)   # 3    - arithmetic works
```

## Q60: How do you handle circular imports in Python?
**A:** Solutions include: move imports inside functions (lazy loading), restructure code to eliminate circular dependencies, use `import module` instead of `from module import name`, merge modules, or create a shared third module. Circular imports often indicate design issues.
**Code:**
```python
# module a.py
def run():
    from module_b import helper   # import inside function = lazy import
    return helper()

# restructure or lazy-import -- never fix cycles by deleting top-level imports
print("lazy imports break the cycle")
```

## Q61: What is the difference between `import module` and `from module import name`?
**A:** `import module` makes all names accessible as `module.name`. `from module import name` brings the name into the current namespace. The latter can cause naming conflicts but requires less typing. `import module` is generally preferred for clarity and avoiding shadowing.
**Code:**
```python
import math                     # full module namespace
from math import sqrt           # specific name into namespace

print(math.floor(2.7))          # module.name
print(sqrt(16))                 # bare name
```

## Q62: Explain Python's namespace and scope.
**A:** Python has LEGB scope rule: Local (inside function), Enclosing (outer functions), Global (module level), Built-in (Python's builtins). Namespaces are dictionaries mapping names to objects. Each function call creates a local namespace. The `global` and `nonlocal` keywords modify variable scope.
**Code:**
```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"            # L: Local
        print(x)
    inner()                    # prints "local"
    print(x)                   # E: Enclosing -> "enclosing"

outer()
print(x)                       # G: Global -> "global" 
```

## Q63: What is the `nonlocal` keyword?
**A:** `nonlocal` is used in nested functions to indicate a variable is defined in an enclosing function (but not global). It allows modifying variables in outer (non-global) scopes. Without `nonlocal`, assignment creates a new local variable. `nonlocal` is similar to `global` but for outer function scopes.
**Code:**
```python
def make_counter():
    count = 0
    def increment():
        nonlocal count     # modify variable in enclosing function scope
        count += 1
        return count
    return increment

c = make_counter()
print(c(), c(), c())     # 1 2 3
```

## Q64: How does Python's `global` keyword work?
**A:** The `global` keyword declares that a variable refers to the module-level global scope. Without it, assignment to a variable creates a new local. `global` allows reading and writing global variables from within functions. Overusing globals is discouraged; they can make code harder to reason about.
**Code:**
```python
count = 0

def bump():
    global count           # write to module-level variable
    count += 1

bump(); bump()
print(count)               # 2
```

## Q65: What are Python's `*` and `**` unpacking operators?
**A:** Single `*` unpacks iterables (lists, tuples, strings) into positional arguments. Double `**` unpacks dictionaries into keyword arguments. Examples: `func(*[1,2,3])` calls `func(1,2,3)`, `func(**{'a':1})` calls `func(a=1)`. Also used in function definitions and container unpacking.
**Code:**
```python
def combine(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(combine(*nums))                  # * unpacks iterable -> 6

kwargs = {"a": 1, "b": 2, "c": 3}
print(combine(**kwargs))               # ** unpacks mapping -> 6
```

## Q66: Explain Python's string formatting methods.
**A:** Three main approaches: %-formatting (`"Hello %s" % name`), `str.format()` (`"Hello {}".format(name)`), and f-strings (`f"Hello {name}"`). F-strings (Python 3.6+) are recommended: they're fast, readable, and support expressions. Template strings are also available for safer formatting.
**Code:**
```python
name, score = "Ada", 95.5

print("Hello %s" % name)                    # %-formatting
print("Hello {}, score {:.1f}".format(name, score))  # str.format
print(f"Hello {name}, score {score:.1f}")   # f-string (preferred)
```

## Q67: What are f-strings and what are their limitations?
**A:** F-strings (formatted string literals) are prefixed with `f`: `f"My name is {name}"`. They support expressions, formatting specifiers (`:.2f`), and nested f-strings. Limitations: can't use backslashes inside expressions (use variables), no lazy evaluation, and they evaluate eagerly.
**Code:**
```python
name = "Ada"
print(f"{name}")                 # simple
print(f"{name!r}")               # repr conversion
print(f"{name:>10}")             # alignment / format specs

# Limitation: no backslashes inside {} (use a variable instead)
nl = "\n"
print(f"line1{nl}line2")
```

## Q68: How does Python handle integer overflow?
**A:** Python integers have arbitrary precision (big integers). They don't overflow like in languages with fixed-width integers. Memory is allocated dynamically as needed. Operations on large integers are slower but never silently wrap around. For performance-critical code needing fixed width, use NumPy arrays.
**Code:**
```python
big = 10 ** 30
print(big)                  # arbitrary precision - no overflow
print(big * big)
```

## Q69: What is the difference between `range` in Python 2 and Python 3?
**A:** In Python 2, `range()` returns a list and `xrange()` returns an iterable. In Python 3, `range()` replaces both: it returns an immutable sequence type (lazy), supporting slicing, membership testing, and iteration. Python 3's `range` is memory-efficient for large ranges.
**Code:**
```python
r = range(1_000_000)              # Python 3: lazy, memory-efficient
print(type(r))                   # <class 'range'>
print(999_999 in r)              # O(1) membership
print(r[5:8])                    # slicing works
```

## Q70: How does Python's `map`, `filter`, and `reduce` work?
**A:** `map(func, iterable)` applies func to each item, returning an iterator. `filter(func, iterable)` yields items where func returns True. `reduce(func, sequence)` (from `functools`) cumulatively applies func to pairs. List comprehensions and generator expressions are often more readable alternatives.
**Code:**
```python
from functools import reduce

nums = [1, 2, 3, 4]
print(list(map(lambda x: x * 2, nums)))            # [2,4,6,8]
print(list(filter(lambda x: x % 2 == 0, nums)))    # [2,4]
print(reduce(lambda a, b: a + b, nums))            # 10
```

## Q71: What is the difference between `any()` and `all()`?
**A:** `any(iterable)` returns True if at least one element is truthy. `all(iterable)` returns True if all elements are truthy. Both short-circuit (stop early). Empty iterables: `any([])` returns False, `all([])` returns True. They're efficient for boolean checks on sequences.
**Code:**
```python
print(any([0, 1, 2]))       # True  - at least one truthy
print(all([1, 2, 3]))       # True  - all truthy
print(any([]), all([]))     # False True (empty edge cases)
```

## Q72: Explain `sys.argv` and `argparse`.
**A:** `sys.argv` is a list of command-line arguments (script name is `argv[0]`). `argparse` is the standard module for parsing CLI arguments with features: positional/optional args, type conversion, help messages, subcommands, and error handling. `argparse` is preferred over manual `sys.argv` parsing.
**Code:**
```python
import argparse, sys

# sys.argv: list of CLI args, argv[0] = script name
print("script:", sys.argv[0])

parser = argparse.ArgumentParser()
parser.add_argument("--count", type=int, default=1)
parser.add_argument("name")
args = parser.parse_args(["--count", "3", "world"])   # simulated argv
print(args.name, args.count)
```

## Q73: How do you profile Python code?
**A:** Using `cProfile` module (`python -m cProfile script.py`), `timeit` for micro-benchmarks, and third-party tools like `py-spy`, `memory_profiler`, `line_profiler`. `cProfile` shows function call counts and timing. For memory profiling, `tracemalloc` in the standard library or `memory_profiler` package.
**Code:**
```python
import cProfile

def work():
    total = 0
    for i in range(1_000_000):
        total += i
    return total

cProfile.run("work()")
```

## Q74: What is the `__name__ == "__main__"` idiom?
**A:** `if __name__ == "__main__":` checks if a module is run directly (vs imported). When run directly, `__name__` is `"__main__"`. When imported, it's the module's name. This idiom allows a file to be both importable and runnable, typically with test code or CLI entry points.
**Code:**
```python
# file.py
def main():
    print("runs when executed directly")

if __name__ == "__main__":
    main()                # skipped when imported
```

## Q75: Explain Python's `@wraps` decorator from functools.
**A:** `@wraps` is a decorator that updates the wrapper function's metadata (`__name__`, `__doc__`, `__module__`) to match the original function. It's used when writing decorators to preserve introspection. Without it, the decorated function loses its original identity.
**Code:**
```python
from functools import wraps

def logged(func):
    @wraps(func)               # preserve __name__, __doc__
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@logged
def greet():
    """Says hi."""
    return "hi"

print(greet.__name__, greet.__doc__)   # greet Says hi.
```

## Q76: What is the difference between `abstractmethod` and `abstractproperty`?
**A:** `@abstractmethod` (from `abc`) marks a method as abstract, forcing subclasses to implement it. `@abstractproperty` (deprecated) combined `@property` and `@abstractmethod`. Modern approach: `@property @abstractmethod` stacked. Classes with abstract methods can't be instantiated.
**Code:**
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @property
    @abstractmethod
    def area(self): ...        # must be implemented by subclasses

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    @property
    def area(self):
        return 3.14159 * self.r ** 2

print(Circle(2).area)          # 12.56636
```

## Q77: How do you create abstract base classes in Python?
**A:** Using the `abc` module. Inherit from `ABC` and decorate abstract methods with `@abstractmethod`. Abstract classes can't be instantiated. Concrete subclasses must implement all abstract methods. Register virtual subclasses with `ABCMeta.register()`. Supports isinstance checks.
**Code:**
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def sound(self): ...

class Dog(Animal):             # must implement all abstract methods
    def sound(self):
        return "woof"

print(Dog().sound())
# Animal() -> TypeError: Can't instantiate abstract class
```

## Q78: What are Python's descriptors?
**A:** Descriptors are objects that define `__get__`, `__set__`, or `__delete__` methods to customize attribute access. `property`, `classmethod`, and `staticmethod` are built-in descriptors. Descriptors control how attributes are looked up and set, enabling computed attributes, validation, and lazy loading.
**Code:**
```python
class Positive:
    def __init__(self):
        self.data = {}
    def __get__(self, obj, objtype=None):     # reading the attribute
        return self.data[id(obj)]
    def __set__(self, obj, value):            # writing the attribute
        if value < 0:
            raise ValueError("must be >= 0")
        self.data[id(obj)] = value

class Prices:
    price = Positive()

p = Prices()
p.price = 5
print(p.price)      # 5
# p.price = -1   -> ValueError
```

## Q79: Explain `__get__`, `__set__`, and `__delete__` descriptor protocol.
**A:** `__get__(self, obj, objtype)` is called when the descriptor attribute is accessed. `__set__(self, obj, value)` is called on assignment. `__delete__(self, obj)` is called on deletion. Data descriptors (with `__set__`/`__delete__`) take precedence over instance attributes in attribute lookup.
**Code:**
```python
class Descriptor:
    def __get__(self, obj, objtype=None):
        print("get")
        return obj.stored
    def __set__(self, obj, value):
        print("set")
        obj.stored = value
    def __delete__(self, obj):
        print("delete")
        del obj.stored

class Demo:
    x = Descriptor()
    def __init__(self):
        self.stored = None

d = Demo()
d.x = 10    # set -> get
print(d.x)
del d.x     # delete
```

## Q80: What is the difference between `__getattr__` and `__getattribute__`?
**A:** `__getattribute__` is called for every attribute access (be careful with recursion). `__getattr__` is only called when normal lookup fails. `__getattribute__` can be used to intercept all accesses; `__getattr__` is simpler for fallback/default implementations.
**Code:**
```python
class Config:
    def __getattribute__(self, name):        # called for EVERY attribute read
        if name == "secret":
            raise AttributeError("denied")
        return super().__getattribute__(name)
    def __getattr__(self, name):             # only when attribute not found
        return "default"

c = Config()
c.visible = 1
print(c.visible)     # 1
print(c.anything)    # default (via __getattr__)
```

## Q81: How do you implement a singleton pattern in Python?
**A:** Multiple approaches: override `__new__` to return same instance, use module-level variable (modules are singletons), use metaclass with `__call__` control, use class decorator with dict, or use `@functools.lru_cache` on a factory function. Module-level singleton is the simplest Pythonic approach.
**Code:**
```python
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

a = Singleton()
b = Singleton()
print(a is b)       # True - always the same instance
```

## Q82: What is `__call__` and when would you use it?
**A:** `__call__` makes an object callable like a function. Classes implementing `__call__` are callable. Uses: creating function-like objects with state (callable classes), decorators with arguments, and partial function applications. `callable(obj)` checks if an object implements `__call__`.
**Code:**
```python
class Adder:
    def __init__(self, n):
        self.n = n
    def __call__(self, x):       # makes instances callable
        return x + self.n

add5 = Adder(5)
print(add5(10))                  # 15
print(callable(add5))            # True
```

## Q83: Explain Python's Context Manager Protocol.
**A:** Context managers implement `__enter__` (acquires resource, returns value) and `__exit__(self, exc_type, exc_val, exc_tb)` (releases resource, handles/ suppresses exceptions). They're used with the `with` statement. The `contextlib.contextmanager` decorator converts generator functions into context managers.
**Code:**
```python
class Ctx:
    def __enter__(self):
        print("enter")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit")
        return False

with Ctx():
    print("body")
```

## Q84: What is `contextlib.suppress`?
**A:** `contextlib.suppress(*exceptions)` is a context manager that suppresses specified exceptions. Example: `with suppress(FileNotFoundError): os.remove('file')`. It's cleaner than try/except/pass for ignoring specific errors. Available since Python 3.4.
**Code:**
```python
from contextlib import suppress
import os

with suppress(FileNotFoundError):      # ignore, like except: pass
    os.remove("missing.txt")
print("nothing raised")
```

## Q85: How do you use `contextlib.contextmanager`?
**A:** Decorate a generator function that yields exactly once. Code before `yield` is `__enter__`, code after is `__exit__`. The yielded value is assigned to the `as` variable. Example: `@contextmanager def managed_file(name): f = open(name); yield f; f.close()`.
**Code:**
```python
from contextlib import contextmanager

@contextmanager
def managed():
    print("before")        # runs on __enter__
    try:
        yield "value"      # yielded value becomes `as` target
    finally:
        print("after")     # runs on __exit__

with managed() as res:
    print("body", res)
```

## Q86: What is the difference between `pickle` and `json` serialization?
**A:** `json` is human-readable, cross-language, supports basic types (dicts, lists, strings, numbers, booleans, None), and is safe. `pickle` is Python-specific, supports arbitrary objects, can execute code on deserialization (unsafe), and produces binary output. JSON is preferred for APIs and storage.
**Code:**
```python
import json, pickle

data = {"a": 1, "b": [1, 2]}

print(json.dumps(data))              # readable, cross-language, safe
print(pickle.dumps(data))            # binary, Python-specific, unsafe
print(pickle.loads(pickle.dumps(data)))
```

## Q87: Explain Python's `__enter__` and `__exit__`.
**A:** `__enter__(self)` sets up the context and returns the resource. `__exit__(self, exc_type, exc_val, exc_tb)` cleans up. If it returns True, exceptions in the with block are suppressed. Parameters carry exception info (None if no exception). Both are part of the context manager protocol.
**Code:**
```python
class Connection:
    def __enter__(self):
        print("connected")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("closed")
        return False      # True would suppress any exception

with Connection() as conn:
    raise ValueError("boom")   # __exit__ still runs, then propagates
```

## Q88: What is the difference between `__new__` and `__init__`?
**A:** `__new__` is a static method that creates and returns a new instance (runs first). `__init__` initializes the instance (called after `__new__` returns). `__new__` is used for immutable types, singletons, and metaclasses. `__init__` is the normal constructor for initialization.
**Code:**
```python
import gc

class Cache:
    def __new__(cls, data):        # create/return instance first
        obj = super().__new__(cls)
        obj._cached = data
        return obj
    def __init__(self, data):      # initialize after __new__
        self.data = data

c = Cache([1, 2])
print(c.data, c._cached)
```

## Q89: How does Python resolve attribute access?
**A:** Attribute lookup follows: data descriptors (class level with `__set__`/`__delete__`), instance `__dict__`, non-data descriptors (class level with only `__get__`), class `__dict__`, parent classes (MRO order), `__getattr__` if defined. `__getattribute__` is called first for all accesses.
**Code:**
```python
class Parent:
    attr = "parent"

class Child(Parent):
    pass

c = Child()
print(c.attr)          # instance __dict__? no -> class -> parent (MRO)
c.attr = "own"         # now stored in instance __dict__
print(c.attr)
```

## Q90: What is `__slots__` and how does it affect `__dict__`?
**A:** Defining `__slots__` prevents the creation of `__dict__` for instances, reducing memory usage. Without `__slots__`, each instance has a `__dict__` for dynamic attributes. `__slots__` restricts attributes to those listed. Classes with `__slots__` can't have `__dict__` unless explicitly included in `__slots__`.
**Code:**
```python
class WithDict:
    pass

class WithSlots:
    __slots__ = ("x",)

a, b = WithDict(), WithSlots()
print(hasattr(a, "__dict__"))    # True  - allows dynamic attrs
print(hasattr(b, "__dict__"))    # False - fixed slots only
```

## Q91: Explain Python's weak references.
**A:** Weak references (`weakref` module) hold a reference to an object without increasing its reference count. They allow garbage collection of referenced objects. Used for caches, callback registrations, and preventing circular references. `weakref.ref(obj)` creates a weak reference; call it to get the object or None.
**Code:**
```python
import weakref

class Payload: pass

p = Payload()
ref = weakref.ref(p)      # weak reference; doesn't stop GC
print(ref() is p)         # True - object still alive

del p
print(ref())              # None - object collected
```

## Q92: What is `weakref.WeakValueDictionary`?
**A:** A dictionary that holds weak references to its values. When a value is garbage collected, its key is automatically removed. Useful for caches that shouldn't prevent object cleanup. `WeakKeyDictionary` is similar but for keys. The `weakref` module also has `WeakSet`.
**Code:**
```python
import weakref

class Payload: pass

cache = weakref.WeakValueDictionary()
p = Payload()
cache["k"] = p

print(len(cache))         # 1
del p
print(len(cache))         # 0 - entry auto-removed after GC
```

## Q93: How does `__del__` work in Python?
**A:** `__del__` is a finalizer called when an object is about to be destroyed. It's not guaranteed to be called promptly (or at all in some cases). It should not be used for critical cleanup (use context managers instead). It can resurrect objects, causing confusing behavior.
**Code:**
```python
class Temp:
    def __del__(self):      # called when instance is being destroyed
        print("cleaning up")

t = Temp()
del t                      # prints "cleaning up"
# Prefer context managers for guaranteed cleanup
```

## Q94: What is the difference between `isinstance` and `type`?
**A:** `isinstance(obj, class)` returns True for subclasses (checks inheritance chain). `type(obj)` returns the exact type. `isinstance` is preferred for type checking as it supports polymorphism. Example: `isinstance(True, int)` is True, but `type(True) == int` is False.
**Code:**
```python
print(isinstance(True, int))    # True  - checks inheritance chain
print(type(True) == int)        # False - exact type is bool
```

## Q95: How do Python's comparison methods work?
**A:** `__eq__` (==), `__ne__` (!=), `__lt__` (<), `__le__` (<=), `__gt__` (>), `__ge__` (>=). Implement `__eq__` and `__hash__` together. `functools.total_ordering` decorator can generate missing comparison methods from `__eq__` and `__lt__` (or any other pair).
**Code:**
```python
from functools import total_ordering

@total_ordering
class Score:
    def __init__(self, v):
        self.v = v
    def __eq__(self, other):
        return self.v == other.v
    def __lt__(self, other):            # total_ordering fills in the rest
        return self.v < other.v

print(Score(2) >= Score(1))    # True (auto-generated)
```

## Q96: What is the `@total_ordering` decorator?
**A:** `@functools.total_ordering` automatically generates missing comparison methods (`__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__`) from `__eq__` and one other comparison method. It simplifies class definitions but may be slightly slower than implementing all methods manually.
**Code:**
```python
from functools import total_ordering

@total_ordering                 # generates missing comparison methods
class Version:
    def __init__(self, n):
        self.n = n
    def __eq__(self, other):
        return self.n == other.n
    def __lt__(self, other):
        return self.n < other.n

print(Version(2) > Version(1))   # True - derived from __eq__/__lt__
```

## Q97: Explain Python's `dataclasses` module.
**A:** `@dataclass` auto-generates `__init__`, `__repr__`, `__eq__`, and optionally `__hash__`, `__lt__` etc. from class annotations. Supports default values, immutability (`frozen=True`), field customization, and post-init processing. Reduces boilerplate compared to traditional classes.
**Code:**
```python
from dataclasses import dataclass

@dataclass                   # generates __init__, __repr__, __eq__, ...
class Point:
    x: int
    y: int

p = Point(1, 2)
print(p)                     # Point(x=1, y=2)
print(p == Point(1, 2))      # True
```

## Q98: What is `field()` in dataclasses?
**A:** `field()` configures individual dataclass fields. Options: `default` (default value), `default_factory` (callable for mutable defaults), `init` (include in `__init__`), `repr` (include in `__repr__`), `compare` (include in comparisons), `hash` (include in `__hash__`), `metadata` (extra info).
**Code:**
```python
from dataclasses import dataclass, field

@dataclass
class Item:
    name: str
    tags: list = field(default_factory=list)   # mutable default fix
    price: float = field(default=0.0, repr=False)

i = Item("pen")
i.tags.append("stationery")
print(i)                     # name in repr, price hidden
```

## Q99: How does `__post_init__` work in dataclasses?
**A:** `__post_init__` is called after `__init__` in dataclasses. It allows additional initialization logic like validation, computed fields, or converting field types. Only called if defined. Must use `InitVar` fields for parameters passed to `__init__` but not stored as fields.
**Code:**
```python
from dataclasses import dataclass

@dataclass
class Rect:
    w: float
    h: float
    area: float = 0.0

    def __post_init__(self):         # extra init logic after defaults set
        self.area = self.w * self.h

r = Rect(3, 4)
print(r.area)     # 12.0
```

## Q100: What are Python's type aliases and `NewType`?
**A:** Type aliases: `Vector = list[float]` creates a type alias for readability. `NewType('UserId', int)` creates a new type that's distinct from `int` for type checkers but is identical at runtime. `NewType` helps catch type confusion errors where different types use the same base type.
**Code:**
```python
from typing import NewType, List

Vector = List[float]                  # type alias
UserId = NewType("UserId", int)       # distinct type at type-check time

def dot(v: Vector) -> float:
    return sum(x * x for x in v)

print(dot([1.0, 2.0]))
uid = UserId(42)
print(uid)                            # runtime: plain int
```
