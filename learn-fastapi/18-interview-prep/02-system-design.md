# System Design Questions with FastAPI

## System 1: URL Shortener (like bit.ly)

### Requirements
- Shorten long URLs to ~7 character codes
- Redirect short URLs to original destinations
- Track click analytics (count, timestamp, referrer, location)
- Handle 100M+ URLs, 1B+ redirects/day
- URLs expire after configurable TTL

### Architecture

```
                    ┌─────────────┐
                    │   Client     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Load Balancer│
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼─────┐ ┌───▼────┐ ┌────▼────┐
        │ API Server │ │ API Srv│ │ API Srv │
        │ (FastAPI)  │ │        │ │         │
        └─────┬──────┘ └───┬────┘ └────┬────┘
              │            │            │
        ┌─────▼──────┐ ┌──▼───────┐ ┌──▼───────┐
        │  Redis     │ │ PostgreSQL│ │ Clickhouse│
        │ (Cache)    │ │ (Primary) │ │ (Analytics)│
        └────────────┘ └──────────┘ └──────────┘
```

### Data Models

```python
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from enum import Enum
import hashlib
import string
import time

class URLCreate(BaseModel):
    long_url: HttpUrl
    custom_alias: str | None = None
    expires_in_days: int | None = None

class URLResponse(BaseModel):
    short_url: str
    long_url: str
    created_at: datetime
    expires_at: datetime | None = None
    click_count: int = 0

class ClickEvent(BaseModel):
    short_code: str
    timestamp: datetime
    ip_address: str
    user_agent: str
    referrer: str | None = None
    country: str | None = None

class AnalyticsResponse(BaseModel):
    total_clicks: int
    clicks_by_day: list[dict]
    top_referrers: list[dict]
    top_countries: list[dict]
```

### API Design

```python
from fastapi import FastAPI, HTTPException, Request, Query, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import hashlib
import string
import time
from collections import defaultdict

app = FastAPI(title="URL Shortener", version="2.0")

# In-memory stores (replace with Redis/DB in production)
url_store: dict[str, dict] = {}
analytics_store: dict[str, list[dict]] = defaultdict(list)
user_urls: dict[str, list[str]] = defaultdict(list)


class URLCreate(BaseModel):
    long_url: str
    custom_alias: str | None = None
    expires_in_days: int | None = None


def generate_code(url: str, length: int = 7) -> str:
    hash_hex = hashlib.sha256(url.encode() + str(time.time()).encode()).hexdigest()
    chars = string.ascii_letters + string.digits
    return "".join(chars[int(hash_hex[i*2:i*2+2], 16) % len(chars)] for i in range(length))


@app.post("/api/v1/urls", response_model=dict, status_code=201)
def create_short_url(payload: URLCreate):
    if payload.custom_alias:
        if payload.custom_alias in url_store:
            raise HTTPException(409, "Alias already taken")
        code = payload.custom_alias
    else:
        code = generate_code(payload.long_url)

    expires_at = None
    if payload.expires_in_days:
        expires_at = time.time() + (payload.expires_in_days * 86400)

    url_store[code] = {
        "long_url": payload.long_url,
        "created_at": time.time(),
        "expires_at": expires_at,
        "clicks": 0,
    }

    return {
        "short_url": f"https://short.ly/{code}",
        "code": code,
        "long_url": payload.long_url,
    }


@app.get("/{code}")
def redirect(code: str, request: Request):
    if code not in url_store:
        raise HTTPException(404, "URL not found")

    data = url_store[code]
    if data["expires_at"] and data["expires_at"] < time.time():
        raise HTTPException(410, "URL expired")

    data["clicks"] += 1
    analytics_store[code].append({
        "timestamp": time.time(),
        "ip": request.client.host,
        "user_agent": request.headers.get("user-agent", ""),
        "referrer": request.headers.get("referer"),
    })

    return RedirectResponse(url=data["long_url"], status_code=307)


@app.get("/api/v1/urls/{code}/analytics")
def get_analytics(code: str):
    if code not in url_store:
        raise HTTPException(404, "URL not found")

    clicks = analytics_store.get(code, [])
    return {
        "total_clicks": len(clicks),
        "recent_clicks": clicks[-10:],
        "unique_ips": len(set(c["ip"] for c in clicks)),
    }


@app.delete("/api/v1/urls/{code}")
def delete_url(code: str):
    if code not in url_store:
        raise HTTPException(404, "URL not found")
    del url_store[code]
    analytics_store.pop(code, None)
    return {"status": "deleted"}
```

### Scaling Considerations

| Component | Small Scale | Medium Scale | Large Scale |
|-----------|-------------|--------------|-------------|
| Storage | PostgreSQL | PostgreSQL + Read Replicas | PostgreSQL + Citus (sharding) |
| Cache | In-memory | Redis Cluster | Redis Cluster + CDN |
| Analytics | PostgreSQL | ClickHouse | ClickHouse + Kafka pipeline |
| URL Generation | Hash-based | Counter-based + Base62 | Distributed ID generator (Snowflake) |
| Redirects | Application server | nginx + application | CDN edge + application |

### Trade-offs
- **Hash vs Counter IDs**: Hashes are stateless but have collisions; counters are sequential but need coordination
- **SQL vs NoSQL**: SQL for ACID compliance on URL mappings; NoSQL for high-read analytics
- **Cache TTL**: Longer TTL = faster reads but stale data; shorter = more DB hits
- **Click deduplication**: Storing every click enables analytics but increases storage; sampling reduces accuracy

---

## System 2: Real-Time Chat System

### Requirements
- 1-on-1 and group messaging
- Message delivery guarantees (at-least-once)
- Online presence tracking
- Message history and search
- Support 100K concurrent users per room

### Architecture

```
                    ┌──────────────┐
                    │    Client     │
                    └──────┬───────┘
                           │ WebSocket
                    ┌──────▼───────┐
                    │  WS Gateway  │
                    │  (FastAPI)    │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼─────┐ ┌───▼────┐ ┌────▼────┐
        │  Redis     │ │  Redis  │ │PostgreSQL│
        │ Pub/Sub    │ │ Cluster │ │ (Messages)│
        │(Broadcast) │ │ (Cache) │ │          │
        └────────────┘ └────────┘ └──────────┘
```

### Implementation

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Query
from pydantic import BaseModel
from dataclasses import dataclass, field
import json
import time
import asyncio
from collections import defaultdict

app = FastAPI(title="Chat API")


# ── Data Models ──────────────────────────────────────────────

@dataclass
class Message:
    id: str
    room_id: str
    sender_id: str
    content: str
    timestamp: float
    read_by: list[str] = field(default_factory=list)


@dataclass
class Room:
    id: str
    name: str
    members: set[str] = field(default_factory=set)
    is_group: bool = False
    created_at: float = field(default_factory=time.time)


# ── Stores ───────────────────────────────────────────────────

rooms: dict[str, Room] = {}
messages: dict[str, list[Message]] = defaultdict(list)
connections: dict[str, WebSocket] = {}
online_users: set[str] = set()
typing_users: dict[str, set[str]] = defaultdict(set)


# ── Connection Manager ──────────────────────────────────────

class ConnectionManager:
    def __init__(self):
        self.user_connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, ws: WebSocket, user_id: str):
        await ws.accept()
        self.user_connections[user_id].append(ws)
        connections[user_id] = ws
        online_users.add(user_id)
        await self.broadcast_presence(user_id, "online")

    def disconnect(self, ws: WebSocket, user_id: str):
        self.user_connections[user_id].remove(ws)
        if not self.user_connections[user_id]:
            connections.pop(user_id, None)
            if user_id not in [
                u for conns in self.user_connections.values()
                for u, s in [(None, None)]  # simplified check
            ]:
                online_users.discard(user_id)

    async def send_personal(self, user_id: str, message: dict):
        for ws in self.user_connections.get(user_id, []):
            try:
                await ws.send_json(message)
            except Exception:
                pass

    async def broadcast_to_room(self, room_id: str, message: dict, exclude: str | None = None):
        room = rooms.get(room_id)
        if not room:
            return
        for member_id in room.members:
            if member_id != exclude:
                await self.send_personal(member_id, message)

    async def broadcast_presence(self, user_id: str, status: str):
        for room_id, room in rooms.items():
            if user_id in room.members:
                await self.broadcast_to_room(room_id, {
                    "type": "presence",
                    "user_id": user_id,
                    "status": status,
                })


manager = ConnectionManager()


# ── WebSocket Handler ───────────────────────────────────────

@app.websocket("/ws/{user_id}")
async def websocket_handler(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "message":
                room_id = data["room_id"]
                content = data["content"]

                msg = Message(
                    id=f"{room_id}-{time.time()}",
                    room_id=room_id,
                    sender_id=user_id,
                    content=content,
                    timestamp=time.time(),
                )
                messages[room_id].append(msg)

                await manager.broadcast_to_room(room_id, {
                    "type": "message",
                    "id": msg.id,
                    "sender_id": msg.sender_id,
                    "content": msg.content,
                    "timestamp": msg.timestamp,
                })

            elif msg_type == "typing":
                room_id = data["room_id"]
                if data.get("is_typing"):
                    typing_users[room_id].add(user_id)
                else:
                    typing_users[room_id].discard(user_id)

                await manager.broadcast_to_room(room_id, {
                    "type": "typing",
                    "room_id": room_id,
                    "users": list(typing_users[room_id]),
                }, exclude=user_id)

            elif msg_type == "read":
                room_id = data["room_id"]
                msg_id = data["message_id"]
                for msg in reversed(messages[room_id]):
                    if msg.id == msg_id:
                        if user_id not in msg.read_by:
                            msg.read_by.append(user_id)
                        break

            elif msg_type == "join_room":
                room_id = data["room_id"]
                if room_id in rooms:
                    rooms[room_id].members.add(user_id)

            elif msg_type == "history":
                room_id = data["room_id"]
                limit = data.get("limit", 50)
                history = messages[room_id][-limit:]
                await websocket.send_json({
                    "type": "history",
                    "room_id": room_id,
                    "messages": [
                        {"id": m.id, "sender_id": m.sender_id, "content": m.content,
                         "timestamp": m.timestamp, "read_by": m.read_by}
                        for m in history
                    ],
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)


# ── REST Endpoints ──────────────────────────────────────────

class RoomCreate(BaseModel):
    name: str
    members: list[str] = []
    is_group: bool = False


@app.post("/rooms")
def create_room(payload: RoomCreate):
    import uuid
    room_id = str(uuid.uuid4())[:8]
    room = Room(id=room_id, name=payload.name, members=set(payload.members), is_group=payload.is_group)
    rooms[room_id] = room
    return {"id": room_id, "name": room.name, "members": list(room.members)}


@app.get("/rooms/{room_id}/messages")
def get_messages(room_id: str, limit: int = 50, offset: int = 0):
    if room_id not in rooms:
        raise HTTPException(404, "Room not found")
    room_msgs = messages[room_id]
    return {"messages": [
        {"id": m.id, "sender_id": m.sender_id, "content": m.content,
         "timestamp": m.timestamp, "read_by": m.read_by}
        for m in room_msgs[-limit - offset: -offset or None]
    ]}


@app.get("/online")
def get_online_users():
    return {"online": list(online_users)}
```

### Scaling Considerations
- **Single Server**: In-memory connection tracking works
- **Multi-Server**: Redis Pub/Sub for cross-server message broadcasting
- **100K+ per Room**: Fan-out on write with message queues; sharded Redis channels
- **Message History**: PostgreSQL with partitioned tables by time range
- **Presence**: Redis with TTL-based heartbeats (set key with 30s TTL, refresh on heartbeat)

### Trade-offs
- **Fan-out on Write vs Read**: Write-time fan-out is faster for reads but slower for large rooms
- **Message Ordering**: Sequential IDs via database sequences vs. Lamport timestamps for distributed
- **Delivery Guarantees**: At-least-once with deduplication vs. exactly-once (complex)
- **WebSocket vs SSE**: WebSocket for bidirectional; SSE for simpler server-push only

---

## System 3: E-Commerce API

### Requirements
- Product catalog with search and filtering
- Shopping cart with real-time sync
- Order processing with payment
- Inventory management
- Support 10K concurrent users, 1K orders/minute

### Architecture

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Client   │  │  Mobile   │  │  Admin   │
└─────┬─────┘  └─────┬─────┘  └────┬─────┘
      │              │              │
      └──────────────┼──────────────┘
                     │
              ┌──────▼──────┐
              │ API Gateway  │
              │  (FastAPI)   │
              └──────┬──────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼────┐    ┌──────▼──────┐   ┌────▼─────┐
│ Product │    │    Order     │   │  Payment  │
│ Service │    │   Service    │   │  Service  │
└───┬────┘    └──────┬──────┘   └────┬─────┘
    │                │                │
┌───▼────┐    ┌──────▼──────┐   ┌────▼─────┐
│  ES/PG  │    │ PostgreSQL  │   │  Stripe  │
│ (Search)│    │  (Orders)   │   │          │
└─────────┘    └─────────────┘   └──────────┘
```

### Implementation

```python
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from enum import Enum
import time
import uuid

app = FastAPI(title="E-Commerce API")


# ── Data Models ──────────────────────────────────────────────

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    stock: int
    tags: list[str] = []

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    category: str
    stock: int
    available: bool

class CartItem(BaseModel):
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    items: list[CartItem]
    shipping_address: dict

class PaymentCreate(BaseModel):
    order_id: str
    payment_method: str
    token: str | None = None


# ── Stores ───────────────────────────────────────────────────

products_db: dict[str, dict] = {}
cart_db: dict[str, list[dict]] = {}
orders_db: dict[str, dict] = {}


# ── Product Endpoints ───────────────────────────────────────

@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    product_id = str(uuid.uuid4())[:8]
    products_db[product_id] = {
        "id": product_id, **product.model_dump(), "available": product.stock > 0
    }
    return products_db[product_id]


@app.get("/products")
def list_products(
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
    sort_by: str = "name",
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    items = list(products_db.values())

    if category:
        items = [p for p in items if p["category"] == category]
    if min_price is not None:
        items = [p for p in items if p["price"] >= min_price]
    if max_price is not None:
        items = [p for p in items if p["price"] <= max_price]
    if search:
        search_lower = search.lower()
        items = [p for p in items if search_lower in p["name"].lower() or search_lower in p["description"].lower()]

    items.sort(key=lambda x: x.get(sort_by, x["name"]))

    total = len(items)
    start = (page - 1) * per_page
    paginated = items[start:start + per_page]

    return {
        "items": paginated,
        "total": total,
        "page": page,
        "pages": max(1, -(-total // per_page)),
    }


@app.get("/products/{product_id}")
def get_product(product_id: str):
    if product_id not in products_db:
        raise HTTPException(404, "Product not found")
    return products_db[product_id]


# ── Cart Endpoints ──────────────────────────────────────────

@app.post("/cart/{user_id}/items")
def add_to_cart(user_id: str, item: CartItem):
    if item.product_id not in products_db:
        raise HTTPException(404, "Product not found")

    product = products_db[item.product_id]
    if product["stock"] < item.quantity:
        raise HTTPException(400, f"Insufficient stock. Available: {product['stock']}")

    if user_id not in cart_db:
        cart_db[user_id] = []

    for cart_item in cart_db[user_id]:
        if cart_item["product_id"] == item.product_id:
            cart_item["quantity"] += item.quantity
            return {"cart": cart_db[user_id]}

    cart_db[user_id].append(item.model_dump())
    return {"cart": cart_db[user_id]}


@app.get("/cart/{user_id}")
def get_cart(user_id: str):
    cart_items = cart_db.get(user_id, [])
    total = 0.0
    for item in cart_items:
        product = products_db.get(item["product_id"])
        if product:
            total += product["price"] * item["quantity"]

    return {"items": cart_items, "total": round(total, 2)}


@app.delete("/cart/{user_id}/items/{product_id}")
def remove_from_cart(user_id: str, product_id: str):
    if user_id not in cart_db:
        raise HTTPException(404, "Cart is empty")

    cart_db[user_id] = [i for i in cart_db[user_id] if i["product_id"] != product_id]
    return {"status": "removed"}


# ── Order Endpoints ─────────────────────────────────────────

@app.post("/orders", status_code=201)
def create_order(user_id: str, payload: OrderCreate):
    order_items = []
    total = 0.0

    for item in payload.items:
        product = products_db.get(item.product_id)
        if not product:
            raise HTTPException(404, f"Product {item.product_id} not found")
        if product["stock"] < item.quantity:
            raise HTTPException(400, f"Insufficient stock for {product['name']}")

        product["stock"] -= item.quantity
        if product["stock"] == 0:
            product["available"] = False

        item_total = product["price"] * item.quantity
        total += item_total
        order_items.append({
            "product_id": item.product_id,
            "name": product["name"],
            "quantity": item.quantity,
            "price": product["price"],
            "subtotal": item_total,
        })

    order_id = str(uuid.uuid4())[:8]
    orders_db[order_id] = {
        "id": order_id,
        "user_id": user_id,
        "items": order_items,
        "total": round(total, 2),
        "status": "pending",
        "shipping": payload.shipping_address,
        "created_at": time.time(),
    }

    cart_db.pop(user_id, None)
    return orders_db[order_id]


@app.post("/orders/{order_id}/pay")
def process_payment(order_id: str, payment: PaymentCreate):
    if order_id not in orders_db:
        raise HTTPException(404, "Order not found")

    order = orders_db[order_id]
    # Simulate Stripe payment
    order["status"] = "paid"
    order["payment"] = {
        "method": payment.payment_method,
        "amount": order["total"],
        "transaction_id": f"txn_{uuid.uuid4().hex[:12]}",
        "paid_at": time.time(),
    }
    return order


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(404, "Order not found")
    return orders_db[order_id]


@app.get("/users/{user_id}/orders")
def list_user_orders(user_id: str):
    return [o for o in orders_db.values() if o["user_id"] == user_id]
```

### Scaling Considerations
- **Product Search**: Elasticsearch for full-text search with faceted filtering
- **Cart Sync**: Redis for real-time cart with pub/sub for multi-device sync
- **Order Processing**: Message queue (RabbitMQ/SQS) for async payment processing
- **Inventory**: Optimistic locking with version numbers to prevent overselling
- **Caching**: CDN for product images, Redis for hot product data

### Trade-offs
- **Inventory Reservation**: Reserve on cart add (safe but holds stock) vs. reserve on checkout (efficient but risky)
- **Payment Processing**: Synchronous (simple, user waits) vs. asynchronous (complex UX but higher throughput)
- **Cart Storage**: Server-side (cross-device sync) vs. client-side (no server cost but no sync)

---

## System 4: Social Media Feed API

### Requirements
- Post creation with text, images, videos
- Fan-out feed generation (following-based)
- Like, comment, share functionality
- Trending topics
- Support 10M users, 100M posts

### Architecture

```
┌──────────┐
│  Client   │
└─────┬────┘
      │
┌─────▼─────┐     ┌─────────────┐
│   API      │────▶│ Feed Cache   │
│ (FastAPI)  │     │   (Redis)    │
└─────┬─────┘     └─────────────┘
      │
┌─────▼─────┐     ┌─────────────┐
│  Worker    │────▶│ PostgreSQL  │
│ (Celery)   │     │             │
└────────────┘     └─────────────┘
```

### Implementation

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from dataclasses import dataclass, field
import time
import uuid
from collections import defaultdict

app = FastAPI(title="Social Feed API")

posts_db: dict[str, dict] = {}
users_db: dict[str, dict] = {}
follows: dict[str, set[str]] = defaultdict(set)  # user -> set of followed users
feed_cache: dict[str, list[str]] = defaultdict(list)  # user -> list of post_ids


class PostCreate(BaseModel):
    content: str
    media_urls: list[str] = []
    tags: list[str] = []


class CommentCreate(BaseModel):
    content: str


@app.post("/users", status_code=201)
def create_user(name: str, username: str):
    user_id = str(uuid.uuid4())[:8]
    users_db[user_id] = {"id": user_id, "name": name, "username": username, "followers": 0}
    return users_db[user_id]


@app.post("/users/{user_id}/follow/{target_id}")
def follow_user(user_id: str, target_id: str):
    if user_id not in users_db or target_id not in users_db:
        raise HTTPException(404, "User not found")
    follows[user_id].add(target_id)
    users_db[target_id]["followers"] += 1

    # Fan-out: add user's recent posts to follower's feed
    target_posts = [pid for pid, p in posts_db.items() if p["author_id"] == target_id][-20:]
    feed_cache[user_id] = target_posts + feed_cache[user_id]
    feed_cache[user_id] = feed_cache[user_id][:500]

    return {"status": "followed"}


@app.post("/posts", status_code=201)
def create_post(user_id: str, payload: PostCreate):
    if user_id not in users_db:
        raise HTTPException(404, "User not found")

    post_id = str(uuid.uuid4())[:8]
    post = {
        "id": post_id,
        "author_id": user_id,
        "content": payload.content,
        "media_urls": payload.media_urls,
        "tags": payload.tags,
        "likes": 0,
        "comments": [],
        "shares": 0,
        "created_at": time.time(),
    }
    posts_db[post_id] = post

    # Fan-out on write: push to all followers' feeds
    for follower_id in follows:
        if user_id in follows[follower_id]:
            feed_cache[follower_id].insert(0, post_id)
            feed_cache[follower_id] = feed_cache[follower_id][:500]

    return post


@app.get("/feed/{user_id}")
def get_feed(user_id: str, page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100)):
    if user_id not in users_db:
        raise HTTPException(404, "User not found")

    feed_post_ids = feed_cache.get(user_id, [])
    start = (page - 1) * per_page
    page_ids = feed_post_ids[start:start + per_page]

    feed = []
    for pid in page_ids:
        if pid in posts_db:
            p = posts_db[pid]
            author = users_db.get(p["author_id"], {})
            feed.append({**p, "author_name": author.get("name", "Unknown")})

    return {"feed": feed, "page": page, "has_more": start + per_page < len(feed_post_ids)}


@app.post("/posts/{post_id}/like")
def like_post(post_id: str, user_id: str):
    if post_id not in posts_db:
        raise HTTPException(404, "Post not found")
    posts_db[post_id]["likes"] += 1
    return {"likes": posts_db[post_id]["likes"]}


@app.post("/posts/{post_id}/comments", status_code=201)
def add_comment(post_id: str, user_id: str, payload: CommentCreate):
    if post_id not in posts_db:
        raise HTTPException(404, "Post not found")

    comment = {
        "id": str(uuid.uuid4())[:8],
        "user_id": user_id,
        "content": payload.content,
        "created_at": time.time(),
    }
    posts_db[post_id]["comments"].append(comment)
    return comment


@app.get("/trending")
def get_trending(hours: int = 24):
    cutoff = time.time() - (hours * 3600)
    tag_counts: dict[str, int] = defaultdict(int)

    for post in posts_db.values():
        if post["created_at"] > cutoff:
            for tag in post["tags"]:
                tag_counts[tag] += post["likes"] + len(post["comments"])

    trending = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    return {"trending": [{"tag": t, "score": s} for t, s in trending]}
```

### Scaling Considerations
- **Feed Generation**: Pre-computed feeds (fan-out on write) for small followings; pull-based for celebrities
- **Hot Users**: Celebrities with millions of followers need pull-based feed (lazy evaluation)
- **Timeline Storage**: Redis sorted sets for recent posts; Cassandra for long-term storage
- **Search**: Elasticsearch for post content and hashtag search
- **Media**: CDN + object storage (S3/R2) with lazy loading

### Trade-offs
- **Fan-out on Write vs Read**: Write-time fan-out is O(followers) per post but O(1) for reads; read-time is O(followings) per read
- **Feed Consistency**: Strong consistency is expensive; eventual consistency is acceptable for feeds
- **Celebrity Problem**: Special-case handling needed for users with millions of followers

---

## System 5: File Storage Service

### Requirements
- Upload/download files up to 1GB
- File versioning
- Sharing with permissions
- Folder organization
- 99.999% durability

### Implementation

```python
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import hashlib
import time
import uuid
import io

app = FastAPI(title="File Storage Service")

files_db: dict[str, dict] = {}
folders_db: dict[str, dict] = {}
file_versions: dict[str, list[dict]] = {}
file_content: dict[str, bytes] = {}  # Simulate object storage


class FolderCreate(BaseModel):
    name: str
    parent_id: str | None = None


class ShareRequest(BaseModel):
    user_id: str
    permission: str  # read, write, admin


@app.post("/folders", status_code=201)
def create_folder(payload: FolderCreate, user_id: str):
    folder_id = str(uuid.uuid4())[:8]
    folders_db[folder_id] = {
        "id": folder_id,
        "name": payload.name,
        "parent_id": payload.parent_id,
        "owner": user_id,
        "created_at": time.time(),
    }
    return folders_db[folder_id]


@app.post("/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    folder_id: str | None = None,
    user_id: str = "user-1",
):
    content = await file.read()
    if len(content) > 1_073_741_824:  # 1GB
        raise HTTPException(413, "File too large")

    checksum = hashlib.sha256(content).hexdigest()
    file_id = str(uuid.uuid4())[:8]
    version = 1

    files_db[file_id] = {
        "id": file_id,
        "name": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "checksum": checksum,
        "folder_id": folder_id,
        "owner": user_id,
        "version": version,
        "created_at": time.time(),
        "shares": [],
    }

    file_content[file_id] = content
    file_versions[file_id] = [{"version": version, "checksum": checksum, "uploaded_at": time.time(), "size": len(content)}]

    return files_db[file_id]


@app.get("/files/{file_id}")
def get_file_info(file_id: str):
    if file_id not in files_db:
        raise HTTPException(404, "File not found")
    return files_db[file_id]


@app.get("/files/{file_id}/download")
def download_file(file_id: str):
    if file_id not in files_db:
        raise HTTPException(404, "File not found")
    if file_id not in file_content:
        raise HTTPException(404, "File content not found")

    content = file_content[file_id]
    return StreamingResponse(
        io.BytesIO(content),
        media_type=files_db[file_id]["content_type"],
        headers={"Content-Disposition": f'attachment; filename="{files_db[file_id]["name"]}"'},
    )


@app.get("/files/{file_id}/versions")
def get_versions(file_id: str):
    if file_id not in file_versions:
        raise HTTPException(404, "File not found")
    return {"versions": file_versions[file_id]}


@app.post("/files/{file_id}/share")
def share_file(file_id: str, payload: ShareRequest):
    if file_id not in files_db:
        raise HTTPException(404, "File not found")
    files_db[file_id]["shares"].append({"user_id": payload.user_id, "permission": payload.permission})
    return {"status": "shared"}


@app.get("/folders/{folder_id}/contents")
def list_folder(folder_id: str):
    subfolders = [f for f in folders_db.values() if f["parent_id"] == folder_id]
    files = [f for f in files_db.values() if f["folder_id"] == folder_id]
    return {"folders": subfolders, "files": files}
```

---

## System 6: Notification System

### Requirements
- Multi-channel: push, email, SMS, in-app
- User preference management
- Priority-based delivery
- Rate limiting per user
- Template management

### Implementation

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from dataclasses import dataclass, field
import time
import uuid

app = FastAPI(title="Notification System")


class Channel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"


class Priority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class NotificationCreate(BaseModel):
    user_id: str
    title: str
    body: str
    channels: list[Channel]
    priority: Priority = Priority.NORMAL
    template_id: str | None = None
    template_data: dict = {}


class PreferencesUpdate(BaseModel):
    email_enabled: bool = True
    sms_enabled: bool = True
    push_enabled: bool = True
    quiet_hours_start: int | None = None  # 0-23
    quiet_hours_end: int | None = None


notifications_db: dict[str, dict] = {}
user_preferences: dict[str, dict] = {}
delivery_log: list[dict] = []
rate_limits: dict[str, list[float]] = {}


@app.put("/users/{user_id}/preferences")
def update_preferences(user_id: str, prefs: PreferencesUpdate):
    user_preferences[user_id] = prefs.model_dump()
    return user_preferences[user_id]


@app.post("/notifications", status_code=201)
def send_notification(payload: NotificationCreate):
    now = time.time()
    prefs = user_preferences.get(payload.user_id, {})

    # Rate limiting: max 100 notifications per hour
    user_rate = rate_limits.setdefault(payload.user_id, [])
    user_rate[:] = [t for t in user_rate if now - t < 3600]
    if len(user_rate) >= 100 and payload.priority != Priority.CRITICAL:
        raise HTTPException(429, "Rate limit exceeded")
    user_rate.append(now)

    # Quiet hours check
    hour = int(time.localtime(now).tm_hour)
    quiet_start = prefs.get("quiet_hours_start")
    quiet_end = prefs.get("quiet_hours_end")
    if quiet_start is not None and quiet_end is not None:
        if quiet_start <= hour < quiet_end and payload.priority != Priority.CRITICAL:
            # Queue for later delivery
            pass

    notification_id = str(uuid.uuid4())[:8]
    results = []

    for channel in payload.channels:
        if not prefs.get(f"{channel.value}_enabled", True):
            results.append({"channel": channel, "status": "skipped", "reason": "disabled"})
            continue

        delivery_log.append({
            "notification_id": notification_id,
            "channel": channel,
            "user_id": payload.user_id,
            "sent_at": now,
            "status": "sent",
        })
        results.append({"channel": channel, "status": "sent"})

    notifications_db[notification_id] = {
        "id": notification_id,
        "user_id": payload.user_id,
        "title": payload.title,
        "body": payload.body,
        "priority": payload.priority,
        "channels": payload.channels,
        "results": results,
        "created_at": now,
    }

    return notifications_db[notification_id]


@app.get("/users/{user_id}/notifications")
def list_notifications(user_id: str, unread_only: bool = False):
    user_notifs = [n for n in notifications_db.values() if n["user_id"] == user_id]
    return {"notifications": user_notifs[-50:]}
```

---

## System 7: Multi-Tenant SaaS API

### Requirements
- Team-based multi-tenancy
- Resource isolation
- Per-tenant configuration
- Usage tracking and billing
- Support 10K tenants

### Implementation

```python
from fastapi import FastAPI, Depends, HTTPException, Request
from pydantic import BaseModel
from contextvars import ContextVar
import time
import uuid

app = FastAPI(title="Multi-Tenant SaaS")

tenant_context: ContextVar[dict] = ContextVar("tenant", default={})

TENANTS_DB: dict[str, dict] = {
    "tenant-1": {
        "id": "tenant-1", "name": "Acme Corp", "plan": "enterprise",
        "max_users": 100, "features": ["sso", "audit", "api_keys"],
        "rate_limit": 10000, "storage_limit_gb": 100,
    },
    "tenant-2": {
        "id": "tenant-2", "name": "Startup Inc", "plan": "starter",
        "max_users": 5, "features": ["basic"],
        "rate_limit": 100, "storage_limit_gb": 5,
    },
}

usage_tracker: dict[str, dict] = {}


class TenantMiddleware:
    async def __call__(self, request: Request, call_next):
        tenant_id = request.headers.get("X-Tenant-ID")
        if not tenant_id:
            raise HTTPException(400, "X-Tenant-ID required")

        tenant = TENANTS_DB.get(tenant_id)
        if not tenant:
            raise HTTPException(404, "Tenant not found")

        # Usage tracking
        usage = usage_tracker.setdefault(tenant_id, {"api_calls": 0, "storage_bytes": 0})
        usage["api_calls"] += 1

        if usage["api_calls"] > tenant["rate_limit"]:
            raise HTTPException(429, "Tenant rate limit exceeded")

        token = tenant_context.set(tenant)
        try:
            response = await call_next(request)
            response.headers["X-Tenant-ID"] = tenant_id
            response.headers["X-Tenant-Plan"] = tenant["plan"]
            return response
        finally:
            tenant_context.reset(token)


@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    if request.url.path.startswith("/internal"):
        return await call_next(request)

    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id:
        return await call_next(request)

    tenant = TENANTS_DB.get(tenant_id)
    if not tenant:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=404, content={"detail": "Tenant not found"})

    usage = usage_tracker.setdefault(tenant_id, {"api_calls": 0})
    usage["api_calls"] += 1

    token = tenant_context.set(tenant)
    try:
        response = await call_next(request)
        response.headers["X-Tenant-ID"] = tenant_id
        return response
    finally:
        tenant_context.reset(token)


def get_tenant():
    tenant = tenant_context.get()
    if not tenant:
        raise HTTPException(400, "No tenant context")
    return tenant


@app.post("/tenants", status_code=201)
def create_tenant(name: str, plan: str = "starter"):
    tenant_id = f"tenant-{uuid.uuid4().hex[:6]}"
    plans = {
        "starter": {"max_users": 5, "rate_limit": 100, "features": ["basic"]},
        "enterprise": {"max_users": 100, "rate_limit": 10000, "features": ["sso", "audit", "api_keys"]},
    }
    config = plans.get(plan, plans["starter"])
    TENANTS_DB[tenant_id] = {"id": tenant_id, "name": name, "plan": plan, **config}
    return TENANTS_DB[tenant_id]


@app.get("/tenant/resources")
def get_tenant_resources(tenant: dict = Depends(get_tenant)):
    usage = usage_tracker.get(tenant["id"], {})
    return {
        "tenant": tenant["id"],
        "plan": tenant["plan"],
        "usage": usage,
        "limits": {"rate_limit": tenant["rate_limit"], "max_users": tenant["max_users"]},
    }


@app.get("/tenant/members")
def list_members(tenant: dict = Depends(get_tenant)):
    return {"tenant": tenant["id"], "members": []}


@app.get("/admin/tenants")
def list_all_tenants():
    return {"tenants": list(TENANTS_DB.values())}
```

---

## System 8: Rate-Limited API Gateway

### Requirements
- Per-user and per-IP rate limiting
- Multiple rate limit algorithms (sliding window, token bucket)
- API key management
- Request logging
- Proxy to backend services

### Implementation

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import time
import hashlib
from collections import defaultdict
from dataclasses import dataclass, field

app = FastAPI(title="API Gateway")


@dataclass
class TokenBucket:
    capacity: int
    refill_rate: float  # tokens per second
    tokens: float = 0
    last_refill: float = field(default_factory=time.time())

    def consume(self, tokens: int = 1) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


@dataclass
class SlidingWindowCounter:
    max_requests: int
    window_seconds: int
    requests: list = field(default_factory=list)

    def is_allowed(self) -> bool:
        now = time.time()
        cutoff = now - self.window_seconds
        self.requests = [t for t in self.requests if t > cutoff]
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False


api_keys: dict[str, dict] = {
    "gw_live_abc123": {"user_id": "user-1", "plan": "premium", "rate_limit": 1000},
    "gw_live_def456": {"user_id": "user-2", "plan": "free", "rate_limit": 100},
}

rate_limiters: dict[str, TokenBucket] = {}
request_logs: list[dict] = []

PROXY_TARGETS = {
    "/api/users": "http://user-service:8001",
    "/api/products": "http://product-service:8002",
    "/api/orders": "http://order-service:8003",
}


def get_or_create_limiter(api_key: str, rate_limit: int) -> TokenBucket:
    if api_key not in rate_limiters:
        rate_limiters[api_key] = TokenBucket(
            capacity=rate_limit,
            refill_rate=rate_limit / 60.0,
            tokens=rate_limit,
        )
    return rate_limiters[api_key]


@app.middleware("http")
async def gateway_middleware(request: Request, call_next):
    start = time.time()

    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return JSONResponse(status_code=401, content={"detail": "X-API-Key required"})

    key_data = api_keys.get(api_key)
    if not key_data:
        return JSONResponse(status_code=403, content={"detail": "Invalid API key"}")

    limiter = get_or_create_limiter(api_key, key_data["rate_limit"])
    if not limiter.consume():
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"},
            headers={"Retry-After": "1"},
        )

    response = await call_next(request)
    duration_ms = (time.time() - start) * 1000

    request_logs.append({
        "path": request.url.path,
        "method": request.method,
        "status": response.status_code,
        "duration_ms": round(duration_ms, 2),
        "api_key": api_key[:8] + "...",
        "user_id": key_data["user_id"],
        "timestamp": time.time(),
    })

    response.headers["X-RateLimit-Remaining"] = str(int(limiter.tokens))
    response.headers["X-Process-Time"] = f"{duration_ms:.2f}ms"
    return response


@app.get("/gateway/keys")
def list_api_keys():
    return [{"key": k[:8] + "...", "user": v["user_id"], "plan": v["plan"]} for k, v in api_keys.items()]


@app.get("/gateway/logs")
def get_logs(limit: int = 50):
    return {"logs": request_logs[-limit:]}
```

### Scaling Considerations
- **Distributed Rate Limiting**: Redis-based sliding window with Lua scripts for atomicity
- **API Key Storage**: PostgreSQL with Redis cache for hot keys
- **Request Logging**: Async logging pipeline to Elasticsearch/Kafka
- **Proxy Routing**: Consistent hashing for backend affinity
- **Circuit Breaking**: Per-backend health checks with automatic failover

---

## General System Design Tips

1. **Start with Requirements**: Clarify scale, latency, consistency needs before designing
2. **Draw the Architecture**: Components, data flow, and communication patterns
3. **Define APIs First**: RESTful endpoints with clear contracts
4. **Choose Data Stores**: Match storage to access patterns (OLTP vs OLAP vs cache)
5. **Plan for Failure**: Redundancy, graceful degradation, circuit breakers
6. **Monitor Everything**: Metrics, logs, traces from day one
7. **Iterate**: Start simple, scale components independently as needed
