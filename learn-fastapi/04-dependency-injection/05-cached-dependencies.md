# Cached Dependencies in FastAPI

## Table of Contents

1. [UseCache in Depends()](#usecache-in-depends)
2. [Caching Behavior Per-Request vs Global](#caching-behavior-per-request-vs-global)
3. [When to Cache](#when-to-cache)
4. [When NOT to Cache](#when-not-to-cache)
5. [Cache Invalidation](#cache-invalidation)
6. [Request-Scoped Dependencies](#request-scoped-dependencies)
7. [State Dependencies](#state-dependencies)
8. [Advanced Caching Patterns](#advanced-caching-patterns)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## UseCache in Depends()

### Default Caching

By default, `Depends()` caches the resolved value per-request:

```python
call_count = 0

def get_data():
    global call_count
    call_count += 1
    print(f"Dependency called: {call_count} times")
    return {"count": call_count}

@app.get("/")
def route(
    a: dict = Depends(get_data),
    b: dict = Depends(get_data),
):
    # get_data is called ONCE
    # a and b are the same object
    return {"a": a, "b": b}
# Output: "Dependency called: 1 times"
```

### use_cache=False

```python
@app.get("/")
def route(
    a: dict = Depends(get_data, use_cache=False),
    b: dict = Depends(get_data, use_cache=False),
):
    # get_data is called TWICE
    # a and b are different objects
    return {"a": a, "b": b}
# Output:
# "Dependency called: 1 times"
# "Dependency called: 2 times"
```

### The Depends Signature

```python
Depends(
    dependency: Callable = None,  # The function/class to resolve
    use_cache: bool = True,       # Cache per-request (default True)
)

# In practice:
Depends(get_db)                  # Cached
Depends(get_db, use_cache=True)  # Cached (explicit)
Depends(get_db, use_cache=False) # Not cached
```

### Caching Key

The cache key is a combination of:
1. The dependency callable (identity check)
2. The `use_cache` parameter
3. The resolved parent dependencies (as input parameters)

```python
def dep(x: int):
    return x * 2

# These are cached separately (different parameters via Depends)
@app.get("/")
def route(
    a: int = Depends(lambda: dep(1)),
    b: int = Depends(lambda: dep(2)),
):
    return {"a": a, "b": b}  # a=2, b=4
```

---

## Caching Behavior Per-Request vs Global

### Per-Request Caching

FastAPI's `Depends()` caching is **per-request only**. Each new request gets fresh dependency resolution.

```python
call_count = 0

def get_timestamp():
    global call_count
    call_count += 1
    return time.time()

# Request 1: call_count = 1, timestamp = 1000.0
# Request 2: call_count = 2, timestamp = 1000.5
# Each request resolves independently
```

### Why Per-Request?

```python
# Database session — must be per-request
def get_db():
    db = SessionLocal()  # New session each request
    try:
        yield db
    finally:
        db.close()  # Close after request

# If cached globally, the same session would be reused across requests
# leading to stale data, connection leaks, and concurrency issues
```

### Global Caching (Manual)

If you need truly global caching, implement it yourself:

```python
import functools

# Global cache (persists across requests)
_global_cache = {}

def global_dep():
    key = "expensive_computation"
    if key not in _global_cache:
        _global_cache[key] = expensive_computation()
    return _global_cache[key]

# Using functools.lru_cache
@functools.lru_cache(maxsize=128)
def cached_global_dep():
    return expensive_computation()

# WARNING: lru_cache persists across requests!
# Only use for truly immutable data
```

### Caching Lifetime Comparison

| Scope | Lifetime | Use Case |
|-------|----------|----------|
| `Depends(use_cache=True)` | Per-request | DB sessions, auth, request context |
| `Depends(use_cache=False)` | Per-injection | Distinct instances per injection |
| `functools.lru_cache` | Application lifetime | Static config, constants |
| Manual dict cache | Custom | Specific caching strategies |

---

## When to Cache

### Database Sessions (ALWAYS Cache)

```python
# CORRECT: Cached — one session shared across all deps in request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_repo(db=Depends(get_db)):
    return UserRepository(db)

def get_order_repo(db=Depends(get_db)):
    return OrderRepository(db)

# Both repos use the SAME db session — correct!
```

### Authentication/Authorization (ALWAYS Cache)

```python
# CORRECT: User resolved once per request
def get_current_user(
    token: str = Security(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.token == token).first()
    if not user:
        raise HTTPException(401)
    return user

def require_admin(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403)
    return user

# get_current_user called ONCE — result cached
# require_admin receives the cached user
```

### Request Context (ALWAYS Cache)

```python
def get_request_context(request: Request):
    return {
        "request_id": request.headers.get("X-Request-ID", str(uuid4())),
        "client_ip": request.client.host,
        "user_agent": request.headers.get("User-Agent"),
    }

# Single resolution, shared across all deps that need it
```

### Configuration (SHOULD Cache)

```python
def get_settings():
    # This could read from environment, file, or database
    # Cache to avoid repeated I/O
    return Settings()

# Cached per-request — settings don't change during a request
# If settings rarely change, consider application-level caching
```

---

## When NOT to Cache

### Random/Unique Values

```python
# BAD: Caching gives same value to all injectors
def get_unique_id():
    return str(uuid4())

@app.get("/")
def route(
    a: str = Depends(get_unique_id, use_cache=True),  # Same ID
    b: str = Depends(get_unique_id, use_cache=True),  # Same ID
):
    return {"a": a, "b": b}  # a == b — probably not intended

# GOOD: Don't cache unique values
@app.get("/")
def route(
    a: str = Depends(get_unique_id, use_cache=False),
    b: str = Depends(get_unique_id, use_cache=False),
):
    return {"a": a, "b": b}  # a != b
```

### Side-Effect Dependencies (When Multiple Calls Needed)

```python
# If you need the dependency to execute its side effects
# each time it's injected, don't cache

call_count = 0

def increment_counter():
    global call_count
    call_count += 1
    return call_count

# With caching: counter incremented once
# Without caching: counter incremented per injection
```

### Time-Sensitive Values

```python
# BAD: Cached timestamp is stale
def get_timestamp():
    return time.time()

# Route receives the same timestamp for all deps
# If timing matters, don't cache

# BETTER: Don't cache, or use middleware
def get_timestamp():
    return time.time()

@app.get("/")
def route(
    start: float = Depends(get_timestamp, use_cache=False),
):
    # Fresh timestamp per injection
    ...
```

### Per-Dependency Configuration

```python
# If different injectors need different configurations
def get_db_for_users():
    return SessionLocal(bind=user_engine)

def get_db_for_orders():
    return SessionLocal(bind=order_engine)

# These are different callables — cached separately regardless
# But if you had a parameterized version:
def get_db(engine_name: str):
    engines = {"users": user_engine, "orders": order_engine}
    return SessionLocal(bind=engines[engine_name])
```

---

## Cache Invalidation

### Per-Request Cache (Automatic)

```python
# FastAPI automatically invalidates cache at the start of each request
# No manual invalidation needed for per-request caching

# Request 1: get_db() called → cached → reused → cleanup
# Request 2: get_db() called → cached → reused → cleanup
# Cache is fresh for each request
```

### Manual Cache Invalidation (Global Cache)

```python
# For application-level caches that persist across requests:

class Cache:
    def __init__(self):
        self._store: dict[str, Any] = {}
        self._timestamps: dict[str, float] = {}

    def get(self, key: str, ttl: int = 300) -> Any | None:
        if key in self._store:
            if time.time() - self._timestamps[key] < ttl:
                return self._store[key]
            else:
                del self._store[key]
                del self._timestamps[key]
        return None

    def set(self, key: str, value: Any):
        self._store[key] = value
        self._timestamps[key] = time.time()

    def invalidate(self, key: str):
        self._store.pop(key, None)
        self._timestamps.pop(key, None)

    def clear(self):
        self._store.clear()
        self._timestamps.clear()

cache = Cache()

def get_cached_user(user_id: int, db: Session = Depends(get_db)):
    cached = cache.get(f"user:{user_id}")
    if cached:
        return cached
    user = db.query(User).get(user_id)
    if user:
        cache.set(f"user:{user_id}", user)
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    cache.invalidate(f"user:{user_id}")  # Invalidate cache
    return user
```

### Dependency Override as Cache Invalidation

```python
# Override dependency for a single test
app.dependency_overrides[get_db] = get_test_db

# "Invalidate" by clearing overrides
app.dependency_overrides.clear()
```

---

## Request-Scoped Dependencies

Request-scoped dependencies use FastAPI's DI caching to provide values that live for exactly one request.

### Using yield Dependencies for Request Scope

```python
def get_request_context():
    """Request-scoped context via yield dependency."""
    context = {
        "id": str(uuid4()),
        "start_time": time.time(),
        "db_queries": [],
    }
    try:
        yield context
    finally:
        # Log everything on request completion
        elapsed = time.time() - context["start_time"]
        logger.info(
            f"Request {context['id']}: {elapsed:.3f}s, "
            f"{len(context['db_queries'])} queries"
        )

@app.get("/items/")
def list_items(
    ctx: dict = Depends(get_request_context),
    db: Session = Depends(get_db),
):
    ctx["db_queries"].append("SELECT * FROM items")
    items = db.query(Item).all()
    return items
```

### Request ID Tracking

```python
import uuid

def get_request_id(request: Request):
    return request.headers.get("X-Request-ID", str(uuid.uuid4()))

def get_logger(request_id: str = Depends(get_request_id)):
    return LoggerAdapter(base_logger, extra={"request_id": request_id})

@app.get("/process/")
def process(
    request_id: str = Depends(get_request_id),
    logger: LoggerAdapter = Depends(get_logger),
):
    logger.info("Processing started")
    result = do_work()
    logger.info("Processing completed")
    return {"request_id": request_id, "result": result}
```

### User Context

```python
def get_current_user_context(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Build comprehensive user context for the request."""
    permissions = db.query(Permission).filter(
        Permission.user_id == user.id
    ).all()
    return UserContext(
        user=user,
        permissions=[p.name for p in permissions],
        is_admin=user.role == "admin",
        is_active=user.is_active,
    )

@app.get("/protected/")
def protected_route(ctx: UserContext = Depends(get_current_user_context)):
    if not ctx.is_active:
        raise HTTPException(403, "Account disabled")
    if "read" not in ctx.permissions:
        raise HTTPException(403, "No read permission")
    return {"user": ctx.user.name, "permissions": ctx.permissions}
```

---

## State Dependencies

FastAPI provides `request.state` for storing request-scoped data. Dependencies can populate and read from it.

### Using request.state

```python
from fastapi import Request

async def add_state_middleware(request: Request):
    """Add state to every request."""
    request.state.request_id = str(uuid.uuid4())
    request.state.user = None  # Will be set by auth dependency
    yield

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("Authorization")
    user = db.query(User).filter(User.token == token).first()
    request.state.user = user  # Store in state
    return user

@app.get("/info/")
def get_info(request: Request, user: User = Depends(get_current_user)):
    return {
        "request_id": request.state.request_id,
        "user": user.name,
        "client_ip": request.client.host,
    }
```

### State as Shared Cache

```python
# Dependencies can share data via request.state
def load_config(request: Request):
    if not hasattr(request.state, "config"):
        request.state.config = Config.load()
    return request.state.config

def get_theme(request: Request, config: dict = Depends(load_config)):
    if not hasattr(request.state, "theme"):
        request.state.theme = Theme.from_config(config["theme"])
    return request.state.theme

# Both dependencies share the same config through request.state
# No duplicate loading
```

### State with Middleware Integration

```python
@app.middleware("http")
async def state_middleware(request: Request, call_next):
    request.state.start_time = time.time()
    request.state.request_id = str(uuid.uuid4())

    response = await call_next(request)

    elapsed = time.time() - request.state.start_time
    response.headers["X-Request-ID"] = request.state.request_id
    response.headers["X-Process-Time"] = f"{elapsed:.3f}"
    return response

# Dependencies can now access state set by middleware
def get_timing(request: Request):
    return {
        "start_time": request.state.start_time,
        "request_id": request.state.request_id,
    }
```

---

## Advanced Caching Patterns

### TTL-Based Dependency Cache

```python
import time

class TTLCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self._cache: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Any | None:
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            del self._cache[key]
        return None

    def set(self, key: str, value: Any):
        self._cache[key] = (value, time.time())

ttl_cache = TTLCache(ttl_seconds=60)

def get_exchange_rate(currency: str):
    cached = ttl_cache.get(f"rate:{currency}")
    if cached:
        return cached
    rate = fetch_rate_from_api(currency)
    ttl_cache.set(f"rate:{currency}", rate)
    return rate
```

### Conditional Caching

```python
def get_data(skip_cache: bool = Query(False)):
    if skip_cache:
        return fetch_fresh_data()  # Bypass any caching
    return get_cached_data()
```

### Layered Caching

```python
# Layer 1: FastAPI per-request cache (Depends default)
# Layer 2: Redis cache (application-wide)
# Layer 3: Database (source of truth)

def get_user(user_id: int, db: Session = Depends(get_db)):
    # Layer 2: Check Redis
    cached = redis.get(f"user:{user_id}")
    if cached:
        return User.parse_raw(cached)

    # Layer 3: Query database
    user = db.query(User).get(user_id)

    # Store in Redis for next request
    if user:
        redis.set(f"user:{user_id}", user.json(), ex=300)

    return user

# Layer 1 is automatic via Depends caching
# If get_user is called multiple times in the same request,
# the same user object is returned
```

### Cache Warming

```python
@app.on_event("startup")
async def warm_cache():
    """Pre-populate cache on application startup."""
    db = SessionLocal()
    try:
        # Cache frequently accessed data
        users = db.query(User).filter(User.is_active == True).all()
        for user in users:
            cache.set(f"user:{user.id}", user.json(), ex=600)
    finally:
        db.close()
```

---

## Best Practices

### 1. Understand When Dependencies Are Cached

```python
# Dependencies are cached per-request by default
# This means:
def get_db(): ...  # Called once per request

def get_user_repo(db=Depends(get_db)): ...
def get_order_repo(db=Depends(get_db)): ...

# get_db is called ONCE — both repos share the same session
# This is correct and desired behavior
```

### 2. Use use_cache=False Deliberately

```python
# Only use when you genuinely need separate instances
def get_db_connection():
    return create_connection()

# Two different DB connections
def route(
    read_conn=Depends(get_db_connection, use_cache=False),
    write_conn=Depends(get_db_connection, use_cache=False),
):
    ...
```

### 3. Don't Fight the Caching

```python
# BAD: Trying to prevent caching for no reason
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# BAD: Overriding caching unnecessarily
def route(db=Depends(get_db, use_cache=False)):
    # Now each Depends(get_db) creates a new session
    # This breaks shared session pattern!
    ...
```

### 4. Use State for Cross-Dependency Communication

```python
# Instead of passing data through dependency chains,
# use request.state for truly shared data

def dependency_a(request: Request):
    request.state.shared_data = compute_expensive()

def dependency_b(request: Request):
    data = request.state.shared_data  # No dependency on dependency_a
```

### 5. Document Caching Decisions

```python
def get_db():
    """
    Database session dependency.
    Cached per-request: Yes (default).
    All dependencies using this share the same session.
    Session is closed after request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## Interview Questions

### Q1: What is the default caching behavior of `Depends()`?
**Answer:** Dependencies are cached per-request by default (`use_cache=True`). The resolved value is reused for all parameters that depend on the same callable within a single request.

### Q2: How does per-request caching differ from global caching?
**Answer:** Per-request caching resolves and caches a dependency once per HTTP request. Global caching (like `lru_cache`) persists across all requests. Per-request is safer for mutable state; global is suitable for immutable data.

### Q3: When should you use `use_cache=False`?
**Answer:** When you need distinct instances for each injection point in the same request. Examples: multiple independent database connections, unique identifiers, or when the dependency has side effects that must execute multiple times.

### Q4: Why are database sessions typically cached?
**Answer:** Caching ensures all dependencies in a request share the same database session/transaction. This maintains consistency, prevents connection leaks, and ensures proper transaction management.

### Q5: What happens to the cache when a request finishes?
**Answer:** The per-request cache is discarded entirely. Each new request starts with an empty cache. This is by design — it prevents stale data from leaking between requests.

### Q6: Can you implement application-level caching with FastAPI DI?
**Answer:** Yes. Use module-level variables, `functools.lru_cache`, or external caching systems (Redis, memcached). FastAPI's `Depends()` only provides per-request caching.

### Q7: How does `request.state` relate to dependency caching?
**Answer:** `request.state` is a separate mechanism for storing request-scoped data. Dependencies can populate it, and other dependencies or route handlers can read it. It persists for the entire request lifecycle.

### Q8: What is the difference between caching and memoization?
**Answer:** Caching stores computed results for reuse. Memoization is a specific form of caching based on function arguments. FastAPI's `Depends()` caching is simpler — it caches the result per callable per request.

### Q9: Can dependency caching cause stale data issues?
**Answer:** Per-request caching is too short-lived for stale data. However, application-level caches (Redis, lru_cache) can serve stale data. Use TTL and invalidation strategies.

### Q10: How do you invalidate FastAPI's dependency cache?
**Answer:** You cannot directly invalidate per-request cache — it's automatic. For application-level caches, implement explicit invalidation (delete keys on updates) or use TTL-based expiration.

### Q11: What is the relationship between `use_cache` and dependency overrides?
**Answer:** Dependency overrides replace the dependency entirely. The override is still cached per-request. If the original was cached, the override is also cached.

### Q12: Can yield dependencies be cached?
**Answer:** Yes. Yield dependencies with `use_cache=True` are resolved once and cleaned up once after the request. With `use_cache=False`, each injection creates and cleans up independently.

### Q13: When would you use `request.state` over dependency caching?
**Answer:** Use `request.state` when you need to share data between dependencies and middleware, or when you want explicit control over what's stored. Use dependency caching when you want transparent, automatic reuse.

### Q14: How do you implement a cache warming strategy?
**Answer:** Use FastAPI's startup event to pre-populate caches with frequently accessed data. This reduces cold-start latency for the first requests after deployment.

### Q15: What is layered caching?
**Answer:** Using multiple cache layers at different scopes: per-request (Depends), application-wide (Redis), and persistent (database). Each layer is checked in order, with the fastest/most local layer checked first.

---

## Summary

FastAPI's dependency caching is per-request by default, which is the correct behavior for most dependencies. Understanding when to cache and when not to cache is crucial for building correct applications. Use `request.state` for cross-dependency communication, and implement application-level caching separately when needed. Always document your caching decisions.
