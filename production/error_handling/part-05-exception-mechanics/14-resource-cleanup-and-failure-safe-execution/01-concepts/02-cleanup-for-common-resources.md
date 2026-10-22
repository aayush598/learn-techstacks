# Cleanup for Common Resources

> Part V · Chapter 14 · Sections 14.5, 14.6, 14.7, 14.8, 14.9 · _Estimated reading time: 17 min_
> **Prerequisite:** [Acquire/Release and Guaranteed Cleanup](./01-acquire-release-and-guaranteed-cleanup.md)

## In one sentence

Each resource family — DB connections, transactions, file handles, streams, and network
connections — has a **specific release discipline**, and getting it wrong leaks pools, leaves
locks, or corrupts data.

## Why this matters in production

The generic rule ("release in `finally`") is necessary but not sufficient. Transactions need
**rollback**, not just close, on failure. Streams need `flush`/`close` in the right order. Network
sockets need graceful shutdown or they linger in `TIME_WAIT`. Each mistake produces a distinct
production failure that is hard to connect back to the code.

## Core concept

| Resource | Acquire | Release (success) | Release (failure) | Leak symptom |
| -------- | ------- | ----------------- | ----------------- | ------------ |
| **DB connection** | pool checkout | return to pool | return to pool | pool exhaustion, `500`s |
| **Transaction** | `BEGIN` | `COMMIT` | `ROLLBACK` | long-held locks, bloat |
| **File handle** | `open` | `close` | `close` | `EMFILE` |
| **Stream** | open writer | `flush` + `close` | `flush`(best-effort) + `close` | truncated output |
| **Network conn** | connect | graceful close | abort/close | `TIME_WAIT`, pool leak |

### DB connections (14.5)

A connection is **borrowed** from a pool. Close/return it as soon as the unit of work ends. Holding
it across an `await` of an unrelated slow call is a common leak that causes pool starvation.

### Transactions (14.6)

A transaction is a connection *plus* state. On failure you must **rollback** before releasing;
closing without rollback may leave an open transaction on the connection, poisoning the next user.

```text
BEGIN ──▶ work ──▶ success ──▶ COMMIT ──▶ release
             └── error ──▶ ROLLBACK ──▶ release
```

### File handles (14.7)

Open late, close eagerly. Prefer `with`/`using`/`try-with-resources`. Never open in a loop without
closing, or you exhaust fds.

### Streams (14.8)

Streams have two distinct actions: **flush** (push buffered data) and **close** (release the
handle). A file copied to disk without flushing can be empty/truncated. On failure, flush what you
can, then close.

### Network connections (14.9)

Close gracefully to allow the peer to clean up; a hard abort can leave the remote half-open. Return
sockets to the pool (HTTP keep-alive) rather than closing per request where reuse is desired.

## How it works (mechanics)

### Connection checkout/return

```text
pool (N connections)
  checkout() ──▶ borrowed  ──▶ use ──▶ release/close ──▶ back to pool
                                     └── throw ──▶ (finally) release/close
```

If release is skipped, the borrowed slot is lost forever; after N leaks the pool blocks or times
out on `checkout()`.

### Transaction rollback-on-failure

```python
with db.transaction() as tx:     # __exit__ rolls back if the block raised
    tx.execute(UPDATE_ORDER)
    charge()                     # throws → rollback → connection returned
```

Manual equivalent must rollback *and* release in `finally`, and rollback itself may fail — attach
that as suppressed (14.13).

### Stream flush-before-close

```java
try (var out = new BufferedWriter(new FileWriter(path))) {
    out.write(data);
    // implicit flush + close on block exit; close flushes
}
```

On the failure path, a partially written temp file should be **deleted**, not left behind (14.11).

## Worked example

A transfer operation using a connection, a transaction, and a temp file:

```go
func (s *Service) Transfer(ctx context.Context, req Transfer) error {
    conn, err := s.pool.Acquire(ctx)
    if err != nil {
        return fmt.Errorf("acquire conn: %w", err)
    }
    defer conn.Release()               // (A) always return the connection

    tx, err := conn.Begin(ctx)
    if err != nil {
        return fmt.Errorf("begin tx: %w", err)
    }
    defer tx.Rollback(ctx)             // (B) no-op after a successful Commit

    audit, err := os.CreateTemp("", "transfer-*.json")
    if err != nil {
        return fmt.Errorf("temp file: %w", err)
    }
    defer os.Remove(audit.Name())      // (C) always delete temp file
    defer audit.Close()                // (D) always close handle

    if err := s.debit(ctx, tx, req); err != nil {
        return err                     // rollback + cleanup run via defer
    }
    if _, err := audit.Write(req.auditJSON()); err != nil {
        return fmt.Errorf("write audit: %w", err)
    }
    if err := s.credit(ctx, tx, req); err != nil {
        return err
    }
    return tx.Commit(ctx)              // (B) Rollback after Commit is a documented no-op
}
```

Note the ordering (LIFO): D closes the file, C removes it, B rolls back (no-op after commit), A
returns the connection — all on every path.

## Key data / numbers

- **Postgres `idle_in_transaction_session_timeout`**: default off, but many deployments set
  `5s`–`60s`; a stuck-open transaction is killed and looks like a random disconnect.
- **Connection pool sizing**: commonly `2 × CPU + effective_spindles`; pool exhaustion under load
  needs a checkout timeout (e.g. `5s`) to fail fast.
- **`ulimit -n`**: typical 1024; `EMFILE` when exceeded.
- **HTTP keep-alive**: reuse pooled sockets; the server may send `Connection: close` — respect it.
- **fsync/flush**: data written to a stream is not durable until flushed to the OS and (for
  durability) fsync'd.

## Real-world use case — Acme SaaS

Acme's `ExportJob` opened a DB transaction, wrote to S3, then committed — with no rollback on the
S3 path. When S3 errored, the transaction stayed open, holding row locks. Later jobs deadlocked
waiting on those locks, and a restart cleared them only to recur. Adding `defer tx.Rollback()` (a
no-op after commit) and releasing the connection in the same scope eliminated the stuck
transactions. Lock waits normalized.

## Trade-offs

| Resource | Aggressive close | Hold for reuse |
| -------- | ---------------- | -------------- |
| DB connection | Safe, more checkouts | Pool reuse; risk of holding during slow work |
| Transaction | Short, low contention | Long, risk of lock/`idle_in_transaction` |
| File handle | Safe | N/A — always close |
| Socket | Safe, but no keep-alive reuse | Reuse with idle timeout |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return connections to the pool in `finally` | Hold a connection across unrelated awaits |
| Rollback on failure, commit on success | Close a transaction without rollback |
| Close files even on the error path | Open in a loop without closing |
| Flush then close streams | Close without flushing |
| Gracefully close sockets; respect `Connection: close` | Abort sockets mid-response |

## Common mistakes

- **Skipping rollback** on the error path — leaves an open transaction.
- **Holding a connection** while awaiting an unrelated slow dependency.
- **Not deleting partial temp files** — disk fills up over time.
- **Closing a stream without flushing** — silently truncated output.
- **Closing a pooled socket** instead of returning it, defeating keep-alive.

## Checklist

- [ ] Connections returned in `finally`/`defer`.
- [ ] Transactions rollback on failure and commit only on success.
- [ ] Files and temp files closed and removed on every path.
- [ ] Streams flushed before close.
- [ ] Sockets gracefully closed/returned; `Connection: close` respected.

## Related

- [Locks, Semaphores, and Temporary Resources](./03-locks-semaphores-and-temporary-resources.md)
- [Multiple Errors and Primary Preservation](./04-multiple-errors-and-primary-preservation.md)
- [Database Error Classification (Part IX)](../../../part-09-database-and-transactions/22-database-error-classification/README.md)
- [File and Media Processing Errors (Part XVI)](../../../part-16-specialized-saas-scenarios/43-file-and-media-processing-errors/README.md)
