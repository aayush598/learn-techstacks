# Sub-Dependencies in FastAPI

## Table of Contents

1. [Dependency Chains](#dependency-chains)
2. [Sub-Dependencies](#sub-dependencies)
3. [Dependency Tree Resolution](#dependency-tree-resolution)
4. [Caching Behavior](#caching-behavior)
5. [Override Dependencies](#override-dependencies)
6. [Dependency Overriding for Testing](#dependency-overriding-for-testing)
7. [Global Dependencies](#global-dependencies)
8. [Router-Level Dependencies](#router-level-dependencies)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## Dependency Chains

A dependency chain is a sequence of dependencies where each depends on the next.

### Linear Chain

```python
def get_config():
    return load_config()

def get_db_url(config: dict = Depends(get_config)):
    return config["database_url"]

def get_db(url: str = Depends(get_db_url)):
    engine = create_engine(url)
    return SessionLocal(bind=engine)

def get_current_user(db: Session = Depends(get_db)):
    return db.query(User).first()

# Chain: get_config → get_db_url → get_db → get_current_user
```

### Chain Resolution

```
Request arrives
  ↓
get_config()          → config
  ↓
get_db_url(config)    → db_url
  ↓
get_db(db_url)        → db_session
  ↓
get_current_user(db)  → user
  ↓
Route handler receives user
```

### Multi-Level Chain with Exception Handling

```python
def get_api_key(api_key: str = Header()):
    if not api_key:
        raise HTTPException(400, "Missing API key")
    return api_key

def validate_api_key(key: str = Depends(get_api_key)):
    if not key.startswith("sk-"):
        raise HTTPException(403, "Invalid API key format")
    return key

def get_user_from_key(
    validated_key: str = Depends(validate_api_key),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.api_key == validated_key).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user

@app.get("/data/")
def get_data(user: User = Depends(get_user_from_key)):
    return user.data

# Chain: get_api_key → validate_api_key → get_user_from_key → handler
# Any exception in the chain short-circuits — handler never called
```

---

## Sub-Dependencies

Sub-dependencies are dependencies that other dependencies themselves depend on.

### Basic Sub-Dependencies

```python
def get_database():
    """No sub-dependencies."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_database)):
    """Sub-dependency: get_database."""
    token = extract_token()
    user = db.query(User).filter(User.token == token).first()
    if not user:
        raise HTTPException(status_code=401)
    return user

def get_admin_user(user: User = Depends(get_current_user)):
    """Sub-dependency: get_current_user (which depends on get_database)."""
    if user.role != "admin":
        raise HTTPException(status_code=403)
    return user

@app.get("/admin/dashboard")
def admin_dashboard(admin: User = Depends(get_admin_user)):
    return {"admin": admin.name}

# Dependency tree:
# get_database
#   └── get_current_user
#         └── get_admin_user
#               └── admin_dashboard
```

### Multiple Sub-Dependencies Per Dependency

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_cache():
    cache = Redis()
    try:
        yield cache
    finally:
        cache.close()

def get_user_service(
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache),
):
    return UserService(db=db, cache=cache)

def get_order_service(
    user_service: UserService = Depends(get_user_service),
    db: Session = Depends(get_db),  # Same get_db — cached, reused
):
    return OrderService(user_service=user_service, db=db)

@app.get("/orders/")
def list_orders(service: OrderService = Depends(get_order_service)):
    return service.get_all()

# Tree:
# get_db ← shared (called once)
#   ├── get_user_service
#   │     └── get_order_service
#   └── get_order_service ← second dep resolved from cache
# get_cache
#   └── get_user_service
```

### Deep Nesting

```python
def get_settings():
    return Settings()

def get_db_url(settings=Depends(get_settings)):
    return settings.DATABASE_URL

def get_engine(url=Depends(get_db_url)):
    return create_engine(url)

def get_session_factory(engine=Depends(get_engine)):
    return sessionmaker(bind=engine)

def get_db(factory=Depends(get_session_factory)):
    session = factory()
    try:
        yield session
    finally:
        session.close()

def get_user_repo(db=Depends(get_db)):
    return UserRepository(db)

def get_user_service(repo=Depends(get_user_repo)):
    return UserService(repo)

def get_auth_service(user_service=Depends(get_user_service)):
    return AuthService(user_service)

# 9-level deep chain — each level adds one dependency
# FastAPI resolves them all automatically
```

---

## Dependency Tree Resolution

FastAPI resolves the entire dependency graph before calling the route handler.

### Resolution Algorithm

```
1. Inspect route handler signature
2. For each parameter with Depends():
   a. Check cache — if resolved, use cached value
   b. If not cached, inspect dependency's signature
   c. Recursively resolve sub-dependencies
   d. Call the dependency with resolved parameters
   e. Cache the result
3. Call route handler with all resolved values
```

### Tree Visualization

```
                    Route Handler
                   /      |      \
              dep_a     dep_b    dep_c
             /    \       |
        dep_d    dep_e  dep_f
         |
      dep_g

Resolution order: dep_g → dep_d → dep_a → dep_e → dep_f → dep_b → dep_c
Cleanup order: dep_c → dep_b → dep_f → dep_e → dep_a → dep_d → dep_g
```

### Resolution with Shared Dependencies

```python
def shared_dep():
    print("Shared dep called")
    return "shared"

def dep_a(common=Depends(shared_dep)):
    print("Dep A called")
    return f"a-{common}"

def dep_b(common=Depends(shared_dep)):
    print("Dep B called")
    return f"b-{common}"

@app.get("/")
def route(a=Depends(dep_a), b=Depends(dep_b)):
    return {"a": a, "b": b}

# Output:
# "Shared dep called"    ← called ONCE
# "Dep A called"
# "Dep B called"         ← shared_dep NOT called again

# Result: {"a": "a-shared", "b": "b-shared"}
```

### Resolution with Diamond Dependencies

```
        get_config
       /          \
get_db_url    get_cache_url
       \          /
        get_services

Diamond: get_config → get_db_url/get_cache_url → get_services
get_config resolved once, cached, shared by both branches
```

```python
def get_config():
    return {"db": "postgresql://...", "redis": "redis://..."}

def get_db_url(config=Depends(get_config)):
    return config["db"]

def get_cache_url(config=Depends(get_config)):
    return config["redis"]

def get_db(url=Depends(get_db_url)):
    return SessionLocal(url=url)

def get_cache(url=Depends(get_cache_url)):
    return Redis.from_url(url)

def get_services(
    db=Depends(get_db),
    cache=Depends(get_cache),
):
    return Services(db=db, cache=cache)

# get_config called once, result shared by get_db_url and get_cache_url
```

---

## Caching Behavior

### Per-Request Caching (Default)

```python
call_count = 0

def expensive_dep():
    global call_count
    call_count += 1
    print(f"Called {call_count} times")
    return "result"

def dep_a(x=Depends(expensive_dep)):
    return f"a-{x}"

def dep_b(x=Depends(expensive_dep)):
    return f"b-{x}"

@app.get("/")
def route(a=Depends(dep_a), b=Depends(dep_b)):
    # expensive_dep called ONCE (cached)
    # dep_a uses cached expensive_dep
    # dep_b uses cached expensive_dep
    return {"a": a, "b": b}
```

### use_cache=False

```python
call_count = 0

def uncached_dep():
    global call_count
    call_count += 1
    return f"result-{call_count}"

@app.get("/")
def route(
    a=Depends(uncached_dep, use_cache=False),
    b=Depends(uncached_dep, use_cache=False),
):
    # uncached_dep called TWICE
    # a="result-1", b="result-2"
    return {"a": a, "b": b}
```

### Caching and Type Hints

```python
# FastAPI caches by the combination of:
# 1. The dependency callable
# 2. The use_cache parameter
# 3. The class type (for class dependencies)

def dep():
    return "value"

# These are cached separately
def route(
    a=Depends(dep),           # cached
    b=Depends(dep),           # same cache as 'a'
    c=Depends(dep, use_cache=False),  # different cache
):
    ...
```

### When Caching Matters

```python
# Scenario 1: Database session — SHOULD be cached
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Without caching, each sub-dependency would create a new session!

# Scenario 2: Random value — should NOT be cached
import random

def get_random_id():
    return random.randint(1, 1000000)

# If cached, same ID returned for all uses in request
# If not cached, each use gets different ID
```

---

## Override Dependencies

### Basic Override

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    return ProductionDatabase()

@app.get("/users/")
def list_users(db=Depends(get_db)):
    return db.query(User).all()

# Override for testing
def get_test_db():
    return TestDatabase()

app.dependency_overrides[get_db] = get_test_db

# Now all routes using get_db will use get_test_db
```

### Override with Class Dependencies

```python
class ProductionUserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int):
        return self.db.query(User).get(user_id)

class MockUserService:
    def get_user(self, user_id: int):
        return User(id=user_id, name="Mock User")

def get_user_service(db: Session = Depends(get_db)):
    return ProductionUserService(db)

@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    service: ProductionUserService = Depends(get_user_service),
):
    return service.get_user(user_id)

# Override
app.dependency_overrides[get_user_service] = lambda: MockUserService()
```

### Conditional Overrides

```python
import os

# Override based on environment
if os.getenv("TESTING") == "1":
    app.dependency_overrides[get_db] = get_test_db
    app.dependency_overrides[get_cache] = get_test_cache
    app.dependency_overrides[get_email] = get_mock_email
```

---

## Dependency Overriding for Testing

### pytest Fixtures with Overrides

```python
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def test_db():
    db = create_test_database()
    yield db
    db.drop_all()

@pytest.fixture
def client(test_db):
    def _override_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = _override_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_user(client):
    response = client.post("/users/", json={
        "name": "Test User",
        "email": "test@example.com",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
```

### Multiple Override Levels

```python
@pytest.fixture
def mock_auth():
    def override():
        return User(id=1, name="Test User", role="admin")
    return override

@pytest.fixture
def mock_db():
    def override():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    return override

@pytest.fixture
def client(mock_auth, mock_db):
    app.dependency_overrides[get_current_user] = mock_auth
    app.dependency_overrides[get_db] = mock_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```

### Override for Specific Tests

```python
def test_with_real_db(client):
    # Uses real database (no override)
    response = client.get("/users/")
    assert response.status_code == 200

def test_with_mock_db(client, mock_db):
    # Override just for this test
    app.dependency_overrides[get_db] = mock_db
    response = client.get("/users/")
    assert response.status_code == 200
    app.dependency_overrides.clear()
```

### Nested Dependency Overrides

```python
# Original
def get_config():
    return {"db_url": PRODUCTION_URL}

def get_db(config=Depends(get_config)):
    return SessionLocal(config["db_url"])

# Override only the config — db automatically uses overridden config
def test_override_config():
    def mock_config():
        return {"db_url": TEST_URL}

    app.dependency_overrides[get_config] = mock_config
    # get_db is NOT overridden, but it receives the mock config
    # This works because get_db depends on get_config
```

---

## Global Dependencies

Global dependencies run for every route in the application.

### App-Level Dependencies

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

async def add_process_time_header(request: Request):
    start_time = time.time()
    yield
    process_time = time.time() - start_time
    # Note: can't modify response headers in dependencies
    # Use middleware for response headers instead

def verify_api_key(api_key: str = Header()):
    if api_key != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

# Global dependency — runs for ALL routes
app = FastAPI(dependencies=[Depends(verify_api_key)])

@app.get("/public/")
def public_route():
    # verify_api_key runs here too!
    return {"message": "This requires API key"}

@app.get("/admin/")
def admin_route():
    # verify_api_key runs here too!
    return {"message": "Admin area"}
```

### Global Dependencies with Yield

```python
async def request_context(request: Request):
    request.state.start_time = time.time()
    yield
    elapsed = time.time() - request.state.start_time
    logger.info(f"{request.method} {request.url.path} took {elapsed:.3f}s")

app = FastAPI(dependencies=[Depends(request_context)])
# Every request now gets timing information
```

### Multiple Global Dependencies

```python
app = FastAPI(
    dependencies=[
        Depends(verify_api_key),
        Depends(add_process_time),
        Depends(set_request_id),
    ]
)
# All three run for every route
```

### Global Dependencies with Sub-Dependencies

```python
def get_rate_limiter():
    return RateLimiter(max_requests=100, window=60)

def global_rate_limit(
    limiter: RateLimiter = Depends(get_rate_limiter),
    request: Request = None,
):
    if not limiter.is_allowed(request.client.host):
        raise HTTPException(429, "Rate limit exceeded")

app = FastAPI(dependencies=[Depends(global_rate_limit)])
# get_rate_limiter resolved once per request, shared by all routes
```

---

## Router-Level Dependencies

### Basic Router Dependencies

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(require_admin)],
)

@router.get("/dashboard/")
def admin_dashboard():
    return {"message": "Admin dashboard"}

@router.get("/users/")
def admin_users():
    return {"message": "User management"}

# require_admin runs for both routes
```

### Router with Sub-Dependencies

```python
def get_admin_db():
    """Separate DB connection for admin operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

admin_router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(get_admin_db)],
)

@router.get("/stats/")
def admin_stats(db: Session = Depends(get_admin_db)):
    # Uses the router's dependency
    stats = db.query(Stats).first()
    return stats
```

### Stacking Router Dependencies

```python
# Base router with auth
auth_router = APIRouter(dependencies=[Depends(get_current_user)])

# Admin router inherits auth + adds admin check
admin_router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(require_admin)],
    parent=auth_router,  # Inherits dependencies
)

# Super admin inherits everything
super_admin_router = APIRouter(
    prefix="/super-admin",
    dependencies=[Depends(require_super_admin)],
    parent=admin_router,
)
```

### Per-Route Dependency Override

```python
router = APIRouter(dependencies=[Depends(verify_api_key)])

@router.get("/public/")
def public():  # verify_api_key runs
    return {"public": True}

@router.get("/internal/", dependencies=[Depends(verify_internal)])
def internal():
    # verify_api_key + verify_internal both run
    return {"internal": True}

# Override just one route
@router.get("/override/", dependencies=[Depends(custom_auth)])
def override_auth():
    # Uses custom_auth instead of verify_api_key
    # (depends on how you structure the override)
    ...
```

---

## Best Practices

### 1. Minimize Dependency Depth

```python
# BAD: Unnecessarily deep chain
def get_config():
    return load_config()

def get_settings(config=Depends(get_config)):
    return Settings(config)

def get_db_url(settings=Depends(get_settings)):
    return settings.db_url

def get_engine(url=Depends(get_db_url)):
    return create_engine(url)

def get_session_factory(engine=Depends(get_engine)):
    return sessionmaker(engine)

def get_db(factory=Depends(get_session_factory)):
    return factory()

# GOOD: Flatten where possible
def get_db():
    settings = load_settings()
    engine = create_engine(settings.db_url)
    Session = sessionmaker(engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
```

### 2. Use Caching Wisely

```python
# GOOD: Shared dependencies are cached by default
def get_db(): ...

def get_user_repo(db=Depends(get_db)):
    return UserRepository(db)

def get_item_repo(db=Depends(get_db)):
    return ItemRepository(db)

# Both repos share the same db session — correct!
```

### 3. Document the Dependency Graph

```python
# In your README or docstrings:
"""
Dependency Graph:
─────────────────
get_config
├── get_db_config → get_db → get_user_repo → get_user_service
│                              get_item_repo → get_item_service
└── get_cache_config → get_cache
"""
```

### 4. Override Entire Chains in Tests

```python
# Instead of overriding every leaf dependency,
# override the top-level one:

# Override the service — all sub-dependencies are replaced
app.dependency_overrides[get_user_service] = mock_user_service
```

### 5. Keep Global Dependencies Minimal

```python
# BAD: Heavy global dependency
app = FastAPI(dependencies=[Depends(heavy_dependency)])

# GOOD: Only essential global deps
app = FastAPI(dependencies=[Depends(set_request_id)])
```

---

## Interview Questions

### Q1: What is a sub-dependency?
**Answer:** A sub-dependency is a dependency that another dependency itself depends on. FastAPI resolves them recursively before calling the parent dependency.

### Q2: How does FastAPI handle shared dependencies in a dependency tree?
**Answer:** Shared dependencies are resolved once per request and cached. All dependents receive the same resolved value. This prevents duplicate resource creation.

### Q3: What is the dependency resolution order?
**Answer:** Dependencies are resolved in topological order — leaf dependencies first. Cleanup happens in reverse (LIFO) order. The exact order follows depth-first traversal.

### Q4: Can you override a sub-dependency without overriding its dependents?
**Answer:** Yes. If you override a sub-dependency, its dependents automatically receive the overridden value because they depend on it through the DI system.

### Q5: What happens when you override a dependency that has sub-dependencies?
**Answer:** The override replaces the entire dependency. Sub-dependencies of the original are NOT automatically overridden unless the override depends on them.

### Q6: What is the difference between app-level and router-level dependencies?
**Answer:** App-level dependencies run for every route in the application. Router-level dependencies only run for routes in that router. Both are additive — they all run together.

### Q7: Can routers inherit dependencies from parent routers?
**Answer:** Yes, by setting the `parent` parameter. Child routers inherit all parent dependencies. You can add more dependencies at the child level.

### Q8: How do you test routes with deep dependency chains?
**Answer:** Override the top-level dependencies. FastAPI's DI system will use the overridden values throughout the chain. You don't need to override every sub-dependency.

### Q9: What is the performance impact of deep dependency trees?
**Answer:** Each level adds function call overhead and resolution time. However, caching mitigates most of the impact. Deep trees (>10 levels) may warrant flattening.

### Q10: Can global dependencies use yield?
**Answer:** Yes. Global yield dependencies set up resources for every request and clean them up after. Use them for request-scoped resources like timing, logging, or request IDs.

### Q11: How do you prevent a dependency from being cached?
**Answer:** Use `use_cache=False` in `Depends()`. This causes the dependency to be resolved fresh each time it's injected, even within the same request.

### Q12: Can you have circular sub-dependencies?
**Answer:** No. Circular dependencies cause infinite recursion. FastAPI will eventually raise a `RecursionError`. You must refactor to break the cycle.

### Q13: What happens if a sub-dependency fails during resolution?
**Answer:** The exception propagates up the chain. The parent dependency is never called. The route handler is never executed. FastAPI returns the appropriate error response.

### Q14: How do router-level dependencies interact with app-level dependencies?
**Answer:** Both are resolved together. App-level dependencies resolve first, then router-level. The route handler receives values from both. All share the same per-request cache.

### Q15: Can you selectively override dependencies for certain routes?
**Answer:** Use route-specific dependency overrides. You can override dependencies at the route level, router level, or app level. More specific overrides take precedence.

---

## Summary

Sub-dependencies and dependency trees are fundamental to FastAPI's DI system. Understanding resolution order, caching behavior, and override mechanisms allows you to build complex, testable applications. Keep dependency trees shallow when possible, leverage caching, and use overrides strategically for testing.
