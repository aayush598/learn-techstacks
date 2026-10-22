# Webhook Signatures, Retries, and Timeouts

> Part XII · Chapter 33 · Sections 33.10–33.12 · _Estimated reading time: 18 min_
> **Prerequisite:** [Publish and Consume Failures](./01-publish-and-consume-failures.md)

## In one sentence

A webhook endpoint must **verify the signature on the raw body**, **store the event durably and
return `2xx` fast**, and let the sender's retry policy do the retrying — because the sender, not you,
owns redelivery.

## Why this matters in production

Webhooks are unauthenticated HTTP by default. Without signature verification, anyone can POST a fake
`invoice.paid` and grant themselves a paid plan. Without a fast `2xx`, the sender times out and
retries, multiplying load. Without idempotency, those retries double-apply the event. Signature
verification, fast acknowledgement, and dedupe are the three legs of a safe webhook.

## 33.10 — Webhook signature errors

A signature error means the request cannot be trusted. Treat it as **authentication failure**, not a
business error:

| Cause | Response | Notes |
| ----- | -------- | ----- |
| Missing signature header | `400`/`401` | Reject |
| Malformed header | `400` | Reject |
| Signature mismatch | `400`/`401` | Reject; do not process |
| Timestamp too old | `400` | Replay protection |
| Unknown key id | `400`/`401` | Rotation mismatch |
| Body parsed before verification | — | Verification fails due to reserialization |

> ⚠️ **Hazard.** Frameworks often parse JSON before your handler runs. Signature verification must
> use the **raw request body bytes**. Re-serializing the parsed object changes whitespace/key order
> and breaks the HMAC.

### Stripe's scheme (concrete)

Stripe sends a `Stripe-Signature` header:

```text
Stripe-Signature: t=1729502520,v1=5257a869e7ecebeda32affa62cdca3fa51cad7e77a0e56ff536d0ce8e108d8bd
```

- `t` — Unix timestamp (seconds) when the signature was created.
- `v1` — HMAC-SHA256 of `"{t}.{raw_body}"` using the endpoint's signing secret.
- Default tolerance: **300 seconds** (5 minutes).
- Multiple `v1` values may be present during secret rotation; accept if any matches.

```ts
import crypto from "node:crypto";

function verifyStripe(rawBody: Buffer, header: string, secret: string, toleranceSec = 300): boolean {
  const parts = Object.fromEntries(header.split(",").map((p) => p.split("=") as [string, string]));
  const timestamp = Number(parts.t);
  if (!Number.isFinite(timestamp)) return false;
  if (Math.abs(Date.now() / 1000 - timestamp) > toleranceSec) return false; // replay

  const expected = crypto
    .createHmac("sha256", secret)
    .update(`${parts.t}.${rawBody.toString("utf8")}`)
    .digest("hex");

  const provided = header.split(",").filter((p) => p.startsWith("v1=")).map((p) => p.slice(3));
  return provided.some((sig) =>
    sig.length === expected.length &&
    crypto.timingSafeEqual(Buffer.from(sig, "hex"), Buffer.from(expected, "hex")),
  );
}
```

`timingSafeEqual` avoids leaking how many bytes matched. Length-check first, because
`timingSafeEqual` throws on unequal lengths.

## 33.11 — Webhook retries

Senders retry failed deliveries, so **duplicates are expected**:

| Provider | Retry behavior (commonly) |
| -------- | ------------------------- |
| Stripe | Retries failed deliveries for up to ~3 days with exponential backoff |
| GitHub | Retries for a period with increasing delay; delivery id in `X-GitHub-Delivery` |
| Generic | Typically 3–10 attempts over minutes to days |

Consequences:

1. **Every handler must be idempotent** (dedupe on `event.id`).
2. **Return `2xx` only after durable receipt**, so a retry means "we did not record it."
3. **Do not return `4xx` for transient internal failures** — the sender may stop retrying.
4. **`4xx` for invalid signatures/payload** is correct: retrying will not help.
5. **A timeout is a retry trigger.** If your handler takes longer than the sender's timeout, the
   sender assumes failure even if you eventually succeed.

### Respond fast, process later

```ts
app.post("/webhooks/stripe", express.raw({ type: "application/json" }), async (req, res) => {
  if (!verifyStripe(req.body, req.get("Stripe-Signature") ?? "", SECRET)) {
    return res.status(400).json({ error: "invalid_signature" });
  }

  const event = JSON.parse(req.body.toString("utf8"));

  // Durably enqueue, then ack immediately.
  await webhookInbox.insertOnce({ id: event.id, type: event.type, payload: event, receivedAt: new Date() });
  res.status(200).json({ received: true });
});
```

The queue worker processes the event asynchronously. The `2xx` means "recorded," not "fully applied."

## 33.12 — Webhook timeouts

Timeouts happen on both sides:

| Timeout | Where | Symptom |
| ------- | ----- | ------- |
| Sender timeout | Provider waits for `2xx` | Retry while your handler still runs |
| Gateway timeout | ALB/nginx | `504` to sender; handler may keep running |
| Handler timeout | Your DB/provider call | Slow response, retries |
| Processing timeout | Worker after ack | Job retried via queue |

Rules:

1. **Ack within the sender's timeout** (often 5–10 s). Do heavy work asynchronously.
2. **Keep the ack path short**: verify → insert inbox row → return.
3. **Do not call slow third parties before acking.** If you must, enqueue.
4. **Make the inbox insert idempotent** so a retry after a timeout does not duplicate.
5. **Track ack latency**; a p99 above the sender timeout is an outage in slow motion.

```text
Sender ──POST──▶ Endpoint ──verify──▶ INSERT inbox ──▶ 200 (≈20 ms)
                                  │
                                  └──▶ worker: apply projection (seconds/minutes)
```

## Worked example — WebhookIngest endpoint

```ts
app.post("/webhooks/stripe",
  express.raw({ type: "application/json", limit: "1mb" }),
  async (req, res) => {
    const started = Date.now();
    const signature = req.get("Stripe-Signature");

    if (!signature || !verifyStripe(req.body, signature, process.env.STRIPE_WEBHOOK_SECRET!)) {
      metrics.increment("webhook_signature_failed");
      return res.status(400).json({ error: "invalid_signature" });
    }

    let event: StripeEvent;
    try {
      event = JSON.parse(req.body.toString("utf8"));
    } catch {
      return res.status(400).json({ error: "invalid_json" });
    }

    try {
      await inbox.insertOnce(event);   // unique on event.id
      metrics.timing("webhook_ack_ms", Date.now() - started);
      return res.status(200).json({ received: true });
    } catch (err) {
      // Internal failure: return 5xx so the sender retries.
      log.error({ err, eventId: event.id }, "webhook inbox write failed");
      return res.status(503).json({ error: "temporarily_unavailable" });
    }
  },
);
```

Note the deliberate status choices: **400** for untrusted input, **200** for recorded, **503** for a
transient internal failure (so the sender retries).

## Key data / numbers

- Stripe signature header: `Stripe-Signature`, `t` + `v1`, HMAC-SHA256 over `"{t}.{raw_body}"`.
- Stripe default timestamp tolerance: **300 s**.
- Stripe retries failed deliveries for up to **~3 days** with exponential backoff.
- Recommended ack budget: **< 5 s** (well under typical 10 s sender timeouts).
- `express.raw()` is required; `express.json()` consumes the body and breaks raw verification.
- A `2xx` includes `200`, `201`, `202`, `204`; most senders treat any 2xx as success.

## Real-world use case — WebhookIngest

Acme's webhook endpoint called `BillingProjector.apply(event)` inline and then returned `200`. During
a database slowdown, the handler took 30 s; Stripe timed out at ~10 s and retried. Three deliveries
ran concurrently; two applied the same `invoice.paid`, double-crediting the tenant. The fix: verify →
insert into a `webhook_inbox` table with a unique `event_id` → return `200` in ~20 ms; a worker
processes the inbox asynchronously with dedupe. Double credits stopped immediately, and the endpoint's
p99 dropped from 30 s to 25 ms.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Process inline, then 2xx | Simple | Slow acks, retries, duplicates | Very fast handlers |
| Inbox + async worker | Fast ack, durable | Extra table/worker | Default |
| Return 2xx before verify | Fastest | Security hole | Never |
| Synchronous third-party call | Immediate result | Timeouts, retries | Rarely |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Verify HMAC on the raw body | Verify after JSON parsing |
| Use constant-time comparison | Compare with `===` |
| Enforce a timestamp tolerance | Accept arbitrarily old signatures |
| Ack after durable receipt | Ack before recording |
| Return `5xx` on transient failure | Return `200` to avoid retries |
| Dedupe on `event.id` | Process every delivery |

## Common mistakes

- **`express.json()` before verification** — the raw bytes are gone.
- **Comparing signatures with `===`** — timing side channel.
- **No timestamp check** — replay of an old signed payload.
- **Acking before the inbox write** — a crash loses the event.
- **Returning `400` on a DB blip** — the sender stops retrying valid events.
- **Heavy processing inline** — timeouts multiply deliveries.

## Checklist

- [ ] Is the raw body preserved for verification?
- [ ] Is the signature compared in constant time?
- [ ] Is there a timestamp tolerance to prevent replay?
- [ ] Is the event recorded durably before returning `2xx`?
- [ ] Is the inbox insert idempotent on `event.id`?
- [ ] Is the ack path under the sender's timeout?
- [ ] Are transient internal failures returned as `5xx`?
- [ ] Is ack latency measured?

## Related

- [Webhook Signature Verification — Mechanics](../02-deep-dive/01-webhook-signature-verification.md)
- [WebhookIngest Dedupe and Signature](../03-practical-examples/01-webhookingest-dedupe-and-signature.md)
- [Webhook Signature Verification — Mechanics](../02-deep-dive/01-webhook-signature-verification.md)
- [Chapter 33 Reference](../05-reference/README.md)
