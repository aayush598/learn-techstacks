# Dependency Injection Interview Questions

## 25+ Questions for FastAPI DI Mastery

---

## Fundamentals

### Q1: What is Dependency Injection and why does it matter?

**Answer:** Dependency Injection is a design pattern where an object receives its dependencies from an external source rather than creating them internally. It matters because:

- **Testability**: Easy to mock dependencies in tests
- **Loose coupling**: Components don't know about concrete implementations
- **Configuration management**: Dependencies configured in one place
- **Single Responsibility**: Each component focuses on its job
- **Reusability**: Dependencies shared across multiple consumers

```python
# Without DI
class UserService:
    def __init__(self):
        self.db = PostgreSQLDatabase()  # hardcoded

# With DI
class UserService:
    def __init__(self, db: Database):
        self.db = db  # injected — can be anything
```

---

### Q2: Explain how FastAPI's DI system works internally.

**Answer:** FastAPI's DI system operates through these steps:

1. **Inspection**: When a route is first called, FastAPI uses `inspect.signature()` to examine the function's parameters
2. **Detection**: Parameters with `Depends()` as their default value are identified as dependencies
3. **Resolution**: Dependencies are resolved recursively — sub-dependencies are resolved first
4. **Caching**: Resolved values are cached per-request to avoid duplicate resolution
5. **Injection**: Resolved values are passed to the route handler as keyword arguments
6. **Cleanup**: Yield dependencies are cleaned up after the response is sent

```python
# FastAPI internally does something like:
def resolve_dependency(dep_func, cache):
    if dep_func in cache:
        return cache[dep_func]
    # Resolve sub-dependencies first
    sub_deps = resolve_params(dep_func, cache)
    result = dep_func(**sub_deps)
    cache[dep_func] = result
    return result
```

---

### Q3: What is the difference between sync and async dependencies?

**Answer:**

| Aspect | Sync Dependencies | Async Dependencies |
|--------|-------------------|-------------------|
| Definition | `def dep()` | `async def dep()` |
| Execution | Threadpool | Event loop |
| Sub-dependencies | Can only have sync | Can have sync or async |
| Performance | Good for CPU-bound | Good for I/O-bound |
| Blocking | Runs in threadpool | Non-blocking |

```python
# Sync — runs in threadpool
def get_db():
    db = SessionLocal()  # Blocking I/O — safe in threadpool
    try:
        yield db
    finally:
        db.close()

# Async — runs on event loop
async def get_redis():
    redis = await aioredis.from_url(REDIS_URL)
    try:
        yield redis
    finally:
        await redis.close()
```

**Key rule**: Async dependencies can depend on sync sub-dependencies, but sync dependencies CANNOT depend on async sub-dependencies.

---

### Q4: What does `use_cache` do and when would you change it?

**Answer:** `use_cache` (default `True`) controls whether a dependency is resolved once per request or each time it's injected.

```python
# Cached (default) — resolved once
def get_db():
    return SessionLocal()

# Not cached — resolved each time
def get_unique_id():
    return str(uuid4())

@app.get("/")
def route(
    db1: Session = Depends(get_db, use_cache=True),   # same session
    db2: Session = Depends(get_db, use_cache=True),   # same session
    id1: str = Depends(get_unique_id, use_cache=False), # different ID
    id2: str = Depends(get_unique_id, use_cache=False), # different ID
):
    ...
```

Change `use_cache` to `False` when:
- You need distinct instances per injection
- The dependency has side effects that should run multiple times
- Values should be truly independent

---

## Yield Dependencies

### Q5: Explain yield dependencies and their lifecycle.

**Answer:** Yield dependencies are generator functions that implement the setup/teardown pattern:

```python
def get_db():
    # SETUP: runs when dependency is resolved
    db = SessionLocal()
    try:
        yield db  # HANDOVER: value injected into route handler
    finally:
        # TEARDOWN: runs after response is sent
        db.close()
```

**Lifecycle:**
1. Request arrives
2. Code before `yield` executes (setup)
3. Yielded value injected into route handler
4. Route handler executes
5. Response generated
6. Code after `yield` executes (teardown)
7. Response sent to client

**Guarantees:**
- Teardown runs even if handler raises exception
- Teardown runs even if setup raises exception (partially)
- Cleanup order is LIFO for multiple yield dependencies

---

### Q6: What is the cleanup order for multiple yield dependencies?

**Answer:** LIFO (Last In, First Out). Dependencies resolved last are cleaned up first.

```python
def dep_a():
    yield "A"
    print("Cleanup A")

def dep_b():
    yield "B"
    print("Cleanup B")

def dep_c():
    yield "C"
    print("Cleanup C")

@app.get("/")
def route(a=Depends(dep_a), b=Depends(dep_b), c=Depends(dep_c)):
    return "handler"

# Execution: A setup → B setup → C setup → handler → C cleanup → B cleanup → A cleanup
```

This is critical for resources like database transactions (close transaction before closing connection).

---

### Q7: How do you handle exceptions in yield dependencies?

**Answer:** Use try/except/finally:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"DB error: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected: {e}")
        raise
    finally:
        db.close()
```

If the cleanup code itself raises an exception, it can override the original response. Always handle or suppress exceptions in cleanup code.

---

## Dependency Trees

### Q8: How does FastAPI resolve dependency trees?

**Answer:** FastAPI resolves dependencies using depth-first traversal:

1. Inspect route handler signature
2. For each `Depends()` parameter:
   a. Check cache — use cached value if present
   b. Inspect the dependency's signature
   c. Recursively resolve its sub-dependencies
   d. Call the dependency
   e. Cache the result
3. Call route handler with all resolved values

```
Handler → dep_a → sub_1
                 sub_2 → sub_3
       → dep_b → sub_1 (cached)

Resolution order: sub_3 → sub_2 → sub_1 → dep_a → dep_b
```

---

### Q9: What happens with diamond-shaped dependency graphs?

**Answer:** A diamond graph occurs when multiple paths lead to the same dependency:

```
    get_config
   /          \
get_db    get_cache
   \          /
  get_services
```

FastAPI handles this correctly — `get_config` is resolved once, cached, and shared by both `get_db` and `get_cache`. The cache prevents redundant resolution.

---

### Q10: Can you have circular dependencies?

**Answer:** No. Circular dependencies cause infinite recursion. FastAPI will raise a `RecursionError`. You must refactor to break the cycle:

```python
# BAD: Circular
def dep_a(b=Depends(dep_b)): ...
def dep_b(a=Depends(dep_a)): ...

# GOOD: Break the cycle with a shared dependency
def get_shared():
    return SharedResource()

def dep_a(shared=Depends(get_shared)): ...
def dep_b(shared=Depends(get_shared)): ...
```

---

## Overriding and Testing

### Q11: How do you override dependencies for testing?

**Answer:** Use `app.dependency_overrides`:

```python
# Production dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test dependency
def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# In test
app.dependency_overrides[get_db] = get_test_db

# In test cleanup
app.dependency_overrides.clear()
```

---

### Q12: Can you override a dependency that has sub-dependencies?

**Answer:** Yes. When you override a dependency, its sub-dependencies are also replaced. The override is resolved independently with its own sub-dependency tree.

```python
def get_db_config():
    return {"url": PRODUCTION_URL}

def get_db(config=Depends(get_db_config)):
    return SessionLocal(config["url"])

# Override just the config — db uses overridden config automatically
def test_override():
    app.dependency_overrides[get_db_config] = lambda: {"url": TEST_URL}
    # get_db still runs, but with test config
```

---

### Q13: How do you test yield dependencies?

**Answer:**

```python
@pytest.fixture
def client(test_db):
    def override_db():
        try:
            yield test_db
        finally:
            pass  # Don't close — test fixture manages lifecycle

    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_endpoint(client):
    response = client.get("/items/")
    assert response.status_code == 200
```

---

## Advanced Patterns

### Q14: Explain the Repository Pattern with DI.

**Answer:** The Repository Pattern abstracts data access behind an interface:

```python
# Abstract interface
class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> User | None: ...

# SQL implementation
class SQLUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db
    def get_by_id(self, id: int):
        return self.db.query(User).get(id)

# Test implementation
class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
    def get_by_id(self, id: int):
        return self.users.get(id)

# DI wiring
def get_repo(db=Depends(get_db)) -> UserRepository:
    return SQLUserRepository(db)

# In tests: override get_repo to return InMemoryUserRepository
```

---

### Q15: What are global dependencies and when should you use them?

**Answer:** Global dependencies run for every route in the application:

```python
app = FastAPI(dependencies=[Depends(verify_api_key)])

# All routes require API key verification
@app.get("/users/")
def list_users(): ...  # API key checked

@app.get("/items/")
def list_items(): ...  # API key checked
```

Use for:
- Request ID generation
- API key verification
- Rate limiting
- Request logging/timing

Don't use for:
- Heavy initialization (use middleware)
- Route-specific logic (use route-level deps)

---

### Q16: How do router-level dependencies differ from app-level?

**Answer:**

```python
# App-level: runs for ALL routes
app = FastAPI(dependencies=[Depends(global_auth)])

# Router-level: runs only for routes in that router
admin_router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(require_admin)],
)

# Route-level: runs only for that specific route
@router.get("/sensitive/")
def sensitive(data=Depends(heavy_validation)):
    ...
```

Both types are resolved together — they're additive. A route inherits all ancestor dependencies.

---

### Q17: Can you use `Depends()` with class `__init__` parameters?

**Answer:** Yes:

```python
class Pagination:
    def __init__(
        self,
        page: int = Query(1, ge=1),
        per_page: int = Query(20, ge=1, le=100),
    ):
        self.page = page
        self.per_page = per_page
        self.offset = (page - 1) * per_page

@app.get("/items/")
def list_items(pagination: Pagination = Depends()):
    ...
```

FastAPI inspects `__init__` parameters and resolves any with `Depends()` or parameter classes (`Query`, `Header`, etc.).

---

### Q18: What are the limitations of FastAPI's DI?

**Answer:**

1. **No circular dependencies** — must be a DAG
2. **Async in sync limitation** — sync deps can't use async sub-deps
3. **Per-request caching only** — no built-in global caching
4. **No automatic scoping** — beyond request-level caching
5. **Signature inspection overhead** — minimal but exists
6. **No compile-time validation** — errors at runtime
7. **Complex debugging** — deep trees hard to trace
8. **Override side effects** — global state, affects all routes

---

### Q19: How do you handle parameterized dependencies?

**Answer:** Use factory functions or closures:

```python
# Factory pattern
def get_rate_limiter(max_requests: int, window: int):
    limiter = RateLimiter(max_requests, window)
    def _get_limiter():
        return limiter
    return _get_limiter

@app.get("/strict/")
def strict(limiter=Depends(get_rate_limiter(10, 60))):
    ...

@app.get("/relaxed/")
def relaxed(limiter=Depends(get_rate_limiter(100, 60))):
    ...
```

---

### Q20: How do you share state between dependencies without direct dependency?

**Answer:** Use `request.state`:

```python
def dep_a(request: Request):
    request.state.shared_value = "computed by A"

def dep_b(request: Request):
    # No dependency on dep_a, but accesses shared data
    value = request.state.shared_value
    return f"B using {value}"
```

---

### Q21: What is the difference between `Depends()` and middleware?

**Answer:**

| Aspect | Dependencies | Middleware |
|--------|-------------|-----------|
| Scope | Specific routes | All routes |
| Purpose | Provide values to handlers | Transform request/response |
| Resolution | Function signature | Wraps entire handler |
| Cleanup | yield dependencies | N/A |
| Override | Yes (dependency_overrides) | No |
| Best for | Auth, DB, services | Logging, CORS, compression |

---

### Q22: Can dependencies return different types based on context?

**Answer:** Yes:

```python
def get_user_role(user: User = Depends(get_current_user)):
    return user.role

def get_display_data(role: str = Depends(get_user_role)):
    if role == "admin":
        return AdminDashboard()
    else:
        return UserDashboard()

@app.get("/dashboard/")
def dashboard(data=Depends(get_display_data)):
    return data
```

---

### Q23: How do you implement feature flags with DI?

**Answer:**

```python
def get_feature_flags():
    return {
        "new_ui": True,
        "beta_api": False,
        "dark_mode": True,
    }

def require_feature(feature_name: str):
    def checker(flags=Depends(get_feature_flags)):
        if not flags.get(feature_name):
            raise HTTPException(404, "Feature not available")
    return checker

@app.get("/beta/", dependencies=[Depends(require_feature("beta_api"))])
def beta_endpoint():
    return {"message": "Beta feature"}
```

---

### Q24: How do you handle dependencies that need the Request object?

**Answer:** FastAPI can inject the `Request` directly:

```python
from fastapi import Request

def get_client_ip(request: Request):
    return request.client.host

def get_user_agent(request: Request):
    return request.headers.get("User-Agent")

@app.get("/info/")
def info(
    ip: str = Depends(get_client_ip),
    ua: str = Depends(get_user_agent),
):
    return {"ip": ip, "user_agent": ua}
```

---

### Q25: How do you debug dependency resolution issues?

**Answer:**

1. **Add logging to dependencies:**

```python
def get_db():
    logger.info("Resolving get_db dependency")
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.info("Cleaning up get_db dependency")
        db.close()
```

2. **Check dependency overrides:**

```python
@app.get("/debug/overrides")
def debug_overrides():
    return {str(k): str(v) for k, v in app.dependency_overrides.items()}
```

3. **Trace the dependency graph:**

```python
def trace_dep(name):
    def traced():
        logger.info(f"Resolving: {name}")
        return name
    return traced
```

4. **Use FastAPI's OpenAPI schema** to verify dependencies appear correctly

---

### Q26: What is the difference between DI and Service Locator patterns?

**Answer:**

**DI (FastAPI's approach):**
```python
def route(db=Depends(get_db)):
    # db is injected — route doesn't know how to create it
    return db.query(User).all()
```

**Service Locator:**
```python
from some_di_container import container

def route():
    db = container.get(Database)  # Route actively fetches dependency
    return db.query(User).all()
```

DI is preferred because:
- Dependencies are explicit (visible in signature)
- Easier to test (override at the DI level)
- Better IDE support
- Follows the Dependency Inversion Principle

---

### Q27: How would you implement dependency injection without FastAPI's `Depends()`?

**Answer:** Manual DI:

```python
class App:
    def __init__(self):
        self.db = Database(settings.DB_URL)
        self.cache = Redis(settings.REDIS_URL)
        self.user_service = UserService(self.db, self.cache)
        self.order_service = OrderService(self.db, self.user_service)

app = App()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return app.user_service.get_user(user_id)
```

Or use a DI library like `dependency-injector`:

```python
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    db = providers.Singleton(Database, url=settings.DB_URL)
    user_repo = providers.Factory(UserRepository, db=db)
    user_service = providers.Factory(UserService, repo=user_repo)
```

FastAPI's `Depends()` is the most Pythonic and framework-native approach.

---

### Q28: What performance considerations exist for DI in FastAPI?

**Answer:**

1. **Signature inspection** — happens once, cached internally
2. **Dependency resolution** — per-request, overhead is function calls
3. **Threadpool for sync deps** — context switching overhead
4. **Caching overhead** — dict lookup, minimal
5. **Deep dependency trees** — recursive resolution, stack overhead

**Benchmarks:**
- Simple dependency resolution: ~1-5 microseconds
- Threadpool overhead: ~10-50 microseconds
- Deep tree (10 levels): ~50-100 microseconds total

**Optimization:**
- Keep dependency trees shallow
- Use async dependencies for I/O-bound work
- Cache aggressively (default behavior)
- Avoid heavy computation in dependencies

---

### Q29: How do you handle dependencies in background tasks?

**Answer:** Background tasks run after the response is sent. Dependencies are resolved before the response:

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # This runs AFTER the response
    # Dependencies must be resolved before
    ...

@app.post("/notify/")
def notify(
    notification: NotificationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = db.query(User).get(notification.user_id)
    # Pass data explicitly to background task
    background_tasks.add_task(send_email, user.email, notification.message)
    return {"status": "queued"}
```

For background tasks that need DI, resolve dependencies explicitly and pass values.

---

### Q30: What are the security implications of DI in FastAPI?

**Answer:**

1. **Dependency overrides persist** — accidentally overriding in production is dangerous
2. **Global state in dependencies** — shared mutable state across requests
3. **Exception leaking** — dependencies may expose internal details
4. **Authentication bypass** — forgetting to add auth dependency

**Best practices:**
```python
# 1. Clear overrides after tests
@pytest.fixture(autouse=True)
def cleanup():
    yield
    app.dependency_overrides.clear()

# 2. Don't use global mutable state
# BAD
_cache = {}

# GOOD
def get_cache():
    return {}  # Fresh per-request

# 3. Validate dependencies exist
@app.get("/protected/")
def protected(user=Depends(get_current_user)):  # Don't forget this!
    ...
```

---

## Quick Reference Card

| Concept | Syntax | Default |
|---------|--------|---------|
| Basic dependency | `Depends(func)` | Cached |
| No-cache dependency | `Depends(func, use_cache=False)` | Not cached |
| Class dependency | `Depends(MyClass)` | Cached |
| Global dependency | `FastAPI(dependencies=[...])` | All routes |
| Router dependency | `APIRouter(dependencies=[...])` | Router routes |
| Override | `app.dependency_overrides[func] = mock` | N/A |
| Clear overrides | `app.dependency_overrides.clear()` | N/A |
| Yield dependency | `def dep(): ... yield ... finally: ...` | Setup/Teardown |
| Sub-dependency | Any `Depends()` in a dependency | Auto-resolved |
| Request object | `def dep(request: Request)` | Auto-injected |
