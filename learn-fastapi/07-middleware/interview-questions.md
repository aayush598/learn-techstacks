# Middleware Interview Questions

## Table of Contents
1. [Fundamentals](#fundamentals)
2. [Middleware Order & Execution](#middleware-order--execution)
3. [CORSMiddleware](#corsmiddleware)
4. [Rate Limiting](#rate-limiting)
5. [Compression & Performance](#compression--performance)
6. [Security Headers](#security-headers)
7. [Middleware vs Dependencies](#middleware-vs-dependencies)
8. [Async Middleware & ASGI](#async-middleware--asgi)
9. [Middleware Testing](#middleware-testing)
10. [Production Middleware Stack](#production-middleware-stack)
11. [Scenario-Based Questions](#scenario-based-questions)

---

## Fundamentals

### Q1: What is middleware in FastAPI and how does the request lifecycle flow through it?
**Answer:** Middleware is a component that wraps every request and response flowing through the application. It operates in an "onion model" where the first middleware added is closest to the route handler, and the last middleware added is closest to the client. When a request arrives, it passes through middleware in reverse order of addition (last added runs first on request), hits the route handler, and then the response passes back through middleware in the opposite order. Each middleware can perform pre-processing (before `call_next`), post-processing (after `call_next`), and can short-circuit the chain by returning a response without calling `call_next`.

```python
@app.middleware("http")
async def my_middleware(request: Request, call_next):
    # Pre-processing (runs on request)
    start_time = time.time()

    response = await call_next(request)

    # Post-processing (runs on response)
    duration = time.time() - start_time
    response.headers["X-Process-Time"] = str(duration)
    return response
```

### Q2: What is the difference between ASGI and WSGI middleware?
**Answer:** ASGI middleware operates at the asynchronous protocol level, handling raw HTTP/WebSocket `scope`, `receive`, and `send` callables. It can process both HTTP and WebSocket connections, handle long-lived connections, and operate asynchronously. WSGI middleware is synchronous, designed for the WSGI interface (environ, start_response), and cannot handle WebSockets or async operations. FastAPI runs on ASGI (via Uvicorn), so it needs ASGI-compatible middleware.

The key architectural difference: ASGI middleware receives three arguments (`scope`, `receive`, `send`) and must handle the raw protocol. WSGI middleware receives two arguments (`environ`, `start_response`) and works with request/response pairs. ASGI middleware like `GZipMiddleware` can operate at the protocol level for maximum efficiency, while `BaseHTTPMiddleware` abstracts this into a simpler `dispatch` pattern at the cost of some performance and flexibility.

### Q3: What is BaseHTTPMiddleware and when should you avoid it?
**Answer:** `BaseHTTPMiddleware` is Starlette's convenience class for creating middleware with a simple `dispatch` method. It handles the ASGI protocol details and provides `Request` and `Response` objects. Use it for most middleware needs where simplicity matters more than raw performance.

**Avoid it when:**
- You need to handle WebSocket connections (it only handles HTTP)
- You need maximum throughput and minimum overhead (it creates `Request`/`Response` objects on every request)
- You need to modify the response body (it has limited support for streaming response modification)
- You need to access raw ASGI events (it abstracts them away)

**For these cases, write pure ASGI middleware:**

```python
class PureASGIMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def modified_send(message):
            if "headers" in message:
                message["headers"].append((b"x-custom", b"value"))
            await send(message)

        await self.app(scope, receive, modified_send)
```

### Q4: What happens if an exception is raised in middleware?
**Answer:** If an exception is raised in middleware and not caught, it propagates to the ASGI framework which returns a generic 500 error. The exception is logged but the response may not have proper headers, CORS headers, or structured error format. Always wrap `call_next` in try/except:

```python
@app.middleware("http")
async def safe_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        logger.exception(
            "middleware_error",
            path=request.url.path,
            method=request.method,
            exc_type=type(exc).__name__
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
            headers={"X-Request-ID": get_request_id()}
        )
```

**Key considerations:**
- Always return a proper `Response` object from exception handlers
- Include request context (request ID, path) in error responses for debugging
- Don't expose internal error details in production
- Consider using FastAPI's exception handlers for specific exception types as a complementary approach
- Catch specific exceptions when possible; broad `except Exception` should be the last resort

### Q5: Can middleware that only applies to specific routes be implemented?
**Answer:** Middleware applies to ALL routes by design — there is no built-in route filtering. For route-specific logic, **use dependencies instead** (`Depends()`). If you must use middleware for route-specific behavior, check the request path inside:

```python
@app.middleware("http")
async def conditional_middleware(request: Request, call_next):
    skip_paths = ["/health", "/metrics", "/docs"]
    if request.url.path in skip_paths:
        return await call_next(request)

    if request.url.path.startswith("/api/"):
        pass  # Apply custom logic

    return await call_next(request)
```

**Better patterns:**
- Use `app.include_router(router, dependencies=[Depends(some_dep)])` for per-router dependencies
- Create middleware classes that accept path patterns in constructor
- Use Starlette's `@app.route` middleware decorator for single-route middleware
- Consider that path checking adds overhead on every request even for non-matching paths

### Q6: What is the performance impact of adding multiple middleware?
**Answer:** Each middleware adds overhead because it wraps the entire request/response cycle. The overhead is per-request and includes:
- Function call overhead for each middleware layer
- Object creation (Request/Response objects for BaseHTTPMiddleware)
- Memory allocation for middleware state
- Potential blocking in async middleware

**Impact analysis:**
- **1-3 lightweight middleware**: Negligible (<1ms added)
- **5-10 middleware**: Measurable (1-5ms added, depends on implementation)
- **BaseHTTPMiddleware**: Higher overhead than pure ASGI (creates Request/Response objects)
- **Pure ASGI middleware**: Lowest overhead (operates at protocol level)

**Optimization strategies:**
- Combine related middleware into a single layer
- Use pure ASGI for performance-critical middleware
- Short-circuit early (return without calling `call_next` for rejected requests)
- Avoid heavy computation in middleware
- Profile middleware separately to identify bottlenecks
- Use dependencies for route-specific logic instead of path-checking middleware

### Q7: How do you add state to requests in middleware?
**Answer:** Use `request.state` to attach values that downstream handlers can access:

```python
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token:
        user = await verify_token(token)
        request.state.user = user
    request.state.request_id = str(uuid.uuid4())
    request.state.start_time = time.time()

    response = await call_next(request)
    return response

@app.get("/profile")
async def get_profile(request: Request):
    user = request.state.user  # Set by middleware
    return {"user": user}
```

**For state that needs to be accessed outside the request context** (e.g., in logging), use `contextvars.ContextVar`:

```python
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id")

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    token = request_id_var.set(request_id)
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
    finally:
        request_id_var.reset(token)
```

---

## Middleware Order & Execution

### Q8: How does middleware order work in FastAPI and why does it matter?
**Answer:** Middleware executes in **reverse order of addition**. The last middleware added runs first on the request path (outermost layer). This creates an onion model:

```python
app.add_middleware(MiddlewareA)  # Added first, closest to handler
app.add_middleware(MiddlewareB)  # Added second, outer layer
app.add_middleware(MiddlewareC)  # Added last, outermost layer
```

Request flow: **C → B → Handler → B → C → A → ... → Client**
Response flow: **... → A → C → B → Client**

**Order matters critically for:**
- **CORS**: Must be outermost (added last) so it handles preflight before other middleware
- **Security headers**: Should wrap authentication middleware
- **Rate limiting**: Should be early to reject requests before expensive processing
- **Logging**: Should be outermost to capture total request time
- **Authentication**: Should be after rate limiting, before route-specific middleware

Getting the order wrong can cause subtle bugs. For example, if CORS is inside authentication middleware, preflight OPTIONS requests might be rejected by auth before CORS headers are added, causing browser requests to fail.

### Q9: What happens when middleware A depends on middleware B's output but is added first?
**Answer:** Since middleware executes in reverse order of addition, if A is added first and B is added second, B runs first on the request path. If A sets `request.state.user` and B depends on it, B won't have access to it because B runs before A. This is a classic middleware ordering bug.

**Solution:** Ensure the middleware that produces state is added AFTER (outer to) the middleware that consumes it. Or use `contextvars` for request-scoped state that doesn't depend on execution order.

```python
# WRONG: B runs before A on the request path
app.add_middleware(StateProducer)  # Added first - runs second on request
app.add_middleware(StateConsumer)  # Added second - runs first on request

# CORRECT: B runs after A on the request path
app.add_middleware(StateConsumer)  # Added first - runs second on request
app.add_middleware(StateProducer)  # Added second - runs first on request
```

### Q10: Can middleware short-circuit the request chain?
**Answer:** Yes. Any middleware can return a `Response` without calling `call_next`, effectively stopping the request from reaching the handler or subsequent middleware. This is useful for:

- **Authentication rejection**: Return 401 without hitting the route
- **Rate limiting**: Return 429 when limits are exceeded
- **Caching**: Return cached responses directly
- **Maintenance mode**: Return 503 for all requests
- **Geographic blocking**: Reject requests from certain regions

```python
@app.middleware("http")
async def short_circuit_middleware(request: Request, call_next):
    if request.url.path == "/maintenance":
        return JSONResponse(
            status_code=503,
            content={"detail": "Under maintenance"},
            headers={"Retry-After": "3600"}
        )

    # Check cache before hitting handler
    cached = await redis.get(f"cache:{request.url.path}")
    if cached:
        return Response(content=cached, media_type="application/json")

    response = await call_next(request)
    return response
```

### Q11: How does middleware interact with FastAPI's exception handlers?
**Answer:** Middleware wraps the entire request/response cycle including exception handling. If a route raises an exception, FastAPI's exception handlers produce a response, and that response flows back through the middleware. However, if middleware itself raises an exception before calling `call_next`, exception handlers are never reached.

**Execution order for exceptions:**
1. Middleware pre-processing runs
2. `call_next` invokes the handler (or fails)
3. If handler raises → exception handler produces a response
4. If middleware raises → generic 500 (exception handler never runs)
5. Response flows back through middleware post-processing

```python
# This middleware catches ALL exceptions including those from handlers
@app.middleware("http")
async def catch_all_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException:
        raise  # Let FastAPI's exception handler deal with HTTPExceptions
    except Exception:
        return JSONResponse(status_code=500, content={"detail": "Internal error"})
```

---

## CORSMiddleware

### Q12: How do you configure CORS in FastAPI and what does each parameter do?
**Answer:**

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com", "https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["X-Request-ID", "X-Total-Count"],
    max_age=600,
)
```

- **`allow_origins`**: List of allowed origins. Browsers send `Origin` header; response must include `Access-Control-Allow-Origin` matching it.
- **`allow_credentials`**: Enables `Access-Control-Allow-Credentials: true`. Required for cookies, Authorization headers.
- **`allow_methods`**: Allowed HTTP methods. Controls `Access-Control-Allow-Methods` in preflight.
- **`allow_headers`**: Allowed request headers. Controls `Access-Control-Allow-Headers` in preflight.
- **`expose_headers`**: Headers the browser can read via JavaScript. Default only allows simple headers.
- **`max_age`**: How long (seconds) the browser caches preflight results. Reduces preflight requests.

### Q13: Can you use `allow_origins=["*"]` with `allow_credentials=True`?
**Answer:** No. The CORS specification explicitly forbids wildcard origins with credentials. Browsers will reject the response. When `allow_credentials=True`, `Access-Control-Allow-Origin` must be a specific origin, not `*`.

**Dynamic origin resolution pattern:**

```python
ALLOWED_ORIGINS = {"https://example.com", "https://app.example.com"}

@app.middleware("http")
async def dynamic_cors_middleware(request: Request, call_next):
    origin = request.headers.get("origin", "")
    if origin in ALLOWED_ORIGINS:
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Vary"] = "Origin"
        return response

    if request.method == "OPTIONS":
        return Response(status_code=403)

    return await call_next(request)
```

**Key rule:** Always set `Vary: Origin` when dynamically setting the origin header to prevent caching proxies from serving the wrong response.

### Q14: What triggers a CORS preflight request and how do you handle it?
**Answer:** A preflight OPTIONS request is triggered when:
- Method is not GET, HEAD, or POST
- POST with `Content-Type` other than `application/x-www-form-urlencoded`, `multipart/form-data`, or `text/plain`
- Request includes custom headers (anything not in the CORS-safelisted list)
- Request includes headers like `Authorization`, `X-Custom-Header`

**The preflight flow:**
1. Browser sends OPTIONS with `Origin`, `Access-Control-Request-Method`, `Access-Control-Request-Headers`
2. Server responds with allowed methods, headers, origin, and max-age
3. Browser sends the actual request if preflight succeeds

**CORSMiddleware handles this automatically.** For custom CORS logic, handle OPTIONS explicitly:

```python
@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response(status_code=200)
        origin = request.headers.get("origin")
        response.headers["Access-Control-Allow-Origin"] = get_allowed_origin(origin)
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        response.headers["Access-Control-Max-Age"] = "600"
        return response

    response = await call_next(request)
    origin = request.headers.get("origin")
    allowed = get_allowed_origin(origin)
    if allowed:
        response.headers["Access-Control-Allow-Origin"] = allowed
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Vary"] = "Origin"
    return response
```

### Q15: What does `expose_headers` do and when do you need it?
**Answer:** By default, browsers only expose "CORS-safelisted" response headers to JavaScript (`Cache-Control`, `Content-Language`, `Content-Type`, `Expires`, `Last-Modified`, `Pragma`). Custom headers like `X-Request-ID`, `X-Total-Count`, or `X-Pagination-Page` must be explicitly exposed:

```python
app.add_middleware(
    CORSMiddleware,
    expose_headers=["X-Request-ID", "X-Total-Count", "X-RateLimit-Remaining"]
)
```

Without `expose_headers`, JavaScript code like `response.headers.get("X-Request-ID")` returns `null` even though the header exists. This is a common gotcha when building SPAs that need custom headers for tracking, pagination, or rate limit information.

### Q16: Why does CORS not protect against server-side attacks?
**Answer:** CORS is a **browser-enforced** security mechanism. It only applies to cross-origin requests made by browsers. It does NOT protect against:
- **Server-to-server requests** (no browser involved, CORS headers ignored)
- **Direct API calls** with curl, Postman, or any HTTP client
- **Same-origin attacks** (CORS doesn't apply)
- **Server-side request forgery (SSRF)**

**Always implement proper server-side authentication and authorization** regardless of CORS configuration. CORS prevents malicious websites from making authenticated requests to your API using the user's cookies. It does NOT replace authentication.

### Q17: How do you handle CORS for a multi-tenant application?
**Answer:** Dynamic CORS middleware that determines the tenant from the request and applies the tenant's allowed origins:

```python
@app.middleware("http")
async def tenant_cors_middleware(request: Request, call_next):
    origin = request.headers.get("origin", "")
    tenant = get_tenant_from_origin(origin)

    if tenant and origin in tenant.allowed_origins:
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Vary"] = "Origin"
        return response

    if request.method == "OPTIONS":
        return Response(status_code=403)

    return await call_next(request)
```

**Cache tenant lookups** in Redis to avoid database hits on every request. Use a TTL-based cache that refreshes when tenant configuration changes.

---

## Rate Limiting

### Q18: What are the main rate limiting algorithms and when do you use each?
**Answer:**

| Algorithm | How It Works | Use Case |
|-----------|-------------|----------|
| **Fixed Window** | Count requests in fixed time windows (e.g., per minute). Simple but allows burst at window boundaries. | Simple APIs, low-stakes limiting |
| **Sliding Window Log** | Store timestamps of all requests. Count within sliding window. Precise but memory-heavy. | High-accuracy requirements |
| **Sliding Window Counter** | Blend current and previous window counts. Good balance of accuracy and efficiency. | Most production APIs |
| **Token Bucket** | Tokens added at fixed rate. Each request consumes a token. Allows controlled bursts. | APIs that allow short bursts |
| **Leaky Bucket** | Requests enter a queue (bucket). Processed at fixed rate. Smooths traffic. | Traffic shaping, queue-based systems |

**Production recommendation:** Sliding window counter for API rate limiting (good accuracy, low memory), token bucket for user-facing features (allows bursts).

### Q19: How do you implement Redis-based rate limiting and prevent race conditions?
**Answer:** Use Redis Lua scripts for atomic operations:

```lua
local key = KEYS[1]
local window = tonumber(ARGV[1])
local limit = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

redis.call("ZREMRANGEBYSCORE", key, 0, now - window)
local count = redis.call("ZCARD", key)

if count < limit then
    redis.call("ZADD", key, now, now .. math.random())
    redis.call("EXPIRE", key, window)
    return {1, limit - count - 1}
else
    return {0, 0}
end
```

```python
class RateLimiter:
    def __init__(self, redis_client, limit: int, window: int):
        self.redis = redis_client
        self.limit = limit
        self.window = window
        self.script = self.redis.register_script(LUA_SCRIPT)

    async def is_allowed(self, key: str) -> tuple[bool, int]:
        result = await self.script(
            keys=[f"ratelimit:{key}"],
            args=[self.window, self.limit, time.time()]
        )
        return bool(result[0]), result[1]
```

**Race condition prevention:** Redis Lua scripts execute atomically — no other command can interleave. Using `ZADD` + `ZCARD` in a script ensures the check-and-increment is atomic. Avoid the pattern of GET → check → SET (TOCTOU vulnerability).

### Q20: What headers should rate-limited responses include?
**Answer:**

```
HTTP/1.1 429 Too Many Requests
Retry-After: 30
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1692000030
X-RateLimit-Policy: 100;w=60
```

- **`Retry-After`**: Seconds until the client should retry (required on 429 responses)
- **`X-RateLimit-Limit`**: Maximum requests allowed in the window
- **`X-RateLimit-Remaining`**: Requests remaining in current window
- **`X-RateLimit-Reset`**: Unix timestamp when the window resets
- **`X-RateLimit-Policy`**: Describes the rate limit policy (draft-ietf-httpapi-ratelimit-headers standard)

Always include these on **every response** (not just 429s) so clients can proactively avoid hitting limits.

### Q21: How do you implement tiered rate limiting for different user subscription levels?
**Answer:**

```python
TIER_LIMITS = {
    "free": {"requests": 100, "window": 60},
    "pro": {"requests": 1000, "window": 60},
    "enterprise": {"requests": 10000, "window": 60},
}

@app.middleware("http")
async def tiered_rate_limit(request: Request, call_next):
    user = getattr(request.state, "user", None)

    if user:
        tier = user.subscription_tier
        key = f"user:{user.id}"
    else:
        tier = "free"
        key = f"ip:{request.client.host}"

    limits = TIER_LIMITS[tier]
    allowed, remaining = await limiter.is_allowed(key, limits)

    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"},
            headers={
                "Retry-After": str(limits["window"]),
                "X-RateLimit-Limit": str(limits["requests"]),
                "X-RateLimit-Remaining": "0",
            }
        )

    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(limits["requests"])
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    return response
```

**Advanced considerations:**
- Separate rate limits for different endpoint categories (auth: 5/min, reads: 100/min, writes: 50/min)
- Per-IP limits for unauthenticated requests
- Global system-wide rate limits to protect infrastructure
- Different limits for different HTTP methods (GET vs DELETE)

---

## Compression & Performance

### Q22: What is the difference between GZip and Brotli compression?
**Answer:**

| Feature | GZip | Brotli |
|---------|------|--------|
| Compression ratio | 25-35% smaller than uncompressed | 15-25% smaller than GZip |
| Speed (compression) | Fast | Slower at max compression |
| Speed (decompression) | Fast | Fast |
| Browser support | Universal | Modern browsers (96%+) |
| Static content | Good | Excellent (pre-compressed) |
| Dynamic content | Good | Good but CPU-heavy |

FastAPI's `GZipMiddleware` only supports GZip. For Brotli, use a custom middleware or configure at the Nginx/CDN level.

### Q23: When should you NOT compress responses?
**Answer:**
- **Already-compressed content**: Images (JPEG, PNG, WebP), videos (MP4), fonts (WOFF2), archives (ZIP, GZ)
- **Very small responses**: Under 150 bytes — compression adds overhead without benefit
- **High CPU usage**: When the server is CPU-bound, compression adds load
- **Sensitive data**: Compression can enable BREACH/CRIME attacks when combined with reflected user input
- **Range requests**: Partial content delivery (video streaming) should not be compressed
- **When a CDN handles compression**: Don't double-compress

### Q24: How do you implement request timeout middleware?
**Answer:**

```python
import asyncio
from starlette.responses import JSONResponse

@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    try:
        response = await asyncio.wait_for(call_next(request), timeout=30.0)
        return response
    except asyncio.TimeoutError:
        return JSONResponse(
            status_code=504,
            content={"detail": "Request timed out"},
            headers={"Retry-After": "30"}
        )
```

**Considerations:**
- Set different timeouts for different endpoints (health checks: 5s, reports: 120s)
- Clean up resources when timeout occurs (close DB connections, cancel tasks)
- Return `Retry-After` header so clients know when to retry
- Use `asyncio.shield` for critical cleanup that must complete even on timeout

---

## Security Headers

### Q25: What security headers should every FastAPI application include?
**Answer:**

```python
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'"

    if request.url.scheme == "https":
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"

    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers.pop("server", None)

    return response
```

**For APIs specifically:**
- `Cache-Control: no-store` for sensitive endpoints
- `X-Content-Type-Options: nosniff` to prevent MIME sniffing
- Don't expose server version information
- Use `Content-Security-Policy: default-src 'none'` for pure APIs

### Q26: How do you implement CSP (Content Security Policy) for a FastAPI app serving both API and frontend?
**Answer:** CSP is complex because it needs different policies for API responses vs. frontend HTML:

```python
CSP_DIRECTIVES = {
    "default-src": "'self'",
    "script-src": "'self' 'nonce-{random}'",
    "style-src": "'self' 'unsafe-inline'",
    "img-src": "'self' data: https://cdn.example.com",
    "connect-src": "'self' https://api.example.com",
    "frame-ancestors": "'none'",
}

@app.middleware("http")
async def csp_middleware(request: Request, call_next):
    response = await call_next(request)
    content_type = response.headers.get("content-type", "")

    if "text/html" in content_type:
        nonce = secrets.token_urlsafe(32)
        directives = "; ".join(
            f"{k} {v.replace('{random}', nonce)}"
            for k, v in CSP_DIRECTIVES.items()
        )
        response.headers["Content-Security-Policy"] = directives

    return response
```

---

## Middleware vs Dependencies

### Q27: When should you use middleware vs dependencies?
**Answer:**

| Use Case | Middleware | Dependencies |
|----------|-----------|-------------|
| Authentication (all routes) | Yes | No |
| Authentication (specific routes) | No | Yes |
| Request logging | Yes | No |
| CORS handling | Yes | No |
| Database session management | No | Yes |
| Rate limiting | Yes | No (too late) |
| Input validation | No | Yes |
| Feature flags | Either | Yes |
| Response transformation | Yes | No |
| Business logic | No | Yes |

**Rule of thumb:**
- **Cross-cutting concerns** that apply to ALL requests → **Middleware**
- **Route-specific logic** that varies per endpoint → **Dependencies**
- **Need to modify response headers** → **Middleware**
- **Need Pydantic model validation** → **Dependencies**

### Q28: What is the difference between middleware and exception handlers?
**Answer:** Middleware wraps the entire request/response cycle. Exception handlers are registered for specific exception types and produce responses when those exceptions are raised.

```python
# Middleware - wraps everything
@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Timing"] = str(time.time() - start)
    return response

# Exception handler - catches specific exceptions
@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": "User not found"})
```

**Key differences:**
- Middleware runs for ALL requests, even if no exception occurs
- Exception handlers only run when the specific exception is raised
- Middleware can modify both request and response
- Exception handlers only produce a response
- Use both together: middleware for logging/timing, exception handlers for error formatting

### Q29: How do you implement dependencies that behave like middleware?
**Answer:** Use dependency injection with yield for setup/teardown behavior:

```python
from fastapi import Depends, Request
import time

async def timing_dependency(request: Request):
    start = time.time()
    yield
    duration = time.time() - start
    logger.info("request_timing", path=request.url.path, duration_ms=duration * 1000)

async def auth_dependency(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401)
    user = await verify_token(token)
    request.state.user = user
    yield

@app.get("/protected", dependencies=[Depends(timing_dependency), Depends(auth_dependency)])
async def protected_route():
    return {"message": "Hello"}
```

---

## Async Middleware & ASGI

### Q30: What is the performance difference between async and sync middleware?
**Answer:** Async middleware integrates with FastAPI's async event loop and doesn't block other requests during I/O operations. Sync middleware runs in a thread pool, consuming a thread for the duration of blocking operations.

```python
# Async - doesn't block event loop
@app.middleware("http")
async def async_middleware(request: Request, call_next):
    data = await redis.get(f"cache:{request.url.path}")  # Non-blocking
    response = await call_next(request)
    return response

# Sync - blocks a thread during redis.get
@app.middleware("http")
def sync_middleware(request: Request, call_next):
    data = redis.get(f"cache:{request.url.path}")  # Blocks thread
    response = call_next(request)
    return response
```

**Impact:**
- Async: 1000 concurrent requests can share one thread
- Sync: 1000 concurrent requests need 1000 threads (or requests queue)
- With Uvicorn's default 1 thread per worker, sync middleware blocks ALL other requests during I/O

**Always use async middleware in FastAPI** unless the middleware does purely CPU-bound work with no I/O.

### Q31: How do you implement pure ASGI middleware for maximum performance?
**Answer:** Pure ASGI middleware operates at the protocol level without the overhead of `BaseHTTPMiddleware`:

```python
class MetricsASGIMiddleware:
    def __init__(self, app):
        self.app = app
        self.request_count = Counter("http_requests_total", "Total requests", ["method", "path", "status"])
        self.request_duration = Histogram("http_request_duration_seconds", "Request duration", ["method", "path"])

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        method = scope["method"]
        path = scope["path"]
        start = time.time()
        status_code = 200

        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message.get("status", 200)
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            duration = time.time() - start
            self.request_count.labels(method=method, path=path, status=status_code).inc()
            self.request_duration.labels(method=method, path=path).observe(duration)
```

**Performance advantage:** ~30-40% less overhead than `BaseHTTPMiddleware` for high-throughput endpoints because it avoids creating `Request`/`Response` objects on every request.

### Q32: Can middleware handle WebSocket connections?
**Answer:** `BaseHTTPMiddleware` only handles HTTP connections. For WebSocket middleware, you must use pure ASGI middleware that checks `scope["type"]`:

```python
class WebSocketAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            token = self._extract_token(scope)
            if not token:
                await send({"type": "websocket.close", "code": 1008})
                return
            user = await verify_ws_token(token)
            scope["user"] = user

        return await self.app(scope, receive, send)

    def _extract_token(self, scope):
        params = dict(parse_qsl(scope.get("query_string", b"").decode()))
        return params.get("token")
```

---

## Middleware Testing

### Q33: How do you unit test middleware in FastAPI?
**Answer:**

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

app = FastAPI()

@app.middleware("http")
async def add_header_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Custom"] = "test-value"
    return response

@app.get("/test")
async def test_endpoint():
    return {"message": "ok"}

client = TestClient(app)

def test_middleware_adds_header():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.headers["X-Custom"] == "test-value"
```

**Advanced testing patterns:**

```python
# Test middleware with dependency injection
def test_rate_limiting():
    with patch("app.middleware.redis") as mock_redis:
        mock_redis.incr.return_value = 101

        response = client.get("/api/data")
        assert response.status_code == 429
        assert "Retry-After" in response.headers

# Test middleware ordering
def test_middleware_order():
    response = client.options(
        "/api/data",
        headers={
            "Origin": "https://example.com",
            "Access-Control-Request-Method": "POST"
        }
    )
    assert response.headers.get("Access-Control-Allow-Origin") == "https://example.com"

# Test exception handling in middleware
def test_middleware_exception_handling():
    with patch("app.middleware.db") as mock_db:
        mock_db.connect.side_effect = ConnectionError("DB down")

        response = client.get("/api/data")
        assert response.status_code == 500
        assert "X-Request-ID" in response.headers
```

### Q34: How do you integration test middleware with external services?
**Answer:**

```python
import pytest
from httpx import AsyncClient, ASGITransport

@pytest.fixture
def app():
    app = FastAPI()
    app.add_middleware(RateLimitMiddleware, redis_url="redis://localhost:6379/15")
    return app

@pytest.mark.asyncio
async def test_rate_limiting_with_redis(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for i in range(100):
            response = await client.get("/api/data")
            assert response.status_code == 200

        response = await client.get("/api/data")
        assert response.status_code == 429
        assert "Retry-After" in response.headers
```

### Q35: How do you test middleware that modifies request bodies?
**Answer:**

```python
def test_body_modification_middleware():
    app = FastAPI()

    @app.middleware("http")
    async def modify_body(request: Request, call_next):
        body = await request.body()
        modified = body.replace(b"old", b"new")
        # In BaseHTTPMiddleware, the body is cached after first read
        response = await call_next(request)
        return response

    @app.post("/test")
    async def endpoint(request: Request):
        body = await request.body()
        return {"body": body.decode()}

    client = TestClient(app)
    response = client.post("/test", content=b"old value")
    assert response.status_code == 200
```

---

## Production Middleware Stack

### Q36: What is the recommended middleware stack for a production FastAPI application?
**Answer:**

```python
from fastapi import FastAPI

app = FastAPI()

# Order matters! Last added = first to process request

# 1. Security headers (outermost on response)
app.add_middleware(SecurityHeadersMiddleware)

# 2. Compression
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=500)

# 3. CORS (must be before auth to handle preflight)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Rate limiting
app.add_middleware(RateLimitMiddleware, redis_url=settings.REDIS_URL)

# 5. Request ID and logging (innermost, closest to handler)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(RequestLoggingMiddleware)
```

**Request processing order:** RequestID → Logging → RateLimit → CORS → SecurityHeaders → GZip → **Handler** → GZip → SecurityHeaders → CORS → RateLimit → Logging → RequestID

**Critical considerations:**
- CORS must be outermost to handle OPTIONS preflight before auth rejects it
- Rate limiting should be early to reject before expensive processing
- Request ID must be first on request path (outermost) so all downstream logs have it
- Compression should be last on response (innermost) so it compresses all output

### Q37: How do you implement a production-ready authentication middleware?
**Answer:**

```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import jwt

PUBLIC_PATHS = {"/health", "/metrics", "/docs", "/openapi.json", "/api/auth/login", "/api/auth/register"}

class AuthMiddleware:
    def __init__(self, app, secret_key: str):
        self.app = app
        self.secret_key = secret_key

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        path = scope["path"]

        if path in PUBLIC_PATHS or path.startswith("/static"):
            return await self.app(scope, receive, send)

        headers = dict(scope.get("headers", []))
        auth_header = headers.get(b"authorization", b"").decode()

        if not auth_header.startswith("Bearer "):
            response = JSONResponse(status_code=401, content={"detail": "Missing authorization header"})
            return await response(scope, receive, send)

        token = auth_header[7:]

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            scope["user"] = payload
        except jwt.ExpiredSignatureError:
            response = JSONResponse(status_code=401, content={"detail": "Token expired"})
            return await response(scope, receive, send)
        except jwt.InvalidTokenError:
            response = JSONResponse(status_code=401, content={"detail": "Invalid token"})
            return await response(scope, receive, send)

        return await self.app(scope, receive, send)
```

### Q38: How do you implement a circuit breaker pattern in middleware?
**Answer:**

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreakerMiddleware:
    def __init__(self, app, failure_threshold=5, recovery_timeout=30):
        self.app = app
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                return JSONResponse(
                    status_code=503,
                    content={"detail": "Service temporarily unavailable"},
                    headers={"Retry-After": str(self.recovery_timeout)}
                )

        try:
            response = await self.app(scope, receive, send)
            if response.status_code >= 500:
                self._record_failure()
            else:
                self._record_success()
            return response
        except Exception:
            self._record_failure()
            raise

    def _record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _record_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
        self.failure_count = 0
```

### Q39: How do you implement request deduplication in middleware?
**Answer:**

```python
import hashlib

class RequestDeduplicationMiddleware:
    def __init__(self, app, redis_client, ttl=5):
        self.app = app
        self.redis = redis_client
        self.ttl = ttl

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        if scope["method"] not in ("POST", "PUT", "PATCH"):
            return await self.app(scope, receive, send)

        body = await self._read_body(receive)
        user = scope.get("user", {}).get("sub", "anonymous")

        key_hash = hashlib.sha256(
            f"{scope['method']}:{scope['path']}:{body}:{user}".encode()
        ).hexdigest()

        dedup_key = f"dedup:{key_hash}"

        existing = await self.redis.get(dedup_key)
        if existing:
            return JSONResponse(
                status_code=409,
                content={"detail": "Duplicate request", "request_id": existing.decode()}
            )

        request_id = str(uuid.uuid4())
        await self.redis.setex(dedup_key, self.ttl, request_id)

        return await self.app(scope, receive, send)
```

---

## Scenario-Based Questions

### Q40: You need to add authentication to all routes except public ones. Should you use middleware or dependencies?
**Answer:** Use a **hybrid approach:**

1. **Middleware** for global token validation and user extraction — this ensures every request has a validated identity or is explicitly marked as public
2. **Dependencies** for role-based access control — different routes need different permissions

```python
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path in PUBLIC_PATHS:
        request.state.user = None
        return await call_next(request)

    token = request.headers.get("Authorization", "").removeprefix("Bearer ")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        request.state.user = payload
    except jwt.InvalidTokenError:
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})

    return await call_next(request)

def require_role(role: str):
    async def role_checker(request: Request):
        if request.state.user.get("role") != role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
    return role_checker

@app.get("/admin", dependencies=[Depends(require_role("admin"))])
async def admin_only():
    return {"data": "sensitive"}
```

### Q41: You notice high latency. How do you debug if it's caused by middleware?
**Answer:**

```python
@app.middleware("http")
async def debug_timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    response.headers["X-Timing-Total"] = f"{duration*1000:.2f}ms"

    if duration > 1.0:
        logger.warning("slow_request", path=request.url.path, duration_ms=duration * 1000)

    return response
```

**Debugging steps:**
1. Add timing middleware that logs time spent in each layer
2. Remove middleware one by one to isolate the bottleneck
3. Profile with `cProfile` or `py-spy` to identify CPU-bound middleware
4. Check for blocking I/O in async middleware (using `await` incorrectly)
5. Monitor memory usage — middleware that accumulates state causes memory pressure
6. Check Redis/network latency for middleware that calls external services
7. Use APM tools (Datadog, New Relic) that automatically instrument middleware

### Q42: You need to add request logging that includes the request body. What are the challenges?
**Answer:**

**Challenges:**
1. **Stream consumption**: Reading the body consumes the stream; the handler won't be able to read it again unless you provide a replacement
2. **Memory**: Large request bodies consume memory when fully read
3. **Performance**: Reading and logging adds latency to every request
4. **PII**: Request bodies often contain sensitive data (passwords, personal info)
5. **File uploads**: Multipart bodies are large and contain binary data
6. **Streaming**: Some handlers expect to read the body as a stream

**Solution:** Selectively log only specific endpoints, sanitize PII before logging, use pure ASGI middleware to provide replacement `receive` callables for modified bodies, and cap maximum body size for logging.

### Q43: How do you build a middleware stack for a multi-tenant SaaS application?
**Answer:**

```python
def create_app():
    app = FastAPI()

    # 1. Request ID (outermost)
    app.add_middleware(RequestIDMiddleware)
    # 2. Structured logging
    app.add_middleware(StructuredLoggingMiddleware)
    # 3. Security headers
    app.add_middleware(SecurityHeadersMiddleware)
    # 4. CORS (dynamic per tenant)
    app.add_middleware(TenantCORSMiddleware)
    # 5. Rate limiting (tiered by tenant plan)
    app.add_middleware(TenantRateLimitMiddleware)
    # 6. Tenant identification
    app.add_middleware(TenantIdentificationMiddleware)
    # 7. Authentication
    app.add_middleware(AuthenticationMiddleware)
    # 8. Compression
    app.add_middleware(GZipMiddleware, minimum_size=500)
    # 9. Request logging (innermost)
    app.add_middleware(AuditLoggingMiddleware)

    return app
```

**Tenant identification middleware:**
```python
class TenantIdentificationMiddleware:
    async def __call__(self, scope, receive, send):
        headers = dict(scope.get("headers", []))
        host = headers.get(b"host", b"").decode()
        tenant_id = host.split(".")[0] if "." in host else None

        if not tenant_id:
            tenant_id = headers.get(b"x-tenant-id", b"").decode()

        if not tenant_id:
            return JSONResponse(status_code=400, content={"detail": "Missing tenant"})(scope, receive, send)

        tenant = await get_tenant_config(tenant_id)  # Cached in Redis
        scope["tenant"] = tenant

        return await self.app(scope, receive, send)
```

### Q44: How do you implement feature flag middleware?
**Answer:**

```python
class FeatureFlagMiddleware:
    def __init__(self, app, flags_client):
        self.app = app
        self.flags = flags_client

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        user = scope.get("user", {})
        context = {
            "user_id": user.get("sub"),
            "plan": user.get("plan", "free"),
            "path": scope["path"],
        }

        enabled_features = {}
        for flag_name in ["new_checkout", "ml_search", "dark_mode"]:
            enabled_features[flag_name] = await self.flags.evaluate(
                flag_name, context, default=False
            )

        scope["features"] = enabled_features

        if scope["path"] == "/api/new-checkout" and not enabled_features.get("new_checkout"):
            response = JSONResponse(status_code=404, content={"detail": "Not found"})
            return await response(scope, receive, send)

        return await self.app(scope, receive, send)
```

### Q45: How do you implement A/B testing middleware?
**Answer:**

```python
import hashlib

VARIANTS = {
    "checkout_flow": ["control", "new_checkout", "simplified_checkout"],
    "search_algorithm": ["control", "ml_ranked"],
}

class ABTestMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        headers = dict(scope.get("headers", []))
        user_id = headers.get(b"x-user-id", b"").decode() or self._get_or_create_user(scope)

        variants = {}
        for test_name, options in VARIANTS.items():
            hash_val = int(hashlib.md5(f"{user_id}:{test_name}".encode()).hexdigest(), 16)
            variant_idx = hash_val % len(options)
            variants[test_name] = options[variant_idx]

        scope["ab_variants"] = variants

        return await self.app(scope, receive, send)
```

### Q46: How do you implement a production middleware stack that handles all cross-cutting concerns?
**Answer:** A complete production stack with all concerns properly ordered:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

def create_production_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url=None,
    )

    # Layer 1: Request ID (outermost - must be first on request)
    app.add_middleware(RequestIDMiddleware)

    # Layer 2: Structured logging
    app.add_middleware(
        StructuredLoggingMiddleware,
        log_request_body=settings.ENVIRONMENT == "development",
    )

    # Layer 3: Security headers
    app.add_middleware(SecurityHeadersMiddleware, csp_policy="default-src 'self'")

    # Layer 4: CORS (must handle preflight before auth)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-RateLimit-Remaining"],
        max_age=600,
    )

    # Layer 5: Rate limiting
    app.add_middleware(
        RateLimitMiddleware,
        redis_url=settings.REDIS_URL,
        default_limit=100,
        default_window=60,
    )

    # Layer 6: Compression
    app.add_middleware(GZipMiddleware, minimum_size=500)

    # Layer 7: Request timeout
    app.add_middleware(TimeoutMiddleware, timeout_seconds=30)

    # Layer 8: Error tracking
    app.add_middleware(SentryMiddleware)

    return app
```

### Q47: How do you implement request/response transformation middleware?
**Answer:**

```python
class RequestTransformationMiddleware:
    def __init__(self, app, transforms=None):
        self.app = app
        self.transforms = transforms or []

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        for transform in self.transforms:
            scope = await transform.transform_request(scope)

        async def transformed_send(message):
            if message["type"] == "http.response.start":
                for transform in self.transforms:
                    message = await transform.transform_response_start(message)
            elif message["type"] == "http.response.body":
                for transform in self.transforms:
                    message = await transform.transform_response_body(message)
            await send(message)

        await self.app(scope, receive, transformed_send)
```

### Q48: How do you handle CORS in a microservices architecture with an API gateway?
**Answer:** In a microservices architecture, CORS should be handled at the **API gateway** level, not in individual services. The gateway is the single entry point for browsers, so it handles preflight requests and adds CORS headers before forwarding to internal services. Internal services don't need CORS because they communicate server-to-server.

```python
# API Gateway middleware
@app.middleware("http")
async def gateway_cors(request: Request, call_next):
    origin = request.headers.get("origin", "")
    tenant = resolve_tenant(origin)

    if request.method == "OPTIONS":
        return Response(
            status_code=204,
            headers={
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Authorization, Content-Type, X-Tenant-ID",
                "Access-Control-Max-Age": "600",
                "Vary": "Origin",
            }
        )

    response = await call_next(request)
    if origin in tenant.allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Vary"] = "Origin"
    return response
```

### Q49: How do you implement idempotency middleware for payment endpoints?
**Answer:**

```python
class IdempotencyMiddleware:
    def __init__(self, app, redis_client, ttl=86400):
        self.app = app
        self.redis = redis_client
        self.ttl = ttl

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["method"] not in ("POST", "PUT", "PATCH"):
            return await self.app(scope, receive, send)

        headers = dict(scope.get("headers", []))
        idempotency_key = headers.get(b"idempotency-key", b"").decode()

        if not idempotency_key:
            return await self.app(scope, receive, send)

        existing = await self.redis.get(f"idempotent:{idempotency_key}")
        if existing:
            cached = json.loads(existing)
            return JSONResponse(
                status_code=cached["status_code"],
                content=cached["body"],
                headers={"Idempotent-Replayed": "true"}
            )

        response = await self.app(scope, receive, send)

        await self.redis.setex(
            f"idempotent:{idempotency_key}",
            self.ttl,
            json.dumps({"status_code": response.status_code, "body": "cached"})
        )

        return response
```

### Q50: How do you implement request body caching middleware for retry scenarios?
**Answer:**

```python
@app.middleware("http")
async def body_caching_middleware(request: Request, call_next):
    if request.method in ("POST", "PUT", "PATCH"):
        body = await request.body()
        # Cache the body keyed by request ID for retry scenarios
        request_id = request.headers.get("X-Request-ID", "")
        if request_id:
            await redis.setex(f"body:{request_id}", 300, body)

    response = await call_next(request)
    return response
```
