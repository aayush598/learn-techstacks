# ARQ (Async Redis Queue) with FastAPI

## Table of Contents
1. [What is ARQ?](#what-is-arq)
2. [ARQ Setup](#arq-setup)
3. [Redis Queue Configuration](#redis-queue-configuration)
4. [Defining Tasks](#defining-tasks)
5. [Job Scheduling](#job-scheduling)
6. [Cron Jobs](#cron-jobs)
7. [Job Result Handling](#job-result-handling)
8. [Retry Strategies](#retry-strategies)
9. [Worker Management](#worker-management)
10. [ARQ vs Celery](#arq-vs-celery)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## What is ARQ?

ARQ (Async Redis Queue) is a lightweight, async task queue for Python using Redis. It's designed for asyncio and integrates naturally with FastAPI.

### Key Features

- **Async-first**: Built on asyncio
- **Lightweight**: Minimal dependencies
- **Redis-based**: Uses Redis for queuing and results
- **Built-in retry**: Automatic retry with configurable strategies
- **Cron support**: Built-in periodic task scheduling
- **FastAPI integration**: Natural fit for async applications

---

## ARQ Setup

### Installation

```bash
pip install arq
```

### Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── worker.py
│   ├── tasks.py
│   └── cron.py
├── worker.py  # Entry point for worker
└── requirements.txt
```

### Worker Configuration

```python
# worker.py (entry point)
from arq import create_pool
from arq.connections import RedisSettings
from app.worker import WorkerSettings

if __name__ == "__main__":
    from arq.worker import run_worker
    run_worker(WorkerSettings)
```

### WorkerSettings

```python
# app/worker.py
from arq.connections import RedisSettings
from app.tasks import send_email, process_data
from app.cron import daily_report

class WorkerSettings:
    functions = [send_email, process_data]
    cron_jobs = [daily_report]
    redis_settings = RedisSettings(host="localhost", port=6379, database=0)
    max_jobs = 10
    job_timeout = 300  # 5 minutes
    keep_result = 3600  # Keep results for 1 hour
    health_check_interval = 10
```

---

## Redis Queue Configuration

### RedisSettings

```python
from arq.connections import RedisSettings

# Basic settings
redis_settings = RedisSettings(
    host="localhost",
    port=6379,
    database=0,
    password=None,
    ssl=None,
    conn_timeout=5,
    conn_retries=5,
    retry_delay=1,
)

# Connection pool settings
redis_settings = RedisSettings(
    host="redis-cluster.example.com",
    port=6380,
    database=0,
    password="secret",
    ssl=True,
)
```

### Multiple Queues

```python
class WorkerSettings:
    functions = [send_email, process_data]
    redis_settings = RedisSettings(host="localhost", port=6379)

    # Queue name for this worker
    queue_name = "arq:default"

# Different workers can consume from different queues
class EmailWorkerSettings:
    functions = [send_email]
    queue_name = "arq:emails"

class DataWorkerSettings:
    functions = [process_data]
    queue_name = "arq:data"
```

---

## Defining Tasks

### Basic Tasks

```python
# app/tasks.py
from arq import cron
from arq.connections import RedisSettings
from pydantic import BaseModel

async def send_email(ctx, to: str, subject: str, body: str) -> dict:
    """Send an email."""
    # ctx is the job context with redis connection
    print(f"Sending email to {to}")

    # Simulate email sending
    await asyncio.sleep(1)

    return {"status": "sent", "to": to, "subject": subject}

async def process_data(ctx, data_id: int) -> dict:
    """Process data asynchronously."""
    # Access redis from context
    redis = ctx["redis"]

    # Update progress
    await redis.set(f"progress:{data_id}", "50%")

    # Process
    result = await do_processing(data_id)

    await redis.set(f"progress:{data_id}", "100%")
    return {"data_id": data_id, "result": result}
```

### Task with Context

```python
async def task_with_context(ctx, user_id: int):
    # ctx contains:
    # - "redis": Redis connection
    # - "job_id": Current job ID
    # - "job_try": Current attempt number
    # - "max_retries": Maximum retry count

    redis = ctx["redis"]
    job_id = ctx["job_id"]

    # Store progress
    await redis.hset(f"job:{job_id}", "status", "processing")

    result = await process_user(user_id)

    await redis.hset(f"job:{job_id}", "status", "completed")
    return result
```

### Task with Dependencies

```python
from app.database import get_db_connection

async def db_task(ctx, user_id: int):
    # Create fresh connection for each task
    db = await get_db_connection()
    try:
        result = await db.fetch_user(user_id)
        return result
    finally:
        await db.close()
```

---

## Job Scheduling

### Enqueue Jobs

```python
from arq import create_pool
from arq.connections import RedisSettings

@app.on_event("startup")
async def startup():
    # Create Redis connection pool
    app.state.redis = await create_pool(RedisSettings())

@app.post("/send-email")
async def send_email_endpoint(to: str, subject: str):
    # Enqueue job
    job = await app.state.redis.enqueue_job(
        "send_email",
        to=to,
        subject=subject,
        body="Hello!",
    )

    return {"job_id": job.job_id, "status": "queued"}

# Delayed jobs
@app.post("/delayed-email")
async def delayed_email(to: str):
    # Send email after 5 minutes
    job = await app.state.redis.enqueue_job(
        "send_email",
        to=to,
        subject="Reminder",
        body="Don't forget!",
        _job_id="custom_id",  # Custom job ID
        _queue_name="arq:emails",  # Specific queue
    )

    return {"job_id": job.job_id}

# Unique jobs (prevent duplicates)
@app.post("/unique-job")
async def unique_job(data_id: int):
    job = await app.state.redis.enqueue_job(
        "process_data",
        data_id,
        _job_id=f"process:{data_id}",  # Unique ID
        _queue_name="arq:data",
    )

    if job is None:
        return {"status": "already_queued"}

    return {"job_id": job.job_id}
```

### Job Options

```python
job = await redis.enqueue_job(
    "task_name",
    arg1, arg2,
    _job_id="custom_id",
    _queue_name="arq:default",
    _job_timeout=300,  # 5 minutes
    _max_tries=3,      # Max retry attempts
    _retry_delay=60,   # Delay between retries
    _keep_result=3600, # Keep result for 1 hour
)
```

---

## Cron Jobs

### Basic Cron Jobs

```python
from arq import cron
from arq.cron import CronJob

async def daily_report(ctx):
    """Generate daily report."""
    report = await generate_report()
    await send_report(report)
    return {"report": "sent"}

async def cleanup_temp_files(ctx):
    """Clean up temporary files."""
    deleted = await cleanup()
    return {"deleted": deleted}

# In WorkerSettings
class WorkerSettings:
    functions = [send_email, process_data]
    cron_jobs = [
        cron(daily_report, hour=8, minute=0),  # Daily at 8 AM
        cron(cleanup_temp_files, hour=2, minute=0),  # Daily at 2 AM
    ]
```

### Cron Schedule Options

```python
from arq import cron

# Every minute
cron(task, minute=None)  # or minute="*"

# Every hour
cron(task, hour=None, minute=0)

# Daily at specific time
cron(task, hour=8, minute=30)

# Weekly on Monday at 9 AM
cron(task, hour=9, minute=0, day_of_week=1)

# Monthly on 1st at midnight
cron(task, hour=0, minute=0, day=1)

# Custom schedule with multiple values
cron(task, minute="*/5")  # Every 5 minutes
cron(task, hour="9-17")   # 9 AM to 5 PM
cron(task, day_of_week="1-5")  # Weekdays only
```

### Dynamic Cron Jobs

```python
@app.post("/schedule-report")
async def schedule_report(time: str):
    hour, minute = map(int, time.split(":"))

    job = cron(daily_report, hour=hour, minute=minute)

    # Add to worker settings dynamically
    # Note: Dynamic cron requires restarting the worker
    return {"scheduled": True, "time": time}
```

---

## Job Result Handling

### Checking Job Status

```python
from arq.worker import JobResult

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    redis = app.state.redis

    # Get job result
    result = await redis.get_result(job_id)

    if result is None:
        return {"job_id": job_id, "status": "unknown"}

    return {
        "job_id": job_id,
        "status": result.status,
        "result": result.result,
        "success": result.success,
        "start_time": result.start_time,
        "end_time": result.end_time,
        "job_try": result.job_try,
    }
```

### Result Storage

```python
# Results are stored in Redis with configurable TTL
class WorkerSettings:
    keep_result = 3600  # Keep results for 1 hour
    keep_result_failure = 86400  # Keep failed results for 24 hours
```

### Cleanup Results

```python
@app.delete("/jobs/{job_id}")
async def delete_job_result(job_id: str):
    redis = app.state.redis
    await redis.delete_job_result(job_id)
    return {"deleted": True}
```

---

## Retry Strategies

### Built-in Retry

```python
async def task_with_retry(ctx, data_id: int):
    # Automatically retry on failure
    pass

class WorkerSettings:
    functions = [task_with_retry]
    max_tries = 3  # Default max retries
    retry_delay = 60  # Default retry delay
```

### Custom Retry

```python
async def task_with_custom_retry(ctx, data_id: int):
    try:
        result = await risky_operation(data_id)
        return result
    except ConnectionError as e:
        # Custom retry logic
        if ctx["job_try"] < 3:
            # Raise to trigger retry
            raise
        # Final attempt failed
        return {"error": str(e)}
```

### Exponential Backoff

```python
from arq.connections import RedisSettings

async def exponential_backoff_task(ctx, data_id: int):
    try:
        return await process(data_id)
    except Exception:
        if ctx["job_try"] < 5:
            # Calculate delay: 2^attempt * base_delay
            delay = (2 ** ctx["job_try"]) * 10  # 20, 40, 80, 160, 320 seconds
            await asyncio.sleep(delay)
            raise
        raise
```

### Task-Specific Retry

```python
async def critical_task(ctx, order_id: int):
    """Critical task with more retries."""
    pass

class WorkerSettings:
    functions = [critical_task]
    # Override per-task retry settings
    job_timeout = 600
    max_tries = 5
```

---

## Worker Management

### Starting Workers

```bash
# Basic worker
arq app.worker.WorkerSettings

# Multiple workers
arq app.worker.WorkerSettings --workers 4

# With custom settings
arq app.worker.WorkerSettings --max-jobs 10 --job-timeout 300
```

### Worker Configuration

```python
class WorkerSettings:
    functions = [send_email, process_data]
    redis_settings = RedisSettings()

    # Worker settings
    max_jobs = 10          # Max concurrent jobs per worker
    job_timeout = 300      # Max job duration (seconds)
    health_check_interval = 10  # Health check interval
    health_check_key = "arq:health-check"

    # Queue settings
    queue_read = True      # Read from queue
    queue_name = "arq:default"

    # Result settings
    keep_result = 3600
    keep_result_failure = 86400
```

### Monitoring Workers

```python
@app.get("/worker/status")
async def worker_status():
    redis = app.state.redis

    # Get queue info
    queue_length = await redis.llen("arq:default")

    # Get job info
    job_ids = await redis.lrange("arq:default", 0, -1)

    return {
        "queue_length": queue_length,
        "pending_jobs": len(job_ids),
    }
```

### Graceful Shutdown

```python
@app.on_event("shutdown")
async def shutdown():
    # Close Redis connection
    await app.state.redis.close()
```

---

## ARQ vs Celery

### Comparison Table

| Feature | ARQ | Celery |
|---------|-----|--------|
| Async support | Native | Through eventlet/gevent |
| Dependencies | Minimal (redis) | More (redis/rabbitmq, kombu, etc.) |
| Setup complexity | Simple | Complex |
| Task routing | Basic | Advanced |
| Result backends | Redis only | Multiple (Redis, DB, RPC) |
| Monitoring | Basic | Flower (rich) |
| Cron jobs | Built-in | Celery Beat |
| Community | Smaller | Large |
| Features | Core features | Feature-rich |

### When to Use ARQ

```python
# Use ARQ when:
# 1. You're already using FastAPI (async)
# 2. You want simplicity
# 3. Redis is your only message broker
# 4. You don't need advanced routing
# 5. You want minimal dependencies
```

### When to Use Celery

```python
# Use Celery when:
# 1. You need advanced task routing
# 2. You need multiple broker support
# 3. You need rich monitoring (Flower)
# 4. You have complex workflow requirements
# 5. You need larger community support
```

---

## Best Practices

### 1. Use Connection Pooling

```python
# Create connection pool on startup
@app.on_event("startup")
async def startup():
    app.state.redis = await create_pool(RedisSettings())

@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()
```

### 2. Set Appropriate Timeouts

```python
class WorkerSettings:
    job_timeout = 300      # 5 minutes max per job
    keep_result = 3600     # Keep results for 1 hour
    max_jobs = 10          # Limit concurrent jobs
```

### 3. Handle Failures Gracefully

```python
async def robust_task(ctx, data_id: int):
    try:
        return await process(data_id)
    except Exception as e:
        logger.error(f"Task failed: {e}")
        # Store failure info
        await ctx["redis"].hset(f"job:{ctx['job_id']}", "error", str(e))
        raise
```

### 4. Use Unique Job IDs

```python
# Prevent duplicate jobs
job = await redis.enqueue_job(
    "process_order",
    order_id,
    _job_id=f"order:{order_id}",  # Unique ID
)
```

### 5. Monitor Queue Depth

```python
@app.get("/queue-stats")
async def queue_stats():
    redis = app.state.redis
    queue_length = await redis.llen("arq:default")
    return {"queue_depth": queue_length}
```

---

## Interview Questions

### Q1: What is ARQ and why use it?
**Answer:** ARQ is an async Redis-based task queue for Python. It's lightweight, has minimal dependencies, and integrates naturally with FastAPI's async ecosystem.

### Q2: How does ARQ differ from Celery?
**Answer:** ARQ is async-native, simpler, and has fewer dependencies. Celery is more feature-rich with advanced routing, multiple brokers, and better monitoring. ARQ is better for async-first applications.

### Q3: What is the ARQ worker context?
**Answer:** The context (`ctx`) is a dictionary passed to tasks containing the Redis connection, job ID, job try count, and max retries. It provides access to Redis for storing progress and results.

### Q4: How do you schedule cron jobs in ARQ?
**Answer:** Use `cron()` in the WorkerSettings `cron_jobs` list. Specify schedule with `hour`, `minute`, `day`, `day_of_week` parameters.

### Q5: How does ARQ handle retries?
**Answer:** ARQ retries failed tasks up to `max_tries` times with `retry_delay` between attempts. Tasks can implement custom retry logic using `ctx["job_try"]`.

### Q6: Can ARQ run tasks in parallel?
**Answer:** Yes, workers run tasks concurrently using asyncio. The `max_jobs` setting controls how many tasks a worker processes simultaneously.

### Q7: What happens if a worker crashes?
**Answer:** Jobs in the queue remain and are picked up by other workers. Jobs being processed may be lost unless you implement heartbeat checking.

### Q8: How do you monitor ARQ workers?
**Answer:** Check queue length with `redis.llen()`. Use health check keys. Implement custom monitoring endpoints. ARQ has fewer built-in monitoring tools than Celery.

### Q9: What is the `_job_id` parameter?
**Answer:** A custom job ID to prevent duplicate jobs. If a job with the same ID is already queued, `enqueue_job` returns None instead of creating a duplicate.

### Q10: How do you pass data to ARQ tasks?
**Answer:** Pass data as positional or keyword arguments to `enqueue_job()`. The worker passes them to the task function along with the context.

### Q11: What is the difference between `keep_result` and `keep_result_failure`?
**Answer:** `keep_result` controls how long successful results are stored. `keep_result_failure` controls how long failed job results are stored. Failed results typically need longer retention.

### Q12: How do you implement unique job processing?
**Answer:** Use `_job_id` with a unique identifier (e.g., `f"order:{order_id}"`). `enqueue_job` returns None if a job with that ID already exists in the queue.

### Q13: Can ARQ use brokers other than Redis?
**Answer:** No, ARQ is specifically designed for Redis. For other brokers, use Celery or another task queue.

### Q14: How do you handle large payloads in ARQ?
**Answer:** Store large data in Redis or a database and pass the key to the task. The task fetches the data when needed. Avoid passing large objects directly.

### Q15: What is the health check in ARQ?
**Answer:** Workers set a health check key in Redis at regular intervals. If the key expires, the worker is considered unhealthy. This helps detect worker failures.

### Q16: How do you deploy ARQ workers?
**Answer:** Use `arq app.worker.WorkerSettings` command. In Docker, run as a separate service. Use systemd or supervisor for process management.

### Q17: How do you implement task progress tracking?
**Answer:** Use Redis to store progress (e.g., `redis.hset(f"job:{job_id}", "progress", "50%")`). Query the progress from a separate endpoint.

### Q18: What is the difference between `max_jobs` and worker concurrency?
**Answer:** `max_jobs` limits how many tasks a worker processes simultaneously. With asyncio, this is cooperative concurrency. With multiple workers, each has its own `max_jobs` limit.

### Q19: How do you handle task timeouts in ARQ?
**Answer:** Set `job_timeout` in WorkerSettings. Tasks that exceed the timeout are killed. Use `ctx["job_try"]` to check if a task is being retried after timeout.

### Q20: Can ARQ and Celery coexist?
**Answer:** Yes, they can share the same Redis instance but use different queue names. However, it's usually better to choose one task queue to avoid confusion.
