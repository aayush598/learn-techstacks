# Python Fundamentals for FastAPI - Interview Questions

## Table of Contents

1. [Async/Await Questions](#asyncawait-questions)
2. [Pydantic Questions](#pydantic-questions)
3. [Type Hints Questions](#type-hints-questions)
4. [Performance Questions](#performance-questions)
5. [Python Features Questions](#python-features-questions)
6. [Dataclasses Questions](#dataclasses-questions)
7. [Architecture & Design Questions](#architecture--design-questions)
8. [Coding Challenges](#coding-challenges)

---

## Async/Await Questions

### Q1: What is the difference between async and sync in Python?

**Answer:**
```python
# Sync code - blocks until complete
import time

def sync_fetch():
    time.sleep(1)  # Blocks entire thread
    return "data"

# Async code - can switch to other tasks while waiting
import asyncio

async def async_fetch():
    await asyncio.sleep(1)  # Non-blocking, event loop can do other work
    return "data"

# Key difference:
# - Sync: One operation at a time per thread
# - Async: Multiple operations concurrently on single thread
# - Async is better for I/O-bound, sync for CPU-bound
```

**Follow-up:** When would you choose sync over async?
- CPU-bound tasks (use multiprocessing instead)
- Simple scripts with no concurrency
- When libraries don't support async
- When sequential execution is required

---

### Q2: What is an event loop and how does it work?

**Answer:**
```python
import asyncio

# Event loop manages all async operations
async def task1():
    print("Task 1 start")
    await asyncio.sleep(1)  # Event loop switches to task2
    print("Task 1 end")
    return 1

async def task2():
    print("Task 2 start")
    await asyncio.sleep(2)  # Event loop waits
    print("Task 2 end")
    return 2

async def main():
    # Event loop orchestrates:
    # 1. Start task1 (schedules it)
    # 2. Start task2 (schedules it)
    # 3. task1 sleeps → event loop runs task2
    # 4. task2 sleeps → event loop waits
    # 5. After 1s: task1 wakes, finishes
    # 6. After 2s: task2 wakes, finishes
    results = await asyncio.gather(task1(), task2())
    # Total: ~2 seconds, not 3

asyncio.run(main())
```

**Follow-up:** How does uvloop improve the event loop?
- uvloop uses libuv (C library) instead of Python's selector
- 2-4x faster for I/O operations
- Lower latency, better memory efficiency
- Drop-in replacement: `uvloop.install()`

---

### Q3: What is the GIL and how does it affect FastAPI?

**Answer:**
```python
# GIL (Global Interpreter Lock) prevents multiple threads from
# executing Python code simultaneously

# Impact on FastAPI:
# 1. Async I/O is NOT affected (doesn't use threads)
# 2. CPU-bound sync endpoints ARE affected (run in thread pool)
# 3. Multiple workers bypass GIL (separate processes)

# FastAPI handles this:
# - async def: Runs on event loop (no GIL issues)
# - def: Runs in thread pool (GIL limits parallelism)

@app.get("/async")
async def async_endpoint():
    # Runs on event loop - no GIL issues
    await asyncio.sleep(1)
    return "async"

@app.get("/sync")
def sync_endpoint():
    # Runs in thread pool - GIL limits to 1 thread at a time
    time.sleep(1)
    return "sync"

# Solution for CPU-bound: Use multiple workers
# gunicorn main:app -w $(nproc) -k uvicorn.workers.UvicornWorker
```

**Follow-up:** How do you bypass the GIL?
- Use multiprocessing (separate processes)
- Use C extensions (NumPy, etc.)
- Use asyncio for I/O-bound work
- Use multiple Gunicorn workers

---

### Q4: When should you NOT use async?

**Answer:**
```python
# 1. CPU-bound operations
def compute_heavy(data):
    # This blocks - don't use async here
    return sum(x * x for x in data)

# 2. Simple scripts with no concurrency
def simple_script():
    # No benefit from async
    print("Hello world")

# 3. Libraries don't support async
def use_sync_library():
    import pandas as pd
    df = pd.read_csv("data.csv")
    return df

# 4. Sequential operations with no waiting
async def sequential_operations():
    # Each depends on previous - no parallelism possible
    result1 = await compute(1)
    result2 = await compute(result1)
    return result2

# 5. When debugging complex async issues
# Built-in asyncio has better debugging tools
```

---

### Q5: What is the difference between `asyncio.gather` and `TaskGroup`?

**Answer:**
```python
import asyncio

async def failing_task():
    await asyncio.sleep(0.5)
    raise ValueError("Failed")

async def successful_task():
    await asyncio.sleep(1)
    return "success"

# asyncio.gather - continues on error
async def with_gather():
    results = await asyncio.gather(
        failing_task(),
        successful_task(),
        return_exceptions=True,
    )
    # results = [ValueError("Failed"), "success"]
    # Second task still completed!

# TaskGroup - cancels all on error
async def with_taskgroup():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(failing_task())
            tg.create_task(successful_task())
    except* ValueError:
        pass  # Both tasks cancelled

# Key differences:
# - gather: Fire-and-forget, continue on error
# - TaskGroup: Structured concurrency, cancel on error
# - TaskGroup: Python 3.11+ only
# - TaskGroup: Safer, more predictable cleanup
```

---

### Q6: What are common async mistakes?

**Answer:**
```python
# Mistake 1: Blocking the event loop
async def bad():
    time.sleep(5)  # BAD: Blocks everything!
    await asyncio.sleep(5)  # GOOD: Non-blocking

# Mistake 2: Forgetting to await
async def bad():
    fetch_data()  # BAD: Coroutine never awaited
    await fetch_data()  # GOOD: Always await

# Mistake 3: Losing task references
async def bad():
    asyncio.create_task(background_task())  # BAD: May be garbage collected
    task = asyncio.create_task(background_task())  # GOOD: Keep reference

# Mistake 4: Using sync libraries
async def bad():
    requests.get(url)  # BAD: Blocks event loop
    await aiohttp.get(url)  # GOOD: Async library
    await asyncio.to_thread(requests.get, url)  # GOOD: Thread pool

# Mistake 5: Unnecessary async
async def bad():
    return sum(range(1000))  # BAD: No I/O, async useless
def good():
    return sum(range(1000))  # GOOD: Synchronous for CPU work
```

---

## Pydantic Questions

### Q7: How does Pydantic V2 differ from V1?

**Answer:**
```python
# V1: Python-based validation
# V2: Rust-based validation (5-50x faster)

# Key API changes:
# V1: @validator -> V2: @field_validator + @classmethod
# V1: @root_validator -> V2: @model_validator
# V1: class Config -> V2: model_config = ConfigDict(...)
# V1: orm_mode -> V2: from_attributes
# V1: schema_extra -> V2: json_schema_extra
# V1: .dict() -> V2: .model_dump()
# V1: .json() -> V2: .model_dump_json()

# V1
class UserV1(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True

    @validator("age")
    def validate_age(cls, v):
        if v < 0:
            raise ValueError("Invalid age")
        return v

# V2
class UserV2(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    age: int

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Invalid age")
        return v
```

**Follow-up:** What are the performance improvements?
- Rust core (pydantic-core) for validation
- 5-50x faster validation
- Better memory usage
- Optimized serialization
- Lazy validation support

---

### Q8: What is the difference between `Optional[str]` and `str | None`?

**Answer:**
```python
from typing import Optional

# They are semantically identical
def a(x: Optional[str]) -> None: ...  # Python 3.5+
def b(x: str | None) -> None: ...     # Python 3.10+

# str | None is preferred for readability
# Both tell type checkers the value can be str or None
# FastAPI handles both the same way

# In FastAPI
@app.get("/items")
async def get_items(
    q: str | None = None,  # Preferred
    # q: Optional[str] = None,  # Also works
):
    return {"q": q}
```

---

### Q9: What is `Annotated` and why does FastAPI prefer it?

**Answer:**
```python
from typing import Annotated
from pydantic import Field
from fastapi import Query, Path

# Annotated adds metadata to types without changing the type
# It separates type from validation rules

# BAD: Uses default values, less explicit
@app.get("/users/{user_id}")
async def get_user(
    user_id: int = Path(..., description="User ID"),
    q: str = Query(None, max_length=50),
):
    ...

# GOOD: Uses Annotated, cleaner
@app.get("/users/{user_id}")
async def get_user(
    user_id: Annotated[int, Path(description="User ID")],
    q: Annotated[str | None, Query(max_length=50)] = None,
):
    ...

# Benefits:
# 1. Type hints remain clean
# 2. Validation rules are metadata, not defaults
# 3. Better for type checkers
# 4. More Pythonic (PEP 593)
```

---

### Q10: How does Pydantic validate data at runtime?

**Answer:**
```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int
    email: str

# Pydantic reads type hints at RUNTIME
# and validates incoming data

# Valid data
user = User(name="Alice", age=30, email="alice@example.com")

# Invalid data - Pydantic catches errors
try:
    user = User(name="", age="not_a_number", email="invalid")
except ValidationError as e:
    print(e)
    # 3 validation errors:
    #   - name: String should have at least 1 character
    #   - age: Input should be a valid integer
    #   - email: Input should be a valid email address

# Pydantic performs:
# 1. Type checking
# 2. Type coercion (in lax mode)
# 3. Custom validation rules
# 4. JSON schema generation
```

---

## Type Hints Questions

### Q11: What are Python type hints and why do they matter for FastAPI?

**Answer:**
```python
# Type hints are annotations that specify types
# They don't affect runtime behavior (Python ignores them)
# But FastAPI USES THEM AT RUNTIME for:

# 1. Automatic request validation
@app.get("/users/{user_id}")
async def get_user(user_id: int):  # FastAPI validates user_id is int
    ...

# 2. OpenAPI documentation generation
# FastAPI generates docs from type hints

# 3. Dependency injection
def get_db(session: Session = Depends(get_session)):  # Type-based injection
    ...

# 4. Serialization
@app.get("/user", response_model=UserResponse)  # Response validation
async def get_user() -> UserResponse:
    ...

# Without type hints, FastAPI cannot:
# - Validate incoming data
# - Generate accurate documentation
# - Perform type-based dependency injection
```

---

### Q12: What is `TypeVar` and when do you use it?

**Answer:**
```python
from typing import TypeVar, Generic

T = TypeVar("T")

# TypeVar defines a placeholder type for generics

# Generic function
def first_element(items: list[T]) -> T | None:
    if items:
        return items[0]
    return None

# Generic class
class Repository(Generic[T]):
    def __init__(self, items: list[T]) -> None:
        self._items = items

    def get(self, index: int) -> T:
        return self._items[index]

# TypeVar with constraints
NumberOrString = TypeVar("NumberOrString", int, str)

def double(value: NumberOrString) -> NumberOrString:
    return value * 2

# TypeVar with bounds
class Animal:
    name: str

AnimalType = TypeVar("AnimalType", bound=Animal)

def get_name(animal: AnimalType) -> str:
    return animal.name
```

---

### Q13: What is the difference between `Union[str, int]` and `str | int`?

**Answer:**
```python
from typing import Union

# They are identical
def a(x: Union[str, int]) -> None: ...  # Python 3.5+
def b(x: str | int) -> None: ...        # Python 3.10+

# str | int is preferred for readability
# Both tell type checkers the value can be str or int
# FastAPI handles both the same way

# In Pydantic
class FlexibleModel(BaseModel):
    value: str | int | None = None  # Preferred

# Note: Python evaluates | left-to-right
# str | int | None  ->  (str | int) | None
# Which is equivalent to Union[str, int, None]
```

---

### Q14: What is `Literal` and when should you use it?

**Answer:**
```python
from typing import Literal

# Literal restricts a type to specific values

# Instead of str with validation
@app.get("/sort")
async def sort_items(
    sort_by: Literal["name", "date", "price"] = "date",
    order: Literal["asc", "desc"] = "asc",
):
    # sort_by can only be "name", "date", or "price"
    # order can only be "asc" or "desc"
    return {"sort_by": sort_by, "order": order}

# Benefits:
# 1. Clearer than string validation
# 2. Better OpenAPI documentation
# 3. IDE autocompletion
# 4. Type checker support

# When to use:
# - Enum-like parameters (small set of values)
# - API parameters with fixed options
# - When you don't need Enum class overhead
```

---

## Performance Questions

### Q15: What is uvloop and when should you use it?

**Answer:**
```python
# uvloop is a fast event loop built on libuv
# It's 2-4x faster than built-in asyncio

# Installation
pip install uvloop

# Usage
import uvloop
uvloop.install()

# When to use:
# - Production FastAPI servers
# - High-concurrency applications
# - I/O-heavy workloads

# When NOT to use:
# - Windows (not supported)
# - Debugging (limited debug tools)
# - Development (may hide issues)

# Benchmark
# asyncio: ~15,000 requests/sec
# uvloop: ~45,000 requests/sec
# 3x improvement!
```

---

### Q16: How do you calculate worker count for Gunicorn?

**Answer:**
```python
import multiprocessing

# Rule of thumb
def calculate_workers(app_type: str = "io_bound") -> int:
    cpu_cores = multiprocessing.cpu_count()

    if app_type == "io_bound":
        # For API servers, web apps
        workers = (2 * cpu_cores) + 1
    elif app_type == "cpu_bound":
        # For data processing, ML
        workers = cpu_cores + 1
    else:
        workers = cpu_cores

    return min(workers, 16)  # Cap at 16

# Examples:
# 4-core (I/O): (2*4)+1 = 9 workers
# 8-core (I/O): (2*8)+1 = 17 → cap at 16
# 4-core (CPU): 4+1 = 5 workers

# Also consider memory
# Each worker uses ~200MB
# 4GB RAM, 4-core: min(4*2+1, 4096*0.8/200) = min(9, 16) = 9
```

---

### Q17: How do you optimize FastAPI performance?

**Answer:**
```python
# 1. Use uvloop
import uvloop
uvloop.install()

# 2. Connection pooling
from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine(DATABASE_URL, pool_size=20)

# 3. Async database drivers
# Use asyncpg instead of psycopg2
# Use aiomysql instead of pymysql

# 4. Caching
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_computation(n: int) -> int:
    return sum(i * i for i in range(n))

# 5. Response streaming
@app.get("/large-data")
async def stream_data():
    async for chunk in read_large_file():
        yield chunk

# 6. Background tasks
@app.post("/process")
async def process(data: BackgroundTasks):
    data.add_task(expensive_operation, data)
    return {"status": "queued"}

# 7. Proper worker count
# gunicorn main:app -w $(nproc) -k uvicorn.workers.UvicornWorker

# 8. Enable HTTP keep-alive
# Uvicorn handles this automatically
```

---

## Python Features Questions

### Q18: What is structural pattern matching?

**Answer:**
```python
# match/case is Python's version of switch/case but more powerful
# It matches patterns against data structures

def handle_command(command: str):
    match command.split():
        case ["quit"]:
            return "Exiting..."
        case ["hello", name]:
            return f"Hello, {name}!"
        case ["add", *numbers]:
            return sum(int(n) for n in numbers)
        case _:
            return "Unknown command"

# With classes
@dataclass
class Point:
    x: float
    y: float

def describe_point(point: Point):
    match point:
        case Point(x=0, y=0):
            return "Origin"
        case Point(x=x, y=0):
            return f"On x-axis at {x}"
        case Point(x=0, y=y):
            return f"On y-axis at {y}"
        case Point(x=x, y=y):
            return f"Point at ({x}, {y})"

# Benefits:
# 1. Cleaner than if/elif chains
# 2. Can destructure data
# 3. Supports guards (conditions)
# 4. More readable for complex patterns
```

---

### Q19: What is the walrus operator?

**Answer:**
```python
# Walrus operator := assigns and returns in one expression

# Before
data = get_data()
if data:
    process(data)

# With walrus
if data := get_data():
    process(data)

# In while loops
while chunk := file.read(8192):
    process(chunk)

# In list comprehensions
results = [y for x in data if (y := expensive_func(x)) is not None]

# In FastAPI
@app.get("/users")
async def get_users(
    q: str | None = Query(default=None),
):
    if query := q:  # Assign and check
        results = await search_database(query)
        return {"query": query, "results": results}
    return {"query": None, "results": []}

# Rule of thumb:
# Use when it improves readability
# Don't use just to save a line
```

---

### Q20: What are dataclasses and when should you use them?

**Answer:**
```python
from dataclasses import dataclass, field

# Dataclasses auto-generate __init__, __repr__, __eq__

@dataclass
class User:
    name: str
    age: int
    email: str
    tags: list[str] = field(default_factory=list)

# Benefits:
# 1. Less boilerplate
# 2. Clear data structure
# 3. Auto-generated methods
# 4. Better than plain classes

# When to use:
# - Simple data containers
# - Internal structures (not API models)
# - When you need equality comparison
# - When performance is critical

# When NOT to use:
# - API models (use Pydantic)
# - When you need validation
# - When you need complex serialization

# Pydantic dataclass hybrid
from pydantic import dataclasses

@dataclasses.dataclass
class UserModel:
    name: str = field(min_length=1)
    age: int = field(ge=0)
```

---

## Dataclasses Questions

### Q21: What is the difference between frozen and mutable dataclasses?

**Answer:**
```python
from dataclasses import dataclass

# Mutable (default)
@dataclass
class MutablePoint:
    x: float
    y: float

point = MutablePoint(1, 2)
point.x = 3  # OK - can modify

# Frozen (immutable)
@dataclass(frozen=True)
class FrozenPoint:
    x: float
    y: float

point = FrozenPoint(1, 2)
# point.x = 3  # AttributeError - cannot modify

# Benefits of frozen:
# 1. Immutable (safer)
# 2. Hashable (can be dict keys)
# 3. Thread-safe
# 4. Prevents accidental modification

# Use cases:
# - Value objects (coordinates, money)
# - Configuration
# - Dict keys
# - Set members
```

---

### Q22: What does `slots=True` do?

**Answer:**
```python
from dataclasses import dataclass

# Without slots (default)
@dataclass
class Regular:
    x: int
    y: int

# With slots
@dataclass(slots=True)
class Slotted:
    x: int
    y: int

# Benefits:
# 1. ~80% less memory per instance
# 2. Faster attribute access (~20%)
# 3. Prevents dynamic attribute creation
# 4. Required for frozen dataclasses

# Memory comparison
import sys
regular = Regular(1, 2)
slotted = Slotted(1, 2)

print(sys.getsizeof(regular.__dict__))  # ~232 bytes
print(hasattr(slotted, '__dict__'))     # False

# When to use:
# - Classes with many instances
# - Performance-critical code
# - When you want fixed attributes
```

---

### Q23: How do you add validation to a dataclass?

**Answer:**
```python
# Native dataclass - manual validation
@dataclass
class NativeUser:
    name: str
    age: int

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative")

# Pydantic dataclass - automatic validation
from pydantic import dataclasses, field

@dataclasses.dataclass
class PydanticUser:
    name: str = field(min_length=1)
    age: int = field(ge=0, le=150)
    email: str = field(pattern=r"^[\w.-]+@[\w.-]+\.\w+$")

    def __post_init_post_parse__(self):
        # Runs AFTER Pydantic validation
        if self.age < 18:
            raise ValueError("Must be 18+")

# Native: Validation in __post_init__
# Pydantic: Validation in field() + __post_init_post_parse__
```

---

## Architecture & Design Questions

### Q24: How do you structure a FastAPI project?

**Answer:**
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app creation
│   ├── config.py          # Settings/configuration
│   ├── dependencies.py    # FastAPI dependencies
│   ├── models/            # Pydantic models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── routers/           # API routes
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── services/          # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   ├── repositories/      # Database access
│   │   ├── __init__.py
│   │   ├── user_repo.py
│   │   └── item_repo.py
│   └── utils/             # Helper functions
│       ├── __init__.py
│       └── helpers.py
├── tests/
├── requirements.txt
└── README.md
```

---

### Q25: When do you use async vs sync dependencies?

**Answer:**
```python
from fastapi import FastAPI, Depends

app = FastAPI()

# Async dependency - for I/O operations
async def get_db():
    db = await create_async_connection()
    try:
        yield db
    finally:
        await db.close()

# Sync dependency - for simple setup
def get_settings():
    return Settings()

# Mix both
async def get_user(
    settings: Settings = Depends(get_settings),
    db: AsyncSession = Depends(get_db),
):
    # settings is sync, db is async
    user = await db.execute(select(User))
    return user

# Rule of thumb:
# - Use async for: DB queries, HTTP calls, file I/O
# - Use sync for: Config, simple calculations, static data
```

---

### Q26: How do you handle errors in FastAPI?

**Answer:**
```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Custom exception
class InsufficientFundsError(Exception):
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount

# Exception handler
@app.exception_handler(InsufficientFundsError)
async def insufficient_funds_handler(
    request: Request,
    exc: InsufficientFundsError,
):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Insufficient funds",
            "balance": exc.balance,
            "requested": exc.amount,
        },
    )

@app.post("/transfer")
async def transfer(amount: float):
    balance = await get_balance()
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    # Process transfer
    return {"status": "success"}

# HTTPException for simple cases
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await fetch_user(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user
```

---

### Q27: How do you implement rate limiting?

**Answer:**
```python
import time
from collections import defaultdict
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)

    async def __call__(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()

        # Clean old requests
        self.requests[client_ip] = [
            t for t in self.requests[client_ip]
            if now - t < self.window_seconds
        ]

        if len(self.requests[client_ip]) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded"},
            )

        self.requests[client_ip].append(now)
        return await call_next(request)

# Add middleware
limiter = RateLimiter(max_requests=100, window_seconds=60)
app.middleware("http")(limiter)

# Or use dependency
from fastapi import Depends

def rate_limit():
    # Implement rate limiting logic
    pass

@app.get("/endpoint")
async def endpoint(rate_limit=Depends(rate_limit)):
    return {"message": "OK"}
```

---

### Q28: How do you test FastAPI applications?

**Answer:**
```python
from fastapi.testclient import TestClient
from pytest import fixture
from httpx import AsyncClient

# Synchronous testing
def test_create_user():
    client = TestClient(app)
    response = client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"

# Asynchronous testing
@fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

async def test_create_user_async(client):
    response = await client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com"},
    )
    assert response.status_code == 201

# With database
@fixture
async def db_session():
    async with async_engine.begin() as conn:
        yield conn
        await conn.rollback()

async def test_get_user(client, db_session):
    # Create user
    await db_session.execute(insert(User).values(name="Alice"))
    # Test endpoint
    response = await client.get("/users/1")
    assert response.status_code == 200
```

---

## Coding Challenges

### Q29: Implement a simple cache with TTL

**Answer:**
```python
import asyncio
import time
from typing import Any, Optional

class AsyncCache:
    def __init__(self, default_ttl: int = 300):
        self.cache: dict[str, tuple[Any, float]] = {}
        self.default_ttl = default_ttl

    async def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                return value
            else:
                del self.cache[key]
        return None

    async def set(self, key: str, value: Any, ttl: int = None):
        ttl = ttl or self.default_ttl
        self.cache[key] = (value, time.time() + ttl)

    async def delete(self, key: str):
        if key in self.cache:
            del self.cache[key]

    async def clear(self):
        self.cache.clear()

# Usage
cache = AsyncCache(default_ttl=60)

async def get_expensive_data(key: str) -> dict:
    # Check cache first
    cached = await cache.get(key)
    if cached is not None:
        return cached

    # Compute value
    await asyncio.sleep(1)  # Simulate expensive computation
    value = {"key": key, "computed_at": time.time()}

    # Cache result
    await cache.set(key, value, ttl=300)
    return value
```

---

### Q30: Implement a connection pool

**Answer:**
```python
import asyncio
from typing import AsyncGenerator

class ConnectionPool:
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.semaphore = asyncio.Semaphore(max_connections)
        self.connections: list = []
        self._lock = asyncio.Lock()

    async def _create_connection(self):
        # Simulate connection creation
        await asyncio.sleep(0.1)
        return {"id": len(self.connections), "active": True}

    async def _release_connection(self, conn):
        conn["active"] = False

    async def get_connection(self) -> AsyncGenerator:
        async with self.semaphore:
            conn = await self._create_connection()
            try:
                yield conn
            finally:
                await self._release_connection(conn)

# Usage
pool = ConnectionPool(max_connections=5)

async def query_database(query: str):
    async with pool.get_connection() as conn:
        # Use connection
        await asyncio.sleep(0.1)
        return f"Result from connection {conn['id']}"

async def main():
    # Run 20 queries, but only 5 concurrent
    tasks = [query_database(f"SELECT {i}") for i in range(20)]
    results = await asyncio.gather(*tasks)
    print(f"Completed {len(results)} queries")
```

---

### Q31: Implement a retry decorator

**Answer:**
```python
import asyncio
import functools
from typing import Type, Union

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff

            raise last_exception
        return wrapper
    return decorator

# Usage
@retry(max_attempts=3, delay=1.0, backoff=2.0)
async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

# Retry sequence:
# Attempt 1: fail → wait 1s
# Attempt 2: fail → wait 2s
# Attempt 3: fail → raise exception
```

---

### Q32: Implement a simple dependency injection system

**Answer:**
```python
from typing import Any, Callable, TypeVar, get_type_hints
import inspect

T = TypeVar("T")

class Container:
    def __init__(self):
        self._services: dict[type, Callable] = {}
        self._singletons: dict[type, Any] = {}

    def register(self, service_type: type, factory: Callable):
        self._services[service_type] = factory

    def register_singleton(self, service_type: type, factory: Callable):
        self._singletons[service_type] = factory

    def resolve(self, service_type: type) -> Any:
        if service_type in self._singletons:
            return self._singletons[service_type]

        if service_type in self._services:
            factory = self._services[service_type]
            instance = factory()
            return instance

        raise ValueError(f"No registration for {service_type}")

# Usage
container = Container()

class Database:
    def __init__(self, url: str):
        self.url = url

class UserService:
    def __init__(self, db: Database):
        self.db = db

# Register
container.register(Database, lambda: Database("postgresql://localhost/db"))
container.register_singleton(
    UserService,
    lambda: UserService(container.resolve(Database)),
)

# Resolve
user_service = container.resolve(UserService)
```

---

### Q33: Implement a simple event system

**Answer:**
```python
import asyncio
from typing import Callable, Any
from collections import defaultdict

class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)

    def on(self, event: str, handler: Callable):
        self._handlers[event].append(handler)

    def off(self, event: str, handler: Callable):
        self._handlers[event].remove(handler)

    async def emit(self, event: str, data: Any = None):
        handlers = self._handlers.get(event, [])
        tasks = [handler(data) for handler in handlers]
        await asyncio.gather(*tasks)

# Usage
event_bus = EventBus()

async def on_user_created(user: dict):
    print(f"User created: {user['name']}")

async def send_welcome_email(user: dict):
    print(f"Sending welcome email to {user['email']}")

# Register handlers
event_bus.on("user.created", on_user_created)
event_bus.on("user.created", send_welcome_email)

# Emit event
await event_bus.emit("user.created", {"name": "Alice", "email": "alice@example.com"})
# Output:
# User created: Alice
# Sending welcome email to alice@example.com
```
