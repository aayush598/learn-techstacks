# Retrying 40001 and 40P01 in Code

> Part IX · Chapter 23 · Sections 23.7–23.9, 23.13 · _Estimated reading time: 24 min_
> **Prerequisite:** [Retry Eligibility and Locking Strategies](../01-concepts/03-retry-eligibility-and-locking-strategies.md)

## In one sentence

A correct retry wrapper **re-runs the whole transaction function** on `40001`/`40P01`/`1213`,
**re-reads all state** inside it, **caps attempts**, **jitters** delays, and **returns a meaningful
exhausted error** — and it is only safe when the work is idempotent.

## Why this matters in production

Most retry wrappers are subtly wrong: they retry the statement (fails with `25P02`), they reuse
captured values (conflict repeats forever), they retry `23505` (duplicates), or they sleep a
fixed second and stampede. The failure mode is not a crash — it is a **higher error rate under
load**, exactly when you can least afford it. This file gives you one wrapper per language that
you can copy, test, and review once.

## The contract

```text
retryTransaction(fn, { maxAttempts, baseMs, maxMs, isRetryable, onRetry })
  fn: (tx) => Promise<T>          // MUST do BEGIN..COMMIT internally
  isRetryable: 40001 | 40P01 | 1213 | class 08 | 53300
  preconditions: fn is idempotent, or guarded by a key
  postconditions: on exhaustion, throw a DomainError with retry metadata
```

| Error | Retry? | Scope |
| ----- | ------ | ----- |
| `40001` serialization | yes | whole transaction |
| `40P01` deadlock | yes | whole transaction |
| MySQL `1213` deadlock | yes | whole transaction |
| `55P03` lock timeout | yes | whole transaction |
| `08006` connection failure | yes | whole transaction (new conn) |
| `53300` capacity | yes + shed | whole transaction |
| `23505` unique | **no** | — |
| `57014` query timeout | selective | reduce work, not blind retry |

## TypeScript (node-pg)

```ts
import type { Pool, PoolClient } from "pg";
import { normalize } from "../db/normalize";

const RETRYABLE = new Set(["40001", "40P01", "55P03", "08006", "08003", "53300"]);

export async function withTransaction<T>(
  pool: Pool,
  fn: (tx: PoolClient) => Promise<T>,
  opts: { maxAttempts?: number; baseMs?: number; maxMs?: number; label: string },
): Promise<T> {
  const maxAttempts = opts.maxAttempts ?? 3;
  const baseMs = opts.baseMs ?? 25;
  const maxMs = opts.maxMs ?? 400;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const client = await pool.connect();
    try {
      await client.query("BEGIN");
      await client.query("SET LOCAL lock_timeout = '2s'");
      const result = await fn(client);          // fn re-reads state every attempt
      await client.query("COMMIT");
      return result;
    } catch (err) {
      await safeRollback(client);
      const db = normalize(err);
      const retryable = RETRYABLE.has(db.code ?? "");
      if (!retryable || attempt === maxAttempts) {
        throw toDomainError(db, { label: opts.label, attempts: attempt });
      }
      await sleep(backoff(attempt, baseMs, maxMs));
    } finally {
      client.release();                          // use release(true) if the socket died
    }
  }
  throw new Error("unreachable");
}

function backoff(attempt: number, baseMs: number, maxMs: number): number {
  const exp = Math.min(maxMs, baseMs * 2 ** (attempt - 1));
  return Math.floor(Math.random() * exp);        // full jitter
}

async function safeRollback(client: PoolClient) {
  try { await client.query("ROLLBACK"); } catch { /* connection already gone */ }
}
```

> ⚠️ **Hazard.** If `COMMIT` itself fails with a connection error, the outcome is **unknown** —
> do not enter the retry loop. Route `08006`/`08007` raised during `COMMIT` to the read-back
> resolver from [Ambiguous Commit Outcomes](../02-deep-dive/01-ambiguous-commit-outcomes.md).

## Go (database/sql)

```go
type TxFunc func(ctx context.Context, tx *sql.Tx) error

func WithTx(ctx context.Context, db *sql.DB, fn TxFunc, maxAttempts int) error {
    if maxAttempts == 0 { maxAttempts = 3 }
    for attempt := 1; attempt <= maxAttempts; attempt++ {
        err := runOnce(ctx, db, fn)
        if err == nil { return nil }
        if !isRetryable(err) || attempt == maxAttempts {
            return toDomain(err, attempt)
        }
        select {
        case <-time.After(backoff(attempt)):
        case <-ctx.Done():
            return ctx.Err()
        }
    }
    return nil
}

func runOnce(ctx context.Context, db *sql.DB, fn TxFunc) error {
    tx, err := db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
    if err != nil { return err }
    if _, err := tx.ExecContext(ctx, "SET LOCAL lock_timeout = '2s'"); err != nil {
        _ = tx.Rollback(); return err
    }
    if err := fn(ctx, tx); err != nil {
        _ = tx.Rollback()          // rollback errors: discard conn via db, already released
        return err
    }
    return tx.Commit()
}

func isRetryable(err error) bool {
    var pgErr *pgconn.PgError
    if errors.As(err, &pgErr) {
        switch pgErr.Code {
        case "40001", "40P01", "55P03", "08006", "08003", "53300":
            return true
        }
    }
    var myErr *mysqldriver.MySQLError
    if errors.As(err, &myErr) {
        return myErr.Number == 1213 || myErr.Number == 1205   // deadlock / lock wait
    }
    return false
}
```

`fn` must not capture mutable state from outside; read everything from the `tx`.

## Python (psycopg2)

```python
import random, time
from contextlib import contextmanager

RETRYABLE = {"40001", "40P01", "55P03", "08006", "08003", "53300"}

def with_transaction(pool, fn, *, max_attempts=3, base=0.025, cap=0.4):
    last = None
    for attempt in range(1, max_attempts + 1):
        conn = pool.getconn()
        try:
            with conn:                 # commits on success, rolls back on exception
                conn.set_session(isolation_level="SERIALIZABLE")
                with conn.cursor() as cur:
                    cur.execute("SET LOCAL lock_timeout = '2s'")
                    return fn(conn)    # fn re-reads inside this transaction
        except Exception as exc:
            last = exc
            state = getattr(exc, "pgcode", None)
            if state not in RETRYABLE or attempt == max_attempts:
                raise translate(exc, attempts=attempt)
            time.sleep(random.uniform(0, min(cap, base * 2 ** (attempt - 1))))
        finally:
            pool.putconn(conn, close=(state_is_broken(locals().get("exc"))))
    raise last
```

`with conn:` handles `COMMIT`/`ROLLBACK`. If the connection is broken, pass `close=True` so the
pool discards it.

## Forcing the failure in tests

```sql
-- Two concurrent SERIALIZABLE transactions reproduce 40001 reliably.
-- Session A:
BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT * FROM accounts WHERE id = 1;          -- read
-- Session B:
BEGIN ISOLATION LEVEL SERIALIZABLE;
UPDATE accounts SET balance = balance - 10 WHERE id = 1;
COMMIT;
-- Session A:
UPDATE accounts SET balance = balance + 10 WHERE id = 1;  -- 40001
COMMIT;
```

```python
def test_retry_once_then_succeed(pool, monkeypatch):
    calls = {"n": 0}
    def flaky(conn):
        calls["n"] += 1
        if calls["n"] == 1:
            raise pg_error("40001")
        return "ok"
    assert with_transaction(pool, flaky) == "ok"
    assert calls["n"] == 2
```

## Key data / numbers

- Retryable: `40001`, `40P01`, `55P03`, class `08`, `53300`; MySQL `1213`, `1205`.
- Attempts: **3** (sometimes 5 for batch jobs); base **25–50 ms**, cap **400–500 ms**, **full
  jitter**.
- `SET LOCAL lock_timeout = '2s'` converts an unbounded wait into a retryable `55P03`.
- Exhausted errors must include `attempts` and the last SQLSTATE for observability.
- A retry that reuses a stale `version`/`balance` will fail all attempts — re-read inside `fn`.

## Real-world use case — Acme SaaS

Acme's `Checkout` retried `UPDATE inventory` when it saw `40001`. Because the `UPDATE` reused the
`available` value read before the conflict, every retry computed the same wrong reservation and
conflicted again. After switching to `withTransaction`, the whole unit re-read inventory and
re-applied the guard; conflict retries succeeded on the second attempt in 98% of cases, and the
checkout error rate under load fell from 3.1% to 0.04%. The wrapper also classified `23505` as
non-retryable, which ended duplicate orders.

## Trade-offs

| Setting | Pros | Cons | When to use |
| ------- | ---- | ---- | ----------- |
| 3 attempts | fast failure, low amplification | may exhaust under heavy contention | request paths |
| 5–8 attempts | higher success under spikes | longer latency, more work | batch jobs |
| Fixed delay | simple | thundering herd | never |
| Full jitter | spreads retries | slightly higher mean latency | default |
| `SERIALIZABLE` + retry | strongest invariants | more `40001` | money, inventory |
| `READ COMMITTED` + locks | fewer aborts | deadlocks possible | simple read-modify-write |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Re-enter `BEGIN` on every attempt | Retry the failed statement |
| Re-read state inside the transaction | Capture values outside and reuse |
| Cap attempts and use jitter | Sleep 1 s in a tight loop |
| Route commit-time connection loss to resolution | Retry it as a normal transient |
| Return `attempts` + last SQLSTATE | Throw the raw driver error |
| Test with two real sessions | Mock `40001` only |

## Common mistakes

- **Retrying `23505`** because "it might be a race" — it is permanent.
- **Catching `40001` outside the transaction but reusing a prepared statement** with stale params.
- **Returning an inner error after exhaustion** — loses retry metadata.
- **Not setting `lock_timeout`** — attempts block for 50 s each.
- **Retrying in both the repository and the service** — amplification (n×m attempts).

## Checklist

- [ ] Exactly one layer owns transaction retries.
- [ ] Retryable set is explicit and excludes class `23`.
- [ ] `fn` re-reads state on every attempt.
- [ ] Attempts, delay, and jitter are configured and logged.
- [ ] Commit-time ambiguity bypasses the retry loop.
- [ ] Tests reproduce `40001` with two real sessions.

## Related

- [Retry Eligibility and Locking Strategies (23.7–23.10)](../01-concepts/03-retry-eligibility-and-locking-strategies.md)
- [Ambiguous Commit Outcomes](../02-deep-dive/01-ambiguous-commit-outcomes.md)
- [Conflicts, Locks, and Timeouts (22.9–22.13)](../../22-database-error-classification/01-concepts/03-conflicts-locks-and-timeouts.md)
- [Retry Policies (Ch. 27)](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
