# Mocking in FastAPI Tests

## Table of Contents

1. [Introduction to Mocking](#1-introduction)
2. [unittest.mock Basics](#2-unittest-mock)
3. [pytest-mock Plugin](#3-pytest-mock)
4. [Mocking FastAPI Dependencies](#4-dependency-overrides)
5. [Mocking Database](#5-mocking-database)
6. [Mocking External Services](#6-external-services)
7. [Mocking Background Tasks](#7-background-tasks)
8. [Mocking Redis](#8-mocking-redis)
9. [Fixture-Based Mocking](#9-fixture-based)
10. [Mocking Async Functions](#10-async-mocking)
11. [Mocking Strategies](#11-strategies)
12. [Common Pitfalls](#12-pitfalls)
13. [Best Practices](#13-best-practices)

---

## 1. Introduction to Mocking <a name="1-introduction"></a>

Mocking replaces real objects with simulated ones during testing. In FastAPI, mocking
is essential for:

- **Isolating units**: Test a function without its dependencies
- **Speed**: Avoid slow operations (DB, network, file I/O)
- **Determinism**: Remove randomness and external state
- **Cost**: Don't call paid APIs during tests
- **Availability**: Test when external services are down

### What to Mock

| Component | When to Mock |
|-----------|-------------|
| Database | Unit tests, fast tests |
| External APIs | Always (cost, reliability) |
| File system | When testing logic, not I/O |
| Time/datetime | Testing time-dependent logic |
| Authentication | When testing non-auth logic |
| Background tasks | Unit tests (verify they're called) |
| Cache (Redis) | Unit tests |

### What NOT to Mock

- The code you're testing (obviously)
- Simple data structures
- Fast, deterministic operations
- The test framework itself

---

## 2. unittest.mock Basics <a name="2-unittest-mock"></a>

### Mock Objects

```python
from unittest.mock import Mock, MagicMock, AsyncMock, patch, call

# Basic Mock
mock_obj = Mock()
mock_obj.some_method.return_value = 42
assert mock_obj.some_method() == 42

# MagicMock (supports magic methods like __len__, __iter__)
mock_list = MagicMock()
mock_list.__len__.return_value = 5
assert len(mock_list) == 5

# Verify calls
mock_obj.some_method("arg1", key="value")
mock_obj.some_method.assert_called_once_with("arg1", key="value")
mock_obj.some_method.assert_called()

# Call count
assert mock_obj.some_method.call_count == 1
```

### Patching

```python
from unittest.mock import patch

# Decorator form
with patch("app.services.get_current_time") as mock_time:
    mock_time.return_value = datetime(2024, 1, 1, 12, 0, 0)
    result = get_user_greeting()
    assert "2024" in result

# Context manager form
mock_obj = Mock()
with patch("app.module.target", mock_obj):
    result = function_that_uses_target()
    mock_obj.assert_called_once()

# patch.object for patching specific attributes
from app import services

with patch.object(services, 'external_api_call') as mock_api:
    mock_api.return_value = {"status": "ok"}
    result = services.process_data()
```

### Mock Return Values and Side Effects

```python
from unittest.mock import Mock

# Return value
mock = Mock()
mock.fetch_data.return_value = {"key": "value"}

# Side effect (function called instead of returning)
def custom_side_effect(*args, **kwargs):
    if args[0] == "error":
        raise ValueError("Invalid input")
    return {"result": args[0]}

mock.process.side_effect = custom_side_effect
assert mock.process("valid") == {"result": "valid"}
assert mock.process("error")  # Would raise ValueError

# Side effect as list (returns values in sequence)
mock.next_item.side_effect = [1, 2, 3, StopIteration]
assert mock.next_item() == 1
assert mock.next_item() == 2
assert mock.next_item() == 3

# raise an exception
mock.fail.side_effect = ConnectionError("Network error")
```

### Assertions on Mocks

```python
from unittest.mock import Mock, call

mock = Mock()

# Was it called?
mock.some_method()
mock.some_method.assert_called()

# How many times?
assert mock.some_method.call_count == 1

# With what arguments?
mock.some_method("a", "b")
mock.some_method.assert_called_with("a", "b")
mock.some_method.assert_called_once_with("a", "b")

# With keyword arguments?
mock.db.execute(query="SELECT *", params={})
mock.db.execute.assert_called_once_with(query="SELECT *", params={})

# Check call order
mock.first()
mock.second()
mock.first.assert_called_before(mock.second)

# List of all calls
assert mock.method.call_args_list == [
    call("a"),
    call("b"),
    call("c"),
]
```

---

## 3. pytest-mock Plugin <a name="3-pytest-mock"></a>

pytest-mock wraps unittest.mock in a pytest fixture (`mocker`), providing a cleaner API.

### Installation

```bash
pip install pytest-mock
```

### Basic Usage

```python
def test_with_mocker(mocker):
    # mocker.patch replaces unittest.mock.patch
    mock_func = mocker.patch("app.services.get_data")
    mock_func.return_value = {"data": "test"}

    result = app.services.process_data()
    assert result == {"data": "test"}
    mock_func.assert_called_once()

def test_mocker_spy(mocker):
    # mocker.spy wraps a real function to track calls
    spy = mocker.spy(app.services, "calculate_total")
    result = app.services.calculate_total([1, 2, 3])

    assert result == 6  # Real function still executes
    spy.assert_called_once_with([1, 2, 3])
```

### mocker Features

```python
def test_mocker_features(mocker):
    # Simple patch
    mock = mocker.patch("app.services.external_api")

    # Patch with attribute
    mock = mocker.patch("app.services.external_api")
    mock.return_value = {"status": "ok"}

    # Side effect
    mock.side_effect = [1, 2, 3]

    # Auto-cleanup (automatic at end of test)
    # No need for context managers or decorators

    # mocker.stop (manual stop)
    handle = mocker.patch("app.services.api")
    # ... test code ...
    mocker.stop(handle)
```

---

## 4. Mocking FastAPI Dependencies <a name="4-dependency-overrides"></a>

FastAPI's `app.dependency_overrides` is the primary way to mock dependencies in tests.

### Basic Dependency Override

```python
# app/dependencies.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# app/routes/users.py
@router.get("/users/me")
async def read_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return current_user

# tests/test_users.py
from app.main import app
from app.dependencies import get_db, get_current_user

def test_read_current_user(client, mock_user):
    # Override the dependency
    async def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["name"] == mock_user.name

    # Clean up
    app.dependency_overrides.clear()
```

### Multiple Dependency Overrides

```python
@pytest.fixture
def mock_dependencies(mock_db_session, mock_user):
    """Set up all dependency overrides for route testing."""

    async def override_get_db():
        yield mock_db_session

    async def override_get_current_user():
        return mock_user

    async def override_get_admin_user():
        return {**mock_user, "role": "admin"}

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    yield

    app.dependency_overrides.clear()

def test_with_overrides(client, mock_dependencies):
    response = client.get("/users/me")
    assert response.status_code == 200
```

### Testing with Multiple Auth Levels

```python
@pytest.fixture
def regular_user_override():
    app.dependency_overrides[get_current_user] = lambda: {
        "id": 1, "name": "Regular User", "role": "user"
    }
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def admin_user_override():
    app.dependency_overrides[get_current_user] = lambda: {
        "id": 1, "name": "Admin User", "role": "admin"
    }
    yield
    app.dependency_overrides.clear()

def test_regular_user_cannot_access_admin(client, regular_user_override):
    response = client.get("/admin/dashboard")
    assert response.status_code == 403

def test_admin_can_access_admin(client, admin_user_override):
    response = client.get("/admin/dashboard")
    assert response.status_code == 200
```

### Override with Mock Objects

```python
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_auth_service(mocker):
    mock_service = AsyncMock()
    mock_service.verify_token.return_value = {"id": 1, "name": "Test User"}
    mock_service.create_token.return_value = "test-token-123"

    app.dependency_overrides[AuthService] = lambda: mock_service
    yield mock_service
    app.dependency_overrides.clear()

def test_login(client, mock_auth_service):
    response = client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "secret",
    })
    assert response.status_code == 200
    assert response.json()["token"] == "test-token-123"
    mock_auth_service.verify_token.assert_called_once()
```

---

## 5. Mocking Database <a name="5-mocking-database"></a>

### Mock SQLAlchemy Session

```python
from unittest.mock import MagicMock, AsyncMock, patch
import pytest

@pytest.fixture
def mock_db_session():
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    session.delete = AsyncMock()
    session.close = AsyncMock()
    session.flush = AsyncMock()
    return session

@pytest.fixture
def mock_user_query(mock_db_session):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = User(
        id=1, name="Test User", email="test@test.com"
    )
    mock_db_session.execute.return_value = mock_result
    return mock_db_session

def test_get_user(mock_user_query):
    from app.services.user_service import get_user

    user = get_user(mock_user_query, user_id=1)
    assert user.name == "Test User"
    mock_user_query.execute.assert_called_once()
```

### Mock Query Results

```python
from unittest.mock import MagicMock
from sqlalchemy import Result

@pytest.fixture
def mock_query_results():
    """Create mock query results."""
    def create_results(items):
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = items
        mock_scalars.first.return_value = items[0] if items else None
        mock_scalars.one.return_value = items[0] if len(items) == 1 else None
        mock_scalars.one_or_none.return_value = items[0] if items else None
        mock_result.scalars.return_value = mock_scalars
        return mock_result
    return create_results

def test_list_users(mock_db_session, mock_query_results):
    users = [
        User(id=1, name="Alice"),
        User(id=2, name="Bob"),
    ]
    mock_db_session.execute.return_value = mock_query_results(users)

    from app.services.user_service import list_users
    result = list_users(mock_db_session)
    assert len(result) == 2
```

### Mock with pytest-mock

```python
def test_create_user(mocker, mock_db_session):
    from app.services import user_service

    # Mock the service function
    mock_create = mocker.patch.object(
        user_service,
        "create_user_in_db",
        new_callable=AsyncMock,
    )
    mock_create.return_value = User(id=1, name="New User")

    # Mock the route's dependency
    app.dependency_overrides[get_db] = lambda: mock_db_session

    response = client.post("/users/", json={"name": "New User"})
    assert response.status_code == 201
    mock_create.assert_called_once()
```

### Mock Database Transactions

```python
@pytest.fixture
def mock_db_with_transaction():
    session = AsyncMock()

    # Mock transaction context
    transaction = AsyncMock()
    session.begin.return_value.__aenter__ = AsyncMock(return_value=transaction)
    session.begin.return_value.__aexit__ = AsyncMock(return_value=None)

    return session

def test_transaction_rollback(mock_db_with_transaction, mocker):
    session = mock_db_with_transaction

    # Make commit raise an exception
    session.commit.side_effect = Exception("DB error")

    from app.services.user_service import create_user
    with pytest.raises(Exception):
        await create_user(session, name="Test")

    # Verify rollback was attempted
    session.rollback.assert_called()
```

---

## 6. Mocking External Services <a name="6-external-services"></a>

### Mock HTTP Calls with respx

```python
import respx
import httpx
import pytest

@pytest.fixture
def mock_external_api():
    with respx.mock:
        # Mock specific endpoints
        respx.get("https://api.stripe.com/v1/customers").mock(
            return_value=httpx.Response(200, json={"id": "cus_123"})
        )
        respx.post("https://api.stripe.com/v1/charges").mock(
            return_value=httpx.Response(200, json={"id": "ch_456"})
        )
        yield

async def test_payment_processing(client, mock_external_api):
    response = await client.post("/pay", json={
        "amount": 100,
        "currency": "usd",
    })
    assert response.status_code == 200
    assert response.json()["charge_id"] == "ch_456"
```

### Mock External API with Response Logic

```python
import respx
import httpx

@respx.mock
async def test_external_api_error_handling(client):
    # Mock a 500 error from external service
    respx.get("https://api.external.com/data").mock(
        return_value=httpx.Response(500, json={"error": "Internal error"})
    )

    response = await client.get("/proxy/data")
    assert response.status_code == 502
    assert "upstream" in response.json()["detail"].lower()

@respx.mock
async def test_external_api_timeout(client):
    respx.get("https://api.slow.com/data").mock(
        side_effect=httpx.ReadTimeout("Read timeout")
    )

    response = await client.get("/proxy/data")
    assert response.status_code == 504

@respx.mock
async def test_external_api_rate_limit(client):
    # First call succeeds
    respx.get("https://api.rate-limited.com/data").mock(
        side_effect=[
            httpx.Response(200, json={"data": "ok"}),
            httpx.Response(429, json={"error": "rate limited"}),
        ]
    )

    response1 = await client.get("/proxy/data")
    assert response1.status_code == 200

    response2 = await client.get("/proxy/data")
    assert response2.status_code == 429
```

### Mock Third-Party SDKs

```python
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.fixture
def mock_stripe():
    with patch("app.services.stripe.Charge") as mock_charge:
        mock_charge.create.return_value = MagicMock(
            id="ch_test123",
            status="succeeded",
        )
        yield mock_charge

def test_stripe_payment(client, mock_stripe):
    response = client.post("/pay", json={"amount": 100})
    assert response.status_code == 200
    mock_charge.create.assert_called_once_with(
        amount=10000,
        currency="usd",
        source="tok_visa",
    )

@pytest.fixture
def mock_sendgrid():
    with patch("app.services.sg.send") as mock_send:
        mock_send.return_value = MagicMock(status_code=202)
        yield mock_send

def test_send_email(client, mock_sendgrid):
    response = client.post("/notify", json={
        "to": "user@test.com",
        "subject": "Hello",
    })
    assert response.status_code == 200
    mock_sendgrid.assert_called_once()
```

### Mock File System Operations

```python
from unittest.mock import mock_open, patch

def test_read_config():
    mock_data = '{"database": "test_db"}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        config = read_config_file("config.json")
        assert config["database"] == "test_db"

def test_file_upload_processing(client):
    with patch("builtins.open", mock_open()) as mocked_file:
        response = client.post(
            "/upload",
            files={"file": ("test.txt", b"content", "text/plain")},
        )
        assert response.status_code == 200
        mocked_file().write.assert_called_once_with(b"content")
```

---

## 7. Mocking Background Tasks <a name="7-background-tasks"></a>

### Mock Background Task Calls

```python
from unittest.mock import AsyncMock, patch
from fastapi import BackgroundTasks

@pytest.fixture
def mock_background_tasks(mocker):
    mock_tasks = AsyncMock(spec=BackgroundTasks)
    return mock_tasks

def test_create_user_sends_email(client, mock_background_tasks, mocker):
    mock_send_email = mocker.patch("app.tasks.send_welcome_email")

    response = client.post("/users/", json={
        "name": "Test User",
        "email": "test@test.com",
    })
    assert response.status_code == 201

    # Verify background task was added
    # Note: In FastAPI, background tasks are added during the request
    # and executed after the response is sent
```

### Direct Background Task Mocking

```python
from unittest.mock import AsyncMock, patch

async def test_send_notification(client):
    with patch("app.tasks.send_notification") as mock_notify:
        mock_notify.return_value = None

        response = client.post("/orders/", json={
            "product_id": 1,
            "quantity": 2,
        })
        assert response.status_code == 201

        # Background task runs after response
        # In tests, we need to verify it was queued
        # The exact approach depends on your FastAPI version
```

### Mock BackgroundTask in Routes

```python
# app/routes/orders.py
from fastapi import BackgroundTasks

@router.post("/orders/")
async def create_order(
    order: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    order = create_order_in_db(db, order)
    background_tasks.add_task(send_order_confirmation, order.id)
    background_tasks.add_task(update_inventory, order.id)
    return {"order_id": order.id}

# tests/test_orders.py
from unittest.mock import AsyncMock, MagicMock

def test_create_order_queues_background_tasks(client, mocker):
    mock_send_confirmation = mocker.patch("app.routes.orders.send_order_confirmation")
    mock_update_inventory = mocker.patch("app.routes.orders.update_inventory")

    response = client.post("/orders/", json={
        "product_id": 1,
        "quantity": 2,
    })
    assert response.status_code == 201

    # Background tasks are executed synchronously in TestClient
    # So we can verify they were called
    mock_send_confirmation.assert_called_once()
    mock_update_inventory.assert_called_once()
```

---

## 8. Mocking Redis <a name="8-mocking-redis"></a>

### Mock Redis Client

```python
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

@pytest.fixture
def mock_redis():
    mock = AsyncMock()
    mock.get.return_value = None
    mock.set.return_value = True
    mock.delete.return_value = 1
    mock.exists.return_value = False
    mock.expire.return_value = True
    mock.keys.return_value = []
    mock.hget.return_value = None
    mock.hset.return_value = 1
    mock.hgetall.return_value = {}
    return mock

async def test_cache_miss(client, mock_redis):
    mock_redis.get.return_value = None  # Cache miss

    with patch("app.services.redis_client", mock_redis):
        response = await client.get("/items/1")
        assert response.status_code == 200
        mock_redis.get.assert_called_with("item:1")
        mock_redis.set.assert_called()  # Should set cache

async def test_cache_hit(client, mock_redis):
    import json
    cached_data = json.dumps({"id": 1, "name": "Cached Item"})
    mock_redis.get.return_value = cached_data  # Cache hit

    with patch("app.services.redis_client", mock_redis):
        response = await client.get("/items/1")
        assert response.status_code == 200
        assert response.json()["name"] == "Cached Item"
        mock_redis.set.assert_not_called()  # Should not set cache
```

### Mock Redis for Rate Limiting

```python
async def test_rate_limiting(client, mock_redis):
    # Simulate rate limit exceeded
    mock_redis.incr.return_value = 101  # Over limit
    mock_redis.ttl.return_value = 60

    with patch("app.middleware.redis_client", mock_redis):
        response = await client.get("/api/data")
        assert response.status_code == 429
        assert "rate limit" in response.json()["detail"].lower()

async def test_rate_limiting_within_limit(client, mock_redis):
    mock_redis.incr.return_value = 50  # Under limit
    mock_redis.ttl.return_value = 60

    with patch("app.middleware.redis_client", mock_redis):
        response = await client.get("/api/data")
        assert response.status_code == 200
```

### Mock Redis for Sessions

```python
import json

async def test_session_management(client, mock_redis):
    session_data = json.dumps({
        "user_id": 1,
        "role": "admin",
        "exp": 1234567890,
    })
    mock_redis.get.return_value = session_data

    with patch("app.services.session_store", mock_redis):
        response = await client.get(
            "/profile/",
            headers={"Authorization": "Bearer session-token"},
        )
        assert response.status_code == 200
        mock_redis.get.assert_called_with("session:session-token")
```

---

## 9. Fixture-Based Mocking <a name="9-fixture-based"></a>

### Composable Mock Fixtures

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_db():
    return AsyncMock()

@pytest.fixture
def mock_cache():
    return AsyncMock()

@pytest.fixture
def mock_email_service():
    return AsyncMock()

@pytest.fixture
def mock_payment_service():
    service = AsyncMock()
    service.charge.return_value = MagicMock(
        id="ch_123", status="succeeded"
    )
    return service

@pytest.fixture
def all_mocks(mock_db, mock_cache, mock_email_service, mock_payment_service):
    """Bundle all mocks for comprehensive mocking."""
    return {
        "db": mock_db,
        "cache": mock_cache,
        "email": mock_email_service,
        "payment": mock_payment_service,
    }
```

### Override Dependencies with Fixtures

```python
@pytest.fixture(autouse=True)
def mock_all_dependencies(mock_db, mock_redis, mock_email):
    """Auto-override all external dependencies."""
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_redis] = lambda: mock_redis
    app.dependency_overrides[get_email_service] = lambda: mock_email

    yield

    app.dependency_overrides.clear()

def test_order_flow(client):
    # All external dependencies are mocked
    response = client.post("/orders/", json={"product_id": 1})
    assert response.status_code == 201
```

### Scoped Mock Fixtures

```python
# Function-scoped: Fresh mock for each test
@pytest.fixture
def fresh_mock_db():
    return AsyncMock()

# Module-scoped: Same mock for all tests in module
@pytest.fixture(scope="module")
def shared_mock_db():
    return AsyncMock()

# Session-scoped: Same mock for entire session
@pytest.fixture(scope="session")
def session_mock_redis():
    return AsyncMock()

# Class-scoped: Same mock for all tests in class
@pytest.fixture(scope="class")
def class_mock_email():
    return AsyncMock()
```

### Fixture with Configuration

```python
@pytest.fixture
def mock_db_with_data():
    """Mock database pre-loaded with test data."""
    mock = AsyncMock()

    users = [
        User(id=1, name="Alice", role="admin"),
        User(id=2, name="Bob", role="user"),
        User(id=3, name="Charlie", role="moderator"),
    ]

    items = [
        Item(id=1, name="Laptop", price=999.99, owner_id=1),
        Item(id=2, name="Phone", price=699.99, owner_id=2),
    ]

    def mock_execute(query):
        result = MagicMock()
        if "users" in str(query):
            result.scalars.return_value.all.return_value = users
        elif "items" in str(query):
            result.scalars.return_value.all.return_value = items
        return result

    mock.execute.side_effect = mock_execute
    return mock
```

---

## 10. Mocking Async Functions <a name="10-async-mocking"></a>

### AsyncMock Basics

```python
from unittest.mock import AsyncMock

# AsyncMock for async functions
async def async_function():
    return "real result"

mock = AsyncMock(return_value="mocked result")
result = await mock()
assert result == "mocked result"

# AsyncMock with side effect
mock = AsyncMock(side_effect=ValueError("Bad value"))
with pytest.raises(ValueError, match="Bad value"):
    await mock()
```

### Patching Async Functions

```python
from unittest.mock import AsyncMock, patch
import pytest

async def test_async_patch():
    with patch("app.services.fetch_external_data", new_callable=AsyncMock) as mock:
        mock.return_value = {"data": "test"}
        result = await app.services.process_external_data()
        assert result == {"data": "test"}

async def test_async_with_mocker(mocker):
    mock = mocker.patch(
        "app.services.fetch_external_data",
        new_callable=AsyncMock,
    )
    mock.return_value = {"data": "test"}
    result = await app.services.process_external_data()
    assert result == {"data": "test"}
```

### Async Mock with pytest-asyncio

```python
import pytest
from unittest.mock import AsyncMock

@pytest_asyncio.fixture
async def async_mock_service():
    mock = AsyncMock()
    mock.fetch.return_value = {"id": 1, "name": "Test"}
    mock.save.return_value = True
    return mock

async def test_with_async_fixture(async_mock_service):
    result = await async_mock_service.fetch()
    assert result["name"] == "Test"
    async_mock_service.save.assert_not_called()
```

### Mock Async Context Manager

```python
from unittest.mock import AsyncMock, MagicMock

# Mock async context manager (e.g., database session)
mock_session = AsyncMock()
mock_session.__aenter__ = AsyncMock(return_value=mock_session)
mock_session.__aexit__ = AsyncMock(return_value=None)

with patch("app.db.get_async_session") as mock_get_session:
    mock_get_session.return_value = mock_session
    async with get_async_session() as session:
        result = await session.execute(query)
```

---

## 11. Mocking Strategies <a name="11-strategies"></a>

### Strategy 1: Dependency Override (FastAPI-Specific)

```python
# Best for: Database, auth, service classes
app.dependency_overrides[MyDependency] = lambda: mock_instance
```

### Strategy 2: unittest.mock.patch

```python
# Best for: External APIs, utility functions, global state
with patch("module.function") as mock:
    mock.return_value = "value"
```

### Strategy 3: Respx for HTTP

```python
# Best for: Testing code that makes HTTP requests
@respx.mock
async def test():
    respx.get("https://api.com/data").mock(return_value=httpx.Response(200))
```

### Strategy 4: Fake Implementation

```python
# Best for: When you want a simple in-memory replacement
class FakeDatabase:
    def __init__(self):
        self.users = {}

    async def get_user(self, user_id: int):
        return self.users.get(user_id)

    async def create_user(self, user):
        self.users[user.id] = user

@pytest.fixture
def fake_db():
    return FakeDatabase()
```

### Strategy 5: Factory Functions

```python
# Best for: Creating test data with defaults
def make_user(**kwargs):
    defaults = {
        "id": 1,
        "name": "Test User",
        "email": "test@test.com",
        "role": "user",
    }
    defaults.update(kwargs)
    return User(**defaults)

@pytest.fixture
def user_factory():
    return make_user

def test_admin_user(client, user_factory):
    admin = user_factory(role="admin", name="Admin")
    # Use admin in test
```

---

## 12. Common Pitfalls <a name="12-pitfalls"></a>

### Pitfall 1: Mocking the Wrong Target

```python
# WRONG: Mocking where it's used instead of where it's defined
with patch("app.routes.users.get_db"):  # routes/users.py imports get_db
    pass

# CORRECT: Mock where it's defined
with patch("app.db.get_db"):
    pass

# BETTER: Use dependency override
app.dependency_overrides[get_db] = mock_db
```

### Pitfall 2: Not Cleaning Up Mocks

```python
# WRONG: Manual cleanup can be forgotten
def test_something():
    app.dependency_overrides[get_db] = mock_db
    # ... test code ...
    # If test fails, cleanup doesn't happen!

# CORRECT: Use fixture with cleanup
@pytest.fixture
def mock_db_override(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    yield
    app.dependency_overrides.clear()
```

### Pitfall 3: Mocking Built-in Functions

```python
# WRONG: Patching builtins
with patch("builtins.open"):
    pass

# CORRECT: Patch the module that uses open
with patch("app.services.open", mock_open(read_data="data")):
    pass
```

### Pitfall 4: AsyncMock Configuration

```python
# WRONG: Using MagicMock for async functions
from unittest.mock import MagicMock
mock = MagicMock()
mock.async_func.return_value = "value"
result = await mock.async_func()  # This fails!

# CORRECT: Use AsyncMock
from unittest.mock import AsyncMock
mock = AsyncMock()
mock.async_func.return_value = "value"
result = await mock.async_func()  # Works!
```

### Pitfall 5: Testing Implementation Instead of Behavior

```python
# WRONG: Testing implementation details
def test_get_user_calls_database(client, mock_db):
    client.get("/users/1")
    mock_db.execute.assert_called_once_with(ANY)  # Tests HOW

# CORRECT: Testing behavior
def test_get_user_returns_correct_data(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"  # Tests WHAT
```

---

## 13. Best Practices <a name="13-best-practices"></a>

### 1. Mock Closest to the Boundary

```python
# Mock at the boundary of your system (DB, network, file system)
# Not in the middle of your business logic

# WRONG
def test_calculate_total(mocker):
    mocker.patch("app.models.Item.price", 10)  # Mocking model attribute

# CORRECT
def test_calculate_total():
    item = Item(name="Test", price=10)
    assert calculate_total(item) == 10  # Test the function directly
```

### 2. Use Dependency Overrides Over Patching

```python
# PREFER: Dependency override
app.dependency_overrides[get_db] = lambda: mock_session

# AVOID: Patching (harder to maintain)
with patch("app.db.SessionLocal") as mock:
    mock.return_value = mock_session
```

### 3. Keep Mocks Simple

```python
# WRONG: Over-specifying mocks
mock = MagicMock()
mock.method.return_value.__iter__ = MagicMock(return_value=iter([1, 2, 3]))

# CORRECT: Simple mock setup
mock = MagicMock()
mock.method.return_value = [1, 2, 3]
```

### 4. Verify Critical Interactions

```python
def test_order_sends_confirmation_email(client, mock_email):
    response = client.post("/orders/", json={"product_id": 1})
    assert response.status_code == 201

    # Verify critical interaction happened
    mock_email.send.assert_called_once()
    call_args = mock_email.send.call_args
    assert "order confirmation" in call_args.kwargs["subject"].lower()
```

### 5. Use pytest-mock for Cleaner Code

```python
# CLEANER: Using mocker fixture
def test_with_mocker(mocker):
    mock = mocker.patch("app.services.api")
    mock.return_value = {"data": "test"}
    # Auto-cleanup at end of test

# VERbose: Using context manager
def test_with_context():
    with patch("app.services.api") as mock:
        mock.return_value = {"data": "test"}
        # Must remember to clean up
```

---

## Summary

| Mocking Approach | Best For | Example |
|-----------------|----------|---------|
| `app.dependency_overrides` | DB, auth, services | `app.dependency_overrides[dep] = mock` |
| `unittest.mock.patch` | Functions, global state | `with patch("module.func") as m:` |
| `pytest-mock` | Clean syntax | `mocker.patch("module.func")` |
| `respx` | HTTP requests | `respx.get("url").mock(...)` |
| `AsyncMock` | Async functions | `AsyncMock(return_value="val")` |
| Fake classes | Simple replacements | `class FakeDB: ...` |

### Key Rules

1. Mock at the boundary (DB, network, file system)
2. Prefer dependency overrides for FastAPI dependencies
3. Clean up mocks automatically with fixtures
4. Test behavior, not implementation
5. Keep mocks simple and focused
