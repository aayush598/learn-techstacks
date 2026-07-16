# FastAPI BackgroundTasks

## Table of Contents
1. [What are Background Tasks?](#what-are-background-tasks)
2. [Basic Usage](#basic-usage)
3. [Adding Tasks](#adding-tasks)
4. [Tasks with Dependencies](#tasks-with-dependencies)
5. [Tasks with Parameters](#tasks-with-parameters)
6. [Tasks After Response](#tasks-after-response)
7. [Task Failure Handling](#task-failure-handling)
8. [Limitations of BackgroundTasks](#limitations-of-backgroundtasks)
9. [When to Use vs Task Queue](#when-to-use-vs-task-queue)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## What are Background Tasks?

Background tasks are functions that run after the response has been sent to the client. They're useful for operations that don't need to block the response but need to happen eventually.

### Use Cases

- Sending emails after user registration
- Updating search indexes
- Generating reports
- Processing uploaded files
- Sending notifications
- Cleaning up temporary data
- Logging analytics events

### How They Work

```
Client → Request → Route Handler → Response (sent to client)
                                      ↓
                               Background Task (runs after)
```

---

## Basic Usage

### Using BackgroundTasks Dependency

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def send_email(email: str, subject: str, body: str):
    # Simulate sending email
    print(f"Sending email to {email}")
    # In real app: use SMTP, SendGrid, etc.

@app.post("/register")
async def register_user(email: str, background_tasks: BackgroundTasks):
    # Create user in database
    user = create_user(email)

    # Add background task
    background_tasks.add_task(send_email, email, "Welcome!", "Thanks for registering")

    return {"message": "User created", "user_id": user.id}
```

### Multiple Background Tasks

```python
@app.post("/register")
async def register_user(email: str, background_tasks: BackgroundTasks):
    user = create_user(email)

    # Multiple background tasks run sequentially
    background_tasks.add_task(send_email, email, "Welcome!", "Thanks for registering")
    background_tasks.add_task(update_analytics, "user_registered", {"email": email})
    background_tasks.add_task(index_user, user.id)

    return {"message": "User created"}
```

---

## Adding Tasks

### With Positional Arguments

```python
def process_data(data: dict, user_id: int):
    # Process data
    pass

@app.post("/process")
async def process(data: dict, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_data, data, current_user.id)
    return {"status": "processing"}
```

### With Keyword Arguments

```python
def send_notification(user_id: int, title: str, message: str, priority: str = "normal"):
    # Send notification
    pass

@app.post("/notify")
async def notify(user_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        send_notification,
        user_id,
        title="Update",
        message="Your report is ready",
        priority="high"
    )
    return {"status": "notified"}
```

### With Async Functions

```python
async def async_send_email(email: str, subject: str):
    # Async email sending
    async with aiosmtplib.SMTP(host="smtp.example.com") as smtp:
        await smtp.send_message(message)

@app.post("/register")
async def register(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(async_send_email, email, "Welcome!")
    return {"message": "Registered"}
```

---

## Tasks with Dependencies

### Accessing Dependencies

```python
from fastapi import Depends

async def get_db():
    db = await create_db_connection()
    try:
        yield db
    finally:
        await db.close()

def process_in_background(db_url: str, data: dict):
    # Can't use async dependencies directly
    # Pass connection info instead
    import sqlite3
    conn = sqlite3.connect(db_url)
    # Process data
    conn.close()

@app.post("/process")
async def process(
    data: dict,
    background_tasks: BackgroundTasks,
    db_url: str = Depends(get_db_url)
):
    # Pass dependency values as arguments
    background_tasks.add_task(process_in_background, db_url, data)
    return {"status": "processing"}
```

### Using Request State

```python
@app.post("/process")
async def process(
    data: dict,
    background_tasks: BackgroundTasks,
    request: Request
):
    # Store data in request state for background task
    background_tasks.add_task(
        process_data,
        data=data,
        user_id=request.state.user_id,
        request_id=request.state.request_id
    )
    return {"status": "processing"}
```

---

## Tasks with Parameters

### Complex Parameters

```python
from pydantic import BaseModel

class OrderData(BaseModel):
    order_id: int
    items: list[dict]
    total: float
    customer_email: str

def process_order(order_id: int, items: list, total: float, email: str):
    # Process order
    print(f"Processing order {order_id}")
    # Update inventory, charge payment, etc.

@app.post("/orders")
async def create_order(order: OrderData, background_tasks: BackgroundTasks):
    # Save order to database
    db_order = save_order(order)

    background_tasks.add_task(
        process_order,
        order.order_id,
        order.items,
        order.total,
        order.customer_email
    )

    return {"order_id": db_order.id, "status": "created"}
```

### Passing Mutable Objects

```python
def update_index(data: dict):
    # Be careful: data might be modified after task is queued
    # Make a copy if needed
    data_copy = data.copy()
    # Update search index
    pass

@app.post("/index")
async def index_data(data: dict, background_tasks: BackgroundTasks):
    # Pass a copy to avoid mutation issues
    background_tasks.add_task(update_index, data.copy())
    return {"status": "indexing"}
```

---

## Tasks After Response

### How It Works

```python
import time

def slow_task():
    # This runs AFTER the response is sent
    time.sleep(5)  # Simulate slow work
    print("Task completed")

@app.post("/task")
async def run_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(slow_task)
    return {"message": "Task started"}  # Response sent immediately

# Output:
# 1. Client receives {"message": "Task started"} immediately
# 2. After 5 seconds, "Task completed" is printed
```

### Chaining Tasks

```python
def step_one(data: dict):
    result = process_data(data)
    return result

def step_two(result: dict):
    # Can't directly chain with BackgroundTasks
    # Use a task queue for chaining
    pass

@app.post("/chain")
async def chain_tasks(background_tasks: BackgroundTasks):
    background_tasks.add_task(step_one, {"key": "value"})
    # step_two won't automatically run after step_one
    return {"message": "Step one started"}
```

---

## Task Failure Handling

### Handling Exceptions in Tasks

```python
import logging

logger = logging.getLogger(__name__)

def risky_task(data: dict):
    try:
        # Risky operation
        process_data(data)
    except Exception as e:
        logger.error(f"Background task failed: {e}")
        # Don't let exceptions crash the task
        # Log and handle gracefully

@app.post("/task")
async def run_task(data: dict, background_tasks: BackgroundTasks):
    background_tasks.add_task(risky_task, data)
    return {"status": "started"}
```

### Task with Retry Logic

```python
import time

def task_with_retry(data: dict, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            process_data(data)
            return  # Success
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            logger.error(f"Task failed after {max_retries} attempts: {e}")

@app.post("/task")
async def run_task(data: dict, background_tasks: BackgroundTasks):
    background_tasks.add_task(task_with_retry, data)
    return {"status": "started"}
```

---

## Limitations of BackgroundTasks

### 1. No Result Tracking

```python
# Can't get the result of a background task
background_tasks.add_task(process_data, data)
# No way to know when it completes or get its result
```

### 2. No Progress Reporting

```python
# Can't report progress back to the client
background_tasks.add_task(long_running_task, data)
# Client has no way to know progress
```

### 3. No Cancellation

```python
# Can't cancel a running background task
background_tasks.add_task(long_running_task, data)
# No way to stop it once started
```

### 4. No Distributed Execution

```python
# Tasks run in the same process as the API server
# If the server crashes, tasks are lost
# No horizontal scaling for tasks
```

### 5. No Retry Mechanism

```python
# Built-in BackgroundTasks has no retry support
# You must implement retry logic manually
```

### 6. No Task Priority

```python
# All tasks have equal priority
# No way to prioritize critical tasks
```

### 7. Memory Limitations

```python
# Tasks share memory with the API server
# Long-running tasks can consume memory
```

---

## When to Use vs Task Queue

### Use BackgroundTasks When

```python
# 1. Simple, short-lived operations
background_tasks.add_task(send_email, email)

# 2. Non-critical operations
background_tasks.add_task(log_analytics_event, event_data)

# 3. Operations that can afford to be lost on restart
background_tasks.add_task(cleanup_temp_files)

# 4. No need for result tracking
background_tasks.add_task(update_search_index, data)

# 5. Single-server deployment
```

### Use Task Queue (Celery, ARQ) When

```python
# 1. Long-running operations (minutes/hours)
# - Video processing
# - Report generation
# - Data ETL

# 2. Critical operations that must complete
# - Payment processing
# - Order fulfillment
# - Email delivery

# 3. Need result tracking
# - User waiting for report
# - Async task status

# 4. Distributed execution needed
# - Multiple worker processes
# - Multiple servers

# 5. Need retry mechanisms
# - Unreliable external services
# - Network operations

# 6. Need task scheduling
# - Cron jobs
# - Delayed tasks

# 7. Need monitoring
# - Task success/failure rates
# - Processing times
# - Queue depths
```

### Decision Matrix

| Feature | BackgroundTasks | Celery/ARQ |
|---------|----------------|------------|
| Setup complexity | Low | High |
| Result tracking | No | Yes |
| Retry mechanism | Manual | Built-in |
| Distributed | No | Yes |
| Monitoring | No | Yes |
| Scheduling | No | Yes |
| Memory usage | Shared | Separate |
| Persistence | No | Yes |
| Scalability | Limited | High |

---

## Best Practices

### 1. Keep Tasks Small and Fast

```python
# GOOD: Quick task
def send_email(to: str, subject: str):
    smtp.send(to, subject)

# BAD: Heavy task
def process_video(video_id: int):
    # This blocks the worker for minutes
    transcode_video(video_id)
    generate_thumbnails(video_id)
    update_metadata(video_id)
```

### 2. Handle Exceptions Gracefully

```python
def safe_task(data: dict):
    try:
        process(data)
    except Exception as e:
        logger.error(f"Task failed: {e}")
        # Send alert if critical
```

### 3. Pass Immutable Data

```python
# GOOD: Pass copies
background_tasks.add_task(process, data.copy())

# BAD: Pass references that might change
background_tasks.add_task(process, shared_data)
```

### 4. Use Appropriate Task Queue for Critical Operations

```python
# For email sending, payment processing, etc.
# Use Celery or ARQ, not BackgroundTasks
```

### 5. Log Task Execution

```python
def logged_task(data: dict):
    logger.info(f"Starting task with data: {data}")
    result = process(data)
    logger.info(f"Task completed: {result}")
```

### 6. Set Timeouts

```python
import signal

def task_with_timeout(data: dict, timeout: int = 30):
    def timeout_handler(signum, frame):
        raise TimeoutError("Task timed out")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)

    try:
        process(data)
    finally:
        signal.alarm(0)
```

---

## Interview Questions

### Q1: What are FastAPI BackgroundTasks?
**Answer:** BackgroundTasks is a built-in FastAPI feature that runs functions after the response is sent to the client. It's useful for simple, short-lived operations like sending emails or logging events.

### Q2: How do you add a background task in FastAPI?
**Answer:** Inject `BackgroundTasks` as a dependency and call `background_tasks.add_task(func, *args, **kwargs)`. The task runs after the response is sent.

### Q3: What are the limitations of BackgroundTasks?
**Answer:** No result tracking, no progress reporting, no cancellation, no distributed execution, no built-in retry, no priority, and tasks share memory with the API server.

### Q4: When should you use BackgroundTasks vs Celery?
**Answer:** Use BackgroundTasks for simple, non-critical, short-lived operations. Use Celery for long-running, critical, or distributed tasks that need result tracking and retries.

### Q5: Can BackgroundTasks run async functions?
**Answer:** Yes, BackgroundTasks supports both sync and async functions. Async functions are awaited in the event loop.

### Q6: What happens if a background task fails?
**Answer:** The exception is logged but doesn't affect the response (already sent). There's no built-in retry mechanism. You must handle exceptions manually.

### Q7: Can you get the result of a background task?
**Answer:** No, BackgroundTasks doesn't provide result tracking. For results, use a task queue like Celery or ARQ.

### Q8: How do you pass dependencies to background tasks?
**Answer:** Pass dependency values as arguments when adding the task. Don't try to inject dependencies directly since the task runs outside the request context.

### Q9: Can background tasks access the database?
**Answer:** Yes, but create a new database connection inside the task. The request's database session is closed after the response is sent.

### Q10: Do background tasks run in a separate process?
**Answer:** No, they run in the same process as the API server, just after the response is sent. This is why they're not suitable for CPU-intensive or long-running tasks.

### Q11: Can you cancel a background task?
**Answer:** No, there's no built-in cancellation mechanism. Once added, the task runs to completion. For cancellable tasks, use a task queue.

### Q12: How do you handle task failures with retry?
**Answer:** Implement retry logic manually in the task function using loops and sleep. For built-in retry, use Celery or ARQ.

### Q13: Can background tasks send data back to the client?
**Answer:** No, the response is already sent. For results the client needs, use WebSockets, Server-Sent Events, or polling with a task queue.

### Q14: What's the best practice for error handling in background tasks?
**Answer:** Wrap task logic in try/except, log errors, handle gracefully, and don't let exceptions propagate. For critical tasks, implement retry logic or use a task queue.

### Q15: Can you schedule background tasks to run later?
**Answer:** No, BackgroundTasks runs tasks immediately after the response. For delayed or scheduled tasks, use Celery Beat, ARQ cron, or APScheduler.

### Q16: How do you test background tasks?
**Answer:** Use `TestClient` and verify side effects (database changes, emails sent). Mock external services. Some testing frameworks support synchronous background task execution.

### Q17: Do background tasks affect API response time?
**Answer:** No, they run after the response is sent. However, they consume resources (CPU, memory) on the same server, which can affect overall performance.

### Q18: Can you use BackgroundTasks in dependency injection?
**Answer:** Yes, inject `BackgroundTasks` in any dependency function. The tasks will still run after the response is sent.

### Q19: How do you handle large data in background tasks?
**Answer:** Pass file paths or database IDs instead of large data objects. The task can then fetch the data as needed.

### Q20: What happens if the server crashes during a background task?
**Answer:** The task is lost. BackgroundTasks doesn't persist tasks. For critical tasks, use a persistent task queue like Celery with a broker.

### Q21: Can multiple background tasks run concurrently?
**Answer:** In FastAPI, BackgroundTasks tasks run sequentially (one after another). For concurrent execution, use asyncio tasks or a task queue.

### Q22: How do you implement task progress tracking?
**Answer:** BackgroundTasks doesn't support progress tracking. Use a database, Redis, or WebSocket to track progress manually, or use a task queue with result tracking.

### Q23: Can you use BackgroundTasks with StreamingResponse?
**Answer:** Yes, but be aware that background tasks run after the streaming response completes, not after the initial response headers are sent.

### Q24: What are alternatives to FastAPI BackgroundTasks?
**Answer:** Celery (feature-rich, distributed), ARQ (async, Redis-based), Huey (simple, Redis), RQ (Redis Queue), and custom asyncio tasks for simple cases.

### Q25: How do you implement a job queue without external dependencies?
**Answer:** Use asyncio.Queue with worker coroutines. Add tasks to the queue, and workers process them concurrently. This is simple but not persistent or distributed.
