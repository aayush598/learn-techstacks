# Python Dunder Methods and Protocols — 100 Interview Q&A

## Q1: What are dunder methods in Python and why do they exist?

**A:** Dunder methods (double underscore methods), also called magic methods or special methods, are predefined methods in Python that have double underscores on both sides of their names — like `__init__`, `__str__`, `__len__`. They are not meant to be called directly by user code; instead, the Python interpreter invokes them implicitly in response to certain language syntax or built-in functions.

They exist to allow user-defined classes to integrate with Python's data model. When you write `len(obj)`, Python translates it to `obj.__len__()`. When you write `obj1 + obj2`, Python calls `obj1.__add__(obj2)`. This is the essence of Python's data model: instead of having a fixed set of rules for how objects behave, Python delegates behavior to dunder methods that your classes can implement.

This design philosophy is deeply rooted in the idea that Python objects should behave "natively" — they should work with `for` loops, `with` statements, `in` operators, and built-in functions seamlessly. By implementing dunder methods, you make your custom objects first-class citizens of the Python ecosystem. This is sometimes referred to as "protocol-based" programming, where dunder methods define implicit interfaces (protocols) that objects can adhere to.

From an interview perspective, understanding dunder methods is critical because it demonstrates your understanding of Python's object model, operator overloading, and how to design classes that feel natural and Pythonic. Senior roles at companies like FAANG expect you to know not just the syntax but the philosophical underpinnings — when to use dunder methods, when to avoid them, and how they relate to duck typing and ABCs.

**Example:**
```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)  # Vector(4, 6)
```

## Q2: What is the difference between `__str__` and `__repr__`?

**A:** `__repr__` is meant to return an unambiguous, developer-oriented string representation of an object. The goal is that the output should ideally be valid Python that could recreate the object — or at minimum, give developers enough information to understand what the object is. `__str__` is meant to return a human-readable, user-friendly string representation. It's what `print()` and `str()` call.

If a class only implements one, Python falls back: `str()` will use `__repr__` if `__str__` is not defined. But `repr()` will never fall back to `__str__` — it always calls `__repr__`. This asymmetry is important: every class should at least implement `__repr__`, because it serves as a debugging lifeline. A good `__repr__` makes objects easier to debug and inspect in REPL sessions, logs, and error messages.

In production codebases at companies like Tesla or Nvidia, the distinction matters for logging and monitoring. You might have a `SensorReading` class where `__repr__` shows all raw fields (timestamp, raw value, unit, calibration offset) while `__str__` shows a formatted human-readable version like "Temperature: 72.3°F". The `__repr__` is invaluable in log aggregation systems where you need machine-parseable output.

A common interview trap is asking what happens when `__str__` is defined but `__repr__` is not — the answer is that `repr()` still shows the default `<ClassName object at 0x...>` output, which is unhelpful. The reverse scenario (only `__repr__` defined) works fine because `str()` falls back to `__repr__`. Always implement `__repr__` first.

**Example:**
```python
from datetime import datetime

class Event:
    def __init__(self, name, timestamp):
        self.name = name
        self.timestamp = timestamp

    def __repr__(self):
        return f"Event(name={self.name!r}, timestamp={self.timestamp!r})"

    def __str__(self):
        return f"{self.name} at {self.timestamp:%Y-%m-%d %H:%M}"

e = Event("deploy", datetime(2025, 1, 15, 10, 30))
print(repr(e))  # Event(name='deploy', timestamp=datetime(2025, 1, 15, 10, 30))
print(str(e))   # deploy at 2025-01-15 10:30
```

## Q3: How does `__len__` work and what are its requirements?

**A:** The `__len__` method is called by the built-in `len()` function and should return an integer representing the number of items in the container. Python requires it to return a non-negative integer — returning a negative number or a non-integer raises a `TypeError`. If `__len__` is not defined but `__bool__` is, `len()` will fall back to using `__bool__` (which should return `True`/`False`, interpreted as 1/0). If neither is defined, `len()` raises a `TypeError`.

There's an important subtlety: `__len__` should only be defined for objects that represent a collection with a meaningful concept of "number of items." It should not be defined for objects where length is ambiguous or meaningless. For example, a `File` object shouldn't have `__len__` — even though you could argue it has a "size," that's conceptually different from the number of items in a sequence.

In interview contexts, a common edge case is: should `__len__` return the number of elements or the capacity? The answer is always the number of actual elements, not the allocated capacity. A list with 3 elements should report `len()` as 3, even if it has pre-allocated space for 100. Similarly, a sparse data structure should report the count of actual entries, not the size of the underlying array.

At senior-level roles, you should also know that `__len__` has performance implications. Python's `bool()` function calls `__bool__` first, then falls back to `__len__`, then defaults to `True`. This means `if my_container:` is O(1) if `__bool__` is defined, but could be O(n) if only `__len__` is defined (Python computes the length just to check truthiness). For large collections, always define `__bool__` explicitly if truthiness checks are performance-critical.

**Example:**
```python
class Polynomial:
    def __init__(self, coefficients):
        self.coeffs = list(coefficients)
        while self.coeffs and self.coeffs[-1] == 0:
            self.coeffs.pop()

    def __len__(self):
        return len(self.coeffs)

    def __bool__(self):
        return bool(self.coeffs)

p = Polynomial([1, 0, 3, 0])
print(len(p))   # 3
print(bool(p))  # True
```

## Q4: What is operator overloading and how do dunder methods enable it?

**A:** Operator overloading is the ability to define custom behavior for Python's built-in operators (`+`, `-`, `*`, `==`, `<`, `in`, `[]`, etc.) when used with instances of your classes. Python achieves this through dunder methods: each operator maps to a specific dunder method. For example, `+` calls `__add__`, `==` calls `__eq__`, `[]` calls `__getitem__`, and `in` calls `__contains__`.

This is fundamentally different from languages like C++ where operator overloading is an explicit language feature. In Python, it's an emergent property of the data model. You don't "declare" operator overloading; you simply define the corresponding dunder method, and Python's runtime automatically uses it. This is elegant but can be surprising — if you define `__eq__` without `__hash__`, your objects become unhashable (can't be used in sets or as dict keys) because Python implicitly sets `__hash__` to `None` when `__eq__` is defined.

The design philosophy behind Python's operator overloading is that operators should be intuitive extensions of an object's natural behavior. A `Matrix` class should support `+` for matrix addition. A `Money` class should support `+` for currency addition. The key guideline is: only overload operators when the operation is semantically meaningful. Overloading `+` for a `NetworkPacket` class to mean "concatenate payloads" makes sense; overloading `+` to mean "send packet" violates the principle of least surprise.

In production systems (especially at scale in companies like Samsung or Infosys), operator overloading has real trade-offs. It makes code more readable and Pythonic but can obscure performance costs. The `+` operator on two lists creates a new list — O(n) time and space. Developers who don't understand this create performance bottlenecks. Senior engineers must understand both the elegance and the cost.

**Example:**
```python
class Money:
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __repr__(self):
        return f"Money({self.amount}, {self.currency!r})"

total = Money(10, "USD") + Money(20, "USD")
print(total)  # Money(30, 'USD')
```

## Q5: Explain `__getitem__` and `__setitem__` dunder methods.

**A:** `__getitem__` enables bracket-notation access (`obj[key]`) on your objects, while `__setitem__` enables bracket-notation assignment (`obj[key] = value`). They are the foundation for making objects behave like dictionaries, lists, or any other subscriptable container. When Python encounters `obj[key]`, it translates it to `obj.__getitem__(key)`, and similarly for assignment.

A critical feature of `__getitem__` is that if it raises `IndexError`, Python will also use it for iteration as a fallback. More importantly, if `__getitem__` is defined, Python will automatically make the object iterable — it will call `__getitem__(0)`, `__getitem__(1)`, etc., until `IndexError` is raised. This means defining `__getitem__` alone is sufficient to make your object work in `for` loops, even without `__iter__`. However, explicitly defining `__iter__` is always preferred for clarity and performance.

In real-world systems, `__getitem__` is used far more broadly than just dictionary-like behavior. Consider a `DataFrame` class where `df["column_name"]` returns a column, or `df[["col1", "col2"]]` returns a subset. Or a `Matrix` class where `mat[1, 2]` returns an element (note: the key here would be a tuple `(1, 2)`). The power is in choosing what the key means — it's completely up to your class.

Edge cases to know: `__getitem__` should raise `KeyError` (for mapping-like access) or `IndexError` (for sequence-like access). Using `TypeError` for missing keys is incorrect — Python's `in` operator relies on the specific exception type. Also, `__setitem__` is not called by `dict.setdefault()` or `dict.update()` on your object — those are dict methods that don't know about your class's `__setitem__`.

**Example:**
```python
class Matrix:
    def __init__(self, rows, cols, fill=0):
        self.data = [[fill] * cols for _ in range(rows)]

    def __getitem__(self, key):
        row, col = key
        return self.data[row][col]

    def __setitem__(self, key, value):
        row, col = key
        self.data[row][col] = value

m = Matrix(3, 3)
m[1, 2] = 5
print(m[1, 2])  # 5
```

## Q6: What is the `__call__` dunder method and when is it useful?

**A:** The `__call__` method allows instances of a class to be called like functions. When you write `obj(args)`, Python translates it to `obj.__call__(args)`. This transforms instances into callable objects (callables), blurring the line between functions and objects. It's one of the most powerful dunder methods because it enables patterns like function objects, decorators as classes, strategy patterns, and stateful functions.

The primary use case is creating objects that encapsulate state along with behavior. Unlike a regular function that receives state through parameters, a callable object carries its configuration with it. This is cleaner than using global variables or closure-heavy decorator factories. For example, a rate limiter configured with `max_calls=100, period=60` can be an object whose `__call__` method checks and enforces the limit — and you can pass this object around as if it were a function.

In production codebases, `__call__` is extensively used in machine learning pipelines (callable loss functions, data transforms), middleware patterns (callable request handlers), and configuration-driven systems (a factory that's called to produce objects). Libraries like PyTorch and TensorFlow rely heavily on this pattern — `nn.Module` subclasses are callables that run the forward pass. At companies like Nvidia, understanding this pattern is essential for designing GPU compute pipelines.

A design consideration: callable objects vs. closures. Closures are simpler for pure state-carrying functions. Callable objects are better when you need multiple methods (not just `__call__`), need to be pickled (closures often can't be pickled), or want to use inheritance. In distributed systems at FAANG-scale, picklability matters — you can't serialize a closure to send across worker nodes, but you can serialize a callable object.

**Example:**
```python
class RetryPolicy:
    def __init__(self, max_retries, backoff_factor=2):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            for attempt in range(self.max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == self.max_retries - 1:
                        raise
                    sleep(self.backoff_factor ** attempt)
        return wrapper

@RetryPolicy(max_retries=3)
def fetch_data(url):
    ...
```

## Q7: How does `__contains__` work and when should you implement it?

**A:** The `__contains__` method is called by the `in` operator. When you write `x in obj`, Python calls `obj.__contains__(x)`. It should return `True` or `False`. If `__contains__` is not defined, Python falls back to iterating over the object using `__iter__`, checking each element until a match is found or the iteration ends. If neither `__contains__` nor `__iter__` is defined, Python falls back to using `__getitem__` with sequential integer indices starting from 0.

You should implement `__contains__` when membership testing is a core operation of your data structure and you can provide a more efficient implementation than linear search. For example, a `BloomFilter` class should implement `__contains__` because its whole purpose is fast probabilistic membership testing — O(1) instead of O(n). A `SortedSet` could implement `__contains__` using binary search (O(log n)) instead of the default linear scan.

There's an important edge case: if `__contains__` is not implemented and the object implements `__iter__`, Python will iterate through all elements looking for a match. This can be surprising for objects where iteration is expensive or where the concept of "equality" is nuanced. For instance, if you have a collection of `SensorReading` objects and the `in` operator compares by object identity rather than value equality, users might be surprised that two seemingly equal readings aren't considered "in" the collection.

In high-performance systems at companies like Tesla (embedded sensor data) or Nvidia (GPU memory management), implementing `__contains__` with the right data structure underneath is critical. A naive implementation with a list gives O(n) lookup; switching to a set-backed implementation gives O(1). The interview question often extends to: "How would you optimize `x in huge_dataset`?" — the answer involves `__contains__` + appropriate internal data structure + possibly caching or indexing.

**Example:**
```python
class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size

    def _hashes(self, item):
        return [hash(f"{item}_{i}") % self.size for i in range(self.hash_count)]

    def add(self, item):
        for pos in self._hashes(item):
            self.bit_array[pos] = 1

    def __contains__(self, item):
        return all(self.bit_array[pos] for pos in self._hashes(item))

bf = BloomFilter(1000, 7)
bf.add("hello")
print("hello" in bf)  # True (possibly)
```

## Q8: What are `__enter__` and `__exit__` and how do context managers work?

**A:** `__enter__` and `__exit__` are dunder methods that implement the context manager protocol. When you use `with obj:`, Python calls `obj.__enter__()` at the start and `obj.__exit__(exc_type, exc_val, exc_tb)` at the end, regardless of whether an exception occurred. `__enter__` can return a value that's bound to the `as` variable. `__exit__` receives exception information — if no exception occurred, all three parameters are `None`.

The `__exit__` method has a critical responsibility: it should perform cleanup (closing files, releasing locks, rolling back transactions) and return `True` if it handled the exception (suppressing it) or `False`/`None` to let it propagate. This exception-handling power is both useful and dangerous — a context manager that swallows exceptions silently can hide bugs. Best practice is to only suppress exceptions when there's a clear semantic reason (like `contextlib.suppress`).

Python also provides `contextlib` utilities that make context managers easier to create. `@contextlib.contextmanager` is a decorator that turns a generator function into a context manager — the code before `yield` is the `__enter__` logic, the code after is `__exit__`. For complex cases (async, nested state), the class-based approach with `__enter__`/`__exit__` is more flexible and explicit.

In production systems, context managers are ubiquitous for resource management: database connections, file handles, network sockets, temporary directories, locks, and transaction boundaries. At senior-level interviews, expect questions about composing context managers (`contextlib.ExitStack`), async context managers (`__aenter__`/`__aexit__`), and edge cases like what happens when `__enter__` raises an exception (the `with` block is never entered, and `__exit__` is NOT called — a common gotcha that can cause resource leaks).

**Example:**
```python
import time
from contextlib import contextmanager

@contextmanager
def timer(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label}: {elapsed:.4f}s")

with timer("sort"):
    sorted(range(1000000, 0, -1))
```

## Q9: Explain the iterator protocol: `__iter__` and `__next__`.

**A:** The iterator protocol consists of two dunder methods: `__iter__` and `__next__`. `__iter__` returns the iterator object itself (typically `return self`) and is called when you use an object in a `for` loop or pass it to `iter()`. `__next__` returns the next item in the sequence and raises `StopIteration` when there are no more items. This protocol is what makes `for` loops work — Python repeatedly calls `__next__` until `StopIteration` is raised.

A crucial distinction many developers confuse: an iterable is NOT the same as an iterator. An iterable has an `__iter__` method that returns an iterator. An iterator has both `__iter__` (returning itself) and `__next__`. This is why you can iterate over a list multiple times (it's iterable) but a generator can only be iterated once (it's an iterator). The `for` loop always calls `__iter__` first to get a fresh iterator, which is why you can use the same list in multiple `for` loops.

Generators (functions with `yield`) are the most common way to create iterators, but you can also build custom iterator classes. Custom iterator classes give you more control: you can implement `send()` and `throw()` for coroutine-like behavior, implement `__length_hint__` for optimization, and the iterator state is explicit in instance variables rather than implicit in the generator's frame. In production code at scale (FAANG), custom iterator classes are preferred when the iteration logic is complex or when you need the iterator to be independently inspectable.

Advanced edge cases: iterators can be finite or infinite. An infinite iterator (like `itertools.count()`) is valid but must be used carefully — consuming it with `list()` will hang forever. The `StopIteration` exception propagating out of `__next__` is caught by the `for` loop; if it propagates out of a generator, it terminates the generator. This interaction between `StopIteration` and generators was the basis for `async/await` syntax (PEP 492) — generators that raise `StopIteration` internally can accidentally terminate themselves, which is why Python 3.7+ raises `RuntimeError` for that case.

**Example:**
```python
class FibonacciIterator:
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.max_count:
            raise StopIteration
        self.count += 1
        self.a, self.b = self.b, self.a + self.b
        return self.a

for num in FibonacciIterator(10):
    print(num, end=" ")  # 1 1 2 3 5 8 13 21 34 55
```

## Q10: What is `__new__` and how does it differ from `__init__`?

**A:** `__new__` is a static method that creates a new instance of a class. It is called BEFORE `__init__` and is responsible for actually allocating and returning the instance. `__init__` is called AFTER `__new__` and is responsible for initializing the instance's attributes. `__new__` takes the class as its first argument; `__init__` takes the instance. This is a common interview distinction that trips up many developers.

`__new__` is rarely needed for everyday Python, but it's essential for specific patterns: singletons (ensuring only one instance exists), immutables (you can't change an object after `__init__` for `int`, `str`, `tuple`), and subclassing immutables. When you subclass `int` or `str`, the value is determined at `__new__` time because these types are immutable — `__init__` can't modify the value after creation.

The singleton pattern via `__new__` is the most common interview example, but there's a subtlety: the `__new__`-based singleton doesn't prevent creation via `object.__new__()` if someone bypasses your class. A more robust approach uses a metaclass. Also, `__init__` is always called on the returned instance, even if `__new__` returns an instance of a different class — so your `__init__` must be compatible with whatever `__new__` returns.

In production systems, `__new__` is critical for interned objects (Python interns small integers and short strings), immutable value objects (like `Decimal` or `Fraction`), and factory patterns where the returned type depends on configuration. At senior-level roles, expect questions about `__init_subclass__` (PEP 487) as a modern alternative to metaclasses for class customization.

**Example:**
```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value):
        self.value = value

a = Singleton(10)
b = Singleton(20)
print(a is b)       # True
print(a.value)      # 20
```

## Q11: What is `__del__` and why should you avoid relying on it?

**A:** `__del__` is a destructor method that Python calls when an object is about to be garbage collected. However, the timing of `__del__` is NOT guaranteed — Python does not promise when (or even if) `__del__` will be called. The garbage collector may collect objects in any order, and in CPython, `__del__` is called when the reference count drops to zero, but in PyPy and other implementations, it may never be called. This unpredictability makes `__del__` unreliable for critical cleanup operations.

The most dangerous aspect of `__del__` is the "zombie object" problem with reference cycles. If object A references object B, and object B references object A, and both have `__del__` methods, Python cannot determine the safe order to destroy them. In Python 3.4+, these objects are simply left in `gc.garbage` and never collected — a memory leak. The `del` statement does NOT call `__del__` immediately; it only decrements the reference count. If other references exist, the object is not destroyed.

For resource cleanup, the correct approaches are: context managers (`__enter__`/`__exit__`), `atexit` handlers, explicit `.close()` methods, or weak references with finalizers (`weakref.finalize`). Context managers are the gold standard because they provide deterministic cleanup — you know exactly when resources are released. The `weakref.finalize` function is a more reliable alternative to `__del__` when you need destructor-like behavior.

In production systems at FAANG-scale, `__del__` is almost never used. Companies like Google and Facebook have Python style guides that explicitly prohibit `__del__`. When you need cleanup, you use context managers. When you need weak references, you use `weakref.ref` or `weakref.finalize`. The only legitimate use of `__del__` is for logging/debugging during development.

**Example:**
```python
import weakref

class Connection:
    def __init__(self, url):
        self.url = url
        self._closed = False
        self._finalizer = weakref.finalize(self, self._cleanup, url)

    @staticmethod
    def _cleanup(url):
        print(f"Cleaning up connection to {url}")

    def close(self):
        if not self._closed:
            self._closed = True
            self._finalizer()

    def __del__(self):
        self.close()  # Fallback, but not guaranteed
```

## Q12: How does `__bool__` work and what is its relationship with `__len__`?

**A:** The `__bool__` method is called by the built-in `bool()` function and when objects are used in boolean contexts (`if obj:`, `while obj:`, `not obj`, `obj and other`). It should return `True` or `False`. Python evaluates truthiness in this priority order: first it checks for `__bool__`, then falls back to `__len__` (returning `True` if the result is non-zero), then defaults to `True` for all objects.

This priority chain has important performance implications. If you only define `__len__` on a large collection, every `if my_collection:` check will compute the full length of the collection just to determine truthiness — O(n) for a linked list, for example. By defining `__bool__` to return early (e.g., checking if a head pointer is None), you can make truthiness O(1). This is critical in performance-sensitive code at companies like Tesla (real-time systems) or Nvidia (GPU scheduling).

There's also a subtle interaction: if an object defines both `__bool__` and `__len__`, `__bool__` takes precedence for truthiness checks. The `__len__` fallback only kicks in when `__bool__` is not defined. This means you can have an object where `len(obj)` returns 5 but `bool(obj)` returns `False` — the two are independent. While this is legal, it can be confusing and should only be done when there's a clear semantic reason.

A common interview pattern is the "empty container" edge case: an object with `__len__` returning 0 is falsy, but what about an object that has no items but is conceptually "present"? For example, an empty `Email` object (no recipients, no body) might still be "truthy" because the email itself exists — this is a design decision, not a technical requirement. At senior level, you should articulate when truthiness should reflect "has items" vs. "is conceptually valid."

**Example:**
```python
class CachedResult:
    def __init__(self, compute_fn):
        self._compute = compute_fn
        self._cache = None
        self._computed = False

    def __bool__(self):
        if not self._computed:
            self._cache = self._compute()
            self._computed = True
        return self._cache is not None

    def __len__(self):
        if not self._computed:
            self._cache = self._compute()
            self._computed = True
        return len(self._cache) if self._cache else 0

result = CachedResult(lambda: expensive_db_query())
if result:  # O(1) check
    print(f"Got {len(result)} results")
```

## Q13: What is the purpose of `__missing__` in dict subclasses?

**A:** The `__missing__` method is called by `dict.__getitem__` when a key is not found. It's NOT a standard dunder method that Python calls directly — it's a hook that the `dict` class specifically checks for. When you access `d[key]` and the key doesn't exist, if the dict subclass defines `__missing__`, it's called with the missing key. If `__missing__` is not defined, `KeyError` is raised.

This is extremely useful for creating specialized dictionary types. The most common use case is a `defaultdict`-like behavior, but `__missing__` gives you more control because you can compute the default based on the key itself, handle side effects, or log missing access patterns. Python's own `collections.defaultdict` is implemented using `__missing__`.

A subtlety that interviewers love: `__missing__` is ONLY called by `__getitem__`. It is NOT called by `dict.get()` or the `in` operator. This means `d.get(key)` will return `None` (or the default) without triggering `__missing__`, and `key in d` will return `False`. If you need `get()` and `in` to also trigger your custom logic, you must override those methods separately. This inconsistency is a common source of bugs when building custom dict subclasses.

In production codebases, `__missing__` is used for configuration management (lazy-loading config values), caching (compute-on-miss caches), and database abstraction (lazy-loading related objects). At senior-level roles, expect questions about thread safety — if multiple threads access the same `__missing__`-backed dict, you need to handle the case where two threads simultaneously try to compute the default for the same key (double computation or race condition).

**Example:**
```python
class TrackingDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.misses = []

    def __missing__(self, key):
        self.misses.append(key)
        raise KeyError(key)

d = TrackingDict(a=1, b=2)
try:
    _ = d["c"]
except KeyError:
    pass
print(d.misses)  # ['c']
```

## Q14: What are the comparison dunder methods: `__eq__`, `__lt__`, etc.?

**A:** These are the comparison dunder methods that define how objects are compared using `==`, `!=`, `<`, `<=`, `>`, and `>=`. `__eq__` is the most important — it defines equality. When you define `__eq__`, Python automatically sets `__ne__` to its negation (unless you explicitly define `__ne__`). The ordering methods (`__lt__`, `__le__`, `__gt__`, `__ge__`) are independent, but Python provides `functools.total_ordering` as a decorator that generates the missing ordering methods.

A critical side effect: defining `__eq__` without `__hash__` makes the class unhashable (sets `__hash__` to `None`). This is because Python requires that objects that compare equal have the same hash value (the hash contract). If you define custom equality, Python can't guarantee this, so it disables hashing. You must explicitly define `__hash__` if you want your objects to be usable as dictionary keys or in sets.

The `total_ordering` decorator is convenient but has a performance cost — it generates methods that make multiple comparison calls. For example, `__le__` generated by `total_ordering` calls `self < other or self == other`, which is two comparisons instead of one. In performance-critical code (common at Nvidia or Tesla), it's better to implement all six methods directly rather than use `total_ordering`.

In distributed systems (FAANG-scale), equality semantics are complex. Should two `User` objects be equal if they have the same ID but different names? Should two database records be equal if they have the same primary key? The answer depends on whether you're comparing "value equality" (all fields match) or "identity equality" (same entity). At senior level, you should discuss the `__eq__` vs. `is` distinction.

**Example:**
```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __eq__(self, other):
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

    def __lt__(self, other):
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    def __hash__(self):
        return hash((self.major, self.minor, self.patch))

print(Version(1, 2, 3) < Version(1, 2, 4))  # True
```

## Q15: What is `__hash__` and what is the hash contract?

**A:** The `__hash__` method returns an integer hash value for an object. This hash is used by hash-based containers (dicts, sets) to quickly locate items. The hash contract has two parts: (1) if `a == b`, then `hash(a) == hash(b)` must be true, and (2) `hash(a)` must return the same value every time it's called during the object's lifetime (the hash must not change after the object is added to a set or used as a dict key).

The contract does NOT require the reverse — two objects with the same hash are not required to be equal (hash collisions are expected). This is why dicts use both hash-based bucketing and equality checks for lookup. The hash value determines which bucket to search, and then equality determines the actual match within the bucket.

When you define `__eq__` without `__hash__`, Python sets `__hash__ = None`, making the object unhashable. If you define both, you must ensure they're consistent. A common pattern is `__hash__ = lambda self: hash((self.field1, self.field2, ...))` for objects whose fields are all hashable. Mutable objects should NOT be hashable because modifying a field after adding the object to a set would break the set's internal structure.

In production systems, hash quality matters. A class that hashes all fields but uses a poor hash function can have pathological performance when many objects share the same hash value. Python's `hash()` function handles this well for basic types, but for custom objects with many fields, consider using `hashlib` for better distribution. In distributed systems at FAANG, hash consistency across nodes is critical for consistent hashing schemes.

A practical edge case: immutable data classes created with `@dataclass(frozen=True)` automatically get `__hash__` based on all fields. Mutable data classes (the default) get `__hash__ = None`. This is correct behavior — you can't hash mutable objects safely.

**Example:**
```python
class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

    def __hash__(self):
        return hash((self._x, self._y))

points = {Point(1, 2), Point(3, 4), Point(1, 2)}
print(len(points))  # 2
```

## Q16: What are `__slots__` and how do they relate to the object model?

**A:** `__slots__` is a class variable that restricts the instance attributes of a class. When you define `__slots__ = ('x', 'y')`, instances of that class can only have `x` and `y` attributes — attempting to set any other attribute raises `AttributeError`. Internally, Python uses a more efficient storage mechanism (an array of descriptors) instead of the standard `__dict__` dictionary, which saves significant memory per instance.

`__slots__` is not a dunder method but a dunder attribute that interacts with the object model. It affects how `__init__`, `__getattr__`, and `__setattr__` work. With `__slots__`, attribute access is faster (direct descriptor lookup vs. dict lookup) and memory usage is lower (no per-instance dict overhead). For classes with millions of instances (common in data processing at FAANG), this can save gigabytes of memory.

The trade-offs are significant: you can't add new attributes at runtime, multiple inheritance with `__slots__` is tricky (each parent with `__slots__` must have non-overlapping slot names), and `__weakref__` must be explicitly included in `__slots__` if you want weak references. Subclasses of classes with `__slots__` need their own `__slots__` or they'll get a `__dict__` anyway.

In production systems, `__slots__` is used extensively in ORM models (SQLAlchemy uses them for mapped classes), network protocol implementations (where millions of message objects are created), and data processing pipelines. At Tesla, sensor data objects that are created millions of times per second benefit enormously from `__slots__`. The performance improvement is both memory (40-50% less per instance) and speed (10-20% faster attribute access).

**Example:**
```python
class Point:
    __slots__ = ('x', 'y', '__weakref__')

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(p.x)         # 1
print(hasattr(p, '__dict__'))  # False
```

## Q17: What is `__getattr__` vs `__getattribute__`?

**A:** `__getattr__` is called as a fallback when normal attribute lookup fails — i.e., when the attribute is not found through the instance, class, or any base class. `__getattribute__` is called for EVERY attribute access, regardless of whether the attribute exists. This distinction is fundamental and often tested in interviews.

The attribute lookup order is: (1) `__getattribute__` is called unconditionally, (2) if `__getattribute__` raises `AttributeError`, `__getattr__` is called, (3) if `__getattr__` also raises `AttributeError` (or is not defined), the standard `AttributeError` is raised. This means `__getattribute__` is a universal interceptor, while `__getattr__` is a catch-all for missing attributes.

A critical gotcha: `__getattribute__` can easily cause infinite recursion if you try to access any attribute within it (because accessing an attribute triggers `__getattribute__` again). You MUST use `super().__getattribute__(name)` or `object.__getattribute__(self, name)` to access attributes within `__getattribute__`. `__getattr__` doesn't have this problem because it's only called for missing attributes.

In production systems, `__getattr__` is used for lazy loading (loading database records on attribute access), API wrappers (proxying attribute access to a backend), and configuration objects (falling back to defaults). `__getattribute__` is used for logging/debugging all attribute access, security (blocking access to sensitive attributes), and caching (intercepting all reads to check a cache first). At senior level, expect questions about combining `__getattr__` with descriptors.

**Example:**
```python
class LazyRecord:
    def __init__(self, record_id):
        self.record_id = record_id
        self._loaded = False
        self._data = {}

    def _load(self):
        if not self._loaded:
            self._data = db.fetch(self.record_id)
            self._loaded = True

    def __getattr__(self, name):
        self._load()
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
```

## Q18: What is `__setattr__` and how do you prevent infinite recursion?

**A:** `__setattr__` is called for EVERY attribute assignment, whether the attribute already exists or not. When you write `obj.attr = value`, Python calls `obj.__setattr__('attr', value)`. This is different from `__getattr__` (which is only for missing attributes) — `__setattr__` intercepts ALL assignments.

The biggest pitfall is infinite recursion. If you try to set an attribute within `__setattr__` using `self.attr = value`, it triggers `__setattr__` again, creating infinite recursion. The solution is to use `super().__setattr__(name, value)` or `object.__setattr__(self, name, value)` to bypass the custom `__setattr__`. This pattern is essential when implementing frozen/immutable objects, validated attribute setting, or computed properties with storage.

A common interview question: "Implement a class where attributes can only be set once (write-once)." The solution uses `__setattr__` to check if the attribute already exists in the instance's `__dict__` and raises `AttributeError` if it does. For classes with `__slots__`, you need a different approach using descriptors.

In production systems, `__setattr__` is used for validation (ensuring attribute values meet constraints), logging (tracking all attribute changes), reactive systems (triggering callbacks when attributes change), and proxy objects (forwarding attribute assignments to a wrapped object). At Tesla, `__setattr__` is used in vehicle configuration objects to ensure critical parameters (like motor limits) can't be accidentally overwritten.

**Example:**
```python
class Validated:
    def __init__(self, **validators):
        object.__setattr__(self, '_validators', validators)

    def __setattr__(self, name, value):
        if name in self._validators:
            if not self._validators[name](value):
                raise ValueError(f"Invalid value for {name}: {value}")
        object.__setattr__(self, name, value)

class Config(Validated):
    def __init__(self):
        super().__init__(
            port=lambda v: isinstance(v, int) and 0 < v < 65536,
            host=lambda v: isinstance(v, str) and len(v) > 0,
        )

c = Config()
c.port = 8080      # OK
# c.port = -1      # ValueError
```

## Q19: What is `__format__` and how does the format protocol work?

**A:** `__format__` is called by the built-in `format()` function and by f-strings. When you write `format(obj, spec)` or `f"{obj:spec}"`, Python calls `obj.__format__(spec)`. The `spec` is the format specification string (like `".2f"` for floats or `">10"` for right-aligned strings). If `__format__` is not defined, Python falls back to `str(obj)` with the spec applied to the resulting string.

This is particularly useful for domain-specific formatting. A `Temperature` class might support `f"{temp:.1f}"` for Celsius, `f"{temp:degF:.1f}"` for Fahrenheit, or `f"{temp:unitless}"` for just the number. The format spec becomes a mini-DSL for your domain. Python's own `datetime` and `Decimal` classes use `__format__` extensively.

A subtle edge case: `format(obj, '')` (empty spec) calls `obj.__format__('')`. If your `__format__` doesn't handle the empty string case, it can fail or return unexpected results. Always handle `''` as a default format. Also, `str(obj)` calls `obj.__format__('')` if `__str__` is not defined, so `__format__` can serve as a fallback for `__str__`.

In production systems, `__format__` is used for report generation (formatting financial data with locale-specific separators), logging (formatting objects with context-specific detail levels), and API responses (formatting objects differently for different clients). At senior level, you should know that `__format__` receives the raw format spec string, so you need to parse it yourself — Python doesn't do any interpretation.

**Example:**
```python
class Distance:
    def __init__(self, meters):
        self.meters = meters

    def __format__(self, spec):
        if spec == '' or spec == 'm':
            return f"{self.meters:.2f} m"
        elif spec == 'km':
            return f"{self.meters / 1000:.3f} km"
        elif spec == 'ft':
            return f"{self.meters * 3.28084:.2f} ft"
        return format(self.meters, spec)

d = Distance(1500)
print(f"{d}")       # 1500.00 m
print(f"{d:km}")    # 1.500 km
```

## Q20: What is `__iter__` vs `__getitem__` for iteration and which should you prefer?

**A:** Both `__getitem__` and `__iter__` can make an object iterable, but they use different protocols. If only `__getitem__` is defined (with integer indices starting from 0), Python will call `__getitem__(0)`, `__getitem__(1)`, etc., until `IndexError` is raised. If `__iter__` is defined, Python calls it once to get an iterator, then calls `__next__` repeatedly. When both are defined, `__iter__` takes precedence.

The `__iter__` protocol is strongly preferred for several reasons: it's more efficient (doesn't require raising exceptions for flow control), it supports infinite iterators, it's the standard protocol that all Python iteration tools expect, and it allows the iterator to maintain state without index-based access. The `__getitem__` fallback exists primarily for backward compatibility with Python 2 style sequences.

However, `__getitem__` has a legitimate use case: when your object is naturally index-based (like a matrix, polynomial, or ring buffer) AND you want to support both `obj[i]` access AND iteration. In this case, implementing `__getitem__` with integer-index support gives you iteration "for free" via the fallback mechanism. But even then, explicitly implementing `__iter__` is better for clarity.

In interview contexts, a common question is: "Why does `for x in my_obj:` work even though I only defined `__getitem__`?" The answer is Python's fallback mechanism. A follow-up: "Should I rely on this?" The answer is no — always implement `__iter__` explicitly. The fallback is an implementation detail, not a guarantee. At senior level, discuss how this relates to "explicit is better than implicit" (The Zen of Python).

**Example:**
```python
class Matrix:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        row, col = index
        return self.data[row][col]

    def __iter__(self):
        for row in self.data:
            for item in row:
                yield item

m = Matrix([[1, 2], [3, 4]])
print(list(m))  # [1, 2, 3, 4]
print(m[0, 1])  # 2
```

## Q21: What is `__copy__` and `__deepcopy__` and when do you need them?

**A:** `__copy__` and `__deepcopy__` are methods called by `copy.copy()` and `copy.deepcopy()` respectively. `copy.copy()` creates a shallow copy — a new object with references to the same nested objects. `copy.deepcopy()` creates a deep copy — a new object with recursively copied nested objects. The `__copy__` method receives the object being copied as an argument, and `__deepcopy__` receives the memo dictionary (used to handle circular references).

You need these methods when the default shallow/deep copy behavior is incorrect for your object. For example, a class with a lock object should NOT deep copy the lock — locks should be shared, not duplicated. A class with a database connection should create a new connection in the copy, not share the same connection. A class with expensive-to-compute caches should decide whether to copy the cache or recompute it.

The `memo` dictionary in `__deepcopy__` is crucial for handling circular references and object identity. When deep copying object A that references object B, which references object A, the memo dict ensures the second reference to A is the same copied object (not an infinite recursion or duplicate copy). If you don't handle the memo dict correctly, deep copying objects with cycles will cause infinite recursion.

In production systems, deep copying is expensive and often unnecessary. Python's `copy.deepcopy` can be 10-100x slower than shallow copy. At FAANG-scale, explicitly designing for copy semantics is preferred over relying on `deepcopy`. Use immutable objects (tuples, namedtuples, frozen dataclasses) to avoid copy concerns entirely. When you must copy, implement `__copy__` and `__deepcopy__` to control exactly what gets copied.

**Example:**
```python
import copy

class Connection:
    def __init__(self, url):
        self.url = url
        self._handle = None

    def __deepcopy__(self, memo):
        new_conn = Connection(copy.deepcopy(self.url, memo))
        new_conn._handle = None
        return new_conn

    def __copy__(self):
        new_conn = Connection(self.url)
        new_conn._handle = self._handle  # Share the handle
        return new_conn
```

## Q22: What is `__sizeof__` and how does it relate to `sys.getsizeof()`?

**A:** `__sizeof__` returns the size in bytes of a single object, excluding the size of objects it references. When `sys.getsizeof(obj)` is called, it returns `obj.__sizeof__()` plus the overhead of the object header. The key distinction: `__sizeof__` reports the shallow size (just the object's own overhead), not the total memory footprint including all referenced objects.

`sys.getsizeof()` calls `__sizeof__` and adds the garbage collector overhead (GC overhead varies by Python implementation). For CPython, this adds 16 bytes for GC-tracked objects. If you want the total memory including referenced objects, you need `pympler.asizeof` or a custom recursive traversal.

The default `__sizeof__` (from `object`) returns the base object size. If your class uses `__slots__`, you should override `__sizeof__` to report the correct size, because `__slots__` changes the internal layout. If your class stores data in external structures (C extensions, numpy arrays), the default `__sizeof__` won't reflect the actual memory usage — you need to override it.

In production systems at Tesla (embedded) or Nvidia (GPU memory), accurate memory reporting is critical for resource management. When you have millions of objects, the difference between reported and actual memory can cause OOM errors. Override `__sizeof__` to report accurate sizes, and use `gc.get_objects()` + recursive traversal for complete memory profiling.

**Example:**
```python
import sys

class Matrix:
    __slots__ = ('rows', 'cols', 'data')

    def __init__(self, rows, cols, data):
        self.rows = rows
        self.cols = cols
        self.data = data

    def __sizeof__(self):
        return sys.getsizeof(self.data) + sys.getsizeof(self.rows) + sys.getsizeof(self.cols)

m = Matrix(1000, 1000, list(range(1000000)))
print(sys.getsizeof(m))
```

## Q23: What are `__instancecheck__` and `__subclasscheck__`?

**A:** `__instancecheck__` is called by `isinstance()` and `__subclasscheck__` is called by `issubclass()`. They allow you to customize the behavior of these built-in functions. When you write `isinstance(obj, MyClass)`, Python calls `MyClass.__instancecheck__(obj)`. When you write `issubclass(A, B)`, Python calls `B.__subclasscheck__(A)`.

These are defined on the metaclass (the class of the class), not on the class itself. By default, they check for actual inheritance relationships. But you can override them to implement custom type-checking logic. For example, the `abc.ABCMeta` metaclass uses `__subclasscheck__` to implement structural subclass checking — a class is considered a subclass of an ABC if it implements the required methods, even without explicit inheritance.

A common use case is the "virtual subclass" pattern, where you register types as subclasses without inheritance. `abc.ABCMeta.register()` uses `__subclasscheck__` for this. You can also use `__instancecheck__` for duck typing checks — `isinstance(obj, Iterable)` checks if the object has `__iter__`, regardless of actual inheritance from `Iterable`.

In production systems, custom `isinstance` checks are used for protocol enforcement (checking that objects implement required interfaces), type coercion (automatically converting between compatible types), and plugin systems (checking if an object matches a plugin interface). At senior level, discuss the performance implications: `isinstance` checks with ABCs are slower than direct inheritance checks because they involve method resolution.

**Example:**
```python
from abc import ABCMeta

class ProtocolMeta(ABCMeta):
    def __instancecheck__(cls, instance):
        if super().__instancecheck__(instance):
            return True
        return all(
            hasattr(instance, method)
            for method in cls._required_methods
        )

class Serializable(metaclass=ProtocolMeta):
    _required_methods = ['serialize', 'deserialize']

class JSON:
    def serialize(self):
        return '{}'
    def deserialize(self, data):
        pass

print(isinstance(JSON(), Serializable))  # True (structural)
```

## Q24: What is `__init_subclass__` and how does it modernize class customization?

**A:** `__init_subclass__` (PEP 487) is called when a class is subclassed. It's defined on the parent class and receives the newly created subclass as its first argument (plus any keyword arguments from the class definition). This provides a clean, simple alternative to metaclasses for many common class customization patterns.

Before `__init_subclass__`, the only way to run code when a class was subclassed was through metaclasses. Metaclasses are powerful but complex — they affect the entire class creation process and are hard to compose. `__init_subclass__` is simpler, more explicit, and easier to understand. It runs after the subclass is fully created, while metaclass `__init__` runs during creation.

The keyword arguments passed to `__init_subclass__` come from the class definition: `class Child(Parent, key=value)`. This enables a declarative style for class configuration. Libraries like Django use this extensively for model fields — `class MyModel(models.Model): name = models.CharField(max_length=100)` uses `CharField.__set_name__` (another PEP 487 feature) to configure the field with its name.

In production systems, `__init_subclass__` is used for: plugin registration (automatically registering subclasses in a registry), validation (ensuring subclasses implement required attributes), configuration (setting up class-level state based on subclass-specific arguments), and documentation (auto-generating docs from class definitions). At senior level, know that `__init_subclass__` is called BEFORE `__set_name__`, so you can't rely on descriptor names being set yet. Also, `__init_subclass__` doesn't prevent metaclass usage — they can coexist.

**Example:**
```python
class Plugin:
    _registry = {}

    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__
        Plugin._registry[name] = cls

class AuthPlugin(Plugin, plugin_name="auth"):
    pass

class LogPlugin(Plugin, plugin_name="logger"):
    pass

print(Plugin._registry)  # {'auth': <class 'AuthPlugin'>, 'logger': <class 'LogPlugin'>}
```

## Q25: What is `__set_name__` and how does it work with descriptors?

**A:** `__set_name__` is called automatically when a class is created (PEP 487). It receives two arguments: the owner class (the class that contains the descriptor) and the attribute name (the name the descriptor was assigned to in the class). This eliminates the need for metaclass-based name injection, which was the standard approach before Python 3.6.

`__set_name__` is primarily useful for descriptors (classes that implement `__get__`, `__set__`, or `__delete__`). Before `__set_name__`, descriptors had to be explicitly told their name through metaclass magic or manual configuration. With `__set_name__`, the descriptor can automatically know its name when it's used in a class definition, making descriptor implementations much cleaner.

A common use case is field validation in ORM-like systems. A `Field` descriptor can use `__set_name__` to store its attribute name and use it in error messages, storage keys, and database column names. This enables the clean Django-style syntax: `class User: name = CharField(max_length=100)` where `name` automatically becomes the field name.

In production systems, `__set_name__` is used extensively in data validation frameworks (Pydantic, Marshmallow), ORM systems (SQLAlchemy, Django), and configuration systems. At senior level, note that `__set_name__` is only called when the descriptor is assigned as a class attribute — it's NOT called when the descriptor is created or when it's assigned to an instance. Also, if a descriptor is reassigned in a subclass, `__set_name__` is called again with the new name.

**Example:**
```python
class Field:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_field_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, None)

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be a string")
        setattr(obj, self.storage, value)

class User:
    name = Field()
    email = Field()

u = User()
u.name = "Alice"
print(u.name)  # Alice
```

## Q26: How do you implement `__reversed__` and when should you use it?

**A:** `__reversed__` is called by the built-in `reversed()` function. It should return an iterator that yields items in reverse order. If `__reversed__` is not defined, Python falls back to: (1) using `__len__` and `__getitem__` with decreasing indices, or (2) raising `TypeError` if neither is available. The fallback mechanism means you can get reversed iteration for free if you implement `__len__` and `__getitem__`, but this is O(n) and involves exception handling for flow control.

You should implement `__reversed__` when: (1) you have a more efficient reverse iteration than the index-based fallback, (2) your data structure has a natural reverse traversal (like a linked list with a tail pointer), or (3) you want to support `for x in reversed(collection)` idiomatically. For example, a tree structure might implement `__reversed__` for reverse in-order traversal, which is useful for operations like finding the k-th largest element.

A common interview question is about the relationship between `__reversed__`, `__iter__`, and `__getitem__`. If all three are defined, `reversed()` uses `__reversed__`, `for` loops use `__iter__`, and indexing uses `__getitem__`. They're independent protocols that serve different purposes. The `__reversed__` protocol is specifically for reverse iteration — it's not the same as `__iter__` running backwards.

In production systems, `__reversed__` is used in data structures that have efficient reverse access (like doubly-linked lists, deques, and skip lists), in UI components that need to render lists in reverse order, and in algorithms that require reverse traversal (like finding predecessors in sorted data). At Tesla, vehicle telemetry data stored in circular buffers uses `__reversed__` for efficient reverse chronological access.

**Example:**
```python
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def __reversed__(self):
        node = self.tail
        while node is not None:
            yield node.value
            node = node.prev

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next
```

## Q27: What is `__abs__` and when is unary negation different from subtraction?

**A:** `__abs__` is called by the built-in `abs()` function and should return the absolute value (or magnitude) of the object. For numeric types, this is straightforward — `abs(-5)` returns `5`. But for more complex types, "absolute value" can mean different things: for a complex number, it's the magnitude; for a vector, it could be the Euclidean norm; for a matrix, it could be the determinant's absolute value.

Unary negation (`-obj`) uses `__neg__`, which is different from `__sub__` (binary subtraction). `__neg__` takes no arguments (besides `self`), while `__sub__` takes another operand. This distinction is important: `-obj` calls `obj.__neg__()`, while `obj1 - obj2` calls `obj1.__sub__(obj2)`. They're different operations that happen to use similar syntax.

A common interview edge case: should `__abs__` return a new object or a numeric value? The answer depends on your type. For numeric types, it should return the same type (a complex number's absolute value is still a complex number, just with zero imaginary part). For geometric types (vectors, matrices), it should return a scalar. The `numbers.Number` ABC defines this contract.

In production systems at Tesla (sensor calibration) or Nvidia (matrix operations), `__abs__` is used for magnitude calculations, error bounds, and tolerance comparisons. A `Tolerance` class might define `__abs__` to return the confidence interval width, allowing `abs(measured - expected) < threshold` to work naturally. This pattern of making domain-specific comparisons work with built-in syntax is a hallmark of Pythonic design.

**Example:**
```python
import math

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

v = Vector(3, 4, 0)
print(abs(v))           # 5.0
print(abs(-v))          # 5.0
print(abs(v - Vector(0,0,0)))  # 5.0
```

## Q28: What is `__index__` and how does it relate to `__int__`?

**A:** `__index__` is called when an object needs to be converted to an integer for use as a sequence index, a slice, or a bitwise operation. It must return an `int`. `__int__` is called by `int()` and can return any integer-compatible value. The key distinction: `__index__` is specifically for contexts where an integer is required (like `list[obj]`), while `__int__` is for explicit conversion.

If `__int__` is defined but `__index__` is not, the object can't be used as a list index. If `__index__` is defined, `int()` also uses it as a fallback (since `int()` first tries `__int__`, then `__index__`). This means defining `__index__` alone covers both use cases, while defining `__int__` alone only covers explicit conversion.

A common interview question: "Can you use a custom object as a list index?" The answer: only if it defines `__index__`. This is why `numpy` arrays define `__index__` for their integer scalar types — so `arr[np.int64(5)]` works as expected. Without `__index__`, Python raises `TypeError: only integers, slices...`.

In production systems, `__index__` is used in: numpy integer types (for array indexing), custom index types (like database row IDs that wrap integers), and type-safe indices (a `PositiveInt` class that validates the value is positive). At senior level, know that `__index__` is also called for bit shifts (`obj << 3`), bitwise AND/OR/XOR, and as the stop argument in `range()`. This makes `__index__` more broadly useful than `__int__`.

**Example:**
```python
class MatrixIndex:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __index__(self):
        return self.row * 1000 + self.col  # Flat index

    def __int__(self):
        return self.row * 1000 + self.col

flat = [0] * 1000000
idx = MatrixIndex(5, 42)
print(flat[idx])        # Uses __index__
print(int(idx))         # Uses __int__
```

## Q29: How does `__matmul__` (`@`) operator work?

**A:** The `@` operator (matmul) was introduced in Python 3.5 (PEP 465) for matrix multiplication. It calls `__matmul__` for `a @ b`, `__rmatmul__` for reflected operations (`b @ a` when `a` doesn't know how), and `__imatmul__` for in-place operations (`a @= b`). The `@` symbol was chosen because `*` was already taken for element-wise multiplication, and `@` is already used in Python decorators (where it means "apply this to that").

The `@` operator is primarily used by numpy for matrix multiplication: `A @ B` performs matrix multiplication, not element-wise. This is a critical distinction — `A * B` is element-wise, `A @ B` is matrix multiplication. The `@` operator was designed specifically for this use case, and numpy's adoption made it a de facto standard.

For custom classes, `__matmul__` can mean anything you want, but semantic consistency is important. If your class represents a linear algebra object, `@` should mean matrix multiplication. If your class represents a transformation, `@` could mean composition. The key is that the operation should be associative (like matrix multiplication) to match user expectations.

In production systems at Nvidia (GPU computing) or Tesla (autonomous driving), `@` is used extensively for matrix operations, neural network forward passes, and geometric transformations. At senior level, know that `__matmul__` has the same reflected operation semantics as `__add__`: Python first tries `a.__matmul__(b)`, and if that returns `NotImplemented`, it tries `b.__rmatmul__(a)`. This allows seamless interoperability between different matrix types (numpy arrays, custom matrices, scipy sparse matrices).

**Example:**
```python
class Matrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    def __matmul__(self, other):
        result = [[0] * other.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result[i][j] += self.data[i][k] * other.data[k][j]
        return Matrix(result)

    def __repr__(self):
        return f"Matrix({self.data})"

a = Matrix([[1, 2], [3, 4]])
b = Matrix([[5, 6], [7, 8]])
print(a @ b)  # Matrix([[19, 22], [43, 50]])
```

## Q30: What is `__bytes__` and how does it differ from `__str__`?

**A:** `__bytes__` is called by the built-in `bytes()` function and should return a bytes representation of the object. While `__str__` returns a human-readable string, `__bytes__` returns a byte sequence suitable for I/O operations, network transmission, or binary file storage. The distinction is fundamental: strings are for text (Unicode), bytes are for raw data (binary).

In Python 3, `str` and `bytes` are completely separate types — you can't mix them without explicit encoding/decoding. `__bytes__` provides the bridge for custom objects that need to be serialized to binary format. For example, a `Packet` class might implement `__bytes__` to return the raw network packet data, while `__str__` returns a human-readable summary like "Packet from 192.168.1.1:80 to 10.0.0.1:443".

A common interview edge case: what about `__str__` vs `__repr__` for bytes-like objects? The `repr()` of a `bytes` object shows escaped ASCII (like `b'hello\\nworld'`), while `str()` of a `bytes` object shows the same thing (since `bytes.__str__` falls back to `bytes.__repr__`). But your custom class can differentiate: `__bytes__` returns the raw bytes, `__str__` returns a formatted description, and `__repr__` returns an unambiguous constructor-like string.

In production systems, `__bytes__` is used for: serialization (converting objects to wire format), encryption (preparing data for encryption), file I/O (writing binary data), and protocol buffers (converting objects to protobuf format). At senior level, know that `__bytes__` should return a `bytes` object, not a `str`. If you return a `str`, Python raises `TypeError`. Also, `bytes(obj)` calls `obj.__bytes__()`, and `memoryview(obj)` also uses it for buffer protocol integration.

**Example:**
```python
class IPAddress:
    def __init__(self, parts):
        self.parts = tuple(parts)

    def __bytes__(self):
        return bytes(self.parts)

    def __str__(self):
        return '.'.join(str(p) for self.parts)

    def __repr__(self):
        return f"IPAddress({list(self.parts)})"

ip = IPAddress([192, 168, 1, 1])
print(bytes(ip))   # b'\xc0\xa8\x01\x01'
print(str(ip))     # 192.168.1.1
```

## Q31: What is `__concat__` and `__iadd__` and how do mutable vs immutable types affect them?

**A:** There is no `__concat__` in Python — the `+` operator uses `__add__` for the result and `__radd__` for the reflected operation. The confusion with `__concat__` comes from other languages. In Python, `+` always maps to `__add__`, regardless of whether it's concatenation or addition. The semantics depend on the types involved: for lists, `+` creates a new list (concatenation); for numbers, `+` returns the sum.

`__iadd__` is the in-place addition operator, called by `+=`. For mutable types like lists, `__iadd__` modifies the list in place (extending it) and returns `self`. For immutable types like integers and tuples, `+=` creates a new object and rebinds the variable — `__iadd__` falls back to `__add__` and then reassignment. This is a critical performance distinction: `list += [1, 2, 3]` is O(1) (amortized), while `tuple += (1, 2, 3)` is O(n) (creates a new tuple).

The interview trap: does `a += b` always modify `a` in place? No — it depends on whether the type implements `__iadd__` as a true in-place modification. For lists, `__iadd__` calls `list.extend()` and returns `self`, so the original list is modified. For integers, `__iadd__` doesn't exist (integers are immutable), so Python falls back to `__add__` + reassignment. You can observe this with `id()`: `id(a)` changes for immutable types after `+=` but stays the same for mutable types.

In production systems, understanding `+=` semantics is critical for performance. In a loop that builds a list, `result += [item]` is much faster than `result = result + [item]` because the former uses `__iadd__` (in-place) while the latter uses `__add__` (creates a new list each time, O(n²) total). At Tesla, real-time data aggregation pipelines rely on this distinction for performance. Always use `__iadd__` (via `+=`) when you want to extend a mutable collection in a loop.

**Example:**
```python
class Vector:
    def __init__(self, components):
        self.components = list(components)

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.components, other.components)])

    def __iadd__(self, other):
        self.components = [a + b for a, b in zip(self.components, other.components)]
        return self  # Modified in place

v1 = Vector([1, 2, 3])
v2 = Vector([4, 5, 6])
v1 += v2
print(v1.components)  # [5, 7, 9]
print(id(v1))         # Same object (in-place)
```

## Q32: What is `__truediv__`, `__floordiv__`, and `__divmod__`?

**A:** These dunder methods implement division operations: `__truediv__` for `/` (true division, always returns float in Python 3), `__floordiv__` for `//` (floor division, returns the floor of the quotient), and `__divmod__` for `divmod(a, b)` which returns a tuple `(a // b, a % b)`. Python 3 also has `__truediv__` instead of `__div__` (which was Python 2's `/` operator that did integer division for integers).

The relationship between these methods is mathematically precise: for any `a` and `b`, `divmod(a, b)` returns `(a // b, a % b)` where `a == (a // b) * b + (a % b)`. This invariant holds for all types, including floats and negative numbers. Implementing `__divmod__` allows you to compute both the quotient and remainder in a single operation, which can be more efficient than computing them separately (especially for big integers or modular arithmetic).

A common interview edge case: floor division vs. truncation. `7 // 2` returns `3` (floor), while `int(7 / 2)` returns `3` (truncation toward zero). For negative numbers, they differ: `-7 // 2` returns `-4` (floor), while `int(-7 / 2)` returns `-3` (truncation). Python uses floor division for `//`, which is mathematically consistent but can surprise developers coming from C/Java. Your `__floordiv__` should always return the floor, not truncation.

In production systems, these operators are used for: coordinate systems (grid snapping), financial calculations (division with remainders), time calculations (converting seconds to hours:minutes:seconds), and cryptographic operations (modular arithmetic). At senior level, know that `__mod__` (for `%`) has its own dunder method and that custom types can define different semantics for `%` — for example, Python's `datetime.timedelta` uses `%` for modular time arithmetic.

**Example:**
```python
class Fraction:
    def __init__(self, num, den):
        self.num = num
        self.den = den

    def __truediv__(self, other):
        return Fraction(self.num * other.den, self.den * other.num)

    def __floordiv__(self, other):
        return (self.num * other.den) // (self.den * other.num)

    def __divmod__(self, other):
        q = self // other
        r = self - Fraction(q * other.num, other.den)
        return q, r

    def __repr__(self):
        return f"Fraction({self.num}, {self.den})"

f1 = Fraction(7, 2)
f2 = Fraction(3, 1)
print(f1 / f2)       # Fraction(7, 6)
print(f1 // f2)      # 1
print(divmod(f1, f2))  # (1, Fraction(1, 6))
```

## Q33: What is `__pow__` and how does the three-argument form work?

**A:** `__pow__` is called by the `**` operator (exponentiation). It takes two arguments: `self` and `exp`. The three-argument form `pow(base, exp, mod)` calls `__pow__` with three arguments: `base.__pow__(exp, mod)`. This three-argument form is specifically for modular exponentiation, which is critical in cryptography and number theory.

The three-argument `pow()` is optimized for modular exponentiation — it uses efficient algorithms (like square-and-multiply) that are much faster than computing `base ** exp % mod` directly. For large numbers (hundreds of digits), the difference can be orders of magnitude. This is why Python's `pow()` with three arguments is the standard for RSA encryption, Diffie-Hellman key exchange, and other cryptographic operations.

A common interview question: "How do you implement `__pow__` for your custom class?" The answer should cover both the two-argument form (`obj ** exp`) and the three-argument form (`pow(obj, exp, mod)`). If you only implement `__pow__(self, exp)`, the three-argument `pow()` will raise `TypeError`. You must implement `__pow__(self, exp, mod=None)` to support both forms. When `mod` is `None`, you're doing regular exponentiation; when it's provided, you're doing modular exponentiation.

In production systems at FAANG (cryptography), Tesla (secure communications), and Nvidia (random number generation), modular exponentiation is used extensively. The `pow(base, exp, mod)` function is also used in hashing algorithms, primality testing, and digital signatures. At senior level, know that `__rpow__` handles the reflected case (`exp ** obj`) and that `__ipow__` handles `**=`. The three-argument form doesn't have a reflected version because `mod` must be the third argument.

**Example:**
```python
class ModularInt:
    def __init__(self, value, modulus):
        self.value = value % modulus
        self.modulus = modulus

    def __pow__(self, exp, mod=None):
        if mod is not None:
            result = pow(self.value, exp, mod)
        else:
            result = pow(self.value, exp, self.modulus)
        return ModularInt(result, self.modulus)

    def __repr__(self):
        return f"ModularInt({self.value}, {self.modulus})"

a = ModularInt(3, 7)
print(a ** 2)          # ModularInt(2, 7)
print(pow(a, 5, 7))   # ModularInt(5, 7)
```

## Q34: How does `__radd__` (and other reflected methods) work?

**A:** Reflected dunder methods (like `__radd__`, `__rsub__`, `__rmul__`, etc.) are called when the left operand doesn't know how to perform the operation. When Python evaluates `a + b`, it first tries `a.__add__(b)`. If that returns `NotImplemented` (not raises `TypeError`, but returns the `NotImplemented` singleton), Python then tries `b.__radd__(a)`. If that also returns `NotImplemented`, Python raises `TypeError`.

The `NotImplemented` return value is a critical concept. It's not an exception — it's a signal that says "I don't know how to handle this operation." If your `__add__` receives an operand of a type it doesn't recognize, it should `return NotImplemented`, not raise `TypeError`. This allows the other operand to try its reflected method. This protocol is what enables seamless interoperability between different numeric types — numpy arrays can add to Python lists, and vice versa, because they each implement reflected methods.

A common interview mistake: confusing `NotImplemented` (the singleton) with `NotImplementedError` (the exception). `NotImplemented` is a special constant returned to signal that an operation is not supported. `NotImplementedError` is an exception raised when a method is not implemented (typically in abstract methods). Mixing them up causes subtle bugs.

In production systems, reflected methods are essential for: type interoperability (numpy + Python scalars), operator chaining (`a + b + c` where different types are involved), and arithmetic expression libraries. At senior level, know that `__radd__` is called with the OTHER operand as the first argument — `b.__radd__(a)` is called when `a + b` fails, with `self=b` and `other=a`. This means the reflected method should implement the operation from the perspective of the right operand.

**Example:**
```python
class Scalar:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if isinstance(other, Scalar):
            return Scalar(self.value + other.value)
        return NotImplemented

    def __radd__(self, other):
        # Called when: int + Scalar (int doesn't know about Scalar)
        if isinstance(other, (int, float)):
            return Scalar(other + self.value)
        return NotImplemented

s = Scalar(10)
print(s + Scalar(5))    # Scalar(15)  (uses __add__)
print(3 + s)            # Scalar(13)  (uses __radd__)
print([1, 2] + s)       # TypeError
```

## Q35: What is `__enter__` returning a different object than `self`?

**A:** `__enter__` can return any object — it doesn't have to return `self`. This is a powerful pattern where the context manager creates and returns a different object that's more convenient to use. The object returned by `__enter__` is what gets bound to the `as` variable in `with` statements. Meanwhile, `__exit__` still receives the original context manager (not the returned object), so it has access to the resources it needs for cleanup.

This pattern is used when the "usage" object is different from the "management" object. For example, a database connection manager might return a cursor object from `__enter__`, while `__exit__` handles committing/rolling back the transaction and closing the connection. A file manager might return a buffered reader from `__enter__`, while `__exit__` handles closing the file descriptor.

A subtle interview question: "If `__enter__` returns a different object, which object does `__exit__` receive?" The answer is `__exit__` always receives the original context manager instance (the `self` of `__enter__`), NOT the object returned by `__enter__`. This means if you need to clean up state from the returned object, you must store a reference to it in `__enter__` before returning.

In production systems, this pattern is ubiquitous. SQLAlchemy sessions return `Session` objects from `__enter__` that manage the transaction lifecycle. Threading locks return the lock object itself from `__enter__`. Temporary directories create a `TemporaryDirectory` object that returns a `str` path from `__enter__`. At senior level, know that `contextlib.contextmanager` also supports this pattern — the value yielded by the generator is bound to `as`, while the generator itself manages cleanup.

**Example:**
```python
class DatabaseTransaction:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = None

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self.cursor  # Returns cursor, not self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.cursor.close()
        return False

with DatabaseTransaction(conn) as cursor:
    cursor.execute("INSERT INTO ...")
# cursor is the returned object, not the DatabaseTransaction
```

## Q36: What is `__delattr__` and how does it differ from `__setattr__`?

**A:** `__delattr__` is called when you use `del obj.attr` on an object. It receives the attribute name as a string and should delete the corresponding attribute. It's the mirror of `__setattr__` — while `__setattr__` intercepts all attribute assignments, `__delattr__` intercepts all attribute deletions. Both are called unconditionally, regardless of whether the attribute exists.

A critical difference: `__delattr__` should raise `AttributeError` if the attribute doesn't exist (matching the behavior of `del` on regular objects). `__setattr__` doesn't have this constraint because assignment always creates or modifies an attribute. If `__delattr__` doesn't raise `AttributeError` for non-existent attributes, code that checks `hasattr(obj, attr)` followed by `delattr(obj, attr)` could break (because `hasattr` checks for `AttributeError`).

A common interview pattern: implementing write-once-delete-never attributes. This requires both `__setattr__` (to prevent reassignment) and `__delattr__` (to prevent deletion). The implementation checks whether the attribute already exists before allowing creation, and always raises `AttributeError` in `__delattr__`. This pattern is used in configuration objects where critical values (like API keys or security settings) must be set once and never changed.

In production systems, `__delattr__` is used for: protected attributes (preventing accidental deletion), audit trails (logging all deletions), and proxy objects (forwarding deletions to a wrapped object). At Tesla, vehicle configuration objects use `__delattr__` to prevent deletion of safety-critical parameters. At senior level, know that `__delattr__` has the same infinite recursion pitfall as `__setattr__` — use `super().__delattr__(name)` or `object.__delattr__(self, name)` to avoid it.

**Example:**
```python
class WriteOnce:
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError(f"Cannot reassign '{name}'")
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        raise AttributeError(f"Cannot delete '{name}'")

config = WriteOnce()
config.host = "localhost"  # OK
# config.host = "0.0.0.0"  # AttributeError: Cannot reassign 'host'
# del config.host          # AttributeError: Cannot delete 'host'
```

## Q37: What is `__dir__` and when should you customize it?

**A:** `__dir__` is called by the built-in `dir()` function and should return an iterable of strings representing the names of the attributes of the object. By default, Python computes `dir()` by collecting: the instance's `__dict__` keys, the class's `__dict__` keys, and all base class `__dict__` keys (following MRO). Customizing `__dir__` allows you to add, remove, or reorder attributes in the listing.

You should customize `__dir__` when: (1) you have dynamically computed attributes (like `__getattr__`-backed lazy loading) that should appear in `dir()` but don't exist in `__dict__`, (2) you want to hide internal attributes from the listing, (3) you want to provide a more organized or relevant listing than the default. The `dir()` output is often used in interactive environments (Jupyter notebooks, REPLs) for autocompletion, so including dynamic attributes improves the developer experience.

A common interview question: "If you implement `__getattr__` for lazy loading, should the attribute appear in `dir()`?" The answer is yes, for usability, but it's not automatic. You need to customize `__dir__` to include the dynamic attributes. Without customization, `dir()` won't show them, making them invisible to autocompletion and documentation tools.

In production systems, `__dir__` is used in: dynamic objects (like database records with varying schemas), proxy objects (forwarding `dir()` to the wrapped object), and API clients (showing only the publicly available methods). At senior level, know that `dir()` sorts its output by default, but your `__dir__` can return an unsorted iterable — `dir()` will sort it automatically. Also, `dir()` on a class lists class attributes, while `dir()` on an instance lists instance + class attributes.

**Example:**
```python
class API:
    def __init__(self, endpoints):
        self.endpoints = endpoints

    def __getattr__(self, name):
        if name in self.endpoints:
            return lambda **kwargs: self._call(name, kwargs)
        raise AttributeError(name)

    def __dir__(self):
        standard = list(super().__dir__())
        return sorted(standard + list(self.endpoints.keys()))

    def _call(self, name, kwargs):
        return f"Calling {name} with {kwargs}"

api = API(["users", "posts", "comments"])
print("users" in dir(api))  # True
```

## Q38: What is `__class_getitem__` and how does it enable generic types?

**A:** `__class_getitem__` (PEP 560) is called when you use subscript notation on a class itself (not an instance). For example, `List[int]`, `Dict[str, int]`, or `MyClass[SomeType]`. It receives the class and the item (the content inside the brackets) and should return something appropriate — typically a `types.GenericAlias` or a `typing._GenericAlias` for type hinting.

Before `__class_getitem__`, you had to use metaclasses or `__getitem__` on the class (which conflicts with instance indexing) to implement generic types. `__class_getitem__` is cleaner because it's specifically for class-level subscripting. It was introduced to make `typing` types work with subscript syntax: `List[int]`, `Dict[str, Any]`, etc., all use `__class_getitem__` internally.

A common interview question: "How does `list[int]` work in Python 3.9+?" The answer is that `list` (the built-in type) implements `__class_getitem__`, which returns a `types.GenericAlias` object. This object is used for type hints and doesn't actually affect runtime behavior — `list[int]` is still just a `list` at runtime. However, this is changing with PEP 695 (Python 3.12+) which adds more formal type parameter syntax.

In production systems, `__class_getitem__` is used for: type hints (generic types), runtime type validation (checking generic parameters at runtime), and DSL creation (subscript syntax for configuration). At senior level, know that `__class_getitem__` receives the class as the first argument (like a classmethod) and the subscripted value as the second. If the class also implements `__getitem__` for instance access, there's no conflict — Python distinguishes between `Class[item]` (calls `__class_getitem__`) and `instance[item]` (calls `__getitem__`).

**Example:**
```python
class Repository:
    _type_params = {}

    def __class_getitem__(cls, item):
        cls._type_params[cls] = item
        return cls

    def __init__(self, items=None):
        self.items = list(items or [])

    def get_type(self):
        return self._type_params.get(type(self))

repo = Repository[int]([1, 2, 3])
print(repo.get_type())  # <class 'int'>
```

## Q39: What is `__fspath__` and how does it enable path-like objects?

**A:** `__fspath__` (PEP 519) is called by `os.fspath()` and by functions that accept path-like objects (like `open()`, `os.path.join()`, `pathlib.Path`). It should return a `str` or `bytes` representing the file system path. This protocol allows custom objects to be used wherever file paths are expected, without inheriting from `pathlib.Path` or `str`.

The protocol was introduced to standardize how path-like objects work across Python's standard library. Before PEP 519, you had to check if an argument was a `str`, `bytes`, or `pathlib.Path` and handle each case. With `__fspath__`, any object that implements the method can be used as a path. `pathlib.Path.__fspath__` returns the string representation of the path.

A common interview edge case: should `__fspath__` return `str` or `bytes`? The answer depends on your use case. For most applications, return `str` (POSIX paths are strings). Return `bytes` only when you need to handle raw byte paths (like paths from C libraries). If you return `bytes`, be aware that some functions (like `os.scandir()`) may not accept bytes paths on all platforms. Always prefer `str` unless you have a specific reason for `bytes`.

In production systems, `__fspath__` is used in: custom path objects (like S3 paths, database URIs), configuration objects (where a path is one of many fields), and API wrappers (where paths are constructed dynamically). At Tesla, log file paths are managed by objects that implement `__fspath__` to support both local and remote storage paths. At senior level, know that `__fspath__` can return a different path than the original — for example, a `TempPath` object might return the actual temporary directory path from `__fspath__`.

**Example:**
```python
import os

class RemotePath:
    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key

    def __fspath__(self):
        return f"s3://{self.bucket}/{self.key}"

    def __str__(self):
        return self.__fspath__()

path = RemotePath("my-bucket", "data/file.csv")
print(os.fspath(path))  # s3://my-bucket/data/file.csv
```

## Q40: What is `__bool__`'s interaction with `__len__` for custom containers?

**A:** When Python needs to evaluate the truthiness of an object (in `if obj:`, `while obj:`, etc.), it follows this priority: (1) call `__bool__()` if defined, (2) fall back to `__len__()` and return `True` if the result is non-zero, (3) default to `True`. This means for a container with `__len__` returning 0, the object is falsy; with `__len__` returning non-zero, it's truthy.

The edge case interviewers love: what if `__bool__` is not defined but `__len__` is? Then `bool(obj)` calls `len(obj)` and checks if it's zero. For large containers, this is expensive — it computes the full length just to check truthiness. This is why the Zen of Python says "Explicit is better than implicit" — always define `__bool__` if truthiness checks are common. For a linked list, `__bool__` should check `self.head is not None` (O(1)), not `len(self) > 0` (O(n)).

Another subtle point: the `__bool__` return value must be `True` or `False` — returning a truthy/falsy value (like `1` or `""`) doesn't work. Python calls `bool()` on the return value, so returning `1` works (it's truthy), but it's better practice to explicitly return `True` or `False`. If `__bool__` is not defined, the `__len__` fallback returns `True` if `len() != 0`, which is already a boolean.

In production systems, this interaction matters for: database query results (checking if a query returned any rows), cached data (checking if the cache is populated), and collection classes (checking if a buffer has data). At senior level, discuss the performance implications: if your `__len__` is O(n) and you only need truthiness, always define `__bool__` as O(1). This is a common optimization in FAANG-scale systems where millions of truthiness checks happen per second.

**Example:**
```python
class StreamBuffer:
    def __init__(self):
        self._chunks = []

    def __len__(self):
        return sum(len(c) for c in self._chunks)

    def __bool__(self):
        return bool(self._chunks)  # O(1) instead of O(n)

    def append(self, chunk):
        self._chunks.append(chunk)

buf = StreamBuffer()
if not buf:  # O(1) thanks to __bool__
    buf.append("data")
```

## Q41: What is the `__radd__` vs `__add__` priority and when is each called?

**A:** When Python evaluates `a + b`, it first tries `a.__add__(b)`. If that returns `NotImplemented`, Python tries `b.__radd__(a)`. If both return `NotImplemented`, Python raises `TypeError`. The right-hand method is only called when the left-hand method fails or doesn't know how to handle the operation. This is the "reflected" or "swapped" operation protocol.

The priority system is designed for type interoperability. When you add a `float` to a custom `Vector` type, the `float.__add__(vector)` returns `NotImplemented` (float doesn't know about Vector), so Python tries `vector.__radd__(float)`. This allows the `Vector` to handle the operation. Without reflected methods, you'd need to modify every built-in type to support your custom types.

A common interview question: "Why is `__radd__` sometimes called even when `__add__` exists?" The answer is that `__radd__` is called when the left operand's `__add__` returns `NotImplemented`. This can happen when: (1) the types are incompatible, (2) the left operand explicitly returns `NotImplemented` for this case, or (3) the left operand doesn't have an `__add__` method at all. It's not an error — it's the normal flow for type interoperability.

In production systems, reflected methods are essential for: numeric type interoperability (numpy + Python scalars), operator chaining (`a + b + c` with mixed types), and expression libraries (like symbolic math). At senior level, know that `__radd__` receives `self` as the right operand and the other operand as the argument — in `b.__radd__(a)`, `self` is `b` and the argument is `a`. This means the reflected method should implement the operation from the right operand's perspective.

**Example:**
```python
class Meters:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if isinstance(other, Meters):
            return Meters(self.value + other.value)
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (int, float)):
            return Meters(other + self.value)
        return NotImplemented

m = Meters(100)
print(m + Meters(50))   # Meters(150)  (__add__)
print(25 + m)           # Meters(125)  (__radd__)
```

## Q42: What is `__sizeof__` vs `sys.getsizeof` and when do they differ?

**A:** `__sizeof__` is a method that returns the size in bytes of the object itself (shallow size), not including the size of objects it references. `sys.getsizeof()` calls `__sizeof__()` and adds the garbage collector overhead (which varies by Python implementation — CPython adds 16 bytes for GC-tracked objects). The two always differ by the GC overhead, but the difference can be much larger for objects with external data.

The default `__sizeof__` (from `object`) returns a fixed value based on the object's internal layout. For classes with `__slots__`, the size is smaller than for classes with `__dict__` (because `__dict__` is an additional dict object). If your class stores data in external structures (C buffers, numpy arrays, mmap'd files), `sys.getsizeof()` won't reflect the actual memory usage — you need to override `__sizeof__` to include the external data size.

A common interview question: "How do you measure the total memory of an object including all its references?" The answer is that `sys.getsizeof()` alone doesn't do this — it only gives the shallow size. For total size, you need `pympler.asizeof` or a custom recursive traversal. Python's `gc.get_objects()` can help you find all objects, but computing the total size of a complex object graph requires traversal.

In production systems, accurate memory reporting is critical for: memory profiling (finding leaks), capacity planning (estimating how many objects fit in memory), and resource management (ensuring you don't OOM). At Tesla, embedded systems with limited RAM require precise memory tracking. At Nvidia, GPU memory management requires knowing the exact size of tensors and buffers. Override `__sizeof__` to report accurate sizes for your domain.

**Example:**
```python
import sys

class Matrix:
    __slots__ = ('data',)

    def __init__(self, data):
        self.data = data

    def __sizeof__(self):
        return sys.getsizeof(self.data)

m = Matrix([1, 2, 3, 4, 5])
print(f"Shallow: {sys.getsizeof(m)} bytes")
print(f"Data:    {sys.getsizeof(m.data)} bytes")
print(f"Total:   {sys.getsizeof(m) + sys.getsizeof(m.data)} bytes")
```

## Q43: What is `__array__` and how does numpy integration work?

**A:** `__array__` is a special dunder method called by `numpy.asarray()` and `numpy.array()` to convert a custom object into a numpy array. It should return a `numpy.ndarray`. This is the standard protocol for integrating custom types with numpy's ecosystem. When you call `numpy.array(my_obj)`, numpy first checks if `my_obj` has `__array__`, and if so, calls it to get the array.

This is different from the buffer protocol (`__buffer__`/`__releasebuffer__`) which is a lower-level interface. `__array__` is higher-level and easier to implement — you just need to return a numpy array. The buffer protocol is more efficient for large data because it avoids copying, but it's more complex to implement. For most use cases, `__array__` is sufficient.

A common interview edge case: what about `__array_function__` and `__array_ufunc__`? These are more advanced numpy integration protocols. `__array_function__` allows your type to override numpy functions like `np.sum()`, `np.dot()`, etc. `__array_ufunc__` allows overriding numpy ufuncs like `np.sin()`, `np.exp()`, etc. These are used by types like pandas DataFrames and astropy Quantities to integrate deeply with numpy.

In production systems at Nvidia (GPU computing) and Tesla (data processing), numpy integration is essential. Custom array types (GPU arrays, distributed arrays, sparse matrices) implement `__array__` to work with numpy's ecosystem. At senior level, know that `__array__` can accept a `dtype` argument to control the output type, and that returning a non-contiguous array may cause unexpected behavior in some numpy operations.

**Example:**
```python
import numpy as np

class GeoGrid:
    def __init__(self, rows, cols, data):
        self.rows = rows
        self.cols = cols
        self.data = data

    def __array__(self, dtype=None):
        return np.array(self.data, dtype=dtype).reshape(self.rows, self.cols)

grid = GeoGrid(2, 3, [1, 2, 3, 4, 5, 6])
arr = np.asarray(grid)
print(arr.shape)  # (2, 3)
```

## Q44: What is `__bytes__` vs `__str__` for serialization?

**A:** `__bytes__` returns the byte representation of an object (for binary I/O, network transmission, encryption), while `__str__` returns the human-readable string representation. In Python 3, these are completely separate — you can't use a `str` where `bytes` is expected, and vice versa. This separation is deliberate and enforces clear handling of text vs. binary data.

For serialization, the choice depends on the use case: `__bytes__` for binary serialization (pickle, msgpack, protobuf), `__str__` for text serialization (JSON, XML, YAML). A well-designed serializable object should implement both, with `__bytes__` returning the binary format and `__str__` returning a human-readable summary (not the full serialized form).

A common interview question: "How does `pickle` use `__bytes__`?" The answer is that pickle doesn't use `__bytes__` directly — it uses `__getstate__` and `__setstate__` for custom serialization. `__bytes__` is for `bytes()` calls, not for pickle. However, `__bytes__` is used by `codecs.encode()` and some network protocols. If you want custom pickle behavior, use `__reduce__` or `__getstate__`/`__setstate__`.

In production systems, the distinction matters for: network protocols (binary vs. text protocols), file formats (binary files vs. text files), and encryption (encryption works on bytes, not strings). At Tesla, vehicle telemetry data is serialized to bytes for transmission over CAN bus. At FAANG, API responses are typically serialized to JSON strings, while internal data structures use binary formats for efficiency. At senior level, know that `__bytes__` should return `bytes`, not `str`. Returning `str` from `__bytes__` raises `TypeError`.

**Example:**
```python
class Message:
    def __init__(self, sender, body, priority):
        self.sender = sender
        self.body = body
        self.priority = priority

    def __bytes__(self):
        header = f"{self.sender}:{self.priority}:".encode()
        return header + self.body.encode()

    def __str__(self):
        return f"[{self.priority}] {self.sender}: {self.body}"

msg = Message("alice", "hello", "high")
print(bytes(msg))  # b'alice:high:hello'
print(str(msg))    # [high] alice: hello
```

## Q45: What is `__format__` and how does it interact with f-strings?

**A:** `__format__` is called by the built-in `format()` function, f-strings, and `str.format()`. When you write `f"{obj:spec}"`, Python calls `obj.__format__(spec)`. The `spec` is the format specification string (like `".2f"` for floats or `">10"` for right-aligned strings). If `__format__` is not defined, Python falls back to `str(obj)` with the spec applied to the resulting string.

The interaction with f-strings is seamless: `f"{obj:.2f}"` is equivalent to `format(obj, ".2f")`, which calls `obj.__format__(".2f")`. This means your custom objects can support rich formatting through f-strings without any special syntax. The format spec becomes a mini-DSL for your domain — you can parse it however you like.

A common interview edge case: what about nested format specs? For example, `f"{obj:>10.2f}"`. This is parsed by Python's format spec mini-language, which splits it into fill, align, sign, width, precision, and type. Your `__format__` receives the entire spec string, so you need to parse it yourself if you want to support the mini-language. Alternatively, you can define your own spec syntax (like `f"{obj:km}"` for kilometers) and parse it in `__format__`.

In production systems, `__format__` is used for: report generation (formatting financial data with locale-specific separators), logging (formatting objects with context-specific detail levels), and API responses (formatting objects differently for different clients). At senior level, know that `format(obj, '')` calls `obj.__format__('')`, which is also what `str(obj)` does if `__str__` is not defined. This means `__format__` can serve as a fallback for `__str__`.

**Example:**
```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __format__(self, spec):
        if spec == '' or spec == 'c':
            return f"{self.celsius:.1f}°C"
        elif spec == 'f':
            return f"{self.celsius * 9/5 + 32:.1f}°F"
        elif spec == 'k':
            return f"{self.celsius + 273.15:.2f}K"
        return format(self.celsius, spec)

t = Temperature(100)
print(f"{t}")       # 100.0°C
print(f"{t:f}")     # 212.0°F
print(f"{t:k}")     # 373.15K
```

## Q46: What is `__iter__` for generators vs iterator classes?

**A:** Generators (functions with `yield`) automatically implement both `__iter__` and `__next__`. When you call a generator function, it returns a generator object that has both methods. Iterator classes require you to explicitly implement both `__iter__` (returning `self`) and `__next__` (returning the next value or raising `StopIteration`). The behavior is identical, but the implementation differs.

Generators are simpler and more concise for straightforward iteration logic. Iterator classes are better when: (1) you need the iterator to have additional methods (like `peek()` or `close()`), (2) you need to pickle the iterator (generators can't be pickled), (3) you need to inspect the iterator's state, or (4) the iteration logic is complex and benefits from explicit state management.

A common interview question: "When would you choose an iterator class over a generator?" The answer involves understanding the trade-offs: generators are syntactically cleaner and more Pythonic for simple cases, but iterator classes provide more control and flexibility. For example, a `ChunkedReader` iterator that reads files in chunks might benefit from being a class (you can add `close()`, `__len__`, and state inspection methods). A simple `range`-like iterator is cleaner as a generator.

In production systems, generators are preferred for: data pipelines (chain of transformations), lazy evaluation (computing values on demand), and memory-efficient iteration (processing large files without loading everything into memory). Iterator classes are preferred for: complex state machines (like protocol parsers), objects that need to be serialized (distributed systems at FAANG), and objects that need additional methods beyond `__iter__`/`__next__`. At senior level, know that generators have a hidden advantage: they automatically close when garbage collected (via `GeneratorExit`), while iterator classes need explicit cleanup.

**Example:**
```python
class WindowIterator:
    def __init__(self, iterable, size):
        self.iterable = iter(iterable)
        self.size = size
        self.buffer = []
        self._fill_buffer()

    def _fill_buffer(self):
        while len(self.buffer) < self.size:
            try:
                self.buffer.append(next(self.iterable))
            except StopIteration:
                break

    def __iter__(self):
        return self

    def __next__(self):
        if not self.buffer:
            raise StopIteration
        result = tuple(self.buffer)
        self.buffer.pop(0)
        self._fill_buffer()
        return result

print(list(WindowIterator(range(7), 3)))
# [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6)]
```

## Q47: What is `__class__` and how does it relate to metaclasses?

**A:** `__class__` is an attribute that returns the class of an instance. For a regular object `obj`, `obj.__class__` returns the class that created it. For a class `MyClass`, `MyClass.__class__` returns the metaclass (the class of the class). This is how Python implements the type hierarchy: every class is an instance of its metaclass, and the default metaclass is `type`.

The `__class__` assignment is a powerful (and dangerous) feature that allows you to change an object's class at runtime. When you write `obj.__class__ = OtherClass`, Python changes the object's class pointer without creating a new object. This is used in some design patterns (like the State pattern) but is generally discouraged because it can break invariants and confuse debugging tools.

A common interview question: "What is `type(obj)` vs `obj.__class__`?" The answer is that they're usually the same, but `type()` is more reliable because `__class__` can be overridden by descriptors. `type(obj)` always returns the actual class, while `obj.__class__` returns whatever the class's `__class__` descriptor returns. For most objects, they're identical.

In production systems, `__class__` is used in: type checking (though `isinstance()` is preferred), debugging (showing the actual class of an object), and dynamic class switching (rare, but used in some ORM and state machine patterns). At senior level, know that `__class__` is a descriptor defined on `object`, and it can be overridden by a metaclass. Metaclasses can use `__class__` to control how class objects behave, including changing what `type()` returns for instances.

**Example:**
```python
class Meta(type):
    def __instancecheck__(cls, instance):
        return hasattr(instance, 'compatible_interface')

class Base(metaclass=Meta):
    def compatible_interface(self):
        return True

class Child(Base):
    pass

obj = Child()
print(obj.__class__)              # <class 'Child'>
print(type(obj))                  # <class 'Child'>
print(isinstance(obj, Base))      # True (Meta.__instancecheck__)
```

## Q48: What is `__init_subclass__` and how does it replace metaclasses for class customization?

**A:** `__init_subclass__` (PEP 487) is called when a class is subclassed. It's defined on the parent class and receives the newly created subclass as its first argument (plus any keyword arguments from the class definition). This provides a simpler alternative to metaclasses for many common class customization patterns: plugin registration, validation, and configuration.

Before `__init_subclass__`, the only way to run code when a class was subclassed was through metaclasses. Metaclasses are powerful but complex — they affect the entire class creation process, are hard to compose (you can only have one metaclass), and can cause subtle bugs. `__init_subclass__` is simpler, more explicit, and composable — you can have multiple parent classes that each define `__init_subclass__`.

A common interview question: "When should you use `__init_subclass__` vs. metaclasses?" The answer: use `__init_subclass__` for simple class customization (registration, validation, configuration). Use metaclasses only when you need to change fundamental aspects of class creation (like controlling `__new__`, `__prepare__`, or the class dictionary). Most class customization needs are covered by `__init_subclass__`.

In production systems, `__init_subclass__` is used for: plugin systems (automatically registering subclasses), validation frameworks (ensuring subclasses implement required methods), and configuration systems (setting up class-level state). At senior level, know that `__init_subclass__` is called AFTER the subclass is created and fully initialized, while metaclass `__init__` is called DURING creation. This means `__init_subclass__` can't control class creation, only post-process it.

**Example:**
```python
class Plugin:
    _registry = {}

    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__
        Plugin._registry[name] = cls
        cls._validate()

    @classmethod
    def _validate(cls):
        if not hasattr(cls, 'process'):
            raise TypeError(f"{cls.__name__} must define 'process' method")

class AuthPlugin(Plugin, plugin_name="auth"):
    def process(self):
        return "authenticated"

class LogPlugin(Plugin, plugin_name="logger"):
    def process(self):
        return "logged"

print(Plugin._registry)  # {'auth': AuthPlugin, 'logger': LogPlugin}
```

## Q49: Why do descriptors need to know their owning class, and which hook in Python provides that information automatically?

**A:** `__set_name__` is called automatically when a class is created (PEP 487). It receives two arguments: the owner class (the class that contains the descriptor) and the attribute name (the name the descriptor was assigned to in the class). This eliminates the need for metaclass-based name injection, which was the standard approach before Python 3.6.

Before `__set_name__`, descriptors had to be explicitly told their name through metaclass magic or manual configuration. For example, Django's `Field` descriptor required a `contribute_to_class` method called by the metaclass. With `__set_name__`, the descriptor can automatically know its name when it's used in a class definition, making descriptor implementations much cleaner.

A common use case is field validation in ORM-like systems. A `Field` descriptor can use `__set_name__` to store its attribute name and use it in error messages, storage keys, and database column names. This enables the clean Django-style syntax: `class User: name = CharField(max_length=100)` where `name` automatically becomes the field name.

In production systems, `__set_name__` is used extensively in data validation frameworks (Pydantic, Marshmallow), ORM systems (SQLAlchemy), and configuration systems. At senior level, note that `__set_name__` is only called when the descriptor is assigned as a class attribute — it's NOT called when the descriptor is created or when it's assigned to an instance. Also, if a descriptor is reassigned in a subclass, `__set_name__` is called again with the new name.

**Example:**
```python
class ValidatedField:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_field_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, None)

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be a string")
        setattr(obj, self.storage, value)

class User:
    name = ValidatedField()
    email = ValidatedField()

u = User()
u.name = "Alice"
print(u.name)  # Alice
```

## Q50: What is `__init_subclass__` keyword arguments and how are they passed?

**A:** When you subclass a class that defines `__init_subclass__`, you can pass keyword arguments in the class definition: `class Child(Parent, key=value)`. These keyword arguments are forwarded to `__init_subclass__` of each ancestor class (following MRO). This enables a declarative style for class configuration without metaclasses.

The keyword arguments are passed to ALL `__init_subclass__` methods in the MRO, not just the immediate parent. This means if multiple ancestors define `__init_subclass__`, they all receive the same keyword arguments. You must use `**kwargs` and pass them to `super().__init_subclass__(**kwargs)` to ensure the chain works correctly. Forgetting to forward kwargs breaks the inheritance chain.

A common interview edge case: what happens if a keyword argument is consumed by one `__init_subclass__` but not forwarded? The answer is that downstream `__init_subclass__` methods won't receive it. This can cause unexpected `TypeError` if a downstream class expects that keyword. Always forward all kwargs unless you intentionally want to consume them. The `**kwargs` pattern is the standard approach.

In production systems, keyword arguments to `__init_subclass__` are used for: plugin configuration (passing plugin-specific settings), validation rules (passing constraints to validators), and database schema (passing column types and constraints). At senior level, know that `__init_subclass__` is called on the PARENT class, not the child class. So `class Child(Parent, key=value)` calls `Parent.__init_subclass__(key=value)` with `cls=Child`. This is a subtle but important distinction.

**Example:**
```python
class Configurable:
    def __init_subclass__(cls, config_key=None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._config_key = config_key or cls.__name__.lower()

class DatabaseConfig(Configurable, config_key="db"):
    pass

class CacheConfig(Configurable, config_key="cache"):
    pass

print(DatabaseConfig._config_key)  # 'db'
print(CacheConfig._config_key)     # 'cache'
```

## Q51: What are Abstract Base Classes (ABCs) and how do they differ from interfaces?

**A:** ABCs (Abstract Base Classes) are classes that cannot be instantiated and define abstract methods that subclasses must implement. They're defined using the `abc.ABC` base class or `abc.ABCMeta` metaclass, with methods decorated with `@abstractmethod`. Unlike interfaces in Java/C#, ABCs can contain concrete methods (with implementations), class methods, static methods, and properties.

The key difference from interfaces: interfaces only define method signatures, while ABCs can provide default implementations. This means ABCs can serve as both interface definitions AND partial implementations. For example, `collections.abc.Iterable` defines `__iter__` as abstract, but also provides concrete `__contains__` and `__iter__` default implementations. Subclasses only need to implement `__iter__`, and they get `__contains__` for free.

ABCs also support structural subclass checking via `register()` and `__subclasshook__`. A class can be considered a subclass of an ABC without explicit inheritance if it implements the required methods. This is Python's version of "structural typing" — `isinstance(obj, Iterable)` checks for `__iter__` regardless of inheritance. This is more flexible than Java's interfaces, which require explicit `implements` declarations.

In production systems at FAANG, ABCs are used for: protocol enforcement (ensuring objects implement required interfaces), type hints (specifying expected methods), and plugin systems (defining plugin contracts). At senior level, know that ABCs have a performance cost: `isinstance(obj, MyABC)` is slower than `isinstance(obj, MyConcreteClass)` because ABCs use `__subclasshook__` for structural checking. In hot paths, prefer concrete type checks or duck typing.

**Example:**
```python
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def put(self, key, value):
        pass

    def get_or_put(self, key, default):
        if not self.contains(key):
            self.put(key, default)
        return self.get(key)

class DictRepository(Repository):
    def __init__(self):
        self._data = {}

    def get(self, key):
        return self._data[key]

    def put(self, key, value):
        self._data[key] = value

    def contains(self, key):
        return key in self._data
```

## Q52: What is duck typing and how does it differ from structural subtyping?

**A:** Duck typing is the principle that "if it walks like a duck and quacks like a duck, it's a duck." Instead of checking an object's type, you check if it has the required methods/attributes. This is Python's natural approach — `for x in obj:` works if `obj` has `__iter__`, regardless of its type. Duck typing focuses on behavior, not inheritance.

Structural subtyping (as implemented by `typing.Protocol`) is a formalized version of duck typing. With `typing.Protocol`, you define a protocol class that specifies the required methods, and mypy/type checkers verify that objects satisfy the protocol based on their structure, not inheritance. This gives you duck typing with static type checking.

The difference: duck typing is checked at runtime (if the method exists, it works; if not, you get `AttributeError`), while structural subtyping is checked at compile time (type checkers verify the structure). Duck typing is more flexible but less safe — you might miss errors until runtime. Structural subtyping provides safety but requires type checker support.

In production systems, duck typing is used for: iterator protocol (anything with `__iter__` works in `for` loops), context manager protocol (anything with `__enter__`/`__exit__` works with `with`), and numeric protocol (anything with `__add__` works with `+`). Structural subtyping is used for: type hints (specifying expected interfaces), API contracts (documenting required methods), and refactoring (ensuring objects satisfy new interfaces). At senior level, know that `typing.Protocol` is the modern way to combine duck typing with type safety.

**Example:**
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Renderable(Protocol):
    def render(self) -> str: ...

class Button:
    def render(self) -> str:
        return "<button>Click</button>"

class Text:
    def render(self) -> str:
        return "<p>Hello</p>"

def draw(obj: Renderable) -> None:
    print(obj.render())

draw(Button())  # Works: Button has render()
draw(Text())    # Works: Text has render()
print(isinstance(Button(), Renderable))  # True
```

## Q53: What is `@abstractmethod` and what happens if you don't implement it?

**A:** `@abstractmethod` marks a method as abstract — subclasses MUST implement it. If you try to instantiate a class with unimplemented abstract methods, Python raises `TypeError`. If a subclass inherits from an ABC but doesn't implement all abstract methods, it's still abstract and can't be instantiated. This is enforced at instantiation time, not at definition time.

A common interview edge case: what about properties? You can decorate a property with `@abstractmethod` to require subclasses to implement the property. The syntax is `@property` followed by `@abstractmethod` on the getter. This is tricky because `@abstractmethod` must be the innermost decorator. Also, `@abstractproperty` (deprecated) is NOT the same as `@property` + `@abstractmethod` — the former doesn't work correctly with inheritance.

Another edge case: `@abstractmethod` can be applied to class methods and static methods. The syntax is `@classmethod` followed by `@abstractmethod`, or `@staticmethod` followed by `@abstractmethod`. This is less common but useful for abstract factory methods that should be class-level.

In production systems, `@abstractmethod` is used for: defining plugin interfaces (all plugins must implement `process()`), enforcing API contracts (all repositories must implement `get()` and `put()`), and ensuring test coverage (mock objects must implement all abstract methods). At senior level, know that `@abstractmethod` doesn't prevent concrete methods on the same class — you can mix abstract and concrete methods in an ABC.

**Example:**
```python
from abc import ABC, abstractmethod

class Stream(ABC):
    @abstractmethod
    def read(self, n):
        pass

    @abstractmethod
    def write(self, data):
        pass

    def read_until(self, delimiter):
        result = b""
        while True:
            chunk = self.read(1)
            if not chunk or chunk == delimiter:
                break
            result += chunk
        return result

class FileStream(Stream):
    def read(self, n):
        return self._file.read(n)

    def write(self, data):
        self._file.write(data)

# Stream()  # TypeError: Can't instantiate abstract class
FileStream()  # OK: all abstract methods implemented
```

## Q54: What is `@property` and how does it relate to descriptors?

**A:** `@property` is a built-in descriptor that creates managed attributes with getter, setter, and deleter methods. It's the most common descriptor in Python. When you access `obj.attr`, the property's `__get__` method is called; when you set `obj.attr = value`, the `__set__` method is called; when you delete `obj.attr`, the `__delete__` method is called.

Properties are descriptors — they implement the descriptor protocol (`__get__`, `__set__`, `__delete__`). The descriptor protocol is what makes properties work: when a descriptor is a class attribute, attribute access is delegated to the descriptor's methods. This is why properties must be defined on the class, not the instance — if you assign a property to an instance, it doesn't work as a descriptor.

A common interview question: "What's the difference between `@property` and `__getattr__`?" The answer is that `@property` creates a specific managed attribute with explicit getter/setter/deleter, while `__getattr__` is a catch-all for all missing attributes. Properties are type-safe and discoverable (they appear in `dir()`), while `__getattr__` is dynamic and can handle any attribute name. Properties are better for known attributes; `__getattr__` is better for dynamic or unknown attributes.

In production systems, properties are used for: computed attributes (calculating values on access), validation (checking values before setting), and encapsulation (hiding internal implementation). At Tesla, sensor readings use properties to convert raw values to calibrated units. At senior level, know that properties have a performance cost — each access involves a method call, which is slower than direct attribute access. For performance-critical code, consider using `__slots__` with descriptors instead of properties.

**Example:**
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        return 3.14159 * self._radius ** 2

c = Circle(5)
print(c.area)    # 78.53975
c.radius = 10
print(c.area)    # 314.159
```

## Q55: What is `@cached_property` and how does it differ from `@property`?

**A:** `@cached_property` (from `functools`) is a descriptor that computes a value on first access and then caches it as an instance attribute. Unlike `@property`, which recomputes on every access, `@cached_property` stores the result in the instance's `__dict__`, making subsequent accesses fast (direct dict lookup instead of method call).

The key difference: `@property` is always computed (O(1) or O(n) depending on computation), while `@cached_property` is computed once and then cached (O(1) for subsequent accesses). This makes `@cached_property` ideal for expensive computations that are accessed frequently. However, it has important implications: the cached value is stored on the instance, so it's not shared across instances, and it can be deleted (using `del obj.attr`) to force recomputation.

A common interview edge case: what about thread safety? `@cached_property` is NOT thread-safe in Python < 3.12. If two threads access the same property simultaneously during first computation, both may compute the value. In Python 3.12+, `@cached_property` is thread-safe. For earlier versions, use `threading.Lock` or implement your own thread-safe cached property.

Another edge case: `@cached_property` doesn't work with `__slots__` because it stores the cached value in `__dict__`. If your class uses `__slots__`, you need a different caching mechanism (like a separate cache dict or `lru_cache` on a method).

In production systems, `@cached_property` is used for: expensive database queries (caching the result of a complex JOIN), computed statistics (caching aggregations), and configuration values (loading once from a config file). At senior level, know that `@cached_property` is a descriptor that implements `__set_name__` to know its attribute name, and it stores the cached value using `object.__setattr__` to bypass any custom `__setattr__`.

**Example:**
```python
from functools import cached_property

class DataProcessor:
    def __init__(self, data):
        self._data = data

    @cached_property
    def statistics(self):
        print("Computing statistics...")  # Only printed once
        return {
            'mean': sum(self._data) / len(self._data),
            'max': max(self._data),
            'min': min(self._data),
        }

proc = DataProcessor([1, 2, 3, 4, 5])
print(proc.statistics)  # Computing statistics... {'mean': 3.0, ...}
print(proc.statistics)  # {'mean': 3.0, ...} (no recomputation)
```

## Q56: What is `__len__` vs `__bool__` for performance?

**A:** `__len__` returns the number of items in a container, while `__bool__` returns whether the container is truthy (non-empty). When Python checks `if obj:`, it first calls `__bool__`, then falls back to `__len__`, then defaults to `True`. This priority chain has critical performance implications for large containers.

If you only define `__len__`, every truthiness check (`if my_collection:`) computes the full length — O(n) for a linked list or O(1) for a list with cached length. By defining `__bool__` to return early (e.g., checking if a head pointer is None), you can make truthiness O(1). This is critical in performance-sensitive code at companies like Tesla (real-time systems) or Nvidia (GPU scheduling).

The Zen of Python says "Explicit is better than implicit" — always define `__bool__` if truthiness checks are common and your `__len__` is expensive. For a linked list, `__bool__` should check `self.head is not None` (O(1)), not `len(self) > 0` (O(n)). For a tree, `__bool__` should check `self.root is not None`, not count all nodes.

In production systems, this optimization matters for: database query results (checking if a query returned any rows), cached data (checking if the cache is populated), and collection classes (checking if a buffer has data). At senior level, discuss the memory trade-off: `__bool__` requires an extra method definition but saves O(n) per truthiness check. For millions of checks per second, this is a significant win.

**Example:**
```python
class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def __len__(self):
        return self._size

    def __bool__(self):
        return self.head is not None  # O(1) vs O(n)

    def append(self, value):
        node = Node(value, self.head)
        self.head = node
        self._size += 1

ll = LinkedList()
if not ll:  # O(1) thanks to __bool__
    ll.append(1)
```

## Q57: What is `__repr__` for debugging and how should it be implemented?

**A:** `__repr__` should return an unambiguous, developer-oriented string representation. The ideal `__repr__` output should be valid Python that could recreate the object (if possible). At minimum, it should give developers enough information to understand what the object is without having to inspect its attributes manually. This makes debugging faster and log messages more useful.

A good `__repr__` includes: the class name, the key attributes (especially those that define the object's identity), and enough information to distinguish between different instances. For example, `Point(x=1, y=2)` is better than `Point at 0x7f...`. The `!r` format specifier is commonly used to show string values with quotes: `f"name={self.name!r}"`.

In production systems, `__repr__` is critical for: logging (log aggregation systems need parseable output), debugging (interactive sessions show `repr()` output), and error messages (exceptions show the `repr()` of relevant objects). At Tesla, sensor reading `__repr__` includes timestamp, raw value, unit, and calibration status. At FAANG, API response objects include request IDs and status codes in their `__repr__`.

A common interview question: "Should `__repr__` always be valid Python?" The answer is: it's a goal, not a requirement. Some objects can't be recreated from their `__repr__` (like database connections or file handles), but the `__repr__` should still be informative. The key is that `__repr__` is for developers, not for users — it should prioritize information over aesthetics.

**Example:**
```python
class User:
    def __init__(self, id, name, email, is_active=True):
        self.id = id
        self.name = name
        self.email = email
        self.is_active = is_active

    def __repr__(self):
        return (
            f"User(id={self.id}, name={self.name!r}, "
            f"email={self.email!r}, is_active={self.is_active})"
        )

u = User(1, "Alice", "alice@example.com")
print(repr(u))
# User(id=1, name='Alice', email='alice@example.com', is_active=True)
```

## Q58: What is `__str__` for user-facing output and how should it differ from `__repr__`?

**A:** `__str__` should return a human-readable, user-friendly string representation. It's what `print()` and `str()` call. Unlike `__repr__` (which is for developers), `__str__` is for end users — it should be readable, formatted, and free of implementation details. The output should make sense to someone who doesn't know the internal structure of the object.

The distinction matters in different contexts: `__repr__` is for debugging (logs, error messages, REPL), while `__str__` is for display (print statements, UI, reports). A `Date` object might have `__repr__` = `Date(2025, 1, 15)` and `__str__` = `"January 15, 2025"`. The first is for developers; the second is for users.

A common interview question: "What if `__str__` is not defined?" Python falls back to `__repr__`. This means if you only implement `__repr__`, both `repr(obj)` and `str(obj)` show the same output. But if you implement both, `str(obj)` uses `__str__` and `repr(obj)` uses `__repr__`. Always implement `__repr__` first, then add `__str__` if you need a different user-facing representation.

In production systems, `__str__` is used for: user-facing messages (error messages shown to users), formatted output (reports, exports), and localization (different string representations for different locales). At senior level, know that `__str__` should handle `None` and edge cases gracefully — `str(None)` returns `"None"`, so your `__str__` should also handle missing data without raising exceptions.

**Example:**
```python
from datetime import datetime

class Event:
    def __init__(self, name, timestamp, location):
        self.name = name
        self.timestamp = timestamp
        self.location = location

    def __repr__(self):
        return f"Event(name={self.name!r}, timestamp={self.timestamp!r})"

    def __str__(self):
        return f"{self.name} at {self.location} ({self.timestamp:%B %d, %Y})"

e = Event("Conference", datetime(2025, 6, 15), "San Francisco")
print(repr(e))  # Event(name='Conference', timestamp=datetime(2025, 6, 15, 0, 0))
print(str(e))   # Conference at San Francisco (June 15, 2025)
```

## Q59: What is `__delitem__` and how does it differ from `__setitem__`?

**A:** `__delitem__` is called when you use `del obj[key]` on an object. It receives the key as an argument and should delete the corresponding item. It's the mirror of `__setitem__` — while `__setitem__` creates or modifies items, `__delitem__` removes them. Both receive the key as an argument, but `__delitem__` doesn't receive a value.

A critical difference: `__delitem__` should raise `KeyError` (for mapping-like access) or `IndexError` (for sequence-like access) if the key doesn't exist. This matches the behavior of `dict` and `list`. If you don't raise the appropriate exception, code that checks `key in obj` followed by `del obj[key]` could break (because the `in` operator relies on the exception type).

A common interview pattern: implementing a sorted container with `__delitem__`. This requires maintaining the sorted order after deletion, which typically involves rebalancing a tree or rebuilding a list. The key insight is that `__delitem__` often needs to trigger additional operations (like rebalancing) that `__setitem__` doesn't, because deletion changes the structure of the container.

In production systems, `__delitem__` is used for: cache invalidation (removing entries from a cache), configuration management (removing configuration keys), and data structures (removing elements from sorted containers). At senior level, know that `__delitem__` interacts with `__contains__` — after `del obj[key]`, `key in obj` should return `False`. This consistency is critical for correct container behavior.

**Example:**
```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self._cache = {}
        self._order = []

    def __setitem__(self, key, value):
        if key in self._cache:
            self._order.remove(key)
        elif len(self._cache) >= self.capacity:
            oldest = self._order.pop(0)
            del self._cache[oldest]
        self._cache[key] = value
        self._order.append(key)

    def __getitem__(self, key):
        if key not in self._cache:
            raise KeyError(key)
        self._order.remove(key)
        self._order.append(key)
        return self._cache[key]

    def __delitem__(self, key):
        if key not in self._cache:
            raise KeyError(key)
        del self._cache[key]
        self._order.remove(key)

    def __contains__(self, key):
        return key in self._cache

cache = LRUCache(3)
cache["a"] = 1
del cache["a"]
print("a" in cache)  # False
```

## Q60: What is `__sizeof__` for memory profiling and how do you override it?

**A:** `__sizeof__` returns the size in bytes of a single object, excluding the size of objects it references. When `sys.getsizeof(obj)` is called, it returns `obj.__sizeof__()` plus the garbage collector overhead. The default `__sizeof__` (from `object`) returns a fixed value based on the object's internal layout. You can override it to report accurate sizes for your specific class.

You should override `__sizeof__` when: (1) your class uses `__slots__` (the default size doesn't account for slots), (2) your class stores data in external structures (C buffers, numpy arrays), or (3) you want to include the size of referenced objects in the report. The override should return the total size of the object itself, not including referenced objects (that's `sys.getsizeof`'s job to add).

A common interview question: "How do you measure the total memory of an object including all its references?" The answer is that `sys.getsizeof()` alone doesn't do this — it only gives the shallow size. For total size, you need `pympler.asizeof` or a custom recursive traversal. Python's `gc.get_objects()` can help you find all objects, but computing the total size of a complex object graph requires traversal.

In production systems at Tesla (embedded) or Nvidia (GPU memory), accurate memory reporting is critical for resource management. When you have millions of objects, the difference between reported and actual memory can cause OOM errors. Override `__sizeof__` to report accurate sizes, and use `gc.get_objects()` + recursive traversal for complete memory profiling.

**Example:**
```python
import sys

class Matrix:
    __slots__ = ('rows', 'cols', 'data')

    def __init__(self, rows, cols, data):
        self.rows = rows
        self.cols = cols
        self.data = data

    def __sizeof__(self):
        return sys.getsizeof(self.data) + sys.getsizeof(self.rows) + sys.getsizeof(self.cols)

m = Matrix(1000, 1000, list(range(1000000)))
print(f"Shallow: {sys.getsizeof(m)} bytes")
print(f"Data:    {sys.getsizeof(m.data)} bytes")
```

## Q61: What is `__contains__` for custom membership testing?

**A:** `__contains__` is called by the `in` operator. When you write `x in obj`, Python calls `obj.__contains__(x)`. It should return `True` or `False`. If `__contains__` is not defined, Python falls back to iterating over the object using `__iter__`, checking each element until a match is found or the iteration ends.

You should implement `__contains__` when membership testing is a core operation and you can provide a more efficient implementation than linear search. For example, a `BloomFilter` class should implement `__contains__` for O(1) probabilistic membership testing. A `SortedSet` could implement `__contains__` using binary search (O(log n)) instead of the default linear scan.

A common interview edge case: what about `frozenset` and `set`? They implement `__contains__` with hash-based lookup (O(1) average case). If your custom set-like class doesn't implement `__contains__`, Python falls back to iteration (O(n)). For set-like classes, always implement `__contains__` with the appropriate data structure.

In production systems, `__contains__` is used for: bloom filters (probabilistic membership), sorted containers (binary search membership), and database query result sets (checking if a record exists). At Tesla, sensor threshold checks use `__contains__` for O(1) range membership testing. At senior level, know that `__contains__` should raise `TypeError` for unhashable types when using hash-based lookup, and should handle edge cases like `None` values.

**Example:**
```python
class IntervalSet:
    def __init__(self):
        self.intervals = []

    def add(self, start, end):
        self.intervals.append((start, end))
        self.intervals.sort()

    def __contains__(self, value):
        for start, end in self.intervals:
            if start <= value <= end:
                return True
            if start > value:
                break
        return False

s = IntervalSet()
s.add(1, 5)
s.add(10, 15)
print(3 in s)    # True
print(7 in s)    # False
print(12 in s)   # True
```

## Q62: What is `__reversed__` for efficient reverse iteration?

**A:** `__reversed__` is called by the built-in `reversed()` function and should return an iterator that yields items in reverse order. If `__reversed__` is not defined, Python falls back to: (1) using `__len__` and `__getitem__` with decreasing indices, or (2) raising `TypeError` if neither is available.

You should implement `__reversed__` when: (1) you have a more efficient reverse traversal than the index-based fallback, (2) your data structure has a natural reverse traversal (like a doubly-linked list), or (3) you want to support `for x in reversed(collection)` idiomatically. The fallback mechanism is O(n) and involves exception handling for flow control, so a custom `__reversed__` can be significantly faster.

A common interview question: "How does `reversed()` interact with `__iter__`?" The answer is that they're independent protocols. `reversed()` uses `__reversed__` first, then falls back to `__len__` + `__getitem__`. It does NOT use `__iter__` — you can't reverse an iterator by calling `reversed()` on it. If you want reverse iteration on an iterator, you need to consume it into a list first.

In production systems, `__reversed__` is used in: doubly-linked lists (efficient reverse traversal), deques (reverse access to elements), and UI components (rendering lists in reverse order). At Tesla, vehicle telemetry data stored in circular buffers uses `__reversed__` for efficient reverse chronological access. At senior level, know that `__reversed__` should return a fresh iterator each time — calling `reversed(obj)` twice should give two independent iterators.

**Example:**
```python
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def __reversed__(self):
        node = self.tail
        while node is not None:
            yield node.value
            node = node.prev

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

dll = DoublyLinkedList()
# ... add nodes ...
print(list(reversed(dll)))  # Reverse order
```

## Q63: What is `__array_interface__` and how does it work with numpy?

**A:** `__array_interface__` is a dictionary that describes the memory layout of an object's data. When numpy encounters an object with `__array_interface__`, it can create a numpy array that shares memory with the object (zero-copy). This is different from `__array__` which returns a numpy array (possibly copying data). `__array_interface__` is a lower-level, more efficient protocol for numpy integration.

The dictionary contains: `data` (a tuple of `(address, readonly)`), `strides` (optional stride information), `typestr` (a four-character type string), `shape` (the array shape), and `version` (the protocol version, currently 3). This allows numpy to create an array view over your object's memory without copying.

A common interview edge case: what about the buffer protocol (`__buffer__`/`__releasebuffer__`)? The buffer protocol is even lower-level than `__array_interface__` — it's implemented in C and allows zero-copy access to an object's memory buffer. `__array_interface__` is Python-level and easier to implement but slightly less efficient. For most use cases, `__array_interface__` is sufficient.

In production systems at Nvidia (GPU computing) and Tesla (data processing), `__array_interface__` is used for: zero-copy integration with numpy, sharing memory between different data structures, and efficient array operations on custom types. At senior level, know that `__array_interface__` requires the object to maintain a consistent memory layout — if the data is moved or resized after creating the array view, numpy operations will use stale data or segfault.

**Example:**
```python
import numpy as np

class Matrix:
    def __init__(self, rows, cols, data):
        self.rows = rows
        self.cols = cols
        self._data = data

    @property
    def __array_interface__(self):
        return {
            'data': (id(self._data), False),
            'strides': (self.cols * 8,),  # float64 = 8 bytes
            'typestr': '<f8',
            'shape': (self.rows, self.cols),
            'version': 3,
        }

data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
m = Matrix(2, 3, data)
arr = np.asarray(m)
print(arr.shape)  # (2, 3)
```

## Q64: What is `__array_ufunc__` and how does it handle numpy ufuncs?

**A:** `__array_ufunc__` is called when a numpy ufunc (like `np.sin`, `np.exp`, `np.add`) is applied to your object. It receives the ufunc, the method name (like `'__call__'`), and the input arguments. This allows your custom type to handle numpy operations without converting to a numpy array first.

The method should return the result of the operation or `NotImplemented` if it doesn't know how to handle the ufunc. If all operands return `NotImplemented`, numpy raises `TypeError`. This is the standard protocol for custom array types to integrate with numpy's ufunc system.

A common interview edge case: what about `__array_function__`? It's a different protocol that handles numpy functions (like `np.sum`, `np.dot`), not ufuncs. `__array_ufunc__` handles element-wise operations, while `__array_function__` handles higher-level functions. Both are needed for full numpy integration.

In production systems at Nvidia, `__array_ufunc__` is used for: GPU array types (handling ufuncs on GPU memory), distributed arrays (handling ufuncs across nodes), and special array types (handling ufuncs with special semantics). At senior level, know that `__array_ufunc__` should preserve the type of the result — if you add two `GPUArray` objects, the result should be a `GPUArray`, not a numpy array.

**Example:**
```python
import numpy as np

class OffsetArray:
    def __init__(self, data, offset=0):
        self.data = np.asarray(data)
        self.offset = offset

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        inputs = tuple(
            x.data if isinstance(x, OffsetArray) else x for x in inputs
        )
        result = getattr(ufunc, method)(*inputs, **kwargs)
        return OffsetArray(result, self.offset)

a = OffsetArray([1, 2, 3], offset=10)
b = OffsetArray([4, 5, 6], offset=10)
c = np.add(a, b)
print(c.data)    # [ 5  7  9]
print(c.offset)  # 10
```

## Q65: What is `__array_function__` and how does it override numpy functions?

**A:** `__array_function__` is called when a numpy function (like `np.sum`, `np.dot`, `np.concatenate`) is applied to your object. It receives the function, the method name, and the input arguments. This allows your custom type to handle numpy functions without converting to a numpy array first. It's the standard protocol for custom array types to override numpy's dispatch.

The method should return the result of the function or `NotImplemented` if it doesn't know how to handle the function. If all operands return `NotImplemented`, numpy falls back to the default implementation. This is the standard protocol for custom array types to integrate with numpy's function system.

A common interview edge case: what about `__array_ufunc__`? It's a different protocol that handles ufuncs (element-wise operations), not functions. `__array_function__` handles higher-level functions like `np.sum`, `np.dot`, `np.mean`. Both are needed for full numpy integration.

In production systems at Nvidia, `__array_function__` is used for: GPU array types (handling functions on GPU memory), distributed arrays (handling functions across nodes), and special array types (handling functions with special semantics). At senior level, know that `__array_function__` should preserve the type of the result — if you sum a `GPUArray`, the result should be a `GPUArray`, not a numpy array.

**Example:**
```python
import numpy as np

HANDLED_FUNCTIONS = {}

def implements(np_function):
    def decorator(func):
        HANDLED_FUNCTIONS[np_function] = func
        return func
    return decorator

class MyArray:
    def __init__(self, data):
        self.data = np.asarray(data)

    def __array_function__(self, func, method, *inputs, **kwargs):
        if func in HANDLED_FUNCTIONS:
            return HANDLED_FUNCTIONS[func](*inputs, **kwargs)
        return NotImplemented

@implements(np.sum)
def my_sum(arr, **kwargs):
    return MyArray([sum(arr.data)])

a = MyArray([1, 2, 3])
print(np.sum(a).data)  # [6]
```

## Q66: What is `__array_finalize__` and how does it handle numpy subclass creation?

**A:** `__array_finalize__` is called when a new array is created from an existing one (via slicing, copying, or view creation). It receives the new array and the parent object (which can be `None` for direct construction). This allows numpy subclasses to properly initialize state that's not part of the base ndarray.

When you subclass `np.ndarray`, slicing and view creation create new array objects that share memory with the original. `__array_finalize__` is called on the new object, allowing you to copy any custom attributes from the parent. Without it, custom attributes are lost during slicing.

A common interview edge case: what about `__new__` vs `__array_finalize__`? `__new__` is called for direct construction (`MyArray(data)`), while `__array_finalize__` is called for all creation methods (including slicing). You need both to properly initialize your subclass. `__new__` handles direct construction, and `__array_finalize__` handles derived arrays.

In production systems at Nvidia, `__array_finalize__` is used for: GPU array subclasses (preserving GPU metadata during slicing), masked arrays (preserving mask during operations), and units arrays (preserving unit information during arithmetic). At senior level, know that `__array_finalize__` should be defensive — the parent can be any ndarray subclass, not just your own. Always check `isinstance(parent, MyArray)` before copying attributes.

**Example:**
```python
import numpy as np

class MyArray(np.ndarray):
    def __new__(cls, input_array, info=None):
        obj = np.asarray(input_array).view(cls)
        obj.info = info
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.info = getattr(obj, 'info', None)

    def __getitem__(self, key):
        result = super().__getitem__(key)
        if isinstance(result, MyArray):
            result.info = self.info
        return result

a = MyArray([1, 2, 3], info="metadata")
b = a[0:2]
print(b.info)  # "metadata" (preserved)
```

## Q67: What is `__array_wrap__` and how does it handle ufunc output?

**A:** `__array_wrap__` is called after a ufunc completes to wrap the output in the appropriate type. It receives the output array and the ufunc context (ufunc, method, inputs). This allows numpy subclasses to ensure that ufunc results are returned in the subclass type, not as plain numpy arrays.

The method should return the wrapped array or `NotImplemented` if it doesn't know how to handle the output. If all operands return `NotImplemented`, numpy uses the default wrapping behavior. This is the standard protocol for custom array types to ensure ufunc results preserve the subclass type.

A common interview edge case: what about `__array_ufunc__`? It's called BEFORE the ufunc executes, while `__array_wrap__` is called AFTER. `__array_ufunc__` can override the ufunc behavior entirely, while `__array_wrap__` only wraps the result. They serve different purposes and are both needed for full ufunc integration.

In production systems at Nvidia, `__array_wrap__` is used for: GPU array types (ensuring ufunc results are on GPU), masked arrays (ensuring ufunc results preserve masks), and units arrays (ensuring ufunc results preserve units). At senior level, know that `__array_wrap__` should handle the case where the output is a scalar (for reduction ufuncs like `np.sum`) by converting it to the appropriate type.

**Example:**
```python
import numpy as np

class MyArray(np.ndarray):
    def __new__(cls, input_array, units=None):
        obj = np.asarray(input_array).view(cls)
        obj.units = units
        return obj

    def __array_wrap__(self, obj, context=None):
        result = obj.view(MyArray)
        result.units = self.units
        return result

a = MyArray([1, 2, 3], units="meters")
b = MyArray([4, 5, 6], units="meters")
c = np.add(a, b)
print(c.units)  # "meters" (preserved)
```

## Q68: What is `__array_ufunc__` vs `__array_function__` for numpy integration?

**A:** `__array_ufunc__` handles numpy ufuncs (element-wise operations like `np.sin`, `np.exp`, `np.add`), while `__array_function__` handles numpy functions (higher-level functions like `np.sum`, `np.dot`, `np.concatenate`). They're complementary protocols that together provide full numpy integration for custom array types.

The key difference: ufuncs operate element-wise on arrays, while functions operate on arrays as a whole. `np.add(a, b)` is a ufunc (element-wise addition), while `np.sum(a)` is a function (reduction). `__array_ufunc__` is called for each element, while `__array_function__` is called once for the entire operation.

A common interview question: "When should I implement `__array_ufunc__` vs `__array_function__`?" The answer: implement `__array_ufunc__` if you need to handle element-wise operations (like GPU arrays that need to run ufuncs on GPU). Implement `__array_function__` if you need to handle higher-level operations (like distributed arrays that need to coordinate across nodes). For full numpy integration, implement both.

In production systems at Nvidia, `__array_ufunc__` is used for: GPU arrays (running ufuncs on GPU memory), while `__array_function__` is used for: distributed arrays (coordinating reductions across nodes). At senior level, know that `__array_ufunc__` is more commonly implemented than `__array_function__` because ufuncs are more frequently used than higher-level functions.

**Example:**
```python
import numpy as np

class GPUArray:
    def __init__(self, data):
        self.data = np.asarray(data)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        inputs = tuple(x.data if isinstance(x, GPUArray) else x for x in inputs)
        result = getattr(ufunc, method)(*inputs, **kwargs)
        return GPUArray(result)

    def __array_function__(self, func, method, *inputs, **kwargs):
        if func == np.sum:
            return GPUArray([sum(self.data)])
        return NotImplemented

a = GPUArray([1, 2, 3])
print(np.add(a, a).data)  # [2 4 6]
print(np.sum(a).data)     # [6]
```

## Q69: What is `__buffer__` and how does it provide zero-copy access?

**A:** `__buffer__` (PEP 688) is called when an object's buffer is requested (via `memoryview(obj)` or numpy array creation). It should return a `Buffer` object that provides zero-copy access to the object's memory. This is the modern replacement for the old buffer protocol (`__bf_getbuffer__`/`__bf_releasebuffer__`) and is Python-level instead of C-level.

The `Buffer` object describes the memory layout: `itemsize` (bytes per element), `ndim` (number of dimensions), `shape` (tuple of dimension sizes), `strides` (tuple of byte strides), and `readonly` (whether the buffer is read-only). This allows numpy and other consumers to create array views over your object's memory without copying.

A common interview edge case: what about `__array_interface__`? It's a dictionary-based protocol for numpy integration, while `__buffer__` is a Buffer protocol for general zero-copy access. `__buffer__` is more general and works with any buffer consumer (not just numpy). `__array_interface__` is numpy-specific and easier to implement for simple cases.

In production systems at Nvidia (GPU memory sharing) and Tesla (sensor data access), `__buffer__` is used for: zero-copy integration with numpy, sharing memory between different data structures, and efficient array operations on custom types. At senior level, know that `__buffer__` requires the object to maintain a consistent memory layout — if the data is moved or resized after creating the buffer, consumers will use stale data or segfault.

**Example:**
```python
import numpy as np

class Matrix:
    def __init__(self, rows, cols, data):
        self.rows = rows
        self.cols = cols
        self.data = data

    def __buffer__(self, flags):
        return memoryview(self.data).cast('b', (self.rows * self.cols * 8,))

    def __release_buffer__(self, buffer):
        pass

m = Matrix(2, 3, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
arr = np.frombuffer(m, dtype=np.float64).reshape(2, 3)
print(arr)
```

## Q70: What is `__release_buffer__` and when is it called?

**A:** `__release_buffer__` is called when a buffer obtained from `__buffer__` is released (when the `memoryview` object is garbage collected or explicitly closed). It should perform any cleanup needed for the buffer, like releasing locks or flushing data. For most objects, `__release_buffer__` is a no-op because the buffer is just a view over existing memory.

The protocol is: `__buffer__` is called to create the buffer, and `__release_buffer__` is called to clean up. This is similar to `__enter__`/`__exit__` for context managers. The buffer protocol ensures that the object's memory is pinned (not moved or garbage collected) while the buffer is in use.

A common interview edge case: what about thread safety? If multiple threads access the same buffer, you need to ensure that the object's memory isn't modified while the buffer is in use. This typically involves locking in `__buffer__` and `__release_buffer__`, or using immutable data structures. At senior level, discuss the trade-offs between zero-copy efficiency and thread safety.

In production systems, `__release_buffer__` is used for: GPU arrays (releasing GPU memory locks), memory-mapped files (flushing dirty pages), and custom memory allocators (releasing allocated memory). At senior level, know that `__release_buffer__` should be idempotent — calling it multiple times should be safe and have no additional effect.

**Example:**
```python
class PinnedMatrix:
    def __init__(self, data):
        self.data = data
        self._pinned = False
        self._lock = threading.Lock()

    def __buffer__(self, flags):
        with self._lock:
            self._pinned = True
            return memoryview(self.data)

    def __release_buffer__(self, buffer):
        with self._lock:
            self._pinned = False

    def modify(self, value):
        with self._lock:
            if self._pinned:
                raise RuntimeError("Cannot modify pinned buffer")
            self.data = value
```

## Q71: What is `__bytes__` vs `__str__` for I/O operations?

**A:** `__bytes__` returns the byte representation of an object (for binary I/O), while `__str__` returns the human-readable string representation (for text I/O). In Python 3, these are completely separate — you can't use a `str` where `bytes` is expected, and vice versa. This separation is deliberate and enforces clear handling of text vs. binary data.

For I/O operations, the choice depends on the use case: `__bytes__` for binary files (`open(file, 'rb')`), `__str__` for text files (`open(file, 'r')`). A well-designed I/O object should implement both, with `__bytes__` returning the binary format and `__str__` returning a human-readable summary.

A common interview question: "How does `io.BytesIO` use `__bytes__`?" The answer is that `io.BytesIO` doesn't use `__bytes__` directly — it implements the buffer protocol for zero-copy access. `__bytes__` is for `bytes()` calls, not for I/O. However, `__bytes__` is used by `codecs.encode()` and some network protocols. If you want custom I/O behavior, use the buffer protocol.

In production systems, the distinction matters for: network protocols (binary vs. text protocols), file formats (binary files vs. text files), and encryption (encryption works on bytes, not strings). At Tesla, vehicle telemetry data is serialized to bytes for transmission over CAN bus. At FAANG, API responses are typically serialized to JSON strings, while internal data structures use binary formats for efficiency.

**Example:**
```python
class Packet:
    def __init__(self, header, payload):
        self.header = header
        self.payload = payload

    def __bytes__(self):
        return self.header + b'\n' + self.payload

    def __str__(self):
        return f"Packet(header={self.header!r}, payload_len={len(self.payload)})"

p = Packet(b'HTTP/1.1', b'Hello World')
print(bytes(p))  # b'HTTP/1.1\nHello World'
print(str(p))    # Packet(header=b'HTTP/1.1', payload_len=11)
```

## Q72: What is `__format__` for custom formatting and how does it interact with `format()`?

**A:** `__format__` is called by the built-in `format()` function and f-strings. When you write `format(obj, spec)` or `f"{obj:spec}"`, Python calls `obj.__format__(spec)`. The `spec` is the format specification string (like `".2f"` for floats or `">10"` for right-aligned strings). If `__format__` is not defined, Python falls back to `str(obj)`.

The interaction with `format()` is seamless: `format(obj, '.2f')` calls `obj.__format__('.2f')`. This means your custom objects can support rich formatting through `format()` and f-strings without any special syntax. The format spec becomes a mini-DSL for your domain.

A common interview edge case: what about nested format specs? For example, `format(obj, ">10.2f")`. This is parsed by Python's format spec mini-language, which splits it into fill, align, sign, width, precision, and type. Your `__format__` receives the entire spec string, so you need to parse it yourself if you want to support the mini-language.

In production systems, `__format__` is used for: report generation (formatting financial data with locale-specific separators), logging (formatting objects with context-specific detail levels), and API responses (formatting objects differently for different clients). At senior level, know that `format(obj, '')` calls `obj.__format__('')`, which is also what `str(obj)` does if `__str__` is not defined. This means `__format__` can serve as a fallback for `__str__`.

**Example:**
```python
class Color:
    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b

    def __format__(self, spec):
        if spec == 'hex':
            return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
        elif spec == 'rgb':
            return f"rgb({self.r}, {self.g}, {self.b})"
        elif spec == 'hsl':
            h, s, l = self._to_hsl()
            return f"hsl({h}, {s}%, {l}%)"
        return str(self)

c = Color(255, 128, 0)
print(f"{c:hex}")  # #ff8000
print(f"{c:rgb}")  # rgb(255, 128, 0)
```

## Q73: What is `__index__` for type-safe indexing?

**A:** `__index__` is called when an object needs to be converted to an integer for use as a sequence index, a slice, or a bitwise operation. It must return an `int`. `__int__` is called by `int()` and can return any integer-compatible value. The key distinction: `__index__` is specifically for contexts where an integer is required (like `list[obj]`), while `__int__` is for explicit conversion.

You should implement `__index__` when: (1) your object represents an integer value that should be usable as an index, (2) you want type-safe indexing that prevents invalid indices, or (3) you want to support bitwise operations. A `PositiveInt` class might implement `__index__` to ensure the value is always positive, raising `ValueError` for negative values.

A common interview edge case: what about `__int__` vs `__index__`? `__int__` is for explicit conversion (`int(obj)`), while `__index__` is for implicit conversion (using the object as an index). If you define `__int__` but not `__index__`, the object can't be used as a list index. If you define `__index__`, `int()` also uses it as a fallback. The safest approach is to define both.

In production systems, `__index__` is used in: numpy integer types (for array indexing), custom index types (like database row IDs that wrap integers), and type-safe indices (a `PositiveInt` class that validates the value is positive). At senior level, know that `__index__` is also called for bit shifts (`obj << 3`), bitwise AND/OR/XOR, and as the stop argument in `range()`.

**Example:**
```python
class MatrixIndex:
    def __init__(self, row, col):
        if row < 0 or col < 0:
            raise ValueError("Indices must be non-negative")
        self.row = row
        self.col = col

    def __index__(self):
        return self.row * 1000 + self.col

    def __int__(self):
        return self.row * 1000 + self.col

flat = list(range(1000000))
idx = MatrixIndex(5, 42)
print(flat[idx])    # Uses __index__
print(int(idx))     # Uses __int__
```

## Q74: What is `__bytes__` for network protocols and how should it be implemented?

**A:** `__bytes__` should return a bytes representation of an object suitable for network transmission. This is different from `__str__` (which returns a human-readable string) and `__repr__` (which returns a developer-oriented string). For network protocols, `__bytes__` should return the exact bytes that will be sent over the wire.

A well-designed `__bytes__` implementation should: (1) return the complete message in wire format, (2) include all necessary headers and metadata, (3) handle encoding correctly (especially for Unicode strings), and (4) be consistent with the corresponding `from_bytes()` class method. The `__bytes__` / `from_bytes` pair should be inverses of each other.

A common interview edge case: what about variable-length messages? For variable-length protocols, `__bytes__` should include a length prefix so the receiver knows how many bytes to read. This is how most network protocols work: the first few bytes indicate the message length, followed by the message body.

In production systems at FAANG (distributed systems) and Tesla (vehicle communication), `__bytes__` is used for: network protocol serialization, message queue encoding, and RPC communication. At senior level, know that `__bytes__` should be efficient — for large messages, consider using the buffer protocol instead of `__bytes__` to avoid copying. Also, ensure `__bytes__` handles edge cases like empty messages, maximum size limits, and encoding errors.

**Example:**
```python
import struct

class NetworkMessage:
    def __init__(self, msg_type, payload):
        self.msg_type = msg_type
        self.payload = payload

    def __bytes__(self):
        type_bytes = self.msg_type.encode()
        payload_bytes = self.payload.encode()
        header = struct.pack('!BH', len(type_bytes), len(payload_bytes))
        return header + type_bytes + payload_bytes

    @classmethod
    def from_bytes(cls, data):
        type_len, payload_len = struct.unpack('!BH', data[:3])
        msg_type = data[3:3+type_len].decode()
        payload = data[3+type_len:3+type_len+payload_len].decode()
        return cls(msg_type, payload)

msg = NetworkMessage("heartbeat", "ok")
wire = bytes(msg)
print(wire)
```

## Q75: What is `__sizeof__` for embedded systems and how do you optimize it?

**A:** `__sizeof__` returns the size in bytes of a single object. For embedded systems (like Tesla's vehicle computers), accurate memory reporting is critical because RAM is limited. The default `__sizeof__` may not reflect the actual memory usage of your objects, especially if they use external data structures or C extensions.

You should override `__sizeof__` when: (1) your class uses `__slots__` (the default size doesn't account for slots), (2) your class stores data in external structures (C buffers, numpy arrays), or (3) you want to include the size of referenced objects in the report. The override should return the total size of the object itself, not including referenced objects.

A common interview edge case: what about the garbage collector overhead? `sys.getsizeof()` adds GC overhead to `__sizeof__` output. For CPython, this adds 16 bytes for GC-tracked objects. Your `__sizeof__` should NOT include GC overhead — that's `sys.getsizeof()`'s job. Also, `__sizeof__` is called by `sys.getsizeof()`, not by `gc.get_size()`.

In production systems at Tesla (embedded) or Nvidia (GPU memory), `__sizeof__` is used for: memory profiling, capacity planning, and resource management. At senior level, know that `__sizeof__` is a single method call — it doesn't recursively compute the size of referenced objects. For total memory, you need `pympler.asizeof` or a custom recursive traversal. Also, `__sizeof__` should be fast — it's called frequently during memory profiling.

**Example:**
```python
import sys

class SensorReading:
    __slots__ = ('timestamp', 'value', 'unit', 'calibration')

    def __init__(self, timestamp, value, unit, calibration):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit
        self.calibration = calibration

    def __sizeof__(self):
        return (
            sys.getsizeof(self.timestamp)
            + sys.getsizeof(self.value)
            + sys.getsizeof(self.unit)
            + sys.getsizeof(self.calibration)
        )

r = SensorReading(1234567890, 42.5, "C", 0.1)
print(f"Size: {sys.getsizeof(r)} bytes")
```

## Q76: Design a context manager that handles database transactions with savepoints.

**A:** A database transaction context manager with savepoints needs to handle: opening a transaction on `__enter__`, creating savepoints within the transaction, and either committing or rolling back on `__exit__`. The savepoint mechanism allows partial rollbacks — you can undo changes since the last savepoint without aborting the entire transaction.

The implementation should track the current savepoint level and handle nested context managers. When entering, create a savepoint (if nested) or start a transaction (if top-level). When exiting without exceptions, release the savepoint (if nested) or commit (if top-level). When exiting with exceptions, rollback to the savepoint (if nested) or rollback the entire transaction (if top-level).

A common interview edge case: what about nested transactions? Most databases don't support true nested transactions — they support savepoints, which simulate nested transactions. The context manager should handle this by tracking the nesting level and using savepoints for inner levels. This is the standard approach in production systems at FAANG.

In production systems, this pattern is used for: API request handlers (transaction per request), data migration scripts (savepoint per batch), and test fixtures (savepoint per test). At senior level, discuss the trade-offs between savepoint overhead and safety, and how to handle connection pool exhaustion under high concurrency.

**Example:**
```python
from contextlib import contextmanager

class TransactionManager:
    def __init__(self, connection):
        self.conn = connection
        self._savepoint_level = 0

    def __enter__(self):
        if self._savepoint_level == 0:
            self.conn.begin()
        else:
            self.conn.execute(f"SAVEPOINT sp_{self._savepoint_level}")
        self._savepoint_level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._savepoint_level -= 1
        if exc_type is not None:
            if self._savepoint_level == 0:
                self.conn.rollback()
            else:
                self.conn.execute(f"ROLLBACK TO SAVEPOINT sp_{self._savepoint_level}")
        else:
            if self._savepoint_level == 0:
                self.conn.commit()
            else:
                self.conn.execute(f"RELEASE SAVEPOINT sp_{self._savepoint_level}")
        return False
```

## Q77: How would you implement a lazy-loading descriptor with caching?

**A:** A lazy-loading descriptor with caching combines three patterns: descriptor protocol (for attribute access interception), caching (to avoid recomputation), and lazy evaluation (to defer computation until first access). The descriptor implements `__get__` to intercept attribute access, checks if the value is cached, and computes it on first access.

The implementation should handle: thread safety (multiple threads accessing the same descriptor), cache invalidation (when should the cached value be recomputed), and memory management (how long to keep the cached value). For thread safety, use a lock or `threading.local()` storage. For cache invalidation, use TTL (time-to-live) or explicit invalidation methods.

A common interview edge case: what about `__set__` and `__delete__`? For lazy-loading descriptors, `__set__` should update the cached value, and `__delete__` should invalidate the cache. This allows external code to force recomputation or set a specific value.

In production systems at Tesla (sensor data caching) and FAANG (database query caching), lazy-loading descriptors are used for: expensive database queries, remote API calls, and complex computations. At senior level, discuss the trade-offs between lazy evaluation (deferred cost) and eager evaluation (upfront cost), and how to choose the right strategy based on access patterns.

**Example:**
```python
import threading

class LazyProperty:
    def __init__(self, func):
        self.func = func
        self.attr_name = None
        self._lock = threading.Lock()

    def __set_name__(self, owner, name):
        self.attr_name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        with self._lock:
            if self.attr_name not in obj.__dict__:
                obj.__dict__[self.attr_name] = self.func(obj)
        return obj.__dict__[self.attr_name]

class DataProcessor:
    def __init__(self, data):
        self._data = data

    @LazyProperty
    def statistics(self):
        return {'mean': sum(self._data) / len(self._data)}
```

## Q78: Design a descriptor that validates attribute types at assignment time.

**A:** A type-validating descriptor checks the assigned value's type during `__set__` and raises `TypeError` if it doesn't match. The descriptor stores the expected type and the attribute name, and uses `__set_name__` to automatically know its name in the class.

The implementation should handle: inheritance (subclasses should inherit the validation), multiple types (allowing `Union` types), and custom validation (beyond simple `isinstance` checks). For inheritance, use `__set_name__` to store the class and name. For multiple types, accept a tuple of types. For custom validation, accept a callable.

A common interview edge case: what about `__get__`? For type-validating descriptors, `__get__` simply returns the stored value (or a default if not set). The validation happens in `__set__`, not `__get__`. This ensures that all assignments are validated, but reads are fast.

In production systems, type-validating descriptors are used in: data validation frameworks (Pydantic, Marshmallow), ORM systems (SQLAlchemy column types), and configuration management (ensuring config values have correct types). At senior level, discuss the performance implications of type checking on every assignment, and how to optimize for hot paths.

**Example:**
```python
class Typed:
    def __init__(self, expected_type):
        self.expected_type = expected_type
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        obj.__dict__[self.name] = value

class User:
    name = Typed(str)
    age = Typed(int)

u = User()
u.name = "Alice"  # OK
u.age = 30        # OK
# u.age = "thirty"  # TypeError
```

## Q79: How do you implement a read-only attribute using descriptors?

**A:** A read-only descriptor implements `__get__` but not `__set__` (or `__set__` raises `AttributeError`). This prevents external code from modifying the attribute after initialization. The descriptor can be set during `__init__` using `object.__setattr__` (to bypass the descriptor's `__set__` if it exists) or through a separate initialization method.

The implementation should handle: initialization (how to set the initial value), thread safety (preventing race conditions during initialization), and inheritance (subclasses should respect read-only semantics). For initialization, use `object.__setattr__` in `__init__`. For thread safety, use a lock or atomic operations. For inheritance, ensure the descriptor is properly inherited.

A common interview edge case: what about `__delete__`? For read-only descriptors, `__delete__` should also raise `AttributeError`. This ensures the attribute can't be deleted either. This is different from "write-once" attributes, which allow setting once but not reassigning.

In production systems, read-only descriptors are used for: immutable data (preventing modification of calculated values), configuration constants (ensuring values aren't changed at runtime), and API objects (exposing read-only views of internal state). At senior level, discuss the trade-offs between read-only descriptors (descriptors that raise on `__set__`) and properties (which can have custom `__set__` logic).

**Example:**
```python
class ReadOnly:
    def __init__(self, value):
        self.value = value
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.value

    def __set__(self, obj, value):
        if hasattr(obj, self.name):
            raise AttributeError(f"Cannot reassign read-only attribute '{self.name}'")
        object.__setattr__(obj, self.name, value)

    def __delete__(self, obj):
        raise AttributeError(f"Cannot delete read-only attribute '{self.name}'")

class Config:
    MAX_RETRIES = ReadOnly(3)

print(Config.MAX_RETRIES)  # 3
```

## Q80: What is `__class_getitem__` for generic types and how does it work with `typing`?

**A:** `__class_getitem__` (PEP 560) is called when you use subscript notation on a class itself: `MyClass[SomeType]`. It receives the class and the item (the content inside the brackets) and should return something appropriate — typically a `types.GenericAlias` or a `typing._GenericAlias` for type hinting.

Before `__class_getitem__`, you had to use metaclasses or `__getitem__` on the class (which conflicts with instance indexing) to implement generic types. `__class_getitem__` is cleaner because it's specifically for class-level subscripting. It was introduced to make `typing` types work with subscript syntax: `List[int]`, `Dict[str, Any]`, etc.

A common interview question: "How does `list[int]` work in Python 3.9+?" The answer is that `list` (the built-in type) implements `__class_getitem__`, which returns a `types.GenericAlias` object. This object is used for type hints and doesn't actually affect runtime behavior — `list[int]` is still just a `list` at runtime. However, this is changing with PEP 695 (Python 3.12+) which adds more formal type parameter syntax.

In production systems, `__class_getitem__` is used for: type hints (generic types), runtime type validation (checking generic parameters at runtime), and DSL creation (subscript syntax for configuration). At senior level, know that `__class_getitem__` receives the class as the first argument (like a classmethod) and the subscripted value as the second. If the class also implements `__getitem__` for instance access, there's no conflict.

**Example:**
```python
class Registry:
    _types = {}

    def __class_getitem__(cls, item):
        def decorator(func):
            cls._types[item] = func
            return func
        return decorator

class Handlers:
    @Registry["login"]
    def handle_login(self, user):
        return f"Welcome {user}"

    @Registry["logout"]
    def handle_logout(self, user):
        return f"Goodbye {user}"

print(Registry._types)  # {'login': <function>, 'logout': <function>}
```

## Q81: How do you implement a `__hash__` that's consistent with `__eq__`?

**A:** The hash contract requires that if `a == b`, then `hash(a) == hash(b)`. This means your `__hash__` must be consistent with `__eq__`. If two objects are equal (according to `__eq__`), they must have the same hash value. The reverse is not required — objects with the same hash are not required to be equal (hash collisions are expected).

A common pattern is to hash the same fields used in `__eq__`. For example, if `__eq__` compares `self.x` and `self.y`, then `__hash__` should hash `(self.x, self.y)`. This ensures consistency. However, if `__eq__` uses a subset of fields, `__hash__` should also use that same subset (or a superset that includes the same equality semantics).

A common interview edge case: what about mutable objects? Mutable objects should NOT be hashable because their hash would change when they're modified. If you define `__eq__` without `__hash__`, Python sets `__hash__ = None`, making the object unhashable. If you define both, you must ensure the hash doesn't change after the object is added to a set or used as a dict key.

In production systems, `__hash__` is used in: dictionaries (hash table lookup), sets (membership testing), and caches (cache key generation). At senior level, discuss the trade-offs between hash quality (good distribution) and hash speed (fast computation). For simple objects, `hash(tuple(fields))` is sufficient. For complex objects, consider using `hashlib` for better distribution.

**Example:**
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

points = {Point(1, 2), Point(3, 4), Point(1, 2)}
print(len(points))  # 2 (duplicate Point(1,2) is collapsed)
```

## Q82: What is `__slots__` for memory optimization and how do you use it with inheritance?

**A:** `__slots__` is a class variable that restricts the instance attributes of a class. When you define `__slots__ = ('x', 'y')`, instances can only have `x` and `y` attributes. Internally, Python uses a more efficient storage mechanism (an array of descriptors) instead of the standard `__dict__` dictionary, saving significant memory per instance.

With inheritance, `__slots__` has important rules: (1) each class in the hierarchy can define its own `__slots__`, (2) subclass `__slots__` should not overlap with parent `__slots__`, (3) if any class in the hierarchy doesn't define `__slots__`, instances get a `__dict__` (defeating the purpose). Also, `__weakref__` must be explicitly included in `__slots__` if you want weak references.

A common interview edge case: what about multiple inheritance with `__slots__`? Each class with `__slots__` must have non-overlapping slot names. If two parent classes define the same slot name, you get a `TypeError`. This is a significant limitation and is one reason why `__slots__` + multiple inheritance is tricky.

In production systems at Tesla (embedded) or FAANG (data processing), `__slots__` is used for: ORM models (SQLAlchemy uses them for mapped classes), network protocol messages (millions of message objects), and data processing pipelines (millions of data records). At senior level, know that `__slots__` doesn't prevent adding attributes via `__dict__` if any base class lacks `__slots__`, and that `__slots__` doesn't work with `@dataclass` by default (you need `@dataclass(slots=True)` in Python 3.10+).

**Example:**
```python
class Base:
    __slots__ = ('id',)

class Child(Base):
    __slots__ = ('name', 'value')

class BadChild(Base):
    pass  # No __slots__, gets __dict__

c = Child()
c.id = 1
c.name = "test"
print(hasattr(c, '__dict__'))  # False (slots only)

b = BadChild()
b.id = 1
print(hasattr(b, '__dict__'))  # True (has __dict__)
```

## Q83: How do you implement a descriptor that works with `__slots__`?

**A:** Descriptors work with `__slots__` because descriptors are stored on the class, not the instance. `__slots__` only restricts instance attributes — class attributes (including descriptors) are unaffected. This means you can use descriptors for computed attributes, validation, or caching even with `__slots__`.

The key challenge is that descriptors that store data on the instance (like `__set__` implementations) need to use `object.__setattr__` instead of `self.attr = value`, because `__slots__` prevents direct attribute assignment. This is because `__slots__` uses descriptors internally, and assigning to a slot descriptor goes through the descriptor's `__set__` method.

A common interview edge case: what about `__dict__`? If a class uses `__slots__`, there's no `__dict__` to store extra data. This means descriptors that store data in `obj.__dict__` (like `@cached_property`) won't work with `__slots__`. You need to use a different storage mechanism (like a separate cache dict or `lru_cache`).

In production systems, descriptors + `__slots__` are used for: memory-efficient validated attributes (combining `__slots__` memory savings with descriptor validation), computed properties (using descriptors for lazy evaluation), and ORM fields (SQLAlchemy's `Column` is a descriptor that works with `__slots__`). At senior level, discuss the interaction between descriptors, `__slots__`, and `__init_subclass__` for class customization.

**Example:**
```python
class ValidatedSlot:
    def __init__(self, validator):
        self.validator = validator
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f'_slot_{self.name}')

    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}")
        object.__setattr__(obj, f'_slot_{self.name}', value)

class User:
    __slots__ = ('_slot_name', '_slot_age')
    name = ValidatedSlot(lambda v: isinstance(v, str))
    age = ValidatedSlot(lambda v: isinstance(v, int) and v > 0)

u = User()
u.name = "Alice"
u.age = 30
```

## Q84: What is `__init_subclass__` for plugin registration and how does it work?

**A:** `__init_subclass__` (PEP 487) is called when a class is subclassed. It's defined on the parent class and receives the newly created subclass as its first argument (plus any keyword arguments from the class definition). This enables automatic plugin registration without metaclasses.

When you define `class Child(Parent, plugin_name="auth")`, Python calls `Parent.__init_subclass__(cls=Child, plugin_name="auth")`. The parent's `__init_subclass__` can then register the child in a registry, validate it, or configure it. This is the standard pattern for plugin systems in Python.

A common interview edge case: what about multiple inheritance? If multiple parent classes define `__init_subclass__`, they're all called (following MRO). You must use `**kwargs` and forward them to `super().__init_subclass__(**kwargs)` to ensure the chain works correctly. Forgetting to forward kwargs breaks the inheritance chain.

In production systems, `__init_subclass__` is used for: plugin systems (automatically registering subclasses), validation frameworks (ensuring subclasses implement required methods), and configuration systems (setting up class-level state). At senior level, know that `__init_subclass__` is called AFTER the subclass is fully created, so you can't control class creation — only post-process it.

**Example:**
```python
class Plugin:
    _registry = {}

    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__
        Plugin._registry[name] = cls
        cls._validate()

    @classmethod
    def _validate(cls):
        if not hasattr(cls, 'process'):
            raise TypeError(f"{cls.__name__} must define 'process'")

class AuthPlugin(Plugin, plugin_name="auth"):
    def process(self):
        return "authenticated"

class LogPlugin(Plugin, plugin_name="logger"):
    def process(self):
        return "logged"

print(Plugin._registry)  # {'auth': AuthPlugin, 'logger': LogPlugin}
```

## Q85: How do you implement a descriptor that provides computed attributes with caching?

**A:** A computed attribute descriptor with caching combines the descriptor protocol with memoization. The descriptor implements `__get__` to intercept attribute access, computes the value on first access, and caches it in the instance's `__dict__` (or a separate cache). Subsequent accesses return the cached value without recomputation.

The implementation should handle: thread safety (multiple threads accessing the same descriptor), cache invalidation (when should the cached value be recomputed), and memory management (how long to keep the cached value). For thread safety, use a lock. For cache invalidation, use TTL or explicit invalidation methods. For memory management, use weak references or LRU eviction.

A common interview edge case: what about `__set__` and `__delete__`? For computed attributes, `__set__` should update the cached value (allowing external code to override the computation), and `__delete__` should invalidate the cache (forcing recomputation on next access).

In production systems, computed attributes with caching are used for: database query results (caching expensive JOINs), computed statistics (caching aggregations), and configuration values (loading once from a config file). At senior level, discuss the trade-offs between lazy evaluation (deferred cost) and eager evaluation (upfront cost), and how to choose the right strategy based on access patterns.

**Example:**
```python
import threading

class CachedComputed:
    def __init__(self, func):
        self.func = func
        self.attr_name = None
        self._lock = threading.Lock()

    def __set_name__(self, owner, name):
        self.attr_name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        cache_key = f'_cached_{self.attr_name}'
        if cache_key not in obj.__dict__:
            with self._lock:
                if cache_key not in obj.__dict__:
                    obj.__dict__[cache_key] = self.func(obj)
        return obj.__dict__[cache_key]

    def invalidate(self, obj):
        cache_key = f'_cached_{self.attr_name}'
        obj.__dict__.pop(cache_key, None)

class DataProcessor:
    def __init__(self, data):
        self._data = data

    @CachedComputed
    def mean(self):
        return sum(self._data) / len(self._data)
```

## Q86: What is `__set_name__` and how does it interact with `__init_subclass__`?

**A:** `__set_name__` is called automatically when a class is created (PEP 487). It receives the owner class and the attribute name. `__init_subclass__` is called when a class is subclassed. They work together: `__set_name__` is called for each descriptor in the class, then `__init_subclass__` is called for the subclass.

The execution order is: (1) class body is executed, (2) `__set_name__` is called for each descriptor, (3) `__init_subclass__` is called on parent classes. This means descriptors are fully initialized before `__init_subclass__` runs, so you can access descriptor names in `__init_subclass__`.

A common interview edge case: what about reassignment? If a descriptor is reassigned in a subclass, `__set_name__` is called again with the new name. This allows descriptors to adapt to different names in different classes. For example, a `Field` descriptor might use the attribute name as the database column name.

In production systems, `__set_name__` + `__init_subclass__` are used for: ORM systems (field names become column names), validation frameworks (field names become error message keys), and configuration systems (field names become config keys). At senior level, know that `__set_name__` is called BEFORE `__init_subclass__`, so you can rely on descriptor names being set in `__init_subclass__`.

**Example:**
```python
class Field:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f'_field_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, None)

    def __set__(self, obj, value):
        setattr(obj, self.storage, value)

class Model:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._fields = {
            name: obj for name, obj in cls.__dict__.items()
            if isinstance(obj, Field)
        }

class User(Model):
    name = Field()
    email = Field()

print(User._fields)  # {'name': <Field>, 'email': <Field>}
```

## Q87: How do you implement a descriptor that supports both class-level and instance-level access?

**A:** A descriptor that supports both class-level and instance-level access checks whether `obj` is `None` in `__get__`. If `obj is None`, the descriptor is being accessed on the class (like `MyClass.attr`), so return the descriptor itself or a class-level value. If `obj` is not `None`, it's being accessed on an instance (like `obj.attr`), so return the instance-specific value.

This is important because descriptors can be accessed in two contexts: on the class (for introspection, documentation, or default values) and on instances (for actual data). A well-designed descriptor should handle both gracefully. For example, a `Field` descriptor might return itself when accessed on the class (for introspection) and the field value when accessed on an instance.

A common interview edge case: what about `__set__` on the class? When you write `MyClass.attr = value`, Python's attribute lookup finds the descriptor on the class and calls its `__set__` method (if defined). This allows descriptors to intercept class-level assignments too. However, this can be surprising — assigning to a class attribute might trigger descriptor logic.

In production systems, dual-access descriptors are used in: ORM fields (class-level access returns field metadata, instance-level access returns the value), validation descriptors (class-level access returns the validator, instance-level access returns the validated value), and configuration descriptors (class-level access returns the default, instance-level access returns the override).

**Example:**
```python
class DualAccess:
    def __init__(self, default=None):
        self.default = default
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self  # Class-level access returns descriptor
        return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

class Config:
    timeout = DualAccess(default=30)

print(Config.timeout)         # <DualAccess object> (class-level)
c = Config()
print(c.timeout)              # 30 (instance-level, uses default)
c.timeout = 60
print(c.timeout)              # 60 (instance-level, custom value)
```

## Q88: What is `__bytes__` for serialization and how does it differ from `__reduce__`?

**A:** `__bytes__` returns the byte representation of an object (for `bytes()` calls), while `__reduce__` returns a tuple describing how to recreate the object (for `pickle`). They serve different purposes: `__bytes__` is for explicit binary serialization, while `__reduce__` is for pickle's object reconstruction.

A common interview question: "How does `pickle` use `__bytes__`?" The answer is that pickle doesn't use `__bytes__` directly — it uses `__reduce__` (or `__reduce_ex__`) for custom serialization. `__bytes__` is for `bytes()` calls, not for pickle. However, `__bytes__` is used by `codecs.encode()` and some network protocols. If you want custom pickle behavior, use `__reduce__` or `__getstate__`/`__setstate__`.

A common interview edge case: what about `__getstate__` and `__setstate__`? These are pickle-specific methods that control what state is serialized and how it's restored. `__reduce__` is more general — it returns a callable and arguments that recreate the object. `__getstate__`/`__setstate__` are simpler and more commonly used for pickle customization.

In production systems, `__bytes__` is used for: network protocol serialization, binary file formats, and encryption. `__reduce__` is used for: object reconstruction across processes, distributed computing (FAANG), and caching (storing objects in Redis). At senior level, discuss the trade-offs between `__bytes__` (explicit control) and `__reduce__` (pickle integration).

**Example:**
```python
import pickle

class DatabaseConnection:
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database
        self._handle = None

    def __bytes__(self):
        return f"{self.host}:{self.port}/{self.database}".encode()

    def __reduce__(self):
        return (self.__class__, (self.host, self.port, self.database))

conn = DatabaseConnection("localhost", 5432, "mydb")
wire = bytes(conn)  # b'localhost:5432/mydb'
data = pickle.dumps(conn)
conn2 = pickle.loads(data)
```

## Q89: How do you implement a descriptor that works with `@dataclass`?

**A:** Descriptors work with `@dataclass` because descriptors are class attributes, and `@dataclass` processes class attributes to generate `__init__`, `__repr__`, `__eq__`, etc. When you define a descriptor as a class attribute, `@dataclass` treats it as a field and generates appropriate code.

The key challenge is that `@dataclass` expects fields to be defined with type annotations, and descriptors don't have type annotations by default. You need to use `field()` with `metadata` or custom `__set_name__` to provide type information. Also, `@dataclass` may interfere with descriptor behavior if it generates `__init__` methods that bypass the descriptor.

A common interview edge case: what about `@dataclass(slots=True)`? In Python 3.10+, `@dataclass(slots=True)` creates a class with `__slots__`. Descriptors work with `__slots__` because descriptors are stored on the class, not the instance. However, descriptors that store data in `obj.__dict__` won't work because `__slots__` prevents `__dict__`.

In production systems, descriptors + `@dataclass` are used for: ORM models (combining dataclass syntax with database field descriptors), validation frameworks (combining dataclass syntax with type validation), and API models (combining dataclass syntax with serialization descriptors). At senior level, discuss the interaction between descriptors, `@dataclass`, and `__init_subclass__` for class customization.

**Example:**
```python
from dataclasses import dataclass, field

class Validated:
    def __init__(self, validator):
        self.validator = validator
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f'_validated_{self.name}')

    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}")
        object.__setattr__(obj, f'_validated_{self.name}', value)

@dataclass
class User:
    name: str = field(metadata={'validator': lambda v: isinstance(v, str)})
    age: int = field(metadata={'validator': lambda v: isinstance(v, int)})

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError("name must be str")
        if not isinstance(self.age, int):
            raise TypeError("age must be int")
```

## Q90: What is `__sizeof__` for memory-efficient classes and how do you optimize it?

**A:** `__sizeof__` returns the size in bytes of a single object. For memory-efficient classes, you should override `__sizeof__` to report accurate sizes, especially when using `__slots__` or storing data in external structures. The default `__sizeof__` may not reflect the actual memory usage.

You should override `__sizeof__` when: (1) your class uses `__slots__` (the default size doesn't account for slots), (2) your class stores data in external structures (C buffers, numpy arrays), or (3) you want to include the size of referenced objects in the report. The override should return the total size of the object itself, not including referenced objects.

A common interview edge case: what about the garbage collector overhead? `sys.getsizeof()` adds GC overhead to `__sizeof__` output. For CPython, this adds 16 bytes for GC-tracked objects. Your `__sizeof__` should NOT include GC overhead — that's `sys.getsizeof()`'s job.

In production systems at Tesla (embedded) or Nvidia (GPU memory), `__sizeof__` is used for: memory profiling, capacity planning, and resource management. At senior level, know that `__sizeof__` is a single method call — it doesn't recursively compute the size of referenced objects. For total memory, you need `pympler.asizeof` or a custom recursive traversal.

**Example:**
```python
import sys

class EfficientClass:
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sizeof__(self):
        return (
            sys.getsizeof(self.x)
            + sys.getsizeof(self.y)
            + sys.getsizeof(self.z)
        )

obj = EfficientClass(1, "hello", [1, 2, 3])
print(f"Size: {sys.getsizeof(obj)} bytes")
```

## Q91: How do you implement a descriptor that provides default values?

**A:** A descriptor that provides default values implements `__get__` to return a default value when the attribute hasn't been set on the instance. The descriptor stores the default value and checks the instance's `__dict__` (or slot) for a custom value. If no custom value exists, return the default.

The implementation should handle: mutable defaults (should each instance get its own copy?), immutable defaults (can they be shared?), and type safety (should the default match the expected type?). For mutable defaults, create a new copy for each instance. For immutable defaults, they can be shared. For type safety, validate the default against the expected type.

A common interview edge case: what about `__set__`? For default value descriptors, `__set__` should store the value in the instance's `__dict__` (or slot), allowing external code to override the default. This is different from "read-only" descriptors, which prevent setting.

In production systems, default value descriptors are used in: configuration management (providing default config values), data models (providing default field values), and API objects (providing default response values). At senior level, discuss the trade-offs between default values (convenient but can be surprising) and explicit initialization (verbose but clear).

**Example:**
```python
class Default:
    def __init__(self, value):
        self.default = value
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f'_default_{self.name}', self.default)

    def __set__(self, obj, value):
        object.__setattr__(obj, f'_default_{self.name}', value)

class Config:
    timeout = Default(30)
    retries = Default(3)

c1 = Config()
c2 = Config()
print(c1.timeout)  # 30 (default)
c1.timeout = 60
print(c1.timeout)  # 60 (custom)
print(c2.timeout)  # 30 (still default)
```

## Q92: What is `__class__` for type checking and how does it relate to `isinstance()`?

**A:** `__class__` returns the class of an instance. `isinstance(obj, cls)` checks if `obj` is an instance of `cls` or its subclasses. The relationship is: `isinstance(obj, cls)` is roughly equivalent to `issubclass(type(obj), cls)`, but `isinstance` also handles virtual subclasses (via `__instancecheck__`).

A common interview question: "What is `type(obj)` vs `obj.__class__`?" The answer is that they're usually the same, but `type()` is more reliable because `__class__` can be overridden by descriptors. `type(obj)` always returns the actual class, while `obj.__class__` returns whatever the class's `__class__` descriptor returns. For most objects, they're identical.

A common interview edge case: what about `__instancecheck__`? It's called by `isinstance()` and allows custom type-checking logic. For example, the `abc.ABCMeta` metaclass uses `__instancecheck__` to implement structural subclass checking — a class is considered a subclass of an ABC if it implements the required methods, even without explicit inheritance.

In production systems, `isinstance()` is used for: type validation (ensuring objects have the correct type), protocol enforcement (checking that objects implement required interfaces), and plugin systems (checking if an object matches a plugin interface). At senior level, discuss the performance implications: `isinstance` checks with ABCs are slower than direct inheritance checks because they involve method resolution.

**Example:**
```python
from abc import ABCMeta

class ProtocolMeta(ABCMeta):
    def __instancecheck__(cls, instance):
        if super().__instancecheck__(instance):
            return True
        return all(
            hasattr(instance, method)
            for method in cls._required_methods
        )

class Serializable(metaclass=ProtocolMeta):
    _required_methods = ['serialize', 'deserialize']

class JSON:
    def serialize(self):
        return '{}'
    def deserialize(self, data):
        pass

print(isinstance(JSON(), Serializable))  # True (structural check)
```

## Q93: How do you implement a descriptor that provides type coercion?

**A:** A type-coercing descriptor automatically converts assigned values to the expected type. The descriptor implements `__set__` to convert the value before storing it. For example, a `IntField` descriptor might convert string values to integers: `obj.field = "42"` stores `42`.

The implementation should handle: conversion errors (what if the value can't be converted?), default values (what should the default be?), and round-trip conversion (does converting back to the original type give the same value?). For conversion errors, raise `TypeError` or `ValueError`. For defaults, use `None` or a sentinel value. For round-trip conversion, ensure the conversion is idempotent.

A common interview edge case: what about `__get__`? For type-coercing descriptors, `__get__` returns the coerced value (which is already the correct type). The coercion happens in `__set__`, not `__get__`. This ensures that all assignments are coerced, but reads are fast.

In production systems, type-coercing descriptors are used in: data validation frameworks (Pydantic, Marshmallow), ORM systems (SQLAlchemy column types), and configuration management (ensuring config values have correct types). At senior level, discuss the performance implications of type coercion on every assignment, and how to optimize for hot paths.

**Example:**
```python
class CoercedField:
    def __init__(self, coerce_to):
        self.coerce_to = coerce_to
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f'_coerced_{self.name}')

    def __set__(self, obj, value):
        try:
            coerced = self.coerce_to(value)
        except (ValueError, TypeError) as e:
            raise TypeError(f"Cannot convert {value!r} to {self.coerce_to.__name__}") from e
        object.__setattr__(obj, f'_coerced_{self.name}', coerced)

class User:
    age = CoercedField(int)
    name = CoercedField(str)

u = User()
u.age = "30"    # Coerced to 30
u.name = 123    # Coerced to "123"
print(u.age)    # 30 (int)
print(u.name)   # "123" (str)
```

## Q94: What is `__array_interface__` vs `__buffer__` for numpy integration?

**A:** `__array_interface__` is a dictionary-based protocol for numpy integration, while `__buffer__` is the buffer protocol for general zero-copy access. `__array_interface__` is numpy-specific and easier to implement for simple cases. `__buffer__` is more general and works with any buffer consumer (not just numpy).

The key difference: `__array_interface__` describes the memory layout as a dictionary (data pointer, strides, shape, typestr), while `__buffer__` provides a `Buffer` object that describes the memory layout (itemsize, ndim, shape, strides). `__array_interface__` is higher-level and easier to use, while `__buffer__` is lower-level and more efficient.

A common interview edge case: what about `__array__`? It's even higher-level — it returns a numpy array (possibly copying data). `__array_interface__` is lower-level and allows zero-copy integration. `__buffer__` is even lower-level and works with any buffer consumer.

In production systems at Nvidia (GPU computing) and Tesla (data processing), `__array_interface__` is used for: zero-copy integration with numpy, while `__buffer__` is used for: general buffer access (including numpy, but also other consumers). At senior level, know that `__array_interface__` requires the object to maintain a consistent memory layout — if the data is moved or resized after creating the array view, numpy operations will use stale data or segfault.

**Example:**
```python
import numpy as np

class Matrix:
    def __init__(self, rows, cols, data):
        self.rows = rows
        self.cols = cols
        self._data = data

    @property
    def __array_interface__(self):
        return {
            'data': (id(self._data), False),
            'strides': (self.cols * 8,),
            'typestr': '<f8',
            'shape': (self.rows, self.cols),
            'version': 3,
        }

    def __buffer__(self, flags):
        return memoryview(self._data)

data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
m = Matrix(2, 3, data)
arr1 = np.asarray(m)        # Uses __array_interface__
arr2 = np.frombuffer(m)     # Uses __buffer__
```

## Q95: How do you implement a descriptor that provides computed properties with dependency tracking?

**A:** A computed property with dependency tracking automatically invalidates cached values when dependencies change. The descriptor tracks which attributes it depends on and invalidates the cache when any dependency is modified. This is useful for complex computations that depend on multiple attributes.

The implementation should handle: dependency discovery (how to know which attributes to track?), invalidation (when should the cache be invalidated?), and performance (how to minimize the overhead of dependency tracking?). For dependency discovery, use introspection or explicit declaration. For invalidation, use signals or `__setattr__` interception. For performance, use lazy invalidation (only check dependencies on access).

A common interview edge case: what about circular dependencies? If attribute A depends on B, and B depends on A, you have a circular dependency. The descriptor should detect this and raise an error, or use a topological sort to determine the correct evaluation order.

In production systems, dependency tracking is used in: reactive systems (automatically updating UI when data changes), spreadsheet-like calculations (automatically recalculating formulas), and data processing pipelines (automatically invalidating cached results). At senior level, discuss the trade-offs between eager invalidation (immediate but potentially expensive) and lazy invalidation (deferred but may compute stale values).

**Example:**
```python
class DependentProperty:
    def __init__(self, func, dependencies=None):
        self.func = func
        self.dependencies = dependencies or []
        self.attr_name = None

    def __set_name__(self, owner, name):
        self.attr_name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        cache_key = f'_cached_{self.attr_name}'
        deps_key = f'_deps_{self.attr_name}'

        if cache_key in obj.__dict__:
            cached_deps = obj.__dict__.get(deps_key, [])
            current_deps = [getattr(obj, d) for d in self.dependencies]
            if cached_deps == current_deps:
                return obj.__dict__[cache_key]

        value = self.func(obj)
        obj.__dict__[cache_key] = value
        obj.__dict__[deps_key] = [getattr(obj, d) for d in self.dependencies]
        return value

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @DependentProperty(func=lambda self: self.width * self.height, dependencies=['width', 'height'])
    def area(self):
        return self.width * self.height
```

## Q96: What is `__class__` for metaclass programming and how do you use it safely?

**A:** `__class__` is an attribute that returns the class of an instance. For metaclass programming, you can override `__class__` to change what `type(obj)` returns. This is powerful but dangerous — it can break debugging tools, type checkers, and third-party code that relies on `type()`.

The safe approach is to use `__class__` assignment only when you have a specific reason (like the State pattern or proxy objects) and when you understand the implications. Always ensure that the new class is compatible with the original class (same base classes, same methods). Also, document the `__class__` assignment clearly so other developers understand what's happening.

A common interview edge case: what about `type(obj)` vs `obj.__class__`? `type(obj)` always returns the actual class, while `obj.__class__` returns whatever the `__class__` descriptor returns. For most objects, they're identical. But if you override `__class__`, `type(obj)` still returns the original class, while `obj.__class__` returns the new class. This inconsistency can be confusing.

In production systems, `__class__` assignment is used in: State pattern (changing object behavior based on state), proxy objects (forwarding attribute access to a wrapped object), and dynamic type switching (changing the type of an object at runtime). At senior level, discuss the trade-offs between `__class__` assignment (powerful but dangerous) and composition (safer but more verbose).

**Example:**
```python
class State:
    def __init__(self, obj):
        self._obj = obj

    def transition(self, new_state):
        self._obj.__class__ = new_state

class OffState(State):
    def toggle(self):
        print("Turning on")
        self.transition(OnState)

class OnState(State):
    def toggle(self):
        print("Turning off")
        self.transition(OffState)

class LightSwitch:
    pass

switch = LightSwitch()
switch.__class__ = OffState
switch.toggle()  # "Turning on"
switch.toggle()  # "Turning off"
```

## Q97: How do you implement a descriptor that provides validation with custom error messages?

**A:** A validating descriptor with custom error messages checks assigned values against constraints and raises descriptive errors. The descriptor stores the validation function and error message, and uses `__set_name__` to automatically know its name in the class.

The implementation should handle: multiple constraints (AND/OR logic), custom error messages (per constraint), and error formatting (including attribute name and value). For multiple constraints, chain validation functions. For custom error messages, accept a message template. For error formatting, include the attribute name and the invalid value.

A common interview edge case: what about `__get__`? For validating descriptors, `__get__` returns the stored value (which is already validated). The validation happens in `__set__`, not `__get__`. This ensures that all assignments are validated, but reads are fast.

In production systems, validating descriptors are used in: data validation frameworks (Pydantic, Marshmallow), ORM systems (SQLAlchemy column constraints), and configuration management (ensuring config values meet requirements). At senior level, discuss the trade-offs between validation at assignment time (immediate feedback but potential performance impact) and validation at read time (deferred cost but may allow invalid intermediate states).

**Example:**
```python
class Validated:
    def __init__(self, validator, error_msg=None):
        self.validator = validator
        self.error_msg = error_msg or "{name} is invalid"
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f'_validated_{self.name}')

    def __set__(self, obj, value):
        if not self.validator(value):
            msg = self.error_msg.format(name=self.name, value=value)
            raise ValueError(msg)
        object.__setattr__(obj, f'_validated_{self.name}', value)

class User:
    age = Validated(
        lambda v: isinstance(v, int) and 0 <= v <= 150,
        error_msg="{name} must be between 0 and 150, got {value}"
    )

u = User()
u.age = 30        # OK
# u.age = 200     # ValueError: age must be between 0 and 150, got 200
```

## Q98: What is `__sizeof__` for memory profiling and how do you integrate it with profiling tools?

**A:** `__sizeof__` returns the size in bytes of a single object. When integrated with profiling tools, it provides accurate memory measurements for individual objects. Python's `sys.getsizeof()` calls `__sizeof__()` and adds GC overhead, making it the standard way to measure object size.

For integration with profiling tools, override `__sizeof__` to report accurate sizes for your specific class. This is especially important for: classes with `__slots__` (the default size doesn't account for slots), classes with external data (C buffers, numpy arrays), and classes with computed sizes (where the size depends on runtime state).

A common interview edge case: what about `pympler.asizeof`? It recursively computes the total size of an object and all its references. This is more accurate than `sys.getsizeof()` for complex object graphs, but it's much slower. For production profiling, use `sys.getsizeof()` for individual objects and `pympler.asizeof` for total memory.

In production systems at Tesla (embedded) or Nvidia (GPU memory), `__sizeof__` is used for: memory profiling, capacity planning, and resource management. At senior level, discuss the trade-offs between accuracy (reporting the exact size) and performance (measuring quickly). For most use cases, `sys.getsizeof()` is sufficient. For complex object graphs, use `pympler.asizeof`.

**Example:**
```python
import sys

class ProfiledClass:
    __slots__ = ('data', 'metadata')

    def __init__(self, data, metadata):
        self.data = data
        self.metadata = metadata

    def __sizeof__(self):
        return sys.getsizeof(self.data) + sys.getsizeof(self.metadata)

obj = ProfiledClass([1, 2, 3], {"key": "value"})
print(f"Size: {sys.getsizeof(obj)} bytes")
```

## Q99: How do you implement a descriptor that provides attribute access logging?

**A:** An attribute-access logging descriptor intercepts all reads and writes to an attribute and logs them. The descriptor implements `__get__` and `__set__` to log access patterns. This is useful for debugging, auditing, and performance analysis.

The implementation should handle: log level (DEBUG, INFO, WARNING), log format (including timestamp, attribute name, value), and performance (minimizing logging overhead). For log level, use the `logging` module. For log format, include context information. For performance, use lazy logging (only log when logging is enabled).

A common interview edge case: what about thread safety? If multiple threads access the same attribute, the logging must be thread-safe. Use `threading.Lock` or `logging` module's thread safety. Also, consider the overhead of logging on every access — in production, you might want to disable logging or use sampling.

In production systems, attribute-access logging is used in: debugging (tracking attribute access patterns), auditing (logging all modifications to sensitive attributes), and performance analysis (identifying hot attributes). At Tesla, vehicle configuration attributes use logging to track who changed critical parameters. At senior level, discuss the trade-offs between logging granularity (every access vs. sampling) and performance impact.

**Example:**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Logged:
    def __init__(self, default=None):
        self.default = default
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = getattr(obj, f'_logged_{self.name}', self.default)
        logger.debug(f"GET {self.name} = {value!r}")
        return value

    def __set__(self, obj, value):
        logger.debug(f"SET {self.name} = {value!r}")
        object.__setattr__(obj, f'_logged_{self.name}', value)

class Config:
    timeout = Logged(default=30)

c = Config()
c.timeout = 60  # DEBUG: SET timeout = 60
print(c.timeout)  # DEBUG: GET timeout = 60
```

## Q100: Design a complete descriptor-based ORM field system with type validation, default values, and lazy loading.

**A:** A complete descriptor-based ORM field system combines multiple descriptor patterns: type validation (ensuring correct types), default values (providing sensible defaults), and lazy loading (deferring expensive operations). The system uses a base `Field` descriptor that's extended by specific field types (StringField, IntegerField, etc.).

The implementation should handle: field registration (tracking all fields in a class), instance storage (storing values efficiently), and query integration (supporting database queries). For field registration, use `__set_name__` to automatically register fields. For instance storage, use `__dict__` or `__slots__`. For query integration, provide class methods for querying.

A common interview edge case: what about relationships? Relationships (ForeignKey, ManyToMany) are more complex — they need to load related objects lazily, handle cascading deletes, and support join queries. The descriptor pattern can be extended to handle relationships by storing the foreign key value and loading the related object on access.

In production systems, this pattern is the foundation of ORM systems like SQLAlchemy and Django ORM. At senior level, discuss the trade-offs between descriptor-based ORMs (flexible but complex) and code-generation ORMs (fast but less flexible), and how to optimize for different workloads (read-heavy vs. write-heavy).

**Example:**
```python
class Field:
    def __init__(self, field_type, default=None, nullable=True):
        self.field_type = field_type
        self.default = default
        self.nullable = nullable
        self.name = None
        self.column_name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.column_name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = getattr(obj, f'_field_{self.name}', self.default)
        if value is None and not self.nullable:
            raise ValueError(f"{self.name} cannot be None")
        return value

    def __set__(self, obj, value):
        if value is None and not self.nullable:
            raise ValueError(f"{self.name} cannot be None")
        if value is not None and not isinstance(value, self.field_type):
            raise TypeError(
                f"{self.name} must be {self.field_type.__name__}, "
                f"got {type(value).__name__}"
            )
        object.__setattr__(obj, f'_field_{self.name}', value)

class StringField(Field):
    def __init__(self, max_length=255, **kwargs):
        super().__init__(str, **kwargs)
        self.max_length = max_length

    def __set__(self, obj, value):
        if value is not None and len(value) > self.max_length:
            raise ValueError(f"{self.name} exceeds max length {self.max_length}")
        super().__set__(obj, value)

class IntegerField(Field):
    def __init__(self, min_value=None, max_value=None, **kwargs):
        super().__init__(int, **kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def __set__(self, obj, value):
        if value is not None:
            if self.min_value is not None and value < self.min_value:
                raise ValueError(f"{self.name} must be >= {self.min_value}")
            if self.max_value is not None and value > self.max_value:
                raise ValueError(f"{self.name} must be <= {self.max_value}")
        super().__set__(obj, value)

class Model:
    _fields = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._fields = {
            name: obj for name, obj in cls.__dict__.items()
            if isinstance(obj, Field)
        }

    def to_dict(self):
        return {name: getattr(self, name) for name in self._fields}

class User(Model):
    name = StringField(max_length=100)
    age = IntegerField(min_value=0, max_value=150)
    email = StringField(max_length=255, nullable=False)

u = User()
u.name = "Alice"
u.age = 30
u.email = "alice@example.com"
print(u.to_dict())  # {'name': 'Alice', 'age': 30, 'email': 'alice@example.com'}
```
