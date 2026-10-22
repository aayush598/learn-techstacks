# Limits, Concurrency, and Data Categories (5.10–5.15, 5.28)

> Part II · Chapter 5 · Sections 5.10–5.15, 5.28 · _Estimated reading time: 30 min_
> **Prerequisite:** [Input, Auth, and Business Categories](./01-input-auth-and-business-errors.md)

## In one sentence

This family covers **rate limits, quotas, concurrency conflicts, databases, caches, file storage,
and data integrity** — the categories where retry safety, transactions, and correctness live.

## Why this matters in production

Here the stakes jump from a bad response to **wrong data and double charges**. A retried
serialization failure can be correct; a retried `23505` is a duplicate; a cache failure must never
be treated like a database failure; and a data-integrity failure must stop everything, never
"continue and fix later."

## 5.10 Rate limiting

A **rate limit** throttles request *rate* to protect a resource. It is a signal, usually
**transient and retryable**.

| Aspect | Value |
| ------ | ----- |
| HTTP | `429` |
| Headers | `Retry-After`, `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset` |
| Retry | **yes**, with backoff + `Retry-After` |
| Code | `RATE_LIMIT_EXCEEDED` |

Rate limits are **per-caller** (token bucket / sliding window). Always honor `Retry-After`; never
retry immediately in a tight loop (retry storm, Chapter 27).

## 5.11 Quota / usage limit

A **quota** is a *business* limit: exports this month, API calls on the plan, storage bytes. It is
**permanent until the plan or window changes**, so it is **not retryable**.

| Aspect | Value |
| ------ | ----- |
| HTTP | `429` or `402`/`403` |
| Retry | no (resets at period boundary, not on backoff) |
| Code | `QUOTA_EXPORT_LIMIT`, `QUOTA_API_CALLS` |

> ⚠️ **Hazard.** Quota (`429`/`402`) and rate limit (`429`) can share a status. Use the **code**
> to disambiguate: one says "slow down," the other says "upgrade or wait for reset."

## 5.12 Concurrency / optimistic locking

Two writers race; the loser must detect and re-read. This is a **transient conflict** in the
database sense — retrying with fresh state usually succeeds.

| Trigger | Postgres SQLSTATE | gRPC | HTTP |
| ------- | ----------------- | ---- | ---- |
| serialization failure | `40001` | `ABORTED (10)` | `409`/`412` |
| deadlock detected | `40P01` | `ABORTED (10)` | `409` |
| version mismatch | — | — | `412` (`If-Match`) |

Optimistic locking: read `ETag`, send `If-Match`, receive `412 Precondition Failed` if stale.
Always **re-read and re-apply** on retry; never retry the same stale write (Chapter 40).

## 5.13 Database

Database failures split into **connection/pool** (transient) and **constraint** (permanent):

| Class | SQLSTATE | Retry | Note |
| ----- | -------- | ----- | ---- |
| unique violation | `23505` | no | duplicate operation |
| foreign key violation | `23503` | no | conflict or validation |
| not-null violation | `23502` | no | programming/validation bug |
| check violation | `23514` | no | business rule / validation |
| serialization failure | `40001` | **yes** | re-read and retry |
| deadlock | `40P01` | **yes** | retry whole transaction |
| query canceled | `57014` | depends | often a timeout |
| connection failure | `08xxx` | **yes** | pool/reconnect |
| too many connections | `53300` | **yes** (backoff) | pool exhaustion |

> ⚠️ **Never expose SQLSTATE to clients.** It reveals schema. Log it; translate it (Chapter 22).

## 5.14 Cache

**Cache** failures are usually **optional**: a failed read falls through to the source of truth.
But cache *writes* and *invalidation* failures can cause **stale data**, which is worse.

| Trigger | Redis | Policy |
| ------- | ----- | ------ |
| miss | `nil` | not an error — read source |
| unavailable | connection error | bypass cache; don't fail the request |
| read-only replica | `READONLY` | refresh topology |
| loading dataset | `LOADING` | transient; retry briefly |
| cluster down | `CLUSTERDOWN` | fail fast or bypass |

Distinguish a **cache miss** (normal) from a **cache error** (fall through). Never 500 a page
because the cache is down.

## 5.15 File storage

Object-storage failures (S3 and compatible) are usually **transient and retryable** but some are
**permanent**:

| Trigger | S3 error | Retry |
| ------- | -------- | ----- |
| key missing | `NoSuchKey` (`404`) | no |
| access denied | `AccessDenied` (`403`) | no |
| object too large | `EntityTooLarge` | no |
| throttled | `SlowDown` (`503`) | yes |
| network/5xx | `500`/`502`/`503` | yes |

Multipart uploads add **partial completion** semantics: abort on failure to avoid orphaned parts
(Chapter 43).

## 5.28 Data integrity

**Data integrity** failures mean the data itself is wrong: checksum mismatch, referential
corruption, impossible state, failed invariant. These are **unrecoverable** — you must **not
continue**.

| Trigger | Example | Policy |
| ------- | ------- | ------ |
| checksum mismatch | corrupted export blob | fail, quarantine, alert |
| orphaned reference | FK broken by a bypass | fail, alert page |
| invariant violation | negative balance | abort, roll back, page |

Integrity failures map to `500` (or a dedicated `DATA_INTEGRITY` code), log at `critical`, and
**never retry** — retrying corrupt input corrupts output.

## Worked example — ExportJob

```text
ExportJob reads 1M rows and writes to S3:
  DB serialization failure (40001)   → 5.12 concurrency → retry after re-read
  DB unique violation on checkpoint  → 5.13 database    → duplicate; do NOT retry blindly
  Redis unavailable                  → 5.14 cache       → bypass, continue
  S3 SlowDown (503)                  → 5.15 file_storage→ retry with backoff
  checksum mismatch on final object  → 5.28 data_integrity → abort, quarantine, page
```

One job, five categories, three different outcomes — retry, bypass, abort.

## Key data / numbers

- `Retry-After` is authoritative for `429`/`503`; respect it before your own backoff.
- PostgreSQL `40001`/`40P01` are **safe to retry** inside a transaction; `23505`/`23503`/`23514`
  are **not**.
- Redis `LOADING`/`READONLY`/`CLUSTERDOWN` are distinct conditions with different handling.
- S3 `SlowDown` returns `503` and is explicitly retryable with backoff.

## Real-world use case — Acme SaaS (billing)

Acme's invoice generator retried every DB error, including `23505`, producing duplicate invoices.
After classification, `40001`/`40P01` retry with fresh reads, while `23505` is treated as
**duplicate operation** (Chapter 5.8) and the existing invoice is returned idempotently. Duplicate
invoices went to zero and the retry budget stopped being consumed by permanent failures.

## Trade-offs

| Category | Retry? | Why |
| -------- | ------ | --- |
| rate_limit | yes | transient by design |
| quota | no | resets on period, not backoff |
| concurrency (40001) | yes | re-read then retry |
| database constraint | no | permanent condition |
| cache | bypass | optional dependency |
| data_integrity | no | retrying worsens corruption |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Honor `Retry-After` | Hammer `429` immediately |
| Disambiguate quota vs rate limit by code | Treat both as retryable |
| Retry `40001`/`40P01` with fresh state | Retry `23505` |
| Bypass cache on error | 500 when Redis is down |
| Abort on integrity failure | "Continue and fix later" |

## Common mistakes

- **Retrying `23505`** and creating duplicates or burning budget.
- **Confusing quota with rate limit** and backing off forever.
- **Failing requests when optional caches are down.**
- **Ignoring multipart partial completion**, leaving orphaned parts.

## Checklist

- [ ] Are quota and rate limit distinguished by code?
- [ ] Does retry re-read state for `40001`/`40P01`?
- [ ] Are DB constraint errors permanent and translated?
- [ ] Does cache failure bypass, not 500?
- [ ] Do integrity failures abort and page?

## Related

- [Input, Auth, and Business Categories](./01-input-auth-and-business-errors.md)
- [External, Network, and Config Categories](./03-external-network-and-config.md)
- [Database Error Classification](../../../part-09-database-and-transactions/22-database-error-classification/README.md)
- [Consistency and Concurrency Failures](../../../part-15-distributed-failures/40-consistency-and-concurrency-failures/README.md)
