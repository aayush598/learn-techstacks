# Pytest Setup with FastAPI

## Table of Contents

1. [Introduction to Testing in FastAPI](#1-introduction)
2. [Installing Pytest and Dependencies](#2-installation)
3. [Your First Test](#3-first-test)
4. [TestClient from Starlette](#4-testclient)
5. [conftest.py and Fixtures](#5-conftest)
6. [Fixture Scopes](#6-fixture-scopes)
7. [pytest-asyncio for Async Tests](#7-pytest-asyncio)
8. [Async Test Client](#8-async-test-client)
9. [Test Database Setup](#9-test-database)
10. [Pytest Markers](#10-markers)
11. [Parametrize](#11-parametrize)
12. [Test Configuration](#12-configuration)
13. [Best Practices](#13-best-practices)
14. [Interview Questions](#14-interview-questions)

---

## 1. Introduction to Testing in FastAPI <a name="1-introduction"></a>

Testing is a critical part of building production-grade FastAPI applications. FastAPI is
specifically designed to be easy to test, providing built-in tools and patterns that make
writing tests straightforward.

### Why Test FastAPI Applications?

- **Regression Prevention**: Catch bugs before they reach production
- **Documentation**: Tests serve as executable documentation of API behavior
- **Refactoring Safety**: Change code confidently knowing tests will catch breakage
- **Code Quality**: Enforces better design through testable patterns
- **API Contract Verification**: Ensures your API behaves as documented

### Testing Pyramid for FastAPI

```
        /  E2E  \          Few: Full stack tests with real DB, auth, etc.
       /----------\
      / Integration \      Medium: Test route + service + DB together
     /----------------\
    /    Unit Tests     \  Many: Test individual functions, validators, utils
```

### FastAPI Testing Tools

| Tool | Purpose |
|------|---------|
| `pytest` | Test runner and framework |
| `TestClient` | Synchronous HTTP testing (from Starlette) |
| `httpx.AsyncClient` | Async HTTP testing |
| `pytest-asyncio` | Async test support |
| `factory_boy` | Test data generation |
| `coverage.py` | Code coverage measurement |
| `faker` | Fake data generation |
| `responses` / `respx` | Mock HTTP responses |

---

## 2. Installing Pytest and Dependencies <a name="2-installation"></a>

```bash
# Core testing dependencies
pip install pytest pytest-asyncio httpx coverage

# For async database testing
pip install aiosqlite pytest-aiohttp

# For test data generation
pip install factory-boy faker

# For mocking HTTP requests
pip install respx

# For code coverage
pip install pytest-cov

# All at once
pip install pytest pytest-asyncio httpx coverage aiosqlite \
    factory-boy faker respx pytest-cov
```

### Project Structure for Tests

```
myapp/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   └── db.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Shared fixtures
│   ├── pytest.ini            # Pytest configuration
│   ├── test_users.py
│   ├── test_items.py
│   ├── test_services/
│   │   ├── __init__.py
│   │   ├── conftest.py       # Service-level fixtures
│   │   └── test_user_service.py
│   └── test_routes/
│       ├── __init__.py
│       ├── conftest.py       # Route-level fixtures
│       └── test_user_routes.py
├── pytest.ini
├── pyproject.toml
└── requirements-test.txt
```

### pyproject.toml Configuration

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
filterwarnings = [
    "ignore::DeprecationWarning",
]

[tool.coverage.run]
source = ["app"]
omit = ["tests/*", "app/migrations/*"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

---

## 3. Your First Test <a name="3-first-test"></a>

### The Application Under Test

```python
# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    total: float

items_db: dict[int, Item] = {}
counter = 0

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items/", response_model=ItemResponse, status_code=201)
async def create_item(item: Item):
    global counter
    counter += 1
    total = item.price + (item.tax or 0)
    items_db[counter] = item
    return ItemResponse(
        id=counter,
        name=item.name,
        price=item.price,
        total=total,
    )

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    item = items_db[item_id]
    return ItemResponse(
        id=item_id,
        name=item.name,
        price=item.price,
        total=item.price + (item.tax or 0),
    )

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
```

### The Simplest Test

```python
# tests/test_basic.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post(
        "/items/",
        json={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 23.5,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Foo"
    assert data["price"] == 23.5
    assert data["total"] == 23.5

def test_create_item_with_tax():
    response = client.post(
        "/items/",
        json={
            "name": "Bar",
            "price": 10.0,
            "tax": 2.5,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["total"] == 12.5
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific file
pytest tests/test_basic.py

# Run specific test function
pytest tests/test_basic.py::test_read_main

# Run with print output visible
pytest -s

# Run with traceback
pytest --tb=long

# Run in parallel
pytest -n auto
```

---

## 4. TestClient from Starlette <a name="4-testclient"></a>

The `TestClient` wraps `httpx` and allows you to make HTTP requests to your FastAPI
application as if it were a real server, without actually starting it.

### TestClient Features

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Basic GET request
response = client.get("/items/")

# POST with JSON body
response = client.post("/items/", json={"name": "Test", "price": 10.0})

# POST with form data
response = client.post("/login", data={"username": "admin", "password": "secret"})

# Upload files
response = client.post(
    "/upload",
    files={"file": ("test.txt", b"file content", "text/plain")},
)

# Query parameters
response = client.get("/items/?skip=0&limit=10")

# Path parameters are part of the URL
response = client.get("/items/1")

# Custom headers
response = client.get("/items/", headers={"X-Custom": "value"})

# Cookies
client.cookies.set("session_id", "abc123")
response = client.get("/profile/")

# Authentication
response = client.get("/users/me", auth=("user", "pass"))

# Timeout configuration
client = TestClient(app, timeout=30.0)

# Follow redirects
response = client.get("/redirect-target", follow_redirects=True)

# Raise server exceptions (default: True)
# When True, raises Exception if server returns 5xx
client = TestClient(app, raise_server_exceptions=False)
```

### Testing Headers and Response Details

```python
def test_response_headers():
    response = client.get("/")
    assert response.status_code == 200
    assert "content-type" in response.headers
    assert response.headers["content-type"] == "application/json"

def test_response_body():
    response = client.get("/items/1")
    assert response.status_code == 200

    # Parse JSON
    data = response.json()
    assert "name" in data

    # Access raw text
    text = response.text
    assert "Foo" in text

    # Check content length
    assert response.headers["content-length"]
```

### Testing Request Bodies

```python
# JSON body
response = client.post("/items/", json={"name": "Foo", "price": 10.0})

# Form data
response = client.post("/login", data={"username": "admin"})

# Form data with files
response = client.post(
    "/create-with-file",
    data={"name": "My Item"},
    files={"avatar": ("avatar.png", b"png content", "image/png")},
)

# Raw body
response = client.post(
    "/raw",
    content=b"raw bytes",
    headers={"Content-Type": "application/octet-stream"},
)
```

### Testing Dependencies and State

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.db = "connected"

@app.on_event("shutdown")
async def shutdown():
    app.state.db = "disconnected"

@app.get("/status")
async def status():
    return {"db": app.state.db}

# TestClient handles startup/shutdown events automatically
def test_app_state():
    with TestClient(app) as client:
        response = client.get("/status")
        assert response.json() == {"db": "connected"}

# Or manually control events
def test_manual_events():
    client = TestClient(app, raise_server_exceptions=False)
    # Client is ready without calling startup
```

---

## 5. conftest.py and Fixtures <a name="5-conftest"></a>

`conftest.py` is a special file that pytest uses to share fixtures across test files
within a directory. It's the backbone of test organization.

### Basic conftest.py

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a TestClient for each test."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_item():
    """Provide a sample item for tests."""
    return {
        "name": "Test Item",
        "description": "A test item description",
        "price": 29.99,
        "tax": 2.5,
    }


@pytest.fixture
def created_item(client, sample_item):
    """Create an item and return the response data."""
    response = client.post("/items/", json=sample_item)
    assert response.status_code == 201
    return response.json()
```

### Using Fixtures in Tests

```python
# tests/test_items.py
import pytest

def test_get_item(client, created_item):
    """Test fetching an item that was already created."""
    response = client.get(f"/items/{created_item['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_item_not_found(client):
    """Test 404 for nonexistent item."""
    response = client.get("/items/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_create_multiple_items(client, sample_item):
    """Test creating multiple items."""
    for i in range(5):
        item = {**sample_item, "name": f"Item {i}"}
        response = client.post("/items/", json=item)
        assert response.status_code == 201
```

### Hierarchical conftest.py

```
tests/
├── conftest.py              # Shared across ALL tests
├── test_routes/
│   ├── conftest.py          # Shared across route tests
│   └── test_user_routes.py
├── test_services/
│   ├── conftest.py          # Shared across service tests
│   └── test_user_service.py
└── test_models/
    ├── conftest.py          # Shared across model tests
    └── test_user_model.py
```

```python
# tests/conftest.py - Root level
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db, Base, engine

@pytest.fixture(scope="session")
def test_app():
    """Application setup for entire test session."""
    Base.metadata.create_all(bind=engine)
    yield app
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def client(test_app):
    """Session-scoped test client."""
    with TestClient(test_app) as c:
        yield c

# tests/test_routes/conftest.py - Route level
import pytest

@pytest.fixture
def auth_headers():
    """Authentication headers for protected routes."""
    # In real app, you'd generate a JWT token
    return {"Authorization": "Bearer test-token-123"}

@pytest.fixture
def admin_headers():
    """Admin authentication headers."""
    return {"Authorization": "Bearer admin-token-456"}

# tests/test_services/conftest.py - Service level
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_db():
    """Mock database session for service tests."""
    db = AsyncMock()
    db.add = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    return db
```

---

## 6. Fixture Scopes <a name="6-fixture-scopes"></a>

Fixture scopes determine how often a fixture is setup and torn down during test execution.

### Scope Types

```python
import pytest

# FUNCTION scope (default) - Created and destroyed for EACH test
@pytest.fixture(scope="function")
def function_fixture():
    """Runs setup before each test, teardown after each test."""
    setup = "setup"
    yield setup
    cleanup = "teardown"

# CLASS scope - Created once per test class
@pytest.fixture(scope="class")
def class_fixture():
    """Runs setup once before the class, teardown once after."""
    setup = "setup"
    yield setup
    cleanup = "teardown"

# MODULE scope - Created once per test file
@pytest.fixture(scope="module")
def module_fixture():
    """Runs setup once before the module, teardown once after."""
    setup = "setup"
    yield setup
    cleanup = "teardown"

# SESSION scope - Created once for entire test session
@pytest.fixture(scope="session")
def session_fixture():
    """Runs setup once before all tests, teardown once after."""
    setup = "setup"
    yield setup
    cleanup = "teardown"
```

### Practical Scope Examples

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base

# SESSION: Create engine once for all tests
@pytest.fixture(scope="session")
def engine():
    """Create a test database engine for the entire session."""
    engine = create_engine(
        "sqlite:///./test.db",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    import os
    os.remove("test.db")

# MODULE: Create tables once per test module
@pytest.fixture(scope="module")
def db_setup(engine):
    """Create fresh tables for each module."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# FUNCTION: Fresh session for each test
@pytest.fixture(scope="function")
def db_session(engine):
    """Create a fresh database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

# FUNCTION: Always a fresh TestClient per test
@pytest.fixture(scope="function")
def client(db_session):
    """Fresh TestClient with overridden DB dependency."""
    from app.main import app
    from app.db import get_db

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
```

### Scope Behavior Diagram

```
Test Session
├── scope="session" fixture: SETUP (once)
│   ├── Module 1
│   │   ├── scope="module" fixture: SETUP (once per module)
│   │   ├── Test A
│   │   │   ├── scope="function" fixture: SETUP
│   │   │   ├── scope="class" fixture: SETUP (once per class)
│   │   │   └── scope="function" fixture: TEARDOWN
│   │   ├── Test B
│   │   │   ├── scope="function" fixture: SETUP
│   │   │   └── scope="function" fixture: TEARDOWN
│   │   └── scope="module" fixture: TEARDOWN
│   ├── Module 2
│   │   ├── scope="module" fixture: SETUP
│   │   ├── Test C
│   │   │   ├── scope="function" fixture: SETUP
│   │   │   └── scope="function" fixture: TEARDOWN
│   │   └── scope="module" fixture: TEARDOWN
│   └── ...
└── scope="session" fixture: TEARDOWN (once)
```

---

## 7. pytest-asyncio for Async Tests <a name="7-pytest-asyncio"></a>

Since FastAPI supports async route handlers, you need `pytest-asyncio` to test them
asynchronously.

### Setup

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"  # All async tests run automatically
```

### Writing Async Tests

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


# With asyncio_mode = "auto", no decorator needed
async def test_read_main():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


async def test_create_item():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/items/",
            json={"name": "Async Item", "price": 15.0},
        )
    assert response.status_code == 201
    assert response.json()["name"] == "Async Item"


# With asyncio_mode = "strict", you need the decorator
@pytest.mark.asyncio
async def test_explicit_async():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
```

### Async Fixtures

```python
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.main import app
from app.db import Base, get_db

# Async fixture using pytest_asyncio.fixture
@pytest_asyncio.fixture
async def async_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///./async_test.db",
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture
async def async_session(async_engine):
    async with AsyncSession(async_engine) as session:
        yield session

@pytest_asyncio.fixture
async def async_client(async_session):
    transport = ASGITransport(app=app)

    async def override_get_db():
        yield async_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# Using async fixtures
async def test_async_with_db(async_client):
    response = await async_client.post(
        "/items/",
        json={"name": "DB Item", "price": 100.0},
    )
    assert response.status_code == 201

    response = await async_client.get("/items/1")
    assert response.status_code == 200
```

### Mixing Sync and Async Fixtures

```python
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app


# Synchronous fixture
@pytest.fixture
def seed_data():
    return [
        {"name": "Item 1", "price": 10.0},
        {"name": "Item 2", "price": 20.0},
        {"name": "Item 3", "price": 30.0},
    ]


# Async fixture that uses sync fixture
@pytest_asyncio.fixture
async def seeded_client(seed_data):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for item in seed_data:
            await ac.post("/items/", json=item)
        yield ac


async def test_seeded_data(seeded_client):
    response = await seeded_client.get("/items/")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 3
```

---

## 8. Async Test Client <a name="8-async-test-client"></a>

The async test client uses `httpx.AsyncClient` with ASGI transport to test FastAPI
applications without starting a real server.

### Basic Async Client Setup

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


# All tests can now use the async client
async def test_home(client):
    response = await client.get("/")
    assert response.status_code == 200

async def test_create(client):
    response = await client.post("/items/", json={"name": "Foo", "price": 1.0})
    assert response.status_code == 201
```

### Custom Transport Configuration

```python
from httpx import ASGITransport

# Custom headers for all requests
transport = ASGITransport(
    app=app,
    raise_app_exceptions=False,   # Don't raise app exceptions
    root_path="/api/v1",          # Set root path
)

# Testing with client kwargs
client = AsyncClient(
    transport=transport,
    base_url="http://testserver",
    headers={"X-Request-ID": "test-123"},
    timeout=30.0,
    cookies={"session": "abc"},
)
```

### Async Client Patterns

```python
async def test_concurrent_requests(client):
    """Test that concurrent requests work correctly."""
    import asyncio

    tasks = [
        client.get(f"/items/{i}")
        for i in range(1, 6)
    ]
    responses = await asyncio.gather(*tasks)
    for response in responses:
        assert response.status_code in (200, 404)

async def test_websocket(client):
    """Test WebSocket connections."""
    async with client.stream("GET", "/ws") as stream:
        async for line in stream.aiter_lines():
            assert line
            break

async def test_file_upload(client):
    """Test file upload with async client."""
    files = {
        "file": ("test.txt", b"file contents", "text/plain"),
    }
    response = await client.post("/upload", files=files)
    assert response.status_code == 200

async def test_form_data(client):
    """Test form data submission."""
    response = await client.post(
        "/login",
        data={"username": "admin", "password": "secret"},
    )
    assert response.status_code == 200

async def test_query_params(client):
    """Test query parameter handling."""
    response = await client.get(
        "/items/",
        params={"skip": 0, "limit": 5, "sort": "name"},
    )
    assert response.status_code == 200

async def test_response_streaming(client):
    """Test streaming response."""
    async with client.stream("GET", "/stream") as response:
        chunks = []
        async for chunk in response.aiter_bytes():
            chunks.append(chunk)
        assert len(chunks) > 0
```

---

## 9. Test Database Setup <a name="9-test-database"></a>

Testing with a real database requires careful setup to ensure test isolation.

### SQLite In-Memory for Tests

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db import Base, get_db
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def test_engine():
    """Create a session-scoped test database engine."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_engine):
    """Create a fresh database session with rollback for each test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create a TestClient with database dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
```

### PostgreSQL for Integration Tests

```python
# tests/conftest_integration.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
import os

DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://test:test@localhost:5432/test_db"
)


@pytest.fixture(scope="session")
def integration_engine():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def integration_session(integration_engine):
    connection = integration_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def integration_client(integration_session):
    def override_get_db():
        yield integration_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
```

### Async Database Testing

```python
# tests/conftest_async.py
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.pool import StaticPool
from app.db import Base, get_db
from app.main import app
from httpx import AsyncClient, ASGITransport

TEST_DATABASE_URL = "sqlite+aiosqlite://"

@pytest_asyncio.fixture(scope="session")
async def async_test_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def async_db_session(async_test_engine):
    async with async_sessionmaker(
        async_test_engine, class_=AsyncSession, expire_on_commit=False
    )() as session:
        async with session.begin():
            yield session
            await session.rollback()


@pytest_asyncio.fixture
async def async_test_client(async_db_session):
    async def override_get_db():
        yield async_db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
```

---

## 10. Pytest Markers <a name="10-markers"></a>

Markers let you categorize and selectively run tests.

### Built-in Markers

```python
import pytest

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Does not run on Windows",
)
def test_linux_only():
    pass

@pytest.mark.xfail(reason="Known bug #123")
def test_known_failure():
    pass

@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("a" * 100, 100),
])
def test_string_length(input, expected):
    assert len(input) == expected
```

### Custom Markers

```python
# pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "integration: integration tests",
    "unit: unit tests",
    "security: security tests",
    "smoke: quick smoke tests",
    "api: API route tests",
    "db: database tests",
]

# tests/conftest.py
import pytest

def pytest_collection_modifyitems(config, items):
    """Auto-mark tests based on file path."""
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        if "security" in str(item.fspath):
            item.add_marker(pytest.mark.security)
```

### Using Markers in Tests

```python
import pytest

@pytest.mark.unit
def test_validate_email():
    assert validate_email("test@example.com") is True

@pytest.mark.integration
@pytest.mark.db
async def test_create_user_in_db(async_db_session):
    user = User(name="Test", email="test@test.com")
    async_db_session.add(user)
    await async_db_session.commit()
    assert user.id is not None

@pytest.mark.slow
@pytest.mark.integration
async def test_large_dataset_processing():
    """Process 10,000 records."""
    for i in range(10000):
        await process_record(i)

@pytest.mark.smoke
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200

@pytest.mark.api
@pytest.mark.security
def test_protected_endpoint(client, auth_headers):
    response = client.get("/admin/users", headers=auth_headers)
    assert response.status_code == 200
```

### Running Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run all except slow tests
pytest -m "not slow"

# Run smoke tests
pytest -m smoke

# Combine markers
pytest -m "integration and not slow"
pytest -m "unit or smoke"
```

---

## 11. Parametrize <a name="11-parametrize"></a>

`@pytest.mark.parametrize` lets you run the same test with different inputs.

### Basic Parametrize

```python
import pytest

@pytest.mark.parametrize("number", [1, 2, 3, 4, 5])
def test_is_positive(number):
    assert number > 0

@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("a", 1),
    ("Hello World", 11),
])
def test_string_length(input, expected):
    assert len(input) == expected

# Multiple parameters (creates cartesian product)
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):
    result = x * y
    assert result > 0
```

### Parametrize with IDs

```python
@pytest.mark.parametrize(
    "email,valid",
    [
        ("user@example.com", True),
        ("invalid-email", False),
        ("user@.com", False),
        ("@example.com", False),
        ("user@example", False),
    ],
    ids=[
        "valid-email",
        "missing-at-sign",
        "invalid-domain",
        "missing-local-part",
        "missing-tld",
    ],
)
def test_email_validation(email, valid):
    assert validate_email(email) == valid
```

### Parametrize FastAPI Endpoints

```python
@pytest.mark.parametrize(
    "payload,expected_status,expected_name",
    [
        ({"name": "Foo", "price": 10.0}, 201, "Foo"),
        ({"name": "Bar", "price": 0.01}, 201, "Bar"),
        ({}, 422, None),               # Missing required fields
        ({"name": ""}, 422, None),     # Empty name
        ({"name": "X", "price": -1}, 422, None),  # Negative price
    ],
    ids=[
        "valid-item",
        "low-price-item",
        "missing-fields",
        "empty-name",
        "negative-price",
    ],
)
def test_create_item_validation(client, payload, expected_status, expected_name):
    response = client.post("/items/", json=payload)
    assert response.status_code == expected_status
    if expected_name:
        assert response.json()["name"] == expected_name
```

### Parametrize with Fixtures

```python
@pytest.fixture
def db_users():
    return [
        {"name": "Alice", "role": "admin"},
        {"name": "Bob", "role": "user"},
        {"name": "Charlie", "role": "moderator"},
    ]

@pytest.mark.parametrize("user_index,expected_role", [
    (0, "admin"),
    (1, "user"),
    (2, "moderator"),
])
def test_user_roles(client, db_users, user_index, expected_role):
    user = db_users[user_index]
    response = client.post("/users/", json=user)
    assert response.status_code == 201
    assert response.json()["role"] == expected_role
```

---

## 12. Test Configuration <a name="12-configuration"></a>

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    slow: Slow running tests
    integration: Integration tests
    unit: Unit tests
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

### conftest.py Hooks

```python
# tests/conftest.py
import pytest
import time

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection."""
    # Add markers based on path
    for item in items:
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)

def pytest_runtest_setup(item):
    """Setup before each test."""
    if "slow" in item.keywords:
        item.add_marker(pytest.mark.timeout(30))

def pytest_runtest_teardown(item):
    """Teardown after each test."""
    pass

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Add additional info to test reports."""
    if call.when == "call":
        if call.excinfo is not None:
            item.add_marker(pytest.mark.xfail)

# Session-scoped setup
@pytest.fixture(autouse=True)
def setup_test_environment(request):
    """Auto-use fixture for every test."""
    # Setup
    import os
    os.environ["TESTING"] = "1"
    yield
    # Teardown
    os.environ.pop("TESTING", None)
```

---

## 13. Best Practices <a name="13-best-practices"></a>

### 1. One Assert Per Test (Preferably)

```python
# BAD: Multiple unrelated assertions
def test_item(client):
    response = client.post("/items/", json={"name": "Foo", "price": 10})
    assert response.status_code == 201
    assert response.json()["name"] == "Foo"
    # Test something completely different
    response2 = client.get("/health")
    assert response2.status_code == 200

# GOOD: Focused tests
def test_create_item_returns_201(client):
    response = client.post("/items/", json={"name": "Foo", "price": 10})
    assert response.status_code == 201

def test_create_item_returns_correct_name(client):
    response = client.post("/items/", json={"name": "Foo", "price": 10})
    assert response.json()["name"] == "Foo"

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
```

### 2. Use Descriptive Test Names

```python
# BAD
def test_1():
def test_create():
def test_error():

# GOOD
def test_create_item_with_valid_data_returns_201():
def test_get_nonexistent_item_returns_404():
def test_create_item_with_negative_price_returns_422():
```

### 3. Arrange-Act-Assert Pattern

```python
def test_create_and_fetch_item(client):
    # Arrange
    item_data = {"name": "Widget", "price": 9.99}

    # Act
    create_response = client.post("/items/", json=item_data)

    # Assert
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]

    # Act
    get_response = client.get(f"/items/{item_id}")

    # Assert
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Widget"
```

### 4. Keep Tests Independent

```python
# BAD: Test depends on previous test's state
def test_create_item(client):
    response = client.post("/items/", json={"name": "Foo", "price": 10})
    assert response.status_code == 201

def test_get_item(client):
    # This fails if test_create_item didn't run
    response = client.get("/items/1")
    assert response.status_code == 200

# GOOD: Each test sets up its own state
def test_get_item(client):
    create_response = client.post(
        "/items/",
        json={"name": "Foo", "price": 10},
    )
    item_id = create_response.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
```

### 5. Test Error Cases

```python
def test_error_cases(client):
    # Test 404
    response = client.get("/items/99999")
    assert response.status_code == 404

    # Test 422 - Validation error
    response = client.post("/items/", json={"name": ""})
    assert response.status_code == 422

    # Test 401 - Unauthorized
    response = client.get("/admin/dashboard")
    assert response.status_code == 401

    # Test 403 - Forbidden
    response = client.get(
        "/admin/dashboard",
        headers={"Authorization": "Bearer regular-user-token"},
    )
    assert response.status_code == 403

    # Test 405 - Method not allowed
    response = client.put("/items/")
    assert response.status_code == 405
```

### 6. Use Fixtures for Shared Setup

```python
@pytest.fixture
def admin_user(client):
    response = client.post("/users/", json={
        "name": "Admin",
        "email": "admin@test.com",
        "role": "admin",
        "password": "securepassword",
    })
    return response.json()

@pytest.fixture
def admin_token(client, admin_user):
    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "securepassword",
    })
    return response.json()["access_token"]

@pytest.fixture
def admin_client(client, admin_token):
    client.headers["Authorization"] = f"Bearer {admin_token}"
    return client

def test_admin_endpoint(admin_client):
    response = admin_client.get("/admin/users")
    assert response.status_code == 200
```

---

## 14. Interview Questions <a name="14-interview-questions"></a>

### Basic Level

1. **What is pytest and why use it with FastAPI?**
   pytest is a Python testing framework that provides fixtures, parametrize,
   markers, and plugins. FastAPI is designed to be testable, and pytest makes
   testing efficient with its clean syntax.

2. **What is TestClient and how does it work?**
   TestClient from Starlette wraps httpx and sends requests to the ASGI app
   without starting a real server. It handles ASGI lifespan events automatically.

3. **What is the difference between sync and async test clients?**
   Sync TestClient blocks during requests. Async client (httpx.AsyncClient with
   ASGITransport) allows `await` for concurrent requests, better for testing
   async routes.

4. **What is conftest.py?**
   A pytest file that provides shared fixtures and hooks to all test files in its
   directory and subdirectories. It's automatically loaded by pytest.

5. **How do you run a specific test?**
   `pytest tests/test_items.py::test_create_item` or `pytest -k "test_create"`

### Intermediate Level

6. **What are fixture scopes and when use each?**
   - `function`: Per test (default) - fresh data per test
   - `class`: Per test class - shared across class methods
   - `module`: Per file - expensive setup shared across file
   - `session`: Entire run - DB engine, seed data

7. **How do you test database operations in FastAPI?**
   Use dependency overrides with `app.dependency_overrides[get_db]` to inject
   a test database session. Use transactions with rollback for isolation.

8. **What is the purpose of `pytest.mark.parametrize`?**
   Runs the same test with multiple input sets. Each set becomes a separate test
   case, reducing code duplication and improving coverage.

9. **How do you handle async tests?**
   Install pytest-asyncio, set `asyncio_mode = "auto"` in pyproject.toml, write
   tests as `async def`, use httpx.AsyncClient with ASGITransport.

10. **How do you ensure test isolation with a database?**
    Wrap each test in a transaction, roll back after each test. Or use in-memory
    SQLite with StaticPool. Never share mutable state between tests.

### Advanced Level

11. **How do you test middleware?**
    Create the client with the app (which has middleware attached), make requests,
    and assert on response headers and status codes. Middleware runs automatically.

12. **How do you test WebSocket endpoints?**
    Use httpx.AsyncClient or Starlette TestClient's websocket_connect context
    manager. Test bidirectional messaging and connection lifecycle.

13. **What is dependency overriding and why is it powerful?**
    `app.dependency_overrides[dep] = mock_dep` replaces a dependency for all
    routes that use it. Enables testing without real DB, auth, or external services.

14. **How do you test background tasks?**
    Use `pytest-asyncio` with `await` to let background tasks complete, or mock
    the background task function to verify it was called with correct arguments.

15. **How do you structure tests for a large FastAPI project?**
    Mirror the app structure in tests/, use hierarchical conftest.py, separate
    unit/integration/e2e tests, use markers to categorize, and maintain shared
    fixtures at appropriate levels.

16. **What is the testing pyramid and how does it apply to FastAPI?**
    Many unit tests (services, utilities) > some integration tests (routes + DB)
    > few E2E tests (full stack). FastAPI's dependency injection makes integration
    testing easy.

17. **How do you test file uploads?**
    Use `files` parameter in TestClient: `client.post("/upload", files={"file":
    ("name.txt", b"content", "text/plain")})`.

18. **How do you test authentication and authorization?**
    Generate test tokens, use dependency overrides to mock auth, or use fixtures
    that create authenticated clients with valid tokens.

19. **What is autouse in pytest fixtures?**
    `@pytest.fixture(autouse=True)` makes the fixture run for every test in scope
    without explicitly requesting it. Useful for setup/teardown that every test needs.

20. **How do you test exception handlers?**
    Create test cases that trigger the exception, assert the response status code
    and body match what the exception handler produces.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| TestClient | Sync HTTP testing without server |
| AsyncClient | Async testing with httpx |
| conftest.py | Shared fixtures hierarchy |
| Fixture Scope | function > class > module > session |
| pytest-asyncio | Enables async test functions |
| Parametrize | Same test, different inputs |
| Markers | Categorize and filter tests |
| Dependency Override | Replace real deps with mocks |
| Test Isolation | Transaction rollback per test |
| Best Practice | Arrange-Act-Assert pattern |
