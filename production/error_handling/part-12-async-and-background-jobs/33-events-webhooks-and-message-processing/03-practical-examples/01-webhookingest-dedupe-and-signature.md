# Practical — WebhookIngest with Dedupe and Signature

> Part XII · Chapter 33 · Sections 33.5, 33.10–33.12 · _Estimated reading time: 19 min_
> **Prerequisite:** [Webhook Signature Verification — Mechanics](../02-deep-dive/01-webhook-signature-verification.md)

## Scenario

`WebhookIngest` receives Stripe webhooks for Acme's billing. Requirements:

- reject forged or replayed requests before parsing,
- return `2xx` within ~100 ms,
- never process the same event twice, even across retries and deploys,
- return `5xx` only for transient internal failures so Stripe retries,
- keep the raw event for audit and DLQ replay.

## Architecture

```text
Stripe ──POST──▶ /webhooks/stripe
                   │ 1. verify signature (raw body)
                   │ 2. insert into webhook_inbox (unique event_id)
                   │ 3. return 200
                   ▼
             webhook_inbox (Postgres)
                   │
                   ▼
             BillingWorker ──▶ projection (idempotent)
                   │ failure
                   ▼
             billing-dlq + alarm
```

The endpoint does **no business logic**. It verifies, records, and acknowledges. The worker owns
processing and retries.

## Step 1 — Schema and inbox table

```sql
CREATE TABLE webhook_inbox (
  event_id     text PRIMARY KEY,
  type         text NOT NULL,
  api_version  text NOT NULL,
  payload      jsonb NOT NULL,
  status       text NOT NULL DEFAULT 'pending', -- pending | processing | done | failed
  attempts     int  NOT NULL DEFAULT 0,
  last_error   text,
  received_at  timestamptz NOT NULL DEFAULT now(),
  processed_at timestamptz
);

CREATE INDEX webhook_inbox_pending ON webhook_inbox (status, received_at)
  WHERE status IN ('pending', 'failed');
```

The primary key on `event_id` is the dedupe mechanism. No TTL; keep events for audit.

## Step 2 — Signature verification

```ts
import crypto from "node:crypto";

export function verifyStripe(
  rawBody: Buffer,
  header: string | undefined,
  secrets: string[],
  toleranceSec = 300,
): boolean {
  if (!header) return false;

  const parts = header.split(",").map((p) => p.split("="));
  const t = Number(parts.find(([k]) => k === "t")?.[1]);
  if (!Number.isFinite(t)) return false;
  if (Math.abs(Date.now() / 1000 - t) > toleranceSec) return false;

  const provided = parts.filter(([k]) => k === "v1").map(([, v]) => v);
  if (provided.length === 0) return false;

  return secrets.some((secret) => {
    const expected = crypto
      .createHmac("sha256", secret)
      .update(`${t}.${rawBody.toString("utf8")}`)
      .digest("hex");

    return provided.some(
      (sig) =>
        sig.length === expected.length &&
        crypto.timingSafeEqual(Buffer.from(sig, "hex"), Buffer.from(expected, "hex")),
    );
  });
}
```

Secrets come from the environment as an array so rotation works:

```ts
const SECRETS = [process.env.STRIPE_WEBHOOK_SECRET!, process.env.STRIPE_WEBHOOK_SECRET_PREV]
  .filter(Boolean);
```

## Step 3 — The endpoint

```ts
import express from "express";

const app = express();

// Raw body ONLY for this route, before any JSON middleware.
app.post(
  "/webhooks/stripe",
  express.raw({ type: "application/json", limit: "1mb" }),
  async (req, res) => {
    const started = Date.now();
    const signature = req.get("Stripe-Signature");

    if (!verifyStripe(req.body, signature, SECRETS)) {
      metrics.increment("webhook_signature_rejected");
      return res.status(400).json({ error: "invalid_signature" }); // do not retry
    }

    let event: StripeEvent;
    try {
      event = JSON.parse(req.body.toString("utf8"));
    } catch {
      metrics.increment("webhook_invalid_json");
      return res.status(400).json({ error: "invalid_json" });
    }

    try {
      const inserted = await db.query(
        `INSERT INTO webhook_inbox (event_id, type, api_version, payload)
         VALUES ($1, $2, $3, $4)
         ON CONFLICT (event_id) DO NOTHING
         RETURNING event_id`,
        [event.id, event.type, event.api_version ?? "unknown", event],
      );

      if (inserted.rowCount === 0) {
        metrics.increment("webhook_duplicate", { type: event.type });
        return res.status(200).json({ received: true, duplicate: true });
      }

      await wakeWorker(); // optional: LISTEN/NOTIFY or queue push
      metrics.timing("webhook_ack_ms", Date.now() - started);
      return res.status(200).json({ received: true });
    } catch (err) {
      // Transient internal failure: 5xx so Stripe retries.
      log.error({ err, eventId: event.id }, "webhook inbox write failed");
      metrics.increment("webhook_inbox_write_failed");
      return res.status(503).json({ error: "temporarily_unavailable" });
    }
  },
);

app.use(express.json()); // JSON for all other routes (mounted after)
```

Note the ordering: the raw parser is attached to the webhook route only; global JSON parsing is added
afterward.

## Step 4 — The worker (idempotent processing)

```ts
async function processInboxRow(row: InboxRow) {
  await db.query(
    `UPDATE webhook_inbox SET status = 'processing', attempts = attempts + 1 WHERE event_id = $1`,
    [row.event_id],
  );

  try {
    await db.transaction(async (tx) => {
      // Dedupe at the effect boundary too, in case of manual replays.
      const claimed = await tx.query(
        `INSERT INTO processed_events (consumer, event_id)
         VALUES ('BillingProjector', $1)
         ON CONFLICT DO NOTHING RETURNING event_id`,
        [row.event_id],
      );
      if (claimed.rowCount === 0) return;

      await billingProjector.apply(tx, row.payload);
    });

    await db.query(
      `UPDATE webhook_inbox SET status = 'done', processed_at = now() WHERE event_id = $1`,
      [row.event_id],
    );
  } catch (err) {
    const cls = classify(err);

    if (cls === "transient" && row.attempts < 6) {
      await db.query(
        `UPDATE webhook_inbox SET status = 'pending', last_error = $2 WHERE event_id = $1`,
        [row.event_id, toCode(err)],
      );
      return; // picked up by the next poll, with backoff in the query
    }

    await db.query(
      `UPDATE webhook_inbox SET status = 'failed', last_error = $2 WHERE event_id = $1`,
      [row.event_id, toCode(err)],
    );
    await dlq.publish({ eventId: row.event_id, type: row.type, code: toCode(err), attempts: row.attempts });
  }
}
```

Claiming the row with `status = 'processing'` plus `FOR UPDATE SKIP LOCKED` lets multiple workers poll
safely:

```sql
SELECT * FROM webhook_inbox
WHERE status = 'pending' AND received_at < now() - interval '5 seconds'
ORDER BY received_at
FOR UPDATE SKIP LOCKED
LIMIT 20;
```

## Step 5 — Status codes

| Situation | Response | Sender behavior |
| --------- | -------- | --------------- |
| Valid, recorded | `200` | Done |
| Valid, duplicate | `200` | Done (idempotent) |
| Invalid signature | `400` | No retry (correct) |
| Invalid JSON | `400` | No retry |
| Inbox write timeout | `503` | Retries (correct) |
| Unexpected exception | `500` | Retries |

Never return `200` for a failure you want retried, and never return `400` for an internal outage.

## Step 6 — Metrics and alarms

| Metric | Alarm |
| ------ | ----- |
| `webhook_signature_rejected` | Spike > baseline (attack or secret mismatch) |
| `webhook_ack_ms` p99 | > 1 s |
| `webhook_duplicate` | Informational |
| `webhook_inbox_write_failed` | Any sustained rate |
| `webhook_inbox_pending_age` | > 5 min |
| `webhook_inbox_failed` | > 0 |
| `billing_dlq_depth` | > 0 for 10 min |

## Real-world use case — WebhookIngest

Acme previously processed webhooks inline. During a 20-minute Postgres slowdown, Stripe timed out and
retried; multiple requests processed the same `invoice.paid`, granting entitlement three times. After
this design, the endpoint writes one row and returns in ~30 ms; the worker processes idempotently.
Stripe's retries hit the `ON CONFLICT DO NOTHING` path and returned `200` without reprocessing.
Signature rejections also surfaced a misconfigured secret during a rotation, caught by the alarm
before any billing impact.

## Key data / numbers

- Signature tolerance: **300 s**.
- Ack target: **< 100 ms p99** (endpoint does no business logic).
- Inbox dedupe: primary key on `event_id`, no TTL.
- Worker retry: **6 attempts** with backoff; then DLQ.
- Pending-row age alarm: **5 min**.
- Body limit: **1 MiB**.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Verify on raw bytes | Parse JSON first |
| Insert inbox row, then `200` | Apply business logic inline |
| Use `event_id` as dedupe | Dedupe on payload |
| Return `5xx` for internal failures | Return `200` to stop retries |
| Claim rows with `SKIP LOCKED` | Let two workers process one row |
| Keep raw events | Store only the projection |

## Checklist

- [ ] Signature verified on raw body with timestamp tolerance.
- [ ] Duplicate deliveries return `200` without reprocessing.
- [ ] Inbox insert is atomic and unique on `event_id`.
- [ ] Ack path performs no slow I/O.
- [ ] Transient failures return `5xx`.
- [ ] Worker is idempotent and claims rows safely.
- [ ] Failures go to a DLQ with event context.
- [ ] Ack latency and pending age are alarmed.

## Related

- [Webhook Signature Verification — Mechanics](../02-deep-dive/01-webhook-signature-verification.md)
- [Webhook Signatures, Retries, and Timeouts](../01-concepts/04-webhook-signatures-retries-timeouts.md)
- [Event Consumer Partial Batch and DLQ](./02-event-consumer-partial-batch-and-dlq.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
