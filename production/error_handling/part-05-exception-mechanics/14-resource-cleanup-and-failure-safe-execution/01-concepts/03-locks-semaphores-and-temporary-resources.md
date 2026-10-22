# Locks, Semaphores, and Temporary Resources

> Part V · Chapter 14 · Sections 14.10, 14.11 · _Estimated reading time: 15 min_
> **Prerequisite:** [Cleanup for Common Resources](./02-cleanup-for-common-resources.md)

## In one sentence

Locks and semaphores must be **released on every path including panic/cancellation**, and temporary
resources (temp files, scratch dirs, uploads) must be **deleted even when the work fails**, or they
accumulate until the system jams or the disk fills.

## Why this matters in production

An unreleased lock is a deadlock waiting for the next caller. An unreleased semaphore permit is a
capacity leak that eventually halts a worker pool. A temp file left behind on failure is a slow
disk leak that shows up days later. These resources are invisible in the happy path and catastrophic
in aggregate — exactly the kind that need structural cleanup.

## Core concept

| Resource | Released how | Panic/cancel safe? | Leak symptom |
| -------- | ------------ | ------------------ | ------------ |
| `Mutex`/`RLock` | `unlock()` / `with` | Only if `defer`/`with` used | deadlock |
| Semaphore permit | `release()` | Only if `defer`/`with` used | capacity loss |
| Distributed lock | lease expiry / `release` | Leases expire; explicit release better | stale lock / fencing |
| Temp file | `remove()` | Needs `defer`/`finally` | disk fills |
| Scratch dir | recursive delete | Needs `defer`/`finally` | inode exhaustion |
| Multipart upload | `AbortMultipartUpload` | Timed rule; explicit better | billable residue |

### Locks/semaphores (14.10)

Rules:

1. **Acquire and release in the same scope**, using `defer`/`with`/`try/finally`.
2. **The release must run on panic.** In Go, `defer mu.Unlock()` does. A plain `mu.Unlock()` after
   the critical section does not if the section panics.
3. **Never hold a lock across a slow/blocking await** if it can be avoided — it serializes callers.
4. **Distributed locks use leases**; always set a TTL and use **fencing tokens** (Chapter 40) so a
   stale holder cannot write after its lease expires.

### Temporary resources (14.11)

Temp files, scratch directories, extraction dirs, and multipart uploads must be cleaned on:
success, failure, cancellation, and timeout. If cleanup is best-effort, also add a **sweeper**
(a periodic job that removes stale temp artifacts) as a backstop.

## How it works (mechanics)

### Mutex release on all paths

```go
mu.Lock()
defer mu.Unlock()      // runs on normal return AND on panic
// ... critical section that may panic ...
```

If the critical section calls a function that panics, the deferred `Unlock` still runs as the
goroutine unwinds. Without `defer`, the lock is held forever and every later `Lock()` blocks.

### Semaphore permit as a scope

```python
async with semaphore:          # acquires on enter, releases on exit (incl. exception)
    await do_work()
```

```ts
const release = await sem.acquire();
try {
  await doWork();
} finally {
  release();                   // capacity returned on every path
}
```

### Distributed lock with lease + fencing

```text
acquire lease(token=7, ttl=30s)
  └─ do work (must finish < ttl, or renew)
       └─ every write tags with fencing token 7
release() (or let TTL expire)
```

If the holder stalls past the TTL, another holder acquires with token 8; the stale holder's writes
(token 7) are rejected by the storage layer. This prevents two writers acting as one.

### Temporary resource lifecycle

```text
create temp ──▶ use ──▶ (success)  ──▶ delete
                       └ (failure) ──▶ delete  (in finally/defer)
                       └ (crash)   ──▶ SWEEPER deletes later
```

## Worked example

```ts
// ❌ Leaks the semaphore permit and the temp file on any throw
async function processBatch(items: Item[]) {
  await sem.acquire();
  const tmp = path.join(os.tmpdir(), `batch-${crypto.randomUUID()}`);
  await fs.writeFile(tmp, serialize(items));
  const result = await transform(tmp);   // throws → permit + temp file leaked
  await fs.unlink(tmp);
  sem.release();
  return result;
}

// ✅ Structural cleanup for both
async function processBatch(items: Item[]) {
  const release = await sem.acquire();
  const tmp = path.join(os.tmpdir(), `batch-${crypto.randomUUID()}`);
  await fs.writeFile(tmp, serialize(items));
  try {
    return await transform(tmp);
  } finally {
    await fs.unlink(tmp).catch((e) => log.warn({ e, tmp }, "temp cleanup failed"));
    release();                            // capacity returned on every path
  }
}
```

Python `with` for both a lock and a temp dir:

```python
import tempfile, threading

lock = threading.Lock()
def process(items):
    with lock:                            # released on exception too
        with tempfile.TemporaryDirectory() as tmp:   # removed on exit/exception
            path = os.path.join(tmp, "batch.json")
            write(path, serialize(items))
            return transform(path)
```

Go with `defer` ordering (LIFO):

```go
mu.Lock()
defer mu.Unlock()

dir, err := os.MkdirTemp("", "batch-*")
if err != nil {
    return err
}
defer os.RemoveAll(dir)                   // runs after the function, incl. on panic
```

## Key data / numbers

- **Redis `SET key val NX PX 30000`**: distributed lock as a lease with a 30s TTL; renew if work
  may exceed the TTL.
- **Fencing tokens** (Kleppmann's design): monotonically increasing; the storage rejects writes
  older than the latest token.
- **Go `defer`** order is LIFO; register `Unlock` and `RemoveAll` immediately after acquiring.
- **S3 multipart**: abandoned uploads are billed; configure a lifecycle rule to abort incomplete
  multipart uploads after N days as a backstop.
- **Temp sweepers**: run periodically; a missing `os.RemoveAll` on a crash otherwise leaks forever.

## Real-world use case — Acme SaaS

Acme's `AgentRun` guarded access to a shared rate-limiter with a semaphore. A bug in a tool caused
a panic mid-critical-section; because the permit was released *after* the work (not deferred), the
panic skipped the release. After enough panics, the semaphore had zero permits and all agent runs
stalled. Moving to `defer release()` fixed it. Separately, crashed export workers left temp files
behind; a nightly sweeper plus correct `defer os.RemoveAll` stopped disk growth.

## Trade-offs

| Technique | Pros | Cons | When |
| --------- | ---- | ---- | ---- |
| `defer`/`with` release | Panic/exception safe | Must be placed immediately | Always |
| Manual release | Explicit | Skips on panic/cancel | Never |
| Lease-based distributed lock | Auto-expiry | Clock skew; need fencing | Cross-process locks |
| Sweeper backstop | Cleans crashes | Delayed; extra job | Always pair with inline cleanup |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| `defer`/`with` lock release immediately after acquire | Release manually at the end |
| Set a TTL + fencing on distributed locks | Hold a distributed lock indefinitely |
| Delete temp resources in `finally`/`defer` | Delete only on success |
| Add a periodic sweeper for crashes | Assume inline cleanup always runs |
| Avoid holding locks across slow awaits | Serialize a pool on a slow dependency |

## Common mistakes

- **Release after the critical section** — skipped on panic.
- **Forgetting that a cancelled context may skip non-deferred cleanup**.
- **No TTL on a distributed lock** — a crashed holder locks forever.
- **No fencing tokens** — a stale holder writes after lease expiry.
- **Temp files deleted only on success** — accumulate on every failure.

## Checklist

- [ ] Every lock/semaphore release is `defer`/`with`/`finally`.
- [ ] Distributed locks have a TTL and fencing.
- [ ] Temp resources are removed on all paths.
- [ ] A sweeper exists as a backstop.
- [ ] Locks are not held across slow/blocking external calls.

## Related

- [Cleanup for Common Resources](./02-cleanup-for-common-resources.md)
- [Multiple Errors and Primary Preservation](./04-multiple-errors-and-primary-preservation.md)
- [Consistency and Concurrency Failures (Part XV)](../../../part-15-distributed-failures/40-consistency-and-concurrency-failures/README.md)
- [Process, Runtime, and Resource Failures (Part XV)](../../../part-15-distributed-failures/41-process-runtime-and-resource-failures/README.md)
