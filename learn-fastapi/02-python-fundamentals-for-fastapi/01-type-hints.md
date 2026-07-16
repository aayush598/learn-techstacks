# Python Type Hints Deep Dive for FastAPI

## Table of Contents

1. [Why Type Hints Matter](#why-type-hints-matter)
2. [Basic Types](#basic-types)
3. [Complex Types](#complex-types)
4. [Optional and Union](#optional-and-union)
5. [Generic Types and TypeVar](#generic-types-and-typevar)
6. [TypeAlias](#typealias)
7. [Annotated (PEP 593)](#annotated-pep-593)
8. [ParamSpec and TypeVarTuple (PEP 646)](#paramspec-and-typevartuple-pep-646)
9. [Final and ClassVar](#final-and-classvar)
10. [NewType](#newtype)
11. [Runtime Type Checking Limitations](#runtime-type-checking-limitations)
12. [Type Hints Best Practices for FastAPI](#type-hints-best-practices-for-fastapi)
13. [Interview Questions](#interview-questions)

---

## Why Type Hints Matter

Type hints were introduced in Python 3.5 (PEP 484) and have evolved significantly.
They serve three primary purposes:

### 1. Static Type Checking

```python
# Without type hints - errors found only at runtime
def add(a, b):
    return a + b

result = add("hello", 5)  # TypeError at runtime

# With type hints - errors caught by tools like mypy/pyright
def add(a: int, b: int) -> int:
    return a + b

result = add("hello", 5)  # mypy catches this: Argument 1 has incompatible type "str"; expected "int"
```

### 2. IDE Autocompletion and Documentation

```python
class UserService:
    def get_user(self, user_id: int) -> dict[str, str]:
        """
        Returns user dictionary with keys: name, email, role.
        IDE knows return type is dict[str, str] and offers
        appropriate autocompletion.
        """
        ...
```

### 3. Runtime Behavior in FastAPI

FastAPI uses type hints at **runtime** to:
- Validate incoming request data via Pydantic
- Generate OpenAPI documentation automatically
- Perform data serialization/deserialization
- Apply dependency injection based on type annotations

```python
from fastapi import FastAPI

app = FastAPI()

# FastAPI uses type hints at RUNTIME to:
# 1. Parse `user_id` from path as int
# 2. Validate `q` is Optional[str]
# 3. Generate OpenAPI schema
@app.get("/items/{user_id}")
async def read_items(user_id: int, q: str | None = None):
    return {"user_id": user_id, "q": q}
```

---

## Basic Types

### Primitive Types

```python
# int - whole numbers
age: int = 25
big_number: int = 10**18

# str - string text
name: str = "FastAPI"
empty: str = ""

# float - floating point numbers
price: float = 19.99
pi: float = 3.14159

# bool - boolean values
is_active: bool = True
has_permission: bool = False

# None - absence of value
result: None = None
```

### Type Hints with Literal Values

```python
from typing import Literal

# Restrict to specific literal values
direction: Literal["north", "south", "east", "west"] = "north"
status_code: Literal[200, 201, 400, 404, 500] = 200
mode: Literal[True] = True  # Literal can also be bool

# In FastAPI - restrict query parameter values
from fastapi import Query

@app.get("/search")
async def search(
    sort_by: Literal["name", "date", "price"] = "date",
    order: Literal["asc", "desc"] = "asc",
):
    return {"sort_by": sort_by, "order": order}
```

### Bytes and Bytearray

```python
data: bytes = b"binary data"
buffer: bytearray = bytearray(b"mutable binary")

# In FastAPI - file upload handling
from fastapi import UploadFile

@app.post("/upload")
async def upload_file(file: UploadFile):
    contents: bytes = await file.read()
    return {"size": len(contents)}
```

---

## Complex Types

### List, Tuple, Set, FrozenSet

```python
from typing import List, Tuple, Set, FrozenSet, Dict
from collections.abc import Sequence, Iterable

# List - ordered, mutable sequence
numbers: list[int] = [1, 2, 3, 4, 5]
names: list[str] = ["Alice", "Bob", "Charlie"]

# Python 3.9+ syntax (preferred over typing.List)
scores: list[float] = [98.5, 87.3, 92.1]

# Tuple - ordered, immutable sequence
# Fixed length tuple
point: tuple[int, int] = (10, 20)
rgb_color: tuple[int, int, int] = (255, 128, 0)

# Variable length tuple
numbers: tuple[int, ...] = (1, 2, 3, 4, 5)

# Set - unordered, unique elements
unique_ids: set[int] = {1, 2, 3, 4, 5}
tags: set[str] = {"python", "fastapi", "async"}

# FrozenSet - immutable set
immutable_tags: frozenset[str] = frozenset({"python", "fastapi"})

# Sequence - abstract type (accepts list, tuple, etc.)
def process_items(items: Sequence[str]) -> str:
    return ", ".join(items)

# In FastAPI - query parameters with lists
from fastapi import Query

@app.get("/filter")
async def filter_items(
    tags: list[str] = Query(default=[], description="Filter by tags"),
    ids: list[int] = Query(default=[], description="Filter by IDs"),
):
    return {"tags": tags, "ids": ids}
```

### Dict and Mapping

```python
from typing import Dict, Mapping

# Dict - key-value pairs
user_scores: dict[str, int] = {"alice": 95, "bob": 87}
config: dict[str, bool | str] = {"debug": True, "log_level": "info"}

# Nested dict
user_data: dict[str, dict[str, int | str]] = {
    "user1": {"name": "Alice", "age": 30},
    "user2": {"name": "Bob", "age": 25},
}

# Mapping - read-only dict interface
def process_config(config: Mapping[str, str | int]) -> None:
    for key, value in config.items():
        print(f"{key}: {value}")

# In FastAPI - response models
from pydantic import BaseModel

class UserResponse(BaseModel):
    name: str
    metadata: dict[str, str | int]

@app.get("/user/{user_id}")
async def get_user(user_id: int) -> UserResponse:
    return UserResponse(
        name="Alice",
        metadata={"role": "admin", "level": 5}
    )
```

### Callable

```python
from typing import Callable

# Simple callable
def process(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# Callable with no arguments
def run_on_startup(func: Callable[[], None]) -> Callable[[], None]:
    print("Running startup task...")
    func()
    return func

# Callable with any arguments
def decorator(func: Callable[..., None]) -> Callable[..., None]:
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# In FastAPI - middleware and dependencies
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next: Callable) -> None:
    response = await call_next(request)
    return response
```

---

## Optional and Union

### Optional

```python
from typing import Optional

# Optional[X] is equivalent to Union[X, None]
def find_user(user_id: int) -> Optional[dict]:
    if user_id == 1:
        return {"name": "Alice"}
    return None

# Python 3.10+ syntax (preferred)
def find_user(user_id: int) -> dict | None:
    if user_id == 1:
        return {"name": "Alice"}
    return None

# In FastAPI - optional query parameters
@app.get("/users")
async def get_users(
    name: str | None = None,      # Optional query param
    age: int | None = None,       # Optional query param
    search: str | None = Query(default=None, max_length=50),
):
    filters = {}
    if name is not None:
        filters["name"] = name
    if age is not None:
        filters["age"] = age
    return filters
```

### Union

```python
from typing import Union

# Union - value can be one of several types
def process_value(value: int | str) -> str:
    if isinstance(value, int):
        return f"Number: {value}"
    return f"String: {value}"

# Union with more than 2 types
response_data: dict[str, int | str | bool | list[str]] = {
    "count": 42,
    "status": "active",
    "verified": True,
    "tags": ["important"],
}

# Discriminated unions in Pydantic (FastAPI uses this)
from pydantic import BaseModel

class Cat(BaseModel):
    type: Literal["cat"]
    meow_volume: int

class Dog(BaseModel):
    type: Literal["dog"]
    bark_volume: int

# FastAPI can handle this with discriminated unions
from typing import Annotated
from fastapi import Form

# In FastAPI - form data with Union
@app.post("/pet")
async def create_pet(pet: Cat | Dog):
    if pet.type == "cat":
        return {"message": f"Cat meows at volume {pet.meow_volume}"}
    return {"message": f"Dog barks at volume {pet.bark_volume}"}
```

### Never and NoReturn

```python
from typing import Never, NoReturn

# NoReturn - function never returns (always raises exception)
def raise_error(message: str) -> Never:
    raise ValueError(message)

# Never (Python 3.11+) - same as NoReturn but more explicit
def crash() -> Never:
    raise RuntimeError("Fatal error")

# Useful in type narrowing
def process(status: str) -> str:
    if status == "ok":
        return "success"
    elif status == "error":
        raise ValueError("Error occurred")
    else:
        # mypy knows this branch is unreachable
        reveal_type(status)  # Never
```

---

## Generic Types and TypeVar

### Basic TypeVar

```python
from typing import TypeVar, Generic

T = TypeVar("T")

# Generic function
def first_element(items: list[T]) -> T | None:
    if items:
        return items[0]
    return None

# TypeVar with constraints - can only be one of these types
NumberOrString = TypeVar("NumberOrString", int, str)

def double(value: NumberOrString) -> NumberOrString:
    if isinstance(value, int):
        return value * 2
    return value * 2

# TypeVar with bounds - must be subclass of specified type
from abc import ABC

class Animal(ABC):
    name: str

AnimalType = TypeVar("AnimalType", bound=Animal)

def get_name(animal: AnimalType) -> str:
    return animal.name
```

### Generic Classes

```python
from typing import TypeVar, Generic, Sequence

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

# Generic repository pattern
class Repository(Generic[T]):
    def __init__(self, items: list[T]) -> None:
        self._items = items

    def get(self, index: int) -> T:
        return self._items[index]

    def add(self, item: T) -> None:
        self._items.append(item)

    def find(self, predicate: Callable[[T], bool]) -> T | None:
        for item in self._items:
            if predicate(item):
                return item
        return None

    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        return [item for item in self._items if predicate(item)]

# Usage
user_repo = Repository[User]([user1, user2, user3])
product_repo = Repository[Product]([product1, product2])

# Generic key-value store
class KeyValueStore(Generic[K, V]):
    def __init__(self) -> None:
        self._store: dict[K, V] = {}

    def get(self, key: K) -> V | None:
        return self._store.get(key)

    def set(self, key: K, value: V) -> None:
        self._store[key] = value

# In FastAPI - generic response models
from pydantic import BaseModel

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    per_page: int

class User(BaseModel):
    name: str
    email: str

@app.get("/users")
async def list_users() -> PaginatedResponse[User]:
    return PaginatedResponse(
        items=[User(name="Alice", email="alice@example.com")],
        total=1,
        page=1,
        per_page=10,
    )
```

### Constrained TypeVar

```python
from typing import TypeVar

# Constrained to specific types
AnyStr = TypeVar("AnyStr", str, bytes)

def concat(a: AnyStr, b: AnyStr) -> AnyStr:
    return a + b

# Multiple type parameters with constraints
Sortable = TypeVar("Sortable", int, float, str)

def sort_items(items: list[Sortable]) -> list[Sortable]:
    return sorted(items)

# Using TypeVar in Pydantic models
from pydantic import BaseModel

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    data: T
    message: str = "success"

class ErrorResponse(BaseModel):
    error: str
    code: int

# FastAPI endpoint returning either success or error
@app.get("/item/{item_id}")
async def get_item(item_id: int) -> SuccessResponse[Item] | ErrorResponse:
    item = find_item(item_id)
    if item:
        return SuccessResponse(data=item)
    return ErrorResponse(error="Not found", code=404)
```

---

## TypeAlias

```python
from typing import TypeAlias

# Clear type aliases for complex types
Vector: TypeAlias = list[float]
Matrix: TypeAlias = list[Vector]
UserDict: TypeAlias = dict[str, dict[str, int | str]]
IntOrStr: TypeAlias = int | str

# Python 3.12+ syntax
type Vector = list[float]
type Matrix = list[Vector]
type UserDict = dict[str, dict[str, int | str]]

# Using TypeAlias in functions
def dot_product(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))

def matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    # Matrix multiplication logic
    ...

# In FastAPI - type aliases for complex response types
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str

class UserWithAddress(BaseModel):
    name: str
    address: Address

# Type alias for complex query parameters
FilterParams: TypeAlias = dict[str, str | int | bool | list[str]]

@app.get("/users")
async def get_users(filters: FilterParams = Depends(get_filters)):
    return {"filters": filters}
```

---

## Annotated (PEP 593)

```python
from typing import Annotated
from pydantic import Field

# Annotated adds metadata to types
# Basic Annotated usage
Name = Annotated[str, Field(min_length=1, max_length=100)]
Age = Annotated[int, Field(ge=0, le=150)]
Email = Annotated[str, Field(pattern=r"^[\w.-]+@[\w.-]+\.\w+$")]

# Using Annotated in functions
def create_user(name: Name, age: Age, email: Email) -> dict:
    return {"name": name, "age": age, "email": email}

# In FastAPI - Annotated is the RECOMMENDED way to add validation
from fastapi import Query, Path, Body, Header, Cookie

@app.get("/users/{user_id}")
async def get_user(
    user_id: Annotated[int, Path(ge=1, description="User ID")],
    q: Annotated[str | None, Query(max_length=50)] = None,
    accept_language: Annotated[str | None, Header()] = None,
    session: str | None = Cookie(default=None),
) -> User:
    ...

# Annotated with multiple metadata
PositiveInt = Annotated[int, Field(ge=1), Field(description="Must be positive")]
RestrictedStr = Annotated[
    str,
    Field(min_length=1),
    Field(max_length=100),
    Field(pattern=r"^[a-zA-Z]+$"),
]

# Annotated in Pydantic models
class Product(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=200)]
    price: Annotated[float, Field(ge=0.01, le=1000000)]
    tags: Annotated[list[str], Field(max_length=10)]
    description: Annotated[str | None, Field(default=None, max_length=5000)]
```

---

## ParamSpec and TypeVarTuple (PEP 646)

### ParamSpec (PEP 612)

```python
from typing import ParamSpec, TypeVar, Callable

P = ParamSpec("P")
R = TypeVar("R")

# Preserves function signature in decorators
def log_execution(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_execution
def add(a: int, b: int) -> int:
    return a + b

# mypy knows add still has signature (a: int, b: int) -> int
add(1, 2)      # OK
add("1", "2")  # mypy error!

# ParamSpec with Concatenate for partial signature modification
from typing import Concatenate

def with_request_id(
    func: Callable[Concatenate[str, P], R]
) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        request_id = generate_request_id()
        return func(request_id, *args, **kwargs)
    return wrapper

@with_request_id
def process_data(request_id: str, data: str, count: int) -> str:
    return f"[{request_id}] {data} x {count}"

# process_data("hello", 5)  # request_id is injected automatically
```

### TypeVarTuple (PEP 646)

```python
from typing import TypeVarTuple, TypeVar, Generic

Ts = TypeVarTuple("Ts")
T = TypeVar("T")

# Variadic generics - types with variable number of type parameters
class Array(Generic[*Ts]):
    """Array with type-checked dimensions."""
    def __init__(self, shape: tuple[*Ts]) -> None:
        self.shape = shape

# Usage
arr_1d: Array[int] = Array((10,))           # 1D array of 10 elements
arr_2d: Array[int, int] = Array((10, 20))   # 2D array 10x20
arr_3d: Array[int, int, int] = Array((10, 20, 30))  # 3D array

# Unpack for type hints
from typing import Unpack

def reshape(arr: Array[*Ts], new_shape: tuple[*Ts]) -> Array[*Ts]:
    return Array(new_shape)
```

---

## Final and ClassVar

### Final

```python
from typing import Final

# Final - value cannot be reassigned
MAX_CONNECTIONS: Final[int] = 100
API_VERSION: Final[str] = "v2"
DEFAULT_TIMEOUT: Final[float] = 30.0

# Can be assigned once at module/class level
# MAX_CONNECTIONS = 200  # mypy error: cannot reassign Final variable

# In Pydantic models - constants
class Settings(BaseModel):
    app_name: Final[str] = "MyApp"       # Won't be serialized
    max_retries: int = 3                  # Regular field

# Final with complex types
ALLOWED_HOSTS: Final[list[str]] = ["localhost", "127.0.0.1"]
# You CAN modify the list contents (shallow Final)
# ALLOWED_HOSTS.append("example.com")  # This is technically allowed
# But mypy will warn about it

# For truly immutable, use frozen Pydantic model
class Constants(BaseModel):
    model_config = ConfigDict(frozen=True)
    api_key: str = "secret"
```

### ClassVar

```python
from typing import ClassVar

class ConnectionPool:
    # ClassVar - not a model field, belongs to class itself
    _instance_count: ClassVar[int] = 0
    _max_pool_size: ClassVar[int] = 10

    def __init__(self) -> None:
        ConnectionPool._instance_count += 1
        self.size: int = 0  # This is an instance variable (field)

    @classmethod
    def get_instance_count(cls) -> int:
        return cls._instance_count

# In Pydantic - ClassVar fields are excluded from the model
from pydantic import BaseModel

class User(BaseModel):
    # ClassVar - not included in serialization/validation
    _count: ClassVar[int] = 0
    table_name: ClassVar[str] = "users"

    # Regular fields - included in model
    name: str
    email: str

    def __init__(self, **data):
        super().__init__(**data)
        User._count += 1

# User.model_fields contains only 'name' and 'email'
print(User.model_fields.keys())  # dict_keys(['name', 'email'])
```

---

## NewType

```python
from typing import NewType

# NewType creates a distinct type from an existing one
UserId = NewType("UserId", int)
OrderId = NewType("OrderId", int)
Email = NewType("Email", str)
ProductName = NewType("ProductName", str)

# At runtime, NewType returns the original type
user_id = UserId(42)
print(type(user_id))  # <class 'int'>

# But static type checkers treat them as distinct
def get_user(user_id: UserId) -> dict:
    return {"id": user_id}

def process_order(order_id: OrderId) -> None:
    ...

# This is a type error - cannot mix UserId and OrderId
uid = UserId(1)
oid = OrderId(1)

get_user(uid)     # OK
get_user(oid)     # mypy error: Argument 1 has incompatible type "OrderId"; expected "UserId"

# NewType with Pydantic in FastAPI
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: UserId        # NewType in model
    name: str
    email: str

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate) -> UserResponse:
    # Database returns int, we wrap it as UserId
    new_id = UserId(generate_id())  # type: ignore
    return UserResponse(id=new_id, name=user.name, email=user.email)
```

---

## Runtime Type Checking Limitations

### What Python Does at Runtime

```python
# Python performs NO runtime type checking for type hints
def add(a: int, b: int) -> int:
    return a + b

# This runs without error despite wrong types
result = add("hello", "world")
print(result)  # "helloworld" - no error!

# Type hints are just annotations - stored in __annotations__
print(add.__annotations__)  # {'a': <class 'int'>, 'b': <class 'int'>}

# Python only checks types in specific cases:
# 1. isinstance() calls you write explicitly
# 2. Pydantic validation (uses type hints)
# 3. Dataclass creation (uses type hints)
# 4. FastAPI parameter validation (uses Pydantic under the hood)
```

### What Tools Like mypy/pyright Check

```python
# Static type checkers analyze code WITHOUT running it

# They catch:
# - Wrong argument types
# - Wrong return types
# - Missing attributes
# - Incompatible assignments
# - Missing return statements

class Dog:
    def bark(self) -> str:
        return "Woof!"

def animal_sound(animal: Dog) -> str:
    return animal.bark()

animal_sound("not a dog")  # mypy error, but runs fine

# They cannot catch:
# - Runtime type changes
# - Dynamic attribute access
# - Logic errors
# - Side effects
```

### Runtime Type Checking Patterns

```python
from typing import get_type_hints, get_origin, get_args
import typing

# Inspect type hints at runtime
def get_param_types(func: Callable) -> dict[str, type]:
    hints = get_type_hints(func)
    return hints

def example(x: int, y: str) -> bool:
    return True

print(get_param_types(example))  # {'x': <class 'int'>, 'y': <class 'str'>}

# Check generic types at runtime
def check_generic_type(tp: type) -> None:
    origin = get_origin(tp)
    args = get_args(tp)
    print(f"Origin: {origin}, Args: {args}")

check_generic_type(list[int])        # Origin: <class 'list'>, Args: (<class 'int'>,)
check_generic_type(dict[str, int])   # Origin: <class 'dict'>, Args: (<class 'str'>, <class 'int'>)
check_generic_type(int | str)        # Origin: <class 'types.UnionType'>, Args: (<class 'int'>, <class 'str'>)

# Pydantic IS the runtime type checker for FastAPI
from pydantic import BaseModel, ValidationError

class StrictModel(BaseModel):
    model_config = ConfigDict(strict=True)  # Enforce strict type checking

    name: str
    age: int

try:
    # This will fail at runtime - Pydantic catches it
    user = StrictModel(name="Alice", age="30")  # age should be int, not str
except ValidationError as e:
    print(e)  # ValidationError: Input should be a valid integer
```

---

## Type Hints Best Practices for FastAPI

### 1. Always Use Annotated for Query/Path/Body Parameters

```python
# BAD - uses default values, less explicit
@app.get("/users/{user_id}")
async def get_user(
    user_id: int = Path(..., description="User ID"),
    q: str = Query(None, max_length=50),
):
    ...

# GOOD - uses Annotated, cleaner and more Pythonic
from typing import Annotated
from fastapi import Query, Path

@app.get("/users/{user_id}")
async def get_user(
    user_id: Annotated[int, Path(description="User ID")],
    q: Annotated[str | None, Query(max_length=50)] = None,
):
    ...
```

### 2. Use Pydantic BaseModel for Request/Response Bodies

```python
from pydantic import BaseModel, Field

# Request model
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[\w.-]+@[\w.-]+\.\w+$")
    age: int | None = Field(default=None, ge=0, le=150)

# Response model - use response_model parameter
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate) -> UserResponse:
    ...
```

### 3. Use TypeAlias for Complex Types

```python
from typing import TypeAlias

# Create readable type aliases
JSON: TypeAlias = dict[str, Any]
Headers: TypeAlias = dict[str, str]
QueryParams: TypeAlias = dict[str, str | int | bool]

# Use in FastAPI
@app.get("/proxy")
async def proxy_endpoint(
    headers: Headers = Depends(get_headers),
    params: QueryParams = Depends(get_query_params),
) -> JSON:
    return {"headers": headers, "params": params}
```

### 4. Use Literal for Constrained Values

```python
from typing import Literal

# Instead of str with validation
@app.get("/sort")
async def sort_items(
    sort_by: Literal["name", "date", "price"] = "date",
    order: Literal["asc", "desc"] = "asc",
):
    return {"sort_by": sort_by, "order": order}
```

### 5. Use Generic Models for Reusable Patterns

```python
from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    error: str | None = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    has_next: bool

# Reusable across endpoints
@app.get("/users", response_model=PaginatedResponse[UserResponse])
async def list_users() -> PaginatedResponse[UserResponse]:
    ...

@app.get("/items", response_model=ApiResponse[list[ItemResponse]])
async def list_items() -> ApiResponse[list[ItemResponse]]:
    ...
```

### 6. Prefer `from __future__ import annotations`

```python
from __future__ import annotations  # PEP 563 - postpone evaluation

# Allows forward references without quotes
class Node:
    children: list[Node]  # Works because annotations are strings

# Also enables modern syntax on older Python
def process(items: list[int | str]) -> dict[str, int]:
    ...
```

### 7. Use Protocol for Structural Subtyping

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Repository(Protocol[T]):
    def get(self, id: int) -> T | None: ...
    def save(self, entity: T) -> T: ...
    def delete(self, id: int) -> bool: ...

# Any class with these methods satisfies the Protocol
class SQLUserRepo:
    def get(self, id: int) -> User | None: ...
    def save(self, entity: User) -> User: ...
    def delete(self, id: int) -> bool: ...

# This works without inheritance
def process_repo(repo: Repository[User]) -> None:
    user = repo.get(1)
    ...

process_repo(SQLUserRepo())  # OK - structural subtyping
```

---

## Interview Questions

### Q1: What is the difference between `List[int]` and `list[int]`?

**Answer:** `List[int]` is from `typing` module (Python 3.5+), while `list[int]` is native Python 3.9+ syntax. They are functionally identical - `list[int]` is preferred in modern Python as it's cleaner and more readable. In FastAPI, either works, but `list[int]` is recommended.

### Q2: What is `Annotated` and why does FastAPI prefer it?

**Answer:** `Annotated[type, metadata]` (PEP 593) attaches metadata to type hints without changing the type. FastAPI prefers it because it allows adding validation rules (via `Query`, `Path`, `Body`) directly in the type hint, keeping function signatures clean. It also separates concerns - the type is separate from the validation.

### Q3: What is the difference between `Optional[str]` and `str | None`?

**Answer:** They are semantically identical. `Optional[str]` is from `typing` module (Python 3.5+), while `str | None` uses the new union syntax (Python 3.10+). `str | None` is preferred in modern Python. FastAPI treats both the same way.

### Q4: Can Python check type hints at runtime?

**Answer:** No. Python does not enforce type hints at runtime - they are just annotations. However, Pydantic (used by FastAPI) reads type hints at runtime to validate data. Static type checkers like mypy and pyright analyze code without running it to catch type errors.

### Q5: What is `TypeVar` and when do you use it?

**Answer:** `TypeVar` defines a placeholder type for generic programming. Use it when writing generic functions or classes that work with multiple types while maintaining type safety. Example: `T = TypeVar("T")` can then be used in `def first(items: list[T]) -> T` to indicate the return type matches the list element type.

### Q6: What is the difference between `ClassVar` and regular class attributes?

**Answer:** `ClassVar[int]` tells type checkers and Pydantic that the attribute belongs to the class, not instances. In Pydantic models, `ClassVar` fields are excluded from serialization, validation, and the model schema. Regular attributes are treated as model fields.

### Q7: How does `NewType` differ from just using the base type?

**Answer:** `NewType` creates a distinct type that type checkers treat as separate, but at runtime it's the same type. This prevents accidentally mixing types (e.g., `UserId` and `OrderId` are both `int` but can't be interchanged in typed code). It adds type safety without runtime overhead.

### Q8: What is `ParamSpec` and when would you use it?

**Answer:** `ParamSpec` (PEP 612) captures the parameter types of a callable. It's used in decorators to preserve the decorated function's type signature. Without it, decorators lose the original function's parameter types, causing mypy to flag valid calls as errors.

### Q9: What is the difference between `Union[str, int]` and `str | int`?

**Answer:** They are identical. `str | int` is Python 3.10+ syntax for the same union type. `str | int` is preferred for readability. FastAPI handles both the same way.

### Q10: Why are type hints important specifically for FastAPI?

**Answer:** FastAPI uses type hints at runtime for three key purposes: (1) automatic request validation via Pydantic, (2) OpenAPI documentation generation, and (3) dependency injection type resolution. Without type hints, FastAPI cannot validate incoming data or generate accurate documentation.

### Q11: What is `Protocol` and how does it differ from abstract base classes?

**Answer:** `Protocol` enables structural subtyping (duck typing with type safety). Classes don't need to inherit from the Protocol - they just need to implement the required methods. ABCs require explicit inheritance. Protocols are more flexible and Pythonic for defining interfaces.

### Q12: What is `Literal` and when should you use it?

**Answer:** `Literal["a", "b", "c"]` restricts a type to specific literal values. Use it for enum-like parameters in FastAPI (e.g., `sort_by: Literal["name", "date"]`) instead of creating separate Enum classes. It's cleaner for simple constrained values.

### Q13: What is the difference between `TypeAlias` and `NewType`?

**Answer:** `TypeAlias` creates an alias for a complex type (e.g., `JSON = dict[str, Any]`). It's just a name for readability. `NewType` creates a distinct type that type checkers treat as separate from its base type. `TypeAlias` is for readability, `NewType` is for type safety.

### Q14: What is `Final` and how does it differ from `ClassVar`?

**Answer:** `Final` means a variable cannot be reassigned after initialization. `ClassVar` means a variable belongs to the class, not instances. They serve different purposes: `Final` prevents reassignment (like `const`), `ClassVar` indicates class-level scope. A variable can be both: `MAX: Final[int] = 100` in a class.

### Q15: How do you handle forward references in type hints?

**Answer:** Use `from __future__ import annotations` (PEP 563) to postpone annotation evaluation, allowing forward references without quotes. Alternatively, use string literals: `'MyClass'` as the type hint. The `__future__` import is recommended for modern Python.
