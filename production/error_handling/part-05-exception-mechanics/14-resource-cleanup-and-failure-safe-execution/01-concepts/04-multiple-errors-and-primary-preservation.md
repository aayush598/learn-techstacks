# Multiple Errors and Primary Preservation

> Part V · Chapter 14 · Sections 14.12, 14.13 · _Estimated reading time: 16 min_
> **Prerequisite:** [Acquire/Release and Guaranteed Cleanup](./01-acquire-release-and-guaranteed-cleanup.md)

## In one sentence

When the body fails **and** cleanup fails, you have two errors: keep the **body failure as the
primary** (that is what the caller must handle) and attach the cleanup failure as **suppressed**
(diagnostic), never letting cleanup overwrite the original.

## Why this matters in production

Cleanup runs on the failure path, so it is *more* likely to fail exactly when the system is already
unhealthy — the network is down, the DB is gone. If the cleanup error replaces the primary, every
incident in that window reports the same misleading cleanup message, and the real cause is erased.
This single mistake makes outages undiagnosable and is trivially preventable.

## Core concept

Two failures travel together:

| Error | Role | Who cares | Must be |
| ----- | ---- | --------- | ------- |
| **Primary** | The operation's failure | The caller, alerts | Reported first, intact |
| **Secondary/suppressed** | Cleanup/rollback failure | Debugging | Attached, not thrown over |

The rule: **the first failure is the primary; every later failure in the same operation is
suppressed.** Do not reorder them.

```text
body throws P ──▶ cleanup throws S ──▶ report: P (cause), S (suppressed)
```

### Multiple errors (14.12)

Multiple errors arise from:
- body + cleanup (the common case),
- parallel work (several independent failures — use `errors.Join` / aggregated results),
- a saga where several compensating steps fail.

The pattern is always: **one primary, N suppressed/aggregated**, and the primary is defined by
*when* the failure first occurred (earliest wins), not by which is "scarier".

## How it works (mechanics)

### Java — first-class suppression

```java
Connection conn = pool.getConnection();
try {
    doWork(conn);                 // throws PrimaryException
} catch (PrimaryException primary) {
    try {
        cleanup(conn);            // throws SecondaryException
    } catch (SecondaryException secondary) {
        primary.addSuppressed(secondary);   // attach; do NOT throw
    }
    throw primary;                // primary is reported
} finally {
    conn.close();                 // if this throws, Java attaches it as suppressed automatically
}
```

Try-with-resources does the suppression for you: if the body throws and `close()` throws, the close
exception is suppressed by the body exception.

### Go — `errors.Join` for parallel, wrap for sequential

```go
if err := doWork(conn); err != nil {
    primary := err
    if cerr := cleanup(conn); cerr != nil {
        return errors.Join(primary, fmt.Errorf("cleanup failed: %w", cerr))
    }
    return primary
}
```

### Python — implicit context

```python
try:
    do_work(conn)                  # raises Primary
finally:
    conn.close()                   # if this raises, it becomes __context__ of... careful
```

Note: in Python, if `finally` raises, it **replaces** the primary unless you catch it. So:

```python
try:
    do_work(conn)
except Exception as primary:
    try:
        conn.close()
    except Exception as secondary:
        primary.add_note(f"cleanup also failed: {secondary!r}")  # 3.11+
    raise                              # re-raise primary
else:
    conn.close()
```

### Node/TS — carry a `suppressed` field explicitly

```ts
try {
  await doWork(conn);
} catch (primary) {
  let suppressed: unknown;
  try { await cleanup(conn); }
  catch (secondary) { suppressed = secondary; }
  throw new WorkFailed("doWork failed", { cause: primary, suppressed });
}
```

## Worked example — before/after trace

**Before** (cleanup overwrites primary):

```java
try {
    processOrder();          // throws InsufficientFunds (the real problem)
} finally {
    conn.close();            // throws "connection already closed"
}
```

Result: every incident in the outage window logs `"connection already closed"` — the real cause
(`InsufficientFunds`) is gone.

**After** (primary preserved, secondary attached):

```java
try {
    processOrder();
} catch (Exception primary) {
    try {
        conn.close();
    } catch (Exception cleanupErr) {
        primary.addSuppressed(cleanupErr);
    }
    throw primary;
}
```

Result:

```text
InsufficientFunds: order 8891 has balance 0, needs 4200
    at processOrder (Order.java:64)
    Suppressed: SQLException: connection already closed
        at Connection.close (Connection.java:212)
```

The primary is intact; the cleanup problem is visible but subordinate.

## Key data / numbers

- **Java `Throwable.addSuppressed` / `getSuppressed`** since Java 7; the try-with-resources contract
  relies on it.
- **Go `errors.Join`** since Go 1.20; a multi-error is transparent to `errors.Is/As`.
- **Python 3.11+ `BaseException.add_note`** attaches free-form notes; `__context__` links the
  implicit cause during `finally`.
- **Node**: no native suppression; a `suppressed` array field is the convention.
- **Aggregation cap**: cap joined errors (e.g. first 10 + a count) to keep logs bounded under
  mass failure.

## Real-world use case — Acme SaaS

During a Postgres failover, Acme's API handlers threw a DB connection error. Their `finally` closed
the connection, which also threw because the socket was already gone. Because the close ran in
plain `finally`, every log line said `"cannot close a closed connection"` and the DB failover cause
was invisible. On-call spent 20 minutes on the wrong problem. The fix wrapped cleanup and attached
it as suppressed, so the failover cause led every log. MTTR dropped immediately.

## Trade-offs

| Strategy | Pros | Cons | When |
| -------- | ---- | ---- | ---- |
| Throw cleanup error | Simple | Erases primary | ❌ Never |
| Suppress cleanup error | Both preserved | Needs a suppressed store | Default |
| Log cleanup error only | Works everywhere | Not structured | Acceptable fallback |
| Combined error tree | Full picture | Bigger, must design | Sagas, parallel failures |
| Aggregate with cap | Bounded logs | Truncates detail | Mass failure |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the first failure as primary | Let cleanup replace the primary |
| Attach cleanup failures as suppressed | Discard the cleanup failure |
| Wrap cleanup in its own try | Let it throw over the primary |
| Cap aggregated parallel errors | Join thousands of errors into one log |
| Define primary as "earliest failure" | Define primary as "scariest" |

## Common mistakes

- **Plain `finally { close() }`** where close can throw — overwrites the primary.
- **Throwing the cleanup error** because it "seems worse" — the caller needed the primary.
- **Losing the secondary entirely** — no record cleanup failed.
- **Unbounded aggregation** — a mass failure produces a megabyte log line.

## Checklist

- [ ] Cleanup that can throw is wrapped in its own try.
- [ ] The primary (body) error is reported first.
- [ ] The cleanup error is attached as suppressed/extra.
- [ ] Parallel errors are aggregated with a cap.
- [ ] Logs show the primary as the cause and cleanup as subordinate.

## Related

- [Cleanup Timeouts, Cancellation, and Idempotency](./05-cleanup-timeouts-cancellation-and-idempotency.md)
- [Primary vs Secondary Errors](../02-deep-dive/02-primary-vs-secondary-errors.md)
- [Errors During Cleanup (Part XXIII)](../../../part-23-special-cases/58-less-obvious-error-handling-scenarios/README.md)
- [Recovery Failure and Recursion (Ch. 13)](../../13-catch-blocks-and-recovery-logic/02-deep-dive/02-recovery-failure-and-recursion.md)
