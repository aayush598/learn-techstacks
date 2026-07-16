# FastAPI Fundamentals - Interview Questions

## Table of Contents

1. [General FastAPI Questions](#general-fastapi-questions)
2. [Setup and Installation](#setup-and-installation)
3. [Path Parameters](#path-parameters)
4. [Query Parameters](#query-parameters)
5. [Request Body](#request-body)
6. [Response Models](#response-models)
7. [Status Codes](#status-codes)
8. [Error Handling](#error-handling)
9. [APIRouter](#apirouter)
10. [Performance and Architecture](#performance-and-architecture)

---

## General FastAPI Questions

### Q1: What is FastAPI and why is it fast?

**Answer:** FastAPI is a modern Python web framework for building APIs. It's fast for two reasons:

1. **Developer fast**: Automatic validation, serialization, and documentation from type hints eliminates boilerplate
2. **Runtime fast**: Built on Starlette (async ASGI) and Pydantic v2 (Rust-based validation), running on Uvicorn (libuv event loop)

Performance benchmarks show ~85,000 req/s for JSON serialization, comparable to Go and Node.js frameworks, and 2-5x faster than Flask and Django.

```python
# This 5-line file gives you:
# - Automatic request validation
# - Automatic JSON serialization
# - Interactive docs at /docs
# - Full async support
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"Hello": "World"}
```

---

### Q2: What is the relationship between FastAPI, Starlette, and Pydantic?

**Answer:** They form a layered architecture:

```
FastAPI (High-level framework)
  ├── Validation & serialization (Pydantic)
  ├── Routing & middleware (Starlette)
  └── ASGI server (Uvicorn)
```

- **Starlette** provides ASGI primitives: routing, middleware, request/response objects, WebSocket support
- **Pydantic** provides data validation using Python type hints, serialization/deserialization
- **FastAPI** combines them with dependency injection, automatic docs, and developer-friendly APIs

---

### Q3: What Python version does FastAPI require? What are the benefits of newer versions?

**Answer:**

| Version | Feature |
|---------|---------|
| 3.7+ | FastAPI minimum |
| 3.8+ | `from __future__ import annotations` for forward references |
| 3.9+ | Built-in generics: `list[str]` instead of `List[str]` |
| 3.10+ | Union syntax: `str \| None` instead of `Optional[str]` |
| 3.10+ | `Annotated` type syntax for cleaner parameter definitions |
| 3.12+ | Improved error messages, faster performance |

Python 3.10+ is strongly recommended for `Annotated` syntax and modern type hints.

---

### Q4: What is the difference between `async def` and `def` in FastAPI path operations?

**Answer:**

```python
# Async path operation - runs on the event loop
@app.get("/async/")
async def async_endpoint():
    result = await some_async_operation()  # Non-blocking
    return result

# Sync path operation - runs in a threadpool
@app.get("/sync/")
def sync_endpoint():
    result = some_sync_operation()  # Can block the thread
    return result
```

- `async def`: Use when you have `await` calls (async DB queries, HTTP requests). More efficient for I/O-bound work
- `def` (sync): Use for CPU-bound operations or synchronous libraries. FastAPI runs it in a threadpool automatically
- For simple endpoints with no I/O, both perform similarly

---

### Q5: How does automatic documentation work in FastAPI?

**Answer:** FastAPI introspects your code to build an OpenAPI schema:

1. Reads all `@app.get()`, `@app.post()`, etc. decorators
2. Extracts path parameters, query parameters, request bodies from function signatures
3. Uses Pydantic models to generate JSON schemas for request/response bodies
4. Generates the OpenAPI 3.1 specification at `/openapi.json`
5. Swagger UI (`/docs`) and ReDoc (`/redoc`) render this schema as interactive docs

```python
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get an item by ID."""
    ...
# FastAPI auto-generates:
# - Path parameter: item_id (integer, required)
# - Response: Item schema with all fields
# - Description from docstring
```

---

### Q6: Is FastAPI production-ready?

**Answer:** Yes. Used in production by Microsoft (Azure), Uber, Netflix, Airbnb, and many others. It has 80,000+ GitHub stars, 150M+ monthly PyPI downloads, active maintenance, and comprehensive security features. It's fully production-ready for APIs of any scale.

---

### Q7: When should you NOT use FastAPI?

**Answer:**

1. **Full-stack apps with templates**: Django is better for server-rendered apps with admin panels
2. **Teams without Python experience**: Node.js/Go may be better if the team is proficient there
3. **Simple CRUD without validation**: Flask may be simpler for trivial APIs
4. **Legacy Python support**: FastAPI requires Python 3.7+
5. **Projects needing built-in ORM**: Django's ORM is more mature (though SQLModel is catching up)
6. **Real-time chat apps**: Socket.io (Node.js) or Django Channels may be better

---

## Setup and Installation

### Q8: What is the recommended way to install FastAPI for a new project?

**Answer:**

```bash
# Using uv (fastest - recommended)
uv init my-project && cd my-project
uv add fastapi uvicorn[standard]

# Using poetry
poetry new my-project && cd my-project
poetry add fastapi
poetry add --group dev uvicorn[standard]
```

Always use a virtual environment. Never install packages system-wide.

---

### Q9: What is the difference between `pip install fastapi` and `pip install fastapi[all]`?

**Answer:**

- `pip install fastapi`: Core dependencies only (starlette, pydantic, typing-extensions)
- `pip install fastapi[all]`: Includes optional extras (uvicorn, python-multipart, jinja2, python-dotenv)

For production, install only what you need to minimize attack surface and image size.

---

### Q10: What does `uvicorn main:app` mean? What are the important flags?

**Answer:** `main` is the Python module (main.py), `app` is the variable name of the FastAPI instance. The colon syntax is Python's module:attribute notation.

Important flags:
- `--reload`: Auto-restart on file changes (development only)
- `--host 0.0.0.0`: Bind to all interfaces
- `--port 8000`: Specify port
- `--workers 4`: Number of worker processes (production)
- `--log-level info`: Logging verbosity

---

### Q11: How many uvicorn workers should you run in production?

**Answer:** The general rule is `(2 × CPU cores) + 1`. For async apps with high I/O, you can use more workers. For CPU-bound work, stick to the formula. Monitor resource usage and adjust. Example: 4-core server → 9 workers.

In production, prefer `gunicorn -w 4 -k uvicorn.workers.UvicornWorker` for better process management.

---

## Path Parameters

### Q12: How does FastAPI handle path parameters vs query parameters?

**Answer:** FastAPI determines parameter type based on where the parameter name appears:

```python
@app.get("/items/{item_id}")  # item_id is in the path template → PATH param
async def get_item(item_id: int, q: str = None):  # q is NOT in path → QUERY param
    pass
```

- **Path parameters**: Defined in `{}` in the URL path. Always required. Converted to the declared type.
- **Query parameters**: Function parameters not in the path template. Can be optional with defaults.

---

### Q13: What happens if you have two routes with overlapping paths?

**Answer:** FastAPI matches routes in definition order. Static routes should be defined before parameterized routes:

```python
# ✅ CORRECT ORDER
@app.get("/users/me")        # Matches first
async def current_user(): ...

@app.get("/users/{user_id}")  # Matches second
async def get_user(user_id: str): ...

# ❌ WRONG ORDER - /users/me will never be reached
@app.get("/users/{user_id}")  # Matches /users/me first!
async def get_user(user_id: str): ...

@app.get("/users/me")
async def current_user(): ...  # Unreachable
```

---

### Q14: Can path parameters have validation constraints?

**Answer:** Yes, using `Path()`:

```python
from fastapi import Path

@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(..., gt=0, le=1000)
):
    return {"item_id": item_id}
```

Available constraints: `gt`, `ge`, `lt`, `le`, `min_length`, `max_length`, `pattern` (regex), `multiple_of`.

---

### Q15: How do UUID path parameters work?

**Answer:** Declare the type as `UUID`. FastAPI validates the format and converts automatically:

```python
from uuid import UUID

@app.get("/users/{user_id}")
async def get_user(user_id: UUID):
    return {"user_id": str(user_id)}
# GET /users/550e8400-e29b-41d4-a716-446655440000 → 200 OK
# GET /users/not-a-uuid → 422 Validation Error
```

---

## Query Parameters

### Q16: What happens when you send extra query parameters?

**Answer:** By default, FastAPI **rejects** extra query parameters with a 422 error. This is intentional for type safety. To allow extra parameters:

```python
from pydantic import BaseModel, ConfigDict

class Params(BaseModel):
    model_config = ConfigDict(extra="allow")
    q: str

@app.get("/search/")
async def search(params: Params = Depends()):
    return params.model_dump()
# /search/?q=test&extra=hello → {"q": "test", "extra": "hello"}
```

---

### Q17: How do you make query parameters optional?

**Answer:**

```python
# Using None default
@app.get("/items/")
async def list_items(q: str | None = None):
    return {"q": q}

# Using Query with None
@app.get("/items/")
async def list_items(q: str | None = Query(None)):
    return {"q": q}
```

When not provided, `q` is `None`. When provided empty (`?q=`), `q` is `""`.

---

### Q18: Can query parameters be lists?

**Answer:** Yes, repeat the parameter in the URL:

```python
@app.get("/items/")
async def list_items(tags: list[str] = Query(default=[])):
    return {"tags": tags}
# /items/?tags=python&tags=fastapi&tags=async
# → {"tags": ["python", "fastapi", "async"]}
```

---

### Q19: How do you validate query parameters?

**Answer:** Use `Query()` with constraints:

```python
@app.get("/search/")
async def search(
    q: str = Query(..., min_length=3, max_length=50, pattern=r"^[a-z]+$"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    return {"q": q, "page": page, "per_page": per_page}
```

---

## Request Body

### Q20: How do you handle JSON request bodies in FastAPI?

**Answer:** Declare a Pydantic model as a function parameter:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users/")
async def create_user(user: User):
    # user is already validated and parsed
    return {"name": user.name, "email": user.email}
```

FastAPI automatically parses JSON, validates against the model, and returns 422 for invalid data.

---

### Q21: Can you combine path parameters, query parameters, and request body in one endpoint?

**Answer:** Yes, FastAPI distinguishes them:

```python
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,           # Path parameter (in URL template)
    q: str | None = None,   # Query parameter (has default, not in path)
    item: Item = ...,       # Request body (Pydantic model)
):
    return {"item_id": item_id, "q": q, "item": item}
```

---

### Q22: What is the difference between Form data and JSON body?

**Answer:**

| Feature | JSON Body | Form Data |
|---------|-----------|-----------|
| Content-Type | `application/json` | `application/x-www-form-urlencoded` or `multipart/form-data` |
| Nesting | Supports nested objects | Flat key-value pairs |
| File upload | No | Yes (multipart) |
| Use case | REST APIs | HTML forms, file uploads |
| Validation | Pydantic models | `Form()` parameters |

```python
# JSON body
@app.post("/api/users/")
async def create_user(user: UserCreate):  # Pydantic model
    return user

# Form data
@app.post("/login/")
async def login(
    username: str = Form(...),
    password: str = Form(...),
):
    return {"token": "..."}
```

---

### Q23: How do you handle file uploads?

**Answer:** Use `UploadFile`:

```python
from fastapi import File, UploadFile

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

# Multiple files
@app.post("/upload-multiple/")
async def upload_multiple(files: list[UploadFile] = File(...)):
    return [{"filename": f.filename} for f in files]

# File + metadata
@app.post("/documents/")
async def upload_document(
    title: str = Form(...),
    file: UploadFile = File(...),
):
    return {"title": title, "filename": file.filename}
```

---

### Q24: What does `Body(embed=True)` do?

**Answer:** Without embed, the request body is the model directly. With embed, it's nested in a key:

```python
@app.post("/items/")
async def create_item(item: Item = Body(..., embed=True)):
    return item

# Without embed: {"name": "Laptop", "price": 999}
# With embed: {"item": {"name": "Laptop", "price": 999}}
```

---

## Response Models

### Q25: What is the difference between `response_model` and `response_model_exclude_unset`?

**Answer:**

- `response_model`: Validates and serializes the entire response against the model schema
- `response_model_exclude_unset=True`: Only includes fields that were explicitly set (not defaults)

```python
class User(BaseModel):
    id: int
    name: str
    is_active: bool = True  # Default value

@app.put("/users/{id}", response_model=User, response_model_exclude_unset=True)
async def update_user(id: int, updates: UserUpdate):
    # If client sends {"name": "New"}, response is {"id": 1, "name": "New"}
    # is_active is NOT included (wasn't explicitly set)
```

---

### Q26: How does `response_model_include` and `response_model_exclude` work?

**Answer:** They filter which fields appear in the response:

```python
@app.get("/users/{id}", response_model=User, response_model_include={"id", "name"})
async def get_user(id: int):
    return User(id=1, name="John", email="john@example.com")
# Response: {"id": 1, "name": "John"} (email filtered out)

@app.get("/public/{id}", response_model=User, response_model_exclude={"email"})
async def get_public_user(id: int):
    return User(id=1, name="John", email="john@example.com")
# Response: {"id": 1, "name": "John"} (email excluded)
```

---

### Q27: What is the difference between `response_model` and return type annotation (`->`)?

**Answer:** For basic cases, they're equivalent:

```python
# These produce the same OpenAPI schema:
@app.get("/users/", response_model=list[User])
async def list_users(): ...

@app.get("/users/")
async def list_users() -> list[User]: ...
```

`response_model` supports extra options: `exclude_unset`, `include`, `exclude`. Return type annotation is cleaner when you don't need those.

---

### Q28: What response classes does FastAPI provide?

**Answer:**

| Class | Use Case |
|-------|----------|
| `JSONResponse` | Default. JSON responses with custom status/headers |
| `HTMLResponse` | HTML pages |
| `PlainTextResponse` | Plain text responses |
| `RedirectResponse` | HTTP redirects |
| `StreamingResponse` | Streaming data (SSE, large files) |
| `FileResponse` | File downloads |
| `ORJSONResponse` | Faster JSON (Rust-based) |

---

## Status Codes

### Q29: What status code should you use for resource creation?

**Answer:** `201 Created`:

```python
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return create_user(user)
```

---

### Q30: When should you use 204 No Content?

**Answer:** For successful operations that don't return a body, typically DELETE:

```python
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    delete_user_from_db(user_id)
    return None
```

---

### Q31: What's the difference between 401 and 403?

**Answer:**

- **401 Unauthorized**: User is NOT authenticated. Needs to provide credentials. Should include `WWW-Authenticate` header.
- **403 Forbidden**: User IS authenticated but lacks permission for the resource.

```python
# 401: No token or invalid token
@app.get("/profile/")
async def profile(token: str = Header(...)):
    if not verify_token(token):
        raise HTTPException(401, "Invalid token", headers={"WWW-Authenticate": "Bearer"})

# 403: Valid token but not allowed
@app.delete("/users/{id}")
async def delete_user(id: int, user = Depends(get_current_user)):
    if user.id != id and not user.is_admin:
        raise HTTPException(403, "Not enough permissions")
```

---

### Q32: Why does FastAPI use 422 for validation errors instead of 400?

**Answer:** FastAPI follows the OpenAPI specification. 400 (Bad Request) means the request is malformed and can't be parsed. 422 (Unprocessable Entity) means the request was parsed but the data failed validation. FastAPI can parse the request but the data doesn't match the schema.

---

## Error Handling

### Q33: How do you create custom exception handlers in FastAPI?

**Answer:**

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class MyAppError(Exception):
    def __init__(self, name: str):
        self.name = name

app = FastAPI()

@app.exception_handler(MyAppError)
async def my_error_handler(request: Request, exc: MyAppError):
    return JSONResponse(
        status_code=400,
        content={"detail": f"Error: {exc.name}"},
    )

@app.get("/error/")
async def trigger_error():
    raise MyAppError("something went wrong")
```

You can override built-in handlers the same way.

---

### Q34: What is the difference between RequestValidationError and ValidationError?

**Answer:**

| Feature | RequestValidationError | ValidationError |
|---------|----------------------|-----------------|
| Source | FastAPI request parsing | Pydantic manual validation |
| When raised | Invalid request data | Invalid data in your code |
| HTTP status | 422 (automatic) | You handle manually |
| Handler | `@app.exception_handler(RequestValidationError)` | Try/except in your code |

---

### Q35: How do you implement a consistent error response format?

**Answer:** Create a custom exception hierarchy and centralized handler:

```python
class AppException(HTTPException):
    def __init__(self, status_code, detail, error_code):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code

@app.exception_handler(AppException)
async def app_error_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.error_code, "message": exc.detail}},
    )
```

---

### Q36: How do you log exceptions in production?

**Answer:** Use Python's `logging` module with structured logging:

```python
import logging
logger = logging.getLogger("api")

@app.exception_handler(Exception)
async def handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc}")  # Includes traceback
    return JSONResponse(status_code=500, content={"detail": "Internal error"})
```

Never log sensitive data (passwords, tokens). Log at appropriate levels (warning for 4xx, exception for 5xx).

---

## APIRouter

### Q37: What is APIRouter and why is it important?

**Answer:** `APIRouter` lets you split your application into modular route files. It has the same interface as `FastAPI` and supports all decorators. Use it to organize routes by feature, apply shared dependencies, and keep code maintainable.

```python
# app/routers/users.py
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def list_users():
    return []

# app/main.py
app.include_router(users.router, prefix="/api/v1")
```

---

### Q38: How do you share dependencies across all routes in a router?

**Answer:**

```python
router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(verify_admin), Depends(get_db)],
)

@router.get("/stats/")
async def stats():  # verify_admin and get_db run automatically
    return {}

# Combine with endpoint-level dependencies
@router.get("/users/")
async def users(admin: User = Depends(get_current_admin)):
    # verify_admin, get_db, AND get_current_admin all run
    return []
```

---

### Q39: How do you organize routes in a large FastAPI application?

**Answer:**

```
app/
├── main.py
├── routers/
│   ├── users.py
│   ├── items.py
│   └── auth.py
├── schemas/
│   ├── user.py
│   └── item.py
├── services/
│   ├── user_service.py
│   └── item_service.py
├── models/
│   └── database.py
└── dependencies.py
```

Key principles:
1. One router per domain feature
2. Separate schemas from routers
3. Business logic in services, not routers
4. Consistent prefix conventions
5. Document everything with summary/description

---

## Performance and Architecture

### Q40: Why is FastAPI faster than Flask?

**Answer:** Three main reasons:

1. **Async I/O**: Native `async`/`await` support allows handling thousands of concurrent connections without blocking
2. **Starlette**: The underlying ASGI framework is highly optimized
3. **Pydantic v2**: Validation is implemented in Rust, not pure Python

Flask is synchronous by default and uses WSGI, which limits concurrent request handling. FastAPI with Uvicorn uses an async event loop, handling I/O-bound operations much more efficiently.

---

### Q41: Can FastAPI handle WebSockets?

**Answer:** Yes, built-in:

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")
```

---

### Q42: How does FastAPI's dependency injection system work?

**Answer:** Dependencies are functions (or classes) that FastAPI calls before your path operation:

```python
from fastapi import Depends

async def get_current_user(token: str = Header(...)):
    return decode_token(token)

@app.get("/profile/")
async def profile(user: User = Depends(get_current_user)):
    return user  # user is already validated
```

Dependencies can be nested, cached, and overridden for testing. They support both sync and async, and can yield resources (like database connections).

---

### Q43: What is the ASGI vs WSGI difference?

**Answer:**

- **WSGI** (Python standard): Synchronous, one thread per request. Used by Flask, Django.
- **ASGI** (async standard): Asynchronous, handles thousands of connections on one thread. Used by FastAPI, Starlette.

ASGI enables WebSocket support, HTTP/2, and async request handling. WSGI apps can run on ASGI servers with adapters, but don't get async benefits.

---

### Q44: How do you test FastAPI applications?

**Answer:** Use `TestClient` (from Starlette) or `httpx.AsyncClient`:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"name": "John", "email": "john@test.com"})
    assert response.status_code == 201
    assert response.json()["name"] == "John"

# Async testing
import httpx
import pytest

@pytest.mark.asyncio
async def test_create_user_async():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users/", json={"name": "John"})
        assert response.status_code == 201
```

---

### Q45: How do you handle CORS in FastAPI?

**Answer:** Use the built-in `CORSMiddleware`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Q46: What is the lifespan pattern in FastAPI?

**Answer:** Used for startup/shutdown events (replacing deprecated `@app.on_event`):

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db = await create_db_pool()
    app.state.db = db
    yield
    # Shutdown
    await db.close()

app = FastAPI(lifespan=lifespan)
```

---

### Q47: How do you structure a production FastAPI application?

**Answer:**

```
project/
├── app/
│   ├── main.py           # App factory, middleware, lifespan
│   ├── config.py          # Settings (pydantic-settings)
│   ├── dependencies.py    # Shared dependencies
│   ├── routers/           # API routes
│   ├── schemas/           # Pydantic models
│   ├── services/          # Business logic
│   ├── repositories/      # Data access
│   └── models/            # Database models (SQLAlchemy/SQLModel)
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── alembic/               # DB migrations
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── .env
```

Key patterns:
- Application factory pattern
- Dependency injection for services and repositories
- Separate input/output schemas
- Centralized error handling
- Structured logging
- Health check endpoints
- Graceful shutdown with lifespan
