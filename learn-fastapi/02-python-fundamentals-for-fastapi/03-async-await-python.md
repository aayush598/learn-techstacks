# Async/Await in Python for FastAPI

## Table of Contents

1. [What is Async/Await](#what-is-asyncawait)
2. [Coroutines](#coroutines)
3. [Event Loop](#event-loop)
4. [Async vs Sync in Python](#async-vs-sync-in-python)
5. [When to Use Async](#when-to-use-async)
6. [asyncio.gather vs TaskGroup](#asynciogather-vs-taskgroup)
7. [Async Context Managers](#async-context-managers)
8. [Async Iterators](#async-iterators)
9. [asyncio.Semaphore for Concurrency Control](#asynciosemaphore-for-concurrency-control)
10. [Common Async Mistakes](#common-async-mistakes)
11. [Async in FastAPI](#async-in-fastapi)
12. [Interview Questions](#interview-questions)

---

## What is Async/Await

Async/await is Python's syntax for writing concurrent code. It allows a single
thread to handle multiple I/O-bound tasks simultaneously without threading overhead.

### The Problem Async Solves

```python
import time
import requests

# Synchronous - one request at a time
def fetch_data():
    # Each request blocks for ~1 second
    r1 = requests.get("https://api.example.com/data1")  # Block for 1s
    r2 = requests.get("https://api.example.com/data2")  # Block for 1s
    r3 = requests.get("https://api.example.com/data3")  # Block for 1s
    # Total: ~3 seconds
    return r1.json(), r2.json(), r3.json()

# Async - all requests start concurrently
import aiohttp

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        # All three requests start immediately
        r1 = session.get("https://api.example.com/data1")
        r2 = session.get("https://api.example.com/data2")
        r3 = session.get("https://api.example.com/data3")
        # Wait for all to complete
        results = await asyncio.gather(r1, r2, r3)
        # Total: ~1 second (limited by slowest)
        return [r.json() for r in results]
```

### Basic Syntax

```python
import asyncio

# Defining a coroutine
async def greet(name: str) -> str:
    await asyncio.sleep(1)  # Non-blocking sleep
    return f"Hello, {name}!"

# Running a coroutine
async def main():
    message = await greet("World")
    print(message)

# Entry point
asyncio.run(main())
```

---

## Coroutines

Coroutines are special functions that can be paused and resumed. They are the
building blocks of async Python.

### Coroutine Objects

```python
import asyncio

# This is a coroutine function (async def)
async def my_coroutine():
    print("Starting")
    await asyncio.sleep(1)
    print("Finished")
    return "result"

# Calling a coroutine function returns a coroutine object
coro = my_coroutine()
print(type(coro))  # <class 'coroutine'>

# You MUST await or run it
asyncio.run(coro)  # Actually executes the coroutine

# Common mistake - coroutine never executed
# my_coroutine()  # Warning: coroutine was never awaited
```

### Coroutine Execution

```python
import asyncio

async def fetch_user(user_id: int) -> dict:
    print(f"Fetching user {user_id}...")
    await asyncio.sleep(1)  # Simulate I/O
    return {"id": user_id, "name": f"User {user_id}"}

async def main():
    # Method 1: Sequential execution
    user1 = await fetch_user(1)  # Wait for completion
    user2 = await fetch_user(2)  # Then start this
    # Total: ~2 seconds

    # Method 2: Concurrent execution
    user1, user2 = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
    )
    # Total: ~1 second

    # Method 3: Create tasks for concurrency
    task1 = asyncio.create_task(fetch_user(1))
    task2 = asyncio.create_task(fetch_user(2))
    user1 = await task1
    user2 = await task2
    # Total: ~1 second

asyncio.run(main())
```

### Task vs Coroutine

```python
import asyncio

async def slow_operation():
    await asyncio.sleep(2)
    return "done"

async def main():
    # Coroutine - not scheduled yet
    coro = slow_operation()

    # Task - scheduled immediately on creation
    task = asyncio.create_task(slow_operation())

    # Task has additional features
    print(task.done())      # False (not completed yet)
    print(task.cancelled()) # False

    result = await task
    print(task.done())      # True (completed)

    # Can cancel a task
    task2 = asyncio.create_task(slow_operation())
    task2.cancel()  # Cancel before completion

asyncio.run(main())
```

---

## Event Loop

The event loop is the core of async Python. It manages and distributes tasks.

### How the Event Loop Works

```python
import asyncio

# The event loop manages all async operations
async def task1():
    print("Task 1 started")
    await asyncio.sleep(1)
    print("Task 1 finished")
    return 1

async def task2():
    print("Task 2 started")
    await asyncio.sleep(2)
    print("Task 2 finished")
    return 2

async def main():
    # Event loop orchestrates these tasks
    # 1. Start task1 (schedules it)
    # 2. Start task2 (schedules it)
    # 3. task1 sleeps for 1s (event loop moves to task2)
    # 4. task2 sleeps for 2s (event loop waits)
    # 5. After 1s, task1 wakes up and finishes
    # 6. After 2s, task2 wakes up and finishes
    results = await asyncio.gather(task1(), task2())
    # Total time: ~2 seconds, not 3

asyncio.run(main())
```

### Getting the Running Loop

```python
import asyncio

async def main():
    # Get current event loop
    loop = asyncio.get_running_loop()

    # Schedule a callback
    loop.call_soon(print, "Scheduled callback")

    # Schedule a delayed callback
    loop.call_later(1.0, print, "Delayed callback")

    # Schedule a coroutine
    await asyncio.sleep(0.1)

asyncio.run(main())
```

### Running Sync Code in Async Context

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Running CPU-bound sync code in async context
async def main():
    loop = asyncio.get_running_loop()

    # Method 1: run_in_executor (for sync functions)
    with ThreadPoolExecutor() as pool:
        # Runs blocking function in thread pool
        result = await loop.run_in_executor(
            pool, heavy_computation, arg1, arg2
        )

    # Method 2: asyncio.to_thread (Python 3.9+)
    result = await asyncio.to_thread(heavy_computation, arg1, arg2)

def heavy_computation(x: int) -> int:
    # This blocks the thread
    return sum(i * i for i in range(x))

async def main():
    # Run in thread pool to not block event loop
    result = await asyncio.to_thread(heavy_computation, 1000000)
    print(f"Result: {result}")

asyncio.run(main())
```

---

## Async vs Sync in Python

### When Async Shines

```python
# Async excels at I/O-bound operations
# - Network requests (HTTP, WebSocket, database)
# - File I/O (with aiofiles)
# - Process output (subprocess)
# - Any operation that waits for external resources

# Async does NOT help with CPU-bound operations
# - Mathematical computations
# - Data processing
# - Image processing
# - Cryptography

import asyncio
import aiohttp
import aiofiles

async def io_bound():
    # I/O-bound: async helps here
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com") as resp:
            data = await resp.json()

    async with aiofiles.open("file.txt") as f:
        content = await f.read()

    return data

async def cpu_bound():
    # CPU-bound: async does NOT help here
    # This blocks the event loop!
    result = sum(i * i for i in range(10_000_000))
    return result

# To run CPU-bound code in async context:
async def proper_cpu_bound():
    loop = asyncio.get_running_loop()
    # Run in thread pool
    result = await loop.run_in_executor(None, cpu_bound)
    return result
```

### Performance Comparison

```python
import asyncio
import time

# Synchronous approach
def sync_fetch(urls: list[str]) -> list[str]:
    import urllib.request
    results = []
    for url in urls:
        response = urllib.request.urlopen(url)
        results.append(response.read().decode())
    return results
    # 10 URLs x 1 second each = 10 seconds

# Async approach
async def async_fetch(urls: list[str]) -> list[str]:
    import aiohttp
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [await r.text() for r in responses]
    # 10 URLs x 1 second max = ~1 second

# Threading approach
import concurrent.futures
import urllib.request

def threaded_fetch(urls: list[str]) -> list[str]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(urllib.request.urlopen, url) for url in urls]
        return [f.read().decode() for f in futures]
    # 10 URLs x 1 second max = ~1 second (but with thread overhead)
```

---

## When to Use Async

### Use Async When

```python
# 1. Handling many concurrent connections (web servers, APIs)
async def handle_websocket(websocket):
    async for message in websocket:
        await process_message(message)

# 2. Making multiple API calls concurrently
async def aggregate_data():
    async with aiohttp.ClientSession() as session:
        user, posts, comments = await asyncio.gather(
            fetch_user(session, 1),
            fetch_posts(session, 1),
            fetch_comments(session, 1),
        )

# 3. Real-time applications (chat, notifications)
async def websocket_handler(websocket):
    async for message in websocket:
        await broadcast(message)

# 4. Database operations (with async drivers)
async def get_user(user_id: int):
    async with async_engine.connect() as conn:
        result = await conn.execute(select(User).where(User.id == user_id))
        return result.scalar_one()

# 5. File operations with many files
async def process_files(file_paths: list[str]):
    tasks = [process_file(path) for path in file_paths]
    return await asyncio.gather(*tasks)
```

### Don't Use Async When

```python
# 1. CPU-bound operations
def compute_heavy(data):
    # This blocks - don't use async here
    return sum(x * x for x in data)

# 2. Simple scripts with no concurrency
def simple_script():
    # No benefit from async
    print("Hello world")

# 3. When libraries don't support async
def use_sync_library():
    # If the library is sync, async won't help
    import pandas as pd
    df = pd.read_csv("data.csv")
    return df

# 4. Sequential operations with no waiting
async def sequential():
    # No benefit - each operation depends on the previous
    result1 = await compute(1)  # Must wait
    result2 = await compute(result1)  # Must wait
    return result2
```

---

## asyncio.gather vs TaskGroup

### asyncio.gather

```python
import asyncio

async def fetch_data(url: str) -> dict:
    await asyncio.sleep(1)
    return {"url": url, "data": "..."}

async def main():
    urls = ["url1", "url2", "url3"]

    # gather runs all tasks concurrently
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3"),
    )
    # results = [result1, result2, result3]

    # With error handling
    try:
        results = await asyncio.gather(
            fetch_data("url1"),
            fetch_data("url2"),
            return_exceptions=True,  # Don't raise, return exception objects
        )
        for result in results:
            if isinstance(result, Exception):
                print(f"Error: {result}")
            else:
                print(f"Success: {result}")
    except Exception as e:
        print(f"Task failed: {e}")

asyncio.run(main())
```

### TaskGroup (Python 3.11+)

```python
import asyncio

async def fetch_data(url: str) -> dict:
    await asyncio.sleep(1)
    return {"url": url, "data": "..."}

async def main():
    urls = ["url1", "url2", "url3"]

    # TaskGroup provides structured concurrency
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch_data(url)) for url in urls]

    # All tasks completed when exiting the context manager
    results = [task.result() for task in tasks]

    # TaskGroup automatically cancels all tasks on exception
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(fetch_data("url1"))
            tg.create_task(fetch_data("url2"))
            tg.create_task(fetch_data("url3"))
            raise ValueError("Something went wrong")
    except* ValueError as eg:
        # All tasks are automatically cancelled
        for exc in eg.exceptions:
            print(f"Error: {exc}")

asyncio.run(main())
```

### gather vs TaskGroup Comparison

```python
# asyncio.gather:
# - Returns results in order
# - Can use return_exceptions=True
# - Doesn't cancel other tasks on failure
# - Less safe (fire-and-forget)

# TaskGroup:
# - Structured concurrency (safer)
# - Automatically cancels all tasks on failure
# - Better error handling with ExceptionGroup
# - More predictable cleanup
# - Python 3.11+ only

# Example: Error handling difference
import asyncio

async def failing_task():
    await asyncio.sleep(0.5)
    raise ValueError("Task failed")

async def successful_task():
    await asyncio.sleep(1)
    return "success"

# gather: first task fails, second continues
async def with_gather():
    results = await asyncio.gather(
        failing_task(),
        successful_task(),
        return_exceptions=True,
    )
    # results = [ValueError("Task failed"), "success"]
    # Second task still completed!

# TaskGroup: first task fails, all cancelled
async def with_taskgroup():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(failing_task())
            tg.create_task(successful_task())
    except* ValueError:
        pass  # Both tasks cancelled
```

---

## Async Context Managers

### Basic Async Context Manager

```python
import asyncio

# Using async with
class AsyncDatabase:
    async def connect(self):
        print("Connecting to database...")
        await asyncio.sleep(1)
        print("Connected!")

    async def disconnect(self):
        print("Disconnecting...")
        await asyncio.sleep(0.5)

    async def execute(self, query: str):
        await asyncio.sleep(0.5)
        return f"Result of: {query}"

async def main():
    db = AsyncDatabase()
    await db.connect()
    try:
        result = await db.execute("SELECT * FROM users")
        print(result)
    finally:
        await db.disconnect()

# Better: Use async context manager
class AsyncDatabaseConnection:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
        return False  # Don't suppress exceptions

    async def connect(self):
        print("Connecting...")
        await asyncio.sleep(1)

    async def disconnect(self):
        print("Disconnecting...")
        await asyncio.sleep(0.5)

    async def execute(self, query: str):
        await asyncio.sleep(0.5)
        return f"Result: {query}"

async def main():
    async with AsyncDatabaseConnection() as db:
        result = await db.execute("SELECT * FROM users")
        print(result)
    # Automatically disconnects
```

### Creating Async Context Managers

```python
import asyncio
from contextlib import asynccontextmanager

# Method 1: Using asynccontextmanager decorator
@asynccontextmanager
async def get_db_connection():
    conn = await create_connection()
    try:
        yield conn
    finally:
        await conn.close()

# Method 2: Class-based
class AsyncResourceManager:
    def __init__(self, resource_name: str):
        self.resource_name = resource_name

    async def __aenter__(self):
        print(f"Acquiring {self.resource_name}")
        await asyncio.sleep(0.5)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"Releasing {self.resource_name}")
        await asyncio.sleep(0.5)
        return False

# Usage
async def main():
    async with AsyncResourceManager("database") as resource:
        print(f"Using {resource.resource_name}")

    # Or with asynccontextmanager
    async with get_db_connection() as conn:
        result = await conn.execute("SELECT 1")

asyncio.run(main())
```

### FastAPI Async Context Managers

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Lifespan context manager (FastAPI 0.93+)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    await init_database()
    yield
    # Shutdown
    print("Shutting down...")
    await close_database()

app = FastAPI(lifespan=lifespan)

# Or with older on_event style (deprecated)
@app.on_event("startup")
async def startup():
    await init_database()

@app.on_event("shutdown")
async def shutdown():
    await close_database()
```

---

## Async Iterators

### Basic Async Iterator

```python
import asyncio

# Async iterator - yields values asynchronously
class AsyncCounter:
    def __init__(self, start: int, stop: int):
        self.start = start
        self.stop = stop
        self.current = start

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)  # Simulate async operation
        value = self.current
        self.current += 1
        return value

async def main():
    async for number in AsyncCounter(0, 5):
        print(number)
    # Output: 0, 1, 2, 3, 4

asyncio.run(main())
```

### Async Generator

```python
import asyncio

# Async generator - simpler syntax
async def async_range(start: int, stop: int):
    for i in range(start, stop):
        await asyncio.sleep(0.1)
        yield i

# Async generator with cleanup
async def read_large_file(path: str):
    try:
        file = await aiofiles.open(path, mode='r')
        async for line in file:
            yield line.strip()
    finally:
        await file.close()

# Using async generators
async def main():
    async for number in async_range(0, 5):
        print(number)

    # Async list comprehension
    numbers = [num async for num in async_range(0, 10)]

    # Async generator expression
    squares = [num ** 2 async for num in async_range(0, 10)]

asyncio.run(main())
```

### Async Iterators in FastAPI

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

# Streaming response with async iterator
async def event_generator():
    for i in range(10):
        await asyncio.sleep(1)
        yield f"data: {i}\n\n"

@app.get("/stream")
async def stream():
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

# Async pagination
async def paginate_items(page: int, per_page: int):
    offset = (page - 1) * per_page
    async with get_db() as db:
        items = await db.fetch(
            "SELECT * FROM items LIMIT $1 OFFSET $2",
            per_page, offset
        )
        for item in items:
            yield item

@app.get("/items")
async def list_items(page: int = 1, per_page: int = 10):
    items = [item async for item in paginate_items(page, per_page)]
    return {"items": items, "page": page}
```

---

## asyncio.Semaphore for Concurrency Control

### Basic Semaphore

```python
import asyncio

# Semaphore limits concurrent access
semaphore = asyncio.Semaphore(5)  # Allow 5 concurrent operations

async def limited_operation(task_id: int):
    async with semaphore:
        print(f"Task {task_id} started")
        await asyncio.sleep(1)
        print(f"Task {task_id} finished")

async def main():
    # Create 20 tasks, but only 5 run concurrently
    tasks = [limited_operation(i) for i in range(20)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

### Connection Pool with Semaphore

```python
import asyncio

class ConnectionPool:
    def __init__(self, max_connections: int):
        self.semaphore = asyncio.Semaphore(max_connections)
        self.connections = []

    async def get_connection(self):
        async with self.semaphore:
            conn = await self._create_connection()
            try:
                yield conn
            finally:
                await self._release_connection(conn)

    async def _create_connection(self):
        # Simulate connection creation
        await asyncio.sleep(0.1)
        conn = {"id": len(self.connections)}
        self.connections.append(conn)
        return conn

    async def _release_connection(self, conn):
        self.connections.remove(conn)

# Usage
pool = ConnectionPool(max_connections=10)

async def query_database(query: str):
    async with pool.get_connection() as conn:
        # Use connection
        await asyncio.sleep(0.5)
        return f"Result from connection {conn['id']}"
```

### Semaphore in FastAPI

```python
from fastapi import FastAPI, Depends
import asyncio

app = FastAPI()

# Limit concurrent requests to external API
api_semaphore = asyncio.Semaphore(10)

async def get_semaphore():
    return api_semaphore

@app.get("/proxy")
async def proxy_endpoint(semaphore: asyncio.Semaphore = Depends(get_semaphore)):
    async with semaphore:
        # Only 10 concurrent requests to external API
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.external.com") as resp:
                return await resp.json()

# Rate limiting middleware
class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    async def __call__(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()

        # Clean old requests
        if client_ip in self.requests:
            self.requests[client_ip] = [
                t for t in self.requests[client_ip]
                if now - t < self.window_seconds
            ]
        else:
            self.requests[client_ip] = []

        if len(self.requests[client_ip]) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded"}
            )

        self.requests[client_ip].append(now)
        return await call_next(request)
```

---

## Common Async Mistakes

### Mistake 1: Blocking the Event Loop

```python
import asyncio
import time

async def bad_example():
    # BAD: This blocks the event loop!
    time.sleep(5)  # Blocks everything

    # GOOD: Use async sleep
    await asyncio.sleep(5)  # Non-blocking

    # GOOD: Run blocking code in executor
    await asyncio.to_thread(time.sleep, 5)

async def main():
    # These would all be blocked by time.sleep
    await asyncio.gather(bad_example(), other_task())

async def other_task():
    print("This would be blocked!")
```

### Mistake 2: Forgetting to Await

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return "data"

async def main():
    # BAD: Coroutine never awaited
    fetch_data()  # Warning: coroutine was never awaited

    # GOOD: Always await coroutines
    result = await fetch_data()

    # BAD: Forgetting to await in gather
    await asyncio.gather(
        fetch_data(),  # OK
        fetch_data(),  # OK
    )

    # GOOD: Proper await
    results = await asyncio.gather(
        fetch_data(),
        fetch_data(),
    )
```

### Mistake 3: Creating Tasks Without Keeping References

```python
import asyncio

async def background_task():
    while True:
        print("Background task running...")
        await asyncio.sleep(1)

async def main():
    # BAD: Task may be garbage collected
    asyncio.create_task(background_task())  # Task may be lost!
    await asyncio.sleep(10)

    # GOOD: Keep reference to task
    task = asyncio.create_task(background_task())
    try:
        await asyncio.sleep(10)
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
```

### Mistake 4: Using Async Libraries Incorrectly

```python
# BAD: Using sync library in async code
import requests  # Sync library!

async def bad_fetch():
    # This blocks the event loop!
    response = requests.get("https://api.example.com")
    return response.json()

# GOOD: Use async library
import aiohttp

async def good_fetch():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com") as resp:
            return await resp.json()

# GOOD: Run sync library in thread
async def also_good_fetch():
    return await asyncio.to_thread(
        requests.get, "https://api.example.com"
    )
```

### Mistake 5: Unnecessary Async

```python
# BAD: No I/O operation, async is unnecessary
async def pure_computation(n: int) -> int:
    return sum(i * i for i in range(n))

# GOOD: Synchronous for pure computation
def pure_computation(n: int) -> int:
    return sum(i * i for i in range(n))

# BAD: Sequential async operations with no concurrency benefit
async def sequential_operations():
    result1 = await compute(1)  # Each depends on previous
    result2 = await compute(result1)  # No parallelism possible
    return result2

# GOOD: Synchronous if no concurrency needed
def sequential_operations():
    result1 = compute(1)
    result2 = compute(result1)
    return result2
```

### Mistake 6: Incorrect Exception Handling

```python
import asyncio

async def risky_operation():
    await asyncio.sleep(0.5)
    raise ValueError("Something went wrong")

async def main():
    # BAD: Exception in one task cancels all
    try:
        await asyncio.gather(
            risky_operation(),
            other_task(),
        )
    except ValueError:
        pass  # other_task is cancelled!

    # GOOD: Use return_exceptions=True
    results = await asyncio.gather(
        risky_operation(),
        other_task(),
        return_exceptions=True,
    )
    for result in results:
        if isinstance(result, Exception):
            print(f"Task failed: {result}")

    # GOOD: Use TaskGroup for structured concurrency
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(risky_operation())
            tg.create_task(other_task())
    except* ValueError as eg:
        for exc in eg.exceptions:
            print(f"Error: {exc}")
```

---

## Async in FastAPI

### How FastAPI Handles Both Async and Sync

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

# FastAPI handles both async and sync functions

# Async endpoint - runs directly on event loop
@app.get("/async")
async def async_endpoint():
    await asyncio.sleep(1)  # Non-blocking
    return {"message": "Async"}

# Sync endpoint - runs in thread pool
@app.get("/sync")
def sync_endpoint():
    time.sleep(1)  # Runs in thread pool, doesn't block event loop
    return {"message": "Sync"}

# FastAPI automatically detects and handles both
# - async def: Run on event loop
# - def: Run in thread pool (run_in_executor)

# You can also use BackgroundTasks with both
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message)

@app.post("/log")
async def log_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "Request logged")
    return {"message": "Log queued"}
```

### Async Dependencies

```python
from fastapi import FastAPI, Depends
import asyncio

app = FastAPI()

# Async dependency
async def get_db():
    db = await create_db_connection()
    try:
        yield db
    finally:
        await db.close()

# Async dependency with other async operations
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await fetch_user_from_token(token)
    return user

@app.get("/users/me")
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user

# Mixing async and sync dependencies
def get_settings():
    # Sync dependency (runs in thread pool)
    return Settings()

async def get_cache(settings = Depends(get_settings)):
    # Async dependency using sync dependency
    cache = await create_cache(settings)
    return cache
```

### Async Database Operations

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Async engine
engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session

@app.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    # Async query
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@app.post("/users")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
```

---

## Interview Questions

### Q1: What is the difference between async and sync in Python?

**Answer:** Sync code executes sequentially - each operation blocks until complete. Async code uses coroutines and an event loop to handle multiple I/O operations concurrently. Async doesn't make individual operations faster, but allows waiting for multiple operations simultaneously. Sync is simpler; async is better for high-concurrency I/O-bound workloads.

### Q2: What is an event loop?

**Answer:** The event loop is Python's mechanism for managing and dispatching async tasks. It monitors coroutines, schedules their execution, handles I/O events, and runs callbacks. When a coroutine awaits, the event loop switches to another ready coroutine. `asyncio.run()` creates and runs the event loop.

### Q3: What is a coroutine?

**Answer:** A coroutine is a special function defined with `async def` that can be paused and resumed. Calling a coroutine function returns a coroutine object. Coroutines use `await` to pause execution until a result is available. They're the building blocks of async Python.

### Q4: What is the difference between `asyncio.gather` and `TaskGroup`?

**Answer:** `asyncio.gather` runs tasks concurrently and returns results in order. `TaskGroup` (Python 3.11+) provides structured concurrency - it automatically cancels all tasks if any fails. `TaskGroup` is safer and more predictable. `gather` is simpler and works on older Python versions.

### Q5: How does FastAPI handle both sync and async endpoints?

**Answer:** FastAPI detects whether a function is `async def` or `def`. Async functions run directly on the event loop. Sync functions are automatically run in a thread pool using `run_in_executor`. This means sync endpoints don't block the event loop, but async endpoints are more efficient.

### Q6: What is `asyncio.Semaphore` used for?

**Answer:** A semaphore limits concurrent access to a resource. `asyncio.Semaphore(n)` allows at most `n` coroutines to hold the semaphore simultaneously. It's used for connection pooling, rate limiting, and preventing resource exhaustion.

### Q7: What is the difference between a coroutine and a task?

**Answer:** A coroutine is a function defined with `async def`. A task is a coroutine wrapped in a `Task` object that's scheduled to run on the event loop. Tasks are created with `asyncio.create_task()` and start executing immediately. Coroutines must be awaited or scheduled.

### Q8: What are async context managers?

**Answer:** Async context managers use `async with` and implement `__aenter__` and `__aexit__` methods. They allow async setup and cleanup of resources. Created with `@asynccontextmanager` decorator or class-based implementation. Used for async database connections, file handles, etc.

### Q9: What is the GIL and how does it affect async?

**Answer:** The Global Interpreter Lock (GIL) prevents multiple threads from executing Python code simultaneously. Async Python doesn't use threads - it uses a single thread with cooperative multitasking. The GIL doesn't affect async performance because async doesn't rely on parallelism. Async is for I/O concurrency, not CPU parallelism.

### Q10: When should you NOT use async?

**Answer:** Don't use async for: (1) CPU-bound operations (use multiprocessing), (2) simple scripts with no concurrency, (3) when libraries don't support async, (4) sequential operations with no waiting. Async adds complexity - only use it when the benefits outweigh the costs.

### Q11: What happens if you block the event loop?

**Answer:** Blocking the event loop (e.g., with `time.sleep()`) prevents all other coroutines from running. This defeats the purpose of async. The entire application becomes unresponsive. Use `asyncio.sleep()` or run blocking code in a thread pool with `asyncio.to_thread()`.

### Q12: What is `asyncio.to_thread`?

**Answer:** `asyncio.to_thread(func, *args)` runs a synchronous function in a thread pool without blocking the event loop. It's useful when you need to call blocking libraries in async code. It returns a coroutine that resolves when the function completes.

### Q13: What is structured concurrency?

**Answer:** Structured concurrency ensures that all spawned tasks complete before the parent scope exits. `asyncio.TaskGroup` implements this - if any task fails, all tasks are cancelled and the exception propagates. This prevents "fire-and-forget" tasks that can leak resources.

### Q14: How do you handle exceptions in async code?

**Answer:** Use `try/except` blocks around `await` calls. For `asyncio.gather`, use `return_exceptions=True` to prevent one failure from cancelling others. For `TaskGroup`, use `except*` to handle `ExceptionGroup`. Always clean up resources in `finally` blocks.

### Q15: What is an async generator?

**Answer:** An async generator is a function with `async def` that uses `yield`. It can `await` between yields. Used for streaming data, pagination, or any case where you need to produce values asynchronously. Consumed with `async for` loop.
