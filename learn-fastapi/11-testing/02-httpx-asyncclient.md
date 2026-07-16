# HTTPX AsyncClient with FastAPI

## Table of Contents

1. [Introduction](#1-introduction)
2. [httpx vs TestClient](#2-httpx-vs-testclient)
3. [AsyncClient Setup](#3-async-setup)
4. [Async Test Patterns](#4-async-patterns)
5. [Base URL Configuration](#5-base-url)
6. [Headers in Tests](#6-headers)
7. [Cookie Handling](#7-cookies)
8. [Timeout Configuration](#8-timeout)
9. [Streaming Response Testing](#9-streaming)
10. [WebSocket Testing](#10-websocket)
11. [File Upload Testing](#11-file-upload)
12. [Error Handling in Tests](#12-error-handling)
13. [Advanced Patterns](#13-advanced-patterns)
14. [Best Practices](#14-best-practices)

---

## 1. Introduction <a name="1-introduction"></a>

httpx is a fully featured HTTP client for Python 3 that provides both sync and async
clients. FastAPI recommends httpx for testing, especially for async tests. The
`ASGITransport` class allows httpx to communicate directly with your FastAPI app
through the ASGI interface, without starting an actual server.

### Key Features

- Async and sync HTTP clients
- ASGI transport for testing without server
- Connection pooling
- Timeout configuration
- Streaming support
- WebSocket support
- Cookie handling
- Authentication helpers

### Installation

```bash
pip install httpx
# For WebSocket testing
pip install httpx[websockets]
# For respx mocking
pip install respx
```

---

## 2. httpx vs TestClient <a name="2-httpx-vs-testclient"></a>

| Feature | TestClient (Starlette) | httpx.AsyncClient |
|---------|----------------------|-------------------|
| Async support | No (sync only) | Yes |
| Server required | No | No (with ASGITransport) |
| Connection pooling | N/A | Built-in |
| Streaming | Limited | Full support |
| Timeout control | Limited | Full control |
| Request interceptors | No | With respx |
| Recommended for | Simple sync tests | Async, complex tests |

### When to Use Each

```python
# TestClient - Simple synchronous tests
from fastapi.testclient import TestClient

def test_simple_endpoint():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200

# httpx.AsyncClient - Async tests with more control
from httpx import AsyncClient, ASGITransport

async def test_complex_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
```

---

## 3. AsyncClient Setup <a name="3-async-setup"></a>

### Basic Setup

```python
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest_asyncio.fixture
async def client():
    """Create an async test client for each test."""
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as ac:
        yield ac
```

### Setup with Configuration

```python
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(
        app=app,
        raise_app_exceptions=False,     # Don't propagate app exceptions
        root_path="/api/v1",            # Set the root path
    )
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
        headers={
            "X-Request-Source": "test",
            "Accept": "application/json",
        },
        timeout=30.0,
        follow_redirects=True,
    ) as ac:
        yield ac
```

### ASGITransport Options

```python
from httpx import ASGITransport

transport = ASGITransport(
    app=app,
    # Raise application exceptions (vs returning 500)
    raise_app_exceptions=True,
    # Client kwargs passed to every request
    client_kwargs={
        "headers": {"X-Trace": "true"},
    },
    # Root path for the application
    root_path="/api",
)
```

### With Dependency Overrides

```python
from app.db import get_db

@pytest_asyncio.fixture
async def client_with_mock_db(async_db_session):
    """Client with mocked database dependency."""
    def override_get_db():
        yield async_db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
```

---

## 4. Async Test Patterns <a name="4-async-patterns"></a>

### Sequential Requests

```python
async def test_crud_operations(client):
    # Create
    create_resp = await client.post("/items/", json={
        "name": "Laptop",
        "price": 999.99,
    })
    assert create_resp.status_code == 201
    item_id = create_resp.json()["id"]

    # Read
    read_resp = await client.get(f"/items/{item_id}")
    assert read_resp.status_code == 200
    assert read_resp.json()["name"] == "Laptop"

    # Update
    update_resp = await client.put(f"/items/{item_id}", json={
        "name": "Gaming Laptop",
        "price": 1499.99,
    })
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Gaming Laptop"

    # Delete
    delete_resp = await client.delete(f"/items/{item_id}")
    assert delete_resp.status_code == 204

    # Verify deleted
    get_resp = await client.get(f"/items/{item_id}")
    assert get_resp.status_code == 404
```

### Concurrent Requests

```python
import asyncio


async def test_concurrent_creates(client):
    """Test creating multiple items concurrently."""
    tasks = [
        client.post("/items/", json={"name": f"Item {i}", "price": i * 10.0})
        for i in range(10)
    ]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        assert response.status_code == 201

async def test_concurrent_reads(client):
    """Test reading items concurrently."""
    # First create some items
    for i in range(5):
        await client.post("/items/", json={"name": f"Item {i}", "price": 10.0})

    # Read all concurrently
    tasks = [client.get(f"/items/{i+1}") for i in range(5)]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        assert response.status_code == 200

async def test_concurrent_mixed_operations(client):
    """Test mixed operations concurrently."""
    # Create an item first
    create_resp = await client.post(
        "/items/",
        json={"name": "Shared Item", "price": 50.0},
    )
    item_id = create_resp.json()["id"]

    # Mix of reads and updates
    tasks = [
        client.get(f"/items/{item_id}"),
        client.get(f"/items/{item_id}"),
        client.put(f"/items/{item_id}", json={"name": "Updated", "price": 60.0}),
        client.get(f"/items/{item_id}"),
    ]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        assert response.status_code in (200, 204)
```

### Rate-Limited Concurrent Requests

```python
import asyncio


async def test_rate_limited_requests(client):
    """Test with semaphore to limit concurrency."""
    semaphore = asyncio.Semaphore(5)

    async def limited_request(item_id: int):
        async with semaphore:
            return await client.get(f"/items/{item_id}")

    tasks = [limited_request(i) for i in range(1, 21)]
    responses = await asyncio.gather(*tasks)

    success_count = sum(1 for r in responses if r.status_code == 200)
    assert success_count > 0
```

### Request with Context Manager

```python
async def test_with_request_context(client):
    """Test using request context for proper resource management."""
    async with client.stream("GET", "/stream-data") as response:
        assert response.status_code == 200
        data = b""
        async for chunk in response.aiter_bytes():
            data += chunk
        assert len(data) > 0
```

---

## 5. Base URL Configuration <a name="5-base-url"></a>

### Basic Base URL

```python
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as ac:
        yield ac

# Tests use relative URLs
async def test_endpoint(client):
    response = await client.get("/items/")
    # Full URL becomes: http://testserver/items/
```

### API Version Prefix

```python
@pytest_asyncio.fixture
async def api_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver/api/v1",
    ) as ac:
        yield ac

async def test_v1_endpoint(api_client):
    response = await api_client.get("/items/")
    # Full URL: http://testserver/api/v1/items/
```

### Multiple API Versions

```python
@pytest.fixture
def v1_client():
    transport = ASGITransport(app=v1_app)
    return AsyncClient(transport=transport, base_url="http://testserver/api/v1")

@pytest.fixture
def v2_client():
    transport = ASGITransport(app=v2_app)
    return AsyncClient(transport=transport, base_url="http://testserver/api/v2")

async def test_v1_list_items(v1_client):
    response = await v1_client.get("/items/")
    assert response.status_code == 200

async def test_v2_list_items(v2_client):
    response = await v2_client.get("/items/")
    assert response.status_code == 200
    # V2 might have different response format
    assert "metadata" in response.json()
```

---

## 6. Headers in Tests <a name="6-headers"></a>

### Default Headers

```python
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
        headers={
            "Accept": "application/json",
            "X-Custom-Header": "test-value",
        },
    ) as ac:
        yield ac
```

### Per-Request Headers

```python
async def test_custom_headers(client):
    response = await client.get(
        "/items/",
        headers={
            "X-Request-ID": "req-123",
            "X-Trace-ID": "trace-456",
            "Accept-Language": "en-US",
        },
    )
    assert response.status_code == 200
```

### Authentication Headers

```python
@pytest_asyncio.fixture
async def auth_client():
    transport = ASGITransport(app=app)

    # Login to get token
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as temp_client:
        login_resp = await temp_client.post("/auth/login", json={
            "email": "user@test.com",
            "password": "password123",
        })
        token = login_resp.json()["access_token"]

    # Create client with auth header
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
        headers={"Authorization": f"Bearer {token}"},
    ) as ac:
        yield ac

async def test_protected_endpoint(auth_client):
    response = await auth_client.get("/users/me")
    assert response.status_code == 200
```

### Bearer Token Header Pattern

```python
def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}

async def test_admin_endpoint(client, admin_token):
    response = await client.get(
        "/admin/dashboard",
        headers=auth_header(admin_token),
    )
    assert response.status_code == 200

async def test_user_endpoint(client, user_token):
    response = await client.get(
        "/users/me",
        headers=auth_header(user_token),
    )
    assert response.status_code == 200
```

### Content-Type Headers

```python
async def test_json_content_type(client):
    response = await client.post(
        "/items/",
        json={"name": "Foo", "price": 10.0},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 201

async def test_xml_content_type(client):
    xml_data = "<item><name>Foo</name></item>"
    response = await client.post(
        "/items/xml",
        content=xml_data,
        headers={"Content-Type": "application/xml"},
    )
    assert response.status_code == 201

async def test_form_content_type(client):
    response = await client.post(
        "/login",
        data={"username": "admin", "password": "secret"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
```

### Checking Response Headers

```python
async def test_response_headers(client):
    response = await client.get("/items/")
    assert response.status_code == 200

    # Check specific headers
    assert response.headers["content-type"] == "application/json"
    assert "x-request-id" in response.headers

    # Check caching headers
    assert "cache-control" in response.headers
    assert "etag" in response.headers

    # Check custom response headers
    assert response.headers["x-api-version"] == "1.0"
```

---

## 7. Cookie Handling <a name="7-cookies"></a>

### Setting Cookies

```python
@pytest_asyncio.fixture
async def client_with_session():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
        cookies={"session_id": "test-session-123"},
    ) as ac:
        yield ac

async def test_cookie_based_session(client_with_session):
    response = await client_with_session.get("/profile/")
    assert response.status_code == 200
```

### Managing Cookies Across Requests

```python
async def test_login_sets_cookie(client):
    # Login
    login_response = await client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "password123",
    })
    assert login_response.status_code == 200

    # Cookies are automatically stored in the client's cookie jar
    # Subsequent requests include the session cookie
    profile_response = await client.get("/users/me")
    assert profile_response.status_code == 200

    # Check cookies on client
    assert "session_id" in client.cookies
```

### Cookie Assertions

```python
async def test_cookie_attributes(client):
    response = await client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "password123",
    })

    # Get specific cookie
    session_cookie = response.cookies.get("session_id")
    assert session_cookie is not None

    # Check Set-Cookie header
    set_cookie_headers = response.headers.get_list("set-cookie")
    assert any("session_id" in header for header in set_cookie_headers)

    # Verify cookie attributes
    assert "HttpOnly" in str(set_cookie_headers)
    assert "Secure" in str(set_cookie_headers)
```

### Clearing Cookies

```python
async def test_logout_clears_cookie(client):
    # Login
    await client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "password123",
    })

    # Logout
    response = await client.post("/auth/logout")
    assert response.status_code == 200

    # Verify cookie is cleared
    client.cookies.clear()
    profile_response = await client.get("/users/me")
    assert profile_response.status_code == 401
```

### Cookie Security Testing

```python
async def test_cookie_security_flags(client):
    """Verify security flags on auth cookies."""
    response = await client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "password123",
    })

    set_cookie = response.headers.get("set-cookie", "")

    # HttpOnly - prevents JavaScript access
    assert "httponly" in set_cookie.lower()

    # Secure - only sent over HTTPS (in production)
    # assert "secure" in set_cookie.lower()

    # SameSite - CSRF protection
    assert "samesite" in set_cookie.lower()
```

---

## 8. Timeout Configuration <a name="8-timeout"></a>

### Default Timeout

```python
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
        timeout=10.0,  # 10 second timeout
    ) as ac:
        yield ac
```

### Timeout Types

```python
import httpx

# Single timeout for all operations
client = AsyncClient(timeout=30.0)

# Granular timeout control
client = AsyncClient(
    timeout=httpx.Timeout(
        connect=5.0,     # Connection establishment
        read=30.0,       # Reading response body
        write=10.0,      # Sending request body
        pool=5.0,        # Waiting for a connection from the pool
    )
)

# No timeout (for testing long-running operations)
client = AsyncClient(timeout=None)
```

### Testing Timeout Behavior

```python
import pytest
from unittest.mock import AsyncMock, patch

async def test_endpoint_timeout(client):
    """Test how app handles slow dependencies."""
    with patch("app.services.slow_function", new_callable=AsyncMock) as mock:
        mock.side_effect = asyncio.TimeoutError("Service timed out")

        response = await client.get("/slow-endpoint")
        assert response.status_code == 504
        assert "timeout" in response.json()["detail"].lower()

async def test_client_timeout(client):
    """Test client-side timeout."""
    with pytest.raises(httpx.ReadTimeout):
        # Use a very short timeout for this test
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport,
            base_url="http://testserver",
            timeout=0.001,  # 1ms timeout
        ) as timeout_client:
            await timeout_client.get("/slow-endpoint")
```

### Timeout Per Request

```python
async def test_different_timeouts(client):
    # Fast endpoint - short timeout
    response = await client.get("/health", timeout=1.0)
    assert response.status_code == 200

    # Slow endpoint - longer timeout
    response = await client.get("/reports/generate", timeout=60.0)
    assert response.status_code == 200
```

---

## 9. Streaming Response Testing <a name="9-streaming"></a>

### Testing Streaming Endpoints

```python
# Application code
from fastapi.responses import StreamingResponse
from fastapi import FastAPI

app = FastAPI()

@app.get("/stream")
async def stream_data():
    async def generate():
        for i in range(100):
            yield f"data: {i}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


# Test code
async def test_streaming_response(client):
    async with client.stream("GET", "/stream") as response:
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

        chunks = []
        async for line in response.aiter_lines():
            chunks.append(line)
            if len(chunks) >= 5:
                break

        assert len(chunks) == 5
        assert chunks[0] == "data: 0"
```

### Streaming JSON Lines

```python
import json

async def test_streaming_jsonl(client):
    async with client.stream("GET", "/items/stream") as response:
        items = []
        async for line in response.aiter_lines():
            if line:
                item = json.loads(line)
                items.append(item)

        assert len(items) > 0
        assert "name" in items[0]

async def test_streaming_bytes(client):
    async with client.stream("GET", "/download") as response:
        total_bytes = 0
        async for chunk in response.aiter_bytes():
            total_bytes += len(chunk)

        assert total_bytes > 0

async def test_streaming_with_filter(client):
    async with client.stream("GET", "/items/stream") as response:
        filtered = []
        async for line in response.aiter_lines():
            if line:
                item = json.loads(line)
                if item.get("price", 0) > 100:
                    filtered.append(item)

        assert all(item["price"] > 100 for item in filtered)
```

### Server-Sent Events (SSE)

```python
async def test_sse_stream(client):
    async with client.stream("GET", "/events") as response:
        events = []
        current_event = {}

        async for line in response.aiter_lines():
            if line.startswith("event:"):
                current_event["type"] = line.split(":", 1)[1].strip()
            elif line.startswith("data:"):
                current_event["data"] = line.split(":", 1)[1].strip()
            elif line == "" and current_event:
                events.append(current_event)
                current_event = {}
                if len(events) >= 3:
                    break

        assert len(events) >= 3
        assert all("type" in event for event in events)
```

---

## 10. WebSocket Testing <a name="10-websocket"></a>

### Basic WebSocket Test

```python
# Application code
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")


# Test code
async def test_websocket_echo(client):
    async with client.websocket_connect("/ws") as ws:
        await ws.send_text("Hello")
        data = await ws.receive_text()
        assert data == "Echo: Hello"

async def test_websocket_multiple_messages(client):
    async with client.websocket_connect("/ws") as ws:
        for i in range(5):
            await ws.send_text(f"Message {i}")
            data = await ws.receive_text()
            assert data == f"Echo: Message {i}"
```

### WebSocket with Authentication

```python
async def test_authenticated_websocket(client, auth_token):
    async with client.websocket_connect(
        "/ws/notifications",
        headers={"Authorization": f"Bearer {auth_token}"},
    ) as ws:
        message = await ws.receive_json()
        assert message["type"] == "welcome"

async def test_unauthenticated_websocket(client):
    with pytest.raises(Exception):
        async with client.websocket_connect("/ws/notifications") as ws:
            await ws.receive_text()
```

### WebSocket JSON Messages

```python
async def test_websocket_json(client):
    async with client.websocket_connect("/ws/chat") as ws:
        # Send JSON
        await ws.send_json({
            "type": "message",
            "content": "Hello, world!",
            "channel": "general",
        })

        # Receive JSON response
        response = await ws.receive_json()
        assert response["type"] == "message_ack"
        assert "message_id" in response

async def test_websocket_binary(client):
    async with client.websocket_connect("/ws/upload") as ws:
        # Send binary data
        await ws.send_bytes(b"\x00\x01\x02\x03")

        # Receive confirmation
        response = await ws.receive_json()
        assert response["type"] == "upload_complete"
        assert response["bytes_received"] == 4
```

### WebSocket Connection Lifecycle

```python
async def test_websocket_lifecycle(client):
    async with client.websocket_connect("/ws") as ws:
        # Connection established
        welcome = await ws.receive_text()
        assert "welcome" in welcome.lower()

        # Normal communication
        await ws.send_text("ping")
        pong = await ws.receive_text()
        assert pong == "Echo: ping"

        # Close connection
        await ws.close(code=1000, reason="Normal close")

async def test_websocket_close_codes(client):
    async with client.websocket_connect("/ws") as ws:
        await ws.send_text("error")
        # Server might close with error code
        with pytest.raises(Exception):
            await ws.receive_text()
```

---

## 11. File Upload Testing <a name="11-file-upload"></a>

### Basic File Upload

```python
async def test_file_upload(client):
    files = {
        "file": ("test.txt", b"Hello, World!", "text/plain"),
    }
    response = await client.post("/upload", files=files)
    assert response.status_code == 200
    assert response.json()["filename"] == "test.txt"

async def test_image_upload(client):
    # Simulating image bytes
    image_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100  # Minimal PNG header

    files = {
        "file": ("photo.png", image_bytes, "image/png"),
    }
    data = {
        "description": "Test photo",
        "tags": "test,demo",
    }
    response = await client.post("/upload/image", files=files, data=data)
    assert response.status_code == 201
```

### Multiple File Upload

```python
async def test_multiple_file_upload(client):
    files = [
        ("files", ("file1.txt", b"Content 1", "text/plain")),
        ("files", ("file2.txt", b"Content 2", "text/plain")),
        ("files", ("file3.csv", b"a,b,c\n1,2,3", "text/csv")),
    ]
    response = await client.post("/upload/multiple", files=files)
    assert response.status_code == 200
    assert response.json()["count"] == 3

async def test_mixed_files_and_data(client):
    files = [
        ("documents", ("resume.pdf", b"%PDF-1.4 fake", "application/pdf")),
        ("documents", ("cover.docx", b"PK fake docx", "application/vnd.openxmlformats")),
    ]
    data = {
        "application_id": "12345",
        "notes": "Please review my application",
    }
    response = await client.post("/apply", files=files, data=data)
    assert response.status_code == 201
```

### File Validation Testing

```python
async def test_upload_too_large(client):
    # Create a 10MB file
    large_content = b"x" * (10 * 1024 * 1024)
    files = {"file": ("large.bin", large_content, "application/octet-stream")}
    response = await client.post("/upload", files=files)
    assert response.status_code == 413  # Payload Too Large

async def test_upload_invalid_extension(client):
    files = {"file": ("malware.exe", b"MZ fake exe", "application/octet-stream")}
    response = await client.post("/upload", files=files)
    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"].lower()

async def test_upload_empty_file(client):
    files = {"file": ("empty.txt", b"", "text/plain")}
    response = await client.post("/upload", files=files)
    assert response.status_code == 400
```

---

## 12. Error Handling in Tests <a name="12-error-handling"></a>

### Testing HTTP Error Responses

```python
async def test_404_error(client):
    response = await client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

async def test_422_validation_error(client):
    response = await client.post("/items/", json={"name": ""})
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert len(errors) > 0
    assert errors[0]["loc"] == ["body", "name"]

async def test_401_unauthorized(client):
    response = await client.get("/protected")
    assert response.status_code == 401

async def test_403_forbidden(client, user_token):
    response = await client.get(
        "/admin/dashboard",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 403
```

### Testing Server Errors

```python
async def test_internal_server_error(client):
    with patch("app.services.risky_operation", side_effect=RuntimeError("Oops")):
        response = await client.post("/risky-endpoint")
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"

async def test_503_service_unavailable(client):
    with patch("app.db.check_connection", return_value=False):
        response = await client.get("/health")
        assert response.status_code == 503
```

### Testing Exception Handlers

```python
# Application code
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

class CustomError(Exception):
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code

@app.exception_handler(CustomError)
async def custom_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.code,
            "message": exc.message,
        },
    )

@app.get("/custom-error")
async def raise_custom_error():
    raise CustomError(message="Something went wrong", code="CUSTOM_ERROR")


# Test code
async def test_custom_exception_handler(client):
    response = await client.get("/custom-error")
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "CUSTOM_ERROR"
    assert data["message"] == "Something went wrong"
```

---

## 13. Advanced Patterns <a name="13-advanced-patterns"></a>

### Mocked External Services with respx

```python
import respx
import httpx

@respx.mock
async def test_with_mocked_external_api(client):
    # Mock external API call
    respx.get("https://api.external.com/data").mock(
        return_value=httpx.Response(200, json={"result": "mocked"})
    )

    response = await client.get("/proxy/external-data")
    assert response.status_code == 200
    assert response.json()["result"] == "mocked"
```

### Request/Response Assertions

```python
async def test_request_response_assertions(client):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/users").mock(
            return_value=httpx.Response(200, json=[])
        )

        response = await client.get("/users/external")

        # Assert the external API was called
        assert mock_route.called
        assert mock_route.call_count == 1

        # Check the request that was made
        request = mock_route.calls[0].request
        assert request.url == "https://api.example.com/users"
        assert request.headers["Authorization"] == "Bearer api-key"
```

### Testing Response Time

```python
import time

async def test_response_time(client):
    start = time.perf_counter()
    response = await client.get("/items/")
    elapsed = time.perf_counter() - start

    assert response.status_code == 200
    assert elapsed < 1.0  # Should respond within 1 second

async def test_concurrent_performance(client):
    """Verify concurrent requests don't degrade performance."""
    import asyncio

    start = time.perf_counter()

    tasks = [client.get("/") for _ in range(100)]
    responses = await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start

    assert all(r.status_code == 200 for r in responses)
    assert elapsed < 5.0  # 100 requests in under 5 seconds
```

### Session-Scoped Client with State

```python
import pytest_asyncio

@pytest_asyncio.fixture(scope="session")
async def seed_db():
    """Seed database once for entire test session."""
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        for i in range(100):
            item = Item(name=f"Item {i}", price=i * 10.0)
            session.add(item)
        await session.commit()

    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def client(seed_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
```

---

## 14. Best Practices <a name="14-best-practices"></a>

### 1. Always Use Context Manager

```python
# CORRECT - resources properly cleaned up
async with AsyncClient(transport=transport, base_url="http://test") as client:
    response = await client.get("/")

# INCORRECT - potential resource leak
client = AsyncClient(transport=transport, base_url="http://test")
response = await client.get("/")
```

### 2. Use Fixture for Common Setup

```python
# CORRECT - reusable fixture
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

async def test_something(client):
    response = await client.get("/")

# INCORRECT - repeated setup
async def test_something():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
```

### 3. Test Both Success and Error Cases

```python
async def test_create_item_success(client):
    response = await client.post("/items/", json={"name": "Foo", "price": 10.0})
    assert response.status_code == 201

async def test_create_item_invalid_data(client):
    response = await client.post("/items/", json={})
    assert response.status_code == 422

async def test_create_item_duplicate(client):
    await client.post("/items/", json={"name": "Foo", "price": 10.0})
    response = await client.post("/items/", json={"name": "Foo", "price": 10.0})
    assert response.status_code == 409
```

### 4. Use Descriptive Test Names

```python
async def test_get_item_returns_200_when_item_exists(client):
    ...

async def test_get_item_returns_404_when_item_not_found(client):
    ...

async def test_get_item_returns_422_when_id_is_negative(client):
    ...
```

### 5. Keep Tests Fast and Independent

```python
# BAD: Slow, depends on external service
async def test_with_real_api(client):
    response = await client.get("/proxy/external-api")

# GOOD: Mocked external dependency
@respx.mock
async def test_with_mocked_api(client):
    respx.get("https://external.com/api").mock(
        return_value=httpx.Response(200, json={"data": "test"})
    )
    response = await client.get("/proxy/external-api")
    assert response.status_code == 200
```

---

## Summary

| Concept | Key Point |
|---------|-----------|
| ASGITransport | Communicates with app via ASGI without server |
| base_url | Set once in fixture, use relative URLs in tests |
| Headers | Pass globally or per-request |
| Cookies | Managed automatically by client instance |
| Timeout | Configure globally or per-request |
| Streaming | Use `client.stream()` context manager |
| WebSocket | Use `client.websocket_connect()` context manager |
| File Upload | Use `files` parameter with tuples |
| respx | Mock external HTTP calls |
| Best Practice | Use fixtures, test success + error, descriptive names |
