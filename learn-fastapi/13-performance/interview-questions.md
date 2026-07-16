# Performance Interview Questions

## Table of Contents

1. [Basic Level (1-10)](#1-basic)
2. [Intermediate Level (11-20)](#2-intermediate)
3. [Advanced Level (21-30)](#3-advanced)
4. [Expert Level (31-40)](#4-expert)
5. [Practical Scenarios](#5-scenarios)
6. [Code Review Questions](#6-code-review)

---

## 1. Basic Level (1-10) <a name="1-basic"></a>

### Q1: What is caching and why is it important?

**Answer:** Caching stores frequently accessed data in a fast-access layer (memory, Redis) to reduce database load and improve response times.

```python
import redis
import json

cache = redis.Redis()

def get_user(user_id: int):
    # Check cache first
    cached = cache.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    # Cache miss - fetch from DB
    user = db.query(User).get(user_id)
    cache.setex(f"user:{user_id}", 300, json.dumps(user.dict()))
    return user
```

### Q2: What is connection pooling?

**Answer:** Connection pooling reuses database connections instead of creating new ones for each request, reducing overhead.

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://user:pass@localhost/db",
    pool_size=20,      # Max persistent connections
    max_overflow=10,   # Extra connections beyond pool_size
)
```

### Q3: What is the difference between sync and async in FastAPI?

**Answer:** Sync routes run in a thread pool (blocking). Async routes run on the event loop (non-blocking). Use async for I/O-bound operations.

```python
# Sync - runs in thread pool
@app.get("/sync")
def sync_endpoint():
    return {"message": "Hello"}

# Async - runs on event loop
@app.get("/async")
async def async_endpoint():
    return {"message": "Hello"}
```

### Q4: What is pagination and when to use it?

**Answer:** Pagination limits the amount of data returned per request. Always paginate lists to avoid returning unbounded data.

```python
@app.get("/items/")
async def list_items(skip: int = 0, limit: int = 20):
    items = db.query(Item).offset(skip).limit(limit).all()
    return {"items": items, "total": db.query(Item).count()}
```

### Q5: What is the N+1 query problem?

**Answer:** N+1 queries occur when you fetch N items, then make N additional queries for related data. Use eager loading to fix.

```python
# BAD: N+1 queries
items = db.query(Item).all()
for item in items:
    owner = db.query(User).get(item.owner_id)  # N queries!

# GOOD: Single query with join
items = db.query(Item).options(joinedload(Item.owner)).all()
```

### Q6: What is Redis and when to use it?

**Answer:** Redis is an in-memory data store used for caching, sessions, queues, and pub/sub. Use it for fast read/write operations.

### Q7: What is rate limiting?

**Answer:** Rate limiting restricts how many requests a client can make in a time period, preventing abuse and ensuring fair resource usage.

### Q8: What is lazy loading vs eager loading?

**Answer:** Lazy loading loads related data on demand. Eager loading loads all related data upfront. Eager loading prevents N+1 queries.

### Q9: What is a CDN?

**Answer:** A Content Delivery Network caches static content at edge locations worldwide, reducing latency for users.

### Q10: What is the difference between horizontal and vertical scaling?

**Answer:** Vertical scaling adds more resources to one server. Horizontal scaling adds more servers. FastAPI supports both with stateless design.

---

## 2. Intermediate Level (11-20) <a name="2-intermediate"></a>

### Q11: How do you implement caching in FastAPI?

**Answer:**
```python
from functools import lru_cache
import redis

# In-memory cache
@lru_cache(maxsize=128)
def expensive_computation(x: int) -> int:
    return x * x

# Redis cache
redis_client = redis.Redis()

def get_or_set(key: str, factory, ttl: int = 300):
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    value = factory()
    redis_client.setex(key, ttl, json.dumps(value))
    return value
```

### Q12: How do you optimize database queries?

**Answer:**
```python
# 1. Use indexes
Index("ix_users_email", User.email)

# 2. Use select_related/joinedload
items = db.query(Item).options(joinedload(Item.owner)).all()

# 3. Use only needed columns
users = db.query(User.id, User.name).all()

# 4. Use pagination
items = db.query(Item).offset(0).limit(20).all()

# 5. Use count efficiently
total = db.query(func.count(Item.id)).scalar()
```

### Q13: What is cache invalidation?

**Answer:** Cache invalidation removes or updates cached data when the source data changes. Common strategies: TTL, event-based, version-based.

```python
# TTL-based
cache.setex("key", 300, value)  # Expires in 5 minutes

# Event-based
@app.put("/users/{user_id}")
async def update_user(user_id: int):
    # Update database
    # Invalidate cache
    cache.delete(f"user:{user_id}")
```

### Q14: How do you implement cursor-based pagination?

**Answer:**
```python
@app.get("/items/")
async def list_items(cursor: str = None, limit: int = 20):
    query = db.query(Item)

    if cursor:
        cursor_data = decode_cursor(cursor)
        query = query.filter(Item.id > cursor_data["last_id"])

    items = query.order_by(Item.id).limit(limit + 1).all()
    has_next = len(items) > limit
    items = items[:limit]

    next_cursor = encode_cursor({"last_id": items[-1].id}) if has_next else None

    return {"items": items, "next_cursor": next_cursor, "has_next": has_next}
```

### Q15: What is the cache-aside pattern?

**Answer:** The application code explicitly manages the cache: check cache → if miss, fetch from DB → cache the result.

```python
def get_or_set(key, factory, ttl=300):
    cached = cache.get(key)
    if cached:
        return json.loads(cached)
    value = factory()
    cache.setex(key, ttl, json.dumps(value))
    return value
```

### Q16: How do you handle slow database queries?

**Answer:**
```python
# 1. Add indexes
# 2. Use EXPLAIN ANALYZE to find bottlenecks
# 3. Use async queries
# 4. Use connection pooling
# 5. Cache query results
# 6. Use read replicas
```

### Q17: What is the difference between Redis and Memcached?

**Answer:**
| Feature | Redis | Memcached |
|---------|-------|-----------|
| Data structures | Strings, lists, sets, hashes | Strings only |
| Persistence | Yes | No |
| Replication | Yes | No |
| Pub/Sub | Yes | No |
| Memory efficiency | Good | Better for simple caching |

### Q18: How do you implement rate limiting?

**Answer:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/data")
@limiter.limit("100/minute")
async def get_data(request: Request):
    return {"data": "value"}
```

### Q19: How do you optimize FastAPI response times?

**Answer:**
```python
# 1. Use async I/O
async def get_data():
    async with httpx.AsyncClient() as client:
        return await client.get("https://api.example.com")

# 2. Cache responses
@app.get("/data")
@lru_cache(maxsize=128)
async def get_data():
    return expensive_computation()

# 3. Use connection pooling
engine = create_engine(url, pool_size=20)

# 4. Paginate responses
@app.get("/items/")
async def list_items(skip: int = 0, limit: int = 20):
    pass
```

### Q20: What is ETag caching?

**Answer:** ETags allow clients to cache responses and only re-fetch when data changes.

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int, request: Request):
    item = db.query(Item).get(item_id)
    etag = generate_etag(item)

    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304)

    response = JSONResponse(item.dict())
    response.headers["ETag"] = etag
    return response
```

---

## 3. Advanced Level (21-30) <a name="3-advanced"></a>

### Q21: How do you implement cache stampede prevention?

**Answer:** Cache stampede occurs when many requests try to compute the same value simultaneously after cache expiration.

```python
import asyncio
import redis

class StampedePrevention:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def get_or_compute(self, key: str, compute_fn, ttl: int = 300):
        # Check cache
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)

        # Try to acquire lock
        lock_key = f"lock:{key}"
        acquired = self.redis.setnx(lock_key, "1")

        if acquired:
            self.redis.expire(lock_key, 10)
            try:
                value = await compute_fn()
                self.redis.setex(key, ttl, json.dumps(value))
                return value
            finally:
                self.redis.delete(lock_key)
        else:
            # Wait and retry
            for _ in range(10):
                await asyncio.sleep(0.1)
                cached = self.redis.get(key)
                if cached:
                    return json.loads(cached)
            return await compute_fn()
```

### Q22: How do you implement write-behind caching?

**Answer:**
```python
import asyncio
from collections import deque

class WriteBehindCache:
    def __init__(self, cache_client, db_session):
        self.cache = cache_client
        self.db = db_session
        self.write_queue = deque()

    def set(self, key: str, value: dict, ttl: int = 300):
        # Write to cache immediately
        self.cache.setex(key, ttl, json.dumps(value))
        # Queue database write
        self.write_queue.append({"key": key, "value": value})

    async def process_writes(self):
        while True:
            if self.write_queue:
                batch = []
                while self.write_queue and len(batch) < 100:
                    batch.append(self.write_queue.popleft())
                for item in batch:
                    await self._save_to_db(item)
            await asyncio.sleep(1)
```

### Q23: How do you implement connection pool monitoring?

**Answer:**
```python
from prometheus_client import Gauge

pool_size = Gauge("db_pool_size", "Database pool size")
pool_checked_out = Gauge("db_pool_checked_out", "Connections checked out")

@app.get("/pool-stats")
async def pool_stats():
    pool = engine.pool
    return {
        "size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
    }
```

### Q24: How do you optimize async operations?

**Answer:**
```python
# BAD: Sequential
async def get_data():
    users = await get_users()      # 100ms
    orders = await get_orders()    # 200ms
    items = await get_items()      # 150ms
    # Total: 450ms

# GOOD: Concurrent
async def get_data():
    users, orders, items = await asyncio.gather(
        get_users(),
        get_orders(),
        get_items(),
    )
    # Total: ~200ms
```

### Q25: How do you implement pagination with total count?

**Answer:**
```python
@app.get("/items/")
async def list_items(skip: int = 0, limit: int = 20):
    # Fast approximate count for large tables
    total = db.query(func.count(Item.id)).scalar()

    items = db.query(Item).offset(skip).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_next": skip + limit < total,
    }
```

### Q26: How do you implement API response caching?

**Answer:**
```python
from fastapi import Response

@app.get("/api/data")
async def get_data(response: Response):
    # Cache for 5 minutes
    response.headers["Cache-Control"] = "private, max-age=300"
    response.headers["ETag"] = generate_etag(data)

    return data
```

### Q27: How do you handle cache invalidation across multiple servers?

**Answer:**
```python
import redis

# Use Redis Pub/Sub for invalidation
class CacheInvalidator:
    def __init__(self, redis_client):
        self.redis = redis_client

    def invalidate(self, pattern: str):
        # Publish invalidation event
        self.redis.publish("cache_invalidation", pattern)
        # Also delete locally
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)
```

### Q28: How do you implement lazy loading in FastAPI?

**Answer:**
```python
from sqlalchemy.orm import lazyload

# Lazy load (default)
items = db.query(Item).all()
for item in items:
    print(item.owner.name)  # Triggers additional query

# Eager load
items = db.query(Item).options(joinedload(Item.owner)).all()
for item in items:
    print(item.owner.name)  # No additional query
```

### Q29: How do you optimize JSON serialization?

**Answer:**
```python
import orjson
from fastapi import Response

@app.get("/items/")
async def list_items():
    items = db.query(Item).all()
    # orjson is faster than default json
    content = orjson.dumps([item.dict() for item in items])
    return Response(content=content, media_type="application/json")
```

### Q30: How do you implement read replicas?

**Answer:**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Write engine
write_engine = create_engine("postgresql://master-host/db")

# Read engine (replica)
read_engine = create_engine("postgresql://replica-host/db")

def get_write_db():
    Session = sessionmaker(bind=write_engine)
    return Session()

def get_read_db():
    Session = sessionmaker(bind=read_engine)
    return Session()

@app.get("/items/")
async def list_items(db: Session = Depends(get_read_db)):
    return db.query(Item).all()

@app.post("/items/")
async def create_item(item: ItemCreate, db: Session = Depends(get_write_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    return db_item
```

---

## 4. Expert Level (31-40) <a name="4-expert"></a>

### Q31: How do you implement circuit breaker pattern?

**Answer:**
```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    async def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit is open")

        try:
            result = await func(*args, **kwargs)
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise
```

### Q32: How do you implement distributed caching?

**Answer:**
```python
import redis
import json
from typing import Optional

class DistributedCache:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    def get(self, key: str) -> Optional[dict]:
        data = self.redis.get(key)
        return json.loads(data) if data else None

    def set(self, key: str, value: dict, ttl: int = 300):
        self.redis.setex(key, ttl, json.dumps(value))

    def delete(self, key: str):
        self.redis.delete(key)

    def get_many(self, keys: list[str]) -> list[dict]:
        pipe = self.redis.pipeline()
        for key in keys:
            pipe.get(key)
        results = pipe.execute()
        return [json.loads(r) if r else None for r in results]
```

### Q33: How do you implement query result caching?

**Answer:**
```python
from sqlalchemy import event
import hashlib

@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    # Generate cache key from query
    cache_key = hashlib.md5(
        f"{statement}{parameters}".encode()
    ).hexdigest()

    # Check cache
    cached = cache.get(f"query:{cache_key}")
    if cached:
        cursor._result = json.loads(cached)
        return

    # Store query info for after execution
    conn.info["cache_key"] = cache_key
```

### Q34: How do you implement API response compression?

**Answer:**
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Or custom compression
import brotli

@app.get("/data")
async def get_data():
    data = {"large": "data" * 10000}
    content = brotli.compress(json.dumps(data).encode())
    return Response(content=content, media_type="application/json")
```

### Q35: How do you implement database query batching?

**Answer:**
```python
async def batch_fetch_users(user_ids: list[int]) -> dict:
    """Batch fetch users to avoid N+1 queries."""
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    return {user.id: user for user in users}

async def get_user_profiles(user_ids: list[int]):
    """Fetch profiles for multiple users."""
    users = await batch_fetch_users(user_ids)
    return [
        {"user_id": uid, "name": users[uid].name}
        for uid in user_ids
        if uid in users
    ]
```

### Q36: How do you implement request coalescing?

**Answer:**
```python
import asyncio
from collections import defaultdict

class RequestCoalescer:
    def __init__(self):
        self.pending = defaultdict(list)
        self.results = {}

    async def get_or_wait(self, key: str, compute_fn):
        if key in self.results:
            return self.results[key]

        future = asyncio.Future()
        self.pending[key].append(future)

        if len(self.pending[key]) == 1:
            # First request - compute
            result = await compute_fn()
            self.results[key] = result

            # Resolve all waiting futures
            for f in self.pending[key]:
                f.set_result(result)

            self.pending.pop(key)

        return await future
```

### Q37: How do you implement response streaming?

**Answer:**
```python
from fastapi.responses import StreamingResponse

@app.get("/stream")
async def stream_data():
    async def generate():
        for i in range(100):
            yield f"data: {i}\n\n"
            await asyncio.sleep(0.1)

    return StreamingResponse(generate(), media_type="text/event-stream")
```

### Q38: How do you implement database connection pooling optimization?

**Answer:**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Calculate optimal pool size
import multiprocessing
cpu_count = multiprocessing.cpu_count()
pool_size = min(cpu_count * 2 + 1, 20)

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=pool_size,
    max_overflow=pool_size // 2,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,
)
```

### Q39: How do you implement cache warming?

**Answer:**
```python
@app.on_event("startup")
async def warm_cache():
    """Pre-populate cache with frequently accessed data."""
    # Warm product listings
    categories = db.query(Category).all()
    for category in categories:
        products = db.query(Product).filter_by(category_id=category.id).all()
        cache.setex(
            f"products:{category.slug}",
            600,
            json.dumps([p.dict() for p in products]),
        )
```

### Q40: How do you implement API response caching with ETags?

**Answer:**
```python
import hashlib
from fastapi import Request, Response

@app.get("/items/{item_id}")
async def get_item(item_id: int, request: Request):
    item = db.query(Item).get(item_id)
    etag = hashlib.md5(json.dumps(item.dict(), sort_keys=True).encode()).hexdigest()

    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304)

    response = JSONResponse(item.dict())
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "max-age=0, must-revalidate"
    return response
```

---

## 5. Practical Scenarios <a name="5-scenarios"></a>

### Scenario 1: "API is slow in production"

**Answer:**
```python
# 1. Profile the endpoint
# 2. Check database query performance
# 3. Add caching
# 4. Use connection pooling
# 5. Implement pagination
# 6. Add indexes
# 7. Use async for I/O operations
```

### Scenario 2: "Database is overloaded"

**Answer:**
```python
# 1. Add connection pooling
# 2. Use read replicas
# 3. Implement caching
# 4. Add database indexes
# 5. Optimize queries
# 6. Use query result caching
# 7. Implement rate limiting
```

### Scenario 3: "Need to handle 10,000 requests per second"

**Answer:**
```python
# 1. Use async endpoints
# 2. Implement caching (Redis)
# 3. Use connection pooling
# 4. Add load balancer
# 5. Scale horizontally
# 6. Use CDN for static content
# 7. Implement rate limiting
```

---

## 6. Code Review Questions <a name="6-code-review"></a>

### Q: Find the performance issues

```python
@app.get("/users/")
async def get_users():
    users = db.query(User).all()
    for user in users:
        user.orders = db.query(Order).filter(Order.user_id == user.id).all()
    return users
```

**Issues:**
1. N+1 query problem (querying orders for each user)
2. No pagination
3. Loading all data at once

### Q: Fix this code

```python
@app.get("/items/")
async def get_items():
    items = []
    for i in range(1000):
        item = db.query(Item).get(i)
        items.append(item)
    return items
```

**Issues:**
1. 1000 individual queries instead of one
2. No pagination
3. Sequential queries

**Fix:**
```python
@app.get("/items/")
async def get_items(skip: int = 0, limit: int = 100):
    items = db.query(Item).offset(skip).limit(limit).all()
    total = db.query(func.count(Item.id)).scalar()
    return {"items": items, "total": total}
```

---

## Summary

### Performance Checklist

- [ ] Implement caching for read-heavy endpoints
- [ ] Use connection pooling for database
- [ ] Paginate all list endpoints
- [ ] Use async for I/O operations
- [ ] Add database indexes
- [ ] Monitor response times
- [ ] Use ETags for conditional requests
- [ ] Implement rate limiting
- [ ] Use CDN for static content
- [ ] Profile regularly

### Quick Reference

| Technique | Benefit | Complexity |
|-----------|---------|-----------|
| Caching | Reduce DB load | Low |
| Connection pooling | Reduce connection overhead | Low |
| Pagination | Reduce data transfer | Low |
| Async I/O | Handle more concurrent requests | Medium |
| Read replicas | Distribute read load | Medium |
| Load balancing | Distribute traffic | High |
| Query optimization | Faster queries | Medium |
| CDN | Reduce latency | Low |
