# Chapter 42 — Do's and Don'ts

> Part XVI · Chapter 42 · All sections

A condensed rule set for auth, billing, and subscription workflows. Use it as a review
checklist for any change that touches money or sessions.

## Payments and idempotency

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Mint the idempotency key at **operation creation** (order row) | Mint a key per HTTP request or per button press |
| Reuse the same key on every retry, forever (local ledger) | Rely on the provider's 24 h retention alone |
| Treat provider 409 (`idempotency_error`) as wait-and-re-read | Surface 409 as a payment failure to the user |
| Reject same-key-different-params locally via a stored request hash | Discover the mismatch as a provider 400 mid-incident |
| Give refunds their own key (`refund:{chargeId}:{hash}`) | Reuse the charge's key for the refund |

## Error classification

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify every provider code once: terminal / action-required / retryable / bug | `catch { retry() }` on payment errors |
| Show `card_declined` etc. as actionable, terminal errors | Retry declines or surface them as 500s |
| Model `authentication_required` / `requires_action` as **pending** | Report SCA challenges as failures |
| Trust `Retry-After` on 429 | Sleep a fixed interval |
| Read codes, never message strings | `if (msg.includes("card"))` |

## Ambiguous outcomes

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Represent "unknown" as a first-class state (`pending_verification`) | Map timeouts to "failed" |
| Resolve ambiguity by same-key replay, then provider lookup, then park | Re-capture with a fresh key |
| Tell the user "confirming your payment" for unknowns | Tell them "failed" while money may have moved |
| Drain the verification queue with backoff, then human review | Let unknowns sit indefinitely |

## Subscriptions and webhooks

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Move status only through one guarded state machine | Write `subscriptions.status` from feature code |
| Dedupe on provider `event.id` in a durable ledger | "Check current status" as dedupe |
| Compare provider timestamps; drop stale events | Last-write-wins appliers |
| Treat `canceled` / `incomplete_expired` as terminal | Let a late `invoice.paid` resurrect a canceled sub |
| Reconcile against the provider on a schedule | Trust the local projection forever |
| Verify the checkout session server-side (or wait for the webhook) | Grant entitlements on the browser redirect |

## Quotas and entitlements

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Consume quota with one atomic SQL/Lua operation | Read-modify-write counters in app code |
| Distinguish `QUOTA_EXCEEDED` (402/429) from `QUOTA_UNVERIFIABLE` (503) | Map store outages to 403 |
| Fail closed for costly/irreversible ops on unknown entitlement | Fail open everywhere "for availability" |
| Keep entitlement cache TTL short; invalidate on billing events | Cache denials for hours |
| Default unknown features to denied + metric | Default unknown to free |

## Auth and sessions

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Catch unique violations (`23505`) as "already registered" | Let duplicate sign-ups 500 |
| Commit the account, then enqueue the welcome email | Send email inside the DB transaction |
| Answer password-reset requests identically for known/unknown emails | Return 404 for unknown accounts |
| Hash reset/verification tokens at rest; single-use; TTL-bounded | Store raw tokens with long TTLs |
| Rotate refresh tokens; revoke the family on reuse | Ignore refresh reuse detection |
| Return machine-readable codes for expired vs invalid refresh | Bare `401` that forces re-auth always |

## Anti-patterns in the wild

1. **The Per-Request Key** — every retry is a fresh charge. Root cause of nearly every
   double-charge postmortem.
2. **The Ambiguity Eraser** — `catch { throw PaymentFailed }` on a timeout. Destroys the one
   signal you need.
3. **The Resurrection** — last-write-wins webhook applier brings canceled subscriptions back.
4. **The Silent Sweep** — no reconciliation job; the first webhook outage is permanent drift.
5. **The Collapsed 403** — entitlement or quota store outage rendered as "you don't have
   access," cached by clients.
6. **The Enumeration Oracle** — password-reset or sign-up responses that differ for existing
   accounts.
7. **The Inline Email** — account creation transaction coupled to the email provider; an
   email outage becomes a sign-up outage.

## Chapter checklist

- [ ] Every money write carries an operation-scoped idempotency key, stored locally.
- [ ] One reviewed classifier decides all financial retry policy.
- [ ] Unknown payment outcomes have a state, a queue, and an owner.
- [ ] Billing state changes go through the guarded applier only.
- [ ] Reconciliation runs on a schedule and its auto-apply classes are documented.
- [ ] Quota/entitlement failures are distinguishable from denials.
- [ ] Auth endpoints pass an enumeration review; sessions rotate and detect reuse.

## Related

- [Chapter 42 Reference](../05-reference/README.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Part XVII — Error Handling in Architecture and Code Organization](../../../part-17-organization/README.md)
