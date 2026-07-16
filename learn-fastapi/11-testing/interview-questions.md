# Testing Interview Questions

## Table of Contents

1. [Basic Level (1-10)](#1-basic)
2. [Intermediate Level (11-20)](#2-intermediate)
3. [Advanced Level (21-30)](#3-advanced)
4. [Expert Level (31-40)](#4-expert)
5. [Scenario-Based Questions](#5-scenario)
6. [Code Review Questions](#6-code-review)

---

## 1. Basic Level (1-10) <a name="1-basic"></a>

### Q1: What is pytest and why use it with FastAPI?

**Answer:** pytest is a Python testing framework that provides fixtures,
parametrize, markers, and a rich plugin ecosystem. FastAPI is designed to be
testable, and pytest makes it easy with:

- Clean assertion syntax
- Fixtures for dependency injection
- Parameterized testing
- Rich plugin ecosystem (pytest-asyncio, pytest-cov, etc.)

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
```

### Q2: What is TestClient and how does it work?

**Answer:** TestClient (from Starlette) wraps httpx and sends HTTP requests to the
ASGI application without starting a real server. It handles ASGI lifespan events
automatically.

```python
from fastapi.testclient import TestClient
from app.main import app

# TestClient communicates directly with the ASGI app
client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
```

### Q3: What is conftest.py?

**Answer:** conftest.py is a pytest file that provides shared fixtures and hooks
to all test files in its directory and subdirectories. It's automatically loaded
by pytest.

```
tests/
├── conftest.py              # Shared across ALL tests
├── test_users.py
├── test_items.py
└── test_orders/
    ├── conftest.py          # Shared across order tests
    └── test_create.py
```

### Q4: What are fixtures in pytest?

**Answer:** Fixtures are functions decorated with `@pytest.fixture` that provide
test setup, execution, and teardown. They support dependency injection.

```python
import pytest

@pytest.fixture
def sample_user():
    return {"name": "Test User", "email": "test@test.com"}

def test_create_user(client, sample_user):
    response = client.post("/users/", json=sample_user)
    assert response.status_code == 201
```

### Q5: What is the difference between sync and async test clients?

**Answer:** Sync TestClient blocks during requests. Async client (httpx.AsyncClient
with ASGITransport) allows `await` for concurrent requests.

```python
# Sync
def test_sync(client):
    response = client.get("/")

# Async
async def test_async(client):
    response = await client.get("/")
```

### Q6: How do you run a specific test?

**Answer:**
```bash
# Run specific file
pytest tests/test_users.py

# Run specific function
pytest tests/test_users.py::test_create_user

# Run by keyword
pytest -k "create"

# Run by marker
pytest -m unit

# Verbose output
pytest -v
```

### Q7: What is the Arrange-Act-Assert pattern?

**Answer:** A test structure pattern:
- **Arrange**: Set up preconditions and test data
- **Act**: Execute the operation being tested
- **Assert**: Verify the expected outcome

```python
def test_create_item(client):
    # Arrange
    item_data = {"name": "Widget", "price": 29.99}

    # Act
    response = client.post("/items/", json=item_data)

    # Assert
    assert response.status_code == 201
    assert response.json()["name"] == "Widget"
```

### Q8: What is pytest.mark.parametrize?

**Answer:** It allows running the same test with different inputs, reducing
code duplication.

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("a" * 100, 100),
])
def test_string_length(input, expected):
    assert len(input) == expected
```

### Q9: How do you install testing dependencies?

**Answer:**
```bash
pip install pytest pytest-asyncio httpx coverage
pip install pytest-cov pytest-html factory-boy faker
```

### Q10: What is a test runner?

**Answer:** A test runner discovers, executes, and reports test results. pytest is
the most popular Python test runner, offering plugin support, fixtures, and
detailed reporting.

---

## 2. Intermediate Level (11-20) <a name="2-intermediate"></a>

### Q11: What are fixture scopes and when to use each?

**Answer:**

| Scope | Setup Frequency | Use Case |
|-------|----------------|----------|
| `function` | Each test | Fresh data per test |
| `class` | Each class | Shared across class methods |
| `module` | Each file | Expensive setup shared |
| `session` | Entire run | DB engine, seed data |

```python
@pytest.fixture(scope="session")
def db_engine():
    """Create engine once for all tests."""
    return create_engine("sqlite://")

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Fresh session per test."""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
```

### Q12: How do you test database operations in FastAPI?

**Answer:** Use dependency overrides with `app.dependency_overrides[get_db]` to
inject a test database session.

```python
from app.db import get_db

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
```

### Q13: What is dependency overriding?

**Answer:** `app.dependency_overrides[dep] = mock_dep` replaces a dependency for
all routes that use it. Essential for testing without real DB, auth, or external
services.

```python
from app.auth import get_current_user

def override_get_current_user():
    return {"id": 1, "name": "Test User"}

app.dependency_overrides[get_current_user] = override_get_current_user
```

### Q14: How do you test error cases?

**Answer:**
```python
def test_404_error(client):
    response = client.get("/items/99999")
    assert response.status_code == 404

def test_422_validation_error(client):
    response = client.post("/items/", json={"name": ""})
    assert response.status_code == 422

def test_401_unauthorized(client):
    response = client.get("/protected")
    assert response.status_code == 401
```

### Q15: How do you test file uploads?

**Answer:**
```python
def test_file_upload(client):
    files = {
        "file": ("test.txt", b"file content", "text/plain")
    }
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    assert response.json()["filename"] == "test.txt"
```

### Q16: What is pytest-asyncio and when to use it?

**Answer:** pytest-asyncio enables testing async functions. Use it when testing
async route handlers, async database operations, or async service functions.

```python
import pytest

@pytest.mark.asyncio
async def test_async_endpoint(client):
    response = await client.get("/async-endpoint")
    assert response.status_code == 200
```

### Q17: How do you test middleware?

**Answer:** Middleware runs automatically. Test by checking response headers,
status codes, or side effects.

```python
def test_cors_middleware(client):
    response = client.options(
        "/items/",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert "access-control-allow-origin" in response.headers

def test_rate_limiting(client):
    for _ in range(100):
        response = client.get("/api/data")
    assert response.status_code == 429
```

### Q18: How do you test authentication?

**Answer:**
```python
@pytest.fixture
def auth_headers():
    # In real app, generate a valid token
    token = create_test_token(user_id=1)
    return {"Authorization": f"Bearer {token}"}

def test_protected_endpoint(client, auth_headers):
    response = client.get("/protected", headers=auth_headers)
    assert response.status_code == 200

def test_unauthorized(client):
    response = client.get("/protected")
    assert response.status_code == 401
```

### Q19: How do you handle test database cleanup?

**Answer:**
```python
@pytest.fixture(autouse=True)
def clean_db(db_session):
    """Rollback after each test."""
    yield db_session
    db_session.rollback()

# Or truncate tables
@pytest.fixture(autouse=True)
def truncate_tables(engine):
    yield
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
```

### Q20: What are test markers?

**Answer:** Markers categorize tests for selective execution.

```python
@pytest.mark.slow
def test_large_dataset():
    pass

@pytest.mark.integration
def test_db_operation():
    pass

# Run: pytest -m "not slow"
# Run: pytest -m integration
```

---

## 3. Advanced Level (21-30) <a name="3-advanced"></a>

### Q21: How do you test WebSocket endpoints?

**Answer:**
```python
async def test_websocket(client):
    async with client.websocket_connect("/ws") as ws:
        await ws.send_text("Hello")
        data = await ws.receive_text()
        assert data == "Echo: Hello"
```

### Q22: How do you test background tasks?

**Answer:**
```python
from unittest.mock import AsyncMock, patch

def test_background_task(client, mocker):
    mock_task = mocker.patch("app.tasks.send_email")
    response = client.post("/send-notification", json={"to": "test@test.com"})
    assert response.status_code == 200
    # Background tasks execute after response in TestClient
    mock_task.assert_called_once()
```

### Q23: How do you test streaming responses?

**Answer:**
```python
async def test_streaming(client):
    async with client.stream("GET", "/stream") as response:
        chunks = []
        async for chunk in response.aiter_bytes():
            chunks.append(chunk)
        assert len(chunks) > 0
```

### Q24: How do you create test data factories?

**Answer:**
```python
import factory

class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Sequence(lambda n: f"User {n}")
    email = factory.Sequence(lambda n: f"user{n}@test.com")
    role = "user"

# Usage
def test_create_user(client):
    user = UserFactory.build()
    response = client.post("/users/", json={
        "name": user.name,
        "email": user.email,
    })
    assert response.status_code == 201
```

### Q25: How do you test external API calls?

**Answer:**
```python
import respx
import httpx

@respx.mock
async def test_external_api(client):
    respx.get("https://api.external.com/data").mock(
        return_value=httpx.Response(200, json={"result": "mocked"})
    )

    response = await client.get("/proxy/data")
    assert response.status_code == 200
    assert response.json()["result"] == "mocked"
```

### Q26: How do you test rate limiting?

**Answer:**
```python
def test_rate_limiting(client, mock_redis):
    mock_redis.incr.return_value = 101  # Over limit
    response = client.get("/api/data")
    assert response.status_code == 429

def test_rate_limiting_within_limit(client, mock_redis):
    mock_redis.incr.return_value = 50  # Under limit
    response = client.get("/api/data")
    assert response.status_code == 200
```

### Q27: What is contract testing?

**Answer:** Contract testing verifies that API providers and consumers agree on the
API interface. schemathesis auto-generates tests from OpenAPI spec.

```python
import schemathesis
from app.main import app

schema = schemathesis.from_asgi("/openapi.json", app=app)

@schema.parametrize()
def test_api_contract(case):
    response = case.call_asgi(app)
    case.validate_response(response)
```

### Q28: How do you test performance?

**Answer:**
```python
import time

def test_response_time(client):
    start = time.perf_counter()
    response = client.get("/items/")
    elapsed = time.perf_counter() - start
    assert response.status_code == 200
    assert elapsed < 1.0  # Under 1 second

# Or use pytest-benchmark
def test_benchmark_create(benchmark, client):
    benchmark(lambda: client.post("/items/", json={"name": "Test", "price": 10}))
```

### Q29: How do you test multiple authentication levels?

**Answer:**
```python
@pytest.fixture
def regular_user():
    return {"Authorization": "Bearer regular-token"}

@pytest.fixture
def admin_user():
    return {"Authorization": "Bearer admin-token"}

def test_regular_user_cannot_access_admin(client, regular_user):
    response = client.get("/admin/dashboard", headers=regular_user)
    assert response.status_code == 403

def test_admin_can_access_admin(client, admin_user):
    response = client.get("/admin/dashboard", headers=admin_user)
    assert response.status_code == 200
```

### Q30: How do you structure tests for a large project?

**Answer:**
```
tests/
├── conftest.py              # Root-level fixtures
├── unit/
│   ├── conftest.py          # Unit test fixtures
│   ├── test_validators.py
│   └── test_utils.py
├── integration/
│   ├── conftest.py          # Integration fixtures (real DB)
│   ├── test_user_routes.py
│   └── test_order_flows.py
├── e2e/
│   └── test_complete_flows.py
└── fixtures/
    ├── factories.py
    └── seed_data.py
```

---

## 4. Expert Level (31-40) <a name="4-expert"></a>

### Q31: How do you test concurrent operations?

**Answer:**
```python
import asyncio

async def test_concurrent_creates(client):
    tasks = [
        client.post("/items/", json={"name": f"Item {i}", "price": 10.0})
        for i in range(10)
    ]
    responses = await asyncio.gather(*tasks)
    assert all(r.status_code == 201 for r in responses)
```

### Q32: How do you test event-driven architectures?

**Answer:**
```python
async def test_event_publishing(client, mock_event_bus):
    response = client.post("/orders/", json={...})
    assert response.status_code == 201

    # Verify event was published
    mock_event_bus.publish.assert_called_once_with(
        "order.created",
        {"order_id": response.json()["order_id"]}
    )
```

### Q33: How do you implement snapshot testing?

**Answer:**
```python
# Using syrupy
def test_api_response_snapshot(client, snapshot):
    response = client.get("/items/")
    assert response.json() == snapshot

# Update snapshots: pytest --snapshot-update
```

### Q34: How do you test GraphQL APIs?

**Answer:**
```python
def test_graphql_query(client):
    query = """
    query {
        users {
            id
            name
            email
        }
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert "data" in response.json()
    assert len(response.json()["data"]["users"]) > 0
```

### Q35: How do you test microservices communication?

**Answer:**
```python
# Mock the other service
@pytest.fixture
def mock_user_service(mocker):
    return mocker.patch(
        "app.services.user_client.UserClient.get_user",
        return_value={"id": 1, "name": "Test User"}
    )

def test_order_with_user_lookup(client, mock_user_service):
    response = client.post("/orders/", json={"user_id": 1, "item_id": 1})
    assert response.status_code == 201
    mock_user_service.assert_called_once_with(user_id=1)
```

### Q36: How do you test idempotency?

**Answer:**
```python
def test_create_order_idempotent(client):
    payload = {"user_id": 1, "item_id": 1, "idempotency_key": "key-123"}

    # First request
    response1 = client.post("/orders/", json=payload)
    assert response1.status_code == 201

    # Same request with same key
    response2 = client.post("/orders/", json=payload)
    assert response2.status_code == 200  # Returns existing order
    assert response1.json()["order_id"] == response2.json()["order_id"]
```

### Q37: How do you test error recovery?

**Answer:**
```python
def test_retry_on_failure(client, mock_external_service):
    # First call fails, second succeeds
    mock_external_service.side_effect = [
        ConnectionError("Timeout"),
        {"status": "success"},
    ]

    response = client.post("/retry-endpoint")
    assert response.status_code == 200
    assert mock_external_service.call_count == 2
```

### Q38: How do you test multi-tenant applications?

**Answer:**
```python
@pytest.fixture
def tenant_a_client(client):
    client.headers["X-Tenant-ID"] = "tenant_a"
    return client

@pytest.fixture
def tenant_b_client(client):
    client.headers["X-Tenant-ID"] = "tenant_b"
    return client

def test_tenant_isolation(tenant_a_client, tenant_b_client):
    # Create in tenant A
    response = tenant_a_client.post("/items/", json={"name": "A's Item"})
    assert response.status_code == 201

    # Tenant B can't see it
    response = tenant_b_client.get("/items/")
    assert all(item["name"] != "A's Item" for item in response.json())
```

### Q39: How do you test database migrations?

**Answer:**
```python
def test_migration_applies_cleanly():
    from alembic import command
    from alembic.config import Config

    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", "sqlite:///test_migrate.db")

    command.upgrade(config, "head")

    engine = create_engine("sqlite:///test_migrate.db")
    inspector = inspect(engine)
    assert "users" in inspector.get_table_names()

    command.downgrade(config, "base")
    assert len(inspector.get_table_names()) == 0
    os.remove("test_migrate.db")
```

### Q40: How do you achieve 100% test coverage?

**Answer:**
```bash
# Run with coverage
pytest --cov=app --cov-report=html --cov-fail-under=100

# Check what's not covered
pytest --cov=app --cov-report=term-missing
```

Key strategies:
- Test all branches (if/else)
- Test exception handlers
- Test middleware
- Test event handlers
- Test utility functions
- Mock external services
- Test edge cases (empty, null, boundary values)

---

## 5. Scenario-Based Questions <a name="5-scenario"></a>

### Scenario 1: "The API is slow in production"

**Answer:**
1. Add response time monitoring
2. Profile slow endpoints with `pytest --durations=10`
3. Add database query logging
4. Check connection pool configuration
5. Implement caching for frequent queries
6. Add async for I/O-bound operations

### Scenario 2: "Tests are flaky in CI"

**Answer:**
1. Identify flaky tests with `pytest --reruns 0`
2. Check for shared state between tests
3. Ensure proper database cleanup
4. Mock external services
5. Add proper waits for async operations
6. Use unique test data (UUIDs)

### Scenario 3: "Need to test payment integration"

**Answer:**
```python
@pytest.fixture
def mock_stripe(mocker):
    return mocker.patch("app.services.stripe")

def test_payment_success(client, mock_stripe):
    mock_stripe.Charge.create.return_value = MagicMock(
        id="ch_123", status="succeeded"
    )
    response = client.post("/pay", json={"amount": 100, "token": "tok_test"})
    assert response.status_code == 200
    assert response.json()["charge_id"] == "ch_123"

def test_payment_failure(client, mock_stripe):
    mock_stripe.Charge.create.side_effect = stripe.error.CardError(
        "Card declined", param="card"
    )
    response = client.post("/pay", json={"amount": 100, "token": "tok_rejected"})
    assert response.status_code == 402
```

### Scenario 4: "Need to test real-time features"

**Answer:**
```python
async def test_notification_websocket(client):
    async with client.websocket_connect("/ws/notifications") as ws:
        # Trigger notification
        await client.post("/notify", json={"message": "Hello"})

        # Receive via WebSocket
        data = await ws.receive_json()
        assert data["message"] == "Hello"
```

---

## 6. Code Review Questions <a name="6-code-review"></a>

### Q: What's wrong with this test?

```python
def test_get_item(client):
    response = client.get("/items/1")
    assert response.status_code == 200
```

**Answer:** The test assumes item 1 exists. It should create the item first or mock
the database. This test will fail if the database is empty.

### Q: Improve this test

```python
def test_create_user(client):
    client.post("/users/", json={"name": "Test", "email": "test@test.com"})
    response = client.get("/users/1")
    assert response.json()["name"] == "Test"
```

**Answer:**
```python
def test_create_and_fetch_user(client):
    # Create
    create_response = client.post("/users/", json={
        "name": "Test",
        "email": "test@test.com",
    })
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    # Fetch
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test"
```

### Q: Why is this bad?

```python
@pytest.fixture
def data():
    return {"name": "Test"}  # Module scope but mutable

def test_a(data):
    data["name"] = "Changed"

def test_b(data):
    assert data["name"] == "Changed"  # Relies on test_a running first!
```

**Answer:** Tests should be independent. test_b relies on test_a modifying the
shared data. Each test should set up its own state. Use function-scoped fixtures
or create new data in each test.

---

## Quick Reference: Common Test Patterns

```python
# Test CRUD operations
def test_crud(client):
    # Create
    r = client.post("/items/", json={...})
    assert r.status_code == 201
    id = r.json()["id"]

    # Read
    r = client.get(f"/items/{id}")
    assert r.status_code == 200

    # Update
    r = client.put(f"/items/{id}", json={...})
    assert r.status_code == 200

    # Delete
    r = client.delete(f"/items/{id}")
    assert r.status_code == 204

# Test authentication
def test_auth_required(client):
    response = client.get("/protected")
    assert response.status_code == 401

# Test validation
def test_validation(client):
    response = client.post("/items/", json={"price": -1})
    assert response.status_code == 422

# Test dependency override
def test_with_mock_db(client, mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    response = client.get("/items/")
    assert response.status_code == 200
```
