# Dependency Injection Basics in FastAPI

## Table of Contents

1. [What is Dependency Injection](#what-is-dependency-injection)
2. [Why DI Matters](#why-di-matters)
3. [FastAPI's DI System](#fastapis-di-system)
4. [The Depends() Function](#the-depends-function)
5. [Sync and Async Dependencies](#sync-and-async-dependencies)
6. [Returning Values from Dependencies](#returning-values-from-dependencies)
7. [Using Dependencies in Path Operations](#using-dependencies-in-path-operations)
8. [Multiple Dependencies](#multiple-dependencies)
9. [Dependency Trees](#dependency-trees)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## What is Dependency Injection

Dependency Injection (DI) is a design pattern where an object receives its dependencies from an external source rather than creating them internally. It is a form of **Inversion of Control (IoC)** — the control of creating and resolving dependencies is transferred from the consumer to the framework.

### The Problem Without DI

```python
# BAD: Tight coupling — hard to test, hard to maintain
class UserService:
    def __init__(self):
        self.db = PostgreSQLDatabase(host="localhost", port=5432)  # hardcoded
        self.mailer = SMTPMailer(host="smtp.gmail.com")           # hardcoded
        self.cache = RedisCache(host="localhost")                  # hardcoded

    def create_user(self, data: dict):
        user = self.db.insert("users", data)
        self.mailer.send(data["email"], "Welcome!", "Hello!")
        self.cache.set(f"user:{user.id}", user)
        return user
```

**Problems:**
- Cannot swap `PostgreSQLDatabase` for a test database
- Cannot mock `SMTPMailer` in unit tests
- Configuration is hardcoded everywhere
- Violates Single Responsibility Principle

### The Solution With DI

```python
# GOOD: Dependencies are injected from outside
class UserService:
    def __init__(self, db: Database, mailer: Mailer, cache: Cache):
        self.db = db
        self.mailer = mailer
        self.cache = cache

    def create_user(self, data: dict):
        user = self.db.insert("users", data)
        self.mailer.send(data["email"], "Welcome!", "Hello!")
        self.cache.set(f"user:{user.id}", user)
        return user

# In production:
service = UserService(db=PostgreSQLDatabase(...), mailer=SMTPMailer(...), cache=RedisCache(...))

# In tests:
service = UserService(db=InMemoryDatabase(), mailer=FakeMailer(), cache=FakeCache())
```

### Three Types of Dependency Injection

| Type | Description | Example |
|------|-------------|---------|
| **Constructor Injection** | Dependencies passed via `__init__` | `UserService(db=db)` |
| **Setter Injection** | Dependencies set via methods | `service.set_db(db)` |
| **Interface Injection** | Dependency provides an injector method | Framework-managed |

FastAPI primarily uses **Constructor Injection** through the `Depends()` mechanism.

---

## Why DI Matters

### 1. Testability

```python
# Without DI — integration test required
def test_create_user():
    service = UserService()  # connects to real DB
    user = service.create_user({"name": "Alice"})
    assert user is not None

# With DI — pure unit test
def test_create_user():
    mock_db = MockDatabase()
    service = UserService(db=mock_db)
    user = service.create_user({"name": "Alice"})
    assert mock_db.called_with("users", {"name": "Alice"})
```

### 2. Configuration Management

```python
# Single place to configure all dependencies
def get_database():
    return Database(url=settings.DATABASE_URL)

def get_cache():
    return Redis(host=settings.REDIS_HOST)

# Every endpoint automatically gets configured dependencies
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Database = Depends(get_database)):
    return db.query(User).get(user_id)
```

### 3. Separation of Concerns

Each dependency handles one thing. The route handler only handles HTTP logic.

### 4. Reusability

A single dependency can be shared across hundreds of route operations.

---

## FastAPI's DI System

FastAPI has one of the most elegant DI systems in any Python web framework. It is built on top of Starlette's dependency system and extends it significantly.

### Core Concepts

1. **`Depends()`** — Registers a dependency
2. **Callable** — Any function or class that can be called
3. **Resolution** — FastAPI resolves the dependency graph automatically
4. **Caching** — Dependencies are cached per-request by default
5. **Override** — Dependencies can be overridden for testing

### How It Works Internally

```python
from fastapi import Depends, FastAPI

app = FastAPI()

async def common_dependency():
    return {"db": "connection"}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_dependency)):
    return commons
```

**What happens when a request arrives:**

1. FastAPI inspects the `read_items` function signature
2. Finds `commons` parameter has `Depends(common_dependency)`
3. Calls `common_dependency()` to resolve the value
4. Passes the result as `commons` to `read_items`
5. Caches the result — if another parameter also depends on `common_dependency`, it reuses the cached value

---

## The Depends() Function

### Basic Usage

```python
from fastapi import Depends, FastAPI

app = FastAPI()

def get_query_string():
    return "some value"

@app.get("/")
def read_root(q: str = Depends(get_query_string)):
    return {"q": q}
```

### Dependency as a Callable

`Depends()` accepts any callable:

```python
# Function
def get_db():
    return Database()

# Lambda
Depends(lambda: Database())

# Class (instantiated)
Depends(Database)

# Async function
async def get_db():
    return Database()

# Method of a class
class ServiceContainer:
    def get_db(self):
        return Database()

container = ServiceContainer()
Depends(container.get_db)
```

### The `use_cache` Parameter

```python
# Default: use_cache=True — called once per request
@app.get("/")
def route(dep: str = Depends(get_dependency, use_cache=True)):
    ...

# use_cache=False — called every time it appears
@app.get("/")
def route(
    dep1: str = Depends(get_dependency, use_cache=False),
    dep2: str = Depends(get_dependency, use_cache=False),
):
    # dep1 and dep2 will be different objects
    ...
```

---

## Sync and Async Dependencies

FastAPI supports both synchronous and asynchronous dependencies transparently.

### Async Dependencies

```python
import httpx

async def get_external_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()

@app.get("/items/")
async def read_items(data: dict = Depends(get_external_data)):
    return data
```

### Sync Dependencies

```python
import time

def slow_dependency():
    time.sleep(2)  # blocking I/O
    return {"status": "ready"}

@app.get("/items/")
async def read_items(data: dict = Depends(slow_dependency)):
    return data
```

**Important:** FastAPI runs sync dependencies in a threadpool automatically so they don't block the event loop.

### Mixing Sync and Async

```python
async def async_dep():
    return "async"

def sync_dep():
    return "sync"

# This works — FastAPI handles both
@app.get("/")
def route(
    a: str = Depends(async_dep),
    b: str = Depends(sync_dep),
):
    return {"a": a, "b": b}
```

### Rules for Dependency Composition

```python
# An async dependency CAN depend on sync dependencies
async def async_with_sync(sync_val: str = Depends(sync_dep)):
    return f"async: {sync_val}"

# A sync dependency CANNOT depend on async dependencies
# This will RAISE AN ERROR:
def sync_with_async(async_val: str = Depends(async_dep)):
    return f"sync: {async_val}"
# ERROR: cannot call async function in sync context
```

**Rule:** Async dependencies can have sync sub-dependencies, but sync dependencies cannot have async sub-dependencies.

---

## Returning Values from Dependencies

### Return a Value

```python
def get_current_user():
    user = authenticate_user(token)
    return user

@app.get("/me")
def read_me(user: User = Depends(get_current_user)):
    return user
```

### Return None

```python
def validate_api_key(api_key: str = Header()):
    if api_key != "secret":
        raise HTTPException(status_code=403)
    # No return value needed — dependency is used for side effects

@app.get("/protected")
def protected_route(_: None = Depends(validate_api_key)):
    return {"message": "Access granted"}
```

### Raise Exceptions

```python
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

API_KEY = "supersecret"

def verify_api_key(api_key: str = Security(APIKeyHeader(name="X-API-Key"))):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )
    return api_key  # optional: return the validated key

@app.get("/secure")
def secure_endpoint(key: str = Depends(verify_api_key)):
    return {"key": key}
```

### Return a Generator (Yield Dependencies)

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

---

## Using Dependencies in Path Operations

### Single Dependency

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

### Multiple Dependencies

```python
def get_db():
    ...

def get_current_user(token: str = Header()):
    ...

@app.get("/users/me")
def read_current_user(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return user
```

### Dependencies with Parameters

```python
def get_db(url: str = None):
    db = SessionLocal(url=url or settings.DATABASE_URL)
    try:
        yield db
    finally:
        db.close()

# Cannot pass params directly to Depends, so use a factory:
def get_db_factory(url: str):
    def _get_db():
        db = SessionLocal(url=url)
        try:
            yield db
        finally:
            db.close()
    return _get_db

@app.get("/users/")
def list_users(db: Session = Depends(get_db_factory(settings.DATABASE_URL))):
    ...
```

---

## Multiple Dependencies

### Sequential Dependencies

```python
def dep_a():
    print("A resolved")
    return "a"

def dep_b():
    print("B resolved")
    return "b"

@app.get("/")
def route(a: str = Depends(dep_a), b: str = Depends(dep_b)):
    return {"a": a, "b": b}

# When called: prints "A resolved" then "B resolved"
```

### Shared Dependencies

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(db: Session = Depends(get_db)):
    return db.query(User).first()

def get_item(db: Session = Depends(get_db)):
    return db.query(Item).first()

@app.get("/summary")
def summary(
    user: User = Depends(get_user),
    item: Item = Depends(get_item),
):
    # get_db is called ONCE — both user and item share the same db session
    return {"user": user, "item": item}
```

### Dependencies with Header/Cookie/Form Parameters

```python
from fastapi import Header, Cookie, Form

def get_token(authorization: str = Header()):
    return authorization.replace("Bearer ", "")

def get_session_id(session_id: str = Cookie()):
    return session_id

@app.post("/form/")
def process_form(
    username: str = Form(),
    password: str = Form(),
    token: str = Depends(get_token),
    session: str = Depends(get_session_id),
):
    return {"username": username, "token": token, "session": session}
```

---

## Dependency Trees

Dependencies can form trees (actually directed acyclic graphs). FastAPI resolves them automatically.

### Simple Tree

```
get_current_user
├── get_database
├── get_token
└── validate_permissions
    └── get_database (shared — resolved once)
```

```python
def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_token(authorization: str = Header()):
    return authorization.split(" ")[1]

def validate_permissions(
    token: str = Depends(get_token),
    db: Session = Depends(get_database),
):
    user = db.query(User).filter(User.token == token).first()
    if not user:
        raise HTTPException(status_code=403)
    return user

def get_current_user(
    user: User = Depends(validate_permissions),
):
    return user

@app.get("/admin/")
def admin_dashboard(user: User = Depends(get_current_user)):
    return {"admin": user.name}
```

**Resolution order:**
1. `get_token` — extracts token from header
2. `get_database` — creates DB session
3. `validate_permissions` — uses token and db to validate
4. `get_current_user` — wraps the validated user
5. `admin_dashboard` — receives the final user object

### Deep Tree

```python
def get_config():
    return load_config()

def get_db_config(config: dict = Depends(get_config)):
    return config["database"]

def get_db(db_config: dict = Depends(get_db_config)):
    return connect(db_config)

def get_cache(config: dict = Depends(get_config)):
    return connect_cache(config["redis"])

def get_user_service(
    db = Depends(get_db),
    cache = Depends(get_cache),
):
    return UserService(db=db, cache=cache)

@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    return service.get(user_id)
```

### Visualization

```
get_config
├── get_db_config
│   └── get_db
│       └── get_user_service ← shared
└── get_cache ← shared
    └── get_user_service ← shared
```

**Key insight:** `get_config` is called once, `get_db` once, `get_cache` once, and `get_user_service` once. The caching ensures no duplicate calls.

---

## Best Practices

### 1. Keep Dependencies Small and Focused

```python
# BAD: One dependency doing too much
def get_everything():
    db = SessionLocal()
    user = authenticate_user()
    validate_permissions(user)
    setup_logging()
    return {"db": db, "user": user, "logger": logger}

# GOOD: Each dependency has one job
def get_db(): ...
def get_current_user(): ...
def get_logger(): ...
```

### 2. Name Dependencies Clearly

```python
# BAD
def dep1(): ...
def helper(): ...
def do_stuff(): ...

# GOOD
def get_database_session(): ...
def get_authenticated_user(): ...
def get_redis_connection(): ...
```

### 3. Use Type Hints

```python
# BAD
def get_db():
    return SessionLocal()

# GOOD
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 4. Don't Overuse Dependencies

```python
# BAD: Dependency for something that simple
def get_current_timestamp():
    return datetime.now()

# Just use it directly
@app.get("/time")
def get_time():
    return {"time": datetime.now()}
```

### 5. Prefer Function Dependencies Over Class Dependencies for Simple Cases

```python
# Simple case — function is fine
def get_db():
    return SessionLocal()

# Complex case — class with __call__ is better
class DatabasePool:
    def __init__(self, min_size: int, max_size: int):
        ...
    def __call__(self):
        return self.get_connection()
```

---

## Interview Questions

### Q1: What is Dependency Injection?
**Answer:** DI is a design pattern where objects receive their dependencies from external sources rather than creating them. It promotes loose coupling, testability, and separation of concerns. FastAPI implements it via `Depends()`.

### Q2: How does FastAPI's DI system work internally?
**Answer:** FastAPI inspects function signatures using `inspect.signature()`, finds parameters with `Depends()` default values, resolves them by calling the dependency callable, caches the results per-request, and injects the resolved values into the route handler.

### Q3: What is the difference between sync and async dependencies?
**Answer:** Async dependencies are awaited directly on the event loop. Sync dependencies are run in a threadpool via `run_in_executor`. Async dependencies can depend on sync sub-dependencies, but sync dependencies cannot depend on async sub-dependencies.

### Q4: What does `use_cache` do in `Depends()`?
**Answer:** When `use_cache=True` (default), the dependency is resolved once per request and reused for all parameters that depend on it. When `use_cache=False`, each `Depends()` call resolves the dependency independently.

### Q5: Can a dependency raise an exception?
**Answer:** Yes. Dependencies can raise `HTTPException` or any other exception. If raised, the exception propagates and the route handler is not executed. This is commonly used for authentication and authorization checks.

### Q6: What is a dependency tree?
**Answer:** A dependency tree (DAG) is formed when dependencies themselves depend on other dependencies. FastAPI resolves them in topological order, caching each resolved value to avoid redundant calls.

### Q7: What happens if a dependency is used in multiple routes?
**Answer:** Without `use_cache=False`, the dependency is cached per-request. Each request resolves it once. The same dependency function shared across routes is called fresh for each request (caching is per-request, not global).

### Q8: Can dependencies have parameters?
**Answer:** Not directly through `Depends()`. You use closure or factory functions to inject configuration into dependencies.

### Q9: How do you test code that uses `Depends()`?
**Answer:** Use `app.dependency_overrides[original_dep] = mock_dep` to replace dependencies in tests. This is built into FastAPI and is the recommended testing approach.

### Q10: What is the difference between `Depends()` and normal function calls?
**Answer:** `Depends()` integrates with FastAPI's dependency resolution system: automatic caching, sub-dependency resolution, async support, and testability via overrides. Normal function calls are just... function calls.

### Q11: Can you use `Depends()` outside of path operations?
**Answer:** `Depends()` is designed for FastAPI's DI system and works in path operations, routers, and app-level dependencies. Using it outside these contexts has no effect.

### Q12: What are the limitations of FastAPI's DI?
**Answer:** Dependencies must be callables. Async dependencies cannot be used in sync dependencies. Dependencies are cached per-request only. Complex dependency graphs can become hard to debug. No automatic scoping beyond request-level caching.

### Q13: How does dependency resolution handle circular dependencies?
**Answer:** FastAPI does not handle circular dependencies — it will raise an error. Dependencies must form a DAG (directed acyclic graph). You must refactor to break cycles.

### Q14: What is the difference between dependency injection and service locator pattern?
**Answer:** DI passes dependencies to the consumer (consumer doesn't know how they're created). Service locator has the consumer actively request dependencies from a registry. DI is generally preferred because it makes dependencies explicit.

### Q15: When would you use `use_cache=False`?
**Answer:** When you need distinct instances per dependency injection point in the same request. For example, two different database connections, or when the dependency has side effects that should run multiple times.

### Q16: How do global dependencies differ from route-level dependencies?
**Answer:** Global dependencies (set on `app` or `router`) run for every route in that scope. Route-level dependencies only run for that specific route. Global deps are resolved first.

### Q17: Can dependencies return async generators?
**Answer:** Yes. An async dependency can use `yield` and be an async generator. FastAPI will `async for` through it, yielding control at the yield point and resuming after the route handler completes.

### Q18: What happens to unhandled exceptions in dependencies?
**Answer:** If a dependency raises an unhandled exception, it propagates up the dependency tree. If not caught, FastAPI returns a 500 Internal Server Error. You should handle expected exceptions explicitly.

### Q19: How does FastAPI handle dependencies that return `None`?
**Answer:** The parameter's type hint determines how `None` is handled. If the parameter is `Optional[T]`, `None` is valid. If the parameter is `T` (non-optional), FastAPI's validation will raise a 422 error.

### Q20: Can a path operation have zero dependencies?
**Answer:** Yes. Dependencies are entirely optional. Routes work fine without them, though most real applications use at least one for database access or authentication.

### Q21: What is the execution order of dependencies?
**Answer:** FastAPI resolves dependencies in the order they appear in the function signature (left to right), but sub-dependencies are resolved before their parents. The overall order follows the topological sort of the dependency graph.

### Q22: How do you share state between dependencies?
**Answer:** Use the `request.state` object, or have one dependency return a value that other dependencies consume. You can also use class-based dependencies with shared state.

### Q23: What is the performance impact of DI in FastAPI?
**Answer:** Minimal. The main cost is function signature inspection (cached after first call), callable invocations, and caching overhead. The threadpool overhead for sync dependencies is the most significant cost.

### Q24: How does DI work with FastAPI's OpenAPI schema?
**Answer:** FastAPI uses dependency information to generate OpenAPI documentation. Dependencies with `Header()`, `Query()`, `Cookie()`, etc., appear as parameters in the API docs. Dependencies without these annotations are hidden.

### Q25: Can you override dependencies in production code?
**Answer:** Yes, using `app.dependency_overrides`. While designed for testing, it can be used in production for A/B testing, feature flags, or environment-specific behavior. Use cautiously.

### Q26: What is the difference between `Depends()` and Python's `functools.lru_cache`?
**Answer:** `Depends()` caches per-request and integrates with FastAPI's DI system. `lru_cache` caches globally across all requests. They serve different purposes — never use `lru_cache` for request-scoped state.

### Q27: How do you implement dependency injection without FastAPI's `Depends()`?
**Answer:** You can manually construct dependencies in route handlers, use a DI container library (like `dependency-injector`), or use constructor injection in your service classes. `Depends()` is FastAPI's built-in, most Pythonic approach.

---

## Summary

FastAPI's dependency injection system is powerful, flexible, and deeply integrated into the framework. It provides:

- **Automatic resolution** of dependency graphs
- **Per-request caching** to avoid redundant calls
- **Sync/async transparency** with threadpool execution
- **Testability** through dependency overrides
- **Type safety** through Python's type hints

Master DI in FastAPI and you'll build applications that are testable, maintainable, and follow SOLID principles.
