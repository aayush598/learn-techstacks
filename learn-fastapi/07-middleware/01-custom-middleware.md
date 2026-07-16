# Custom Middleware in FastAPI

## Table of Contents
1. [What is Middleware?](#what-is-middleware)
2. [BaseHTTPMiddleware](#basehttpmiddleware)
3. [Custom Middleware Classes](#custom-middleware-classes)
4. [Async Middleware](#async-middleware)
5. [Middleware with State](#middleware-with-state)
6. [Middleware Order](#middleware-order)
7. [Middleware for Logging](#middleware-for-logging)
8. [Middleware for Timing](#middleware-for-timing)
9. [Request ID Injection](#request-id-injection)
10. [Middleware Exceptions](#middleware-exceptions)
11. [Middleware vs Dependency Injection](#middleware-vs-dependency-injection)
12. [Best Practices](#best-practices)
13. [Interview Questions](#interview-questions)

---

## What is Middleware?

Middleware is a layer that sits between the client and the application, intercepting every request and response. It can modify the request before it reaches the route handler, modify the response before it's sent back, or perform actions like logging, authentication, and compression.

### How Middleware Works

```
Client → Middleware 1 → Middleware 2 → ... → Route Handler
Client ← Middleware 1 ← Middleware 2 ← ... ← Route Handler
```

Each middleware can:
- **Pre-process** the request (before the route handler)
- **Post-process** the response (after the route handler)
- **Short-circuit** the request (return a response without calling the route handler)
- **Pass the request** to the next middleware or the route handler

### ASGI vs WSGI Middleware

FastAPI uses ASGI (Asynchronous Server Gateway Interface). This means:

- **ASGI middleware** operates at a lower level and handles raw HTTP/WebSocket messages
- **WSGI middleware** (like from Flask) cannot be used directly in FastAPI
- ASGI middleware is inherently async, making it more efficient

---

## BaseHTTPMiddleware

FastAPI provides `BaseHTTPMiddleware` as the easiest way to create custom middleware.

### Basic Structure

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import FastAPI

app = FastAPI()

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Pre-processing: runs before the route handler
        response = await call_next(request)
        # Post-processing: runs after the route handler
        return response

app.add_middleware(CustomMiddleware)
```

### Request Object Access

Inside the middleware, the `request` object provides access to:

```python
class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # URL information
        url = request.url              # Full URL
        path = request.url.path        # e.g., "/api/users"
        query = request.url.query      # e.g., "page=1&limit=10"

        # Method
        method = request.method        # GET, POST, PUT, DELETE, etc.

        # Headers
        content_type = request.headers.get("content-type")
        auth = request.headers.get("authorization")

        # Client info
        client_ip = request.client.host
        client_port = request.client.port

        # Cookies
        session_id = request.cookies.get("session_id")

        # Scope (raw ASGI info)
        scope = request.scope

        response = await call_next(request)
        return response
```

### Full Example: Simple Logging Middleware

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)
app = FastAPI()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        logger.info(f"Request: {request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response

app.add_middleware(LoggingMiddleware)
```

---

## Custom Middleware Classes

### Middleware That Modifies Request Headers

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class AddHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Add a custom header to the incoming request
        request.scope["headers"].append(
            (b"x-custom-header", b"custom-value")
        )
        response = await call_next(request)
        return response
```

### Middleware That Modifies Response Headers

```python
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000"
        return response
```

### Middleware That Blocks Requests

```python
from starlette.responses import JSONResponse

class BlockBotsMiddleware(BaseHTTPMiddleware):
    BLOCKED_AGENTS = ["badbot", "malicious-crawler", "scanner"]

    async def dispatch(self, request: Request, call_next) -> Response:
        user_agent = request.headers.get("user-agent", "").lower()
        for agent in self.BLOCKED_AGENTS:
            if agent in user_agent:
                return JSONResponse(
                    status_code=403,
                    content={"detail": "Access denied"}
                )
        response = await call_next(request)
        return response
```

### Middleware with Configuration

```python
class ConfigurableMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, header_name: str = "X-Custom", header_value: str = "default"):
        super().__init__(app)
        self.header_name = header_name
        self.header_value = header_value

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers[self.header_name] = self.header_value
        return response

# Usage
app.add_middleware(ConfigurableMiddleware, header_name="X-API-Version", header_value="v2")
```

---

## Async Middleware

### Why Async Matters

Since FastAPI is built on Starlette (an async framework), middleware should be async for maximum performance. Synchronous middleware blocks the event loop.

### Async vs Sync Middleware

```python
# BAD: Sync middleware (blocks the event loop)
class SyncMiddleware(BaseHTTPMiddleware):
    def dispatch(self, request: Request, call_next) -> Response:
        # This blocks the entire event loop!
        import time
        time.sleep(1)
        response = call_next(request)
        return response

# GOOD: Async middleware (non-blocking)
class AsyncMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # This doesn't block the event loop
        import asyncio
        await asyncio.sleep(1)
        response = await call_next(request)
        return response
```

### Pure ASGI Middleware (Higher Performance)

For maximum performance, you can write pure ASGI middleware without `BaseHTTPMiddleware`:

```python
from starlette.types import ASGIApp, Receive, Send, Scope, Message

class PureASGIMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Pre-processing
        print(f"Request: {scope['method']} {scope['path']}")

        # Call the next app
        await self.app(scope, receive, send)

        # Note: Post-processing is harder with pure ASGI
        # because responses are sent via the send callable

# Usage
app.add_middleware(PureASGIMiddleware)
```

### When to Use Pure ASGI vs BaseHTTPMiddleware

| Feature | BaseHTTPMiddleware | Pure ASGI |
|---------|-------------------|-----------|
| Ease of use | High | Low |
| Access to full response | Yes | Complex |
| Performance | Good | Better |
| Response streaming | Limited | Full control |
| Body modification | Yes | Manual |

---

## Middleware with State

### Using `app.state`

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class StatefulMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Access app state
        request.app.state.request_count += 1
        response = await call_next(request)
        return response

@app.on_event("startup")
async def init_state():
    app.state.request_count = 0

app.add_middleware(StatefulMiddleware)
```

### Using `request.state`

```python
class RequestStateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Set per-request state
        request.state.start_time = time.time()
        request.state.user_id = None  # Will be set by auth middleware

        response = await call_next(request)
        return response

@app.get("/profile")
async def get_profile(request: Request):
    # Access middleware-set state
    user_id = request.state.user_id
    return {"user_id": user_id}
```

### Middleware That Passes Data to Handlers

```python
import uuid

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request.state.correlation_id = str(uuid.uuid4())
        request.state.start_time = time.time()
        response = await call_next(request)
        return response

@app.get("/api/data")
async def get_data(request: Request):
    correlation_id = request.state.correlation_id
    duration = time.time() - request.state.start_time
    return {"correlation_id": correlation_id, "duration": duration}
```

---

## Middleware Order

The order in which middleware is added determines the order in which they execute.

### Execution Order

```python
from starlette.middleware.base import BaseHTTPMiddleware

class MiddlewareA(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        print("A - Before")
        response = await call_next(request)
        print("A - After")
        return response

class MiddlewareB(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        print("B - Before")
        response = await call_next(request)
        print("B - After")
        return response

class MiddlewareC(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        print("C - Before")
        response = await call_next(request)
        print("C - After")
        return response

# The LAST added middleware runs FIRST
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
app.add_middleware(MiddlewareC)

# Output for a request:
# C - Before
# B - Before
# A - Before
# [Route handler executes]
# A - After
# B - After
# C - After
```

### Typical Middleware Order

```python
# 1. Exception handling (outermost)
app.add_middleware(ExceptionHandlingMiddleware)
# 2. CORS (must be before authentication)
app.add_middleware(CORSMiddleware, ...)
# 3. Compression
app.add_middleware(GZipMiddleware)
# 4. Request ID / Logging
app.add_middleware(RequestIDMiddleware)
# 5. Authentication (innermost)
app.add_middleware(AuthMiddleware)
```

### Visual Representation

```
Request → [Exception] → [CORS] → [Compression] → [Logging] → [Auth] → Route
Response ← [Exception] ← [CORS] ← [Compression] ← [Logging] ← [Auth] ← Route
```

---

## Middleware for Logging

### Comprehensive Logging Middleware

```python
import time
import logging
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("app.access")
error_logger = logging.getLogger("app.error")

class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())
        start_time = time.time()

        # Log request
        logger.info(
            "request_started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "query": str(request.url.query),
                "client_ip": request.client.host,
                "user_agent": request.headers.get("user-agent"),
            }
        )

        # Add request ID to response headers
        request.state.request_id = request_id

        try:
            response = await call_next(request)
            duration = time.time() - start_time

            logger.info(
                "request_completed",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2),
                }
            )

            response.headers["X-Request-ID"] = request_id
            return response

        except Exception as e:
            duration = time.time() - start_time
            error_logger.exception(
                "request_failed",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "duration_ms": round(duration * 1000, 2),
                }
            )
            raise
```

---

## Middleware for Timing

### Response Time Middleware

```python
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        # Add timing header
        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        # Log slow requests
        if process_time > 1.0:
            logger.warning(
                f"Slow request: {request.method} {request.url.path} "
                f"took {process_time:.2f}s"
            )

        return response
```

### Detailed Timing with Breakdown

```python
class DetailedTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        timings = {}

        # Time before middleware chain
        timings["start"] = time.perf_counter()
        timings["method"] = request.method
        timings["path"] = request.url.path

        response = await call_next(request)

        timings["end"] = time.perf_counter()
        timings["total_ms"] = round(
            (timings["end"] - timings["start"]) * 1000, 2
        )

        response.headers["Server-Timing"] = (
            f"total;dur={timings['total_ms']}"
        )
        return response
```

---

## Request ID Injection

### UUID-Based Request IDs

```python
import uuid
from contextvars import ContextVar

# Context variable for accessing request ID anywhere in the app
request_id_var: ContextVar[str] = ContextVar("request_id", default="")

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Use client-provided ID or generate new one
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Set in context variable
        request_id_var.set(request_id)
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

# Usage in route handlers or services
@app.get("/api/users")
async def get_users():
    rid = request_id_var.get()
    logger.info(f"[{rid}] Fetching users")
    return {"users": []}
```

### Using Context Variables in Logging

```python
import logging

class RequestIDFilter(logging.Filter):
    def __init__(self):
        super().__init__()

    def filter(self, record):
        record.request_id = request_id_var.get("-")
        return True

# Configure logging
handler = logging.StreamHandler()
handler.addFilter(RequestIDFilter())
formatter = logging.Formatter(
    "%(asctime)s [%(request_id)s] %(levelname)s %(name)s: %(message)s"
)
handler.setFormatter(formatter)
logging.root.addHandler(handler)
logging.root.setLevel(logging.INFO)
```

---

## Middleware Exceptions

### Handling Exceptions in Middleware

```python
from starlette.responses import JSONResponse

class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
            return response
        except ValueError as e:
            return JSONResponse(
                status_code=400,
                content={"detail": f"Bad request: {str(e)}"}
            )
        except PermissionError as e:
            return JSONResponse(
                status_code=403,
                content={"detail": "Permission denied"}
            )
        except Exception as e:
            logger.exception("Unhandled exception in middleware")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )
```

### Catching HTTPException

```python
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

class HTTPExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
            return response
        except StarletteHTTPException as e:
            # Convert to JSON response
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "detail": e.detail,
                    "path": request.url.path,
                }
            )
```

### Middleware That Raises Exceptions

```python
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip auth for public routes
        if request.url.path in ["/health", "/docs", "/openapi.json"]:
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Missing auth token")

        try:
            user = decode_token(token)
            request.state.user = user
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)
```

---

## Middleware vs Dependency Injection

### When to Use Middleware

```python
# Middleware is best for:
# 1. Cross-cutting concerns that apply to ALL requests
# 2. Request/response transformation
# 3. Logging and monitoring
# 4. CORS
# 5. Compression
# 6. Request ID injection

# Example: Logging ALL requests
class GlobalLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        log_request(request)
        response = await call_next(request)
        log_response(response)
        return response
```

### When to Use Dependencies

```python
# Dependencies are best for:
# 1. Per-route or per-router logic
# 2. Authentication (when different routes need different auth)
# 3. Database sessions
# 4. Business logic injection

# Example: Per-route authentication
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    return user

@app.get("/admin/users")
async def admin_only(user = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(403)
    return {"users": []}

@app.get("/profile")
async def profile(user = Depends(get_current_user)):
    return {"user": user}
```

### Comparison Table

| Feature | Middleware | Dependency Injection |
|---------|-----------|---------------------|
| Scope | All requests | Per-route/endpoint |
| Access to request | Yes | Yes (via Request object) |
| Can short-circuit | Yes | Yes (raise exception) |
| Performance overhead | Every request | Only when route uses it |
| Complexity | Higher | Lower |
| Reusability | Global | Per-route |
| Response modification | Yes | No |

---

## Best Practices

### 1. Keep Middleware Lightweight

```python
# BAD: Heavy computation in middleware
class HeavyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Don't do expensive operations here
        data = await fetch_all_data_from_db()  # Bad!
        response = await call_next(request)
        return response

# GOOD: Minimal middleware
class LightweightMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request.state.start_time = time.time()
        response = await call_next(request)
        return response
```

### 2. Always Use Async

```python
# BAD
class SyncMiddleware(BaseHTTPMiddleware):
    def dispatch(self, request, call_next):
        return call_next(request)

# GOOD
class AsyncMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        return await call_next(request)
```

### 3. Handle Exceptions Properly

```python
class SafeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.exception(f"Error in middleware: {e}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )
```

### 4. Don't Modify Response Body in BaseHTTPMiddleware

```python
# BaseHTTPMiddleware doesn't handle streaming responses well
# For response body modification, consider:
# 1. Using pure ASGI middleware
# 2. Using response background tasks
# 3. Using a different approach entirely
```

### 5. Add Middleware Before Routes

```python
app = FastAPI()

# Middleware first
app.add_middleware(LoggingMiddleware)
app.add_middleware(CORSMiddleware, ...)

# Then routes
@app.get("/api/users")
async def get_users():
    return {"users": []}
```

### 6. Use contextvars for Cross-Middleware Communication

```python
from contextvars import ContextVar

user_var: ContextVar[Optional[User]] = ContextVar("user", default=None)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        token = request.headers.get("Authorization")
        if token:
            user = decode_token(token)
            user_var.set(user)
        response = await call_next(request)
        return response

async def get_current_user():
    return user_var.get()
```

---

## Interview Questions

### Q1: What is middleware in FastAPI?
**Answer:** Middleware is a component that sits between the client and the route handler, intercepting every request and response. It can perform pre-processing (before the handler) and post-processing (after the handler), such as logging, authentication, compression, and CORS handling.

### Q2: What is the difference between BaseHTTPMiddleware and pure ASGI middleware?
**Answer:** `BaseHTTPMiddleware` provides a simpler, more intuitive API for writing middleware with access to `call_next`. Pure ASGI middleware operates at a lower level using `scope`, `receive`, and `send` callables. Pure ASGI is more performant but harder to write, especially for response modification.

### Q3: Why should middleware be async in FastAPI?
**Answer:** FastAPI runs on an async event loop (uvicorn). Synchronous middleware blocks the entire event loop, preventing other requests from being processed. Async middleware allows the event loop to handle other tasks while waiting for I/O operations.

### Q4: How does middleware order work in FastAPI?
**Answer:** Middleware is executed in reverse order of addition. The last middleware added runs first on the request path. On the response path, it runs last. This creates a "onion" model where the first middleware added is closest to the route handler.

### Q5: Can middleware modify the request body?
**Answer:** Yes, but with limitations. You can read the body with `await request.body()` but modifying it is tricky because the body is a stream. For most cases, use request headers or state to pass data instead.

### Q6: What's the difference between middleware and dependencies?
**Answer:** Middleware applies to ALL requests globally and can modify both request and response. Dependencies are per-route, injected via `Depends()`, and are better for business logic like authentication and database sessions.

### Q7: How do you inject a request ID in FastAPI middleware?
**Answer:** Generate a UUID in middleware, store it in `request.state` and a `ContextVar`, add it to response headers, and use it in logging via a logging Filter.

### Q8: What happens if an exception is raised in middleware?
**Answer:** If not caught, it propagates up and returns a 500 error. You should wrap `call_next` in try/except to handle exceptions gracefully and return appropriate error responses.

### Q9: Can middleware short-circuit the request?
**Answer:** Yes. Instead of calling `await call_next(request)`, return a `Response` directly (e.g., `JSONResponse(status_code=401)`). The request never reaches the route handler.

### Q10: How do you access middleware state in route handlers?
**Answer:** Use `request.state` to set values in middleware and access them in handlers. Alternatively, use `ContextVar` for cross-cutting state that doesn't depend on the request object.

### Q11: What is the performance impact of middleware?
**Answer:** Each middleware adds overhead because it wraps the entire request/response cycle. Keep middleware lightweight, avoid heavy computation, and prefer ASGI middleware for performance-critical paths.

### Q12: When should you NOT use middleware?
**Answer:** When the logic only applies to specific routes (use dependencies), when it needs database access (use dependencies), when it's route-specific business logic (use dependencies).

### Q13: How do you test middleware in FastAPI?
**Answer:** Use `TestClient` with the app that includes the middleware. Test that expected headers are added, responses have correct status codes, and middleware behavior is correct for different request types.

### Q14: Can middleware handle WebSocket connections?
**Answer:** `BaseHTTPMiddleware` only handles HTTP. For WebSocket middleware, use pure ASGI middleware that checks `scope["type"] == "websocket"`.

### Q15: How do you add middleware that depends on settings?
**Answer:** Pass settings as constructor arguments to the middleware class, or use `app.state` to store settings after app initialization.

### Q16: What is ContextVar and why use it in middleware?
**Answer:** `ContextVar` is a Python feature for storing context-local variables. It's useful in middleware to pass data (like request ID, current user) to any part of the application without threading it through function parameters.

### Q17: How does exception handling middleware differ from @app.exception_handler?
**Answer:** Exception handlers in FastAPI are specific to certain exception types. Exception handling middleware catches ALL exceptions and provides a global catch-all. Use exception handlers for specific exceptions and middleware for cross-cutting exception handling.

### Q18: Can middleware interact with dependency injection?
**Answer:** Not directly. Middleware runs before the dependency injection system. However, middleware can set values in `request.state` that dependencies can later access via the `Request` object.

### Q19: What are the common mistakes with BaseHTTPMiddleware?
**Answer:** Using sync functions instead of async, not catching exceptions, modifying the response body (limited support), forgetting to `await call_next`, and not handling streaming responses properly.

### Q20: How do you implement rate limiting in middleware?
**Answer:** Use a counter (in-memory or Redis) keyed by client IP or API key. Check the counter on each request, increment it, and return 429 if the limit is exceeded. Implement with sliding window or token bucket algorithm.
