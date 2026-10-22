# Chapter 22 — Database Error Classification

> Part IX · _Estimated reading time: 75–100 min_
> **Prerequisite:** [Error Categories in Detail (5.13 Database)](../../part-02-error-taxonomy/05-error-categories-in-detail/01-concepts/02-limits-concurrency-and-data.md)

## One-sentence summary

Every database failure belongs to one of a handful of **classes** — connection, constraint,
concurrency, availability, schema, integrity — and the class, not the exception type, decides
**retry, response, and alert**.

## Why this chapter matters

A `try/catch` around a query that logs "insert failed" and returns `500` is the default in most
codebases, and it is wrong in four different ways: a duplicate invitation becomes an outage, a
deadlock becomes a user-facing error, a schema bug pages nobody, and a pool timeout hammers a
struggling database with retries. The fix is not more catch blocks — it is a **classification
table** that maps `SQLSTATE` (Postgres), error numbers (MySQL), and ORM codes to your
application's error categories, once, at one boundary.

## Chapter map

The chapter has 20 sections. They are grouped into these files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-connection-and-pool-errors.md`](./01-concepts/01-connection-and-pool-errors.md) | 22.1, 22.2 | Connection establishment failures and pool exhaustion (`08006`, `53300`) |
| [`01-concepts/02-query-execution-and-constraint-violations.md`](./01-concepts/02-query-execution-and-constraint-violations.md) | 22.3–22.8 | Query execution errors; unique `23505`, FK `23503`, not-null `23502`, check `23514` |
| [`01-concepts/03-conflicts-locks-and-timeouts.md`](./01-concepts/03-conflicts-locks-and-timeouts.md) | 22.9–22.13 | Deadlock `40P01`, lock timeout `55P03`, query timeout `57014`, serialization `40001` |
| [`01-concepts/04-failover-replicas-and-unavailability.md`](./01-concepts/04-failover-replicas-and-unavailability.md) | 22.14–22.16 | Failover, read-replica lag and read-only writes, unavailable/unreachable databases |
| [`01-concepts/05-schema-migrations-corruption-and-translation.md`](./01-concepts/05-schema-migrations-corruption-and-translation.md) | 22.17–22.20 | Schema mismatch, migration failures, corruption, translating to stable app errors |
| [`02-deep-dive/01-sqlstate-classification-table.md`](./02-deep-dive/01-sqlstate-classification-table.md) | 22.3–22.13, 22.17, 22.20 | The full SQLSTATE class → category → retry → HTTP decision table |
| [`02-deep-dive/02-driver-and-vendor-error-shapes.md`](./02-deep-dive/02-driver-and-vendor-error-shapes.md) | 22.1–22.6, 22.20 | How node-pg, psycopg2, pq/pgx, mysql2, and Prisma expose codes — and how to read them safely |
| [`03-practical-examples/01-sqlstate-to-domain-error-mapping.md`](./03-practical-examples/01-sqlstate-to-domain-error-mapping.md) | 22.4–22.6, 22.9, 22.20 | A runnable classification module: Postgres `SQLSTATE` + MySQL numbers → domain errors |
| [`03-practical-examples/02-classifying-real-failures-with-the-cast.md`](./03-practical-examples/02-classifying-real-failures-with-the-cast.md) | 22.2, 22.9, 22.11, 22.16 | `ExportJob`, `WebhookIngest`, and `Checkout` failing against a live database |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Classification rules, anti-patterns, review checks |
| [`05-reference/README.md`](./05-reference/README.md) | all | SQLSTATE cheat sheet, MySQL error table, decision table, chapter glossary |

## Learning objectives

By the end you can:

- Read any database error (Postgres `SQLSTATE`, MySQL `errno`, ORM code) and classify it as
  connection / constraint / concurrency / availability / schema / integrity.
- Say for each class: is it **transient**, who should **see** it, and who should be **alerted**.
- Explain why `23505` is a business-visible conflict, `40001` is an invisible retry, and `42P01`
  is a page for on-call.
- Distinguish *the query failed* from *the row was not there*, and *the pool is full* from *the
  database is down*.

## Key takeaways

1. **Class first, code second.** Decide policy per SQLSTATE class; only then map to a specific
   application error code.
2. **Constraint errors are answers, not accidents.** `23505`/`23503` usually mean a legitimate
   business conflict or duplicate submission.
3. **Class 40 and class 08 are transient** — retry with backoff; class 23 and class 42 are not.
4. **Class 42 and corruption errors alert.** A schema mismatch after a deploy is discovered by
   users in minutes if nothing pages.
5. **Never let `SQLSTATE`, constraint names, or SQL text cross the repository.** Translate once,
   preserve the cause as server-side `cause` only.

## Exercises

1. Take your five most common database errors in production and write their SQLSTATE/errno,
   class, retry decision, HTTP status, and alert decision in one table.
2. Find every place in your code that inspects a driver exception directly. Count how many
   layers deep the vendor code travels.
3. Trigger a `42P01`/`1146` locally (rename a table) and verify your alert fires before your
   test suite does.
4. Prove which of your errors are retryable: run the same insert twice under two connections and
   observe `40001` vs `23505`.

## Related

- [Chapter 23 — Transaction and Rollback Error Handling](../23-transaction-and-rollback-error-handling/README.md)
- [Chapter 24 — Repository and Data Access Error Handling](../24-repository-and-data-access-error-handling/README.md)
- [Error Translation and Normalization (16.4 DB→domain)](../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- [Glossary](../../GLOSSARY.md)
