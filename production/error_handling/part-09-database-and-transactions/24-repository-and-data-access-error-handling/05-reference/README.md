# Chapter 24 — Reference: Repository Error Handling

> Part IX · Chapter 24 · Quick reference
> **Prerequisite:** [Chapter 24 README](../README.md)

## 1. Repository error contract

```ts
type RepoCode =
  | "NOT_FOUND"          // required read/update matched nothing
  | "CONFLICT"           // unique/version/state conflict
  | "REFERENCE_MISSING"  // FK target absent (23503)
  | "RESOURCE_IN_USE"    // delete blocked by FK (23503 on delete / MySQL 1451)
  | "STALE_VERSION"      // optimistic-lock mismatch
  | "VALIDATION"         // not-null, check, type/cast
  | "DB_UNAVAILABLE"     // connection refused/reset, too many connections
  | "DB_TIMEOUT"         // statement timeout / canceled
  | "SCHEMA_MISMATCH"    // missing table/column (deploy skew)
  | "DATA_INTEGRITY"     // corrupt page/index, unexpected constraint state
  | "INTERNAL";          // unclassified

interface RepoError extends Error {
  code: RepoCode;
  category: "CONFLICT" | "VALIDATION" | "DEPENDENCY" | "INTERNAL";
  transient: boolean;
  retryScope: "none" | "statement" | "transaction";
  alert: boolean;
  safeMessage: string;      // user-safe, authored
  field?: string;           // public field name (allowlisted)
  op: string;               // "projects.insert"
  resource: string;         // "projects"
  cause: unknown;           // driver error — never serialized
}
```

**Invariants**

- `cause` is the only place `SQLSTATE`, SQL text, constraint, table, column, and `DETAIL` live.
- `safeMessage` never contains any of those.
- Exactly one function constructs `RepoError`.

## 2. Persistence → repository code map

| Driver signal | Repo code | Category | Transient | retryScope | HTTP |
| ------------- | --------- | -------- | --------- | ---------- | ---- |
| Postgres `23505` / MySQL `1062` | `CONFLICT` | CONFLICT | no | none | 409 |
| Postgres `23503` / MySQL `1452` (insert) | `REFERENCE_MISSING` | VALIDATION | no | none | 422 |
| Postgres `23503` / MySQL `1451` (delete) | `RESOURCE_IN_USE` | CONFLICT | no | none | 409 |
| Postgres `23502` / MySQL `1048` | `VALIDATION` | VALIDATION | no | none | 422 |
| Postgres `23514` / MySQL `3819` | `VALIDATION` | VALIDATION | no | none | 422 |
| Version predicate, 0 rows | `STALE_VERSION` | CONFLICT | no | none | 409/412 |
| Postgres `40001` | `CONFLICT`/serialization | DEPENDENCY | **yes** | transaction | 503/retry |
| Postgres `40P01` / MySQL `1213` | `CONFLICT`/deadlock | DEPENDENCY | **yes** | transaction | 503/retry |
| MySQL `1205` / Postgres `55P03` | `DB_TIMEOUT`/lock | DEPENDENCY | **yes** | transaction | 503 |
| Postgres `57014` | `DB_TIMEOUT` | DEPENDENCY | yes | statement | 503/504 |
| Postgres `53300` | `DB_UNAVAILABLE` | DEPENDENCY | yes | transaction | 503 |
| Postgres `08006` / `08001` / MySQL `2006`, `2013`, `1040` | `DB_UNAVAILABLE` | DEPENDENCY | yes | transaction | 503 |
| Postgres `08007` | `INTERNAL`/ambiguous | INTERNAL | no | none | 500 |
| Postgres `25P02` | `INTERNAL` (tx aborted) | INTERNAL | no | none | 500 |
| Postgres `42P01` / `42703` | `SCHEMA_MISMATCH` | INTERNAL | no | none | 500 |
| Postgres `XX001` | `DATA_INTEGRITY` | INTERNAL | no | none | 500 |
| MySQL `3024` (max exec time) | `DB_TIMEOUT` | DEPENDENCY | yes | statement | 503 |

Full classification tables: [Chapter 22 Reference](../../22-database-error-classification/05-reference/README.md).

## 3. CRUD decision table

| Operation | Result | Return | Code | Default HTTP |
| --------- | ------ | ------ | ---- | ------------ |
| `findById` | row | entity | — | 200 |
| `findById` | absent | `null` | — | 404 at use-case |
| `getById` | absent | throw | `NOT_FOUND` | 404 |
| `insert` | ok | row (`RETURNING`) | — | 201 |
| `insert` | duplicate | throw | `CONFLICT` (+`field`) | 409 |
| `insert` | replay with idempotency key | existing row | — | 200 |
| `update` | 1 row | row (`RETURNING`) | — | 200 |
| `update` | 0 rows, row exists, version differs | throw | `STALE_VERSION` | 409/412 |
| `update` | 0 rows, row absent | throw | `NOT_FOUND` | 404 |
| `delete` | ≥0 rows | `boolean` | — | 204 |
| `deleteOrFail` | 0 rows | throw | `NOT_FOUND` | 404 |
| `delete` | FK referenced | throw | `RESOURCE_IN_USE` | 409 |
| any | query failed | throw | translated | 5xx |

**Rule:** absence is an error only when the **use case** requires the row.

## 4. Bulk outcomes

```ts
type BulkResult<T> =
  | { kind: "all_succeeded"; succeeded: T[] }
  | { kind: "partial"; succeeded: T[]; failed: ItemFailure<T>[]; skipped: T[] }
  | { kind: "all_failed"; failed: ItemFailure<T>[]; skipped: T[] };
```

| Strategy | Partial success | Best for |
| -------- | --------------- | -------- |
| Single multi-row statement | no (all-or-nothing) | small atomic batches |
| Savepoint per item | yes | imports, user data |
| Savepoint per chunk | yes (per chunk) | large imports |
| `ON CONFLICT DO NOTHING` | duplicates hidden | idempotent replays |
| Checkpointed chunks | yes, resumable | very large / long jobs |

Limits: Postgres **65,535** bind params; chunk **500–5,000**; cap inline error lists (~1,000) and
link to a report.

## 5. Read consistency decision table

| Read | Source | Guarantee |
| ---- | ------ | --------- |
| Write response | primary (`RETURNING`) | read-your-writes |
| Edit form after save | primary / LSN token | strong |
| Auth, entitlements, billing | primary | strong |
| Idempotency-key lookup | primary | strong |
| Ambiguous commit resolution | primary only | strong |
| User dashboard | replica | eventual + freshness hint |
| Search / analytics | replica/index | eventual |

Mechanisms: `RETURNING` > signed LSN/GTID token > bounded sticky window > session pin.

Lag thresholds (tune to SLA): warn **> 2 s**, page **> 10 s** on primary-backed paths.

## 6. Leak checklist

| Check | Pass criteria |
| ----- | ------------- |
| Driver import | only in adapter package |
| Exception types | only `RepoError` leaves the repository |
| Serialization | explicit allowlist; `cause` non-enumerable |
| Codes | app codes only; no `23505` in responses |
| Constraint names | mapped via allowlist or omitted |
| SQL / `DETAIL` | logs only, redacted for PII |
| Error tracker | scrubbed; no SQL, params, PII |
| Stack traces | never in production responses |
| Debug endpoints | do not echo `cause` |
| Tests | assert internals absent **and** `cause` present |

## 7. Anti-pattern → fix

| Anti-pattern | Why it hurts | Fix |
| ------------ | ------------ | --- |
| `catch { return null }` | outages become 404s | translate and throw |
| `throw new Error("db")` | no classification | typed `RepoError` |
| `field: err.constraint` | schema leak | allowlist |
| `200` after 0-row update | silent lost update | `STALE_VERSION` |
| Delete throws when absent | breaks retries | idempotent delete |
| `boolean` from bulk | lies about partial success | per-item result |
| Write → replica read | "lost saves" | `RETURNING` / token |
| Repo retries internally | hides attempts, breaks budgets | retry in service |

## 8. Glossary

| Term | Meaning |
| ---- | ------- |
| **Translation membrane** | the single boundary where driver errors become app errors |
| **Read-your-writes** | a client observes its own committed write |
| **Consistency token** | signed LSN/GTID returned by a write and checked on read |
| **Lag budget** | maximum acceptable replica staleness per read class |
| **Savepoint** | transaction sub-boundary that can be rolled back independently |
| **Idempotent delete** | deleting an absent row still succeeds |
| **Stale version** | optimistic-lock mismatch (row changed since read) |
| **Skipped item** | bulk row that was never attempted |

## 9. Related chapters

- [Chapter 22 — Database Error Classification](../../22-database-error-classification/README.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../../23-transaction-and-rollback-error-handling/README.md)
- [Error Translation and Normalization (Ch. 16)](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- [Idempotency and Duplicate-Operation Safety (Ch. 28)](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Consistency and Concurrency Failures (Ch. 40)](../../../part-15-distributed-failures/40-consistency-and-concurrency-failures/README.md)
- [Sensitive Data and Error Context (Ch. 36)](../../../part-13-security-aware/36-sensitive-data-and-error-context/README.md)
