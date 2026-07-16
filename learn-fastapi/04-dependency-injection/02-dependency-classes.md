# Class-Based Dependencies in FastAPI

## Table of Contents

1. [What are Class-Based Dependencies](#what-are-class-based-dependencies)
2. [The `__call__` Protocol](#the-call-protocol)
3. [Injectable Services](#injectable-services)
4. [Repository Pattern with DI](#repository-pattern-with-di)
5. [Service Layer Pattern](#service-layer-pattern)
6. [Using Classes with Depends()](#using-classes-with-depends)
7. [Class Dependencies with Init Params](#class-dependencies-with-init-params)
8. [Advanced Patterns](#advanced-patterns)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## What are Class-Based Dependencies

While function-based dependencies are sufficient for simple cases, class-based dependencies provide significant advantages for complex applications:

- **State management** — classes can hold configuration and state
- **Method organization** — related logic grouped together
- **Testability** — mock the entire class
- **Lifecycle management** — `__init__` for setup, `__call__` for per-request use
- **Type safety** — full IDE support for autocompletion

### Function vs Class Dependencies

```python
# Function-based dependency
def get_user_service():
    db = SessionLocal()
    return UserService(db=db)

# Class-based dependency
class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int):
        return self.db.query(User).get(user_id)

    def create_user(self, data: dict):
        user = User(**data)
        self.db.add(user)
        self.db.commit()
        return user

# Both used the same way
@app.get("/users/{user_id}")
def read_user(user_id: int, service: UserService = Depends(UserService)):
    return service.get_user(user_id)
```

---

## The `__call__` Protocol

When you pass a class to `Depends()`, FastAPI calls `ClassName()` which invokes `__init__`. But you can also make instances callable using `__call__`.

### How Depends() Handles Classes

```python
class MyDependency:
    def __init__(self):
        print("Init called")

    def __call__(self):
        print("Call called")
        return "result"

# FastAPI does: instance = MyDependency() then calls instance()
dep = Depends(MyDependency)
# Output: "Init called" (during resolution)
# Then: "Call called" (when resolving the dependency)
```

### Callable Class Pattern

```python
class DatabaseConnector:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port
        )

    def __call__(self) -> psycopg2.extensions.connection:
        if self.connection is None:
            self.connect()
        return self.connection

# Usage
connector = DatabaseConnector(host="localhost", port=5432)

@app.get("/users/")
def list_users(conn: psycopg2.extensions.connection = Depends(connector)):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    return cur.fetchall()
```

### Async Callable Classes

```python
class AsyncDBPool:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool = None

    async def initialize(self):
        self.pool = await asyncpg.create_pool(self.dsn)

    async def __call__(self) -> asyncpg.Connection:
        if self.pool is None:
            await self.initialize()
        return await self.pool.acquire()

# Async callable class — __call__ must be async
pool = AsyncDBPool(dsn="postgresql://localhost/mydb")

@app.get("/items/")
async def list_items(conn: asyncpg.Connection = Depends(pool)):
    return await conn.fetch("SELECT * FROM items")
```

---

## Injectable Services

Class-based dependencies are ideal for creating injectable service classes.

### Basic Injectable Service

```python
from pydantic import BaseModel
from sqlalchemy.orm import Session

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, data: CreateUserRequest) -> UserResponse:
        user = User(
            name=data.name,
            email=data.email,
            hashed_password=hash_password(data.password)
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return UserResponse.from_orm(user)

    def get_user(self, user_id: int) -> UserResponse | None:
        user = self.db.query(User).get(user_id)
        return UserResponse.from_orm(user) if user else None

    def list_users(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        users = self.db.query(User).offset(skip).limit(limit).all()
        return [UserResponse.from_orm(u) for u in users]

    def update_user(self, user_id: int, data: dict) -> UserResponse | None:
        user = self.db.query(User).get(user_id)
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return UserResponse.from_orm(user)

    def delete_user(self, user_id: int) -> bool:
        user = self.db.query(User).get(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db=db)

@app.post("/users/", response_model=UserResponse)
def create_user(
    data: CreateUserRequest,
    service: UserService = Depends(get_user_service),
):
    return service.create_user(data)

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Multi-Service Composition

```python
class NotificationService:
    def __init__(self, email_client: EmailClient, sms_client: SMSClient):
        self.email = email_client
        self.sms = sms_client

    def notify_user(self, user: User, message: str):
        self.email.send(user.email, message)
        if user.phone:
            self.sms.send(user.phone, message)

class OrderService:
    def __init__(
        self,
        db: Session,
        user_service: UserService,
        notification_service: NotificationService,
        payment_gateway: PaymentGateway,
    ):
        self.db = db
        self.user_service = user_service
        self.notification = notification_service
        self.payment = payment_gateway

    def create_order(self, user_id: int, items: list[dict]) -> Order:
        user = self.user_service.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        total = sum(item["price"] * item["quantity"] for item in items)
        self.payment.charge(user_id, total)

        order = Order(user_id=user_id, items=items, total=total)
        self.db.add(order)
        self.db.commit()

        self.notification.notify_user(user, f"Order #{order.id} confirmed!")
        return order

def get_order_service(
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
    notification: NotificationService = Depends(get_notification_service),
    payment: PaymentGateway = Depends(get_payment_gateway),
) -> OrderService:
    return OrderService(
        db=db,
        user_service=user_service,
        notification_service=notification,
        payment_gateway=payment,
    )
```

---

## Repository Pattern with DI

The Repository Pattern abstracts data access behind an interface. DI makes it swappable.

### Abstract Repository

```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        ...

    @abstractmethod
    def create(self, data: dict) -> User:
        ...

    @abstractmethod
    def update(self, user_id: int, data: dict) -> User | None:
        ...

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        ...

    @abstractmethod
    def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        ...
```

### SQL Repository Implementation

```python
class SQLUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, data: dict) -> User:
        user = User(**data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: int, data: dict) -> User | None:
        user = self.get_by_id(user_id)
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

    def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.db.query(User).offset(skip).limit(limit).all()
```

### In-Memory Repository (for testing)

```python
class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users: dict[int, User] = {}
        self.counter = 0

    def get_by_id(self, user_id: int) -> User | None:
        return self.users.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        return next(
            (u for u in self.users.values() if u.email == email),
            None,
        )

    def create(self, data: dict) -> User:
        self.counter += 1
        user = User(id=self.counter, **data)
        self.users[user.id] = user
        return user

    def update(self, user_id: int, data: dict) -> User | None:
        user = self.users.get(user_id)
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        return user

    def delete(self, user_id: int) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

    def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        users = list(self.users.values())
        return users[skip:skip + limit]
```

### Wiring with DI

```python
# Production dependency
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return SQLUserRepository(db)

# Test dependency
def get_test_user_repository() -> UserRepository:
    return InMemoryUserRepository()

# Route using the abstract interface
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repository),
):
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# In tests:
# app.dependency_overrides[get_user_repository] = get_test_user_repository
```

---

## Service Layer Pattern

The Service Layer Pattern puts business logic in service classes that coordinate between repositories and external systems.

### Service Interface

```python
class IUserService(ABC):
    @abstractmethod
    def register(self, data: RegisterRequest) -> UserResponse:
        ...

    @abstractmethod
    def authenticate(self, email: str, password: str) -> str:
        ...

    @abstractmethod
    def get_profile(self, user_id: int) -> UserResponse:
        ...
```

### Service Implementation

```python
class UserService(IUserService):
    def __init__(
        self,
        user_repo: UserRepository,
        auth_service: AuthService,
        email_service: EmailService,
    ):
        self.user_repo = user_repo
        self.auth = auth_service
        self.email = email_service

    def register(self, data: RegisterRequest) -> UserResponse:
        existing = self.user_repo.get_by_email(data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed = self.auth.hash_password(data.password)
        user = self.user_repo.create({
            "name": data.name,
            "email": data.email,
            "hashed_password": hashed,
        })

        self.email.send_welcome(user.email, user.name)
        return UserResponse.from_orm(user)

    def authenticate(self, email: str, password: str) -> str:
        user = self.user_repo.get_by_email(email)
        if not user or not self.auth.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return self.auth.create_access_token(user.id)

    def get_profile(self, user_id: int) -> UserResponse:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.from_orm(user)

# DI wiring
def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
    auth: AuthService = Depends(get_auth_service),
    email: EmailService = Depends(get_email_service),
) -> IUserService:
    return UserService(user_repo=user_repo, auth_service=auth, email_service=email)
```

---

## Using Classes with Depends()

### Direct Class Usage

```python
class QueryParams:
    def __init__(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        search: str | None = Query(None, max_length=100),
        sort_by: str = Query("created_at"),
        order: str = Query("desc", regex="^(asc|desc)$"),
    ):
        self.skip = skip
        self.limit = limit
        self.search = search
        self.sort_by = sort_by
        self.order = order

@app.get("/users/")
def list_users(params: QueryParams = Depends()):
    # All params are validated and parsed by Pydantic
    ...
```

### Class with Dependencies

```python
class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1),
        per_page: int = Query(20, ge=1, le=100),
        db: Session = Depends(get_db),  # This works!
    ):
        self.page = page
        self.per_page = per_page
        self.offset = (page - 1) * per_page
        self.db = db

    def paginate(self, query):
        return query.offset(self.offset).limit(self.per_page)
```

**Important:** When using a class as a dependency with sub-dependencies, the class's `__init__` parameters that are `Depends()` are resolved by FastAPI.

---

## Class Dependencies with Init Params

### Configuration at Init Time

```python
class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = {}

    def __call__(self, request: Request):
        client_ip = request.client.host
        now = time.time()

        if client_ip not in self.requests:
            self.requests[client_ip] = []

        # Clean old entries
        self.requests[client_ip] = [
            t for t in self.requests[client_ip]
            if now - t < self.window_seconds
        ]

        if len(self.requests[client_ip]) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Too many requests")

        self.requests[client_ip].append(now)

# Different rate limits for different routes
strict_limiter = RateLimiter(max_requests=10, window_seconds=60)
relaxed_limiter = RateLimiter(max_requests=100, window_seconds=60)

@app.get("/sensitive/")
def sensitive_route(_: None = Depends(strict_limiter)):
    return {"message": "sensitive data"}

@app.get("/public/")
def public_route(_: None = Depends(relaxed_limiter)):
    return {"message": "public data"}
```

### Factory Pattern with Classes

```python
class PermissionChecker:
    def __init__(self, required_permissions: list[str]):
        self.required_permissions = required_permissions

    def __call__(self, current_user: User = Depends(get_current_user)):
        user_permissions = set(current_user.permissions)
        required = set(self.required_permissions)

        if not required.issubset(user_permissions):
            missing = required - user_permissions
            raise HTTPException(
                status_code=403,
                detail=f"Missing permissions: {missing}"
            )
        return current_user

# Usage with specific permissions
admin_only = PermissionChecker(["admin"])
editor_or_admin = PermissionChecker(["editor", "admin"])

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    user: User = Depends(admin_only),
):
    ...

@app.post("/articles/")
def create_article(
    article: ArticleCreate,
    user: User = Depends(editor_or_admin),
):
    ...
```

---

## Advanced Patterns

### Scoped Dependencies

```python
class ScopedService:
    _instance = None

    def __init__(self):
        self.request_id = id(self)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls):
        cls._instance = None
```

### Dependency with Lifecycle

```python
class ConnectionPool:
    def __init__(self, min_size: int = 5, max_size: int = 20):
        self.min_size = min_size
        self.max_size = max_size
        self.pool = []

    async def startup(self):
        for _ in range(self.min_size):
            conn = await self._create_connection()
            self.pool.append(conn)

    async def shutdown(self):
        for conn in self.pool:
            await conn.close()
        self.pool.clear()

    async def _create_connection(self):
        return await asyncpg.connect(settings.DATABASE_URL)

    async def acquire(self):
        if self.pool:
            return self.pool.pop()
        if len(self.pool) < self.max_size:
            return await self._create_connection()
        raise RuntimeError("Pool exhausted")

    async def release(self, conn):
        self.pool.append(conn)

# Usage with lifespan
pool = ConnectionPool()

@app.on_event("startup")
async def startup():
    await pool.startup()

@app.on_event("shutdown")
async def shutdown():
    await pool.shutdown()

async def get_connection():
    conn = await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)
```

### Multi-Implementation Pattern

```python
class CacheBackend(ABC):
    @abstractmethod
    async def get(self, key: str) -> str | None: ...
    @abstractmethod
    async def set(self, key: str, value: str, ttl: int = 300): ...

class RedisCache(CacheBackend):
    async def get(self, key: str): ...
    async def set(self, key: str, value: str, ttl: int = 300): ...

class MemcachedCache(CacheBackend):
    async def get(self, key: str): ...
    async def set(self, key: str, value: str, ttl: int = 300): ...

class LocalCache(CacheBackend):
    async def get(self, key: str): ...
    async def set(self, key: str, value: str, ttl: int = 300): ...

def get_cache_backend() -> CacheBackend:
    if settings.CACHE_BACKEND == "redis":
        return RedisCache(url=settings.REDIS_URL)
    elif settings.CACHE_BACKEND == "memcached":
        return MemcachedCache(host=settings.MEMCACHED_HOST)
    else:
        return LocalCache()
```

---

## Best Practices

### 1. Separate Configuration from Business Logic

```python
# BAD
class UserService:
    def __init__(self):
        self.db = SessionLocal(url="postgresql://...")  # config in service

# GOOD
class UserService:
    def __init__(self, db: Session):
        self.db = db  # injected
```

### 2. Use Protocols for Loose Coupling

```python
from typing import Protocol

class UserRepository(Protocol):
    def get_by_id(self, user_id: int) -> User | None: ...

# Any class with matching methods satisfies this protocol
class SQLUserRepository:
    def get_by_id(self, user_id: int) -> User | None:
        ...

# No inheritance needed — structural subtyping
def get_repo(db: Session = Depends(get_db)) -> UserRepository:
    return SQLUserRepository(db)
```

### 3. Keep Dependencies Focused

```python
# BAD: God service
class AppService:
    def __init__(self, db, cache, mailer, sms, payment, auth, ...):
        ...

# GOOD: Composed from focused services
class OrderService:
    def __init__(self, order_repo, payment_service, notification_service):
        ...
```

### 4. Document Dependencies

```python
class InventoryService:
    """Manages product inventory operations.

    Dependencies:
        db: Database session for persisting inventory changes
        cache: Cache layer for fast inventory lookups
        event_bus: Event bus for publishing inventory events
    """
    def __init__(self, db: Session, cache: CacheBackend, event_bus: EventBus):
        ...
```

---

## Interview Questions

### Q1: When should you use class-based dependencies vs function-based?
**Answer:** Use class-based for complex dependencies with state, multiple methods, or configuration. Use function-based for simple, stateless dependencies. Classes are better when you need lifecycle management (init/cleanup).

### Q2: How does `Depends()` handle class instantiation?
**Answer:** When you pass a class to `Depends()`, FastAPI calls `ClassName()` to create an instance, resolving any `__init__` parameters through the DI system. The instance is then cached for the request.

### Q3: What is the `__call__` protocol and why is it important?
**Answer:** The `__call__` protocol allows class instances to be called like functions. When a class instance is a dependency, FastAPI calls `instance()` after instantiation. This enables classes to act as both configuration containers (init) and dependency providers (call).

### Q4: How do you implement the Repository Pattern with FastAPI DI?
**Answer:** Define an abstract base class (ABC) or Protocol for the repository. Create concrete implementations (SQL, in-memory, etc.). Use DI to inject the appropriate implementation. Override in tests to swap implementations.

### Q5: Can class `__init__` parameters be other dependencies?
**Answer:** Yes. FastAPI inspects `__init__` parameters and resolves any that have `Depends()` defaults, just like with regular functions.

### Q6: How do you handle service composition?
**Answer:** Inject services into other services via their constructors. FastAPI resolves the entire dependency graph, ensuring each service gets its dependencies. This creates a clean, testable composition.

### Q7: What is the advantage of class-based dependencies over function closures?
**Answer:** Classes provide better organization (methods vs closure variables), easier testing (mock the class), clearer intent, and the ability to have lifecycle methods. Closures are simpler but don't scale well.

### Q8: How do you make dependencies swappable?
**Answer:** Depend on abstract types (ABCs, Protocols). Create concrete implementations. Use DI overrides in tests. This follows the Dependency Inversion Principle.

### Q9: What is the difference between `Depends(Class)` and `Depends(instance)`?
**Answer:** `Depends(Class)` creates a new instance per resolution. `Depends(instance)` uses the pre-created instance. Use `Class` for fresh instances, `instance` for shared singletons.

### Q10: How do you test class-based dependencies?
**Answer:** Create mock implementations of the same interface. Override the dependency function that returns the class instance. Or mock individual methods on the class instance.

### Q11: Can a class dependency return different types from `__call__`?
**Answer:** `__call__` can return any type. The return type is what gets injected into route parameters. `__init__` returns the class instance. `__call__` returns whatever the dependency provides.

### Q12: How do you handle initialization errors in class dependencies?
**Answer:** Catch exceptions in `__init__` and either raise a meaningful error or use a factory function that handles the error. FastAPI will return 500 if initialization fails.

### Q13: What is the Service Layer Pattern?
**Answer:** A pattern where business logic lives in service classes that coordinate between repositories and external systems. Services encapsulate use cases and are injected via DI.

### Q14: How do you implement factory dependencies?
**Answer:** Create a function that returns a class instance or an instance method. Use `functools.partial` or closures to pre-configure the class. Pass the factory to `Depends()`.

### Q15: When would you use a class with `__call__` over a plain function?
**Answer:** When you need pre-configured state (set in `__init__`), multiple methods, lifecycle management, or the ability to swap implementations via interfaces.

---

## Summary

Class-based dependencies in FastAPI provide a structured approach to dependency injection that scales well with application complexity. They enable clean architecture patterns like Repository, Service Layer, and Strategy while maintaining full testability through DI overrides.
