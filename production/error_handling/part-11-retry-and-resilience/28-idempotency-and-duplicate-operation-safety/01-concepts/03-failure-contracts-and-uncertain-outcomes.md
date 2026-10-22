# Failure Contracts and Uncertain Outcomes

> Part XI · Chapter 28 · Sections 28.10, 28.15, 28.16 · _Estimated reading time: 18 min_
> **Prerequisite:** [Idempotency Keys and Duplicate Detection](./02-idempotency-keys-and-duplicate-detection.md)

## In one sentence

An idempotent operation needs an explicit **failure contract**: which attempt failures are safe to
retry, what gets recorded when a side effect fails, and how to resolve the case where the caller
genuinely cannot tell whether the operation succeeded.

## Why this matters in production

Most idempotency designs handle the happy duplicate well and break on the unhappy ones. A failed
attempt that recorded the key as "done" blocks a legitimate retry. A failed attempt that recorded
nothing lets a retry duplicate partial work. An unknown outcome — the payment may or may not have
been captured — is reported as "failed," and finance discovers the discrepancy days later. The
failure contract is the difference between a dedup table and a trustworthy ledger.

## 28.10 — The failure contract

When an attempt fails, the key record must transition deliberately:

| Failure type | Recorded state | Retry under same key? |
| ------------ | -------------- | --------------------- |
| Transient before side effect | `failed_retryable` | Yes |
| Transient after partial side effect | `in_progress` / `unknown` | Only after reconciliation |
| Terminal validation error | `failed_terminal` | No; replay the error |
| Provider declined (business) | `failed_terminal` | No; replay the decline |
| Process crashed mid-operation | `unknown` (lease expiry) | Reconcile, then decide |
| Side effect succeeded, response lost | `completed` | Yes; replay success |

### Rule: record failures, do not delete keys

Deleting the key on failure reopens the duplicate window. Persist the failure with enough context for
the next request to make the same decision.

```ts
type KeyState =
  | { state: "in_progress"; leaseUntil: number }
  | { state: "completed"; status: number; body: unknown; resourceId: string }
  | { state: "failed_retryable"; lastError: string }
  | { state: "failed_terminal"; status: number; body: unknown }
  | { state: "unknown"; lastError: string; reconcileBy: string };
```

### The transaction boundary

The strongest design commits the key record and the side effect **in one transaction**:

```text
BEGIN
  claim key (in_progress)
  create charge row (pending)
  call provider?  ── external call cannot be in the DB transaction ──
  update charge (succeeded) + key (completed)
COMMIT
```

External calls cannot participate in a DB transaction, so the common pattern is:

1. Commit an intent/outbox row with the key.
2. Call the provider.
3. Commit the outcome and mark the key complete.
4. If step 2 times out, mark `unknown` and reconcile.

This is where idempotency meets the transactional outbox (Chapter 23.17).

## 28.15 — Uncertain outcomes

An uncertain outcome means the caller cannot determine success. It is **not** the same as failure.

### The three states after an ambiguous call

```text
                 ┌─────────────┐
   request ────▶ │  provider   │
                 └──────┬──────┘
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
   succeeded       failed            unknown
   (observed)     (observed)      (no response)
```

For `unknown`, the correct action is **reconciliation**, not retry:

1. Query the provider using your own correlation id / idempotency key.
2. If found succeeded → mark key `completed`, return success.
3. If found failed → mark retryable/terminal and act accordingly.
4. If not found after the provider's consistency window → retry (with the same key).

```ts
async function reconcileCharge(key: string, provider: Provider) {
  const found = await provider.findByKey(key); // provider must support lookup
  if (!found) return { state: "not_found" as const };
  return found.status === "succeeded"
    ? { state: "completed" as const, resourceId: found.id }
    : { state: "failed" as const, reason: found.failureCode };
}
```

If the provider offers no lookup, use your own outbox + webhook correlation, or a provider idempotency
key that guarantees a retry returns the original result.

### Never report "unknown" as success or failure

| Report | Consequence |
| ------ | ----------- |
| `unknown` as success | Customer thinks it worked; no charge may exist |
| `unknown` as failure | Customer retries; may double-charge |
| `unknown` as `pending` + reconcile | Correct: the system resolves it |

Surface `202 Accepted` / `pending` with a status endpoint when resolution is asynchronous.

## 28.16 — Preventing duplicate billing and creation

Duplicate billing is the highest-cost failure in this chapter. The defenses stack:

| Layer | Defense |
| ----- | ------- |
| Client | Generate one key per checkout; disable the button after submit |
| API | Require `Idempotency-Key` on `POST /charges`, `/refunds`, `/subscriptions` |
| Storage | Unique `(tenant_id, key)` + payload hash |
| Provider | Pass the same key to Stripe/Adyen; they dedupe server-side |
| Reconciliation | Nightly job compares your ledger to provider charges by key |
| Alerts | Alert on any charge without a matching key record |

### The double-defense principle

Use **both** your key and the provider's key. Your key protects against your own retries; the
provider's key protects against network ambiguity between you and them. Stripe, for example, retains
keys for 24 hours and returns the original response for a repeated key.

```ts
await stripe.charges.create(
  { amount, currency, customer, source },
  { idempotencyKey: `${tenantId}:${orderId}:charge` },
);
```

### Duplicate creation (non-billing)

For projects, exports, and invitations, prefer a **natural unique constraint** first:

```sql
CREATE UNIQUE INDEX projects_tenant_slug_key ON projects (tenant_id, slug);
```

Then the idempotency key handles the case where the client cannot supply a natural identity. The two
mechanisms complement each other: the constraint prevents duplicates forever; the key prevents
duplicates within the retry window and lets the server replay the original response.

## Worked example — payment with unknown outcome

```text
1. Client POSTs /pay key=K.
2. Server claims K, writes charge(status=pending, key=K).
3. Provider call times out after 5s. Server marks charge unknown, key unknown.
4. Server returns 202 { status:"pending", reconcile:"/charges/ch_1" }.
5. Reconciler queries provider by key K.
6a. Provider says succeeded → charge=succeeded, key=completed. Client polling sees success.
6b. Provider says not found after consistency window → server retries with key K.
6c. Provider says declined → charge=failed, key=failed_terminal. Client sees decline.
```

At no point does the client's retry create a second charge.

## Key data / numbers

- Stripe idempotency-key retention: **24 hours** by default.
- Reconciliation consistency window: seconds to minutes for most providers; check your provider.
- Key TTL must exceed the retry window and the reconciliation window.
- Ambiguous outcome response: `202 Accepted` + a status/reconcile endpoint.
- Alert if a captured charge has no `key` record.

## Real-world use case — Checkout

Checkout marked keys as `completed` as soon as the provider call *returned*, and as `failed` when it
threw. A timeout that occurred after the provider captured the charge recorded `failed`. The client
retried, saw `failed`, and tried a new payment method, producing a second charge. The fix introduced
an explicit `unknown` state plus a reconciler that queried Stripe by idempotency key. Charges with no
matching local record dropped to zero, and the finance reconciliation job went from a weekly manual
task to an automated check.

## Trade-offs

| Approach | Pros | Cons |
| -------- | ---- | ---- |
| DB transaction with side effect | Atomic | Impossible for external calls |
| Outbox + async commit | Reliable | More moving parts, eventual |
| Provider idempotency only | Simple | Trusts provider retention window |
| Reconciliation job | Resolves unknown | Needs provider lookup support |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Record terminal failures | Delete the key on failure |
| Add an explicit `unknown` state | Collapse unknown into failed |
| Reconcile by correlation id | Retry blind after a timeout |
| Use both your key and the provider's | Rely on only one dedup layer |
| Alert on charges without keys | Assume the ledger is complete |
| Return `202` + status endpoint | Return `500` for a pending outcome |

## Common mistakes

- **Treating a provider timeout as failure**, then retrying with a new key.
- **Deleting keys on error**, reopening the duplicate window.
- **Marking completed before the side effect commits**, so a crash loses the work but blocks retry.
- **No reconciler**, leaving unknown outcomes permanently unresolved.
- **Assuming provider key retention is infinite** (it is often 24h).

## Checklist

- [ ] Every failure type maps to a persisted key state.
- [ ] Unknown outcomes are distinct from failures.
- [ ] A reconciler queries the provider by correlation id.
- [ ] Retries reuse the same key at both your layer and the provider.
- [ ] A `202`/status endpoint exists for pending outcomes.
- [ ] Alerts fire on side effects without key records.
- [ ] Key TTL exceeds retry + reconciliation windows.

## Related

- [Idempotency Key Lifecycle](../02-deep-dive/01-idempotency-key-lifecycle.md)
- [Checkout and Webhook Idempotency](../03-practical-examples/02-checkout-and-webhook-idempotency.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
- [Chapter 39 — Partial Failures and Multi-Step Operations](../../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
