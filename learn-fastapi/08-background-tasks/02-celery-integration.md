# Celery Integration with FastAPI

## Table of Contents
1. [What is Celery?](#what-is-celery)
2. [Celery Setup with FastAPI](#celery-setup-with-fastapi)
3. [Celery Configuration](#celery-configuration)
4. [Defining Tasks](#defining-tasks)
5. [Groups](#groups)
6. [Chains](#chains)
7. [Chord](#chord)
8. [Canvas Primitives](#canvas-primitives)
9. [Result Backends](#result-backends)
10. [Task Retry](#task-retry)
11. [Rate Limiting Tasks](#rate-limiting-tasks)
12. [Monitoring with Flower](#monitoring-with-flower)
13. [Celery + Docker](#celery--docker)
14. [Best Practices](#best-practices)
15. [Interview Questions](#interview-questions)

---

## What is Celery?

Celery is a distributed task queue that allows you to run tasks asynchronously across multiple workers. It supports multiple message brokers (RabbitMQ, Redis) and result backends.

### Key Concepts

- **Broker**: Message broker that receives and stores tasks (Redis, RabbitMQ)
- **Worker**: Process that executes tasks
- **Result Backend**: Stores task results (Redis, database, RPC)
- **Task**: Python function decorated with `@celery.task`
- **Queue**: Named queue where tasks are sent
- **Beat**: Scheduler for periodic tasks

---

## Celery Setup with FastAPI

### Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── celery_app.py
│   ├── tasks.py
│   └── models.py
├── docker-compose.yml
└── requirements.txt
```

### Celery App Configuration

```python
# celery_app.py
from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes
    task_soft_time_limit=270,  # 4.5 minutes (raises SoftTimeLimitExceeded)
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
)

# Auto-discover tasks
celery_app.autodiscover_tasks(["app"])
```

### FastAPI Integration

```python
# main.py
from fastapi import FastAPI
from app.celery_app import celery_app
from app.tasks import process_data

app = FastAPI()

@app.post("/process")
async def start_processing(data: dict):
    # Send task to Celery
    task = process_data.delay(data["id"], data["params"])

    return {
        "task_id": task.id,
        "status": "queued",
        "check_status_url": f"/tasks/{task.id}"
    }

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    result = celery_app.AsyncResult(task_id)

    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }
```

---

## Celery Configuration

### Environment-Based Configuration

```python
# config.py
from celery import Celery
import os

class CeleryConfig:
    # Broker
    broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

    # Result Backend
    result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

    # Serialization
    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]

    # Timezone
    timezone = "UTC"
    enable_utc = True

    # Task Settings
    task_track_started = True
    task_time_limit = 300
    task_soft_time_limit = 270
    task_acks_late = True  # Acknowledge after task completes
    task_reject_on_worker_lost = True

    # Worker Settings
    worker_prefetch_multiplier = 1
    worker_max_tasks_per_child = 100
    worker_concurrency = 4

    # Queue Settings
    task_routes = {
        "app.tasks.email_*": {"queue": "emails"},
        "app.tasks.report_*": {"queue": "reports"},
        "app.tasks.default_*": {"queue": "default"},
    }

    # Retry Settings
    task_default_retry_delay = 60
    task_max_retries = 3

# Apply config
celery_app = Celery("worker")
celery_app.config_from_object(CeleryConfig)
```

### Multiple Queues

```python
from kombu import Queue

celery_app.conf.task_queues = (
    Queue("default", routing_key="default"),
    Queue("emails", routing_key="emails"),
    Queue("reports", routing_key="reports"),
    Queue("priority", routing_key="priority"),
)

celery_app.conf.task_default_queue = "default"
```

---

## Defining Tasks

### Basic Tasks

```python
# tasks.py
from app.celery_app import celery_app
import time

@celery_app.task
def add(x: int, y: int) -> int:
    return x + y

@celery_app.task
def process_item(item_id: int) -> dict:
    # Simulate processing
    time.sleep(2)
    return {"item_id": item_id, "status": "processed"}
```

### Task with Name

```python
@celery_app.task(name="app.tasks.send_email")
def send_email(to: str, subject: str, body: str):
    # Send email
    print(f"Sending email to {to}")
    return {"status": "sent", "to": to}
```

### Task with Bind (Access Self)

```python
@celery_app.task(bind=True)
def retry_task(self, data: dict):
    try:
        # Process data
        return {"status": "success"}
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60, max_retries=3)
```

### Task with Rate Limit

```python
@celery_app.task(rate_limit="10/m")  # 10 tasks per minute
def api_call(url: str):
    response = requests.get(url)
    return response.json()
```

### Task with Time Limit

```python
@celery_app.task(time_limit=300, soft_time_limit=270)
def long_running_task(data: dict):
    # Must complete within 5 minutes
    # Soft limit at 4.5 minutes raises SoftTimeLimitExceeded
    process(data)
```

### Task with Ignore Result

```python
@celery_app.task(ignore_result=True)
def fire_and_forget(data: dict):
    # Don't need to track the result
    process(data)
```

---

## Groups

### What is a Group?

A group sends the same task to multiple arguments in parallel.

```python
from celery import group

# Send task to multiple items in parallel
job = group(
    process_item.s(item_id) for item_id in range(100)
)
result = job.apply_async()

# Wait for all tasks to complete
results = result.get(timeout=60)
```

### Group Example

```python
@app.post("/process-batch")
async def process_batch(item_ids: list[int]):
    # Create group of tasks
    job = group(process_item.s(item_id) for item_id in item_ids)
    result = job.apply_async()

    return {
        "group_id": result.id,
        "total_tasks": len(item_ids),
        "status": "processing"
    }

@app.get("/batch/{group_id}")
async def get_batch_status(group_id: str):
    result = celery_app.GroupResult.restore(group_id)
    return {
        "group_id": group_id,
        "total": len(result.results),
        "completed": sum(1 for r in result.results if r.ready()),
        "successful": sum(1 for r in result.results if r.successful()),
    }
```

### Parallel Processing with Groups

```python
@app.post("/process-all")
async def process_all(items: list[dict]):
    # Process items in parallel batches
    batch_size = 10
    batches = [
        group(process_item.s(item) for item in items[i:i+batch_size])
        for i in range(0, len(items), batch_size)
    ]

    # Execute batches sequentially
    results = []
    for batch in batches:
        result = batch.apply_async()
        results.append(result)

    return {"batches": len(results), "total_items": len(items)}
```

---

## Chains

### What is a Chain?

A chain passes the result of one task to the next task in sequence.

```python
from celery import chain

# Chain tasks: output of one becomes input of next
job = chain(
    fetch_data.s(url),
    process_data.s(),
    save_results.s()
)
result = job.apply_async()
```

### Chain Example

```python
@celery_app.task
def fetch_data(url: str) -> dict:
    response = requests.get(url)
    return response.json()

@celery_app.task
def process_data(data: dict) -> dict:
    # Process the fetched data
    processed = transform(data)
    return processed

@celery_app.task
def save_results(processed_data: dict) -> str:
    # Save to database
    db.save(processed_data)
    return "saved"

# Chain them together
pipeline = chain(
    fetch_data.s("https://api.example.com/data"),
    process_data.s(),
    save_results.s()
)
result = pipeline.apply_async()
```

### Chain with Callbacks

```python
@celery_app.task
def on_success(result):
    print(f"Pipeline completed: {result}")

@celery_app.task
def on_failure(exc):
    print(f"Pipeline failed: {exc}")

# Chain with error handling
pipeline = chain(
    fetch_data.s(url),
    process_data.s(),
    save_results.s()
)

result = pipeline.apply_async()
```

---

## Chord

### What is a Chord?

A chord is a group followed by a callback that runs after all group tasks complete.

```python
from celery import chord

# Run group of tasks, then callback with all results
job = chord(
    [process_item.s(item_id) for item_id in range(100)],
    callback=finalize.s()
)
result = job.apply_async()
```

### Chord Example

```python
@celery_app.task
def process_item(item_id: int) -> dict:
    # Process individual item
    return {"item_id": item_id, "result": "processed"}

@celery_app.task
def finalize(results: list) -> dict:
    # Runs after all items are processed
    total = len(results)
    successful = sum(1 for r in results if r.get("status") == "processed")
    return {"total": total, "successful": successful}

@app.post("/process-all")
async def process_all():
    # Process 100 items, then finalize
    job = chord(
        [process_item.s(i) for i in range(100)],
        callback=finalize.s()
    )
    result = job.apply_async()

    return {"chord_id": result.id}
```

### Chord with Error Handling

```python
@celery_app.task
def on_chord_error(exc):
    print(f"Chord failed: {exc}")

# Add error callback
job = chord(
    [process_item.s(i) for i in range(100)],
    callback=finalize.s()
)
result = job.apply_error_callback(on_chord_error).apply_async()
```

---

## Canvas Primitives

### Signature (.s)

```python
# Create a task signature without executing
task_signature = process_item.s(item_id)
# Execute later
task_signature.apply_async()
```

### group

```python
# Parallel execution
from celery import group
g = group(task.s(i) for i in range(10))
g.apply_async()
```

### chain

```python
# Sequential execution
from celery import chain
c = chain(task1.s(), task2.s(), task3.s())
c.apply_async()
```

### chord

```python
# Parallel + callback
from celery import chord
c = chord([task.s(i) for i in range(10)], callback=finalize.s())
c.apply_async()
```

### chunks

```python
# Split large tasks into chunks
from celery import chunks

# Process 1000 items in chunks of 100
task.chunks(range(1000), 100).apply_async()
```

### maps

```python
# Map function across arguments
from celery import map

result = process_item.map(range(100)).apply_async()
```

---

## Result Backends

### Redis Backend

```python
celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

# Result settings
celery_app.conf.update(
    result_expires=3600,  # Results expire after 1 hour
    result_persistent=True,  # Persist results to disk
    result_backend_transport_options={
        "master_name": "mymaster",
        "visibility_timeout": 43200,
    }
)
```

### RPC Backend

```python
# Uses RabbitMQ for results (not recommended for large results)
celery_app = Celery(
    "worker",
    broker="amqp://guest:guest@localhost:5672//",
    backend="rpc://",
)
```

### Database Backend

```python
# Using SQLAlchemy
celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="db+sqlite:///results.db",
)
```

### Getting Results

```python
from celery.result import AsyncResult

@app.get("/tasks/{task_id}")
async def get_result(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "status": result.status,
    }

    if result.ready():
        response["result"] = result.result
        response["successful"] = result.successful()
        if not result.successful():
            response["error"] = str(result.result)

    return response
```

---

## Task Retry

### Manual Retry

```python
@celery_app.task(bind=True, max_retries=3)
def send_email(self, to: str, subject: str):
    try:
        smtp_send(to, subject)
    except SMTPException as exc:
        # Retry with exponential backoff
        raise self.retry(
            exc=exc,
            countdown=60 * (2 ** self.request.retries),  # 60s, 120s, 240s
            max_retries=3,
        )
```

### Automatic Retry

```python
@celery_app.task(
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_kwargs={"max_retries": 5},
)
def unreliable_api_call(url: str):
    response = requests.get(url, timeout=10)
    return response.json()
```

### Retry with Callback

```python
@celery_app.task(bind=True)
def task_with_retry_callback(self, data: dict):
    try:
        process(data)
    except Exception as exc:
        self.retry(exc=exc, countdown=60)
        # After max retries, the task fails
        # Handle failure in the caller
```

---

## Rate Limiting Tasks

### Task-Level Rate Limits

```python
@celery_app.task(rate_limit="10/m")  # 10 per minute
def api_call(url: str):
    return requests.get(url)

@celery_app.task(rate_limit="100/h")  # 100 per hour
def limited_task(data: dict):
    process(data)
```

### Dynamic Rate Limits

```python
@app.post("/configure-rate-limit")
async def configure_rate_limit(task_name: str, rate_limit: str):
    # Dynamically set rate limit for a task
    celery_app.control.rate_limit(task_name, rate_limit)
    return {"task": task_name, "rate_limit": rate_limit}
```

### Rate Limit Formats

```python
# Tasks per second
@celery_app.task(rate_limit="10/s")

# Tasks per minute
@celery_app.task(rate_limit="100/m")

# Tasks per hour
@celery_app.task(rate_limit="1000/h")
```

---

## Monitoring with Flower

### Setup

```python
# Install: pip install flower
# Run: flower -A app.celery_app --port=5555
```

### Docker Setup

```yaml
services:
  flower:
    image: mher/flower
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    ports:
      - "5555:5555"
    depends_on:
      - redis
```

### Flower API

```python
import httpx

@app.get("/flower/tasks")
async def get_flower_tasks():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://flower:5555/api/tasks")
        return response.json()

@app.get("/flower/workers")
async def get_flower_workers():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://flower:5555/api/workers")
        return response.json()
```

---

## Celery + Docker

### docker-compose.yml

```yaml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      - redis
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000

  worker:
    build: .
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      - redis
    command: celery -A app.celery_app worker --loglevel=info

  beat:
    build: .
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      - redis
    command: celery -A app.celery_app beat --loglevel=info

  flower:
    build: .
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    ports:
      - "5555:5555"
    depends_on:
      - redis
    command: celery -A app.celery_app flower --port=5555

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

### Production Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD celery -A app.celery_app inspect ping

CMD ["celery", "-A", "app.celery_app", "worker", "--loglevel=info"]
```

---

## Best Practices

### 1. Use Separate Queues for Different Task Types

```python
celery_app.conf.task_routes = {
    "app.tasks.email_*": {"queue": "emails"},
    "app.tasks.report_*": {"queue": "reports"},
}
```

### 2. Set Appropriate Time Limits

```python
@celery_app.task(time_limit=300, soft_time_limit=270)
def task_with_timeout(data: dict):
    process(data)
```

### 3. Use Ack Late for Critical Tasks

```python
# Acknowledge after task completes, not before
celery_app.conf.task_acks_late = True
```

### 4. Monitor Worker Health

```python
@app.get("/worker-health")
async def worker_health():
    inspect = celery_app.control.inspect()
    stats = inspect.stats()
    return {"workers": stats}
```

### 5. Implement Dead Letter Queues

```python
# Move failed tasks to a dead letter queue
@celery_app.task(bind=True)
def task_with_dlq(self, data: dict):
    try:
        process(data)
    except Exception as exc:
        if self.request.retries >= self.max_retries:
            # Send to dead letter queue
            dead_letter.s(data, str(exc)).apply_async()
            return
        raise self.retry(exc=exc, countdown=60)
```

---

## Interview Questions

### Q1: What is Celery and why use it with FastAPI?
**Answer:** Celery is a distributed task queue for running tasks asynchronously. FastAPI's built-in BackgroundTasks is limited to single-process, non-persistent tasks. Celery provides distributed execution, result tracking, retries, and monitoring.

### Q2: What is a Celery broker?
**Answer:** A broker (Redis, RabbitMQ) receives and stores tasks in a queue. Workers poll the broker for new tasks and execute them. The broker decouples task submission from execution.

### Q3: What is the difference between .delay() and .apply_async()?
**Answer:** `.delay()` is a shortcut for `.apply_async()` with default options. `.apply_async()` allows specifying queue, countdown, eta, and other options.

### Q4: What is a Celery worker?
**Answer:** A worker is a process that polls the broker for tasks and executes them. Multiple workers can run on the same or different machines for parallel processing.

### Q5: What are Celery groups, chains, and chords?
**Answer:** Groups run tasks in parallel. Chains pass results sequentially from one task to the next. Chords run a group of tasks and execute a callback when all complete.

### Q6: What is the difference between Redis and RabbitMQ as a broker?
**Answer:** Redis is simpler, faster, and easier to set up. RabbitMQ is more feature-rich with better routing and reliability guarantees. Redis is sufficient for most use cases.

### Q7: How do you handle task failures in Celery?
**Answer:** Use `max_retries` and `retry()` for automatic retries. Implement exponential backoff. Use dead letter queues for permanently failed tasks. Monitor failures with Flower.

### Q8: What is Flower and why use it?
**Answer:** Flower is a web-based monitoring tool for Celery. It shows worker status, task results, success/failure rates, and allows you to inspect and control workers.

### Q9: What is the difference between task_acks_late and default acknowledgment?
**Answer:** Default acknowledgment happens when the worker receives the task. `acks_late` acknowledges after the task completes. This prevents task loss if a worker crashes mid-execution.

### Q10: How do you set up Celery with Docker?
**Answer:** Use docker-compose with separate services for the API, Celery worker, Celery beat (scheduler), Flower, and the broker (Redis). Each service shares the same codebase but runs different commands.

### Q11: What is Celery Beat?
**Answer:** Celery Beat is a scheduler that sends periodic tasks to the broker at specified intervals. It's used for cron-like tasks (daily reports, cleanup, etc.).

### Q12: How do you implement task prioritization in Celery?
**Answer:** Use multiple queues with different priorities. Configure workers to consume from queues in priority order. Higher priority queues are consumed first.

### Q13: What is a task result backend?
**Answer:** A backend (Redis, database, RPC) that stores task results. Workers write results after task completion. Clients can retrieve results using the task ID.

### Q14: How do you handle long-running tasks?
**Answer:** Set appropriate `time_limit` and `soft_time_limit`. Use `acks_late` to prevent task loss. Implement progress tracking using a database or Redis.

### Q15: What is the difference between .s() and .delay()?
**Answer:** `.s()` creates a signature (task + args) without executing. `.delay()` creates a signature and executes it immediately. Signatures are used for chaining and grouping.

### Q16: How do you implement rate limiting in Celery?
**Answer:** Use the `rate_limit` parameter on tasks (e.g., `@celery.task(rate_limit="10/m")`). Celery controls the rate at the worker level.

### Q17: What happens if a worker crashes during task execution?
**Answer:** With default acknowledgment, the task is lost. With `acks_late=True`, the task is requeued and another worker picks it up. This is why `acks_late` is recommended for critical tasks.

### Q18: How do you scale Celery workers?
**Answer:** Add more worker processes on the same machine (increase concurrency) or add more machines running workers. Celery handles distribution automatically via the broker.

### Q19: What is a Celery chord?
**Answer:** A chord is a group of tasks followed by a callback. The callback runs after all group tasks complete, receiving their results as input.

### Q20: How do you test Celery tasks?
**Answer:** Use `CELERY_TASK_ALWAYS_EAGER=True` to run tasks synchronously in tests. Mock external services. Use `celery_app.control.purge()` to clear test tasks.
