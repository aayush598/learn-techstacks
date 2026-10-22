# Consistent Contracts Across Three Services

> Part IV · Chapter 10 · Sections 10.14–10.17 · _Estimated reading time: 22 min_
> **Prerequisite:** [Error Contracts Across Modules and Services](../01-concepts/04-contracts-across-modules-and-services.md)

## In one sentence

Three Acme components — the **Checkout API**, the **billing worker**, and the **WebhookIngest**
consumer — share **one envelope, one registry, and one compatibility policy**, so an error born
in Stripe is recognizable in all three, even when their deployments are weeks apart.

## Why this matters in production

Most "inconsistent error handling" incidents are contract incidents in disguise: the API said
`409`, the worker retried the same condition forever, and the webhook consumer returned `200` to
make Stripe stop — three behaviors for one root cause. Fixing each service individually guarantees
drift returns. Fixing the *contract* once makes drift a review failure instead of an outage.

## The topology

```text
 Stripe ──webhook──▶ WebhookIngest ──event──▶ Billing worker ──query──▶ Checkout API
    ▲                      │                        │                       │
    └──────────────────────┴──── one error contract ┴───────────────────────┘
                       (envelope + codes + correlation)
```

## Part 1 — The shared contract artifact

```ts
// packages/error-contract/src/index.ts — versioned, published, imported by all three
export interface ProblemDoc {
  type: string;            // "https://acme.example/errors/<CODE>" — identifier, not a fetchable doc
  title: string;
  status: number;
  detail?: string;         // human-safe, never raw vendor text
  instance?: string;       // route or resource reference
  code: string;            // stable app code, e.g. "BILLING_PROVIDER_DEGRADED"
  "request-id": string;
}

export const CODES = {
  BILLING_PROVIDER_DEGRADED: { status: 503, retryable: true },
  BILLING_INVOICE_FINALIZED: { status: 409, retryable: false },
  BILLING_DUPLICATE_CHARGE:  { status: 409, retryable: false },
  PAYMENT_CARD_DECLINED:     { status: 402, retryable: false },
  UPSTREAM_RATE_LIMITED:     { status: 429, retryable: true },
  WEBHOOK_SIGNATURE_INVALID: { status: 400, retryable: false },
} as const;

export function statusFor(code: string): number { return CODES[code as keyof typeof CODES]?.status ?? 500; }
export function isRetryable(code: string): boolean { return CODES[code as keyof typeof CODES]?.retryable ?? false; }
```

Note what is *in* the artifact: codes, statuses, retryability, envelope shape. Note what is
*out*: any service's internal exception classes (10.12 — the contract must not import features).

## Part 2 — Each producer, same shape, local ownership

```ts
// WebhookIngest — Stripe failures normalized at ITS boundary, then rendered with the shared shape
app.post("/webhooks/stripe", rawBody, async (req, res) => {
  if (!verifySignature(req)) {
    // terminal for the producer: Stripe will not fix our signature; do NOT 200
    return res.status(400).json(problem("WEBHOOK_SIGNATURE_INVALID", req.id));
  }
  try {
    await handleEvent(JSON.parse(req.body.toString()));
    res.status(200).json({ received: true });
  } catch (err) {
    const e = normalize(err);
    if (isRetryable(e.code)) return res.status(statusFor(e.code)).json(problem(e.code, req.id)); // Stripe retries
    await deadLetter(e, req.id);                        // permanent: record + 200-with-audit OR 400 per policy
    res.status(200).json({ received: true, skipped: e.code });
  }
});
```

```ts
// Billing worker — consumes events; failures carry THE SAME codes to the queue metadata
try { await finalizeInvoice(event); }
catch (err) {
  const e = normalize(err);
  await jobs.recordFailure({ code: e.code, correlationId: event.correlationId });
  if (!isRetryable(e.code)) await jobs.failTerminal({ code: e.code, dlq: true });
  else await jobs.retry({ delayMs: backoff(attempt), code: e.code });
}
```

```ts
// Checkout API — HTTP rendering via the same contract
catch (err) {
  const e = normalize(err);
  res.status(statusFor(e.code)).json({ ...problem(e.code, req.id), detail: safeDetail(e.code) });
}
```

Three producers, **one** vocabulary. A `BILLING_PROVIDER_DEGRADED` raised in the worker is the
same string the API would return and the same code the webhook consumer would log — because all
three import the same artifact.

## Part 3 — The consumer side: tolerance is mandatory

```ts
// Checkout API consuming a worker's error (or vice versa)
function classifyRemote(doc: ProblemDoc): AppError {
  const known = CODES[doc.code as keyof typeof CODES];
  if (known) return { code: doc.code, retryable: known.retryable, cause: doc };
  // unknown code (deploy skew): classify by STATUS CLASS, never crash, never 200-swallow
  if (doc.status >= 500 || doc.status === 429) return { code: "REMOTE_UNAVAILABLE", retryable: true, cause: doc };
  if (doc.status >= 400) return { code: "REMOTE_REJECTED", retryable: false, cause: doc };
  return { code: "REMOTE_MALFORMED", retryable: false, cause: doc };
}
```

This 10-line function is the entire defense against version skew (10.16). It is also what saved
Acme during the billing split: consumers on contract v1 met a v2 code and degraded to the right
class instead of hard-failing.

## Part 4 — Correlation across hops

```text
 Stripe delivery ──▶ WebhookIngest            worker queue                Checkout API
   (Stripe event id)   X-Request-Id: corr_5b8   message.correlationId      X-Request-Id: corr_5b8
                                                (unchanged end to end)
```

Rule: **the correlation ID is created at the first inbound hop and mutated by nobody.** Every
log line, failure record, and ProblemDoc carries it; support can walk one ID across all three
services (Chapter 6 defined it; this is where it earns its keep).

## Key data / numbers

- Envelope: RFC 9457 members `type`, `title`, `status`, `detail`, `instance` + app extensions
  `code`, `request-id`.
- Compatibility policy (recommendation): additive fields non-breaking; new codes non-breaking;
  changing a code's `status` or `retryable` flag **breaking** → bump the contract major version.
- Skew assumption to design for: producers/consumers at contract **N, N-1, N-2** coexist during
  rollouts.
- Retryability is part of the *contract*, not the implementation: `isRetryable()` is called by
  services that cannot see each other's code — changing it silently is an outage in slow motion.
- Webhook policy examples (real services): Stripe retries for up to **~3 days** with backoff;
  returning `2xx` acknowledges permanently — so `200`-for-permanent-skip must be *audited*, and
  `2xx` for transient failures is data loss.

## Real-world use case — Acme SaaS

During a Stripe incident, `BILLING_PROVIDER_DEGRADED` fired from the webhook consumer **and** the
billing worker simultaneously. Because all three components shared the artifact and the tolerance
rule:

- The webhook consumer retried (503-class) instead of acknowledging — no lost events.
- The worker's DLQ stayed empty (retryable), and invoices settled once Stripe recovered.
- The Checkout API surfaced `503` + `Retry-After` to the few in-flight checkout attempts.
- A consumer still on the previous contract version classified by status class and behaved
  identically, because `classifyRemote` treated unknown codes as their class.

One incident, three services, one behavior — and no coordinated deploy.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Shared contract artifact + tolerant consumers (shown) | Independent deploys, consistent behavior | Requires publishing discipline | Any multi-service system |
| Copy the tables into each repo | No coordination | Silent drift on first hotfix | Never |
| Hard lockstep deploys | Perfect consistency | Coupled release trains; slow | Only inside a monolith |
| Contract-first with schema registry | Strongest guarantees | Heavier tooling | High-volume regulated pipelines |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Publish codes + retryability as a versioned artifact | Redefine statuses per service |
| Classify unknown remote codes by status class | Throw on unknown codes or map to `200` |
| Propagate one correlation ID across all hops | Mint a new ID per service |
| Treat `retryable` as contract surface | Change retryability in a hotfix without a version bump |

## Common mistakes

- **Acknowledging transient webhook failures** — a `200` for a retryable error is silent data
  loss; classify first, acknowledge second.
- **Per-service `statusFor` copies** — they will diverge; derive every map from the artifact.
- **Contract tests that only check happy paths** — replay a recorded corpus of error bodies,
  including one unknown code, in each consumer's CI.

## Checklist

- [ ] One published artifact defines codes, statuses, retryability, and the envelope.
- [ ] All producers render through the shared serializer.
- [ ] All consumers have a tested `classifyRemote`-style tolerance path.
- [ ] Correlation IDs cross every hop unchanged.
- [ ] CI replays representative error bodies (including unknown codes) per consumer.

## Related

- [Error Contracts Across Modules and Services](../01-concepts/04-contracts-across-modules-and-services.md)
- [A Global Handler and Local Recovery, Together](./01-global-handler-and-local-recovery.md)
- [Chapter 49 — Error Contract Design and Versioning](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
- [Chapter 33 — Events, Webhooks, and Message Processing](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
