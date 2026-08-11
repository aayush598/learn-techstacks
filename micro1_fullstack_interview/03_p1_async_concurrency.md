# Priority 1 — Async Python & Concurrency (Q79–Q120)

**Why these matter for micro1:** the role explicitly requires "concurrency patterns and backend optimizations" and the AI recruiter (Zara) makes many concurrent LLM/external calls. This is one of the two most drilled focus areas. Expect code-writing + "what happens if this fails at scale."

---

## Q79: What is asynchronous programming?

A programming style where a task can **pause (yield) and let other tasks run** while waiting for slow operations (I/O) to finish, instead of blocking the whole thread.

- One thread interleaves many tasks; the event loop schedules which task runs next.
- Benefit: high concurrency with low overhead — thousands of in-flight I/O operations per thread/process.
- Contrast with threads (preemptive, kernel-scheduled, expensive switching, shared memory) and processes (isolated, expensive).
- Python's flavor is **cooperative** (tasks yield explicitly with `await`).

---

## Q80: What is `asyncio`?

Python's **standard library for async I/O**: an event loop + primitives (tasks, futures, coroutines) + I/O APIs.

Key pieces:
- `asyncio.run(main())` — entry point; creates/runs/closes the event loop.
- Coroutines (`async def`) — awaitable functions.
- `asyncio.gather()`, `asyncio.create_task()`, `asyncio.wait()` — run multiple coroutines.
- Synchronization: `Semaphore`, `Lock`, `Event`, `Condition`, `Queue`.
- Timeouts/cancellation: `asyncio.wait_for()`, `task.cancel()`, `asyncio.timeout()`.
- Subprocess/files/streams support (not just sockets).
- Third-party async I/O: `httpx`, `aiohttp`, `asyncpg`, `aioredis`.

---

## Q81: What is an event loop?

The core scheduler of async code — a single loop that:

1. Tracks **ready tasks** and **I/O callbacks** (via OS polling: `select`/`epoll`/`kqueue`/IOCP).
2. Runs one task until it `await`s something that would block → the loop switches to another ready task.
3. When the awaited I/O completes, the loop resumes the task.

```
loop.run_until_complete(coro)
  ├─ task A running... hits await socket.read()
  ├─ loop polls sockets (epoll) → B ready
  ├─ task B running... hits await sleep(1)
  ├─ socket ready → resume A
  └─ ... until done
```

- There is **one event loop per thread** (in the main thread by default). Everything runs on a single thread → no races on Python objects between coroutines (as long as no blocking interleaves).
- Uvicorn runs one (or more) event loops per worker process.

---

## Q82: What is a coroutine?

A function defined with `async def`; calling it **returns a coroutine object** without running it. It's **awaitable** — you must schedule it (await/`asyncio.run`/task) for its body to execute.

```python
async def fetch(url):          # coroutine function
    async with httpx.AsyncClient() as c:
        return await c.get(url)

coro = fetch("https://x.com")  # nothing executed yet — coroutine object
```

- Inside a coroutine, `await` suspends it until the awaited operation completes.
- A coroutine is a specialized generator under the hood (stackless state machine in CPython via `CO_COROUTINE`).
- Never forget to await one — "RuntimeWarning: coroutine was never awaited".

---

## Q83: What does `async` mean in Python?

Marks a function as a **coroutine function**: it returns an awaitable coroutine when called, and its body may use `await`, `async for`, `async with`.

- `async def foo(): ...` — coroutine function.
- `async for x in agen` — iterate an async generator/stream (each iteration awaits).
- `async with` — enter/exit an async context manager (e.g., an async client/session).
- Also used for `async generators` (`async def` + `yield`).
- `async` means "this may yield control to the event loop" — not "runs in parallel."

---

## Q84: What does `await` mean?

`await expr` **suspends the current coroutine** and gives control back to the event loop until `expr` (an awaitable) completes, then resumes with its result.

```python
async def main():
    resp = await fetch(url)   # pause here; loop can run other tasks
    print(resp)
```

- Only legal inside `async def` (or the REPL/`asyncio.run`).
- Awaitables: coroutines, `asyncio.Future`, `asyncio.Task`, objects with `__await__`.
- While suspended, the event loop runs other ready tasks → concurrency.
- `await` does NOT block the thread — that's the whole point.

---

## Q85: What happens when you `await` a coroutine?

1. The current coroutine **suspends** — its state is saved in its frame.
2. The event loop gets control and continues running other ready tasks.
3. The awaited coroutine runs until it itself awaits/returns.
4. When it completes, the result is delivered back; the waiting coroutine **resumes** where it left off.
5. If the awaited coroutine raises, the exception propagates at the `await` point (you can `try/except` it).

```python
try:
    data = await fetch(url)      # suspend → resume with data (or raise)
except httpx.TimeoutException:
    data = fallback()
```

---

## Q86: What is the difference between synchronous and asynchronous code?

| | **Synchronous** | **Asynchronous** |
|---|---|---|
| Execution | One thing at a time; blocks on I/O | Interleaves tasks while I/O is pending |
| Threads | 1 operation = 1 blocked thread | Many operations on 1 thread |
| Concurrency | No (unless threads/processes) | Yes (cooperative) |
| Blocking calls | `requests.get()`, `time.sleep()` | `await client.get()`, `await asyncio.sleep()` |
| Best for | CPU-bound, simple scripts, sync services | I/O-bound, high concurrency |
| Latency per task | Similar | Similar (concurrency ≠ speedup per task) |
| Throughput under I/O | Low (threads idle-waiting) | High |

- Sync is simpler to reason about; async shines when many I/O waits overlap (APIs, DB, LLM calls).
- **Async ≠ faster** for CPU-bound or single sequential task; it's about *overlapping* waiting.

---

## Q87: When should you use asynchronous programming?

Use async when your workload is **I/O-bound** and **concurrency-hungry**:

- Many concurrent HTTP calls (LLM APIs, third-party services, aggregators).
- Web servers handling many simultaneous connections (FastAPI/Uvicorn).
- Real-time streams, WebSockets, SSE (LLM streaming!).
- DB access with async drivers, Redis, message queues.
- Long-running external operations (email, file uploads to S3, scraping).

Use sync when: CPU-bound heavy math (use multiprocessing), simple scripts, legacy sync libs, or where complexity isn't justified.

---

## Q88: What types of workloads benefit from async programming?

- **Network I/O** — HTTP, sockets, gRPC: thousands of concurrent calls.
- **Database I/O** — async drivers (`asyncpg`, `async SQLAlchemy`, `aioredis`).
- **Streaming** — SSE/WebSocket fan-out, log/event streams.
- **External APIs / LLMs** — many parallel inference calls.
- **File I/O** (with care — use `asyncio.to_thread` for blocking file ops).
- Anything where the CPU sits idle waiting for something outside the process.

The rule: **if you'd otherwise block on I/O, async lets you overlap it.**

---

## Q89: What types of workloads do not benefit from async programming?

- **CPU-bound** compute (heavy math, image processing, data crunching) — the GIL + single loop means no parallelism; use `multiprocessing` or C extensions.
- **Single sequential I/O** — no overlap to gain.
- **Code dominated by sync/blocking libraries** that you can't replace (some DB drivers, crypto, regex on huge strings) — they'd block the loop.
- **Latency-critical per-request compute** — async adds overhead for no gain.
- Very high-throughput CPU work where you need multicore → processes/threads, not asyncio.

---

## Q90: What happens if you perform blocking I/O inside an async function?

The **entire event loop blocks** — all other coroutines on that loop freeze until the blocking call returns. Concurrency is lost; it's effectively sync.

```python
async def endpoint():
    data = requests.get(url).text     # BLOCKING — freezes the whole loop!
```

- `requests`, `time.sleep`, `os.read`, CPU-heavy calls, sync ORM calls inside `async def` all block.
- Symptoms: latency spikes, watchdog timeouts, cascading timeouts to *all* users.
- Detection: look for sync network/DB calls in async paths; profiling shows long "no await" spans.

---

## Q91: Why is blocking code dangerous inside an async FastAPI endpoint?

- FastAPI runs `async def` endpoints **on the event loop**. One blocking call (e.g., `requests.get`, a heavy `time.sleep`, sync DB query) **blocks the whole worker's loop** → every other request on that worker stalls.
- At high concurrency this looks like the server is dead: timeouts everywhere, health checks fail.
- **Mitigations:**
  1. Mark endpoints `def` (sync) — FastAPI runs them in a **threadpool** (`run_in_threadpool`), so they don't block the loop.
  2. Or keep `async def` and ensure every call inside is truly async.
  3. Or run blocking work via `await asyncio.to_thread(blocking_fn, ...)`.
  4. For CPU-heavy work, use a process pool or a worker queue.

**Golden rule:** inside `async def`, every operation must be awaitable and non-blocking.

---

## Q92: How would you run blocking code from an async application?

```python
import asyncio

# Option 1: threadpool (best for I/O-bound blocking calls)
result = await asyncio.to_thread(blocking_function, arg1, arg2)

# Option 2: explicit executor
from concurrent.futures import ThreadPoolExecutor
loop = asyncio.get_running_loop()
result = await loop.run_in_executor(thread_pool, blocking_function, arg)

# Option 3: CPU-heavy → ProcessPoolExecutor (bypasses GIL)
with ProcessPoolExecutor() as pool:
    result = await loop.run_in_executor(pool, cpu_intensive, data)

# Option 4: in FastAPI, just make the endpoint sync (def) — auto-threadpool
@app.get("/")
def sync_endpoint():
    return heavy_sync_work()
```

- `asyncio.to_thread` runs in a default thread pool (ThreadPoolExecutor) — the loop stays free.
- Never block the loop with sync calls directly.

---

## Q93: What is `asyncio.gather()`?

Runs multiple awaitables **concurrently** and returns their results **in input order**.

```python
async def main():
    results = await asyncio.gather(
        fetch(url1), fetch(url2), fetch(url3),
        return_exceptions=False,   # default: first exception propagates, others cancelled
    )
```

- If `return_exceptions=True`, exceptions are returned as values instead of raising.
- All tasks must complete for `gather` to return (unless one raises and you don't use `return_exceptions` → it cancels the rest and raises).
- Good for fan-out where you want *all* results together.

---

## Q94: What is `asyncio.create_task()`?

Schedules a coroutine to run **concurrently** as a background task and returns the `Task` object immediately — the caller keeps going.

```python
task = asyncio.create_task(fetch(url))   # starts running on the loop
# ... do other work ...
data = await task                        # await the task for its result
```

- The task starts executing as soon as the loop gets a chance (next await/scheduling point).
- Keep a **reference** to the task or it may be garbage collected (pre-Py3.11 warnings; Py3.11+ holds them via the loop, but still keep refs for control).
- `task.cancel()` to cancel; `task.done()`/`task.result()` for inspection.

---

## Q95: What is the difference between `create_task()` and `gather()`?

| | **`create_task()`** | **`gather()`** |
|---|---|---|
| Returns | Task immediately | Awaits all results together |
| Concurrency | Starts task; caller continues | Runs all until all complete |
| Result collection | Manual (`await task`) | Returns list in input order |
| Error handling | Task's exception surfaces when awaited | Propagates first error (or collects with `return_exceptions`) |
| Use case | Fire-and-forget/background work; mixing with other awaits | Fan-out where you want all results |

```python
t = asyncio.create_task(fetch(a))     # start, don't block
r = await asyncio.gather(fetch(b), fetch(c))
```

- Related: `asyncio.wait()` (more control: `FIRST_COMPLETED`, `ALL_COMPLETED`), `asyncio.as_completed()` (yield results as they finish).

---

## Q96: How do you execute multiple API calls concurrently?

```python
import asyncio, httpx

async def fetch_all(urls, client):
    return await asyncio.gather(*(client.get(u) for u in urls))

async def main():
    async with httpx.AsyncClient(timeout=10) as client:
        responses = await fetch_all(urls, client)
```

- Use one shared `httpx.AsyncClient` (connection pooling, keep-alive — Q108).
- `asyncio.gather` for all-results; `asyncio.as_completed` to process as they finish; `create_task` for fire-and-forget.
- **Always bound concurrency** with a semaphore (Q97) — unbounded fan-out of 10k calls will exhaust sockets/limits.

---

## Q97: How would you limit the number of concurrent requests?

Use `asyncio.Semaphore`:

```python
import asyncio

async def limited_fetch(sem, client, url):
    async with sem:                    # acquire before starting
        return await client.get(url)

async def main(urls, limit=20):
    sem = asyncio.Semaphore(limit)
    async with httpx.AsyncClient() as c:
        return await asyncio.gather(*(limited_fetch(sem, c, u) for u in urls))
```

- Caps in-flight work to `limit` regardless of how many tasks you spawn.
- For rate limits measured per second, combine a semaphore + token bucket / `asyncio.sleep` pacing.
- Also useful for: DB connection use, LLM concurrency, external API quotas.

---

## Q98: What is `asyncio.Semaphore`?

An async **counting semaphore**: allows at most `n` concurrent holders of the resource.

- `sem = asyncio.Semaphore(n)`; `async with sem:` acquires (waits if full) and releases on exit.
- `sem.acquire()`/`sem.release()` for manual control.
- `BoundedSemaphore` — raises if release exceeds acquire (bug detection).
- Like a mutex with a counter — for limiting concurrency, not mutual exclusion (Q99).

---

## Q99: What is `asyncio.Lock`?

An async **mutex**: ensures at most one task holds the lock at a time — mutual exclusion around a critical section.

```python
lock = asyncio.Lock()

async def inc():
    async with lock:          # wait until no one else holds it
        shared_counter += 1   # critical section
```

- Use when multiple coroutines mutate **shared state** (cache dicts, counters, file offsets).
- Different from a threading lock: it's tied to the event loop (don't share across loops).
- Also `asyncio.Event` (wait until set), `asyncio.Condition` (wait for a condition), `asyncio.Queue` (producer/consumer).

---

## Q100: When would you use an async lock?

- Guarding shared mutable state mutated by multiple coroutines: caches, in-memory counters/rate limiters, connection managers, idempotency stores.
- Protecting non-thread-safe resources shared across tasks.
- Ensuring a resource is initialized once (`async with lock: if not init: ...`).
- Serializing operations that must not interleave (e.g., token refresh for an OAuth client — only one task refreshes, others await).

```python
async def get_token():
    async with token_lock:
        if not token or token.expired:
            token = await refresh()   # one task refreshes; others wait
        return token
```

- Note: coroutines don't race on pure Python data between `await`s *in the same loop* — but a mutation **across an await** (or in threads) is where locks matter.

---

## Q101: What is a race condition?

A bug where the outcome depends on the **nondeterministic interleaving** of concurrent operations. Two tasks read-modify-write the same state and one clobbers the other.

```python
# counter += 1  ≈  read → add → write
# task A reads 5, task B reads 5, both write 6 → lost update
```

- Classic: bank balance, inventory, token refresh, duplicate inserts.
- Prevention: locks/semaphores (mutual exclusion), atomic operations, transactions with isolation, idempotency keys, optimistic locking.
- **async caveat:** without `await` between read/write there's no preemption *within a loop*, so races typically need `await` boundaries or threads/processes.

---

## Q102: How can race conditions happen in concurrent applications?

1. **Multiple threads/processes** writing shared state (no lock) → lost updates, torn reads.
2. **Async tasks** interleaving across `await` points (suspend while holding stale state).
3. **Check-then-act**: `if key not in cache: cache[key] = ...` — two tasks both pass the check.
4. **Read-modify-write** on shared counters/balances.
5. **Non-atomic DB ops**: `SELECT count` then `UPDATE` without a transaction.
6. **Caches + DB** coherence (cache-aside write ordering).
7. **Session reuse** across concurrent requests (SQLAlchemy Session is not thread-safe).

**Fixes:** serialize access (locks), make operations atomic (DB `UPDATE ... WHERE` with conditions), transactions + isolation levels, unique constraints + retry on conflict, idempotency keys, single-writer patterns.

---

## Q103: How do you prevent race conditions?

1. **Mutual exclusion:** locks (threading/asyncio), semaphores for capacity.
2. **Atomic operations:** DB `UPDATE counters SET n = n + 1` (single statement), Redis `INCR`.
3. **Transactions:** wrap read-modify-write in a transaction with appropriate isolation (Q153, Q553–555).
4. **Pessimistic locking:** `SELECT ... FOR UPDATE` (Q554).
5. **Optimistic locking:** version column + `UPDATE ... WHERE version = ?`; retry on conflict (Q553).
6. **Idempotency keys:** dedupe duplicate requests (Q397).
7. **Single-threaded per-key processing:** route per-user work to one worker; partition by key.
8. **Immutability / avoid shared mutable state** where possible.
9. **Redis distributed locks** (Redlock/`SET NX PX`) for cross-instance mutual exclusion.

---

## Q104: What is a deadlock?

A state where **two or more tasks each hold a resource the other needs**, so none can proceed — the system stalls forever.

```python
# Thread A: locks X, then waits for Y
# Thread B: locks Y, then waits for X
# → neither can finish
```

**Four necessary conditions:** mutual exclusion, hold-and-wait, no preemption, circular wait. Breaking any one prevents deadlock.

**Prevention/avoidance:**
- **Lock ordering** — always acquire locks in the same global order.
- **Timeouts** — `lock.acquire(timeout=...)`; abandon/retry.
- **Try-lock + backoff** instead of blocking forever.
- **Single lock** granularity where possible.
- In DBs: keep transactions short, consistent statement order, use `FOR UPDATE` sparingly; deadlocks surface as errors → retry.

---

## Q105: How can deadlocks happen?

- **Lock inversion:** two tasks acquiring two locks in opposite order.
- **Nested transactions** waiting on rows the other holds (`SELECT FOR UPDATE` both ways).
- **Thread pool exhaustion:** a task inside the pool waits for another task that can never be scheduled (e.g., pool of 1, main thread waits on pool).
- **Distributed systems:** two services calling each other while holding locks (use timeouts + idempotency).
- **async:** a task awaiting something that only *another task* (which is waiting on this task) can produce — e.g., awaiting a result inside a callback.
- **DB:** `UPDATE` two rows in opposite order across two transactions → classic row-lock deadlock.

---

## Q106: What is starvation?

A situation where a task is **indefinitely prevented from making progress** because other tasks always get the resource first (even though it's not deadlocked).

- Examples: a low-priority thread never scheduled because high-priority threads flood the queue; a fair lock where a waiter keeps losing; a consumer starved by a producer.
- **vs deadlock:** deadlock = none progress; starvation = some progress, others never do.
- **Mitigations:** fair scheduling (FIFO locks), priorities with aging, batching fairness, ensuring every retry makes progress, watchdog for stuck tasks.

---

## Q107: What is backpressure?

The system's way of **slowing down producers when consumers/limits can't keep up**, instead of buffering unboundedly until memory/queues explode.

- **Why needed:** infinite queues → OOM, huge latency, cascading failure.
- **Mechanisms:**
  - Bounded queues (full → reject/drop/retry later or block producer).
  - Semaphores / max concurrency on the producer side.
  - Rate limiting / throttling at the entry point.
  - Flow control in protocols (TCP windows, HTTP/2, WebSocket).
  - `asyncio.Queue(maxsize=n)` + `put` blocking when full.
- **Interview angle:** "10k concurrent LLM requests" → a bounded worker queue + semaphores = backpressure instead of OOM.

---

## Q108: What is a connection pool?

A set of pre-established, **reused** connections (DB, HTTP, Redis) managed by a pool object, instead of opening/closing per request.

- **DB:** `psycopg2.pool`, SQLAlchemy `create_engine` (pool_size + max_overflow), `asyncpg.create_pool`, connection URLs with pooling (PgBouncer).
- **HTTP:** `httpx.AsyncClient` / `aiohttp.ClientSession` reuse TCP connections (keep-alive) across requests — effectively a connection pool.
- **Benefits:** avoids 3-way TCP/TLS handshake + auth per call; amortizes setup; bounded resource usage; safe concurrent usage.

---

## Q109: Why are connection pools important in high-concurrency applications?

1. **Latency:** connection setup (TCP+TLS+auth) is expensive; pooling removes it per request.
2. **Resource limits:** PostgreSQL caps connections (~`max_connections`, default 100); a pool caps concurrent DB connections instead of 1-per-request. Without it, 1000 concurrent requests → "too many connections" errors.
3. **Stability:** healthy pool + health checks avoids connection churn and failed storms.
4. **Sizing rule of thumb:** `pool_size ≈ workers × concurrent_queries_per_worker`; oversized pools exhaust the DB.

**Failure mode to mention:** "too many clients already" — classic symptom of missing pools or oversized pool config.

---

## Q110: How would you prevent a service from creating too many database connections?

1. **Use a connection pool** (SQLAlchemy `pool_size`, `max_overflow`, `pool_timeout`).
2. **Size it correctly:** pool ≈ (uvicorn workers) × (max concurrent queries/worker); keep under DB `max_connections` with headroom.
3. **Session-per-request + close in `finally`** — return connections to the pool (Q353).
4. **Async drivers** with their own pooling (`asyncpg`, `async engine`).
5. **Connection validation** (`pool_pre_ping=True`) and recycling (`pool_recycle`) to avoid stale connections.
6. **External pooler** (PgBouncer/PgPool) for high concurrency — centralizes connection reuse.
7. **Rate-limit / queue** DB-heavy work; batch queries; cache hot reads.
8. **Monitor:** current_connections vs max; set alerts (Q630).

---

## Q111: How would you handle concurrent requests to an external API?

1. **Shared async client** with connection pooling + keep-alive (`httpx.AsyncClient` once, reuse).
2. **Bound concurrency** with a semaphore (max in-flight per host/endpoint).
3. **Timeouts** on connect/read/overall (Q116) — never hang forever.
4. **Retries with exponential backoff + jitter** (Q113–115) for transient failures.
5. **Rate limiting respect:** token bucket / pacing to stay under quota; respect `Retry-After`.
6. **Circuit breaker** — if the API is down, fail fast instead of hammering it (Q445).
7. **Caching** identical responses to avoid duplicate calls.
8. **Batching** endpoints if the provider supports it.
9. **Fallbacks / degradation** (Q679–680).
10. **Observability:** log latency/errors per provider, alert on anomaly.

---

## Q112: How would you handle API rate limits?

1. **Know the limit** — read provider docs; respect `RateLimit-Limit` / `Retry-After` headers.
2. **Client-side pacing:** token bucket / sliding window limiter (e.g., `asyncio`-based throttle) so you stay under quota.
3. **Semaphore** for max concurrent requests + sleep-based pacing for per-second rate.
4. **On 429:** back off for `Retry-After` (or exponential), retry with jitter, cap retries.
5. **Queue requests** when quota exhausted (bounded queue = backpressure, Q107).
6. **Batching:** use batch endpoints to reduce call count.
7. **Caching** repeated responses.
8. **Sharding across keys/instances** if the platform allows multiple keys.
9. **Monitor usage** — alert before hitting the cap.

```python
async def rate_limited_fetch(client, url, sem, bucket):
    async with sem:
        await bucket.wait()          # paces to requests/second
        return await client.get(url)
```

---

## Q113: How would you implement retries for failed requests?

```python
import asyncio, logging

async def fetch_with_retry(client, url, *, retries=3, base_delay=0.5, backoff=2.0, jitter=True):
    for attempt in range(retries):
        try:
            return await client.get(url, timeout=10)
        except (httpx.TimeoutException, httpx.TransportError) as e:
            if attempt == retries - 1:
                raise
            delay = base_delay * (backoff ** attempt)
            if jitter:
                delay *= random.uniform(0.5, 1.5)
            logging.warning("retry %s/%s for %s (delay=%.2fs)", attempt+1, retries, url, delay)
            await asyncio.sleep(delay)
```

- **What to retry:** network errors, 5xx, 429 (respect `Retry-After`), timeouts.
- **What NOT to retry:** 4xx client errors (400/401/403/404 — the request is wrong), validation errors.
- **Idempotency:** retrying POST needs an idempotency key so duplicates are safe (Q397).
- Add **jitter** to avoid thundering herd; cap total attempts; make it bounded.
- Use libraries: `tenacity` (declarative), `backoff`.

---

## Q114: What is exponential backoff?

Delaying retries by an exponentially growing amount: `delay = base * 2^attempt` (e.g., 0.5s, 1s, 2s, 4s...).

```python
delay = base_delay * (backoff_factor ** attempt)
```

- Why: a failing service is often overloaded; retrying instantly at the same time (thundering herd) makes it worse.
- Add **jitter** (random ±) to desynchronize clients — prevents synchronized retry waves.
- Cap the max delay; add a retry count cap; stop retrying after N attempts or a deadline.
- Respect server `Retry-After` headers when present (they take precedence).

---

## Q115: Why should retries have limits?

1. **Avoid overload** — infinite retries hammer an already-sick service (retry storm).
2. **Bounded latency** — users shouldn't wait forever; fail fast and degrade.
3. **Cost control** — each attempt may cost money (LLM calls! DB writes).
4. **Avoid duplicate side effects** — non-idempotent operations must not repeat blindly.
5. **Detect real failure** — after N attempts, raise and alert; the system needs to know it's down (→ circuit breaker).
6. **Resource protection** — endless retries exhaust threads/sockets/timeouts.

Good practice: max attempts (3–5), time budget (e.g., total ≤ 30s), jittered backoff, and a circuit breaker so you stop trying while the provider is known-down.

---

## Q116: How would you implement request timeouts?

```python
import httpx, asyncio

# httpx: connect / read / write / pool timeouts
client = httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0, read=8.0))

# per-request override
await client.get(url, timeout=15.0)

# asyncio-level timeout (works on any awaitable)
async def call():
    return await asyncio.wait_for(some_slow_op(), timeout=8.0)

# Py3.11+ idiom
async def call():
    async with asyncio.timeout(8.0):
        return await some_slow_op()
```

- **Separate timeouts:** connect (socket establishment), read (between bytes), write, total.
- On timeout: catch the exception, log, retry (bounded) or fall back, return a friendly error (408/504).
- **Never no timeout** on external calls — a hung call blocks the worker indefinitely.
- For LLM calls set generous but bounded timeouts + streaming.

---

## Q117: How would you cancel an async task?

```python
task = asyncio.create_task(some_coro())

task.cancel()          # request cancellation → CancelledError injected at next await

try:
    await task
except asyncio.CancelledError:
    # cleanup here, then re-raise if needed
    ...
```

- `cancel()` raises `CancelledError` **inside the task** at its next suspension point.
- The task should catch `CancelledError` to run cleanup (close client, roll back), then typically re-raise (or swallow only if you truly want to stop).
- `asyncio.shield(awaitable)` protects a task from being cancelled by its caller.
- `asyncio.wait_for(timeout)` internally cancels the task on timeout.
- In Python 3.11+, `asyncio.TaskGroup` cancels siblings when one fails.

---

## Q118: What happens when an async task raises an exception?

- If you `await` it: the exception **propagates** at the await point (catchable).
- If it's fire-and-forget (`create_task` without awaiting): the exception is stored on the task and surfaced when you call `task.result()`; if never retrieved, Python logs "Task exception was never retrieved" and may (3.12+) emit a warning — silently lost otherwise.
- With `gather(return_exceptions=False)`: first exception propagates, other tasks are **cancelled**.
- With `gather(return_exceptions=True)`: exceptions come back as values.
- `asyncio.TaskGroup`: first task exception cancels the rest and the group raises the first exception after all complete.
- **Best practice:** always attach a callback or await/handle tasks; add `task.add_done_callback` or `try/except` around awaits to log failures.

---

## Q119: How would you handle partial failures when running multiple concurrent operations?

1. **`gather(return_exceptions=True)`** — collect per-item outcomes; handle successes + failures separately.

```python
results = await asyncio.gather(*[fetch(u) for u in urls], return_exceptions=True)
ok = [r for r in results if isinstance(r, Response)]
errors = [r for r in results if isinstance(r, Exception)]
```

2. **`asyncio.as_completed`** — process as each finishes; fail only the individual item.
3. **Per-item isolation** — wrap each call in `try/except` so one failure can't kill the batch (partial success is *by design*).
4. **Compensating actions** — for writes: retry failed items, record them in a dead-letter/retry queue, alert.
5. **Batch-level policy** — define success threshold ("write all-or-nothing" vs "best-effort write successful items").
6. **Idempotency** so the retry of failed items is safe.
7. **Response shape:** return `{successes, failures, failed_ids}` so the client can act.

---

## Q120: How would you optimize a FastAPI endpoint that makes multiple independent API calls?

**The whole point: parallelize independent awaits** — sequential awaits serialize all the latency.

```python
# SLOW — sequential
data1 = await api1()          # 1s
data2 = await api2()          # 1s
data3 = await api3()          # 1s   → 3s total

# FAST — concurrent
async def fetch_all():
    r1, r2, r3 = await asyncio.gather(api1(), api2(), api3())   # ~1s total
```

**Full playbook:**
1. **Concurrent calls** with `asyncio.gather`/`as_completed` (above) — biggest win.
2. **Bound concurrency** with a semaphore (don't blast 100 calls).
3. **Reuse async clients** (connection pooling) instead of creating per call.
4. **Timeouts + bounded retries + backoff** (Q113, Q116).
5. **Cache** stable responses (Redis) — skip the external call entirely (Q248).
6. **Parallelize with other work:** fetch external data while running the DB query (start DB query and API calls together).
7. **Return partial data fast** — stream/return what's ready (SSE/first-chunk).
8. **Run background enrichment** after the response (background tasks/queue).
9. **Batch endpoints** if provider supports; reduce the number of calls.
10. **Metrics:** trace each call's latency; alert when p95 degrades.
