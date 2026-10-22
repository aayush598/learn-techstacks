# Structure, Separation, and Responsibility

> Part I · Chapter 2 · Sections 2.4, 2.5, 2.6, 2.19, 2.20 · _Estimated reading time: 24 min_

## In one sentence

Keep **business logic separate from error policy**, centralize the **rules** while leaving the
**decisions** local, give each handler **one responsibility**, and use that structure to drive down
**boilerplate** and **maintenance cost**.

## Why this matters in production

When business logic and error handling are tangled, three things happen: the domain becomes
unreadable (you cannot see the rule for the `try/catch`), the policy drifts (every handler invents
its own mapping), and change becomes expensive (touching one means touching the other).

The goal is not "no error handling in the domain" — the domain must express its failures. The goal
is: the domain *names* failures; a small number of boundary components *decide what to do* about
them.

## Core concept — five principles

### 2.4 Separation of business logic and error handling

Business logic answers **"is this allowed?"** Error handling answers **"what do we do when it
isn't?"** Keep the first in the domain, the second at boundaries.

```ts
// ✅ Domain names the failure; it does not decide the HTTP response.
function withdraw(account: Account, amount: Money): Account {
  if (account.balance.lt(amount)) {
    throw new InsufficientFunds({ accountId: account.id, shortfall: amount.minus(account.balance) });
  }
  return account.debit(amount);
}
```

The domain does not know about `402`, retries, or JSON. Those live at the edge.

### 2.5 Centralized policy vs decentralized decisions

There are two different things people conflate:

| Thing | Where it lives | Example |
| ----- | -------------- | ------- |
| **Policy** (rules, invariant) | Central | "validation errors → 422, never retried" |
| **Decision** (context-specific choice) | Local | "this optional widget degrades instead of failing" |

> **Centralize policy; decentralize decisions.** A single policy table (Chapter 8/20) prevents
> drift. Local decisions preserve the context only the caller has.

The anti-pattern is centralizing *decisions* (a giant `switch` in one middleware that guesses what
every caller wanted) or decentralizing *policy* (every service maps `409` differently).

### 2.6 Single responsibility in error handling

Each error-handling component does exactly one job:

| Component | Responsibility | Not responsible for |
| --------- | -------------- | ------------------- |
| Validator | Detect invalid input | Decide HTTP status |
| Domain | State the rule violation | Retry, log, translate |
| Translator | Map native → app error | Recover |
| Global handler | Convert app error → response | Business rules |
| Retry policy | Classify retryable | Compensation |

When one component does several, the others become inconsistent and untestable.

### 2.19 Minimize boilerplate

Every line of repetitive error plumbing is a line that can drift and a line reviewers stop reading.
Reduce it with **shared primitives**, not with a framework:

- One `DomainError` base carrying `code`, `httpStatus`, `retryable`.
- One decorator/wrapper for the "catch-log-rethrow at the boundary" pattern (Chapters 12, 46).
- One registry-driven mapping instead of N `if` chains.

Boilerplate reduction must not hide control flow (see Chapter 53). If a reader cannot tell what
happens on failure, you removed too much.

### 2.20 Optimize for maintainability

The people who maintain the code are not the people who wrote it. Maintainability means:

1. **Locate decisions fast** — a new error needs one registry entry, not edits in ten files.
2. **Change safely** — adding a category does not require touching every handler.
3. **Read the happy path** — error handling does not drown the feature.

## How it works (mechanics)

A maintainable structure separates the *rule* from the *mechanism*:

```text
  ┌─────────── Domain ───────────┐
  │ rule: balance >= amount      │  throws InsufficientFunds
  └───────────────┬──────────────┘
                  ▼
  ┌─────── Translator ───────────┐
  │ InsufficientFunds → AppError │  code, category, retryable=false
  └───────────────┬──────────────┘
                  ▼
  ┌──── Global Handler ──────────┐
  │ AppError → HTTP 402 + body   │  one place, registry-driven
  └──────────────────────────────┘
```

Each box has one responsibility. Adding a new business rule touches the domain and the registry —
not the handler.

## Worked example

**Acme SaaS** `Checkout`. Before: business logic interleaved with retries and HTTP codes.

```python
# ❌ Business rule, retry, and HTTP status all in one place.
def charge(order):
    try:
        result = stripe.charge(order.amount, idempotency_key=order.id)
    except stripe.error.CardError as e:
        if e.code == "card_declined":
            return {"status": 402, "msg": "card declined"}   # policy in the wrong layer
        raise
    except stripe.error.RateLimitError:
        time.sleep(2)
        return charge(order)                                  # recursive retry, no budget
    if not result.paid:
        return {"status": 200, "ok": False}                   # failure as success
    return {"status": 200, "ok": True}
```

After: the domain states outcomes; one policy decides representation; retries live in the client.

```python
# ✅ Domain outcomes (results), policy centralized, retry in the adapter.
def settle(order) -> Result[Payment, PaymentError]:
    outcome = gateway.charge(order.amount, idempotency_key=order.id)  # adapter handles retry/backoff
    if outcome.declined:
        return Err(PaymentDeclined(reason=outcome.reason))   # non-retryable, → 402
    return Ok(Payment(id=outcome.id))
# HTTP representation for PaymentDeclined is defined ONCE in the error registry.
```

## Key data / numbers

| Item | Value | Why |
| ---- | ----- | --- |
| Payment required | `402 Payment Required` | Declined card mapping (commonly used for this) |
| Session-expired auth | `401` | Credential problem, not permission |
| Permission denied | `403` | Authenticated but not allowed |
| Idempotency key scope | Per-account, retained 24h (Stripe) | Adapter owns this, not the domain |
| Retry attempts (common) | 3–5 with exponential backoff | Policy table value, not inline |
| PostgreSQL unique violation | SQLSTATE `23505` | Maps to `409 Conflict` centrally |
| PostgreSQL serialization failure | SQLSTATE `40001` | Maps to "retryable" centrally |

## Real-world use case — Acme SaaS

Acme's billing service had retry logic copy-pasted into four call sites; one used fixed 1s delays,
another had no cap, and a third retried a permanent card decline, causing double charges during
retries because it lacked idempotency. The fix applied three principles at once: **separation** (the
domain returned outcomes; the adapter owned retrying), **centralized policy** (one retry table:
`40001`/`429`/`503` → retry, `card_declined`/`402` → never), and **single responsibility** (the
adapter did transport; the domain did rules). Duplicate charges went to zero, and the four copies of
retry logic became one.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Central policy table | No drift, easy audit | Must be kept current | Any shared contract |
| Local decisions | Context-aware | Can diverge | Optional features, UI |
| Shared primitives | Less boilerplate | Risk of hidden flow | Repeated patterns |
| Full framework | Powerful | Coupling, upgrade cost | Only at real scale |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Domain names failures; boundaries decide responses | Put HTTP codes in the domain |
| Centralize mapping, localize fallback | One giant middleware guessing intent |
| One job per handler | Catch, log, retry, translate, and continue in one block |
| Extract repeated plumbing | Copy-paste retry loops |

## Common mistakes

- **A "god" global handler** that encodes business decisions it cannot know.
- **Domain leaking transport** (`throw new Http404`).
- **Boilerplate removed by magic** — decorators that swallow the flow so nobody sees the failure.
- **One responsibility violated silently** — a validator that also persists.

## Checklist

- [ ] Does the domain avoid HTTP/transport concepts?
- [ ] Is policy defined once and reused?
- [ ] Does each handler have exactly one job?
- [ ] Can a new error be added by editing one registry entry?
- [ ] Is the happy path readable without wading through error code?

## Related

- [Explicitness, Consistency, and Predictability](./01-explicitness-consistency-and-predictability.md)
- [Chapter 9 — Layered Error-Handling Architecture](../../../part-04-architecture/09-layered-error-handling-architecture/README.md)
- [Chapter 53 — Reducing Error-Handling Complexity](../../../part-21-maintainability/53-reducing-error-handling-complexity/README.md)
- [Glossary: error boundary](../../../GLOSSARY.md)
