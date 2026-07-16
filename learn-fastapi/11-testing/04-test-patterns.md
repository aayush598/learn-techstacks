# Test Patterns

## Table of Contents

1. [Arrange-Act-Assert Pattern](#1-aaa)
2. [Factory Pattern for Test Data](#2-factory-pattern)
3. [Snapshot Testing](#3-snapshot)
4. [Contract Testing](#4-contract)
5. [Load Testing](#5-load-testing)
6. [Integration Testing](#6-integration)
7. [End-to-End Testing](#7-e2e)
8. [Test Data Management](#8-data-management)
9. [Test Doubles](#9-test-doubles)
10. [Parameterized Testing](#10-parameterized)
11. [Test Isolation](#11-isolation)
12. [Golden Master Testing](#12-golden-master)
13. [Best Practices](#13-best-practices)

---

## 1. Arrange-Act-Assert Pattern <a name="1-aaa"></a>

AAA is the fundamental pattern for structuring tests. Every test should follow these
three phases clearly.

### Basic AAA

```python
def test_create_item(client):
    # ARRANGE: Set up test data and preconditions
    item_data = {
        "name": "Widget",
        "description": "A useful widget",
        "price": 29.99,
        "tax": 2.50,
    }

    # ACT: Execute the operation being tested
    response = client.post("/items/", json=item_data)

    # ASSERT: Verify the outcome
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Widget"
    assert data["total"] == 32.49
```

### AAA with Setup/Teardown

```python
@pytest.fixture
def item_payload():
    """ARRANGE: Shared test data."""
    return {
        "name": "Test Item",
        "description": "For testing",
        "price": 10.0,
    }

def test_get_item(client, item_payload):
    # ARRANGE
    create_response = client.post("/items/", json=item_payload)
    item_id = create_response.json()["id"]

    # ACT
    response = client.get(f"/items/{item_id}")

    # ASSERT
    assert response.status_code == 200
    assert response.json()["name"] == item_payload["name"]

def test_update_item(client, item_payload):
    # ARRANGE
    create_response = client.post("/items/", json=item_payload)
    item_id = create_response.json()["id"]
    updated_data = {"name": "Updated Item", "price": 39.99}

    # ACT
    response = client.put(f"/items/{item_id}", json=updated_data)

    # ASSERT
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Item"
    assert response.json()["price"] == 39.99
```

### Given-When-Then (BDD Variant)

```python
def test_user_registration(client):
    # GIVEN: A new user with valid data
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "SecurePass123!",
    }

    # WHEN: The user submits registration
    response = client.post("/register", json=user_data)

    # THEN: User is created successfully
    assert response.status_code == 201
    assert response.json()["email"] == "john@example.com"
    assert "password" not in response.json()  # Password not returned

    # THEN: User can login with the credentials
    login_response = client.post("/login", json={
        "email": "john@example.com",
        "password": "SecurePass123!",
    })
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
```

### Multiple Asserts in AAA

```python
def test_item_calculation(client):
    # ARRANGE
    item_data = {"name": "Expensive Item", "price": 100.0, "tax": 10.0}

    # ACT
    response = client.post("/items/", json=item_data)

    # ASSERT (multiple related assertions)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Expensive Item"
    assert data["price"] == 100.0
    assert data["tax"] == 10.0
    assert data["total"] == 110.0
    assert data["id"] is not None
    assert isinstance(data["id"], int)
```

---

## 2. Factory Pattern for Test Data <a name="2-factory-pattern"></a>

### Simple Factory Function

```python
import random

def make_user(**kwargs):
    """Factory function for creating test users."""
    defaults = {
        "name": f"User {random.randint(1000, 9999)}",
        "email": f"user{random.randint(1000, 9999)}@test.com",
        "password": "testpass123",
        "role": "user",
        "is_active": True,
    }
    defaults.update(kwargs)
    return defaults

def make_item(**kwargs):
    """Factory function for creating test items."""
    defaults = {
        "name": f"Item {random.randint(1000, 9999)}",
        "description": "Test item description",
        "price": round(random.uniform(1.0, 1000.0), 2),
        "tax": None,
        "is_available": True,
    }
    defaults.update(kwargs)
    return defaults

def make_order(**kwargs):
    """Factory function for creating test orders."""
    defaults = {
        "user_id": 1,
        "items": [{"item_id": 1, "quantity": 1}],
        "shipping_address": "123 Test St",
        "status": "pending",
    }
    defaults.update(kwargs)
    return defaults

# Usage
def test_create_user(client):
    user = make_user(name="Alice", role="admin")
    response = client.post("/users/", json=user)
    assert response.status_code == 201

def test_create_item(client):
    item = make_item(price=29.99)
    response = client.post("/items/", json=item)
    assert response.status_code == 201
```

### factory_boy Library

```python
# factories.py
import factory
from factory import fuzzy
from app.models import User, Item, Order
from app.db import get_db_session

class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Sequence(lambda n: f"User {n}")
    email = factory.Sequence(lambda n: f"user{n}@test.com")
    password = "hashed_password_here"
    role = fuzzy.FuzzyChoice(["admin", "user", "moderator"])
    is_active = True
    created_at = factory.Faker("date_time_this_year")

class ItemFactory(factory.Factory):
    class Meta:
        model = Item

    name = factory.Sequence(lambda n: f"Item {n}")
    description = factory.Faker("sentence")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    is_available = True

class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    items = factory.LazyFunction(lambda: [ItemFactory()])
    status = fuzzy.FuzzyChoice(["pending", "processing", "shipped"])
    total = factory.LazyAttribute(lambda o: sum(item.price for item in o.items))

# tests/test_user.py
from factories import UserFactory, ItemFactory

def test_user_creation(client):
    user_data = UserFactory.build()  # Build without saving to DB
    response = client.post("/users/", json={
        "name": user_data.name,
        "email": user_data.email,
        "password": "testpass123",
    })
    assert response.status_code == 201

def test_item_listing(client):
    # Create multiple items
    items = [ItemFactory() for _ in range(5)]
    # Note: In real tests, you'd insert these into the test DB

    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) >= 5
```

### Faker for Realistic Data

```python
from faker import Faker

fake = Faker()

def make_realistic_user():
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip": fake.zipcode(),
            "country": "US",
        },
        "bio": fake.text(max_nb_chars=200),
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
    }

def test_create_realistic_user(client):
    user = make_realistic_user()
    response = client.post("/users/", json=user)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user["email"]
```

### Factory with Sequences

```python
import factory

class SequentialUserFactory(factory.Factory):
    class Meta:
        model = dict

    _id = 0

    @factory.sequence
    def id(n):
        return n

    @factory.sequence
    def name(n):
        return f"User {n}"

    @factory.sequence
    def email(n):
        return f"user{n}@example.com"

# Each call gets unique, sequential values
users = [SequentialUserFactory() for _ in range(3)]
# [{"id": 1, "name": "User 1", "email": "user1@example.com"}, ...]
```

---

## 3. Snapshot Testing <a name="3-snapshot"></a>

Snapshot testing captures the output of a function and compares future runs against
that snapshot. Great for API response formats.

### Using syrupy (pytest snapshot)

```bash
pip install syrupy
```

```python
# tests/test_snapshots.py
import pytest

def test_api_response_snapshot(client, snapshot):
    """Test that API response format hasn't changed."""
    response = client.get("/items/")
    assert response.json() == snapshot

def test_user_schema_snapshot(client, snapshot):
    """Test that user response schema is stable."""
    response = client.post("/users/", json={
        "name": "Snapshot User",
        "email": "snapshot@test.com",
    })
    assert response.json() == snapshot

# Update snapshots when intentional changes are made
# pytest --snapshot-update
```

### Custom Snapshot Testing

```python
import json
import os
import pytest

SNAPSHOT_DIR = "tests/snapshots"

@pytest.fixture
def snapshot_manager():
    """Simple snapshot testing manager."""

    class SnapshotManager:
        def __init__(self, snapshot_dir):
            self.snapshot_dir = snapshot_dir
            os.makedirs(snapshot_dir, exist_ok=True)

        def assert_matches_snapshot(self, name, actual_data):
            snapshot_path = os.path.join(self.snapshot_dir, f"{name}.json")

            if os.path.exists(snapshot_path):
                with open(snapshot_path, "r") as f:
                    expected = json.load(f)
                assert actual_data == expected, (
                    f"Snapshot mismatch for '{name}'. "
                    f"Run with --update-snapshots to update."
                )
            else:
                # Create new snapshot
                with open(snapshot_path, "w") as f:
                    json.dump(actual_data, f, indent=2)

    return SnapshotManager(SNAPSHOT_DIR)

def test_response_format(client, snapshot_manager):
    response = client.get("/items/1")
    snapshot_manager.assert_matches_snapshot("item_response", response.json())

# Run with: pytest --update-snapshots
```

### Response Schema Snapshot

```python
def extract_schema(data):
    """Extract the schema (structure) from a data object."""
    if isinstance(data, dict):
        return {k: extract_schema(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [extract_schema(data[0])] if data else []
    elif isinstance(data, str):
        return "string"
    elif isinstance(data, (int, float)):
        return "number"
    elif isinstance(data, bool):
        return "boolean"
    elif data is None:
        return "null"
    return "unknown"

def test_api_response_schema_snapshot(client, snapshot):
    response = client.get("/items/")
    schema = extract_schema(response.json())
    assert schema == snapshot
```

---

## 4. Contract Testing <a name="4-contract"></a>

Contract testing verifies that API providers and consumers agree on the API
interface. Tools like Pact enable consumer-driven contracts.

### Basic Contract Definition

```python
# Consumer side (tests/test_api_contract.py)
from pact import Consumer, Provider

pact = Consumer("FrontendApp").has_pact_with(
    Provider("BackendAPI"),
    pact_dir="./pacts",
)

def test_get_items_contract():
    """Verify the API contract for GET /items/."""
    expected_response = [
        {
            "id": 1,
            "name": "Test Item",
            "price": 29.99,
            "is_available": True,
        }
    ]

    pact.given("items exist")
    pact.upon_receiving("a request for items")
    pact.with_request("get", "/api/v1/items/")
    pact.will_respond_with(200, body=expected_response)

    with pact:
        # Consumer code that calls the API
        response = get_items_from_api()
        assert len(response) == 1
        assert response[0]["name"] == "Test Item"
```

### Contract Testing with schemathesis

```python
# tests/test_api_contract_validation.py
import schemathesis
from app.main import app

# Auto-generate tests from OpenAPI schema
schema = schemathesis.from_asgi("/openapi.json", app=app)

@schema.parametrize()
def test_api_contract(case):
    """Auto-generated contract tests from OpenAPI spec."""
    response = case.call_asgi(app)
    case.validate_response(response)
```

### Manual Contract Testing

```python
def test_api_contract_get_items(client):
    """Verify GET /items/ returns expected structure."""
    response = client.get("/items/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        item = data[0]
        assert "id" in item
        assert isinstance(item["id"], int)
        assert "name" in item
        assert isinstance(item["name"], str)
        assert "price" in item
        assert isinstance(item["price"], (int, float))

def test_api_contract_post_item(client):
    """Verify POST /items/ accepts and returns expected structure."""
    request_payload = {
        "name": "Test Item",
        "price": 29.99,
    }

    response = client.post("/items/", json=request_payload)
    assert response.status_code == 201

    data = response.json()
    assert isinstance(data, dict)
    assert "id" in data
    assert data["name"] == request_payload["name"]
    assert data["price"] == request_payload["price"]
    assert "created_at" in data  # Response has additional fields

def test_api_contract_error_response(client):
    """Verify error responses follow consistent structure."""
    response = client.get("/items/99999")
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data
    assert isinstance(data["detail"], str)
```

---

## 5. Load Testing <a name="5-load-testing"></a>

### Locust (Python-based)

```python
# locustfile.py
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Login and get auth token."""
        response = self.client.post("/auth/login", json={
            "email": "loadtest@test.com",
            "password": "password123",
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)  # Weight: 3x more likely
    def view_items(self):
        self.client.get("/items/", headers=self.headers)

    @task(1)  # Weight: 1x
    def create_item(self):
        self.client.post("/items/", json={
            "name": f"Load Test Item {self.environment.runner.user_count}",
            "price": 10.0,
        }, headers=self.headers)

    @task(2)  # Weight: 2x
    def view_item(self):
        self.client.get("/items/1", headers=self.headers)

    @task(1)
    def search_items(self):
        self.client.get("/items/?search=test", headers=self.headers)
```

### k6 (JavaScript-based load testing)

```javascript
// loadtest.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Ramp up
    { duration: '1m', target: 20 },   // Stay at 20 users
    { duration: '30s', target: 50 },  // Ramp up to 50
    { duration: '1m', target: 50 },   // Stay at 50
    { duration: '30s', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    http_req_failed: ['rate<0.01'],     // Less than 1% failures
  },
};

export default function () {
  const BASE_URL = 'http://localhost:8000';

  // GET items
  const itemsRes = http.get(`${BASE_URL}/items/`);
  check(itemsRes, {
    'items status is 200': (r) => r.status === 200,
    'items response time < 200ms': (r) => r.timings.duration < 200,
  });

  sleep(1);

  // POST item
  const payload = JSON.stringify({
    name: `k6 Item ${Date.now()}`,
    price: 10.0,
  });

  const postRes = http.post(`${BASE_URL}/items/`, payload, {
    headers: { 'Content-Type': 'application/json' },
  });

  check(postRes, {
    'create status is 201': (r) => r.status === 201,
  });
}
```

### pytest-benchmark

```python
# tests/test_benchmark.py
import pytest

def test_benchmark_create_item(benchmark, client):
    """Benchmark item creation endpoint."""
    def create():
        return client.post("/items/", json={
            "name": "Benchmark Item",
            "price": 10.0,
        })

    result = benchmark(create)
    assert result.status_code == 201

def test_benchmark_concurrent_reads(benchmark, client):
    """Benchmark concurrent read operations."""
    import asyncio

    async def read_all():
        tasks = [client.get(f"/items/{i}") for i in range(1, 101)]
        return await asyncio.gather(*tasks)

    benchmark(lambda: asyncio.run(read_all()))
```

---

## 6. Integration Testing <a name="6-integration"></a>

### Database Integration Tests

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, get_db
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture(scope="module")
def integration_engine():
    """Real database for integration tests."""
    engine = create_engine("sqlite:///integration_test.db")
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    import os
    os.remove("integration_test.db")

@pytest.fixture
def integration_session(integration_engine):
    connection = integration_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
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

def test_full_crud_flow(integration_client):
    """Integration test: complete CRUD lifecycle."""
    # Create
    response = integration_client.post("/items/", json={
        "name": "Integration Item",
        "price": 25.0,
    })
    assert response.status_code == 201
    item_id = response.json()["id"]

    # Read
    response = integration_client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Integration Item"

    # Update
    response = integration_client.put(f"/items/{item_id}", json={
        "name": "Updated Integration Item",
        "price": 50.0,
    })
    assert response.status_code == 200

    # Delete
    response = integration_client.delete(f"/items/{item_id}")
    assert response.status_code == 204

    # Verify deletion
    response = integration_client.get(f"/items/{item_id}")
    assert response.status_code == 404
```

### Service Integration Tests

```python
@pytest.mark.integration
async def test_order_placement_flow(integration_client):
    """Test complete order placement with inventory check."""
    # 1. Create user
    user_resp = integration_client.post("/users/", json={
        "name": "Integration User",
        "email": "integration@test.com",
    })
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    # 2. Create item with inventory
    item_resp = integration_client.post("/items/", json={
        "name": "Orderable Item",
        "price": 25.0,
        "stock": 10,
    })
    assert item_resp.status_code == 201
    item_id = item_resp.json()["id"]

    # 3. Place order
    order_resp = integration_client.post("/orders/", json={
        "user_id": user_id,
        "items": [{"item_id": item_id, "quantity": 2}],
    })
    assert order_resp.status_code == 201
    order_id = order_resp.json()["id"]

    # 4. Verify inventory decreased
    item_resp = integration_client.get(f"/items/{item_id}")
    assert item_resp.json()["stock"] == 8

    # 5. Verify order details
    order_resp = integration_client.get(f"/orders/{order_id}")
    assert order_resp.json()["total"] == 50.0
    assert order_resp.json()["status"] == "pending"
```

---

## 7. End-to-End Testing <a name="7-e2e"></a>

### Playwright E2E Tests

```python
# tests/e2e/test_user_flow.py
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="module")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": "http://localhost:8000",
    }

def test_complete_user_registration_flow(page: Page):
    """E2E test: user registration through the UI."""
    # Navigate to registration
    page.goto("/register")

    # Fill out form
    page.fill('input[name="name"]', "E2E User")
    page.fill('input[name="email"]', "e2e@test.com")
    page.fill('input[name="password"]', "SecurePass123!")
    page.click('button[type="submit"]')

    # Verify redirect to dashboard
    expect(page).to_have_url("/dashboard")
    expect(page.locator("h1")).to_have_text("Welcome, E2E User!")

def test_complete_order_flow(page: Page, logged_in_user):
    """E2E test: placing an order through the UI."""
    # Navigate to shop
    page.goto("/shop")

    # Add item to cart
    page.click('[data-testid="add-to-cart-1"]')
    expect(page.locator('[data-testid="cart-count"]')).to_have_text("1")

    # Go to checkout
    page.click('[data-testid="checkout-button"]')
    expect(page).to_have_url("/checkout")

    # Fill shipping info
    page.fill('input[name="address"]', "123 Test Street")
    page.fill('input[name="city"]', "Testville")
    page.fill('input[name="zip"]', "12345")

    # Place order
    page.click('button[data-testid="place-order"]')

    # Verify confirmation
    expect(page.locator('[data-testid="order-confirmation"]')).to_be_visible()
    expect(page.locator('[data-testid="order-number"]')).not_to_be_empty()
```

### E2E API Tests with Real Server

```python
import pytest
import httpx
import subprocess
import time
import signal

@pytest.fixture(scope="session")
def real_server():
    """Start a real server for E2E tests."""
    process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8999"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(3)  # Wait for server to start

    yield "http://127.0.0.1:8999"

    process.send_signal(signal.SIGTERM)
    process.wait()

@pytest.fixture
def real_client(real_server):
    with httpx.Client(base_url=real_server) as client:
        yield client

@pytest.mark.e2e
def test_full_user_lifecycle(real_client):
    """E2E test with real HTTP server and database."""
    # Register
    reg_resp = real_client.post("/register", json={
        "name": "E2E User",
        "email": "e2e@test.com",
        "password": "SecurePass123!",
    })
    assert reg_resp.status_code == 201

    # Login
    login_resp = real_client.post("/login", json={
        "email": "e2e@test.com",
        "password": "SecurePass123!",
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    # Access protected resource
    profile_resp = real_client.get(
        "/profile/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert profile_resp.status_code == 200
    assert profile_resp.json()["name"] == "E2E User"
```

---

## 8. Test Data Management <a name="8-data-management"></a>

### Test Data Builder Pattern

```python
class TestDataBuilder:
    """Fluent builder for complex test data."""

    def __init__(self):
        self._users = []
        self._items = []
        self._orders = []

    def with_user(self, **kwargs) -> "TestDataBuilder":
        self._users.append(make_user(**kwargs))
        return self

    def with_item(self, **kwargs) -> "TestDataBuilder":
        self._items.append(make_item(**kwargs))
        return self

    def with_order(self, user_index=0, item_indices=None, **kwargs) -> "TestDataBuilder":
        if item_indices is None:
            item_indices = [0]
        order = make_order(
            user_id=f"$users[{user_index}].id",
            items=[{"item_id": f"$items[{i}].id"} for i in item_indices],
            **kwargs,
        )
        self._orders.append(order)
        return self

    def build(self) -> dict:
        return {
            "users": self._users,
            "items": self._items,
            "orders": self._orders,
        }

# Usage
data = (
    TestDataBuilder()
    .with_user(name="Admin", role="admin")
    .with_user(name="Regular User", role="user")
    .with_item(name="Laptop", price=999.99)
    .with_item(name="Phone", price=699.99)
    .with_order(user_index=0, item_indices=[0, 1])
    .build()
)
```

### Seed Data

```python
# tests/seed_data.py
SEED_USERS = [
    {"name": "Admin User", "email": "admin@test.com", "role": "admin"},
    {"name": "Regular User", "email": "user@test.com", "role": "user"},
    {"name": "Moderator", "email": "mod@test.com", "role": "moderator"},
]

SEED_ITEMS = [
    {"name": "Laptop", "price": 999.99, "description": "High-performance laptop"},
    {"name": "Phone", "price": 699.99, "description": "Latest smartphone"},
    {"name": "Tablet", "price": 499.99, "description": "Portable tablet"},
]

SEED_CATEGORIES = [
    {"name": "Electronics", "description": "Electronic devices"},
    {"name": "Accessories", "description": "Device accessories"},
    {"name": "Software", "description": "Software products"},
]

@pytest.fixture(scope="session")
def seed_database():
    """Seed the test database with initial data."""
    from app.db import SessionLocal, engine
    from app.models import User, Item, Category

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        for user_data in SEED_USERS:
            db.add(User(**user_data))
        for item_data in SEED_ITEMS:
            db.add(Item(**item_data))
        for cat_data in SEED_CATEGORIES:
            db.add(Category(**cat_data))
        db.commit()
    finally:
        db.close()

    yield

    Base.metadata.drop_all(bind=engine)
```

### Data Cleanup Strategies

```python
# Strategy 1: Transaction rollback (fastest, most common)
@pytest.fixture
def clean_db_session(db_session):
    yield db_session
    db_session.rollback()

# Strategy 2: Truncate tables (between tests)
@pytest.fixture(autouse=True)
def truncate_tables(integration_engine):
    yield
    with integration_engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())

# Strategy 3: Use test-specific prefixes
@pytest.fixture
def test_data(client):
    prefix = f"test_{uuid.uuid4().hex[:8]}"
    yield {"prefix": prefix}
    # Cleanup: delete all data with this prefix
    client.delete(f"/cleanup/{prefix}")
```

---

## 9. Test Doubles <a name="9-test-doubles"></a>

### Types of Test Doubles

```python
# 1. Dummy: Passed around but never used
class DummyUser:
    def __init__(self):
        self.id = 1
        self.name = "Dummy"

# 2. Stub: Returns predefined values
class StubAuthService:
    def get_current_user(self):
        return User(id=1, name="Stub User", role="user")

# 3. Spy: Records calls for later verification
class SpyEmailService:
    def __init__(self):
        self.sent_emails = []

    def send_email(self, to, subject, body):
        self.sent_emails.append({"to": to, "subject": subject, "body": body})

# 4. Mock: Predefined expectations + verification
class MockPaymentService:
    def __init__(self):
        self.expect_charge = None
        self.was_charged = False

    def charge(self, amount):
        self.was_charged = True
        if self.expect_charge:
            assert amount == self.expect_charge

# 5. Fake: Working implementation (simplified)
class FakeDatabase:
    def __init__(self):
        self.users = {}
        self._next_id = 1

    def add_user(self, user):
        user.id = self._next_id
        self.users[user.id] = user
        self._next_id += 1
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)
```

### Using Test Doubles

```python
@pytest.fixture
def stub_auth():
    """Stub: always returns the same user."""
    return StubAuthService()

@pytest.fixture
def spy_email():
    """Spy: tracks sent emails."""
    return SpyEmailService()

@pytest.fixture
def fake_db():
    """Fake: in-memory database."""
    return FakeDatabase()

def test_get_user_uses_auth(stub_auth):
    user = stub_auth.get_current_user()
    assert user.name == "Stub User"

def test_send_welcome_email(spy_email):
    spy_email.send_email("user@test.com", "Welcome!", "Hello!")
    assert len(spy_email.sent_emails) == 1
    assert spy_email.sent_emails[0]["to"] == "user@test.com"

def test_add_user(fake_db):
    user = User(name="Test", email="test@test.com")
    result = fake_db.add_user(user)
    assert result.id == 1
    assert fake_db.get_user(1) is not None
```

---

## 10. Parameterized Testing <a name="10-parameterized"></a>

### Advanced Parametrize

```python
import pytest

# Parametrize with complex data structures
@pytest.mark.parametrize("input_data,expected", [
    ({"name": "A", "price": 10}, {"total": 10, "discount": 0}),
    ({"name": "B", "price": 100}, {"total": 90, "discount": 10}),
    ({"name": "C", "price": 500}, {"total": 425, "discount": 75}),
], ids=["small", "medium", "large"])
def test_calculate_total_with_discount(input_data, expected):
    result = calculate_total(input_data["price"])
    assert result["total"] == expected["total"]
    assert result["discount"] == expected["discount"]

# Parametrize across multiple dimensions
@pytest.mark.parametrize("role", ["admin", "user", "guest"])
@pytest.mark.parametrize("endpoint", ["/users/", "/items/", "/orders/"])
def test_role_based_access(client, role, endpoint):
    headers = {"Authorization": f"Bearer {role}-token"}
    response = client.get(endpoint, headers=headers)
    # Admin can access everything, user can access items, guest gets 403
    if role == "admin":
        assert response.status_code == 200
    elif role == "user" and endpoint == "/users/":
        assert response.status_code == 403
    else:
        assert response.status_code == 200
```

### Parametrize with Fixtures

```python
@pytest.fixture
def api_endpoints():
    return [
        ("/users/", "GET", 200),
        ("/items/", "GET", 200),
        ("/orders/", "GET", 200),
        ("/admin/", "GET", 403),
        ("/health", "GET", 200),
    ]

@pytest.mark.parametrize("endpoint,method,expected_status", [
    ("/users/", "GET", 200),
    ("/items/", "GET", 200),
    ("/nonexistent", "GET", 404),
])
def test_endpoint_status(client, endpoint, method, expected_status):
    response = client.request(method, endpoint)
    assert response.status_code == expected_status
```

---

## 11. Test Isolation <a name="11-isolation"></a>

### Database Isolation

```python
@pytest.fixture(autouse=True)
def isolate_database(integration_engine):
    """Ensure each test runs in its own transaction."""
    connection = integration_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    # Override get_db to return this session
    app.dependency_overrides[get_db] = lambda: session

    yield session

    # Rollback everything
    session.close()
    transaction.rollback()
    connection.close()
    app.dependency_overrides.clear()
```

### Test Order Independence

```python
# BAD: Test depends on test ordering
@pytest.mark.dependency
def test_create_item(client):
    response = client.post("/items/", json={"name": "Test", "price": 10})
    assert response.status_code == 201

@pytest.mark.dependency(depends=["test_create_item"])
def test_get_item(client):
    response = client.get("/items/1")  # Assumes item 1 exists
    assert response.status_code == 200

# GOOD: Each test creates its own state
def test_create_and_get_item(client):
    # Create
    response = client.post("/items/", json={"name": "Test", "price": 10})
    assert response.status_code == 201
    item_id = response.json()["id"]

    # Get
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test"
```

### Global State Isolation

```python
@pytest.fixture(autouse=True)
def isolate_global_state():
    """Isolate global state between tests."""
    import app.services.cache as cache_module
    original_cache = cache_module.cache.copy()

    yield

    cache_module.cache.clear()
    cache_module.cache.update(original_cache)
```

---

## 12. Golden Master Testing <a name="12-golden-master"></a>

Capture the output of a function and assert it hasn't changed.

```python
import json
import os

GOLDEN_MASTER_DIR = "tests/golden_masters"

def assert_golden_master(name, actual_output):
    """Compare actual output against golden master."""
    filepath = os.path.join(GOLDEN_MASTER_DIR, f"{name}.json")

    if os.environ.get("UPDATE_GOLDEN_MASTERS"):
        os.makedirs(GOLDEN_MASTER_DIR, exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(actual_output, f, indent=2)
        return

    with open(filepath, "r") as f:
        expected = json.load(f)

    assert actual_output == expected, (
        f"Golden master '{name}' mismatch. "
        f"Run with UPDATE_GOLDEN_MASTERS=1 to update."
    )

def test_api_response_format(client):
    response = client.get("/items/")
    assert_golden_master("items_list_response", response.json())

def test_error_format(client):
    response = client.get("/items/99999")
    assert_golden_master("not_found_error", response.json())
```

---

## 13. Best Practices <a name="13-best-practices"></a>

### 1. One Concept Per Test

```python
# BAD: Tests multiple things
def test_item_crud(client):
    # Create, Read, Update, Delete all in one test

# GOOD: Separate tests
def test_create_item(client):
def test_read_item(client):
def test_update_item(client):
def test_delete_item(client):
```

### 2. Test the Contract, Not Implementation

```python
# BAD: Tests implementation
def test_create_item_calls_db(client, mock_db):
    client.post("/items/", json={"name": "Test", "price": 10})
    mock_db.add.assert_called_once()

# GOOD: Tests behavior
def test_create_item_returns_correct_response(client):
    response = client.post("/items/", json={"name": "Test", "price": 10})
    assert response.status_code == 201
    assert response.json()["name"] == "Test"
```

### 3. Use Descriptive Names

```python
# BAD
def test_create():
def test_error():
def test_auth():

# GOOD
def test_create_item_with_valid_data_returns_201():
def test_create_item_with_invalid_price_returns_422():
def test_protected_endpoint_without_token_returns_401():
def test_protected_endpoint_with_expired_token_returns_401():
```

### 4. Test Edge Cases

```python
@pytest.mark.parametrize("input,expected", [
    ("normal string", True),
    ("", False),                    # Empty string
    (" " * 1000, False),           # Whitespace only
    ("a" * 10000, True),           # Very long string
    ("<script>alert('xss')</script>", False),  # XSS attempt
    ("'; DROP TABLE users; --", False),         # SQL injection
    ("日本語テスト", True),          # Unicode
    ("\x00\x01\x02", False),      # Null bytes
])
def test_name_validation(input, expected):
    assert validate_name(input) == expected
```

---

## Summary

| Pattern | Use Case | Tool/Technique |
|---------|----------|---------------|
| AAA | Structure all tests | Arrange-Act-Assert |
| Factory | Create test data | factory_boy, Faker |
| Snapshot | Response format stability | syrupy, custom |
| Contract | API compatibility | schemathesis, Pact |
| Load | Performance under stress | Locust, k6, wrk |
| Integration | Multi-component | Real DB, service chain |
| E2E | Full stack | Playwright, httpx |
| Golden Master | Output stability | Custom snapshots |
| Test Doubles | Isolation | Mock, Stub, Fake, Spy |
