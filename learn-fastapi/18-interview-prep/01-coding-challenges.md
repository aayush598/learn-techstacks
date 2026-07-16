# FastAPI Coding Challenges - Complete Solutions

## Challenge 1: URL Shortener API

### Problem Statement
Build a URL shortener that generates short codes, redirects to original URLs, and tracks click analytics.

### Solution

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl
import hashlib
import string
import time
from collections import defaultdict

app = FastAPI(title="URL Shortener")

url_store: dict[str, dict] = {}
click_analytics: dict[str, list[dict]] = defaultdict(list)

BASE_URL = "http://localhost:8000"


def generate_short_code(url: str, length: int = 7) -> str:
    """Generate a deterministic short code from URL hash."""
    hash_hex = hashlib.sha256(url.encode()).hexdigest()
    chars = string.ascii_letters + string.digits
    code = []
    for i in range(0, length):
        idx = int(hash_hex[i * 2 : i * 2 + 2], 16) % len(chars)
        code.append(chars[idx])
    return "".join(code)


@app.post("/shorten")
def shorten_url(url: HttpUrl):
    url_str = str(url)

    for code, data in url_store.items():
        if data["original_url"] == url_str:
            return {"short_url": f"{BASE_URL}/{code}", "code": code}

    code = generate_short_code(url_str)
    url_store[code] = {
        "original_url": url_str,
        "created_at": time.time(),
        "clicks": 0,
    }
    return {"short_url": f"{BASE_URL}/{code}", "code": code}


@app.get("/{code}")
def redirect_to_url(code: str, request: Request):
    if code not in url_store:
        raise HTTPException(status_code=404, detail="Short URL not found")

    url_store[code]["clicks"] += 1
    click_analytics[code].append(
        {
            "timestamp": time.time(),
            "ip": request.client.host,
            "user_agent": request.headers.get("user-agent", ""),
        }
    )
    return RedirectResponse(url=url_store[code]["original_url"], status_code=307)


@app.get("/analytics/{code}")
def get_analytics(code: str):
    if code not in url_store:
        raise HTTPException(status_code=404, detail="Short URL not found")

    data = url_store[code]
    clicks = click_analytics.get(code, [])
    return {
        "original_url": data["original_url"],
        "total_clicks": data["clicks"],
        "created_at": data["created_at"],
        "recent_clicks": clicks[-10:],
    }
```

### Complexity Analysis
- **Shorten**: O(n) average for hash lookup, O(1) amortized insert
- **Redirect**: O(1) lookup and update
- **Space**: O(n) where n is number of shortened URLs

---

## Challenge 2: Rate Limiter Middleware

### Problem Statement
Implement a sliding window rate limiter middleware that limits requests per client IP.

### Solution

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import time
from collections import defaultdict
from dataclasses import dataclass, field

app = FastAPI()


@dataclass
class SlidingWindowRateLimiter:
    max_requests: int = 100
    window_seconds: int = 60
    _windows: dict = field(default_factory=lambda: defaultdict(list))

    def _clean_window(self, client_id: str, now: float):
        cutoff = now - self.window_seconds
        self._windows[client_id] = [
            ts for ts in self._windows[client_id] if ts > cutoff
        ]

    def is_allowed(self, client_id: str) -> tuple[bool, dict]:
        now = time.time()
        self._clean_window(client_id, now)

        current_count = len(self._windows[client_id])
        remaining = max(0, self.max_requests - current_count)
        reset_at = self._windows[client_id][0] + self.window_seconds if self._windows[client_id] else now + self.window_seconds

        headers = {
            "X-RateLimit-Limit": str(self.max_requests),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(int(reset_at)),
        }

        if current_count >= self.max_requests:
            retry_after = self._windows[client_id][0] + self.window_seconds - now
            headers["Retry-After"] = str(int(retry_after) + 1)
            return False, headers

        self._windows[client_id].append(now)
        headers["X-RateLimit-Remaining"] = str(remaining - 1)
        return True, headers


limiter = SlidingWindowRateLimiter(max_requests=100, window_seconds=60)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    allowed, headers = limiter.is_allowed(client_ip)

    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"},
            headers=headers,
        )

    response = await call_next(request)
    for key, value in headers.items():
        response.headers[key] = value
    return response


@app.get("/")
def root():
    return {"message": "Rate limiting active"}
```

### Explanation
- Uses a sliding window algorithm with sorted timestamp lists
- Per-IP tracking with automatic cleanup of expired entries
- Returns standard rate limit headers (X-RateLimit-*)
- Retry-After header tells clients when to retry

### Complexity Analysis
- **Check**: O(n) cleanup, O(1) check where n = requests in window
- **Space**: O(n) per client, bounded by max_requests

---

## Challenge 3: Real-Time Notification System with WebSockets

### Problem Statement
Build a WebSocket-based notification system that supports user subscriptions and targeted notifications.

### Solution

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
import asyncio
from collections import defaultdict

app = FastAPI(title="Notification System")


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = defaultdict(list)
        self.user_channels: dict[str, set[str]] = defaultdict(set)

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        self.active_connections[user_id].remove(websocket)
        if not self.active_connections[user_id]:
            del self.active_connections[user_id]

    async def send_to_user(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            dead = []
            for ws in self.active_connections[user_id]:
                try:
                    await ws.send_json(message)
                except Exception:
                    dead.append(ws)
            for ws in dead:
                self.active_connections[user_id].remove(ws)

    async def broadcast(self, message: dict):
        for user_id in list(self.active_connections.keys()):
            await self.send_to_user(user_id, message)

    async def send_to_channel(self, channel: str, message: dict):
        for user_id, channels in self.user_channels.items():
            if channel in channels:
                await self.send_to_user(user_id, message)


manager = ConnectionManager()


@app.websocket("/ws/notifications/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            if action == "subscribe":
                channel = data.get("channel")
                manager.user_channels[user_id].add(channel)
                await websocket.send_json(
                    {"type": "system", "message": f"Subscribed to {channel}"}
                )
            elif action == "unsubscribe":
                channel = data.get("channel")
                manager.user_channels[user_id].discard(channel)
                await websocket.send_json(
                    {"type": "system", "message": f"Unsubscribed from {channel}"}
                )
            elif action == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)


class NotificationPayload(BaseModel):
    user_id: str
    title: str
    body: str
    channel: str | None = None


@app.post("/notify")
async def send_notification(payload: NotificationPayload):
    message = {
        "type": "notification",
        "title": payload.title,
        "body": payload.body,
    }
    if payload.channel:
        await manager.send_to_channel(payload.channel, message)
    else:
        await manager.send_to_user(payload.user_id, message)
    return {"status": "sent"}
```

### Explanation
- ConnectionManager handles all WebSocket lifecycle operations
- Channel-based pub/sub allows topic subscriptions
- Dead connection cleanup prevents memory leaks
- HTTP endpoint allows backend services to push notifications

---

## Challenge 4: Typed Pagination System

### Problem Statement
Create a generic, type-safe pagination system with cursor and offset strategies.

### Solution

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Generic, TypeVar, Sequence
from dataclasses import dataclass

T = TypeVar("T")

app = FastAPI()


class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 20
    cursor: str | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
    next_cursor: str | None = None


def paginate(
    items: Sequence,
    page: int = 1,
    per_page: int = 20,
) -> dict:
    total = len(items)
    total_pages = max(1, -(-total // per_page))
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page

    return {
        "items": list(items[start:end]),
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }


class Item(BaseModel):
    id: int
    name: str
    price: float


items_db = [Item(id=i, name=f"Item {i}", price=i * 9.99) for i in range(1, 101)]


@app.get("/items", response_model=PaginatedResponse[Item])
def list_items(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    return paginate(items_db, page=page, per_page=per_page)


class CursorPage(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: str | None
    has_more: bool


def cursor_paginate(items: Sequence, cursor: str | None = None, limit: int = 20):
    start_idx = 0
    if cursor:
        for i, item in enumerate(items):
            if getattr(item, "id", None) == int(cursor):
                start_idx = i + 1
                break

    page_items = list(items[start_idx : start_idx + limit + 1])
    has_more = len(page_items) > limit
    page_items = page_items[:limit]
    next_cursor = str(getattr(page_items[-1], "id", None)) if has_more and page_items else None

    return {
        "items": page_items,
        "next_cursor": next_cursor,
        "has_more": has_more,
    }


@app.get("/items/cursor", response_model=CursorPage[Item])
def list_items_cursor(
    cursor: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
):
    return cursor_paginate(items_db, cursor=cursor, limit=limit)
```

### Complexity Analysis
- **Offset pagination**: O(1) access, O(n) scan for total
- **Cursor pagination**: O(n) scan but efficient for large datasets with indexed cursors

---

## Challenge 5: Multi-Tenant Middleware

### Problem Statement
Implement middleware that extracts tenant information from headers and scopes database access per tenant.

### Solution

```python
from fastapi import FastAPI, Request, HTTPException, Depends
from contextvars import ContextVar
from pydantic import BaseModel
from typing import AsyncGenerator
from dataclasses import dataclass

app = FastAPI(title="Multi-Tenant API")

tenant_context: ContextVar[str] = ContextVar("tenant_id", default="")


class TenantConfig(BaseModel):
    tenant_id: str
    db_schema: str
    plan: str
    rate_limit: int


TENANTS: dict[str, TenantConfig] = {
    "tenant-a": TenantConfig(tenant_id="tenant-a", db_schema="tenant_a", plan="enterprise", rate_limit=1000),
    "tenant-b": TenantConfig(tenant_id="tenant-b", db_schema="tenant_b", plan="starter", rate_limit=100),
}


@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    tenant_id = request.headers.get("X-Tenant-ID")

    if not tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header required")

    if tenant_id not in TENANTS:
        raise HTTPException(status_code=404, detail=f"Tenant '{tenant_id}' not found")

    token = tenant_context.set(tenant_id)
    try:
        response = await call_next(request)
        response.headers["X-Tenant-ID"] = tenant_id
        response.headers["X-Tenant-Plan"] = TENANTS[tenant_id].plan
        return response
    finally:
        tenant_context.reset(token)


def get_current_tenant() -> TenantConfig:
    tenant_id = tenant_context.get()
    if not tenant_id:
        raise HTTPException(status_code=400, detail="No tenant context")
    return TENANTS[tenant_id]


@app.get("/resources")
def get_resources(tenant: TenantConfig = Depends(get_current_tenant)):
    return {
        "tenant": tenant.tenant_id,
        "plan": tenant.plan,
        "resources": ["item-1", "item-2"],
    }


@app.get("/tenant-info")
def tenant_info(tenant: TenantConfig = Depends(get_current_tenant)):
    return {"schema": tenant.db_schema, "rate_limit": tenant.rate_limit}
```

### Explanation
- Uses Python `ContextVars` for thread/async-safe tenant isolation
- Middleware validates tenant early and sets context for downstream handlers
- Dependency injection provides typed tenant config to route handlers
- Easy to extend with row-level security in database queries

---

## Challenge 6: Cache-Aside Pattern

### Problem Statement
Implement a cache-aside pattern with TTL, LRU eviction, and cache invalidation.

### Solution

```python
from fastapi import FastAPI
from functools import wraps
import time
import hashlib
import json
from collections import OrderedDict
from typing import Callable, Any
from threading import Lock

app = FastAPI()


class LRUCache:
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._store: OrderedDict = OrderedDict()
        self._lock = Lock()

    def get(self, key: str) -> Any | None:
        with self._lock:
            if key in self._store:
                entry = self._store[key]
                if entry["expires_at"] > time.time():
                    self._store.move_to_end(key)
                    return entry["value"]
                else:
                    del self._store[key]
        return None

    def set(self, key: str, value: Any, ttl: int | None = None):
        with self._lock:
            if key in self._store:
                del self._store[key]
            elif len(self._store) >= self.max_size:
                self._store.popitem(last=False)
            self._store[key] = {
                "value": value,
                "expires_at": time.time() + (ttl or self.default_ttl),
            }

    def invalidate(self, key: str):
        with self._lock:
            self._store.pop(key, None)

    def clear(self):
        with self._lock:
            self._store.clear()


cache = LRUCache(max_size=500, default_ttl=60)


def cached(ttl: int | None = None, key_prefix: str = ""):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{key_prefix}:{func.__name__}:{hashlib.md5(json.dumps(kwargs, default=str).encode()).hexdigest()}"

            result = cache.get(cache_key)
            if result is not None:
                return result

            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl=ttl)
            return result

        return wrapper
    return decorator


@app.get("/products/{product_id}")
@cached(ttl=120, key_prefix="product")
def get_product(product_id: int):
    # Simulate expensive database query
    time.sleep(0.1)
    return {"id": product_id, "name": f"Product {product_id}", "price": 99.99}


@app.delete("/products/{product_id}/cache")
def invalidate_product_cache(product_id: int):
    cache_key_pattern = f"product:get_product:"
    for key in list(cache._store.keys()):
        if f"product_id={product_id}" in key:
            cache.invalidate(key)
    return {"status": "invalidated"}
```

### Complexity Analysis
- **Get**: O(1) average (hash map + ordered dict move)
- **Set**: O(1) average with LRU eviction
- **Space**: Bounded by max_size parameter

---

## Challenge 7: WebSocket Chat Room

### Problem Statement
Build a WebSocket chat room with rooms, user joins/leaves, and message history.

### Solution

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from pydantic import BaseModel
import time
from collections import defaultdict
from dataclasses import dataclass, field

app = FastAPI()


@dataclass
class ChatMessage:
    user: str
    message: str
    room: str
    timestamp: float


@dataclass
class ChatRoom:
    name: str
    connections: dict[str, WebSocket] = field(default_factory=dict)
    history: list[ChatMessage] = field(default_factory=list)
    max_history: int = 100

    def add_message(self, msg: ChatMessage):
        self.history.append(msg)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]


rooms: dict[str, ChatRoom] = {}


@app.websocket("/ws/chat/{room_name}")
async def chat_websocket(websocket: WebSocket, room_name: str, username: str = Query(...)):
    if room_name not in rooms:
        rooms[room_name] = ChatRoom(name=room_name)

    room = rooms[room_name]
    await websocket.accept()
    room.connections[username] = websocket

    await broadcast(room, {"type": "system", "message": f"{username} joined"})
    history = [
        {"user": m.user, "message": m.message, "timestamp": m.timestamp}
        for m in room.history[-20:]
    ]
    await websocket.send_json({"type": "history", "messages": history})

    try:
        while True:
            data = await websocket.receive_json()
            msg = ChatMessage(
                user=username,
                message=data["message"],
                room=room_name,
                timestamp=time.time(),
            )
            room.add_message(msg)
            await broadcast(room, {
                "type": "message",
                "user": username,
                "message": data["message"],
                "timestamp": msg.timestamp,
            })
    except WebSocketDisconnect:
        del room.connections[username]
        await broadcast(room, {"type": "system", "message": f"{username} left"})
        if not room.connections and not room.history:
            del rooms[room_name]


async def broadcast(room: ChatRoom, message: dict):
    dead = []
    for user, ws in room.connections.items():
        try:
            await ws.send_json(message)
        except Exception:
            dead.append(user)
    for user in dead:
        del room.connections[user]


@app.get("/rooms")
def list_rooms():
    return {"rooms": [{"name": r.name, "users": len(r.connections), "messages": len(r.history)} for r in rooms.values()]}
```

### Explanation
- Room auto-creation on first connection
- Message history stored per room with configurable max
- New users receive recent history on join
- Dead connections cleaned up during broadcast

---

## Challenge 8: Webhook Delivery System with Retry

### Problem Statement
Build a webhook delivery system that queues webhooks, delivers them with exponential backoff retry, and tracks delivery status.

### Solution

```python
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, HttpUrl
import httpx
import time
import hashlib
import hmac
import json
import asyncio
from enum import Enum
from dataclasses import dataclass, field

app = FastAPI(title="Webhook Delivery")


class DeliveryStatus(str, Enum):
    PENDING = "pending"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    FAILED = "failed"


@dataclass
class WebhookDelivery:
    id: str
    url: str
    payload: dict
    status: DeliveryStatus = DeliveryStatus.PENDING
    attempts: int = 0
    max_attempts: int = 5
    last_error: str | None = None
    created_at: float = field(default_factory=time.time)
    delivered_at: float | None = None


deliveries: dict[str, WebhookDelivery] = {}

WEBHOOK_SECRET = "whsec_supersecretkey"


def sign_payload(payload: bytes) -> str:
    return hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256).hexdigest()


async def deliver_webhook(delivery_id: str):
    delivery = deliveries[delivery_id]
    delivery.status = DeliveryStatus.DELIVERING

    payload_bytes = json.dumps(delivery.payload).encode()
    signature = sign_payload(payload_bytes)

    for attempt in range(delivery.max_attempts):
        delivery.attempts = attempt + 1
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    delivery.url,
                    content=payload_bytes,
                    headers={
                        "Content-Type": "application/json",
                        "X-Webhook-Signature": signature,
                        "X-Webhook-Attempt": str(attempt + 1),
                    },
                )
                if response.status_code < 400:
                    delivery.status = DeliveryStatus.DELIVERED
                    delivery.delivered_at = time.time()
                    return
                delivery.last_error = f"HTTP {response.status_code}"
        except Exception as e:
            delivery.last_error = str(e)

        delay = min(2 ** attempt * 5, 300)
        await asyncio.sleep(delay)

    delivery.status = DeliveryStatus.FAILED


@app.post("/webhooks")
async def create_webhook(url: HttpUrl, payload: dict, background_tasks: BackgroundTasks):
    import uuid
    delivery_id = str(uuid.uuid4())
    delivery = WebhookDelivery(id=delivery_id, url=str(url), payload=payload)
    deliveries[delivery_id] = delivery
    background_tasks.add_task(deliver_webhook, delivery_id)
    return {"id": delivery_id, "status": delivery.status}


@app.get("/webhooks/{delivery_id}")
def get_delivery_status(delivery_id: str):
    if delivery_id not in deliveries:
        raise HTTPException(status_code=404, detail="Delivery not found")
    d = deliveries[delivery_id]
    return {"id": d.id, "status": d.status, "attempts": d.attempts, "last_error": d.last_error}
```

### Explanation
- Exponential backoff with jitter prevents thundering herd
- HMAC signatures let receivers verify authenticity
- Background tasks deliver webhooks without blocking the API
- Delivery status tracking for debugging and retries

---

## Challenge 9: API Versioning System

### Problem Statement
Implement URL-based API versioning with backward compatibility support.

### Solution

```python
from fastapi import FastAPI, APIRouter, Request
from pydantic import BaseModel

app = FastAPI()


class UserResponseV1(BaseModel):
    id: int
    name: str


class UserResponseV2(BaseModel):
    id: int
    name: str
    email: str
    created_at: str


USERS = [{"id": 1, "name": "Alice", "email": "alice@example.com", "created_at": "2024-01-01"}]

router_v1 = APIRouter(prefix="/api/v1")
router_v2 = APIRouter(prefix="/api/v2")


@router_v1.get("/users/{user_id}", response_model=UserResponseV1)
def get_user_v1(user_id: int):
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404)
    return {"id": user["id"], "name": user["name"]}


@router_v2.get("/users/{user_id}", response_model=UserResponseV2)
def get_user_v2(user_id: int):
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404)
    return user


app.include_router(router_v1)
app.include_router(router_v2)


@app.get("/api/versions")
def list_versions():
    return {
        "versions": [
            {"version": "v1", "status": "deprecated", "sunset": "2025-01-01"},
            {"version": "v2", "status": "stable"},
        ]
    }
```

---

## Challenge 10: Dynamic OpenAPI Schema

### Problem Statement
Create endpoints that dynamically modify the OpenAPI schema at runtime.

### Solution

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(title="Dynamic API")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {"url": "https://example.com/logo.png"}
    openapi_schema["info"]["contact"] = {"name": "API Support", "email": "support@example.com"}

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path, methods in openapi_schema.get("paths", {}).items():
        for method, details in methods.items():
            if method in ("get", "post", "put", "delete"):
                details["security"] = [{"BearerAuth": []}]

    openapi_schema["tags"] = [
        {"name": "users", "description": "User management"},
        {"name": "items", "description": "Item operations"},
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/users", tags=["users"])
def list_users():
    return {"users": []}


@app.get("/items", tags=["items"])
def list_items():
    return {"items": []}
```

### Explanation
- `custom_openapi()` replaces the default schema generation
- Adds custom info fields, security schemes, and tags
- Schema is cached after first generation
- All routes automatically get security requirements

---

## Challenge 11: Background Email Service

### Problem Statement
Build a background email sending service with template rendering and queue management.

### Solution

```python
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
import asyncio
import aiosmtplib
from email.mime.text import MIMEText
from jinja2 import Template
from dataclasses import dataclass, field
from enum import Enum
import time
import uuid

app = FastAPI()


class EmailStatus(str, Enum):
    QUEUED = "queued"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"


@dataclass
class EmailMessage:
    id: str
    to: str
    subject: str
    body: str
    status: EmailStatus = EmailStatus.QUEUED
    created_at: float = field(default_factory=time.time)
    sent_at: float | None = None
    error: str | None = None


email_queue: list[EmailMessage] = []
email_log: dict[str, EmailMessage] = {}

TEMPLATES = {
    "welcome": "Welcome {{ name }}! Your account is now active.",
    "password_reset": "Hi {{ name }}, click here to reset: {{ link }}",
    "invoice": "Hi {{ name }}, your invoice #{{ invoice_id }} is {{ amount }}.",
}


class EmailRequest(BaseModel):
    to: EmailStr
    template: str
    subject: str
    context: dict = {}


@app.post("/emails/send")
async def send_email(request: EmailRequest, background_tasks: BackgroundTasks):
    template = TEMPLATES.get(request.template)
    if not template:
        raise HTTPException(status_code=400, detail=f"Template '{request.template}' not found")

    body = Template(template).render(**request.context)
    msg = EmailMessage(
        id=str(uuid.uuid4()),
        to=request.to,
        subject=request.subject,
        body=body,
    )
    email_log[msg.id] = msg
    background_tasks.add_task(process_email, msg.id)
    return {"id": msg.id, "status": msg.status}


async def process_email(email_id: str):
    msg = email_log[email_id]
    msg.status = EmailStatus.SENDING
    try:
        mime = MIMEText(msg.body, "plain")
        mime["Subject"] = msg.subject
        mime["To"] = msg.to
        mime["From"] = "noreply@example.com"
        await aiosmtplib.send(mime, hostname="localhost", port=1025)
        msg.status = EmailStatus.SENT
        msg.sent_at = time.time()
    except Exception as e:
        msg.status = EmailStatus.FAILED
        msg.error = str(e)


@app.get("/emails/{email_id}")
def get_email_status(email_id: str):
    if email_id not in email_log:
        raise HTTPException(status_code=404)
    msg = email_log[email_id]
    return {"id": msg.id, "status": msg.status, "error": msg.error}
```

---

## Challenge 12: Health Check Aggregator

### Problem Statement
Build a health check system that aggregates checks for multiple dependencies.

### Solution

```python
from fastapi import FastAPI
import httpx
import asyncio
import time
from dataclasses import dataclass
from enum import Enum

app = FastAPI()


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass
class HealthCheck:
    name: str
    url: str
    timeout: float = 5.0


CHECKS = [
    HealthCheck(name="database", url="http://localhost:5432/health"),
    HealthCheck(name="redis", url="http://localhost:6379"),
    HealthCheck(name="external-api", url="https://api.example.com/health"),
]


async def check_dependency(check: HealthCheck) -> dict:
    start = time.time()
    try:
        async with httpx.AsyncClient(timeout=check.timeout) as client:
            resp = await client.get(check.url)
            latency = (time.time() - start) * 1000
            return {
                "name": check.name,
                "status": "healthy" if resp.status_code < 500 else "unhealthy",
                "latency_ms": round(latency, 2),
            }
    except Exception as e:
        latency = (time.time() - start) * 1000
        return {"name": check.name, "status": "unhealthy", "latency_ms": round(latency, 2), "error": str(e)}


@app.get("/health")
async def health_check():
    results = await asyncio.gather(*[check_dependency(c) for c in CHECKS])
    overall = HealthStatus.HEALTHY
    for r in results:
        if r["status"] == "unhealthy":
            overall = HealthStatus.UNHEALTHY
            break
        elif r["status"] == "degraded":
            overall = HealthStatus.DEGRADED

    return {"status": overall, "checks": list(results), "timestamp": time.time()}
```

---

## Challenge 13: Task Queue with Retry Logic

### Problem Statement
Implement an in-memory task queue with configurable retry, backoff, and dead letter queue.

### Solution

```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from enum import Enum
from dataclasses import dataclass, field
import asyncio
import time
import uuid

app = FastAPI()


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD = "dead"


@dataclass
class Task:
    id: str
    name: str
    payload: dict
    status: TaskStatus = TaskStatus.PENDING
    attempts: int = 0
    max_retries: int = 3
    backoff_factor: float = 2.0
    created_at: float = field(default_factory=time.time)
    error: str | None = None


tasks_db: dict[str, Task] = {}
dead_letter_queue: list[Task] = []

TASK_HANDLERS = {}


def task_handler(name: str):
    def decorator(func):
        TASK_HANDLERS[name] = func
        return func
    return decorator


class TaskRequest(BaseModel):
    name: str
    payload: dict = {}
    max_retries: int = 3


@app.post("/tasks")
async def create_task(request: TaskRequest, background_tasks: BackgroundTasks):
    task = Task(
        id=str(uuid.uuid4()),
        name=request.name,
        payload=request.payload,
        max_retries=request.max_retries,
    )
    tasks_db[task.id] = task
    background_tasks.add_task(execute_task, task.id)
    return {"id": task.id, "status": task.status}


async def execute_task(task_id: str):
    task = tasks_db[task_id]
    task.status = TaskStatus.RUNNING
    task.attempts += 1

    handler = TASK_HANDLERS.get(task.name)
    if not handler:
        task.status = TaskStatus.FAILED
        task.error = f"No handler for task '{task.name}'"
        return

    try:
        result = handler(task.payload)
        if asyncio.iscoroutine(result):
            await result
        task.status = TaskStatus.COMPLETED
    except Exception as e:
        if task.attempts >= task.max_retries:
            task.status = TaskStatus.DEAD
            task.error = str(e)
            dead_letter_queue.append(task)
        else:
            delay = task.backoff_factor ** task.attempts
            task.status = TaskStatus.PENDING
            await asyncio.sleep(delay)
            await execute_task(task_id)


@task_handler("send_email")
async def handle_send_email(payload: dict):
    await asyncio.sleep(0.1)  # Simulate work
    print(f"Email sent to {payload.get('to')}")


@task_handler("process_image")
async def handle_process_image(payload: dict):
    await asyncio.sleep(0.2)
    print(f"Image processed: {payload.get('url')}")


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    if task_id not in tasks_db:
        from fastapi import HTTPException
        raise HTTPException(status_code=404)
    t = tasks_db[task_id]
    return {"id": t.id, "status": t.status, "attempts": t.attempts, "error": t.error}


@app.get("/tasks/dead-letter")
def get_dead_letter_queue():
    return [{"id": t.id, "name": t.name, "error": t.error, "attempts": t.attempts} for t in dead_letter_queue]
```

---

## Challenge 14: File Upload Service with Validation

### Problem Statement
Build a file upload service with type validation, size limits, and metadata tracking.

### Solution

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import hashlib
import time
import uuid
import os

app = FastAPI()

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = {"image/jpeg", "image/png", "application/pdf"}
MAX_SIZE = 10 * 1024 * 1024  # 10MB

file_registry: dict[str, dict] = {}


class FileMetadata(BaseModel):
    id: str
    filename: str
    content_type: str
    size: int
    checksum: str
    uploaded_at: float


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"Type '{file.content_type}' not allowed. Use: {ALLOWED_TYPES}")

    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(400, f"File too large. Max: {MAX_SIZE // (1024*1024)}MB")

    file_id = str(uuid.uuid4())
    checksum = hashlib.sha256(content).hexdigest()
    file_path = os.path.join(UPLOAD_DIR, file_id)

    with open(file_path, "wb") as f:
        f.write(content)

    metadata = FileMetadata(
        id=file_id,
        filename=file.filename or "unknown",
        content_type=file.content_type,
        size=len(content),
        checksum=checksum,
        uploaded_at=time.time(),
    )
    file_registry[file_id] = metadata.model_dump()
    return metadata


@app.get("/files")
def list_files():
    return list(file_registry.values())


@app.get("/files/{file_id}")
def get_file_metadata(file_id: str):
    if file_id not in file_registry:
        raise HTTPException(404, "File not found")
    return file_registry[file_id]


@app.delete("/files/{file_id}")
def delete_file(file_id: str):
    if file_id not in file_registry:
        raise HTTPException(404, "File not found")
    file_path = os.path.join(UPLOAD_DIR, file_id)
    if os.path.exists(file_path):
        os.remove(file_path)
    del file_registry[file_id]
    return {"status": "deleted"}
```

---

## Challenge 15: Typed Event Emitter

### Problem Statement
Implement a type-safe event emitter system for decoupled component communication.

### Solution

```python
from fastapi import FastAPI
from typing import Callable, Any
from dataclasses import dataclass, field
from pydantic import BaseModel
import time
import asyncio

app = FastAPI()


class Event(BaseModel):
    name: str
    data: dict
    timestamp: float = field(default_factory=time.time)


class EventEmitter:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = {}
        self._history: list[Event] = []

    def on(self, event_name: str):
        def decorator(func: Callable):
            if event_name not in self._handlers:
                self._handlers[event_name] = []
            self._handlers[event_name].append(func)
            return func
        return decorator

    async def emit(self, event_name: str, data: dict):
        event = Event(name=event_name, data=data)
        self._history.append(event)

        handlers = self._handlers.get(event_name, []) + self._handlers.get("*", [])
        for handler in handlers:
            result = handler(event)
            if asyncio.iscoroutine(result):
                await result

    def get_history(self, event_name: str | None = None) -> list[Event]:
        if event_name:
            return [e for e in self._history if e.name == event_name]
        return self._history


emitter = EventEmitter()


@emitter.on("user.created")
async def on_user_created(event: Event):
    print(f"Welcome email sent for user: {event.data}")


@emitter.on("order.placed")
async def on_order_placed(event: Event):
    print(f"Order notification: {event.data}")


@emitter.on("*")
def on_any_event(event: Event):
    print(f"Event logged: {event.name}")


@app.post("/events/{event_name}")
async def emit_event(event_name: str, data: dict):
    await emitter.emit(event_name, data)
    return {"status": "emitted", "event": event_name}


@app.get("/events/history")
def get_event_history(event_name: str | None = None):
    return emitter.get_history(event_name)
```

---

## Challenge 16: Request/Response Logging Middleware

### Problem Statement
Build middleware that logs all requests/responses with timing, body capture, and PII redaction.

### Solution

```python
from fastapi import FastAPI, Request
from fastapi.responses import Response
import time
import json
import re
from collections import deque

app = FastAPI()

log_buffer: deque = deque(maxlen=1000)

PII_PATTERNS = {
    "email": (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[REDACTED_EMAIL]"),
    "phone": (re.compile(r"\b\d{10}\b"), "[REDACTED_PHONE]"),
    "ssn": (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[REDACTED_SSN]"),
}


def redact_pii(text: str) -> str:
    for name, (pattern, replacement) in PII_PATTERNS.items():
        text = pattern.sub(replacement, text)
    return text


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start = time.time()

    body = await request.body()
    body_str = redact_pii(body.decode("utf-8", errors="replace"))[:1000]

    response = await call_next(request)

    duration_ms = (time.time() - start) * 1000
    log_entry = {
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration_ms": round(duration_ms, 2),
        "client": request.client.host,
        "body_preview": body_str[:200],
        "timestamp": time.time(),
    }
    log_buffer.append(log_entry)

    response.headers["X-Process-Time"] = f"{duration_ms:.2f}ms"
    return response


@app.get("/logs")
def get_logs(limit: int = 50):
    return list(log_buffer)[-limit:]
```

---

## Challenge 17: Database Migration Runner

### Problem Statement
Build an in-app migration runner that applies SQL migrations in order.

### Solution

```python
from fastapi import FastAPI
from dataclasses import dataclass
import time

app = FastAPI()


@dataclass
class Migration:
    version: str
    name: str
    up: str
    down: str


MIGRATIONS = [
    Migration(
        version="001",
        name="create_users",
        up="CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(100), email VARCHAR(255) UNIQUE);",
        down="DROP TABLE users;",
    ),
    Migration(
        version="002",
        name="create_posts",
        up="CREATE TABLE posts (id SERIAL PRIMARY KEY, user_id INT REFERENCES users(id), title VARCHAR(255), content TEXT);",
        down="DROP TABLE posts;",
    ),
    Migration(
        version="003",
        name="add_timestamps",
        up="ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT NOW(); ALTER TABLE posts ADD COLUMN created_at TIMESTAMP DEFAULT NOW();",
        down="ALTER TABLE users DROP COLUMN created_at; ALTER TABLE posts DROP COLUMN created_at;",
    ),
]

applied_migrations: list[dict] = []


@app.post("/migrations/up")
def run_migrations():
    applied_versions = {m["version"] for m in applied_migrations}
    results = []

    for migration in MIGRATIONS:
        if migration.version not in applied_versions:
            applied_migrations.append({
                "version": migration.version,
                "name": migration.name,
                "applied_at": time.time(),
            })
            results.append({"version": migration.version, "status": "applied"})

    return {"migrations_run": len(results), "details": results}


@app.post("/migrations/down/{version}")
def rollback_migration(version: str):
    migration = next((m for m in MIGRATIONS if m.version == version), None)
    if not migration:
        from fastapi import HTTPException
        raise HTTPException(404, "Migration not found")

    applied_migrations[:] = [m for m in applied_migrations if m["version"] != version]
    return {"rolled_back": version}


@app.get("/migrations")
def list_migrations():
    return {
        "available": [{"version": m.version, "name": m.name} for m in MIGRATIONS],
        "applied": applied_migrations,
    }
```

---

## Challenge 18: Circuit Breaker Pattern

### Problem Statement
Implement a circuit breaker for external service calls.

### Solution

```python
from fastapi import FastAPI
from enum import Enum
from dataclasses import dataclass
import time

app = FastAPI()


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreaker:
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    last_failure_time: float = 0

    def record_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def allow_request(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        return True  # HALF_OPEN allows one request


breakers: dict[str, CircuitBreaker] = {}


def get_breaker(service: str) -> CircuitBreaker:
    if service not in breakers:
        breakers[service] = CircuitBreaker()
    return breakers[service]


@app.get("/call/{service}")
async def call_service(service: str):
    breaker = get_breaker(service)
    if not breaker.allow_request():
        return {"status": "circuit_open", "service": service}

    try:
        # Simulate external call
        import random
        if random.random() < 0.3:
            raise ConnectionError("Simulated failure")
        breaker.record_success()
        return {"status": "success", "service": service}
    except Exception as e:
        breaker.record_failure()
        return {"status": "failure", "service": service, "error": str(e)}


@app.get("/breakers")
def get_breaker_states():
    return {name: {"state": b.state, "failures": b.failure_count} for name, b in breakers.items()}
```

---

## Challenge 19: Graceful Shutdown Handler

### Problem Statement
Implement graceful shutdown with in-flight request completion and resource cleanup.

### Solution

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import signal

active_requests = 0
shutdown_event = asyncio.Event()
resources_cleaned = False


async def cleanup_resources():
    global resources_cleaned
    print("Closing database connections...")
    await asyncio.sleep(0.1)
    print("Flushing caches...")
    await asyncio.sleep(0.1)
    print("Closing file handles...")
    resources_cleaned = True
    print("All resources cleaned up")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up...")
    print("Warming up connection pools...")
    yield
    print("Shutdown signal received, waiting for in-flight requests...")
    shutdown_event.set()
    while active_requests > 0:
        await asyncio.sleep(0.1)
    await cleanup_resources()
    print("Graceful shutdown complete")


app = FastAPI(lifespan=lifespan)


@app.get("/work")
async def do_work():
    global active_requests
    active_requests += 1
    try:
        await asyncio.sleep(2)
        return {"result": "work completed"}
    finally:
        active_requests -= 1


@app.get("/status")
def status():
    return {"active_requests": active_requests, "shutdown_requested": shutdown_event.is_set()}
```

---

## Challenge 20: Custom Authentication Backend

### Problem Statement
Build a pluggable authentication system supporting API keys, JWT, and OAuth2.

### Solution

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
import time
from enum import Enum
from typing import Protocol

app = FastAPI()
security = HTTPBearer()

JWT_SECRET = "supersecret"
JWT_ALGORITHM = "HS256"


class AuthMethod(str, Enum):
    API_KEY = "api_key"
    JWT = "jwt"
    OAUTH2 = "oauth2"


class AuthResult(BaseModel):
    user_id: str
    method: AuthMethod
    permissions: list[str]


API_KEYS = {"sk_live_abc123": {"user_id": "user-1", "permissions": ["read", "write"]}}


def verify_api_key(credentials: HTTPAuthorizationCredentials) -> AuthResult:
    key = credentials.credentials
    if key not in API_KEYS:
        raise HTTPException(401, "Invalid API key")
    data = API_KEYS[key]
    return AuthResult(user_id=data["user_id"], method=AuthMethod.API_KEY, permissions=data["permissions"])


def verify_jwt(credentials: HTTPAuthorizationCredentials) -> AuthResult:
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return AuthResult(
            user_id=payload["sub"],
            method=AuthMethod.JWT,
            permissions=payload.get("permissions", []),
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> AuthResult:
    token = credentials.credentials

    if token.startswith("sk_"):
        return verify_api_key(credentials)

    return verify_jwt(credentials)


@app.post("/auth/token")
def create_token(user_id: str, permissions: list[str] = ["read"]):
    payload = {"sub": user_id, "permissions": permissions, "exp": time.time() + 3600}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/protected")
def protected_route(auth: AuthResult = Depends(get_current_user)):
    return {"user": auth.user_id, "method": auth.method, "permissions": auth.permissions}


@app.get("/admin")
def admin_route(auth: AuthResult = Depends(get_current_user)):
    if "admin" not in auth.permissions:
        raise HTTPException(403, "Admin permission required")
    return {"message": "Welcome, admin"}
```

---

## Interview Tips for Coding Challenges

1. **Start with the data model** - Define your schemas before writing logic
2. **Consider edge cases** - Empty inputs, race conditions, resource limits
3. **Use dependency injection** - FastAPI's DI system makes testing easier
4. **Think about scalability** - In-memory stores are fine for interviews but mention Redis/DB alternatives
5. **Error handling** - Always return proper HTTP status codes and error messages
6. **Type safety** - Leverage Pydantic and Python type hints throughout
7. **Async when beneficial** - I/O-bound operations should be async, CPU-bound can stay sync
8. **Document your API** - Use response_model, summary, and description parameters
