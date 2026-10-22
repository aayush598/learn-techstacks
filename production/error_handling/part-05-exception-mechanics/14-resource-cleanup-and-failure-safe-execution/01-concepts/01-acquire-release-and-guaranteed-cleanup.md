# Acquire/Release and Guaranteed Cleanup

> Part V · Chapter 14 · Sections 14.1, 14.2, 14.3, 14.4 · _Estimated reading time: 16 min_
> **Prerequisite:** [Catch Blocks and Recovery Logic](../../13-catch-blocks-and-recovery-logic/README.md)

## In one sentence

**Acquire and release in the same scope**, and make the release **guaranteed by the language's
scope mechanism** (`finally`, `using`, `defer`, context manager) so it runs whether the body
succeeds, throws, times out, or is cancelled.

## Why this matters in production

Every resource has a finite supply: connections (pool-limited), file descriptors (ulimit), locks
(exclusive), temp disk (bounded), memory. A leak does not announce itself; it accumulates until a
pool exhausts, a process hits its fd limit, or a lock deadlocks. The leak almost always occurs on
the *failure* path, which is exactly the path hand-written cleanup forgets. Guaranteed cleanup is
the difference between a system that survives failures and one that degrades with each one.

## Core concept

The acquire/release contract:

```text
acquire()  ──▶ use  ──▶ release()
                 │
                 └── throws / times out / cancelled ──▶ release() STILL runs
```

| Term | Meaning |
| ---- | ------- |
| **Acquire** | Obtain a bounded resource (connection, lock, fd, lease) |
| **Release** | Return/invalidate it so others can use it |
| **Guaranteed cleanup** | Release happens on every exit path |
| **Scoped management** | The language ties release to the lexical scope |

The key property: release must not depend on the body finishing. It must depend on the **scope
ending**, which the runtime controls.

### Guaranteed cleanup (14.2)

Three mechanisms provide it:

| Language | Mechanism | Runs on |
| -------- | --------- | ------- |
| Java | `try (Resource r = …) {}` | normal + throw |
| C# | `using (var r = …) {}` | normal + throw |
| Python | `with open(...) as f:` | normal + exception |
| Go | `defer r.Close()` | normal + panic (not on `os.Exit`) |
| JS/TS | `try { } finally { }` (or `using` with explicit resource management) | normal + throw |
| Rust | `Drop` (RAII) | normal + panic (unless `mem::forget`) |

### finally-style (14.3)

`finally` runs as the stack unwinds. Critical caveat: **if `finally` throws, it replaces any
in-flight exception**. Never let cleanup throw over the primary error (14.13).

### Scoped management (14.4)

The strongest form ties the resource's lifetime to a lexical block. You cannot forget to release
because there is no "end of function" to reach — the block's end *is* the release. Prefer scoped
management over manual `try/finally` when the language offers it.

## How it works (mechanics)

For `try/finally`:

1. Enter `try`.
2. Body runs. If it throws, the exception is held.
3. `finally` runs — always.
4. If `finally` completes normally, the held exception (if any) resumes unwinding.
5. If `finally` throws, its exception **replaces** the held one.

```text
try body throws E1 ──▶ finally runs ──▶ finally throws E2 ──▶ E1 LOST (unless suppressed)
```

For `defer`/`Drop`, cleanup is registered at acquire time and runs LIFO at scope exit or during
unwind.

## Worked example

```ts
// ❌ Manual release: leaks on any throw between acquire and release
async function query() {
  const conn = await pool.acquire();
  const rows = await conn.query("select ..."); // throws → conn never released
  conn.release();
  return rows;
}

// ✅ Guaranteed release
async function query() {
  const conn = await pool.acquire();
  try {
    return await conn.query("select ...");
  } finally {
    conn.release(); // runs on success AND on throw
  }
}
```

Same idea in each language:

```java
// Java try-with-resources — release guaranteed, AutoCloseable
try (Connection conn = pool.getConnection();
     PreparedStatement ps = conn.prepareStatement(SQL)) {
    return ps.executeQuery();
} // conn + ps closed on every path
```

```python
# Python context manager
with pool.acquire() as conn:      # __exit__ releases even on exception
    return conn.query(SQL)
```

```go
// Go defer (LIFO)
conn, err := pool.Acquire(ctx)
if err != nil {
    return err
}
defer conn.Release()               // runs on return AND on panic
return conn.Query(ctx, SQL)
```

## Key data / numbers

- **Postgres default `max_connections`**: 100 — a leaked connection per failed request exhausts the
  pool quickly under load.
- **Linux default `ulimit -n`**: often 1024 — leaked file descriptors/sockets hit this and cause
  `EMFILE`/`too many open files`.
- **`defer` does NOT run on `os.Exit`** in Go, nor on process `SIGKILL`; cleanup must be registered
  *before* a possible exit.
- **Python `with`** calls `__exit__(type, value, tb)`; returning a truthy value suppresses the
  exception — usually a mistake for cleanup.
- **Java** `AutoCloseable.close()` may throw; try-with-resources attaches it as suppressed to the
  primary. This is the model to imitate elsewhere.

## Real-world use case — Acme SaaS

Acme's API opened a DB connection per request and released it at the end of the handler. When a
validation error threw early, the release was skipped. Under normal load this was invisible; during
a burst of validation failures the pool exhausted and the whole API returned `500`s for unrelated
tenants. Wrapping the handler body in `try/finally` (release in `finally`) fixed it, and a follow-up
refactor moved to a scoped transaction helper so release could never be forgotten again.

## Trade-offs

| Mechanism | Guarantees | Caveats |
| --------- | ---------- | ------- |
| Manual release | Nothing on failure | Leaks on any throw |
| `try/finally` | Runs on throw | `finally` throwing replaces the error |
| try-with-resources / `using` | Runs + suppressed on close error | Needs `AutoCloseable`/`IDisposable` |
| Context manager (`with`) | Runs; can suppress | `__exit__` truthiness can hide errors |
| `defer`/`Drop` | Runs during unwind | Not on hard exit/`SIGKILL` |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Release in `finally`/`using`/`with`/`defer` | Release only at the end of the happy path |
| Acquire and release in the same scope | Acquire here, release in a caller |
| Prefer scoped management | Hand-roll `try/finally` when `using` exists |
| Keep cleanup unable to throw over primary | Let `finally` throw freely |
| Release before a process exits | Rely on `defer` after `os.Exit` |

## Common mistakes

- **Release after the last statement** — skipped on throw.
- **`try { acquire; ... } finally { release }` with the acquire inside the try** — if acquire
  throws, `finally` releases a null/unacquired resource.
- **Assuming GC closes resources** — GC is not deterministic; sockets/fds leak.
- **Returning from inside `try` without `finally`** — release skipped.
- **Trusting `defer` after `os.Exit`/`log.Fatal`** — it never runs.

## Checklist

- [ ] Every acquire has a matching release in the same scope.
- [ ] Release uses a scope mechanism, not end-of-function.
- [ ] Acquire happens *before* the try so `finally` never releases an unacquired resource.
- [ ] Cleanup runs on cancellation/timeout as well as throw.
- [ ] No path returns from inside `try` without guaranteed cleanup.

## Related

- [Cleanup for Common Resources](./02-cleanup-for-common-resources.md)
- [Scoped Cleanup Mechanics](../02-deep-dive/01-scoped-cleanup-mechanics.md)
- [try/finally and using Patterns](../03-practical-examples/01-try-finally-and-using-patterns.md)
- [Transaction and Rollback Error Handling (Part IX)](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
