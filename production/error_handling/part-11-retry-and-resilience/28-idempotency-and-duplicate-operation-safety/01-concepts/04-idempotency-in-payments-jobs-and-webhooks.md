# Idempotency in Payments, Jobs, and Webhooks

> Part XI · Chapter 28 · Sections 28.11–28.14 · _Estimated reading time: 20 min_
> **Prerequisite:** [Failure Contracts and Uncertain Outcomes](./03-failure-contracts-and-uncertain-outcomes.md)

## In one sentence

The same idempotency mechanism applies everywhere, but **the natural key changes**: a payment uses
an order/charge key, a job uses `(job_id, step)`, a webhook uses the provider's event id, and a
distributed workflow uses a key that travels with the request.

## Why this matters in production

Each of these domains has a different duplicate source and a different consequence. A duplicate
payment costs money and trust. A duplicate job corrupts a dataset or double-sends notifications. A
duplicate webhook flips a subscription state twice. A distributed duplicate is the hardest because no
single database owns the truth. Knowing the natural key for each is most of the design.

## 28.11 — Payments

### The key

Use a deterministic key derived from the **business operation**, not a random per-request value:

```text
charge key      = tenant_id : order_id : "charge"
refund key      = tenant_id : payment_id : "refund" : refund_request_id
subscription key= tenant_id : signup_id : "subscription"
```

### The flow

```text
1. Verify amount/currency against the stored order (never trust the client).
2. Claim idempotency key (tenant, key) in the DB.
3. Create a local payment row (status=pending, key).
4. Call the provider with the same key.
5. On success: payment=succeeded, key=completed, store provider charge id.
6. On decline: payment=failed, key=failed_terminal.
7. On timeout: payment=unknown, key=unknown → reconcile.
```

### Rules specific to money

| Rule | Reason |
| ---- | ------ |
| Amount comes from the server-side order | A retried client must not change the price |
| Same key to your DB and the provider | Both layers must dedupe |
| Never retry a captured charge with a new key | Guarantees a duplicate |
| Refunds are idempotent by refund id | A retried refund must not refund twice |
| Store provider id + key together | Enables reconciliation and audit |
| Alert on duplicate provider charges | Detect the failure you failed to prevent |

> ⚠️ **Hazard.** A "retry payment" button that creates a new key per click is a duplicate-charge
> button. Derive the key from the order and persist it before the first call.

## 28.12 — Jobs

### The key is the step, not the job

A long job has many steps. Retrying the job should replay completed steps and resume at the failed
one.

```text
job key = job_id : step_name : step_input_hash
```

```ts
interface StepRecord {
  jobId: string;
  step: string;
  inputHash: string;
  status: "pending" | "done" | "failed";
  output?: unknown;
}

async function runStep<T>(jobId: string, step: string, input: unknown, fn: () => Promise<T>) {
  const key = { jobId, step, inputHash: hash(input) };
  const existing = await steps.get(key);
  if (existing?.status === "done") return existing.output as T;

  await steps.claim(key);           // unique constraint
  const output = await fn();
  await steps.complete(key, output); // atomic with any local write
  return output;
}
```

### Rules specific to jobs

| Rule | Reason |
| ---- | ------ |
| Step keys include an input hash | A changed input is a new step |
| Outputs are stored | A resumed job can reuse them |
| Checkpoint after each step | Resume, don't restart |
| Side effects use the step key | Emails, uploads, API writes |
| Poison steps go to a DLQ | Do not retry forever |
| Queue redelivery is expected | At-least-once is the norm |

## 28.13 — Webhooks

### The key is the provider's event id

Webhook providers deliver **at least once** and retry on non-2xx responses. The event id is the
natural idempotency key.

```ts
app.post("/webhooks/stripe", async (req, res) => {
  verifySignature(req); // reject forgeries before any processing

  const event = req.body;
  const firstSeen = await events.insertIfAbsent({
    provider: "stripe",
    eventId: event.id,          // evt_...
    type: event.type,
    payloadHash: hash(event),
  });

  if (!firstSeen) return res.status(200).json({ received: true, duplicate: true });

  await queue.enqueue("stripe-event", event); // async processing
  return res.status(200).json({ received: true });
});
```

### Rules specific to webhooks

| Rule | Reason |
| ---- | ------ |
| Dedup on the event id, not the payload | Payloads may differ in metadata |
| Acknowledge **before** long processing | Providers time out and retry |
| Process asynchronously via a queue | Keeps the webhook endpoint fast |
| Make the handler idempotent too | Queue redelivery happens |
| Store the raw event for replay | Needed for debugging and backfill |
| Ignore unknown event types safely | Providers add events over time |

A duplicate webhook should return `2xx` (so the provider stops retrying) without re-applying the
effect.

## 28.14 — Distributed idempotency

In a multi-service workflow, no single database owns the operation. The key must **travel with the
request** and each service must dedupe locally.

```text
Client ── key=K ──▶ API gateway ── key=K ──▶ Order service ── key=K:charge ──▶ Payment service
                                                  │
                                                  └── key=K:inventory ──▶ Inventory service
```

### Patterns

| Pattern | How it works | Trade-off |
| ------- | ------------ | --------- |
| **Propagated key** | The original key (or a derived child key) is forwarded to every service | Requires discipline; child keys must be deterministic |
| **Idempotency service** | A shared store answers "have I seen K?" | Extra network hop, single point of failure |
| **Outbox per service** | Each service records intent + result locally, emits events | Eventual consistency |
| **Saga log** | Workflow state persisted centrally | More orchestration complexity |

### Child key derivation

```text
parent key K
  → charge key      = K : "payment"
  → inventory key   = K : "reserve"
  → notification key= K : "email" : message_id
```

Deterministic derivation means a retried parent reproduces the same child keys, so every service
dedupes consistently.

### Distributed rules

1. **Never regenerate a key at a service boundary.**
2. **Derive child keys deterministically** from the parent and the step.
3. **Each service stores its own key-to-result mapping**; do not assume a shared DB.
4. **Include the key in events** so consumers can dedupe.
5. **Reconcile across services** when an outcome is unknown (28.15).

## Worked example — subscription upgrade

```text
1. Client: POST /upgrade key=K.
2. API: forwards K to Billing.
3. Billing: claims K, calls Stripe with key "K:charge".
4. Billing: on success, emits SubscriptionUpgraded {key:K}.
5. Entitlements consumer: dedupes on event key K before granting features.
6. Notifications consumer: dedupes on K:email before sending.
```

If step 3 times out and the client retries, Billing replays the charge result, and no consumer sees a
second event.

## Key data / numbers

- Stripe webhook events carry a unique `evt_...` id; use it as the dedup key.
- Provider idempotency-key retention: commonly **24 hours**.
- Webhook endpoints should respond in **under a few seconds**; queue the work.
- Job step key: `job_id : step : input_hash`.
- Child key format: `parent_key : step` (deterministic).
- Duplicate webhook response: `200` with `duplicate: true`.

## Real-world use case — WebhookIngest

`WebhookIngest` processed Stripe `invoice.paid` events synchronously and returned `500` on transient
DB errors. Stripe retried, the handler ran again, and the tenant's invoice was marked paid twice —
triggering two receipt emails and a duplicate accounting entry. The team switched to: verify
signature, dedupe on `event.id`, enqueue, return `200`, and process with an idempotent worker keyed by
the event id. Duplicate accounting entries stopped, and webhook latency dropped from seconds to
milliseconds.

## Trade-offs

| Domain | Natural key | Main risk |
| ------ | ----------- | --------- |
| Payments | Order/refund id | Double charge |
| Jobs | Job id + step + input hash | Duplicate side effects |
| Webhooks | Provider event id | Double state transition |
| Distributed | Propagated key / child keys | Inconsistent dedup across services |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Derive payment keys from the order | Generate a new key per retry/click |
| Key job steps by input hash | Key only by job id |
| Dedup webhooks on event id | Dedup on payload bytes |
| Acknowledge webhooks before long work | Process synchronously and risk timeout |
| Propagate keys across services | Regenerate at each boundary |
| Derive child keys deterministically | Use random child keys |

## Common mistakes

- **Retrying a refund with a new key**, refunding twice.
- **Deduping a webhook on the payload**, which changes between deliveries.
- **Acking a webhook after processing**, so the provider times out and retries.
- **Job step keys without input hashes**, so a changed input is silently skipped.
- **Assuming a shared idempotency store across services**, which usually does not exist.

## Checklist

- [ ] Payments: key derived from the order, used at both DB and provider.
- [ ] Refunds: key derived from the refund request.
- [ ] Jobs: step key includes `job_id`, step, and input hash.
- [ ] Jobs: outputs stored for resume.
- [ ] Webhooks: dedup on provider event id before processing.
- [ ] Webhooks: acknowledged before long work.
- [ ] Distributed: keys propagate, child keys are deterministic.

## Related

- [Idempotency Key Lifecycle](../02-deep-dive/01-idempotency-key-lifecycle.md)
- [Checkout and Webhook Idempotency](../03-practical-examples/02-checkout-and-webhook-idempotency.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- [Chapter 42 — Authentication, Billing, and Subscription Workflows](../../../part-16-specialized-saas-scenarios/42-auth-billing-and-subscription-workflows/README.md)
