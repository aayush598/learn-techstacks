# Yield Dependencies in FastAPI

## Table of Contents

1. [What are Yield Dependencies](#what-are-yield-dependencies)
2. [Setup/Teardown Pattern](#setup teardown-pattern)
3. [Database Session Management](#database-session-management)
4. [File Handle Management](#file-handle-management)
5. [Yield with try/finally](#yield-with-tryfinally)
6. [Exception Handling in Yield Dependencies](#exception-handling-in-yield-dependencies)
7. [Yield Dependency Cleanup Order](#yield-dependency-cleanup-order)
8. [Async Yield Dependencies](#async-yield-dependencies)
9. [Advanced Patterns](#advanced-patterns)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## What are Yield Dependencies

Yield dependencies are dependencies that use Python's `yield` keyword to provide a setup/teardown mechanism. They are **generators** that produce a value for the route handler and perform cleanup after the handler completes.

### The Core Concept

```python
def get_dependency():
    # SETUP: Code before yield runs when dependency is resolved
    resource = acquire_resource()
    print("Resource acquired")

    yield resource  # This value is injected into the route handler

    # TEARDOWN: Code after yield runs after the response is sent
    resource.close()
    print("Resource released")
```

### How FastAPI Processes Yield Dependencies

```
1. Request arrives
2. FastAPI calls the dependency generator
3. Code before `yield` executes
4. The yielded value is passed to the route handler
5. The route handler executes
6. The route handler returns a response
7. Code after `yield` executes (cleanup)
8. The response is sent to the client
```

### Simple Example

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def simple_yield():
    print("Before yield")
    yield "Hello from dependency"
    print("After yield")

@app.get("/")
def route(msg: str = Depends(simple_yield)):
    print(f"Handler received: {msg}")
    return {"message": msg}

# When GET / is called:
# Output: "Before yield"
# Output: "Handler received: Hello from dependency"
# Output: "After yield"
```

---

## Setup/Teardown Pattern

Yield dependencies implement the classic Setup/Teardown pattern elegantly.

### General Pattern

```python
def resource_manager():
    # === SETUP ===
    resource = create_resource()
    print(f"Setup: {resource}")

    try:
        yield resource  # === HANDOVER ===
    finally:
        # === TEARDOWN ===
        resource.cleanup()
        print(f"Teardown: {resource}")
```

### Multiple Resources

```python
def multi_resource_manager():
    # Setup multiple resources
    db = create_database_connection()
    cache = create_redis_connection()
    logger = create_logger()

    try:
        yield {
            "db": db,
            "cache": cache,
            "logger": logger,
        }
    finally:
        # Teardown in reverse order
        logger.close()
        cache.close()
        db.close()

@app.get("/")
def route(resources: dict = Depends(multi_resource_manager)):
    db = resources["db"]
    cache = resources["cache"]
    logger = resources["logger"]
    # ... use resources
```

### Real-World Example: External API Client

```python
import httpx

def get_api_client():
    client = httpx.AsyncClient(
        base_url="https://api.external-service.com",
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=30.0,
    )
    try:
        yield client
    finally:
        await client.aclose()

@app.get("/external-data/")
async def fetch_external_data(client: httpx.AsyncClient = Depends(get_api_client)):
    response = await client.get("/data")
    return response.json()
```

---

## Database Session Management

The most common use of yield dependencies is database session management.

### SQLAlchemy Session Dependency

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "postgresql://user:pass@localhost/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Yield a SQLAlchemy database session.

    The session is automatically closed after the request completes,
    whether the request succeeds or fails.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

### Why `finally` is Critical

```python
# DANGEROUS: No finally block
def get_db():
    db = SessionLocal()
    yield db
    db.close()  # Never called if exception occurs!

# SAFE: Finally block ensures cleanup
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Always called
```

### Async SQLAlchemy Session

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

async_engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/dbname",
    echo=True,
)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

@app.get("/users/")
async def list_users(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```

### Connection Pool with Yield

```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)

def get_db_with_pool():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    try:
        yield session
        transaction.commit()
    except Exception:
        transaction.rollback()
        raise
    finally:
        session.close()
        connection.close()
```

---

## File Handle Management

Yield dependencies are excellent for managing file handles.

### CSV File Processing

```python
import csv
from pathlib import Path

def read_csv_file(file_path: Path):
    """Open a CSV file, yield the reader, close after use."""
    file = open(file_path, "r", newline="", encoding="utf-8")
    reader = csv.DictReader(file)
    try:
        yield reader
    finally:
        file.close()

@app.get("/import/{filename}")
def import_data(
    filename: str,
    reader: csv.DictReader = Depends(read_csv_file),
):
    rows = list(reader)
    return {"total_rows": len(rows), "data": rows}
```

### Temporary File Management

```python
import tempfile
import os

def temporary_workspace():
    """Create a temporary directory, yield the path, clean up after."""
    temp_dir = tempfile.mkdtemp(prefix="fastapi_work_")
    try:
        yield Path(temp_dir)
    finally:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

@app.post("/process-upload/")
async def process_upload(
    file: UploadFile,
    workspace: Path = Depends(temporary_workspace),
):
    # Save uploaded file to temp directory
    temp_file = workspace / file.filename
    content = await file.read()
    temp_file.write_bytes(content)

    # Process the file
    result = process_file(temp_file)
    return result

# The temp directory is automatically cleaned up
```

### Log File Handler

```python
import logging
from datetime import datetime

def get_request_logger():
    """Create a per-request log file."""
    log_filename = f"logs/request_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger = logging.getLogger(f"request_{id}")
    handler = logging.FileHandler(log_filename)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    try:
        yield logger
    finally:
        handler.close()
        logger.removeHandler(handler)

@app.get("/process/")
def process_data(logger: logging.Logger = Depends(get_request_logger)):
    logger.info("Processing started")
    result = do_work()
    logger.info(f"Processing complete: {result}")
    return result
```

---

## Yield with try/finally

The `try/finally` pattern in yield dependencies ensures cleanup happens regardless of what happens in the route handler.

### Pattern Variations

```python
# Pattern 1: Basic try/finally
def dep():
    resource = acquire()
    try:
        yield resource
    finally:
        resource.release()

# Pattern 2: try/except/finally
def dep():
    resource = acquire()
    try:
        yield resource
    except Exception as e:
        log_error(e)
        raise
    finally:
        resource.release()

# Pattern 3: Conditional cleanup
def dep():
    resource = acquire()
    try:
        yield resource
    finally:
        if resource.is_connected:
            resource.disconnect()
```

### Real-World: Transaction Management

```python
def get_db_transaction():
    db = SessionLocal()
    transaction = db.begin()
    try:
        yield db
        transaction.commit()  # Commit if no exception
    except Exception:
        transaction.rollback()  # Rollback on exception
        raise
    finally:
        db.close()  # Always close session

@app.post("/transfer/")
def transfer_funds(
    transfer: TransferRequest,
    db: Session = Depends(get_db_transaction),
):
    sender = db.query(Account).get(transfer.sender_id)
    receiver = db.query(Account).get(transfer.receiver_id)

    sender.balance -= transfer.amount
    receiver.balance += transfer.amount

    # If this raises, transaction is rolled back
    if sender.balance < 0:
        raise HTTPException(400, "Insufficient funds")

    # If we reach here, transaction is committed
    return {"status": "success"}
```

### Semaphore/Lock Management

```python
import asyncio

# Global semaphore to limit concurrent operations
semaphore = asyncio.Semaphore(10)

async def rate_limited():
    """Limit concurrent access to a resource."""
    await semaphore.acquire()
    try:
        yield
    finally:
        semaphore.release()

@app.get("/limited/")
async def limited_endpoint(_: None = Depends(rate_limited)):
    # Only 10 requests can execute this concurrently
    result = await expensive_operation()
    return result
```

---

## Exception Handling in Yield Dependencies

### How Exceptions Propagate

```python
def dep():
    print("Setup")
    try:
        yield "value"
    except Exception as e:
        print(f"Caught exception: {e}")
        raise  # Re-raise to propagate to FastAPI
    finally:
        print("Always runs")

@app.get("/error/")
def error_route(dep: str = Depends(dep)):
    raise ValueError("Something went wrong")

# Output:
# "Setup"
# "Caught exception: Something went wrong"
# "Always runs"
# FastAPI returns 500 Internal Server Error
```

### Handling Specific Exceptions

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error: {e}")
        raise
    finally:
        db.close()

@app.post("/data/")
def create_data(data: DataCreate, db: Session = Depends(get_db)):
    record = Record(**data.dict())
    db.add(record)
    db.commit()
    return record
```

### Error Logging Dependency

```python
import traceback
from datetime import datetime

def error_logging():
    start_time = datetime.now()
    errors = []

    class ErrorCollector:
        def log_error(self, error: Exception):
            errors.append({
                "type": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc(),
                "timestamp": datetime.now().isoformat(),
            })

    collector = ErrorCollector()
    try:
        yield collector
    except Exception as e:
        collector.log_error(e)
        raise
    finally:
        elapsed = (datetime.now() - start_time).total_seconds()
        if errors:
            logger.error(
                f"Request failed after {elapsed}s with {len(errors)} errors: "
                f"{errors}"
            )
        else:
            logger.info(f"Request completed in {elapsed}s")
```

### Exception Translation

```python
def translate_errors():
    try:
        yield
    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=409, detail="Resource already exists")
    except DatabaseNotFoundError as e:
        raise HTTPException(status_code=404, detail="Resource not found")
    except DatabaseTimeoutError as e:
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except Exception as e:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## Yield Dependency Cleanup Order

FastAPI guarantees that yield dependencies are cleaned up in **LIFO (Last In, First Out)** order — the reverse of their resolution order.

### Demonstration

```python
def dep_a():
    print("Setup A")
    yield "A"
    print("Teardown A")

def dep_b():
    print("Setup B")
    yield "B"
    print("Teardown B")

def dep_c():
    print("Setup C")
    yield "C"
    print("Teardown C")

@app.get("/")
def route(
    a: str = Depends(dep_a),
    b: str = Depends(dep_b),
    c: str = Depends(dep_c),
):
    print("Handler executing")
    return {"a": a, "b": b, "c": c}

# Output:
# "Setup A"
# "Setup B"
# "Setup C"
# "Handler executing"
# "Teardown C"
# "Teardown B"
# "Teardown A"
```

### Why LIFO Matters

```python
def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_transaction(db: Session = Depends(get_database)):
    transaction = db.begin()
    try:
        yield transaction
    except Exception:
        transaction.rollback()
        raise
    finally:
        transaction.close()

# Cleanup order:
# 1. Transaction is closed (last resolved, first cleaned up)
# 2. Database session is closed (first resolved, last cleaned up)
# This is correct — you must close transaction before closing the session
```

### Complex Cleanup Graph

```
Resolution order: A → B → C → D
Cleanup order: D → C → B → A

With sub-dependencies:
A resolves → B resolves → C resolves
Cleanup: C → B → A

With shared dependencies (cached):
A resolves → B resolves (uses A's cache) → C resolves
Cleanup: C → B → A (A cleaned once, not twice)
```

---

## Async Yield Dependencies

### Basic Async Yield

```python
async def get_async_db():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        session = AsyncSession(bind=conn)
        try:
            yield session
        finally:
            await session.close()

@app.get("/users/")
async def list_users(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```

### Async File Operations

```python
import aiofiles

async def async_file_reader(file_path: str):
    async with aiofiles.open(file_path, "r") as f:
        yield f

@app.get("/read/{filename}")
async def read_file(
    filename: str,
    f: aiofiles.threadpool.AsyncTextIOWrapper = Depends(async_file_reader),
):
    content = await f.read()
    return {"content": content}
```

### Async Context Manager Pattern

```python
from contextlib import asynccontextmanager

class AsyncResource:
    @asynccontextmanager
    async def acquire(self):
        resource = await self._create()
        try:
            yield resource
        finally:
            await resource.close()

# As a yield dependency
async def get_resource():
    resource = AsyncResource()
    async with resource.acquire() as res:
        yield res
```

---

## Advanced Patterns

### Conditional Cleanup

```python
def get_db():
    db = SessionLocal()
    committed = False
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    else:
        try:
            db.commit()
            committed = True
        except Exception:
            db.rollback()
            raise
    finally:
        if not committed:
            db.rollback()
        db.close()
```

### Cached Yield Dependencies with Cleanup

```python
from typing import Generator

# IMPORTANT: Yield dependencies with use_cache=True (default)
# work correctly — cleanup happens once after the request

def get_db_session():
    """This is cached — db.close() called once after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Even if multiple parameters use Depends(get_db_session),
# cleanup runs once
```

### Nested Yield Dependencies

```python
def get_outer():
    print("Outer setup")
    resource_outer = acquire_outer()
    try:
        yield resource_outer
    finally:
        print("Outer teardown")
        resource_outer.close()

def get_inner(outer=Depends(get_outer)):
    print("Inner setup")
    resource_inner = acquire_inner(outer)
    try:
        yield resource_inner
    finally:
        print("Inner teardown")
        resource_inner.close()

# Output:
# "Outer setup"
# "Inner setup"
# [handler executes]
# "Inner teardown"
# "Outer teardown"
```

### Yield with State

```python
def get_request_context():
    context = {
        "start_time": time.time(),
        "db_queries": 0,
        "cache_hits": 0,
    }
    try:
        yield context
    finally:
        elapsed = time.time() - context["start_time"]
        logger.info(
            f"Request: {elapsed:.3f}s, "
            f"queries: {context['db_queries']}, "
            f"cache_hits: {context['cache_hits']}"
        )

@app.get("/stats/")
def get_stats(
    ctx: dict = Depends(get_request_context),
    db: Session = Depends(get_db),
):
    ctx["db_queries"] += 1
    users = db.query(User).all()
    return {"count": len(users)}
```

---

## Best Practices

### 1. Always Use try/finally for Cleanup

```python
# BAD: Cleanup might not happen
def get_db():
    db = SessionLocal()
    yield db
    db.close()  # Won't run on exception

# GOOD: Cleanup always happens
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2. Keep Dependencies Focused

```python
# BAD: One dependency managing everything
def get_everything():
    db = SessionLocal()
    cache = Redis()
    logger = get_logger()
    file = open("log.txt", "w")
    try:
        yield {"db": db, "cache": cache, "logger": logger, "file": file}
    finally:
        file.close()
        cache.close()
        db.close()

# GOOD: Each dependency manages its own resource
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_cache():
    cache = Redis()
    try:
        yield cache
    finally:
        cache.close()
```

### 3. Log Cleanup Errors

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"Error closing DB session: {e}")
```

### 4. Don't Return Values from Cleanup Code

```python
# BAD: Confusing
def dep():
    yield value
    return "cleanup result"  # Ignored, but confusing

# GOOD: Cleanup is for side effects only
def dep():
    yield value
    cleanup()  # Just do the cleanup
```

---

## Interview Questions

### Q1: What are yield dependencies in FastAPI?
**Answer:** Yield dependencies are generator functions used as dependencies. Code before `yield` runs during setup, the yielded value is injected into the handler, and code after `yield` runs during cleanup (teardown).

### Q2: When does the cleanup code in a yield dependency execute?
**Answer:** After the route handler returns a response and before the response is sent to the client. Cleanup happens even if the handler raises an exception.

### Q3: What is the cleanup order for multiple yield dependencies?
**Answer:** LIFO (Last In, First Out). Dependencies resolved last are cleaned up first. This ensures correct resource release ordering (e.g., close transaction before closing DB connection).

### Q4: Why use `try/finally` in yield dependencies?
**Answer:** To ensure cleanup code always runs, even if the route handler or setup code raises an exception. Without `try/finally`, resource leaks can occur.

### Q5: Can yield dependencies be async?
**Answer:** Yes. Async yield dependencies use `async def` and `await` in the cleanup section. FastAPI processes them asynchronously on the event loop.

### Q6: What happens if a yield dependency's cleanup code raises an exception?
**Answer:** The exception propagates and may override the original response. FastAPI may return a 500 error. Always handle exceptions in cleanup code or let them pass silently.

### Q7: How do yield dependencies interact with `use_cache`?
**Answer:** With `use_cache=True` (default), the yield dependency is resolved once and cleaned up once. With `use_cache=False`, each resolution creates and cleans up independently.

### Q8: Can you have multiple yield statements in one dependency?
**Answer:** Technically yes (it becomes a multi-yield generator), but FastAPI only takes the first yielded value. Multiple yields are not recommended — use separate dependencies.

### Q9: What is the most common use case for yield dependencies?
**Answer:** Database session management. The session is created in setup, yielded to the handler, and closed in the finally block.

### Q10: How do yield dependencies differ from context managers?
**Answer:** They serve similar purposes. Yield dependencies are FastAPI's version of the setup/teardown pattern. `contextlib.contextmanager` is the general Python equivalent. FastAPI's yield dependencies integrate with the DI system.

### Q11: Can a yield dependency yield None?
**Answer:** Yes. Use it when the dependency is only for setup/teardown side effects, like creating a log file or acquiring a lock.

### Q12: What happens to the database session if the route handler commits?
**Answer:** The session is still closed in the `finally` block. The commit happens before cleanup. If you need auto-commit, handle it in the dependency or use middleware.

### Q13: How do you handle rollback in yield dependencies?
**Answer:** Catch exceptions before yield, rollback, and re-raise. Or let the route handler handle it and only do cleanup in `finally`.

### Q14: Can yield dependencies have sub-dependencies?
**Answer:** Yes. A yield dependency can use `Depends()` in its parameters. Sub-dependencies resolve first and their cleanup runs in LIFO order.

### Q15: What is the difference between yield dependency cleanup and middleware?
**Answer:** Yield dependency cleanup runs after the response but is scoped to the dependency. Middleware runs for every request and wraps the entire request/response cycle. Use yield dependencies for resource-specific cleanup.

---

## Summary

Yield dependencies are FastAPI's mechanism for resource management. They ensure proper setup and cleanup of resources like database sessions, file handles, connections, and locks. Combined with `try/finally`, they provide robust cleanup guarantees that prevent resource leaks even in error scenarios. Understanding LIFO cleanup order is essential for composing multiple yield dependencies correctly.
