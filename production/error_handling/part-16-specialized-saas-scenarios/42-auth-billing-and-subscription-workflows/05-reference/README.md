# Chapter 42 — Reference

> Part XVI · Chapter 42 · Safe-retry rules for financial operations, Stripe error map,
> subscription state table, and glossary.

## Safe-retry rules for financial operations

Apply in order. **If no rule applies, do not retry — reconcile.**

| # | Situation | Retry? | Key | Notes |
| - | --------- | ------ | --- | ----- |
| 1 | Provider rejected the request before evaluation (`invalid_request_error`) | ❌ | — | Fix code; retrying repeats the bug |
| 2 | Terminal outcome (`card_declined`, `expired_card`, `incorrect_cvc`, `insufficient_funds`) | ❌ | — | User action required |
| 3 | Action required (`authentication_required`) | ❌ | — | Resume 3DS/SCA challenge; state = pending |
| 4 | Rate limited (`429`, `rate_limit`) | ✅ | **same** | Honor `Retry-After`; jittered backoff |
| 5 | Provider transient **before send** (connect refused, DNS) | ✅ | **same** | No side effect possible |
| 6 | Provider `5xx` / timeout **after send** (ambiguous) | ⚠️ replay **once** | **same** | Then reconcile; never a new key |
| 7 | Concurrent same-key request (`409`, `idempotency_error`) | ⚠️ wait + re-read | **same** | Not a failure |
| 8 | Key older than 24 h and outcome unknown | ❌ | — | Provider retention expired; look up or park |
| 9 | Refund of an already-refunded charge | ❌ | — | Return existing refund as success-shaped |
| 10 | Read-only status query | ✅ | n/a | Always safe |

**Non-negotiables**

- A financial write **always** carries an idempotency key derived from the business
  operation, not the HTTP request.
- "Unknown outcome" is a state (`pending_verification`), never mapped to "failed."
- Retries beyond the provider's retention window are **new operations** to the provider.

## Stripe-flavored error map

| Code / HTTP | Class | User-facing meaning | Handling |
| ----------- | ----- | ------------------- | -------- |
| `card_declined` (402) | Terminal | Card refused | Update-card CTA |
| `expired_card` (402) | Terminal | Card expired | Update-card CTA |
| `incorrect_cvc` (402) | Terminal | Wrong CVC | Re-enter |
| `incorrect_number` (402) | Terminal | Bad number | Re-enter |
| `insufficient_funds` (402) | Terminal | No funds | Retry later, user-initiated |
| `authentication_required` (402) | Action required | Bank verification | 3DS/SCA challenge |
| `processing_error` (402/500) | Transient | Temporary | Retry same key |
| `rate_limit` (429) | Transient | Too many requests | `Retry-After` + same key |
| `invalid_request_error` (400) | Bug | — | Fix code; never retry |
| `idempotency_error` (400) | Bug | — | Same key, different params — fix |
| `idempotency_error` (409) | Concurrent | — | Wait, then re-read |
| `resource_missing` (404) | Bug/config | — | Wrong ID or wrong account/mode |
| `charge_already_refunded` | Terminal | Already refunded | Return existing refund |
| `insufficient_quota` (AI providers) | Account | Billing/config | Not retryable until fixed |

## Idempotency-key facts

| Fact | Value |
| ---- | ----- |
| Provider retention (Stripe) | **24 hours** |
| Same key + same params | Stored response replayed |
| Same key + different params | HTTP **400** `idempotency_error` |
| Same key while in flight | HTTP **409** `idempotency_error` |
| Scope | Per endpoint; keys are not global |
| Local ledger retention | At least the dispute window; commonly indefinite |
| Recommended key shape | `charge:{orderId}`, `refund:{chargeId}:{intentHash}` |

## Subscription status table

| Status | Entitled? | Terminal? | Typical next |
| ------ | --------- | --------- | ------------ |
| `incomplete` | No (or trial-only) | No | `active`, `incomplete_expired` |
| `trialing` | Yes | No | `active`, `past_due` |
| `active` | Yes | No | `past_due`, `paused`, `canceled` |
| `past_due` | Read yes; writes per policy | No | `active`, `unpaid`, `canceled` |
| `unpaid` | No (after grace) | No | `active`, `canceled` |
| `paused` | No (or read-only) | No | `active`, `canceled` |
| `canceled` | No | **Yes** | — (new subscription if returning) |
| `incomplete_expired` | No | **Yes** | — |

## Webhook handling quick rules

| Rule | Why |
| ---- | --- |
| Dedupe on `event.id` in a durable ledger | Providers retry deliveries (Stripe ~3 days) |
| Ack after ledger insert, apply async | Fast ack prevents retry storms |
| Guard transitions with provider timestamps | Events arrive out of order |
| Terminal states reject transitions | Late events must not resurrect |
| Return 5xx on internal failure, 4xx on bad signature | Retry semantics |
| Reconcile on a schedule regardless | Events can be lost permanently |

## Auth quick rules

| Area | Rule |
| ---- | ---- |
| Sign-up | Catch `23505`; treat as already-registered, not 500 |
| Email send | Outbox/queue **after** commit; never inside the tx |
| Verification token | Single-use, hashed, ~24 h TTL |
| Password reset | Identical response for existing/non-existing accounts |
| Reset token | Single-use, hashed, ~30–60 min TTL, throttled resend |
| Access token | Short TTL (commonly ~15 min), machine-readable expiry code |
| Refresh token | Rotate on use; reuse ⇒ revoke family |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **Ambiguous outcome** | A call where success/failure cannot be determined (timeout after send) |
| **Idempotency key** | Client/server token that lets the provider collapse duplicate requests |
| **Dunning** | The retry-and-notify process for failed invoice payments |
| **Entitlement** | The right to use a feature, derived from billing state |
| **Projection** | Local state derived from provider objects via events |
| **Reconciliation** | Periodic comparison of local projection against the provider |
| **Monotonic applier** | Applier that ignores events older than current state |
| **Terminal state** | A state no further transitions are allowed from |
| **Fail-closed / open** | Deny vs allow when a check cannot be completed |
| **SCA / 3DS** | Strong Customer Authentication / 3-D Secure challenge |

## Signposts

- Payments and idempotency in depth → [Ch. 28 Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- Webhook transport mechanics → [Ch. 33 Events and Webhooks](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- Auth and enumeration → [Ch. 35 Auth Errors](../../../part-13-security-aware/35-auth-authorization-and-tenant-isolation-errors/README.md)
- Degradation policy → [Ch. 30 Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)

## Related

- [Chapter 42 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 42 Overview](../README.md)
- [Part XVI Index](../../README.md)
