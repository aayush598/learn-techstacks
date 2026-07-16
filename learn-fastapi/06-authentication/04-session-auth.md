# Session Authentication with FastAPI

## Table of Contents

1. [Server-Side Sessions](#server-side-sessions)
2. [Session Middleware](#session-middleware)
3. [Secure Cookies](#secure-cookies)
4. [SameSite Cookies](#samesite-cookies)
5. [CSRF Protection](#csrf-protection)
6. [Session vs JWT](#session-vs-jwt)
7. [Redis-Backed Sessions](#redis-backed-sessions)
8. [Best Practices](#best-practices)
9. [Interview Questions](#interview-questions)

---

## Server-Side Sessions

Server-side sessions store user data on the server, with only a session ID sent to the client via a cookie.

### How Sessions Work

```
1. User logs in with credentials
2. Server creates session data (user_id, role, etc.)
3. Server stores session data in memory/database
4. Server sends session ID to client via cookie
5. Client sends session ID with each request
6. Server looks up session data by ID
7. Server processes request with user context
```

### Session Storage Options

| Storage | Pros | Cons |
|---------|------|------|
| Memory | Fast | Lost on restart, not scalable |
| File | Simple | Slow, not scalable |
| Database | Persistent | Adds DB load |
| Redis | Fast, persistent, scalable | Extra dependency |
| Memcached | Fast, distributed | No persistence |

---

## Session Middleware

### Starlette Session Middleware

```python
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI

app = FastAPI()

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key",
    session_cookie="session_id",
    max_age=3600,          # 1 hour
    same_site="lax",       # CSRF protection
    https_only=True,       # HTTPS only
    domain=None,           # Current domain only
    path="/",              # All paths
)

@app.post("/login")
async def login(request: Request, username: str, password: str):
    user = authenticate_user(username, password)
    if user:
        request.session["user_id"] = user.id
        request.session["role"] = user.role
        return {"message": "Logged in"}
    raise HTTPException(401, "Invalid credentials")

@app.get("/me")
async def get_me(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(401, "Not authenticated")
    return {"user_id": user_id}

@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out"}
```

### Custom Session Backend

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class CustomSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secret_key: str, session_store):
        super().__init__(app)
        self.secret_key = secret_key
        self.session_store = session_store

    async def dispatch(self, request: Request, call_next):
        session_id = request.cookies.get("session_id")

        if session_id:
            session_data = await self.session_store.get(session_id)
        else:
            session_id = generate_session_id()
            session_data = {}

        request.session = Session(session_data, session_id)

        response = await call_next(request)

        # Save session
        await self.session_store.set(session_id, request.session.data)

        # Set cookie
        response.set_cookie(
            "session_id",
            session_id,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=3600,
        )

        return response
```

### FastAPI Session Dependency

```python
from starlette.requests import Request

async def get_session(request: Request) -> dict:
    return request.session

@app.get("/profile/")
async def get_profile(session: dict = Depends(get_session)):
    user_id = session.get("user_id")
    if not user_id:
        raise HTTPException(401)
    return {"user_id": user_id}
```

---

## Secure Cookies

### Cookie Security Flags

```python
@app.post("/login")
async def login(response: Response, ...):
    # Set secure cookie
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,    # Not accessible via JavaScript (prevents XSS)
        secure=True,     # Only sent over HTTPS
        samesite="lax",  # CSRF protection
        max_age=3600,    # Expires after 1 hour
        path="/",        # Available on all paths
        domain=None,     # Current domain only
    )
```

### Cookie Attributes Explained

| Attribute | Purpose | Recommended |
|-----------|---------|-------------|
| `httponly` | Prevents JavaScript access | Always `True` |
| `secure` | HTTPS only | Always `True` in production |
| `samesite` | CSRF protection | `"lax"` or `"strict"` |
| `max_age` | Expiration in seconds | 3600 (1 hour) for sessions |
| `path` | URL path scope | `"/"` for all |
| `domain` | Domain scope | `None` for current domain |

---

## SameSite Cookies

### SameSite Values

```python
# Lax (recommended for most cases)
# Sends cookie for top-level navigation and GET requests
response.set_cookie("session_id", value, samesite="lax")

# Strict
# Only sends cookie for same-site requests
response.set_cookie("session_id", value, samesite="strict")

# None
# Sends cookie for all requests (requires Secure=True)
response.set_cookie("session_id", value, samesite="none", secure=True)
```

### Cross-Site Request Forgery Prevention

```python
# With SameSite=Lax, CSRF is mostly prevented
# For extra security, use CSRF tokens

from secrets import token_hex

class CSRFProtection:
    def __init__(self):
        self.tokens: dict[str, str] = {}

    def generate_token(self, session_id: str) -> str:
        token = token_hex(32)
        self.tokens[session_id] = token
        return token

    def validate_token(self, session_id: str, token: str) -> bool:
        stored = self.tokens.get(session_id)
        return stored and secrets.compare_digest(stored, token)

csrf_protection = CSRFProtection()

@app.get("/form/")
async def get_form(request: Request):
    token = csrf_protection.generate_token(request.session["id"])
    return {"csrf_token": token}

@app.post("/form/")
async def submit_form(
    request: Request,
    csrf_token: str = Form(),
):
    if not csrf_protection.validate_token(request.session["id"], csrf_token):
        raise HTTPException(403, "Invalid CSRF token")
    # Process form
```

---

## Session vs JWT

### Comparison

| Aspect | Sessions | JWT |
|--------|----------|-----|
| Storage | Server-side | Client-side |
| Scalability | Requires shared store | Stateless |
| Revocation | Easy (delete session) | Hard (blocklist) |
| Performance | DB lookup per request | No DB lookup |
| Size | Small cookie (ID only) | Larger (contains claims) |
| Mobile | Cookie challenges | Works well |
| Complexity | Simple | Moderate |

### When to Use Sessions

```python
# GOOD: Traditional web apps
# - Server-rendered pages
# - Simple authentication
# - Easy revocation needed
# - Same-domain only

@app.post("/login")
async def login(request: Request, ...):
    request.session["user_id"] = user.id
    # Session stored server-side
```

### When to Use JWT

```python
# GOOD: API-first applications
# - SPA + API architecture
# - Mobile apps
# - Microservices
# - Cross-domain requests

@app.post("/token")
async def login(...):
    token = create_access_token({"sub": user.id})
    return {"access_token": token}
```

### Hybrid Approach

```python
# Use JWT for API access + session for web
@app.post("/login/web")
async def web_login(request: Request, ...):
    # Web: session-based
    request.session["user_id"] = user.id
    return RedirectResponse("/dashboard")

@app.post("/login/api")
async def api_login(...):
    # API: JWT-based
    token = create_access_token({"sub": user.id})
    return {"access_token": token}
```

---

## Redis-Backed Sessions

### Implementation

```python
import redis.asyncio as redis
import json
import uuid

class RedisSessionStore:
    def __init__(self, redis_url: str, ttl: int = 3600):
        self.redis = redis.Redis.from_url(redis_url)
        self.ttl = ttl

    async def create(self, data: dict) -> str:
        session_id = str(uuid.uuid4())
        await self.redis.setex(
            f"session:{session_id}",
            self.ttl,
            json.dumps(data),
        )
        return session_id

    async def get(self, session_id: str) -> dict | None:
        data = await self.redis.get(f"session:{session_id}")
        if data:
            return json.loads(data)
        return None

    async def set(self, session_id: str, data: dict):
        await self.redis.setex(
            f"session:{session_id}",
            self.ttl,
            json.dumps(data),
        )

    async def delete(self, session_id: str):
        await self.redis.delete(f"session:{session_id}")

    async def refresh(self, session_id: str):
        await self.redis.expire(f"session:{session_id}", self.ttl)

# Dependency
session_store = RedisSessionStore("redis://localhost:6379")

async def get_session(request: Request) -> dict:
    session_id = request.cookies.get("session_id")
    if not session_id:
        return {}

    data = await session_store.get(session_id)
    if data:
        await session_store.refresh(session_id)
        return data
    return {}
```

### Full Session Auth Implementation

```python
from fastapi import FastAPI, Depends, Response, Request
from fastapi.security import HTTPBearer

app = FastAPI()
session_store = RedisSessionStore("redis://localhost:6379")

@app.post("/login")
async def login(
    response: Response,
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")

    # Create session
    session_data = {
        "user_id": user.id,
        "role": user.role,
        "email": user.email,
    }
    session_id = await session_store.create(session_data)

    # Set cookie
    response.set_cookie(
        "session_id",
        session_id,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600,
    )

    return {"message": "Logged in"}

@app.get("/me")
async def get_me(
    request: Request,
    session: dict = Depends(get_session),
):
    if not session.get("user_id"):
        raise HTTPException(401, "Not authenticated")
    return {"user_id": session["user_id"], "role": session["role"]}

@app.post("/logout")
async def logout(
    response: Response,
    request: Request,
):
    session_id = request.cookies.get("session_id")
    if session_id:
        await session_store.delete(session_id)
    response.delete_cookie("session_id")
    return {"message": "Logged out"}
```

---

## Best Practices

### 1. Always Use HTTPS

```python
# Force HTTPS
@app.middleware("http")
async def force_https(request: Request, call_next):
    if request.url.scheme == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url, status_code=301)
    return await call_next(request)
```

### 2. Set Appropriate Expiration

```python
# Short-lived sessions for sensitive apps
max_age = 1800  # 30 minutes

# Longer sessions for convenience
max_age = 86400  # 24 hours

# Sliding expiration (refresh on activity)
if session_data:
    await session_store.refresh(session_id)
```

### 3. Regenerate Session ID on Login

```python
@app.post("/login")
async def login(request: Request, ...):
    # Prevent session fixation
    old_session_id = request.cookies.get("session_id")
    if old_session_id:
        await session_store.delete(old_session_id)

    # Create new session
    new_session_id = await session_store.create(session_data)
    response.set_cookie("session_id", new_session_id, ...)
```

### 4. Invalidate Sessions on Password Change

```python
@app.post("/change-password/")
async def change_password(
    request: Request,
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
):
    # Update password
    user.hashed_password = hash_password(data.new_password)
    db.commit()

    # Invalidate all other sessions
    await session_store.delete_all_for_user(user.id)
```

### 5. Monitor Session Activity

```python
async def get_session(request: Request) -> dict:
    session_id = request.cookies.get("session_id")
    data = await session_store.get(session_id)

    if data:
        # Track activity
        data["last_activity"] = datetime.now().isoformat()
        data["ip_address"] = request.client.host
        await session_store.set(session_id, data)

    return data or {}
```

---

## Interview Questions

### Q1: What is server-side session authentication?
**Answer:** User data is stored on the server, with only a session ID sent to the client via cookie. The client sends the session ID with each request, and the server looks up the session data.

### Q2: What are the advantages of sessions over JWT?
**Answer:** Easy revocation (delete session), smaller cookie size, server controls session data, no token expiration issues. Good for traditional web apps.

### Q3: What are the disadvantages of sessions?
**Answer:** Requires server-side storage, doesn't scale horizontally without shared store (Redis), can't work across domains easily, adds server load for session lookups.

### Q4: How do you prevent session fixation?
**Answer:** Regenerate the session ID on login. Never accept session IDs from untrusted sources. Invalidate old sessions before creating new ones.

### Q5: What is SameSite cookie attribute?
**Answer:** Controls when cookies are sent with cross-site requests. `Lax` sends cookies for top-level navigation. `Strict` only sends for same-site requests. `None` sends always (requires HTTPS).

### Q6: How does CSRF protection work with sessions?
**Answer:** SameSite cookies prevent most CSRF attacks. For additional protection, use CSRF tokens — include a secret token in forms that the server validates on submission.

### Q7: Why use Redis for session storage?
**Answer:** Fast (in-memory), persistent, supports TTL for automatic expiration, scalable, and handles concurrent access well. Better than file or database storage for session data.

### Q8: How do you handle session expiration?
**Answer:** Set `max_age` on the cookie and TTL in the store. Implement sliding expiration (refresh on activity) or fixed expiration (absolute timeout).

### Q9: Can sessions work with mobile apps?
**Answer:** Yes, but cookies are less natural for mobile. Mobile apps typically use JWT. You can use session cookies with HTTP clients that support cookies.

### Q10: How do you logout with sessions?
**Answer:** Delete the session from the server store and clear the cookie on the client. For security, also clear any cached data.

---

## Summary

Session authentication is a secure, server-side approach ideal for traditional web applications. Use Redis for scalable session storage, implement secure cookie flags, prevent CSRF with SameSite, and regenerate session IDs on login. Consider JWT for API-first or cross-domain applications.
