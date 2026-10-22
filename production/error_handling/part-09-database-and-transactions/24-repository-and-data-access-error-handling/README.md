# Chapter 24 — Repository and Data Access Error Handling

> Part IX · _Estimated reading time: 70–95 min_
> **Prerequisite:** [Chapter 23 — Transaction and Rollback Error Handling](../23-transaction-and-rollback-error-handling/README.md)

## One-sentence summary

A repository's job is **not to hide errors but to translate them**: it turns persistence
dialects into application errors, distinguishes "no row" from "query failed", and never lets
SQL, constraint names, or driver types escape into the domain.

## Why this chapter matters

The repository is the most common place for two opposite mistakes. One team leaks everything:
`SQLAlchemyError`, `pgcode`, and table names travel through services into API responses. The
other hides everything: every failure becomes `RepositoryError("database error")`, so a duplicate
email, a stale update, and a dead connection are indistinguishable and the service cannot choose
retry, `409`, or `503`. Both make correct error handling impossible. This chapter draws the line:
**translate, preserve metadata, and expose intent — not implementation.**

## Chapter map

The chapter has 15 sections. They are grouped into these files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-repository-responsibilities-and-domain-boundary.md`](./01-concepts/01-repository-responsibilities-and-domain-boundary.md) | 24.1, 24.2, 24.11 | What the repository owns, repo vs domain errors, preventing leakage |
| [`01-concepts/02-mapping-persistence-to-application-errors.md`](./01-concepts/02-mapping-persistence-to-application-errors.md) | 24.3, 24.12, 24.13 | Mapping rules, why generic repo errors hurt, preserving failure metadata |
| [`01-concepts/03-crud-failure-semantics.md`](./01-concepts/03-crud-failure-semantics.md) | 24.4–24.8 | Missing records, missing vs failed, duplicate inserts, failed updates/deletes |
| [`01-concepts/04-bulk-operations-and-partial-success.md`](./01-concepts/04-bulk-operations-and-partial-success.md) | 24.9, 24.10 | Bulk failure modes and representing partial success |
| [`01-concepts/05-read-after-write-and-consistency-guarantees.md`](./01-concepts/05-read-after-write-and-consistency-guarantees.md) | 24.14, 24.15 | Read-your-writes, replica lag, stated consistency guarantees |
| [`02-deep-dive/01-leak-prevention-and-metadata-preservation.md`](./02-deep-dive/01-leak-prevention-and-metadata-preservation.md) | 24.11–24.13 | The leak paths, the metadata every repo error must carry |
| [`02-deep-dive/02-read-after-write-and-consistency-mechanics.md`](./02-deep-dive/02-read-after-write-and-consistency-mechanics.md) | 24.14, 24.15 | Session stickiness, `RETURNING`, lag budgets, consistency contracts |
| [`03-practical-examples/01-repository-translating-persistence-errors.md`](./03-practical-examples/01-repository-translating-persistence-errors.md) | 24.1–24.8 | A TypeScript repository that translates every CRUD failure |
| [`03-practical-examples/02-bulk-partial-success-with-cast.md`](./03-practical-examples/02-bulk-partial-success-with-cast.md) | 24.9, 24.10, 24.14 | `ExportJob` bulk insert with per-row results and read-back |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Repository rules, anti-patterns, review checks |
| [`05-reference/README.md`](./05-reference/README.md) | all | Repository error contract, CRUD decision table, leak checklist |

## Learning objectives

By the end you can:

- State exactly what a repository owns — and what belongs to the service or the domain.
- Choose between returning `null`, throwing `NotFound`, and treating a missing row as success.
- Translate persistence errors **once**, preserving `cause`, retry class, and safe metadata.
- Represent **bulk partial success** without lying about the result.
- Explain and implement **read-after-write** consistency when replicas are in the path.

## Key takeaways

1. **`null` is a result, not an error.** "No row" is only an error when the caller required one.
2. **Zero rows affected is data, not an exception** — and usually means a conflict, not "not found".
3. **One error shape per repository**, with stable codes and preserved `cause`.
4. **Bulk operations return per-item outcomes**; a single boolean is always wrong for a batch.
5. **Read-your-writes is a routing decision**, not a wish — return the written row or read the
   primary.
6. **No driver type, SQL text, or constraint name escapes the repository.**

## Exercises

1. Read one repository in your codebase and list every distinct exception it can throw.
2. Classify each as: no-row, conflict, validation, transient, or internal.
3. Change one `update()` to return the affected-row count and map `0` to a conflict.
4. Add per-item results to one bulk endpoint and remove the aggregate boolean.
5. Write a test that writes then immediately reads through a lagging replica; make it pass.

## Related

- [Chapter 22 — Database Error Classification](../22-database-error-classification/README.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../23-transaction-and-rollback-error-handling/README.md)
- [Layered Error-Handling Architecture (Ch. 9)](../../part-04-architecture/09-layered-error-handling-architecture/README.md)
- [Domain and Business Logic Errors (Ch. 18)](../../part-07-validation-and-business-errors/18-domain-and-business-logic-errors/README.md)
