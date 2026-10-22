# Chapter 9 — Do's and Don'ts

> Part IV · Chapter 9 · All sections 9.1–9.20

A condensed rule set for layered error handling. Use it as a review checklist.

## Layer ownership

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give each layer exactly one error job (detect / translate / decide / render) | Let two layers decide the same error |
| Treat workers, schedulers, bootstrap, and the process as real layers | Assume the HTTP rules cover async paths |
| Route workers through the same application service as HTTP | Re-implement business logic in the worker |

## Handle, translate, propagate

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Handle where the outcome is decided (application, worker, transport-for-shape) | Handle in the controller *and* the service |
| Translate once per boundary crossed, preserving `cause` | Translate the same error twice in a row |
| Propagate when you cannot name a new outcome | `catch` only to log and rethrow |
| Retry in exactly one layer per operation | Retry in controller + service (3 × 3 amplification) |

## Leakage

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Translate driver/vendor errors at their boundary (T1/T2) | Let `SQLSTATE` or Stripe types reach the domain or a response |
| Lint import boundaries (no `pg`/`stripe` in domain code) | Trust review alone to catch leaks |
| Give every wrapper failure a distinct stable code | Collapse failures into `Error("failed")` |
| Keep `cause` for logs; sanitize only what users see | Delete classification to "be safe" |

## Async and process layers

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Cap job attempts (recommendation: 5) and DLQ terminal codes | Retry every failure until "it works" |
| Guard scheduled runs against overlap; record `SKIPPED_OVERLAP` | Assume the previous run finished |
| Validate config/deps at bootstrap; exit non-zero on failure | Serve traffic half-wired |
| Terminate on `uncaughtException`; drain on `SIGTERM` | Continue after an uncaught exception |

## Consistency

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep a handle-once ledger: one handling layer per code | Let conventions be tribal knowledge |
| Assert the same code for HTTP and queue entry points | Let workers and APIs drift |
| Render per protocol only after the decision | Let renderers re-classify errors |

## Anti-patterns in the wild

1. **The Leaky Repository** — driver error rethrown verbatim; schema reaches clients.
2. **The Erasing Wrapper** — `catch { throw new Error("db error") }`; classification dies.
3. **The Two-Headed Retry** — controller and service both retry; side effects duplicate.
4. **The Controller Oracle** — HTTP layer inspects vendor/SDK internals to decide policy.
5. **The Hopeful Worker** — `catch (e) { queue.retry(msg) }`; poison jobs stall the queue.
6. **The Half-Wired Boot** — service accepts traffic before config/DB validation.
7. **The Immortal Process** — `uncaughtException` logged and swallowed; state stays corrupt.

## Chapter checklist

- [ ] Every layer in the request path has a documented error job.
- [ ] Translation points T1–T6 exist as named, tested functions.
- [ ] One retry owner per operation; counts live in one module.
- [ ] Job types have retryable/terminal verdicts and a DLQ.
- [ ] Bootstrap fails fast; process handlers terminate, not continue.
- [ ] The same fault produces the same code via HTTP and via the queue.
- [ ] No domain file imports an infrastructure library (enforced in CI).

## Related

- [Chapter 9 Reference](../05-reference/README.md)
- [Chapter 15 — Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- [Chapter 46 — Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
