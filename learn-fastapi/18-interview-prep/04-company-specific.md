# Company-Specific FastAPI Interview Questions

## Google / Meta Style (System Design + Coding)

### Question 1: Design a Distributed URL Shortener (Google-style)

**Interviewer context**: Google values scalability, distributed systems knowledge, and clean code.

```python
# ── Core Data Model ─────────────────────────────────────────

from pydantic import BaseModel
from datetime import datetime

class ShortenRequest(BaseModel):
    long_url: str
    custom_alias: str | None = None
    expires_at: datetime | None = None

class ShortenResponse(BaseModel):
    short_url: str
    code: str
    long_url: str

class URLRecord(BaseModel):
    code: str
    long_url: str
    created_by: str | None = None
    created_at: datetime
    expires_at: datetime | None = None
    click_count: int = 0

# ── ID Generation Strategy ──────────────────────────────────

# Problem: How to generate unique short codes across distributed servers?

# Solution 1: Base62 Encoding with Auto-Increment (Single DB)
# Simple but doesn't scale to multiple servers

# Solution 2: Snowflake-like Distributed ID Generator
import time
import threading

class DistributedIDGenerator:
    """
    Generates unique 64-bit IDs:
    - 41 bits: timestamp (ms) → ~69 years
    - 10 bits: worker ID → 1024 workers
    - 12 bits: sequence → 4096 IDs/ms per worker
    """
    EPOCH = 1609459200000  # 2021-01-01 in ms
    WORKER_ID_BITS = 10
    SEQUENCE_BITS = 12

    def __init__(self, worker_id: int):
        self.worker_id = worker_id & ((1 << self.WORKER_ID_BITS) - 1)
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()

    def _current_millis(self) -> int:
        return int(time.time() * 1000)

    def _wait_next_millis(self, last_ts: int) -> int:
        ts = self._current_millis()
        while ts <= last_ts:
            ts = self._current_millis()
        return ts

    def generate(self) -> int:
        with self.lock:
            ts = self._current_millis()

            if ts == self.last_timestamp:
                self.sequence = (self.sequence + 1) & ((1 << self.SEQUENCE_BITS) - 1)
                if self.sequence == 0:
                    ts = self._wait_next_millis(ts)
            else:
                self.sequence = 0

            self.last_timestamp = ts
            return (
                ((ts - self.EPOCH) << (self.WORKER_ID_BITS + self.SEQUENCE_BITS))
                | (self.worker_id << self.SEQUENCE_BITS)
                | self.sequence
            )

    def to_base62(self, num: int) -> str:
        chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if num == 0:
            return chars[0]
        result = []
        while num:
            result.append(chars[num % 62])
            num //= 62
        return "".join(reversed(result))

# Solution 3: Consistent Hashing for Code Assignment
import hashlib

class ConsistentHashRing:
    """Routes URLs to servers based on URL hash for cache-friendly distribution."""

    def __init__(self, servers: list[str], virtual_nodes: int = 150):
        self.ring: dict[int, str] = {}
        self.sorted_keys: list[int] = []
        self.virtual_nodes = virtual_nodes

        for server in servers:
            for i in range(virtual_nodes):
                key = self._hash(f"{server}:{i}")
                self.ring[key] = server
                self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def get_server(self, url: str) -> str:
        h = self._hash(url)
        for key in self.sorted_keys:
            if h <= key:
                return self.ring[key]
        return self.ring[self.sorted_keys[0]]

# ── API Implementation ──────────────────────────────────────

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse

app = FastAPI(title="Google-style URL Shortener")
id_generator = DistributedIDGenerator(worker_id=1)
hash_ring = ConsistentHashRing(["server-1", "server-2", "server-3"])

# In-memory store (use distributed DB in production)
url_store: dict[str, URLRecord] = {}
url_index: dict[str, str] = {}  # long_url -> code (dedup)

@app.post("/urls", response_model=ShortenResponse, status_code=201)
def create_short_url(request: ShortenRequest):
    # Check for duplicate
    if request.long_url in url_index:
        code = url_index[request.long_url]
        return ShortenResponse(
            short_url=f"https://sho.rt/{code}",
            code=code,
            long_url=request.long_url,
        )

    if request.custom_alias:
        if request.custom_alias in url_store:
            raise HTTPException(409, "Alias already in use")
        code = request.custom_alias
    else:
        # Generate distributed ID
        unique_id = id_generator.generate()
        code = id_generator.to_base62(unique_id)[:7]

    record = URLRecord(
        code=code,
        long_url=request.long_url,
        created_at=datetime.utcnow(),
        expires_at=request.expires_at,
    )
    url_store[code] = record
    url_index[request.long_url] = code

    # Route to server via consistent hashing
    assigned_server = hash_ring.get_server(request.long_url)

    return ShortenResponse(
        short_url=f"https://sho.rt/{code}",
        code=code,
        long_url=request.long_url,
    )


@app.get("/{code}")
def redirect_to_url(code: str, request: Request):
    if code not in url_store:
        raise HTTPException(404, "URL not found")

    record = url_store[code]
    if record.expires_at and record.expires_at < datetime.utcnow():
        raise HTTPException(410, "URL expired")

    record.click_count += 1

    # Log click asynchronously (don't block redirect)
    click_data = {
        "code": code,
        "timestamp": time.time(),
        "ip": request.client.host,
        "user_agent": request.headers.get("user-agent", ""),
    }

    return RedirectResponse(url=record.long_url, status_code=307)

# ── Scaling Discussion Points ────────────────────────────────
# 1. Database: Shard by code hash across PostgreSQL clusters
# 2. Cache: Redis cluster with consistent hashing for hot URLs
# 3. Analytics: Kafka → ClickHouse pipeline for click analytics
# 4. CDN: Edge caching for high-traffic URLs
# 5. Rate Limiting: Sliding window with Redis sorted sets
# 6. Consistency: Eventual consistency acceptable for analytics
```

**Key Discussion Points**:
- How would you handle 1 billion URLs? (Sharding strategy)
- What happens when a server goes down? (Replication, failover)
- How do you prevent abuse? (Rate limiting, CAPTCHA)
- How do you handle custom aliases? (Collision detection, reservation)
- Cache invalidation strategy? (TTL + event-driven invalidation)

---

### Question 2: Design a News Feed System (Meta-style)

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime
from collections import defaultdict
import heapq

app = FastAPI(title="News Feed System")


class Post(BaseModel):
    id: str
    author_id: str
    content: str
    media_urls: list[str] = []
    created_at: datetime
    score: float = 0.0  # For ranking

class FeedResponse(BaseModel):
    posts: list[Post]
    cursor: str | None
    has_more: bool


# ── Fan-out Strategy ─────────────────────────────────────────

class FanoutService:
    """
    Two strategies:
    1. Fan-out on Write (push): Pre-compute feeds when post is created
    2. Fan-out on Read (pull): Compute feed when user requests it

    Meta's approach: Hybrid
    - Regular users: Fan-out on write
    - Celebrity users (1M+ followers): Fan-out on read
    """

    def __init__(self):
        self.user_feeds: dict[str, list[str]] = defaultdict(list)  # user_id -> [post_ids]
        self.user_followers: dict[str, set[str]] = defaultdict(set)
        self.user_following: dict[str, set[str]] = defaultdict(set)
        self.posts_db: dict[str, Post] = {}
        self.CELEBRITY_THRESHOLD = 1_000_000

    def follow(self, follower_id: str, followee_id: str):
        self.user_followers[followee_id].add(follower_id)
        self.user_following[follower_id].add(followee_id)

    def create_post(self, post: Post):
        self.posts_db[post.id] = post
        followers = self.user_followers.get(post.author_id, set())

        is_celebrity = len(followers) > self.CELEBRITY_THRESHOLD

        if not is_celebrity:
            # Fan-out on write: push to all followers' feeds
            for follower_id in followers:
                self.user_feeds[follower_id].append(post.id)
                # Keep feed bounded
                if len(self.user_feeds[follower_id]) > 1000:
                    self.user_feeds[follower_id] = self.user_feeds[follower_id][-500:]
        # Celebrity posts will be pulled on read

    def get_feed(self, user_id: str, cursor: str | None = None, limit: int = 20) -> FeedResponse:
        # Get pre-computed feed (push posts)
        feed_ids = list(self.user_feeds.get(user_id, []))

        # Pull posts from followings (especially celebrities)
        following = self.user_following.get(user_id, set())
        for followee_id in following:
            followee_followers = len(self.user_followers.get(followee_id, set()))
            if followee_followers > self.CELEBRITY_THRESHOLD:
                # Pull recent posts from this celebrity
                celebrity_posts = [
                    pid for pid, p in self.posts_db.items()
                    if p.author_id == followee_id
                ][-50:]  # Only check last 50 posts
                feed_ids.extend(celebrity_posts)

        # Score and rank
        scored = []
        for pid in feed_ids:
            if pid in self.posts_db:
                post = self.posts_db[pid]
                score = self._calculate_score(post)
                scored.append((score, pid))

        scored.sort(reverse=True)

        # Pagination with cursor
        start = 0
        if cursor:
            for i, (_, pid) in enumerate(scored):
                if pid == cursor:
                    start = i + 1
                    break

        page = scored[start:start + limit]
        posts = [self.posts_db[pid] for _, pid in page]
        next_cursor = page[-1][1] if len(page) == limit else None

        return FeedResponse(posts=posts, cursor=next_cursor, has_more=next_cursor is not None)

    def _calculate_score(self, post: Post) -> float:
        """Ranking algorithm: recency + engagement + author relevance"""
        age_hours = (datetime.utcnow() - post.created_at).total_seconds() / 3600
        recency_score = 1.0 / (1.0 + age_hours)
        return recency_score + post.score


fanout = FanoutService()

@app.post("/posts")
def create_post(author_id: str, content: str):
    import uuid
    post = Post(
        id=str(uuid.uuid4())[:8],
        author_id=author_id,
        content=content,
        created_at=datetime.utcnow(),
    )
    fanout.create_post(post)
    return post

@app.get("/feed/{user_id}", response_model=FeedResponse)
def get_feed(user_id: str, cursor: str | None = None, limit: int = Query(20, le=100)):
    return fanout.get_feed(user_id, cursor=cursor, limit=limit)

@app.post("/follow")
def follow_user(follower_id: str, followee_id: str):
    fanout.follow(follower_id, followee_id)
    return {"status": "followed"}
```

---

### Question 3: Rate Limiter Design (Google-style)

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
from dataclasses import dataclass
from collections import defaultdict
import threading

app = FastAPI()


# ── Sliding Window Log (Exact, Memory-Heavy) ────────────────

class SlidingWindowLog:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.logs: dict[str, list[float]] = defaultdict(list)
        self.lock = threading.Lock()

    def is_allowed(self, key: str) -> tuple[bool, dict]:
        now = time.time()
        cutoff = now - self.window_seconds

        with self.lock:
            self.logs[key] = [t for t in self.logs[key] if t > cutoff]
            count = len(self.logs[key])
            remaining = max(0, self.max_requests - count)

            headers = {
                "X-RateLimit-Limit": str(self.max_requests),
                "X-RateLimit-Remaining": str(remaining),
            }

            if count >= self.max_requests:
                oldest = self.logs[key][0] if self.logs[key] else now
                retry_after = oldest + self.window_seconds - now
                headers["Retry-After"] = str(int(retry_after) + 1)
                return False, headers

            self.logs[key].append(now)
            headers["X-RateLimit-Remaining"] = str(remaining - 1)
            return True, headers


# ── Token Bucket (Efficient, Smooth) ────────────────────────

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets: dict[str, dict] = {}
        self.lock = threading.Lock()

    def _refill(self, bucket: dict):
        now = time.time()
        elapsed = now - bucket["last_refill"]
        bucket["tokens"] = min(
            self.capacity,
            bucket["tokens"] + elapsed * self.refill_rate,
        )
        bucket["last_refill"] = now

    def is_allowed(self, key: str) -> tuple[bool, dict]:
        with self.lock:
            if key not in self.buckets:
                self.buckets[key] = {"tokens": self.capacity, "last_refill": time.time()}

            bucket = self.buckets[key]
            self._refill(bucket)

            if bucket["tokens"] >= 1:
                bucket["tokens"] -= 1
                return True, {"X-RateLimit-Remaining": str(int(bucket["tokens"]))}
            else:
                wait_time = (1 - bucket["tokens"]) / self.refill_rate
                return False, {"Retry-After": str(int(wait_time) + 1)}


# ── Fixed Window Counter (Memory-Efficient, Burst-Prone) ────

class FixedWindowCounter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.windows: dict[str, dict] = {}

    def is_allowed(self, key: str) -> tuple[bool, dict]:
        now = time.time()
        window_key = int(now // self.window_seconds)

        if key not in self.windows or self.windows[key]["window"] != window_key:
            self.windows[key] = {"window": window_key, "count": 0}

        window = self.windows[key]
        count = window["count"]

        if count >= self.max_requests:
            return False, {"Retry-After": str(self.window_seconds)}

        window["count"] += 1
        remaining = self.max_requests - window["count"]
        return True, {"X-RateLimit-Remaining": str(remaining)}


# ── Combined Rate Limiter (Production-Ready) ────────────────

class MultiTierRateLimiter:
    """
    Layer 1: IP-based (protection against brute force)
    Layer 2: API Key-based (per-user limits)
    Layer 3: Endpoint-specific (different limits per endpoint)
    """

    def __init__(self):
        self.ip_limiter = TokenBucket(capacity=100, refill_rate=10)
        self.api_key_limiter = TokenBucket(capacity=1000, refill_rate=100)
        self.endpoint_limits: dict[str, TokenBucket] = {
            "/api/search": TokenBucket(capacity=10, refill_rate=1),
            "/api/auth": TokenBucket(capacity=5, refill_rate=0.1),
        }

    def check(self, request: Request) -> tuple[bool, dict]:
        client_ip = request.client.host
        api_key = request.headers.get("X-API-Key", "anonymous")
        path = request.url.path

        # Layer 1: IP check
        allowed, headers = self.ip_limiter.is_allowed(client_ip)
        if not allowed:
            return False, {**headers, "limit_type": "ip"}

        # Layer 2: API key check
        allowed, headers = self.api_key_limiter.is_allowed(api_key)
        if not allowed:
            return False, {**headers, "limit_type": "api_key"}

        # Layer 3: Endpoint check
        for pattern, limiter in self.endpoint_limits.items():
            if path.startswith(pattern):
                allowed, headers = limiter.is_allowed(f"{api_key}:{path}")
                if not allowed:
                    return False, {**headers, "limit_type": "endpoint"}

        return True, {"X-RateLimit-Status": "ok"}


rate_limiter = MultiTierRateLimiter()

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    allowed, headers = rate_limiter.check(request)
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded", "type": headers.get("limit_type")},
            headers=headers,
        )
    response = await call_next(request)
    response.headers.update(headers)
    return response
```

---

## Amazon Style (Behavioral + Architecture)

### Question 4: Design an Order Processing System

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from enum import Enum
from dataclasses import dataclass
import time
import uuid

app = FastAPI(title="Order Processing System")


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PAYMENT_PENDING = "payment_pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


@dataclass
class OrderStateMachine:
    """Amazon-style order state machine with clear transition rules."""

    VALID_TRANSITIONS = {
        OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
        OrderStatus.CONFIRMED: [OrderStatus.PAYMENT_PENDING, OrderStatus.CANCELLED],
        OrderStatus.PAYMENT_PENDING: [OrderStatus.PAID, OrderStatus.CANCELLED],
        OrderStatus.PAID: [OrderStatus.SHIPPED, OrderStatus.REFUNDED],
        OrderStatus.SHIPPED: [OrderStatus.DELIVERED, OrderStatus.REFUNDED],
        OrderStatus.DELIVERED: [OrderStatus.REFUNDED],
        OrderStatus.CANCELLED: [],
        OrderStatus.REFUNDED: [],
    }

    @classmethod
    def can_transition(cls, from_status: OrderStatus, to_status: OrderStatus) -> bool:
        return to_status in cls.VALID_TRANSITIONS.get(from_status, [])

    @classmethod
    def validate_transition(cls, from_status: OrderStatus, to_status: OrderStatus):
        if not cls.can_transition(from_status, to_status):
            raise HTTPException(
                400,
                f"Invalid transition: {from_status.value} → {to_status.value}. "
                f"Valid next states: {[s.value for s in cls.VALID_TRANSITIONS[from_status]]}"
            )


# ── Order Service ───────────────────────────────────────────

class OrderCreate(BaseModel):
    customer_id: str
    items: list[dict]
    shipping_address: dict
    payment_method: str

orders_db: dict[str, dict] = {}
order_events: list[dict] = []


class OrderService:
    @staticmethod
    def create_order(payload: OrderCreate) -> dict:
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        total = sum(item["price"] * item["quantity"] for item in payload.items)

        order = {
            "id": order_id,
            "customer_id": payload.customer_id,
            "items": payload.items,
            "total": total,
            "status": OrderStatus.PENDING,
            "shipping": payload.shipping_address,
            "payment_method": payload.payment_method,
            "created_at": time.time(),
            "updated_at": time.time(),
            "status_history": [{"status": "pending", "timestamp": time.time()}],
        }
        orders_db[order_id] = order

        OrderService._emit_event(order_id, "order_created", order)
        return order

    @staticmethod
    def update_status(order_id: str, new_status: OrderStatus, reason: str = ""):
        if order_id not in orders_db:
            raise HTTPException(404, "Order not found")

        order = orders_db[order_id]
        OrderStateMachine.validate_transition(order["status"], new_status)

        order["status"] = new_status
        order["updated_at"] = time.time()
        order["status_history"].append({
            "status": new_status.value,
            "timestamp": time.time(),
            "reason": reason,
        })

        OrderService._emit_event(order_id, f"order_{new_status.value}", order)

        # Trigger side effects
        if new_status == OrderStatus.PAID:
            OrderService._trigger_fulfillment(order_id)
        elif new_status == OrderStatus.SHIPPED:
            OrderService._send_shipping_notification(order_id)
        elif new_status == OrderStatus.CANCELLED:
            OrderService._release_inventory(order_id)

    @staticmethod
    def _emit_event(order_id: str, event_type: str, data: dict):
        order_events.append({
            "order_id": order_id,
            "event": event_type,
            "data": data,
            "timestamp": time.time(),
        })

    @staticmethod
    def _trigger_fulfillment(order_id: str):
        print(f"Triggering fulfillment for {order_id}")

    @staticmethod
    def _send_shipping_notification(order_id: str):
        print(f"Sending shipping notification for {order_id}")

    @staticmethod
    def _release_inventory(order_id: str):
        print(f"Releasing inventory for {order_id}")


@app.post("/orders", status_code=201)
def create_order(payload: OrderCreate):
    return OrderService.create_order(payload)

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: str, status: OrderStatus, reason: str = ""):
    OrderService.update_status(order_id, status, reason)
    return orders_db[order_id]

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(404)
    return orders_db[order_id]

@app.get("/orders/{order_id}/timeline")
def get_order_timeline(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(404)
    return {"timeline": orders_db[order_id]["status_history"]}
```

### Behavioral Answer Framework (Amazon STAR Method)

When asked about your experience, use this structure:

```
Situation: "In my previous role, we had an order processing system that..."
Task: "I was responsible for..."
Action: "I implemented a state machine pattern to..."
Result: "This reduced order processing errors by 40% and..."
```

---

## Netflix Style (Scaling + Reliability)

### Question 5: Design a Video Streaming API

```python
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from dataclasses import dataclass
import time

app = FastAPI(title="Video Streaming API")


@dataclass
class AdaptiveBitrate:
    """Netflix-style ABR (Adaptive Bitrate) streaming."""

    QUALITY_PROFILES = {
        "4K": {"bitrate": 20_000_000, "resolution": "3840x2160", "codec": "h265"},
        "1080p": {"bitrate": 8_000_000, "resolution": "1920x1080", "codec": "h264"},
        "720p": {"bitrate": 5_000_000, "resolution": "1280x720", "codec": "h264"},
        "480p": {"bitrate": 2_500_000, "resolution": "854x480", "codec": "h264"},
        "360p": {"bitrate": 1_000_000, "resolution": "640x360", "codec": "h264"},
    }

    @staticmethod
    def select_quality(bandwidth_bps: int) -> str:
        """Select optimal quality based on measured bandwidth."""
        for quality in ["4K", "1080p", "720p", "480p", "360p"]:
            profile = AdaptiveBitrate.QUALITY_PROFILES[quality]
            # Use 70% of bandwidth for safety margin
            if bandwidth_bps * 0.7 >= profile["bitrate"]:
                return quality
        return "360p"


class ManifestRequest(BaseModel):
    video_id: str
    client_bandwidth: int | None = None  # bps
    device_type: str = "web"  # web, mobile, tv

class ManifestResponse(BaseModel):
    video_id: str
    selected_quality: str
    segments: list[dict]
    cdn_urls: list[str]
    drm_license_url: str


videos_db = {
    "vid-001": {
        "id": "vid-001",
        "title": "Big Buck Bunny",
        "duration_seconds": 596,
        "qualities": ["4K", "1080p", "720p", "480p"],
        "segments": 120,  # Each segment ~5 seconds
        "cdn_distribution": ["cdn-us-east", "cdn-eu-west", "cdn-ap-south"],
    }
}

# CDN selection based on user location
CDN_MAP = {
    "US": "cdn-us-east",
    "EU": "cdn-eu-west",
    "ASIA": "cdn-ap-south",
}


@app.get("/manifest/{video_id}")
def get_streaming_manifest(
    video_id: str,
    bandwidth: int = Query(default=5_000_000),
    region: str = Query(default="US"),
):
    if video_id not in videos_db:
        raise HTTPException(404, "Video not found")

    video = videos_db[video_id]
    selected_quality = AdaptiveBitrate.select_quality(bandwidth)

    segments = []
    for i in range(video["segments"]):
        segments.append({
            "segment_id": i,
            "duration": 5.0,
            "url": f"/segments/{video_id}/{selected_quality}/{i}",
            "size_bytes": int(AdaptiveBitrate.QUALITY_PROFILES[selected_quality]["bitrate"] * 5 / 8),
        })

    cdn_url = CDN_MAP.get(region, "cdn-us-east")

    return ManifestResponse(
        video_id=video_id,
        selected_quality=selected_quality,
        segments=segments,
        cdn_urls=[f"https://{cdn_url}.netflix.com"],
        drm_license_url=f"/drm/license/{video_id}",
    )


@app.get("/video/{video_id}/stats")
def get_streaming_stats(video_id: str):
    """Netflix-style streaming analytics endpoint."""
    return {
        "video_id": video_id,
        "concurrent_streams": 1234,
        "avg_bandwidth": 8_500_000,
        "buffering_ratio": 0.02,
        "quality_distribution": {"4K": 15, "1080p": 45, "720p": 25, "480p": 10, "360p": 5},
    }
```

### Netflix Reliability Concepts to Discuss

```
1. Chaos Engineering: Inject failures to test resilience
2. Circuit Breakers: Prevent cascade failures
3. Bulkheads: Isolate failures to one service
4. Retry with Exponential Backoff: Handle transient failures
5. Fallback Mechanisms: Degrade gracefully
6. Load Shedding: Drop low-priority requests under load
7. Feature Flags: Gradual rollouts and A/B testing
```

---

## Startup Style (Full-Stack + Speed)

### Question 6: Build a Complete SaaS MVP in One Day

```python
"""
Startup-style: Ship fast, iterate fast.
Full-featured SaaS boilerplate with auth, billing, multi-tenancy.
"""

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from enum import Enum
import time
import uuid

app = FastAPI(title="SaaS MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Auth (Minimal but Functional) ───────────────────────────

class UserPlan(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class User(BaseModel):
    id: str
    email: str
    name: str
    plan: UserPlan = UserPlan.FREE
    team_id: str | None = None
    created_at: float

users_db: dict[str, dict] = {}
teams_db: dict[str, dict] = {}


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/auth/register")
def register(payload: RegisterRequest):
    for u in users_db.values():
        if u["email"] == payload.email:
            raise HTTPException(400, "Email already registered")

    user_id = str(uuid.uuid4())[:8]
    users_db[user_id] = {
        "id": user_id,
        "email": payload.email,
        "name": payload.name,
        "password_hash": f"hashed_{payload.password}",  # Use bcrypt in production
        "plan": UserPlan.FREE,
        "created_at": time.time(),
    }

    # Create default team
    team_id = str(uuid.uuid4())[:8]
    teams_db[team_id] = {
        "id": team_id,
        "name": f"{payload.name}'s Team",
        "owner_id": user_id,
        "members": [user_id],
        "plan": UserPlan.FREE,
    }
    users_db[user_id]["team_id"] = team_id

    return {"user_id": user_id, "team_id": team_id, "token": f"tok_{user_id}"}

# ── Feature Gating ──────────────────────────────────────────

PLAN_FEATURES = {
    UserPlan.FREE: {"max_projects": 3, "max_members": 1, "api_calls": 1000},
    UserPlan.PRO: {"max_projects": 50, "max_members": 10, "api_calls": 100_000},
    UserPlan.ENTERPRISE: {"max_projects": -1, "max_members": -1, "api_calls": -1},
}

def require_plan(min_plan: UserPlan):
    def dependency(user = Depends(get_current_user)):
        plan_hierarchy = [UserPlan.FREE, UserPlan.PRO, UserPlan.ENTERPRISE]
        if plan_hierarchy.index(user["plan"]) < plan_hierarchy.index(min_plan):
            raise HTTPException(403, f"Requires {min_plan.value} plan or higher")
        return user
    return dependency

@app.get("/features")
def get_features(user = Depends(get_current_user)):
    return PLAN_FEATURES[user["plan"]]

@app.get("/pro-feature")
def pro_feature(user = Depends(require_plan(UserPlan.PRO))):
    return {"feature": "This is a pro-only feature"}

# ── Team Management ─────────────────────────────────────────

@app.post("/teams/{team_id}/invite")
def invite_member(team_id: str, email: str, user = Depends(get_current_user)):
    if team_id not in teams_db:
        raise HTTPException(404)
    team = teams_db[team_id]
    if team["owner_id"] != user["id"]:
        raise HTTPException(403, "Only team owner can invite")

    plan = team["plan"]
    limits = PLAN_FEATURES[plan]
    if limits["max_members"] != -1 and len(team["members"]) >= limits["max_members"]:
        raise HTTPException(400, f"Team member limit reached for {plan.value} plan")

    return {"invite_sent": True, "email": email}

@app.get("/teams/{team_id}")
def get_team(team_id: str, user = Depends(get_current_user)):
    if team_id not in teams_db:
        raise HTTPException(404)
    team = teams_db[team_id]
    if user["id"] not in team["members"]:
        raise HTTPException(403)
    return team
```

---

## Tesla / NVIDIA Style (Performance + Low-Level)

### Question 7: Optimize a Slow API Endpoint

```python
"""
Tesla/NVIDIA style: They care about raw performance, low-level optimization,
hardware awareness, and efficient algorithms.
"""

from fastapi import FastAPI, Query
from dataclasses import dataclass
import asyncio
import time
from typing import Iterator

app = FastAPI(title="High-Performance API")


# ── Problem: Slow Data Processing Endpoint ──────────────────

# BAD: Naive implementation
@app.get("/analytics/bad")
async def get_analytics_bad():
    # O(n) database scan
    all_events = await fetch_all_events()  # 1M rows
    # O(n) processing in Python
    results = {}
    for event in all_events:
        key = event["category"]
        if key not in results:
            results[key] = {"count": 0, "total_value": 0}
        results[key]["count"] += 1
        results[key]["total_value"] += event["value"]
    return results


# GOOD: Optimized implementation
@app.get("/analytics/good")
async def get_analytics_good():
    # O(1) aggregation at database level
    # Use materialized views / pre-aggregated tables
    results = await db.fetch("""
        SELECT category, COUNT(*) as count, SUM(value) as total_value
        FROM events
        GROUP BY category
    """)
    return {row["category"]: dict(row) for row in results}


# ── Streaming Response for Large Datasets ───────────────────

from fastapi.responses import StreamingResponse
import orjson

@app.get("/export/large")
async def export_large_dataset():
    """Stream JSONL for memory efficiency with large datasets."""

    async def generate():
        async for batch in stream_events(batch_size=1000):
            for event in batch:
                yield orjson.dumps(event) + b"\n"

    return StreamingResponse(generate(), media_type="application/jsonl")


# ── Efficient Caching with LRU ─────────────────────────────

from functools import lru_cache
import hashlib

# In-memory LRU cache (fastest possible)
@lru_cache(maxsize=10000)
def compute_expensive_query(query_hash: str, params: str) -> bytes:
    """Cache results by query hash for repeated queries."""
    # Actual computation here
    return orjson.dumps({"result": "computed"})


@app.get("/query")
async def execute_query(q: str, params: str = "{}"):
    query_hash = hashlib.md5(f"{q}:{params}".encode()).hexdigest()
    return StreamingResponse(
        iter([compute_expensive_query(query_hash, params)]),
        media_type="application/json",
    )


# ── Batch Processing with AsyncIO ──────────────────────────

async def process_batch(batch: list[dict]) -> list[dict]:
    """Process a batch of items concurrently."""
    semaphore = asyncio.Semaphore(100)  # Limit concurrent operations

    async def process_item(item: dict):
        async with semaphore:
            return await heavy_computation(item)

    tasks = [process_item(item) for item in batch]
    return await asyncio.gather(*tasks)


@app.post("/process/batch")
async def batch_process(items: list[dict]):
    """Process up to 10K items efficiently."""
    CHUNK_SIZE = 1000
    results = []

    # Process in chunks to avoid memory spikes
    for i in range(0, len(items), CHUNK_SIZE):
        chunk = items[i:i + CHUNK_SIZE]
        chunk_results = await process_batch(chunk)
        results.extend(chunk_results)

    return {"processed": len(results)}


# ── Memory-Efficient Pagination ─────────────────────────────

@app.get("/huge-dataset")
async def huge_dataset(
    cursor: str | None = None,
    limit: int = Query(100, le=1000),
):
    """
    Cursor-based pagination for billion-row datasets.
    No OFFSET scanning - O(log n) with proper indexing.
    """
    if cursor:
        # Use cursor for efficient seeking
        query = """
            SELECT * FROM events
            WHERE id > $1
            ORDER BY id
            LIMIT $2
        """
        rows = await db.fetch(query, cursor, limit + 1)
    else:
        query = "SELECT * FROM events ORDER BY id LIMIT $1"
        rows = await db.fetch(query, limit + 1)

    has_more = len(rows) > limit
    rows = rows[:limit]

    return {
        "data": rows,
        "next_cursor": rows[-1]["id"] if has_more else None,
        "has_more": has_more,
    }


# ── Performance Monitoring ──────────────────────────────────

@app.middleware("http")
async def performance_middleware(request: Request, call_next):
    start = time.perf_counter()  # Higher precision than time.time()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000

    response.headers["X-Response-Time"] = f"{duration_ms:.3f}ms"

    # Alert on slow requests
    if duration_ms > 1000:
        print(f"SLOW REQUEST: {request.method} {request.url.path} took {duration_ms:.1f}ms")

    return response
```

### Performance Optimization Checklist (Tesla/NVIDIA Style)

```
1. Database:
   - Index all query columns
   - Use EXPLAIN ANALYZE to find slow queries
   - Connection pooling (pgbouncer)
   - Read replicas for read-heavy workloads
   - Materialized views for complex aggregations

2. Application:
   - Async I/O everywhere
   - Streaming responses for large payloads
   - Connection pooling (httpx, asyncpg)
   - LRU caching for hot data
   - Batch operations instead of loops

3. Infrastructure:
   - Multiple uvicorn workers (CPU cores * 2 + 1)
   - GZip compression
   - HTTP/2 multiplexing
   - CDN for static assets
   - Keep-alive connections

4. Monitoring:
   - p95/p99 latency tracking
   - Memory profiling (memory_profiler)
   - CPU profiling (cProfile, py-spy)
   - Distributed tracing (OpenTelemetry)

5. Algorithmic:
   - O(1) or O(log n) lookups with proper indexing
   - Avoid N+1 queries (use JOINs or eager loading)
   - Streaming for datasets larger than memory
   - Lazy evaluation where possible
```

---

## General Multi-Company Questions

### Question 8: Explain the CAP Theorem with FastAPI Examples

```python
"""
CAP Theorem: A distributed system can only guarantee 2 of 3:
- Consistency: Every read receives the most recent write
- Availability: Every request receives a response
- Partition Tolerance: System continues despite network failures

In practice, you always need Partition Tolerance, so the choice is CP vs AP.
"""

# CP System (Consistency + Partition Tolerance)
# Example: PostgreSQL with synchronous replication
# Use when: Financial transactions, inventory management

@app.post("/transfer")
async def transfer_funds(from_account: str, to_account: str, amount: float):
    # Strong consistency required - money can't be duplicated or lost
    async with db.transaction(isolation="SERIALIZABLE"):
        from_acc = await db.fetch_one("SELECT * FROM accounts WHERE id = $1 FOR UPDATE", from_account)
        if from_acc["balance"] < amount:
            raise HTTPException(400, "Insufficient funds")

        await db.execute("UPDATE accounts SET balance = balance - $1 WHERE id = $2", amount, from_account)
        await db.execute("UPDATE accounts SET balance = balance + $1 WHERE id = $2", amount, to_account)

    return {"status": "transferred"}

# AP System (Availability + Partition Tolerance)
# Example: Redis cluster, Cassandra
# Use when: Social media feeds, analytics, caching

@app.get("/feed")
async def get_feed(user_id: str):
    # Eventual consistency is acceptable for feeds
    # Even if slightly stale, show something rather than error
    try:
        # Try primary data source
        feed = await redis.get(f"feed:{user_id}")
        if feed:
            return {"feed": orjson.loads(feed)}
    except RedisConnectionError:
        pass

    # Fallback to cached version (might be stale)
    cached_feed = await get_cached_feed(user_id)
    return {"feed": cached_feed, "stale": True}
```

### Question 9: Design a Circuit Breaker Pattern

```python
from fastapi import FastAPI
from enum import Enum
from dataclasses import dataclass
import time

app = FastAPI()

class CircuitState(str, Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open" # Testing recovery

@dataclass
class CircuitBreaker:
    name: str
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    success_threshold: int = 3
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: float = 0
    last_state_change: float = 0

    def record_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
                self.last_state_change = time.time()

    def record_failure(self):
        self.failure_count += 1
        self.success_count = 0
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.last_state_change = time.time()

    def should_allow_request(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.last_state_change = time.time()
                return True
            return False
        return True  # HALF_OPEN allows requests through

breakers: dict[str, CircuitBreaker] = {}

def get_breaker(service: str) -> CircuitBreaker:
    if service not in breakers:
        breakers[service] = CircuitBreaker(name=service)
    return breakers[service]

@app.get("/call/{service}")
async def call_external_service(service: str):
    breaker = get_breaker(service)
    if not breaker.allow_request():
        return {"status": "circuit_open", "service": service, "fallback": True}

    try:
        # Simulate external call
        result = await make_external_call(service)
        breaker.record_success()
        return {"status": "success", "data": result}
    except Exception as e:
        breaker.record_failure()
        return {"status": "failure", "error": str(e)}
```

### Question 10: Explain Eventual Consistency with a Real Example

```python
"""
Eventual Consistency: If no new updates, all replicas will eventually
converge to the same value. This is the foundation of many distributed systems.
"""

from fastapi import FastAPI, BackgroundTasks
import asyncio
from collections import defaultdict

app = FastAPI()

class EventuallyConsistentStore:
    """
    Simulates eventual consistency with multiple replicas.
    Writes go to primary, async replication to secondaries.
    """

    def __init__(self, num_replicas: int = 3):
        self.primary: dict[str, dict] = {}
        self.replicas: list[dict[str, dict]] = [{} for _ in range(num_replicas)]
        self.replication_lag: list[float] = [0.1, 0.3, 0.5]  # Simulated lag

    async def write(self, key: str, value: dict):
        # Write to primary (strong consistency for writes)
        self.primary[key] = value

        # Async replication to replicas
        for i, replica in enumerate(self.replicas):
            asyncio.create_task(self._replicate(i, key, value))

    async def _replicate(self, replica_idx: int, key: str, value: dict):
        await asyncio.sleep(self.replication_lag[replica_idx])
        self.replicas[replica_idx][key] = value

    def read_from_primary(self, key: str) -> dict | None:
        return self.primary.get(key)

    def read_from_replica(self, key: str, replica_idx: int = 0) -> dict | None:
        # May read stale data!
        return self.replicas[replica_idx].get(key)

store = EventuallyConsistentStore()

@app.post("/write")
async def write_data(key: str, value: dict):
    await store.write(key, value)
    return {"status": "written_to_primary"}

@app.get("/read/primary")
def read_primary(key: str):
    return store.read_from_primary(key)

@app.get("/read/replica/{replica_idx}")
def read_replica(key: str, replica_idx: int = 0):
    data = store.read_from_replica(key, replica_idx)
    return {"data": data, "potentially_stale": True}
```

---

## Quick Reference: Company Focus Areas

| Company | Focus | Key Topics |
|---------|-------|------------|
| Google | System design, scalability | Distributed systems, algorithms, data structures |
| Meta | Product engineering, scale | Real-time systems, social graphs, news feed |
| Amazon | Leadership principles, architecture | Microservices, reliability, customer obsession |
| Netflix | Reliability, streaming | Chaos engineering, CDN, adaptive streaming |
| Tesla | Performance, real-time | Low-latency, hardware awareness, optimization |
| NVIDIA | Performance, compute | GPU awareness, parallel processing, CUDA |
| Startups | Speed, full-stack | Ship fast, MVP, wear many hats |
