# uvloop and Performance for FastAPI

## Table of Contents

1. [What is uvloop](#what-is-uvloop)
2. [Installing uvloop](#installing-uvloop)
3. [Benchmark Comparison](#benchmark-comparison)
4. [When to Use uvloop](#when-to-use-uvloop)
5. [FastAPI with uvloop](#fastapi-with-uvloop)
6. [Gunicorn + Uvicorn Workers](#gunicorn--uvicorn-workers)
7. [Worker Count Calculation](#worker-count-calculation)
8. [Async Performance Patterns](#async-performance-patterns)
9. [Connection Pool Sizing](#connection-pool-sizing)
10. [Interview Questions](#interview-questions)

---

## What is uvloop

uvloop is a fast, drop-in replacement for the built-in `asyncio` event loop.
It's built on top of `libuv` (the same library Node.js uses) and provides
significantly better performance.

### How uvloop Works

```python
# Built-in asyncio event loop
import asyncio

async def main():
    # Uses Python's default event loop (selector-based)
    await asyncio.sleep(1)

asyncio.run(main())

# uvloop event loop
import uvloop

async def main():
    # Uses libuv-based event loop (much faster)
    await asyncio.sleep(1)

uvloop.install()
asyncio.run(main())
```

### Why uvloop is Faster

```
┌─────────────────────────────────────────────────────┐
│                Built-in asyncio                      │
│  ┌──────────────┐  ┌──────────────┐                │
│  │  Python I/O   │  │  Selector    │                │
│  │  Multiplexer  │  │  (epoll/     │                │
│  │              │  │   kqueue)    │                │
│  └──────────────┘  └──────────────┘                │
│         Pure Python, slower                          │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                    uvloop                            │
│  ┌──────────────┐  ┌──────────────┐                │
│  │   libuv      │  │  Optimized   │                │
│  │   Event      │  │  I/O         │                │
│  │   Loop       │  │  Multiplexer │                │
│  └──────────────┘  └──────────────┘                │
│     C-based, much faster                             │
└─────────────────────────────────────────────────────┘

Performance improvements:
- 2-4x faster than built-in asyncio
- Lower latency for I/O operations
- Better memory efficiency
- Optimized for high-concurrency workloads
```

### Key Differences

```python
# Built-in asyncio
import asyncio

# Uses selector module (epoll on Linux, kqueue on macOS)
loop = asyncio.new_event_loop()
print(type(loop))  # <class '_UnixSelectorEventLoop'>

# uvloop
import uvloop

# Uses libuv (cross-platform, optimized)
loop = uvloop.new_event_loop()
print(type(loop))  # <class 'uvloop.Loop'>

# Feature comparison:
# - Both support: coroutines, tasks, futures, subprocesses
# - uvloop adds: better performance, lower latency
# - uvloop adds: process watchers, signal handlers
# - uvloop adds: optimized timer implementation
```

---

## Installing uvloop

### Installation

```bash
# Basic installation
pip install uvloop

# With FastAPI (uvloop is often installed automatically)
pip install fastapi uvicorn[standard]

# Check if uvloop is installed
python -c "import uvloop; print(uvloop.__version__)"

# Platform support
# - Linux: Full support (best performance)
# - macOS: Full support
# - Windows: Not supported (use ProactorEventLoop instead)
```

### Platform Considerations

```python
import sys
import platform

# Check platform compatibility
def check_uvloop_support():
    if sys.platform == "win32":
        print("uvloop not supported on Windows")
        print("Use ProactorEventLoop instead")
        return False
    elif sys.platform == "linux":
        print("uvloop fully supported on Linux")
        print("Best performance on Linux")
        return True
    elif sys.platform == "darwin":
        print("uvloop supported on macOS")
        print("Good performance on macOS")
        return True
    return False

# Conditional uvloop usage
def setup_event_loop():
    if sys.platform != "win32":
        import uvloop
        uvloop.install()
    # On Windows, asyncio.run() uses ProactorEventLoop by default
```

---

## Benchmark Comparison

### uvloop vs asyncio Benchmarks

```python
import asyncio
import time
import uvloop

# Benchmark: High-concurrency I/O operations
async def io_bound_task(n: int) -> int:
    """Simulate I/O-bound operation."""
    await asyncio.sleep(0.01)
    return n

async def benchmark_asyncio(num_tasks: int = 10000):
    """Benchmark built-in asyncio."""
    start = time.perf_counter()
    tasks = [io_bound_task(i) for i in range(num_tasks)]
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start
    return elapsed

async def benchmark_uvloop(num_tasks: int = 10000):
    """Benchmark uvloop."""
    start = time.perf_counter()
    tasks = [io_bound_task(i) for i in range(num_tasks)]
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start
    return elapsed

# Run benchmarks
async def main():
    num_tasks = 10000

    # asyncio benchmark
    asyncio_time = await benchmark_asyncio(num_tasks)
    print(f"asyncio: {asyncio_time:.3f}s for {num_tasks} tasks")

    # uvloop benchmark
    uvloop.install()
    uvloop_time = await benchmark_uvloop(num_tasks)
    print(f"uvloop: {uvloop_time:.3f}s for {num_tasks} tasks")

    improvement = asyncio_time / uvloop_time
    print(f"uvloop is {improvement:.1f}x faster")

# Typical results:
# asyncio: 1.050s for 10000 tasks
# uvloop: 0.350s for 10000 tasks
# uvloop is 3.0x faster
```

### Real-World HTTP Benchmark

```bash
# Using wrk to benchmark FastAPI with and without uvloop

# Without uvloop
uvicorn main:app --host 0.0.0.0 --port 8000
wrk -t12 -c400 -d30s http://localhost:8000/

# Results:
# Requests/sec: 15000
# Latency: 25ms avg

# With uvloop
uvicorn main:app --host 0.0.0.0 --port 8000 --loop uvloop
wrk -t12 -c400 -d30s http://localhost:8000/

# Results:
# Requests/sec: 45000
# Latency: 8ms avg
# 3x improvement!
```

### Memory Usage Comparison

```python
import asyncio
import uvloop
import tracemalloc

async def memory_benchmark():
    tracemalloc.start()

    # Create many tasks
    tasks = [asyncio.sleep(0.01) for _ in range(10000)]
    await asyncio.gather(*tasks)

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")

# uvloop typically uses less memory for the same workload
```

---

## When to Use uvloop

### Use uvloop When

```python
# 1. Production FastAPI servers
# uvloop is the recommended event loop for production

# 2. High-concurrency applications
# WebSocket servers, chat applications, real-time systems

# 3. I/O-heavy workloads
# API gateways, proxy servers, load balancers

# 4. Microservices with many connections
# Database connections, Redis connections, message queues

# Example: Production FastAPI app
import uvloop
import asyncio

uvloop.install()

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### Don't Use uvloop When

```python
# 1. Windows development
# uvloop doesn't support Windows

# 2. Debugging complex async issues
# Built-in asyncio has better debugging tools
# asyncio.run(main(), debug=True)

# 3. When using incompatible libraries
# Some libraries may not work with uvloop

# 4. Development environment
# May hide performance issues that appear in production

# Conditional usage
import sys

if sys.platform != "win32":
    import uvloop
    uvloop.install()
```

---

## FastAPI with uvloop

### Configuration

```python
# Method 1: Command line
# uvicorn main:app --loop uvloop

# Method 2: In code
import uvloop
import asyncio

# Install uvloop as default event loop
uvloop.install()

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Running on uvloop"}

# Method 3: Environment variable
# UVLOOP_LOOP=1 uvicorn main:app

# Method 4: uvicorn config
# uvicorn_config.py
import uvloop

def setup():
    uvloop.install()
```

### FastAPI + Uvicorn + uvloop

```python
# main.py
import uvloop
import asyncio

# Install uvloop before importing FastAPI
uvloop.install()

from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up with uvloop...")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "FastAPI with uvloop"}

@app.get("/health")
async def health():
    loop = asyncio.get_running_loop()
    return {
        "event_loop": type(loop).__name__,
        "status": "healthy"
    }
```

### Running with uvloop

```bash
# Development
uvicorn main:app --reload --loop uvloop

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --loop uvloop --workers 4

# Or using Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --loop uvloop

# Or using Docker
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--loop", "uvloop", "--workers", "4"]
```

---

## Gunicorn + Uvicorn Workers

### Why Gunicorn + Uvicorn

```python
# Uvicorn alone:
# - Single process
# - Single event loop
# - Limited CPU utilization

# Gunicorn + Uvicorn:
# - Multiple worker processes
# - Each worker runs its own Uvicorn
# - Better CPU utilization
# - Process management (restart crashed workers)
# - Graceful shutdown

# Architecture:
# ┌─────────────────────────────────────────┐
# │              Gunicorn Master             │
# │  ┌─────────┐ ┌─────────┐ ┌─────────┐  │
# │  │Worker 1 │ │Worker 2 │ │Worker 3 │  │
# │  │Uvicorn  │ │Uvicorn  │ │Uvicorn  │  │
# │  │Event    │ │Event    │ │Event    │  │
# │  │Loop     │ │Loop     │ │Loop     │  │
# │  └─────────┘ └─────────┘ └─────────┘  │
# └─────────────────────────────────────────┘
```

### Configuration

```python
# gunicorn_config.py
import multiprocessing

# Worker configuration
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000

# Bind
bind = "0.0.0.0:8000"

# Timeout
timeout = 120
graceful_timeout = 30
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "fastapi_app"

# Server mechanics
preload_app = True  # Load app before forking workers
max_requests = 1000  # Restart workers after N requests
max_requests_jitter = 50  # Random jitter to prevent thundering herd
```

### Running Gunicorn

```bash
# Basic
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# With config file
gunicorn main:app -c gunicorn_config.py

# With uvloop (requires uvloop installation)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --loop uvloop

# Production command
gunicorn main:app \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    --loop uvloop \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
```

---

## Worker Count Calculation

### CPU-Bound vs I/O-Bound

```python
import multiprocessing
import os

# Rule of thumb for worker count

# I/O-bound applications (most FastAPI apps):
# workers = (2 * CPU_CORES) + 1
# This accounts for context switching overhead

# CPU-bound applications:
# workers = CPU_CORES + 1
# More workers than cores cause context switching overhead

# Calculate workers
def calculate_workers(app_type: str = "io_bound") -> int:
    cpu_cores = multiprocessing.cpu_count()

    if app_type == "io_bound":
        # For I/O-bound (API servers, web apps)
        workers = (2 * cpu_cores) + 1
    elif app_type == "cpu_bound":
        # For CPU-bound (data processing, ML inference)
        workers = cpu_cores + 1
    else:
        # Conservative default
        workers = cpu_cores

    return min(workers, 16)  # Cap at 16 for most cases

# Example on different machines:
# 4-core machine (I/O-bound): (2*4)+1 = 9 workers
# 8-core machine (I/O-bound): (2*8)+1 = 17 workers -> cap at 16
# 4-core machine (CPU-bound): 4+1 = 5 workers
# 8-core machine (CPU-bound): 8+1 = 9 workers
```

### Memory Considerations

```python
import psutil

def calculate_workers_with_memory(app_memory_mb: int = 200) -> int:
    """Calculate workers based on available memory."""
    # Get available memory
    mem = psutil.virtual_memory()
    available_mb = mem.available / (1024 * 1024)

    # Reserve 20% for system
    usable_mb = available_mb * 0.8

    # Calculate max workers based on memory
    max_by_memory = int(usable_mb / app_memory_mb)

    # Calculate max workers based on CPU
    cpu_cores = multiprocessing.cpu_count()
    max_by_cpu = (2 * cpu_cores) + 1

    # Use the lower of the two
    workers = min(max_by_memory, max_by_cpu)

    return max(1, min(workers, 16))

# Example:
# 8GB RAM, 200MB per worker: 8192 * 0.8 / 200 = ~32 workers
# But 4-core CPU: max 9 workers
# Result: 9 workers

# 4GB RAM, 200MB per worker: 4096 * 0.8 / 200 = ~16 workers
# But 2-core CPU: max 5 workers
# Result: 5 workers
```

### Environment-Based Configuration

```python
import os
import multiprocessing

def get_worker_count() -> int:
    """Get worker count from environment or auto-calculate."""
    # Check environment variable first
    env_workers = os.environ.get("WEB_CONCURRENCY")
    if env_workers:
        return int(env_workers)

    # Auto-calculate based on environment
    environment = os.environ.get("ENVIRONMENT", "development")

    if environment == "development":
        return 1  # Single worker for development
    elif environment == "staging":
        return 2  # Fewer workers for staging
    elif environment == "production":
        cpu_cores = multiprocessing.cpu_count()
        return (2 * cpu_cores) + 1
    else:
        return multiprocessing.cpu_count()

# Docker compose example
# docker-compose.yml:
# services:
#   web:
#     environment:
#       - WEB_CONCURRENCY=4
#       - ENVIRONMENT=production
```

---

## Async Performance Patterns

### Connection Pooling

```python
import asyncio
from typing import AsyncGenerator

class ConnectionPool:
    """Efficient connection pool for async operations."""

    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.semaphore = asyncio.Semaphore(max_connections)
        self.connections: list = []

    async def get_connection(self) -> AsyncGenerator:
        async with self.semaphore:
            conn = await self._create_connection()
            try:
                yield conn
            finally:
                await self._release_connection(conn)

    async def _create_connection(self):
        # Create new connection
        return {"id": len(self.connections)}

    async def _release_connection(self, conn):
        # Release connection back to pool
        pass

# Usage
pool = ConnectionPool(max_connections=20)

async def query_database(query: str):
    async with pool.get_connection() as conn:
        # Use connection
        await asyncio.sleep(0.1)
        return f"Result from {conn['id']}"
```

### Batch Processing

```python
import asyncio
from typing import TypeVar, Sequence

T = TypeVar("T")

async def process_batch(
    items: Sequence[T],
    batch_size: int = 100,
    process_func: callable = None,
) -> list:
    """Process items in batches to avoid overwhelming resources."""
    results = []

    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_tasks = [process_func(item) for item in batch]
        batch_results = await asyncio.gather(*batch_tasks)
        results.extend(batch_results)

        # Optional: small delay between batches
        if i + batch_size < len(items):
            await asyncio.sleep(0.01)

    return results

# Usage
async def process_user(user_id: int) -> dict:
    await asyncio.sleep(0.01)  # Simulate work
    return {"user_id": user_id, "processed": True}

async def main():
    user_ids = list(range(1000))
    results = await process_batch(
        user_ids,
        batch_size=100,
        process_func=process_user,
    )
    print(f"Processed {len(results)} users")
```

### Caching with TTL

```python
import asyncio
import time
from typing import Any, Optional

class AsyncCache:
    """Simple async cache with TTL."""

    def __init__(self, default_ttl: int = 300):
        self.cache: dict[str, tuple[Any, float]] = {}
        self.default_ttl = default_ttl

    async def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                return value
            else:
                del self.cache[key]
        return None

    async def set(self, key: str, value: Any, ttl: int = None):
        ttl = ttl or self.default_ttl
        self.cache[key] = (value, time.time() + ttl)

    async def get_or_set(
        self, key: str, factory: callable, ttl: int = None
    ) -> Any:
        value = await self.get(key)
        if value is None:
            value = await factory()
            await self.set(key, value, ttl)
        return value

# Usage
cache = AsyncCache(default_ttl=60)

async def get_user_from_db(user_id: int) -> dict:
    # Simulate database query
    await asyncio.sleep(0.1)
    return {"id": user_id, "name": f"User {user_id}"}

async def get_user(user_id: int) -> dict:
    return await cache.get_or_set(
        f"user:{user_id}",
        lambda: get_user_from_db(user_id),
        ttl=300,
    )
```

### Rate Limiting

```python
import asyncio
import time
from collections import defaultdict

class AsyncRateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)

    async def acquire(self, key: str) -> bool:
        now = time.time()

        # Clean old requests
        self.requests[key] = [
            t for t in self.requests[key]
            if now - t < self.window_seconds
        ]

        if len(self.requests[key]) >= self.max_requests:
            return False

        self.requests[key].append(now)
        return True

# Usage
rate_limiter = AsyncRateLimiter(max_requests=100, window_seconds=60)

async def handle_request(request_id: int):
    if await rate_limiter.acquire("api"):
        # Process request
        return {"status": "ok", "request_id": request_id}
    else:
        return {"status": "rate_limited", "request_id": request_id}
```

---

## Connection Pool Sizing

### Database Connection Pool

```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Calculate optimal pool size
def calculate_pool_size(
    cpu_cores: int = 4,
    max_connections: int = 100,
    avg_query_time_ms: float = 10,
    target_utilization: float = 0.8,
) -> int:
    """
    Calculate optimal database connection pool size.

    Formula: connections = (cores * 2) + effective_spindle_count
    For SSD: connections = (cores * 2) + 1
    """
    # For SSD-based databases
    base_connections = (cpu_cores * 2) + 1

    # Adjust for query time
    # If queries are fast, fewer connections needed
    if avg_query_time_ms < 10:
        pool_size = base_connections
    elif avg_query_time_ms < 100:
        pool_size = base_connections * 2
    else:
        pool_size = base_connections * 3

    # Cap at max connections
    pool_size = min(pool_size, max_connections)

    # Apply utilization target
    pool_size = int(pool_size * target_utilization)

    return max(1, pool_size)

# Example configurations
print(calculate_pool_size(cpu_cores=4))  # 9
print(calculate_pool_size(cpu_cores=8))  # 17
print(calculate_pool_size(cpu_cores=4, avg_query_time_ms=50))  # 18
```

### Redis Connection Pool

```python
import redis.asyncio as redis

# Calculate Redis connection pool size
def calculate_redis_pool_size(
    max_connections: int = 100,
    concurrent_clients: int = 50,
) -> int:
    """
    Redis connection pool sizing.

    Redis is single-threaded, so too many connections
    can actually hurt performance.
    """
    # Rule of thumb: 2x the number of concurrent clients
    # but capped at a reasonable maximum
    pool_size = min(concurrent_clients * 2, max_connections)

    # For most applications, 10-20 connections is sufficient
    return min(pool_size, 20)

# Create Redis pool
redis_pool = redis.ConnectionPool(
    host="localhost",
    port=6379,
    db=0,
    max_connections=calculate_redis_pool_size(),
    decode_responses=True,
)

async def get_redis():
    return redis.Redis(connection_pool=redis_pool)
```

### HTTP Connection Pool

```python
import aiohttp
import asyncio

# Calculate HTTP connection pool size
def calculate_http_pool_size(
    target_services: int = 5,
    requests_per_service: int = 10,
) -> dict:
    """Calculate HTTP connection pool configuration."""
    total_connections = target_services * requests_per_service

    return {
        "limit": total_connections,  # Total connection limit
        "limit_per_host": requests_per_service,  # Per-host limit
        "ttl_dns_cache": 300,  # DNS cache TTL
        "enable_cleanup_closed": True,  # Cleanup closed connections
        "keepalive_timeout": 30,  # Keep-alive timeout
    }

# Create HTTP session with optimized pool
async def create_http_session():
    pool_config = calculate_http_pool_size()

    connector = aiohttp.TCPConnector(
        limit=pool_config["limit"],
        limit_per_host=pool_config["limit_per_host"],
        ttl_dns_cache=pool_config["ttl_dns_cache"],
        enable_cleanup_closed=pool_config["enable_cleanup_closed"],
        keepalive_timeout=pool_config["keepalive_timeout"],
    )

    timeout = aiohttp.ClientTimeout(total=30, connect=10)

    return aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
    )
```

### FastAPI Connection Pool Configuration

```python
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import redis.asyncio as redis

app = FastAPI()

# Database pool
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,  # Base pool size
    max_overflow=10,  # Additional connections when pool is full
    pool_timeout=30,  # Timeout waiting for connection
    pool_recycle=1800,  # Recycle connections after 30 minutes
    pool_pre_ping=True,  # Test connections before using
)

# Redis pool
redis_pool = redis.ConnectionPool(
    host="localhost",
    port=6379,
    db=0,
    max_connections=20,
)

# Session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@app.on_event("startup")
async def startup():
    # Warm up connection pools
    async with engine.connect() as conn:
        await conn.execute("SELECT 1")

@app.on_event("shutdown")
async def shutdown():
    # Close connection pools
    await engine.dispose()
    await redis_pool.disconnect()
```

---

## Interview Questions

### Q1: What is uvloop?

**Answer:** uvloop is a fast, drop-in replacement for Python's built-in asyncio event loop. It's built on libuv (the same library Node.js uses) and provides 2-4x better performance for I/O-bound operations. It's recommended for production FastAPI servers.

### Q2: When should you use uvloop?

**Answer:** Use uvloop for production FastAPI servers, high-concurrency applications, I/O-heavy workloads, and microservices. Don't use it on Windows (not supported), during debugging (limited debug tools), or when using incompatible libraries.

### Q3: How does Gunicorn + Uvicorn work?

**Answer:** Gunicorn is a process manager that spawns multiple worker processes. Each worker runs Uvicorn, which handles async I/O. This combines process-level parallelism (Gunicorn) with async concurrency (Uvicorn). Configuration uses `worker_class = "uvicorn.workers.UvicornWorker"`.

### Q4: How do you calculate worker count?

**Answer:** For I/O-bound apps: `(2 * CPU_CORES) + 1`. For CPU-bound apps: `CPU_CORES + 1`. Cap at 16 for most cases. Also consider available memory - each worker uses ~200MB. Use environment variables for different environments.

### Q5: What is the GIL and how does it affect FastAPI?

**Answer:** The Global Interpreter Lock (GIL) prevents multiple threads from executing Python code simultaneously. FastAPI uses async I/O, not threads, so the GIL doesn't affect async performance. For CPU-bound work, use multiprocessing (Gunicorn workers) to bypass the GIL.

### Q6: How do you optimize FastAPI performance?

**Answer:** Key optimizations: (1) Use uvloop, (2) Enable connection pooling, (3) Use async database drivers, (4) Implement caching, (5) Use proper worker count, (6) Enable HTTP keep-alive, (7) Use response streaming for large payloads, (8) Profile and optimize slow endpoints.

### Q7: What is connection pool sizing?

**Answer:** Connection pool sizing balances between having enough connections for concurrent requests and not overwhelming the database. Rule of thumb: `(CPU_CORES * 2) + 1` for SSD databases. Adjust based on query time, concurrent clients, and database limits.

### Q8: When should you NOT use uvloop?

**Answer:** Don't use uvloop on Windows (not supported), when debugging complex async issues (built-in asyncio has better tools), when libraries are incompatible, or in development environments where you want consistent behavior across platforms.

### Q9: What is the difference between uvloop and built-in asyncio?

**Answer:** Both implement the asyncio event loop interface. uvloop is built on libuv (C library) while asyncio uses Python's selector module. uvloop is 2-4x faster, uses less memory, and has lower latency. They're API-compatible, so switching is usually a one-line change.

### Q10: How do you handle graceful shutdown in FastAPI?

**Answer:** Use the `lifespan` context manager or `on_event` decorators. In the shutdown handler, close database connections, flush caches, and wait for background tasks. Gunicorn handles graceful shutdown with `--timeout` and `--graceful-timeout` options.

### Q11: What is the difference between `pool_size` and `max_overflow`?

**Answer:** `pool_size` is the base number of connections maintained in the pool. `max_overflow` is the number of additional connections allowed when the pool is exhausted. Total max connections = `pool_size + max_overflow`. Overflow connections are closed when returned to the pool.

### Q12: How does async affect database performance?

**Answer:** Async allows the event loop to handle other requests while waiting for database responses. With proper connection pooling, this significantly increases throughput. Use async drivers (asyncpg, aiomysql) and avoid blocking database operations in async code.

### Q13: What is `pool_pre_ping`?

**Answer:** `pool_pre_ping` tests database connections before using them. It sends a simple query (like `SELECT 1`) to verify the connection is alive. This prevents errors from stale connections but adds slight overhead. Recommended for production environments.

### Q14: How do you monitor FastAPI performance?

**Answer:** Key metrics: (1) Request latency (p50, p95, p99), (2) Requests per second, (3) Error rates, (4) Connection pool usage, (5) Memory usage, (6) CPU usage. Tools: Prometheus + Grafana, DataDog, New Relic, or built-in `prometheus_fastapi_instrumentator`.

### Q15: What is the difference between `worker_connections` and `worker_count`?

**Answer:** `worker_count` is the number of worker processes. `worker_connections` is the maximum number of simultaneous connections each worker can handle. Total max connections = `worker_count * worker_connections`. For async workers, `worker_connections` is typically high (1000+).
