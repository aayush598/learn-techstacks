# Async Optimization

## Table of Contents

1. [Introduction](#1-introduction)
2. [Concurrent I/O with asyncio.gather](#2-gather)
3. [TaskGroup for Structured Concurrency](#3-taskgroup)
4. [Semaphore for Limiting Concurrency](#4-semaphore)
5. [Async Database Queries](#5-async-db)
6. [Async HTTP Calls](#6-async-http)
7. [Parallel Processing Patterns](#7-parallel)
8. [Async Context Managers](#8-async-context)
9. [Performance Anti-Patterns](#9-anti-patterns)
10. [Best Practices](#10-best-practices)

---

## 1. Introduction <a name="1-introduction"></a`

FastAPI's async support enables handling thousands of concurrent requests efficiently.
Understanding async patterns is crucial for building high-performance APIs.

### Sync vs Async Performance

```
Sync (100 requests, 100ms each):
Total time: 100 × 100ms = 10,000ms (10 seconds)

Async (100 requests, 100ms each):
Total time: ~100ms (all run concurrently)
```

### When to Use Async

| Use Case | Async Benefit |
|----------|--------------|
| HTTP requests to external APIs | High (I/O bound) |
| Database queries | High (I/O bound) |
| File operations | Medium (I/O bound) |
| CPU-intensive computation | Low (need multiprocessing) |
| Simple computations | Low (overhead not worth it) |

---

## 2. Concurrent I/O with asyncio.gather <a name="2-gather"></a>

### Basic gather

```python
import asyncio
import httpx

async def fetch_url(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def fetch_multiple_urls(urls: list[str]) -> list[dict]:
    """Fetch multiple URLs concurrently."""
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

# Usage
urls = [
    "https://api.example.com/users",
    "https://api.example.com/products",
    "https://api.example.com/orders",
]
results = await fetch_multiple_urls(urls)
```

### gather with Error Handling

```python
async def fetch_with_error_handling(url: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return {"url": url, "data": response.json(), "error": None}
    except Exception as e:
        return {"url": url, "data": None, "error": str(e)}

async def fetch_all_safe(urls: list[str]) -> list[dict]:
    """Fetch all URLs, handling errors individually."""
    tasks = [fetch_with_error_handling(url) for url in urls]
    return await asyncio.gather(*tasks)

# Usage
results = await fetch_all_safe(urls)
for result in results:
    if result["error"]:
        print(f"Failed to fetch {result['url']}: {result['error']}")
```

### gather with return_exceptions

```python
async def fetch_all_with_exceptions(urls: list[str]) -> list:
    """Fetch all URLs, exceptions returned as results."""
    tasks = [fetch_url(url) for url in urls]
    # return_exceptions=True means exceptions are returned as values
    results = await asyncio.gather(*tasks, return_exceptions=True)

    successful = []
    failed = []
    for result in results:
        if isinstance(result, Exception):
            failed.append(result)
        else:
            successful.append(result)

    return successful, failed

# Usage
successful, failed = await fetch_all_with_exceptions(urls)
print(f"Fetched {len(successful)} URLs successfully")
print(f"Failed to fetch {len(failed)} URLs")
```

---

## 3. TaskGroup for Structured Concurrency <a name="3-taskgroup"></a>

### Basic TaskGroup (Python 3.11+)

```python
import asyncio

async def fetch_user_data(user_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        return response.json()

async def fetch_all_users(user_ids: list[int]) -> list[dict]:
    """Fetch all users with structured concurrency."""
    results = []
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(fetch_user_data(user_id))
            for user_id in user_ids
        ]

    # All tasks completed successfully
    return [task.result() for task in tasks]

# Usage
user_ids = [1, 2, 3, 4, 5]
users = await fetch_all_users(user_ids)
```

### TaskGroup with Error Handling

```python
async def fetch_user_safe(user_id: int) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.example.com/users/{user_id}")
            response.raise_for_status()
            return {"id": user_id, "data": response.json()}
    except Exception as e:
        return {"id": user_id, "error": str(e)}

async def fetch_users_structured(user_ids: list[int]) -> list[dict]:
    """TaskGroup automatically cancels all tasks on error."""
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(fetch_user_safe(user_id))
            for user_id in user_ids
        ]
    return [task.result() for task in tasks]

# If any task raises an exception, all other tasks are cancelled
```

### TaskGroup vs gather

```python
# gather: Errors don't cancel other tasks (with return_exceptions=False, raises first)
# TaskGroup: All tasks are cancelled if any task fails

# gather example
async def gather_example():
    tasks = [
        task1(),  # Fails
        task2(),  # Continues
        task3(),  # Continues
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    # task2 and task3 complete even if task1 fails

# TaskGroup example
async def taskgroup_example():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(task1())  # Fails
        tg.create_task(task2())  # Cancelled
        tg.create_task(task3())  # Cancelled
    # ExceptionGroup is raised if any task fails
```

---

## 4. Semaphore for Limiting Concurrency <a name="4-semaphore"></a>

### Basic Semaphore

```python
import asyncio

async def fetch_with_limit(urls: list[str], max_concurrent: int = 10):
    """Limit concurrent requests."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def limited_fetch(url: str):
        async with semaphore:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response.json()

    tasks = [limited_fetch(url) for url in urls]
    return await asyncio.gather(*tasks)

# Only 10 requests run at a time
results = await fetch_with_limit(urls, max_concurrent=10)
```

### Semaphore with Timeout

```python
async def fetch_with_timeout_and_limit(
    urls: list[str],
    max_concurrent: int = 10,
    timeout: float = 30.0,
):
    """Limit concurrency with overall timeout."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def limited_fetch(url: str):
        async with semaphore:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=timeout)
                return response.json()

    tasks = [limited_fetch(url) for url in urls]
    return await asyncio.gather(*tasks, return_exceptions=True)

# Usage
results = await fetch_with_timeout_and_limit(
    urls,
    max_concurrent=20,
    timeout=60.0,
)
```

### FastAPI Endpoint with Semaphore

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

# Global semaphore
semaphore = asyncio.Semaphore(20)

@app.get("/proxy/{path:path}")
async def proxy_endpoint(path: str):
    """Proxy endpoint with rate limiting."""
    async with semaphore:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.example.com/{path}")
            return response.json()

@app.post("/batch-process")
async def batch_process(items: list[dict], background_tasks: BackgroundTasks):
    """Process items in batches."""
    async def process_item(item):
        async with semaphore:
            # Simulate processing
            await asyncio.sleep(0.1)
            return {"processed": True, "item": item}

    tasks = [process_item(item) for item in items]
    results = await asyncio.gather(*tasks)
    return {"results": results}
```

---

## 5. Async Database Queries <a name="5-async-db"></a>

### SQLAlchemy Async

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Create async engine
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,
    max_overflow=10,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Async queries
@app.get("/users/")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@app.post("/users/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
```

### Concurrent Database Queries

```python
async def get_dashboard_data(user_id: int, db: AsyncSession):
    """Fetch dashboard data with concurrent queries."""
    # Run multiple queries concurrently
    user_task = db.execute(select(User).filter(User.id == user_id))
    orders_task = db.execute(
        select(Order).filter(Order.user_id == user_id).limit(10)
    )
    items_task = db.execute(
        select(Item).filter(Item.owner_id == user_id).limit(20)
    )

    # Gather all results
    user_result, orders_result, items_result = await asyncio.gather(
        user_task, orders_task, items_task
    )

    return {
        "user": user_result.scalar_one(),
        "orders": orders_result.scalars().all(),
        "items": items_result.scalars().all(),
    }
```

---

## 6. Async HTTP Calls <a name="6-async-http"></a`

### httpx AsyncClient

```python
import httpx
from typing import Optional

class APIClient:
    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = timeout
        self.client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(self.timeout),
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20,
            ),
        )
        return self

    async def __aexit__(self, *args):
        if self.client:
            await self.client.aclose()

    async def get(self, path: str, **kwargs) -> dict:
        response = await self.client.get(path, **kwargs)
        response.raise_for_status()
        return response.json()

    async def post(self, path: str, **kwargs) -> dict:
        response = await self.client.post(path, **kwargs)
        response.raise_for_status()
        return response.json()

# Usage
async def fetch_user_data():
    async with APIClient("https://api.example.com") as api:
        user = await api.get("/users/1")
        orders = await api.get(f"/users/{user['id']}/orders")
        return {"user": user, "orders": orders}
```

### Concurrent HTTP Calls

```python
async def fetch_multiple_resources():
    """Fetch multiple resources concurrently."""
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/products",
        "https://api.example.com/orders",
        "https://api.example.com/categories",
    ]

    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    results = []
    for response in responses:
        if isinstance(response, Exception):
            results.append({"error": str(response)})
        else:
            results.append(response.json())

    return results
```

---

## 7. Parallel Processing Patterns <a name="7-parallel"></a>

### CPU-Bound with ProcessPoolExecutor

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

def cpu_intensive_task(data: dict) -> dict:
    """CPU-bound task that runs in a separate process."""
    result = sum(i * i for i in range(data["count"]))
    return {"result": result}

async def process_in_parallel(items: list[dict]):
    """Process items in parallel using process pool."""
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        tasks = [
            loop.run_in_executor(executor, cpu_intensive_task, item)
            for item in items
        ]
        results = await asyncio.gather(*tasks)
    return results

# Usage
items = [{"count": i * 1000000} for i in range(10)]
results = await process_in_parallel(items)
```

### Async with ThreadPoolExecutor

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def blocking_io_task(url: str) -> dict:
    """Blocking I/O task (e.g., legacy library)."""
    import requests
    response = requests.get(url)
    return response.json()

async def fetch_with_thread_pool(urls: list[str]):
    """Run blocking tasks in thread pool."""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=20) as executor:
        tasks = [
            loop.run_in_executor(executor, blocking_io_task, url)
            for url in urls
        ]
        results = await asyncio.gather(*tasks)
    return results
```

---

## 8. Async Context Managers <a name="8-async-context"></a>

### Custom Async Context Manager

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db_session():
    """Async context manager for database sessions."""
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()

@asynccontextmanager
async def get_redis_connection():
    """Async context manager for Redis connections."""
    conn = await aioredis.from_url("redis://localhost")
    try:
        yield conn
    finally:
        await conn.close()

# Usage
async def get_user(user_id: int):
    async with get_db_session() as db:
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one()
```

### FastAPI Lifespan

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup and shutdown events."""
    # Startup
    app.state.db_engine = create_async_engine(DATABASE_URL)
    app.state.redis = await aioredis.from_url(REDIS_URL)

    yield

    # Shutdown
    await app.state.db_engine.dispose()
    await app.state.redis.close()

app = FastAPI(lifespan=lifespan)
```

---

## 9. Performance Anti-Patterns <a name="9-anti-patterns"></a>

### Anti-Pattern: Sequential awaits

```python
# BAD: Sequential execution
async def get_dashboard_slow(user_id: int):
    user = await get_user(user_id)  # 100ms
    orders = await get_orders(user_id)  # 200ms
    items = await get_items(user_id)  # 150ms
    # Total: 450ms

# GOOD: Concurrent execution
async def get_dashboard_fast(user_id: int):
    user, orders, items = await asyncio.gather(
        get_user(user_id),
        get_orders(user_id),
        get_items(user_id),
    )
    # Total: ~200ms (slowest task)
```

### Anti-Pattern: Blocking in async

```python
# BAD: Blocking the event loop
async def bad_example():
    import time
    time.sleep(1)  # Blocks entire event loop!
    return {"status": "done"}

# GOOD: Use async sleep
async def good_example():
    import asyncio
    await asyncio.sleep(1)  # Yields control to event loop
    return {"status": "done"}

# GOOD: Run blocking in executor
async def also_good():
    import time
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, time.sleep, 1)
    return {"status": "done"}
```

### Anti-Pattern: Not closing resources

```python
# BAD: Resource leak
async def bad_fetch():
    client = httpx.AsyncClient()
    response = await client.get("https://api.example.com")
    return response.json()
    # Client never closed!

# GOOD: Use context manager
async def good_fetch():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")
        return response.json()
```

---

## 10. Best Practices <a name="10-best-practices"></a>

### 1. Use asyncio.gather for Concurrent I/O

```python
# Fetch multiple resources concurrently
results = await asyncio.gather(
    fetch_users(),
    fetch_products(),
    fetch_orders(),
)
```

### 2. Use Semaphore to Limit Concurrency

```python
semaphore = asyncio.Semaphore(50)

async def limited_fetch(url):
    async with semaphore:
        return await fetch(url)
```

### 3. Use TaskGroup for Structured Concurrency (Python 3.11+)

```python
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(fetch_data1())
    task2 = tg.create_task(fetch_data2())
# Both tasks complete or both are cancelled
```

### 4. Don't Block the Event Loop

```python
# Use async I/O libraries
import httpx  # Async
import aiosqlite  # Async
import aioredis  # Async

# For blocking code, use run_in_executor
await loop.run_in_executor(None, blocking_function)
```

### 5. Use Connection Pools

```python
# Reuse connections
async with httpx.AsyncClient() as client:
    # All requests use same connection pool
    for url in urls:
        await client.get(url)
```

### 6. Monitor Async Performance

```python
import time

@app.middleware("http")
async def measure_time(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{duration:.4f}"
    return response
```

---

## Summary

| Pattern | Use Case | Benefit |
|---------|----------|---------|
| asyncio.gather | Concurrent I/O | Run multiple awaits in parallel |
| TaskGroup | Structured concurrency | Automatic cancellation on error |
| Semaphore | Rate limiting | Control maximum concurrency |
| ProcessPoolExecutor | CPU-bound work | True parallelism |
| ThreadPoolExecutor | Blocking I/O | Don't block event loop |
| Async context managers | Resource management | Proper cleanup |

### Key Rules

1. Use `asyncio.gather()` for concurrent I/O operations
2. Use `Semaphore` to limit concurrency
3. Never block the event loop with sync I/O
4. Use connection pools for HTTP and database
5. Use `run_in_executor()` for blocking code
6. Always close resources with context managers
7. Monitor async performance metrics
