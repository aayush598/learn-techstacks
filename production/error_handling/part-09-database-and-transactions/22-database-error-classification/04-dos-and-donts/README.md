# Chapter 22 — Do's and Don'ts

> Part IX · Chapter 22 · All sections

A condensed rule set for classifying database failures. Use it in code review.

## Classification

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Bucket by **SQLSTATE class** first, refine by code | Match English error messages |
| Read MySQL **`errno`** (`1062`, `1452`, `1213`) | Treat every `23000` as a duplicate |
| Give every class all four policy bits: transient, http, alert, retryScope | Decide retry ad hoc in each handler |
| Default unknown codes to **permanent + alert** | Default unknown codes to "retry" |
| Keep **one** classifier module | Maintain separate API/worker classifiers |

## Constraints (`23`)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map `23505`→`409`, `23503`→`422`/`404`, `23502`/`23514`→`422` | Map all `IntegrityError` to `500` |
| Derive `details.field` from a constraint allowlist | Echo the constraint/index name |
| Treat a dedupe-table `23505` as success | Retry a business `23505` |
| `ROLLBACK` (or savepoint) after a class-`23` error | Keep querying in a failed transaction (`25P02`) |
| Alert when pre-validated input hits `23502` | Assume not-null is always user error |

## Concurrency and timeouts (`40`, `55`, `57`)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Retry the **whole transaction** on `40001`/`40P01`/`1213` | Retry one statement inside an aborted txn |
| Re-read state before re-applying | Reuse stale `balance`/`version` |
| Cap retries (~3) with jittered backoff | Retry indefinitely |
| Set `lock_timeout` and `statement_timeout` | Wait forever on a lock |
| Treat MySQL `1205` as statement-level rollback | Assume the whole transaction aborted |

## Connections, capacity, availability (`08`, `53`, `57P0x`)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set explicit pool max and a non-zero acquire timeout | Leave Go's `0` (unlimited) pool |
| Distinguish `POOL_EXHAUSTED` from `DB_UNAVAILABLE` | Log both as "connection error" |
| Back off and shed load on `53300` | Retry `53300` inline |
| Separate pools per workload | Share one pool between API and exports |
| Page on `28P01`/`1045` immediately | Retry a bad password |

## Schema, migrations, corruption (`42`, `58`, `XX`)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Alert on `42xxx` and `XXxxx` immediately | Return `422` for a missing table |
| Use expand/contract for renames/drops | Drop a column the live code still reads |
| Run migrations under an advisory lock | Let replicas migrate concurrently |
| Fail closed on corruption | Retry a corrupted read |
| Assume MySQL DDL **cannot** roll back | Write multi-step non-idempotent DDL |

## Anti-patterns in the wild

1. **The `IntegrityError` blanket** — every constraint becomes `500`, users see fake outages.
2. **The message matcher** — `if "duplicate key" in str(e)`, broken by upgrade/locale.
3. **The statement retry** — retries `40001` inside a dead transaction; always fails.
4. **The infinite pool** — Go's default `SetMaxOpenConns(0)` DoS-es the server.
5. **The leaky detail** — logs/returns Postgres `DETAIL` containing user data.
6. **The silent `25P02`** — catch constraint error, keep using the transaction.
7. **The transient unknown** — unknown SQLSTATE retried forever.

## Chapter checklist

- [ ] Every DB error is classified by class, then code.
- [ ] Class `23` is permanent; class `40`/`08`/`53` are transient.
- [ ] Class `42`/`XX`/auth alerts; class `23` never pages.
- [ ] No `SQLSTATE`, constraint name, or `DETAIL` leaves the repository.
- [ ] MySQL paths key on `errno`.
- [ ] Pool sizes and timeouts are explicit.
- [ ] Unknown errors are permanent, generic, and alerting.

## Related

- [Chapter 22 Reference](../05-reference/README.md)
- [Chapter 24 Do's and Don'ts](../../24-repository-and-data-access-error-handling/04-dos-and-donts/README.md)
- [Error Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
