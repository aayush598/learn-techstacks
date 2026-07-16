# Background Tasks Interview Questions

## Table of Contents
1. [FastAPI BackgroundTasks](#fastapi-backgroundtasks)
2. [Task Queue Concepts](#task-queue-concepts)
3. [Celery](#celery)
4. [ARQ](#arq)
5. [Task Retry & Failure Patterns](#task-retry--failure-patterns)
6. [Dead Letter Queues](#dead-letter-queues)
7. [Task Prioritization & Routing](#task-prioritization--routing)
8. [Monitoring & Observability](#monitoring--observability)
9. [Scaling Workers](#scaling-workers)
10. [Idempotency & Task Ordering](#idempotency--task-ordering)
11. [Architecture & Design](#architecture--design)

---

## FastAPI BackgroundTasks

### Q1: What are FastAPI BackgroundTasks and when should you use them?
**Answer:** BackgroundTasks is FastAPI's built-in mechanism for running functions after the response is sent to the client. It runs tasks in the same process as the API server.

**Use BackgroundTasks when:**
- Task is simple and short-lived (< 10 seconds)
- Task is non-critical (email, logging, analytics)
- No result tracking needed
- Single-server deployment
- No retry logic needed

**Do NOT use BackgroundTasks when:**
- Task is long-running (> 30 seconds)
- Task needs retry logic or failure handling
- Task needs to be tracked or monitored
- Multiple servers need to process tasks
- Task needs to survive server restarts

```python
from fastapi import BackgroundTasks

@app.post("/send-notification")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, subject="Welcome!", body="Hello!")
    return {"message": "Notification queued"}
```

### Q2: What are the critical limitations of BackgroundTasks?
**Answer:**

| Limitation | Impact | Workaround |
|-----------|--------|------------|
| No result tracking | Can't check if task succeeded | Use task queue |
| No retry on failure | Failed tasks are lost | Use Celery/ARQ |
| No distributed execution | Single-server only | Use task queue |
| No persistence | Lost on server restart | Use task queue |
| No cancellation | Can't stop running tasks | Use task queue |
| No progress reporting | Can't show progress to users | Use task queue |
| Runs in same process | Blocks if CPU-intensive | Use task queue |
| No scheduling | Can't delay or cron-schedule | Use Celery Beat |
| No priority | All tasks equal | Use task queue |

### Q3: Can BackgroundTasks run async functions and what are the implications?
**Answer:** Yes, BackgroundTasks supports both sync and async functions. Async functions run in the event loop — if they block, they block ALL other requests. Sync functions run in a thread pool — they don't block the event loop but consume threads. For I/O-bound tasks: use async. For CPU-bound tasks: use sync or a separate task queue.

```python
# Async function - runs in event loop, don't block!
async def process_data(data):
    await db.insert(data)  # Non-blocking I/O - OK
    # time.sleep(5)        # BLOCKS entire event loop - NEVER do this

# Sync function - runs in thread pool, safe for blocking operations
def process_file(file_path):
    result = heavy_computation(file_path)  # CPU-bound - OK in thread
    return result
```

### Q4: What happens if a BackgroundTasks function raises an exception?
**Answer:** The exception is logged by Python's logging system but doesn't affect the client response (already sent). There's no built-in retry, error handling, or notification mechanism. Always wrap tasks in try/except for proper error handling.

```python
async def safe_task(email: str):
    try:
        await send_email(email)
    except SMTPException as e:
        logger.error(f"Failed to send email to {email}: {e}")
        # No retry mechanism - task is lost
        # For critical tasks, use Celery/ARQ instead
```

### Q5: How do you test BackgroundTasks in FastAPI?
**Answer:** Use FastAPI's TestClient — BackgroundTasks run synchronously in test mode. Verify side effects after making requests. For more control, create a MockBackgroundTasks class and override the dependency.

```python
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

app = FastAPI()

@app.post("/send-email")
async def send_email_endpoint(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_async, email)
    return {"status": "queued"}

# TestClient runs background tasks synchronously
def test_send_email():
    with patch("app.send_email_async") as mock_send:
        client = TestClient(app)
        response = client.post("/send-email?email=test@example.com")
        assert response.status_code == 200
        mock_send.assert_called_once_with("test@example.com")

# For async tests, use MockBackgroundTasks
class MockBackgroundTasks:
    def __init__(self):
        self.tasks = []

    def add_task(self, func, *args, **kwargs):
        self.tasks.append((func, args, kwargs))

    async def run_all(self):
        for func, args, kwargs in self.tasks:
            await func(*args, **kwargs)
```

### Q6: How do you pass dependencies and database sessions to BackgroundTasks?
**Answer:** BackgroundTasks run outside the request context, so you can't use Depends() inside them. Pass dependency values as arguments when adding the task. Create fresh connections in the task if the request-scoped connection may be closed.

```python
@app.post("/process-order")
async def process_order(
    order_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Pass only serializable data - not the db session!
    background_tasks.add_task(
        process_order_background,
        order_id=order_id,
        user_id=user.id,  # Pass IDs, not objects
    )
    return {"status": "processing"}

async def process_order_background(order_id: str, user_id: int):
    # Create a fresh database session
    async with async_session() as db:
        order = await db.get(Order, order_id)
        if order:
            order.status = "processed"
            await db.commit()
```

### Q7: When should you use BackgroundTasks vs Celery vs ARQ?
**Answer:**

| Criteria | BackgroundTasks | Celery | ARQ |
|----------|----------------|--------|-----|
| Setup complexity | None | High | Medium |
| Distributed execution | No | Yes | Yes |
| Result tracking | No | Yes | Yes |
| Retry logic | No | Yes | Yes |
| Monitoring | No | Flower | Custom |
| Persistence | No | Yes | Yes |
| Scheduling | No | Celery Beat | Cron |
| Async support | Yes | Limited | Native |
| Memory overhead | Low | High | Low |

**Decision framework:**
- **BackgroundTasks**: Fire-and-forget, non-critical, single-server, simple
- **Celery**: Complex workflows, scheduling, large ecosystem, mature
- **ARQ**: Async-first, minimal deps, Redis-only, simpler than Celery

### Q8: Can you schedule BackgroundTasks to run later?
**Answer:** No, BackgroundTasks runs tasks immediately after the response. For delayed tasks use asyncio.sleep (not recommended for production), Celery Beat for recurring tasks, or ARQ cron for async cron scheduling.

### Q9: How do you implement a migration path from BackgroundTasks to Celery?
**Answer:** Create an abstract TaskRunner interface with add_task method. Implement BackgroundTasksRunner and CeleryTaskRunner. Use dependency injection to swap implementations without changing route code.

```python
from abc import ABC, abstractmethod

class TaskRunner(ABC):
    @abstractmethod
    async def add_task(self, func, *args, **kwargs):
        pass

class BackgroundTasksRunner(TaskRunner):
    def __init__(self):
        self.tasks = BackgroundTasks()

    async def add_task(self, func, *args, **kwargs):
        self.tasks.add_task(func, *args, **kwargs)

class CeleryTaskRunner(TaskRunner):
    async def add_task(self, func, *args, **kwargs):
        func.delay(*args, **kwargs)

# Dependency injection
def get_task_runner() -> TaskRunner:
    if settings.USE_CELERY:
        return CeleryTaskRunner()
    return BackgroundTasksRunner()

@app.post("/process")
async def process(
    data: str,
    runner: TaskRunner = Depends(get_task_runner),
):
    await runner.add_task(process_data, data)
    return {"status": "queued"}
```

### Q10: How do you implement graceful shutdown for BackgroundTasks?
**Answer:** Track running tasks in a set. Use FastAPI lifespan to wait for tasks on shutdown. For critical tasks, use a task queue with built-in shutdown handling.

```python
import asyncio
from contextlib import asynccontextmanager

running_tasks: set[asyncio.Task] = set()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Cancel all running tasks on shutdown
    for task in running_tasks:
        task.cancel()
    # Wait for all tasks to finish (with timeout)
    if running_tasks:
        await asyncio.wait(running_tasks, timeout=10.0)

app = FastAPI(lifespan=lifespan)
```

---

## Task Queue Concepts

### Q11: What is a message broker and why is it needed?
**Answer:** A message broker (Redis, RabbitMQ) receives, stores, and delivers messages between task producers (API servers) and task consumers (workers). It decouples task submission from execution, enables distributed processing, persistence, load balancing, and buffering for traffic spikes.

**Broker comparison:**

| Feature | Redis | RabbitMQ | Kafka |
|---------|-------|----------|-------|
| Speed | Very fast | Fast | Fast |
| Persistence | Optional | Yes | Yes (log) |
| Routing | Simple | Complex | Complex |
| Complexity | Low | Medium | High |
| Best for | Simple queues | Complex routing | Event streaming |

### Q12: What is the difference between push and pull task delivery models?
**Answer:** Pull: workers poll the broker for tasks, control their own rate, natural load balancing. Push: broker pushes tasks to workers, lower latency, risk of overwhelming slow workers. Most task queues (Celery, ARQ) use pull models.

### Q13: What is task serialization and why does it matter?
**Answer:** Converting task function name, arguments to JSON for broker transmission. JSON is portable and secure. NEVER use pickle with untrusted data (arbitrary code execution risk). Convert complex objects to JSON-compatible formats before passing to tasks.

```python
# BAD: pickle serialization (security risk!)
app.conf.task_serializer = 'pickle'

# GOOD: JSON serialization (safe)
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'

# Convert non-serializable objects before passing to tasks
@app.post("/process")
async def process(data: MyModel, background_tasks: BackgroundTasks):
    # Convert Pydantic model to dict for serialization
    background_tasks.add_task(process_data, data.model_dump())
```

### Q14: What is idempotency and why is it critical for background tasks?
**Answer:** Idempotency means a task produces the same result when run multiple times. In distributed systems, tasks may be delivered more than once (at-least-once delivery). Use idempotency keys, database constraints, check-then-act patterns, or event deduplication to ensure safety.

```python
async def process_payment(payment_id: str, amount: float):
    # Idempotent: check if already processed
    existing = await db.get(Payment, payment_id)
    if existing and existing.status == "completed":
        return existing  # Already processed, return cached result

    # Process payment
    result = await charge(amount)
    await db.insert(Payment(id=payment_id, status="completed", result=result))
    return result
```

### Q15: What is at-least-once vs exactly-once delivery?
**Answer:** At-least-once: task delivered at least once, may duplicate, requires idempotent tasks. At-most-once: task delivered at most once, may be lost on worker crash. Exactly-once: nearly impossible in distributed systems, approximated through idempotency + deduplication + transactions.

### Q16: What is a result backend and when do you need one?
**Answer:** A result backend (Redis, PostgreSQL) stores task results after completion. Needed when clients need results, task status tracking, task chains, or chord workflows. Not needed for fire-and-forget tasks like emails or logging.

---

## Celery

### Q17: What is the difference between .delay() and .apply_async()?
**Answer:** `.delay()` is a shortcut with default options. `.apply_async()` allows specifying queue, countdown, eta, expires, retry policy, callbacks, and priority. Use `.delay()` for simple cases, `.apply_async()` for production with routing and scheduling needs.

```python
# Simple - uses default queue
process_data.delay(data)

# Production - with full control
process_data.apply_async(
    args=[data],
    queue="high-priority",
    countdown=60,        # Delay 60 seconds
    eta=datetime(2025, 1, 15, 10, 0),  # Specific time
    expires=3600,        # Expires in 1 hour
    retry_policy={
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.5,
    },
    priority=0,  # 0=highest, 9=lowest
)
```

### Q18: What are Celery groups, chains, and chords?
**Answer:** Groups run tasks in parallel with no dependencies. Chains pass results sequentially (pipeline). Chords run a group followed by a callback when all complete (parallel + aggregation).

```python
from celery import group, chain, chord

# Group: parallel execution
job = group(process.s(item) for item in items)
result = job.apply_async()

# Chain: sequential pipeline
workflow = chain(
    validate.s(data),
    process.s(),
    store.s(),
    notify.s()
)
result = workflow.apply_async()

# Chord: parallel + callback
callback = notify_complete.s()
workflow = chord(
    [process.s(item) for item in items],
    callback
)
result = workflow.apply_async()
```

### Q19: What is task_acks_late and why is it important?
**Answer:** Controls when tasks are acknowledged in the broker. Default (False): ack when received, risky if worker crashes mid-task. True: ack after completion, safe but may duplicate on crash. Always combine with idempotent tasks for reliability.

```python
# celeryconfig.py
task_acks_late = True
task_reject_on_worker_lost = True  # Re-queue on worker crash
```

### Q20: What is Flower and how does it help?
**Answer:** Flower is a web-based Celery monitoring tool showing worker status, task results, success/failure rates, and worker management. For production, consider Prometheus + Grafana for more customizable monitoring.

### Q21: How do you configure Celery for production with FastAPI?
**Answer:**

```python
from celery import Celery

celery_app = Celery("worker")
celery_app.config_from_object({
    'broker_url': settings.REDIS_URL,
    'result_backend': settings.REDIS_URL,
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
    'timezone': 'UTC',
    'enable_utc': True,
    'task_acks_late': True,
    'task_reject_on_worker_lost': True,
    'worker_prefetch_multiplier': 1,  # One task at a time per worker
    'task_routes': {
        'app.tasks.email.*': {'queue': 'email'},
        'app.tasks.payment.*': {'queue': 'high-priority'},
    },
    'task_default_queue': 'default',
    'worker_max_tasks_per_child': 1000,  # Recycle workers to prevent leaks
    'worker_max_memory_per_child': 200000,  # 200MB memory limit
})
```

---

## ARQ

### Q22: What is ARQ and why choose it over Celery?
**Answer:** ARQ is an async Redis-based task queue. Choose it for async-first apps, simplicity, and minimal dependencies. Celery for advanced features (scheduling, complex workflows, larger community). ARQ is native async, Celery has limited async support.

```python
from arq import create_pool
from arq.connections import RedisSettings

async def enqueue_task(ctx, task_func, *args, **kwargs):
    pool = ctx['redis_pool']
    await pool.enqueue_job(task_func, *args, **kwargs)

# Worker setup
from arq import Worker

async def startup(ctx):
    ctx['redis_pool'] = await create_pool(RedisSettings())

worker = Worker(
    functions=[process_data, send_email],
    on_startup=startup,
    max_jobs=10,
    job_timeout=30,
)
```

### Q23: What is the ARQ worker context?
**Answer:** A dictionary containing Redis connection, job ID, job try count, and max retries. Initialize shared resources in on_startup. Provides access to Redis, database connections, and other resources for all tasks.

```python
async def process_order(ctx, order_id: str):
    redis = ctx['redis']
    db = ctx['db']
    job_id = ctx['job_id']
    max_tries = ctx.get('max_tries', 3)

    order = await db.get(Order, order_id)
    if not order:
        return None

    result = await process_payment(order)
    await redis.set(f"order:{order_id}:result", result, expire=3600)
    return result
```

### Q24: How does ARQ handle retries?
**Answer:** ARQ retries failed tasks up to max_tries times with retry_delay between attempts. Tasks can raise Retry exception with custom delay. Distinguish temporary errors (retry) from permanent errors (fail immediately, log to DLQ).

```python
from arq import Retry

async def unreliable_task(ctx):
    try:
        result = await call_external_api()
        return result
    except TemporaryError as e:
        # Retry with exponential backoff
        raise Retry(delay=min(2 ** ctx.get('job_try', 0), 60))
    except PermanentError as e:
        # Don't retry, log to DLQ
        await log_to_dlq(ctx, str(e))
        raise  # Will be marked as failed
```

### Q25: How do you implement task priority in ARQ?
**Answer:** ARQ doesn't have built-in priority queues. Implement with multiple Redis lists (queue:0 through queue:9). Worker checks high-priority queues first. Enqueue to specific queue based on task priority.

```python
class PriorityARQ:
    def __init__(self, redis_pool):
        self.redis = redis_pool

    async def enqueue(self, func, priority=5, *args, **kwargs):
        queue_name = f"arq:queue:{priority}"
        await self.redis.enqueue_job(func, *args, _queue_name=queue_name, **kwargs)

# Worker processes high-priority queues first
async def start_priority_worker():
    worker = Worker(
        functions=[process_task],
        queue_names=['arq:queue:0', 'arq:queue:1', 'arq:queue:5', 'arq:queue:9'],
    )
    await worker.run()
```

---

## Task Retry & Failure Patterns

### Q26: How do you implement exponential backoff with jitter?
**Answer:** Exponential backoff increases delay exponentially (1s, 2s, 4s, 8s). Jitter adds randomness to prevent thundering herd. Types: full jitter (0 to delay), equal jitter (half base + random half), decorrelated jitter. Always cap maximum delay.

```python
import random
import asyncio

def get_backoff_delay(attempt, base=1.0, max_delay=60.0):
    delay = min(base * (2 ** attempt), max_delay)
    return random.uniform(0, delay)  # Full jitter

async def retry_with_backoff(func, max_retries=5, *args, **kwargs):
    for attempt in range(max_retries):
        try:
            return await func(*args, **kwargs)
        except (TemporaryError, ConnectionError) as e:
            if attempt == max_retries - 1:
                raise
            delay = get_backoff_delay(attempt)
            logger.info(f"Retry {attempt + 1}/{max_retries} after {delay:.1f}s: {e}")
            await asyncio.sleep(delay)

# Celery implementation
from celery import Task

class RetryableTask(Task):
    autoretry_for = (ConnectionError, TimeoutError)
    max_retries = 5
    retry_backoff = True
    retry_backoff_max = 60
    retry_jitter = True
```

### Q27: What is a dead letter queue and when do you need one?
**Answer:** A DLQ stores messages that failed processing after maximum retries. Enables investigation, manual reprocessing, and alerting. Without DLQ, permanently failed tasks are lost. Implement with a separate Redis list or queue. Monitor DLQ depth for anomalies.

```python
async def task_with_dlq(ctx, message):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return await process_message(message)
        except Exception as e:
            if attempt == max_retries - 1:
                # All retries exhausted, send to DLQ
                await ctx['redis'].lpush("dlq:tasks", json.dumps({
                    "task": "process_message",
                    "args": [message],
                    "error": str(e),
                    "attempt": attempt,
                    "timestamp": datetime.utcnow().isoformat(),
                }))
                logger.error(f"Task sent to DLQ after {max_retries} attempts: {e}")
                raise
            await asyncio.sleep(2 ** attempt)
```

### Q28: How do you implement task timeouts?
**Answer:** Use time_limit in Celery, job_timeout in ARQ. Implement soft timeouts for graceful shutdown (catch TimeoutError, cleanup, re-raise). Hard timeouts kill the worker process. Set different timeouts for different task types.

```python
# Celery
@app.task(time_limit=300, soft_time_limit=280)
def long_running_task(data):
    # 300s hard limit, 280s soft limit (raises SoftTimeLimitExceeded)
    try:
        result = process(data)
        return result
    except SoftTimeLimitExceeded:
        # Graceful cleanup
        cleanup_resources()
        raise

# ARQ
async def process(ctx, data):
    result = await heavy_computation(data)
    return result

# Worker configuration
worker = Worker(
    functions=[process],
    job_timeout=300,  # 5 minutes
)
```

### Q29: How do you handle partial failures in task chains?
**Answer:** Use error callbacks (link_error) in Celery chains. Implement compensating transactions to roll back completed steps. Use saga pattern for complex workflows. Log the state at each step for debugging and manual recovery.

```python
from celery import chain

# Chain with error handling
workflow = chain(
    validate.s(data) | process.s() | store.s()
)
result = workflow.apply_async(link_error=handle_failure.s())

@app.task
def handle_failure(request, exc, *args, **kwargs):
    logger.error(f"Task {request.task} failed: {exc}")
    # Notify, alert, or compensate
    send_alert.delay(f"Workflow failed: {exc}")
```

### Q30: What is the poison pill pattern?
**Answer:** A message that causes a worker to crash or loop indefinitely. Prevent by: validating all inputs, setting timeouts, limiting retry count, implementing circuit breakers, and monitoring worker health. Dead letter queues catch poison pills after max retries.

### Q31: How do you implement task cancellation?
**Answer:** Check for cancellation flag during execution (stored in Redis with TTL). Use Celery revoke() with terminate=True (sends SIGTERM). ARQ requires manual implementation. Always handle cleanup when a task is cancelled (release locks, rollback transactions).

```python
import asyncio
from contextvars import ContextVar

cancel_flags: dict[str, bool] = {}

async def cancellable_task(ctx, task_id: str):
    try:
        for step in range(100):
            # Check cancellation flag
            if cancel_flags.get(task_id, False):
                await cleanup(task_id)
                raise asyncio.CancelledError(f"Task {task_id} cancelled")

            await process_step(step)
    finally:
        cancel_flags.pop(task_id, None)

# Cancel a task
async def cancel_task(task_id: str):
    cancel_flags[task_id] = True

# Celery approach
from celery.result import AsyncResult

def cancel_celery_task(task_id: str):
    result = AsyncResult(task_id)
    result.revoke(terminate=True, signal='SIGTERM')
```

---

## Dead Letter Queues

### Q32: How do you implement a DLQ system?
**Answer:** Create a separate queue for failed tasks. After max retries, move the task to DLQ with error metadata (error message, stack trace, retry count, timestamp). Implement a DLQ consumer for manual inspection and reprocessing. Alert when DLQ depth exceeds threshold.

```python
class DLQManager:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def send_to_dlq(self, task_name: str, args: tuple, kwargs: dict, error: Exception, metadata: dict = None):
        message = {
            "task": task_name,
            "args": args,
            "kwargs": kwargs,
            "error": {
                "type": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc(),
            },
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat(),
            "retry_count": metadata.get("retry_count", 0) if metadata else 0,
        }
        await self.redis.lpush("dlq:main", json.dumps(message))
        await self.redis.incr("dlq:count")

    async def get_dlq_messages(self, start: int = 0, count: int = 50) -> list:
        messages = await self.redis.lrange("dlq:main", start, start + count - 1)
        return [json.loads(m) for m in messages]

    async def reprocess(self, index: int):
        """Move message back to main queue for reprocessing"""
        message = await self.redis.lindex("dlq:main", index)
        if message:
            await self.redis.lrem("dlq:main", 1, message)
            msg = json.loads(message)
            # Re-enqueue with original task
            await self.redis.lpush("queue:default", message)
```

### Q33: How do you implement DLQ reprocessing?
**Answer:** Build an admin API to list DLQ messages, inspect details, and requeue with fixed parameters. Implement bulk reprocessing for systematic failures. Track reprocessing attempts. Use idempotency keys to prevent duplicates during reprocessing.

### Q34: What information should you store with DLQ messages?
**Answer:** Original task name and arguments, error message and type, stack trace, retry count, timestamps (created, failed, added to DLQ), worker ID, and any context that helps debugging. Store as structured JSON for easy querying.

---

## Task Prioritization & Routing

### Q35: How do you implement task prioritization in Celery?
**Answer:** Use multiple queues with different priorities. Workers consume from high-priority queues first using -Q flag ordering. Route tasks based on type, urgency, or user tier. Use priority headers in apply_async() with RabbitMQ or Redis priority support.

```python
# Task routing configuration
task_routes = {
    'app.tasks.email.*': {'queue': 'email'},
    'app.tasks.payment.*': {'queue': 'high-priority'},
    'app.tasks.reports.*': {'queue': 'background'},
    'app.tasks.cleanup.*': {'queue': 'low-priority'},
}

# Worker consumes from queues in priority order
# celery -A app worker -Q high-priority,email,default,background,low-priority
```

### Q36: How do you handle queue saturation?
**Answer:** Monitor queue depth with Prometheus metrics. Implement backpressure (reject new tasks when queue is full). Scale workers horizontally. Use multiple queues to isolate critical tasks. Set task expiry (expires argument) for time-sensitive tasks.

```python
@app.middleware("http")
async def backpressure_middleware(request: Request, call_next):
    queue_depth = await redis.llen("queue:default")
    if queue_depth > 10000:  # Threshold
        return JSONResponse(
            status_code=503,
            content={"detail": "Service overloaded, try again later"},
            headers={"Retry-After": "30"}
        )
    return await call_next(request)
```

---

## Monitoring & Observability

### Q37: What metrics should you track for task queues?
**Answer:** Queue depth (tasks waiting), processing time (task duration percentiles), success/failure rates, worker count (active, idle), task throughput (tasks/second), retry rate, DLQ depth, memory usage per worker, and broker connection health.

```python
from prometheus_client import Counter, Histogram, Gauge

task_started = Counter('celery_tasks_started_total', 'Tasks started', ['task_name'])
task_succeeded = Counter('celery_tasks_succeeded_total', 'Tasks succeeded', ['task_name'])
task_failed = Counter('celery_tasks_failed_total', 'Tasks failed', ['task_name'])
task_duration = Histogram('celery_task_duration_seconds', 'Task duration', ['task_name'])
queue_depth = Gauge('celery_queue_depth', 'Queue depth', ['queue_name'])
active_workers = Gauge('celery_active_workers', 'Active workers')
```

### Q38: How do you implement task queue monitoring?
**Answer:** Use Prometheus client to export metrics from workers. Create Grafana dashboards for queue health visualization. Set up alerts for: queue depth > threshold, failure rate > 5%, worker count < minimum, DLQ depth > 0. Use structured logging for task lifecycle events.

### Q39: How do you trace a task through the system?
**Answer:** Generate a unique task ID and include it in all log entries. Pass correlation IDs through task chains. Store task metadata (start time, end time, status) in Redis/database. Use distributed tracing (OpenTelemetry) to connect API requests to background tasks.

```python
from opentelemetry import trace

@app.post("/order")
async def create_order(order: Order, background_tasks: BackgroundTasks):
    with tracer.start_as_current_span("create_order") as span:
        trace_id = span.get_span_context().trace_id
        background_tasks.add_task(process_order, order.id, trace_id=trace_id)

async def process_order(order_id: str, trace_id: int = None):
    with tracer.start_as_current_span("process_order") as span:
        if trace_id:
            span.set_attribute("trace_id", trace_id)
        # Processing...
```

### Q40: How do you monitor Celery in production?
**Answer:** Use Flower for real-time monitoring. Export metrics to Prometheus with celery-exporter. Set up Sentry for error tracking. Use Datadog/New Relic for APM. Monitor broker metrics (connection count, memory usage, queue lengths). Set up PagerDuty alerts for critical failures.

---

## Scaling Workers

### Q41: How do you scale Celery workers horizontally?
**Answer:** Add more worker processes or containers. Use Kubernetes HPA based on queue depth or CPU. Separate workers by task type (CPU-bound on dedicated nodes, I/O-bound on others). Use Celery pools (prefork, gevent, eventlet) based on task type.

```yaml
# Kubernetes HPA for Celery workers
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: celery-worker
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: celery-worker
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: External
    external:
      metric:
        name: celery_queue_depth
        selector:
          matchLabels:
            queue: default
      target:
        type: AverageValue
        averageValue: "100"
```

### Q42: What is the difference between Celery worker pools?
**Answer:** Prefork: separate processes, true parallelism, good for CPU-bound tasks, higher memory. Gevent: green threads, lightweight, good for I/O-bound tasks, cooperative multitasking. Eventlet: similar to gevent, different implementation. Solo: single process, debugging. Default is prefork.

```bash
# Prefork for CPU-bound tasks
celery -A app worker --pool=prefork --concurrency=4

# Gevent for I/O-bound tasks
celery -A app worker --pool=gevent --concurrency=100

# Solo for debugging
celery -A app worker --pool=solo
```

### Q43: How do you handle worker autoscaling?
**Answer:** Celery has built-in autoscaler (min/max workers). Kubernetes HPA with custom metrics (queue depth). Cloud auto-scaling groups based on queue metrics. Scale up aggressively, scale down conservatively (drain queue first).

### Q44: How do you distribute workers across multiple machines?
**Answer:** All workers connect to the same broker (Redis/RabbitMQ). Use consistent hashing for task routing if needed. Deploy workers in the same region as the broker for low latency. Use separate broker instances for different environments.

---

## Idempotency & Task Ordering

### Q45: How do you ensure task idempotency?
**Answer:** Use idempotency keys (UUID) sent with each task. Store processed keys with TTL in Redis. Before processing, check if key exists and return cached result. Use database unique constraints. Design operations to be naturally idempotent (set state, don't increment).

```python
async def idempotent_process(ctx, task_id: str, data: dict):
    redis = ctx['redis']

    # Check if already processed
    result = await redis.get(f"result:{task_id}")
    if result:
        return json.loads(result)

    # Process
    output = await process_data(data)

    # Store result with TTL (24 hours)
    await redis.setex(f"result:{task_id}", 86400, json.dumps(output))

    return output
```

### Q46: How do you handle task ordering guarantees?
**Answer:** Celery guarantees order within a single queue and worker. For strict ordering, use a single worker (limits throughput). Use sequence numbers for partial ordering. Accept eventual consistency for most use cases. Use database transactions for critical ordering.

```python
# Single queue + single worker = strict ordering
celery -A app worker --pool=solo --queues=ordered

# Partial ordering with sequence numbers
async def process_event(ctx, sequence: int, event: dict):
    last_seq = await ctx['redis'].get("last_sequence")
    if last_seq and int(last_seq) >= sequence:
        return  # Already processed or out of order

    await process(event)
    await ctx['redis'].set("last_sequence", sequence)
```

### Q47: How do you handle duplicate task detection?
**Answer:** Hash the task (name + args + user + timestamp window). Store hashes in Redis with TTL. If duplicate detected within TTL, return cached response or skip processing. Use idempotency keys as an alternative. Implement at the application level, not broker level.

---

## Architecture & Design

### Q48: How do you handle task dependencies?
**Answer:** Use Celery chains/chords for dependent tasks. ARQ requires manual chaining (pass result as argument). For complex workflows, consider workflow engines (Airflow, Prefect). Use the saga pattern for distributed transactions with compensation.

### Q49: How do you handle task results for async clients?
**Answer:** Use WebSockets, Server-Sent Events, or polling. Store results in Redis/database with TTL. Provide endpoints to check task status and retrieve results. Use long polling for simple cases. WebSocket for real-time updates.

```python
@app.get("/task/{task_id}/status")
async def get_task_status(task_id: str):
    result = await redis.hgetall(f"task:{task_id}")
    if not result:
        raise HTTPException(404, "Task not found")

    return {
        "task_id": task_id,
        "status": result[b"status"].decode(),
        "progress": int(result.get(b"progress", 0)),
        "result": json.loads(result[b"result"]) if b"result" in result else None,
    }

@app.websocket("/ws/tasks/{task_id}")
async def task_progress(websocket: WebSocket, task_id: str):
    await websocket.accept()
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"task:{task_id}:progress")

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_json(json.loads(message["data"]))
    finally:
        await pubsub.unsubscribe()
```

### Q50: What are the security considerations for task queues?
**Answer:** Don't pass sensitive data in tasks (use references instead). Use TLS for broker connections. Validate all task inputs (prevent injection). Implement access control for task management. Use separate brokers for different environments. Rotate broker credentials regularly.

```python
# Don't do this - passes sensitive data through broker
send_email.delay(user_email, password_reset_token)

# Do this instead - pass reference, fetch in task
send_email.delay(user_id=user.id, token_id=token.id)

async def send_email(user_id: int, token_id: int):
    user = await db.get(User, user_id)
    token = await db.get(PasswordResetToken, token_id)
    # Fetch sensitive data at task execution time
    await _send_email(user.email, token.value)
```
