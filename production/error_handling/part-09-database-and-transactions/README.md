# Part IX — Database, Persistence, and Transaction Errors

> **Chapters 22–24.** Databases fail in ways no other dependency does: they refuse
> connections, they abort half a unit of work, they deadlock, and — worst of all — they can
> commit your change and lose the acknowledgment. This part turns **SQLSTATE codes, transaction
> semantics, and repository boundaries** into a repeatable handling standard.

## Learning objectives

By the end of Part IX you will be able to:

1. **Classify any database failure** by SQLSTATE class (Postgres), error number (MySQL), or ORM
   code, and say what each class means for retry, user messaging, and alerting.
2. **Choose the safe outcome per class**: constraint violations fail permanently, `40001`/`40P01`
   retry the whole transaction, `53300`/`08006` back off and retry, schema errors page on-call.
3. **Design transaction boundaries** so atomicity, rollback, savepoints, and retries are explicit
   — including the cases where the outcome of `COMMIT` is unknown.
4. **Prevent duplicate side effects** with idempotency keys, unique constraints, and the
   **transactional outbox** instead of hope.
5. **Keep persistence errors out of the domain and the API**: the repository translates once,
   preserves the cause, and never leaks SQL or constraint names.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 22 | [Database Error Classification](./22-database-error-classification/README.md) | Connection, constraint, lock, failover, schema, corruption — and stable app translation |
| 23 | [Transaction and Rollback Error Handling](./23-transaction-and-rollback-error-handling/README.md) | Boundaries, commit/rollback failure, retries, ambiguous outcomes, outbox, compensation |
| 24 | [Repository and Data Access Error Handling](./24-repository-and-data-access-error-handling/README.md) | What the repository owns, CRUD/bulk semantics, leak prevention, read-after-write |

## How to study this part

- Start with Chapter 22's concepts, then memorize the SQLSTATE cheat sheet in
  [`22-database-error-classification/05-reference/README.md`](./22-database-error-classification/05-reference/README.md).
- Chapter 23 only makes sense if you accept one uncomfortable fact first: **`COMMIT` can fail
  after it succeeded.** Read the ambiguous-outcome deep dive before the retry code.
- Chapter 24 is where most codebases leak. Audit one repository module against its dos and
  don'ts before moving on.

## Key takeaways

- **Classification lives at the persistence boundary.** Exactly one layer reads `SQLSTATE` or
  a MySQL error number; everything downstream sees your application's error codes.
- **Retry is a property of the error class, not of the operation.** `23505` never retries;
  `40001` always retries *the whole transaction* with fresh reads.
- **A transaction is the smallest unit you can honestly promise to roll back.** Anything
  outside it (Stripe calls, S3 writes, emails) needs compensation or an outbox.
- **Unknown commit outcome is a first-class state**, not an edge case to ignore. Design for
  `08007`-style resolution instead of hoping TCP delivers.
- **Repositories translate, they do not decide.** They preserve cause and retry class; the
  service decides retry; the API boundary decides what the client sees.

## Related

- [Part VI — Error Boundaries and Translation](../part-06-boundaries-and-translation/README.md)
- [Part XI — Retry Logic and Resilience](../part-11-retry-and-resilience/README.md)
- [Glossary](../GLOSSARY.md)
