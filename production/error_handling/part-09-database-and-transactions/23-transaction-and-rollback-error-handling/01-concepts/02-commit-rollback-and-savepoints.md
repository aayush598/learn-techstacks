# Commit, Rollback, and Savepoints (23.3–23.6)

> Part IX · Chapter 23 · Sections 23.3–23.6 · _Estimated reading time: 20 min_
> **Prerequisite:** [Transaction Boundaries and Atomicity](./01-transaction-boundaries-and-atomicity.md)

## In one sentence

`COMMIT` and `ROLLBACK` are **operations that can themselves fail**, savepoints let you recover
*inside* a transaction without losing the whole unit of work, and **partial completion** is what
you get when a multi-statement or multi-item operation is only partly rolled back.

## Why this matters in production

Teams assume `ROLLBACK` always works and wrap it in `finally` without observing it. But rollback
can fail on a dead connection, leaving you unsure whether locks or changes remain. Teams also
treat a failed `COMMIT` as "nothing happened" — when the commit record may already be durable.
And savepoint misuse produces `25P02` cascades and leaked partial writes. Each failure has a
different safe response, and they are not interchangeable.

## Core concept

| § | Operation | Can fail how? | Safe response |
| - | --------- | ------------- | ------------- |
| 23.3 | **Commit** | connection lost, constraint deferred, disk full, replica promotion | **unknown outcome** → read back (§23.12); never blind-retry |
| 23.4 | **Rollback** | connection already dead, server shutting down | log, discard connection, **do not reuse**; state is server-resolved |
| 23.5 | **Savepoints** | invalid savepoint name, txn already aborted | roll back to savepoint; if that fails, roll back the whole txn |
| 23.6 | **Partial completion** | per-item success/failure in a batch, or `COMMIT` of a partially applied saga | record per-item results explicitly; compensate or resume |

```text
BEGIN ──▶ statement ──▶ SAVEPOINT sp1 ──▶ statement ✗ ──▶ ROLLBACK TO sp1 ──▶ continue
   │                                                                           │
   └──────────────────────────── COMMIT ──────────────────────────────────────┘
                                   │
                          ack lost? → UNKNOWN (not "failed")
```

### 23.3 Commit failures

A `COMMIT` that returns an error is **not automatically a rollback**:

- **Constraint checked at commit** (deferred constraints): the commit is rejected and the
  transaction aborts — a definite *failure*.
- **Connection dies during `COMMIT`**: the server may have committed before the socket broke.
  The outcome is **unknown** — the caller must resolve it, not guess.
- **Disk full / I/O error**: commit may fail after partially writing; treat as unknown and page.

### 23.4 Rollback failures

`ROLLBACK` on a healthy connection essentially cannot fail for business reasons. When it *does*
fail, the connection is broken or the server is gone. The important consequence is not the
rollback itself (the server resolves an abandoned transaction) but that **the connection must be
discarded**, never returned to the pool.

```python
try:
    conn.commit()
except Exception as exc:
    try:
        conn.rollback()          # best effort
    except Exception as rb_exc:
        log.error("rollback failed; discarding connection", exc_info=rb_exc)
    finally:
        conn.close()             # NEVER put a broken connection back in the pool
    raise translate(exc)
```

### 23.5 Nested transactions and savepoints

Most databases do **not** support true nested transactions. `SAVEPOINT` gives you a named point
you can partially roll back to **within** one transaction:

```sql
BEGIN;
  INSERT INTO imports (id, status) VALUES (1, 'running');

  SAVEPOINT item_1;
  INSERT INTO import_rows (import_id, line, data) VALUES (1, 1, $1);
  -- fails with 23505 or 23514:
  ROLLBACK TO SAVEPOINT item_1;     -- only this row is undone, txn stays usable
  -- record the row failure separately

  SAVEPOINT item_2;
  INSERT INTO import_rows (import_id, line, data) VALUES (1, 2, $2);
  RELEASE SAVEPOINT item_2;

COMMIT;
```

⚠️ **Hazard.** After any error in Postgres, the transaction is in a failed state (`25P02`) until
you `ROLLBACK TO SAVEPOINT` or `ROLLBACK`. If you use savepoints, you **must** roll back to the
savepoint immediately after each caught error.

### 23.6 Partial completion

Partial completion appears at three levels:

1. **Batch items** — row 7 of 100 fails; rows 1–6 are already in the transaction. Either roll
   back all, or savepoint per item and record failures.
2. **Sagas** — step 3 of 5 succeeds, step 4 fails; you compensate steps 1–3.
3. **Commit acknowledgment** — the write completed but the caller saw an error.

In all three, the dangerous outcome is **claiming total success** or **claiming total failure**
when the truth is "some". Model it explicitly:

```ts
type BulkResult<T> =
  | { kind: "all_succeeded"; items: T[] }
  | { kind: "partial"; succeeded: T[]; failed: Array<{ item: T; error: DomainError }> }
  | { kind: "all_failed"; error: DomainError };
```

## Worked example

```ts
// Savepoint-per-item import, with explicit partial results.
async function importRows(tx: Tx, rows: Row[]): Promise<BulkResult<Row>> {
  const succeeded: Row[] = [];
  const failed: Array<{ item: Row; error: DomainError }> = [];

  for (const [i, row] of rows.entries()) {
    const sp = `item_${i}`;
    await tx.query(`SAVEPOINT ${sp}`);
    try {
      await tx.query(`INSERT INTO import_rows (import_id, line, data) VALUES ($1,$2,$3)`,
                     [row.importId, row.line, row.data]);
      await tx.query(`RELEASE SAVEPOINT ${sp}`);
      succeeded.push(row);
    } catch (err) {
      await tx.query(`ROLLBACK TO SAVEPOINT ${sp}`);   // txn stays usable
      failed.push({ item: row, error: classify(normalize(err), { resource: "import:row" }) });
    }
  }

  if (failed.length === 0) return { kind: "all_succeeded", items: succeeded };
  if (succeeded.length === 0) return { kind: "all_failed", error: failed[0].error };
  return { kind: "partial", succeeded, failed };
}
```

```text
ExportJob result: 998 rows inserted, 2 rejected (23502 line 41, 23514 line 87)
  → import status = 'completed_with_errors'
  → per-row reasons stored, retry only the 2
```

## Key data / numbers

- Postgres marks the transaction failed after **any** statement error; only
  `ROLLBACK TO SAVEPOINT` or `ROLLBACK` clears `25P02`.
- `SAVEPOINT`/`RELEASE` are cheap but not free: **thousands** per transaction increase memory and
  WAL; batch in groups of **100–1,000** rather than one per million rows.
- MySQL supports `SAVEPOINT` in InnoDB; DDL still auto-commits and **destroys** the transaction.
- A broken connection must be **closed, not returned to the pool** — otherwise every later
  request inherits the failure.
- `COMMIT` failure with a lost acknowledgment is **not** a rollback; resolve via read-back.

## Real-world use case — Acme SaaS

Acme's CSV importer wrapped 50,000 rows in one transaction. A single bad row (a `23502` on
`line`) aborted everything, and the UI reported "import failed" while the `imports` status row
had already been inserted by a *previous* committed transaction — so users saw a phantom
"running" import. The fix: savepoint per row (batched in groups of 500), an explicit
`completed_with_errors` status, and per-row error records. Imports now succeed partially,
users can fix only the rejected rows, and `25P02` disappeared from the logs.

## Trade-offs

| Strategy | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| All-or-nothing transaction | simplest correctness | one bad row kills the batch | small batches, strict atomicity |
| Savepoint per item | partial success, txn survives | memory/WAL overhead | imports, bulk operations |
| One transaction per item | isolation, simple retry | slow, no cross-item atomicity | very large imports |
| Compensate after partial commit | works across services | complex, needs idempotency | sagas |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Treat `COMMIT` errors as "unknown" until resolved | Assume a failed commit rolled back |
| `ROLLBACK TO SAVEPOINT` immediately after a caught error | Keep querying in `25P02` |
| Close broken connections | Return them to the pool |
| Return explicit partial results | Report "success" for partial failure |
| Batch savepoints | Create one savepoint per million rows |

## Common mistakes

- **Ignoring rollback failure** and reusing the connection.
- **Blind retry after a commit error** — the write may already be durable.
- **Catching inside a transaction without a savepoint** — every later statement fails.
- **Marking a batch "failed" when 998/1000 rows succeeded** — data and UX both wrong.
- **Using DDL inside a long MySQL transaction** — DDL commits implicitly.

## Checklist

- [ ] Commit failures are classified as `failed` vs `unknown`.
- [ ] Rollback failure closes the connection.
- [ ] Savepoints are used for per-item recovery and rolled back on each error.
- [ ] Bulk operations return `all_succeeded` / `partial` / `all_failed`.
- [ ] Partial results are persisted, not just logged.

## Related

- [Ambiguous Commit Outcomes](../02-deep-dive/01-ambiguous-commit-outcomes.md)
- [Retry Eligibility and Locking Strategies (23.7–23.10)](./03-retry-eligibility-and-locking-strategies.md)
- [Bulk Operations and Partial Success (24.9–24.10)](../../24-repository-and-data-access-error-handling/01-concepts/04-bulk-operations-and-partial-success.md)
- [Resource Cleanup: Transactions (14.6)](../../../part-05-exception-mechanics/14-resource-cleanup-and-failure-safe-execution/01-concepts/02-cleanup-for-common-resources.md)
