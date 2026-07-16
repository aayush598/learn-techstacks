# Rate Limiting in FastAPI

## Table of Contents
1. [Rate Limiting Concepts](#rate-limiting-concepts)
2. [In-Memory Rate Limiting](#in-memory-rate-limiting)
3. [Redis-Based Rate Limiting](#redis-based-rate-limiting)
4. [Sliding Window Algorithm](#sliding-window-algorithm)
5. [Token Bucket Algorithm](#token-bucket-algorithm)
6. [Fixed Window Algorithm](#fixed-window-algorithm)
7. [Rate Limit Headers](#rate-limit-headers)
8. [Rate Limiting Middleware](#rate-limiting-middleware)
9. [Per-User/Per-IP/Per-API-Key Limits](#per-userper-ipper-api-key-limits)
10. [429 Responses](#429-responses)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## Rate Limiting Concepts

Rate limiting restricts how many requests a client can make within a given time window. It protects APIs from abuse, ensures fair resource usage, and maintains service stability.

### Why Rate Limit?

- **Prevent abuse**: Stop DDoS attacks and brute force attempts
- **Ensure fairness**: Prevent one client from monopolizing resources
- **Cost control**: Limit resource consumption for third-party APIs
- **Service stability**: Prevent overload on backend services
- **SLA compliance**: Ensure consistent performance for all clients

### Common Rate Limiting Algorithms

| Algorithm | Pros | Cons | Use Case |
|-----------|------|------|----------|
| Fixed Window | Simple, memory efficient | Burst at window edges | Basic rate limiting |
| Sliding Window Log | Precise | High memory usage | Precise limiting |
| Sliding Window Counter | Good balance | Approximate | General purpose |
| Token Bucket | Handles bursts smoothly | More complex | APIs with burst traffic |
| Leaky Bucket | Smooths traffic | Configures rate precisely | Queue-based systems |

### Rate Limiting Terminology

- **Window**: Time period for counting requests (e.g., 1 minute)
- **Limit**: Maximum requests allowed in a window
- **Remaining**: Requests left in the current window
- **Reset**: Time when the current window expires
- **Throttle**: The action of rejecting requests

---

## In-Memory Rate Limiting

### Simple In-Memory Counter

```python
import time
from collections import defaultdict
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class InMemoryRateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds

        # Remove old requests outside the window
        self.requests[key] = [
            t for t in self.requests[key] if t > window_start
        ]

        if len(self.requests[key]) >= self.max_requests:
            return False

        self.requests[key].append(now)
        return True

    def get_remaining(self, key: str) -> int:
        now = time.time()
        window_start = now - self.window_seconds
        valid_requests = [t for t in self.requests[key] if t > window_start]
        return max(0, self.max_requests - len(valid_requests))

    def get_reset_time(self) -> float:
        return self.window_seconds

rate_limiter = InMemoryRateLimiter(max_requests=100, window_seconds=60)

@app.get("/api/data")
async def get_data(request: Request):
    client_ip = request.client.host
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(rate_limiter.get_reset_time())}
        )
    remaining = rate_limiter.get_remaining(client_ip)
    return {"data": "value", "remaining": remaining}
```

### In-Memory Rate Limiting Middleware

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class InMemoryRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        window_start = now - self.window_seconds

        # Clean old entries
        self.requests[client_ip] = [
            t for t in self.requests[client_ip] if t > window_start
        ]

        if len(self.requests[client_ip]) >= self.max_requests:
            retry_after = int(
                self.requests[client_ip][0] + self.window_seconds - now
            )
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "retry_after": retry_after,
                },
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(
                        int(self.requests[client_ip][0] + self.window_seconds)
                    ),
                }
            )

        self.requests[client_ip].append(now)
        remaining = self.max_requests - len(self.requests[client_ip])

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response

app.add_middleware(
    InMemoryRateLimitMiddleware,
    max_requests=100,
    window_seconds=60,
)
```

### Limitations of In-Memory

- **Not shared**: Each worker process has its own state
- **Lost on restart**: All counters are lost
- **Memory growth**: Unbounded memory usage if keys aren't cleaned up
- **Not suitable for distributed systems**

---

## Redis-Based Rate Limiting

### Basic Redis Rate Limiter

```python
import redis.asyncio as redis
import time
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

redis_client = redis.from_url("redis://localhost:6379")

class RedisRateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def is_allowed(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        pipeline = redis_client.pipeline()

        # Remove old entries
        pipeline.zremrangebyscore(key, 0, window_start)
        # Add current request
        pipeline.zadd(key, {str(now): now})
        # Count requests in window
        pipeline.zcard(key)
        # Set expiry
        pipeline.expire(key, self.window_seconds)

        results = await pipeline.execute()
        request_count = results[2]

        if request_count > self.max_requests:
            # Remove the added request (it's over limit)
            await redis_client.zrem(key, str(now))
            return False

        return True

    async def get_remaining(self, key: str) -> int:
        now = time.time()
        window_start = now - self.window_seconds
        count = await redis_client.zcount(key, window_start, now)
        return max(0, self.max_requests - count)

rate_limiter = RedisRateLimiter(max_requests=100, window_seconds=60)

@app.get("/api/data")
async def get_data(request: Request):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"

    if not await rate_limiter.is_allowed(key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    remaining = await rate_limiter.get_remaining(key)
    return {"data": "value", "remaining": remaining}
```

### Using lua scripts for atomicity

```python
RATE_LIMIT_SCRIPT = """
local key = KEYS[1]
local max_requests = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

-- Remove expired entries
redis.call('ZREMRANGEBYSCORE', key, 0, now - window)

-- Count current requests
local count = redis.call('ZCARD', key)

if count >= max_requests then
    return 0
end

-- Add current request
redis.call('ZADD', key, now, now)
redis.call('EXPIRE', key, window)

return 1
"""

class AtomicRedisRateLimiter:
    def __init__(self, redis_client, max_requests: int = 100, window_seconds: int = 60):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.script = None

    async def init_script(self):
        self.script = await self.redis.script_load(RATE_LIMIT_SCRIPT)

    async def is_allowed(self, key: str) -> bool:
        now = time.time()
        result = await self.redis.evalsha(
            self.script,
            1,
            key,
            self.max_requests,
            self.window_seconds,
            now,
        )
        return result == 1

limiter = AtomicRedisRateLimiter(
    redis_client, max_requests=100, window_seconds=60
)

@app.on_event("startup")
async def startup():
    await limiter.init_script()
```

---

## Sliding Window Algorithm

### Sliding Window Log

Stores timestamp of each request and counts requests in the window.

```python
import time
import redis.asyncio as redis

class SlidingWindowLog:
    def __init__(self, redis_client, max_requests: int, window_seconds: int):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def is_allowed(self, key: str) -> tuple[bool, dict]:
        now = time.time()
        window_start = now - self.window_seconds

        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)
        pipe.zadd(key, {f"{now}": now})
        pipe.zcard(key)
        pipe.expire(key, self.window_seconds)
        results = await pipe.execute()

        count = results[2]
        remaining = max(0, self.max_requests - count)

        if count > self.max_requests:
            await self.redis.zrem(key, f"{now}")
            oldest = await self.redis.zrange(key, 0, 0, withscores=True)
            retry_after = int(oldest[0][1] + self.window_seconds - now) if oldest else self.window_seconds
            return False, {
                "limit": self.max_requests,
                "remaining": 0,
                "reset": int(now + retry_after),
                "retry_after": retry_after,
            }

        return True, {
            "limit": self.max_requests,
            "remaining": remaining,
            "reset": int(now + self.window_seconds),
        }
```

### Sliding Window Counter (Hybrid)

Approximates the count using fixed windows with weighted overlap.

```python
import math
import redis.asyncio as redis
import time

class SlidingWindowCounter:
    def __init__(self, redis_client, max_requests: int, window_seconds: int):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def is_allowed(self, key: str) -> tuple[bool, dict]:
        now = time.time()
        current_window = int(now // self.window_seconds)
        previous_window = current_window - 1
        window_start = current_window * self.window_seconds
        elapsed = now - window_start

        prev_key = f"{key}:{previous_window}"
        curr_key = f"{key}:{current_window}"

        pipe = self.redis.pipeline()
        pipe.get(prev_key)
        pipe.get(curr_key)
        pipe.incr(curr_key)
        pipe.expire(curr_key, self.window_seconds * 2)
        results = await pipe.execute()

        prev_count = int(results[0] or 0)
        curr_count = int(results[1] or 0)

        # Weighted count from previous window
        weight = 1 - (elapsed / self.window_seconds)
        estimated = prev_count * weight + curr_count + 1

        if estimated > self.max_requests:
            # Undo the increment
            await self.redis.decr(curr_key)
            retry_after = int(self.window_seconds - elapsed)
            return False, {
                "limit": self.max_requests,
                "remaining": 0,
                "reset": int(now + retry_after),
                "retry_after": retry_after,
            }

        remaining = max(0, int(self.max_requests - estimated))
        return True, {
            "limit": self.max_requests,
            "remaining": remaining,
            "reset": int(current_window * self.window_seconds + self.window_seconds),
        }
```

---

## Token Bucket Algorithm

### How It Works

- Bucket holds up to `max_tokens` tokens
- Each request consumes one token
- Tokens are added at a fixed rate (e.g., 10 tokens/second)
- If no tokens available, request is rejected

### Implementation

```python
import time
import redis.asyncio as redis

class TokenBucket:
    def __init__(
        self,
        redis_client,
        max_tokens: int = 100,
        refill_rate: float = 10.0,  # tokens per second
    ):
        self.redis = redis_client
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate

    async def is_allowed(self, key: str) -> tuple[bool, dict]:
        now = time.time()

        lua_script = """
        local key = KEYS[1]
        local max_tokens = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])

        local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
        local tokens = tonumber(bucket[1])
        local last_refill = tonumber(bucket[2])

        if tokens == nil then
            tokens = max_tokens
            last_refill = now
        end

        -- Refill tokens
        local elapsed = now - last_refill
        local new_tokens = math.min(max_tokens, tokens + elapsed * refill_rate)

        if new_tokens >= 1 then
            new_tokens = new_tokens - 1
            redis.call('HMSET', key, 'tokens', new_tokens, 'last_refill', now)
            redis.call('EXPIRE', key, math.ceil(max_tokens / refill_rate) + 10)
            return {1, new_tokens, 0}
        else
            -- Calculate wait time for next token
            local wait_time = math.ceil((1 - new_tokens) / refill_rate)
            redis.call('HMSET', key, 'tokens', new_tokens, 'last_refill', now)
            redis.call('EXPIRE', key, math.ceil(max_tokens / refill_rate) + 10)
            return {0, 0, wait_time}
        end
        """

        result = await self.redis.eval(
            lua_script,
            1,
            key,
            self.max_tokens,
            self.refill_rate,
            now,
        )

        allowed = result[0] == 1
        remaining = result[1] if allowed else 0
        retry_after = result[2]

        return allowed, {
            "limit": self.max_tokens,
            "remaining": remaining,
            "retry_after": retry_after,
        }

bucket = TokenBucket(redis_client, max_tokens=100, refill_rate=10.0)

@app.get("/api/data")
async def get_data(request: Request):
    key = f"token_bucket:{request.client.host}"
    allowed, info = await bucket.is_allowed(key)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(info["retry_after"])},
        )
    return {"data": "value", "remaining": info["remaining"]}
```

---

## Fixed Window Algorithm

### How It Works

- Divide time into fixed windows (e.g., 1-minute intervals)
- Count requests in the current window
- Reject if count exceeds limit

### Implementation

```python
import time
import redis.asyncio as redis

class FixedWindow:
    def __init__(self, redis_client, max_requests: int, window_seconds: int):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def is_allowed(self, key: str) -> tuple[bool, dict]:
        now = time.time()
        window = int(now // self.window_seconds)
        window_key = f"{key}:{window}"

        pipe = self.redis.pipeline()
        pipe.incr(window_key)
        pipe.expire(window_key, self.window_seconds)
        results = await pipe.execute()

        count = results[0]

        if count > self.max_requests:
            await self.redis.decr(window_key)
            reset_time = (window + 1) * self.window_seconds
            return False, {
                "limit": self.max_requests,
                "remaining": 0,
                "reset": int(reset_time),
                "retry_after": int(reset_time - now),
            }

        remaining = self.max_requests - count
        reset_time = (window + 1) * self.window_seconds
        return True, {
            "limit": self.max_requests,
            "remaining": remaining,
            "reset": int(reset_time),
        }
```

---

## Rate Limit Headers

### Standard Headers

```python
from fastapi import Response

@app.get("/api/data")
async def get_data(response: Response):
    # Standard rate limit headers
    response.headers["X-RateLimit-Limit"] = "100"
    response.headers["X-RateLimit-Remaining"] = "99"
    response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)
    return {"data": "value"}

# Draft RFC 6585 / IETF headers
response.headers["RateLimit-Limit"] = "100"
response.headers["RateLimit-Remaining"] = "99"
response.headers["RateLimit-Reset"] = str(int(time.time()) + 60)

# Retry-After header (required with 429)
response.headers["Retry-After"] = "30"  # seconds
```

### Header Middleware

```python
class RateLimitHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter):
        super().__init__(app)
        self.limiter = limiter

    async def dispatch(self, request: Request, call_next):
        key = f"rate_limit:{request.client.host}"
        allowed, info = await self.limiter.is_allowed(key)

        response = await call_next(request) if allowed else Response(
            status_code=429,
            content={"detail": "Rate limit exceeded"},
        )

        response.headers["X-RateLimit-Limit"] = str(info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(info["reset"])

        if "retry_after" in info:
            response.headers["Retry-After"] = str(info["retry_after"])

        return response
```

---

## Rate Limiting Middleware

### Complete Middleware Implementation

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import FastAPI, Request
import time
import redis.asyncio as redis
from functools import lru_cache

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        redis_url: str = "redis://localhost:6379",
        default_limit: int = 100,
        default_window: int = 60,
    ):
        super().__init__(app)
        self.redis = redis.from_url(redis_url)
        self.default_limit = default_limit
        self.default_window = default_window
        self.custom_limits: dict[str, tuple[int, int]] = {}

    def set_limit(self, path: str, limit: int, window: int):
        self.custom_limits[path] = (limit, window)

    async def dispatch(self, request: Request, call_next):
        # Determine rate limit for this path
        limit, window = self.custom_limits.get(
            request.url.path,
            (self.default_limit, self.default_window)
        )

        # Get rate limit key
        key = f"rate_limit:{request.client.host}:{request.url.path}"

        # Check rate limit
        now = time.time()
        window_start = now - window

        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)
        pipe.zadd(key, {f"{now}:{id(request)}": now})
        pipe.zcard(key)
        pipe.expire(key, window)
        results = await pipe.execute()

        count = results[2]
        remaining = max(0, limit - count)

        if count > limit:
            retry_after = int(window - (now - window_start))
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "retry_after": retry_after,
                },
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(now + retry_after)),
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response

# Usage
app = FastAPI()
app.add_middleware(RateLimitMiddleware, default_limit=100, default_window=60)

@app.on_event("startup")
async def set_custom_limits():
    # Tighter limits for sensitive endpoints
    app.middleware_stack.app.set_limit("/api/login", 5, 60)
    app.middleware_stack.app.set_limit("/api/register", 3, 300)
```

---

## Per-User/Per-IP/Per-API-Key Limits

### Different Keys for Different Clients

```python
class MultiKeyRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client

    def get_rate_limit_key(self, request: Request) -> tuple[str, int, int]:
        # Priority: API key > Authenticated user > IP address

        # 1. API Key
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return f"rate_limit:apikey:{api_key}", 1000, 60  # 1000/min

        # 2. Authenticated user
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"rate_limit:user:{user_id}", 500, 60  # 500/min

        # 3. IP address
        client_ip = request.client.host
        return f"rate_limit:ip:{client_ip}", 100, 60  # 100/min

    async def is_allowed(self, request: Request) -> tuple[bool, dict]:
        key, limit, window = self.get_rate_limit_key(request)
        now = time.time()
        window_start = now - window

        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)
        pipe.zadd(key, {f"{now}:{id(request)}": now})
        pipe.zcard(key)
        pipe.expire(key, window)
        results = await pipe.execute()

        count = results[2]
        remaining = max(0, limit - count)

        return count <= limit, {
            "limit": limit,
            "remaining": remaining,
            "reset": int(now + window),
            "retry_after": max(0, int(count + window - now)) if count > limit else 0,
        }
```

### Per-Endpoint Limits

```python
ENDPOINT_LIMITS = {
    "/api/login": (5, 60),          # 5 requests per minute
    "/api/register": (3, 300),      # 3 requests per 5 minutes
    "/api/password-reset": (3, 300), # 3 requests per 5 minutes
    "/api/search": (30, 60),        # 30 requests per minute
    "/api/upload": (10, 3600),      # 10 requests per hour
}

DEFAULT_LIMIT = (100, 60)  # 100 requests per minute

class EndpointRateLimiter(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        limit, window = ENDPOINT_LIMITS.get(
            request.url.path, DEFAULT_LIMIT
        )
        key = f"rate_limit:{request.client.host}:{request.url.path}"
        # ... rate limiting logic
```

---

## 429 Responses

### Proper 429 Response Format

```python
from fastapi.responses import JSONResponse

@app.exception_handler(429)
async def rate_limit_handler(request: Request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limit_exceeded",
            "message": "Too many requests. Please retry later.",
            "retry_after": exc.headers.get("Retry-After", 60),
        },
        headers={
            "Retry-After": exc.headers.get("Retry-After", "60"),
            "X-RateLimit-Limit": exc.headers.get("X-RateLimit-Limit", "100"),
            "X-RateLimit-Remaining": "0",
        },
    )
```

### Client-Side Handling

```python
import httpx
import asyncio

async def make_request_with_retry(url: str, max_retries: int = 3):
    async with httpx.AsyncClient() as client:
        for attempt in range(max_retries):
            response = await client.get(url)

            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 1))
                await asyncio.sleep(retry_after)
                continue

            return response

    raise Exception("Max retries exceeded")
```

---

## Best Practices

### 1. Use Multiple Rate Limit Layers

```python
# Layer 1: IP-based (global protection)
# Layer 2: User-based (per-user fairness)
# Layer 3: Endpoint-based (protect expensive operations)
```

### 2. Always Return Rate Limit Headers

```python
response.headers["X-RateLimit-Limit"] = "100"
response.headers["X-RateLimit-Remaining"] = "99"
response.headers["X-RateLimit-Reset"] = "1609459200"
```

### 3. Use Redis for Production

```python
# In-memory for development
# Redis for production (shared across workers/instances)
```

### 4. Implement Graceful Degradation

```python
# Don't just reject - provide useful information
{
    "error": "rate_limit_exceeded",
    "message": "You've exceeded the rate limit of 100 requests per minute.",
    "retry_after": 30,
    "docs": "https://api.example.com/docs/rate-limits"
}
```

### 5. Consider Different Limits for Different Tiers

```python
TIER_LIMITS = {
    "free": (100, 60),
    "pro": (1000, 60),
    "enterprise": (10000, 60),
}
```

### 6. Monitor Rate Limiting

```python
# Log rate limit hits
logger.warning(
    "Rate limit exceeded",
    extra={
        "client_ip": request.client.host,
        "path": request.url.path,
        "limit": limit,
        "window": window,
    }
)
```

### 7. Use Lua Scripts for Atomicity

```python
# Redis operations should be atomic to prevent race conditions
# Use Lua scripts for complex rate limiting logic
```

---

## Interview Questions

### Q1: What is rate limiting and why is it important?
**Answer:** Rate limiting restricts how many requests a client can make in a given time window. It prevents abuse, ensures fair resource usage, maintains service stability, and protects against DDoS attacks.

### Q2: What are the main rate limiting algorithms?
**Answer:** Fixed window (simple, burst-prone), sliding window log (precise, memory-heavy), sliding window counter (balanced), token bucket (handles bursts), and leaky bucket (smooths traffic).

### Q3: What's the difference between fixed window and sliding window?
**Answer:** Fixed window counts requests in fixed time intervals (e.g., 1:00-2:00), which can allow bursts at window boundaries. Sliding window continuously moves and provides smoother rate limiting.

### Q4: How does the token bucket algorithm work?
**Answer:** A bucket holds tokens up to a maximum. Each request consumes one token. Tokens refill at a constant rate. If no tokens remain, the request is rejected. It allows controlled bursts while maintaining average rate.

### Q5: Why use Redis for rate limiting?
**Answer:** Redis provides shared state across multiple server instances, atomic operations, built-in expiration, and high performance. In-memory rate limiting doesn't work in distributed systems.

### Q6: What headers should rate-limited responses include?
**Answer:** `X-RateLimit-Limit` (total allowed), `X-RateLimit-Remaining` (requests left), `X-RateLimit-Reset` (window reset time), and `Retry-After` (seconds to wait) on 429 responses.

### Q7: How do you handle rate limiting for authenticated vs unauthenticated users?
**Answer:** Use different keys based on authentication status. Authenticated users get limits by user ID, unauthenticated by IP. Different tiers (free/pro/enterprise) can have different limits.

### Q8: What is a 429 status code?
**Answer:** HTTP 429 "Too Many Requests" indicates the client has exceeded the rate limit. The response should include a `Retry-After` header telling the client when to retry.

### Q9: How do you prevent race conditions in rate limiting?
**Answer:** Use atomic Redis operations (Lua scripts, pipelines) to ensure the check-and-increment operation is atomic. Without atomicity, multiple concurrent requests could all pass the check.

### Q10: What's the difference between rate limiting and throttling?
**Answer:** Rate limiting rejects requests that exceed the limit (returns 429). Throttling slows down requests that exceed the limit (queues or delays them). Rate limiting is more common for APIs.

### Q11: How do you handle rate limiting in a microservices architecture?
**Answer:** Use a centralized rate limiter (Redis) accessible by all services, or implement rate limiting at the API gateway level. Each service can also have its own rate limiting for internal protection.

### Q12: How do you test rate limiting?
**Answer:** Send requests in rapid succession and verify that the correct number get through. Check response headers, verify 429 status after limit, test Retry-After header, and verify different limits for different endpoints.

### Q13: What is a sliding window counter?
**Answer:** A hybrid approach that approximates the sliding window using fixed windows. It counts requests in the current and previous windows, applying a weight based on how much of the previous window has elapsed.

### Q14: How do you implement rate limiting per API key?
**Answer:** Use the API key as part of the rate limit key (e.g., `rate_limit:{api_key}`). Each API key gets its own counter. Provide different limits based on the key's subscription tier.

### Q15: What happens when Redis is down during rate limiting?
**Answer:** Implement a fallback strategy: either allow all requests (fail open) or block all requests (fail closed). Most APIs fail open to maintain availability, accepting the risk of rate limit bypass.

### Q16: How do you handle rate limiting for different HTTP methods?
**Answer:** Include the method in the rate limit key or apply different limits per method. For example, POST requests might have lower limits than GET requests.

### Q17: What is a burst in rate limiting?
**Answer:** A burst is a sudden spike of requests in a short period. Token bucket allows controlled bursts by storing tokens. Fixed window can unintentionally allow bursts at window boundaries.

### Q18: How do you communicate rate limits to API consumers?
**Answer:** Include rate limit headers in every response, document rate limits in API docs, provide a rate limit endpoint, and send notifications when approaching limits.

### Q19: Should rate limiting be applied to health check endpoints?
**Answer:** Generally no. Health checks should be exempt from rate limiting as they're used by load balancers and monitoring systems that need frequent access.

### Q20: How do you handle rate limiting for WebSocket connections?
**Answer:** Rate limit WebSocket messages separately from HTTP connections. Limit the number of messages per second, the number of connections per IP, and the total concurrent connections.

### Q21: What's the memory impact of rate limiting with Redis?
**Answer:** Each rate limit key uses memory for the sorted set entries. With millions of users, this can grow significantly. Use TTL on keys and consider approximate algorithms like sliding window counter.

### Q22: How do you implement global rate limiting?
**Answer:** Use a single Redis key for all clients (e.g., `rate_limit:global`) to limit total API throughput. This protects the backend from overload regardless of individual client usage.

### Q23: What's the difference between local and distributed rate limiting?
**Answer:** Local rate limiting uses in-process state (per server instance). Distributed rate limiting uses shared state (Redis). Distributed is needed for multi-instance deployments.

### Q24: How do you handle rate limiting during deployment/scaling?
**Answer:** Use Redis for persistent rate limit state that survives deployments. Implement graceful shutdown to avoid losing in-flight requests. Consider warm-up periods after deployment.

### Q25: What are common anti-patterns in rate limiting?
**Answer:** Using in-memory counters in distributed systems, not returning rate limit headers, not handling 429 on the client side, applying the same limit to all endpoints, and using rate limiting as the only security measure.
