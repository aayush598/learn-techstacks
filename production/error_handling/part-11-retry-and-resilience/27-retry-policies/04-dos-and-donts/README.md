# Chapter 27 — Do's and Don'ts

> Part XI · Chapter 27 · All sections

A condensed rule set distilled from the chapter. Use it as a retry-policy review checklist.

## Eligibility

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Retry only classified-transient errors | Retry everything in a `catch` |
| Default unknown errors to terminal | Default unknown errors to retryable |
| Classify at the translation boundary | Parse error messages to decide |
| Carry `Retry-After` into `retryAfterMs` | Recompute a delay the server gave you |
| Treat side effects as conditional | Retry `POST` because "it usually works" |

## Attempts and backoff

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Count the first try in `maxAttempts` | Define attempts differently per service |
| Cap exponential backoff | Let delay grow unbounded |
| Use full jitter by default | Use fixed delays across a fleet |
| Sleep only if another attempt can run | Sleep after the final attempt |
| Inject clock/RNG/sleep for tests | Depend on real time in unit tests |

## Budgets and deadlines

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Derive deadlines from the caller | Invent a 30s budget at each layer |
| Clamp per-attempt timeout to remaining time | Use a timeout longer than the deadline |
| Budget retries per dependency | Share one global budget |
| Stop when the next attempt cannot fit | Sleep until the deadline, then fail |
| Propagate deadlines downstream | Reset the budget at each hop |

## Amplification and ownership

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Compute the attempt product across layers | Reason about one loop in isolation |
| Name exactly one retry owner per dependency | Let gateway, service, and SDK all retry |
| Disable SDK/client retries explicitly | Assume retries are off by default |
| Count queue redelivery as a layer | Treat the queue as retry-free |
| Include fan-out in load math | Forget parallel calls |

## Exhaustion and failure

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Preserve the last cause and attempt count | Throw a fresh `"failed"` error |
| Return a meaningful terminal code | Collapse everything to `500` |
| State when outcome is unknown | Report "failed" for a maybe-succeeded payment |
| Emit one metric per outcome | Log only the final attempt |
| Alert on retry exhaustion rates | Ignore growing exhaustion |

## By dependency

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Retry the whole DB transaction | Retry a statement in an aborted tx |
| Keep DB backoff short (10–50ms base) | Hold a connection for seconds |
| Reuse one provider idempotency key | Generate a key per attempt |
| Honor `Retry-After` for `429`/`503` | Retry early |
| Checkpoint job progress | Restart long jobs from zero |
| Send exhausted jobs to a monitored DLQ | Retry forever |

## Anti-patterns in the wild

1. **The Optimist** — retries every exception "just in case."
2. **The Metronome** — fixed-delay retries that synchronize the fleet.
3. **The Unbounded** — `while (true)` with a sleep and no deadline.
4. **The Multiplier** — SDK + service + gateway retries, invisibly.
5. **The Amnesiac** — exhaustion throws a new error with no cause.
6. **The Double Charger** — retries unkeyed payments after timeouts.
7. **The Transaction Retrier** — retries a statement in an aborted transaction.

## Chapter checklist

- [ ] Every retry has an explicit retryability predicate.
- [ ] Attempts, budget, and deadline are all bounded.
- [ ] Backoff is exponential, capped, and jittered.
- [ ] `Retry-After` overrides computed delay.
- [ ] One retry owner per dependency is documented.
- [ ] Side effects are keyed or reconciled, never retried blind.
- [ ] Exhaustion preserves cause, attempts, and elapsed time.
- [ ] DB, provider, and job retries use their correct safe unit.

## Related

- [Chapter 27 Reference](../05-reference/README.md)
- [Why Retry — and When It Is Dangerous](../01-concepts/01-why-retry-and-when-it-is-dangerous.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../28-idempotency-and-duplicate-operation-safety/README.md)
- [Part XVII — Error-Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
