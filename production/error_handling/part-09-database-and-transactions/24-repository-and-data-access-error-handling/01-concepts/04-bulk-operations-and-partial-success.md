# Bulk Operations and Partial Success (24.9, 24.10)

> Part IX · Chapter 24 · Sections 24.9, 24.10 · _Estimated reading time: 20 min_
> **Prerequisite:** [CRUD Failure Semantics](./03-crud-failure-semantics.md)

## In one sentence

Bulk operations fail **per item, per statement, or per transaction**, and a single boolean result
is always a lie — return a **per-item outcome** that distinguishes success, rejection, and "not
attempted".

## Why this matters in production

A bulk endpoint that returns `500` when row 7 of 1,000 is invalid forces users to resubmit
everything and hope; one that returns `200` when 993 rows were inserted tells them their import
worked. The database makes this worse: in Postgres, **one failing row aborts the entire
statement**, so "bulk insert" is all-or-nothing unless you deliberately add savepoints or split
the batch. `ExportJob` and CSV imports live or die on getting this right.

## Core concept

| Granularity | Failure behavior | Result shape |
| ----------- | ---------------- | ------------ |
| **Per statement** (`INSERT ... VALUES (...), (...)`) | one bad row aborts all | `all_succeeded` or `all_failed` |
| **Per item** (savepoint / separate txn) | others continue | `partial` with per-item errors |
| **Per chunk** (batches of N) | chunk atomic, earlier chunks durable | partial across chunks |
| **Per transaction** | everything or nothing | `all_succeeded` or `all_failed` |

```text
bulk insert 1,000 rows
  ├─ single statement          → 1 × 23502 aborts all 1,000
  ├─ statement per row         → 993 succeed, 7 fail (slow: 1,000 round trips)
  ├─ savepoint per row         → 993 succeed, 7 fail (one txn, one round trip each)
  └─ chunk of 100 + savepoint  → partial per chunk; retry only failed chunks
```

### 24.9 Bulk failure modes

| Failure | Example | Effect |
| ------- | ------- | ------ |
| One invalid row | `23502` on line 41 | whole statement aborts (Postgres) |
| Duplicate key | `23505` on line 87 | whole statement aborts unless `ON CONFLICT` |
| Batch too large | `54000`/`54001` program limit | statement rejected; split it |
| Parameter limit | Postgres **65,535** bind params | driver/protocol error |
| Lock/timeout mid-batch | `40P01`, `55P03` | whole transaction aborts; retry the batch |
| Partial network failure | resume/checkpoint needed | some chunks applied, some not |

### 24.10 Partial bulk success

Represent it explicitly and persist it:

```ts
type BulkResult<T> =
  | { kind: "all_succeeded"; succeeded: T[] }
  | { kind: "partial"; succeeded: T[]; failed: Array<{ item: T; error: RepoError }> }
  | { kind: "all_failed"; error: RepoError };

function summarize<T>(r: BulkResult<T>) {
  switch (r.kind) {
    case "all_succeeded": return { ok: r.succeeded.length, failed: 0, status: "completed" };
    case "partial":       return { ok: r.succeeded.length, failed: r.failed.length,
                                   status: "completed_with_errors" };
    case "all_failed":    return { ok: 0, failed: 0, status: "failed" };
  }
}
```

**"Not attempted"** is a fourth outcome. If you stop at the first failed chunk, the remaining
items were never tried — do not report them as failed. Include them in a `skipped` list or
resume from a checkpoint.

## How it works (mechanics)

### Strategy 1 — single statement (all-or-nothing)

```sql
INSERT INTO import_rows (import_id, line, data)
VALUES ($1,$2,$3), ($4,$5,$6), ($7,$8,$9);
-- Any constraint error aborts the whole statement. Simple, fast, no partial success.
```

Use when the batch is small and atomicity is required. Return `all_succeeded` or `all_failed`.

### Strategy 2 — savepoint per item

```sql
BEGIN;
SAVEPOINT r1;  INSERT ...;  -- ok
RELEASE SAVEPOINT r1;
SAVEPOINT r2;  INSERT ...;  -- 23505
ROLLBACK TO SAVEPOINT r2;   -- txn still usable
-- record failure, continue
COMMIT;
```

Use for imports where partial success is acceptable. Batch savepoints in groups of 100–1,000 to
bound memory/WAL.

### Strategy 3 — upsert for duplicates

```sql
INSERT INTO import_rows (import_id, line, data)
VALUES ...
ON CONFLICT (import_id, line) DO NOTHING;   -- duplicates are not failures
```

Only for **expected** duplicates (retries, re-uploads). A duplicate that means "different data
for the same key" should be a conflict, not silently ignored.

### Strategy 4 — chunk + checkpoint

Split into chunks, record progress, retry only failed chunks. `ExportJob` uses this so a crash
does not restart the whole export.

## Worked example (Python, per-item savepoints)

```python
def bulk_insert(tx, rows, *, chunk=500):
    succeeded, failed = [], []
    try:
        for start in range(0, len(rows), chunk):
            tx.execute("SAVEPOINT chunk")
            try:
                for i, row in enumerate(rows[start:start + chunk]):
                    tx.execute("SAVEPOINT item")
                    try:
                        tx.execute(
                            "INSERT INTO import_rows (import_id, line, data) VALUES (%s,%s,%s)",
                            (row.import_id, row.line, row.data),
                        )
                        tx.execute("RELEASE SAVEPOINT item")
                        succeeded.append(row)
                    except DriverError as exc:
                        tx.execute("ROLLBACK TO SAVEPOINT item")
                        failed.append({"line": row.line,
                                       "error": translate(normalize(exc), op="import.row")})
                tx.execute("RELEASE SAVEPOINT chunk")
            except DriverError:
                tx.execute("ROLLBACK TO SAVEPOINT chunk")
                raise
        return BulkResult.partial(succeeded, failed) if failed else BulkResult.ok(succeeded)
    except DriverError as exc:
        return BulkResult.failed(translate(normalize(exc), op="import.batch"))
```

```text
Result: 993 succeeded, 7 failed, 0 skipped
  line 41: REQUIRED_FIELD_MISSING (23502)
  line 87: CONFLICT (23505, field=line)
  ...
Import status: completed_with_errors; retry endpoint accepts only failed lines.
```

## Key data / numbers

- Postgres protocol limit: **65,535** bind parameters per statement — at 3 params/row, ~21,000
  rows max per insert.
- Recommended chunk size: **500–5,000** rows; measure round-trip vs memory.
- Savepoint overhead grows with count; batch them rather than one per million rows.
- `ON CONFLICT` requires a unique/exclusion constraint; MySQL equivalent is `INSERT ... ON
  DUPLICATE KEY UPDATE` (and `INSERT IGNORE` swallows more than duplicates).
- A per-item strategy turns one 1,000-row failure into 993 successes + 7 actionable errors —
  the difference between a support ticket and a retry button.

## Real-world use case — Acme SaaS

Acme's `ExportJob` imported a customer CSV in one `INSERT` of 40,000 rows. A single malformed
date (`22007`) aborted everything and the API returned "import failed" with no line number.
Customers re-uploaded the same file, hitting the same row, in a loop. Switching to **chunks of
500 with per-item savepoints** produced `completed_with_errors`, a downloadable error report by
line, and a retry endpoint for the 7 rejected rows. Support tickets for imports fell by ~80%,
and `ExportJob` stopped re-processing 39,993 good rows for one bad one.

## Trade-offs

| Strategy | Speed | Partial success | Complexity | When to use |
| -------- | ----- | --------------- | ---------- | ----------- |
| Single statement | fastest | no | low | small atomic batches |
| Savepoint per item | slower | yes | medium | imports, user data |
| Statement per item | slowest | yes | low | tiny batches, external retries |
| Chunk + savepoint | fast | yes (per chunk) | medium | large imports |
| `ON CONFLICT DO NOTHING` | fast | duplicates hidden | low | idempotent replays only |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return per-item success/failure | Return one boolean for a batch |
| Distinguish "failed" from "not attempted" | Mark unprocessed rows as failed |
| Use `ON CONFLICT` only for expected duplicates | Silence all conflicts |
| Batch savepoints | One savepoint per million rows |
| Persist per-item errors with line numbers | Log them and return `500` |
| Retry only failed chunks/lines | Re-run the whole import |

## Common mistakes

- **Assuming a multi-row insert is partially applied** — in Postgres, it is not.
- **Returning `200` with `failed: 7` hidden** — clients think everything worked.
- **`INSERT IGNORE` for all errors** — also ignores truncation and other data problems.
- **No checkpoint in long batches** — a crash restarts from zero.
- **Retrying the batch with the same failed rows** — fails identically forever.

## Checklist

- [ ] Bulk method returns `all_succeeded` / `partial` / `all_failed` (+ `skipped`).
- [ ] Per-item errors carry item identity and a translated code.
- [ ] Chunk size is configured and within parameter limits.
- [ ] Duplicate handling is deliberate (`ON CONFLICT` vs conflict).
- [ ] Long imports checkpoint and can retry only failures.
- [ ] Partial results are persisted, not just returned.

## Related

- [CRUD Failure Semantics (24.4–24.8)](./03-crud-failure-semantics.md)
- [Bulk Partial Success with the Cast](../03-practical-examples/02-bulk-partial-success-with-cast.md)
- [Commit, Rollback, and Savepoints (23.3–23.6)](../../23-transaction-and-rollback-error-handling/01-concepts/02-commit-rollback-and-savepoints.md)
- [File and Media Processing Errors (Ch. 43)](../../../part-16-specialized-saas-scenarios/43-file-and-media-processing-errors/README.md)
