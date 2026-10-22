# Retry Classification and Eligibility

> Part XI · Chapter 27 · Sections 27.4, 27.5, 27.24 · _Estimated reading time: 18 min_
> **Prerequisite:** [Why Retry — and When It Is Dangerous](./01-why-retry-and-when-it-is-dangerous.md)

## In one sentence

**Retry eligibility is a deterministic function of the error and the operation** — not a guess made
inside a `catch` block — and it must be computed once, carried on the error, and enforced at the one
layer that owns the retry.

## Why this matters in production

Every retry bug starts with an implicit classification. A developer sees a timeout and adds a retry;
six months later the same handler retries `422`s, `401`s, and business declines because the predicate
was never written down. Classification gives you a **single table** that retry engines, dashboards,
and API responses all read. It also prevents the most expensive class of bug: retrying an operation
whose first attempt already succeeded.

## 27.4 — Retryable vs not retryable

Retryability is a property with three values, not two:

| Class | Meaning | Retry? |
| ----- | ------- | ------ |
| **Retryable** | Transient; expected to succeed later without changes | Yes, with backoff |
| **Retryable-with-preconditions** | Safe only if idempotent/keyed, or after refresh/rollback | Conditional |
| **Non-retryable** | Will fail identically (validation, auth, business, schema) | No |

### The classification table

| Error | Class | Why |
| ----- | ----- | --- |
| HTTP `408`, `429`, `502`, `503`, `504` | Retryable | Transient transport/overload |
| HTTP `500` from a provider | Usually retryable | Provider bug or transient fault |
| HTTP `400`, `401`, `403`, `404`, `422` | Non-retryable | Input/identity/permission |
| HTTP `409` | Conditional | Conflict may need refresh first |
| Postgres `40001`, `40P01` | Retryable (after rollback) | Serialization/deadlock |
| Postgres `08xxx`, `53300` | Retryable | Connection/pool exhaustion |
| Postgres `23505`, `23503`, `23514` | Non-retryable | Constraint/business |
| Postgres `42xxx` | Non-retryable | Schema/deploy fault — alert |
| `ECONNRESET`, `ECONNREFUSED`, `ETIMEDOUT` | Retryable | Network |
| TLS certificate error | Non-retryable | Misconfiguration |
| `ENOENT`, `EACCES` | Non-retryable | Missing/forbidden resource |
| Provider `card_declined` | Non-retryable | Business decision |
| Provider `context_length_exceeded` | Non-retryable | Input too large |
| `CancellationError` / deadline exceeded | Non-retryable | Caller gave up |

## 27.5 — Classification for retry

Classification belongs at the **translation boundary** (Chapter 16), not at the retry call site. The
normalized error must carry the decision:

```ts
type RetryClass = "retryable" | "conditional" | "terminal";

interface AppError {
  code: string;
  retryClass: RetryClass;
  retryAfterMs?: number;   // from Retry-After or provider hint
  transient: boolean;      // convenience alias (retryClass === "retryable")
  attempt?: number;        // set by the retry engine
  cause?: unknown;
}
```

```python
RETRYABLE_SQLSTATES = {"40001", "40P01", "08006", "08003", "53300"}
RETRYABLE_HTTP = {408, 429, 502, 503, 504}

def classify(err) -> str:
    if isinstance(err, ValidationError) or isinstance(err, AuthError):
        return "terminal"
    if (code := getattr(err, "pgcode", None)) in RETRYABLE_SQLSTATES:
        return "retryable"
    if (status := getattr(err, "status", None)) in RETRYABLE_HTTP:
        return "retryable"
    if isinstance(err, (ConnectionError, TimeoutError)):
        return "retryable"
    if isinstance(err, ConflictError):
        return "conditional"
    return "terminal"   # safe default: do not retry unknown errors
```

**Default unknown errors to terminal.** Retrying an unknown failure is a bet with no information;
it can amplify a bug and delay the user-facing error by seconds.

### Why not derive retryability from the message?

Messages change, are localized, and leak vendor wording. A code/status/class is stable. If you must
parse a vendor payload, do it once in the adapter (Chapter 25) and emit a stable code.

## 27.24 — Side-effect retries

Side effects change the analysis. The question is not only "will this succeed later?" but "what
happens if the first attempt already succeeded?"

| Operation | Retry rule |
| --------- | ---------- |
| `GET`, `HEAD` | Safe to retry |
| `PUT` with full state | Idempotent by definition; safe |
| `DELETE` | Usually idempotent (`404` on second call is acceptable) |
| `POST` create | **Not safe** without an idempotency key |
| `POST` charge/refund | **Not safe** without a key; verify status first |
| `PATCH` increment (`count = count + 1`) | **Not safe**; use absolute values or versions |
| Sending email/SMS | **Not safe**; dedupe by message id |
| Queue publish | Needs a dedup key or transactional outbox |

The rule:

```text
side_effect_retry_allowed = idempotent(op) OR has_stable_idempotency_key(op)
```

If neither holds, the correct action after an ambiguous failure is **reconciliation** (query the
provider for the result), not another blind attempt. Chapter 28 covers the mechanics.

### Retrying after a transaction failure

A failed statement inside a Postgres transaction leaves the transaction **aborted**. You cannot
simply retry the statement; you must roll back and retry the **whole transaction** (Chapter 23).

```python
for attempt in range(3):
    try:
        with db.transaction():
            repo.insert(order)
            repo.decrement_stock(sku)
        break
    except SerializationFailure:
        if attempt == 2:
            raise
        time.sleep(backoff(attempt))
```

## Worked example

```go
func isRetryable(err error, op Operation) bool {
    var appErr *AppError
    if !errors.As(err, &appErr) {
        return false // unknown → terminal
    }
    switch appErr.RetryClass {
    case Retryable:
        return true
    case Conditional:
        return op.Idempotent || op.IdempotencyKey != ""
    default:
        return false
    }
}
```

The retry engine never inspects `err.Error()` or a vendor type; it reads the classification carried
on the error, plus one fact about the operation.

## Key data / numbers

- Retryable HTTP: `408`, `429`, `500` (provider), `502`, `503`, `504`.
- Retryable Postgres: `40001`, `40P01`, `08xxx`, `53300`.
- Non-retryable Postgres: `23xxx`, `42xxx`.
- `Retry-After` may be seconds (`Retry-After: 120`) or an HTTP date.
- Safe methods: `GET`, `HEAD`, `OPTIONS`, `TRACE`; idempotent: `PUT`, `DELETE`.
- Common retry key TTL: **24 hours** (see Chapter 28).

## Real-world use case — AgentRun

`AgentRun` called an LLM provider that returned `429` on bursty traffic and `400
context_length_exceeded` when a conversation grew too long. The first implementation retried both,
which turned a permanent token-limit error into six failed calls and a 30-second delay. After
classification, `429` carried `retryAfterMs` from the provider header and was retried; the
`context_length_exceeded` error was terminal and triggered conversation truncation instead. Latency
for oversized prompts dropped from 30s to under 200ms, and provider quota usage fell accordingly.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Boolean `isRetryable` | Simple | Cannot express conditional cases | Read-only calls |
| Three-state class | Handles side effects | Slightly more code | Default |
| Per-error retry hint | Precise, provider-aware | Must be maintained | Provider adapters |
| Message parsing | No schema change | Brittle, localizable | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify at the translation boundary | Classify inside every `catch` |
| Default unknown → terminal | Default unknown → retryable |
| Treat side effects as conditional | Retry `POST` because it "usually works" |
| Roll back before retrying a transaction | Retry a statement in an aborted transaction |
| Carry `retryAfterMs` from the provider | Recompute a delay the server already told you |

## Common mistakes

- **Two sources of truth.** Retryability set in one place and overridden in another.
- **Retrying `409` without refreshing.** The same conflict recurs forever.
- **Treating `500` as always retryable.** A deterministic provider bug will burn your budget.
- **Ignoring `CancellationError`.** Retrying after the caller gave up delays shutdown.
- **Retrying an SDK call that already retried internally**, doubling attempts silently.

## Checklist

- [ ] Every error has a `retryClass` assigned at translation.
- [ ] The retry predicate reads the class, not the message.
- [ ] Unknown errors default to terminal.
- [ ] Side-effecting operations require a key or reconciliation.
- [ ] Transactions are rolled back before retry.
- [ ] `Retry-After` and provider hints are preserved.

## Related

- [Attempts, Delays, and Jitter](./03-attempts-delays-and-jitter.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../28-idempotency-and-duplicate-operation-safety/README.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
- [Retry vs Fail Decision Guide](../05-reference/README.md)
