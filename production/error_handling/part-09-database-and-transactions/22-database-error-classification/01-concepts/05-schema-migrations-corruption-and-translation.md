# Schema, Migrations, Corruption, and Translation (22.17–22.20)

> Part IX · Chapter 22 · Sections 22.17–22.20 · _Estimated reading time: 20 min_
> **Prerequisite:** [Failover, Replicas, and Unavailability](./04-failover-replicas-and-unavailability.md)

## In one sentence

Schema errors (`42xxx`), migration failures, and corruption (`XXxxx`) are **permanent,
deploy-caused faults that must page a human**, while everything the database tells you must be
**translated exactly once into stable application errors** at the persistence boundary.

## Why this matters in production

These are the failures that turn a routine deploy into an incident. A migration adds a column
and the old code still selects it as `NOT NULL` (`23502` for every insert); a rollback deploys
code that references a table the previous migration dropped (`42P01`); a disk fills and pages
come back corrupted (`XX001`). Unlike a duplicate email, none of these resolve with a retry,
a nicer message, or a client action. They require **alerting, deploy rollback, and a human** —
and the classification layer is the only place that can tell the difference.

## Core concept

| § | Failure | Postgres SQLSTATE | MySQL | Nature | Response |
| - | ------- | ----------------- | ----- | ------ | -------- |
| 22.17 | **Schema mismatch** | `42P01` undefined table, `42703` undefined column, `42601` syntax, `42704` undefined object | `1146` no such table, `1054` unknown column, `1064` syntax | permanent, deploy fault | `500` + **alert** |
| 22.18 | **Migration failure** | any of the above, plus `55P03` lock timeout, `40P01` deadlock during `ALTER` | `1205`, `1213`, `1846` (FK re-create) | permanent until fixed | abort deploy, alert, **roll back migration** |
| 22.19 | **Corruption / integrity** | `XX001` data corrupted, `XX002` index corrupted, `58P01` disk error, `XX000` internal | `1812` tablespace? (use generic), `1016` file read error | unrecoverable | fail closed, **page**, restore/repair |
| 22.20 | **Translation** | *(meta)* | *(meta)* | — | one boundary, stable app codes |

**The division of labor is absolute:** class `42` and `XX` are *not* validation errors, *not*
retryable, and *not* the user's fault. Class `23` and `22` are data/rule errors. Confusing them
is how teams end up showing "invalid input" for a missing table.

## How it works (mechanics)

### Schema mismatch (22.17)

Occurs when **code and schema disagree**, almost always during a rolling deploy:

```text
t0  migration v42 drops column projects.archived_at
t1  old app instances (still running) SELECT archived_at → 42703 on every request
t2  new code deployed; errors stop
```

The **expand/contract** pattern prevents it: add new columns first, deploy code that writes
both, backfill, then remove the old column in a later release. Never drop or rename a column
that the currently-deployed code still reads.

### Migration failures (22.18)

- **Postgres has transactional DDL**: a failed `ALTER TABLE` inside a transaction rolls back
  cleanly. Run each migration in a transaction and take an **advisory lock** so two deploy
  replicas do not migrate concurrently.
- **MySQL auto-commits DDL**: a failed multi-step migration leaves partial schema changes.
  Keep migrations small, idempotent (`IF NOT EXISTS`), and verify state before proceeding.
- Long `ALTER TABLE`s take locks; pair with `lock_timeout` so a migration fails fast instead of
  blocking traffic (Chapter 23 covers retry, not migration).

```sql
-- Postgres: serialize migrations across replicas
SELECT pg_advisory_lock(82420261);          -- arbitrary, stable app-wide key
-- ... run migration statements ...
SELECT pg_advisory_unlock(82420261);
```

### Corruption / integrity (22.19)

These indicate the **storage layer itself is wrong**: bad pages, checksum failures, broken
indexes, impossible values. Retrying cannot help and may spread damage. Stop writes, fail
closed, page, and restore from a known-good backup or rebuild the index.

### Translation (22.20)

Translation is the *terminal* step for every other subsection: map the class to a **stable
application error** with a category, retry flag, public message, and alert flag. Only the
repository/driver adapter reads `SQLSTATE` or `errno`; everything above speaks your codes.

## Worked example

```python
# One classifier, all classes, explicit defaults. No SQLSTATE leaves this function.
def classify_db_error(exc: BaseException, *, op: str) -> AppError:
    state = getattr(exc, "pgcode", None) or getattr(exc, "sqlstate", None)

    if state in ("42P01", "42703", "42601", "42704", "3F000"):
        return AppError("SCHEMA_MISMATCH", "INTERNAL", transient=False,
                        http=500, alert=True, op=op, cause=exc)
    if state in ("XX001", "XX002", "XX000", "58P01"):
        return AppError("DATA_CORRUPTION", "INTERNAL", transient=False,
                        http=503, alert=True, fail_closed=True, op=op, cause=exc)
    if state in ("23505", "23503", "23502", "23514"):
        return AppError("CONSTRAINT_VIOLATION", "CONFLICT", transient=False,
                        http=409, alert=False, op=op, cause=exc)
    if state in ("40001", "40P01", "55P03"):
        return AppError("RETRYABLE_CONFLICT", "CONCURRENCY", transient=True,
                        http=409, alert=False, op=op, cause=exc)
    if state in ("08006", "08003", "08001", "53300", "57P03"):
        return AppError("DB_UNAVAILABLE", "DEPENDENCY", transient=True,
                        http=503, alert=False, op=op, cause=exc)
    # Unknown: never assume transient on a write, never claim success.
    return AppError("DB_UNKNOWN", "INTERNAL", transient=False,
                    http=500, alert=True, op=op, cause=exc)
```

```text
Production trace after a bad deploy:
  SELECT archived_at ... → 42703
  classify → SCHEMA_MISMATCH (alert=true, transient=false)
  API → 500 INTERNAL, generic detail, correlation id
  alert → "schema mismatch on projects, deploy v42" within seconds
```

## Key data / numbers

- Class **`42`** prefix = syntax/access/schema; most `42xxx` in production mean **deploy
  mismatch**, not a user mistake.
- Postgres **`55P03`** during `ALTER TABLE` means a lock timeout — fail the migration, don't
  queue traffic behind it.
- MySQL DDL is **auto-committing**: there is no `ROLLBACK` for a half-applied migration;
  design migrations to be resumable.
- `XX001`/`XX002` are **corruption**; `58P01` is an **I/O/disk** failure. Both are `503`-class
  and page.
- Alert rule of thumb: **class `42` and `XX` page immediately; class `23`/`40` never page; class
  `08` pages only if sustained > 30 s.**

## Real-world use case — Acme SaaS

Acme deployed a migration that renamed `projects.archived_at` to `projects.archived_on` in a
single step. Old pods kept selecting `archived_at` and produced **`42703`** on every project
read; because the generic handler mapped it to a `500` with no alert, the team learned from
customers. Two changes followed: migrations now follow **expand/contract** (add `archived_on`,
dual-write, backfill, drop later), and class-`42` errors carry `alert=true` so a schema mismatch
pages within a minute. The next rename shipped with zero user-visible errors.

## Trade-offs

| Decision | Pros | Cons | When to use |
|----------|------|------|-------------|
| Single-step rename | fast | breaks rolling deploys | never in production |
| Expand/contract | zero-downtime | 2–3 releases, backfill job | any column rename/drop |
| Transactional DDL (Postgres) | clean rollback | locks held longer | default in Postgres |
| Small idempotent DDL (MySQL) | resumable after failure | more manual steps | default in MySQL |
| Fail-open on corruption | availability | **spreads corruption** | never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Alert on `42xxx`/`XXxxx` immediately | Show schema errors as `422` to users |
| Use expand/contract for renames and drops | Rename a column the live code reads |
| Take an advisory lock around migrations | Let several replicas migrate at once |
| Fail closed on `XX001`/`XX002` | Retry a corrupted read |
| Translate once, keep `SQLSTATE` server-side | Put `42P01` or a table name in the API |

## Common mistakes

- **Mapping `42P01` to "not found"** — the table is missing, not the row.
- **Retrying schema or corruption errors** — they never succeed and can worsen damage.
- **Dropping a column in the same release that stops using it** — rolling deploys guarantee a
  window where old code still needs it.
- **Assuming MySQL migrations roll back** — they do not.
- **Leaking `relation "projects" does not exist`** — reveals schema and confuses clients.

## Checklist

- [ ] Class `42` and `XX` are `alert=true`, `transient=false`, and return `500`/`503`.
- [ ] The API response never contains table, column, or SQLSTATE text.
- [ ] Every rename/drop follows expand/contract.
- [ ] Migrations run under an advisory lock and with `lock_timeout`.
- [ ] Corruption triggers fail-closed and a restore runbook, not a retry.

## Related

- [Query Execution and Constraint Violations (22.3–22.8)](./02-query-execution-and-constraint-violations.md)
- [SQLSTATE Classification Table](../02-deep-dive/01-sqlstate-classification-table.md)
- [Transaction Boundaries and Atomicity (23.1–23.2)](../../23-transaction-and-rollback-error-handling/01-concepts/01-transaction-boundaries-and-atomicity.md)
- [Chapter 22 Reference — SQLSTATE Cheat Sheet](../05-reference/README.md)
