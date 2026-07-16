# Caching

## Table of Contents

1. [Introduction](#1-introduction)
2. [Redis Caching](#2-redis)
3. [In-Memory Caching](#3-in-memory)
4. [functools.lru_cache](#4-lru-cache)
5. [Cache-Aside Pattern](#5-cache-aside)
6. [Write-Through and Write-Behind](#6-write-patterns)
7. [Cache Invalidation](#7-invalidation)
8. [ETag and If-None-Match](#8-etag)
9. [HTTP Caching Headers](#9-http-caching)
10. [CDN Caching](#10-cdn)
11. [Cache Patterns](#11-patterns)
12. [Best Practices](#12-best-practices)

---

## 1. Introduction <a name="1-introduction"></a>

Caching stores frequently accessed data in a fast-access layer to reduce database
load and improve response times. For FastAPI applications, caching is critical
for performance at scale.

### Caching Layers

```
Client → CDN Cache → Reverse Proxy (Nginx) → Application Cache → Database
```

### When to Cache

- Read-heavy endpoints
- Expensive computations
- External API responses
- Database query results
- Static content
- Session data

### When NOT to Cache

- Real-time data (stock prices, live scores)
- Frequently changing data
- Personalized data (user-specific)
- Write-heavy workloads

---

## 2. Redis Caching <a name="2-redis"></a>

### Basic Redis Cache

```python
import redis
import json
from typing import Optional

class RedisCache:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url, decode_responses=True)

    def get(self, key: str) -> Optional[str]:
        return self.redis.get(key)

    def set(
        self,
        key: str,
        value: str,
        ttl: int = 300,
    ):
        self.redis.setex(key, ttl, value)

    def delete(self, key: str):
        self.redis.delete(key)

    def exists(self, key: str) -> bool:
        return self.redis.exists(key) > 0

    def increment(self, key: str) -> int:
        return self.redis.incr(key)

# Usage
cache = RedisCache()

async def get_item(item_id: int):
    cache_key = f"item:{item_id}"

    # Check cache first
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)

    # Cache miss - fetch from DB
    item = db.query(Item).get(item_id)
    if item:
        cache.set(cache_key, json.dumps(item.dict()), ttl=600)

    return item
```

### Redis with JSON Serialization

```python
import redis
import json
from datetime import datetime
from typing import Any

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class RedisJSONCache:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url, decode_responses=True)

    def get_json(self, key: str) -> Any:
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    def set_json(self, key: str, value: Any, ttl: int = 300):
        self.redis.setex(key, ttl, json.dumps(value, cls=JSONEncoder))

    def get_or_set(
        self,
        key: str,
        factory,
        ttl: int = 300,
    ) -> Any:
        """Get from cache or compute and cache."""
        cached = self.get_json(key)
        if cached is not None:
            return cached

        value = factory()
        self.set_json(key, value, ttl)
        return value

# Usage
cache = RedisJSONCache("redis://localhost:6379")

def get_user(user_id: int):
    return cache.get_or_set(
        f"user:{user_id}",
        lambda: db.query(User).get(user_id).dict(),
        ttl=300,
    )
```

### Redis Pipeline for Bulk Operations

```python
def get_multiple_items(item_ids: list[int]) -> list[dict]:
    """Fetch multiple items using Redis pipeline."""
    pipe = cache.redis.pipeline()

    for item_id in item_ids:
        pipe.get(f"item:{item_id}")

    results = pipe.execute()

    items = []
    missing_ids = []

    for item_id, result in zip(item_ids, results):
        if result:
            items.append(json.loads(result))
        else:
            missing_ids.append(item_id)

    # Fetch missing items from DB
    if missing_ids:
        db_items = db.query(Item).filter(Item.id.in_(missing_ids)).all()
        pipe = cache.redis.pipeline()

        for item in db_items:
            pipe.setex(
                f"item:{item.id}",
                600,
                json.dumps(item.dict()),
            )
            items.append(item.dict())

        pipe.execute()

    return items
```

### Redis Pub/Sub for Cache Invalidation

```python
import threading

class RedisCacheWithPubSub:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.pubsub = self.redis.pubsub()

    def publish_invalidation(self, pattern: str):
        """Publish cache invalidation event."""
        self.redis.publish("cache_invalidation", pattern)

    def subscribe_to_invalidations(self):
        """Subscribe to cache invalidation events."""
        self.pubsub.subscribe(**{
            "cache_invalidation": self.handle_invalidation,
        })
        thread = threading.Thread(target=self.pubsub.run_in_forever)
        thread.daemon = True
        thread.start()

    def handle_invalidation(self, message):
        pattern = message["data"]
        # Delete matching keys
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)
```

---

## 3. In-Memory Caching <a name="3-in-memory"></a>

### Simple In-Memory Cache

```python
import time
from typing import Any, Optional
from collections import OrderedDict
import threading

class LRUCache:
    """Thread-safe LRU cache with TTL support."""

    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache = OrderedDict()
        self.timestamps = {}
        self.lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None

            # Check TTL
            if time.time() - self.timestamps[key] > self.default_ttl:
                del self.cache[key]
                del self.timestamps[key]
                return None

            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]

    def set(self, key: str, value: Any, ttl: int = None):
        with self.lock:
            if key in self.cache:
                del self.cache[key]
            elif len(self.cache) >= self.max_size:
                # Remove oldest item
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
                del self.timestamps[oldest_key]

            self.cache[key] = value
            self.timestamps[key] = time.time()

    def delete(self, key: str):
        with self.lock:
            self.cache.pop(key, None)
            self.timestamps.pop(key, None)

    def clear(self):
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()

# Usage
memory_cache = LRUCache(max_size=1000, default_ttl=300)

def get_expensive_data(key: str):
    cached = memory_cache.get(key)
    if cached is not None:
        return cached

    # Compute expensive result
    result = expensive_computation(key)
    memory_cache.set(key, result)
    return result
```

### cachetools Library

```python
from cachetools import TTLCache, LRUCache, cached
import cachetools

# TTL cache with automatic expiration
ttl_cache = TTLCache(maxsize=1000, ttl=300)

# LRU cache
lru_cache = LRUCache(maxsize=1000)

# Using decorators
@cached(cache=ttl_cache, key=lambda user_id: f"user:{user_id}")
def get_user(user_id: int) -> dict:
    return db.query(User).get(user_id).dict()

@cached(cache=lru_cache, key=lambda path: f"template:{path}")
def render_template(path: str) -> str:
    return render(path)

# Thread-safe cache
from cachetools import cachedmethod
import threading

class CacheManager:
    def __init__(self):
        self._cache = TTLCache(maxsize=1000, ttl=300)
        self._lock = threading.Lock()

    @cachedmethod(lambda self: self._cache, key=lambda self, k: k)
    def get(self, key: str):
        return self._compute(key)

    def _compute(self, key: str):
        return expensive_computation(key)
```

### FastAPI In-Memory Cache

```python
from fastapi import FastAPI
from cachetools import TTLCache

app = FastAPI()

# Application-level cache
app.state.cache = TTLCache(maxsize=1000, ttl=300)

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    cache = app.state.cache
    cache_key = f"item:{item_id}"

    # Check cache
    if cache_key in cache:
        return cache[cache_key]

    # Fetch from DB
    item = db.query(Item).get(item_id)
    if item:
        cache[cache_key] = item.dict()

    return item.dict()

@app.post("/items/{item_id}/invalidate")
async def invalidate_cache(item_id: int):
    cache = app.state.cache
    cache_key = f"item:{item_id}"
    cache.pop(cache_key, None)
    return {"detail": "Cache invalidated"}
```

---

## 4. functools.lru_cache <a name="4-lru-cache"></a>

### Basic Usage

```python
from functools import lru_cache
import time

# Simple LRU cache
@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Cached with TTL (Python 3.9+)
from functools import cache  # Unlimited cache

@cache
def expensive_function(x: int) -> int:
    time.sleep(1)  # Simulate slow computation
    return x * x

# Clear cache
fibonacci.cache_clear()

# Get cache info
print(fibonacci.cache_info())
# CacheInfo(hits=5, misses=10, maxsize=128, currsize=10)
```

### LRU Cache for API Endpoints

```python
from fastapi import FastAPI, Query
from functools import lru_cache
import hashlib

app = FastAPI()

def make_cache_key(*args, **kwargs) -> str:
    """Create a cache key from function arguments."""
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    return hashlib.md5(":".join(key_parts).encode()).hexdigest()

@lru_cache(maxsize=256)
def get_products_from_db(category: str, min_price: float, max_price: float) -> list:
    """Expensive database query, cached by arguments."""
    return db.query(Product).filter(
        Product.category == category,
        Product.price >= min_price,
        Product.price <= max_price,
    ).all()

@app.get("/products/")
async def list_products(
    category: str = Query("all"),
    min_price: float = Query(0),
    max_price: float = Query(10000),
):
    products = get_products_from_db(category, min_price, max_price)
    return {"products": [p.dict() for p in products]}
```

### TTL Cache with TTL

```python
from functools import lru_cache
from datetime import datetime
import time

class TTLCache:
    """Simple TTL cache implementation."""

    def __init__(self, ttl: int = 300):
        self.ttl = ttl
        self.cache = {}
        self.timestamps = {}

    def __call__(self, func):
        @lru_cache(maxsize=128)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))
            now = time.time()

            if key in self.cache:
                if now - self.timestamps[key] < self.ttl:
                    return self.cache[key]
                else:
                    del self.cache[key]
                    del self.timestamps[key]

            result = func(*args, **kwargs)
            self.cache[key] = result
            self.timestamps[key] = now
            return result

        wrapper.cache_clear = self.cache.clear
        return wrapper

@TTLCache(ttl=60)
def get_weather(city: str) -> dict:
    """Weather data, cached for 60 seconds."""
    return fetch_weather_from_api(city)
```

---

## 5. Cache-Aside Pattern <a name="5-cache-aside"></a>

The application code explicitly manages the cache:

```python
import json
from typing import Optional, Callable

class CacheAside:
    def __init__(self, cache_client, serializer=json):
        self.cache = cache_client
        self.serializer = serializer

    def get_or_set(
        self,
        key: str,
        factory: Callable,
        ttl: int = 300,
    ):
        """Cache-aside: Check cache, then DB, then cache result."""
        # 1. Check cache
        cached = self.cache.get(key)
        if cached is not None:
            return self.serializer.loads(cached)

        # 2. Cache miss - execute factory
        value = factory()

        # 3. Cache the result
        if value is not None:
            self.cache.setex(
                key,
                ttl,
                self.serializer.dumps(value),
            )

        return value

    def invalidate(self, key: str):
        """Invalidate cache entry."""
        self.cache.delete(key)

    def invalidate_pattern(self, pattern: str):
        """Invalidate all keys matching pattern."""
        keys = self.cache.keys(pattern)
        if keys:
            self.cache.delete(*keys)

# Usage
cache_aside = CacheAside(redis_client)

def get_user(user_id: int):
    return cache_aside.get_or_set(
        f"user:{user_id}",
        lambda: db.query(User).get(user_id).dict(),
        ttl=300,
    )

def get_products(category: str):
    return cache_aside.get_or_set(
        f"products:{category}",
        lambda: [p.dict() for p in db.query(Product).filter_by(category=category).all()],
        ttl=600,
    )

@app.put("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate):
    user = db.query(User).get(user_id)
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()

    # Invalidate cache
    cache_aside.invalidate(f"user:{user_id}")
    cache_aside.invalidate_pattern("users:list:*")

    return user.dict()
```

---

## 6. Write-Through and Write-Behind <a name="6-write-patterns"></a>

### Write-Through (Write to cache AND database)

```python
class WriteThroughCache:
    def __init__(self, cache_client, db_session):
        self.cache = cache_client
        self.db = db_session

    def set(self, key: str, value: dict, ttl: int = 300):
        """Write to both cache and database."""
        # Write to database
        db_obj = self._save_to_db(key, value)

        # Write to cache
        self.cache.setex(key, ttl, json.dumps(value))

        return db_obj

    def _save_to_db(self, key: str, value: dict):
        # Implementation depends on your model
        pass

# Usage
cache = WriteThroughCache(redis_client, db_session)

async def update_product(product_id: int, data: dict):
    return cache.set(f"product:{product_id}", data, ttl=600)
```

### Write-Behind (Write to cache, async write to database)

```python
import asyncio
from collections import deque

class WriteBehindCache:
    def __init__(self, cache_client, db_session):
        self.cache = cache_client
        self.db = db_session
        self.write_queue = deque()
        self._running = True

    def set(self, key: str, value: dict, ttl: int = 300):
        """Write to cache, queue database write."""
        # Write to cache immediately
        self.cache.setex(key, ttl, json.dumps(value))

        # Queue database write
        self.write_queue.append({"key": key, "value": value})

    async def process_writes(self):
        """Background task to process queued writes."""
        while self._running:
            if self.write_queue:
                batch = []
                while self.write_queue and len(batch) < 100:
                    batch.append(self.write_queue.popleft())

                for item in batch:
                    await self._save_to_db(item["key"], item["value"])

            await asyncio.sleep(1)

    async def _save_to_db(self, key: str, value: dict):
        # Batch insert/update
        pass
```

---

## 7. Cache Invalidation <a name="7-invalidation"></a>

### Time-Based Invalidation

```python
# Simple TTL-based
cache.setex("key", 300, value)  # Expires in 5 minutes

# Different TTLs for different data types
TTL_CONFIG = {
    "user": 300,          # 5 minutes
    "product": 600,       # 10 minutes
    "category": 1800,     # 30 minutes
    "config": 3600,       # 1 hour
    "session": 86400,     # 24 hours
}
```

### Event-Based Invalidation

```python
class CacheInvalidator:
    def __init__(self, cache_client):
        self.cache = cache_client

    def on_user_update(self, user_id: int):
        """Invalidate user cache on update."""
        self.cache.delete(f"user:{user_id}")
        self.cache.delete(f"user:{user_id}:profile")
        self.cache.delete(f"user:{user_id}:settings")

    def on_product_update(self, product_id: int):
        """Invalidate product cache on update."""
        self.cache.delete(f"product:{product_id}")
        # Also invalidate product lists
        self.cache.delete_pattern("products:*")

    def on_category_update(self, category_id: int):
        """Invalidate category and related product caches."""
        self.cache.delete(f"category:{category_id}")
        self.cache.delete_pattern("products:category:*")

# Usage
invalidator = CacheInvalidator(redis_client)

@app.put("/users/{user_id}")
async def update_user(user_id: int, data: UserUpdate):
    user = db.query(User).get(user_id)
    # ... update user ...
    db.commit()

    # Invalidate relevant caches
    invalidator.on_user_update(user_id)
    return user.dict()
```

### Tag-Based Invalidation

```python
class TaggedCache:
    def __init__(self, cache_client):
        self.cache = cache_client

    def set_with_tags(self, key: str, value: str, tags: list[str], ttl: int = 300):
        """Cache value with tags for grouped invalidation."""
        self.cache.setex(key, ttl, value)

        for tag in tags:
            self.cache.sadd(f"tag:{tag}", key)
            self.cache.expire(f"tag:{tag}", ttl)

    def invalidate_tag(self, tag: str):
        """Invalidate all cache entries with a tag."""
        keys = self.cache.smembers(f"tag:{tag}")
        if keys:
            self.cache.delete(*keys)
            self.cache.delete(f"tag:{tag}")

# Usage
tagged_cache = TaggedCache(redis_client)

# Cache with tags
tagged_cache.set_with_tags(
    "product:1",
    json.dumps(product.dict()),
    tags=["products", "category:electronics"],
)

# Invalidate all products
tagged_cache.invalidate_tag("products")
```

---

## 8. ETag and If-None-Match <a name="8-etag"></a>

```python
import hashlib
from fastapi import FastAPI, Request, Response
from starlette.responses import JSONResponse

app = FastAPI()

def generate_etag(data: dict) -> str:
    """Generate ETag from response data."""
    content = json.dumps(data, sort_keys=True)
    return hashlib.md5(content.encode()).hexdigest()

@app.get("/items/{item_id}")
async def get_item(item_id: int, request: Request):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    data = item.dict()
    etag = generate_etag(data)

    # Check If-None-Match header
    if_none_match = request.headers.get("if-none-match")
    if if_none_match == etag:
        return Response(status_code=304)

    response = JSONResponse(content=data)
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "max-age=0, must-revalidate"
    return response

@app.get("/items/")
async def list_items(request: Request):
    items = db.query(Item).all()
    data = [item.dict() for item in items]
    etag = generate_etag(data)

    if_none_match = request.headers.get("if-none-match")
    if if_none_match == etag:
        return Response(status_code=304)

    response = JSONResponse(content=data)
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "max-age=0, must-revalidate"
    return response
```

---

## 9. HTTP Caching Headers <a name="9-http-caching"></a>

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta

app = FastAPI()

class CachingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, cache_control_config: dict = None):
        super().__init__(app)
        self.config = cache_control_config or {}

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        path = request.url.path

        # Static assets - aggressive caching
        if path.startswith("/static/"):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"

        # API responses - moderate caching
        elif path.startswith("/api/"):
            if request.method == "GET":
                response.headers["Cache-Control"] = "private, max-age=60"
            else:
                response.headers["Cache-Control"] = "no-store"

        # HTML pages - short caching
        elif path.endswith(".html") or path == "/":
            response.headers["Cache-Control"] = "public, max-age=300"

        # No cache for auth endpoints
        elif path.startswith("/auth/"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"

        return response

app.add_middleware(CachingMiddleware)
```

### Cache-Control Directives

```python
# Directives
DIRECTIVES = {
    "public": "Response can be cached by any cache",
    "private": "Response only for single user",
    "no-cache": "Must revalidate before using cached version",
    "no-store": "Don't cache at all",
    "max-age": "Max seconds the response is fresh",
    "s-maxage": "Max seconds for shared caches (CDN)",
    "must-revalidate": "Must check with server when stale",
    "proxy-revalidate": "Same as must-revalidate for proxies",
    "immutable": "Response will never change",
}

# Common configurations
CACHE_CONFIGS = {
    "static_assets": "public, max-age=31536000, immutable",
    "api_list": "private, max-age=60, must-revalidate",
    "api_detail": "private, max-age=300, must-revalidate",
    "html_page": "public, max-age=300, must-revalidate",
    "no_cache": "no-store, no-cache, must-revalidate",
    "cdn_cache": "public, max-age=86400, s-maxage=604800",
}
```

---

## 10. CDN Caching <a name="10-cdn"></a`

```python
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/api/products/{product_id}")
async def get_product(product_id: int, response: Response):
    product = db.query(Product).get(product_id)

    # CDN-friendly headers
    response.headers["Cache-Control"] = "public, max-age=300, s-maxage=3600"
    response.headers["CDN-Cache-Control"] = "public, max-age=3600"
    response.headers["Vary"] = "Accept-Encoding, Authorization"

    return product.dict()

@app.get("/api/user/profile")
async def get_profile(user: User = Depends(get_current_user)):
    # Private - don't cache at CDN
    response = JSONResponse(content=user.dict())
    response.headers["Cache-Control"] = "private, no-cache"
    response.headers["Vary"] = "Authorization"
    return response
```

### CloudFlare Cache Rules

```python
# Set CloudFlare-specific headers
@app.get("/api/data")
async def get_data(response: Response):
    response.headers["Cache-Control"] = "public, max-age=300"
    response.headers["Cloudflare-CDN-Cache-Control"] = "max-age=3600"
    response.headers["CF-Cache-Status"] = "HIT"  # Or MISS
    return {"data": "value"}
```

---

## 11. Cache Patterns <a name="11-patterns"></a>

### Cache Stampede Prevention

```python
import asyncio
import time

class StampedePrevention:
    def __init__(self, cache_client):
        self.cache = cache_client
        self.locks = {}

    async def get_or_set(
        self,
        key: str,
        factory,
        ttl: int = 300,
        lock_ttl: int = 10,
    ):
        """Prevent cache stampede with locking."""
        # Check cache first
        cached = self.cache.get(key)
        if cached:
            return json.loads(cached)

        # Acquire lock
        lock_key = f"lock:{key}"
        acquired = self.cache.setnx(lock_key, "1")

        if acquired:
            self.cache.expire(lock_key, lock_ttl)
            try:
                # Compute value
                value = await factory()
                self.cache.setex(key, ttl, json.dumps(value))
                return value
            finally:
                self.cache.delete(lock_key)
        else:
            # Another process is computing, wait and retry
            for _ in range(10):
                await asyncio.sleep(0.1)
                cached = self.cache.get(key)
                if cached:
                    return json.loads(cached)
            # Fallback to direct computation
            return await factory()
```

### Cache Warming

```python
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

    # Warm popular products
    popular = db.query(Product).order_by(Product.views.desc()).limit(100).all()
    for product in popular:
        cache.setex(
            f"product:{product.id}",
            600,
            json.dumps(product.dict()),
        )

@app.on_event("startup")
async def startup():
    await warm_cache()
```

### Cache Refresh

```python
class RefreshAheadCache:
    """Refresh cache before expiration."""

    def __init__(self, cache_client):
        self.cache = cache_client

    def get_or_set(self, key: str, factory, ttl: int = 300):
        cached = self.cache.get(key)
        if cached:
            data = json.loads(cached)

            # Check if refresh needed
            if data.get("_expires_at", 0) < time.time() + 60:
                # Refresh in background
                asyncio.create_task(self._refresh(key, factory, ttl))

            return data.get("value")
        else:
            value = factory()
            self._cache_with_expiry(key, value, ttl)
            return value

    async def _refresh(self, key: str, factory, ttl: int):
        value = await factory() if asyncio.iscoroutinefunction(factory) else factory()
        self._cache_with_expiry(key, value, ttl)

    def _cache_with_expiry(self, key: str, value: Any, ttl: int):
        data = {
            "value": value,
            "_expires_at": time.time() + ttl,
        }
        self.cache.setex(key, ttl, json.dumps(data))
```

---

## 12. Best Practices <a name="12-best-practices"></a>

### 1. Cache Keys Strategy

```python
# Use consistent naming
CACHE_KEYS = {
    "user": lambda id: f"user:{id}",
    "user_profile": lambda id: f"user:{id}:profile",
    "products": lambda category: f"products:{category}",
    "product_list": lambda **filters: f"products:list:{hash(frozenset(filters.items()))}",
}

# Use versioned keys
def cache_key(version: str, key: str) -> str:
    return f"v{version}:{key}"

# Clear old version on deploy
def clear_old_cache(version: str):
    keys = cache.keys(f"v{version}:*")
    if keys:
        cache.delete(*keys)
```

### 2. Cache Size Management

```python
# Monitor cache size
def get_cache_stats():
    info = cache.info()
    return {
        "used_memory": info["used_memory"],
        "keys": info["db0"]["keys"],
        "hit_rate": info.get("keyspace_hits", 0) / (
            info.get("keyspace_hits", 0) + info.get("keyspace_misses", 1)
        ),
    }
```

### 3. Graceful Degradation

```python
def get_with_fallback(key: str, factory, ttl: int = 300):
    """Cache with database fallback if cache fails."""
    try:
        cached = cache.get(key)
        if cached:
            return json.loads(cached)
    except redis.ConnectionError:
        logger.warning("Cache unavailable, falling back to database")

    # Always compute value
    value = factory()

    try:
        cache.setex(key, ttl, json.dumps(value))
    except redis.ConnectionError:
        logger.warning("Failed to set cache")

    return value
```

---

## Summary

| Pattern | Best For | Complexity |
|---------|----------|-----------|
| Redis Cache | Distributed, persistent | Medium |
| In-Memory | Single server, fast access | Low |
| lru_cache | Pure functions, simple | Low |
| Cache-Aside | Most use cases | Medium |
| Write-Through | Data consistency | Medium |
| Write-Behind | High write throughput | High |
| ETag | Browser caching | Low |
| CDN | Static content, global | Low |

### Key Rules

1. Cache reads, not writes (usually)
2. Set appropriate TTLs
3. Implement cache invalidation
4. Handle cache misses gracefully
5. Monitor cache hit rates
6. Use consistent key naming
7. Prevent cache stampede
8. Warm cache on startup
