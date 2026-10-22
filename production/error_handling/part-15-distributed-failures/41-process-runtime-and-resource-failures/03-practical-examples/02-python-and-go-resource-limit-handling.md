# Python and Go — OOM and Resource-Limit Handling

> Part XV · Chapter 41 · Sections 41.3, 41.5, 41.7, 41.16, 41.17 · _Estimated reading time: 25 min_
> **Prerequisite:** [Memory, Stack, and Descriptor Exhaustion (41.3–41.6)](../01-concepts/02-memory-stack-and-descriptor-exhaustion.md)

## In one sentence

Python and Go fail differently on the same resource — **Python lets you catch `MemoryError` and
`RecursionError`, Go lets you catch neither** — so the *only* portable strategy is the same in
both: **bound the resource in code, detect the pressure before it bites, and treat exhaustion as
a reason to exit rather than to continue.**

## Why this matters in production

The languages differ in a way that catches teams out during a migration. A Python service that
catches `MemoryError` and keeps running believes it has a recovery path. It does not: the allocation
failed because the process was at its ceiling, and the next few allocations fail too — including the
ones your recovery code needs. A Go service has **no** `MemoryError` to catch: the runtime's
out-of-memory is a fatal error that exits with status **2** and prints every goroutine's stack. The
Go failure is louder and, honestly, safer.

The same split shows up with file descriptors. Python's `open()` raises `OSError` with `errno.EMFILE`
(**24**) and Go returns a `*os.SyscallError` wrapping `syscall.EMFILE`; both are catchable, and in both
**catching is the wrong move** — the table is full, the leak is still leaking, and every subsequent
operation fails the same way.

## Python — memory, recursion, and descriptors

### Reading the limits the process actually has

```python
import resource, os

soft_nofile, _ = resource.getrlimit(resource.RLIMIT_NOFILE)   # e.g. 1024
in_use   = len(os.listdir("/proc/self/fd"))
mem_max  = open("/sys/fs/cgroup/memory.max").read().strip()    # cgroups v2: bytes or "max"
```

This is the number that matters. A container's `nofile` limit is set by the runtime and is often
**1024** even though the host allows **1048576** — which is why a service that works on a laptop
fails at 200 concurrent downloads in production.

### `MemoryError` — catch it only to die properly

```python
# ❌ The trap: "handling" MemoryError without changing anything — the process stays at its
#    ceiling, so the next allocation fails too (including the one inside the logging call).
def render_export_safe(rows) -> bytes:
    try:
        return render_export(rows)
    except MemoryError:
        raise ServiceBusy("EXPORT_TOO_LARGE", http=503)
```

The correct handling has two parts: **the operation** is bounded so it cannot happen again, and
**the process** exits so the ceiling is reset.

```python
# ✅ Bound the work: stream in fixed chunks instead of buffering the whole result.
def stream_export(rows, sink, chunk_bytes: int = 1 << 20) -> int:
    written, buf = 0, bytearray()
    for row in rows:
        buf.extend(row)
        if len(buf) >= chunk_bytes:
            sink.write(buf); written += len(buf); buf.clear()
    if buf:
        sink.write(buf); written += len(buf)
    return written

# ✅ If the ceiling is hit anyway, exit — do not keep serving at the ceiling.
def export_worker(job):
    try:
        stream_export(job.rows(), job.sink())
    except MemoryError as exc:
        log.critical({"job_id": job.id, "err": repr(exc)}, "oom during export — terminating")
        raise SystemExit(1) from exc        # SystemExit is not caught by `except Exception`
```

`raise SystemExit(1)` (or `os._exit(1)` after flushing) is the honest response: the *only* way to
get a fresh ceiling is a new process.

### `RecursionError` and the recursion limit

```python
import sys, threading

sys.setrecursionlimit(100_000)                 # ❌ alone: segfault, not RecursionError
threading.stack_size(64 * 1024 * 1024)         # ✅ real 64 MB stack first, then the limit
threading.Thread(target=run_worker, daemon=True).start()
```

The rule: **a depth limit that fails fast beats a stack overflow.** `RecursionError` is catchable,
which makes it *more* dangerous than a segfault — you keep serving with a stack that is almost gone.

### Descriptors: `EMFILE` is a terminal state

```python
def open_stream(path):
    try:
        return open(path, "rb")
    except OSError as exc:
        if exc.errno in (errno.EMFILE, errno.ENFILE):   # 24 = this process, 23 = whole host
            log.critical({"errno": exc.errno}, "fd table full — terminating")
            raise SystemExit(1) from exc                # rationing will not help
        raise
```

### Bounded pool acquisition

```python
import psycopg_pool

pool = psycopg_pool.ConnectionPool(conninfo="", min_size=1, max_size=5, timeout=1.0,
    kwargs={"options": "-c statement_timeout=5000"}, open=False)

def fetch_tenant(tenant_id):
    try:
        with pool.connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT ... WHERE tenant_id = %s LIMIT 200", (tenant_id,))
            return cur.fetchall()
    except psycopg_pool.PoolTimeout:
        raise ServiceBusy("DB_POOL_EXHAUSTED", http=503, retry_after=2)
```

Three bounds, all necessary: **pool size** (how many sessions), **acquire timeout** (how long a
caller waits), and **`statement_timeout`** (how long one statement may hold a session).

## Go — memory, panics, and descriptors

### The soft memory limit (Go 1.19+)

Go's garbage collector has a **soft memory limit**: it works harder as the heap approaches the limit,
and if the limit is genuinely exceeded the runtime fails with a fatal, uncatchable error that exits
the process with status **2**.

```go
func init() {
    // Soft limit: the GC keeps the heap under this, working harder as it approaches.
    debug.SetMemoryLimit(768 << 20) // 768 MiB — below the 1 GiB container limit
}
```

- **`GOMEMLIMIT`** — soft heap limit (Go 1.19+); **`GOGC`** — GC target (default **100**);
  **`GOMAXPROCS`** — OS threads running Go code (default = visible CPUs, *not* the cgroup quota).
  Setting `GOMAXPROCS` below the container's CPU limit stops the scheduler thrashing against the quota.

### `panic` and `recover` — the rule that catches people

```go
// ❌ recover() in a DIFFERENT goroutine does nothing. The panic still kills the process.
func startWorker() {
	go func() {
		defer func() { recover() }()   // recovers the wrong goroutine's panic — never fires
		work()
	}()
}
```

`recover()` only works when called **in a deferred function of the panicking goroutine's own stack
frame**. An unrecovered panic in *any* goroutine terminates the program — with a stack trace of every
goroutine, which is genuinely useful. The production pattern is a **recover boundary per goroutine**:

```go
func safeGo(name string, fn func()) {
	go func() {
		defer func() {
			if r := recover(); r != nil {
				log.Printf("panic in %s: %v\n%s", name, r, debug.Stack())
				metrics.Inc("worker_panic_total", "worker", name)
			}
		}()
		fn()
	}()
}
```

### HTTP server bounds and graceful shutdown

```go
srv := &http.Server{Addr: ":8080", ReadHeaderTimeout: 5 * time.Second, ReadTimeout: 30 * time.Second,
    WriteTimeout: 60 * time.Second, IdleTimeout: 120 * time.Second}

ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGTERM, syscall.SIGINT)
defer stop()
go func() {
    <-ctx.Done()
    drain, cancel := context.WithTimeout(context.Background(), 20*time.Second)
    defer cancel()
    if err := srv.Shutdown(drain); err != nil { srv.Close() }   // force-close what is left
}()
log.Fatal(srv.ListenAndServe())
```

### Bounded outbound connections and fd headroom

```go
transport := &http.Transport{MaxIdleConns: 100, MaxIdleConnsPerHost: 20,
    MaxConnsPerHost: 40, IdleConnTimeout: 90 * time.Second, TLSHandshakeTimeout: 10 * time.Second}
client := &http.Client{Transport: transport, Timeout: 15 * time.Second}

func openFDs() int { e, err := os.ReadDir("/proc/self/fd"); if err != nil { return -1 }; return len(e) }

// Alert before the table is full — 75% of the soft limit is a good tripwire.
func checkFDHeadroom(softLimit uint64) {
    if used := uint64(openFDs()); softLimit == 0 || used*4 >= softLimit*3 { metrics.Inc("fd_headroom_low") }
}
```

`MaxConnsPerHost` stops an outbound dependency consuming your **descriptors**: every outbound
connection is an fd, and an unbounded client is an `EMFILE` waiting to happen.

## Key data / numbers

- **Errno values (Linux)**: `EMFILE` **24**, `ENFILE` **23**, `ENOMEM` **12**, `EAGAIN` **11**,
  `ETIMEDOUT` **110**, `ECONNRESET` **104**. Go: `syscall.EMFILE` etc.; Python: `errno.EMFILE`.
- **Exit codes**: Go fatal runtime error / panic → **2**; Python `sys.exit(1)` → **1**; container
  OOM-kill → **137**; `SIGSEGV` → **139**; `SIGABRT` (V8 OOM) → **134**.
- **Go**: `debug.SetMemoryLimit` (**1.19+**) and `GOMEMLIMIT`; default `GOGC` **100**; `GOMAXPROCS`
  defaults to visible CPUs, not the cgroup quota.
- **Go** `http.Server` zero values are **no timeout at all** — set `ReadTimeout`/`WriteTimeout`/
  `IdleTimeout` explicitly; `ReadHeaderTimeout` is the slowloris guard.
- **ulimit**: `ulimit -n` (soft) / `ulimit -Hn` (hard) — **check inside the container**; runtimes
  often set **1024** while the host allows **1048576**. Linux `fs.nr_open` default **1048576**.
- **Container memory**: cgroups v2 `memory.max`, v1 `memory.limit_in_bytes`, K8s
  `resources.limits.memory`. Exceeding it = `SIGKILL` → **137**.

## Real-world use case — Acme SaaS

Acme ran two services in this pair of languages, and both hit the same wall from different
directions.

**The Python `ExportJob` worker** caught `MemoryError` and returned a `503` to the request that
triggered it. The intent was graceful degradation; the effect was a *stuck ceiling*. Because the
worker kept its memory, the next export — for a different tenant — failed the same way; GC slowed,
the worker's event-loop latency climbed, and the API pods sharing the node began timing out too. The
pod was finally `OOMKilled` (exit **137**) after 40 minutes of degrading.

The fix was structural: the export now **streams** rows to object storage in 1 MiB chunks, so memory
is bounded by chunk size rather than result size; the `MemoryError` handler now **exits**
(`raise SystemExit(1)`); and the worker reads `/sys/fs/cgroup/memory.max` at boot and alerts when RSS
crosses **80%**. A 40M-row export now runs in constant memory.

**The Go `WebhookIngest` service** leaked an fd on the error path: an `http.Response.Body` was never
closed, so every failed Stripe call leaked one. After roughly a day the process hit `EMFILE` on
`http.Transport` dial — and because it retried with the *same* client, every retry failed identically.
The symptom was "Stripe is down"; the cause was our own descriptor table, which was **full**.

The fix was three lines — a `defer resp.Body.Close()` on every response path, the `MaxConnsPerHost: 40`
bound, and one alert (`fd_headroom_low` at **75%** of `ulimit -n`). The alert fired on the day of the
fix and has since caught two leaks in staging. The outage lasted **6 hours** — because it was
misattributed to Stripe for its first 5.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| **Bound the resource in code** (stream, page, cap) | the failure never happens | more code | always — this is the fix |
| **Catch `MemoryError` and degrade** | no crash | keeps the process at the ceiling; the next allocation fails too | only for a small, bounded allocation |
| **Exit on `MemoryError`** | a fresh ceiling | loses in-flight work | when the process state is suspect |
| **Raise the memory limit** | buys headroom | defers a leak | when the workload is genuinely larger |
| **Set Go's soft memory limit (`GOMEMLIMIT`)** | GC works harder before the fatal error | does not prevent the fatal error | always in containers |
| **Raise the recursion limit** | deeper recursion works | can segfault without a bigger stack | only with a bigger stack, per thread |
| **Recover panics per goroutine** | one bad job does not kill the service | hides bugs if unmonitored | for background workers, with a metric |
| **Let panics crash the process** | loud, correct, with a full stack dump | downtime for a bad payload | for request-path code |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Read the real limits at boot (`ulimit -n`, `memory.max`) | Assume the host's limits apply in the container |
| Stream large results instead of buffering | Buffer a whole export in memory |
| Exit the process on `MemoryError` | Return a `503` and keep serving at the ceiling |
| Bound the pool with size + acquire timeout + `statement_timeout` | Wait for a connection forever |
| Set `GOMEMLIMIT` below the container limit | Let the runtime hit the cgroup limit |
| Set `GOMAXPROCS` below the container CPU limit | Run 16 threads on a 1-CPU container |
| `defer resp.Body.Close()` on every response path | Close bodies only on the success path |
| Bound outbound connections with `MaxConnsPerHost` | Let an outbound client consume your fds |
| Give deep recursion an explicit depth limit | Catch `RecursionError` and keep serving |
| Recover panics per goroutine with a metric | `recover()` in the wrong goroutine |

## Common mistakes

- **Catching `MemoryError` and continuing** — the process is at its ceiling; the recovery code
  cannot allocate either.
- **Raising `sys.setrecursionlimit` without raising the stack size** — the interpreter segfaults
  instead of raising `RecursionError`.
- **Assuming Go's `http.Server` has timeouts** — the zero value is *no timeout*; slow clients hold
  connections forever.
- **Leaving `GOMAXPROCS` at the host's CPU count in a CPU-limited container** — the scheduler
  thrashes against the CFS quota.
- **Not closing response bodies on the error path** — an `EMFILE` leak that presents as "the upstream
  is down".
- **Retrying with the same exhausted client** — the retry cannot succeed when the resource is gone.

## Checklist

- [ ] The container's `ulimit -n` and `memory.max` are read at boot and logged.
- [ ] Large results are streamed or paged; no unbounded in-memory buffers.
- [ ] `MemoryError` terminates the process rather than degrading it.
- [ ] Recursion has an explicit depth limit, and any raised recursion limit comes with a bigger
      thread stack.
- [ ] Pools have a size, an acquire timeout, and a statement timeout.
- [ ] Go: `GOMEMLIMIT` is below the container limit; `GOMAXPROCS` matches the CPU limit.
- [ ] Go: `ReadHeaderTimeout`, `ReadTimeout`, `WriteTimeout`, and `IdleTimeout` are set.
- [ ] Every outbound response body is closed on every path; outbound connections are bounded.
- [ ] Alerts fire at ~75–80% of the fd limit and ~80% of the memory limit.

## Related

- [Memory, Stack, and Descriptor Exhaustion (41.3–41.6)](../01-concepts/02-memory-stack-and-descriptor-exhaustion.md)
- [Pool, Queue, and CPU Pressure (41.7–41.9)](../01-concepts/03-pool-queue-and-cpu-pressure.md)
- [Process Recovery Limits and When to Terminate — deep dive](../02-deep-dive/01-process-recovery-limits-and-termination.md)
- [Language-Level Error Semantics (Ch. 47)](../../../part-18-languages-and-frameworks/47-language-level-error-semantics/README.md)
- [Connection and Pool Errors](../../../part-09-database-and-transactions/22-database-error-classification/01-concepts/01-connection-and-pool-errors.md)
