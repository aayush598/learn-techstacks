# Practical: Bulk Partial Success with the Cast (24.9, 24.10, 24.14)

> Part IX · Chapter 24 · Sections 24.9, 24.10, 24.14 · _Estimated reading time: 25 min_
> **Prerequisite:** [Bulk Operations and Partial Success](../01-concepts/04-bulk-operations-and-partial-success.md)

## What we're building

`ExportJob` ingests a customer CSV of up to 100,000 rows into `import_rows`. Requirements:

- one invalid row must **not** abort the import;
- the API returns **per-line outcomes** (`succeeded`, `failed`, `skipped`);
- re-uploading the same file must not duplicate rows;
- after the import, the job's status read must reflect the completed write (**read-your-writes**).

## Stage 1 — the schema and outcome types

```sql
CREATE TABLE import_rows (
  id          bigserial PRIMARY KEY,
  import_id   uuid NOT NULL,
  line        int  NOT NULL,
  sku         text NOT NULL,
  quantity    int  NOT NULL CHECK (quantity > 0),
  created_at  timestamptz NOT NULL DEFAULT now(),
  UNIQUE (import_id, line)          -- natural idempotency key
);
```

```python
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class ItemFailure:
    line: int
    code: str                 # CONFLICT | VALIDATION | ...
    message: str              # safe, per-line
    retryable: bool

@dataclass
class BulkResult:
    kind: Literal["all_succeeded", "partial", "all_failed"]
    succeeded: list[int] = field(default_factory=list)
    failed: list[ItemFailure] = field(default_factory=list)
    skipped: list[int] = field(default_factory=list)
```

`skipped` exists so a late connection failure does not mislabel untried rows as invalid.

## Stage 2 — chunked import with per-row savepoints

```python
CHUNK = 500

def import_rows(tx, import_id, rows) -> BulkResult:
    # 24.9: one bad row must not abort the whole file → savepoint per row.
    succeeded, failed, skipped = [], [], []
    try:
        for start in range(0, len(rows), CHUNK):
            chunk = rows[start:start + CHUNK]
            tx.execute("SAVEPOINT chunk")
            try:
                for row in chunk:
                    outcome = _insert_one(tx, import_id, row)
                    if outcome is None:
                        succeeded.append(row.line)
                    else:
                        failed.append(outcome)
                tx.execute("RELEASE SAVEPOINT chunk")
            except DriverError as exc:
                # Chunk-level failure (e.g. lock timeout): roll back this chunk only,
                # then mark remaining rows as skipped and stop.
                tx.execute("ROLLBACK TO SAVEPOINT chunk")
                skipped.extend(r.line for r in rows[start + len(chunk):])
                failed.append(_translate_chunk(exc, start, len(chunk)))
                break
    except DriverError as exc:
        error = translate(normalize(exc), op="export.import")
        return BulkResult(kind="all_failed", failed=[ItemFailure(
            line=0, code=error.code, message=error.safe_message, retryable=error.transient,
        )])
    return _classify(succeeded, failed, skipped)


def _insert_one(tx, import_id, row):
    tx.execute("SAVEPOINT item")
    try:
        tx.execute(
            """INSERT INTO import_rows (import_id, line, sku, quantity)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (import_id, line) DO NOTHING""",
            (import_id, row.line, row.sku, row.quantity),
        )
        tx.execute("RELEASE SAVEPOINT item")
        return None
    except DriverError as exc:
        tx.execute("ROLLBACK TO SAVEPOINT item")
        error = translate(normalize(exc), op="export.insertRow")
        return ItemFailure(
            line=row.line, code=error.code,
            message=error.safe_message, retryable=error.transient,
        )
```

Why `ON CONFLICT DO NOTHING` **and** savepoints? `ON CONFLICT` handles the expected case
(re-upload of the same line). Savepoints handle everything else (`23502`, `23514`, a bad cast to
`int` from the CSV parser) so the statement does not poison the transaction.

> In Postgres, once a statement fails **without** a savepoint, the whole transaction is
> `25P02` ("current transaction is aborted"). The savepoint is what makes per-row continuation
> possible.

## Stage 3 — classify and persist the result

```python
def _classify(succeeded, failed, skipped) -> BulkResult:
    if not failed and not skipped:
        return BulkResult("all_succeeded", succeeded=succeeded)
    if not succeeded:
        return BulkResult("all_failed", failed=failed, skipped=skipped)
    return BulkResult("partial", succeeded=succeeded, failed=failed, skipped=skipped)


def finish_import(tx, job_id, result: BulkResult, lsn: str):
    # 24.10: persist per-line outcomes; the API is not the only consumer.
    tx.executemany(
        """INSERT INTO import_row_results (job_id, line, outcome, code, message)
           VALUES (%s, %s, %s, %s, %s)""",
        [(job_id, line, "succeeded", None, None) for line in result.succeeded]
        + [(job_id, f.line, "failed", f.code, f.message) for f in result.failed]
        + [(job_id, line, "skipped", None, None) for line in result.skipped],
    )
    tx.execute(
        """UPDATE import_jobs
              SET status=%s, ok_count=%s, failed_count=%s, skipped_count=%s,
                  consistency_lsn=%s::pg_lsn, finished_at=now()
            WHERE id=%s""",
        (result.kind, len(result.succeeded), len(result.failed), len(result.skipped),
         lsn, job_id),
    )
```

## Stage 4 — read-your-writes for the job status

```python
def get_import_job(request, job_id, db):
    token = verify(request.headers.get("X-Consistency-Token"))
    # 24.14: the client just triggered the import; do not read a lagging replica.
    if token and not replica_caught_up(db.replica, token["lsn"]):
        return db.primary.fetch_one(JOB_SQL, (job_id,))
    return db.replica.fetch_one(JOB_SQL, (job_id,))


def replica_caught_up(replica, lsn) -> bool:
    return replica.scalar(
        "SELECT pg_last_wal_replay_lsn() >= %s::pg_lsn", (lsn,)
    )
```

The write path returns the completed job with `consistency_lsn`, sets
`X-Consistency-Token`, and the immediate `GET /imports/{id}` is guaranteed to see
`completed_with_errors`.

## Stage 5 — the API response

```json
{
  "jobId": "9f1c...",
  "status": "completed_with_errors",
  "ok": 993,
  "failed": 7,
  "skipped": 0,
  "errors": [
    { "line": 41, "code": "VALIDATION", "message": "quantity must be greater than 0" },
    { "line": 87, "code": "CONFLICT", "message": "That value is already taken." }
  ],
  "retry": { "endpoint": "/imports/9f1c/retry", "lines": [41, 87] }
}
```

| Internal result | API `status` | HTTP | Retry allowed |
| --------------- | ------------ | ---- | ------------- |
| `all_succeeded` | `completed` | `200` | n/a |
| `partial` | `completed_with_errors` | `200` | failed lines only |
| `all_failed` (validation) | `failed` | `200` (job accepted, zero rows) | after fix |
| chunk failure | `completed_with_errors` + `skipped` | `200` | skipped + failed chunks |
| connection lost | `failed` | `503` | whole job, idempotent |

Returning `200` for a **completed job with rejected rows** is correct: the request succeeded, the
report contains the per-line failures. Reserve `4xx` for a malformed request and `5xx` for a job
that could not run.

## Stage 6 — retry only what failed

```python
def retry_failed(tx, job_id, db):
    rows = db.primary.any(
        """SELECT line, sku, quantity FROM import_rows_staging
            WHERE job_id=%s AND line = ANY(%s)""", (job_id, failed_lines))
    return import_rows(tx, job_id, rows)   # same UNIQUE key → idempotent
```

Because `(import_id, line)` is unique and handled with `ON CONFLICT DO NOTHING`, re-running the
whole file is also safe — but re-running only failed lines is cheaper and keeps counts stable.

## Tests

```python
def test_one_bad_row_does_not_abort_the_batch(tx):
    rows = [good(1), bad_quantity(2), good(3)]
    r = import_rows(tx, uuid4(), rows)
    assert r.kind == "partial"
    assert r.succeeded == [1, 3]
    assert [f.line for f in r.failed] == [2]

def test_reupload_is_idempotent(tx):
    jid = uuid4()
    first = import_rows(tx, jid, [good(1), good(2)])
    second = import_rows(tx, jid, [good(1), good(2)])
    assert first.kind == second.kind == "all_succeeded"
    assert tx.scalar("SELECT count(*) FROM import_rows WHERE import_id=%s", (jid,)) == 2

def test_chunk_failure_marks_remaining_as_skipped(tx, monkeypatch):
    monkeypatch.setattr(tx, "execute", fail_on_third_insert)
    r = import_rows(tx, uuid4(), [good(i) for i in range(1, 11)])
    assert r.kind in ("partial", "all_failed")
    assert r.skipped and r.failed

def test_status_read_sees_completed_job(tx, replica_lagging):
    jid, lsn = run_import_sync(tx, rows)
    assert get_import_job(fake_req(lsn), jid, db).status == "completed_with_errors"
```

## Key numbers

- Chunk **500** rows; 100,000 rows → 200 chunks, 200 savepoint groups.
- Postgres bind-parameter ceiling is **65,535**; at 4 params/row the theoretical max is ~16,000
  per statement — stay well under.
- Per-row savepoints add roughly **0.1–0.3 ms** each; acceptable for ≤ 100k-row imports.
- Report size: cap inline errors at **1,000** and link to the full CSV report.

## Takeaways

- One row's failure must not erase 999 successes — **savepoint per row** (or per small chunk).
- `ON CONFLICT` is for **expected** duplicates; savepoints are for unexpected failures.
- Return `succeeded` / `failed` / **`skipped`** and persist all three.
- `200` + per-line report beats `500` for a completed job with rejected rows.
- The job status read must honor the write's **LSN token** or hit the primary.
- The natural key `(import_id, line)` makes retries idempotent for free.

## Related

- [Bulk Operations and Partial Success (24.9, 24.10)](../01-concepts/04-bulk-operations-and-partial-success.md)
- [Read-After-Write and Consistency Mechanics](../02-deep-dive/02-read-after-write-and-consistency-mechanics.md)
- [Commit, Rollback, and Savepoints (Ch. 23)](../../23-transaction-and-rollback-error-handling/01-concepts/02-commit-rollback-and-savepoints.md)
- [File and Media Processing Errors (Ch. 43)](../../../part-16-specialized-saas-scenarios/43-file-and-media-processing-errors/README.md)
