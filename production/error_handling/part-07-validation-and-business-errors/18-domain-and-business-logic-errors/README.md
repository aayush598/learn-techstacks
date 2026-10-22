# Chapter 18 — Domain and Business Logic Errors

> Part VII · _Estimated reading time: 90–130 min_
> **Prerequisite:** [Chapter 17 — Input Validation Error Handling](../17-input-validation-error-handling/README.md)

## One-sentence summary

A **domain error** is a first-class, coded value expressing that a well-formed request is
unacceptable *right now* — a violated **invariant**, **state transition**, **ownership** rule,
**duplicate**, **quota**, **entitlement**, or **precondition** — and it must be modeled, categorized,
and translated with the same care as your entities, never thrown as a bare string.

## Why this chapter matters

Validation errors say "fix your request"; domain errors say "the world says no" — and the world
saying no is *normal product behavior*, not a crash. Teams that throw `Error("invalid state")`
from service methods lose exactly the information the client and support need: which rule failed,
whether retrying helps, whether it is a conflict (`409`), a permission problem (`403`), or a
billing problem (`402`). Those teams end up with every business denial rendered as a `500` or a
generic `400`, support playing archaeology with stack traces, and clients that cannot branch. The
fix is not more exceptions — it is a **domain error vocabulary** with owners and mappings.

## Chapter map

The chapter has 20 sections. They are grouped into these files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-what-domain-errors-are.md`](./01-concepts/01-what-domain-errors-are.md) | 18.1, 18.11, 18.18 | Definition; separating domain from infrastructure errors; preserving domain meaning through layers |
| [`01-concepts/02-invariants-and-business-rules.md`](./01-concepts/02-invariants-and-business-rules.md) | 18.2, 18.3, 18.19 | Invariants vs rules, where each is enforced, and how multiple simultaneous violations are handled |
| [`01-concepts/03-state-transitions-and-lifecycle.md`](./01-concepts/03-state-transitions-and-lifecycle.md) | 18.4, 18.6, 18.10 | Invalid state transitions, entity lifecycles, workflow preconditions |
| [`01-concepts/04-access-duplicates-quota-entitlements.md`](./01-concepts/04-access-duplicates-quota-entitlements.md) | 18.5, 18.7–18.9 | Ownership/access, duplicate/uniqueness, insufficient balance/quota, subscription/entitlement |
| [`01-concepts/05-outcome-modeling-and-contracts.md`](./01-concepts/05-outcome-modeling-and-contracts.md) | 18.12, 18.13, 18.20 | Expected outcomes vs exceptions, modeling alternative outcomes (Result/unions), backward-compatible domain contracts |
| [`02-deep-dive/01-domain-services-aggregates-and-ddd.md`](./02-deep-dive/01-domain-services-aggregates-and-ddd.md) | 18.14–18.16 | Domain services, aggregate operations, DDD alignment |
| [`02-deep-dive/02-framework-independence-and-outcome-mechanics.md`](./02-deep-dive/02-framework-independence-and-outcome-mechanics.md) | 18.11, 18.12, 18.17, 18.18 | Keeping the domain framework-free; exception-vs-result mechanics across languages; meaning-preserving translation |
| [`03-practical-examples/01-value-object-money-and-domain-errors.md`](./03-practical-examples/01-value-object-money-and-domain-errors.md) | all | Value objects (`Money`, `Seats`) that make invariant violations impossible; coded domain errors end to end |
| [`03-practical-examples/02-entitlement-lifecycle-and-webhooks.md`](./03-practical-examples/02-entitlement-lifecycle-and-webhooks.md) | all | Entitlement denial, invalid transitions, and duplicate webhooks across `Checkout`/`WebhookIngest` |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Domain-error rules, anti-patterns, checks |
| [`05-reference/README.md`](./05-reference/README.md) | all | Domain error contract, HTTP/gRPC mapping tables, decision tables |

## Learning objectives

By the end you can:

- Define a domain error and distinguish it from validation and infrastructure errors (18.1, 18.11).
- Enforce **invariants** at construction/mutation and **business rules** at the service layer,
  including multi-violation behavior (18.2, 18.3, 18.19).
- Model lifecycle, **state transitions**, and **workflow preconditions** as explicit, coded
  outcomes (18.4, 18.6, 18.10).
- Give ownership, duplicate, quota/balance, and entitlement denials **named errors with correct
  HTTP mappings** (18.5, 18.7–18.9).
- Choose **exception vs result** deliberately, model alternative outcomes, and keep domain
  contracts backward-compatible (18.12, 18.13, 18.20).
- Place logic in **domain services** and **aggregates** correctly and keep the domain free of
  framework dependencies (18.14–18.17).

## Key takeaways

1. **Domain errors are data.** `InsufficientSeats { requested, available }` with a code and a
   category — not `Error("not enough seats")`.
2. **Invariants live with the data; rules live with the flow.** An object that can exist in an
   invalid state will eventually do so; a rule that needs the DB does not belong in a constructor.
3. **Expected outcomes are not exceptions.** "Already subscribed", "trial not ended", "not your
   project" are documented API results with statuses (`409`, `403`, `404`), not server crashes.
4. **Every domain error has one HTTP/gRPC mapping, decided by category** — never guessed
   per-handler ([Ch. 19/20](../../part-08-http-and-api/19-http-error-semantics/README.md)).
5. **The domain must not know the transport or the framework.** No HTTP statuses, no Spring/Django
   exception types inside domain code — translation happens at the boundary (18.17).
6. **Version the vocabulary.** Adding a code is additive; changing what a code means or which
   status it maps to is a breaking change (18.20).

## Exercises

1. List every "no" your API currently returns; map each to invariant, transition, ownership,
   duplicate, quota, entitlement, or precondition.
2. Find one business denial thrown as a generic `Error`/`Exception` and give it a code, category,
   details, and HTTP mapping.
3. Draw your subscription state machine; mark every illegal arrow and the error code it should
   produce.
4. Audit your domain layer for framework imports (`spring`, `django`, `fastapi`, `express`) and
   HTTP status numbers; list what must move to the boundary.
5. Pick one existing domain error code and write its backward-compatible deprecation plan.

## Related

- [Chapter 17 — Input Validation Error Handling](../17-input-validation-error-handling/README.md)
- [Chapter 5 — Error Categories in Detail](../../part-02-error-taxonomy/05-error-categories-in-detail/README.md)
- [Part IX — Database, Persistence, and Transaction Errors](../../part-09-database-and-transactions/README.md)
- [Part VII — Part overview](../README.md)
