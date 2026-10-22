# Schema Validation and Version Incompatibility

> Part XII · Chapter 33 · Sections 33.8–33.9 · _Estimated reading time: 16 min_
> **Prerequisite:** [Delivery Guarantees, Duplicates, and Ordering](./02-delivery-guarantees-duplicates-and-ordering.md)

## In one sentence

Validate every inbound event against a **known schema version** at the trust boundary, and treat an
unknown or incompatible version as a **classified terminal outcome** — never as a crash that stalls
the consumer.

## Why this matters in production

Schemas evolve on the producer's schedule, not yours. A new required field, a renamed property, or a
type change (string → number) can make every event fail at once. If the consumer throws an
unclassified error, the partition stalls or the queue fills with poison messages. If it silently
coerces the new shape, it may write wrong data. Version-aware validation makes the incompatibility
**visible, contained, and replayable** after a fix.

## 33.8 — Schema validation

Validate at the **consumer boundary** even if the producer validates, because:

- the producer may be a third party (Stripe, GitHub),
- the event may have been mutated in transit,
- the schema may have drifted between deploy and consumer version,
- messages can be replayed from an old DLQ.

### What to validate

| Layer | Checks | Failure action |
| ----- | ------ | -------------- |
| **Envelope** | required attributes (`id`, `type`, `version`, `occurredAt`) | DLQ (malformed) |
| **Schema** | field types, required fields, enums | DLQ (invalid) |
| **Semantics** | date ranges, state transitions, referential existence | Business/terminal |
| **Authorization** | signature, tenant match | Reject (4xx / no ack) |

### Runtime validation

```ts
import { z } from "zod";

const InvoicePaidV1 = z.object({
  id: z.string().startsWith("evt_"),
  type: z.literal("invoice.paid"),
  version: z.literal(1),
  occurredAt: z.string().datetime(),
  data: z.object({
    invoiceId: z.string(),
    amountCents: z.number().int().nonnegative(),
    currency: z.string().length(3),
  }),
});

function parseEvent(body: unknown) {
  const envelope = z.object({ id: z.string(), type: z.string(), version: z.number() }).safeParse(body);
  if (!envelope.success) throw new InvalidEventError("INVALID_ENVELOPE", envelope.error);

  if (envelope.data.type === "invoice.paid" && envelope.data.version === 1) {
    const parsed = InvoicePaidV1.safeParse(body);
    if (!parsed.success) throw new InvalidEventError("INVALID_SCHEMA", parsed.error);
    return parsed.data;
  }

  throw new UnsupportedEventVersion(envelope.data.type, envelope.data.version);
}
```

Validation errors should carry the **event id and version**, so a DLQ record is triageable.

## 33.9 — Version incompatibility

Version incompatibility has several shapes, each with a different response:

| Situation | Example | Response |
| --------- | ------- | -------- |
| Consumer older than producer | Producer emits `v2`, consumer knows `v1` | DLQ + deploy consumer |
| Consumer newer than producer | Old `v1` events still arrive | **Upcast** `v1` → `v2` |
| Additive change | New optional field | Ignore unknown fields |
| Breaking change | Field renamed/removed | New event type or major version |
| Unknown event type | Producer adds `invoice.disputed` | DLQ/quarantine; never crash |
| Enum extension | New `status: "paused"` | Default branch + metric |

### Additive changes (preferred)

```ts
// v1 -> v2 added optional `discountCents`. Old consumers ignore it.
const InvoicePaidV2 = InvoicePaidV1.extend({
  data: InvoicePaidV1.shape.data.extend({ discountCents: z.number().int().nonnegative().optional() }),
});
```

Rules for compatible evolution:

1. **Never remove or rename a field** in a minor version.
2. **Never change a field's type** in place.
3. **Add optional fields**; require them only in a major version.
4. **Tolerate unknown fields** (`passthrough` or explicit ignore) so a newer producer does not break
   an older consumer.
5. **Use new event types** for genuinely new semantics.

### Upcasting old versions

Consumers should accept the versions they claim to support and **transform** older ones:

```ts
function upcast(raw: RawEvent): InvoicePaidV2 {
  if (raw.version === 2) return InvoicePaidV2.parse(raw);
  if (raw.version === 1) {
    const v1 = InvoicePaidV1.parse(raw);
    return { ...v1, version: 2, data: { ...v1.data, discountCents: 0 } };
  }
  throw new UnsupportedEventVersion(raw.type, raw.version);
}
```

Upcasting keeps one handler path and makes the compatibility decision explicit.

### Unknown versions and unknown types

`UnsupportedEventVersion` is **terminal but not an error in the business sense**. Options:

1. **DLQ** and page the owning team (safest for financial events).
2. **Quarantine topic** and continue (preserves partition throughput).
3. **Ignore with a metric** only when the type is explicitly out of scope.

Never let an unknown version throw an uncaught error that kills the consumer loop.

```ts
try {
  await applyEvent(raw);
} catch (err) {
  if (err instanceof UnsupportedEventVersion) {
    await quarantine.publish(raw, err);
    metrics.increment("event_unsupported_version", { type: err.type, version: err.version });
    return; // ack/quarantine, do not stall
  }
  throw err;
}
```

## Worked example — WebhookIngest schema drift

Stripe added a new `status` value to `subscription.updated`. Acme's consumer used a `switch` with no
default and threw `Unhandled status`, so the webhook endpoint returned `500`, Stripe retried, and the
DLQ filled with the same event. Billing projections for those tenants stopped.

```ts
const STATUS_MAP = {
  active: "active",
  trialing: "trialing",
  past_due: "past_due",
  canceled: "cancelled",
  unpaid: "past_due",
  paused: "paused",            // new
} as const;

function mapStatus(status: string) {
  const mapped = STATUS_MAP[status as keyof typeof STATUS_MAP];
  if (!mapped) {
    metrics.increment("unknown_subscription_status", { status });
    return "unknown";          // terminal-but-storable, not a crash
  }
  return mapped;
}
```

The fix was not "add `paused`" alone; it was the **default branch + metric + explicit `unknown`
state**, so the next new status is contained rather than fatal.

## Key data / numbers

- CloudEvents `specversion` attribute carries the envelope version (currently `1.0`).
- Stripe webhook events include `api_version` on the event object, which may lag your account version.
- JSON Schema / Zod validation at the boundary typically costs <1 ms for events under 10 KB.
- Unknown-field tolerance: most JSON parsers keep extra fields; strict schema validation should
  **strip** them explicitly, not reject.
- Support window recommendation: keep consumers able to read **N and N−1** versions for at least one
  deploy cycle (often 2–4 weeks).

## Real-world use case — Acme SaaS

Acme's `BillingProjector` consumed `invoice.created` `v1`. The producer added `v2` with
`amountCents` as a string to support large values. The consumer's validator rejected `v2` as a type
error on every event; the queue stalled for 40 minutes. They introduced explicit `v1`/`v2` schemas,
an upcaster from `v1` to a normalized internal shape, and a quarantine path for unknown versions.
The next breaking change was rolled out with a one-week dual-read window and no consumer downtime.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Strict validation | Catches drift early | Rejects additive changes | Financial events |
| Lenient (ignore unknown) | Forward compatible | Hides typos | Stable internal events |
| Upcasting | One handler path | More code | Multi-version support |
| New event type per version | Clean separation | More types | Major semantic changes |
| Quarantine unknown | Keeps partition moving | Requires triage | High-volume streams |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Validate envelope + payload at the boundary | Trust the producer blindly |
| Version every event | Rely on "it hasn't changed yet" |
| Tolerate unknown fields | Reject additive changes |
| Upcast old versions | Branch the whole handler everywhere |
| Quarantine unknown versions | Crash the consumer loop |
| Metric per unknown type/status | Silently ignore |

## Common mistakes

- **No version field** — impossible to reason about compatibility.
- **Strict schema rejects new fields** — an additive producer change takes down the consumer.
- **`switch` without default** — a new enum value throws.
- **Upcasting losing the original** — keep the raw event for audit.
- **Unknown events acked with no record** — silent loss.

## Checklist

- [ ] Does every event carry a type and version?
- [ ] Is the envelope validated before the payload?
- [ ] Are additive fields tolerated?
- [ ] Is there an explicit upcast path for old versions?
- [ ] Are unknown versions/types quarantined and measured?
- [ ] Do handlers have a safe default branch for enums?
- [ ] Is the raw event retained for audit/replay?

## Related

- [Out-of-order Events and Versioning — Mechanics](../02-deep-dive/03-out-of-order-events-and-versioning.md)
- [Delivery Guarantees, Duplicates, and Ordering](./02-delivery-guarantees-duplicates-and-ordering.md)
- [Out-of-Order Events and Versioning — Mechanics](../02-deep-dive/03-out-of-order-events-and-versioning.md)
- [Chapter 33 Reference](../05-reference/README.md)
