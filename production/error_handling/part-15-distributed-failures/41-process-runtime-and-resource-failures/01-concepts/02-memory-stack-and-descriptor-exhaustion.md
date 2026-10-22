# Memory, Stack, and Descriptor Exhaustion (41.3–41.6)

> Part XV · Chapter 41 · Sections 41.3–41.6 · _Estimated reading time: 24 min_
> **Prerequisite:** [Uncaught Exceptions and Unhandled Async Failures (41.1–41.2)](./01-uncaught-and-unhandled-failures.md)

## In one sentence

Memory, stack, file-descriptor, and socket exhaustion are **not catchable incidents** — they are
**states the process cannot leave** — so the design rule is to *detect them before they happen*,
*bound what can grow*, and *treat the kill as the correct outcome* rather than a bug to be
retried around.

## Why this matters in production

These four failures share a shape that makes them nastier than ordinary errors: **the process
keeps running after the first symptom.** A `try/catch` around `fs.readFile` catches the `EMFILE`
and returns a 500 — while the descriptor table stays full, so every *other* file, socket, and
module load now fails too. A caught `RangeError: Maximum call stack size exceeded` lets the request
return a 500 with a stack that is still nearly exhausted, so the next request dies in a different
place. The governing idea: **exhaustion is a state, not an event.** Recovering from the event
while the state persists is what turns a degraded service into a dead one.

## Core concept

### 41.3 Out of memory

There are three different "out of memory" failures, and telling them apart is the whole job:

| Failure | Who kills it | Signature | Recoverable in-process? |
|---------|--------------|-----------|------------------------|
| **Heap OOM** (V8 "JavaScript heap out of memory") | the runtime aborts | `FATAL ERROR: ... JavaScript heap out of memory`, exit **134** (`SIGABRT`) | no — the heap is exhausted; the abort is the fix |
| **Container / cgroup OOM kill** | the kernel, via the OOM killer | exit **137** (`128 + 9`), pod status `reason: OOMKilled` | no — the process is gone; the *replacement* must not repeat the mistake |
| **Native allocation failure** | the allocator returns `NULL` | `ENOMEM` (errno **12**) from the syscall | **maybe** — a single small allocation can fail while the process is otherwise healthy |

The distinction that matters operationally:

- **exit 134** + "heap out of memory" → your code's allocation. Fix the code and the heap flags.
- **exit 137** + `reason: OOMKilled` → the container limit was hit. Fix the limit or the workload.
- **`ENOMEM` on one small allocation** → transient pressure; tolerable once. A process-wide
  `ENOMEM` storm means the cgroup is out of memory and the kernel is about to kill you.

**Container memory limits** are the operating envelope, and they include more than your heap:

```text
container memory limit (e.g. 2Gi)
├── JS heap          ← V8, tunable with --max-old-space-size
├── native memory    ← buffers, Buffers, native addons, mmap
├── code + stacks    ← V8 heap + thread stacks
└── page cache       ← charged to the cgroup, but reclaimable under pressure
```

Two classic production mistakes follow from this picture:

- **Setting `--max-old-space-size` equal to the container limit.** V8 then believes it may use all
  of it, leaves no room for native allocations, and the cgroup kills the process before V8 reaches
  its own limit. Give V8 **~70–75%** of the container limit and leave the rest.
- **Ignoring that the page cache counts.** A process that writes 4 GB of export files inside a
  2 Gi container looks like it "used" far more memory than `heapUsed` suggests.

**Memory shapes** tell you the fix before you read a single stack trace:

| Shape | Signature | Usual cause |
|-------|-----------|-------------|
| Monotonic growth | RSS climbs steadily, never returns | a true leak (cache, listener, closure retention) |
| Sawtooth | climbs, drops at GC, baseline rises | leak *plus* churn — the baseline is the real signal |
| Step | jumps at a threshold and stays | one large buffer, an unbounded collection, a loaded dataset |
| Cliff | fine until a specific tenant/size | unbounded per-tenant data (e.g. loading a whole account) |

### 41.4 Stack overflow

Stack overflow is a **guard-page hit**, and whether you can catch it depends on the runtime:

| Runtime | Behavior | Catchable? |
|---------|----------|------------|
| **JavaScript / Node** | `RangeError: Maximum call stack size exceeded` | yes — the engine checks the limit before the real stack runs out |
| **Python** | `RecursionError` (default recursion limit **1000**, `sys.setrecursionlimit`) | yes, though a deep C-level call can still segfault |
| **Go** | stacks grow dynamically to a limit (default max **1 GB**); overflow is a fatal runtime error, exit **2** | no |
| **Rust** | "thread has overflowed its stack" → abort (`SIGABRT`, exit **134**) | no |
| **C / C++** | guard page → `SIGSEGV` (exit **139**) | no |

The practical consequence: **in JavaScript and Python, a `catch` around deep recursion lets you
return a 500 and keep serving; in Go, Rust, and C it does not.** In every language, catching it
is usually the wrong answer — the correct recovery is a bounded iterative algorithm plus a depth
limit that fails *before* the real stack is at risk.

Recursion also reaches production indirectly:

```text
deep JSON.parse() on a hostile payload       → stack overflow in the parser
a serializer walking a self-referential graph → infinite recursion
a regex with catastrophic backtracking       → not a stack overflow: a HANG (different failure)
mutual recursion between two modules         → stack overflow at a surprising depth
```

⚠️ **Hazard.** The last one — catastrophic backtracking — looks like a memory problem in the
metrics and a stack problem in the log. It is neither: it is a CPU hang, and it is fixed by
rewriting the pattern, not by adding memory.

### 41.5 File-descriptor exhaustion

Every open file, socket, pipe, and epoll instance consumes one entry in the process's file
descriptor table. The limits:

| Limit | Scope | Linux knob |
|-------|-------|-----------|
| **soft** `RLIMIT_NOFILE` | per process | `ulimit -n` — a process may lower it but not raise it above the hard limit |
| **hard** `RLIMIT_NOFILE` | per process | `ulimit -Hn` — only root may raise it |
| **system-wide** open files | whole host | `fs.file-max` (commonly a large fraction of RAM) |
| **system-wide** max fd value | whole host | `fs.nr_open` (commonly **1048576**) |

The two errnos you will see:

- **`EMFILE`** (errno **24**) — *this* process hit its per-process limit. Usually a leak.
- **`ENFILE`** (errno **23**) — *the whole system* hit its limit. Someone else is leaking, or the
  host is too small. Do not "fix" it by raising your own limit.

⚠️ **Hazard.** `ulimit -n` inside a container is set by the container runtime, and the values vary
enormously — historically **1024**, in many modern runtimes the host's maximum (commonly
**1048576**). **Check `ulimit -n` in the container, not on your laptop.** A service that works on a
developer machine and fails at 200 concurrent uploads in production has usually discovered the
container's `nofile` limit.

The symptom is characteristic: `EMFILE` on `accept()` means new **connections** fail (the service
looks alive but serves nothing new); `EMFILE` on `open()` means **file** operations fail. Either
way, the descriptor table is full and *the process must be recycled* — every subsequent operation
now contends for the same empty table.

### 41.6 Socket exhaustion

Sockets are file descriptors, but they have a **second, independent** limit: the ephemeral port
space.

```text
client:10.0.0.5 ──▶ server:443
   source port chosen from net.ipv4.ip_local_port_range
   Linux default: 32768 60999  → ~28,231 ports per (src ip, dst ip, dst port) tuple
   after close: TIME_WAIT for tcp_fin_timeout (default 60 s)
```

Under a connection-churning workload (short-lived HTTP connections, many upstream calls), the
port space can fill while the descriptor table still has room. Symptoms:

| Symptom | Meaning |
|---------|---------|
| `EADDRNOTAVAIL` (errno **99**) on `bind`/`connect` | ephemeral port exhaustion |
| outbound connects hang, then `ETIMEDOUT` (errno **110**) | conntrack table full (`nf_conntrack_max`) — packets are **dropped**, not refused |
| `ENOBUFS` (errno **105**) | socket buffer memory unavailable — memory pressure, not ports |

⚠️ **Hazard.** conntrack exhaustion produces **timeouts, not errors**. The packets are silently
dropped, so the symptom is a latency cliff with no error rate to alert on. If your egress
suddenly times out with no upstream errors, check `nf_conntrack_max` before you blame the provider.

The prevention is structural, not reactive: **HTTP keep-alive / connection reuse** (one connection
instead of one per request is the single biggest port and fd saver), **bounded upstream pools**
(*N* connections instead of *N* per request), and `SO_REUSEADDR` on listeners.

## How it works (mechanics)

### The descriptor lifecycle in a request handler

One missing `close()` in a loop produces the exact production incident:

```text
t0   0 open fds
t+   500 requests   → 500 open fds (leak: one per request)
t+   ulimit -n = 1024 → 1024 open fds
t+   next accept() → EMFILE → new connections rejected → 502/503 to every client
t+   the process is "healthy" by every metric except "can it accept connections"
```

### Node's independent limits (all different, all real)

| Limit | Where | Symptom when hit |
|-------|-------|------------------|
| V8 old-space heap | `--max-old-space-size` (MB) | `JavaScript heap out of memory`, exit 134 |
| Container memory | cgroup `memory.max` / k8s `resources.limits.memory` | exit **137**, `OOMKilled` |
| File descriptors | `ulimit -n` | `EMFILE` on `accept`/`open` |

Node's HTTP server also has its own timeouts, which are the difference between a *leak* and a
*pile-up*: `server.keepAliveTimeout` (default **5000 ms**), `server.headersTimeout` (default
**60000 ms**), `server.requestTimeout` (default **300000 ms**). A client that opens a socket and
never sends headers holds an fd until `headersTimeout` fires — 60 seconds of fd occupancy per
slow client. That is a **slowloris-shaped fd leak**.

## Worked example

```ts
// The leak: a stream is created per request and never destroyed on the error path.
export async function downloadExport(tenantId: string, exportId: string): Promise<Readable> {
  const file = await storage.getObject(exportPath(tenantId, exportId));
  const stream = file.createReadStream();
  stream.on("error", (err) => log.error({ err }, "export stream failed"));  // logs, never closes
  return stream;
}
```

```text
each request → one open fd on the object store
after ~1000 concurrent downloads → EMFILE
  → the upload handler's fs.open() also fails → "uploads are broken"
  → the DB driver's socket() also fails → "the database is down"
  → one fd leak took down four unrelated subsystems
```

The fixed version releases the descriptor on every path:

```ts
export async function downloadExport(tenantId: string, exportId: string): Promise<Readable> {
  const file = await storage.getObject(exportPath(tenantId, exportId));
  const stream = file.createReadStream();
  stream.on("error", (err) => {
    log.error({ err, tenantId, exportId }, "export stream failed");
    stream.destroy();                       // ← releases the fd
  });
  stream.on("aborted", () => stream.destroy());
  return stream;
}
```

The belt-and-braces guard turns an unbounded leak into a *bounded* one: alert when the open-fd
count crosses **75% of `ulimit -n`** (see the [chapter reference](../05-reference/README.md)).

## Key data / numbers

- **Exit codes**: `134` = `SIGABRT` (V8 heap OOM abort), `137` = `128 + 9` = `SIGKILL` (cgroup
  OOM-kill *or* an external kill), `139` = `128 + 11` = `SIGSEGV`, `143` = `128 + 15` = `SIGTERM`.
- **Errno values (Linux)**: `ENOMEM` **12**, `EMFILE` **24**, `ENFILE` **23**, `EAGAIN` **11**,
  `EADDRNOTAVAIL` **99**, `EADDRINUSE` **98**, `ENOBUFS` **105**, `ECONNRESET` **104**,
  `ECONNREFUSED` **111**, `ETIMEDOUT` **110**, `EPIPE` **32**, `EINTR` **4**.
- **Container memory limits**: cgroups v2 `memory.max`, cgroups v1 `memory.limit_in_bytes`;
  Kubernetes `resources.limits.memory`. Give V8 **~70–75%** of the container limit.
- **V8 heap**: `--max-old-space-size=<MB>`; always set it explicitly against your container limit
  (Node's own default is roughly **4 GB** on 64-bit hosts with enough RAM, **~2 GB** otherwise).
- **`ulimit -n`**: soft limit per process (`ulimit -n`), hard limit (`ulimit -Hn`); check it
  **inside the container**. Linux `fs.nr_open` default **1048576**, `fs.file-max` is host-wide.
- **Ephemeral ports**: `net.ipv4.ip_local_port_range` default `32768 60999` → **~28,231** ports
  per tuple; `tcp_fin_timeout` default **60 s** holds them in `TIME_WAIT`.
- **Conntrack**: `nf_conntrack_max` commonly **262144**; exceeding it drops packets silently →
  timeouts, not errors.
- **Postgres SQLSTATEs**: `53200` `out_of_memory`, `53300` `too_many_connections`,
  `53400` `configuration_limit_exceeded`. MySQL: `1040` too many connections, `1041` out of
  resources.
- **Python** recursion limit default **1000**; **Go** max goroutine stack default **1 GB**
  (`debug.SetMaxStack`), Go **1.19+** soft memory limit via `GOMEMLIMIT` / `debug.SetMemoryLimit`.

## Real-world use case — Acme SaaS

Acme's `ExportJob` worker streamed a CSV export by buffering each tenant's rows in memory before
writing. A 40M-row export for one large tenant pushed RSS past the container's **2 Gi** limit; the
cgroup OOM killer sent `SIGKILL`, the pod exited **137** with `reason: OOMKilled`, and the
restarted pod re-read the same job from the queue and re-ran out of memory — a **crash loop** that
also held the export lease, so the job never completed and the tenant saw a spinner for an hour.

Separately, the upload handler created a read stream per chunk and only closed it on the success
path; a client that aborted mid-upload leaked one fd. After ~1000 aborted uploads the worker hit
**`EMFILE`** on `accept()` and then on `fs.open()` for the export spool — the same process now
could not accept connections *or* write files, and the incident looked like three unrelated
outages.

The fixes were structural: the export now **streams** rows to the object store instead of
buffering them, and the job's memory is bounded by page size rather than result size; the cgroup
limit stayed at 2 Gi but V8's `--max-old-space-size` was set to **1536 MB** so the process gets a
clean `134` heap-OOM abort with a JS stack trace instead of a `137` kill with no diagnostics; the
upload handler now destroys the stream on `error` and `aborted`, and the worker **alerts when open
fds exceed 75% of `ulimit -n`** — a warning that fired days before the original `EMFILE`
incident. Exports of that size now complete, and the fd-headroom alert has caught two leaks
before they reached production.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| **Catch and continue** | no downtime | exhaustion is a state; the process stays broken | only for a single small `ENOMEM` allocation |
| **Terminate and let the orchestrator restart** | clean, fast recovery | only works if the new process doesn't repeat the mistake | default for OOM/`EMFILE` |
| **Bound the resource in code** (streaming, paging, pooling) | prevents the failure entirely | more code | default — this is the real fix |
| **Raise the limit** (memory, `nofile`, pool size) | buys headroom | defers the same failure | when the workload is genuinely larger and bounded |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Bound every collection, buffer, and cache | Load a whole tenant into memory "for now" |
| Stream large results instead of buffering | Buffer a 40M-row export to write one CSV |
| Set `--max-old-space-size` below the container limit | Set it equal to the container limit |
| Alert on fd headroom and RSS growth shape | Wait for `EMFILE` to page you |
| Close sockets/streams on every path, including abort | Close only on the success path |
| Check `ulimit -n` inside the container | Assume your laptop's limit applies |
| Treat `EMFILE`/`ENOMEM` as a signal to exit | Catch `EMFILE` and keep serving 500s |

## Common mistakes

- **Catching `EMFILE` and retrying the open** — the table is still full; the retry fails the same
  way, faster.
- **Treating `137` as "the platform killed us, ignore it"** — `137` is the OOM-killer's signature
  and must page someone.
- **Streaming without an `error` handler that destroys the stream** — the leak only shows up under
  aborts, which is exactly when production is busiest.
- **Assuming a caught `RangeError` means the recursion is handled** — the *bug* remains, and the
  next deep call may land in a native frame that cannot be caught.
- **Growing `--max-old-space-size` to fix a leak** — you have converted a fast, diagnosable crash
  into a slow, opaque one.

## Checklist

- [ ] Every large result set is streamed or paged; no unbounded in-memory buffers.
- [ ] Container memory limit, V8 heap flag, and fd limit are explicitly set and documented.
- [ ] V8 heap ≤ ~75% of the container memory limit.
- [ ] Open-fd count, RSS, and heap growth shape are monitored with alerts.
- [ ] Streams and sockets are closed/destroyed on success, error, and abort paths.
- [ ] Exit code `137` is treated as an OOM alert, not noise.
- [ ] Pool sizes are bounded and derived from the fd budget, not from the machine's core count.

## Related

- [Pool, Queue, and CPU Pressure (41.7–41.9)](./03-pool-queue-and-cpu-pressure.md)
- [Uncaught Exceptions and Unhandled Async Failures (41.1–41.2)](./01-uncaught-and-unhandled-failures.md)
- [Python and Go: OOM and Resource-Limit Handling](../03-practical-examples/02-python-and-go-resource-limit-handling.md)
- [Cleanup for Common Resources](../../../part-05-exception-mechanics/14-resource-cleanup-and-failure-safe-execution/01-concepts/02-cleanup-for-common-resources.md)
- [Connection and Pool Errors](../../../part-09-database-and-transactions/22-database-error-classification/01-concepts/01-connection-and-pool-errors.md)
