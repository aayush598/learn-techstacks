# Classifying Real Failures with the Cast

> Part IX · Chapter 22 · Sections 22.2, 22.9, 22.11, 22.16 · _Estimated reading time: 22 min_
> **Prerequisite:** [SQLSTATE → Domain Error Mapping](./01-sqlstate-to-domain-error-mapping.md)

## In one sentence

The same driver exception means different things depending on **which operation was running** —
so classification needs the **operation context** (`resource`, `op`, idempotency state), not just
the `SQLSTATE`.

## Why this matters in production

`23505` from a webhook dedupe table means *success*; `23505` from an invitations table means
*conflict*. `57014` while exporting a million rows means *reduce the batch*; `57014` while
loading a dashboard means *the query is too slow for the latency budget*. A classifier that
ignores context will be "correct" per SQLSTATE and still wrong per operation. These are four
concrete traces from the recurring cast.

## Scenario 1 — `WebhookIngest`: `23505` is success

```text
Event:  POST /webhooks/stripe   invoice.paid  (duplicate delivery)
SQL:    INSERT INTO webhook_events (provider, event_id, payload)
        VALUES ('stripe', 'evt_1P...', $1)
Error:  SQLSTATE 23505, constraint webhook_events_provider_event_id_key
```

| Decision | Wrong | Right |
| -------- | ----- | ----- |
| Retry | yes (`500` → Stripe retries) | **no** |
| Response | `500` | **`200`** with stored result |
| Meaning | "insert failed" | "already processed" |
| Ledger effect | none | none (idempotent) |

```ts
async function ingest(event: StripeEvent) {
  try {
    const row = await repo.insertEvent(event);        // dedupe by unique key
    await processInTransaction(event);                // same transaction as the row
    return { status: 200, body: { received: true } };
  } catch (err) {
    const db = normalize(err);
    if (db.code === "23505" && db.constraint === "webhook_events_provider_event_id_key") {
      return { status: 200, body: { received: true, duplicate: true } };
    }
    throw classify(db, { resource: "webhooks:ingest" });  // everything else is real
  }
}
```

**Why `200`, not `409`:** the caller is Stripe, not a user. `409` triggers retries; `200` stops
them. The *user-facing* API uses `409` for the same code.

## Scenario 2 — `ExportJob`: `40P01` retries the transaction

```text
Job:    export tenant 42 → S3
Txn:    UPDATE export_jobs SET checkpoint = $1 WHERE id = $2
        UPDATE export_jobs SET rows_written = $3 WHERE id = $4
Error:  SQLSTATE 40P01 deadlock_detected
```

Two export workers for the same tenant updated the same checkpoint row in different orders.
The correct handling is **not** "fail the job": it is retry the **whole transaction** with a
fresh read of the checkpoint. On exhaustion, fail the *attempt* and let the queue retry with
backoff (Chapter 32).

```text
attempt 1: 40P01  → rollback → sleep 50ms + jitter → re-read checkpoint
attempt 2: 40P01  → rollback → sleep 120ms         → re-read
attempt 3: success → checkpoint advanced, no duplicate rows written
```

| Signal | Wrong | Right |
| ------ | ----- | ----- |
| `40P01` | mark job failed permanently | retry transaction (max 3) |
| `40001` | retry the single `UPDATE` | retry from `BEGIN` |
| exhaustion | `500` to the user | job failure + queue retry / DLQ |

## Scenario 3 — `Checkout`: `53300` means shed load

```text
Flow:   POST /checkout  (spike: 400 rps, pool max 25)
Error:  SQLSTATE 53300 too_many_connections  (server max_connections = 100, shared by 6 pods)
```

`53300` is **not** "the database is down". Every pod retrying immediately makes it worse. The
correct behavior:

```text
1. Do NOT retry inside the request (no free slot; retries add queue).
2. Return 503 + Retry-After: 2 with a stable code CHECKOUT_UNAVAILABLE.
3. Trip the breaker for the checkout path; keep reads on replicas.
4. Alert on pool saturation + server connection count, not on the individual 53300.
```

| Metric | Action |
| ------ | ------ |
| pool wait > 100ms p95 | scale pool *down* per pod or add PgBouncer |
| server connections > 80% `max_connections` | page; find the leak / bound total |
| `53300` sustained > 30s | shed load, `503`, backoff |

## Scenario 4 — `AgentRun`: `57014` is a deadline, not a bug

```text
Tool call: run_sql("SELECT ... FROM events WHERE tenant_id = $1 AND created_at > $2")
Error:     SQLSTATE 57014 query_canceled   (statement_timeout = 3s)
```

The agent's tool path has a **3 s** budget; the query has no supporting index. Retrying the same
query is guaranteed to time out again. Correct classification: `QUERY_TIMEOUT`, `transient=true`
for the *request*, but the **remedy is structural** — add the index, reduce the range, or
paginate. Surface a tool error the agent can reason about, not a `500`.

```ts
const SQL_TOOL_DEADLINE_MS = 3_000;

async function runSqlTool(sql: string) {
  try {
    return await db.query({ text: sql, statement_timeout: SQL_TOOL_DEADLINE_MS });
  } catch (err) {
    const db = normalize(err);
    if (db.code === "57014") {
      // Do not retry blindly; tell the agent the budget was exceeded.
      throw new ToolError("SQL_TIMEOUT", { retryable: false, budgetMs: SQL_TOOL_DEADLINE_MS });
    }
    throw classify(db, { resource: "agent:sql" });
  }
}
```

## Decision matrix

| Cast member | Error | Context | Verdict |
| ----------- | ----- | ------- | ------- |
| `WebhookIngest` | `23505` on `webhook_events` | dedupe insert | **success / `200`** |
| `WebhookIngest` | `23505` on `invoices` | business insert | `409`, no retry |
| `ExportJob` | `40P01`/`40001` | checkpoint update | retry whole txn, ≤3 |
| `ExportJob` | `42P01` | schema drift after deploy | **fail job, alert** |
| `Checkout` | `53300` | connection storm | `503` + shed, no inline retry |
| `Checkout` | `23503` | deleted plan referenced | `422`, refresh client |
| `AgentRun` | `57014` | 3 s tool budget | tool error, no automatic retry |
| `Acme API` | `08006` during failover | any read | retry once, then `503` |

## Key data / numbers

- `23505` on the **dedupe table** → `200`; on a **business table** → `409`. Same code.
- `40001`/`40P01`: **≤3 attempts**, jittered **20–160 ms**, whole transaction.
- `53300`: **no inline retry**; `Retry-After: 2–5`; server `max_connections` default **100**.
- `57014`: comes from `statement_timeout` (unset by default); the agent tool budget here is
  **3 s**.
- `42P01` after a deploy: **alert immediately**; do not retry or translate to `404`.

## Real-world use case — Acme SaaS

All four scenarios happened in the same week at Acme. The webhook endpoint `500`ed on a
duplicate and Stripe retried it 12 times; `ExportJob` marked a deadlock as a permanent failure
and skipped a checkpoint; `Checkout` retried `53300` in a loop and doubled its own load; and the
`AgentRun` SQL tool returned a generic `500` for a missing index. After adding **operation
context** to classification, each error took its correct path: duplicates became `200`, deadlocks
became invisible retries, capacity errors became fast `503`s, and the agent got an actionable
`SQL_TIMEOUT`. The week's database incident count went from four to zero.

## Trade-offs

| Context approach | Pros | Cons | When to use |
| ---------------- | ---- | ---- | ----------- |
| Pass `resource`/`op` into classifier | precise, no duplicate tables | every call site supplies it | default |
| Separate classifiers per module | local clarity | drift between modules | large teams with ownership |
| One global table only | simple | cannot distinguish dedupe vs business `23505` | single-purpose services |
| Infer from table name | no call-site change | fragile, leaks schema knowledge | small codebases |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Pass `resource`/`op` into `classify()` | Classify `23505` as one thing everywhere |
| Return `200` for webhook dedupe hits | Let Stripe retry successful duplicates |
| Retry the whole transaction on `40P01` | Mark the job permanently failed |
| Shed load on `53300` | Retry inside the request |
| Give the agent a typed tool error | Return a generic `500` for `57014` |

## Common mistakes

- **Treating every `23505` as a user conflict** — breaks idempotent webhooks.
- **Retrying `53300` with the same pool** — the retry cannot get a connection either.
- **Retrying `57014` unchanged** — same query, same timeout.
- **Alerting on `40P01`** — deadlocks are expected under contention.
- **Classifying without the operation** — same code, opposite correct outcome.

## Checklist

- [ ] Dedupe-table `23505` is success; business-table `23505` is `409`.
- [ ] Transaction retries are keyed on `40001`/`40P01` with a cap.
- [ ] Capacity errors shed load and never retry inline.
- [ ] Query timeouts produce actionable, non-retryable tool errors.
- [ ] Every call site passes `resource`/`op` context.

## Related

- [SQLSTATE → Domain Error Mapping](./01-sqlstate-to-domain-error-mapping.md)
- [Connections and Pool Errors (22.1–22.2)](../01-concepts/01-connection-and-pool-errors.md)
- [Retrying 40001 and 40P01 in Code](../../23-transaction-and-rollback-error-handling/03-practical-examples/01-retrying-40001-and-40p01.md)
- [Idempotency and Duplicate-Operation Safety](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
