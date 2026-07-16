# 01 - What is FastAPI?

## Table of Contents

1. [What is FastAPI?](#what-is-fastapi)
2. [History and Creator](#history-and-creator)
3. [Built on Starlette + Pydantic](#built-on-starlette--pydantic)
4. [Core Features](#core-features)
5. [Performance Benchmarks](#performance-benchmarks)
6. [Type Safety in FastAPI](#type-safety-in-fastapi)
7. [Why FastAPI Over Alternatives](#why-fastapi-over-alternatives)
8. [The FastAPI Ecosystem](#the-fastapi-ecosystem)
9. [Industry Adoption](#industry-adoption)
10. [When NOT to Use FastAPI](#when-not-to-use-fastapi)
11. [Interview Questions](#interview-questions)

---

## What is FastAPI?

FastAPI is a modern, high-performance Python web framework for building APIs. It was specifically designed to be fast, easy to use, and easy to learn. FastAPI sits in the category of "type-driven" web frameworks, where Python type hints are not just annotations but functional parts of the framework's core machinery.

Unlike traditional frameworks where you write repetitive boilerplate code, FastAPI leverages Python 3.6+ type hints to automatically:

- Validate incoming request data
- Serialize response data
- Generate interactive API documentation
- Provide type-checked autocompletion in your editor

**In one sentence:** FastAPI is a Python framework that turns type hints into a fully validated, documented, and高性能的 API with minimal code.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}
```

That 5-line file is a complete, production-ready API with automatic documentation, async support, and full type validation.

---

## History and Creator

### Sebastián Ramírez (Tiangolo)

FastAPI was created by **Sebastián Ramírez**, known online as **Tiangolo**. He is a Colombian software engineer who previously worked at Uber and other companies. He created FastAPI in 2018 while working on a project at Uber where he needed a better way to build APIs.

The name "FastAPI" comes from two properties:
- **Fast**: It is very high performance, on par with Node.js and Go
- **Fast** (second meaning): It is fast to develop with, about 200% to 300% faster

### Timeline

| Year | Event |
|------|-------|
| 2018 | Sebastián Ramírez starts developing FastAPI |
| 2018-11 | First release on PyPI (v0.1.0) |
| 2019 | Gains significant traction in the Python community |
| 2020 | Reaches 10,000 GitHub stars |
| 2021 | Reaches 40,000+ GitHub stars |
| 2022 | Reaches 50,000+ GitHub stars |
| 2023 | Reaches 60,000+ GitHub stars |
| 2024 | Becomes the most popular Python API framework on GitHub |
| 2025 | 80,000+ GitHub stars, widely adopted in production |

### Key Related Projects by Tiangolo

Sebastián also created or maintains several related projects:

- **SQLModel**: ORM that combines SQLAlchemy and Pydantic
- **Typer**: CLI framework built on Click
- **Strawberry**: GraphQL library that integrates with FastAPI
- **LangServe**: Deployment of LangChain chains as FastAPI endpoints
- **FastAPI CLI**: Official CLI tool for FastAPI projects

---

## Built on Starlette + Pydantic

FastAPI is not built from scratch. It stands on the shoulders of two powerful libraries:

### Starlette (The Foundation)

Starlette is a lightweight ASGI (Asynchronous Server Gateway Interface) framework/toolkit. It provides:

- **Routing**: URL path matching and parameter extraction
- **Middleware**: Request/response processing pipeline
- **WebSocket support**: Full async WebSocket handling
- **Request/Response objects**: Low-level HTTP abstractions
- **Static file serving**: Serving files from disk
- **Template rendering**: Jinja2 integration
- **Test client**: For testing without running a server

```
┌─────────────────────────────────────────┐
│               FastAPI                    │
│  (Validation, Documentation, DI, etc.)  │
├─────────────────────────────────────────┤
│             Starlette                   │
│  (Routing, Middleware, Request/Response) │
├─────────────────────────────────────────┤
│                ASGI                     │
│  (Uvicorn, Daphne, Hypercorn)          │
└─────────────────────────────────────────┘
```

### Pydantic (The Validator)

Pydantic is a data validation library that uses Python type hints for validation. FastAPI uses it for:

- **Request body validation**: Automatically parse and validate JSON request bodies
- **Query parameter validation**: Validate query string parameters
- **Path parameter validation**: Validate path parameters
- **Response serialization**: Convert Python objects to JSON responses
- **Settings management**: Environment variable validation (via pydantic-settings)

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., gt=0, lt=150)
    email: str
    is_active: bool = True
```

### How They Work Together

```
HTTP Request → Uvicorn (ASGI Server)
    → Starlette (Routing, Middleware)
        → FastAPI (Type Validation, DI, Serialization)
            → Your Code (Business Logic)
                → FastAPI (Response Serialization)
                    → Starlette (Response Formatting)
                        → Uvicorn (HTTP Response)
```

---

## Core Features

### 1. Automatic API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI** at `/docs` - The industry standard for API documentation
- **ReDoc** at `/redoc` - An alternative documentation interface
- **OpenAPI schema** at `/openapi.json` - The machine-readable API specification

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="A sample API with documentation",
    version="1.0.0",
)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get a user by ID.
    
    This endpoint returns a user object for the given ID.
    """
    return {"user_id": user_id}
```

### 2. Automatic Request Validation

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

@app.post("/items/")
async def create_item(item: Item):
    # item is already validated and parsed
    # If invalid data is sent, FastAPI returns 422 with detailed error
    return {"item_name": item.name, "price": item.price}
```

### 3. Native Async/Await Support

```python
import httpx
from fastapi import FastAPI

app = FastAPI()

@app.get("/external-data/")
async def get_external_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

### 4. Dependency Injection System

```python
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

async def verify_token(token: str = Header(...)):
    if token != "secret":
        raise HTTPException(status_code=403, detail="Invalid token")
    return token

@app.get("/protected/")
async def protected_route(token: str = Depends(verify_token)):
    return {"message": "Access granted"}
```

### 5. Type Hints Everywhere

```python
from fastapi import FastAPI, Path, Query
from typing import Optional, List

app = FastAPI()

@app.get("/search/")
async def search(
    q: str = Query(..., min_length=3, max_length=50),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    tags: Optional[List[str]] = None,
):
    return {"query": q, "skip": skip, "limit": limit, "tags": tags}
```

---

## Performance Benchmarks

FastAPI is one of the fastest Python frameworks available, on par with Go and Node.js frameworks.

### TechEmpower Round 21 Results (Normalized)

| Framework | Language | Performance Score |
|-----------|----------|-------------------|
| FastAPI + Uvicorn | Python | ~85,000 req/s |
| Starlette | Python | ~90,000 req/s |
| Flask | Python | ~45,000 req/s |
| Django | Python | ~25,000 req/s |
| Express | Node.js | ~75,000 req/s |
| Gin | Go | ~95,000 req/s |

> **Note**: These are approximate figures for JSON serialization benchmarks. Real-world performance varies based on workload.

### Why is FastAPI Fast?

1. **Async I/O**: Non-blocking I/O operations using Python's `async`/`await`
2. **Starlette**: The underlying framework is highly optimized
3. **Pydantic v2**: Validation in Rust (compiled), not pure Python
4. **Minimal overhead**: No unnecessary middleware or processing
5. **ASGI**: Uses Uvicorn (libuv) which is extremely fast

### Benchmark Comparison: JSON Serialization

```python
# This endpoint benchmarks at ~85,000 req/s on a modern server
@app.get("/benchmark")
async def benchmark():
    return {"message": "Hello, World!"}
```

### Real-World Performance Tips

```python
# Use ORJSONResponse for even faster JSON serialization
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)

# ORJSON is 10x faster than standard json for some workloads
```

---

## Type Safety in FastAPI

FastAPI's type system is its superpower. Every type hint serves multiple purposes:

### A Single Type Hint Does Three Things

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}
```

This single `user_id: int` type hint:

1. **Documentation**: Shows `user_id` as an integer in Swagger UI
2. **Validation**: Rejects non-integer values (e.g., `"abc"` → 422 error)
3. **Conversion**: Converts string `"123"` to integer `123` automatically

### Comprehensive Type Checking

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum

class Status(str, Enum):
    active = "active"
    inactive = "inactive"
    pending = "pending"

class CreateUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr  # Validates email format automatically
    age: int = Field(..., ge=0, le=150)
    status: Status = Status.active
    tags: List[str] = []
    created_at: Optional[datetime] = None

@app.post("/users/", status_code=201)
async def create_user(user: CreateUser):
    # user.email is guaranteed to be a valid email
    # user.age is guaranteed to be between 0 and 150
    # user.status is guaranteed to be a valid Status enum
    return user
```

### Type Safety Benefits

```python
# WITHOUT type safety (Django/Flask style)
def create_user(request):
    data = request.json()
    name = data.get("name")  # Could be anything
    age = data.get("age")    # Could be a string
    # No validation, no documentation, bugs at runtime

# WITH FastAPI type safety
@app.post("/users/")
async def create_user(user: UserCreate):
    # user.name is guaranteed to be a string
    # user.age is guaranteed to be an integer
    # Validation happens BEFORE your code runs
    # Documentation is automatic
    return user
```

---

## Why FastAPI Over Alternatives

### vs Flask

| Feature | FastAPI | Flask |
|---------|---------|-------|
| Async support | Native | Limited (Flask 2.0+) |
| Auto documentation | Yes | No (need flask-restx) |
| Request validation | Automatic | Manual |
| Type checking | Built-in | Not built-in |
| Performance | ~85k req/s | ~45k req/s |
| Learning curve | Easy | Easier |
| Ecosystem | Growing fast | Very mature |

### vs Django REST Framework

| Feature | FastAPI | DRF |
|---------|---------|-----|
| Speed | Much faster | Slower |
| Async | Native | Limited |
| Admin UI | Not built-in | Built-in |
| ORM | Optional (SQLModel) | Django ORM (built-in) |
| Authentication | Flexible | Built-in |
| Scalability | Excellent | Good |
| Maturity | Newer | Very mature |

### vs Sanic

| Feature | FastAPI | Sanic |
|---------|---------|-------|
| Type validation | Pydantic (automatic) | Manual |
| Documentation | Auto-generated | Not built-in |
| Performance | Similar | Similar |
| Community | Larger, growing | Smaller |
| Documentation quality | Excellent | Good |

### vs Tornado

| Feature | FastAPI | Tornado |
|---------|---------|---------|
| Modern Python | Full support | Partial |
| Type safety | Full | None |
| Documentation | Automatic | Manual |
| Learning curve | Easy | Moderate |
| WebSocket support | Yes | Yes |

---

## The FastAPI Ecosystem

### Core Packages

| Package | Purpose | Author |
|---------|---------|--------|
| `fastapi` | The web framework | Sebastián Ramírez |
| `starlette` | ASGI toolkit | Encode |
| `pydantic` | Data validation | Samuel Colvin |
| `uvicorn` | ASGI server | Encode |
| `sqlmodel` | ORM + Pydantic | Sebastián Ramírez |

### Community Packages

```bash
# Database
pip install sqlalchemy sqlmodel tortoise-orm databases asyncpg

# Authentication
pip install python-jose[cryptography] passlib[bcrypt] python-multipart

# Testing
pip install httpx pytest pytest-asyncio

# Documentation
pip install fastapi-extra slowapi

# Background tasks
pip install dramatiq arq celery

# Caching
pip install fastapi-cache2 redis

# Rate limiting
pip install slowapi

# CORS
pip install fastapi-cors  # Or use built-in CORSMiddleware
```

### FastAPI vs Flask Ecosystem Comparison

```
Flask:                          FastAPI:
├── Flask-RESTful               ├── FastAPI (built-in)
├── Flask-RESTPlus/RESTX        ├── Automatic docs
├── Flask-Marshmallow           ├── Pydantic (built-in)
├── Flask-SQLAlchemy            ├── SQLModel
├── Flask-Migrate              ├── Alembic (direct)
├── Flask-Login                ├── python-jose + passlib
├── Flask-JWT-Extended          ├── FastAPI Security utilities
├── Flask-CORS                 ├── CORSMiddleware (built-in)
└── Flask-WTF                  └── Form data (built-in)
```

---

## Industry Adoption

### Companies Using FastAPI in Production

| Company | Use Case |
|---------|----------|
| **Microsoft** | Azure services, Power Platform |
| **Uber** | Internal microservices |
| **Netflix** | Studio production workflows |
| **Airbnb** | ML model serving |
| **Slack** | Internal tools |
| **Netflix** | Data APIs |
| **IBM** | Watson services |
| **Intel** | Edge computing |
| **SAP** | Enterprise APIs |
| **NASA** | Data processing APIs |
| **Polygon.io** | Geospatial data APIs |

### Open Source Projects

- **Nginx Unit**: Python runtime support
- **Robusta**: Kubernetes monitoring platform
- **Metlo**: API security platform
- **Hoppscotch**: API testing (backend)

### GitHub Statistics (as of 2025)

- **Stars**: 80,000+
- **Forks**: 7,000+
- **Contributors**: 700+
- **PyPI Downloads**: 150M+ monthly

---

## When NOT to Use FastAPI

### 1. Full-Stack Web Applications with Templates

If you need server-side rendering, admin panels, and a full-stack framework:

```python
# Flask/Django might be better for:
# - Traditional server-rendered web apps
# - Apps with complex admin interfaces
# - Projects requiring built-in ORM with migrations
```

**Alternative**: Use Django (with Django templates) or Flask (with Jinja2).

### 2. Simple Microservices That Don't Need Validation

For extremely simple services where you just need to forward requests:

```python
# If you just need a simple proxy, consider:
# - aiohttp for lightweight async
# - httpx for simple request forwarding
```

### 3. Teams Without Python Experience

If your team is experienced in Go/Node.js and unfamiliar with Python, the learning curve may not be worth it.

### 4. Projects Requiring Mature Admin UI

Django's admin interface is unmatched for rapid internal tool development. FastAPI has no equivalent.

### 5. Real-Time Applications (Primarily WebSocket)

While FastAPI supports WebSockets, frameworks like Socket.io (Node.js) or Django Channels may be better for chat-heavy applications.

### 6. Extremely Simple CRUD APIs

For trivial APIs, Flask might be simpler:

```python
# Flask - simpler for trivial APIs
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/users")
def get_users():
    return jsonify([...])
```

### 7. When You Need Legacy Python Support

FastAPI requires Python 3.7+. If you're stuck on Python 2 or 3.5, use Flask or Django.

---

## Interview Questions

### Q1: What is FastAPI and why should I use it?

**Answer:** FastAPI is a modern, high-performance Python web framework for building APIs. It's built on Starlette (ASGI) and Pydantic (validation), and uses Python type hints for automatic validation, serialization, and documentation generation. It's 2-3x faster than Flask and Django, and provides type safety that catches bugs at development time.

### Q2: How does FastAPI achieve its performance?

**Answer:** FastAPI achieves performance through:
1. Native async/await support (non-blocking I/O)
2. Starlette's optimized ASGI implementation
3. Pydantic v2's Rust-based validation engine
4. Minimal overhead (no unnecessary middleware)
5. Uvicorn's libuv-based event loop

### Q3: What is the relationship between FastAPI, Starlette, and Pydantic?

**Answer:** FastAPI is the high-level framework that developers interact with. Starlette provides the underlying ASGI toolkit (routing, middleware, request/response objects). Pydantic handles data validation and serialization using Python type hints. FastAPI combines these to provide automatic validation, documentation, and serialization.

### Q4: What Python version does FastAPI require?

**Answer:** FastAPI requires Python 3.7 or higher. However, Python 3.9+ is recommended for full functionality (e.g., built-in generic types like `list[str]` instead of `List[str]`). Python 3.10+ is ideal for `Annotated` type syntax.

### Q5: Is FastAPI production-ready?

**Answer:** Yes. FastAPI is used in production by Microsoft, Uber, Netflix, Airbnb, and many other large companies. It has 80,000+ GitHub stars, 150M+ monthly PyPI downloads, and active maintenance. It's fully production-ready for APIs of any scale.

### Q6: What are the alternatives to FastAPI in Python?

**Answer:** The main alternatives are:
- **Flask**: Simpler, more mature, but slower and without automatic docs
- **Django REST Framework**: Full-featured with built-in ORM, admin, but heavier
- **Sanic**: Similar async support, but less ecosystem
- **Tornado**: Older async framework, less Pythonic
- **Litestar**: Similar to FastAPI with some different design choices
