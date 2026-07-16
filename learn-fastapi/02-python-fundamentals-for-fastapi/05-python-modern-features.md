# Python Modern Features Relevant to FastAPI

## Table of Contents

1. [match/case (Python 3.10+)](#matchcase-python-310)
2. [Structural Pattern Matching](#structural-pattern-matching)
3. [Dataclasses](#dataclasses)
4. [attrs](#attrs)
5. [__slots__](#slots)
6. [Walrus Operator (:=)](#walrus-operator)
7. [F-Strings](#f-strings)
8. [Type Unions with |](#type-unions-with)
9. [ParamSpec and TypeVarTuple](#paramspec-and-typevartuple)
10. [Python 3.12 Type Parameter Syntax](#python-312-type-parameter-syntax)
11. [Python 3.13 Features](#python-313-features)
12. [Interview Questions](#interview-questions)

---

## match/case (Python 3.10+)

### Basic Syntax

```python
# match/case is Python's version of switch/case but more powerful
# It performs structural pattern matching

def handle_http_status(status: int) -> str:
    match status:
        case 200:
            return "OK"
        case 201:
            return "Created"
        case 400:
            return "Bad Request"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:  # Wildcard - matches anything
            return f"Unknown status: {status}"

# Multiple values in one case
def handle_status(status: int) -> str:
    match status:
        case 200 | 201 | 202:
            return "Success"
        case 400 | 401 | 403:
            return "Client Error"
        case 500 | 502 | 503:
            return "Server Error"
        case _:
            return "Unknown"

# Guards (additional conditions)
def classify_number(n: int) -> str:
    match n:
        case n if n < 0:
            return "negative"
        case 0:
            return "zero"
        case n if n % 2 == 0:
            return "positive even"
        case _:
            return "positive odd"
```

### Pattern Matching with Variables

```python
# Variable capture
def process_command(command: str):
    match command.split():
        case ["quit"]:
            return "Exiting..."
        case ["hello", name]:
            return f"Hello, {name}!"
        case ["add", *numbers]:
            return sum(int(n) for n in numbers)
        case ["delete", item] if item in valid_items:
            return f"Deleted {item}"
        case _:
            return "Unknown command"

# Named capture groups
def parse_url(url: str):
    match url.split("/"):
        case ["https:", "", domain, *path]:
            return {"domain": domain, "path": path}
        case ["http:", "", domain, *path]:
            return {"domain": domain, "path": path}
        case _:
            return None
```

### Pattern Matching with Classes

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

@dataclass
class Circle:
    center: Point
    radius: float

@dataclass
class Rectangle:
    top_left: Point
    bottom_right: Point

def describe_shape(shape) -> str:
    match shape:
        case Circle(center=Point(x=0, y=0), radius=r):
            return f"Circle centered at origin with radius {r}"
        case Circle(center=Point(x=x, y=y), radius=r):
            return f"Circle at ({x}, {y}) with radius {r}"
        case Rectangle(top_left=Point(x=x1, y=y1), bottom_right=Point(x=x2, y=y2)):
            width = x2 - x1
            height = y2 - y1
            return f"Rectangle {width}x{height}"
        case _:
            return "Unknown shape"

# Usage
shape = Circle(center=Point(0, 0), radius=5)
print(describe_shape(shape))  # "Circle centered at origin with radius 5"
```

### match/case in FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class WebhookEvent(BaseModel):
    type: str
    data: dict

@app.post("/webhook")
async def handle_webhook(event: WebhookEvent):
    match event.type:
        case "user.created":
            return await handle_user_created(event.data)
        case "user.updated":
            return await handle_user_updated(event.data)
        case "user.deleted":
            return await handle_user_deleted(event.data)
        case "payment.completed":
            return await handle_payment(event.data)
        case _:
            return {"status": "ignored", "type": event.type}
```

---

## Structural Pattern Matching

### Matching Sequences

```python
# List matching
def process_list(items: list) -> str:
    match items:
        case []:
            return "Empty list"
        case [single]:
            return f"Single item: {single}"
        case [first, second]:
            return f"Two items: {first}, {second}"
        case [first, *rest]:
            return f"First: {first}, rest: {rest}"

# Tuple matching
def process_point(point: tuple) -> str:
    match point:
        case (0, 0):
            return "Origin"
        case (x, 0):
            return f"On x-axis at {x}"
        case (0, y):
            return f"On y-axis at {y}"
        case (x, y):
            return f"Point at ({x}, {y})"

# Nested sequences
def process_nested(data: list) -> str:
    match data:
        case [1, [2, 3]]:
            return "Nested pattern matched"
        case [x, [y, z]] if x == y + z:
            return f"Sum match: {x} = {y} + {z}"
        case _:
            return "No match"
```

### Matching Mappings (Dicts)

```python
# Dict matching
def process_config(config: dict) -> str:
    match config:
        case {"debug": True, "level": level}:
            return f"Debug mode at level {level}"
        case {"mode": "production", "workers": n} if n > 1:
            return f"Production with {n} workers"
        case {"mode": mode, **rest}:
            return f"Mode: {mode}, extra: {rest}"

# API request matching
def handle_api_request(request: dict) -> str:
    match request:
        case {"method": "GET", "path": path}:
            return f"GET {path}"
        case {"method": "POST", "path": path, "body": body}:
            return f"POST {path} with {len(body)} bytes"
        case {"method": "DELETE", "path": path}:
            return f"DELETE {path}"
        case _:
            return "Unknown request"
```

### Matching Objects

```python
from dataclasses import dataclass
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"

@dataclass
class User:
    name: str
    email: str
    status: Status
    age: int

def describe_user(user: User) -> str:
    match user:
        case User(name=name, status=Status.ACTIVE, age=age) if age >= 18:
            return f"Active adult: {name}"
        case User(name=name, status=Status.ACTIVE, age=age):
            return f"Active minor: {name}"
        case User(name=name, status=Status.PENDING):
            return f"Pending user: {name}"
        case User(name=name, status=Status.INACTIVE):
            return f"Inactive user: {name}"
        case _:
            return "Unknown user"

# Usage
user = User(name="Alice", email="alice@example.com", status=Status.ACTIVE, age=25)
print(describe_user(user))  # "Active adult: Alice"
```

---

## Dataclasses

### Basic Dataclasses

```python
from dataclasses import dataclass, field
from typing import ClassVar

# Basic dataclass
@dataclass
class User:
    name: str
    email: str
    age: int
    tags: list[str] = field(default_factory=list)

# Auto-generates __init__, __repr__, __eq__
user = User(name="Alice", email="alice@example.com", age=30)
print(user)  # User(name='Alice', email='alice@example.com', age=30, tags=[])

# With defaults
@dataclass
class Config:
    host: str = "localhost"
    port: int = 8000
    debug: bool = False

# With field options
@dataclass
class Product:
    name: str
    price: float
    description: str = field(default="", repr=False)  # Exclude from repr
    id: int = field(init=False)  # Not in __init__, set in __post_init__
    created_at: ClassVar[str] = "2024-01-01"  # Class variable, not field

    def __post_init__(self):
        self.id = hash(self.name) % 10000
```

### Frozen Dataclasses

```python
# Frozen dataclasses are immutable
@dataclass(frozen=True)
class Point:
    x: float
    y: float

point = Point(1.0, 2.0)
# point.x = 3.0  # AttributeError: cannot assign to field 'x'

# Can be used as dict keys
points = {Point(1, 2): "first", Point(3, 4): "second"}

# Can be used in sets
point_set = {Point(1, 2), Point(3, 4), Point(1, 2)}  # Duplicate removed

# Hash is auto-generated
print(hash(Point(1, 2)))

# With slots (Python 3.10+)
@dataclass(frozen=True, slots=True)
class OptimizedPoint:
    x: float
    y: float

# slots=True:
# - Uses __slots__ instead of __dict__
# - Less memory usage
# - Faster attribute access
# - Required for frozen dataclasses to work properly
```

### Dataclass Performance

```python
import time
from dataclasses import dataclass
from pydantic import BaseModel

# Dataclass vs Pydantic performance
@dataclass
class UserDC:
    name: str
    age: int
    email: str

class UserPydantic(BaseModel):
    name: str
    age: int
    email: str

# Creation performance
start = time.perf_counter()
for _ in range(100000):
    UserDC(name="Alice", age=30, email="alice@example.com")
dc_time = time.perf_counter() - start

start = time.perf_counter()
for _ in range(100000):
    UserPydantic(name="Alice", age=30, email="alice@example.com")
pydantic_time = time.perf_counter() - start

print(f"Dataclass: {dc_time:.3f}s")
print(f"Pydantic: {pydantic_time:.3f}s")
# Dataclass is typically 5-10x faster for creation
# But Pydantic provides validation, serialization, etc.
```

### Dataclasses in FastAPI

```python
from fastapi import FastAPI
from dataclasses import dataclass
from typing import AsyncGenerator

app = FastAPI()

# Dataclass as response model (limited support)
@dataclass
class UserResponse:
    name: str
    email: str
    age: int

# FastAPI works better with Pydantic models
# But you can use dataclasses with some configuration

# Better: Use Pydantic dataclasses
from pydantic import dataclasses as pydantic_dataclasses

@pydantic_dataclasses.dataclass
class UserPydanticDC:
    name: str
    email: str
    age: int

    def __post_init_post_parse__(self):
        # Pydantic validation happens here
        if self.age < 0:
            raise ValueError("Age cannot be negative")

@app.get("/user")
async def get_user() -> UserPydanticDC:
    return UserPydanticDC(name="Alice", email="alice@example.com", age=30)
```

---

## attrs

### Basic attrs Usage

```python
import attr
from attrs import validators

# attrs provides more features than dataclasses
@attr.s(auto_attribs=True, slots=True, frozen=True)
class User:
    name: str
    email: str
    age: int = attr.ib(validator=[validators.gt(0), validators.lt(150)])
    tags: list[str] = attr.Factory(list)

# Validation is automatic
user = User(name="Alice", email="alice@example.com", age=30)
# User(name="Alice", email="alice@example.com", age=-1)  # ValidationError

# Custom validators
def validate_email(instance, attribute, value):
    if "@" not in value:
        raise ValueError(f"Invalid email: {value}")

@attr.s(auto_attribs=True)
class ValidatedUser:
    name: str
    email: str = attr.ib(validator=validate_email)

# Converter
@attr.s(auto_attribs=True)
class ConvertedUser:
    name: str
    age: int = attr.ib(converter=int)

user = ConvertedUser(name="Alice", age="30")  # age is converted to int
```

### attrs vs Dataclasses

```python
# attrs advantages:
# 1. More validation options
# 2. Custom converters
# 3. Better performance (with C extension)
# 4. More decorators and utilities
# 5. Better frozen support

# Dataclass advantages:
# 1. Built into Python (no dependency)
# 2. Simpler API
# 3. More standard in the community

# When to use which:
# - Use dataclasses for simple data containers
# - Use attrs when you need validation or complex features
# - Use Pydantic for API models (FastAPI integration)
```

---

## __slots__

### What is __slots__

```python
# __slots__ restricts instance attributes to a fixed set
# Reduces memory usage and improves attribute access speed

class WithoutSlots:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class WithSlots:
    __slots__ = ('x', 'y')

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

# Memory comparison
import sys

without = WithoutSlots(1, 2)
with_slots = WithSlots(1, 2)

print(sys.getsizeof(without.__dict__))  # ~232 bytes
print(hasattr(with_slots, '__dict__'))   # False - no __dict__!

# Performance comparison
import timeit

without_time = timeit.timeit(
    "obj.x",
    setup="obj = WithoutSlots(1, 2)",
    globals=globals(),
    number=1000000,
)

with_slots_time = timeit.timeit(
    "obj.x",
    setup="obj = WithSlots(1, 2)",
    globals=globals(),
    number=1000000,
)

print(f"Without slots: {without_time:.3f}s")
print(f"With slots: {with_slots_time:.3f}s")
# With slots is typically 10-20% faster
```

### Slots with Pydantic

```python
from pydantic import BaseModel, ConfigDict

# Pydantic V2 supports slots
class SlottedModel(BaseModel):
    model_config = ConfigDict(
        slots=True,  # Python 3.10+
        frozen=True,  # Immutable
    )

    name: str
    age: int

# Benefits:
# - Less memory per instance
# - Faster attribute access
# - Prevents accidental attribute creation
# - Works with Pydantic validation
```

---

## Walrus Operator (:=)

### Basic Usage

```python
# Walrus operator assigns and returns in one expression

# Before walrus operator
data = get_data()
if data:
    process(data)

# With walrus operator
if data := get_data():
    process(data)

# In while loops
while chunk := file.read(8192):
    process(chunk)

# In list comprehensions
results = [y for x in data if (y := expensive_func(x)) is not None]

# In if conditions
if (n := len(data)) > 10:
    print(f"List is too long: {n} elements")
```

### Walrus in FastAPI

```python
from fastapi import FastAPI, Query

app = FastAPI()

# Walrus operator in validation
@app.get("/search")
async def search(
    q: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
):
    if query := q:  # Assign and check
        results = await search_database(query, page)
        return {"query": query, "results": results}
    return {"query": None, "results": []}

# Walrus in dependencies
async def get_current_user(token: str | None = Depends(oauth2_scheme)):
    if user := await verify_token(token):
        return user
    raise HTTPException(status_code=401)

# Walrus in response processing
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item := await fetch_item(item_id):
        return item
    raise HTTPException(status_code=404)
```

### Walrus Best Practices

```python
# GOOD: Clear intent
if user := await get_user(user_id):
    process(user)

# GOOD: Reducing function calls
if n := len(data) > 100:
    paginate(data)

# BAD: Obscuring code
if (result := (await process(await get_data()))).is_valid:
    save(result)

# GOOD: Clearer version
data = await get_data()
result = await process(data)
if result.is_valid:
    save(result)

# Rule of thumb: Use walrus when it improves readability
# Don't use it just to save a line of code
```

---

## F-Strings

### Advanced F-String Features

```python
# Basic formatting
name = "Alice"
age = 30
print(f"Name: {name}, Age: {age}")

# Expressions
print(f"Name: {name.upper()}, Age: {age * 2}")

# Format specifications
pi = 3.14159265
print(f"Pi: {pi:.2f}")           # Pi: 3.14
print(f"Pi: {pi:10.2f}")         # Pi:       3.14
print(f"Pi: {pi:010.2f}")        # Pi: 0000003.14

# Alignment
name = "Alice"
print(f"{name:<20}")             # Left aligned
print(f"{name:>20}")             # Right aligned
print(f"{name:^20}")             # Center aligned
print(f"{name:*^20}")            # Center with fill char

# Numbers
print(f"{1000000:,}")            # 1,000,000
print(f"{0.25:.0%}")             # 25%
print(f"{1000:b}")               # 1111101000 (binary)
print(f"{255:x}")                # ff (hex)
print(f"{255:#x}")               # 0xff

# Debugging (Python 3.8+)
name = "Alice"
age = 30
print(f"{name=}, {age=}")        # name='Alice', age=30
print(f"{name.upper()=}")        # name.upper()='ALICE'
```

### F-Strings in FastAPI

```python
from fastapi import FastAPI
import time

app = FastAPI()

# Dynamic query building
@app.get("/users")
async def list_users(
    name: str | None = None,
    age: int | None = None,
    role: str | None = None,
):
    conditions = []
    params = {}

    if name:
        conditions.append(f"name ILIKE :name")
        params["name"] = f"%{name}%"
    if age:
        conditions.append(f"age = :age")
        params["age"] = age
    if role:
        conditions.append(f"role = :role")
        params["role"] = role

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    query = f"SELECT * FROM users {where_clause}"

    return {"query": query, "params": params}

# Error messages with f-strings
class ValidationError(Exception):
    def __init__(self, field: str, value: any, reason: str):
        self.field = field
        self.value = value
        self.reason = reason
        super().__init__(
            f"Validation error on field '{field}': "
            f"value '{value}' is invalid because {reason}"
        )
```

---

## Type Unions with |

### Modern Union Syntax

```python
# Python 3.10+ union syntax
def process(value: int | str) -> str:
    if isinstance(value, int):
        return f"Number: {value}"
    return f"String: {value}"

# Multiple types
def handle_data(data: int | str | list[int] | None) -> str:
    if data is None:
        return "No data"
    if isinstance(data, int):
        return f"Number: {data}"
    if isinstance(data, str):
        return f"String: {data}"
    return f"List of {len(data)} items"

# With isinstance
def validate_input(value: str | int | float) -> bool:
    return isinstance(value, (str, int, float))

# In Pydantic/FastAPI
from pydantic import BaseModel

class FlexibleModel(BaseModel):
    value: int | str | None = None
    data: list[int] | list[str] | None = None

@app.post("/flexible")
async def flexible_endpoint(data: FlexibleModel):
    return {"received": data.value}
```

### Union vs Optional

```python
# They are equivalent:
def a(x: int | None) -> None: ...    # Python 3.10+
def b(x: Optional[int]) -> None: ...  # typing module
def c(x: Union[int, None]) -> None: ...  # typing module

# Prefer | syntax in Python 3.10+
# It's cleaner and more Pythonic

# But be careful with complex types:
# This is NOT a union:
# x: int | str | None  # This is (int | str) | None

# Python evaluates | left-to-right:
# int | str | None  ->  (int | str) | None
# Which is equivalent to Union[int, str, None]
```

---

## ParamSpec and TypeVarTuple

### ParamSpec (PEP 612)

```python
from typing import ParamSpec, TypeVar, Callable

P = ParamSpec("P")
R = TypeVar("R")

# Preserve function signatures in decorators
def retry(max_attempts: int = 3):
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
        return wrapper
    return decorator

@retry(max_attempts=3)
def fetch_data(url: str, timeout: int = 10) -> dict:
    ...

# mypy knows fetch_data still has signature (url: str, timeout: int = 10) -> dict
```

### TypeVarTuple (PEP 646)

```python
from typing import TypeVarTuple, TypeVar, Generic

Ts = TypeVarTuple("Ts")

# Variadic generics
class Array(Generic[*Ts]):
    def __init__(self, shape: tuple[*Ts]) -> None:
        self.shape = shape

# Usage
arr_2d: Array[int, int] = Array((10, 20))
arr_3d: Array[int, int, int] = Array((10, 20, 30))
```

---

## Python 3.12 Type Parameter Syntax

### New Type Syntax

```python
# Python 3.12 introduces new type parameter syntax
# No more TypeVar needed!

# Old syntax (Python 3.11-)
from typing import TypeVar, Generic

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

class OldGeneric(Generic[T, K, V]):
    def __init__(self, items: list[T]) -> None:
        self.items = items

# New syntax (Python 3.12+)
class NewGeneric[T, K, V]:
    def __init__(self, items: list[T]) -> None:
        self.items = items

# Type aliases
type Point = tuple[float, float]
type Vector = list[float]
type Matrix = list[Vector]

# Generic functions
def first[T](items: list[T]) -> T | None:
    if items:
        return items[0]
    return None

# Constrained types
def double[T: (int, float)](value: T) -> T:
    return value * 2

# Bounded types
from collections.abc import Comparable
def max_value[T: Comparable](items: list[T]) -> T:
    return max(items)
```

### Python 3.12 in FastAPI

```python
from fastapi import FastAPI

app = FastAPI()

# Generic response model with new syntax
class ApiResponse[T]:
    success: bool
    data: T | None = None
    error: str | None = None

class PaginatedResponse[T]:
    items: list[T]
    total: int
    page: int

@app.get("/users")
async def list_users() -> PaginatedResponse[User]:
    return PaginatedResponse(
        items=[User(name="Alice", age=30)],
        total=1,
        page=1,
    )

@app.get("/item/{item_id}")
async def get_item(item_id: int) -> ApiResponse[Item]:
    item = await fetch_item(item_id)
    if item:
        return ApiResponse(success=True, data=item)
    return ApiResponse(success=False, error="Not found")
```

---

## Python 3.13 Features

### Key Python 3.13 Features

```python
# 1. Improved error messages
# Better suggestions for common mistakes
# "Did you mean 'print'?" when you misspell print

# 2. Per-interpreter GIL (PEP 684)
# Each sub-interpreter can have its own GIL
# Enables true parallelism for CPU-bound tasks
import _interpreters

# 3. Improved asyncio
# Better TaskGroup, improved exception handling

# 4. Type parameter syntax improvements
# More flexible generic types

# 5. Performance improvements
# Faster startup, better memory usage

# 6. Deprecation warnings
# Many deprecated features now raise errors
```

### Python 3.13 in FastAPI Context

```python
# Python 3.13 improvements relevant to FastAPI:

# 1. Better error messages help debugging
# More helpful tracebacks for async code

# 2. Per-interpreter GIL enables better concurrency
# Multiple interpreters in same process

# 3. Performance improvements
# Faster startup time for FastAPI apps
# Better memory management

# 4. Type system improvements
# More expressive type hints
# Better generic support

# Example: Using Python 3.13 features
from typing import TypeVarTuple, TypeVar

# Variadic generics (PEP 646)
Ts = TypeVarTuple("Ts")

class Tensor:
    shape: tuple[*Ts]

# Better error messages
async def example():
    # Python 3.13 gives better suggestions
    # if you make common mistakes
    pass
```

---

## Interview Questions

### Q1: What is structural pattern matching?

**Answer:** Structural pattern matching (match/case) is Python's version of switch/case but much more powerful. It matches patterns against data structures, not just values. It supports matching sequences, mappings, objects, and can include guards (conditions). It's useful for handling different data shapes cleanly.

### Q2: What are dataclasses and when should you use them?

**Answer:** Dataclasses (PEP 555) automatically generate `__init__`, `__repr__`, `__eq__`, and other methods. Use them for simple data containers. For API models with validation, use Pydantic. For immutable data, use `frozen=True`. For better performance, use `slots=True`.

### Q3: What is the walrus operator?

**Answer:** The walrus operator `:=` assigns a value and returns it in one expression. It's useful in while loops (`while chunk := read():`), if conditions (`if user := get_user():`), and list comprehensions. It reduces redundant code but should be used sparingly for readability.

### Q4: What is the difference between `int | None` and `Optional[int]`?

**Answer:** They are semantically identical. `int | None` is Python 3.10+ syntax, while `Optional[int]` is from the `typing` module. `int | None` is preferred for readability. Both tell type checkers the value can be `int` or `None`.

### Q5: What are __slots__ and why use them?

**Answer:** `__slots__` restricts instance attributes to a fixed set, reducing memory usage and improving attribute access speed. Use them for classes with many instances (like data objects). They prevent accidental attribute creation but make classes less flexible (no dynamic attributes).

### Q6: What is the difference between dataclasses and attrs?

**Answer:** Dataclasses are built into Python (3.7+) and simpler. attrs provides more features: better validation, converters, decorators, and performance (with C extension). Use dataclasses for simple containers, attrs for complex validation needs. For FastAPI, Pydantic is usually best.

### Q7: What is Python 3.12's new type parameter syntax?

**Answer:** Python 3.12 allows defining type parameters directly in class/function definitions: `class List[T]:` instead of `T = TypeVar("T"); class List(Generic[T]):`. It also introduces `type` keyword for type aliases: `type Point = tuple[float, float]`.

### Q8: What are f-strings and why are they preferred?

**Answer:** F-strings (formatted string literals) provide readable string interpolation: `f"Hello, {name}"`. They're faster than `.format()` and `%` formatting, more readable, and support expressions. Python 3.12 adds multi-line f-strings and f-string debugging (`f"{name=}"`).

### Q9: What is the difference between `match/case` and `if/elif`?

**Answer:** `match/case` performs structural pattern matching, while `if/elif` checks conditions. `match/case` can destructure data, match patterns, and use guards. It's more powerful for complex data shapes but simpler for basic value comparisons.

### Q10: What is ParamSpec used for?

**Answer:** `ParamSpec` (PEP 612) preserves function signatures in decorators. Without it, decorators lose type information. `ParamSpec` captures parameter types so mypy/pyright can verify calls to decorated functions.

### Q11: What is TypeVarTuple?

**Answer:** `TypeVarTuple` (PEP 646) enables variadic generics - types with variable number of type parameters. It's used for tensor shapes, arrays with dynamic dimensions, and other cases where the number of type parameters varies.

### Q12: What are the benefits of Python 3.13 for FastAPI?

**Answer:** Python 3.13 offers: (1) Better error messages for debugging, (2) Per-interpreter GIL for true parallelism, (3) Performance improvements (faster startup, better memory), (4) Improved type system, (5) Better asyncio support.

### Q13: When should you use frozen dataclasses?

**Answer:** Use frozen dataclasses when you need immutable data objects. They're hashable (can be dict keys or set members), thread-safe, and prevent accidental modification. Use for value objects, configuration, or any data that shouldn't change.

### Q14: What is the difference between `__slots__` and regular classes?

**Answer:** Classes with `__slots__` use fixed-size storage instead of a dict for attributes. Benefits: less memory (no per-instance dict), faster attribute access, prevents dynamic attribute creation. Drawbacks: can't add new attributes, inheritance is more complex.

### Q15: How do you use pattern matching in FastAPI?

**Answer:** Pattern matching is useful for handling different request types, webhook events, or API responses. Example: match different webhook event types and route to appropriate handlers. It's cleaner than multiple if/elif chains for complex data shapes.
