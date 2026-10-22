# Conflicts, Locks, and Timeouts (22.9–22.13)

> Part IX · Chapter 22 · Sections 22.9–22.13 · _Estimated reading time: 22 min_
> **Prerequisite:** [Query Execution and Constraint Violations](./02-query-execution-and-constraint-violations.md)

## In one sentence

Deadlocks, lock timeouts, query timeouts, and serialization failures all mean **another
transaction got in the way** — and unlike constraint errors they are **transient by
definition**: retry the *whole transaction* with fresh reads.

## Why this matters in production

The concurrency class is where correct retries save a product and incorrect ones corrupt it.
A `40001 serialization_failure` retried with the *same stale* values fails forever; a `40P01`
deadlock retried **only the failing statement** retries inside an already-aborted transaction;
a `57014` query timeout caused by a missing index gets retried until the queue melts. Worse, a
`1205` lock-wait timeout in MySQL leaves the transaction *open* by default, so naive code
commits a half-applied unit of work. These are all **classifiable**, and each has one correct
recovery.

## Core concept

| § | Condition | Postgres | MySQL (InnoDB) | Transaction state after |
| - | --------- | -------- | -------------- | ----------------------- |
| 22.9 | **Deadlock** | `40P01` `deadlock_detected` | `1213` `ER_LOCK_DEADLOCK` | **aborted** — must `ROLLBACK` and retry all |
| 22.10 | **Lock timeout** | `55P03` `lock_not_available` (`lock_timeout`) | `1205` `ER_LOCK_WAIT_TIMEOUT` | PG: transaction aborted; MySQL: **statement only** rolled back, txn open |
| 22.11 | **Query timeout** | `57014` `query_canceled` (`statement_timeout`) | `3024` `ER_QUERY_TIMEOUT` (`max_execution_time`) | statement cancelled; txn may still be open |
| 22.12 | **Transaction conflict** | write-write / update conflict | lock wait / deadlock | varies — inspect |
| 22.13 | **Serialization failure** | `40001` `serialization_failure` (SERIALIZABLE, or REPEATABLE READ update conflict) | `1213` under `SERIALIZABLE` | **aborted** — retry all |

The mental model:

```text
  T1 ──locks row A──▶ wants B            "deadlock"     40P01 / 1213
  T2 ──locks row B──▶ wants A            → abort one, retry it

  T1 ──holds row A for 30s──▶ T2 waits   "lock timeout" 55P03 / 1205
                                         → abort waiter, retry/alert

  T1 ──runs 35s query──────▶ cancelled   "query timeout" 57014 / 3024
                                         → cancel, maybe reduce work

  T1,T2 ──serializable snapshot overlap──▶ "serialization" 40001
                                         → abort one, re-read, retry
```

**All four are transient *for the transaction*, not for the user.** The client sees a `409` or
`503` only after the retry budget is exhausted; a successful retry is invisible.

> ⚠️ **Hazard.** Retrying **the statement** after `40001`/`40P01` is a bug: the transaction
> snapshot is already poisoned. Retry the **entire unit of work**, from `BEGIN`, with freshly
> read state.

## How it works (mechanics)

### Deadlock (22.9)

Postgres detects a cycle in the wait-for graph and aborts **one** victim with `40P01`; the
victim's transaction is dead. InnoDB does the same with `1213`, rolling back the *whole*
transaction. This is a **safety mechanism**, not corruption — but only if you retry.

### Lock timeout (22.10)

- Postgres: set `lock_timeout = '2s'` per transaction; exceeding it raises `55P03` and aborts
  the transaction. Without it, a blocked `UPDATE` waits indefinitely (bounded by
  `statement_timeout`, if set).
- MySQL: `innodb_lock_wait_timeout` (default **50 s**) raises `1205`. With the default
  `innodb_rollback_on_timeout=OFF`, **only the statement** is rolled back — the transaction
  remains usable and can be committed. Decide explicitly whether to retry the statement or
  roll back everything.

### Query timeout (22.11)

`statement_timeout` cancels the statement server-side and returns `57014`. On the client this
must be **distinguishable from a client-side deadline** (`ETIMEDOUT`, context cancelled): the
server may have completed the work before the cancel landed. For writes this intersects the
ambiguous-outcome problem (Chapter 23).

### Serialization failure (22.13)

Under `SERIALIZABLE`, Postgres uses SSI and aborts one transaction with `40001` when the
interleaving is not serializable. Under `REPEATABLE READ`, a concurrent update to a row you
then modify also yields `40001`. MySQL's `SERIALIZABLE` turns plain reads into shared locks and
typically produces `1213` deadlocks instead. Either way: **re-read, re-apply, retry**.

## Worked example

```ts
// Correct shape: retry the WHOLE transaction, never the inner query.
async function withSerializableRetry<T>(
  run: (tx: Tx) => Promise<T>,
  maxAttempts = 3,
): Promise<T> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await db.transaction({ isolation: "serializable" }, run);
    } catch (err) {
      if (!isRetryableConflict(err)) throw err;      // 40001, 40P01, 1213
      if (attempt === maxAttempts) throw mapExhausted(err);
      await sleep(jitteredBackoff(attempt));          // 20–80ms, then 40–160ms
      // loop re-enters db.transaction → BEGIN again, run() re-reads
    }
  }
  throw new Error("unreachable");
}
```

```sql
-- Postgres: a deadlock-prone transfer, fixed by deterministic ordering
BEGIN;
SET LOCAL lock_timeout = '2s';       -- 55P03 instead of infinite wait
UPDATE accounts SET balance = balance - 10 WHERE id = 1;  -- always lock lower id first
UPDATE accounts SET balance = balance + 10 WHERE id = 2;
COMMIT;                              -- 40P01 on deadlock → retry THIS whole block
```

## Key data / numbers

- Postgres deadlock detection is controlled by `deadlock_timeout` (default **1 s**): a waiter
  checks for a cycle after waiting that long.
- `lock_timeout` — **unset by default** (wait forever); set per transaction, e.g. `2s`.
- `statement_timeout` — **unset by default**; `57014` on expiry.
- MySQL `innodb_lock_wait_timeout` default **50 s**; `max_execution_time` default **0**
  (unlimited, and applies to `SELECT` only in MySQL 8).
- Postgres `40001`/`40P01` retry: **typically 2–4 attempts** with jittered backoff; more
  attempts hide contention you should fix (indexes, lock order).
- Isolation: `SERIALIZABLE` → more `40001` but fewer anomalies; `READ COMMITTED` (Postgres
  default) → fewer aborts, requires explicit locking for read-modify-write.

## Real-world use case — Acme SaaS

Acme's `Checkout` decremented inventory and inserted an order in one transaction. Under load,
two tickets for the same SKU deadlocked (`40P01`) because one flow locked `orders` then
`inventory`, the other the reverse. The service retried the *failed statement*, which failed
instantly with `25P02`, then surfaced `500`s. The fix: **one lock order** (`inventory` first),
`lock_timeout=2s`, and a wrapper that retries the **whole transaction** on `40001`/`40P01` up to
three times. Deadlocks fell by ~90%; the remaining ones became invisible retries, and checkout
conversion recovered.

## Trade-offs

| Strategy | Pros | Cons | When to use |
|----------|------|------|-------------|
| Retry whole transaction | correct for `40001`/`40P01` | work re-executed; side effects must be idempotent | default |
| Pessimistic `SELECT ... FOR UPDATE` | simple mutual exclusion | contention, deadlocks, lock timeouts | short critical sections |
| Optimistic version check | no locks; scales reads | `409`/`412` to clients, retry logic | low-contention updates |
| Higher isolation (`SERIALIZABLE`) | strongest guarantee | more `40001`, retries | money, inventory, uniqueness across rows |
| Increase timeouts | fewer aborts | latency cliffs, stuck workers | never as the first fix |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Retry the **whole transaction** on `40001`/`40P01`/`1213` | Retry one statement inside a dead transaction |
| Re-read state before re-applying | Reuse the stale `balance`/`version` captured before the abort |
| Impose a deterministic lock order | Lock rows in whatever order the request arrived |
| Set `lock_timeout` and `statement_timeout` | Wait forever on a lock |
| Treat `1205` as "statement rolled back, txn open" in MySQL | Assume the whole txn aborted |
| Log the attempt count with the final failure | Silently swallow retries |

## Common mistakes

- **Retrying with stale state** — `40001` recurs on every attempt.
- **Not rolling back after `40P01`** — all subsequent statements fail with `25P02`.
- **Confusing client deadline with `57014`** — a client timeout does not prove the server
  cancelled the write (see [ambiguous outcomes](../../23-transaction-and-rollback-error-handling/02-deep-dive/01-ambiguous-commit-outcomes.md)).
- **Raising `50s` lock timeouts to "fix" contention** — you converted a fast failure into a slow
  one.
- **Using `SERIALIZABLE` everywhere** — correct but expensive; scope it to invariants that need it.

## Checklist

- [ ] `40001`, `40P01`, `1213`, `55P03`, `57014`, `1205`, `3024` each have an explicit policy.
- [ ] Retry wraps the transaction, not the query, and re-reads state.
- [ ] `lock_timeout` and `statement_timeout` are set on request paths.
- [ ] Deadlock retries are capped and counted; a rising rate is an alert, not a fix.
- [ ] Isolation level is chosen per operation and documented.

## Related

- [Failover, Replicas, and Unavailability (22.14–22.16)](./04-failover-replicas-and-unavailability.md)
- [Retry Eligibility and Locking Strategies (23.7–23.10)](../../23-transaction-and-rollback-error-handling/01-concepts/03-retry-eligibility-and-locking-strategies.md)
- [Retrying 40001 and 40P01 in Code](../../23-transaction-and-rollback-error-handling/03-practical-examples/01-retrying-40001-and-40p01.md)
- [SQLSTATE Classification Table](../02-deep-dive/01-sqlstate-classification-table.md)
