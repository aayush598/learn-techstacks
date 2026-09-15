# Decorator, Composite and Bridge — 100 Interview Q&A

## Q1: What is the Decorator pattern and what problem does it solve?

**A:** The Decorator pattern is a structural design pattern that allows you to dynamically add new behavior to objects by wrapping them in decorator objects. Instead of modifying the original class or using inheritance to add functionality, decorators provide a flexible alternative by composing objects with additional responsibilities at runtime. This solves the "class explosion" problem that arises when you try to support every combination of features through inheritance.

The core problem the Decorator pattern addresses is the rigid coupling between behavior and class hierarchy. With inheritance, adding a feature means creating a new subclass, and combining N features requires up to 2^N subclasses. Decorators eliminate this by allowing you to wrap an object with any combination of decorators at runtime. Each decorator implements the same interface as the object it wraps, so the client code does not know whether it is dealing with the original object or a decorated one.

In Python, the Decorator pattern manifests in two forms: the GoF Decorator pattern (class-based wrappers) and Python's `@decorator` syntax (function wrappers). Both share the same principle — adding behavior without modifying the original object — but differ in implementation. The GoF pattern uses object composition, while Python's `@decorator` uses function composition. Understanding both forms is essential for interviews because they test different aspects of the pattern.

```python
class TextProcessor:
    def process(self, text):
        return text

class UpperDecorator:
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def process(self, text):
        return self._wrapped.process(text).upper()

class TrimDecorator:
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def process(self, text):
        return self._wrapped.process(text).strip()

base = TextProcessor()
decorated = TrimDecorator(UpperDecorator(base))
print(decorated.process("  hello world  "))  # "HELLO WORLD"
```

## Q2: Explain the structure of the Decorator pattern with its key participants.

**A:** The Decorator pattern has four key participants: the Component interface, the Concrete Component, the Decorator base class, and Concrete Decorators. The Component interface defines the common interface for both the original object and all decorators. The Concrete Component is the original object whose behavior you want to extend. The Decorator base class implements the Component interface and holds a reference to a Component object (the wrapped object). Concrete Decorators add specific behavior before or after delegating to the wrapped object.

The critical design constraint is that both Decorators and Components share the same interface. This means clients can treat decorated and undecorated objects identically. A decorator can wrap any Component, including other decorators, which enables stacking multiple decorators. The decorator delegates to the wrapped object by calling the same method on it, allowing the decorator to add behavior before or after the delegation (or to skip the delegation entirely).

In Python, the Component is typically an abstract base class or a protocol. The Decorator base class inherits from the Component and stores a reference to the wrapped Component in its `__init__`. Each Concrete Decorator overrides the relevant methods to add behavior. The Python `@decorator` syntax is a syntactic sugar for this pattern when applied to functions — the decorator function wraps the original function and returns a new function with added behavior.

```python
from abc import ABC, abstractmethod

class DataSource(ABC):
    @abstractmethod
    def write_data(self, data):
        pass

class FileDataSource(DataSource):
    def __init__(self, filename):
        self.filename = filename

    def write_data(self, data):
        print(f"Writing {data} to {self.filename}")

class EncryptionDecorator(DataSource):
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def write_data(self, data):
        encrypted = f"ENCRYPTED({data})"
        self._wrapped.write_data(encrypted)

class CompressionDecorator(DataSource):
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def write_data(self, data):
        compressed = f"COMPRESSED({data})"
        self._wrapped.write_data(compressed)

source = CompressionDecorator(EncryptionDecorator(FileDataSource("file.txt")))
source.write_data("secret data")
# Writing COMPRESSED(ENCRYPTED(secret data)) to file.txt
```

## Q3: When should you use the Decorator pattern versus inheritance?

**A:** Use the Decorator pattern when you need to add responsibilities to objects dynamically, when subclassing is impractical due to class explosion, or when you need to combine multiple independent behaviors. Use inheritance when the relationship is a true "is-a" relationship and the behavior is static and known at compile time. Decorators are preferred when behavior must be added or removed at runtime, when the same behavior needs to be applied to different class hierarchies, or when you need to combine multiple behaviors in different orders.

The key distinction is between "is-a" and "has-a" relationships with behavior extension. Inheritance implies a permanent, compile-time commitment to a specific behavior. Decorators imply a flexible, runtime composition of behaviors. If you find yourself creating many subclasses to handle different combinations of features, the Decorator pattern is likely more appropriate. For example, a text processor that needs bold, italic, and underline formatting would require 7 subclasses (2^3 - 1) using inheritance, but only 3 decorators using the Decorator pattern.

A practical rule of thumb is: use inheritance for core identity (a `Dog` IS an `Animal`), use decorators for optional behavior (a `Dog` CAN have `GPS tracking`). Decorators are also preferable when the behavior needs to be applied across unrelated class hierarchies — a logging decorator can wrap a file processor, a network handler, or a database connector without requiring them to share a common base class.

```python
# Inheritance approach — rigid, requires many subclasses
class TextProcessor:
    def process(self, text): return text
class UpperText(TextProcessor):
    def process(self, text): return super().process(text).upper()
class TrimText(TextProcessor):
    def process(self, text): return super().process(text).strip()
class UpperTrimText(UpperText):  # Combining features requires new class
    def process(self, text): return super().process(text).strip()

# Decorator approach — flexible, composable at runtime
class UpperDecorator:
    def __init__(self, wrapped): self._wrapped = wrapped
    def process(self, text): return self._wrapped.process(text).upper()

class TrimDecorator:
    def __init__(self, wrapped): self._wrapped = wrapped
    def process(self, text): return self._wrapped.process(text).strip()

# Any combination works without new classes:
decorated = UpperDecorator(TrimDecorator(TextProcessor()))
```

## Q4: How do you implement the Decorator pattern in Python using `functools.wraps`?

**A:** Python's `@decorator` syntax is the functional form of the Decorator pattern. A decorator is a function that takes a function and returns a new function with added behavior. `functools.wraps` preserves the original function's metadata (`__name__`, `__doc__`, `__module__`, etc.) in the wrapper function. Without `functools.wraps`, the wrapper function would have different metadata, which can break debugging tools, documentation generators, and introspection.

The implementation pattern is straightforward: define a decorator function that takes a function as input, define a wrapper function inside it that adds behavior and calls the original function, use `@functools.wraps(original)` on the wrapper to preserve metadata, and return the wrapper. The wrapper can add behavior before the call (pre-processing), after the call (post-processing), around the call (error handling, retries), or instead of the call (caching, short-circuiting).

`functools.wraps` copies `__module__`, `__name__`, `__qualname__`, `__doc__`, `__dict__`, and `__wrapped__` from the original function to the wrapper. The `__wrapped__` attribute is particularly useful because it allows you to access the original function through the wrapper. This is important for testing and for nested decorators where you need to unwrap the decorator chain.

```python
import functools

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    """Add two numbers."""
    return a + b

print(add(1, 2))  # Calling add with (1, 2), {}
print(add.__name__)  # 'add' — metadata preserved
print(add.__doc__)   # 'Add two numbers.' — docstring preserved
```

## Q5: What is the difference between the GoF Decorator pattern and Python's `@decorator`?

**A:** The GoF Decorator pattern is a class-based structural pattern that wraps objects with decorator objects sharing the same interface. Python's `@decorator` is a syntactic sugar for function composition where a wrapper function replaces the original function. Both add behavior without modifying the original, but they operate at different levels: the GoF pattern wraps objects (instances), while Python's `@decorator` wraps functions (callables).

The GoF pattern is implemented with classes that inherit from a common Component interface. Each decorator holds a reference to the wrapped object and delegates method calls to it. This works well for adding behavior to objects with state and multiple methods. Python's `@decorator` is implemented with higher-order functions. The decorator function receives the original function and returns a new function. This works well for adding behavior to functions but is less natural for objects with multiple methods.

In practice, many Python developers use both forms. The `@decorator` syntax is used for function-level concerns (logging, caching, validation, retry logic). The class-based Decorator pattern is used for object-level concerns (adding encryption to data sources, adding formatting to text processors). Python's duck typing makes the class-based pattern less rigid than in statically typed languages — you do not need to formally declare that a class implements a Component interface, as long as it has the required methods.

```python
# GoF Decorator — class-based, wraps objects
class Notifier:
    def send(self, message): print(message)

class SMSNotifier:
    def __init__(self, wrapped): self._wrapped = wrapped
    def send(self, message):
        print(f"SMS: {message}")
        self._wrapped.send(message)

# Python @decorator — function-based, wraps functions
def retry(max_attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Retry {attempt + 1}/{max_attempts}")
        return wrapper
    return decorator

@retry(max_attempts=3)
def unstable_function():
    pass
```

## Q6: How do you stack multiple decorators in Python and what is the execution order?

**A:** Multiple decorators are applied bottom-up (innermost first) when defined, and top-down (outermost first) when called. When you write `@decorator_a @decorator_b @decorator_c def func:`, Python applies `decorator_c` first (wrapping `func`), then `decorator_b` (wrapping the result), then `decorator_a` (wrapping the result). At call time, `decorator_a`'s wrapper runs first, then `decorator_b`'s, then `decorator_c`'s, and finally the original function.

This order matters because it determines which decorator's pre-processing runs first and which runs last. For logging decorators, the outermost decorator logs first. For security decorators, the outermost decorator should check permissions first. For caching decorators, the caching layer should be outermost to short-circuit before other decorators run. Understanding this order is critical for correctly composing decorators.

The composition can be visualized as a chain: `decorator_a(decorator_b(decorator_c(func)))`. When the decorated function is called, execution flows through `decorator_a` → `decorator_b` → `decorator_c` → `func`. Return values flow back through the same chain in reverse. This LIFO order means that pre-processing follows the decorator definition order (top to bottom), while post-processing follows the reverse order (bottom to top).

```python
import functools

def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

@bold
@italic
def greet(name):
    return f"Hello, {name}"

print(greet("World"))  # <b><i>Hello, World</i></b>
# bold wraps italic, which wraps greet
# Call order: bold → italic → greet
```

## Q7: What is a decorator factory and when would you use one?

**A:** A decorator factory is a function that returns a decorator. It allows you to parameterize decorators — passing configuration to the decorator that controls its behavior. The outer function (factory) accepts parameters, the middle function (decorator) accepts the function to wrap, and the inner function (wrapper) adds the behavior. This three-layer structure is necessary because `@decorator_with_args` syntax requires the decorator to be callable with the function as its argument.

The pattern is: `@decorator_factory(arg)` is equivalent to `func = decorator_factory(arg)(func)`. The factory is called with `arg`, returns a decorator, and that decorator is called with `func` to produce the wrapper. This is used when decorators need configuration like retry counts, cache TTLs, log levels, or validation rules. Without the factory pattern, you would need to use global variables or class-based decorators to pass configuration.

The naming convention is to name the factory with the same name as the decorator it produces (without the factory suffix). This makes the usage site clean: `@retry(max_attempts=3)` looks like a single decorator, not a factory call. The factory can also support both with and without arguments by detecting whether the first argument is a callable (the function) or a configuration value.

```python
import functools

def retry(max_attempts=3, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
        return wrapper
    return decorator

@retry(max_attempts=5, exceptions=(ValueError, ConnectionError))
def fetch_data(url):
    pass

@retry  # Without arguments — uses defaults
def simple_task():
    pass
```

## Q8: How does the Decorator pattern relate to the Open-Closed Principle?

**A:** The Decorator pattern is a direct application of the Open-Closed Principle (OCP), which states that classes should be open for extension but closed for modification. Decorators extend behavior by adding new objects to the composition, not by modifying existing classes. This means you can add new functionality to a system without changing the code of the original classes, which is exactly what OCP requires.

The key insight is that the Decorator pattern achieves extension through composition rather than inheritance. When you need to add logging to a function, you wrap it with a logging decorator instead of modifying the function's code. When you need to add encryption to a data source, you wrap it with an encryption decorator instead of modifying the data source class. The original classes remain unchanged (closed for modification) while new behavior is added through decorators (open for extension).

This is important for maintaining large codebases because it reduces the risk of breaking existing functionality when adding new features. Each decorator is independent and can be tested in isolation. The decorator chain can be reconfigured at runtime to add or remove behavior. This flexibility is why the Decorator pattern is so widely used in Python — from `functools.lru_cache` to `Django's` `@login_required` to `Flask's` `@app.route`.

```python
# Violating OCP — modifying the class
class DataProcessor:
    def process(self, data):
        # Original code
        return data.upper()

# Following OCP — extending through decorators
class DataProcessor:
    def process(self, data):
        return data.upper()

def validate_input(func):
    def wrapper(data):
        if not isinstance(data, str):
            raise TypeError("Input must be string")
        return func(data)
    return wrapper

def log_processing(func):
    def wrapper(data):
        print(f"Processing: {data}")
        result = func(data)
        print(f"Result: {result}")
        return result
    return wrapper

@log_processing
@validate_input
def process_data(data):
    return data.upper()
```

## Q9: How do you implement a decorator that preserves the decorated function's signature?

**A:** Preserving function signatures is important for IDE support, type checking, and introspection. The simplest approach is `functools.wraps`, which copies `__name__`, `__doc__`, and `__dict__`, but does not copy the actual signature for static analysis tools. For full signature preservation, use `inspect.signature()` to copy the signature from the original function to the wrapper, or use the `decorator` library which handles this automatically.

The `inspect` module provides tools for signature manipulation. `inspect.signature(func)` returns a `Signature` object that describes the function's parameters. You can then set `wrapper.__signature__ = inspect.signature(original)` to make the wrapper's signature match the original. This ensures that tools like `mypy`, IDE autocomplete, and `help()` display the correct signature.

For more complex cases (decorators that add parameters), you can use `inspect.Parameter` to modify the signature. For example, a `@retry(max_attempts=3)` decorator adds a `max_attempts` parameter to the wrapper's signature. This is done by constructing a new `Signature` object with the additional parameters and setting it on the wrapper. This is an advanced technique used in framework development.

```python
import functools
import inspect

def preserve_signature(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.__signature__ = inspect.signature(func)
    return wrapper

@preserve_signature
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

print(inspect.signature(add))  # (a: int, b: int) -> int
print(add.__doc__)             # 'Add two numbers.'
```

## Q10: What are the common use cases for the Decorator pattern in Python frameworks?

**A:** Python frameworks use decorators extensively for cross-cutting concerns. Common use cases include: logging (`@log_calls`), caching (`@functools.lru_cache`), authentication (`@login_required`), authorization (`@permission_required`), rate limiting (`@rate_limit`), retry logic (`@retry`), timing (`@timer`), input validation (`@validate`), memoization (`@memoize`), and routing (`@app.route`). These decorators share a common pattern: they wrap a function to add behavior before, after, or around the original function call.

Web frameworks like Django and Flask use decorators as the primary mechanism for defining URL routes, requiring authentication, and configuring view behavior. `@app.route('/path')` in Flask registers a function as a URL handler. `@login_required` in Django ensures the user is authenticated before the view runs. These decorators are not just syntactic sugar — they fundamentally change how the decorated function is invoked and integrated into the framework.

Testing frameworks use decorators to mark tests with metadata (`@pytest.mark.slow`), to set up fixtures (`@pytest.fixture`), and to skip tests under certain conditions (`@pytest.skip`). Serialization libraries use decorators to define custom serialization logic (`@dataclass`). ORM libraries use decorators to map Python classes to database tables (`@dataclass` in SQLAlchemy). The decorator pattern is so ubiquitous in Python that understanding it is essential for framework-level development.

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

def retry(max_attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
        return wrapper
    return decorator

@timer
@retry(max_attempts=3)
def slow_function():
    time.sleep(0.1)
    return "done"

slow_function()  # Prints timing info
```

## Q11: How do you implement a class-based decorator in Python?

**A:** A class-based decorator is a class that implements the `__call__` method, making instances callable. When you use `@MyDecorator`, Python creates an instance of `MyDecorator` with the decorated function as an argument, and replaces the original function with this instance. Since the instance has a `__call__` method, it can be invoked like a function. This approach is useful when the decorator needs to maintain state, when the logic is complex, or when you want to use inheritance to create decorator hierarchies.

The class-based decorator stores the wrapped function in `__init__` and implements `__call__` to add behavior before or after delegating to the wrapped function. The `__call__` method receives the same arguments as the original function and must return the same type of result. Unlike function-based decorators, class-based decorators can have multiple methods (for different aspects of the behavior) and can maintain internal state across calls.

A key advantage of class-based decorators is that they can be subclassed to create specialized decorators. For example, a `CacheDecorator` base class can be subclassed to create `LRUCacheDecorator`, `TTLCacheDecorator`, and `FileCacheDecorator`. Each subclass overrides the caching strategy while inheriting the core caching logic. This is more natural than function-based decorators, which cannot be easily extended through inheritance.

```python
import functools
import time

class Timer:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.total_time = 0
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        start = time.time()
        result = self.func(*args, **kwargs)
        elapsed = time.time() - start
        self.total_time += elapsed
        self.call_count += 1
        print(f"{self.func.__name__} took {elapsed:.4f}s")
        return result

    def stats(self):
        avg = self.total_time / self.call_count if self.call_count else 0
        return {"total": self.total_time, "calls": self.call_count, "avg": avg}

@Timer
def compute(n):
    return sum(range(n))

compute(1000000)
compute(2000000)
print(compute.stats())  # {'total': ..., 'calls': 2, 'avg': ...}
```

## Q12: What is the transparent decorator pattern and how does it differ from the opaque decorator pattern?

**A:** The transparent decorator pattern allows the client to interact with the decorated object without knowing that it is decorated. The decorator implements the same interface as the wrapped object, so the client code works identically with decorated and undecorated objects. The opaque decorator pattern intentionally reveals that the object is decorated, often by adding new methods or attributes that are not part of the original interface.

The transparent pattern is the standard GoF Decorator implementation. The decorator delegates all methods to the wrapped object and only overrides the methods it wants to augment. The client never knows that the object is wrapped. This is useful for adding cross-cutting concerns (logging, caching, validation) that should be invisible to the caller.

The opaque pattern is used when the decorator's additional behavior needs to be visible to the caller. For example, a decorator might add a `get_stats()` method that returns performance statistics, or a `disable()` method that temporarily disables the decorator's behavior. The client must know about the decorator to use these additional methods, which breaks the transparency. This is sometimes called the "leaky decorator" pattern and is useful when the decorator needs to expose configuration or status information.

```python
# Transparent decorator — client doesn't know it's decorated
class DataSource:
    def read(self): return "data"

class EncryptionDecorator:
    def __init__(self, wrapped):
        self._wrapped = wrapped
    def read(self):
        return f"DECRYPTED({self._wrapped.read()})"

source = EncryptionDecorator(DataSource())
print(source.read())  # DECRYPTED(data) — transparent

# Opaque decorator — client knows about the decorator
class LoggingDecorator:
    def __init__(self, wrapped):
        self._wrapped = wrapped
        self.log_count = 0

    def read(self):
        self.log_count += 1
        return self._wrapped.read()

    def get_log_count(self):
        return self.log_count

logging_source = LoggingDecorator(DataSource())
logging_source.read()
print(logging_source.get_log_count())  # 1 — opaque
```

## Q13: How do you handle exceptions in decorators and what are the best practices?

**A:** Exception handling in decorators determines whether exceptions propagate to the caller, are caught and logged, or are transformed into different exceptions. The decorator's wrapper function can use try/except blocks to catch exceptions from the wrapped function, log them, retry the call, or raise a different exception. The best practice is to preserve the original exception type and traceback unless you have a specific reason to transform it.

Common patterns include: (1) catch-and-retry (catch the exception, wait, and retry the function), (2) catch-and-log (catch the exception, log it, and re-raise), (3) catch-and-transform (catch one exception type and raise another), and (4) catch-and-suppress (catch the exception and return a default value). The choice depends on the use case: retry decorators catch and retry, logging decorators catch and re-raise, and fallback decorators catch and return defaults.

A best practice is to always re-raise exceptions if you catch them, unless the decorator's explicit purpose is to suppress exceptions. Suppressing exceptions silently (without logging) makes debugging difficult because the caller has no indication that something went wrong. If you must suppress exceptions, log them at a minimum. Another best practice is to use `raise ... from e` when transforming exceptions, which preserves the original exception chain and makes debugging easier.

```python
import functools
import logging

def handle_exceptions(default=None, log_level=logging.ERROR):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.log(log_level, f"{func.__name__} failed: {e}")
                if default is not None:
                    return default
                raise
        return wrapper
    return decorator

@handle_exceptions(default="fallback")
def risky_operation():
    raise ValueError("something went wrong")

print(risky_operation())  # "fallback" — exception suppressed with logging
```

## Q14: What is the difference between function decorators and class decorators?

**A:** Function decorators wrap a function with another function, adding behavior before, after, or around the original function call. Class decorators wrap a class with another class or function, modifying the class itself (not its instances). Function decorators are used for function-level concerns (logging, caching, validation). Class decorators are used for class-level concerns (adding methods, modifying the metaclass, registering the class).

Function decorators receive the function as input and return a wrapper function. The wrapper is called instead of the original function. Class decorators receive the class as input and return a modified class or a wrapper class. The modification can add new methods, modify existing methods, change the class's metaclass, or register the class in a global registry. Class decorators are an alternative to metaclasses for many use cases.

The key difference is the scope of the modification. Function decorators affect individual function calls. Class decorators affect all instances of the class. A function decorator can add retry logic to a single function. A class decorator can add retry logic to all methods of a class. Class decorators are also composable — you can stack multiple class decorators to add multiple behaviors. This makes class decorators a powerful tool for modifying existing classes without inheritance.

```python
import functools

# Function decorator — wraps individual functions
def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# Class decorator — modifies the entire class
def add_repr(cls):
    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'{cls.__name__}({attrs})'
    cls.__repr__ = __repr__
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(p)  # Point(x=1, y=2)
```

## Q15: How do you implement a decorator that works with both regular functions and methods?

**A:** Decorating methods requires handling the implicit `self` parameter. When a decorator wraps a method, the `self` argument is passed as the first positional argument to the wrapper. The decorator must correctly pass `self` to the original method. This is straightforward with `functools.wraps` and `*args, **kwargs`, but requires care when the decorator needs to access the instance (e.g., for logging the instance's class name).

The standard approach uses `*args, **kwargs` in the wrapper, which naturally handles both regular functions and methods. The `self` parameter is just the first element of `args` for methods. For decorators that need to distinguish between functions and methods, you can use `inspect.signature()` to check whether the first parameter is named `self` or `cls`. However, this is rarely necessary — most decorators work correctly with both functions and methods without modification.

A more nuanced issue is decorating static methods, class methods, and properties. Static methods do not receive `self` or `cls`, so decorators work normally. Class methods receive `cls` as the first argument, which is handled by `*args`. Properties are descriptors, so decorators must be applied to the getter/setter/deleter functions, not to the property itself. The `@property` decorator must be the outermost decorator in the chain.

```python
import functools

def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__} on {args[0].__class__.__name__}")
        return func(*args, **kwargs)
    return wrapper

class Calculator:
    @log_execution
    def add(self, a, b):
        return a + b

    @log_execution
    @staticmethod
    def multiply(a, b):
        return a * b

calc = Calculator()
print(calc.add(1, 2))         # Executing add on Calculator
print(Calculator.multiply(3, 4))  # Executing multiply on Calculator
```

## Q16: What is the Composite pattern and what problem does it solve?

**A:** The Composite pattern is a structural design pattern that lets you compose objects into tree structures to represent part-whole hierarchies. It allows clients to treat individual objects (leaves) and compositions of objects (composites) uniformly through a common interface. This solves the problem of working with tree structures where you need to perform operations on both individual items and groups of items without writing separate code for each.

The core problem the Composite pattern addresses is the asymmetry between individual objects and collections. Without Composite, client code must check whether an object is a leaf or a composite and handle each case differently. This leads to type checking throughout the codebase, makes adding new node types difficult, and violates the Open-Closed Principle. Composite eliminates this by providing a uniform interface that both leaves and composites implement.

The pattern is used extensively in GUI frameworks (widgets containing widgets), file systems (files and directories), organizational structures (employees and managers), and document structures (paragraphs and sections). In each case, the tree structure is natural, and the ability to treat leaves and composites uniformly simplifies client code significantly.

```python
from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def operation(self):
        pass

class Leaf(Component):
    def __init__(self, name):
        self.name = name

    def operation(self):
        return f"Leaf({self.name})"

class Composite(Component):
    def __init__(self, name):
        self.name = name
        self._children = []

    def add(self, component):
        self._children.append(component)

    def remove(self, component):
        self._children.remove(component)

    def operation(self):
        results = [child.operation() for child in self._children]
        return f"Composite({self.name}): [{', '.join(results)}]"

root = Composite("root")
root.add(Leaf("A"))
root.add(Leaf("B"))
child = Composite("child")
child.add(Leaf("C"))
root.add(child)
print(root.operation())
# Composite(root): [Leaf(A), Leaf(B), Composite(child): [Leaf(C)]]
```

## Q17: Explain the key participants in the Composite pattern.

**A:** The Composite pattern has three key participants: Component, Leaf, and Composite. Component is the interface (or abstract class) that declares the common operations for all objects in the composition. It defines the interface for both leaves and composites, enabling clients to treat them uniformly. Leaf represents leaf objects in the composition — objects that have no children. Leaf implements the Component interface and performs the actual work. Composite represents complex components that have children — other composites or leaves.

The Composite class maintains a list of children (other Component objects) and implements the Component interface by delegating operations to its children. The key insight is that Composite implements the same interface as Leaf, so a Composite can contain other Composites, creating a recursive tree structure. The Composite's operation typically iterates over its children and calls their operations, accumulating the results.

A design decision in the Composite pattern is whether to define child management methods (`add`, `remove`, `get_child`) in the Component interface or only in the Composite class. The GoF pattern recommends defining them only in Composite (the "safe" or "transparent" approach depends on the context). If you define them in Component, leaves must implement them (usually raising exceptions), which violates the Interface Segregation Principle. If you define them only in Composite, clients must know whether they are dealing with a Composite to manage children, which breaks transparency.

```python
from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def price(self):
        pass

    @abstractmethod
    def description(self):
        pass

class Product(Component):
    def __init__(self, name, price):
        self._name = name
        self._price = price

    def price(self):
        return self._price

    def description(self):
        return self._name

class Box(Component):
    def __init__(self, name):
        self._name = name
        self._items = []

    def add(self, item):
        self._items.append(item)

    def price(self):
        return sum(item.price() for item in self._items)

    def description(self):
        descs = [item.description() for item in self._items]
        return f"{self._name}: [{', '.join(descs)}]"

box = Box("Gift Box")
box.add(Product("Book", 29.99))
box.add(Product("Pen", 4.99))
print(box.price())        # 34.98
print(box.description())  # Gift Box: [Book, Pen]
```

## Q18: How do you implement a Composite pattern with a uniform interface for leaves and composites?

**A:** Implementing a uniform interface requires that both Leaf and Composite classes implement the same Component interface. The Component interface defines the operations that both types support. For operations that make sense only for Composites (like `add` and `remove`), you have two choices: define them in the Component interface (transparent approach) or only in Composite (safe approach). The transparent approach is simpler but forces Leaf to implement methods it does not use.

The transparent approach defines all operations in the Component interface. Leaf implementations of composite-specific methods typically raise `NotImplementedError` or do nothing. This allows clients to treat all objects uniformly without type checking, but it violates the Interface Segregation Principle because leaves are forced to implement methods they do not need.

The safe approach defines composite-specific methods only in the Composite class. Clients must check whether an object is a Composite before calling child management methods. This is safer because it prevents clients from calling `add` on leaves, but it requires type checking, which reduces the uniformity benefit. The choice depends on whether you prioritize transparency (transparent) or safety (safe). Most practical implementations use the safe approach with type checking only where needed.

```python
from abc import ABC, abstractmethod

class FileSystemComponent(ABC):
    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def display(self, indent=0):
        pass

class File(FileSystemComponent):
    def __init__(self, name, size):
        self.name = name
        self._size = size

    def size(self):
        return self._size

    def display(self, indent=0):
        return "  " * indent + f"File: {self.name} ({self._size}KB)"

class Directory(FileSystemComponent):
    def __init__(self, name):
        self.name = name
        self._children = []

    def add(self, component):
        self._children.append(component)

    def size(self):
        return sum(child.size() for child in self._children)

    def display(self, indent=0):
        result = "  " * indent + f"Dir: {self.name}/"
        for child in self._children:
            result += "\n" + child.display(indent + 1)
        return result

root = Directory("root")
root.add(File("readme.txt", 1))
subdir = Directory("src")
subdir.add(File("main.py", 5))
subdir.add(File("utils.py", 3))
root.add(subdir)
print(root.size())     # 9
print(root.display())  # Tree visualization
```

## Q19: What are the different traversal strategies for Composite trees?

**A:** Composite trees can be traversed using several strategies: depth-first search (DFS), breadth-first search (BFS), pre-order traversal, and post-order traversal. DFS visits the deepest nodes first, useful for operations that need to process children before parents. BFS visits nodes level by level, useful for operations that need to process parents before children. Pre-order processes the current node before its children, while post-order processes children before the current node.

The choice of traversal strategy depends on the operation being performed. For calculating aggregate values (like total price in a bill of materials), post-order traversal is natural — process all children first, then combine their results. For displaying a tree structure, pre-order traversal is natural — display the current node, then recurse into children. For searching for a specific node, BFS is often more efficient because it finds the shallowest match first.

Implementing traversal in a Composite requires either a recursive method in the Composite class (delegating to children) or an external iterator. The recursive approach is simpler but tightly couples the traversal to the Composite. The iterator approach is more flexible because it can be applied to different tree structures and can support different traversal strategies. Python's `__iter__` method can be implemented on Composite to support iteration over children.

```python
class Node:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []

    def dfs(self):
        """Depth-first: process node, then recurse into children."""
        result = [self.name]
        for child in self.children:
            result.extend(child.dfs())
        return result

    def bfs(self):
        """Breadth-first: process level by level."""
        result = []
        queue = [self]
        while queue:
            node = queue.pop(0)
            result.append(node.name)
            queue.extend(node.children)
        return result

    def post_order(self):
        """Post-order: process children first."""
        result = []
        for child in self.children:
            result.extend(child.post_order())
        result.append(self.name)
        return result

root = Node("root", [
    Node("A", [Node("A1"), Node("A2")]),
    Node("B", [Node("B1")])
])
print(root.dfs())       # ['root', 'A', 'A1', 'A2', 'B', 'B1']
print(root.bfs())       # ['root', 'A', 'B', 'A1', 'A2', 'B1']
print(root.post_order())  # ['A1', 'A2', 'A', 'B1', 'B', 'root']
```

## Q20: How do you handle cyclic references in Composite structures?

**A:** Cyclic references occur when a node in a Composite tree has a reference (direct or indirect) to one of its ancestors. This can cause infinite recursion during traversal, stack overflow, or incorrect aggregation results. The solution is to track visited nodes during traversal using a set, and to skip nodes that have already been visited. This prevents infinite loops and ensures that each node is processed exactly once.

The implementation adds a `visited` parameter (typically a set) to traversal methods. Before processing a node, the method checks if the node is in the `visited` set. If so, it skips the node. If not, it adds the node to `visited` and processes it. For recursive traversals, the `visited` set is passed as a parameter or stored on the Composite itself. For iterative traversals, the set is maintained in the loop.

A more fundamental solution is to prevent cyclic references at the data model level. This can be done by restricting the Composite to only allow adding children that are not ancestors (checking the tree structure before adding). Alternatively, use weak references (`weakref`) to break reference cycles and allow garbage collection. The choice depends on whether cycles are a legitimate part of the domain (in which case, handle them in traversal) or an error (in which case, prevent them at creation time).

```python
class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        # Prevent cycles by checking ancestry
        if self._is_ancestor(child):
            raise ValueError(f"Adding {child.name} would create a cycle")
        self.children.append(child)

    def _is_ancestor(self, node):
        if node is self:
            return True
        return any(child._is_ancestor(node) for child in self.children)

    def traverse(self, visited=None):
        if visited is None:
            visited = set()
        if id(self) in visited:
            return []
        visited.add(id(self))
        result = [self.name]
        for child in self.children:
            result.extend(child.traverse(visited))
        return result

a = Node("A")
b = Node("B")
c = Node("C")
a.add_child(b)
b.add_child(c)
# c.add_child(a)  # ValueError: Adding A would create a cycle
print(a.traverse())  # ['A', 'B', 'C']
```

## Q21: What is the difference between the Composite pattern and the Decorator pattern?

**A:** The Composite pattern and the Decorator pattern both involve object composition, but they serve different purposes. Composite represents part-whole hierarchies where individual objects and compositions are treated uniformly. Decorator adds behavior to objects by wrapping them in decorator objects. Composite is about structure (tree of objects), while Decorator is about behavior (enhancing objects).

The key structural difference is that Composite objects contain children (other Components), forming a tree. Decorator objects contain a single wrapped object (the Component they enhance). Composite's primary operation traverses the tree, while Decorator's primary operation delegates to the wrapped object. Composite is used when you need to treat individual and grouped objects the same way. Decorator is used when you need to add responsibilities to objects dynamically.

Another difference is in the relationship between the wrapper and the wrapped object. In Composite, the relationship is "contains" — a Composite contains Children. In Decorator, the relationship is "wraps" — a Decorator wraps a Component. Composite's children are typically of the same type as the Composite (implementing the same Component interface). Decorator's wrapped object is always of the same type as the Decorator (implementing the same Component interface). Despite this similarity, the intent is fundamentally different.

```python
# Composite — tree of objects
class MenuComponent:
    def price(self): pass

class MenuItem(MenuComponent):
    def __init__(self, name, price):
        self.name, self.price_val = name, price
    def price(self): return self.price_val

class MenuGroup(MenuComponent):
    def __init__(self, name):
        self.name, self.items = name, []
    def add(self, item): self.items.append(item)
    def price(self): return sum(i.price() for i in self.items)

# Decorator — wraps single object
class MenuDecorator(MenuComponent):
    def __init__(self, wrapped):
        self._wrapped = wrapped
    def price(self): return self._wrapped.price()

class DiscountDecorator(MenuDecorator):
    def __init__(self, wrapped, discount):
        super().__init__(wrapped)
        self.discount = discount
    def price(self): return self._wrapped.price() * (1 - self.discount)
```

## Q22: How do you implement the Composite pattern with an iterator for tree traversal?

**A:** Implementing an iterator for Composite tree traversal separates the traversal logic from the tree structure. The Composite class implements `__iter__` to return an iterator that yields all nodes in the tree. This allows clients to iterate over the tree using Python's standard `for` loop syntax without needing to know the tree's internal structure. The iterator can implement different traversal strategies (DFS, BFS, pre-order, post-order).

The simplest implementation uses a generator function for DFS traversal. The generator yields the current node and then recursively iterates over its children. For BFS, the generator uses a queue instead of recursion. The generator approach is memory-efficient because it yields one node at a time, avoiding the need to build a complete list of all nodes before iteration starts.

A more advanced implementation provides configurable traversal strategies. The Composite's `__iter__` method accepts a strategy parameter (or uses a default strategy) that determines the traversal order. This allows the same tree to be traversed in different orders for different operations. For example, a file system tree might be traversed in DFS order for size calculation and BFS order for display.

```python
class TreeNode:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []

    def __iter__(self):
        """DFS iterator using a generator."""
        yield self
        for child in self.children:
            yield from child

    def bfs_iter(self):
        """BFS iterator."""
        queue = [self]
        while queue:
            node = queue.pop(0)
            yield node
            queue.extend(node.children)

root = TreeNode("root", [
    TreeNode("A", [TreeNode("A1"), TreeNode("A2")]),
    TreeNode("B")
])

for node in root:
    print(node.name, end=" ")  # root A A1 A2 B

print()
for node in root.bfs_iter():
    print(node.name, end=" ")  # root A B A1 A2
```

## Q23: What are the trade-offs between the transparent and safe approaches in the Composite pattern?

**A:** The transparent approach defines all operations (including child management) in the Component interface. Leaf classes must implement child management methods, typically raising `NotImplementedError`. The benefit is complete transparency — clients never need to check whether an object is a Leaf or Composite. The drawback is that it violates the Interface Segregation Principle because Leaf classes implement methods they cannot use, and clients might accidentally call `add` on a Leaf.

The safe approach defines child management methods only in the Composite class. Leaves do not implement these methods, so they cannot be accidentally called on Leaves. The drawback is that clients must check whether an object is a Composite before calling child management methods, which breaks the uniform interface benefit. This requires either type checking (`isinstance(obj, Composite)`) or using the visitor pattern to handle different types.

In practice, the safe approach is more common because it prevents bugs at the cost of some type checking. The transparent approach is used when the operation set is small and well-defined, and when the risk of calling invalid methods is low. Python's duck typing makes the transparent approach more natural because there is no compile-time type checking to catch errors. The choice also depends on the domain: if leaves genuinely cannot have children (like files in a file system), the transparent approach's empty implementations are harmless.

```python
# Safe approach — child management only in Composite
class Component:
    def operation(self): pass

class Leaf(Component):
    def __init__(self, name):
        self.name = name
    def operation(self):
        return f"Leaf({self.name})"

class Composite(Component):
    def __init__(self, name):
        self.name, self._children = name, []
    def add(self, child):
        self._children.append(child)
    def operation(self):
        results = [c.operation() for c in self._children]
        return f"Composite({self.name}): {results}"

def process(component):
    result = component.operation()
    # Only access children if it's a Composite
    if isinstance(component, Composite):
        for child in component._children:
            result += " " + process(child)
    return result
```

## Q24: How do you implement the Composite pattern with a visitor for separating traversal from operation?

**A:** Combining Composite with Visitor separates the tree structure from the operations performed on it. The Visitor interface defines a `visit` method for each type of node (Leaf and Composite). Each node's `accept` method calls the appropriate `visit` method on the visitor. This allows you to add new operations without modifying the node classes, which is useful when the tree structure is stable but operations change frequently.

The implementation requires each node class to have an `accept(visitor)` method that calls `visitor.visit_leaf(self)` or `visitor.visit_composite(self)` depending on the node type. The visitor implements these methods to perform the operation on each type of node. For Composite nodes, the visitor must also iterate over children and call `accept` on each child, which requires the visitor to have access to the Composite's children.

The trade-off is that adding new node types requires modifying the Visitor interface and all existing visitor implementations, which violates the Open-Closed Principle for visitors. However, adding new operations only requires creating a new visitor, which follows OCP. This pattern is useful when the tree structure is fixed (like a compiler's AST) but operations change (like different code generation targets).

```python
from abc import ABC, abstractmethod

class Visitable(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class Element(Visitable):
    def __init__(self, name):
        self.name = name
    def accept(self, visitor):
        return visitor.visit_element(self)

class Group(Visitable):
    def __init__(self, name):
        self.name, self.children = name, []
    def add(self, child):
        self.children.append(child)
    def accept(self, visitor):
        return visitor.visit_group(self)

class Visitor(ABC):
    @abstractmethod
    def visit_element(self, elem): pass
    @abstractmethod
    def visit_group(self, group): pass

class PricingVisitor(Visitor):
    def visit_element(self, elem):
        return elem.price
    def visit_group(self, group):
        return sum(child.accept(self) for child in group.children)

class DisplayVisitor(Visitor):
    def visit_element(self, elem):
        return f"  {elem.name}"
    def visit_group(self, group):
        items = "\n".join(child.accept(self) for child in group.children)
        return f"{group.name}:\n{items}"
```

## Q25: What are the real-world applications of the Composite pattern?

**A:** The Composite pattern is used in numerous real-world systems. File systems use it to represent files and directories, where directories contain files and other directories. GUI frameworks use it for widget hierarchies, where containers hold widgets and other containers. Document processing systems use it for document structures, where sections contain paragraphs, images, and tables. Organizational charts use it for employee hierarchies, where managers have reports who may also be managers.

In Python, the Composite pattern appears in the `ast` module (Abstract Syntax Tree), where nodes represent different syntactic constructs and can contain child nodes. The `tkinter` and `PyQt` GUI frameworks use Composite for widget hierarchies. The `os.walk()` function traverses a Composite-like file system structure. The `json` and `xml` libraries parse data into Composite tree structures.

The pattern is also used in game development (scene graphs where entities contain child entities), network protocols (packet structures where packets contain sub-packets), and build systems (dependency trees where targets depend on other targets). The key characteristic of all these applications is the part-whole hierarchy where operations need to be performed on both individual items and groups of items.

```python
# Real-world example: Building system (dependency tree)
class BuildTarget:
    def build(self): pass

class FileTarget(BuildTarget):
    def __init__(self, name):
        self.name = name
    def build(self):
        print(f"  Building file: {self.name}")

class GroupTarget(BuildTarget):
    def __init__(self, name):
        self.name, self.targets = name, []
    def add(self, target):
        self.targets.append(target)
    def build(self):
        print(f"Building group: {self.name}")
        for target in self.targets:
            target.build()

# Build system like Make/CMake
all_targets = GroupTarget("all")
src = GroupTarget("src")
src.add(FileTarget("main.c"))
src.add(FileTarget("utils.c"))
tests = GroupTarget("tests")
tests.add(FileTarget("test_main.c"))
all_targets.add(src)
all_targets.add(tests)
all_targets.build()
```

## Q26: What is the Bridge pattern and what problem does it solve?

**A:** The Bridge pattern is a structural design pattern that separates an abstraction from its implementation so that both can vary independently. It solves the problem of combinatorial class explosion that occurs when you have multiple dimensions of variation. For example, if you have shapes (circle, square, triangle) that can be rendered in different ways (vector, raster, SVG), inheritance would require a class for every combination (VectorCircle, RasterCircle, SVGCircle, etc.). Bridge eliminates this by splitting the hierarchy into two independent axes: abstraction and implementation.

The core problem Bridge addresses is the tight coupling between an abstraction and its implementation. When you use inheritance to combine an abstraction with an implementation, adding a new implementation (e.g., OpenGL rendering) requires creating new subclasses for every abstraction (OpenGLCircle, OpenGLSquare, etc.). With Bridge, adding a new implementation only requires creating one new class that implements the implementation interface. The abstraction hierarchy remains unchanged.

Bridge achieves this through composition: the abstraction holds a reference to an implementation object, and delegates work to it. The abstraction defines high-level logic, while the implementation provides low-level details. Both hierarchies can be extended independently, and implementations can be swapped at runtime. This is the same principle as "favor composition over inheritance," applied to the problem of multi-dimensional variation.

```python
from abc import ABC, abstractmethod

class Implementation(ABC):
    @abstractmethod
    def draw_circle(self, x, y, radius):
        pass

class VectorImplementation(Implementation):
    def draw_circle(self, x, y, radius):
        print(f"Drawing vector circle at ({x},{y}) r={radius}")

class RasterImplementation(Implementation):
    def draw_circle(self, x, y, radius):
        print(f"Drawing raster circle at ({x},{y}) r={radius}")

class Shape(ABC):
    def __init__(self, impl):
        self._impl = impl

    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def __init__(self, impl, x, y, radius):
        super().__init__(impl)
        self.x, self.y, self.radius = x, y, radius

    def draw(self):
        self._impl.draw_circle(self.x, self.y, self.radius)

# Bridge: abstraction (Circle) is decoupled from implementation (Vector/Raster)
circle = Circle(VectorImplementation(), 10, 20, 5)
circle.draw()  # Drawing vector circle at (10,20) r=5
circle._impl = RasterImplementation()
circle.draw()  # Drawing raster circle at (10,20) r=5
```

## Q27: Explain the key participants in the Bridge pattern.

**A:** The Bridge pattern has four key participants: Abstraction, RefinedAbstraction, Implementor, and ConcreteImplementor. Abstraction is the high-level interface that defines the abstraction's operations. It holds a reference to an Implementor object and delegates low-level operations to it. RefinedAbstraction extends the Abstraction with additional operations that use the Implementor. Implementor is the interface for implementation classes. ConcreteImplementor implements the Implementor interface, providing concrete implementations of the low-level operations.

The Abstraction is not an abstract class in the traditional sense — it is a class that defines high-level business logic and delegates low-level work to the Implementor. The Abstraction may define abstract methods that RefinedAbstraction must implement, or it may provide default implementations. The key is that the Abstraction does not know the details of the Implementor — it only knows the Implementor interface.

The Implementor hierarchy is separate from the Abstraction hierarchy. Implementors are typically more granular than Abstractions — a single Implementor can be used by multiple Abstractions. This is different from the Adapter pattern, where the adapter wraps a specific implementation. In Bridge, the Implementor is a strategy for performing low-level operations, and the Abstraction is a strategy for composing those operations into high-level behavior. The two hierarchies can be extended independently.

```python
from abc import ABC, abstractmethod

class Abstraction:
    def __init__(self, impl):
        self._impl = impl

    def operation(self):
        return f"Abstraction: {self._impl.operation_implementation()}"

class RefinedAbstraction(Abstraction):
    def extended_operation(self):
        return f"Refined: {self._impl.operation_implementation()} + extra"

class Implementor(ABC):
    @abstractmethod
    def operation_implementation(self):
        pass

class ConcreteImplementorA(Implementor):
    def operation_implementation(self):
        return "Implementor A"

class ConcreteImplementorB(Implementor):
    def operation_implementation(self):
        return "Implementor B"

a1 = RefinedAbstraction(ConcreteImplementorA())
a2 = RefinedAbstraction(ConcreteImplementorB())
print(a1.operation())         # Abstraction: Implementor A
print(a2.extended_operation())  # Refined: Implementor B + extra
```

## Q28: How do you implement the Bridge pattern with multiple implementation hierarchies?

**A:** The Bridge pattern supports multiple implementation hierarchies by having the Abstraction hold references to multiple Implementors. For example, a shape might need both a rendering implementation (Vector/Raster) and a persistence implementation (JSON/Database). The Abstraction delegates rendering to one Implementor and persistence to another, allowing both dimensions to vary independently.

The implementation requires the Abstraction to hold references to multiple Implementor objects, typically as named attributes (e.g., `self._renderer` and `self._serializer`). Each Implementor hierarchy is independent and can be extended without affecting the others. The Abstraction's methods combine operations from multiple Implementors to provide high-level functionality.

This is a common extension of the basic Bridge pattern in real-world applications. A UI framework might have Abstractions (Button, TextBox) that use a rendering Implementor (Windows/Mac/Linux) and a data binding Implementor (Direct/Reactive). A network application might have Abstractions (Client, Server) that use a protocol Implementor (TCP/UDP) and a serialization Implementor (JSON/Protobuf). The key benefit is that adding a new protocol or serialization format does not require changing the Client or Server classes.

```python
from abc import ABC, abstractmethod

class Renderer(ABC):
    @abstractmethod
    def render(self, shape): pass

class SVGRenderer(Renderer):
    def render(self, shape):
        return f"<svg>{shape.name}</svg>"

class CanvasRenderer(Renderer):
    def render(self, shape):
        return f"Canvas({shape.name})"

class Serializer(ABC):
    @abstractmethod
    def serialize(self, data): pass

class JSONSerializer(Serializer):
    def serialize(self, data):
        return f'{{"data": {data}}}'

class PickleSerializer(Serializer):
    def serialize(self, data):
        return f"PICKLE({data})"

class Shape:
    def __init__(self, renderer, serializer):
        self._renderer = renderer
        self._serializer = serializer

    def draw_and_save(self, name, data):
        rendered = self._renderer.render(self)
        saved = self._serializer.serialize(data)
        return f"{rendered} -> {saved}"

s = Shape(SVGRenderer(), JSONSerializer())
print(s.draw_and_save("circle", 42))
# <svg>circle</svg> -> {"data": 42}
```

## Q29: What is the difference between the Bridge pattern and the Adapter pattern?

**A:** The Bridge pattern and the Adapter pattern both connect two interfaces, but they serve different purposes. Bridge is designed upfront to decouple an abstraction from its implementation, allowing both to vary independently. Adapter is designed after the fact to make incompatible interfaces work together. Bridge is a design-time decision; Adapter is a compatibility fix.

The key distinction is intent. Bridge separates an abstraction from its implementation so that they can be extended independently. The two interfaces are designed to work together from the start. Adapter makes an existing interface usable by another interface. The two interfaces were not designed to work together and need a translator. Bridge is about structural decoupling; Adapter is about interface compatibility.

In practice, the patterns look similar but have different lifecycle implications. Bridge's implementation can be swapped at runtime because the abstraction is designed to work with any implementation. Adapter's wrapped object is typically fixed at creation time because the adapter is designed to make a specific incompatible interface work. Bridge implies a permanent architectural decision; Adapter implies a temporary compatibility fix.

```python
# Bridge — designed to work together
class Abstraction:
    def __init__(self, impl):
        self._impl = impl
    def operation(self):
        return self._impl.operation()

# Adapter — makes incompatible interface work
class OldSystem:
    def legacy_operation(self):
        return "old system result"

class Adapter:
    def __init__(self, old_system):
        self._old = old_system
    def operation(self):
        return self._old.legacy_operation()  # Translate

# Bridge: abstraction and implementation are designed together
# Adapter: adapter translates between incompatible interfaces
```

## Q30: How does the Bridge pattern relate to the Strategy pattern?

**A:** The Bridge pattern and the Strategy pattern are structurally similar — both use composition to delegate work to a separate object. The key difference is intent. Bridge is a structural pattern that separates an abstraction from its implementation to allow independent variation. Strategy is a behavioral pattern that encapsulates algorithms and makes them interchangeable. Bridge is about structural separation; Strategy is about algorithmic flexibility.

The structural similarity is that both patterns have a context object that holds a reference to a delegate object. In Bridge, the context is the Abstraction and the delegate is the Implementor. In Strategy, the context is the class that uses the strategy and the delegate is the Strategy. Both patterns allow swapping the delegate at runtime. Both patterns reduce coupling between the context and the delegate.

The intent difference manifests in the interface design. Bridge's Implementor interface typically has low-level, granular operations that the Abstraction composes into high-level behavior. Strategy's interface has high-level, complete operations that the context delegates to entirely. Bridge is used when you have multiple dimensions of variation (e.g., shape × renderer). Strategy is used when you have multiple algorithms for the same task (e.g., sorting × performance characteristics).

```python
# Bridge — separates abstraction from implementation
class Abstraction:
    def __init__(self, impl):
        self._impl = impl
    def high_level_operation(self):
        return f"Do something, then {self._impl.low_level()}"

# Strategy — encapsulates interchangeable algorithms
class Context:
    def __init__(self, strategy):
        self._strategy = strategy
    def execute(self, data):
        return self._strategy.algorithm(data)

# Both use composition, but Bridge is about structure, Strategy is about algorithms
```

## Q31: How do you implement the Bridge pattern with abstract factories?

**A:** Combining Bridge with Abstract Factory creates a system where the factory produces both Abstractions and Implementors, ensuring that compatible pairs are created together. The Abstract Factory provides a creational mechanism for the Bridge's components, ensuring that the Abstraction and Implementor hierarchies are used consistently. This is useful when the system must support multiple families of related objects (e.g., cross-platform UI where each platform provides its own widgets and renderers).

The factory interface defines methods for creating both Abstraction and Implementor objects. Each concrete factory creates a compatible set of objects. For example, a WindowsFactory creates WindowsButton and WindowsRenderer, while a MacFactory creates MacButton and MacRenderer. The client uses the factory to create objects, ensuring that the Abstraction and Implementor are from the same family.

This combination is powerful because it eliminates the risk of mixing incompatible implementations with abstractions. The factory guarantees that the objects it creates work together. It also encapsulates the creation logic, making it easy to add new families (new platforms) without changing client code. This follows the Open-Closed Principle and the Dependency Inversion Principle.

```python
from abc import ABC, abstractmethod

class Renderer(ABC):
    @abstractmethod
    def render(self, text): pass

class WindowsRenderer(Renderer):
    def render(self, text): return f"Win: {text}"

class MacRenderer(Renderer):
    def render(self, text): return f"Mac: {text}"

class Widget:
    def __init__(self, renderer):
        self._renderer = renderer

class Button(Widget):
    def draw(self, label):
        return self._renderer.render(f"Button({label})")

class GUIFactory(ABC):
    @abstractmethod
    def create_button(self): pass

class WindowsFactory(GUIFactory):
    def create_button(self):
        return Button(WindowsRenderer())

class MacFactory(GUIFactory):
    def create_button(self):
        return Button(MacRenderer())

def build_ui(factory):
    btn = factory.create_button()
    return btn.draw("OK")

print(build_ui(WindowsFactory()))  # Win: Button(OK)
print(build_ui(MacFactory()))      # Mac: Button(OK)
```

## Q32: What are the real-world applications of the Bridge pattern?

**A:** The Bridge pattern is used in numerous real-world systems where abstraction and implementation must vary independently. Database drivers use Bridge to separate the database abstraction (Connection, Query) from the implementation (MySQL, PostgreSQL, SQLite). Rendering engines use Bridge to separate the shape abstraction (Circle, Rectangle) from the rendering implementation (OpenGL, DirectX, Vulkan). Device drivers use Bridge to separate the device abstraction (Printer, Scanner) from the platform implementation (Windows, Linux, macOS).

In Python, the `abc` module uses Bridge-like patterns to separate abstract interfaces from concrete implementations. The `logging` module separates the Logger abstraction from Handler implementations (FileHandler, StreamHandler, SysLogHandler). The `csv` module separates the reader abstraction from the dialect implementation (Excel, Unix, Sniffed). These examples show how Bridge is used to create flexible, extensible systems where new implementations can be added without changing the abstraction.

Other applications include payment processing (Payment abstraction × Gateway implementation), notification systems (Notification abstraction × Channel implementation), and storage systems (Storage abstraction × Backend implementation). In each case, the abstraction defines the high-level interface, and the implementation provides the low-level details. The two hierarchies can be extended independently, and implementations can be swapped at runtime.

```python
# Real-world example: Payment processing bridge
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount): pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        return f"Charging ${amount} to credit card"

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        return f"Sending ${amount} via PayPal"

class PaymentNotification:
    def __init__(self, processor):
        self._processor = processor

    def checkout(self, amount, email):
        result = self._processor.process_payment(amount)
        return f"Payment: {result}, receipt sent to {email}"

# Bridge: notification logic is separate from payment gateway
cc = PaymentNotification(CreditCardProcessor())
pp = PaymentNotification(PayPalProcessor())
print(cc.checkout(99.99, "user@email.com"))
print(pp.checkout(49.99, "user@email.com"))
```

## Q33: How do you handle implementation switching at runtime in the Bridge pattern?

**A:** Switching implementations at runtime is a key benefit of the Bridge pattern. Since the Abstraction holds a reference to the Implementor through an interface, you can swap the Implementor at any time by reassigning the reference. This allows the same Abstraction object to use different implementations during its lifetime, enabling dynamic behavior changes without creating new objects.

The implementation is straightforward: the Abstraction exposes a method (or the reference is public) that allows the Implementor to be changed. For example, a Shape object might switch from VectorRenderer to RasterRenderer at runtime. The next time `draw()` is called, it uses the new implementation. This is useful for scenarios like switching between online and offline modes, changing compression algorithms, or adapting to different network conditions.

A more sophisticated approach uses a factory or registry to look up implementations by name. The Abstraction's method accepts an implementation name (e.g., "vector", "raster") and looks up the corresponding Implementor class from a registry. This eliminates the need to import specific Implementor classes and makes the system more extensible. New implementations can be registered at runtime without modifying the Abstraction.

```python
class Renderer:
    def render(self, shape): return "base"

class VectorRenderer(Renderer):
    def render(self, shape): return f"Vector({shape})"

class RasterRenderer(Renderer):
    def render(self, shape): return f"Raster({shape})"

class Shape:
    def __init__(self, name, renderer):
        self.name, self._renderer = name, renderer

    def set_renderer(self, renderer):
        self._renderer = renderer

    def draw(self):
        return self._renderer.render(self.name)

s = Shape("Circle", VectorRenderer())
print(s.draw())  # Vector(Circle)
s.set_renderer(RasterRenderer())
print(s.draw())  # Raster(Circle)
```

## Q34: What is the difference between the Bridge pattern and the Decorator pattern?

**A:** The Bridge pattern and the Decorator pattern both use composition to delegate work to other objects, but they serve different purposes. Bridge separates an abstraction from its implementation to allow independent variation. Decorator adds responsibilities to objects dynamically. Bridge is about structural separation (two hierarchies that vary independently). Decorator is about behavioral extension (adding features to existing objects).

The key structural difference is that Bridge's Abstraction holds a single Implementor reference that provides the implementation. Decorator holds a reference to the wrapped object and adds behavior around it. Bridge's implementation is the core behavior; Decorator's implementation is the added behavior. Bridge is used at design time to separate concerns; Decorator is used at runtime to add concerns.

Another difference is in the relationship between the wrapper and the wrapped object. In Bridge, the Abstraction and Implementor are designed to work together — they are two halves of the same functionality. In Decorator, the Decorator enhances the wrapped object — the Decorator adds value beyond what the wrapped object provides. Bridge is about decomposition (splitting a complex thing into two simpler things); Decorator is about composition (combining simple things into a complex thing).

```python
# Bridge — separation of concerns
class Abstraction:
    def __init__(self, impl):
        self._impl = impl  # Implementation is the core behavior
    def operation(self):
        return self._impl.do_work()

# Decorator — adding responsibilities
class Decorator:
    def __init__(self, wrapped):
        self._wrapped = wrapped  # Wrapped object is the core behavior
    def operation(self):
        return self._wrapped.operation() + " + extra"
```

## Q35: How do you implement a Bridge pattern for cross-platform application development?

**A:** Cross-platform application development is a classic use case for the Bridge pattern. The Abstraction defines the application's UI components (Button, TextBox, Dialog), and the Implementor provides platform-specific rendering (Windows, macOS, Linux). The same application logic works across platforms by delegating rendering to the platform-specific implementation. This eliminates the need to rewrite the entire application for each platform.

The implementation typically defines an Abstraction hierarchy for UI components and an Implementor hierarchy for platform APIs. Each UI component (Button, TextBox) holds a reference to a platform renderer. The renderer provides low-level drawing operations (drawRectangle, drawText, drawCircle). Platform-specific renderers implement these operations using the platform's native drawing APIs.

The benefit is that the application logic (Abstraction) is written once and works on all platforms. Adding a new platform only requires implementing a new Renderer. Adding a new UI component only requires creating a new Abstraction class. The two hierarchies are completely independent, which is exactly what Bridge is designed for. This pattern is used by cross-platform frameworks like Qt, GTK, and Flutter.

```python
from abc import ABC, abstractmethod

class PlatformRenderer(ABC):
    @abstractmethod
    def draw_button(self, label): pass
    @abstractmethod
    def draw_textbox(self, text): pass

class WindowsRenderer(PlatformRenderer):
    def draw_button(self, label):
        return f"[Win Button: {label}]"
    def draw_textbox(self, text):
        return f"[Win TextBox: {text}]"

class LinuxRenderer(PlatformRenderer):
    def draw_button(self, label):
        return f"(Linux Button: {label})"
    def draw_textbox(self, text):
        return f"(Linux TextBox: {text})"

class UIButton:
    def __init__(self, renderer, label):
        self._renderer = renderer
        self._label = label
    def render(self):
        return self._renderer.draw_button(self._label)

class UITextBox:
    def __init__(self, renderer, text):
        self._renderer = renderer
        self._text = text
    def render(self):
        return self._renderer.draw_textbox(self._text)

win_btn = UIButton(WindowsRenderer(), "OK")
linux_btn = UIButton(LinuxRenderer(), "OK")
print(win_btn.render())   # [Win Button: OK]
print(linux_btn.render()) # (Linux Button: OK)
```

## Q36: How do you combine the Decorator and Composite patterns?

**A:** Combining Decorator and Composite creates a system where composite tree nodes can be decorated with additional behavior. This is useful when you need both the part-whole hierarchy of Composite and the dynamic behavior extension of Decorator. For example, a file system tree (Composite) might have nodes that are decorated with caching, compression, or encryption (Decorator).

The implementation requires that the Decorator implements the same Component interface as the Composite. The Decorator wraps a Component (which can be a Leaf, a Composite, or another Decorator) and adds behavior. The Composite contains Decorated Components, so the entire tree benefits from the decorator's behavior. This is more flexible than applying decorators only at the leaves, because the decorator's behavior applies to the entire subtree.

A practical example is a document processing system where the document is a Composite tree of paragraphs, images, and tables. Each node can be decorated with formatting (bold, italic, underline), localization (translation), or accessibility (alt text). The decorations are applied dynamically based on the output format (HTML, PDF, plain text). This combination provides both structural flexibility (Composite) and behavioral flexibility (Decorator).

```python
from abc import ABC, abstractmethod

class DocumentComponent(ABC):
    @abstractmethod
    def render(self):
        pass

class TextNode(DocumentComponent):
    def __init__(self, text):
        self.text = text
    def render(self):
        return self.text

class Section(DocumentComponent):
    def __init__(self, title):
        self.title = title
        self._children = []
    def add(self, child):
        self._children.append(child)
    def render(self):
        content = " ".join(c.render() for c in self._children)
        return f"<h1>{self.title}</h1> {content}"

class BoldDecorator(DocumentComponent):
    def __init__(self, wrapped):
        self._wrapped = wrapped
    def render(self):
        return f"<b>{self._wrapped.render()}</b>"

doc = Section("Introduction")
doc.add(TextNode("Hello world"))
decorated = BoldDecorator(TextNode("Important"))
doc.add(decorated)
print(doc.render())
# <h1>Introduction</h1> Hello world <b>Important</b>
```

## Q37: What is the difference between the Composite pattern and the Chain of Responsibility pattern?

**A:** The Composite pattern and the Chain of Responsibility pattern both involve traversing a sequence of objects, but they serve different purposes. Composite represents a tree structure where each node can have children, and operations are performed on the entire tree. Chain of Responsibility passes a request along a chain of handlers, where each handler decides whether to handle the request or pass it on. Composite is about structure (tree); Chain of Responsibility is about request handling (chain).

The key structural difference is that Composite's children are organized in a tree (each node can have multiple children), while Chain of Responsibility's handlers are organized in a chain (each handler has one successor). Composite's operation is typically performed on the entire tree (aggregate results from all nodes). Chain of Responsibility's operation stops when a handler processes the request (only one handler processes the request).

Another difference is in the purpose of the traversal. Composite traverses the tree to aggregate results from all nodes (e.g., calculating the total price of a bill of materials). Chain of Responsibility traverses the chain to find a handler that can process the request (e.g., finding a logger that handles a specific log level). Composite is about aggregation; Chain of Responsibility is about dispatching.

```python
# Composite — tree structure, aggregate results
class Composite:
    def __init__(self, name):
        self.name, self.children = name, []
    def add(self, child): self.children.append(child)
    def operation(self):
        return sum(c.operation() for c in self.children)

# Chain of Responsibility — linear chain, find handler
class Handler:
    def __init__(self):
        self._next = None
    def set_next(self, handler):
        self._next = handler
        return handler
    def handle(self, request):
        if self._next:
            return self._next.handle(request)
        return None
```

## Q38: How do you implement the Composite pattern with a proxy for lazy loading?

**A:** Combining Composite with Proxy creates a system where composite nodes load their children lazily — only when accessed. This is useful for large tree structures where loading the entire tree upfront is expensive (e.g., file systems, database schemas, organizational charts). The Proxy node stands in for the real Composite and loads the children on first access.

The implementation uses a Virtual Proxy that implements the same interface as the Composite. The Proxy holds a loader function (or data source) and loads the real Composite on first access. Subsequent accesses use the cached Composite. This is similar to the lazy loading pattern but applied to Composite trees. The Proxy can load the entire subtree or just the immediate children, depending on the use case.

The benefit is that large trees can be represented without loading all nodes into memory. For example, a file system tree can be represented with Proxy nodes that load directory contents on demand. A database schema can be represented with Proxy nodes that query the database only when the user expands a node. This provides a responsive user experience while minimizing resource usage.

```python
class CompositeProxy:
    def __init__(self, name, loader):
        self.name = name
        self._loader = loader
        self._real_composite = None

    def _load(self):
        if self._real_composite is None:
            self._real_composite = self._loader()
        return self._real_composite

    def render(self, indent=0):
        return self._load().render(indent)

    def children(self):
        return self._load().children()

class Composite:
    def __init__(self, name):
        self.name, self._children = name, []
    def add(self, child): self._children.append(child)
    def children(self): return self._children
    def render(self, indent=0):
        result = "  " * indent + self.name
        for child in self._children:
            result += "\n" + child.render(indent + 1)
        return result

def lazy_load_dir(path):
    print(f"Loading {path}...")
    c = Composite(path)
    c.add(Composite("file1.txt"))
    c.add(Composite("file2.txt"))
    return c

root = CompositeProxy("/root", lambda: lazy_load_dir("/root"))
print("Before access")
print(root.render())  # Loads on first access
print("After access")
print(root.render())  # Uses cached version
```

## Q39: How do you test Composite structures effectively?

**A:** Testing Composite structures requires testing both individual leaves and composite operations. The key challenge is that Composite operations depend on children, so tests must set up realistic tree structures. The recommended approach is to use test fixtures that build representative trees, test individual node operations, test composite aggregation, and test traversal strategies.

For individual leaves, test that they return correct values for their operations. For composites, test that they correctly aggregate results from children. For traversal, test that all nodes are visited in the expected order. For edge cases, test empty composites (no children), single-child composites, deeply nested composites, and composites with mixed leaf and composite children.

Mock objects are useful for testing Composite structures because they allow you to control the behavior of individual nodes. You can mock a Leaf to return a specific value and verify that the Composite correctly aggregates it. You can mock a Composite to verify that the correct traversal order is used. The key is to test the Composite's behavior independently of its children's behavior.

```python
import unittest

class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []
    def add(self, child): self.children.append(child)
    def total(self):
        return self.value + sum(c.total() for c in self.children)

class TestComposite(unittest.TestCase):
    def setUp(self):
        self.leaf = Node(10)
        self.composite = Node(5)
        self.composite.add(Node(3))
        self.composite.add(Node(7))

    def test_leaf_total(self):
        self.assertEqual(self.leaf.total(), 10)

    def test_composite_total(self):
        self.assertEqual(self.composite.total(), 15)  # 5 + 3 + 7

    def test_nested_composite(self):
        root = Node(1)
        root.add(self.composite)
        self.assertEqual(root.total(), 16)  # 1 + 15

    def test_empty_composite(self):
        empty = Node(0)
        self.assertEqual(empty.total(), 0)

if __name__ == "__main__":
    unittest.main()
```

## Q40: What are the common pitfalls when implementing the Composite pattern?

**A:** Common pitfalls include: (1) defining child management methods in the Component interface (violates Interface Segregation Principle), (2) not handling the case where `add` or `remove` is called on a Leaf (should raise an appropriate exception), (3) creating cycles in the tree (a node is its own ancestor), (4) not implementing proper equality comparison for tree nodes (identity vs. value equality), (5) using deep recursion for traversal (risk of stack overflow for deep trees), and (6) not providing a way to flatten or serialize the tree for debugging.

The cycle issue is particularly dangerous because it can cause infinite recursion during traversal. The solution is to check for cycles before adding a child (verify that the child is not an ancestor of the current node) or to use a visited set during traversal. The recursion depth issue can be mitigated by using iterative traversal (BFS or explicit stack) instead of recursive traversal.

Another pitfall is assuming that all operations make sense for both leaves and composites. For example, `size()` might return the number of items in a composite but the size of a leaf. The semantics should be consistent and clearly documented. If an operation does not make sense for a leaf (like `add`), it should raise `NotImplementedError` or be excluded from the Component interface.

```python
class SafeNode:
    def __init__(self, name):
        self.name, self._children = name, []

    def add(self, child):
        if child is self:
            raise ValueError("Cannot add self as child")
        if self._is_descendant(child):
            raise ValueError("Would create cycle")
        self._children.append(child)

    def _is_descendant(self, node):
        for child in self._children:
            if child is node or child._is_descendant(node):
                return True
        return False

    def depth(self):
        if not self._children:
            return 0
        return 1 + max(c.depth() for c in self._children)

root = SafeNode("root")
a = SafeNode("A")
b = SafeNode("B")
root.add(a)
a.add(b)
# root.add(b)  # ValueError: Would create cycle
print(root.depth())  # 2
```

## Q41: How do you implement the Composite pattern with an observer for change notification?

**A:** Combining Composite with Observer creates a system where changes to any node in the tree are notified to registered observers. This is useful for UI frameworks where changing a node's state should trigger a redraw, or for data models where changes should trigger validation or persistence. The observer is notified of the change and can perform appropriate actions.

The implementation adds observer management methods (`add_observer`, `remove_observer`) to the Component interface. When a node's state changes, it notifies all registered observers. For Composite nodes, the notification can propagate to children (so observers can monitor entire subtrees) or be limited to the specific node that changed. The observer receives information about which node changed and what the change was.

A practical example is a file system monitor where the Composite tree represents the directory structure. When a file is created, modified, or deleted, the corresponding node notifies observers. Observers can update the UI, trigger backups, or log the change. The notification propagates up the tree so that parent directories are also notified of changes in their children.

```python
class ObservableNode:
    def __init__(self, name):
        self.name = name
        self._children, self._observers = [], []

    def add(self, child):
        self._children.append(child)
        self._notify("added", child)

    def add_observer(self, observer):
        self._observers.append(observer)

    def _notify(self, event, node):
        for obs in self._observers:
            obs(event, self, node)
        # Propagate to parent if needed

    def set_value(self, value):
        self._value = value
        self._notify("changed", self)

class LoggingObserver:
    def __call__(self, event, source, node):
        print(f"[LOG] {event} on {source.name}: {node.name}")

root = ObservableNode("root")
root.add_observer(LoggingObserver())
a = ObservableNode("A")
root.add(a)
# [LOG] added on root: A
```

## Q42: How do you implement a Composite pattern with caching for performance?

**A:** Caching in Composite structures can significantly improve performance for operations that are called repeatedly. The cache can be applied at different levels: leaf-level caching (cache the result of individual leaves), composite-level caching (cache the aggregated result), or subtree caching (cache the result of an entire subtree). The choice depends on how frequently values change and how expensive computation is.

Leaf-level caching stores the result of the leaf's operation and returns it on subsequent calls. This is useful when the leaf's value is expensive to compute but does not change often. Composite-level caching stores the aggregated result from children and invalidates it when any child changes. This is useful when the composite's operation is expensive and children rarely change.

Cache invalidation is the key challenge. When a leaf changes, all parent composites must invalidate their caches. This requires a notification mechanism (like Observer) or a dirty flag that propagates up the tree. The implementation can use `functools.lru_cache` for simple cases or a custom cache with invalidation logic for more complex scenarios.

```python
class CachedNode:
    def __init__(self, value):
        self._value = value
        self._cached_total = None
        self._dirty = True
        self._children = []

    def add(self, child):
        self._children.append(child)
        self._dirty = True

    def set_value(self, value):
        self._value = value
        self._dirty = True

    def total(self):
        if self._dirty or self._cached_total is None:
            self._cached_total = self._value + sum(c.total() for c in self._children)
            self._dirty = False
        return self._cached_total

root = CachedNode(1)
root.add(CachedNode(2))
root.add(CachedNode(3))
print(root.total())  # 6 — computed and cached
print(root.total())  # 6 — served from cache
root.set_value(10)
print(root.total())  # 15 — recomputed after invalidation
```

## Q43: How do you implement a Composite pattern with serialization for persistence?

**A:** Serializing Composite structures requires handling the recursive tree structure. The serialization must capture the node type (Leaf or Composite), the node's data, and the children (for Composites). JSON and XML are natural formats for tree structures because they support nesting. Binary formats require explicit tree encoding (e.g., length-prefixed nodes).

The implementation typically uses a recursive serialization function that handles each node type. For Leaves, serialize the value. For Composites, serialize the value and recursively serialize all children. Deserialization reverses the process: read the node type, create the appropriate object, and recursively deserialize children.

A key consideration is handling object references. If the same object appears in multiple places in the tree (shared children), serialization must handle reference identity to avoid duplicating the object. This requires a reference tracking mechanism (like `pickle`'s memo) or using IDs to represent references. For simple trees without shared children, recursive serialization is sufficient.

```python
import json

class TreeNode:
    def __init__(self, name, value=None, children=None):
        self.name, self.value = name, value
        self.children = children or []

    def to_dict(self):
        d = {"name": self.name, "value": self.value}
        if self.children:
            d["children"] = [c.to_dict() for c in self.children]
        return d

    @classmethod
    def from_dict(cls, data):
        children = [cls.from_dict(c) for c in data.get("children", [])]
        return cls(data["name"], data.get("value"), children)

root = TreeNode("root", 1, [
    TreeNode("A", 2, [TreeNode("A1", 3)]),
    TreeNode("B", 4)
])
serialized = json.dumps(root.to_dict(), indent=2)
print(serialized)
restored = TreeNode.from_dict(json.loads(serialized))
print(restored.to_dict() == root.to_dict())  # True
```

## Q44: What are the performance considerations for Composite tree operations?

**A:** Performance considerations for Composite trees include traversal complexity, memory overhead, and cache efficiency. Traversal complexity is O(n) for visiting all nodes, where n is the total number of nodes in the tree. For deep trees, recursive traversal can cause stack overflow — use iterative traversal instead. For wide trees, BFS traversal may be more cache-efficient than DFS because it accesses nodes level by level.

Memory overhead comes from storing child references in each Composite node. For large trees, this overhead can be significant. Using `__slots__` reduces per-node memory overhead by eliminating the `__dict__`. For very large trees, consider using array-based representations (like binary trees stored in arrays) instead of pointer-based representations.

Cache efficiency is affected by the tree's structure. DFS traversal accesses nodes in depth-first order, which may cause cache misses for wide trees. BFS traversal accesses nodes level by level, which is more cache-friendly for wide trees. For repeated operations, caching at the Composite level (see Q42) can eliminate redundant computation. For read-heavy workloads, pre-computing and storing results can improve performance at the cost of memory.

```python
import sys

class EfficientNode:
    __slots__ = ('name', 'value', '_children')

    def __init__(self, name, value=0):
        self.name, self.value = name, value
        self._children = []

    def add(self, child):
        self._children.append(child)

    def total(self):
        return self.value + sum(c.total() for c in self._children)

    def total_iterative(self):
        stack, total = [self], 0
        while stack:
            node = stack.pop()
            total += node.value
            stack.extend(node._children)
        return total

# Memory comparison
regular = type('Node', (), {'__init__': lambda s, n: setattr(s, 'name', n)})("test")
print(f"Regular: {sys.getsizeof(regular.__dict__)} bytes overhead")
```

## Q45: How do you implement the Composite pattern with type safety using generics?

**A:** Using generics with the Composite pattern provides type safety by ensuring that the Component interface is parameterized with the correct return types. In Python, this can be achieved using `typing.TypeVar` and `typing.Generic` to define generic Component, Leaf, and Composite classes. The generic type parameter ensures that operations return the correct types and that children are of the correct type.

The implementation defines a generic Component type with a type parameter for the value type. Leaf and Composite classes inherit from the generic Component and specify the concrete type. This provides type checking at class definition time and IDE support for autocompletion. For example, `Component[int]` ensures that all operations return `int` values.

Python's type system does not enforce generics at runtime, so the type safety is primarily for static analysis tools (mypy, pyright) and IDE support. However, this is valuable for large codebases where type errors can be difficult to track down. The generic approach also makes the code self-documenting by making the expected types explicit.

```python
from typing import TypeVar, Generic, List

T = TypeVar('T')

class Component(Generic[T]):
    def value(self) -> T:
        raise NotImplementedError

class Leaf(Component[T]):
    def __init__(self, val: T):
        self._val = val
    def value(self) -> T:
        return self._val

class Composite(Component[T]):
    def __init__(self):
        self._children: List[Component[T]] = []
    def add(self, child: Component[T]):
        self._children.append(child)
    def value(self) -> T:
        # Aggregate children's values
        return sum(c.value() for c in self._children)  # type: ignore

comp: Component[int] = Composite()
comp.add(Leaf(1))
comp.add(Leaf(2))
print(comp.value())  # 3
```

## Q46: How do you implement the Composite pattern with a command for undo/redo?

**A:** Combining Composite with Command creates a system where operations on tree nodes are encapsulated as command objects that support undo and redo. Each command stores the state needed to reverse the operation. When a command is executed, it performs the operation and stores the inverse. When undo is called, the inverse is executed. This is useful for tree editors (file managers, organizational chart editors) where users need to undo changes.

The implementation defines a Command interface with `execute()` and `undo()` methods. Each tree operation (add node, remove node, move node, change value) has a corresponding Command class. The Composite maintains a history stack of executed commands. Undo pops the last command from the stack and calls `undo()`. Redo pushes the command back onto the stack and calls `execute()`.

A practical example is a file manager where users can create, rename, move, and delete files and directories. Each operation is a Command that stores the original state. Undo reverses the operation by restoring the original state. The Composite tree structure ensures that operations on parent nodes affect all children correctly.

```python
class Command:
    def execute(self): pass
    def undo(self): pass

class AddNodeCommand(Command):
    def __init__(self, parent, child):
        self.parent, self.child = parent, child
    def execute(self):
        self.parent.add(self.child)
    def undo(self):
        self.parent.remove(self.child)

class Composite:
    def __init__(self, name):
        self.name, self._children, self._history = name, [], []

    def add(self, child):
        self._children.append(child)

    def remove(self, child):
        self._children.remove(child)

    def execute(self, command):
        command.execute()
        self._history.append(command)

    def undo(self):
        if self._history:
            self._history.pop().undo()

root = Composite("root")
child = Composite("child")
root.execute(AddNodeCommand(root, child))
print([c.name for c in root._children])  # ['child']
root.undo()
print([c.name for c in root._children])  # []
```

## Q47: What are the best practices for designing Composite hierarchies?

**A:** Best practices for Composite hierarchies include: (1) keep the Component interface minimal — only include operations that make sense for both leaves and composites; (2) use the safe approach for child management (define `add`/`remove` only in Composite); (3) handle cycles explicitly (prevent them or detect them during traversal); (4) provide both recursive and iterative traversal options; (5) implement proper equality comparison (value equality, not identity equality); (6) use `__slots__` for memory efficiency in large trees; and (7) support serialization for persistence and debugging.

The Component interface should follow the Interface Segregation Principle — leaves should not be forced to implement methods they do not need. If an operation only makes sense for Composites, define it only in the Composite class. If an operation makes sense for all nodes, define it in the Component interface with a sensible default for leaves.

For deep trees, provide iterative traversal methods to avoid stack overflow. For large trees, consider lazy loading (Proxy pattern) to avoid loading the entire tree into memory. For mutable trees, implement observer notifications so that changes propagate correctly. For persistent trees, implement copy-on-write semantics to avoid unnecessary copying.

```python
from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def depth(self) -> int:
        pass

class Leaf(Component):
    def __init__(self, name: str, file_size: int):
        self.name, self.file_size = name, file_size
    def size(self) -> int:
        return self.file_size
    def depth(self) -> int:
        return 0

class Composite(Component):
    def __init__(self, name: str):
        self.name, self._children = name, []

    def add(self, child: Component):
        if child._has_ancestor(self):
            raise ValueError("Cycle detected")
        self._children.append(child)

    def _has_ancestor(self, node):
        return any(c is node or c._has_ancestor(node) for c in self._children)

    def size(self) -> int:
        return sum(c.size() for c in self._children)

    def depth(self) -> int:
        if not self._children:
            return 0
        return 1 + max(c.depth() for c in self._children)
```

## Q48: How do you implement a Composite pattern with a mediator for coordination?

**A:** Combining Composite with Mediator creates a system where the Mediator coordinates interactions between nodes in the tree. Instead of nodes communicating directly with each other, they communicate through the Mediator. This decouples nodes from each other and centralizes coordination logic. The Mediator can enforce constraints, coordinate updates, and manage cross-cutting concerns.

The implementation defines a Mediator interface with methods for inter-node communication. Each node holds a reference to the Mediator and sends messages through it instead of directly to other nodes. The Mediator routes messages to the appropriate recipients and enforces any coordination rules. This is useful for complex tree structures where nodes need to coordinate their behavior (e.g., a UI where changing one widget affects others).

A practical example is a spreadsheet where cells are nodes in a Composite tree. When a cell's value changes, the Mediator recalculates all dependent cells. The cells do not know about each other — they only know about the Mediator. This centralizes the dependency tracking and recalculation logic, making the system easier to maintain and extend.

```python
class Mediator:
    def __init__(self):
        self._nodes = {}
    def register(self, name, node):
        self._nodes[name] = node
    def notify(self, sender, event, data):
        for name, node in self._nodes.items():
            if node is not sender:
                node.handle_event(event, data)

class MediatedNode:
    def __init__(self, name, mediator):
        self.name, self._mediator = name, mediator
        mediator.register(name, self)
    def handle_event(self, event, data):
        print(f"{self.name} received {event}: {data}")
    def send(self, event, data):
        self._mediator.notify(self, event, data)

mediator = Mediator()
a = MediatedNode("A", mediator)
b = MediatedNode("B", mediator)
a.send("update", {"value": 42})
# B received update: {'value': 42}
```

## Q49: How do you implement the Composite pattern with a flyweight for memory optimization?

**A:** Combining Composite with Flyweight creates a system where shared subtrees are represented by a single object, reducing memory usage. This is useful when the same subtree structure appears multiple times in a larger tree (e.g., repeated UI components, shared file directories, duplicated data structures). The Flyweight stores the shared state, and references to it are used instead of creating duplicate objects.

The implementation uses a Flyweight Factory that caches and returns shared objects. When a Composite node is created, the factory checks if an identical node already exists. If so, it returns the existing node. If not, it creates a new node and caches it. The key is defining what "identical" means — typically, two nodes are identical if they have the same type, same data, and same children.

This pattern is particularly effective for large trees with many repeated structures. For example, a UI framework might have thousands of buttons with the same appearance — using Flyweight, only one button definition is stored, and all instances reference it. A file system might have many directories with the same structure — using Flyweight, each unique directory is stored once.

```python
class FlyweightFactory:
    def __init__(self):
        self._cache = {}

    def get_node(self, name, value):
        key = (name, value)
        if key not in self._cache:
            self._cache[key] = FlyweightNode(name, value)
        return self._cache[key]

    def count(self):
        return len(self._cache)

class FlyweightNode:
    def __init__(self, name, value):
        self.name, self.value = name, value
        self._children = []

    def add(self, child):
        self._children.append(child)

factory = FlyweightFactory()
# These create only 3 unique nodes, not 6
root = FlyweightNode("root", 0)
root.add(factory.get_node("type_a", 1))
root.add(factory.get_node("type_a", 1))  # Same as above — shared
root.add(factory.get_node("type_b", 2))
print(factory.count())  # 2 unique flyweights
```

## Q50: What are the limitations of the Composite pattern and when should you avoid it?

**A:** The Composite pattern has several limitations: (1) it can make the design overly general — it is tempting to use Composite when a simpler structure would suffice; (2) it can be difficult to restrict which components can be children (Composite does not naturally enforce type constraints on children); (3) it can lead to performance issues for deep or wide trees (especially with recursive traversal); (4) it can make it difficult to enforce structural invariants (e.g., a maximum tree depth or a maximum number of children); and (5) it can complicate the implementation of operations that need to traverse the tree in a specific order.

You should avoid Composite when: (1) the tree structure is fixed and simple (a linked list or a simple hierarchy does not need Composite); (2) the operations on leaves and composites are fundamentally different (the uniform interface benefit is lost); (3) the tree is very deep or very wide (performance concerns outweigh the design benefits); (4) you need to enforce strict structural constraints (Composite does not naturally support this); or (5) the tree structure changes frequently and the overhead of maintaining the Composite is not justified.

The decision to use Composite should be based on whether the part-whole hierarchy is a natural fit for the problem domain and whether the uniform interface benefit justifies the added complexity. For simple hierarchies, a concrete class hierarchy may be more appropriate. For complex hierarchies with many node types and operations, Composite provides significant design benefits.

```python
# When NOT to use Composite — simple hierarchy with different operations
# Bad: Using Composite for a simple linked list
class ListNode:
    def __init__(self, value, next=None):
        self.value, self.next = value, next
    def sum(self):
        result = self.value
        current = self.next
        while current:
            result += current.value
            current = current.next
        return result

# Good: Simple hierarchy without needing Composite
# Use a concrete class hierarchy instead
class Animal:
    def speak(self): pass

class Dog(Animal):
    def speak(self): return "Woof"

class Cat(Animal):
    def speak(self): return "Meow"
```

## Q51: How do you compare the Decorator, Composite, and Bridge patterns in terms of intent?

**A:** The three patterns have distinct intents despite their structural similarities. Decorator adds responsibilities to objects dynamically — it is about extending behavior. Composite composes objects into tree structures and treats individual and composite objects uniformly — it is about representing part-whole hierarchies. Bridge separates an abstraction from its implementation so that both can vary independently — it is about decoupling two dimensions of variation.

Decorator answers "how do I add behavior to an existing object without modifying it?" Composite answers "how do I treat individual objects and groups of objects the same way?" Bridge answers "how do I separate an abstraction from its implementation so they can vary independently?" The patterns address different design problems and are not interchangeable.

In practice, these patterns are often combined. A Composite tree might use Decorator to add behavior to nodes. A Bridge abstraction might use Decorator to add cross-cutting concerns. A Decorator might use Composite to wrap multiple objects. Understanding the intent of each pattern helps you choose the right one for the problem at hand and combine them correctly.

```python
# Decorator — adds behavior
class Decorator:
    def __init__(self, wrapped): self._wrapped = wrapped
    def operation(self): return self._wrapped.operation() + " + decorated"

# Composite — represents tree
class Composite:
    def __init__(self): self._children = []
    def add(self, child): self._children.append(child)
    def operation(self): return sum(c.operation() for c in self._children)

# Bridge — separates abstraction from implementation
class Abstraction:
    def __init__(self, impl): self._impl = impl
    def operation(self): return self._impl.implement()
```

## Q52: What is the relationship between the Bridge pattern and the Dependency Inversion Principle?

**A:** The Bridge pattern is a direct application of the Dependency Inversion Principle (DIP), which states that high-level modules should not depend on low-level modules; both should depend on abstractions. In Bridge, the Abstraction (high-level module) depends on the Implementor interface (abstraction), not on the ConcreteImplementor (low-level module). This inverts the typical dependency direction where the high-level module would depend on the low-level implementation.

The Bridge achieves DIP by introducing an Implementor interface between the Abstraction and the ConcreteImplementor. The Abstraction knows only the Implementor interface, not the concrete implementations. Concrete implementations are injected at runtime (typically through the constructor), allowing the Abstraction to work with any Implementor that satisfies the interface. This makes the system flexible and testable.

The practical benefit is that the Abstraction can be tested independently of the Implementor by using mock implementations. New implementations can be added without modifying the Abstraction. The Abstraction and Implementor can be developed by different teams and combined at deployment time. This is the same benefit that DIP provides in general, applied specifically to the problem of separating abstraction from implementation.

```python
from abc import ABC, abstractmethod

# Abstraction depends on abstraction (Implementor), not on concrete implementation
class Abstraction:
    def __init__(self, impl: 'Implementor'):
        self._impl = impl  # Depends on interface, not concrete class

    def operation(self):
        return self._impl.implement()

class Implementor(ABC):
    @abstractmethod
    def implement(self): pass

class ConcreteImplementor(Implementor):
    def implement(self): return "concrete implementation"

# DIP: high-level Abstraction depends on low-level Implementor interface
a = Abstraction(ConcreteImplementor())
print(a.operation())
```

## Q53: How do you use the Decorator pattern for cross-cutting concerns?

**A:** Cross-cutting concerns are features that affect multiple parts of an application (logging, security, transaction management, caching). The Decorator pattern is ideal for these because decorators can wrap any object and add the cross-cutting behavior without modifying the wrapped object. Each concern is encapsulated in its own decorator, and multiple decorators can be stacked to combine concerns.

The implementation defines a decorator for each cross-cutting concern. The logging decorator wraps functions to log their calls. The authentication decorator wraps functions to check credentials. The caching decorator wraps functions to cache results. These decorators are independent and can be applied in any combination. The order of application determines the order of execution (outermost decorator runs first).

This approach is used extensively in web frameworks. Django's `@login_required` is a decorator for authentication. Flask's `@app.route` is a decorator for URL routing. Spring (Java) uses decorators for transaction management. The key benefit is that cross-cutting concerns are separated from business logic, making both easier to understand and maintain.

```python
import functools

def logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"LOG: {func.__name__} called")
        return func(*args, **kwargs)
    return wrapper

def timing(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        print(f"TIME: {func.__name__} took {time.time()-start:.4f}s")
        return result
    return wrapper

def caching(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@logging
@timing
@caching
def compute(n):
    return sum(range(n))

compute(1000000)  # LOG, computes, caches, times
compute(1000000)  # LOG, returns from cache, times
```

## Q54: What is the Decorator pattern's impact on the Liskov Substitution Principle?

**A:** The Decorator pattern preserves the Liskov Substitution Principle (LSP) when decorators implement the same interface as the wrapped object. Since the decorator is substitutable for the wrapped object (it implements the same interface and delegates to the wrapped object), client code can use decorated and undecorated objects interchangeably. This is the fundamental requirement for Decorator to work correctly.

However, decorators can violate LSP if they change the behavior of the wrapped object in ways that break the expected contract. For example, a decorator that short-circuits the wrapped method (skipping it entirely) or that throws unexpected exceptions can break the contract. A decorator that adds new methods not present in the original interface can also break LSP because the client does not expect these methods.

The practical guideline is: decorators should add behavior, not change behavior. Adding logging does not change the return value. Adding caching does not change the return value (for the same inputs). Adding validation might change the behavior by raising exceptions for invalid inputs, but this is acceptable because the original method's contract includes the precondition that inputs are valid. The key is that the decorator's behavior is consistent with the original object's contract.

```python
# LSP-compliant decorator — adds behavior without changing contract
class LSPCompliant:
    def __init__(self, wrapped):
        self._wrapped = wrapped
    def process(self, data):
        # Adds logging without changing the return value
        print(f"Processing: {data}")
        return self._wrapped.process(data)

# LSP-violating decorator — changes contract
class LSPViolating:
    def __init__(self, wrapped):
        self._wrapped = wrapped
    def process(self, data):
        # Changes return type — violates LSP
        return str(self._wrapped.process(data))
```

## Q55: How do you implement the Decorator pattern for API rate limiting?

**A:** API rate limiting is a classic use case for the Decorator pattern. The rate limiting decorator wraps API call functions and enforces a maximum number of calls within a time window. If the limit is exceeded, the decorator raises an exception or waits until the window resets. This provides rate limiting without modifying the API functions themselves.

The implementation tracks the number of calls within the current time window using a counter and a timestamp. When a call is made, the decorator checks whether the counter has exceeded the limit. If not, it increments the counter and allows the call. If the limit is exceeded, it either raises `RateLimitError` or blocks until the window resets. The window can be fixed (e.g., 100 calls per minute) or sliding (e.g., 100 calls in the last 60 seconds).

A more sophisticated implementation supports per-user rate limiting, different limits for different endpoints, and graceful degradation (returning a cached response instead of raising an error). The decorator can also log rate limit violations and provide metrics for monitoring.

```python
import time
import functools

class RateLimitError(Exception):
    pass

def rate_limit(max_calls, period_seconds):
    calls = []
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove calls outside the window
            calls[:] = [t for t in calls if now - t < period_seconds]
            if len(calls) >= max_calls:
                raise RateLimitError(f"Rate limit exceeded: {max_calls}/{period_seconds}s")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=5, period_seconds=60)
def call_api(endpoint):
    return f"Response from {endpoint}"

for i in range(5):
    print(call_api("/data"))  # Works 5 times
# call_api("/data")  # RateLimitError on 6th call
```

## Q56: What is the Composite pattern's relationship to the Iterator pattern?

**A:** The Composite pattern and the Iterator pattern are frequently combined because Composite tree structures need traversal mechanisms, and the Iterator pattern provides a standard interface for traversal. The Composite's `__iter__` method can return an iterator that traverses the tree using different strategies (DFS, BFS, pre-order, post-order). This separates the traversal logic from the tree structure, following the Single Responsibility Principle.

The implementation defines an iterator class or generator function that traverses the Composite tree. The iterator maintains a stack (for DFS) or queue (for BFS) of nodes to visit. For each node, it yields the node and adds its children to the traversal structure. The iterator can be configured with a traversal strategy, allowing the same tree to be traversed in different orders.

Python's `__iter__` method makes Composite objects iterable, allowing them to be used with `for` loops, list comprehensions, and other iteration constructs. This is a natural fit because Composite trees are inherently hierarchical structures that need to be traversed. The combination of Composite and Iterator provides a clean, Pythonic way to work with tree structures.

```python
class TreeNode:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []

    def __iter__(self):
        """DFS iteration using generator."""
        yield self
        for child in self.children:
            yield from child

    def bfs(self):
        """BFS iteration."""
        queue = [self]
        while queue:
            node = queue.pop(0)
            yield node
            queue.extend(node.children)

root = TreeNode("root", [
    TreeNode("A", [TreeNode("A1"), TreeNode("A2")]),
    TreeNode("B")
])
# Use with for loop, list comprehension, etc.
names = [node.name for node in root]  # DFS
bfs_names = [node.name for node in root.bfs()]  # BFS
```

## Q57: How do you implement the Bridge pattern for a database abstraction layer?

**A:** A database abstraction layer is a classic use case for the Bridge pattern. The Abstraction defines the database operations (connect, query, insert, update, delete), and the Implementor provides the database-specific implementation (MySQL, PostgreSQL, SQLite, MongoDB). The same application logic works with any database by delegating to the appropriate Implementor.

The implementation defines a Database abstraction with high-level operations and a DatabaseDriver implementor with low-level database operations. The abstraction handles transaction management, connection pooling, and query building. The driver handles the actual SQL execution, parameter binding, and result parsing. The two hierarchies can be extended independently — new databases require only a new driver, and new operations require only a new abstraction method.

This pattern is used by ORM libraries like SQLAlchemy, Django ORM, and Peewee. The abstraction provides a Pythonic interface for database operations, and the driver handles the database-specific details. This allows applications to switch databases by changing only the driver configuration, without modifying the application code.

```python
from abc import ABC, abstractmethod

class DatabaseDriver(ABC):
    @abstractmethod
    def execute(self, query, params): pass
    @abstractmethod
    def connect(self, connection_string): pass

class MySQLDriver(DatabaseDriver):
    def connect(self, cs):
        print(f"MySQL connected: {cs}")
    def execute(self, query, params):
        return f"MySQL: {query} with {params}"

class PostgresDriver(DatabaseDriver):
    def connect(self, cs):
        print(f"PostgreSQL connected: {cs}")
    def execute(self, query, params):
        return f"PostgreSQL: {query} with {params}"

class Database:
    def __init__(self, driver):
        self._driver = driver

    def query(self, table, conditions):
        sql = f"SELECT * FROM {table} WHERE {conditions}"
        return self._driver.execute(sql, None)

    def insert(self, table, data):
        sql = f"INSERT INTO {table} VALUES"
        return self._driver.execute(sql, data)

db_mysql = Database(MySQLDriver())
db_pg = Database(PostgresDriver())
print(db_mysql.query("users", "id=1"))
print(db_pg.query("users", "id=1"))
```

## Q58: How do you combine the Decorator pattern with the Proxy pattern?

**A:** The Decorator pattern and the Proxy pattern are structurally identical — both wrap an object and implement the same interface. The difference is intent: Decorator adds behavior, while Proxy controls access. Combining them creates a system where access control and behavior extension are applied through the same mechanism. For example, a caching proxy adds caching behavior (Decorator) while controlling access to the original object (Proxy).

The implementation creates classes that serve as both Decorators and Proxies. A caching proxy wraps an object, adds caching behavior (Decorator), and controls access by serving cached results without hitting the original object (Proxy). A logging proxy wraps an object, adds logging (Decorator), and controls access by restricting which methods can be called (Proxy).

The combination is useful because both patterns share the same structure. A single wrapper class can implement both behaviors. For example, a `SecureCacheProxy` might cache results (Decorator), control access based on permissions (Proxy), and log access attempts (Decorator). This reduces the number of wrapper classes and makes the system easier to maintain.

```python
class CachingProxy:
    def __init__(self, real):
        self._real = real
        self._cache = {}

    def get(self, key):
        if key not in self._cache:
            self._cache[key] = self._real.get(key)
        return self._cache[key]

    def set(self, key, value):
        self._cache[key] = value
        self._real.set(key, value)

class RealDataSource:
    def __init__(self):
        self._data = {}
    def get(self, key):
        print(f"Fetching {key} from database")
        return self._data.get(key)
    def set(self, key, value):
        self._data[key] = value

real = RealDataSource()
proxy = CachingProxy(real)
real.set("x", 42)
print(proxy.get("x"))  # Fetches from DB
print(proxy.get("x"))  # Serves from cache — no DB access
```

## Q59: What are the testing strategies for the Decorator pattern?

**A:** Testing decorators requires verifying that the decorator adds the correct behavior without breaking the original function. The key test cases are: (1) the decorator preserves the function's return value (when no additional behavior is added), (2) the decorator adds the expected behavior (logging, caching, etc.), (3) the decorator handles exceptions correctly, (4) the decorator preserves function metadata (`__name__`, `__doc__`), and (5) multiple decorators compose correctly.

The recommended approach is to test each decorator independently using the original function as a mock. This isolates the decorator's behavior from the function's behavior. For example, a logging decorator test should verify that the log message is produced, not that the function returns the correct value. A caching decorator test should verify that the function is called only once for repeated inputs.

For integration testing, test the decorator chain to verify that multiple decorators compose correctly. This verifies that the execution order is correct and that the decorators do not interfere with each other. Use `functools.wraps` to ensure that metadata is preserved across the chain.

```python
import functools

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count = getattr(wrapper, 'call_count', 0) + 1
        return func(*args, **kwargs)
    return wrapper

def test_decorator_preserves_return_value():
    @log_calls
    def add(a, b):
        return a + b
    assert add(1, 2) == 3

def test_decorator_counts_calls():
    @log_calls
    def add(a, b):
        return a + b
    add(1, 2)
    add(3, 4)
    assert add.call_count == 2

def test_decorator_preserves_metadata():
    @log_calls
    def add(a, b):
        """Add two numbers."""
        return a + b
    assert add.__name__ == 'add'
    assert add.__doc__ == 'Add two numbers.'

test_decorator_preserves_return_value()
test_decorator_counts_calls()
test_decorator_preserves_metadata()
print("All tests passed")
```

## Q60: What is the Composite pattern's impact on the Single Responsibility Principle?

**A:** The Composite pattern can violate the Single Responsibility Principle (SRP) if a Composite class handles both its own behavior and the management of children. The Composite class is responsible for its own data and behavior (like any other class) AND for managing its children (add, remove, traverse). This violates SRP because the class has two reasons to change: its own behavior changes, or the child management logic changes.

The solution is to separate the child management logic into a separate class (e.g., a `TreeManager` or `CompositeIterator`). The Composite class focuses on its own behavior, and the TreeManager handles child management and traversal. This separation follows SRP by giving each class a single responsibility.

However, the pragmatic view is that the child management logic is closely related to the Composite's purpose — a Composite that does not manage children is not really a Composite. The SRP violation is minor and acceptable in most cases. The key is to keep the Composite class focused on its domain-specific behavior and to extract child management into a separate class only if the child management logic becomes complex or is shared with other classes.

```python
# SRP violation — Composite handles both behavior and child management
class Composite:
    def __init__(self):
        self._children = []
    def add(self, child):
        self._children.append(child)
    def operation(self):
        return sum(c.operation() for c in self._children)

# SRP improvement — separate child management
class TreeManager:
    def __init__(self):
        self._children = []
    def add(self, child):
        self._children.append(child)
    def traverse(self):
        for child in self._children:
            yield child

class Composite:
    def __init__(self):
        self._manager = TreeManager()
    def add(self, child):
        self._manager.add(child)
    def operation(self):
        return sum(c.operation() for c in self._manager.traverse())
```

## Q61: How do you implement the Bridge pattern with dependency injection?

**A:** Combining Bridge with Dependency Injection (DI) creates a system where the Implementor is injected into the Abstraction at runtime, typically through constructor injection. This makes the Bridge more flexible because the Implementor can be swapped without modifying the Abstraction. DI frameworks (like `injector`, `dependency-injector`, or manual injection) can manage the lifecycle and wiring of Implementors.

The implementation defines the Abstraction's constructor to accept an Implementor argument. The DI container creates the Abstraction and injects the appropriate Implementor based on configuration. This decouples the Abstraction from the concrete Implementor and allows different Implementors to be used in different environments (development, testing, production).

The benefit is testability — you can inject mock Implementors for testing without modifying the Abstraction. It also makes the system configurable — different Implementors can be selected based on configuration files, environment variables, or runtime conditions. This is a common pattern in enterprise applications where the same code runs against different databases, message brokers, or external services.

```python
from abc import ABC, abstractmethod

class EmailSender(ABC):
    @abstractmethod
    def send(self, to, subject, body): pass

class SMTPEmailSender(EmailSender):
    def send(self, to, subject, body):
        return f"SMTP: Sending to {to}: {subject}"

class MockEmailSender(EmailSender):
    def send(self, to, subject, body):
        return f"MOCK: Would send to {to}: {subject}"

class NotificationService:
    def __init__(self, email_sender: EmailSender):
        self._email_sender = email_sender

    def notify_user(self, user, message):
        return self._email_sender.send(user.email, "Notification", message)

# Production
service = NotificationService(SMTPEmailSender())
# Testing
test_service = NotificationService(MockEmailSender())
```

## Q62: What is the difference between the Decorator pattern and the Proxy pattern?

**A:** The Decorator pattern and the Proxy pattern are structurally identical — both wrap an object and implement the same interface. The key difference is intent. Decorator adds behavior to the wrapped object (logging, caching, validation). Proxy controls access to the wrapped object (lazy loading, access control, remote access). Decorator is about enhancing; Proxy is about controlling.

The practical difference manifests in how the wrapper relates to the wrapped object. A Decorator always delegates to the wrapped object and adds behavior before or after. A Proxy may or may not delegate — a caching proxy serves cached results without hitting the wrapped object, a virtual proxy delays creation of the wrapped object, and a protection proxy may deny access entirely. Decorator is transparent (the wrapped object is always called); Proxy is sometimes opaque (the wrapped object may not be called).

Another difference is in the relationship between the wrapper and the wrapped object. Decorator's wrapper is typically created at the same time as the wrapped object. Proxy's wrapper may be created before the wrapped object (virtual proxy) or may wrap a remote object (remote proxy). Decorator's wrapper is part of the object's behavior; Proxy's wrapper is part of the access control mechanism.

```python
# Decorator — adds behavior, always delegates
class LoggingDecorator:
    def __init__(self, wrapped):
        self._wrapped = wrapped
    def operation(self):
        print("Logging")
        return self._wrapped.operation()  # Always delegates

# Proxy — controls access, may not delegate
class CachingProxy:
    def __init__(self, real):
        self._real = real
        self._cache = {}
    def operation(self, key):
        if key in self._cache:
            return self._cache[key]  # Does NOT delegate
        result = self._real.operation(key)
        self._cache[key] = result
        return result
```

## Q63: How do you implement the Composite pattern with a visitor for double dispatch?

**A:** Double dispatch is a technique where the operation performed depends on both the visitor type and the node type. The Composite pattern with Visitor uses double dispatch: the node's `accept` method calls the appropriate `visit` method on the visitor, and the visitor's `visit` method performs the operation on the node. This allows different visitors to perform different operations on the same tree without modifying the node classes.

The implementation requires each node class to have an `accept(visitor)` method that calls `visitor.visit_<node_type>(self)`. The visitor has separate `visit` methods for each node type. When `accept` is called on a node, it dispatches to the correct `visit` method based on the node's type. This is the first dispatch. The visitor's `visit` method then performs the operation on the node, which may call `accept` on child nodes, triggering the second dispatch.

The benefit is that adding new operations only requires creating a new visitor — no changes to node classes are needed. This follows the Open-Closed Principle for operations. However, adding new node types requires modifying the Visitor interface and all existing visitors, which violates OCP for node types. This trade-off is acceptable when the node types are stable but operations change frequently.

```python
from abc import ABC, abstractmethod

class Visitable(ABC):
    @abstractmethod
    def accept(self, visitor): pass

class Element(Visitable):
    def __init__(self, value):
        self.value = value
    def accept(self, visitor):
        return visitor.visit_element(self)

class Composite(Visitable):
    def __init__(self):
        self.children = []
    def add(self, child):
        self.children.append(child)
    def accept(self, visitor):
        return visitor.visit_composite(self)

class Visitor(ABC):
    @abstractmethod
    def visit_element(self, elem): pass
    @abstractmethod
    def visit_composite(self, comp): pass

class SumVisitor(Visitor):
    def visit_element(self, elem):
        return elem.value
    def visit_composite(self, comp):
        return sum(child.accept(self) for child in comp.children)

tree = Composite()
tree.add(Element(1))
tree.add(Element(2))
sub = Composite()
sub.add(Element(3))
tree.add(sub)
print(tree.accept(SumVisitor()))  # 6
```

## Q64: What are the common use cases for the Bridge pattern in Python frameworks?

**A:** Python frameworks use Bridge extensively for separating abstractions from implementations. Django's ORM uses Bridge to separate model definitions from database backends. Flask's application context separates the WSGI abstraction from the server implementation. SQLAlchemy separates the Core expression language from dialect-specific SQL generation. These frameworks demonstrate how Bridge enables multiple backends for the same abstraction.

Other common use cases include: rendering engines (PIL/Pillow separates image operations from file format handlers), logging (Python's `logging` module separates Logger from Handler), serialization (marshmallow separates Schema from field types), and testing (pytest separates test collection from test execution). In each case, the abstraction defines the high-level interface, and the implementation provides the backend-specific details.

The key benefit in frameworks is extensibility — new backends can be added without modifying the core framework code. This allows third-party developers to add support for new databases, file formats, or protocols by implementing the Implementor interface. The framework's Abstraction remains unchanged, ensuring backward compatibility.

```python
# Framework example: Logger with multiple handlers (Bridge)
import logging

class Logger:
    def __init__(self, handler):
        self._handler = handler

    def log(self, level, message):
        self._handler.emit(level, message)

class ConsoleHandler:
    def emit(self, level, message):
        print(f"[{level}] {message}")

class FileHandler:
    def __init__(self, filename):
        self.filename = filename
    def emit(self, level, message):
        print(f"Writing to {self.filename}: [{level}] {message}")

# Same Logger, different handlers
console_logger = Logger(ConsoleHandler())
file_logger = Logger(FileHandler("app.log"))
console_logger.log("INFO", "Server started")
file_logger.log("INFO", "Server started")
```

## Q65: How do you handle thread safety in Composite tree operations?

**A:** Thread safety in Composite trees requires synchronization when multiple threads access or modify the tree simultaneously. The key challenges are: (1) concurrent modifications to the tree structure (adding/removing children), (2) concurrent reads during modification (traversal while another thread modifies), and (3) concurrent operations on the same node (multiple threads calling the same method).

The implementation uses locks to protect critical sections. A per-node lock protects each node's children list. A tree-level lock protects the entire tree. The choice depends on the granularity needed — per-node locks allow more concurrency but are more complex to implement. Tree-level locks are simpler but reduce concurrency.

For read-heavy workloads, use a read-write lock (or `threading.RLock`) that allows concurrent reads but exclusive writes. For write-heavy workloads, use a mutex that serializes all operations. Python's `threading.Lock` and `threading.RLock` provide the basic synchronization primitives. The `concurrent.futures` module provides higher-level abstractions for parallel tree operations.

```python
import threading

class ThreadSafeNode:
    def __init__(self, name):
        self.name = name
        self._children = []
        self._lock = threading.Lock()

    def add(self, child):
        with self._lock:
            self._children.append(child)

    def remove(self, child):
        with self._lock:
            self._children.remove(child)

    def total(self):
        with self._lock:
            children = self._children[:]
        return sum(c.total() for c in children)

root = ThreadSafeNode("root")
# Multiple threads can safely add/remove/iterate
```

## Q66: What is the Decorator pattern's relationship to the Open-Closed Principle?

**A:** The Decorator pattern is one of the primary mechanisms for achieving the Open-Closed Principle (OCP) in Python. OCP states that classes should be open for extension but closed for modification. Decorators extend behavior by wrapping objects with new decorators, not by modifying the original classes. This means you can add new functionality to existing code without changing it.

The key insight is that decorators compose behavior through wrapping. When you need to add logging to a function, you wrap it with a logging decorator instead of modifying the function's code. When you need to add caching, you wrap it with a caching decorator. The original function remains unchanged (closed for modification), and new behavior is added through decorators (open for extension).

This is why Python frameworks use decorators so extensively. Django's `@login_required` adds authentication without modifying the view function. Flask's `@app.route` adds URL routing without modifying the handler function. Each decorator is independent and can be applied in any combination. New decorators can be created for new cross-cutting concerns without modifying existing decorators or functions.

```python
# Following OCP — extending through decorators
def audit(func):
    def wrapper(*args, **kwargs):
        print(f"AUDIT: {func.__name__} called")
        return func(*args, **kwargs)
    return wrapper

def compress(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"COMPRESSED: {result}")
        return result
    return wrapper

# Adding new behavior without modifying existing code
@audit
@compress
def process_data(data):
    return f"Processed: {data}"

process_data("input")
# AUDIT: process_data called
# COMPRESSED: Processed: input
```

## Q67: How do you implement the Bridge pattern with strategy selection at runtime?

**A:** Runtime strategy selection in Bridge allows the implementation to be chosen dynamically based on conditions (configuration, environment, user input). The Abstraction holds a reference to an Implementor interface, and the concrete Implementor is selected at runtime from a registry or factory. This makes the system configurable without code changes.

The implementation uses a factory or registry to look up Implementor classes by name. The Abstraction's constructor (or a setter method) accepts the implementation name and looks up the corresponding class from the registry. The registry can be populated at startup from configuration files, environment variables, or command-line arguments. This pattern is used in database drivers, rendering engines, and payment processors.

The benefit is that the same code can work with different implementations in different environments. For example, a test environment might use a mock database driver, while production uses a real PostgreSQL driver. The selection is based on configuration, not code changes. This is the Strategy pattern applied to the Bridge's Implementor.

```python
class RendererRegistry:
    _renderers = {}

    @classmethod
    def register(cls, name, renderer_class):
        cls._renderers[name] = renderer_class

    @classmethod
    def get(cls, name):
        return cls._renderers[name]()

class SVGRenderer:
    def render(self, shape):
        return f"SVG: {shape}"

class CanvasRenderer:
    def render(self, shape):
        return f"Canvas: {shape}"

RendererRegistry.register("svg", SVGRenderer)
RendererRegistry.register("canvas", CanvasRenderer)

class Shape:
    def __init__(self, name, renderer_name):
        self.name = name
        self._renderer = RendererRegistry.get(renderer_name)

    def draw(self):
        return self._renderer.render(self.name)

# Runtime selection based on configuration
s = Shape("circle", "svg")
print(s.draw())  # SVG: circle
```

## Q68: What are the limitations of the Bridge pattern?

**A:** The Bridge pattern has several limitations: (1) it increases complexity by introducing two separate hierarchies; (2) it requires careful design to identify the correct abstraction and implementation axes; (3) it can be overkill for simple systems where inheritance is sufficient; (4) it adds indirection that can reduce performance; (5) it can make the code harder to understand for developers unfamiliar with the pattern; and (6) it requires both hierarchies to be designed upfront, which may not be possible in rapidly evolving systems.

The main challenge is identifying the correct axes of variation. If you split the hierarchy incorrectly (e.g., splitting along the wrong dimension), the pattern provides little benefit and adds unnecessary complexity. The correct split requires understanding which dimensions of the system are likely to vary independently. If only one dimension varies, Bridge is unnecessary — use inheritance or Strategy instead.

Another limitation is that Bridge's indirection can reduce performance. The extra method call (Abstraction → Implementor) adds overhead compared to direct method calls. In performance-critical code, this overhead may be significant. The recommendation is to use Bridge when the design benefits justify the complexity and performance cost, and to avoid it for simple systems where the overhead is not justified.

```python
# Bridge is overkill for simple cases
# Bad: Using Bridge for a simple system
class Abstraction:
    def __init__(self, impl):
        self._impl = impl
    def operation(self):
        return self._impl.do_work()

# Good: Simple inheritance is sufficient
class Base:
    def operation(self):
        return "base"

class Derived(Base):
    def operation(self):
        return "derived"
```

## Q69: How do you implement the Composite pattern with a fluent interface?

**A:** A fluent interface allows method calls to be chained, making Composite tree construction more readable. Instead of calling `add()` multiple times on separate lines, you can chain calls: `tree.add(child1).add(child2).add(child3)`. This is achieved by having `add()` return `self` (the Composite instance), enabling method chaining.

The implementation modifies the Composite's `add` method to return `self`. This allows the next `add` call to be chained. The fluent interface can also support other operations like `set_value`, `set_name`, and `traverse`, each returning `self` for chaining. The result is a more concise and readable tree construction API.

A common extension is to support builder-style construction where the tree is built step by step with a readable API. For example, `TreeBuilder().root("A").child("B").child("C").build()` creates a tree with root "A" and children "B" and "C". This is particularly useful for test fixtures and configuration files where trees need to be constructed frequently.

```python
class FluentNode:
    def __init__(self, name, value=None):
        self.name, self.value = name, value
        self._children = []

    def add(self, child):
        self._children.append(child)
        return self  # Enable chaining

    def child(self, name, value=None):
        node = FluentNode(name, value)
        self._children.append(node)
        return self

    def build(self):
        return self

root = (FluentNode("root")
    .child("A")
    .child("B")
    .child("C"))
print([c.name for c in root._children])  # ['A', 'B', 'C']
```

## Q70: What is the Decorator pattern's impact on debugging and stack traces?

**A:** Decorators can complicate debugging by adding extra frames to the stack trace. When a decorated function raises an exception, the stack trace includes the decorator's wrapper function, making it harder to identify the original function's code. This is mitigated by using `functools.wraps`, which preserves the original function's `__name__` and `__qualname__`, making stack traces more readable.

The key issue is that Python's traceback shows the wrapper function's frame in addition to the original function's frame. With `functools.wraps`, the traceback shows the original function's name, which helps identify the source of the error. Without `functools.wraps`, the traceback shows the wrapper's name, which is confusing.

A more advanced technique is to use `traceback` module to customize the stack trace. You can filter out decorator frames, add custom error messages, or format the traceback differently. However, this adds complexity and is rarely necessary for simple decorators. The recommendation is to use `functools.wraps` consistently and to keep decorator logic simple.

```python
import functools

def simple_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@simple_decorator
def buggy_function():
    raise ValueError("Something went wrong")

try:
    buggy_function()
except ValueError:
    import traceback
    traceback.print_exc()
    # Shows: ValueError: Something went wrong
    # In function: buggy_function (thanks to functools.wraps)
```

## Q71: How do you implement the Bridge pattern for cross-platform file I/O?

**A:** Cross-platform file I/O is a classic Bridge use case. The Abstraction defines file operations (read, write, seek, close), and the Implementor provides platform-specific implementations (Windows, Linux, macOS). The same application code works on any platform by delegating to the appropriate Implementor. The Implementor handles platform-specific details like file path formats, permissions, and encoding.

The implementation defines a File abstraction with high-level operations and a PlatformFile implementor with low-level I/O operations. The abstraction handles buffering, encoding, and error handling. The implementor handles the actual system calls (open, read, write, close). The two hierarchies can be extended independently — new platforms require only a new implementor, and new operations require only a new abstraction method.

This pattern is used by Python's `io` module, which separates the BufferedIOBase abstraction from platform-specific implementations. It is also used by cross-platform libraries like `pathlib`, which provides a unified interface for file path operations across platforms. The key benefit is that application code does not need to know which platform it is running on.

```python
from abc import ABC, abstractmethod

class FileImplementor(ABC):
    @abstractmethod
    def open(self, path): pass
    @abstractmethod
    def read(self, handle): pass
    @abstractmethod
    def write(self, handle, data): pass

class UnixFileImplementor(FileImplementor):
    def open(self, path):
        print(f"Unix: opening {path}")
        return f"unix_handle({path})"
    def read(self, handle):
        return f"Unix read from {handle}"
    def write(self, handle, data):
        print(f"Unix: writing '{data}' to {handle}")

class WindowsFileImplementor(FileImplementor):
    def open(self, path):
        print(f"Windows: opening {path}")
        return f"win_handle({path})"
    def read(self, handle):
        return f"Windows read from {handle}"
    def write(self, handle, data):
        print(f"Windows: writing '{data}' to {handle}")

class File:
    def __init__(self, implementor, path):
        self._impl = implementor
        self._handle = self._impl.open(path)

    def read(self):
        return self._impl.read(self._handle)

    def write(self, data):
        self._impl.write(self._handle, data)

unix_file = File(UnixFileImplementor(), "/tmp/test.txt")
win_file = File(WindowsFileImplementor(), "C:\\test.txt")
unix_file.write("hello")
win_file.write("hello")
```

## Q72: What is the Composite pattern's relationship to the Flyweight pattern?

**A:** The Composite pattern and the Flyweight pattern can be combined to optimize memory usage in large trees. Flyweight shares common state between objects, reducing memory consumption. When applied to Composite trees, nodes with identical structure and data share a single Flyweight instance, and references to the shared node are used instead of creating duplicates.

The implementation uses a Flyweight Factory that caches node instances. When a node is created, the factory checks if an identical node already exists. If so, it returns the existing node. If not, it creates a new node and caches it. The key is defining what "identical" means — typically, two nodes are identical if they have the same type, same data, and same children.

This combination is particularly effective for trees with many repeated structures. For example, a UI framework might have thousands of buttons with the same appearance — using Flyweight, only one button definition is stored. A file system might have many directories with the same structure — using Flyweight, each unique directory is stored once. The Composite structure is preserved, but memory usage is significantly reduced.

```python
class FlyweightFactory:
    def __init__(self):
        self._cache = {}

    def get(self, name, value):
        key = (name, value)
        if key not in self._cache:
            self._cache[key] = FlyweightNode(name, value)
        return self._cache[key]

class FlyweightNode:
    def __init__(self, name, value):
        self.name, self.value = name, value
        self._children = []

    def add(self, child):
        self._children.append(child)

factory = FlyweightFactory()
root = FlyweightNode("root", 0)
# These share the same FlyweightNode instance
root.add(factory.get("type_a", 1))
root.add(factory.get("type_a", 1))
root.add(factory.get("type_b", 2))
print(len(factory._cache))  # 2 unique nodes, not 3
```

## Q73: How do you implement the Decorator pattern for input validation?

**A:** Input validation decorators wrap functions to validate their arguments before the function executes. The decorator inspects the arguments, checks them against validation rules, and raises exceptions for invalid inputs. This separates validation logic from business logic, making both easier to maintain. The decorator can validate types, ranges, formats, and custom constraints.

The implementation uses `functools.wraps` to preserve the original function's metadata and `*args, **kwargs` to handle any argument pattern. The decorator can use type hints, validation functions, or schema definitions to validate inputs. For complex validation, libraries like `pydantic` or `cerberus` can be integrated into the decorator.

A key design decision is whether to validate all arguments or only specific ones. Validating all arguments provides comprehensive coverage but may be slow for functions with many arguments. Validating only specific arguments (specified as parameters to the decorator) provides targeted validation without the overhead. The decorator can also validate return values by wrapping the return statement.

```python
import functools

def validate(**rules):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            for param_name, rule in rules.items():
                value = bound.arguments.get(param_name)
                if not rule(value):
                    raise ValueError(f"Invalid {param_name}: {value}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate(
    age=lambda v: isinstance(v, int) and 0 <= v <= 150,
    name=lambda v: isinstance(v, str) and len(v) > 0
)
def create_user(name, age):
    return {"name": name, "age": age}

print(create_user("Alice", 30))  # OK
# create_user("", 30)  # ValueError: Invalid name
```

## Q74: What are the best practices for combining multiple structural patterns?

**A:** Best practices for combining structural patterns include: (1) use each pattern for its intended purpose — Decorator for behavior extension, Composite for tree structures, Bridge for decoupling abstraction from implementation; (2) minimize the number of patterns combined — each pattern adds complexity; (3) ensure the patterns are complementary, not redundant; (4) document the pattern relationships in design documents; and (5) test each pattern independently before combining them.

The key is to understand the intent of each pattern and combine them only when the combination provides clear benefits. For example, combining Decorator with Composite makes sense when you need to add behavior to tree nodes. Combining Bridge with Abstract Factory makes sense when you need to create compatible abstraction-implementation pairs. Combining all three patterns is rarely necessary and should be avoided unless the problem demands it.

A practical guideline is to start with the simplest pattern that solves the problem. If Decorator alone is sufficient, do not add Composite. If Composite alone is sufficient, do not add Bridge. Only add complexity when the problem requires it. This follows the YAGNI principle (You Ain't Gonna Need It) and keeps the codebase maintainable.

```python
# Good: Using Decorator + Bridge for a specific use case
class Abstraction:
    def __init__(self, impl):
        self._impl = impl
    def operation(self):
        return self._impl.do_work()

class LoggingDecorator:
    def __init__(self, wrapped):
        self._wrapped = wrapped
    def operation(self):
        print("Logging")
        return self._wrapped.operation()

# Bridge separates abstraction from implementation
# Decorator adds logging
bridge = Abstraction(SomeImplementor())
decorated = LoggingDecorator(bridge)
decorated.operation()  # Logs, then delegates to bridge
```

## Q75: How do you refactor inherited code to use the Decorator pattern?

**A:** Refactoring inherited code to use Decorator involves replacing inheritance-based behavior extension with composition-based extension. The steps are: (1) identify the behaviors added by subclasses, (2) extract each behavior into a decorator class, (3) replace subclass instantiation with decorator composition, and (4) remove the subclasses. This reduces the class hierarchy and makes behavior extension more flexible.

The key challenge is identifying which behaviors are added by subclasses. If a subclass overrides a method to add logging, the logging behavior can be extracted into a decorator. If a subclass adds new methods, those methods may need to remain in the class or be moved to a separate utility. The refactoring should be done incrementally, one behavior at a time, with tests to verify that behavior is preserved.

A common refactoring is to replace a hierarchy of classes like `TextProcessor`, `UpperTextProcessor`, `TrimTextProcessor`, `UpperTrimTextProcessor` with a single `TextProcessor` class and decorators `UpperDecorator`, `TrimDecorator`. This eliminates the 2^N subclass explosion and makes behavior combination flexible at runtime.

```python
# Before: Inheritance-based
class TextProcessor:
    def process(self, text): return text

class UpperText(TextProcessor):
    def process(self, text): return super().process(text).upper()

class TrimText(TextProcessor):
    def process(self, text): return super().process(text).strip()

# After: Decorator-based
class TextProcessor:
    def process(self, text): return text

class UpperDecorator:
    def __init__(self, wrapped): self._wrapped = wrapped
    def process(self, text): return self._wrapped.process(text).upper()

class TrimDecorator:
    def __init__(self, wrapped): self._wrapped = wrapped
    def process(self, text): return self._wrapped.process(text).strip()

# Any combination works without new classes
decorated = UpperDecorator(TrimDecorator(TextProcessor()))
```

## Q76: How do you compare the Decorator and Bridge patterns in terms of flexibility?

**A:** The Decorator pattern provides flexibility in behavior extension — you can add, remove, or rearrange decorators at runtime. The Bridge pattern provides flexibility in implementation selection — you can swap the implementation at runtime. Both patterns use composition to achieve flexibility, but they apply it to different concerns. Decorator is about what the object does; Bridge is about how the object does it.

Decorator's flexibility is in the number and order of decorators. You can stack as many decorators as needed and change the stack at any time. This makes it ideal for cross-cutting concerns that need to be applied in different combinations. Bridge's flexibility is in the implementation choice. You can switch from MySQL to PostgreSQL without changing the application code. This makes it ideal for backend services that need to support multiple implementations.

The practical difference is that Decorator's flexibility is compositional (combining multiple behaviors), while Bridge's flexibility is substitutive (replacing one implementation with another). Decorator adds layers; Bridge swaps the core. Both are valuable, and they can be combined when you need both compositional behavior extension and substitutive implementation selection.

```python
# Decorator — compositional flexibility
class Base:
    def op(self): return "base"
class Decorator1:
    def __init__(self, w): self._w = w
    def op(self): return self._w.op() + " +d1"
class Decorator2:
    def __init__(self, w): self._w = w
    def op(self): return self._w.op() + " +d2"

# Any combination: d1(d2(base)), d2(d1(base)), d1(base), etc.

# Bridge — substitutive flexibility
class Abstraction:
    def __init__(self, impl): self._impl = impl
    def op(self): return self._impl.do_work()

# Can swap impl at runtime: Abstraction(ImplA) -> Abstraction(ImplB)
```

## Q77: What is the Composite pattern's impact on memory management?

**A:** The Composite pattern can have significant memory implications, especially for large trees. Each Composite node stores references to its children, which creates a parent-child reference graph. This graph can prevent garbage collection if there are cyclic references. Python's garbage collector handles reference cycles, but the overhead of cycle detection can impact performance.

Memory overhead comes from: (1) storing child references in each Composite node, (2) the overhead of the list used to store children, (3) the overhead of the Composite object itself (Python object header, `__dict__`). For large trees with millions of nodes, this overhead can be significant. Using `__slots__` reduces per-node overhead by eliminating the `__dict__`.

To optimize memory, consider: (1) using `__slots__` for nodes, (2) using weak references for back-references (parent references), (3) sharing common subtrees using Flyweight, (4) using array-based representations for binary trees, and (5) implementing lazy loading for large subtrees. The choice of optimization depends on the tree's size, structure, and access patterns.

```python
import sys
import weakref

class OptimizedNode:
    __slots__ = ('name', 'value', '_children', '_parent_ref')

    def __init__(self, name, value=0):
        self.name, self.value = name, value
        self._children = []
        self._parent_ref = None

    def add(self, child):
        self._children.append(child)
        child._parent_ref = weakref.ref(self)

    @property
    def parent(self):
        return self._parent_ref() if self._parent_ref else None

root = OptimizedNode("root")
root.add(OptimizedNode("child"))
print(f"Node size: {sys.getsizeof(root)} bytes")  # Smaller than dict-based
```

## Q78: How do you implement the Decorator pattern for authentication and authorization?

**A:** Authentication and authorization decorators wrap functions to verify user identity and permissions before the function executes. The authentication decorator checks that the user is logged in (has valid credentials). The authorization decorator checks that the user has the required permissions. These decorators separate security concerns from business logic, making both easier to maintain.

The implementation typically uses a decorator factory that accepts the required role or permission. The decorator retrieves the current user from a request context (e.g., Flask's `g` object or Django's `request.user`), checks the user's permissions, and raises an exception if the check fails. The decorator can also handle different authentication mechanisms (session-based, token-based, OAuth).

A key design decision is where to store the user context. In web frameworks, the user context is typically stored in a thread-local variable or a context variable. The decorator accesses this context to retrieve the current user. For non-web applications, the user context might be passed as a parameter or stored in a global variable.

```python
import functools

class PermissionDenied(Exception):
    pass

class Unauthorized(Exception):
    pass

def require_auth(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, '_current_user') or wrapper._current_user is None:
            raise Unauthorized("Authentication required")
        return func(*args, **kwargs)
    return wrapper

def require_role(role):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = getattr(wrapper, '_current_user', None)
            if user is None:
                raise Unauthorized("Authentication required")
            if role not in user.get('roles', []):
                raise PermissionDenied(f"Role '{role}' required")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@require_role('admin')
def delete_user(user_id):
    return f"Deleted user {user_id}"

# Simulate authenticated user
delete_user._current_user = {'name': 'Alice', 'roles': ['admin']}
print(delete_user(42))  # "Deleted user 42"
```

## Q79: What is the Composite pattern's role in UI framework design?

**A:** UI frameworks use the Composite pattern extensively because user interfaces are naturally hierarchical. Widgets (buttons, text boxes, panels) can contain other widgets, forming a tree structure. The Composite pattern allows the framework to treat individual widgets and containers uniformly, simplifying layout, rendering, and event handling. A container widget manages its children, and the framework traverses the tree to render all widgets.

The implementation defines a Widget interface with methods like `render()`, `handle_event()`, and `get_bounds()`. Leaf widgets (Button, Label) implement these methods directly. Container widgets (Panel, Window) implement these methods by delegating to their children. The framework traverses the widget tree to render the entire UI, handle events (clicks, key presses), and perform layout calculations.

This pattern is used by tkinter, PyQt, wxPython, and web frameworks (where the DOM is a Composite tree). The key benefit is that adding new widget types does not require changing the framework code — the new widget implements the Widget interface and is automatically integrated into the tree. The framework can also apply decorators to widgets (for logging, accessibility, or theming) without modifying the widget classes.

```python
class Widget:
    def __init__(self, name):
        self.name = name
        self._children = []

    def add(self, child):
        self._children.append(child)

    def render(self, indent=0):
        result = "  " * indent + f"<{self.name}>"
        for child in self._children:
            result += "\n" + child.render(indent + 1)
        result += "\n" + "  " * indent + f"</{self.name}>"
        return result

class Button(Widget):
    def __init__(self, label):
        super().__init__("button")
        self.label = label

    def render(self, indent=0):
        return "  " * indent + f"<button>{self.label}</button>"

panel = Widget("panel")
panel.add(Button("OK"))
panel.add(Button("Cancel"))
print(panel.render())
# <panel>
#   <button>OK</button>
#   <button>Cancel</button>
# </panel>
```

## Q80: How do you implement the Decorator pattern for caching with TTL?

**A:** A TTL (Time-To-Live) caching decorator stores computed results and returns them until they expire. The decorator tracks when each result was computed and checks the TTL on each access. If the result has expired, the decorator recomputes it and resets the TTL. This provides time-based cache invalidation without manual cache management.

The implementation uses a dictionary to store cached results keyed by function arguments. Each entry stores the result and the timestamp when it was computed. On each access, the decorator checks whether the current time exceeds the timestamp plus TTL. If so, the entry is removed and the function is called again. The TTL can be fixed (same for all entries) or variable (different for different entries).

A key design decision is whether to use a sliding TTL (reset on each access) or a fixed TTL (expire after creation regardless of access). Sliding TTL keeps frequently accessed data in cache longer. Fixed TTL ensures data is refreshed at regular intervals. The choice depends on the data's freshness requirements and access patterns.

```python
import functools
import time

def ttl_cache(ttl_seconds=60):
    cache = {}
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache:
                result, timestamp = cache[args]
                if now - timestamp < ttl_seconds:
                    return result
            result = func(*args)
            cache[args] = (result, now)
            return result
        wrapper.cache_clear = cache.clear
        return wrapper
    return decorator

@ttl_cache(ttl_seconds=5)
def expensive_computation(n):
    print(f"Computing {n}...")
    return sum(range(n))

print(expensive_computation(1000000))  # Computes
print(expensive_computation(1000000))  # Returns from cache
```

## Q81: How do you combine the Composite and Bridge patterns for a file system abstraction?

**A:** Combining Composite and Bridge creates a file system where the tree structure (Composite) is separated from the platform implementation (Bridge). The Composite defines the file/directory hierarchy, and the Bridge provides platform-specific I/O operations. This allows the same file system tree to work on Windows, Linux, and macOS by swapping the platform implementation.

The implementation defines a FileSystemNode interface (Component) with `read`, `write`, and `list` operations. File and Directory classes implement this interface (Composite). A PlatformImplementor provides low-level I/O operations (open, read, write, close). Each FileSystemNode holds a reference to the PlatformImplementor and delegates I/O operations to it.

This combination is powerful because it provides both structural flexibility (Composite for tree operations) and implementation flexibility (Bridge for platform operations). The tree can be traversed using DFS or BFS, and each node delegates I/O to the platform-specific implementation. Adding a new platform only requires a new Implementor, and adding new node types only requires a new Component subclass.

```python
from abc import ABC, abstractmethod

class PlatformIO(ABC):
    @abstractmethod
    def read(self, path): pass
    @abstractmethod
    def write(self, path, data): pass

class UnixIO(PlatformIO):
    def read(self, path):
        return f"Unix read: {path}"
    def write(self, path, data):
        print(f"Unix write: {path} = {data}")

class WindowsIO(PlatformIO):
    def read(self, path):
        return f"Windows read: {path}"
    def write(self, path, data):
        print(f"Windows write: {path} = {data}")

class FSNode(ABC):
    def __init__(self, name, io):
        self.name, self._io = name, io

class File(FSNode):
    def read(self):
        return self._io.read(self.name)
    def write(self, data):
        self._io.write(self.name, data)

class Directory(FSNode):
    def __init__(self, name, io):
        super().__init__(name, io)
        self._children = []
    def add(self, child):
        self._children.append(child)
    def list(self):
        return [c.name for c in self._children]

root = Directory("/", UnixIO())
root.add(File("readme.txt", UnixIO()))
print(root.list())  # ['readme.txt']
```

## Q82: What is the Decorator pattern's impact on performance and how do you mitigate it?

**A:** Decorators add performance overhead because each decorator adds a function call layer. When you stack N decorators, each function call goes through N wrapper functions before reaching the original function. This overhead is typically small (a few microseconds per call) but can add up in hot paths that are called millions of times. The overhead includes function call overhead, argument passing, and any additional logic in the wrapper.

Mitigation strategies include: (1) minimize decorator logic — keep wrapper functions simple; (2) use caching decorators to avoid recomputation; (3) profile to identify which decorators are bottlenecks; (4) merge multiple decorators into a single decorator that performs all operations; (5) use class-based decorators with `__slots__` for lower overhead; and (6) for extreme performance cases, use compile-time decoration (metaclasses or class decorators) instead of runtime decoration.

The most effective mitigation is caching — if a caching decorator is outermost, subsequent calls are served from cache without going through the inner decorators. This eliminates the overhead for repeated calls. For unique calls, the overhead is unavoidable but typically negligible compared to the actual work being done.

```python
import functools

# Minimal overhead decorator
def minimal_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Merged decorators — single wrapper for multiple concerns
def merged_decorators(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Logging + timing + validation in one wrapper
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Result: {result}")
        return result
    return wrapper
```

## Q83: How do you implement the Composite pattern for organizational hierarchies?

**A:** Organizational hierarchies are a natural fit for the Composite pattern. Employees are leaf nodes, and managers are composite nodes that contain their reports. Operations like calculating salary, counting headcount, and finding reporting chains can be performed uniformly on both individual employees and entire departments. The Composite pattern allows the same operations to work at any level of the hierarchy.

The implementation defines an Employee interface with methods like `salary()`, `headcount()`, and `name()`. Individual Employee classes implement these methods directly. Manager classes implement these methods by aggregating results from their reports. The tree structure naturally represents the organizational hierarchy, and operations traverse the tree to aggregate results.

A practical example is a company where the CEO's headcount includes all employees. The CFO's headcount includes only the finance department. Each manager's salary includes their own salary plus the salaries of all their reports. The Composite pattern makes these aggregations straightforward — each node's operation aggregates results from its children.

```python
class Employee:
    def __init__(self, name, salary):
        self.name, self._salary = name, salary
        self._reports = []

    def add_report(self, employee):
        self._reports.append(employee)

    def salary(self):
        return self._salary + sum(r.salary() for r in self._reports)

    def headcount(self):
        return 1 + sum(r.headcount() for r in self._reports)

ceo = Employee("CEO", 200000)
cfo = Employee("CFO", 150000)
dev_lead = Employee("Dev Lead", 120000)
dev1 = Employee("Dev1", 80000)
dev2 = Employee("Dev2", 80000)

cfo.add_report(Employee("Accountant", 60000))
dev_lead.add_report(dev1)
dev_lead.add_report(dev2)
ceo.add_report(cfo)
ceo.add_report(dev_lead)

print(f"CEO headcount: {ceo.headcount()}")  # 5
print(f"CEO total salary: {ceo.salary()}")  # 690000
print(f"Dev Lead headcount: {dev_lead.headcount()}")  # 3
```

## Q84: What is the Bridge pattern's role in database driver architecture?

**A:** Database driver architecture is a classic Bridge use case. The Abstraction defines the database interface (connect, query, insert, update, delete, transaction), and the Implementor provides the database-specific implementation (MySQL, PostgreSQL, SQLite, MongoDB). The same application code works with any database by delegating to the appropriate driver. This eliminates vendor lock-in and simplifies database migration.

The implementation defines a DBDriver interface with low-level operations and a Database abstraction with high-level operations. The abstraction handles connection pooling, transaction management, and query building. The driver handles SQL execution, parameter binding, and result parsing. The two hierarchies can be extended independently — new databases require only a new driver, and new operations require only a new abstraction method.

This pattern is used by SQLAlchemy, Django ORM, and Python's `dbapi` standard. The key benefit is that applications can switch databases by changing only the connection string and driver, without modifying the application code. This is essential for applications that need to support multiple databases or that may need to migrate databases in the future.

```python
from abc import ABC, abstractmethod

class DBDriver(ABC):
    @abstractmethod
    def connect(self, url): pass
    @abstractmethod
    def execute(self, sql, params=None): pass
    @abstractmethod
    def fetch_all(self): pass

class SQLiteDriver(DBDriver):
    def connect(self, url):
        print(f"SQLite connected: {url}")
    def execute(self, sql, params=None):
        print(f"SQLite: {sql}")
        return [("row1",), ("row2",)]
    def fetch_all(self):
        return [("row1",), ("row2",)]

class PostgreSQLDriver(DBDriver):
    def connect(self, url):
        print(f"PostgreSQL connected: {url}")
    def execute(self, sql, params=None):
        print(f"PostgreSQL: {sql}")
        return [("row1",), ("row2",)]
    def fetch_all(self):
        return [("row1",), ("row2",)]

class Database:
    def __init__(self, driver):
        self._driver = driver
        self._connected = False

    def connect(self, url):
        self._driver.connect(url)
        self._connected = True

    def query(self, table, where="1=1"):
        sql = f"SELECT * FROM {table} WHERE {where}"
        return self._driver.execute(sql)

db = Database(SQLiteDriver())
db.connect("app.db")
print(db.query("users"))
```

## Q85: How do you implement the Decorator pattern for retry logic with exponential backoff?

**A:** A retry decorator with exponential backoff wraps a function and retries it when it fails. The retry delay increases exponentially with each attempt (e.g., 1s, 2s, 4s, 8s), giving the failing service time to recover. This is essential for network calls, database operations, and other operations that may fail temporarily.

The implementation tracks the attempt number and calculates the delay as `base_delay * 2^attempt`. After each failed attempt, the decorator waits for the calculated delay before retrying. If all attempts fail, the decorator raises the last exception. The decorator can also accept a list of exception types to retry on, allowing it to retry on transient errors while failing immediately on permanent errors.

A key design decision is whether to add jitter (randomness) to the delay. Jitter prevents thundering herd problems where multiple clients retry simultaneously, overwhelming the failing service. The decorator can add jitter by randomizing the delay within a range (e.g., `delay * random(0.5, 1.5)`). This distributes retries across time and reduces the load on the failing service.

```python
import functools
import time
import random

def retry_with_backoff(max_attempts=5, base_delay=1, max_delay=60, jitter=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    if jitter:
                        delay *= random.uniform(0.5, 1.5)
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry_with_backoff(max_attempts=3, base_delay=0.1)
def unreliable_api():
    import random
    if random.random() < 0.7:
        raise ConnectionError("API unavailable")
    return "success"

# Will retry with exponential backoff until success or max attempts
```

## Q86: What are the design principles that guide the use of structural patterns?

**A:** The key design principles guiding structural patterns are: (1) Composition over Inheritance — prefer composing objects over creating deep class hierarchies; (2) Program to an Interface — depend on abstractions, not concrete implementations; (3) Single Responsibility — each class should have one reason to change; (4) Open-Closed — classes should be open for extension, closed for modification; (5) Liskov Substitution — subtypes must be substitutable for their base types; (6) Interface Segregation — many specific interfaces are better than one general-purpose interface; and (7) Dependency Inversion — depend on abstractions, not concretions.

These principles guide the choice and implementation of structural patterns. Decorator follows OCP by extending behavior without modification. Composite follows ISP by defining a minimal interface for tree nodes. Bridge follows DIP by separating abstraction from implementation. Understanding these principles helps you choose the right pattern for the problem and implement it correctly.

The principles also help identify anti-patterns. If you find yourself creating many subclasses to handle feature combinations, you are violating OCP — use Decorator instead. If your Composite interface forces leaves to implement methods they do not need, you are violating ISP — use the safe approach. If your Bridge abstraction depends on a concrete implementor, you are violating DIP — depend on the Implementor interface.

```python
# Composition over Inheritance
class Composed:
    def __init__(self, a, b):
        self._a, self._b = a, b

# Program to Interface
from abc import ABC, abstractmethod
class Interface(ABC):
    @abstractmethod
    def method(self): pass

# Open-Closed
class Extended:
    def __init__(self, wrapped):
        self._wrapped = wrapped
    def method(self):
        return self._wrapped.method() + " extended"
```

## Q87: How do you test the Bridge pattern effectively?

**A:** Testing the Bridge pattern requires testing both the Abstraction and the Implementor independently, and then testing their interaction. The key is to verify that the Abstraction correctly delegates to the Implementor and that swapping Implementors does not break the Abstraction's behavior. Mock Implementors are essential for testing the Abstraction in isolation.

For unit testing, mock the Implementor and verify that the Abstraction calls the correct methods with the correct arguments. This tests the delegation logic without depending on the real Implementor. For integration testing, use real Implementors to verify that the Abstraction and Implementor work together correctly. For swap testing, verify that the Abstraction works with different Implementors without modification.

The test structure should include: (1) tests for each Abstraction method, verifying delegation to the Implementor; (2) tests for each Implementor, verifying correct behavior; (3) tests for Abstraction-Implementor pairs, verifying integration; and (4) tests for Implementor swapping, verifying that the Abstraction works with different Implementors.

```python
import unittest
from unittest.mock import Mock

class Abstraction:
    def __init__(self, impl):
        self._impl = impl
    def operation(self):
        return self._impl.implement()

class TestAbstraction(unittest.TestCase):
    def setUp(self):
        self.mock_impl = Mock()
        self.mock_impl.implement.return_value = "mock result"
        self.abstraction = Abstraction(self.mock_impl)

    def test_delegates_to_implementor(self):
        result = self.abstraction.operation()
        self.assertEqual(result, "mock result")
        self.mock_impl.implement.assert_called_once()

    def test_works_with_different_implementor(self):
        impl2 = Mock()
        impl2.implement.return_value = "impl2 result"
        ab2 = Abstraction(impl2)
        self.assertEqual(ab2.operation(), "impl2 result")

if __name__ == "__main__":
    unittest.main()
```

## Q88: What is the Composite pattern's relationship to the Visitor pattern?

**A:** The Composite pattern and the Visitor pattern are frequently combined because Composite trees need operations that traverse the tree, and Visitor provides a way to add operations without modifying the tree nodes. The Visitor pattern separates the operation from the tree structure, allowing new operations to be added by creating new Visitors. This follows the Open-Closed Principle for operations.

The implementation defines a Visitor interface with `visit` methods for each node type. Each node's `accept` method calls the appropriate `visit` method on the Visitor. For Composite nodes, the Visitor's `visit` method also iterates over children and calls `accept` on each child. This provides double dispatch — the operation depends on both the Visitor type and the node type.

The benefit is that adding new operations (like pricing, validation, or transformation) only requires creating a new Visitor. No changes to the node classes are needed. This is useful when the tree structure is stable but operations change frequently (like a compiler's AST, where the tree structure is defined by the language grammar but operations like code generation, optimization, and analysis change frequently).

```python
from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def accept(self, visitor): pass

class Element(Node):
    def __init__(self, value):
        self.value = value
    def accept(self, visitor):
        return visitor.visit_element(self)

class Composite(Node):
    def __init__(self):
        self.children = []
    def add(self, child):
        self.children.append(child)
    def accept(self, visitor):
        return visitor.visit_composite(self)

class Visitor(ABC):
    @abstractmethod
    def visit_element(self, elem): pass
    @abstractmethod
    def visit_composite(self, comp): pass

class ValidateVisitor(Visitor):
    def visit_element(self, elem):
        return elem.value > 0
    def visit_composite(self, comp):
        return all(child.accept(self) for child in comp.children)

tree = Composite()
tree.add(Element(1))
tree.add(Element(2))
print(tree.accept(ValidateVisitor()))  # True
```

## Q89: How do you implement the Decorator pattern for logging with different log levels?

**A:** A logging decorator with different log levels wraps functions to log their calls at specified severity levels. The decorator logs the function name, arguments, return value, and execution time. Different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) control the verbosity of the logging. This provides consistent logging across all functions without modifying the function code.

The implementation uses a decorator factory that accepts the log level as a parameter. The decorator logs at the specified level using Python's `logging` module. The log message can include the function name, arguments, return value, and execution time. For error logging, the decorator can also log the exception traceback.

A key design decision is what to log. Logging everything (arguments, return values, timing) provides maximum visibility but can generate excessive output. Logging only errors and warnings provides minimal overhead but limited visibility. The decorator should be configurable to support different logging needs.

```python
import functools
import logging
import time

def log_execution(level=logging.INFO):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start
                logging.log(level, f"{func.__name__} completed in {elapsed:.4f}s")
                return result
            except Exception as e:
                logging.error(f"{func.__name__} failed: {e}")
                raise
        return wrapper
    return decorator

@log_execution(level=logging.DEBUG)
def compute(n):
    return sum(range(n))

logging.basicConfig(level=logging.DEBUG)
compute(1000000)  # Logs at DEBUG level
```

## Q90: What are the anti-patterns to avoid when using structural patterns?

**A:** Common anti-patterns include: (1) Over-Engineering — using complex patterns when simple code would suffice; (2) Pattern Unification — forcing all problems into a single pattern; (3) God Object — putting too much responsibility into a single class; (4) Deep Hierarchy — creating too many levels of inheritance or decoration; (5) Circular Dependencies — creating cycles in Composite or Bridge structures; (6) Leaky Abstraction — exposing implementation details in the Abstraction interface; and (7) Premature Abstraction — creating patterns before the problem is well understood.

The most common anti-pattern is over-engineering. Using Bridge for a simple system with one implementation, using Composite for a flat list, or using Decorator for a function that needs only one additional behavior adds complexity without benefit. The recommendation is to start simple and add patterns only when the problem demands it.

Another anti-pattern is deep decoration — stacking many decorators on a single function. While each decorator is simple, the combination can be difficult to understand and debug. If you find yourself stacking more than 3-4 decorators, consider whether the behaviors should be merged into a single class or whether the function should be restructured.

```python
# Anti-pattern: Over-engineering
# Bad: Using Bridge for a simple system
class Abstraction:
    def __init__(self, impl):
        self._impl = impl
    def op(self):
        return self._impl.do_work()

# Good: Simple function
def op():
    return "result"

# Anti-pattern: Deep decoration
@decorator1
@decorator2
@decorator3
@decorator4
@decorator5  # Too many layers
def func():
    pass
```

## Q91: How do you refactor from inheritance to the Decorator pattern?

**A:** Refactoring from inheritance to Decorator involves identifying behaviors added by subclasses, extracting each behavior into a decorator, replacing subclass instantiation with decorator composition, and removing the subclasses. The key is to identify which subclass methods add behavior (logging, caching, validation) and extract them into independent decorators.

The refactoring steps are: (1) identify all subclasses and their overridden methods; (2) extract each overridden behavior into a decorator class; (3) replace `UpperTextProcessor()` with `UpperDecorator(TextProcessor())`; (4) verify that all tests pass; (5) remove the subclasses. The refactoring should be done incrementally, one behavior at a time, with tests at each step.

The benefit is that the class hierarchy is flattened, and behaviors can be combined at runtime. The drawback is that the decorator pattern adds indirection, which can make the code harder to follow for developers unfamiliar with the pattern. The trade-off is usually worth it for systems with many feature combinations.

```python
# Before: Inheritance hierarchy
class Text:
    def process(self, text): return text

class Upper(Text):
    def process(self, text): return super().process(text).upper()

class Trim(Text):
    def process(self, text): return super().process(text).strip()

# After: Decorator composition
class Text:
    def process(self, text): return text

class UpperDec:
    def __init__(self, w): self._w = w
    def process(self, text): return self._w.process(text).upper()

class TrimDec:
    def __init__(self, w): self._w = w
    def process(self, text): return self._w.process(text).strip()

# Usage: UpperDec(TrimDec(Text())) — any combination without new classes
```

## Q92: What is the Composite pattern's role in document processing systems?

**A:** Document processing systems use Composite to represent document structure. A document is a tree of elements: paragraphs, headings, images, tables, and lists. Each element type implements a common interface with methods like `render()`, `to_html()`, and `to_text()`. Operations on the document traverse the tree, processing each element according to its type.

The implementation defines a DocumentElement interface with rendering methods. Leaf elements (Paragraph, Image) implement these methods directly. Composite elements (Section, Table, List) implement these methods by delegating to their children. The document tree can be serialized to different formats (HTML, PDF, Markdown) by applying different renderers.

This pattern is used by document processing libraries like `python-docx`, `markdown`, and `reportlab`. The key benefit is that new element types can be added without modifying the document structure. Operations like search, spell-check, and formatting can be implemented as tree traversals that visit each element.

```python
class DocElement:
    def __init__(self, content):
        self.content = content

    def to_html(self):
        return f"<p>{self.content}</p>"

class Heading(DocElement):
    def __init__(self, level, text):
        self.level, self.content = level, text

    def to_html(self):
        return f"<h{self.level}>{self.content}</h{self.level}>"

class Section(DocElement):
    def __init__(self, title):
        self.title, self._children = title, []

    def add(self, child):
        self._children.append(child)

    def to_html(self):
        children_html = "\n".join(c.to_html() for c in self._children)
        return f"<section>\n<h1>{self.title}</h1>\n{children_html}\n</section>"

doc = Section("Introduction")
doc.add(Heading(2, "Background"))
doc.add(DocElement("This is the background."))
print(doc.to_html())
```

## Q93: How do you implement the Bridge pattern for notification systems?

**A:** Notification systems are a natural Bridge use case. The Abstraction defines the notification logic (what to notify, when to notify), and the Implementor provides the delivery mechanism (email, SMS, push notification, Slack). The same notification logic works with any delivery mechanism by delegating to the appropriate Implementor. This allows the system to support multiple notification channels without modifying the notification logic.

The implementation defines a Notification abstraction with methods like `send()` and `format()`. A NotificationChannel implementor provides the delivery mechanism. The abstraction handles message formatting, recipient management, and delivery scheduling. The implementor handles the actual delivery (SMTP for email, SMS gateway for SMS, push service for push notifications).

This pattern is used by notification services like Twilio, SendGrid, and Firebase Cloud Messaging. The key benefit is that adding a new notification channel only requires implementing a new NotificationChannel. The notification logic remains unchanged, ensuring consistent behavior across channels.

```python
from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, recipient, message): pass

class EmailChannel(NotificationChannel):
    def send(self, recipient, message):
        return f"Email to {recipient}: {message}"

class SMSChannel(NotificationChannel):
    def send(self, recipient, message):
        return f"SMS to {recipient}: {message}"

class PushChannel(NotificationChannel):
    def send(self, recipient, message):
        return f"Push to {recipient}: {message}"

class Notification:
    def __init__(self, channel):
        self._channel = channel

    def notify(self, recipient, subject, body):
        message = f"[{subject}] {body}"
        return self._channel.send(recipient, message)

email = Notification(EmailChannel())
sms = Notification(SMSChannel())
print(email.notify("user@email.com", "Alert", "Server down"))
print(sms.notify("+1234567890", "Alert", "Server down"))
```

## Q94: What is the Decorator pattern's relationship to the Open-Closed Principle in practice?

**A:** In practice, the Decorator pattern achieves OCP by allowing new behavior to be added through new decorator classes, not by modifying existing code. When a new cross-cutting concern arises (like rate limiting), you create a new decorator. The existing decorators and functions remain unchanged. This is the practical application of OCP — extension through composition, not modification.

The key practical benefit is that decorators can be applied and removed independently. You can add logging to a function without affecting its caching behavior. You can add authentication to a view without affecting its logging. Each decorator is independent and can be tested in isolation. This makes the system easier to maintain and extend.

In practice, the Decorator pattern is the primary mechanism for OCP in Python frameworks. Django's `@login_required`, Flask's `@app.route`, and Python's `@functools.lru_cache` are all applications of OCP through Decorator. The pattern is so natural in Python that developers often use it without thinking of it as a design pattern.

```python
# Practical OCP: Adding new behavior through new decorators
import functools

def rate_limit(max_calls):
    def decorator(func):
        calls = []
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time
            now = time.time()
            calls[:] = [t for t in calls if now - t < 60]
            if len(calls) >= max_calls:
                raise Exception("Rate limited")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# New concern: rate limiting — add new decorator, no code changes
@rate_limit(max_calls=10)
def api_call():
    return "data"
```

## Q95: How do you implement the Composite pattern with a command for batch operations?

**A:** Combining Composite with Command creates a system where operations on tree nodes are encapsulated as command objects that can be executed, undone, and batched. Batch operations apply a command to multiple nodes at once, which is useful for operations like renaming multiple files, moving entire subtrees, or updating multiple records. The Composite tree provides the structure, and the Command pattern provides the operation abstraction.

The implementation defines a Command interface with `execute()` and `undo()` methods. Each tree operation (add, remove, move, rename) has a corresponding Command class. A BatchCommand class wraps multiple commands and executes them as a unit. If any command in the batch fails, the batch can be rolled back by undoing all previously executed commands.

This pattern is used in file managers (batch rename, batch move), database tools (batch update, batch delete), and document editors (find and replace). The key benefit is that complex operations are broken into simple, reversible commands that can be composed into batches.

```python
class Command:
    def execute(self): pass
    def undo(self): pass

class RenameCommand(Command):
    def __init__(self, node, new_name):
        self.node, self.new_name = node, new_name
        self.old_name = None
    def execute(self):
        self.old_name = self.node.name
        self.node.name = self.new_name
    def undo(self):
        self.node.name = self.old_name

class BatchCommand(Command):
    def __init__(self, commands):
        self.commands = commands
        self._executed = []
    def execute(self):
        for cmd in self.commands:
            cmd.execute()
            self._executed.append(cmd)
    def undo(self):
        for cmd in reversed(self._executed):
            cmd.undo()
        self._executed = []

class Node:
    def __init__(self, name):
        self.name = name

a, b, c = Node("a"), Node("b"), Node("c")
batch = BatchCommand([
    RenameCommand(a, "A"),
    RenameCommand(b, "B"),
    RenameCommand(c, "C")
])
batch.execute()
print(a.name, b.name, c.name)  # A B C
batch.undo()
print(a.name, b.name, c.name)  # a b c
```

## Q96: What are the performance implications of combining multiple structural patterns?

**A:** Combining multiple structural patterns adds indirection layers that can impact performance. Each pattern adds a delegation layer: Decorator adds a wrapper call, Composite adds a child traversal, Bridge adds an implementation call. When combined, these layers multiply, potentially adding significant overhead to each operation.

The practical impact depends on the operation frequency and the overhead of each layer. For operations called millions of times (like attribute access in a hot loop), the overhead can be measurable. For operations called rarely (like HTTP requests), the overhead is negligible. The recommendation is to profile before optimizing and to combine patterns only when the design benefits justify the performance cost.

Mitigation strategies include: (1) caching at the outermost layer (so inner layers are not called repeatedly); (2) merging multiple delegation layers into a single layer; (3) using `__slots__` to reduce per-object overhead; (4) pre-computing results where possible; and (5) using lazy evaluation to defer computation until needed.

```python
# Performance impact of multiple layers
class Base:
    def op(self): return "base"

class Layer1:
    def __init__(self, w): self._w = w
    def op(self): return self._w.op() + " +l1"

class Layer2:
    def __init__(self, w): self._w = w
    def op(self): return self._w.op() + " +l2"

class Layer3:
    def __init__(self, w): self._w = w
    def op(self): return self._w.op() + " +l3"

# Three delegation layers
obj = Layer3(Layer2(Layer1(Base())))
obj.op()  # Three function calls before reaching Base

# Merged into single layer
class Merged:
    def __init__(self, w): self._w = w
    def op(self):
        base = self._w.op()
        return base + " +l1 +l2 +l3"  # One function call
```

## Q97: How do you implement the Decorator pattern for rate limiting with sliding window?

**A:** A sliding window rate limiter tracks requests within a moving time window. Unlike fixed windows (which reset at fixed intervals), sliding windows provide smoother rate limiting by considering requests from the last N seconds. This prevents bursts at window boundaries and provides more accurate rate limiting.

The implementation maintains a list of timestamps for recent requests. When a new request arrives, the decorator removes timestamps older than the window size, counts the remaining timestamps, and compares with the limit. If the count exceeds the limit, the request is rejected. Otherwise, the current timestamp is added and the request proceeds.

The sliding window algorithm is more accurate than the fixed window algorithm because it considers the exact timing of requests, not just the count within a fixed interval. This prevents the "boundary burst" problem where a client can make twice the limit by timing requests at the end of one window and the start of the next.

```python
import functools
import time

def sliding_window_rate_limit(max_requests, window_seconds):
    requests = []
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove requests outside the window
            requests[:] = [t for t in requests if now - t < window_seconds]
            if len(requests) >= max_requests:
                raise Exception(f"Rate limit: {max_requests}/{window_seconds}s")
            requests.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@sliding_window_rate_limit(max_requests=5, window_seconds=60)
def api_call(endpoint):
    return f"Response from {endpoint}"

# Smooth rate limiting — no boundary burst
for i in range(5):
    print(api_call("/data"))
```

## Q98: What is the Composite pattern's role in configuration management systems?

**A:** Configuration management systems use Composite to represent hierarchical configuration. Configuration sections can contain subsections, key-value pairs, and references to other configurations. The Composite pattern allows operations like merging, validation, and serialization to work uniformly on individual settings and entire configuration trees.

The implementation defines a ConfigNode interface with methods like `get()`, `set()`, `merge()`, and `validate()`. Leaf nodes represent individual settings (key-value pairs). Composite nodes represent configuration sections that contain other nodes. The tree structure naturally represents the configuration hierarchy, and operations traverse the tree to perform their work.

This pattern is used by configuration libraries like `configparser`, `pydantic-settings`, and `dynaconf`. The key benefit is that configuration can be loaded from multiple sources (files, environment variables, databases) and merged into a single tree. The Composite pattern makes the merge operation straightforward — each node type handles its own merge logic.

```python
class ConfigNode:
    def __init__(self, key, value=None):
        self.key, self.value = key, value
        self._children = {}

    def add(self, child):
        self._children[child.key] = child

    def get(self, path):
        parts = path.split(".")
        node = self
        for part in parts:
            if part in node._children:
                node = node._children[part]
            else:
                return None
        return node.value

    def set(self, path, value):
        parts = path.split(".")
        node = self
        for part in parts[:-1]:
            if part not in node._children:
                node._children[part] = ConfigNode(part)
            node = node._children[part]
        node._children[parts[-1]] = ConfigNode(parts[-1], value)

root = ConfigNode("root")
root.set("database.host", "localhost")
root.set("database.port", 5432)
root.set("debug", True)
print(root.get("database.host"))  # localhost
print(root.get("database.port"))  # 5432
```

## Q99: How do you combine the Decorator and Bridge patterns for a flexible architecture?

**A:** Combining Decorator and Bridge creates a system where the Bridge separates abstraction from implementation, and Decorator adds cross-cutting concerns. The Bridge provides the core functionality (e.g., database operations), and Decorators add logging, caching, validation, and other concerns. This separation makes the system both flexible (different implementations) and extensible (different behaviors).

The implementation defines a Bridge where the Abstraction uses an Implementor for core operations. Decorators wrap the Abstraction to add behavior. The decorators are independent of the Bridge — they can be applied to any Abstraction, regardless of the Implementor. This makes the system highly composable: you can swap the Implementor and rearrange the Decorators independently.

This pattern is used in enterprise applications where the core functionality is provided by a Bridge (database, messaging, file system) and cross-cutting concerns are added through Decorators (logging, security, monitoring). The key benefit is that each concern is independent and can be developed, tested, and maintained separately.

```python
from abc import ABC, abstractmethod

# Bridge: separates abstraction from implementation
class DataStore(ABC):
    @abstractmethod
    def read(self, key): pass
    @abstractmethod
    def write(self, key, value): pass

class RedisStore(DataStore):
    def read(self, key):
        return f"Redis: {key}"
    def write(self, key, value):
        print(f"Redis: {key} = {value}")

class DictStore(DataStore):
    def __init__(self):
        self._data = {}
    def read(self, key):
        return self._data.get(key)
    def write(self, key, value):
        self._data[key] = value

# Decorators: add cross-cutting concerns
class LoggingDecorator:
    def __init__(self, wrapped):
        self._wrapped = wrapped
    def read(self, key):
        print(f"LOG: read({key})")
        return self._wrapped.read(key)
    def write(self, key, value):
        print(f"LOG: write({key}, {value})")
        self._wrapped.write(key, value)

class CachingDecorator:
    def __init__(self, wrapped):
        self._wrapped = wrapped
        self._cache = {}
    def read(self, key):
        if key not in self._cache:
            self._cache[key] = self._wrapped.read(key)
        return self._cache[key]
    def write(self, key, value):
        self._cache[key] = value
        self._wrapped.write(key, value)

# Combine Bridge + Decorators
store = CachingDecorator(LoggingDecorator(RedisStore()))
store.write("x", 42)  # LOG: write(x, 42) -> Redis: x = 42
print(store.read("x")) # LOG: read(x) -> Redis: x (cached)
```

## Q100: What are the key takeaways for using Decorator, Composite, and Bridge patterns effectively?

**A:** The key takeaways are: (1) Decorator is for behavior extension — use it when you need to add responsibilities to objects dynamically without modifying them. It is the primary mechanism for OCP in Python. (2) Composite is for tree structures — use it when you need to treat individual objects and groups uniformly. It is essential for hierarchical data (file systems, UI, organizations). (3) Bridge is for decoupling — use it when you have multiple dimensions of variation that should vary independently. It prevents class explosion.

The patterns are complementary, not competing. Decorator adds behavior, Composite represents structure, Bridge separates concerns. They can be combined when the problem requires multiple pattern benefits. However, start with the simplest pattern that solves the problem and add complexity only when needed.

In Python, the `@decorator` syntax makes Decorator particularly natural. Composite is well-supported by Python's iteration protocols (`__iter__`, `__len__`). Bridge is implemented through composition and interfaces (ABCs or duck typing). The key is understanding the intent of each pattern and applying it correctly to the problem at hand. The best developers know when to use a pattern and when to keep the code simple.

```python
# Summary: Three patterns, three purposes
# Decorator — extends behavior
@log_execution
@cache_result
def compute(n):
    return sum(range(n))

# Composite — represents tree
class TreeNode:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []

# Bridge — separates abstraction from implementation
class Abstraction:
    def __init__(self, impl):
        self._impl = impl
    def operation(self):
        return self._impl.implement()
```
