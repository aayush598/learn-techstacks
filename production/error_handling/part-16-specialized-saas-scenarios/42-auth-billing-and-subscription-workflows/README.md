# Chapter 42 — Authentication, Billing, and Subscription Workflows

> Part XVI · _Estimated reading time: 90–120 min_
> **Prerequisite:** [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)

## One-sentence summary

Auth and billing workflows fail in ways that are **irreversible or financially dangerous** —
double charges, locked-out customers, inconsistent entitlements — so every step needs an
explicit state, an idempotency story, and a reconciliation path back to the source of truth.

## Why this chapter matters

Billing is where error handling stops being about UX and becomes about money, contracts, and
trust. A `card_declined` retried like a timeout charges the customer twice. A webhook that
arrives out of order downgrades a paying customer to a free plan. A `past_due` subscription that
never transitions blocks an invoice forever. Auth failures are the other half: a refresh-token
bug that silently keeps sessions alive is a security incident, while a password-reset endpoint
that reveals whether an email exists is a user-enumeration hole. This chapter turns both
surfaces into explicit state machines with defined failure outcomes.

## Chapter map

The chapter has 16 sections grouped into eleven files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-account-lifecycle-errors.md`](./01-concepts/01-account-lifecycle-errors.md) | 42.1–42.4 | Sign-up races, email verification, password reset, session create/refresh |
| [`01-concepts/02-subscription-and-payment-errors.md`](./01-concepts/02-subscription-and-payment-errors.md) | 42.5–42.8 | Subscription creation, provider error classes, duplicate attempts, ambiguous outcomes |
| [`01-concepts/03-refunds-subscription-states-and-entitlements.md`](./01-concepts/03-refunds-subscription-states-and-entitlements.md) | 42.9–42.12 | Refund failures, legal state transitions, quota enforcement, entitlement resolution |
| [`01-concepts/04-invoice-webhooks-and-billing-consistency.md`](./01-concepts/04-invoice-webhooks-and-billing-consistency.md) | 42.13–42.15 | Invoice generation, webhook-driven state, preventing inconsistent billing |
| [`02-deep-dive/01-ambiguous-payment-outcomes-and-idempotency.md`](./02-deep-dive/01-ambiguous-payment-outcomes-and-idempotency.md) | 42.7, 42.8, 42.16 | Three-way outcome model, idempotency-key mechanics, safe-retry classification |
| [`02-deep-dive/02-billing-state-machine-and-reconciliation.md`](./02-deep-dive/02-billing-state-machine-and-reconciliation.md) | 42.10, 42.14, 42.15 | Transition guards, monotonic webhook appliers, drift reconciliation |
| [`02-deep-dive/03-entitlement-resolution-and-quota-mechanics.md`](./02-deep-dive/03-entitlement-resolution-and-quota-mechanics.md) | 42.11, 42.12 | Atomic quota counters, fail-open vs fail-closed, entitlement caching |
| [`03-practical-examples/01-checkout-subscription-state-machine.md`](./03-practical-examples/01-checkout-subscription-state-machine.md) | 42.5, 42.8, 42.10 | `Checkout` end-to-end: PaymentIntent + state machine + `requires_action` |
| [`03-practical-examples/02-webhook-reconciliation-and-safe-financial-retries.md`](./03-practical-examples/02-webhook-reconciliation-and-safe-financial-retries.md) | 42.13–42.16 | `WebhookIngest` applier, nightly reconciliation, retry classifier |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Billing/auth rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Safe-retry rules for financial ops, Stripe error map, glossary |

## Learning objectives

By the end you can:

- Model account creation, verification, reset, and session refresh as state machines with
  enumeration-safe error contracts.
- Classify every Stripe-style error code as **retryable**, **action-required**, or **terminal**.
- Design an idempotent `Checkout` flow that survives double-clicks, timeouts, and `409`
  concurrent-key conflicts.
- Resolve **ambiguous payment outcomes** by reconciling against the provider, not by guessing.
- Apply webhook events **monotonically and idempotently**, and detect drift with a
  reconciliation job.
- Enforce quotas atomically and decide, per operation, whether a downed entitlement store
  fails open or closed.

## Key takeaways

1. **Payment errors are not exceptions; they are classifications.** `card_declined` is terminal
   and user-actionable; `authentication_required` is *pending*, not failed; `rate_limit` is
   retryable with `Retry-After`.
2. **Ambiguity is a first-class state.** A timeout on a charge means "unknown," not "failed" —
   the only safe response is idempotent replay or provider reconciliation.
3. **Idempotency keys are scoped, time-boxed, and payload-bound.** Stripe retains them for
   **24 hours**; reusing a key with different parameters is an error, not a shortcut.
4. **Local billing state is a projection.** Webhooks duplicate, reorder, and get missed — the
   applier must be idempotent and monotonic, and a reconciliation job must be the backstop.
5. **Quota and entitlement checks have their own failure modes.** The store being down is a
   decision point (fail-open vs fail-closed), not an unhandled exception.
6. **Auth errors must not disclose.** Password-reset and verification endpoints answer the same
   way whether or not the account exists; refresh-token reuse revokes the whole token family.

## Exercises

1. Draw the full state machine for a subscription with `trialing`, `active`, `past_due`,
   `paused`, `canceled`, `unpaid` and write the guard for each transition.
2. List every payment provider error you can produce in your system and label each
   retryable / action-required / terminal.
3. Trigger a timeout on your payment capture path and write down exactly how you would prove
   whether the charge happened.
4. Write the SQL unique constraint and conflict-handling code for a webhook inbox keyed on
   `event_id`, and prove a duplicate delivery is a no-op.
5. Decide, for your five most expensive operations, whether entitlement-store downtime should
   fail open or closed — and write the rule next to the code.
6. Write the drift query for a reconciliation job that compares local subscription rows against
   provider objects nightly.

## Related

- [Chapter 43 — File and Media Processing Errors](../43-file-and-media-processing-errors/README.md)
- [Chapter 44 — AI, LLM, and Tool-Calling Errors](../44-ai-llm-and-tool-calling-application-errors/README.md)
- [Chapter 28 — Idempotency](../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- [Chapter 35 — Authentication, Authorization, and Tenant Isolation Errors](../../part-13-security-aware/35-auth-authorization-and-tenant-isolation-errors/README.md)
