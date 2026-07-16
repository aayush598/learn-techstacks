# Common FastAPI Interview Questions - Detailed Answers

## Section 1: FastAPI Fundamentals

### 1. What is FastAPI and why is it fast?

FastAPI is a modern, high-performance Python web framework for building APIs. It's fast for three key reasons:

**ASGI Native**: FastAPI runs on ASGI (Asynchronous Server Gateway Interface) using uvicorn, which is significantly faster than WSGI frameworks like Flask/Django for I/O-bound operations. ASGI supports async/await natively, allowing concurrent request handling without threads.

**Starlette Foundation**: Built on Starlette, which provides the async routing, middleware, and request/response handling. Starlette is one of the fastest Python frameworks available.

**Pydantic Integration**: Request validation happens at the C-extension level via Pydantic v2's Rust core. Validation is compiled to efficient machine code rather than pure Python interpretation.

**Performance**: In benchmarks, FastAPI achieves 20,000-50,000+ requests/second (depending on endpoint complexity), comparable to Go and Node.js frameworks. This is 2-10x faster than Flask for I/O-bound workloads.

```python
# FastAPI achieves performance through:
# 1. Async I/O (non-blocking)
@app.get("/users")
async def get_users():  # Runs in event loop, not blocking
    users = await db.fetch_all("SELECT * FROM users")
    return users

# 2. Pydantic v2 Rust core validation
class User(BaseModel):  # Validated at C speed
    name: str
    age: int

# 3. Automatic OpenAPI generation (zero runtime cost)
# Schema generated at startup, not per-request
```

### 2. How does FastAPI compare to Flask and Django?

| Feature | FastAPI | Flask | Django |
|---------|---------|-------|--------|
| Async Support | Native | Limited (2.0+) | Limited (4.0+) |
| Performance | Very High | Medium | Medium |
| Type Safety | Built-in (Pydantic) | Optional | Optional |
| Auto Docs | OpenAPI + ReDoc | Manual | Manual |
| Dependency Injection | Built-in | Manual | Manual |
| Learning Curve | Medium | Low | High |
| Ecosystem | Growing | Large | Massive |
| ORM Integration | SQLAlchemy, Tortoise | SQLAlchemy | Django ORM |
| WebSocket | Built-in | Extensions | Limited |
| Enterprise Features | Basic | Via Extensions | Built-in |

**When to choose FastAPI**: High-performance APIs, microservices, data science APIs (ML model serving), async-heavy applications, teams that value type safety.

**When to choose Flask**: Simple APIs, rapid prototyping, when you need extensive third-party extensions, small teams.

**When to choose Django**: Full-stack applications, admin-heavy apps, when you need batteries-included (auth, ORM, admin), large teams.

### 3. What is ASGI and why does it matter?

ASGI (Asynchronous Server Gateway Interface) is the spiritual successor to WSGI. It defines how Python web applications communicate with web servers.

**WSGI (synchronous)**:
```python
# WSGI handles one request per thread
def application(environ, start_response):
    # Blocks the thread during I/O
    data = database_query()  # Thread waits here
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [data]
```

**ASGI (asynchronous)**:
```python
# ASGI handles many requests on one thread
async def application(scope, receive, send):
    # Non-blocking I/O, thread is free
    data = await database_query()  # Event loop runs other tasks
    await send({'type': 'http.response.body', 'body': data})
```

**Why it matters**:
- One ASGI worker can handle thousands of concurrent connections vs. hundreds with WSGI
- Native WebSocket support
- HTTP/2 support
- Better resource utilization (less memory per connection)

### 4. How does request validation work in FastAPI?

FastAPI uses Pydantic models for automatic request validation. The validation happens before your endpoint function is called:

```python
from pydantic import BaseModel, Field, field_validator

class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[\w.-]+@[\w.-]+\.\w+$')
    age: int = Field(..., ge=0, le=150)

    @field_validator('name')
    @classmethod
    def name_must_be_title(cls, v):
        if not v[0].isupper():
            raise ValueError('Name must start with uppercase')
        return v

@app.post("/users", status_code=201)
def create_user(user: CreateUserRequest):
    # user is already validated and typed
    return {"name": user.name, "email": user.email}
```

**Validation flow**:
1. Request arrives at FastAPI
2. FastAPI inspects the function signature
3. Pydantic model validates the request body/query params/path params
4. If validation fails, 422 Unprocessable Entity is returned with detailed errors
5. If validation passes, the validated model is injected into your function

### 5. What are the different parameter types in FastAPI?

```python
from fastapi import FastAPI, Query, Path, Body, Header, Cookie, Form, File, UploadFile

app = FastAPI()

# Path Parameters
@app.get("/users/{user_id}")
def get_user(user_id: int):  # Automatically parsed as int
    return {"user_id": user_id}

# Query Parameters
@app.get("/search")
def search(q: str, page: int = 1, limit: int = 20):
    return {"query": q, "page": page}

# Request Body
@app.post("/users")
def create_user(name: str, age: int):  # JSON body
    return {"name": name, "age": age}

# Form Data
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}

# File Upload
@app.post("/upload")
def upload(file: UploadFile = File(...)):
    return {"filename": file.filename}

# Headers
@app.get("/headers")
def check_headers(user_agent: str = Header(...)):
    return {"user_agent": user_agent}

# Cookies
@app.get("/cookies")
def check_cookies(session: str = Cookie(None)):
    return {"session": session}
```

### 6. How does dependency injection work in FastAPI?

FastAPI's dependency injection system is one of its most powerful features. Dependencies are functions or classes that provide resources (database connections, authentication, etc.) to your endpoints.

```python
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated

app = FastAPI()

# Simple dependency
def get_db():
    db = DatabaseConnection()
    try:
        yield db  # Provides the connection
    finally:
        db.close()  # Cleanup

# Authentication dependency
def get_current_user(token: str = Header(...)):
    user = decode_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# Dependency with parameters
def pagination(page: int = 1, limit: int = 20):
    return {"page": max(1, page), "limit": min(100, limit)}

# Nested dependencies
def get_admin_user(
    user: Annotated[User, Depends(get_current_user)]
) -> User:
    if user.role != "admin":
        raise HTTPException(403, "Admin required")
    return user

# Using dependencies
@app.get("/items")
def list_items(
    db: Annotated[DatabaseConnection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    pagination: dict = Depends(pagination),
):
    return db.query("SELECT * FROM items").paginate(**pagination)
```

**Key points**:
- Dependencies are called once per request (unless cached)
- Generator dependencies (with `yield`) support cleanup
- Dependencies can depend on other dependencies (chaining)
- `@lru_cache` or `CacheControl` can cache dependencies across requests

---

## Section 2: Pydantic and Validation

### 7. What are Pydantic models and why are they important?

Pydantic models are Python classes that use type hints for data validation and serialization. In FastAPI, they're the backbone of request/response validation.

```python
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

class Address(BaseModel):
    street: str
    city: str
    zip_code: str = Field(pattern=r'^\d{5}(-\d{4})?$')

class Order(BaseModel):
    id: int
    items: list[str] = Field(min_length=1)
    total: float = Field(gt=0)
    status: OrderStatus = OrderStatus.PENDING
    shipping_address: Address
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @model_validator(mode='after')
    def validate_total_matches_items(self):
        if self.total <= 0 and len(self.items) > 0:
            raise ValueError('Total must be positive when items exist')
        return self

# Pydantic v2 uses Rust core for validation (10-50x faster than v1)
# Serializes/deserializes automatically
order = Order(**json_data)  # Validates and creates
json_str = order.model_dump_json()  # Serializes to JSON
dict_data = order.model_dump()  # Converts to dict
```

### 8. What is the difference between Pydantic v1 and v2?

| Aspect | Pydantic v1 | Pydantic v2 |
|--------|-------------|-------------|
| Core | Pure Python | Rust (pydantic-core) |
| Performance | Baseline | 5-50x faster |
| Validation | `@validator` | `@field_validator` / `@model_validator` |
| Config | `class Config:` | `model_config = ConfigDict(...)` |
| Serialization | `.dict()` | `.model_dump()` |
| JSON Schema | Basic | Full JSON Schema support |
| Custom Types | `@validator` | `TypeAdapter` / `@field_serializer` |

```python
# Pydantic v1 (deprecated)
from pydantic import BaseModel, validator

class UserV1(BaseModel):
    name: str

    @validator('name')
    def validate_name(cls, v):
        return v.strip()

    class Config:
        orm_mode = True

# Pydantic v2 (current)
from pydantic import BaseModel, field_validator, ConfigDict

class UserV2(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        return v.strip()
```

### 9. How do you handle complex nested validation?

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Annotated

class SKU(BaseModel):
    code: str = Field(pattern=r'^[A-Z]{3}-\d{4}$')
    warehouse: str

class ProductVariant(BaseModel):
    name: str
    sku: SKU
    price: float = Field(gt=0)
    stock: int = Field(ge=0)

class Product(BaseModel):
    name: str
    variants: list[ProductVariant] = Field(min_length=1)
    tags: list[str] = Field(default_factory=list, max_length=10)

    @model_validator(mode='after')
    def validate_unique_skus(self):
        skus = [v.sku.code for v in self.variants]
        if len(skus) != len(set(skus)):
            raise ValueError('Duplicate SKUs found')
        return self

    @field_validator('tags')
    @classmethod
    def normalize_tags(cls, v):
        return [tag.lower().strip() for tag in v]

# Partial updates (PATCH)
from pydantic import BaseModel

class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = Field(default=None, gt=0)

# Merge partial updates
def update_product(product: Product, updates: ProductUpdate) -> Product:
    update_data = updates.model_dump(exclude_unset=True)
    return product.model_copy(update=update_data)
```

### 10. How do you create custom Pydantic types?

```python
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaMode
from pydantic_core import core_schema
from typing import Annotated

# Custom type with validation
class PositiveInt:
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.no_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.plain_serializer_function_ser_schema(int),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        return {"type": "integer", "minimum": 1}

    @classmethod
    def validate(cls, v):
        if not isinstance(v, int) or v <= 0:
            raise ValueError("Must be a positive integer")
        return v

# Reusable constrained types
PositiveIntType = Annotated[int, Field(gt=0)]
NonEmptyStr = Annotated[str, Field(min_length=1, max_length=255)]
EmailStr = Annotated[str, Field(pattern=r'^[\w.-]+@[\w.-]+\.\w+$')]

class Config:
    # Global config for all models
    str_strip_whitespace = True
    validate_default = True
    populate_by_name = True
```

---

## Section 3: Async/Await in Python

### 11. How does async/await work in Python?

Python's async/await is built on coroutines and an event loop:

```python
import asyncio

# Coroutine function
async def fetch_data(url: str) -> dict:
    # Event loop is free to run other tasks during await
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Running multiple coroutines concurrently
async def main():
    # Sequential (slow)
    data1 = await fetch_data("http://api1.com")
    data2 = await fetch_data("http://api2.com")

    # Concurrent (fast) - both run simultaneously
    data1, data2 = await asyncio.gather(
        fetch_data("http://api1.com"),
        fetch_data("http://api2.com"),
    )

# FastAPI handles the event loop automatically
@app.get("/aggregated")
async def aggregated_data():
    # This runs concurrently
    users, products = await asyncio.gather(
        fetch_users(),
        fetch_products(),
    )
    return {"users": users, "products": products}
```

**Key concepts**:
- `async def` defines a coroutine function
- `await` yields control back to the event loop
- Event loop schedules and runs coroutines
- `asyncio.gather()` runs coroutines concurrently
- Only I/O-bound operations benefit from async (not CPU-bound)

### 12. When should you NOT use async?

```python
# BAD: CPU-bound work blocks the event loop
@app.get("/compute")
async def heavy_computation():
    result = 0
    for i in range(10_000_000):  # Blocks event loop!
        result += i
    return {"result": result}

# GOOD: Offload CPU work to thread/process pool
import asyncio
from concurrent.futures import ProcessPoolExecutor

executor = ProcessPoolExecutor()

@app.get("/compute")
async def heavy_computation():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, compute_heavily)
    return {"result": result}

def compute_heavily():
    result = 0
    for i in range(10_000_000):
        result += i
    return result

# GOOD: Sync functions work fine for non-I/O operations
@app.get("/transform")
def transform_data(data: list[int]):  # Sync is fine here
    return [x * 2 for x in data]
```

### 13. What is the event loop and how does FastAPI manage it?

The event loop is Python's mechanism for running async code. FastAPI/uvicorn manages it:

```python
# Uvicorn creates and runs the event loop
# uvicorn main:app --host 0.0.0.0 --port 8000

# What uvicorn does internally:
# 1. Creates event loop
# 2. Loads your FastAPI app
# 3. Wraps it in ASGI protocol handler
# 4. Runs the event loop to serve requests

# You can access the event loop in your code:
import asyncio

@app.get("/check-loop")
async def check_loop():
    loop = asyncio.get_running_loop()
    return {"loop": str(loop), "is_running": loop.is_running()}

# Starlette's lifecycle events
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: before the event loop starts accepting requests
    await init_database()
    yield
    # Shutdown: after the event loop stops accepting requests
    await close_database()

app = FastAPI(lifespan=lifespan)
```

### 14. How do you handle database connections with async?

```python
# SQLAlchemy async
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

# Dependency
async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return user
```

---

## Section 4: Dependency Injection

### 15. Explain FastAPI's dependency injection system in depth

```python
from fastapi import FastAPI, Depends, Query
from typing import Annotated
from functools import lru_cache

app = FastAPI()

# ── Basic Dependencies ──────────────────────────────────────

# Simple function dependency
def common_params(skip: int = 0, limit: int = 20):
    return {"skip": skip, "limit": min(limit, 100)}

@app.get("/items")
def list_items(params: dict = Depends(common_params)):
    return {"skip": params["skip"], "limit": params["limit"]}

# ── Class Dependencies ──────────────────────────────────────

class QueryFilter:
    def __init__(self, field: str, operator: str = "eq", value: str = ""):
        self.field = field
        self.operator = operator
        self.value = value

    def apply(self, query):
        if self.operator == "eq":
            return query.filter_by(**{self.field: self.value})
        elif self.operator == "contains":
            return query.filter(query.model.__dict__[self.field].contains(self.value))
        return query

@app.get("/filtered")
def get_filtered(filters: Annotated[QueryFilter, Depends()]):
    return {"filter": f"{filters.field} {filters.operator} {filters.value}"}

# ── Generator Dependencies (with cleanup) ───────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Header(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(token=token).first()
    if not user:
        raise HTTPException(401)
    return user

# ── Cached Dependencies ─────────────────────────────────────

@lru_cache
def get_settings():
    return Settings()

@app.get("/config")
def get_config(settings: Settings = Depends(get_settings)):
    return {"db_url": settings.database_url}

# ── Overriding Dependencies (for testing) ───────────────────

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ── Use Cases ───────────────────────────────────────────────

# 1. Database sessions
# 2. Authentication/authorization
# 3. Pagination
# 4. Feature flags
# 5. Rate limiting
# 6. Logging/audit context
# 7. Caching layers
# 8. External service clients
```

---

## Section 5: Database Patterns

### 16. How do you structure a FastAPI project with SQLAlchemy?

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       └── items.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
├── alembic/
├── pyproject.toml
└── Dockerfile
```

```python
# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"

engine = create_async_engine(DATABASE_URL, pool_size=20, max_overflow=10)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# app/models/user.py
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    items: Mapped[list["Item"]] = relationship(back_populates="owner")

# app/services/user_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, email: str, name: str) -> User:
        user = User(email=email, name=name)
        self.db.add(user)
        await self.db.flush()
        return user

# app/api/v1/users.py
from fastapi import APIRouter, Depends
from app.database import get_db
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}")
async def get_user(user_id: int, db = Depends(get_db)):
    service = UserService(db)
    user = await service.get_by_id(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user
```

### 17. How do you handle N+1 query problems?

```python
from sqlalchemy.orm import selectinload, joinedload, contains_eager

# Problem: N+1 queries
@app.get("/users-with-items-bad")
async def get_users_bad(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()

    for user in users:
        # This fires a separate query for EACH user!
        items_result = await db.execute(select(Item).where(Item.owner_id == user.id))
        user.items = items_result.scalars().all()

    return users

# Solution 1: selectinload (recommended for collections)
@app.get("/users-with-items-good")
async def get_users_good(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(selectinload(User.items))
    )
    users = result.scalars().all()  # Items loaded in 1 extra query
    return users

# Solution 2: joinedload (for single relationships)
@app.get("/items-with-owner")
async def get_items_with_owner(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Item).options(joinedload(Item.owner))
    )
    return result.scalars().all()

# Solution 3: Subquery loading for complex scenarios
@app.get("/complex-query")
async def complex_query(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User)
        .options(selectinload(User.items).selectinload(Item.tags))
        .where(User.is_active == True)
    )
    return result.scalars().all()
```

---

## Section 6: Authentication and Security

### 18. How do you implement JWT authentication in FastAPI?

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

### 19. What security best practices should you follow?

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

# 1. CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=600,
)

# 2. Trusted Hosts
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com"])

# 3. HTTPS Only (in production)
# app.add_middleware(HTTPSRedirectMiddleware)

# 4. Rate Limiting (use slowapi or custom middleware)
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/limited")
@limiter.limit("100/minute")
async def limited_endpoint(request: Request):
    return {"status": "ok"}

# 5. Security Headers
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return response

# 6. Input sanitization
from pydantic import Field, field_validator
import bleach

class Comment(BaseModel):
    content: str = Field(max_length=5000)

    @field_validator('content')
    @classmethod
    def sanitize(cls, v):
        return bleach.clean(v)
```

---

## Section 7: Testing

### 20. How do you write tests for FastAPI?

```python
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
import pytest
from unittest.mock import patch, AsyncMock
from app.main import app
from app.database import get_db

# ── Synchronous Tests ───────────────────────────────────────

client = TestClient(app)

def test_create_user():
    response = client.post("/users", json={"name": "Alice", "email": "alice@test.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"

def test_get_nonexistent_user():
    response = client.get("/users/999")
    assert response.status_code == 404

# ── Async Tests ─────────────────────────────────────────────

@pytest.mark.anyio
async def test_async_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/items")
    assert response.status_code == 200

# ── Database Tests with Fixtures ────────────────────────────

@pytest.fixture
def test_db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = async_sessionmaker(engine, class_=AsyncSession)()
    yield session
    session.close()

@pytest.fixture
def override_get_db(test_db_session):
    async def _override():
        yield test_db_session
    return _override

def test_user_database(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    response = client.post("/users", json={"name": "Test", "email": "test@test.com"})
    assert response.status_code == 201
    app.dependency_overrides.clear()

# ── Mock External Services ──────────────────────────────────

@patch("app.services.email.send_email")
def test_send_notification(mock_send_email):
    mock_send_email.return_value = AsyncMock(return_value=True)
    response = client.post("/notifications", json={"user_id": 1, "message": "Hello"})
    assert response.status_code == 200
    mock_send_email.assert_called_once()

# ── Pydantic Model Tests ────────────────────────────────────

def test_user_validation():
    with pytest.raises(ValidationError):
        UserCreate(name="", email="invalid")

    user = UserCreate(name="Alice", email="alice@test.com")
    assert user.name == "Alice"
```

### 21. How do you test dependencies and middleware?

```python
from fastapi import FastAPI, Depends, Request
from fastapi.testclient import TestClient

app = FastAPI()

# Dependency to test
def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if api_key != "valid-key":
        from fastapi import HTTPException
        raise HTTPException(403, "Invalid API key")
    return api_key

@app.get("/protected")
def protected_route(api_key: str = Depends(verify_api_key)):
    return {"status": "authenticated"}

# Test the dependency directly
def test_verify_api_key_valid():
    from starlette.testclient import TestClient
    from starlette.requests import Request

    scope = {"type": "http", "headers": [(b"x-api-key", b"valid-key")]}
    request = Request(scope)
    result = verify_api_key(request)
    assert result == "valid-key"

def test_verify_api_key_invalid():
    from starlette.requests import Request
    from fastapi import HTTPException

    scope = {"type": "http", "headers": []}
    request = Request(scope)
    with pytest.raises(HTTPException) as exc:
        verify_api_key(request)
    assert exc.value.status_code == 403

# Test middleware
def test_security_headers():
    response = client.get("/any-endpoint")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
```

---

## Section 8: Performance Optimization

### 22. How do you optimize FastAPI performance?

```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
import asyncio
import functools

app = FastAPI()

# 1. Enable GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 2. Use response caching
from fastapi import Request
from starlette.responses import JSONResponse

cache_store: dict[str, tuple[float, any]] = {}

def cache_response(ttl: int = 60):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{str(kwargs)}"
            if cache_key in cache_store:
                ts, data = cache_store[cache_key]
                if time.time() - ts < ttl:
                    return data

            result = await func(*args, **kwargs)
            cache_store[cache_key] = (time.time(), result)
            return result
        return wrapper
    return decorator

@app.get("/expensive-data")
@cache_response(ttl=30)
async def expensive_data():
    await asyncio.sleep(1)  # Simulate slow query
    return {"data": "expensive"}

# 3. Database query optimization
@app.get("/optimized-query")
async def optimized_query(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User)
        .options(selectinload(User.items))  # Eager loading
        .where(User.is_active == True)
        .limit(100)  # Always limit
    )
    return result.scalars().all()

# 4. Use connection pooling
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# 5. Background tasks for non-critical work
@app.post("/events")
async def process_event(event: Event, background_tasks: BackgroundTasks):
    background_tasks.add_task(store_event, event)  # Don't block response
    return {"status": "received"}

# 6. Use async I/O everywhere possible
async def fetch_all_users():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_user(session, uid) for uid in user_ids]
        return await asyncio.gather(*tasks)
```

---

## Section 9: Error Handling

### 23. How do you implement custom error handling?

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# Custom exception classes
class AppException(Exception):
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code

class NotFoundException(AppException):
    def __init__(self, resource: str, identifier: str):
        super().__init__(404, f"{resource} with id '{identifier}' not found", "NOT_FOUND")

class ValidationException(AppException):
    def __init__(self, detail: str):
        super().__init__(422, detail, "VALIDATION_ERROR")

class RateLimitException(AppException):
    def __init__(self):
        super().__init__(429, "Rate limit exceeded", "RATE_LIMITED")

# Global exception handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.detail,
                "path": request.url.path,
            }
        },
    )

# Validation error handler
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({"field": field, "message": error["msg"]})
    return JSONResponse(status_code=422, content={"errors": errors})

# Usage
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = db.get(item_id)
    if not item:
        raise NotFoundException("Item", str(item_id))
    return item
```

---

## Section 10: Deployment

### 24. How do you deploy FastAPI applications?

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run with uvicorn in production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# Or use gunicorn with uvicorn workers
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@db/app
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    deploy:
      replicas: 3

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass

  redis:
    image: redis:7-alpine

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### 25. How do you handle environment-specific configuration?

```python
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "My API"
    DEBUG: bool = False
    VERSION: str = "1.0.0"

    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # External Services
    STRIPE_API_KEY: Optional[str] = None
    SENDGRID_API_KEY: Optional[str] = None

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Usage in dependencies
def get_config():
    return get_settings()

@app.get("/config")
def config(settings: Settings = Depends(get_config)):
    return {"app": settings.APP_NAME, "version": settings.VERSION}
```

---

## Section 11: Design Patterns

### 26. What design patterns are commonly used with FastAPI?

```python
# ── Repository Pattern ──────────────────────────────────────

from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    async def create(self, user: UserCreate) -> User: ...

class SQLUserRepository(UserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, user: UserCreate) -> User:
        db_user = User(**user.model_dump())
        self.db.add(db_user)
        await self.db.flush()
        return db_user

def get_user_repo(db: AsyncSession = Depends(get_db)):
    return SQLUserRepository(db)

@app.get("/users/{user_id}")
async def get_user(user_id: int, repo: UserRepository = Depends(get_user_repo)):
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(404)
    return user

# ── Service Layer Pattern ───────────────────────────────────

class UserService:
    def __init__(self, repo: UserRepository, mailer: EmailService):
        self.repo = repo
        self.mailer = mailer

    async def register_user(self, data: UserCreate) -> User:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise ValidationException("Email already registered")

        user = await self.repo.create(data)
        await self.mailer.send_welcome(user.email)
        return user

# ── Factory Pattern ─────────────────────────────────────────

class PaymentProcessorFactory:
    _processors = {
        "stripe": StripeProcessor,
        "paypal": PayPalProcessor,
        "bank_transfer": BankTransferProcessor,
    }

    @classmethod
    def get_processor(cls, method: str) -> PaymentProcessor:
        processor_cls = cls._processors.get(method)
        if not processor_cls:
            raise ValueError(f"Unknown payment method: {method}")
        return processor_cls()
```

---

## Section 12: Advanced Topics

### 27. How do you handle WebSockets in FastAPI?

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dataclasses import dataclass, field

app = FastAPI()

@dataclass
class ConnectionManager:
    rooms: dict[str, list[WebSocket]] = field(default_factory=dict)

    async def connect(self, ws: WebSocket, room: str):
        await ws.accept()
        self.rooms.setdefault(room, []).append(ws)

    def disconnect(self, ws: WebSocket, room: str):
        if room in self.rooms:
            self.rooms[room].remove(ws)
            if not self.rooms[room]:
                del self.rooms[room]

    async def broadcast(self, room: str, message: str):
        for ws in self.rooms.get(room, []):
            await ws.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str):
    await manager.connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(room, f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
```

### 28. How do you implement background tasks?

```python
from fastapi import BackgroundTasks
import asyncio

# Method 1: BackgroundTasks (simple)
@app.post("/process")
async def process(data: Data, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_data, data.id)
    return {"status": "queued"}

def process_data(data_id: int):
    # Runs after response is sent
    time.sleep(10)  # Simulate work

# Method 2: Celery (production)
from celery import Celery

celery_app = Celery("tasks", broker="redis://localhost:6379")

@celery_app.task(bind=True, max_retries=3)
def send_email_task(self, email: str, subject: str, body: str):
    try:
        send_email(email, subject, body)
    except Exception as exc:
        self.retry(exc=exc, countdown=60)

@app.post("/send-email")
async def send_email_endpoint(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_task.delay, email, "Subject", "Body")
    return {"status": "queued"}

# Method 3: APScheduler (scheduled tasks)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job("interval", hours=1)
async def cleanup_old_sessions():
    await db.execute(delete(Session).where(Session.expires_at < datetime.utcnow()))

scheduler.start()
```

### 29. How do you implement API versioning?

```python
from fastapi import FastAPI, APIRouter

app = FastAPI()

# Method 1: URL path versioning (recommended)
v1_router = APIRouter(prefix="/api/v1", tags=["v1"])
v2_router = APIRouter(prefix="/api/v2", tags=["v2"])

@v1_router.get("/users/{user_id}")
def get_user_v1(user_id: int):
    user = get_user(user_id)
    return {"id": user.id, "name": user.name}  # v1 response

@v2_router.get("/users/{user_id}")
def get_user_v2(user_id: int):
    user = get_user(user_id)
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,  # v2 adds email
        "preferences": user.preferences,  # v2 adds preferences
    }

app.include_router(v1_router)
app.include_router(v2_router)

# Method 2: Header versioning
from fastapi import Header

@app.get("/users/{user_id}")
def get_user(user_id: int, accept_version: str = Header("1.0")):
    user = get_user(user_id)
    if accept_version == "2.0":
        return {"id": user.id, "name": user.name, "email": user.email}
    return {"id": user.id, "name": user.name}
```

### 30. How do you monitor FastAPI in production?

```python
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanExporter
import logging

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

# OpenTelemetry tracing
provider = TracerProvider()
processor = BatchSpanExporter(JaegerExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

@app.get("/traced")
async def traced_endpoint():
    with tracer.start_as_current_span("fetch_data") as span:
        span.set_attribute("user.id", 123)
        data = await fetch_data()
        span.add_event("data_fetched", {"count": len(data)})
        return data

# Structured logging
import structlog

logger = structlog.get_logger()

@app.get("/logged")
async def logged_endpoint():
    logger.info("request_started", path="/logged", method="GET")
    result = await process()
    logger.info("request_completed", result_length=len(result))
    return result
```

---

## Quick Reference: Top 10 Must-Know Answers

1. **FastAPI is fast** because of async/await, Pydantic's Rust core, and Starlette's efficient routing
2. **Pydantic validates** at the C level, providing both validation and serialization
3. **async/await** enables non-blocking I/O; use `run_in_executor` for CPU-bound work
4. **Dependency injection** chains resources like DB sessions, auth, and config
5. **Use async SQLAlchemy** with `selectinload` to avoid N+1 queries
6. **JWT auth** with `python-jose` and `passlib` is the standard approach
7. **Test with** `TestClient` (sync) or `httpx.AsyncClient` (async)
8. **Deploy with** Docker + uvicorn workers; use environment variables for config
9. **Handle errors** with custom exception classes and global handlers
10. **Monitor with** Prometheus metrics, OpenTelemetry tracing, and structured logging
