# Chapter 23 — Reference

> Part IX · Chapter 23 · Transaction failure guide, retry table, outbox checklist.

## Transaction failure guide

```text
Error while …            Meaning                         Action
─────────────────────────────────────────────────────────────────────────────
BEGIN / statement         normal failure                  rollback → translate
COMMIT → constraint       definitely not committed        rollback → 409/422
COMMIT → 08006/08007      UNKNOWN                         read marker on primary
COMMIT → disk full        UNKNOWN / failed                fail, page, reconcile
ROLLBACK                  broken connection               close conn, don't reuse
SAVEPOINT rollback        txn can continue                record item, proceed
```

## What each error tells you

| Observation | Can you retry? | Scope | Notes |
| ----------- | -------------- | ----- | ----- |
| `23505` / `1062` | **no** | — | duplicate; dedupe or `409` |
| `23503` / `1452` | no | — | missing parent |
| `23502` / `1048` | no | — | missing required field |
| `23514` / `3819` | no | — | business rule |
| `40001` | yes | whole txn | serialization |
| `40P01` / `1213` | yes | whole txn | deadlock |
| `55P03` / `1205` | yes | whole txn | lock timeout |
| `57014` / `3024` | selective | statement | reduce work first |
| `08006` / `2013` during `COMMIT` | **resolve first** | — | ambiguous |
| `08006` elsewhere | yes | whole txn | reconnect |
| `53300` / `1040` | yes + shed | whole txn | capacity |
| `42P01` / `1146` | no | — | schema; page |
| `XX001` | no | — | corruption; fail closed |

## Retry decision table

| Question | If no |
| -------- | ----- |
| Is the error class transient? | Translate and return |
| Is the retry scope the whole transaction? | Don't retry |
| Is the operation idempotent or keyed? | Make it so first |
| Attempts remaining? | Return an exhausted error |
| Is the commit outcome known? | Resolve before retrying |

## Commit outcome matrix

| Client sees | Server state | Correct handling |
| ----------- | ------------ | ---------------- |
| `COMMIT` OK | committed | success |
| constraint error at commit | not committed | `409`/`422` |
| socket reset during `COMMIT` | **unknown** | read marker |
| `08007` | **unknown** | read marker |
| client deadline during `COMMIT` | **unknown** | read marker |
| process crash after commit | committed | reconcile on startup |
| `ROLLBACK` fails | server resolves on disconnect | close connection |

## Idempotency checklist

- [ ] Key is supplied by the client or derived from a stable operation id.
- [ ] Key row and business effect commit **atomically**.
- [ ] Key reuse with a different payload returns `409`.
- [ ] Completed response is stored for replay.
- [ ] `in_progress` has a timeout and a resolver.
- [ ] Records expire (24 h–7 days) and are purged.
- [ ] Unknown commits resolve by reading the key from the **primary**.

## Outbox checklist

- [ ] Outbox insert is in the same transaction as the business change.
- [ ] `event_id` is stable and sent to consumers.
- [ ] Relay uses `FOR UPDATE SKIP LOCKED`.
- [ ] Publish happens **before** marking `published_at`.
- [ ] Failures back off and move to a DLQ after N attempts.
- [ ] Consumers dedupe on `event_id`.
- [ ] Published rows are archived/purged.
- [ ] Ordering is per `aggregate_id`, not global.

## Isolation cheat sheet

| Level | Prevents | Allows | `40001` risk |
| ----- | -------- | ------ | ------------ |
| `READ COMMITTED` (PG default) | dirty reads | non-repeatable reads, write skew | low |
| `REPEATABLE READ` | non-repeatable reads | write skew (PG), phantom (MySQL) | medium |
| `SERIALIZABLE` | all of the above | — | **higher** |

| Lock clause | Effect | Use |
| ----------- | ------ | --- |
| `FOR UPDATE` | exclusive row lock | read-modify-write |
| `FOR NO KEY UPDATE` | weaker, no FK block | high concurrency (PG) |
| `FOR SHARE` | shared lock | stable reference reads |
| `FOR UPDATE SKIP LOCKED` | skip busy rows | queue/outbox relay |
| `FOR UPDATE NOWAIT` | fail if locked | latency-sensitive paths |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **Boundary** | Line where a unit of work begins/commits |
| **Ambiguous outcome** | Commit may or may not have applied |
| **Idempotency key** | Stable token collapsing duplicate attempts |
| **Savepoint** | Named point for partial rollback inside a txn |
| **Compensation** | Business-level undo of a committed step |
| **Outbox** | Table holding events to publish after commit |
| **Transactional outbox** | Business change + event in one transaction |
| **At-least-once** | Delivery guarantee requiring consumer dedupe |
| **In-doubt transaction** | Prepared 2PC transaction awaiting resolution |

## Signposts

- Ambiguity mechanics → [Ambiguous Commit Outcomes](../02-deep-dive/01-ambiguous-commit-outcomes.md)
- Outbox design → [Outbox Mechanics](../02-deep-dive/02-outbox-mechanics-and-cross-store-consistency.md)
- Retry code → [Retrying 40001 and 40P01](../03-practical-examples/01-retrying-40001-and-40p01.md)
- Repository translation → [Chapter 24](../../24-repository-and-data-access-error-handling/README.md)

## Related

- [Chapter 23 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Part IX Index](../../README.md)
- [Glossary](../../../GLOSSARY.md)
