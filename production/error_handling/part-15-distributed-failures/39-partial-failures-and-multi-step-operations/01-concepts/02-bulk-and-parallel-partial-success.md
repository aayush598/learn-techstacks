# Bulk and Parallel Partial Success (39.4–39.5)

> Part XV · Chapter 39 · Sections 39.4–39.5 · _Estimated reading time: 18 min_
> **Prerequisite:** [Partial Failure and Multi-Step Operations (39.1–39.3)](./01-partial-failure-and-multi-step-operations.md)

## In one sentence

When a batch or a fan-out finishes with **some items succeeded and some failed**, the only honest
answer is a **per-item result plus an aggregate** — never a single boolean, and never a silent
`200`.

## Why this matters in production

`ExportJob` processes 50,000 rows; 312 fail validation. If the job is marked `succeeded`, the
customer exports wrong data and never learns why. If it is marked `failed`, the 49,688 good rows
vanish and the customer files a ticket. Both are bugs in the *contract*, not in the code. The same
shape appears everywhere: bulk invite emails, multi-tenant migrations, `WebhookIngest` batches,
parallel fan-out calls to three providers. A system that cannot express "mostly" will silently
convert partial success into either total success or total failure.

## Core concept

Two different phenomena share the word "partial" — keep them apart:

| | **Bulk partial success (39.4)** | **Parallel partial success (39.5)** |
| - | ------------------------------ | ----------------------------------- |
| Structure | N independent items in one unit of work | K concurrent branches of one operation |
| Failure unit | an item | a branch |
| Typical code | loop with per-item try/catch | `Promise.allSettled` / errgroup |
| Reporting | per-item status + aggregate counts | per-branch outcome + overall status |
| Retry scope | the failed items only | the failed branches only |
| Classic bug | all-or-nothing response | `all()` first-error cancels the truth |

**Bulk** is *sequential or batched but item-addressable*. **Parallel** adds a wrinkle: branches
race, one may fail while another is still running, and cancellation may be the right response.

```text
Bulk (39.4)                      Parallel (39.5)
┌──────────────┐                 ┌── branch A: ok ──────────▶┐
│ item 1  ✓    │                 ├── branch B: 409 conflict ─┼─▶ aggregate:
│ item 2  ✗    │                 ├── branch C: ok            │    ok=2, conflict=1,
│ item 3  ✓    │                 └── branch D: timeout ──────┘    timeout=1
│ ...          │
└──────────────┘                 status = PARTIAL (never "failed")
```

## How it works (mechanics)

### 39.4 Bulk partial success

The response shape is the design. Give every item a stable identity and a classified status:

```ts
type ItemResult<T> = {
  key: string;                       // caller-supplied stable id (row id, email, sku)
  status: "succeeded" | "failed" | "skipped" | "unknown";
  code?: string;                     // registry code, e.g. IMPORT_ROW_INVALID
  http?: number;                     // per-item semantic: 422, 409, 404...
  retryable?: boolean;
  value?: T;
};

type BulkResult<T> = {
  status: "succeeded" | "partial" | "failed";
  counts: { total: number; succeeded: number; failed: number; skipped: number; unknown: number };
  results: ItemResult<T>[];
};
```

Decision rules:

1. **Aggregate status is derived, never hand-set.** `failed=0 → succeeded`; `succeeded=0 →
   failed`; otherwise `partial`.
2. **`unknown` items must exist.** An item whose write timed out is not "failed" — it may be
   applied. Collapsing it to `failed` invites a duplicate on retry.
3. **Retry is scoped to items**, with the same idempotency key the item originally used.
4. **HTTP status describes the batch, codes describe the items.** `207`-style multi-status is
   uncommon in JSON APIs; the common, portable choice is **`200` with `status: "partial"`** when
   the batch was accepted and processed, or **`422`** only when *nothing* was processed because of
   a request-level problem. State the choice in the contract and keep it consistent.
5. **Cap what you report.** 50,000 item results in one response is a denial of service against
   yourself — return the first N failures plus counts, and put the full report behind the job.

### 39.5 Parallel partial success

```ts
// Promise.all → first rejection hides everything else. Never the shape you want
// for a multi-branch operation whose branches are independent.
const settled = await Promise.allSettled(branches.map((b) => run(b)));

const results = settled.map((s, i) =>
  s.status === "fulfilled"
    ? { branch: branches[i].name, status: "succeeded" as const }
    : { branch: branches[i].name, status: "failed" as const, error: classify(s.reason) });

const failed = results.filter((r) => r.status === "failed");
const overall = failed.length === 0 ? "succeeded"
  : failed.length === results.length ? "failed" : "partial";
```

Choose the aggregation policy **explicitly** per operation:

| Policy | Semantics | Use when |
| ------ | --------- | -------- |
| **Collect-all** (`allSettled`) | every branch runs to completion, report all outcomes | branches are independent and cheap (read fan-out, bulk notify) |
| **Fail-fast** (`all`) | first failure cancels the rest | branches are dependent — later branches are meaningless without the first |
| **Quorum** | succeed if ≥ k branches succeed | redundant calls (three replicas, two must answer) |
| **Best-effort with compensation** | run all, then undo successes if the operation must be atomic | money or state that must not be left half-applied |

⚠️ **Hazard.** With `fail-fast`, a cancelled branch may already have committed its side effect.
Cancellation stops *attempting*, it does not *undo*. If a cancelled branch wrote something, you
now have an accidental partial failure — the ledger must say so.

## Worked example

```python
def import_rows(rows, tenant_id) -> dict:
    results, counts = [], {"total": len(rows), "succeeded": 0, "failed": 0,
                           "skipped": 0, "unknown": 0}
    for row in rows:
        try:
            with transaction():                 # one txn per row: rows are independent
                validate(row)
                upsert(row, tenant_id)
            results.append({"key": row.key, "status": "succeeded"})
            counts["succeeded"] += 1
        except AmbiguousOutcome:
            # The write may have landed. Do NOT report failed, do NOT blind-retry.
            results.append({"key": row.key, "status": "unknown", "retryable": True})
            counts["unknown"] += 1
        except DomainError as e:
            if e.permanent:
                results.append({"key": row.key, "status": "failed",
                                "code": e.code, "http": e.http, "retryable": False})
                counts["failed"] += 1
            else:
                results.append({"key": row.key, "status": "failed",
                                "code": e.code, "http": e.http, "retryable": True})
                counts["failed"] += 1
    status = ("succeeded" if counts["failed"] == counts["unknown"] == 0 else
              "failed" if counts["succeeded"] == 0 else "partial")
    return {"status": status, "counts": counts, "results": results}
```

```text
POST /v1/imports → 200
{ "status": "partial",
  "counts": { "total": 3, "succeeded": 1, "failed": 1, "skipped": 0, "unknown": 1 },
  "results": [
    { "key": "row:1", "status": "succeeded" },
    { "key": "row:2", "status": "failed", "code": "IMPORT_ROW_INVALID", "http": 422 },
    { "key": "row:3", "status": "unknown", "retryable": true } ] }
```

The client can now retry exactly `row:3` with the same idempotency key and never re-send `row:2`.

## Key data / numbers

- **`Promise.allSettled`** (Node ≥ 12.9) is the standard collect-all primitive; Go's `errgroup`
  gives fail-fast plus first-error retrieval; `Promise.all` fails on first rejection and drops the
  other results.
- For HTTP multi-status semantics, RFC 9110 defines **`207 Multi-Status`** (WebDAV); most JSON APIs
  instead use `200` + per-item status. Either is fine — inconsistency is not.
- Cap inline item results (commonly **100–1000** rows); larger batches belong to a job with a
  downloadable report.
- Per-item transactions: **1 transaction per item**, not one giant transaction — a single failing
  row must not roll back 49,687 good ones, and one huge transaction holds locks far too long.
- Parallel fan-out: bound concurrency (**commonly 8–32** concurrent branches per worker); unlimited
  fan-out turns partial failure into socket exhaustion.

## Real-world use case — Acme SaaS

`ExportJob` reported a single `succeeded`/`failed` for a whole file. During a schema migration, 2%
of tenants' rows had a missing `owner_id`; those exports silently omitted the column and customers
imported broken CSVs into their own analytics. The fix was a per-row ledger with
`succeeded/failed/skipped/unknown`, a `partial` aggregate, and a sidecar `.errors.csv`. Customers
began fixing their data themselves; the support queue for "bad export" emptied within a month, and
the job no longer needed a human to interpret failures.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Single boolean result | trivial | lies in both directions | never for real batches |
| Per-item results + aggregate | precise, actionable, retryable | larger contract, more code | default for all bulk work |
| Fail-fast on first error | simple, fast | discards completed work, may leave partial side effects | dependent branches only |
| All-or-nothing (single txn) | truly atomic | huge locks, one bad item blocks all | small, local, high-value batches |
| Async report (job + URL) | scales to huge batches | not synchronous, needs storage | thousands of items |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Derive aggregate status from item counts | Set `status: "succeeded"` by default |
| Keep an `unknown` item status | Collapse timeouts into `failed` |
| Retry only the failed/unknown items | Re-run the whole batch |
| Bound parallel branches with a concurrency limit | `Promise.all` over 10,000 fan-out calls |
| Return counts even when you truncate results | Ship 50k rows in one JSON response |

## Common mistakes

- **One transaction for the whole batch** — one poison row aborts everything; rollback is then
  indistinguishable from a batch failure.
- **`Promise.all` for independent branches** — the first error wins the narrative; four successes
  are reported as one failure.
- **Retrying the whole batch because one item failed** — duplicates for the successful items unless
  every item is idempotent (they usually are not).
- **Reporting `partial` as `failed`** — customers re-run work that already succeeded.
- **No stable item key** — retries cannot be scoped, so they are all-or-nothing by accident.

## Checklist

- [ ] Every bulk API returns per-item status and counts.
- [ ] Aggregate status is computed, not asserted.
- [ ] `unknown` exists in the contract and is never silently downgraded.
- [ ] Fail-fast vs collect-all is an explicit, documented choice per operation.
- [ ] Retries target only failed/unknown items with their original keys.
- [ ] Concurrency on parallel branches is bounded.
- [ ] Results are truncated with counts, not dumped wholesale.

## Related

- [Partial Failure and Multi-Step Operations (39.1–39.3)](./01-partial-failure-and-multi-step-operations.md)
- [States, Compensation Safety, and Irreversibility (39.13–39.16)](./05-states-compensation-safety-and-irreversibility.md)
- [Concurrent Failures and Aggregation](../../../part-12-async-and-background-jobs/31-asynchronous-error-handling/01-concepts/02-concurrent-failures-and-aggregation.md)
- [Partial Completion and Failure Contracts (32.14–32.22)](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/01-concepts/05-partial-completion-and-failure-contracts.md)
