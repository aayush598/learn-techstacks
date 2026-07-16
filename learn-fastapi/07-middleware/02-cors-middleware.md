# CORS Middleware in FastAPI

## Table of Contents
1. [What is CORS?](#what-is-cors)
2. [Why CORS Exists](#why-cors-exists)
3. [CORSMiddleware Setup](#corsmiddleware-setup)
4. [allow_origins](#allow_origins)
5. [allow_methods](#allow_methods)
6. [allow_headers](#allow_headers)
7. [allow_credentials](#allow_credentials)
8. [expose_headers](#expose_headers)
9. [Preflight Requests](#preflight-requests)
10. [CORS Best Practices](#cors-best-practices)
11. [Security Implications](#security-implications)
12. [Production CORS Configuration](#production-cors-configuration)
13. [Common CORS Errors](#common-cors-errors)
14. [Interview Questions](#interview-questions)

---

## What is CORS?

CORS (Cross-Origin Resource Sharing) is a security mechanism implemented in browsers that controls which origins can access resources from a different origin. An "origin" is the combination of protocol, hostname, and port.

### Same-Origin vs Cross-Origin

```python
# Same origin (all three must match):
# https://example.com:443
# https://example.com:443/api/users

# Different origins:
# https://example.com → https://api.example.com (different hostname)
# https://example.com → http://example.com (different protocol)
# https://example.com → https://example.com:8080 (different port)
```

### How CORS Works

1. Browser makes a **simple request** (GET, HEAD, POST with certain content types)
2. Browser adds `Origin` header automatically
3. Server responds with `Access-Control-Allow-Origin` header
4. Browser checks if the origin is allowed

For **preflight requests** (complex requests):
1. Browser sends an OPTIONS request first
2. Server responds with allowed methods, headers, etc.
3. Browser then sends the actual request

---

## Why CORS Exists

CORS exists to prevent **Cross-Site Request Forgery (CSRF)** and protect users from malicious websites making unauthorized requests to other services on behalf of the user.

### Without CORS

```javascript
// A malicious site could do this without CORS:
fetch("https://bank.com/api/transfer", {
    method: "POST",
    body: JSON.stringify({ to: "attacker", amount: 10000 }),
    credentials: "include"  // sends cookies
});
// The browser would send this request WITH the user's cookies
// Bank server would see valid session and process the transfer
```

### With CORS

```javascript
// CORS blocks this because:
// 1. Origin is "malicious-site.com"
// 2. Bank server doesn't include that origin in Access-Control-Allow-Origin
// 3. Browser blocks the response
```

---

## CORSMiddleware Setup

### Basic Setup

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/users")
async def get_users():
    return {"users": ["Alice", "Bob"]}
```

### How FastAPI Handles It

FastAPI uses Starlette's `CORSMiddleware` under the hood. It:

1. Intercepts all requests
2. For simple requests: adds CORS headers to the response
3. For preflight requests: responds with CORS headers without reaching the route
4. Handles OPTIONS method automatically

### Adding Middleware to Existing App

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware should be added early
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://app.example.com",
        "https://admin.example.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

---

## allow_origins

### Specific Origins

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://app.example.com",
        "https://admin.example.com",
        "https://staging.example.com",
    ],
)
```

### Wildcard Origin

```python
# Allow ALL origins (NOT recommended for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)
```

**Warning:** `allow_origins=["*"]` with `allow_credentials=True` is NOT allowed by the CORS specification. Browsers will reject the response.

### Origin Validation Function

```python
from starlette.middleware.cors import CORSMiddleware

ALLOWED_ORIGINS = {
    "https://app.example.com",
    "https://admin.example.com",
}

def is_origin_allowed(origin: str) -> bool:
    # You can add dynamic logic here
    if origin in ALLOWED_ORIGINS:
        return True
    # Allow subdomains
    if origin.endswith(".example.com"):
        return True
    return False

# Use the custom middleware for dynamic origin validation
class DynamicCORSMiddleware(CORSMiddleware):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

# Or configure origins dynamically at startup
@app.on_event("startup")
async def configure_cors():
    # Dynamic origins based on environment
    origins = ["https://app.example.com"]
    if settings.ENVIRONMENT == "development":
        origins.append("http://localhost:3000")
    app.state.allowed_origins = origins
```

### Environment-Based Origins

```python
import os

def get_allowed_origins() -> list[str]:
    env = os.getenv("ENVIRONMENT", "production")
    if env == "development":
        return [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
        ]
    elif env == "staging":
        return ["https://staging.example.com"]
    else:
        return [
            "https://app.example.com",
            "https://admin.example.com",
        ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## allow_methods

### Default Methods

By default, `CORSMiddleware` allows these methods for simple requests:
- `GET`
- `POST`
- `HEAD`

### Allowing Specific Methods

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
)
```

### Allowing All Methods

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_methods=["*"],  # Allows all methods
)
```

### Custom Methods

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "CUSTOM"],
)
```

---

## allow_headers

### Default Headers

By default, only these headers are allowed:
- `Accept`
- `Accept-Language`
- `Content-Language`
- `Content-Type`

### Allowing Specific Headers

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Custom-Header",
        "X-API-Key",
        "X-Request-ID",
    ],
)
```

### Allowing All Headers

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_headers=["*"],
)
```

---

## allow_credentials

### What Credentials Include

When `allow_credentials=True`, the browser includes:
- Cookies
- Authorization headers
- TLS client certificates

### Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,  # Important for cookie-based auth
)
```

### Limitations

```python
# CANNOT use "*" origin with credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # ❌ Won't work with credentials
    allow_credentials=True,        # ❌ Browser will reject
)

# Must specify explicit origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],  # ✅ Works with credentials
    allow_credentials=True,
)
```

### JavaScript Side

```javascript
// Frontend must set credentials
fetch("https://api.example.com/users", {
    credentials: "include"  // Sends cookies
});

// Or for axios
axios.get("https://api.example.com/users", {
    withCredentials: true
});
```

---

## expose_headers

### Why Expose Headers

By default, browsers only expose these response headers to JavaScript:
- `Cache-Control`
- `Content-Language`
- `Content-Length`
- `Content-Type`
- `Expires`
- `Last-Modified`
- `Pragma`

Any custom headers need to be explicitly exposed.

### Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    expose_headers=[
        "X-Request-ID",
        "X-RateLimit-Limit",
        "X-RateLimit-Remaining",
        "X-RateLimit-Reset",
        "X-Total-Count",
        "X-Process-Time",
    ],
)
```

### JavaScript Side

```javascript
const response = await fetch("https://api.example.com/users");
const data = await response.json();

// These headers are accessible
const requestId = response.headers.get("X-Request-ID");
const rateLimit = response.headers.get("X-RateLimit-Limit");
```

---

## Preflight Requests

### How Preflight Works

1. Browser sends `OPTIONS` request with headers:
   - `Origin`: The requesting origin
   - `Access-Control-Request-Method`: The HTTP method
   - `Access-Control-Request-Headers`: The headers the request will use

2. Server responds with:
   - `Access-Control-Allow-Origin`: Allowed origin
   - `Access-Control-Allow-Methods`: Allowed methods
   - `Access-Control-Allow-Headers`: Allowed headers
   - `Access-Control-Max-Age`: How long to cache the preflight result

### Example Preflight Flow

```javascript
// Browser sends this preflight
OPTIONS /api/users
Origin: https://app.example.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Authorization, Content-Type

// Server responds
204 No Content
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Max-Age: 86400

// Browser then sends the actual request
POST /api/users
Origin: https://app.example.com
Authorization: Bearer xxx
Content-Type: application/json
```

### Non-Preflight Requests

Simple requests don't trigger preflight:
- Method: GET, HEAD, POST
- Content-Type: application/x-www-form-urlencoded, multipart/form-data, text/plain
- No custom headers (except CORS-safe ones)

---

## CORS Best Practices

### 1. Never Use Wildcard Origin in Production

```python
# BAD
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
)

# GOOD
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
)
```

### 2. Limit Allowed Methods

```python
# BAD: Allows all methods
allow_methods=["*"]

# GOOD: Only allow what you need
allow_methods=["GET", "POST", "PUT", "DELETE"]
```

### 3. Limit Allowed Headers

```python
# BAD: Allows all headers
allow_headers=["*"]

# GOOD: Only allow what you need
allow_headers=["Authorization", "Content-Type"]
```

### 4. Set Max-Age for Preflight Cache

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    max_age=600,  # Cache preflight for 10 minutes
)
```

### 5. Use Environment-Based Configuration

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = "production"
    ALLOWED_ORIGINS: list[str] = ["https://app.example.com"]

    @property
    def cors_origins(self) -> list[str]:
        if self.ENVIRONMENT == "development":
            return ["http://localhost:3000", "http://localhost:5173"]
        return self.ALLOWED_ORIGINS

settings = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### 6. Log CORS Rejections

```python
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.cors")

class LoggingCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        origin = request.headers.get("origin")
        if origin and origin not in ALLOWED_ORIGINS:
            logger.warning(f"CORS rejection for origin: {origin}")
        return await call_next(request)
```

---

## Security Implications

### CORS Is Not Authentication

```python
# WRONG: Using CORS as a security layer
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    # Assuming this alone prevents unauthorized access
)

# RIGHT: CORS + Authentication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
)

@app.get("/api/secret")
async def secret_endpoint(user = Depends(get_current_user)):
    # Still require authentication!
    return {"secret": "data"}
```

### Common Security Mistakes

```python
# Mistake 1: Allowing all origins
allow_origins=["*"]

# Mistake 2: Trusting the Origin header without validation
# The Origin header can be spoofed by non-browser clients

# Mistake 3: Using CORS to protect API endpoints
# CORS only applies to browsers; API clients can bypass it

# Mistake 4: Reflecting the Origin header without validation
# If server echoes back any Origin, it's equivalent to *
```

### What CORS Protects Against

1. **CSRF from malicious websites**: Cannot read responses from other origins
2. **Unauthorized cross-origin requests**: Browser blocks requests to disallowed origins
3. **Data leakage**: Prevents JavaScript from reading responses from other origins

### What CORS Does NOT Protect Against

1. **Server-to-server requests**: CORS is a browser mechanism
2. **Direct API calls**: Tools like curl ignore CORS
3. **Same-site attacks**: Use CSRF tokens for these
4. **Subdomain takeovers**: Configure CORS carefully for subdomains

---

## Production CORS Configuration

### Full Production Setup

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    ENVIRONMENT: str = "production"
    CORS_ORIGINS: list[str] = []
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    CORS_ALLOW_HEADERS: list[str] = ["Authorization", "Content-Type", "X-Request-ID"]
    CORS_EXPOSE_HEADERS: list[str] = ["X-Request-ID", "X-RateLimit-Limit", "X-RateLimit-Remaining"]
    CORS_MAX_AGE: int = 3600

    class Config:
        env_file = ".env"

settings = Settings()

app = FastAPI(title="Production API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
    expose_headers=settings.CORS_EXPOSE_HEADERS,
    max_age=settings.CORS_MAX_AGE,
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Multi-Tenant CORS

```python
def get_tenant_cors_origins(tenant_id: str) -> list[str]:
    """Get allowed origins for a specific tenant."""
    tenant_configs = {
        "tenant_a": ["https://a.example.com", "https://a-admin.example.com"],
        "tenant_b": ["https://b.example.com", "https://b-admin.example.com"],
    }
    return tenant_configs.get(tenant_id, [])

class TenantCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        origin = request.headers.get("origin", "")

        # Determine tenant from origin or path
        tenant_id = extract_tenant(origin)
        allowed_origins = get_tenant_cors_origins(tenant_id)

        if origin in allowed_origins:
            response = await call_next(request)
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            return response
        else:
            return JSONResponse(
                status_code=403,
                content={"detail": "Origin not allowed"}
            )
```

---

## Common CORS Errors

### Error 1: "No 'Access-Control-Allow-Origin' header is present"

**Cause:** Server doesn't include CORS headers in the response.
**Fix:** Add CORSMiddleware with the correct origin.

### Error 2: "The value of 'Access-Control-Allow-Origin' must not be '*'"

**Cause:** Using wildcard with credentials.
**Fix:** Specify explicit origins.

### Error 3: "Method not allowed by Access-Control-Allow-Methods"

**Cause:** The method isn't in the allowed list.
**Fix:** Add the method to `allow_methods`.

### Error 4: "Request header field not allowed by Access-Control-Allow-Headers"

**Cause:** The header isn't in the allowed list.
**Fix:** Add the header to `allow_headers`.

### Error 5: "Credentials flag is true, but Access-Control-Allow-Credentials is false"

**Cause:** Frontend sends `credentials: include` but server doesn't set `allow_credentials=True`.
**Fix:** Set `allow_credentials=True` in CORSMiddleware.

### Debugging CORS Issues

```python
# Temporary debugging middleware
class CORSDebugMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        origin = request.headers.get("origin")
        method = request.method

        if method == "OPTIONS":
            print(f"PREFLIGHT: {origin} -> {request.url.path}")
            print(f"  Request-Method: {request.headers.get('access-control-request-method')}")
            print(f"  Request-Headers: {request.headers.get('access-control-request-headers')}")

        response = await call_next(request)

        if origin:
            print(f"RESPONSE:")
            print(f"  Allow-Origin: {response.headers.get('access-control-allow-origin')}")
            print(f"  Allow-Credentials: {response.headers.get('access-control-allow-credentials')}")

        return response
```

---

## Interview Questions

### Q1: What is CORS and why does it exist?
**Answer:** CORS (Cross-Origin Resource Sharing) is a browser security mechanism that controls which origins can access resources from a different origin. It prevents malicious websites from making unauthorized requests to other services on behalf of users.

### Q2: How does FastAPI handle CORS?
**Answer:** FastAPI uses Starlette's `CORSMiddleware` which intercepts requests and adds appropriate CORS headers. For preflight requests (OPTIONS), it responds directly without reaching the route handler.

### Q3: Can you use `allow_origins=["*"]` with `allow_credentials=True`?
**Answer:** No. The CORS specification forbids wildcard origins when credentials are allowed. Browsers will reject the response. You must specify explicit origins.

### Q4: What is a preflight request?
**Answer:** A preflight is an OPTIONS request the browser sends before the actual request for "complex" requests (non-simple methods, custom headers, etc.). The server responds with allowed methods and headers, and the browser then makes the actual request.

### Q5: What triggers a preflight request?
**Answer:** Requests with methods other than GET/HEAD/POST, or POST requests with non-simple content types (anything other than form-encoded, multipart, or text/plain), or requests with custom headers.

### Q6: Why do I need `expose_headers`?
**Answer:** By default, browsers only allow JavaScript to read a limited set of response headers. Custom headers like `X-Request-ID` or `X-RateLimit-*` must be explicitly exposed via `Access-Control-Expose-Headers`.

### Q7: What does `max_age` do in CORS middleware?
**Answer:** It sets the `Access-Control-Max-Age` header, telling the browser how long (in seconds) to cache the preflight response. This reduces the number of OPTIONS requests.

### Q8: Is CORS a substitute for authentication?
**Answer:** No. CORS only applies to browsers. API clients (curl, Postman, server-to-server) ignore CORS. Always implement proper authentication regardless of CORS configuration.

### Q9: How do you handle CORS for WebSocket connections?
**Answer:** CORS doesn't apply to WebSocket connections. WebSocket security relies on the initial HTTP upgrade request and Origin header validation, which must be handled manually.

### Q10: What's the difference between CORS and CSRF protection?
**Answer:** CORS prevents browsers from making cross-origin requests to disallowed origins. CSRF protection prevents malicious sites from tricking users into making requests to sites where they're authenticated. They serve different purposes.

### Q11: How do you debug CORS issues?
**Answer:** Check browser DevTools Network tab for preflight responses, verify the Origin header, check response CORS headers, look for missing methods/headers in the allowed lists, and check server logs.

### Q12: Can CORS middleware block all requests?
**Answer:** Yes, if `allow_origins` doesn't include the requesting origin. The middleware will return 403 for preflight requests and strip CORS headers for simple requests.

### Q13: How does CORS affect different HTTP methods?
**Answer:** Simple methods (GET, HEAD, POST) with simple content types don't trigger preflight. Other methods (PUT, DELETE, PATCH) always trigger preflight. You can configure `allow_methods` to control which methods are allowed.

### Q14: What happens if CORS middleware is added after routes?
**Answer:** Middleware order matters. CORS should be added before (or at least not after) other middleware that might affect the response. In FastAPI, add middleware before routes for correct ordering.

### Q15: How do you implement dynamic CORS origins?
**Answer:** Use a custom middleware class that checks the Origin header against a dynamic list (from database, config, or environment). You can also subclass `CORSMiddleware` for custom origin validation.

### Q16: What are CORS-safe request headers?
**Answer:** Accept, Accept-Language, Content-Language, Content-Type (with restrictions). These headers can be sent without triggering a preflight request.

### Q17: How does CORS work with cookies?
**Answer:** When `allow_credentials=True`, the browser includes cookies in cross-origin requests if the server responds with `Access-Control-Allow-Credentials: true`. The `SameSite` cookie attribute also affects this behavior.

### Q18: Can CORS be bypassed?
**Answer:** Yes, by non-browser HTTP clients (curl, Postman). CORS is a browser-only security mechanism. Server-side validation (authentication, authorization) is still necessary.

### Q19: What's the relationship between CORS and Content-Security-Policy?
**Answer:** CORS controls which origins can access resources. CSP controls what resources a page can load. CSP `connect-src` directive restricts which URLs JavaScript can fetch, working alongside CORS.

### Q20: How do you handle CORS in a microservices architecture?
**Answer:** Handle CORS at the API gateway or BFF (Backend for Frontend) level. Individual microservices typically don't need CORS middleware since they're called by the gateway, not directly by browsers.

### Q21: What is `Access-Control-Allow-Private-Network`?
**Answer:** A newer CORS header that controls whether public internet websites can access resources on private networks (localhost, 192.168.x.x). Useful for development with local backends.

### Q22: How do you test CORS configuration?
**Answer:** Use browser DevTools to check preflight and actual request/response headers. Use curl with `-H "Origin: ..."` to simulate cross-origin requests. Write integration tests with TestClient.

### Q23: Can CORS headers be cached?
**Answer:** Yes, via `Access-Control-Max-Age`. The browser caches preflight responses for the specified duration. This reduces OPTIONS requests but can cause issues when updating CORS configuration.

### Q24: What are the security risks of misconfigured CORS?
**Answer:** Overly permissive CORS (e.g., reflecting any origin) can allow any website to read API responses, potentially leaking sensitive data. It can also enable CSRF attacks if combined with credentials.

### Q25: How do you handle CORS with server-sent events (SSE)?
**Answer:** SSE uses standard HTTP GET requests, so CORS applies normally. Set `allow_origins` to include the frontend origin and ensure the response includes proper CORS headers.
