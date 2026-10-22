# Chapter 22 — Reference

> Part IX · Chapter 22 · SQLSTATE cheat sheet, MySQL codes, decision table, glossary.

## Cheat sheet — the five classes that matter

```text
08  connection      transient   → 503, backoff, maybe page if sustained
23  constraint      permanent   → 409/422, translate, never retry
40  concurrency     transient   → retry WHOLE transaction, 409 after exhaustion
42  schema/access   permanent   → 500, PAGE, deploy fault
XX  corruption      permanent   → 503, fail closed, PAGE
53  capacity        transient   → 503 + shed load, shrink pools
57  timeout/op      transient   → 504/503, retry selectively
```

## SQLSTATE cheat sheet (Postgres)

| Code | Name | Class | Retry | HTTP | Alert |
| ---- | ---- | ----- | ----- | ---- | ----- |
| `08001` | unable to establish connection | 08 | no (config) | 500 | yes |
| `08003` | connection does not exist | 08 | yes | 503 | no |
| `08006` | connection failure | 08 | yes | 503 | sustained |
| `08007` | transaction resolution unknown | 08 | **read-back** | 503 | no |
| `22001` | string data right truncation | 22 | no | 422 | no |
| `22003` | numeric value out of range | 22 | no | 422 | no |
| `22P02` | invalid text representation | 22 | no | 422 | no |
| `23502` | not-null violation | 23 | no | 422 | if pre-validated |
| `23503` | foreign-key violation | 23 | no | 422/409 | no |
| `23505` | unique violation | 23 | no | 409 | no |
| `23514` | check violation | 23 | no | 422 | no |
| `23P01` | exclusion violation | 23 | no | 409 | no |
| `25006` | read-only SQL transaction | 25 | routing | 503 | no |
| `25P02` | in failed SQL transaction | 25 | no (bug) | 500 | yes |
| `25P03` | idle-in-transaction timeout | 25 | no (bug) | 500 | yes |
| `28000` | invalid authorization | 28 | no | 500 | yes |
| `28P01` | invalid password | 28 | no | 500 | yes |
| `3D000` | invalid catalog name | 3D | no | 500 | yes |
| `3F000` | invalid schema name | 3F | no | 500 | yes |
| `40001` | serialization failure | 40 | **yes, whole txn** | 409/503 | no |
| `40P01` | deadlock detected | 40 | **yes, whole txn** | 409/503 | no |
| `42501` | insufficient privilege | 42 | no | 500 | yes |
| `42601` | syntax error | 42 | no | 500 | yes |
| `42703` | undefined column | 42 | no | 500 | yes |
| `42P01` | undefined table | 42 | no | 500 | yes |
| `53100` | disk full | 53 | no | 503 | yes |
| `53200` | out of memory | 53 | yes | 503 | yes |
| `53300` | too many connections | 53 | yes + shed | 503 | sustained |
| `54001` | statement too complex | 54 | no | 500 | yes |
| `55P03` | lock not available (`lock_timeout`) | 55 | yes | 409/503 | no |
| `57014` | query canceled (`statement_timeout`) | 57 | selective | 504 | no |
| `57P01` | admin shutdown | 57 | yes | 503 | no |
| `57P03` | cannot connect now | 57 | yes | 503 | no |
| `58000` | system error | 58 | no | 503 | yes |
| `58P01` | disk error (I/O) | 58 | no | 503 | yes |
| `XX000` | internal error | XX | no | 503 | yes |
| `XX001` | data corrupted | XX | no | 503 | **yes** |
| `XX002` | index corrupted | XX | no | 503 | **yes** |

## MySQL error numbers

| errno | SQLSTATE | Meaning | Retry |
| ----- | -------- | ------- | ----- |
| `1040` | `08004` | too many connections | yes + shed |
| `1045` | `28000` | access denied | no, page |
| `1048` | `23000` | column cannot be null | no |
| `1054` | `42S22` | unknown column | no, page |
| `1062` | `23000` | duplicate entry | no |
| `1064` | `42000` | syntax error | no, page |
| `1142` | `42000` | command denied | no, page |
| `1146` | `42S02` | table doesn't exist | no, page |
| `1205` | `HY000` | lock wait timeout | yes (statement) |
| `1213` | `40001` | deadlock | **yes, whole txn** |
| `1290` | `HY000` | read-only server | routing |
| `1451` | `23000` | row is referenced | no |
| `1452` | `23000` | no referenced row | no |
| `2006` | `HY000` | server has gone away | yes |
| `2013` | `HY000` | lost connection during query | yes (ambiguous for writes) |
| `3024` | `HY000` | query timeout | selective |
| `3819` | `HY000` | check constraint violated | no |

## Decision table — what do I do right now?

| Observed | Class | Action |
| -------- | ----- | ------ |
| duplicate email on signup | `23505` | `409`, show field, no retry |
| duplicate webhook event id | `23505` on dedupe table | `200`, already processed |
| deleted parent referenced | `23503` | `422`/`404`, refresh client |
| negative budget | `23514` | `422`, no retry |
| two writers conflict | `40001`/`40P01` | retry whole txn, fresh read |
| `UPDATE` blocked 2 s | `55P03`/`1205` | retry txn / fix lock order |
| query hit 3 s budget | `57014` | `504`, add index, don't blind-retry |
| pool wait timed out | *(no SQLSTATE)* | `503`, fix pool sizing |
| server full | `53300`/`1040` | `503` + `Retry-After`, shed load |
| connections dropped | `08006`/`2013` | retry, check ambiguity for writes |
| commit ack lost | `08007` | read back, don't blind-retry |
| table missing after deploy | `42P01`/`1146` | `500`, **page**, roll back deploy |
| bad page/checksum | `XX001` | fail closed, **page**, restore |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **SQLSTATE** | Five-character standard error code; first two chars are the class |
| **Class** | Coarse category (`08`, `23`, `40`, `42`, …) used to pick policy |
| **Constraint identity** | Server-side name of the index/constraint that fired |
| **Pool exhaustion** | Client-side wait for a free connection; no SQLSTATE |
| **Serialization failure** | `40001`; concurrent transactions not serializable; retry all |
| **Ambiguous outcome** | Commit may or may not have applied (`08007`) |
| **Transient** | Worth retrying with backoff |
| **Alert** | Failure requires a human/on-call, not a client action |

## Signposts

- Classification mechanics → [SQLSTATE Classification Table](../02-deep-dive/01-sqlstate-classification-table.md)
- Driver fields → [Driver and Vendor Error Shapes](../02-deep-dive/02-driver-and-vendor-error-shapes.md)
- Transaction retries → [Chapter 23](../../23-transaction-and-rollback-error-handling/README.md)
- Repository translation → [Chapter 24](../../24-repository-and-data-access-error-handling/README.md)

## Related

- [Chapter 22 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Part IX Index](../../README.md)
- [Glossary](../../../GLOSSARY.md)
