# Redis Integration with FastAPI

## Table of Contents

1. [Redis with FastAPI](#redis-with-fastapi)
2. [redis-py vs aioredis](#redis-py-vs-aioredis)
3. [Connection Setup](#connection-setup)
4. [Caching Patterns](#caching-patterns)
5. [Session Storage](#session-storage)
6. [Rate Limiting with Redis](#rate-limiting-with-redis)
7. [Pub/Sub](#pubsub)
8. [Redis Streams](#redis-streams)
9. [Connection Pooling](#connection-pooling)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## Redis with FastAPI

Redis is an in-memory data store used for caching, session storage, rate limiting, pub/sub messaging, and real-time features. It's one of the most common dependencies in FastAPI applications.

### Use Cases

| Use Case | Data Structure | Example |
|----------|---------------|---------|
| Caching | Strings | `SET user:1 "{...}" EX 300` |
| Session storage | Hashes | `HSET session:abc123 user_id 1` |
| Rate limiting | Sorted Sets | `ZADD rate:ip timestamp` |
| Pub/Sub | Channels | `PUBLISH channel message` |
| Queue/Jobs | Lists | `LPUSH queue task_data` |
| Real-time counters | Strings | `INCR page:views:/home` |
| Leaderboards | Sorted Sets | `ZADD leaderboard score member` |

---

## redis-py vs aioredis

### History

- `aioredis` was the original async Redis library for Python
- `redis-py` added native async support in v4.2+
- `aioredis` is now deprecated and redirects to `redis-py`

### Current Recommendation: `redis-py`

```bash
pip install redis[hiredis]
# hiredis is an optional C parser for better performance
```

### Using redis-py Async

```python
import redis.asyncio as redis

# Create async client
r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True,  # Return strings instead of bytes
)

# Or use connection pool
pool = redis.ConnectionPool.from_url(
    "redis://localhost:6379/0",
    max_connections=20,
    decode_responses=True,
)
r = redis.Redis(connection_pool=pool)
```

### Using redis-py Sync (in Background Tasks)

```python
import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True,
)

# Use in background tasks or sync contexts
def background_job():
    r.set("key", "value")
```

---

## Connection Setup

### With FastAPI Dependency

```python
import redis.asyncio as redis
from fastapi import FastAPI, Depends

REDIS_URL = "redis://localhost:6379/0"

async def get_redis():
    r = redis.Redis.from_url(
        REDIS_URL,
        decode_responses=True,
    )
    try:
        yield r
    finally:
        await r.aclose()

app = FastAPI()

@app.get("/cache/{key}")
async def get_cached(key: str, r: redis.Redis = Depends(get_redis)):
    value = await r.get(key)
    return {"key": key, "value": value}
```

### With Connection Pool

```python
import redis.asyncio as redis

# Global connection pool
pool = redis.ConnectionPool.from_url(
    "redis://localhost:6379/0",
    max_connections=20,
    retry_on_timeout=True,
    socket_connect_timeout=5,
    socket_timeout=5,
)

async def get_redis():
    r = redis.Redis(connection_pool=pool)
    try:
        yield r
    finally:
        # Don't close — pool manages connections
        pass

@app.on_event("startup")
async def startup():
    await pool.connect()

@app.on_event("shutdown")
async def shutdown():
    await pool.disconnect()
```

### With Sentinel (High Availability)

```python
from redis.asyncio import Sentinel

sentinel = Sentinel(
    [("sentinel-1", 26379), ("sentinel-2", 26379)],
    socket_timeout=0.5,
)

# Get master for writes
master = sentinel.master_for("mymaster", socket_timeout=0.5)

# Get slave for reads
slave = sentinel.slave_for("mymaster", socket_timeout=0.5)
```

---

## Caching Patterns

### Simple Cache

```python
import json
from typing import Any

async def cache_get_or_set(
    r: redis.Redis,
    key: str,
    factory,
    ttl: int = 300,
) -> Any:
    """Get from cache or compute and cache."""
    cached = await r.get(key)
    if cached:
        return json.loads(cached)

    value = await factory() if callable(factory) else factory
    await r.setex(key, ttl, json.dumps(value))
    return value

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    r: redis.Redis = Depends(get_redis),
    db: Session = Depends(get_db),
):
    user = await cache_get_or_set(
        r,
        f"user:{user_id}",
        lambda: get_user_from_db(db, user_id),
        ttl=300,
    )
    return user
```

### Cache Aside Pattern

```python
async def get_user_cached(user_id: int, r: redis.Redis, db: Session):
    # 1. Check cache
    cached = await r.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    # 2. Query database
    user = db.query(User).get(user_id)
    if not user:
        return None

    # 3. Store in cache
    user_data = {"id": user.id, "name": user.name, "email": user.email}
    await r.setex(f"user:{user_id}", 300, json.dumps(user_data))

    return user_data

async def invalidate_user_cache(user_id: int, r: redis.Redis):
    await r.delete(f"user:{user_id}")
```

### Cache Invalidation

```python
async def update_user(
    user_id: int,
    data: UserUpdate,
    r: redis.Redis,
    db: Session,
):
    # Update database
    user = db.query(User).get(user_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()

    # Invalidate cache
    await r.delete(f"user:{user_id}")

    # Or use cache-aside with TTL
    # Cache expires automatically — no explicit invalidation needed
```

### Cache Warming

```python
@app.on_event("startup")
async def warm_cache(r: redis.Redis = Depends(get_redis)):
    """Pre-populate cache on startup."""
    db = SessionLocal()
    try:
        # Cache top users
        top_users = db.query(User).order_by(User.score.desc()).limit(100).all()
        for user in top_users:
            await r.setex(
                f"user:{user.id}",
                600,
                json.dumps({"id": user.id, "name": user.name}),
            )
    finally:
        db.close()
```

---

## Session Storage

### Redis-Backed Sessions

```python
import json
import uuid
from datetime import datetime, timedelta

class RedisSession:
    def __init__(self, redis: redis.Redis, ttl: int = 3600):
        self.redis = redis
        self.ttl = ttl

    async def create(self, user_id: int) -> str:
        session_id = str(uuid.uuid4())
        session_data = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(seconds=self.ttl)).isoformat(),
        }
        await self.redis.setex(
            f"session:{session_id}",
            self.ttl,
            json.dumps(session_data),
        )
        return session_id

    async def get(self, session_id: str) -> dict | None:
        data = await self.redis.get(f"session:{session_id}")
        if data:
            return json.loads(data)
        return None

    async def delete(self, session_id: str):
        await self.redis.delete(f"session:{session_id}")

    async def refresh(self, session_id: str):
        await self.redis.expire(f"session:{session_id}", self.ttl)

# Dependency
async def get_session_store(r: redis.Redis = Depends(get_redis)):
    return RedisSession(r)

@app.post("/login")
async def login(
    credentials: LoginRequest,
    session_store: RedisSession = Depends(get_session_store),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401)

    session_id = await session_store.create(user.id)
    return {"session_id": session_id}

@app.get("/me")
async def get_current_user(
    session_id: str = Cookie(),
    session_store: RedisSession = Depends(get_session_store),
):
    session = await session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=401)
    return {"user_id": session["user_id"]}
```

---

## Rate Limiting with Redis

### Fixed Window Rate Limiter

```python
from datetime import datetime

class FixedWindowRateLimiter:
    def __init__(self, redis: redis.Redis, max_requests: int, window: int):
        self.redis = redis
        self.max_requests = max_requests
        self.window = window

    async def is_allowed(self, key: str) -> bool:
        now = datetime.now().timestamp()
        window_key = f"rate:{key}:{int(now // self.window)}"

        current = await self.redis.incr(window_key)
        if current == 1:
            await self.redis.expire(window_key, self.window)

        return current <= self.max_requests

async def rate_limit(
    request: Request,
    r: redis.Redis = Depends(get_redis),
):
    limiter = FixedWindowRateLimiter(r, max_requests=100, window=60)
    client_ip = request.client.host

    if not await limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": "60"},
        )

@app.get("/api/data/", dependencies=[Depends(rate_limit)])
async def get_data():
    return {"data": "value"}
```

### Sliding Window Rate Limiter

```python
class SlidingWindowRateLimiter:
    def __init__(self, redis: redis.Redis, max_requests: int, window: int):
        self.redis = redis
        self.max_requests = max_requests
        self.window = window

    async def is_allowed(self, key: str) -> bool:
        now = datetime.now().timestamp()
        window_start = now - self.window

        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, self.window)

        results = await pipe.execute()
        request_count = results[2]

        return request_count <= self.max_requests
```

---

## Pub/Sub

### Basic Pub/Sub

```python
import asyncio
import json

# Publisher
async def publish_event(r: redis.Redis, channel: str, data: dict):
    await r.publish(channel, json.dumps(data))

# Subscriber
async def subscribe_events(r: redis.Redis, channel: str):
    pubsub = r.pubsub()
    await pubsub.subscribe(channel)

    async for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            yield data

# In FastAPI
@app.post("/events/")
async def create_event(
    event: EventCreate,
    r: redis.Redis = Depends(get_redis),
):
    await publish_event(r, "events", event.model_dump())
    return {"status": "published"}

# Background subscriber
async def event_handler():
    r = redis.Redis()
    async for event in subscribe_events(r, "events"):
        print(f"Processing event: {event}")
        await process_event(event)
```

### Pattern Subscription

```python
async def subscribe_patterns(r: redis.Redis):
    pubsub = r.pubsub()
    await psubscribe("user:*:notifications")

    async for message in pubsub.listen():
        if message["type"] == "pmessage":
            channel = message["channel"]
            data = json.loads(message["data"])
            user_id = channel.split(":")[1]
            await send_notification(user_id, data)
```

---

## Redis Streams

### Producing Messages

```python
async def add_to_stream(r: redis.Redis, stream: str, data: dict):
    message_id = await r.xadd(
        stream,
        {k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
         for k, v in data.items()},
    )
    return message_id

@app.post("/orders/")
async def create_order(
    order: OrderCreate,
    r: redis.Redis = Depends(get_redis),
):
    # Save to database
    db_order = save_order(order)

    # Publish to stream
    await add_to_stream(r, "orders", {
        "order_id": db_order.id,
        "user_id": db_order.user_id,
        "total": db_order.total,
    })

    return db_order
```

### Consuming Messages

```python
async def consume_stream(r: redis.Redis, stream: str, group: str, consumer: str):
    try:
        await r.xgroup_create(stream, group, id="0", mkstream=True)
    except redis.ResponseError:
        pass  # Group already exists

    while True:
        messages = await r.xreadgroup(
            groupname=group,
            consumername=consumer,
            streams={stream: ">"},
            count=10,
            block=5000,
        )

        for stream_name, stream_messages in messages:
            for msg_id, data in stream_messages:
                await process_message(data)
                await r.xack(stream, group, msg_id)
```

---

## Connection Pooling

### Pool Configuration

```python
import redis.asyncio as redis

pool = redis.ConnectionPool.from_url(
    "redis://localhost:6379/0",
    max_connections=20,          # Maximum concurrent connections
    retry_on_timeout=True,      # Retry on timeout
    socket_connect_timeout=5,   # Connection timeout
    socket_timeout=5,           # Read/write timeout
    socket_keepalive=True,      # Keep connections alive
    socket_keepalive_options={
        1: 30,  # TCP_KEEPIDLE
        2: 10,  # TCP_KEEPINTVL
        3: 5,   # TCP_KEEPCNT
    },
    health_check_interval=30,   # Check connection health
    decoder_class=json.loads,   # Custom decoder
)

r = redis.Redis(connection_pool=pool)
```

### Monitoring Pool Health

```python
async def get_pool_stats(r: redis.Redis):
    pool = r.connection_pool
    return {
        "created": pool._created_connections,
        "available": pool._available_connections,
        "in_use": pool._in_use_connections,
    }
```

---

## Best Practices

### 1. Always Set TTL for Cache Keys

```python
# BAD: No expiration — memory leak
await r.set("user:1", data)

# GOOD: Set TTL
await r.setex("user:1", 300, data)
```

### 2. Use Connection Pooling

```python
# BAD: New connection per request
async def get_redis():
    r = redis.Redis(host="localhost", port=6379)
    yield r
    await r.aclose()

# GOOD: Connection pool
pool = redis.ConnectionPool.from_url("redis://localhost:6379")
async def get_redis():
    r = redis.Redis(connection_pool=pool)
    yield r
```

### 3. Handle Redis Failures Gracefully

```python
async def get_cached_data(r: redis.Redis, key: str):
    try:
        return await r.get(key)
    except redis.ConnectionError:
        # Redis is down — fall back to database
        logger.warning("Redis unavailable, falling back to DB")
        return None
```

### 4. Use Pipelines for Batch Operations

```python
# BAD: Individual operations
for user in users:
    await r.set(f"user:{user.id}", json.dumps(user))

# GOOD: Pipeline
pipe = r.pipeline()
for user in users:
    pipe.set(f"user:{user.id}", json.dumps(user))
await pipe.execute()
```

### 5. Serialize Efficiently

```python
import json
import msgpack

# JSON — human readable, larger
data = json.dumps(user_dict)

# MessagePack — binary, smaller, faster
data = msgpack.packb(user_dict)
```

---

## Interview Questions

### Q1: When would you use Redis in a FastAPI application?
**Answer:** Caching frequently accessed data, session storage, rate limiting, pub/sub messaging, job queues, real-time counters, leaderboards, and as a message broker between services.

### Q2: What is the difference between `redis-py` and `aioredis`?
**Answer:** `aioredis` was the original async library but is now deprecated. `redis-py` v4.2+ has native async support via `redis.asyncio`. Use `redis-py` for all new projects.

### Q3: How do you implement rate limiting with Redis?
**Answer:** Use sorted sets (sliding window) or simple counters (fixed window). Store request timestamps in a key with TTL. Check count against threshold before processing.

### Q4: What is the cache-aside pattern?
**Answer:** Application checks cache first. On miss, query database, store result in cache with TTL. On hit, return cached data. Simplest and most common caching pattern.

### Q5: How do you handle Redis connection failures?
**Answer:** Wrap Redis operations in try/except. Fall back to database queries. Use circuit breaker pattern for repeated failures. Log warnings for monitoring.

### Q6: What are Redis Streams used for?
**Answer:** Append-only log for event streaming. Support consumer groups for distributed processing. Use for job queues, event sourcing, and real-time data pipelines.

### Q7: How does Redis Pub/Sub differ from Streams?
**Answer:** Pub/Sub is fire-and-forget — messages are lost if no subscriber is listening. Streams persist messages and support consumer groups, acknowledgment, and replay.

### Q8: When would you use Redis over a database for caching?
**Answer:** When you need sub-millisecond reads, high throughput (100K+ ops/sec), TTL-based expiration, or atomic operations. Redis is in-memory — much faster than disk-based databases.

### Q9: How do you serialize data for Redis?
**Answer:** JSON for human readability and cross-language compatibility. MessagePack for smaller size and faster serialization. Pickle for Python-only (security risk — avoid).

### Q10: What is Redis connection pooling?
**Answer:** Maintaining a pool of reusable connections to avoid the overhead of creating/destroying connections per request. Configure `max_connections` based on expected concurrency.

### Q11: How do you implement distributed locking with Redis?
**Answer:** Use `SET NX EX` (SET if Not eXists with expiration). Or use Redlock algorithm for multi-node reliability. Libraries like `aioredlock` simplify this.

### Q12: What are the memory optimization strategies for Redis?
**Answer:** Use compact data structures, set TTLs, use `maxmemory` with eviction policies (LRU, LFU), compress values, and monitor with `INFO memory`.

### Q13: How do you handle cache stampede?
**Answer:** Use locking (only one process rebuilds cache), stale-while-revalidate (serve stale data while refreshing), or probabilistic early expiration.

---

## Summary

Redis is a versatile tool in the FastAPI ecosystem. Use it for caching with TTL, session storage, rate limiting, pub/sub messaging, and job queues. Always use connection pooling, handle failures gracefully, and set TTLs to prevent memory leaks.
